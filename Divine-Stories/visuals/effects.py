"""Procedural atmosphere drawn with Cairo over the camera frame.

All effects are deterministic (seeded per scene) so re-renders are identical.
Depth/parallax: fog, clouds and particles come in near/far layers that move at different speeds and sizes,
giving a 2.5D feel over a flat painting.

Each effect: fn(ctx, t, dur, env) where env carries the scene's camera Shot, resolved cue times and fx params.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from functools import lru_cache

import cairo
import numpy as np

from config import settings as S

W, H = S.W, S.H


# ---------------------------------------------------------------- shared

@dataclass
class Env:
    shot: object                 # visuals.camera.Shot
    fx: dict = field(default_factory=dict)
    cues: dict = field(default_factory=dict)   # name -> seconds (resolved "word:" cues etc.)
    seed: int = 0
    grade: str = "cinematic"


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def _hex(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def glow(ctx, x, y, r, color, a):
    if a <= 0 or r <= 0:
        return
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *color, a)
    g.add_color_stop_rgba(0.35, *color, a * 0.45)
    g.add_color_stop_rgba(1, *color, 0)
    ctx.set_source(g)
    ctx.arc(x, y, r, 0, math.tau)
    ctx.fill()


@lru_cache(maxsize=8)
def noise_texture(size: int = 1024, beta: float = 2.4, seed: int = 7, contrast: float = 1.6) -> cairo.ImageSurface:
    """Tileable fractal noise (1/f^beta spectrum) as an A8 surface - used for fog, clouds and smoke."""
    r = np.random.default_rng(seed)
    white = r.standard_normal((size, size))
    fy = np.fft.fftfreq(size)[:, None]
    fx = np.fft.fftfreq(size)[None, :]
    f = np.sqrt(fx * fx + fy * fy)
    f[0, 0] = 1
    spec = np.fft.fft2(white) / f ** (beta / 2)
    spec[0, 0] = 0
    n = np.real(np.fft.ifft2(spec))
    n = (n - n.mean()) / (n.std() + 1e-9)
    n = np.clip(0.5 + n * 0.22 * contrast, 0, 1) ** 1.6
    a8 = (n * 255).astype(np.uint8)
    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_A8, size)
    buf = np.zeros((size, stride), np.uint8)
    buf[:, :size] = a8
    surf = cairo.ImageSurface.create_for_data(memoryview(buf), cairo.FORMAT_A8, size, size, stride)
    _KEEP[(size, beta, seed, contrast)] = buf  # keep the numpy buffer alive as long as the surface
    return surf


_KEEP: dict = {}


def _noise_layer(ctx, t, color, alpha, scale, vx, vy, seed, y_from=0.0, y_to=1.0, fade="bottom"):
    """Scrolling tileable noise, tinted, with a vertical fade mask."""
    tex = noise_texture(seed=seed)
    ctx.push_group()
    ctx.save()
    ctx.scale(scale, scale)
    pat = cairo.SurfacePattern(tex)
    pat.set_extend(cairo.EXTEND_REPEAT)
    pat.set_filter(cairo.FILTER_BILINEAR)
    m = cairo.Matrix()
    m.translate(-vx * t / scale, -vy * t / scale)
    pat.set_matrix(m)
    ctx.set_source_rgba(*color, alpha)
    ctx.mask(pat)
    ctx.restore()
    layer = ctx.pop_group()
    g = cairo.LinearGradient(0, H * y_from, 0, H * y_to)
    if fade == "bottom":   # dense at the bottom
        g.add_color_stop_rgba(0, 0, 0, 0, 0)
        g.add_color_stop_rgba(1, 0, 0, 0, 1)
    elif fade == "top":
        g.add_color_stop_rgba(0, 0, 0, 0, 1)
        g.add_color_stop_rgba(1, 0, 0, 0, 0)
    else:
        g.add_color_stop_rgba(0, 0, 0, 0, 1)
        g.add_color_stop_rgba(1, 0, 0, 0, 1)
    ctx.set_source(layer)
    ctx.mask(g)


# ---------------------------------------------------------------- atmosphere

def fog(ctx, t, dur, env):
    _noise_layer(ctx, t, (0.85, 0.88, 0.95), 0.32, 2.4, 22, -4, 11, 0.45, 1.0)       # far, slow
    _noise_layer(ctx, t, (0.9, 0.92, 1.0), 0.22, 1.5, 55, -9, 12, 0.6, 1.0)          # near, faster (parallax)


def ocean_mist(ctx, t, dur, env):
    _noise_layer(ctx, t, (0.75, 0.85, 0.95), 0.35, 1.8, 70, 0, 21, 0.55, 1.0)
    _noise_layer(ctx, t, (0.95, 0.98, 1.0), 0.18, 1.1, 140, -6, 22, 0.7, 1.0)


def clouds(ctx, t, dur, env):
    dark = env.grade in ("night", "poison")
    c = (0.12, 0.13, 0.18) if dark else (0.95, 0.93, 0.9)
    _noise_layer(ctx, t, c, 0.45 if dark else 0.25, 3.0, 30, 0, 31, 0.0, 0.45, fade="top")
    _noise_layer(ctx, t, c, 0.30 if dark else 0.18, 1.8, 75, 0, 32, 0.0, 0.35, fade="top")


def target_mode(p: dict) -> bool:
    return bool(p.get("target"))


def poison_smoke(ctx, t, dur, env):
    p = env.fx.get("poison_smoke", {})
    start = env.cues.get("poison_smoke.from", 0.0)
    k = min(1.0, max(0.0, (t - start + 0.6) / 0.8)) if "from" in p else 1.0
    if k <= 0:
        return
    if not target_mode(p):   # full-scene poison: sink the light paper of old prints into a toxic dark
        ctx.save()
        ctx.set_operator(cairo.OPERATOR_MULTIPLY)
        ctx.set_source_rgba(0.35, 0.55, 0.45, 0.75 * k)
        ctx.paint()
        ctx.restore()
    _noise_layer(ctx, t, (0.25, 0.85, 0.55), 0.38 * k, 2.0, 18, 60, 41, 0.35, 1.0)
    _noise_layer(ctx, t, (0.1, 0.55, 0.45), 0.30 * k, 1.3, -35, 90, 42, 0.5, 1.0)
    target = p.get("target")
    r = rng(env.seed + 5)
    n = 70
    ox, oy = r.uniform(0, W, n), r.uniform(H * 0.55, H * 1.05, n)
    sp = r.uniform(0.25, 0.6, n)
    sz = r.uniform(6, 22, n)
    for i in range(n):
        if target:
            tx, ty = env.shot.to_screen(t, target)
            u = ((t - start) * sp[i] + i / n) % 1.0
            e = u * u
            x = ox[i] + (tx - ox[i]) * e + math.sin(u * 9 + i) * 40 * (1 - e)
            y = oy[i] + (ty - oy[i]) * e
            a = k * (1 - e) * 0.8
        else:
            u = (t * sp[i] * 0.25 + i / n) % 1.0
            x = ox[i] + math.sin(t * 0.8 + i) * 30
            y = oy[i] - u * H * 0.6
            a = k * math.sin(u * math.pi) * 0.7
        glow(ctx, x, y, sz[i] * 2.2, (0.35, 1.0, 0.6), a * 0.6)


def rays(ctx, t, dur, env):
    p = env.fx.get("rays", {})
    ox, oy = env.shot.to_screen(t, tuple(p.get("origin", (0.5, 0.0))))
    ox, oy = min(max(ox, -200), W + 200), min(max(oy, -400), H * 0.7)
    warm = (1.0, 0.86, 0.6) if env.grade not in ("night", "poison", "cold") else (0.7, 0.8, 1.0)
    r = rng(env.seed + 9)
    n = 11
    ctx.save()
    ctx.set_operator(cairo.OPERATOR_ADD)
    L = 2600
    for i in range(n):
        # angle measured from straight down; rays fan out below the origin
        ang = (i - (n - 1) / 2) * 0.17 + r.uniform(-0.05, 0.05) + 0.04 * math.sin(t * 0.35 + i)
        wdt = r.uniform(0.025, 0.07)
        a = (0.045 + 0.03 * math.sin(t * 0.9 + i * 1.7)) * (0.6 + 0.4 * r.random())
        g = cairo.RadialGradient(ox, oy, 0, ox, oy, L)
        g.add_color_stop_rgba(0, *warm, a)
        g.add_color_stop_rgba(0.6, *warm, a * 0.35)
        g.add_color_stop_rgba(1, *warm, 0)
        ctx.move_to(ox, oy)
        ctx.line_to(ox + L * math.sin(ang - wdt), oy + L * math.cos(ang - wdt))
        ctx.line_to(ox + L * math.sin(ang + wdt), oy + L * math.cos(ang + wdt))
        ctx.close_path()
        ctx.set_source(g)
        ctx.fill()
    ctx.restore()
    glow(ctx, ox, oy, 380, warm, 0.18)


def _particles(ctx, t, env, salt, n, color, size, speed, rise, wobble, alpha, layer_depths=(0.5, 1.0)):
    r = rng(env.seed + salt)
    xs, ys = r.uniform(0, W, n), r.uniform(0, H, n)
    depth = r.uniform(*layer_depths, n)
    ph = r.uniform(0, math.tau, n)
    for i in range(n):
        d = depth[i]
        y = (ys[i] - t * rise * speed * d) % (H + 100) - 50
        x = (xs[i] + math.sin(t * wobble + ph[i]) * 25 * d + t * 8 * d) % (W + 60) - 30
        flick = 0.6 + 0.4 * math.sin(t * 6 + ph[i] * 3)
        glow(ctx, x, y, size * d * 2.4, color, alpha * flick * d)
        ctx.set_source_rgba(*color, min(1, alpha * 1.4 * flick))
        ctx.arc(x, y, max(0.8, size * d * 0.35), 0, math.tau)
        ctx.fill()


def dust(ctx, t, dur, env):
    warm = (1.0, 0.93, 0.8) if env.grade not in ("night", "poison") else (0.8, 0.9, 1.0)
    _particles(ctx, t, env, 1, 55, warm, 7, 18, 1.0, 0.6, 0.35, (0.3, 1.0))


def embers(ctx, t, dur, env):
    _particles(ctx, t, env, 2, 45, (1.0, 0.55, 0.18), 9, 90, 1.0, 1.8, 0.65, (0.4, 1.0))


def sparks(ctx, t, dur, env):
    r = rng(env.seed + 3)
    n = 40
    cx, cy = W * 0.5, H * 0.72
    for i in range(n):
        life = (t * r.uniform(0.6, 1.2) + i / n) % 1.0
        ang = r.uniform(-math.pi * 0.95, -math.pi * 0.05)
        v = r.uniform(300, 900)
        x = cx + math.cos(ang) * v * life + r.uniform(-200, 200)
        y = cy + math.sin(ang) * v * life + 400 * life * life
        a = (1 - life) * 0.9
        ctx.set_source_rgba(0.6, 1.0, 0.7, a)
        ctx.set_line_width(3)
        ctx.move_to(x, y)
        ctx.line_to(x - math.cos(ang) * 30, y - math.sin(ang) * 30)
        ctx.stroke()


def _bolt(r, x0, y0, x1, y1, depth=0):
    pts = [(x0, y0), (x1, y1)]
    disp = math.hypot(x1 - x0, y1 - y0) * 0.22
    for _ in range(6):
        new = [pts[0]]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            mx, my = (ax + bx) / 2 + r.uniform(-disp, disp), (ay + by) / 2 + r.uniform(-disp, disp) * 0.3
            new += [(mx, my), (bx, by)]
        pts = new
        disp *= 0.55
    return pts


def lightning(ctx, t, dur, env):
    times = env.fx.get("lightning", {}).get("times", [dur * 0.3])
    for k, t0 in enumerate(times):
        u = t - t0
        if not 0 <= u < 0.45:
            continue
        flicker = 1.0 if u < 0.06 else (0.3 if u < 0.1 else (0.85 if u < 0.16 else max(0, 1 - (u - 0.16) / 0.3)))
        r = rng(env.seed * 31 + k)
        x0 = r.uniform(W * 0.2, W * 0.8)
        pts = _bolt(r, x0, -20, x0 + r.uniform(-300, 300), r.uniform(H * 0.45, H * 0.7))
        ctx.save()
        ctx.set_operator(cairo.OPERATOR_ADD)
        ctx.set_source_rgba(0.75, 0.85, 1.0, 0.18 * flicker)
        ctx.paint()
        for wdt, a in ((26, 0.12), (10, 0.35), (3.5, 1.0)):
            ctx.set_source_rgba(0.85, 0.92, 1.0, a * flicker)
            ctx.set_line_width(wdt)
            ctx.move_to(*pts[0])
            for p in pts[1:]:
                ctx.line_to(*p)
            ctx.stroke()
        for b in range(3):   # branches
            i = int(r.uniform(0.2, 0.7) * len(pts))
            bx, by = pts[i]
            br = _bolt(r, bx, by, bx + r.uniform(-260, 260), by + r.uniform(120, 380))
            ctx.set_source_rgba(0.8, 0.9, 1.0, 0.6 * flicker)
            ctx.set_line_width(2)
            ctx.move_to(*br[0])
            for p in br[1:]:
                ctx.line_to(*p)
            ctx.stroke()
        ctx.restore()


def energy_wave(ctx, t, dur, env):
    p = env.fx.get("energy_wave", {})
    t0 = env.cues.get("energy_wave.at", dur * 0.6)
    x, y = env.shot.to_screen(t, tuple(p.get("point", (0.5, 0.5))))
    for k in range(3):
        u = (t - t0 - k * 0.18) / 1.1
        if not 0 <= u <= 1:
            continue
        rad = 40 + 900 * (1 - (1 - u) ** 3)
        ctx.save()
        ctx.set_operator(cairo.OPERATOR_ADD)
        ctx.set_source_rgba(0.45, 0.75, 1.0, 0.55 * (1 - u))
        ctx.set_line_width(14 * (1 - u) + 2)
        ctx.arc(x, y, rad, 0, math.tau)
        ctx.stroke()
        ctx.restore()


def throat_glow(ctx, t, dur, env):
    p = env.fx.get("throat_glow", {})
    t0 = env.cues.get("throat_glow.from", 0.0)
    k = min(1.0, max(0.0, (t - t0) / 0.9))
    if k <= 0:
        return
    x, y = env.shot.to_screen(t, tuple(p.get("point", (0.5, 0.5))))
    # radius is a fraction of the artwork width, so the glow tracks the face size at any zoom
    r = p.get("radius", 0.06) * env.shot.src.size[0] * env.shot.scale(t)
    pulse = 0.85 + 0.15 * math.sin(t * 4)
    col = _hex(p.get("color", "#3FA9FF"))
    ctx.save()
    # 1) recolour the throat itself (hue/saturation only, keeps the painting's shading), wider than tall
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(1.25, 0.6)
    ctx.set_operator(cairo.OPERATOR_HSL_COLOR)
    g = cairo.RadialGradient(0, 0, 0, 0, 0, r)
    g.add_color_stop_rgba(0, *col, 0.62 * k)
    g.add_color_stop_rgba(0.55, *col, 0.4 * k)
    g.add_color_stop_rgba(1, *col, 0)
    ctx.set_source(g)
    ctx.arc(0, 0, r, 0, math.tau)
    ctx.fill()
    ctx.restore()
    # 2) restrained additive glow (no blown-out highlight)
    ctx.set_operator(cairo.OPERATOR_ADD)
    glow(ctx, x, y, r * 0.8 * pulse, col, 0.22 * k)
    glow(ctx, x, y, r * 2.6, col, 0.08 * k)
    ctx.restore()


EFFECTS = {
    # back-to-front draw order
    "clouds": clouds, "ocean_mist": ocean_mist, "fog": fog, "poison_smoke": poison_smoke, "rays": rays,
    "throat_glow": throat_glow, "energy_wave": energy_wave, "dust": dust, "embers": embers, "sparks": sparks,
    "lightning": lightning, "rain_light": dust,
}
ORDER = list(EFFECTS)


def draw_all(ctx, names, t, dur, env):
    for name in ORDER:
        if name in names:
            EFFECTS[name](ctx, t, dur, env)


# ---------------------------------------------------------------- finishing (per frame)

@lru_cache(maxsize=1)
def _vignette() -> cairo.RadialGradient:
    g = cairo.RadialGradient(W / 2, H * 0.45, H * 0.25, W / 2, H * 0.45, H * 0.78)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.72)
    return g


def vignette(ctx):
    ctx.set_source(_vignette())
    ctx.paint()


@lru_cache(maxsize=1)
def _grain_bank(n: int = 6) -> list[np.ndarray]:
    r = np.random.default_rng(99)
    return [r.normal(0, 5.5, (H // 2, W // 2)).astype(np.int16) for _ in range(n)]


def grain(bgra: np.ndarray, frame_idx: int) -> None:
    """In-place film grain on a BGRA uint8 frame (half-res noise, upsampled by repetition)."""
    g = _grain_bank()[frame_idx % 6]
    g = np.repeat(np.repeat(g, 2, 0), 2, 1)[:, :, None]
    rgb = bgra[:, :, :3].astype(np.int16) + g
    np.clip(rgb, 0, 255, out=rgb)
    bgra[:, :, :3] = rgb.astype(np.uint8)
