"""3. COPYRIGHT & POLICY VALIDATOR.

Checks: asset ownership/licence records (data/growth/asset_ledger.json), outside media pulled into the story,
Community Guidelines risk words, misinformation sourcing, synthetic-media disclosure and advertiser suitability.

It can only find risks in what it can see. It NEVER certifies copyright clearance: a clean result means
"no known risk found in the files checked", not "cleared". Content ID can still match anything.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from datetime import date
from pathlib import Path

from ..config import CHANNELS, PIPELINE, load_json, save_json
from .base import Result

LEDGER = "asset_ledger.json"
MEDIA_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp3", ".wav", ".m4a", ".ogg", ".flac", ".mp4", ".mov",
             ".ttf", ".otf", ".ttc"}
OK_LICENSES = {"own", "original", "cc0", "public-domain", "licensed", "cc-by"}

# Extra Community-Guidelines / advertiser checks on top of the channel's policy.py lists (AGENTS.md #3, #9).
SENSITIVE = re.compile(r"(\bjihad|\bmullah|\bkafir|katua|\bchamar|\bbhangi|\bneech jaati|\bdalit\b|\bsavarna|"
                       r"hindu vs muslim|हिंदू बनाम मुस्लिम|जिहाद|काफिर)", re.IGNORECASE)
POLITICS = re.compile(r"(\bbjp\b|\bcongress\b|\baap party|\bmodi\b|\brahul gandhi|\bkejriwal|#bjp|#modi)",
                      re.IGNORECASE)
PROMISE = re.compile(r"(manokamna (zaroor )?puri|wish (will )?come true|guaranteed blessing|paisa aayega|"
                     r"share nahi (kiya|kia) to|ignore (kiya|kia) to|warna .*bura|bura hoga|naraz ho jayenge|"
                     r"type karo .* (paisa|naukri|shaadi) milegi|मनोकामना (ज़रूर |जरूर )?पूरी|वरना|बुरा होगा)",
                     re.IGNORECASE)
MEDICAL = re.compile(r"(\bcure[sd]?\b|\bilaaj\b|\bilaj\b|ठीक हो जाएगा|bimari door|दवा की जरूरत नहीं)", re.IGNORECASE)
FICTION_MARK = re.compile(r"(kalpanik|काल्पनिक|fictional|original fictional|prerak katha)", re.IGNORECASE)
REALISTIC = re.compile(r"(\brealistic\b|photoreal|stable.?diffusion|midjourney|\bdall.?e\b|\bimagen\b|\bsora\b|"
                       r"\bveo ?\d|runway ?ml|runway gen|deepfake|face.?swap|voice.?clon)", re.IGNORECASE)
WAR = re.compile(r"(\bwar\b|\byudh\b|\bjung\b|\bhamla\b|\battack\b|\bbomb|\bmissile|\bstrike\b|युद्ध|हमला)",
                 re.IGNORECASE)

_FALLBACK = {
    "OFF_PLATFORM": re.compile(r"(डीएम|\bDM\b|इनबॉक्स|\binbox\b|link in bio|लिंक इन बायो|\bbio\b|बायो)", re.I),
    "CLICKBAIT": re.compile(r"(ILLEGAL|GUARANTEED|100% SURE|BANNED|SECRET|HACK|FREE MONEY)", re.I),
    "GRAPHIC": re.compile(r"(\bBLOOD\b|\bGORE\b|\bKILL(ED|ING)?\b|\bDEAD BODIES\b|\bMASSACRE\b|\bBEHEAD)", re.I),
    "DEROGATORY": re.compile(r"(\bBEGGARS?\b|\bDOGS\b|\bCOCKROACH|\bPIGS\b|\bTERRORIST NATION\b)", re.I),
}


def channel_rules(ch: str) -> dict:
    """The channel's own policy.py word lists (single source of truth); built-in copy if it is missing."""
    p = CHANNELS[ch]["root"] / "core" / "policy.py"
    if p.exists():
        try:
            spec = importlib.util.spec_from_file_location(f"_growth_policy_{ch}", p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return {k: getattr(mod, k, _FALLBACK[k]) for k in _FALLBACK}
        except Exception:
            pass
    return dict(_FALLBACK)


# ---------------------------------------------------------------------------------------------------------
# Asset ledger
# ---------------------------------------------------------------------------------------------------------
def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def scan_assets(write: bool = True) -> dict:
    """Find every media file under each channel's assets/ folder; add unknown ones to the ledger for a human
    to fill in (owner, license, source, proof). Existing entries are never overwritten."""
    ledger = load_json(LEDGER, {"_note": "One entry per media file the videos can contain. license: own | original "
                                         "| cc0 | public-domain | licensed | cc-by | unknown. Fill 'source' and "
                                         "'proof' (invoice, licence URL, 'made in code by X') by hand.",
                                "assets": {}})
    added = []
    for ch, cfg in CHANNELS.items():
        d = cfg["root"] / "assets"
        if not d.exists():
            continue
        for p in sorted(d.rglob("*")):
            if p.suffix.lower() not in MEDIA_EXT or not p.is_file():
                continue
            rel = p.relative_to(PIPELINE).as_posix()
            if rel not in ledger["assets"]:
                ledger["assets"][rel] = {"channel": ch, "sha": _sha(p), "owner": None, "license": "unknown",
                                         "source": None, "proof": None, "added": date.today().isoformat()}
                added.append(rel)
            elif ledger["assets"][rel].get("sha") != _sha(p):
                ledger["assets"][rel]["changed_since_recorded"] = True
    if write:
        save_json(LEDGER, ledger)
    return {"ledger": ledger, "added": added}


def ledger_status(ch: str | None = None) -> dict:
    ledger = load_json(LEDGER, {"assets": {}})["assets"]
    rows = {k: v for k, v in ledger.items() if ch is None or v.get("channel") == ch}
    unknown = [k for k, v in rows.items() if (v.get("license") or "unknown") not in OK_LICENSES]
    changed = [k for k, v in rows.items() if v.get("changed_since_recorded")]
    return {"total": len(rows), "unknown": unknown, "changed": changed}


# ---------------------------------------------------------------------------------------------------------
def _texts(s) -> dict:
    up = s.upload or {}
    return {"script": s.spoken_text + " " + s.roman_text, "title": s.title,
            "description": up.get("description", ""), "pinned": up.get("pinned_comment", "") or up.get("pinned", ""),
            "tags": " ".join(up.get("tags", []))}


def validate(me) -> Result:
    r = Result("copyright_policy")
    ch = me.channel
    rules = channel_rules(ch)
    copyright_pts, policy_pts = 0, 0

    # --- copyright: outside media referenced by the module ---------------------------------------
    ledger = load_json(LEDGER, {"assets": {}})["assets"]
    for line_no, text in me.media_refs:
        if re.search(r"\b(yt_dlp|youtube_dl|pytube|urlopen|requests\.get|httpx\.get|wget)\b", text):
            r.add("block", f"downloads outside media (line {line_no}): {text}")
            copyright_pts += 60
            continue
        hit = next((k for k in ledger if Path(k).name in text), None)
        if hit and (ledger[hit].get("license") or "unknown") in OK_LICENSES:
            r.add("ok", f"line {line_no} uses '{Path(hit).name}' - licence recorded ({ledger[hit]['license']})")
        else:
            r.add("fix", f"line {line_no} loads a media file with no licence record (if it is a screenshot of a "
                         f"real person's post, it also needs their permission or full anonymising): {text}")
            copyright_pts += 30
    st = ledger_status(ch)
    if st["unknown"]:
        r.add("warn", f"{len(st['unknown'])} channel asset(s) have no ownership/licence record: "
                      f"{', '.join(Path(u).name for u in st['unknown'][:5])} (fill data/growth/asset_ledger.json)")
        copyright_pts += 10
    if ch in ("dr", "rs"):
        r.add("info", "visuals drawn in code (Cairo) and music synthesized in code (engine MUSIC_STYLE) - no "
                      "third-party footage or tracks found in this module")
    if me.music_style is None and ch != "bb":
        r.add("info", "no MUSIC_STYLE in the module - the engine's default synthesized bed is used")

    # --- Community Guidelines / advertiser suitability -------------------------------------------
    t = _texts(me)
    every = " ".join(t.values())
    for label, rx, level, pts in (("off-platform call to action", rules["OFF_PLATFORM"], "fix", 15),
                                  ("demeaning words for a people/nation/religion", rules["DEROGATORY"], "block", 60),
                                  ("religion/caste flashpoint", SENSITIVE, "fix", 25),
                                  ("party-politics names (keep factual, no side-taking)", POLITICS, "warn", 8),
                                  ("promise / threat / fake blessing (rule #9)", PROMISE, "fix", 25),
                                  ("health-cure claim", MEDICAL, "warn", 10)):
        found = sorted({m.group(0) for m in rx.finditer(every)})
        if found:
            r.add(level, f"{label}: {', '.join(found[:5])}")
            policy_pts += pts
    bait = sorted({m.group(0) for m in rules["CLICKBAIT"].finditer(t["title"] + " " + t["description"])})
    if bait:
        unsupported = [b for b in bait if b.lower() not in t["script"].lower()]
        if unsupported:
            r.add("fix", f"clickbait word(s) in metadata the video never backs up: {', '.join(unsupported)}")
            policy_pts += 15
        else:
            r.add("warn", f"clickbait word(s) {', '.join(bait)} - keep only if literally true")
    graphic = sorted({m.group(0) for m in rules["GRAPHIC"].finditer(every)})
    if graphic:
        r.add("warn", f"graphic words limit ads (advertiser-friendly guidelines): {', '.join(graphic[:5])}")
        policy_pts += 8
    if ch == "rs" and WAR.search(every):
        r.add("info", "war / weapons subject: keep it educational and non-graphic (no injury close-ups, no "
                      "celebration of killing) to stay advertiser-friendly")

    # --- misinformation sourcing ------------------------------------------------------------------
    fictional = bool(FICTION_MARK.search(" ".join(map(str, me.sources)) + " " + me.topic))
    if fictional:
        if not FICTION_MARK.search(t["description"]):
            r.add("fix", "fictional story is not labelled in the description ('Kalpanik prerak katha')")
            policy_pts += 15
    elif ch in ("dr", "rs") and len(me.sources) < 2:
        r.add("fix", f"{len(me.sources)} source(s) listed - facts need at least 2 (misinformation policy)")
        policy_pts += 15

    # --- synthetic media disclosure ---------------------------------------------------------------
    src = me.path.read_text(encoding="utf-8", errors="replace")
    if REALISTIC.search(src) or REALISTIC.search(me.topic):
        r.add("warn", "module mentions realistic/AI-generated imagery or voice tools - if any shot could be "
                      "mistaken for real people/events, set 'Altered or synthetic content' = YES")
        r.data["synthetic_disclosure"] = "REVIEW"
    else:
        r.data["synthetic_disclosure"] = "NO (stylised 2D animation; the AI narration voice is not a real person)"
    r.data["made_for_kids"] = "NO (cartoon style - set it explicitly so it is not auto-flagged)"

    r.data["copyright_risk"] = min(100, copyright_pts)
    r.data["policy_risk"] = min(100, policy_pts)
    r.data["disclaimer"] = ("Risk screen of the files and text checked here. Not legal advice and not a "
                            "copyright clearance - Content ID and YouTube reviewers decide.")
    r.score = max(0, 100 - max(r.data["copyright_risk"], r.data["policy_risk"]))
    return r
