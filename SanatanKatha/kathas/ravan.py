"""Ravan Head Sacrifice: Mahadev ke liye apni gardan kaat di (~21.5s loop katha, 6 scenes).

Angle: King of Lanka Ravana performed intense penance on Mount Kailash to bring Mahadev to Lanka.
When Shiva did not appear, Ravana severed 9 of his heads one by one into the sacrificial yagya fire.
As he raised his sword to cut his 10th and final head, Mahadev appeared and held his hand, healing
him as Vaidyanath and granting him the divine Atma Lingam.
The last words "...TABHI TO" loop seamlessly back into "MAHADEV KE LIYE... RAVAN NE APNI NAU GARDANEIN KAAT DI THIN!".
"""

import math
import cairo

from core.katha import *  # noqa: F401,F403
import core.devta as dv
from core.devta import ell, gem, hand, ink, limb, sheen, smooth, eye, palm, rrect, line, lerp, clamp, ease_out_cubic, ease_out_back, rnd

TOPIC = "RAVAN MAHADEV HEAD SACRIFICE"
OUTPUTS = {"edge": "ravan_short.mp4", "files": "ravan_short.mp4"}
MUSIC_STYLE = "pulse"      # Intense sacred pulse & austerity tension
MUSIC_BPM = 92             # Pacing 92 BPM (distinct from abhimanyu 84, tulsi 76)
MUSIC_VOLUME = 0.12
TAIL_PAD = 0.04
MAX_GAP = 0.04
KIKI_PAUSE_MS = 150

# Palettes
FIRE_O = hexc("#FF6A1A")
FIRE_Y = hexc("#FFD24A")
GOLD_HI = dv.GOLD_HI
SHIVA_BLUE = hexc("#8BB8E8")
SHIVA_HALO = hexc("#A8D8FF")
SHIVA_WRAP = hexc("#C87A38")   # Tiger skin / ochre wrap
RAVAN_SKIN = hexc("#C48A58")   # Regal golden-bronze
RAVAN_ARMOR = hexc("#E8A824")  # Radiant golden armour
RAVAN_DHOTI = hexc("#9E1B28")  # Royal crimson silk
STEEL = hexc("#E0E8F0")

SOURCES = [
    "Shiva Purana, Kotirudra Samhita (Vaidyanath Jyotirlinga Mahatmya, sections 28-31): Ravana undertakes intense penance "
    "on Mount Kailash to bring Shiva to Lanka. When Shiva does not manifest, Ravana cuts off his heads one by one into the fire.",
    "Shiva Purana: As Ravana prepares to sever his tenth and final head, Lord Shiva appears, stays his hand, heals his wounds "
    "as Vaidyanath (the divine physician), and bestows upon him the revered Atma Lingam.",
]

SPEC = [
    {"key": "hook", "text": "NAU GARDANEIN KAAT DI THIN",
     "visual": "Ravana in fierce devotion holding sword Chandrahasa, nine glowing severed heads floating before him",
     "vo": [("punch", [("महादेव के लिए...", "MAHADEV KE LIYE..."),
                       ("रावण ने अपनी", "RAVAN NE APNI"),
                       ("नौ गर्दनें काट दी थीं!", "NAU GARDANEIN KAAT DI THIN!")], 0.04)]},
    {"key": "tapasya", "text": "SHIV KO LANKA LE JAANA THA",
     "visual": "Ravana meditating in deep penance on Mount Kailash before the sacred havan fire and Shivling",
     "vo": [("build", [("वो शिव को लंका", "WO SHIV KO LANKA"),
                       ("ले जाना चाहता था...", "LE JAANA CHAHTA THA..."),
                       ("पर महादेव नहीं आए।", "PAR MAHADEV NAHIN AAYE.")], 0.04)]},
    {"key": "ahuti", "text": "TALWAR SE SIR ARPIT KIYE",
     "visual": "Ravana unsheathes sword Chandrahasa and offers his heads one by one into the roaring sacrificial fire",
     "vo": [("fast", [("तब रावण ने तलवार उठाई...", "TAB RAVAN NE TALWAR UTHAI..."),
                      ("और नौ सिर,", "AUR NAU SIR,"),
                      ("हवन में अर्पित कर दिए!", "HAVAN MEIN ARPIT KAR DIYE!")], 0.04)]},
    {"key": "mahadev", "text": "MAHADEV NE HAATH THAAMA",
     "visual": "As Ravana prepares to offer his 10th neck, Mahadev materializes in cosmic blue radiance and grips his wrist",
     "vo": [("punch", [("दसवां सिर अर्पित करने लगा...", "DASVAN SIR ARPIT KARNE LAGA..."),
                       ("तो साक्षात महादेव ने", "TO SAAKSHAT MAHADEV NE"),
                       ("हाथ थाम लिया!", "HAATH THAAM LIYA!")], 0.04)]},
    {"key": "vardan", "text": "SAARE SIR JODE... AATMALINGA",
     "visual": "Mahadev heals Ravana, ten crowned heads appear in a divine arc, and grants the radiant Atma Lingam",
     "vo": [("tell", [("शिव ने सारे सिर जोड़े...", "SHIV NE SAARE SIR JODE..."),
                      ("और आत्मलिंग का", "AUR AATMALINGA KA"),
                      ("वरदान दिया।", "VARDAAN DIYA.")], 0.04)]},
    {"key": "loop", "text": "AISA HATH KISI MEIN NAHIN",
     "visual": "Ravana bowing before Mahadev in supreme reverent surrender, seamlessly crossfading into opening frame",
     "vo": [("awe", [("रावण जैसा हठ", "RAVAN JAISA HATH"),
                     ("किसी में नहीं था।", "KISI MEIN NAHIN THA."),
                     ("तभी तो", "TABHI TO")], 0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "MAHADEV": hexc("#82C4FF"), "LIYE...": hexc("#82C4FF"), "RAVAN": dv.GOLD, "APNI": FIRE_Y,
    "NAU": hexc("#FF5555"), "GARDANEIN": hexc("#FF5555"), "KAAT": hexc("#FF5555"), "THIN!": hexc("#FF5555"),
    "SHIV": hexc("#82C4FF"), "LANKA": dv.GOLD_HI, "LE": dv.GOLD, "JAANA": dv.GOLD, "CHAHTA": dv.GOLD, "THA...": dv.GOLD,
    "NAHIN": hexc("#FF5555"), "AAYE.": hexc("#FF5555"),
    "TALWAR": hexc("#FFFFFF"), "UTHAI...": dv.GOLD_HI, "SIR,": hexc("#FF5555"),
    "HAVAN": FIRE_O, "MEIN": FIRE_O, "ARPIT": FIRE_Y, "KAR": dv.GOLD, "DIYE!": hexc("#FF5555"),
    "DASVAN": FIRE_Y, "SIR": hexc("#FF5555"), "KARNE": dv.GOLD, "LAGA...": hexc("#FF5555"),
    "SAAKSHAT": hexc("#82C4FF"), "HAATH": dv.GOLD_HI, "THAAM": dv.GOLD_HI, "LIYA!": dv.GOLD_HI,
    "SAARE": dv.GOLD, "JODE...": dv.GOLD_HI, "AATMALINGA": hexc("#82C4FF"), "VARDAAN": dv.GOLD_HI, "DIYA.": dv.GOLD_HI,
    "AISA": FIRE_Y, "HATH": hexc("#FF5555"), "KISI": dv.GOLD, "THA.": dv.GOLD, "TABHI": dv.GOLD_HI, "TO": dv.GOLD_HI,
})

def ease_in(u):
    u = clamp(u)
    return u * u

def circle(ctx, x, y, r, c, a=1.0):
    ctx.arc(x, y, r, 0, math.tau)
    rgba(ctx, c, a)
    ctx.fill()

# ============================================================ Scenery & Backgrounds

RAVAN_CAPE = hexc("#3A1240")
RAVAN_CAPE_IN = hexc("#8A1F3E")
DHOTI_DK = hexc("#6A0F1A")
PATKA = hexc("#C9283C")
RUDRAKSHA = hexc("#7A3E1C")
TIGER = hexc("#E08A2E")
SNAKE = hexc("#2F7A4A")
SNAKE_BELLY = hexc("#C8E09A")
NEEL = hexc("#3E68B4")
JATA = hexc("#1C1612")
JATA_HI = hexc("#4A3A2E")
STONE = hexc("#1A181C")
STONE_HI = hexc("#3A3640")


def arc_pts(cx, cy, rx, ry, a0, a1, n):
    return [(cx + rx * math.cos(a0 + (a1 - a0) * i / (n - 1)),
             cy + ry * math.sin(a0 + (a1 - a0) * i / (n - 1))) for i in range(n)]


def beads(ctx, pts, r, c=RUDRAKSHA):
    for (bx, by) in pts:
        circle(ctx, bx, by, r + 1.6, dv.OUTLINE)
        circle(ctx, bx, by, r, c)
        circle(ctx, bx - r * 0.3, by - r * 0.35, r * 0.3, (1, 0.9, 0.7), 0.55)


def band(ctx, p0, p1, u, w, c=None):
    """Armlet / kada across a limb segment at fraction u."""
    bx, by = lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    ell(ctx, bx, by, 8, w * 0.5 + 5, rot=ang)
    ink(ctx, c or dv.GOLD, 3)


def kailash_night(ctx, t, haze=1.0):
    """Moonlit Mount Kailash: starfield, milky band, layered snow ranges, mist and a rocky snow plateau."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in ((0.0, "#04061A"), (0.30, "#0C1640"), (0.52, "#1C2C62"), (0.68, "#3A3A78"),
                  (0.80, "#2A2E5C"), (1.0, "#0E1226")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.paint()

    # Milky band + stars
    for k in range(8):
        glow(ctx, 40 + k * 140, 120 + k * 60, 170, hexc("#7088E0"), 0.07 * haze)
    dv.stars(ctx, t, n=95, a=0.85)

    # Full moon with craters and halo ring
    mx, my = 830, 270
    glow(ctx, mx, my, 300, hexc("#6C8EE8"), 0.32 * haze)
    ctx.arc(mx, my, 96, 0, math.tau)
    rgba(ctx, hexc("#BFD2FF"), 0.18)
    ctx.set_line_width(3)
    ctx.stroke()
    circle(ctx, mx, my, 58, hexc("#F4F6FF"))
    for cx, cy, cr in ((-18, -14, 11), (16, 8, 8), (-6, 22, 6), (22, -20, 5)):
        circle(ctx, mx + cx, my + cy, cr, hexc("#D2DAEE"), 0.8)

    # Far range (pale, jagged, snow tipped)
    far = [(0, 760), (90, 690), (160, 720), (250, 640), (330, 700), (420, 660), (540, 700), (650, 650),
           (740, 700), (830, 630), (920, 690), (1000, 650), (W, 700), (W, 900), (0, 900)]
    ctx.move_to(*far[0])
    for p in far[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    rgba(ctx, hexc("#2C3C70"), 0.9)
    ctx.fill()
    for px, py in ((250, 640), (830, 630), (650, 650), (90, 690), (1000, 650)):
        ctx.move_to(px, py)
        ctx.line_to(px - 26, py + 30)
        ctx.line_to(px - 8, py + 24)
        ctx.line_to(px + 6, py + 34)
        ctx.line_to(px + 28, py + 28)
        ctx.close_path()
        rgba(ctx, hexc("#C9D6F2"), 0.55)
        ctx.fill()

    # Mount Kailash: pyramid dome, lit right face, snow cap and the famous ledge "stairway"
    peak = [(270, 860), (400, 640), (470, 545), (540, 488), (610, 545), (680, 640), (810, 860)]
    smooth(ctx, peak, closed=True)
    ink(ctx, hexc("#3E5A96"), 4, edge=hexc("#1A2448"))
    ctx.move_to(540, 488)
    ctx.line_to(470, 545)
    ctx.line_to(400, 640)
    ctx.line_to(270, 860)
    ctx.line_to(540, 860)
    ctx.close_path()
    rgba(ctx, hexc("#1A2448"), 0.45)
    ctx.fill()
    cap = [(466, 550), (540, 488), (614, 550), (598, 562), (580, 554), (562, 578), (546, 560), (530, 586),
           (512, 560), (494, 572), (480, 558)]
    ctx.move_to(*cap[0])
    for p in cap[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    rgba(ctx, hexc("#EEF3FF"), 0.95)
    ctx.fill()
    ctx.move_to(536, 590)
    ctx.line_to(548, 590)
    ctx.line_to(556, 770)
    ctx.line_to(526, 770)
    ctx.close_path()
    rgba(ctx, hexc("#121A38"), 0.35)
    ctx.fill()
    for ly, half in ((632, 40), (672, 58), (712, 76)):
        line(ctx, [(540 - half, ly), (540 + half, ly + 4)], hexc("#C8D4F0"), 2, 0.22)
    glow(ctx, 540, 520, 120, hexc("#CFE0FF"), 0.18 * haze)

    # Mid ridges left & right
    for pts in ([(0, 900), (0, 760), (120, 700), (230, 780), (330, 760), (420, 900)],
                [(W, 900), (W, 770), (960, 705), (860, 790), (760, 770), (660, 900)]):
        smooth(ctx, pts, closed=True)
        ink(ctx, hexc("#18213E"), 4, edge=hexc("#0A0F22"))
    for px, py, sgn in ((120, 702, 1), (960, 707, -1)):
        smooth(ctx, [(px - 40, py + 34), (px, py), (px + 40, py + 30), (px + 12 * sgn, py + 20)], closed=True)
        rgba(ctx, hexc("#B8C8EE"), 0.6)
        ctx.fill()

    # Mist band
    mg = cairo.LinearGradient(0, 760, 0, 920)
    mg.add_color_stop_rgba(0, 0.8, 0.86, 1.0, 0)
    mg.add_color_stop_rgba(0.5, 0.8, 0.86, 1.0, 0.16 * haze)
    mg.add_color_stop_rgba(1, 0.8, 0.86, 1.0, 0)
    ctx.rectangle(0, 760, W, 160)
    ctx.set_source(mg)
    ctx.fill()

    # Foreground rocky plateau with moon rim light, boulders, snow patches and alpine grass
    smooth(ctx, [(0, 900), (200, 870), (420, 885), (700, 865), (W, 880), (W, H), (0, H)], closed=True)
    ink(ctx, hexc("#121828"), 4, edge=hexc("#070A14"))
    line(ctx, [(200, 872), (420, 887), (700, 867), (W, 882)], hexc("#7C92C8"), 3, 0.5)
    for bx, by, rx, ry in ((70, 1000, 90, 46), (1010, 990, 100, 50), (180, 1120, 60, 28), (930, 1140, 70, 30)):
        ell(ctx, bx, by, rx, ry)
        ink(ctx, hexc("#1C2236"), 4, edge=hexc("#070A14"))
        ell(ctx, bx + rx * 0.2, by - ry * 0.45, rx * 0.6, ry * 0.25)
        rgba(ctx, hexc("#DCE6FF"), 0.55)
        ctx.fill()
    for sx, sy, rx in ((330, 960, 80), (760, 950, 100), (520, 1030, 70), (60, 1170, 70), (1020, 1180, 60)):
        ell(ctx, sx, sy, rx, rx * 0.16)
        rgba(ctx, hexc("#C4D2F2"), 0.35)
        ctx.fill()
    for k in range(14):
        gx = 20 + k * 78 + 18 * math.sin(k * 2.3)
        gy = GROUND + 4 + 10 * math.sin(k * 1.7)
        for blade in (-1, 0, 1):
            sway = 3 * math.sin(t * 2.0 + k + blade)
            line(ctx, [(gx + blade * 6, gy), (gx + blade * 12 + sway, gy - 22 - 6 * abs(blade - 0.5))],
                 hexc("#3E5A4A"), 3, 0.8)

    # Drifting snow / spirit dust
    for p in range(26):
        px = (rnd(p, 3) * W + t * (14 + 10 * rnd(p, 4))) % W
        py = (rnd(p, 9) * 1100 + t * (28 + 20 * rnd(p, 2))) % 1150
        circle(ctx, px, py, 1.5 + 2 * rnd(p, 5), hexc("#E2ECFF"), 0.35 + 0.35 * rnd(p, 6))


def shivling(ctx, x, y, s, t, a=1.0):
    """Black stone Shiva Lingam: two-tier yoni-peetha with spout, Tripundra, Belpatra, marigolds, abhishek stream."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    glow(ctx, 0, -70, 120, SHIVA_HALO, 0.35 * a)

    # Yoni-peetha (two tiers) with spout to the right
    smooth(ctx, [(70, -6), (160, 0), (172, 14), (90, 20)], closed=True)
    ink(ctx, STONE)
    ell(ctx, 0, 12, 112, 24)
    ink(ctx, STONE)
    ell(ctx, 0, -2, 94, 19)
    ink(ctx, STONE_HI)
    line(ctx, [(-96, 6), (0, 22), (96, 6)], dv.GOLD, 3, 0.8)

    # Lingam
    smooth(ctx, [(-45, 0), (-45, -90), (0, -135), (45, -90), (45, 0)], closed=True)
    ink(ctx, hexc("#121114"))
    sheen(ctx, -18, -70, 14, 46, 0.22)
    line(ctx, [(10, -128), (14, -60), (18, -2), (60, 4), (150, 6)], hexc("#DDF0FF"), 3, 0.55)   # abhishek water

    # Tripundra + kumkum bindu
    for ty in (-88, -76, -64):
        line(ctx, [(-26, ty), (26, ty)], hexc("#FFF0D0"), 4)
    circle(ctx, 0, -76, 5, hexc("#FF2A1A"))

    # Belpatra (3-leaf) on top
    for ang in (-0.7, 0.0, 0.7):
        ctx.save()
        ctx.translate(0, -132)
        ctx.rotate(ang)
        ell(ctx, 0, -18, 9, 20)
        ink(ctx, hexc("#3FA34F"), 3)
        line(ctx, [(0, -4), (0, -32)], hexc("#246B30"), 2)
        ctx.restore()

    # Marigold offerings at the base
    for k, fx in enumerate((-80, -50, -18, 22, 56, 86)):
        fy = 10 + 6 * math.sin(k * 1.9)
        circle(ctx, fx, fy, 11, dv.OUTLINE)
        circle(ctx, fx, fy, 9.5, hexc("#FF8C1A") if k % 2 else hexc("#FFC21A"))
        circle(ctx, fx, fy, 3.5, hexc("#C85A00"))
    ctx.restore()


def havan_kund(ctx, x, y, s, t, fires=1.0):
    """Brick Vedic havan kund: layered flames (outer/inner/core), smoke wisps and rising embers."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # Leaping flames (behind the front wall)
    if fires > 0.0:
        glow(ctx, 0, -50 * fires, 170 * fires, FIRE_O, 0.5)
        for layer, col, k in ((0, FIRE_O, 1.0), (1, FIRE_Y, 0.68), (2, hexc("#FFF6D8"), 0.36)):
            for f in range(5):
                fx = (f - 2) * 24 * (1.0 - layer * 0.18)
                fh = (math.sin(t * 8.0 + f * 1.4 + layer) * 26 + 70) * fires * k
                fw = (22 + 7 * math.sin(t * 10.0 + f)) * (0.6 + 0.4 * k) * min(fires, 1.4)
                tip = fx + 8 * math.sin(t * 6 + f)
                smooth(ctx, [(fx - fw, 6), (fx - fw * 0.6, -fh * 0.45), (tip, -fh), (fx + fw * 0.6, -fh * 0.45),
                             (fx + fw, 6)], closed=True)
                rgba(ctx, col, 0.95)
                ctx.fill()
        for sm in range(4):        # smoke wisps
            u = ((t * 0.5 + sm * 0.25) % 1.0)
            glow(ctx, 20 * math.sin(t + sm * 2) + u * 30, -120 * fires - u * 220, 40 + u * 50,
                 hexc("#8A8AA0"), 0.22 * (1 - u))
        for em in range(9):        # embers
            ex = math.sin(t * 4.0 + em * 2.0) * 45
            ey = -30 - ((t * 85 + em * 30) % 170) * fires
            circle(ctx, ex, ey, 2.6, hexc("#FFE080"), 0.8)

    # Terraced brick altar (front)
    for idx, (w, h, col) in enumerate(((140, 36, "#8C3D1E"), (112, 26, "#B5562E"), (84, 18, "#5A2210"))):
        top = idx * 16
        rrect(ctx, -w, top, w * 2, h, 6)
        ink(ctx, hexc(col))
        ctx.save()
        rrect(ctx, -w, top, w * 2, h, 6)
        ctx.clip()
        line(ctx, [(-w, top + h * 0.5), (w, top + h * 0.5)], hexc("#3A160A"), 2, 0.6)
        for bx in range(-w + 18, w, 36):
            off = 18 if idx % 2 else 0
            line(ctx, [(bx + off, top), (bx + off, top + h * 0.5)], hexc("#3A160A"), 2, 0.5)
            line(ctx, [(bx + 18 - off, top + h * 0.5), (bx + 18 - off, top + h)], hexc("#3A160A"), 2, 0.5)
        ctx.restore()
    line(ctx, [(-138, 2), (138, 2)], hexc("#FFB060"), 3, 0.6)   # firelit rim
    ctx.restore()


def chandrahasa_sword(ctx, x, y, ang=0.0, s=1.0):
    """Chandrahasa ("moon's laughter"): crescent steel blade, blood groove, gold makara guard, wrapped grip."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(s, s)
    glow(ctx, 14, -160, 130, hexc("#CFE6FF"), 0.22)

    smooth(ctx, [(-12, 6), (24, -70), (52, -170), (40, -250), (6, -292), (14, -240), (16, -170), (0, -80),
                 (-16, 6)], closed=True)
    ink(ctx, STEEL)
    line(ctx, [(2, -20), (22, -120), (24, -215)], hexc("#93A2B6"), 4)
    sheen(ctx, 30, -150, 8, 60, 0.45)

    smooth(ctx, [(-46, 14), (-22, 0), (22, 0), (46, 14), (34, 28), (-34, 28)], closed=True)
    ink(ctx, dv.GOLD, 3)
    for sgn in (-1, 1):
        circle(ctx, sgn * 44, 12, 6, dv.GOLD_HI)
    gem(ctx, 0, 14, 7, dv.RED_GEM)
    rrect(ctx, -9, 28, 18, 50, 6)
    ink(ctx, hexc("#5A2A14"), 3)
    for wy in (36, 48, 60, 72):
        line(ctx, [(-8, wy), (8, wy - 6)], dv.GOLD, 2.5)
    ell(ctx, 0, 86, 13, 12)
    ink(ctx, dv.GOLD, 3)
    gem(ctx, 0, 86, 5, dv.RED_GEM)
    ctx.restore()

# ============================================================ Character Rigs

def mini_head(ctx, x, y, s, t, closed=False, seed=0, a=1.0):
    """Small crowned Ravana head (offered heads / Dashanan arc): face, brows, mustache, kundal, mukut."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)
        for side in (-1, 1):
            ell(ctx, side * 47, 2, 9, 13)
            ink(ctx, RAVAN_SKIN, 4)
        ell(ctx, 0, 0, 48, 54)
        ink(ctx, RAVAN_SKIN)
        sheen(ctx, -12, -16, 20, 16, 0.18)
        if closed:
            for sgn in (-1, 1):
                line(ctx, [(sgn * 28, -6), (sgn * 18, 0), (sgn * 8, -6)], dv.OUTLINE, 5)
        else:
            eye(ctx, -18, -6, 10, 8, t, seed=seed, lash=True)
            eye(ctx, 18, -6, 10, 8, t, seed=seed, lash=True)
        for sgn in (-1, 1):
            line(ctx, [(sgn * 32, -22), (sgn * 8, -16)], hexc("#1A0C06"), 5)
        smooth(ctx, [(-34, 16), (-12, 12), (0, 15), (12, 12), (34, 16), (40, 6), (24, 22), (0, 20), (-24, 22),
                     (-40, 6)], closed=True)
        ink(ctx, hexc("#150B05"), 3)
        for sgn in (-1, 1):
            circle(ctx, sgn * 48, 20, 6, dv.GOLD)
        smooth(ctx, [(-46, -40), (46, -40), (50, -82), (24, -104), (0, -122), (-24, -104), (-50, -82)], closed=True)
        ink(ctx, dv.GOLD)
        line(ctx, [(-46, -76), (46, -76)], dv.GOLD_DK, 3)
        rrect(ctx, -50, -52, 100, 16, 6)
        ink(ctx, dv.GOLD_DK, 3)
        gem(ctx, 0, -64, 8, dv.RED_GEM)
        ctx.restore()
    dv.group(ctx, a, draw)


def ravan(ctx, x, y, s, t, pose="stand", look=(0.0, 0.0), severed=0, a=1.0, flip=False):
    """Regal King of Lanka Ravana: tiered mukut, Shaiva tripundra, armour, cape, crimson dhoti, Chandrahasa."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        if flip:
            ctx.scale(-1, 1)
        b = 1 + 0.012 * math.sin(t * 3.5)
        ctx.scale(s, s * b)
        _ravan_body(ctx, t, pose, look, severed)
        ctx.restore()
    dv.group(ctx, a, draw)


def _ravan_body(ctx, t, pose, look, severed):
    skin = RAVAN_SKIN
    Ls, Rs = (-130, -540), (130, -540)
    mood = {"sword_raise": "fierce", "stand": "fierce", "caught": "shock"}.get(pose, "calm")

    # 0. Royal cape behind the body
    if pose in ("tapasya", "bow"):
        cape = [(-120, -560), (120, -560), (230, -230), (270, -14), (-270, -14), (-230, -230)]
    else:
        cape = [(-120, -560), (120, -560), (205, -300), (235, -36), (0, -64), (-235, -36), (-205, -300)]
    smooth(ctx, cape, closed=True)
    ink(ctx, RAVAN_CAPE)
    line(ctx, cape[2:5] if pose not in ("tapasya", "bow") else cape[2:4], RAVAN_CAPE_IN, 5, 0.8)

    # 0b. Dashanan arc (behind everything else of the head)
    if severed == -1:
        order = sorted(range(9), key=lambda k: -(k // 2))
        for k in order:
            side = -1 if k % 2 == 0 else 1
            idx = k // 2 + 1
            hx = side * (idx * 72 + 22)
            hy = -668 + idx * idx * 4
            glow(ctx, hx, hy, 70, GOLD_HI, 0.3)
            mini_head(ctx, hx, hy, 0.62 - idx * 0.03, t, closed=(mood == "calm"), seed=k)

    # 1. Legs & royal crimson dhoti
    if pose == "tapasya":
        limb(ctx, [(-90, -320), (-140, -180), (-30, -25)], skin, 48)
        limb(ctx, [(90, -320), (140, -180), (30, -25)], skin, 48)
        hem = [(-170, -180), (0, -70), (170, -180)]
        smooth(ctx, [(-150, -340), (150, -340), (170, -180), (0, -70), (-170, -180)], closed=True)
        ink(ctx, RAVAN_DHOTI)
        for fx in (-70, 70):
            line(ctx, [(fx * 0.4, -330), (fx, -220), (fx * 1.4, -170)], DHOTI_DK, 5)
    elif pose == "bow":
        limb(ctx, [(-65, -300), (-110, -170), (-140, -15)], skin, 48)
        limb(ctx, [(65, -300), (95, -150), (40, -15)], skin, 48)
        for fx in (-140, 40):
            band(ctx, (fx, -60), (fx, -10), 0.4, 44)
        hem = [(-140, -170), (-85, -60), (85, -60), (140, -170)]
        smooth(ctx, [(-135, -340), (135, -340), (140, -170), (85, -60), (-85, -60), (-140, -170)], closed=True)
        ink(ctx, RAVAN_DHOTI)
        for fx in (-60, 60):
            line(ctx, [(fx * 0.3, -330), (fx, -200), (fx * 1.2, -90)], DHOTI_DK, 5)
    else:
        for side in (-1, 1):
            fx = side * 62
            limb(ctx, [(side * 52, -320), (side * 60, -160), (fx, -15)], skin, 48)
            band(ctx, (fx, -70), (fx, -10), 0.45, 44)
            ell(ctx, fx + side * 6, -10, 38, 16)
            ink(ctx, skin)
        hem = [(-140, -180), (-80, -65), (0, -130), (80, -65), (140, -180)]
        smooth(ctx, [(-130, -350), (130, -350), (140, -180), (80, -65), (0, -130), (-80, -65), (-140, -180)],
               closed=True)
        ink(ctx, RAVAN_DHOTI)
        for fx in (-1, 1):
            line(ctx, [(fx * 40, -340), (fx * 70, -220), (fx * 84, -90)], DHOTI_DK, 5)
            line(ctx, [(fx * 95, -330), (fx * 118, -200)], DHOTI_DK, 4)
        smooth(ctx, [(-32, -352), (32, -352), (40, -190), (0, -160), (-40, -190)], closed=True)   # front patka
        ink(ctx, PATKA, 4)
        line(ctx, [(-40, -190), (0, -160), (40, -190)], dv.GOLD_HI, 5)
        for py in (-310, -270, -230):
            circle(ctx, 0, py, 5, dv.GOLD_HI)
    line(ctx, hem, dv.GOLD_HI, 7)
    for i in range(len(hem) - 1):
        for u in (0.25, 0.5, 0.75):
            circle(ctx, lerp(hem[i][0], hem[i + 1][0], u), lerp(hem[i][1], hem[i + 1][1], u) - 10, 3.5, dv.GOLD)

    # 2. Torso & golden armour
    smooth(ctx, [(-135, -550), (135, -550), (120, -380), (-120, -380)], closed=True)
    ink(ctx, RAVAN_ARMOR)
    for sgn in (-1, 1):
        smooth(ctx, [(sgn * 12, -540), (sgn * 108, -540), (sgn * 100, -470), (sgn * 56, -450), (sgn * 14, -470)],
               closed=True)
        ink(ctx, dv.GOLD, 3, edge=dv.GOLD_DK)
        sheen(ctx, sgn * 60, -510, 30, 16, 0.25)
    for ay in (-430, -405):
        line(ctx, [(-104, ay), (0, ay + 8), (104, ay)], dv.GOLD_DK, 4)
    for k in range(12):        # sun medallion
        ra = k * math.tau / 12
        line(ctx, [(math.cos(ra) * 18, -462 + math.sin(ra) * 18), (math.cos(ra) * 30, -462 + math.sin(ra) * 30)],
             dv.GOLD_HI, 4)
    ell(ctx, 0, -462, 19, 19)
    ink(ctx, dv.GOLD_HI, 3)
    gem(ctx, 0, -462, 11, dv.RED_GEM)
    rrect(ctx, -132, -392, 264, 40, 10)              # belt
    ink(ctx, dv.GOLD, 4)
    for gx in (-80, 0, 80):
        gem(ctx, gx, -372, 8 if gx else 11, dv.GREEN_GEM if gx else dv.RED_GEM)
    for tx in range(-110, 120, 44):                  # hanging tassels
        line(ctx, [(tx, -352), (tx, -322)], dv.GOLD, 3)
        circle(ctx, tx, -318, 5, dv.GOLD_HI)

    # 3. Arms according to pose (sword arm of sword_raise drawn after the head)
    late = None
    if pose == "sword_raise":
        L = [Ls, (-200, -470), (-110, -410)]
        limb(ctx, L, skin, 42)
        band(ctx, L[0], L[1], 0.55, 42)
        band(ctx, L[1], L[2], 0.8, 42)
        hand(ctx, -110, -410, skin, 26)
        late = [Rs, (252, -600), (230, -720)]
    elif pose == "caught":
        L = [Ls, (-190, -460), (-130, -380)]
        limb(ctx, L, skin, 42)
        band(ctx, L[0], L[1], 0.55, 42)
        hand(ctx, -130, -380, skin, 26)
        late = [Rs, (220, -580), (169, -676)]
    elif pose == "tapasya":
        for arm in ([Ls, (-180, -460), (-35, -340)], [Rs, (180, -460), (35, -340)]):
            limb(ctx, arm, skin, 42)
            band(ctx, arm[0], arm[1], 0.55, 42)
            band(ctx, arm[1], arm[2], 0.75, 42)
        hand(ctx, -20, -340, skin, 24)
        hand(ctx, 20, -340, skin, 24)
        beads(ctx, arc_pts(0, -345, 34, 16, 0.1, math.pi - 0.1, 9), 4)
    elif pose == "bow":
        for arm in ([Ls, (-140, -470), (-22, -455)], [Rs, (140, -470), (22, -455)]):
            limb(ctx, arm, skin, 40)
            band(ctx, arm[0], arm[1], 0.55, 40)
            band(ctx, arm[1], arm[2], 0.7, 40)
        smooth(ctx, [(-18, -420), (-14, -480), (0, -512), (14, -480), (18, -420)], closed=True)   # namaskar
        ink(ctx, skin)
        line(ctx, [(0, -506), (0, -424)], dv.OUTLINE, 3)
    else:
        for arm in ([Ls, (-190, -480), (-170, -360)], [Rs, (190, -480), (170, -360)]):
            limb(ctx, arm, skin, 42)
            band(ctx, arm[0], arm[1], 0.55, 42)
        chandrahasa_sword(ctx, -170, -360, ang=0.1, s=0.75)
        hand(ctx, -170, -360, skin, 26)
        hand(ctx, 170, -360, skin, 26)

    # Shoulder pauldrons, collar and rudraksha mala
    for sgn in (-1, 1):
        ell(ctx, sgn * 128, -546, 46, 32, rot=sgn * 0.25)
        ink(ctx, dv.GOLD, 4)
        for r in (30, 18):
            ctx.arc(sgn * 128, -540, r, math.pi * 1.1, math.pi * 1.9)
            rgba(ctx, dv.GOLD_DK, 0.9)
            ctx.set_line_width(3)
            ctx.stroke()
        gem(ctx, sgn * 128, -548, 6, dv.RED_GEM)
    smooth(ctx, [(-82, -560), (82, -560), (64, -522), (0, -506), (-64, -522)], closed=True)
    ink(ctx, dv.GOLD, 4)
    for gx, gy in ((-40, -530), (0, -520), (40, -530)):
        gem(ctx, gx, gy, 6, dv.GREEN_GEM if gx else dv.RED_GEM)
    beads(ctx, arc_pts(0, -540, 78, 110, 0.12 * math.pi, 0.88 * math.pi, 15), 5)

    # 4. Head & mukut
    _ravan_head(ctx, t, look, mood)

    if late:
        limb(ctx, late, skin, 42)
        band(ctx, late[0], late[1], 0.55, 42)
        band(ctx, late[1], late[2], 0.85, 42)
        if pose == "sword_raise":
            chandrahasa_sword(ctx, late[2][0], late[2][1], ang=-2.23, s=0.75)
        else:
            chandrahasa_sword(ctx, late[2][0], late[2][1], ang=0.25, s=0.75)
        hand(ctx, late[2][0], late[2][1], skin, 27)


def _ravan_head(ctx, t, look, mood="fierce"):
    skin = RAVAN_SKIN
    brow_c = hexc("#1A0C06")
    limb(ctx, [(0, -560), (0, -615)], skin, 58)
    for side in (-1, 1):
        ell(ctx, side * 66, -662, 13, 20)
        ink(ctx, skin, 4)

    ell(ctx, 0, -660, 68, 76)
    ink(ctx, skin)
    ell(ctx, 0, -606, 46, 18)
    rgba(ctx, hexc("#5A2A10"), 0.12)
    ctx.fill()
    sheen(ctx, -12, -680, 36, 28, 0.16)

    if mood == "calm":
        for sgn in (-1, 1):
            line(ctx, [(sgn * 38, -670), (sgn * 26, -662), (sgn * 14, -670)], dv.OUTLINE, 6)
        for sgn in (-1, 1):
            line(ctx, [(sgn * 44, -690), (sgn * 26, -697), (sgn * 10, -690)], brow_c, 6)
    elif mood == "shock":
        for sgn in (-1, 1):
            eye(ctx, sgn * 26, -670, 14, 13, t, look=look, lash=True)
            line(ctx, [(sgn * 44, -696), (sgn * 26, -706), (sgn * 10, -698)], brow_c, 6)
    else:
        for sgn in (-1, 1):
            eye(ctx, sgn * 26, -670, 13, 10, t, look=look, lash=True, lid=0.18, skin=skin)
            smooth(ctx, [(sgn * 48, -698), (sgn * 10, -686), (sgn * 8, -679), (sgn * 46, -688)], closed=True)
            ink(ctx, brow_c, 2, edge=brow_c)

    line(ctx, [(2, -664), (-6, -646), (6, -642)], hexc("#6A3418"), 4)    # nose
    if mood == "calm":
        line(ctx, [(-14, -620), (0, -614), (14, -620)], hexc("#5A1E10"), 4)
    elif mood == "shock":
        ell(ctx, 0, -618, 9, 11)
        ink(ctx, hexc("#3A0E08"), 3)
    else:
        line(ctx, [(-18, -616), (0, -621), (18, -616)], hexc("#5A1E10"), 5)

    # Curled handlebar mustache
    smooth(ctx, [(0, -636), (-24, -644), (-50, -640), (-66, -652), (-70, -664), (-60, -660), (-56, -646),
                 (-30, -628), (0, -630), (30, -628), (56, -646), (60, -660), (70, -664), (66, -652), (50, -640),
                 (24, -644)], closed=True)
    ink(ctx, hexc("#150B05"), 3)

    # Shaiva tripundra (Ravana, the great Shiva bhakt)
    for ty in (-712, -705, -698):
        line(ctx, [(-24, ty), (24, ty)], hexc("#FFF3DC"), 3)
    circle(ctx, 0, -705, 4, hexc("#E0201A"))

    # Kundal hoops
    for side in (-1, 1):
        ctx.arc(side * 70, -630, 14, 0, math.tau)
        rgba(ctx, dv.OUTLINE)
        ctx.set_line_width(10)
        ctx.stroke()
        ctx.arc(side * 70, -630, 14, 0, math.tau)
        rgba(ctx, dv.GOLD)
        ctx.set_line_width(6)
        ctx.stroke()
        gem(ctx, side * 70, -614, 6, dv.RED_GEM)

    # Tiered golden mukut with side wings and kalash finial
    for side in (-1, 1):
        smooth(ctx, [(side * 56, -722), (side * 96, -740), (side * 104, -792), (side * 74, -772)], closed=True)
        ink(ctx, dv.GOLD, 4)
        gem(ctx, side * 90, -760, 5, dv.GREEN_GEM)
    smooth(ctx, [(-66, -722), (66, -722), (72, -790), (44, -846), (0, -880), (-44, -846), (-72, -790)], closed=True)
    ink(ctx, dv.GOLD)
    sheen(ctx, -24, -800, 16, 40, 0.28)
    line(ctx, [(-70, -786), (70, -786)], dv.GOLD_DK, 4)
    line(ctx, [(-48, -836), (48, -836)], dv.GOLD_DK, 4)
    for gx in (-46, -16, 16, 46):
        circle(ctx, gx, -810, 5, dv.GOLD_HI)
    rrect(ctx, -74, -746, 148, 26, 9)
    ink(ctx, dv.GOLD_DK, 4)
    dv.pearls(ctx, [(gx, -733) for gx in range(-62, 66, 16)], r=4)
    gem(ctx, 0, -764, 14, dv.RED_GEM)
    for cx in (-38, 38):
        gem(ctx, cx, -760, 8, dv.GREEN_GEM)
    gem(ctx, 0, -858, 7, dv.RED_GEM)
    ell(ctx, 0, -888, 9, 9)
    ink(ctx, dv.GOLD_HI, 3)
    line(ctx, [(0, -896), (0, -906)], dv.GOLD_HI, 4)


def _crescent(ctx, x, y, r, c):
    ctx.push_group()
    circle(ctx, x, y, r, c)
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    circle(ctx, x + r * 0.45, y - r * 0.25, r * 0.86, (0, 0, 0))
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.pop_group_to_source()
    ctx.paint()


def mahadev(ctx, x, y, s, t, pose="bless", flip=False, a=1.0):
    """Devadhidev Mahadev: jatajuta with crescent & Ganga, Neelkanth, Vasuki, rudraksha, tiger skin, trishul+damru."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        if flip:
            ctx.scale(-1, 1)
        b = 1 + 0.012 * math.sin(t * 3.5)
        ctx.scale(s, s * b)
        skin = SHIVA_BLUE

        # Prabhamandal halo with rays
        glow(ctx, 0, -680, 260, SHIVA_HALO, 0.45)
        ctx.arc(0, -690, 175, 0, math.tau)
        rgba(ctx, SHIVA_HALO, 0.55)
        ctx.set_line_width(6)
        ctx.stroke()
        for k in range(28):
            ra = k * math.tau / 28 + t * 0.15
            line(ctx, [(math.cos(ra) * 186, -690 + math.sin(ra) * 186),
                       (math.cos(ra) * 206, -690 + math.sin(ra) * 206)], SHIVA_HALO, 4, 0.45)

        # Flowing back locks of the jata
        for side in (-1, 1):
            smooth(ctx, [(side * 46, -742), (side * 96, -706), (side * 122, -610), (side * 112, -520),
                         (side * 84, -556), (side * 70, -650)], closed=True)
            ink(ctx, JATA)
            line(ctx, [(side * 80, -700), (side * 104, -610), (side * 100, -545)], JATA_HI, 3)

        # Trishul planted on the ground (held in screen-left hand)
        tx = -182
        line(ctx, [(tx, -10), (tx, -560)], dv.OUTLINE, 16)
        line(ctx, [(tx, -10), (tx, -560)], hexc("#DDE6F2"), 10)
        dv.trishul(ctx, tx, -560, 1.0, t)

        # Legs, rudraksha anklets
        for fx in (-50, 50):
            limb(ctx, [(fx * 0.9, -320), (fx, -160), (fx, -15)], skin, 46)
            beads(ctx, [(fx + dx, -52) for dx in (-16, -6, 4, 14)], 5)
            ell(ctx, fx, -10, 38, 16)
            ink(ctx, skin)

        # Tiger-skin wrap with stripes, zigzag hem and a hanging paw
        wrap = [(-122, -352), (122, -352), (136, -180), (96, -150), (40, -178), (0, -150), (-40, -178),
                (-96, -150), (-136, -180)]
        smooth(ctx, wrap, closed=True)
        rgba(ctx, TIGER)
        ctx.fill_preserve()
        ctx.save()
        ctx.clip()
        for k, sx in enumerate(range(-110, 130, 34)):
            line(ctx, [(sx, -350), (sx + 14, -300), (sx - 4, -250), (sx + 10, -200)], hexc("#2A140A"), 7)
        line(ctx, [(-140, -168), (-96, -150), (-40, -178), (0, -150), (40, -178), (96, -150), (140, -168)],
             hexc("#FFF2DC"), 10)
        ctx.restore()
        smooth(ctx, wrap, closed=True)
        rgba(ctx, dv.OUTLINE)
        ctx.set_line_width(dv.OW)
        ctx.stroke()
        smooth(ctx, [(96, -200), (122, -110), (100, -96), (84, -170)], closed=True)   # paw flap
        ink(ctx, TIGER)
        for cx in (98, 108, 116):
            line(ctx, [(cx, -102), (cx + 2, -92)], hexc("#FFF2DC"), 3)
        line(ctx, [(-124, -346), (124, -346)], SNAKE, 9)    # serpent belt

        # Torso, bhasma tripundra on chest, navel
        smooth(ctx, [(-125, -550), (125, -550), (115, -380), (-115, -380)], closed=True)
        ink(ctx, skin)
        sheen(ctx, 0, -470, 75, 55, 0.2)
        for ty in (-498, -486, -474):
            line(ctx, [(-70, ty), (70, ty + 2)], hexc("#F2F6FF"), 4, 0.7)
        line(ctx, [(-6, -404), (0, -398), (6, -404)], dv.OUTLINE, 3)

        # Rudraksha malas
        beads(ctx, arc_pts(0, -556, 72, 92, 0.1 * math.pi, 0.9 * math.pi, 15), 5.5)
        beads(ctx, arc_pts(0, -556, 88, 150, 0.14 * math.pi, 0.86 * math.pi, 19), 5.5)

        # Arms
        Ls, Rs = (-120, -540), (120, -540)
        L = [Ls, (-196, -480), (tx, -430)]
        limb(ctx, L, skin, 40)
        if pose == "catch_hand":
            R = [Rs, (214, -600), (287, -667)]
        else:
            R = [Rs, (196, -500), (212, -446)]
        limb(ctx, R, skin, 40)
        for arm in (L, R):
            for u, seg in ((0.5, (arm[0], arm[1])), (0.82, (arm[1], arm[2]))):
                p0, p1 = seg
                bx, by = lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u)
                ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0]) + math.pi / 2
                beads(ctx, [(bx + math.cos(ang) * d, by + math.sin(ang) * d) for d in (-14, -5, 5, 14)], 4.5)
            for d in (-10, 0, 10):     # bhasma stripes on upper arm
                bx, by = lerp(arm[0][0], arm[1][0], 0.28), lerp(arm[0][1], arm[1][1], 0.28)
                circle(ctx, bx, by + d, 2.5, hexc("#F2F6FF"), 0.7)
        hand(ctx, tx, -430, skin, 26)
        if pose == "catch_hand":
            hand(ctx, 287, -667, skin, 30)
            line(ctx, [(270, -690), (300, -690)], dv.OUTLINE, 4)
        else:
            palm(ctx, 212, -446, skin, ang=-0.1, s=1.0)

        # Neelkanth neck + Vasuki coiled around it
        limb(ctx, [(0, -552), (0, -612)], NEEL, 54)
        coil = [(-62, -566), (-34, -540), (0, -534), (34, -542), (62, -566), (82, -604)]
        line(ctx, coil, dv.OUTLINE, 22)
        line(ctx, coil, SNAKE, 15)
        for (cx, cy) in coil[1:5]:
            circle(ctx, cx, cy + 3, 3, SNAKE_BELLY, 0.9)
        ell(ctx, 90, -630, 22, 27, rot=0.2)
        ink(ctx, SNAKE, 4)
        ell(ctx, 92, -626, 11, 15, rot=0.2)
        rgba(ctx, SNAKE_BELLY, 0.85)
        ctx.fill()
        for ex in (82, 98):
            circle(ctx, ex, -640, 3, hexc("#FFD24A"))
        line(ctx, [(92, -606), (94, -594), (88, -588)], hexc("#E0302A"), 2)
        line(ctx, [(94, -594), (100, -588)], hexc("#E0302A"), 2)

        # Face
        for side in (-1, 1):
            ell(ctx, side * 62, -662, 12, 18)
            ink(ctx, skin, 4)
            circle(ctx, side * 64, -640, 9, hexc("#F2F6FF"))
            circle(ctx, side * 64, -640, 5, RUDRAKSHA)
        ell(ctx, 0, -660, 64, 72)
        ink(ctx, skin)
        sheen(ctx, -10, -680, 34, 26, 0.18)
        for sgn in (-1, 1):
            eye(ctx, sgn * 24, -666, 12, 9, t, look=(0.0, 0.0), lash=True, lid=0.45, skin=skin, seed=3)
            line(ctx, [(sgn * 40, -684), (sgn * 24, -690), (sgn * 10, -685)], JATA, 4)
        line(ctx, [(2, -660), (-4, -642), (5, -640)], hexc("#3A5A90"), 3)
        line(ctx, [(-14, -620), (0, -614), (14, -620)], hexc("#2A3A6A"), 4)
        for ty in (-716, -709, -702):
            line(ctx, [(-28, ty), (28, ty)], hexc("#F2F6FF"), 3)
        glow(ctx, 0, -704, 22, hexc("#FF7A3A"), 0.5)
        smooth(ctx, [(0, -718), (6, -704), (0, -690), (-6, -704)], closed=True)
        ink(ctx, hexc("#FF4A2A"), 2)

        # Jatajuta: front hairline, stacked bun, coils, rudraksha band
        smooth(ctx, [(-66, -690), (-62, -736), (0, -754), (62, -736), (66, -690), (42, -718), (0, -728),
                     (-42, -718)], closed=True)
        ink(ctx, JATA)
        ell(ctx, 0, -792, 58, 50)
        ink(ctx, JATA)
        ell(ctx, 0, -848, 42, 38)
        ink(ctx, JATA)
        for r, cy in ((40, -792), (26, -792), (26, -848)):
            ctx.arc(0, cy, r, math.pi * 1.05, math.pi * 1.95)
            rgba(ctx, JATA_HI)
            ctx.set_line_width(3)
            ctx.stroke()
        beads(ctx, arc_pts(0, -752, 60, 16, 0.05 * math.pi, 0.95 * math.pi, 11), 5)
        _crescent(ctx, -56, -818, 24, hexc("#FFF8D4"))

        # Ganga springing from the jata
        glow(ctx, 50, -900, 70, hexc("#C8E8FF"), 0.35)
        ctx.move_to(2, -878)
        ctx.curve_to(6, -944, 72, -956, 86, -902)
        ctx.curve_to(92, -874, 88, -850, 80, -826)
        ctx.curve_to(74, -852, 74, -886, 62, -906)
        ctx.curve_to(46, -930, 22, -914, 18, -876)
        ctx.close_path()
        rgba(ctx, hexc("#BFE4FF"), 0.88)
        ctx.fill()
        line(ctx, [(14, -890), (34, -928), (64, -930), (80, -900)], hexc("#FFFFFF"), 3, 0.8)
        for k in range(5):
            dy = (t * 120 + k * 18) % 80
            circle(ctx, 80 + 3 * math.sin(k * 2), -826 + dy, 3, hexc("#C8E8FF"), 0.8 * (1 - dy / 80))

        ctx.restore()
    dv.group(ctx, a, draw)

# ============================================================ Scene Classes

class Hook(Cued):
    """Scene 1: Hook - Ravana with Chandrahasa at his own neck, an arch of nine offered heads glowing above him."""
    def beats(self, d):
        c = self.cue
        return {
            "mahadev": c("MAHADEV", d * 0.15),
            "ravan": c("RAVAN", d * 0.40),
            "nau": c("NAU", d * 0.65),
            "kaat": c("KAAT", d * 0.85),
        }

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["nau"], "zap"), (b["kaat"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        kailash_night(ctx, t, haze=1.2)
        glow(ctx, 540, GROUND - 260, 300, FIRE_O, 0.45)

        # Arch of nine offered heads, popping in one by one on "NAU"
        for i in range(9):
            u = clamp((t - b["nau"] - i * 0.07) / 0.25) if t >= b["nau"] else 0.0
            if u <= 0.0:
                continue
            ang = math.pi * (1.08 - i * 0.145)
            hx = 540 + 380 * math.cos(ang)
            hy = 770 - 320 * math.sin(ang) + 6 * math.sin(t * 3.0 + i)
            glow(ctx, hx, hy, 70, FIRE_Y, 0.55 * u)
            glow(ctx, hx, hy + 10, 40, FIRE_O, 0.5 * u)
            mini_head(ctx, hx, hy, 0.4 * ease_out_back(u), t, closed=True, seed=i)

        ravan(ctx, 540, GROUND - 10, 0.76, t, pose="sword_raise", look=(0.0, 0.0), flip=False)


class Tapasya(Cued):
    """Scene 2: Ravana seated in deep Padmasana tapasya before the sacred havan fire and Shivling."""
    def beats(self, d):
        c = self.cue
        return {
            "lanka": c("LANKA", d * 0.25),
            "le": c("LE", d * 0.45),
            "nahin": c("NAHIN", d * 0.75),
        }

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["lanka"], "whoosh"), (b["nahin"], "thud")]

    def draw(self, ctx, t, d):
        kailash_night(ctx, t, haze=1.0)
        havan_kund(ctx, 250, GROUND - 20, 1.0, t, fires=1.0)
        shivling(ctx, 470, GROUND - 15, 1.0, t)
        glow(ctx, 790, GROUND - 200, 220, GOLD_HI, 0.35)
        ravan(ctx, 790, GROUND - 10, 0.74, t, pose="tapasya", look=(-0.6, 0.0), flip=True)


class Ahuti(Cued):
    """Scene 3: Ravana severs his heads one by one into the roaring havan fire."""
    def beats(self, d):
        c = self.cue
        return {
            "talwar": c("TALWAR", d * 0.25),
            "nau": c("NAU", d * 0.55),
            "diye": c("DIYE", d * 0.80),
        }

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "whoosh"), (b["talwar"], "zap"), (b["diye"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        kailash_night(ctx, t, haze=1.4)
        u_fire = 1.0 + 0.6 * clamp((t - b["nau"]) / (d * 0.4))

        # Offered head arcing down into the fire on cue
        if t >= b["nau"]:
            u_fall = clamp((t - b["nau"]) / 0.5)
            hx = lerp(620, 320, u_fall)
            hy = lerp(GROUND - 400, GROUND - 70, ease_in(u_fall))
            glow(ctx, hx, hy, 60, FIRE_Y, 0.6)
            mini_head(ctx, hx, hy, 0.4, t, closed=True, a=1.0 - 0.6 * clamp((u_fall - 0.8) / 0.2))

        havan_kund(ctx, 320, GROUND - 20, 1.2, t, fires=u_fire)
        ravan(ctx, 720, GROUND - 10, 0.76, t, pose="sword_raise", look=(-0.7, 0.0), flip=True)


class MahadevScene(Cued):
    """Scene 4: As Ravana attempts the 10th cut, Mahadev appears and holds his hand."""
    def beats(self, d):
        c = self.cue
        return {
            "dasvan": c("DASVAN", d * 0.20),
            "mahadev": c("MAHADEV", d * 0.55),
            "thaam": c("THAAM", d * 0.80),
        }

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["mahadev"], "shimmer"), (b["thaam"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        kailash_night(ctx, t, haze=1.5)
        havan_kund(ctx, 540, GROUND - 15, 0.9, t, fires=0.8)

        caught = t >= b["thaam"]
        ravan(ctx, 700, GROUND - 10, 0.74, t, pose="caught" if caught else "sword_raise", look=(-0.6, 0.0),
              flip=True)

        if t >= b["dasvan"]:
            u_appear = clamp((t - b["dasvan"]) / 0.4)
            glow(ctx, 360, GROUND - 260, 320 * u_appear, SHIVA_HALO, 0.6 * u_appear)
            mahadev(ctx, 360, GROUND - 10, 0.75, t, pose="catch_hand" if caught else "bless", flip=False,
                    a=u_appear)
            if caught:
                glow(ctx, 575, 670, 60, hexc("#FFFFFF"), 0.6 * clamp(1 - (t - b["thaam"]) / 0.5))


class Vardan(Cued):
    """Scene 5: Mahadev restores all ten heads (Dashanan) and grants the Atma Lingam."""
    def beats(self, d):
        c = self.cue
        return {
            "saare": c("SAARE", d * 0.20),
            "jode": c("JODE", d * 0.45),
            "aatmalinga": c("AATMALINGA", d * 0.70),
            "vardaan": c("VARDAAN", d * 0.85),
        }

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "ghanti"), (b["jode"], "shimmer"), (b["aatmalinga"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        kailash_night(ctx, t, haze=1.2)
        dv.petals(ctx, t, n=35, a=0.7)

        glow(ctx, 300, GROUND - 280, 260, SHIVA_HALO, 0.5)
        mahadev(ctx, 300, GROUND - 10, 0.74, t, pose="bless", flip=False)

        if t >= b["aatmalinga"]:
            u_ling = clamp((t - b["aatmalinga"]) / 0.4)
            glow(ctx, 520, GROUND - 320, 180 * u_ling, GOLD_HI, 0.8)
            shivling(ctx, 520, GROUND - 240, 0.7 * u_ling, t)

        restored = -1 if t >= b["jode"] else 0
        glow(ctx, 770, GROUND - 260, 280, GOLD_HI, 0.5)
        ravan(ctx, 770, GROUND - 10, 0.72, t, pose="bow", look=(-0.6, 0.0), severed=restored, flip=True)


class Loop(Cued):
    """Scene 6: Ravana bowing before the Lingam in supreme resolve; seamless loop back into the opening frame."""
    def beats(self, d):
        c = self.cue
        return {
            "hath": c("HATH", d * 0.25),
            "kisi": c("KISI", d * 0.55),
            "tabhi": c("TABHI", d * 0.85),
        }

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["hath"], "shimmer"), (b["tabhi"], "whoosh")]

    def draw(self, ctx, t, d):
        kailash_night(ctx, t, haze=1.1)
        shivling(ctx, 320, GROUND - 15, 1.15, t)
        glow(ctx, 740, GROUND - 200, 240, GOLD_HI, 0.45)
        ravan(ctx, 740, GROUND - 10, 0.74, t, pose="bow", look=(0.0, 0.0), flip=True)

        rem = d - t
        if rem <= 0.45:
            x_fade = (0.45 - rem) / 0.45
            ctx.push_group()
            Hook().draw(ctx, 0.0, d)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(x_fade)


SCENE_CLASSES = {
    "hook": Hook,
    "tapasya": Tapasya,
    "ahuti": Ahuti,
    "mahadev": MahadevScene,
    "vardan": Vardan,
    "loop": Loop,
}
SCENES = SCENE_CLASSES

# ============================================================ Thumbnail & Upload Kit

def thumbnail(ctx):
    t = 0.5
    kailash_night(ctx, t, haze=1.3)
    glow(ctx, 680, 900, 560, FIRE_O, 0.5)
    glow(ctx, 270, 860, 440, SHIVA_HALO, 0.5)

    # The moment: Chandrahasa at Ravana's own neck, Mahadev's hand reaching for the wrist
    ravan(ctx, 730, 1400, 0.92, t, pose="sword_raise", look=(-0.5, 0.0), flip=True)
    mahadev(ctx, 270, 1400, 0.88, t, pose="catch_hand", flip=False)

    # Havan kund up front, offered crowned heads resting in its flames
    havan_kund(ctx, 520, 1580, 1.35, t, fires=1.5)
    for hx, hy, hs in ((390, 1530, 0.55), (650, 1530, 0.55), (520, 1505, 0.6)):
        glow(ctx, hx, hy, 90, FIRE_O, 0.55)
        mini_head(ctx, hx, hy, hs, t, closed=True)
        glow(ctx, hx, hy + 30, 50, FIRE_Y, 0.5)

    g = cairo.LinearGradient(0, 0, 0, 560)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.92)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 560)
    ctx.set_source(g)
    ctx.fill()
    g = cairo.LinearGradient(0, 1640, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.9)
    ctx.rectangle(0, 1640, W, H - 1640)
    ctx.set_source(g)
    ctx.fill()

    text(ctx, "RAVAN NE APNA SIR", 540, 230, 105, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "KYUN KAAT DIYA?", 540, 370, 115, hexc("#FF4A3A"), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
         stroke_w=24)
    text(ctx, "DIVYA RAHASYA", 540, 1830, 42, GOLD_HI, a=0.85)


UPLOAD = {
    "thumb_text": "SIR KYUN KAATA",
    "titles": [
        "Ravan Ne Mahadev Ke Liye Apni Gardan Kyun Kaat Di Thi? #shorts",
        "Kailash Par Ravan Ne Kaate Apne 9 Sir: Vaidyanath Rahasya",
        "Jab Mahadev Ne Ravan Ka Haath Thama! 😱 #shorts",
        "Ravan Ki Aisi Bhakti Ki Mahadev Bhi Kaanp Uthe! #shorts",
        "Shiva Lingam Ke Liye Ravan Ka Sabse Bada Balidaan",
    ],
    "queries": [
        "ravan ne mahadev ke liye apni gardan kyun kaat di thi",
        "ravan ne apne 9 sir kyun kaate shiva purana",
        "vaidyanath jyotirlinga ravan tapasya rahasya",
        "ravan aatmalinga kailash mahabharat katha",
    ],
    "description": (
        "Mahadev ko Kailash se Lanka lane ke liye Ravan ne ghor tapasya ki. Jab bholenath nahi aaye, "
        "to usne havan mein ek-ek karke apne 9 sir kaat dale!\n\n"
        "Jaise hi 10va sir katne laga, saakshat Mahadev ne prakat hokar uska hath pakad liya aur use "
        "Vaidyanath bankar saare sir wapas jode aur Atma Lingam ka vardaan diya.\n\n"
        "Sources: Shiva Purana, Kotirudra Samhita (Vaidyanath Jyotirlinga Mahatmya, sections 28-31).\n\n"
        "Comment mein likhiye: Har Har Mahadev! 🔱\n\n"
        "#Shorts #Mahadev #Ravan #Kailash #DivyaRahasya #SanatanDharma"
    ),
    "tags": [
        "ravan", "mahadev", "shiva", "kailash", "vaidyanath", "aatmalinga",
        "tapasya", "bholenath", "shiva purana", "divya rahasya", "sanatan dharma"
    ],
    "hashtags": ["#Shorts", "#Mahadev", "#Ravan", "#Kailash"],
}
