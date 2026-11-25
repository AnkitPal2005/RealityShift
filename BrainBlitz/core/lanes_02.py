"""Brain Blitz lanes_02 - "WHO WINS?" BODMAS race (new look, same winning 4-lane + "1,2,3 ya 4?" idea).

4 runners on a stadium track, each lane has its own sum. Speed = BODMAS answer.
  1) 8 + 4 x 2  = 16   (left-to-right 24)
  2) 30 - 5 x 4 = 10   (left-to-right 100 -> the trap: sprints ahead, then falls)
  3) 6 x 3 + 2  = 20
  4) 7 + 7 x 2  = 21   (left-to-right 28) -> wins a photo finish over lane 3
Timeline: 0-6.5 think time (countdown) | 6.5-16 race + answers pop | 16 photo finish |
          17-21.5 answer | 21.5-25 comment prompt | 25-26 fades back into frame 0 (loop).

Usage:  python core/lanes_02.py            -> output/lanes_02/lanes_02.mp4
        python core/lanes_02.py --preview  -> preview stills only
"""
import os
import sys
import math
import random
import subprocess

import numpy as np
import cairo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes as ln  # noqa: E402  (shared helpers: text, rrect, limb, brand badge, audio bits)
from lanes import clamp, ease, ease_out_back, text, rrect, fill_outline, limb, INK  # noqa: E402

try:                       # importing lanes makes an empty output/lanes_01 folder
    os.rmdir(ln.OUT)
except OSError:
    pass

NAME = "lanes_02_en"   # English (Brain Blitz = global since 25 Nov); Hinglish cut = lanes_02
OUT = os.path.join(ln.BASE, "output", NAME)
os.makedirs(OUT, exist_ok=True)
W, H, FPS, DUR = 1080, 1920, 30, 26.0
BEAT_NO = 5
STYLE = "chiptune"     # 8-bit game feel (beats.py); every Short gets its own style/beat
SR = ln.SR

LANE_TOP, LANE_H, LANE_GAP = 308, 304, 14
START_X, FINISH_X = 95, 905
GO_T, END_RACE = 6.5, 16.0
ANS_T, PROMPT_T, LOOP_T = 17.0, 21.5, 25.0

GRASS = (0.36, 0.68, 0.33)
TRACK = (0.82, 0.38, 0.27)
WHITE = (1, 1, 1)
RED = (0.88, 0.20, 0.25)

LANES = [
    dict(q="8 + 4 x 2", ans=16, col=(1.00, 0.62, 0.10), skin=(0.98, 0.80, 0.64), hair="spiky",
         key=[(GO_T, 0), (END_RACE, 16 / 21)], reveal=9.0),
    dict(q="30 - 5 x 4", ans=10, col=(0.62, 0.38, 0.90), skin=(0.86, 0.64, 0.47), hair="cap",
         key=[(GO_T, 0), (10.5, 0.42), (11.7, 0.42), (END_RACE, 10 / 21)], reveal=10.5),
    dict(q="6 x 3 + 2", ans=20, col=(0.20, 0.55, 0.95), skin=(0.94, 0.74, 0.58), hair="pony",
         key=[(GO_T, 0), (10.5, 0.30), (12.0, 0.45), (14.5, 0.80), (END_RACE, 20 / 21)], reveal=12.0),
    dict(q="7 + 7 x 2", ans=21, col=(0.95, 0.30, 0.45), skin=(0.80, 0.58, 0.42), hair="neat",
         key=[(GO_T, 0), (10.5, 0.28), (12.0, 0.43), (14.5, 0.79), (END_RACE, 1.0)], reveal=13.5),
]
FALL = (10.5, 11.7)   # lane 2 trips when its real answer shows


def lane_top(i):
    return LANE_TOP + i * (LANE_H + LANE_GAP)


def progress(i, t):
    key = LANES[i]["key"]
    if t <= key[0][0]:
        return 0.0
    for (t0, p0), (t1, p1) in zip(key, key[1:]):
        if t <= t1:
            return p0 + (p1 - p0) * (t - t0) / (t1 - t0)
    return key[-1][1]


def run_phase(i, t):
    """Leg-cycle angle: tied to distance so feet never slide; idle bounce before GO."""
    return progress(i, t) * 2 * math.pi * 11


# ----------------------------------------------------------------- background
def stadium(ctx, t):
    g = cairo.LinearGradient(0, 290, 0, H)
    g.add_color_stop_rgb(0, 0.42, 0.74, 0.38)
    g.add_color_stop_rgb(1, 0.28, 0.58, 0.27)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()
    # mowing stripes
    for k in range(0, W, 90):
        ctx.rectangle(k, 290, 45, H)
        ctx.set_source_rgba(1, 1, 1, 0.04)
        ctx.fill()
    # crowd at the bottom (under the Shorts UI, just texture)
    rnd = random.Random(3)
    yb = lane_top(4) + 10
    ctx.rectangle(0, yb, W, H - yb)
    ctx.set_source_rgb(0.20, 0.22, 0.32)
    ctx.fill()
    for row in range(6):
        for k in range(28):
            x = k * 40 + (row % 2) * 20 + 10
            y = yb + 40 + row * 48 + 3 * math.sin(t * 7 + k + row) * (t > END_RACE)
            c = rnd.choice([(0.95, 0.75, 0.2), (0.9, 0.3, 0.3), (0.3, 0.6, 0.95), (0.95, 0.95, 0.95),
                            (0.4, 0.8, 0.45)])
            ctx.arc(x, y, 14, 0, 2 * math.pi)
            ctx.set_source_rgb(*c)
            ctx.fill()


def draw_lane_bg(ctx, i, t):
    y0 = lane_top(i)
    ty = y0 + 96
    ctx.rectangle(0, ty, W, LANE_H - 96)
    ctx.set_source_rgb(*TRACK)
    ctx.fill()
    for yy in (ty, y0 + LANE_H):
        ctx.rectangle(0, yy - 3, W, 6)
        ctx.set_source_rgb(*WHITE)
        ctx.fill()
    # start line
    ctx.rectangle(START_X - 30, ty, 8, LANE_H - 96)
    ctx.set_source_rgb(*WHITE)
    ctx.fill()
    # checkered finish
    sq = 16
    for r in range(int((LANE_H - 96) / sq) + 1):
        for c in range(2):
            ctx.rectangle(FINISH_X + 30 + c * sq, ty + r * sq, sq, min(sq, y0 + LANE_H - ty - r * sq))
            ctx.set_source_rgb(*((0.1, 0.1, 0.1) if (r + c) % 2 else WHITE))
            ctx.fill()
    # lane number painted on the track
    text(ctx, str(i + 1), 40, ty + 95, 70, (1, 1, 1), alpha=0.55)


def sum_card(ctx, i, t):
    L = LANES[i]
    y0 = lane_top(i) + 2
    win = i == 3 and t >= END_RACE + 0.4
    if win:
        g = cairo.RadialGradient(270, y0 + 46, 20, 270, y0 + 46, 300)
        g.add_color_stop_rgba(0, 1, 0.9, 0.3, 0.6)
        g.add_color_stop_rgba(1, 1, 0.9, 0.3, 0)
        ctx.set_source(g)
        ctx.rectangle(0, y0 - 12, W, 118)
        ctx.fill()
    ctx.new_path()
    rrect(ctx, 22, y0 + 4, 470, 84, 18)
    fill_outline(ctx, WHITE, 4)
    ctx.new_path()
    ctx.arc(70, y0 + 46, 34, 0, 2 * math.pi)
    fill_outline(ctx, L["col"], 4)
    text(ctx, str(i + 1), 70, y0 + 48, 50, WHITE, stroke=INK, sw=5)
    text(ctx, L["q"], 290, y0 + 48, 62, INK)
    # answer chip
    if t >= L["reveal"]:
        s = ease_out_back((t - L["reveal"]) / 0.35)
        ctx.save()
        ctx.translate(600, y0 + 46)
        ctx.scale(s, s)
        ctx.new_path()
        rrect(ctx, -78, -38, 156, 76, 16)
        fill_outline(ctx, (0.2, 0.75, 0.4) if win else L["col"], 4)
        text(ctx, "= %d" % L["ans"], 0, 2, 58, WHITE, stroke=INK, sw=6)
        ctx.restore()
        if i == 1:   # the trap: "100?" gets crossed out
            a = clamp((t - L["reveal"]) / 0.2)
            text(ctx, "100", 760, y0 + 48, 54, RED, alpha=a)
            ctx.set_source_rgba(*RED, a)
            ctx.set_line_width(8)
            ctx.move_to(712, y0 + 50)
            ctx.line_to(808, y0 + 46)
            ctx.stroke()


def winner_sticker(ctx, t):
    """Drawn after the runners so the winner's raised hand never covers it."""
    y0 = lane_top(3) + 2
    if t >= END_RACE + 0.4:
        s = ease_out_back((t - END_RACE - 0.4) / 0.4)
        ctx.save()
        ctx.translate(795, y0 + 46)
        ctx.rotate(0.08)
        ctx.scale(s, s)
        ctx.new_path()
        rrect(ctx, -110, -34, 220, 68, 12)
        fill_outline(ctx, (1, 0.82, 0.15), 4)
        text(ctx, "WINNER", 0, 2, 50, INK)
        ctx.restore()


# ----------------------------------------------------------------- runner
def runner(ctx, i, t):
    L = LANES[i]
    p = progress(i, t)
    x = START_X + p * (FINISH_X - START_X)
    yf = lane_top(i) + LANE_H - 12
    moving = GO_T <= t < END_RACE and not (i == 1 and FALL[0] <= t < FALL[1])
    if i == 1 and t >= FALL[1]:
        moving = t < END_RACE
    ph = run_phase(i, t) if moving else 0.0
    won = i == 3 and t >= END_RACE

    ctx.save()
    ctx.translate(x, yf)
    s = 1.1
    ctx.scale(s, s)
    # fall: tip forward and get back up
    if i == 1 and FALL[0] <= t < FALL[1]:
        k = (t - FALL[0]) / (FALL[1] - FALL[0])
        ang = 1.35 * math.sin(math.pi * min(1, k * 1.6)) if k < 0.62 else 1.35 * (1 - (k - 0.62) / 0.38)
        ctx.translate(20, 0)
        ctx.rotate(max(0, ang))
        ctx.translate(-20, 0)
    bob = -7 * abs(math.sin(ph)) if moving else (-3 * abs(math.sin(t * 5 + i)) if t < GO_T else 0)
    crouch = 10 if t < GO_T else 0
    hip = (0, -78 + crouch + bob)
    lean = 14 if moving else (10 if t < GO_T else 0)
    sho = (hip[0] + lean, hip[1] - 50)
    head = (sho[0] + lean * 0.5 + 4, sho[1] - 32)

    def leg(phase, col):
        a = 0.75 * math.sin(phase) if moving else (0.25 if t < GO_T else 0.08)
        knee = (hip[0] + 38 * math.sin(a), hip[1] + 38 * math.cos(a))
        b = a - (0.9 * (0.5 + 0.5 * math.cos(phase)) if moving else 0.25 * (t < GO_T))
        foot = (knee[0] + 38 * math.sin(b), knee[1] + 38 * math.cos(b))
        limb(ctx, [hip, knee, foot], col, 13)
        ctx.new_path()
        rrect(ctx, foot[0] - 6, foot[1] - 4, 26, 12, 5)
        fill_outline(ctx, (0.95, 0.95, 0.95), 3)

    def arm(phase, col):
        if won:
            el, hd = (sho[0] - 6 + 40 * phase, sho[1] - 30), (sho[0] - 4 + 52 * phase, sho[1] - 62)
        else:
            a = -0.8 * math.sin(phase) if moving else 0.3
            el = (sho[0] + 28 * math.sin(a), sho[1] + 28 * math.cos(a))
            hd = (el[0] + 26 * math.sin(a + 1.3), el[1] + 26 * math.cos(a + 1.3))
        limb(ctx, [sho, el, hd], col, 11)
        ctx.new_path()
        ctx.arc(hd[0], hd[1], 7, 0, 2 * math.pi)
        fill_outline(ctx, L["skin"], 3)

    dark = tuple(c * 0.7 for c in L["col"])
    skin_d = tuple(c * 0.85 for c in L["skin"])
    leg(ph + math.pi, (0.18, 0.2, 0.32))
    arm((ph + math.pi) if not won else -0.4, skin_d)
    # torso (jersey) + bib
    ctx.save()
    ctx.translate(*hip)
    ctx.rotate(math.atan2(sho[0] - hip[0], hip[1] - sho[1]))
    ctx.new_path()
    rrect(ctx, -17, -58, 34, 64, 12)
    fill_outline(ctx, L["col"], 4)
    ctx.new_path()
    ctx.arc(0, -28, 12, 0, 2 * math.pi)
    fill_outline(ctx, WHITE, 2.5)
    text(ctx, str(i + 1), 0, -27, 18, INK)
    ctx.restore()
    leg(ph, (0.25, 0.28, 0.42))
    arm(ph if not won else 0.4, L["skin"])
    # head
    hx, hy = head
    ctx.new_path()
    ctx.arc(hx, hy, 24, 0, 2 * math.pi)
    fill_outline(ctx, L["skin"], 4)
    hair(ctx, L["hair"], hx, hy, dark)
    # face (looks right)
    shocked = i == 1 and FALL[0] - 0.05 <= t < FALL[1] + 1.2
    sad = (not won) and t >= END_RACE + 0.3
    for ex in (hx + 4, hx + 15):
        ctx.new_path()
        ctx.arc(ex, hy - 3, 5 if shocked else 4, 0, 2 * math.pi)
        ctx.set_source_rgb(*WHITE)
        ctx.fill_preserve()
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(2)
        ctx.stroke()
        ctx.new_path()
        ctx.arc(ex + 1.5, hy - 3, 2, 0, 2 * math.pi)
        ctx.fill()
    ctx.set_line_width(3)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.new_path()
    if shocked:
        ctx.arc(hx + 12, hy + 11, 5, 0, 2 * math.pi)
        ctx.set_source_rgb(*INK)
        ctx.fill()
    elif won or (moving and i in (0, 1) and t < FALL[0]):
        ctx.arc(hx + 10, hy + 7, 8, 0.2, math.pi - 0.2)
        ctx.set_source_rgb(*INK)
        ctx.stroke()
    elif sad:
        ctx.arc(hx + 10, hy + 16, 7, math.pi + 0.4, 2 * math.pi - 0.4)
        ctx.set_source_rgb(*INK)
        ctx.stroke()
    else:
        ctx.move_to(hx + 4, hy + 11)
        ctx.line_to(hx + 17, hy + 10)
        ctx.set_source_rgb(*INK)
        ctx.stroke()
    ctx.restore()

    # lane 2 is sure it is 100 while it sprints ahead
    if i == 1 and 7.6 <= t < FALL[0]:
        a = clamp((t - 7.6) / 0.2) * clamp((FALL[0] - t) / 0.15)
        bx, by = x + 95, yf - 175
        ctx.new_path()
        rrect(ctx, bx - 72, by - 30, 144, 60, 26)
        ctx.set_source_rgba(1, 1, 1, a)
        ctx.fill_preserve()
        ctx.set_source_rgba(*INK, a)
        ctx.set_line_width(3)
        ctx.stroke()
        text(ctx, "100!", bx, by + 2, 44, (0.62, 0.38, 0.90), alpha=a)
    if i == 1 and FALL[0] <= t < FALL[1] + 0.6:   # dizzy stars
        for k in range(3):
            ang = t * 6 + k * 2.1
            text(ctx, "*", x + 60 + 34 * math.cos(ang), yf - 40 + 12 * math.sin(ang), 40, (1, 0.85, 0.1),
                 stroke=INK, sw=4)
    if 7.0 <= t < END_RACE and moving:   # speed lines
        for k in range(3):
            yy = yf - 60 - k * 26
            ctx.move_to(x - 40 - k * 8, yy)
            ctx.line_to(x - 80 - k * 8, yy)
        ctx.set_source_rgba(1, 1, 1, 0.7)
        ctx.set_line_width(4)
        ctx.stroke()


def hair(ctx, style, hx, hy, col):
    ctx.new_path()
    if style == "cap":
        ctx.arc(hx, hy - 4, 25, math.pi, 2 * math.pi)
        ctx.close_path()
        fill_outline(ctx, col, 3.5)
        ctx.new_path()
        rrect(ctx, hx + 4, hy - 9, 34, 9, 4)
        fill_outline(ctx, col, 3)
    elif style == "spiky":
        ctx.move_to(hx - 24, hy - 4)
        for k in range(6):
            ctx.line_to(hx - 22 + k * 8 + 4, hy - 38 + (k % 2) * 4)
            ctx.line_to(hx - 22 + k * 8 + 8, hy - 22)
        ctx.line_to(hx + 22, hy - 8)
        ctx.arc_negative(hx, hy, 23, -0.3, math.pi + 0.1)
        ctx.close_path()
        fill_outline(ctx, (0.15, 0.12, 0.1), 3)
    elif style == "pony":
        ctx.arc(hx - 4, hy - 6, 24, math.pi * 0.9, math.pi * 1.95)
        ctx.close_path()
        fill_outline(ctx, (0.2, 0.12, 0.08), 3)
        ctx.new_path()
        ctx.move_to(hx - 22, hy - 12)
        ctx.curve_to(hx - 52, hy - 14, hx - 50, hy + 14, hx - 34, hy + 24)
        ctx.curve_to(hx - 40, hy + 4, hx - 36, hy - 6, hx - 20, hy - 4)
        ctx.close_path()
        fill_outline(ctx, (0.2, 0.12, 0.08), 3)
    else:  # neat + headband
        ctx.arc(hx - 2, hy - 5, 24, math.pi * 0.95, math.pi * 2.0)
        ctx.close_path()
        fill_outline(ctx, (0.1, 0.08, 0.08), 3)
        ctx.new_path()
        rrect(ctx, hx - 25, hy - 14, 50, 8, 3)
        fill_outline(ctx, col, 2.5)


# ----------------------------------------------------------------- header
def header(ctx, t):
    ctx.new_path()
    rrect(ctx, 14, 10, W - 28, 270, 26)
    fill_outline(ctx, (0.99, 0.97, 0.90), 5)
    hl = ln.highlighter
    if t < GO_T:
        pulse = 1 + 0.02 * math.sin(t * 4)
        hl(ctx, 520, 112, 640 * pulse, 110)
        text(ctx, "WHO WINS?", 520, 110, 108 * pulse, INK)
        text(ctx, "BIGGER ANSWER = FASTER", 520, 222, 50, RED)
        # countdown ring
        left = GO_T - t
        cx, cy, r = 965, 145, 62
        ctx.new_path()
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
        fill_outline(ctx, WHITE, 5)
        ctx.new_path()
        ctx.arc(cx, cy, r - 10, -math.pi / 2, -math.pi / 2 + 2 * math.pi * left / GO_T)
        ctx.set_source_rgb(*RED)
        ctx.set_line_width(12)
        ctx.stroke()
        text(ctx, str(min(6, max(1, math.ceil(left - 0.5)))), cx, cy + 3, 64, INK)
    elif t < GO_T + 0.9:
        k = ease_out_back((t - GO_T) / 0.3)
        hl(ctx, 540, 140, 420 * k, 150, col=(0.55, 0.95, 0.60))
        text(ctx, "GO!", 540, 140, 170 * k, INK)
    elif t < END_RACE:
        hl(ctx, 540, 112, 700, 104)
        text(ctx, "BODMAS / PEMDAS", 540, 110, 96, INK)
        text(ctx, "FIRST  x  THEN  +  -", 540, 222, 54, RED)
    elif t < ANS_T:
        k = ease_out_back((t - END_RACE) / 0.3)
        hl(ctx, 540, 140, 760 * k, 140, col=(1, 0.85, 0.3))
        text(ctx, "PHOTO FINISH!", 540, 140, 120 * k, INK)
    elif t < PROMPT_T:
        k = ease_out_back((t - ANS_T) / 0.35)
        hl(ctx, 540, 112, 700 * k, 108, col=(0.55, 0.95, 0.60))
        text(ctx, "WINNER = 4", 540, 110, 110 * k, INK)
        text(ctx, "7 + 7 x 2 = 7 + 14 = 21", 540, 222, 54, RED, alpha=clamp((t - ANS_T - 0.3) / 0.3))
    else:
        k = ease_out_back((t - PROMPT_T) / 0.35)
        pulse = 1 + 0.03 * math.sin(t * 6)
        hl(ctx, 560, 112, 720 * k * pulse, 104)
        text(ctx, "WHO DID YOU PICK?", 560, 110, 88 * k * pulse, INK)
        text(ctx, "1, 2, 3 OR 4? COMMENT BELOW", 540, 222, 52, RED, alpha=clamp((t - PROMPT_T - 0.2) / 0.3))
    ln.brand_badge(ctx, x=26, y=20, d=110)


def draw_raw(ctx, t):
    stadium(ctx, t)
    for i in range(4):
        draw_lane_bg(ctx, i, t)
    for i in range(4):
        sum_card(ctx, i, t)
        runner(ctx, i, t)
    winner_sticker(ctx, t)
    # photo-finish flash
    if END_RACE <= t < END_RACE + 0.35:
        ctx.rectangle(0, 0, W, H)
        ctx.set_source_rgba(1, 1, 1, 0.85 * (1 - (t - END_RACE) / 0.35))
        ctx.fill()
    # confetti for the winner
    if END_RACE + 0.3 <= t < PROMPT_T + 1:
        rnd = random.Random(9)
        dt = t - END_RACE - 0.3
        for _ in range(70):
            vx, vy = rnd.uniform(-500, 300), rnd.uniform(-700, -250)
            c = rnd.choice([(1, 0.7, 0.1), (0.15, 0.72, 0.42), (0.9, 0.2, 0.3), (0.2, 0.55, 0.95)])
            x = FINISH_X - 60 + vx * dt
            y = lane_top(3) + 150 + vy * dt + 650 * dt * dt
            ctx.rectangle(x, y, 11, 6)
            ctx.set_source_rgba(*c, clamp(4.5 - dt))
            ctx.fill()
    header(ctx, t)


_FIRST = []


def draw_frame(ctx, t):
    draw_raw(ctx, t)
    if t >= LOOP_T:   # cross-fade into frame 0 so the end loops into the start
        if not _FIRST:
            s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
            draw_raw(cairo.Context(s), 0.0)
            _FIRST.append(s)
        ctx.set_source_surface(_FIRST[0], 0, 0)
        ctx.paint_with_alpha(ease((t - LOOP_T) / (DUR - LOOP_T - 0.15)))


# ----------------------------------------------------------------- audio
def build_audio(path):
    tone, noise = ln.tone, ln.noise
    n = int(SR * DUR)
    mix = np.zeros(n)

    def put(sig, at, vol=1.0):
        i = int(at * SR)
        j = min(n, i + len(sig))
        if 0 <= i < n:
            mix[i:j] += sig[:j - i] * vol

    from beats import music_bed
    bed = music_bed(DUR, style=STYLE, beat_no=BEAT_NO, seed=3, breaks=[(END_RACE, ANS_T)], build=(3.5, GO_T))
    put(bed, 0, 0.5)
    for k in range(6):                                   # countdown ticks
        put(tone([1200], 0.12, 30, 0.35), 0.5 + k)
    put(tone([1760, 2637], 0.5, 6, 0.4), GO_T)           # GO whistle
    tt = np.arange(int(SR * 0.4)) / SR
    put(np.sin(2 * np.pi * (90 - 60 * tt / 0.4) * tt) * np.exp(-tt * 9) * 0.5, FALL[0] + 0.25)   # thud
    for L in LANES:
        put(tone([880, 1320], 0.25, 18, 0.35), L["reveal"])
    put(tone([300, 240], 0.5, 6, 0.3), FALL[0] + 0.05)   # "oops"
    put(noise(0.08, 1, 4) * np.exp(-np.arange(int(SR * 0.08)) / SR * 50), END_RACE, 0.6)   # camera shutter
    d = 2.2
    tt = np.arange(int(SR * d)) / SR
    put(noise(d, 25, 7) * np.minimum(1, tt / 0.2) * np.exp(-tt * 1.2), END_RACE + 0.1, 0.45)   # crowd cheer
    for j, f in enumerate([1046.5, 1318.5, 1568.0, 2093.0]):
        put(tone([f], 0.9, 4, 0.4), ANS_T + j * 0.07)
    put(tone([784, 988, 1175], 1.2, 3, 0.3), PROMPT_T)
    ln._lane_finish(mix, path)


# ----------------------------------------------------------------- main
def main():
    preview = "--preview" in sys.argv
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    shots = [("p00_first", 0.0), ("p01_go", 6.7), ("p02_trap", 9.6), ("p03_fall", 11.0),
             ("p04_close", 15.2), ("p05_finish", 16.8), ("p06_answer", 19.0), ("p07_prompt", 23.0),
             ("p08_loop", 25.9)]
    for name, t in shots:
        draw_frame(ctx, t)
        surf.write_to_png(os.path.join(OUT, name + ".png"))
    draw_frame(ctx, 3.0)
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
        if f % 150 == 0:
            print(f"frame {f}/{total}", flush=True)
    proc.stdin.close()
    proc.wait()
    print("done:", mp4)


if __name__ == "__main__":
    main()
