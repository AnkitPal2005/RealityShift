"""Render 5 moments of EVERY scene (preview timing: 6 s per scene) as one grid, to see the poses/actions the
2-tile preview sheet hides.

Usage (from story-pipeline/SanatanKatha):
    python ../../.agents/skills/divya-short-studio/scripts/probe_moments.py <katha_name> <out.png>
Rows = scenes, columns = t 0.6 / 1.8 / 3.0 / 4.2 / 5.4 s.
"""
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
import cairo  # noqa: E402
from core import engine, katha  # noqa: E402

name, out = sys.argv[1], sys.argv[2]
story = importlib.import_module("kathas." + name)
dur = 6.0
engine.SCENES.clear()
t0 = 0.0
for key, chunks in story.SCRIPT:
    caps = [(dur * 0.9 * i / len(chunks), cap) for i, (_, cap) in enumerate(chunks)]
    engine.SCENES.append({"key": key, "obj": story.SCENE_CLASSES[key](), "start": t0, "dur": dur, "captions": caps})
    t0 += dur
times = (0.6, 1.8, 3.0, 4.2, 5.4)
sw, sh = 216, 384
sheet = cairo.ImageSurface(cairo.FORMAT_ARGB32, len(times) * sw, len(engine.SCENES) * sh)
ctx = cairo.Context(sheet)
for r in range(len(engine.SCENES)):
    for c, tl in enumerate(times):
        ctx.save()
        ctx.translate(c * sw, r * sh)
        ctx.scale(sw / engine.W, sh / engine.H)
        ctx.set_source_surface(katha.compose(story, r, tl))
        ctx.paint()
        ctx.restore()
sheet.write_to_png(out)
print(out)
