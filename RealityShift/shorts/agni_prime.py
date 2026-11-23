"""Reality Shift Short: Agni Prime — Bharat Ka Naya Game Changer Kyu Ban Raha Hai.

Topic: Agni Prime Canisterised Ballistic Missile — Road & Rail Mobility, MaRV Evasion & 2,000 KM Strategic Dominance
Format: Vertical 1080x1920 (9:16) for YouTube Shorts
Audio: KikiVoice narrator audio (~21.5s), aligned and split via Whisper
Visuals: Heavy 8x8 TEL launcher elevating launch canister, military rail-car launcher,
         hermetically sealed canister cutaway defying spy satellites, hypersonic MaRV warhead
         dodging enemy BMD air defense in terminal re-entry, 2,000 km tactical strike zone.
"""

import importlib
import json
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
from shorts.chabahar import Cued
from shorts.reality_shift import flag

TOPIC = "AGNI PRIME GAME CHANGER"
OUTPUTS = {"edge": "agni_prime_short.mp4"}
LEGO = {"header": "radar", "caption": "typewriter", "transition": "scan", "palette": "glacier", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.55
TAIL_PAD = 0.20
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 120
MUSIC_STYLE = "march"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 250

PAL = lego.PALETTES["glacier"]
UI = PAL["ui"]
HI = PAL["hi"]
RED = PAL["alert"]
INK = PAL["ink"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
STEEL = hexc("#90A4AE")
DARK_STEEL = hexc("#1A2530")
RADAR_GREEN = hexc("#00FF66")
CYAN = hexc("#00E5FF")
WHITE = (1.0, 1.0, 1.0)
FIRE_ORANGE = hexc("#FF5500")
GOLD = hexc("#FFD700")
SKY_DARK = hexc("#050B14")
MONO = "Consolas"

SOURCES = [
    "Defence Research and Development Organisation (DRDO) - Agni-Prime (Agni-P) two-stage canisterised solid-propellant ballistic missile flight test parameters (MoD / PIB).",
    "Strategic Forces Command (SFC) & DRDO - Pre-induction night launch from Dr APJ Abdul Kalam Island, Odisha, validating dual redundant navigation and terminal Maneuverable Re-entry Vehicle (MaRV).",
    "Jane's Defence & CSIS Missile Threat - Agni-P road and rail mobile Transporter Erector Launcher (TEL) canister design and comparison vs legacy liquid-fueled systems.",
]

SPEC = [
    # Scene 1: Road & Rail Mobile Rapid Launch Hook
    {"key": "rail_road_hook", "accent": RED, "text": "ROAD & RAIL MISSILE LAUNCH",
     "visual": "Heavy 8x8 TEL launcher and tactical rail carriage deploying; hydraulic cylinder elevates sealed canister to 85°; supersonic missile launch blast",
     "vo": [("tell", [("सड़क हो या रेलवे ट्रैक—", "SADAK HO YA RAILWAY TRACK —"),
                      ("महज़ कुछ ही मिनटों में", "MAHAZ KUCH HI MINUTE MEIN"),
                      ("सुपरसोनिक मिसाइल लॉन्च!", "SUPERSONIC MISSILE LAUNCH!")])]},

    # Scene 2: Sealed Canister & Zero Satellite Warning
    {"key": "canister_secrecy", "accent": GOLD, "text": "SEALED CANISTER // ZERO WARNING",
     "visual": "Hermetically sealed composite canister cutaway; 15-year ready storage; hostile spy satellite scanning overhead but finding zero fuel/thermal signature",
     "vo": [("tell", [("यही है भारत की अग्नि प्राइम!", "YAHI HAI BHARAT KI AGNI PRIME!"),
                      ("कैनिस्टर में बंद,", "CANISTER MEIN BAND,"),
                      ("सालों तक रेडी-टू-लॉन्च!", "SAALON TAK READY-TO-LAUNCH!"),
                      ("दुश्मन सेटेलाइट को भनक तक नहीं!", "DUSHMAN SATELLITE KO BHANAK TAK NAHI!")])]},

    # Scene 3: 2,000 KM Range & MaRV Air Defense Evasion
    {"key": "marv_evasion_strike", "accent": FIRE_ORANGE, "text": "2,000 KM // MARV WARHEAD",
     "visual": "Hypersonic atmospheric re-entry; maneuverable re-entry vehicle (MaRV) with terminal fins executing high-G maneuvers, dodging enemy interceptor missile to destroy target",
     "vo": [("tell", [("दो हज़ार किलोमीटर रेंज,", "2,000 KM RANGE,"),
                      ("और इसका हवा में मुड़ने वाला वारहेड", "AUR ISKA HAWA MEIN MUDNE WALA WARHEAD"),
                      ("दुश्मन के एयर डिफेंस को", "DUSHMAN KE AIR DEFENSE KO"),
                      ("चकमा देकर तबाह कर देता है!", "CHAKMA DEKAR TABAH KAR DETA HAI!")])]},

    # Scene 4: Infinite Loop CTA & Audience Poll
    {"key": "cta_poll", "accent": SAFFRON, "text": "AGNI PRIME GAME CHANGER",
     "visual": "Tactical commander HUD with 2,000 km glowing strike envelope over Bharat map; mobile launcher in ready posture; interactive poll card",
     "vo": [("tell", [("यानी बचने की कोई गुंजाइश नहीं!", "YAANI BACHNE KI KOI GUNJAISH NAHI!"),
                      ("क्या अग्नि प्राइम असली गेम चेंजर है?", "KYA AGNI PRIME ASLI GAME CHANGER HAI?"),
                      ("कमेंट में बताओ!", "COMMENT MEIN BATAO!")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "SADAK": SAFFRON, "RAILWAY": CYAN, "TRACK": CYAN, "MAHAZ": GOLD, "KUCH": GOLD,
    "MINUTE": CYAN, "SUPERSONIC": FIRE_ORANGE, "MISSILE": FIRE_ORANGE, "LAUNCH": RED,
    "BHARAT": SAFFRON, "AGNI": FIRE_ORANGE, "PRIME": GOLD, "CANISTER": CYAN,
    "BAND": GOLD, "SAALON": GOLD, "READY-TO-LAUNCH": INDIA_GREEN,
    "DUSHMAN": RED, "SATELLITE": CYAN, "BHANAK": RED, "NAHI": RED,
    "2,000": CYAN, "KM": CYAN, "RANGE": CYAN, "HAWA": GOLD, "MUDNE": GOLD,
    "WARHEAD": RED, "AIR": RED, "DEFENSE": RED, "CHAKMA": GOLD, "TABAH": RED,
    "BACHNE": RED, "ZERO": RED, "CHANCE": RED, "GUNJAISH": RED,
    "ASLI": GOLD, "GAME": RED, "CHANGER": RED, "COMMENT": HI, "BATAO": HI,
    "HAAN": INDIA_GREEN, "NAA": RED
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".—,?!")] = HOT[_k]


def ell(ctx, x, y, rx, ry):
    """Draw an ellipse centered at (x, y) with radii rx, ry."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1.0, 0, 2 * math.pi)
    ctx.restore()


# ============================================================
# PROCEDURAL DRAWING ROUTINES (8x8 TEL, Canister, Agni-P, MaRV)
# ============================================================

def draw_tel_truck(ctx, x, y, scale=1.0, canister_ang=0.0, blast=0.0):
    """Draw 8x8 heavy Transporter Erector Launcher (TEL) with elevating launch canister."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(scale, scale)

    # 1. Wheels (4 axles: 8 huge off-road tires)
    wheel_xs = [-180, -110, 80, 150]
    for wx in wheel_xs:
        # Outer tire
        circle(ctx, wx, 35, 26, (0.12, 0.14, 0.16), 1.0)
        circle(ctx, wx, 35, 20, (0.05, 0.06, 0.08), 1.0)
        # Steel Rim & Hub
        circle(ctx, wx, 35, 12, STEEL, 1.0)
        circle(ctx, wx, 35, 5, (0.02, 0.03, 0.04), 1.0)
        # Tire tread notches
        for a_deg in range(0, 360, 45):
            rad = math.radians(a_deg)
            line(ctx, [(wx + 18 * math.cos(rad), 35 + 18 * math.sin(rad)),
                       (wx + 25 * math.cos(rad), 35 + 25 * math.sin(rad))], (0.2, 0.22, 0.25), 2.5)

    # 2. Heavy Chassis Frame
    rrect(ctx, -210, -5, 400, 35, 4)
    ctx.set_source_rgb(0.18, 0.22, 0.26)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.08, 0.1, 0.12)
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Hydraulic Outriggers (Stabilizer jacks down)
    for out_x in [-195, 175]:
        rrect(ctx, out_x - 6, 20, 12, 28, 2)
        ctx.set_source_rgb(0.3, 0.35, 0.4)
        ctx.fill()
        rrect(ctx, out_x - 16, 46, 32, 6, 2)
        ctx.set_source_rgb(0.15, 0.18, 0.22)
        ctx.fill()

    # 3. Armored Cabin (Right side, forward-facing cab)
    ctx.move_to(120, -5)
    ctx.line_to(120, -55)
    ctx.line_to(185, -55)
    ctx.line_to(205, -25)
    ctx.line_to(205, -5)
    ctx.close_path()
    ctx.set_source_rgb(0.24, 0.30, 0.26)  # Military olive drab
    ctx.fill_preserve()
    ctx.set_source_rgb(0.1, 0.14, 0.12)
    ctx.set_line_width(2.5)
    ctx.stroke()

    # Armored Windshield & Side Windows
    ctx.move_to(130, -50)
    ctx.line_to(155, -50)
    ctx.line_to(155, -28)
    ctx.line_to(130, -28)
    ctx.close_path()
    ctx.set_source_rgb(0.2, 0.45, 0.55)
    ctx.fill()

    ctx.move_to(162, -50)
    ctx.line_to(182, -50)
    ctx.line_to(198, -28)
    ctx.line_to(162, -28)
    ctx.close_path()
    ctx.set_source_rgb(0.15, 0.38, 0.5)
    ctx.fill()

    # Headlights & Bumper
    rrect(ctx, 202, -18, 8, 12, 2)
    ctx.set_source_rgb(1.0, 0.9, 0.5)
    ctx.fill()

    # 4. Canister Support Frame & Hydraulic Actuator
    # Pivot at x = -130, y = -10
    pivot_x, pivot_y = -130, -10
    circle(ctx, pivot_x, pivot_y, 10, STEEL, 1.0)
    circle(ctx, pivot_x, pivot_y, 5, (0.1, 0.1, 0.1), 1.0)

    # Hydraulic Cylinder
    hyd_top_x = pivot_x + 90 * math.cos(canister_ang)
    hyd_top_y = pivot_y - 90 * math.sin(canister_ang)
    line(ctx, [(pivot_x + 70, 0), (hyd_top_x, hyd_top_y)], (0.7, 0.75, 0.8), 7)
    line(ctx, [(pivot_x + 70, 0), (pivot_x + 35, -5)], (0.2, 0.25, 0.3), 11)

    # 5. Elevating Composite Launch Canister
    ctx.save()
    ctx.translate(pivot_x, pivot_y)
    ctx.rotate(-canister_ang)  # rotate up

    # Canister main body cylinder
    can_len = 310
    can_diam = 48
    rrect(ctx, -20, -can_diam * 0.5, can_len, can_diam, 6)
    g_can = cairo.LinearGradient(0, -can_diam * 0.5, 0, can_diam * 0.5)
    g_can.add_color_stop_rgb(0, 0.28, 0.34, 0.40)
    g_can.add_color_stop_rgb(0.35, 0.50, 0.58, 0.65)
    g_can.add_color_stop_rgb(0.7, 0.30, 0.36, 0.42)
    g_can.add_color_stop_rgb(1, 0.16, 0.20, 0.25)
    ctx.set_source(g_can)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.1, 0.14, 0.18)
    ctx.set_line_width(2.5)
    ctx.stroke()

    # Carbon Composite Reinforcing Rings
    for rx in [30, 95, 160, 225, 280]:
        rrect(ctx, rx, -can_diam * 0.5 - 2, 8, can_diam + 4, 2)
        ctx.set_source_rgb(0.12, 0.15, 0.18)
        ctx.fill()

    # Indian Tricolor Band on Canister
    rrect(ctx, 115, -can_diam * 0.5 + 2, 36, 14, 1)
    ctx.set_source_rgb(1.0, 0.6, 0.2)
    ctx.fill()
    rrect(ctx, 115, -can_diam * 0.5 + 16, 36, 14, 1)
    ctx.set_source_rgb(1.0, 1.0, 1.0)
    ctx.fill()
    circle(ctx, 133, -can_diam * 0.5 + 23, 5, (0.0, 0.1, 0.6), 1.0)
    rrect(ctx, 115, -can_diam * 0.5 + 30, 36, 14, 1)
    ctx.set_source_rgb(0.1, 0.6, 0.15)
    ctx.fill()

    # Canister Endcap / Blast Hatch
    rrect(ctx, can_len - 24, -can_diam * 0.5 - 4, 26, can_diam + 8, 4)
    ctx.set_source_rgb(0.65, 0.70, 0.75)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.2, 0.25, 0.3)
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Text markings
    ctx.save()
    ctx.set_source_rgb(0.85, 0.9, 0.95)
    ctx.select_font_face(MONO, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(14)
    ctx.move_to(170, 4)
    ctx.show_text("AGNI-P // SFC")
    ctx.restore()

    ctx.restore()  # canister restore

    # 6. Launch Fire / Ejection Blast
    if blast > 0.05:
        bx = pivot_x + (can_len + 10) * math.cos(canister_ang)
        by = pivot_y - (can_len + 10) * math.sin(canister_ang)
        ctx.save()
        ctx.translate(bx, by)
        ctx.rotate(-canister_ang)

        # Expanding supersonic flame plume
        g_plume = cairo.LinearGradient(0, 0, 180 * blast, 0)
        g_plume.add_color_stop_rgb(0, 1.0, 1.0, 0.9)
        g_plume.add_color_stop_rgb(0.25, 1.0, 0.65, 0.15)
        g_plume.add_color_stop_rgb(0.7, 0.95, 0.2, 0.05)
        g_plume.add_color_stop_rgba(1, 0.5, 0.05, 0.0, 0.0)
        ctx.set_source(g_plume)

        ctx.move_to(0, -22 * blast)
        ctx.line_to(190 * blast, -48 * blast)
        ctx.line_to(220 * blast, 0)
        ctx.line_to(190 * blast, 48 * blast)
        ctx.line_to(0, 22 * blast)
        ctx.close_path()
        ctx.fill()

        # Mach Diamonds
        for m_dist in [40, 80, 120]:
            if m_dist * blast < 180 * blast:
                ell(ctx, m_dist * blast, 0, 12 * blast, 6 * blast)
                ctx.set_source_rgba(1.0, 1.0, 0.8, 0.85)
                ctx.fill()

        # Billowing Launch Smoke Clouds
        for s_idx, (sx, sy, sr) in enumerate([(-15, -45, 35), (20, -55, 45), (10, 50, 42), (-25, 40, 38)]):
            circle(ctx, sx * blast, sy * blast, sr * blast, (0.85, 0.88, 0.92), 0.45)

        ctx.restore()

    ctx.restore()


def draw_rail_launcher(ctx, x, y, scale=1.0, hatch_open=0.0):
    """Draw tactical military railway carriage with roof launch hatches."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(scale, scale)

    # 1. Rail Tracks & Sleepers
    rrect(ctx, -240, 42, 480, 12, 2)
    ctx.set_source_rgb(0.3, 0.25, 0.2)
    ctx.fill()
    for rx in range(-230, 240, 28):
        rrect(ctx, rx, 38, 14, 18, 1)
        ctx.set_source_rgb(0.2, 0.16, 0.12)
        ctx.fill()
    # Steel Rails
    rrect(ctx, -240, 34, 480, 5, 1)
    ctx.set_source_rgb(0.7, 0.75, 0.8)
    ctx.fill()

    # 2. Bogie Wheels
    for bogie_x in [-150, 150]:
        for bx in [bogie_x - 35, bogie_x + 35]:
            circle(ctx, bx, 25, 18, (0.2, 0.22, 0.25), 1.0)
            circle(ctx, bx, 25, 12, STEEL, 1.0)
            circle(ctx, bx, 25, 5, (0.05, 0.05, 0.05), 1.0)
        # Bogie frame
        rrect(ctx, bogie_x - 50, 10, 100, 12, 2)
        ctx.set_source_rgb(0.12, 0.15, 0.18)
        ctx.fill()

    # 3. Railway Wagon Body (Dark Military Boxcar)
    rrect(ctx, -220, -75, 440, 88, 4)
    g_rail = cairo.LinearGradient(0, -75, 0, 13)
    g_rail.add_color_stop_rgb(0, 0.18, 0.24, 0.22)
    g_rail.add_color_stop_rgb(0.5, 0.25, 0.32, 0.28)
    g_rail.add_color_stop_rgb(1, 0.12, 0.16, 0.15)
    ctx.set_source(g_rail)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.08, 0.1, 0.09)
    ctx.set_line_width(2.5)
    ctx.stroke()

    # Camouflage panel stripes
    for px, pw in [(-160, 45), (-80, 55), (40, 60), (130, 40)]:
        rrect(ctx, px, -73, pw, 84, 1)
        ctx.set_source_rgba(0.15, 0.18, 0.16, 0.5)
        ctx.fill()

    # Sliding Roof Hatch (opens left & right when hatch_open > 0)
    hatch_shift = 65 * hatch_open
    rrect(ctx, -120 - hatch_shift, -85, 115, 12, 2)
    ctx.set_source_rgb(0.4, 0.45, 0.5)
    ctx.fill()
    rrect(ctx, 5 + hatch_shift, -85, 115, 12, 2)
    ctx.set_source_rgb(0.4, 0.45, 0.5)
    ctx.fill()

    # Elevated Agni-P Canister emerging from wagon
    if hatch_open > 0.1:
        ctx.save()
        rrect(ctx, -22, -85 - 140 * hatch_open, 44, 150 * hatch_open, 4)
        g_c = cairo.LinearGradient(-22, 0, 22, 0)
        g_c.add_color_stop_rgb(0, 0.3, 0.38, 0.45)
        g_c.add_color_stop_rgb(0.5, 0.55, 0.65, 0.75)
        g_c.add_color_stop_rgb(1, 0.25, 0.32, 0.38)
        ctx.set_source(g_c)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.1, 0.15, 0.2)
        ctx.set_line_width(2)
        ctx.stroke()
        # Top dome
        circle(ctx, 0, -85 - 140 * hatch_open, 22, STEEL, 1.0)
        ctx.restore()

    ctx.restore()


def draw_agni_prime_missile(ctx, x, y, scale=1.0, angle=0.0, flame=True):
    """Draw Agni Prime two-stage solid-fueled ballistic missile in flight."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(angle)
    ctx.scale(scale, scale)

    # 1. Supersonic Exhaust Plume (Bottom)
    if flame:
        g_f = cairo.LinearGradient(0, 110, 0, 260)
        g_f.add_color_stop_rgb(0, 1.0, 1.0, 0.9)
        g_f.add_color_stop_rgb(0.25, 1.0, 0.6, 0.1)
        g_f.add_color_stop_rgb(0.65, 0.9, 0.2, 0.05)
        g_f.add_color_stop_rgba(1, 0.4, 0.05, 0.0, 0.0)
        ctx.set_source(g_f)

        ctx.move_to(-14, 110)
        ctx.line_to(-28, 220)
        ctx.line_to(0, 265)
        ctx.line_to(28, 220)
        ctx.line_to(14, 110)
        ctx.close_path()
        ctx.fill()

        # Mach diamonds
        for m_y in [140, 175, 210]:
            ell(ctx, 0, m_y, 7, 14)
            ctx.set_source_rgba(1.0, 1.0, 0.8, 0.85)
            ctx.fill()

    # 2. Stage 1 Motor Casing (Bottom half)
    rrect(ctx, -18, 10, 36, 100, 2)
    g_stg1 = cairo.LinearGradient(-18, 0, 18, 0)
    g_stg1.add_color_stop_rgb(0, 0.22, 0.26, 0.30)
    g_stg1.add_color_stop_rgb(0.4, 0.45, 0.52, 0.60)
    g_stg1.add_color_stop_rgb(1, 0.15, 0.18, 0.22)
    ctx.set_source(g_stg1)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.1, 0.12, 0.15)
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Carbon composite bands
    for by in [35, 65, 95]:
        rrect(ctx, -18, by, 36, 4, 1)
        ctx.set_source_rgb(0.1, 0.12, 0.14)
        ctx.fill()

    # 3. Interstage Separation Lattice
    rrect(ctx, -17, 2, 34, 8, 1)
    ctx.set_source_rgb(0.12, 0.14, 0.16)
    ctx.fill()
    for lx in range(-14, 15, 7):
        line(ctx, [(lx, 2), (lx + 3, 10)], (0.7, 0.75, 0.8), 1.5)

    # 4. Stage 2 Motor Casing (Upper half)
    rrect(ctx, -16, -70, 32, 72, 2)
    g_stg2 = cairo.LinearGradient(-16, 0, 16, 0)
    g_stg2.add_color_stop_rgb(0, 0.80, 0.84, 0.90)
    g_stg2.add_color_stop_rgb(0.5, 0.95, 0.98, 1.00)
    g_stg2.add_color_stop_rgb(1, 0.65, 0.70, 0.78)
    ctx.set_source(g_stg2)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.2, 0.25, 0.3)
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Indian Tricolor on Stage 2
    rrect(ctx, -14, -55, 28, 6, 1)
    ctx.set_source_rgb(1.0, 0.6, 0.2)
    ctx.fill()
    rrect(ctx, -14, -49, 28, 6, 1)
    ctx.set_source_rgb(1.0, 1.0, 1.0)
    ctx.fill()
    circle(ctx, 0, -46, 2.5, (0.0, 0.1, 0.6), 1.0)
    rrect(ctx, -14, -43, 28, 6, 1)
    ctx.set_source_rgb(0.1, 0.6, 0.15)
    ctx.fill()

    # 5. Maneuverable Re-entry Vehicle (MaRV Nose Cone & Control Fins)
    ctx.move_to(-16, -70)
    ctx.line_to(-10, -115)
    ctx.line_to(0, -145)  # sharp nose tip
    ctx.line_to(10, -115)
    ctx.line_to(16, -70)
    ctx.close_path()
    g_marv = cairo.LinearGradient(-16, 0, 16, 0)
    g_marv.add_color_stop_rgb(0, 0.35, 0.40, 0.48)
    g_marv.add_color_stop_rgb(0.5, 0.65, 0.75, 0.85)
    g_marv.add_color_stop_rgb(1, 0.25, 0.30, 0.36)
    ctx.set_source(g_marv)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.1, 0.15, 0.2)
    ctx.set_line_width(2.0)
    ctx.stroke()

    # MaRV Aerodynamic Grid/Steering Fins
    for fin_dir in [-1, 1]:
        ctx.move_to(fin_dir * 14, -75)
        ctx.line_to(fin_dir * 28, -82)
        ctx.line_to(fin_dir * 26, -95)
        ctx.line_to(fin_dir * 12, -92)
        ctx.close_path()
        ctx.set_source_rgb(0.18, 0.22, 0.28)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.5, 0.6, 0.7)
        ctx.set_line_width(1.5)
        ctx.stroke()

    ctx.restore()


def draw_marv_warhead(ctx, x, y, scale=1.0, angle=0.0, plasma=True):
    """Draw Maneuverable Re-entry Vehicle (MaRV) with glowing hypersonic plasma trail."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(angle)
    ctx.scale(scale, scale)

    # 1. Hypersonic Re-entry Shockwave / Plasma Cone
    if plasma:
        ctx.save()
        g_plas = cairo.LinearGradient(0, -80, 0, 90)
        g_plas.add_color_stop_rgba(0, 0.0, 0.9, 1.0, 0.7)
        g_plas.add_color_stop_rgba(0.3, 0.9, 0.2, 0.8, 0.5)
        g_plas.add_color_stop_rgba(0.7, 1.0, 0.5, 0.1, 0.3)
        g_plas.add_color_stop_rgba(1, 0.8, 0.1, 0.0, 0.0)
        ctx.set_source(g_plas)

        ctx.move_to(0, -90)
        ctx.curve_to(35, -40, 65, 30, 85, 95)
        ctx.line_to(-85, 95)
        ctx.curve_to(-65, 30, -35, -40, 0, -90)
        ctx.close_path()
        ctx.fill()
        ctx.restore()

    # 2. MaRV Body
    ctx.move_to(0, -75)  # Warhead tip
    ctx.line_to(15, -20)
    ctx.line_to(18, 35)
    ctx.line_to(-18, 35)
    ctx.line_to(-15, -20)
    ctx.close_path()
    g_w = cairo.LinearGradient(-18, 0, 18, 0)
    g_w.add_color_stop_rgb(0, 0.3, 0.36, 0.44)
    g_w.add_color_stop_rgb(0.45, 0.75, 0.85, 0.95)
    g_w.add_color_stop_rgb(1, 0.2, 0.25, 0.32)
    ctx.set_source(g_w)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.08, 0.12, 0.16)
    ctx.set_line_width(2.5)
    ctx.stroke()

    # 3. Cruciform Steering Fins
    for f_side in [-1, 1]:
        ctx.move_to(f_side * 17, 10)
        ctx.line_to(f_side * 34, 18)
        ctx.line_to(f_side * 32, 36)
        ctx.line_to(f_side * 18, 34)
        ctx.close_path()
        ctx.set_source_rgb(0.2, 0.26, 0.34)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.4, 0.55, 0.7)
        ctx.set_line_width(2.0)
        ctx.stroke()

    # Lateral Thruster Reaction Control System (RCS) Jet
    circle(ctx, -14, -5, 4, CYAN, 0.9)
    line(ctx, [(-14, -5), (-38, -5)], (0.0, 0.9, 1.0), 3, 0.8)

    ctx.restore()


def draw_spy_satellite(ctx, x, y, scale=1.0, scan=False):
    """Draw adversary spy reconnaissance satellite scanning with radar beam."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(scale, scale)

    # Solar Panels (Left & Right)
    for px in [-75, 35]:
        rrect(ctx, px, -15, 40, 30, 2)
        ctx.set_source_rgb(0.1, 0.35, 0.7)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.3, 0.6, 0.9)
        ctx.set_line_width(1.5)
        ctx.stroke()
        # Panel grid
        line(ctx, [(px + 20, -15), (px + 20, 15)], (0.3, 0.6, 0.9), 1)

    # Satellite Core Body
    rrect(ctx, -20, -18, 40, 36, 4)
    ctx.set_source_rgb(0.85, 0.75, 0.3)  # Gold foil thermal wrap
    ctx.fill_preserve()
    ctx.set_source_rgb(0.4, 0.35, 0.1)
    ctx.set_line_width(2)
    ctx.stroke()

    # Optical / Radar Dish pointing down
    ctx.arc(0, 18, 16, 0, math.pi)
    ctx.set_source_rgb(0.6, 0.65, 0.7)
    ctx.fill()
    line(ctx, [(0, 18), (0, 32)], (0.3, 0.35, 0.4), 2.5)

    # Scanning Cone
    if scan:
        g_sc = cairo.LinearGradient(0, 32, 0, 220)
        g_sc.add_color_stop_rgba(0, 1.0, 0.1, 0.1, 0.5)
        g_sc.add_color_stop_rgba(1, 1.0, 0.1, 0.1, 0.0)
        ctx.set_source(g_sc)
        ctx.move_to(0, 32)
        ctx.line_to(-120, 220)
        ctx.line_to(120, 220)
        ctx.close_path()
        ctx.fill()

    ctx.restore()


# ============================================================
# SCENE 1: Road & Rail Mobile Rapid Launch Hook
# ============================================================

class SceneRailRoadHook(Cued):
    def events(self, d):
        return [(0.4, "whoosh"), (2.2, "boom")]

    def draw(self, ctx, t, d):
        # Dark tactical twilight backdrop
        ctx.set_source_rgb(0.02, 0.04, 0.08)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()

        # Dynamic perspective terrain / road & rail tracks
        ctx.save()
        g_road = cairo.LinearGradient(0, 850, 0, 1400)
        g_road.add_color_stop_rgb(0, 0.08, 0.10, 0.14)
        g_road.add_color_stop_rgb(1, 0.04, 0.05, 0.07)
        ctx.set_source(g_road)
        ctx.rectangle(0, 850, W, 550)
        ctx.fill()

        # Highway dashed lines
        for hx in range(-50, W + 100, 110):
            line(ctx, [(hx, 1150), (hx + 50, 1150)], (0.9, 0.85, 0.4), 4, 0.6)

        # Tactical Rail Track at bottom
        for rx in range(-20, W + 40, 35):
            rrect(ctx, rx, 1260, 14, 30, 2)
            ctx.set_source_rgb(0.25, 0.22, 0.18)
            ctx.fill()
        line(ctx, [(0, 1270), (W, 1270)], STEEL, 5)
        line(ctx, [(0, 1285), (W, 1285)], STEEL, 5)
        ctx.restore()

        # Distant mountain silhouettes & night sky stars
        ctx.save()
        for i in range(25):
            sx = (i * 137 + 45) % W
            sy = (i * 89 + 120) % 650
            circle(ctx, sx, sy, 1.5, WHITE, 0.6 + 0.4 * math.sin(t * 3.0 + i))
        ctx.restore()

        # Elevating Canister on 8x8 TEL Truck (Center-left)
        elev_progress = clamp(t / 2.2, 0.0, 1.0)
        # Smoothly elevate from 10 deg to 82 deg
        can_angle = math.radians(15 + 67 * ease_out_cubic(elev_progress))
        blast_progress = clamp((t - 1.8) / 1.0, 0.0, 1.0) if t > 1.8 else 0.0

        draw_tel_truck(ctx, 420, 1020, scale=1.35, canister_ang=can_angle, blast=blast_progress)

        # Camouflaged Military Rail Wagon on the right
        draw_rail_launcher(ctx, 880, 1230, scale=0.95, hatch_open=clamp(t / 2.5, 0.0, 0.8))

        # Agni-P missile emerging in cold/hot launch if blast > 0
        if blast_progress > 0.05:
            m_dist = 180 * blast_progress
            mx = 420 - 130 * 1.35 + (310 * 1.35 + m_dist) * math.cos(can_angle)
            my = 1020 - 10 * 1.35 - (310 * 1.35 + m_dist) * math.sin(can_angle)
            draw_agni_prime_missile(ctx, mx, my, scale=1.1, angle=math.pi * 0.5 - can_angle, flame=True)


# ============================================================
# SCENE 2: Sealed Canister & Zero Satellite Warning
# ============================================================

class SceneCanisterSecrecy(Cued):
    def events(self, d):
        return [(0.4, "beep"), (2.0, "whoosh")]

    def draw(self, ctx, t, d):
        # Deep space & high-altitude tactical backdrop
        ctx.set_source_rgb(0.01, 0.02, 0.05)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()

        # Orbiting Enemy Spy Satellite at top
        sat_x = 240 + ((t * 60) % (W - 200))
        draw_spy_satellite(ctx, sat_x, 340, scale=1.4, scan=True)

        # Large Technical Cross-Section of Canister in Center
        cx, cy = W * 0.5, 820
        can_w, can_h = 380, 520

        rrect(ctx, cx - can_w * 0.5, cy - can_h * 0.5, can_w, can_h, 16)
        ctx.set_source_rgba(0.05, 0.08, 0.14, 0.92)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.2, 0.7, 0.9)
        ctx.set_line_width(3.0)
        ctx.stroke()

        # Interior Hermetic Seal Glow
        pulse = 0.5 + 0.3 * math.sin(t * 4.0)
        rrect(ctx, cx - can_w * 0.5 + 16, cy - can_h * 0.5 + 16, can_w - 32, can_h - 32, 12)
        ctx.set_source_rgba(0.0, 0.9, 0.5, 0.15 * pulse)
        ctx.fill()

        # Agni-P Missile seated ready inside canister
        draw_agni_prime_missile(ctx, cx, cy + 20, scale=1.35, angle=0, flame=False)


# ============================================================
# SCENE 3: 2,000 KM Range & MaRV Air Defense Evasion
# ============================================================

class SceneMarvEvasionStrike(Cued):
    def events(self, d):
        return [(0.3, "whoosh"), (2.5, "boom")]

    def draw(self, ctx, t, d):
        # Stratospheric hypersonic re-entry view (Dark blue to fiery orange horizon)
        g_bg = cairo.LinearGradient(0, 0, 0, H)
        g_bg.add_color_stop_rgb(0, 0.01, 0.02, 0.06)
        g_bg.add_color_stop_rgb(0.65, 0.05, 0.08, 0.18)
        g_bg.add_color_stop_rgb(0.9, 0.25, 0.10, 0.05)
        g_bg.add_color_stop_rgb(1, 0.05, 0.02, 0.02)
        ctx.set_source(g_bg)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()

        # Atmospheric glowing re-entry plasma clouds
        ctx.save()
        for i in range(12):
            cy = 380 + i * 55
            cx = (W * 0.5 + math.sin(t * 3.0 + i) * 180)
            glow(ctx, cx, cy, 75, FIRE_ORANGE, 0.25)
        ctx.restore()

        # MaRV Trajectory Trail (High-G S-curve Evasive Maneuver)
        ctx.save()
        ctx.set_source_rgba(0.0, 0.9, 1.0, 0.65)
        ctx.set_line_width(6)
        ctx.move_to(W * 0.5 - 120, 260)
        ctx.curve_to(W * 0.5 + 240, 460, W * 0.5 - 280, 660, W * 0.5 + 100, 920)
        ctx.stroke()
        ctx.restore()

        # Current MaRV Position along evasive path
        path_t = clamp(t / 2.2, 0.0, 1.0)
        # Interpolate S-curve position
        mx = W * 0.5 + math.sin(path_t * math.pi * 2.2) * 160
        my = 280 + path_t * 640
        marv_ang = math.radians(22 + 25 * math.cos(path_t * math.pi * 2.2))

        draw_marv_warhead(ctx, mx, my, scale=1.55, angle=marv_ang, plasma=True)

        # Hostile Air Defense Interceptor Missile MISSING completely
        int_t = clamp((t - 0.6) / 1.5, 0.0, 1.0)
        ix = 250 + int_t * 480
        iy = 1050 - int_t * 580
        if int_t > 0.0:
            circle(ctx, ix, iy, 12, RED, 0.9)
            line(ctx, [(ix, iy), (ix - 80, iy + 90)], (1.0, 0.2, 0.2), 4, 0.8)

        # Target Strike Impact at Bottom if t > 2.0
        if t > 2.0:
            blast_t = (t - 2.0)
            circle(ctx, W * 0.5 + 100, 1020, 70 * blast_t, FIRE_ORANGE, 0.85)
            glow(ctx, W * 0.5 + 100, 1020, 160 * blast_t, GOLD, 0.9)


# ============================================================
# SCENE 4: Infinite Loop CTA & Audience Poll
# ============================================================

class SceneCtaPoll(Cued):
    def events(self, d):
        return [(0.3, "whoosh"), (2.0, "pop")]

    def draw(self, ctx, t, d):
        # Command center deep background
        ctx.set_source_rgb(0.02, 0.03, 0.06)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()

        # Strategic concentric range rings (2,000 km dome)
        center_x, center_y = W * 0.5, 340
        for r_km, r_px, col in [(500, 120, CYAN), (1000, 210, GOLD), (2000, 310, RED)]:
            circle(ctx, center_x, center_y, r_px, col, 0.10)
            ctx.save()
            ctx.set_source_rgba(col[0], col[1], col[2], 0.40)
            ctx.set_line_width(2.0)
            ctx.set_dash([8, 8], t * 15)
            ctx.arc(center_x, center_y, r_px, 0, 2 * math.pi)
            ctx.stroke()
            ctx.restore()
            text(ctx, f"{r_km} KM", center_x + r_px - 40, center_y - 10, 15, col, font=MONO, anchor="c")

        # Center: Agni-P launcher in ready posture
        draw_tel_truck(ctx, center_x - 20, center_y + 40, scale=0.85, canister_ang=math.radians(75), blast=0.0)

        # Flag of India Badge
        rrect(ctx, center_x - 65, 200, 130, 40, 6)
        ctx.set_source_rgba(0.05, 0.1, 0.15, 0.9)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.9, 0.9, 0.9)
        ctx.set_line_width(1.5)
        ctx.stroke()
        flag(ctx, center_x - 55, 206, 42, 28, "in", t)
        text(ctx, "SFC", center_x + 20, 226, 20, GOLD, font=MONO, anchor="c")

        # Interactive Poll Card (HAAN vs NAA) placed safely above caption safe zone
        py = 560
        rrect(ctx, 100, py, W - 200, 320, 18)
        ctx.set_source_rgba(0.03, 0.06, 0.12, 0.95)
        ctx.fill_preserve()
        ctx.set_source_rgb(1.0, 0.65, 0.1)
        ctx.set_line_width(3.0)
        ctx.stroke()

        text(ctx, "KYA AGNI PRIME GAME CHANGER HAI?", W * 0.5, py + 48, 25, GOLD, anchor="c")

        # HAAN bar (94%)
        rrect(ctx, 140, py + 88, W - 280, 52, 8)
        ctx.set_source_rgb(0.08, 0.22, 0.14)
        ctx.fill()
        rrect(ctx, 140, py + 88, (W - 280) * 0.94, 52, 8)
        ctx.set_source_rgb(0.1, 0.7, 0.25)
        ctx.fill()
        text(ctx, "HAAN  94%", W * 0.5, py + 124, 22, WHITE, font=MONO, anchor="c")

        # NAA bar (6%)
        rrect(ctx, 140, py + 158, W - 280, 52, 8)
        ctx.set_source_rgb(0.20, 0.08, 0.08)
        ctx.fill()
        rrect(ctx, 140, py + 158, (W - 280) * 0.06, 52, 8)
        ctx.set_source_rgb(0.8, 0.15, 0.15)
        ctx.fill()
        text(ctx, "NAA  6%", W * 0.5, py + 194, 20, (0.8, 0.8, 0.8), font=MONO, anchor="c")

        # Animated pointer arrow to comment button
        arrow_y = py + 242 + math.sin(t * 6.0) * 6
        line(ctx, [(W * 0.5 - 60, arrow_y), (W * 0.5 + 60, arrow_y)], SAFFRON, 4)
        line(ctx, [(W * 0.5 + 40, arrow_y - 10), (W * 0.5 + 60, arrow_y), (W * 0.5 + 40, arrow_y + 10)], SAFFRON, 4)
        text(ctx, "COMMENT MEIN BATAO!", W * 0.5, py + 284, 23, CYAN, font=MONO, anchor="c")


SCENE_CLASSES = {
    "rail_road_hook": SceneRailRoadHook,
    "canister_secrecy": SceneCanisterSecrecy,
    "marv_evasion_strike": SceneMarvEvasionStrike,
    "cta_poll": SceneCtaPoll,
}


UPLOAD = {
    "titles": [
        "Agni Prime Missile Bharat Ka Naya Game Changer Kyu Ban Raha Hai? 🇮🇳🔥 #shorts",
        "Why Agni Prime Missile Is A Nightmare For Adversaries? 🚀 #shorts",
        "Train Se Bhi Launch Hogi Bharat Ki Agni Prime! 🇮🇳 #shorts",
        "Agni Prime: Canister Launch & MaRV Warhead Explained! #shorts",
        "Agni Prime vs Adversaries: 2000 KM Strategic Deterrence! 🇮🇳 #shorts",
    ],
    "title": "Agni Prime Missile Bharat Ka Naya Game Changer Kyu Ban Raha Hai? 🇮🇳🔥 #shorts",
    "thumb_text": "AGNI PRIME STRIKE",
    "queries": ["agni prime missile", "agni p missile", "drdo agni prime"],
    "description": """Bharat ki nayi Agni Prime (Agni-P) missile border par game changer kyu ban rahi hai?
DRDO dwara viksit Agni Prime ek do-stage canisterised solid-propellant ballistic missile hai. Ise sadak ya railway network par kisi bhi mobile launcher se mahaz kuch hi minute mein daaga ja sakta hai.
Iska hermetically sealed canister ise 15 saal tak bina maintenance ke ready-to-launch rakhta hai, aur iska Maneuverable Re-entry Vehicle (MaRV) warhead dushman ke air defense / BMD radar ko hawa mein chakma dekar target ko tabah karta hai!

Is Short mein:
• Road & Rail Mobile 8x8 Transporter Erector Launcher (TEL)
• Canisterised Launch System: Zero Satellite Warning & 15-Year Storage
• 2,000 KM Strike Range & Terminal MaRV Evasion Warhead

Kya Agni Prime Bharat ka sabse shaktishali strategic game changer hai? Comment mein likhein - JAI HIND! 🇮🇳
Subscribe to RealityShift for high-tech defence breakdowns.

#Shorts #AgniPrime #DRDO #IndianArmy #IndianAirForce
""",
    "tags": [
        "agni prime", "agni p missile", "drdo agni prime", "agni missile test",
        "ballistic missile", "canister launch", "marv warhead", "indian army",
        "reality shift", "defence shorts", "viral shorts"
    ],
    "hashtags": ["#Shorts", "#AgniPrime", "#DRDO"],
}


def thumbnail(ctx):
    """High-CTR YouTube Shorts cover for Agni Prime."""
    # Dark tactical navy & space backdrop
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.01, 0.02, 0.06)
    g.add_color_stop_rgb(0.5, 0.04, 0.08, 0.16)
    g.add_color_stop_rgb(1, 0.01, 0.02, 0.05)
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()

    # Concentric 2,000 km Tactical Radar Rings
    for r in [300, 560, 820]:
        circle(ctx, W * 0.5, 1100, r, CYAN, 0.07)

    # Hero 8x8 TEL Launcher launching Agni Prime
    draw_tel_truck(ctx, 450, 1260, scale=1.75, canister_ang=math.radians(78), blast=1.0)

    # Hero Agni Prime Missile roaring upwards with massive supersonic plume
    draw_agni_prime_missile(ctx, 420, 820, scale=2.1, angle=math.radians(-12), flame=True)

    # Hypersonic MaRV Warhead at top right diving with glowing plasma
    draw_marv_warhead(ctx, 760, 520, scale=1.9, angle=math.radians(45), plasma=True)
    text(ctx, "TERMINAL MARV // MACH 8+", 760, 420, 22, GOLD, font=MONO, anchor="c")

    # High-Impact Thumbnail Header Box
    rrect(ctx, 70, 140, W - 140, 210, 22)
    ctx.set_source_rgba(0.01, 0.03, 0.08, 0.94)
    ctx.fill_preserve()
    ctx.set_source_rgb(1.0, 0.65, 0.1)
    ctx.set_line_width(4)
    ctx.stroke()

    text(ctx, "AGNI PRIME", W * 0.5, 215, 68, GOLD, anchor="c")
    text(ctx, "BHARAT KA NAYA GAME CHANGER!", W * 0.5, 295, 30, CYAN, font=MONO, anchor="c")

    # Tactical Badges at bottom
    badges = [
        ("ROAD & RAIL MOBILE", 1480, CYAN),
        ("2,000 KM RANGE", 1540, GOLD),
        ("ZERO PREP LAUNCH", 1600, RED),
    ]
    for b_text, by, b_col in badges:
        rrect(ctx, W * 0.5 - 200, by - 26, 400, 48, 8)
        ctx.set_source_rgba(0.02, 0.04, 0.08, 0.88)
        ctx.fill_preserve()
        ctx.set_source_rgb(b_col[0], b_col[1], b_col[2])
        ctx.set_line_width(2)
        ctx.stroke()
        text(ctx, b_text, W * 0.5, by + 6, 22, b_col, font=MONO, anchor="c")


def write_alignment(final: Path) -> None:
    """Word-level alignment export for captions & subtitles."""
    out = [
        {
            "scene": spec["key"],
            "start": round(s["start"], 3),
            "end": round(s["start"] + s["dur"], 3),
            "dur": round(s["dur"], 3),
            "words": [{"t": round(s["start"] + st, 3), "w": w} for st, w in s["captions"]],
        }
        for spec, s in zip(SPEC, engine.SCENES)
    ]
    path = final.with_suffix(".json")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Alignment: {path}")


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.agni_prime")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))
