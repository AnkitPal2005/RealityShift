"""Reality Shift Short - "Pinaka: 44 Second Mein 12 Rocket Ka Danka" (~45-50s).

Usage:
  python make.py pinaka --kiki-export     # exports text for KikiVoice
  python make.py pinaka --check           # policy check
  python make.py pinaka --engine edge     # preview render with edge-tts
  python make.py pinaka                   # final render from KikiVoice files

Strategic overview:
India's indigenous Pinaka Multi-Barrel Rocket Launcher (MBRL) developed by DRDO.
Fires a devastating salvo of 12 rockets in just 44 seconds, neutralizing 4 sq km.
Battle-proven in the 1999 Kargil War, upgraded with NavIC-guided 90 km precision strike,
and now exported to Armenia with strong evaluation by the French Army.
"""

import math
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cairo
import numpy as np

from core import delivery, engine, lego
from core.engine import *  # noqa: F401,F403
from shorts.brahmos_lego import tag
from shorts.chabahar import Cued
from shorts.reality_shift import flag, stamp

TOPIC = "PINAKA ROCKET SYSTEM"
OUTPUTS = {"edge": "pinaka_short.mp4"}
LEGO = {"header": "intel", "caption": "typewriter", "transition": "shutter", "palette": "glacier", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.55
TAIL_PAD = 0.20
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 126
MUSIC_STYLE = "tension"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 500

PAL = lego.PALETTES["glacier"]
UI = PAL["ui"]
HI = PAL["hi"]
RED = PAL["alert"]
INK = PAL["ink"]
SAFFRON = hexc("#FF9933")
GREEN = hexc("#3DDC84")
STEEL = hexc("#90A4AE")
DARK_STEEL = hexc("#263238")
FIRE = hexc("#FF5722")
FIRE_HI = hexc("#FFD54F")
GOLD_HI = hexc("#FFD54F")
CAMO_GREEN = hexc("#384838")
SKIN = hexc("#D49B72")
DARK_SKIN = hexc("#A86E4A")
MAROON_BERET = hexc("#80152B")
UNIFORM_BLUE = hexc("#1A2D4A")

SOURCES = [
    "Defence Research and Development Organisation (DRDO): Pinaka Multi-Barrel Rocket Launcher (MBRL) specifications, "
    "12 rockets salvo in 44 seconds, area coverage of 1000m x 800m (PIB, Ministry of Defence).",
    "Kargil War 1999 deployment: Pinaka Mk-I weapon system inducted for high-altitude artillery saturation bombardment "
    "against entrenched mountain bunker positions (Indian Army Historical Division).",
    "International Defence Exports: ₹2,000+ crore export contract signed with Armenia for Pinaka batteries and guided rockets, "
    "and French Army technical evaluation of Pinaka to replace Unitary MLRS systems (The Hindu, Janes, Economic Times).",
]

SPEC = [
    {"key": "hook", "accent": RED, "text": "44 SECONDS // 12 ROCKETS",
     "visual": "Indian Army artillery commander shouting 'FIRE!' with raised arm; Pinaka 8x8 launcher firing a 12-rocket salvo into dark sky",
     "vo": [("hook", [("सिर्फ चवालीस सेकंड में", "SIRF 44 SECOND MEIN"),
                      ("बारह घातक रॉकेट और", "12 GHATAK ROCKET AUR"),
                      ("चार वर्ग किलोमीटर का इलाका पूरी तरह राख!", "4 SQ KM ILAKA PURI TARAH RAAKH!"),
                      ("ये है भारत का स्वदेशी पिनाका सिस्टम,", "YE HAI BHARAT KA PINAKA SYSTEM,"),
                      ("जिससे दुश्मन कांपते हैं।", "JISSE DUSHMAN KAAMPTE HAIN.")])]},

    {"key": "kargil", "accent": HI, "text": "KARGIL 1999: FIRST STRIKE",
     "visual": "Kargil jawan in snow parka observing peak with binoculars; high mountain Pakistani bunker pounded to rubble by Pinaka rockets",
     "vo": [("tell", [("भगवान शिव के धनुष पिनाका पर बना", "BHAGAWAN SHIV KE DHANUSH PAR BANA"),
                      ("ये हथियार 1999 के", "YE HATHIYAR 1999 KE"),
                      ("करगिल युद्ध में गरजा था।", "KARGIL YUDH MEIN GARJA THA."),
                      ("ऊंची चोटियों पर बने पाकिस्तानी बंकरों को", "OONCHI CHOTIYON PAR BANE BUNKERS KO"),
                      ("इसने सेकंडों में तबाह कर दिया था।", "ISNE SECOND-ON MEIN TABAAH KAR DIYA THA.")])]},

    {"key": "tech", "accent": GREEN, "text": "NAVIC GUIDED // 90 KM RANGE",
     "visual": "DRDO tech controller with radar console; NavIC satellite beaming telemetry; guided rocket hitting 90 KM crosshair target",
     "vo": [("tell", [("पुराने रॉकेट्स सिर्फ अंधाधुंध फायर करते थे,", "PURANE ROCKETS ANDHADHU DH FIRE KARTE THE,"),
                      ("लेकिन नया 'गाइडेड पिनाका'", "LEKIN NAYA GUIDED PINAKA"),
                      ("नाविक सैटेलाइट से लैस है।", "NAVIC SATELLITE SE LAIS HAI."),
                      ("ये नब्बे किलोमीटर दूर दुश्मन के बंकर पर", "YE 90 KM DOOR DUSHMAN KE BANKER PAR"),
                      ("सटीक वार करता है।", "SATEEK VAAR KARTA HAI.")])]},

    {"key": "vs_himars", "accent": UI, "text": "PINAKA VS US HIMARS",
     "visual": "US HIMARS operator with empty 6-tube pod looking stunned vs Indian Army commander proudly pointing at roaring 12-salvo Pinaka",
     "vo": [("tell", [("अमेरिका का हिमार्क सिस्टम दुनिया में मशहूर है,", "AMERICA KA HIMARS MASHHOOR HAI,"),
                      ("लेकिन भारत का पिनाका उससे पांच गुना सस्ता है!", "LEKIN BHARAT KA PINAKA 5 GUNA SASTA HAI!"),
                      ("हिमार्क जहां सिर्फ छह रॉकेट दागता है,", "HIMARS JAHAN SIRF 6 ROCKET DAAGTA HAI,"),
                      ("वहीं पिनाका पूरे बारह रॉकेट दागकर", "WAHEEN PINAKA PURE 12 ROCKET DAAGKAR"),
                      ("तबाही मचाता है।", "TABAHI MACHAATA HAI.")])]},

    {"key": "export", "accent": SAFFRON, "text": "ARMENIA & FRANCE INTEREST",
     "visual": "Armenian commander in uniform shaking hands with Indian officer; French general in Kepi cap inspecting Pinaka with binoculars in awe",
     "vo": [("tell", [("इसी ताकत के दम पर", "ISI TAAKAT KE DAM PAR"),
                      ("आर्मेनिया ने भारत से", "ARMENIA NE BHARAT SE"),
                      ("ढाई हज़ार करोड़ का पिनाका खरीदा।", "2500 CRORE KA PINAKA KHAREEDA."),
                      ("और अब खुद फ्रांस की सेना भी अपने पुराने सिस्टम हटाकर", "AUR AB FRANCE KI SENA BHI APNE SYSTEM HATAKAR"),
                      ("भारत के पिनाका का टेस्ट कर रही है!", "BHARAT KE PINAKA KA TEST KAR RAHI HAI!")])]},

    {"key": "ask", "accent": HI, "text": "SABSE GHATAK HATHIYAR?",
     "visual": "Indian Army Commander in crisp military salute; tricolor fluttering behind; interactive Poll card: 'PINAKA SABSE GHATAK?'",
     "vo": [("ask", [("भारत का ये पराक्रम", "BHARAT KA YE PARAKRAM"),
                     ("पूरी दुनिया में धाक जमा रहा है।", "PURI DUNIYA MEIN DHAAK JAMA RAHA HAI."),
                     ("क्या पिनाका सेना का सबसे घातक हथियार है?", "KYA PINAKA SENA KA SABSE GHATAK HATHIYAR HAI?"),
                     ("कमेंट में बताइए", "COMMENT MEIN BATAIYE"),
                     ("और सब्सक्राइब कीजिए रियलिटी शिफ्ट!", "AUR SUBSCRIBE KIJIYE REALITY SHIFT!")])]},
]

DELIVERY = delivery.build(SPEC)
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "44": RED, "SECOND": RED, "12": RED, "GHATAK": RED, "ROCKET": RED, "4": RED, "SQ": RED, "KM": RED,
    "RAAKH!": RED, "PINAKA": HI, "SWADESHI": SAFFRON, "SYSTEM,": HI, "DUSHMAN": RED, "KAAMPTE": RED,
    "SHIV": HI, "DHANUSH": HI, "1999": HI, "KARGIL": HI, "YUDH": RED, "OONCHI": STEEL, "CHOTIYON": STEEL,
    "BUNKERS": RED, "TABAAH": RED, "GUIDED": GREEN, "NAVIC": GREEN, "SATELLITE": GREEN, "90": GREEN,
    "SATEEK": GREEN, "VAAR": GREEN, "HIMARS": UI, "5": GREEN, "SASTA": GREEN, "6": UI, "ARMENIA": SAFFRON,
    "2500": SAFFRON, "CRORE": SAFFRON, "FRANCE": UI, "SENA": SAFFRON, "TEST": HI, "PARAKRAM": SAFFRON,
    "DHAAK": SAFFRON, "GHATAK?": RED, "COMMENT": HI, "REALITY": UI, "SHIFT!": UI
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".—")] = HOT[_k]


# ============================================================ DRAWING HELPERS

def ell(ctx, x, y, rx, ry):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, math.tau)
    ctx.restore()


def smooth(ctx, pts, closed=True, k=1 / 6):
    if len(pts) < 3:
        for p in pts:
            ctx.line_to(*p)
        return
    n = len(pts)
    ctx.move_to(*pts[0])
    for i in range(n if closed else n - 1):
        p0 = pts[(i - 1) % n]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n]
        c1x = p1[0] + (p2[0] - p0[0]) * k
        c1y = p1[1] + (p2[1] - p0[1]) * k
        c2x = p2[0] - (p3[0] - p1[0]) * k
        c2y = p2[1] - (p3[1] - p1[1]) * k
        ctx.curve_to(c1x, c1y, c2x, c2y, p2[0], p2[1])
    if closed:
        ctx.close_path()


def grid_bg(ctx, t, alert=False):
    """Military tactical radar grid background."""
    ctx.rectangle(0, 0, W, H)
    rgba(ctx, (0.01, 0.02, 0.04) if not alert else (0.03, 0.015, 0.015))
    ctx.fill()

    for x in range(0, W + 1, 90):
        line(ctx, [(x, 0), (x, H)], UI if not alert else RED, 1, 0.08)
    for y in range(0, H + 1, 90):
        line(ctx, [(0, y), (W, y)], UI if not alert else RED, 1, 0.08)


# ============================================================ CHARACTER RIGS

def indian_commander(ctx, x, y, s, t, pose="command", flip=False, a=1.0):
    """Indian Army Artillery Officer in combat uniform & maroon beret."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(-s if flip else s, s)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)

    # Shadow
    ell(ctx, 0, 10, 80, 16)
    rgba(ctx, (0, 0, 0), 0.55 * a)
    ctx.fill()

    # Combat Boots
    for bx in (-35, 35):
        rrect(ctx, bx - 16, -20, 32, 24, 6)
        rgba(ctx, hexc("#1A1A1A"), a)
        ctx.fill()

    # Camo Trousers / Legs
    for side in (-1, 1):
        smooth(ctx, [(side * 42, -180), (side * 48, -70), (side * 36, -20), (side * 14, -20), (side * 20, -70), (side * 10, -180)])
        rgba(ctx, CAMO_GREEN, a)
        ctx.fill()

    # Tactical Belt
    rrect(ctx, -56, -195, 112, 18, 4)
    rgba(ctx, hexc("#212121"), a)
    ctx.fill()
    circle(ctx, 0, -186, 7, GOLD_HI)

    # Torso (Olive Camo Combat Shirt & Tactical Vest)
    torso = [(-68, -320), (68, -320), (58, -195), (-58, -195)]
    smooth(ctx, torso, k=0.05)
    rgba(ctx, CAMO_GREEN, a)
    ctx.fill()

    # Armored Tactical Plate Carrier
    rrect(ctx, -48, -310, 96, 100, 10)
    rgba(ctx, hexc("#283626"), a)
    ctx.fill()
    line(ctx, [(-30, -280), (30, -280)], hexc("#1B241A"), 5)
    line(ctx, [(-30, -250), (30, -250)], hexc("#1B241A"), 5)

    # Indian Flag Patch on shoulder
    rrect(ctx, -64, -305, 18, 12, 2)
    rgba(ctx, SAFFRON, a)
    ctx.fill()
    rrect(ctx, -64, -299, 18, 4, 1)
    rgba(ctx, (1, 1, 1), a)
    ctx.fill()
    rrect(ctx, -64, -295, 18, 4, 1)
    rgba(ctx, GREEN, a)
    ctx.fill()

    # Head & Neck
    rrect(ctx, -16, -350, 32, 34, 6)
    rgba(ctx, SKIN, a)
    ctx.fill()

    ell(ctx, 0, -385, 42, 46)
    rgba(ctx, SKIN, a)
    ctx.fill()

    # Determined Eyes & Brow
    for side in (-1, 1):
        ex = side * 18
        line(ctx, [(ex - 10, -402), (ex + 10, -396)], hexc("#1A1A1A"), 4)
        circle(ctx, ex, -388, 5, hexc("#141414"))
        circle(ctx, ex + 2, -390, 1.5, (1, 1, 1))

    # Moustache & Mouth
    smooth(ctx, [(-18, -366), (0, -372), (18, -366)], closed=False)
    rgba(ctx, hexc("#212121"), a)
    ctx.set_line_width(4)
    ctx.stroke()
    line(ctx, [(-10, -356), (10, -356)], hexc("#6A2A2A"), 3)

    # Officer Maroon Beret (Tilted to the right)
    beret_pts = [(-52, -405), (-35, -440), (20, -448), (62, -425), (55, -400), (-35, -398)]
    smooth(ctx, beret_pts, k=0.1)
    rgba(ctx, MAROON_BERET, a)
    ctx.fill()
    # Golden Army Insignia Badge
    circle(ctx, -24, -412, 7, GOLD_HI)

    # Radio Headset & Mic
    line(ctx, [(38, -385), (42, -355), (20, -350)], hexc("#141414"), 3)
    circle(ctx, 16, -350, 4, hexc("#37474F"))

    # Arms & Poses
    if pose == "command":
        # Right Arm raised up & forward shouting "FIRE!"
        sway = 6 * math.sin(t * 8)
        line(ctx, [(55, -310), (100, -360), (135 + sway, -420)], CAMO_GREEN, 24)
        # Clenched fist pointing forward
        circle(ctx, 135 + sway, -420, 14, SKIN)
        # Left Arm holding tactical binoculars at waist
        line(ctx, [(-55, -310), (-85, -260), (-45, -230)], CAMO_GREEN, 24)
        rrect(ctx, -55, -240, 24, 18, 4)
        rgba(ctx, hexc("#1A1A1A"), a)
        ctx.fill()
    elif pose == "salute":
        # Crisp Indian Military Salute: Right hand touching beret edge
        line(ctx, [(55, -310), (95, -340), (45, -410)], CAMO_GREEN, 24)
        # Hand flat at 45 deg touching beret
        rrect(ctx, 35, -420, 24, 10, 3)
        rgba(ctx, SKIN, a)
        ctx.fill()
        # Left Arm down by side at attention
        line(ctx, [(-55, -310), (-65, -230), (-62, -180)], CAMO_GREEN, 22)
    else:  # "observe"
        # Both hands holding binoculars to eyes
        line(ctx, [(-55, -310), (-65, -340), (-20, -385)], CAMO_GREEN, 22)
        line(ctx, [(55, -310), (65, -340), (20, -385)], CAMO_GREEN, 22)
        rrect(ctx, -32, -398, 64, 24, 6)
        rgba(ctx, hexc("#1A1A1A"), a)
        ctx.fill()
        circle(ctx, -16, -390, 8, hexc("#3878D8"))
        circle(ctx, 16, -390, 8, hexc("#3878D8"))

    ctx.restore()


def kargil_jawan(ctx, x, y, s, t, a=1.0):
    """Indian Army Jawan in high-altitude snow camouflage & winter goggles."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)

    # Snow boots
    for bx in (-32, 32):
        rrect(ctx, bx - 18, -22, 36, 26, 6)
        rgba(ctx, hexc("#2A2E32"), a)
        ctx.fill()

    # White Winter Trousers
    for side in (-1, 1):
        smooth(ctx, [(side * 40, -170), (side * 42, -70), (side * 32, -22), (side * 14, -22), (side * 20, -70), (side * 10, -170)])
        rgba(ctx, hexc("#DDE4EB"), a)
        ctx.fill()

    # Heavy Snow Parka (Hooded, White/Grey)
    parka = [(-72, -310), (72, -310), (62, -170), (-62, -170)]
    smooth(ctx, parka, k=0.08)
    rgba(ctx, hexc("#CFD8DC"), a)
    ctx.fill()

    # Thermal fur trim around neck
    rrect(ctx, -50, -325, 100, 25, 10)
    rgba(ctx, hexc("#ECEFF1"), a)
    ctx.fill()

    # Face & Winter balaclava
    ell(ctx, 0, -365, 38, 42)
    rgba(ctx, hexc("#37474F"), a)
    ctx.fill()

    # Combat Helmet (Olive Drab with Net)
    ell(ctx, 0, -395, 46, 32)
    rgba(ctx, hexc("#455A42"), a)
    ctx.fill()

    # High Altitude Snow Goggles (Yellow/Amber tinted)
    rrect(ctx, -34, -380, 68, 22, 8)
    rgba(ctx, hexc("#1A1A1A"), a)
    ctx.fill()
    circle(ctx, -16, -370, 9, hexc("#FFA000"), a=0.9)
    circle(ctx, 16, -370, 9, hexc("#FFA000"), a=0.9)

    # Holding heavy rangefinder binoculars looking at peaks
    line(ctx, [(-55, -290), (-55, -340), (-20, -370)], hexc("#B0BEC5"), 24)
    line(ctx, [(55, -290), (55, -340), (20, -370)], hexc("#B0BEC5"), 24)
    rrect(ctx, -30, -380, 60, 26, 6)
    rgba(ctx, hexc("#263238"), a)
    ctx.fill()

    ctx.restore()


def french_general(ctx, x, y, s, t, a=1.0):
    """French Military General in dark blue uniform with gold epaulettes and French Kepi."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)

    # Trousers
    for side in (-1, 1):
        smooth(ctx, [(side * 36, -180), (side * 38, -60), (side * 30, -15), (side * 12, -15), (side * 18, -60), (side * 8, -180)])
        rgba(ctx, hexc("#101C2B"), a)
        ctx.fill()

    # Shoes
    for bx in (-30, 30):
        rrect(ctx, bx - 14, -16, 28, 18, 4)
        rgba(ctx, hexc("#111111"), a)
        ctx.fill()

    # French Dark Blue Dress Uniform Tunic
    tunic = [(-62, -315), (62, -315), (52, -180), (-52, -180)]
    smooth(ctx, tunic, k=0.06)
    rgba(ctx, UNIFORM_BLUE, a)
    ctx.fill()

    # Gold Epaulettes on shoulders
    rrect(ctx, -70, -325, 26, 12, 3)
    rgba(ctx, GOLD_HI, a)
    ctx.fill()
    rrect(ctx, 44, -325, 26, 12, 3)
    rgba(ctx, GOLD_HI, a)
    ctx.fill()

    # Medal Ribbons on Chest
    for r in range(3):
        rrect(ctx, -35 + r * 14, -280, 11, 8, 2)
        rgba(ctx, [RED, GREEN, UI][r], a)
        ctx.fill()

    # Face & Neck
    rrect(ctx, -15, -345, 30, 32, 6)
    rgba(ctx, hexc("#F3C6A2"), a)
    ctx.fill()

    ell(ctx, 0, -380, 38, 42)
    rgba(ctx, hexc("#F3C6A2"), a)
    ctx.fill()

    # Amazed Expression (Wide eyes & raised eyebrows)
    for side in (-1, 1):
        ex = side * 16
        line(ctx, [(ex - 8, -398), (ex + 8, -402)], hexc("#333333"), 3)
        circle(ctx, ex, -384, 6, (1, 1, 1))
        circle(ctx, ex, -384, 3.5, hexc("#285082"))
    # Open O-shaped mouth in awe
    ell(ctx, 0, -355, 6, 8)
    rgba(ctx, hexc("#4A1A1A"), a)
    ctx.fill()

    # French Military Kepi Cap (Cylindrical flat-topped with visor)
    rrect(ctx, -40, -430, 80, 34, 4)
    rgba(ctx, UNIFORM_BLUE, a)
    ctx.fill()
    # Gold braid band
    line(ctx, [(-38, -402), (38, -402)], GOLD_HI, 5)
    # Black leather visor
    rrect(ctx, -42, -400, 84, 8, 3)
    rgba(ctx, hexc("#1A1A1A"), a)
    ctx.fill()

    # Holding Binoculars looking up in amazement
    line(ctx, [(-55, -305), (-50, -350), (-16, -380)], UNIFORM_BLUE, 20)
    line(ctx, [(55, -305), (50, -350), (16, -380)], UNIFORM_BLUE, 20)
    rrect(ctx, -26, -390, 52, 20, 5)
    rgba(ctx, hexc("#1C1C1C"), a)
    ctx.fill()

    ctx.restore()


def armenian_officer(ctx, x, y, s, t, a=1.0):
    """Armenian Military Commander in olive-desert uniform with Armenian flag patch."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)

    # Trousers
    for side in (-1, 1):
        smooth(ctx, [(side * 36, -180), (side * 38, -60), (side * 28, -15), (side * 12, -15), (side * 18, -60), (side * 8, -180)])
        rgba(ctx, hexc("#5A4A36"), a)
        ctx.fill()

    # Boots
    for bx in (-28, 28):
        rrect(ctx, bx - 14, -16, 28, 18, 4)
        rgba(ctx, hexc("#221A14"), a)
        ctx.fill()

    # Olive-Khaki Uniform Jacket
    jacket = [(-60, -315), (60, -315), (50, -180), (-50, -180)]
    smooth(ctx, jacket, k=0.06)
    rgba(ctx, hexc("#6D5E48"), a)
    ctx.fill()

    # Armenian Tricolor Patch on shoulder (Red, Blue, Orange)
    rrect(ctx, 48, -295, 14, 12, 2)
    rgba(ctx, hexc("#D90012"), a)
    ctx.fill()
    rrect(ctx, 48, -291, 14, 4, 1)
    rgba(ctx, hexc("#0033A0"), a)
    ctx.fill()
    rrect(ctx, 48, -287, 14, 4, 1)
    rgba(ctx, hexc("#F2A800"), a)
    ctx.fill()

    # Head & Peaked Military Cap
    rrect(ctx, -14, -345, 28, 32, 6)
    rgba(ctx, SKIN, a)
    ctx.fill()

    ell(ctx, 0, -380, 36, 40)
    rgba(ctx, SKIN, a)
    ctx.fill()

    # Friendly, satisfied smiling face
    for side in (-1, 1):
        ex = side * 15
        circle(ctx, ex, -384, 4, hexc("#212121"))
    smooth(ctx, [(-12, -358), (0, -352), (12, -358)], closed=False)
    rgba(ctx, hexc("#5A1E1E"), a)
    ctx.set_line_width(3)
    ctx.stroke()

    # Armenian Officer Cap
    rrect(ctx, -38, -425, 76, 28, 6)
    rgba(ctx, hexc("#5A4A36"), a)
    ctx.fill()
    circle(ctx, 0, -412, 6, GOLD_HI)

    # Right Hand extended forward for Handshake
    line(ctx, [(-50, -305), (-75, -260), (-110, -250)], hexc("#6D5E48"), 20)
    # Hand open for handshake
    circle(ctx, -115, -250, 12, SKIN)

    ctx.restore()


def us_himars_operator(ctx, x, y, s, t, a=1.0):
    """US Army HIMARS operator in desert camo, looking at empty launcher in disbelief."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)

    # ACU Camo Trousers
    for side in (-1, 1):
        smooth(ctx, [(side * 36, -180), (side * 38, -60), (side * 28, -15), (side * 12, -15), (side * 18, -60), (side * 8, -180)])
        rgba(ctx, hexc("#8C7E6A"), a)
        ctx.fill()

    # Desert boots
    for bx in (-28, 28):
        rrect(ctx, bx - 14, -16, 28, 18, 4)
        rgba(ctx, hexc("#B89E78"), a)
        ctx.fill()

    # Combat Uniform & Tactical Vest
    tunic = [(-58, -315), (58, -315), (48, -180), (-48, -180)]
    smooth(ctx, tunic, k=0.06)
    rgba(ctx, hexc("#A89880"), a)
    ctx.fill()

    # Combat Helmet with NVG Mount
    ell(ctx, 0, -395, 42, 30)
    rgba(ctx, hexc("#7C6E5A"), a)
    ctx.fill()
    rrect(ctx, -10, -408, 20, 14, 3)
    rgba(ctx, hexc("#263238"), a)
    ctx.fill()

    # Face & Stressed expression
    ell(ctx, 0, -370, 34, 38)
    rgba(ctx, hexc("#F0C29E"), a)
    ctx.fill()
    for side in (-1, 1):
        ex = side * 14
        circle(ctx, ex, -375, 4.5, hexc("#1A2D4A"))
    # Frowning mouth
    smooth(ctx, [(-12, -350), (0, -356), (12, -350)], closed=False)
    rgba(ctx, hexc("#5A2222"), a)
    ctx.set_line_width(3)
    ctx.stroke()

    # Arms raised with open palms in exasperation ("OUT OF ROCKETS!")
    line(ctx, [(-50, -300), (-80, -320), (-95, -350)], hexc("#A89880"), 20)
    circle(ctx, -98, -355, 12, hexc("#F0C29E"))
    line(ctx, [(50, -300), (80, -320), (95, -350)], hexc("#A89880"), 20)
    circle(ctx, 98, -355, 12, hexc("#F0C29E"))

    ctx.restore()


# ============================================================ VEHICLES & WEAPONS

def pinaka_truck(ctx, x, y, s, t, firing=False):
    """Detailed 8x8 heavy BEML-Tatra launcher truck with dual 6-tube rocket pods."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # Shadow
    ell(ctx, 0, 15, 340, 22)
    rgba(ctx, (0, 0, 0), 0.6)
    ctx.fill()

    # 8 Heavy Wheels
    wheel_xs = [-240, -160, 130, 210]
    for wx in wheel_xs:
        circle(ctx, wx, 0, 32, DARK_STEEL)
        circle(ctx, wx, 0, 24, hexc("#101416"))
        circle(ctx, wx, 0, 10, STEEL)
        for i in range(6):
            ang = i * math.tau / 6
            line(ctx, [(wx, 0), (wx + 20 * math.cos(ang), 20 * math.sin(ang))], hexc("#455A64"), 2)

    # Heavy Armored Chassis
    rrect(ctx, -270, -45, 520, 35, 6)
    rgba(ctx, hexc("#2E3B32"))
    ctx.fill()

    # Armored Cab
    cab = [(-270, -45), (-270, -110), (-240, -145), (-140, -145), (-140, -45)]
    smooth(ctx, cab, closed=True, k=0.05)
    rgba(ctx, hexc("#3B4A3E"))
    ctx.fill()

    # Windshield
    windshield = [(-262, -105), (-238, -137), (-185, -137), (-185, -105)]
    smooth(ctx, windshield, closed=True, k=0.05)
    rgba(ctx, hexc("#1C2C32"), 0.95)
    ctx.fill()

    # Stabilizer Jacks
    for jx in (-210, 170):
        rrect(ctx, jx - 6, -15, 12, 30, 2)
        rgba(ctx, STEEL)
        ctx.fill()
        rrect(ctx, jx - 18, 12, 36, 8, 2)
        rgba(ctx, DARK_STEEL)
        ctx.fill()

    # Launcher Turret Mount & Pods
    rrect(ctx, -40, -85, 120, 45, 6)
    rgba(ctx, DARK_STEEL)
    ctx.fill()

    # Elevated Dual Pods (Angled at 46 deg)
    elev_ang = -math.radians(46)
    ctx.save()
    ctx.translate(40, -75)
    ctx.rotate(elev_ang)

    line(ctx, [(-30, 15), (-10, 40)], STEEL, 8)

    # Pod body
    rrect(ctx, -20, -50, 280, 72, 8)
    rgba(ctx, hexc("#28362B"))
    ctx.fill_preserve()
    rgba(ctx, hexc("#4C6250"))
    ctx.set_line_width(3)
    ctx.stroke()

    # 12 Muzzle Openings
    for row in (-28, -2):
        for col in range(6):
            tx = 250
            ty = row + 14
            circle(ctx, tx, ty, 8, hexc("#141A16"))
            circle(ctx, tx, ty, 7, STEEL, a=0.5)

    # Rocket Launch Flames
    if firing:
        blast_w = 40 + 20 * math.sin(t * 25)
        glow(ctx, -50, -14, 110, FIRE, 0.75)
        for b in range(5):
            bx = -30 - b * 22
            by = -14 + 12 * math.sin(t * 12 + b)
            circle(ctx, bx, by, 18 + b * 6, FIRE_HI, 0.7 - b * 0.12)

        glow(ctx, 270, -14, 140, FIRE_HI, 0.9)
        ctx.move_to(260, -32)
        ctx.line_to(260 + blast_w * 2, -14)
        ctx.line_to(260, 4)
        ctx.close_path()
        rgba(ctx, FIRE_HI, 0.95)
        ctx.fill()

    ctx.restore()
    ctx.restore()


def himars_truck(ctx, x, y, s, t):
    """US HIMARS 6x6 truck with single 6-tube pod (empty / idle)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # 6 Wheels
    for wx in (-150, 60, 130):
        circle(ctx, wx, 0, 26, DARK_STEEL)
        circle(ctx, wx, 0, 10, STEEL)

    # Chassis
    rrect(ctx, -190, -35, 340, 25, 4)
    rgba(ctx, hexc("#7C6E5A"))
    ctx.fill()

    # Cab
    rrect(ctx, -190, -110, 85, 75, 4)
    rgba(ctx, hexc("#8C7E6A"))
    ctx.fill()

    # Single 6-tube pod (flat/empty)
    rrect(ctx, -80, -95, 180, 55, 6)
    rgba(ctx, hexc("#6D5E4A"))
    ctx.fill_preserve()
    rgba(ctx, hexc("#3D3222"))
    ctx.set_line_width(2)
    ctx.stroke()

    # 6 Empty Tubes
    for i in range(6):
        tx = 95
        ty = -85 + i * 8
        circle(ctx, tx, ty, 5, hexc("#1A1A1A"))

    ctx.restore()


def rocket_in_flight(ctx, x, y, ang, L, t, trail=True):
    """Sleek Pinaka rocket in flight with glowing flame trail."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)

    if trail:
        trail_len = 160 + 30 * math.sin(t * 20)
        g = cairo.LinearGradient(-trail_len, 0, 0, 0)
        g.add_color_stop_rgba(0, 1, 0.3, 0.1, 0)
        g.add_color_stop_rgba(0.7, 1, 0.5, 0.1, 0.6)
        g.add_color_stop_rgba(1, 1, 0.9, 0.5, 0.95)
        ctx.move_to(-trail_len, 0)
        ctx.line_to(0, -6)
        ctx.line_to(0, 6)
        ctx.close_path()
        ctx.set_source(g)
        ctx.fill()

    rrect(ctx, 0, -5, L, 10, 2)
    rgba(ctx, hexc("#ECEFF1"))
    ctx.fill()

    # Warhead
    ctx.move_to(L, -5)
    ctx.line_to(L + 18, 0)
    ctx.line_to(L, 5)
    ctx.close_path()
    rgba(ctx, hexc("#263238"))
    ctx.fill()

    ctx.restore()


# ============================================================ SCENES

class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"sec": c("44", 0.8), "ghatak": c("GHATAK", 2.2), "pinaka": c("PINAKA", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["sec"], "whoosh"), (b["ghatak"], "boom"), (b["pinaka"], "beep")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        grid_bg(ctx, t, alert=True)

        # Ground line
        line(ctx, [(0, 1140), (W, 1140)], hexc("#1C252B"), 3)

        # Left: Indian Army Commander giving the launch order with raised arm!
        indian_commander(ctx, 230, 1130, 0.76, t, pose="command")

        # Right: Pinaka Launcher firing rockets!
        firing = t > b["sec"]
        pinaka_truck(ctx, 720, 1120, 0.74, t, firing=firing)

        # Rocket Salvo in flight across night sky
        if t > b["sec"]:
            for r in range(6):
                rt = t - b["sec"] - r * 0.35
                if rt > 0:
                    prog = (rt * 1.8) % 3.0
                    rx = 710 + prog * 240 + r * 25
                    ry = 940 - prog * 280 - r * 20
                    ang = -math.radians(46)
                    rocket_in_flight(ctx, rx, ry, ang, 46, t)

        tag(ctx, "FIREPOWER: 12 ROCKETS // 44 SEC", 540, 290, RED, 1.0)


class Kargil(Cued):
    def beats(self, d):
        c = self.cue
        return {"shiv": c("SHIV", 1.0), "kargil": c("KARGIL", 2.4), "tabaah": c("TABAAH", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["shiv"], "whoosh"), (b["kargil"], "boom"), (b["tabaah"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        grid_bg(ctx, t)

        # Kargil Mountain Ridges
        far_mountains = [(0, 780), (180, 620), (360, 740), (540, 580), (740, 720), (920, 600), (1080, 760)]
        smooth(ctx, far_mountains + [(W, 1140), (0, 1140)], closed=True, k=0.1)
        rgba(ctx, hexc("#1A2533"))
        ctx.fill()

        near_ridge = [(0, 920), (280, 820), (520, 760), (760, 860), (1080, 820)]
        smooth(ctx, near_ridge + [(W, 1140), (0, 1140)], closed=True, k=0.1)
        rgba(ctx, hexc("#283848"))
        ctx.fill()

        # Snow top
        line(ctx, [(440, 780), (520, 760), (600, 800)], (1, 1, 1), 6, 0.8)

        # Enemy Bunker on Peak getting blasted
        rrect(ctx, 490, 735, 60, 24, 4)
        rgba(ctx, hexc("#455A64"))
        ctx.fill()

        if t > b["kargil"]:
            du = clamp((t - b["kargil"]) / 0.8)
            glow(ctx, 520, 745, 140 * du, FIRE_HI, 0.85 * (1 - du * 0.7))
            circle(ctx, 520, 745, 30 * du, FIRE, 0.9)
            for k in range(8):
                px = 520 + (k - 4) * 18 * du
                py = 745 - 35 * math.sin(k + du * 4)
                circle(ctx, px, py, 4, hexc("#90A4AE"), 1 - du)

        # Left: Kargil Jawan in snow parka observing with binoculars!
        kargil_jawan(ctx, 230, 1130, 0.76, t)

        tag(ctx, "KARGIL 1999: FIRST BATTLE STRIKE", 540, 290, HI, 1.0)


class Tech(Cued):
    def beats(self, d):
        c = self.cue
        return {"guided": c("GUIDED", 1.2), "navic": c("NAVIC", 2.2), "km": c("90", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["guided"], "beep"), (b["navic"], "whoosh"), (b["km"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        grid_bg(ctx, t)

        # Left: Artillery Commander operating console
        indian_commander(ctx, 230, 1130, 0.74, t, pose="observe")

        # NavIC Satellite in sky
        sat_x, sat_y = 680, 480
        circle(ctx, sat_x, sat_y, 22, STEEL)
        circle(ctx, sat_x, sat_y, 10, GREEN)
        rrect(ctx, sat_x - 85, sat_y - 12, 55, 24, 3)
        rgba(ctx, hexc("#1E88E5"), 0.9)
        ctx.fill()
        rrect(ctx, sat_x + 30, sat_y - 12, 55, 24, 3)
        rgba(ctx, hexc("#1E88E5"), 0.9)
        ctx.fill()

        # Telemetry beam
        scan_cone = [
            (sat_x, sat_y + 22),
            (sat_x - 160 - 30 * math.sin(t * 4), 980),
            (sat_x + 160 + 30 * math.sin(t * 4), 980)
        ]
        smooth(ctx, scan_cone, closed=True)
        rgba(ctx, GREEN, 0.12 + 0.05 * math.sin(t * 6))
        ctx.fill()

        # Target Crosshair at 90 km
        tx, ty = 850, 960
        circle(ctx, tx, ty, 38, RED, 0.8)
        circle(ctx, tx, ty, 20, RED, 0.5)
        line(ctx, [(tx - 46, ty), (tx + 46, ty)], RED, 3)
        line(ctx, [(tx, ty - 46), (tx, ty + 46)], RED, 3)

        tag(ctx, "NAVIC GUIDED // 90 KM PRECISION", 540, 290, GREEN, 1.0)


class VsHimars(Cued):
    def beats(self, d):
        c = self.cue
        return {"himars": c("HIMARS", 1.0), "sasta": c("SASTA", 2.5), "pure": c("PURE", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["himars"], "whoosh"), (b["sasta"], "beep"), (b["pure"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        grid_bg(ctx, t)

        line(ctx, [(0, 1140), (W, 1140)], hexc("#1C252B"), 3)

        # Left: US HIMARS Operator in disbelief + empty HIMARS truck
        us_himars_operator(ctx, 220, 1130, 0.72, t)
        himars_truck(ctx, 360, 1130, 0.56, t)
        tag(ctx, "USA: 6 ROCKETS // EMPTY", 260, 680, UI, 1.0, size=30)

        # Right: Indian Commander proudly pointing + Pinaka firing
        indian_commander(ctx, 880, 1130, 0.72, t, pose="command", flip=True)
        pinaka_truck(ctx, 680, 1130, 0.56, t, firing=True)
        tag(ctx, "INDIA: 12 ROCKETS // ROARING", 820, 680, GREEN, 1.0, size=30)

        tag(ctx, "PINAKA: 2X ROCKETS AT 1/5TH COST", 540, 290, HI, 1.0)


class Export(Cued):
    def beats(self, d):
        c = self.cue
        return {"armenia": c("ARMENIA", 1.2), "crore": c("CRORE", 2.2), "france": c("FRANCE", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["armenia"], "whoosh"), (b["crore"], "beep"), (b["france"], "beep")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        grid_bg(ctx, t)

        line(ctx, [(0, 1140), (W, 1140)], hexc("#1C252B"), 3)

        # Left: Armenian Commander shaking hands with Indian Officer!
        armenian_officer(ctx, 220, 1130, 0.74, t)
        indian_commander(ctx, 420, 1130, 0.74, t, pose="observe", flip=True)
        tag(ctx, "ARMENIA: ₹2,500 CR ORDER", 320, 680, SAFFRON, 1.0, size=30)

        # Right: French General inspecting Pinaka with binoculars in awe!
        french_general(ctx, 840, 1130, 0.74, t)
        tag(ctx, "FRENCH ARMY: EVALUATING", 840, 680, UI, 1.0, size=30)

        tag(ctx, "GLOBAL EXPORT SURGE: ARMENIA & FRANCE", 540, 290, HI, 1.0)


class Ask(Cued):
    def beats(self, d):
        c = self.cue
        return {"parakram": c("PARAKRAM", 1.0), "ghatak": c("GHATAK", 2.5), "cmt": c("COMMENT", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(b["parakram"], "whoosh"), (b["ghatak"], "beep"), (b["cmt"], "pop")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        grid_bg(ctx, t)

        line(ctx, [(0, 1140), (W, 1140)], hexc("#1C252B"), 3)

        # Center: Indian Commander in proud salute
        indian_commander(ctx, 540, 1130, 0.78, t, pose="salute")

        # Indian Tricolor fluttering softly on top left
        flag(ctx, 80, 420, 160, 100, "in", t)

        # Pinaka truck in background right
        pinaka_truck(ctx, 820, 1120, 0.52, t, firing=True)

        # Interactive Poll Card
        lego.ending(
            STORY, ctx, t, t - b["ghatak"], t - b["cmt"],
            question=("PINAKA: SENA KA", "SABSE GHATAK HATHIYAR?"),
            poll=("HAAN", "NAHI"),
            tag="REALITY SHIFT"
        )


SCENE_CLASSES = {
    "hook": Hook,
    "kargil": Kargil,
    "tech": Tech,
    "vs_himars": VsHimars,
    "export": Export,
    "ask": Ask,
}
STORY = sys.modules[__name__]


# ============================================================ UPLOAD KIT

UPLOAD = {
    "titles": [
        "Pinaka Rocket System: 44 Second Mein 12 Rocket Ka Danka",
        "Armenia Se France Tak: India Ke Pinaka Rocket Ka Khauf",
        "Pinaka vs HIMARS: America Ka Ghamand Todne Wala Desi Rocket",
        "Kargil Se Europe Tak: DRDO Ke Pinaka Ne Kaise Machayi Tabahi?",
        "12 Rockets in 44 Seconds: Indian Army Ka Pinaka MBRL System",
    ],
    "title": "Pinaka Rocket System: 44 Second Mein 12 Rocket Ka Danka",
    "thumb_text": "12 ROCKETS IN 44 SEC",
    "queries": ["pinaka rocket system", "pinaka vs himars", "pinaka armenia france"],
    "description": """Pinaka Rocket System: 44 Second Mein 12 Rocket Ka Danka:
Sirf 44 second me 12 rocket aur 4 square kilometer ka ilaka tabah!
DRDO dwara viksit Bharat ka swadeshi Pinaka Multi-Barrel Rocket Launcher (MBRL) aaj poori duniya me danka baja raha hai.

Is video me janiye:
• 12 rockets in 44 seconds: Pinaka ki tabahi machane wali takat
• 1999 Kargil yudh me Pakistani banyon par pehla prahar
• NavIC satellite se guided 90 kilometer tak pinpoint target lock
• American HIMARS ke mukable 1/5th cost aur 2x firepower
• Armenia ka ₹2,500 crore export order aur France ka testing interest

Bharat ke is swadeshi hathiyar par garv hai toh comment me likhiye: Jai Hind!
Subscribe kijiye Reality Shift channel ko defence aur geopolitics explainers ke liye.

#Shorts #Pinaka #IndianArmy
""",
    "tags": ["pinaka rocket system", "pinaka mbrl", "drdo pinaka", "indian army artillery", "pinaka vs himars",
             "armenia pinaka deal", "france pinaka test", "defence news india", "reality shift", "indian weapons"],
    "hashtags": ["#Shorts", "#Pinaka", "#IndianArmy"],
}


def thumbnail(ctx):
    """1080x1920 cover: Tactical night background, Indian Commander saluting + Pinaka firing 12 rockets."""
    grid_bg(ctx, 0.5, alert=True)
    indian_commander(ctx, 340, 1180, 0.88, 0.5, pose="command")
    pinaka_truck(ctx, 720, 1140, 0.68, 0.5, firing=True)

    for r in range(4):
        rocket_in_flight(ctx, 580 + r * 50, 840 - r * 60, -math.radians(46), 48, 0.5)

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
    text(ctx, "44 SECONDS", 540, 280, 145, RED, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "12 ROCKETS!", 540, 440, 125, HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    tag(ctx, "PINAKA MBRL // ARMENIA & FRANCE", 540, 600, SAFFRON, 1.0)
    text(ctx, "REALITY SHIFT", 540, 1800, 36, UI, font=lego.MONO, a=0.7)


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


def main() -> None:
    import importlib
    from core import upload_kit
    story = importlib.import_module("shorts.pinaka")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
