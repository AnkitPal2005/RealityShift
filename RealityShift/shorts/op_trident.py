"""Reality Shift Short: Operation Trident (4 Dec 1971) - Indian Navy's missile boats struck Karachi harbour.

Facts (see SOURCES): On 4 December 1971, Indian Navy Vidyut-class missile boats (INS Nipat, INS Nirghat, INS Veer)
armed with Styx missiles struck Karachi harbour at night, sinking PNS Khaibar and PNS Muhafiz and setting Karachi's
fuel storage tanks ablaze, returning with zero Indian casualties. Celebrated every year as Indian Navy Day.
"""

import importlib
import math
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cairo

from core import delivery, engine, lego  # noqa: F401
from core.engine import *  # noqa: F401,F403
from shorts.chabahar import Cued
from shorts.haji_pir import chip, stamp

TOPIC = "OPERATION TRIDENT 1971 KARACHI HARBOUR INDIAN NAVY"
OUTPUTS = {"edge": "op_trident_short.mp4"}
LEGO = {"header": "intel", "caption": "chip", "transition": "shutter", "palette": "glacier", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.45
TAIL_PAD = 0.35
TRIM = {"thresh": 0.006, "keep": 0.04, "keep_tail": 0.06}
MUSIC_BPM = 104
MUSIC_STYLE = "march"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 0
MAX_SECONDS = 35.0

PAL = lego.PALETTES["glacier"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
WHITE = (1.0, 1.0, 1.0)
GOLD = hexc("#FFD166")
RED = hexc("#E2483A")
CYAN = hexc("#5FD3FF")
NAVY_C = hexc("#8FA2B6")
FIRE = hexc("#FF6A1A")

SOURCES = [
    "Wikipedia - Operation Trident (1971): https://en.wikipedia.org/wiki/Operation_Trident_(1971)",
    "Indian Navy Official History - Navy Day 4 December: https://www.indiannavy.nic.in/",
]

SPEC = [
    {"key": "hook", "accent": GOLD, "text": "",
     "visual": "Night sea: Indian missile boat in foreground facing burning Karachi fuel tanks",
     "vo": [("hook", [("चार दिसंबर उन्नीस सौ इकहत्तर को", "4 DECEMBER 1971 KO"),
                      ("भारतीय नौसेना ने कराची में", "BHARATIYA NAUSENA NE KARACHI MEIN"),
                      ("आग लगा दी थी।", "AAG LAGA DI THI.")])]},
    {"key": "boats", "accent": CYAN, "text": "",
     "visual": "Radar map showing Okha -> Karachi route + 3 detailed Vidyut missile boats",
     "vo": [("tell", [("कोई बड़ा जहाज नहीं", "KOI BADA JAHAAZ NAHIN"),
                      ("सिर्फ तीन छोटी मिसाइल बोट", "SIRF TEEN CHHOTI MISSILE BOAT"),
                      ("कराची की तरफ बढ़ीं।", "KARACHI KI TARAF BADHEEN.")])]},
    {"key": "radar", "accent": RED, "text": "",
     "visual": "Close-up of missile boat firing bright Styx missile with flame & smoke",
     "vo": [("build", [("रात के अंधेरे में", "RAAT KE ANDHERE MEIN"),
                       ("पहली स्टिक्स मिसाइल दागी गई।", "PEHLI STYX MISSILE DAAGI GAYI.")])]},
    {"key": "khaibar", "accent": FIRE, "text": "",
     "visual": "Detailed destroyer PNS Khaibar hit mid-hull, breaking and burning on sea",
     "vo": [("punch", [("दुश्मन का सबसे बड़ा विध्वंसक", "DUSHMAN KA SABSE BADA DESTROYER"),
                       ("पी एन एस खैबर डूब गया।", "PNS KHAIBAR DOOB GAYA.")])]},
    {"key": "oil", "accent": SAFFRON, "text": "",
     "visual": "Karachi Keamari harbour: huge fuel tanks & dock cranes burning in orange flames",
     "vo": [("build", [("कराची के तेल टैंक", "KARACHI KE TEL TANK"),
                       ("कई दिनों तक जलते रहे।", "KAI DINO TAK JALTE RAHE.")])]},
    {"key": "zero", "accent": INDIA_GREEN, "text": "",
     "visual": "Dawn sea: Indian missile boat returning with tricolor stripe & ZERO LOSS stamp",
     "vo": [("tell", [("और भारतीय नौसेना का", "AUR BHARATIYA NAUSENA KA"),
                      ("एक भी जवान शहीद नहीं हुआ।", "EK BHI JAWAN SHAHEED NAHIN HUA.")])]},
    {"key": "day", "accent": GOLD, "text": "",
     "visual": "Heroic Navy missile boat & 4 DEC NAVY DAY badge",
     "vo": [("punch", [("इसी जीत की याद में", "ISI JEET KI YAAD MEIN"),
                      ("हर साल नौसेना दिवस मनाया जाता है।", "HAR SAAL NAVY DAY MANAYA JATA HAI.")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}
HOT = {
    "KARACHI": FIRE, "NAUSENA": CYAN, "MISSILE": GOLD, "STYX": FIRE,
    "KHAIBAR": RED, "TEL": SAFFRON, "SHAHEED": INDIA_GREEN, "NAVY": GOLD,
}


def smooth(ctx, pts, k=0.2):
    ctx.move_to(*pts[0])
    for x, y in pts[1:]:
        ctx.line_to(x, y)
    ctx.close_path()


def sea_sky(ctx, t, glow_fire=0.0, dawn=False):
    g = cairo.LinearGradient(0, 0, 0, 920)
    g.add_color_stop_rgb(0, *hexc("#0B1B36" if dawn else "#050B16"))
    g.add_color_stop_rgb(1, *hexc("#2C4E78" if dawn else "#12294A"))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, 920)
    ctx.fill()
    if glow_fire > 0:
        glow(ctx, 740, 820, 440, FIRE, 0.55 * glow_fire)
    g2 = cairo.LinearGradient(0, 910, 0, H)
    g2.add_color_stop_rgb(0, *hexc("#0E2D4C" if dawn else "#09213B"))
    g2.add_color_stop_rgb(1, *hexc("#030812"))
    ctx.set_source(g2)
    ctx.rectangle(0, 910, W, H - 910)
    ctx.fill()
    for k in range(9):
        wy = 950 + k * 75
        line(ctx, [(0, wy + 10 * math.sin(t * 3 + k)), (W, wy - 10 * math.sin(t * 3 + k))],
             CYAN, 3.0, 0.2)


def missile_boat(ctx, x, y, s, t, label=None):
    """Detailed Indian Vidyut-class missile boat with radar mast, Styx missile tubes, and tricolor stripe."""
    ctx.save()
    ctx.translate(x, y + 5 * math.sin(t * 4))
    ctx.scale(s, s)
    # Bow wake
    smooth(ctx, [(-175, 22), (-320, 34), (-320, 12)], k=0.2)
    rgba(ctx, WHITE, 0.35)
    ctx.fill()
    # Hull
    smooth(ctx, [(-170, 22), (165, 22), (225, -24), (-145, -24)], k=0.05)
    rgba(ctx, NAVY_C)
    ctx.fill()
    # Bridge & radar mast
    rrect(ctx, -70, -76, 110, 52, 8)
    rgba(ctx, hexc("#5B6C7E"))
    ctx.fill()
    rrect(ctx, -50, -64, 48, 18, 4)
    rgba(ctx, CYAN, 0.7)
    ctx.fill()
    line(ctx, [(-15, -76), (-15, -135)], hexc("#B0C0D0"), 6)
    line(ctx, [(-38, -118), (8, -118)], CYAN, 5)
    # Styx missile launcher tubes
    rrect(ctx, 48, -54, 72, 28, 6)
    rgba(ctx, SAFFRON)
    ctx.fill()
    rrect(ctx, 48, -42, 72, 10, 3)
    rgba(ctx, WHITE)
    ctx.fill()
    # Tricolor hull stripe
    rrect(ctx, -120, -14, 70, 6, 2)
    rgba(ctx, SAFFRON)
    ctx.fill()
    rrect(ctx, -120, -8, 70, 6, 2)
    rgba(ctx, INDIA_GREEN)
    ctx.fill()
    if label:
        text(ctx, label, 0, 54, 24, WHITE, bold=True)
    ctx.restore()


def destroyer_ship(ctx, x, y, s, hit=0.0):
    """Large enemy destroyer (PNS Khaibar) with twin turrets, funnel, and explosion."""
    ctx.save()
    ctx.translate(x, y + 55 * hit)
    ctx.rotate(0.28 * hit)
    ctx.scale(s, s)
    smooth(ctx, [(-240, 28), (240, 28), (290, -28), (-210, -28)], k=0.05)
    rgba(ctx, hexc("#3E4A58"))
    ctx.fill()
    rrect(ctx, -95, -96, 175, 68, 8)
    rgba(ctx, hexc("#2E3844"))
    ctx.fill()
    rrect(ctx, -35, -135, 36, 42, 4)
    rgba(ctx, hexc("#242B34"))
    ctx.fill()
    line(ctx, [(110, -34), (175, -52)], hexc("#6E7A88"), 10)
    if hit > 0:
        glow(ctx, 0, -50, 220 * hit, FIRE, 0.9)
        circle(ctx, -10, -70, 58 * hit, FIRE, 0.85)
    ctx.restore()


def oil_tanks(ctx, x, y, s, t, fire=1.0):
    """Karachi Keamari harbour fuel storage tanks + dock crane + towering flames."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    # Dock wall
    rrect(ctx, -30, 0, 420, 32, 4)
    rgba(ctx, hexc("#303844"))
    ctx.fill()
    for k in range(3):
        tx = k * 125
        rrect(ctx, tx, -110, 98, 110, 8)
        rgba(ctx, hexc("#647080"))
        ctx.fill()
        rrect(ctx, tx + 10, -82, 78, 12, 3)
        rgba(ctx, hexc("#C83E32"), 0.85)
        ctx.fill()
        if fire > 0:
            fl = 115 + 40 * abs(math.sin(t * 7 + k))
            glow(ctx, tx + 49, -125, 160, FIRE, 0.65 * fire)
            smooth(ctx, [(tx + 14, -110), (tx + 49, -110 - fl * fire), (tx + 84, -110)], k=0.3)
            rgba(ctx, FIRE, 0.92)
            ctx.fill()
            smooth(ctx, [(tx + 28, -110), (tx + 49, -110 - fl * 0.6 * fire), (tx + 70, -110)], k=0.3)
            rgba(ctx, GOLD, 0.95)
            ctx.fill()
    ctx.restore()


class Hook(Cued):
    def events(self, d):
        return [(0.1, "boom")]

    def draw(self, ctx, t, d):
        sea_sky(ctx, t, glow_fire=1.0)
        oil_tanks(ctx, 560, 910, 1.15, t, fire=1.0)
        missile_boat(ctx, 290, 1060, 1.35, t, label="INS NIPAT")
        chip(ctx, "4 DEC 1971  |  KARACHI", 540, 310, GOLD, clamp(t / 0.4))


class Boats(Cued):
    def events(self, d):
        return [(0.1, "whoosh")]

    def draw(self, ctx, t, d):
        sea_sky(ctx, t, glow_fire=0.1)
        # Tactical route line OKHA -> KARACHI
        rrect(ctx, 110, 410, 860, 180, 18)
        rgba(ctx, hexc("#0A1A30"), 0.75)
        ctx.fill()
        line(ctx, [(240, 500), (840, 500)], CYAN, 6, 0.8)
        circle(ctx, 240, 500, 16, INDIA_GREEN)
        circle(ctx, 840, 500, 16, RED)
        text(ctx, "OKHA (INDIA)", 240, 455, 28, WHITE)
        text(ctx, "KARACHI", 840, 455, 28, RED)
        for k, (bx, by, bs, nm) in enumerate((
            (250, 940, 0.95, "NIPAT"), (540, 1080, 1.15, "NIRGHAT"), (830, 960, 0.95, "VEER")
        )):
            missile_boat(ctx, bx + 35 * clamp(t / d), by, bs, t + k, label=nm)
        chip(ctx, "3 MISSILE BOATS", 540, 310, CYAN, clamp(t / 0.4))


class Radar(Cued):
    def beats(self, d):
        return {"fire": self.cue("STYX", d * 0.5)}

    def events(self, d):
        return [(self.beats(d)["fire"], "arrow")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        sea_sky(ctx, t, glow_fire=0.25)
        missile_boat(ctx, 280, 1040, 1.45, t, label="STYX LAUNCH")
        u = clamp((t - b["fire"] + 0.35) / 0.95)
        if u > 0:
            mx = lerp(370, 960, u)
            my = lerp(960, 470, u)
            line(ctx, [(370, 960), (mx, my)], FIRE, 10, 0.75)
            glow(ctx, mx, my, 60, GOLD, 0.95)
            circle(ctx, mx, my, 14, WHITE)
        chip(ctx, "STYX MISSILE", 540, 310, RED, clamp(t / 0.4))


class Khaibar(Cued):
    def beats(self, d):
        return {"hit": self.cue("DOOB", d * 0.55)}

    def events(self, d):
        return [(self.beats(d)["hit"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        hit = clamp((t - b["hit"] + 0.35) / 0.65)
        sea_sky(ctx, t, glow_fire=hit)
        destroyer_ship(ctx, 540, 940, 1.35, hit=hit)
        chip(ctx, "PNS KHAIBAR SUNK", 540, 310, RED, max(0.3, hit))


class Oil(Cued):
    def events(self, d):
        return [(0.1, "boom")]

    def draw(self, ctx, t, d):
        sea_sky(ctx, t, glow_fire=1.0)
        oil_tanks(ctx, 280, 930, 1.45, t, fire=1.25)
        chip(ctx, "KARACHI OIL TANKS", 540, 310, SAFFRON, clamp(t / 0.4))


class Zero(Cued):
    def events(self, d):
        return [(0.2, "dingdong")]

    def draw(self, ctx, t, d):
        sea_sky(ctx, t, glow_fire=0.1, dawn=True)
        missile_boat(ctx, 540, 1040, 1.55, t, label="SAFE RETURN")
        stamp(ctx, "ZERO LOSS", 540, 480, clamp(t / 0.4), c=INDIA_GREEN, size=96)


class Day(Cued):
    def events(self, d):
        return [(0.1, "shimmer")]

    def draw(self, ctx, t, d):
        sea_sky(ctx, t, glow_fire=0.2, dawn=True)
        missile_boat(ctx, 540, 1020, 1.5, t)
        chip(ctx, "INDIAN NAVY DAY - 4 DEC", 540, 340, GOLD, clamp(t / 0.4))


SCENE_CLASSES = {"hook": Hook, "boats": Boats, "radar": Radar, "khaibar": Khaibar,
                 "oil": Oil, "zero": Zero, "day": Day}

UPLOAD = {
    "titles": [
        "3 Chhoti Boats Ne Karachi Jalaya... 1971 Operation Trident #shorts",
        "4 Dec 1971: Jab Indian Navy Ne Karachi Mein Aag Laga Di #shorts",
        "Zero Casualties! Operation Trident Ki Asli Kahani #shorts",
    ],
    "thumb_text": "KARACHI ON FIRE",
    "queries": ["operation trident", "indian navy 1971", "karachi attack 1971"],
    "description": """Operation Trident (4 December 1971) - jab Indian Navy ki chhoti missile boats ne Karachi harbour par
hamla kiya aur zero Indian casualties ke saath wapas lauti.

Debate: Operation Trident ki sabse badi jeet kya thi - chhoti missile boats ki chaal ya Navy ka silent attack?

Sources:
- Wikipedia: Operation Trident (1971)
- Indian Navy Official History
""",
    "tags": ["operation trident", "1971 war", "indian navy", "navy day", "karachi attack", "ins nipat",
             "pns khaibar", "reality shift", "defence shorts", "indian military history"],
    "hashtags": ["#Shorts", "#IndianNavy", "#OperationTrident"],
    "pinned_comment": "Operation Trident ki sabse badi taqat kya thi - chhoti MISSILE BOATS ki chaal ya Navy ka "
                      "SURPRISE night attack? Apni raay comments mein likhein! 🇮🇳⚓",
}


def thumbnail(ctx):
    sea_sky(ctx, 0.5, glow_fire=1.0)
    oil_tanks(ctx, 540, 920, 1.25, 0.5, fire=1.2)
    missile_boat(ctx, 300, 1060, 1.4, 0.5)
    text(ctx, "4 DEC 1971", 540, 210, 115, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "KARACHI ON FIRE", 540, 340, 112, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "ZERO LOSS!", 540, 1340, 118, INDIA_GREEN, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, PAL["ui"], a=0.85)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.op_trident")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    total = sum(s["dur"] for s in engine.SCENES)
    write_alignment(final)
    upload_kit.build(story, final, total)
    if total > MAX_SECONDS:
        raise SystemExit(f"[length] {total:.1f}s is over the {MAX_SECONDS:.0f}s lock")


if __name__ == "__main__":
    main()
