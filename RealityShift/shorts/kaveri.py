"""Reality Shift Short: Kaveri engine - 37 years after India started its own jet engine, Tejas still flies on an
American one (sequel to HF-24 Marut, 24 Nov 2026).

Facts (see SOURCES): GTRE's Kaveri programme sanctioned 1989 for the LCA Tejas; it never reached the thrust Tejas
needs, so Tejas flies on the American GE F404 (Mk1A: F404-IN20); late F404 deliveries pushed back Tejas Mk1A
deliveries; only a handful of countries build fighter jet engines; a dry (non-afterburning) Kaveri derivative for the
Ghatak UCAV has been flown on an Il-76 flying testbed in Russia. Not used (not confirmed in a primary source): any
2026 afterburner-test date or a signed Safran deal.
Debate (no party, no person): "DRDO ki galti ya paison ki kami?" - institution vs funding.
Format: 9:16, ~34 s, 6 scenes, spec callouts instead of exposition (Marut lesson: no flat backstory at 0:15-0:20).
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
from shorts.akashteer import ell, poly, seg01
from shorts.reality_shift import flag
from shorts.tejas_mk1a import draw_tejas_fighter
from shorts.ghatak import draw_ghatak_drone
from shorts.marut import person, jet_engine, balance, sky, mach_gauge  # noqa: F401

TOPIC = "KAVERI ENGINE - 37 SAAL BAAD BHI TEJAS AMERICAN ENGINE PAR"
OUTPUTS = {"edge": "kaveri_short.mp4"}
LEGO = {"header": "intel", "caption": "typewriter", "transition": "shutter", "palette": "glacier", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.30
TAIL_PAD = 0.12
TRIM = {"thresh": 0.006, "keep": 0.04, "keep_tail": 0.06}
MUSIC_BPM = 98           # >= 6 away from Marut (90)
MUSIC_STYLE = "march"    # Marut tension, chinese_comment pulse
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 0
MAX_SECONDS = 45.0

PAL = lego.PALETTES["glacier"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
WHITE = (1.0, 1.0, 1.0)
GOLD = hexc("#FFD166")
RED = hexc("#E2483A")
CYAN = hexc("#5FD3FF")
FIRE = hexc("#FF6A1A")
STEEL = hexc("#8C969E")
STEEL_DK = hexc("#4F575E")
MONO = "Consolas"
GROUND = 1120

SOURCES = [
    "Wikipedia - GTRE GTX-35VS Kaveri (programme sanctioned 1989 for the LCA; fell short of required thrust; Tejas "
    "uses GE F404; dry Kaveri derivative for Ghatak UCAV, flight trials on an Il-76 testbed in Russia): "
    "https://en.wikipedia.org/wiki/GTRE_GTX-35VS_Kaveri",
    "Business Today, 13 Jul 2026 - HAL gets 7th GE F404 engine for Tejas Mk1A (F404 delivery delays held up Tejas "
    "Mk1A): https://www.businesstoday.in/india/story/hal-gets-7th-ge-f404-engine-for-tejas-mk1a-fault-in-earlier-"
    "engine-resolved-542588-2026-07-13",
    "AlphaDefense - Kaveri Engine (GTX-35VS) overview: https://alphadefense.in/encyclopedia/kaveri-engine-gtx-35vs/",
]

SPEC = [
    {"key": "hook", "accent": SAFFRON, "text": "",
     "visual": "Sepia 1989: engineers cheer a new engine on a test stand with a tricolour; cut to today's Tejas in "
               "the sky, its engine bay circled with a US flag",
     "vo": [("hook", [("सैंतीस साल पहले", "37 SAAL PEHLE"), ("भारत ने अपना जेट इंजन", "BHARAT NE APNA JET ENGINE"),
                      ("बनाना शुरू किया।", "BANANA SHURU KIYA")]),
            ("punch", [("पर आज भी तेजस", "PAR AAJ BHI TEJAS"), ("अमेरिकी इंजन से उड़ता है।", "AMERICAN ENGINE SE UDTA HAI")])]},
    {"key": "late", "accent": RED, "text": "",
     "visual": "A row of new Tejas jets parked without engines, a clock spinning; a crate with a US flag arrives late; "
               "crew wait with arms folded",
     "vo": [("tell", [("और जब अमेरिका से", "AUR JAB AMERICA SE"), ("इंजन देर से आए", "ENGINE DER SE AAYE")]),
            ("punch", [("तो हमारे नए तेजस", "TO HAMARE NAYE TEJAS"), ("भी देर से मिले।", "BHI DER SE MILE")])]},
    {"key": "thrust", "accent": CYAN, "text": "",
     "visual": "Spec callout: two thrust bars rise side by side - F404 reaches the NEED line, KAVERI stops short; the "
               "Kaveri on its stand gives a weaker flame",
     "vo": [("build", [("हमारा कावेरी इंजन", "HAMARA KAVERI ENGINE"), ("तेजस के लिए", "TEJAS KE LIYE"),
                       ("ज़रूरी ज़ोर नहीं दे पाया।", "ZAROORI ZOR NAHI DE PAYA")])]},
    {"key": "hard", "accent": FIRE, "text": "",
     "visual": "Engine cutaway: turbine blades glow red-hot; then a globe with only a few flags lit (US, Russia, "
               "France) and an empty slot for India",
     "vo": [("tell", [("क्योंकि जेट इंजन बनाना", "KYUNKI JET ENGINE BANANA"), ("रॉकेट बनाने से भी", "ROCKET BANANE SE BHI"),
                      ("मुश्किल माना जाता है।", "MUSHKIL MAANA JAATA HAI")]),
            ("punch", [("दुनिया के गिने चुने देश", "DUNIYA KE GINE CHUNE DESH"), ("ही ये कर पाते हैं।", "HI YE KAR PAATE HAIN")])]},
    {"key": "ghatak", "accent": INDIA_GREEN, "text": "",
     "visual": "The Ghatak flying-wing drone streaks across the sky with a blue Kaveri glow in its exhaust; a test "
               "aircraft escorts it",
     "vo": [("build", [("अब कावेरी का नया रूप", "AB KAVERI KA NAYA ROOP"), ("घातक ड्रोन के लिए", "GHATAK DRONE KE LIYE"),
                       ("हवा में टेस्ट हो रहा है।", "HAWA MEIN TEST HO RAHA HAI")])]},
    {"key": "debate", "accent": GOLD, "text": "",
     "visual": "Balance scale: engineer (DRDO) on one side, an empty cash box on the other; the poll card asks",
     "vo": [("ask", [("तो इस देरी की", "TO IS DERI KI"), ("असली वजह क्या है।", "ASLI WAJAH KYA HAI")]),
            ("punch", [("डी आर डी ओ की गलती", "DRDO KI GALTI"), ("या पैसों की कमी।", "YA PAISON KI KAMI?")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "37": GOLD, "SAAL": GOLD, "BHARAT": SAFFRON, "APNA": SAFFRON, "JET": CYAN, "ENGINE": CYAN, "TEJAS": SAFFRON,
    "AMERICAN": CYAN, "AMERICA": CYAN, "DER": RED, "KAVERI": SAFFRON, "ZOR": RED, "NAHI": RED, "ROCKET": FIRE,
    "MUSHKIL": FIRE, "GINE": GOLD, "CHUNE": GOLD, "GHATAK": INDIA_GREEN, "DRONE": INDIA_GREEN, "TEST": INDIA_GREEN,
    "DRDO": SAFFRON, "GALTI": RED, "PAISON": GOLD, "KAMI?": GOLD, "KAMI": GOLD, "ASLI": GOLD, "WAJAH": GOLD,
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".")] = HOT[_k]


def at(scene, key, frac, d):
    return scene.cue(key, frac * d)


# ============================================================ scenery & props

def lab(ctx, t, sepia=0.0):
    """GTRE-style test cell: concrete walls, a big exhaust duct, floor markings."""
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    g.add_color_stop_rgb(0, *hexc("#2A3340"))
    g.add_color_stop_rgb(1, *hexc("#4A5664"))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    for k in range(6):
        line(ctx, [(0, 200 + 150 * k), (W, 200 + 150 * k)], hexc("#3A4450"), 3, 0.6)
    ctx.arc(980, 640, 210, 0, math.tau)                         # exhaust duct
    rgba(ctx, hexc("#151A20"))
    ctx.fill()
    ctx.arc(980, 640, 210, 0, math.tau)
    rgba(ctx, STEEL)
    ctx.set_line_width(14)
    ctx.stroke()
    ctx.rectangle(0, 1000, W, GROUND)
    rgba(ctx, hexc("#30363E"))
    ctx.fill()
    for k in range(8):
        line(ctx, [(k * 160, 1010), (k * 160 + 80, 1010)], hexc("#E8C040"), 8, 0.8)
    if sepia > 0:
        sep = cairo.LinearGradient(0, 0, 0, H)
        sep.add_color_stop_rgba(0, 0.45, 0.32, 0.15, 0.45 * sepia)
        sep.add_color_stop_rgba(1, 0.3, 0.2, 0.08, 0.45 * sepia)
        ctx.rectangle(0, 0, W, H)
        ctx.set_source(sep)
        ctx.fill()
        for k in range(3):
            sx = rnd(int(t * 12) + k, 5) * W
            line(ctx, [(sx, 0), (sx + 6, GROUND)], (1, 0.95, 0.85), 1.5, 0.25 * sepia)


def plume(ctx, x, y, L, t, c=FIRE, a=1.0):
    """Jet exhaust flame pointing to +x from (x, y)."""
    for k in range(5):
        fl = L * (0.6 + 0.4 * (k / 4)) * (0.9 + 0.1 * math.sin(t * 30 + k))
        ctx.move_to(x, y - 40 + 8 * k)
        ctx.curve_to(x + fl * 0.4, y - 30, x + fl * 0.8, y - 10, x + fl, y)
        ctx.curve_to(x + fl * 0.8, y + 10, x + fl * 0.4, y + 30, x, y + 40 - 8 * k)
        ctx.close_path()
        rgba(ctx, c if k < 3 else hexc("#FFE6A0"), 0.25 * a)
        ctx.fill()
    glow(ctx, x + L * 0.3, y, L * 0.5, c, 0.4 * a)


def tejas_engine_callout(ctx, cx, cy, s, ang, t, k):
    """Circle the engine bay of a drawn Tejas and pin a US flag to it (k = reveal 0..1)."""
    ex, ey = cx + (-55 * s) * math.cos(ang), cy + (-55 * s) * math.sin(ang)
    pulse = 0.5 + 0.5 * math.sin(t * 7)
    ctx.arc(ex, ey, 70 + 8 * pulse, 0, math.tau * clamp(k * 2))
    rgba(ctx, CYAN, 0.9)
    ctx.set_line_width(6)
    ctx.stroke()
    glow(ctx, ex, ey, 90, CYAN, 0.35 * k)
    kk = clamp(k * 2 - 1)
    line(ctx, [(ex - 50, ey + 50), (ex - 50 - 100 * kk, ey + 50 + 150 * kk)], CYAN, 5)
    if kk >= 1:
        flag(ctx, ex - 290, ey + 200, 150, 90, "us", t)
        rrect(ctx, ex - 296, ey + 194, 162, 102, 6)
        rgba(ctx, CYAN)
        ctx.set_line_width(4)
        ctx.stroke()


def crate(ctx, x, y, s, t):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -150, -200, 300, 200, 10)
    rgba(ctx, hexc("#8A6A3A"))
    ctx.fill()
    for k in range(3):
        line(ctx, [(-150, -150 + 60 * k), (150, -150 + 60 * k)], hexc("#6A4A22"), 6)
    flag(ctx, -70, -170, 140, 84, "us", t)
    ctx.restore()


def clock(ctx, x, y, r, t, speed=8.0):
    ctx.arc(x, y, r, 0, math.tau)
    rgba(ctx, hexc("#F4F4F0"))
    ctx.fill()
    ctx.arc(x, y, r, 0, math.tau)
    rgba(ctx, RED)
    ctx.set_line_width(8)
    ctx.stroke()
    for ang, L, w in ((t * speed, r * 0.8, 6), (t * speed / 12, r * 0.55, 9)):
        line(ctx, [(x, y), (x + L * math.sin(ang), y - L * math.cos(ang))], hexc("#1A1A1A"), w)


def thrust_bar(ctx, x, y0, top, u, c, label, t, need_y=None):
    """A vertical thrust bar growing from y0 up to `top` (by u); label under it (ASCII prop marking)."""
    h = (y0 - top) * u
    rrect(ctx, x - 70, y0 - h, 140, h, 10)
    rgba(ctx, c, 0.9)
    ctx.fill()
    glow(ctx, x, y0 - h, 90, c, 0.3)
    text(ctx, label, x, y0 + 50, 46, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=8)


def globe(ctx, cx, cy, r, t):
    g = cairo.RadialGradient(cx - r * 0.3, cy - r * 0.3, r * 0.1, cx, cy, r)
    g.add_color_stop_rgb(0, *hexc("#3A8AD8"))
    g.add_color_stop_rgb(1, *hexc("#0A2A5A"))
    ctx.arc(cx, cy, r, 0, math.tau)
    ctx.set_source(g)
    ctx.fill()
    ctx.save()
    ctx.arc(cx, cy, r, 0, math.tau)
    ctx.clip()
    for k in range(6):                                            # drifting land masses
        lx = cx - r + ((rnd(k, 2) * 2 * r + t * 40) % (2.4 * r)) - 0.2 * r
        ly = cy - r * 0.7 + rnd(k, 3) * r * 1.4
        ell(ctx, lx, ly, 90 + 60 * rnd(k, 4), 50 + 40 * rnd(k, 5))
        rgba(ctx, hexc("#3E8A4A"), 0.9)
        ctx.fill()
    ctx.restore()
    ctx.arc(cx, cy, r, 0, math.tau)
    rgba(ctx, CYAN, 0.6)
    ctx.set_line_width(4)
    ctx.stroke()


def sky_day(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    g.add_color_stop_rgb(0, *hexc("#0E2A5A"))
    g.add_color_stop_rgb(0.6, *hexc("#3A7AC8"))
    g.add_color_stop_rgb(1, *hexc("#A8D0F0"))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    for i in range(6):
        cx = (rnd(i, 1) * W - t * 160 * (0.6 + rnd(i, 2))) % (W + 400) - 200
        cy = 200 + rnd(i, 3) * 700
        for k in range(4):
            ell(ctx, cx + 60 * k, cy + 10 * math.sin(k), 90, 40)
            rgba(ctx, WHITE, 0.55)
            ctx.fill()


# ============================================================ scenes

class Hook(Cued):
    """1989 sepia cheer at the test stand -> today's Tejas with its American engine circled."""

    def events(self, d):
        return [(0.1, "whoosh"), (at(self, "PAR AAJ", 0.5, d), "whoosh"), (at(self, "AMERICAN", 0.7, d), "beep")]

    def draw(self, ctx, t, d):
        tp = at(self, "PAR AAJ", 0.5, d)
        if t < tp + 0.3:
            lab(ctx, t, sepia=1.0)
            jet_engine(ctx, 560, 760, 1.0, solid=1.0, t=t)
            flag(ctx, 150, 330, 170, 104, "in", t, pole=600)
            rrect(ctx, 420, 260, 240, 90, 8)                       # year plaque (prop marking)
            rgba(ctx, hexc("#2A2418"))
            ctx.fill()
            text(ctx, "1989", 540, 305, 64, GOLD, font=CAPTION_FONT, bold=False)
            person(ctx, 200, GROUND, 0.6, t, "engineer", "cheer")
            person(ctx, 900, GROUND, 0.6, t, "engineer2", "cheer", flip=True)
        if t >= tp:
            ctx.push_group()
            sky_day(ctx, t)
            ang = math.radians(-24)
            draw_tejas_fighter(ctx, 540, 640, scale=2.1, angle=ang, afterburner=True)
            tejas_engine_callout(ctx, 540, 640, 2.1, ang, t, clamp((t - tp - 0.4) / 0.8))
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(clamp((t - tp) / 0.3))


class Late(Cued):
    """New Tejas jets wait without engines; the US crate arrives late; the clock spins."""

    def events(self, d):
        return [(0.2, "tick"), (at(self, "TO HAMARE", 0.55, d), "thud")]

    def draw(self, ctx, t, d):
        th = at(self, "TO HAMARE", 0.55, d)
        g = cairo.LinearGradient(0, 0, 0, GROUND)
        g.add_color_stop_rgb(0, *hexc("#1E2430"))
        g.add_color_stop_rgb(1, *hexc("#3A4250"))
        ctx.set_source(g)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()
        ctx.rectangle(0, 900, W, GROUND)
        rgba(ctx, hexc("#2A2E36"))
        ctx.fill()
        for k, (x, y) in enumerate(((300, 520), (780, 520), (540, 780))):
            draw_tejas_fighter(ctx, x, y, scale=0.95, angle=0.0, afterburner=False)
            ex = x - 55 * 0.95
            ctx.arc(ex, y, 48, 0, math.tau)                        # empty engine bay
            rgba(ctx, RED, 0.6 + 0.3 * math.sin(t * 6 + k))
            ctx.set_line_width(6)
            ctx.stroke()
        clock(ctx, 900, 230, 90, t, speed=10)
        arrive = clamp((t - th + 0.4) / 0.9)
        crate(ctx, lerp(-260, 220, ease_out_cubic(arrive)), 1090, 0.8, t)
        person(ctx, 880, GROUND, 0.6, t, "crew", "think", flip=True)
        person(ctx, 1000, GROUND, 0.56, t, "pilot", "shrug" if t > th else "stand", flip=True)


class Thrust(Cued):
    """Side-by-side spec callout: F404 reaches the NEED line, Kaveri stops short; weak flame on the stand."""

    def events(self, d):
        return [(0.15, "whoosh"), (at(self, "ZAROORI", 0.6, d), "alarm")]

    def draw(self, ctx, t, d):
        tz = at(self, "ZAROORI", 0.6, d)
        lab(ctx, t)
        jet_engine(ctx, 300, 900, 0.62, solid=1.0, t=t)
        plume(ctx, 300 + 170, 900, 180 + 40 * math.sin(t * 3), t, c=hexc("#FF9A4A"), a=0.8)
        need = 330
        line(ctx, [(600, need), (1040, need)], GOLD, 6)
        text(ctx, "NEED", 1000, need - 36, 40, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=6)
        u = clamp(t / max(0.8, tz))
        thrust_bar(ctx, 700, 1000, need, u, CYAN, "F404", t)
        thrust_bar(ctx, 930, 1000, need + 150, u, SAFFRON, "KAVERI", t)
        if t > tz:                                                  # the shortfall gap flashes red
            k = 0.5 + 0.5 * math.sin(t * 10)
            rrect(ctx, 860, need, 140, 150, 8)
            rgba(ctx, RED, 0.25 + 0.25 * k)
            ctx.fill()
            person(ctx, 150, GROUND, 0.58, t, "engineer", "shrug")
        else:
            person(ctx, 150, GROUND, 0.58, t, "engineer", "point")


class Hard(Cued):
    """Red-hot turbine blades (why it's harder than a rocket), then a globe with only a few flags lit."""

    def events(self, d):
        return [(0.1, "whoosh"), (at(self, "DUNIYA", 0.55, d), "pop")]

    def draw(self, ctx, t, d):
        td = at(self, "DUNIYA", 0.55, d)
        if t < td + 0.3:
            g = cairo.RadialGradient(540, 600, 40, 540, 600, 800)
            g.add_color_stop_rgb(0, *hexc("#3A1A10"))
            g.add_color_stop_rgb(1, *hexc("#0A0604"))
            ctx.set_source(g)
            ctx.rectangle(0, 0, W, H)
            ctx.fill()
            heat = 0.6 + 0.4 * math.sin(t * 4)
            glow(ctx, 540, 600, 420, FIRE, 0.4 * heat)
            ctx.save()
            ctx.translate(540, 600)
            ctx.rotate(t * 6)
            for k in range(28):                                     # spinning turbine disc
                ctx.save()
                ctx.rotate(k * math.tau / 28)
                poly(ctx, [(60, -14), (300, -26), (310, 10), (60, 14)],
                     mix_c(hexc("#FFB04A"), hexc("#FF3A1A"), heat))
                ctx.restore()
            ctx.arc(0, 0, 70, 0, math.tau)
            rgba(ctx, STEEL_DK)
            ctx.fill()
            ctx.restore()
            for i in range(20):                                     # heat sparks
                u = (t * 0.8 + rnd(i, 4)) % 1
                circle(ctx, 540 + 420 * (rnd(i, 5) - 0.5), 600 - 400 * u, 5, hexc("#FFD08A"), 0.8 * (1 - u))
        if t >= td:
            ctx.push_group()
            g = cairo.LinearGradient(0, 0, 0, H)
            g.add_color_stop_rgb(0, *hexc("#04081A"))
            g.add_color_stop_rgb(1, *hexc("#0A1430"))
            ctx.set_source(g)
            ctx.rectangle(0, 0, W, H)
            ctx.fill()
            for i in range(60):
                circle(ctx, rnd(i, 1) * W, rnd(i, 2) * 1000, 2, WHITE, 0.6)
            globe(ctx, 540, 640, 300, t - td)
            for k, (code, x, y) in enumerate((("us", 140, 260), ("ru", 400, 200), ("fr", 680, 200))):
                kk = clamp((t - td - 0.25 * k) / 0.3)
                if kk > 0:
                    flag(ctx, x, y, 200 * kk, 120 * kk, code, t)
            for k, x in enumerate((900, 160)):                       # two more (unnamed) members
                circle(ctx, x + 40, 1000 - 60 * k, 26, GOLD, 0.8 * clamp((t - td - 0.8) / 0.3))
            kk = clamp((t - td - 1.0) / 0.3)                         # India's empty slot, dashed
            if kk > 0:
                ctx.set_dash([18, 12])
                rrect(ctx, 760, 900, 200, 120, 10)
                rgba(ctx, SAFFRON, 0.9 * kk)
                ctx.set_line_width(6)
                ctx.stroke()
                ctx.set_dash([])
                flag(ctx, 800, 930, 120, 70, "in", t)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(clamp((t - td) / 0.3))


class Ghatak(Cued):
    """Ghatak drone flies with a blue Kaveri glow; trail of light; the first hopeful beat."""

    def events(self, d):
        return [(0.1, "whoosh"), (at(self, "HAWA", 0.6, d), "shimmer")]

    def draw(self, ctx, t, d):
        sky_day(ctx, t)
        u = t / max(1.0, d)
        x = lerp(-150, 1150, u)
        y = 600 - 120 * math.sin(u * math.pi)
        for k in range(16):                                         # exhaust trail
            circle(ctx, x - 140 - 40 * k, y + 6 * math.sin(t * 3 + k), 22 - k, CYAN, 0.35 * (1 - k / 16))
        glow(ctx, x - 120, y, 160, CYAN, 0.45)
        draw_ghatak_drone(ctx, x, y, 0.9, t)
        flag(ctx, 80, 1000, 160, 96, "in", t, pole=0)


class Debate(Cued):
    """Balance: engineer side vs empty cash box; the poll card asks the question."""

    def events(self, d):
        return [(0.15, "tick"), (at(self, "DRDO", 0.55, d), "pop")]

    def draw(self, ctx, t, d):
        tq = at(self, "DRDO", 0.55, d)
        g = cairo.RadialGradient(540, 600, 60, 540, 600, 900)
        g.add_color_stop_rgb(0, *hexc("#1E3A5A"))
        g.add_color_stop_rgb(1, *hexc("#08101C"))
        ctx.set_source(g)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()
        balance(ctx, 540, 380, 0.16 * math.sin(t * 2.2), t)
        person(ctx, 120, GROUND, 0.58, t, "engineer", "point")
        person(ctx, 960, GROUND, 0.58, t, "official", "shrug", flip=True)
        rrect(ctx, 830, 960, 150, 100, 8)                           # empty cash box
        rgba(ctx, hexc("#3A3A40"))
        ctx.fill()
        rrect(ctx, 830, 930, 150, 30, 6)
        rgba(ctx, hexc("#5A5A62"))
        ctx.fill()
        lego.ending(sys.modules[__name__], ctx, t, t - tq, t - tq - 0.8, question=("DRDO KI GALTI", "YA PAISON KI KAMI?"),
                    options=("DRDO", "PAISA"), y=600)


def mix_c(a, b, u):
    return tuple(x + (y - x) * clamp(u) for x, y in zip(a, b))


SCENE_CLASSES = {"hook": Hook, "late": Late, "thrust": Thrust, "hard": Hard, "ghatak": Ghatak, "debate": Debate}


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
        "37 Saal Baad Bhi Tejas American Engine Par Kyun? Kaveri Ka Sach #shorts",
        "Kaveri Engine: Galti DRDO Ki Ya Paison Ki Kami? #shorts",
        "Bharat Apna Jet Engine Kyun Nahi Bana Paya? Kaveri #shorts",
    ],
    "title": "37 Saal Baad Bhi Tejas American Engine Par Kyun? Kaveri Ka Sach #shorts",
    "thumb_text": "37 SAAL BAAD BHI?",
    "queries": ["kaveri engine", "tejas engine", "kaveri engine kyun fail hua"],
    "description": """Kaveri engine ka sach: Bharat ne 1989 mein apna jet engine banana shuru kiya, par aaj bhi Tejas American GE F404 engine par udta hai. Kaveri engine kyun fail hua aur aage kya?

Is Short mein:
- 1989: GTRE ka Kaveri programme Tejas (LCA) ke liye shuru hua
- Kaveri Tejas ke liye zaroori thrust tak nahi pahuncha, isliye Tejas mein GE F404 laga
- GE F404 engines der se aaye, to Tejas Mk1A ki delivery bhi der se hui
- Jet engine banana rocket se bhi mushkil maana jaata hai - duniya ke gine chune desh hi bana paate hain
- Ab Kaveri ka dry version Ghatak drone ke liye test ho raha hai (Russia mein Il-76 flying testbed par udaan trials)

Debate: deri ki asli wajah DRDO ki galti hai ya paison ki kami? Ye kisi party ya neta ki baat nahi - apna jawab comment mein likho.

Sources:
- Wikipedia: GTRE GTX-35VS Kaveri
- Business Today (13 Jul 2026): HAL gets 7th GE F404 engine for Tejas Mk1A
- AlphaDefense: Kaveri Engine (GTX-35VS)
""",
    "tags": ["kaveri engine", "tejas engine", "kaveri engine news", "ge f404", "drdo", "gtre", "ghatak drone",
             "indian fighter jet engine", "tejas mk1a", "jet engine india", "reality shift", "defence shorts",
             "aatmanirbhar bharat defence"],
    "hashtags": ["#Shorts", "#KaveriEngine", "#Tejas"],
    "pinned_comment": "37 saal ki deri - galti DRDO ki ya paison ki kami ki? 🤔 Apna jawab likho 👇 (DRDO / PAISA)",
}


def thumbnail(ctx):
    sky_day(ctx, 1.0)
    ang = math.radians(-24)
    draw_tejas_fighter(ctx, 540, 760, scale=2.1, angle=ang, afterburner=True)
    tejas_engine_callout(ctx, 540, 760, 2.1, ang, 1.0, 1.0)
    text(ctx, "37 SAAL BAAD BHI", 540, 205, 104, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "AMERICAN ENGINE?", 540, 330, 112, RED, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "KAVERI KA SACH", 540, 1330, 120, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, PAL["ui"], a=0.85)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.kaveri")
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
