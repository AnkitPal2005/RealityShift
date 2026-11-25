"""Brain Blitz lanes_03 - "WHO HITS A SIX?" BODMAS cricket (2x2 grid, one ball per batsman).

Each batsman's sum = the runs off his ball.
  1) 2 + 1 x 2 = 4  FOUR   (left-to-right 6 -> the trap: he is sure it's a SIX)
  2) 9 - 4 x 2 = 1  1 RUN  (left-to-right 10)
  3) 1 + 1 x 5 = 6  SIX!   (left-to-right 10)  -> played last, the climax
  4) 5 - 5 x 1 = 0  OUT
Timeline: 0-6 pick (countdown) | balls: P1 6.0, P2 9.5, P4 13.0, P3 16.5 (3.5 s each) |
          20 answer | 23.5 comment prompt | 26.5-27.5 fades into frame 0 (loop).

Usage:  python core/lanes_03.py            -> output/lanes_03/lanes_03.mp4
        python core/lanes_03.py --preview  -> preview stills only
"""
import os
import sys
import math
import random
import subprocess

import numpy as np
import cairo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes as ln  # noqa: E402
from lanes import clamp, ease, ease_out_back, text, rrect, fill_outline, limb, INK  # noqa: E402

try:
    os.rmdir(ln.OUT)
except OSError:
    pass

NAME = "lanes_03_en"   # English (Brain Blitz = global since 25 Nov); Hinglish cut = lanes_03
OUT = os.path.join(ln.BASE, "output", NAME)
os.makedirs(OUT, exist_ok=True)
W, H, FPS, DUR = 1080, 1920, 30, 27.5
BEAT_NO = 6
STYLE = "house"        # four-on-the-floor stadium energy (beats.py)
SR = ln.SR
WHITE = (1, 1, 1)
RED = (0.88, 0.20, 0.25)

PICK_END, ANS_T, PROMPT_T, LOOP_T = 6.0, 20.0, 23.5, 26.5
PW, PH = 520, 680
POS = [(14, 300), (546, 300), (14, 996), (546, 996)]
BY = 630            # feet line inside a panel
BALL = 3.5
CHAR_S = 1.25

PANELS = [
    dict(q="2 + 1 x 2", ans=4, res="FOUR", col=(1.00, 0.62, 0.10), skin=(0.98, 0.80, 0.64), start=6.0,
         rcol=(0.15, 0.55, 0.95)),
    dict(q="9 - 4 x 2", ans=1, res="1 RUN", col=(0.62, 0.38, 0.90), skin=(0.86, 0.64, 0.47), start=9.5,
         rcol=(0.45, 0.45, 0.55)),
    dict(q="1 + 1 x 5", ans=6, res="SIX!", col=(0.95, 0.30, 0.45), skin=(0.80, 0.58, 0.42), start=16.5,
         rcol=(0.15, 0.72, 0.42)),
    dict(q="5 - 5 x 1", ans=0, res="OUT!", col=(0.20, 0.55, 0.95), skin=(0.94, 0.74, 0.58), start=13.0,
         rcol=RED),
]
RELEASE, BOUNCE, CONTACT, REVEAL = 0.8, 1.4, 1.7, 2.2   # local seconds inside a ball


def u_of(i, t):
    return t - PANELS[i]["start"]


# ----------------------------------------------------------------- scenery
def panel_bg(ctx, i, t):
    g = cairo.LinearGradient(0, 0, 0, 260)
    g.add_color_stop_rgb(0, 0.45, 0.72, 0.98)
    g.add_color_stop_rgb(1, 0.78, 0.90, 1.0)
    ctx.rectangle(0, 0, PW, 260)
    ctx.set_source(g)
    ctx.fill()
    # stands + crowd
    ctx.rectangle(0, 150, PW, 110)
    ctx.set_source_rgb(0.22, 0.24, 0.34)
    ctx.fill()
    rnd = random.Random(10 + i)
    cheer = 1 if (u_of(i, t) > REVEAL and PANELS[i]["ans"] in (4, 6)) else 0
    for row in range(3):
        for k in range(18):
            x = k * 30 + (row % 2) * 15 + 8
            y = 170 + row * 32 - cheer * 5 * abs(math.sin(t * 9 + k))
            ctx.arc(x, y, 10, 0, 2 * math.pi)
            ctx.set_source_rgb(*rnd.choice([(0.95, 0.75, 0.2), (0.9, 0.3, 0.3), (0.3, 0.6, 0.95),
                                            (0.95, 0.95, 0.95), (0.4, 0.8, 0.45)]))
            ctx.fill()
    # boundary rope + field
    g = cairo.LinearGradient(0, 260, 0, PH)
    g.add_color_stop_rgb(0, 0.40, 0.72, 0.36)
    g.add_color_stop_rgb(1, 0.30, 0.60, 0.28)
    ctx.rectangle(0, 260, PW, PH - 260)
    ctx.set_source(g)
    ctx.fill()
    ctx.rectangle(0, 258, PW, 6)
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()
    # pitch strip
    ctx.rectangle(0, BY - 30, PW, 70)
    ctx.set_source_rgb(0.82, 0.72, 0.50)
    ctx.fill()
    ctx.rectangle(60, BY - 30, 5, 70)
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()


def stumps(ctx, i, t):
    u = u_of(i, t)
    hit = PANELS[i]["ans"] == 0 and u >= 1.95
    k = clamp((u - 1.95) / 0.35) if hit else 0
    for j, sx in enumerate((84, 96, 108)):
        ctx.save()
        ctx.translate(sx, BY)
        ctx.rotate(-k * (0.9 + 0.3 * j))
        ctx.new_path()
        rrect(ctx, -3.5, -78, 7, 78, 3)
        fill_outline(ctx, (0.98, 0.92, 0.75), 2.5)
        ctx.restore()
    if hit:   # bails fly
        for j in range(2):
            d = u - 1.95
            x = 90 + j * 12 - 140 * d
            y = BY - 80 - 260 * d + 600 * d * d
            ctx.save()
            ctx.translate(x, y)
            ctx.rotate(d * 14 + j)
            ctx.new_path()
            rrect(ctx, -8, -3, 16, 6, 2)
            fill_outline(ctx, (0.98, 0.92, 0.75), 2)
            ctx.restore()
    else:
        ctx.new_path()
        rrect(ctx, 80, BY - 82, 32, 6, 2)
        fill_outline(ctx, (0.98, 0.92, 0.75), 2)


def bat_angle(i, u):
    """0 = bat hangs down, negative = back/up (backlift), positive = follow-through to the front."""
    res = PANELS[i]["ans"]
    stance = -0.35 + 0.08 * math.sin(u * 6)
    if u < 1.0:
        return stance
    lift_end = 1.5 if res != 0 else 1.62
    if u < lift_end:
        return stance + (-2.3 - stance) * ease((u - 1.0) / (lift_end - 1.0))
    swing = 0.35 if res != 0 else 0.38
    ft = {6: 2.6, 4: 1.7, 1: 0.5, 0: 1.4}[res]
    if u < lift_end + swing:
        return -2.3 + (ft + 2.3) * ease((u - lift_end) / swing)
    return ft


def batsman(ctx, i, t):
    P = PANELS[i]
    u = u_of(i, t)
    run = P["ans"] == 1 and u >= 2.0
    rk = clamp((u - 2.0) / 1.3) if run else 0
    bx = 150 + 190 * rk
    ph = rk * 2 * math.pi * 3.5 if run and rk < 1 else 0
    happy = u >= REVEAL and P["ans"] in (4, 6, 1)
    sad = u >= REVEAL and P["ans"] == 0
    hip = (bx, BY - 72 - (5 * abs(math.sin(ph)) if run else 0))
    sho = (bx + 6, hip[1] - 50)
    head = (bx + 12, sho[1] - 30)

    def leg(dx, phase, col):
        if run and rk < 1:
            a = 0.7 * math.sin(phase)
            knee = (hip[0] + 36 * math.sin(a), hip[1] + 36 * math.cos(a))
            b = a - 0.8 * (0.5 + 0.5 * math.cos(phase))
            foot = (knee[0] + 36 * math.sin(b), knee[1] + 36 * math.cos(b))
        else:
            knee = (hip[0] + dx * 0.6, hip[1] + 38)
            foot = (hip[0] + dx, BY - 4)
        limb(ctx, [hip, knee, foot], col, 17)
        ctx.new_path()
        rrect(ctx, foot[0] - 8, foot[1] - 5, 28, 12, 5)
        fill_outline(ctx, (0.95, 0.95, 0.95), 3)

    leg(-20, ph + math.pi, (0.92, 0.92, 0.95))     # white pads
    # bat + arms (one line from the shoulder)
    if run and rk < 1:
        phi = 0.6
    elif run:
        phi = -2.6       # raises the bat after taking the run
    else:
        phi = bat_angle(i, u)
    dirx, diry = math.sin(phi), math.cos(phi)
    hands = (sho[0] + 40 * dirx, sho[1] + 40 * diry)
    toe = (hands[0] + 92 * dirx, hands[1] + 92 * diry)
    ctx.save()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(*hands)
    ctx.line_to(hands[0] + 22 * dirx, hands[1] + 22 * diry)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(9)
    ctx.stroke()
    ctx.restore()
    ctx.save()
    ctx.translate(hands[0] + 22 * dirx, hands[1] + 22 * diry)
    ctx.rotate(-phi)
    ctx.new_path()
    rrect(ctx, -9, 0, 18, 72, 6)
    fill_outline(ctx, (0.93, 0.80, 0.55), 3)
    ctx.restore()
    _ = toe
    # torso
    ctx.save()
    ctx.translate(*hip)
    ctx.rotate(math.atan2(sho[0] - hip[0], hip[1] - sho[1]))
    ctx.new_path()
    rrect(ctx, -18, -58, 36, 64, 12)
    fill_outline(ctx, P["col"], 4)
    ctx.new_path()
    ctx.arc(0, -30, 12, 0, 2 * math.pi)
    fill_outline(ctx, WHITE, 2.5)
    text(ctx, str(i + 1), 0, -29, 18, INK)
    ctx.restore()
    leg(22, ph, (0.97, 0.97, 1.0))
    limb(ctx, [sho, ((sho[0] + hands[0]) / 2 + 6, (sho[1] + hands[1]) / 2 + 4), hands], P["skin"], 11)
    ctx.new_path()
    ctx.arc(hands[0], hands[1], 8, 0, 2 * math.pi)
    fill_outline(ctx, (0.95, 0.95, 0.95), 3)     # gloves
    # head + helmet
    hx, hy = head
    ctx.new_path()
    ctx.arc(hx, hy, 22, 0, 2 * math.pi)
    fill_outline(ctx, P["skin"], 4)
    ctx.new_path()
    ctx.arc(hx - 2, hy - 3, 24, math.pi * 0.95, math.pi * 2.05)
    ctx.close_path()
    fill_outline(ctx, tuple(c * 0.75 for c in P["col"]), 3.5)
    ctx.new_path()
    rrect(ctx, hx + 6, hy - 6, 30, 7, 3)
    fill_outline(ctx, tuple(c * 0.75 for c in P["col"]), 2.5)
    ctx.set_source_rgba(0.75, 0.75, 0.8, 0.9)        # face grill
    ctx.set_line_width(2.5)
    for gx in (hx + 18, hx + 26):
        ctx.move_to(gx, hy - 1)
        ctx.line_to(gx - 2, hy + 18)
    ctx.stroke()
    ctx.set_source_rgb(*INK)
    ctx.new_path()
    ctx.arc(hx + 9, hy + 2, 3.5, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_line_width(3)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.new_path()
    if happy:
        ctx.arc(hx + 8, hy + 9, 7, 0.2, math.pi - 0.2)
    elif sad or (i == 0 and u >= REVEAL):
        ctx.arc(hx + 8, hy + 18, 6, math.pi + 0.4, 2 * math.pi - 0.4)
    else:
        ctx.move_to(hx + 3, hy + 13)
        ctx.line_to(hx + 14, hy + 12)
    ctx.stroke()
    # trap: batsman 1 is sure it is a six
    if i == 0 and 0.2 <= u < 1.6:
        a = clamp((u - 0.2) / 0.2) * clamp((1.6 - u) / 0.15)
        bx_, by_ = hx + 70, hy - 50
        ctx.new_path()
        rrect(ctx, bx_ - 58, by_ - 26, 116, 52, 22)
        ctx.set_source_rgba(1, 1, 1, a)
        ctx.fill_preserve()
        ctx.set_source_rgba(*INK, a)
        ctx.set_line_width(3)
        ctx.stroke()
        text(ctx, "SIX!", bx_, by_ + 2, 40, P["col"], alpha=a)


def bowler(ctx, i, t):
    u = u_of(i, t)
    if u < -0.2 or u > 3.6:
        x, arm, ph = 440, 0.4, 0.0
    else:
        k = clamp(u / RELEASE)
        x = 450 - 40 * k
        ph = k * 2 * math.pi * 2
        arm = 0.4 + k * 2 * math.pi * 1.25 if u < RELEASE + 0.3 else 0.4 + 2 * math.pi * 1.25
    hip = (x, BY - 70)
    sho = (x - 4, hip[1] - 48)
    for phase, col in ((ph + math.pi, (0.85, 0.85, 0.9)), (ph, (0.97, 0.97, 1.0))):
        a = 0.6 * math.sin(phase) if 0 < u < RELEASE else 0.1
        knee = (hip[0] - 34 * math.sin(a), hip[1] + 34 * math.cos(a))
        foot = (knee[0] - 34 * math.sin(a - 0.4), BY - 4)
        limb(ctx, [hip, knee, foot], col, 12)
    ctx.save()
    ctx.translate(*hip)
    ctx.new_path()
    rrect(ctx, -16, -56, 32, 62, 12)
    fill_outline(ctx, (0.97, 0.97, 1.0), 4)
    ctx.restore()
    hand = (sho[0] + 42 * math.sin(arm + math.pi), sho[1] + 42 * math.cos(arm + math.pi))
    limb(ctx, [sho, hand], (0.86, 0.64, 0.47), 10)
    ctx.new_path()
    ctx.arc(x - 6, sho[1] - 26, 20, 0, 2 * math.pi)
    fill_outline(ctx, (0.86, 0.64, 0.47), 4)
    ctx.new_path()
    ctx.arc(x - 6, sho[1] - 30, 21, math.pi, 2 * math.pi)
    ctx.close_path()
    fill_outline(ctx, (0.1, 0.1, 0.12), 3)
    ctx.set_source_rgb(*INK)
    ctx.new_path()
    ctx.arc(x - 16, sho[1] - 24, 3, 0, 2 * math.pi)
    ctx.fill()


def ball_pos(i, u):
    res = PANELS[i]["ans"]
    rel, bnc, hit = (415, BY - 150), (265, BY - 8), (196, BY - 50)
    if u < RELEASE:
        return None
    if u < BOUNCE:
        k = (u - RELEASE) / (BOUNCE - RELEASE)
        return (rel[0] + (bnc[0] - rel[0]) * k, rel[1] + (bnc[1] - rel[1]) * k * k)
    if res == 0:          # misses the bat, hits the stumps
        k = (u - BOUNCE) / 0.55
        if k <= 1:
            return (bnc[0] + (100 - bnc[0]) * k, bnc[1] + (BY - 45 - bnc[1]) * math.sqrt(k))
        return (100 - 30 * min(1, k - 1), BY - 45 + 40 * min(1, k - 1))
    if u < CONTACT:
        k = (u - BOUNCE) / (CONTACT - BOUNCE)
        return (bnc[0] + (hit[0] - bnc[0]) * k, bnc[1] + (hit[1] - bnc[1]) * math.sqrt(k))
    d = u - CONTACT
    if res == 6:
        return (hit[0] + 250 * d, hit[1] - 900 * d + 380 * d * d)
    if res == 4:
        return (hit[0] - 600 * d, BY - 12 - 30 * abs(math.sin(d * 9)) * math.exp(-d * 3))
    return (hit[0] + 120 * (1 - math.exp(-d * 2.5)), BY - 10)      # 1 run: soft push


def draw_ball(ctx, i, t):
    u = u_of(i, t)
    if u < 0 or u > 3.4:
        return
    p = ball_pos(i, u)
    if p is None:
        return
    ctx.new_path()
    ctx.arc(p[0], p[1], 9, 0, 2 * math.pi)
    fill_outline(ctx, (0.85, 0.12, 0.15), 2.5)
    if PANELS[i]["ans"] == 6 and u > CONTACT:     # trail
        for k in range(1, 6):
            q = ball_pos(i, u - k * 0.03)
            ctx.arc(q[0], q[1], 9 - k, 0, 2 * math.pi)
            ctx.set_source_rgba(1, 0.85, 0.2, 0.5 - k * 0.08)
            ctx.fill()


def result(ctx, i, t):
    P = PANELS[i]
    u = u_of(i, t)
    if u < REVEAL:
        return
    s = ease_out_back((u - REVEAL) / 0.35)
    if P["ans"] == 6:     # fireworks
        rnd = random.Random(2)
        for b in range(3):
            cx, cy = 140 + b * 120, 120 + (b % 2) * 50
            d = u - REVEAL - b * 0.25
            if 0 < d < 1.6:
                for k in range(14):
                    ang = k * 2 * math.pi / 14
                    r = 90 * ease(d / 0.6)
                    ctx.arc(cx + r * math.cos(ang), cy + r * math.sin(ang) + 20 * d * d, 5, 0, 2 * math.pi)
                    c = rnd.choice([(1, 0.8, 0.2), (1, 0.35, 0.45), (0.4, 0.9, 1.0)])
                    ctx.set_source_rgba(*c, clamp(1.6 - d))
                    ctx.fill()
    ctx.save()
    ctx.translate(PW / 2 + 30, 345)
    ctx.rotate(-0.06)
    ctx.scale(s, s)
    text(ctx, P["res"], 0, 0, 104, P["rcol"], stroke=WHITE, sw=14)
    ctx.restore()


def sum_card(ctx, i, t):
    P = PANELS[i]
    u = u_of(i, t)
    win = P["ans"] == 6 and t >= ANS_T
    if win:
        ctx.rectangle(0, 0, PW, PH)
        ctx.set_source_rgba(1, 0.9, 0.3, 0.18 + 0.06 * math.sin(t * 6))
        ctx.fill()
    ctx.new_path()
    rrect(ctx, 14, 12, PW - 28, 82, 18)
    fill_outline(ctx, WHITE, 4)
    ctx.new_path()
    ctx.arc(56, 53, 30, 0, 2 * math.pi)
    fill_outline(ctx, P["col"], 4)
    text(ctx, str(i + 1), 56, 55, 44, WHITE, stroke=INK, sw=5)
    if u >= REVEAL:
        text(ctx, P["q"], 225, 55, 52, INK)
        k = ease_out_back((u - REVEAL) / 0.3)
        ctx.save()
        ctx.translate(430, 53)
        ctx.scale(k, k)
        ctx.new_path()
        rrect(ctx, -58, -34, 116, 68, 14)
        fill_outline(ctx, P["rcol"], 4)
        text(ctx, "= %d" % P["ans"], 0, 2, 50, WHITE, stroke=INK, sw=5)
        ctx.restore()
    else:
        text(ctx, P["q"] + " = ?", 285, 55, 52, INK)


# ----------------------------------------------------------------- frame
def active(t):
    for i, P in enumerate(PANELS):
        if P["start"] <= t < P["start"] + BALL:
            return i
    return -1


def header(ctx, t):
    ctx.new_path()
    rrect(ctx, 14, 10, W - 28, 274, 26)
    fill_outline(ctx, (0.99, 0.97, 0.90), 5)
    hl = ln.highlighter
    if t < PICK_END:
        pulse = 1 + 0.02 * math.sin(t * 4)
        hl(ctx, 520, 112, 660 * pulse, 108)
        text(ctx, "WHO HITS A SIX?", 520, 110, 96 * pulse, INK)
        text(ctx, "ANSWER = RUNS  |  6 = SIX", 520, 222, 50, RED)
        left = PICK_END - t
        cx, cy, r = 968, 145, 60
        ctx.new_path()
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
        fill_outline(ctx, WHITE, 5)
        ctx.new_path()
        ctx.arc(cx, cy, r - 10, -math.pi / 2, -math.pi / 2 + 2 * math.pi * left / PICK_END)
        ctx.set_source_rgb(*RED)
        ctx.set_line_width(12)
        ctx.stroke()
        text(ctx, str(min(6, max(1, math.ceil(left)))), cx, cy + 3, 62, INK)
    elif t < ANS_T:
        hl(ctx, 560, 112, 700, 104)
        text(ctx, "BODMAS / PEMDAS", 560, 110, 92, INK)
        text(ctx, "FIRST  x  THEN  +  -", 560, 222, 54, RED)
    elif t < PROMPT_T:
        k = ease_out_back((t - ANS_T) / 0.35)
        hl(ctx, 560, 112, 560 * k, 108, col=(0.55, 0.95, 0.60))
        text(ctx, "SIX = 3", 560, 110, 112 * k, INK)
        text(ctx, "1 + 1 x 5 = 1 + 5 = 6", 560, 222, 54, RED, alpha=clamp((t - ANS_T - 0.3) / 0.3))
    else:
        k = ease_out_back((t - PROMPT_T) / 0.35)
        pulse = 1 + 0.03 * math.sin(t * 6)
        hl(ctx, 560, 112, 720 * k * pulse, 104)
        text(ctx, "WHO DID YOU PICK?", 560, 110, 88 * k * pulse, INK)
        text(ctx, "1, 2, 3 OR 4? COMMENT BELOW", 560, 222, 52, RED, alpha=clamp((t - PROMPT_T - 0.2) / 0.3))
    ln.brand_badge(ctx, x=26, y=20, d=110)


def draw_raw(ctx, t):
    ctx.rectangle(0, 0, W, H)
    ctx.set_source_rgb(0.16, 0.18, 0.26)
    ctx.fill()
    act = active(t)
    for i in range(4):
        x0, y0 = POS[i]
        ctx.save()
        ctx.translate(x0, y0)
        ctx.new_path()
        rrect(ctx, 0, 0, PW, PH, 22)
        ctx.save()
        ctx.clip()
        panel_bg(ctx, i, t)
        ctx.save()                      # characters drawn 1.25x around the pitch
        ctx.translate(270, BY)
        ctx.scale(CHAR_S, CHAR_S)
        ctx.translate(-270, -BY)
        stumps(ctx, i, t)
        bowler(ctx, i, t)
        batsman(ctx, i, t)
        draw_ball(ctx, i, t)
        ctx.restore()
        result(ctx, i, t)
        sum_card(ctx, i, t)
        if act >= 0 and act != i:
            ctx.rectangle(0, 0, PW, PH)
            ctx.set_source_rgba(0.1, 0.1, 0.15, 0.45)
            ctx.fill()
        ctx.restore()
        ctx.new_path()
        rrect(ctx, 0, 0, PW, PH, 22)
        ctx.set_line_width(10 if act == i else 5)
        ctx.set_source_rgb(*((1, 0.85, 0.15) if act == i else INK))
        ctx.stroke()
        ctx.restore()
    header(ctx, t)


_FIRST = []


def draw_frame(ctx, t):
    draw_raw(ctx, t)
    if t >= LOOP_T:
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
    p6 = PANELS[2]["start"]
    bed = music_bed(DUR, style=STYLE, beat_no=BEAT_NO, seed=4, breaks=[(p6 + 0.6, p6 + REVEAL), (ANS_T - 0.1, ANS_T + 0.6)],
                    build=(p6 - 1.5, p6 + 0.6))
    put(bed, 0, 0.5)
    for k in range(6):
        put(tone([1200], 0.1, 30, 0.25), 0.05 + k)
    for i, P in enumerate(PANELS):
        s0 = P["start"]
        put(tone([700], 0.12, 25, 0.25), s0 + BOUNCE)                       # bounce
        if P["ans"] == 0:
            tt = np.arange(int(SR * 0.3)) / SR
            put(np.sin(2 * np.pi * 900 * tt) * np.exp(-tt * 25) * 0.4 + noise(0.3, 3, i) * np.exp(-tt * 30) * 0.3,
                s0 + 1.95)                                                   # stumps
            tt = np.arange(int(SR * 0.6)) / SR
            put(np.sign(np.sin(2 * np.pi * 120 * tt)) * np.exp(-tt * 5) * 0.2, s0 + REVEAL)   # buzzer
        else:
            tt = np.arange(int(SR * 0.15)) / SR
            put(noise(0.15, 2, i + 3) * np.exp(-tt * 40) * (0.7 if P["ans"] != 1 else 0.3), s0 + CONTACT)  # bat
            if P["ans"] in (4, 6):
                d = 1.8
                tt = np.arange(int(SR * d)) / SR
                put(noise(d, 25, 7 + i) * np.minimum(1, tt / 0.15) * np.exp(-tt * 1.3),
                    s0 + REVEAL - 0.1, 0.5 if P["ans"] == 6 else 0.3)       # crowd
            for j, f in enumerate([1046.5, 1318.5, 1568.0] + ([2093.0] if P["ans"] == 6 else [])):
                put(tone([f], 0.7, 5, 0.3), s0 + REVEAL + j * 0.07)
    put(tone([784, 988, 1175], 1.2, 3, 0.3), PROMPT_T)
    ln._lane_finish(mix, path)


# ----------------------------------------------------------------- main
def main():
    preview = "--preview" in sys.argv
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    shots = [("p00_first", 0.0), ("p01_trap", 7.2), ("p02_four", 8.6), ("p03_run", 12.4),
             ("p04_out", 15.4), ("p05_six_hit", 18.4), ("p06_six", 19.2), ("p07_answer", 21.5),
             ("p08_prompt", 25.0), ("p09_loop", 27.4)]
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
