"""YouTube Partner Program gate: runs BEFORE narration/render and blocks risky stories.

Targets YPP's "reused content", "inauthentic (mass-produced / repetitive) content" and misleading-metadata/spam
rules. Divine Stories deliberately uses public-domain artworks, so on top of the repetition checks it enforces
that each video is a transformation (original narration carries the video; every shot is animated) rather than a
slideshow of other people's work.

BLOCKS when:
  - narration repeats another story (4-word phrase overlap > MAX_OVERLAP)
  - topic / Hindi title / slug duplicates another story
  - the same narrative template was used by the last MAX_TEMPLATE_RUN rendered Shorts
  - the closing scene (question/CTA) repeats either of the last two rendered Shorts
  - visuals reuse >= MAX_ASSET_REUSE of the images of any earlier rendered Short
  - any shot is static (no zoom/pan change) or has no added atmosphere
  - an asset is missing from the licence manifest, not PD/CC0/CC BY, or blocked by the rights review
  - off-platform calls to action (DM, link in bio...) - Shorts viewers can't follow them
WARNS on clickbait words (allowed only if literally true) and long runs of the same screen layout.

Passing this gate does NOT guarantee monetization; it removes the known, checkable risks.
Render order is kept in qc/policy_history.json.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from config import settings as S
from generators.commons import license_ok, load_manifest, rights_block
from story import schema

HISTORY = S.ROOT / "qc" / "policy_history.json"
MAX_OVERLAP = 0.25        # share of this narration's 4-word phrases allowed in any other story
MAX_ENDING_OVERLAP = 0.5  # closing scene vs the last two Shorts
MAX_TEMPLATE_RUN = 3      # same narrative template allowed this many times in a row
MAX_ASSET_REUSE = 0.5     # share of this video's images that may come from a single earlier Short
LAYOUT_WARN_RUN = 5       # same screen layout this many in a row -> warning (build a layout variant)
MIN_ZOOM_CHANGE = 0.08

OFF_PLATFORM = re.compile(r"(डीएम|\bDM\b|इनबॉक्स|\binbox\b|link in bio|लिंक इन बायो|\bbio\b|बायो|व्हाट्सएप|whatsapp)",
                          re.IGNORECASE)
CLICKBAIT = re.compile(r"(सच्चाई छुपाई|कोई नहीं जानता|100%|गारंटी|guaranteed|secret|सीक्रेट|banned|बैन|shocking|"
                       r"चौंकाने वाला|miracle|चमत्कार पक्का)", re.IGNORECASE)


def _words(story: dict) -> list[str]:
    return [w.strip("।,.?!…\"'").lower() for s in story["scenes"] for w in s["narration"].split()
            if w.strip("।,.?!…\"'")]


def shingles(words: list[str], n: int = 4) -> set[tuple]:
    return {tuple(words[i:i + n]) for i in range(len(words) - n + 1)}


def _norm(s: str) -> str:
    return re.sub(r"[\W_]+", "", (s or "").lower())


def load_history() -> dict:
    if HISTORY.exists():
        return json.loads(HISTORY.read_text(encoding="utf-8"))
    return {"order": []}


def _library(exclude: str) -> dict[str, dict]:
    out = {}
    for p in sorted(S.STORY_LIBRARY.glob("*.json")):
        try:
            st = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:   # a broken neighbour must not silently hide a duplicate
            print(f"[ypp] could not read {p.name}: {e}")
            continue
        if st.get("slug") != exclude:
            out[st.get("slug", p.stem)] = st
    return out


def evaluate(story: dict, library: dict[str, dict] | None = None, history: dict | None = None,
             manifest: dict | None = None) -> tuple[list[str], list[str]]:
    """Return (problems, warnings). Pure function so it can be unit-tested."""
    slug = story["slug"]
    library = _library(slug) if library is None else library
    history = load_history() if history is None else history
    manifest = load_manifest() if manifest is None else manifest
    problems, warnings = [], []

    # 1. originality vs every other story in the library
    mine = shingles(_words(story))
    for other_slug, other in library.items():
        if _norm(other.get("topic")) == _norm(story["topic"]):
            problems.append(f'topic duplicates "{other_slug}"')
        if _norm(other.get("title_hi")) == _norm(story["title_hi"]):
            problems.append(f'Hindi title duplicates "{other_slug}"')
        if mine:
            ov = len(mine & shingles(_words(other))) / len(mine)
            if ov > MAX_OVERLAP:
                problems.append(f"{ov:.0%} of the narration repeats {other_slug} (limit {MAX_OVERLAP:.0%})")

    # 2. repetition vs the Shorts rendered before this one
    order = history["order"]
    before = [e for e in (order[:next((i for i, e in enumerate(order) if e["slug"] == slug), len(order))])]
    tmpl = story.get("template", "")
    run = [e["slug"] for e in before[-MAX_TEMPLATE_RUN:] if e.get("template") == tmpl]
    if tmpl and len(run) == MAX_TEMPLATE_RUN:
        problems.append(f'narrative template "{tmpl}" used by the last {MAX_TEMPLATE_RUN} Shorts ({", ".join(run)}) '
                        f"- pick another template so the channel isn't one formula repeated")
    layout = story.get("layout", "classic")
    lrun = [e["slug"] for e in before[-LAYOUT_WARN_RUN:] if e.get("layout", "classic") == layout]
    if len(lrun) == LAYOUT_WARN_RUN:
        warnings.append(f'screen layout "{layout}" used by the last {LAYOUT_WARN_RUN} Shorts - add a layout variant '
                        f"(caption style, label position, transitions) soon")
    ending = shingles([w.strip("।,.?!…").lower() for w in story["scenes"][-1]["narration"].split()], 3)
    for e in before[-2:]:
        prev_end = shingles([w.lower() for w in e.get("ending", "").split()], 3)
        if ending and prev_end and len(ending & prev_end) / len(ending) >= MAX_ENDING_OVERLAP:
            problems.append(f'closing question/CTA repeats {e["slug"]} - write a different ending')
    assets = {s["visual"]["asset"] for s in story["scenes"]}
    for e in before:
        reuse = len(assets & set(e.get("assets", []))) / max(1, len(assets))
        if reuse >= MAX_ASSET_REUSE:
            problems.append(f"{reuse:.0%} of the images were already used in {e['slug']} (limit "
                            f"{MAX_ASSET_REUSE:.0%}) - find fresh artwork")

    # 3. transformation, not a slideshow of public-domain art
    for s in story["scenes"]:
        v = s["visual"]
        z = v.get("zoom", [1.0, 1.0])
        moving = abs(z[1] - z[0]) >= MIN_ZOOM_CHANGE or any(abs(p) >= 0.03 for p in v.get("pan", [0, 0]))
        if not moving:
            problems.append(f"{s['id']}: static shot (zoom change < {MIN_ZOOM_CHANGE} and no pan)")
        if not v.get("effects"):
            problems.append(f"{s['id']}: no atmosphere layers - plain artwork on screen")
        if not s.get("narration", "").strip():
            problems.append(f"{s['id']}: no narration - the original commentary must carry every shot")

    # 4. licensing (before any render work is spent)
    for a in sorted(assets):
        m = manifest.get(a)
        if not m:
            problems.append(f"asset not downloaded/approved: {a} (run: python main.py assets <story>)")
        elif not license_ok(m["license"], m["license_name"]):
            problems.append(f"licence not allowed for {a}: {m['license']}")
        elif reason := rights_block(a):
            problems.append(f"rights review blocks {a}: {reason}")

    # 5. misleading / spammy text
    shown = " ".join([story["title_hi"]] + [s["narration"] for s in story["scenes"]] +
                     [s.get("label", "") + " " + s.get("title", "") for s in story["scenes"]] +
                     story.get("upload", {}).get("titles", []))
    if m := OFF_PLATFORM.search(shown):
        problems.append(f'off-platform call to action "{m.group(0)}" - ask for a comment instead')
    for w in sorted({m.group(0) for m in CLICKBAIT.finditer(shown)}):
        warnings.append(f'"{w}" in title/narration - keep only if literally true (misleading-metadata risk)')
    return problems, warnings


def check(story: dict) -> None:
    """Block the render on problems; on success record this Short in the render order."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
    problems, warnings = evaluate(story)
    if problems:
        raise SystemExit("[ypp] Render blocked - reused/repetitive/misleading content risk:\n  - "
                         + "\n  - ".join(problems))
    for w in warnings:
        print(f"[ypp] WARNING: {w}")
    hist = load_history()
    entry = {"slug": story["slug"], "template": story.get("template", ""), "layout": story.get("layout", "classic"),
             "ending": " ".join(w.strip("।,.?!…").lower() for w in story["scenes"][-1]["narration"].split()),
             "assets": sorted({s["visual"]["asset"] for s in story["scenes"]})}
    hist["order"] = [e for e in hist["order"] if e["slug"] != story["slug"]]
    # keep the original position if re-rendered, else append
    old = load_history()["order"]
    idx = next((i for i, e in enumerate(old) if e["slug"] == story["slug"]), None)
    if idx is None:
        hist["order"].append(entry)
    else:
        hist["order"].insert(idx, entry)
    HISTORY.write_text(json.dumps(hist, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[ypp] OK - original narration ({len(shingles(_words(story)))} phrases checked), unique topic, "
          f"animated shots, licensed art; template {story.get('template')}, layout {story.get('layout', 'classic')}")
