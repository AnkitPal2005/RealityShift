"""Reality Shift Short — China's Brahmaputra mega-dam (Medog / Yarlung Tsangpo) and India's answer (~40s).

Usage:
  python generate_brahmaputra_dam_short.py

New "water watch" layout (not the fire mission, speed file, naval-brief map, defence-lab blueprint or intel file):
deep-teal night palette, a water-drop emblem + WATER WATCH header top-left, a filling water-tank gauge top-right,
captions on a navy strip with a wave crest that wipes in left-to-right at 1180-1280, a rising-water wipe between
scenes, bottom 400px clean. Ends on a KHATRA / SIRF DAR balance scale that tips as each side is named; no poll
board, subscribe badge, bell or cursor.
Facts (as reported): China broke ground on the lower Yarlung Tsangpo (Medog) hydropower project on 19 July 2025 near
the Great Bend, just upstream of where the river enters Arunachal Pradesh as the Siang and becomes the Brahmaputra in
Assam. Investment ~1.2 trillion yuan (~USD 167 bn, Xinhua); planned ~60 GW, ~300 bn kWh a year, roughly three times
the Three Gorges output. Arunachal CM Pema Khandu called it a "water bomb" (July 2025); the worry is sudden release /
flooding and data on flows, not China "stopping" the river. India's answer: the proposed Siang Upper Multipurpose
Project (~11,000 MW, reservoir of several billion cubic metres as a buffer), still at survey stage.
"""

import importlib
import json
import math

import cairo
import numpy as np

import engine
from engine import *  # noqa: F401,F403
from generate_brahmos_short import big_readout, chip
from generate_chabahar_short import Cued
from stories.reality_shift import GOLD, INDIA_GREEN, SAFFRON, stamp

TOPIC = "BRAHMAPUTRA MEGA DAM"
OUTPUTS = {"edge": "brahmaputra_dam_short.mp4"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.18
TAIL_PAD = 0.12
TRIM = {"thresh": 0.006, "keep": 0.04, "keep_tail": 0.06}
MUSIC_BPM = 96
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"

RED = hexc("#FF4436")
CHINA_RED = hexc("#E8392F")
WATER = hexc("#2EC4E6")
WATER_D = hexc("#0E5C80")
NAVY = hexc("#06182A")
FOAM = hexc("#DDF7FF")
PLATEAU = hexc("#8A6E4E")
EARTH = hexc("#2A3A22")
EARTH_D = hexc("#141C10")
CONCRETE = hexc("#B9C0C6")
SKY_TOP, SKY_BOT = hexc("#04121E"), hexc("#12425A")
MONO = "Consolas"

# each line: (tone, [(spoken Hindi, Hinglish caption), ...], pause after)
SPEC = [
    {"key": "bomb", "accent": WATER, "text": "BRAHMAPUTRA PAR CHINA KA DAM",
     "visual": "Stylised map: the Yarlung Tsangpo flows east across Tibet, U-turns at the Great Bend and drops into "
               "Arunachal (Siang) and Assam (Brahmaputra); a red dam pin lands at the bend next to the dashed border",
     "vo": [("tell", [("भारत की सीमा से", "BHARAT KI SEEMA SE"), ("कुछ ही दूर...", "KUCH HI DOOR...")], 0.35),
            ("punch", [("चीन बना रहा है,", "CHINA BANA RAHA HAI,"), ("दुनिया का सबसे बड़ा", "DUNIYA KA SABSE BADA"),
                       ("हाइड्रो प्रोजेक्ट!", "HYDRO PROJECT!")], 0.25),
            ("tell", [("वो भी ब्रह्मपुत्र पर।", "WOH BHI BRAHMAPUTRA PAR!")], 0)]},
    {"key": "size", "accent": GOLD, "text": "~300 vs ~100 ARAB UNIT",
     "visual": "A dollar counter rolls to ~$167 BN; a 60,000 MW chip; then two bars rise: THREE GORGES ~100 vs MEDOG "
               "~300 billion units a year, with pylons humming behind",
     "vo": [("fast", [("करीब एक सौ सड़सठ", "KAREEB 167"), ("बिलियन डॉलर!", "BILLION DOLLAR!")], 0.25),
            ("tell", [("साठ हज़ार मेगावाट की ताकत...", "60,000 MEGAWATT KI TAAKAT...")], 0.3),
            ("punch", [("यानी थ्री गॉर्जेस से", "YAANI THREE GORGES SE"), ("करीब तीन गुना बिजली!", "KAREEB 3 GUNA BIJLI!")],
             0)]},
    {"key": "khatra", "accent": RED, "text": "'WATER BOMB'?",
     "visual": "Side profile of the valley: the Chinese dam high on the left, a surge released from it races down the "
               "slope, the low Assam plain floods round the houses; FLOOD ALERT; 'WATER BOMB' stamp",
     "vo": [("slow", [("पर असली डर", "PAR ASLI DAR"), ("बिजली का नहीं...", "BIJLI KA NAHI...")], 0.35),
            ("tell", [("अगर कभी", "AGAR KABHI"), ("एक साथ पानी छोड़ा गया,", "EK SAATH PAANI CHHODA GAYA,")], 0.2),
            ("punch", [("तो अरुणाचल और असम में", "TO ARUNACHAL AUR ASSAM ME"), ("बाढ़ का खतरा!", "BAADH KA KHATRA!")],
             0.3),
            ("tell", [("इसीलिए अरुणाचल के मुख्यमंत्री ने", "ISILIYE ARUNACHAL KE CM NE"), ("इसे कहा,", "ISE KAHA,")], 0.2),
            ("punch", [("वॉटर बम!", "'WATER BOMB'!")], 0)]},
    {"key": "jawab", "accent": INDIA_GREEN, "text": "KHATRA YA SIRF DAR?",
     "visual": "Same valley: India's proposed Siang Upper dam rises downstream and its reservoir soaks up the surge "
               "(BUFFER); then a balance scale KHATRA / SIRF DAR tips toward each side as it is named",
     "vo": [("tell", [("भारत का जवाब?", "BHARAT KA JAWAAB?")], 0.3),
            ("punch", [("सियांग अपर प्रोजेक्ट!", "SIANG UPPER PROJECT!")], 0.2),
            ("tell", [("ग्यारह हज़ार मेगावाट,", "11,000 MEGAWATT,"), ("और अरबों घन मीटर पानी का", "AUR ARBON GHAN METER PAANI KA"),
                      ("बफर।", "BUFFER!")], 0.35),
            ("tell", [("आपके हिसाब से,", "AAPKE HISAAB SE,"), ("यह डैम खतरा है,", "YEH DAM KHATRA HAI,"),
                      ("या सिर्फ डर?", "YA SIRF DAR?")], 0.2),
            ("punch", [("कमेंट में बताइए!", "COMMENT ME BATAIYE!")], 0)]},
]

# one narrator: pitch stays fixed (pitch swings read as two voices); pace and loudness carry the delivery
DAM_TONES = {"tell": ("+12%", "+0Hz", "+10%"), "punch": ("+10%", "+0Hz", "+20%"),
             "slow": ("+4%", "+0Hz", "+8%"), "fast": ("+18%", "+0Hz", "+18%")}
DELIVERY = {s["key"]: [(DAM_TONES[tone], " ".join(hi for hi, _ in chunks), pause) for tone, chunks, pause in s["vo"]]
            for s in SPEC}
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {"BHARAT": SAFFRON, "SEEMA": SAFFRON, "CHINA": CHINA_RED, "DUNIYA": GOLD, "SABSE": GOLD, "BADA": GOLD,
       "HYDRO": WATER, "BRAHMAPUTRA": WATER, "167": GOLD, "BILLION": GOLD, "DOLLAR": GOLD, "60,000": GOLD,
       "MEGAWATT": GOLD, "3": GOLD, "GUNA": GOLD, "BIJLI": GOLD, "THREE": FOAM, "GORGES": FOAM, "ASLI": RED,
       "DAR": RED, "PAANI": WATER, "CHHODA": RED, "ARUNACHAL": SAFFRON, "ASSAM": INDIA_GREEN, "BAADH": RED,
       "KHATRA": RED, "WATER": RED, "BOMB": RED, "CM": SAFFRON, "JAWAAB": INDIA_GREEN, "SIANG": INDIA_GREEN,
       "UPPER": INDIA_GREEN, "11,000": INDIA_GREEN, "ARBON": WATER, "BUFFER": WATER, "COMMENT": GOLD, "SIRF": WATER}

CAP_TOP, CAP_BOTTOM = 1180, 1280
UI_CLEAR = H - 400


# ============================================================ drawing kit

def night_sky(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, 1150)
    g.add_color_stop_rgb(0, *SKY_TOP)
    g.add_color_stop_rgb(1, *SKY_BOT)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()
    for i in range(36):
        circle(ctx, rnd(i, 41) * W, 160 + rnd(i, 42) * 360, 1 + 1.2 * rnd(i, 43), (1, 1, 1),
               0.12 + 0.25 * rnd(i, 44) * (0.6 + 0.4 * math.sin(t * 2 + i)))


def far_peaks(ctx, base, amp, seed, c, a=1.0, drift=0.0):
    """Himalayan silhouette with snow caps."""
    pts = []
    for i in range(31):
        x = i / 30 * (W + 200) - 100 - drift
        h = amp * (0.4 + 0.6 * abs(math.sin(i * 1.1 + seed)) * (0.6 + 0.4 * rnd(i, seed)))
        pts.append((x, base - h))
    ctx.move_to(-100, base + 600)
    for p in pts:
        ctx.line_to(*p)
    ctx.line_to(W + 100, base + 600)
    ctx.close_path()
    rgba(ctx, c, a)
    ctx.fill()
    for i in range(1, len(pts) - 1):
        x, y = pts[i]
        if y < pts[i - 1][1] and y < pts[i + 1][1]:
            ctx.move_to(x, y)
            ctx.line_to(x - 22, y + 28)
            ctx.line_to(x + 22, y + 28)
            ctx.close_path()
            rgba(ctx, FOAM, 0.55 * a)
            ctx.fill()


def drop(ctx, x, y, s, c, a=1.0):
    """Water drop emblem."""
    ctx.move_to(x, y - 26 * s)
    ctx.curve_to(x + 6 * s, y - 14 * s, x + 18 * s, y - 2 * s, x + 18 * s, y + 8 * s)
    ctx.arc(x, y + 8 * s, 18 * s, 0, math.pi)
    ctx.curve_to(x - 18 * s, y - 2 * s, x - 6 * s, y - 14 * s, x, y - 26 * s)
    ctx.close_path()
    rgba(ctx, c, a)
    ctx.fill()


def path_len(pts):
    return [0.0] + list(np.cumsum([math.dist(a, b) for a, b in zip(pts, pts[1:])]))


def partial(pts, k):
    """The first k (0-1) of a polyline, by length."""
    cum = path_len(pts)
    target = cum[-1] * clamp(k)
    out = [pts[0]]
    for (a, b), c0, c1 in zip(zip(pts, pts[1:]), cum, cum[1:]):
        if c1 <= target:
            out.append(b)
            continue
        f = (target - c0) / max(1e-6, c1 - c0)
        out.append((lerp(a[0], b[0], f), lerp(a[1], b[1], f)))
        break
    return out


def point_at(pts, k):
    return partial(pts, k)[-1]


def house(ctx, x, y, s, c, a=1.0):
    ctx.rectangle(x - 22 * s, y - 34 * s, 44 * s, 34 * s)
    rgba(ctx, c, a)
    ctx.fill()
    ctx.move_to(x - 28 * s, y - 32 * s)
    ctx.line_to(x, y - 56 * s)
    ctx.line_to(x + 28 * s, y - 32 * s)
    ctx.close_path()
    rgba(ctx, shade(c, 0.6), a)
    ctx.fill()
    ctx.rectangle(x - 6 * s, y - 18 * s, 12 * s, 18 * s)
    rgba(ctx, (1, 0.85, 0.45), 0.8 * a)
    ctx.fill()


def tick_badge(ctx, x, y, u, c):
    if u <= 0:
        return
    k = ease_out_back(clamp(u / 0.3))
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    circle(ctx, 0, 0, 30, c)
    line(ctx, [(-13, 0), (-3, 11), (15, -11)], (1, 1, 1), 7)
    ctx.restore()


# ============================================================ scene 1: the map

class MapScene(Cued):
    """Yarlung Tsangpo -> Great Bend -> Siang -> Brahmaputra; dam pin at the bend."""

    RIVER = [(-20, 520), (150, 500), (320, 530), (480, 500), (620, 515), (740, 490), (820, 440), (900, 420),
             (960, 460), (955, 520), (900, 590), (840, 650), (805, 730), (780, 820), (740, 900), (660, 960),
             (520, 985), (360, 1000), (200, 1020), (-20, 1035)]
    BORDER = [(-20, 700), (300, 690), (560, 712), (760, 702), (900, 668), (1100, 645)]
    DAM = (957, 505)
    BEND = 0.47   # share of the river length that is in Tibet (before the border)

    def beats(self, d):
        c = self.cue
        return {"china": c("CHINA", d * 0.3), "duniya": c("DUNIYA", d * 0.45), "brahma": c("BRAHMAPUTRA", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "whoosh"), (0.4, "beep"), (b["china"], "boom"), (b["china"] + 0.05, "thud"),
                (b["duniya"], "kaching"), (b["brahma"], "whoosh"), (b["brahma"] + 0.25, "pop")]

    def jolts(self, d):
        return [self.beats(d)["china"]]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        zoom = 1 + 0.05 * t / d
        ctx.save()
        ctx.translate(540, 700)
        ctx.scale(zoom, zoom)
        ctx.translate(-540, -700)
        ctx.rectangle(0, 0, W, H)   # India: green lowland
        rgba(ctx, hexc("#1F3A22"))
        ctx.fill()
        ctx.move_to(-20, 0)   # Tibet plateau above the border
        for p in self.BORDER:
            ctx.line_to(*p)
        ctx.line_to(1100, 0)
        ctx.close_path()
        g = cairo.LinearGradient(0, 200, 0, 700)
        g.add_color_stop_rgb(0, *shade(PLATEAU, 0.55))
        g.add_color_stop_rgb(1, *PLATEAU)
        ctx.set_source(g)
        ctx.fill()
        for i in range(7):   # Himalayan peaks along the border
            px, py = 60 + i * 150 + 30 * rnd(i, 51), 690 - 8 * i * rnd(i, 52)
            ctx.move_to(px - 60, py)
            ctx.line_to(px, py - 70 - 30 * rnd(i, 53))
            ctx.line_to(px + 60, py)
            ctx.close_path()
            rgba(ctx, shade(PLATEAU, 0.75), 0.9)
            ctx.fill()
        for i in range(20):   # contour flecks
            x, y = rnd(i, 54) * W, 760 + rnd(i, 55) * 320
            line(ctx, [(x, y), (x + 30, y - 4)], (1, 1, 1), 2, 0.05)
        # Namcha Barwa inside the bend
        ctx.move_to(845, 545)
        ctx.line_to(892, 470)
        ctx.line_to(935, 545)
        ctx.close_path()
        rgba(ctx, FOAM, 0.85)
        ctx.fill()
        text(ctx, "NAMCHA BARWA", 890, 568, 20, FOAM, font=MONO, a=0.7)
        ctx.set_dash([16, 12])
        line(ctx, self.BORDER, SAFFRON, 4, 0.85)
        ctx.set_dash([])
        text(ctx, "SEEMA", 140, 722, 24, SAFFRON, font=MONO, a=0.85)
        # the river draws itself in, then flows
        k = ease_in_out(clamp(t / 1.2))
        india_glow = clamp((t - b["brahma"]) / 0.4)
        river = partial(self.RIVER, k)
        if len(river) > 1:
            line(ctx, river, WATER_D, 22, 0.9)
            line(ctx, river, WATER, 10)
            if india_glow > 0:
                low = partial(self.RIVER, 1.0)[11:]
                line(ctx, low, WATER, 34, 0.25 * india_glow * (0.7 + 0.3 * math.sin(t * 8)))
                line(ctx, low, FOAM, 6, india_glow)
            for q in range(14):   # flow particles
                p = (q / 14 + t * 0.08) % 1
                if p < k:
                    x, y = point_at(self.RIVER, p)
                    circle(ctx, x, y, 4, FOAM, 0.8)
        a_lab = clamp((t - 0.6) / 0.4)
        text(ctx, "TIBET (CHINA)", 260, 452, 44, (1, 1, 1), font=CAPTION_FONT, bold=False, a=a_lab, stroke=(0, 0, 0),
             stroke_w=6)
        text(ctx, "YARLUNG TSANGPO", 330, 565, 24, FOAM, font=MONO, a=a_lab)
        text(ctx, "ARUNACHAL", 470, 820, 44, SAFFRON, font=CAPTION_FONT, bold=False, a=a_lab, stroke=(0, 0, 0),
             stroke_w=6)
        text(ctx, "SIANG", 720, 760, 24, FOAM, font=MONO, a=a_lab, anchor="r")
        text(ctx, "ASSAM", 300, 1075, 44, INDIA_GREEN, font=CAPTION_FONT, bold=False, a=a_lab, stroke=(0, 0, 0),
             stroke_w=6)
        text(ctx, "BRAHMAPUTRA", 470, 945, 26, FOAM, font=MONO, a=a_lab)
        # dam pin drops at the Great Bend
        u = t - b["china"]
        if u > 0:
            x, y = self.DAM
            fall = 1 - ease_out_back(clamp(u / 0.35))
            for r in range(3):
                ph = (u * 1.2 + r / 3) % 1
                ctx.arc(x, y, 20 + 140 * ph, 0, math.tau)
                rgba(ctx, CHINA_RED, 0.7 * (1 - ph))
                ctx.set_line_width(4)
                ctx.stroke()
            py = y - 220 * fall
            ctx.move_to(x, py)
            ctx.arc(x, py - 52, 30, math.pi * 0.8, math.pi * 0.2)
            ctx.close_path()
            rgba(ctx, CHINA_RED)
            ctx.fill()
            rrect(ctx, x - 13, py - 62, 26, 18, 3)   # little dam wall icon in the pin
            rgba(ctx, CONCRETE)
            ctx.fill()
            chip(ctx, "MEDOG", x - 46, py - 52, CHINA_RED, u - 0.25, size=30, anchor="r")
        ctx.restore()
        if t < b["china"]:
            stamp(ctx, 540, 300, t - 0.15, -0.02, 760, 150, SAFFRON, [("SEEMA KE PAAS", 4, 90, SAFFRON)])
        elif t < b["duniya"]:
            stamp(ctx, 540, 300, t - b["china"], 0.02, 700, 150, CHINA_RED, [("CHINA KA DAM", 4, 96, CHINA_RED)])
        else:
            stamp(ctx, 540, 300, t - b["duniya"], -0.02, 900, 190, GOLD,
                  [("DUNIYA KA SABSE BADA", -26, 80, GOLD), ("HYDROPOWER PROJECT", 50, 40, (1, 1, 1))])


# ============================================================ scene 2: size

def pylon(ctx, x, base, h, a):
    top = base - h
    for sgn in (-1, 1):
        line(ctx, [(x + sgn * h * 0.22, base), (x + sgn * 10, top)], (0.6, 0.7, 0.75), 4, a)
    for k in range(1, 6):
        y = lerp(base, top, k / 6)
        w = lerp(h * 0.22, 10, k / 6)
        line(ctx, [(x - w, y), (x + w, y)], (0.6, 0.7, 0.75), 3, a)
    for y, w in ((top + h * 0.12, h * 0.3), (top + h * 0.28, h * 0.24)):
        line(ctx, [(x - w, y), (x + w, y)], (0.6, 0.7, 0.75), 4, a)


class SizeScene(Cued):
    """Dollar counter, 60,000 MW chip, Three Gorges vs Medog bars (annual energy)."""

    BASE = 1040

    def beats(self, d):
        c = self.cue
        return {"dollar": c("BILLION", d * 0.12), "mw": c("60,000", d * 0.35), "tg": c("THREE GORGES", d * 0.6),
                "guna": c("3 GUNA", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        ev = [(0.02, "whoosh"), (b["dollar"] + 0.3, "kaching"), (b["mw"], "zap"), (b["tg"], "pop"),
              (b["guna"], "boom"), (b["guna"] + 0.1, "thud")]
        return ev + [(k * 0.08, "tick" if k % 2 else "tock") for k in range(int((b["dollar"] + 0.3) / 0.08))]

    def jolts(self, d):
        return [self.beats(d)["guna"]]

    def bar(self, ctx, x, h, c, label, val, a, t, live=False):
        top = self.BASE - h
        rrect(ctx, x - 120, top, 240, h, 18)
        g = cairo.LinearGradient(0, top, 0, self.BASE)
        g.add_color_stop_rgb(0, *shade(c, 1.15))
        g.add_color_stop_rgb(1, *shade(c, 0.55))
        ctx.set_source(g)
        ctx.fill()
        if live and h > 60:   # crackling bolts inside the big bar
            for i in range(3):
                y0 = top + 40 + i * (h - 80) / 3
                pts = [(x - 60 + 60 * j, y0 + 30 * math.sin(t * 30 + i * 3 + j * 2)) for j in range(3)]
                line(ctx, pts, (1, 1, 0.8), 4, 0.5 + 0.5 * math.sin(t * 40 + i))
        text(ctx, label, x, self.BASE - 36, 36, (1, 1, 1), font=CAPTION_FONT, bold=False, a=a, stroke=(0, 0, 0),
             stroke_w=5)
        if h > 40:
            big_readout(ctx, val, x, top - 56, 80, c, a)

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_sky(ctx, t)
        far_peaks(ctx, 1000, 260, 2.4, hexc("#0D2B3C"), drift=t * 8)
        for x in (90, 990):   # pylons and a sagging line between them
            pylon(ctx, x, 1060, 420, 0.35)
        ctx.move_to(90, 690)
        ctx.curve_to(400, 820, 680, 820, 990, 690)
        rgba(ctx, (0.6, 0.7, 0.75), 0.3)
        ctx.set_line_width(2)
        ctx.stroke()
        ctx.rectangle(0, self.BASE, W, H - self.BASE)
        rgba(ctx, NAVY)
        ctx.fill()
        line(ctx, [(60, self.BASE), (1020, self.BASE)], (1, 1, 1), 3, 0.5)
        if t < b["tg"]:
            roll = 167 * ease_out_cubic(clamp(t / (b["dollar"] + 0.3)))
            big_readout(ctx, f"${roll:.0f} BN", 540, 540, 190, GOLD)
            text(ctx, "~ 1.2 LAKH CRORE YUAN", 540, 670, 32, FOAM, font=MONO, a=clamp((t - b["dollar"]) / 0.3))
            chip(ctx, "60,000 MW", 540, 840, GOLD, t - b["mw"], size=64, sub="PLANNED CAPACITY")
            stamp(ctx, 540, 300, t - 0.1, -0.02, 640, 150, GOLD, [("KHARCHA?", 4, 100, GOLD)])
            return
        u = t - b["tg"]
        a = clamp(u / 0.25)
        text(ctx, "SAALANA BIJLI (ARAB UNIT)", 540, 1086, 30, FOAM, font=MONO, a=a)
        h_tg = 180 * ease_out_cubic(clamp(u / 0.4))
        h_md = 180 * ease_out_cubic(clamp(u / 0.4)) + 300 * ease_out_back(clamp((t - b["guna"]) / 0.5), 1.4)
        self.bar(ctx, 300, h_tg, hexc("#8A96A3"), "THREE GORGES", "~100", a, t)
        self.bar(ctx, 780, h_md, CHINA_RED, "MEDOG", "~300" if t > b["guna"] else "", a, t, live=t > b["guna"])
        if t > b["guna"]:
            stamp(ctx, 540, 300, t - b["guna"], 0.03, 600, 160, GOLD, [("~3X BIJLI!", 4, 110, GOLD)])


# ============================================================ scenes 3-4: the valley

GROUND_PTS = [(0, 560), (180, 600), (300, 650), (420, 720), (560, 800), (700, 880), (840, 930), (1080, 960)]
CN_DAM = 300
IN_DAM = 600
HOUSES = (790, 860, 930, 1000)


def ground_y(x):
    for (x0, y0), (x1, y1) in zip(GROUND_PTS, GROUND_PTS[1:]):
        if x <= x1:
            return lerp(y0, y1, (x - x0) / (x1 - x0))
    return GROUND_PTS[-1][1]


def valley_bg(ctx, t):
    night_sky(ctx, t)
    far_peaks(ctx, 700, 300, 0.7, hexc("#16384A"), drift=t * 5)
    far_peaks(ctx, 760, 180, 3.3, hexc("#0E2836"), drift=t * 11)


def valley_ground(ctx):
    ctx.move_to(0, H)
    for p in GROUND_PTS:
        ctx.line_to(*p)
    ctx.line_to(W, H)
    ctx.close_path()
    g = cairo.LinearGradient(0, 560, 0, 1150)
    g.add_color_stop_rgb(0, *EARTH)
    g.add_color_stop_rgb(1, *EARTH_D)
    ctx.set_source(g)
    ctx.fill()
    line(ctx, GROUND_PTS, shade(EARTH, 1.6), 4, 0.8)


def water_over(ctx, x0, x1, top_of, c, a):
    """Water body from x0 to x1 whose surface is top_of(x); the ground drawn afterwards hides what is under it."""
    xs = np.linspace(x0, x1, 60)
    ctx.move_to(x0, H)
    for x in xs:
        ctx.line_to(x, top_of(x))
    ctx.line_to(x1, H)
    ctx.close_path()
    rgba(ctx, c, a)
    ctx.fill()


def flood_over(ctx, level, x0, a):
    """Standing water above the ground wherever the ground is below `level`."""
    xs = np.linspace(x0, W, 60)
    ctx.move_to(x0, level)
    for x in xs:
        ctx.line_to(x, level)
    for x in xs[::-1]:
        ctx.line_to(x, max(level, ground_y(x)))
    ctx.close_path()
    rgba(ctx, WATER, a)
    ctx.fill()
    ctx.move_to(x0, level)
    for x in xs:
        ctx.line_to(x, level + 4 * math.sin(x * 0.05))
    rgba(ctx, FOAM, a)
    ctx.set_line_width(3)
    ctx.stroke()


def dam_wall(ctx, x, h, c, a=1.0, flag=None, gates=0.0):
    base = ground_y(x) + 10
    ctx.move_to(x - 30, base)
    ctx.line_to(x - 16, base - h)
    ctx.line_to(x + 16, base - h)
    ctx.line_to(x + 34, base)
    ctx.close_path()
    rgba(ctx, c, a)
    ctx.fill()
    for k in range(4):
        line(ctx, [(x - 14 + k * 9, base - h + 10), (x - 18 + k * 12, base - 6)], shade(c, 0.7), 2, a)
    if gates > 0:
        glow(ctx, x + 30, base - h * 0.35, 90, WATER, 0.8 * gates)
    if flag:
        line(ctx, [(x, base - h), (x, base - h - 60)], (0.9, 0.9, 0.9), 3, a)
        for k, fc in enumerate(flag):
            ctx.rectangle(x + 2, base - h - 60 + k * 12, 44, 12)
            rgba(ctx, fc, a)
            ctx.fill()


class KhatraScene(Cued):
    """Chinese dam high up the valley releases a surge; the Assam plain floods."""

    def beats(self, d):
        c = self.cue
        return {"chhoda": c("EK SAATH", d * 0.3), "baadh": c("BAADH", d * 0.55), "cm": c("ISILIYE", d * 0.7),
                "bomb": c("WATER BOMB", d * 0.88)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["chhoda"], "boom"), (b["chhoda"] + 0.1, "whoosh"),
                (b["chhoda"] + 0.4, "engine", 1.4), (b["baadh"], "alarm"), (b["baadh"] + 0.5, "alarm"),
                (b["cm"], "pick"), (b["bomb"], "boom"), (b["bomb"] + 0.05, "thud")]

    def jolts(self, d):
        b = self.beats(d)
        return [b["chhoda"], b["bomb"]]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        valley_bg(ctx, t)
        rel = clamp((t - b["chhoda"]) / 1.6)
        front = lerp(CN_DAM + 30, W + 40, ease_out_cubic(rel))
        level = lerp(500, 560, ease_in_out(rel))
        water_over(ctx, 0, CN_DAM, lambda x: level + 5 * math.sin(x * 0.04 + t * 2), WATER_D, 1)
        surge = rel > 0

        def surface(x):
            base = 10 + (36 if surge else 0) * clamp((front - x) / 200)
            bulge = 70 * math.exp(-((x - front + 40) / 90) ** 2) if surge and rel < 1 else 0
            return ground_y(x) - base - bulge + 3 * math.sin(x * 0.08 - t * 8)

        water_over(ctx, CN_DAM, min(W, front) if surge else W, surface, WATER, 0.95)
        valley_ground(ctx)
        dam_wall(ctx, CN_DAM, 190, CONCRETE, flag=(CHINA_RED, CHINA_RED), gates=clamp((t - b["chhoda"]) / 0.2) *
                 (1 - rel))
        text(ctx, "CHINA DAM", CN_DAM + 44, 500, 34, CHINA_RED, font=CAPTION_FONT, bold=False, anchor="l",
             stroke=(0, 0, 0), stroke_w=5)
        for hx in HOUSES:
            house(ctx, hx, ground_y(hx), 1.0, hexc("#C9A27A"))
        u_f = t - b["baadh"]
        if u_f > 0:
            flood_over(ctx, lerp(965, 850, ease_out_cubic(clamp(u_f / 1.2))), 560, 0.8)
            if math.sin(t * 14) > -0.3:
                chip(ctx, "FLOOD ALERT", 820, 640, RED, 1.0, size=40)
        text(ctx, "ARUNACHAL", 560, 900, 40, SAFFRON, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=5)
        text(ctx, "ASSAM", 930, 1040, 40, INDIA_GREEN, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=5)
        if surge and rel < 1:
            chip(ctx, "PAANI CHHODA!", 560, 640, WATER, t - b["chhoda"] - 0.1, size=32)
        if t < b["chhoda"]:
            stamp(ctx, 540, 300, t - 0.1, -0.02, 660, 150, RED, [("ASLI DAR?", 4, 110, RED)])
        elif t >= b["bomb"]:
            stamp(ctx, 540, 300, t - b["bomb"], 0.03, 860, 200, RED,
                  [("'WATER BOMB'", -24, 110, (1, 1, 1)), ("- ARUNACHAL CM KA BAYAAN", 56, 34, RED)])
        elif t >= b["baadh"]:
            stamp(ctx, 540, 300, t - b["baadh"], 0.02, 700, 150, RED, [("BAADH KA KHATRA", 4, 80, RED)])


class JawabScene(Cued):
    """India's proposed Siang Upper dam soaks up the surge; then the KHATRA / SIRF DAR scale."""

    def beats(self, d):
        c = self.cue
        return {"siang": c("SIANG", d * 0.12), "mw": c("11,000", d * 0.3), "buffer": c("BUFFER", d * 0.48),
                "aapke": c("AAPKE", d * 0.58), "khatra": c("KHATRA HAI", d * 0.68), "dar": c("SIRF DAR", d * 0.8),
                "cmt": c("COMMENT", d * 0.9)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "whoosh"), (b["siang"], "thud"), (b["siang"] + 0.1, "kaching"), (b["mw"], "zap"),
                (b["buffer"] - 0.6, "whoosh"), (b["buffer"], "pop"), (b["aapke"], "whoosh"),
                (b["khatra"], "soft_thud"), (b["dar"], "soft_thud"), (b["cmt"], "dingdong")]

    def scale(self, ctx, t, b):
        u = t - b["aapke"]
        if t < b["khatra"]:
            ang = 0.0
        elif t < b["dar"]:
            ang = 0.2 * ease_out_back(clamp((t - b["khatra"]) / 0.4))
        elif t < b["cmt"]:
            ang = lerp(0.2, -0.2, ease_out_back(clamp((t - b["dar"]) / 0.4)))
        else:   # keeps rocking: the viewer decides
            ang = -0.2 * math.cos((t - b["cmt"]) * 5) * math.exp(-(t - b["cmt"]) * 0.6)
        px, py, half = 540, 520, 330
        k = ease_out_cubic(clamp(u / 0.35))
        ctx.save()
        ctx.translate(0, 80 * (1 - k))
        rrect(ctx, px - 14, py, 28, 460, 8)   # stand
        rgba(ctx, CONCRETE, k)
        ctx.fill()
        rrect(ctx, px - 140, py + 450, 280, 30, 12)
        rgba(ctx, CONCRETE, k)
        ctx.fill()
        ends = [(px - half * math.cos(ang), py + half * math.sin(ang)),
                (px + half * math.cos(ang), py - half * math.sin(ang))]
        line(ctx, ends, CONCRETE, 16, k)
        circle(ctx, px, py, 22, GOLD, k)
        for (ex, ey), name, c in zip(ends, ("KHATRA", "SIRF DAR"), (RED, WATER)):
            line(ctx, [(ex, ey), (ex - 110, ey + 220)], CONCRETE, 3, k)
            line(ctx, [(ex, ey), (ex + 110, ey + 220)], CONCRETE, 3, k)
            ctx.move_to(ex - 140, ey + 220)
            ctx.curve_to(ex - 120, ey + 300, ex + 120, ey + 300, ex + 140, ey + 220)
            ctx.close_path()
            rgba(ctx, c, 0.9 * k)
            ctx.fill()
            text(ctx, name, ex, ey + 180, 56, (1, 1, 1), font=CAPTION_FONT, bold=False, a=k, stroke=(0, 0, 0),
                 stroke_w=7)
        ctx.restore()
        text(ctx, "AAPKA FAISLA?", 540, 300, 96, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
             stroke_w=9, a=clamp(u / 0.2))
        if t > b["cmt"]:
            pop = ease_out_back(clamp((t - b["cmt"]) / 0.35))
            ctx.save()
            ctx.translate(540, 1080)
            ctx.scale(pop, pop)
            rrect(ctx, -330, -52, 660, 104, 52)
            rgba(ctx, GOLD)
            ctx.fill()
            text(ctx, "KHATRA YA DAR? COMMENT", 0, 2, 48, (0.05, 0.05, 0.05), font=CAPTION_FONT, bold=False)
            ctx.restore()

    def draw(self, ctx, t, d):
        b = self.beats(d)
        valley_bg(ctx, t)
        if t >= b["aapke"]:
            ctx.rectangle(0, 0, W, H)
            rgba(ctx, NAVY, 0.55)
            ctx.fill()
            self.scale(ctx, t, b)
            return
        rise = ease_out_back(clamp((t - b["siang"]) / 0.45), 1.4)
        fill = ease_in_out(clamp((t - (b["buffer"] - 0.6)) / 0.9))
        water_over(ctx, 0, CN_DAM, lambda x: 520 + 5 * math.sin(x * 0.04 + t * 2), WATER_D, 1)
        water_over(ctx, CN_DAM, IN_DAM, lambda x: ground_y(x) - 10 + 3 * math.sin(x * 0.08 - t * 8), WATER, 0.95)
        if rise > 0.3:   # India's reservoir behind its wall, rising as it soaks up the surge
            lvl = lerp(760, 690, fill)
            water_over(ctx, 420, IN_DAM, lambda x: lvl + 4 * math.sin(x * 0.05 + t * 2), WATER_D, clamp(rise))
        water_over(ctx, IN_DAM, W, lambda x: ground_y(x) - 8 + 2 * math.sin(x * 0.08 - t * 6), WATER, 0.9)
        valley_ground(ctx)
        dam_wall(ctx, CN_DAM, 190, CONCRETE, flag=(CHINA_RED, CHINA_RED))
        text(ctx, "CHINA DAM", CN_DAM + 44, 500, 30, CHINA_RED, font=CAPTION_FONT, bold=False, anchor="l",
             stroke=(0, 0, 0), stroke_w=5)
        if rise > 0:
            dam_wall(ctx, IN_DAM, 150 * rise, CONCRETE, flag=(SAFFRON, (1, 1, 1), INDIA_GREEN))
            chip(ctx, "SIANG UPPER", IN_DAM, 560, INDIA_GREEN, t - b["siang"] - 0.2, size=34, sub="PRASTAVIT / PLANNED")
            chip(ctx, "~11,000 MW", IN_DAM + 250, 660, GOLD, t - b["mw"], size=34)
        if fill > 0:
            chip(ctx, "BUFFER", 500, 860, WATER, t - b["buffer"], size=40)
        for i, hx in enumerate(HOUSES):
            house(ctx, hx, ground_y(hx), 1.0, hexc("#C9A27A"))
            tick_badge(ctx, hx, ground_y(hx) - 90, t - b["buffer"] - 0.15 * i, INDIA_GREEN)
        text(ctx, "ASSAM", 930, 1040, 40, INDIA_GREEN, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=5)
        if t < b["siang"]:
            stamp(ctx, 540, 300, t - 0.05, -0.02, 740, 150, INDIA_GREEN, [("BHARAT KA JAWAAB?", 4, 80, INDIA_GREEN)])
        else:
            stamp(ctx, 540, 300, t - b["siang"], 0.02, 820, 160, SAFFRON, [("SIANG UPPER PROJECT", 4, 76, SAFFRON)])


SCENE_CLASSES = {"bomb": MapScene, "size": SizeScene, "khatra": KhatraScene, "jawab": JawabScene}


# ============================================================ compositor ("water watch")

def header(ctx, idx, t_global):
    drop(ctx, 84, 104, 1.1, WATER)
    text(ctx, "REALITY SHIFT", 128, 90, 34, (1, 1, 1), a=0.92, anchor="l")
    text(ctx, "WATER WATCH // BRAHMAPUTRA", 128, 124, 22, WATER, font=MONO, a=0.85, anchor="l")
    # tank gauge: fills a quarter per scene, wavy surface
    x, y, w, h = W - 190, 70, 130, 64
    rrect(ctx, x, y, w, h, 12)
    rgba(ctx, (0, 0, 0), 0.5)
    ctx.fill()
    lvl = y + h - h * (idx + 1) / len(SPEC)
    ctx.save()
    rrect(ctx, x, y, w, h, 12)
    ctx.clip()
    ctx.move_to(x, y + h)
    for k in range(21):
        xx = x + w * k / 20
        ctx.line_to(xx, lvl + 4 * math.sin(xx * 0.12 + t_global * 6))
    ctx.line_to(x + w, y + h)
    ctx.close_path()
    rgba(ctx, SPEC[idx]["accent"], 0.9)
    ctx.fill()
    ctx.restore()
    rrect(ctx, x, y, w, h, 12)
    rgba(ctx, (1, 1, 1), 0.8)
    ctx.set_line_width(3)
    ctx.stroke()
    text(ctx, f"LVL {idx + 1}/{len(SPEC)}", x - 16, y + h / 2, 26, (1, 1, 1), font=MONO, a=0.9, anchor="r")


def caption(ctx, sc, tl, accent):
    """Navy strip with a wave crest in the scene accent; wipes in left-to-right."""
    cur = None
    for i, (start, _) in enumerate(sc["captions"]):
        if tl >= start - 0.03:
            cur = i
    if cur is None:
        return
    start, cap = sc["captions"][cur]
    u = tl - start + 0.03
    k = ease_out_cubic(clamp(u / 0.2))
    size = 80
    words_ = cap.split(" ")
    ws = [text_width(ctx, w, size, font=CAPTION_FONT, bold=False) for w in words_]
    gap = size * 0.26
    tw = sum(ws) + gap * (len(ws) - 1)
    fit = min(1.0, 880 / tw)
    cy = (CAP_TOP + CAP_BOTTOM) / 2
    pad = 46
    hh = size * 0.74
    ctx.save()
    ctx.translate(W / 2, cy)
    ctx.scale(fit, fit)
    x0 = -tw / 2 - pad
    full = tw + 2 * pad
    ctx.rectangle(x0 - 20, -hh - 40, (full + 40) * k, 2 * hh + 80)
    ctx.clip()
    rrect(ctx, x0, -hh, full, 2 * hh, 14)
    rgba(ctx, NAVY, 0.94)
    ctx.fill()
    ctx.move_to(x0, -hh + 4)   # wave crest on the top edge
    for j in range(41):
        xx = x0 + full * j / 40
        ctx.line_to(xx, -hh - 6 + 7 * math.sin(xx * 0.06 + tl * 9))
    ctx.line_to(x0 + full, -hh + 10)
    ctx.line_to(x0, -hh + 10)
    ctx.close_path()
    rgba(ctx, accent, 0.95)
    ctx.fill()
    x = -tw / 2
    for w, ww in zip(words_, ws):
        c = HOT.get(w.strip(PUNCT + ".").split("-")[0], (1, 1, 1))
        text(ctx, w, x, 4, size, c, font=CAPTION_FONT, bold=False, anchor="l", stroke=(0, 0, 0), stroke_w=8)
        x += ww + gap
    ctx.restore()


def water_wipe(ctx, tl):
    """Rising-water cut: a wall of water with a foamy crest sweeps up and off the frame."""
    if tl >= 0.4:
        return
    k = ease_in_out(tl / 0.4)
    y_crest = lerp(H * 0.2, -200, k)
    ctx.move_to(0, H)
    for j in range(41):
        x = W * j / 40
        ctx.line_to(x, y_crest + 30 * math.sin(x * 0.012 + tl * 20))
    ctx.line_to(W, H)
    ctx.close_path()
    rgba(ctx, WATER_D, 0.9 * (1 - k * 0.6))
    ctx.fill()
    for j in range(41):
        x = W * j / 40
        circle(ctx, x, y_crest + 30 * math.sin(x * 0.012 + tl * 20), 8, FOAM, 0.8 * (1 - k))


def compose(idx, tl):
    sc = engine.SCENES[idx]
    spec = SPEC[idx]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    shake = 8 * max(0.0, 1 - tl / 0.3)
    for ts in (getattr(sc["obj"], "jolts", lambda _d: [])(sc["dur"])):
        shake += 12 * max(0.0, 1 - (tl - ts) / 0.3) * (tl >= ts)
    ctx.save()
    ctx.translate(shake * math.sin(tl * 83), shake * math.cos(tl * 67))
    sc["obj"].draw(ctx, tl, sc["dur"])
    ctx.restore()
    vignette(ctx)
    g = cairo.LinearGradient(0, 0, 0, 200)
    g.add_color_stop_rgba(0, 0.01, 0.04, 0.07, 0.9)
    g.add_color_stop_rgba(1, 0.01, 0.04, 0.07, 0.0)
    ctx.rectangle(0, 0, W, 200)
    ctx.set_source(g)
    ctx.fill()
    g = cairo.LinearGradient(0, CAP_TOP - 60, 0, UI_CLEAR)
    g.add_color_stop_rgba(0, 0.01, 0.04, 0.07, 0.0)
    g.add_color_stop_rgba(1, 0.01, 0.04, 0.07, 0.92)
    ctx.rectangle(0, CAP_TOP - 60, W, UI_CLEAR - CAP_TOP + 60)
    ctx.set_source(g)
    ctx.fill()
    ctx.rectangle(0, UI_CLEAR, W, H - UI_CLEAR)
    rgba(ctx, (0.01, 0.04, 0.07), 0.92)
    ctx.fill()
    header(ctx, idx, sc["start"] + tl)
    caption(ctx, sc, tl, spec["accent"])
    if idx:
        water_wipe(ctx, tl)
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
        "China Ka 'Water Bomb'? Brahmaputra Pe Duniya Ka Sabse Bada Dam!",
        "China Ka 'Water Bomb'? Brahmaputra Pe Mega Dam 🇮🇳",
        "Brahmaputra Pe China Ka Mega Dam: Bharat Ke Liye Khatra?",
        "Three Gorges Se 3 Guna Bada! China Ka Brahmaputra Dam",
        "China Ka Medog Dam: Arunachal Aur Assam Ko Kya Khatra?",
        "Brahmaputra Dam vs Siang Upper Project: Bharat Ka Jawab",
        "$167 Billion Ka Dam, Bharat Ki Seema Ke Paas!",
        "China Ka Brahmaputra Dam: Khatra Ya Sirf Dar?",
    ],
    "thumb_text": "WATER BOMB?",
    "queries": ["brahmaputra dam", "china dam brahmaputra", "medog dam"],
    "description": """
China ne Brahmaputra (Tibet me Yarlung Tsangpo) par Medog dam, yaani duniya ka sabse bada hydropower project shuru kiya hai, Bharat ki seema ke paas. Arunachal ke CM ne ise 'water bomb' kaha. Kya ye sach me khatra hai? Aur Bharat ka jawab kya hai?

Is Short me:
• Medog / Yarlung Tsangpo lower reaches project: construction 19 July 2025 ko shuru (Great Bend, Arunachal border ke paas)
• Kharcha: ~1.2 trillion yuan (~$167 billion, Xinhua ke mutabik)
• Planned capacity ~60,000 MW, ~300 arab unit bijli saal ki, yaani Three Gorges se karib 3 guna
• Asli chinta: achanak chhoda gaya paani (baadh) aur river data; China ka kehna hai downstream deshon se baat-cheet jaari rahegi
• Bharat ka jawab: Siang Upper Multipurpose Project (~11,000 MW, arabon ghan metre ka buffer), abhi prastavit / survey stage par

Aapke hisaab se ye dam Bharat ke liye khatra hai ya sirf dar? Comment karo.
Aisi aur defence aur geopolitics ke liye Reality Shift ko subscribe karo.

Note: map aur graphics schematic hain, scale par nahi. Baadh ka scene ek sambhavit khatre ko samjhane ke liye hai, kisi asli ghatna ka nahi.
""",
    "tags": ["brahmaputra dam", "china dam brahmaputra", "medog dam", "yarlung tsangpo dam", "water bomb",
             "siang upper project", "arunachal pradesh", "assam flood", "india china water war", "three gorges dam",
             "china mega dam", "geopolitics hindi", "india china", "defence shorts hindi", "reality shift"],
    "hashtags": ["#Shorts", "#Brahmaputra", "#IndiaChina"],
}


def thumbnail(ctx):
    """1080x1920 cover: WATER BOMB? over the valley with the Chinese dam bursting a surge toward Assam."""
    ctx.rectangle(0, 0, W, H)
    rgba(ctx, SKY_TOP)
    ctx.fill()
    ctx.save()   # valley sits in the middle third, under the headline
    ctx.translate(0, 380)
    valley_bg(ctx, 0.3)
    water_over(ctx, 0, CN_DAM, lambda x: 500 + 5 * math.sin(x * 0.04), WATER_D, 1)
    water_over(ctx, CN_DAM, W, lambda x: ground_y(x) - 46 - 90 * math.exp(-((x - 640) / 140) ** 2), WATER, 0.95)
    valley_ground(ctx)
    for hx in HOUSES:
        house(ctx, hx, ground_y(hx), 1.0, hexc("#C9A27A"))
    flood_over(ctx, 880, 560, 0.75)
    dam_wall(ctx, CN_DAM, 190, CONCRETE, flag=(CHINA_RED, CHINA_RED), gates=1.0)
    glow(ctx, 640, 820, 380, FOAM, 0.35)
    ctx.restore()
    g = cairo.LinearGradient(0, 0, 0, 700)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.92)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 700)
    ctx.set_source(g)
    ctx.fill()
    vignette(ctx)
    glow(ctx, 540, 330, 600, RED, 0.2)
    text(ctx, "WATER", 540, 230, 220, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "BOMB?", 540, 450, 220, RED, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    rrect(ctx, 170, 1440, 740, 120, 30)
    rgba(ctx, (0, 0, 0), 0.82)
    ctx.fill_preserve()
    rgba(ctx, WATER)
    ctx.set_line_width(6)
    ctx.stroke()
    text(ctx, "CHINA vs BRAHMAPUTRA", 540, 1500, 64, (1, 1, 1), font=CAPTION_FONT, bold=False)
    text(ctx, "REALITY SHIFT", 540, 1780, 40, (1, 1, 1), a=0.7)


def main() -> None:
    import upload_kit
    story = importlib.import_module("generate_brahmaputra_dam_short")  # named module: work files land in work/<name>/
    engine.make_frame = story.make_frame
    final = engine.render(story, "edge")
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
