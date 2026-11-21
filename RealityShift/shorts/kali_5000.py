"""Reality Shift Short — "KALI 5000: India's Invisible Beam Weapon" (~35-38s).

Usage:
  python make.py kali_5000 --kiki-split
  python make.py kali_5000 --engine files
  python make.py kali_5000 --preview

Technical Overview:
KALI (Kilo Ampere Linear Injector) 5000:
Developed by Bhabha Atomic Research Centre (BARC) and DRDO.
A high-power pulse accelerator emitting gigawatt relativistic electron beams (REB)
and High-Power Microwaves (HPM) designed to soft-kill enemy incoming missiles, UAVs,
and satellites by frying on-board electronics and circuitry in nanoseconds.
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

TOPIC = "KALI 5000 DIRECTED ENERGY WEAPON"
OUTPUTS = {"edge": "kali_5000_short.mp4"}
LEGO = {"header": "radar", "caption": "speech", "transition": "scan", "palette": "glacier", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.55
TAIL_PAD = 0.20
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 86
MUSIC_STYLE = "ambient"
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
DARK_STEEL = hexc("#151D24")
RADAR_GREEN = hexc("#00FF66")
CYAN_BEAM = hexc("#00F0FF")
FIRE_ORANGE = hexc("#FF5500")
GOLD = hexc("#FFD700")
MONO = "Consolas"

SOURCES = [
    "Bhabha Atomic Research Centre (BARC) - Accelerators & Pulse Power Division (KALI Project)",
    "Defence Research and Development Organisation (DRDO) - Directed Energy Weapon & High-Power Microwave Systems",
    "Department of Atomic Energy (DAE) - Relativistic Electron Beam & EMP Defense Research",
]

SPEC = [
    # Scene 1: Incoming Missile vs Defense Calm
    {"key": "incoming_missile", "accent": RED, "text": "INCOMING MISSILE THREAT",
     "visual": "Supersonic missile streaking across crimson alert sky; Indian border outpost monitors calmly without launching",
     "vo": [("tell", [("दुश्मन की तेज़ मिसाइल भारत की ओर बढ़ रही है,", "DUSHMAN KI TEZ MISSILE BHARAT KI OR BADH RAHI HAI,"),
                      ("पर हमारे सैनिक", "PAR HAMARE SAINIK"),
                      ("कोई मिसाइल नहीं छोड़ते!", "KOI MISSILE NAHI CHHODTE!")])]},

    # Scene 2: The Sky Spark / Energy Wave
    {"key": "sky_wave", "accent": CYAN_BEAM, "text": "INVISIBLE ENERGY WAVE",
     "visual": "A massive invisible electromagnetic wave ripples across dark blue sky, cyan lightning arcs flash silently",
     "vo": [("tell", [("अचानक आसमान में एक अनदेखी,", "ACHANAK AASMAAN MEIN EK ANDEKHI,"),
                      ("ज़बरदस्त बिजली की तरंग चमकती है!", "ZABARDAST BIJLI KI TARANG CHAMAKTI HAI!")])]},

    # Scene 3: Electronics Fry Inside Missile
    {"key": "circuit_fry", "accent": FIRE_ORANGE, "text": "CIRCUIT CHIPS MELTING",
     "visual": "Close-up cutaway of missile interior: microchips spark furiously, copper circuits melt, black smoke bursts out",
     "vo": [("tell", [("न कोई बारूद, न कोई धमाका—", "NA KOI BAROOD, NA KOI DHAMAKA—"),
                      ("लेकिन एक सेकंड में", "LEKIN EK SECOND MEIN"),
                      ("मिसाइल के सारे कलपुर्जे", "MISSILE KE SAARE KALPURJE"),
                      ("पिघल कर राख हो जाते हैं!", "PIGHAL KAR RAAKH HO JAATE HAIN!")])]},

    # Scene 4: Reveal KALI 5000
    {"key": "reveal_kali", "accent": SAFFRON, "text": "PROJECT KALI-5000",
     "visual": "Massive military bunker housing KALI 5000 accelerator dome, BARC & DRDO crest, high voltage capacitors glowing",
     "vo": [("tell", [("ये है भारत का सबसे गुप्त हथियार—", "YEH HAI BHARAT KA SABSE GUPT HATHIYAR—"),
                      ("काली पाँच हज़ार!", "KALI PAANCH HAZAAR!")])]},

    # Scene 5: BARC & DRDO Scientists Beam Emitter
    {"key": "scientists_beam", "accent": CYAN_BEAM, "text": "RELATIVISTIC BEAM EMISSION",
     "visual": "Indian scientists in high-tech lab firing the relativistic electron emitter; gigawatt energy rings radiate upwards",
     "vo": [("tell", [("हमारे वैज्ञानिकों का बनाया ये हथियार", "HAMARE VAIGYANIKON KA BANAYA YEH HATHIYAR"),
                      ("इतनी तगड़ी किरणें फेंकता है,", "ITNI TAGDI KIRNEIN PHENKTA HAI,")])]},

    # Scene 6: Spying Drones & Jets Neutralized
    {"key": "air_neutralized", "accent": RED, "text": "AIR THREATS DESTROYED",
     "visual": "Enemy surveillance stealth drones and supersonic jets losing navigation display, smoking engines, plunging from sky",
     "vo": [("tell", [("कि आसमान में उड़ते दुश्मन के जासूसी जहाज", "KI AASMAAN MEIN UDTE DUSHMAN KE JASOOSI JAHAJ"),
                      ("और मिसाइलें हवा में ही", "AUR MISSILE-EIN HAWA MEIN HI"),
                      ("भुनकर बेजान हो जाती हैं!", "BHUNKAR BEJAAN HO JAATI HAIN!")])]},

    # Scene 7: Pride & Poll CTA
    {"key": "cta", "accent": HI, "text": "NATIONAL PRIDE & POLL",
     "visual": "Indian flag glowing proud in the background, interactive poll card: 'KYA KALI-5000 BORDER PAR HONA CHAHIYE?', clean arrow pointing down",
     "vo": [("ask", [("भारत के इस गुप्त अस्त्र पर आपको गर्व है?", "BHARAT KE IS GUPT ASTRA PAR AAPKO GARV HAI?"),
                      ("कमेंट में जय हिंद लिखें", "COMMENT MEIN JAI HIND LIKHEN"),
                      ("और सब्सक्राइब करें रियलिटी शिफ्ट!", "AUR SUBSCRIBE KAREIN REALITY SHIFT!")])]},
]

DELIVERY = delivery.build(SPEC)
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "DUSHMAN": RED, "MISSILE": RED, "BHARAT": SAFFRON, "SAINIK": SAFFRON, "AASMAAN": CYAN_BEAM,
    "ANDEKHI": CYAN_BEAM, "BIJLI": CYAN_BEAM, "TARANG": CYAN_BEAM, "CHAMAKTI": GOLD, "BAROOD": RED,
    "DHAMAKA": RED, "SECOND": GOLD, "KALPURJE": RED, "PIGHAL": FIRE_ORANGE, "RAAKH": FIRE_ORANGE,
    "GUPT": GOLD, "HATHIYAR": GOLD, "KALI": SAFFRON, "HAZAAR": SAFFRON, "VAIGYANIKON": SAFFRON,
    "KIRNEIN": CYAN_BEAM, "JASOOSI": RED, "JAHAJ": RED, "BHUNKAR": FIRE_ORANGE, "BEJAAN": RED,
    "ASTRA": GOLD, "GARV": SAFFRON, "COMMENT": HI, "JAI": SAFFRON, "HIND": SAFFRON, "SUBSCRIBE": HI
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".—")] = HOT[_k]


# ============================================================ SCENE CLASSES

# Ultra-vivid, cinematic visual classes for KALI 5000 Short

class IncomingMissileScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"dushman": c("DUSHMAN", 1.0), "sainik": c("SAINIK", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["dushman"], "pick"), (b["sainik"], "pop")]

    def draw(self, ctx, t, d):
        # 1. Dramatic sunset alert sky with red/amber atmospheric glow
        grad = cairo.LinearGradient(0, 0, 0, engine.H)
        grad.add_color_stop_rgb(0, 0.12, 0.02, 0.05)
        grad.add_color_stop_rgb(0.4, 0.28, 0.08, 0.06)
        grad.add_color_stop_rgb(0.7, 0.18, 0.04, 0.03)
        grad.add_color_stop_rgb(1.0, 0.05, 0.02, 0.03)
        ctx.set_source(grad)
        ctx.paint()

        # Blood red glowing radar grid lines in background
        ctx.save()
        ctx.set_source_rgba(1.0, 0.2, 0.2, 0.15)
        ctx.set_line_width(2)
        for gy in range(200, 1400, 120):
            ctx.move_to(0, gy); ctx.line_to(engine.W, gy); ctx.stroke()
        for gx in range(100, 1000, 150):
            ctx.move_to(gx, 200); ctx.line_to(gx, 1400); ctx.stroke()
        ctx.restore()

        # Mountain silhouette with crimson rim light
        ctx.save()
        ctx.set_source_rgb(0.06, 0.03, 0.04)
        ctx.move_to(0, engine.H * 0.74)
        ctx.line_to(180, engine.H * 0.64)
        ctx.line_to(400, engine.H * 0.70)
        ctx.line_to(680, engine.H * 0.61)
        ctx.line_to(920, engine.H * 0.68)
        ctx.line_to(1080, engine.H * 0.63)
        ctx.line_to(1080, engine.H); ctx.line_to(0, engine.H); ctx.close_path()
        ctx.fill()
        # Rim light on mountains
        ctx.set_source_rgba(1.0, 0.4, 0.1, 0.5)
        ctx.set_line_width(4)
        ctx.move_to(0, engine.H * 0.74)
        ctx.line_to(180, engine.H * 0.64); ctx.line_to(400, engine.H * 0.70)
        ctx.line_to(680, engine.H * 0.61); ctx.line_to(920, engine.H * 0.68); ctx.line_to(1080, engine.H * 0.63)
        ctx.stroke()
        ctx.restore()

        # Indian Border Defense Outpost with green holographic dome
        ctx.save()
        ctx.translate(240, engine.H * 0.68)
        # Radar base
        ctx.set_source_rgb(0.15, 0.20, 0.26)
        ctx.rectangle(-70, -30, 140, 50); ctx.fill()
        # Glowing green hologram scanning cone
        ctx.set_source_rgba(0.0, 1.0, 0.5, 0.25)
        dish_ang = math.sin(t * 4.0) * 0.6
        ctx.move_to(0, -30)
        ctx.arc(0, -30, 180, -math.pi * 0.75 + dish_ang, -math.pi * 0.25 + dish_ang)
        ctx.close_path(); ctx.fill()
        ctx.restore()

        # Supersonic enemy missile diving at high speed
        prog = (t / max(d, 0.1)) % 1.0
        mx = 1150 - prog * 1350
        my = 480 + math.sin(t * 10.0) * 35
        
        ctx.save()
        ctx.translate(mx, my)
        ctx.rotate(math.pi * 0.95)
        
        # Roaring fire afterburner flame
        for i in range(12):
            ctx.set_source_rgba(1.0, 0.3 + i*0.06, 0.0, 0.7 - i*0.05)
            ctx.arc(-90 - i*28, 0, 24 - i*1.8, 0, math.pi * 2)
            ctx.fill()
        # Shock diamonds in flame
        for si in range(4):
            ctx.set_source_rgba(1.0, 1.0, 1.0, 0.8)
            ctx.arc(-110 - si*50, 0, 8, 0, math.pi * 2); ctx.fill()

        # Missile body with sharp military red and hazard stripes
        ctx.set_source_rgb(0.9, 0.15, 0.15)
        ctx.rectangle(-80, -18, 160, 36); ctx.fill()
        # Nose cone
        ctx.set_source_rgb(0.15, 0.15, 0.18)
        ctx.move_to(80, -18); ctx.line_to(140, 0); ctx.line_to(80, 18); ctx.close_path(); ctx.fill()
        # Yellow hazard band
        ctx.set_source_rgb(1.0, 0.85, 0.0)
        ctx.rectangle(20, -18, 25, 36); ctx.fill()
        # Wings
        ctx.set_source_rgb(0.3, 0.35, 0.42)
        ctx.move_to(-70, -18); ctx.line_to(-100, -50); ctx.line_to(-40, -18); ctx.fill()
        ctx.move_to(-70, 18); ctx.line_to(-100, 50); ctx.line_to(-40, 18); ctx.fill()
        ctx.restore()


class SkyWaveScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"andekhi": c("ANDEKHI", 1.0), "bijli": c("BIJLI", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["andekhi"], "pick"), (b["bijli"], "thud")]

    def draw(self, ctx, t, d):
        # 2. Electric neon indigo night sky
        grad = cairo.LinearGradient(0, 0, 0, engine.H)
        grad.add_color_stop_rgb(0, 0.02, 0.05, 0.18)
        grad.add_color_stop_rgb(0.5, 0.04, 0.14, 0.32)
        grad.add_color_stop_rgb(1, 0.01, 0.03, 0.10)
        ctx.set_source(grad)
        ctx.paint()

        # Expanding High-Power Microwave (HPM) energy shockwaves
        cx, cy = 540, engine.H * 0.85
        for r_idx in range(8):
            r = ((t * 500 + r_idx * 140) % 1100)
            alpha = max(0.0, 1.0 - (r / 1100.0))
            # Outer cyan glow
            ctx.set_source_rgba(0.0, 0.95, 1.0, alpha * 0.6)
            ctx.set_line_width(10 - (r / 140))
            ctx.arc(cx, cy, r, 0, math.pi * 2); ctx.stroke()
            # Inner white energy crest
            ctx.set_source_rgba(1.0, 1.0, 1.0, alpha * 0.85)
            ctx.set_line_width(3.5)
            ctx.arc(cx, cy, r, 0, math.pi * 2); ctx.stroke()

        # Multi-branch violent lightning arcs crackling across screen
        np.random.seed(int(t * 16))
        for _ in range(5):
            lx = 540 + np.random.uniform(-400, 400)
            ly = 320 + np.random.uniform(-200, 200)
            ctx.save()
            ctx.set_source_rgba(0.6, 1.0, 1.0, 0.9)
            ctx.set_line_width(np.random.uniform(3, 7))
            ctx.move_to(lx, ly)
            for step in range(6):
                lx += np.random.uniform(-60, 60)
                ly += np.random.uniform(-40, 60)
                ctx.line_to(lx, ly)
            ctx.stroke()
            ctx.restore()


class CircuitFryScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"barood": c("BAROOD", 1.0), "pighal": c("PIGHAL", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["barood"], "pop"), (b["pighal"], "thud")]

    def draw(self, ctx, t, d):
        # 3. Macro Emerald Green Printed Circuit Board
        ctx.set_source_rgb(0.02, 0.12, 0.08)
        ctx.paint()

        # Intricate gold copper circuit bus traces
        ctx.save()
        ctx.set_source_rgba(0.9, 0.75, 0.2, 0.45)
        ctx.set_line_width(5)
        for offset in range(80, 1020, 70):
            ctx.move_to(offset, 350)
            ctx.line_to(offset + 50, 520)
            ctx.line_to(offset + 50, 1000)
            ctx.stroke()
        ctx.restore()

        # Central Military Microprocessor Overheating & Exploding
        cx, cy = 540, 720
        ctx.save()
        ctx.translate(cx, cy)
        
        # Ceramic Chip Body
        ctx.set_source_rgb(0.14, 0.14, 0.18)
        ctx.rectangle(-250, -200, 500, 400); ctx.fill()
        
        # Gold chip pins glowing with electric surge
        for px in range(-230, 240, 30):
            ctx.set_source_rgb(0.0, 0.95, 1.0)
            ctx.rectangle(px, -220, 14, 25); ctx.fill()
            ctx.rectangle(px, 195, 14, 25); ctx.fill()

        # Molten Red-Hot Cracks bursting open
        melt_pulse = 0.6 + 0.4 * math.sin(t * 18.0)
        ctx.set_source_rgba(1.0, 0.2, 0.0, melt_pulse)
        ctx.set_line_width(16)
        ctx.move_to(-180, -120); ctx.line_to(-40, 10); ctx.line_to(90, -60); ctx.line_to(190, 110)
        ctx.stroke()
        
        # Inner white-hot liquid core
        ctx.set_source_rgba(1.0, 0.95, 0.4, 0.95)
        ctx.set_line_width(6)
        ctx.move_to(-180, -120); ctx.line_to(-40, 10); ctx.line_to(90, -60); ctx.line_to(190, 110)
        ctx.stroke()

        # Intense particle burst: flying sparks and fire embers
        np.random.seed(int(t * 24))
        for _ in range(35):
            sx = np.random.uniform(-220, 220)
            sy = np.random.uniform(-180, 180)
            ctx.set_source_rgba(1.0, np.random.uniform(0.5, 0.95), 0.1, 0.95)
            ctx.arc(sx, sy, np.random.uniform(5, 14), 0, math.pi * 2)
            ctx.fill()
        ctx.restore()


class RevealKaliScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"gupt": c("GUPT", 1.0), "kali": c("KALI", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["gupt"], "pop"), (b["kali"], "thud")]

    def draw(self, ctx, t, d):
        # 4. High-tech defense laboratory vault
        grad = cairo.RadialGradient(540, 700, 50, 540, 700, 750)
        grad.add_color_stop_rgb(0, 0.08, 0.18, 0.28)
        grad.add_color_stop_rgb(0.6, 0.03, 0.08, 0.14)
        grad.add_color_stop_rgb(1.0, 0.01, 0.02, 0.05)
        ctx.set_source(grad)
        ctx.paint()

        # Gigantic KALI 5000 Linear Injector Accelerator
        cx, cy = 540, 750
        ctx.save()
        ctx.translate(cx, cy)
        
        # Heavy generator chassis with gunmetal and titanium sheen
        ctx.set_source_rgb(0.20, 0.26, 0.34)
        ctx.rectangle(-320, -220, 640, 440); ctx.fill()
        ctx.set_line_width(6); ctx.set_source_rgb(0.4, 0.55, 0.7); ctx.stroke()

        # High-voltage blue capacitor banks on sides
        for col_x in [-280, -200, 200, 280]:
            ctx.set_source_rgb(0.12, 0.45, 0.75)
            ctx.rectangle(col_x - 30, -190, 60, 380); ctx.fill()
            ctx.set_source_rgb(0.0, 0.95, 1.0)
            ctx.rectangle(col_x - 10, -170, 20, 340); ctx.fill()

        # Pulsing Relativistic Core Emitter in Center
        core_scale = 1.0 + 0.08 * math.sin(t * 12.0)
        # Giant outer cyan aura
        ctx.set_source_rgba(0.0, 0.85, 1.0, 0.5)
        ctx.arc(0, 0, 130 * core_scale, 0, math.pi * 2); ctx.fill()
        # White hot center
        ctx.set_source_rgba(1.0, 1.0, 1.0, 0.95)
        ctx.arc(0, 0, 60 * core_scale, 0, math.pi * 2); ctx.fill()

        # Tactical Insignia Plate
        ctx.set_source_rgb(0.08, 0.10, 0.14)
        ctx.rectangle(-220, -280, 440, 55); ctx.fill()
        ctx.set_source_rgb(1.0, 0.85, 0.0)
        ctx.select_font_face("Impact", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(36)
        ctx.move_to(-180, -240)
        ctx.show_text("PROJECT KALI-5000 // BARC")
        ctx.restore()


class ScientistsBeamScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"vaigyanik": c("VAIGYANIKON", 1.0), "kirne": c("KIRNEIN", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["vaigyanik"], "pick"), (b["kirne"], "thud")]

    def draw(self, ctx, t, d):
        # 5. Command telemetry room with glowing terminal screens
        ctx.set_source_rgb(0.03, 0.05, 0.08)
        ctx.paint()

        # Multicolored tactical monitors in background
        ctx.save()
        for x_pos, col in [(160, (0.0, 0.8, 1.0)), (540, (1.0, 0.3, 0.0)), (920, (0.0, 1.0, 0.5))]:
            ctx.set_source_rgb(0.10, 0.14, 0.20)
            ctx.rectangle(x_pos - 150, 460, 300, 240); ctx.fill()
            ctx.set_source_rgba(col[0], col[1], col[2], 0.25)
            ctx.rectangle(x_pos - 140, 470, 280, 220); ctx.fill()
            # Digital waveforms
            ctx.set_source_rgb(col[0], col[1], col[2])
            ctx.set_line_width(3)
            ctx.move_to(x_pos - 130, 580)
            for wx in range(x_pos - 130, x_pos + 130, 15):
                ctx.line_to(wx, 580 + math.sin(wx*0.12 + t*8.0)*40)
            ctx.stroke()
        ctx.restore()

        # Giant Relativistic Electron Energy Beam shooting upwards into sky
        ctx.save()
        beam_w = 140 + 30 * math.sin(t * 14.0)
        b_grad = cairo.LinearGradient(540 - beam_w, 0, 540 + beam_w, 0)
        b_grad.add_color_stop_rgba(0, 0.0, 0.9, 1.0, 0.0)
        b_grad.add_color_stop_rgba(0.3, 0.0, 0.95, 1.0, 0.5)
        b_grad.add_color_stop_rgba(0.5, 1.0, 1.0, 1.0, 0.95)
        b_grad.add_color_stop_rgba(0.7, 0.0, 0.95, 1.0, 0.5)
        b_grad.add_color_stop_rgba(1.0, 0.0, 0.9, 1.0, 0.0)
        ctx.rectangle(540 - beam_w, 0, beam_w * 2, 450)
        ctx.set_source(b_grad); ctx.fill()
        ctx.restore()

        # Scientists in white lab coats operating holographic pedestals
        for sx in [350, 730]:
            ctx.save()
            ctx.set_source_rgb(0.9, 0.94, 1.0)
            ctx.arc(sx, 800, 32, 0, math.pi * 2); ctx.fill()
            ctx.move_to(sx - 40, 835); ctx.line_to(sx + 40, 835)
            ctx.line_to(sx + 55, 1020); ctx.line_to(sx - 55, 1020); ctx.close_path(); ctx.fill()
            # Cyan holographic tablet in hands
            ctx.set_source_rgba(0.0, 0.95, 1.0, 0.8)
            ctx.rectangle(sx - 25, 870, 50, 35); ctx.fill()
            ctx.restore()


class AirNeutralizedScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"jasoosi": c("JASOOSI", 1.0), "bhunkar": c("BHUNKAR", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["jasoosi"], "pick"), (b["bhunkar"], "pop")]

    def draw(self, ctx, t, d):
        # 6. Dramatic combat storm sky with lightning
        grad = cairo.LinearGradient(0, 0, 0, engine.H)
        grad.add_color_stop_rgb(0, 0.10, 0.02, 0.03)
        grad.add_color_stop_rgb(0.5, 0.18, 0.05, 0.08)
        grad.add_color_stop_rgb(1.0, 0.04, 0.01, 0.02)
        ctx.set_source(grad)
        ctx.paint()

        # Falling enemy stealth drone spinning in flames
        drone_prog = (t / max(d, 0.1))
        dy = 320 + drone_prog * 580
        dx = 540 + math.sin(t * 4.0) * 160
        
        ctx.save()
        ctx.translate(dx, dy)
        ctx.rotate(t * 3.8) # tumbling spin
        
        # Heavy black smoke and bright fire explosion plume
        for i in range(16):
            # Fire core
            ctx.set_source_rgba(1.0, 0.4 + i*0.03, 0.0, 0.7 - i*0.04)
            ctx.arc(-i*18, -i*22, 24 + i*3, 0, math.pi * 2); ctx.fill()
            # Dark smoke
            ctx.set_source_rgba(0.1, 0.1, 0.12, 0.5 - i*0.03)
            ctx.arc(-i*24, -i*30, 32 + i*4, 0, math.pi * 2); ctx.fill()

        # Broken drone fuselage
        ctx.set_source_rgb(0.2, 0.22, 0.28)
        ctx.rectangle(-80, -18, 160, 36); ctx.fill()
        ctx.rectangle(-18, -80, 36, 160); ctx.fill()
        
        # Crackling electric short-circuit arcs over dead drone
        np.random.seed(int(t * 15))
        for _ in range(6):
            ctx.set_source_rgba(0.0, 0.95, 1.0, 0.9)
            ctx.set_line_width(3.5)
            ctx.move_to(np.random.uniform(-60, 60), np.random.uniform(-60, 60))
            ctx.line_to(np.random.uniform(-40, 40), np.random.uniform(-40, 40))
            ctx.stroke()
        ctx.restore()


class CtaScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"garv": c("GARV", 1.0), "sub": c("SUBSCRIBE", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["garv"], "pop"), (b["sub"], "pick")]

    def draw(self, ctx, t, d):
        # 7. Radiant, victorious twilight gradient
        grad = cairo.LinearGradient(0, 0, 0, engine.H)
        grad.add_color_stop_rgb(0, 0.02, 0.08, 0.18)
        grad.add_color_stop_rgb(0.5, 0.05, 0.14, 0.22)
        grad.add_color_stop_rgb(1.0, 0.02, 0.04, 0.08)
        ctx.set_source(grad)
        ctx.paint()

        # Rotating Golden Ashok Chakra in background
        ctx.save()
        ctx.translate(540, 640)
        ctx.rotate(t * 0.2)
        ctx.set_source_rgba(1.0, 0.85, 0.0, 0.25)
        ctx.set_line_width(10)
        ctx.arc(0, 0, 260, 0, math.pi * 2); ctx.stroke()
        for sp in range(24):
            ang = sp * (math.pi * 2 / 24)
            ctx.move_to(0, 0); ctx.line_to(math.cos(ang) * 260, math.sin(ang) * 260); ctx.stroke()
        ctx.restore()

        # Proud Indian Tricolor Flag
        ctx.save()
        flag(ctx, 420, 240, 240, 160, "india", 0.0)
        ctx.restore()

        # Interactive High-Contrast Poll Card
        ctx.save()
        ctx.translate(540, 820)
        ctx.set_source_rgb(0.10, 0.15, 0.22)
        ctx.rectangle(-360, -70, 720, 140); ctx.fill()
        ctx.set_line_width(5); ctx.set_source_rgb(0.0, 0.85, 1.0); ctx.stroke()
        
        ctx.set_source_rgb(1.0, 1.0, 1.0)
        ctx.select_font_face("Impact", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(42)
        ctx.move_to(-310, 15)
        ctx.show_text("KALI 5000 BORDER PAR HONA CHAHIYE?")
        ctx.restore()

        # Animated Bouncing Pointer Arrow to Comments
        arrow_bob = math.sin(t * 8.0) * 25
        ctx.save()
        ctx.translate(540, 1020 + arrow_bob)
        ctx.set_source_rgb(1.0, 0.85, 0.0)
        ctx.move_to(-40, -45); ctx.line_to(40, -45); ctx.line_to(40, 15)
        ctx.line_to(75, 15); ctx.line_to(0, 85); ctx.line_to(-75, 15); ctx.line_to(-40, 15)
        ctx.close_path(); ctx.fill()
        ctx.restore()


SCENE_CLASSES = {
    "incoming_missile": IncomingMissileScene,
    "sky_wave": SkyWaveScene,
    "circuit_fry": CircuitFryScene,
    "reveal_kali": RevealKaliScene,
    "scientists_beam": ScientistsBeamScene,
    "air_neutralized": AirNeutralizedScene,
    "cta": CtaScene,
}


# ============================================================ UPLOAD KIT & THUMBNAIL

UPLOAD = {
    "titles": [
        "Bharat Ka Adrishya Hathiyar: KALI 5000!",
        "KALI 5000: Bina Goli Chalaye Dushman Tabah!",
        "DRDO & BARC Ka KALI 5000: Desi Energy Beam",
        "Ek Second Mein Missile Khak! KALI 5000 Ka Sach",
        "KALI 5000: Dushman Ke Drone Aur Radar Ka Kaal",
        "India's Secret Energy Weapon: KALI 5000 Explained",
    ],
    "title": "Bharat Ka Adrishya Hathiyar: KALI 5000!",
    "thumb_text": "KALI 5000",
    "queries": ["kali 5000", "barc kali 5000", "drdo secret energy weapon"],
    "description": """BARC aur DRDO ka banaya KALI 5000 (Kilo Ampere Linear Injector) Bharat ka ek aisa shaktishali hathiyar hai jo bina kisi barood ke, sirf prachand bijli ki tarango se dushman ki missile aur drone ke circuit pighla deta hai.

#RealityShift #KALI5000 #DRDO #BARC #IndianDefense #ScienceShorts #IndianArmy #Shorts""",
    "tags": [
        "KALI 5000", "DRDO KALI 5000", "BARC energy weapon", "directed energy weapon India",
        "Indian defense shorts", "Reality Shift", "Indian Army weapons", "secret weapons of India"
    ],
    "hashtags": ["#RealityShift", "#KALI5000", "#IndianDefense"]
}


def thumbnail(ctx):
    
        # 1. Dark tactical deep-space navy vignette background
        bg = cairo.RadialGradient(W / 2, H * 0.45, 100, W / 2, H * 0.45, 950)
        bg.add_color_stop_rgb(0, 0.05, 0.12, 0.22)
        bg.add_color_stop_rgb(0.5, 0.02, 0.05, 0.10)
        bg.add_color_stop_rgb(1.0, 0.01, 0.01, 0.03)
        ctx.rectangle(0, 0, W, H)
        ctx.set_source(bg)
        ctx.fill()
    
        # 2. Glowing Electric Arc Grid & Particle Sparks
        ctx.save()
        np.random.seed(42)
        for _ in range(45):
            px = np.random.uniform(50, W - 50)
            py = np.random.uniform(100, H - 200)
            pr = np.random.uniform(2, 6)
            ctx.set_source_rgba(0.0, 0.95, 1.0, np.random.uniform(0.4, 0.9))
            ctx.arc(px, py, pr, 0, math.pi * 2)
            ctx.fill()
        ctx.restore()
    
        # 3. Massive Relativistic Electron Beam & Lightning Discharge (Center)
        ctx.save()
        beam_grad = cairo.LinearGradient(W/2 - 120, 0, W/2 + 120, 0)
        beam_grad.add_color_stop_rgba(0, 0.0, 0.8, 1.0, 0.0)
        beam_grad.add_color_stop_rgba(0.3, 0.0, 0.95, 1.0, 0.4)
        beam_grad.add_color_stop_rgba(0.5, 1.0, 1.0, 1.0, 0.95)
        beam_grad.add_color_stop_rgba(0.7, 0.0, 0.95, 1.0, 0.4)
        beam_grad.add_color_stop_rgba(1.0, 0.0, 0.8, 1.0, 0.0)
        ctx.rectangle(W/2 - 140, 250, 280, 1100)
        ctx.set_source(beam_grad)
        ctx.fill()
        ctx.restore()
    
        # Jagged violent lightning bolts striking down
        ctx.save()
        ctx.set_line_width(8)
        ctx.set_source_rgba(0.7, 1.0, 1.0, 0.95)
        for offset_x in [-90, 80]:
            ctx.move_to(W/2 + offset_x, 400)
            ctx.line_to(W/2 + offset_x + 60, 560)
            ctx.line_to(W/2 + offset_x - 30, 720)
            ctx.line_to(W/2 + offset_x + 80, 900)
            ctx.line_to(W/2 + offset_x, 1100)
            ctx.stroke()
        ctx.restore()
    
        # 4. Cinematic Threat: Incoming Supersonic Missile Getting Fried by the Beam!
        ctx.save()
        ctx.translate(W/2, 820)
        ctx.rotate(-math.pi * 0.28)
        
        # Missile body (Military red/steel)
        ctx.set_source_rgb(0.85, 0.15, 0.15)
        ctx.rectangle(-220, -35, 440, 70)
        ctx.fill()
        # Missile nose
        ctx.move_to(220, -35)
        ctx.line_to(340, 0)
        ctx.line_to(220, 35)
        ctx.close_path()
        ctx.fill()
        # Missile fins
        ctx.set_source_rgb(0.2, 0.25, 0.3)
        ctx.move_to(-210, -35); ctx.line_to(-270, -95); ctx.line_to(-160, -35); ctx.fill()
        ctx.move_to(-210, 35); ctx.line_to(-270, 95); ctx.line_to(-160, 35); ctx.fill()
    
        # Missile Internal Circuit Cutaway Bursting in Flames/Sparks
        ctx.set_source_rgb(1.0, 0.3, 0.0)
        ctx.arc(30, 0, 75, 0, math.pi * 2)
        ctx.fill()
        ctx.set_source_rgb(1.0, 0.9, 0.2)
        ctx.arc(30, 0, 45, 0, math.pi * 2)
        ctx.fill()
    
        # Sparks bursting out of the fractured missile
        np.random.seed(101)
        for _ in range(25):
            sx = 30 + np.random.uniform(-120, 120)
            sy = np.random.uniform(-80, 80)
            ctx.set_source_rgba(1.0, 0.9, 0.3, 0.9)
            ctx.arc(sx, sy, np.random.uniform(5, 12), 0, math.pi * 2)
            ctx.fill()
    
        ctx.restore()
    
        # 5. KALI 5000 Generator Base (Military High-Tech Bunker Aperture)
        ctx.save()
        ctx.translate(W/2, 1380)
        # Generator housing
        ctx.set_source_rgb(0.12, 0.16, 0.22)
        ctx.rectangle(-380, -80, 760, 240)
        ctx.fill()
        ctx.set_line_width(6)
        ctx.set_source_rgb(0.0, 0.85, 1.0)
        ctx.rectangle(-380, -80, 760, 240)
        ctx.stroke()
        # Glowing Aperture Emitter Rings
        for r in [180, 130, 80, 40]:
            ctx.set_source_rgba(0.0, 0.9, 1.0, 0.6)
            ctx.arc(0, 40, r, 0, math.pi * 2)
            ctx.set_line_width(8)
            ctx.stroke()
        ctx.set_source_rgba(1.0, 1.0, 1.0, 0.95)
        ctx.arc(0, 40, 25, 0, math.pi * 2)
        ctx.fill()
        ctx.restore()
    
        # 6. High-Contrast Gradient Backdrop for Typography (Top & Bottom)
        # Top Shadow
        top_g = cairo.LinearGradient(0, 0, 0, 650)
        top_g.add_color_stop_rgba(0, 0.0, 0.0, 0.0, 0.92)
        top_g.add_color_stop_rgba(1, 0.0, 0.0, 0.0, 0.0)
        ctx.rectangle(0, 0, W, 650)
        ctx.set_source(top_g)
        ctx.fill()
    
        # Bottom Shadow
        bot_g = cairo.LinearGradient(0, 1350, 0, H)
        bot_g.add_color_stop_rgba(0, 0.0, 0.0, 0.0, 0.0)
        bot_g.add_color_stop_rgba(1, 0.0, 0.0, 0.0, 0.95)
        ctx.rectangle(0, 1350, W, H - 1350)
        ctx.set_source(bot_g)
        ctx.fill()
    
        # 7. Punchy, Viral YouTube Typography (High Click-Through Design)
        # Badge: BARC // DRDO SECRET WEAPON
        ctx.save()
        ctx.set_source_rgb(0.9, 0.1, 0.1) # Danger Red Pill
        ctx.rectangle(W/2 - 280, 130, 560, 68)
        ctx.fill()
        ctx.set_source_rgb(1.0, 1.0, 1.0)
        ctx.select_font_face("Impact", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(44)
        ctx.move_to(W/2 - 245, 180)
        ctx.show_text("BARC & DRDO SECRET")
        ctx.restore()
    
        # BIG HEADLINE 1: "KALI 5000" in Glowing Gold / Cyan
        ctx.save()
        ctx.select_font_face("Impact", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(165)
        # Black Stroke Outline for maximum contrast
        ctx.set_line_width(22)
        ctx.set_source_rgb(0, 0, 0)
        ctx.move_to(W/2 - 380, 340)
        ctx.text_path("KALI 5000")
        ctx.stroke()
        # Yellow / Gold Fill
        ctx.set_source_rgb(1.0, 0.85, 0.0)
        ctx.move_to(W/2 - 380, 340)
        ctx.show_text("KALI 5000")
        ctx.restore()
    
        # BIG SUB-HEADLINE: "ENERGY BEAM!" in Blinding White with Cyan Glow
        ctx.save()
        ctx.select_font_face("Impact", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(105)
        ctx.set_line_width(18)
        ctx.set_source_rgb(0, 0, 0)
        ctx.move_to(W/2 - 320, 465)
        ctx.text_path("ENERGY BEAM!")
        ctx.stroke()
        ctx.set_source_rgb(0.0, 0.95, 1.0)
        ctx.move_to(W/2 - 320, 465)
        ctx.show_text("ENERGY BEAM!")
        ctx.restore()
    
        # BOTTOM PUNCHLINE: "NO MISSILE NEEDED"
        ctx.save()
        ctx.set_source_rgb(1.0, 0.2, 0.2)
        ctx.rectangle(W/2 - 340, 1680, 680, 85)
        ctx.fill()
        ctx.set_source_rgb(1.0, 1.0, 1.0)
        ctx.select_font_face("Impact", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(52)
        ctx.move_to(W/2 - 270, 1742)
        ctx.show_text("1 SEC MEIN MISSILE KHAK!")
        ctx.restore()
    
        # Subtle Branding Watermark
        ctx.save()
        ctx.set_source_rgba(1.0, 1.0, 1.0, 0.6)
        ctx.select_font_face("Consolas", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(36)
        ctx.move_to(W/2 - 130, 1830)
        ctx.show_text("• REALITY SHIFT •")
        ctx.restore()

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
    story = importlib.import_module('shorts.kali_5000')
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index('--engine') + 1] if '--engine' in sys.argv else 'files'
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s['dur'] for s in engine.SCENES))


if __name__ == '__main__':
    main()
