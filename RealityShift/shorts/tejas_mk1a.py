"""Reality Shift Short: Tejas Mk 1A — BVR Combat & AESA Radar Dominance.

Topic: Can HAL Tejas Mk 1A Beat Neighboring Fighter Jets In Beyond Visual Range (BVR) Combat?
Format: Vertical 1080x1920 (9:16) for YouTube Shorts
Audio: KikiVoice narrator audio (~21.0s), aligned and split via Whisper
Visuals: Compound delta wing Tejas Mk 1A, AESA active phased array radar beam sweep,
         Electronic warfare jammer scrambling enemy radar, Mach 4.5 Astra BVR missile launch.
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

TOPIC = "TEJAS MK 1A BVR RADAR COMBAT"
OUTPUTS = {"edge": "tejas_mk1a_short.mp4"}
LEGO = {"header": "intel", "caption": "chip", "transition": "shutter", "palette": "amber", "ending": "prompt"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.55
TAIL_PAD = 0.20
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 132
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
AESA_GOLD = hexc("#FFD54F")
CYAN = hexc("#00E5FF")
WHITE = (1.0, 1.0, 1.0)
FIRE_ORANGE = hexc("#FF5500")
GOLD = hexc("#FFD700")
COCKPIT_GOLD = hexc("#E5A93B")
SKY_DARK = hexc("#07101E")
MONO = "Consolas"

SOURCES = [
    "Hindustan Aeronautics Limited (HAL) & Aeronautical Development Agency (ADA) - Tejas Mk 1A Avionics, EL/M-2052 / Uttam AESA Radar & EW Suite Specifications.",
    "Defence Research and Development Organisation (DRDO) - Astra Mk-1 and Mk-2 Beyond Visual Range Air-to-Air Missile (BVRAAM) flight clearance on Tejas (PIB / MoD).",
    "Indian Air Force (IAF) - Operational BVR combat evaluation: small Radar Cross Section (RCS ~0.5m²) and electronic counter-countermeasures (ECCM) vs regional competitors (Jane's Defence).",
]

SPEC = [
    # Scene 1: BVR 100 KM Hook
    {"key": "bvr_hook", "accent": RED, "text": "100 KM BVR STRIKE ZONE",
     "visual": "Long-range tactical radar HUD showing distant enemy blip at 100+ km; Tejas Mk 1A delta fighter cruising undetected in stratosphere",
     "vo": [("tell", [("सोचो—", "SOCHO —"),
                      ("सौ किलोमीटर दूर से ही", "100 KM DOOR SE HI"),
                      ("बिना दिखे", "BINA DIKHE"),
                      ("दुश्मन फाइटर का", "DUSHMAN FIGHTER KA"),
                      ("गेम बजा देना!", "GAME BAJA DENA!")])]},

    # Scene 2: AESA Radar & Electronic Warfare Jammer
    {"key": "aesa_radar_jammer", "accent": GOLD, "text": "AESA RADAR // EW JAMMER",
     "visual": "Tejas Mk 1A nose cone AESA radar emitting focused golden multi-target tracking beams; Angad EW jammer pod blinding enemy radar",
     "vo": [("tell", [("जवाब है— हां!", "JAWAB HAI — HAAN!"),
                      ("इसके नए एईएसए रडार", "ISKE NAYE AESA RADAR"),
                      ("और जैमर के आगे", "AUR JAMMER KE AAGE"),
                      ("दुश्मन का रडार", "DUSHMAN KA RADAR"),
                      ("अंधा हो जाता है!", "ANDHA HO JATA HAI!")])]},

    # Scene 3: Mach 4.5 Astra BVR Missile Strike
    {"key": "astra_bvr_strike", "accent": FIRE_ORANGE, "text": "MACH 4.5 ASTRA STRIKE",
     "visual": "Underwing pylon drops Astra BVR missile; booster ignites with brilliant flame trail; supersonic interception destroys enemy fighter",
     "vo": [("tell", [("और जैसे ही ये देसी", "AUR JAISE HI YE DESI"),
                      ("अस्त्र मिसाइल दागता है,", "ASTRA MISSILE DAAGTA HAI,"),
                      ("सुपरसोनिक स्पीड से", "SUPERSONIC SPEED SE"),
                      ("बॉर्डर पार", "BORDER PAAR"),
                      ("खेल खत्म!", "KHEL KHATAM!")])]},

    # Scene 4: Infinite Loop CTA & Prompt
    {"key": "cta_prompt", "accent": SAFFRON, "text": "TEJAS MK 1A DOMINANCE",
     "visual": "Tejas Mk 1A climbing aggressively with twin orange afterburners into golden sunset; tricolor wingtips; interactive comment prompt",
     "vo": [("tell", [("यानी डॉगफाइट की", "YAANI DOGFIGHT KI"),
                      ("नौबत ही नहीं आएगी!", "NAUBAT HI NAHI AAYEGI!"),
                      ("क्या तेजस सबसे धाकड़ है?", "KYA TEJAS SABSE DHAKAD HAI?"),
                      ("कमेंट में बताओ!", "COMMENT MEIN BATAO!")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "SOCHO": HI, "100": CYAN, "KM": CYAN, "DOOR": CYAN, "BINA": GOLD, "DIKHE": GOLD,
    "DUSHMAN": RED, "FIGHTER": RED, "GAME": RED, "BAJA": RED,
    "JAWAB": HI, "HAAN": INDIA_GREEN, "AESA": GOLD, "RADAR": AESA_GOLD,
    "JAMMER": CYAN, "ANDHA": RED, "DESI": SAFFRON, "ASTRA": FIRE_ORANGE,
    "MISSILE": FIRE_ORANGE, "SUPERSONIC": CYAN, "SPEED": CYAN, "BORDER": RED,
    "KHEL": RED, "KHATAM": RED, "DOGFIGHT": RED, "NAUBAT": GOLD,
    "TEJAS": SAFFRON, "DHAKAD": GOLD, "COMMENT": HI, "BATAO": HI
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
# PROCEDURAL DRAWING ROUTINES (Tejas Mk 1A Delta Wing & Avionics)
# ============================================================

def draw_tejas_fighter(ctx, x, y, scale=1.0, angle=0.0, afterburner=False, vapor=False):
    """Draw HAL Tejas Mk 1A compound delta-wing fighter with pylons & Astra missile."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(angle)
    ctx.scale(scale, scale)

    # Supersonic Vapor Cone
    if vapor:
        ctx.save()
        g_vap = cairo.LinearGradient(-80, 0, 40, 0)
        g_vap.add_color_stop_rgba(0, 1, 1, 1, 0.4)
        g_vap.add_color_stop_rgba(1, 0, 0.8, 1, 0.0)
        ctx.set_source(g_vap)
        ctx.move_to(30, 0)
        ctx.line_to(-120, -75)
        ctx.line_to(-100, 0)
        ctx.line_to(-120, 75)
        ctx.close_path()
        ctx.fill()
        ctx.restore()

    # Afterburner Plume
    if afterburner:
        ctx.save()
        g_fire = cairo.LinearGradient(-75, 0, -170, 0)
        g_fire.add_color_stop_rgb(0, 1.0, 0.9, 0.4)
        g_fire.add_color_stop_rgb(0.4, 1.0, 0.4, 0.1)
        g_fire.add_color_stop_rgba(1, 0.8, 0.1, 0.0, 0.0)
        ctx.set_source(g_fire)
        ctx.move_to(-75, -12)
        ctx.line_to(-175, 0)
        ctx.line_to(-75, 12)
        ctx.close_path()
        ctx.fill()
        # Mach diamonds
        for mx in [-100, -125, -150]:
            circle(ctx, mx, 0, 5, (1.0, 1.0, 0.9), 0.9)
        ctx.restore()

    # Compound Delta Wing (Tailless delta silhouette)
    # Wing root starts around x = -10, sweeps back to x = -70, span out to y = +/- 78
    ctx.move_to(110, 0)       # Radome tip
    ctx.line_to(55, 14)       # Forward fuselage
    ctx.line_to(10, 24)       # Wing root start
    ctx.line_to(-65, 82)      # Wingtip right
    ctx.line_to(-75, 80)      # Wingtip edge
    ctx.line_to(-72, 22)      # Trailing edge right
    ctx.line_to(-75, 12)      # Exhaust nozzle right
    ctx.line_to(-75, -12)     # Exhaust nozzle left
    ctx.line_to(-72, -22)     # Trailing edge left
    ctx.line_to(-75, -80)     # Wingtip edge left
    ctx.line_to(-65, -82)     # Wingtip left
    ctx.line_to(10, -24)      # Wing root left
    ctx.line_to(55, -14)      # Forward fuselage left
    ctx.close_path()

    # Airframe filling: Lightweight grey composite
    ctx.set_source_rgb(0.26, 0.32, 0.38)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.45, 0.55, 0.65)
    ctx.set_line_width(2.5)
    ctx.stroke()

    # Wing panel lines & control surfaces (elevons)
    ctx.set_line_width(1.5)
    ctx.set_source_rgb(0.18, 0.22, 0.28)
    line(ctx, [(-65, 78), (-25, 24), (-68, 22)], (0.18, 0.22, 0.28), 1.5)
    line(ctx, [(-65, -78), (-25, -24), (-68, -22)], (0.18, 0.22, 0.28), 1.5)

    # Single Center Vertical Fin
    ctx.move_to(-20, 0)
    ctx.line_to(-78, 0)
    ctx.line_to(-68, 0)
    ctx.close_path()
    rrect(ctx, -75, -4, 55, 8, 2)
    ctx.set_source_rgb(0.35, 0.42, 0.50)
    ctx.fill()

    # IAF Tricolor Roundel on right wing
    circle(ctx, -38, 48, 14, SAFFRON, 1.0)
    circle(ctx, -38, 48, 9, WHITE, 1.0)
    circle(ctx, -38, 48, 5, INDIA_GREEN, 1.0)

    # Cockpit Bubble Canopy (Tinted Gold Glass)
    ctx.move_to(68, 0)
    ctx.curve_to(55, -8, 20, -9, 0, 0)
    ctx.curve_to(20, 9, 55, 8, 68, 0)
    ctx.close_path()
    ctx.set_source_rgb(0.95, 0.75, 0.22)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.1, 0.15, 0.2)
    ctx.set_line_width(2)
    ctx.stroke()

    # Pilot silhouette inside canopy
    circle(ctx, 32, 0, 4, (0.1, 0.1, 0.1), 0.9)

    # In-flight Refueling Probe (Starboard forward nose)
    line(ctx, [(52, 10), (82, 16)], (0.3, 0.35, 0.4), 2.5)

    # Underwing Pylons with Astra BVR Missiles
    for py_y in [-55, 55]:
        # Pylon
        rrect(ctx, -45, py_y - 2, 35, 4, 1)
        ctx.set_source_rgb(0.2, 0.25, 0.3)
        ctx.fill()
        # Astra Missile
        rrect(ctx, -48, py_y - 4, 52, 8, 2)
        ctx.set_source_rgb(0.85, 0.9, 0.95)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.3, 0.4, 0.5)
        ctx.set_line_width(1.5)
        ctx.stroke()
        # Red / Orange seeker nose
        ctx.move_to(4, py_y - 4)
        ctx.line_to(12, py_y)
        ctx.line_to(4, py_y + 4)
        ctx.close_path()
        ctx.set_source_rgb(1.0, 0.2, 0.1)
        ctx.fill()

    ctx.restore()


def draw_enemy_fighter(ctx, x, y, scale=1.0, angle=0.0):
    """Draw red hostile combat jet (neighboring JF-17 / F-16 silhouette)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(angle)
    ctx.scale(scale, scale)

    # Dark tactical airframe with red trim
    ctx.move_to(90, 0)
    ctx.line_to(45, 12)
    ctx.line_to(-10, 58)
    ctx.line_to(-35, 58)
    ctx.line_to(-25, 15)
    ctx.line_to(-65, 30)
    ctx.line_to(-70, 0)
    ctx.line_to(-65, -30)
    ctx.line_to(-25, -15)
    ctx.line_to(-35, -58)
    ctx.line_to(-10, -58)
    ctx.line_to(45, -12)
    ctx.close_path()
    ctx.set_source_rgb(0.22, 0.18, 0.20)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.9, 0.2, 0.2)
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Red lock cockpit
    rrect(ctx, 15, -6, 28, 12, 3)
    ctx.set_source_rgba(1.0, 0.1, 0.1, 0.8)
    ctx.fill()
    ctx.restore()


# ============================================================
# SCENE 1: BVR 100 KM Kill Zone Hook
# ============================================================

class SceneBvrHook(Cued):
    def events(self, d):
        return [(0.4, "whoosh"), (2.2, "beep")]

    def draw(self, ctx, t, d):
        # High altitude dark twilight sky
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, 0.02, 0.04, 0.09)
        g.add_color_stop_rgb(0.6, 0.06, 0.10, 0.18)
        g.add_color_stop_rgb(1, 0.02, 0.04, 0.08)
        ctx.set_source(g)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()

        # Tactical HUD Range Arc & Telemetry
        ctx.save()
        ctx.set_line_width(2)
        ctx.set_source_rgba(0, 0.9, 1.0, 0.25)
        for r_arc in [350, 600, 850]:
            ctx.arc(W * 0.5, 950, r_arc, -math.pi * 0.85, -math.pi * 0.15)
            ctx.stroke()
        text(ctx, "RANGE: 100+ KM // BEYOND VISUAL ENGAGEMENT", 80, 210, 22, CYAN, font=MONO, a=0.85, anchor="l")
        ctx.restore()

        # Tejas Mk 1A cruising in safe standoff airspace (bottom left)
        tx = 340 + math.sin(t * 1.8) * 25
        ty = 880 + math.cos(t * 1.5) * 15
        draw_tejas_fighter(ctx, tx, ty, scale=1.45, angle=math.radians(-35), afterburner=False, vapor=False)

        # Tejas Stealth Low-RCS Indicator
        rrect(ctx, tx - 120, ty - 85, 240, 36, 6)
        ctx.set_source_rgba(0.02, 0.08, 0.15, 0.85)
        ctx.fill_preserve()
        ctx.set_source_rgb(0.0, 0.9, 1.0)
        ctx.set_line_width(1.5)
        ctx.stroke()
        text(ctx, "TEJAS RCS: ~0.5 SQ M", tx, ty - 68, 16, CYAN, font=MONO, anchor="c")

        # Distant Hostile Jet locked at 100+ KM (top right)
        ex = 780 + math.sin(t * 2.2) * 20
        ey = 440 + math.cos(t * 2.0) * 15
        draw_enemy_fighter(ctx, ex, ey, scale=1.1, angle=math.radians(145))

        # Red BVR Targeting Reticle on Hostile
        ctx.save()
        circle(ctx, ex, ey, 60 + 8 * math.sin(t * 8), RED, 0.4)
        rrect(ctx, ex - 65, ey - 65, 130, 130, 10)
        ctx.set_source_rgba(1.0, 0.2, 0.2, 0.85)
        ctx.set_line_width(2.5)
        ctx.stroke()
        text(ctx, "TGT LOCK: 110 KM", ex, ey - 80, 20, RED, font=MONO, anchor="c")
        ctx.restore()


# ============================================================
# SCENE 2: AESA Radar & EW Jammer Dominance
# ============================================================

class SceneAesaRadarJammer(Cued):
    def events(self, d):
        return [(0.3, "whoosh"), (1.8, "beep")]

    def draw(self, ctx, t, d):
        # Deep space tactical radar view
        ctx.set_source_rgb(0.02, 0.03, 0.07)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()

        # Tejas Mk 1A in center-left facing forward
        tx, ty = 340, 750
        draw_tejas_fighter(ctx, tx, ty, scale=1.55, angle=math.radians(15))

        # Golden AESA Phased Array Radar Beams fanning out from nose
        nx, ny = tx + 160 * math.cos(math.radians(15)), ty + 160 * math.sin(math.radians(15))
        for beam_idx in range(7):
            ang = math.radians(-35 + beam_idx * 12 + math.sin(t * 4.0 + beam_idx) * 4)
            line(ctx, [(nx, ny), (nx + 480 * math.cos(ang), ny + 480 * math.sin(ang))], AESA_GOLD, 3.5, 0.75)
            # Pulse particles
            px = nx + ((t * 220 + beam_idx * 60) % 460) * math.cos(ang)
            py = ny + ((t * 220 + beam_idx * 60) % 460) * math.sin(ang)
            circle(ctx, px, py, 7, GOLD, 0.9)

        # Angad EW Jammer Pod emitting cyan static waves
        jx, jy = tx - 20, ty + 40
        for jw in range(4):
            rad = 40 + ((t * 120 + jw * 70) % 260)
            ctx.save()
            ctx.set_source_rgba(0, 0.9, 1.0, max(0.0, 0.8 - rad / 260))
            ctx.set_line_width(3)
            ctx.arc(jx, jy, rad, -math.pi * 0.4, math.pi * 0.6)
            ctx.stroke()
            ctx.restore()

        # Hostile jet radar scrambled on right
        hx, hy = 820, 640
        draw_enemy_fighter(ctx, hx, hy, scale=1.15, angle=math.radians(180))
        # Scrambled static box
        rrect(ctx, hx - 80, hy - 70, 160, 140, 8)
        ctx.set_source_rgba(1.0, 0.1, 0.1, 0.6 + 0.3 * math.sin(t * 15))
        ctx.set_line_width(2.5)
        ctx.stroke()
        text(ctx, "JAMMED // ZERO LOCK", hx, hy - 85, 20, RED, font=MONO, anchor="c")

        # Top Information Card
        rrect(ctx, W * 0.5 - 280, 240, 560, 100, 14)
        ctx.set_source_rgba(0.02, 0.05, 0.10, 0.88)
        ctx.fill_preserve()
        ctx.set_source_rgb(1.0, 0.7, 0.1)
        ctx.set_line_width(2.5)
        ctx.stroke()
        text(ctx, "UTTAM AESA RADAR + EW SUITE", W * 0.5, 275, 28, GOLD, anchor="c")
        text(ctx, "MULTI-TARGET TRACK // ENEMY RADAR BLINDED", W * 0.5, 315, 17, (1, 1, 1), font=MONO, a=0.85, anchor="c")


# ============================================================
# SCENE 3: Mach 4.5 Astra BVR Missile Strike
# ============================================================

class SceneAstraBvrStrike(Cued):
    def events(self, d):
        return [(0.3, "whoosh"), (3.0, "boom")]

    def draw(self, ctx, t, d):
        # Stratospheric horizon with orange glow
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, 0.01, 0.02, 0.06)
        g.add_color_stop_rgb(0.7, 0.08, 0.12, 0.22)
        g.add_color_stop_rgb(1, 0.16, 0.08, 0.06)
        ctx.set_source(g)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()

        pr = min(1.0, t / 4.0)

        # Tejas Mk 1A firing missile from left
        tx, ty = 280, 780
        draw_tejas_fighter(ctx, tx, ty, scale=1.35, angle=math.radians(-25), afterburner=True, vapor=True)

        # Astra BVR Missile streaking across screen at Mach 4.5
        mx = tx + 80 + pr * 560
        my = ty - 40 - pr * 260

        # Blazing solid rocket flame & smoke contrail
        line(ctx, [(tx + 80, ty - 40), (mx, my)], (1.0, 0.6, 0.1), 7, 0.9)
        line(ctx, [(tx + 80, ty - 40), (mx, my)], (1.0, 0.95, 0.7), 3, 0.95)

        # Flying Astra Missile body
        ctx.save()
        ctx.translate(mx, my)
        ctx.rotate(math.radians(-25))
        rrect(ctx, -30, -5, 60, 10, 3)
        ctx.set_source_rgb(0.9, 0.95, 1.0)
        ctx.fill()
        circle(ctx, 30, 0, 8, (1.0, 0.3, 0.1), 1.0)
        glow(ctx, 30, 0, 30, FIRE_ORANGE, 0.9)
        ctx.restore()

        # Distant Enemy Fighter hit and exploding on top right
        ex, ey = 840, 520
        ex_p = max(0.0, (t - 2.2) / 2.0)
        if ex_p > 0.0:
            glow(ctx, ex, ey, 70 + ex_p * 90, FIRE_ORANGE, 0.9 * (1.0 - ex_p))
            glow(ctx, ex, ey, 35 + ex_p * 45, (1.0, 0.9, 0.2), 1.0 * (1.0 - ex_p))
            text(ctx, "BORDER PAAR KHEL KHATAM!", ex, ey + 60, 22, FIRE_ORANGE, font=MONO, anchor="c")
        else:
            draw_enemy_fighter(ctx, ex, ey, scale=1.0, angle=math.radians(160))
            circle(ctx, ex, ey, 45, RED, 0.5)
            text(ctx, "INCOMING MACH 4.5", ex, ey - 50, 18, RED, font=MONO, anchor="c")


# ============================================================
# SCENE 4: Infinite Loop CTA & Prompt
# ============================================================

class SceneCtaPrompt(Cued):
    def events(self, d):
        return [(0.3, "whoosh"), (2.0, "pop")]

    def draw(self, ctx, t, d):
        # Blazing saffron-twilight sky
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, 0.03, 0.05, 0.12)
        g.add_color_stop_rgb(0.5, 0.15, 0.10, 0.16)
        g.add_color_stop_rgb(1, 0.04, 0.03, 0.06)
        ctx.set_source(g)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()

        # Central Tejas climbing aggressively into twilight
        ctx.save()
        glow(ctx, W * 0.5, 520, 280, SAFFRON, 0.3)
        draw_tejas_fighter(ctx, W * 0.5, 520, scale=1.65, angle=math.radians(-65), afterburner=True, vapor=True)
        ctx.restore()

        # Interactive Question / Prompt UI Card
        py = 730
        rrect(ctx, W * 0.5 - 330, py, 660, 190, 18)
        ctx.set_source_rgba(0.02, 0.05, 0.10, 0.92)
        ctx.fill_preserve()
        ctx.set_source_rgb(1.0, 0.65, 0.1)
        ctx.set_line_width(3)
        ctx.stroke()

        text(ctx, "KYA TEJAS SABSE DHAKAD HAI?", W * 0.5, py + 50, 30, GOLD, anchor="c")
        text(ctx, "COMMENT MEIN BATAO!", W * 0.5, py + 110, 26, WHITE, font=MONO, anchor="c")

        # Animated arrow pointing to comment button
        arrow_y = py + 145 + math.sin(t * 6.0) * 8
        line(ctx, [(W * 0.5 - 60, arrow_y), (W * 0.5 + 60, arrow_y)], SAFFRON, 4)
        line(ctx, [(W * 0.5 + 40, arrow_y - 12), (W * 0.5 + 60, arrow_y), (W * 0.5 + 40, arrow_y + 12)], SAFFRON, 4)


SCENE_CLASSES = {
    "bvr_hook": SceneBvrHook,
    "aesa_radar_jammer": SceneAesaRadarJammer,
    "astra_bvr_strike": SceneAstraBvrStrike,
    "cta_prompt": SceneCtaPrompt,
}


UPLOAD = {
    "titles": [
        "Tejas Mk 1A: 100 KM Door Se Dushman Tabah! 🇮🇳🔥 #shorts",
        "Can Tejas Mk 1A Beat JF-17 In BVR Combat? 🚀 #shorts",
        "Desi Tejas Ka AESA Radar: Dushman Ka Khel Khatam! 🇮🇳 #shorts",
        "Why No Neighboring Jet Can Beat Tejas Mk 1A? #shorts",
        "Tejas Mk 1A vs Neighboring Fighters: BVR Dominance! #shorts",
    ],
    "title": "Tejas Mk 1A: 100 KM Door Se Dushman Tabah! 🇮🇳🔥 #shorts",
    "thumb_text": "TEJAS BVR COMBAT",
    "queries": ["tejas mk 1a", "tejas bvr combat", "tejas radar combat"],
    "description": """Bharat ka apna desi supersonic fighter Tejas Mk 1A vs JF-17 BVR combat breakdown!
Uttam AESA Radar aur electronic warfare jammer ke sath, Tejas 100+ kilometer door se hi dushman fighter ko lock karke Astra BVR missile se hawa mein uda deta hai.

Is Short mein:
• 100+ KM BVR Engagement Envelope
• Advanced Uttam AESA Radar & Angad EW Jammer Suite
• Mach 4.5 Indigenous Astra Air-to-Air Missile Strike

Kya Tejas Mk 1A border par sabse bada game changer hai? Comment mein likhein - JAI HIND! 🇮🇳
Subscribe to RealityShift for high-tech defence breakdowns.

#Shorts #TejasMk1A #IndianAirForce
""",
    "tags": [
        "tejas mk 1a", "hal tejas", "tejas vs jf17", "indian air force",
        "tejas aesa radar", "astra missile", "bvr combat", "tejas fighter jet",
        "reality shift", "defence shorts", "viral shorts"
    ],
    "hashtags": ["#Shorts", "#TejasMk1A", "#IndianAirForce"],
}


def thumbnail(ctx):
    """High-CTR YouTube Shorts cover for Tejas Mk 1A."""
    # Dark tactical radar background
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.02, 0.03, 0.08)
    g.add_color_stop_rgb(0.5, 0.08, 0.12, 0.22)
    g.add_color_stop_rgb(1, 0.02, 0.03, 0.06)
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()

    # Concentric BVR Radar Rings
    for r in [280, 520, 760]:
        circle(ctx, W * 0.5, 1100, r, CYAN, 0.08)

    # Hero Tejas Mk 1A climbing aggressively with twin afterburners
    draw_tejas_fighter(ctx, 480, 1120, scale=1.9, angle=math.radians(-50), afterburner=True, vapor=True)

    # Mach 4.5 Astra Missile streaking towards target
    line(ctx, [(520, 940), (320, 640)], (1.0, 0.6, 0.1), 8, 0.85)
    circle(ctx, 320, 640, 18, (1.0, 0.9, 0.3), 1.0)
    glow(ctx, 320, 640, 55, FIRE_ORANGE, 0.8)

    # Hostile jet locked in target reticle at top left
    draw_enemy_fighter(ctx, 300, 520, scale=1.35, angle=math.radians(135))
    circle(ctx, 300, 520, 65, RED, 0.4)
    rrect(ctx, 230, 450, 140, 140, 10)
    ctx.set_source_rgba(1.0, 0.2, 0.2, 0.9)
    ctx.set_line_width(3)
    ctx.stroke()
    text(ctx, "TGT LOCK: 100+ KM", 300, 420, 22, RED, font=MONO, anchor="c")

    # High-Impact Thumbnail Header Box
    rrect(ctx, 80, 140, W - 160, 190, 20)
    ctx.set_source_rgba(0.02, 0.04, 0.08, 0.92)
    ctx.fill_preserve()
    ctx.set_source_rgb(1.0, 0.65, 0.1)
    ctx.set_line_width(4)
    ctx.stroke()

    text(ctx, "TEJAS MK 1A", W * 0.5, 210, 64, GOLD, anchor="c")
    text(ctx, "100 KM BVR RADAR COMBAT", W * 0.5, 280, 30, CYAN, font=MONO, anchor="c")


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
    story = importlib.import_module("shorts.tejas_mk1a")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))
