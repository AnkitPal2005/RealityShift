"""YouTube Partner Program gate, run by engine.render() before any narration is generated.

Blocks a render that would risk YPP's "reused content" / "inauthentic (mass-produced, repetitive)
content" policies, or its misleading-metadata / spam rules:
  - narration that repeats another Short's script (4-word shingle overlap above MAX_OVERLAP)
  - a TOPIC already used by another Short
  - third-party media pulled into the story (video/image/audio files, downloads, stock clips)
  - the same screen layout as the last MAX_LAYOUT_RUN Shorts in a row (one template, mass-produced)
  - the same ending (CTA devices) as either of the last two Shorts
  - off-platform calls to action ("DM me", "link in bio/inbox") that YouTube viewers can't follow
  - the same opening words as a recent Short, or a stock hook ("क्या आपको पता है")
  - the same music style as the previous Short, a style already used twice in the last three, or a tempo
    within MIN_BPM_STEP of the previous Short (one bed under every video reads as a template)
  - no SOURCES for the facts (misinformation), no UPLOAD kit / thumbnail (packaging is checked in upload_kit.py)
  - derogatory words for a people, nation or religion (hate / harassment)
and warns about clickbait words that must be literally true, graphic/violent words that limit ads, and a
closing line or scene count copied from recent Shorts.
Everything else in the pipeline is original by construction: Cairo-drawn visuals, synthesized
music (seeded per story, style rotated, see engine.MUSIC_STYLES) and synthesized SFX.

Render order lives in policy_history.json (committed with the code). Shorts made before the template
rules existed are listed under "grandfathered" so they can still be re-rendered as published.
"""

import ast
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HISTORY = ROOT / "policy_history.json"
MAX_OVERLAP = 0.25   # share of this script's 4-word phrases allowed to appear in any other Short
MAX_LAYOUT_RUN = 2   # Shorts in a row allowed on the same screen layout
CTA_DEVICES = {"subscribe_badge", "cursor_click", "comment_bubble", "bell"}
OPENING_WORDS = 4    # this many opening words may not match any of the last OPENING_LOOKBACK Shorts
OPENING_LOOKBACK = 5
MIN_BPM_STEP = 6     # music tempo must move at least this far from the previous Short
MIN_SOURCES = 2
STOCK_HOOKS = ("क्या आपको पता है", "क्या आप जानते हैं", "kya aapko pata hai", "kya aap jaante hain")

# Loading outside media is how reused content sneaks in; every frame and sound must be made here.
MEDIA_PATTERNS = [
    r"\.(mp4|mov|mkv|webm|avi|gif|png|jpe?g|webp|mp3|wav|m4a|aac|ogg|flac)\b",
    r"\b(VideoFileClip|ImageClip|ImageSequenceClip|AudioFileClip|create_from_png|cv2\.imread|Image\.open)\b",
    r"\b(yt_dlp|youtube_dl|pytube|urlopen|requests\.get|httpx\.get|wget)\b",
]
# Files the engine itself writes (TTS clips, the mix, the render) are not outside media.
GENERATED = re.compile(r'(scene_\{|_l\{|master_audio\.wav|\.mp3"\)|OUTPUTS\s*=|^Output:|"\.json"|mp3_44100)')
# YouTube has no DMs and Shorts links aren't clickable: promising links this way misleads the viewer.
OFF_PLATFORM = re.compile(r"(डीएम|\bDM\b|इनबॉक्स|\binbox\b|link in bio|लिंक इन बायो|\bbio\b|बायो)", re.IGNORECASE)
# Allowed only when literally true; YPP's misleading-metadata rule covers titles/text that oversell.
CLICKBAIT = re.compile(r"(ILLEGAL|इलीगल|गैरकानूनी|GUARANTEED|गारंटी|100% SURE|BANNED|बैन|SECRET|सीक्रेट|"
                       r"HACK|हैक|FREE MONEY)", re.IGNORECASE)
# Advertiser-friendly guidelines: graphic violence / gore and shocking words get limited or no ads.
GRAPHIC = re.compile(r"(खून|लाश|लाशें|कत्ल|क़त्ल|मार डाल|नरसंहार|धमाके में मारे|सिर काट|"
                     r"\bBLOOD\b|\bGORE\b|\bKILL(ED|ING)?\b|\bDEAD BODIES\b|\bMASSACRE\b|\bBEHEAD)", re.IGNORECASE)
# Hate / harassment: demeaning labels for a people, nation or religion are never allowed.
DEROGATORY = re.compile(r"(भिखारी|कुत्ते|कीड़े|सूअर|\bBEGGARS?\b|\bDOGS\b|\bCOCKROACH|\bPIGS\b|\bTERRORIST NATION\b)",
                        re.IGNORECASE)


def narration(story) -> list[str]:
    return [w for _, chunks in story.SCRIPT for spoken, _ in chunks for w in spoken.lower().split()]


def shingles(words: list[str], n: int = 4) -> set[tuple]:
    return {tuple(words[i:i + n]) for i in range(len(words) - n + 1)}


def other_shorts(name: str):
    mods = [f"stories.{p.stem}" for p in (ROOT / "stories").glob("*.py") if p.stem != "__init__"]
    mods += [p.stem for p in ROOT.glob("generate_*_short.py")]
    for mod in sorted(mods):
        if mod.split(".")[-1] == name:
            continue
        try:
            yield mod, importlib.import_module(mod)
        except Exception as e:   # a broken neighbour must not hide a duplicate silently
            print(f"      [policy] could not load {mod} for comparison: {e}")


def source_of(name: str) -> Path | None:
    for p in (ROOT / f"{name}.py", ROOT / "stories" / f"{name}.py"):
        if p.exists():
            return p
    return None


def module_of(name: str):
    p = source_of(name)
    if p is None:
        return None
    try:
        return importlib.import_module(name if p.parent == ROOT else f"stories.{name}")
    except Exception as e:
        print(f"      [policy] could not load {name} for comparison: {e}")
        return None


def bare(words: list[str]) -> list[str]:
    return [w.strip(".,!?।…'\"—-") for w in words if w.strip(".,!?।…'\"—-")]


def opening(story) -> list[str]:
    return bare(narration(story))[:OPENING_WORDS]


def closing(story) -> list[str]:
    if not getattr(story, "SCRIPT", None):
        return []
    return bare([w for spoken, _ in story.SCRIPT[-1][1] for w in spoken.lower().split()])[-6:]


def music_of(story) -> tuple[str, float]:
    return getattr(story, "MUSIC_STYLE", "tension"), getattr(story, "MUSIC_BPM", 100)


def series_problems(story, before: list[str]) -> tuple[list[str], list[str]]:
    """Hook, music, ending-line and structure repetition against the Shorts rendered before this one."""
    problems, warnings = [], []
    prev = [(n, m) for n in before if (m := module_of(n)) is not None]
    spoken = " ".join(narration(story))
    for hook in STOCK_HOOKS:
        if hook.lower() in spoken[:80]:
            problems.append(f'stock hook "{hook}" in the opening - open on the claim itself')
    mine = opening(story)
    for n, m in prev[-OPENING_LOOKBACK:]:
        if mine and mine == opening(m):
            problems.append(f'opens with the same {OPENING_WORDS} words as {n} ("{" ".join(mine)}")')
    if prev:
        style, bpm = music_of(story)
        n, m = prev[-1]
        p_style, p_bpm = music_of(m)
        if style == p_style:
            problems.append(f'MUSIC_STYLE "{style}" is the same as {n} - rotate (styles: tension, pulse, ambient, march)')
        if abs(bpm - p_bpm) < MIN_BPM_STEP:
            problems.append(f"MUSIC_BPM {bpm} is within {MIN_BPM_STEP} of {n} ({p_bpm}) - move the tempo")
        used = [music_of(m)[0] for _, m in prev[-3:]]
        if used.count(style) >= 2:
            problems.append(f'MUSIC_STYLE "{style}" already used in 2 of the last 3 Shorts')
        end = closing(story)
        if end and end == closing(m):
            warnings.append(f"closing line copies {n} word for word - vary the sign-off")
        counts = [len(getattr(m, "SCRIPT", [])) for _, m in prev[-3:]]
        if len(counts) == 3 and all(c == len(story.SCRIPT) for c in counts):
            warnings.append(f"{len(story.SCRIPT)} scenes again, like the last 3 Shorts - change the structure")
    return problems, warnings


def kit_problems(story) -> list[str]:
    """Facts and packaging a new Short must carry before it may render."""
    problems = []
    if len(getattr(story, "SOURCES", ())) < MIN_SOURCES:
        problems.append(f"SOURCES lists fewer than {MIN_SOURCES} references for the facts - add where each "
                        f"number/claim comes from (misinformation policy)")
    if not hasattr(story, "UPLOAD") or not hasattr(story, "thumbnail"):
        problems.append("no UPLOAD kit / thumbnail(ctx) - every Short ships with scored metadata (see upload_kit.py)")
    return problems


def template(path: Path) -> tuple[str, frozenset]:
    """(screen layout, ending devices) of a Short, read from the calls in its source."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    alias, origin, local = {}, {}, set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                alias[a.asname or a.name] = a.name
        elif isinstance(n, ast.ImportFrom) and n.module:
            for a in n.names:
                origin[a.asname or a.name] = n.module
        elif isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            local.add(n.name)
    calls = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id in alias:
                calls.add((alias[f.value.id], f.attr))
            elif isinstance(f, ast.Name):
                calls.add((path.stem if f.id in local else origin.get(f.id, "engine"), f.id))
    composers = sorted(o for o, fn in calls if fn == "compose")
    # a story's own compose() is its own layout; with none, engine.make_frame draws the kinetic captions
    layout = composers[0] if composers else (path.stem if "make_frame" in local else "engine")
    return layout, frozenset(fn for _, fn in calls if fn in CTA_DEVICES)


def load_history() -> dict:
    if HISTORY.exists():
        return json.loads(HISTORY.read_text(encoding="utf-8"))
    return {"order": [], "grandfathered": []}


def template_problems(name: str, path: Path, history: dict) -> list[str]:
    order = history["order"]
    before = order[:order.index(name)] if name in order else order
    prev = [(n, template(p)) for n in before if (p := source_of(n))]
    layout, ending = template(path)
    problems = []
    run = [n for n, (lay, _) in prev[-MAX_LAYOUT_RUN:] if lay == layout]
    if len(run) == MAX_LAYOUT_RUN:
        problems.append(f'same screen layout ("{layout}") as the last {MAX_LAYOUT_RUN} Shorts ({", ".join(run)}) - '
                        f"build a new layout (badge position, header, transitions, caption style)")
    for n, (_, end) in prev[-2:]:
        if ending and ending == end:
            problems.append(f"same ending as {n} ({', '.join(sorted(ending))}) - change the closing scene/CTA")
    return problems


def metadata_text(story) -> str:
    up = getattr(story, "UPLOAD", {})
    return " ".join([*up.get("titles", []), up.get("thumb_text", ""), up.get("description", ""), *up.get("tags", [])])


def check(story, name: str) -> None:
    if hasattr(sys.stdout, "reconfigure"):   # Devanagari in a message must not crash a cp1252 console
        sys.stdout.reconfigure(errors="backslashreplace")
    problems, warnings = [], []
    path = Path(story.__file__)
    src = path.read_text(encoding="utf-8")
    for ln, line in enumerate(src.splitlines(), 1):
        if GENERATED.search(line):
            continue
        for pat in MEDIA_PATTERNS:
            if re.search(pat, line):
                problems.append(f"outside media at {path.name}:{ln}: {line.strip()[:90]}")
                break

    mine = shingles(narration(story))
    topic = story.TOPIC.strip().upper()
    for mod, other in other_shorts(name):
        if getattr(other, "TOPIC", "").strip().upper() == topic:
            problems.append(f'TOPIC "{story.TOPIC}" is already used by {mod}')
        if mine and hasattr(other, "SCRIPT"):
            overlap = len(mine & shingles(narration(other))) / len(mine)
            if overlap > MAX_OVERLAP:
                problems.append(f"{overlap:.0%} of the narration repeats {mod} (limit {MAX_OVERLAP:.0%})")

    spoken = " ".join(narration(story))
    shown = [story.TOPIC] + [s.get("text", "") for s in getattr(story, "SPEC", [])]
    if m := OFF_PLATFORM.search(spoken + " " + " ".join(shown)):
        problems.append(f'off-platform call to action "{m.group(0)}" - YouTube has no DMs/bio links; '
                        f"ask for a comment or subscribe instead")
    everything = spoken + " " + " ".join(shown) + " " + metadata_text(story)
    for s in sorted({m.group(0) for m in CLICKBAIT.finditer(everything)}):
        warnings.append(f'"{s}" in narration/on-screen text/metadata - keep only if literally true, or YPP may treat '
                        f"it as misleading")
    for s in sorted({m.group(0) for m in GRAPHIC.finditer(everything)}):
        warnings.append(f'"{s}" is graphic/violent wording - advertisers may limit ads; describe it factually instead')

    history = load_history()
    if name not in history["grandfathered"]:
        for s in sorted({m.group(0) for m in DEROGATORY.finditer(everything)}):
            problems.append(f'"{s}" demeans a people/nation/religion - hate & harassment policy; remove it')
        order = history["order"]
        before = order[:order.index(name)] if name in order else order
        problems += template_problems(name, path, history)
        more, warn = series_problems(story, before)
        problems += more + kit_problems(story)
        warnings += warn

    if problems:
        raise SystemExit("[policy] Render blocked - YPP reused/inauthentic/misleading content risk:\n  - "
                         + "\n  - ".join(problems)
                         + "\nFix the story (fresh script/topic, new layout or ending, drawn visuals), then render again.")
    for w in warnings:
        print(f"[policy] WARNING: {w}")
    if name not in history["order"]:
        history["order"].append(name)
        HISTORY.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")
    layout, ending = template(path)
    style, bpm = music_of(story)
    print(f"[policy] OK - original narration, unique topic, no outside media ({len(mine)} phrases checked); "
          f"layout {layout}, ending {', '.join(sorted(ending)) or 'none'}, music {style} @ {bpm} BPM")
    print("[policy] On upload: original title/description/thumbnail; tick 'altered or synthetic' only if a\n"
          "         real person is shown realistically saying/doing something they didn't (cartoons don't need it).")


if __name__ == "__main__":   # dry run: python policy.py <story name>, checks without rendering
    target = sys.argv[1].removesuffix(".py")
    check(module_of(target), target)
