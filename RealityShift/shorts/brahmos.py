"""Reality Shift Short — BrahMos: ~1 km every second, and why that leaves a ship ~30 s to react (~40s).

Usage:
  python make.py brahmos

New "speed file" layout (not the naval-brief map, defence-lab blueprint or intel file): night sea with speed
streaks, a T+ mission clock and scene pips top-right, captions on a dark slab that slides in from the left in the
1150-1250 band, speed-streak wipes between scenes, bottom 400px clean. Ends with the missile itself flying to the
comment button over an export board (Philippines, Indonesia, ?); no subscribe badge / bell / cursor.
Facts (as commonly reported): BrahMos (India's DRDO + Russia's NPOM) cruises at ~Mach 2.8, upgraded variants
~Mach 3, i.e. ~0.95-1.0 km/s near sea level; an AK-47 bullet leaves the muzzle at ~715 m/s; Delhi-Agra is ~180 km
straight-line (~3 min at that speed); it flies sea-skimming in the terminal phase. Radar horizon estimate: a mast
radar ~20 m up sees a ~10 m-high target at ~4.12 x (sqrt 20 + sqrt 10) ~ 31 km -> ~30 s warning (an estimate, said
as "lagbhag"). Philippines was the first export customer (2022 deal, deliveries from 2024); Indonesia announced a
BrahMos agreement in March 2026; in Nov 2026 the Philippines said it is eyeing more.
"""

import importlib
import json
import math

import cairo
import numpy as np

from core import engine
from core.engine import *  # noqa: F401,F403
from shorts.chabahar import Cued
from shorts.rupee import VOICE_TONES
from shorts.reality_shift import GOLD, INDIA_GREEN, SAFFRON, stamp

TOPIC = "BRAHMOS 1 KM PER SECOND"
OUTPUTS = {"edge": "brahmos_short.mp4"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.3
TAIL_PAD = 0.3
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 122
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"

RED = hexc("#FF3B3B")
CYAN = hexc("#3FE0FF")
STEEL = hexc("#9AA8B6")
FLAME = hexc("#FF9A2E")
NIGHT_TOP, NIGHT_BOT = hexc("#050B1A"), hexc("#0B2236")
SEA_TOP, SEA_BOT = hexc("#06263A"), hexc("#020C16")
MONO = "Consolas"

# each line: (tone, [(spoken Hindi, Hinglish caption), ...], pause after)
SPEC = [
    {"key": "sec", "accent": GOLD, "text": "1 SEC = 1 KM",
     "visual": "Stopwatch loops 0 -> 1.00 s while BrahMos crosses a 1 KM ruler; close-up of the missile; "
               "race lanes: AK-47 bullet (~715 m/s) vs BrahMos (~950 m/s), the missile pulls ahead",
     "vo": [("hook", [("एक सेकंड...", "EK SECOND...")], 0.25),
            ("punch", [("एक किलोमीटर!", "EK KILOMETRE!")], 0.35),
            ("tell", [("ब्रह्मोस की रफ़्तार", "BRAHMOS KI RAFTAAR"), ("इतनी है कि", "ITNI HAI KI")], 0.1),
            ("punch", [("एके-सैंतालीस की गोली", "AK-47 KI GOLI"), ("भी पीछे छूट जाए।", "BHI PEECHE CHHOOT JAAYE!")], 0)]},
    {"key": "mach", "accent": CYAN, "text": "MACH 3",
     "visual": "Speed gauge needle sweeps past the AWAAZ (Mach 1) mark to MACH 3; then Delhi -> Agra, ~180 KM, "
               "the missile crosses it while a clock runs to ~3 MIN",
     "vo": [("tell", [("ये है लगभग", "YEH HAI LAGBHAG"), ("मैक थ्री,", "MACH 3,")], 0.15),
            ("build", [("आवाज़ से तीन गुना तेज़।", "AWAAZ SE TEEN GUNA TEZ!")], 0.3),
            ("low", [("दिल्ली से आगरा?", "DELHI SE AGRA?")], 0.2),
            ("punch", [("सिर्फ़ तीन मिनट!", "SIRF 3 MINUTE!")], 0)]},
    {"key": "radar", "accent": RED, "text": "~30 SEC",
     "visual": "Earth-curve cross-section: a ship's radar beam grazes the horizon, BrahMos skims the waves inside the "
               "red RADAR SHADOW, is DETECTED at ~30 KM, a 30 -> 0 countdown runs to impact",
     "vo": [("low", [("पर असली ख़ौफ़ ये है,", "PAR ASLI KHAUF YEH HAI,")], 0.2),
            ("tell", [("ये लहरों के", "YEH LEHRON KE"), ("ठीक ऊपर उड़ती है,", "THEEK UPAR UDTI HAI,")], 0.15),
            ("tell", [("तो दुश्मन का रडार", "TOH DUSHMAN KA RADAR"), ("इसे बहुत देर से देखता है।", "ISE BAHUT DER SE DEKHTA HAI.")],
             0.3),
            ("punch", [("बचने के लिए लगभग", "BACHNE KE LIYE LAGBHAG"), ("सिर्फ़ तीस सेकंड!", "SIRF 30 SECOND!")], 0)]},
    {"key": "buyer", "accent": INDIA_GREEN, "text": "AGLA KHAREEDAR?",
     "visual": "Export board: PHILIPPINES DEAL, INDONESIA DEAL, then a pulsing ? row; the missile loops out and "
               "flies to the comment button",
     "vo": [("tell", [("इसीलिए फ़िलीपींस के बाद", "ISILIYE PHILIPPINES KE BAAD"), ("अब इंडोनेशिया ने भी", "AB INDONESIA NE BHI"),
                      ("ब्रह्मोस की डील की है।", "BRAHMOS KI DEAL KI HAI!")], 0.4),
            ("ask", [("आपके हिसाब से", "AAPKE HISAAB SE"), ("अगला ख़रीदार कौन?", "AGLA KHAREEDAR KAUN?")], 0.3),
            ("cta", [("कमेंट में लिखो।", "COMMENT MEIN LIKHO!")], 0)]},
]

DELIVERY = {s["key"]: [(VOICE_TONES[tone], " ".join(hi for hi, _ in chunks), pause) for tone, chunks, pause in s["vo"]]
            for s in SPEC}
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {"EK": GOLD, "SECOND": GOLD, "KILOMETRE": GOLD, "BRAHMOS": SAFFRON, "RAFTAAR": GOLD, "AK-47": RED,
       "GOLI": RED, "PEECHE": GOLD, "MACH": CYAN, "3": CYAN, "AWAAZ": CYAN, "TEEN": CYAN, "TEZ": GOLD,
       "DELHI": SAFFRON, "AGRA": SAFFRON, "MINUTE": GOLD, "KHAUF": RED, "LEHRON": CYAN, "DUSHMAN": RED,
       "RADAR": RED, "DER": RED, "30": RED, "PHILIPPINES": INDIA_GREEN, "INDONESIA": INDIA_GREEN,
       "DEAL": GOLD, "AGLA": GOLD, "KHAREEDAR": GOLD, "KAUN": GOLD, "COMMENT": GOLD}

CAP_TOP, CAP_BOTTOM = 1150, 1250
UI_CLEAR = H - 400
COMMENT_BTN = (1000, 1380)   # roughly where the Shorts comment button sits on the right rail


# ============================================================ drawing kit

def seascape(ctx, t, horizon=980, speed=1.0, stars=True):
    """Night sky + sea with streaks rushing left (the camera rides with the missile)."""
    g = cairo.LinearGradient(0, 0, 0, horizon)
    g.add_color_stop_rgb(0, *NIGHT_TOP)
    g.add_color_stop_rgb(1, *NIGHT_BOT)
    ctx.rectangle(0, 0, W, horizon)
    ctx.set_source(g)
    ctx.fill()
    if stars:
        for i in range(70):
            x = (rnd(i, 1) * W * 1.2 - t * 18 * speed) % W
            y = rnd(i, 2) * (horizon - 120)
            circle(ctx, x, y, 1 + 1.6 * rnd(i, 3), (1, 1, 1), 0.25 + 0.35 * rnd(i, 4))
    g = cairo.LinearGradient(0, horizon, 0, H)
    g.add_color_stop_rgb(0, *SEA_TOP)
    g.add_color_stop_rgb(1, *SEA_BOT)
    ctx.rectangle(0, horizon, W, H - horizon)
    ctx.set_source(g)
    ctx.fill()
    line(ctx, [(0, horizon), (W, horizon)], CYAN, 2, 0.35)
    for i in range(46):   # wave dashes, faster near the viewer
        depth = rnd(i, 5)
        y = horizon + 12 + depth * (H - horizon - 40)
        v = (300 + 1400 * depth) * speed
        x = (rnd(i, 6) * W * 1.5 - t * v) % (W + 300) - 150
        line(ctx, [(x, y), (x + 40 + 140 * depth, y)], CYAN, 1.5 + 3 * depth, 0.12 + 0.2 * depth)
    for i in range(18):   # speed streaks in the sky
        y = 220 + rnd(i, 7) * (horizon - 300)
        x = (rnd(i, 8) * W * 2 - t * 2600 * speed) % (W + 900) - 450
        line(ctx, [(x, y), (x + 260 + 200 * rnd(i, 9), y)], (1, 1, 1), 2, 0.08 + 0.1 * rnd(i, 10))


def missile(ctx, x, y, s, t, ang=0.0, flame=1.0, a=1.0, outline=None):
    """Side view: ogive nose, long body, saffron band, mid wings, tail fins, ramjet flame with shock diamonds."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(s, s)
    if flame > 0:
        fl = 1 + 0.12 * math.sin(t * 47) + 0.08 * math.sin(t * 31)
        glow(ctx, -175, 0, 120 * flame, FLAME, 0.45 * a)
        ctx.move_to(-160, -13)
        ctx.line_to(-160 - 150 * flame * fl, 0)
        ctx.line_to(-160, 13)
        ctx.close_path()
        rgba(ctx, FLAME, 0.85 * a)
        ctx.fill()
        for k in range(3):   # shock diamonds
            cx = -190 - k * 38 * flame
            ctx.move_to(cx + 12, 0)
            ctx.line_to(cx, -6)
            ctx.line_to(cx - 12, 0)
            ctx.line_to(cx, 6)
            ctx.close_path()
            rgba(ctx, (1, 0.95, 0.8), 0.85 * a * flame)
            ctx.fill()
    for sgn in (-1, 1):   # tail fins and mid wings
        ctx.move_to(-158, sgn * 14)
        ctx.line_to(-150, sgn * 52)
        ctx.line_to(-128, sgn * 52)
        ctx.line_to(-112, sgn * 14)
        ctx.close_path()
        rgba(ctx, shade(STEEL, 0.75), a)
        ctx.fill()
        ctx.move_to(-20, sgn * 14)
        ctx.line_to(4, sgn * 36)
        ctx.line_to(24, sgn * 36)
        ctx.line_to(30, sgn * 14)
        ctx.close_path()
        rgba(ctx, shade(STEEL, 0.85), a)
        ctx.fill()
    ctx.move_to(-162, -16)
    ctx.line_to(92, -16)
    ctx.curve_to(132, -16, 160, -8, 178, 0)
    ctx.curve_to(160, 8, 132, 16, 92, 16)
    ctx.line_to(-162, 16)
    ctx.close_path()
    g = cairo.LinearGradient(0, -16, 0, 16)
    g.add_color_stop_rgba(0, 0.93, 0.95, 0.97, a)
    g.add_color_stop_rgba(0.45, 0.78, 0.82, 0.86, a)
    g.add_color_stop_rgba(1, 0.42, 0.46, 0.52, a)
    ctx.set_source(g)
    ctx.fill_preserve()
    rgba(ctx, outline or (0.1, 0.12, 0.15), a)
    ctx.set_line_width(4 if outline else 2.5)
    ctx.stroke()
    ctx.rectangle(-70, -16, 16, 32)
    rgba(ctx, SAFFRON, a)
    ctx.fill()
    ctx.rectangle(-54, -16, 6, 32)
    rgba(ctx, INDIA_GREEN, a)
    ctx.fill()
    line(ctx, [(96, -14), (96, 14)], (0.2, 0.22, 0.25), 2, a)
    ctx.restore()


def bullet(ctx, x, y, s, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for k in range(5):
        line(ctx, [(-30 - k * 26, 0), (-46 - k * 26, 0)], (1, 1, 1), 4 - 0.6 * k, (0.5 - 0.09 * k) * a)
    ctx.move_to(-24, -7)
    ctx.line_to(6, -7)
    ctx.curve_to(18, -7, 26, -3, 30, 0)
    ctx.curve_to(26, 3, 18, 7, 6, 7)
    ctx.line_to(-24, 7)
    ctx.close_path()
    rgba(ctx, hexc("#D9A441"), a)
    ctx.fill()
    ctx.restore()


def chip(ctx, s, x, y, c, u, size=38, sub=None, anchor="c"):
    """Pill that pops in; anchor l/c/r on x."""
    if u <= 0:
        return
    k = ease_out_back(u / 0.3)
    w = max(text_width(ctx, s, size, font=MONO), text_width(ctx, sub, size * 0.62, font=MONO) if sub else 0) + 56
    h = size * (2.15 if sub else 1.5)
    cx = x + w / 2 if anchor == "l" else (x - w / 2 if anchor == "r" else x)
    ctx.save()
    ctx.translate(cx, y)
    ctx.scale(k, k)
    rrect(ctx, -w / 2, -h / 2, w, h, 14)
    rgba(ctx, (0.01, 0.03, 0.06), 0.9)
    ctx.fill_preserve()
    rgba(ctx, c)
    ctx.set_line_width(3)
    ctx.stroke()
    text(ctx, s, 0, -size * 0.4 if sub else 0, size, (1, 1, 1), font=MONO)
    if sub:
        text(ctx, sub, 0, size * 0.55, size * 0.62, c, font=MONO)
    ctx.restore()


def big_readout(ctx, s, x, y, size, c, a=1.0):
    text(ctx, s, x, y, size, c, font=CAPTION_FONT, bold=False, a=a, stroke=(0, 0, 0), stroke_w=size * 0.09)


def tick_mark(ctx, x, y, s, c, u):
    if u <= 0:
        return
    k = ease_out_cubic(u / 0.3)
    pts = [(x - 22 * s, y), (x - 6 * s, y + 16 * s), (x + 24 * s, y - 18 * s)]
    if k < 0.5:
        pts = [pts[0], (lerp(pts[0][0], pts[1][0], k * 2), lerp(pts[0][1], pts[1][1], k * 2))]
    else:
        pts = [pts[0], pts[1], (lerp(pts[1][0], pts[2][0], (k - 0.5) * 2), lerp(pts[1][1], pts[2][1], (k - 0.5) * 2))]
    line(ctx, pts, (0, 0, 0), 14 * s, 0.6)
    line(ctx, pts, c, 8 * s)


# ============================================================ scenes

class Sec(Cued):
    """Stopwatch + 1 KM ruler loop, missile close-up, then the bullet-vs-BrahMos race."""

    LOOP = 1.25

    def beats(self, d):
        c = self.cue
        return {"km": c("KILOMETRE", d * 0.15), "brah": c("BRAHMOS", d * 0.35), "ak": c("AK-47", d * 0.6),
                "peeche": c("PEECHE", d * 0.82)}

    def events(self, d):
        b = self.beats(d)
        beeps = [(k * self.LOOP + 1.0, "beep") for k in range(8) if k * self.LOOP + 1.0 < b["brah"]]
        ticks = [(k * 0.1, "tick" if k % 2 else "tock") for k in range(10)]
        return [(0.02, "boom"), (0.04, "whoosh"), (b["km"], "thud"), (b["brah"], "zap"), (b["brah"] + 0.05, "boom"),
                (b["ak"], "pop"), (b["ak"] + 0.08, "whoosh"), (b["peeche"], "thud")] + beeps + ticks

    def draw(self, ctx, t, d):
        b = self.beats(d)
        seascape(ctx, t, 980, 1.0 + 0.6 * (t > b["brah"]))
        fade_a = clamp((b["brah"] - t) / 0.25)
        if fade_a > 0:   # phase A: the 1-second loop
            k = clamp((t % self.LOOP) / 1.0)
            ry = 860
            line(ctx, [(90, ry), (990, ry)], (1, 1, 1), 5, 0.8 * fade_a)
            for i in range(11):
                x = lerp(90, 990, i / 10)
                hgt = 28 if i % 5 == 0 else 14
                line(ctx, [(x, ry), (x, ry + hgt)], (1, 1, 1), 3, 0.8 * fade_a)
            for lbl, i in (("0", 0), ("500 M", 5), ("1 KM", 10)):
                text(ctx, lbl, lerp(90, 990, i / 10), ry + 60, 32, GOLD if i == 10 else (1, 1, 1), font=MONO,
                     a=fade_a)
            line(ctx, [(90, ry - 6), (lerp(90, 990, k), ry - 6)], GOLD, 10, 0.9 * fade_a)
            missile(ctx, lerp(40, 1000, k), ry - 90, 0.8, t, a=fade_a)
            big_readout(ctx, f"{k:.2f} s", 540, 520, 190, (1, 1, 1), fade_a)
            big_readout(ctx, f"{k:.2f} KM", 540, 690, 110, GOLD, fade_a)
            if t < 2.6:   # cold-open hook card
                stamp(ctx, 540, 300, t, -0.03, 760, 170, GOLD, [("1 SEC = 1 KM", 4, 110, GOLD)])
            elif t > b["km"]:
                stamp(ctx, 540, 300, t - b["km"], 0.02, 760, 170, GOLD, [("1 SEC = 1 KM", 4, 110, GOLD)])
        u = t - b["brah"]
        if u > 0 and t < b["ak"]:   # phase B: hero close-up
            k = ease_out_cubic(u / 0.35)
            missile(ctx, lerp(-300, 560, k), 660 + 10 * math.sin(t * 6), 2.4, t, ang=-0.04)
            stamp(ctx, 540, 320, u, -0.02, 780, 190, SAFFRON,
                  [("BRAHMOS", -26, 100, (1, 1, 1)), ("SUPERSONIC CRUISE MISSILE", 52, 34, SAFFRON)])
            chip(ctx, "~1 KM / SEC", 540, 920, GOLD, u - 0.4, size=46)
        u = t - b["ak"]
        if u > 0:   # phase C: the race
            px = 380   # pixels per second at ~950 m/s
            lanes = ((560, "AK-47 GOLI", "~715 M/S", RED, 715), (840, "BRAHMOS", "~950 M/S", GOLD, 950))
            for ly, name, spd, c, v in lanes:
                line(ctx, [(60, ly + 70), (1020, ly + 70)], (1, 1, 1), 2, 0.25)
                ctx.set_dash([10, 14])
                line(ctx, [(60, ly + 70), (1020, ly + 70)], c, 2, 0.5)
                ctx.set_dash([])
                chip(ctx, name, 70, ly - 95, c, u - (0.1 if v == 950 else 0), size=36, sub=spd, anchor="l")
            run = max(0.0, u - 0.25)
            bx = min(80 + px * run * 715 / 950, 900)
            mx = min(140 + px * run, 900)
            bullet(ctx, bx, 560, 2.4)
            missile(ctx, mx, 840, 0.9, t)
            if t > b["peeche"]:
                uu = t - b["peeche"]
                ctx.set_dash([12, 10])
                line(ctx, [(bx + 70, 700), (mx + 160, 700)], GOLD, 4, clamp(uu / 0.2))
                ctx.set_dash([])
                stamp(ctx, 540, 320, uu, 0.03, 700, 160, GOLD, [("GOLI SE TEZ!", 4, 100, GOLD)])


class Mach(Cued):
    """Speed gauge to MACH 3 past the sound mark, then Delhi -> Agra in ~3 minutes."""

    def beats(self, d):
        c = self.cue
        return {"mach": c("MACH 3", d * 0.15), "awaaz": c("AWAAZ", d * 0.3), "delhi": c("DELHI", d * 0.55),
                "min": c("3 MINUTE", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        ticks = [(b["delhi"] + 0.4 + k * 0.08, "tick" if k % 2 else "tock") for k in range(14)]
        return [(0.02, "whoosh"), (b["mach"], "engine", 1.4), (b["mach"] + 0.6, "zap"), (b["awaaz"], "boom"),
                (b["delhi"], "pick"), (b["delhi"] + 0.3, "whoosh"), (b["min"], "kaching"), (b["min"] + 0.05, "thud")] \
            + ticks

    def draw(self, ctx, t, d):
        b = self.beats(d)
        seascape(ctx, t, 1000, 1.6)
        gx, gy, r = 540, 760, 330
        a = clamp((b["delhi"] - t) / 0.15)
        if a > 0:   # speed gauge: 0..3.5 Mach on a 220-degree arc
            a0, a1 = math.radians(160), math.radians(380)
            ctx.arc(gx, gy, r, a0, a1)
            rgba(ctx, (0.01, 0.03, 0.06), 0.85 * a)
            ctx.set_line_width(70)
            ctx.stroke()
            sweep = 3.0 * ease_out_cubic((t - b["mach"] + 0.2) / 0.8) if t > b["mach"] - 0.2 else 0.0
            sweep += 0.03 * math.sin(t * 23) * (sweep > 2.9)
            for m in range(36):
                val = m / 10
                ang = lerp(a0, a1, val / 3.5)
                lit = val <= sweep
                c = RED if val >= 2.8 else (CYAN if val >= 1 else (1, 1, 1))
                ctx.arc(gx, gy, r, ang, ang + (a1 - a0) / 36 * 0.75)
                rgba(ctx, c, (0.9 if lit else 0.15) * a)
                ctx.set_line_width(46)
                ctx.stroke()
            for m in range(4):
                ang = lerp(a0, a1, m / 3.5)
                text(ctx, str(m), gx + (r - 95) * math.cos(ang), gy + (r - 95) * math.sin(ang), 48, (1, 1, 1),
                     font=CAPTION_FONT, bold=False, a=a)
            ang = lerp(a0, a1, sweep / 3.5)
            line(ctx, [(gx, gy), (gx + (r - 30) * math.cos(ang), gy + (r - 30) * math.sin(ang))], (0, 0, 0), 16, 0.6 * a)
            line(ctx, [(gx, gy), (gx + (r - 30) * math.cos(ang), gy + (r - 30) * math.sin(ang))], GOLD, 9, a)
            circle(ctx, gx, gy, 22, GOLD, a)
            big_readout(ctx, f"MACH {sweep:.1f}", gx, gy + 120, 120, (1, 1, 1), a)
            text(ctx, "~1 KM / SEC", gx, gy + 215, 40, GOLD, font=MONO, a=a)
            u = t - b["awaaz"]
            if u > 0:   # the sound barrier mark, and 3x it
                ang = lerp(a0, a1, 1 / 3.5)
                px, py = gx + (r + 70) * math.cos(ang), gy + (r + 70) * math.sin(ang)
                chip(ctx, "AWAAZ = MACH 1", px + 40, py - 40, CYAN, u, size=32, anchor="l")
                stamp(ctx, 540, 300, u, -0.03, 640, 170, CYAN, [("3X AWAAZ", 4, 110, CYAN)])
        u = t - b["delhi"]
        if u > 0:   # Delhi -> Agra schematic
            k = clamp(u / 0.3)
            d0, d1 = (300, 470), (760, 920)
            ctx.rectangle(0, 200, W, 900)
            rgba(ctx, (0.01, 0.04, 0.07), 0.85 * k)
            ctx.fill()
            ctx.set_dash([16, 12])
            line(ctx, [d0, d1], (1, 1, 1), 4, 0.5 * k)
            ctx.set_dash([])
            for (x, y), name in ((d0, "DELHI"), (d1, "AGRA")):
                pulse = (t * 1.2) % 1
                ctx.arc(x, y, 18 + 60 * pulse, 0, math.tau)
                rgba(ctx, SAFFRON, 0.7 * (1 - pulse) * k)
                ctx.set_line_width(3)
                ctx.stroke()
                circle(ctx, x, y, 14, SAFFRON, k)
                text(ctx, name, x + (-40 if name == "DELHI" else 40), y + (-50 if name == "DELHI" else 50), 54,
                     (1, 1, 1), font=CAPTION_FONT, bold=False, a=k, anchor="r" if name == "DELHI" else "l",
                     stroke=(0, 0, 0), stroke_w=6)
            chip(ctx, "~180 KM", 690, 590, SAFFRON, u - 0.2, size=40)
            f = ease_in_out((u - 0.35) / max(0.4, b["min"] - b["delhi"] - 0.25))
            mx, my = lerp(d0[0], d1[0], f), lerp(d0[1], d1[1], f)
            ang = math.atan2(d1[1] - d0[1], d1[0] - d0[0])
            if 0 < f:
                line(ctx, [d0, (mx, my)], GOLD, 8, 0.9)
                missile(ctx, mx, my, 0.55, t, ang=ang, flame=1.0 if f < 1 else 0.0, a=1.0 if f < 1 else 0.0)
            secs = round(180 * f)
            big_readout(ctx, f"{secs // 60}:{secs % 60:02d}", 270, 820, 130, GOLD if f >= 1 else (1, 1, 1))
            text(ctx, "MIN", 270, 915, 34, GOLD, font=MONO)
            if t > b["min"]:
                ctx.arc(d1[0], d1[1], 60 + 200 * ease_out_cubic((t - b["min"]) / 0.5), 0, math.tau)
                rgba(ctx, GOLD, 0.8 * (1 - clamp((t - b["min"]) / 0.5)))
                ctx.set_line_width(8)
                ctx.stroke()
                stamp(ctx, 540, 300, t - b["min"], 0.03, 600, 170, GOLD, [("~3 MIN!", 4, 120, GOLD)])


# Earth-curve cross-section for the radar scene (curvature exaggerated, not to scale)
R_EARTH = 700
APEX_Y = 820
C_EARTH = (540, APEX_Y + R_EARTH)
SHIP_TH = math.asin((820 - 540) / R_EARTH)
MAST = 200
MISSILE_ALT = 50
ALPHA = math.acos(R_EARTH / (R_EARTH + MAST))
TANGENT_TH = SHIP_TH - ALPHA                                                 # the beam grazes the sea here
DETECT_TH = TANGENT_TH - math.acos(R_EARTH / (R_EARTH + MISSILE_ALT))        # first point the beam can see
START_TH = -0.95


def on_earth(th, alt=0.0):
    r = R_EARTH + alt
    return C_EARTH[0] + r * math.sin(th), C_EARTH[1] - r * math.cos(th)


class Radar(Cued):
    """Ship + radar beam over the curve, missile skims inside the radar shadow, DETECTED at ~30 KM, countdown."""

    def beats(self, d):
        c = self.cue
        return {"lehron": c("LEHRON", d * 0.18), "radar": c("RADAR", d * 0.42), "der": c("DER SE", d * 0.58),
                "bach": c("BACHNE", d * 0.72), "sec": c("30 SECOND", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        n = int((d - b["bach"]) / 0.12)
        ticks = [(b["bach"] + k * 0.12, "tick" if k % 2 else "tock") for k in range(max(0, n))]
        return [(0.02, "thud"), (0.1, "alarm"), (b["lehron"], "whoosh"), (b["radar"], "beep"), (b["radar"] + 0.3, "beep"),
                (b["der"], "alarm"), (b["der"] + 0.05, "zap"), (b["sec"], "boom"), (d - 0.25, "boom")] + ticks

    def theta(self, t, b, d):
        if t < b["lehron"]:
            return None
        if t < b["der"]:
            return lerp(START_TH, DETECT_TH, ease_in_out((t - b["lehron"]) / (b["der"] - b["lehron"])) ** 0.9)
        return lerp(DETECT_TH, SHIP_TH - 0.02, clamp((t - b["der"]) / max(0.5, d - 0.3 - b["der"])))

    def draw(self, ctx, t, d):
        b = self.beats(d)
        g = cairo.LinearGradient(0, 0, 0, APEX_Y)
        g.add_color_stop_rgb(0, *NIGHT_TOP)
        g.add_color_stop_rgb(1, *NIGHT_BOT)
        ctx.rectangle(0, 0, W, H)
        ctx.set_source(g)
        ctx.fill()
        for i in range(60):
            circle(ctx, rnd(i, 1) * W, 200 + rnd(i, 2) * 500, 1 + 1.5 * rnd(i, 3), (1, 1, 1), 0.3 * rnd(i, 4) + 0.1)
        ctx.arc(*C_EARTH, R_EARTH, 0, math.tau)   # the sea, as a curved Earth
        g = cairo.LinearGradient(0, APEX_Y, 0, APEX_Y + 500)
        g.add_color_stop_rgb(0, *hexc("#0E4866"))
        g.add_color_stop_rgb(1, *SEA_BOT)
        ctx.set_source(g)
        ctx.fill()
        ctx.arc(*C_EARTH, R_EARTH, 0, math.tau)
        rgba(ctx, CYAN, 0.6)
        ctx.set_line_width(3)
        ctx.stroke()
        mast = on_earth(SHIP_TH, MAST)
        tan = on_earth(TANGENT_TH)
        far_dir = (tan[0] - mast[0], tan[1] - mast[1])
        n = math.hypot(*far_dir)
        far = (mast[0] + far_dir[0] / n * 1600, mast[1] + far_dir[1] / n * 1600)
        # radar shadow: below the grazing beam, beyond the horizon point
        ctx.move_to(*tan)
        ctx.line_to(*far)
        for k in range(30):
            ctx.line_to(*on_earth(lerp(START_TH - 0.2, TANGENT_TH, k / 29)))
        ctx.close_path()
        sh = clamp((t - b["radar"]) / 0.4)
        rgba(ctx, RED, (0.1 + 0.06 * math.sin(t * 5)) * sh)
        ctx.fill()
        if sh > 0:
            sx = 215
            beam_y = lerp(mast[1], far[1], (mast[0] - sx) / (mast[0] - far[0]))
            surf_y = C_EARTH[1] - math.sqrt(R_EARTH ** 2 - (sx - C_EARTH[0]) ** 2)
            text(ctx, "RADAR", sx, (beam_y + surf_y) / 2 - 22, 34, RED, font=MONO, a=sh, stroke=(0, 0, 0), stroke_w=5)
            text(ctx, "SHADOW", sx, (beam_y + surf_y) / 2 + 18, 34, RED, font=MONO, a=sh, stroke=(0, 0, 0), stroke_w=5)
        # beam: grazing line + pulses travelling out
        line(ctx, [mast, far], CYAN, 14, 0.15)
        line(ctx, [mast, far], CYAN, 3, 0.85)
        for k in range(4):
            f = (t * 0.9 + k / 4) % 1
            circle(ctx, lerp(mast[0], far[0], f * 0.6), lerp(mast[1], far[1], f * 0.6), 7, CYAN, 0.9 * (1 - f))
        # the ship
        ctx.save()
        ctx.translate(*on_earth(SHIP_TH))
        ctx.rotate(SHIP_TH)
        ctx.scale(1.3, 1.3)
        ctx.move_to(-110, -6)
        ctx.line_to(110, -6)
        ctx.line_to(90, 22)
        ctx.line_to(-96, 22)
        ctx.close_path()
        rgba(ctx, STEEL)
        ctx.fill()
        rrect(ctx, -60, -40, 80, 36, 4)
        rgba(ctx, shade(STEEL, 1.15))
        ctx.fill()
        line(ctx, [(-20, -40), (-20, -MAST / 1.3)], STEEL, 6)
        line(ctx, [(-40, -MAST / 1.3 + 18), (0, -MAST / 1.3 + 18)], STEEL, 5)
        ctx.restore()
        ping_r = (t * 1.4) % 1
        ctx.arc(*mast, 10 + 70 * ping_r, 0, math.tau)
        rgba(ctx, CYAN, 0.8 * (1 - ping_r))
        ctx.set_line_width(3)
        ctx.stroke()
        circle(ctx, *mast, 8, CYAN)
        if t < b["lehron"]:
            stamp(ctx, 540, 320, t, -0.02, 620, 170, RED, [("ASLI KHAUF", 4, 110, RED)])
        th = self.theta(t, b, d)
        if th is not None:
            mx, my = on_earth(th, MISSILE_ALT)
            seen = t > b["der"]
            for q in range(1, 8):   # wake on the waves
                wx, wy = on_earth(th - q * 0.02, MISSILE_ALT * 0.25)
                circle(ctx, wx, wy, 6 - 0.6 * q, (1, 1, 1), 0.3 - 0.035 * q)
            missile(ctx, mx, my, 0.55, t, ang=th, outline=RED if seen else None)
            if not seen:
                chip(ctx, "SEA-SKIMMING", max(200, mx + 30), my - 130, CYAN, t - b["lehron"] - 0.2, size=32)
        u = t - b["der"]
        if u > 0:
            dx, dy = on_earth(DETECT_TH, MISSILE_ALT)
            ctx.arc(dx, dy, 30 + 220 * ease_out_cubic(u / 0.5), 0, math.tau)
            rgba(ctx, RED, 0.9 * (1 - clamp(u / 0.5)))
            ctx.set_line_width(8)
            ctx.stroke()
            line(ctx, [mast, (dx, dy)], RED, 3, 0.7)
            for k in range(25):   # distance along the sea, detection point -> ship
                p = on_earth(lerp(DETECT_TH, SHIP_TH, k / 24), -26)
                if k % 2 == 0 and k < 24:
                    q = on_earth(lerp(DETECT_TH, SHIP_TH, (k + 1) / 24), -26)
                    line(ctx, [p, q], GOLD, 5, clamp(u / 0.3))
            chip(ctx, "~30 KM", *on_earth((DETECT_TH + SHIP_TH) / 2, -95), GOLD, u - 0.2, size=40)
            if t < b["bach"]:
                stamp(ctx, 540, 320, u, 0.03, 620, 170, RED, [("DETECTED!", 4, 110, RED)])
        u = t - b["bach"]
        if u > 0:   # countdown to impact
            left = 30 * (1 - clamp(u / max(0.5, d - 0.3 - b["bach"])))
            big_readout(ctx, f"00:{math.ceil(left):02d}", 540, 330, 170, RED if left < 10 else (1, 1, 1))
            text(ctx, "BACHNE KA TIME", 540, 450, 38, RED, font=MONO, stroke=(0, 0, 0), stroke_w=5)
        u = t - (d - 0.3)
        if u > 0:
            sx, sy = on_earth(SHIP_TH, 40)
            glow(ctx, sx, sy, 260, FLAME, 0.9 * (1 - clamp(u / 0.4)))
            glow(ctx, sx, sy, 120, (1, 1, 0.9), 1 - clamp(u / 0.3))


class Buyer(Cued):
    """Export board (Philippines, Indonesia, ?) and the missile flying to the comment button."""

    def beats(self, d):
        c = self.cue
        return {"ph": c("PHILIPPINES", 0.05), "id": c("INDONESIA", d * 0.18), "deal": c("DEAL", d * 0.32),
                "agla": c("AGLA", d * 0.6), "cmt": c("COMMENT", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "whoosh"), (b["ph"] + 0.1, "pop"), (b["id"], "pop"), (b["deal"], "kaching"),
                (b["agla"], "dingdong"), (b["cmt"] - 0.3, "whoosh"), (b["cmt"] + 0.35, "boom")]

    def row(self, ctx, y, code, name, status, c, u, t, done):
        if u <= 0:
            return
        k = ease_out_cubic(u / 0.35)
        ctx.save()
        ctx.translate(lerp(-900, 0, k), 0)
        rrect(ctx, 80, y - 75, 920, 150, 24)
        rgba(ctx, (0.01, 0.04, 0.07), 0.92)
        ctx.fill_preserve()
        rgba(ctx, c, 0.9)
        ctx.set_line_width(4)
        ctx.stroke()
        circle(ctx, 170, y, 50, c, 0.9)
        text(ctx, code, 170, y, 48, (0.03, 0.05, 0.08), font=CAPTION_FONT, bold=False)
        text(ctx, name, 250, y, 66, (1, 1, 1), font=CAPTION_FONT, bold=False, anchor="l")
        if status:
            text(ctx, status, 880, y, 40, c, font=MONO, anchor="r")
            tick_mark(ctx, 935, y, 1.3, c, done)
        ctx.restore()

    def draw(self, ctx, t, d):
        b = self.beats(d)
        seascape(ctx, t, 1050, 0.6)
        text(ctx, "BRAHMOS EXPORT BOARD", 540, 290, 46, GOLD, font=MONO, stroke=(0, 0, 0), stroke_w=6)
        self.row(ctx, 430, "PH", "PHILIPPINES", "DEAL", INDIA_GREEN, t - b["ph"], t, t - b["ph"] - 0.3)
        self.row(ctx, 610, "ID", "INDONESIA", "DEAL", INDIA_GREEN, t - b["id"], t, t - b["deal"])
        u = t - b["agla"]
        if u > 0:
            pulse = 0.5 + 0.5 * math.sin(t * 6)
            glow(ctx, 540, 790, 420, GOLD, 0.15 + 0.15 * pulse)
            self.row(ctx, 790, "?", "AGLA KAUN?", "", GOLD, u, t, 0)
        u = t - b["cmt"] + 0.35
        if u > 0:   # the missile loops out of the board and dives onto the comment button
            k = ease_in_out(u / 0.7)
            p0, p1, p2 = (120, 980), (760, 760), COMMENT_BTN
            pts = [(lerp(lerp(p0[0], p1[0], s), lerp(p1[0], p2[0], s), s),
                    lerp(lerp(p0[1], p1[1], s), lerp(p1[1], p2[1], s), s)) for s in np.linspace(0, k, 30)]
            if k < 1:
                line(ctx, pts, (1, 1, 1), 6, 0.35)
                (ax, ay), (bx, by) = pts[-2], pts[-1]
                missile(ctx, bx, by, 0.5, t, ang=math.atan2(by - ay, bx - ax))
            else:
                v = u - 0.7
                for q in range(3):
                    r = ((v * 0.9 + q / 3) % 1)
                    ctx.arc(*COMMENT_BTN, 30 + 150 * r, 0, math.tau)
                    rgba(ctx, GOLD, 0.9 * (1 - r))
                    ctx.set_line_width(6)
                    ctx.stroke()
                glow(ctx, *COMMENT_BTN, 130, GOLD, 0.5)
            pop = ease_out_back(u / 0.35)
            ctx.save()
            ctx.translate(500, 1000)
            ctx.scale(pop, pop)
            rrect(ctx, -260, -50, 520, 100, 50)
            rgba(ctx, GOLD)
            ctx.fill()
            text(ctx, "NAAM COMMENT KARO", 0, 2, 50, (0.05, 0.05, 0.05), font=CAPTION_FONT, bold=False)
            ctx.restore()


SCENE_CLASSES = {"sec": Sec, "mach": Mach, "radar": Radar, "buyer": Buyer}


# ============================================================ compositor ("speed file")

def header(ctx, idx, t_global):
    ex, ey = 84, 102
    ctx.save()   # chevron emblem
    ctx.translate(ex, ey)
    for k in range(2):
        ctx.move_to(-18 + k * 18, -20)
        ctx.line_to(2 + k * 18, 0)
        ctx.line_to(-18 + k * 18, 20)
        rgba(ctx, GOLD if k else SAFFRON)
        ctx.set_line_width(7)
        ctx.stroke()
    ctx.restore()
    text(ctx, "REALITY SHIFT", 128, 90, 34, (1, 1, 1), a=0.92, anchor="l")
    text(ctx, "SPEED FILE // BRAHMOS", 128, 124, 22, GOLD, font=MONO, a=0.85, anchor="l")
    text(ctx, f"T+ {t_global:05.1f}s", W - 60, 92, 32, (1, 1, 1), font=MONO, a=0.9, anchor="r")
    for i in range(len(SPEC)):
        x = W - 60 - (len(SPEC) - 1 - i) * 34 - 10
        ctx.rectangle(x - 10, 116, 20, 12)
        rgba(ctx, SPEC[i]["accent"] if i <= idx else (1, 1, 1), 1.0 if i <= idx else 0.2)
        ctx.fill()


def caption(ctx, sc, tl, accent):
    """Slab caption: the current Hinglish chunk slides in from the left on a dark bar with an accent edge."""
    cur = None
    for i, (start, _) in enumerate(sc["captions"]):
        if tl >= start - 0.03:
            cur = i
    if cur is None:
        return
    start, cap = sc["captions"][cur]
    u = tl - start + 0.03
    k = ease_out_cubic(clamp(u / 0.16))
    size = 82
    words_ = cap.split(" ")
    ws = [text_width(ctx, w, size, font=CAPTION_FONT, bold=False) for w in words_]
    gap = size * 0.26
    tw = sum(ws) + gap * (len(ws) - 1)
    fit = min(1.0, 900 / tw)
    cy = (CAP_TOP + CAP_BOTTOM) / 2
    ctx.save()
    ctx.translate(W / 2 - 70 * (1 - k), cy)
    ctx.scale(fit, fit)
    pad = 44
    rrect(ctx, -tw / 2 - pad, -size * 0.72, tw + 2 * pad, size * 1.44, 14)
    rgba(ctx, (0.0, 0.02, 0.05), 0.82 * k)
    ctx.fill()
    ctx.rectangle(-tw / 2 - pad, -size * 0.72, 12, size * 1.44)
    rgba(ctx, accent, k)
    ctx.fill()
    x = -tw / 2
    for w, ww in zip(words_, ws):
        c = HOT.get(w.strip(PUNCT + "."), (1, 1, 1))
        text(ctx, w, x, 0, size, c, font=CAPTION_FONT, bold=False, a=k, anchor="l", stroke=(0, 0, 0), stroke_w=8)
        x += ww + gap
    ctx.restore()


def streak_wipe(ctx, tl, accent):
    """Speed-streak wipe: dark bands of the old frame race off to the right, staggered."""
    if tl >= 0.45:
        return
    bands = 14
    bh = H / bands
    for i in range(bands):
        k = ease_out_cubic((tl - 0.012 * ((i * 5) % bands)) / 0.3)
        if k >= 1:
            continue
        x0 = W * k
        ctx.rectangle(x0, i * bh, W - x0 + 2, bh + 1)
        rgba(ctx, (0.0, 0.01, 0.03))
        ctx.fill()
        line(ctx, [(x0, i * bh + bh * 0.5), (x0 - 160 * (1 - k), i * bh + bh * 0.5)], accent, 6, 0.9 * (1 - k))


def compose(idx, tl):
    sc = engine.SCENES[idx]
    spec = SPEC[idx]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    shake = 6 * max(0.0, 1 - tl / 0.25)   # a jolt on every cut
    ctx.save()
    ctx.translate(shake * math.sin(tl * 90), shake * math.cos(tl * 70))
    sc["obj"].draw(ctx, tl, sc["dur"])
    ctx.restore()
    vignette(ctx)
    g = cairo.LinearGradient(0, 0, 0, 200)  # header plate
    g.add_color_stop_rgba(0, 0.0, 0.01, 0.03, 0.9)
    g.add_color_stop_rgba(1, 0.0, 0.01, 0.03, 0.0)
    ctx.rectangle(0, 0, W, 200)
    ctx.set_source(g)
    ctx.fill()
    g = cairo.LinearGradient(0, CAP_TOP - 60, 0, UI_CLEAR)  # fade into the clean bottom 400px
    g.add_color_stop_rgba(0, 0.0, 0.01, 0.03, 0.0)
    g.add_color_stop_rgba(1, 0.0, 0.01, 0.03, 0.9)
    ctx.rectangle(0, CAP_TOP - 60, W, UI_CLEAR - CAP_TOP + 60)
    ctx.set_source(g)
    ctx.fill()
    ctx.rectangle(0, UI_CLEAR, W, H - UI_CLEAR)
    rgba(ctx, (0.0, 0.01, 0.03), 0.9)
    ctx.fill()
    header(ctx, idx, sc["start"] + tl)
    caption(ctx, sc, tl, spec["accent"])
    if idx:
        streak_wipe(ctx, tl, spec["accent"])
    return surf


def make_frame(t: float) -> np.ndarray:
    scenes = engine.SCENES
    idx = max(i for i, s in enumerate(scenes) if t >= s["start"] or i == 0)
    surf = compose(idx, t - scenes[idx]["start"])
    surf.flush()
    buf = np.ndarray((H, W, 4), dtype=np.uint8, buffer=surf.get_data())
    return buf[:, :, 2::-1].copy()


def write_alignment(final):
    out = [{"scene": spec["key"], "start": round(s["start"], 3), "end": round(s["start"] + s["dur"], 3),
            "voiceover": NARRATION[spec["key"]], "on_screen_text": spec["text"], "visual": spec["visual"],
            "words": [{"t": round(s["start"] + st, 3), "w": w} for st, w in s["captions"]]}
           for spec, s in zip(SPEC, engine.SCENES)]
    path = final.with_suffix(".json")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Alignment: {path}")


# ============================================================ upload kit (see upload_kit.py)

UPLOAD = {
    "titles": [
        "1 Second Me 1 KM! BrahMos Ka Mach 3 Khauf! 🇮🇳",
        "1 Second Me 1 KM! BrahMos Se Bachne Ko Sirf ~30 Sec 🇮🇳",
        "BrahMos Speed: AK-47 Ki Goli Se Bhi Tez!",
        "BrahMos: Delhi Se Agra Sirf 3 Minute Me!",
        "BrahMos Ko Radar Itni Der Se Kyun Dekhta Hai?",
        "Mach 3 BrahMos: Dushman Ke Paas Sirf 30 Second",
        "BrahMos Missile Kitni Tez Hai? 1 KM Per Second",
        "Philippines Ke Baad Indonesia: BrahMos Ka Agla Khareedar?",
        "BrahMos Ki Speed Ka Asli Matlab, 40 Second Me",
        "Sea-Skimming BrahMos: Radar Ka Sabse Bada Dar",
    ],
    "thumb_text": "1 KM/SEC!",
    "queries": ["brahmos speed", "brahmos missile", "mach 3"],
    "description": """
BrahMos missile ki speed: lagbhag Mach 2.8 se Mach 3, yaani har second qareeb 1 KM.
AK-47 ki goli se tez, Delhi se Agra lagbhag 3 minute, aur samandar ki lehron ke upar udne se dushman ke radar ko bahut der se dikhti hai.

Is Short me:
• BrahMos: Bharat (DRDO) aur Russia (NPOM) ki supersonic cruise missile, ~Mach 2.8 (naye version ~Mach 3)
• ~950 m/s vs AK-47 ki goli ~715 m/s (muzzle velocity)
• Delhi-Agra ~180 KM seedhi doori: ~3 minute
• Sea-skimming: ~20 m oonchi radar ~10 m par udti cheez ko lagbhag 30 KM par hi dekh paati hai, yaani ~30 second (radar horizon ka anumaan)
• Exports: Philippines (pehla grahak, 2022 deal), Indonesia (March 2026 agreement); Philippines aur missiles lene par vichaar kar raha hai (Nov 2026)

Aapke hisaab se BrahMos ka agla khareedar kaun? Desh ka naam comment me likho.
Aisi aur defence aur geopolitics ke liye Reality Shift ko subscribe karo.

Note: graphics schematic hain, scale par nahi. 30 second ek physics-based anumaan hai; asli warning time radar, oonchai aur mausam par nirbhar karta hai.
""",
    "tags": ["brahmos", "brahmos missile", "brahmos speed", "mach 3", "supersonic cruise missile", "indian defence",
             "sea skimming missile", "radar horizon", "brahmos philippines", "brahmos indonesia", "drdo",
             "indian navy", "defence shorts hindi", "bharat ki taakat", "reality shift"],
    "hashtags": ["#Shorts", "#BrahMos", "#IndianDefence"],
}


def thumbnail(ctx):
    """1080x1920 cover: 1 KM/SEC! over BrahMos streaking low across a night sea."""
    seascape(ctx, 0.37, 1150, 1.0)
    for i in range(14):   # heavy motion streaks behind the missile
        y = 980 + (i - 7) * 18
        line(ctx, [(-50, y), (520 - abs(i - 7) * 30, y)], (1, 1, 1), 4, 0.12 + 0.02 * (7 - abs(i - 7)))
    glow(ctx, 640, 980, 520, FLAME, 0.25)
    missile(ctx, 640, 980, 2.3, 0.37, ang=-0.06)
    g = cairo.LinearGradient(0, 0, 0, 800)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.9)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 800)
    ctx.set_source(g)
    ctx.fill()
    vignette(ctx)
    glow(ctx, 540, 480, 600, GOLD, 0.18)
    text(ctx, "1 KM", 540, 360, 300, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=24)
    text(ctx, "/SEC!", 540, 640, 260, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "REALITY SHIFT", 540, 1780, 40, (1, 1, 1), a=0.7)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.brahmos")  # a named module, so work files land in work/<name>/
    engine.make_frame = story.make_frame
    final = engine.render(story, "edge")
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
