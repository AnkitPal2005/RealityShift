"""Reality Shift Short — 5.9M tonnes of lithium in J&K vs China's battery monopoly (~33s, pure Devanagari edge-tts).

Usage:
  python generate_lithium_short.py

Same pipeline and Golden Safe Zone layout as generate_rupee_short.py (whose one-narrator delivery and chain it
reuses, along with Chabahar's compositor, map and plates and Maldives' comment bubble and cursor): watermark
top-centre, on-screen text badge locked to Y 1150-1250, bottom 400px clean, ending on the comment + subscribe CTA.
Output: output/shorts/lithium_reasi_short.mp4 (+ a .json with the scene/word alignment).
"""

import importlib
import math

import cairo
import numpy as np

import engine
import generate_chabahar_short as cs
from engine import *  # noqa: F401,F403
from generate_chabahar_short import (CITIES, RED, bell, bust, draw_map, flash, partial, pin, plate, poly, proj,
                                     red_cross, view_at)
from generate_maldives_short import CN_RED, CN_YELLOW, cn_flag, comment_bubble, cursor_click
from generate_rupee_short import GAP, VOICE_TONES, chain
from stories.reality_shift import GOLD, INDIA_GREEN, SAFFRON, embers, flag, stamp, subscribe_badge

TOPIC = "INDIA VS CHINA"
OUTPUTS = {"edge": "lithium_reasi_short.mp4"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.18
TAIL_PAD = 0.08                # scene length = audio duration + 0.08s
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 112
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"

ICE = hexc("#BFEFFF")
LI_BLUE = hexc("#4CC3FF")
EV_GREEN = hexc("#2BFF88")
ROCK = hexc("#2A2E36")

SPEC = [
    {"key": "lithium", "window": "0:00-0:06", "icon": "bolt", "accent": LI_BLUE,
     "vo": [("ask", "क्या आपको पता है...?"),
            ("build", "जम्मू-कश्मीर में मिले"),
            ("punch", "5.9 मिलियन टन लिथियम ने"),
            ("tell", "चाइना के 500 बिलियन डॉलर के मोनोपॉली को..."),
            ("punch", "हिला कर रख दिया?")],
     "text": "5.9M TON LITHIUM FOUND!",
     "visual": "Fast zoom into a glowing white-blue crystal rock labeled LITHIUM (Li), shocked China graphic behind"},
    {"key": "monopoly", "window": "0:06-0:13", "icon": "battery", "accent": CN_RED,
     "vo": [("low", "दुनिया की 80% ईवी बैटरीज़ पर"),
            ("low", "सिर्फ चाइना का कंट्रोल था,"),
            ("sly", "और वो जब चाहे..."),
            ("build", "किसी भी देश की ऑटोमोबाइल इंडस्ट्री को"),
            ("punch", "ब्लैकमेल कर सकता था।")],
     "text": "80% BATTERY CONTROL",
     "visual": "China battery hub chained to car industries of USA, Europe, Japan and India, CHINA MONOPOLY warning"},
    {"key": "reasi", "window": "0:13-0:24", "icon": "flag", "accent": SAFFRON,
     "vo": [("punch", "लेकिन...", 0.22),
            ("build", "भारत के रियासी में मिले इस..."),
            ("punch", "व्हाइट गोल्ड के बाद,", 0.1),
            ("tell", "भारत दुनिया का सातवां सबसे बड़ा"),
            ("tell", "लिथियम रिज़र्व वाला देश बन गया।"),
            ("sly", "यानी अब टेस्ला और टाटा को"),
            ("punch", "चाइना के आगे हाथ फैलाने की ज़रूरत नहीं।")],
     "text": "INDIA'S WHITE GOLD",
     "visual": "Map zooms into Reasi, Jammu & Kashmir; white gold pin, #7 reserves, EV cars rolling out with India flag"},
    {"key": "future", "window": "0:24-0:33", "icon": "bell", "accent": hexc("#FF0000"),
     "vo": [("low", "चाइना का सबसे बड़ा बिज़नेस..."),
            ("punch", "अब खतरे में है।", 0.2),
            ("ask", "क्या भारत 2030 तक दुनिया का सबसे बड़ा ईवी हब बन पाएगा?", 0.28),
            ("cta", "कमेंट्स में बताओ,", 0.04),
            ("cta", "और रियलिटी शिफ्ट को सब्सक्राइब करो!")],
     "text": "SUBSCRIBE @RealityShift",
     "visual": "India EV graph shooting up past 2030, CHINA IN DANGER stamp, comment icon, subscribe click"},
]

# one narrator throughout (see generate_rupee_short.VOICE_TONES): same pitch every line, level gaps, dry voice;
# this script is ~20% wordier than the Rupee one, so every line runs 12 points faster with tighter gaps
TONES = {k: (f"+{int(r[1:-1]) + 12}%", p, v) for k, (r, p, v) in VOICE_TONES.items()}
DELIVERY = {s["key"]: [(TONES[tone], text_, GAP * 0.6) for tone, text_, *_ in s["vo"]] for s in SPEC}
BREATHS = False
ROOM = 0
NARRATION = {s["key"]: " ".join(line[1] for line in s["vo"]) for s in SPEC}
SCRIPT = [(s["key"], [(w, w) for w in NARRATION[s["key"]].split()]) for s in SPEC]


# ============================================================ lithium + icons

def crystal(ctx, x, y, w, h, rot, a=1.0):
    """One hexagonal prism of lithium ore, base centred on (x, y), leaning by rot."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    pts = [(-w / 2, 0), (-w / 2, -h), (0, -h - w * 0.6), (w / 2, -h), (w / 2, 0)]
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    g = cairo.LinearGradient(-w / 2, 0, w / 2, 0)
    g.add_color_stop_rgba(0, 0.55, 0.85, 1.0, 0.95 * a)
    g.add_color_stop_rgba(0.45, 0.97, 1.0, 1.0, a)
    g.add_color_stop_rgba(1, 0.35, 0.62, 0.92, 0.95 * a)
    ctx.set_source(g)
    ctx.fill_preserve()
    rgba(ctx, (1, 1, 1), 0.9 * a)
    ctx.set_line_width(3)
    ctx.stroke()
    line(ctx, [(0, 0), (0, -h - w * 0.6)], (1, 1, 1), 2, 0.6 * a)   # centre facet
    line(ctx, [(-w / 2, -h), (0, -h + w * 0.25), (w / 2, -h)], (1, 1, 1), 2, 0.5 * a)
    ctx.restore()


CLUSTER = [(-120, 46, 150, -0.42), (-60, 60, 230, -0.2), (0, 78, 320, 0.0), (64, 62, 250, 0.22),
           (124, 48, 170, 0.45), (-20, 40, 140, -0.05), (40, 38, 120, 0.12)]


def ore(ctx, x, y, s, t, a=1.0):
    """Dark rock with a glowing cluster of white-blue crystals growing out of it, base centred on (x, y)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    glow(ctx, 0, -120, 380, LI_BLUE, (0.45 + 0.1 * math.sin(t * 5)) * a)
    for cx, w, h, rot in CLUSTER:
        crystal(ctx, cx, 10, w, h, rot, a)
    ctx.move_to(-230, 0)
    for px, py in ((-170, -40), (-80, -22), (0, -34), (90, -20), (180, -44), (240, 10), (200, 90), (60, 120),
                   (-110, 112), (-240, 70)):
        ctx.line_to(px, py)
    ctx.close_path()
    g = cairo.LinearGradient(0, -40, 0, 120)
    g.add_color_stop_rgba(0, *shade(ROCK, 1.6), a)
    g.add_color_stop_rgba(1, *shade(ROCK, 0.6), a)
    ctx.set_source(g)
    ctx.fill()
    for k in range(5):  # glittering flecks in the rock
        fx, fy = -180 + 90 * k + 20 * rnd(k, 3), 20 + 60 * rnd(k, 4)
        circle(ctx, fx, fy, 5 + 3 * math.sin(t * 7 + k), ICE, 0.8 * a)
    for k in range(4):  # sparkles on the tips
        cx, w, h, rot = CLUSTER[(k * 2) % len(CLUSTER)]
        tw = 0.5 + 0.5 * math.sin(t * 6 + k * 1.9)
        sx, sy = cx + (h + w * 0.6) * math.sin(rot), 10 - (h + w * 0.6) * math.cos(rot)
        for ang in (0, math.pi / 2):
            line(ctx, [(sx - 26 * tw * math.cos(ang), sy - 26 * tw * math.sin(ang)),
                       (sx + 26 * tw * math.cos(ang), sy + 26 * tw * math.sin(ang))], (1, 1, 1), 4, a)
    ctx.restore()


def li_tile(ctx, x, y, s, a=1.0):
    """Periodic-table tile for lithium, centred on (x, y)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    glow(ctx, 0, 0, 200, LI_BLUE, 0.5 * a)
    rrect(ctx, -110, -130, 220, 260, 18)
    rgba(ctx, (0.03, 0.06, 0.1), 0.92 * a)
    ctx.fill_preserve()
    rgba(ctx, LI_BLUE, a)
    ctx.set_line_width(6)
    ctx.stroke()
    text(ctx, "3", -80, -98, 38, ICE, font=CAPTION_FONT, bold=False, a=a, anchor="l")
    text(ctx, "6.94", 80, -98, 30, ICE, font=CAPTION_FONT, bold=False, a=0.8 * a, anchor="r")
    text(ctx, "Li", 0, -4, 130, (1, 1, 1), a=a)
    text(ctx, "LITHIUM", 0, 92, 40, LI_BLUE, font=CAPTION_FONT, bold=False, a=a)
    ctx.restore()


def battery(ctx, x, y, w, h, level, c, a=1.0):
    """Upright battery cell centred on (x, y) filled to level 0..1 in colour c."""
    rrect(ctx, x - w * 0.18, y - h / 2 - h * 0.08, w * 0.36, h * 0.1, 6)
    rgba(ctx, (0.85, 0.87, 0.9), a)
    ctx.fill()
    rrect(ctx, x - w / 2, y - h / 2, w, h, w * 0.14)
    rgba(ctx, (0.04, 0.04, 0.06), 0.9 * a)
    ctx.fill_preserve()
    rgba(ctx, (0.85, 0.87, 0.9), a)
    ctx.set_line_width(max(3.0, w * 0.06))
    ctx.stroke()
    pad = w * 0.12
    fh = (h - 2 * pad) * clamp(level)
    rrect(ctx, x - w / 2 + pad, y + h / 2 - pad - fh, w - 2 * pad, fh, w * 0.06)
    rgba(ctx, c, a)
    ctx.fill()


def battery_icon(ctx, x, y, t):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(math.pi / 2)
    battery(ctx, 0, 0, 40, 76, 0.8, CN_RED)
    ctx.restore()
    cs.bolt(ctx, x, y, 0.5, CN_YELLOW)


cs.ICONS.update({"battery": battery_icon})


def ev_car(ctx, x, y, s, t, body, spin=0.0, lights=1.0):
    """Side-on electric hatchback facing right, wheels on the ground at y, centred on x."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.save()
    ctx.scale(1, 0.18)
    ctx.arc(0, 0, 230, 0, math.tau)
    ctx.restore()
    rgba(ctx, (0, 0, 0), 0.45)
    ctx.fill()
    ctx.move_to(-230, -40)                       # body
    ctx.curve_to(-232, -90, -210, -104, -170, -108)
    ctx.line_to(-110, -112)
    ctx.curve_to(-70, -170, -30, -182, 40, -180)
    ctx.curve_to(100, -178, 130, -150, 160, -116)
    ctx.curve_to(215, -110, 236, -90, 236, -40)
    ctx.line_to(236, -26)
    ctx.line_to(-230, -26)
    ctx.close_path()
    g = cairo.LinearGradient(0, -180, 0, -26)
    g.add_color_stop_rgb(0, *shade(body, 1.35))
    g.add_color_stop_rgb(1, *shade(body, 0.7))
    ctx.set_source(g)
    ctx.fill()
    ctx.move_to(-96, -114)                       # glasshouse
    ctx.curve_to(-62, -160, -30, -168, 30, -166)
    ctx.line_to(30, -114)
    ctx.close_path()
    ctx.move_to(46, -166)
    ctx.curve_to(96, -162, 118, -146, 142, -114)
    ctx.line_to(46, -114)
    ctx.close_path()
    rgba(ctx, hexc("#16202E"))
    ctx.fill()
    line(ctx, [(-100, -60), (190, -60)], (1, 1, 1), 2, 0.3)
    cs.bolt(ctx, 30, -76, 0.55, EV_GREEN)
    glow(ctx, 228, -78, 60, (1, 0.95, 0.75), 0.7 * lights)
    rrect(ctx, 214, -86, 22, 14, 5)
    rgba(ctx, (1, 0.97, 0.85), 0.4 + 0.6 * lights)
    ctx.fill()
    rrect(ctx, -232, -84, 14, 16, 4)
    rgba(ctx, RED)
    ctx.fill()
    for wx in (-138, 146):                       # wheels
        circle(ctx, wx, -26, 50, (0.06, 0.06, 0.07))
        circle(ctx, wx, -26, 28, (0.72, 0.75, 0.8))
        for k in range(5):
            ang = spin + k / 5 * math.tau
            line(ctx, [(wx, -26), (wx + 26 * math.cos(ang), -26 + 26 * math.sin(ang))], (0.3, 0.32, 0.36), 6)
        circle(ctx, wx, -26, 8, (0.2, 0.2, 0.22))
    ctx.restore()


def warning(ctx, x, y, s, c, a=1.0):
    """Warning triangle with an exclamation mark centred on (x, y)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(0, -70)
    ctx.line_to(78, 62)
    ctx.line_to(-78, 62)
    ctx.close_path()
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    rgba(ctx, c, a)
    ctx.set_line_width(14)
    ctx.stroke_preserve()
    ctx.fill()
    rrect(ctx, -8, -30, 16, 54, 6)
    rgba(ctx, (0.05, 0.02, 0.02), a)
    ctx.fill()
    circle(ctx, 0, 42, 9, (0.05, 0.02, 0.02), a)
    ctx.restore()


def crack(ctx, x, y, u, seed=0):
    """Glass-crack burst out of (x, y), drawn on over u = 0..1."""
    for k in range(7):
        ang = k / 7 * math.tau + rnd(k, seed)
        pts = [(x, y)]
        r = 0
        for j in range(4):
            r += 50 + 40 * rnd(k * 4 + j, seed + 1)
            jit = 0.25 * (rnd(k * 4 + j, seed + 2) - 0.5)
            pts.append((x + r * math.cos(ang + jit), y + r * math.sin(ang + jit)))
        drawn, _ = partial(pts, u)
        line(ctx, drawn, (1, 1, 1), 4, 0.85)


# ============================================================ scenes

class Lithium(cs.Cued):
    """Fast zoom into a glowing lithium crystal rock, Li tile, 5.9M tonnes count-up, China shaken on 'हिला'."""

    def beats(self, d):
        c = self.cue
        return {"jk": c("जम्मू-कश्मीर", d * 0.15), "num": c("5.9", d * 0.3), "li": c("लिथियम", d * 0.4),
                "china": c("चाइना", d * 0.55), "shake": c("हिला", d * 0.82)}

    def events(self, d):
        b = self.beats(d)
        ticks = [(b["num"] + k * 0.06, "tick" if k % 2 else "tock") for k in range(8)]
        return [(0.02, "boom"), (0.05, "whoosh"), (b["jk"], "beep"), (b["num"], "thud"), (b["li"], "zap"),
                (b["china"], "alarm"), (b["shake"], "boom"), (b["shake"] + 0.03, "thud")] + ticks

    def draw(self, ctx, t, d):
        b = self.beats(d)
        backdrop(ctx, hexc("#0A1A2A"), hexc("#02060B"), LI_BLUE, 540, 700, t, motes=30)
        u = t - b["shake"]
        shaking = 0 < u < 0.6
        if shaking:
            ctx.translate(18 * (1 - u / 0.6) * math.sin(u * 80), 10 * (1 - u / 0.6) * math.cos(u * 70))
        z = lerp(0.45, 1.25, ease_out_cubic(t / 0.7))  # fast zoom in
        ore(ctx, 540, 860, z, t)
        u = t - b["jk"]
        if u > 0 and t < b["china"]:
            plate(ctx, "JAMMU & KASHMIR", 540, 1050, SAFFRON, u, size=50)
        u = t - b["li"]
        if u > 0:
            li_tile(ctx, 190, 330, ease_out_back(u / 0.35), 1.0)
            flash(ctx, u, 0.2, 0.4)
        u = t - b["num"]
        if u > 0 and t < b["china"]:
            n = 5.9 * ease_out_cubic(u / 0.7)
            stamp(ctx, 640, 300, u, -0.04, 620, 200, LI_BLUE,
                  [(f"{n:.1f}M TONNES", -18, 100, (1, 1, 1)), ("LITHIUM FOUND", 62, 44, LI_BLUE)])
        u = t - b["china"]
        if u > 0:  # China's monopoly, shaken and cracked on 'हिला'
            pop = ease_out_back(u / 0.35)
            ctx.save()
            ctx.translate(780, 330)
            ctx.scale(pop, pop)
            glow(ctx, 0, 0, 300, CN_RED, 0.45)
            rrect(ctx, -230, -200, 460, 360, 22)
            rgba(ctx, (0.08, 0.02, 0.02), 0.9)
            ctx.fill()
            ctx.save()
            rrect(ctx, -230, -200, 460, 360, 22)
            ctx.clip()
            cn_flag(ctx, -230, -200, 460, 300, 0.45)
            bust(ctx, 0, -60, 0.42, t, hexc("#1C2233"), CN_RED, None, 0,
                 mood="stressed" if t >= b["shake"] else "smug")
            ctx.restore()
            rrect(ctx, -230, -200, 460, 360, 22)
            rgba(ctx, CN_RED)
            ctx.set_line_width(6)
            ctx.stroke()
            ctx.restore()
            plate(ctx, "$500B MONOPOLY", 780, 560, CN_RED, u - 0.15, size=48, sub="CHINA")
        u = t - b["shake"]
        if u > 0:
            crack(ctx, 780, 330, ease_out_cubic(u / 0.3), seed=2)
            flash(ctx, u, 0.25, 0.6)
            embers(ctx, t, 18, LI_BLUE, speed=170, seed=5)


class Monopoly(cs.Cued):
    """China's battery hub chained to the world's car industries; 80% meter, CHINA MONOPOLY, then BLACKMAIL."""

    CARS = (("USA", "us", 250, 420), ("EUROPE", "de", 830, 420), ("JAPAN", "jp", 250, 1010), ("INDIA", "in", 830, 1010))

    def beats(self, d):
        c = self.cue
        return {"pct": c("80%", d * 0.08), "ctrl": c("कंट्रोल", d * 0.3), "any": c("किसी", d * 0.6),
                "black": c("ब्लैकमेल", d * 0.82)}

    def events(self, d):
        b = self.beats(d)
        ticks = [(b["pct"] + k * 0.07, "tick" if k % 2 else "tock") for k in range(10)]
        return [(0.02, "boom"), (b["ctrl"], "alarm"), (b["any"], "pick"), (b["any"] + 0.25, "pick"),
                (b["black"], "boom"), (b["black"] + 0.02, "thud")] + ticks

    def draw(self, ctx, t, d):
        b = self.beats(d)
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, *hexc("#1E0606"))
        g.add_color_stop_rgb(1, *hexc("#060101"))
        ctx.set_source(g)
        ctx.paint()
        for k in range(12):  # faint grid
            line(ctx, [(0, 120 + k * 90), (W, 120 + k * 90)], CN_RED, 1, 0.1)
        black = clamp((t - b["black"]) / 0.3)
        hx, hy = 540, 720
        for k, (_, _, cx, cy) in enumerate(self.CARS):  # chains out to every car industry
            u = (t - b["ctrl"] - 0.12 * k) / 0.6
            chain(ctx, hx, hy, cx, cy - 60, u, c=RED if black else hexc("#AEB4BD"))
        for k, (name, kind, cx, cy) in enumerate(self.CARS):
            u = t - 0.15 - 0.12 * k
            if u <= 0:
                continue
            pop = ease_out_back(u / 0.3)
            ctx.save()
            ctx.translate(cx, cy)
            ctx.scale(pop, pop)
            rrect(ctx, -200, -170, 400, 230, 24)
            rgba(ctx, (0.03, 0.03, 0.05), 0.88)
            ctx.fill_preserve()
            rgba(ctx, RED if black else (0.5, 0.52, 0.58))
            ctx.set_line_width(4)
            ctx.stroke()
            flag(ctx, -180, -154, 66, 44, kind, t)
            text(ctx, name, 0, -130, 40, (1, 1, 1), font=CAPTION_FONT, bold=False)
            ev_car(ctx, 0, 40, 0.62, t, hexc(("#3C7DFF", "#D8D8DE", "#E04848", "#FF9933")[k]), lights=1 - black)
            ctx.restore()
            if black:
                red_cross(ctx, cx, cy - 40, t - b["black"] - 0.1 * k, size=55)
        # the hub: China's battery with the 80% ring
        glow(ctx, hx, hy, 340, CN_RED, 0.4 + 0.1 * math.sin(t * 6))
        circle(ctx, hx, hy, 170, (0.05, 0.02, 0.02), 0.95)
        pct = 0.8 * ease_out_cubic((t - b["pct"]) / 0.9) if t > b["pct"] else 0.0
        ctx.arc(hx, hy, 150, 0, math.tau)
        rgba(ctx, (1, 1, 1), 0.12)
        ctx.set_line_width(22)
        ctx.stroke()
        if pct:
            ctx.arc(hx, hy, 150, -math.pi / 2, -math.pi / 2 + pct * math.tau)
            rgba(ctx, CN_RED)
            ctx.set_line_width(22)
            ctx.stroke()
        battery(ctx, hx, hy - 20, 90, 150, pct / 0.8, CN_RED)
        cs.bolt(ctx, hx, hy - 20, 1.0, CN_YELLOW)
        text(ctx, f"{round(pct * 100)}%", hx, hy + 100, 54, (1, 1, 1), font=CAPTION_FONT, bold=False)
        cn_flag(ctx, hx - 45, hy - 230, 90, 60)
        u = t - b["ctrl"]
        if u > 0:
            ctx.save()
            ctx.translate(540, 190)
            ctx.scale(ease_out_back(u / 0.3), ease_out_back(u / 0.3))
            on = int(t * 4) % 2 == 0
            warning(ctx, -330, 0, 0.6, RED if on else CN_YELLOW)
            warning(ctx, 330, 0, 0.6, RED if on else CN_YELLOW)
            ctx.restore()
            plate(ctx, "CHINA MONOPOLY", 540, 190, RED, u, size=62)
        u = t - b["black"]
        if u > 0:
            if u < 0.3:
                ctx.translate(14 * (1 - u / 0.3) * math.sin(u * 90), 0)
            stamp(ctx, 540, 720, u, -0.08, 720, 180, RED, [("BLACKMAIL", 0, 140, RED)])


JK = [(75.3, 32.3), (74.6, 32.68), (74.0, 33.0), (73.5, 33.6), (73.7, 34.2), (73.9, 34.5), (74.3, 34.8),
      (75.0, 34.65), (75.6, 34.4), (75.9, 33.9), (75.95, 33.3), (75.9, 32.8), (75.6, 32.4)]
REASI = (74.83, 33.08)


class Reasi(cs.Cued):
    """Map dives into Reasi, J&K: white-gold pin, #7 in reserves, then EVs roll out and China's flag is crossed out."""

    def beats(self, d):
        c = self.cue
        return {"reasi": c("रियासी", d * 0.12), "gold": c("व्हाइट", d * 0.24), "rank": c("सातवां", d * 0.4),
                "cars": c("यानी", d * 0.62), "tesla": c("टेस्ला", d * 0.66), "tata": c("टाटा", d * 0.72),
                "china": c("चाइना", d * 0.78), "no": c("नहीं", d * 0.92)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (0.1, "whoosh"), (b["reasi"], "dingdong"), (b["gold"], "kaching"),
                (b["gold"] + 0.3, "zap"), (b["rank"], "boom"), (b["cars"], "whoosh"), (b["tesla"], "beep"),
                (b["tata"], "beep"), (b["china"], "alarm"), (b["no"], "boom"), (b["no"] + 0.02, "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        v = view_at([(0.0, (80.0, 30.0, 26)), (b["reasi"] - 0.1, (76.5, 31.5, 60)),
                     (b["reasi"] + 0.9, (74.85, 33.35, 250))], t)
        draw_map(ctx, v, t)
        hl = clamp((t - b["reasi"] + 0.3) / 0.5)
        poly(ctx, v, JK)  # Jammu & Kashmir lights up saffron
        rgba(ctx, SAFFRON, 0.1 + 0.18 * hl)
        ctx.fill_preserve()
        rgba(ctx, SAFFRON, 0.4 + 0.5 * hl)
        ctx.set_line_width(4)
        ctx.stroke()
        jx, jy = proj(v, 75.3, 34.2)
        if 0 < jy < 1100:
            text(ctx, "JAMMU & KASHMIR", jx, jy, 34, SAFFRON, font=CAPTION_FONT, bold=False, a=0.4 + 0.5 * hl)
        cx, cy = proj(v, *CITIES["KASHGAR"])
        text(ctx, "CHINA", min(cx, 980), max(cy, 200), 34, CN_RED, font=CAPTION_FONT, bold=False, a=0.6)
        rx, ry = proj(v, *REASI)
        u = t - b["reasi"]
        pin(ctx, rx, ry, LI_BLUE, u, t)
        if u > 0 and t < b["cars"]:
            plate(ctx, "REASI", rx, ry + 150, SAFFRON, u, size=54, sub="J&K")
        u = t - b["gold"]
        if u > 0:  # crystals rise out of the pin
            ore(ctx, rx, ry + 30, 0.55 * ease_out_back(u / 0.4), t)
            if t < b["rank"]:
                stamp(ctx, 540, 260, u, -0.05, 700, 170, LI_BLUE, [("WHITE GOLD", 0, 130, (1, 1, 1))])
        u = t - b["rank"]
        if u > 0 and t < b["china"]:
            stamp(ctx, 540, 260, u, -0.04, 760, 200, GOLD,
                  [("#7 IN THE WORLD", -22, 100, GOLD), ("LITHIUM RESERVES", 60, 46, (1, 1, 1))])
        u = t - b["cars"]
        if u > 0:  # road in front of the map: EVs roll out under the tricolour
            dim = clamp(u / 0.4)
            ctx.rectangle(0, 0, W, H)
            rgba(ctx, (0.01, 0.02, 0.04), 0.45 * dim)
            ctx.fill()
            ctx.rectangle(0, 990, W, 150)
            rgba(ctx, hexc("#16181D"), dim)
            ctx.fill()
            ctx.set_dash([60, 50], -t * 600)
            line(ctx, [(0, 1065), (W, 1065)], (1, 1, 1), 6, 0.7 * dim)
            ctx.set_dash([])
            flag(ctx, 60, 760, 210, 140, "in", t, pole=230)
            for key, name, body, home in (("tesla", "TESLA", hexc("#D9DCE2"), 330), ("tata", "TATA", SAFFRON, 770)):
                uc = t - b[key]
                if uc <= 0:
                    continue
                x = lerp(-300, home, ease_out_cubic(uc / 0.8))
                ev_car(ctx, x, 1040, 0.85, t, body, spin=-t * 14 if uc < 0.8 else 0)
                plate(ctx, name, x, 830, EV_GREEN, uc - 0.5, size=46)
        u = t - b["china"]
        if u > 0:
            ctx.save()
            ctx.translate(820, 300)
            pop = ease_out_back(u / 0.3)
            ctx.scale(pop, pop)
            rrect(ctx, -8, -8, 236, 156, 10)
            rgba(ctx, (0, 0, 0), 0.75)
            ctx.fill()
            cn_flag(ctx, 0, 0, 220, 140)
            ctx.restore()
            red_cross(ctx, 930, 370, t - b["no"], size=95)
        u = t - b["no"]
        if u > 0:
            stamp(ctx, 400, 360, u, -0.06, 560, 160, EV_GREEN, [("NO NEED!", 0, 120, EV_GREEN)])


class Future(cs.Cued):
    """India's EV graph shoots up toward 2030; CHINA IN DANGER, EV-hub question card, comment icon, subscribe."""

    def beats(self, d):
        c = self.cue
        return {"danger": c("खतरे", d * 0.18), "hub": c("2030", d * 0.35), "comment": c("कमेंट", d * 0.68),
                "sub": c("सब्सक्राइब", d * 0.86)}

    def click(self, d):
        return min(d - 0.4, self.beats(d)["sub"] + 0.3)

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["danger"], "alarm"), (b["hub"], "whoosh"), (b["hub"] + 0.4, "kaching"),
                (b["comment"], "pop"), (b["comment"] + 0.2, "dingdong"), (self.click(d), "pick"),
                (self.click(d) + 0.05, "pop")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, *hexc("#06140C"))
        g.add_color_stop_rgb(0.6, *hexc("#2A1606"))
        g.add_color_stop_rgb(1, *hexc("#050302"))
        ctx.set_source(g)
        ctx.paint()
        glow(ctx, 760, 300, 600, EV_GREEN, 0.18)
        x0, x1, y0, y1 = 120, 960, 200, 760
        for k in range(8):
            line(ctx, [(x0, y0 + k * 80), (x1, y0 + k * 80)], (1, 1, 1), 1, 0.1)
        line(ctx, [(x0, y0 - 20), (x0, y1), (x1 + 10, y1)], (1, 1, 1), 3, 0.55)
        for k, yr in enumerate(("2024", "2026", "2028", "2030")):
            text(ctx, yr, x0 + 60 + k * 255, y1 + 36, 32, (1, 1, 1), font=CAPTION_FONT, bold=False, a=0.6)
        grow = ease_in_out(t / max(b["hub"] + 0.6, 1.0))
        cn = [(x0 + (x1 - x0) * k / 9, y) for k, y in enumerate((240, 245, 262, 290, 330, 380, 440, 500, 560, 620))]
        ind = [(x0 + (x1 - x0) * k / 9, y) for k, y in enumerate((740, 735, 725, 705, 670, 620, 545, 450, 330, 200))]
        for pts, c, lab in ((cn, CN_RED, "CHINA SHARE"), (ind, SAFFRON, "INDIA EV")):
            drawn, head = partial(pts, grow)
            line(ctx, drawn, c, 22, 0.25)
            line(ctx, drawn, c, 8)
            glow(ctx, *head, 44, c, 0.9)
            circle(ctx, *head, 9, (1, 1, 1))
            if grow > 0.55:
                plate(ctx, lab, min(head[0] - 70, 840), head[1] + (60 if c is CN_RED else -64), c, 1.0, size=34)
        if grow >= 1:  # the arrowhead on India's line
            hx, hy = ind[-1]
            ang = math.atan2(hy - ind[-2][1], hx - ind[-2][0])
            ctx.move_to(hx + 40 * math.cos(ang), hy + 40 * math.sin(ang))
            for da in (2.5, -2.5):
                ctx.line_to(hx + 34 * math.cos(ang + da), hy + 34 * math.sin(ang + da))
            ctx.close_path()
            rgba(ctx, SAFFRON)
            ctx.fill()
        u = t - b["danger"]
        if u > 0 and t < b["hub"]:
            ctx.save()
            if u < 0.3:
                ctx.translate(12 * (1 - u / 0.3) * math.sin(u * 90), 0)
            stamp(ctx, 540, 920, u, -0.05, 640, 150, RED, [("CHINA IN DANGER", 0, 76, RED)])
            ctx.restore()
        u = t - b["hub"]
        if u > 0 and t < b["comment"]:  # the question card
            pop = ease_out_back(u / 0.3)
            ctx.save()
            ctx.translate(540, 920)
            ctx.scale(pop, pop)
            rrect(ctx, -420, -110, 840, 220, 28)
            rgba(ctx, (0.03, 0.03, 0.06), 0.92)
            ctx.fill_preserve()
            rgba(ctx, GOLD)
            ctx.set_line_width(5)
            ctx.stroke()
            battery(ctx, -320, 6, 70, 130, 0.5 + 0.5 * (0.5 + 0.5 * math.sin(t * 3)), EV_GREEN)
            cs.bolt(ctx, -320, 6, 0.8, (1, 1, 1))
            text(ctx, "WORLD'S EV HUB", 50, -38, 66, (1, 1, 1), font=CAPTION_FONT, bold=False)
            text(ctx, "BY 2030?", 50, 44, 70, GOLD, font=CAPTION_FONT, bold=False)
            ctx.restore()
        if t >= b["comment"]:  # chart steps back for the CTA
            ctx.rectangle(0, 0, W, H)
            rgba(ctx, (0.02, 0.01, 0.03), 0.5 * clamp((t - b["comment"]) / 0.4))
            ctx.fill()
        comment_bubble(ctx, 540, 560, t - b["comment"], t)
        u = t - b["comment"]
        if u > 0:
            ctx.save()
            ctx.translate(540, 1000)
            pop = ease_out_back(u / 0.35)
            ctx.scale(pop, pop)
            ctx.translate(-540, -1000)
            bx, by = subscribe_badge(ctx, 540, 1000, t, t >= self.click(d))
            ctx.restore()
            bell(ctx, 120, 1000, 0.9, t)
            cursor_click(ctx, t, self.click(d), bx, by)


SCENE_CLASSES = {"lithium": Lithium, "monopoly": Monopoly, "reasi": Reasi, "future": Future}


def make_frame(t: float) -> np.ndarray:
    scenes = engine.SCENES
    idx = max(i for i, s in enumerate(scenes) if t >= s["start"] or i == 0)
    surf = cs.compose(idx, t - scenes[idx]["start"], SPEC)
    surf.flush()
    buf = np.ndarray((H, W, 4), dtype=np.uint8, buffer=surf.get_data())
    return buf[:, :, 2::-1].copy()


def main() -> None:
    story = importlib.import_module("generate_lithium_short")  # a named module, so work files land in work/<name>/
    engine.make_frame = story.make_frame
    final = engine.render(story, "edge")
    cs.write_alignment(final, SPEC)


if __name__ == "__main__":
    main()
