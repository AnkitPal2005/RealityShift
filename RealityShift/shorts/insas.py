"""Reality Shift Short: INSAS - India's own rifle that the Army itself replaced (series "Hathiyar Jo Army Ne Chhode",
after Arjun tank; 24 Nov 2026).

Facts (see SOURCES): INSAS 5.56 mm, in service from the late 1990s; complaints in Kargil's cold of cracked
magazines and jamming; the 5.56 round reflects a wound-rather-than-kill doctrine; the Army now fields the AK-203
(made at Korwa, Amethi, by Indo-Russia Rifles) and the American SIG716; INSAS served roughly 25 years and was cheap
and fully indigenous.
Debate (no party, no person): "INSAS bekaar thi ya badnaam ki gayi?"
Format: 9:16, ~33 s, 6 scenes, spec callouts (rifle vs rifle, round vs round) - no exposition block.
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
from shorts.akashteer import ell, poly, soldier
from shorts.reality_shift import flag
from shorts.siachen import snow

TOPIC = "INSAS RIFLE - DESI RIFLE JISE ARMY NE HI BADAL DIYA"
OUTPUTS = {"edge": "insas_short.mp4"}
LEGO = {"header": "radar", "caption": "speech", "transition": "scan", "palette": "amber", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.30
TAIL_PAD = 0.12
TRIM = {"thresh": 0.006, "keep": 0.04, "keep_tail": 0.06}
MUSIC_BPM = 84            # >= 6 away from Marut 90 / Kaveri 98
MUSIC_STYLE = "ambient"   # chinese_comment pulse, marut tension, kaveri march
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 0
MAX_SECONDS = 45.0

PAL = lego.PALETTES["amber"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
WHITE = (1.0, 1.0, 1.0)
GOLD = hexc("#FFD166")
RED = hexc("#E2483A")
CYAN = hexc("#5FD3FF")
BLACK = hexc("#1E2024")
GUN = hexc("#2C3036")
GUN_HI = hexc("#4A5058")
FDE = hexc("#9A8360")
GROUND = 1120

SOURCES = [
    "Wikipedia - INSAS rifle (5.56 mm, inducted late 1990s; Kargil-era complaints of jamming and cracked magazines "
    "in extreme cold; being replaced by AK-203 and SIG716): https://en.wikipedia.org/wiki/INSAS",
    "ThePrint - SIG Sauer 716 rifles are a stopgap, AK-203 is the future rifle: https://theprint.in/opinion/sig-sauer-"
    "716-rifles-are-a-stopgap-ak-203-is-the-future-rifle-of-indian-armed-forces/2263620",
    "The Week, 1 Nov 2025 - AK-203, made at Korwa (Amethi) by Indo-Russia Rifles: https://www.theweek.in/magazine/"
    "theweek/specials/2025/11/01/ak-203-rifle-why-this-indo-russian-weapon-is-a-game-changer-for-the-army.html",
    "Republic - India's dual-rifle doctrine (AK-203 + SIG716): https://www.republicworld.com/defence/war-games/as-"
    "indias-infantry-shifts-to-a-dual-rifle-doctrine-how-ak-203-and-sig-716-redefine-firepower",
]

SPEC = [
    {"key": "hook", "accent": SAFFRON, "text": "",
     "visual": "Armoury: a jawan lays the INSAS into a crate and the lid slams; the rifle glows on the name",
     "vo": [("hook", [("भारत ने अपनी राइफल बनाई", "BHARAT NE APNI RIFLE BANAYI"),
                      ("और सेना ने ही", "AUR SENA NE HI"), ("उसे बदल दिया।", "USE BADAL DIYA")]),
            ("punch", [("नाम था इंसास।", "NAAM THA INSAS")])]},
    {"key": "kargil", "accent": CYAN, "text": "",
     "visual": "Kargil snow at night: a jawan shivers; rifle close-up, the magazine cracks and the action jams",
     "vo": [("build", [("करगिल की ठंड में", "KARGIL KI THAND MEIN"), ("इसकी मैगज़ीन चटकने", "ISKI MAGAZINE CHATAKNE"),
                       ("और जाम होने की", "AUR JAAM HONE KI"), ("शिकायतें आईं।", "SHIKAYATEIN AAYIN")])]},
    {"key": "round", "accent": RED, "text": "",
     "visual": "Spec callout: 5.56 round next to a bigger 7.62 round; a target board with a hit marker",
     "vo": [("tell", [("इसकी गोली छोटी थी", "ISKI GOLI CHHOTI THI"), ("जो दुश्मन को मारने से", "JO DUSHMAN KO MAARNE SE"),
                      ("ज़्यादा घायल करने के लिए", "ZYADA GHAYAL KARNE KE LIYE"), ("सोची गई थी।", "SOCHI GAYI THI")])]},
    {"key": "new", "accent": GOLD, "text": "",
     "visual": "Two new rifles slide in side by side: AK-203 with the tricolour (Amethi) and SIG716 with the US flag",
     "vo": [("tell", [("अब सैनिकों के हाथ में", "AB SAINIKON KE HAATH MEIN"), ("दो नई राइफलें हैं।", "DO NAYI RIFLEIN HAIN")]),
            ("punch", [("अमेठी में बनी", "AMETHI MEIN BANI"), ("ए के दो सौ तीन", "AK-203"),
                       ("और अमेरिका की", "AUR AMERICA KI"), ("सिग सात सौ सोलह।", "SIG 716")])]},
    {"key": "pride", "accent": INDIA_GREEN, "text": "",
     "visual": "Border post at dawn: jawans with INSAS on guard under the tricolour; a 25 SAAL ticker; DESI stamp",
     "vo": [("build", [("पर इंसास ने ही", "PAR INSAS NE HI"), ("करीब पच्चीस साल तक", "KAREEB 25 SAAL TAK"),
                     ("भारत की सरहद संभाली।", "BHARAT KI SARHAD SAMBHALI")]),
            ("punch", [("सस्ती थी", "SASTI THI"), ("और पूरी तरह देसी थी।", "AUR POORI TARAH DESI THI")])]},
    {"key": "debate", "accent": GOLD, "text": "",
     "visual": "The INSAS on a display stand under a spotlight; the poll card asks",
     "vo": [("ask", [("तो इंसास बेकार थी", "TO INSAS BEKAAR THI"), ("या बदनाम की गई।", "YA BADNAAM KI GAYI?")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "BHARAT": SAFFRON, "APNI": SAFFRON, "RIFLE": GOLD, "SENA": INDIA_GREEN, "BADAL": RED, "INSAS": SAFFRON,
    "KARGIL": CYAN, "THAND": CYAN, "MAGAZINE": RED, "CHATAKNE": RED, "JAAM": RED, "GOLI": GOLD, "CHHOTI": RED,
    "GHAYAL": RED, "NAYI": GOLD, "AMETHI": SAFFRON, "AK-203": GOLD, "AMERICA": CYAN, "SIG": CYAN, "716": CYAN,
    "25": GOLD, "SAAL": GOLD, "SARHAD": INDIA_GREEN, "SASTI": GOLD, "DESI": SAFFRON, "BEKAAR": RED,
    "BADNAAM": GOLD,
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".?")] = HOT[_k]


def at(scene, key, frac, d):
    return scene.cue(key, frac * d)


# ============================================================ props

def rifle(ctx, x, y, s, kind="insas", crack=0.0, jam=0.0, glow_c=None, t=0.0, ang=0.0):
    """Side-profile rifle, muzzle to +x. kind: insas (translucent straight mag, wooden-look furniture),
    ak203 (curved mag, black), sig716 (FDE handguard, optic). Balanced save/restore."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(s, s)
    if glow_c:
        glow(ctx, 0, 0, 360, glow_c, 0.35)
    body = GUN
    furn = hexc("#5A3A22") if kind == "insas" else (FDE if kind == "sig716" else BLACK)
    poly(ctx, [(-330, -20), (-170, -40), (-170, 30), (-330, 70), (-345, 30)], furn)           # stock
    poly(ctx, [(-175, -45), (60, -45), (60, 25), (-175, 25)], body)                         # receiver
    poly(ctx, [(60, -35), (230, -30), (230, 18), (60, 18)], furn if kind != "ak203" else BLACK)  # handguard
    line(ctx, [(230, -8), (360, -8)], BLACK, 16)                                           # barrel
    rrect(ctx, 352, -20, 30, 24, 4)
    rgba(ctx, GUN_HI)
    ctx.fill()
    poly(ctx, [(-110, 25), (-70, 25), (-90, 110), (-125, 105)], body)                       # pistol grip
    if kind == "ak203":                                                                     # curved mag
        ctx.move_to(-20, 25)
        ctx.curve_to(-10, 90, 30, 150, 80, 190)
        ctx.line_to(120, 165)
        ctx.curve_to(75, 130, 40, 80, 30, 25)
        ctx.close_path()
        rgba(ctx, BLACK)
        ctx.fill()
    else:
        poly(ctx, [(-30, 25), (25, 25), (35, 160), (-20, 160)],
             hexc("#C8B89A") if kind == "insas" else BLACK, 0.85 if kind == "insas" else 1.0)
        if kind == "insas":                                                                 # see-through mag rounds
            for k in range(5):
                rrect(ctx, -14, 40 + 22 * k, 34, 12, 4)
                rgba(ctx, GOLD, 0.6)
                ctx.fill()
    if kind == "sig716":                                                                    # optic on top
        rrect(ctx, -120, -100, 170, 46, 20)
        rgba(ctx, BLACK)
        ctx.fill()
        ctx.arc(55, -77, 22, 0, math.tau)
        rgba(ctx, CYAN, 0.6)
        ctx.fill()
    else:
        line(ctx, [(-150, -45), (-150, -75), (-60, -75)], BLACK, 10)                        # carry handle / sight
    if crack > 0:                                                                           # cracks on the magazine
        for k in range(4):
            u = clamp(crack * 4 - k)
            if u > 0:
                x0, y0 = -10 + 12 * k, 40 + 26 * k
                line(ctx, [(x0, y0), (x0 + 18 * u, y0 + 14 * u), (x0 + 6 * u, y0 + 30 * u)], RED, 5)
    if jam > 0:                                                                             # jam: smoke puff + red ring
        for k in range(4):
            u = (t * 0.9 + k / 4) % 1
            circle(ctx, -40 + 30 * math.sin(k + t), -60 - 120 * u, 20 + 26 * u, hexc("#D8D8D8"), 0.45 * (1 - u) * jam)
        ctx.arc(-50, -10, 70 + 6 * math.sin(t * 10), 0, math.tau)
        rgba(ctx, RED, 0.9 * jam)
        ctx.set_line_width(7)
        ctx.stroke()
    ctx.restore()


def bullet(ctx, x, y, s, length, width, c=GOLD):
    """A rifle round standing upright: brass case + copper tip."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -width / 2, -length * 0.65, width, length * 0.65, 6)
    rgba(ctx, c)
    ctx.fill()
    ctx.move_to(-width / 2 + 3, -length * 0.65)
    ctx.curve_to(-width / 2, -length * 0.85, -6, -length, 0, -length)
    ctx.curve_to(6, -length, width / 2, -length * 0.85, width / 2 - 3, -length * 0.65)
    ctx.close_path()
    rgba(ctx, hexc("#C86A3A"))
    ctx.fill()
    line(ctx, [(-width / 2, -10), (width / 2, -10)], hexc("#A88A3A"), 5)
    ctx.restore()


def label(ctx, s, x, y, size, c=WHITE):
    text(ctx, s, x, y, size, c, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=8)


def armoury(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    g.add_color_stop_rgb(0, *hexc("#2A2418"))
    g.add_color_stop_rgb(1, *hexc("#4A3E2A"))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    for r in range(3):                                                  # wall racks
        line(ctx, [(60, 260 + 150 * r), (1020, 260 + 150 * r)], hexc("#6A5A3A"), 10)
        for k in range(8):
            line(ctx, [(110 + 115 * k, 250 + 150 * r), (100 + 115 * k, 140 + 150 * r)], hexc("#1E2024"), 12, 0.8)
    glow(ctx, 540, 120, 300, hexc("#FFD08A"), 0.3)
    ctx.rectangle(0, 1000, W, GROUND)
    rgba(ctx, hexc("#3A3020"))
    ctx.fill()


def snowy(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    g.add_color_stop_rgb(0, *hexc("#0A1022"))
    g.add_color_stop_rgb(1, *hexc("#3A4A6A"))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    for k, (base, c) in enumerate(((760, "#5A6A8A"), (900, "#7A8AAA"))):
        ctx.move_to(-50, GROUND)
        for x in range(-50, W + 60, 60):
            ctx.line_to(x, base - 260 * abs(math.sin(x / 210 + k * 1.7)) * (0.6 + 0.4 * k))
        ctx.line_to(W + 50, GROUND)
        ctx.close_path()
        rgba(ctx, hexc(c))
        ctx.fill()
    ctx.rectangle(0, 1000, W, GROUND)
    rgba(ctx, hexc("#E8EEF8"))
    ctx.fill()


def dawn_post(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    g.add_color_stop_rgb(0, *hexc("#2A3A6A"))
    g.add_color_stop_rgb(0.6, *hexc("#F4A86A"))
    g.add_color_stop_rgb(1, *hexc("#F8D8A0"))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    glow(ctx, 820, 760, 160, hexc("#FFE0A0"), 0.7)
    circle(ctx, 820, 760, 70, hexc("#FFE8B0"))
    ctx.move_to(-50, GROUND)
    for x in range(-50, W + 60, 60):
        ctx.line_to(x, 880 - 90 * abs(math.sin(x / 260)))
    ctx.line_to(W + 50, GROUND)
    ctx.close_path()
    rgba(ctx, hexc("#5A4A3A"))
    ctx.fill()
    for k in range(7):                                                  # sandbag wall
        ell(ctx, 80 + 150 * k, 1000, 80, 34)
        rgba(ctx, hexc("#B89A6A"))
        ctx.fill()


# ============================================================ scenes

class Hook(Cued):
    """Armoury: the INSAS goes into a crate and the lid slams; then the rifle itself under a spotlight."""

    def events(self, d):
        return [(0.1, "whoosh"), (at(self, "BADAL", 0.45, d), "thud"), (at(self, "INSAS", 0.8, d), "pop")]

    def draw(self, ctx, t, d):
        tb = at(self, "BADAL", 0.45, d)
        tn = at(self, "INSAS", 0.8, d)
        if t < tn + 0.3:
            armoury(ctx, t)
            soldier(ctx, 260, GROUND, 0.9, t, pose="stand")
            lid = clamp((t - tb + 0.2) / 0.4)
            rrect(ctx, 520, 860, 460, 160, 10)                          # crate
            rgba(ctx, hexc("#6A5A3A"))
            ctx.fill()
            rifle(ctx, 750, 880 - 140 * (1 - clamp(t / max(0.6, tb))), 0.9, "insas", t=t)
            ctx.save()                                                  # lid swings shut
            ctx.translate(520, 860)
            ctx.rotate(-1.4 * (1 - lid))
            rrect(ctx, 0, -30, 460, 34, 8)
            rgba(ctx, hexc("#7A6A4A"))
            ctx.fill()
            ctx.restore()
        if t >= tn:
            ctx.push_group()
            g = cairo.RadialGradient(540, 620, 40, 540, 620, 800)
            g.add_color_stop_rgb(0, *hexc("#3A2A14"))
            g.add_color_stop_rgb(1, *hexc("#0A0804"))
            ctx.set_source(g)
            ctx.rectangle(0, 0, W, H)
            ctx.fill()
            rifle(ctx, 520, 620, 1.35, "insas", glow_c=SAFFRON, t=t)
            flag(ctx, 90, 220, 170, 104, "in", t)
            label(ctx, "INSAS", 540, 900, 130, SAFFRON)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(clamp((t - tn) / 0.3))


class Kargil(Cued):
    """Kargil night snow: shivering jawan, then the magazine cracks and the action jams."""

    def events(self, d):
        return [(0.1, "whoosh"), (at(self, "CHATAKNE", 0.4, d), "zap"), (at(self, "JAAM", 0.65, d), "thud")]

    def draw(self, ctx, t, d):
        tc = at(self, "CHATAKNE", 0.4, d)
        tj = at(self, "JAAM", 0.65, d)
        snowy(ctx, t)
        soldier(ctx, 230, GROUND, 0.82, t, pose="look_up")
        crack = clamp((t - tc) / 0.8)
        jam = clamp((t - tj) / 0.4)
        rifle(ctx, 640, 720, 1.05, "insas", crack=crack, jam=jam, t=t, ang=-0.05)
        if crack > 0:
            glow(ctx, 640, 800, 160, RED, 0.25 * crack)
        snow(ctx, t, 80, wind=1.6)


class Round(Cued):
    """Spec callout: 5.56 vs 7.62 rounds side by side, then a target board with a hit marker."""

    def events(self, d):
        return [(0.1, "pop"), (at(self, "GHAYAL", 0.6, d), "tick")]

    def draw(self, ctx, t, d):
        tg = at(self, "GHAYAL", 0.6, d)
        g = cairo.LinearGradient(0, 0, 0, GROUND)
        g.add_color_stop_rgb(0, *hexc("#1E1A14"))
        g.add_color_stop_rgb(1, *hexc("#3A3020"))
        ctx.set_source(g)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()
        u = ease_out_cubic(clamp(t / 0.6))
        bullet(ctx, 300, 760, 1.0 * u + 0.01, 300, 52)
        label(ctx, "5.56", 300, 830, 70, GOLD)
        label(ctx, "INSAS", 300, 910, 50, SAFFRON)
        u2 = ease_out_cubic(clamp((t - 0.4) / 0.6))
        bullet(ctx, 620, 760, 1.0 * u2 + 0.01, 400, 70)
        label(ctx, "7.62", 620, 830, 70, GOLD)
        label(ctx, "AK-203 / SIG", 620, 910, 46, CYAN)
        if t > tg:                                                      # target board with a marker
            k = clamp((t - tg) / 0.4)
            for r, c in ((150, WHITE), (110, RED), (70, WHITE), (30, RED)):
                circle(ctx, 920, 520, r * k, c, 0.9)
            circle(ctx, 960, 470, 10 * k, BLACK)
            ctx.arc(960, 470, 22, 0, math.tau)
            rgba(ctx, GOLD, k)
            ctx.set_line_width(5)
            ctx.stroke()


class New(Cued):
    """AK-203 (tricolour, Amethi) and SIG716 (US flag) slide in; jawans hold them."""

    def events(self, d):
        return [(0.1, "whoosh"), (at(self, "AK-203", 0.55, d), "kaching"), (at(self, "SIG", 0.8, d), "kaching")]

    def draw(self, ctx, t, d):
        ta = at(self, "AMETHI", 0.45, d)
        ts = at(self, "AUR AMERICA", 0.75, d)
        armoury(ctx, t)
        ka = ease_out_cubic(clamp((t - ta + 0.3) / 0.6))
        ks = ease_out_cubic(clamp((t - ts + 0.3) / 0.6))
        if t < ta - 0.3:
            soldier(ctx, 300, GROUND, 0.82, t, pose="point")
            soldier(ctx, 780, GROUND, 0.82, t, pose="stand", flip=True)
            label(ctx, "2", 540, 520, 220, GOLD)
            return
        rifle(ctx, lerp(-500, 520, ka), 420, 1.0, "ak203", glow_c=SAFFRON, t=t)
        if ka > 0.9:
            flag(ctx, 80, 300, 140, 86, "in", t)
            label(ctx, "AK-203  AMETHI", 540, 600, 60, SAFFRON)
        rifle(ctx, lerp(1600, 520, ks), 820, 1.0, "sig716", glow_c=CYAN, t=t)
        if ks > 0.9:
            flag(ctx, 860, 700, 140, 86, "us", t)
            label(ctx, "SIG716  USA", 540, 1000, 60, CYAN)


class Pride(Cued):
    """Dawn border post: jawans with INSAS under the tricolour; 25 SAAL; then SASTI + DESI stamps."""

    def events(self, d):
        return [(0.1, "whoosh"), (at(self, "25", 0.35, d), "pop"), (at(self, "DESI", 0.8, d), "thud")]

    def draw(self, ctx, t, d):
        t25 = at(self, "25", 0.35, d)
        ts = at(self, "SASTI", 0.65, d)
        td = at(self, "DESI", 0.8, d)
        dawn_post(ctx, t)
        flag(ctx, 520, 360, 200, 120, "in", t, pole=600)
        for k, x in enumerate((200, 860)):
            soldier(ctx, x, GROUND, 0.8, t, pose="stand", flip=k == 1)
        rifle(ctx, 300, 880, 0.55, "insas", t=t, ang=-1.2)
        rifle(ctx, 760, 880, 0.55, "insas", t=t, ang=-1.95)
        if t > t25:
            k = ease_out_back(clamp((t - t25) / 0.5))
            label(ctx, "25 SAAL", 540, 250, 120 * k + 1, GOLD)
        for tt, s, y, c in ((ts, "SASTI", 560, GOLD), (td, "DESI", 680, SAFFRON)):
            if t > tt:
                k = ease_out_back(clamp((t - tt) / 0.4))
                ctx.save()
                ctx.translate(540, y)
                ctx.rotate(-0.08)
                rrect(ctx, -190 * k, -60 * k, 380 * k + 1, 120 * k + 1, 14)
                rgba(ctx, c)
                ctx.set_line_width(8)
                ctx.stroke()
                ctx.restore()
                label(ctx, s, 540, y, 90 * k + 1, c)


class Debate(Cued):
    """The INSAS on a display stand under a spotlight; the poll asks."""

    def events(self, d):
        return [(0.15, "tick"), (at(self, "BADNAAM", 0.5, d), "pop")]

    def draw(self, ctx, t, d):
        tq = at(self, "TO INSAS", 0.05, d)
        g = cairo.RadialGradient(540, 300, 40, 540, 300, 1000)
        g.add_color_stop_rgb(0, *hexc("#3A2E1A"))
        g.add_color_stop_rgb(1, *hexc("#0A0804"))
        ctx.set_source(g)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()
        poly(ctx, [(440, 0), (640, 0), (900, 1100), (180, 1100)], hexc("#FFE0A0"), 0.08)
        rifle(ctx, 520, 1000, 0.9, "insas", glow_c=SAFFRON, t=t)
        lego.ending(sys.modules[__name__], ctx, t, t - tq, t - tq - 0.8, question=("INSAS BEKAAR THI", "YA BADNAAM?"),
                    options=("BEKAAR", "BADNAAM"), y=560)


SCENE_CLASSES = {"hook": Hook, "kargil": Kargil, "round": Round, "new": New, "pride": Pride, "debate": Debate}


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
        "INSAS Rifle: Bekaar Thi Ya Badnaam Ki Gayi? #shorts",
        "Desi INSAS Rifle Ko Army Ne Kyun Chhoda? AK-203 vs SIG716 #shorts",
        "INSAS Se AK-203 Tak: Army Ne Desi Rifle Kyun Badli? #shorts",
    ],
    "title": "INSAS Rifle: Bekaar Thi Ya Badnaam Ki Gayi? #shorts",
    "thumb_text": "BEKAAR YA BADNAAM?",
    "queries": ["insas rifle", "insas vs ak 203", "insas rifle kyun hataya"],
    "description": """INSAS rifle ka sach: Bharat ki apni rifle, jise Army ne hi badal diya. INSAS vs AK-203 aur SIG716 - INSAS rifle kyun hataya gaya?

Is Short mein:
- INSAS (5.56 mm) 1990s ke aakhir mein Army mein aayi
- Kargil ki thand mein magazine chatakne aur jam hone ki shikayatein aayi
- 5.56 goli "maarne se zyada ghayal karne" wali soch par bani thi
- Ab Army ke paas Amethi (Korwa) mein bani AK-203 aur America ki SIG716 hai
- Phir bhi INSAS ne kareeb 25 saal sarhad sambhali - sasti thi aur poori tarah desi thi

Debate: INSAS bekaar thi ya badnaam ki gayi? Apna jawab comment mein likho.

Sources:
- Wikipedia: INSAS rifle
- ThePrint: SIG716 stopgap, AK-203 future rifle
- The Week (Nov 2025): AK-203
- Republic: India's dual-rifle doctrine
""",
    "tags": ["insas rifle", "insas vs ak 203", "ak 203", "sig 716", "indian army rifle", "insas rifle problem",
             "kargil war", "indian army weapons", "make in india defence", "reality shift", "defence shorts",
             "amethi ak 203"],
    "hashtags": ["#Shorts", "#INSAS", "#IndianArmy"],
    "pinned_comment": "INSAS - bekaar thi ya badnaam ki gayi? 🤔 Apna jawab likho 👇 (BEKAAR / BADNAAM)",
}


def thumbnail(ctx):
    g = cairo.RadialGradient(540, 620, 40, 540, 620, 900)
    g.add_color_stop_rgb(0, *hexc("#3A2A14"))
    g.add_color_stop_rgb(1, *hexc("#0A0804"))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    rifle(ctx, 520, 720, 1.35, "insas", crack=1.0, glow_c=SAFFRON, t=1.0)
    flag(ctx, 90, 420, 170, 104, "in", 1.0)
    text(ctx, "INSAS", 540, 230, 150, SAFFRON, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "BEKAAR YA BADNAAM?", 540, 1300, 100, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, PAL["ui"], a=0.85)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.insas")
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
