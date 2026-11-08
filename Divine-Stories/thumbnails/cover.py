"""Shorts cover (1080x1920): the character's approved primary portrait, strong grade, one Hindi headline.

Layout: face in the upper-middle third, headline below it, nothing in the bottom Shorts UI band.
Driven by story["thumbnail"] if present, else sensible defaults from the story.
"""

from __future__ import annotations

import math

import cairo
import numpy as np
from PIL import Image

from characters import library as chars
from compositor import text as T
from compositor.captions import GOLD
from config import settings as S
from generators.commons import load_manifest
from visuals import camera, effects


def build(story: dict, out_png) -> dict:
    th = story.get("thumbnail", {})
    char = th.get("character") or (story["characters"][0] if story["characters"] else None)
    asset = th.get("asset") or (chars.approved(char)["primary_portrait"] if char else story["scenes"][0]["visual"]["asset"])
    bounds = tuple(th.get("bounds", next((s["visual"].get("bounds", (0, 0, 1, 1)) for s in story["scenes"]
                                          if s["visual"]["asset"] == asset), (0, 0, 1, 1))))
    focus = tuple(th.get("focus", (0.45, 0.42)))
    zoom = th.get("zoom", 1.9)
    src = camera.prepare(S.ROOT / load_manifest()[asset]["local"], bounds, th.get("grade", "divine"), zoom)
    shot = camera.Shot(src, focus, (0, 0), (zoom, zoom), 1.0)
    rgb = np.asarray(shot.frame(1.0))
    bgra = np.empty((S.H, S.W, 4), np.uint8)
    bgra[..., 0], bgra[..., 1], bgra[..., 2], bgra[..., 3] = rgb[..., 2], rgb[..., 1], rgb[..., 0], 255
    surf = cairo.ImageSurface.create_for_data(memoryview(bgra), cairo.FORMAT_ARGB32, S.W, S.H, S.W * 4)
    ctx = cairo.Context(surf)
    env = effects.Env(shot, th.get("fx", {}), {}, seed=4242, grade="divine")
    effects.draw_all(ctx, th.get("effects", ["rays", "dust"]), 1.0, 1.0, env)
    effects.vignette(ctx)
    g = cairo.LinearGradient(0, S.H * 0.5, 0, S.H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(0.45, 0, 0, 0, 0.75)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.92)
    ctx.set_source(g)
    ctx.rectangle(0, S.H * 0.5, S.W, S.H * 0.5)
    ctx.fill()
    headline = th.get("headline", story["title_hi"])
    sub = th.get("subline", "")
    size = 150
    while T.width(headline, size) > S.W - 120 and size > 70:
        size -= 6
    hy = th.get("headline_y", 1230)
    glow_g = cairo.RadialGradient(S.W / 2, hy, 20, S.W / 2, hy, 520)
    glow_g.add_color_stop_rgba(0, 1.0, 0.7, 0.3, 0.25)
    glow_g.add_color_stop_rgba(1, 1.0, 0.7, 0.3, 0)
    ctx.set_source(glow_g)
    ctx.paint()
    T.draw(ctx, headline, S.W / 2, hy, size, GOLD, 1.0, stroke=18, stroke_color=(0.06, 0.02, 0.0), shadow=10)
    if sub:
        T.draw(ctx, sub, S.W / 2, hy + size * 0.95, 66, (1, 1, 1), 1.0, stroke=10, stroke_color=(0, 0, 0))
    T.draw(ctx, S.CHANNEL_NAME_HI, S.W / 2, 230, 40, (1, 0.95, 0.85), 0.9, stroke=5, stroke_color=(0, 0, 0))
    surf.flush()
    im = Image.fromarray(bgra[:, :, [2, 1, 0]])
    im.save(out_png)
    preview = im.resize((S.W // 4, S.H // 4), Image.LANCZOS)   # roughly feed size: check legibility
    preview.save(str(out_png).replace(".png", "_feed_preview.png"))
    return {"asset": asset, "headline": headline}
