"""Reality Shift Short — "Ghatak UCAV: DRDO Ka Adrishya Shikari" (~50-55s).

Usage:
  python make.py ghatak --kiki-export
  python make.py ghatak --kiki-split
  python make.py ghatak --engine files
  python make.py ghatak --preview

Technical Overview:
DRDO Ghatak (Swift / Autonomous Flying Wing Technology Demonstrator):
India's stealth unmanned combat aerial vehicle (UCAV) developed by Aeronautical Development Establishment (ADE).
Flying-wing design with internal weapons bay, dry Kaveri engine, radar-absorbent materials (RAM),
and deep penetration surgical strike capabilities.
"""

import importlib
import json
import math
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cairo
import numpy as np

from core import delivery, engine, lego
from core.engine import *  # noqa: F401,F403
from shorts.chabahar import Cued
from shorts.reality_shift import flag

TOPIC = "DRDO GHATAK STEALTH UCAV"
OUTPUTS = {"edge": "ghatak_short.mp4"}
LEGO = {"header": "intel", "caption": "typewriter", "transition": "shutter", "palette": "intel", "ending": "prompt"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.55
TAIL_PAD = 0.20
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 118
MUSIC_STYLE = "tension"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 400

PAL = lego.PALETTES["intel"]
UI = PAL["ui"]
HI = PAL["hi"]
RED = PAL["alert"]
INK = PAL["ink"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
STEEL = hexc("#90A4AE")
DARK_STEEL = hexc("#151D24")
RADAR_GREEN = hexc("#00FF66")
STEALTH_BLACK = hexc("#0D1117")
FIRE_ORANGE = hexc("#FF5500")
GOLD = hexc("#FFD700")
MONO = "Consolas"

SOURCES = [
    "DRDO Aeronautical Development Establishment (ADE) - Autonomous Flying Wing Technology Demonstrator (SWiFT / Ghatak UCAV)",
    "Defence Research and Development Organisation (DRDO) - Flight trials at Aeronautical Test Range (ATR), Chitradurga, Karnataka",
    "Gas Turbine Research Establishment (GTRE) - Indigenous Dry Kaveri engine integration for Ghatak UCAV",
]

SPEC = [
    {"key": "radar_bunker", "accent": RED, "text": "RADAR SCREEN EMPTY",
     "visual": "Enemy radar operator staring at circular green scope in bunker, confused, scratching head, screen is empty",
     "vo": [("tell", [("दुश्मन का पहरेदार अपने रडार को", "DUSHMAN KA PAHREDAAR RADAR KO"),
                      ("बार-बार देख रहा है,", "BAAR BAAR DEKH RAHA HAI,"),
                      ("पर उसे कुछ भी", "PAR USE KUCH BHI"),
                      ("दिखाई नहीं दे रहा!", "DIKHAYI NAHI DE RAHA!")])]},

    {"key": "ghost_shadow", "accent": STEEL, "text": "STEALTH GHOST ABOVE",
     "visual": "Ghatak stealth shadow gliding silently above cloud layer, operator below relaxed thinking sky is empty",
     "vo": [("tell", [("उसे लग रहा है कि", "USE LAG RAHA HAI KI"),
                      ("आसमान बिल्कुल खाली है,", "AASMAAN BIKUL KHAALI HAI,"),
                      ("लेकिन असल में", "LEKIN ASAL MEIN"),
                      ("उनके सिर के ठीक ऊपर", "UNKE SIR KE THEEK UPAR"),
                      ("मौत बनकर", "MAUT BANKAR"),
                      ("एक शिकारी उड़ रहा है!", "EK SHIKARI UD RAHA HAI!")])]},

    {"key": "reveal", "accent": SAFFRON, "text": "DRDO GHATAK STEALTH DRONE",
     "visual": "DRDO Ghatak Stealth Drone revealed: sleek matte black flying wing, sharp angled leading edges, IAF roundel",
     "vo": [("tell", [("ये है भारत का सबसे खुफिया हथियार—डीआरडीओ का", "YEH HAI BHARAT KA SABSE KHUFIYA HATHIYAR—DRDO KA"),
                      ("घातक लड़ाकू ड्रोन!", "GHATAK LADAAKU DRONE!")])]},

    {"key": "stealth_physics", "accent": STEEL, "text": "FLYING WING STEALTH",
     "visual": "Flying-wing aerodynamic shape; red enemy radar waves hit stealth faceted angles and scatter harmlessly into space",
     "vo": [("tell", [("बिना किसी पूंछ वाला इसका अनोखा तिरछा आकार", "BINA KISI POONCH WALA ANKHOA TIRCCHA AAKAAR"),
                      ("और खास काली परत ऐसी है,", "AUR KHAAS KAALI PARAT AISI HAI,"),
                      ("कि दुश्मन की रडार तरंगें", "KI DUSHMAN KI RADAR TARANGEIN"),
                      ("इससे टकराकर गायब हो जाती हैं।", "ISSE TAKRAAKAR GAAYAB HO JAATI HAIN."),
                      ("एक नन्हा पक्षी भी रडार पर दिख जाएगा,", "EK NANHA PAKSHI BHI RADAR PAR DIKH JAYEGA,"),
                      ("पर ये नहीं!", "PAR YEH NAHI!")])]},

    {"key": "command_center", "accent": SAFFRON, "text": "COMMANDER LAUNCH ORDER",
     "visual": "Indian Air Force Commander & DRDO Scientist at holographic console; Commander presses glowing red weapon trigger",
     "vo": [("tell", [("हज़ारों किलोमीटर दूर बैठे", "HAZARON KM DOOR BAITHE"),
                      ("भारतीय वायुसेना के अफसर", "BHARATIYA VAYUSENA KE OFFICER"),
                      ("बस एक इशारा करते हैं,", "BAS EK ISHARA KARTE HAIN,"),
                      ("और आसमान में उड़ते घातक के पेट का", "AUR AASMAAN MEIN UDTE GHATAK KE PET KA"),
                      ("गुप्त दरवाज़ा खुल जाता है!", "GUPT DARWAZA KHUL JAATA HAI!")])]},

    {"key": "strike", "accent": FIRE_ORANGE, "text": "PRECISION BOMB STRIKE",
     "visual": "Ghatak internal bomb bay opens, precision bomb drops, diving onto enemy radar base, huge fireball explosion",
     "vo": [("tell", [("पलक झपकते ही", "PALAK JHAPAKTE HI"),
                      ("अचूक बम सीधा ठिकाने पर गिरता है,", "ACHOOK BOMB SEEDHA THIKAANE PAR GIRTA HAI,"),
                      ("और दुश्मन का पूरा सैन्य अड्डा", "AUR DUSHMAN KA POORA ADDA"),
                      ("आग के शोले में तब्दील हो जाता है—वो भी", "AAG KE SHOLE MEIN TABDEEL HO JAATA HAI—WO BHI"),
                      ("बिना किसी पायलट की", "BINA KISI PILOT KI"),
                      ("जान खतरे में डाले!", "JAAN KHATRE MEIN DAALE!")])]},

    {"key": "enemy_panic", "accent": RED, "text": "ENEMY GENERAL IN PANIC",
     "visual": "Enemy General in uniform sweating heavily, wiping forehead with handkerchief, holding head in panic and disbelief",
     "vo": [("tell", [("दुश्मन के बड़े अफसर", "DUSHMAN KE BADE OFFICER"),
                      ("अब पसीना पोंछते हुए हैरान हैं", "AB PASEENA PONCHTE HUE HAIRAAN HAIN"),
                      ("कि हमला आखिर हुआ कहाँ से!", "KI HAMLA AAKHIR HUA KAHAN SE!")])]},

    {"key": "cta", "accent": HI, "text": "DRDO PRIDE & CTA",
     "visual": "Indian Commander smiling with thumbs up, Tiranga flag glowing, Ghatak climbing into the sunset",
     "vo": [("ask", [("भारत के इस अदृश्य शिकारी पर", "BHARAT KE IS ADRISHYA SHIKARI PAR"),
                     ("क्या आपको गर्व है?", "KYA AAPKO GARV HAI?"),
                     ("कमेंट में बताइए,", "COMMENT MEIN BATAIYE,"),
                     ("और सब्सक्राइब कीजिए रियलिटी शिफ्ट!", "AUR SUBSCRIBE KIJIYE REALITY SHIFT!"),
                     ("जय हिंद!", "JAI HIND!")])]},
]

DELIVERY = delivery.build(SPEC)
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "DUSHMAN": RED, "RADAR": RED, "BAAR": STEEL, "AASMAAN": STEEL, "KHAALI": STEEL, "MAUT": RED,
    "SHIKARI": SAFFRON, "BHARAT": SAFFRON, "KHUFIYA": GOLD, "HATHIYAR—": GOLD, "DRDO": SAFFRON,
    "GHATAK": SAFFRON, "DRONE!": SAFFRON, "POONCH": STEEL, "AAKAAR": STEEL, "KAALI": STEEL,
    "PARAT": STEEL, "TARANGEIN": RED, "GAAYAB": STEEL, "PAKSHI": STEEL, "NAHI!": RED,
    "HAZARON": GOLD, "KM": GOLD, "VAYUSENA": SAFFRON, "OFFICER": SAFFRON, "ISHARA": GOLD,
    "PET": STEEL, "GUPT": GOLD, "DARWAZA": GOLD, "ACHOOK": RED, "BOMB": RED, "THIKAANE": RED,
    "ADDA": RED, "AAG": FIRE_ORANGE, "SHOLE": FIRE_ORANGE, "TABDEEL": FIRE_ORANGE, "PILOT": STEEL,
    "PASEENA": HI, "PONCHTE": HI, "HAIRAAN": RED, "HAMLA": RED, "KAHAN": RED, "ADRISHYA": SAFFRON,
    "GARV": SAFFRON, "COMMENT": HI, "SUBSCRIBE": HI, "JAI": SAFFRON, "HIND!": SAFFRON
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".—")] = HOT[_k]


# ============================================================ CHARACTER DRAWING PRIMITIVES

def draw_operator_character(ctx, x, y, s, t, sweating=False, scratching=False):
    """Animated radar operator in bunker with military headset, shifting eyes, blinking."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # Torso (military uniform)
    rrect(ctx, -85, 30, 170, 200, 24)
    rgba(ctx, (0.12, 0.22, 0.16))  # Olive drab
    ctx.fill()
    # Collar / Lapel
    line(ctx, [(-30, 30), (0, 90), (30, 30)], (0.08, 0.15, 0.10), 4)

    # Neck
    rrect(ctx, -24, -15, 48, 55, 8)
    rgba(ctx, (0.86, 0.68, 0.54))
    ctx.fill()

    # Head (leaning forward slightly with t)
    tilt = 0.05 * math.sin(t * 3)
    ctx.save()
    ctx.rotate(tilt)

    # Face base
    rrect(ctx, -60, -135, 120, 130, 42)
    rgba(ctx, (0.86, 0.68, 0.54))
    ctx.fill()

    # Military Hair
    ctx.move_to(-65, -100)
    ctx.curve_to(-65, -155, 65, -155, 65, -100)
    ctx.close_path()
    rgba(ctx, (0.1, 0.08, 0.06))
    ctx.fill()

    # Headset headband
    ctx.arc(0, -90, 72, math.pi * 0.95, math.pi * 2.05)
    ctx.set_line_width(8)
    rgba(ctx, (0.2, 0.22, 0.25))
    ctx.stroke()
    # Headset earcups
    rrect(ctx, -78, -95, 20, 42, 8)
    rrect(ctx, 58, -95, 20, 42, 8)
    rgba(ctx, (0.1, 0.1, 0.12))
    ctx.fill()
    # Headset boom mic
    line(ctx, [(68, -75), (55, -45), (20, -45)], (0.2, 0.22, 0.25), 4)
    circle(ctx, 16, -45, 6, (0.05, 0.05, 0.05))

    # Eyes (shifting left/right in confusion, blinking every ~3s)
    blink = 1.0 if (t % 3.2 > 0.18) else 0.1
    eye_shift = 6 * math.sin(t * 4)

    # Left eye
    rrect(ctx, -40, -82, 28, 20 * blink, 6)
    rgba(ctx, INK)
    ctx.fill()
    circle(ctx, -26 + eye_shift, -72, 5 * blink, (0.15, 0.1, 0.05))

    # Right eye
    rrect(ctx, 12, -82, 28, 20 * blink, 6)
    rgba(ctx, INK)
    ctx.fill()
    circle(ctx, 26 + eye_shift, -72, 5 * blink, (0.15, 0.1, 0.05))

    # Eyebrows (worried / furrowed slant)
    line(ctx, [(-44, -94), (-16, -90)], (0.15, 0.1, 0.05), 3.5)
    line(ctx, [(16, -90), (44, -94)], (0.15, 0.1, 0.05), 3.5)

    # Mouth (open in confusion / gap)
    rrect(ctx, -14, -42, 28, 12, 6)
    rgba(ctx, (0.4, 0.2, 0.2))
    ctx.fill()

    # Sweat droplets if sweating
    if sweating:
        for i in range(3):
            sw_y = -90 + ((t * 80 + i * 35) % 90)
            circle(ctx, 48 + i * 4, sw_y, 4, UI, 0.8)

    ctx.restore()

    # Hand scratching head if scratching
    if scratching:
        ctx.save()
        arm_ang = -0.3 + 0.15 * math.sin(t * 7)
        ctx.translate(-70, 70)
        ctx.rotate(arm_ang)
        rrect(ctx, -20, -140, 36, 140, 16)
        rgba(ctx, (0.12, 0.22, 0.16))
        ctx.fill()
        circle(ctx, 0, -150, 18, (0.86, 0.68, 0.54))
        ctx.restore()

    ctx.restore()


def draw_commander_character(ctx, x, y, s, t, pressing_button=False):
    """Indian Air Force Commander in blue air force uniform, confident posture, wings badge."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # Torso (IAF Sky Blue Uniform)
    rrect(ctx, -90, 30, 180, 210, 24)
    rgba(ctx, (0.18, 0.28, 0.42))
    ctx.fill()

    # IAF Wings Pilot Badge on left chest
    line(ctx, [(-55, 75), (-25, 75)], GOLD, 4)
    circle(ctx, -40, 75, 6, SAFFRON)

    # Neck
    rrect(ctx, -25, -15, 50, 55, 8)
    rgba(ctx, (0.84, 0.66, 0.52))
    ctx.fill()

    # Face base
    rrect(ctx, -62, -140, 124, 135, 42)
    rgba(ctx, (0.84, 0.66, 0.52))
    ctx.fill()

    # Hair (clean side-parted military cut)
    ctx.move_to(-67, -105)
    ctx.curve_to(-67, -165, 67, -165, 67, -105)
    ctx.close_path()
    rgba(ctx, (0.08, 0.08, 0.08))
    ctx.fill()

    # Confident Eyes
    blink = 1.0 if (t % 3.8 > 0.18) else 0.1
    circle(ctx, -25, -74, 5 * blink, (0.1, 0.1, 0.1))
    circle(ctx, 25, -74, 5 * blink, (0.1, 0.1, 0.1))
    # Confident straight eyebrows
    line(ctx, [(-42, -88), (-14, -88)], (0.1, 0.1, 0.1), 3.5)
    line(ctx, [(14, -88), (42, -88)], (0.1, 0.1, 0.1), 3.5)

    # Confident slight smile
    ctx.move_to(-18, -42)
    ctx.curve_to(-8, -34, 8, -34, 18, -42)
    ctx.set_line_width(3.5)
    rgba(ctx, (0.35, 0.18, 0.15))
    ctx.stroke()

    # Arm reaching out to press button if pressing_button
    if pressing_button:
        ctx.save()
        push = clamp(math.sin(t * 5), 0.0, 1.0)
        ctx.translate(65, 85)
        rrect(ctx, 0, -20, 110 + push * 25, 40, 14)
        rgba(ctx, (0.18, 0.28, 0.42))
        ctx.fill()
        # Hand / Index finger pressing
        circle(ctx, 125 + push * 25, 0, 16, (0.84, 0.66, 0.52))
        line(ctx, [(125 + push * 25, 0), (145 + push * 25, 0)], (0.84, 0.66, 0.52), 8)
        ctx.restore()

    ctx.restore()


def draw_enemy_general(ctx, x, y, s, t):
    """Enemy Military General sweating, holding head in panic and disbelief."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # Torso (High ranking military coat with medals)
    rrect(ctx, -95, 30, 190, 210, 24)
    rgba(ctx, (0.18, 0.16, 0.14))
    ctx.fill()

    # Medals ribbon bar
    for mx in range(-60, 0, 16):
        rrect(ctx, mx, 65, 12, 10, 2)
        rgba(ctx, RED if mx % 32 == 0 else GOLD)
        ctx.fill()

    # Face base
    rrect(ctx, -65, -135, 130, 135, 42)
    rgba(ctx, (0.88, 0.68, 0.54))
    ctx.fill()

    # General Peak Cap (askew / tilted in panic)
    ctx.save()
    ctx.rotate(-0.12)
    rrect(ctx, -85, -180, 170, 65, 18)
    rgba(ctx, (0.15, 0.14, 0.12))
    ctx.fill()
    # Golden cap band & badge
    rrect(ctx, -80, -135, 160, 18, 4)
    rgba(ctx, GOLD)
    ctx.fill()
    ctx.restore()

    # Wide panicked eyes
    rrect(ctx, -42, -85, 32, 28, 8)
    rrect(ctx, 10, -85, 32, 28, 8)
    rgba(ctx, INK)
    ctx.fill()
    # Tiny pupils (shocked expression)
    circle(ctx, -26, -71, 4, (0.1, 0.1, 0.1))
    circle(ctx, 26, -71, 4, (0.1, 0.1, 0.1))

    # Sweating heavily
    for i in range(4):
        drop_y = -95 + ((t * 90 + i * 28) % 110)
        circle(ctx, -55 + i * 36, drop_y, 4.5, UI, 0.85)

    # Hands clutching head in panic
    hand_y = -100 + 8 * math.sin(t * 6)
    circle(ctx, -75, hand_y, 24, (0.88, 0.68, 0.54))
    circle(ctx, 75, hand_y, 24, (0.88, 0.68, 0.54))

    ctx.restore()


def draw_ghatak_drone(ctx, x, y, s, t, bay_open=False, bomb_dropping=False):
    """High-detail, colorful procedural DRDO Ghatak Flying-Wing Combat Drone."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # 1. Soft atmospheric drop shadow underneath
    ctx.save()
    ctx.scale(1.0, 0.28)
    circle(ctx, 0, 190, 260, (0, 0, 0), 0.45)
    ctx.restore()

    # 2. Main Flying-Wing Planform (B-2 / Swift faceted shape)
    # Nose -> Wingtip Right -> Serrated trailing edge -> Wingtip Left -> Close
    ctx.move_to(0, -105)          # Nose
    ctx.line_to(290, 65)          # Right wingtip
    ctx.line_to(230, 110)         # Outer right serration
    ctx.line_to(145, 75)          # Middle right serration
    ctx.line_to(0, 135)           # Beaver tail center
    ctx.line_to(-145, 75)         # Middle left serration
    ctx.line_to(-230, 110)        # Outer left serration
    ctx.line_to(-290, 65)         # Left wingtip
    ctx.close_path()

    # Dynamic multi-tone composite body gradient (Stealth Titanium Slate)
    g = cairo.LinearGradient(0, -105, 0, 135)
    g.add_color_stop_rgb(0, 0.16, 0.22, 0.28)    # Sleek tactical slate blue
    g.add_color_stop_rgb(0.45, 0.10, 0.14, 0.18) # Mid stealth composite
    g.add_color_stop_rgb(1.0, 0.04, 0.06, 0.09)  # Deep carbon dark
    ctx.set_source(g)
    ctx.fill_preserve()

    # Crisp metallic panel edge highlight
    ctx.set_line_width(3.0)
    rgba(ctx, (0.4, 0.55, 0.68), 0.8)
    ctx.stroke()

    # 3. High-Contrast Saffron Aerodynamic Racing Trim (Leading Edges)
    # Right leading edge stripe
    line(ctx, [(10, -95), (280, 60)], SAFFRON, 4.5, 0.9)
    # Left leading edge stripe
    line(ctx, [(-10, -95), (-280, 60)], SAFFRON, 4.5, 0.9)

    # 4. Angular Faceted Stealth Panels (Geometric sci-fi wings)
    # Right wing composite panel
    ctx.move_to(35, -30)
    ctx.line_to(200, 45)
    ctx.line_to(145, 70)
    ctx.line_to(20, 40)
    ctx.close_path()
    rgba(ctx, (0.22, 0.30, 0.38), 0.6)
    ctx.fill()
    ctx.set_line_width(1.5)
    rgba(ctx, (0.5, 0.65, 0.78), 0.5)
    ctx.stroke()

    # Left wing composite panel
    ctx.move_to(-35, -30)
    ctx.line_to(-200, 45)
    ctx.line_to(-145, 70)
    ctx.line_to(-20, 40)
    ctx.close_path()
    rgba(ctx, (0.22, 0.30, 0.38), 0.6)
    ctx.fill()
    ctx.set_line_width(1.5)
    rgba(ctx, (0.5, 0.65, 0.78), 0.5)
    ctx.stroke()

    # 5. Glowing Cyan Formation & Avionics Strips
    line(ctx, [(70, 15), (170, 50)], (0.0, 0.95, 1.0), 3.0, 0.95)
    line(ctx, [(-70, 15), (-170, 50)], (0.0, 0.95, 1.0), 3.0, 0.95)

    # Wingtip Anti-Collision Beacons (Green on Right, Red on Left)
    circle(ctx, 288, 65, 7, (0.0, 1.0, 0.4), 0.9 + 0.1 * math.sin(t * 12))  # Right Green
    circle(ctx, -288, 65, 7, (1.0, 0.15, 0.2), 0.9 + 0.1 * math.sin(t * 12)) # Left Red

    # 6. S-Duct Stealth Dorsal Engine Air Intake
    ctx.move_to(-50, -45)
    ctx.line_to(50, -45)
    ctx.line_to(36, -20)
    ctx.line_to(-36, -20)
    ctx.close_path()
    rgba(ctx, (0.02, 0.03, 0.05))
    ctx.fill()
    line(ctx, [(-50, -45), (50, -45)], GOLD, 3.0, 0.9)
    # Turbine glow deep in the duct
    circle(ctx, 0, -32, 16, FIRE_ORANGE, 0.7 + 0.3 * math.sin(t * 15))

    # 7. Rear Dry Kaveri Stealth Jet Nozzle Exhaust
    # Serrated 2D stealth nozzle
    ctx.move_to(-25, 120)
    ctx.line_to(0, 140)
    ctx.line_to(25, 120)
    ctx.close_path()
    rgba(ctx, DARK_STEEL)
    ctx.fill()
    # Glowing supersonic afterburner cone
    ex_pulse = 0.8 + 0.2 * math.sin(t * 20)
    circle(ctx, 0, 132, 16 * ex_pulse, (1.0, 0.4, 0.0), 0.9)
    circle(ctx, 0, 132, 9 * ex_pulse, (1.0, 0.9, 0.2), 1.0)
    circle(ctx, 0, 132, 4, INK, 1.0)

    # 8. Nose Electro-Optical / FLIR Targeting Sensor (Golden Crystal Glass)
    rrect(ctx, -14, -100, 28, 22, 6)
    rgba(ctx, DARK_STEEL)
    ctx.fill()
    circle(ctx, 0, -90, 8, GOLD, 0.9)
    circle(ctx, 0, -90, 4, (0.0, 0.9, 1.0), 1.0)

    # 9. Prominent Indian Air Force Roundel & Markings
    # Left Wing Roundel
    rx, ry = -115, 20
    circle(ctx, rx, ry, 22, SAFFRON)
    circle(ctx, rx, ry, 15, INK)
    circle(ctx, rx, ry, 8, INDIA_GREEN)

    # Right Wing "DRDO GHATAK" Tactical Stencil
    ctx.save()
    ctx.translate(75, 26)
    ctx.rotate(0.24)
    text(ctx, "DRDO GHATAK", 0, 0, 16, INK, font=MONO, bold=True, a=0.9)
    ctx.restore()

    # 10. Internal Weapons Bay (With Hazard Stripes & Smart Bomb)
    if bay_open:
        # Deep weapons bay cavity
        rrect(ctx, -55, -15, 110, 95, 10)
        rgba(ctx, (0.02, 0.03, 0.05))
        ctx.fill()
        
        # Yellow & Black Caution Warning Edges
        for hx in range(-50, 50, 18):
            line(ctx, [(hx, -13), (hx + 10, -13)], GOLD, 3)
            line(ctx, [(hx, 78), (hx + 10, 78)], GOLD, 3)

        # Dual Bay Doors Pushed Open Sideways
        rrect(ctx, -78, -15, 24, 95, 4)
        rrect(ctx, 54, -15, 24, 95, 4)
        rgba(ctx, (0.18, 0.24, 0.30))
        ctx.fill()
        line(ctx, [(-78, -15), (-78, 80)], SAFFRON, 2)
        line(ctx, [(78, -15), (78, 80)], SAFFRON, 2)

        # High-Tech Precision Smart Bomb Releasing
        if bomb_dropping:
            bomb_y = 25 + (t * 220) % 360
            # Bomb body in olive green with yellow hazard ring
            rrect(ctx, -18, bomb_y, 36, 85, 14)
            rgba(ctx, (0.28, 0.38, 0.24)) # Military Olive
            ctx.fill()
            # Golden laser seeker nose
            circle(ctx, 0, bomb_y + 85, 9, GOLD)
            circle(ctx, 0, bomb_y + 85, 4, RED)
            # High-viz yellow band
            rrect(ctx, -18, bomb_y + 20, 36, 12, 2)
            rgba(ctx, GOLD)
            ctx.fill()
            # Cruciform guidance fins (4 fins)
            line(ctx, [(-28, bomb_y + 5), (28, bomb_y + 5)], STEEL, 4)
            line(ctx, [(-22, bomb_y - 8), (-18, bomb_y + 15)], STEEL, 4)
            line(ctx, [(22, bomb_y - 8), (18, bomb_y + 15)], STEEL, 4)

    ctx.restore()


# ============================================================ SCENE CLASSES (ZERO TEXT CLUTTER - ONLY SUBTITLES)

class RadarBunkerScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"radar": c("RADAR", 1.2), "dikh": c("DIKHAYI", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["radar"], "pick"), (b["dikh"], "pop")]

    def draw(self, ctx, t, d):
        # Dark tactical bunker background
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, 0.02, 0.04, 0.06)
        g.add_color_stop_rgb(1, 0.01, 0.02, 0.03)
        ctx.rectangle(0, 0, W, H)
        ctx.set_source(g)
        ctx.fill()

        # Circular glowing radar console on left
        cx, cy, r = 320, 520, 180
        circle(ctx, cx, cy, r, (0.01, 0.05, 0.02), 0.9)
        # Radar range rings
        for ring in (0.33, 0.66, 1.0):
            circle(ctx, cx, cy, r * ring, RADAR_GREEN, 0.25)
            ctx.set_line_width(2)
            ctx.stroke()
        # Radar sweep beam
        ang = t * 3.5
        ctx.move_to(cx, cy)
        ctx.arc(cx, cy, r, ang - 0.2, ang)
        ctx.close_path()
        rgba(ctx, RADAR_GREEN, 0.4)
        ctx.fill()

        # Radar operator sitting at console, confused, scratching head
        draw_operator_character(ctx, 720, 580, 1.35, t, scratching=(t > 1.5))


class GhostShadowScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"khaali": c("KHAALI", 1.2), "shikari": c("SHIKARI", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["khaali"], "pick"), (b["shikari"], "thud")]

    def draw(self, ctx, t, d):
        # Night moonlit clouds sky
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, 0.01, 0.03, 0.08)
        g.add_color_stop_rgb(0.6, 0.02, 0.05, 0.12)
        g.add_color_stop_rgb(1.0, 0.01, 0.02, 0.04)
        ctx.rectangle(0, 0, W, H)
        ctx.set_source(g)
        ctx.fill()

        # Moon disc
        circle(ctx, 850, 240, 75, INK, 0.85)

        # Ghatak stealth drone gliding silently across the sky
        drone_x = 200 + ((t * 85) % 700)
        drone_y = 480 + 15 * math.sin(t * 2)
        draw_ghatak_drone(ctx, drone_x, drone_y, 1.15, t)

        # Distant radar bunker at bottom with relaxed operator silhouette
        rrect(ctx, 180, 850, 720, 260, 24)
        rgba(ctx, (0.05, 0.07, 0.10))
        ctx.fill()
        # Operator leaning back
        draw_operator_character(ctx, 540, 960, 0.85, t, scratching=False)


class RevealScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"drdo": c("DRDO", 1.2), "ghatak": c("GHATAK", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["drdo"], "pop"), (b["ghatak"], "thud")]

    def draw(self, ctx, t, d):
        # Cinematic dark studio backdrop
        g = cairo.RadialGradient(540, 560, 50, 540, 560, 600)
        g.add_color_stop_rgb(0, 0.06, 0.10, 0.15)
        g.add_color_stop_rgb(1, 0.01, 0.02, 0.03)
        ctx.rectangle(0, 0, W, H)
        ctx.set_source(g)
        ctx.fill()

        # Ghatak UCAV in full majestic view, banking smoothly
        bank = 0.06 * math.sin(t * 2.5)
        draw_ghatak_drone(ctx, 540, 560, 1.7, t)


class StealthPhysicsScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"tarang": c("TARANGEIN", 1.2), "gaayab": c("GAAYAB", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["tarang"], "pick"), (b["gaayab"], "pop")]

    def draw(self, ctx, t, d):
        # Dark physics testing environment
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, 0.01, 0.02, 0.04)
        g.add_color_stop_rgb(1, 0.02, 0.03, 0.05)
        ctx.rectangle(0, 0, W, H)
        ctx.set_source(g)
        ctx.fill()

        # Ghatak in center
        draw_ghatak_drone(ctx, 540, 520, 1.4, t)

        # Incoming red radar waves hitting the stealth wing & deflecting away
        for i in range(6):
            rx0 = 120
            ry0 = 340 + i * 65
            rx1 = 540 - 180 + i * 20
            ry1 = 520 - 40 + i * 20
            # Incoming wave line
            line(ctx, [(rx0, ry0), (rx1, ry1)], RED, 3, 0.7)
            # Deflected wave scattering away into empty space
            line(ctx, [(rx1, ry1), (rx1 + 180, ry1 - 140)], UI, 2.5, 0.5)


class CommandCenterScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"officer": c("OFFICER", 1.2), "darwaza": c("DARWAZA", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["officer"], "pick"), (b["darwaza"], "thud")]

    def draw(self, ctx, t, d):
        # Indian Command Center interior
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, 0.02, 0.04, 0.08)
        g.add_color_stop_rgb(1, 0.01, 0.02, 0.03)
        ctx.rectangle(0, 0, W, H)
        ctx.set_source(g)
        ctx.fill()

        # Holographic mission console table in foreground
        rrect(ctx, 160, 680, 760, 180, 20)
        rgba(ctx, DARK_STEEL, 0.95)
        ctx.fill()
        # Glowing holographic mission grid
        for hx in range(200, 880, 60):
            line(ctx, [(hx, 700), (hx, 840)], UI, 1, 0.3)

        # Red weapon launch button
        circle(ctx, 740, 760, 32, RED, 0.85)
        circle(ctx, 740, 760, 18, (1.0, 0.3, 0.2), 1.0)

        # IAF Commander pressing button
        draw_commander_character(ctx, 420, 520, 1.4, t, pressing_button=(t > 1.2))


class StrikeScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"bomb": c("BOMB", 1.2), "shole": c("SHOLE", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["bomb"], "thud"), (b["shole"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        # Night mountain target zone
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, 0.01, 0.02, 0.05)
        g.add_color_stop_rgb(1, 0.03, 0.02, 0.02)
        ctx.rectangle(0, 0, W, H)
        ctx.set_source(g)
        ctx.fill()

        # Ghatak flying overhead with bay open
        draw_ghatak_drone(ctx, 540, 280, 1.15, t, bay_open=True, bomb_dropping=True)

        # Target enemy radar dome at bottom
        cx, cy = 540, 820
        circle(ctx, cx, cy, 70, (0.3, 0.35, 0.38))  # Radar dome

        # Explosion fireball when bomb hits
        if t > b["shole"]:
            ex_t = t - b["shole"]
            pulse = 1.0 + 0.3 * math.sin(ex_t * 12)
            circle(ctx, cx, cy, 140 * pulse, FIRE_ORANGE, 0.85)
            circle(ctx, cx, cy, 95 * pulse, GOLD, 0.9)
            circle(ctx, cx, cy, 45, INK, 1.0)


class EnemyPanicScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"paseena": c("PASEENA", 1.2), "hamla": c("HAMLA", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["paseena"], "pick"), (b["hamla"], "pop")]

    def draw(self, ctx, t, d):
        # Red emergency bunker lighting
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, 0.15, 0.02, 0.02)
        g.add_color_stop_rgb(1, 0.03, 0.01, 0.01)
        ctx.rectangle(0, 0, W, H)
        ctx.set_source(g)
        ctx.fill()

        # Emergency flashing red strobe
        strobe = 0.5 + 0.5 * math.sin(t * 8)
        circle(ctx, 540, 200, 320, RED, 0.15 * strobe)

        # Enemy General holding head, sweating profusely
        draw_enemy_general(ctx, 540, 560, 1.4, t)


class CtaScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"garv": c("GARV", 1.2), "sub": c("SUBSCRIBE", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["garv"], "pop"), (b["sub"], "pick")]

    def draw(self, ctx, t, d):
        # Majestic twilight sky
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, 0.02, 0.06, 0.14)
        g.add_color_stop_rgb(0.6, 0.18, 0.08, 0.04)
        g.add_color_stop_rgb(1.0, 0.02, 0.02, 0.04)
        ctx.rectangle(0, 0, W, H)
        ctx.set_source(g)
        ctx.fill()

        # Indian Flag fluttering
        flag(ctx, 420, 260, 240, 160, "india", 0.0)

        # Indian Commander smiling in center with thumbs up
        draw_commander_character(ctx, 540, 620, 1.45, t, pressing_button=False)

        # Ghatak flying victoriously in the background
        draw_ghatak_drone(ctx, 780, 280, 0.65, t)


SCENE_CLASSES = {
    "radar_bunker": RadarBunkerScene,
    "ghost_shadow": GhostShadowScene,
    "reveal": RevealScene,
    "stealth_physics": StealthPhysicsScene,
    "command_center": CommandCenterScene,
    "strike": StrikeScene,
    "enemy_panic": EnemyPanicScene,
    "cta": CtaScene,
}


def write_alignment(final: Path) -> None:
    """Word-level alignment export for captions & subtitles."""
    out = [
        {
            "scene": spec["key"],
            "start": round(s["start"], 3),
            "dur": round(s["dur"], 3),
            "words": [{"t": round(s["start"] + st, 3), "w": w} for st, w in s["captions"]],
        }
        for spec, s in zip(SPEC, engine.SCENES)
    ]
    path = final.with_suffix(".json")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Alignment: {path}")


# ============================================================ UPLOAD KIT

UPLOAD = {
    "titles": [
        "DRDO Ka Ghatak Drone: Dushman Ke Radar Ka Kaal!",
        "Ghatak Stealth UCAV: B-2 Bomber Jaisa Desi Shikari",
        "Dushman Ka Radar Andha! DRDO Ka Ghatak Stealth Drone",
        "Ghatak Drone: Bina Pilot Ke Surgical Strike Karega Bharat",
        "DRDO Ka Secret Stealth Drone: Ghatak UCAV Explained",
        "Ghatak Drone: Radar Par Ek Pakshi Bhi Nahi Dikhega",
        "Indian Air Force Ka Adrishya Shikari: Ghatak Drone",
        "Ghatak UCAV: Kaveri Engine Wala Bharat Ka Stealth Drone",
    ],
    "title": "DRDO Ka Ghatak Drone: Dushman Ke Radar Ka Kaal!",
    "thumb_text": "GHATAK DRONE",
    "queries": ["ghatak drone", "drdo ghatak ucav", "drdo stealth drone"],
    "description": """DRDO Ghatak Stealth UCAV: Bharat ka sabse khufiya aur deadly bina pilot ka ladaku drone.
America ke B-2 stealth bomber jaise flying-wing design wala Ghatak UCAV dushman ke radar ko andha karke unke military addo par deep surgical strike kar sakta hai.

Is Short me:
• Dushman ke radar se poori tarah adrishya
• Flying-wing design aur special radar-absorbent coating
• Internal weapons bay se laser-guided bomb strike
• Desi Dry Kaveri engine power
• Bina kisi pilot ki jaan khatre me daale dushman ke base tabah

Aapko Bharat ke is adrishya shikari par kitna garv hai? Comment me likho - Jai Hind!
Subscribe to Reality Shift for hard-hitting defence and geopolitical analysis.

Sources: DRDO ADE Bangalore, GTRE, Ministry of Defence.

#Shorts #GhatakDrone #DRDO #IndianAirForce
""",
    "tags": ["ghatak drone", "drdo ghatak", "ghatak ucav", "drdo stealth drone", "swift drone",
             "indian air force", "kaveri engine", "stealth bomber", "indian defence shorts",
             "geopolitics hindi", "bharat news shorts", "reality shift"],
    "hashtags": ["#Shorts", "#GhatakDrone", "#DRDO", "#IndianAirForce"],
}


def thumbnail(ctx):
    """1080x1920 cover: 'GHATAK DRONE' over sleek flying-wing stealth UCAV."""
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.01, 0.02, 0.05)
    g.add_color_stop_rgb(0.5, 0.05, 0.08, 0.12)
    g.add_color_stop_rgb(1.0, 0.01, 0.01, 0.02)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()

    draw_ghatak_drone(ctx, 540, 780, 2.0, 0.5)

    g = cairo.LinearGradient(0, 1150, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.88)
    ctx.rectangle(0, 1150, W, H - 1150)
    ctx.set_source(g)
    ctx.fill()

    g = cairo.LinearGradient(0, 0, 0, 780)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.92)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 780)
    ctx.set_source(g)
    ctx.fill()

    vignette(ctx)
    text(ctx, "GHATAK DRONE", 540, 290, 150, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "DRDO STEALTH UCAV", 540, 460, 90, INK, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, INK, a=0.7)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.ghatak")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
