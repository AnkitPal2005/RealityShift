"""Brain Blitz - "4 DIMAAG, 1 SAWAAL" lane-format Short (original procedural animation).

Format idea: one situation, 4 parallel lanes (types of people), camera visits each lane,
results stamped together, ends on "TUM KAUN HO? 1, 2, 3 YA 4?" (comment driver).
Brain Blitz's OWN look (not the neon-stickman look of the reference):
maths-notebook paper, cartoon kids with faces/expressions/hair, tape labels, chalkboards.
Story: 3 + 3 x 3 = ? (BODMAS answer 12).

Usage:  python core/lanes.py            -> output/lanes_01/lanes_01.mp4
        python core/lanes.py --preview  -> preview stills only
"""
import os, sys, math, random, subprocess, wave
import numpy as np
import cairo

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = "lanes_01"
OUT = os.path.join(BASE, "output", NAME)
os.makedirs(OUT, exist_ok=True)

W, H, FPS, DUR = 1080, 1920, 30, 28.5
FONT = "Impact"
LANE_H, LANE_GAP, LANES_TOP = 320, 12, 292
FLOOR = 290
OVERVIEW_C = (540, LANES_TOP + 2 * (LANE_H + LANE_GAP) - LANE_GAP / 2)
SCREEN_C = (540, 960)
GX, GS = 70, 1.3            # character group offset/scale inside a lane (x' = GX + x*GS)
FOCUS_S, FOCUS_X = 1.5, 545

PAPER = (0.985, 0.965, 0.90)
INK = (0.13, 0.14, 0.24)
RULE = (0.55, 0.72, 0.92)

LANES = [
    {"name": "TUKKA MASTER", "col": (1.00, 0.70, 0.10), "skin": (0.98, 0.80, 0.64), "hair": "spiky"},
    {"name": "COPY KING", "col": (0.20, 0.55, 0.95), "skin": (0.86, 0.64, 0.47), "hair": "cap"},
    {"name": "GIVE UP", "col": (0.62, 0.38, 0.90), "skin": (0.94, 0.74, 0.58), "hair": "messy"},
    {"name": "THINKER", "col": (0.15, 0.72, 0.42), "skin": (0.80, 0.58, 0.42), "hair": "neat"},
]

CAM = [(0.0, None), (3.5, 0), (8.0, 1), (12.2, 2), (16.4, 3), (21.5, None)]
CAM_MOVE = 0.6
STAMP_T = [22.6, 23.1, 23.6, 24.1]
END_T = 25.0


# ----------------------------------------------------------------- helpers
def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out_back(x):
    x = clamp(x)
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def lane_top(i):
    return LANES_TOP + i * (LANE_H + LANE_GAP)


def text(ctx, s, x, y, size, fill, stroke=None, sw=8, align="c", alpha=1.0):
    ctx.save()
    ctx.select_font_face(FONT)
    ctx.set_font_size(size)
    xb, yb, tw, th, _, _ = ctx.text_extents(s)
    tx = x - tw / 2 - xb if align == "c" else x - xb
    ty = y - yb - th / 2
    if stroke is not None:
        ctx.move_to(tx, ty)
        ctx.text_path(s)
        ctx.set_source_rgba(*stroke, alpha)
        ctx.set_line_width(sw)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke()
    ctx.move_to(tx, ty)
    ctx.text_path(s)
    ctx.set_source_rgba(*fill, alpha)
    ctx.fill()
    ctx.restore()
    return tw


def text_w(ctx, s, size):
    ctx.select_font_face(FONT)
    ctx.set_font_size(size)
    return ctx.text_extents(s)[2]


def rrect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()


def fill_outline(ctx, col, lw=4):
    ctx.set_source_rgb(*col)
    ctx.fill_preserve()
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(lw)
    ctx.stroke()


def limb(ctx, pts, col, w):
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    for lw, c in ((w + 8, INK), (w, col)):
        ctx.new_path()
        ctx.move_to(*pts[0])
        for p in pts[1:]:
            ctx.line_to(*p)
        ctx.set_source_rgb(*c)
        ctx.set_line_width(lw)
        ctx.stroke()


def paper_bg(ctx, x0, y0, w, h, margin=True):
    ctx.rectangle(x0, y0, w, h)
    ctx.set_source_rgb(*PAPER)
    ctx.fill()
    ctx.set_line_width(2)
    ctx.set_source_rgba(*RULE, 0.45)
    y = y0 + 34 - ((y0) % 34)
    while y < y0 + h:
        ctx.move_to(x0, y)
        ctx.line_to(x0 + w, y)
        y += 34
    ctx.stroke()
    if margin:
        ctx.set_source_rgba(0.90, 0.35, 0.40, 0.55)
        ctx.set_line_width(3)
        ctx.move_to(x0 + 70, y0)
        ctx.line_to(x0 + 70, y0 + h)
        ctx.stroke()


# ----------------------------------------------------------------- poses (lane-local coords, pre group scale)
_B = dict(head=(210, 146), neck=(206, 170), hip=(198, 232), lk=(244, 232), lf=(246, FLOOR - 2),
          rk=(240, 238), rf=(234, FLOOR - 2), le=(236, 198), lh=(266, 206), re=(230, 204), rh=(258, 211),
          look=(1, 0.6))
POSES = {
    "BASE": dict(_B),
    "WRITE": dict(_B, look=(1, 1)),
    "THINK": dict(_B, head=(212, 143), re=(238, 190), rh=(226, 162), look=(0.6, -1)),
    "SCRATCH": dict(_B, re=(246, 150), rh=(222, 112), look=(0.4, -1)),
    "CHEER": dict(_B, head=(208, 142), re=(222, 140), rh=(236, 100), look=(1, 0)),
    "BOTH_UP": dict(_B, le=(186, 148), lh=(170, 108), re=(232, 148), rh=(248, 108), look=(0, -1)),
    "SLEEP": dict(_B, head=(258, 190), neck=(232, 188), le=(242, 204), lh=(284, 205), re=(236, 208),
                  rh=(276, 210), look=(0, 0)),
    "PEEK": dict(_B, head=(196, 132), neck=(199, 158), re=(236, 196), rh=(262, 206), look=(0.3, -1)),
    "SLUMP": dict(_B, head=(222, 162), neck=(212, 182), le=(216, 210), lh=(226, 234), re=(222, 212),
                  rh=(236, 236), look=(0.5, 1)),
}
EXPR = {  # brows (inner raise, outer raise), mouth
    "BASE": ((0, 0), "smile"), "WRITE": ((0, 0), "line"), "THINK": ((-3, 2), "side"),
    "SCRATCH": ((4, -2), "wavy"), "CHEER": ((3, 3), "grin"), "BOTH_UP": ((-5, 3), "open"),
    "SLEEP": ((0, 0), "o"), "PEEK": ((-3, 3), "smirk"), "SLUMP": ((6, -2), "frown"),
}
TIMELINES = [
    [(0, "WRITE"), (4.0, "BASE"), (5.0, "SCRATCH"), (5.9, "WRITE"), (6.8, "CHEER"), (22.8, "SLUMP")],
    [(0, "WRITE"), (8.6, "BASE"), (9.5, "PEEK"), (10.9, "WRITE"), (11.6, "PEEK"), (23.3, "SLUMP")],
    [(0, "THINK"), (12.8, "SCRATCH"), (14.0, "BOTH_UP"), (14.9, "SLEEP")],
    [(0, "THINK"), (20.0, "WRITE"), (20.9, "BASE"), (24.2, "CHEER")],
]
CARDS = [(6.8, "18"), (11.6, "18"), (15.3, "?"), (20.9, "12")]
STAMP = [("X", (0.90, 0.15, 0.20)), ("X", (0.90, 0.15, 0.20)), ("0", (0.55, 0.55, 0.60)), ("OK", (0.10, 0.70, 0.35))]


def lerp(a, b, k):
    return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)


def pose_at(i, t):
    tl = TIMELINES[i]
    k = 0
    for j, (tt, _) in enumerate(tl):
        if t >= tt:
            k = j
    cur = POSES[tl[k][1]]
    prev = POSES[tl[k - 1][1]] if k > 0 else cur
    a = ease((t - tl[k][0]) / 0.35)
    p = {key: lerp(prev[key], cur[key], a) for key in cur}
    name = tl[k][1]
    ename = name if a > 0.5 else (tl[k - 1][1] if k > 0 else name)
    if name == "WRITE" and a >= 1:
        p["rh"] = (p["rh"][0] + 4 * math.sin(t * 38), p["rh"][1] + 2 * math.sin(t * 29))
        p["head"] = (p["head"][0], p["head"][1] + 1.5 * math.sin(t * 6))
    if name == "SCRATCH" and a >= 1:
        p["rh"] = (p["rh"][0] + 6 * math.sin(t * 22), p["rh"][1])
    if name == "THINK":
        p["head"] = (p["head"][0] + 2 * math.sin(t * 1.7), p["head"][1])
    if name == "CHEER" and a >= 1:
        p["rh"] = (p["rh"][0] + 5 * math.sin(t * 9), p["rh"][1])
    if name == "SLEEP":
        b = math.sin(t * 2.2)
        p["neck"] = (p["neck"][0], p["neck"][1] - 2 * b)
        p["head"] = (p["head"][0], p["head"][1] - 1.5 * b)
    p["neck"] = (p["neck"][0], p["neck"][1] + 0.8 * math.sin(t * 2 + i))
    return p, name, ename


# ----------------------------------------------------------------- cartoon kid
def head_center(p):
    dx, dy = p["head"][0] - p["neck"][0], p["head"][1] - p["neck"][1]
    d = math.hypot(dx, dy) or 1
    return (p["neck"][0] + dx / d * 36, p["neck"][1] + dy / d * 36)


def draw_hair(ctx, style, hx, hy, col):
    R = 30
    if style == "spiky":
        ctx.new_path()
        ctx.move_to(hx - R + 2, hy - 4)
        pts = [(-26, -30), (-16, -22), (-10, -44), (0, -28), (10, -46), (16, -26), (28, -36), (26, -12), (R - 1, -4)]
        for dx, dy in pts:
            ctx.line_to(hx + dx, hy + dy)
        ctx.arc_negative(hx, hy, R, -0.1, math.pi + 0.1)
        ctx.close_path()
        fill_outline(ctx, (0.40, 0.25, 0.12), 3.5)
    elif style == "cap":
        ctx.new_path()
        ctx.arc(hx, hy - 2, R + 1, math.pi, 2 * math.pi)
        ctx.close_path()
        fill_outline(ctx, tuple(c * 0.75 for c in col), 3.5)
        ctx.new_path()       # brim pointing backwards (cap worn the cool way)
        ctx.move_to(hx - R + 4, hy - 6)
        ctx.curve_to(hx - R - 16, hy - 8, hx - R - 22, hy - 2, hx - R - 20, hy + 2)
        ctx.line_to(hx - R + 6, hy + 1)
        ctx.close_path()
        fill_outline(ctx, tuple(c * 0.6 for c in col), 3)
        ctx.arc(hx + 2, hy - R + 2, 4, 0, 2 * math.pi)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()
    elif style == "messy":
        ctx.new_path()
        ctx.move_to(hx - R - 2, hy + 6)
        for k in range(9):
            a = math.pi + k * math.pi / 8
            rr = R + (10 if k % 2 else 3)
            ctx.line_to(hx + rr * math.cos(a), hy - 4 + rr * math.sin(a))
        ctx.line_to(hx + R + 2, hy + 2)
        ctx.arc_negative(hx, hy, R - 6, -0.1, math.pi + 0.1)
        ctx.close_path()
        fill_outline(ctx, (0.16, 0.12, 0.20), 3.5)
    else:  # neat side part
        ctx.new_path()
        ctx.arc(hx, hy - 2, R + 2, math.pi * 1.02, math.pi * 1.98)
        ctx.curve_to(hx + 20, hy - 20, hx - 6, hy - 24, hx - 30, hy - 8)
        ctx.close_path()
        fill_outline(ctx, (0.18, 0.12, 0.08), 3.5)


def draw_face(ctx, hx, hy, look, expr, glasses):
    (bin_, bout), mouth = expr
    lx, ly = look
    eyes = [(hx - 1, hy - 3), (hx + 15, hy - 3)]
    if mouth == "o" and look == (0, 0):  # sleeping: closed eyes
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(3)
        for ex, ey in eyes:
            ctx.new_path()
            ctx.arc(ex, ey, 6, 0.2, math.pi - 0.2)
            ctx.stroke()
    else:
        for ex, ey in eyes:
            ctx.new_path()
            ctx.arc(ex, ey, 7.5, 0, 2 * math.pi)
            ctx.set_source_rgb(1, 1, 1)
            ctx.fill_preserve()
            ctx.set_source_rgb(*INK)
            ctx.set_line_width(2.5)
            ctx.stroke()
            ctx.arc(ex + lx * 3, ey + ly * 3, 3.8, 0, 2 * math.pi)
            ctx.fill()
    # brows
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_width(3.5)
    for k, (ex, ey) in enumerate(eyes):
        inner = 1 if k == 0 else -1
        ctx.new_path()
        ctx.move_to(ex - 7 * inner, ey - 13 - bout)   # outer end
        ctx.line_to(ex + 7 * inner, ey - 13 - bin_)   # inner end (towards the other eye)
        ctx.set_source_rgb(*INK)
        ctx.stroke()
    if glasses:
        ctx.set_line_width(3)
        for ex, ey in eyes:
            ctx.new_path()
            ctx.arc(ex, ey, 10.5, 0, 2 * math.pi)
            ctx.stroke()
        ctx.new_path()
        ctx.move_to(eyes[0][0] + 10, eyes[0][1])
        ctx.line_to(eyes[1][0] - 10, eyes[1][1])
        ctx.stroke()
    # mouth
    mx, my = hx + 8, hy + 14
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(3)
    ctx.new_path()
    if mouth == "smile":
        ctx.arc(mx, my - 4, 8, 0.3, math.pi - 0.3)
        ctx.stroke()
    elif mouth == "grin":
        ctx.arc(mx, my - 4, 11, 0, math.pi)
        ctx.close_path()
        ctx.set_source_rgb(0.55, 0.12, 0.15)
        ctx.fill_preserve()
        ctx.set_source_rgb(*INK)
        ctx.stroke()
    elif mouth == "line":
        ctx.move_to(mx - 6, my)
        ctx.line_to(mx + 6, my)
        ctx.stroke()
    elif mouth == "side":
        ctx.move_to(mx - 2, my + 1)
        ctx.curve_to(mx + 4, my - 2, mx + 9, my - 2, mx + 12, my - 5)
        ctx.stroke()
    elif mouth == "smirk":
        ctx.move_to(mx - 8, my)
        ctx.curve_to(mx, my + 3, mx + 8, my, mx + 12, my - 6)
        ctx.stroke()
    elif mouth == "wavy":
        ctx.move_to(mx - 8, my)
        ctx.curve_to(mx - 4, my - 4, mx, my + 4, mx + 4, my)
        ctx.curve_to(mx + 6, my - 3, mx + 8, my - 2, mx + 10, my)
        ctx.stroke()
    elif mouth == "open":
        ctx.save()
        ctx.translate(mx, my)
        ctx.scale(6, 8)
        ctx.arc(0, 0, 1, 0, 2 * math.pi)
        ctx.restore()
        ctx.set_source_rgb(0.55, 0.12, 0.15)
        ctx.fill_preserve()
        ctx.set_source_rgb(*INK)
        ctx.stroke()
    elif mouth == "o":
        ctx.arc(mx, my, 4, 0, 2 * math.pi)
        ctx.stroke()
    elif mouth == "frown":
        ctx.arc(mx, my + 8, 8, math.pi + 0.4, 2 * math.pi - 0.4)
        ctx.stroke()
    # cheek blush
    ctx.new_path()
    ctx.arc(hx + 22, hy + 8, 5, 0, 2 * math.pi)
    ctx.set_source_rgba(1, 0.45, 0.45, 0.35)
    ctx.fill()


def draw_kid(ctx, i, p, ename):
    L = LANES[i]
    hood, skin = L["col"], L["skin"]
    pants = (0.25, 0.28, 0.40)
    # legs + shoes
    for knee, foot in (("rk", "rf"), ("lk", "lf")):
        limb(ctx, [p["hip"], p[knee], p[foot]], pants, 13)
        fx, fy = p[foot]
        ctx.new_path()
        ctx.save()
        ctx.translate(fx + 7, fy - 3)
        ctx.scale(13, 7)
        ctx.arc(0, 0, 1, 0, 2 * math.pi)
        ctx.restore()
        fill_outline(ctx, (0.95, 0.95, 0.97), 3)
    # torso (hoodie capsule)
    limb(ctx, [p["neck"], p["hip"]], hood, 34)
    return hood, skin


def draw_kid_upper(ctx, i, p, ename, hood, skin):
    L = LANES[i]
    # arms
    for el, ha in (("le", "lh"), ("re", "rh")):
        limb(ctx, [p["neck"], p[el], p[ha]], hood, 12)
        ctx.new_path()
        ctx.arc(p[ha][0], p[ha][1], 7, 0, 2 * math.pi)
        fill_outline(ctx, skin, 2.5)
    # pencil in the right hand
    hx_, hy_ = p["rh"]
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for lw, c in ((7, INK), (4, (1, 0.8, 0.2))):
        ctx.new_path()
        ctx.move_to(hx_ - 2, hy_ + 4)
        ctx.line_to(hx_ + 7, hy_ - 14)
        ctx.set_source_rgb(*c)
        ctx.set_line_width(lw)
        ctx.stroke()
    # head
    hx, hy = head_center(p)
    if L["hair"] == "messy":  # hood behind the head
        ctx.new_path()
        ctx.arc(hx - 4, hy + 4, 36, 0, 2 * math.pi)
        fill_outline(ctx, tuple(c * 0.8 for c in hood), 3.5)
    ctx.new_path()
    ctx.arc(hx - 27, hy + 2, 7, 0, 2 * math.pi)   # ear
    fill_outline(ctx, skin, 3)
    ctx.new_path()
    ctx.arc(hx, hy, 30, 0, 2 * math.pi)
    fill_outline(ctx, skin, 4)
    draw_hair(ctx, L["hair"], hx, hy, hood)
    draw_face(ctx, hx, hy, POSES[ename]["look"] if ename != "SLEEP" else (0, 0), EXPR[ename],
              glasses=L["hair"] == "neat")
    return hx, hy


# ----------------------------------------------------------------- lane drawing
def draw_lane(ctx, i, t):
    L = LANES[i]
    col = L["col"]
    paper_bg(ctx, 0, 0, W, LANE_H)
    # wobbly marker floor
    ctx.new_path()
    ctx.move_to(0, FLOOR)
    for x in range(0, W + 30, 30):
        ctx.line_to(x, FLOOR + 2 * math.sin(x * 0.05 + i))
    ctx.set_source_rgb(*col)
    ctx.set_line_width(6)
    ctx.stroke()
    ctx.rectangle(0, FLOOR + 3, W, LANE_H - FLOOR)
    ctx.set_source_rgba(*col, 0.18)
    ctx.fill()

    # chalkboard: the question, then the lane number at the end
    bx, by, bw, bh = 650, 115, 250, 125
    rrect(ctx, bx - 10, by - 10, bw + 20, bh + 20, 8)
    fill_outline(ctx, (0.62, 0.42, 0.25), 3)
    # tape label stuck on top of the board
    tw = text_w(ctx, L["name"], 32)
    lx0 = bx + bw / 2 - tw / 2
    ctx.save()
    ctx.translate(bx + bw / 2, 66)
    ctx.rotate(-0.03)
    ctx.rectangle(-tw / 2 - 14, -22, tw + 28, 44)
    ctx.set_source_rgba(*col, 0.9)
    ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.25)
    ctx.rectangle(-tw / 2 - 14, -22, tw + 28, 10)
    ctx.fill()
    ctx.restore()
    text(ctx, L["name"], lx0, 66, 32, INK, align="l")
    ctx.rectangle(bx, by, bw, bh)
    fill_outline(ctx, (0.14, 0.32, 0.24), 2)
    if t < END_T:
        text(ctx, "3 + 3 x 3 = ?", bx + bw / 2, by + bh / 2, 40, (0.95, 0.97, 0.93))
    else:
        s = ease_out_back((t - END_T - i * 0.12) / 0.35)
        pulse = 1 + 0.06 * math.sin(t * 6 + i)
        if s > 0:
            text(ctx, str(i + 1), bx + bw / 2, by + bh / 2 + 4, 120 * s * pulse, col,
                 stroke=(0.95, 0.97, 0.93), sw=6)

    # ---------- character group
    ctx.save()
    ctx.translate(GX, FLOOR)
    ctx.scale(GS, GS)
    ctx.translate(0, -FLOOR)
    p, pname, ename = pose_at(i, t)
    # chair
    ctx.new_path()
    rrect(ctx, 160, 170, 12, 70, 5)
    fill_outline(ctx, (0.55, 0.35, 0.22), 3)
    ctx.new_path()
    rrect(ctx, 160, 232, 62, 10, 4)
    fill_outline(ctx, (0.62, 0.40, 0.25), 3)
    for lx in (166, 212):
        ctx.new_path()
        ctx.rectangle(lx, 242, 6, FLOOR - 242)
        fill_outline(ctx, (0.50, 0.32, 0.20), 2.5)
    hood, skin = draw_kid(ctx, i, p, ename)
    # desk
    ctx.new_path()
    rrect(ctx, 248, 206, 148, 14, 4)
    fill_outline(ctx, (0.80, 0.55, 0.32), 3)
    for lx in (258, 380):
        ctx.new_path()
        ctx.rectangle(lx, 220, 8, FLOOR - 220)
        fill_outline(ctx, (0.62, 0.42, 0.25), 2.5)
    ctx.save()
    ctx.translate(296, 203)
    ctx.rotate(-0.05)
    ctx.rectangle(0, -3, 50, 5)
    fill_outline(ctx, (1, 1, 1), 1.5)
    ctx.restore()
    hx, hy = draw_kid_upper(ctx, i, p, ename, hood, skin)

    # ---- lane-specific props
    if i == 0 and 5.0 <= t < 6.0:
        s = ease_out_back((t - 5.0) / 0.3)
        text(ctx, "?", hx + 58, hy - 8, 60 * s, col, stroke=INK, sw=6)
    if i == 1:
        # peek at lane 1: everything stays inside this lane (visible top ~ y 70 here)
        ax, ay = hx + 58, 104
        if 9.6 <= t < 10.9:
            a = clamp((t - 9.6) / 0.2) * clamp((10.9 - t) / 0.2)
            bob = 4 * math.sin(t * 14)
            ctx.save()
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.move_to(ax, ay + 44 + bob)
            ctx.line_to(ax, ay + 4 + bob)
            ctx.move_to(ax - 12, ay + 16 + bob)
            ctx.line_to(ax, ay + 2 + bob)
            ctx.line_to(ax + 12, ay + 16 + bob)
            ctx.set_source_rgba(*INK, a)
            ctx.set_line_width(9)
            ctx.stroke_preserve()
            ctx.set_source_rgba(1, 0.7, 0.1, a)
            ctx.set_line_width(4)
            ctx.stroke()
            ctx.restore()
        if 10.0 <= t < 11.6:
            k = ease((t - 10.0) / 0.9)
            x = ax + 30 + (330 - ax - 30) * k
            y = ay + 10 + (120 - ay - 10) * k
            text(ctx, "18", x, y, 34 + 20 * k, (1, 0.7, 0.1), stroke=INK, sw=6,
                 alpha=clamp((t - 10.0) / 0.15) * clamp((11.75 - t) / 0.15))
    if i == 2:
        if 12.8 <= t < 14.0:
            for k, ch in enumerate("???"):
                s = ease_out_back((t - 12.8 - k * 0.2) / 0.3)
                if s > 0:
                    text(ctx, ch, hx + 50 + k * 28, hy - 10 - 5 * math.sin(t * 8 + k), 42 * s,
                         col, stroke=INK, sw=5)
        if 14.4 <= t < 15.3:
            k = (t - 14.4) / 0.9
            bx_, by_ = 280 + 420 * k, 200 - 220 * k + 300 * k * k
            ctx.new_path()
            ctx.arc(bx_, by_, 11, 0, 2 * math.pi)
            fill_outline(ctx, (1, 1, 1), 2.5)
        if t >= 15.0:
            for k in range(3):
                ph = ((t - 15.0) * 0.6 + k / 3) % 1.0
                text(ctx, "Z", hx - 30 - ph * 45, hy - 40 - ph * 45, 22 + 18 * ph, col,
                     stroke=INK, sw=4, alpha=math.sin(ph * math.pi))
    if i == 3:
        if 17.0 <= t < 19.9:
            s = ease_out_back((t - 17.0) / 0.35) * clamp((19.9 - t) / 0.2)
            ctx.save()
            ctx.translate(420, 116)
            ctx.scale(s, s)
            for cx, cy, r in ((-162, 28, 7), (-136, 14, 10)):
                ctx.new_path()
                ctx.arc(cx, cy, r, 0, 2 * math.pi)
                fill_outline(ctx, (1, 1, 1), 3)
            ctx.new_path()
            rrect(ctx, -110, -34, 220, 68, 30)
            fill_outline(ctx, (1, 1, 1), 4)
            ctx.restore()
            msg = "3 x 3 = 9" if t < 18.5 else "9 + 3 = 12"
            text(ctx, msg, 420, 118, 40 * s, INK)
        if 19.6 <= t < 20.9:
            a = clamp((t - 19.6) / 0.15) * clamp((20.9 - t) / 0.3)
            # beside the head (above it the lane edge clips the bulb)
            bx_, by_ = hx + 70, hy - 24
            g = cairo.RadialGradient(bx_, by_, 0, bx_, by_, 50)
            g.add_color_stop_rgba(0, 1, 0.95, 0.4, 0.7 * a)
            g.add_color_stop_rgba(1, 1, 0.95, 0.4, 0)
            ctx.set_source(g)
            ctx.arc(bx_, by_, 50, 0, 2 * math.pi)
            ctx.fill()
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            for r_ in range(7):
                ang = -math.pi + r_ * math.pi / 6
                ctx.move_to(bx_ + 24 * math.cos(ang), by_ + 24 * math.sin(ang))
                ctx.line_to(bx_ + 34 * math.cos(ang), by_ + 34 * math.sin(ang))
            ctx.set_source_rgba(1, 0.75, 0.1, a)
            ctx.set_line_width(4)
            ctx.stroke()
            ctx.new_path()
            ctx.arc(bx_, by_, 16, 0, 2 * math.pi)
            ctx.set_source_rgba(1, 0.9, 0.3, a)
            ctx.fill_preserve()
            ctx.set_source_rgba(*INK, a)
            ctx.set_line_width(3)
            ctx.stroke()
            ctx.rectangle(bx_ - 7, by_ + 14, 14, 10)
            ctx.set_source_rgba(0.6, 0.6, 0.65, a)
            ctx.fill()
        if STAMP_T[3] <= t < STAMP_T[3] + 2.5:
            rnd = random.Random(5)
            dt = t - STAMP_T[3]
            for _ in range(40):
                vx, vy = rnd.uniform(-420, 420), rnd.uniform(-520, -180)
                c = rnd.choice([(1, 0.7, 0.1), (0.15, 0.72, 0.42), (0.9, 0.2, 0.3), (0.2, 0.55, 0.95)])
                x, y = 330 + vx * dt, 110 + vy * dt + 700 * dt * dt
                ctx.rectangle(x, y, 9, 5)
                ctx.set_source_rgba(*c, clamp(2.5 - dt))
                ctx.fill()

    # ---- answer sheet + stamp
    ct, ctext = CARDS[i]
    if t >= ct:
        s = ease_out_back((t - ct) / 0.35)
        ctx.save()
        ctx.translate(330, 118)
        ctx.scale(s, s)
        ctx.rotate(-0.06 if i % 2 else 0.05)
        if t >= STAMP_T[i] and i == 3:
            g = cairo.RadialGradient(0, 0, 10, 0, 0, 110)
            g.add_color_stop_rgba(0, 1, 0.9, 0.3, 0.55)
            g.add_color_stop_rgba(1, 1, 0.9, 0.3, 0)
            ctx.set_source(g)
            ctx.arc(0, 0, 110, 0, 2 * math.pi)
            ctx.fill()
        ctx.new_path()
        ctx.rectangle(-40, -48, 80, 96)
        fill_outline(ctx, (1, 1, 1), 3.5)
        ctx.set_source_rgba(*RULE, 0.6)
        ctx.set_line_width(1.5)
        for ly in (-24, -8, 8, 24, 40):
            ctx.move_to(-34, ly)
            ctx.line_to(34, ly)
        ctx.stroke()
        ctx.rectangle(-20, -56, 40, 14)       # tape
        ctx.set_source_rgba(*col, 0.75)
        ctx.fill()
        ctx.restore()
        text(ctx, ctext, 330, 120, 54 * s, INK if ctext != "?" else (0.55, 0.55, 0.6))
        if t >= STAMP_T[i]:
            k = ease_out_back((t - STAMP_T[i]) / 0.3)
            sym, scol = STAMP[i]
            ctx.save()
            ctx.translate(330, 118)
            ctx.scale(1.6 - 0.6 * k, 1.6 - 0.6 * k)
            a = clamp((t - STAMP_T[i]) / 0.12)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.new_path()
            if sym == "X":
                ctx.move_to(-36, -36); ctx.line_to(36, 36)
                ctx.move_to(36, -36); ctx.line_to(-36, 36)
                w_ = 12
            elif sym == "OK":
                ctx.move_to(-34, 2); ctx.line_to(-8, 30); ctx.line_to(40, -34)
                w_ = 13
            else:
                ctx.arc(0, 0, 40, 0, 2 * math.pi)
                w_ = 9
            ctx.set_source_rgba(*scol, a)
            ctx.set_line_width(w_)
            ctx.stroke()
            ctx.restore()
    ctx.restore()  # end character group


# ----------------------------------------------------------------- camera + frame
def cam_state(t):
    def target(lane):
        if lane is None:
            return (1.0, OVERVIEW_C[0], OVERVIEW_C[1], -1)
        return (FOCUS_S, FOCUS_X, lane_top(lane) + 165, lane)
    k = 0
    for j, (tt, _) in enumerate(CAM):
        if t >= tt:
            k = j
    cur = target(CAM[k][1])
    prev = target(CAM[k - 1][1]) if k > 0 else cur
    a = ease((t - CAM[k][0]) / CAM_MOVE)
    s = prev[0] + (cur[0] - prev[0]) * a
    cx = prev[1] + (cur[1] - prev[1]) * a
    cy = prev[2] + (cur[2] - prev[2]) * a
    focus = cur[3]
    fa = a if focus >= 0 else (1 - a if prev[3] >= 0 else 0)
    flane = focus if focus >= 0 else prev[3]
    return s, cx, cy, flane, fa


def highlighter(ctx, cx, cy, w, h, col=(1, 0.92, 0.25), a=0.85):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(-0.02)
    ctx.new_path()
    ctx.move_to(-w / 2, -h / 2 + 4)
    ctx.line_to(w / 2, -h / 2)
    ctx.line_to(w / 2 - 6, h / 2)
    ctx.line_to(-w / 2 + 4, h / 2 - 3)
    ctx.close_path()
    ctx.set_source_rgba(*col, a)
    ctx.fill()
    ctx.restore()


LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "logo_round.png")
_LOGO = []


def brand_badge(ctx, x=18, y=12, d=124):
    """Channel logo (round), top-left: clear of the header text and the Shorts UI."""
    if not _LOGO:
        _LOGO.append(cairo.ImageSurface.create_from_png(LOGO_PATH))
    img = _LOGO[0]
    k = d / img.get_width()
    ctx.save()
    ctx.arc(x + d / 2, y + d / 2 + 3, d / 2 + 2, 0, 2 * math.pi)   # soft drop shadow
    ctx.set_source_rgba(0, 0, 0, 0.18)
    ctx.fill()
    ctx.translate(x, y)
    ctx.scale(k, k)
    ctx.set_source_surface(img, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_BEST)
    ctx.paint()
    ctx.restore()


def draw_frame(ctx, t):
    paper_bg(ctx, 0, 0, W, H)
    s, cx, cy, flane, fa = cam_state(t)
    ctx.save()
    ctx.translate(SCREEN_C[0], SCREEN_C[1] + (OVERVIEW_C[1] - SCREEN_C[1]) * (1 - min(1, (s - 1) / (FOCUS_S - 1))))
    ctx.scale(s, s)
    ctx.translate(-cx, -cy)
    for i in range(4):
        ctx.save()
        ctx.translate(0, lane_top(i))
        ctx.rectangle(0, 0, W, LANE_H)
        ctx.clip()
        draw_lane(ctx, i, t)
        if flane >= 0 and i != flane:
            ctx.rectangle(0, 0, W, LANE_H)
            ctx.set_source_rgba(*PAPER, 0.72 * fa)
            ctx.fill()
        ctx.restore()
        # pencil separator under each lane
        ctx.save()
        ctx.set_dash([14, 10])
        ctx.move_to(0, lane_top(i) + LANE_H + LANE_GAP / 2)
        ctx.line_to(W, lane_top(i) + LANE_H + LANE_GAP / 2)
        ctx.set_source_rgba(*INK, 0.35)
        ctx.set_line_width(2)
        ctx.stroke()
        ctx.restore()
    ctx.restore()

    # header on clean paper
    paper_bg(ctx, 0, 0, W, 285, margin=True)
    ctx.move_to(0, 285)
    ctx.line_to(W, 285)
    ctx.set_source_rgba(*INK, 0.5)
    ctx.set_line_width(3)
    ctx.stroke()
    if t < 22.3:
        pulse = 1 + 0.02 * math.sin(t * 4)
        highlighter(ctx, 540, 122, 700 * pulse, 110)
        ctx.save()
        ctx.translate(540, 120)
        ctx.scale(pulse, pulse)
        text(ctx, "3 + 3 x 3 = ?", 0, 0, 118, INK)
        ctx.restore()
        text(ctx, "4 DIMAAG, 1 SAWAAL", 540, 228, 52, (0.88, 0.20, 0.25))
    elif t < END_T:
        k = ease_out_back((t - 22.3) / 0.35)
        highlighter(ctx, 540, 122, 820 * k, 104, col=(0.55, 0.95, 0.60))
        text(ctx, "SAHI JAWAB = 12", 540, 120, 104 * k, INK)
        text(ctx, "PEHLE 3 x 3 = 9, PHIR 9 + 3", 540, 228, 48, (0.88, 0.20, 0.25),
             alpha=clamp((t - 22.5) / 0.3))
    else:
        k = ease_out_back((t - END_T) / 0.35)
        pulse = 1 + 0.03 * math.sin(t * 6)
        highlighter(ctx, 540, 122, 760 * k * pulse, 116)
        text(ctx, "TUM KAUN HO?", 540, 120, 122 * k * pulse, INK)
        text(ctx, "1, 2, 3 YA 4? COMMENT KARO", 540, 228, 52, (0.88, 0.20, 0.25),
             alpha=clamp((t - END_T - 0.2) / 0.3))
    brand_badge(ctx)


# ----------------------------------------------------------------- audio
SR = 44100


def tone(freqs, dur, decay, vol=1.0, harm=0.3):
    t = np.arange(int(SR * dur)) / SR
    s = sum(np.sin(2 * np.pi * f * t) + harm * np.sin(4 * np.pi * f * t) for f in freqs)
    return s * np.exp(-t * decay) * np.clip(t / 0.004, 0, 1) * vol / max(1, len(freqs))


def noise(dur, smooth=1, seed=0):
    x = np.random.RandomState(seed).uniform(-1, 1, int(SR * dur))
    if smooth > 1:
        x = np.convolve(x, np.ones(smooth) / smooth, mode="same")
    return x


BEAT_NO = 1   # phonk beat for this Short (user approved beat 1 for lanes_01)


def build_audio(path, music="phonk"):
    n = int(SR * DUR)
    mix = np.zeros(n)

    def put(sig, at, vol=1.0):
        i = int(at * SR)
        j = min(n, i + len(sig))
        if 0 <= i < n:
            mix[i:j] += sig[:j - i] * vol

    if music == "phonk":
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from phonk import phonk_bed
        # beat drops out as the answer is revealed, comes back for "TUM KAUN HO?"
        put(phonk_bed(DUR, beat_no=BEAT_NO, seed=2, breaks=[(22.3, END_T)], build=(19.6, 22.3)), 0, 0.5)
        _lane_sfx(put)
        _lane_finish(mix, path)
        return

    # playful pizzicato bed: C - Am - F - G, 104 bpm
    e = 60 / 104 / 2
    chords = [(261.63, 329.63, 392.0), (220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (196.0, 246.94, 293.66)]
    bass = [130.81, 110.0, 87.31, 98.0]
    pat = [0, 2, 1, 2, 0, 2, 1, 2]
    k, tt = 0, 0.0
    while tt < DUR - 0.3:
        bar = (k // 8) % 4
        put(tone([chords[bar][pat[k % 8]] * 2], 0.25, 14, 0.13, harm=0.4), tt)
        if k % 4 == 0:
            put(tone([bass[bar]], 0.6, 5, 0.25, harm=0.15), tt)
        if k % 4 == 2:
            put(noise(0.06, 1, k) * np.exp(-np.arange(int(SR * 0.06)) / SR * 70), tt, 0.05)
        tt += e
        k += 1
    _lane_sfx(put)
    _lane_finish(mix, path)


def _lane_sfx(put):
    for wt in (3.5, 8.0, 12.2, 16.4, 21.5):
        d = 0.5
        tt_ = np.arange(int(SR * d)) / SR
        put(noise(d, 40, int(wt * 10)) * np.sin(np.pi * tt_ / d), wt, 0.55)
    for a, b in ((5.9, 6.8), (10.9, 11.6), (20.0, 20.9)):
        d = b - a
        tt_ = np.arange(int(SR * d)) / SR
        put(noise(d, 6, int(a * 7)) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 7 * tt_))), a, 0.10)
    for ct, _ in CARDS:
        put(tone([880, 1320], 0.25, 18, 0.35), ct)
    put(tone([600], 0.35, 6, 0.25), 5.0)
    put(tone([300], 0.6, 5, 0.25), 14.0)
    put(tone([1568, 2093], 0.8, 5, 0.35), 19.6)
    tt_ = np.arange(int(SR * 0.35)) / SR
    buzz = np.sign(np.sin(2 * np.pi * 140 * tt_)) * np.exp(-tt_ * 7) * 0.22
    put(buzz, STAMP_T[0]); put(buzz, STAMP_T[1])
    put(tone([120], 0.3, 10, 0.4, harm=0.1), STAMP_T[2])
    for j, f in enumerate([1046.5, 1318.5, 1568.0, 2093.0]):
        put(tone([f], 0.9, 4, 0.4), STAMP_T[3] + j * 0.07)
    put(tone([784, 988, 1175], 1.2, 3, 0.3), END_T)


def _lane_finish(mix, path):
    fl = int(SR * 0.4)
    mix[-fl:] *= np.linspace(1, 0, fl)
    mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
    with wave.open(path, "w") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
        wf.writeframes((mix * 32767).astype(np.int16).tobytes())


# ----------------------------------------------------------------- main
def main():
    preview = "--preview" in sys.argv
    if "--audio-only" in sys.argv:   # swap the soundtrack of the already-rendered video
        wav = os.path.join(OUT, "audio.wav")
        build_audio(wav)
        mp4 = os.path.join(OUT, NAME + ".mp4")
        tmp = os.path.join(OUT, NAME + "_tmp.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-i", wav, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", tmp],
                       check=True)
        os.replace(tmp, mp4)
        print("done:", mp4)
        return
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    shots = [("p00_first", 0.0), ("p01_tukka", 7.2), ("p02_copy", 10.3), ("p03_giveup", 15.8),
             ("p04_thinker", 18.9), ("p05_result", 24.6), ("p06_end", 27.0)]
    for name, t in shots:
        draw_frame(ctx, t)
        surf.write_to_png(os.path.join(OUT, name + ".png"))
    draw_frame(ctx, 24.8)
    surf.write_to_png(os.path.join(OUT, "thumbnail.png"))
    if preview:
        print("previews in", OUT)
        return
    wav = os.path.join(OUT, "audio.wav")
    build_audio(wav)
    mp4 = os.path.join(OUT, NAME + ".mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "17",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", mp4]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    total = int(DUR * FPS)
    for f in range(total):
        draw_frame(ctx, f / FPS)
        surf.flush()
        proc.stdin.write(bytes(surf.get_data()))
        if f % 120 == 0:
            print(f"frame {f}/{total}", flush=True)
    proc.stdin.close()
    proc.wait()
    print("done:", mp4)


if __name__ == "__main__":
    main()
