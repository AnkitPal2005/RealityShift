"""Reality Shift Short - "Kya India ne S-400 cancel kiya? Project Kusha ka sach" (~50s fact-check).

Usage:
  python generate_s400_kusha_short.py

Rumour-check Short on the Lego template: intel-file header, word-chip captions, shutter wipes, amber palette,
poll ending. Seven scenes: the viral claim on a phone, stamped "SACH: ULTA" -> 2018 deal, 4 of 5 squadrons
delivered, 5th on the way -> Russia offers 5 more (~Rs 50,000 cr), India still deciding -> Project Kusha, first
flight test 23 Jul 2026 off Odisha -> M1/M2/M3 range arcs vs the S-400's 400 km -> "aaj Russ ki dhaal, kal apni"
-> poll: 5 more S-400 or wait for Kusha?
Not the old reality_shift_kusha Short (2025 hype version): new angle, new facts, fresh script and drawings.
"""

import importlib
import json
import math

import cairo

import engine
import lego
from engine import *  # noqa: F401,F403
from generate_brahmos_lego_short import bg, tag
from generate_chabahar_short import Cued
from generate_rupee_short import VOICE_TONES
from stories.reality_shift import flag, stamp

TOPIC = "S-400 CANCEL? KUSHA FACT-CHECK"
OUTPUTS = {"edge": "s400_kusha_short.mp4"}
LEGO = {"header": "intel", "caption": "chip", "transition": "shutter", "palette": "amber", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.3
TAIL_PAD = 0.35
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 104
MUSIC_STYLE = "tension"    # rumour-check needs suspense (BrahMos was pulse @ 118)
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
    "S-400: 2018 contract, five squadrons, ~USD 5.43 bn; four delivered, fifth due by Nov 2026 "
    "(Indian Defence News, Sept 2026; The Week, 12 Jan 2026; Tribune India)",
    "Russia's proposal for five more S-400 squadrons, ~Rs 50,000 crore, under consideration, no contract signed "
    "(Indian Defence News, Sept 2026; DefenceXP)",
    "S-400 used in Operation Sindoor, May 2025 (The Week, 2 Jun 2025)",
    "Project Kusha first flight test 23 Jul 2026, APJ Abdul Kalam Island off Odisha, successful interception of an "
    "electronic target; M1 ~150 km, M2 ~250 km, M3 ~350-400 km; M2/M3 testing over the next 2-3 years; meant to work "
    "alongside the S-400 (MoD via India Sentinels, Jul 2026; The Diplomat, Jul 2026; Business Today, 24 Jul 2026)",
    "No report of any S-400 cancellation found in Indian or Russian official statements or major outlets "
    "(checked 5 Nov 2026)",
]

# each line: (tone, [(spoken Hindi, Hinglish caption), ...], pause after)
SPEC = [
    {"key": "rumor", "accent": RED, "text": "SACH: ULTA",
     "visual": "A phone with a viral 'S-400 CANCEL' post, TRENDING badge; a red stamp 'SACH: ULTA' slams over it",
     "vo": [("hook", [("इंटरनेट पर दावा है—", "INTERNET PAR DAAVA HAI—"), ("भारत ने चुपके से", "BHARAT NE CHUPKE SE"),
                      ("रूस का एस चार सौ", "RUSS KA S-400"), ("कैंसल कर दिया।", "CANCEL KAR DIYA!")], 0.45),
            ("punch", [("सच?", "SACH?"), ("बिल्कुल उल्टा।", "BILKUL ULTA!")], 0)]},
    {"key": "deal", "accent": HI, "text": "4/5 DELIVERED",
     "visual": "2018 DEAL card; five launcher rows, four tick to DELIVERED, the fifth shows a truck on the road",
     "vo": [("tell", [("दो हज़ार अठारह की डील—", "2018 KI DEAL—"), ("पाँच स्क्वाड्रन,", "5 SQUADRON,"),
                      ("पाँच अरब डॉलर से ज़्यादा।", "5 BILLION DOLLAR+")], 0.35),
            ("punch", [("चार भारत पहुँच चुके हैं,", "4 BHARAT PAHUNCH CHUKE HAIN,"),
                       ("पाँचवाँ रास्ते में है।", "PAANCHVAN RASTE MEIN HAI.")], 0)]},
    {"key": "offer", "accent": AMBER, "text": "+5 OFFER",
     "visual": "Shield dome stops incoming dots (Operation Sindoor); Russia flag + '+5 SQUADRON' offer, ~Rs 50,000 cr; "
               "file card STATUS: VICHAAR MEIN",
     "vo": [("tell", [("ऑपरेशन सिंदूर में", "OPERATION SINDOOR MEIN"), ("ये काम आया,", "YEH KAAM AAYA,")], 0.3),
            ("build", [("और अब रूस ने", "AUR AB RUSS NE"), ("पाँच और स्क्वाड्रन", "5 AUR SQUADRON"),
                       ("ऑफ़र किए हैं—", "OFFER KIYE HAIN—"), ("करीब पचास हज़ार करोड़ के।", "KAREEB ₹50,000 CRORE!")], 0.35),
            ("low", [("भारत अभी", "BHARAT ABHI"), ("सोच रहा है।", "SOCH RAHA HAI.")], 0)]},
    {"key": "kusha", "accent": TEAL, "text": "KUSHA TEST",
     "visual": "PROJECT KUSHA title; Odisha coast at night, interceptor climbs from the island and meets an "
               "electronic target, '23 JULY 2026' and 'TEST SAFAL' cards",
     "vo": [("sly", [("तो फिर", "TOH PHIR"), ("प्रोजेक्ट कुशा क्या है?", "PROJECT KUSHA KYA HAI?")], 0.35),
            ("tell", [("डीआरडीओ का अपना", "DRDO KA APNA"), ("लंबी दूरी का एयर डिफ़ेंस।", "LONG-RANGE AIR DEFENCE.")], 0.3),
            ("punch", [("तेईस जुलाई,", "23 JULY,"), ("ओडिशा तट—", "ODISHA TAT—"), ("पहला टेस्ट,", "PEHLA TEST,"),
                       ("इंटरसेप्शन सफल।", "INTERCEPTION SAFAL!")], 0)]},
    {"key": "range", "accent": HI, "text": "150-400 KM",
     "visual": "Range arcs from a radar: M1 150 km, M2 250 km, M3 350-400 km; the S-400's 400 km ring lands on M3",
     "vo": [("tell", [("तीन मिसाइलें—", "3 MISSILES—"), ("एम वन, करीब डेढ़ सौ किलोमीटर,", "M1: ~150 KM,"),
                      ("एम टू, ढाई सौ,", "M2: ~250 KM,")], 0.3),
            ("punch", [("और एम थ्री—", "AUR M3—"), ("साढ़े तीन सौ से चार सौ।", "350 SE 400 KM!"),
                       ("यानी एस चार सौ जितनी पहुँच।", "YAANI S-400 JITNI PAHUNCH!")], 0)]},
    {"key": "plan", "accent": SAFFRON, "text": "AAJ + KAL",
     "visual": "Test timeline bar (M2/M3: 2-3 years); S-400 shield 'AAJ' beside a Kusha shield 'KAL' filling up",
     "vo": [("low", [("पर एम टू और एम थ्री के टेस्ट", "PAR M2 AUR M3 KE TEST"),
                     ("अभी दो-तीन साल चलेंगे।", "ABHI 2-3 SAAL CHALENGE.")], 0.35),
            ("build", [("इसलिए प्लान साफ़ है—", "ISLIYE PLAN SAAF HAI—")], 0.2),
            ("punch", [("आज रूस की ढाल,", "AAJ RUSS KI DHAAL,"), ("कल अपनी।", "KAL APNI!")], 0)]},
    {"key": "ask", "accent": HI, "text": "POLL",
     "visual": "Dim range arcs behind the poll card: '5 AUR S-400 LEIN? / YA KUSHA KA WAIT?'",
     "vo": [("ask", [("आप बताओ—", "AAP BATAO—"), ("पाँच और एस चार सौ लें,", "5 AUR S-400 LEIN,"),
                     ("या कुशा का इंतज़ार?", "YA KUSHA KA INTEZAAR?")], 0.4),
            ("cta", [("कमेंट में लिखो।", "COMMENT MEIN LIKHO!")], 0)]},
]

DELIVERY = {s["key"]: [(VOICE_TONES[tone], " ".join(hi for hi, _ in chunks), pause) for tone, chunks, pause in s["vo"]]
            for s in SPEC}
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {"DAAVA": AMBER, "CHUPKE": RED, "S-400": HI, "CANCEL": RED, "SACH?": HI, "ULTA!": RED, "2018": AMBER,
       "5": HI, "BILLION": HI, "DOLLAR+": HI, "4": GREEN, "PAHUNCH": GREEN, "PAANCHVAN": HI, "RASTE": HI,
       "SINDOOR": SAFFRON, "RUSS": AMBER, "OFFER": HI, "₹50,000": HI, "CRORE!": HI, "SOCH": AMBER,
       "KUSHA": TEAL, "DRDO": TEAL, "LONG-RANGE": TEAL, "23": TEAL, "JULY": TEAL, "ODISHA": TEAL,
       "SAFAL!": GREEN, "M1": TEAL, "M2": AMBER, "M3": HI, "~150": TEAL, "~250": AMBER, "350": HI, "400": HI,
       "2-3": AMBER, "SAAL": AMBER, "AAJ": AMBER, "DHAAL": AMBER, "KAL": SAFFRON, "APNI!": SAFFRON,
       "INTEZAAR?": TEAL, "COMMENT": HI}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".")] = HOT[_k]


# ============================================================ props

def launcher(ctx, x, y, s, c=STEEL, a=1.0, elev=0.75):
    """S-400-style launcher truck, centred on (x, y) at the wheel line; tubes raised by elev radians."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.save()  # tubes, pivoting at the rear of the bed
    ctx.translate(-120, -48)
    ctx.rotate(-elev)
    for k in range(4):
        rrect(ctx, 0, -14 - 26 * k, 250, 22, 6)
        rgba(ctx, shade(c, 0.85 - 0.08 * k), a)
        ctx.fill()
    ctx.restore()
    rrect(ctx, -160, -50, 250, 34, 6)
    rgba(ctx, shade(c, 0.7), a)
    ctx.fill()
    rrect(ctx, 95, -78, 70, 62, 10)
    rgba(ctx, shade(c, 0.8), a)
    ctx.fill()
    rrect(ctx, 125, -70, 30, 22, 4)
    rgba(ctx, (0.1, 0.12, 0.16), a)
    ctx.fill()
    for wx in (-130, -80, -30, 60, 130):
        circle(ctx, wx, -8, 17, (0.08, 0.08, 0.09), a)
        circle(ctx, wx, -8, 7, shade(c, 0.6), a)
    ctx.restore()


def interceptor(ctx, x, y, length, ang, t, a=1.0):
    """Slim white SAM with a short flame, nose along ang (drawn here, not the BrahMos body)."""
    d = length * 0.07
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    for k, (c, al) in enumerate(((RED, 0.5), (AMBER, 0.85), ((1, 1, 0.9), 0.95))):
        f = (1 + 0.25 * math.sin(t * 50 + k * 2)) * (1 - 0.3 * k)
        ctx.move_to(-length / 2, -d * 0.4)
        ctx.line_to(-length / 2 - length * 0.45 * f, 0)
        ctx.line_to(-length / 2, d * 0.4)
        ctx.close_path()
        rgba(ctx, c, al * a)
        ctx.fill()
    rrect(ctx, -length / 2, -d / 2, length * 0.82, d, d / 2)
    rgba(ctx, (0.94, 0.95, 0.97), a)
    ctx.fill()
    ctx.move_to(length * 0.32, -d / 2)
    ctx.line_to(length / 2, 0)
    ctx.line_to(length * 0.32, d / 2)
    ctx.close_path()
    rgba(ctx, (0.85, 0.86, 0.9), a)
    ctx.fill()
    for sgn in (-1, 1):
        ctx.move_to(-length / 2, sgn * d / 2)
        ctx.line_to(-length / 2 - length * 0.04, sgn * d * 1.4)
        ctx.line_to(-length / 2 + length * 0.12, sgn * d / 2)
        ctx.close_path()
        rgba(ctx, STEEL, a)
        ctx.fill()
    ctx.restore()


def shield_path(ctx, cx, cy, w, h):
    ctx.move_to(cx - w / 2, cy - h / 2)
    ctx.line_to(cx + w / 2, cy - h / 2)
    ctx.line_to(cx + w / 2, cy - h * 0.05)
    ctx.curve_to(cx + w / 2, cy + h * 0.28, cx + w * 0.2, cy + h * 0.42, cx, cy + h / 2)
    ctx.curve_to(cx - w * 0.2, cy + h * 0.42, cx - w / 2, cy + h * 0.28, cx - w / 2, cy - h * 0.05)
    ctx.close_path()


def shield(ctx, cx, cy, w, h, c, fill=1.0, a=1.0):
    """Shield outline in c, filled from the bottom up to fraction fill."""
    shield_path(ctx, cx, cy, w, h)
    rgba(ctx, (0.03, 0.02, 0.01), 0.9 * a)
    ctx.fill()
    if fill > 0:
        ctx.save()
        shield_path(ctx, cx, cy, w, h)
        ctx.clip()
        top = cy + h / 2 - h * fill
        g = cairo.LinearGradient(0, top, 0, cy + h / 2)
        g.add_color_stop_rgba(0, *c, 0.85 * a)
        g.add_color_stop_rgba(1, *shade(c, 0.45), 0.85 * a)
        ctx.rectangle(cx - w / 2, top, w, h * fill + 2)
        ctx.set_source(g)
        ctx.fill()
        if fill < 1:
            line(ctx, [(cx - w / 2, top), (cx + w / 2, top)], (1, 1, 1), 4, 0.8 * a)
        ctx.restore()
    shield_path(ctx, cx, cy, w, h)
    rgba(ctx, c, a)
    ctx.set_line_width(8)
    ctx.stroke()


def arc_band(ctx, cx, cy, r, u, c, w=6, a=1.0, dash=None):
    """Upper half-circle of radius r, drawn from the left up to fraction u."""
    if u <= 0:
        return
    if dash:
        ctx.set_dash(dash)
    ctx.arc(cx, cy, r, math.pi, math.pi + math.pi * clamp(u))
    rgba(ctx, c, a)
    ctx.set_line_width(w)
    ctx.stroke()
    ctx.set_dash([])


def range_arcs(ctx, t, a=1.0, cx=540, cy=1080, px=2.1, upto=4):
    """Kusha M1/M2/M3 arcs and the S-400 400 km ring (static version for the poll backdrop)."""
    for k, (km, c) in enumerate(((150, TEAL), (250, AMBER), (375, HI))):
        if k < upto:
            arc_band(ctx, cx, cy, km * px, 1, c, 5, 0.6 * a)
    arc_band(ctx, cx, cy, 400 * px, 1, RED, 4, 0.5 * a, dash=[20, 14])


# ============================================================ scenes

class Rumor(Cued):
    """Phone with the viral claim; 'SACH: ULTA' slams over it."""

    def beats(self, d):
        c = self.cue
        return {"chupke": c("CHUPKE", d * 0.2), "cancel": c("CANCEL", d * 0.5), "sach": c("SACH", d * 0.72),
                "ulta": c("ULTA", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (0.25, "pop"), (b["chupke"], "beep"), (b["cancel"], "alarm"), (b["sach"], "thud"),
                (b["ulta"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx, (0.07, 0.03, 0.02), (0.01, 0.01, 0.01))
        dim = 1 - 0.5 * clamp((t - b["sach"]) / 0.3)
        pop = max(ease_out_back(clamp(t / 0.4)), 0.01)
        ctx.save()
        ctx.translate(540, 640)
        ctx.scale(pop, pop)
        ctx.rotate(-0.03 + 0.01 * math.sin(t * 1.5))
        rrect(ctx, -300, -440, 600, 880, 60)  # phone
        rgba(ctx, (0.12, 0.12, 0.14), dim)
        ctx.fill()
        rrect(ctx, -275, -410, 550, 820, 40)
        rgba(ctx, (0.93, 0.93, 0.95), dim)
        ctx.fill()
        rrect(ctx, -60, -400, 120, 22, 11)
        rgba(ctx, (0.12, 0.12, 0.14), dim)
        ctx.fill()
        circle(ctx, -200, -310, 42, AMBER, dim)  # post header
        text(ctx, "VIRAL POST", -140, -325, 34, (0.1, 0.1, 0.12), a=dim, anchor="l")
        text(ctx, "forwarded many times", -140, -285, 24, (0.4, 0.4, 0.45), bold=False, a=dim, anchor="l")
        if int(t * 3) % 2 == 0 or t > b["sach"]:
            rrect(ctx, 90, -350, 160, 46, 23)
            rgba(ctx, RED, dim)
            ctx.fill()
            text(ctx, "TRENDING", 170, -327, 24, (1, 1, 1), a=dim)
        lines = (("BREAKING:", RED, 0.0), ("INDIA NE", (0.1, 0.1, 0.12), b["chupke"] - 0.3),
                 ("S-400", (0.1, 0.1, 0.12), b["chupke"]), ("CANCEL", RED, b["cancel"]),
                 ("KAR DIYA!", (0.1, 0.1, 0.12), b["cancel"] + 0.2))
        for k, (s, c, start) in enumerate(lines):
            if t > start:
                k2 = ease_out_back(clamp((t - start) / 0.25))
                ctx.save()
                ctx.translate(0, -170 + 105 * k)
                ctx.scale(k2, k2)
                text(ctx, s, 0, 0, 92, c, font=CAPTION_FONT, bold=False, a=dim)
                ctx.restore()
        for k, lab in enumerate(("SHARE", "LIKE", "FWD")):
            rrect(ctx, -240 + k * 170, 330, 140, 50, 25)
            rgba(ctx, (0.85, 0.85, 0.88), dim)
            ctx.fill()
            text(ctx, lab, -170 + k * 170, 355, 24, (0.3, 0.3, 0.35), a=dim)
        ctx.restore()
        u = t - b["sach"]
        if u > 0:  # a red slash across the claim, then the verdict stamp
            k = ease_out_cubic(u / 0.25)
            line(ctx, [(170, 330), (lerp(170, 910, k), lerp(330, 960, k))], RED, 22, 0.9)
            if t > b["ulta"] - 0.05:
                stamp(ctx, 540, 1010, t - b["ulta"] + 0.05, -0.06, 760, 180, RED, [("SACH: ULTA", -8, 120, RED)])
            else:
                stamp(ctx, 540, 1010, u, -0.06, 760, 180, HI, [("SACH?", -8, 120, HI)])


class Deal(Cued):
    """2018 deal card; five launcher rows, four tick DELIVERED, the fifth is on the road."""

    ROWS = (330, 480, 630, 780, 930)

    def beats(self, d):
        c = self.cue
        return {"sq": c("SQUADRON", d * 0.15), "usd": c("BILLION", d * 0.3), "four": c("PAHUNCH", d * 0.55),
                "five": c("RASTE", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        ev = [(0.02, "thud"), (b["usd"], "kaching")]
        ev += [(b["sq"] + 0.12 * k, "pop") for k in range(5)]
        ev += [(b["four"] + 0.22 * k, "pick") for k in range(4)]
        return ev + [(b["five"], "whoosh"), (b["five"] + 0.3, "beep")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx)
        text(ctx, "2018 DEAL", 70, 225, 64, HI, font=CAPTION_FONT, bold=False, anchor="l",
             a=clamp(t / 0.3))
        if t > b["usd"]:
            tag(ctx, "$5 BILLION+", 800, 225, HI, t - b["usd"], size=44)
        for k, y in enumerate(self.ROWS):
            u = t - b["sq"] - 0.12 * k
            if u <= 0:
                continue
            slide = ease_out_cubic(u / 0.35)
            x0 = lerp(-500, 0, slide)
            rrect(ctx, 60 + x0, y - 62, W - 120, 124, 18)
            rgba(ctx, (0.04, 0.03, 0.02), 0.9)
            ctx.fill()
            done = k < 4 and t > b["four"] + 0.22 * k
            moving = k == 4 and t > b["five"]
            c = GREEN if done else (HI if moving else shade(AMBER, 0.5))
            rrect(ctx, 60 + x0, y - 62, W - 120, 124, 18)
            rgba(ctx, c, 0.9 if (done or moving) else 0.4)
            ctx.set_line_width(4)
            ctx.stroke()
            if k == 4 and moving:  # the fifth one drives in along a dashed road
                ctx.set_dash([24, 16])
                line(ctx, [(120, y + 40), (620, y + 40)], HI, 4, 0.6)
                ctx.set_dash([])
                lx = lerp(150, 330, ease_in_out(clamp((t - b["five"]) / 1.2)))
                launcher(ctx, lx + x0, y + 28, 0.45, STEEL, elev=0.0)
            else:
                launcher(ctx, 220 + x0, y + 28, 0.45, STEEL if done else shade(STEEL, 0.45), elev=0.6)
            text(ctx, f"SQUADRON {k + 1}", 420 + x0, y - 20, 34, INK, font=MONO, anchor="l")
            if done:
                k2 = ease_out_back(clamp((t - b["four"] - 0.22 * k) / 0.3))
                ctx.save()
                ctx.translate(900 + x0, y)
                ctx.scale(k2, k2)
                circle(ctx, 0, 0, 40, GREEN)
                line(ctx, [(-18, 0), (-4, 15), (20, -14)], (0.03, 0.06, 0.03), 9)
                ctx.restore()
                text(ctx, "DELIVERED", 420 + x0, y + 26, 30, GREEN, font=MONO, anchor="l")
            elif moving:
                text(ctx, "RASTE MEIN", 660 + x0, y + 26, 30, HI, font=MONO, anchor="l",
                     a=0.6 + 0.4 * math.sin(t * 6))
            else:
                text(ctx, "STATUS ?", 420 + x0, y + 26, 30, shade(AMBER, 0.7), font=MONO, anchor="l")
        if t > b["four"] + 1.0:
            stamp(ctx, 540, 1065, t - b["four"] - 1.0, -0.03, 520, 120, GREEN, [("4 / 5 AA CHUKE", 0, 74, GREEN)])


class Offer(Cued):
    """Shield dome stops incoming dots; Russia offers 5 more squadrons; the file says VICHAAR MEIN."""

    def beats(self, d):
        c = self.cue
        return {"russ": c("RUSS", d * 0.25), "five": c("SQUADRON", d * 0.4), "cr": c("CRORE", d * 0.6),
                "soch": c("SOCH", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (0.4, "zap"), (0.8, "zap"), (1.2, "zap"), (b["russ"], "pop"), (b["five"], "boom"),
                (b["cr"], "kaching"), (b["soch"], "tick"), (b["soch"] + 0.4, "tock"), (b["soch"] + 0.8, "tick")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx, (0.05, 0.03, 0.02), (0.01, 0.01, 0.02))
        fade = 1 - clamp((t - b["russ"]) / 0.4)
        # dome over a ground line; dots fall and burst on it
        gx, gy, r = 540, 760, 360
        ctx.arc(gx, gy, r, math.pi, 2 * math.pi)
        rgba(ctx, AMBER, 0.12 * fade)
        ctx.fill()
        ctx.arc(gx, gy, r, math.pi, 2 * math.pi)
        rgba(ctx, AMBER, 0.8 * fade)
        ctx.set_line_width(6)
        ctx.stroke()
        line(ctx, [(100, gy), (980, gy)], AMBER, 4, 0.6 * fade)
        launcher(ctx, 540, gy - 4, 0.6, STEEL, a=fade)
        for k, (sx, hit) in enumerate(((240, 0.4), (620, 0.8), (880, 1.2))):
            u = t - (hit - 0.6)
            if 0 < u < 0.6:
                ang = math.pi + math.pi * (sx - 180) / 720
                hx, hy = gx + r * math.cos(ang), gy + r * math.sin(ang)
                k2 = u / 0.6
                circle(ctx, lerp(sx, hx, k2), lerp(180, hy, k2), 10, RED, fade)
            elif 0.6 <= u < 1.2:
                ang = math.pi + math.pi * (sx - 180) / 720
                hx, hy = gx + r * math.cos(ang), gy + r * math.sin(ang)
                ring = (u - 0.6) / 0.6
                ctx.arc(hx, hy, 10 + 50 * ring, 0, math.tau)
                rgba(ctx, HI, (1 - ring) * fade)
                ctx.set_line_width(5)
                ctx.stroke()
        if fade > 0.5:
            tag(ctx, "OPERATION SINDOOR • 2025", 540, 300, SAFFRON, t, size=40)
        u = t - b["russ"]
        if u > 0:
            pop = ease_out_back(u / 0.35)
            ctx.save()
            ctx.translate(540, 330)
            ctx.scale(pop, pop)
            flag(ctx, -170, -110, 340, 220, "ru", t)
            ctx.restore()
        u = t - b["five"]
        if u > 0:
            stamp(ctx, 540, 600, u, -0.04, 640, 150, HI, [("+5 SQUADRON", -6, 104, HI)])
        u = t - b["cr"]
        if u > 0:
            tag(ctx, "~₹50,000 CRORE", 540, 790, HI, u, size=58)
        u = t - b["soch"]
        if u > 0:  # file card: status pending, deal not signed
            k = ease_out_cubic(u / 0.3)
            ctx.save()
            ctx.translate(540, 990)
            ctx.scale(1, k)
            rrect(ctx, -400, -95, 800, 190, 14)
            rgba(ctx, (0.03, 0.02, 0.01), 0.95)
            ctx.fill_preserve()
            rgba(ctx, AMBER)
            ctx.set_line_width(4)
            ctx.stroke()
            text(ctx, "STATUS: VICHAAR MEIN", -360, -36, 44, AMBER, font=MONO, anchor="l")
            dots = "." * (1 + int(t * 3) % 3)
            text(ctx, "DEAL SIGN: ABHI NAHI" + dots, -360, 40, 36, INK, font=MONO, anchor="l", a=0.85)
            ctx.restore()


class Kusha(Cued):
    """PROJECT KUSHA title, then the Odisha-coast flight test: interceptor meets an electronic target."""

    LAUNCH = (230, 890)
    HIT = (700, 400)

    def beats(self, d):
        c = self.cue
        return {"name": c("KUSHA", d * 0.08), "drdo": c("DRDO", d * 0.25), "date": c("23", d * 0.5),
                "test": c("PEHLA", d * 0.72), "hit": c("SAFAL", d * 0.88)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["name"], "dingdong"), (b["drdo"], "pop"), (b["date"], "beep"),
                (b["test"], "whoosh"), (b["test"] + 0.2, "engine", 0.9), (b["hit"], "boom"), (b["hit"] + 0.3, "pick")]

    def target(self, t, b):
        k = clamp((t - b["date"]) / max(b["hit"] - b["date"], 0.5))
        return lerp(1140, self.HIT[0], k), lerp(300, self.HIT[1], k)

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx, (0.02, 0.03, 0.06), (0.01, 0.02, 0.03))
        for i in range(50):
            circle(ctx, rnd(i, 31) * W, 180 + rnd(i, 33) * 620, 1.5 + 2 * rnd(i, 35), INK, 0.2 + 0.3 * rnd(i, 37))
        sea_y = 900
        ctx.rectangle(0, sea_y, W, 300)
        g = cairo.LinearGradient(0, sea_y, 0, sea_y + 300)
        g.add_color_stop_rgb(0, 0.04, 0.15, 0.24)
        g.add_color_stop_rgb(1, 0.01, 0.03, 0.06)
        ctx.set_source(g)
        ctx.fill()
        for k in range(4):
            pts = [(x, sea_y + 20 + 26 * k + 5 * math.sin(x * 0.02 + t * 2 + k)) for x in range(0, W + 1, 20)]
            line(ctx, pts, SKY, 2, 0.3 - 0.06 * k)
        ctx.move_to(90, sea_y + 4)  # the island
        ctx.curve_to(150, sea_y - 40, 330, sea_y - 40, 380, sea_y + 4)
        ctx.close_path()
        rgba(ctx, hexc("#2E4A3A"))
        ctx.fill()
        text(ctx, "ODISHA TAT", 235, sea_y + 70, 28, TEAL, font=MONO, a=0.7)
        if t < b["date"]:  # title card first
            pop = ease_out_back(clamp((t - b["name"]) / 0.35))
            if pop > 0:
                ctx.save()
                ctx.translate(540, 470)
                ctx.scale(pop, pop)
                glow(ctx, 0, 0, 380, TEAL, 0.3)
                text(ctx, "PROJECT", 0, -80, 90, INK, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=10)
                text(ctx, "KUSHA", 0, 50, 190, TEAL, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=14)
                ctx.restore()
            if t > b["drdo"]:
                tag(ctx, "DRDO • LONG-RANGE SAM", 540, 690, TEAL, t - b["drdo"], size=40)
            return
        tag(ctx, "23 JULY 2026", 540, 230, TEAL, t - b["date"], size=48)
        tx, ty = self.target(t, b)
        if t < b["hit"]:  # electronic target: a hollow diamond with a trail
            for j in range(8):
                circle(ctx, tx + 22 * j, ty - 4 * j, 6 - 0.6 * j, RED, 0.5 * (1 - j / 8))
            ctx.move_to(tx, ty - 22)
            for px, py in ((tx + 22, ty), (tx, ty + 22), (tx - 22, ty)):
                ctx.line_to(px, py)
            ctx.close_path()
            rgba(ctx, RED)
            ctx.set_line_width(5)
            ctx.stroke()
            text(ctx, "ELECTRONIC TARGET", min(tx + 10, 880), ty - 50, 24, RED, font=MONO, a=0.85)
        u = t - b["test"]
        if u > 0:
            k = clamp(u / max(b["hit"] - b["test"], 0.4))
            (x0, y0), (x1, y1) = self.LAUNCH, self.HIT
            cxp, cyp = x0 + 60, y1 - 60
            pts = [((1 - s) ** 2 * x0 + 2 * (1 - s) * s * cxp + s * s * x1,
                    (1 - s) ** 2 * y0 + 2 * (1 - s) * s * cyp + s * s * y1) for s in [i / 40 * k for i in range(41)]]
            line(ctx, pts, (1, 1, 1), 10, 0.18)
            line(ctx, pts, INK, 3, 0.6)
            if k < 1:
                (ax, ay), (bx, by) = pts[-2], pts[-1]
                interceptor(ctx, bx, by, 150, math.atan2(by - ay, bx - ax), t)
            tag(ctx, "PEHLA TEST", 540, 330, AMBER, u, size=40)
        u = t - b["hit"]
        if u > 0:
            hx, hy = self.HIT
            for k in range(3):
                ring = clamp(u * 1.4 - k * 0.2)
                if 0 < ring < 1:
                    ctx.arc(hx, hy, 20 + 160 * ring, 0, math.tau)
                    rgba(ctx, (HI, AMBER, RED)[k], 1 - ring)
                    ctx.set_line_width(8)
                    ctx.stroke()
            glow(ctx, hx, hy, 180 * clamp(1 - u), HI, 0.8)
            stamp(ctx, 540, 1050, u - 0.2, -0.04, 640, 140, GREEN, [("TEST SAFAL", 0, 96, GREEN)])


class Range(Cued):
    """Range arcs from one radar: M1 150 km, M2 250 km, M3 350-400 km; the S-400's 400 km ring lands on M3."""

    CX, CY, PX = 540, 1080, 2.1

    def beats(self, d):
        c = self.cue
        return {"m1": c("M1", d * 0.15), "m2": c("M2", d * 0.38), "m3": c("M3", d * 0.55), "s4": c("S-400", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["m1"], "zap"), (b["m2"], "zap"), (b["m3"], "zap"), (b["m3"] + 0.4, "thud"),
                (b["s4"], "dingdong")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx)
        cx, cy, px = self.CX, self.CY, self.PX
        for k in range(1, 9):  # faint 50 km grid
            arc_band(ctx, cx, cy, 50 * k * px, 1, AMBER, 1.5, 0.12)
        line(ctx, [(60, cy), (W - 60, cy)], AMBER, 3, 0.5)
        circle(ctx, cx, cy, 16, TEAL)
        glow(ctx, cx, cy, 60, TEAL, 0.5)
        text(ctx, "KUSHA RADAR", cx, cy + 46, 26, TEAL, font=MONO, a=0.8)
        rows = (("m1", 150, 150, TEAL, "M1  ~150 KM"), ("m2", 250, 250, AMBER, "M2  ~250 KM"),
                ("m3", 350, 400, HI, "M3  350-400 KM"))
        for k, (key, lo, hi, c, lab) in enumerate(rows):
            u = t - b[key]
            if u <= 0:
                continue
            grow = ease_out_cubic(u / 0.7)
            if hi > lo:  # M3 is a band, not a line
                ctx.arc(cx, cy, hi * px, math.pi, math.pi + math.pi * grow)
                ctx.arc_negative(cx, cy, lo * px, math.pi + math.pi * grow, math.pi)
                ctx.close_path()
                rgba(ctx, c, 0.22)
                ctx.fill()
            arc_band(ctx, cx, cy, hi * px, grow, c, 8)
            if hi > lo:
                arc_band(ctx, cx, cy, lo * px, grow, c, 4, 0.8)
            # label rides the arc top
            ly = cy - hi * px - 30
            text(ctx, lab, cx, max(ly, 200), 40, c, font=MONO, a=clamp(u / 0.3), stroke=(0, 0, 0), stroke_w=6)
            sx = cx - (lo * px if k < 2 else hi * px)  # the interceptor flies out to the arc
            interceptor(ctx, lerp(cx, sx, grow), cy - 30 - 40 * k, 90, math.pi, t, a=1 - clamp((u - 0.7) / 0.3))
        u = t - b["s4"]
        if u > 0:
            arc_band(ctx, cx, cy, 400 * px, ease_out_cubic(u / 0.6), RED, 6, 0.95, dash=[24, 14])
            text(ctx, "S-400 • 400 KM", cx, cy - 400 * px + 38, 34, RED, font=MONO, a=clamp(u / 0.3),
                 stroke=(0, 0, 0), stroke_w=6)
            stamp(ctx, 540, 640, u - 0.4, -0.03, 660, 112, HI, [("S-400 JITNI PAHUNCH", 0, 70, HI)])


class Plan(Cued):
    """Test timeline, then two shields: S-400 'AAJ' and Kusha 'KAL' filling up."""

    def beats(self, d):
        c = self.cue
        return {"test": c("TEST", d * 0.05), "plan": c("PLAN", d * 0.5), "aaj": c("AAJ", d * 0.7),
                "kal": c("KAL", d * 0.88)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["test"], "tick"), (b["test"] + 0.5, "tock"), (b["test"] + 1.0, "tick"),
                (b["plan"], "beep"), (b["aaj"], "thud"), (b["kal"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx)
        # timeline: 2026 -> ~2029, M1 further along than M2/M3
        x0, x1, y = 140, 940, 300
        text(ctx, "2026", x0, y - 60, 36, INK, font=MONO)
        text(ctx, "~2029", x1, y - 60, 36, INK, font=MONO)
        for k, (lab, done, c) in enumerate((("M1", 0.55, TEAL), ("M2", 0.2, AMBER), ("M3", 0.12, HI))):
            yy = y + 70 * k
            rrect(ctx, x0, yy - 16, x1 - x0, 32, 16)
            rgba(ctx, c, 0.15)
            ctx.fill()
            grow = ease_out_cubic(clamp((t - b["test"] - 0.15 * k) / 0.8)) * done
            if grow > 0:
                rrect(ctx, x0, yy - 16, (x1 - x0) * grow, 32, 16)
                rgba(ctx, c, 0.9)
                ctx.fill()
            text(ctx, lab, x0 - 20, yy, 30, c, font=MONO, anchor="r")
        if t > b["test"] + 0.6:
            tag(ctx, "TESTING: 2-3 SAAL", 540, 560, AMBER, t - b["test"] - 0.6, size=44)
        # the two shields
        sy = 870
        u = t - b["aaj"]
        if u > 0:
            pop = ease_out_back(u / 0.35)
            ctx.save()
            ctx.translate(300, sy)
            ctx.scale(pop, pop)
            shield(ctx, 0, 0, 340, 400, AMBER)
            text(ctx, "S-400", 0, -40, 76, INK, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=8)
            text(ctx, "AAJ", 0, 60, 60, (0.05, 0.03, 0.01), font=CAPTION_FONT, bold=False)
            ctx.restore()
        u = t - b["kal"]
        if u > 0:
            pop = ease_out_back(u / 0.35)
            fill = 0.25 + 0.45 * ease_in_out(clamp((u - 0.3) / 1.2))
            ctx.save()
            ctx.translate(780, sy)
            ctx.scale(pop, pop)
            shield(ctx, 0, 0, 340, 400, SAFFRON, fill=fill)
            text(ctx, "KUSHA", 0, -40, 76, INK, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=8)
            text(ctx, "KAL", 0, 60, 60, INK, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=6)
            ctx.restore()
            if u > 0.4:
                text(ctx, "+", 540, sy - 20, 110, HI, font=CAPTION_FONT, bold=False, a=clamp((u - 0.4) / 0.3))


class Ask(Cued):
    """Dim range arcs behind the poll card (Lego ending 'poll')."""

    def beats(self, d):
        c = self.cue
        return {"q": c("BATAO", 0.05), "cmt": c("COMMENT", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["q"] + 0.05, "pop"), (b["cmt"], "dingdong")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx)
        range_arcs(ctx, t, a=0.4, cy=1150)
        lego.ending(STORY, ctx, t, t - b["q"], t - b["cmt"], question=("5 AUR S-400 LEIN?", "YA KUSHA KA WAIT?"),
                    options=("S-400 LO", "KUSHA KA WAIT"), y=600)


SCENE_CLASSES = {"rumor": Rumor, "deal": Deal, "offer": Offer, "kusha": Kusha, "range": Range, "plan": Plan,
                 "ask": Ask}
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
        "Kya India Ne S-400 Cancel Kiya? Project Kusha Ka Sach",
        "S-400 vs Project Kusha: India Ka Asli Plan",
        "Desi S-400 Aa Gaya? Project Kusha Ka Pehla Test",
        "S-400 Cancel Ki Khabar Galat: 4 Squadron Aa Chuke",
        "Project Kusha: 400 KM Tak Bharat Ki Apni Dhaal",
        "Russia Ne 5 Aur S-400 Offer Kiye: India Kya Karega?",
        "Project Kusha Test Safal: Ab S-400 Ka Kya Hoga?",
        "S-400 Ya Project Kusha: Bharat Kiske Bharose?",
        "Project Kusha M1 M2 M3: Range Kitni Hai?",
        "Aaj Russia Ki Dhaal, Kal Apni: Project Kusha",
    ],
    "title": "Kya India Ne S-400 Cancel Kiya? Project Kusha Ka Sach",   # creator's pick, still scored
    "thumb_text": "DAAVA GALAT",
    "queries": ["s-400 cancel", "project kusha", "s-400 vs project kusha"],
    "description": """
S-400 cancel ki khabar galat hai: S-400 vs Project Kusha ka asli plan ye hai ki dono saath chalenge.
2018 ki deal ke 5 me se 4 S-400 squadron India pahunch chuke hain, aur Russia ne 5 aur offer kiye hain.

Is Short me:
• 2018 deal: 5 squadron, $5 billion+; 4 delivered, 5th raste me (Nov 2026 tak)
• Operation Sindoor ke baad Russia ka offer: 5 aur squadron, ~₹50,000 crore; deal abhi sign nahi hui
• Project Kusha: DRDO ka long-range air defence, pehla flight test 23 July 2026, Odisha tat
• Range: M1 ~150 KM, M2 ~250 KM, M3 ~350-400 KM
• M2 aur M3 ke test 2-3 saal aur chalenge, isliye abhi S-400 + Kusha saath

Aap kya chunoge: 5 aur S-400, ya Kusha ka intezaar? Comment me likho.
Aisi aur defence fact-checks ke liye Reality Shift ko subscribe karo.

Note: animation schematic hai, scale pe nahi. Facts public reports (MoD, Nov 2026 tak) par based hain.
""",
    "tags": ["s-400", "s-400 cancel", "project kusha", "s-400 vs project kusha", "kusha missile", "drdo",
             "indian air defence", "s400 india", "russia india defence", "operation sindoor", "desi s-400",
             "indian defence shorts", "defence hindi", "fact check", "reality shift"],
    "hashtags": ["#Shorts", "#ProjectKusha", "#S400"],
}


def thumbnail(ctx):
    """1080x1920 cover: DAAVA / GALAT over an S-400 launcher with a Kusha interceptor rising."""
    bg(ctx, (0.07, 0.03, 0.02), (0.01, 0.01, 0.01))
    range_arcs(ctx, 0, a=0.6, cy=1500)
    launcher(ctx, 540, 1480, 1.6, STEEL, elev=0.7)
    interceptor(ctx, 780, 980, 420, -1.0, 0.3)
    g = cairo.LinearGradient(0, 0, 0, 860)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.95)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 860)
    ctx.set_source(g)
    ctx.fill()
    vignette(ctx)
    glow(ctx, 540, 420, 560, RED, 0.25)
    text(ctx, "DAAVA", 540, 300, 250, INK, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "GALAT", 540, 560, 260, RED, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=24)
    tag(ctx, "S-400  vs  KUSHA", 540, 760, HI, 1.0, size=56)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, INK, a=0.7)


def main() -> None:
    import upload_kit
    story = importlib.import_module("generate_s400_kusha_short")
    engine.make_frame = lego.frame_maker(story)
    final = engine.render(story, "edge")
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
