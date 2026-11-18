"""Panchmukhi Hanuman Rahasya: Hanuman Ji Ne Panch Mukh Kyun Dhaaran Kiye? (~33s katha, 5 scenes).

Usage (from SanatanKatha/):
  python make.py panchmukhi --preview       # preview contact sheet & thumbnail
  python make.py panchmukhi --kiki-split    # splits the user's narrator voice into scene clips
  python make.py panchmukhi                 # final render with the user's voice, music and SFX

Rahasya:
During the Lanka war, Ahiravan (Mahiravan), the sorcerer-king of Patala and an ally of Ravana, cast a maya-sleep
on the camp and carried Shri Ram and Lakshman down to Patala to offer them to his Devi. His life was bound to five
lamps burning in five directions; only by putting all five out at the same instant could he be slain. Hanuman Ji
took the Panchmukhi form - Hanuman (east), Narasimha (south), Garuda (west), Varaha (north) and Hayagriva
(upward) - blew out all five lamps in one breath and slew Ahiravan, freeing Shri Ram and Lakshman.
"""

import math
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cairo

from core import katha
from core.katha import *  # noqa: F401,F403
import core.devta as dv
from core.devta import OUTLINE, group, place, halo, smooth, ink, ell, gem, limb, hand, sheen, eye, shade

TOPIC = "PANCHMUKHI HANUMAN AHIRAVAN PAATAAL RAHASYA"
OUTPUTS = {"edge": "panchmukhi_short.mp4"}
MUSIC_STYLE = "ambient"   # cinematic devotional pad, no shankh
MUSIC_BPM = 84
MUSIC_VOLUME = 0.11
TAIL_PAD = 0.04
MAX_GAP = 0.04

WHITE = (1.0, 1.0, 1.0)
RED_GEM = hexc("#D61F3A")
HANUMAN_ORANGE = hexc("#E05B16")
HANUMAN_FUR = hexc("#5A2008")
LAVA = hexc("#FF6A1A")
MAYA = hexc("#B05CFF")
ASURA_SKIN = hexc("#4B3C6E")
LAKSHMAN_SKIN = hexc("#E9B47E")

SOURCES = [
    "Ramayana folk retellings (Krittivasi Ramayana, Bengal; and regional Ramkathas): Ahiravan/Mahiravan, king of "
    "Patala, abducts Shri Ram and Lakshman during the Lanka war and Hanuman Ji rescues them from Patala.",
    "Panchmukha Hanuman tradition (Panchamukha Hanumat Kavacham, attributed to the Sudarshana Samhita): the five "
    "faces - Hanuman (east), Narasimha (south), Garuda (west), Varaha (north), Hayagriva (upward).",
    "Popular temple lore (Panchmukhi Hanuman temples, e.g. Rameswaram and Panchamukhi near Mantralayam): Ahiravan's "
    "life was held in five lamps in five directions, put out together by the Panchmukhi form.",
]


# -----------------------------------------------------------------------------
# Background: Paatal Lok (lava cavern under a blood-red orb)
# -----------------------------------------------------------------------------
def patala_bg(ctx, t, freed=0.0, rage=0.0):
    """Layered Patala cavern: red orb, stalactites, cave ridges, lava cracks, rising embers.
    freed 0..1 warms the cave into golden dawn light (CTA), rage 0..1 deepens the red glow."""
    dv.sky(ctx, hexc("#0A0410"), hexc("#2B0A24"), hexc("#5C1622"), 0.55)
    if freed > 0:
        g = cairo.LinearGradient(0, 0, 0, GROUND)
        g.add_color_stop_rgba(0, 0.30, 0.16, 0.05, 0.0)
        g.add_color_stop_rgba(1, 0.95, 0.62, 0.22, 0.55 * freed)
        ctx.rectangle(0, 0, W, GROUND)
        ctx.set_source(g)
        ctx.fill()

    # Glowing celestial orb of Patala
    orb = hexc("#FFD58A") if freed > 0.5 else hexc("#FF7A3C")
    glow(ctx, 540, 640, 470, orb, 0.32 + 0.18 * rage + 0.2 * freed)
    circle(ctx, 540, 640, 92, hexc("#FFE6B0") if freed > 0.5 else hexc("#FFB27A"), 0.7)
    circle(ctx, 540, 640, 70, hexc("#FFF4DC"), 0.35 + 0.3 * freed)

    # Distant cave ridges (three layers for depth)
    for base, amp, freq, ph, col in ((900, 70, 150, 0.4, "#3A1530"), (980, 55, 110, 1.7, "#26101F"),
                                     (1060, 40, 80, 2.9, "#170A14")):
        ctx.move_to(0, base)
        for x in range(0, W + 1, 30):
            ctx.line_to(x, base - amp * abs(math.sin(x / freq + ph)) - 18 * math.sin(x / 47 + ph))
        ctx.line_to(W, H)
        ctx.line_to(0, H)
        ctx.close_path()
        rgba(ctx, hexc(col))
        ctx.fill()

    # Stalactites hanging from the cavern roof
    rgba(ctx, hexc("#12060F"))
    ctx.move_to(0, 0)
    ctx.line_to(W, 0)
    ctx.line_to(W, 175)
    for i, x in enumerate(range(W, -1, -60)):
        depth = 175 + (120 if i % 3 == 0 else 55 if i % 2 else 85) + 20 * math.sin(i * 1.7)
        ctx.line_to(x - 30, depth)
        ctx.line_to(x - 60, 175)
    ctx.line_to(0, 175)
    ctx.close_path()
    ctx.fill()

    # Ground with glowing lava cracks
    ctx.rectangle(0, GROUND - 25, W, H)
    rgba(ctx, hexc("#160810"))
    ctx.fill()
    pulse = 0.55 + 0.25 * math.sin(t * 3.0)
    for k, (x0, x1, y0) in enumerate(((40, 330, GROUND - 5), (420, 640, GROUND + 25), (720, 1040, GROUND))):
        pts = [(x0 + (x1 - x0) * i / 6, y0 + 12 * math.sin(i * 2.1 + k)) for i in range(7)]
        line(ctx, pts, LAVA, 7, a=pulse * (1 - 0.6 * freed))
        line(ctx, pts, hexc("#FFD27A"), 2, a=pulse * (1 - 0.6 * freed))

    # Rising embers / spiritual dust
    for i in range(26):
        ex = (rnd(i, 3) * W + 30 * math.sin(t * 0.8 + i)) % W
        ey = GROUND - ((t * (40 + 30 * rnd(i, 5)) + rnd(i, 9) * 900) % 950)
        c = hexc("#FFE38A") if freed > 0.5 else LAVA
        circle(ctx, ex, ey, 2.5 + 2.5 * rnd(i, 7), c, 0.55)


# -----------------------------------------------------------------------------
# Props
# -----------------------------------------------------------------------------
def deepak(ctx, x, y, s, t, flame=1.0, smoke=-1.0, seed=0):
    """Clay diya of Ahiravan's life. flame 0..1 (0 = out); smoke = seconds since it went out (<0 = none)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if flame > 0.02:
        f = flame * (1 + 0.12 * math.sin(t * 13 + seed) + 0.06 * math.sin(t * 29 + seed))
        glow(ctx, 0, -55, 170, hexc("#FF8A3D"), 0.6 * flame)
        smooth(ctx, [(0, -40), (-15 * f, -64), (0, -40 - 75 * f), (15 * f, -64)])
        rgba(ctx, hexc("#FFB347"))
        ctx.fill()
        smooth(ctx, [(0, -44), (-7 * f, -60), (0, -44 - 42 * f), (7 * f, -60)])
        rgba(ctx, (1, 1, 0.9))
        ctx.fill()
    if smoke >= 0:
        for k in range(5):
            u = (smoke * 0.9 + k * 0.22)
            if u < 1.6:
                circle(ctx, 14 * math.sin(u * 4 + k), -50 - 120 * u, 10 + 16 * u, hexc("#B9AFC4"),
                       0.45 * max(0.0, 1 - u / 1.6))
    ctx.move_to(-70, -36)
    ctx.curve_to(-60, 22, 60, 22, 70, -36)
    ctx.close_path()
    ink(ctx, hexc("#B4532A"), 5)
    line(ctx, [(-58, -30), (58, -30)], GOLD, 4)
    ctx.restore()


def rope_bands(ctx, a=1.0):
    """Maya-bound ropes across arms and torso (local character frame)."""
    if a <= 0:
        return
    for yy in (-470, -415, -360):
        ctx.move_to(-150, yy + 6)
        ctx.curve_to(-60, yy + 22, 60, yy + 22, 150, yy + 6)
        ctx.set_line_width(16)
        rgba(ctx, hexc("#6B4423"), a)
        ctx.stroke()
        ctx.move_to(-150, yy + 6)
        ctx.curve_to(-60, yy + 22, 60, yy + 22, 150, yy + 6)
        ctx.set_line_width(4)
        rgba(ctx, MAYA, 0.8 * a)
        ctx.stroke()


# -----------------------------------------------------------------------------
# Characters
# -----------------------------------------------------------------------------
def strong_arm(ctx, pts, skin, w=44):
    """Muscular arm: round deltoid, bulging bicep on the upper arm, gold armlet (bajuband), forearm."""
    (x0, y0), (x1, y1), (x2, y2) = pts
    limb(ctx, pts, skin, w)
    ell(ctx, x0, y0 + 6, 40, 38)
    ink(ctx, skin)
    ang = math.atan2(y1 - y0, x1 - x0)
    mx, my = lerp(x0, x1, 0.55), lerp(y0, y1, 0.55)
    ell(ctx, mx, my, math.hypot(x1 - x0, y1 - y0) * 0.36, w * 0.66, rot=ang)
    ink(ctx, skin)
    sheen(ctx, mx - 6, my - 8, 16, 8, 0.2)
    bx, by = lerp(x0, x1, 0.2), lerp(y0, y1, 0.2)
    nx, ny = -math.sin(ang) * w * 0.55, math.cos(ang) * w * 0.55
    line(ctx, [(bx - nx, by - ny), (bx + nx, by + ny)], GOLD, 9)
    fx, fy = lerp(x1, x2, 0.45), lerp(y1, y2, 0.45)
    ell(ctx, fx, fy, math.hypot(x2 - x1, y2 - y1) * 0.32, w * 0.5, rot=math.atan2(y2 - y1, x2 - x1))
    ink(ctx, skin)


def gada(ctx, hx, hy, skin):
    """Hanuman Ji's golden gada held upright in a fist at (hx, hy): pommel, wrapped grip, shaft, ribbed head."""
    line(ctx, [(hx, hy + 55), (hx, hy - 150)], GOLD_DK, 20)
    line(ctx, [(hx, hy + 55), (hx, hy - 150)], GOLD_HI, 12)
    for k in range(4):
        line(ctx, [(hx - 10, hy - 60 - k * 22), (hx + 10, hy - 70 - k * 22)], GOLD_DK, 4)
    circle(ctx, hx, hy + 62, 14, GOLD)
    cy = hy - 210
    rrect(ctx, hx - 26, hy - 162, 52, 18, 6)
    ink(ctx, GOLD_DK, 3)
    ell(ctx, hx, cy, 58, 64)
    ink(ctx, GOLD, 5)
    for k in (-1, 0, 1):
        ctx.move_to(hx + k * 30, cy - 60 + abs(k) * 10)
        ctx.curve_to(hx + k * 46, cy - 20, hx + k * 46, cy + 20, hx + k * 30, cy + 60 - abs(k) * 10)
        ctx.set_line_width(4)
        rgba(ctx, GOLD_DK)
        ctx.stroke()
    sheen(ctx, hx - 20, cy - 24, 18, 12, 0.35)
    gem(ctx, hx, cy, 13, RED_GEM)
    smooth(ctx, [(hx - 14, cy - 60), (hx, cy - 104), (hx + 14, cy - 60)])
    ink(ctx, GOLD_HI, 4)
    hand(ctx, hx, hy, skin, 26)


def hanuman(ctx, x, y, s, t, pose="namaste", mouth="smile", look=(0.0, 0.0), flip=False, a=1.0, aura=True):
    """Pawanputra Hanuman: sindoori skin, golden mukut and gada. Poses: namaste, gada, think, abhaya."""
    def draw():
        place(ctx, x, y, s, t, flip)
        if aura:
            halo(ctx, 0, -620, 185, t, c=GOLD)
        skin = HANUMAN_ORANGE

        # Tail
        limb(ctx, [(-50, -310), (-140, -360), (-180, -480), (-160, -620), (-90, -700), (-40, -720)], skin, 28)
        circle(ctx, -40, -720, 16, skin)
        # Fur behind shoulders
        for side in (-1, 1):
            smooth(ctx, [(side * 60, -660), (side * 115, -590), (side * 125, -520), (side * 110, -460),
                         (side * 80, -470), (side * 75, -540)])
            ink(ctx, HANUMAN_FUR)
        ell(ctx, 0, -638, 108, 106)
        ink(ctx, HANUMAN_FUR)
        # Feet
        for fx in (-52, 52):
            ell(ctx, fx, -14, 46, 20)
            ink(ctx, skin)
            line(ctx, [(fx - 26, -30), (fx, -24), (fx + 26, -30)], GOLD, 7)
        # Dhoti
        smooth(ctx, [(-110, -330), (110, -330), (128, -200), (142, -50), (60, -36), (0, -60), (-60, -36),
                     (-142, -50), (-128, -200)])
        ink(ctx, GOLD)
        line(ctx, [(140, -52), (60, -38), (0, -62), (-60, -38), (-140, -52)], hexc("#E8741E"), 10)
        # Torso
        smooth(ctx, [(-158, -492), (-70, -518), (70, -518), (158, -492), (150, -430), (112, -380), (100, -332),
                     (-100, -332), (-112, -380), (-150, -430)])
        ink(ctx, skin)
        mus = shade(skin, 0.72)
        for side in (-1, 1):   # pecs
            ctx.move_to(side * 6, -488)
            ctx.curve_to(side * 40, -430, side * 105, -425, side * 128, -462)
            ctx.set_line_width(5)
            rgba(ctx, mus)
            ctx.stroke()
            sheen(ctx, side * 62, -470, 34, 18, 0.16)
        line(ctx, [(0, -480), (0, -360)], mus, 4)
        for yy in (-418, -390, -362):   # abs
            for side in (-1, 1):
                line(ctx, [(side * 10, yy), (side * 40, yy - 3)], mus, 4)
        for side in (-1, 1):   # obliques
            line(ctx, [(side * 92, -430), (side * 72, -350)], mus, 4)
        line(ctx, [(-120, -500), (-60, -455), (20, -390), (92, -334)], WHITE, 4)
        line(ctx, [(-70, -510), (-35, -478), (0, -466), (35, -478), (70, -510)], GOLD, 7)
        gem(ctx, 0, -460, 10, RED_GEM)
        rrect(ctx, -112, -350, 224, 30, 10)
        ink(ctx, GOLD, 5)
        gem(ctx, 0, -335, 8, RED_GEM)
        # Head
        rrect(ctx, -34, -546, 68, 60, 14)
        ink(ctx, skin)
        for side in (-1, 1):
            ell(ctx, side * 96, -616, 20, 26)
            ink(ctx, skin)
            circle(ctx, side * 102, -586, 12, GOLD)
        ell(ctx, 0, -616, 96, 102)
        ink(ctx, skin)
        smooth(ctx, [(-42, -580), (42, -580), (36, -538), (0, -528), (-36, -538)])
        ink(ctx, hexc("#F4803A"))
        line(ctx, [(0, -690), (0, -650)], hexc("#E2231A"), 8)
        line(ctx, [(-6, -684), (-6, -656)], GOLD_HI, 3)
        line(ctx, [(6, -684), (6, -656)], GOLD_HI, 3)
        for side in (-1, 1):
            eye(ctx, side * 36, -624, 23, 26, t, look=look, iris=hexc("#3B1808"), seed=1)
            brow_in = -662 if pose == "gada" else -652
            line(ctx, [(side * 14, brow_in), (side * 36, -660), (side * 60, -654)], HANUMAN_FUR, 6)
        if mouth == "blow":
            ell(ctx, 0, -552, 12, 14)
            ink(ctx, hexc("#5A0E0A"), 3)
        elif mouth == "worry":
            ctx.move_to(-16, -548)
            ctx.curve_to(-6, -556, 6, -556, 16, -548)
            ctx.set_line_width(4)
            rgba(ctx, hexc("#8A1810"))
            ctx.stroke()
        else:
            ctx.move_to(-18, -554)
            ctx.curve_to(-6, -546, 6, -546, 18, -554)
            ctx.set_line_width(4)
            rgba(ctx, hexc("#8A1810"))
            ctx.stroke()
        smooth(ctx, [(-76, -698), (-56, -788), (0, -840), (56, -788), (76, -698), (0, -710)])
        ink(ctx, GOLD, 5)
        gem(ctx, 0, -770, 12, RED_GEM)

        # Arms (deltoids + biceps; the gada is gripped in a fist)
        if pose == "gada":
            strong_arm(ctx, [(140, -480), (215, -400), (205, -305)], skin)
            gada(ctx, 205, -305, skin)
            strong_arm(ctx, [(-140, -480), (-185, -410), (-160, -325)], skin)
            dv.palm(ctx, -160, -315, skin, ang=0.1, s=1.1)
        elif pose == "abhaya":
            strong_arm(ctx, [(140, -480), (190, -420), (172, -322)], skin)
            dv.palm(ctx, 172, -312, skin, ang=-0.1, s=1.15)
            strong_arm(ctx, [(-140, -480), (-215, -400), (-205, -305)], skin)
            gada(ctx, -205, -305, skin)
        elif pose == "think":
            sc = 6 * math.sin(t * 9)
            strong_arm(ctx, [(140, -480), (215, -575), (112 + sc, -690)], skin)
            hand(ctx, 112 + sc, -690, skin, 24)
            strong_arm(ctx, [(-140, -480), (-215, -400), (-205, -305)], skin)
            gada(ctx, -205, -305, skin)
        else:  # namaste
            strong_arm(ctx, [(-140, -480), (-80, -430), (-25, -430)], skin)
            strong_arm(ctx, [(140, -480), (80, -430), (25, -430)], skin)
            circle(ctx, -26, -430, 16, GOLD)
            circle(ctx, 26, -430, 16, GOLD)
            smooth(ctx, [(-20, -450), (0, -470), (20, -450), (12, -420), (-12, -420)])
            ink(ctx, skin)
        ctx.restore()
    group(ctx, a, draw)


def _mini_mukut(ctx, cx, top, w):
    smooth(ctx, [(cx - w, top), (cx - w * 0.72, top - 46), (cx, top - 74), (cx + w * 0.72, top - 46),
                 (cx + w, top), (cx, top - 10)])
    ink(ctx, GOLD, 4)
    gem(ctx, cx, top - 36, 8, RED_GEM)


def _fierce_eyes(ctx, cx, cy, t, iris, dx=24, r=13, seed=3):
    for side in (-1, 1):
        eye(ctx, cx + side * dx, cy, r, r + 2, t, iris=iris, seed=seed, lash=False)
        line(ctx, [(cx + side * (dx - 16), cy - r - 2), (cx + side * (dx + 14), cy - r - 12)], OUTLINE, 5)


def narasimha_head(ctx, cx, cy, t):
    pts = []
    for k in range(32):
        ang = k * math.tau / 32
        rr = 100 if k % 2 == 0 else 78
        pts.append((cx + rr * math.cos(ang), cy + 6 + rr * math.sin(ang)))
    smooth(ctx, pts, k=0.08)
    ink(ctx, hexc("#C2410C"))
    ell(ctx, cx, cy + 4, 62, 66)
    ink(ctx, hexc("#F5A524"))
    _fierce_eyes(ctx, cx, cy - 12, t, hexc("#7A0A0A"))
    ell(ctx, cx, cy + 14, 22, 15)
    ink(ctx, hexc("#7C2D12"), 3)
    ell(ctx, cx, cy + 44, 30, 15)
    rgba(ctx, hexc("#4A0808"))
    ctx.fill()
    for side in (-1, 1):
        ctx.move_to(cx + side * 20, cy + 34)
        ctx.line_to(cx + side * 12, cy + 34)
        ctx.line_to(cx + side * 16, cy + 50)
        ctx.close_path()
        rgba(ctx, WHITE)
        ctx.fill()
    _mini_mukut(ctx, cx, cy - 62, 46)


def garuda_head(ctx, cx, cy, t):
    for k, dxx in enumerate((-30, 0, 30)):
        smooth(ctx, [(cx + dxx - 12, cy - 50), (cx + dxx * 1.6, cy - 120 - 10 * (k == 1)), (cx + dxx + 12, cy - 50)])
        ink(ctx, hexc("#1B5E20"), 4)
    ell(ctx, cx, cy, 60, 64)
    ink(ctx, hexc("#2E7D32"))
    sheen(ctx, cx - 18, cy - 24, 22, 14, 0.2)
    _fierce_eyes(ctx, cx, cy - 14, t, hexc("#F2B829"), dx=26, r=12)
    smooth(ctx, [(cx - 18, cy + 2), (cx + 18, cy + 2), (cx + 12, cy + 36), (cx, cy + 62), (cx - 10, cy + 40)])
    ink(ctx, hexc("#F59E0B"), 4)
    _mini_mukut(ctx, cx, cy - 58, 42)


def varaha_head(ctx, cx, cy, t):
    for side in (-1, 1):
        smooth(ctx, [(cx + side * 30, cy - 50), (cx + side * 70, cy - 92), (cx + side * 64, cy - 30)])
        ink(ctx, hexc("#455A64"), 4)
    ell(ctx, cx, cy, 62, 60)
    ink(ctx, hexc("#546E7A"))
    _fierce_eyes(ctx, cx, cy - 18, t, hexc("#3B1808"), dx=26, r=11)
    ell(ctx, cx, cy + 34, 36, 26)
    ink(ctx, hexc("#78909C"))
    for side in (-1, 1):
        circle(ctx, cx + side * 12, cy + 36, 6, hexc("#263238"))
        ctx.move_to(cx + side * 30, cy + 46)
        ctx.curve_to(cx + side * 46, cy + 40, cx + side * 52, cy + 22, cx + side * 46, cy + 6)
        ctx.set_line_width(7)
        rgba(ctx, WHITE)
        ctx.stroke()
    _mini_mukut(ctx, cx, cy - 56, 44)


def hayagriva_head(ctx, cx, cy, t):
    for side in (-1, 1):
        smooth(ctx, [(cx + side * 18, cy - 54), (cx + side * 34, cy - 104), (cx + side * 42, cy - 46)])
        ink(ctx, hexc("#CFD8DC"), 4)
    for k in range(5):
        smooth(ctx, [(cx - 52, cy - 40 + k * 22), (cx - 82, cy - 26 + k * 22), (cx - 50, cy - 18 + k * 22)])
        ink(ctx, hexc("#7E8CA0"), 3)
    ell(ctx, cx, cy - 6, 50, 62)
    ink(ctx, hexc("#ECEFF1"))
    ell(ctx, cx, cy + 48, 36, 30)
    ink(ctx, hexc("#E0E4E8"))
    for side in (-1, 1):
        circle(ctx, cx + side * 13, cy + 56, 5, hexc("#455A64"))
    _fierce_eyes(ctx, cx, cy - 18, t, hexc("#1A237E"), dx=24, r=11)
    _mini_mukut(ctx, cx, cy - 62, 40)


PANCH = [("varaha", -170, -840), ("hayagriva", 170, -840), ("garuda", -225, -665), ("narasimha", 225, -665)]
HEADS = {"narasimha": narasimha_head, "garuda": garuda_head, "varaha": varaha_head, "hayagriva": hayagriva_head}


def panch_heads(ctx, x, y, s, t, a=1.0, flip=False):
    """The four extra divine faces behind Hanuman Ji's own face (draw before hanuman())."""
    def draw():
        place(ctx, x, y, s, t, flip)
        glow(ctx, 0, -680, 380, GOLD_HI, 0.35)
        halo(ctx, 0, -690, 300, t, c=GOLD)
        for name, hx, hy in PANCH:
            HEADS[name](ctx, hx, hy, t)
        ctx.restore()
    group(ctx, a, draw)


def panchmukhi(ctx, x, y, s, t, heads=1.0, pose="gada", mouth="smile"):
    panch_heads(ctx, x, y, s, t, a=heads)
    hanuman(ctx, x, y, s, t, pose=pose, mouth=mouth, aura=heads < 0.5)


def raghu(ctx, x, y, s, t, who="ram", pose="bound", rope=1.0, flip=False, a=1.0):
    """Shri Ram (blue, tall royal mukut, saffron) or Lakshman (fair, smaller mukut, maroon). No peacock feather.
    pose bound = maya-sleep, eyes closed, ropes; bless / namaste = freed, Kodanda bow on the shoulder."""
    ram = who == "ram"

    def draw():
        place(ctx, x, y, s, t, flip)
        skin = dv.KRISHNA_SKIN if ram else LAKSHMAN_SKIN
        hair = dv.KRISHNA_HAIR
        robe = dv.SAFFRON if ram else hexc("#9F1239")
        if pose == "bound":
            glow(ctx, 0, -450, 260, MAYA, 0.35)
        else:
            halo(ctx, 0, -650, 165 if ram else 140, t, c=GOLD_HI)
        for side in (-1, 1):
            smooth(ctx, [(side * 70, -700), (side * 122, -620), (side * 138, -540), (side * 128, -470),
                         (side * 98, -480), (side * 88, -560)])
            ink(ctx, hair)
        ell(ctx, 0, -668, 116, 112)
        ink(ctx, hair)
        for fx in (-50, 50):
            ell(ctx, fx, -14, 44, 18)
            ink(ctx, skin)
            line(ctx, [(fx - 26, -30), (fx, -24), (fx + 26, -30)], GOLD, 7)
        smooth(ctx, [(-118, -345), (118, -345), (136, -200), (152, -44), (62, -32), (0, -64), (-62, -32),
                     (-152, -44), (-136, -200)])
        ink(ctx, robe)
        line(ctx, [(150, -48), (62, -36), (0, -68), (-62, -36), (-150, -48)], GOLD, 10)
        smooth(ctx, [(-122, -500), (-60, -522), (60, -522), (122, -500), (128, -430), (100, -340), (-100, -340),
                     (-128, -430)])
        ink(ctx, skin)
        smooth(ctx, [(-128, -505), (-88, -520), (118, -372), (96, -342)], k=0.1)
        ink(ctx, hexc("#E0502A") if ram else hexc("#F2B829"), 5)
        rrect(ctx, -114, -366, 228, 34, 12)
        ink(ctx, GOLD, 5)
        line(ctx, [(-66, -516), (-30, -486), (0, -478), (30, -486), (66, -516)], GOLD, 8)
        gem(ctx, 0, -470, 10, RED_GEM)
        rrect(ctx, -32, -566, 64, 64, 14)
        ink(ctx, skin)
        for side in (-1, 1):
            ell(ctx, side * 98, -640, 18, 28)
            ink(ctx, skin)
            circle(ctx, side * 104, -604, 13, GOLD)
        ell(ctx, 0, -640, 100, 110)
        ink(ctx, skin)
        sheen(ctx, -36, -690, 40, 26, 0.14)
        for side in (-1, 1):
            eye(ctx, side * 38, -646, 25, 29, t, iris=hexc("#2A1810"), seed=2 if ram else 4,
                closed=(pose == "bound"))
            line(ctx, [(side * 14, -686), (side * 38, -697), (side * 64, -688)], hair, 7)
        line(ctx, [(2, -640), (-6, -618), (5, -613)], shade(skin, 0.65), 4)
        ctx.move_to(-20, -594)
        ctx.curve_to(-8, -586, 8, -586, 20, -594)
        ctx.set_line_width(4)
        rgba(ctx, hexc("#B5283C"))
        ctx.stroke()
        line(ctx, [(0, -730), (0, -684)], hexc("#E2231A"), 7)
        line(ctx, [(-6, -720), (-6, -690)], GOLD_HI, 3)
        line(ctx, [(6, -720), (6, -690)], GOLD_HI, 3)
        top = -900 if ram else -850
        smooth(ctx, [(-84, -734), (-64, top + 60), (0, top), (64, top + 60), (84, -734), (0, -748)])
        ink(ctx, GOLD, 6)
        rrect(ctx, -90, -736, 180, 24, 8)
        ink(ctx, GOLD_HI, 4)
        gem(ctx, 0, top + 80, 13, RED_GEM)

        if pose == "bound":
            limb(ctx, [(-112, -490), (-132, -420), (-118, -330)], skin, 38)
            hand(ctx, -118, -320, skin, 22)
            limb(ctx, [(112, -490), (132, -420), (118, -330)], skin, 38)
            hand(ctx, 118, -320, skin, 22)
            rope_bands(ctx, rope)
        else:
            ctx.save()
            ctx.translate(-110, -520)
            ctx.rotate(-0.4)
            dv.bow(ctx, 0, -220, 220, -40, a=0.95)
            ctx.restore()
            if pose == "namaste":
                limb(ctx, [(-112, -490), (-70, -430), (-24, -430)], skin, 36)
                limb(ctx, [(112, -490), (70, -430), (24, -430)], skin, 36)
                smooth(ctx, [(-20, -450), (0, -472), (20, -450), (12, -418), (-12, -418)])
                ink(ctx, skin)
            else:  # bless: Abhaya mudra
                limb(ctx, [(-112, -490), (-145, -420), (-120, -320)], skin, 38)
                hand(ctx, -120, -310, skin, 22)
                limb(ctx, [(112, -490), (160, -430), (150, -340)], skin, 38)
                dv.palm(ctx, 150, -330, skin, ang=0.1, s=1.1)
        ctx.restore()
    group(ctx, a, draw)


def ahiravan(ctx, x, y, s, t, pose="smirk", flip=False, a=1.0, fall=0.0):
    """Ahiravan, sorcerer-king of Patala: violet-grey asura, dark horned crown, red eyes, fangs, khadga sword.
    fall 0..1 topples him backwards (rotation about his feet) as he dissolves into dust."""
    def draw():
        if fall > 0:
            ctx.save()
            ctx.translate(x, y)
            ctx.rotate(0.85 * ease_in_out(fall) * (1 if flip else -1))
            ctx.translate(-x, -y)
        place(ctx, x, y, s, t, flip)
        skin = ASURA_SKIN
        glow(ctx, 0, -500, 300, hexc("#C0182E"), 0.28)
        for k in range(7):
            ang = -math.pi / 2 + (k - 3) * 0.32
            smooth(ctx, [(0, -650), (150 * math.cos(ang - 0.08), -650 + 150 * math.sin(ang - 0.08)),
                         (175 * math.cos(ang), -650 + 175 * math.sin(ang)),
                         (150 * math.cos(ang + 0.08), -650 + 150 * math.sin(ang + 0.08))])
            ink(ctx, hexc("#120A14"), 3)
        for fx in (-56, 56):
            ell(ctx, fx, -14, 48, 20)
            ink(ctx, skin)
        smooth(ctx, [(-122, -350), (122, -350), (145, -200), (160, -44), (64, -32), (0, -64), (-64, -32),
                     (-160, -44), (-145, -200)])
        ink(ctx, hexc("#3B0A12"))
        line(ctx, [(158, -48), (64, -36), (0, -68), (-64, -36), (-158, -48)], hexc("#B07A12"), 9)
        smooth(ctx, [(-135, -505), (-66, -530), (66, -530), (135, -505), (140, -430), (108, -345), (-108, -345),
                     (-140, -430)])
        ink(ctx, skin)
        # dark armour plate with red heart-gem (his life)
        smooth(ctx, [(-90, -500), (90, -500), (80, -400), (0, -380), (-80, -400)])
        ink(ctx, hexc("#2A1830"), 4)
        circle(ctx, 0, -450, 18, hexc("#FF2A3D"), 0.6 + 0.4 * math.sin(t * 6))
        gem(ctx, 0, -450, 11, RED_GEM)
        rrect(ctx, -118, -372, 236, 32, 10)
        ink(ctx, hexc("#B07A12"), 5)
        rrect(ctx, -34, -572, 68, 64, 14)
        ink(ctx, skin)
        ell(ctx, 0, -645, 104, 112)
        ink(ctx, skin)
        laugh = pose == "laugh"
        for side in (-1, 1):
            eye(ctx, side * 38, -655, 22, 22, t, iris=hexc("#E01030"), seed=5, lash=False,
                closed=(fall > 0.35))
            line(ctx, [(side * 10, -682), (side * 40, -694), (side * 70, -704)], hexc("#0E0810"), 9)
        # curled moustache
        for side in (-1, 1):
            ctx.move_to(0, -612)
            ctx.curve_to(side * 30, -622, side * 62, -612, side * 70, -632)
            ctx.set_line_width(9)
            rgba(ctx, hexc("#0E0810"))
            ctx.stroke()
        if laugh:
            ell(ctx, 0, -585, 30, 20)
            rgba(ctx, hexc("#3A0610"))
            ctx.fill()
        else:
            ctx.move_to(-24, -592)
            ctx.curve_to(-8, -584, 12, -588, 26, -600)
            ctx.set_line_width(5)
            rgba(ctx, hexc("#3A0610"))
            ctx.stroke()
        for side in (-1, 1):
            ctx.move_to(side * 18, -598)
            ctx.line_to(side * 10, -598)
            ctx.line_to(side * 14, -576)
            ctx.close_path()
            rgba(ctx, WHITE)
            ctx.fill()
        # dark horned crown (he is a king, an asura one)
        smooth(ctx, [(-86, -736), (-60, -828), (-30, -790), (0, -860), (30, -790), (60, -828), (86, -736),
                     (0, -750)])
        ink(ctx, hexc("#3A2A12"), 6)
        rrect(ctx, -92, -742, 184, 24, 8)
        ink(ctx, hexc("#B07A12"), 4)
        gem(ctx, 0, -800, 12, hexc("#FF2A3D"))
        for side in (-1, 1):
            smooth(ctx, [(side * 80, -748), (side * 140, -800), (side * 150, -870), (side * 112, -790)])
            ink(ctx, hexc("#D9CBB0"), 4)

        def sword(hx, hy, ang):
            ctx.save()
            ctx.translate(hx, hy)
            ctx.rotate(ang)
            rrect(ctx, -10, -8, 20, 40, 5)
            ink(ctx, hexc("#B07A12"), 3)
            line(ctx, [(-34, -8), (34, -8)], hexc("#B07A12"), 9)
            smooth(ctx, [(-11, -10), (11, -10), (16, -200), (0, -290), (-8, -200)], k=0.12)
            ink(ctx, hexc("#C9D3DE"), 3)
            line(ctx, [(0, -20), (0, -240)], WHITE, 2, a=0.7)
            ctx.restore()

        if fall > 0:
            limb(ctx, [(-125, -495), (-200, -560), (-230, -660)], skin, 38)
            hand(ctx, -230, -670, skin, 22)
            limb(ctx, [(125, -495), (200, -560), (230, -660)], skin, 38)
            hand(ctx, 230, -670, skin, 22)
        elif laugh:
            limb(ctx, [(125, -495), (190, -580), (175, -700)], skin, 38)
            hand(ctx, 175, -705, skin, 22)
            sword(175, -705, 0.25)
            limb(ctx, [(-125, -495), (-170, -420), (-118, -360)], skin, 38)
            hand(ctx, -118, -360, skin, 22)
        else:  # smirk: sword lowered, other hand pointing at the lamps
            limb(ctx, [(125, -495), (160, -420), (150, -330)], skin, 38)
            hand(ctx, 150, -320, skin, 22)
            sword(150, -320, math.pi - 0.15)
            limb(ctx, [(-125, -495), (-210, -520), (-270, -560)], skin, 36)
            hand(ctx, -272, -562, skin, 20)
        ctx.restore()
        if fall > 0:
            ctx.restore()
    group(ctx, a, draw)


# -----------------------------------------------------------------------------
# Story: 5 scenes, one KikiVoice line each (34.8s raw voice)
# -----------------------------------------------------------------------------
SPEC = [
    {
        "key": "hook",
        "text": "PANCHMUKHI KYUN?",
        "visual": "Paatal cavern under a red orb; Hanuman Ji in namaste, four divine faces flash in as ghosts",
        "vo": [
            ("ask", [
                ("हनुमान जी ने पंचमुखी", "HANUMAN JI NE PANCHMUKHI"),
                ("अवतार क्यों लिया था?", "AVATAAR KYUN LIYA THA?"),
            ], 0.04),
        ],
    },
    {
        "key": "apharan",
        "text": "AHIRAVAN KA APHARAN",
        "visual": "Shri Ram and Lakshman in maya-sleep sink into Patala; Ahiravan laughs, ropes bind them",
        "vo": [
            ("tell", [
                ("जब अहिरावण ने श्री राम", "JAB AHIRAVAN NE SHRI RAM"),
                ("और लक्ष्मण को पाताल में बंदी बनाया,", "AUR LAKSHMAN KO PAATAAL MEIN BANDI BANAYA,"),
            ], 0.04),
        ],
    },
    {
        "key": "deepak",
        "text": "PAANCH DEEPAK",
        "visual": "Five lamps light up one by one, life-threads to Ahiravan's heart-gem; Hanuman Ji puzzled",
        "vo": [
            ("build", [
                ("तब उसकी जान पांच अलग दिशाओं के", "TAB USKI JAAN PAANCH ALAG DISHAON KE"),
                ("दीपकों में थी — जिन्हें एक साथ बुझाना था!", "DEEPAKON MEIN THI — JINHEN EK SAATH BUJHANA THA!"),
            ], 0.04),
        ],
    },
    {
        "key": "panchmukhi",
        "text": "PANCHMUKHI ROOP",
        "visual": "Hanuman Ji takes five faces in a golden blast, blows out all five lamps, Ahiravan falls",
        "vo": [
            ("punch", [
                ("तब बजरंगबली ने पांच दिव्य मुख धारण कर,", "TAB BAJRANGBALI NE PAANCH DIVYA MUKH DHAARAN KAR,"),
                ("एक ही सांस में पांचों दीपक बुझा दिए!", "EK HI SAANS MEIN PAANCHON DEEPAK BUJHA DIYE!"),
            ], 0.04),
        ],
    },
    {
        "key": "cta",
        "text": "JAI BAJRANGBALI",
        "visual": "Freed Shri Ram (Abhaya) and Lakshman (namaste) beside Panchmukhi Hanuman; petals; pointer arrow",
        "vo": [
            ("whisper", [
                ("और इसीलिए आज भी दुनिया पूछती है...", "AUR ISILIYE AAJ BHI DUNIYA PUCHHTI HAI..."),
            ], 0.04),
        ],
    },
]
DELIVERY, SCRIPT, NARRATION = script_of(SPEC)

HOT = hot_words({
    "PANCHMUKHI": GOLD_HI, "HANUMAN": hexc("#FFAA48"), "PAATAAL": LAVA, "RAHASYA": GOLD_HI,
    "AHIRAVAN": hexc("#FF4D5E"), "RAM": hexc("#7FB2FF"), "LAKSHMAN": hexc("#FFD08A"), "APHARAN": hexc("#C58BFF"),
    "BANDI": hexc("#C58BFF"), "JAAN": hexc("#FF4D5E"), "PAANCH": GOLD_HI, "DEEPAKON": hexc("#FFB347"),
    "SAATH": GOLD_HI, "BAJRANGBALI": hexc("#FFAA48"), "MUKH": GOLD_HI, "SAANS": hexc("#9FE8FF"),
    "DEEPAK": hexc("#FFB347"), "VADH": hexc("#FF4D5E"), "BHAKT": GOLD_HI, "JAI": GOLD_HI,
    "COMMENT": GOLD_HI, "SUBSCRIBE": SAFF, "DIVYA": SAFF,
})


# -----------------------------------------------------------------------------
# Scenes
# -----------------------------------------------------------------------------
LAMPS_AROUND = [(540, 300), (150, 650), (930, 650), (150, 1075), (930, 1075)]
HEAD_TIPS = [(540, 560), (420, 720), (660, 720), (400, 800), (680, 800)]   # where each breath leaves from


class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"panch": c("PANCHMUKHI", 0.6), "pataal": c("PAATAAL", d * 0.5), "rahasya": c("RAHASYA", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["panch"] + 0.2, "shimmer"), (b["pataal"], "thud"), (b["rahasya"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        quake = 7 * math.sin(t * 40) * max(0.0, 1 - abs(t - b["pataal"]) / 0.45)
        ctx.save()
        ctx.translate(quake, 0)
        patala_bg(ctx, t, rage=clamp((t - b["pataal"]) / 1.0))
        ghost = clamp((t - b["panch"] - 0.2) / 0.6) * (0.55 + 0.25 * math.sin(t * 5))
        panch_heads(ctx, 540, GROUND - 10, 0.76, t, a=ghost)
        hanuman(ctx, 540, GROUND - 10, 0.76, t, pose="gada", look=(0.0, -0.2 if t > b["pataal"] else 0.0),
                aura=ghost < 0.3)
        ctx.restore()
        flash(ctx, t - b["panch"] - 0.2, c=(1, 0.9, 0.6), dur=0.5)


class Apharan(Cued):
    def beats(self, d):
        c = self.cue
        return {"ahi": c("AHIRAVAN", 0.4), "apharan": c("APHARAN", d * 0.4), "bandi": c("BANDI", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(b["ahi"], "thud"), (b["apharan"], "whoosh"), (b["bandi"], "soft_thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        patala_bg(ctx, t, rage=0.6)
        # maya portal the captives sink out of
        u = ease_out_cubic(clamp((t - b["ahi"] + 0.2) / max(0.6, b["apharan"] - b["ahi"] + 0.8)))
        if u < 1:
            for k in range(4):
                r = 70 + 50 * k + 20 * math.sin(t * 4 + k)
                ctx.arc(320, 330, r, 0, math.tau)
                ctx.set_line_width(6)
                rgba(ctx, MAYA, 0.45 * (1 - u))
                ctx.stroke()
        drop = (1 - u) * 520
        rope = clamp((t - b["bandi"]) / 0.4)
        raghu(ctx, 210, GROUND - 10 - drop, 0.68, t, who="ram", pose="bound", rope=rope, a=0.2 + 0.8 * u)
        raghu(ctx, 430, GROUND - 10 - drop, 0.66, t, who="lakshman", pose="bound", rope=rope, a=0.2 + 0.8 * u)
        ahiravan(ctx, 830, GROUND - 10, 0.74, t, pose="laugh" if t > b["apharan"] else "smirk", flip=True)


class Deepak(Cued):
    def beats(self, d):
        c = self.cue
        return {"jaan": c("JAAN", 0.4), "panch": c("PAANCH", d * 0.25), "saath": c("SAATH", d * 0.75)}

    def lamp_times(self, d):
        b = self.beats(d)
        span = max(1.2, b["saath"] - b["panch"] - 0.4)
        return [b["panch"] + span * k / 5 for k in range(5)]

    def events(self, d):
        b = self.beats(d)
        return [(b["jaan"], "soft_thud")] + [(lt, "pop") for lt in self.lamp_times(d)] + [(b["saath"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        patala_bg(ctx, t, rage=0.4)
        ax, ay = 770, GROUND - 10
        heart = (ax, ay - 450 * 0.74)
        lamps = [(560, 330), (500, 640), (1000, 600), (520, 1010), (1010, 1010)]
        for k, ((lx, ly), lt) in enumerate(zip(lamps, self.lamp_times(d))):
            on = clamp((t - lt) / 0.35)
            if on > 0:
                line(ctx, [heart, (lx, ly - 60)], hexc("#FF2A3D"), 4, a=on * (0.45 + 0.3 * math.sin(t * 6 + k)))
        ahiravan(ctx, ax, ay, 0.74, t, pose="smirk" if t < b["saath"] else "laugh", flip=True)
        for k, ((lx, ly), lt) in enumerate(zip(lamps, self.lamp_times(d))):
            on = clamp((t - lt) / 0.35)
            deepak(ctx, lx, ly, 0.55, t, flame=ease_out_back(on) if on > 0 else 0.0, seed=k)
        # Hanuman Ji puzzled, looking from lamp to lamp
        look = (0.5 * math.sin(t * 1.8), -0.3 + 0.2 * math.cos(t * 1.3))
        hanuman(ctx, 230, GROUND - 10, 0.72, t, pose="think" if t < b["saath"] else "gada", mouth="worry",
                look=look)


class Panchmukhi(Cued):
    def beats(self, d):
        c = self.cue
        return {"bajrang": c("BAJRANGBALI", 0.3), "mukh": c("MUKH", d * 0.22), "saans": c("SAANS", d * 0.45),
                "bujha": c("BUJHAKAR", d * 0.62), "vadh": c("VADH", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(b["bajrang"], "shimmer"), (b["mukh"], "boom"), (b["saans"], "whoosh"),
                (b["bujha"] + 0.3, "zap"), (b["vadh"] - 0.35, "whoosh"), (b["vadh"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        out_t = b["bujha"] + 0.3                         # all five lamps die on the same frame
        shake = 9 * math.sin(t * 45) * max(0.0, 1 - abs(t - out_t) / 0.4)
        shake += 7 * math.sin(t * 50) * max(0.0, 1 - abs(t - b["vadh"]) / 0.4)
        ctx.save()
        ctx.translate(shake, 0)
        patala_bg(ctx, t, rage=0.3)
        heads = ease_out_back(clamp((t - b["mukh"] + 0.3) / 0.6))
        move = ease_in_out(clamp((t - b["vadh"] + 0.5) / 0.6))
        hx = lerp(540, 320, move)
        # golden aura pulse rings after the transformation
        if heads > 0.3:
            for k in range(3):
                ph = ((t - b["mukh"]) * 0.9 + k / 3) % 1
                ctx.arc(hx, GROUND - 520, 120 + 520 * ph, 0, math.tau)
                ctx.set_line_width(8)
                rgba(ctx, GOLD_HI, 0.5 * (1 - ph))
                ctx.stroke()
        # five lamps (fade away as the camera turns to Ahiravan)
        lamp_a = 1 - move
        if lamp_a > 0.02:
            blowing = b["saans"] - 0.1 < t < out_t + 0.1
            for k, ((lx, ly), (sx, sy)) in enumerate(zip(LAMPS_AROUND, HEAD_TIPS)):
                if blowing:
                    for j in range(3):
                        ph = (t * 2.4 + j / 3 + k * 0.17) % 1
                        px, py = lerp(sx, lx, ph), lerp(sy, ly - 50, ph)
                        line(ctx, [(px, py), (lerp(sx, lx, ph + 0.12), lerp(sy, ly - 50, ph + 0.12))],
                             hexc("#BFF4FF"), 6, a=0.7 * lamp_a)
                ctx.push_group()
                if t < out_t:
                    flicker = 1.0 if t < b["saans"] else 1 - 0.55 * clamp((t - b["saans"]) / (out_t - b["saans"]))
                    deepak(ctx, lx, ly, 0.5, t, flame=flicker, seed=k)
                else:
                    deepak(ctx, lx, ly, 0.5, t, flame=0.0, smoke=t - out_t, seed=k)
                ctx.pop_group_to_source()
                ctx.paint_with_alpha(lamp_a)
        # Ahiravan topples as his life goes out
        if move > 0:
            fall = clamp((t - b["vadh"]) / 0.9)
            ahiravan(ctx, 840, GROUND - 10, 0.72, t, pose="smirk", flip=True, a=move * (1 - clamp(fall * 1.4 - 0.6)),
                     fall=fall)
            if fall > 0:
                for i in range(18):
                    ang = rnd(i, 2) * math.tau
                    r = 60 + 260 * fall * rnd(i, 4)
                    circle(ctx, 840 + r * math.cos(ang), GROUND - 420 + r * math.sin(ang), 5, GOLD_HI,
                           0.8 * (1 - fall))
        mouth = "blow" if b["saans"] - 0.1 < t < out_t + 0.2 else "smile"
        panchmukhi(ctx, hx, GROUND - 10, 0.76, t, heads=heads, pose="gada", mouth=mouth)
        # gada strike flash on Ahiravan
        if move > 0:
            glow(ctx, 760, GROUND - 520, 260, GOLD_HI, 0.8 * max(0.0, 1 - abs(t - b["vadh"]) / 0.35))
        ctx.restore()
        flash(ctx, t - b["mukh"] + 0.1, c=(1, 0.92, 0.6), dur=0.55)


class Cta(Cued):
    def beats(self, d):
        c = self.cue
        return {"bhakt": c("BHAKT", 0.6), "comment": c("COMMENT", d * 0.45), "sub": c("SUBSCRIBE", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(b["comment"], "ghanti"), (b["sub"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        patala_bg(ctx, t, freed=clamp(0.4 + t / 2.0))
        dv.petals(ctx, t, n=40, seed=11, a=0.9)
        # broken ropes falling away
        for k, rx in enumerate((150, 270, 380, 470)):
            u = clamp(t / 1.2)
            if u < 1:
                line(ctx, [(rx, 800 + 380 * u), (rx + 50, 790 + 380 * u + 20 * math.sin(k))], hexc("#6B4423"), 10,
                     a=1 - u)
        raghu(ctx, 205, GROUND - 10, 0.68, t, who="ram", pose="bless")
        raghu(ctx, 875, GROUND - 10, 0.66, t, who="lakshman", pose="namaste", flip=True)
        panchmukhi(ctx, 540, GROUND - 10, 0.70, t, heads=1.0, pose="abhaya")
        # pointer to the Shorts comment button (right edge), no text
        if t > b["comment"] - 0.2:
            bob = 14 * math.sin(t * 8)
            ax, ay = 1020, 1090 + bob
            glow(ctx, ax, ay, 70, GOLD_HI, 0.5)
            ctx.move_to(ax, ay + 60)
            ctx.line_to(ax - 34, ay)
            ctx.line_to(ax - 12, ay)
            ctx.line_to(ax - 12, ay - 50)
            ctx.line_to(ax + 12, ay - 50)
            ctx.line_to(ax + 12, ay)
            ctx.line_to(ax + 34, ay)
            ctx.close_path()
            ink(ctx, GOLD_HI, 4)


SCENE_CLASSES = {"hook": Hook, "apharan": Apharan, "deepak": Deepak, "panchmukhi": Panchmukhi, "cta": Cta}

UPLOAD = {
    "title": "Panchmukhi Hanuman Rahasya: Ahiravan Ki Jaan 5 Deepakon Mein! 🚩 #shorts",
    "titles": [
        "Panchmukhi Hanuman Rahasya: Ahiravan Ki Jaan 5 Deepakon Mein! 🚩 #shorts",
        "Panchmukhi Roop Kyun Liya? Paatal Lok Ka Rahasya 😱 #shorts",
        "Ahiravan Ki Jaan 5 Deepakon Mein Thi! Panchmukhi Hanuman Ka Rahasya #shorts",
        "Jab Ahiravan Ne Shri Ram Ko Paatal Le Gaya! Panchmukhi Hanuman #shorts",
        "Panchmukhi Hanuman Ke 5 Mukh Ka Asli Rahasya 🚩 #shorts",
        "Ek Saans Mein 5 Deepak! Panchmukhi Hanuman Aur Ahiravan Vadh #shorts",
    ],
    "thumb_text": "PANCHMUKHI KYUN BANE?",
    "queries": ["panchmukhi hanuman rahasya", "ahiravan vadh", "panchmukhi roop kyun liya"],
    "description": (
        "Panchmukhi Hanuman rahasya: Hanuman Ji ne Panchmukhi roop kyun liya? Ramayan yuddh mein Paatal ke raja Ahiravan ne Shri Ram aur "
        "Lakshman ka apharan kar liya tha. Uski jaan paanch dishaon mein jal rahe paanch deepakon mein thi, jinhe "
        "ek saath bujhana tha. Tab Bajrangbali ne Hanuman, Narasimha, Garuda, Varaha aur Hayagriva - paanch mukh "
        "dhaaran kiye aur ek hi saans mein paanchon deepak bujha kar Ahiravan ka vadh kiya.\n\n"
        "Note: Ahiravan ki yeh katha Krittivasi Ramayan aur lok-paramparaon mein milti hai; Valmiki Ramayan mein "
        "iska varnan nahi hai. Paanch mukhon ka varnan Panchmukha Hanumat Kavach mein hai.\n\n"
        "Comment mein 'JAI BAJRANGBALI' likhiye aur Divya Rahasya ko subscribe karein. 🙏🚩\n\n"
        "#Shorts #PanchmukhiHanuman #Hanuman #Ramayan #DivyaRahasya"
    ),
    "tags": [
        "panchmukhi hanuman", "panchmukhi hanuman story", "ahiravan vadh", "ahiravan mahiravan",
        "hanuman ji", "paatal lok", "ramayan katha", "hanuman 5 mukh", "divya rahasya", "sanatan katha", "shorts",
    ],
    "hashtags": ["#Shorts", "#PanchmukhiHanuman", "#Hanuman"],
}


def thumbnail(ctx):
    """1080x1920 cover: Panchmukhi Hanuman centre-stage with five lamps, 'PANCHMUKHI KYUN?'."""
    patala_bg(ctx, 0.4, rage=0.6)
    for k, (lx, ly) in enumerate([(150, 760), (930, 760), (150, 1090), (930, 1090)]):
        deepak(ctx, lx, ly, 0.55, 0.4, seed=k)
    for k in range(3):
        ctx.arc(540, GROUND - 560, 260 + 90 * k, 0, math.tau)
        ctx.set_line_width(7)
        rgba(ctx, GOLD_HI, 0.35 - 0.1 * k)
        ctx.stroke()
    panchmukhi(ctx, 540, GROUND - 10, 0.82, 0.4, heads=1.0, pose="gada")

    g = cairo.LinearGradient(0, 0, 0, 560)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.92)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 560)
    ctx.set_source(g)
    ctx.fill()
    g = cairo.LinearGradient(0, 1150, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.9)
    ctx.rectangle(0, 1150, W, H - 1150)
    ctx.set_source(g)
    ctx.fill()

    text(ctx, "PANCHMUKHI", 540, 200, 130, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "KYUN BANE?", 540, 330, 96, hexc("#FF4D5E"), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
         stroke_w=16)
    text(ctx, "AHIRAVAN KA PAATAAL RAHASYA", 540, 1380, 56, WHITE, font=CAPTION_FONT, bold=False,
         stroke=(0, 0, 0), stroke_w=10)
    text(ctx, "DIVYA RAHASYA", 540, 1800, 40, GOLD_HI, a=0.8)
