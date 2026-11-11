"""Reality Shift Short - Prithvi: February 1988, India's first home-made missile lifts off (~38s fact).

Usage:
  python generate_prithvi_short.py

Lego template: radar header, typewriter captions, scan-line wipes, intel palette, comment-prompt ending.
Five scenes: Sriharikota pad, countdown and lift-off, PRITHVI stamp -> IGMDP 1983 file, five missile cards, Prithvi
lights up first -> side-view ballistic arcs over a km ruler: Prithvi-I 150 km (Army), Prithvi-II ~350 km ->
liquid fuel: tanker hose, fuel gauge and a prep clock; solid-fuel Pralay takes over -> "favourite desi missile?"
prompt over a line of missiles growing from Prithvi to Agni (sets up the 6:30 PM Agni Short).
The exact first-flight day differs by source (8 / 22 / 25 Feb 1988), so the script says only "February 1988".
"""

import importlib
import json
import math

import cairo

import engine
import delivery
import lego
from engine import *  # noqa: F401,F403
from generate_chabahar_short import Cued
from stories.reality_shift import stamp

TOPIC = "PRITHVI FIRST DESI MISSILE"
OUTPUTS = {"edge": "prithvi_short.mp4"}
LEGO = {"header": "radar", "caption": "typewriter", "transition": "scan", "palette": "intel", "ending": "prompt"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.3
TAIL_PAD = 0.25
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 90
MUSIC_STYLE = "march"      # origin story, Army pride (Kusha was tension @ 104)
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"

PAL = lego.PALETTES["intel"]
UI = PAL["ui"]
HI = PAL["hi"]
RED = PAL["alert"]
INK = PAL["ink"]
GREEN = hexc("#3DDC84")
SAFFRON = hexc("#FF9933")
SKY = hexc("#4FA3FF")
STEEL = hexc("#B9C0CA")
OLIVE = hexc("#6E7B4A")
FLAME = hexc("#FF9A2E")
MONO = lego.MONO

SOURCES = [
    "Prithvi: first missile of the Integrated Guided Missile Development Programme (IGMDP, started 1983 under "
    "Dr A.P.J. Abdul Kalam: Prithvi, Agni, Trishul, Akash, Nag); first flight Feb 1988 from SHAR, Sriharikota "
    "(day given as 25 Feb by most Indian accounts, 8 Feb by CSIS Missile Threat, 22 Feb in some news reports) "
    "(Wikipedia: Integrated Guided Missile Development Programme; Drishti IAS, Prithvi-II, 16 Jun 2022)",
    "Prithvi-I ~150 km, Army; Prithvi-II ~350 km, 500-1,000 kg payload, single-stage liquid-fuelled, user trials by "
    "Strategic Forces Command off Odisha (DRDO newsletter, Jun 2019; The Diplomat, Jun 2019; Business Standard/PTI, "
    "Oct 2018)",
    "Liquid fuel must be loaded before launch, making Prithvi slow to prepare; solid-fuel Pralay (MoD) is the "
    "announced successor for the Army (Indian Defence News, Dec 2022; Frontier India; The Defense Post, Sep 2023)",
]

# each line: (tone, [(spoken Hindi, Hinglish caption), ...], pause after)
SPEC = [
    {"key": "launch", "accent": HI, "text": "PRITHVI",
     "visual": "Pre-dawn Sriharikota pad: gantry, missile upright, 3-2-1 countdown, lift-off with smoke; "
               "'FEB 1988' and 'SHAR • SRIHARIKOTA' tags; PRITHVI stamp with 'PEHLI DESI MISSILE'",
     "vo": [("hook", [("सिर्फ़ पाँच साल में...", "SIRF 5 SAAL MEIN...")]),
            ("punch", [("प्लान से उड़ान तक!", "PLAN SE UDAAN TAK!")]),
            ("tell", [("फ़रवरी उन्नीस सौ अठासी,", "FEBRUARY 1988,"), ("श्रीहरिकोटा।", "SRIHARIKOTA.")], 0.3),
            ("build", [("भाई, एक मिसाइल", "BHAI, EK MISSILE"), ("आसमान में उठी—", "AASMAAN MEIN UTHI—")], 0.25),
            ("punch", [("म्हारे देश की पहली देसी मिसाइल,", "MHAARE DESH KI PEHLI DESI MISSILE,"), ("पृथ्वी!", "PRITHVI!")], 0)]},
    {"key": "plan", "accent": UI, "text": "IGMDP 1983",
     "visual": "File card 'IGMDP • 1983 • DR. KALAM KI TEAM'; five missile cards slide in (PRITHVI, AGNI, TRISHUL, "
               "AKASH, NAG); the Prithvi card lights up with a #1 badge",
     "vo": [("tell", [("उन्नीस सौ तिरासी में", "1983 MEIN"), ("कलाम साहब की टीम ने", "KALAM SAAHAB KI TEAM NE"),
                      ("पाँच मिसाइलों का प्लान बनाया।", "5 MISSILES KA PLAN BANAYA.")], 0.3),
            ("punch", [("और सबसे पहले", "AUR SABSE PEHLE"), ("तैयार हुई पृथ्वी।", "TAIYAAR HUI PRITHVI!")], 0)]},
    {"key": "range", "accent": HI, "text": "150 → 350 KM",
     "visual": "Side view over a 0-350 km ground ruler: launcher at the left, Prithvi-I arc lands at 150 km "
               "(ARMY tag), then a taller Prithvi-II arc lands at ~350 km",
     "vo": [("tell", [("पृथ्वी वन—", "PRITHVI-I:"), ("डेढ़ सौ किलोमीटर,", "150 KM,"), ("आर्मी के लिए।", "ARMY KE LIYE.")],
             0.3),
            ("build", [("फिर पृथ्वी टू—", "PHIR PRITHVI-II:"), ("साढ़े तीन सौ किलोमीटर,", "350 KM,"), ("घणी दूर!", "GHANI DOOR!")], 0)]},
    {"key": "fuel", "accent": RED, "text": "TARAL vs THOS",
     "visual": "Prithvi on its launcher, a tanker hose fills a LIQUID FUEL gauge while a PREP TIME clock runs; "
               "then a solid-fuel Pralay rises beside it with 'THOS INDHAN = JALDI TAIYAAR' and a PRALAY stamp",
     "vo": [("low", [("पर इसमें लिक्विड फ़्यूल", "PAR ISMEIN LIQUID FUEL"), ("भरना पड़ता है,", "BHARNA PADTA HAI,")], 0.2),
            ("tell", [("लॉन्च से पहले", "LAUNCH SE PEHLE"), ("घणा टाइम लगता है।", "GHANA TIME LAGTA HAI.")], 0.3),
            ("punch", [("इसीलिए इब सॉलिड फ़्यूल वाली", "ISILIYE IB SOLID FUEL WAALI"), ("प्रलय", "PRALAY"),
                       ("इसकी जगह ले रही है।", "ISKI JAGAH LE RAHI HAI!")], 0)]},
    {"key": "ask", "accent": HI, "text": "AAPKI BAARI",
     "visual": "A dim row of missiles growing left to right (PRITHVI ... AGNI) behind the comment-prompt card that "
               "types PRITHVI / AGNI-V / BRAHMOS / AKASH",
     "vo": [("tell", [("पृथ्वी से शुरू होया सफ़र", "PRITHVI SE SHURU HOYA SAFAR"),
                      ("आज अग्नि तक पहुँच गया।", "AAJ AGNI TAK PAHUNCH GAYA.")], 0.35),
            ("ask", [("थारी फ़ेवरेट देसी मिसाइल", "THAARI FAVOURITE DESI MISSILE"), ("कौन सी है?", "KAUN SI HAI?")], 0.2),
            ("cta", [("कमेंट में बता दो भाई।", "COMMENT MEIN BATA DO BHAI!")], 0)]},
]

DELIVERY = delivery.build(SPEC)   # catchy pace: quick builds, held beat, heavy punch
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {"SIRF": HI, "SAAL": HI, "UDAAN": HI, "FEBRUARY": HI, "1988": HI, "SRIHARIKOTA": UI, "AASMAAN": SKY, "UTHI": HI, "PEHLI": HI, "DESI": SAFFRON,
       "PRITHVI": HI, "PRITHVI!": HI, "1983": UI, "KALAM": SAFFRON, "5": HI, "MISSILES": UI, "PLAN": UI,
       "SABSE": HI, "PEHLE": HI, "TAIYAAR": GREEN, "PRITHVI-I": UI, "150": UI, "KM": INK, "ARMY": OLIVE,
       "PRITHVI-II": HI, "350": HI, "LIQUID": RED, "FUEL": RED, "GHANA": RED, "TIME": RED, "SOLID": GREEN, "GHANI": HI, "MHAARE": SAFFRON, "THAARI": HI, "BHAI": SAFFRON, "PRALAY": GREEN,
       "JAGAH": GREEN, "SAFAR": UI, "AGNI": SAFFRON, "FAVOURITE": HI, "COMMENT": HI}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".")] = HOT[_k]


# ============================================================ props

def bg(ctx, top=(0.02, 0.04, 0.05), bottom=(0.005, 0.01, 0.015)):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *top)
    g.add_color_stop_rgb(1, *bottom)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()


def grid(ctx, a=0.08, step=90):
    for x in range(0, W + 1, step):
        line(ctx, [(x, 150), (x, 1140)], UI, 1, a)
    for y in range(150, 1141, step):
        line(ctx, [(0, y), (W, y)], UI, 1, a)


def tag(ctx, s, x, y, c, u, size=40, sub=None):
    """Bracketed mono label that wipes open, centred on (x, y)."""
    if u <= 0:
        return
    w = max(text_width(ctx, s, size, font=MONO), text_width(ctx, sub, size * 0.65, font=MONO) if sub else 0) + 50
    h = size * (2.3 if sub else 1.5)
    k = ease_out_cubic(u / 0.25)
    ctx.save()
    ctx.translate(x, y)
    ctx.rectangle(-w / 2, -h / 2 - 10, w * k, h + 20)
    ctx.clip()
    rrect(ctx, -w / 2, -h / 2, w, h, 8)
    rgba(ctx, PAL["panel"], 0.92)
    ctx.fill()
    for sx in (-1, 1):
        for sy in (-1, 1):
            px, py = sx * w / 2, sy * h / 2
            line(ctx, [(px - sx * 22, py), (px, py), (px, py - sy * 22)], c, 4)
    text(ctx, s, 0, -size * 0.42 if sub else 0, size, INK, font=MONO)
    if sub:
        text(ctx, sub, 0, size * 0.62, size * 0.65, c, font=MONO)
    ctx.restore()


def flame_jet(ctx, L, d, t, f):
    """Exhaust plume behind the tail (local coords: tail at x = -L/2, pointing -x)."""
    for k, (c, a) in enumerate(((RED, 0.5), (FLAME, 0.85), ((1, 0.97, 0.85), 0.95))):
        s = (1 + 0.22 * math.sin(t * 47 + k * 2.1)) * f * (1 - 0.28 * k)
        ctx.move_to(-L / 2, -d * (0.4 - 0.1 * k))
        ctx.curve_to(-L / 2 - L * 0.2 * s, -d * 0.3, -L / 2 - L * 0.36 * s, -d * 0.05, -L / 2 - L * 0.42 * s, 0)
        ctx.curve_to(-L / 2 - L * 0.36 * s, d * 0.05, -L / 2 - L * 0.2 * s, d * 0.3, -L / 2, d * (0.4 - 0.1 * k))
        ctx.close_path()
        rgba(ctx, c, a)
        ctx.fill()
    glow(ctx, -L / 2 - L * 0.12, 0, L * 0.2, FLAME, 0.35 * f)


def rocket(ctx, x, y, L, ang, t, flame=0.0, body=(0.93, 0.94, 0.95), band=OLIVE, name=None, a=1.0):
    """Stubby ballistic missile (Prithvi-style: thick body, cone nose, four tail fins); centre (x, y), nose along ang."""
    d = L * 0.13
    nose = L * 0.24
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.push_group()
    if flame > 0:
        flame_jet(ctx, L, d, t, flame)
    for sgn in (-1, 1):  # tail fins
        ctx.move_to(-L / 2 + L * 0.02, sgn * d * 0.5)
        ctx.line_to(-L / 2 - L * 0.02, sgn * d * 1.25)
        ctx.line_to(-L / 2 + L * 0.2, sgn * d * 0.5)
        ctx.close_path()
        rgba(ctx, shade(band, 0.8))
        ctx.fill()
    g = cairo.LinearGradient(0, -d / 2, 0, d / 2)
    g.add_color_stop_rgb(0, *body)
    g.add_color_stop_rgb(0.55, *shade(body, 0.78))
    g.add_color_stop_rgb(1, *shade(body, 0.42))
    ctx.move_to(-L / 2, -d / 2)
    ctx.line_to(L / 2 - nose, -d / 2)
    ctx.curve_to(L / 2 - nose * 0.4, -d / 2, L / 2 - nose * 0.08, -d * 0.2, L / 2, 0)
    ctx.curve_to(L / 2 - nose * 0.08, d * 0.2, L / 2 - nose * 0.4, d / 2, L / 2 - nose, d / 2)
    ctx.line_to(-L / 2, d / 2)
    ctx.close_path()
    ctx.set_source(g)
    ctx.fill()
    for bx in (-L * 0.28, L * 0.12):  # painted bands
        ctx.rectangle(bx, -d / 2, L * 0.05, d)
        rgba(ctx, band, 0.95)
        ctx.fill()
    ctx.rectangle(-L / 2, -d / 2, L * 0.04, d)
    rgba(ctx, (0.18, 0.19, 0.2))
    ctx.fill()
    if name and L > 260:
        text(ctx, name, -L * 0.07, 1, d * 0.42, (0.08, 0.1, 0.1), font=CAPTION_FONT, bold=False)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(a)
    ctx.restore()


def smoke(ctx, x, y, u, a=1.0, n=14, spread=260):
    """Billowing exhaust cloud at a launch pad, u = seconds since ignition."""
    for i in range(n):
        k = clamp(u * 0.9 - rnd(i, 3) * 0.3)
        if k <= 0:
            continue
        side = (rnd(i, 1) - 0.5) * 2
        cx = x + side * spread * ease_out_cubic(k)
        cy = y - 20 * rnd(i, 2) - 50 * k * rnd(i, 4)
        r = 40 + 90 * k * (0.6 + rnd(i, 5))
        circle(ctx, cx, cy, r, (0.72, 0.74, 0.76), 0.22 * a * (1 - 0.4 * k))


def truck(ctx, x, y, s, c=OLIVE, a=1.0):
    """Flat launcher truck, wheel line at y, centred on x."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -230, -60, 340, 36, 6)
    rgba(ctx, shade(c, 0.85), a)
    ctx.fill()
    rrect(ctx, 115, -110, 110, 86, 12)
    rgba(ctx, c, a)
    ctx.fill()
    rrect(ctx, 160, -98, 50, 32, 5)
    rgba(ctx, (0.1, 0.13, 0.15), a)
    ctx.fill()
    for wx in (-190, -120, 60, 180):
        circle(ctx, wx, -12, 24, (0.07, 0.07, 0.08), a)
        circle(ctx, wx, -12, 10, shade(c, 0.6), a)
    ctx.restore()


# ============================================================ scenes

class Launch(Cued):
    """Pre-dawn pad, countdown, lift-off; PRITHVI stamp."""

    PAD = (540, 1000)

    def beats(self, d):
        c = self.cue
        return {"shar": c("SRIHARIKOTA", d * 0.18), "up": c("AASMAAN", d * 0.4), "first": c("PEHLI", d * 0.65),
                "name": c("PRITHVI", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (0.15, "beep"), (b["shar"], "beep"), (b["up"] - 0.25, "beep"), (b["up"], "whoosh"),
                (b["up"] + 0.1, "engine", 1.2), (b["first"], "thud"), (b["name"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dawn = clamp(t / max(d, 1))
        bg(ctx, (0.02 + 0.08 * dawn, 0.04 + 0.05 * dawn, 0.09), (0.01, 0.02, 0.03))
        for i in range(60):
            circle(ctx, rnd(i, 11) * W, 160 + rnd(i, 12) * 600, 1.2 + 1.8 * rnd(i, 13), INK,
                   (0.15 + 0.35 * rnd(i, 14)) * (1 - 0.6 * dawn))
        px, py = self.PAD
        ctx.rectangle(0, py, W, H - py)  # ground + palms on the coast
        rgba(ctx, (0.02, 0.05, 0.04))
        ctx.fill()
        for i in range(7):
            tx = 60 + i * 160 + 30 * rnd(i, 21)
            if abs(tx - px) < 220:
                continue
            line(ctx, [(tx, py), (tx + 10, py - 120)], (0.05, 0.1, 0.07), 8)
            for k in range(5):
                ang = -math.pi / 2 + (k - 2) * 0.6
                line(ctx, [(tx + 10, py - 120), (tx + 10 + 60 * math.cos(ang), py - 120 + 40 * math.sin(ang) + 30)],
                     (0.05, 0.12, 0.08), 7)
        rrect(ctx, px - 170, py - 30, 340, 30, 4)  # pad
        rgba(ctx, (0.2, 0.22, 0.24))
        ctx.fill()
        gx = px + 120  # gantry tower swings away before lift-off
        lean = 0.35 * ease_in_out(clamp((t - b["up"] + 0.8) / 0.6))
        ctx.save()
        ctx.translate(gx, py - 30)
        ctx.rotate(lean)
        for k in range(9):
            line(ctx, [(0, -60 * k), (60, -60 * (k + 1))], (0.55, 0.3, 0.12), 4)
            line(ctx, [(60, -60 * k), (0, -60 * (k + 1))], (0.55, 0.3, 0.12), 4)
        line(ctx, [(0, 0), (0, -540)], (0.75, 0.42, 0.15), 8)
        line(ctx, [(60, 0), (60, -540)], (0.75, 0.42, 0.15), 8)
        ctx.restore()
        u = t - b["up"]
        rise = 0 if u < 0 else 1100 * (u / 2.2) ** 2
        if u > 0:
            smoke(ctx, px, py - 20, u)
            glow(ctx, px, py - 40, 260 * clamp(u * 2), FLAME, 0.4 * clamp(1 - (u - 1.2) / 1.0))
        rocket(ctx, px, py - 230 - rise, 400, -math.pi / 2, t, flame=clamp(u * 3) if u > 0 else 0, name="PRITHVI")
        if t < b["up"]:  # countdown in the sky
            n = 3 - int(clamp((t - 0.1) / max(b["up"] - 0.1, 0.5)) * 3)
            if n >= 1:
                text(ctx, str(n), 300, 520, 220, HI, font=CAPTION_FONT, bold=False, a=0.85, stroke=(0, 0, 0), stroke_w=12)
        tag(ctx, "FEB 1988", 260, 250, HI, t - 0.05, size=48)
        tag(ctx, "SHAR • SRIHARIKOTA", 700, 340, UI, t - b["shar"], size=34)
        if t > b["first"]:
            stamp(ctx, 540, 640, t - b["name"], -0.04, 760, 230, HI,
                  [("PRITHVI", -28, 140, HI), ("PEHLI DESI MISSILE", 64, 44, INK)])
            if t < b["name"]:
                tag(ctx, "PEHLI DESI MISSILE", 540, 640, SAFFRON, t - b["first"], size=52)


class Plan(Cued):
    """IGMDP 1983 file; five cards; Prithvi lights up first."""

    NAMES = ("PRITHVI", "AGNI", "TRISHUL", "AKASH", "NAG")

    def beats(self, d):
        c = self.cue
        return {"kalam": c("KALAM", d * 0.15), "five": c("MISSILES", d * 0.35), "first": c("PEHLE", d * 0.7),
                "ready": c("TAIYAAR", d * 0.82)}

    def events(self, d):
        b = self.beats(d)
        ev = [(0.02, "thud"), (b["kalam"], "pop")]
        ev += [(b["five"] + 0.14 * k, "pick") for k in range(5)]
        return ev + [(b["first"], "beep"), (b["ready"], "dingdong")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx)
        grid(ctx)
        a0 = clamp(t / 0.3)
        rrect(ctx, 70, 190, W - 140, 150, 16)
        rgba(ctx, PAL["panel"], 0.92 * a0)
        ctx.fill_preserve()
        rgba(ctx, UI, 0.8 * a0)
        ctx.set_line_width(4)
        ctx.stroke()
        text(ctx, "IGMDP • 1983", 110, 240, 58, UI, font=CAPTION_FONT, bold=False, anchor="l", a=a0)
        text(ctx, "Integrated Guided Missile Development Programme", 110, 300, 26, INK, font=MONO, anchor="l",
             a=0.7 * a0)
        if t > b["kalam"]:
            tag(ctx, "DR. KALAM KI TEAM", 540, 410, SAFFRON, t - b["kalam"], size=40)
        lit = t > b["first"]
        for k, name in enumerate(self.NAMES):
            u = t - b["five"] - 0.14 * k
            if u <= 0:
                continue
            y = 520 + 120 * k
            x0 = lerp(W, 0, ease_out_cubic(u / 0.35))
            me = k == 0 and lit
            dim = 0.35 if (lit and k) else 1.0
            rrect(ctx, 110 + x0, y - 48, W - 220, 96, 14)
            rgba(ctx, (0.02, 0.06, 0.06), 0.95)
            ctx.fill_preserve()
            rgba(ctx, HI if me else UI, (0.95 if me else 0.6) * dim)
            ctx.set_line_width(6 if me else 3)
            ctx.stroke()
            rocket(ctx, 260 + x0, y, 190, 0, t, body=(0.9, 0.92, 0.93) if me else (0.6, 0.65, 0.66), a=dim)
            text(ctx, name, 420 + x0, y, 54, HI if me else INK, font=CAPTION_FONT, bold=False, anchor="l", a=dim)
            if me:
                glow(ctx, 540, y, 420, HI, 0.18)
                pop = ease_out_back(clamp((t - b["first"]) / 0.35))
                ctx.save()
                ctx.translate(880, y)
                ctx.scale(pop, pop)
                circle(ctx, 0, 0, 44, HI)
                text(ctx, "#1", 0, 2, 44, (0.05, 0.05, 0.02), font=CAPTION_FONT, bold=False)
                ctx.restore()
        if t > b["ready"]:
            tag(ctx, "SABSE PEHLE TAIYAAR", 540, 1100, HI, t - b["ready"], size=44)


class Range(Cued):
    """Side view: Prithvi-I arc to 150 km, Prithvi-II arc to ~350 km over a ground ruler."""

    X0, GY, PX = 120, 1000, 2.4   # launch x, ground y, pixels per km

    def beats(self, d):
        c = self.cue
        return {"p1": c("PRITHVI-I", d * 0.05), "km1": c("150", d * 0.2), "army": c("ARMY", d * 0.4),
                "p2": c("PRITHVI-II", d * 0.6), "km2": c("350", d * 0.78)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["p1"], "whoosh"), (b["km1"] + 0.6, "boom"), (b["army"], "pop"),
                (b["p2"], "whoosh"), (b["km2"] + 0.8, "boom"), (b["km2"] + 1.0, "dingdong")]

    def arc(self, km, peak, k):
        x1 = self.X0 + km * self.PX
        return [(lerp(self.X0, x1, s), self.GY - 4 * peak * s * (1 - s)) for s in [i / 50 * k for i in range(51)]]

    def flight(self, ctx, t, start, km, peak, c, label):
        u = t - start
        if u <= 0:
            return
        k = ease_in_out(clamp(u / 1.2))
        pts = self.arc(km, peak, k)
        ctx.set_dash([18, 12])
        line(ctx, pts, c, 6, 0.9)
        ctx.set_dash([])
        if k < 1:
            (ax, ay), (bx, by) = pts[-2], pts[-1]
            rocket(ctx, bx, by, 120, math.atan2(by - ay, bx - ax), t, flame=1.0)
        else:
            x1 = self.X0 + km * self.PX
            ring = clamp((u - 1.2) / 0.6)
            if ring < 1:
                ctx.arc(x1, self.GY, 20 + 90 * ring, math.pi, 2 * math.pi)
                rgba(ctx, c, 1 - ring)
                ctx.set_line_width(7)
                ctx.stroke()
            circle(ctx, x1, self.GY, 14, c)
            tag(ctx, label, min(max(x1 - 120, 260), 640), self.GY - peak - 70, c, u - 1.2, size=44)

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx)
        grid(ctx, 0.06)
        gy, x0, px = self.GY, self.X0, self.PX
        ctx.rectangle(0, gy, W, 140)
        rgba(ctx, (0.03, 0.07, 0.05))
        ctx.fill()
        line(ctx, [(60, gy), (W - 40, gy)], UI, 4, 0.8)
        for km in range(0, 351, 50):  # ruler
            x = x0 + km * px
            line(ctx, [(x, gy), (x, gy + (26 if km % 100 == 0 else 14))], UI, 3, 0.8)
            if km % 100 == 0 or km == 350:
                text(ctx, f"{km}", x, gy + 56, 28, INK, font=MONO, a=0.75)
        text(ctx, "KM", W - 70, gy + 100, 26, UI, font=MONO, a=0.7)
        truck(ctx, x0 + 10, gy, 0.42)
        self.flight(ctx, t, b["p1"], 150, 300, UI, "PRITHVI-I • 150 KM")
        if t > b["army"]:
            tag(ctx, "ARMY", x0 + 150 * px * 0.5, gy - 140, OLIVE, t - b["army"], size=36)
        self.flight(ctx, t, b["p2"], 350, 620, HI, "PRITHVI-II • ~350 KM")


class Fuel(Cued):
    """Liquid fuel: hose, gauge and prep clock; then solid-fuel Pralay rises beside Prithvi."""

    def beats(self, d):
        c = self.cue
        return {"taral": c("LIQUID", d * 0.05), "waqt": c("TIME", d * 0.45), "thos": c("SOLID", d * 0.6),
                "pralay": c("PRALAY", d * 0.7), "jagah": c("JAGAH", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        ev = [(0.02, "thud"), (b["taral"], "alarm")]
        ev += [(b["taral"] + 0.5 * k, "tick" if k % 2 == 0 else "tock") for k in range(1, 7)]
        return ev + [(b["waqt"], "beep"), (b["thos"], "whoosh"), (b["pralay"], "boom"), (b["jagah"], "dingdong")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx, (0.05, 0.03, 0.03), (0.01, 0.01, 0.015))
        grid(ctx, 0.05)
        gy = 1000
        line(ctx, [(40, gy), (W - 40, gy)], UI, 3, 0.5)
        swap = ease_in_out(clamp((t - b["thos"]) / 0.6))
        # Prithvi on its launcher slides left when Pralay arrives
        lx = lerp(400, 250, swap)
        truck(ctx, lx, gy, 0.75, a=1 - 0.5 * swap)
        rocket(ctx, lx - 20, gy - 110, 330, -0.5, t, name="PRITHVI", a=1 - 0.5 * swap)
        # hose from a tanker on the right into the missile
        fill = clamp((t - b["taral"]) / max(b["thos"] - b["taral"], 1.0))
        hose_a = 1 - swap
        if hose_a > 0:
            rrect(ctx, 760, gy - 170, 260, 150, 20)  # tanker
            rgba(ctx, shade(RED, 0.55), hose_a)
            ctx.fill()
            text(ctx, "FUEL", 890, gy - 95, 40, INK, font=MONO, a=hose_a)
            pts = [(760, gy - 110), (650, gy - 60), (540, gy - 170), (lx + 40, gy - 200)]
            line(ctx, pts, (0.1, 0.1, 0.1), 16, hose_a)
            flow = (t * 2) % 1
            for j in range(3):
                s = (flow + j / 3) % 1
                i = min(int(s * 3), 2)
                (ax, ay), (bx, by) = pts[i], pts[i + 1]
                f = s * 3 - i
                circle(ctx, lerp(ax, bx, f), lerp(ay, by, f), 9, FLAME, hose_a)
            # gauge
            gx, gyy = 300, 470
            rrect(ctx, gx - 160, gyy - 40, 320, 80, 14)
            rgba(ctx, PAL["panel"], 0.9 * hose_a)
            ctx.fill_preserve()
            rgba(ctx, RED, hose_a)
            ctx.set_line_width(4)
            ctx.stroke()
            rrect(ctx, gx - 145, gyy - 25, 290 * fill, 50, 10)
            rgba(ctx, FLAME, 0.9 * hose_a)
            ctx.fill()
            text(ctx, "LIQUID FUEL", gx, gyy - 75, 38, RED, font=MONO, a=hose_a)
            text(ctx, f"{int(fill * 100)}%", gx, gyy, 36, INK, font=MONO, a=hose_a)
            # prep clock
            cx, cy, r = 790, 480, 110
            circle(ctx, cx, cy, r, PAL["panel"], 0.9 * hose_a)
            ctx.arc(cx, cy, r, 0, math.tau)
            rgba(ctx, RED, hose_a)
            ctx.set_line_width(6)
            ctx.stroke()
            hand = -math.pi / 2 + fill * math.tau * 1.5
            line(ctx, [(cx, cy), (cx + 85 * math.cos(hand), cy + 85 * math.sin(hand))], INK, 7, hose_a)
            circle(ctx, cx, cy, 10, RED, hose_a)
            text(ctx, "PREP TIME", cx, cy - r - 36, 34, RED, font=MONO, a=hose_a)
            if t > b["waqt"]:
                tag(ctx, "GHANA TIME LAGTA HAI", 540, 680, RED, t - b["waqt"], size=48)
        u = t - b["thos"]
        if u > 0:  # Pralay: solid fuel, already loaded, rises from its canister
            k = ease_out_back(clamp(u / 0.5))
            px = 780
            rrect(ctx, px - 50, gy - 520, 100, 520, 16)  # canister
            rgba(ctx, shade(GREEN, 0.35))
            ctx.fill()
            rocket(ctx, px, gy - 300 - 120 * k, 420, -math.pi / 2, t, body=(0.88, 0.92, 0.88), band=GREEN,
                   name="PRALAY")
            tag(ctx, "SOLID FUEL = JHAT TAIYAAR", 540, 300, GREEN, u - 0.2, size=38)
        u = t - b["jagah"]
        if u > 0:
            stamp(ctx, 330, 560, u, -0.04, 480, 120, GREEN, [("PRALAY", 0, 86, GREEN)])


class Ask(Cued):
    """Dim row of missiles growing Prithvi -> Agni behind the comment-prompt card (Lego ending 'prompt')."""

    def beats(self, d):
        c = self.cue
        return {"agni": c("AGNI", d * 0.2), "q": c("FAVOURITE", d * 0.45), "cmt": c("COMMENT", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["agni"], "whoosh"), (b["q"], "pop"), (b["cmt"], "dingdong"),
                (b["cmt"] + 1.1, "pick"), (b["cmt"] + 2.2, "pick")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx)
        grid(ctx, 0.05)
        row = (("PRITHVI", 190, UI), ("", 240, UI), ("", 300, HI), ("", 360, HI), ("AGNI", 430, SAFFRON))
        fade = 1 - 0.65 * clamp((t - b["q"]) / 0.4)
        for k, (name, L, c) in enumerate(row):
            u = t - 0.1 - 0.25 * k
            if u <= 0:
                continue
            x = 120 + 210 * k
            rise = ease_out_back(clamp(u / 0.4))
            rocket(ctx, x, 1060 - L / 2 * rise, L, -math.pi / 2, t, a=fade * clamp(u / 0.2),
                   body=(0.9, 0.92, 0.93) if k < 4 else (0.98, 0.9, 0.82), band=c)
            if name:
                text(ctx, name, x, 1100, 30, c, font=MONO, a=fade)
        if t > b["agni"] and t < b["q"] + 0.4:
            line(ctx, [(120, 520), (960, 520)], SAFFRON, 6, 0.7 * fade)
            tag(ctx, "PRITHVI → AGNI", 540, 520, SAFFRON, t - b["agni"], size=48)
        lego.ending(STORY, ctx, t, t - b["q"], t - b["cmt"], question=("FAVOURITE", "DESI MISSILE?"),
                    suggestions=("PRITHVI", "AGNI-V", "BRAHMOS", "AKASH"), y=560)


SCENE_CLASSES = {"launch": Launch, "plan": Plan, "range": Range, "fuel": Fuel, "ask": Ask}
STORY = importlib.import_module(__name__)


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
        "Prithvi: Bharat Ki Pehli Desi Missile Ki Kahani",
        "1988 Me Udi Bharat Ki Pehli Desi Missile: Prithvi",
        "Prithvi Missile: 150 KM Se 350 KM Tak Ka Safar",
        "Kalam Ki Team Ka Pehla Missile: Prithvi",
        "Prithvi vs Pralay: Liquid vs Solid Fuel",
        "Prithvi Missile Ki Range Kitni Hai? 150 vs 350 KM",
        "IGMDP Ki Pehli Missile: Prithvi Kaise Bani",
        "Bharat Ki Pehli Desi Missile Kaun Si Thi?",
    ],
    "title": "1988 Me Udi Bharat Ki Pehli Desi Missile: Prithvi",   # result-first, number in front
    "thumb_text": "PEHLA KADAM",
    "queries": ["prithvi missile", "bharat ki pehli missile", "prithvi missile range"],
    "description": """
Prithvi missile: Bharat ki pehli desi missile, February 1988 me Sriharikota se pehli baar udi.
Prithvi missile range: Prithvi-I ~150 KM, Prithvi-II ~350 KM.

Is Short me:
• 1983: Dr. Kalam ki team ka IGMDP plan, 5 missiles (Prithvi, Agni, Trishul, Akash, Nag)
• Sabse pehle taiyaar hui Prithvi (pehla test Feb 1988, SHAR Sriharikota)
• Prithvi-I: ~150 KM, Army ke liye | Prithvi-II: ~350 KM tak
• Liquid fuel: launch se pehle bharna padta hai, taiyaari me time lagta hai
• Isliye solid fuel wali Pralay iski jagah le rahi hai

Aapki favourite desi missile kaun si hai? Comment me batao.
Aaj shaam: Agni 1 se 5 tak ki range ka safar, Reality Shift pe.

Note: animation schematic hai, scale pe nahi. Facts public reports (DRDO/MoD) par based hain; pehle test ki
exact tareekh alag-alag sources me 8, 22 ya 25 Feb 1988 di gayi hai.
""",
    "tags": ["prithvi missile", "prithvi", "bharat ki pehli missile", "prithvi missile range", "prithvi 2",
             "igmdp", "abdul kalam missile", "pralay missile", "drdo", "indian missiles", "desi missile",
             "indian defence shorts", "defence hindi", "reality shift"],
    "hashtags": ["#Shorts", "#Prithvi", "#DRDO"],
}


def thumbnail(ctx):
    """1080x1920 cover: PEHLA / KADAM over Prithvi lifting off a pad (title carries 1988 + name)."""
    bg(ctx, (0.06, 0.07, 0.12), (0.01, 0.02, 0.03))
    ctx.rectangle(0, 1560, W, H - 1560)
    rgba(ctx, (0.02, 0.05, 0.04))
    ctx.fill()
    smoke(ctx, 540, 1540, 1.4, a=1.4, n=22, spread=420)
    glow(ctx, 540, 1480, 420, FLAME, 0.45)
    rocket(ctx, 540, 1180, 720, -math.pi / 2, 0.3, flame=1.0, name="PRITHVI")
    g = cairo.LinearGradient(0, 0, 0, 860)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.95)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 860)
    ctx.set_source(g)
    ctx.fill()
    vignette(ctx)
    glow(ctx, 540, 380, 520, HI, 0.22)
    text(ctx, "PEHLA", 540, 320, 280, INK, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=24)
    text(ctx, "KADAM", 540, 590, 250, HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, INK, a=0.7)


def main() -> None:
    import upload_kit
    story = importlib.import_module("generate_prithvi_short")
    engine.make_frame = lego.frame_maker(story)
    final = engine.render(story, "edge")
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
