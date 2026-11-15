"""Reality Shift pipeline - one command per Short.

Usage (run from this folder):
  python make.py nyoma                  # full render: YPP gate -> voice -> music -> frames -> upload kit
  python make.py nyoma --check          # only the YPP policy gate (no voice spent, nothing rendered)
  python make.py nyoma --preview        # contact sheet of all scenes + thumbnail (fast, no voice)
  python make.py nyoma --kit            # rebuild the upload kit + thumbnail for an already rendered Short
  python make.py nyoma --kiki-export    # KikiVoice: one text file per voice
  python make.py nyoma --kiki-split     # cut the downloaded KikiVoice files into lines (+ --check-voice)
  python make.py nyoma --engine edge    # force the edge-tts voice (preview without KikiVoice clips)
  python make.py --list                 # every Short in shorts/ and whether it has been rendered

A new Short = a new shorts/<name>.py (copy the latest Lego Short, e.g. shorts/nyoma.py) - see README.md.
"""

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
if hasattr(sys.stdout, "reconfigure"):   # Devanagari in messages must not crash a cp1252 console
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")


def shorts():
    return sorted(p.stem for p in (ROOT / "shorts").glob("*.py") if p.stem != "__init__")


def render(name, args):
    from core import engine
    story = importlib.import_module(f"shorts.{name}")
    if hasattr(story, "main"):          # every generate-style Short wires its own frame maker + upload kit
        story.main()
    else:                               # the early stories: engine draws their SCENE_CLASSES directly
        engine.render(story, args[args.index("--engine") + 1] if "--engine" in args else "edge")


def preview(name):
    """Render stills with fake timings so visuals and thumbnail can be checked fast without audio."""
    import cairo
    from core import engine, lego
    story = importlib.import_module(f"shorts.{name}")
    out = engine.OUT_DIR / "preview"
    out.mkdir(parents=True, exist_ok=True)
    dur = 6.0
    engine.SCENES.clear()
    t0 = 0.0
    if hasattr(story, "SPEC") and hasattr(story, "SCENE_CLASSES"):
        for spec in story.SPEC:
            key = spec["key"]
            cls = story.SCENE_CLASSES.get(key)
            if cls:
                engine.SCENES.append({"key": key, "obj": cls(), "start": t0, "dur": dur, "captions": []})
                t0 += dur
        n = len(engine.SCENES)
        sw, sh = 270, 480
        sheet = cairo.ImageSurface(cairo.FORMAT_ARGB32, n * sw, 2 * sh)
        ctx = cairo.Context(sheet)
        for i in range(n):
            for r, tl in enumerate((dur * 0.35, dur * 0.95)):
                ctx.save()
                ctx.translate(i * sw, r * sh)
                ctx.scale(sw / engine.W, sh / engine.H)
                ctx.set_source_surface(lego.compose(story, i, tl))
                ctx.paint()
                ctx.restore()
        sheet_path = out / f"{name}_sheet.png"
        sheet.write_to_png(str(sheet_path))
        print(f"preview: {sheet_path}")
    if hasattr(story, "thumbnail"):
        thumb = cairo.ImageSurface(cairo.FORMAT_ARGB32, engine.W, engine.H)
        story.thumbnail(cairo.Context(thumb))
        thumb_path = out / f"{name}_thumb.png"
        thumb.write_to_png(str(thumb_path))
        print(f"         {thumb_path}")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    if args[0] == "--list":
        from core import engine
        for k in shorts():
            story = importlib.import_module(f"shorts.{k}")
            out = engine.shorts_dir(story) / next(iter(getattr(story, "OUTPUTS", {"": "-"}).values()))
            print(f"  {k:24s} {'rendered' if out.exists() else '-'}")
        return
    name = args[0].removesuffix(".py")
    if name not in shorts():
        raise SystemExit(f"no shorts/{name}.py - available: {', '.join(shorts())}")
    if "--check" in args:
        from core import policy
        policy.check(importlib.import_module(f"shorts.{name}"), name)
    elif "--preview" in args:
        preview(name)
    elif "--kit" in args:
        from core import upload_kit
        sys.argv = [sys.argv[0], name]
        upload_kit.main()
    elif "--kiki-export" in args:
        from core import voice_kit
        voice_kit.export(name)
    elif "--kiki-split" in args:
        from core import voice_kit
        voice_kit.split(name, check="--check-voice" in args)
    else:
        render(name, args)


if __name__ == "__main__":
    main()
