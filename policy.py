"""YouTube Partner Program gate, run by engine.render() before any narration is generated.

Blocks a render that would risk YPP's "reused content" / "inauthentic (mass-produced, repetitive)
content" policies:
  - narration that repeats another Short's script (4-word shingle overlap above MAX_OVERLAP)
  - a TOPIC already used by another Short
  - third-party media pulled into the story (video/image/audio files, downloads, stock clips)
Everything else in the pipeline is original by construction: Cairo-drawn visuals, synthesized
music (seeded per story, see engine.tension_music) and synthesized SFX.
"""

import importlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAX_OVERLAP = 0.25   # share of this script's 4-word phrases allowed to appear in any other Short

# Loading outside media is how reused content sneaks in; every frame and sound must be made here.
MEDIA_PATTERNS = [
    r"\.(mp4|mov|mkv|webm|avi|gif|png|jpe?g|webp|mp3|wav|m4a|aac|ogg|flac)\b",
    r"\b(VideoFileClip|ImageClip|ImageSequenceClip|AudioFileClip|create_from_png|cv2\.imread|Image\.open)\b",
    r"\b(yt_dlp|youtube_dl|pytube|urlopen|requests\.get|httpx\.get|wget)\b",
]
# Files the engine itself writes (TTS clips, the mix, the render) are not outside media.
GENERATED = re.compile(r'(scene_\{|_l\{|master_audio\.wav|\.mp3"\)|OUTPUTS\s*=|^Output:|"\.json"|mp3_44100)')


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


def check(story, name: str) -> None:
    problems = []
    src = Path(story.__file__).read_text(encoding="utf-8")
    for ln, line in enumerate(src.splitlines(), 1):
        if GENERATED.search(line):
            continue
        for pat in MEDIA_PATTERNS:
            if re.search(pat, line):
                problems.append(f"outside media at {Path(story.__file__).name}:{ln}: {line.strip()[:90]}")
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

    if problems:
        raise SystemExit("[policy] Render blocked - YPP reused/inauthentic content risk:\n  - "
                         + "\n  - ".join(problems)
                         + "\nWrite a fresh script/topic or draw the visual in code, then render again.")
    print(f"[policy] OK - original narration, unique topic, no outside media ({len(mine)} phrases checked)")
    print("[policy] On upload: original title/description/thumbnail; tick 'altered or synthetic' only if a\n"
          "         real person is shown realistically saying/doing something they didn't (cartoons don't need it).")
