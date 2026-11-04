"""Reality Shift Short — India's boycott vs Maldives (~33s, pure Devanagari edge-tts voiceover).

Usage:
  python generate_maldives_short.py

Same pipeline and Golden Safe Zone layout as generate_chabahar_short.py (whose compositor, badge,
plates and leader busts it reuses): watermark top-centre, on-screen text badge locked to Y 1150-1250,
bottom 400px clean, ending on the comment + subscribe CTA.
Output: output/shorts/maldives_boycott_short.mp4 (+ a .json with the scene/word alignment).
"""

import importlib
import math

import cairo
import numpy as np

import engine
import generate_chabahar_short as cs
from engine import *  # noqa: F401,F403
from generate_chabahar_short import NEON, RED, Cued, bell, bust, flash, partial, plate
from stories.reality_shift import GOLD, INDIA_GREEN, SAFFRON, flag, hero, stamp, subscribe_badge

TOPIC = "INDIA VS MALDIVES"
OUTPUTS = {"edge": "maldives_boycott_short.mp4"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.18
TAIL_PAD = 0.08                # scene length = audio duration + 0.08s
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 112
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"

CN_RED = hexc("#DE2910")
CN_YELLOW = hexc("#FFDE00")
MV_RED = hexc("#D21034")
MV_GREEN = hexc("#007E3A")
LAGOON = hexc("#19C3C9")

SPEC = [
    {"key": "loss", "window": "0:00-0:06", "icon": "chart", "accent": RED,
     "vo": [("ask", "क्या आपको पता है...?"),
            ("build", "भारत के सिर्फ 60 दिन के बॉयकॉट ने"),
            ("tell", "मालदीव को 500 मिलियन डॉलर का..."),
            ("punch", "तगड़ा झटका दे दिया!")],
     "text": "500M KA LOSS!",
     "visual": "Split screen: empty Maldives water villas over a red crash chart showing -$500M"},
    {"key": "china", "window": "0:06-0:13", "icon": "cn", "accent": CN_RED,
     "vo": [("low", "प्रेसिडेंट मुइज़्ज़ू ने 'इंडिया आउट' के नारे लगाए,"),
            ("low", "और सोचा कि..."),
            ("sly", "चाइना आकर उनको बचा लेगा!")],
     "text": "CHINA SE MADAD?",
     "visual": "News-style frame: Muizzu with Xi Jinping, INDIA OUT slam, sinking boat"},
    {"key": "crash", "window": "0:13-0:23", "icon": "beachx", "accent": RED,
     "vo": [("punch", "लेकिन...", 0.22),
            ("build", "जैसे ही इंडियन टूरिस्ट्स ने अपनी फ्लाइट्स कैंसिल कीं,"),
            ("build", "मालदीव की पूरी टूरिज्म इंडस्ट्री क्रैश हो गई,", 0.08),
            ("tell", "और उनका फॉरेक्स रिज़र्व्..."),   # final halant: without it the voice says "reserva"
            ("punch", "खाली हो गया!")],
     "text": "TOURISM CRASHED",
     "visual": "Empty beach, cancelled flight tickets, #Lakshadweep trending, forex reserves draining"},
    {"key": "bailout", "window": "0:23-0:33", "icon": "bell", "accent": hexc("#FF0000"),
     "vo": [("sly", "और आज?"),
            ("tell", "वही मुइज़्ज़ू भारत के सामने 400 मिलियन डॉलर का बेलआउट मांग रहे हैं।"),
            ("ask", "क्या भारत को उनकी मदद करनी चाहिए?", 0.28),
            ("cta", "कमेंट्स में बताओ,", 0.04),
            ("cta", "और रियलिटी शिफ्ट को सब्सक्राइब करो!")],
     "text": "SUBSCRIBE @RealityShift",
     "visual": "Muizzu with PM Modi in New Delhi, $400M bailout, YES/NO poll, comment icon, subscribe click"},
]

# each scene is performed line by line (engine.TONES): its own pace, pitch and loudness per line,
# punctuation-sized pauses with a soft breath between, so the edge voice reads like a narrator
DELIVERY = {s["key"]: s["vo"] for s in SPEC}
ROOM = 0.12
NARRATION = {s["key"]: " ".join(line[1] for line in s["vo"]) for s in SPEC}
SCRIPT = [(s["key"], [(w, w) for w in NARRATION[s["key"]].split()]) for s in SPEC]


# ============================================================ flags + icons

def star(ctx, x, y, r, rot, c, a=1.0):
    cs.Masterstroke.star(ctx, x, y, r, rot, c, a)


def cn_flag(ctx, x, y, w, h, a=1.0):
    ctx.rectangle(x, y, w, h)
    rgba(ctx, CN_RED, a)
    ctx.fill()
    star(ctx, x + w * 0.17, y + h * 0.27, h * 0.17, 0, CN_YELLOW, a)
    for sx, sy in ((0.33, 0.1), (0.4, 0.2), (0.4, 0.35), (0.33, 0.45)):
        star(ctx, x + w * sx, y + h * sy, h * 0.057, 0.4, CN_YELLOW, a)


def mv_flag(ctx, x, y, w, h, a=1.0):
    ctx.rectangle(x, y, w, h)
    rgba(ctx, MV_RED, a)
    ctx.fill()
    ctx.rectangle(x + w * 0.25, y + h * 0.25, w * 0.5, h * 0.5)
    rgba(ctx, MV_GREEN, a)
    ctx.fill()
    circle(ctx, x + w * 0.5, y + h * 0.5, h * 0.17, (1, 1, 1), a)
    circle(ctx, x + w * 0.54, y + h * 0.5, h * 0.15, MV_GREEN, a)


def chart_icon(ctx, x, y, t):
    line(ctx, [(x - 30, y - 30), (x - 30, y + 30), (x + 34, y + 30)], (1, 1, 1), 5)
    pts = [(x - 24, y - 20), (x - 8, y - 6), (x + 4, y - 14), (x + 26, y + 18)]
    line(ctx, pts, RED, 7)
    circle(ctx, x + 26, y + 18, 7, RED)


def umbrella(ctx, x, y, s, open_=1.0, c=hexc("#FF6B3D")):
    """Beach umbrella with its pole foot at (x, y); open_ 0 = furled."""
    line(ctx, [(x, y), (x, y - 150 * s)], hexc("#EFE6D2"), 6 * s)
    r = 110 * s
    ctx.move_to(x - r * open_, y - 140 * s + 30 * s * (1 - open_))
    ctx.curve_to(x - r * open_ * 0.6, y - 210 * s, x + r * open_ * 0.6, y - 210 * s, x + r * open_,
                 y - 140 * s + 30 * s * (1 - open_))
    ctx.line_to(x + 6 * s, y - 60 * s * (1 - open_) - 140 * s * open_)
    ctx.line_to(x - 6 * s, y - 60 * s * (1 - open_) - 140 * s * open_)
    ctx.close_path()
    rgba(ctx, c)
    ctx.fill()


def beach_x_icon(ctx, x, y, t):
    umbrella(ctx, x, y + 32, 0.38)
    for sx in (-1, 1):
        line(ctx, [(x - 30, y - 30 * sx), (x + 30, y + 30 * sx)], RED, 9)


cs.ICONS.update({
    "chart": chart_icon,
    "cn": lambda ctx, x, y, t: cn_flag(ctx, x - 38, y - 25, 76, 50),
    "beachx": beach_x_icon,
})


# ============================================================ props

def villa(ctx, x, y, s, t, k):
    """Overwater villa on stilts, deck at (x, y), lights out."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for sx in (-70, -25, 25, 70):
        line(ctx, [(sx, 10), (sx, 90)], hexc("#5A3A22"), 8)
        line(ctx, [(sx, 92), (sx, 130)], hexc("#5A3A22"), 6, 0.25 + 0.1 * math.sin(t * 2 + sx))
    ctx.rectangle(-100, 0, 200, 16)
    rgba(ctx, hexc("#8A5A32"))
    ctx.fill()
    ctx.rectangle(-72, -84, 144, 84)
    rgba(ctx, hexc("#EAD9B5"))
    ctx.fill()
    for wx in (-48, 20):
        ctx.rectangle(wx, -62, 28, 30)
    rgba(ctx, hexc("#1B2A33"))
    ctx.fill()
    ctx.move_to(-108, -78)
    ctx.line_to(0, -160 - 6 * (k % 2))
    ctx.line_to(108, -78)
    ctx.close_path()
    rgba(ctx, hexc("#9A6A34"))
    ctx.fill()
    for j in range(6):
        line(ctx, [(-90 + j * 36, -82), (-60 + j * 24, -130)], hexc("#7A4E22"), 3)
    ctx.restore()


def palm(ctx, x, y, s, t, lean=1):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(lean * s, s)
    ctx.move_to(0, 0)
    ctx.curve_to(10, -150, 40, -280, 90, -380)
    rgba(ctx, hexc("#7A5634"))
    ctx.set_line_width(26)
    ctx.stroke()
    sway = 0.06 * math.sin(t * 1.5)
    for k in range(7):
        a = -math.pi / 2 + (k - 3) * 0.5 + sway
        ctx.move_to(90, -380)
        ctx.curve_to(90 + 90 * math.cos(a - 0.3), -380 + 90 * math.sin(a - 0.3) - 20,
                     90 + 170 * math.cos(a), -380 + 170 * math.sin(a) + 30,
                     90 + 200 * math.cos(a), -380 + 200 * math.sin(a) + 70)
        rgba(ctx, hexc("#1F7A3A"))
        ctx.set_line_width(22)
        ctx.stroke()
    ctx.restore()


def lounger(ctx, x, y, s):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    line(ctx, [(-90, 0), (60, 0), (110, -60)], hexc("#FFFFFF"), 18)
    for lx in (-80, 50):
        line(ctx, [(lx, 0), (lx, 26)], hexc("#C9C2B0"), 6)
    ctx.restore()


def ticket(ctx, x, y, rot, s, cancel_u):
    """Delhi -> Male boarding pass; cancel_u = seconds since its CANCELLED stamp."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    rrect(ctx, -300, -100, 600, 200, 18)
    rgba(ctx, (0.98, 0.98, 0.97))
    ctx.fill()
    rrect(ctx, -300, -100, 140, 200, 18)
    rgba(ctx, SAFFRON)
    ctx.fill()
    for k in range(9):
        circle(ctx, -160, -88 + k * 22, 4, (0.85, 0.85, 0.85))
    text(ctx, "BOARDING PASS", -230, 0, 26, (1, 1, 1), font=CAPTION_FONT, bold=False)
    text(ctx, "DELHI", -40, -30, 58, hexc("#1A2340"), font=CAPTION_FONT, bold=False)
    text(ctx, "MALE", 200, -30, 58, hexc("#1A2340"), font=CAPTION_FONT, bold=False)
    line(ctx, [(40, -30), (120, -30)], hexc("#1A2340"), 5)
    ctx.move_to(130, -30)
    ctx.line_to(112, -42)
    ctx.line_to(112, -18)
    ctx.close_path()
    rgba(ctx, hexc("#1A2340"))
    ctx.fill()
    text(ctx, "FLIGHT AI 263  ·  SEAT 14A", 80, 50, 28, (0.4, 0.4, 0.45), font=CAPTION_FONT, bold=False)
    if cancel_u > 0:
        k = lerp(2.2, 1.0, ease_out_cubic(cancel_u / 0.16))
        ctx.save()
        ctx.translate(70, 0)
        ctx.rotate(-0.22)
        ctx.scale(k, k)
        rrect(ctx, -200, -50, 400, 100, 10)
        rgba(ctx, RED, 0.95)
        ctx.set_line_width(9)
        ctx.stroke()
        text(ctx, "CANCELLED", 0, 0, 72, RED, font=CAPTION_FONT, bold=False)
        ctx.restore()
    ctx.restore()


def india_gate(ctx, x, y, s, c):
    """India Gate silhouette with its base centred on (x, y)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.rectangle(-170, -420, 340, 420)
    ctx.rectangle(-190, -470, 380, 50)
    ctx.rectangle(-150, -520, 300, 50)
    ctx.rectangle(-90, -560, 180, 40)
    rgba(ctx, c)
    ctx.fill()
    ctx.move_to(-75, 0)
    ctx.line_to(-75, -230)
    ctx.arc(0, -230, 75, math.pi, 2 * math.pi)
    ctx.line_to(75, 0)
    ctx.close_path()
    rgba(ctx, hexc("#2A1C3A"))
    ctx.fill()
    ctx.restore()


def comment_bubble(ctx, x, y, u, t):
    if u <= 0:
        return
    pop = ease_out_back(u / 0.3) * (1 + 0.05 * math.sin(t * 7))
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(pop, pop)
    glow(ctx, 0, 0, 140, (1, 1, 1), 0.25)
    rrect(ctx, -80, -60, 160, 110, 30)
    ctx.move_to(-40, 45)
    ctx.line_to(-60, 85)
    ctx.line_to(-5, 48)
    ctx.close_path()
    rgba(ctx, (1, 1, 1))
    ctx.fill()
    for k in (-1, 0, 1):
        circle(ctx, k * 38, -5, 11, hexc("#1A2340"))
    text(ctx, "COMMENT", 0, 125, 40, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=8)
    ctx.restore()


def cursor_click(ctx, t, click, bx, by):
    """White pointer gliding in from the right and pressing at time click."""
    cu = clamp((t - (click - 0.8)) / 0.7)
    if cu <= 0:
        return
    cx, cy = lerp(1040, bx + 20, ease_in_out(cu)), lerp(1110, by + 20, ease_in_out(cu))
    sc = 0.85 if abs(t - click) < 0.12 else 1.0
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(sc, sc)
    ctx.move_to(0, 0)
    for px, py in ((0, 62), (16, 48), (28, 74), (40, 68), (28, 43), (48, 42)):
        ctx.line_to(px, py)
    ctx.close_path()
    rgba(ctx, (1, 1, 1))
    ctx.fill_preserve()
    rgba(ctx, (0, 0, 0))
    ctx.set_line_width(3)
    ctx.stroke()
    ctx.restore()


# ============================================================ scenes

class Loss(Cued):
    """Split screen: empty water villas on top, revenue crash chart with -$500M below."""

    def beats(self, d):
        c = self.cue
        return {"days": c("60", d * 0.3), "boycott": c("बॉयकॉट", d * 0.4), "loss": c("500", d * 0.6),
                "hit": c("झटका", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        ticks = [(b["days"] + k * 0.1, "tick" if k % 2 else "tock") for k in range(12)]
        return [(0.02, "boom"), (b["boycott"], "thud"), (b["loss"], "boom"), (b["loss"] + 0.05, "thud"),
                (b["hit"], "beep")] + ticks

    def draw(self, ctx, t, d):
        b = self.beats(d)
        # top: lagoon with empty villas
        g = cairo.LinearGradient(0, 0, 0, 380)
        g.add_color_stop_rgb(0, *hexc("#3FA9D8"))
        g.add_color_stop_rgb(1, *hexc("#BDEFFF"))
        ctx.set_source(g)
        ctx.paint()
        g = cairo.LinearGradient(0, 380, 0, 640)
        g.add_color_stop_rgb(0, *LAGOON)
        g.add_color_stop_rgb(1, *hexc("#0A7F9E"))
        ctx.rectangle(0, 380, W, 260)
        ctx.set_source(g)
        ctx.fill()
        for i in range(18):
            y = 400 + 230 * rnd(i, 1)
            x = (rnd(i, 2) * W + t * 20) % (W + 100) - 50
            line(ctx, [(x, y), (x + 50, y)], (1, 1, 1), 3, 0.3)
        line(ctx, [(-20, 505), (W + 20, 470)], hexc("#8A5A32"), 12)
        for k, x in enumerate((120, 340, 560, 780, 1000)):
            villa(ctx, x, 470 - k * 7, 0.85, t, k)
        if b["hit"] <= t:  # the colour drains out once the loss lands
            ctx.rectangle(0, 0, W, 640)
            rgba(ctx, (0.25, 0.25, 0.28), 0.45 * clamp((t - b["hit"]) / 0.6))
            ctx.fill()
        plate(ctx, "EMPTY VILLAS", 540, 590, RED, t - 0.3, size=40)
        if t >= b["boycott"]:
            plate(ctx, "#BOYCOTTMALDIVES", 540, 200, SAFFRON, t - b["boycott"], size=56)
        # bottom: revenue crash chart
        g = cairo.LinearGradient(0, 640, 0, 1150)
        g.add_color_stop_rgb(0, *hexc("#1A070B"))
        g.add_color_stop_rgb(1, *hexc("#050203"))
        ctx.rectangle(0, 640, W, H - 640)
        ctx.set_source(g)
        ctx.fill()
        for k in range(6):
            line(ctx, [(100, 760 + k * 64), (980, 760 + k * 64)], (1, 1, 1), 1, 0.12)
        line(ctx, [(100, 740), (100, 1090), (990, 1090)], (1, 1, 1), 3, 0.6)
        text(ctx, "TOURISM REVENUE", 110, 700, 38, (1, 1, 1), font=CAPTION_FONT, bold=False, a=0.85, anchor="l")
        pts = [(110, 860), (230, 840), (340, 800), (430, 815), (520, 790), (600, 880), (700, 930), (790, 1010),
               (880, 1040), (960, 1075)]
        drawn, head = partial(pts, ease_in_out((t - 0.2) / max(b["hit"] - 0.2, 0.5)))
        line(ctx, drawn, RED, 22, 0.25)
        line(ctx, drawn, RED, 8)
        glow(ctx, *head, 40, RED, 0.9)
        circle(ctx, *head, 9, (1, 1, 1))
        u = t - b["days"]
        if u > 0:
            n = int(60 * ease_out_cubic(u / 1.2))
            plate(ctx, f"DAY {n}", 880, 710, SAFFRON, u, size=42)
        u = t - b["loss"]
        if u > 0:
            stamp(ctx, 540, 900, u, -0.06, 560, 170, RED, [("-$500M", 0, 130, RED)])
        line(ctx, [(0, 640), (W, 640)], RED, 16, 0.35)
        line(ctx, [(0, 640), (W, 640)], (1, 1, 1), 4)


class China(Cued):
    """News frame: Muizzu with Xi Jinping, INDIA OUT slam, then the sinking boat."""

    def beats(self, d):
        c = self.cue
        return {"out": c("इंडिया", d * 0.2), "china": c("चाइना", d * 0.6), "sink": c("बचा", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (0.3, "beep"), (b["out"], "boom"), (b["out"] + 0.02, "thud"),
                (b["china"], "zap"), (b["sink"], "whoosh"), (b["sink"] + 0.4, "soft_thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, *hexc("#2E0508"))
        g.add_color_stop_rgb(1, *hexc("#080102"))
        ctx.set_source(g)
        ctx.paint()
        cn_on = clamp((t - b["china"]) / 0.4)
        glow(ctx, 800, 520, 560, CN_RED, 0.25 + 0.35 * cn_on)
        cn_flag(ctx, 560, 380, 480, 320, 0.22 + 0.3 * cn_on)
        mv_flag(ctx, 40, 380, 480, 320, 0.22)
        for i in range(10):  # studio light streaks
            x = (i * 140 + t * 40) % (W + 200) - 100
            line(ctx, [(x, 0), (x - 300, H)], (1, 1, 1), 2, 0.04)
        bust(ctx, 290, 640, 0.78, t, hexc("#1C2233"), hexc("#3A6EA5"), None, 0, mood="smug")
        bust(ctx, 800, 660, 0.78, t, hexc("#1C2233"), hexc("#B3121F"), None, 0, mood="smug")
        plate(ctx, "MUIZZU", 290, 930, MV_GREEN, t - 0.2, size=46, sub="PRESIDENT, MALDIVES")
        plate(ctx, "XI JINPING", 800, 930, CN_RED, t - 0.35, size=46, sub="CHINA")
        # LIVE tag + breaking ticker
        if int(t * 2) % 2 == 0:
            circle(ctx, 92, 172, 10, RED)
        text(ctx, "LIVE", 114, 172, 40, (1, 1, 1), font=CAPTION_FONT, bold=False, anchor="l")
        ctx.rectangle(0, 1050, W, 72)
        rgba(ctx, (0.96, 0.96, 0.96))
        ctx.fill()
        ctx.rectangle(0, 1050, 230, 72)
        rgba(ctx, RED)
        ctx.fill()
        ctx.save()
        ctx.rectangle(230, 1050, W - 230, 72)
        ctx.clip()
        tx = W - (t * 220) % 1400
        text(ctx, "MALDIVES TURNS TO CHINA  ·  'INDIA OUT' CAMPAIGN", tx, 1086, 40, hexc("#1A1A1A"),
             font=CAPTION_FONT, bold=False, anchor="l")
        ctx.restore()
        text(ctx, "BREAKING", 115, 1086, 42, (1, 1, 1), font=CAPTION_FONT, bold=False)
        u = t - b["out"]
        if u > 0 and t < b["sink"]:
            if u < 0.3:
                ctx.translate(14 * (1 - u / 0.3) * math.sin(u * 90), 0)
            stamp(ctx, 540, 290, u, -0.07, 780, 190, RED, [("INDIA OUT", 0, 150, RED)])
        u = t - b["sink"]
        if u > 0:  # doobti naiya: Maldives boat sinking
            ctx.save()
            ctx.rectangle(140, 160, 800, 300)
            ctx.clip()
            rrect(ctx, 140, 160, 800, 300, 24)
            rgba(ctx, hexc("#0A3A5A"), 0.92)
            ctx.fill()
            sink = ease_in_out(u / 2.2)
            ctx.save()
            ctx.translate(540, 330 + 110 * sink)
            ctx.rotate(0.35 * sink)
            ctx.move_to(-170, -20)
            ctx.line_to(170, -20)
            ctx.line_to(120, 50)
            ctx.line_to(-120, 50)
            ctx.close_path()
            rgba(ctx, hexc("#8A5A32"))
            ctx.fill()
            line(ctx, [(0, -20), (0, -140)], hexc("#DDDDDD"), 6)
            mv_flag(ctx, 3, -140, 96, 64)
            ctx.restore()
            for k in range(3):
                y = 360 + k * 18
                pts = [(140 + x, y + 8 * math.sin(x / 40 + t * 4 + k)) for x in range(0, 801, 20)]
                line(ctx, pts, LAGOON, 8, 0.8 - k * 0.2)
            ctx.rectangle(140, 380, 800, 80)
            rgba(ctx, hexc("#0E5C80"), 0.85)
            ctx.fill()
            ctx.restore()
            plate(ctx, "SINKING ECONOMY", 540, 190, RED, u - 0.2, size=44)


class Crash(Cued):
    """Empty beach: cancelled tickets, #Lakshadweep trending, forex reserves draining."""

    def beats(self, d):
        c = self.cue
        return {"stop": c("कैंसिल", d * 0.3), "halt": c("क्रैश", d * 0.6), "forex": c("फॉरेक्स", d * 0.72),
                "empty": c("खाली", d * 0.9)}

    def events(self, d):
        b = self.beats(d)
        stamps = [(b["stop"] + 0.3 + k * 0.35, "thud") for k in range(3)]
        return [(0.02, "boom"), (b["stop"], "whoosh"), (b["halt"], "zap"), (b["forex"], "alarm"),
                (b["empty"], "boom")] + stamps

    def draw(self, ctx, t, d):
        b = self.beats(d)
        g = cairo.LinearGradient(0, 0, 0, 560)
        g.add_color_stop_rgb(0, *hexc("#4FB6E8"))
        g.add_color_stop_rgb(1, *hexc("#DDF5FF"))
        ctx.set_source(g)
        ctx.paint()
        g = cairo.LinearGradient(0, 560, 0, 740)
        g.add_color_stop_rgb(0, *LAGOON)
        g.add_color_stop_rgb(1, *hexc("#7FE3D8"))
        ctx.rectangle(0, 560, W, 180)
        ctx.set_source(g)
        ctx.fill()
        g = cairo.LinearGradient(0, 740, 0, H)
        g.add_color_stop_rgb(0, *hexc("#F2DDB0"))
        g.add_color_stop_rgb(1, *hexc("#C9A874"))
        ctx.rectangle(0, 740, W, H - 740)
        ctx.set_source(g)
        ctx.fill()
        foam = [(x, 742 + 8 * math.sin(x / 60 + t * 2)) for x in range(0, W + 21, 20)]
        line(ctx, foam, (1, 1, 1), 10, 0.8)
        palm(ctx, 40, 1000, 1.1, t)
        palm(ctx, 1040, 980, 1.0, t, lean=-1)
        for k, x in enumerate((280, 540, 800)):
            umbrella(ctx, x + 70, 900, 0.9, open_=0.0, c=(SAFFRON, hexc("#2F9BD8"), hexc("#FF6B3D"))[k])
            lounger(ctx, x, 960, 1.0)
        # beach drains of colour as the industry stalls
        ctx.rectangle(0, 0, W, H)
        rgba(ctx, (0.2, 0.2, 0.24), 0.5 * clamp((t - b["halt"]) / 1.5))
        ctx.fill()
        if t < b["stop"]:
            plate(ctx, "NO TOURISTS", 540, 300, RED, t - 0.3, size=56)
        u = t - b["stop"]
        if u > 0 and t < b["halt"] + 0.4:
            off = ease_in_out((t - b["halt"]) / 0.4) if t > b["halt"] else 0
            for k in range(3):
                v = ease_out_back((u - k * 0.2) / 0.4, 1.2)
                if v <= 0:
                    continue
                ticket(ctx, lerp(1500, 540 + (k - 1) * 30, v) - 1700 * off, 230 + k * 200, (k - 1) * 0.06, 1.25,
                       u - 0.3 - k * 0.35)
        u = t - b["halt"]
        if u > 0:  # #Lakshadweep trending card
            pop = ease_out_back(u / 0.35)
            ctx.save()
            ctx.translate(540, 330)
            ctx.scale(pop, pop)
            rrect(ctx, -380, -130, 760, 260, 30)
            rgba(ctx, (0.03, 0.04, 0.08), 0.92)
            ctx.fill_preserve()
            rgba(ctx, NEON)
            ctx.set_line_width(5)
            ctx.stroke()
            flag(ctx, -330, -100, 72, 48, "in", t)
            text(ctx, "TRENDING IN INDIA", -240, -76, 36, (0.75, 0.78, 0.85), font=CAPTION_FONT, bold=False,
                 anchor="l")
            text(ctx, "#Lakshadweep", -330, 30, 96, (1, 1, 1), font=CAPTION_FONT, bold=False, anchor="l")
            ax, ay = 300, -60
            glow(ctx, ax, ay, 60, NEON, 0.6)
            ctx.move_to(ax, ay - 34)
            ctx.line_to(ax + 30, ay + 4)
            ctx.line_to(ax + 12, ay + 4)
            ctx.line_to(ax + 12, ay + 34)
            ctx.line_to(ax - 12, ay + 34)
            ctx.line_to(ax - 12, ay + 4)
            ctx.line_to(ax - 30, ay + 4)
            ctx.close_path()
            rgba(ctx, NEON)
            ctx.fill()
            ctx.restore()
        u = t - b["forex"]
        if u > 0:  # forex reserves draining
            pop = ease_out_back(u / 0.3)
            ctx.save()
            ctx.translate(540, 620)
            ctx.scale(pop, pop)
            rrect(ctx, -400, -90, 800, 180, 24)
            rgba(ctx, (0.04, 0.02, 0.03), 0.92)
            ctx.fill_preserve()
            rgba(ctx, RED)
            ctx.set_line_width(5)
            ctx.stroke()
            text(ctx, "FOREX RESERVES", -360, -46, 44, (1, 1, 1), font=CAPTION_FONT, bold=False, anchor="l")
            level = lerp(0.8, 0.05, ease_in_out((u - 0.2) / max(b["empty"] - b["forex"] + 0.6, 0.8)))
            rrect(ctx, -360, 4, 720, 54, 12)
            rgba(ctx, (1, 1, 1), 0.12)
            ctx.fill()
            rrect(ctx, -360, 4, 720 * level, 54, 12)
            rgba(ctx, RED if level < 0.4 else SAFFRON)
            ctx.fill()
            text(ctx, f"{int(level * 100)}%", 300, -46, 44, RED, font=CAPTION_FONT, bold=False)
            ctx.restore()
        u = t - b["empty"]
        if u > 0:
            stamp(ctx, 540, 830, u, -0.05, 520, 150, RED, [("KHAALI!", 0, 110, RED)])


class Bailout(Cued):
    """New Delhi: Muizzu asks PM Modi for a $400M bailout; YES/NO poll, comment icon, subscribe click."""

    def beats(self, d):
        c = self.cue
        return {"ask": c("400", d * 0.2), "poll": c("क्या", d * 0.45), "comment": c("कमेंट", d * 0.65),
                "sub": c("सब्सक्राइब", d * 0.85)}

    def click(self, d):
        return min(d - 0.4, self.beats(d)["sub"] + 0.3)

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["ask"], "kaching"), (b["poll"], "beep"), (b["comment"], "pop"),
                (b["comment"] + 0.2, "dingdong"), (self.click(d), "pick"), (self.click(d) + 0.05, "pop")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, *hexc("#1A0F2E"))
        g.add_color_stop_rgb(0.55, *hexc("#5A2A14"))
        g.add_color_stop_rgb(1, *hexc("#120804"))
        ctx.set_source(g)
        ctx.paint()
        glow(ctx, 540, 760, 700, SAFFRON, 0.35)
        india_gate(ctx, 540, 1000, 0.95, hexc("#2A1C3A"))
        for k, c in enumerate((SAFFRON, (1, 1, 1), INDIA_GREEN)):
            ctx.rectangle(0, 1000 + k * 10, W, 10)
            rgba(ctx, c, 0.7)
            ctx.fill()
        plate(ctx, "NEW DELHI", 540, 470, GOLD, t - 0.1, size=36)
        bust(ctx, 280, 650, 0.74, t, hexc("#1C2233"), hexc("#3A6EA5"), None, 0)
        hero(ctx, 790, 720, 0.55, t, d, pose="namaste")
        plate(ctx, "MUIZZU", 280, 930, MV_GREEN, t - 0.2, size=44)
        plate(ctx, "PM MODI", 790, 930, SAFFRON, t - 0.35, size=44)
        u = t - b["ask"]
        if u > 0 and t < b["poll"]:
            stamp(ctx, 540, 280, u, -0.05, 700, 190, GOLD, [("$400M", -20, 110, GOLD),
                                                              ("BAILOUT REQUEST", 60, 40, (1, 1, 1))])
        u = t - b["poll"]
        if u > 0:  # YES / NO poll
            pop = ease_out_back(u / 0.3)
            ctx.save()
            ctx.translate(540, 280)
            ctx.scale(pop, pop)
            rrect(ctx, -400, -150, 800, 300, 28)
            rgba(ctx, (0.03, 0.03, 0.06), 0.92)
            ctx.fill_preserve()
            rgba(ctx, GOLD)
            ctx.set_line_width(5)
            ctx.stroke()
            text(ctx, "BHARAT MADAD KARE?", 0, -95, 56, (1, 1, 1), font=CAPTION_FONT, bold=False)
            for k, (lab, c, share) in enumerate((("YES", INDIA_GREEN, 0.38), ("NO", RED, 0.62))):
                y = -20 + k * 90
                fill = share * ease_out_cubic((u - 0.4) / 1.2)
                rrect(ctx, -360, y - 30, 720, 64, 16)
                rgba(ctx, (1, 1, 1), 0.1)
                ctx.fill()
                rrect(ctx, -360, y - 30, max(720 * fill, 1), 64, 16)
                rgba(ctx, c, 0.9)
                ctx.fill()
                text(ctx, lab, -330, y + 2, 44, (1, 1, 1), font=CAPTION_FONT, bold=False, anchor="l")
                text(ctx, "?", 320, y + 2, 44, (1, 1, 1), font=CAPTION_FONT, bold=False)
            ctx.restore()
        comment_bubble(ctx, 540, 600, t - b["comment"], t)
        u = t - b["comment"]
        if u > 0:
            ctx.save()
            ctx.translate(540, 1050)
            pop = ease_out_back(u / 0.35)
            ctx.scale(pop, pop)
            ctx.translate(-540, -1050)
            bx, by = subscribe_badge(ctx, 540, 1050, t, t >= self.click(d))
            ctx.restore()
            bell(ctx, 120, 1050, 0.9, t)
            cursor_click(ctx, t, self.click(d), bx, by)


SCENE_CLASSES = {"loss": Loss, "china": China, "crash": Crash, "bailout": Bailout}


def make_frame(t: float) -> np.ndarray:
    scenes = engine.SCENES
    idx = max(i for i, s in enumerate(scenes) if t >= s["start"] or i == 0)
    surf = cs.compose(idx, t - scenes[idx]["start"], SPEC)
    surf.flush()
    buf = np.ndarray((H, W, 4), dtype=np.uint8, buffer=surf.get_data())
    return buf[:, :, 2::-1].copy()


def main() -> None:
    story = importlib.import_module("generate_maldives_short")  # a named module, so work files land in work/<name>/
    engine.make_frame = story.make_frame
    final = engine.render(story, "edge")
    cs.write_alignment(final, SPEC)


if __name__ == "__main__":
    main()
