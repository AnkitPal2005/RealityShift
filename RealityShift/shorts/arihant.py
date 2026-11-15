"""Reality Shift Short - "INS Arihant: Deep Sea Nuclear Patrol & 2nd Strike Explained" (~45-50s).

Usage:
  python make.py arihant --kiki-export     # exports clean narrator text for KikiVoice
  python make.py arihant --check           # policy check
  python make.py arihant --engine edge     # preview render with edge-tts
  python make.py arihant                   # final render from KikiVoice files

Strategic overview:
INS Arihant (SSBN 73) is India's first indigenous nuclear-powered ballistic missile submarine.
Powered by an 83 MW pressurized water reactor developed by BARC, it gives India Continuous
At-Sea Deterrence (CASD) and an invulnerable 'Second Strike' capability under India's
No First Use nuclear doctrine. Armed with K-15 and K-4 SLBMs launched from submerged depths,
and protected by anechoic acoustic stealth and the Project Varsha underground mountain base,
INS Arihant guarantees absolute deterrence against any hostile power.
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

TOPIC = "INS ARIHANT DEEP SEA DETERRENCE"
OUTPUTS = {"edge": "arihant_short.mp4"}
LEGO = {"header": "intel", "caption": "typewriter", "transition": "shutter", "palette": "amber", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.55
TAIL_PAD = 0.20
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 84
MUSIC_STYLE = "ambient"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 500

PAL = lego.PALETTES["amber"]
UI = PAL["ui"]
HI = PAL["hi"]
RED = PAL["alert"]
INK = PAL["ink"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
STEEL = hexc("#90A4AE")
DARK_STEEL = hexc("#1A2530")
HULL_BLACK = hexc("#101720")
OCEAN_DEEP = hexc("#030A14")
OCEAN_MID = hexc("#071E32")
OCEAN_SURF = hexc("#0F3556")
CHERENKOV_BLUE = hexc("#00E5FF")
REACTOR_GLOW = hexc("#80D8FF")
SONAR_GREEN = hexc("#00E676")
NAVY_GOLD = hexc("#FFD700")
BOOSTER_FIRE = hexc("#FF6D00")

SOURCES = [
    "Ministry of Defence & Prime Minister's Office (November 2018): Announcement of INS Arihant's first deterrence "
    "patrol, formally establishing India's operational nuclear triad (PIB New Delhi).",
    "Bhabha Atomic Research Centre (BARC) & Indian Navy: Development of the 83 MW pressurized light-water reactor (PWR) "
    "fueled by enriched uranium for the Advanced Technology Vessel (ATV) project.",
    "SIPRI Military Expenditure & Nuclear Forces Database (2024-2026): Details on India's SSBN program, K-15 Sagarika "
    "(750 km) and K-4 (3,500 km) Submarine Launched Ballistic Missiles (SLBM), and Project Varsha at Rambilli.",
]

SPEC = [
    {"key": "hook", "accent": CHERENKOV_BLUE, "text": "INS ARIHANT // DEEP SEA GHOST",
     "visual": "Deep midnight ocean abyss in pitch dark waters; INS Arihant submarine gliding silently with subtle water trails; Naval Commander at periscope console tracking stealth",
     "vo": [("hook", [("समंदर के गहरे पानी में,", "SAMANDAR KE GEHRE PAANI MEIN,"),
                      ("चुपचाप तैर रहा है", "CHUPCHAP TAIR RAHA HAI"),
                      ("भारत का सबसे खतरनाक हथियार—", "BHARAT KA SABSE KHATARNAK HATHIYAR—"),
                      ("पनडुब्बी अरिहंत!", "PANDUBBI ARIHANT!"),
                      ("जिसकी भनक तक", "JISKI BHANAK TAK"),
                      ("दुश्मन को नहीं लगती।", "DUSHMAN KO NAHI LAGTI.")])]},

    {"key": "triad", "accent": HI, "text": "NUCLEAR TRIAD // SECOND STRIKE",
     "visual": "Nuclear Triad HUD: Land Agni launcher, Air Su-30MKI jet, and Sea INS Arihant; enemy preemptive strike destroys land/air bases, but Arihant in deep water guarantees retaliatory second strike",
     "vo": [("tell", [("भारत का सीधा नियम है—", "BHARAT KA SEEDHA NIYAM HAI—"),
                      ("हम पहले कभी हमला नहीं करेंगे।", "HUM PEHLE HAMLA NAHI KARENGE."),
                      ("लेकिन अगर दुश्मन ने हमारे सारे ठिकाने उड़ा भी दिए,", "LEKIN DUSHMAN NE THIKANE UDA BHI DIYE,"),
                      ("तो समंदर के नीचे से अरिहंत", "TOH NEECHE SE ARIHANT"),
                      ("ऐसा पलटवार करेगा कि नक्शा बदल जाएगा!", "AISA PALATWAR KAREGA KI NAKSHA BADAL JAYEGA!")])]},

    {"key": "reactor", "accent": CHERENKOV_BLUE, "text": "83 MW REACTOR // MONTHS SUBMERGED",
     "visual": "Cross section of Arihant nuclear bay; BARC Chief Scientist in radiation protective gear monitoring 83 MW reactor core glowing in eerie Cherenkov blue radiation; unlimited underwater endurance",
     "vo": [("tell", [("आम पनडुब्बियों को हवा लेने", "AAM PANDUBBI KO HAWA LENE"),
                      ("बार-बार पानी के ऊपर आना पड़ता है।", "BAAR BAAR SURFACE PAR AANA PADTA HAI."),
                      ("लेकिन अपनी परमाणु ताकत के दम पर,", "LEKIN APNI PARMANU TAAQAT SE,"),
                      ("अरिहंत महीनों तक बिना बाहर निकले", "ARIHANT MAHINON TAK SUBMERGED"),
                      ("पानी के अंदर छुपा रहता है!", "PAANI KE ANDAR CHHUPA REHTA HAI!")])]},

    {"key": "slbm", "accent": RED, "text": "K-15 & K-4 // UNDERWATER LAUNCH",
     "visual": "Submarine VLS missile deck hatch opens underwater; high-pressure gas launches K-15/K-4 missile through water column; missile breaches surface into white froth and rocket engine roars into space",
     "vo": [("tell", [("इसकी पीठ पर तैनात हैं", "ISKI PEETH PAR TAINAAT HAIN"),
                      ("भारत की सबसे ताकतवर मिसाइलें।", "BHARAT KI SABSE TAAQATWAR MISSILES."),
                      ("गहरे पानी से भारी दबाव के साथ मिसाइल निकलती है,", "GEHRE PAANI SE BHARI DABAV SE MISSILE NIKALTI HAI,"),
                      ("और पानी को चीरती हुई", "AUR PAANI KO CHEERTI HUYI"),
                      ("सीधे आसमान में उड़ जाती है!", "SEEDHE AASMAAN MEIN UDD JAATI HAI!")])]},

    {"key": "stealth", "accent": SONAR_GREEN, "text": "ANECHOIC TILES // PROJECT VARSHA",
     "visual": "Left: Close-up of rubber anechoic tiles absorbing enemy active sonar waves; Right: Coastline granite mountain carved with deep underground submarine pens at Project Varsha",
     "vo": [("tell", [("इसकी ख़ास काली परत", "ISKI KHAAS KAALI PARAT"),
                      ("दुश्मन की पकड़ में नहीं आने देती।", "DUSHMAN KI PAKAD MEIN NAHI AANE DETI."),
                      ("और विशाखापट्टनम का गुप्त अड्डा वर्षा—", "AUR PROJECT VARSHA KA GUPT ADDA—"),
                      ("पहाड़ के अंदर बनी वो गुफा है,", "PAHAAD KE ANDAR WOH GUFA HAI,"),
                      ("जहाँ आसमान से कोई भी इसे देख नहीं सकता!", "JAHAN KOI BHI ISE DEKH NAHI SAKTA!")])]},

    {"key": "poll", "accent": HI, "text": "BHARAT KA SABSE BADA RAKSHAK?",
     "visual": "Naval Commander and BARC Scientist standing proud beside Indian Naval Crest; interactive poll card: 'KYA ARIHANT BHARAT KA SABSE BADA RAKSHAK HAI?'; animated cursor clicking HAAN",
     "vo": [("ask", [("अरिहंत ने भारत को", "ARIHANT NE BHARAT KO"),
                     ("समंदर में सबसे ताकतवर बना दिया है।", "SAMANDAR MEIN SABSE TAAQATWAR BANA DIYA HAI."),
                     ("क्या ये भारत का सबसे बड़ा रक्षा कवच है?", "KYA YEH BHARAT KA SABSE BADA RAKSHA KAVACH HAI?"),
                     ("अपनी राय नीचे बताइए,", "APNI RAI NEECHE BATAIYE,"),
                     ("और हमारे साथ ज़रूर जुड़िए!", "AUR HAMARE SAATH ZAROOR JUDIYE!")])]},
]

DELIVERY = delivery.build(SPEC)
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "SAMANDAR": OCEAN_SURF, "300": CHERENKOV_BLUE, "METER": CHERENKOV_BLUE, "NEECHE,": CHERENKOV_BLUE,
    "KHAMOSH": STEEL, "GHATAK": RED, "HATHIYAR—": RED, "PANDUBBI": NAVY_GOLD, "ARIHANT!": NAVY_GOLD,
    "ARIHANT": NAVY_GOLD, "BHANAK": STEEL, "ATOOT": HI, "NIYAM": HI, "WAR": RED,
    "THIKANE": RED, "TABAH": RED, "PALATWAR": RED, "NAKSHA": RED, "SADHARAN": STEEL,
    "HAWA": CHERENKOV_BLUE, "SURFACE": OCEAN_SURF, "SHAKTISHALI": HI, "PARMANU": CHERENKOV_BLUE,
    "BHATTI": CHERENKOV_BLUE, "MAHINON": HI, "SUBMERGED": CHERENKOV_BLUE, "PEETH": STEEL,
    "TAINAAT": STEEL, "K-15": RED, "K-4": RED, "MISSILES.": RED, "BHARI": STEEL, "DABAV": STEEL,
    "PAANI": CHERENKOV_BLUE, "AASMAAN": HI, "DAHADTI": RED, "KHAAS": SONAR_GREEN, "RUBBER": SONAR_GREEN,
    "PARAT": SONAR_GREEN, "TARANGON": SONAR_GREEN, "SOKH": SONAR_GREEN, "PROJECT": NAVY_GOLD,
    "VARSHA": NAVY_GOLD, "GUPT": NAVY_GOLD, "ADDA—": STEEL, "PAHAAD": STEEL, "UPAGRAH": RED,
    "AJEYA": NAVY_GOLD, "RAKSHA": HI, "KAVACH": HI, "HAAN": INDIA_GREEN, "NAA": RED,
    "RAI": HI, "BATAIYE,": HI, "REALITY": UI, "SHIFT": UI, "JUDIYE!": SAFFRON
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


def ocean_bg(ctx, t, depth_level="deep"):
    """Photorealistic ocean depth gradient with floating marine particles & sonar grids."""
    g = cairo.LinearGradient(0, 0, 0, H)
    if depth_level == "deep":
        g.add_color_stop_rgb(0, 0.015, 0.04, 0.08)
        g.add_color_stop_rgb(0.4, 0.008, 0.02, 0.045)
        g.add_color_stop_rgb(1.0, 0.002, 0.005, 0.012)
    elif depth_level == "surface":
        g.add_color_stop_rgb(0, 0.08, 0.22, 0.38)
        g.add_color_stop_rgb(0.35, 0.03, 0.10, 0.20)
        g.add_color_stop_rgb(1.0, 0.01, 0.03, 0.07)
    else:  # tactical interior
        g.add_color_stop_rgb(0, 0.03, 0.02, 0.01)
        g.add_color_stop_rgb(0.5, 0.02, 0.015, 0.01)
        g.add_color_stop_rgb(1.0, 0.01, 0.01, 0.015)

    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()

    # Subtle tactical grid
    for x in range(0, W + 1, 90):
        line(ctx, [(x, 0), (x, H)], UI, 1, 0.04)
    for y in range(0, H + 1, 90):
        line(ctx, [(0, y), (W, y)], UI, 1, 0.04)

    # Ambient bioluminescent / marine snow particles
    for i in range(16):
        px = (i * 67 + int(t * 15 * (1 + (i % 3) * 0.5))) % W
        py = (i * 123 + int(t * 10 * (1 + (i % 2) * 0.4))) % H
        r = 1.5 + (i % 3)
        circle(ctx, px, py, r, CHERENKOV_BLUE if i % 2 == 0 else SONAR_GREEN, 0.25 + 0.2 * math.sin(t * 2 + i))


# ============================================================ VEHICLES & ASSETS

def ins_arihant_sub(ctx, x, y, s, t, launch_mode=False, a=1.0):
    """Detailed INS Arihant SSBN-73 profile with sail, missile hump, anechoic tiles, pumpjet."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # Deep water shadow underneath
    ell(ctx, 0, 55, 340, 45)
    rgba(ctx, (0, 0, 0), 0.7 * a)
    ctx.fill()

    # Main Teardrop Hull
    hull_pts = [
        (-310, 0), (-260, -32), (-120, -36), (100, -36),
        (260, -30), (330, -5), (350, 0), (330, 8),
        (260, 32), (100, 38), (-120, 38), (-260, 32)
    ]
    smooth(ctx, hull_pts, closed=True, k=0.18)
    rgba(ctx, HULL_BLACK, a)
    ctx.fill()

    # Anechoic Tile Pattern Highlights (fine subtle panel seams)
    for tx in range(-250, 320, 35):
        line(ctx, [(tx, -30), (tx, 32)], STEEL, 1, 0.12 * a)
    line(ctx, [(-260, 0), (330, 0)], STEEL, 1, 0.15 * a)

    # Ballast Waterline & Trim Markings
    line(ctx, [(-250, 15), (310, 15)], RED, 2.5, 0.5 * a)

    # Missile Hump (Raised casing behind sail for 4 VLS silos)
    hump_pts = [(-70, -36), (-50, -56), (90, -56), (110, -36)]
    smooth(ctx, hump_pts, closed=True, k=0.08)
    rgba(ctx, hexc("#17202A"), a)
    ctx.fill()

    # 4 Vertical Launch Silo Hatches on the hump
    for h in range(4):
        hx = -30 + h * 32
        if launch_mode and h == 1:
            # Open Hatch at 85 degrees
            line(ctx, [(hx, -56), (hx - 12, -88)], hexc("#546E7A"), 5, a)
            # Silo tube opening interior glow
            ell(ctx, hx + 5, -56, 10, 4)
            rgba(ctx, RED, 0.9 * a)
            ctx.fill()
        else:
            # Closed hatch cover
            rrect(ctx, hx - 10, -58, 20, 4, 1)
            rgba(ctx, hexc("#455A64"), a)
            ctx.fill()

    # Sail (Conning Tower)
    sail_pts = [(-170, -34), (-155, -120), (-100, -120), (-90, -34)]
    smooth(ctx, sail_pts, closed=True, k=0.06)
    rgba(ctx, hexc("#1A2530"), a)
    ctx.fill()

    # Hydroplanes (Diving fins on the sail)
    rrect(ctx, -145, -88, 48, 8, 3)
    rgba(ctx, hexc("#37474F"), a)
    ctx.fill()

    # Periscope & Sensor Masts
    for mi, mx in enumerate([-145, -132, -118, -108]):
        mh = 22 + (mi % 2) * 10
        line(ctx, [(mx, -120), (mx, -120 - mh)], STEEL, 3, 0.85 * a)
        circle(ctx, mx, -120 - mh, 3, CHERENKOV_BLUE if mi == 1 else STEEL, a)

    # Bow Sonar Dome (Rounded acoustic nose)
    dome_pts = [(310, -25), (350, 0), (310, 25)]
    smooth(ctx, dome_pts, closed=True, k=0.2)
    rgba(ctx, hexc("#0D131A"), a)
    ctx.fill()
    arc_c = CHERENKOV_BLUE
    for dr in range(3):
        ctx.arc(330, 0, 16 + dr * 8, -math.pi * 0.4, math.pi * 0.4)
        rgba(ctx, arc_c, (0.3 - dr * 0.08) * a)
        ctx.set_line_width(2)
        ctx.stroke()

    # Stern Control Fins (Cruciform rudders)
    # Top vertical rudder
    r_pts = [(-280, -28), (-315, -78), (-290, -78), (-255, -28)]
    smooth(ctx, r_pts, closed=True, k=0.05)
    rgba(ctx, hexc("#1A2530"), a)
    ctx.fill()
    # Bottom vertical rudder
    rb_pts = [(-280, 28), (-315, 78), (-290, 78), (-255, 28)]
    smooth(ctx, rb_pts, closed=True, k=0.05)
    rgba(ctx, hexc("#1A2530"), a)
    ctx.fill()

    # Shrouded Pump-jet Propulsor at the tail
    rrect(ctx, -338, -24, 30, 48, 4)
    rgba(ctx, hexc("#263238"), a)
    ctx.fill()
    # Propeller wake bubbles
    prop_phase = t * 14
    for b in range(4):
        bx = -350 - b * 30
        by = -4 + math.sin(prop_phase + b) * 8
        circle(ctx, bx, by, 3 + b * 2, CHERENKOV_BLUE, (0.4 - b * 0.08) * a)

    # Submarine Name & Pennant marking: "S73"
    text(ctx, "S73", -125, -55, 18, STEEL, font=lego.MONO, a=0.7 * a)

    ctx.restore()


# ============================================================ CHARACTERS

def naval_commander(ctx, x, y, s, t, pose="stand", a=1.0):
    """Indian Navy Commander in white uniform, peaked cap, epaulettes and binoculars."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # Feet / Shoes at Ground
    circle(ctx, -24, -10, 14, hexc("#101010"), a)
    circle(ctx, 24, -10, 14, hexc("#101010"), a)

    # White Naval Trousers
    line(ctx, [(-24, -20), (-18, -190)], (1, 1, 1), 32, a)
    line(ctx, [(24, -20), (18, -190)], (1, 1, 1), 32, a)
    # Trouser creases & black naval shoes
    rrect(ctx, -38, -18, 30, 16, 4)
    rgba(ctx, (0.05, 0.05, 0.05), a)
    ctx.fill()
    rrect(ctx, 8, -18, 30, 16, 4)
    rgba(ctx, (0.05, 0.05, 0.05), a)
    ctx.fill()

    # Black Belt with Gold Buckle
    rrect(ctx, -42, -202, 84, 18, 2)
    rgba(ctx, (0.1, 0.1, 0.1), a)
    ctx.fill()
    rrect(ctx, -12, -204, 24, 22, 2)
    rgba(ctx, NAVY_GOLD, a)
    ctx.fill()

    # White Naval Command Tunic / Shirt
    torso_pts = [(-52, -200), (52, -200), (46, -340), (-46, -340)]
    smooth(ctx, torso_pts, closed=True, k=0.05)
    rgba(ctx, (0.97, 0.97, 0.98), a)
    ctx.fill()
    line(ctx, [(0, -200), (0, -340)], hexc("#CFD8DC"), 2, a)

    # Shoulder Epaulettes (Black with Gold Stripes & Navy Emblem)
    for side in (-1, 1):
        rrect(ctx, side * 45 - 12, -346, 24, 12, 2)
        rgba(ctx, (0.08, 0.1, 0.14), a)
        ctx.fill()
        line(ctx, [(side * 45 - 10, -340), (side * 45 + 10, -340)], NAVY_GOLD, 3, a)

    # Chest Medal Ribbons & Gold Badge
    rrect(ctx, -36, -315, 26, 12, 2)
    rgba(ctx, SAFFRON, a)
    ctx.fill()
    circle(ctx, -23, -290, 6, NAVY_GOLD, a)

    # Arms and Poses
    if pose == "binoculars":
        # Both arms raised holding binoculars to eyes
        line(ctx, [(-44, -330), (-60, -380), (-16, -400)], (1, 1, 1), 22, a)
        line(ctx, [(44, -330), (60, -380), (16, -400)], (1, 1, 1), 22, a)
        # Black Naval Binoculars
        rrect(ctx, -28, -412, 24, 30, 4)
        rgba(ctx, (0.12, 0.14, 0.16), a)
        ctx.fill()
        rrect(ctx, 4, -412, 24, 30, 4)
        rgba(ctx, (0.12, 0.14, 0.16), a)
        ctx.fill()
        # Cyan lens glint
        circle(ctx, -16, -400, 8, CHERENKOV_BLUE, 0.8 * a)
        circle(ctx, 16, -400, 8, CHERENKOV_BLUE, 0.8 * a)
    elif pose == "salute":
        # Right arm sharply raised in crisp naval salute
        line(ctx, [(-44, -330), (-52, -260), (-38, -210)], (1, 1, 1), 22, a)
        line(ctx, [(44, -330), (74, -380), (46, -415)], (1, 1, 1), 22, a)
        circle(ctx, 46, -415, 10, hexc("#D7CCC8"), a)
    else:  # stand / command
        line(ctx, [(-44, -330), (-62, -260), (-50, -210)], (1, 1, 1), 22, a)
        line(ctx, [(44, -330), (62, -260), (50, -210)], (1, 1, 1), 22, a)
        # Tactical tablet in right hand
        rrect(ctx, 42, -225, 34, 46, 4)
        rgba(ctx, (0.1, 0.15, 0.2), a)
        ctx.fill()
        rrect(ctx, 45, -222, 28, 40, 2)
        rgba(ctx, CHERENKOV_BLUE, 0.7 * a)
        ctx.fill()

    # Head and Neck
    rrect(ctx, -14, -360, 28, 24, 4)
    rgba(ctx, hexc("#E0CFB9"), a)
    ctx.fill()
    circle(ctx, 0, -388, 32, hexc("#E0CFB9"), a)

    # Facial details: determined eyes, moustache
    circle(ctx, -10, -390, 3, (0.1, 0.1, 0.12), a)
    circle(ctx, 10, -390, 3, (0.1, 0.1, 0.12), a)
    # Naval Moustache
    line(ctx, [(-14, -378), (14, -378)], (0.15, 0.12, 0.1), 3.5, a)

    # Indian Navy Officer Peaked Cap
    # Black Visor / Peak with gold oak leaves
    rrect(ctx, -38, -406, 76, 12, 4)
    rgba(ctx, (0.05, 0.05, 0.05), a)
    ctx.fill()
    # Gold chin strap
    line(ctx, [(-34, -410), (34, -410)], NAVY_GOLD, 3, a)
    # White Crown
    crown_pts = [(-38, -412), (38, -412), (48, -440), (-48, -440)]
    smooth(ctx, crown_pts, closed=True, k=0.08)
    rgba(ctx, (1, 1, 1), a)
    ctx.fill()
    # Gold Anchor & Ashoka Emblem on front of cap
    circle(ctx, 0, -425, 8, NAVY_GOLD, a)

    ctx.restore()


def barc_scientist(ctx, x, y, s, t, a=1.0):
    """BARC Chief Nuclear Scientist in protective navy coveralls, dosimeter badge, diagnostics pad."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # Protective Safety Boots
    rrect(ctx, -38, -18, 30, 16, 4)
    rgba(ctx, (0.1, 0.12, 0.14), a)
    ctx.fill()
    rrect(ctx, 8, -18, 30, 16, 4)
    rgba(ctx, (0.1, 0.12, 0.14), a)
    ctx.fill()

    # Dark Navy / Lead-lined protective coverall legs
    line(ctx, [(-24, -20), (-18, -190)], hexc("#1A365D"), 34, a)
    line(ctx, [(24, -20), (18, -190)], hexc("#1A365D"), 34, a)

    # Heavy Duty Utility Belt
    rrect(ctx, -44, -202, 88, 18, 2)
    rgba(ctx, (0.1, 0.1, 0.1), a)
    ctx.fill()

    # Torso (Navy coverall with yellow safety stripes)
    torso_pts = [(-52, -200), (52, -200), (46, -340), (-46, -340)]
    smooth(ctx, torso_pts, closed=True, k=0.05)
    rgba(ctx, hexc("#1E3A5F"), a)
    ctx.fill()
    # Radiation hazard chevron stripes on shoulders
    line(ctx, [(-46, -325), (46, -325)], HI, 4, a)

    # Dosimeter Radiation Badge (Green safe LED)
    rrect(ctx, -34, -295, 20, 26, 3)
    rgba(ctx, (1, 1, 1), a)
    ctx.fill()
    circle(ctx, -24, -282, 5, SONAR_GREEN, a)

    # BARC Logo Crest
    circle(ctx, 24, -282, 8, NAVY_GOLD, a)

    # Arms holding digital reactor diagnostics pad
    line(ctx, [(-44, -330), (-65, -260), (-20, -235)], hexc("#1E3A5F"), 24, a)
    line(ctx, [(44, -330), (65, -260), (20, -235)], hexc("#1E3A5F"), 24, a)

    # Digital Diagnostics Pad (Glowing blue Cherenkov monitor)
    rrect(ctx, -38, -250, 76, 52, 6)
    rgba(ctx, (0.05, 0.08, 0.12), a)
    ctx.fill()
    rrect(ctx, -34, -246, 68, 44, 4)
    rgba(ctx, CHERENKOV_BLUE, 0.85 * a)
    ctx.fill()
    # Telemetry sine waves on screen
    line(ctx, [(-28, -224), (-12, -232), (8, -218), (28, -224)], (0.05, 0.1, 0.2), 2.5, a)

    # Head and Glasses
    rrect(ctx, -14, -360, 28, 24, 4)
    rgba(ctx, hexc("#E0CFB9"), a)
    ctx.fill()
    circle(ctx, 0, -388, 30, hexc("#E0CFB9"), a)

    # Glasses & Eyes
    rrect(ctx, -20, -396, 16, 12, 2)
    rgba(ctx, STEEL, a)
    ctx.set_line_width(2)
    ctx.stroke()
    rrect(ctx, 4, -396, 16, 12, 2)
    rgba(ctx, STEEL, a)
    ctx.set_line_width(2)
    ctx.stroke()
    line(ctx, [(-4, -390), (4, -390)], STEEL, 2, a)

    # Scientist Hair
    ctx.arc(0, -400, 31, math.pi * 0.9, 2.1 * math.pi)
    rgba(ctx, (0.2, 0.2, 0.22), a)
    ctx.fill()

    ctx.restore()


# ============================================================ SCENE RENDERERS

def hook_scene(ctx, t, d):
    """Scene 1: Deep ocean abyss (300m), silent submarine glide, Commander observing stealth."""
    ocean_bg(ctx, t, depth_level="deep")

    # Depth Gauge on Top Right
    rrect(ctx, 760, 220, 240, 68, 8)
    rgba(ctx, (0.02, 0.04, 0.08), 0.9)
    ctx.fill()
    rrect(ctx, 760, 220, 240, 68, 8)
    rgba(ctx, CHERENKOV_BLUE, 0.7)
    ctx.set_line_width(2)
    ctx.stroke()
    text(ctx, "DEPTH: 300 METERS", 880, 252, 22, CHERENKOV_BLUE, font=lego.MONO)
    text(ctx, "STATUS: ULTRA-STEALTH", 880, 274, 16, SONAR_GREEN, font=lego.MONO)

    # Sonar sweep wave pulsing from bow
    cx, cy = 680, 750
    pulse = (t * 0.5) % 1.0
    circle(ctx, cx, cy, 80 + pulse * 280, CHERENKOV_BLUE, (1 - pulse) * 0.4)

    # Gliding INS Arihant Submarine (scale: 1.15)
    sub_x = 480 + 35 * math.sin(t * 0.8)
    sub_y = 750 + 12 * math.cos(t * 0.6)
    ins_arihant_sub(ctx, sub_x, sub_y, 1.15, t)

    # Naval Commander standing beside tactical console
    naval_commander(ctx, 240, 1170, 0.72, t, pose="binoculars")

    # Stamp: "PATAAL KA BHEDIYA // 100% STEALTH"
    stamp(ctx, 540, 320, t, -0.04, 540, 90, CHERENKOV_BLUE, [("INS ARIHANT: DEEP GHOST", 8, 42, CHERENKOV_BLUE)])
    tag(ctx, "UNDETECTABLE TO ENEMY SATELLITE & RADAR", 540, 1100, SONAR_GREEN, 1.0, size=28)


def triad_scene(ctx, t, d):
    """Scene 2: India's Nuclear Triad & Second Strike Capability HUD."""
    ocean_bg(ctx, t, depth_level="surface")

    # Center Trident / Trishul Crest
    circle(ctx, 540, 460, 95, NAVY_GOLD, 0.15)
    circle(ctx, 540, 460, 95, NAVY_GOLD, 0.8)
    # Trishul Prongs
    line(ctx, [(540, 520), (540, 380)], NAVY_GOLD, 8)
    line(ctx, [(500, 460), (500, 395)], NAVY_GOLD, 6)
    line(ctx, [(580, 460), (580, 395)], NAVY_GOLD, 6)
    line(ctx, [(490, 460), (590, 460)], NAVY_GOLD, 6)
    text(ctx, "NUCLEAR TRIAD", 540, 590, 32, NAVY_GOLD, font=CAPTION_FONT)

    # 3 Triad Cards:
    # 1. LAND: Agni Missiles
    rrect(ctx, 60, 640, 280, 320, 10)
    rgba(ctx, (0.05, 0.02, 0.02), 0.9)
    ctx.fill()
    rrect(ctx, 60, 640, 280, 320, 10)
    rgba(ctx, RED, 0.7)
    ctx.set_line_width(2)
    ctx.stroke()
    tag(ctx, "LAND (AGNI)", 200, 680, RED, 1.0, size=22)
    # Missile Launcher silhouette
    line(ctx, [(140, 830), (220, 750)], SAFFRON, 10)
    text(ctx, "AIRFIELDS & BASES", 200, 880, 18, STEEL, font=lego.MONO)
    text(ctx, "VULNERABLE 1ST HIT", 200, 915, 18, RED, font=lego.MONO)

    # 2. AIR: Su-30MKI / Rafale
    rrect(ctx, 740, 640, 280, 320, 10)
    rgba(ctx, (0.05, 0.02, 0.02), 0.9)
    ctx.fill()
    rrect(ctx, 740, 640, 280, 320, 10)
    rgba(ctx, RED, 0.7)
    ctx.set_line_width(2)
    ctx.stroke()
    tag(ctx, "AIR (SU-30 / RAFALE)", 880, 680, RED, 1.0, size=22)
    # Jet silhouette
    line(ctx, [(840, 800), (920, 800)], STEEL, 6)
    line(ctx, [(880, 770), (880, 830)], STEEL, 4)
    text(ctx, "HANGARS & RUNWAYS", 880, 880, 18, STEEL, font=lego.MONO)
    text(ctx, "CAN BE TARGETED", 880, 915, 18, RED, font=lego.MONO)

    # 3. SEA: INS Arihant (Center Big Green Card)
    rrect(ctx, 360, 640, 360, 340, 12)
    rgba(ctx, (0.01, 0.05, 0.03), 0.95)
    ctx.fill()
    rrect(ctx, 360, 640, 360, 340, 12)
    rgba(ctx, SONAR_GREEN, 0.9)
    ctx.set_line_width(3)
    ctx.stroke()
    tag(ctx, "SEA: INS ARIHANT", 540, 680, SONAR_GREEN, 1.0, size=26)
    ins_arihant_sub(ctx, 540, 770, 0.45, t)
    text(ctx, "SECOND STRIKE GUARANTEE", 540, 860, 20, HI, font=lego.MONO)
    text(ctx, "100% UNTOUCHABLE", 540, 895, 24, SONAR_GREEN, font=CAPTION_FONT)
    text(ctx, "ASSURED RETALIATION", 540, 935, 18, INK, font=lego.MONO)

    # Bottom Commander & Scientist
    naval_commander(ctx, 250, 1170, 0.70, t, pose="stand")
    barc_scientist(ctx, 830, 1170, 0.70, t)

    tag(ctx, "NO FIRST USE // GUARANTEED 2ND STRIKE", 540, 280, HI, 1.0)


def reactor_scene(ctx, t, d):
    """Scene 3: BARC 83 MW Pressurized Light-Water Reactor & Unlimited Submersion."""
    ocean_bg(ctx, t, depth_level="tactical")

    # Reactor Pressure Vessel (RPV) Housing
    rx, ry = 540, 680
    rrect(ctx, rx - 180, ry - 220, 360, 440, 30)
    rgba(ctx, (0.08, 0.1, 0.14))
    ctx.fill()
    rrect(ctx, rx - 180, ry - 220, 360, 440, 30)
    rgba(ctx, STEEL, 0.8)
    ctx.set_line_width(6)
    ctx.stroke()

    # Inner Cherenkov Radiation Chamber (Vibrant pulsating blue glow)
    glow_pulse = 0.6 + 0.3 * math.sin(t * 5)
    glow(ctx, rx, ry, 170, CHERENKOV_BLUE, glow_pulse)
    ell(ctx, rx, ry, 130, 180)
    rgba(ctx, (0.0, 0.45, 0.85), 0.75)
    ctx.fill()

    # Uranium Fuel Rod Assemblies
    for rod in range(7):
        rodx = rx - 90 + rod * 30
        rrect(ctx, rodx - 8, ry - 140, 16, 280, 4)
        rgba(ctx, (0.9, 0.95, 1.0), 0.9)
        ctx.fill()
        # Active neutron flux lines
        line(ctx, [(rodx, ry - 130), (rodx, ry + 130)], CHERENKOV_BLUE, 2, 0.8)

    # High-pressure Coolant Circulation Pipes
    line(ctx, [(rx - 180, ry - 80), (rx - 260, ry - 80), (rx - 260, ry + 160), (rx - 180, ry + 160)], CHERENKOV_BLUE, 16, 0.7)
    line(ctx, [(rx + 180, ry - 80), (rx + 260, ry - 80), (rx + 260, ry + 160), (rx + 180, ry + 160)], RED, 16, 0.7)

    # Reactor Telemetry Badge
    rrect(ctx, 320, 260, 440, 70, 8)
    rgba(ctx, (0.02, 0.04, 0.08), 0.95)
    ctx.fill()
    rrect(ctx, 320, 260, 440, 70, 8)
    rgba(ctx, CHERENKOV_BLUE, 0.8)
    ctx.set_line_width(2)
    ctx.stroke()
    text(ctx, "BARC 83 MW LIGHT-WATER REACTOR", 540, 292, 22, CHERENKOV_BLUE, font=lego.MONO)
    text(ctx, "AIR & WATER: 100% SELF-GENERATED", 540, 318, 18, SONAR_GREEN, font=lego.MONO)

    # BARC Scientist inspecting reactor telemetry
    barc_scientist(ctx, 240, 1170, 0.72, t)

    # Endurance Comparison Card on Right
    rrect(ctx, 640, 940, 380, 180, 10)
    rgba(ctx, (0.02, 0.05, 0.08), 0.92)
    ctx.fill()
    rrect(ctx, 640, 940, 380, 180, 10)
    rgba(ctx, UI, 0.7)
    ctx.set_line_width(2)
    ctx.stroke()
    text(ctx, "SUBMERGED ENDURANCE", 830, 975, 22, UI, font=CAPTION_FONT)
    text(ctx, "DIESEL SUB: 3-4 DAYS", 830, 1020, 20, RED, font=lego.MONO)
    text(ctx, "ARIHANT: MONTHS (UNLIMITED)", 830, 1065, 22, SONAR_GREEN, font=lego.MONO)
    text(ctx, "LIMIT: CREW FOOD SUPPLY ONLY", 830, 1098, 16, STEEL, font=lego.MONO)


def slbm_scene(ctx, t, d):
    """Scene 4: Submerged Ballistic Missile Launch (K-15 / K-4) breaking ocean surface."""
    ocean_bg(ctx, t, depth_level="surface")

    # Water Surface Line at y = 520
    line(ctx, [(0, 520), (W, 520)], (0.3, 0.7, 0.9), 6, 0.8)
    for wx in range(0, W + 1, 40):
        wy = 520 + 4 * math.sin(t * 8 + wx * 0.05)
        circle(ctx, wx, wy, 4, (0.8, 0.95, 1.0), 0.6)

    # Sky above y = 520, Ocean below y = 520
    text(ctx, "ATMOSPHERE / STRATOSPHERE", 260, 490, 20, STEEL, font=lego.MONO)
    text(ctx, "DEEP OCEAN LAUNCH DEPTH", 260, 560, 20, CHERENKOV_BLUE, font=lego.MONO)

    # Submarine submerged at bottom (scale: 0.85)
    ins_arihant_sub(ctx, 540, 980, 0.85, t, launch_mode=True)

    # High pressure bubble column rising from silo
    bubble_x = 540 + (-30 + 1 * 32) * 0.85
    for bi in range(12):
        by = 920 - bi * 34
        circle(ctx, bubble_x + math.sin(t * 12 + bi) * 12, by, 6 + bi * 2, (0.8, 0.95, 1.0), 0.5)

    # Submarine-Launched Missile breaching surface & roaring into sky!
    mx = bubble_x
    launch_progress = (t * 0.4) % 1.0
    my = 850 - launch_progress * 600

    # Missile Body (K-4 heavy SLBM)
    rrect(ctx, mx - 14, my - 90, 28, 120, 6)
    rgba(ctx, (0.95, 0.95, 0.98))
    ctx.fill()
    # Conical Ogive Warhead
    nose_pts = [(mx - 14, my - 90), (mx + 14, my - 90), (mx, my - 130)]
    smooth(ctx, nose_pts, closed=True)
    rgba(ctx, hexc("#212121"))
    ctx.fill()
    # Tricolour marking bands on missile
    rrect(ctx, mx - 14, my - 70, 28, 8, 1)
    rgba(ctx, SAFFRON)
    ctx.fill()
    rrect(ctx, mx - 14, my - 54, 28, 8, 1)
    rgba(ctx, INDIA_GREEN)
    ctx.fill()

    # Rocket booster fire plume (if above or near water)
    if my < 600:
        glow(ctx, mx, my + 50, 90, RED, 0.9)
        fire_pts = [(mx - 14, my + 30), (mx + 14, my + 30), (mx, my + 130 + 20 * math.sin(t * 20))]
        smooth(ctx, fire_pts, closed=True)
        rgba(ctx, BOOSTER_FIRE)
        ctx.fill()

    # Launch Specs HUD on Right
    rrect(ctx, 640, 240, 380, 180, 10)
    rgba(ctx, (0.02, 0.04, 0.08), 0.92)
    ctx.fill()
    rrect(ctx, 640, 240, 380, 180, 10)
    rgba(ctx, RED, 0.8)
    ctx.set_line_width(2)
    ctx.stroke()
    tag(ctx, "SLBM ARSENAL", 830, 280, RED, 1.0, size=24)
    text(ctx, "K-15 SAGARIKA: 750 KM", 830, 330, 22, HI, font=lego.MONO)
    text(ctx, "K-4 SLBM: 3,500 KM", 830, 375, 24, RED, font=CAPTION_FONT)

    # Naval Commander on left observing the launch
    naval_commander(ctx, 180, 1170, 0.68, t, pose="stand")

    tag(ctx, "UNDERWATER VERTICAL LAUNCH // K-4 SLBM", 540, 280, RED, 1.0)


def stealth_scene(ctx, t, d):
    """Scene 5: Anechoic Rubber Tiles absorbing sonar & Project Varsha underground base."""
    ocean_bg(ctx, t, depth_level="deep")

    # Center Divider
    line(ctx, [(540, 360), (540, 1120)], STEEL, 2, 0.3)

    # LEFT CARD: Anechoic Rubber Tiles
    rrect(ctx, 60, 380, 440, 680, 12)
    rgba(ctx, (0.02, 0.04, 0.06), 0.92)
    ctx.fill()
    rrect(ctx, 60, 380, 440, 680, 12)
    rgba(ctx, SONAR_GREEN, 0.8)
    ctx.set_line_width(2.5)
    ctx.stroke()

    tag(ctx, "ANECHOIC TILES", 280, 430, SONAR_GREEN, 1.0, size=28)
    # Anechoic tile rubber grid close-up
    for gx in range(120, 440, 50):
        for gy in range(480, 680, 50):
            rrect(ctx, gx, gy, 44, 44, 4)
            rgba(ctx, HULL_BLACK)
            ctx.fill()
            circle(ctx, gx + 22, gy + 22, 6, (0.2, 0.25, 0.3))

    # Incoming enemy sonar waves hitting and getting absorbed
    for sw in range(3):
        ctx.arc(100, 580, 40 + sw * 35, -0.6, 0.6)
        rgba(ctx, RED, 0.7 - sw * 0.2)
        ctx.set_line_width(4)
        ctx.stroke()

    text(ctx, "ACTIVE SONAR", 280, 740, 22, RED, font=lego.MONO)
    text(ctx, "99% ENERGY ABSORBED", 280, 785, 30, SONAR_GREEN, font=CAPTION_FONT)
    text(ctx, "ACOUSTIC BLIND SPOT", 280, 835, 22, HI, font=lego.MONO)
    stamp(ctx, 280, 940, t, -0.06, 320, 80, SONAR_GREEN, [("GHOST STEALTH", 6, 36, SONAR_GREEN)])

    # RIGHT CARD: Project Varsha Underground Mountain Base
    rrect(ctx, 580, 380, 440, 680, 12)
    rgba(ctx, (0.02, 0.04, 0.06), 0.92)
    ctx.fill()
    rrect(ctx, 580, 380, 440, 680, 12)
    rgba(ctx, NAVY_GOLD, 0.8)
    ctx.set_line_width(2.5)
    ctx.stroke()

    tag(ctx, "PROJECT VARSHA", 800, 430, NAVY_GOLD, 1.0, size=28)

    # Mountain Cliff profile with underground submarine pen
    mountain_pts = [(620, 680), (680, 500), (760, 480), (840, 520), (980, 680)]
    smooth(ctx, mountain_pts, closed=True)
    rgba(ctx, hexc("#37474F"))
    ctx.fill()
    # Underground pen cavern opening
    rrect(ctx, 720, 580, 160, 100, 16)
    rgba(ctx, (0.01, 0.02, 0.04))
    ctx.fill()
    # Submarine resting inside cavern pen
    ins_arihant_sub(ctx, 800, 640, 0.22, t)

    text(ctx, "RAMBILLI (VIZAG)", 800, 740, 22, STEEL, font=lego.MONO)
    text(ctx, "SOLID GRANITE SHIELD", 800, 785, 28, NAVY_GOLD, font=CAPTION_FONT)
    text(ctx, "IMMUNE TO SATELLITES", 800, 835, 22, SONAR_GREEN, font=lego.MONO)
    stamp(ctx, 800, 940, t, 0.06, 340, 80, NAVY_GOLD, [("UNTOUCHABLE", 6, 36, NAVY_GOLD)])

    tag(ctx, "STEALTH: ANECHOIC TILES + PROJECT VARSHA", 540, 280, SONAR_GREEN, 1.0)


def poll_scene(ctx, t, d):
    """Scene 6: Naval Commander & Scientist salute + Interactive Lego Poll."""
    ocean_bg(ctx, t, depth_level="deep")

    # Indian Flag Fluttering top left
    flag(ctx, 80, 380, 160, 100, "in", t)

    # Naval Commander in Salute on Left
    naval_commander(ctx, 270, 1170, 0.72, t, pose="salute")

    # BARC Scientist on Right
    barc_scientist(ctx, 810, 1170, 0.72, t)


# ============================================================ SCENE CLASSES

class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"paani": c("PAANI", 0.9), "arihant": c("ARIHANT", 2.2), "dushman": c("DUSHMAN", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["paani"], "whoosh"), (b["arihant"], "boom"), (b["dushman"], "beep")]

    def draw(self, ctx, t, d):
        hook_scene(ctx, t, d)


class Triad(Cued):
    def beats(self, d):
        c = self.cue
        return {"hamla": c("HAMLA", 1.0), "thikane": c("THIKANE", 2.2), "palatwar": c("PALATWAR", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["hamla"], "whoosh"), (b["thikane"], "boom"), (b["palatwar"], "thud")]

    def draw(self, ctx, t, d):
        triad_scene(ctx, t, d)


class Reactor(Cued):
    def beats(self, d):
        c = self.cue
        return {"hawa": c("HAWA", 0.9), "taaqat": c("TAAQAT", 2.2), "submerged": c("SUBMERGED", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["hawa"], "whoosh"), (b["taaqat"], "beep"), (b["submerged"], "boom")]

    def draw(self, ctx, t, d):
        reactor_scene(ctx, t, d)


class Slbm(Cued):
    def beats(self, d):
        c = self.cue
        return {"missiles": c("MISSILES", 1.0), "dabav": c("DABAV", 2.3), "aasmaan": c("AASMAAN", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["missiles"], "whoosh"), (b["dabav"], "beep"), (b["aasmaan"], "boom")]

    def draw(self, ctx, t, d):
        slbm_scene(ctx, t, d)


class Stealth(Cued):
    def beats(self, d):
        c = self.cue
        return {"kaali": c("KAALI", 1.0), "varsha": c("VARSHA", 2.2), "pahaad": c("PAHAAD", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["kaali"], "beep"), (b["varsha"], "whoosh"), (b["pahaad"], "thud")]

    def draw(self, ctx, t, d):
        stealth_scene(ctx, t, d)


class Poll(Cued):
    def beats(self, d):
        c = self.cue
        return {"taaqatwar": c("TAAQATWAR", 1.2), "bataiye": c("BATAIYE", 2.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["taaqatwar"], "whoosh"), (b["bataiye"], "pop")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        poll_scene(ctx, t, d)

        # Interactive Ending Poll Card
        lego.ending(
            STORY, ctx, t, t - b["taaqatwar"], t - b["bataiye"],
            question=("KYA ARIHANT BHARAT KA", "SABSE BADA RAKSHAK HAI?"),
            tag="REALITY SHIFT"
        )


SCENE_CLASSES = {
    "hook": Hook,
    "triad": Triad,
    "reactor": Reactor,
    "slbm": Slbm,
    "stealth": Stealth,
    "poll": Poll,
}
STORY = sys.modules[__name__]


# ============================================================ UPLOAD KIT

UPLOAD = {
    "titles": [
        "INS Arihant: Deep Sea Nuclear Deterrence & India's 2nd Strike Explained",
        "INS Arihant: Deep Sea Nuclear Submarine India Secret Patrol Explained",
        "Samandar Ke 300 Metre Neeche: Kaise INS Arihant Ne Banaya Bharat Ko Ajeya?",
        "INS Arihant: Bharat Ka Silent Nuclear Guardian Kaise Kaam Karta Hai?",
        "Deep Sea Deterrence: Dushman Ke Sare Base Khatam Hone Par Bhi Bharat Ka Palatwar!",
        "K-4 SLBM & 83 MW Reactor: INS Arihant Ki Asli Taqat Dekh Kar Dushman Dang",
    ],
    "title": "INS Arihant: Deep Sea Nuclear Deterrence & India's 2nd Strike Explained",
    "thumb_text": "INS ARIHANT",
    "queries": ["ins arihant", "nuclear submarine india", "deep sea deterrence"],
    "description": """INS Arihant: Deep Sea Nuclear Deterrence Patrol & 2nd Strike Explained.
INS Arihant is India's first nuclear submarine India developed for deep sea deterrence.
Kyu INS Arihant ko Bharat ka sabse bada deep sea deterrence aur 'Brahma-astra' mana jata hai?

Is video me janiye:
• Samandar ke 300 metre neeche INS Arihant ka silent nuclear deterrence patrol
• Bharat ka Nuclear Triad (Land, Air, Sea) aur No First Use ke tehat Second Strike capability
• BARC dwara viksit 83 MW light-water reactor jisse milti hai mahinon tak unlimited submersion
• Underwater VLS launch se chhutne wali K-15 aur K-4 ballistic missiles
• Anechoic rubber tiles stealth aur Project Varsha ka abhedya underground mountain base

Bharat ke is aitihasik raksha kavach par aapki kya rai hai? Comment me likhiye!
Defence aur geopolitics explainers ke liye Reality Shift channel ko subscribe kijiye.

#Shorts #INSArihant #IndianNavy
""",
    "tags": ["ins arihant", "nuclear submarine", "indian navy", "ssbn 73", "second strike capability",
             "k4 missile", "barc reactor", "project varsha", "reality shift", "defence explainer"],
    "hashtags": ["#Shorts", "#INSArihant", "#IndianNavy"],
}


def thumbnail(ctx):
    """1080x1920 cover: INS Arihant in Deep Midnight Ocean with Glowing Cherenkov Blue & Commander."""
    ocean_bg(ctx, 0.5, depth_level="deep")

    # Center Submarine cruising in midnight blue
    ins_arihant_sub(ctx, 540, 840, 1.45, 0.5)

    # Submerged K-4 Missile Launch erupting behind
    glow(ctx, 740, 520, 140, RED, 0.8)
    line(ctx, [(740, 680), (740, 480)], BOOSTER_FIRE, 12)

    # Naval Commander in Foreground
    naval_commander(ctx, 280, 1380, 0.88, 0.5, pose="binoculars")

    # Dark gradient overlays for crisp text readability
    g = cairo.LinearGradient(0, 1240, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.94)
    ctx.rectangle(0, 1240, W, H - 1240)
    ctx.set_source(g)
    ctx.fill()

    g = cairo.LinearGradient(0, 0, 0, 780)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.94)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 780)
    ctx.set_source(g)
    ctx.fill()

    vignette(ctx)
    text(ctx, "INS ARIHANT", 540, 280, 140, NAVY_GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=24)
    text(ctx, "PATAAL KA BHEDIYA!", 540, 440, 105, CHERENKOV_BLUE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    tag(ctx, "NUCLEAR PATROL // SECOND STRIKE", 540, 590, SONAR_GREEN, 1.0)
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
    story = importlib.import_module("shorts.arihant")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
