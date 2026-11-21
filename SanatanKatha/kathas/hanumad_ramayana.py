"""Hanumad Ramayana: Hanuman Ji Ne Apni Ramayana Samudra Mein Kyun Baha Di? (~30-35s katha, seven scenes).

Usage (from SanatanKatha/):
  python make.py hanumad_ramayana --preview       # preview contact sheet & thumbnail
  python make.py hanumad_ramayana --kiki-export   # exports clean voice text files
  python make.py hanumad_ramayana --kiki-split    # splits user audio into lines
  python make.py hanumad_ramayana                 # final render with music & devta characters

Rahasya:
Before Maharshi Valmiki's Ramayana gained cosmic renown, another complete Ramayana was written:
the Hanumad Ramayana, engraved by Pawanputra Hanuman himself with his sharp nails onto Himalayan
rock monoliths at Mount Gandhamadana. When Maharshi Valmiki read its divine verses, he wept knowing
his own epic would pale before its celestial beauty. Seeing a fellow devotee's grief, Hanuman Ji
lifted the colossal rock slab and cast it into the cosmic ocean, proving that a true devotee seeks
neither literary fame nor pride, but only selfless love for Prabhu Shri Ram.
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

TOPIC = "HANUMAD RAMAYANA SAMUDRA VISARJAN"
OUTPUTS = {"edge": "hanumad_ramayana_short.mp4"}
MUSIC_STYLE = "ambient"   # Fresh cinematic ambient pads (no loud conch horn)
MUSIC_BPM = 86            # Calm, reverent, devotional pace
MUSIC_VOLUME = 0.12       # Clear dialogue clarity
TAIL_PAD = 0.04           # Seamless transition between scene chunks
MAX_GAP = 0.04            # Zero awkward silence

WHITE = (1.0, 1.0, 1.0)
RED_GEM = hexc("#D61F3A")
HANUMAN_ORANGE = hexc("#E05B16")
HANUMAN_SHADE = hexc("#B44208")
ROCK_DARK = hexc("#2A2D34")
ROCK_LIGHT = hexc("#4E5360")
GOLD_TEXT = hexc("#FFE082")
OCEAN_DARK = hexc("#0B1B3D")
OCEAN_MED = hexc("#153A6B")
OCEAN_FOAM = hexc("#D6F0FF")

SOURCES = [
    "Skanda Purana & Hanumad-Nataka: Hanuman inscribes the story of Rama on the rocks of the Himalayas; Valmiki reads it and weeps fearing his epic will be eclipsed.",
    "Bhavishyottara Purana: Highlights Hanuman Ji's selfless sacrifice of discarding the stone monolith into the ocean so that Valmiki's Ramayana may flourish among mankind.",
    "Valmiki tradition: Demonstrates supreme Nishkama Bhakti where ego, authorship, and fame are dissolved in pure love for the Divine.",
]


# -----------------------------------------------------------------------------
# Background Scenery Renderers
# -----------------------------------------------------------------------------
def himalaya_bg(ctx, t, sunset=True):
    """Majestic Himalayan peaks at sunset/twilight with sacred cosmic aura."""
    if sunset:
        dv.sky(ctx, hexc("#10162E"), hexc("#5A2846"), hexc("#D46B34"), 0.58)
        glow(ctx, 540, 700, 420, hexc("#FFA842"), 0.40)
        circle(ctx, 540, 700, 75, hexc("#FFE6A0"), 0.85)
    else:
        dv.sky(ctx, hexc("#0A1024"), hexc("#1C2548"), hexc("#3C1E40"), 0.58)
        glow(ctx, 540, 660, 360, hexc("#70A8FF"), 0.32)

    # Distant towering snow peaks
    ctx.move_to(0, 880)
    peaks = [(150, 720), (320, 840), (520, 680), (740, 830), (920, 710), (1080, 860)]
    for px, py in peaks:
        ctx.line_to(px, py + 15 * math.sin(px / 120 + t * 0.2))
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    rgba(ctx, hexc("#322544") if sunset else hexc("#1B233D"))
    ctx.fill()

    # Snow ridge highlights
    ctx.set_line_width(4)
    for px, py in peaks:
        line(ctx, [(px - 60, py + 70), (px, py), (px + 70, py + 80)], hexc("#E8D8F0"), 3)

    # Mid-ground rugged pine/rock ridge
    ctx.move_to(0, 990)
    for x in range(0, W + 1, 35):
        ctx.line_to(x, 990 - 28 * math.sin(x / 140 + 1.2) - 12 * math.cos(x / 55))
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    rgba(ctx, hexc("#1A1224") if sunset else hexc("#101626"))
    ctx.fill()


def ocean_bg(ctx, t):
    """Dramatic cosmic ocean with breaking crests and twilight atmosphere."""
    dv.sky(ctx, hexc("#080D1E"), hexc("#1A2542"), hexc("#284566"), 0.55)
    glow(ctx, 540, 640, 400, hexc("#4C8DDC"), 0.35)
    circle(ctx, 540, 640, 70, hexc("#DDF0FF"), 0.80)

    # Rolling ocean horizon and waves
    for layer, (y_base, col, spd) in enumerate([(820, OCEAN_DARK, 1.0), (920, OCEAN_MED, 1.4), (1040, hexc("#0E2648"), 1.8)]):
        ctx.move_to(0, y_base)
        for x in range(0, W + 1, 30):
            wy = y_base + 16 * math.sin(x / 90 + t * 2.2 * spd + layer) + 8 * math.cos(x / 40 - t * spd)
            ctx.line_to(x, wy)
        ctx.line_to(W, H)
        ctx.line_to(0, H)
        ctx.close_path()
        rgba(ctx, col)
        ctx.fill()

        # Foam crest lines
        for fx in range(30, W, 80):
            fy = y_base + 16 * math.sin(fx / 90 + t * 2.2 * spd + layer)
            line(ctx, [(fx - 24, fy + 2), (fx + 24, fy - 2)], OCEAN_FOAM, 3)


# -----------------------------------------------------------------------------
# Character & Prop Primitives
# -----------------------------------------------------------------------------
def rock_monolith(ctx, x, y, s, t, glow_verses=True, lift=False):
    """Colossal stone slab inscribed with glowing Sanskrit verses of Hanumad Ramayana."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # Monolith stone body
    pts = [(-160, -320), (150, -335), (175, 40), (140, 340), (-145, 340), (-170, 30)]
    smooth(ctx, pts)
    ink(ctx, ROCK_DARK)
    ctx.fill_preserve()
    rgba(ctx, ROCK_LIGHT, 0.4)
    ctx.set_line_width(6)
    ctx.stroke()

    # Surface cracks & chiseled texture
    line(ctx, [(-120, -280), (-80, -200), (-110, -110)], hexc("#1A1C22"), 4)
    line(ctx, [(90, -260), (120, -170), (85, -80)], hexc("#1A1C22"), 4)
    line(ctx, [(-60, 120), (-30, 220), (-80, 290)], hexc("#1A1C22"), 4)

    # Engraved glowing verses (Sanskrit rhythmic lines)
    if glow_verses:
        pulse = 0.8 + 0.2 * math.sin(t * 3.5)
        glow(ctx, 0, 0, 240, GOLD, 0.28 * pulse)

        # Sanskrit-like engraved horizontal stanzas with golden luster
        for i, row_y in enumerate(range(-240, 260, 48)):
            w_line = 240 - abs(row_y) * 0.25
            line(ctx, [(-w_line / 2, row_y), (w_line / 2, row_y)], GOLD_HI, 5 * pulse)
            # Small character glyph dots
            for gx in range(int(-w_line / 2) + 15, int(w_line / 2) - 10, 28):
                dot_y = row_y + 10 + 4 * math.sin(gx + i)
                circle(ctx, gx, dot_y, 4, GOLD_TEXT, 0.95 * pulse)

    ctx.restore()


def hanuman(ctx, x, y, s, t, pose="namaste", flip=False, a=1.0):
    """Pawanputra Hanuman: Divine sindoori skin, golden mukut, tailored for Hanumad Ramayana."""
    def draw():
        place(ctx, x, y, s, t, flip)
        halo_y = -680 if pose == "lift_rock" else -620
        halo(ctx, 0, halo_y, 185, t, c=GOLD)
        skin = HANUMAN_ORANGE

        # Vanara Tail
        if pose == "lift_rock":
            tail_pts = [(-50, -320), (-140, -420), (-210, -560), (-190, -740), (-120, -820)]
            limb(ctx, tail_pts, skin, 30)
            circle(ctx, -120, -820, 16, skin)
        else:
            tail_pts = [(-50, -310), (-140, -360), (-180, -480), (-160, -620), (-90, -700), (-40, -720)]
            limb(ctx, tail_pts, skin, 28)
            circle(ctx, -40, -720, 16, skin)

        # Hair / Fur behind shoulders
        for side in (-1, 1):
            smooth(ctx, [(side * 60, -660), (side * 115, -590), (side * 125, -520), (side * 110, -460), (side * 80, -470), (side * 75, -540)])
            ink(ctx, hexc("#5A2008"))
        ell(ctx, 0, -638, 108, 106)
        ink(ctx, hexc("#5A2008"))

        # Strong legs & feet with golden anklets
        for fx in (-52, 52):
            ell(ctx, fx, -14, 46, 20)
            ink(ctx, skin)
            line(ctx, [(fx - 26, -30), (fx, -24), (fx + 26, -30)], GOLD, 7)

        # Saffron & Golden Dhoti
        dhoti = [(-110, -330), (110, -330), (128, -200), (142, -50), (60, -36), (0, -60), (-60, -36), (-142, -50), (-128, -200)]
        smooth(ctx, dhoti)
        ink(ctx, GOLD)
        line(ctx, [(140, -52), (60, -38), (0, -62), (-60, -38), (-140, -52)], hexc("#E8741E"), 10)

        # Muscular Torso
        smooth(ctx, [(-128, -480), (-65, -506), (65, -506), (128, -480), (134, -410), (105, -330), (-105, -330), (-134, -410)])
        ink(ctx, skin)
        sheen(ctx, 0, -410, 80, 50, 0.12)

        # Janeu & Garland
        line(ctx, [(-100, -490), (-50, -450), (20, -390), (95, -330)], WHITE, 4)
        line(ctx, [(-70, -490), (-35, -455), (0, -440), (35, -455), (70, -490)], GOLD, 7)
        gem(ctx, 0, -435, 10, RED_GEM)

        # Kamarbandh
        rrect(ctx, -112, -350, 224, 30, 10)
        ink(ctx, GOLD, 5)
        gem(ctx, 0, -335, 8, RED_GEM)

        # Neck & Divine Vanara Head
        rrect(ctx, -34, -546, 68, 60, 14)
        ink(ctx, skin)
        for side in (-1, 1):
            ell(ctx, side * 96, -616, 20, 26)
            ink(ctx, skin)
            circle(ctx, side * 102, -586, 12, GOLD)
        ell(ctx, 0, -616, 96, 102)
        ink(ctx, skin)

        # Muzzle/jaw
        smooth(ctx, [(-42, -580), (42, -580), (36, -538), (0, -528), (-36, -538)])
        ink(ctx, hexc("#F4803A"))

        # Tilak
        line(ctx, [(0, -690), (0, -650)], hexc("#E2231A"), 8)
        line(ctx, [(-6, -684), (-6, -656)], GOLD_HI, 3)
        line(ctx, [(6, -684), (6, -656)], GOLD_HI, 3)

        # Eyes
        for side in (-1, 1):
            eye(ctx, side * 36, -624, 23, 26, t, look=(0, 0), iris=hexc("#3B1808"), seed=1)
            line(ctx, [(side * 14, -652), (side * 36, -660), (side * 60, -654)], hexc("#5A2008"), 6)

        # Divine smile
        ctx.move_to(-18, -554)
        ctx.curve_to(-6, -546, 6, -546, 18, -554)
        ctx.set_line_width(4)
        rgba(ctx, hexc("#8A1810"))
        ctx.stroke()

        # Mukut
        mukut = [(-76, -698), (-56, -788), (0, -840), (56, -788), (76, -698), (0, -710)]
        smooth(ctx, mukut)
        ink(ctx, GOLD, 5)
        gem(ctx, 0, -770, 12, RED_GEM)

        # Arm Poses
        if pose == "carve":
            # Right arm raised with sharp glowing nail carving rock
            limb(ctx, [(118, -470), (170, -460), (195, -530)], skin, 38)
            hand(ctx, 195, -530, skin, 22)
            # Sharp glowing nail beam
            circle(ctx, 205, -545, 10, GOLD_HI)
            line(ctx, [(205, -545), (230, -560)], GOLD_HI, 6)
            glow(ctx, 215, -550, 45, GOLD, 0.7)
            # Left arm steady at side/chest
            limb(ctx, [(-118, -470), (-145, -410), (-120, -320)], skin, 36)
            hand(ctx, -120, -310, skin, 22)

        elif pose == "lift_rock":
            # Both muscular arms raised high overhead lifting colossal rock
            limb(ctx, [(-118, -470), (-150, -560), (-110, -680)], skin, 42)
            dv.palm(ctx, -110, -690, skin, ang=-0.3, s=1.2)
            limb(ctx, [(118, -470), (150, -560), (110, -680)], skin, 42)
            dv.palm(ctx, 110, -690, skin, ang=0.3, s=1.2)

        elif pose == "abhaya":
            limb(ctx, [(118, -470), (170, -420), (160, -320)], skin, 38)
            dv.palm(ctx, 160, -310, skin, ang=-0.1, s=1.15)
            limb(ctx, [(-118, -470), (-145, -410), (-110, -340)], skin, 36)
            hand(ctx, -110, -330, skin, 22)

        elif pose == "namaste":
            limb(ctx, [(-118, -470), (-70, -420), (-25, -420)], skin, 36)
            limb(ctx, [(118, -470), (70, -420), (25, -420)], skin, 36)
            circle(ctx, -26, -420, 16, GOLD)
            circle(ctx, 26, -420, 16, GOLD)
            smooth(ctx, [(-20, -440), (0, -460), (20, -440), (12, -410), (-12, -410)])
            ink(ctx, skin)

        ctx.restore()
    group(ctx, a, draw)


def maharshi_valmiki(ctx, x, y, s, t, pose="read", flip=False, a=1.0):
    """Adi Kavi Maharshi Valmiki: Flowing white beard, ascetic jata, rudraksha mala, palm-leaf manuscript."""
    def draw():
        place(ctx, x, y, s, t, flip)
        halo(ctx, 0, -620, 150, t, c=hexc("#FFCC66"), a=0.65)
        skin = hexc("#D29E74")

        # Ascetic Gerua / Saffron Dhoti & Vastra
        robe = [(-110, -500), (110, -500), (130, -50), (50, -30), (0, -40), (-50, -30), (-130, -50)]
        smooth(ctx, robe)
        ink(ctx, hexc("#C85520"))

        # Rudraksha Mala across chest
        line(ctx, [(-60, -500), (-30, -440), (0, -420), (30, -440), (60, -500)], hexc("#5A2610"), 8)

        # Head & Ascetic Topknot
        rrect(ctx, -30, -540, 60, 50, 12)
        ink(ctx, skin)
        ell(ctx, 0, -600, 85, 90)
        ink(ctx, skin)

        # Matted Hair (Jata) topknot
        circle(ctx, 0, -690, 48, hexc("#4A3020"))

        # Flowing White/Silver Beard
        beard = [(-55, -590), (55, -590), (45, -490), (0, -430), (-45, -490)]
        smooth(ctx, beard)
        ink(ctx, hexc("#ECEAE6"))

        # Eyes & Brow
        for side in (-1, 1):
            eye(ctx, side * 30, -610, 20, 22, t, look=(0.2, 0.1), iris=hexc("#221008"))
            line(ctx, [(side * 12, -630), (side * 45, -634)], hexc("#ECEAE6"), 5)

        # Tear drops in 'tears' pose
        if pose == "tears":
            for side in (-1, 1):
                circle(ctx, side * 30 + 8, -580, 5, hexc("#80D0FF"), 0.9)
                line(ctx, [(side * 30 + 8, -580), (side * 30 + 8, -560)], hexc("#80D0FF"), 3)

        # Arm & Manuscript Poses
        if pose == "read":
            # Both hands holding open palm-leaf manuscript (taal-patra)
            limb(ctx, [(-95, -480), (-60, -430), (-30, -390)], skin, 30)
            limb(ctx, [(95, -480), (60, -430), (30, -390)], skin, 30)
            # Palm-leaf bundle (golden-brown leaf with ties)
            rrect(ctx, -65, -410, 130, 32, 6)
            ink(ctx, hexc("#D4B07B"))
            line(ctx, [(-55, -394), (55, -394)], hexc("#7A4E1D"), 3)

        elif pose == "tears":
            # One hand holding palm leaves loosely, other hand touching face/eyes in grief
            limb(ctx, [(-95, -480), (-120, -420), (-90, -340)], skin, 30)
            hand(ctx, -90, -330, skin, 20)
            # Palm-leaf manuscript resting at waist
            rrect(ctx, -130, -350, 75, 24, 5)
            ink(ctx, hexc("#D4B07B"))
            # Right hand raised to eyes wiping tears
            limb(ctx, [(95, -480), (110, -540), (45, -570)], skin, 30)
            hand(ctx, 45, -570, skin, 20)

        elif pose == "wonder":
            # Both hands raised in awe/astonishment
            limb(ctx, [(-95, -480), (-140, -430), (-120, -360)], skin, 30)
            dv.palm(ctx, -120, -350, skin, ang=0.2, s=1.0)
            limb(ctx, [(95, -480), (140, -430), (120, -360)], skin, 30)
            dv.palm(ctx, 120, -350, skin, ang=-0.2, s=1.0)

        ctx.restore()
    group(ctx, a, draw)


def shri_ram(ctx, x, y, s, t, pose="bless", flip=False, a=1.0):
    """Maryada Purushottam Shri Ram: Royal mukut, blessing devotee in divine golden aura."""
    def draw():
        place(ctx, x, y, s, t, flip)
        halo(ctx, 0, -650, 180, t, c=GOLD_HI)
        skin = dv.KRISHNA_SKIN
        hair = dv.KRISHNA_HAIR

        # Hair behind shoulders
        for side in (-1, 1):
            smooth(ctx, [(side * 70, -700), (side * 122, -620), (side * 138, -540), (side * 128, -470), (side * 98, -480), (side * 88, -560)])
            ink(ctx, hair)
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

        # Torso
        smooth(ctx, [(-122, -500), (-60, -522), (60, -522), (122, -500), (128, -430), (100, -340), (-100, -340), (-128, -430)])
        ink(ctx, skin)

        # Angavastra sash
        smooth(ctx, [(-128, -505), (-88, -520), (118, -372), (96, -342)], k=0.1)
        ink(ctx, hexc("#E0502A"), 5)

        # Kamarbandh
        rrect(ctx, -114, -366, 228, 34, 12)
        ink(ctx, GOLD, 5)
        gem(ctx, 0, -349, 9, RED_GEM)

        # Head & Divine Face
        rrect(ctx, -32, -572, 64, 58, 14)
        ink(ctx, skin)
        ell(ctx, 0, -642, 92, 98)
        ink(ctx, skin)

        # Raghuvanshi Tilak
        line(ctx, [(0, -718), (0, -675)], hexc("#E2231A"), 8)
        circle(ctx, 0, -668, 5, GOLD)

        # Eyes
        for side in (-1, 1):
            eye(ctx, side * 34, -648, 22, 24, t, look=(0, 0), iris=hexc("#1B2A4A"), seed=0)
            line(ctx, [(side * 12, -674), (side * 34, -682), (side * 56, -676)], hexc("#0E1628"), 5)

        # Royal Mukut (no peacock feather)
        mukut = [(-72, -722), (-52, -812), (0, -864), (52, -812), (72, -722), (0, -734)]
        smooth(ctx, mukut)
        ink(ctx, GOLD, 5)
        gem(ctx, 0, -794, 11, RED_GEM)

        # Arms: Abhaya blessing hand lovingly raised towards Hanuman
        limb(ctx, [(112, -490), (160, -430), (140, -340)], skin, 36)
        dv.palm(ctx, 140, -330, skin, ang=-0.1, s=1.1)
        limb(ctx, [(-112, -490), (-145, -420), (-120, -320)], skin, 36)
        hand(ctx, -120, -310, skin, 22)

        ctx.restore()
    group(ctx, a, draw)


# -----------------------------------------------------------------------------
# Story specification: 7 scenes (~30-35s total, 98 spoken Hindi words)
# -----------------------------------------------------------------------------
SPEC = [
    {
        "key": "hook",
        "text": "HANUMAD RAMAYANA?",
        "visual": "Mount Gandhamadana: Hanuman Ji with glowing aura beside an engraved rock monolith",
        "vo": [
            ("open", [("वाल्मीकि रामायण से पहले,", "VALMIKI RAMAYANA SE PEHLE,")], 0.02),
            ("punch", [("एक और रामायण लिखी गई थी—", "EK AUR RAMAYANA LIKHI GAYI THI—"), ("हनुमत रामायण!", "HANUMAD RAMAYANA!")], 0.04),
            ("build", [("जिसे खुद हनुमान जी ने", "JISE KHUD HANUMAN JI NE"), ("समुद्र में बहा दिया।", "SAMUDRA MEIN BAHA DIYA.")], 0.02),
            ("ask", [("क्यों?", "KYUN?")], 0.04),
        ],
    },
    {
        "key": "himalaya",
        "text": "SHILA PAR KATHA",
        "visual": "Himalayan peak: Hanuman Ji carving sacred verses with his nails onto a massive rock slab",
        "vo": [
            ("tell", [("लंका विजय के बाद,", "LANKA VIJAY KE BAAD,")], 0.02),
            ("build", [("हनुमान जी ने हिमालय की शिलाओं पर,", "HIMALAYA KI SHILAON PAR,")], 0.02),
            ("awe", [("अपने नाखूनों से", "APNE NAKHON SE"), ("प्रभु राम की कथा उकेरी।", "PRABHU RAM KI KATHA UKERI.")], 0.04),
        ],
    },
    {
        "key": "valmiki",
        "text": "VALMIKI KA AAGAMAN",
        "visual": "Maharshi Valmiki holding palm leaves, reading the glowing verses in complete awe",
        "vo": [
            ("tell", [("महर्षि वाल्मीकि ने जब", "MAHARSHI VALMIKI NE JAB")], 0.02),
            ("awe", [("वो दिव्य श्लोक पढ़े,", "WO DIVYA SHLOK PADHE,")], 0.02),
            ("punch", [("तो वे दंग रह गए!", "TO WE DANG RAH GAYE!")], 0.04),
        ],
    },
    {
        "key": "tears",
        "text": "VALMIKI KE AANSU",
        "visual": "Valmiki weeping in despair; Hanuman looking at him with deep compassion",
        "vo": [
            ("low", [("पर फिर वे रोने लगे—", "PAR PHIR WE RONE LAGE—")], 0.02),
            ("whisper", [("इतनी अलौकिक रामायण के आगे,", "ITNI ALOUKIK RAMAYANA KE AAGE,")], 0.02),
            ("ask", [("मेरी रचना कौन पढ़ेगा?", "MERI RACHNA KAUN PADHEGA?")], 0.04),
        ],
    },
    {
        "key": "sacrifice",
        "text": "SAMUDRA VISARJAN",
        "visual": "Hanuman Ji lifts the heavy rock monolith and casts it into the roaring cosmic ocean",
        "vo": [
            ("tell", [("भक्त का दुख देखकर,", "BHAKT KA DUKH DEKHKAR,")], 0.02),
            ("fast", [("हनुमान जी ने उस भारी शिला को उठाया...", "HANUMAN JI NE US BHAARI SHILA KO UTHAYA...")], 0.02),
            ("punch", [("और समुद्र में विसर्जित कर दिया!", "AUR SAMUDRA MEIN VISARJIT KAR DIYA!")], 0.04),
        ],
    },
    {
        "key": "moral",
        "text": "NISWARTH PREM",
        "visual": "Lord Rama blessing Hanuman with divine embrace and golden celestial flower shower",
        "vo": [
            ("awe", [("सच्चा भक्त प्रसिद्धि नहीं,", "SACHCHA BHAKT PRASIDDHI NAHI,")], 0.02),
            ("warm", [("केवल प्रभु का प्रेम चाहता है।", "KEWAL PRABHU KA PREM CHAHTA HAI.")], 0.04),
        ],
    },
    {
        "key": "cta",
        "text": "JAI BAJRANGBALI",
        "visual": "Hanuman Ji in radiant Abhaya mudra blessing posture",
        "vo": [
            ("cta", [("कमेंट में लिखिए—", "COMMENT MEIN LIKHIYE—")], 0.02),
            ("punch", [("जय बजरंगबली!", "JAI BAJRANGBALI!")], 0.04),
        ],
    },
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "VALMIKI": GOLD_HI,
    "RAMAYANA": GOLD_HI,
    "HANUMAD": hexc("#FFAA48"),
    "HANUMAN": hexc("#FFAA48"),
    "SAMUDRA": hexc("#6BA4FF"),
    "HIMALAYA": hexc("#90CAF9"),
    "NAKHON": GOLD_HI,
    "RAM": GOLD_HI,
    "SHLOK": GOLD_HI,
    "AANSU": hexc("#80D0FF"),
    "SHILA": hexc("#D4B07B"),
    "VISARJIT": hexc("#6BA4FF"),
    "BHAKT": GOLD_HI,
    "PREM": hexc("#FF80AB"),
    "JAI": GOLD_HI,
    "BAJRANGBALI": hexc("#FFAA48"),
    "COMMENT": GOLD_HI,
})


# -----------------------------------------------------------------------------
# Scene Visual Classes (Zero On-Screen Clutter - Only Subtitles Rule)
# -----------------------------------------------------------------------------
class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "ramayana": c("RAMAYANA", 1.0),
            "hanumad": c("HANUMAD", d * 0.40),
            "samudra": c("SAMUDRA", d * 0.70),
        }

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["hanumad"], "ghanti"), (b["samudra"], "whoosh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        himalaya_bg(ctx, t, sunset=True)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#1A0E08"))
        ctx.fill()

        # Sacred glowing rock monolith inscribed with verses in center
        rock_monolith(ctx, 540, 720, 0.75, t, glow_verses=True)

        # Left: Hanuman Ji gazing with devotion
        hanuman(ctx, 240, GROUND - 10, 0.70, t, pose="namaste", flip=True)


class Himalaya(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "vijay": c("VIJAY", 1.0),
            "shila": c("HIMALAYA", d * 0.40),
            "nakh": c("NAKHON", d * 0.70),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["shila"], "thud"), (b["nakh"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        himalaya_bg(ctx, t, sunset=False)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#101626"))
        ctx.fill()

        # Right: Rock monolith standing tall
        rock_monolith(ctx, 750, 710, 0.78, t, glow_verses=True)

        # Left: Hanuman Ji actively carving verses with glowing nails
        hanuman(ctx, 300, GROUND - 10, 0.72, t, pose="carve", flip=True)

        # Divine sparks floating between nail and rock
        spark_x = 450 + 20 * math.sin(t * 8)
        spark_y = 660 + 15 * math.cos(t * 6)
        glow(ctx, spark_x, spark_y, 60, GOLD_HI, 0.6)
        for i in range(8):
            ang = t * 10 + i * (math.pi / 4)
            dist = 25 + 10 * math.sin(t * 12 + i)
            circle(ctx, spark_x + dist * math.cos(ang), spark_y + dist * math.sin(ang), 3.5, GOLD_TEXT, 0.85)


class Valmiki(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "valmiki": c("VALMIKI", 1.0),
            "shlok": c("SHLOK", d * 0.45),
            "dang": c("DANG", d * 0.75),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["valmiki"], "ghanti"), (b["dang"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        himalaya_bg(ctx, t, sunset=True)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#161022"))
        ctx.fill()

        # Center-right: Glowing rock slab
        rock_monolith(ctx, 620, 720, 0.70, t, glow_verses=True)

        # Left: Maharshi Valmiki reading palm leaves in awe
        maharshi_valmiki(ctx, 240, GROUND - 10, 0.68, t, pose="read", flip=True)

        # Right: Hanuman Ji with folded hands in humility
        hanuman(ctx, 840, GROUND - 10, 0.68, t, pose="namaste", flip=False)


class Tears(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "rone": c("RONE", 1.0),
            "aloukik": c("ALOUKIK", d * 0.45),
            "kaun": c("KAUN", d * 0.75),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["rone"], "thud"), (b["aloukik"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        himalaya_bg(ctx, t, sunset=False)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#121424"))
        ctx.fill()

        # Left: Maharshi Valmiki weeping with tears running down face
        maharshi_valmiki(ctx, 250, GROUND - 10, 0.68, t, pose="tears", flip=True)

        # Center: Inscribed rock monolith
        rock_monolith(ctx, 540, 720, 0.65, t, glow_verses=True)

        # Right: Hanuman Ji turning to Valmiki with deep sorrow and love
        hanuman(ctx, 830, GROUND - 10, 0.68, t, pose="namaste", flip=False)


class Sacrifice(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "dukh": c("DUKH", 1.0),
            "uthaya": c("BHAARI", d * 0.40),
            "visarjit": c("VISARJIT", d * 0.70),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["uthaya"], "whoosh"), (b["visarjit"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        ocean_bg(ctx, t)

        # Roaring waves foreground
        ctx.rectangle(0, GROUND - 20, W, H)
        rgba(ctx, hexc("#0A1C38"))
        ctx.fill()

        # Hanuman Ji lifting the rock high and casting into ocean
        if t < b["visarjit"]:
            # Hanuman carrying rock overhead
            hanuman(ctx, 450, GROUND - 10, 0.72, t, pose="lift_rock", flip=True)
            rock_monolith(ctx, 450, 480, 0.68, t, glow_verses=True)
        else:
            # Rock submerging into waves with giant splash
            hanuman(ctx, 320, GROUND - 10, 0.72, t, pose="namaste", flip=True)
            splash_prog = (t - b["visarjit"]) / max(0.01, (d - b["visarjit"]))
            rock_y = 650 + splash_prog * 250
            rock_monolith(ctx, 680, rock_y, 0.60, t, glow_verses=True)
            # Water splash rings & celestial mist
            glow(ctx, 680, 850, 220, OCEAN_FOAM, 0.6)
            for i in range(12):
                sx = 680 + (i - 6) * 35 + 10 * math.sin(t * 10 + i)
                sy = 820 - 40 * math.sin(i * 0.5) - 20 * math.cos(t * 15)
                circle(ctx, sx, sy, 8, OCEAN_FOAM, 0.8)


class Moral(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "bhakt": c("BHAKT", 1.0),
            "prem": c("PREM", d * 0.50),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["bhakt"], "shimmer"), (b["prem"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        himalaya_bg(ctx, t, sunset=True)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#1C1024"))
        ctx.fill()

        # Divine shower of celestial flowers
        dv.petals(ctx, t, n=45, seed=7, a=0.90)

        # Left: Prabhu Shri Ram with abhaya hand blessing Hanuman
        shri_ram(ctx, 360, GROUND - 10, 0.70, t, pose="bless", flip=True)

        # Right: Hanuman Ji with folded hands in pure divine ecstasy
        hanuman(ctx, 720, GROUND - 10, 0.70, t, pose="namaste", flip=False)


class Cta(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "comment": c("COMMENT", 1.0),
            "jai": c("JAI", d * 0.45),
            "bajrangbali": c("BAJRANGBALI", d * 0.75),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["comment"], "ghanti"), (b["jai"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        himalaya_bg(ctx, t, sunset=True)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#180C1E"))
        ctx.fill()

        # Celestial shower of petals
        dv.petals(ctx, t, n=55, seed=15, a=0.95)

        # Centered magnificent Hanuman Ji in full Abhaya Blessing Mudra
        hanuman(ctx, 540, GROUND - 10, 0.74, t, pose="abhaya", flip=False)


# -----------------------------------------------------------------------------
# Module Exports
# -----------------------------------------------------------------------------
SCENE_CLASSES = {
    "hook": Hook,
    "himalaya": Himalaya,
    "valmiki": Valmiki,
    "tears": Tears,
    "sacrifice": Sacrifice,
    "moral": Moral,
    "cta": Cta,
}

UPLOAD = {
    "titles": [
        "Hanuman Ji Ne Apni Ramayana Samudra Mein Kyun Baha Di? 😱 #shorts",
        "Valmiki Se Pehle Hanuman Ne Likhi Thi Ramayana! Divya Rahasya #shorts",
        "Hanumad Ramayana: Hanuman Ji Ka Sabse Bada Balidan 🚩 #shorts",
        "Kyun Samudra Mein Phek Di Hanuman Ji Ne Apni Ramayana? #shorts",
        "Jab Maharshi Valmiki Dekhkar Rone Lage Hanumad Ramayana! #shorts",
        "Hanuman Ji Ki Wo Ramayana Jo Samudra Mein Doob Gayi #shorts",
        "Valmiki Ramayana vs Hanumad Ramayana: Asli Rahasya #shorts",
        "Kyun Mita Diya Hanuman Ji Ne Apna Hi Naam? #shorts",
        "Hanuman Ka Wo Balidan Jise Dekh Prabhu Ram Bhi Rone Lage #shorts",
        "Mangalwar Special: Hanumad Ramayana Ka Chhupa Rahasya #shorts",
    ],
    "thumb_text": "HANUMAD RAMAYANA?",
    "queries": [
        "hanuman ji ne apni ramayana samudra mein kyun baha di",
        "hanumad ramayana katha",
        "hanuman ramayana valmiki kahani",
    ],
    "description": """
Valmiki Ramayana se pehle ek aur Ramayana likhi gayi thi—Hanumad Ramayana! 
Jise khud Pawanputra Hanuman Ji ne Himalaya ki shilaon par apne nakhon se ukeera tha.
Lekin jab Maharshi Valmiki ne use dekha, toh Hanuman Ji ne use samudra mein visarjit kyun kar diya?

Mangalwar ke is pawan din par dekhiye Hanuman Ramayana Valmiki kahani aur nishkam prem ki yeh adbhut Hanumad Ramayana katha. 
Comment mein prem se likhein—JAI BAJRANGBALI! 🚩
""",
    "tags": [
        "hanumad ramayana",
        "hanuman ji",
        "valmiki ramayana",
        "hanuman ramayana katha",
        "mangalwar special",
        "sanatan katha",
        "divya rahasya",
        "shri ram",
        "bajrangbali",
        "shorts",
    ],
    "hashtags": [
        "#Shorts",
        "#Hanuman",
        "#JaiShriRam",
    ],
}


def thumbnail(ctx):
    himalaya_bg(ctx, 0.4, sunset=True)
    ctx.rectangle(0, GROUND - 25, W, H)
    rgba(ctx, hexc("#1A0E08"))
    ctx.fill()

    # Left: Hanuman Ji lifting the rock monolith
    hanuman(ctx, 300, GROUND - 10, 0.72, 0.5, pose="lift_rock", flip=True)
    rock_monolith(ctx, 300, 480, 0.65, 0.5, glow_verses=True)

    # Right: Maharshi Valmiki looking in shock / weeping
    maharshi_valmiki(ctx, 810, GROUND - 10, 0.70, 0.5, pose="tears", flip=False)

    # Impactful thumbnail text
    text(ctx, "HANUMAD", 540, 210, 115, GOLD_HI, font=CAPTION_FONT, bold=True, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "RAMAYANA?", 540, 320, 105, hexc("#FF4444"), font=CAPTION_FONT, bold=True, stroke=(0, 0, 0), stroke_w=20)
