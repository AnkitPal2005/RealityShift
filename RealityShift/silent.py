"""Silent Reality renderer: no-voice 10-15s Shorts (ink sketch that draws itself + on-screen text + music).

Usage:
  python silent.py silent_reality_candle        # a story module in stories/

A silent story defines CHANNEL = "silent_reality", TOPIC, OUTPUTS = {"silent": "<name>.mp4"}, DURATION,
SCRIPT (the on-screen text as [(key, [(text, text), ...])] - the policy gate reads it like narration),
BEATS (per-key (start, end, visual) for the scene log), STROKES (list of Stroke), draw(ctx, t),
MUSIC_STYLE / MUSIC_BPM, SOURCES, UPLOAD and thumbnail(ctx).
Same YPP gate as Reality Shift (policy.check), everything drawn and synthesized here, then the upload kit.
"""

import hashlib
import importlib
import json
import math
import sys

import cairo
import numpy as np
from moviepy import AudioFileClip, VideoClip

import engine
from engine import FPS, SR, H, W, _lowpass, _noise, ffilter, rgba, rnd, write_wav

INK = (0.13, 0.10, 0.08)
PAPER = (0.93, 0.89, 0.80)
MUSIC_GAIN = 0.75
SCRATCH_GAIN = 0.22


# ============================================================ ink strokes

class Stroke:
    """A hand-drawn line that is inked from its first point to its last between t0 and t1."""

    def __init__(self, pts, t0, t1, width=5.0, color=INK, seed=0, wobble=2.2, alpha=0.92):
        self.pts = jitter(pts, seed, wobble)
        self.t0, self.t1, self.width, self.color, self.alpha = t0, t1, width, color, alpha
        seg = np.hypot(*np.diff(np.array(self.pts), axis=0).T)
        self.cum = np.concatenate([[0.0], np.cumsum(seg)])

    def progress(self, t):
        return engine.clamp((t - self.t0) / max(1e-6, self.t1 - self.t0))

    def draw(self, ctx, t, fade=1.0, nib=True):
        u = self.progress(t)
        if u <= 0 or fade <= 0:
            return
        upto = u * self.cum[-1]
        k = int(np.searchsorted(self.cum, upto))
        pts = self.pts[:max(1, k)]
        if k < len(self.pts):
            a, b = self.pts[k - 1], self.pts[k]
            s = (upto - self.cum[k - 1]) / max(1e-6, self.cum[k] - self.cum[k - 1])
            pts = pts + [(a[0] + (b[0] - a[0]) * s, a[1] + (b[1] - a[1]) * s)]
        if len(pts) < 2:
            return
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        for off, w, al in ((0.0, self.width, self.alpha), (1.6, self.width * 0.45, self.alpha * 0.35)):
            ctx.move_to(pts[0][0] + off, pts[0][1] + off * 0.6)
            for x, y in pts[1:]:
                ctx.line_to(x + off, y + off * 0.6)
            rgba(ctx, self.color, al * fade)
            ctx.set_line_width(w)
            ctx.stroke()
        if nib and u < 1:   # the wet pen tip
            x, y = pts[-1]
            engine.circle(ctx, x, y, self.width * 0.9, self.color, 0.85 * fade)


def jitter(pts, seed, amt):
    """Small smooth wobble so lines look drawn by hand, not plotted."""
    out = []
    for i, (x, y) in enumerate(pts):
        f = i * 0.35
        out.append((x + amt * (math.sin(f + seed * 1.7) + 0.5 * math.sin(2.3 * f + seed)),
                    y + amt * (math.cos(1.3 * f + seed * 0.9) + 0.5 * math.sin(1.9 * f - seed))))
    return out


def bezier(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n + 1):
        u = i / n
        a, b, c, d = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def arc(cx, cy, rx, ry, a0, a1, n=48):
    return [(cx + rx * math.cos(a0 + (a1 - a0) * i / n), cy + ry * math.sin(a0 + (a1 - a0) * i / n))
            for i in range(n + 1)]


def activity(strokes, t):
    """How much pen is moving at time t (0..1) - drives the scratch sound."""
    return min(1.0, sum(1 for s in strokes if s.t0 <= t < s.t1) / 2.0)


def paper(ctx, t=0.0):
    """Aged parchment: warm gradient, fibre speckle and darker edges (all procedural)."""
    g = cairo.RadialGradient(W / 2, H * 0.45, 200, W / 2, H / 2, H * 0.8)
    g.add_color_stop_rgb(0, 0.95, 0.91, 0.82)
    g.add_color_stop_rgb(1, 0.80, 0.72, 0.58)
    ctx.set_source(g)
    ctx.paint()
    for i in range(900):
        x, y = rnd(i, 11) * W, rnd(i, 12) * H
        engine.circle(ctx, x, y, 0.6 + 1.8 * rnd(i, 13), (0.45, 0.35, 0.22), 0.05 + 0.07 * rnd(i, 14))
    for i in range(40):   # long paper fibres
        x, y, a = rnd(i, 21) * W, rnd(i, 22) * H, rnd(i, 23) * math.pi
        L = 20 + 50 * rnd(i, 24)
        engine.line(ctx, [(x, y), (x + L * math.cos(a), y + L * math.sin(a))], (0.5, 0.4, 0.28), 1.0, 0.08)


# ============================================================ sound

def scratch_track(strokes, dur, seed):
    """Nib-on-paper scratch: band-passed noise gated by how many strokes are being drawn."""
    n = int(dur * SR)
    noise = _noise(n, seed)
    hiss = noise - _lowpass(noise, 1800)
    hiss = _lowpass(hiss, 6500)
    t = np.arange(n) / SR
    act = np.array([activity(strokes, x) for x in np.arange(0, dur, 1 / 200)])
    gate = np.interp(t, np.arange(len(act)) / 200, act)
    flutter = 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 7.3 * t + 2 * np.sin(2 * np.pi * 0.9 * t)))
    out = hiss * gate * flutter
    return out / (np.max(np.abs(out)) + 1e-9)


# ============================================================ render

def load(name):
    name = name.removesuffix(".py")
    try:
        return importlib.import_module(f"stories.{name}")
    except ModuleNotFoundError:
        return importlib.import_module(name)


def render(story):
    import policy
    import upload_kit
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
    name = story.__name__.split(".")[-1]
    if getattr(story, "CHANNEL", "") != "silent_reality":
        raise SystemExit(f'{name}: silent.py renders CHANNEL = "silent_reality" stories only')
    policy.check(story, name)
    dur = story.DURATION
    work = engine.WORK_DIR / name / "silent"
    final = engine.shorts_dir(story) / story.OUTPUTS["silent"]
    work.mkdir(parents=True, exist_ok=True)
    final.parent.mkdir(parents=True, exist_ok=True)

    print("[1/3] Synthesizing music + pen scratch...")
    seed = getattr(story, "MUSIC_SEED", int(hashlib.md5(name.encode()).hexdigest()[:8], 16))
    music = engine.MUSIC_STYLES[story.MUSIC_STYLE](dur + 0.5, bpm=story.MUSIC_BPM, seed=seed)[:int(dur * SR)]
    music = np.pad(music, (0, int(dur * SR) - len(music)))
    mix = MUSIC_GAIN * music + SCRATCH_GAIN * scratch_track(story.STROKES, dur, seed % 1000)
    bank = engine.sfx_bank()
    for at, sfx, gain in getattr(story, "SFX", []):
        clip = bank[sfx] * gain
        i0 = int(at * SR)
        end = min(len(mix), i0 + len(clip))
        mix[i0:end] += clip[:end - i0]
    mix = ffilter(mix, "acompressor=threshold=0.3:ratio=2.5:attack=5:release=120,loudnorm=I=-14:TP=-1.5:LRA=9")
    master = work / "master_audio.wav"
    write_wav(master, np.clip(mix, -0.99, 0.99))

    def frame(t):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        story.draw(cairo.Context(surf), t)
        surf.flush()
        buf = np.ndarray((H, W, 4), dtype=np.uint8, buffer=surf.get_data())
        return buf[:, :, 2::-1].copy()

    print(f"[2/3] Rendering {int(dur * FPS)} frames...")
    VideoClip(frame, duration=dur).with_audio(AudioFileClip(str(master))).write_videofile(
        str(final), fps=FPS, codec="libx264", audio_codec="aac", audio_bitrate="192k", preset="medium",
        threads=8, ffmpeg_params=["-pix_fmt", "yuv420p", "-crf", "18"], temp_audiofile_path=str(work), logger="bar")

    scenes = [{"scene": key, "start": story.BEATS[key][0], "end": story.BEATS[key][1], "voiceover": "",
               "on_screen_text": " ".join(c for _, c in chunks), "visual": story.BEATS[key][2]}
              for key, chunks in story.SCRIPT]
    scenes[-1]["end"] = dur
    final.with_suffix(".json").write_text(json.dumps(scenes, indent=2, ensure_ascii=False), encoding="utf-8")
    print("[3/3] Upload kit...")
    upload_kit.build(story, final, dur)
    print(f"Done: {final}  ({dur:.1f}s)")
    return final


if __name__ == "__main__":
    render(load(sys.argv[1]))
