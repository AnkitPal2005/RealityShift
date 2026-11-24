"""Brain Blitz - Spot the Difference Short renderer (original procedural art).

Fixes from Short #1 data (37.85% viewed, 98.86% APV, 0 comments):
  * Frame 0 already shows both panels + header + full timer (no intro).
  * Comment prompt ("KITNE MILE? 1, 2 YA 3?") before/while the answer shows.
  * Last 0.5 s returns to the frame-0 look so the Short loops.
  * 2 fair differences + 1 genuinely hard one.

Usage:  python core/spot_diff.py            -> output/spot_diff_01/spot_diff_01.mp4
        python core/spot_diff.py --preview  -> only preview stills
"""
import os, sys, math, random, subprocess, wave
import numpy as np
import cairo

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = "spot_diff_01"
OUT = os.path.join(BASE, "output", NAME)
os.makedirs(OUT, exist_ok=True)

W, H, FPS, DUR = 1080, 1920, 30, 16.0
PX, PW, PH = 60, 960, 640
PA_Y, PB_Y = 250, 930
PUZZLE_END = 10.0
BEAT_NO = 1   # phonk beat for this Short - give every new Short its own number
FONT = "Impact"

# (local x, local y, circle r, reveal time, label)
DIFFS = [
    (300, 283, 62, 11.0, "EASY"),
    (545, 96, 36, 12.1, "MEDIUM"),
    (440, 369, 28, 13.2, "99% MISSED THIS!"),
]


# ----------------------------------------------------------------- helpers
def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def ease_out_back(x):
    c1, c3 = 1.70158, 2.70158
    x = clamp(x)
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()


def lin(ctx, x0, y0, x1, y1, stops):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    for o, c in stops:
        g.add_color_stop_rgba(o, *c) if len(c) == 4 else g.add_color_stop_rgb(o, *c)
    return g


def text_c(ctx, s, cx, cy, size, fill, stroke=(0, 0, 0), sw=10, scale=1.0, alpha=1.0):
    """Centered Impact text with outline + soft shadow. ASCII only."""
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(scale, scale)
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    xb, yb, tw, th, _, _ = ctx.text_extents(s)
    x, y = -tw / 2 - xb, -yb - th / 2
    # shadow
    ctx.move_to(x + 4, y + 6)
    ctx.text_path(s)
    ctx.set_source_rgba(0, 0, 0, 0.45 * alpha)
    ctx.set_line_width(sw)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.stroke_preserve()
    ctx.fill()
    ctx.move_to(x, y)
    ctx.text_path(s)
    ctx.set_source_rgba(*stroke, alpha)
    ctx.stroke_preserve()
    ctx.set_source_rgba(*fill, alpha)
    ctx.fill()
    ctx.restore()


def pill(ctx, s, cx, cy, size, bg, fg=(1, 1, 1), scale=1.0, alpha=1.0):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(scale, scale)
    ctx.select_font_face(FONT)
    ctx.set_font_size(size)
    xb, yb, tw, th, _, _ = ctx.text_extents(s)
    pw, ph = tw + size * 0.9, th + size * 0.6
    rrect(ctx, -pw / 2 + 3, -ph / 2 + 5, pw, ph, ph / 2)
    ctx.set_source_rgba(0, 0, 0, 0.35 * alpha)
    ctx.fill()
    rrect(ctx, -pw / 2, -ph / 2, pw, ph, ph / 2)
    ctx.set_source_rgba(*bg, alpha)
    ctx.fill_preserve()
    ctx.set_source_rgba(1, 1, 1, 0.9 * alpha)
    ctx.set_line_width(4)
    ctx.stroke()
    ctx.move_to(-tw / 2 - xb, -yb - th / 2)
    ctx.set_source_rgba(*fg, alpha)
    ctx.show_text(s)
    ctx.restore()


# ----------------------------------------------------------------- the scene
def draw_scene(ctx, variant, t=0.0):
    """Cozy evening room, 960x640 local space. variant 'A' or 'B'.
    Everything that moves depends only on t, so both panels move identically;
    the 3 differences themselves never move or change."""
    A = variant == "A"

    # wall
    ctx.set_source(lin(ctx, 0, 0, 0, 470, [(0, (0.99, 0.87, 0.72)), (1, (0.95, 0.76, 0.62))]))
    ctx.rectangle(0, 0, 960, 470)
    ctx.fill()
    for x in range(0, 960, 48):
        ctx.rectangle(x, 0, 22, 470)
        ctx.set_source_rgba(1, 1, 1, 0.08)
        ctx.fill()
    # floor
    ctx.set_source(lin(ctx, 0, 470, 0, 640, [(0, (0.74, 0.49, 0.31)), (1, (0.52, 0.31, 0.19))]))
    ctx.rectangle(0, 470, 960, 170)
    ctx.fill()
    rnd = random.Random(7)
    for i, y in enumerate([500, 535, 575, 618]):
        ctx.set_source_rgba(0, 0, 0, 0.13)
        ctx.set_line_width(2)
        ctx.move_to(0, y)
        ctx.line_to(960, y)
        ctx.stroke()
        off = rnd.randint(0, 200)
        for x in range(off, 960, 240):
            ctx.move_to(x, y)
            ctx.line_to(x, y - (30 if i else 30))
            ctx.stroke()
    # baseboard
    ctx.set_source_rgb(0.88, 0.70, 0.55)
    ctx.rectangle(0, 458, 960, 14)
    ctx.fill()

    # --- window with sunset sky
    ctx.set_source_rgb(0.97, 0.95, 0.90)
    rrect(ctx, 40, 40, 240, 270, 8)
    ctx.fill()
    ctx.save()
    ctx.rectangle(55, 55, 210, 240)
    ctx.clip()
    ctx.set_source(lin(ctx, 0, 55, 0, 295, [(0, (0.13, 0.17, 0.42)), (0.55, (0.55, 0.33, 0.58)),
                                            (1, (1.0, 0.62, 0.40))]))
    ctx.paint()
    srnd = random.Random(3)
    for k in range(14):
        sx, sy = srnd.uniform(60, 260), srnd.uniform(60, 170)
        base = srnd.uniform(0.5, 1)
        tw = 0.55 + 0.45 * math.sin(t * 3.2 + k * 1.7)
        ctx.arc(sx, sy, srnd.uniform(1.2, 2.4), 0, 2 * math.pi)
        ctx.set_source_rgba(1, 1, 0.9, base * tw)
        ctx.fill()
    # shooting star (same moment in both panels)
    for st0 in (2.6, 8.4):
        sp = (t - st0) / 0.7
        if 0 <= sp <= 1:
            hx, hy = 250 - 190 * sp, 65 + 70 * sp
            g = cairo.LinearGradient(hx, hy, hx + 60, hy - 22)
            g.add_color_stop_rgba(0, 1, 1, 0.9, 1 - sp * 0.6)
            g.add_color_stop_rgba(1, 1, 1, 0.9, 0)
            ctx.set_source(g)
            ctx.set_line_width(3)
            ctx.move_to(hx, hy)
            ctx.line_to(hx + 60, hy - 22)
            ctx.stroke()
    g = cairo.RadialGradient(205, 100, 10, 205, 100, 60)
    g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.45)
    g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0)
    ctx.set_source(g)
    ctx.arc(205, 100, 60, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source_rgb(1, 0.97, 0.82)
    ctx.arc(205, 100, 20, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source_rgb(0.24, 0.24, 0.50)
    ctx.arc(214, 94, 18, 0, 2 * math.pi)
    ctx.fill()
    # hills
    ctx.move_to(55, 250)
    ctx.curve_to(110, 215, 150, 225, 190, 245)
    ctx.curve_to(220, 230, 250, 228, 265, 238)
    ctx.line_to(265, 295)
    ctx.line_to(55, 295)
    ctx.close_path()
    ctx.set_source_rgb(0.30, 0.18, 0.40)
    ctx.fill()
    ctx.move_to(55, 275)
    ctx.curve_to(120, 255, 190, 262, 265, 270)
    ctx.line_to(265, 295)
    ctx.line_to(55, 295)
    ctx.close_path()
    ctx.set_source_rgb(0.20, 0.12, 0.28)
    ctx.fill()
    ctx.restore()
    ctx.set_source_rgb(0.97, 0.95, 0.90)
    ctx.rectangle(156, 55, 8, 240)
    ctx.rectangle(55, 172, 210, 8)
    ctx.fill()
    ctx.set_source_rgb(0.90, 0.86, 0.80)
    rrect(ctx, 28, 304, 264, 16, 4)
    ctx.fill()
    # curtain rod + curtains
    ctx.set_source_rgb(0.45, 0.28, 0.16)
    ctx.set_line_width(7)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(14, 30)
    ctx.line_to(306, 30)
    ctx.stroke()
    for side in (0, 1):
        ctx.save()
        if side:
            ctx.translate(320, 0)
            ctx.scale(-1, 1)
        sw = 5 * math.sin(t * 1.3 + side * 1.1)
        ctx.move_to(14, 32)
        ctx.line_to(80, 32)
        ctx.curve_to(70, 120, 48 + sw * 0.6, 200, 62 + sw, 330)
        ctx.line_to(10 + sw, 330)
        ctx.curve_to(18 + sw * 0.6, 220, 10, 120, 14, 32)
        ctx.close_path()
        ctx.set_source(lin(ctx, 10, 0, 80, 0, [(0, (0.12, 0.45, 0.50)), (0.5, (0.22, 0.62, 0.66)),
                                               (1, (0.14, 0.48, 0.53))]))
        ctx.fill()
        ctx.set_source_rgba(0, 0, 0, 0.15)
        ctx.set_line_width(3)
        for fx in (30, 50):
            ctx.move_to(fx, 40)
            ctx.curve_to(fx - 4, 150, fx - 10, 240, fx - 6, 325)
            ctx.stroke()
        ctx.restore()

    # --- painting (sun only in A)
    ctx.set_source(lin(ctx, 400, 60, 580, 200, [(0, (0.95, 0.78, 0.35)), (0.5, (0.78, 0.55, 0.20)),
                                                (1, (0.95, 0.78, 0.35))]))
    rrect(ctx, 396, 56, 188, 148, 6)
    ctx.fill()
    ctx.save()
    ctx.rectangle(410, 70, 160, 120)
    ctx.clip()
    ctx.set_source(lin(ctx, 0, 70, 0, 190, [(0, (0.55, 0.80, 0.98)), (1, (0.95, 0.92, 0.80))]))
    ctx.paint()
    if A:
        ctx.set_source_rgb(1.0, 0.80, 0.20)
        ctx.arc(545, 96, 15, 0, 2 * math.pi)
        ctx.fill()
    ctx.move_to(410, 170)
    ctx.line_to(455, 115)
    ctx.line_to(490, 150)
    ctx.line_to(520, 120)
    ctx.line_to(570, 165)
    ctx.line_to(570, 190)
    ctx.line_to(410, 190)
    ctx.close_path()
    ctx.set_source_rgb(0.35, 0.55, 0.62)
    ctx.fill()
    ctx.move_to(445, 127)
    ctx.line_to(455, 115)
    ctx.line_to(466, 126)
    ctx.close_path()
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()
    ctx.rectangle(410, 172, 160, 18)
    ctx.set_source_rgb(0.38, 0.68, 0.40)
    ctx.fill()
    ctx.restore()

    # --- wall clock (10:10)
    ctx.set_source_rgba(0, 0, 0, 0.15)
    ctx.arc(664, 119, 50, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source_rgb(0.30, 0.22, 0.18)
    ctx.arc(660, 115, 50, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source_rgb(0.99, 0.98, 0.94)
    ctx.arc(660, 115, 42, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source_rgb(0.3, 0.25, 0.2)
    for i in range(12):
        a = i * math.pi / 6
        ctx.set_line_width(4 if i % 3 == 0 else 2)
        ctx.move_to(660 + 34 * math.cos(a), 115 + 34 * math.sin(a))
        ctx.line_to(660 + 39 * math.cos(a), 115 + 39 * math.sin(a))
        ctx.stroke()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for ang, ln, lw in ((math.radians(-150 + 5), 22, 5), (math.radians(-30), 32, 3)):
        ctx.set_line_width(lw)
        ctx.move_to(660, 115)
        ctx.line_to(660 + ln * math.cos(ang), 115 + ln * math.sin(ang))
        ctx.stroke()
    # second hand ticks with the countdown (small overshoot on each tick)
    sec = math.floor(t) + min(1.0, (t % 1.0) / 0.12) * (1 + 0.15 * math.sin(min(1.0, (t % 1.0) / 0.25) * math.pi))
    sa_ = -math.pi / 2 + 2 * math.pi * (8 + sec) / 60
    ctx.set_source_rgb(0.85, 0.25, 0.25)
    ctx.set_line_width(2)
    ctx.move_to(660 - 8 * math.cos(sa_), 115 - 8 * math.sin(sa_))
    ctx.line_to(660 + 36 * math.cos(sa_), 115 + 36 * math.sin(sa_))
    ctx.stroke()
    ctx.arc(660, 115, 4, 0, 2 * math.pi)
    ctx.fill()

    # --- bookshelf + plant
    ctx.set_source_rgba(0, 0, 0, 0.15)
    ctx.rectangle(778, 198, 155, 280)
    ctx.fill()
    ctx.set_source_rgb(0.52, 0.33, 0.20)
    ctx.rectangle(770, 190, 155, 285)
    ctx.fill()
    ctx.set_source_rgb(0.33, 0.20, 0.13)
    ctx.rectangle(780, 200, 135, 265)
    ctx.fill()
    brnd = random.Random(11)
    colors = [(0.85, 0.30, 0.30), (0.25, 0.50, 0.80), (0.95, 0.75, 0.25), (0.35, 0.65, 0.45),
              (0.60, 0.40, 0.75), (0.95, 0.55, 0.30), (0.20, 0.35, 0.55)]
    for sy in (200, 290, 380):
        x = 783
        while x < 905:
            bw = brnd.randint(12, 20)
            bh = brnd.randint(55, 78)
            if x + bw > 912:
                break
            if brnd.random() < 0.15:
                ctx.save()
                ctx.translate(x, sy + 85)
                ctx.rotate(-0.25)
                ctx.rectangle(0, -bh, bw, bh)
                ctx.restore()
                x += 10
            else:
                ctx.rectangle(x, sy + 85 - bh, bw, bh)
            ctx.set_source_rgb(*brnd.choice(colors))
            ctx.fill()
            ctx.rectangle(x + 2, sy + 85 - bh + 10, bw - 4, 4)
            ctx.set_source_rgba(1, 1, 1, 0.35)
            ctx.fill()
            x += bw + 2
        ctx.set_source_rgb(0.58, 0.38, 0.24)
        ctx.rectangle(775, sy + 85, 145, 7)
        ctx.fill()
    for i, (lx, ly, rot) in enumerate([(830, 160, -0.8), (850, 150, 0.0), (870, 160, 0.8),
                                       (818, 175, -1.2), (882, 175, 1.2)]):
        ctx.save()
        ctx.translate(850, 175)
        ctx.rotate(0.05 * math.sin(t * 1.6 + i))
        ctx.translate(lx - 850, ly - 175)
        ctx.rotate(rot)
        ctx.scale(1, 2.2)
        ctx.arc(0, 0, 11, 0, 2 * math.pi)
        ctx.restore()
        ctx.set_source_rgb(0.25 + 0.05 * i, 0.62, 0.35)
        ctx.fill()
    ctx.move_to(826, 168)
    ctx.line_to(874, 168)
    ctx.line_to(866, 190)
    ctx.line_to(834, 190)
    ctx.close_path()
    ctx.set_source_rgb(0.85, 0.45, 0.30)
    ctx.fill()

    # --- rug
    for rx, ry, c in ((330, 56, (0.80, 0.28, 0.33)), (300, 46, (0.96, 0.80, 0.52)),
                      (270, 38, (0.80, 0.28, 0.33)), (190, 24, (0.35, 0.55, 0.65))):
        ctx.save()
        ctx.translate(520, 568)
        ctx.scale(rx, ry)
        ctx.arc(0, 0, 1, 0, 2 * math.pi)
        ctx.restore()
        ctx.set_source_rgb(*c)
        ctx.fill()

    # --- side table + fishbowl
    ctx.set_source_rgba(0, 0, 0, 0.2)
    ctx.save()
    ctx.translate(140, 480)
    ctx.scale(85, 8)
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()
    ctx.fill()
    ctx.set_source_rgb(0.45, 0.28, 0.17)
    ctx.rectangle(75, 405, 10, 75)
    ctx.rectangle(195, 405, 10, 75)
    ctx.fill()
    ctx.set_source(lin(ctx, 0, 392, 0, 410, [(0, (0.66, 0.44, 0.28)), (1, (0.50, 0.32, 0.20))]))
    rrect(ctx, 58, 394, 164, 16, 5)
    ctx.fill()
    ctx.save()
    ctx.arc(140, 357, 37, 0, 2 * math.pi)
    ctx.clip()
    ctx.set_source_rgba(0.85, 0.95, 1.0, 0.35)
    ctx.paint()
    ctx.rectangle(100, 340, 80, 60)
    ctx.set_source(lin(ctx, 0, 340, 0, 395, [(0, (0.45, 0.75, 0.95, 0.85)), (1, (0.20, 0.50, 0.80, 0.9))]))
    ctx.fill()
    ctx.restore()
    # fish swims back and forth
    fxp = 140 + 14 * math.sin(t * 1.4)
    face = -1 if math.cos(t * 1.4) > 0 else 1   # -1 = facing right
    fy = 366 + 3 * math.sin(t * 2.3)
    wag = 3 * math.sin(t * 12)
    ctx.save()
    ctx.translate(fxp, fy)
    ctx.scale(-face, 1)   # drawn facing left
    ctx.set_source_rgb(1.0, 0.55, 0.15)
    ctx.save()
    ctx.scale(13, 8)
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()
    ctx.fill()
    ctx.move_to(11, 0)
    ctx.line_to(23, -8 + wag)
    ctx.line_to(23, 8 + wag)
    ctx.close_path()
    ctx.fill()
    ctx.set_source_rgb(0.1, 0.1, 0.1)
    ctx.arc(-6, -2, 1.8, 0, 2 * math.pi)
    ctx.fill()
    ctx.restore()
    ctx.save()
    ctx.arc(140, 357, 36, 0, 2 * math.pi)
    ctx.clip()
    for k in range(3):
        ph = (t * 0.9 + k / 3.0) % 1.0
        bx = 128 + 10 * k + 3 * math.sin(t * 4 + k)
        by = 385 - ph * 50
        ctx.new_path()
        ctx.arc(bx, by, 2 + k * 0.6, 0, 2 * math.pi)
        ctx.set_source_rgba(1, 1, 1, 0.85 * (1 - ph))
        ctx.set_line_width(1.5)
        ctx.stroke()
    ctx.restore()
    ctx.set_source_rgba(1, 1, 1, 0.7)
    ctx.set_line_width(3)
    ctx.arc(140, 357, 37, 0, 2 * math.pi)
    ctx.stroke()
    ctx.arc(140, 357, 28, math.radians(200), math.radians(250))
    ctx.set_source_rgba(1, 1, 1, 0.9)
    ctx.set_line_width(4)
    ctx.stroke()
    ctx.set_source_rgba(0.35, 0.55, 0.30, 1)
    ctx.rectangle(124, 383, 5, 12)
    ctx.rectangle(150, 380, 5, 15)
    ctx.fill()

    # --- sofa
    ctx.set_source_rgba(0, 0, 0, 0.22)
    ctx.save()
    ctx.translate(520, 478)
    ctx.scale(220, 13)
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()
    ctx.fill()
    ctx.set_source_rgb(0.35, 0.22, 0.14)
    for lx in (342, 690):
        ctx.rectangle(lx, 455, 12, 20)
    ctx.fill()
    ctx.set_source(lin(ctx, 0, 300, 0, 410, [(0, (0.50, 0.43, 0.78)), (1, (0.38, 0.32, 0.64))]))
    rrect(ctx, 340, 300, 360, 115, 30)
    ctx.fill()
    ctx.set_source_rgba(0, 0, 0, 0.12)
    ctx.set_line_width(3)
    ctx.move_to(520, 312)
    ctx.line_to(520, 400)
    ctx.stroke()
    ctx.set_source(lin(ctx, 0, 395, 0, 460, [(0, (0.55, 0.48, 0.82)), (1, (0.42, 0.36, 0.70))]))
    rrect(ctx, 330, 395, 380, 64, 18)
    ctx.fill()
    for ax in (306, 674):
        ctx.set_source(lin(ctx, ax, 0, ax + 60, 0, [(0, (0.36, 0.30, 0.60)), (0.5, (0.45, 0.39, 0.72)),
                                                    (1, (0.34, 0.28, 0.58))]))
        rrect(ctx, ax, 350, 60, 112, 26)
        ctx.fill()
    # cushion
    ctx.save()
    ctx.translate(628, 365)
    ctx.rotate(0.12)
    rrect(ctx, -42, -40, 84, 80, 20)
    ctx.set_source(lin(ctx, -42, -40, 42, 40, [(0, (1.0, 0.80, 0.35)), (1, (0.92, 0.62, 0.22))]))
    ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.35)
    ctx.set_line_width(3)
    for d in (-20, 0, 20):
        ctx.move_to(-30, d)
        ctx.line_to(30, d)
    ctx.stroke()
    ctx.set_source_rgb(0.75, 0.45, 0.15)
    ctx.arc(0, 0, 5, 0, 2 * math.pi)
    ctx.fill()
    ctx.restore()

    # --- floor lamp (shade colour differs)
    ctx.set_source_rgb(0.22, 0.20, 0.20)
    ctx.save()
    ctx.translate(300, 478)
    ctx.scale(32, 8)
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()
    ctx.fill()
    ctx.rectangle(296, 300, 8, 178)
    ctx.fill()
    shade = ((1.0, 0.50, 0.40), (0.85, 0.32, 0.28)) if A else ((0.30, 0.72, 0.75), (0.16, 0.52, 0.58))
    ctx.move_to(268, 250)
    ctx.line_to(332, 250)
    ctx.line_to(354, 316)
    ctx.line_to(246, 316)
    ctx.close_path()
    ctx.set_source(lin(ctx, 246, 0, 354, 0, [(0, shade[1]), (0.45, shade[0]), (1, shade[1])]))
    ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.5)
    ctx.set_line_width(3)
    ctx.move_to(246, 316)
    ctx.line_to(354, 316)
    ctx.stroke()

    # --- cat on the sofa (bell only in A)
    org, dark, light = (1.0, 0.63, 0.27), (0.85, 0.45, 0.15), (1.0, 0.88, 0.70)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    breath = math.sin(t * 2 * math.pi / 2.4)
    sw = math.sin(t * 2.6)                       # tail swish
    tip = (555 + 22 * sw, 338 - 6 * abs(sw))
    ctx.set_source_rgb(*org)
    ctx.set_line_width(15)
    ctx.move_to(525, 405)
    ctx.curve_to(575, 400, 588 + 8 * sw, 360, tip[0], tip[1])
    ctx.stroke()
    ctx.set_source_rgb(*dark)
    ctx.arc(tip[0], tip[1], 7.5, 0, 2 * math.pi)
    ctx.fill()
    ctx.save()
    ctx.translate(482, 380 - 1.5 * breath)
    ctx.scale(58 * (1 + 0.015 * breath), 40 * (1 + 0.04 * breath))
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()
    ctx.set_source(lin(ctx, 0, 340, 0, 420, [(0, org), (1, dark)]))
    ctx.fill()
    ctx.set_source_rgba(*dark, 1)
    ctx.set_line_width(5)
    for sx in (490, 508, 524):
        ctx.move_to(sx, 343)
        ctx.curve_to(sx + 6, 355, sx + 6, 365, sx + 2, 375)
        ctx.stroke()
    ctx.save()
    ctx.translate(455, 392)
    ctx.scale(26, 20)
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()
    ctx.set_source_rgb(*light)
    ctx.fill()
    for px in (428, 456):
        ctx.save()
        ctx.translate(px, 410)
        ctx.scale(12, 7)
        ctx.arc(0, 0, 1, 0, 2 * math.pi)
        ctx.restore()
        ctx.set_source_rgb(*light)
        ctx.fill()
    # head group: gentle bob + tilt (collar/bell move with it in both panels)
    ctx.save()
    ctx.translate(440, 365)
    ctx.rotate(0.035 * math.sin(t * 0.9))
    ctx.translate(-440, -365 - 1.8 * breath)
    # ears (right ear twitches now and then)
    twitch = math.sin(clamp(((t + 1.0) % 4.0) / 0.3) * math.pi) * 0.12
    ears = ((((410, 316), (414, 280), (440, 304)), ((416, 309), (418, 290), (432, 304))),
            (((442, 302), (468, 280), (472, 318)), ((450, 302), (466, 290), (467, 310))))
    for ei, (pts, inner) in enumerate(ears):
        ctx.save()
        if ei == 1:
            ctx.translate(458, 312)
            ctx.rotate(twitch)
            ctx.translate(-458, -312)
        ctx.move_to(*pts[0])
        ctx.line_to(*pts[1])
        ctx.line_to(*pts[2])
        ctx.close_path()
        ctx.set_source_rgb(*org)
        ctx.fill()
        ctx.move_to(*inner[0])
        ctx.line_to(*inner[1])
        ctx.line_to(*inner[2])
        ctx.close_path()
        ctx.set_source_rgb(1.0, 0.70, 0.72)
        ctx.fill()
        ctx.restore()
    ctx.arc(440, 333, 37, 0, 2 * math.pi)
    ctx.set_source(lin(ctx, 0, 296, 0, 370, [(0, org), (1, (0.96, 0.56, 0.22))]))
    ctx.fill()
    ctx.set_source_rgb(*dark)
    ctx.set_line_width(4)
    for sx in (430, 440, 450):
        ctx.move_to(sx, 299)
        ctx.line_to(sx, 311)
        ctx.stroke()
    ctx.save()
    ctx.translate(440, 346)
    ctx.scale(19, 13)
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()
    ctx.set_source_rgb(*light)
    ctx.fill()
    ctx.set_source_rgb(0.25, 0.15, 0.10)
    ctx.set_line_width(3.5)
    for ex in (425, 455):
        ctx.arc(ex, 330, 7, math.radians(200), math.radians(340))
        ctx.stroke()
    ctx.set_source_rgba(1.0, 0.55, 0.55, 0.6)
    for bx in (414, 466):
        ctx.arc(bx, 343, 7, 0, 2 * math.pi)
        ctx.fill()
    ctx.set_source_rgb(0.95, 0.45, 0.50)
    ctx.move_to(436, 340)
    ctx.line_to(444, 340)
    ctx.line_to(440, 345)
    ctx.close_path()
    ctx.fill()
    ctx.set_source_rgb(0.25, 0.15, 0.10)
    ctx.set_line_width(2)
    ctx.move_to(440, 345)
    ctx.curve_to(438, 350, 434, 351, 432, 348)
    ctx.move_to(440, 345)
    ctx.curve_to(442, 350, 446, 351, 448, 348)
    ctx.stroke()
    ctx.set_source_rgba(0.3, 0.2, 0.15, 0.7)
    ctx.set_line_width(1.5)
    for side in (-1, 1):
        for dy in (-3, 3):
            ctx.move_to(440 + side * 16, 346 + dy)
            ctx.line_to(440 + side * 40, 342 + dy * 2.2)
    ctx.stroke()
    # collar
    ctx.set_source_rgb(0.85, 0.15, 0.25)
    ctx.set_line_width(7)
    ctx.move_to(415, 359)
    ctx.curve_to(428, 368, 452, 368, 465, 359)
    ctx.stroke()
    if A:
        ctx.set_source_rgb(0.98, 0.80, 0.20)
        ctx.arc(440, 371, 6.5, 0, 2 * math.pi)
        ctx.fill()
        ctx.set_source_rgb(0.70, 0.50, 0.08)
        ctx.set_line_width(1.5)
        ctx.arc(440, 371, 6.5, 0, 2 * math.pi)
        ctx.stroke()
        ctx.move_to(437, 373)
        ctx.line_to(443, 373)
        ctx.stroke()
        ctx.set_source_rgba(1, 1, 1, 0.9)
        ctx.arc(438, 369, 1.8, 0, 2 * math.pi)
        ctx.fill()
    ctx.restore()  # end head group

    # --- lighting: lamp glow (soft flicker) + light cone + dust + vignette
    fl = 1 + 0.05 * math.sin(t * 7.3) + 0.03 * math.sin(t * 13.1)
    g = cairo.RadialGradient(300, 300, 10, 300, 300, 330)
    g.add_color_stop_rgba(0, 1.0, 0.85, 0.55, 0.42 * fl)
    g.add_color_stop_rgba(0.5, 1.0, 0.80, 0.50, 0.12 * fl)
    g.add_color_stop_rgba(1, 1.0, 0.80, 0.50, 0)
    ctx.set_source(g)
    ctx.paint()
    ctx.move_to(250, 316)
    ctx.line_to(350, 316)
    ctx.line_to(420, 478)
    ctx.line_to(180, 478)
    ctx.close_path()
    ctx.set_source(lin(ctx, 0, 316, 0, 478, [(0, (1, 0.92, 0.65, 0.20)), (1, (1, 0.92, 0.65, 0))]))
    ctx.fill()
    drnd = random.Random(21)
    for k in range(12):
        x0, y0, sp = drnd.uniform(200, 400), drnd.uniform(320, 470), drnd.uniform(8, 18)
        ph = drnd.uniform(0, 6.28)
        x = x0 + 12 * math.sin(t * 0.7 + ph)
        y = 320 + ((y0 - 320 - t * sp) % 150)
        ctx.arc(x, y, 1.6, 0, 2 * math.pi)
        ctx.set_source_rgba(1, 0.95, 0.75, 0.55 * (0.5 + 0.5 * math.sin(t * 2 + ph)))
        ctx.fill()
    g = cairo.RadialGradient(480, 320, 250, 480, 320, 640)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0.1, 0.03, 0.08, 0.35)
    ctx.set_source(g)
    ctx.paint()


def paint_scene(surf, variant, t):
    c = cairo.Context(surf)
    c.set_antialias(cairo.ANTIALIAS_BEST)
    c.set_operator(cairo.OPERATOR_CLEAR)
    c.paint()
    c.set_operator(cairo.OPERATOR_OVER)
    draw_scene(c, variant, t)
    surf.flush()
    return surf


# ----------------------------------------------------------------- frame
BOKEH = [(random.Random(i).uniform(0, W), random.Random(i + 99).uniform(0, H),
          random.Random(i + 7).uniform(20, 90), random.Random(i + 3).uniform(15, 45),
          random.Random(i + 5).choice([(1, 0.5, 0.8), (0.5, 0.7, 1), (1, 0.85, 0.4)]))
         for i in range(26)]
CONF = []
crnd = random.Random(42)
for _ in range(70):
    a = crnd.uniform(-math.pi, 0)
    sp = crnd.uniform(500, 1100)
    CONF.append((math.cos(a) * sp, math.sin(a) * sp, crnd.uniform(-8, 8), crnd.uniform(8, 16),
                 crnd.choice([(1, 0.3, 0.4), (1, 0.85, 0.2), (0.3, 0.8, 1), (0.5, 1, 0.5), (1, 1, 1)])))


def puzzle_header(ctx, t, alpha=1.0):
    pulse = 1 + 0.025 * math.sin(t * 5)
    text_c(ctx, "FIND 3 DIFFERENCES", W / 2, 128, 92, (1, 0.88, 0.15), sw=12, scale=pulse, alpha=alpha)
    text_c(ctx, "ONLY 1% FIND THE LAST ONE", W / 2, 205, 50, (1, 1, 1), sw=8, alpha=alpha)


def draw_frame(ctx, t, sa, sb):
    # background
    ctx.set_source(lin(ctx, 0, 0, 0, H, [(0, (0.22, 0.08, 0.42)), (0.5, (0.10, 0.08, 0.32)),
                                         (1, (0.04, 0.10, 0.28))]))
    ctx.paint()
    for x, y, r, sp, c in BOKEH:
        yy = (y - t * sp) % (H + 200) - 100
        g = cairo.RadialGradient(x, yy, 0, x, yy, r)
        g.add_color_stop_rgba(0, *c, 0.22)
        g.add_color_stop_rgba(1, *c, 0)
        ctx.set_source(g)
        ctx.arc(x, yy, r, 0, 2 * math.pi)
        ctx.fill()

    # urgency pulse in the last 3 seconds
    if 7.0 <= t < PUZZLE_END:
        a = 0.18 * (0.5 + 0.5 * math.sin(t * 2 * math.pi * 2))
        g = cairo.RadialGradient(W / 2, H / 2, 500, W / 2, H / 2, 1150)
        g.add_color_stop_rgba(0, 1, 0, 0, 0)
        g.add_color_stop_rgba(1, 1, 0.05, 0.1, a)
        ctx.set_source(g)
        ctx.paint()

    # panels
    for py, surf in ((PA_Y, sa), (PB_Y, sb)):
        for i in range(6):
            rrect(ctx, PX - 10 - i * 3, py - 6 - i * 3 + 14, PW + 20 + i * 6, PH + 20 + i * 6, 30 + i * 3)
            ctx.set_source_rgba(0, 0, 0, 0.07)
            ctx.fill()
        rrect(ctx, PX - 10, py - 10, PW + 20, PH + 20, 30)
        ctx.set_source(lin(ctx, 0, py, 0, py + PH, [(0, (1, 1, 1)), (1, (0.88, 0.88, 0.95))]))
        ctx.fill()
        ctx.save()
        rrect(ctx, PX, py, PW, PH, 22)
        ctx.clip()
        ctx.set_source_surface(surf, PX, py)
        ctx.paint()
        ctx.restore()

    # reveal circles
    fade = 1.0 - clamp((t - 15.1) / 0.45)
    for i, (lx, ly, r, ts, label) in enumerate(DIFFS):
        if t < ts or fade <= 0:
            continue
        p = ease_out((t - ts) / 0.35)
        sc = ease_out_back((t - ts) / 0.4)
        for py in (PA_Y, PB_Y):
            cx, cy = PX + lx, py + ly
            # flash ring
            fr = clamp((t - ts) / 0.5)
            if fr < 1:
                ctx.arc(cx, cy, r * (1 + fr * 1.2), 0, 2 * math.pi)
                ctx.set_source_rgba(1, 1, 0.6, (1 - fr) * 0.8 * fade)
                ctx.set_line_width(6)
                ctx.stroke()
            a0 = -math.pi / 2
            ctx.new_path()
            ctx.arc(cx, cy, r * sc, a0, a0 + 2 * math.pi * p)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgba(1, 1, 1, fade)
            ctx.set_line_width(16)
            ctx.stroke_preserve()
            ctx.set_source_rgba(1, 0.15, 0.3, fade)
            ctx.set_line_width(9)
            ctx.stroke()
        if t > ts + 0.25:
            lp = ease_out_back((t - ts - 0.25) / 0.35)
            hard = i == 2
            bx = PX + lx + (0 if not hard else 40)
            by = PB_Y + ly - r - 42
            if hard:
                by = PB_Y + ly + r + 50
            elif ly - r < 120:  # near the panel top: label goes below (timer ring sits above)
                by = PB_Y + ly + r + 38
            pill(ctx, label, bx, by, 46 if hard else 38,
                 (0.90, 0.10, 0.30) if hard else (0.10, 0.65, 0.35), scale=lp, alpha=fade)

    # magnifier zoom on the hard difference (both panels, so the eye compares)
    MAG_T = DIFFS[2][3] + 0.4
    if t >= MAG_T and fade > 0:
        ms = ease_out_back((t - MAG_T) / 0.4)
        hx, hy = DIFFS[2][0], DIFFS[2][1]
        mlx, mly, mr, zoom = 705, 300, 92, 3.0
        for py, variant in ((PA_Y, "A"), (PB_Y, "B")):
            mx, my = PX + mlx, py + mly
            ctx.save()
            ctx.set_source_rgba(1, 1, 1, 0.9 * fade)
            ctx.set_line_width(5)
            ctx.move_to(PX + hx + 20, py + hy - 20)
            ctx.line_to(mx - mr * ms * 0.7, my + mr * ms * 0.7)
            ctx.stroke()
            ctx.arc(mx + 4, my + 8, mr * ms + 8, 0, 2 * math.pi)
            ctx.set_source_rgba(0, 0, 0, 0.35 * fade)
            ctx.fill()
            ctx.new_path()
            ctx.arc(mx, my, mr * ms, 0, 2 * math.pi)
            ctx.clip()
            ctx.translate(mx, my)
            ctx.scale(zoom, zoom)
            ctx.translate(-hx, -hy)
            ctx.push_group()          # vector redraw = sharp zoom
            draw_scene(ctx, variant, t)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(fade)
            ctx.restore()
            ctx.new_path()
            ctx.arc(mx, my, mr * ms, 0, 2 * math.pi)
            ctx.set_source_rgba(1, 1, 1, fade)
            ctx.set_line_width(10)
            ctx.stroke_preserve()
            ctx.set_source_rgba(1, 0.15, 0.3, fade)
            ctx.set_line_width(5)
            ctx.stroke()

    # confetti on the hard reveal
    ts3 = DIFFS[2][3]
    if ts3 <= t < ts3 + 1.8:
        dt = t - ts3
        ox, oy = PX + DIFFS[2][0], PB_Y + DIFFS[2][1]
        for vx, vy, rot, sz, c in CONF:
            x = ox + vx * dt
            y = oy + vy * dt + 900 * dt * dt
            ctx.save()
            ctx.translate(x, y)
            ctx.rotate(rot * dt)
            ctx.rectangle(-sz / 2, -sz / 4, sz, sz / 2)
            ctx.set_source_rgba(*c, clamp(1.8 - dt))
            ctx.fill()
            ctx.restore()

    # timer ring between the panels
    cx, cy, R = W / 2, (PA_Y + PH + PB_Y) / 2, 62
    if t < PUZZLE_END:
        rem = PUZZLE_END - t
        frac = rem / PUZZLE_END
        num = str(int(math.ceil(rem - 1e-6)))
    elif t < 15.5:
        frac, num = 0.0, None
    else:
        frac = ease_out((t - 15.5) / 0.45)
        num = "10"
    col = (0.2, 0.9, 0.4) if frac > 0.5 else ((1, 0.8, 0.1) if frac > 0.3 else (1, 0.2, 0.25))
    beat = 1 + (0.08 * max(0, 1 - ((t % 1.0) / 0.25)) if 7.0 <= t < PUZZLE_END else 0)
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(beat, beat)
    ctx.arc(0, 4, R + 10, 0, 2 * math.pi)
    ctx.set_source_rgba(0, 0, 0, 0.4)
    ctx.fill()
    ctx.arc(0, 0, R + 10, 0, 2 * math.pi)
    ctx.set_source_rgb(0.12, 0.10, 0.25)
    ctx.fill_preserve()
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(5)
    ctx.stroke()
    ctx.arc(0, 0, R - 6, 0, 2 * math.pi)
    ctx.set_source_rgba(1, 1, 1, 0.12)
    ctx.set_line_width(12)
    ctx.stroke()
    if frac > 0:
        ctx.new_path()
        ctx.arc(0, 0, R - 6, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac)
        ctx.set_source_rgb(*col)
        ctx.set_line_width(12)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
    ctx.restore()
    if num is not None:
        text_c(ctx, num, cx, cy + 2, 64 * beat, (1, 1, 1), sw=6)
    else:
        found = sum(1 for d in DIFFS if t >= d[3])
        text_c(ctx, f"{found}/3", cx, cy + 2, 46, (1, 0.88, 0.15), sw=6)

    # header
    if t < PUZZLE_END:
        puzzle_header(ctx, t)
    elif t < 11.0:
        s = ease_out_back((t - PUZZLE_END) / 0.35)
        text_c(ctx, "TIME UP!", W / 2, 128, 110, (1, 0.25, 0.3), sw=14, scale=s)
        text_c(ctx, "KITNE MILE? 1, 2 YA 3?", W / 2, 208, 52, (1, 1, 1), sw=8,
               alpha=clamp((t - PUZZLE_END) / 0.25))
    elif t < 15.5:
        a = 1 - clamp((t - 15.25) / 0.25)
        text_c(ctx, "ANSWER", W / 2, 128, 100, (0.35, 1, 0.55), sw=14, alpha=a)
        text_c(ctx, "KITNE MILE? COMMENT KARO", W / 2, 208, 52, (1, 1, 1), sw=8, alpha=a)
    else:
        puzzle_header(ctx, t, alpha=clamp((t - 15.5) / 0.2))


# ----------------------------------------------------------------- audio
SR = 44100


def env_tone(freqs, dur, decay, vol=1.0, harm=0.3):
    t = np.arange(int(SR * dur)) / SR
    s = sum(np.sin(2 * np.pi * f * t) + harm * np.sin(4 * np.pi * f * t) for f in freqs)
    attack = np.clip(t / 0.004, 0, 1)
    return s * np.exp(-t * decay) * attack * vol / max(1, len(freqs))


def build_audio(path, music="pluck"):
    n = int(SR * DUR)
    mix = np.zeros(n)

    def put(sig, at, vol=1.0):
        i = int(at * SR)
        j = min(n, i + len(sig))
        if i < n:
            mix[i:j] += sig[:j - i] * vol

    if music == "phonk":
        from phonk import phonk_bed
        put(phonk_bed(DUR, beat_no=BEAT_NO, seed=1, breaks=[(PUZZLE_END, DIFFS[0][3])],
                      build=(7.0, PUZZLE_END)), 0, 0.55)
        for s in (7, 8, 9):                      # hats keep time; only the final 3 ticks
            put(env_tone([2400], 0.08, 70, 0.25, harm=0.5), s)
        _sfx(put)
        _finish(mix, path)
        return

    # light pluck bed: C - G - Am - F, 108 bpm eighths
    bpm = 108
    e = 60 / bpm / 2
    chords = [(261.63, 329.63, 392.0, 523.25), (246.94, 293.66, 392.0, 493.88),
              (261.63, 329.63, 440.0, 523.25), (261.63, 349.23, 440.0, 523.25)]
    bass = [130.81, 98.0, 110.0, 87.31]
    pattern = [0, 1, 2, 3, 2, 1, 2, 3]
    k = 0
    tt = 0.0
    while tt < DUR:
        bar = int(k // 8) % 4
        note = chords[bar][pattern[k % 8]]
        put(env_tone([note], 0.5, 7, 0.16, harm=0.25), tt)
        if k % 4 == 0:
            put(env_tone([bass[bar]], 0.9, 3.5, 0.22, harm=0.1), tt)
        if k % 2 == 1:
            hat = np.random.RandomState(k).uniform(-1, 1, int(SR * 0.05)) * np.exp(-np.arange(int(SR * 0.05)) / SR * 90)
            put(hat, tt, 0.03)
        tt += e
        k += 1

    # ticks for the countdown
    for s in range(10):
        hi = s >= 7
        put(env_tone([2400 if hi else 1800], 0.08, 70, 0.35, harm=0.5), s)
        if hi:
            put(env_tone([2400], 0.08, 70, 0.25, harm=0.5), s + 0.5)
    _sfx(put)
    _finish(mix, path)


def _sfx(put):
    # time up buzz
    t = np.arange(int(SR * 0.45)) / SR
    buzz = np.sign(np.sin(2 * np.pi * 160 * t)) * 0.18 * np.exp(-t * 4)
    put(buzz, PUZZLE_END)
    # reveal dings
    put(env_tone([1046.5, 1568.0], 0.9, 5, 0.5), DIFFS[0][3])
    put(env_tone([1174.7, 1760.0], 0.9, 5, 0.5), DIFFS[1][3])
    for j, f in enumerate([1046.5, 1318.5, 1568.0, 2093.0]):
        put(env_tone([f], 1.0, 4, 0.45), DIFFS[2][3] + j * 0.07)
    # whoosh into the loop
    t = np.arange(int(SR * 0.5)) / SR
    wn = np.random.RandomState(1).uniform(-1, 1, len(t))
    wn = np.convolve(wn, np.ones(30) / 30, mode="same")
    put(wn * np.sin(np.pi * t / 0.5) * 0.9, 15.45)


def _finish(mix, path):
    n = len(mix)
    fade = np.ones(n)
    fl = int(SR * 0.12)
    fade[:fl] = np.linspace(0.3, 1, fl)
    fade[-fl:] = np.linspace(1, 0.3, fl)
    mix *= fade
    mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
    data = (mix * 32767).astype(np.int16)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(data.tobytes())


# ----------------------------------------------------------------- main
def main():
    preview = "--preview" in sys.argv
    if "--phonk" in sys.argv:   # same video, phonk audio -> separate file (no re-render)
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        wav = os.path.join(OUT, "audio_phonk.wav")
        build_audio(wav, music="phonk")
        src = os.path.join(OUT, NAME + ".mp4")
        dst = os.path.join(OUT, NAME + "_phonk.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", wav, "-map", "0:v",
                        "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                        "-movflags", "+faststart", dst], check=True)
        print("done:", dst)
        return
    sa = cairo.ImageSurface(cairo.FORMAT_ARGB32, PW, PH)
    sb = cairo.ImageSurface(cairo.FORMAT_ARGB32, PW, PH)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)

    def frame(t):
        paint_scene(sa, "A", t)
        paint_scene(sb, "B", t)
        draw_frame(ctx, t, sa, sb)

    for name, t in (("p00_first_frame", 0.0), ("p01_countdown", 2.9), ("p02_time_up", 10.3),
                    ("p03_reveal_all", 14.3), ("p04_loop_end", 15.95)):
        frame(t)
        surf.write_to_png(os.path.join(OUT, name + ".png"))
    frame(0.0)
    surf.write_to_png(os.path.join(OUT, "thumbnail.png"))
    if preview:
        print("previews in", OUT)
        return

    wav = os.path.join(OUT, "audio.wav")
    build_audio(wav)
    mp4 = os.path.join(OUT, NAME + ".mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav,
           "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", mp4]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    total = int(DUR * FPS)
    for f in range(total):
        frame(f / FPS)
        surf.flush()
        proc.stdin.write(bytes(surf.get_data()))
        if f % 60 == 0:
            print(f"frame {f}/{total}", flush=True)
    proc.stdin.close()
    proc.wait()
    print("done:", mp4)


if __name__ == "__main__":
    main()
