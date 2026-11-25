"""Brain Blitz - Spot the Difference #2 v2 (cyber ramen bar), upgraded onto the spot_diff.py renderer.

Upgrade over the first cyber-ramen render (output/spot_diff_02_cyber_ramen):
  * spot_diff.py layout: frame 0 already shows the puzzle, big comment prompt, loop end, magnifier on the hard one.
  * Fair-but-harder differences (the old ones - RAMEN/TOKYO text, cyan/pink visor - were spotted instantly):
      1 EASY   : the right neon sign reads 12H instead of 24H
      2 MEDIUM : the lantern's RAMEN text is orange instead of yellow
      3 HARD   : one green scallion missing from the soup
  * No unverifiable "only 1%" claim in the header.
  * Music: the original pluck bed (phonk starts 27 Nov so the hook test stays clean).

Usage:  python core/spot_diff_02_v2.py            -> output/spot_diff_02_v2/spot_diff_02_v2.mp4
        python core/spot_diff_02_v2.py --preview  -> preview stills only
"""
import math
import os
import random
import sys

import cairo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spot_diff as sd  # noqa: E402

sd.NAME = "spot_diff_02_v2"
sd.OUT = os.path.join(sd.BASE, "output", sd.NAME)
os.makedirs(sd.OUT, exist_ok=True)
sd.BEAT_NO = 1
# (local x, local y, circle r, reveal time, label) on panel B
sd.DIFFS = [
    (855, 168, 70, 11.0, "EASY"),
    (312, 232, 62, 12.1, "MEDIUM"),
    (530, 500, 30, 13.2, "SABSE MUSHKIL!"),
]
sd.MAG_POS = (175, 520)   # empty counter, left of the bowl

lin, rrect, text_c, FONT = sd.lin, sd.rrect, sd.text_c, sd.FONT


def puzzle_header(ctx, t, alpha=1.0):
    pulse = 1 + 0.025 * math.sin(t * 5)
    text_c(ctx, "FIND 3 DIFFERENCES", sd.W / 2, 128, 92, (1, 0.88, 0.15), sw=12, scale=pulse, alpha=alpha)
    text_c(ctx, "TEESRA FARAK SABSE MUSHKIL", sd.W / 2, 205, 50, (1, 1, 1), sw=8, alpha=alpha)


def draw_scene(ctx, variant, t=0.0):
    """Cyber ramen bar, 960x640 local space (art from spot_diff_02.py; differences rebuilt)."""
    A = variant == "A"
    ctx.set_source(lin(ctx, 0, 0, 0, 420, [(0.0, (0.05, 0.04, 0.12)), (0.6, (0.08, 0.05, 0.18)),
                                           (1.0, (0.14, 0.08, 0.22))]))
    ctx.rectangle(0, 0, 960, 420)
    ctx.fill()
    rnd = random.Random(42)
    for bx in range(0, 960, 60):                                  # distant neon city
        bh = rnd.randint(120, 260)
        bw = rnd.randint(45, 75)
        ctx.set_source_rgb(0.03, 0.02, 0.07)
        ctx.rectangle(bx, 420 - bh, bw, bh)
        ctx.fill()
        ctx.set_source_rgba(0.0, 0.85, 1.0, 0.25)
        for wy in range(420 - bh + 20, 400, 30):
            for wx in range(bx + 8, bx + bw - 10, 15):
                if rnd.random() > 0.4:
                    ctx.rectangle(wx, wy, 8, 14)
                    ctx.fill()
    ctx.set_source(lin(ctx, 0, 0, 0, 90, [(0, (0.20, 0.12, 0.10)), (1, (0.10, 0.05, 0.04))]))
    ctx.rectangle(0, 0, 960, 80)
    ctx.fill()
    ctx.set_line_width(3)
    ctx.set_source_rgba(0.9, 0.3, 0.1, 0.4)
    for x in range(0, 960, 40):
        ctx.move_to(x, 0)
        ctx.line_to(x, 80)
        ctx.stroke()
    ctx.rectangle(0, 80, 960, 12)
    ctx.set_source_rgb(0.8, 0.25, 0.1)
    ctx.fill()
    ctx.set_source(lin(ctx, 0, 420, 0, 640, [(0, (0.35, 0.18, 0.10)), (1, (0.18, 0.09, 0.05))]))
    ctx.rectangle(0, 420, 960, 220)
    ctx.fill()
    ctx.set_source(lin(ctx, 0, 410, 0, 440, [(0, (0.55, 0.30, 0.18)), (1, (0.28, 0.14, 0.08))]))
    ctx.rectangle(0, 410, 960, 30)
    ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.15)
    ctx.rectangle(0, 412, 960, 4)
    ctx.fill()

    # red paper lantern (same in both)
    ctx.set_line_width(3)
    ctx.set_source_rgb(0.2, 0.2, 0.2)
    ctx.move_to(310, 92)
    ctx.line_to(310, 160)
    ctx.stroke()
    ctx.save()
    ctx.translate(310, 230)
    aura = cairo.RadialGradient(0, 0, 20, 0, 0, 130)
    aura.add_color_stop_rgba(0, 1.0, 0.2, 0.1, 0.35 + 0.05 * math.sin(t * 3))
    aura.add_color_stop_rgba(1, 1.0, 0.2, 0.1, 0.0)
    ctx.set_source(aura)
    ctx.arc(0, 0, 130, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source(lin(ctx, 0, -65, 0, 65, [(0, (1.0, 0.3, 0.2)), (0.5, (0.9, 0.1, 0.05)), (1, (0.6, 0.05, 0.02))]))
    ctx.scale(55, 75)
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.fill()
    ctx.restore()
    ctx.set_line_width(2)
    ctx.set_source_rgba(0, 0, 0, 0.4)
    for ly in [185, 210, 235, 260, 285]:
        ctx.move_to(270, ly)
        ctx.curve_to(310, ly + 8, 310, ly + 8, 350, ly)
        ctx.stroke()
    ctx.save()
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(36)
    ctx.set_source_rgb(1.0, 0.9, 0.2) if A else ctx.set_source_rgb(1.0, 0.55, 0.15)   # DIFFERENCE 2
    ctx.move_to(285, 242)
    ctx.show_text("RAMEN")
    ctx.restore()

    # cyber cat chef
    ctx.set_source(lin(ctx, 600, 320, 740, 480, [(0, (0.12, 0.15, 0.25)), (1, (0.05, 0.08, 0.15))]))
    ctx.arc(670, 420, 95, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source_rgb(0.92, 0.92, 0.95)
    ctx.arc(670, 440, 65, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source_rgb(1, 1, 1)
    ctx.arc(610, 440, 20, 0, 2 * math.pi)
    ctx.fill()
    ctx.arc(730, 440, 20, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source(lin(ctx, 620, 240, 720, 360, [(0, (0.95, 0.95, 0.98)), (1, (0.80, 0.82, 0.88))]))
    ctx.arc(670, 310, 75, 0, 2 * math.pi)
    ctx.fill()
    ctx.move_to(600, 270)
    ctx.line_to(585, 200)
    ctx.line_to(640, 250)
    ctx.close_path()
    ctx.fill()
    ctx.move_to(740, 270)
    ctx.line_to(755, 200)
    ctx.line_to(700, 250)
    ctx.close_path()
    ctx.fill()
    ctx.set_source_rgb(1.0, 0.6, 0.7)                                 # inner pink ears
    ctx.move_to(605, 265)
    ctx.line_to(595, 215)
    ctx.line_to(635, 250)
    ctx.close_path()
    ctx.fill()
    if True:
        ctx.move_to(735, 265)
        ctx.line_to(745, 215)
        ctx.line_to(705, 250)
        ctx.close_path()
        ctx.fill()
    ctx.save()                                                    # visor (same in both now)
    rrect(ctx, 615, 280, 110, 38, 12)
    ctx.set_source_rgb(0.0, 0.9, 1.0)
    ctx.fill_preserve()
    ctx.set_line_width(3)
    ctx.set_source_rgb(1, 1, 1)
    ctx.stroke()
    ctx.set_source_rgba(1, 1, 1, 0.7)
    ctx.rectangle(630, 285 + 1.5 * math.sin(t * 2), 45, 5)
    ctx.fill()
    ctx.restore()
    ctx.set_source_rgb(1.0, 0.4, 0.5)
    ctx.move_to(666, 332)
    ctx.line_to(674, 332)
    ctx.line_to(670, 338)
    ctx.close_path()
    ctx.fill()
    ctx.set_line_width(2.5)
    ctx.set_source_rgb(0.2, 0.2, 0.2)
    whiskers = [((610, 335), (550, 330)), ((610, 345), (555, 350)), ((730, 335), (790, 330))]
    if True:
        whiskers.append(((730, 345), (785, 350)))
    for (x0, y0), (x1, y1) in whiskers:
        ctx.move_to(x0, y0)
        ctx.line_to(x1, y1)
        ctx.stroke()

    # steaming ramen bowl (same in both)
    ctx.save()
    ctx.set_line_width(4)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgba(1, 1, 1, 0.35)
    for k, sx in enumerate([440, 480, 520]):
        wob = 6 * math.sin(t * 2 + k)
        ctx.move_to(sx, 440)
        ctx.curve_to(sx - 15 + wob, 410, sx + 20 - wob, 380, sx + wob, 350)
        ctx.stroke()
    ctx.restore()
    ctx.save()
    ctx.translate(480, 510)
    ctx.set_source(lin(ctx, -140, 0, 140, 90, [(0, (0.9, 0.15, 0.1)), (1, (0.5, 0.05, 0.05))]))
    ctx.move_to(-140, 0)
    ctx.curve_to(-130, 90, 130, 90, 140, 0)
    ctx.close_path()
    ctx.fill()
    ctx.set_line_width(5)
    ctx.set_source_rgb(1.0, 0.8, 0.1)
    ctx.move_to(-140, 0)
    ctx.curve_to(-130, 90, 130, 90, 140, 0)
    ctx.stroke()
    ctx.scale(136, 32)
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.set_source_rgb(0.95, 0.75, 0.25)
    ctx.fill()
    ctx.restore()
    ctx.set_line_width(4)
    ctx.set_source_rgb(1.0, 0.92, 0.55)
    for ny in [495, 505, 515]:
        ctx.move_to(400, ny)
        ctx.curve_to(440, ny - 6, 520, ny + 6, 560, ny)
        ctx.stroke()
    ctx.set_source_rgb(0.1, 0.75, 0.2)
    for gx, gy in [(430, 500), (450, 520), (510, 510), (470, 495)] + ([(530, 500)] if A else []):   # DIFFERENCE 3
        ctx.arc(gx, gy, 5, 0, 2 * math.pi)
        ctx.fill()
    ctx.set_source_rgb(1, 1, 1)                                   # naruto fishcake
    ctx.arc(480, 505, 22, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_line_width(4)
    ctx.set_source_rgb(1.0, 0.3, 0.6)
    ctx.arc(480, 505, 12, 0, 1.5 * math.pi)
    ctx.stroke()
    ctx.set_line_width(6)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgb(0.35, 0.18, 0.08)
    ctx.move_to(360, 490)
    ctx.line_to(580, 530)
    ctx.stroke()
    ctx.move_to(365, 498)
    ctx.line_to(585, 538)
    ctx.stroke()

    # neon signs: DIFFERENCE 1 = 24H vs 12H
    rrect(ctx, 40, 140, 130, 55, 10)
    ctx.set_source_rgba(0.08, 0.05, 0.15, 0.85)
    ctx.fill_preserve()
    ctx.set_line_width(3)
    ctx.set_source_rgb(0.0, 1.0, 0.4)
    ctx.stroke()
    text_c(ctx, "OPEN", 105, 168, 36, (0.0, 1.0, 0.4), sw=2)
    rrect(ctx, 790, 140, 130, 55, 10)
    ctx.set_source_rgba(0.08, 0.05, 0.15, 0.85)
    ctx.fill_preserve()
    ctx.set_line_width(3)
    ctx.set_source_rgb(1.0, 0.8, 0.0)
    ctx.stroke()
    text_c(ctx, "24H" if A else "12H", 855, 168, 36, (1.0, 0.8, 0.0), sw=2)


sd.draw_scene = draw_scene
sd.puzzle_header = puzzle_header

if __name__ == "__main__":
    sd.main()
