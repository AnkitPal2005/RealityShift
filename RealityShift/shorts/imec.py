"""Reality Shift Short - "IMEC Corridor vs Suez Canal: Red Sea Crisis Ka Desi Tod" (~45-50s).

Usage:
  python make.py imec --kiki-export     # exports text for KikiVoice
  python make.py imec --check           # policy check
  python make.py imec --engine edge     # preview render with edge-tts
  python make.py imec                   # final render from KikiVoice files

Strategic overview:
India-Middle East-Europe Economic Corridor (IMEC) vs Suez Canal.
Suez Canal handles 12% of world trade, but the Red Sea crisis & Houthis forced ships
into a 10,000 km detour around Africa. IMEC connects India to Europe via ship,
high-speed freight rail across UAE & Saudi Arabia, and Mediterranean sea routes,
cutting transit time by 40% and costs by 30% while checkmating China's BRI.
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

TOPIC = "IMEC VS SUEZ CANAL"
OUTPUTS = {"edge": "imec_short.mp4"}
LEGO = {"header": "radar", "caption": "chip", "transition": "scan", "palette": "intel", "ending": "prompt"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.55
TAIL_PAD = 0.20
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 114
MUSIC_STYLE = "pulse"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 500

PAL = lego.PALETTES["intel"]
UI = PAL["ui"]
HI = PAL["hi"]
RED = PAL["alert"]
INK = PAL["ink"]
SAFFRON = hexc("#FF9933")
GREEN = hexc("#3DDC84")
STEEL = hexc("#90A4AE")
DARK_STEEL = hexc("#1A2530")
OCEAN_BLUE = hexc("#0A1C2A")
CYAN_ROUTE = hexc("#00E5FF")
GOLD_RAIL = hexc("#FFD54F")
DESERT_SAND = hexc("#C29B38")
EGYPT_SAND = hexc("#8D6E63")

SOURCES = [
    "G20 New Delhi Summit 2023: Memorandum of Understanding on India-Middle East-Europe Economic Corridor (IMEC) "
    "signed by India, USA, UAE, Saudi Arabia, France, Germany, Italy, and EU (Ministry of External Affairs, PIB).",
    "Suez Canal Authority (SCA) & UNCTAD Trade and Development Report 2024: Impact of Red Sea shipping crisis, "
    "Bab-el-Mandeb disruptions, and 42% decline in Suez Canal transits.",
    "IMF PortWatch & World Shipping Council: Maritime route distance analysis (Mumbai-Europe via Suez: ~7,200 nm, "
    "via Cape of Good Hope: ~11,800 nm, IMEC multimodal corridor 40% transit time reduction).",
]

SPEC = [
    {"key": "hook", "accent": RED, "text": "SUEZ CANAL // $10B/DAY TRAP",
     "visual": "Giant 400m container ship wedged diagonally across narrow Suez Canal; red blinking alert circles; $10B daily trade choked",
     "vo": [("hook", [("एक जहाज़ स्वेज नहर में फंसा,", "EK JAHAZ SUEZ MEIN FANSA,"),
                      ("और पूरी दुनिया का दस अरब डॉलर का व्यापार", "AUR DUNIYA KA 10 BILLION DOLLAR VYAPAR"),
                      ("एक झटके में ठप हो गया!", "EK JHATKE MEIN THAP HO GAYA!"),
                      ("लेकिन अब भारत ने ऐसा चक्रव्यूह रचा,", "LEKIN BHARAT NE AISA CHAKRAVYUH RACHA,"),
                      ("जिसने स्वेज नहर की हवा निकाल दी।", "JISNE SUEZ NAHAR KI HAWA NIKAL DI.")])]},

    {"key": "red_sea", "accent": RED, "text": "RED SEA // 10,000 KM DETOUR",
     "visual": "Red Sea and Bab-el-Mandeb highlighted red with missile strikes; massive detour arc around Africa's Cape of Good Hope (+14 DAYS)",
     "vo": [("tell", [("लाल सागर में हूती मिसाइलों के डर से", "LAL SAGAR MEIN HOUTHI MISSILES SE"),
                      ("आज जहाजों को पूरे अफ्रीका का चक्कर काटकर", "JAHAZON KO PURE AFRICA KA CHAKKAR KAATKAR"),
                      ("दस हज़ार किलोमीटर घूमना पड़ रहा है।", "10,000 KM GHOOMNA PAD RAHA HAI."),
                      ("चौदह दिन की देरी", "14 DIN KI DERI"),
                      ("और लाखों डॉलर का खर्चा!", "AUR LAKHON DOLLAR KA KHARCHA!")])]},

    {"key": "imec", "accent": GREEN, "text": "IMEC // THE MULTIMODAL ROUTE",
     "visual": "G20 IMEC route lights up: Sea line from India (Mundra/JNPT) to UAE; glowing railway track through Saudi & Jordan to Haifa; sea route to Europe",
     "vo": [("tell", [("तभी एंट्री होती है आई-मेक की—", "TABHI ENTRY HOTI HAI IMEC KI—"),
                      ("इंडिया-मिडिल ईस्ट-यूरोप कॉरिडोर!", "INDIA-MIDDLE EAST-EUROPE CORRIDOR!"),
                      ("समंदर, हाई-स्पीड रेल और फिर समंदर—", "SAMANDAR, HIGH-SPEED RAIL, SAMANDAR—"),
                      ("भारत से यूएई, सऊदी, जॉर्डन,", "BHARAT SE UAE, SAUDI, JORDAN,"),
                      ("इज़राइल होते हुए सीधा यूरोप!", "ISRAEL HOTE HUYE SEEDHA EUROPE!")])]},

    {"key": "speed", "accent": HI, "text": "40% FASTER // 30% CHEAPER",
     "visual": "Split HUD telemetry: Suez Canal (35 Days, High Risk) vs IMEC Corridor (20 Days, Zero Risk, -30% Logistics Cost)",
     "vo": [("tell", [("स्वेज नहर से यूरोप पहुंचने में", "SUEZ SE EUROPE PAHUNCHNE MEIN"),
                      ("पैंतीस दिन लगते हैं,", "35 DIN LAGTE HAIN,"),
                      ("लेकिन आई-मेक से सिर्फ बीस दिन!", "LEKIN IMEC SE SIRF 20 DIN!"),
                      ("यानी पूरे चालीस प्रतिशत समय की बचत", "PURI 40% SAMAY KI BACHAT"),
                      ("और तीस प्रतिशत सस्ता किराया!", "AUR 30% SASTA KIRAYA!")])]},

    {"key": "strategy", "accent": SAFFRON, "text": "CHINA BRI DEBT-TRAP CHECKMATE",
     "visual": "China's BRI debt-trap corridor cracking under red warning; IMEC corridor beaming green clean hydrogen pipeline and high-speed undersea digital data cables; India standing tall as global hub",
     "vo": [("tell", [("ये सिर्फ व्यापार नहीं,", "YE SIRF VYAPAR NAHI,"),
                      ("बल्कि चीन के बीआरआई डेट-ट्रैप को", "BALKI CHINA KE BRI DEBT-TRAP KO"),
                      ("भारत का सीधा जवाब है।", "BHARAT KA SEEDHA JAWAB HAI."),
                      ("इसके साथ ही बिछेंगी क्लीन हाइड्रोजन पाइपलाइन्स", "CLEAN HYDROGEN PIPELINES"),
                      ("और हाई-स्पीड डेटा केबल्स!", "AUR HIGH-SPEED DATA CABLES!")])]},

    {"key": "ask", "accent": HI, "text": "SUEZ KA ANTIM SAMAY?",
     "visual": "Tactical prompt card: 'KYA IMEC SUEZ KO KHATAM KAREGA?'; India tricolor emblem; animated cursor clicking on YouTube Shorts comment section",
     "vo": [("ask", [("क्या आई-मेक स्वेज नहर के", "KYA IMEC SUEZ NAHAR KE"),
                     ("डेढ़ सौ साल पुराने दबदबे को खत्म करेगा?", "150 SAAL PURANE DABDABE KO KHATAM KAREGA?"),
                     ("अपनी राय कमेंट में बताइए,", "APNI RAI COMMENT MEIN BATAIYE,"),
                     ("और ऐसे ही खुलासों के लिए सब्सक्राइब करें रियलिटी शिफ्ट!", "AISE HI KHULASON KE LIYE SUBSCRIBE REALITY SHIFT!")])]},
]

DELIVERY = delivery.build(SPEC)
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "SUEZ": RED, "FANSA,": RED, "10": RED, "BILLION": RED, "DOLLAR": RED, "VYAPAR": RED,
    "THAP": RED, "CHAKRAVYUH": SAFFRON, "HAWA": HI, "NIKAL": HI, "LAL": RED, "SAGAR": RED,
    "HOUTHI": RED, "MISSILES": RED, "AFRICA": HI, "10,000": RED, "KM": RED, "14": RED,
    "DIN": RED, "IMEC": GREEN, "CORRIDOR!": GREEN, "SAMANDAR,": UI, "HIGH-SPEED": HI,
    "RAIL,": GOLD_RAIL, "BHARAT": SAFFRON, "UAE,": UI, "SAUDI,": UI, "JORDAN,": UI,
    "ISRAEL": UI, "EUROPE!": GREEN, "35": RED, "20": GREEN, "40%": GREEN, "BACHAT": GREEN,
    "30%": GREEN, "KAM": GREEN, "TRANSPORT": UI, "CHINA": RED, "BRI": RED, "DEBT-TRAP": RED,
    "HYDROGEN": GREEN, "PIPELINES": GREEN, "DATA": UI, "CABLES!": UI, "150": HI,
    "DABDABE": RED, "COMMENT": HI, "REALITY": UI, "SHIFT!": UI, "DEFENCE": SAFFRON
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
    rgba(ctx, (0.01, 0.02, 0.035) if not alert else (0.03, 0.015, 0.018))
    ctx.fill()

    for x in range(0, W + 1, 90):
        line(ctx, [(x, 0), (x, H)], UI if not alert else RED, 1, 0.07)
    for y in range(0, H + 1, 90):
        line(ctx, [(0, y), (W, y)], UI if not alert else RED, 1, 0.07)


def container_box(ctx, x, y, w, h, col):
    """Single cargo container with corrugated lines."""
    rrect(ctx, x, y, w, h, 2)
    rgba(ctx, col)
    ctx.fill()
    rrect(ctx, x, y, w, h, 2)
    rgba(ctx, (0, 0, 0), 0.4)
    ctx.set_line_width(1.5)
    ctx.stroke()
    # corrugations
    step = 6
    for cx in range(int(x + 4), int(x + w - 3), step):
        line(ctx, [(cx, y + 2), (cx, y + h - 2)], (0, 0, 0), 1, 0.35)


def container_ship(ctx, x, y, s, t, blocked=False, a=1.0):
    """Detailed container cargo vessel with colorful stacks and bridge tower."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # Water shadow
    ell(ctx, 0, 40, 240, 45)
    rgba(ctx, (0, 0, 0), 0.6 * a)
    ctx.fill()

    # Ship Hull
    hull_pts = [(-220, 10), (160, 10), (220, -10), (200, 35), (-190, 35)]
    smooth(ctx, hull_pts, closed=True, k=0.08)
    rgba(ctx, hexc("#B71C1C") if not blocked else hexc("#C62828"), a)
    ctx.fill()
    hull_top = [(-220, 10), (160, 10), (220, -10), (210, -15), (-215, -15)]
    smooth(ctx, hull_top, closed=True, k=0.08)
    rgba(ctx, hexc("#212121"), a)
    ctx.fill()

    # Deck base line
    line(ctx, [(-215, -15), (210, -15)], hexc("#424242"), 4, a)

    # Container Stacks (4 bays, multiple tiers)
    cols = [hexc("#1565C0"), hexc("#2E7D32"), hexc("#F57F17"), hexc("#C62828"), hexc("#455A64"), hexc("#00838F")]
    cw, ch = 34, 18
    for bay in range(6):
        bx = -180 + bay * 42
        for tier in range(4):
            by = -33 - tier * 20
            col = cols[(bay * 3 + tier) % len(cols)]
            container_box(ctx, bx, by, cw, ch, col)

    # Bridge Tower (Superstructure)
    rrect(ctx, 80, -125, 42, 110, 3)
    rgba(ctx, (1, 1, 1), a)
    ctx.fill()
    # Bridge windows
    rrect(ctx, 84, -118, 34, 10, 2)
    rgba(ctx, hexc("#1A237E"), a)
    ctx.fill()
    # Radar Mast & Funnel
    line(ctx, [(101, -125), (101, -150)], STEEL, 3, a)
    circle(ctx, 101, -150, 4, HI)
    # Funnel
    rrect(ctx, 65, -95, 12, 45, 2)
    rgba(ctx, hexc("#B71C1C"), a)
    ctx.fill()

    # Bow wake or warning
    if blocked:
        # Emergency Red Warning beacon
        glow(ctx, 0, -60, 180, RED, 0.4 + 0.3 * math.sin(t * 8))
        text(ctx, "EVER GIVEN // BLOCKED", 0, -165, 30, RED, font=lego.MONO)
    else:
        # Water ripples
        for rw in range(3):
            line(ctx, [(190 + rw * 30, 25 + rw * 6), (230 + rw * 35, 30 + rw * 8)], CYAN_ROUTE, 2, 0.4 - rw * 0.1)

    ctx.restore()


def suez_canal_blocked_scene(ctx, t, d):
    """Scene 1: Narrow canal banks, ship grounded sideways, warning icons, traffic jam."""
    grid_bg(ctx, t, alert=True)

    # Canal sandy banks
    # Top bank (Sinai)
    rrect(ctx, 0, 0, W, 480, 0)
    rgba(ctx, hexc("#1C1608"))
    ctx.fill()
    line(ctx, [(0, 480), (W, 480)], DESERT_SAND, 5, 0.8)
    tag(ctx, "SINAI PENINSULA (EGYPT)", 540, 430, DESERT_SAND, 1.0, size=26)

    # Bottom bank
    rrect(ctx, 0, 960, W, H - 960, 0)
    rgba(ctx, hexc("#1C1608"))
    ctx.fill()
    line(ctx, [(0, 960), (W, 960)], DESERT_SAND, 5, 0.8)
    tag(ctx, "SUEZ CANAL (WIDTH: 205 METERS)", 540, 1010, UI, 1.0, size=26)

    # Canal water channel
    rrect(ctx, 0, 480, W, 480, 0)
    rgba(ctx, hexc("#0A2233"))
    ctx.fill()

    # Sand spit where Ever Given bow got stuck
    sand_spit = [(720, 480), (880, 560), (840, 480)]
    smooth(ctx, sand_spit, closed=True)
    rgba(ctx, hexc("#8D6E63"))
    ctx.fill()

    # Container Ship Wedged diagonally across canal!
    ctx.save()
    ctx.translate(520, 720)
    rot = -math.radians(32 + 2 * math.sin(t * 2))
    ctx.rotate(rot)
    container_ship(ctx, 0, 0, 1.25, t, blocked=True)
    ctx.restore()

    # Blockade Stamp & Lost Trade Telemetry
    stamp(ctx, 540, 310, t, -0.06, 520, 100, RED, [("SUEZ CHOKED", 8, 48, RED)])
    tag(ctx, "$10 BILLION / DAY TRADE BLOCKED", 540, 1100, RED, 1.0, size=32)

    # Queue of blocked ships behind in Red Sea
    for i in range(4):
        bx = 140 + i * 160
        by = 890 - i * 40
        container_ship(ctx, bx, by, 0.32, t)


def red_sea_crisis_scene(ctx, t, d):
    """Scene 2: Map of Red Sea, Houthi missile attack zone, Cape of Good Hope detour arc."""
    grid_bg(ctx, t, alert=True)

    # Continent outlines (Africa left, Arabian peninsula right)
    africa = [
        (0, 300), (280, 340), (320, 520), (260, 750), (290, 940),
        (220, 1180), (140, 1340), (0, 1340)
    ]
    smooth(ctx, africa, closed=True, k=0.15)
    rgba(ctx, hexc("#131B22"))
    ctx.fill()
    line(ctx, [(0, 300), (280, 340), (320, 520), (260, 750), (290, 940), (220, 1180), (140, 1340)], STEEL, 2, 0.4)
    text(ctx, "AFRICA", 120, 600, 36, STEEL, font=lego.MONO, a=0.6)

    # Arabian Peninsula / Middle East
    arabia = [
        (460, 240), (840, 260), (960, 440), (860, 720), (620, 760),
        (480, 660), (440, 480)
    ]
    smooth(ctx, arabia, closed=True, k=0.15)
    rgba(ctx, hexc("#1A2328"))
    ctx.fill()
    line(ctx, [(460, 240), (840, 260), (960, 440), (860, 720), (620, 760), (480, 660), (440, 480)], STEEL, 2, 0.4)
    text(ctx, "ARABIAN PENINSULA", 680, 480, 30, STEEL, font=lego.MONO, a=0.6)

    # Red Sea corridor (between Africa and Arabia)
    # Danger zone around Bab-el-Mandeb
    bx, by = 470, 710
    danger_pulse = 0.5 + 0.5 * math.sin(t * 8)
    glow(ctx, bx, by, 160, RED, 0.5 * danger_pulse)
    circle(ctx, bx, by, 28, RED, 0.8)
    circle(ctx, bx, by, 48, RED, 0.4)
    line(ctx, [(bx - 60, by), (bx + 60, by)], RED, 2)
    line(ctx, [(bx, by - 60), (bx, by + 60)], RED, 2)
    text(ctx, "MISSILE ATTACK ZONE", bx + 160, by - 10, 24, RED, font=lego.MONO, anchor="l")
    text(ctx, "BAB-EL-MANDEB STRAIT", bx + 160, by + 18, 20, HI, font=lego.MONO, anchor="l")

    # Cape of Good Hope Detour Arrow (Huge red arc looping around Africa)
    detour_pts = [
        (460, 340), (280, 480), (200, 760), (160, 1080),
        (180, 1260), (320, 1340), (460, 1300), (580, 1120)
    ]
    smooth(ctx, detour_pts, closed=False, k=0.2)
    rgba(ctx, RED, 0.85)
    ctx.set_line_width(6)
    ctx.set_dash([14, 8])
    ctx.stroke()
    ctx.set_dash([])

    # Telemetry HUD Card
    rrect(ctx, 160, 890, 760, 180, 12)
    rgba(ctx, (0.04, 0.05, 0.08), 0.92)
    ctx.fill()
    rrect(ctx, 160, 890, 760, 180, 12)
    rgba(ctx, RED, 0.7)
    ctx.set_line_width(2)
    ctx.stroke()

    text(ctx, "CAPE OF GOOD HOPE DETOUR", 540, 935, 34, RED, font=CAPTION_FONT)
    text(ctx, "+10,000 KM DISTANCE  //  +14 DAYS TRANSIT", 540, 985, 26, HI, font=lego.MONO)
    text(ctx, "INSURANCE COST: +300%  //  FUEL: +$1,000,000", 540, 1030, 24, STEEL, font=lego.MONO)

    tag(ctx, "RED SEA CRISIS: MARITIME CHOKEPOINT", 540, 280, RED, 1.0)


def draw_rail_track(ctx, pts, col=GOLD_RAIL):
    """Draws railway track with sleepers and rails."""
    # Rail lines
    ctx.set_line_width(4)
    rgba(ctx, col, 0.9)
    smooth(ctx, pts, closed=False, k=0.1)
    ctx.stroke()

    # Sleepers (ties)
    ctx.set_line_width(8)
    ctx.set_dash([4, 12])
    rgba(ctx, col, 0.6)
    smooth(ctx, pts, closed=False, k=0.1)
    ctx.stroke()
    ctx.set_dash([])


def freight_train(ctx, x, y, s, t):
    """Futuristic high-speed double-stack freight train."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # Train Body (Engine)
    rrect(ctx, 40, -40, 90, 36, 4)
    rgba(ctx, hexc("#0D47A1"))
    ctx.fill()
    # Aerodynamic nose
    nose = [(130, -40), (165, -15), (130, -4)]
    smooth(ctx, nose, closed=True)
    rgba(ctx, hexc("#1976D2"))
    ctx.fill()
    # Windshield
    rrect(ctx, 115, -34, 25, 14, 2)
    rgba(ctx, CYAN_ROUTE)
    ctx.fill()

    # Container Wagons (Double-stacked containers)
    for w in range(3):
        wx = -170 + w * 68
        # Chassis
        rrect(ctx, wx, -8, 62, 8, 2)
        rgba(ctx, hexc("#212121"))
        ctx.fill()
        # Wheels
        circle(ctx, wx + 12, 3, 6, STEEL)
        circle(ctx, wx + 50, 3, 6, STEEL)
        # Bottom Container
        container_box(ctx, wx + 2, -28, 58, 18, hexc("#1565C0") if w % 2 == 0 else hexc("#C62828"))
        # Top Container
        container_box(ctx, wx + 2, -48, 58, 18, hexc("#F57F17") if w % 2 == 0 else hexc("#2E7D32"))

    # Headlight Beam
    glow(ctx, 175, -15, 60, HI, 0.8)

    ctx.restore()


def imec_route_scene(ctx, t, d):
    """Scene 3: Complete IMEC corridor lighting up across India, UAE, Saudi, Israel, Europe."""
    grid_bg(ctx, t)

    # Tactical Map Hubs
    hubs = {
        "INDIA": (820, 840, "MUNDRA / JNPT", SAFFRON),
        "UAE": (590, 720, "FUJAIRAH / JEBEL ALI", UI),
        "SAUDI": (440, 640, "RIYADH / AL HADITHA", GOLD_RAIL),
        "ISRAEL": (330, 520, "HAIFA PORT", CYAN_ROUTE),
        "EUROPE": (180, 380, "PIRAEUS / MARSEILLE", GREEN),
    }

    # Sea Route 1: India to UAE (Cyan dotted line with moving ship)
    line(ctx, [(820, 840), (590, 720)], CYAN_ROUTE, 4, 0.8)
    ctx.set_dash([10, 6])
    line(ctx, [(820, 840), (590, 720)], (1, 1, 1), 2, 0.6)
    ctx.set_dash([])
    text(ctx, "EASTERN MARITIME ROUTE", 730, 790, 20, CYAN_ROUTE, font=lego.MONO)

    # Rail Route: UAE -> Saudi Arabia -> Jordan -> Haifa (Gold Rail Track with moving train)
    rail_pts = [(590, 720), (480, 660), (410, 610), (330, 520)]
    draw_rail_track(ctx, rail_pts, GOLD_RAIL)
    text(ctx, "NORTHERN FREIGHT RAILWAY", 450, 570, 20, GOLD_RAIL, font=lego.MONO)

    # Sea Route 2: Haifa to Europe (Cyan dotted line with ship)
    line(ctx, [(330, 520), (180, 380)], CYAN_ROUTE, 4, 0.8)
    ctx.set_dash([10, 6])
    line(ctx, [(330, 520), (180, 380)], (1, 1, 1), 2, 0.6)
    ctx.set_dash([])
    text(ctx, "MEDITERRANEAN ROUTE", 230, 460, 20, CYAN_ROUTE, font=lego.MONO)

    # Draw Hub Nodes
    for name, (hx, hy, label, col) in hubs.items():
        glow(ctx, hx, hy, 45, col, 0.6)
        circle(ctx, hx, hy, 16, col)
        circle(ctx, hx, hy, 6, (1, 1, 1))
        rrect(ctx, hx - 90, hy + 24, 180, 42, 6)
        rgba(ctx, (0.02, 0.04, 0.07), 0.9)
        ctx.fill()
        rrect(ctx, hx - 90, hy + 24, 180, 42, 6)
        rgba(ctx, col, 0.6)
        ctx.set_line_width(1.5)
        ctx.stroke()
        text(ctx, name, hx, hy + 42, 20, col, font=CAPTION_FONT)
        text(ctx, label, hx, hy + 58, 14, STEEL, font=lego.MONO)

    # Moving cargo vessel on Arabian Sea
    prog_sea1 = (t * 0.25) % 1.0
    sx1 = 820 + (590 - 820) * prog_sea1
    sy1 = 840 + (720 - 840) * prog_sea1
    container_ship(ctx, sx1, sy1, 0.35, t)

    # Moving train on desert rail
    prog_rail = ((t * 0.3) + 0.3) % 1.0
    rx = 590 + (330 - 590) * prog_rail
    ry = 720 + (520 - 720) * prog_rail
    freight_train(ctx, rx, ry, 0.42, t)

    tag(ctx, "IMEC: MULTIMODAL MARITIME + RAILWAY", 540, 280, GREEN, 1.0)


def speed_economics_scene(ctx, t, d):
    """Scene 4: Split HUD comparing Suez Canal vs IMEC Corridor."""
    grid_bg(ctx, t)

    # Center divider
    line(ctx, [(540, 360), (540, 1120)], STEEL, 2, 0.3)

    # LEFT CARD: SUEZ CANAL
    rrect(ctx, 60, 380, 440, 680, 12)
    rgba(ctx, (0.05, 0.02, 0.02), 0.9)
    ctx.fill()
    rrect(ctx, 60, 380, 440, 680, 12)
    rgba(ctx, RED, 0.8)
    ctx.set_line_width(2.5)
    ctx.stroke()

    tag(ctx, "SUEZ CANAL ROUTE", 280, 430, RED, 1.0, size=28)
    container_ship(ctx, 280, 560, 0.6, t, blocked=True)

    text(ctx, "TRANSIT TIME", 280, 660, 22, STEEL, font=lego.MONO)
    text(ctx, "35 - 40 DAYS", 280, 710, 48, RED, font=CAPTION_FONT)

    line(ctx, [(100, 750), (460, 750)], STEEL, 1, 0.2)

    text(ctx, "SECURITY STATUS", 280, 790, 22, STEEL, font=lego.MONO)
    text(ctx, "HIGH RISK // HOUTHIS", 280, 830, 28, RED, font=CAPTION_FONT)

    text(ctx, "LOGISTICS EXPENSE", 280, 890, 22, STEEL, font=lego.MONO)
    text(ctx, "+$1M FUEL PER TRIP", 280, 930, 26, HI, font=lego.MONO)
    text(ctx, "+200% WAR INSURANCE", 280, 970, 24, RED, font=lego.MONO)

    # RIGHT CARD: IMEC CORRIDOR
    rrect(ctx, 580, 380, 440, 680, 12)
    rgba(ctx, (0.01, 0.05, 0.03), 0.9)
    ctx.fill()
    rrect(ctx, 580, 380, 440, 680, 12)
    rgba(ctx, GREEN, 0.9)
    ctx.set_line_width(2.5)
    ctx.stroke()

    tag(ctx, "IMEC CORRIDOR", 800, 430, GREEN, 1.0, size=28)
    freight_train(ctx, 800, 560, 0.68, t)

    text(ctx, "TRANSIT TIME", 800, 660, 22, STEEL, font=lego.MONO)
    text(ctx, "20 DAYS (-40%)", 800, 710, 48, GREEN, font=CAPTION_FONT)

    line(ctx, [(620, 750), (980, 750)], STEEL, 1, 0.2)

    text(ctx, "SECURITY STATUS", 800, 790, 22, STEEL, font=lego.MONO)
    text(ctx, "ZERO MISSILE THREAT", 800, 830, 28, CYAN_ROUTE, font=CAPTION_FONT)

    text(ctx, "LOGISTICS EXPENSE", 800, 890, 22, STEEL, font=lego.MONO)
    text(ctx, "30% CHEAPER TRANSPORT", 800, 930, 26, GREEN, font=lego.MONO)
    text(ctx, "RELIABLE RAIL GRID", 800, 970, 24, HI, font=lego.MONO)

    tag(ctx, "40% FASTER // 30% CHEAPER", 540, 280, HI, 1.0)


def strategy_scene(ctx, t, d):
    """Scene 5: Strategic checkmate - China BRI debt-trap vs IMEC Green & Digital Corridor."""
    grid_bg(ctx, t)

    # Center Shield with India Tricolor
    flag(ctx, 540 - 80, 400, 160, 100, "in", t)

    # Left: China BRI Debt Trap (Cracking)
    rrect(ctx, 60, 580, 440, 480, 12)
    rgba(ctx, (0.05, 0.02, 0.02), 0.92)
    ctx.fill()
    rrect(ctx, 60, 580, 440, 480, 12)
    rgba(ctx, RED, 0.7)
    ctx.set_line_width(2)
    ctx.stroke()

    tag(ctx, "CHINA BRI (DEBT-TRAP)", 280, 630, RED, 1.0, size=26)
    text(ctx, "UNSUSTAINABLE LOANS", 280, 700, 26, STEEL, font=lego.MONO)
    text(ctx, "DEFAULT CRISIS (SRI LANKA)", 280, 750, 24, RED, font=lego.MONO)
    text(ctx, "HIGH DELAYS & BOTTLENECK", 280, 800, 24, STEEL, font=lego.MONO)
    stamp(ctx, 280, 920, t, -0.08, 320, 80, RED, [("CRACKING", 6, 36, RED)])

    # Right: IMEC Clean Hydrogen & High-Speed Data Grid
    rrect(ctx, 580, 580, 440, 480, 12)
    rgba(ctx, (0.01, 0.04, 0.05), 0.92)
    ctx.fill()
    rrect(ctx, 580, 580, 440, 480, 12)
    rgba(ctx, CYAN_ROUTE, 0.8)
    ctx.set_line_width(2)
    ctx.stroke()

    tag(ctx, "IMEC: CLEAN ENERGY & DATA", 800, 630, GREEN, 1.0, size=26)
    text(ctx, "GREEN HYDROGEN PIPELINES", 800, 700, 24, GREEN, font=lego.MONO)
    text(ctx, "UNDERSEA DIGITAL CABLES", 800, 750, 24, CYAN_ROUTE, font=lego.MONO)
    text(ctx, "DIRECT TRADE TO EUROPE", 800, 800, 24, HI, font=lego.MONO)
    stamp(ctx, 800, 920, t, 0.06, 340, 80, GREEN, [("FUTURE-READY", 6, 36, GREEN)])

    tag(ctx, "STRATEGIC CHECKMATE: INDIA AS GLOBAL ANCHOR", 540, 280, SAFFRON, 1.0)


# ============================================================ SCENE CLASSES

class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"fansa": c("FANSA", 0.9), "billion": c("BILLION", 2.2), "hawa": c("HAWA", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["fansa"], "whoosh"), (b["billion"], "boom"), (b["hawa"], "thud")]

    def draw(self, ctx, t, d):
        suez_canal_blocked_scene(ctx, t, d)


class RedSea(Cued):
    def beats(self, d):
        c = self.cue
        return {"houthi": c("HOUTHI", 1.0), "km": c("10,000", 2.4), "kharcha": c("KHARCHA", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["houthi"], "beep"), (b["km"], "whoosh"), (b["kharcha"], "boom")]

    def draw(self, ctx, t, d):
        red_sea_crisis_scene(ctx, t, d)


class Imec(Cued):
    def beats(self, d):
        c = self.cue
        return {"entry": c("ENTRY", 0.9), "corridor": c("CORRIDOR", 2.2), "europe": c("EUROPE", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["entry"], "whoosh"), (b["corridor"], "beep"), (b["europe"], "beep")]

    def draw(self, ctx, t, d):
        imec_route_scene(ctx, t, d)


class Speed(Cued):
    def beats(self, d):
        c = self.cue
        return {"35": c("35", 1.0), "20": c("20", 2.4), "cheaper": c("30%", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["35"], "whoosh"), (b["20"], "beep"), (b["cheaper"], "boom")]

    def draw(self, ctx, t, d):
        speed_economics_scene(ctx, t, d)


class Strategy(Cued):
    def beats(self, d):
        c = self.cue
        return {"bri": c("BRI", 1.2), "jawab": c("JAWAB", 2.4), "cables": c("CABLES", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["bri"], "whoosh"), (b["jawab"], "beep"), (b["cables"], "boom")]

    def draw(self, ctx, t, d):
        strategy_scene(ctx, t, d)


class Ask(Cued):
    def beats(self, d):
        c = self.cue
        return {"dabdabe": c("DABDABE", 1.2), "cmt": c("COMMENT", 2.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["dabdabe"], "whoosh"), (b["cmt"], "pop")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        grid_bg(ctx, t)

        # Flag fluttering
        flag(ctx, 80, 420, 160, 100, "in", t)

        # Container ship and train meeting
        container_ship(ctx, 280, 1100, 0.55, t)
        freight_train(ctx, 760, 1100, 0.58, t)

        # Interactive Ending Prompt
        lego.ending(
            STORY, ctx, t, t - b["dabdabe"], t - b["cmt"],
            question=("KYA IMEC SUEZ KO", "KHATAM KAR DEGA?"),
            tag="REALITY SHIFT"
        )


SCENE_CLASSES = {
    "hook": Hook,
    "red_sea": RedSea,
    "imec": Imec,
    "speed": Speed,
    "strategy": Strategy,
    "ask": Ask,
}
STORY = sys.modules[__name__]


# ============================================================ UPLOAD KIT

UPLOAD = {
    "titles": [
        "IMEC Corridor vs Suez Canal: Red Sea Crisis Ka Desi Tod",
        "Suez Canal vs IMEC: 40% Faster Route Jisne Duniyan Ko Hila Diya",
        "Red Sea Crisis: Kaise Bharat Ka IMEC Banega Duniyan Ka Naya Route?",
        "IMEC vs Suez Canal: Duniyan Ke Sabse Bade Trade Chokepoint Ka Ant?",
        "India To Europe in 20 Days: IMEC Corridor Ka Geopolitical Masterstroke",
    ],
    "title": "IMEC Corridor vs Suez Canal: Red Sea Crisis Ka Desi Tod",
    "thumb_text": "IMEC VS SUEZ",
    "queries": ["imec corridor", "suez canal", "red sea crisis"],
    "description": """IMEC Corridor vs Suez Canal: Red Sea Crisis Ka Desi Tod:
IMEC Corridor vs Suez Canal: Red Sea crisis me Bharat ka masterstroke.
Kyu Suez Canal ke badle IMEC trade route banega duniya ka bhavishya?

Is video me janiye:
• Suez Canal me Ever Given jaise ship blockages aur $10B daily loss
• Red Sea me Houthi missiles ke karan 10,000 KM Africa detour
• IMEC (India-Middle East-Europe Corridor) ka multimodal ship-rail-ship network
• 40% faster transit time (35 din ke badle sirf 20 din) aur 30% sasta freight
• China ke BRI debt-trap par direct checkmate aur Clean Hydrogen grid

Bharat ke is aitihasik masterstroke par aapki kya rai hai? Comment me likhiye!
Defence aur geopolitics explainers ke liye Reality Shift channel ko subscribe kijiye.

#Shorts #IMEC #Geopolitics
""",
    "tags": ["imec corridor", "suez canal", "red sea crisis", "imec vs suez", "india middle east europe corridor",
             "bab el mandeb", "houthi red sea", "geopolitics india", "reality shift", "india trade route"],
    "hashtags": ["#Shorts", "#IMEC", "#Geopolitics"],
}


def thumbnail(ctx):
    """1080x1920 cover: Ever Given blocked Suez Canal vs Glowing IMEC Golden Route."""
    grid_bg(ctx, 0.5, alert=True)

    # Top: Suez Blocked Ship
    ctx.save()
    ctx.translate(540, 780)
    ctx.rotate(-math.radians(24))
    container_ship(ctx, 0, 0, 1.35, 0.5, blocked=True)
    ctx.restore()

    # Bottom: High Speed Freight Train
    freight_train(ctx, 540, 1140, 0.92, 0.5)

    # Dark gradient overlays for crisp text readability
    g = cairo.LinearGradient(0, 1180, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.94)
    ctx.rectangle(0, 1180, W, H - 1180)
    ctx.set_source(g)
    ctx.fill()

    g = cairo.LinearGradient(0, 0, 0, 780)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.94)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 780)
    ctx.set_source(g)
    ctx.fill()

    vignette(ctx)
    text(ctx, "IMEC VS SUEZ", 540, 280, 140, RED, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "40% FASTER ROUTE!", 540, 440, 110, HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    tag(ctx, "RED SEA CRISIS // INDIA MASTERSTROKE", 540, 600, GREEN, 1.0)
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
    story = importlib.import_module("shorts.imec")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
