"""Lepakshi Mandir Ka Rahasya: Hawa Mein Jhulta Khambha (~55-60s katha, seven scenes).

Usage (from SanatanKatha/):
  python make.py lepakshi --preview       # preview contact sheet
  python make.py lepakshi --kiki-export   # exports kiki_narrator text file
  python make.py lepakshi --kiki-split    # cuts the downloaded voice files into lines
  python make.py lepakshi                 # final render with music & devta characters

Rahasya:
The 16th-century Veerabhadra Temple in Lepakshi, Andhra Pradesh, features 70 carved stone pillars.
Among them, one massive granite pillar—the Aakaasa Stambha (Hanging Pillar)—does NOT touch the stone floor.
A clearly visible gap exists underneath through which cloth, paper, and sticks pass freely from one side to the other.
During British rule, engineer Hamilton attempted to dislodge the hanging pillar with iron crowbars to uncover its secret,
only for the entire stone roof and surrounding pillars to tremble and tilt, proving the temple's interconnected
gravity-balancing architectural genius. Furthermore, local lore links Lepakshi to Ramayana Treta Yuga, where Prabhu
Shri Rama blessed the heroic fallen bird Jatayu with the words 'Le Pakshi' (Rise, Bird!).
"""

import math
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cairo

from core import engine, katha, upload_kit
from core.katha import *  # noqa: F401,F403
import core.devta as dv
from core.devta import group, place, halo, smooth, ink, ell, gem, limb, hand, sheen, eye, shade

TOPIC = "LEPAKSHI MANDIR HANGING PILLAR RAHASYA"
OUTPUTS = {"edge": "lepakshi_short.mp4"}
MUSIC_BPM = 82   # Distinct tempo: kailash was 90 (>= 6 BPM step)
WHITE = (1.0, 1.0, 1.0)
RED_GEM = hexc("#D61F3A")
GOLD_HI = hexc("#FFF099")
AMBER_GLOW = hexc("#FF9A28")
STONE_DARK = hexc("#28221C")
STONE_MID = hexc("#4E443B")
STONE_LIGHT = hexc("#7C7064")
STONE_BASE = hexc("#383028")

SOURCES = [
    "Archaeological Survey of India (ASI) & Temple Epigraphs: Veerabhadra Temple, Lepakshi, constructed circa 1530-1538 CE by brothers Virupanna Nayaka and Viranna during the Vijayanagara Empire (King Achyuta Deva Raya).",
    "British Colonial Archaeological Records (Hamilton Investigation, circa 1902): British engineer Hamilton attempted to mechanically pry the hanging pillar, resulting in structural shifting across the Natya Mantapa.",
    "Valmiki Ramayana (Aranya Kanda) & Sthala Purana: Lore of divine eagle Jatayu fighting Ravana to rescue Mata Sita; Prabhu Shri Rama blessing him with 'Le Pakshi' (Rise, Bird!) and granting Moksha.",
]


def title_card(ctx, main, sub, a=1.0):
    """Clean, high-impact minimal title card with gold border."""
    rrect(ctx, 160, 240, 760, 130, 20)
    rgba(ctx, hexc("#14100D"), 0.90 * a)
    ctx.fill_preserve()
    rgba(ctx, GOLD, 0.95 * a)
    ctx.set_line_width(3.2)
    ctx.stroke()
    text(ctx, main, 540, 290, 42, GOLD_HI, bold=True, a=a)
    text(ctx, sub, 540, 338, 25, WHITE, a=0.92 * a)


def ribbon(ctx, x, y, msg, col, u=1.0):
    """Sleek, minimal top cue ribbon (no screen clutter)."""
    if u <= 0:
        return
    p = max(0.01, ease_out_back(clamp(u / 0.4)))
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(p, p)
    w = text_width(ctx, msg, 34) + 50
    rrect(ctx, -w / 2, -28, w, 56, 16)
    rgba(ctx, col, 0.92)
    ctx.fill_preserve()
    rgba(ctx, GOLD, 0.95)
    ctx.set_line_width(2.8)
    ctx.stroke()
    text(ctx, msg, 0, 9, 32, (1, 1, 1), bold=True)
    ctx.restore()


# ============================================================ REALISTIC TEMPLE ARCHITECTURE & SCENERY

def temple_mantapa_bg(ctx, t, shake=0.0):
    """Realistic 16th-century Vijayanagara granite Natya Mantapa corridor with deep perspective and warm lamps."""
    ctx.save()
    if shake > 0:
        sx = 8 * math.sin(t * 45) * shake
        sy = 5 * math.cos(t * 38) * shake
        ctx.translate(sx, sy)

    # Ambient deep sanctum sky/wall
    dv.sky(ctx, hexc("#120D0A"), hexc("#221812"), hexc("#36261C"), 0.55)

    # Carved granite ceiling beams
    rrect(ctx, 0, 160, W, 140, 0)
    rgba(ctx, STONE_DARK, 0.96)
    ctx.fill()
    for bx in range(0, W + 1, 140):
        line(ctx, [(bx, 160), (bx, 300)], hexc("#1A140E"), 8)
        line(ctx, [(bx + 4, 160), (bx + 4, 300)], STONE_LIGHT, 2.5)

    # Granite flagstone floor with receding perspective lines
    ctx.rectangle(0, 960, W, H - 960)
    rgba(ctx, hexc("#1C1712"), 1.0)
    ctx.fill()
    # Floor stone slabs
    for fy in [1020, 1090, 1170, 1260, 1370]:
        line(ctx, [(0, fy), (W, fy)], hexc("#14100D"), 5)
        line(ctx, [(0, fy + 2), (W, fy + 2)], hexc("#322A22"), 2)
    # Floor perspective joints
    for fx in [100, 260, 420, 580, 740, 900, 1040]:
        line(ctx, [(fx, 960), (fx + (fx - 540) * 0.45, H)], hexc("#14100D"), 4)

    # Background carved pillars fading into sanctum depth
    for px, sc in [(160, 0.62), (920, 0.62), (300, 0.52), (780, 0.52)]:
        ctx.save()
        ctx.translate(px, 980)
        ctx.scale(sc, sc)
        # Background pillar shaft
        rrect(ctx, -42, -900, 84, 900, 8)
        rgba(ctx, hexc("#28201A"), 0.88)
        ctx.fill()
        # Pillar capital
        smooth(ctx, [(-70, -900), (70, -900), (45, -840), (-45, -840)])
        rgba(ctx, hexc("#342B23"), 0.9)
        ctx.fill()
        ctx.restore()

    # Hanging brass oil lamps (Deepams) with glowing golden flames
    for lx, ly, lseed in [(220, 480, 1), (860, 480, 2)]:
        # Brass chain
        line(ctx, [(lx, 260), (lx, ly)], hexc("#B58828"), 4)
        for cy in range(270, ly, 24):
            circle(ctx, lx, cy, 3.5, hexc("#E2B845"), 0.9)
        # Deepam lamp bowl
        ctx.save()
        ctx.translate(lx, ly)
        smooth(ctx, [(-30, 0), (30, 0), (22, 28), (0, 36), (-22, 28)])
        rgba(ctx, hexc("#966A16"), 0.95)
        ctx.fill()
        rgba(ctx, GOLD, 0.95)
        ctx.set_line_width(2.5)
        ctx.stroke()
        # Glowing flame
        flicker = 3 * math.sin(t * 12 + lseed)
        glow(ctx, 0, -18, 120, AMBER_GLOW, 0.55)
        smooth(ctx, [(0, -32 + flicker), (10, -14), (0, 0), (-10, -14)])
        rgba(ctx, hexc("#FFF29A"), 0.95)
        ctx.fill()
        circle(ctx, 0, -12, 5, WHITE)
        ctx.restore()

    # Drifting sacred incense smoke / spiritual aura
    for i in range(16):
        sx = (rnd(i, 41) * W + t * 18 * (0.5 + rnd(i, 42))) % W
        sy = 380 + 720 * rnd(i, 43)
        circle(ctx, sx, sy, 2.5 + 2 * rnd(i, 44), hexc("#FFE0B2"), 0.25 + 0.15 * math.sin(t * 3 + i))

    ctx.restore()


def hanging_pillar(ctx, x, y, s, t, cloth_u=0.0, tilt=0.0, gap_highlight=True):
    """Magnificent carved granite Hanging Pillar with visible floating gap beneath its base."""
    ctx.save()
    ctx.translate(x, y)
    if tilt != 0.0:
        ctx.rotate(tilt)
    ctx.scale(s, s)

    # 1. Carved Ceiling Capital & Lotus Corbels (attached to temple roof)
    # Upper bracket
    smooth(ctx, [(-150, -1080), (150, -1080), (110, -980), (-110, -980)])
    rgba(ctx, STONE_DARK)
    ctx.fill_preserve()
    rgba(ctx, STONE_LIGHT)
    ctx.set_line_width(4)
    ctx.stroke()

    # Inverted lotus petals on capital
    for pet in range(-100, 110, 35):
        smooth(ctx, [(pet, -980), (pet + 18, -940), (pet, -920), (pet - 18, -940)])
        rgba(ctx, STONE_MID)
        ctx.fill()
        rgba(ctx, STONE_LIGHT)
        ctx.set_line_width(2)
        ctx.stroke()

    # 2. Main Fluted Pillar Shaft (multi-tiered Vijayanagara granite)
    # Upper shaft segment
    rrect(ctx, -75, -920, 150, 240, 10)
    rgba(ctx, STONE_MID)
    ctx.fill()
    # Carved vertical fluting
    for fl in [-50, -25, 0, 25, 50]:
        line(ctx, [(fl, -915), (fl, -685)], hexc("#2A221A"), 5)
        line(ctx, [(fl + 2, -915), (fl + 2, -685)], hexc("#8A7C6E"), 2.5)

    # Middle octagonal band with carved deity niche
    rrect(ctx, -90, -680, 180, 260, 12)
    rgba(ctx, STONE_BASE)
    ctx.fill_preserve()
    rgba(ctx, STONE_LIGHT)
    ctx.set_line_width(3.5)
    ctx.stroke()

    # Carved bas-relief sculpture in central niche (Veerabhadra / dancing deity motif)
    rrect(ctx, -52, -655, 104, 210, 8)
    rgba(ctx, hexc("#201A14"), 0.9)
    ctx.fill()
    # Carved deity silhouette inside pillar facet
    circle(ctx, 0, -620, 22, hexc("#9C8E7E"))
    smooth(ctx, [(-28, -590), (28, -590), (34, -510), (-34, -510)])
    rgba(ctx, hexc("#8C7E6E"))
    ctx.fill()
    # Sculpted arms with divine bow / trishul
    line(ctx, [(-28, -580), (-44, -550), (-36, -515)], hexc("#7C6E5E"), 6)
    line(ctx, [(28, -580), (44, -550), (36, -515)], hexc("#7C6E5E"), 6)

    # Lower fluted shaft segment
    rrect(ctx, -75, -420, 150, 320, 10)
    rgba(ctx, STONE_MID)
    ctx.fill()
    for fl in [-50, -25, 0, 25, 50]:
        line(ctx, [(fl, -415), (fl, -105)], hexc("#2A221A"), 5)
        line(ctx, [(fl + 2, -415), (fl + 2, -105)], hexc("#8A7C6E"), 2.5)

    # 3. Carved Base Plinth (SUSPENDED IN MID-AIR!)
    # The pillar base stops at y = -50, leaving a clean 50px gap above the ground line (y = 0)!
    rrect(ctx, -105, -100, 210, 50, 10)
    rgba(ctx, STONE_DARK)
    ctx.fill_preserve()
    rgba(ctx, STONE_LIGHT)
    ctx.set_line_width(4)
    ctx.stroke()
    # Bottom chiselled lip of the hanging pillar
    line(ctx, [(-100, -52), (100, -52)], hexc("#A89C8C"), 4)

    # 4. THE IMPOSSIBLE GAP & PASSING CLOTH
    # Highlight the clear visible empty space between base (-50) and floor (0)
    if gap_highlight:
        # Golden radiance shining through the gap
        glow(ctx, 0, -25, 90, GOLD_HI, 0.45 + 0.15 * math.sin(t * 4))
        # Clear gap visual arrows / indicators
        line(ctx, [(-125, -25), (125, -25)], GOLD, 2.5)

    # Smooth silk cloth sliding completely through the gap (from left to right)
    if cloth_u > 0.0:
        cloth_prog = clamp(cloth_u, 0.0, 1.0)
        cx_mid = lerp(-220, 220, cloth_prog)
        wave1 = 6 * math.sin(t * 8)
        wave2 = 6 * math.cos(t * 8)

        # Silk cloth ribbon gliding through gap at y = -25
        ctx.save()
        smooth(ctx, [
            (cx_mid - 160, -28 + wave1),
            (cx_mid - 70, -23 + wave2),
            (cx_mid + 70, -25 - wave1),
            (cx_mid + 160, -27 - wave2),
            (cx_mid + 160, -17 - wave2),
            (cx_mid + 70, -15 - wave1),
            (cx_mid - 70, -13 + wave2),
            (cx_mid - 160, -18 + wave1)
        ])
        rgba(ctx, hexc("#E23B18"), 0.95)  # Rich sacred crimson-saffron silk
        ctx.fill_preserve()
        rgba(ctx, GOLD, 0.95)
        ctx.set_line_width(2.5)
        ctx.stroke()
        # Gold zari border along cloth edges
        line(ctx, [(cx_mid - 150, -26), (cx_mid + 150, -25)], GOLD_HI, 2)
        ctx.restore()

    # Ground shadow directly beneath (soft ambient, showing clear gap detachment)
    ell(ctx, 0, 0, 110, 14)
    rgba(ctx, (0, 0, 0), 0.32)
    ctx.fill()

    ctx.restore()


# ============================================================ CHARACTERS

def pujari_devotee(ctx, x, y, s, t, kneeling=True, flip=False, a=1.0):
    """Devoted South Indian temple priest / pilgrim testing the gap with a sacred silk cloth."""
    def draw():
        place(ctx, x, y, s, t, flip)
        skin = dv.BRAHMIN_SKIN
        hair = dv.HAIR

        # Sacred shikha topknot
        ell(ctx, -25 if not flip else 25, -590, 28, 28)
        ink(ctx, hair)

        if kneeling:
            # Kneeling pose: folded legs on stone floor
            # Legs folded
            smooth(ctx, [(-80, -280), (80, -280), (120, -140), (140, -15), (70, -15), (-70, -15), (-120, -140)])
            ink(ctx, hexc("#F8F4EA"))   # White cotton dhoti
            # Gold Zari border
            line(ctx, [(-110, -22), (130, -22)], GOLD, 7)
            line(ctx, [(120, -140), (140, -20)], GOLD, 4)

            # Torso (upright in devotion)
            smooth(ctx, [(-90, -460), (-50, -480), (50, -480), (90, -460), (95, -360), (75, -270), (-75, -270), (-95, -360)])
            ink(ctx, skin)

            # Sacred Thread (Yajnopavita / Janeu) & Angavastram
            line(ctx, [(-50, -475), (55, -275)], WHITE, 4)
            # Silk Angavastram draped over shoulder
            smooth(ctx, [(-85, -465), (-45, -480), (60, -320), (35, -290)], k=0.1)
            ink(ctx, hexc("#D86C20"), 5)

            # Neck & Head
            rrect(ctx, -24, -520, 48, 52, 12)
            ink(ctx, skin)
            ell(ctx, 0, -560, 75, 82)
            ink(ctx, skin)

            # Gentle, smiling devotional eyes looking at the pillar gap
            eye(ctx, 24, -564, 18, 22, t, look=(0.4, 0.4), iris=hexc("#2A1810"), seed=1)

            # Sacred Vibhuti Tripundra & Red Kumkum tilak on forehead
            for ty in (-602, -594, -586):
                line(ctx, [(-28, ty), (28, ty)], WHITE, 3)
            circle(ctx, 0, -594, 3.5, RED_GEM)

            # Devoted peaceful smile
            ctx.move_to(8, -532)
            ctx.curve_to(18, -524, 30, -524, 38, -532)
            ctx.set_line_width(3.2)
            rgba(ctx, hexc("#A83248"))
            ctx.stroke()

            # Rudraksha mala
            for rk in range(7):
                rang = -0.6 + rk * 0.2
                circle(ctx, 36 * math.sin(rang), -480 + 14 * math.cos(rang), 5, hexc("#7A3E1E"))

            # Arms extended forward, holding silk cloth beneath the pillar gap
            L = (-85, -450)
            R = (85, -450)
            limb(ctx, [L, (30, -380), (120, -310)], skin, 36)
            hand(ctx, 120, -310, skin, 22)
            limb(ctx, [R, (90, -360), (150, -290)], skin, 36)
            hand(ctx, 150, -290, skin, 22)
        else:
            # Standing pose
            for side in (-1, 1):
                limb(ctx, [(side * 42, -290), (side * 45, -150), (side * 42, -25)], skin, 38)
                ell(ctx, side * 46, -14, 34, 15)
                ink(ctx, skin)
            smooth(ctx, [(-85, -310), (85, -310), (95, -180), (105, -35), (45, -25), (0, -45), (-45, -25), (-105, -35), (-95, -180)])
            ink(ctx, hexc("#F8F4EA"))
            line(ctx, [(-100, -38), (100, -38)], GOLD, 6)

            smooth(ctx, [(-90, -460), (-50, -480), (50, -480), (90, -460), (95, -360), (75, -290), (-75, -290), (-95, -360)])
            ink(ctx, skin)
            rrect(ctx, -24, -520, 48, 52, 12)
            ink(ctx, skin)
            ell(ctx, 0, -560, 75, 82)
            ink(ctx, skin)
            for side in (-1, 1):
                eye(ctx, side * 28, -564, 18, 22, t, look=(0, 0), iris=hexc("#2A1810"), seed=1)
            for ty in (-602, -594, -586):
                line(ctx, [(-28, ty), (28, ty)], WHITE, 3)
            circle(ctx, 0, -594, 3.5, RED_GEM)

        ctx.restore()
    group(ctx, a, draw)


def british_engineer(ctx, x, y, s, t, pose="shock", flip=False, a=1.0):
    """British colonial engineer Hamilton in 1900s khaki explorer gear, shocked by the shifting temple."""
    def draw():
        place(ctx, x, y, s, t, flip)
        skin = hexc("#F5D2B3")
        khaki = hexc("#A89874")
        dark_khaki = hexc("#6A5E44")
        leather = hexc("#3E2214")
        hair = hexc("#4A301E")

        # Legs in riding breeches & tall leather boots
        for side in (-1, 1):
            limb(ctx, [(side * 48, -320), (side * 52, -180), (side * 50, -30)], khaki, 42)
            # Tall leather boots
            limb(ctx, [(side * 52, -180), (side * 50, -30)], leather, 40)
            ell(ctx, side * 55, -14, 38, 16)
            ink(ctx, leather)

        # Khaki safari tunic
        smooth(ctx, [(-100, -490), (-55, -510), (55, -510), (100, -490), (105, -380), (85, -310), (-85, -310), (-105, -380)])
        ink(ctx, khaki)
        # Leather utility belt & brass buckle
        rrect(ctx, -85, -340, 170, 28, 6)
        ink(ctx, leather)
        circle(ctx, 0, -326, 10, GOLD)
        # Brass buttons along chest
        for btn in (-460, -425, -390, -355):
            circle(ctx, 0, btn, 5, GOLD)

        # Neck & Head
        rrect(ctx, -26, -560, 52, 58, 12)
        ink(ctx, skin)
        ell(ctx, 0, -610, 80, 88)
        ink(ctx, skin)

        # English moustache
        smooth(ctx, [(-28, -580), (0, -572), (28, -580), (38, -568), (0, -562), (-38, -568)])
        ink(ctx, hair)

        # Eyes: wide open in shock and terror!
        eye(ctx, -30, -618, 22, 26, t, look=(0.3, -0.4), iris=hexc("#1E4268"), seed=3)
        eye(ctx, 30, -618, 22, 26, t, look=(0.3, -0.4), iris=hexc("#1E4268"), seed=4)
        # Raised, arched shocked eyebrows
        line(ctx, [(-46, -652), (-18, -660)], hair, 6)
        line(ctx, [(18, -660), (46, -652)], hair, 6)

        # Open mouth in gasp / disbelief
        ell(ctx, 0, -550, 16, 14)
        ink(ctx, hexc("#3A1414"))

        # British Pith Helmet (Solar Topee)
        ctx.save()
        ctx.translate(0, -680)
        # Helmet brim
        ell(ctx, 0, 10, 115, 30)
        ink(ctx, hexc("#EAE3D2"))
        # Helmet dome
        smooth(ctx, [(-75, 10), (-70, -65), (0, -95), (70, -65), (75, 10)])
        ink(ctx, hexc("#F4EEE2"))
        # Helmet leather puggaree band
        rrect(ctx, -72, -10, 144, 22, 6)
        ink(ctx, dark_khaki)
        ctx.restore()

        # Arms: dropping or trembling with an iron crowbar
        L, R = (-95, -480), (95, -480)
        if pose == "shock":
            # Recoiling back, arms raised in panic
            limb(ctx, [L, (-150, -420), (-120, -320)], khaki, 38)
            hand(ctx, -120, -320, skin, 24)
            limb(ctx, [R, (150, -440), (180, -360)], khaki, 38)
            hand(ctx, 180, -360, skin, 24)
            # Dropped iron crowbar falling at an angle
            line(ctx, [(140, -340), (190, -180)], hexc("#5A626A"), 12)
        else:
            # Prying with crowbar
            limb(ctx, [L, (-130, -420), (-60, -340)], khaki, 38)
            hand(ctx, -60, -340, skin, 24)
            limb(ctx, [R, (120, -420), (60, -340)], khaki, 38)
            hand(ctx, 60, -340, skin, 24)
            # Iron crowbar jammed under
            line(ctx, [(40, -360), (-80, -40)], hexc("#5A626A"), 12)

        ctx.restore()
    group(ctx, a, draw)


def architect_virupanna(ctx, x, y, s, t, flip=False, a=1.0):
    """16th-century Vijayanagara Master Architect Virupanna holding palm-leaf architectural blueprints."""
    def draw():
        place(ctx, x, y, s, t, flip)
        skin = dv.BARBARIK_SKIN
        hair = dv.HAIR

        # Legs in royal silk dhoti
        for side in (-1, 1):
            limb(ctx, [(side * 48, -310), (side * 52, -160), (side * 50, -30)], skin, 42)
            ell(ctx, side * 54, -14, 38, 16)
            ink(ctx, skin)

        # Deep crimson and gold Vijayanagara royal dhoti
        smooth(ctx, [(-110, -330), (110, -330), (125, -200), (140, -40), (60, -30), (0, -55), (-60, -30), (-140, -40), (-125, -200)])
        ink(ctx, hexc("#961C2C"))
        line(ctx, [(-135, -42), (135, -42)], GOLD, 8)

        # Torso & regal angavastram
        smooth(ctx, [(-110, -490), (-60, -510), (60, -510), (110, -490), (115, -400), (95, -320), (-95, -320), (-115, -400)])
        ink(ctx, skin)
        # Gold embroidered sash across chest
        smooth(ctx, [(-115, -495), (-70, -510), (105, -360), (80, -330)], k=0.1)
        ink(ctx, GOLD, 6)

        # Regal gold necklace & navaratna pendant
        line(ctx, [(-55, -495), (-25, -465), (0, -460), (25, -465), (55, -495)], GOLD, 7)
        gem(ctx, 0, -450, 9, RED_GEM)

        # Neck & Head
        rrect(ctx, -28, -550, 56, 55, 12)
        ink(ctx, skin)
        ell(ctx, 0, -600, 82, 92)
        ink(ctx, skin)

        # Proud moustache
        smooth(ctx, [(-34, -575), (0, -568), (34, -575), (45, -562), (0, -556), (-45, -562)])
        ink(ctx, hair)

        # Intellectually sharp, visionary eyes
        eye(ctx, -32, -610, 20, 24, t, look=(0.2, -0.1), iris=hexc("#22140A"), seed=5)
        eye(ctx, 32, -610, 20, 24, t, look=(0.2, -0.1), iris=hexc("#22140A"), seed=6)
        line(ctx, [(-50, -642), (-18, -648)], hair, 6)
        line(ctx, [(18, -648), (50, -642)], hair, 6)

        # Tilak on forehead
        line(ctx, [(0, -665), (0, -630)], hexc("#E2231A"), 5)
        circle(ctx, 0, -628, 3.5, GOLD)

        # Vijayanagara Royal Turban (Pagri with Gold Brooch)
        ctx.save()
        ctx.translate(0, -675)
        smooth(ctx, [(-95, 20), (-85, -60), (0, -85), (85, -60), (95, 20)])
        ink(ctx, hexc("#B84218"))
        # Turban gold folds
        for ty in [-35, -15, 5]:
            line(ctx, [(-80, ty), (80, ty)], GOLD, 4)
        # Royal feather crest & jewel
        gem(ctx, 0, -45, 14, GOLD_HI)
        gem(ctx, 0, -45, 8, RED_GEM)
        ctx.restore()

        # Arms: holding ancient palm-leaf architectural blueprint (Tala-patra) & plumb-bob
        L, R = (-105, -480), (105, -480)
        limb(ctx, [L, (-160, -410), (-130, -350)], skin, 40)
        hand(ctx, -130, -350, skin, 24)
        limb(ctx, [R, (150, -420), (130, -340)], skin, 40)
        hand(ctx, 130, -340, skin, 24)

        # Palm-leaf architectural scroll held in hands
        rrect(ctx, -150, -360, 280, 42, 6)
        rgba(ctx, hexc("#D2B882"), 0.96)
        ctx.fill_preserve()
        rgba(ctx, hexc("#6A5228"), 0.9)
        ctx.set_line_width(2.5)
        ctx.stroke()
        # Inscribed Sanskrit architectural lines
        for sy in (-350, -338, -326):
            line(ctx, [(-135, sy), (115, sy)], hexc("#4A3618"), 2)

        ctx.restore()
    group(ctx, a, draw)


def shri_rama(ctx, x, y, s, t, flip=False, a=1.0):
    """Bhagavan Shri Rama: Treta Yuga warrior mukut (NO peacock feather!), Kodanda bow, blessing mudra."""
    def draw():
        place(ctx, x, y, s, t, flip)
        skin = dv.KRISHNA_SKIN   # Divine shyama/neelkanth hue
        hair = dv.KRISHNA_HAIR

        # Radiant divine Rama halo
        halo(ctx, 0, -640, 200, t, c=GOLD)

        # Hair
        ell(ctx, 0, -668, 116, 112)
        ink(ctx, hair)

        # Feet with golden anklets
        for fx in (-50, 50):
            ell(ctx, fx, -14, 44, 18)
            ink(ctx, skin)
            line(ctx, [(fx - 26, -30), (fx, -24), (fx + 26, -30)], GOLD, 7)

        # Saffron dhoti
        dhoti = [(-118, -345), (118, -345), (136, -200), (152, -44), (62, -32), (0, -64), (-62, -32), (-152, -44), (-136, -200)]
        smooth(ctx, dhoti)
        ink(ctx, dv.SAFFRON)
        line(ctx, [(150, -48), (62, -36), (0, -68), (-62, -36), (-150, -48)], hexc("#E8741E"), 12)

        # Torso
        smooth(ctx, [(-122, -500), (-60, -522), (60, -522), (122, -500), (128, -430), (100, -340), (-100, -340), (-128, -430)])
        ink(ctx, skin)

        # Angavastra sash & golden waistbelt
        smooth(ctx, [(-128, -505), (-88, -520), (118, -372), (96, -342)], k=0.1)
        ink(ctx, hexc("#E0502A"), 5)
        rrect(ctx, -114, -366, 228, 34, 12)
        ink(ctx, GOLD, 5)
        gem(ctx, 0, -349, 9, RED_GEM)

        # Gold necklace
        line(ctx, [(-66, -516), (-30, -486), (0, -478), (30, -486), (66, -516)], GOLD, 8)
        gem(ctx, 0, -470, 10, RED_GEM)

        # Neck & Head
        rrect(ctx, -32, -566, 64, 64, 14)
        ink(ctx, skin)
        for side in (-1, 1):
            circle(ctx, side * 104, -604, 13, GOLD)
        ell(ctx, 0, -640, 100, 110)
        ink(ctx, skin)

        # Compassionate, merciful eyes
        for side in (-1, 1):
            eye(ctx, side * 38, -646, 25, 29, t, look=(0.2, 0.3), iris=hexc("#2A1810"), seed=7)
            line(ctx, [(side * 14, -686), (side * 38, -697), (side * 64, -688)], hair, 7)

        # Gentle smile
        ctx.move_to(-20, -594)
        ctx.curve_to(-8, -586, 8, -586, 20, -594)
        ctx.set_line_width(4)
        rgba(ctx, hexc("#B5283C"))
        ctx.stroke()

        # Raghuvanshi Tilak
        line(ctx, [(0, -730), (0, -684)], hexc("#E2231A"), 7)
        line(ctx, [(-6, -720), (-6, -690)], GOLD_HI, 3)
        line(ctx, [(6, -720), (6, -690)], GOLD_HI, 3)

        # Royal Suryavanshi Mukut (Warrior gold crown, NO peacock feather!)
        rrect(ctx, -104, -776, 208, 36, 10)
        ink(ctx, GOLD, 5)
        smooth(ctx, [(-96, -772), (-74, -840), (-40, -820), (0, -895), (40, -820), (74, -840), (96, -772)], k=0.08)
        ink(ctx, GOLD, 5)
        gem(ctx, 0, -825, 16, RED_GEM)

        # Arms: Left shoulder holds Kodanda Bow; Right hand in Abhaya blessing mudra towards Jatayu
        L, R = (-120, -500), (120, -500)
        limb(ctx, [L, (-190, -420), (-160, -480)], skin, 46)
        hand(ctx, -160, -480, skin, 26)
        dv.bow(ctx, -165, -840, -100, -55)

        # Right arm blessing
        limb(ctx, [R, (180, -430), (200, -350)], skin, 46)
        dv.palm(ctx, 200, -350, skin, s=0.9)

        ctx.restore()
    group(ctx, a, draw)


def jatayu_bird(ctx, x, y, s, t, a=1.0):
    """Divine Bird King Jatayu resting devotedly before Lord Rama."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)

        gold_feather = hexc("#D49624")
        dark_feather = hexc("#6A4212")
        crest_gold = hexc("#FFDA52")

        # Soft shadow on ground
        ell(ctx, 0, -6, 160, 24)
        rgba(ctx, (0, 0, 0), 0.35)
        ctx.fill()

        # Folded mighty wings & feathered tail
        smooth(ctx, [(-180, -90), (-120, -40), (-60, -20), (-140, -120)])
        ink(ctx, dark_feather)
        smooth(ctx, [(-150, -110), (-90, -55), (-30, -25), (-110, -130)])
        ink(ctx, gold_feather)

        # Massive feathered body resting gently
        ell(ctx, 0, -95, 130, 80)
        ink(ctx, dark_feather)
        ell(ctx, 10, -100, 115, 68)
        ink(ctx, gold_feather)

        # Feather texture layers
        for fx in range(-60, 80, 25):
            smooth(ctx, [(fx, -80), (fx + 15, -45), (fx + 30, -80)])
            rgba(ctx, hexc("#F0B842"), 0.85)
            ctx.fill()

        # Golden talons / claws resting on ground
        for tx in [30, 70]:
            rrect(ctx, tx, -22, 28, 18, 6)
            ink(ctx, hexc("#52361A"))

        # Neck & Head facing upward toward Rama
        ctx.save()
        ctx.translate(95, -150)
        ctx.rotate(-0.25)
        # Neck
        smooth(ctx, [(-40, 20), (20, 20), (10, -50), (-30, -50)])
        ink(ctx, gold_feather)
        # Head
        ell(ctx, 0, -65, 48, 42)
        ink(ctx, gold_feather)

        # Majestic curved golden eagle beak
        smooth(ctx, [(32, -75), (85, -60), (70, -40), (28, -50)])
        ink(ctx, crest_gold)
        line(ctx, [(30, -60), (75, -52)], hexc("#8A5E12"), 3.5)

        # Devoted, tearful loving eye
        eye(ctx, 12, -75, 14, 16, t, look=(-0.3, -0.4), iris=hexc("#1E120A"), seed=8)

        # Divine royal crest (Kalgi feathers) on head
        smooth(ctx, [(-25, -95), (-10, -135), (10, -130), (5, -95)])
        ink(ctx, crest_gold)
        smooth(ctx, [(-10, -95), (10, -145), (25, -138), (15, -95)])
        ink(ctx, RED_GEM)

        ctx.restore()

        ctx.restore()
    group(ctx, a, draw)


def veerabhadra_swamy(ctx, x, y, s, t, a=1.0):
    """Bhagavan Veerabhadra Swamy: Lord Shiva's fierce protector form with blazing fire halo and Trishul."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)

        # Blazing cosmic fire halo
        halo(ctx, 0, -660, 220, t, c=hexc("#FF6622"))
        glow(ctx, 0, -660, 360, hexc("#FFAA22"), 0.5)

        skin = hexc("#8BB8E8")   # Neelkanth pale blue
        hair = dv.KRISHNA_HAIR

        # Matted locks (Jata)
        ell(ctx, 0, -780, 88, 98)
        ink(ctx, hair)
        for side in (-1, 1):
            smooth(ctx, [(side * 40, -820), (side * 85, -760), (side * 100, -670), (side * 70, -680)])
            ink(ctx, hair)

        # Crescent moon & Ganga in locks
        circle(ctx, -55, -810, 22, hexc("#FFF8D4"))
        circle(ctx, -46, -818, 19, hexc("#10182E"))

        # Head & Face
        ell(ctx, 0, -660, 94, 108)
        ink(ctx, skin)

        # Trinetra (Third Eye of Shiva blazing)
        smooth(ctx, [(0, -725), (14, -705), (0, -685), (-14, -705)], k=0.1)
        rgba(ctx, hexc("#FF4411"), 0.95)
        ctx.fill()
        line(ctx, [(0, -718), (0, -692)], GOLD_HI, 4)

        # Sacred Tripundra
        for ty in (-730, -718, -706):
            line(ctx, [(-42, ty), (42, ty)], WHITE, 3.5)

        # Intense yet protective eyes
        for side in (-1, 1):
            eye(ctx, side * 36, -652, 24, 27, t, look=(0, 0), iris=hexc("#8C1414"), seed=9)
            line(ctx, [(side * 14, -685), (side * 38, -695), (side * 62, -685)], hair, 7)

        # Powerful expression & Neelkanth blue throat
        rrect(ctx, -32, -580, 64, 55, 12)
        ink(ctx, skin)
        circle(ctx, 0, -555, 22, hexc("#224892"), 0.65)

        # Golden Trishul held majestically
        dv.trishul(ctx, -180, -430, 1.3, t)
        flutter = 15 * math.sin(t * 6)
        ctx.move_to(-180, -530)
        ctx.line_to(-250 + flutter, -510)
        ctx.line_to(-230 + flutter, -475)
        ctx.line_to(-180, -500)
        ctx.close_path()
        rgba(ctx, hexc("#E85A1A"), 0.96)
        ctx.fill()

        # Broad warrior chest & Tiger skin (Vyaghrambar)
        smooth(ctx, [(-135, -490), (-70, -515), (70, -515), (135, -490), (140, -390), (100, -290), (-100, -290), (-140, -390)])
        ink(ctx, skin)
        smooth(ctx, [(-130, -300), (130, -300), (150, -120), (0, -100), (-150, -120)])
        ink(ctx, hexc("#D48828"))
        for sy in (-250, -200, -150):
            line(ctx, [(-110, sy), (-60, sy + 15)], hexc("#381A08"), 7)
            line(ctx, [(110, sy), (60, sy + 15)], hexc("#381A08"), 7)

        # Legs standing firm
        for side in (-1, 1):
            limb(ctx, [(side * 55, -280), (side * 60, -140), (side * 55, -25)], skin, 48)
            ell(ctx, side * 60, -14, 44, 18)
            ink(ctx, skin)

        # Right arm raised in powerful Abhaya blessing mudra
        R = (135, -490)
        limb(ctx, [R, (190, -420), (210, -340)], skin, 46)
        dv.palm(ctx, 210, -340, skin, s=0.95)

        ctx.restore()
    group(ctx, a, draw)


def lepakshi_nandi(ctx, x, y, s, t, flip=False, a=1.0):
    """The colossal monolithic granite Nandi of Lepakshi."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        if flip:
            ctx.scale(-s, s)
        else:
            ctx.scale(s, s)

        body_col = hexc("#3C352E")      # Dark monolithic carved granite
        shadow_col = hexc("#241F1A")
        hi_col = hexc("#5A5046")

        # Ground shadow
        ell(ctx, 30, -8, 200, 36)
        rgba(ctx, (0, 0, 0), 0.4)
        ctx.fill()

        # Majestic monolithic Nandi torso & hump
        smooth(ctx, [(-130, -135), (0, -155), (100, -135), (120, -70), (100, -22), (-120, -22), (-150, -65)])
        ink(ctx, body_col)

        # Iconic Zebu hump
        smooth(ctx, [(25, -155), (65, -235), (95, -235), (115, -165)], k=0.12)
        ink(ctx, body_col)
        smooth(ctx, [(30, -155), (65, -230), (80, -230), (70, -155)], k=0.12)
        rgba(ctx, hi_col, 0.45)
        ctx.fill()

        # Folded granite legs
        smooth(ctx, [(75, -70), (120, -50), (135, -20), (95, -14), (65, -40)])
        ink(ctx, body_col)
        rrect(ctx, -95, -20, 30, 16, 5)
        ink(ctx, shadow_col)

        # Royal sculpted bell necklace (Ghanti Mala)
        ctx.move_to(90, -145)
        ctx.curve_to(110, -125, 130, -115, 150, -125)
        ctx.set_line_width(9)
        rgba(ctx, GOLD)
        ctx.stroke()
        for gx, gy in [(95, -140), (112, -126), (128, -120), (145, -126)]:
            circle(ctx, gx, gy, 8, GOLD_HI)

        # Head & curved horns
        ctx.save()
        ctx.translate(155, -185)
        smooth(ctx, [(-28, -50), (40, -44), (70, -12), (65, 26), (22, 34), (-22, 20), (-38, -20)])
        ink(ctx, body_col)
        ell(ctx, 52, 12, 20, 14)
        ink(ctx, shadow_col)

        # Devoted calm eye
        eye(ctx, 14, -18, 17, 13, t, look=(-0.3, -0.3), iris=hexc("#18120C"), seed=10)

        # Sculpted horns with gold rings
        for hx, hy, crv in [(-10, -48, -24), (16, -46, -14)]:
            ctx.move_to(hx, hy)
            ctx.curve_to(hx + crv, hy - 40, hx + crv + 10, hy - 65, hx + crv + 25, hy - 76)
            ctx.set_line_width(13)
            rgba(ctx, shadow_col)
            ctx.stroke()
            circle(ctx, hx + crv + 22, hy - 74, 5, GOLD)

        ctx.restore()

        ctx.restore()
    group(ctx, a, draw)


# ============================================================ SCRIPT SPEC

SPEC = [
    {"key": "hook", "text": "HAWA MEIN JHULTA KHAMBHA",
     "visual": "Lepakshi Temple granite mantapa: Massive carved hanging pillar suspended in mid-air; Priest gently testing the gap with silk cloth",
     "vo": [("tell", [("आंध्र प्रदेश के लेपाक्षी मंदिर में,", "ANDHRA PRADESH KE LEPAKSHI MANDIR MEIN,"),
                      ("पत्थर का एक ऐसा विशाल खंभा है...", "PATTHAR KA EK AISA VISHAAL KHAMBHA HAI..."),
                      ("जो छत से तो जुड़ा है,", "JO CHHAT SE TO JUDA HAI,"),
                      ("लेकिन ज़मीन को छूता तक नहीं!", "LEKIN ZAMEEN KO CHHOOTA TAK NAHI!")])]},

    {"key": "proof", "text": "KAPDA NIKALTA HAI AAR-PAAR",
     "visual": "Close-up of hanging pillar base: Saffron silk cloth glides smoothly through empty space under the pillar without snagging",
     "vo": [("tell", [("लोग इसके नीचे से कपड़ा निकालते हैं,", "LOG ISKE NEECHE SE KAPDA NIKALTE HAIN,"),
                      ("और वह बिना अटके आर-पार हो जाता है!", "AUR WAH BINA ATKE AAR-PAAR HO JAATA HAI!")])]},

    {"key": "engineer", "text": "BRITISH ENGINEER KA PRAPANCH",
     "visual": "British engineer Hamilton tries to dislodge the pillar with crowbar; roof tremors shake the mantapa; engineer recoils in terror",
     "vo": [("tell", [("अंग्रेजी हुकूमत के एक इंजीनियर ने", "ANGREZI HUKUMAT KE EK ENGINEER NE"),
                      ("इसका राज़ जानने के लिए खंभे को हिलाने की कोशिश की...", "ISKA RAAZ JAANNE KE LIYE KHAMBHE KO HILANE KI KOSHISH KI..."),
                      ("लेकिन तभी पूरे मंदिर की छत कांपने लगी!", "LEKIN TABHI POORE MANDIR KI CHHAT KAAMPNE LAGI!"),
                      ("डरकर अंग्रेज उल्टे पैर भाग खड़ा हुआ!", "DARKAR ANGREZ ULTE PAIR BHAAG KHADA HUA!")])]},

    {"key": "architecture", "text": "VIJAYANAGARA ARCHITECTURE",
     "visual": "Chief Architect Virupanna holding palm-leaf Shilpa Shastra blueprints, revealing the interconnected cosmic balance of the temple",
     "vo": [("tell", [("सोलहवीं सदी में विजयनगर साम्राज्य के", "SOLAHVI SADI MEIN VIJAYANAGARA SAMRAJYA KE"),
                      ("महान शिल्पकारों ने इसे ऐसे संतुलित किया था,", "MAHAAN SHILPKAARON NE ISE AISE SANTULIT KIYA THA,"),
                      ("कि इस एक खंभे पर", "KI IS EK KHAMBHE PAR"),
                      ("पूरे मंदिर का गुरुत्वाकर्षण टिका हुआ है!", "POORE MANDIR KA GURUTVAKARSHAN TIKA HUA HAI!")])]},

    {"key": "jatayu", "text": "LE PAKSHI! (UTHO PAKSHI)",
     "visual": "Treta Yuga: Prabhu Shri Rama with Kodanda bow blessing wounded divine bird Jatayu; 'Le Pakshi' lore",
     "vo": [("tell", [("पौराणिक मान्यता है कि", "PAURANIK MAANYATA HAI KI"),
                      ("माता सीता को बचाते हुए घायल जटायु यहीं गिरे थे...", "MATA SITA KO BACHATE HUE GHAYAL JATAYU YAHIN GIRE THE..."),
                      ("और प्रभु श्री राम ने उन्हें मोक्ष देते हुए कहा था—", "AUR PRABHU SHRI RAM NE UNHEIN MOKSHA DETE HUE KAHA THA—"),
                      ("'ले पाक्षी!' यानि 'उठो पक्षी'!", "'LE PAKSHI!' YAANI 'UTHO PAKSHI'!")])]},

    {"key": "veerabhadra", "text": "VEERABHADRA MAHADEV",
     "visual": "Lord Shiva in fierce Veerabhadra form with glowing Trishul and cosmic aura; colossal monolithic Lepakshi Nandi beside Him",
     "vo": [("tell", [("यह पवित्र धाम", "YAH PAVITRA DHAM"),
                      ("भगवान शिव के रौद्र रूप 'वीरभद्र' का है...", "BHAGAWAN SHIV KE RAUDRA ROOP 'VEERABHADRA' KA HAI..."),
                      ("जहाँ की अलौकिक शक्ति और सनातन रहस्य", "JAHAN KI ALAUKIK SHAKTI AUR SANATAN RAHASYA"),
                      ("आज भी आधुनिक विज्ञान से कोसों आगे है!", "AAJ BHI AADHUNIK VIGYAN SE KOSON AAGE HAI!")])]},

    {"key": "cta", "text": "HAR HAR MAHADEV",
     "visual": "Divine golden Shiva Lingam & Trishul in sanctum; flower shower; burning deepams; animated comment pointer arrow",
     "vo": [("tell", [("सनातन भारत की इस अद्भुत कला और", "SANATAN BHARAT KI IS ADBHUT KALA AUR"),
                      ("महादेव के चमत्कार को नमन करते हैं,", "MAHADEV KE CHAMATKAR KO NAMAN KARTE HAIN,"),
                      ("तो कमेंट में लिखिए—", "TO COMMENT MEIN LIKHIYE—"),
                      ("हर हर महादेव!", "HAR HAR MAHADEV!"),
                      ("और सब्सक्राइब कीजिए दिव्य रहस्य!", "AUR SUBSCRIBE KIJIYE DIVYA RAHASYA!")])]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)

HOT = {
    "LEPAKSHI": GOLD_HI, "MANDIR": GOLD, "KHAMBHA": GOLD_HI, "CHHOOTA": RED_GEM, "NAHI!": RED_GEM,
    "KAPDA": WHITE, "AAR-PAAR": GOLD_HI, "VIGYAN": WHITE, "CHUNAUTI": RED_GEM,
    "ENGINEER": WHITE, "HILANE": RED_GEM, "CHHAT": GOLD, "KAAMPNE": RED_GEM, "BHAAG": RED_GEM,
    "VIJAYANAGARA": GOLD_HI, "SHILPKAARON": WHITE, "SANTULIT": GOLD, "GURUTVAKARSHAN": GOLD_HI,
    "JATAYU": GOLD_HI, "RAM": GOLD_HI, "MOKSHA": GOLD, "PAKSHI!": GOLD_HI,
    "VEERABHADRA": GOLD_HI, "SHIV": GOLD_HI, "ROOP": GOLD, "ALAUKIK": GOLD, "SANATAN": GOLD,
    "CHAMATKAR": GOLD_HI, "HAR": GOLD, "MAHADEV!": GOLD_HI, "COMMENT": GOLD, "DIVYA": GOLD, "RAHASYA!": GOLD
}


# ============================================================ SCENES

class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"lepakshi": c("LEPAKSHI", 1.2), "khambha": c("KHAMBHA", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["lepakshi"], "whoosh"), (b["khambha"], "shankh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        temple_mantapa_bg(ctx, t)

        # Hanging Pillar in center-right
        hanging_pillar(ctx, 640, GROUND - 10, 0.88, t, cloth_u=0.0)

        # Devotee sitting on left reaching toward gap
        pujari_devotee(ctx, 300, GROUND - 10, 0.72, t, kneeling=True)

        title_card(ctx, "LEPAKSHI HANGING PILLAR", "HAWA MEIN JHULTA KHAMBHA", 0.95)

        if t > b["khambha"]:
            ribbon(ctx, 540, 480, "HAWA MEIN JHULTA KHAMBHA", RED_GEM, t - b["khambha"])


class Proof(Cued):
    def beats(self, d):
        c = self.cue
        return {"kapda": c("KAPDA", 1.0), "vigyan": c("VIGYAN", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["kapda"], "shimmer"), (b["vigyan"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        temple_mantapa_bg(ctx, t)

        # Close-up scale of hanging pillar to prominently reveal the cloth passing through
        cloth_prog = clamp((t - b["kapda"]) / max(0.1, d - b["kapda"] - 0.5), 0.0, 1.0)
        hanging_pillar(ctx, 540, GROUND + 40, 1.05, t, cloth_u=cloth_prog)

        # Devotees on both sides guiding the cloth
        pujari_devotee(ctx, 230, GROUND - 10, 0.74, t, kneeling=True, flip=False)
        pujari_devotee(ctx, 850, GROUND - 10, 0.74, t, kneeling=True, flip=True)

        ribbon(ctx, 540, 340, "KAPDA NIKALTA HAI AAR-PAAR", hexc("#1A3A5E"), 1.0)


class Engineer(Cued):
    def beats(self, d):
        c = self.cue
        return {"engineer": c("ENGINEER", 1.2), "chhat": c("CHHAT", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["engineer"], "whoosh"), (b["chhat"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        tremor = clamp((t - b["chhat"]) / 2.0, 0.0, 1.0) if t > b["chhat"] else 0.0

        # Shaking mantapa background as engineer forces the pillar
        temple_mantapa_bg(ctx, t, shake=tremor)

        # Pillar slightly tilting under mechanical pry
        tilt_ang = 0.03 * math.sin(t * 8) * tremor
        hanging_pillar(ctx, 680, GROUND - 10, 0.88, t, tilt=tilt_ang)

        # Terrified British engineer recoiling on the left
        british_engineer(ctx, 270, GROUND - 10, 0.74, t, pose="shock" if tremor > 0 else "pry")

        # Falling stone dust particles during tremor
        if tremor > 0:
            for i in range(24):
                dx = (rnd(i, 61) * W + 40 * math.sin(t * 15 + i)) % W
                dy = (180 + t * 450 * (0.8 + rnd(i, 62))) % H
                circle(ctx, dx, dy, 2.5 + 2 * rnd(i, 63), hexc("#C2B4A0"), 0.5)

        ribbon(ctx, 540, 340, "BRITISH ENGINEER KA PRAPANCH", hexc("#5A1820"), 1.0)


class Architecture(Cued):
    def beats(self, d):
        c = self.cue
        return {"shilpkaar": c("SHILPKAARON", 1.3), "gurutva": c("GURUTVAKARSHAN", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["shilpkaar"], "ghanti"), (b["gurutva"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        temple_mantapa_bg(ctx, t)

        # Hanging pillar with cosmic geometric balance lines radiating
        hanging_pillar(ctx, 680, GROUND - 10, 0.86, t)

        # Golden architectural equilibrium lines connecting pillar to ceiling and roof
        if t > b["gurutva"]:
            u_g = clamp((t - b["gurutva"]) / 1.0, 0.0, 1.0)
            ctx.save()
            ctx.set_line_width(3)
            rgba(ctx, GOLD, 0.75 * u_g)
            # Equilibrium vectors
            line(ctx, [(680, 200), (450, 400)], GOLD, 3)
            line(ctx, [(680, 200), (910, 400)], GOLD, 3)
            circle(ctx, 680, 200, 12, GOLD_HI)
            circle(ctx, 680, GROUND - 35, 14, GOLD_HI)
            ctx.restore()

        # Chief Architect Virupanna holding palm-leaf blueprints on left
        architect_virupanna(ctx, 270, GROUND - 10, 0.75, t)

        ribbon(ctx, 540, 340, "VIJAYANAGARA ARCHITECTURAL GENIUS", hexc("#1A4870"), 1.0)


class Jatayu(Cued):
    def beats(self, d):
        c = self.cue
        return {"jatayu": c("JATAYU", 1.2), "pakshi": c("PAKSHI!", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["jatayu"], "whoosh"), (b["pakshi"], "shankh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        # Sacred twilight sky & sacred rocky ground of Lepakshi
        dv.sky(ctx, hexc("#1A1428"), hexc("#4A2234"), hexc("#B85A28"), 0.58)
        glow(ctx, 540, 720, 420, hexc("#FFAA48"), 0.45)

        # Sacred rocky boulder landscape
        ctx.rectangle(0, GROUND - 60, W, H - GROUND + 60)
        rgba(ctx, hexc("#2A2018"))
        ctx.fill()

        # Prabhu Shri Rama standing on left in blessing mudra
        shri_rama(ctx, 320, GROUND - 10, 0.74, t)

        # Divine bird Jatayu resting on right devotedly looking up at Rama
        jatayu_bird(ctx, 720, GROUND - 10, 0.78, t)

        # Shower of celestial flower petals
        for i in range(16):
            px = (rnd(i, 71) * W + t * 22 * (0.6 + rnd(i, 72))) % W
            py = 350 + 800 * rnd(i, 73)
            circle(ctx, px, py, 3 + 2.5 * rnd(i, 74), GOLD_HI, 0.4 + 0.3 * math.sin(t * 4 + i))

        ribbon(ctx, 540, 340, "LE PAKSHI! (UTHO PAKSHI)", hexc("#963412"), 1.0)


class Veerabhadra(Cued):
    def beats(self, d):
        c = self.cue
        return {"veerabhadra": c("VEERABHADRA", 1.2), "alaukik": c("ALAUKIK", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["veerabhadra"], "shankh"), (b["alaukik"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        # Deep cosmic sanctum aura
        dv.sky(ctx, hexc("#0A0E1C"), hexc("#1C1E3C"), hexc("#3C142A"), 0.55)
        temple_mantapa_bg(ctx, t)

        # Bhagavan Veerabhadra Swamy on the left with flaming halo & Trishul
        veerabhadra_swamy(ctx, 360, GROUND - 10, 0.74, t)

        # Colossal Monolithic Lepakshi Nandi seated on the right facing Him
        lepakshi_nandi(ctx, 790, GROUND - 10, 0.68, t, flip=True)

        ribbon(ctx, 540, 340, "DEVADHIDEV VEERABHADRA DHAM", hexc("#1A2454"), 1.0)


class Cta(Cued):
    def beats(self, d):
        c = self.cue
        return {"mahadev": c("MAHADEV!", 1.8), "comment": c("COMMENT", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["mahadev"], "shankh"), (b["comment"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        temple_mantapa_bg(ctx, t)

        # Golden Shiva Lingam & glowing Trishul in center
        glow(ctx, 540, 820, 360, GOLD, 0.7)
        dv.trishul(ctx, 540, 880, 1.2, t)

        # Floating spiritual petals
        for i in range(18):
            px = (rnd(i, 81) * W + t * 24 * (0.6 + rnd(i, 82))) % W
            py = 400 + 900 * rnd(i, 83)
            circle(ctx, px, py, 3 + 2.5 * rnd(i, 84), GOLD_HI, 0.4 + 0.3 * math.sin(t * 4 + i))

        # Top prompt ribbon
        ribbon(ctx, 540, 340, "COMMENT MEIN LIKHIYE:", hexc("#101828"), 1.0)
        text(ctx, "HAR HAR MAHADEV", 540, 440, 68, GOLD_HI, font=CAPTION_FONT, bold=True, stroke=(0, 0, 0), stroke_w=14)

        # Animated pointer arrow pointing towards YouTube Shorts comment button
        arrow_y = 1380 + 15 * math.sin(t * 6)
        ctx.save()
        ctx.translate(920, arrow_y)
        ctx.rotate(0.3)
        line(ctx, [(0, 60), (0, -40)], GOLD, 14)
        ctx.move_to(0, -65)
        ctx.line_to(-28, -25)
        ctx.line_to(28, -25)
        ctx.close_path()
        rgba(ctx, GOLD_HI)
        ctx.fill()
        ctx.restore()


SCENE_CLASSES = {
    "hook": Hook,
    "proof": Proof,
    "engineer": Engineer,
    "architecture": Architecture,
    "jatayu": Jatayu,
    "veerabhadra": Veerabhadra,
    "cta": Cta,
}
STORY = sys.modules[__name__]


def write_alignment(final):
    import json
    out = [
        {
            "scene": spec["key"],
            "start": round(s["start"], 3),
            "end": round(s["start"] + s["dur"], 3),
            "voiceover": NARRATION[spec["key"]],
            "on_screen_text": spec["text"],
            "visual": spec["visual"],
            "words": [{"t": round(s["start"] + st, 3), "w": w} for st, w in s["captions"]]
        }
        for spec, s in zip(SPEC, engine.SCENES)
    ]
    path = final.with_suffix(".json")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Alignment: {path}")


# ============================================================ UPLOAD KIT

UPLOAD = {
    "titles": [
        "Lepakshi Temple Ke Hanging Pillar Ka Rahasya Jo Vigyan Bhi Nahi Samajh Paya",
        "Hawa Mein Jhulta Khambha: Lepakshi Mandir Ka Sabse Bada Rahasya!",
        "Lepakshi Hanging Pillar Mystery: Angrez Engineer Ne Hilaya To Mandir Hil Gaya!",
        "Lepakshi Mandir Ka Rahasya: Zameen Se Upar Kyun Jhulta Hai Ye Khambha?",
        "Le Pakshi: Jatayu, Shri Rama Aur Veerabhadra Mandir Ka Chamatkar",
    ],
    "title": "Lepakshi Temple Ke Hanging Pillar Ka Rahasya Jo Vigyan Bhi Nahi Samajh Paya",
    "thumb_text": "HAWA MEIN KHAMBHA?",
    "queries": ["lepakshi temple hanging pillar mystery", "lepakshi mandir rahasya", "hanging pillar of lepakshi"],
    "description": """Lepakshi Temple Ke Hanging Pillar Ka Rahasya Jo Vigyan Bhi Nahi Samajh Paya!
Andhra Pradesh ke prasiddh Lepakshi (Veerabhadra) mandir me 70 vishaal patthar ke khambhe hain...
Lekin inme se ek aisa chamatkari khambha hai jo chhat se to juda hai, par zameen ko chhoota tak nahi!

Is katha me janiye:
• Hawa me jhulte khambhe ke neeche se kapda nikalne ka adbhut rahasya
• British engineer Hamilton ne jab khambha hilane ki koshish ki, to poora mandir kyun hilne laga?
• 16vi sadi ke Vijayanagara shilpkaaron ka adbhut architectural balance
• Ramayana kaal me Prabhu Shri Ram aur Jatayu ka 'Le Pakshi' (उठो पक्षी!) ka divya prasang
• Bhagawan Shiva ke krodh se janme Veerabhadra Swamy aur vishaal monolithic Nandi ka dham

Sanatan Sanskriti ke is adbhut chamatkar ke liye comment me श्रद्धा se likhiye: Har Har Mahadev!
Subscribe kijiye Divya Rahasya channel ko aisi hi anokhi sanatan kathaon ke liye.

#Shorts #LepakshiTemple #HangingPillar #HarHarMahadev
""",
    "tags": ["lepakshi temple", "hanging pillar", "lepakshi mandir rahasya", "veerabhadra temple", "har har mahadev",
             "british engineer mystery", "ancient indian architecture", "jatayu rama", "sanatan katha", "divya rahasya"],
    "hashtags": ["#Shorts", "#LepakshiTemple", "#HangingPillar", "#HarHarMahadev"],
}


def thumbnail(ctx):
    """1080x1920 cover: Magnificent Hanging Pillar of Lepakshi with cloth passing under it and Veerabhadra Swamy."""
    temple_mantapa_bg(ctx, 0.5)

    # Hanging pillar prominently centered
    hanging_pillar(ctx, 540, 920, 1.0, 0.5, cloth_u=0.55)

    # Devotee on left sliding cloth, Veerabhadra manifestation aura
    pujari_devotee(ctx, 220, GROUND - 10, 0.72, 0.5, kneeling=True)
    glow(ctx, 820, 800, 360, hexc("#FF7722"), 0.5)
    veerabhadra_swamy(ctx, 840, GROUND - 10, 0.68, 0.5)

    # Vignettes
    g = cairo.LinearGradient(0, 1150, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.92)
    ctx.rectangle(0, 1150, W, H - 1150)
    ctx.set_source(g)
    ctx.fill()

    g = cairo.LinearGradient(0, 0, 0, 780)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.94)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 780)
    ctx.set_source(g)
    ctx.fill()

    vignette(ctx)
    text(ctx, "HAWA MEIN KHAMBHA?", 540, 290, 105, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "LEPAKSHI MANDIR", 540, 440, 95, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    ribbon(ctx, 540, 600, "VIGYAN BHI DANG!", RED_GEM, 1.0)
    text(ctx, "DIVYA RAHASYA", 540, 1800, 40, GOLD, a=0.7)


def main() -> None:
    story = sys.modules[__name__]
    story.__name__ = "kathas.lepakshi"

    if "--check" in sys.argv:
        from core import policy
        policy.check(story, "lepakshi")
        print("[policy] OK - all checks passed!")
        return

    if "--preview" in sys.argv:
        import make
        make.preview("lepakshi")
        return

    engine.make_frame = katha.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()

