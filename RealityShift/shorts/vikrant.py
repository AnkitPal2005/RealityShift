"""Reality Shift Short: INS Vikrant — 45,000 Tonne Ka Tairta Kila.

Topic: INS Vikrant Aircraft Carrier - India's 45,000-Tonne Indigenous Flagship
Format: Vertical 1080x1920 (9:16) for YouTube Shorts
Audio: KikiVoice narrator audio (34.85s), aligned and split via Whisper
Visuals: Procedural Cairo animations, deep ocean waves & ship wake, 14-degree ski-jump,
         carrier flight deck, MiG-29K jet launch, AK-630 CIWS Gatling intercept, sonar sub-hunt.
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

TOPIC = "INS VIKRANT AIRCRAFT CARRIER"
OUTPUTS = {"edge": "vikrant_short.mp4"}
LEGO = {"header": "radar", "caption": "chip", "transition": "shutter", "palette": "glacier", "ending": "prompt"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.55
TAIL_PAD = 0.20
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 116
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
NAVY_GREY = hexc("#37474F")
DARK_NAVY = hexc("#1C2833")
HULL_GREY = hexc("#455A64")
DECK_GREY = hexc("#263238")
OCEAN_DEEP = hexc("#0A192F")
OCEAN_MID = hexc("#0D2538")
OCEAN_CYAN = hexc("#00B4D8")
FOAM_WHITE = hexc("#E0F7FA")
WHITE = (1.0, 1.0, 1.0)
FIRE_ORANGE = hexc("#FF5500")
GOLD = hexc("#FFD700")
HUD_GREEN = hexc("#00FF66")
CYAN = hexc("#00E5FF")
MONO = "Consolas"

SOURCES = [
    "Indian Navy (Directorate of Naval Design) - INS Vikrant (IAC-1) Design & Flight Deck Envelope",
    "Cochin Shipyard Limited (CSL) - 45,000-tonne Indigenous Aircraft Carrier Construction",
    "Naval Aviation - MiG-29K STOBAR Ski-Jump Operations & 3-Wire Arresting Gear Recovery",
    "DRDO & Bharat Electronics Limited (BEL) - MF-STAR Phased Array Radar & AK-630 CIWS",
]

SPEC = [
    # Scene 1: Chinese Fleet vs INS Vikrant Hook
    {"key": "carrier_race_hook", "accent": RED, "text": "INDIAN OCEAN SUPREMACY",
     "visual": "Dusk over high seas; INS Vikrant cutting through deep ocean swells with foaming bow wake; tactical telemetry identifies carrier",
     "vo": [("tell", [("चीन के पास चाहे जितने", "CHINA KE PAAS CHAHE JITNE"),
                      ("जंगी जहाज हों,", "JANGI JAHAZ HON,"),
                      ("लेकिन समंदर में भारत के", "LEKIN SAMANDAR MEIN BHARAT KE"),
                      ("आईएनएस विक्रांत का खौफ सबसे अलग है!", "INS VIKRANT KA KHAUF SABSE ALAG HAI!")])]},

    # Scene 2: 45,000-Tonne Warship Scale & MiG-29K Launch
    {"key": "warship_scale", "accent": GOLD, "text": "45,000-TONNE FLOATING FORTRESS",
     "visual": "Aerial zoom over flight deck with ski-jump bow, MiG-29K twin engines ignite with orange afterburner cones, launches off the ramp",
     "vo": [("tell", [("पानी पर तैरता ये", "PAANI PAR TAIRTA YE"),
                      ("भारत का सबसे बड़ा युद्धपोत है,", "BHARAT KA SABSE BADA YUDDHPOT HAI,"),
                      ("जिस पर लड़ाकू विमान और मिसाइलें", "JIS PAR LADAKU VIMAN AUR MISSILE-EIN"),
                      ("हर वक्त तैनात रहती हैं!", "HAR WAQT TAINAAT REHTI HAIN!")])]},

    # Scene 3: AK-630 CIWS 4,000 RPM Missile Intercept (The 15-18s Anti-Drop)
    {"key": "ciws_defense", "accent": FIRE_ORANGE, "text": "4,000 RPM POINT DEFENSE",
     "visual": "Incoming anti-ship cruise missile; AK-630 Gatling gun tracking target, glowing red-yellow tracer stream erupts, missile destroyed in mid-air",
     "vo": [("tell", [("अगर दुश्मन की कोई मिसाइल", "AGAR DUSHMAN KI KOI MISSILE"),
                      ("इसकी तरफ बढ़े,", "ISKI TARAF BADHE,"),
                      ("तो इसकी ऑटोमैटिक तोपें", "TO ISKI AUTOMATIC TOP-EIN"),
                      ("एक सेकंड में ही उसे आसमान में उड़ा देती हैं!", "EK SECOND MEIN HI USE AASMAAN MEIN UDA DETI HAIN!")])]},

    # Scene 4: Anti-Submarine Warfare Dominance
    {"key": "anti_submarine", "accent": CYAN, "text": "SUBMARINE HUNTER",
     "visual": "Subsea sonar screen with green/blue concentric acoustic rings; enemy submarine detected at 120m depth, crosshairs lock with zero escape",
     "vo": [("tell", [("हिंद महासागर में", "HIND MAHASAGAR MEIN"),
                      ("भारत की इजाज़त के बिना,", "BHARAT KI IJAZAT KE BINA,"),
                      ("दुश्मन की एक पनडुब्बी भी", "DUSHMAN KI EK PANDUBBI BHI"),
                      ("आगे नहीं बढ़ सकती!", "AAGE NAHI BADH SAKTI!")])]},

    # Scene 5: 3-Second Snap CTA
    {"key": "cta_poll", "accent": SAFFRON, "text": "INDIAN NAVY PRIDE",
     "visual": "INS Vikrant cruising into blazing golden-saffron sunset, Indian Naval flag fluttering, MiG-29K overhead with tricolor smoke trails",
     "vo": [("tell", [("क्या आप भारतीय नौसेना की", "KYA AAP BHARATIYA NAUSENA KI"),
                      ("ताकत पर गर्व करते हैं?", "TAAQAT PAR GARV KARTE HAIN?"),
                      ("कमेंट में जय हिंद लिखें", "COMMENT MEIN JAI HIND LIKHEIN"),
                      ("और सब्सक्राइब करें रियलिटी शिफ्ट!", "AUR SUBSCRIBE KAREIN REALITY SHIFT!")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "CHINA": RED, "JANGI": RED, "JAHAZ": RED, "SAMANDAR": CYAN,
    "BHARAT": SAFFRON, "INS": GOLD, "VIKRANT": GOLD, "KHAUF": RED,
    "PAANI": CYAN, "TAIRTA": CYAN, "YUDDHPOT": GOLD, "LADAKU": SAFFRON,
    "VIMAN": SAFFRON, "MISSILE-EIN": FIRE_ORANGE, "TAINAAT": HUD_GREEN,
    "DUSHMAN": RED, "MISSILE": FIRE_ORANGE, "AUTOMATIC": GOLD,
    "TOP-EIN": FIRE_ORANGE, "AASMAAN": CYAN, "HIND": SAFFRON,
    "MAHASAGAR": CYAN, "IJAZAT": GOLD, "PANDUBBI": RED, "AAGE": RED,
    "NAUSENA": SAFFRON, "TAAQAT": GOLD, "GARV": SAFFRON, "COMMENT": HI,
    "JAI": SAFFRON, "SUBSCRIBE": SAFFRON, "REALITY": CYAN, "SHIFT": CYAN
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
# PROCEDURAL DRAWING ROUTINES (INS Vikrant, Ocean Wake & MiG-29K)
# ============================================================

def ocean_surface(ctx, t, sunset=False, storm=False):
    """Multi-layered deep ocean simulation with swells, rolling whitecaps, and sea spray."""
    # Sky Gradient
    pat_sky = cairo.LinearGradient(0, 0, 0, 960)
    if sunset:
        pat_sky.add_color_stop_rgb(0.0, 0.08, 0.04, 0.12)
        pat_sky.add_color_stop_rgb(0.45, 0.45, 0.18, 0.08)
        pat_sky.add_color_stop_rgb(0.85, 0.95, 0.55, 0.18)
        pat_sky.add_color_stop_rgb(1.0, 0.85, 0.42, 0.15)
    else:
        pat_sky.add_color_stop_rgb(0.0, 0.02, 0.06, 0.14)
        pat_sky.add_color_stop_rgb(0.5, 0.08, 0.16, 0.28)
        pat_sky.add_color_stop_rgb(1.0, 0.14, 0.28, 0.44)
    ctx.set_source(pat_sky)
    ctx.rectangle(0, 0, W, 960)
    ctx.fill()

    # Sun or Moon disk on horizon
    if sunset:
        glow(ctx, 540, 820, 240, hexc("#FF7A00"), 0.55)
        circle(ctx, 540, 820, 55, hexc("#FFE082"), 0.9)
    else:
        glow(ctx, 800, 420, 180, CYAN, 0.35)
        circle(ctx, 800, 420, 42, WHITE, 0.85)

    # Ocean Base (From Horizon 960 down to Bottom 1920)
    pat_ocean = cairo.LinearGradient(0, 960, 0, H)
    pat_ocean.add_color_stop_rgb(0.0, 0.05, 0.15, 0.24)
    pat_ocean.add_color_stop_rgb(0.5, 0.03, 0.09, 0.18)
    pat_ocean.add_color_stop_rgb(1.0, 0.01, 0.04, 0.10)
    ctx.set_source(pat_ocean)
    ctx.rectangle(0, 960, W, H - 960)
    ctx.fill()

    # Multi-frequency rolling waves across ocean surface
    ctx.save()
    for wave_layer in range(4):
        wy = 980 + wave_layer * 220
        speed = (wave_layer + 1) * 35.0
        amp = 12.0 + wave_layer * 8.0
        ctx.move_to(0, wy)
        for x in range(0, W + 30, 20):
            y_wave = wy + amp * math.sin((x / 140.0) + (t * speed / 100.0) + wave_layer)
            ctx.line_to(x, y_wave)
        ctx.line_to(W, H)
        ctx.line_to(0, H)
        ctx.close_path()
        rgba(ctx, (0.02, 0.08, 0.15 + wave_layer * 0.03), 0.4)
        ctx.fill()

        # Foaming wave crest highlights
        for x in range(30, W - 30, 90):
            crest_x = (x + int(t * speed)) % W
            crest_y = wy + amp * math.sin((crest_x / 140.0) + (t * speed / 100.0) + wave_layer)
            line(ctx, [(crest_x - 22, crest_y), (crest_x + 22, crest_y)], FOAM_WHITE, 2.0, 0.35)
    ctx.restore()


def draw_carrier_wake(ctx, ship_x, ship_y, s, t):
    """Turbulent foaming V-shaped wake trailing behind the carrier."""
    ctx.save()
    ctx.translate(ship_x, ship_y)
    ctx.scale(s, s)

    # Expanding churned foam wake
    for k in range(8):
        wy = 220 + k * 85
        ww = 140 + k * 75
        drift = math.sin(t * 4.0 + k) * 12
        pat = cairo.RadialGradient(0, wy, 10, 0, wy, ww)
        pat.add_color_stop_rgba(0.0, 0.9, 0.98, 1.0, 0.65 - k * 0.06)
        pat.add_color_stop_rgba(0.6, 0.4, 0.8, 0.9, 0.35 - k * 0.04)
        pat.add_color_stop_rgba(1.0, 0.05, 0.2, 0.3, 0.0)
        ctx.set_source(pat)
        ell(ctx, drift, wy, ww, 40)
        ctx.fill()

    # Twin divergent bow wave lines
    line(ctx, [(-90, -180), (-320, 600)], FOAM_WHITE, 6.0, 0.5)
    line(ctx, [(90, -180), (320, 600)], FOAM_WHITE, 6.0, 0.5)
    ctx.restore()


def draw_ins_vikrant(ctx, x, y, s, t, ciws_firing=False, jet_on_deck=True, ski_launch=False):
    """High-detail procedural model of INS Vikrant (IAC-1).

    Features: 14-degree ski-jump ramp at the bow, angled flight deck,
    runway stripes, arresting cables, island superstructure with MF-STAR radar,
    Indian Naval flag, and AK-630 CIWS turrets.
    """
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # 1. Main Hull Silhouette (262m long carrier deck shape)
    # Bow -> Ski Jump -> Starboard Island sponson -> Stern -> Port Angled Deck -> Bow
    ctx.move_to(0, -320)          # Tapered bow ski-jump tip
    ctx.line_to(65, -300)         # Starboard ski-jump corner
    ctx.line_to(110, -140)        # Starboard forward sponson
    ctx.line_to(135, 60)          # Starboard island base sponson
    ctx.line_to(125, 260)         # Starboard aft sponson
    ctx.line_to(95, 330)          # Starboard stern corner
    ctx.line_to(-75, 330)         # Stern center aft
    ctx.line_to(-145, 180)        # Angled deck port sponson
    ctx.line_to(-125, -60)        # Port mid deck
    ctx.line_to(-80, -220)        # Port forward ski-jump corner
    ctx.close_path()

    # Naval Steel Non-Skid Deck Coating Gradient
    g_deck = cairo.LinearGradient(0, -320, 0, 330)
    g_deck.add_color_stop_rgb(0.0, 0.24, 0.30, 0.36)   # Bow steel
    g_deck.add_color_stop_rgb(0.4, 0.16, 0.20, 0.24)   # Mid deck non-skid
    g_deck.add_color_stop_rgb(1.0, 0.10, 0.13, 0.16)   # Aft dark steel
    ctx.set_source(g_deck)
    ctx.fill_preserve()

    # Outer hull chamfer border
    ctx.set_line_width(3.5)
    rgba(ctx, (0.5, 0.62, 0.72), 0.8)
    ctx.stroke()

    # 2. 14-Degree Ski-Jump Ramp at the Bow
    ctx.move_to(-65, -280)
    ctx.line_to(55, -280)
    ctx.line_to(45, -315)
    ctx.line_to(-55, -315)
    ctx.close_path()
    rgba(ctx, hexc("#2C3B47"), 0.95)
    ctx.fill_preserve()
    ctx.set_line_width(2.0)
    rgba(ctx, GOLD, 0.85)
    ctx.stroke()

    # Yellow Takeoff Guide Stripes on Ski-Jump
    line(ctx, [(0, -220), (0, -315)], GOLD, 3.5, 0.95)
    line(ctx, [(-18, -250), (-18, -310)], GOLD, 2.0, 0.75)
    line(ctx, [(18, -250), (18, -310)], GOLD, 2.0, 0.75)

    # 3. Angled Runway Flight Deck Lines
    # Landing strip centerline (angled ~8 degrees)
    ctx.save()
    line(ctx, [(-5, 310), (-75, -60)], WHITE, 4.0, 0.85)
    # Runway touch-down markings
    for mk in range(5):
        my = 260 - mk * 50
        mx = -12 - mk * 12
        line(ctx, [(mx - 24, my), (mx + 24, my)], WHITE, 3.0, 0.6)
    ctx.restore()

    # 4. Arresting Gear Wires (3 cables across aft deck)
    for w_i, wy in enumerate([210, 240, 270]):
        line(ctx, [(-100 + w_i * 6, wy - 10), (70, wy + 15)], (0.1, 0.1, 0.1), 3.0, 0.9)
        line(ctx, [(-100 + w_i * 6, wy - 10), (70, wy + 15)], (0.8, 0.85, 0.9), 1.0, 0.7)

    # 5. Starboard Island Superstructure (Command Bridge & Radars)
    # Island Base
    rrect(ctx, 65, -40, 52, 140, 8)
    rgba(ctx, hexc("#37474F"), 0.95)
    ctx.fill()
    rrect(ctx, 65, -40, 52, 140, 8)
    rgba(ctx, (0.6, 0.75, 0.85), 0.7)
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Command Bridge Windows (Tinted Cyan Glass)
    rrect(ctx, 70, -34, 42, 14, 3)
    rgba(ctx, CYAN, 0.85)
    ctx.fill()

    # MF-STAR Phased Array Radar (Rotating Octagonal Array)
    rad_ang = t * 3.5
    ctx.save()
    ctx.translate(91, 15)
    circle(ctx, 0, 0, 14, hexc("#212D36"), 0.95)
    circle(ctx, 0, 0, 14, GOLD, 0.8)
    ctx.set_line_width(1.5)
    ctx.stroke()
    line(ctx, [(-12 * math.cos(rad_ang), -12 * math.sin(rad_ang)),
               (12 * math.cos(rad_ang), 12 * math.sin(rad_ang))], HUD_GREEN, 2.5, 0.95)
    ctx.restore()

    # Main Mast & TACAN Antennas
    line(ctx, [(91, 35), (91, 105)], (0.2, 0.25, 0.3), 5.0, 0.95)
    line(ctx, [(80, 55), (102, 55)], (0.6, 0.7, 0.8), 2.5, 0.8)
    line(ctx, [(83, 75), (99, 75)], (0.6, 0.7, 0.8), 2.5, 0.8)

    # Fluttering Indian Naval Tricolor Ensign on Mast
    flag_wave = math.sin(t * 8.0) * 4
    ctx.save()
    ctx.translate(93, 100)
    # Saffron stripe
    rrect(ctx, 0, 0, 26, 6 + flag_wave * 0.3, 1)
    rgba(ctx, SAFFRON, 0.95)
    ctx.fill()
    # White stripe
    rrect(ctx, 0, 6, 26, 6 + flag_wave * 0.3, 1)
    rgba(ctx, WHITE, 0.95)
    ctx.fill()
    circle(ctx, 13, 9, 2.5, hexc("#000080"), 0.9)
    # Green stripe
    rrect(ctx, 0, 12, 26, 6 + flag_wave * 0.3, 1)
    rgba(ctx, INDIA_GREEN, 0.95)
    ctx.fill()
    ctx.restore()

    # 6. AK-630 CIWS 30mm Gatling Gun (Starboard Sponson)
    ciws_x, ciws_y = 125, -95
    circle(ctx, ciws_x, ciws_y, 11, hexc("#263238"), 0.95)
    circle(ctx, ciws_x, ciws_y, 11, FIRE_ORANGE, 0.8)
    ctx.set_line_width(1.5)
    ctx.stroke()
    if ciws_firing:
        # Muzzle flashes & rotating barrel tracer volley
        barrel_ang = -0.75 + math.sin(t * 35.0) * 0.15
        bx = ciws_x + 18 * math.cos(barrel_ang)
        by = ciws_y + 18 * math.sin(barrel_ang)
        line(ctx, [(ciws_x, ciws_y), (bx, by)], (0.1, 0.1, 0.1), 4.0, 0.95)
        # Blinding orange muzzle flash
        glow(ctx, bx, by, 45, FIRE_ORANGE, 0.9)
        circle(ctx, bx, by, 9, WHITE, 0.95)

    # 7. Parked / Taxiing MiG-29K Jets on Deck
    if jet_on_deck and not ski_launch:
        # Jet 1 parked on starboard aft
        draw_mig29k(ctx, 55, 180, 0.36, t, afterburner=False, angle_deg=-15.0)
        # Jet 2 lined up near ski-jump
        draw_mig29k(ctx, -10, -180, 0.40, t, afterburner=True, angle_deg=0.0)

    ctx.restore()


def draw_mig29k(ctx, x, y, s, t, afterburner=False, angle_deg=0.0):
    """Carrier-borne MiG-29K Fulcrum Naval Fighter."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if angle_deg != 0.0:
        ctx.rotate(math.radians(angle_deg))

    # Afterburner Plumes (RD-33MK Sea Wasp Engines)
    if afterburner:
        for ex in [-18, 18]:
            pat = cairo.RadialGradient(ex, 90, 4, ex, 140, 50)
            pat.add_color_stop_rgba(0.0, 1.0, 0.95, 0.5, 0.95)
            pat.add_color_stop_rgba(0.35, 1.0, 0.45, 0.0, 0.85)
            pat.add_color_stop_rgba(0.7, 0.0, 0.5, 1.0, 0.4)
            pat.add_color_stop_rgba(1.0, 0.0, 0.1, 0.6, 0.0)
            ctx.set_source(pat)
            ctx.arc(ex, 115, 38, 0, 2 * math.pi)
            ctx.fill()
            # Shock diamonds
            for sk in range(2):
                sy = 100 + sk * 20
                ctx.move_to(ex, sy - 6)
                ctx.line_to(ex + 6, sy)
                ctx.line_to(ex, sy + 6)
                ctx.line_to(ex - 6, sy)
                ctx.close_path()
                rgba(ctx, WHITE, 0.9)
                ctx.fill()

    # Airframe Outline
    ctx.move_to(0, -95)           # Radome nose tip
    ctx.line_to(22, -45)          # LERX right
    ctx.line_to(85, 35)           # Right wingtip
    ctx.line_to(80, 50)           # Aileron
    ctx.line_to(36, 50)           # Wing root
    ctx.line_to(28, 88)           # Right nozzle
    ctx.line_to(10, 88)           # Engine tunnel right
    ctx.line_to(0, 78)            # Beaver tail
    ctx.line_to(-10, 88)          # Engine tunnel left
    ctx.line_to(-28, 88)          # Left nozzle
    ctx.line_to(-36, 50)          # Wing root
    ctx.line_to(-80, 50)          # Aileron
    ctx.line_to(-85, 35)          # Left wingtip
    ctx.line_to(-22, -45)         # LERX left
    ctx.close_path()

    # Naval Air Superiority Grey Gradient
    g_mig = cairo.LinearGradient(0, -95, 0, 88)
    g_mig.add_color_stop_rgb(0.0, 0.35, 0.45, 0.55)
    g_mig.add_color_stop_rgb(0.5, 0.22, 0.28, 0.35)
    g_mig.add_color_stop_rgb(1.0, 0.14, 0.18, 0.22)
    ctx.set_source(g_mig)
    ctx.fill_preserve()
    ctx.set_line_width(2.0)
    rgba(ctx, (0.55, 0.70, 0.85), 0.8)
    ctx.stroke()

    # Twin Canted Vertical Fins
    for side in (-1, 1):
        ctx.move_to(side * 24, 30)
        ctx.line_to(side * 38, 82)
        ctx.line_to(side * 26, 86)
        ctx.line_to(side * 18, 45)
        ctx.close_path()
        rgba(ctx, (0.16, 0.22, 0.28), 0.95)
        ctx.fill()

    # Cockpit Canopy with Pilot Helmet
    pat_can = cairo.LinearGradient(0, -50, 0, -10)
    pat_can.add_color_stop_rgba(0.0, 0.2, 0.8, 1.0, 0.9)
    pat_can.add_color_stop_rgba(1.0, 0.05, 0.15, 0.25, 0.95)
    ctx.set_source(pat_can)
    ell(ctx, 0, -32, 9, 24)
    ctx.fill()
    circle(ctx, 0, -38, 4, WHITE, 0.9)  # White helmet

    # IAF Naval Tricolor Roundel on wings
    for rx in (-52, 52):
        circle(ctx, rx, 35, 9, SAFFRON)
        circle(ctx, rx, 35, 6, WHITE)
        circle(ctx, rx, 35, 3, INDIA_GREEN)

    ctx.restore()


def draw_ciws_tracers(ctx, x0, y0, x1, y1, t):
    """Stream of high-velocity 30mm tungsten tracer rounds firing at 4,000 RPM."""
    ctx.save()
    dist = math.hypot(x1 - x0, y1 - y0)
    ang = math.atan2(y1 - y0, x1 - x0)

    # 12 rapid pulse tracer bullet dashes
    for b_i in range(14):
        offset = ((t * 1400 + b_i * 95) % dist)
        bx = x0 + offset * math.cos(ang)
        by = y0 + offset * math.sin(ang)
        tx = bx + 28 * math.cos(ang)
        ty = by + 28 * math.sin(ang)

        # Glowing yellow-red incendiary core
        line(ctx, [(bx, by), (tx, ty)], FIRE_ORANGE, 4.5, 0.9)
        line(ctx, [(bx, by), (tx, ty)], (1.0, 0.95, 0.4), 2.0, 0.95)
        glow(ctx, tx, ty, 20, (1.0, 0.4, 0.0), 0.7)
    ctx.restore()


def draw_sonar_scope(ctx, x, y, r, t, sub_locked=True):
    """Subsea acoustic sonar PPI display searching ocean depths."""
    ctx.save()
    ctx.translate(x, y)

    # Sonar housing ring
    circle(ctx, 0, 0, r + 12, hexc("#101C24"), 0.95)
    circle(ctx, 0, 0, r + 12, (0.2, 0.4, 0.6), 0.8)
    ctx.set_line_width(3.0)
    ctx.stroke()

    # Dark blue-green underwater display
    circle(ctx, 0, 0, r, hexc("#021018"), 0.95)
    circle(ctx, 0, 0, r, CYAN, 0.7)
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Expanding acoustic sonar rings
    for k in range(3):
        ring_r = ((t * 70 + k * 90) % r)
        alpha = max(0.0, 1.0 - (ring_r / r))
        circle(ctx, 0, 0, ring_r, CYAN, 0.4 * alpha)
        ctx.set_line_width(1.5)
        ctx.stroke()

    # Crosshairs & Bearing tick marks
    line(ctx, [(-r, 0), (r, 0)], CYAN, 1.0, 0.25)
    line(ctx, [(0, -r), (0, r)], CYAN, 1.0, 0.25)

    # Locked Enemy Submarine Contact
    if sub_locked:
        sx, sy = r * 0.38, -r * 0.28
        # Red pulsing lock box
        box_s = 28 + 4 * math.sin(t * 8.0)
        rrect(ctx, sx - box_s / 2, sy - box_s / 2, box_s, box_s, 4)
        rgba(ctx, RED, 0.9)
        ctx.set_line_width(2.0)
        ctx.stroke()
        # Submarine acoustic silhouette
        ell(ctx, sx, sy, 18, 6)
        rgba(ctx, (1.0, 0.3, 0.3), 0.95)
        ctx.fill()
        text(ctx, "CONTACT: HOSTILE SUB", sx + 25, sy - 8, 16, RED, font=MONO, bold=True)
        text(ctx, "DEPTH: 120M / RANGE: 8NM", sx + 25, sy + 14, 14, GOLD, font=MONO)

    ctx.restore()


# ============================================================
# SCENE CLASSES (Strictly synchronized to KikiVoice 5 lines)
# ============================================================

class CarrierRaceHookScene(Cued):
    """Scene 1: China vs India naval supremacy; INS Vikrant cutting through ocean swells."""
    def beats(self, d):
        c = self.cue
        return {
            "china": c("CHINA", 0.6),
            "samandar": c("SAMANDAR", d * 0.4),
            "vikrant": c("VIKRANT", d * 0.7)
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["china"], "alarm"), (b["samandar"], "whoosh"), (b["vikrant"], "boom")]

    def draw(self, ctx, t, d):
        ocean_surface(ctx, t, sunset=False)

        # Tactical comparison banner at top
        rrect(ctx, 80, 240, 420, 105, 12)
        rgba(ctx, hexc("#1A0C0E"), 0.88)
        ctx.fill()
        rrect(ctx, 80, 240, 420, 105, 12)
        rgba(ctx, RED, 0.85)
        ctx.set_line_width(2.0)
        ctx.stroke()
        text(ctx, "CHINA CARRIER FLEET", 290, 280, 24, RED, font=MONO, bold=True)
        text(ctx, "3 CARRIERS IN PACIFIC", 290, 315, 18, (0.8, 0.8, 0.8), font=MONO)

        rrect(ctx, 580, 240, 420, 105, 12)
        rgba(ctx, hexc("#0C1A24"), 0.88)
        ctx.fill()
        rrect(ctx, 580, 240, 420, 105, 12)
        rgba(ctx, GOLD, 0.85)
        ctx.set_line_width(2.0)
        ctx.stroke()
        text(ctx, "INS VIKRANT (IAC-1)", 790, 280, 24, GOLD, font=MONO, bold=True)
        text(ctx, "LORD OF INDIAN OCEAN", 790, 315, 18, (0.8, 0.8, 0.8), font=MONO)

        # Carrier Wake & INS Vikrant sailing towards camera
        ship_sway = math.sin(t * 1.8) * 16
        draw_carrier_wake(ctx, 540 + ship_sway, 1220, 1.1, t)
        draw_ins_vikrant(ctx, 540 + ship_sway, 1180, 1.15, t, jet_on_deck=True)


class WarshipScaleScene(Cued):
    """Scene 2: 45,000-Tonne warship scale; MiG-29K ski-jump launch."""
    def beats(self, d):
        c = self.cue
        return {
            "yuddhpot": c("YUDDHPOT", 0.5),
            "viman": c("VIMAN", d * 0.45),
            "tainaat": c("TAINAAT", d * 0.75)
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["yuddhpot"], "whoosh"), (b["viman"], "engine", 1.8), (b["tainaat"], "shimmer")]

    def draw(self, ctx, t, d):
        ocean_surface(ctx, t, sunset=False)

        # Aerial view of INS Vikrant angled flight deck
        draw_carrier_wake(ctx, 540, 1050, 1.3, t)
        draw_ins_vikrant(ctx, 540, 1000, 1.35, t, jet_on_deck=False)

        # MiG-29K taking off off the ski-jump ramp into sky
        launch_t = (t * 1.6) % 3.0
        if launch_t < 1.0:
            # Accelerating on runway
            jx = 540 - launch_t * 20
            jy = 980 - launch_t * 280
            draw_mig29k(ctx, jx, jy, 0.48 + launch_t * 0.2, t, afterburner=True, angle_deg=-launch_t * 8)
        else:
            # Airborne climbing into air with high angle of attack
            air_t = launch_t - 1.0
            jx = 520 - air_t * 120
            jy = 700 - air_t * 360
            draw_mig29k(ctx, jx, jy, 0.68 + air_t * 0.35, t, afterburner=True, angle_deg=-18.0)


class CiwsDefenseScene(Cued):
    """Scene 3: AK-630 CIWS 4,000 RPM rotary cannon shoots down incoming anti-ship missile."""
    def beats(self, d):
        c = self.cue
        return {
            "dushman": c("DUSHMAN", 0.45),
            "automatic": c("AUTOMATIC", d * 0.4),
            "uda": c("AASMAAN", d * 0.75)
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["dushman"], "alarm"), (b["automatic"], "whoosh"), (b["uda"], "boom")]

    def draw(self, ctx, t, d):
        ocean_surface(ctx, t, sunset=False)

        # Telemetry Card at top
        rrect(ctx, 140, 240, 800, 95, 12)
        rgba(ctx, hexc("#0C1520"), 0.90)
        ctx.fill()
        rrect(ctx, 140, 240, 800, 95, 12)
        rgba(ctx, FIRE_ORANGE, 0.90)
        ctx.set_line_width(2.5)
        ctx.stroke()
        text(ctx, "AK-630 CIWS ENGAGEMENT", 540, 280, 28, FIRE_ORANGE, font=MONO, bold=True)
        text(ctx, "RATE OF FIRE: 4,000 ROUNDS / MIN", 540, 315, 18, GOLD, font=MONO)

        # INS Vikrant bridge & CIWS turret close-up
        draw_ins_vikrant(ctx, 420, 1220, 1.25, t, ciws_firing=True)

        # Target incoming missile position
        m_t = (t * 1.5) % 2.5
        tgt_x = 880 - m_t * 260
        tgt_y = 520 + m_t * 180

        # High-rate tracer rounds stream from CIWS (approx 580, 1100) to target
        ciws_gun_x, ciws_gun_y = 575, 1100
        draw_ciws_tracers(ctx, ciws_gun_x, ciws_gun_y, tgt_x, tgt_y, t)

        # Incoming Cruise Missile
        ctx.save()
        ctx.translate(tgt_x, tgt_y)
        ctx.rotate(math.atan2(180, -260))
        # Rocket flame
        pat_m = cairo.RadialGradient(-20, 0, 2, -45, 0, 30)
        pat_m.add_color_stop_rgba(0.0, 1.0, 0.9, 0.3, 0.95)
        pat_m.add_color_stop_rgba(0.5, 1.0, 0.3, 0.0, 0.8)
        pat_m.add_color_stop_rgba(1.0, 0.0, 0.0, 0.0, 0.0)
        ctx.set_source(pat_m)
        ctx.arc(-25, 0, 22, 0, 2 * math.pi)
        ctx.fill()
        # Missile body
        rrect(ctx, -20, -7, 42, 14, 3)
        rgba(ctx, hexc("#546E7A"), 0.95)
        ctx.fill()
        ctx.restore()

        # Air Intercept Mid-Air Fireball Explosion
        if m_t > 1.3:
            ex_alpha = min(1.0, (m_t - 1.3) * 3.5)
            pat_ex = cairo.RadialGradient(tgt_x, tgt_y, 10, tgt_x, tgt_y, 175)
            pat_ex.add_color_stop_rgba(0.0, 1.0, 1.0, 0.9, 0.95 * ex_alpha)
            pat_ex.add_color_stop_rgba(0.25, 1.0, 0.6, 0.1, 0.85 * ex_alpha)
            pat_ex.add_color_stop_rgba(0.65, 0.8, 0.1, 0.0, 0.5 * ex_alpha)
            pat_ex.add_color_stop_rgba(1.0, 0.1, 0.02, 0.0, 0.0)
            ctx.set_source(pat_ex)
            ctx.arc(tgt_x, tgt_y, 185, 0, 2 * math.pi)
            ctx.fill()
            text(ctx, "MISSILE INTERCEPTED!", tgt_x, tgt_y + 110, 24, GOLD, font=MONO, bold=True)


class AntiSubmarineScene(Cued):
    """Scene 4: Anti-Submarine Warfare Sonar Screen tracking enemy submarine in Indian Ocean."""
    def beats(self, d):
        c = self.cue
        return {
            "mahasagar": c("MAHASAGAR", 0.5),
            "pandubbi": c("PANDUBBI", d * 0.45),
            "badh": c("AAGE", d * 0.75)
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["mahasagar"], "tick"), (b["pandubbi"], "beep"), (b["badh"], "zap")]

    def draw(self, ctx, t, d):
        ocean_surface(ctx, t, sunset=False)

        # Large center acoustic sonar scope
        draw_sonar_scope(ctx, 540, 720, 360, t, sub_locked=True)

        # INS Vikrant sailing in distance above water line
        draw_carrier_wake(ctx, 540, 1380, 0.75, t)
        draw_ins_vikrant(ctx, 540, 1340, 0.80, t, jet_on_deck=True)


class CtaPollScene(Cued):
    """Scene 5: 3-Second Snap CTA: INS Vikrant in blazing sunset with tricolor jets."""
    def beats(self, d):
        c = self.cue
        return {
            "nausena": c("NAUSENA", 0.5),
            "jaihind": c("HIND", d * 0.45),
            "subscribe": c("SUBSCRIBE", d * 0.75)
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["nausena"], "shimmer"), (b["jaihind"], "ghanti"), (b["subscribe"], "shimmer")]

    def draw(self, ctx, t, d):
        ocean_surface(ctx, t, sunset=True)

        # Glorious Sunset Cruise: INS Vikrant cutting through waves
        draw_carrier_wake(ctx, 540, 1260, 1.25, t)
        draw_ins_vikrant(ctx, 540, 1200, 1.30, t, jet_on_deck=True)

        # MiG-29K flying overhead in formation with tricolor smoke
        fly_y = 480 - (t * 80) % 600
        for idx, (fx, col) in enumerate([(-180, SAFFRON), (0, WHITE), (180, INDIA_GREEN)]):
            draw_mig29k(ctx, 540 + fx, fly_y + abs(fx) * 0.3, 0.55, t, afterburner=True, angle_deg=0.0)
            # Smoke trail
            line(ctx, [(540 + fx, fly_y + 60), (540 + fx, fly_y + 350)], col, 7.0, 0.75)


SCENE_CLASSES = {
    "carrier_race_hook": CarrierRaceHookScene,
    "warship_scale": WarshipScaleScene,
    "ciws_defense": CiwsDefenseScene,
    "anti_submarine": AntiSubmarineScene,
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
        "Samandar Mein Bharat Ka Tairta Kila: INS Vikrant! 🇮🇳⚓ #shorts",
        "China Ke Hosh Udane Wala Bharat Ka Aircraft Carrier! 🇮🇳 #shorts",
        "INS Vikrant: Indian Ocean Ka Asli Baap! ⚓🔥 #shorts",
        "Dushman Ki Missile Ko Hawa Mein Bhashm Karta INS Vikrant #shorts",
        "45,000 Tonne Ka Superweapon: INS Vikrant Explained #shorts",
    ],
    "title": "Samandar Mein Bharat Ka Tairta Kila: INS Vikrant! 🇮🇳⚓ #shorts",
    "thumb_text": "INS VIKRANT",
    "queries": ["ins vikrant", "indian navy aircraft carrier", "vikrant vs china"],
    "description": """Indian Ocean mein Bharat ke 45,000-tonne ke tairte kile INS Vikrant se dushman kyun kaanpta hai?
Do football maidan jitna bada flight deck, 14-degree ski-jump se Mach 2 par udne wale MiG-29K fighter jets aur har minute 4,000 rounds daagne wali AK-630 rotary gun!

Is Short mein:
• 45,000 Tonne Ka Desi Aircraft Carrier
• Ski-Jump se MiG-29K jet launch
• AK-630 CIWS missile intercept system
• Indian Ocean aur Malacca Strait mein Bharat ka danka

Kya aapko Bharatiya Nausena par garv hai? Comment mein likhein - JAI HIND! 🇮🇳
Subscribe to RealityShift for high-tech defence breakdowns.

#Shorts #INSVikrant #IndianNavy #Defence
""",
    "tags": [
        "ins vikrant", "indian navy", "aircraft carrier", "mig 29k",
        "vikrant vs china", "indian ocean", "defence shorts", "navy shorts",
        "reality shift", "viral shorts", "jai hind"
    ],
    "hashtags": ["#Shorts", "#INSVikrant", "#IndianNavy", "#Defence"],
}


def thumbnail(ctx):
    """High-CTR YouTube Shorts cover for INS Vikrant."""
    ocean_surface(ctx, 1.0, sunset=True)
    draw_carrier_wake(ctx, 540, 1180, 1.35, 1.0)
    draw_ins_vikrant(ctx, 540, 1120, 1.40, 1.0, jet_on_deck=True)
    # MiG-29K launching overhead
    draw_mig29k(ctx, 540, 520, 0.95, 1.0, afterburner=True, angle_deg=-15.0)

    # High-impact typography
    text(ctx, "INS VIKRANT", 540, 260, 125, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "SAMANDAR KA BAAP?", 540, 390, 80, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, CYAN, a=0.85)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.vikrant")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
