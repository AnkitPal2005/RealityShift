"""Reality Shift Short — Zorawar, India's ~25 t light tank for Ladakh (~42s).

Usage:
  python make.py zorawar

New "defence lab" layout (not the intel-file or Chabahar compose()): blueprint grid with Ladakh ridges, a
persistent altitude gauge on the left, side-view tank schematics, pop-in captions in the 1160-1250 band,
scan-line wipes between scenes, bottom 400px clean. Ends on a GAME-CHANGER? gauge card asking for a comment,
no subscribe badge / bell / cursor.
Facts: Zorawar light tank by DRDO (CVRDE) with L&T, ~25 t, 105 mm gun, prototype shown July 2024 about two
years after the project started; high-altitude firing trials in Ladakh above 4,200 m (Dec 2024); designed to be
air-transportable and to work with drones / loitering munitions. Need came from the 2020 eastern Ladakh stand-off,
where China fielded Type 15 light tanks and India's main tanks (T-72 / T-90, ~45-46 t) are heavy for the passes.
Named after General Zorawar Singh, who led the Dogra conquest of Ladakh from 1834.
"""

import importlib
import json
import math

import cairo
import numpy as np

from core import engine
from core.engine import *  # noqa: F401,F403
from shorts.chabahar import Cued
from shorts.maldives import CN_RED, CN_YELLOW
from shorts.rupee import VOICE_TONES
from shorts.reality_shift import GOLD, INDIA_GREEN, SAFFRON, stamp

TOPIC = "ZORAWAR LIGHT TANK"
OUTPUTS = {"edge": "zorawar_short.mp4"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.3
TAIL_PAD = 0.3
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 104
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"

RED = hexc("#FF3B3B")
CYAN = hexc("#5CD6FF")
ICE = hexc("#BFEFFF")
OLIVE = hexc("#5B6A30")
ZOR = hexc("#6E7B3C")
CN_TANK = hexc("#6A2C2C")
MONO = "Consolas"

SPEC = [
    {"key": "thin", "accent": CYAN, "text": "14,000 FT KI JUNG",
     "visual": "Altitude gauge climbs to 4,200 m, heavy Indian tank wheezes on the slope, LAC line, China's Type 15 rolls in",
     "vo": [("hook", [("चौदह हज़ार फीट पर,", "CHAUDAH HAZAAR FEET PAR,")], 0.15),
            ("punch", [("हवा इतनी पतली है,", "HAWA ITNI PATLI HAI,")], 0.15),
            ("build", [("कि भारी टैंक का इंजन", "KI BHAARI TANK KA ENGINE"), ("भी हांफने लगता है।", "BHI HAANFNE LAGTA HAI!")],
             0.4),
            ("low", [("और एलएसी के उस पार,", "AUR LAC KE US PAAR,")], 0.15),
            ("tell", [("चीन ले आया", "CHINA LE AAYA"), ("हल्के टाइप फिफ्टीन टैंक।", "HALKE TYPE-15 TANK!")], 0)]},
    {"key": "answer", "accent": SAFFRON, "text": "ZORAWAR",
     "visual": "Question mark, blueprint of Zorawar draws itself and fills in, DRDO + L&T, ~2 SAAL, 46 T vs 25 T bars",
     "vo": [("setup", [("तो भारत का जवाब", "TOH BHARAT KA JAWAB"), ("क्या था?", "KYA THA?")], 0.6),
            ("punch", [("ज़ोरावर!", "ZORAWAR!")], 0.35),
            ("build", [("डी आर डी ओ और एल एंड टी ने,", "DRDO AUR L&T NE,")], 0.12),
            ("punch", [("सिर्फ दो साल में", "SIRF 2 SAAL MEIN"), ("तैयार कर दिया!", "TAIYAAR KAR DIYA!")], 0.3),
            ("punch", [("वज़न सिर्फ पच्चीस टन।", "WAZAN SIRF 25 TON!")], 0)]},
    {"key": "power", "accent": GOLD, "text": "105 MM + DRONE",
     "visual": "Zorawar on a ridge: 105 MM gun callout, drone lifts off, transport plane crosses, 4,200 M+ trial, target hit",
     "vo": [("tell", [("एक सौ पांच एमएम की तोप,", "105 MM KI TOP,")], 0.15),
            ("tell", [("ड्रोन से जुड़ा सिस्टम,", "DRONE SE JUDA SYSTEM,")], 0.2),
            ("build", [("और इतना हल्का कि", "AUR ITNA HALKA KI"), ("हवाई जहाज़ से सीधा", "HAWAI JAHAZ SE SEEDHA"),
                       ("लद्दाख पहुंच जाए।", "LADAKH PAHUNCH JAAYE!")], 0.35),
            ("low", [("ट्रायल में", "TRIAL MEIN"), ("चार हज़ार दो सौ मीटर से ऊपर,", "4200 METER SE UPAR,")], 0.15),
            ("punch", [("निशाना सटीक लगा।", "NISHANA SATEEK LAGA!")], 0)]},
    {"key": "verdict", "accent": INDIA_GREEN, "text": "GAME-CHANGER?",
     "visual": "Plaque for General Zorawar Singh on a peak, then a GAME-CHANGER? gauge card asks HAAN / NAHI in the comments",
     "vo": [("tell", [("ये नाम उस जनरल का है,", "YEH NAAM US GENERAL KA HAI,")], 0.12),
            ("punch", [("जिसने लद्दाख जीता था।", "JISNE LADAKH JEETA THA!")], 0.45),
            ("ask", [("क्या ज़ोरावर बनेगा", "KYA ZORAWAR BANEGA"), ("पहाड़ों का गेम चेंजर?", "PAHADON KA GAME-CHANGER?")], 0.5),
            ("cta", [("कमेंट में बताओ,", "COMMENT MEIN BATAO,")], 0.15),
            ("cta", [("और रियलिटी शिफ्ट को", "AUR REALITY SHIFT KO"), ("सब्सक्राइब करो!", "SUBSCRIBE KARO!")], 0)]},
]

# the approved narrator (Rupee VOICE_TONES) plus a slower, lower "setup" for the suspense question before a reveal
TONES = {**VOICE_TONES, "setup": ("+4%", "-4Hz", "+8%")}
DELIVERY = {s["key"]: [(TONES[tone], " ".join(hi for hi, _ in chunks), pause) for tone, chunks, pause in s["vo"]]
            for s in SPEC}
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {"CHAUDAH": GOLD, "HAZAAR": GOLD, "PATLI": ICE, "BHAARI": GOLD, "HAANFNE": RED, "LAC": RED, "CHINA": RED,
       "TYPE-15": RED, "JAWAB": SAFFRON, "ZORAWAR": SAFFRON, "DRDO": CYAN, "L&T": CYAN, "2": GOLD, "SAAL": GOLD, "SIRF": GOLD,
       "25": GOLD, "TON": GOLD, "105": GOLD, "MM": GOLD, "DRONE": CYAN, "HALKA": CYAN, "HAWAI": CYAN, "LADAKH": GOLD,
       "4200": GOLD, "SATEEK": INDIA_GREEN, "GENERAL": SAFFRON, "JEETA": SAFFRON, "GAME-CHANGER": GOLD,
       "COMMENT": GOLD, "SUBSCRIBE": RED}

CAP_TOP, CAP_BOTTOM = 1160, 1250
UI_CLEAR = H - 400
GROUND = 1040


# ============================================================ blueprint world

FAR = [(-60, 760), (60, 600), (170, 660), (300, 500), (420, 620), (560, 450), (700, 590), (840, 470), (960, 610),
       (1140, 540)]
MID = [(-60, 880), (120, 740), (280, 830), (420, 730), (580, 850), (720, 720), (880, 820), (1020, 740), (1140, 800)]
NEAR = [(-60, GROUND + 10), (260, GROUND - 6), (560, GROUND + 8), (820, GROUND - 4), (1140, GROUND + 6)]


def blueprint(ctx, t, glow_c=CYAN):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc("#071A2E"))
    g.add_color_stop_rgb(1, *hexc("#020911"))
    ctx.set_source(g)
    ctx.paint()
    glow(ctx, W * 0.6, 500, 900, glow_c, 0.12)
    for k in range(0, max(W, H) // 60 + 1):
        a = 0.1 if k % 5 == 0 else 0.045
        if k * 60 <= W:
            line(ctx, [(k * 60, 0), (k * 60, H)], CYAN, 1, a)
        line(ctx, [(0, k * 60), (W, k * 60)], CYAN, 1, a)


def _ridge(ctx, pts, fill, snow_y, snow_a, edge_a, shift):
    ctx.save()
    ctx.translate(shift, 0)
    ctx.move_to(pts[0][0], H)
    for p in pts:
        ctx.line_to(*p)
    ctx.line_to(pts[-1][0], H)
    ctx.close_path()
    rgba(ctx, fill)
    ctx.fill_preserve()
    ctx.save()
    ctx.clip_preserve()
    ctx.rectangle(-200, 0, W + 400, snow_y)
    rgba(ctx, (0.93, 0.97, 1.0), snow_a)
    ctx.fill()
    ctx.restore()
    ctx.new_path()
    line(ctx, pts, CYAN, 2, edge_a)
    ctx.restore()


def ridges(ctx, t):
    _ridge(ctx, FAR, hexc("#132840"), 540, 0.38, 0.35, -6 * math.sin(t * 0.25))
    _ridge(ctx, MID, hexc("#0D1D30"), 770, 0.16, 0.3, -12 * math.sin(t * 0.25))
    _ridge(ctx, NEAR, hexc("#08131F"), 0, 0, 0.45, 0)


def snow(ctx, t, n=60, k=1.0):
    for i in range(n):
        x = (rnd(i, 1) * W + 30 * math.sin(t * 0.8 + i)) % W
        y = (rnd(i, 2) * H + t * (70 + 90 * rnd(i, 3))) % H
        circle(ctx, x, y, 1.5 + 2.5 * rnd(i, 4), (1, 1, 1), (0.2 + 0.4 * rnd(i, 5)) * k)


# ============================================================ tanks (side view, facing +x)

TANKS = {
    "heavy":   {"L": 430, "hh": 74, "r": 27, "n": 6, "tw": 190, "th": 82, "tx": -30, "gl": 270, "dome": True,
                "brake": False},
    "zorawar": {"L": 400, "hh": 58, "r": 22, "n": 6, "tw": 200, "th": 64, "tx": -40, "gl": 320, "dome": False,
                "brake": True},
    "type15":  {"L": 400, "hh": 62, "r": 23, "n": 6, "tw": 185, "th": 62, "tx": -35, "gl": 285, "dome": False,
                "brake": False},
}


def tank(ctx, x, y, s, kind, t, body, rot=0.0, flip=False, outline=None, reveal=1.0, a=1.0, recoil=0.0, roll=0.0):
    """Side-view tank, track bottom centred on (x, y). outline= draws it as a blueprint stroke instead of solid.
    Returns the muzzle and exhaust points in the caller's coordinates."""
    P = TANKS[kind]
    L, r, hh, tw, th, tx, gl = P["L"], P["r"], P["hh"], P["tw"], P["th"], P["tx"], P["gl"]
    base = -(2 * r + 12)
    top = base - hh
    gx0, gy = tx + tw / 2 - 12, top - th * 0.55
    sx = -s if flip else s

    def to_parent(lx, ly):
        px, py = lx * sx, ly * s
        return x + px * math.cos(rot) - py * math.sin(rot), y + px * math.sin(rot) + py * math.cos(rot)

    muzzle, exhaust = to_parent(gx0 + gl - recoil, gy), to_parent(-L / 2 + 6, top + 6)
    if reveal <= 0 or a <= 0:
        return muzzle, exhaust
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(sx, s)
    if reveal < 1:
        ctx.rectangle(-L / 2 - 40, top - th - 300, (L + gl + 120) * reveal, 700)
        ctx.clip()

    def paint(c):
        if outline:
            rgba(ctx, outline, 0.95 * a)
            ctx.set_line_width(3.2 / s)
            ctx.stroke()
        else:
            rgba(ctx, c, a)
            ctx.fill()

    rrect(ctx, -L / 2 - 6, base, L + 12, 2 * r + 12, r + 6)
    paint((0.09, 0.09, 0.08))
    for i in range(P["n"]):
        wx = -L / 2 + r + 12 + i * (L - 2 * r - 24) / (P["n"] - 1)
        ctx.arc(wx, base + r + 6, r, 0, math.tau)
        paint(shade(body, 0.55))
        for k in range(3):
            ang = roll + k * math.tau / 3
            line(ctx, [(wx, base + r + 6), (wx + r * 0.8 * math.cos(ang), base + r + 6 + r * 0.8 * math.sin(ang))],
                 outline or (0.15, 0.15, 0.13), 2.5 / s, a)
    ctx.move_to(-L / 2 - 4, base)
    ctx.line_to(L / 2 + 34, base)
    ctx.line_to(L / 2 - 16, top)
    ctx.line_to(-L / 2 + 4, top)
    ctx.close_path()
    paint(body)
    ctx.rectangle(-L / 2 + 10, base - hh * 0.42, L * 0.86, 5)
    paint(shade(body, 0.7))
    ctx.rectangle(gx0 - 22 - recoil, gy - 15, 30, 30)
    paint(shade(body, 0.8))
    ctx.rectangle(gx0 - recoil, gy - 7, gl, 14)
    paint(shade(body, 0.75))
    if P["brake"]:
        ctx.rectangle(gx0 + gl - recoil - 30, gy - 12, 32, 24)
        paint(shade(body, 0.6))
    if P["dome"]:
        rrect(ctx, tx - tw / 2, top - th, tw, th, th * 0.55)
    else:
        ctx.move_to(tx - tw / 2, top)
        ctx.line_to(tx + tw / 2 + 12, top)
        ctx.line_to(tx + tw / 2 - 22, top - th)
        ctx.line_to(tx - tw / 2 + 12, top - th)
        ctx.close_path()
    paint(shade(body, 1.12))
    rrect(ctx, tx - tw * 0.25, top - th - 14, 48, 16, 5)
    paint(shade(body, 0.9))
    line(ctx, [(tx - tw / 2 + 20, top - th), (tx - tw / 2 + 4, top - th - 90)], outline or (0.2, 0.2, 0.2), 2.5 / s, a)
    ctx.restore()
    return muzzle, exhaust


def smoke(ctx, x, y, t, k, c=(0.55, 0.55, 0.55)):
    for i in range(7):
        u = (t * 0.9 + i / 7) % 1.0
        circle(ctx, x - 70 * u - 10 * math.sin(i), y - 90 * u, 10 + 34 * u, c, 0.45 * (1 - u) * k)


def flash(ctx, x, y, u, c=GOLD):
    if 0 <= u < 0.3:
        k = 1 - u / 0.3
        glow(ctx, x, y, 200 * k + 40, c, 0.9 * k)
        circle(ctx, x, y, 30 * k, (1, 1, 1), k)


def blast(ctx, x, y, u):
    if u <= 0:
        return
    k = clamp(u / 0.6)
    glow(ctx, x, y, 60 + 260 * k, hexc("#FF8A2A"), 0.85 * (1 - k))
    for i in range(14):
        ang = i * math.tau / 14 + rnd(i, 7)
        d = 220 * ease_out_cubic(k) * (0.5 + 0.5 * rnd(i, 8))
        circle(ctx, x + d * math.cos(ang), y + d * math.sin(ang) - 60 * k, 6 * (1 - k) + 2, GOLD, 1 - k)
    for i in range(5):
        circle(ctx, x - 40 + 20 * i, y - 40 - 120 * k * (0.6 + 0.4 * rnd(i, 9)), 30 + 40 * k, (0.25, 0.25, 0.27),
               0.6 * (1 - k * 0.7))


def chip(ctx, s, x, y, c, u, size=40, sub=None, anchor="c"):
    """Rounded spec chip that slides up into place; a dot in the accent colour leads the label."""
    if u <= 0:
        return
    k = ease_out_cubic(u / 0.3)
    w = max(text_width(ctx, s, size), text_width(ctx, sub, size * 0.62, font=MONO) if sub else 0) + 80
    h = size * (2.1 if sub else 1.45)
    x0 = x - w / 2 if anchor == "c" else (x if anchor == "l" else x - w)
    y = y + 30 * (1 - k)
    rrect(ctx, x0, y - h / 2, w, h, h / 2 if not sub else 22)
    rgba(ctx, (0.02, 0.05, 0.09), 0.9 * k)
    ctx.fill_preserve()
    rgba(ctx, c, k)
    ctx.set_line_width(3)
    ctx.stroke()
    circle(ctx, x0 + 30, y - (size * 0.36 if sub else 0), size * 0.17, c, k)
    text(ctx, s, x0 + 52, y - (size * 0.36 if sub else 0), size, (1, 1, 1), a=k, anchor="l")
    if sub:
        text(ctx, sub, x0 + 52, y + size * 0.48, size * 0.62, c, font=MONO, a=k, anchor="l")


def callout(ctx, p, q, c, u):
    """Leader line from a part of a drawing (p) out to a label anchor (q)."""
    if u <= 0:
        return
    k = ease_out_cubic(u / 0.3)
    e = (lerp(p[0], q[0], k), lerp(p[1], q[1], k))
    circle(ctx, *p, 9, c)
    line(ctx, [p, e], c, 3, 0.9)


def drone(ctx, x, y, t, c=CYAN):
    line(ctx, [(x - 60, y), (x + 60, y)], (0.75, 0.8, 0.85), 6)
    rrect(ctx, x - 24, y - 12, 48, 26, 8)
    rgba(ctx, (0.2, 0.24, 0.28))
    ctx.fill()
    for sx in (-1, 1):
        w = 34 * abs(math.sin(t * 40 + sx))
        line(ctx, [(x + sx * 60 - w, y - 12), (x + sx * 60 + w, y - 12)], (0.9, 0.95, 1.0), 4, 0.8)
    circle(ctx, x, y + 6, 5, c if int(t * 4) % 2 else RED)


def plane(ctx, x, y, s):
    """Four-engine transport silhouette heading right."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    c = hexc("#9FB3C8")
    rrect(ctx, -260, -34, 520, 68, 34)
    rgba(ctx, c)
    ctx.fill()
    ctx.move_to(-40, -10)
    ctx.line_to(-150, -170)
    ctx.line_to(-100, -170)
    ctx.line_to(70, -10)
    ctx.close_path()
    ctx.fill()
    ctx.move_to(-230, -20)
    ctx.line_to(-290, -150)
    ctx.line_to(-240, -150)
    ctx.line_to(-170, -20)
    ctx.close_path()
    ctx.fill()
    for ex in (-120, -70):
        rrect(ctx, ex - 22, -120 + (ex + 120) * 0.6, 44, 20, 8)
        rgba(ctx, shade(c, 0.7))
        ctx.fill()
    for k in range(6):
        circle(ctx, 150 - k * 46, -6, 8, hexc("#20324A"))
    ctx.restore()


def target(ctx, x, y, t, a=1.0):
    for k, c in enumerate((RED, (1, 1, 1), RED)):
        circle(ctx, x, y, 46 - k * 15, c, a)
    line(ctx, [(x, y + 46), (x, y + 110)], (0.6, 0.6, 0.6), 5, a)


# ============================================================ scenes

class Thin(Cued):
    """Gauge climbs to 4,200 m; heavy tank wheezes (smoke, power bar drops); LAC line; Type 15 rolls in."""

    def beats(self, d):
        c = self.cue
        return {"thin": c("PATLI", d * 0.15), "heavy": c("BHAARI", d * 0.3), "gasp": c("HAANFNE", d * 0.42),
                "lac": c("LAC", d * 0.6), "china": c("CHINA", d * 0.72), "t15": c("TYPE-15", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        ticks = [(0.1 + k * 0.12, "tick" if k % 2 else "tock") for k in range(12)]
        return [(0.02, "boom"), (b["thin"], "whoosh"), (b["heavy"] - 0.2, "engine", 2.2), (b["gasp"], "alarm"),
                (b["lac"], "thud"), (b["china"], "engine", 1.6), (b["t15"], "boom")] + ticks

    def draw(self, ctx, t, d):
        b = self.beats(d)
        blueprint(ctx, t)
        ridges(ctx, t)
        snow(ctx, t, 30 + int(50 * clamp(t / 2)))
        u = t - b["thin"]
        if u > 0 and t < b["lac"]:
            chip(ctx, "OXYGEN ~40% KAM", 540, 300, ICE, u, size=46, sub="4,200 M PAR, SEA LEVEL SE")
        gasp = clamp((t - b["gasp"]) / 0.4)
        shake = 4 * math.sin(t * 50) * gasp
        hx = lerp(-200, 330, ease_out_cubic(clamp(t / 1.4)))
        _, ex = tank(ctx, hx + shake, GROUND - 4, 0.62, "heavy", t, OLIVE, rot=-0.035, roll=-t * 3 * (1 - 0.6 * gasp))
        u = t - b["heavy"]
        if u > 0 and t < b["china"]:
            chip(ctx, "T-90 · ~46 TON", 330, 760, GOLD, u, size=40)
        if gasp:
            smoke(ctx, *ex, t, gasp)
            power = lerp(1.0, 0.62, gasp) + 0.03 * math.sin(t * 9)
            x0, y0 = 150, 870
            text(ctx, "ENGINE POWER", x0, y0 - 34, 30, (1, 1, 1), font=MONO, anchor="l")
            rrect(ctx, x0, y0, 360, 30, 8)
            rgba(ctx, (1, 1, 1), 0.12)
            ctx.fill()
            rrect(ctx, x0, y0, 360 * power, 30, 8)
            rgba(ctx, RED if power < 0.8 else GOLD)
            ctx.fill()
            ax = x0 + 390
            ctx.move_to(ax - 16, y0 + 4)
            ctx.line_to(ax + 16, y0 + 4)
            ctx.line_to(ax, y0 + 28)
            ctx.close_path()
            rgba(ctx, RED)
            ctx.fill()
        u = t - b["lac"]
        if u > 0:
            k = ease_out_cubic(u / 0.4)
            ctx.set_dash([26, 18], -t * 40)
            line(ctx, [(660, GROUND), (660, lerp(GROUND, 380, k))], RED, 7)
            ctx.set_dash([])
            text(ctx, "LAC", 660, 340, 54, RED, font=CAPTION_FONT, bold=False, a=k)
        u = t - b["china"]
        if u > 0:
            cx = lerp(W + 260, 880, ease_out_cubic(u / 1.0))
            tank(ctx, cx, GROUND, 0.52, "type15", t, CN_TANK, flip=True, roll=t * 3 * (1 - clamp(u)))
            chip(ctx, "CHINA · TYPE 15", 800, 760, CN_RED, u - 0.3, size=40, sub="LIGHT TANK")
        u = t - b["t15"]
        if u > 0:
            stamp(ctx, 540, 470, u, -0.04, 520, 140, CN_RED, [("HALKA + TEZ", 0, 92, CN_YELLOW)])


class Answer(Cued):
    """Big '?', then Zorawar's blueprint draws itself and fills; DRDO + L&T, ~2 SAAL; 46 T vs 25 T weight bars."""

    def beats(self, d):
        c = self.cue
        return {"name": c("ZORAWAR", d * 0.2), "drdo": c("DRDO", d * 0.4), "yrs": c("SAAL", d * 0.6),
                "wt": c("25", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (0.3, "beep"), (b["name"], "boom"), (b["name"] + 0.1, "zap"), (b["drdo"], "pop"),
                (b["drdo"] + 0.25, "pop"), (b["yrs"], "thud"), (b["wt"], "whoosh"), (b["wt"] + 0.6, "kaching")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        blueprint(ctx, t, SAFFRON)
        snow(ctx, t, 25, 0.6)
        u = t - b["name"]
        if u < 0.3:  # the question
            k = ease_out_back(clamp(t / 0.4)) * (1 - clamp(u / 0.3) if u > 0 else 1)
            text(ctx, "?", 540, 640, 520 * k + 1, SAFFRON, font=CAPTION_FONT, bold=False, a=0.9,
                 stroke=(0, 0, 0), stroke_w=14)
        if u > 0:
            draw = clamp(u / 0.9)
            fill = clamp((u - 0.9) / 0.5)
            ty = 960
            if fill < 1:
                tank(ctx, 440, ty, 1.0, "zorawar", t, ZOR, outline=CYAN, reveal=draw)
            tank(ctx, 440, ty, 1.0, "zorawar", t, ZOR, a=fill)
            if draw > 0.2:  # dimension line under the drawing
                k = clamp((draw - 0.2) / 0.6)
                line(ctx, [(240, ty + 40), (lerp(240, 900, k), ty + 40)], CYAN, 3, 0.8)
                for xx in (240, lerp(240, 900, k)):
                    line(ctx, [(xx, ty + 26), (xx, ty + 54)], CYAN, 3, 0.8)
                text(ctx, "LIGHT TANK", 570, ty + 80, 32, CYAN, font=MONO, a=k)
            ctx.save()  # the name: slams in, then stays as the page title
            sc = lerp(1.9, 1.0, ease_out_cubic(u / 0.25))
            ctx.translate(540, 300)
            ctx.scale(sc, sc)
            text(ctx, "ZORAWAR", 0, 0, 170, SAFFRON, font=CAPTION_FONT, bold=False, a=clamp(u / 0.12),
                 stroke=(0, 0, 0), stroke_w=12)
            ctx.restore()
        u = t - b["drdo"]
        if u > 0 and t < b["wt"]:
            chip(ctx, "DRDO", 330, 470, CYAN, u, size=50)
            text(ctx, "+", 540, 470, 70, (1, 1, 1), a=clamp(u / 0.3))
            chip(ctx, "L&T", 750, 470, CYAN, u - 0.15, size=50)
        u = t - b["yrs"]
        if u > 0 and t < b["wt"]:
            stamp(ctx, 540, 610, u, -0.03, 420, 120, GOLD, [("~2 SAAL", 0, 86, GOLD)])
        u = t - b["wt"]
        if u > 0:
            for k, (label, tons, c) in enumerate((("T-90", 46, (0.6, 0.62, 0.55)), ("ZORAWAR", 25, SAFFRON))):
                y = 470 + k * 120
                g = ease_out_cubic(clamp((u - 0.15 * k) / 0.6))
                text(ctx, label, 90, y, 44, (1, 1, 1), font=CAPTION_FONT, bold=False, anchor="l", a=clamp(u / 0.2))
                rrect(ctx, 330, y - 30, 11 * tons * g + 1, 60, 12)
                rgba(ctx, c, 0.9)
                ctx.fill()
                text(ctx, f"{round(tons * g)} T", 350 + 11 * tons * g, y, 48, c, font=CAPTION_FONT, bold=False,
                     anchor="l")


class Power(Cued):
    """Zorawar on the ridge: 105 MM callout + shot, drone lifts off, transport plane crosses, 4,200 M+ trial, hit."""

    def beats(self, d):
        c = self.cue
        return {"gun": c("105", 0.1), "drone": c("DRONE", d * 0.15), "light": c("HALKA", d * 0.3),
                "air": c("HAWAI", d * 0.4), "trial": c("TRIAL", d * 0.62), "hit": c("NISHANA", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["gun"] + 0.35, "boom"), (b["drone"], "zap"), (b["drone"] + 0.1, "beep"),
                (b["air"], "whoosh"), (b["air"] + 0.4, "whoosh"), (b["trial"], "beep"), (b["trial"] + 0.2, "beep"),
                (b["hit"], "boom"), (b["hit"] + 0.35, "boom"), (b["hit"] + 0.5, "kaching")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        blueprint(ctx, t, GOLD)
        ridges(ctx, t)
        snow(ctx, t, 45)
        tx_, ty_ = 330, GROUND
        tgt = (900, 760)
        shot = t - b["hit"]
        fire1 = t - (b["gun"] + 0.35)
        recoil = 22 * math.exp(-min(abs(x) for x in (fire1, shot)) * 8) if (fire1 > 0 or shot > 0) else 0
        muzzle, _ = tank(ctx, tx_, ty_, 0.6, "zorawar", t, ZOR, rot=-0.02, recoil=recoil)
        flash(ctx, *muzzle, fire1)
        u = t - b["gun"]
        if u > 0 and t < b["drone"] + 0.2:
            callout(ctx, muzzle, (760, 560), GOLD, u)
            chip(ctx, "105 MM GUN", 760, 520, GOLD, u - 0.2, size=48)
        u = t - b["drone"]
        if u > 0:
            k = ease_out_cubic(u / 0.8)
            dx, dy = lerp(tx_ - 20, 300, k), lerp(ty_ - 150, 520, k) + 10 * math.sin(t * 3)
            if t < b["air"] or t > b["trial"]:
                ctx.set_dash([10, 12], -t * 60)
                line(ctx, [(tx_ - 20, ty_ - 140), (dx, dy)], CYAN, 3, 0.7)
                ctx.set_dash([])
            drone(ctx, dx, dy, t)
            if t < b["air"]:
                chip(ctx, "DRONE LINK", 470, 410, CYAN, u - 0.3, size=42)
        u = t - b["light"]
        if u > 0 and t < b["air"]:
            chip(ctx, "~25 TON", 760, 680, SAFFRON, u, size=46)
        u = t - b["air"]
        if 0 < u < 2.8:
            px = lerp(-420, W + 420, clamp(u / 2.6))
            plane(ctx, px, 330, 0.95)
            chip(ctx, "AIR-LIFT → LADAKH", 540, 520, CYAN, u - 0.2, size=44)
        u = t - b["trial"]
        if u > 0:
            stamp(ctx, 540, 300, u, -0.03, 520, 150, GOLD, [("4,200 M+", -16, 86, GOLD), ("LADAKH TRIAL", 46, 34, (1, 1, 1))])
            if shot < 0.35:
                target(ctx, *tgt, t, clamp(u / 0.3))
        if shot > 0:
            flash(ctx, *muzzle, shot)
            k = clamp(shot / 0.35)
            if k < 1:
                hx, hy = lerp(muzzle[0], tgt[0], k), lerp(muzzle[1], tgt[1], k) - 60 * math.sin(math.pi * k)
                line(ctx, [(lerp(muzzle[0], hx, 0.6), lerp(muzzle[1], hy, 0.6)), (hx, hy)], GOLD, 8)
                glow(ctx, hx, hy, 40, GOLD, 0.9)
            blast(ctx, *tgt, shot - 0.35)
            if shot > 0.5:
                stamp(ctx, 540, 520, shot - 0.5, 0.04, 520, 130, INDIA_GREEN, [("TARGET HIT", 0, 88, INDIA_GREEN)])


class Verdict(Cued):
    """Plaque for Gen. Zorawar Singh on a peak, then a GAME-CHANGER? gauge card asks HAAN / NAHI in the comments."""

    def beats(self, d):
        c = self.cue
        return {"gen": c("GENERAL", 0.1), "won": c("JEETA", d * 0.18), "q": c("BANEGA", d * 0.38),
                "cmt": c("COMMENT", d * 0.68), "sub": c("SUBSCRIBE", d * 0.88)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["gen"], "dingdong"), (b["won"], "boom"), (b["q"], "whoosh"), (b["q"] + 0.3, "pop"),
                (b["cmt"], "pop"), (b["cmt"] + 0.1, "beep"), (b["sub"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        blueprint(ctx, t, INDIA_GREEN)
        ridges(ctx, t)
        snow(ctx, t, 50)
        tank(ctx, 300, GROUND, 0.5, "zorawar", t, ZOR)
        u = t - b["gen"]
        if u > 0:
            self.plaque(ctx, u, t - b["won"])
        u = t - b["q"]
        if u > 0:
            ctx.rectangle(0, 0, W, H)
            rgba(ctx, (0.01, 0.02, 0.04), 0.7 * clamp(u / 0.35))
            ctx.fill()
            self.gauge(ctx, t, u, t - b["cmt"])
        u = t - b["sub"]
        if u > 0:
            stamp(ctx, 540, 1060, u, -0.03, 780, 120, RED, [("SUBSCRIBE • REALITY SHIFT", 0, 58, (1, 1, 1))])

    @staticmethod
    def plaque(ctx, u, uw):
        k = ease_out_back(u / 0.4)
        ctx.save()
        ctx.translate(560, 420)
        ctx.scale(k, k)
        rrect(ctx, -380, -130, 760, 260, 20)
        rgba(ctx, (0.04, 0.05, 0.07), 0.92)
        ctx.fill_preserve()
        rgba(ctx, SAFFRON)
        ctx.set_line_width(5)
        ctx.stroke()
        for sgn in (-1, 1):  # crossed swords
            ctx.save()
            ctx.translate(-290, 0)
            ctx.rotate(sgn * 0.7)
            line(ctx, [(0, -90), (0, 70)], (0.85, 0.87, 0.9), 9)
            line(ctx, [(-22, 50), (22, 50)], GOLD, 9)
            ctx.restore()
        text(ctx, "GEN. ZORAWAR SINGH", 60, -50, 64, (1, 1, 1), font=CAPTION_FONT, bold=False)
        text(ctx, "LADAKH CAMPAIGN · 1834", 60, 30, 36, SAFFRON, font=MONO)
        if uw > 0:
            text(ctx, "LADAKH JEETA", 60, 90, 44, GOLD, font=CAPTION_FONT, bold=False, a=clamp(uw / 0.25))
        ctx.restore()

    @staticmethod
    def gauge(ctx, t, u, uc):
        pop = ease_out_back(u / 0.35)
        ctx.save()
        ctx.translate(540, 600)
        ctx.scale(pop, pop)
        rrect(ctx, -450, -380, 900, 700, 30)
        rgba(ctx, (0.02, 0.04, 0.07), 0.96)
        ctx.fill_preserve()
        rgba(ctx, CYAN)
        ctx.set_line_width(4)
        ctx.stroke()
        text(ctx, "GAME-CHANGER?", 0, -290, 100, GOLD, font=CAPTION_FONT, bold=False)
        cy, r = 110, 300
        for k in range(40):  # red -> green arc
            a0 = math.pi + k * math.pi / 40
            ctx.arc(0, cy, r, a0, a0 + math.pi / 40 + 0.01)
            c = tuple(lerp(RED[i], INDIA_GREEN[i], k / 39) for i in range(3))
            rgba(ctx, c)
            ctx.set_line_width(46)
            ctx.stroke()
        text(ctx, "NAHI", -r, cy + 70, 56, RED, font=CAPTION_FONT, bold=False)
        text(ctx, "HAAN", r, cy + 70, 56, INDIA_GREEN, font=CAPTION_FONT, bold=False)
        swing = math.pi * (0.5 + 0.42 * math.sin(t * 1.7))  # the needle can't make up its mind - you decide
        nx, ny = -math.cos(swing) * (r - 50), cy - math.sin(swing) * (r - 50)
        line(ctx, [(0, cy), (nx, ny)], (1, 1, 1), 12)
        circle(ctx, 0, cy, 26, (1, 1, 1))
        text(ctx, "AAPKA VOTE?", 0, cy + 72, 40, (1, 1, 1), font=MONO)
        if uc > 0:
            k = ease_out_back(uc / 0.3)
            ctx.save()
            ctx.translate(0, cy + 160)
            ctx.scale(k, k)
            rrect(ctx, -300, -48, 600, 96, 48)
            rgba(ctx, GOLD)
            ctx.fill()
            text(ctx, "COMMENT MEIN BATAO", 0, 2, 54, (0.05, 0.05, 0.05), font=CAPTION_FONT, bold=False)
            ctx.restore()
        ctx.restore()


SCENE_CLASSES = {"thin": Thin, "answer": Answer, "power": Power, "verdict": Verdict}


# ============================================================ compositor ("defence lab")

def header(ctx, idx, tl):
    text(ctx, "REALITY SHIFT", 60, 92, 40, (1, 1, 1), anchor="l")
    text(ctx, "DEFENCE LAB  /  ZORAWAR", 62, 136, 26, CYAN, font=MONO, a=0.8, anchor="l")
    for k in range(len(SPEC)):  # progress segments
        x = W - 70 - (len(SPEC) - k) * 74
        rrect(ctx, x, 86, 62, 12, 6)
        done = 1.0 if k < idx else (clamp(tl / engine.SCENES[idx]["dur"]) if k == idx else 0.0)
        rgba(ctx, (1, 1, 1), 0.18)
        ctx.fill()
        if done:
            rrect(ctx, x, 86, 62 * done, 12, 6)
            rgba(ctx, SPEC[k]["accent"])
            ctx.fill()


def altitude(ctx, m):
    """Vertical altitude gauge pinned to the left edge, 0-5,000 m."""
    x, y0, y1 = 34, 1100, 300
    line(ctx, [(x, y0), (x, y1)], CYAN, 3, 0.4)
    for k in range(6):
        y = lerp(y0, y1, k / 5)
        line(ctx, [(x, y), (x + 16, y)], CYAN, 3, 0.5)
    y = lerp(y0, y1, m / 5000)
    line(ctx, [(x, y0), (x, y)], GOLD, 6)
    ctx.move_to(x + 4, y)
    ctx.line_to(x + 26, y - 14)
    ctx.line_to(x + 26, y + 14)
    ctx.close_path()
    rgba(ctx, GOLD)
    ctx.fill()
    text(ctx, f"{int(m):,} M", x + 34, y - 16, 30, GOLD, font=MONO, anchor="l", stroke=(0, 0, 0), stroke_w=5)
    text(ctx, f"~{int(m * 3.281 / 100) * 100:,} FT", x + 34, y + 18, 22, (1, 1, 1), font=MONO, a=0.8, anchor="l",
         stroke=(0, 0, 0), stroke_w=4)


def caption(ctx, sc, tl, accent):
    """Current Hinglish chunk pops in centred in the 1160-1250 band, with an accent bar sweeping under it."""
    cur = None
    for i, (start, _) in enumerate(sc["captions"]):
        if tl >= start - 0.03:
            cur = i
    if cur is None:
        return
    start, cap = sc["captions"][cur]
    u = tl - start + 0.03
    size = 84
    words = cap.split(" ")
    ws = [text_width(ctx, w, size, font=CAPTION_FONT, bold=False) for w in words]
    gap = size * 0.26
    tw = sum(ws) + gap * (len(ws) - 1)
    fit = min(1.0, 940 / tw)
    cy = (CAP_TOP + CAP_BOTTOM) / 2
    pop = lerp(0.7, 1.0, ease_out_back(u / 0.18))
    ctx.save()
    ctx.translate(W / 2, cy)
    ctx.scale(fit * pop, fit * pop)
    x = -tw / 2
    for w, ww in zip(words, ws):
        c = HOT.get(w.strip(PUNCT + "."), (1, 1, 1))
        text(ctx, w, x, 0, size, c, font=CAPTION_FONT, bold=False, anchor="l", stroke=(0, 0, 0), stroke_w=10)
        x += ww + gap
    ctx.restore()
    bw = tw * fit * ease_out_cubic(u / 0.3)
    rrect(ctx, W / 2 - bw / 2, CAP_BOTTOM + 4, bw, 8, 4)
    rgba(ctx, accent)
    ctx.fill()


def scan(ctx, tl, accent):
    """A bright scan line sweeps down on every cut, revealing the new scene above it."""
    u = ease_out_cubic(tl / 0.35)
    if u >= 1:
        return
    y = u * H
    ctx.rectangle(0, y, W, H - y)
    rgba(ctx, (0.0, 0.01, 0.02))
    ctx.fill()
    line(ctx, [(0, y), (W, y)], accent, 30, 0.3)
    line(ctx, [(0, y), (W, y)], (1, 1, 1), 5, 0.95)


def compose(idx, tl):
    sc = engine.SCENES[idx]
    spec = SPEC[idx]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    zoom = 1.0 + 0.035 * tl / sc["dur"]  # slow push toward the ground line
    ctx.save()
    ctx.translate(W / 2, GROUND - 200)
    ctx.scale(zoom, zoom)
    ctx.translate(-W / 2, -(GROUND - 200))
    sc["obj"].draw(ctx, tl, sc["dur"])
    ctx.restore()
    vignette(ctx)
    g = cairo.LinearGradient(0, CAP_BOTTOM + 20, 0, UI_CLEAR)  # bottom 400px stays clean and dark
    g.add_color_stop_rgba(0, 0.0, 0.01, 0.02, 0)
    g.add_color_stop_rgba(1, 0.0, 0.01, 0.02, 0.96)
    ctx.rectangle(0, CAP_BOTTOM + 20, W, H)
    ctx.set_source(g)
    ctx.fill()
    ctx.rectangle(0, UI_CLEAR, W, H - UI_CLEAR)
    rgba(ctx, (0.0, 0.01, 0.02), 0.96)
    ctx.fill()
    if idx in (0, 2):  # the gauge belongs to the mountain scenes
        altitude(ctx, 4200 * ease_in_out(clamp((tl - 0.1) / 1.8)) if idx == 0 else 4200)
    header(ctx, idx, tl)
    caption(ctx, sc, tl, spec["accent"])
    if idx:
        scan(ctx, tl, spec["accent"])
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
        "14,000 Feet Par China Ko Jawab: Zorawar Light Tank 🇮🇳",
        "Zorawar: 25 Ton Ka Tank Jo Ladakh Ke Liye Bana",
        "Zorawar Light Tank Kya Hai? Ladakh Ka Naya Shikari",
        "T-90 Bhaari, Zorawar Halka: Ladakh Me Kyun Zaroori?",
        "China Ke Type 15 Ka Jawab: Bharat Ka Zorawar Tank",
        "DRDO + L&T Ka Zorawar: Pahadon Ka Light Tank",
        "Zorawar Tank: Ladakh Trial Me Sateek Nishana",
        "25 Ton, 105 MM Gun: Zorawar Light Tank Explained",
        "Kya Zorawar Tank Ladakh Me Game-Changer Banega?",
        "Zorawar Light Tank Explained in 40 Seconds",
    ],
    "thumb_text": "CHINA KA JAWAB",
    "queries": ["zorawar light tank", "zorawar tank ladakh", "india light tank"],
    "description": """
Zorawar light tank: India ka ~25 ton ka tank, Ladakh jaise 14,000 feet ke pahadon ke liye banaya gaya.
DRDO aur L&T ne ise sirf ~2 saal me taiyaar kiya, China ke Type 15 light tank ke jawab me.

Is Short me:
• Oonchai par bhaari tanks (T-72 / T-90, ~45-46 ton) ki mushkil kyun badhti hai
• Zorawar: ~25 ton, 105 mm gun, drone integration, air-transportable
• Ladakh me 4,200 meter se upar firing trials (December 2024)
• Naam General Zorawar Singh par, jinhone 1834 se Ladakh campaign lead kiya

Aapki raay: kya Zorawar pahadon ka game-changer banega? HAAN ya NAHI, comment me batao.
Aisi aur defence stories ke liye Reality Shift ko subscribe karo.

Note: video ke drawings schematic hain, scale pe nahi.
""",
    "tags": ["zorawar light tank", "zorawar tank", "india light tank", "drdo", "larsen and toubro", "ladakh",
             "india vs china", "type 15 tank", "indian army", "t-90", "indian defence shorts", "defence hindi",
             "lac ladakh", "make in india defence", "reality shift"],
    "hashtags": ["#Shorts", "#ZorawarTank", "#IndianArmy"],
}


def thumbnail(ctx):
    """1080x1920 cover: CHINA KA / JAWAB over the ridges, Zorawar big and firing."""
    blueprint(ctx, 0.0, SAFFRON)
    ctx.save()
    ctx.translate(0, 220)
    ridges(ctx, 0.0)
    snow(ctx, 0.5, 70)
    muzzle, _ = tank(ctx, 400, GROUND, 1.05, "zorawar", 0.0, ZOR, rot=-0.03)
    glow(ctx, *muzzle, 260, GOLD, 0.8)
    circle(ctx, *muzzle, 34, (1, 1, 1))
    ctx.restore()
    g = cairo.LinearGradient(0, 0, 0, 900)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.95)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 900)
    ctx.set_source(g)
    ctx.fill()
    vignette(ctx)
    glow(ctx, 540, 520, 600, SAFFRON, 0.22)
    text(ctx, "CHINA KA", 540, 380, 230, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "JAWAB", 540, 640, 300, SAFFRON, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=24)
    text(ctx, "ZORAWAR · 25 TON", 540, 850, 64, GOLD, font=MONO, stroke=(0, 0, 0), stroke_w=8)
    text(ctx, "REALITY SHIFT", 540, 1780, 40, (1, 1, 1), a=0.7)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.zorawar")  # a named module, so work files land in work/<name>/
    engine.make_frame = story.make_frame
    final = engine.render(story, "edge")
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
