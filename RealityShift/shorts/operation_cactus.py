"""Reality Shift Short — "Operation Cactus: 9 Ghante Me Maldives Rescue" (~50-55s).

Usage:
  python make.py operation_cactus --kiki-export
  python make.py operation_cactus --kiki-split
  python make.py operation_cactus --engine files
  python make.py operation_cactus --preview
  python make.py operation_cactus --kit

Historical overview:
On 3 November 1988, ~80 PLOTE mercenaries attempted a coup in the Maldives.
At the request of President Gayoom, the Indian Armed Forces executed Operation Cactus.
IAF IL-76 transport aircraft flew 2,000 km non-stop from Agra, landed on the unlit runway
at Hulhule, and 50th Parachute Brigade (Para SF) secured the capital and rescued the President
in under 9 hours with zero Indian casualties.
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
from shorts.brahmos_lego import tag
from shorts.chabahar import Cued
from shorts.reality_shift import flag, stamp

TOPIC = "OPERATION CACTUS MALDIVES RESCUE"
OUTPUTS = {"edge": "operation_cactus_short.mp4"}
LEGO = {"header": "radar", "caption": "chip", "transition": "scan", "palette": "glacier", "ending": "prompt"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.55
TAIL_PAD = 0.20
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 104
MUSIC_STYLE = "march"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 400

PAL = lego.PALETTES["glacier"]
UI = PAL["ui"]
HI = PAL["hi"]
RED = PAL["alert"]
INK = PAL["ink"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
STEEL = hexc("#90A4AE")
DARK_STEEL = hexc("#1A2530")
NIGHT_NAVY = hexc("#0A1118")
OCEAN_BLUE = hexc("#062038")
TROPICAL_TEAL = hexc("#00B4D8")
GOLD = hexc("#FFD700")
GREEN = hexc("#3DDC84")
MONO = "Consolas"

SOURCES = [
    "Operation Cactus (1988 Maldives Coup Intervention): 50th Parachute Brigade (6 PARA) and Indian Air Force "
    "Il-76 transport aircraft executed a 2,000 km non-stop airborne assault into Hulhule Airport within 9 hours "
    "of President Maumoon Abdul Gayoom's distress call (Ministry of Defence, Indian Army Historical Division)",
    "Naval Operations: Indian Navy frigates INS Godavari and INS Betwa intercepted the fleeing mercenary freighter "
    "MV Progress Light, capturing mercenaries and hostages without loss of Indian personnel (Indian Navy Records)",
    "International Geopolitical Recognition: Operation praised by US President Ronald Reagan and UK Prime Minister "
    "Margaret Thatcher, establishing India as the net security provider in the Indian Ocean region (SIPRI, IDSA)",
]

SPEC = [
    {"key": "night", "accent": RED, "text": "3 NOV 1988: ATTACK ON MALE",
     "visual": "Night skyline of Male, gunfire muzzle flashes, red tracer bullets slicing through palm trees and ocean",
     "vo": [("tell", [("3 नवंबर 1988 की रात,", "3 NOV 1988 KI RAAT,"),
                      ("जब मालदीव की राजधानी माले में", "JAB MALDIVES KI RAJDHANI MALE MEIN"),
                      ("अचानक गोलियों से", "ACHANAK GOLIYON SE"),
                      ("सन्नाटा टूट गया!", "SANNATA TOOT GAYA!")])]},

    {"key": "coup", "accent": RED, "text": "80 ARMED MERCENARIES",
     "visual": "Tactical island map of Male besieged by PLOTE mercenaries, President Gayoom safe house, rejected US/UK calls",
     "vo": [("tell", [("श्रीलंका के अस्सी से ज़्यादा", "SRI LANKA KE 80 SE ZYADA"),
                      ("भारी हथियारों से लैस विद्रोहियों ने", "BHARI HATHIYARON SE LAIS VIDROHIYON NE"),
                      ("पूरे देश पर कब्ज़ा कर लिया था।", "POORE DESH PAR KABZA KAR LIYA THA."),
                      ("राष्ट्रपति गयूम किसी तरह", "RASHTRAPATI GAYOOM KISI TARAH"),
                      ("एक सेफ हाउस में छिपे,", "EK SAFE HOUSE MEIN CHHIPE,"),
                      ("और उन्होंने अमेरिका और ब्रिटेन से", "AUR UNHONE US AUR UK SE"),
                      ("मदद मांगी,", "MADAD MANGI,"),
                      ("पर सबने हाथ खड़े कर दिए।", "PAR SABNE HAATH KHADE KAR DIYE.")])]},

    {"key": "call", "accent": SAFFRON, "text": "OPERATION CACTUS: GREEN LIGHT",
     "visual": "Red telephone distress line from Male to New Delhi; PM Rajiv Gandhi greenlights mission; OPERATION CACTUS stamp",
     "vo": [("tell", [("आखिरी उम्मीद में", "AAKHIRI UMEED MEIN"),
                      ("भारत से मदद मांगी गई,", "BHARAT SE MADAD MANGI GAYI,"),
                      ("और शुरू हुआ", "AUR SHURU HUA"),
                      ("भारतीय सेना का", "BHARATIYA SENA KA"),
                      ("सबसे जांबाज मिशन—", "SABSE JAANBAZ MISSION—"),
                      ("ऑपरेशन कैक्टस!", "OPERATION CACTUS!")])]},

    {"key": "airlift", "accent": STEEL, "text": "AGRA AIRBASE: IL-76 TAKEOFF",
     "visual": "IAF Ilyushin IL-76 Gajraj heavy transport aircraft roaring down Agra runway into the stormy night sky",
     "vo": [("tell", [("आगरा से वायुसेना के", "AGRA SE VAYUSENA KE"),
                      ("दो इल्युशिन छिहत्तर विमान", "DO ILYUSHIN 76 VIMAN"),
                      ("फिफ्टीथ पैराशूट ब्रिगेड के", "50TH PARACHUTE BRIGADE KE"),
                      ("पैरा कमांडोज़ को लेकर उड़े।", "PARA COMMANDOS KO LEKAR UDE.")])]},

    {"key": "landing", "accent": TROPICAL_TEAL, "text": "2,000 KM NON-STOP AIRLIFT",
     "visual": "Strategic map tracing 2,000 km non-stop flight from Agra to unlit Hulhule runway; pitch-black touchdown",
     "vo": [("tell", [("बिना किसी नेविगेशन लाइट के,", "BINA KISI NAVIGATION LIGHT KE,"),
                      ("दो हज़ार किलोमीटर की", "2,000 KM KI"),
                      ("नॉन-स्टॉप उड़ान भरकर", "NON-STOP UDAAN BHARKAR"),
                      ("कमांडोज़ सीधे", "COMMANDOS SEEDHE"),
                      ("हुलहुले की अंधेरी रनवे पर उतरे।", "HULHULE KI ANDHERI RUNWAY PAR UTRE.")])]},

    {"key": "assault", "accent": SAFFRON, "text": "PARA SF COMBAT ASSAULT",
     "visual": "Para SF commandos in speedboats storming across the lagoon from Hulhule to Male, suppressing mercenaries",
     "vo": [("tell", [("उतरते ही", "UTARTE HI"),
                      ("पैरा एसएफ के जवानों ने", "PARA SF KE JAWANON NE"),
                      ("एयरपोर्ट सील किया,", "AIRPORT SEAL KIYA,"),
                      ("और माले पहुँचकर", "AUR MALE PAHUNCHKAR"),
                      ("आतंकियों पर काल बनकर टूट पड़े!", "AATANKIYON PAR KAAL BANKAR TOOT PADE!")])]},

    {"key": "victory", "accent": INDIA_GREEN, "text": "9 HOURS: PRESIDENT SECURED",
     "visual": "9-hour mission clock locked; mercenaries disarmed; President Gayoom rescued; ZERO CASUALTY gold badge",
     "vo": [("tell", [("सिर्फ नौ घंटे के भीतर", "SIRF 9 GHANTE KE BHEETAR"),
                      ("सारे विद्रोही ढेर करके", "SAARE VIDROHI DHER KARKE"),
                      ("राष्ट्रपति को बचा लिया गया,", "RASHTRAPATI KO BACHA LIYA GAYA,"),
                      ("वो भी बिना एक भी जवान खोए!", "WO BHI BINA EK BHI JAWAN KHOYE!")])]},

    {"key": "ask", "accent": HI, "text": "NET SECURITY PROVIDER?",
     "visual": "Indian Armed Forces tri-service crest, glowing Indian Ocean radar, comment prompt card",
     "vo": [("ask", [("सेना की इस रफ़्तार पर", "SENA KI IS RAFTAAR PAR"),
                     ("क्या आपको गर्व है?", "KYA AAPKO GARV HAI?"),
                     ("कमेंट में बताएं,", "COMMENT MEIN BATAYEIN,"),
                     ("और सब्सक्राइब करें रियलिटी शिफ्ट!", "AUR SUBSCRIBE KAREIN REALITY SHIFT!"),
                     ("जय हिंद!", "JAI HIND!")])]},
]

DELIVERY = delivery.build(SPEC)
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "3": RED, "NOV": RED, "1988": RED, "RAAT,": RED, "MALDIVES": TROPICAL_TEAL, "MALE": TROPICAL_TEAL,
    "GOLIYON": RED, "SANNATA": STEEL, "80": RED, "MERCENARIES": RED, "VIDROHIYON": RED, "KABZA": RED,
    "GAYOOM": HI, "SAFE": STEEL, "HOUSE": STEEL, "US": STEEL, "UK": STEEL, "MADAD": SAFFRON,
    "BHARAT": SAFFRON, "MISSION—": SAFFRON, "OPERATION": SAFFRON, "CACTUS!": SAFFRON, "AGRA": SAFFRON,
    "VAYUSENA": STEEL, "ILYUSHIN": STEEL, "76": STEEL, "50TH": SAFFRON, "PARACHUTE": SAFFRON, "BRIGADE": SAFFRON,
    "PARA": SAFFRON, "COMMANDOS": SAFFRON, "2,000": GOLD, "KM": GOLD, "NON-STOP": GOLD, "UDAAN": GOLD,
    "HULHULE": TROPICAL_TEAL, "RUNWAY": STEEL, "UTRE.": STEEL, "SF": SAFFRON, "AIRPORT": STEEL,
    "SEAL": RED, "AATANKIYON": RED, "KAAL": RED, "TOOT": RED, "9": GOLD, "GHANTE": GOLD,
    "DHER": RED, "RASHTRAPATI": HI, "BACHA": INDIA_GREEN, "BINA": INDIA_GREEN, "KHOYE!": INDIA_GREEN,
    "SENA": SAFFRON, "RAFTAAR": GOLD, "GARV": SAFFRON, "COMMENT": HI, "SUBSCRIBE": HI, "JAI": SAFFRON, "HIND!": SAFFRON
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".—")] = HOT[_k]


# ============================================================ DRAWING PRIMITIVES

def night_ocean_bg(ctx, t):
    """Deep tropical night ocean background with starry sky and subtle waves."""
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.01, 0.02, 0.05)
    g.add_color_stop_rgb(0.5, 0.015, 0.035, 0.08)
    g.add_color_stop_rgb(1.0, 0.005, 0.015, 0.03)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()

    # Tactical grid
    for x in range(0, W + 1, 120):
        line(ctx, [(x, 0), (x, H)], UI, 1, 0.03)
    for y in range(0, H + 1, 120):
        line(ctx, [(0, y), (W, y)], UI, 1, 0.03)

    # Distant twinkling stars in night sky
    for i in range(24):
        sx = (i * 89 + 37) % W
        sy = (i * 53 + 71) % 650
        circle(ctx, sx, sy, 1.5, INK, 0.2 + 0.3 * math.sin(t * 3 + i))


def il76_aircraft(ctx, x, y, s, t, angle=0.0):
    """Procedural Indian Air Force IL-76 Gajraj heavy transport aircraft."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(angle)
    ctx.scale(s, s)

    # Shadow underneath
    ctx.save()
    ctx.scale(1.0, 0.25)
    circle(ctx, 0, 180, 220, (0, 0, 0), 0.4)
    ctx.restore()

    # Fuselage main body
    ctx.save()
    rrect(ctx, -220, -28, 440, 56, 26)
    rgba(ctx, STEEL)
    ctx.fill()
    # Fuselage cockpit nose cone
    rrect(ctx, 160, -22, 70, 44, 18)
    rgba(ctx, DARK_STEEL)
    ctx.fill()
    ctx.restore()

    # Glass cockpit windows
    for wx in range(180, 220, 10):
        rrect(ctx, wx, -12, 6, 12, 2)
        rgba(ctx, UI, 0.8)
        ctx.fill()

    # Main Swept Wings
    ctx.move_to(-20, -20)
    ctx.line_to(-160, -240)
    ctx.line_to(-90, -240)
    ctx.line_to(70, -20)
    ctx.close_path()
    rgba(ctx, STEEL)
    ctx.fill()

    ctx.move_to(-20, 20)
    ctx.line_to(-160, 240)
    ctx.line_to(-90, 240)
    ctx.line_to(70, 20)
    ctx.close_path()
    rgba(ctx, STEEL)
    ctx.fill()

    # 4 Jet Turbofan Engines
    for ex, ey in [(-80, -110), (-40, -180), (-80, 110), (-40, 180)]:
        rrect(ctx, ex - 40, ey - 14, 75, 28, 12)
        rgba(ctx, DARK_STEEL)
        ctx.fill()
        # Engine exhaust glow
        circle(ctx, ex - 40, ey, 9, (1.0, 0.5, 0.1), 0.6 + 0.3 * math.sin(t * 15))

    # T-Tail Fin (Rear)
    ctx.move_to(-190, 0)
    ctx.line_to(-250, -80)
    ctx.line_to(-200, -80)
    ctx.line_to(-150, 0)
    ctx.close_path()
    rgba(ctx, DARK_STEEL)
    ctx.fill()

    # Indian Air Force Roundel (Saffron/White/Green)
    rx, ry = 40, 0
    circle(ctx, rx, ry, 16, SAFFRON)
    circle(ctx, rx, ry, 11, INK)
    circle(ctx, rx, ry, 6, INDIA_GREEN)

    ctx.restore()


def para_sf_badge(ctx, x, y, s, t):
    """50th Parachute Brigade / Para SF Winged Dagger emblem."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # Parachute open canopy
    ctx.move_to(-60, -20)
    ctx.curve_to(-50, -80, 50, -80, 60, -20)
    ctx.close_path()
    rgba(ctx, INK, 0.9)
    ctx.fill()
    ctx.set_line_width(3)
    rgba(ctx, SAFFRON)
    ctx.stroke()

    # Parachute suspension lines to center
    for lx in (-45, -20, 0, 20, 45):
        line(ctx, [(lx, -25), (0, 35)], SAFFRON, 2, 0.7)

    # Winged Dagger
    # Left wing
    ctx.move_to(-5, 10)
    ctx.line_to(-80, -5)
    ctx.line_to(-30, 25)
    ctx.close_path()
    rgba(ctx, GOLD, 0.85)
    ctx.fill()

    # Right wing
    ctx.move_to(5, 10)
    ctx.line_to(80, -5)
    ctx.line_to(30, 25)
    ctx.close_path()
    rgba(ctx, GOLD, 0.85)
    ctx.fill()

    # Central Combat Dagger (Balidan shape)
    line(ctx, [(0, -50), (0, 50)], STEEL, 4, 1.0)
    line(ctx, [(-15, 20), (15, 20)], GOLD, 4, 1.0)
    circle(ctx, 0, 50, 5, GOLD)

    ctx.restore()


def tropical_island_male(ctx, x, y, s, t, alert_mode=False):
    """Stylized tactical map view of Male & Hulhule Atolls."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # Turquoise coral reef lagoon glow
    circle(ctx, 0, 0, 220, TROPICAL_TEAL, 0.22)
    circle(ctx, 0, 0, 170, TROPICAL_TEAL, 0.35)

    # Male Island (Capital)
    rrect(ctx, -130, -50, 110, 100, 24)
    rgba(ctx, (0.15, 0.25, 0.2) if not alert_mode else (0.4, 0.08, 0.08))
    ctx.fill()
    line(ctx, [(-130, -50), (-20, 50)], RED if alert_mode else UI, 2, 0.8)

    # Hulhule Island (Airport Runway)
    rrect(ctx, 40, -110, 55, 220, 16)
    rgba(ctx, DARK_STEEL)
    ctx.fill()
    # Runway centerline
    for ry in range(-90, 95, 25):
        line(ctx, [(67, ry), (67, ry + 14)], INK, 3, 0.9)

    tag(ctx, "MALE (CAPITAL)", -75, -80, RED if alert_mode else HI, 1.0, size=22)
    tag(ctx, "HULHULE (AIRPORT)", 67, 135, TROPICAL_TEAL, 1.0, size=22)

    # Gunfire muzzle flashes if alert
    if alert_mode:
        for i in range(4):
            fx = -110 + (i * 27)
            fy = -30 + (i * 21)
            pulse = 0.5 + 0.5 * math.sin(t * 18 + i * 3)
            circle(ctx, fx, fy, 12 * pulse, RED, 0.8)
            circle(ctx, fx, fy, 4, INK, 0.9)

    ctx.restore()


# ============================================================ SCENE CLASSES

class NightAttack(Cued):
    def beats(self, d):
        c = self.cue
        return {"goli": c("GOLIYON", 1.8), "break": c("SANNATA", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["goli"], "pop"), (b["goli"] + 0.3, "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_ocean_bg(ctx, t)
        tropical_island_male(ctx, 540, 680, 1.8, t, alert_mode=True)

        # Dramatic red tracers across sky
        for i in range(5):
            u = (t * 2.2 + i * 0.3) % 1.0
            tx0 = 320 + i * 40
            ty0 = 780 - i * 30
            tx1 = tx0 + 160 * u
            ty1 = ty0 - 140 * u
            line(ctx, [(tx0, ty0), (tx1, ty1)], RED, 3, 0.75)

        tag(ctx, "3 NOVEMBER 1988", 540, 310, RED, 1.0, size=46, sub="SURPRISE COUP IN MALDIVES")
        if t > b["goli"]:
            tag(ctx, "CAPITAL UNDER SIEGE", 540, 410, HI, t - b["goli"], size=36)


class MercenaryCoup(Cued):
    def beats(self, d):
        c = self.cue
        return {"mercs": c("MERCENARIES", 1.5), "safe": c("SAFE", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["mercs"], "pop"), (b["safe"], "pick")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_ocean_bg(ctx, t)
        tropical_island_male(ctx, 540, 650, 1.7, t, alert_mode=True)

        # Danger zone boundary
        circle(ctx, 540, 650, 340 + 20 * math.sin(t * 5), RED, 0.3)

        tag(ctx, "80+ ARMED MERCENARIES", 540, 300, RED, 1.0, size=44, sub="PLOTE TAMIL MILITANTS")
        tag(ctx, "PRESIDENT GAYOOM: IN HIDING", 540, 390, HI, 1.0, size=32)

        # Rejected help indicators (USA / UK Crossed out)
        for idx, (nation, nx) in enumerate([("USA: UNABLE", 340), ("UK: TOO FAR", 740)]):
            rrect(ctx, nx - 120, 1020, 240, 60, 12)
            rgba(ctx, DARK_STEEL, 0.8)
            ctx.fill()
            text(ctx, nation, nx, 1060, 26, STEEL, font=MONO, bold=True)
            line(ctx, [(nx - 110, 1070), (nx + 110, 1030)], RED, 4, 0.85)


class DistressCall(Cued):
    def beats(self, d):
        c = self.cue
        return {"call": c("MADAD", 1.2), "cactus": c("CACTUS!", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["call"], "pick"), (b["cactus"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_ocean_bg(ctx, t)

        # Hotline connection between Male and New Delhi
        line(ctx, [(540, 950), (540, 520)], SAFFRON, 3, 0.6)
        pulse_y = 950 - ((t * 350) % 430)
        circle(ctx, 540, pulse_y, 14, HI, 0.9)

        tag(ctx, "NEW DELHI: SOS RECEIVED", 540, 300, SAFFRON, 1.0, size=40)
        circle(ctx, 540, 520, 45, SAFFRON, 0.9)
        text(ctx, "PMO", 540, 532, 28, INK, font=MONO, bold=True)

        if t > b["cactus"]:
            stamp(ctx, 540, 750, t - b["cactus"], -0.04, 640, 130, SAFFRON, [("OPERATION CACTUS", 0, 74, SAFFRON)])
            tag(ctx, "ORDER: IMMEDIATE MILITARY RESCUE", 540, 840, GREEN, t - b["cactus"], size=30)


class Airlift(Cued):
    def beats(self, d):
        c = self.cue
        return {"agra": c("AGRA", 1.2), "para": c("PARA", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["agra"], "pop"), (b["para"], "pick")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_ocean_bg(ctx, t)

        # IL-76 roaring forward into the sky
        progress = clamp(t / d, 0.0, 1.0)
        plane_y = 780 - (progress * 180)
        il76_aircraft(ctx, 540, plane_y, 1.45, t, angle=-0.08)

        # Jet wash / vapor trails
        for off in (-180, -110, 110, 180):
            line(ctx, [(540 + off * 1.45, plane_y + 40), (540 + off * 1.45, plane_y + 260)], STEEL, 3, 0.25)

        tag(ctx, "AGRA AIRBASE: 2X IL-76 GAJRAJ", 540, 300, STEEL, 1.0, size=40)
        tag(ctx, "50TH PARACHUTE BRIGADE (PARA SF)", 540, 380, SAFFRON, 1.0, size=32)


class NonStopLanding(Cued):
    def beats(self, d):
        c = self.cue
        return {"dist": c("2,000", 1.4), "hulhule": c("HULHULE", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["dist"], "pop"), (b["hulhule"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_ocean_bg(ctx, t)

        # 2,000 KM Strategic Arc from India down to Maldives
        line(ctx, [(540, 480), (540, 880)], SAFFRON, 3, 0.5)
        # Radar calipers
        line(ctx, [(440, 480), (640, 480)], SAFFRON, 2, 0.8)
        line(ctx, [(440, 880), (640, 880)], TROPICAL_TEAL, 2, 0.8)

        text(ctx, "AGRA / INDIA", 540, 460, 26, SAFFRON, font=MONO, bold=True)
        text(ctx, "HULHULE RUNWAY", 540, 915, 26, TROPICAL_TEAL, font=MONO, bold=True)

        tag(ctx, "2,000 KM NON-STOP AIRLIFT", 540, 300, GOLD, 1.0, size=44, sub="LIGHTS-OUT COMBAT DESCENT")

        # IL-76 approaching dark runway
        il76_aircraft(ctx, 540, 680, 0.95, t, angle=0.0)

        if t > b["hulhule"]:
            tag(ctx, "TOUCHDOWN: PITCH-BLACK RUNWAY", 540, 1020, GREEN, t - b["hulhule"], size=34)


class CombatAssault(Cued):
    def beats(self, d):
        c = self.cue
        return {"sf": c("SF", 1.2), "male": c("MALE", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["sf"], "pop"), (b["male"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_ocean_bg(ctx, t)

        # Para SF Badge glowing centrally
        para_sf_badge(ctx, 540, 640, 2.0, t)

        tag(ctx, "PARA SF ASSAULT INITIATED", 540, 300, SAFFRON, 1.0, size=42)
        tag(ctx, "SPEEDBOATS STORM THE LAGOON", 540, 380, TROPICAL_TEAL, 1.0, size=32)

        # Tactical status indicators
        for i, task in enumerate(["AIRPORT SECURED", "COMMUNICATION RESTORED", "MALE PERIMETER CORDON"]):
            ty = 940 + i * 50
            rrect(ctx, 240, ty - 26, 600, 44, 8)
            rgba(ctx, DARK_STEEL, 0.85)
            ctx.fill()
            circle(ctx, 270, ty - 4, 8, GREEN)
            text(ctx, task, 300, ty + 4, 22, INK, font=MONO, bold=True, anchor="l")


class MissionAccomplished(Cued):
    def beats(self, d):
        c = self.cue
        return {"hours": c("9", 1.2), "safe": c("BACHA", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["hours"], "pop"), (b["safe"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_ocean_bg(ctx, t)

        # 9 Hours Clock Badge
        rrect(ctx, 270, 520, 540, 180, 24)
        rgba(ctx, DARK_STEEL, 0.9)
        ctx.fill()
        line(ctx, [(270, 520), (810, 520)], GOLD, 4, 1.0)
        text(ctx, "MISSION TIME: 09:00:00", 540, 580, 34, GOLD, font=MONO, bold=True)
        text(ctx, "PRESIDENT GAYOOM RESCUED", 540, 640, 30, GREEN, font=MONO, bold=True)

        stamp(ctx, 540, 780, t - b["hours"], -0.03, 560, 120, GREEN, [("ZERO CASUALTY", 0, 86, GREEN)])

        tag(ctx, "TOTAL MISSION TIME: 9 HOURS", 540, 300, GOLD, 1.0, size=44)
        tag(ctx, "GLOBAL RECOGNITION: USA & UK PRAISE", 540, 380, HI, 1.0, size=30)


class Ask(Cued):
    def beats(self, d):
        c = self.cue
        return {"garv": c("GARV", 1.2), "sub": c("SUBSCRIBE", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["garv"], "pop"), (b["sub"], "pick")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_ocean_bg(ctx, t)

        # Glowing Ashoka Chakra / Flag in center
        flag(ctx, 420, 520, 240, 160, "india", 0.0)

        tag(ctx, "OPERATION CACTUS: 1988", 540, 320, SAFFRON, 1.0, size=46)
        tag(ctx, "INDIAN ARMED FORCES PRIDE", 540, 420, HI, 1.0, size=34)

        # Comment prompt card
        rrect(ctx, 160, 760, 760, 200, 20)
        rgba(ctx, DARK_STEEL, 0.95)
        ctx.fill()
        line(ctx, [(160, 760), (920, 760)], SAFFRON, 4, 1.0)
        text(ctx, "KNOW MORE ABOUT OPERATION CACTUS?", 540, 820, 28, INK, font=MONO, bold=True)
        text(ctx, "COMMENT KARO - JAI HIND!", 540, 880, 34, GOLD, font=MONO, bold=True)

        # Pointer arrow to Shorts comment icon
        arrow_x = 880 + 15 * math.sin(t * 8)
        line(ctx, [(arrow_x, 920), (arrow_x + 50, 920)], HI, 4, 0.9)
        ctx.move_to(arrow_x + 50, 920)
        ctx.line_to(arrow_x + 35, 905)
        ctx.line_to(arrow_x + 35, 935)
        ctx.close_path()
        rgba(ctx, HI)
        ctx.fill()


SCENE_CLASSES = {
    "night": NightAttack,
    "coup": MercenaryCoup,
    "call": DistressCall,
    "airlift": Airlift,
    "landing": NonStopLanding,
    "assault": CombatAssault,
    "victory": MissionAccomplished,
    "ask": Ask,
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
        "Operation Cactus: 9 Ghante Mein Maldives Ko Kaise Bachaya?",
        "Jab Indian Army Ne 9 Ghante Mein Maldives Azaad Karaya!",
        "Operation Cactus 1988: Indian Para SF Ka Sabse Bada Mission",
        "Maldives Coup 1988: Jab Bharat Ne Bachayi Maldives Ki Sarkar",
        "2,000 KM Non-Stop Flight: Indian Air Force Ka Masterstroke",
        "Operation Cactus: America Aur Britain Bhi Dekh Kar Dang Reh Gaye",
        "Indian Army Maldives Operation: Zero Casualty World Record",
        "Operation Cactus: Bharat Ka Sabse Tez International Rescue",
    ],
    "title": "Operation Cactus: 9 Ghante Mein Maldives Ko Kaise Bachaya?",
    "thumb_text": "9 GHANTE",
    "queries": ["operation cactus", "operation cactus maldives 1988", "indian army maldives operation"],
    "description": """Operation Cactus 1988: 3 November 1988 ko jab Maldives ki rajdhani Male par 80 se zyada PLOTE mercenaries ne kabza kar liya, tab Indian Armed Forces ne itihaas ka sabse tez international airborne rescue mission anjaam diya.

Agra Airbase se IAF ke do Il-76 viman 50th Parachute Brigade ke Para SF jawano ko lekar 2,000 km non-stop udey, Hulhule airport ki andheri runway par land kiya, aur akele 9 ghante ke bheetar poore desh ko azaad karaya—bina apna ek bhi jawan khoye!

Is Short me:
• 3 Nov 1988: Maldives par achanak mercenary attack
• President Gayoom ka Bharat se madad mangna
• Agra se 2,000 KM ki non-stop lights-out flight
• Hulhule airport aur Male par Para SF ka combat assault
• 9 ghante me poora mission safal aur Zero Indian Casualty

Aapko Bharat ke is shandar military mission par kitna garv hai? Comment me likho - Jai Hind!
Subscribe to Reality Shift for hard-hitting defence and geopolitical analysis.

Sources: Indian Army Historical Division, Ministry of Defence, Indian Navy Records, SIPRI.
""",
    "tags": ["operation cactus", "maldives 1988", "indian army", "para sf", "indian air force", "il76",
             "president gayoom", "male coup", "indian defence shorts", "geopolitics hindi",
             "bharat news shorts", "reality shift"],
    "hashtags": ["#Shorts", "#OperationCactus", "#IndianArmy", "#IndianAirForce"],
}


def thumbnail(ctx):
    """1080x1920 cover: '9 GHANTE' over IL-76 aircraft and Maldives lagoon."""
    night_ocean_bg(ctx, 0.5)
    il76_aircraft(ctx, 540, 750, 1.5, 0.5, angle=-0.05)
    para_sf_badge(ctx, 540, 1150, 1.6, 0.5)

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
    text(ctx, "9 GHANTE", 540, 290, 180, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "OPERATION CACTUS", 540, 480, 95, INK, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    tag(ctx, "MALDIVES RESCUE 1988", 540, 600, SAFFRON, 1.0, size=38)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, INK, a=0.7)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.operation_cactus")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()

