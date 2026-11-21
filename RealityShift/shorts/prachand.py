"""Reality Shift Short — "LCH Prachand: Siachen Ka Desi Shikari" (~45-50s).

Usage:
  python make.py prachand --kiki-split
  python make.py prachand --engine files
  python make.py prachand --preview

Technical Overview:
HAL LCH Prachand (Light Combat Helicopter):
World's only dedicated attack helicopter capable of taking off and landing at 5,000 meters (16,400 ft)
with a full combat weapons and fuel payload.
Developed by Hindustan Aeronautics Limited (HAL) following critical operational lessons from the 1999 Kargil War.
Powered by twin HAL/Safran Shakti turboshaft engines, featuring narrow stealth fuselage, armor protection,
20mm M621 nose turret gun, 70mm rocket pods, and Dhruvastra/Helina anti-tank guided missiles.
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
from shorts.reality_shift import flag, stamp

TOPIC = "LCH PRACHAND ATTACK HELICOPTER"
OUTPUTS = {"edge": "prachand_short.mp4"}
LEGO = {"header": "radar", "caption": "typewriter", "transition": "shutter", "palette": "glacier", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.55
TAIL_PAD = 0.20
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 112
MUSIC_STYLE = "tension"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 300

PAL = lego.PALETTES["glacier"]
UI = PAL["ui"]
HI = PAL["hi"]
RED = PAL["alert"]
INK = PAL["ink"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
STEEL = hexc("#90A4AE")
DARK_STEEL = hexc("#1A2530")
CAMO_OLIVE = hexc("#3B4F35")
CAMO_DARK = hexc("#283625")
SNOW_WHITE = hexc("#E8F1F5")
WHITE = (1.0, 1.0, 1.0)
FIRE_ORANGE = hexc("#FF5500")
GOLD = hexc("#FFD700")
HUD_GREEN = hexc("#00FF66")
CYAN = hexc("#00E5FF")
MONO = "Consolas"

SOURCES = [
    "Hindustan Aeronautics Limited (HAL) - Light Combat Helicopter (LCH Prachand) Design & Flight Envelope",
    "Indian Air Force & Indian Army Aviation Corps - High Altitude Trials at Siachen & Daulat Beg Oldie (DBO)",
    "Ministry of Defence (MoD) - Cabinet Committee on Security approval for 156 LCH Prachand helicopters",
    "1999 Kargil Conflict Post-Operations Analysis - High-Altitude Close Air Support Requirements",
]

SPEC = [
    # Scene 1: Kargil 1999 Need
    {"key": "kargil_need", "accent": RED, "text": "1999 KARGIL CRISIS",
     "visual": "Snow-covered peaks of Kargil, enemy bunkers high on steep ridgelines, Indian troops facing intense fire, zero high-altitude attack helicopter available",
     "vo": [("tell", [("उन्नीस सौ निन्यानवे, करगिल।", "1999 KARGIL."),
                      ("दुश्मन ऊँची चोटियों पर बैठा था।", "DUSHMAN OONCHI CHOTIYON PAR BAITHA THA."),
                      ("और हमारे पास, उतनी ऊँचाई पर लड़ने वाला,", "AUR HAMARE PAAS UTNI UNCHAI PAR LADNE WALA,"),
                      ("कोई हमलावर हेलीकॉप्टर नहीं था।", "KOI HAMLAWAR HELICOPTER NAHI THA.")])]},

    # Scene 2: Birth of Prachand
    {"key": "birth_prachand", "accent": SAFFRON, "text": "BIRTH OF PRACHAND",
     "visual": "HAL engineering blueprint transforms into aggressive stealth fuselage of LCH Prachand, angular cockpit, twin Shakti engines, tricolor insignia",
     "vo": [("tell", [("उसी कमी से जन्म हुआ...", "USI KAMI SE JANM HUA..."),
                      ("प्रचंड का!", "PRACHAND KA!")])]},

    # Scene 3: World Record 5,000m Capability
    {"key": "high_altitude_record", "accent": GOLD, "text": "5,000M WORLD RECORD",
     "visual": "LCH Prachand climbing vertically above mountain clouds at 5000 meters (16,400 ft), altitude gauge rolling up, spinning rotor blades",
     "vo": [("tell", [("ये दुनिया का इकलौता हमलावर हेलीकॉप्टर है,", "YE DUNIYA KA EKLOTA ATTACK HELICOPTER HAI,"),
                      ("जो पाँच हज़ार मीटर की ऊँचाई पर,", "JO 5000 METER KI UNCHAI PAR,"),
                      ("उतर भी सकता है, और उड़ भी सकता है।", "UTAR BHI SAKTA HAI, AUR UDD BHI SAKTA HAI.")])]},

    # Scene 4: Siachen 4700m Landing
    {"key": "siachen_landing", "accent": HUD_GREEN, "text": "SIACHEN 4700M TOUCHDOWN",
     "visual": "Extreme cold Siachen Glacier, Prachand lands on frozen snowpad with 500kg combat load; foreign heavy choppers show warning red alert",
     "vo": [("tell", [("सियाचिन में, करीब सैंतालीस सौ मीटर पर,", "SIACHEN MEIN, QAREEB 4700 METER PAR,"),
                      ("ये पाँच सौ किलो वज़न लेकर उतर चुका है।", "YE 500 KG WAZAN LEKAR UTAR CHUKA HAI."),
                      ("जहाँ हवा इतनी पतली,", "JAHAN HAWA ITNI PATLI,"),
                      ("कि बाकी हेलीकॉप्टर हाँफ जाएँ।", "KI BAAKI HELICOPTER HAANF JAAYEIN.")])]},

    # Scene 5: Indigenous Firepower
    {"key": "weapons_arsenal", "accent": FIRE_ORANGE, "text": "LETHAL DESI ARSENAL",
     "visual": "Close-up of 20mm rotating chin cannon tracking adversary, 70mm rocket volley erupting from stub wings, anti-tank missile obliterating bunker",
     "vo": [("tell", [("नाक के नीचे घूमने वाली तोप,", "NAAK KE NEECHE GHOOMNE WALI TOP,"),
                      ("रॉकेट, और टैंक तोड़ने वाली मिसाइलें...", "ROCKET, AUR TANK TODNE WALI MISSILE-EIN..."),
                      ("सब इसी में। और भाई, डिज़ाइन पूरा देसी।", "SAB ISI MEIN. AUR DESIGN PURA DESI.")])]},

    # Scene 6: Mega 156 Order
    {"key": "mega_order", "accent": SAFFRON, "text": "156 PRACHAND FLEET",
     "visual": "Formation of LCH Prachand choppers flying along Himalayan ridgeline, big 156 badge, Indian Army and Air Force joint combat power",
     "vo": [("tell", [("सरकार ने, एक सौ छप्पन प्रचंड का ऑर्डर दे दिया है।", "SARKAR NE 156 PRACHAND KA ORDER DIYA HAI."),
                      ("पहली खेप, दो हज़ार अट्ठाईस से आनी शुरू होगी।", "PEHLI KHEP 2028 SE AANI SHURU HOGI.")])]},

    # Scene 7: CTA & National Pride
    {"key": "cta_poll", "accent": HI, "text": "NATIONAL PRIDE & POLL",
     "visual": "Cinematic head-on hover of Prachand, glowing HUD crosshair, poll prompt ribbon: 'SIACHEN MEIN TAINAATI?', arrow pointing down to comment",
     "vo": [("ask", [("प्रचंड की सबसे बड़ी ताकत कौन सी लगी,", "PRACHAND KI SABSE BADI TAAQAT KAUN SI LAGI,"),
                      ("कमेंट में बताइए।", "COMMENT MEIN BATAIYE."),
                      ("जय हिंद!", "JAI HIND!")])]},
]

DELIVERY = delivery.build(SPEC)
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "1999": GOLD, "KARGIL": RED, "DUSHMAN": RED, "CHOTIYON": GOLD, "OONCHI": GOLD,
    "HAMLAWAR": FIRE_ORANGE, "HELICOPTER": SAFFRON, "PRACHAND": SAFFRON, "EKLOTA": GOLD,
    "5000": GOLD, "METER": GOLD, "UNCHAI": GOLD, "UTAR": HUD_GREEN, "UDD": HUD_GREEN,
    "SIACHEN": SNOW_WHITE, "4700": GOLD, "500": GOLD, "HAWA": HUD_GREEN, "PATLI": RED,
    "HAANF": RED, "NAAK": GOLD, "TOP": FIRE_ORANGE, "ROCKET": FIRE_ORANGE, "TANK": RED,
    "MISSILE-EIN": FIRE_ORANGE, "DESI": SAFFRON, "DESIGN": HUD_GREEN, "SARKAR": SAFFRON,
    "156": GOLD, "ORDER": GOLD, "2028": GOLD, "TAAQAT": SAFFRON, "COMMENT": HI,
    "BATAIYE": HI, "JAI": SAFFRON, "HIND": SAFFRON, "ATTACK": RED
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".—,")] = HOT[_k]


# ============================================================ DRAWING HELPERS

def fill_circle(ctx, x, y, r, color, a=1.0):
    circle(ctx, x, y, r, color, a)


def stroke_circle(ctx, x, y, r, color, stroke_w=2, a=1.0):
    ctx.arc(x, y, r, 0, 2 * math.pi)
    rgba(ctx, color, a)
    ctx.set_line_width(stroke_w)
    ctx.stroke()


def fill_rrect(ctx, x, y, w, h, r, color, a=1.0):
    rrect(ctx, x, y, w, h, r)
    rgba(ctx, color, a)
    ctx.fill()


def stroke_rrect(ctx, x, y, w, h, r, color, stroke_w=2, a=1.0):
    rrect(ctx, x, y, w, h, r)
    rgba(ctx, color, a)
    ctx.set_line_width(stroke_w)
    ctx.stroke()


def draw_line(ctx, x1, y1, x2, y2, c, w=2, a=1.0):
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    rgba(ctx, c, a)
    ctx.set_line_width(w)
    ctx.stroke()


def draw_card(ctx, x, y, w, h, r, fill_c, stroke_c, stroke_w=3, a=1.0):
    fill_rrect(ctx, x, y, w, h, r, fill_c, a)
    stroke_rrect(ctx, x, y, w, h, r, stroke_c, stroke_w, a)


def draw_badge(ctx, label, x, y, c, w=720, h=90):
    draw_card(ctx, x - w / 2, y - h / 2, w, h, 14, (0.04, 0.04, 0.08), c, stroke_w=4, a=0.92)
    text(ctx, label, x, y + 10, 36, c, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=8)


def draw_mountain_ridges(ctx, t=0.0, snow_color=SNOW_WHITE):
    """Draw layered jagged mountain peaks with snow caps."""
    # Far ridge (dark purplish slate)
    ctx.set_source_rgb(0.12, 0.16, 0.22)
    ctx.move_to(0, 1100)
    peaks1 = [(0, 850), (180, 720), (380, 820), (540, 680), (720, 790), (920, 690), (1080, 800), (1080, 1920), (0, 1920)]
    for px, py in peaks1:
        ctx.line_to(px, py)
    ctx.close_path()
    ctx.fill()

    # Mid ridge with snow caps
    ctx.set_source_rgb(0.18, 0.24, 0.32)
    ctx.move_to(0, 1200)
    peaks2 = [(0, 980), (220, 820), (420, 940), (620, 780), (840, 890), (1080, 810), (1080, 1920), (0, 1920)]
    for px, py in peaks2:
        ctx.line_to(px, py)
    ctx.close_path()
    ctx.fill()

    # Snow caps on mid ridge
    rgba(ctx, snow_color, 0.85)
    caps = [
        [(170, 870), (220, 820), (280, 890), (220, 870)],
        [(560, 840), (620, 780), (680, 850), (620, 830)],
        [(790, 930), (840, 890), (890, 940), (840, 925)],
    ]
    for cap in caps:
        ctx.move_to(cap[0][0], cap[0][1])
        for pt in cap[1:]:
            ctx.line_to(pt[0], pt[1])
        ctx.close_path()
        ctx.fill()

    # Near foreground snowy ridge
    ctx.set_source_rgb(0.24, 0.32, 0.42)
    ctx.move_to(0, 1400)
    peaks3 = [(0, 1250), (320, 1100), (650, 1220), (950, 1080), (1080, 1180), (1080, 1920), (0, 1920)]
    for px, py in peaks3:
        ctx.line_to(px, py)
    ctx.close_path()
    ctx.fill()

    # Foreground snow cover
    rgba(ctx, snow_color, 0.95)
    ctx.move_to(0, 1320)
    ctx.line_to(320, 1100)
    ctx.line_to(450, 1190)
    ctx.line_to(650, 1220)
    ctx.line_to(950, 1080)
    ctx.line_to(1080, 1180)
    ctx.line_to(1080, 1920)
    ctx.line_to(0, 1920)
    ctx.close_path()
    ctx.fill()


def draw_prachand_helicopter(ctx, x, y, scale=1.0, t=0.0, rotor_speed=1.0, firing=False, side_view=True):
    """Draw high-fidelity procedural HAL LCH Prachand attack helicopter."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(scale, scale)

    if side_view:
        # Hover / bob motion
        bob_y = math.sin(t * 5.0) * 8.0
        pitch = math.sin(t * 3.0) * 0.03
        ctx.translate(0, bob_y)
        ctx.rotate(pitch)

        # 1. Main Rotor Shaft
        ctx.set_source_rgb(DARK_STEEL[0], DARK_STEEL[1], DARK_STEEL[2])
        ctx.rectangle(-12, -100, 24, 45)
        ctx.fill()
        fill_circle(ctx, 0, -100, 20, STEEL)
        stroke_circle(ctx, 0, -100, 20, DARK_STEEL, stroke_w=4)

        # 2. Main Rotor Blades (4-blade spinning blur + blades)
        blade_ang = (t * 40.0 * rotor_speed) % (2.0 * math.pi)
        blade_w = 460.0
        # Blade blur disc
        ctx.set_source_rgba(0.8, 0.9, 1.0, 0.12)
        ctx.save()
        ctx.scale(1.0, 0.18)
        ctx.arc(0, -100 / 0.18, blade_w, 0, 2 * math.pi)
        ctx.fill()
        ctx.restore()

        # Physical blades
        for b_i in range(4):
            ang = blade_ang + b_i * (math.pi / 2.0)
            bx = math.cos(ang) * blade_w
            by = math.sin(ang) * (blade_w * 0.16)
            ctx.set_source_rgba(0.1, 0.15, 0.2, 0.85)
            ctx.set_line_width(12)
            ctx.move_to(0, -100)
            ctx.line_to(bx, -100 + by)
            ctx.stroke()
            # Yellow blade tips
            ctx.set_source_rgba(GOLD[0], GOLD[1], GOLD[2], 0.9)
            ctx.set_line_width(14)
            ctx.move_to(bx * 0.85, -100 + by * 0.85)
            ctx.line_to(bx, -100 + by)
            ctx.stroke()

        # 3. Tail Boom & Tail Rotor
        ctx.set_source_rgb(CAMO_OLIVE[0], CAMO_OLIVE[1], CAMO_OLIVE[2])
        ctx.move_to(40, -40)
        ctx.line_to(360, -30)
        ctx.line_to(380, -90)    # Vertical fin
        ctx.line_to(405, -95)
        ctx.line_to(390, 0)
        ctx.line_to(330, 10)
        ctx.line_to(40, 20)
        ctx.close_path()
        ctx.fill()

        # Horizontal stabilizer
        ctx.set_source_rgb(CAMO_DARK[0], CAMO_DARK[1], CAMO_DARK[2])
        ctx.rectangle(300, -25, 60, 12)
        ctx.fill()

        # Tail rotor
        tail_ang = (t * 60.0) % (2.0 * math.pi)
        stroke_circle(ctx, 385, -70, 45, (0.7, 0.8, 0.9), stroke_w=2, a=0.3)
        for t_i in range(2):
            tang = tail_ang + t_i * math.pi
            tx = math.cos(tang) * 45
            ty = math.sin(tang) * 45
            draw_line(ctx, 385 - tx, -70 - ty, 385 + tx, -70 + ty, c=(0.1, 0.1, 0.1), w=6)

        # 4. Main Fuselage (Stealth chiseled angular design)
        # Camo base
        ctx.set_source_rgb(CAMO_OLIVE[0], CAMO_OLIVE[1], CAMO_OLIVE[2])
        ctx.move_to(-240, 25)   # Nose bottom
        ctx.line_to(-210, -35)  # Nose upper
        ctx.line_to(-120, -65)  # Tandem canopy front
        ctx.line_to(20, -65)    # Canopy rear / engine hump
        ctx.line_to(110, -50)   # Exhaust section
        ctx.line_to(140, -10)   # Engine rear
        ctx.line_to(70, 40)     # Belly rear
        ctx.line_to(-180, 45)   # Belly front
        ctx.close_path()
        ctx.fill()

        # Camo dark patch
        ctx.set_source_rgb(CAMO_DARK[0], CAMO_DARK[1], CAMO_DARK[2])
        ctx.move_to(-140, 42)
        ctx.line_to(-70, -20)
        ctx.line_to(30, -55)
        ctx.line_to(80, 10)
        ctx.line_to(10, 42)
        ctx.close_path()
        ctx.fill()

        # 5. Twin Tandem Cockpit Windows (Stealth faceted canopy)
        # Front Gunner Canopy
        ctx.set_source_rgba(0.08, 0.18, 0.28, 0.92)
        ctx.move_to(-190, -25)
        ctx.line_to(-130, -55)
        ctx.line_to(-90, -55)
        ctx.line_to(-110, -20)
        ctx.close_path()
        ctx.fill()
        draw_line(ctx, -180, -28, -135, -50, c=(0.2, 0.8, 1.0), w=4)

        # Rear Pilot Canopy (Stepped higher for visibility)
        ctx.set_source_rgba(0.08, 0.18, 0.28, 0.92)
        ctx.move_to(-80, -20)
        ctx.line_to(-80, -60)
        ctx.line_to(0, -60)
        ctx.line_to(-10, -15)
        ctx.close_path()
        ctx.fill()
        draw_line(ctx, -75, -55, -10, -55, c=(0.2, 0.8, 1.0), w=4)

        # 6. Stub Wing & Weapons Pylons
        ctx.set_source_rgb(DARK_STEEL[0], DARK_STEEL[1], DARK_STEEL[2])
        ctx.rectangle(-40, 10, 80, 18)
        ctx.fill()

        # 70mm Rocket Pod (cylindrical pod mounted under stub wing)
        draw_card(ctx, -55, 26, 90, 28, 6, STEEL, DARK_STEEL, stroke_w=3)
        for h_y in (-4, 4):
            fill_circle(ctx, -50, 40 + h_y, 4, FIRE_ORANGE)

        # Helina / Dhruvastra Anti-Tank Missiles rail
        fill_rrect(ctx, -30, 54, 70, 12, 3, DARK_STEEL)
        fill_rrect(ctx, -25, 56, 60, 8, 2, WHITE)

        # 7. Nose 20mm M621 Turret Cannon
        cannon_angle = 0.15 + math.sin(t * 2.0) * 0.12
        ctx.save()
        ctx.translate(-215, 30)
        ctx.rotate(cannon_angle)
        fill_circle(ctx, 0, 0, 14, DARK_STEEL)
        stroke_circle(ctx, 0, 0, 14, STEEL, stroke_w=3)
        # Gun barrel
        ctx.set_source_rgb(0.05, 0.05, 0.05)
        ctx.rectangle(-45, -4, 45, 8)
        ctx.fill()
        # Muzzle brake
        ctx.rectangle(-52, -6, 7, 12)
        ctx.fill()

        # Firing flash if enabled
        if firing:
            flash_len = 60 + math.sin(t * 80.0) * 25
            ctx.set_source_rgba(FIRE_ORANGE[0], FIRE_ORANGE[1], FIRE_ORANGE[2], 0.9)
            ctx.move_to(-52, 0)
            ctx.line_to(-52 - flash_len, -16)
            ctx.line_to(-52 - flash_len * 1.3, 0)
            ctx.line_to(-52 - flash_len, 16)
            ctx.close_path()
            ctx.fill()
            fill_circle(ctx, -55, 0, 22, GOLD, a=0.8)
        ctx.restore()

        # 8. Fixed Rugged Tricycle Landing Gear (Crashworthy)
        draw_line(ctx, 10, 40, -10, 85, c=DARK_STEEL, w=10)
        fill_circle(ctx, -10, 85, 14, (0.1, 0.1, 0.1))
        stroke_circle(ctx, -10, 85, 14, STEEL, stroke_w=4)
        draw_line(ctx, 320, 10, 310, 55, c=DARK_STEEL, w=6)
        fill_circle(ctx, 310, 55, 9, (0.1, 0.1, 0.1))
        stroke_circle(ctx, 310, 55, 9, STEEL, stroke_w=3)

        # 9. IAF Tricolor Roundel & Serial
        fill_circle(ctx, 100, -10, 16, SAFFRON)
        fill_circle(ctx, 100, -10, 10, WHITE)
        fill_circle(ctx, 100, -10, 5, INDIA_GREEN)
        text(ctx, "IAF PRACHAND", 150, -12, 14, WHITE, font=MONO, bold=True, a=0.8)

    ctx.restore()


# ============================================================ SCENE CLASSES

class KargilNeedScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"kargil": c("KARGIL", 0.8), "dushman": c("DUSHMAN", d * 0.4), "chopper": c("HELICOPTER", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["kargil"], "pick"), (b["dushman"], "pop"), (b["chopper"], "whoosh")]

    def draw(self, ctx, t, d):
        # 1. Cold dramatic mountain sky
        grad = cairo.LinearGradient(0, 0, 0, engine.H)
        grad.add_color_stop_rgb(0, 0.08, 0.12, 0.18)
        grad.add_color_stop_rgb(0.5, 0.15, 0.18, 0.24)
        grad.add_color_stop_rgb(1.0, 0.05, 0.06, 0.08)
        ctx.set_source(grad)
        ctx.paint()

        # Mountains
        draw_mountain_ridges(ctx, t)

        # 2. Enemy bunker on high ridge with red alert circle
        bx, by = 620, 780
        fill_circle(ctx, bx, by, 32, (0.3, 0.1, 0.1))
        stroke_circle(ctx, bx, by, 32, RED, stroke_w=4)
        fill_rrect(ctx, bx - 22, by - 6, 44, 12, 2, (0.1, 0.1, 0.1))

        # Enemy flag silhouette
        draw_line(ctx, bx + 16, by - 20, bx + 16, by - 65, c=RED, w=4)
        ctx.set_source_rgb(0.8, 0.1, 0.1)
        ctx.rectangle(bx + 16, by - 65, 30, 20)
        ctx.fill()

        # Alert pulse around bunker
        pulse_r = 40 + (t * 80) % 90
        stroke_circle(ctx, bx, by, pulse_r, RED, stroke_w=3, a=max(0, 1.0 - pulse_r / 130))

        # 3. 1999 Kargil Stamp
        draw_badge(ctx, "1999 KARGIL WAR CRISIS", 540, 360, RED)

        # Missing attack helicopter tag
        draw_card(ctx, 160, 480, 760, 90, 12, (0.05, 0.08, 0.12), RED, stroke_w=4, a=0.92)
        text(ctx, "CRITICAL GAP: NO HIGH-ALTITUDE ATTACK CHOPPER", 540, 535, 34, RED, font=MONO, bold=True)


class BirthPrachandScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"kami": c("KAMI", 0.6), "prachand": c("PRACHAND", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["kami"], "pick"), (b["prachand"], "boom")]

    def draw(self, ctx, t, d):
        # High-tech blueprint grid
        grad = cairo.LinearGradient(0, 0, 0, engine.H)
        grad.add_color_stop_rgb(0, 0.02, 0.08, 0.16)
        grad.add_color_stop_rgb(1.0, 0.01, 0.04, 0.08)
        ctx.set_source(grad)
        ctx.paint()

        # Technical grid lines
        ctx.set_source_rgba(0.2, 0.6, 1.0, 0.12)
        ctx.set_line_width(2)
        for gx in range(0, engine.W, 80):
            ctx.move_to(gx, 0)
            ctx.line_to(gx, engine.H)
            ctx.stroke()
        for gy in range(0, engine.H, 80):
            ctx.move_to(0, gy)
            ctx.line_to(engine.W, gy)
            ctx.stroke()

        # HAL & DRDO Design Title
        text(ctx, "PROJECT LCH : DESI DESIGN", 540, 320, 52, GOLD, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=8)
        text(ctx, "TWIN SHAKTI ENGINES | STEALTH AIRFRAME", 540, 390, 32, HUD_GREEN, font=MONO, bold=True)

        # Prachand emerging from blueprint
        prog = min(1.0, t / (d * 0.5))
        draw_prachand_helicopter(ctx, 540, 920, scale=1.35 * prog, t=t, rotor_speed=1.5)

        # Technical callouts around chopper
        if prog > 0.6:
            draw_card(ctx, 120, 1150, 380, 80, 8, (0.02, 0.06, 0.12), HUD_GREEN, stroke_w=3, a=0.9)
            text(ctx, "NARROW TANDEM COCKPIT", 310, 1180, 24, HUD_GREEN, font=MONO, bold=True)
            text(ctx, "RADAR CROSS SECTION MINIMIZED", 310, 1210, 20, WHITE, font=MONO)

            draw_card(ctx, 580, 1150, 400, 80, 8, (0.02, 0.06, 0.12), SAFFRON, stroke_w=3, a=0.9)
            text(ctx, "TWIN SHAKTI ENGINES", 780, 1180, 24, SAFFRON, font=MONO, bold=True)
            text(ctx, "1,032 kW HIGH-ALTITUDE POWER", 780, 1210, 20, WHITE, font=MONO)


class HighAltitudeRecordScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"eklota": c("EKLOTA", 0.6), "5000": c("5000", d * 0.4), "record": c("RECORD", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["eklota"], "pick"), (b["5000"], "pop"), (b["record"], "beep")]

    def draw(self, ctx, t, d):
        # Deep blue stratosphere sky
        grad = cairo.LinearGradient(0, 0, 0, engine.H)
        grad.add_color_stop_rgb(0, 0.01, 0.06, 0.22)
        grad.add_color_stop_rgb(0.5, 0.05, 0.16, 0.38)
        grad.add_color_stop_rgb(1.0, 0.35, 0.55, 0.75)
        ctx.set_source(grad)
        ctx.paint()

        # Distant low clouds scrolling under
        for c_i in range(6):
            cx = (c_i * 260 + t * 40) % (engine.W + 200) - 100
            cy = 1350 + (c_i % 3) * 80
            fill_circle(ctx, cx, cy, 140, (0.95, 0.98, 1.0), a=0.35)

        # Altitude telemetry HUD meter
        meter_y = 340
        draw_card(ctx, 160, meter_y, 760, 150, 16, (0.04, 0.08, 0.15), GOLD, stroke_w=5, a=0.92)
        text(ctx, "WORLD RECORD ALTITUDE", 540, meter_y + 45, 36, HUD_GREEN, font=MONO, bold=True)

        # Altitude counter 0 -> 5,000 meters
        cur_alt = min(5000, int((t / (d * 0.65)) * 5000))
        text(ctx, f"{cur_alt:,} METERS (16,400 FT)", 540, meter_y + 115, 62, GOLD, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=10)

        # Prachand climbing high
        heli_y = 1050 - (t / d) * 160
        draw_prachand_helicopter(ctx, 520, heli_y, scale=1.4, t=t, rotor_speed=1.8)

        # Badge: WORLD ONLY
        draw_badge(ctx, "WORLD'S ONLY ATTACK CHOPPER @ 5000M", 540, 1380, HUD_GREEN, w=820)


class SiachenLandingScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"siachen": c("SIACHEN", 0.7), "500kg": c("500", d * 0.4), "patli": c("PATLI", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["siachen"], "pick"), (b["500kg"], "pop"), (b["patli"], "beep")]

    def draw(self, ctx, t, d):
        # Icy arctic white-blue atmosphere
        grad = cairo.LinearGradient(0, 0, 0, engine.H)
        grad.add_color_stop_rgb(0, 0.15, 0.25, 0.35)
        grad.add_color_stop_rgb(0.6, 0.45, 0.55, 0.65)
        grad.add_color_stop_rgb(1.0, 0.85, 0.92, 0.98)
        ctx.set_source(grad)
        ctx.paint()

        # Glacier snowy ridge
        draw_mountain_ridges(ctx, t, snow_color=(0.95, 0.98, 1.0))

        # Snow blowing storm particles
        for p_i in range(35):
            px = (p_i * 97 + t * 450) % engine.W
            py = (p_i * 123 + t * 200) % engine.H
            fill_circle(ctx, px, py, 4 + (p_i % 4), WHITE, a=0.7)

        # Helipad 'H' on snow
        stroke_circle(ctx, 540, 1180, 120, RED, stroke_w=8)
        text(ctx, "H", 540, 1205, 110, RED, font=CAPTION_FONT, bold=True)

        # Header tag
        draw_card(ctx, 140, 320, 800, 110, 12, (0.05, 0.12, 0.2), SNOW_WHITE, stroke_w=4, a=0.92)
        text(ctx, "SIACHEN GLACIER : 4,700 METERS", 540, 370, 38, SNOW_WHITE, font=MONO, bold=True)
        text(ctx, "TOUCHDOWN WITH 500 KG COMBAT PAYLOAD", 540, 410, 26, GOLD, font=MONO, bold=True)

        # Prachand landing firmly on helipad
        land_prog = min(1.0, t / (d * 0.5))
        py = 780 + land_prog * 320
        draw_prachand_helicopter(ctx, 540, py, scale=1.35, t=t, rotor_speed=1.6)

        # Snow rotor wash blast rings
        if land_prog > 0.8:
            for w_r in (80, 160, 240):
                blast_r = w_r + (t * 120) % 180
                ctx.save()
                ctx.translate(540, 1200)
                ctx.scale(1.0, 0.3)
                stroke_circle(ctx, 0, 0, blast_r, WHITE, stroke_w=6, a=max(0, 1.0 - blast_r / 400))
                ctx.restore()


class WeaponsArsenalScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"top": c("TOP", 0.6), "rocket": c("ROCKET", d * 0.4), "desi": c("DESI", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["top"], "boom"), (b["rocket"], "zap"), (b["desi"], "pick")]

    def draw(self, ctx, t, d):
        # Dark tactical military background
        grad = cairo.LinearGradient(0, 0, 0, engine.H)
        grad.add_color_stop_rgb(0, 0.04, 0.06, 0.08)
        grad.add_color_stop_rgb(0.5, 0.12, 0.08, 0.06)
        grad.add_color_stop_rgb(1.0, 0.04, 0.05, 0.06)
        ctx.set_source(grad)
        ctx.paint()

        # HUD Crosshair overlay
        cx, cy = 540, 850
        stroke_circle(ctx, cx, cy, 260, HUD_GREEN, stroke_w=3, a=0.6)
        draw_line(ctx, cx - 290, cy, cx + 290, cy, c=HUD_GREEN, w=2, a=0.6)
        draw_line(ctx, cx, cy - 290, cx, cy + 290, c=HUD_GREEN, w=2, a=0.6)

        # Title Card
        text(ctx, "PRACHAND FIREPOWER", 540, 320, 54, FIRE_ORANGE, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=8)
        text(ctx, "20MM TURRET CANNON + 70MM ROCKET VOLLEY", 540, 385, 30, GOLD, font=MONO, bold=True)

        # Prachand firing cannon and rockets!
        draw_prachand_helicopter(ctx, 480, 820, scale=1.45, t=t, rotor_speed=2.0, firing=True)

        # Flying 70mm rockets streak across screen
        for r_i in range(3):
            rx = 350 - (t * 800 + r_i * 180) % 900
            ry = 860 + r_i * 35
            # Smoke trail
            draw_line(ctx, rx + 140, ry, rx, ry, c=(0.8, 0.8, 0.8), w=8, a=0.6)
            # Rocket fire
            draw_line(ctx, rx + 30, ry, rx, ry, c=FIRE_ORANGE, w=10)
            fill_circle(ctx, rx, ry, 6, GOLD)

        # Target bunker explosion in distance
        ex_x, ex_y = 120, 870
        fill_circle(ctx, ex_x, ex_y, 45 + math.sin(t * 20.0) * 15, FIRE_ORANGE, a=0.85)
        fill_circle(ctx, ex_x, ex_y, 25, GOLD)

        # Badge: 100% DESI WEAPONS INTEGRATION
        draw_badge(ctx, "INDIGENOUS WEAPONS INTEGRATION", 540, 1380, SAFFRON)


class MegaOrderScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"order": c("ORDER", 0.7), "156": c("156", d * 0.4), "khep": c("KHEP", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["order"], "pick"), (b["156"], "boom"), (b["khep"], "pop")]

    def draw(self, ctx, t, d):
        # Patriotic golden twilight sky
        grad = cairo.LinearGradient(0, 0, 0, engine.H)
        grad.add_color_stop_rgb(0, 0.08, 0.06, 0.14)
        grad.add_color_stop_rgb(0.4, 0.28, 0.14, 0.08)
        grad.add_color_stop_rgb(0.7, 0.18, 0.12, 0.08)
        grad.add_color_stop_rgb(1.0, 0.05, 0.06, 0.08)
        ctx.set_source(grad)
        ctx.paint()

        # Mountains silhouette
        draw_mountain_ridges(ctx, t)

        # Huge "156 PRACHAND" Order Card
        draw_card(ctx, 120, 310, 840, 180, 20, (0.05, 0.08, 0.14), GOLD, stroke_w=6, a=0.94)
        text(ctx, "MEGA DEFENSE ORDER", 540, 365, 36, SAFFRON, font=MONO, bold=True)
        text(ctx, "156 LCH PRACHAND", 540, 440, 68, GOLD, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=10)

        # 3-Helicopter formation flight
        # Lead helicopter
        draw_prachand_helicopter(ctx, 540, 840, scale=1.2, t=t, rotor_speed=1.5)
        # Wingman 1 (top right)
        draw_prachand_helicopter(ctx, 800, 720, scale=0.85, t=t + 0.3, rotor_speed=1.4)
        # Wingman 2 (top left)
        draw_prachand_helicopter(ctx, 280, 720, scale=0.85, t=t + 0.6, rotor_speed=1.4)

        # Service branch badges
        draw_card(ctx, 150, 1150, 360, 90, 10, (0.04, 0.08, 0.15), HUD_GREEN, stroke_w=3)
        text(ctx, "INDIAN ARMY", 330, 1190, 30, HUD_GREEN, font=MONO, bold=True)
        text(ctx, "90 HELICOPTERS", 330, 1225, 22, WHITE, font=MONO)

        draw_card(ctx, 570, 1150, 360, 90, 10, (0.04, 0.08, 0.15), CYAN, stroke_w=3)
        text(ctx, "INDIAN AIR FORCE", 750, 1190, 30, CYAN, font=MONO, bold=True)
        text(ctx, "66 HELICOPTERS", 750, 1225, 22, WHITE, font=MONO)


class CtaPollScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"taaqat": c("TAAQAT", 0.6), "comment": c("COMMENT", d * 0.4), "jaihind": c("HIND", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["taaqat"], "pick"), (b["comment"], "pop"), (b["jaihind"], "whoosh")]

    def draw(self, ctx, t, d):
        # Dramatic cinematic background with tricolor glow
        grad = cairo.LinearGradient(0, 0, 0, engine.H)
        grad.add_color_stop_rgb(0, 0.12, 0.05, 0.02)
        grad.add_color_stop_rgb(0.5, 0.04, 0.06, 0.12)
        grad.add_color_stop_rgb(1.0, 0.02, 0.08, 0.04)
        ctx.set_source(grad)
        ctx.paint()

        # Prachand hovering front-and-center
        draw_prachand_helicopter(ctx, 540, 720, scale=1.35, t=t, rotor_speed=1.8)

        # Tricolor ribbons in sky
        ctx.set_source_rgba(SAFFRON[0], SAFFRON[1], SAFFRON[2], 0.25)
        ctx.rectangle(0, 0, engine.W, 120)
        ctx.fill()
        ctx.set_source_rgba(INDIA_GREEN[0], INDIA_GREEN[1], INDIA_GREEN[2], 0.25)
        ctx.rectangle(0, engine.H - 120, engine.W, 120)
        ctx.fill()

        # Poll Prompt Card
        py = 280
        draw_card(ctx, 120, py, 840, 150, 16, (0.04, 0.06, 0.1), GOLD, stroke_w=5, a=0.94)
        text(ctx, "PRACHAND KI SABSE BADI TAAQAT?", 540, py + 50, 42, GOLD, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=8)
        text(ctx, "16,000 FT LANDING  ya  DESI FIREPOWER?", 540, py + 110, 32, WHITE, font=MONO, bold=True)

        # Bottom Call To Action Arrow pointing down to comment button
        draw_card(ctx, 160, 1160, 760, 90, 12, (0.05, 0.1, 0.18), SAFFRON, stroke_w=4, a=0.92)
        text(ctx, "COMMENT MEIN 'JAI HIND' LIKHEN!", 540, 1215, 36, SAFFRON, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=8)

        # Animated pointer arrow
        arrow_y = 1270 + math.sin(t * 8.0) * 12
        ctx.set_source_rgb(GOLD[0], GOLD[1], GOLD[2])
        ctx.move_to(540, arrow_y + 40)
        ctx.line_to(500, arrow_y)
        ctx.line_to(580, arrow_y)
        ctx.close_path()
        ctx.fill()


SCENE_CLASSES = {
    "kargil_need": KargilNeedScene,
    "birth_prachand": BirthPrachandScene,
    "high_altitude_record": HighAltitudeRecordScene,
    "siachen_landing": SiachenLandingScene,
    "weapons_arsenal": WeaponsArsenalScene,
    "mega_order": MegaOrderScene,
    "cta_poll": CtaPollScene,
}

UPLOAD = {
    "title": "Duniya Ka Akela Chopper Jo Siachen Mein Lad Sakta Hai! 🚁🇮🇳",
    "titles": [
        "Duniya Ka Akela Chopper Jo Siachen Mein Lad Sakta Hai! 🚁🇮🇳",
        "Apache Bhi Yahan Haanf Jata Hai: Bharat Ka LCH Prachand! 💥",
        "16,000 Feet Par Dushman Ka Kaal: LCH Prachand! 🚀",
        "1999 Kargil Se Janma Bharat Ka Sabse Ghatak Shikar: Prachand",
        "Siachen Mein 4700M Touchdown: HAL LCH Prachand Ka Khauf",
    ],
    "thumb_text": "LCH PRACHAND",
    "queries": ["lch prachand", "prachand helicopter", "prachand vs apache siachen"],
    "description": (
        "HAL LCH Prachand (Light Combat Helicopter) duniya ka akela attack chopper hai "
        "jo 5,000 meters (16,400 ft) ki unchai par pura weapons payload lekar utar bhi sakta hai aur udd bhi sakta hai! "
        "1999 Kargil yudh ke sabak se janma yeh desi shikar ab 156 helicopters ke sath Bharatiya Sena aur Vayusena ki shaan hai.\n\n"
        "#RealityShift #LCHPrachand #IndianAirForce #IndianArmy #MakeInIndia #Siachen #DefenseShorts #Shorts"
    ),
    "tags": [
        "LCH Prachand", "Light Combat Helicopter", "Indian Air Force", "Indian Army",
        "Siachen Glacier", "Prachand vs Apache", "Kargil war", "HAL Prachand",
        "Indian defense shorts", "Make in India defense", "reality shift"
    ],
    "hashtags": ["#Shorts", "#LCHPrachand", "#IndianArmy", "#IndianAirForce"],
}


def thumbnail(ctx):
    """1080x1920 cover: 'LCH PRACHAND' over high-altitude attack helicopter."""
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.05, 0.12, 0.22)
    g.add_color_stop_rgb(0.5, 0.18, 0.28, 0.38)
    g.add_color_stop_rgb(1.0, 0.05, 0.08, 0.12)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()

    draw_mountain_ridges(ctx, 0.0)
    draw_prachand_helicopter(ctx, 540, 850, 1.9, 0.5, firing=True)

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
    text(ctx, "LCH PRACHAND", 540, 290, 130, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "SIACHEN KA DESI SHIKARI", 540, 440, 75, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, INK, a=0.7)


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
    story = importlib.import_module("shorts.prachand")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
