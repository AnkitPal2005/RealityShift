"""Brain Blitz lanes_04 - "WHO REACHES SPACE?" BODMAS rocket launch (4 vertical space lanes).

Each rocket's sum = the altitude in KM it reaches. 10 KM = SPACE!
  1) 2 + 3 x 2  = 8   (left-to-right 10 -> THE TRAP: rockets ahead, stalls at 8 KM)
  2) 10 - 3 x 2 = 4   (left-to-right 14 -> fizzles at 4 KM)
  3) 6 - 3 x 2  = 0   (left-to-right 6  -> fails on the launchpad)
  4) 1 + 3 x 3  = 10  (left-to-right 12 -> blasts past everyone to 10 KM SPACE!)

Timeline: 0-6.0 countdown | 6.0-17.5 launch & staggered cutoffs |
          17.5-21.5 answer | 21.5-25.5 comment prompt | 25.5-26.5 loop fade.

Usage:  python core/lanes_04.py            -> output/lanes_04_en/lanes_04_en.mp4
        python core/lanes_04.py --preview  -> preview stills only
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
from lanes import clamp, ease, ease_out_back, text, rrect, fill_outline, INK  # noqa: E402

try:
    os.rmdir(ln.OUT)
except OSError:
    pass

NAME = "lanes_04_en"
OUT = os.path.join(ln.BASE, "output", NAME)
os.makedirs(OUT, exist_ok=True)
W, H, FPS, DUR = 1080, 1920, 30, 26.5
BEAT_NO = 7
STYLE = "dnb"          # 170+ bpm breakbeat + reese bass (beats.py)
SR = ln.SR
WHITE = (1, 1, 1)
RED = (0.88, 0.20, 0.25)

PICK_END, LAUNCH_END, ANS_T, PROMPT_T, LOOP_T = 6.0, 17.5, 17.5, 21.5, 25.5

# 4 vertical lanes layout
LANE_X = [24, 286, 548, 810]
LW = 246
PAD_Y = 1720           # launchpad deck y
SPACE_Y = 410          # 10 KM Space finish line y
TRAVEL = PAD_Y - 120 - SPACE_Y   # full 10 KM vertical distance

ROCKETS = [
    dict(q="2 + 3 x 2", ans=8, tag="8 KM!", col=(1.00, 0.56, 0.12), reveal=13.5,
         key=[(6.0, 0.0), (9.5, 0.42), (12.8, 0.80), (13.5, 0.80), (16.5, 0.76)]),
    dict(q="10 - 3 x 2", ans=4, tag="4 KM", col=(0.62, 0.38, 0.92), reveal=10.5,
         key=[(6.0, 0.0), (9.8, 0.40), (10.5, 0.40), (14.0, 0.37)]),
    dict(q="6 - 3 x 2", ans=0, tag="0 - BOOM!", col=(0.18, 0.58, 0.96), reveal=7.8,
         key=[(6.0, 0.0), (6.5, 0.02), (7.2, 0.0), (7.8, 0.0)]),
    dict(q="1 + 3 x 3", ans=10, tag="SPACE!", col=(0.95, 0.26, 0.46), reveal=16.5,
         key=[(6.0, 0.0), (10.5, 0.36), (13.5, 0.62), (16.5, 1.00), (17.5, 1.00)]),
]


def rocket_prog(i, t):
    """Return normalized altitude 0..1 at time t."""
    if t <= PICK_END:
        return 0.0
    pts = ROCKETS[i]["key"]
    if t >= pts[-1][0]:
        return pts[-1][1]
    for (t0, p0), (t1, p1) in zip(pts, pts[1:]):
        if t <= t1:
            return p0 + (p1 - p0) * ease((t - t0) / max(1e-4, t1 - t0))
    return pts[-1][1]


def hl(ctx, cx, cy, w, h, col=(1.0, 0.92, 0.28)):
    ctx.new_path()
    rrect(ctx, cx - w / 2, cy - h / 2, w, h, 24)
    fill_outline(ctx, col, 6)


# ----------------------------------------------------------------- scenery
def draw_sky(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0.00, 0.05, 0.06, 0.16)
    g.add_color_stop_rgb(0.28, 0.12, 0.14, 0.36)
    g.add_color_stop_rgb(0.62, 0.24, 0.42, 0.72)
    g.add_color_stop_rgb(1.00, 0.48, 0.76, 0.96)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()

    # Twinkling stars in upper space zone
    rnd = random.Random(404)
    for k in range(75):
        sx = rnd.uniform(15, W - 15)
        sy = rnd.uniform(260, 1050)
        r = rnd.uniform(1.8, 4.5)
        tw = 0.45 + 0.55 * abs(math.sin(t * 2.5 + k * 0.7))
        ctx.arc(sx, sy, r, 0, 2 * math.pi)
        ctx.set_source_rgba(1, 1, 0.92, tw * clamp(1.0 - (sy - 260) / 850))
        ctx.fill()

    # Glowing Moon + planets in space header zone
    ctx.save()
    ctx.arc(920, 330, 56, 0, 2 * math.pi)
    ctx.set_source_rgb(0.98, 0.95, 0.78)
    ctx.fill()
    for cx, cy, cr in [(902, 315, 11), (938, 342, 15), (915, 355, 8)]:
        ctx.arc(cx, cy, cr, 0, 2 * math.pi)
        ctx.set_source_rgba(0.84, 0.80, 0.62, 0.7)
        ctx.fill()
    ctx.restore()

    # Space finish line (10 KM)
    ctx.save()
    ctx.set_dash([18, 12])
    ctx.move_to(20, SPACE_Y)
    ctx.line_to(W - 20, SPACE_Y)
    ctx.set_source_rgba(0.35, 0.98, 0.62, 0.9)
    ctx.set_line_width(6)
    ctx.stroke()
    ctx.restore()

    # Finish line pill badge
    ctx.new_path()
    rrect(ctx, W / 2 - 140, SPACE_Y - 24, 280, 44, 22)
    fill_outline(ctx, (0.20, 0.86, 0.48), 4)
    text(ctx, "10 KM = SPACE!", W / 2, SPACE_Y - 2, 30, INK)

    # Distance markers (2, 4, 6, 8 KM)
    for km in (2, 4, 6, 8):
        my = PAD_Y - 120 - TRAVEL * (km / 10.0)
        ctx.move_to(20, my)
        ctx.line_to(W - 20, my)
        ctx.set_source_rgba(1, 1, 1, 0.16)
        ctx.set_line_width(2)
        ctx.stroke()
        text(ctx, f"{km} KM", 62, my - 16, 22, (1, 1, 1), alpha=0.55)

    # Soft clouds around lower sky
    for cx, cy, sc in [(160, 1460, 1.0), (540, 1360, 1.15), (920, 1490, 0.95)]:
        ctx.save()
        ctx.translate(cx + 12 * math.sin(t * 0.4 + cx), cy)
        ctx.scale(sc, sc)
        ctx.set_source_rgba(1, 1, 1, 0.30)
        for dx, dy, r in [(-45, 8, 34), (0, -8, 46), (48, 10, 32)]:
            ctx.arc(dx, dy, r, 0, 2 * math.pi)
            ctx.fill()
        ctx.restore()

    # Ground + Launchpad Deck
    ctx.rectangle(0, PAD_Y, W, H - PAD_Y)
    ctx.set_source_rgb(0.22, 0.25, 0.34)
    ctx.fill()
    ctx.rectangle(0, PAD_Y, W, 12)
    ctx.set_source_rgb(0.96, 0.78, 0.22)
    ctx.fill()


def draw_lane_bg(ctx, i, t):
    x0 = LANE_X[i]
    R = ROCKETS[i]
    # Subtle lane column guide
    ctx.new_path()
    rrect(ctx, x0, SPACE_Y - 10, LW, PAD_Y - SPACE_Y + 10, 18)
    ctx.set_source_rgba(1, 1, 1, 0.06)
    ctx.fill()

    # Launchpad platform + gantry tower
    px = x0 + LW / 2
    ctx.new_path()
    rrect(ctx, x0 + 26, PAD_Y - 18, LW - 52, 22, 8)
    fill_outline(ctx, (0.55, 0.58, 0.68), 4)

    # Gantry pole
    ctx.rectangle(x0 + 36, PAD_Y - 150, 12, 132)
    ctx.set_source_rgb(0.45, 0.48, 0.58)
    ctx.fill()

    # Lane number circle at bottom deck
    cy = PAD_Y + 62
    ctx.new_path()
    ctx.arc(px, cy, 40, 0, 2 * math.pi)
    fill_outline(ctx, R["col"], 5)
    text(ctx, str(i + 1), px, cy + 2, 48, WHITE, stroke=INK, sw=6)


def draw_rocket(ctx, i, t):
    R = ROCKETS[i]
    px = LANE_X[i] + LW / 2
    prog = rocket_prog(i, t)
    ry = PAD_Y - 18 - prog * TRAVEL  # base of rocket

    firing = (t >= PICK_END and t < R["reveal"])
    if i == 3 and t >= ANS_T:
        firing = False
    boom = (i == 2 and t >= 6.8 and t < 9.5)

    # Pre-launch steam or boom smoke on pad
    if t < PICK_END:
        for k in range(3):
            ph = (t * 1.4 + k * 0.33 + i * 0.2) % 1.0
            sx = px + math.sin(ph * 6 + i) * 26 * ph
            sy = PAD_Y - 18 - ph * 18
            ctx.arc(sx, sy, 10 + 18 * ph, 0, 2 * math.pi)
            ctx.set_source_rgba(1, 1, 1, 0.35 * (1 - ph))
            ctx.fill()

    if boom:
        d = t - 6.8
        for k in range(8):
            ang = k * math.pi / 4 + 0.3
            dist = 20 + 65 * clamp(d / 1.0)
            ctx.arc(px + math.cos(ang) * dist, PAD_Y - 60 + math.sin(ang) * dist * 0.6,
                    18 + 14 * clamp(d), 0, 2 * math.pi)
            ctx.set_source_rgba(0.25, 0.25, 0.30, 0.7 * clamp(1 - d / 2.6))
            ctx.fill()

    # Exhaust flame when flying
    if firing and i != 2:
        turbo = (i == 3 and t >= 13.5)
        flen = (115 if turbo else 78) + 22 * math.sin(t * 45 + i)
        ctx.save()
        ctx.translate(px, ry)
        ctx.move_to(-22, 0)
        ctx.line_to(0, flen)
        ctx.line_to(22, 0)
        ctx.close_path()
        ctx.set_source_rgb(1.0, 0.45, 0.08)
        ctx.fill()
        ctx.move_to(-12, 0)
        ctx.line_to(0, flen * 0.62)
        ctx.line_to(12, 0)
        ctx.close_path()
        ctx.set_source_rgb(1.0, 0.94, 0.35)
        ctx.fill()
        ctx.restore()

    # Vibration during launch
    jx = math.sin(t * 55 + i * 2) * (3.5 if firing else 0.0)
    if t < PICK_END and t > PICK_END - 1.5:
        jx = math.sin(t * 60) * 2.0

    ctx.save()
    ctx.translate(px + jx, ry)

    # Fins
    for sgn in (-1, 1):
        ctx.move_to(sgn * 26, -24)
        ctx.line_to(sgn * 48, 4)
        ctx.line_to(sgn * 24, -4)
        ctx.close_path()
        fill_outline(ctx, R["col"], 4)

    # Thruster nozzle
    ctx.new_path()
    rrect(ctx, -16, -8, 32, 14, 4)
    fill_outline(ctx, (0.35, 0.38, 0.48), 4)

    # Rocket body
    ctx.new_path()
    ctx.move_to(0, -148)
    ctx.curve_to(32, -108, 34, -45, 28, -6)
    ctx.line_to(-28, -6)
    ctx.curve_to(-34, -45, -32, -108, 0, -148)
    ctx.close_path()
    fill_outline(ctx, WHITE, 5)

    # Nose cone
    ctx.save()
    ctx.clip()
    ctx.rectangle(-40, -155, 80, 48)
    ctx.set_source_rgb(*R["col"])
    ctx.fill()
    ctx.restore()

    # Re-stroke body outline cleanly
    ctx.new_path()
    ctx.move_to(0, -148)
    ctx.curve_to(32, -108, 34, -45, 28, -6)
    ctx.line_to(-28, -6)
    ctx.curve_to(-34, -45, -32, -108, 0, -148)
    ctx.close_path()
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(5)
    ctx.stroke()

    # Window porthole
    ctx.new_path()
    ctx.arc(0, -68, 17, 0, 2 * math.pi)
    fill_outline(ctx, (0.45, 0.85, 1.0), 4)
    ctx.arc(-5, -73, 5, 0, 2 * math.pi)
    ctx.set_source_rgba(1, 1, 1, 0.85)
    ctx.fill()

    # Rocket number on lower body
    text(ctx, str(i + 1), 0, -28, 30, INK)

    # Winner crown/stars on Rocket 4 after reveal
    if i == 3 and t >= R["reveal"]:
        k = ease_out_back((t - R["reveal"]) / 0.4)
        for sgn in (-1, 1):
            ctx.save()
            ctx.translate(sgn * 58, -110)
            ctx.scale(k, k)
            ctx.arc(0, 0, 10, 0, 2 * math.pi)
            ctx.set_source_rgb(1.0, 0.90, 0.20)
            ctx.fill()
            ctx.restore()

    ctx.restore()

    # Math card above each pad (always visible at bottom or floating neatly)
    card_y = PAD_Y + 112
    ctx.new_path()
    rrect(ctx, LANE_X[i] + 8, card_y, LW - 16, 62, 14)
    fill_outline(ctx, WHITE, 4)
    show_ans = t >= R["reveal"]
    label = f"{R['q']} = {R['ans']}" if show_ans else R["q"]
    text(ctx, label, px, card_y + 32, 34 if show_ans else 38, INK)

    # Result pop tag right above rocket (or below Rocket 4 when at Space line)
    if show_ans:
        k = ease_out_back((t - R["reveal"]) / 0.3)
        ty = (ry + 52) if R["ans"] == 10 else max(SPACE_Y + 52, ry - 178)
        bg = (0.16, 0.78, 0.42) if R["ans"] == 10 else (RED if R["ans"] == 0 else (0.98, 0.82, 0.20))
        fg = WHITE if R["ans"] in (10, 0) else INK
        ctx.save()
        ctx.translate(px, ty)
        ctx.scale(k, k)
        ctx.new_path()
        rrect(ctx, -96, -26, 192, 52, 16)
        fill_outline(ctx, bg, 4)
        text(ctx, R["tag"], 0, 1, 34, fg)
        ctx.restore()


def header(ctx, t):
    if t < PICK_END:
        pulse = 1 + 0.02 * math.sin(t * 4)
        hl(ctx, 515, 112, 720 * pulse, 108)
        text(ctx, "WHO REACHES SPACE?", 515, 110, 76 * pulse, INK)
        text(ctx, "ANSWER = KM  |  10 = SPACE", 515, 222, 46, (1.0, 0.92, 0.35), stroke=INK, sw=6)
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
        text(ctx, "BODMAS / PEMDAS", 560, 110, 86, INK)
        text(ctx, "FIRST  x  THEN  +  -", 560, 222, 52, (1.0, 0.92, 0.35), stroke=INK, sw=6)
    elif t < PROMPT_T:
        k = ease_out_back((t - ANS_T) / 0.35)
        hl(ctx, 560, 112, 700 * k, 108, col=(0.55, 0.95, 0.60))
        text(ctx, "SPACE = ROCKET 4!", 560, 110, 82 * k, INK)
        text(ctx, "1 + 3 x 3 = 1 + 9 = 10", 560, 222, 52, WHITE, stroke=INK, sw=6,
             alpha=clamp((t - ANS_T - 0.3) / 0.3))
    else:
        k = ease_out_back((t - PROMPT_T) / 0.35)
        pulse = 1 + 0.03 * math.sin(t * 6)
        hl(ctx, 560, 112, 720 * k * pulse, 104)
        text(ctx, "WHO DID YOU PICK?", 560, 110, 86 * k * pulse, INK)
        text(ctx, "1, 2, 3 OR 4? COMMENT BELOW", 560, 222, 48, (1.0, 0.92, 0.35), stroke=INK, sw=6,
             alpha=clamp((t - PROMPT_T - 0.2) / 0.3))
    ln.brand_badge(ctx, x=26, y=20, d=110)


def draw_raw(ctx, t):
    draw_sky(ctx, t)
    for i in range(4):
        draw_lane_bg(ctx, i, t)
    for i in range(4):
        draw_rocket(ctx, i, t)
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
    bed = music_bed(DUR, style=STYLE, beat_no=BEAT_NO, seed=7,
                    breaks=[(13.3, 14.0), (17.3, 17.9)], build=(4.5, 6.0))
    put(bed, 0, 0.5)

    # Countdown ticks
    for k in range(6):
        put(tone([1200], 0.1, 30, 0.25), 0.05 + k)

    # Launch ignition rumble
    tt = np.arange(int(SR * 1.4)) / SR
    put(noise(1.4, 3, 11) * np.minimum(1, tt / 0.15) * np.exp(-tt * 1.4), PICK_END, 0.55)

    # Rocket 3 boom / buzzer (0 KM)
    tt = np.arange(int(SR * 0.45)) / SR
    put(noise(0.45, 4, 21) * np.exp(-tt * 8) * 0.45, 6.8)
    tt = np.arange(int(SR * 0.5)) / SR
    put(np.sign(np.sin(2 * np.pi * 115 * tt)) * np.exp(-tt * 6) * 0.22, ROCKETS[2]["reveal"])

    # Rocket 2 sputter (4 KM)
    put(tone([520, 390], 0.35, 8, 0.25), ROCKETS[1]["reveal"])

    # Rocket 1 trap sputter (8 KM - so close!)
    put(tone([660, 440], 0.4, 7, 0.28), ROCKETS[0]["reveal"])

    # Rocket 4 turbo boost + Space fanfare
    tt = np.arange(int(SR * 0.8)) / SR
    put(noise(0.8, 12, 33) * np.minimum(1, tt / 0.1) * np.exp(-tt * 2.2), 13.6, 0.45)
    for j, f in enumerate([1046.5, 1318.5, 1568.0, 2093.0]):
        put(tone([f], 0.75, 5, 0.32), ROCKETS[3]["reveal"] + j * 0.07)

    # Comment prompt chord
    put(tone([784, 988, 1175], 1.2, 3, 0.3), PROMPT_T)
    ln._lane_finish(mix, path)


# ----------------------------------------------------------------- main
def main():
    preview = "--preview" in sys.argv
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    shots = [
        ("p00_first", 0.0),
        ("p01_launch", 6.5),
        ("p02_boom", 8.0),
        ("p03_four", 10.8),
        ("p04_trap", 13.8),
        ("p05_space", 16.8),
        ("p06_answer", 18.5),
        ("p07_prompt", 22.5),
        ("p08_loop", 26.4),
    ]
    for name, t in shots:
        draw_frame(ctx, t)
        surf.write_to_png(os.path.join(OUT, name + ".png"))
    draw_frame(ctx, 2.5)
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
