"""Frame compositor + FFmpeg encoder.

Per frame: camera frame of the scene's graded artwork -> Cairo atmosphere layers -> (crossfade with the
neighbouring scene near a cut) -> vignette, labels, title card, captions, branding -> film grain.
Frames are streamed as raw BGRA into FFmpeg (no PNG sequence on disk, which keeps OneDrive quiet).
Rendering is split across worker processes into segments that are concatenated without re-encoding.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
from pathlib import Path

import cairo
import numpy as np

from audio.mix import resolve_cue
from compositor import captions as C
from config import settings as S
from generators.commons import load_manifest
from visuals import camera, effects

XFADE = 0.5      # cut transition length (s)


# ---------------------------------------------------------------- scene setup

def _asset_path(title: str) -> Path:
    m = load_manifest()
    if title not in m:
        raise FileNotFoundError(f"asset not downloaded / not licence-approved: {title}")
    return S.ROOT / m[title]["local"]


@lru_cache(maxsize=32)
def _source(title: str, bounds: tuple, grade: str, max_zoom: float):
    return camera.prepare(_asset_path(title), bounds, grade, max_zoom)


class Scene:
    def __init__(self, sc: dict, tl: dict, idx: int):
        v = sc["visual"]
        self.sc, self.tl, self.idx = sc, tl, idx
        self.start, self.dur = tl["start"], tl["dur"]
        zoom = tuple(v.get("zoom", (1.0, 1.12)))
        src = _source(v["asset"], tuple(v.get("bounds", (0, 0, 1, 1))), v.get("grade", "cinematic"), max(zoom))
        self.shot = camera.Shot(src, tuple(v.get("focus", (0.5, 0.5))), tuple(v.get("pan", (0, 0))), zoom,
                                self.dur)
        fx = v.get("fx", {})
        cues = {}
        for name, params in fx.items():
            for key in ("from", "at"):
                if key in params:
                    cues[f"{name}.{key}"] = resolve_cue(params[key], tl) - self.start
        self.env = effects.Env(self.shot, fx, cues, seed=1000 + idx * 17, grade=v.get("grade", "cinematic"))
        self.effects = v.get("effects", [])
        self.highlight = set(sc.get("highlight", []))
        self.chunks = C.chunk(C.align_tokens(sc["narration"], tl["words"]), tl["start"] + tl["dur"])
        self.title = sc.get("title", "")
        self.title_t = (resolve_cue(sc["title_at"], tl) if sc.get("title_at") else self.start + 0.1) - self.start
        self.popular = any(c["kind"] == "popular_interpretation" for c in sc.get("claims", []))

    def layer(self, t_local: float) -> np.ndarray:
        """Artwork + atmosphere as a BGRA array."""
        im = self.shot.frame(t_local)
        rgb = np.asarray(im)
        bgra = np.empty((S.H, S.W, 4), np.uint8)
        bgra[:, :, 0] = rgb[:, :, 2]
        bgra[:, :, 1] = rgb[:, :, 1]
        bgra[:, :, 2] = rgb[:, :, 0]
        bgra[:, :, 3] = 255
        surf = cairo.ImageSurface.create_for_data(memoryview(bgra), cairo.FORMAT_ARGB32, S.W, S.H, S.W * 4)
        ctx = cairo.Context(surf)
        effects.draw_all(ctx, self.effects, t_local, self.dur, self.env)
        surf.flush()
        return bgra


def load_scenes(story: dict, timeline: list[dict]) -> list[Scene]:
    return [Scene(sc, tl, i) for i, (sc, tl) in enumerate(zip(story["scenes"], timeline))]


# ---------------------------------------------------------------- frame

def compose(scenes: list[Scene], t: float, frame_idx: int) -> np.ndarray:
    i = max(k for k, s in enumerate(scenes) if t >= s.start or k == 0)
    s = scenes[i]
    lt = t - s.start
    base = s.layer(lt)
    flash = 0.0
    # crossfade around cuts: the second half of the fade belongs to the incoming scene
    if i > 0 and lt < XFADE / 2:
        prev = scenes[i - 1]
        mix = 0.5 + lt / XFADE
        other = prev.layer(t - prev.start)
        base = (base.astype(np.float32) * mix + other.astype(np.float32) * (1 - mix)).astype(np.uint8)
        flash = 1 - lt / (XFADE / 2)
    elif i + 1 < len(scenes) and s.dur - lt < XFADE / 2:
        nxt = scenes[i + 1]
        mix = 0.5 - (s.dur - lt) / XFADE
        other = nxt.layer(t - nxt.start)
        base = (base.astype(np.float32) * (1 - mix) + other.astype(np.float32) * mix).astype(np.uint8)
        flash = 1 - (s.dur - lt) / (XFADE / 2)
    base = np.ascontiguousarray(base)
    surf = cairo.ImageSurface.create_for_data(memoryview(base), cairo.FORMAT_ARGB32, S.W, S.H, S.W * 4)
    ctx = cairo.Context(surf)
    if flash > 0:   # warm light-leak at the cut
        ctx.save()
        ctx.set_operator(cairo.OPERATOR_ADD)
        g = cairo.LinearGradient(0, 0, S.W, S.H)
        g.add_color_stop_rgba(0, 1.0, 0.7, 0.35, 0.22 * flash)
        g.add_color_stop_rgba(1, 1.0, 0.85, 0.6, 0.05 * flash)
        ctx.set_source(g)
        ctx.paint()
        ctx.restore()
    effects.vignette(ctx)
    # top/bottom gradients keep UI text readable and the bottom Shorts area calm
    g = cairo.LinearGradient(0, 0, 0, 330)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.55)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g)
    ctx.rectangle(0, 0, S.W, 330)
    ctx.fill()
    g = cairo.LinearGradient(0, S.H - S.SAFE_BOTTOM - 260, 0, S.H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.6)
    ctx.set_source(g)
    ctx.rectangle(0, S.H - S.SAFE_BOTTOM - 260, S.W, S.SAFE_BOTTOM + 260)
    ctx.fill()
    C.draw_branding(ctx, t)
    C.draw_label(ctx, s.sc.get("label", ""), lt, s.popular)
    if s.title:
        C.draw_title(ctx, s.title, lt - s.title_t, s.sc.get("title_y", 700))
    C.draw_caption(ctx, s.chunks, t, s.highlight)
    surf.flush()
    effects.grain(base, frame_idx)
    return base


# ---------------------------------------------------------------- encode

def _segment(args) -> str:
    story_path, tl_path, f0, f1, out = args
    story = json.loads(Path(story_path).read_text(encoding="utf-8"))
    timeline = json.loads(Path(tl_path).read_text(encoding="utf-8"))
    scenes = load_scenes(story, timeline)
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{S.W}x{S.H}",
           "-r", str(S.FPS), "-i", "-", "-c:v", "libx264", "-preset", S.X264_PRESET, "-crf", str(S.CRF),
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-g", str(S.FPS * 2), out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(f0, f1):
        proc.stdin.write(compose(scenes, f / S.FPS, f).tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"ffmpeg failed on segment {out}")
    return out


def render(story_path: Path, timeline: list[dict], audio_wav: Path, out_mp4: Path, workers: int | None = None) -> Path:
    tmp = S.story_temp(json.loads(Path(story_path).read_text(encoding="utf-8"))["slug"])
    tl_path = tmp / "timeline.json"
    tl_path.write_text(json.dumps(timeline, ensure_ascii=False, indent=1), encoding="utf-8")
    total = timeline[-1]["start"] + timeline[-1]["dur"]
    n = int(math.ceil(total * S.FPS))
    workers = workers or max(1, min(6, (os.cpu_count() or 2) - 1))
    bounds = [round(n * k / workers) for k in range(workers + 1)]
    jobs = [(str(story_path), str(tl_path), bounds[k], bounds[k + 1], str(tmp / f"seg_{k:02d}.mp4"))
            for k in range(workers)]
    with ProcessPoolExecutor(workers) as ex:
        segs = list(ex.map(_segment, jobs))
    lst = tmp / "segments.txt"
    lst.write_text("".join(f"file '{Path(p).name}'\n" for p in segs), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(audio_wav),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-shortest", "-movflags", "+faststart", str(out_mp4)], check=True)
    for p in segs:
        Path(p).unlink(missing_ok=True)
    return out_mp4


def stills(story: dict, timeline: list[dict], times: list[float], out_png: Path, cols: int = 4) -> Path:
    """Contact sheet of composed frames at the given times (fast visual review without a full render)."""
    from PIL import Image

    scenes = load_scenes(story, timeline)
    tw, th = S.W // 3, S.H // 3
    rows = math.ceil(len(times) / cols)
    sheet = Image.new("RGB", (cols * tw, rows * th), (0, 0, 0))
    for k, t in enumerate(times):
        bgra = compose(scenes, t, int(t * S.FPS))
        im = Image.fromarray(bgra[:, :, [2, 1, 0]]).resize((tw, th), Image.LANCZOS)
        sheet.paste(im, ((k % cols) * tw, (k // cols) * th))
    sheet.save(out_png)
    return out_png
