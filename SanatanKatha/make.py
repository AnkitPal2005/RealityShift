"""Sanatan Katha pipeline - one command per katha.

Usage (run from this folder):
  python make.py barbarik            # full render: YPP gate -> voice -> music -> frames -> scene log -> upload kit
  python make.py barbarik --check    # only the YPP policy gate (no voice spent, nothing rendered)
  python make.py barbarik --preview  # contact sheet of every scene (2 moments each) + thumbnail, no voice needed
  python make.py --list              # every katha in kathas/ and whether it has been rendered
  python make.py barbarik --kiki-export   # KikiVoice: one text file per voice (narrator, devta, maa, char)
  python make.py barbarik --kiki-split    # cut the downloaded KikiVoice files into lines (+ --check-voice)
  python make.py barbarik --engine edge   # force the old edge-tts voice (default: KikiVoice clips if split)

A new katha = copy kathas/_template.py to kathas/<name>.py and write the story (see README.md).
"""

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
if hasattr(sys.stdout, "reconfigure"):   # Devanagari in messages must not crash a cp1252 console
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")


def kathas():
    return sorted(p.stem for p in (ROOT / "kathas").glob("*.py") if not p.stem.startswith("_"))


def preview(name):
    """Render stills with fake timings (each scene 6 s, captions spread evenly) so visuals can be checked fast."""
    import cairo

    from core import engine
    from core import katha
    story = importlib.import_module(f"kathas.{name}")
    out = engine.OUT_DIR / "preview"
    out.mkdir(parents=True, exist_ok=True)
    dur = 6.0
    engine.SCENES.clear()
    t0 = 0.0
    for key, chunks in story.SCRIPT:
        caps = [(dur * 0.9 * i / len(chunks), cap) for i, (_, cap) in enumerate(chunks)]
        engine.SCENES.append({"key": key, "obj": story.SCENE_CLASSES[key](), "start": t0, "dur": dur,
                              "captions": caps})
        t0 += dur
    n = len(engine.SCENES)
    sw, sh = 270, 480
    sheet = cairo.ImageSurface(cairo.FORMAT_ARGB32, n * sw, 2 * sh)
    ctx = cairo.Context(sheet)
    for i in range(n):
        for r, tl in enumerate((dur * 0.35, dur * 0.97)):
            ctx.save()
            ctx.translate(i * sw, r * sh)
            ctx.scale(sw / engine.W, sh / engine.H)
            ctx.set_source_surface(katha.compose(story, i, tl))
            ctx.paint()
            ctx.restore()
    sheet.write_to_png(str(out / f"{name}_sheet.png"))
    thumb = cairo.ImageSurface(cairo.FORMAT_ARGB32, engine.W, engine.H)
    story.thumbnail(cairo.Context(thumb))
    thumb.write_to_png(str(out / f"{name}_thumb.png"))
    print(f"preview: {out / (name + '_sheet.png')}\n         {out / (name + '_thumb.png')}")


def run_qc(name):
    """Render each scene at 1080x1920 and run vision-model Visual QC + report."""
    from core import engine, katha
    sys.path.insert(0, str(ROOT.parent))
    import visual_qc

    story = importlib.import_module(f"kathas.{name}")
    qc_dir = engine.OUT_DIR / "work" / name / "qc"
    qc_dir.mkdir(parents=True, exist_ok=True)
    dur = 6.0
    engine.SCENES.clear()
    t0 = 0.0
    spec_map = {s["key"]: s for s in getattr(story, "SPEC", [])}
    items = []
    for idx, (key, chunks) in enumerate(story.SCRIPT):
        caps = [(dur * 0.9 * i / len(chunks), cap) for i, (_, cap) in enumerate(chunks)]
        engine.SCENES.append({"key": key, "obj": story.SCENE_CLASSES[key](), "start": t0, "dur": dur,
                              "captions": caps})
        surf = katha.compose(story, idx, dur * 0.65)
        img_path = qc_dir / f"scene_{idx + 1:02d}_{key}.png"
        surf.write_to_png(str(img_path))
        spec = spec_map.get(key, {})
        items.append({
            "scene_id": f"scene_{idx + 1:02d}_{key}",
            "image_path": img_path,
            "narration": " ".join(hi for hi, _ in chunks),
            "visual_brief": spec.get("visual", ""),
        })
        t0 += dur
    reports = visual_qc.validate_scene_sequence(items, debug_dir=qc_dir, is_cartoon=True)
    for rep in reports:
        print(f"[visual_qc] {rep['scene_id']}: {rep['status']} ({rep['score']}/100)")
    print(f"[visual_qc] report -> {qc_dir / 'qc_report.json'}")


def run_audit(name):
    """Run full-video audience, audio, pacing, and policy audit on the rendered Short."""
    from core import engine
    sys.path.insert(0, str(ROOT.parent))
    import shorts_auditor

    story = importlib.import_module(f"kathas.{name}")
    mp4 = engine.SHORTS_DIR / f"{name}_short.mp4"
    rep = shorts_auditor.audit_short(mp4, story_module=story)
    print(f"[audit] {mp4.name}: {rep['video_status']} ({rep['overall_score']}/100) - {rep['final_recommendation']}")
    for seg in rep["weak_segments"]:
        print(f"  - {seg['start']}-{seg['end']}: {seg['problem']} -> {seg['suggestion']}")
    print(f"[audit] report -> {mp4.with_name(mp4.stem + '_audit.json')}")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    if args[0] == "--list":
        from core import engine
        for k in kathas():
            story_out = engine.SHORTS_DIR / f"{k}_short.mp4"
            print(f"  {k:24s} {'rendered' if story_out.exists() else '-'}")
        return
    name = args[0].removesuffix(".py")
    if name not in kathas():
        raise SystemExit(f"no kathas/{name}.py - available: {', '.join(kathas()) or 'none'}")
    if "--check" in args:
        from core import policy
        policy.check(importlib.import_module(f"kathas.{name}"), name)
    elif "--preview" in args:
        preview(name)
    elif "--qc" in args:
        run_qc(name)
    elif "--audit" in args:
        run_audit(name)
    elif "--kiki-export" in args:
        from core import voice_kit
        voice_kit.export(name)
    elif "--kiki-split" in args:
        from core import voice_kit
        voice_kit.split(name, check="--check-voice" in args)
    else:
        if "--strict-qc" in args:
            run_qc(name)
        from core import katha
        katha.run(name, args[args.index("--engine") + 1] if "--engine" in args else None)


if __name__ == "__main__":
    main()
