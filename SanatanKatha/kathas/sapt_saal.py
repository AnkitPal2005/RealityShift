"""Sapt Saal: Ek Teer, 7 Ped, 1 Pahaad... Phir Wapas Ram Ji Ke Paas! (~21s, six scenes).

Usage (from SanatanKatha/):
  python make.py sapt_saal --preview       # contact sheet + thumbnail
  python make.py sapt_saal --kiki-split    # cut the narrator voice into line clips (Whisper anchored)
  python make.py sapt_saal                 # final render from the user's KikiVoice clips

Rahasya (Valmiki Ramayana, Kishkindha Kanda 12.3-4):
Sugriv doubted that Shri Ram could defeat Bali. Ram loosed one arrow: it pierced seven sala trees and the
mountain slope, entered the earth, and in a moment came back into his own quiver.

Layout: side view of Kishkindha. Ram on the left, seven sal trees in a receding row with the mountain behind;
the arrow's flight is the whole show. The last line ("kyunki ye tha bas...") loops into the hook ("ek teer...").
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

from kathas.ram_hanuman import shri_ram          # royal mukut, Kodanda, poses bow/aim/shot/bless
from kathas.hanumad_ramayana import hanuman      # poses namaste/abhaya

TOPIC = "SHRI RAM SAPT SAAL BHEDAN EK BAAN SUGRIV KA SHAK"
OUTPUTS = {"edge": "sapt_saal_short.mp4"}
MUSIC_STYLE = "ambient"   # previous Short (ram_van_gaman) used divine: rotate
MUSIC_BPM = 90            # >= 6 BPM away from ram_van_gaman (84)
MUSIC_VOLUME = 0.11
TAIL_PAD = 0.04
MAX_GAP = 0.04

WHITE = (1.0, 1.0, 1.0)
RED_GEM = hexc("#D61F3A")
ARROW_Y = GROUND - 10 - 450 * 0.72          # Ram's arrow height (aim pose, scale 0.72)
BOW_X = 230 + 330 * 0.72                     # arrow head when nocked (Ram at x 230, flipped)
TREES = [(505, 1.0), (572, 0.95), (639, 0.9), (706, 0.85), (773, 0.8), (840, 0.75), (905, 0.7)]
TREE_BASE = 1080
PEAK = (995, 560)
MOUNT_X = 985
QUIVER = (176, 806)                          # on Ram's back
QUIVER_MOUTH = (150, 706)

SOURCES = [
    "Valmiki Ramayana, Kishkindha Kanda 12.3-4: the arrow pierces seven sala trees and the mountain slope, "
    "enters the earth and in a moment returns to Shri Ram's quiver.",
    "Valmiki Ramayana, Kishkindha Kanda 11: Sugriv's doubt about Bali's strength, the test Ram agrees to.",
    "Ramcharitmanas, Kishkindha Kanda: Tulsidas tells the same test with seven taal trees; the script follows "
    "Valmiki and just says 'saat bahut bade ped'.",
]


# =============================================================================
# Scenery and props
# =============================================================================
def kishkindha_bg(ctx, t, dusk=0.0):
    """Rocky Kishkindha at golden hour: sun low behind the hills, layered boulders, dry grass, dust."""
    dv.sky(ctx, hexc("#2A1A4A"), hexc("#D0603A") if not dusk else hexc("#8A3046"), hexc("#FFC46A"), 0.6)
    dv.sun_disc(ctx, 700, 560, 70, t, a=0.9, rays=16)
    for k in range(6):                                    # birds
        bx = (200 + k * 140 + t * 40) % (W + 100) - 50
        by = 360 + 30 * math.sin(k * 1.7)
        line(ctx, [(bx - 14, by - 6), (bx, by), (bx + 14, by - 6)], hexc("#3A1A2A"), 3, 0.7)
    for k, (yy, c, amp) in enumerate(((900, "#6A3448", 60), (980, "#4A2234", 40))):
        ctx.move_to(0, yy)
        for x in range(0, W + 1, 30):
            ctx.line_to(x, yy - amp * abs(math.sin(x / 150 + k)) - 14 * math.sin(x / 47))
        ctx.line_to(W, H)
        ctx.line_to(0, H)
        ctx.close_path()
        rgba(ctx, hexc(c))
        ctx.fill()
    for i, (x, r) in enumerate(((60, 80), (330, 50), (1040, 70), (700, 40))):
        ell(ctx, x, 1060 - r * 0.5, r * 1.3, r)
        ink(ctx, hexc("#7A4228"), 3)
        sheen(ctx, x - r * 0.3, 1060 - r * 0.9, r * 0.4, r * 0.25, 0.15)
    ctx.rectangle(0, GROUND - 25, W, H)
    rgba(ctx, hexc("#3A2014"))
    ctx.fill()
    for i in range(40):
        x = rnd(i, 9) * W
        y = GROUND - 14 + 50 * rnd(i, 10)
        line(ctx, [(x, y), (x - 6, y - 22)], hexc("#A07A3A"), 4, 0.8)
        line(ctx, [(x, y), (x + 6, y - 20)], hexc("#A07A3A"), 4, 0.8)
    for i in range(24):
        x = (rnd(i, 3) * W + t * 30 * (0.4 + rnd(i, 4))) % W
        y = 600 + 560 * rnd(i, 5) + 12 * math.sin(t * 1.5 + i)
        circle(ctx, x, y, 2 + 3 * rnd(i, 6), hexc("#FFE2A8"), 0.25 + 0.2 * math.sin(t * 2 + i))


def mountain(ctx, t, crack=0.0):
    smooth(ctx, [(800, TREE_BASE + 10), (880, 760), PEAK, (1070, 700), (1120, TREE_BASE + 10)], k=0.08)
    ink(ctx, hexc("#5A3A30"), 4)
    for k in range(4):                                    # rock strata
        y = 700 + 90 * k
        line(ctx, [(900 + 10 * k, y), (1060, y - 30)], hexc("#3A241E"), 3, 0.7)
    if crack > 0:
        pts = [(MOUNT_X, ARROW_Y), (MOUNT_X + 24, ARROW_Y - 60), (MOUNT_X + 6, ARROW_Y - 120), (MOUNT_X + 30, ARROW_Y - 190),
               (MOUNT_X + 14, ARROW_Y - 260)]
        n = max(2, int(len(pts) * min(1.0, crack * 1.5)))
        line(ctx, pts[:n], GOLD_HI, 8, min(1.0, crack * 2))
        line(ctx, [(MOUNT_X, ARROW_Y), (MOUNT_X - 30, ARROW_Y + 70), (MOUNT_X - 10, ARROW_Y + 150)][:n], GOLD_HI, 6,
             min(1.0, crack * 2))
        glow(ctx, MOUNT_X, ARROW_Y, 120, GOLD_HI, 0.7 * min(1.0, crack * 2))


def sal_tree(ctx, x, s, t, hole=0.0, shake=0.0):
    """Tall sal tree, trunk foot at (x, TREE_BASE). hole (0..1) = the arrow's glowing hole at ARROW_Y."""
    ctx.save()
    ctx.translate(x, TREE_BASE)
    ctx.scale(s, s)
    ctx.rotate(0.03 * shake * math.sin(t * 40))
    smooth(ctx, [(-24, 0), (-18, -300), (-13, -450), (13, -450), (18, -300), (24, 0)], k=0.1)
    ink(ctx, hexc("#6E4524"), 4)
    line(ctx, [(0, -300), (-60, -380)], hexc("#6E4524"), 8)
    line(ctx, [(0, -340), (56, -410)], hexc("#6E4524"), 8)
    sway = 6 * math.sin(t * 1.4 + x)
    tint = 0.85 + 0.3 * ((int(x) // 67) % 2)             # alternate shades so each tree reads on its own
    for dx, dy, r, c in ((0, -470, 56, "#2E5A2A"), (-34, -520, 44, "#2A5226"), (34, -520, 44, "#2A5226"),
                         (0, -580, 48, "#3A6A30"), (-20, -640, 36, "#4A7A36"), (18, -660, 32, "#4A7A36")):
        circle(ctx, dx + sway, dy, r, shade(hexc(c), tint))
        ctx.arc(dx + sway, dy, r, 0, math.tau)
        rgba(ctx, dv.OUTLINE, 0.5)
        ctx.set_line_width(3)
        ctx.stroke()
        circle(ctx, dx + sway - r * 0.3, dy - r * 0.3, r * 0.4, hexc("#6A9A46"), 0.35)
    ctx.restore()
    if hole > 0:
        glow(ctx, x, ARROW_Y, 60, GOLD_HI, 0.9 * hole)
        circle(ctx, x, ARROW_Y, 9, hexc("#FFF4C8"), hole)
        for k in range(6):
            ang = k / 6 * math.tau + t * 3
            circle(ctx, x + 22 * math.cos(ang), ARROW_Y + 22 * math.sin(ang), 3, GOLD_HI, 0.8 * hole)


def all_trees(ctx, t, holes, shake=0.0):
    for i in reversed(range(len(TREES))):                 # far trees first
        x, s = TREES[i]
        sal_tree(ctx, x, s, t, hole=holes[i], shake=shake if holes[i] > 0.5 else 0.0)


def quiver(ctx, t, glow_a=0.0):
    """Ram's quiver, drawn before Ram so it sits on his back."""
    ctx.save()
    ctx.translate(*QUIVER)
    ctx.rotate(-0.35)
    if glow_a > 0:
        glow(ctx, 0, -100, 110, GOLD_HI, glow_a)
    for k in range(3):
        line(ctx, [(-12 + 12 * k, -110), (-12 + 12 * k, -150)], hexc("#F3E2BC"), 5)
        smooth(ctx, [(-12 + 12 * k, -150), (-20 + 12 * k, -176), (-4 + 12 * k, -176)])
        ink(ctx, RED_GEM, 2)
    rrect(ctx, -24, -120, 48, 220, 12)
    ink(ctx, hexc("#7A4A1E"), 4)
    line(ctx, [(-24, -100), (24, -100)], GOLD, 6)
    line(ctx, [(-24, 80), (24, 80)], GOLD, 6)
    ctx.restore()


def bali_shadow(ctx, x, y, s, t, a=1.0):
    """Bali far away on the hill: a dark vanar silhouette with a gada and red eyes."""
    if a <= 0:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    glow(ctx, 0, -420, 360, hexc("#B01E2A"), 0.45 * a)
    c = hexc("#160810")
    ell(ctx, 0, -300, 150, 200)
    rgba(ctx, c, a)
    ctx.fill()
    ell(ctx, 0, -560, 95, 100)
    rgba(ctx, c, a)
    ctx.fill()
    ctx.move_to(-100, -620)
    for k, px in enumerate((-100, -70, -50, -25, 0, 25, 50, 70, 100)):
        ctx.line_to(px, -650 if k % 2 == 0 else -700)
    ctx.line_to(100, -620)
    ctx.close_path()
    rgba(ctx, c, a)
    ctx.fill()
    circle(ctx, 0, -690, 10, hexc("#FF3A2A"), 0.6 * a)
    for fx in (-70, 70):
        ctx.rectangle(fx - 30, -140, 60, 140)
        rgba(ctx, c, a)
        ctx.fill()
    line(ctx, [(120, -380), (230, -520), (260, -700)], c, 40, a)
    circle(ctx, 268, -760, 70, c, a)                      # gada head
    limb(ctx, [(-50, -150), (-200, -260), (-260, -420), (-200, -540)], c, 34)   # tail
    for side in (-1, 1):
        circle(ctx, side * 32, -570, 11, hexc("#FF3A2A"), a * (0.8 + 0.2 * math.sin(t * 8)))
    ctx.restore()


def arrow_at(ctx, x, y, ang, t, a=1.0, trail=1.0):
    dv.divine_arrow(ctx, x, y, ang, 190 * 0.72, t, a=a, trail=trail)


def bez(p0, p1, p2, p3, u):
    v = 1 - u
    x = v ** 3 * p0[0] + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u ** 3 * p3[0]
    y = v ** 3 * p0[1] + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u ** 3 * p3[1]
    dx = 3 * v * v * (p1[0] - p0[0]) + 6 * v * u * (p2[0] - p1[0]) + 3 * u * u * (p3[0] - p2[0])
    dy = 3 * v * v * (p1[1] - p0[1]) + 6 * v * u * (p2[1] - p1[1]) + 3 * u * u * (p3[1] - p2[1])
    return x, y, math.atan2(dy, dx)


RETURN = ((MOUNT_X, TREE_BASE + 20), (1030, 300), (220, 260), QUIVER_MOUTH)


def return_flight(ctx, t, u):
    """Arrow comes out of the ground, sweeps across the sky and drops into Ram's quiver (u 0..1)."""
    if u <= 0 or u >= 1:
        return
    x, y, ang = bez(*RETURN, ease_in_out(u))
    for k in range(10):                                   # golden spiral trail
        uu = ease_in_out(max(0.0, u - k * 0.02))
        tx, ty, _ = bez(*RETURN, uu)
        circle(ctx, tx + 10 * math.cos(t * 14 + k), ty + 10 * math.sin(t * 14 + k), 7 - k * 0.5, GOLD_HI,
               0.7 * (1 - k / 10))
    arrow_at(ctx, x, y, ang, t, a=1.0 if u < 0.92 else (1 - u) / 0.08)


# =============================================================================
# Sugriv: vanar king of Kishkindha (golden-brown fur, teal dhoti, three-point king's crown)
# =============================================================================
FUR = hexc("#C98A3A")
FUR_DK = hexc("#6A3C14")
FACE = hexc("#EBC28A")


def _sugriv_face(ctx, t, pose):
    ell(ctx, 0, -620, 92, 96)
    ink(ctx, FUR)
    ell(ctx, 0, -600, 70, 66)
    ink(ctx, FACE, 0)
    smooth(ctx, [(-40, -586), (40, -586), (34, -540), (0, -530), (-34, -540)])
    ink(ctx, shade(FACE, 1.08))
    ell(ctx, 0, -578, 14, 8)
    ink(ctx, FUR_DK, 2)
    if pose == "sharan":
        for side in (-1, 1):
            eye(ctx, side * 32, -622, 20, 22, t, closed=True)
        line(ctx, [(-14, -550), (0, -545), (14, -550)], hexc("#7A2A1A"), 4)
        return
    wide = pose in ("fear", "wonder")
    look = {"fear": (0.6, 0.1), "doubt": (-0.5, 0.0), "wonder": (-0.6, -0.6)}.get(pose, (0, 0))
    for side in (-1, 1):
        eye(ctx, side * 32, -622, 20, 27 if wide else 22, t, look=look, iris=hexc("#3A1A08"), seed=4,
            lid=0.35 if pose == "doubt" and side > 0 else 0.0, skin=FACE)
        if pose == "fear":
            line(ctx, [(side * 12, -660), (side * 50, -650)], FUR_DK, 6)
        elif pose == "doubt":
            line(ctx, [(side * 12, -656 - (10 if side < 0 else 0)), (side * 50, -660 - (14 if side < 0 else 0))],
                 FUR_DK, 6)
        else:
            line(ctx, [(side * 12, -664), (side * 34, -674), (side * 52, -666)], FUR_DK, 6)
    if pose == "fear":                                     # wobbly worried mouth
        line(ctx, [(-18, -548), (-9, -553), (0, -547), (9, -553), (18, -548)], hexc("#7A2A1A"), 4)
    elif pose == "wonder":
        ell(ctx, 0, -548, 12, 15)
        ink(ctx, hexc("#5A1A10"), 3)
    else:
        line(ctx, [(-16, -550), (14, -546)], hexc("#7A2A1A"), 4)


def _sugriv_crown(ctx):
    smooth(ctx, [(-66, -690), (-58, -762), (-28, -722), (0, -792), (28, -722), (58, -762), (66, -690), (0, -702)],
           k=0.05)
    ink(ctx, GOLD, 4)
    rrect(ctx, -70, -696, 140, 18, 6)
    ink(ctx, GOLD_HI, 3)
    gem(ctx, 0, -744, 9, hexc("#2EA05A"))


def sugriv(ctx, x, y, s, t, pose="fear", flip=False, a=1.0):
    """Sugriv faces left (towards Ram) when not flipped. pose: fear | doubt | wonder | sharan (kneeling bow)."""
    def draw():
        jit = 3 * math.sin(t * 38) if pose == "fear" else 0.0
        place(ctx, x + jit, y, s, t, flip)
        if pose == "sharan":
            limb(ctx, [(150, -170), (220, -280), (230, -420), (180, -480)], FUR, 26)       # tail
            limb(ctx, [(190, -24), (-10, -32)], FUR, 46)                                  # shin on the ground
            ell(ctx, 210, -18, 36, 16)
            ink(ctx, FUR)
            limb(ctx, [(-10, -40), (90, -170)], FUR, 58)                                  # thigh
            ell(ctx, 70, -160, 104, 78, 0.3)
            ink(ctx, hexc("#1F7A7A"))
            line(ctx, [(0, -110), (150, -200)], GOLD, 8)
            ell(ctx, -40, -250, 136, 82, 0.38)
            ink(ctx, FUR)
            ell(ctx, -60, -228, 70, 40, 0.38)
            ink(ctx, FACE, 0)
            for k in range(7):                                                            # garland
                circle(ctx, -110 + k * 26, -210 + 10 * math.sin(k), 8, hexc("#E8452A") if k % 2 else GOLD)
            for dy in (0, 26):                                                            # arms to the feet
                limb(ctx, [(-120, -290 + dy), (-230, -170 + dy * 0.5), (-330, -50)], FUR, 32)
            circle(ctx, -338, -46, 22, FUR)
            ctx.save()
            ctx.translate(-250, -270)
            ctx.rotate(-0.75)
            ctx.translate(0, 600)
            ell(ctx, 0, -632, 112, 108)
            ink(ctx, FUR_DK)
            _sugriv_face(ctx, t, "sharan")
            _sugriv_crown(ctx)
            ctx.restore()
            ctx.restore()
            return
        limb(ctx, [(50, -300), (170, -420), (210, -560), (160, -650), (120, -630)], FUR, 26)  # tail
        ell(ctx, 0, -630, 112, 108)
        ink(ctx, FUR_DK)
        for fx in (-46, 46):
            ell(ctx, fx, -14, 42, 17)
            ink(ctx, FUR)
        smooth(ctx, [(-112, -340), (112, -340), (128, -200), (140, -44), (56, -32), (0, -60), (-56, -32),
                     (-140, -44), (-128, -200)])
        ink(ctx, hexc("#1F7A7A"))
        line(ctx, [(138, -48), (56, -36), (0, -64), (-56, -36), (-138, -48)], GOLD, 10)
        smooth(ctx, [(-118, -490), (-60, -514), (60, -514), (118, -490), (124, -420), (98, -336), (-98, -336),
                     (-124, -420)])
        ink(ctx, FUR)
        ell(ctx, 0, -428, 66, 56)
        ink(ctx, FACE, 0)
        for k in range(9):
            ang = math.pi * (0.12 + 0.76 * k / 8)
            circle(ctx, 76 * math.cos(ang), -520 + 66 * math.sin(ang), 9, hexc("#E8452A") if k % 2 else GOLD)
        rrect(ctx, -108, -358, 216, 30, 10)
        ink(ctx, GOLD, 4)
        rrect(ctx, -30, -560, 60, 56, 14)
        ink(ctx, FUR)
        for side in (-1, 1):
            ell(ctx, side * 92, -622, 20, 26)
            ink(ctx, FUR)
            circle(ctx, side * 96, -592, 10, GOLD)
        _sugriv_face(ctx, t, pose)
        _sugriv_crown(ctx)
        if pose == "fear":                                 # wiping sweat, other arm hugging himself
            limb(ctx, [(-112, -480), (-160, -560), (-70, -672)], FUR, 34)
            hand(ctx, -64, -676, FUR, 20)
            limb(ctx, [(112, -480), (136, -420), (40, -416)], FUR, 34)
            hand(ctx, 36, -414, FUR, 20)
            for k in range(3):                             # sweat drops
                fu = (t * 1.3 + k * 0.33) % 1
                circle(ctx, 64 + 14 * k, -660 + fu * 90, 7, hexc("#9AD8FF"), 0.9 * (1 - fu))
        elif pose == "doubt":                              # hand on chin
            limb(ctx, [(112, -480), (146, -430), (44, -540)], FUR, 34)
            hand(ctx, 40, -542, FUR, 20)
            limb(ctx, [(-112, -480), (-126, -400), (-30, -392)], FUR, 34)
            hand(ctx, -26, -390, FUR, 20)
        else:                                              # wonder: both palms up
            for side in (-1, 1):
                limb(ctx, [(side * 112, -480), (side * 170, -560), (side * 150, -660)], FUR, 34)
                dv.palm(ctx, side * 150, -670, FUR, ang=-side * 0.25, s=0.95)
        ctx.restore()
    group(ctx, a, draw)


# =============================================================================
# Story: 6 scenes, 66 spoken words (simple Hindi, no hyphens/dashes so the AI voice reads it cleanly)
# =============================================================================
SPEC = [
    {"key": "hook", "text": "", "visual": "Ram looses one arrow: it rips through seven sal trees into the mountain, "
                                          "then sweeps back into his quiver",
     "vo": [("punch", [("एक तीर...", "EK TEER...")], 0.02),
            ("punch", [("सात पेड़, एक पहाड़...", "SAAT PED, EK PAHAAD..."),
                       ("और फिर तीर वापस!", "AUR PHIR TEER WAPAS!")], 0.04)]},
    {"key": "shak", "text": "", "visual": "Sugriv trembles and wipes his sweat; Hanuman stands with folded hands; "
                                          "Bali's dark silhouette rises on the far hill",
     "vo": [("low", [("किष्किंधा में सुग्रीव को डर था...", "KISHKINDHA MEIN SUGRIV KO DAR THA...")], 0.02),
            ("ask", [("क्या राम जी बाली को हरा पाएंगे?", "KYA RAM JI BAALI KO HARA PAAYENGE?")], 0.04)]},
    {"key": "dhanush", "text": "", "visual": "Ram raises the Kodanda and draws; seven sal trees stand in a row; "
                                             "Sugriv watches with a hand on his chin",
     "vo": [("build", [("राम जी ने धनुष उठाया...", "RAM JI NE DHANUSH UTHAYA..."),
                       ("सामने सात बड़े पेड़।", "SAAMNE SAAT BADE PED.")], 0.02)]},
    {"key": "baan", "text": "", "visual": "Release: the arrow pierces tree after tree, cracks the mountain, "
                                          "and dives into the ground with a shake",
     "vo": [("low", [("बस एक तीर...", "BAS EK TEER...")], 0.02),
            ("fast", [("सातों पेड़ आर पार,", "SAATON PED AAR PAAR,"), ("पहाड़ आर पार,", "PAHAAD AAR PAAR,"),
                      ("और तीर जमीन के अंदर!", "AUR TEER JAMEEN KE ANDAR!")], 0.02)]},
    {"key": "wapas", "text": "", "visual": "The arrow bursts out of the earth, sweeps across the sky and drops into "
                                           "Ram's quiver; golden aura; Sugriv amazed",
     "vo": [("awe", [("और अगले ही पल...", "AUR AGLE HI PAL..."),
                     ("तीर वापस राम जी के पास!", "TEER WAPAS RAM JI KE PAAS!")], 0.02)]},
    {"key": "sharan", "text": "", "visual": "Sugriv kneels at Ram's feet, Ram blesses him, Hanuman with folded "
                                            "hands; loops into the hook",
     "vo": [("whisper", [("सुग्रीव पैरों में गिर पड़े...", "SUGRIV PAIRON MEIN GIR PADE..."),
                         ("क्योंकि ये था बस...", "KYUNKI YE THA BAS...")], 0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "TEER...": GOLD_HI, "TEER": GOLD_HI, "SAAT": hexc("#9BE07A"), "PED,": hexc("#9BE07A"), "PED.": hexc("#9BE07A"),
    "PAHAAD...": hexc("#E0A070"), "PAHAAD": hexc("#E0A070"), "WAPAS": GOLD_HI, "RAM": GOLD_HI,
    "SUGRIV": hexc("#FFB347"), "DAR": hexc("#9AD8FF"), "BAALI": hexc("#FF5A5A"), "DHANUSH": GOLD_HI,
    "SAATON": hexc("#9BE07A"), "AAR": GOLD_HI, "PAAR,": GOLD_HI, "JAMEEN": hexc("#E0A070"),
    "PAL...": GOLD_HI, "PAIRON": hexc("#FFB347"), "BAS...": GOLD_HI,
})


def edge_glow(ctx, t, d, start=0.0, end=0.0):
    if start and t < start:
        glow(ctx, W / 2, H * 0.4, 1300, (1, 0.9, 0.6), 0.85 * (1 - t / start))
    if end and t > d - end:
        glow(ctx, W / 2, H * 0.4, 1300, (1, 0.9, 0.6), 0.85 * (t - (d - end)) / end)


def shake_at(ctx, t, hits, amp=12):
    for h in hits:
        u = t - h
        if 0 <= u < 0.4:
            ctx.translate(amp * (1 - u / 0.4) * math.sin(u * 90), amp * 0.6 * (1 - u / 0.4) * math.cos(u * 70))


def flight(t, t0, t1):
    """Arrow head x along the tree line between t0 (release) and t1 (mountain)."""
    return lerp(BOW_X, MOUNT_X, clamp((t - t0) / max(0.05, t1 - t0)))


def holes_for(x):
    return [1.0 if x >= tx else 0.0 for tx, _ in TREES]


class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"rel": 0.25, "hit": 0.85, "wapas": c("AUR PHIR", d * 0.62)}

    def events(self, d):
        b = self.beats(d)
        return [(b["rel"] - 0.05, "arrow"), (b["hit"], "boom"), (b["wapas"], "whoosh"), (d - 0.35, "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        shake_at(ctx, t, [b["hit"]])
        kishkindha_bg(ctx, t)
        mountain(ctx, t, crack=clamp((t - b["hit"]) / 0.4))
        x = flight(t, b["rel"], b["hit"])
        all_trees(ctx, t, holes_for(x), shake=1.0)
        back = clamp((t - b["wapas"]) / max(0.4, d - b["wapas"] - 0.25))
        quiver(ctx, t, glow_a=0.8 if back >= 1 else 0.0)
        shri_ram(ctx, 230, GROUND - 10, 0.72, t, pose="aim" if t < b["rel"] else "shot", flip=True)
        if b["rel"] <= t < b["hit"]:
            arrow_at(ctx, x, ARROW_Y, 0.0, t)
        return_flight(ctx, t, back)
        edge_glow(ctx, t, d, start=0.3)


class Shak(Cued):
    def beats(self, d):
        c = self.cue
        return {"bali": c("BAALI", d * 0.5)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "thud"), (b["bali"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        kishkindha_bg(ctx, t, dusk=1.0)
        rise = ease_out_cubic(clamp((t - b["bali"]) / 0.6))
        bali_shadow(ctx, 560, lerp(1060, 990, rise), 0.42, t, a=rise)
        sugriv(ctx, 320, GROUND - 10, 0.70, t, pose="fear", flip=True)
        hanuman(ctx, 800, GROUND - 10, 0.70, t, pose="namaste")


class Dhanush(Cued):
    def beats(self, d):
        c = self.cue
        return {"saamne": c("SAAMNE", d * 0.5)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "whoosh"), (b["saamne"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        kishkindha_bg(ctx, t)
        mountain(ctx, t)
        pulse = clamp(1 - abs(t - b["saamne"] - 0.3) / 0.5)
        all_trees(ctx, t, [0.0] * 7)
        if pulse > 0:                                       # the seven trees light up one by one
            for i, (tx, s) in enumerate(TREES):
                k = clamp((t - b["saamne"]) / 0.6 * 7 - i)
                glow(ctx, tx, TREE_BASE - 420 * s, 90 * s, GOLD_HI, 0.5 * k * pulse)
        quiver(ctx, t)
        shri_ram(ctx, 230, GROUND - 10, 0.72, t, pose="bow" if t < b["saamne"] else "aim", flip=True)
        sugriv(ctx, 880, GROUND - 10, 0.68, t, pose="doubt")


class Baan(Cued):
    def beats(self, d):
        c = self.cue
        rel = c("SAATON", d * 0.35)
        pah = c("PAHAAD", d * 0.6)
        jam = c("JAMEEN", d * 0.78)
        return {"rel": rel, "pah": pah, "jam": jam}

    def events(self, d):
        b = self.beats(d)
        return [(b["rel"] - 0.05, "arrow"), (b["pah"], "boom"), (b["jam"] + 0.2, "boom"), (b["jam"] + 0.25, "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dive_t = b["jam"] + 0.2
        shake_at(ctx, t, [b["pah"], dive_t], amp=14)
        kishkindha_bg(ctx, t)
        mountain(ctx, t, crack=clamp((t - b["pah"]) / 0.4))
        x = flight(t, b["rel"], b["pah"])
        all_trees(ctx, t, holes_for(x) if t >= b["rel"] else [0.0] * 7, shake=1.0)
        quiver(ctx, t)
        if t < b["rel"]:                                    # slow build: the nocked arrow glows
            shri_ram(ctx, 230, GROUND - 10, 0.72, t, pose="aim", flip=True)
            glow(ctx, BOW_X, ARROW_Y, 60 + 60 * clamp(t / b["rel"]), GOLD_HI, 0.6)
        else:
            shri_ram(ctx, 230, GROUND - 10, 0.72, t, pose="shot", flip=True)
        if b["rel"] <= t < b["pah"]:
            arrow_at(ctx, x, ARROW_Y, 0.0, t)
        elif b["pah"] <= t < dive_t:                       # through the rock, curving down into the earth
            k = ease_in_out(clamp((t - b["pah"]) / max(0.1, dive_t - b["pah"])))
            ax, ay = MOUNT_X + 20 * k, lerp(ARROW_Y, TREE_BASE + 20, k)
            arrow_at(ctx, ax, ay, lerp(0.0, math.pi / 2, k), t)
        if t >= dive_t:                                     # dust burst and glowing cracks in the ground
            u = clamp((t - dive_t) / 0.8)
            glow(ctx, MOUNT_X, TREE_BASE + 20, 200 * (0.4 + u), GOLD_HI, 0.8 * (1 - u))
            for i in range(16):
                ang = math.pi + math.pi * rnd(i, 81)
                r = 40 + 200 * u * (0.5 + rnd(i, 82))
                circle(ctx, MOUNT_X + r * math.cos(ang), TREE_BASE + 20 + r * math.sin(ang) * 0.6, 6 + 6 * rnd(i, 83),
                       hexc("#C9A46A"), 0.8 * (1 - u))
            for side in (-1, 1):
                line(ctx, [(MOUNT_X, TREE_BASE + 30), (MOUNT_X + side * 60, TREE_BASE + 50),
                           (MOUNT_X + side * 130, TREE_BASE + 40)], GOLD_HI, 5, 1 - u * 0.5)


class Wapas(Cued):
    def beats(self, d):
        c = self.cue
        return {"wapas": c("WAPAS", d * 0.45)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "whoosh"), (b["wapas"], "whoosh"), (d - 0.35, "ghanti"), (d - 0.3, "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        kishkindha_bg(ctx, t)
        mountain(ctx, t, crack=1.0)
        all_trees(ctx, t, [1.0] * 7)
        u = clamp(t / max(0.5, d - 0.3))
        landed = u >= 1
        quiver(ctx, t, glow_a=0.8 if landed else 0.0)
        if landed:
            glow(ctx, 230, GROUND - 400, 360, GOLD_HI, 0.5 + 0.2 * math.sin(t * 10))
        shri_ram(ctx, 230, GROUND - 10, 0.72, t, pose="bow", flip=True)
        sugriv(ctx, 860, GROUND - 10, 0.68, t, pose="wonder")
        return_flight(ctx, t, u)


class Sharan(Cued):
    def beats(self, d):
        c = self.cue
        return {"kyunki": c("KYUNKI", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "ghanti"), (b["kyunki"], "shimmer")]

    def draw(self, ctx, t, d):
        kishkindha_bg(ctx, t)
        dv.petals(ctx, t, n=34, seed=11, a=0.9)
        glow(ctx, 300, GROUND - 420, 320, GOLD_HI, 0.35 + 0.1 * math.sin(t * 4))
        hanuman(ctx, 925, GROUND - 10, 0.68, t, pose="namaste")
        shri_ram(ctx, 290, GROUND - 10, 0.72, t, pose="bless", flip=False)
        sugriv(ctx, 640, GROUND - 10, 0.70, t, pose="sharan")
        edge_glow(ctx, t, d, end=0.3)


SCENE_CLASSES = {"hook": Hook, "shak": Shak, "dhanush": Dhanush, "baan": Baan, "wapas": Wapas, "sharan": Sharan}

UPLOAD = {
    "titles": [
        "Ek Teer, 7 Ped, 1 Pahaad... Phir Wapas Ram Ji Ke Paas! 🏹 #shorts",
        "Ram Ji Ka Wo Teer Jo 7 Ped Cheer Kar Wapas Aa Gaya! #shorts",
        "Sugriv Ko Shak Tha... Ram Ji Ne Ek Teer Se Saat Ped Gira Diye! #shorts",
    ],
    "thumb_text": "7 PED CHEERE!",
    "queries": [
        "ram ji ka teer 7 ped",
        "sugriv bali ramayan katha",
        "ram ne saat taal ek teer se",
    ],
    "description": """
Ram ji ka teer 7 ped aur pahaad cheer kar wapas aa gaya! Sugriv Bali Ramayan katha ka chamatkar 🏹
Ram ne saat taal (saal) ke ped ek teer se cheere, Valmiki Ramayan ke anusaar.
Kishkindha mein Sugriv ko shak tha ki kya Shri Ram Bali ko hara payenge. Ram ji ne ek baan chalaya:
saaton ped aar paar, pahaad aar paar, teer zameen ke andar... aur agle hi pal wapas unke tarkash mein!

Source: Valmiki Ramayana, Kishkindha Kanda 12 (shlok 3-4). Tulsidas ji ki Ramcharitmanas mein saat taal ke ped.

Comment mein likhiye: JAI SHRI RAM 🚩
""",
    "tags": [
        "shri ram", "ram ji ka teer", "sugriv", "bali", "kishkindha", "saat taal", "ramayan", "valmiki ramayana",
        "jai shri ram", "divya rahasya", "sanatan katha", "shorts", "ram sugriv mitrata", "ramayan katha",
    ],
    "hashtags": ["#Shorts", "#JaiShriRam", "#Ramayan"],
}


def thumbnail(ctx):
    kishkindha_bg(ctx, 0.4)
    mountain(ctx, 0.4, crack=1.0)
    all_trees(ctx, 0.4, [1.0] * 7)
    quiver(ctx, 0.4)
    shri_ram(ctx, 230, GROUND - 10, 0.74, 0.5, pose="shot", flip=True)
    line(ctx, [(BOW_X, ARROW_Y), (MOUNT_X, ARROW_Y)], GOLD_HI, 6, 0.9)
    glow(ctx, 700, ARROW_Y, 300, GOLD_HI, 0.35)
    text(ctx, "7 PED CHEERE!", 540, 1330, 124, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
         stroke_w=18)
    text(ctx, "TEER WAPAS AAYA!", 540, 1470, 104, hexc("#FF6A3A"), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
         stroke_w=18)
