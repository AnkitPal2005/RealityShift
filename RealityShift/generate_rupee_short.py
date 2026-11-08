"""Reality Shift Short — 22 countries trading in Rupees, not Dollars (~33s, pure Devanagari edge-tts voiceover).

Usage:
  python generate_rupee_short.py

Same pipeline and Golden Safe Zone layout as generate_maldives_short.py (whose comment bubble and cursor it
reuses, along with Chabahar's compositor, map, plates and cargo ship): watermark top-centre, on-screen text badge
locked to Y 1150-1250, bottom 400px clean, ending on the comment + subscribe CTA.
Output: output/shorts/rupee_vostro_short.mp4 (+ a .json with the scene/word alignment).
"""

import importlib
import math

import cairo
import numpy as np

import engine
import generate_chabahar_short as cs
from engine import *  # noqa: F401,F403
from generate_chabahar_short import (CITIES, NEON, RED, RU_LEG, SEA_LEG, Cued, bell, container_ship, draw_map,
                                     flash, partial, plate, poly, proj, route, view_at)
from generate_maldives_short import comment_bubble, cursor_click
from stories.reality_shift import GOLD, INDIA_GREEN, SAFFRON, embers, flag, stamp, subscribe_badge

TOPIC = "RUPEE VS DOLLAR"
OUTPUTS = {"edge": "rupee_vostro_short.mp4"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.18
TAIL_PAD = 0.08                # scene length = audio duration + 0.08s
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 112
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"

USD_GREEN = hexc("#2E6B3F")
BILL = hexc("#CFE3C4")
US_BLUE = hexc("#3C3B6E")
US_RED = hexc("#B22234")
FIRE = hexc("#FF7A1A")
AE_GREEN = hexc("#00732F")
LK_MAROON = hexc("#8D153A")
LK_GOLD = hexc("#FFBE29")

SPEC = [
    {"key": "usd", "window": "0:00-0:06", "icon": "usdx", "accent": RED,
     "vo": [("ask", "क्या आपको पता है...?"),
            ("build", "दुनिया के 22 देशों ने अचानक"),
            ("tell", "अमेरिकी डॉलर छोड़ कर..."),
            ("punch", "भारतीय रुपये में ट्रेड करना शुरू कर दिया?")],
     "text": "22 COUNTRIES DITCH USD!",
     "visual": "Fast zoom into a US Dollar cracking and burning, then a shining ₹1 coin spinning forward"},
    {"key": "swift", "window": "0:06-0:13", "icon": "lock", "accent": US_RED,
     "vo": [("low", "सालों से अमेरिका"),
            ("low", "अपने डॉलर और स्विफ्ट सिस्टम का इस्तेमाल करके,"),
            ("sly", "दूसरे देशों पर सैंक्शंस लगाता आ रहा था।")],
     "text": "US DOLLAR WEAPON",
     "visual": "Uncle Sam figure locking a bank vault, red stamp: SWIFT SANCTIONS"},
    {"key": "vostro", "window": "0:13-0:24", "icon": "flag", "accent": SAFFRON,
     "vo": [("punch", "लेकिन...", 0.22),
            ("build", "भारत ने वोस्ट्रो अकाउंट्स का ऐसा..."),
            ("punch", "मास्टरस्ट्रोक चला,", 0.1),
            ("tell", "कि रूस, यूएई और श्रीलंका जैसे देश"),
            ("build", "अब बिना डॉलर छुए..."),
            ("punch", "सीधे रुपये में तेल और सामान खरीद रहे हैं!")],
     "text": "DIRECT RUPEE TRADE",
     "visual": "Map linking India to Russia, UAE and Sri Lanka with cargo ships, RBI hub glowing at Mumbai"},
    {"key": "future", "window": "0:24-0:33", "icon": "bell", "accent": hexc("#FF0000"),
     "vo": [("low", "यानी डॉलर का ग्लोबल दबदबा..."),
            ("punch", "अब खतरे में है।", 0.2),
            ("ask", "क्या भारतीय रुपया दुनिया की अगली सुपर-करेंसी बन सकता है?", 0.28),
            ("cta", "कमेंट्स में बताओ,", 0.04),
            ("cta", "और रियलिटी शिफ्ट को सब्सक्राइब करो!")],
     "text": "SUBSCRIBE @RealityShift",
     "visual": "Currency chart with the Rupee rising past a falling Dollar, comment icon, subscribe click"},
]

# one narrator throughout: every line keeps the same pitch (pitch swings between lines read as two voices),
# only pace and loudness move so the payoff lines hit harder; level gaps, no breaths, no room reverb
VOICE_TONES = {
    "tell":  ("+14%", "+0Hz", "+10%"),
    "hook":  ("+14%", "+0Hz", "+15%"),
    "ask":   ("+14%", "+0Hz", "+10%"),
    "low":   ("+12%", "+0Hz", "+10%"),
    "sly":   ("+12%", "+0Hz", "+10%"),
    "build": ("+16%", "+0Hz", "+12%"),
    "punch": ("+10%", "+0Hz", "+20%"),
    "cta":   ("+14%", "+0Hz", "+15%"),
}
GAP = 0.12                     # the same pause after every line
DELIVERY = {s["key"]: [(VOICE_TONES[tone], text_, GAP) for tone, text_, *_ in s["vo"]] for s in SPEC}
BREATHS = False
ROOM = 0
NARRATION = {s["key"]: " ".join(line[1] for line in s["vo"]) for s in SPEC}
SCRIPT = [(s["key"], [(w, w) for w in NARRATION[s["key"]].split()]) for s in SPEC]


# ============================================================ money + icons

def dollar_bill(ctx, x, y, s, rot=0.0, a=1.0):
    """Greenback centred on (x, y), 600 x 260 at s = 1."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    rrect(ctx, -300, -130, 600, 260, 14)
    rgba(ctx, BILL, a)
    ctx.fill()
    rrect(ctx, -284, -114, 568, 228, 10)
    rgba(ctx, USD_GREEN, a)
    ctx.set_line_width(6)
    ctx.stroke()
    for k in range(9):  # guilloche
        ctx.arc(0, 0, 40 + k * 9, 0, math.tau)
        rgba(ctx, USD_GREEN, 0.18 * a)
        ctx.set_line_width(2)
        ctx.stroke()
    ctx.save()
    ctx.scale(1, 1.25)
    ctx.arc(0, 0, 92, 0, math.tau)
    ctx.restore()
    rgba(ctx, hexc("#E4F0DC"), a)
    ctx.fill_preserve()
    rgba(ctx, USD_GREEN, a)
    ctx.set_line_width(5)
    ctx.stroke()
    text(ctx, "$", 0, 4, 150, USD_GREEN, font=CAPTION_FONT, bold=False, a=a)
    for cx, cy in ((-230, -70), (230, -70), (-230, 70), (230, 70)):
        text(ctx, "100", cx, cy, 52, USD_GREEN, font=CAPTION_FONT, bold=False, a=a)
    text(ctx, "UNITED STATES DOLLAR", 0, -96, 26, USD_GREEN, font=CAPTION_FONT, bold=False, a=a)
    ctx.restore()


def bill_half(ctx, x, y, s, side, u, t):
    """One half of the bill split along a jagged crack, drifting apart and burning (u = seconds since crack)."""
    crack = [(-14, -130), (12, -80), (-18, -30), (16, 20), (-10, 70), (10, 130)]
    off = 260 * ease_out_cubic(u / 0.9) * side
    ctx.save()
    ctx.translate(x + off, y + 60 * ease_in_out(u / 1.4))
    ctx.rotate(0.35 * side * ease_out_cubic(u / 0.9))
    ctx.translate(-x, -y)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    edge = 340 * side
    ctx.move_to(edge, -140)
    for px, py in crack:
        ctx.line_to(px, py)
    ctx.line_to(edge, 140)
    ctx.close_path()
    ctx.restore()
    ctx.clip()
    dollar_bill(ctx, x, y, s)
    ctx.restore()
    heat = clamp(u / 0.5)
    for k, (px, py) in enumerate(crack):  # fire along the torn edge
        fx = x + off + px * s
        fy = y + py * s + 60 * ease_in_out(u / 1.4)
        f = 0.6 + 0.4 * math.sin(t * 22 + k * 1.7 + side)
        glow(ctx, fx, fy, 110 * s * f, FIRE, 0.7 * heat)
        glow(ctx, fx, fy, 40 * s * f, GOLD, 0.8 * heat)


def rupee_coin(ctx, x, y, r, spin=0.0, a=1.0):
    """Gold ₹1 coin; spin turns it on its vertical axis."""
    k = max(abs(math.cos(spin)), 0.06)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, 1)
    g = cairo.RadialGradient(-r * 0.3, -r * 0.35, r * 0.1, 0, 0, r)
    g.add_color_stop_rgba(0, 1.0, 0.95, 0.65, a)
    g.add_color_stop_rgba(0.6, 0.95, 0.72, 0.18, a)
    g.add_color_stop_rgba(1, 0.66, 0.44, 0.06, a)
    ctx.arc(0, 0, r, 0, math.tau)
    ctx.set_source(g)
    ctx.fill()
    ctx.arc(0, 0, r * 0.86, 0, math.tau)
    rgba(ctx, hexc("#A8730E"), a)
    ctx.set_line_width(r * 0.05)
    ctx.stroke()
    for j in range(48):  # milled rim
        ang = j / 48 * math.tau
        line(ctx, [(r * 0.92 * math.cos(ang), r * 0.92 * math.sin(ang)),
                   (r * 0.99 * math.cos(ang), r * 0.99 * math.sin(ang))], hexc("#8A5C08"), r * 0.02, a)
    if k > 0.3:
        text(ctx, "₹", 0, -r * 0.12, r * 0.95, hexc("#7A4E06"), a=a)
        text(ctx, "1", 0, r * 0.55, r * 0.34, hexc("#7A4E06"), font=CAPTION_FONT, bold=False, a=a)
    ctx.restore()


def usd_x_icon(ctx, x, y, t):
    text(ctx, "$", x, y, 82, hexc("#4CC86A"), font=CAPTION_FONT, bold=False)
    for sx in (-1, 1):
        line(ctx, [(x - 30, y - 30 * sx), (x + 30, y + 30 * sx)], RED, 9)


def padlock(ctx, x, y, s, shut=1.0, c=GOLD):
    """Padlock with its body centred on (x, y); shut 0 = shackle lifted open."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    lift = 26 * (1 - shut)
    ctx.arc(0, -30 - lift, 26, math.pi, 0)
    ctx.line_to(26, -10 - lift)
    ctx.move_to(-26, -10 - lift * (1 - shut))
    ctx.line_to(-26, -30 - lift)
    rgba(ctx, (0.85, 0.87, 0.9))
    ctx.set_line_width(10)
    ctx.stroke()
    rrect(ctx, -38, -16, 76, 58, 10)
    rgba(ctx, c)
    ctx.fill()
    circle(ctx, 0, 8, 8, (0.1, 0.08, 0.02))
    ctx.rectangle(-3, 10, 6, 18)
    ctx.fill()
    ctx.restore()


def ae_flag(ctx, x, y, w, h):
    for k, c in enumerate((AE_GREEN, (1, 1, 1), (0, 0, 0))):
        ctx.rectangle(x, y + k * h / 3, w, h / 3 + 1)
        rgba(ctx, c)
        ctx.fill()
    ctx.rectangle(x, y, w * 0.26, h)
    rgba(ctx, hexc("#FF0000"))
    ctx.fill()


def lk_flag(ctx, x, y, w, h):
    ctx.rectangle(x, y, w, h)
    rgba(ctx, LK_GOLD)
    ctx.fill()
    for k, c in enumerate((hexc("#005F56"), hexc("#FF7300"))):
        ctx.rectangle(x + w * (0.05 + k * 0.12), y + h * 0.08, w * 0.11, h * 0.84)
        rgba(ctx, c)
        ctx.fill()
    ctx.rectangle(x + w * 0.32, y + h * 0.08, w * 0.63, h * 0.84)
    rgba(ctx, LK_MAROON)
    ctx.fill()
    circle(ctx, x + w * 0.63, y + h * 0.5, h * 0.2, LK_GOLD)


cs.ICONS.update({
    "usdx": usd_x_icon,
    "lock": lambda ctx, x, y, t: padlock(ctx, x, y + 6, 0.85),
})


# ============================================================ props

def uncle_sam(ctx, x, y, s, t, arm=0.0):
    """Generic Uncle Sam figure, chin at (x, y); arm 0..1 swings the key hand out to his right."""
    ctx.save()
    ctx.translate(x, y + 3 * math.sin(t * 2))
    ctx.scale(s, s)
    # coat + shoulders
    ctx.move_to(-190, 420)
    ctx.curve_to(-200, 220, -150, 90, 0, 80)
    ctx.curve_to(150, 90, 200, 220, 190, 420)
    ctx.close_path()
    rgba(ctx, US_BLUE)
    ctx.fill()
    ctx.move_to(-40, 80)
    ctx.line_to(0, 210)
    ctx.line_to(40, 80)
    ctx.close_path()
    rgba(ctx, (1, 1, 1))
    ctx.fill()
    ctx.move_to(-22, 90)
    ctx.line_to(22, 90)
    ctx.line_to(0, 130)
    ctx.close_path()
    rgba(ctx, US_RED)
    ctx.fill()
    for k in range(3):
        cs.Masterstroke.star(ctx, -70, 140 + k * 60, 14, 0.3, (1, 1, 1), 1.0)
    # arm with key
    ang = lerp(1.2, -0.15, ease_in_out(arm))
    sx, sy = 150, 140
    hx, hy = sx + 230 * math.cos(ang), sy + 230 * math.sin(ang)
    line(ctx, [(sx, sy), (hx, hy)], US_BLUE, 56)
    circle(ctx, hx, hy, 30, hexc("#F1C9A5"))
    line(ctx, [(hx + 20, hy), (hx + 90, hy)], GOLD, 12)
    for kx in (62, 80):
        line(ctx, [(hx + kx, hy), (hx + kx, hy + 22)], GOLD, 9)
    ctx.arc(hx + 8, hy, 20, 0, math.tau)
    rgba(ctx, GOLD)
    ctx.set_line_width(8)
    ctx.stroke()
    # head
    ctx.save()
    ctx.scale(1, 1.15)
    ctx.arc(0, -40, 72, 0, math.tau)
    ctx.restore()
    rgba(ctx, hexc("#F1C9A5"))
    ctx.fill()
    ctx.move_to(-46, 0)
    ctx.curve_to(-30, 90, 30, 90, 46, 0)
    ctx.curve_to(20, 30, -20, 30, -46, 0)
    rgba(ctx, (0.95, 0.95, 0.95))
    ctx.fill()                                     # goatee
    for ex in (-26, 26):
        circle(ctx, ex, -54, 7, (0.1, 0.1, 0.14))
        line(ctx, [(ex - 18, -76 + (4 if ex < 0 else -4)), (ex + 18, -76 - (4 if ex < 0 else -4))],
             (0.92, 0.92, 0.92), 7)
    line(ctx, [(-22, -6), (0, -14), (22, -6)], (0.55, 0.3, 0.25), 5)
    # top hat
    ctx.rectangle(-110, -120, 220, 22)
    rgba(ctx, (1, 1, 1))
    ctx.fill()
    ctx.rectangle(-70, -300, 140, 182)
    rgba(ctx, (1, 1, 1))
    ctx.fill()
    for k in range(3):
        ctx.rectangle(-70 + k * 50, -300, 22, 150)
        rgba(ctx, US_RED)
        ctx.fill()
    ctx.rectangle(-72, -170, 144, 40)
    rgba(ctx, US_BLUE)
    ctx.fill()
    for k in range(3):
        cs.Masterstroke.star(ctx, -42 + k * 42, -150, 13, 0.3, (1, 1, 1), 1.0)
    ctx.restore()


def vault(ctx, x, y, r, t, spin=0.0, locked=0.0):
    """Round bank-vault door centred on (x, y); spin turns the wheel, locked tints it red."""
    glow(ctx, x, y, r * 1.6, RED, 0.35 * locked)
    ctx.arc(x, y, r * 1.08, 0, math.tau)
    rgba(ctx, hexc("#3A3F48"))
    ctx.fill()
    g = cairo.RadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r)
    g.add_color_stop_rgb(0, *hexc("#B7BEC8"))
    g.add_color_stop_rgb(1, *hexc("#5E6672"))
    ctx.arc(x, y, r, 0, math.tau)
    ctx.set_source(g)
    ctx.fill()
    for k in range(16):  # bolts
        ang = k / 16 * math.tau
        circle(ctx, x + r * 0.9 * math.cos(ang), y + r * 0.9 * math.sin(ang), r * 0.035, hexc("#2C3038"))
    ctx.arc(x, y, r * 0.62, 0, math.tau)
    rgba(ctx, hexc("#2C3038"))
    ctx.set_line_width(r * 0.04)
    ctx.stroke()
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(spin)
    for k in range(6):  # handle wheel
        ang = k / 6 * math.tau
        line(ctx, [(0, 0), (r * 0.48 * math.cos(ang), r * 0.48 * math.sin(ang))], hexc("#D9DEE5"), r * 0.06)
        circle(ctx, r * 0.5 * math.cos(ang), r * 0.5 * math.sin(ang), r * 0.06, hexc("#D9DEE5"))
    circle(ctx, 0, 0, r * 0.13, hexc("#D9DEE5"))
    ctx.restore()
    text(ctx, "$", x, y, r * 0.3, US_BLUE, font=CAPTION_FONT, bold=False)
    if locked:
        ctx.arc(x, y, r * 1.08, 0, math.tau)
        rgba(ctx, RED, 0.9 * locked)
        ctx.set_line_width(10)
        ctx.stroke()


def chain(ctx, x0, y0, x1, y1, u, c=hexc("#AEB4BD")):
    """Chain of oval links from (x0, y0) toward (x1, y1), drawn on to fraction u."""
    n = 14
    ang = math.atan2(y1 - y0, x1 - x0)
    for k in range(int(n * clamp(u))):
        f = (k + 0.5) / n
        ctx.save()
        ctx.translate(lerp(x0, x1, f), lerp(y0, y1, f))
        ctx.rotate(ang)
        ctx.scale(1, 0.55 if k % 2 else 0.3)
        ctx.arc(0, 0, math.dist((x0, y0), (x1, y1)) / n * 0.62, 0, math.tau)
        ctx.restore()
        rgba(ctx, c)
        ctx.set_line_width(9)
        ctx.stroke()


SRI_LANKA = [(79.87, 9.8), (80.25, 9.83), (80.9, 8.9), (81.4, 8.1), (81.85, 7.3), (81.7, 6.4), (80.6, 5.95),
             (80.0, 6.3), (79.85, 7.2), (79.8, 8.2)]
COLOMBO = (79.86, 6.93)
DUBAI = (55.3, 25.27)
UAE_LEG = [CITIES["MUMBAI"], (66.5, 21.6), (60.5, 23.6), (58.0, 24.6), (56.7, 26.4), DUBAI]
LK_LEG = [CITIES["MUMBAI"], (72.0, 14.5), (73.6, 9.0), (76.5, 6.6), COLOMBO]
RUSSIA_LEG = SEA_LEG + RU_LEG[1:]


class Usd(Cued):
    """Fast zoom into a greenback; it cracks and burns on 'छोड़', then a ₹1 coin spins out of the light."""

    def beats(self, d):
        c = self.cue
        return {"n": c("22", d * 0.25), "drop": c("छोड़", d * 0.5), "coin": c("रुपये", d * 0.68),
                "trade": c("ट्रेड", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        ticks = [(b["n"] + k * 0.06, "tick" if k % 2 else "tock") for k in range(10)]
        return [(0.02, "boom"), (0.05, "whoosh"), (b["drop"], "thud"), (b["drop"] + 0.03, "boom"),
                (b["coin"] - 0.15, "whoosh"), (b["coin"] + 0.25, "kaching"), (b["trade"], "beep")] + ticks

    def draw(self, ctx, t, d):
        b = self.beats(d)
        backdrop(ctx, hexc("#0C1A10"), hexc("#020604"), USD_GREEN, 540, 600, t, motes=24)
        dropped = t >= b["drop"]
        if dropped:
            u = t - b["drop"]
            glow(ctx, 540, 600, 700, FIRE, 0.35 * clamp(1 - u / 2.5))
            embers(ctx, t, 26, FIRE, speed=160, seed=3)
            if t < b["coin"] + 0.6:
                fade = 1 - clamp((t - b["coin"]) / 0.6)
                ctx.push_group()
                for side in (-1, 1):
                    bill_half(ctx, 540, 600, 1.45, side, u, t)
                ctx.pop_group_to_source()
                ctx.paint_with_alpha(fade)
        else:
            z = lerp(0.55, 1.45, ease_out_cubic(t / 0.7))  # fast zoom in
            dollar_bill(ctx, 540, 600, z, rot=0.04 * math.sin(t * 3))
            u = t - (b["drop"] - 0.35)
            if u > 0:  # hairline crack runs down before it splits
                pts = [(540 + px * 1.45, 600 + py * 1.45)
                       for px, py in [(-14, -130), (12, -80), (-18, -30), (16, 20), (-10, 70), (10, 130)]]
                drawn, head = partial(pts, u / 0.35)
                line(ctx, drawn, (0.05, 0.05, 0.05), 8)
                glow(ctx, *head, 50, FIRE, 0.9)
        u = t - b["n"]
        if u > 0 and t < b["coin"]:
            n = int(22 * ease_out_cubic(u / 0.6))
            stamp(ctx, 540, 250, u, -0.05, 620, 160, RED, [(f"{n} COUNTRIES", 0, 110, (1, 1, 1))])
        u = t - b["coin"]
        if u > 0:  # ₹1 coin bursts forward out of the light
            for k in range(18):
                ang = k / 18 * math.tau + t * 0.4
                ctx.move_to(540, 600)
                ctx.arc(540, 600, 1400, ang, ang + math.tau / 40)
                ctx.close_path()
                rgba(ctx, GOLD, 0.08 * clamp(u / 0.4))
                ctx.fill()
            glow(ctx, 540, 600, 420, GOLD, 0.6 * clamp(u / 0.3))
            r = lerp(30, 250, ease_out_back(u / 0.6, 1.4))
            rupee_coin(ctx, 540, 600, r, spin=max(0.0, 9.0 - u * 14.0))
            if t >= b["trade"]:
                plate(ctx, "RUPEE TRADE", 540, 940, SAFFRON, t - b["trade"], size=60)
            flash(ctx, u, 0.25, 0.7)


class Swift(Cued):
    """Uncle Sam turns the key on a dollar vault, chains lock the world out, SWIFT SANCTIONS stamp."""

    def beats(self, d):
        c = self.cue
        return {"dollar": c("डॉलर", d * 0.3), "swift": c("स्विफ्ट", d * 0.45), "others": c("दूसरे", d * 0.62),
                "sanction": c("सैंक्शंस", d * 0.78)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["dollar"], "kaching"), (b["swift"], "zap"), (b["swift"] + 0.6, "pick"),
                (b["others"], "alarm"), (b["sanction"], "boom"), (b["sanction"] + 0.02, "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, *hexc("#0B1030"))
        g.add_color_stop_rgb(1, *hexc("#03040C"))
        ctx.set_source(g)
        ctx.paint()
        for k in range(13):  # faint stripes behind
            ctx.rectangle(0, 140 + k * 74, W, 37)
            rgba(ctx, US_RED, 0.05)
            ctx.fill()
        locked = clamp((t - b["sanction"]) / 0.3)
        turn = ease_in_out((t - b["swift"]) / 0.9)
        vault(ctx, 700, 560, 270, t, spin=turn * 2.2, locked=locked)
        uncle_sam(ctx, 250, 700, 0.95, t, arm=turn)
        plate(ctx, "UNCLE SAM", 250, 1080, US_RED, t - 0.3, size=40)
        u = t - b["dollar"]
        if u > 0:
            plate(ctx, "US DOLLAR", 700, 880, GOLD, u, size=44, sub="WORLD RESERVE CURRENCY")
        u = t - b["swift"]
        if u > 0 and t < b["sanction"]:
            plate(ctx, "SWIFT", 860, 250, hexc("#4CC3FF"), u, size=52, sub="BANK NETWORK")
        u = t - b["others"]
        if u > 0:  # chains across the vault, padlock snaps shut
            chain(ctx, 430, 330, 970, 790, u / 0.6)
            chain(ctx, 430, 790, 970, 330, (u - 0.15) / 0.6)
            padlock(ctx, 700, 560, 1.6, shut=clamp((u - 0.5) / 0.15), c=RED if locked else GOLD)
        u = t - b["sanction"]
        if u > 0:
            if u < 0.3:
                ctx.translate(14 * (1 - u / 0.3) * math.sin(u * 90), 0)
            stamp(ctx, 540, 300, u, -0.08, 860, 190, RED, [("SWIFT SANCTIONS", 0, 92, RED)])


class Vostro(Cued):
    """Map out of Mumbai: RBI hub lights up, rupee routes to Russia, UAE and Sri Lanka, cargo ships under way."""

    def beats(self, d):
        c = self.cue
        return {"vostro": c("वोस्ट्रो", d * 0.12), "master": c("मास्टरस्ट्रोक", d * 0.25), "ru": c("रूस", d * 0.38),
                "ae": c("यूएई", d * 0.45), "lk": c("श्रीलंका", d * 0.52), "nousd": c("डॉलर", d * 0.68),
                "inr": c("रुपये", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["vostro"], "dingdong"), (b["master"], "boom"), (b["ru"], "whoosh"),
                (b["ae"], "whoosh"), (b["lk"], "whoosh"), (b["nousd"], "beep"), (b["inr"], "kaching"),
                (b["inr"] + 0.35, "kaching")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        v = view_at([(0.0, (75.0, 20.5, 46)), (b["master"] + 0.2, (73.0, 21.0, 40)),
                     (b["ru"] + 0.8, (60.5, 31.0, 18.5))], t)
        draw_map(ctx, v, t)
        poly(ctx, v, SRI_LANKA)
        rgba(ctx, hexc("#152133"))
        ctx.fill_preserve()
        rgba(ctx, hexc("#4CC3FF"), 0.75)
        ctx.set_line_width(2.5)
        ctx.stroke()
        mx, my = proj(v, *CITIES["MUMBAI"])
        hub = clamp((t - b["vostro"]) / 0.4)
        if hub:  # RBI hub: pulsing rings out of Mumbai
            glow(ctx, mx, my, 260, SAFFRON, 0.45 * hub + 0.1 * math.sin(t * 6))
            for k in range(3):
                r = ((t * 0.7 + k / 3) % 1.0)
                ctx.arc(mx, my, 20 + 170 * r, 0, math.tau)
                rgba(ctx, GOLD, 0.6 * (1 - r) * hub)
                ctx.set_line_width(4)
                ctx.stroke()
            circle(ctx, mx, my, 34 * hub, GOLD)
            text(ctx, "RBI", mx, my, 30 * hub, hexc("#3A2404"), font=CAPTION_FONT, bold=False)
        dashed = b["nousd"] <= t
        flow = []
        for key, leg, end, tint in (("ru", RUSSIA_LEG, CITIES["MOSCOW"], hexc("#4C8DFF")),
                                    ("ae", UAE_LEG, DUBAI, NEON), ("lk", LK_LEG, COLOMBO, GOLD)):
            u = ease_in_out((t - b[key]) / 1.0)
            head = route(ctx, v, leg, u, tint, t, w=6)
            if u >= 1:
                ex, ey = proj(v, *end)
                circle(ctx, ex, ey, 10, (1, 1, 1))
                if dashed:  # rupee coins flowing out along each finished route
                    pts = [proj(v, *p) for p in leg]
                    for k in range(3):
                        f = ((t - b["nousd"]) * 0.45 + k / 3) % 1.0
                        flow.append(partial(pts, f)[1])
            elif head is not None and key != "ru":
                ctx.save()  # cargo ship riding the head of each sea route
                ctx.translate(*head)
                ctx.scale(-1 if key == "ae" else 1, 1)
                container_ship(ctx, 0, 0, 0.13, t, seed=len(key))
                ctx.restore()
        for p in flow:
            glow(ctx, *p, 34, GOLD, 0.7)
            rupee_coin(ctx, *p, 17, spin=t * 3)
        for key, end, x_off, y_off, kind in (("ru", CITIES["MOSCOW"], -70, -60, "ru"), ("ae", DUBAI, -150, -40, "ae"),
                                            ("lk", COLOMBO, 40, -90, "lk")):
            u = t - b[key] - 0.9
            if u > 0:
                ex, ey = proj(v, *end)
                pop = ease_out_back(u / 0.3)
                ctx.save()
                ctx.translate(ex + x_off, ey + y_off)
                ctx.scale(pop, pop)
                rrect(ctx, -6, -6, 102, 70, 6)
                rgba(ctx, (0, 0, 0), 0.7)
                ctx.fill()
                if kind == "ru":
                    flag(ctx, 0, 0, 90, 58, "ru", t)
                elif kind == "ae":
                    ae_flag(ctx, 0, 0, 90, 58)
                else:
                    lk_flag(ctx, 0, 0, 90, 58)
                ctx.restore()
        if t < b["ru"]:
            plate(ctx, "VOSTRO ACCOUNTS", 540, 300, SAFFRON, t - b["vostro"], size=56, sub="RBI · RUPEE SETTLEMENT")
        u = t - b["master"]
        if u > 0 and t < b["ru"] + 0.3:
            stamp(ctx, 540, 470, u, -0.06, 760, 170, GOLD, [("MASTERSTROKE", 0, 120, GOLD)])
        u = t - b["nousd"]
        if u > 0:  # "no dollar" badge, then the payoff
            ctx.save()
            ctx.translate(900, 260)
            ctx.scale(ease_out_back(u / 0.3), ease_out_back(u / 0.3))
            circle(ctx, 0, 0, 78, (0.03, 0.03, 0.05), 0.9)
            text(ctx, "$", 0, 4, 100, hexc("#4CC86A"), font=CAPTION_FONT, bold=False)
            ctx.arc(0, 0, 70, 0, math.tau)
            rgba(ctx, RED)
            ctx.set_line_width(12)
            ctx.stroke()
            line(ctx, [(-50, -50), (50, 50)], RED, 12)
            ctx.restore()
        u = t - b["inr"]
        if u > 0:
            plate(ctx, "OIL + GOODS IN ₹", 440, 1060, GOLD, u, size=54)
        flash(ctx, t - b["master"], 0.25, 0.5)


class Future(Cued):
    """Currency chart: the Dollar dips into the red, the Rupee climbs; question card, comment icon, subscribe."""

    def beats(self, d):
        c = self.cue
        return {"danger": c("खतरे", d * 0.18), "super": c("सुपर", d * 0.45), "comment": c("कमेंट", d * 0.68),
                "sub": c("सब्सक्राइब", d * 0.86)}

    def click(self, d):
        return min(d - 0.4, self.beats(d)["sub"] + 0.3)

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["danger"], "alarm"), (b["super"], "kaching"), (b["comment"], "pop"),
                (b["comment"] + 0.2, "dingdong"), (self.click(d), "pick"), (self.click(d) + 0.05, "pop")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, *hexc("#160B22"))
        g.add_color_stop_rgb(0.6, *hexc("#3A1E08"))
        g.add_color_stop_rgb(1, *hexc("#0B0503"))
        ctx.set_source(g)
        ctx.paint()
        glow(ctx, 540, 520, 640, SAFFRON, 0.28)
        x0, x1, y0, y1 = 110, 970, 200, 760
        for k in range(8):
            line(ctx, [(x0, y0 + k * 80), (x1, y0 + k * 80)], (1, 1, 1), 1, 0.1)
        line(ctx, [(x0, y0 - 20), (x0, y1), (x1 + 10, y1)], (1, 1, 1), 3, 0.55)
        grow = ease_in_out(t / max(b["super"] + 0.4, 1.0))
        usd = [(x0 + (x1 - x0) * k / 9, y) for k, y in
               enumerate((290, 270, 300, 330, 360, 420, 470, 540, 600, 660))]
        inr = [(x0 + (x1 - x0) * k / 9, y) for k, y in
               enumerate((640, 650, 610, 600, 540, 500, 430, 370, 300, 230))]
        for pts, c, lab in ((usd, RED, "$ USD"), (inr, GOLD, "₹ INR")):
            drawn, head = partial(pts, grow)
            line(ctx, drawn, c, 22, 0.25)
            line(ctx, drawn, c, 8)
            glow(ctx, *head, 44, c, 0.9)
            circle(ctx, *head, 9, (1, 1, 1))
            if grow > 0.55:  # the lines have crossed, so the labels sit apart
                plate(ctx, lab, head[0] - 30, head[1] - 60 if c is GOLD else head[1] + 60, c, 1.0, size=36)
        u = t - b["danger"]
        if u > 0 and t < b["super"]:
            ctx.save()
            if u < 0.3:
                ctx.translate(12 * (1 - u / 0.3) * math.sin(u * 90), 0)
            stamp(ctx, 540, 900, u, -0.05, 600, 150, RED, [("DOLLAR IN DANGER", 0, 76, RED)])
            ctx.restore()
        u = t - b["super"]
        if u > 0 and t < b["comment"]:  # the question card
            pop = ease_out_back(u / 0.3)
            ctx.save()
            ctx.translate(540, 920)
            ctx.scale(pop, pop)
            rrect(ctx, -400, -110, 800, 220, 28)
            rgba(ctx, (0.03, 0.03, 0.06), 0.92)
            ctx.fill_preserve()
            rgba(ctx, GOLD)
            ctx.set_line_width(5)
            ctx.stroke()
            rupee_coin(ctx, -290, 0, 74, spin=0.6 * math.sin(t * 2.5))  # wobble, never edge-on
            text(ctx, "NEXT SUPER", 40, -38, 70, (1, 1, 1), font=CAPTION_FONT, bold=False)
            text(ctx, "CURRENCY?", 40, 44, 70, GOLD, font=CAPTION_FONT, bold=False)
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


SCENE_CLASSES = {"usd": Usd, "swift": Swift, "vostro": Vostro, "future": Future}


def make_frame(t: float) -> np.ndarray:
    scenes = engine.SCENES
    idx = max(i for i, s in enumerate(scenes) if t >= s["start"] or i == 0)
    surf = cs.compose(idx, t - scenes[idx]["start"], SPEC)
    surf.flush()
    buf = np.ndarray((H, W, 4), dtype=np.uint8, buffer=surf.get_data())
    return buf[:, :, 2::-1].copy()


def main() -> None:
    story = importlib.import_module("generate_rupee_short")  # a named module, so work files land in work/<name>/
    engine.make_frame = story.make_frame
    final = engine.render(story, "edge")
    cs.write_alignment(final, SPEC)


if __name__ == "__main__":
    main()
