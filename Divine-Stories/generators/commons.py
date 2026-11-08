"""Wikimedia Commons asset fetcher with licence filtering and attribution tracking.

Uses the public MediaWiki Action API (no key, no billing):
  action=query & generator=search (namespace 6 = File) & prop=imageinfo & iiprop=url|size|mime|extmetadata
Only files whose machine licence is public domain, CC0 or plain CC BY are accepted (no SA/NC/ND).
Every accepted file is recorded in assets/manifest.json with author, licence, licence URL and source page.
Downloads are cached by title, so an approved image is never fetched twice.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import requests

from config import settings as S
from generators.log import log


@dataclass
class CommonsAsset:
    title: str
    page_url: str
    url: str            # the (thumbnail) URL actually downloaded
    width: int
    height: int
    license: str        # machine licence code, e.g. "pd", "cc0", "cc-by-4.0"
    license_name: str   # human name, e.g. "Public domain"
    license_url: str
    artist: str
    credit: str
    description: str
    local: str = ""     # path relative to project root once downloaded

    @property
    def attribution(self) -> str:
        who = self.artist or "Unknown author"
        lic = self.license_name or self.license
        return f'"{self.title.removeprefix("File:")}" by {who}, {lic}, via Wikimedia Commons ({self.page_url})'


def _strip_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    return " ".join(html.unescape(s).split())


def license_ok(code: str, name: str = "") -> bool:
    """True for public domain, CC0 and CC BY (any version); False for SA/NC/ND/GFDL/unknown."""
    c = (code or "").lower().strip()
    n = (name or "").lower()
    if not c and not n:
        return False
    if any(m in c for m in S.BLOCKED_LICENSE_MARKERS) or any(m in n for m in ("share alike", "sharealike", "-sa ",
                                                                                 "noncommercial", "noderiv", "gfdl")):
        return False
    if c.startswith("pd") or c == "cc0" or n.startswith("public domain") or n == "cc0":
        return True
    return bool(re.fullmatch(r"cc-by(-\d(\.\d)?)?", c))


def _session() -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = S.HTTP_USER_AGENT
    return s


def _get(sess: requests.Session, params: dict, retries: int = 3) -> dict:
    for attempt in range(retries):
        try:
            r = sess.get(S.COMMONS_API, params={**params, "format": "json", "formatversion": 2}, timeout=30)
            if r.status_code == 429:
                time.sleep(5 * (attempt + 1))
                continue
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            log("commons", f"request failed ({e}); retry {attempt + 1}/{retries}")
            time.sleep(2 * (attempt + 1))
    raise RuntimeError("Commons API unreachable")


def _to_asset(page: dict) -> CommonsAsset | None:
    infos = page.get("imageinfo") or []
    if not infos:
        return None
    ii = infos[0]
    if ii.get("mime") not in ("image/jpeg", "image/png", "image/tiff", "image/webp"):
        return None
    meta = {k: (v.get("value") if isinstance(v, dict) else v) for k, v in (ii.get("extmetadata") or {}).items()}
    return CommonsAsset(
        title=page["title"],
        page_url=ii.get("descriptionurl", ""),
        url=ii.get("thumburl") or ii.get("url", ""),
        width=int(ii.get("width", 0)),
        height=int(ii.get("height", 0)),
        license=_strip_html(meta.get("License", "")).lower(),
        license_name=_strip_html(meta.get("LicenseShortName", "")),
        license_url=_strip_html(meta.get("LicenseUrl", "")),
        artist=_strip_html(meta.get("Artist", "")),
        credit=_strip_html(meta.get("Credit", "")),
        description=_strip_html(meta.get("ImageDescription", ""))[:400],
    )


IIPROP = {"prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": S.COMMONS_THUMB_WIDTH}


def search(query: str, limit: int = 20, min_side: int = 900) -> list[CommonsAsset]:
    """Search File: pages; return only licence-approved, large-enough images."""
    data = _get(_session(), {"action": "query", "generator": "search", "gsrsearch": query, "gsrnamespace": 6,
                             "gsrlimit": limit, **IIPROP})
    out = []
    for page in (data.get("query") or {}).get("pages", []):
        a = _to_asset(page)
        if a and license_ok(a.license, a.license_name) and min(a.width, a.height) >= min_side:
            out.append(a)
    return out


RIGHTS_OVERRIDES = S.ASSETS / "rights_overrides.json"


def rights_block(title: str, today: str | None = None) -> str | None:
    """Reason string if a human rights review blocks this title (today = ISO date), else None."""
    import datetime as _dt

    if not RIGHTS_OVERRIDES.exists():
        return None
    o = json.loads(RIGHTS_OVERRIDES.read_text(encoding="utf-8")).get(title)
    if not o:
        return None
    today = today or _dt.date.today().isoformat()
    if o["status"] == "blocked" or (o["status"] == "blocked_until" and today < o["until"]):
        return o["reason"]
    return None


def lookup(titles: list[str]) -> list[CommonsAsset]:
    """Fetch metadata for exact File: titles (licence-filtered, rights overrides applied)."""
    data = _get(_session(), {"action": "query", "titles": "|".join(titles), **IIPROP})
    out = []
    for page in (data.get("query") or {}).get("pages", []):
        a = _to_asset(page)
        if a is None:
            log("commons", f"no image info for {page.get('title')}")
        elif reason := rights_block(a.title):
            log("commons", f"REJECTED by rights review: {a.title} ({reason})")
        elif not license_ok(a.license, a.license_name):
            log("commons", f"REJECTED licence {a.license!r}/{a.license_name!r}: {a.title}")
        else:
            out.append(a)
    return out


# ---------------------------------------------------------------- manifest + cache

def load_manifest() -> dict[str, dict]:
    if S.ASSET_MANIFEST.exists():
        return json.loads(S.ASSET_MANIFEST.read_text(encoding="utf-8"))
    return {}


def save_manifest(m: dict[str, dict]) -> None:
    S.ASSET_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    S.ASSET_MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")


def local_name(title: str, url: str) -> str:
    ext = Path(url.split("?")[0]).suffix.lower() or ".jpg"
    if ext in (".tif", ".tiff"):
        ext = ".jpg"
    stem = re.sub(r"[^A-Za-z0-9]+", "_", title.removeprefix("File:"))[:60].strip("_")
    return f"{stem}_{hashlib.sha1(title.encode()).hexdigest()[:8]}{ext}"


def ensure(titles: list[str]) -> dict[str, Path]:
    """Download (once) every licence-approved title; return {title: local path}. Rejects are skipped and logged."""
    manifest = load_manifest()
    have = {t: S.ROOT / manifest[t]["local"] for t in titles
            if t in manifest and (S.ROOT / manifest[t]["local"]).exists()}
    need = [t for t in titles if t not in have]
    if need:
        S.ASSET_CACHE.mkdir(parents=True, exist_ok=True)
        sess = _session()
        for i in range(0, len(need), 40):
            for a in lookup(need[i:i + 40]):
                dest = S.ASSET_CACHE / local_name(a.title, a.url)
                if not dest.exists():
                    try:
                        _download(sess, a.url, dest, retries=3)
                    except RuntimeError:
                        # originals are throttled harder than cached standard-size thumbnails
                        log("commons", f"falling back to a 960px thumbnail for {a.title}")
                        d = _get(sess, {"action": "query", "titles": a.title, "prop": "imageinfo",
                                        "iiprop": "url", "iiurlwidth": 960})
                        thumb = d["query"]["pages"][0]["imageinfo"][0]["thumburl"]
                        _download(sess, thumb, dest, retries=3)
                        a.url = thumb.split("?")[0]
                    log("commons", f"downloaded {a.title} -> {dest.name} ({dest.stat().st_size // 1024} KB)")
                    time.sleep(2.0)  # be polite; upload.wikimedia.org rate-limits bursts
                a.local = dest.relative_to(S.ROOT).as_posix()
                manifest[a.title] = {**asdict(a), "attribution": a.attribution,
                                     "sha256": hashlib.sha256(dest.read_bytes()).hexdigest()}
                have[a.title] = dest
                save_manifest(manifest)   # incremental: a later failure keeps earlier work
    return have


def _download(sess: requests.Session, url: str, dest: Path, retries: int = 5) -> None:
    url = url.split("?")[0]   # drop utm_* tracking params Commons appends
    for attempt in range(retries):
        r = sess.get(url, timeout=60)
        if r.status_code == 429:
            wait = int(r.headers.get("retry-after", "0") or 0) or 30 * (attempt + 1)
            log("commons", f"429 rate-limited; waiting {wait}s")
            time.sleep(wait)
            continue
        r.raise_for_status()
        if not r.headers.get("content-type", "").startswith("image/"):
            raise RuntimeError(f"unexpected content-type {r.headers.get('content-type')} for {url}")
        tmp = dest.with_suffix(dest.suffix + ".part")
        tmp.write_bytes(r.content)
        tmp.replace(dest)
        return
    raise RuntimeError(f"download failed after {retries} attempts: {url}")


if __name__ == "__main__":  # quick manual search: python -m generators.commons "query words"
    import sys

    for a in search(" ".join(sys.argv[1:]) or "Shiva painting", limit=30):
        print(f"{a.width}x{a.height}  {a.license:<12} {a.title}  | {a.artist[:50]}")
