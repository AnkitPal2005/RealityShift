"""Ram Van Gaman: 14 Saal Paidal, Wapsi Ek Udaan Mein! Shri Ram ka poora safar ek map par (~23s, six scenes).

Usage (from SanatanKatha/):
  python make.py ram_van_gaman --preview       # contact sheet + thumbnail
  python make.py ram_van_gaman --kiki-split    # cut the narrator voice into line clips (Whisper anchored)
  python make.py ram_van_gaman                 # final render from the user's KikiVoice clips

Rahasya:
Shri Ram walked from Ayodhya to Lanka through fourteen years of vanvas (Shringverpur, Prayag, Chitrakoot,
Dandakaranya, Panchavati, Kishkindha, Rameshwaram), the Setu was built in five days and was a hundred yojan
long (Valmiki Yuddha Kanda 22). The way back was one flight of the Pushpak Viman (Yuddha Kanda 123-127).

Layout: one glowing map hangs over every scene and the route draws itself as the story moves; the characters
act the line below it. The video loops: the last line ("kyunki shuruaat hui thi...") lands on Ayodhya and
the hook ("chaudah saal paidal...") starts there.
"""

import math
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cairo

from core import engine, katha, upload_kit  # noqa: F401
from core.katha import *  # noqa: F401,F403
import core.devta as dv
from core.devta import group, place, halo, smooth, ink, ell, gem, limb, hand, sheen, eye, shade

# Characters already drawn for earlier kathas (same rig, same look across the channel)
from kathas.ram_hanuman import shri_ram          # royal mukut, Kodanda, poses bow/aim/shot/bless
from kathas.hanumad_ramayana import hanuman      # poses namaste/abhaya/lift_rock
from kathas.lepakshi import jatayu_bird

TOPIC = "SHRI RAM VAN GAMAN 14 SAAL KA SAFAR EK MAP PAR"
OUTPUTS = {"edge": "ram_van_gaman_short.mp4"}
MUSIC_STYLE = "divine"    # channel signature bed (previous Short tulsi_vivah used ambient: rotate)
MUSIC_BPM = 84            # >= 6 BPM away from tulsi_vivah (76)
MUSIC_VOLUME = 0.11
TAIL_PAD = 0.04
MAX_GAP = 0.04

WHITE = (1.0, 1.0, 1.0)
RED_GEM = hexc("#D61F3A")
SAFFRON_PATH = hexc("#FF9A3C")
FLY_GOLD = hexc("#FFE082")
STONE = hexc("#7D8594")
STONE_DK = hexc("#4B5260")

SOURCES = [
    "Valmiki Ramayana, Ayodhya Kanda 50-54: Shringaverapura and Nishadraj Guha's boat across the Ganga, "
    "Bharadwaj ashram at Prayag, then Chitrakoot.",
    "Valmiki Ramayana, Aranya Kanda: Dandakaranya, Panchavati, the abduction of Sita and Jatayu's fall; "
    "Kishkindha Kanda 3: Hanuman meets Shri Ram.",
    "Valmiki Ramayana, Yuddha Kanda 22: the Setu built in five days (14, 20, 21, 22, 23 yojan), "
    "a hundred yojan long and ten wide.",
    "Valmiki Ramayana, Yuddha Kanda 123-127: return on the Pushpak Viman, halting at Bharadwaj ashram "
    "before Ayodhya. The modern 'Ram Van Gaman Path' site list is tradition; distances are not in Valmiki, "
    "so the script says 'hazaaron kilometer' and gives no exact figure.",
]


# =============================================================================
# The map: one glowing India map hangs over every scene
# =============================================================================
MAP_X, MAP_Y, MAP_W, MAP_H = 320, 162, 440, 452
K = 13.4


def mp(lon, lat):
    return (540 + (lon - 82.75) * K, 388 + (21.25 - lat) * K)


INDIA = [mp(*p) for p in [
    (68.4, 23.6), (69.2, 22.3), (70.0, 21.0), (71.2, 20.8), (72.6, 21.4), (72.9, 20.2), (72.8, 19.0),
    (73.2, 17.3), (73.7, 15.9), (74.3, 14.6), (74.8, 12.9), (75.5, 11.6), (76.2, 10.1), (76.6, 9.0),
    (77.5, 8.1), (78.2, 8.9), (79.0, 9.3), (79.3, 10.3), (79.9, 10.4), (79.8, 11.6), (80.3, 13.2),
    (80.1, 15.2), (81.2, 16.4), (82.4, 16.7), (83.9, 18.2), (85.3, 19.6), (86.9, 20.8), (87.0, 21.6),
    (88.2, 21.7), (88.9, 21.6), (89.1, 22.8), (88.7, 24.3), (88.1, 24.9), (88.4, 25.9), (89.8, 26.0),
    (90.4, 25.2), (92.1, 25.1), (91.9, 23.7), (92.6, 22.0), (93.3, 23.6), (94.3, 24.5), (95.0, 26.6),
    (96.8, 27.4), (97.2, 28.2), (96.2, 29.3), (94.6, 29.3), (92.4, 27.8), (89.9, 26.9), (88.9, 27.3),
    (88.1, 27.9), (88.1, 26.4), (85.8, 26.6), (84.1, 27.4), (81.1, 28.4), (80.1, 28.8), (81.0, 30.2),
    (79.2, 31.0), (78.4, 32.5), (79.0, 34.3), (77.8, 35.5), (75.5, 36.8), (74.4, 36.4), (73.5, 34.8),
    (73.9, 33.6), (74.5, 32.6), (75.0, 32.3), (74.6, 31.0), (73.9, 30.0), (73.2, 29.0), (72.0, 28.0),
    (70.7, 27.8), (69.6, 26.9), (70.2, 26.4), (70.1, 25.3), (71.0, 24.4), (69.6, 24.3), (68.8, 24.0),
]]
LANKA_C = mp(80.75, 7.75)

# walking route: Ayodhya, Shringverpur, Prayag, Chitrakoot, Dandakaranya, Panchavati, Kishkindha,
# Rameshwaram, Lanka
WALK = [mp(*p) for p in [(82.2, 26.8), (81.65, 25.6), (81.85, 25.43), (80.87, 25.2), (81.6, 20.2),
                         (73.8, 20.0), (76.46, 15.33), (79.31, 9.29), (80.4, 8.4)]]
AYODHYA, CHITRAKOOT, PANCHAVATI, KISHKINDHA, RAMESHWARAM, LANKA = 0, 3, 5, 6, 7, 8
LABELS = [(AYODHYA, "AYODHYA", "r"), (CHITRAKOOT, "CHITRAKOOT", "l"), (PANCHAVATI, "PANCHAVATI", "l"),
          (KISHKINDHA, "KISHKINDHA", "l"), (RAMESHWARAM, "RAMESHWARAM", "l"), (LANKA, "LANKA", "r")]


def _bez(p0, p1, p2, n=24):
    return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0],
             (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]) for u in (i / n for i in range(n + 1))]


# Pushpak flight home: Lanka -> Kishkindha -> Prayag (Bharadwaj ashram) -> Ayodhya, one sweeping arc
FLY = _bez(WALK[LANKA], mp(88.5, 17.5), WALK[KISHKINDHA])[:-1] + _bez(WALK[KISHKINDHA], mp(78.0, 23.5), WALK[2])[:-1] \
    + _bez(WALK[2], mp(82.6, 26.0), WALK[AYODHYA])


def _cum(pts):
    c = [0.0]
    for a, b in zip(pts, pts[1:]):
        c.append(c[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return c


WALK_CUM, FLY_CUM = _cum(WALK), _cum(FLY)
U = [c / WALK_CUM[-1] for c in WALK_CUM]      # route fraction at each stop


def upto(pts, cum, u):
    """Points of the polyline up to fraction u, plus the head point and heading."""
    L = cum[-1] * clamp(u)
    out = [pts[0]]
    for i in range(1, len(pts)):
        if cum[i] <= L:
            out.append(pts[i])
            continue
        a, b = pts[i - 1], pts[i]
        k = (L - cum[i - 1]) / max(1e-6, cum[i] - cum[i - 1])
        out.append((lerp(a[0], b[0], k), lerp(a[1], b[1], k)))
        return out, out[-1], math.atan2(b[1] - a[1], b[0] - a[0])
    a, b = pts[-2], pts[-1]
    return out, pts[-1], math.atan2(b[1] - a[1], b[0] - a[0])


def vimana_icon(ctx, x, y, s, ang=0.0):
    """Tiny golden Pushpak glyph for the map."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    glow(ctx, 0, 0, 34, FLY_GOLD, 0.8)
    for side in (-1, 1):                                  # wings
        smooth(ctx, [(side * 8, 2), (side * 30, -10), (side * 26, 4)])
        ink(ctx, GOLD_HI, 2)
    rrect(ctx, -14, 0, 28, 7, 3)
    ink(ctx, GOLD, 2)
    smooth(ctx, [(-9, 1), (-6, -12), (0, -20), (6, -12), (9, 1)])
    ink(ctx, GOLD_HI, 2)
    ctx.restore()


def india_map(ctx, t, walk=0.0, fly=0.0, ping=None, ping_u=0.0, home=0.0, a=1.0):
    """walk/fly: 0..1 along the route and the flight home; ping: stop index with an expanding ring."""
    ctx.push_group()
    rrect(ctx, MAP_X, MAP_Y, MAP_W, MAP_H, 26)
    g = cairo.LinearGradient(0, MAP_Y, 0, MAP_Y + MAP_H)
    g.add_color_stop_rgba(0, 0.05, 0.09, 0.2, 0.86)
    g.add_color_stop_rgba(1, 0.03, 0.06, 0.15, 0.9)
    ctx.set_source(g)
    ctx.fill_preserve()
    rgba(ctx, GOLD, 0.9)
    ctx.set_line_width(4)
    ctx.stroke()
    for i in range(10):                                   # sea shimmer
        yy = MAP_Y + 40 + i * 42
        line(ctx, [(MAP_X + 20 + 8 * math.sin(t + i), yy), (MAP_X + 70 + 8 * math.sin(t + i), yy)],
             hexc("#5C8AD6"), 2, 0.25)
    # land
    ctx.move_to(*INDIA[0])
    for p in INDIA[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    g = cairo.LinearGradient(0, MAP_Y, 0, MAP_Y + MAP_H)
    g.add_color_stop_rgb(0, *hexc("#B98B4E"))
    g.add_color_stop_rgb(1, *hexc("#8E6234"))
    ctx.set_source(g)
    ctx.fill_preserve()
    rgba(ctx, hexc("#FFD58A"), 0.9)
    ctx.set_line_width(2.5)
    ctx.stroke()
    ell(ctx, LANKA_C[0], LANKA_C[1], 0.85 * K, 1.5 * K, 0.25)
    rgba(ctx, hexc("#A0743E"))
    ctx.fill_preserve()
    rgba(ctx, hexc("#FFD58A"), 0.9)
    ctx.set_line_width(2.5)
    ctx.stroke()
    # faint full route under everything
    line(ctx, WALK, hexc("#3A2410"), 3, 0.35)
    # walked route: glowing saffron footsteps
    if walk > 0:
        pts, head, ang = upto(WALK, WALK_CUM, walk)
        line(ctx, pts, SAFFRON_PATH, 9, 0.25)
        ctx.set_dash([7, 6], -t * 18)
        line(ctx, pts, hexc("#FFD9A0"), 4)
        ctx.set_dash([])
        if walk < 1:
            pulse = 1 + 0.3 * math.sin(t * 9)
            glow(ctx, head[0], head[1], 30 * pulse, SAFFRON_PATH, 0.9)
            circle(ctx, head[0], head[1], 6, WHITE)
    # flight home: golden arc and the vimana
    if fly > 0:
        pts, head, ang = upto(FLY, FLY_CUM, fly)
        line(ctx, pts, FLY_GOLD, 12, 0.25)
        line(ctx, pts, FLY_GOLD, 4)
        vimana_icon(ctx, head[0], head[1], 1.0)
    # stops and labels
    for idx, name, side in LABELS:
        x, y = WALK[idx]
        lit = walk >= U[idx] - 1e-3 or (idx == AYODHYA)
        circle(ctx, x, y, 6 if lit else 4, GOLD_HI if lit else hexc("#E8C890"), 1.0 if lit else 0.6)
        lx = x + 12 if side == "r" else x - 12
        text(ctx, name, lx, y, 21, GOLD_HI if lit else hexc("#F2E2C0"), font=CAPTION_FONT, bold=False,
             anchor="l" if side == "r" else "r", a=1.0 if lit else 0.55, stroke=(0, 0, 0), stroke_w=4)
    if ping is not None and 0 < ping_u < 1:
        x, y = WALK[ping]
        ctx.arc(x, y, 8 + 60 * ping_u, 0, math.tau)
        rgba(ctx, GOLD_HI, 1 - ping_u)
        ctx.set_line_width(4)
        ctx.stroke()
    if home > 0:                                           # loop: Ayodhya glows as the flight lands
        x, y = WALK[AYODHYA]
        glow(ctx, x, y, 70 * home, FLY_GOLD, 0.9 * home)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(a)


# =============================================================================
# Scenery
# =============================================================================
PAL = {
    "ayodhya":    ("#2A1840", "#D9663A", "#FFC26B", "#3A1E2A", "#24121C", "#2A140E"),
    "ganga":      ("#3A2E62", "#E88A6A", "#FFD7A0", "#3C3050", "#2A2238", "#24301E"),
    "forest":     ("#1A1430", "#7A3050", "#E07A3E", "#251A2E", "#170F1E", "#1A140E"),
    "kishkindha": ("#2A1A3A", "#C8582E", "#FFB45A", "#5A3020", "#3C1E16", "#3A2014"),
    "ocean":      ("#14204A", "#5A4A8A", "#F0A060", "#22305A", "#182448", "#C9A46A"),
    "lanka":      ("#12060E", "#4A0E1E", "#B8402A", "#2A0A14", "#1C060E", "#1A0A0A"),
    "sky":        ("#2A4A8A", "#F2B27A", "#FFE2A8", "#E8D2C0", "#D8C0B0", "#D8C0B0"),
}


def hills(ctx, yy, c, amp, f, ph):
    ctx.move_to(0, yy)
    for x in range(0, W + 1, 30):
        ctx.line_to(x, yy - amp * math.sin(x / f + ph) - amp * 0.4 * math.sin(x / (f * 0.37) + ph * 2))
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    rgba(ctx, c)
    ctx.fill()


def tree(ctx, x, y, s, c):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.rectangle(-10, -120, 20, 120)
    rgba(ctx, c)
    ctx.fill()
    for dx, dy, r in ((0, -170, 70), (-50, -130, 50), (50, -130, 50), (0, -230, 50)):
        circle(ctx, dx, dy, r, c)
    ctx.restore()


def dust(ctx, t, c=hexc("#FFE2A8"), n=26, seed=3):
    for i in range(n):
        x = (rnd(i, seed) * W + t * 30 * (0.4 + rnd(i, seed + 1))) % W
        y = 650 + 520 * rnd(i, seed + 2) + 14 * math.sin(t * 1.5 + i)
        circle(ctx, x, y, 2 + 3 * rnd(i, seed + 4), c, 0.25 + 0.2 * math.sin(t * 2 + i))


def scenery(ctx, t, kind):
    top, mid, low, h1, h2, gnd = (hexc(c) for c in PAL[kind])
    dv.sky(ctx, top, mid, low, 0.62)
    if kind == "lanka":
        dv.stars(ctx, t, n=40, a=0.6)
        circle(ctx, 540, 760, 70, hexc("#FFD9B0"), 0.85)
        glow(ctx, 540, 760, 260, hexc("#FF7A4A"), 0.35)
    elif kind == "sky":
        glow(ctx, 540, 780, 520, hexc("#FFF0C0"), 0.6)
    else:
        dv.sun_disc(ctx, 540, 780, 78, t, a=0.95, rays=18)
    if kind == "sky":                                     # flight: clouds racing past
        for i in range(14):
            sp = 500 + 300 * rnd(i, 21)
            x = W + 200 - ((t * sp + rnd(i, 22) * 1600) % (W + 500))
            y = 640 + 560 * rnd(i, 23)
            for k in range(4):
                circle(ctx, x + k * 46, y - 18 * math.sin(k * 1.3), 40 + 14 * math.sin(k * 2.1 + i),
                       hexc("#FFF8EC"), 0.55)
        for i in range(10):                               # speed lines
            y = 660 + 50 * i
            x = W - ((t * 1400 + i * 233) % (W + 400))
            line(ctx, [(x, y), (x + 220, y)], WHITE, 3, 0.35)
        return
    hills(ctx, 960, h1, 34, 160, 0.6)
    if kind == "ayodhya":                                 # palace domes on the far hill
        for k, x in enumerate((140, 300, 780, 940)):
            hh = 90 + 30 * (k % 2)
            ctx.rectangle(x - 40, 960 - hh, 80, hh)
            rgba(ctx, hexc("#4A2232"))
            ctx.fill()
            smooth(ctx, [(x - 46, 960 - hh), (x, 960 - hh - 70), (x + 46, 960 - hh)])
            rgba(ctx, hexc("#4A2232"))
            ctx.fill()
            circle(ctx, x, 960 - hh - 78, 6, GOLD_HI, 0.9)
            for w in (-16, 16):
                circle(ctx, x + w, 960 - hh * 0.5, 5, hexc("#FFC46B"), 0.8)
    if kind == "lanka":                                   # golden Lanka towers far away
        for k, x in enumerate((90, 210, 330, 750, 870, 990)):
            hh = 160 + 60 * rnd(k, 31)
            smooth(ctx, [(x - 46, 990), (x - 34, 990 - hh), (x, 990 - hh - 80), (x + 34, 990 - hh), (x + 46, 990)])
            rgba(ctx, hexc("#3A1A12"))
            ctx.fill()
            glow(ctx, x, 990 - hh * 0.6, 60, hexc("#FFB347"), 0.25 + 0.1 * math.sin(t * 3 + k))
    if kind in ("forest", "ganga", "ayodhya"):
        for i in range(12):
            tree(ctx, 40 + i * 92 + 20 * rnd(i, 5), 1010, 0.55 + 0.3 * rnd(i, 6), h2)
    if kind == "kishkindha":                              # Hampi boulders
        for i, (x, r) in enumerate(((80, 90), (190, 70), (930, 100), (1040, 80), (560, 60))):
            ell(ctx, x, 1010 - r * 0.6, r * 1.2, r)
            ink(ctx, hexc("#7A4228"), 3)
            sheen(ctx, x - r * 0.3, 1010 - r, r * 0.4, r * 0.25, 0.15)
    hills(ctx, 1040, h2, 22, 110, 2.1)
    if kind == "forest":
        dv.peepal(ctx, 540, 1040, 0.55, t)
    if kind == "ganga":                                   # the river fills the foreground
        g = cairo.LinearGradient(0, 1020, 0, H)
        g.add_color_stop_rgb(0, *hexc("#D88A6A"))
        g.add_color_stop_rgb(1, *hexc("#24365A"))
        ctx.rectangle(0, 1020, W, H)
        ctx.set_source(g)
        ctx.fill()
        for i in range(24):
            y = 1040 + i * 14
            x = (rnd(i, 41) * W + t * 40) % W
            line(ctx, [(x - 40, y), (x + 40, y)], hexc("#FFE0B8"), 3, 0.45)
    elif kind == "ocean":                                 # sea, with Rameshwaram's sand on the left
        g = cairo.LinearGradient(0, 900, 0, H)
        g.add_color_stop_rgb(0, *hexc("#3A5A9A"))
        g.add_color_stop_rgb(1, *hexc("#0E1E3E"))
        ctx.rectangle(0, 900, W, H)
        ctx.set_source(g)
        ctx.fill()
        for layer in range(3):
            y0 = 940 + layer * 80
            for x in range(0, W, 70):
                wy = y0 + 10 * math.sin(x / 60 + t * 2.4 + layer)
                line(ctx, [(x, wy), (x + 36, wy - 4)], hexc("#CFE8FF"), 3, 0.5)
        ell(ctx, 120, GROUND + 20, 330, 70)
        ink(ctx, gnd, 3)
    else:
        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, gnd)
        ctx.fill()
        for i in range(36):
            x = rnd(i, 9) * W
            y = GROUND - 14 + 50 * rnd(i, 10)
            c = shade(gnd, 1.8)
            line(ctx, [(x, y), (x - 6, y - 20)], c, 4, 0.8)
            line(ctx, [(x, y), (x + 6, y - 18)], c, 4, 0.8)
    dust(ctx, t)


# =============================================================================
# New characters: Sita, Lakshman, Ravan, Nishadraj (+ naav), Pushpak Viman
# =============================================================================
def sita(ctx, x, y, s, t, pose="walk", look=(0.0, 0.0), flip=False, a=1.0):
    """Mata Sita: red saree with gold border, pallu over the head, maang tikka; no crown."""
    def draw():
        place(ctx, x, y, s, t, flip)
        halo(ctx, 0, -620, 140, t, c=GOLD_HI, a=0.6)
        skin, hair, saree, choli = hexc("#EDB98E"), hexc("#1A0E0A"), hexc("#C8102E"), hexc("#F2B705")
        ell(ctx, 0, -628, 98, 102)
        ink(ctx, hair)
        limb(ctx, [(46, -560), (62, -470), (54, -380)], hair, 30)          # braid
        for fx in (-36, 36):
            ell(ctx, fx, -12, 34, 14)
            ink(ctx, skin)
        smooth(ctx, [(-96, -350), (96, -350), (118, -200), (138, -30), (0, -22), (-138, -30), (-118, -200)])
        ink(ctx, saree)
        for px in (-34, 0, 34):
            line(ctx, [(px, -330), (px * 1.7, -44)], shade(saree, 0.75), 4)
        line(ctx, [(-136, -34), (0, -26), (136, -34)], GOLD, 10)
        smooth(ctx, [(-96, -500), (-48, -520), (48, -520), (96, -500), (100, -430), (82, -350), (-82, -350),
                     (-100, -430)])
        ink(ctx, choli)
        smooth(ctx, [(-100, -505), (-60, -522), (98, -372), (80, -345)], k=0.1)
        ink(ctx, saree, 5)
        line(ctx, [(-50, -512), (-22, -486), (0, -480), (22, -486), (50, -512)], GOLD, 6)
        gem(ctx, 0, -474, 8, RED_GEM)
        rrect(ctx, -26, -562, 52, 54, 12)
        ink(ctx, skin)
        ell(ctx, 0, -622, 80, 88)
        ink(ctx, skin)
        sheen(ctx, -28, -664, 28, 18, 0.14)
        smooth(ctx, [(-82, -640), (-62, -700), (0, -716), (62, -700), (82, -640), (40, -680), (0, -690),
                     (-40, -680)])
        ink(ctx, hair)
        # pallu over the head
        smooth(ctx, [(-106, -590), (-98, -690), (-52, -740), (0, -750), (52, -740), (98, -690), (106, -590),
                     (86, -600), (80, -680), (40, -720), (0, -728), (-40, -720), (-80, -680), (-86, -600)])
        ink(ctx, saree)
        line(ctx, [(-104, -600), (-96, -690), (-52, -738), (0, -748), (52, -738), (96, -690), (104, -600)],
             GOLD, 5)
        line(ctx, [(0, -716), (0, -694)], GOLD, 3)
        gem(ctx, 0, -688, 7, RED_GEM)
        circle(ctx, 0, -664, 6, hexc("#C8102E"))
        scared = pose in ("fear", "reach")
        for side in (-1, 1):
            eye(ctx, side * 30, -628, 20, 23 if not scared else 26, t, look=look, iris=hexc("#2A1810"), seed=3)
            line(ctx, [(side * 12, -656 - (6 if scared else 0)), (side * 46, -652)], hair, 5)
        if scared:
            ell(ctx, 0, -584, 9, 12)
            ink(ctx, hexc("#6A1020"), 3)
        else:
            ctx.move_to(-14, -590)
            ctx.curve_to(-5, -583, 5, -583, 14, -590)
            ctx.set_line_width(4)
            rgba(ctx, hexc("#B5283C"))
            ctx.stroke()
        if pose == "namaste":
            limb(ctx, [(-92, -490), (-56, -440), (-20, -440)], skin, 30)
            limb(ctx, [(92, -490), (56, -440), (20, -440)], skin, 30)
            smooth(ctx, [(-16, -456), (0, -476), (16, -456), (10, -428), (-10, -428)])
            ink(ctx, skin)
        elif pose == "fear":
            for side in (-1, 1):
                limb(ctx, [(side * 92, -490), (side * 140, -560), (side * 104, -620)], skin, 30)
                dv.palm(ctx, side * 104, -630, skin, ang=-side * 0.3, s=0.8)
        elif pose == "reach":                              # one arm stretched forward, the other at the face
            limb(ctx, [(92, -490), (190, -505), (262, -520)], skin, 30)
            dv.palm(ctx, 270, -520, skin, ang=1.35, s=0.8)
            limb(ctx, [(-92, -490), (-130, -560), (-80, -610)], skin, 30)
            hand(ctx, -78, -614, skin, 18)
        else:                                              # walk: one hand holds the pallu
            limb(ctx, [(-92, -490), (-118, -420), (-100, -332)], skin, 30)
            hand(ctx, -100, -322, skin, 18)
            limb(ctx, [(92, -490), (106, -430), (60, -400)], skin, 30)
            hand(ctx, 56, -398, skin, 18)
        ctx.restore()
    group(ctx, a, draw)


def lakshman(ctx, x, y, s, t, pose="bow", flip=False, a=1.0):
    """Lakshman: fair, green dhoti with gold border, smaller mukut with a blue gem, quiver on the back."""
    def draw():
        place(ctx, x, y, s, t, flip)
        halo(ctx, 0, -640, 150, t, c=GOLD, a=0.7)
        skin, hair, dhoti = hexc("#E2A877"), hexc("#1C120C"), hexc("#2E8B57")
        # quiver behind the shoulder
        ctx.save()
        ctx.translate(70, -520)
        ctx.rotate(0.35)
        rrect(ctx, -22, 0, 44, 230, 12)
        ink(ctx, hexc("#7A4A1E"))
        for k in range(3):
            line(ctx, [(-12 + 12 * k, 0), (-12 + 12 * k, -60)], hexc("#F3E2BC"), 5)
            smooth(ctx, [(-12 + 12 * k, -60), (-20 + 12 * k, -86), (-4 + 12 * k, -86)])
            ink(ctx, RED_GEM, 2)
        ctx.restore()
        for side in (-1, 1):
            smooth(ctx, [(side * 66, -690), (side * 112, -610), (side * 120, -540), (side * 92, -490),
                         (side * 82, -560)])
            ink(ctx, hair)
        ell(ctx, 0, -656, 108, 104)
        ink(ctx, hair)
        for fx in (-46, 46):
            ell(ctx, fx, -14, 40, 17)
            ink(ctx, skin)
            line(ctx, [(fx - 22, -28), (fx, -22), (fx + 22, -28)], GOLD, 6)
        smooth(ctx, [(-110, -340), (110, -340), (126, -200), (140, -44), (56, -32), (0, -60), (-56, -32),
                     (-140, -44), (-126, -200)])
        ink(ctx, dhoti)
        line(ctx, [(138, -48), (56, -36), (0, -64), (-56, -36), (-138, -48)], GOLD, 10)
        smooth(ctx, [(-114, -490), (-56, -512), (56, -512), (114, -490), (118, -420), (94, -336), (-94, -336),
                     (-118, -420)])
        ink(ctx, skin)
        smooth(ctx, [(118, -495), (82, -510), (-110, -368), (-90, -340)], k=0.1)
        ink(ctx, hexc("#F2B705"), 4)
        rrect(ctx, -106, -360, 212, 30, 10)
        ink(ctx, GOLD, 4)
        line(ctx, [(-60, -506), (0, -472), (60, -506)], GOLD, 7)
        rrect(ctx, -30, -556, 60, 58, 14)
        ink(ctx, skin)
        for side in (-1, 1):
            ell(ctx, side * 90, -626, 16, 24)
            ink(ctx, skin)
            circle(ctx, side * 95, -594, 11, GOLD)
        ell(ctx, 0, -628, 92, 100)
        ink(ctx, skin)
        sheen(ctx, -30, -672, 34, 22, 0.14)
        for side in (-1, 1):
            eye(ctx, side * 34, -634, 22, 26, t, look=(0.1, 0), iris=hexc("#2A1810"), seed=5)
            line(ctx, [(side * 12, -670), (side * 34, -682), (side * 58, -674)], hair, 7)
        line(ctx, [(0, -712), (0, -672)], hexc("#E2231A"), 6)
        ctx.move_to(-16, -584)
        ctx.curve_to(-6, -578, 6, -578, 16, -584)
        ctx.set_line_width(4)
        rgba(ctx, hexc("#B5283C"))
        ctx.stroke()
        smooth(ctx, [(-70, -716), (-54, -800), (0, -846), (54, -800), (70, -716), (0, -728)])
        ink(ctx, GOLD, 5)
        rrect(ctx, -76, -720, 152, 20, 7)
        ink(ctx, GOLD_HI, 3)
        gem(ctx, 0, -778, 11, hexc("#00B4D8"))
        if pose == "namaste":
            limb(ctx, [(-106, -480), (-60, -430), (-22, -430)], skin, 34)
            limb(ctx, [(106, -480), (60, -430), (22, -430)], skin, 34)
            smooth(ctx, [(-18, -448), (0, -470), (18, -448), (12, -418), (-12, -418)])
            ink(ctx, skin)
        else:                                              # bow held upright, alert
            limb(ctx, [(-106, -480), (-150, -410), (-160, -320)], skin, 34)
            hand(ctx, -160, -312, skin, 20)
            dv.bow(ctx, -168, -600, -40, -60)
            limb(ctx, [(106, -480), (138, -410), (112, -320)], skin, 34)
            hand(ctx, 112, -312, skin, 20)
        ctx.restore()
    group(ctx, a, draw)


def _ravan_head(ctx, x, y, sc, t, roar, main=False):
    skin = hexc("#8C5A44")
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(sc, sc)
    smooth(ctx, [(-66, -60), (-48, -150), (-22, -110), (0, -176), (22, -110), (48, -150), (66, -60)])
    ink(ctx, hexc("#2A1A10"), 4)
    for gx in (-48, 0, 48):
        gem(ctx, gx, -120 if gx else -140, 7, RED_GEM)
    rrect(ctx, -72, -72, 144, 22, 8)
    ink(ctx, GOLD, 4)
    ell(ctx, 0, 0, 74, 82)
    ink(ctx, skin)
    for side in (-1, 1):
        eye(ctx, side * 28, -12, 17, 18, t, look=(-0.4, 0), iris=hexc("#7A0A0A"), seed=6 + x * 0.01)
        line(ctx, [(side * 6, -30), (side * 44, -42)], hexc("#140A06"), 9)  # angry brows
    for side in (-1, 1):                                  # curled moustache
        smooth(ctx, [(0, 26), (side * 30, 18), (side * 58, 30), (side * 62, 12), (side * 40, 32), (0, 36)])
        ink(ctx, hexc("#140A06"), 2)
    if roar:
        ell(ctx, 0, 50, 22, 16)
        ink(ctx, hexc("#4A0A10"), 3)
    else:
        line(ctx, [(-18, 50), (18, 50)], hexc("#4A0A10"), 5)
    ctx.restore()


def ravan(ctx, x, y, s, t, pose="abduct", flip=False, a=1.0, fall=0.0):
    """Ravan: ten heads with dark crowns, black-maroon robes, gold armour; faces left (towards Ram/Sita)."""
    def draw():
        place(ctx, x, y, s, t, flip)
        ctx.rotate(fall * 0.55)                           # topples backwards as he falls
        skin = hexc("#8C5A44")
        glow(ctx, 0, -560, 420, hexc("#B01E2A"), 0.35)
        roar = pose in ("abduct", "sword", "hit")
        # side heads, far ones first
        for k in (5, 4, 3, 2, 1):
            _ravan_head(ctx, 60 * k, -640 + 10 * k, 0.62 - 0.03 * k, t + k, roar)
            if k <= 4:
                _ravan_head(ctx, -60 * k, -640 + 10 * k, 0.62 - 0.03 * k, t - k, roar)
        for fx in (-56, 56):
            ell(ctx, fx, -14, 48, 20)
            ink(ctx, skin)
        smooth(ctx, [(-130, -350), (130, -350), (150, -200), (166, -40), (0, -30), (-166, -40), (-150, -200)])
        ink(ctx, hexc("#3A0A18"))
        line(ctx, [(-164, -44), (0, -34), (164, -44)], GOLD, 10)
        smooth(ctx, [(-140, -510), (-70, -536), (70, -536), (140, -510), (146, -430), (116, -346), (-116, -346),
                     (-146, -430)])
        ink(ctx, skin)
        smooth(ctx, [(-110, -500), (110, -500), (96, -380), (-96, -380)])
        ink(ctx, hexc("#5A1020"), 4)                      # armour plate
        line(ctx, [(-90, -470), (0, -430), (90, -470)], GOLD, 8)
        gem(ctx, 0, -420, 13, RED_GEM)
        rrect(ctx, -124, -370, 248, 34, 12)
        ink(ctx, GOLD, 5)
        rrect(ctx, -34, -580, 68, 60, 14)
        ink(ctx, skin)
        _ravan_head(ctx, 0, -650, 1.0, t, roar, main=True)
        if pose == "abduct":                              # left hand grabbing forward
            limb(ctx, [(-126, -500), (-220, -480), (-300, -490)], skin, 40)
            hand(ctx, -306, -490, skin, 24)
            limb(ctx, [(126, -500), (176, -440), (150, -350)], skin, 40)
            hand(ctx, 150, -340, skin, 24)
        elif pose == "hit":
            for side in (-1, 1):
                limb(ctx, [(side * 126, -500), (side * 210, -560), (side * 250, -650)], skin, 40)
                hand(ctx, side * 252, -660, skin, 24)
        else:                                             # sword raised
            limb(ctx, [(-126, -500), (-190, -430), (-176, -350)], skin, 40)
            hand(ctx, -176, -340, skin, 24)
            limb(ctx, [(126, -500), (186, -580), (170, -680)], skin, 40)
            hand(ctx, 170, -690, skin, 24)
            ctx.move_to(164, -700)
            ctx.line_to(150, -960)
            ctx.line_to(184, -930)
            ctx.line_to(180, -700)
            ctx.close_path()
            ink(ctx, hexc("#D8E0EA"), 4)
            rrect(ctx, 140, -712, 64, 16, 6)
            ink(ctx, GOLD, 3)
        ctx.restore()
    group(ctx, a, draw)


def nishadraj(ctx, x, y, s, t, flip=False, a=1.0):
    """Nishadraj Guha: boatman king of Shringverpur. Rustic headband (no mukut), rope belt, long oar."""
    def draw():
        place(ctx, x, y, s, t, flip)
        skin, hair = hexc("#7A4A2E"), hexc("#1A0E08")
        ph = math.sin(t * 3.2)                            # rowing stroke
        top = (-150 + 40 * ph, -760 + 20 * ph)
        bot = (230 + 50 * ph, 80)
        line(ctx, [top, bot], dv.OUTLINE, 18)
        line(ctx, [top, bot], hexc("#9A6A3A"), 12)
        smooth(ctx, [(bot[0] - 30, bot[1] - 40), (bot[0] + 30, bot[1] - 60), (bot[0] + 40, bot[1] + 20),
                     (bot[0] - 20, bot[1] + 30)])
        ink(ctx, hexc("#9A6A3A"))
        for fx in (-48, 48):
            ell(ctx, fx, -14, 42, 17)
            ink(ctx, skin)
        for fx in (-40, 40):
            limb(ctx, [(fx, -40), (fx * 1.1, -200)], skin, 50)
        smooth(ctx, [(-116, -350), (116, -350), (128, -200), (60, -190), (0, -220), (-60, -190), (-128, -200)])
        ink(ctx, hexc("#D9C7A0"))
        smooth(ctx, [(-120, -500), (-60, -522), (60, -522), (120, -500), (126, -420), (100, -340), (-100, -340),
                     (-126, -420)])
        ink(ctx, skin)
        line(ctx, [(-112, -350), (112, -350)], hexc("#6A4A2A"), 12)                       # rope belt
        for k in range(9):                                                                # wooden beads
            ang = math.pi * (0.15 + 0.7 * k / 8)
            circle(ctx, 60 * math.cos(ang), -520 + 50 * math.sin(ang), 7, hexc("#5A3018"))
        rrect(ctx, -30, -566, 60, 58, 14)
        ink(ctx, skin)
        ell(ctx, 0, -632, 90, 98)
        ink(ctx, skin)
        smooth(ctx, [(-92, -650), (-70, -720), (0, -740), (70, -720), (92, -650), (60, -690), (-60, -690)])
        ink(ctx, hair)
        rrect(ctx, -94, -690, 188, 26, 10)
        ink(ctx, hexc("#B5283C"), 3)                       # headband
        smooth(ctx, [(70, -690), (96, -780), (110, -770), (86, -690)])
        ink(ctx, hexc("#8A5A2A"), 3)                       # plain brown bird feather (not a mor-pankh)
        for side in (-1, 1):
            eye(ctx, side * 32, -636, 20, 22, t, look=(0.3, 0), iris=hexc("#2A1408"), seed=9)
            line(ctx, [(side * 12, -664), (side * 50, -668)], hair, 7)
        smooth(ctx, [(-60, -600), (60, -600), (44, -548), (0, -536), (-44, -548)])
        ink(ctx, hair)                                     # short beard
        ctx.move_to(-14, -592)
        ctx.curve_to(-4, -584, 4, -584, 14, -592)
        ctx.set_line_width(4)
        rgba(ctx, hexc("#E8B0A0"))
        ctx.stroke()
        h1 = (lerp(top[0], bot[0], 0.32), lerp(top[1], bot[1], 0.32))
        h2 = (lerp(top[0], bot[0], 0.52), lerp(top[1], bot[1], 0.52))
        limb(ctx, [(-112, -490), (-130, -430), h1], skin, 36)
        hand(ctx, *h1, skin, 22)
        limb(ctx, [(112, -490), (150, -420), h2], skin, 36)
        hand(ctx, *h2, skin, 22)
        ctx.restore()
    group(ctx, a, draw)


def naav(ctx, cx, wy, t):
    """Wooden boat hull drawn in front of the people standing in it (feet hidden)."""
    bob = 6 * math.sin(t * 2.4)
    y = wy + bob
    smooth(ctx, [(cx - 470, y - 170), (cx - 380, y - 80), (cx, y - 70), (cx + 380, y - 80), (cx + 470, y - 170),
                 (cx + 400, y + 10), (cx, y + 40), (cx - 400, y + 10)])
    ink(ctx, hexc("#7A4A22"), 5)
    for k in range(3):
        yy = y - 50 + k * 28
        line(ctx, [(cx - 400 + k * 20, yy - 4), (cx, yy + 6), (cx + 400 - k * 20, yy - 4)], hexc("#4A2A12"), 3)
    line(ctx, [(cx - 460, y - 166), (cx - 380, y - 82), (cx, y - 72), (cx + 380, y - 82), (cx + 460, y - 166)],
         GOLD, 6)
    for i in range(10):                                   # wake ripples
        xx = cx - 480 - i * 30 + (t * 60) % 30
        line(ctx, [(xx - 20, y + 30 + i * 4), (xx + 20, y + 30 + i * 4)], hexc("#FFE0B8"), 3, 0.5 - i * 0.04)


def pushpak(ctx, x, y, s, t, part="all", a=1.0):
    """Pushpak Viman: golden flying temple-chariot. part = all | back (canopy) | front (deck, wings, clouds)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    flap = math.sin(t * 5)
    if part in ("all", "back"):
        glow(ctx, 0, -200, 520, FLY_GOLD, 0.35 * a)
    if part == "all":
        for px in (-240, 240):
            rrect(ctx, px - 18, -420, 36, 420, 10)
            ink(ctx, GOLD, 4, a)
        ctx.move_to(-260, -400)
        ctx.curve_to(-260, -560, 260, -560, 260, -400)
        ctx.line_to(260, -420)
        ctx.line_to(-260, -420)
        ctx.close_path()
        ink(ctx, hexc("#E9B640"), 4, a)
        smooth(ctx, [(-150, -500), (-110, -600), (0, -680), (110, -600), (150, -500)])
        ink(ctx, GOLD_HI, 4, a)
        for k in range(3):
            line(ctx, [(-120 + k * 20, -520 - k * 40), (120 - k * 20, -520 - k * 40)], RED_GEM, 5, a)
        circle(ctx, 0, -700, 18, GOLD_HI, a)
        line(ctx, [(0, -716), (0, -790)], dv.OUTLINE, 4, a)
        smooth(ctx, [(0, -790), (60, -776 + 8 * flap), (0, -756)])
        ink(ctx, SAFF, 2, a)
    if part in ("all", "front"):
        for side in (-1, 1):                              # swan wings
            tip = (side * 580, -200 - 70 * flap)
            smooth(ctx, [(side * 300, -20), (side * 420, -120 - 40 * flap), tip, (side * 470, -60), (side * 330, 30)])
            ink(ctx, hexc("#FFF4D6"), 4, a)
            for k in range(4):
                fx = side * (360 + 50 * k)
                line(ctx, [(fx, -20 - 10 * k), (fx + side * 30, -90 - 30 * k - 40 * flap * (k / 3))],
                     GOLD, 4, a)
        for i in range(7):                                # cloud bed
            cx = -360 + i * 120 + 20 * math.sin(t * 2 + i)
            circle(ctx, cx, 120 + 16 * math.sin(i * 1.7), 74, hexc("#FFF8EC"), 0.8 * a)
        smooth(ctx, [(-360, 0), (360, 0), (300, 90), (0, 130), (-300, 90)])
        ink(ctx, hexc("#E0A830"), 5, a)
        for k in range(9):                                # lotus petals on the hull
            px = -280 + k * 70
            smooth(ctx, [(px - 26, 20), (px, 100 - abs(px) * 0.12), (px + 26, 20)])
            ink(ctx, hexc("#F6C8A0"), 3, a)
        rrect(ctx, -370, -24, 740, 34, 12)
        ink(ctx, GOLD_HI, 4, a)
        for k in range(7):
            gem(ctx, -300 + k * 100, -7, 9, RED_GEM if k % 2 else hexc("#00B4D8"))
    ctx.restore()


def jatayu_fly(ctx, x, y, s, t, ang=0.0, cut=0.0, a=1.0):
    """Jatayu with wings spread; cut (0..1) folds the right wing away as Ravan's blade strikes it."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    flap = math.sin(t * 9) * (1 - cut)
    for side, keep in ((-1, 1.0), (1, 1 - cut)):
        if keep <= 0.02:
            continue
        ctx.save()
        ctx.scale(s, s * keep)
        smooth(ctx, [(side * 40, -100), (side * 200, -230 - 60 * flap), (side * 330, -180 - 80 * flap),
                     (side * 260, -110), (side * 120, -70)])
        ink(ctx, hexc("#6A4212"), 4, a)
        for k in range(4):
            fx = side * (130 + 50 * k)
            line(ctx, [(fx, -90 - 8 * k), (fx + side * 20, -170 - 30 * k - 50 * flap)], hexc("#D49624"), 6, a)
        ctx.restore()
    ctx.restore()
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    jatayu_bird(ctx, 0, 0, s, t, a=a)
    ctx.restore()


def ram_stone(ctx, x, y, s, t, glow_a=0.0):
    """Floating setu stone with RAM carved on it (Roman letters: no Devanagari in Cairo)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if glow_a > 0:
        glow(ctx, 0, 0, 90, GOLD_HI, glow_a)
    smooth(ctx, [(-52, -30), (-20, -40), (40, -34), (56, 0), (36, 30), (-30, 34), (-58, 6)])
    ink(ctx, STONE, 4)
    sheen(ctx, -16, -16, 22, 10, 0.18)
    text(ctx, "RAM", 0, 2, 30, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=STONE_DK, stroke_w=3)
    ctx.restore()


def walk_bob(t, phase=0.0):
    return -abs(math.sin(t * 5.5 + phase)) * 8


# =============================================================================
# Story: 6 scenes, 62 spoken words, ~23 s (25 s HARD LOCK)
# =============================================================================
SPEC = [
    {"key": "hook", "text": "", "visual": "Ram, Sita, Lakshman leave Ayodhya; the map draws 14 years of footsteps "
                                          "to Lanka, then a golden Pushpak streaks home",
     "vo": [("punch", [("चौदह साल पैदल...", "CHAUDAH SAAL PAIDAL...")], 0.02),
            ("punch", [("और वापसी?", "AUR WAPSI?"), ("सिर्फ़ एक उड़ान में!", "SIRF EK UDAAN MEIN!")], 0.04)]},
    {"key": "ganga", "text": "", "visual": "Nishadraj rows Ram and Sita across the Ganga; route reaches Chitrakoot",
     "vo": [("tell", [("अयोध्या से निकले श्रीराम,", "AYODHYA SE NIKLE SHRI RAM,"),
                      ("निषादराज की नाव से गंगा पार,", "NISHADRAJ KI NAAV SE GANGA PAAR,")], 0.02),
            ("tell", [("फिर चित्रकूट।", "PHIR CHITRAKOOT.")], 0.04)]},
    {"key": "haran", "text": "", "visual": "Panchavati: Ravan seizes Sita, Jatayu strikes and falls; Kishkindha: "
                                           "Hanuman meets Ram with folded hands",
     "vo": [("low", [("पंचवटी में सीता हरण...", "PANCHAVATI MEIN SITA HARAN..."), ("जटायु गिरे,", "JATAYU GIRE,")], 0.02),
            ("awe", [("किष्किंधा में हनुमान मिले।", "KISHKINDHA MEIN HANUMAN MILE.")], 0.04)]},
    {"key": "setu", "text": "", "visual": "Rameshwaram: Hanuman lifts a RAM stone, the setu races across the sea "
                                          "with a golden pulse",
     "vo": [("build", [("रामेश्वरम में सागर पर सेतु—", "RAMESHWARAM MEIN SAAGAR PAR SETU—"),
                       ("पाँच दिन में सौ योजन!", "PAANCH DIN MEIN SAU YOJAN!")], 0.04)]},
    {"key": "vadh", "text": "", "visual": "Lanka: Ram releases the arrow, Ravan dissolves into light; the Pushpak "
                                          "descends",
     "vo": [("fast", [("लंका में रावण वध...", "LANKA MEIN RAVAN VADH..."),
                      ("और फिर पुष्पक विमान!", "AUR PHIR PUSHPAK VIMAN!")], 0.04)]},
    {"key": "loop", "text": "", "visual": "Ram, Sita, Lakshman ride the Pushpak through the clouds; the golden "
                                          "flight line lands on Ayodhya and loops to the hook",
     "vo": [("awe", [("हज़ारों किलोमीटर का सफ़र,", "HAZARON KILOMETER KA SAFAR,"),
                     ("एक ही उड़ान में पूरा...", "EK HI UDAAN MEIN POORA...")], 0.02),
            ("whisper", [("क्योंकि शुरुआत हुई थी—", "KYUNKI SHURUAAT HUI THI—")], 0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "CHAUDAH": SAFFRON_PATH, "PAIDAL": SAFFRON_PATH, "UDAAN": FLY_GOLD, "WAPSI?": FLY_GOLD,
    "AYODHYA": GOLD_HI, "RAM,": GOLD_HI, "NISHADRAJ": hexc("#E0B080"), "GANGA": hexc("#8FD0FF"),
    "CHITRAKOOT.": hexc("#9BE07A"), "PANCHAVATI": hexc("#9BE07A"), "SITA": hexc("#FF8A8A"),
    "HARAN...": hexc("#FF5A5A"), "JATAYU": hexc("#FFB347"), "KISHKINDHA": hexc("#FFB347"),
    "HANUMAN": hexc("#FFAA48"), "RAMESHWARAM": hexc("#8FD0FF"), "SETU—": GOLD_HI, "PAANCH": GOLD_HI,
    "SAU": GOLD_HI, "YOJAN!": GOLD_HI, "LANKA": hexc("#FF6A4A"), "RAVAN": hexc("#FF5A5A"),
    "PUSHPAK": FLY_GOLD, "VIMAN!": FLY_GOLD, "HAZARON": SAFFRON_PATH, "SHURUAAT": GOLD_HI,
})


def fade_in_out(ctx, t, d, start_glow=0.0, end_glow=0.0):
    """Golden wash at the scene edges (the loop scene ends in gold and the hook starts in it)."""
    if start_glow and t < start_glow:
        glow(ctx, W / 2, H * 0.4, 1300, (1, 0.9, 0.6), 0.85 * (1 - t / start_glow))
    if end_glow and t > d - end_glow:
        glow(ctx, W / 2, H * 0.4, 1300, (1, 0.9, 0.6), 0.85 * (t - (d - end_glow)) / end_glow)


class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"wapsi": c("WAPSI", d * 0.4), "udaan": c("UDAAN", d * 0.62)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["wapsi"], "ghanti"), (b["udaan"], "whoosh"), (b["udaan"] + 0.15, "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        scenery(ctx, t, "ayodhya")
        walk = ease_in_out(clamp(t / max(0.6, b["wapsi"] - 0.05)))
        fly = ease_in_out(clamp((t - b["udaan"]) / max(0.4, d - b["udaan"] - 0.1)))
        india_map(ctx, t, walk=walk, fly=fly)
        lakshman(ctx, 850, GROUND - 10 + walk_bob(t, 1.2), 0.70, t, pose="bow")
        sita(ctx, 545, GROUND - 10 + walk_bob(t, 0.6), 0.70, t, pose="walk", look=(0.0, -0.3) if fly > 0 else (0, 0))
        shri_ram(ctx, 235, GROUND - 10 + walk_bob(t), 0.72, t, pose="bow", flip=True)
        if fly > 0:
            dv.petals(ctx, t, n=30, seed=4, a=min(1.0, fly * 2))
        fade_in_out(ctx, t, d, start_glow=0.3)


class Ganga(Cued):
    def beats(self, d):
        c = self.cue
        return {"nishad": c("NISHADRAJ", d * 0.3), "chitra": c("CHITRAKOOT", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(b["nishad"], "whoosh"), (b["chitra"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        scenery(ctx, t, "ganga")
        if t < b["nishad"]:
            walk = lerp(0.0, U[1], ease_in_out(clamp(t / max(0.3, b["nishad"]))))
        else:
            walk = lerp(U[1], U[CHITRAKOOT], ease_in_out(clamp((t - b["nishad"]) / max(0.3, b["chitra"] + 0.5 - b["nishad"]))))
        india_map(ctx, t, walk=walk, ping=CHITRAKOOT, ping_u=clamp((t - b["chitra"]) / 0.8))
        cx = lerp(470, 560, ease_in_out(clamp(t / d)))
        nishadraj(ctx, cx - 280, GROUND - 10, 0.68, t, flip=True)
        shri_ram(ctx, cx + 20, GROUND - 10, 0.70, t, pose="bless", flip=True)
        sita(ctx, cx + 290, GROUND - 10, 0.68, t, pose="namaste")
        naav(ctx, cx, GROUND - 40, t)


class Haran(Cued):
    def beats(self, d):
        c = self.cue
        return {"jatayu": c("JATAYU", d * 0.35), "hanu": c("KISHKINDHA", d * 0.62)}

    def events(self, d):
        b = self.beats(d)
        fall = lerp(b["jatayu"], b["hanu"], 0.45)
        return [(0.03, "thud"), (b["jatayu"], "whoosh"), (fall, "thud"), (b["hanu"], "ghanti"),
                (b["hanu"] + 0.1, "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        if t < b["jatayu"]:
            walk = lerp(U[CHITRAKOOT], U[PANCHAVATI], ease_in_out(clamp(t / max(0.3, b["jatayu"]))))
        else:
            walk = lerp(U[PANCHAVATI], U[KISHKINDHA], ease_in_out(clamp((t - b["jatayu"]) / max(0.3, b["hanu"] + 0.4 - b["jatayu"]))))
        if t >= b["hanu"]:                                # Kishkindha: Hanuman meets Shri Ram
            scenery(ctx, t, "kishkindha")
            india_map(ctx, t, walk=walk, ping=KISHKINDHA, ping_u=clamp((t - b["hanu"]) / 0.8))
            dv.petals(ctx, t, n=26, seed=9, a=0.85)
            u = ease_out_cubic(clamp((t - b["hanu"]) / 0.5))
            shri_ram(ctx, 250, GROUND - 10, 0.72, t, pose="bless", flip=True)
            hanuman(ctx, lerp(900, 800, u), GROUND - 10, 0.70, t, pose="namaste", flip=False)
            return
        scenery(ctx, t, "forest")
        india_map(ctx, t, walk=walk, ping=PANCHAVATI, ping_u=clamp(t / 0.8))
        if t < b["jatayu"]:                               # Ravan closes in on Sita
            u = ease_out_cubic(clamp(t / max(0.3, b["jatayu"])))
            sita(ctx, lerp(250, 290, u), GROUND - 10, 0.70, t, pose="fear", look=(0.5, 0))
            ravan(ctx, lerp(900, 720, u), GROUND - 10, 0.72, t, pose="abduct")
            return
        span = max(0.4, b["hanu"] - b["jatayu"])
        u = (t - b["jatayu"]) / span
        sita(ctx, 520, GROUND - 10, 0.70, t, pose="reach", look=(-0.5, -0.4), flip=True)
        ravan(ctx, 820, GROUND - 10, 0.72, t, pose="sword")
        if u < 0.45:                                      # Jatayu swoops in high, over Sita, at Ravan's heads
            k = ease_out_cubic(u / 0.45)
            jatayu_fly(ctx, lerp(-160, 650, k), lerp(470, 640, k), 0.6, t, ang=0.12)
        else:                                             # struck: one wing gone, he falls to the left
            k = ease_in_out(clamp((u - 0.45) / 0.4))
            jx, jy = lerp(650, 230, k), lerp(640, GROUND - 20, k)
            jatayu_fly(ctx, jx, jy, 0.62, t, ang=lerp(0.15, -0.5, k), cut=min(1.0, k * 2))
            for i in range(14):                           # golden feathers drifting
                fu = (t - b["jatayu"] + rnd(i, 61)) % 1.5
                circle(ctx, 650 - 260 * rnd(i, 62) + 30 * math.sin(t * 3 + i), 620 + fu * 380, 6,
                       hexc("#F0B842"), 0.9 * (1 - fu / 1.5))


class Setu(Cued):
    def beats(self, d):
        c = self.cue
        return {"paanch": c("PAANCH", d * 0.5)}

    def events(self, d):
        b = self.beats(d)
        return [(0.25, "thud"), (b["paanch"] * 0.6, "thud"), (b["paanch"], "boom"), (b["paanch"] + 0.1, "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        scenery(ctx, t, "ocean")
        if t < b["paanch"]:
            walk = lerp(U[KISHKINDHA], U[RAMESHWARAM], ease_in_out(clamp(t / max(0.3, b["paanch"]))))
        else:
            walk = lerp(U[RAMESHWARAM], U[LANKA], ease_in_out(clamp((t - b["paanch"]) / max(0.3, d - b["paanch"] - 0.2))))
        india_map(ctx, t, walk=walk, ping=LANKA, ping_u=clamp((t - d + 0.6) / 0.6))
        pulse = clamp(1 - (t - b["paanch"]) / 0.9) if t >= b["paanch"] else 0.0
        prog = ease_out_cubic(clamp(t / (b["paanch"] + 0.4)))
        n = 11
        for i in range(n):                                 # the setu races out across the sea
            if i / n > prog:
                break
            sx = 330 + i * 62
            ram_stone(ctx, sx, GROUND - 4 + 5 * math.sin(t * 2 + i), 0.95, t, glow_a=0.8 * pulse)
        smooth(ctx, [(760, GROUND + 30), (790, GROUND - 40), (900, GROUND - 50), (940, GROUND + 30)])
        ink(ctx, STONE_DK, 4)                              # rock Hanuman stands on
        shri_ram(ctx, 200, GROUND - 10, 0.72, t, pose="bless", flip=True)
        hanuman(ctx, 850, GROUND - 10, 0.70, t, pose="lift_rock", flip=False)
        ram_stone(ctx, 850, 632, 1.9, t, glow_a=0.5 + 0.3 * math.sin(t * 4))
        if pulse > 0:
            glow(ctx, 600, GROUND - 10, 520, GOLD_HI, 0.5 * pulse)


class Vadh(Cued):
    def beats(self, d):
        c = self.cue
        push = c("PUSHPAK", d * 0.52)
        shoot = max(0.3, push * 0.42)
        return {"shoot": shoot, "hit": shoot + 0.32, "push": push}

    def events(self, d):
        b = self.beats(d)
        return [(b["shoot"] - 0.05, "arrow"), (b["hit"], "boom"), (b["push"], "shimmer"), (b["push"] + 0.1, "whoosh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        scenery(ctx, t, "lanka")
        if t >= b["push"]:                                 # the Pushpak descends behind the map
            k = ease_out_cubic(clamp((t - b["push"]) / 0.9))
            pushpak(ctx, 760, lerp(560, 960, k), 0.5, t, part="all", a=k)
        india_map(ctx, t, walk=1.0, ping=LANKA, ping_u=clamp((t - b["hit"]) / 0.9))
        if t >= b["push"]:
            vimana_icon(ctx, *WALK[LANKA], 1.0)
        # Ram: aim -> release (string relaxed) -> blessing
        if t < b["shoot"]:
            shri_ram(ctx, 250, GROUND - 10, 0.72, t, pose="aim", flip=True)
        elif t < b["hit"] + 0.4:
            shri_ram(ctx, 250, GROUND - 10, 0.72, t, pose="shot", flip=True)
        else:
            shri_ram(ctx, 250, GROUND - 10, 0.72, t, pose="bless", flip=True)
        fall = clamp((t - b["hit"]) / 0.9)
        if fall < 1:
            ravan(ctx, 830, GROUND - 10, 0.72, t, pose="hit" if t >= b["hit"] else "sword", a=1 - fall, fall=fall)
        if b["shoot"] <= t < b["hit"]:                    # arrow in flight, head forward, true heading
            x0, y0 = 250 + 330 * 0.72, GROUND - 10 - 450 * 0.72
            x1, y1 = 790, GROUND - 10 - 470 * 0.72
            k = (t - b["shoot"]) / (b["hit"] - b["shoot"])
            dv.divine_arrow(ctx, lerp(x0, x1, k), lerp(y0, y1, k), math.atan2(y1 - y0, x1 - x0), 190 * 0.72, t,
                            trail=1.0)
        if 0 < fall < 1:                                  # his light rises (no gore)
            for i in range(24):
                rise = (fall + rnd(i, 71)) % 1
                circle(ctx, 830 + 160 * (rnd(i, 72) - 0.5), GROUND - 200 - rise * 500, 4 + 4 * rnd(i, 73),
                       FLY_GOLD, 0.9 * (1 - rise))
        flash(ctx, t - b["hit"], dur=0.45)


class Loop(Cued):
    def beats(self, d):
        c = self.cue
        return {"kyunki": c("KYUNKI", d * 0.78)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "whoosh"), (b["kyunki"] - 0.1, "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        scenery(ctx, t, "sky")
        fly = ease_in_out(clamp(t / max(0.6, b["kyunki"] + 0.2)))
        home = clamp((t - b["kyunki"]) / 0.6)
        pushpak(ctx, 540, GROUND - 10, 0.92, t, part="back")
        india_map(ctx, t, walk=1.0, fly=fly, home=home)
        bob = 8 * math.sin(t * 2.2)
        sita(ctx, 300, GROUND - 10 + bob, 0.68, t, pose="namaste")
        shri_ram(ctx, 540, GROUND - 10 + bob, 0.72, t, pose="bless", flip=False)
        lakshman(ctx, 780, GROUND - 10 + bob, 0.68, t, pose="namaste")
        pushpak(ctx, 540, GROUND - 10 + bob, 0.92, t, part="front")
        fade_in_out(ctx, t, d, end_glow=0.3)


SCENE_CLASSES = {"hook": Hook, "ganga": Ganga, "haran": Haran, "setu": Setu, "vadh": Vadh, "loop": Loop}

UPLOAD = {
    "titles": [
        "14 Saal Paidal, Wapsi Ek Udaan Mein! 🏹 Shri Ram Ka Poora Safar 1 Map Par #shorts",
        "Ayodhya Se Lanka: Shri Ram Ka 14 Saal Ka Raasta Ek Map Par #shorts",
        "Ram Setu 5 Din Mein? Shri Ram Ke Safar Ka Poora Naksha #shorts",
        "Pushpak Viman Ne 14 Saal Ka Raasta Ek Udaan Mein Kaise Tay Kiya? #shorts",
        "Shri Ram Van Gaman Path: Ayodhya, Chitrakoot, Panchavati, Lanka #shorts",
    ],
    "thumb_text": "14 SAAL PAIDAL",
    "queries": [
        "shri ram van gaman path map",
        "ayodhya se lanka shri ram ka raasta",
        "ram setu kitne din mein bana",
    ],
    "description": """
Shri Ram van gaman path ka map: Ayodhya se Lanka ka raasta, 14 saal paidal aur wapsi ek udaan mein! 🏹
Ram Setu kitne din mein bana? Valmiki ke anusaar sirf 5 din mein!
Shringverpur mein Nishadraj ki naav, Chitrakoot, Panchavati mein Sita haran, Jatayu ka balidan,
Kishkindha mein Hanuman ji se milan, Rameshwaram mein 5 din mein 100 yojan ka Ram Setu, Lanka vijay
aur phir Pushpak Viman se Ayodhya. Shri Ram ka poora safar ek map par.

Source: Valmiki Ramayana (Ayodhya, Aranya, Kishkindha aur Yuddha Kanda). Setu ke 5 din: Yuddha Kanda 22.
Van Gaman Path ke sthaan parampara se maane jaate hain; doori Valmiki mein nahi likhi.

Comment mein likhiye: JAI SHRI RAM 🚩
""",
    "tags": [
        "shri ram", "ram van gaman path", "ayodhya to lanka", "ram setu", "pushpak viman", "ramayan",
        "valmiki ramayana", "jai shri ram", "divya rahasya", "sanatan katha", "shorts",
    ],
    "hashtags": ["#Shorts", "#JaiShriRam", "#Ramayan"],
}


def thumbnail(ctx):
    scenery(ctx, 0.4, "ayodhya")
    india_map(ctx, 1.0, walk=1.0, fly=0.85)
    shri_ram(ctx, 250, GROUND - 10, 0.76, 0.5, pose="bow", flip=True)
    pushpak(ctx, 790, GROUND - 40, 0.42, 0.5, part="all")
    text(ctx, "14 SAAL PAIDAL", 540, 1330, 118, SAFFRON_PATH, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
         stroke_w=18)
    text(ctx, "WAPSI 1 UDAAN!", 540, 1470, 110, FLY_GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
         stroke_w=18)
