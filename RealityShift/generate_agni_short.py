"""Reality Shift Short - "Agni 1 se 5: range ka safar" (~65s list: five steps, 700 -> 5,000+ km).

Usage:
  python generate_agni_short.py

List Short on the Lego template: intel-file header, word-chip captions, scan-line wipes, amber palette,
comment-prompt ending. One schematic "range board" carries the whole list: a small drawn India at the centre,
and every Agni adds its own range ring (to scale against each other, not a map projection), with a launch from
the centre, a counting range readout and one fact stamp per step. Seven scenes: hook (700 -> 5,000 km, ~7x,
first flight 1989 at Chandipur) -> Agni-I -> II (x3 in one step) -> III (~50 t) -> IV (under half the weight of
III, ~4,000 km) -> V (canister, Mission Divyastra MIRV, 11 Mar 2024) -> "agla kadam kya?" comment prompt.
No countries or cities are marked inside the rings on purpose: the Short is about India's own progress.
"""

import importlib
import json
import math

import cairo

import engine
import delivery
import lego
from engine import *  # noqa: F401,F403
from generate_brahmos_lego_short import bg, tag
from generate_chabahar_short import Cued
from stories.reality_shift import stamp

TOPIC = "AGNI 1 TO 5 RANGE"
OUTPUTS = {"edge": "agni_short.mp4"}
LEGO = {"header": "intel", "caption": "chip", "transition": "scan", "palette": "amber", "ending": "prompt"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.3
TAIL_PAD = 0.25
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 112
MUSIC_STYLE = "pulse"      # steady build for a step-by-step list (Kusha was tension @ 104)
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"

PAL = lego.PALETTES["amber"]
AMBER = PAL["ui"]
HI = PAL["hi"]
RED = PAL["alert"]
INK = PAL["ink"]
TEAL = hexc("#46E0B0")
GREEN = hexc("#3DDC84")
SAFFRON = hexc("#FF9933")
SKY = hexc("#4FA3FF")
STEEL = hexc("#B9C0CA")
MONO = lego.MONO

SOURCES = [
    "Agni ranges (published figures vary with payload; official full ranges are not released): Agni-I ~700-900 km "
    "(up to ~1,200 km light payload), Agni-II 2,000+ km, Agni-III 3,000+ km (~48 t), Agni-IV ~3,500-4,000 km "
    "(~17-20 t), Agni-V 5,000+ km, canisterised (CSIS Missile Threat 'Agni' profiles; Wikipedia 'Agni (missile)'; "
    "Vajiram & Ravi / Business Standard explainers)",
    "First Agni flight: technology demonstrator, 22 May 1989, Interim Test Range Chandipur, Odisha, under the IGMDP "
    "(CSIS Missile Threat 'Agni-1'; India Today 'Agni-I 1989')",
    "Mission Divyastra: first flight test of Agni-5 with MIRV technology, 11 Mar 2024, Dr APJ Abdul Kalam Island, "
    "Odisha, DRDO (PIB / All India Radio newsonair, 11-13 Mar 2024; Tribune India; Deccan Herald)",
    "Agni-V maiden flight 19 Apr 2012, Wheeler Island, three-stage solid-fuel; later canisterised road-mobile "
    "version tested Jan 2015 (CSIS Missile Threat 'Agni-5'; NPR, 19 Apr 2012; Tribune India, 20 Apr 2012)",
    "Agni-I single-stage solid fuel; Agni-II and Agni-III two-stage (CSIS Missile Threat 'Agni' profiles)",
    "7x = 5,000 / 700 and +1,000 km = 3,000 - 2,000 (arithmetic on the figures above, said as 'lagbhag')",
]

# each line: (tone, [(spoken Hindi, Hinglish caption), ...], pause after)
SPEC = [
    {"key": "hook", "accent": HI, "text": "700 -> 5,000 KM",
     "visual": "Range board: India in the centre, a counter rolls 700 -> 5,000 KM while five rings pop out; "
               "'~7 GUNA' stamp; then a first launch from the Odisha coast with a '1989 • CHANDIPUR' tag",
     "vo": [("hook", [("सात सौ से...", "700 SE...")]),
            ("punch", [("पाँच हज़ार किलोमीटर!", "5,000 KM!")]),
            ("build", [("भाई, सिर्फ़ पाँच कदम में", "BHAI, SIRF 5 KADAM MEIN"), ("सात गुना छलांग।", "7 GUNA CHHALAANG!")])]},
    {"key": "a1", "accent": TEAL, "text": "AGNI-I ~700 KM",
     "visual": "Launch from the centre; ring 1 grows to ~700 KM; '1 STAGE' stamp",
     "vo": [("build", [("अग्नि वन—", "AGNI-I—"), ("एक स्टेज,", "1 STAGE,")]),
            ("punch", [("सात सौ किलोमीटर।", "700 KM.")])]},
    {"key": "a2", "accent": SKY, "text": "AGNI-II 2,000+ KM",
     "visual": "Second launch; ring 2 grows past 2,000 KM; '2 STAGE' and 'x3' stamps",
     "vo": [("build", [("अग्नि टू—", "AGNI-II—"), ("दो हज़ार पार!", "2,000 PAAR!")]),
            ("punch", [("एक झटके में", "EK JHATKE MEIN"), ("तीन गुना!", "3 GUNA!")])]},
    {"key": "a3", "accent": SAFFRON, "text": "AGNI-III 3,000+ KM",
     "visual": "A heavy missile on a weighing plate reads ~50 TON; ring 3 grows past 3,000 KM",
     "vo": [("tell", [("अग्नि थ्री—", "AGNI-III—"), ("तीन हज़ार किलोमीटर,", "3,000 KM,")]),
            ("sly", [("पर वज़न?", "PAR WAZAN?")]),
            ("punch", [("करीब पचास टन!", "KAREEB 50 TON!"), ("घणा भारी।", "GHANA BHAARI.")])]},
    {"key": "a4", "accent": GREEN, "text": "AGNI-IV ~4,000 KM",
     "visual": "A balance: Agni-III (~48 t) sinks, Agni-IV (<1/2) rises; ring 4 grows to ~4,000 KM",
     "vo": [("low", [("फिर अग्नि फ़ोर ने", "PHIR AGNI-IV NE"), ("खेल पलट दिया—", "KHEL PALAT DIYA—")]),
            ("tell", [("वज़न आधे से भी कम,", "WAZAN AADHE SE BHI KAM,")]),
            ("punch", [("रेंज चार हज़ार!", "RANGE 4,000 KM!")])]},
    {"key": "a5", "accent": RED, "text": "AGNI-V 5,000+ KM",
     "visual": "Canister rises and ejects the missile; ring 5 grows past 5,000 KM; '11 MARCH 2024 • MISSION "
               "DIVYASTRA' tag; one missile splits into several re-entry vehicles fanning to different points",
     "vo": [("build", [("और अग्नि फ़ाइव—", "AUR AGNI-V—"), ("पाँच हज़ार से ज़्यादा,", "5,000 KM SE ZYADA,"),
                       ("डिब्बे से सीधा लॉन्च।", "DIBBE SE SEEDHA LAUNCH.")]),
            ("tell", [("दो हज़ार चौबीस में", "2024 MEIN"), ("मिशन दिव्यास्त्र—", "MISSION DIVYASTRA—")]),
            ("punch", [("एक मिसाइल,", "EK MISSILE,"), ("कई निशाने!", "KAI NISHAANE!")])]},
    {"key": "ask", "accent": HI, "text": "AGLA KADAM?",
     "visual": "All five rings dim behind the comment-prompt card: 'AGLA KADAM / KYA HO?', suggestions type in",
     "vo": [("ask", [("इब बता भाई,", "IB BATA BHAI,"), ("अगला कदम क्या हो?", "AGLA KADAM KYA HO?")]),
            ("cta", [("कमेंट में लिख दो।", "COMMENT MEIN LIKH DO!")])]},
]

DELIVERY = delivery.build(SPEC)   # catchy pace: quick builds, held beat, heavy punch
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

# the five steps: (name, km shown on the ring, ring colour, label)
AGNI = [("AGNI-I", 700, TEAL, "~700"), ("AGNI-II", 2000, SKY, "2,000+"), ("AGNI-III", 3000, SAFFRON, "3,000+"),
        ("AGNI-IV", 4000, GREEN, "~4,000"), ("AGNI-V", 5000, RED, "5,000+")]

HOT = {"700": TEAL, "5,000": RED, "AGNI": AMBER, "7": HI, "GUNA": HI, "1989": AMBER, "CHANDIPUR": AMBER,
       "ODISHA": AMBER, "AGNI-I": TEAL, "1": TEAL, "STAGE": AMBER, "SAFAR": HI, "AGNI-II": SKY, "2": SKY,
       "2,000": SKY, "3": HI, "AGNI-III": SAFFRON, "50": SAFFRON, "TON": SAFFRON, "BHAARI": SAFFRON,
       "3,000": SAFFRON, "AGNI-IV": GREEN, "AADHE": GREEN, "KAM": GREEN, "4,000": GREEN, "AGNI-V": RED,
       "CANISTER": AMBER, "JHATKE": SKY, "PAAR!": SKY, "PALAT": GREEN, "KHEL": GREEN, "GHANA": SAFFRON, "WAZAN?": SAFFRON, "SEEDHA": AMBER, "DIBBE": AMBER, "BAND": AMBER, "NISHAANE": RED, "GHANI": HI, "CHHALAANG": HI, "MHAARA": HI, "BHAI": AMBER, "2012": AMBER, "1,000": SAFFRON, "AAGE": SAFFRON, "SOLID": TEAL, "11": HI, "MARCH": HI, "2024": HI, "DIVYASTRA": HI, "KAI": RED, "WARHEAD": RED,
       "AGLA": HI, "KADAM": HI, "COMMENT": HI}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".—")] = HOT[_k]

# ============================================================ range board

CX, CY = 540, 600          # ring centre (central India)
KM_PX = 12.0               # 5,000 km -> ~417 px
LON0, LAT0 = 78.5, 22.5
DEG_LAT = 111.0 / KM_PX
DEG_LON = DEG_LAT * math.cos(math.radians(LAT0))
LABEL_ANG = math.radians(38)

# simplified outline of India (official boundary incl. all of J&K and Ladakh), lon/lat
INDIA = [
    (68.2, 23.7), (68.8, 24.3), (70.0, 24.2), (71.0, 24.6), (70.1, 25.2), (70.2, 26.3), (69.5, 26.6), (69.6, 27.2),
    (70.3, 27.9), (71.0, 27.8), (72.8, 28.9), (73.4, 29.9), (74.0, 30.0), (74.5, 31.0), (74.6, 32.5), (73.9, 33.5),
    (73.5, 34.7), (73.0, 35.6), (74.0, 36.6), (74.8, 37.0), (75.8, 36.8), (77.0, 35.7), (78.0, 35.5), (79.5, 35.6),
    (80.3, 35.3), (79.0, 34.3), (78.8, 33.0), (79.4, 32.6), (78.8, 31.4), (81.1, 30.2), (80.06, 28.84), (81.1, 28.6),
    (83.3, 27.4), (84.1, 27.4), (86.0, 26.6), (88.1, 26.5), (88.05, 27.3), (88.1, 27.9), (88.6, 28.1), (88.8, 27.4),
    (88.85, 26.95), (89.85, 26.78), (92.1, 26.85), (92.1, 27.8), (94.0, 29.3), (96.0, 29.4), (97.3, 28.2),
    (96.2, 27.3), (95.3, 26.6), (95.0, 25.5), (94.6, 24.6), (94.2, 23.8), (93.4, 23.0), (93.3, 22.0), (92.6, 22.0),
    (92.3, 23.5), (91.8, 23.4), (91.4, 24.1), (92.4, 24.3), (92.0, 25.1), (89.85, 25.3), (89.85, 26.0),
    (88.95, 26.25), (88.38, 26.45), (88.1, 25.6), (88.6, 24.2), (88.9, 22.0), (88.2, 21.8), (87.0, 21.0),
    (85.8, 19.8), (84.0, 18.3), (82.3, 16.6), (81.3, 16.3), (80.2, 15.5), (80.3, 13.1), (79.8, 11.9), (79.9, 10.3),
    (79.0, 9.3), (78.2, 8.9), (77.5, 8.1), (76.9, 8.6), (76.3, 9.9), (75.9, 11.0), (75.4, 11.8), (74.8, 12.9),
    (74.4, 14.3), (73.8, 15.5), (73.3, 17.0), (72.9, 19.0), (72.8, 20.4), (72.6, 21.4), (72.2, 21.6), (71.6, 21.0),
    (70.6, 20.9), (69.6, 21.8), (69.1, 22.4), (70.0, 22.9), (68.8, 23.2),
]
CHANDIPUR = (87.0, 21.45)


def proj(lon, lat):
    return CX + (lon - LON0) * DEG_LON, CY - (lat - LAT0) * DEG_LAT


def india(ctx, a=1.0, glow_a=0.0):
    pts = [proj(*p) for p in INDIA]
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    rgba(ctx, hexc("#3A2A14"), 0.95 * a)
    ctx.fill_preserve()
    rgba(ctx, AMBER, 0.9 * a)
    ctx.set_line_width(2.5)
    ctx.stroke()
    if glow_a:
        glow(ctx, CX, CY, 160, AMBER, glow_a)


def ring(ctx, km, u, c, w=6, a=1.0, fill=0.0):
    """Range ring of km drawn clockwise from the top up to fraction u, optional soft fill."""
    if u <= 0:
        return
    r = km / KM_PX
    if fill:
        ctx.arc(CX, CY, r, 0, math.tau)
        rgba(ctx, c, fill * a * clamp(u))
        ctx.fill()
    ctx.arc(CX, CY, r, -math.pi / 2, -math.pi / 2 + math.tau * clamp(u))
    rgba(ctx, c, a)
    ctx.set_line_width(w)
    ctx.stroke()


def ring_label(ctx, k, a=1.0):
    name, km, c, lab = AGNI[k]
    r = km / KM_PX
    x, y = CX + r * math.cos(LABEL_ANG), CY - r * math.sin(LABEL_ANG)
    circle(ctx, x, y, 7, c, a)
    text(ctx, f"{name.split('-')[1]}  {lab}", x + 14, y - 16, 28, c, font=MONO, anchor="l", a=a,
         stroke=(0, 0, 0), stroke_w=6)


def board(ctx, t, done, a=1.0):
    """Grid, India and the rings already earned (indices < done), dimmed by a."""
    for k in range(1, 6):
        ctx.arc(CX, CY, 1000 * k / KM_PX, 0, math.tau)
        rgba(ctx, AMBER, 0.08 * a)
        ctx.set_line_width(1.5)
        ctx.stroke()
    for ang in range(0, 360, 30):
        r0, r1 = 40, 5000 / KM_PX + 20
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        line(ctx, [(CX + r0 * c, CY + r0 * s), (CX + r1 * c, CY + r1 * s)], AMBER, 1, 0.06 * a)
    india(ctx, a)
    for k in range(done):
        ring(ctx, AGNI[k][1], 1, AGNI[k][2], 4, 0.55 * a)
        ring_label(ctx, k, 0.7 * a)


def agni(ctx, x, y, length, ang, t, stages=2, flame=1.0, a=1.0, c=(0.93, 0.92, 0.88)):
    """Drawn ballistic missile, centre (x, y), nose along ang; dark bands mark the stages."""
    d = length * 0.09
    L = length
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    if flame > 0:
        for k, (fc, fa) in enumerate(((RED, 0.55), (AMBER, 0.85), ((1, 0.97, 0.85), 0.95))):
            f = (1 + 0.22 * math.sin(t * 47 + k * 2.1)) * flame * (1 - 0.28 * k)
            ctx.move_to(-L / 2, -d * 0.45)
            ctx.line_to(-L / 2 - L * 0.4 * f, 0)
            ctx.line_to(-L / 2, d * 0.45)
            ctx.close_path()
            rgba(ctx, fc, fa * a)
            ctx.fill()
    rrect(ctx, -L / 2, -d / 2, L * 0.8, d, d * 0.2)
    rgba(ctx, c, a)
    ctx.fill()
    ctx.move_to(L * 0.3, -d / 2)
    ctx.curve_to(L * 0.42, -d / 2, L * 0.5, -d * 0.1, L * 0.5, 0)
    ctx.curve_to(L * 0.5, d * 0.1, L * 0.42, d / 2, L * 0.3, d / 2)
    ctx.close_path()
    rgba(ctx, shade(c, 0.85), a)
    ctx.fill()
    for s in range(1, stages + 1):   # stage joints
        xs = -L / 2 + L * 0.8 * s / (stages + 1)
        ctx.rectangle(xs - 2, -d / 2, 4, d)
        rgba(ctx, (0.2, 0.18, 0.15), a)
        ctx.fill()
    for sgn in (-1, 1):
        ctx.move_to(-L / 2, sgn * d / 2)
        ctx.line_to(-L / 2 - L * 0.03, sgn * d * 1.3)
        ctx.line_to(-L / 2 + L * 0.12, sgn * d / 2)
        ctx.close_path()
        rgba(ctx, STEEL, a)
        ctx.fill()
    ctx.restore()


def launch(ctx, t, u, stages, c, top=230):
    """Missile rises from the ring centre and fades out near the top (u = seconds since launch)."""
    if u <= 0 or u > 1.6:
        return
    k = ease_in_out(clamp(u / 1.3))
    y = lerp(CY - 40, top, k)
    a = 1 - clamp((u - 1.2) / 0.4)
    line(ctx, [(CX, CY - 30), (CX, y + 60)], INK, 10, 0.15 * a)
    agni(ctx, CX, y, 150, -math.pi / 2, t, stages=stages, a=a)


def counter(ctx, value, c, name, u, a=1.0):
    """Range readout panel below the board."""
    if u <= 0:
        return
    k = ease_out_cubic(u / 0.3)
    ctx.save()
    ctx.translate(540, 1085)
    ctx.scale(1, k)
    rrect(ctx, -420, -50, 840, 100, 16)
    rgba(ctx, (0.03, 0.02, 0.01), 0.92 * a)
    ctx.fill_preserve()
    rgba(ctx, c, a)
    ctx.set_line_width(4)
    ctx.stroke()
    text(ctx, name, -390, 0, 40, c, font=MONO, anchor="l", a=a)
    text(ctx, f"{int(round(value / 10) * 10):,} KM", 390, 0, 58, INK, font=MONO, anchor="r", a=a)
    ctx.restore()


def odometer(t, start, end, v0, v1):
    return lerp(v0, v1, ease_in_out(clamp((t - start) / max(end - start, 0.3))))


# ============================================================ scenes

class Hook(Cued):
    """Counter rolls 700 -> 5,000 while the five rings pop out; ~7x stamp; first flight from Chandipur, 1989."""

    def beats(self, d):
        c = self.cue
        return {"s": c("700", 0.05), "e": c("5,000", d * 0.15), "guna": c("GUNA", d * 0.45), "y": c("1989", d * 0.65),
                "ch": c("CHANDIPUR", d * 0.82)}

    def events(self, d):
        b = self.beats(d)
        ev = [(0.02, "boom"), (b["guna"], "thud"), (b["y"], "beep"), (b["ch"], "whoosh")]
        return ev + [(b["s"] + 0.25 * k, "zap") for k in range(5)]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx)
        dim = 1 - 0.55 * clamp((t - b["y"]) / 0.4)
        board(ctx, t, 0, dim)
        for k in range(5):
            u = t - b["s"] - 0.25 * k
            if u > 0:
                ring(ctx, AGNI[k][1], ease_out_cubic(u / 0.45), AGNI[k][2], 6, dim, fill=0.05)
                if u > 0.45:
                    ring_label(ctx, k, dim)
        v = odometer(t, b["s"], b["e"] + 0.6, 700, 5000)
        counter(ctx, v, HI, "AGNI RANGE", t - b["s"] + 0.1)
        if b["guna"] < t < b["y"]:
            stamp(ctx, 540, 300, t - b["guna"], -0.04, 420, 130, HI, [("~7 GUNA", 0, 96, HI)])
        u = t - b["y"]
        if u > 0:   # 1989: the first flight lifts off from the Odisha coast
            x, y = proj(*CHANDIPUR)
            for k in range(3):
                ring_u = (u * 1.2 - k * 0.3) % 1.2
                ctx.arc(x, y, 8 + 50 * ring_u, 0, math.tau)
                rgba(ctx, AMBER, max(0, 1 - ring_u) * 0.8)
                ctx.set_line_width(3)
                ctx.stroke()
            circle(ctx, x, y, 9, HI)
            tag(ctx, "1989 • CHANDIPUR", 540, 260, AMBER, u, size=46, sub="PEHLI AGNI UDAAN")
            uc = t - b["ch"]
            if uc > 0:
                k2 = ease_in_out(clamp(uc / 1.4))
                pts = [(lerp(x, x + 150, s), y - 380 * s * (1.4 - s)) for s in [i / 30 * k2 for i in range(31)]]
                line(ctx, pts, INK, 4, 0.6)
                if k2 < 1:
                    (ax, ay), (bx, by) = pts[-2], pts[-1]
                    agni(ctx, bx, by, 90, math.atan2(by - ay, bx - ax), t, stages=1)


class Step(Cued):
    """One Agni: launch from the centre, its ring grows, the counter counts up, then a fact stamp."""

    K = 0
    STAGES = 1
    FACT = "k"      # caption word that triggers the fact

    def beats(self, d):
        c = self.cue
        name = AGNI[self.K][0]
        return {"name": c(name, 0.2), "km": c(f"{AGNI[self.K][1]:,}", d * 0.45), "fact": c(self.FACT, d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["name"], "whoosh"), (b["name"] + 0.1, "engine", 0.8), (b["km"], "zap"),
                (b["km"] + 0.7, "pick"), (b["fact"], "boom")]

    def extra(self, ctx, t, b, d):
        pass

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx)
        k = self.K
        name, km, c, _ = AGNI[k]
        board(ctx, t, k)
        launch(ctx, t, t - b["name"], self.STAGES, c)
        u = t - b["km"]
        grow = ease_out_cubic(clamp(u / 0.8)) if u > 0 else 0
        ring(ctx, km, grow, c, 8, 1.0, fill=0.08)
        if grow >= 1:
            ring_label(ctx, k)
        prev = AGNI[k - 1][1] if k else 0
        counter(ctx, odometer(t, b["km"], b["km"] + 0.8, prev, km), c, name, t - b["name"] + 0.1)
        self.extra(ctx, t, b, d)


class A1(Step):
    K, STAGES, FACT = 0, 1, "STAGE"

    def extra(self, ctx, t, b, d):
        u = t - b["fact"]
        if u > 0:
            stamp(ctx, 540, 930, u, -0.03, 420, 110, TEAL, [("1 STAGE", 0, 80, TEAL)])
        u = t - self.cue("SAFAR", d * 0.8)
        if u > 0:
            tag(ctx, "SAFAR SHURU", 540, 270, TEAL, u, size=44)


class A2(Step):
    K, STAGES, FACT = 1, 2, "GUNA"

    def extra(self, ctx, t, b, d):
        u = t - self.cue("STAGE", d * 0.3)
        if u > 0:
            tag(ctx, "2 STAGE", 540, 270, SKY, u, size=44)
        u = t - b["fact"]
        if u > 0:   # x3: the old ring and the new one side by side
            stamp(ctx, 540, 930, u, -0.04, 480, 120, HI, [("700 → 2,000 = x3", 0, 66, HI)])


class A3(Step):
    K, STAGES, FACT = 2, 2, "TON"

    def extra(self, ctx, t, b, d):
        u = t - b["fact"]
        if u <= 0:
            return
        # weighing plate with the missile lying on it, needle swings to ~50 t
        k = ease_out_back(clamp(u / 0.4))
        ctx.save()
        ctx.translate(540, 300)
        ctx.scale(k, k)
        rrect(ctx, -300, -80, 600, 160, 18)
        rgba(ctx, (0.03, 0.02, 0.01), 0.92)
        ctx.fill_preserve()
        rgba(ctx, SAFFRON)
        ctx.set_line_width(4)
        ctx.stroke()
        agni(ctx, -110, -20, 300, 0, t, stages=2, flame=0)
        rrect(ctx, -270, 18, 330, 14, 6)
        rgba(ctx, STEEL)
        ctx.fill()
        text(ctx, "~50 TON", 185, 0, 48, SAFFRON, font=MONO)
        ctx.restore()


class A4(Step):
    K, STAGES, FACT = 3, 2, "AADHE"

    def extra(self, ctx, t, b, d):
        u = t - self.cue("WAZAN", d * 0.25)
        if u <= 0:
            return
        k = ease_out_cubic(clamp(u / 0.3))
        tilt = 0.22 * ease_out_back(clamp((t - b["fact"]) / 0.6)) if t > b["fact"] else 0.0
        ctx.save()
        ctx.translate(540, 300)
        ctx.scale(k, k)
        line(ctx, [(0, -20), (0, 110)], STEEL, 8)
        ctx.move_to(-40, 120)
        ctx.line_to(40, 120)
        ctx.line_to(0, 90)
        ctx.close_path()
        rgba(ctx, STEEL)
        ctx.fill()
        ctx.save()
        ctx.translate(0, -20)
        ctx.rotate(-tilt)          # heavier Agni-III side (left) goes down
        line(ctx, [(-300, 0), (300, 0)], STEEL, 8)
        for sx, lab, c, size in ((-230, "III", SAFFRON, 1.0), (230, "IV", GREEN, 0.6)):
            ctx.save()
            ctx.translate(sx, 0)
            ctx.rotate(tilt)
            line(ctx, [(-70, 0), (-70, 60), (70, 60), (70, 0)], STEEL, 3, 0.6)
            agni(ctx, 0, 40, 170 * size, 0, t, stages=2, flame=0, c=shade(c, 1.1))
            text(ctx, lab, 0, 100, 34, c, font=MONO)
            ctx.restore()
        ctx.restore()
        ctx.restore()
        if t > b["fact"]:
            stamp(ctx, 540, 930, t - b["fact"], -0.03, 460, 110, GREEN, [("WAZAN < 1/2", 0, 72, GREEN)])


class A5(Step):
    K, STAGES, FACT = 4, 3, "NISHAANE"

    def beats(self, d):
        b = super().beats(d)
        c = self.cue
        b["can"] = c("DIBBE", d * 0.35)
        b["div"] = c("DIVYASTRA", d * 0.6)
        b["one"] = c("EK", d * 0.78)
        return b

    def events(self, d):
        b = self.beats(d)
        return super().events(d) + [(b["can"], "thud"), (b["div"], "dingdong"), (b["one"], "beep")]

    def extra(self, ctx, t, b, d):
        u = t - b["can"]
        if 0 < u < b["div"] - b["can"] + 0.3:   # canister: a tube rises, the missile pops out of the top
            a = 1 - clamp((t - b["div"]) / 0.3)
            ctx.save()
            ctx.translate(880, 960)
            rrect(ctx, -34, -260 * ease_out_cubic(clamp(u / 0.4)), 68, 260 * ease_out_cubic(clamp(u / 0.4)), 10)
            rgba(ctx, shade(STEEL, 0.6), a)
            ctx.fill()
            ctx.restore()
            if u > 0.5:
                k = ease_out_cubic(clamp((u - 0.5) / 0.8))
                agni(ctx, 880, 690 - 260 * k, 190, -math.pi / 2, t, stages=3, flame=k, a=a)
            if u > 0.3:
                tag(ctx, "CANISTER", 880, 1000, AMBER, u - 0.3, size=30)
        u = t - b["div"]
        if u > 0:
            tag(ctx, "11 MARCH 2024", 540, 250, HI, u, size=40, sub="MISSION DIVYASTRA")
        u = t - b["one"]
        if u > 0:   # one bus, then several re-entry vehicles fan out to different points on the ring
            r = 5000 / KM_PX
            bus_y = lerp(CY - 60, CY - 230, ease_out_cubic(clamp(u / 0.6)))
            agni(ctx, CX, bus_y, 120, -math.pi / 2, t, stages=3, flame=1 - clamp(u / 0.6))
            n = 5
            for j in range(n):
                ang = math.radians(-150 + 30 * j)
                k = ease_in_out(clamp((t - b["fact"] - 0.05 * j) / 1.0))
                if k <= 0:
                    continue
                tx, ty = CX + r * 0.82 * math.cos(ang), CY + r * 0.82 * math.sin(ang)
                pts = [(lerp(CX, tx, s), lerp(bus_y, ty, s) - 120 * math.sin(math.pi * s)) for s in
                       [i / 24 * k for i in range(25)]]
                line(ctx, pts, RED, 4, 0.7)
                circle(ctx, *pts[-1], 10, HI)
            if t > b["fact"] + 0.4:
                stamp(ctx, 540, 930, t - b["fact"] + 0.15, -0.03, 520, 110, RED, [("MIRV: KAI NISHAANE", 0, 64, RED)])


class Ask(Cued):
    """All five rings dim behind the comment-prompt card (Lego ending 'prompt')."""

    def beats(self, d):
        c = self.cue
        return {"q": c("AGLA", d * 0.35), "cmt": c("COMMENT", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["q"] + 0.05, "pop"), (b["cmt"], "dingdong"), (b["cmt"] + 1.1, "pick"),
                (b["cmt"] + 2.2, "pick")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx)
        board(ctx, t, 5, 1 - 0.55 * clamp((t - b["q"]) / 0.4))
        if t < b["q"]:
            counter(ctx, 5000, HI, "700 → 5,000", t + 0.3)
        lego.ending(STORY, ctx, t, t - b["q"], t - b["cmt"], question=("AGLA KADAM", "KYA HO?"),
                    suggestions=("AGNI-6", "AUR RANGE", "AGNI PRIME", "AUR MIRV"), y=600)


SCENE_CLASSES = {"hook": Hook, "a1": A1, "a2": A2, "a3": A3, "a4": A4, "a5": A5, "ask": Ask}
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
        "Agni 1 Se Agni 5: 700 Se 5,000 KM Tak Ka Safar",
        "Agni Missile Ki Range: 5 Kadam, 7 Guna",
        "Agni-I vs Agni-V: Range Kitni Badhi?",
        "Agni 1, 2, 3, 4, 5: Har Missile Ki Range",
        "5,000 KM Se Zyada: Agni-V Tak Kaise Pahuncha Bharat",
        "Agni Series Explained: 1989 Se Mission Divyastra Tak",
        "Agni-V Ka MIRV: Ek Missile, Kai Nishaane",
        "Agni Missile Family: Range Ka Poora Safar",
        "Agni 5 Missile Range Kitni Hai? Poori Series",
        "700 KM Se 5,000 KM: Agni Missile Ki Kahani",
    ],
    "title": "Agni 1 Se Agni 5: 700 Se 5,000 KM Tak Ka Safar",   # creator's pick, still scored
    "thumb_text": "7 GUNA BADHI",
    "queries": ["agni missile range", "agni 5 range", "agni 1 se 5"],
    "description": """
Agni missile range: Agni 1 se Agni 5 tak, 700 KM se 5,000 KM se zyada, sirf 5 kadam me lagbhag 7 guna.
Agni 5 range 5,000 KM+, aur Mission Divyastra me ek missile se kai nishaane (MIRV).

Is Short me:
• Agni-I: 1 stage, range ~700 KM
• Agni-II: 2,000 KM se zyada (ek jhatke me lagbhag 3 guna)
• Agni-III: 3,000 KM se zyada, wazan ~50 ton
• Agni-IV: wazan Agni-III se aadhe se bhi kam, range ~4,000 KM
• Agni-V: 5,000 KM se zyada, canister (dibbe) se launch; 11 March 2024 ko Mission Divyastra me pehla MIRV test

Agni ka agla kadam kya hona chahiye? Comment me likho.
Bharat ki pehli desi missile Prithvi ki kahani bhi dekho, Reality Shift pe.

Note: rings range ka schematic comparison hain, asli map nahi. Range ke public figures payload ke hisaab se
alag-alag sources me thode alag hain; yahan commonly reported numbers liye gaye hain.
""",
    "tags": ["agni missile", "agni 5", "agni missile range", "agni 1 to 5", "agni v", "mission divyastra",
             "mirv", "drdo", "indian missiles", "agni 5 range", "agni missile kitni door", "ballistic missile india", "indian defence shorts",
             "defence hindi", "reality shift"],
    "hashtags": ["#Shorts", "#Agni5", "#DRDO"],
}


def thumbnail(ctx):
    """1080x1920 cover: '7 GUNA / BADHI' over the five range rings with an Agni rising from the centre."""
    bg(ctx, (0.07, 0.04, 0.02), (0.01, 0.01, 0.01))
    ctx.save()
    ctx.translate(0, 560)
    board(ctx, 0, 0, 0.9)
    for k in range(5):
        ring(ctx, AGNI[k][1], 1, AGNI[k][2], 7 + k, 0.95, fill=0.04)
        ring_label(ctx, k, 0.95)
    agni(ctx, CX + 10, CY - 230, 300, -math.pi / 2, 0.3, stages=3)
    ctx.restore()
    g = cairo.LinearGradient(0, 0, 0, 760)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.95)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 760)
    ctx.set_source(g)
    ctx.fill()
    vignette(ctx)
    glow(ctx, 540, 360, 520, AMBER, 0.25)
    text(ctx, "7 GUNA", 540, 260, 230, HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "BADHI", 540, 500, 220, INK, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    tag(ctx, "I  →  V", 540, 680, RED, 1.0, size=56)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, INK, a=0.7)


def main() -> None:
    import upload_kit
    story = importlib.import_module("generate_agni_short")
    engine.make_frame = lego.frame_maker(story)
    final = engine.render(story, "edge")
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
