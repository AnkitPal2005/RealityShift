"""Reality Shift Short: Longewala 1971 - 120 jawans held a post against a tank column till the Hunters came (Ek Jung Ek Raaz, 26 Nov 2026).

Facts (see SOURCES): on the night of 4-5 Dec 1971 about 120 men of A Company, 23 Punjab under Major Kuldip Singh
Chandpuri held the Longewala post (Thar desert, Rajasthan) against a Pakistani armoured column of roughly 40-45 tanks
(sources give 40-65); Chandpuri was given the choice to withdraw and chose to stay; the column halted at the wire,
fearing a minefield; the post held through the night; at first light IAF Hunters from Jaisalmer attacked and
destroyed many tanks and vehicles. Chandpuri got the Maha Vir Chakra. The army-vs-air-force credit question is a
long-running, open debate (no person attacked).
Not used: exact tank kill counts (sources differ), any film details.
Debate: "Jeet jawanon ki thi ya Air Force ki?"
Format: 9:16, ~26 s, 6 scenes; conflict in line 1, the turn (withdraw allowed) in line 2.
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

from core import delivery, engine, lego
from core.engine import *  # noqa: F401,F403
from shorts.chabahar import Cued
from shorts.reality_shift import flag
from shorts.akashteer import soldier, ell
from shorts.marut import tank, sandbags
from shorts.nyoma import jet
from shorts.reality_shift_weapons import fireball
from shorts.haji_pir import chip, stamp

TOPIC = "LONGEWALA 1971 - 120 JAWAN VS TANK, JEET KISKI"
OUTPUTS = {"edge": "longewala_short.mp4"}
LEGO = {"header": "intel", "caption": "chip", "transition": "shutter", "palette": "khaki", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.45            # natural breaths, no speed-up (user, 25 Nov)
TAIL_PAD = 0.35
TRIM = {"thresh": 0.006, "keep": 0.04, "keep_tail": 0.06}
MUSIC_BPM = 88           # >= 6 away from Haji Pir (100)
MUSIC_STYLE = "pulse"    # haji_pir march, k9 tension
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 0
MAX_SECONDS = 35.0

PAL = lego.PALETTES["khaki"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
WHITE = (1.0, 1.0, 1.0)
GOLD = hexc("#FFD166")
RED = hexc("#E2483A")
CYAN = hexc("#5FD3FF")
GREY = hexc("#8A8F96")
STEEL = hexc("#9AA3AC")
GROUND = 1040
POST_X = 230

SOURCES = [
    "Wikipedia - Battle of Longewala: https://en.wikipedia.org/wiki/Battle_of_Longewala",
    "Wikipedia - Kuldip Singh Chandpuri (Maha Vir Chakra): https://en.wikipedia.org/wiki/Kuldip_Singh_Chandpuri",
    "Indian Air Force history - Battle of Longewala, Hunters from Jaisalmer (IAF official history pages)",
]

SPEC = [
    {"key": "hook", "accent": RED, "text": "",
     "visual": "Night desert: a small sandbag post with a few jawans on the left; a long line of tank headlights rolls "
               "in from the right; 120 JAWAN vs 45 TANK chips; then a radio chip PEECHHE HATO?",
     "vo": [("hook", [("उस रात एक सौ बीस जवानों के सामने", "US RAAT 120 JAWANON KE SAAMNE"),
                      ("करीब पैंतालीस टैंक खड़े थे।", "KAREEB 45 TANK KHADE THE")]),
            ("tell", [("और उन्हें चौकी छोड़कर", "AUR UNHEN CHAUKI CHHODKAR"),
                      ("पीछे हटने की छूट दी गई थी।", "PEECHHE HATNE KI CHHOOT DI GAYI THI")])]},
    {"key": "faisla", "accent": SAFFRON, "text": "",
     "visual": "Close on the commander (beret) behind the sandbags; he raises a fist; the tricolour flutters behind him",
     "vo": [("punch", [("पर मेजर कुलदीप सिंह चांदपुरी बोले", "PAR MAJOR KULDIP SINGH CHANDPURI BOLE"),
                       ("हम यहीं रुकेंगे।", "HUM YAHIN RUKENGE")])]},
    {"key": "surang", "accent": GOLD, "text": "",
     "visual": "4 DEC 1971 LONGEWALA chip; tanks crawl left toward a barbed-wire line; a MINES? chip pulses and the "
               "tanks stop",
     "vo": [("tell", [("चार दिसंबर उन्नीस सौ इकहत्तर की रात", "4 DECEMBER 1971 KI RAAT"),
                      ("लोंगेवाला की रेत में।", "LONGEWALA KI RET MEIN")]),
            ("build", [("दुश्मन के टैंकों को लगा", "DUSHMAN KE TANKON KO LAGA"), ("आगे बारूदी सुरंग है", "AAGE BAROODI SURANG HAI"),
                       ("और वो रुक गए।", "AUR WO RUK GAYE")])]},
    {"key": "raat", "accent": CYAN, "text": "",
     "visual": "All night: shells burst around the post again and again; the flag never falls; the sky slowly lightens",
     "vo": [("build", [("पूरी रात गोले बरसते रहे", "POORI RAAT GOLE BARASTE RAHE"),
                       ("पर चौकी नहीं गिरी।", "PAR CHAUKI NAHIN GIRI")])]},
    {"key": "subah", "accent": INDIA_GREEN, "text": "",
     "visual": "Dawn breaks over the dunes; two Hunter jets dive in from the top right toward the halted tanks",
     "vo": [("build", [("सुबह होते ही", "SUBAH HOTE HI"), ("वायु सेना के हंटर विमान आए।", "VAYU SENA KE HUNTER VIMAAN AAYE")])]},
    {"key": "jalna", "accent": RED, "text": "",
     "visual": "Low over the dunes: the tanks burst into fire one by one as the jets pull up",
     "vo": [("punch", [("और रेत में टैंक", "AUR RET MEIN TANK"), ("एक एक करके जलने लगे।", "EK EK KARKE JALNE LAGE")])]},
    {"key": "debate", "accent": SAFFRON, "text": "",
     "visual": "A jawan at the post with the flag and a jet passing overhead; the poll asks JAWAN YA AIR FORCE",
     "vo": [("punch", [("तो लोंगेवाला की जीत", "TO LONGEWALA KI JEET"), ("जवानों की थी", "JAWANON KI THI"),
                       ("या वायु सेना की।", "YA VAYU SENA KI?")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "120": SAFFRON, "JAWANON": SAFFRON, "45": RED, "TANK": RED, "CHHOOT": GOLD, "PEECHHE": GOLD,
    "KULDIP": SAFFRON, "CHANDPURI": SAFFRON, "RUKENGE": INDIA_GREEN, "1971": GOLD, "LONGEWALA": GOLD,
    "BAROODI": RED, "SURANG": RED, "RUK": CYAN, "GOLE": RED, "NAHIN": INDIA_GREEN, "GIRI": INDIA_GREEN,
    "HUNTER": CYAN, "VAYU": CYAN, "JALNE": RED, "JEET": GOLD, "SENA": CYAN, "KI?": CYAN,
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".")] = HOT[_k]


def at(scene, key, frac, d):
    return scene.cue(key, frac * d)


def mixc(a, b, u):
    return tuple(p + (q - p) * clamp(u) for p, q in zip(a, b))


# ============================================================ scenery & props

def sand(ctx, t, night=1.0):
    """Thar dunes; night 1 = deep blue night with stars, 0 = warm dawn."""
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    for at_, cn, cd in ((0, "#050814", "#2B2448"), (0.55, "#101A33", "#B4566A"), (0.85, "#1C2238", "#F29E5C"),
                        (1, "#2A2A36", "#F7C77A")):
        g.add_color_stop_rgb(at_, *mixc(hexc(cd), hexc(cn), night))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    if night > 0.2:
        for i in range(70):
            circle(ctx, rnd(i, 3) * W, rnd(i, 4) * 700, 1.5 + 1.5 * rnd(i, 5), WHITE,
                   night * (0.4 + 0.4 * math.sin(t * 2 + i)))
        circle(ctx, 860, 260, 46, hexc("#E8ECF4"), 0.8 * night)
    if night < 0.8:
        glow(ctx, 780, 860, 320, hexc("#FFC46B"), 0.5 * (1 - night))
        circle(ctx, 780, 860, 70, hexc("#FFE0A0"), 0.95 * (1 - night))
    for layer, (base, amp, cd, cn) in enumerate(((860, 40, "#C98A58", "#2A2E44"), (950, 30, "#D9A066", "#343852"),
                                                (1030, 22, "#D9B27A", "#3E425C"))):
        ctx.move_to(0, H)
        for x in range(0, W + 30, 30):
            ctx.line_to(x, base + amp * math.sin(x * 0.006 + layer * 1.7) + 0.4 * amp * math.sin(x * 0.019))
        ctx.line_to(W, H)
        ctx.close_path()
        rgba(ctx, mixc(hexc(cd), hexc(cn), night))
        ctx.fill()
    for k in range(14):                                            # wind ripples on the near sand
        y = 1070 + k * 60 + 10 * rnd(k, 7)
        x0 = -40 + 120 * rnd(k, 8)
        pts = [(x, y + 8 * math.sin(x * 0.02 + k)) for x in range(int(x0), W + 40, 40)]
        line(ctx, pts, mixc(hexc("#B88B55"), hexc("#2A2E44"), night), 4, 0.5)


def post(ctx, t, x=POST_X, flag_on=True):
    """The Longewala post: sandbag wall, flag pole and tricolour."""
    if flag_on:
        line(ctx, [(x + 40, 1000), (x + 40, 640)], hexc("#C9C9C9"), 7)
        flag(ctx, x + 44, 680, 150, 96, "in", t)
    sandbags(ctx, x - 200, x + 160, 1070)


def headlights(ctx, x, y, s, a):
    glow(ctx, x - 140 * s, y - 70 * s, 90 * s, hexc("#FFF2B0"), 0.7 * a)
    circle(ctx, x - 135 * s, y - 75 * s, 9 * s, hexc("#FFF8D8"), a)


def column(ctx, t, advance, moving=True, night=1.0, wreck=None):
    """The tank column: five tanks facing left, spread back to the horizon."""
    slots = [(700, 1080, 0.62), (900, 1010, 0.5), (560, 960, 0.42), (1000, 930, 0.36), (780, 900, 0.3)]
    for i, (x0, y, s) in reversed(list(enumerate(slots))):
        x = x0 + 220 * (1 - advance) * s
        w = wreck[i] if wreck else 0.0
        tank(ctx, x, y, s, t, wreck=w, moving=moving and w == 0)
        if night > 0.3 and w == 0:
            headlights(ctx, x, y, s, night)


def wire(ctx, x, a=1.0):
    """Barbed-wire fence line across the sand."""
    for k in range(9):
        y = 900 + k * 24
        line(ctx, [(x - 30 + 6 * k, y), (x + 30 + 6 * k, y + 20)], hexc("#B0B4BA"), 3, a * 0.9)
    for y in range(880, 1110, 70):
        line(ctx, [(x, y), (x + 14, y + 60)], hexc("#7A6A52"), 6, a)


def jet_left(ctx, x, y, L, t, dive=0.0, burner=0.6):
    """A jet flying LEFT, upright (mirrored, never rotated by pi); dive > 0 noses down, < 0 pulls up."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(-1, 1)
    jet(ctx, 0, 0, L, dive, t, burner=burner, c=STEEL)
    ctx.restore()


def shell_bursts(ctx, t, rate=1.2):
    for i in range(6):
        u = (t * rate + rnd(i, 11)) % 1.6
        bx = POST_X + (rnd(i, 12) - 0.3) * 500 + 60 * math.floor(t * rate + rnd(i, 11))
        bx = 80 + (bx % 900)
        by = 980 + 80 * rnd(i, 13)
        if u < 0.7:
            fireball(ctx, bx, by, u, size=0.35, seed=i)


# ============================================================ scenes

class Hook(Cued):
    """Night: post with jawans vs a line of tank headlights; 120 vs 45 chips; withdraw allowed."""

    def events(self, d):
        return [(0.1, "boom"), (at(self, "45", 0.3, d), "thud"), (at(self, "CHHOOT", 0.7, d), "beep")]

    def draw(self, ctx, t, d):
        t45 = at(self, "45", 0.3, d)
        tc = at(self, "CHHOOT", 0.7, d)
        sand(ctx, t, 1.0)
        column(ctx, t, clamp(t / max(1.0, d)), night=1.0)
        post(ctx, t)
        soldier(ctx, POST_X - 110, GROUND - 10, 0.5, t, pose="binocs")
        soldier(ctx, POST_X + 90, GROUND - 10, 0.5, t, pose="stand", flip=True)
        chip(ctx, "120 JAWAN", 250, 330, SAFFRON, t / 0.4, size=58)
        chip(ctx, "~45 TANK", 800, 330, RED, (t - t45) / 0.4, size=58)
        chip(ctx, "PEECHHE HATO?", 540, 470, GOLD, (t - tc) / 0.4, size=50)


class Faisla(Cued):
    """The commander raises a fist behind the sandbags: HUM YAHIN RUKENGE."""

    def events(self, d):
        return [(at(self, "RUKENGE", 0.7, d), "thud")]

    def draw(self, ctx, t, d):
        tr = at(self, "RUKENGE", 0.7, d)
        sand(ctx, t, 1.0)
        glow(ctx, 540, 760, 360, SAFFRON, 0.18 + 0.1 * math.sin(t * 3))
        line(ctx, [(820, 1000), (820, 560)], hexc("#C9C9C9"), 8)
        flag(ctx, 824, 600, 200, 128, "in", t)
        soldier(ctx, 470, GROUND - 10, 0.74, t, pose="fist" if t >= tr - 0.2 else "stand", commander=True)
        sandbags(ctx, 120, 960, 1110)
        chip(ctx, "MAJ KULDIP SINGH CHANDPURI", 540, 300, WHITE, (t - 0.2) / 0.4, size=40)
        chip(ctx, "23 PUNJAB", 540, 400, SAFFRON, (t - 0.6) / 0.4, size=40)
        stamp(ctx, "HUM YAHIN RUKENGE", 540, 520, t - tr, c=INDIA_GREEN, size=60, ang=-0.08)


class Surang(Cued):
    """4 Dec 1971: tanks crawl to the wire; MINES? pulses; they stop."""

    def events(self, d):
        return [(0.1, "tick"), (at(self, "SURANG", 0.6, d), "alarm"), (at(self, "RUK", 0.85, d), "thud")]

    def draw(self, ctx, t, d):
        ts = at(self, "SURANG", 0.6, d)
        tr = at(self, "RUK", 0.85, d)
        stop_at = max(ts, 0.5)
        adv = clamp(t / stop_at)
        sand(ctx, t, 1.0)
        wire(ctx, 470)
        column(ctx, t, 0.4 + 0.6 * adv, moving=t < tr)
        post(ctx, t, x=110)
        chip(ctx, "4 DEC 1971", 540, 290, GOLD, t / 0.4, size=58)
        chip(ctx, "LONGEWALA, THAR", 540, 390, WHITE, (t - 0.3) / 0.4, size=40)
        if t >= ts:
            pulse = 1 + 0.08 * math.sin(t * 12)
            ctx.save()
            ctx.translate(470, 820)
            ctx.scale(pulse, pulse)
            chip(ctx, "MINES?", 0, 0, RED, (t - ts) / 0.3, size=64)
            ctx.restore()
        if t >= tr:
            chip(ctx, "STOP", 820, 760, CYAN, (t - tr) / 0.3, size=50)


class Raat(Cued):
    """Shells burst around the post all night; the flag stays up; the sky lightens."""

    def events(self, d):
        return [(0.05, "boom"), (0.9, "boom"), (at(self, "GIRI", 0.75, d), "shimmer")]

    def draw(self, ctx, t, d):
        tg = at(self, "GIRI", 0.75, d)
        sand(ctx, t, 1.0 - 0.35 * clamp(t / max(1.0, d)))
        column(ctx, t, 0.75, moving=False, night=0.8)
        shell_bursts(ctx, t)
        post(ctx, t)
        soldier(ctx, POST_X - 90, GROUND - 10, 0.5, t, pose="point", flip=False)
        soldier(ctx, POST_X + 110, GROUND - 10, 0.5, t, pose="binocs", flip=True)
        if t >= tg:
            glow(ctx, POST_X + 110, 700, 200, GOLD, 0.4 * clamp((t - tg) / 0.5))
            chip(ctx, "CHAUKI NAHIN GIRI", 540, 330, INDIA_GREEN, (t - tg) / 0.4, size=54)


class Subah(Cued):
    """Dawn breaks; two Hunters dive in toward the halted column."""

    def events(self, d):
        return [(0.1, "shimmer"), (at(self, "HUNTER", 0.4, d), "whoosh")]

    def draw(self, ctx, t, d):
        th = at(self, "HUNTER", 0.4, d)
        sand(ctx, t, 1.0 - clamp(t / 0.9))
        column(ctx, t, 0.75, moving=False, night=max(0.0, 1.0 - t / 0.9))
        post(ctx, t)
        for k in range(2):
            u = clamp((t - th + 0.5 + 0.25 * k) / 1.6)
            if 0 < u < 1:
                jet_left(ctx, lerp(1250, -200, u), lerp(240 + 90 * k, 620 + 60 * k, u), 260, t,
                         dive=math.atan2(380, 1450))
        chip(ctx, "HUNTER", 540, 300, CYAN, (t - th) / 0.4, size=58)
        chip(ctx, "IAF  -  JAISALMER", 540, 400, WHITE, (t - th - 0.3) / 0.4, size=38)


SLOTS = [(700, 1080), (900, 1010), (560, 960), (1000, 930), (780, 900)]


class Jalna(Cued):
    """The tanks burst into fire one by one as the jets pull up."""

    def events(self, d):
        tj = at(self, "JALNE", 0.5, d)
        return [(max(0.05, tj - 0.8 + 0.3 * i), "boom") for i in range(4)]

    def draw(self, ctx, t, d):
        tj = at(self, "JALNE", 0.5, d)
        sand(ctx, t, 0.0)
        hits = [max(0.05, tj - 0.8 + 0.3 * i) for i in range(5)]
        column(ctx, t, 0.75, moving=False, night=0.0, wreck=[clamp((t - h) / 0.6) for h in hits])
        for i, h in enumerate(hits):
            x, y = SLOTS[i]
            fireball(ctx, x + 40, y - 40, t - h, size=0.5, seed=i)
        u = clamp(t / 1.2)
        if u < 1:
            jet_left(ctx, lerp(700, -250, u), lerp(560, 200, u), 240, t, dive=-0.35, burner=0.8)
        if t >= tj:
            chip(ctx, "EK EK KARKE", 540, 320, RED, (t - tj) / 0.4, size=58)


class Debate(Cued):
    """A jawan at the post, a jet overhead; poll JAWAN YA AIR FORCE."""

    def events(self, d):
        return [(0.1, "whoosh"), (at(self, "JAWANON", 0.5, d), "tick")]

    def draw(self, ctx, t, d):
        tq = at(self, "TO", 0.05, d)
        sand(ctx, t, 0.0)
        rgba(ctx, (0, 0, 0), 0.3)
        ctx.paint()
        u = clamp(t / 1.6)
        if u < 1:
            jet_left(ctx, lerp(1200, -200, u), 250, 220, t, burner=0.5)
        post(ctx, t, x=760)
        soldier(ctx, 300, GROUND - 10, 0.68, t, pose="fist")
        lego.ending(sys.modules[__name__], ctx, t, t - tq, t - tq - 0.8,
                    question=("LONGEWALA KI JEET", "KISKI?"), options=("JAWAN", "AIR FORCE"), y=560)


SCENE_CLASSES = {"hook": Hook, "faisla": Faisla, "surang": Surang, "raat": Raat, "subah": Subah, "jalna": Jalna,
                 "debate": Debate}


def write_alignment(final: Path) -> None:
    out = [
        {"scene": spec["key"], "start": round(s["start"], 3), "dur": round(s["dur"], 3),
         "words": [{"t": round(s["start"] + st, 3), "w": w} for st, w in s["captions"]]}
        for spec, s in zip(SPEC, engine.SCENES)
    ]
    path = final.with_suffix(".json")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Alignment: {path}")


UPLOAD = {
    "titles": [
        "120 Jawan vs 45 Tank: Longewala Ki Jeet Kiski Thi? #shorts",
        "Longewala 1971: Jawan Jeete Ya Air Force? #shorts",
        "Peeche Hatne Ki Chhoot Thi... Phir Bhi Nahi Hate #shorts",
    ],
    "title": "120 Jawan vs 45 Tank: Longewala Ki Jeet Kiski Thi? #shorts",
    "thumb_text": "120 VS 45 TANK",
    "queries": ["longewala", "battle of longewala", "longewala 1971"],
    "description": """Longewala 1971 ka sach: 120 jawan, saamne kareeb 45 tank - aur peeche hatne ki chhoot ke baad bhi chauki nahi chhodi.

Is Short mein:
- 4-5 December 1971 ki raat, Thar ke Longewala post par 23 Punjab ki A Company (kareeb 120 jawan)
- Saamne kareeb 40-45 tanks ka column (alag sources mein alag sankhya)
- Major Kuldip Singh Chandpuri ko peeche hatne ki chhoot thi - unhone ruk kar ladna chuna (Maha Vir Chakra)
- Tank wire par ruk gaye - unhe laga aage baroodi surang hai
- Subah hote hi Jaisalmer se IAF ke Hunter aaye aur tank ek ek karke jalne lage

Debate: Longewala ki jeet jawanon ki thi ya Vayu Sena ki? Dono ki bahaduri ko salaam - apni raay comment mein likho.

Sources:
- Wikipedia: Battle of Longewala
- Gallantry Awards (Govt of India): Kuldip Singh Chandpuri, MVC
- The Print: Battle of Longewala
- Indian Air Force: Battle of Longewala
""",
    "tags": ["longewala", "battle of longewala", "longewala 1971", "1971 war", "kuldip singh chandpuri",
             "23 punjab", "hawker hunter", "indian air force", "indian army history", "thar desert war",
             "reality shift", "defence shorts", "ek jung ek raaz"],
    "hashtags": ["#Shorts", "#Longewala", "#IndianArmy"],
    "pinned_comment": "Longewala 1971 ki jeet kiski thi - chauki na chhodne wale JAWANON ki ya subah aaye HUNTER "
                      "pilots ki? 🤔 Apni raay likho 👇 (JAWAN / AIR FORCE)",
}


def thumbnail(ctx):
    sand(ctx, 1.0, 0.6)
    column(ctx, 1.0, 0.7, moving=False, night=0.6, wreck=[0.8, 0, 0, 0.6, 0])
    fireball(ctx, 740, 1040, 0.35, size=0.6)
    post(ctx, 1.0)
    soldier(ctx, POST_X - 60, GROUND - 10, 0.66, 1.0, pose="fist", commander=True)
    jet_left(ctx, 760, 520, 300, 1.0, dive=0.25, burner=0.7)
    text(ctx, "120 JAWAN", 540, 205, 110, SAFFRON, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "VS 45 TANK", 540, 330, 116, RED, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "LONGEWALA 1971", 540, 1330, 110, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, PAL["ui"], a=0.85)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.longewala")
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
