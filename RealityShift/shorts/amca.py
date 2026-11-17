"""Reality Shift Short: India's 5th Gen Stealth Fighter AMCA.

Topic: Project AMCA (Advanced Medium Combat Aircraft) - India's 5.5th Gen Stealth Fighter
Format: Vertical 1080x1920 (9:16) for YouTube Shorts
Audio: KikiVoice narrator audio (33.55s), aligned and split via Whisper
Visuals: Procedural Cairo animations, stealth faceted airframe, internal weapons bay,
         supersonic vapor cone, radar sweep, Astra BVR missile launch.
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

TOPIC = "AMCA 5TH GEN STEALTH FIGHTER"
OUTPUTS = {"edge": "amca_short.mp4"}
LEGO = {"header": "intel", "caption": "typewriter", "transition": "scan", "palette": "amber", "ending": "prompt"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.55
TAIL_PAD = 0.20
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 126
MUSIC_STYLE = "pulse"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 250

PAL = lego.PALETTES["amber"]
UI = PAL["ui"]
HI = PAL["hi"]
RED = PAL["alert"]
INK = PAL["ink"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
STEEL = hexc("#90A4AE")
DARK_STEEL = hexc("#1A2530")
STEALTH_GREY = hexc("#21262D")
STEALTH_DARK = hexc("#13171C")
COCKPIT_GOLD = hexc("#E5A93B")
SNOW_WHITE = hexc("#E8F1F5")
WHITE = (1.0, 1.0, 1.0)
FIRE_ORANGE = hexc("#FF5500")
GOLD = hexc("#FFD700")
HUD_GREEN = hexc("#00FF66")
CYAN = hexc("#00E5FF")
MONO = "Consolas"

SOURCES = [
    "Aeronautical Development Agency (ADA) & DRDO - AMCA Design & Wind Tunnel Envelope",
    "Indian Air Force (IAF) - 5th Generation Stealth Fighter Requirements & CCS Clearance",
    "Cabinet Committee on Security (CCS) - Approval of Rs 15,000 Crore for AMCA Prototype Development",
    "Gas Turbine Research Establishment (GTRE) - 110 kN Indigenous Supercruise Engine Program",
]

SPEC = [
    # Scene 1: 5th Gen Stealth Race Hook (J-20 vs F-35 vs AMCA)
    {"key": "hook_stealth", "accent": RED, "text": "5TH GEN STEALTH RACE",
     "visual": "China J-20 and US F-35 tactical silhouettes on radar HUD, AMCA emerges aggressively through clouds with glowing gold canopy",
     "vo": [("tell", [("चीन के पास जे-20 है,", "CHINA KE PAAS J-20 HAI,"),
                      ("अमेरिका के पास एफ-35...", "AMERICA KE PAAS F-35..."),
                      ("पर भारत का फिफ्थ जनरेशन स्टेल्थ फाइटर अमका", "PAR BHARAT KA 5TH GEN STEALTH FIGHTER AMCA"),
                      ("उनसे अलग क्यों है?", "UNSE ALAG KYUN HAI?")])]},

    # Scene 2: Radar Cross Section Bird Comparison
    {"key": "radar_rcs", "accent": GOLD, "text": "RADAR INVISIBILITY",
     "visual": "Green military radar scope scanning sky, bird RCS comparison, radar waves deflection by faceted stealth airframe, zero blip detected",
     "vo": [("tell", [("इसका रडार क्रॉस सेक्शन", "ISKA RADAR CROSS SECTION"),
                      ("एक छोटी चिड़िया जितना है,", "EK CHHOTI CHIDIYA JITNA HAI,"),
                      ("यानी दुश्मन के रडार पर", "YAANI DUSHMAN KE RADAR PAR"),
                      ("ये गायब रहता है!", "YE GAYAB REHTA HAI!")])]},

    # Scene 3: Mach 2 Supercruise & Internal Weapons Bay (15-18s Anti-Drop)
    {"key": "supercruise_bay", "accent": CYAN, "text": "MACH 2 SUPERCRUISE",
     "visual": "Supersonic vapor cone forming around AMCA wings at Mach 2, twin engine shock diamonds, belly bay door opens to reveal Astra missile",
     "vo": [("tell", [("बिना आफ्टरबर्नर के", "BINA AFTERBURNER KE"),
                      ("सुपरसोनिक स्पीड,", "SUPERSONIC SPEED,"),
                      ("और अंदर छुपे", "AUR ANDAR CHHUPE"),
                      ("घातक अस्त्र मिसाइल!", "GHATAK ASTRA MISSILE!")])]},

    # Scene 4: BVR Supersonic Strike
    {"key": "bvr_strike", "accent": FIRE_ORANGE, "text": "BEYOND VISUAL RANGE",
     "visual": "Astra Mk3 missile drops from internal bay, booster ignites with blinding flame, streaks at Mach 4.5, distant radar station explodes",
     "vo": [("tell", [("बॉर्डर पर दुश्मन को", "BORDER PAR DUSHMAN KO"),
                      ("भनक लगने से पहले ही,", "BHANAK LAGNE SE PEHLE HI,"),
                      ("अमका उसका खेल", "AMCA USKA KHEL"),
                      ("खत्म कर देगा!", "KHATAM KAR DEGA!")])]},

    # Scene 5: 3-Second Snap CTA
    {"key": "cta_poll", "accent": SAFFRON, "text": "MISSION AMCA 2030",
     "visual": "AMCA climbing into twilight sky with orange afterburner glow, Indian Air Force tricolor roundel, crisp engagement prompt",
     "vo": [("tell", [("क्या भारत को अमका जल्द तैनात करना चाहिए?", "KYA BHARAT KO AMCA JALD TAINAAT KARNA CHAHIYE?"),
                      ("कमेंट में जय हिंद लिखें", "COMMENT MEIN JAI HIND LIKHEIN"),
                      ("और सब्सक्राइब करें रियलिटी शिफ्ट!", "AUR SUBSCRIBE KAREIN REALITY SHIFT!")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "CHINA": RED, "J-20": RED, "AMERICA": CYAN, "F-35": CYAN,
    "BHARAT": SAFFRON, "5TH": GOLD, "GEN": GOLD, "STEALTH": HUD_GREEN,
    "FIGHTER": SAFFRON, "AMCA": GOLD, "RADAR": RED, "CROSS": RED,
    "SECTION": RED, "CHIDIYA": GOLD, "DUSHMAN": RED, "GAYAB": HUD_GREEN,
    "AFTERBURNER": FIRE_ORANGE, "SUPERSONIC": CYAN, "SPEED": CYAN,
    "ASTRA": FIRE_ORANGE, "MISSILE": FIRE_ORANGE, "BORDER": RED,
    "BHANAK": GOLD, "KHEL": RED, "KHATAM": RED, "TAINAAT": SAFFRON,
    "COMMENT": HI, "JAI": SAFFRON, "HIND": SAFFRON, "SUBSCRIBE": SAFFRON,
    "REALITY": CYAN, "SHIFT": CYAN
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
# PROCEDURAL DRAWING ROUTINES (AMCA Stealth Fighter & Tactical HUD)
# ============================================================

def draw_tactical_sky(ctx, t, night=True):
    """Deep tactical stratosphere sky with subtle rolling high-altitude clouds."""
    pat = cairo.LinearGradient(0, 0, 0, H)
    if night:
        pat.add_color_stop_rgb(0.0, 0.02, 0.04, 0.08)
        pat.add_color_stop_rgb(0.5, 0.05, 0.08, 0.14)
        pat.add_color_stop_rgb(1.0, 0.08, 0.12, 0.20)
    else:
        pat.add_color_stop_rgb(0.0, 0.03, 0.06, 0.12)
        pat.add_color_stop_rgb(0.6, 0.10, 0.18, 0.28)
        pat.add_color_stop_rgb(1.0, 0.25, 0.15, 0.12)
    ctx.set_source(pat)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()

    # Cloud streaks passing horizontally
    ctx.save()
    for ci in range(6):
        cy = 300 + ci * 240
        cx = ((t * (120 + ci * 35) + ci * 300) % (W + 600)) - 300
        g = cairo.LinearGradient(cx - 200, cy, cx + 200, cy)
        g.add_color_stop_rgba(0, 1, 1, 1, 0)
        g.add_color_stop_rgba(0.5, 0.6, 0.7, 0.85, 0.09)
        g.add_color_stop_rgba(1, 1, 1, 1, 0)
        ctx.set_source(g)
        ctx.rectangle(cx - 200, cy - 25, 400, 50)
        ctx.fill()
    ctx.restore()


def draw_hud_grid(ctx, t):
    """Futuristic aerospace HUD grid overlays with altitude tape and heading."""
    ctx.save()
    rgba(ctx, HUD_GREEN, 0.12)
    ctx.set_line_width(1.0)
    # Horizontal grid lines
    for gy in range(200, 1700, 180):
        line(ctx, [(80, gy), (W - 80, gy)], HUD_GREEN, 1.0, 0.10)
    # Center pitch ladder
    cy = 960
    for p in [-3, -2, -1, 1, 2, 3]:
        py = cy + p * 90
        line(ctx, [(440, py), (490, py)], HUD_GREEN, 1.5, 0.22)
        line(ctx, [(590, py), (640, py)], HUD_GREEN, 1.5, 0.22)
        text(ctx, f"{abs(p)*10}°", 400, py + 5, 14, HUD_GREEN, font=MONO, a=0.3)
    ctx.restore()


def draw_amca_fighter(ctx, x, y, s, t, bay_open=False, astra_missile=False,
                      afterburner=False, vapor_cone=False, bank_deg=0.0):
    """High-fidelity procedural 5th Gen AMCA Stealth Fighter.

    Faceted diamond-delta stealth wings, canted twin vertical stabilizers,
    gold-tinted radar-absorbent cockpit canopy, serrated trailing edges,
    and internal weapons bay mechanism.
    """
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if bank_deg != 0.0:
        ctx.rotate(math.radians(bank_deg))

    # Engine Afterburner Flame / Supercruise Shock Diamonds
    if afterburner:
        for ex in [-55, 55]:
            # Outer Mach flame glow
            pat = cairo.RadialGradient(ex, 280, 10, ex, 350, 120)
            pat.add_color_stop_rgba(0.0, 1.0, 0.9, 0.4, 0.95)
            pat.add_color_stop_rgba(0.3, 1.0, 0.4, 0.0, 0.8)
            pat.add_color_stop_rgba(0.7, 0.0, 0.6, 1.0, 0.4)
            pat.add_color_stop_rgba(1.0, 0.0, 0.2, 0.8, 0.0)
            ctx.set_source(pat)
            ctx.rectangle(ex - 45, 270, 90, 160)
            ctx.fill()
            # Supersonic shock diamond cores
            for k in range(3):
                sy = 290 + k * 35 + math.sin(t * 40 + k) * 3
                ctx.move_to(ex, sy - 12)
                ctx.line_to(ex + 14, sy)
                ctx.line_to(ex, sy + 12)
                ctx.line_to(ex - 14, sy)
                ctx.close_path()
                rgba(ctx, (1.0, 1.0, 1.0), 0.85)
                ctx.fill()

    # Supersonic Vapor Cone (Prandtl-Glauert Singularity)
    if vapor_cone:
        v_alpha = 0.55 + 0.15 * math.sin(t * 18.0)
        pat = cairo.LinearGradient(0, -60, 0, 120)
        pat.add_color_stop_rgba(0.0, 1, 1, 1, 0)
        pat.add_color_stop_rgba(0.5, 0.8, 0.95, 1.0, v_alpha)
        pat.add_color_stop_rgba(1.0, 1, 1, 1, 0)
        ctx.set_source(pat)
        ctx.move_to(0, -70)
        ctx.line_to(220, 130)
        ctx.line_to(-220, 130)
        ctx.close_path()
        ctx.fill()

    # Soft drop shadow
    ctx.save()
    ctx.scale(1.0, 0.35)
    circle(ctx, 0, 320, 240, (0, 0, 0), 0.4)
    ctx.restore()

    # 1. Main Stealth Fuselage & Diamond Wings Planform
    ctx.move_to(0, -220)          # Sharp radar-deflecting nose
    ctx.line_to(45, -130)         # Chined forebody right
    ctx.line_to(70, -40)          # Leading-edge root extension (LERX)
    ctx.line_to(260, 120)         # Right wingtip leading edge
    ctx.line_to(240, 160)         # Wingtip edge
    ctx.line_to(110, 175)         # Trailing edge right
    ctx.line_to(65, 260)          # Right engine nozzle outer edge
    ctx.line_to(20, 275)          # Right nozzle inner
    ctx.line_to(0, 260)           # Beaver tail center
    ctx.line_to(-20, 275)         # Left nozzle inner
    ctx.line_to(-65, 260)         # Left engine nozzle outer edge
    ctx.line_to(-110, 175)        # Trailing edge left
    ctx.line_to(-240, 160)        # Wingtip edge
    ctx.line_to(-260, 120)        # Left wingtip leading edge
    ctx.line_to(-70, -40)         # LERX left
    ctx.line_to(-45, -130)        # Chined forebody left
    ctx.close_path()

    # Tactical Stealth Carbon-Composite Gradient
    g = cairo.LinearGradient(0, -220, 0, 270)
    g.add_color_stop_rgb(0.0, 0.18, 0.22, 0.26)    # Radar-absorbent nose cone
    g.add_color_stop_rgb(0.4, 0.12, 0.15, 0.19)    # Mid-body stealth slate
    g.add_color_stop_rgb(1.0, 0.07, 0.09, 0.12)    # Dark composite tail
    ctx.set_source(g)
    ctx.fill_preserve()

    # Sharp metallic edge sheen
    ctx.set_line_width(2.5)
    rgba(ctx, (0.45, 0.58, 0.70), 0.7)
    ctx.stroke()

    # 2. Canted Twin Vertical Stabilizers (V-Tail)
    # Right canted fin
    ctx.save()
    ctx.move_to(60, 90)
    ctx.line_to(135, 230)
    ctx.line_to(95, 245)
    ctx.line_to(45, 140)
    ctx.close_path()
    rgba(ctx, (0.10, 0.13, 0.17), 0.95)
    ctx.fill_preserve()
    ctx.set_line_width(1.5)
    rgba(ctx, (0.35, 0.48, 0.60), 0.8)
    ctx.stroke()
    # Left canted fin
    ctx.move_to(-60, 90)
    ctx.line_to(-135, 230)
    ctx.line_to(-95, 245)
    ctx.line_to(-45, 140)
    ctx.close_path()
    rgba(ctx, (0.10, 0.13, 0.17), 0.95)
    ctx.fill_preserve()
    ctx.set_line_width(1.5)
    rgba(ctx, (0.35, 0.48, 0.60), 0.8)
    ctx.stroke()
    ctx.restore()

    # 3. Cockpit Canopy with Gold-Tinted Indium Tin Oxide (ITO) Stealth Coating
    pat_canopy = cairo.LinearGradient(0, -120, 0, -20)
    pat_canopy.add_color_stop_rgba(0.0, 0.95, 0.75, 0.25, 0.95)  # Gold reflection
    pat_canopy.add_color_stop_rgba(0.5, 0.55, 0.38, 0.10, 0.90)  # Dark amber tint
    pat_canopy.add_color_stop_rgba(1.0, 0.15, 0.12, 0.08, 0.95)
    ctx.set_source(pat_canopy)
    ell(ctx, 0, -70, 20, 52)
    ctx.fill_preserve()
    ctx.set_line_width(2.0)
    rgba(ctx, (1.0, 0.88, 0.45), 0.8)
    ctx.stroke()

    # Pilot HUD Silhouette inside canopy
    circle(ctx, 0, -82, 7, (0.1, 0.15, 0.2), 0.9)
    line(ctx, [(0, -68), (0, -50)], (0.1, 0.15, 0.2), 10, 0.9)
    circle(ctx, 0, -84, 11, HUD_GREEN, 0.25)

    # 4. Indian Air Force Tricolor Roundel on Wings
    for rx, ry in [(160, 130), (-160, 130)]:
        circle(ctx, rx, ry, 18, SAFFRON, 0.9)
        circle(ctx, rx, ry, 12, WHITE, 0.9)
        circle(ctx, rx, ry, 6, INDIA_GREEN, 0.9)

    # 5. Internal Weapons Bay (Belly Doors & Astra BVR Missile)
    if bay_open:
        # Open weapons bay cavity
        rrect(ctx, -38, 10, 76, 120, 8)
        rgba(ctx, hexc("#080B0E"), 0.98)
        ctx.fill()
        rrect(ctx, -38, 10, 76, 120, 8)
        rgba(ctx, (0.3, 0.4, 0.5), 0.9)
        ctx.set_line_width(2.0)
        ctx.stroke()

        # Twin angled open bay doors
        # Left door
        line(ctx, [(-38, 10), (-62, 25), (-62, 115), (-38, 130)], hexc("#1C232B"), 4, 0.95)
        # Right door
        line(ctx, [(38, 10), (62, 25), (62, 115), (38, 130)], hexc("#1C232B"), 4, 0.95)

        # Astra BVR Missile mounted inside or launching
        if astra_missile:
            m_drop = min(90.0, (t * 80.0) % 120.0)
            ctx.save()
            ctx.translate(0, 70 + m_drop)
            # White missile body
            rrect(ctx, -6, -45, 12, 90, 4)
            rgba(ctx, (0.95, 0.95, 0.95), 0.95)
            ctx.fill()
            # Golden RF seeker radome
            ctx.move_to(-6, -45)
            ctx.line_to(0, -60)
            ctx.line_to(6, -45)
            ctx.close_path()
            rgba(ctx, GOLD, 0.95)
            ctx.fill()
            # Control fins
            line(ctx, [(-14, -20), (14, -20)], (0.3, 0.3, 0.3), 3, 0.9)
            line(ctx, [(-16, 35), (16, 35)], (0.3, 0.3, 0.3), 3, 0.9)
            # Rocket plume if dropped past bay
            if m_drop > 35:
                pat_p = cairo.RadialGradient(0, 45, 2, 0, 75, 30)
                pat_p.add_color_stop_rgba(0.0, 1.0, 1.0, 0.8, 0.95)
                pat_p.add_color_stop_rgba(0.4, 1.0, 0.4, 0.0, 0.8)
                pat_p.add_color_stop_rgba(1.0, 1.0, 0.1, 0.0, 0.0)
                ctx.set_source(pat_p)
                ctx.arc(0, 60, 25, 0, 2 * math.pi)
                ctx.fill()
            ctx.restore()
    else:
        # Closed bay door serrations
        line(ctx, [(-28, 15), (-28, 125)], (0.28, 0.36, 0.45), 1.5, 0.6)
        line(ctx, [(28, 15), (28, 125)], (0.28, 0.36, 0.45), 1.5, 0.6)

    # 6. Wingtip Formation Strips
    line(ctx, [(240, 130), (250, 150)], CYAN, 2.5, 0.9)
    line(ctx, [(-240, 130), (-250, 150)], CYAN, 2.5, 0.9)

    ctx.restore()


def draw_radar_scope(ctx, x, y, r, t, sweep=True, bird_blip=False, amca_invisible=True):
    """Green military PPI radar display comparing RCS blips."""
    ctx.save()
    ctx.translate(x, y)

    # Scope bezel
    circle(ctx, 0, 0, r + 15, hexc("#10151C"), 0.95)
    circle(ctx, 0, 0, r + 15, (0.3, 0.4, 0.5), 0.8)
    ctx.set_line_width(3.0)
    ctx.stroke()

    # Scope display background
    circle(ctx, 0, 0, r, hexc("#021208"), 0.95)
    circle(ctx, 0, 0, r, HUD_GREEN, 0.8)
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Range rings
    for ring_i in [0.3, 0.6, 0.85]:
        circle(ctx, 0, 0, r * ring_i, HUD_GREEN, 0.25)
        ctx.set_line_width(1.0)
        ctx.stroke()

    # Crosshairs
    line(ctx, [(-r, 0), (r, 0)], HUD_GREEN, 1.0, 0.25)
    line(ctx, [(0, -r), (0, r)], HUD_GREEN, 1.0, 0.25)

    # Rotating radar sweep beam
    if sweep:
        ang = (t * 2.5) % (2 * math.pi)
        pat = cairo.RadialGradient(0, 0, 5, 0, 0, r)
        pat.add_color_stop_rgba(0, 0.0, 1.0, 0.4, 0.45)
        pat.add_color_stop_rgba(1, 0.0, 1.0, 0.4, 0.05)
        ctx.set_source(pat)
        ctx.move_to(0, 0)
        ctx.arc(0, 0, r, ang - 0.45, ang)
        ctx.close_path()
        ctx.fill()
        line(ctx, [(0, 0), (r * math.cos(ang), r * math.sin(ang))], HUD_GREEN, 2.0, 0.85)

    # Bird Blip (Small pulsing dot detected on screen)
    if bird_blip:
        bx, by = -r * 0.45, -r * 0.35
        circle(ctx, bx, by, 6, GOLD, 0.9)
        circle(ctx, bx, by, 14 + 4 * math.sin(t * 8), GOLD, 0.3)
        text(ctx, "BIRD / 0.01 m²", bx - 40, by - 18, 14, GOLD, font=MONO)

    # AMCA Radar Cross Section (Zero return / stealth absorbed)
    if amca_invisible:
        ax, ay = r * 0.40, r * 0.25
        # Ghost outline indicating no return
        circle(ctx, ax, ay, 22, (1.0, 0.2, 0.2), 0.35 + 0.15 * math.sin(t * 6))
        ctx.set_line_width(1.5)
        ctx.stroke()
        text(ctx, "AMCA: NO BLIP", ax - 50, ay + 36, 14, HUD_GREEN, font=MONO)
        text(ctx, "RCS: 0.0001 m²", ax - 50, ay + 54, 14, (1.0, 0.8, 0.2), font=MONO)

    ctx.restore()


# ============================================================
# SCENE CLASSES (Strictly synchronized to KikiVoice 5 lines)
# ============================================================

class HookStealthScene(Cued):
    """Scene 1: China J-20 & US F-35 on tactical HUD; AMCA emerges aggressively."""
    def beats(self, d):
        c = self.cue
        return {
            "china": c("J-20", 0.6),
            "america": c("F-35", d * 0.35),
            "amca": c("AMCA", d * 0.65)
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["china"], "alarm"), (b["america"], "beep"), (b["amca"], "whoosh")]

    def draw(self, ctx, t, d):
        draw_tactical_sky(ctx, t, night=True)
        draw_hud_grid(ctx, t)

        # Tactical comparison boxes at top
        rrect(ctx, 80, 260, 420, 110, 12)
        rgba(ctx, hexc("#1A0C0E"), 0.85)
        ctx.fill()
        rrect(ctx, 80, 260, 420, 110, 12)
        rgba(ctx, RED, 0.85)
        ctx.set_line_width(2.0)
        ctx.stroke()
        text(ctx, "CHINA J-20", 290, 305, 26, RED, font=MONO, bold=True)
        text(ctx, "HEAVY STEALTH", 290, 340, 20, (0.8, 0.8, 0.8), font=MONO)

        rrect(ctx, 580, 260, 420, 110, 12)
        rgba(ctx, hexc("#0C1520"), 0.85)
        ctx.fill()
        rrect(ctx, 580, 260, 420, 110, 12)
        rgba(ctx, CYAN, 0.85)
        ctx.set_line_width(2.0)
        ctx.stroke()
        text(ctx, "US F-35", 790, 305, 26, CYAN, font=MONO, bold=True)
        text(ctx, "LIGHT STEALTH", 790, 340, 20, (0.8, 0.8, 0.8), font=MONO)

        # AMCA sweeps into screen from bottom center with intense tactical presence
        zoom = 0.85 + 0.15 * math.sin(t * 1.5)
        sway = math.sin(t * 2.2) * 25
        draw_amca_fighter(ctx, 540 + sway, 1020, zoom, t, afterburner=True, vapor_cone=False, bank_deg=-sway * 0.4)


class RadarRcsScene(Cued):
    """Scene 2: Military Radar Scope sweeping, Bird RCS comparison; AMCA undetected."""
    def beats(self, d):
        c = self.cue
        return {
            "radar": c("RADAR", 0.5),
            "chidiya": c("CHIDIYA", d * 0.4),
            "gayab": c("GAYAB", d * 0.75)
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["radar"], "tick"), (b["chidiya"], "beep"), (b["gayab"], "zap")]

    def draw(self, ctx, t, d):
        draw_tactical_sky(ctx, t, night=True)

        # Large center radar scope
        draw_radar_scope(ctx, 540, 720, 360, t, sweep=True, bird_blip=True, amca_invisible=True)

        # AMCA passing in high-speed tactical flyover below radar scope
        fly_x = 200 + (t * 180) % (W + 200)
        fly_y = 1380 + math.sin(t * 3.0) * 15
        draw_amca_fighter(ctx, fly_x, fly_y, 0.72, t, afterburner=False, bank_deg=12.0)


class SupercruiseBayScene(Cued):
    """Scene 3: Mach 2 Supercruise & Internal Weapons Bay Open (The 15-18s Anti-Drop)."""
    def beats(self, d):
        c = self.cue
        return {
            "afterburner": c("AFTERBURNER", 0.6),
            "speed": c("SUPERSONIC", d * 0.35),
            "astra": c("ASTRA", d * 0.7)
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["afterburner"], "whoosh"), (b["speed"], "zap"), (b["astra"], "kaching")]

    def draw(self, ctx, t, d):
        draw_tactical_sky(ctx, t, night=False)
        draw_hud_grid(ctx, t)

        # Telemetry Card top
        rrect(ctx, 160, 240, 760, 95, 12)
        rgba(ctx, hexc("#0C1520"), 0.90)
        ctx.fill()
        rrect(ctx, 160, 240, 760, 95, 12)
        rgba(ctx, CYAN, 0.90)
        ctx.set_line_width(2.5)
        ctx.stroke()
        text(ctx, "SUPERCRUISE: MACH 2.05", 540, 285, 30, CYAN, font=MONO, bold=True)
        text(ctx, "INTERNAL WEAPONS BAY ARMED", 540, 318, 18, GOLD, font=MONO)

        # AMCA facing camera, internal weapons bay wide open with Astra BVR missile
        draw_amca_fighter(ctx, 540, 940, 1.25, t, bay_open=True, astra_missile=True,
                          afterburner=True, vapor_cone=True, bank_deg=math.sin(t * 1.5) * 5)


class BvrStrikeScene(Cued):
    """Scene 4: Astra BVR Missile supersonic strike; enemy ground radar eliminated."""
    def beats(self, d):
        c = self.cue
        return {
            "border": c("BORDER", 0.5),
            "bhanak": c("BHANAK", d * 0.35),
            "khatam": c("KHATAM", d * 0.75)
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["border"], "alarm"), (b["bhanak"], "whoosh"), (b["khatam"], "boom")]

    def draw(self, ctx, t, d):
        draw_tactical_sky(ctx, t, night=False)

        # AMCA banking aggressively in top corner after firing
        draw_amca_fighter(ctx, 360, 520, 0.78, t, afterburner=True, bank_deg=-22.0)

        # Astra missile flying towards horizon target
        m_t = (t * 1.4) % 2.5
        mx = 360 + m_t * 220
        my = 560 + m_t * 280
        ctx.save()
        ctx.translate(mx, my)
        ctx.rotate(math.atan2(280, 220))
        # Missile rocket plume
        pat = cairo.RadialGradient(-40, 0, 5, -80, 0, 70)
        pat.add_color_stop_rgba(0.0, 1.0, 1.0, 0.8, 0.95)
        pat.add_color_stop_rgba(0.4, 1.0, 0.4, 0.0, 0.8)
        pat.add_color_stop_rgba(1.0, 1.0, 0.1, 0.0, 0.0)
        ctx.set_source(pat)
        ctx.arc(-50, 0, 35, 0, 2 * math.pi)
        ctx.fill()
        # White body
        rrect(ctx, -30, -8, 60, 16, 4)
        rgba(ctx, (0.95, 0.95, 0.95), 0.95)
        ctx.fill()
        ctx.restore()

        # Horizon impact explosion at bottom right
        if m_t > 1.2:
            ex_alpha = min(1.0, (m_t - 1.2) * 3.0)
            pat_ex = cairo.RadialGradient(820, 1380, 10, 820, 1380, 180)
            pat_ex.add_color_stop_rgba(0.0, 1.0, 1.0, 0.9, 0.95 * ex_alpha)
            pat_ex.add_color_stop_rgba(0.3, 1.0, 0.6, 0.1, 0.85 * ex_alpha)
            pat_ex.add_color_stop_rgba(0.7, 0.8, 0.1, 0.0, 0.5 * ex_alpha)
            pat_ex.add_color_stop_rgba(1.0, 0.2, 0.05, 0.0, 0.0)
            ctx.set_source(pat_ex)
            ctx.arc(820, 1380, 190, 0, 2 * math.pi)
            ctx.fill()
            text(ctx, "TARGET DESTROYED", 820, 1420, 24, GOLD, font=MONO, bold=True)


class CtaPollScene(Cued):
    """Scene 5: 3-Second Snap CTA: AMCA climbing into sunset; comment Jai Hind."""
    def beats(self, d):
        c = self.cue
        return {
            "tainaat": c("TAINAAT", 0.5),
            "jaihind": c("HIND", d * 0.4),
            "subscribe": c("SUBSCRIBE", d * 0.75)
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["tainaat"], "shimmer"), (b["jaihind"], "ghanti"), (b["subscribe"], "shimmer")]

    def draw(self, ctx, t, d):
        draw_tactical_sky(ctx, t, night=False)
        draw_hud_grid(ctx, t)

        # AMCA climbing vertically with twin orange plumes
        climb_y = 1180 - (t * 70) % 500
        draw_amca_fighter(ctx, 540, climb_y, 0.95, t, afterburner=True, vapor_cone=True, bank_deg=-8.0)


SCENE_CLASSES = {
    "hook_stealth": HookStealthScene,
    "radar_rcs": RadarRcsScene,
    "supercruise_bay": SupercruiseBayScene,
    "bvr_strike": BvrStrikeScene,
    "cta_poll": CtaPollScene,
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
        "China-US Ke Hosh Udane Wala Bharat Ka AMCA Fighter! 🇮🇳🔥 #shorts",
        "Radar Par Chidiya Jaisa Dikhega Bharat Ka AMCA! 😱 #shorts",
        "AMCA 5th Gen Stealth Fighter: India Ka Superweapon! 🇮🇳 #shorts",
        "Bina Radar Par Dikhe Dushman Tabah: AMCA Fighter #shorts",
        "Why India Rejected Russian Su-57 For Desi AMCA? #shorts",
    ],
    "title": "China-US Ke Hosh Udane Wala Bharat Ka AMCA Fighter! 🇮🇳🔥 #shorts",
    "thumb_text": "AMCA 5TH GEN STEALTH",
    "queries": ["amca fighter", "india 5th gen fighter", "amca vs j20"],
    "description": """Bharat ka apna 5th Generation Stealth Fighter AMCA (Advanced Medium Combat Aircraft) aasmaan mein aane ko taiyar hai!
China ke J-20 aur America ke F-35 ko takkar dene wala AMCA radar par ek chhoti chidiya jitna dikhta hai, yaani dushman ke radar par poori tarah gayab!

Is Short mein:
• Supercruise bina afterburner ke Mach 2 speed
• Radar Cross Section (RCS) smaller than a bird (0.0001 m²)
• Internal weapons bay se Astra Mk3 BVR missile strike
• Advanced AESA radar aur indigenous stealth composite body

Kya Bharat ko AMCA jald se jald deploy karna chahiye? Comment mein likhein - JAI HIND! 🇮🇳
Subscribe to RealityShift for high-tech defence breakdowns.

#Shorts #AMCA #IndianAirForce #DRDO
""",
    "tags": [
        "amca fighter", "amca 5th gen", "drdo amca", "india stealth fighter",
        "amca vs j20", "amca vs f35", "indian air force", "hal amca",
        "reality shift", "defence shorts", "viral shorts"
    ],
    "hashtags": ["#Shorts", "#AMCA", "#IndianAirForce", "#DRDO"],
}


def thumbnail(ctx):
    """High-CTR YouTube Shorts cover for AMCA."""
    draw_tactical_sky(ctx, 1.0, night=True)
    draw_hud_grid(ctx, 1.0)
    # Center AMCA with intense afterburners
    draw_amca_fighter(ctx, 540, 960, 1.45, 0.5, afterburner=True, vapor_cone=True)

    # High-impact typography
    text(ctx, "AMCA 5TH GEN", 540, 290, 110, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "RADAR SE GAYAB?", 540, 420, 80, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, CYAN, a=0.85)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.amca")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
