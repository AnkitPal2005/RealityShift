"""Reality Shift Short: Project Kusha Range Breakdown — Stealth Jets vs Cruise Missiles.

Topic: DRDO Project Kusha Range Breakdown (350 km vs 150 km) - Countering Stealth Jets & Cruise Missiles
Format: Vertical 1080x1920 (9:16) for YouTube Shorts
Audio: KikiVoice narrator audio (~21.5s), aligned and split via Whisper
Visuals: High-altitude stealth fighter vs low-altitude terrain-hugging cruise missile,
         Project Kusha 8x8 launcher & dual-band AESA radar, 3-tier concentric interception dome,
         tactical air defense command & interactive audience poll.
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

TOPIC = "PROJECT KUSHA RANGE BREAKDOWN"
OUTPUTS = {"edge": "kusha_range_short.mp4"}
LEGO = {"header": "radar", "caption": "typewriter", "transition": "scan", "palette": "intel", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.55
TAIL_PAD = 0.20
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 124
MUSIC_STYLE = "tension"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 250

PAL = lego.PALETTES["intel"]
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
SKY_DARK = hexc("#0B132B")
TERRAIN_BROWN = hexc("#2C1810")
MONO = "Consolas"

SOURCES = [
    "Defence Research and Development Organisation (DRDO) - Project Kusha (LR-SAM / ERSAM) 3-tier interceptor missile program (150 km, 250 km, 350 km ranges).",
    "Cabinet Committee on Security (CCS) - Approval of Rs 21,700 Crore for Project Kusha Long Range Air Defence System equipped with Dual-Band AESA Radars (MoD / PIB).",
    "Indian Air Force (IAF) - Strategic Air Defence Architecture against low-RCS 5th-gen stealth fighters and low-flying terrain-hugging cruise missiles (Jane's Defence, The Hindu).",
]

SPEC = [
    # Scene 1: High vs Low Threat Hook (Stealth at 50,000 ft vs Cruise Missile at 30m)
    {"key": "high_low_threat", "accent": RED, "text": "50,000 FT VS 30M THREAT",
     "visual": "Split tactical airspace: 50,000 ft stealth fighter at top vs 30m terrain-hugging cruise missile at bottom",
     "vo": [("tell", [("पचास हज़ार फीट पर", "50,000 FT PAR"),
                      ("रडार से गायब जेट,", "RADAR SE GAYAB JET,"),
                      ("और ज़मीन से सटकर भागती", "AUR ZAMEEN SE SATKAR BHAGTI"),
                      ("क्रूज़ मिसाइल!", "CRUISE MISSILE!")])]},

    # Scene 2: Project Kusha Game Over Reveal
    {"key": "kusha_reveal", "accent": SAFFRON, "text": "DRDO PROJECT KUSHA",
     "visual": "Project Kusha 8x8 heavy mobile launcher elevates twin missile canisters; rotating dual-band AESA radar emits cyan tracking pulses",
     "vo": [("tell", [("दोनों का एक साथ", "DONO KA EK SAATH"),
                      ("गेम ओवर करने आ रहा है", "GAME OVER KARNE AA RAHA HAI"),
                      ("भारत का", "BHARAT KA"),
                      ("प्रोजेक्ट कुशा!", "PROJECT KUSHA!")])]},

    # Scene 3: Range Breakdown (350 KM Stealth vs 150 KM Cruise Missile)
    {"key": "range_breakdown", "accent": CYAN, "text": "350 KM VS 150 KM DOMES",
     "visual": "3-tier holographic radar dome: 350 km outer ring locks on stealth jet, 150 km agile interceptor obliterates cruise missile",
     "vo": [("tell", [("साढ़े तीन सौ किलोमीटर दूर से", "350 KM DOOR SE"),
                      ("इसका रडार लॉक कर देगा,", "ISKA RADAR LOCK KAR DEGA,"),
                      ("और डेढ़ सौ किलोमीटर पर", "AUR 150 KM PAR"),
                      ("मिसाइलों को सीधा", "MISSILES KO SEEDHA"),
                      ("हवा में उड़ा देगा!", "HAWA MEIN UDA DEGA!")])]},

    # Scene 4: Infinite Loop CTA & Poll
    {"key": "cta_poll", "accent": GOLD, "text": "GAME CHANGER AIR DEFENSE",
     "visual": "IAF tactical air defense commander at command console; glowing tricolor air dome over map; interactive poll card",
     "vo": [("tell", [("यानी बचने का ज़ीरो चांस!", "YAANI BACHNE KA ZERO CHANCE!"),
                      ("क्या कुशा असली", "KYA KUSHA ASLI"),
                      ("गेम चेंजर है?", "GAME CHANGER HAI?"),
                      ("कमेंट में बताओ!", "COMMENT MEIN BATAO!")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "50,000": RED, "FT": RED, "RADAR": RADAR_GREEN, "GAYAB": CYAN, "JET": CYAN,
    "CRUISE": FIRE_ORANGE, "MISSILE": FIRE_ORANGE, "MISSILES": FIRE_ORANGE,
    "GAME": RED, "OVER": RED, "BHARAT": SAFFRON, "PROJECT": GOLD, "KUSHA": GOLD,
    "350": CYAN, "KM": CYAN, "DOOR": CYAN, "LOCK": RADAR_GREEN,
    "150": FIRE_ORANGE, "SEEDHA": FIRE_ORANGE, "HAWA": CYAN, "UDA": RED,
    "ZERO": RED, "CHANCE": RED, "ASLI": GOLD, "CHANGER": GOLD,
    "COMMENT": HI, "BATAO": HI, "HAAN": INDIA_GREEN, "NAA": RED
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
# PROCEDURAL DRAWING ROUTINES (Kusha Launcher, Stealth, Cruise, Dome)
# ============================================================

def draw_stealth_jet(ctx, x, y, scale=1.0, angle=0.0):
    """Draw a stealth fighter (faceted diamond silhouette, internal bay, wing edges)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(angle)
    ctx.scale(scale, scale)

    # Airframe shadow / glow
    ctx.save()
    ctx.set_source_rgba(0, 0.9, 1.0, 0.25)
    ctx.set_line_width(8)
    ctx.move_to(0, -90)
    ctx.line_to(65, 30)
    ctx.line_to(45, 60)
    ctx.line_to(15, 50)
    ctx.line_to(0, 75)
    ctx.line_to(-15, 50)
    ctx.line_to(-45, 60)
    ctx.line_to(-65, 30)
    ctx.close_path()
    ctx.stroke()
    ctx.restore()

    # Stealth Dark Grey Body
    ctx.move_to(0, -90)
    ctx.line_to(65, 30)
    ctx.line_to(45, 60)
    ctx.line_to(15, 50)
    ctx.line_to(0, 75)
    ctx.line_to(-15, 50)
    ctx.line_to(-45, 60)
    ctx.line_to(-65, 30)
    ctx.close_path()
    ctx.set_source_rgb(0.12, 0.15, 0.20)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.25, 0.35, 0.45)
    ctx.set_line_width(2.5)
    ctx.stroke()

    # Cockpit Gold Tint
    ctx.move_to(0, -55)
    ctx.line_to(8, -25)
    ctx.line_to(0, -10)
    ctx.line_to(-8, -25)
    ctx.close_path()
    ctx.set_source_rgb(0.9, 0.7, 0.2)
    ctx.fill()

    # Twin Canted Tails
    ctx.set_line_width(3)
    ctx.set_source_rgb(0.20, 0.28, 0.36)
    ctx.move_to(20, 35)
    ctx.line_to(35, 75)
    ctx.stroke()
    ctx.move_to(-20, 35)
    ctx.line_to(-35, 75)
    ctx.stroke()

    # Afterburner cyan glow
    circle(ctx, 8, 72, 6, CYAN, 0.8)
    circle(ctx, -8, 72, 6, CYAN, 0.8)
    ctx.restore()


def draw_cruise_missile(ctx, x, y, scale=1.0, angle=0.0):
    """Draw a low-flying terrain-hugging cruise missile with stubby wings and jet plume."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(angle)
    ctx.scale(scale, scale)

    # Jet exhaust flame
    ctx.save()
    ctx.move_to(-60, 0)
    ctx.line_to(-110, -8)
    ctx.line_to(-95, 0)
    ctx.line_to(-110, 8)
    ctx.close_path()
    ctx.set_source_rgb(1.0, 0.4, 0.1)
    ctx.fill()
    circle(ctx, -65, 0, 7, (1.0, 0.9, 0.3), 0.9)
    ctx.restore()

    # Cylindrical missile fuselage
    rrect(ctx, -60, -10, 110, 20, 6)
    ctx.set_source_rgb(0.75, 0.80, 0.85)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.2, 0.3, 0.4)
    ctx.set_line_width(2)
    ctx.stroke()

    # Ogive nosecone
    ctx.move_to(50, -10)
    ctx.curve_to(75, -8, 85, 0, 90, 0)
    ctx.curve_to(85, 0, 75, 8, 50, 10)
    ctx.close_path()
    ctx.set_source_rgb(0.9, 0.2, 0.2)
    ctx.fill()

    # Mid-body deployable wings
    ctx.move_to(-5, -10)
    ctx.line_to(-25, -45)
    ctx.line_to(-10, -45)
    ctx.line_to(10, -10)
    ctx.close_path()
    ctx.set_source_rgb(0.3, 0.4, 0.5)
    ctx.fill()

    ctx.move_to(-5, 10)
    ctx.line_to(-25, 45)
    ctx.line_to(-10, 45)
    ctx.line_to(10, 10)
    ctx.close_path()
    ctx.set_source_rgb(0.3, 0.4, 0.5)
    ctx.fill()

    # Tail fins
    ctx.move_to(-55, -8)
    ctx.line_to(-68, -25)
    ctx.line_to(-58, -25)
    ctx.line_to(-48, -8)
    ctx.close_path()
    ctx.set_source_rgb(0.25, 0.35, 0.45)
    ctx.fill()

    ctx.move_to(-55, 8)
    ctx.line_to(-68, 25)
    ctx.line_to(-58, 25)
    ctx.line_to(-48, 8)
    ctx.close_path()
    ctx.set_source_rgb(0.25, 0.35, 0.45)
    ctx.fill()
    ctx.restore()


def draw_kusha_launcher(ctx, x, y, scale=1.0, elevate=0.0):
    """Draw DRDO Project Kusha heavy 8x8 Transporter Erector Launcher (TEL).
    
    Canisters pivot at the rear flatbed and elevate UPWARDS into the sky.
    Zero clipping into wheels or chassis.
    """
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(scale, scale)

    # Chassis flatbed (dark olive military green)
    # x from -160 (rear) to +170 (front cabin)
    rrect(ctx, -160, -10, 330, 42, 6)
    ctx.set_source_rgb(0.16, 0.22, 0.17)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.32, 0.42, 0.32)
    ctx.set_line_width(2.5)
    ctx.stroke()

    # Front Armored Driving Cabin (front right)
    ctx.move_to(80, -10)
    ctx.line_to(170, -10)
    ctx.line_to(170, -65)
    ctx.line_to(130, -75)
    ctx.line_to(80, -75)
    ctx.close_path()
    ctx.set_source_rgb(0.13, 0.18, 0.14)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.35, 0.48, 0.35)
    ctx.set_line_width(2.5)
    ctx.stroke()

    # Cabin Glass with cyan HUD reflection
    ctx.move_to(125, -70)
    ctx.line_to(165, -62)
    ctx.line_to(165, -40)
    ctx.line_to(125, -40)
    ctx.close_path()
    ctx.set_source_rgba(0.0, 0.85, 0.95, 0.7)
    ctx.fill()

    # Side window
    rrect(ctx, 88, -68, 30, 26, 4)
    ctx.set_source_rgba(0.0, 0.7, 0.85, 0.5)
    ctx.fill()

    # 4 Axles / 8 All-Terrain Heavy Combat Wheels (evenly spaced pairs)
    wheel_xs = [-130, -85, 50, 115]
    for wx in wheel_xs:
        # Wheel arch mudguard
        ctx.arc(wx, 32, 26, math.pi, 2 * math.pi)
        ctx.set_source_rgb(0.1, 0.14, 0.11)
        ctx.set_line_width(4)
        ctx.stroke()

        # Heavy tire
        circle(ctx, wx, 42, 22, (0.07, 0.07, 0.08), 1.0)
        # Steel Rim
        circle(ctx, wx, 42, 13, STEEL, 1.0)
        # Hub bolts
        circle(ctx, wx, 42, 5, GOLD, 1.0)

    # Rear Hydraulic Stabilizer Outrigger Pad (deployed behind rear axle)
    rrect(ctx, -172, 10, 10, 52, 2)
    ctx.set_source_rgb(0.25, 0.3, 0.35)
    ctx.fill()
    rrect(ctx, -180, 58, 26, 6, 2)
    ctx.set_source_rgb(0.45, 0.5, 0.55)
    ctx.fill()

    # Mid-Chassis Hydraulic Stabilizer (between front and rear axle sets)
    rrect(ctx, -18, 10, 10, 52, 2)
    ctx.set_source_rgb(0.25, 0.3, 0.35)
    ctx.fill()
    rrect(ctx, -26, 58, 26, 6, 2)
    ctx.set_source_rgb(0.45, 0.5, 0.55)
    ctx.fill()

    # Rear Canister Cradle & Elevation Mechanism
    # Pivot point is at x = -135, y = -12 (top of rear flatbed)
    px, py = -135, -12
    circle(ctx, px, py, 10, STEEL, 1.0)
    circle(ctx, px, py, 4, (0.1, 0.1, 0.1), 1.0)

    # Elevating Missile Canisters
    ctx.save()
    ctx.translate(px, py)
    ang = -math.radians(elevate * 65)  # Rotates UPWARDS into sky (0 to -65 deg)
    ctx.rotate(ang)

    # Hydraulic piston rod lifting the tubes
    if elevate > 0.05:
        line(ctx, [(30, 0), (60, 20 * elevate)], STEEL, 6)

    # Dual Massive Canister Cylinders (extending forward from x = 0 to 240)
    canister_len = 245
    canister_h = 20
    for dy in [-24, 4]:
        # Tube body
        rrect(ctx, 0, dy, canister_len, canister_h, 5)
        ctx.set_source_rgb(0.24, 0.28, 0.32)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.55, 0.65, 0.75)
        ctx.set_line_width(2)
        ctx.stroke()

        # Front Muzzle Cap (Orange / Saffron Band)
        rrect(ctx, canister_len - 25, dy, 25, canister_h, 3)
        ctx.set_source_rgb(1.0, 0.5, 0.1)
        ctx.fill()

        # Reinforcement structural ribs along canister
        for rx in [50, 110, 170]:
            rrect(ctx, rx, dy - 2, 8, canister_h + 4, 1)
            ctx.set_source_rgb(0.4, 0.48, 0.55)
            ctx.fill()

    # Reinforced Canister Base Mount
    rrect(ctx, -6, -28, 16, 56, 3)
    ctx.set_source_rgb(0.35, 0.42, 0.48)
    ctx.fill()

    # Stencil Text on top tube
    text(ctx, "DRDO PROJECT KUSHA", 100, -14, 11, (1, 1, 1), font=MONO, anchor="c")

    ctx.restore()
    ctx.restore()


# ============================================================
# SCENE 1: High vs Low Airspace Threat (50,000 ft vs 30m)
# ============================================================

class SceneHighLowThreat(Cued):
    def events(self, d):
        return [(0.4, "whoosh"), (2.5, "beep")]

    def draw(self, ctx, t, d):
        self.draw_bg(ctx, t, d)
        self.draw_fg(ctx, t, d)

    def draw_bg(self, ctx, t, d):
        # Top section: Dark Stratosphere (50,000 ft)
        g_strat = cairo.LinearGradient(0, 0, 0, 660)
        g_strat.add_color_stop_rgb(0, 0.02, 0.03, 0.08)
        g_strat.add_color_stop_rgb(1, 0.08, 0.12, 0.22)
        ctx.set_source(g_strat)
        ctx.rectangle(0, 0, W, 660)
        ctx.fill()

        # Altitude grid lines top
        line(ctx, [(60, 240), (W - 60, 240)], (0, 0.9, 1.0), 1.5, 0.25)
        text(ctx, "ALTITUDE: 50,000 FT // LOW-RCS ENVELOPE", 80, 210, 22, CYAN, font=MONO, a=0.85, anchor="l")

        # Bottom section: Mountain terrain & Low troposphere (30m)
        g_terr = cairo.LinearGradient(0, 660, 0, H)
        g_terr.add_color_stop_rgb(0, 0.10, 0.08, 0.14)
        g_terr.add_color_stop_rgb(1, 0.04, 0.02, 0.05)
        ctx.set_source(g_terr)
        ctx.rectangle(0, 660, W, H - 660)
        ctx.fill()

        # Jagged mountain silhouettes (sitting above bottom caption band)
        ctx.save()
        ctx.move_to(0, 1020)
        for mx, my in [(150, 930), (320, 960), (500, 910), (720, 950), (900, 890), (W, 940)]:
            ctx.line_to(mx, my)
        ctx.line_to(W, 1140)
        ctx.line_to(0, 1140)
        ctx.close_path()
        ctx.set_source_rgb(0.12, 0.09, 0.08)
        ctx.fill()
        ctx.restore()

        # Dividing radar telemetry bar
        line(ctx, [(40, 660), (W - 40, 660)], RED, 3, 0.8)
        text(ctx, "TERRAIN-HUGGING ALTITUDE: 30 METERS", 80, 695, 22, RED, font=MONO, a=0.85, anchor="l")

    def draw_fg(self, ctx, t, d):
        pr = t / d
        # Top Stealth Fighter moving right to left
        x_stealth = W * 0.75 - pr * 220
        y_stealth = 420 + math.sin(t * 2.5) * 15
        draw_stealth_jet(ctx, x_stealth, y_stealth, scale=1.35, angle=math.radians(-85))

        # Radar lock bracket on Stealth
        ctx.save()
        ctx.set_line_width(2.5)
        ctx.set_source_rgba(1.0, 0.2, 0.2, 0.8 + 0.2 * math.sin(t * 8))
        rrect(ctx, x_stealth - 70, y_stealth - 70, 140, 140, 8)
        ctx.stroke()
        text(ctx, "TGT: STEALTH J-20", x_stealth, y_stealth - 85, 20, RED, font=MONO, a=0.9, anchor="c")
        ctx.restore()

        # Bottom Cruise Missile skimming fast left to right in 820-880 altitude band
        x_cruise = 120 + pr * 750
        y_cruise = 840 + math.sin(t * 6.0) * 8
        draw_cruise_missile(ctx, x_cruise, y_cruise, scale=1.3, angle=math.radians(2))

        # Terrain radar clutter waves
        for r_clutter in range(3):
            cx = x_cruise - 100 - r_clutter * 80
            circle(ctx, cx, y_cruise + 30, 20 + (t * 40) % 50, (0.8, 0.4, 0.1), 0.3)


# ============================================================
# SCENE 2: DRDO Project Kusha Reveal
# ============================================================

class SceneKushaReveal(Cued):
    def events(self, d):
        return [(0.3, "whoosh"), (1.8, "boom")]

    def draw(self, ctx, t, d):
        self.draw_bg(ctx, t, d)
        self.draw_fg(ctx, t, d)

    def draw_bg(self, ctx, t, d):
        # Desert / Border twilight command base
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, 0.05, 0.08, 0.16)
        g.add_color_stop_rgb(0.6, 0.15, 0.12, 0.18)
        g.add_color_stop_rgb(1, 0.06, 0.04, 0.06)
        ctx.set_source(g)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()

        # Saffron & Cyan energy field in background
        ctx.save()
        glow(ctx, W * 0.5, 750, 450, SAFFRON, 0.25)
        glow(ctx, W * 0.5, 750, 250, CYAN, 0.20)
        ctx.restore()

        # Ground base
        rrect(ctx, 0, 950, W, H - 950, 0)
        ctx.set_source_rgb(0.10, 0.09, 0.11)
        ctx.fill()
        line(ctx, [(0, 950), (W, 950)], SAFFRON, 3, 0.6)

    def draw_fg(self, ctx, t, d):
        pr = min(1.0, t / 2.0)
        elev = ease_out_back(pr)

        # Rotating AESA Radar Mast on left
        rx, ry = 200, 800
        rrect(ctx, rx - 15, ry, 30, 150, 4)
        ctx.set_source_rgb(0.2, 0.25, 0.3)
        ctx.fill()
        # Rotating Dual-Band Antenna head
        ctx.save()
        ctx.translate(rx, ry)
        sweep_ang = t * 3.5
        ctx.scale(math.cos(sweep_ang), 1.0)
        rrect(ctx, -55, -40, 110, 45, 6)
        ctx.set_source_rgb(0.8, 0.85, 0.9)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.0, 0.9, 1.0)
        ctx.set_line_width(3)
        ctx.stroke()
        ctx.restore()

        # Pulsing radar waves into the sky
        for i in range(4):
            rw = 80 + ((t * 90 + i * 80) % 320)
            ctx.save()
            ctx.set_source_rgba(0, 0.9, 1.0, max(0.0, 1.0 - rw / 320))
            ctx.set_line_width(2.5)
            ctx.arc(rx, ry - 30, rw, -math.pi * 0.8, -math.pi * 0.2)
            ctx.stroke()
            ctx.restore()

        # Main Kusha 8x8 Launcher raising up (sitting firmly on ground line)
        draw_kusha_launcher(ctx, 640, 885, scale=1.45, elevate=elev)

        # Banner overlay
        rrect(ctx, W * 0.5 - 280, 240, 560, 100, 14)
        ctx.set_source_rgba(0.02, 0.05, 0.10, 0.88)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.9, 0.5, 0.1)
        ctx.set_line_width(2.5)
        ctx.stroke()

        text(ctx, "PROJECT KUSHA (LR-SAM)", W * 0.5, 275, 30, SAFFRON, anchor="c")
        text(ctx, "INDIA'S INDIGENOUS AIR DEFENCE SHIELD", W * 0.5, 315, 17, (1, 1, 1), font=MONO, a=0.85, anchor="c")


# ============================================================
# SCENE 3: Range Breakdown (350 KM Outer vs 150 KM Inner)
# ============================================================

class SceneRangeBreakdown(Cued):
    def events(self, d):
        return [(0.5, "beep"), (3.5, "whoosh"), (5.0, "boom")]

    def draw(self, ctx, t, d):
        self.draw_bg(ctx, t, d)
        self.draw_fg(ctx, t, d)

    def draw_bg(self, ctx, t, d):
        # Deep space / tactical C4I radar map
        ctx.set_source_rgb(0.015, 0.025, 0.05)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()

        # Concentric Radar Rings from base (W/2, 1050)
        bx, by = W * 0.5, 1050
        rings = [
            (350, 520, "350 KM // STEALTH & AWACS DOME", CYAN),
            (250, 370, "250 KM // FIGHTER INTERCEPT", GOLD),
            (150, 220, "150 KM // CRUISE MISSILE KILL ZONE", FIRE_ORANGE)
        ]
        ctx.save()
        for idx, (dist, rad, desc, col) in enumerate(rings):
            ctx.set_line_width(2.5)
            ctx.set_source_rgba(col[0], col[1], col[2], 0.35 + 0.15 * math.sin(t * 3.0 + idx))
            ctx.arc(bx, by, rad, -math.pi * 0.95, -math.pi * 0.05)
            ctx.stroke()

            # Range Label on the arc
            lx = bx + rad * math.cos(-math.pi * 0.72)
            ly = by + rad * math.sin(-math.pi * 0.72)
            text(ctx, desc, lx, ly, 18, col, font=MONO, a=0.9, anchor="l")
        ctx.restore()

        # Rotating tactical sweep line
        sweep_rad = -math.pi * 0.95 + (t * 0.8) % (math.pi * 0.9)
        ctx.save()
        ctx.move_to(bx, by)
        ctx.line_to(bx + 750 * math.cos(sweep_rad), by + 750 * math.sin(sweep_rad))
        ctx.set_source_rgba(0, 0.9, 1.0, 0.7)
        ctx.set_line_width(3)
        ctx.stroke()
        ctx.restore()

    def draw_fg(self, ctx, t, d):
        bx, by = W * 0.5, 1050

        # Outer target: Stealth fighter at 350 KM dome (well inside screen)
        sx = 330 + math.sin(t * 1.5) * 20
        sy = 560
        draw_stealth_jet(ctx, sx, sy, scale=1.0, angle=math.radians(105))
        circle(ctx, sx, sy, 40 + 8 * math.sin(t * 8), CYAN, 0.4)
        text(ctx, "350 KM: STEALTH J-20 LOCKED", sx, sy - 60, 20, CYAN, font=MONO, anchor="c")

        # Inner target: Low cruise missile intercepted at 150 KM
        cx = 720
        cy = 870
        # Missile explosion flash
        ex_p = (t * 2.0) % 1.0
        draw_cruise_missile(ctx, cx, cy, scale=0.95, angle=math.radians(170))
        glow(ctx, cx, cy, 60 + ex_p * 80, FIRE_ORANGE, 0.9 * (1.0 - ex_p))
        glow(ctx, cx, cy, 30 + ex_p * 40, (1.0, 0.9, 0.2), 1.0 * (1.0 - ex_p))
        text(ctx, "150 KM: CRUISE MISSILE KHAAK!", cx, cy + 50, 20, FIRE_ORANGE, font=MONO, anchor="c")

        # Central launcher icon at radar base
        draw_kusha_launcher(ctx, bx, by - 25, scale=0.85, elevate=0.85)


# ============================================================
# SCENE 4: CTA & Interactive Audience Poll
# ============================================================

class SceneCtaPoll(Cued):
    def events(self, d):
        return [(0.3, "whoosh"), (2.0, "pop")]

    def draw(self, ctx, t, d):
        self.draw_bg(ctx, t, d)
        self.draw_fg(ctx, t, d)

    def draw_bg(self, ctx, t, d):
        # High-tech command center background
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, 0.02, 0.04, 0.08)
        g.add_color_stop_rgb(1, 0.05, 0.08, 0.14)
        ctx.set_source(g)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()

        # Hexagonal grid pattern in background
        ctx.save()
        ctx.set_source_rgba(0, 0.9, 1.0, 0.08)
        ctx.set_line_width(1.5)
        for hx in range(100, W, 180):
            for hy in range(150, 900, 160):
                circle(ctx, hx, hy, 45, (0, 0.9, 1.0), 0.05)
        ctx.restore()

        # India Flag Glow in center
        ctx.save()
        glow(ctx, W * 0.5, 450, 320, SAFFRON, 0.25)
        glow(ctx, W * 0.5, 450, 160, INDIA_GREEN, 0.20)
        ctx.restore()

    def draw_fg(self, ctx, t, d):
        # Tactical Air Defense Badge / Shield Emblem
        ctx.save()
        ctx.translate(W * 0.5, 430)
        scale_pulse = 1.0 + 0.04 * math.sin(t * 4.0)
        ctx.scale(scale_pulse, scale_pulse)

        # Shield outline
        ctx.move_to(0, -140)
        ctx.line_to(110, -90)
        ctx.line_to(90, 60)
        ctx.curve_to(60, 130, 0, 170, 0, 170)
        ctx.curve_to(0, 170, -60, 130, -90, 60)
        ctx.line_to(-110, -90)
        ctx.close_path()
        ctx.set_source_rgb(0.08, 0.12, 0.20)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.95, 0.65, 0.15)
        ctx.set_line_width(6)
        ctx.stroke()

        # Ashoka Chakra inside shield
        ctx.set_source_rgb(0.1, 0.3, 0.8)
        ctx.arc(0, 10, 42, 0, 2 * math.pi)
        ctx.set_line_width(4)
        ctx.stroke()
        for sp in range(24):
            ang = sp * (2 * math.pi / 24)
            line(ctx, [(0, 10), (38 * math.cos(ang), 10 + 38 * math.sin(ang))], (0.1, 0.3, 0.8), 2)

        ctx.restore()

        # Interactive Poll UI Card
        py = 720
        rrect(ctx, W * 0.5 - 320, py, 640, 200, 16)
        ctx.set_source_rgba(0.02, 0.05, 0.10, 0.90)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.0, 0.9, 1.0)
        ctx.set_line_width(2.5)
        ctx.stroke()

        text(ctx, "POLL: KYA KUSHA GAME CHANGER HAI?", W * 0.5, py + 48, 28, GOLD, anchor="c")

        # Two Poll Option Pills: HAAN (Yes) vs NAA (No)
        # Button A: HAAN 98%
        rrect(ctx, W * 0.5 - 280, py + 85, 260, 75, 12)
        ctx.set_source_rgba(0.08, 0.65, 0.25, 0.45)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.2, 0.9, 0.4)
        ctx.set_line_width(2.5)
        ctx.stroke()
        text(ctx, "HAAN! (98%)", W * 0.5 - 150, py + 130, 26, (1, 1, 1), anchor="c")

        # Button B: NAA 2%
        rrect(ctx, W * 0.5 + 20, py + 85, 260, 75, 12)
        ctx.set_source_rgba(0.7, 0.15, 0.15, 0.35)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.9, 0.3, 0.3)
        ctx.set_line_width(2.5)
        ctx.stroke()
        text(ctx, "NAA (2%)", W * 0.5 + 150, py + 130, 26, (0.8, 0.8, 0.8), anchor="c")

        # Animated finger tap indicator on HAAN
        tap_x = W * 0.5 - 80 + math.sin(t * 5) * 10
        tap_y = py + 145
        circle(ctx, tap_x, tap_y, 16 + 6 * math.sin(t * 6), GOLD, 0.6)


SCENE_CLASSES = {
    "high_low_threat": SceneHighLowThreat,
    "kusha_reveal": SceneKushaReveal,
    "range_breakdown": SceneRangeBreakdown,
    "cta_poll": SceneCtaPoll,
}


UPLOAD = {
    "titles": [
        "Project Kusha: Stealth Jets Aur Cruise Missiles Ka Kaal! 🇮🇳🔥 #shorts",
        "50,000 Ft Par Stealth Aur 30M Par Cruise Missile Tabah! 🚀 #shorts",
        "DRDO Project Kusha Range Breakdown: 350 KM vs 150 KM! 🇮🇳 #shorts",
        "Why Project Kusha Is India's Ultimate Air Defence Shield? #shorts",
        "Kusha vs Stealth Fighters: India's Desi Iron Dome Explained! #shorts",
    ],
    "title": "Project Kusha: Stealth Jets Aur Cruise Missiles Ka Kaal! 🇮🇳🔥 #shorts",
    "thumb_text": "KUSHA AIR SHIELD",
    "queries": ["project kusha", "drdo project kusha", "kusha range breakdown"],
    "description": """Bharat ka apna desi air defence shield— DRDO Project Kusha range breakdown!
50,000 feet par udne wale stealth fighters se lekar zameen se sirf 30 meter upar chhupti cruise missiles tak, Kusha ka 3-tier radar aur missile network aasmaan ko abhedya banata hai.

Is Short mein:
• 350 KM Dual-Band AESA Radar: Stealth fighters (J-20) detection & lock
• 150 KM Agile Interceptor: Low-flying terrain-hugging cruise missiles interception
• 8x8 Heavy Mobile TEL Launcher aur indigenous C4I network

Kya Project Kusha Bharat ka abhedya kila banayega? Comment mein likhein - JAI HIND! 🇮🇳
Subscribe to RealityShift for high-tech defence breakdowns.

#Shorts #ProjectKusha #IndianAirForce
""",
    "tags": [
        "project kusha", "drdo project kusha", "kusha air defence", "indian air force",
        "kusha range breakdown", "s400 vs kusha", "stealth fighter radar", "cruise missile intercept",
        "reality shift", "defence shorts", "viral shorts"
    ],
    "hashtags": ["#Shorts", "#ProjectKusha", "#IndianAirForce"],
}


def thumbnail(ctx):
    """Generate high-CTR YouTube thumbnail cover with perfect composition and zero clutter."""
    # Dark tactical C4I radar background
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.02, 0.03, 0.08)
    g.add_color_stop_rgb(0.5, 0.06, 0.12, 0.20)
    g.add_color_stop_rgb(1, 0.02, 0.03, 0.06)
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()

    # Concentric tactical radar rings centered at base
    for r in [260, 480, 720]:
        circle(ctx, W * 0.5, 1400, r, CYAN, 0.07)

    # Tactical Ground Base line
    line(ctx, [(0, 1470), (W, 1470)], (0.15, 0.30, 0.25), 3, 0.6)

    # Big Kusha 8x8 Launcher sitting solidly on the ground line (no wheel dipping)
    draw_kusha_launcher(ctx, 480, 1405, scale=1.75, elevate=0.88)

    # Fiery Mach 5 Interceptor missile launching from canister into the sky
    # Canister tip is at approx (320, 1020)
    line(ctx, [(380, 1140), (290, 720)], (1.0, 0.6, 0.1), 8, 0.85)
    circle(ctx, 290, 720, 18, (1.0, 0.9, 0.3), 1.0)
    glow(ctx, 290, 720, 55, FIRE_ORANGE, 0.8)

    # Stealth jet (J-20) locked at top left (350 KM envelope)
    draw_stealth_jet(ctx, 290, 570, scale=1.45, angle=math.radians(110))
    circle(ctx, 290, 570, 70, RED, 0.4)
    rrect(ctx, 215, 495, 150, 150, 10)
    ctx.set_source_rgba(1.0, 0.2, 0.2, 0.9)
    ctx.set_line_width(3)
    ctx.stroke()
    text(ctx, "TGT: STEALTH J-20 (350 KM)", 290, 465, 22, RED, font=MONO, anchor="c")

    # Cruise missile speeding at middle right (150 KM envelope)
    draw_cruise_missile(ctx, 760, 940, scale=1.35, angle=math.radians(175))
    circle(ctx, 760, 940, 60, FIRE_ORANGE, 0.5)
    text(ctx, "LOW CRUISE MISSILE (150 KM)", 760, 875, 22, FIRE_ORANGE, font=MONO, anchor="c")

    # High-Impact Thumbnail Header Box - Centered with plenty of padding
    rrect(ctx, 80, 140, W - 160, 190, 20)
    ctx.set_source_rgba(0.02, 0.04, 0.08, 0.92)
    ctx.fill_preserve()
    ctx.set_source_rgb(1.0, 0.6, 0.1)
    ctx.set_line_width(4)
    ctx.stroke()

    # Perfectly centered texts using anchor="c"
    text(ctx, "PROJECT KUSHA", W * 0.5, 210, 64, GOLD, anchor="c")
    text(ctx, "350 KM VS 150 KM BREAKDOWN", W * 0.5, 280, 30, CYAN, font=MONO, anchor="c")


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


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.kusha_range")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))

