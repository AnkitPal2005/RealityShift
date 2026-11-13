"""Reality Shift Short - "Su-30MKI: 'I' matlab INDIA" (~40s, single voice, recorded in KikiVoice, L007).

Usage:
  python make.py su30 --kiki-export     # narrator text for KikiVoice
  python make.py su30 --kiki-split --check-voice
  python make.py su30                   # renders from the KikiVoice clips (--engine edge = preview)

Air Force week, 13 Nov 2026. Seven scenes on a drawn sky: hook (a Flanker flies RUSSIA -> BHARAT, then a grey
one flies back for Russia itself) -> name card SU-30 MKI where the last letter lights up as INDIA -> top view
with chips for the four countries' equipment -> Nashik hangar, jets pop in, counter to 200+ -> close-up of the
two nozzles swivelling, then a pitch-up manoeuvre -> side view with BrahMos under the belly, 2,500 KG counter,
IKLAUTA FIGHTER stamp -> IAF jet chips behind a SUKHOI vs RAFALE poll. All aircraft are generic drawings.
"""

import importlib
import json
import math
import sys

import cairo

from core import engine
from core import delivery
from core import lego
from core.engine import *  # noqa: F401,F403
from shorts.brahmos_lego import tag
from shorts.chabahar import Cued
from shorts.reality_shift import stamp

TOPIC = "SU-30MKI IAF"
OUTPUTS = {"edge": "su30_short.mp4"}
LEGO = {"header": "radar", "caption": "typewriter", "transition": "shutter", "palette": "intel", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.6              # keep the voice's own comma / '...' pauses, only clip dead air
TAIL_PAD = 0.25
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 118
MUSIC_STYLE = "pulse"      # jets, steady drive (Nyoma was tension @ 100, Siachen ambient @ 80)
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 300        # KikiVoice pause tag between scenes (800 felt too long, user 13 Nov)
# no "?" right before more words: Kiki dropped the word after "मतलब?" - use "..." for the held beat

PAL = lego.PALETTES["intel"]
UI = PAL["ui"]
HI = PAL["hi"]
RED = PAL["alert"]
INK = PAL["ink"]
SAFFRON = hexc("#FF9933")
GREEN = hexc("#3DDC84")
SKY = hexc("#6FB7FF")
STEEL = hexc("#AEB8C2")
CAMO = hexc("#8FA3B3")      # IAF Flanker light grey-blue
RUS = hexc("#C9D2DA")

SOURCES = [
    "Su-30MKI = 'Modernizirovanny Kommercheskiy Indiyskiy' (modernised commercial, Indian); a Su-30 variant "
    "developed by Sukhoi/Irkut for the IAF (Wikipedia 'Sukhoi Su-30MKI'; HAL product page)",
    "Russia's own Su-30SM (ordered 2012 for the Russian Air Force / Navy) is derived from the export Su-30MKI/MKM "
    "design (Irkut / UAC; Wikipedia 'Sukhoi Su-30SM'; The Diplomat 2012). Script says 'वैसा ही जेट' (same type)",
    "Avionics from Russia, India, France and Israel: e.g. Indian mission computer/RWR, French (Thales/Sagem) "
    "navigation and displays, Israeli (Elbit/Rafael) systems and pods (Wikipedia; Bharat Rakshak; HAL)",
    "Licence-built by HAL at Nashik (Ozar); over 200 delivered out of 272 ordered - HAL said 222 by 2020 "
    "(PIB; HAL annual reports; ThePrint). Script: 'दो सौ से ज़्यादा'",
    "Twin AL-31FP engines with thrust-vectoring nozzles (±15° in pitch), supermanoeuvrable (UEC Saturn; Wikipedia)",
    "BrahMos-A air-launched variant ~2.5 t; first air launch from a Su-30MKI 22 Nov 2017; the Su-30MKI is the only "
    "fighter integrated with it (PIB 22 Nov 2017; BrahMos Aerospace)",
]

# Written for KikiVoice: one flowing paragraph per scene; punctuation sets the pace. Captions follow the spoken
# words (Hinglish), split on the same commas the voice breathes at.
SPEC = [
    {"key": "hook", "accent": RED, "text": "RUSSIA -> BHARAT",
     "visual": "Sky; RUSSIA tag left, BHARAT tag right; an IAF Flanker flies across to BHARAT, then a grey one "
               "flies back to RUSSIA",
     "vo": [("hook", [("रूस ने,", "RUSS NE,"), ("भारत के लिए", "BHARAT KE LIYE"),
                      ("एक लड़ाकू जेट बनाया।", "EK LADAAKU JET BANAYA."), ("फिर, वैसा ही जेट,", "PHIR, WAISA HI JET,"),
                      ("खुद के लिए भी ले लिया।", "KHUD KE LIYE BHI LE LIYA.")])]},
    {"key": "name", "accent": HI, "text": "MKI = INDIA",
     "visual": "Name card SU-30 / M K I; the I glows and drops a tricolour line to 'INDIA'",
     "vo": [("tell", [("नाम है,", "NAAM HAI,"), ("सुखोई तीस, एम के आई।", "SUKHOI 30 MKI."),
                      ("और आखिरी 'आई' का मतलब है...", "AUR AAKHRI 'I' KA MATLAB HAI..."), ("इंडिया।", "INDIA.")])]},
    {"key": "inside", "accent": UI, "text": "4 DESH KE UPKARAN",
     "visual": "Top view of the jet; chips RUSSIA (airframe/engines), FRANCE, ISRAEL, BHARAT point at it",
     "vo": [("tell", [("ये जेट,", "YE JET,"), ("म्हारी वायुसेना की ज़रूरत", "MHAARI VAYUSENA KI ZAROORAT"),
                      ("के हिसाब से बदला गया।", "KE HISAAB SE BADLA GAYA."),
                      ("इसमें फ्रांस, इज़राइल", "ISME FRANCE, ISRAEL"),
                      ("और भारत के उपकरण भी लगे हैं।", "AUR BHARAT KE UPKARAN BHI LAGE HAIN.")])]},
    {"key": "nashik", "accent": SAFFRON, "text": "NASHIK: 200+",
     "visual": "Hangar interior; small jets pop into rows; counter to 200+; 'NASHIK • HAL' tag",
     "vo": [("tell", [("और ये नासिक में बनता है।", "AUR YE NASHIK MEIN BANTA HAI."),
                      ("और दो सौ से ज़्यादा सुखोई,", "AUR 200 SE ZYADA SUKHOI,"), ("यहीं जोड़े गए।", "YAHIN JODE GAYE.")])]},
    {"key": "tvc", "accent": GREEN, "text": "MUDNE WALI DHAAR",
     "visual": "Close-up of two nozzles swivelling up/down with flame (±15°), then the jet pitches up past "
               "vertical and recovers; 'KAM HI JET' stamp",
     "vo": [("tell", [("इसके दो इंजन,", "ISKE 2 ENGINE,"), ("अपनी धार को मोड़ सकते हैं।", "APNI DHAAR KO MOD SAKTE HAIN."),
                      ("इसलिए हवा में ये,", "ISLIYE HAWA MEIN YE,"), ("ऐसे करतब करता है,", "AISE KARTAB KARTA HAI,"),
                      ("जो कम ही जेट कर पाते हैं।", "JO KAM HI JET KAR PAATE HAIN.")])]},
    {"key": "brahmos", "accent": RED, "text": "2.5 TON BRAHMOS",
     "visual": "Side view with a BrahMos under the belly; weight counter to 2,500 KG; 'IKLAUTA FIGHTER' stamp",
     "vo": [("tell", [("और सबसे बड़ी बात...", "AUR SABSE BADI BAAT..."), ("ब्रह्मोस जैसी", "BRAHMOS JAISI"),
                      ("ढाई टन की मिसाइल,", "2.5 TON KI MISSILE,"), ("उठाकर उड़ने वाला,", "UTHAAKAR UDNE WALA,"),
                      ("ये इकलौता लड़ाकू जेट है।", "YE IKLAUTA LADAAKU JET HAI.")])]},
    {"key": "ask", "accent": HI, "text": "SABSE DAMDAAR?",
     "visual": "IAF jet chips (SU-30MKI glowing, RAFALE, TEJAS, MIRAGE 2000) behind a poll: SUKHOI vs RAFALE",
     "vo": [("ask", [("भाई, आपकी नज़र में,", "BHAI, AAPKI NAZAR MEIN,"), ("म्हारी वायुसेना का", "MHAARI VAYUSENA KA"),
                     ("सबसे दमदार जेट कौन सा है,", "SABSE DAMDAAR JET KAUN SA HAI,"),
                     ("कमेंट में बताइए।", "COMMENT MEIN BATAIYE."), ("जय हिंद!", "JAI HIND!")])]},
]

DELIVERY = delivery.build(SPEC)   # gaps between lines; KikiVoice supplies the performance itself
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {"RUSS": RED, "BHARAT": SAFFRON, "KHUD": RED, "SUKHOI": HI, "30": HI, "MKI.": HI, "'I'": HI, "MATLAB": HI,
       "INDIA.": SAFFRON, "MHAARI": SAFFRON, "ZAROORAT": UI, "BADLA": UI, "FRANCE,": UI, "ISRAEL": UI,
       "UPKARAN": UI, "NASHIK": SAFFRON, "200": SAFFRON, "ZYADA": SAFFRON, "JODE": SAFFRON, "2": GREEN,
       "ENGINE,": GREEN, "DHAAR": GREEN, "MOD": GREEN, "KARTAB": GREEN, "KAM": GREEN, "BADI": RED, "BAAT...": RED,
       "BRAHMOS": RED, "2.5": RED, "TON": RED, "IKLAUTA": RED, "BHAI,": SAFFRON, "DAMDAAR": HI, "COMMENT": HI,
       "JAI": SAFFRON, "HIND!": SAFFRON, "LADAAKU": UI}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".—")] = HOT[_k]


# ============================================================ world

def mix(a, b, u):
    return tuple(lerp(x, y, clamp(u)) for x, y in zip(a, b))


def sky(ctx, t, dusk=0.0, haze=True):
    """High blue sky with drifting cloud banks and a hazy horizon low in the frame."""
    g = cairo.LinearGradient(0, 0, 0, 1300)
    g.add_color_stop_rgb(0, *mix(hexc("#0B2A5C"), hexc("#070F22"), dusk))
    g.add_color_stop_rgb(0.7, *mix(hexc("#3E86D6"), hexc("#20375E"), dusk))
    g.add_color_stop_rgb(1, *mix(hexc("#BFE0FF"), hexc("#4A5B7A"), dusk))
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()
    glow(ctx, 860, 200, 260, (1, 0.96, 0.85), 0.3 * (1 - dusk))
    for k in range(7):                                   # cloud banks scroll left, parallax by row
        sp = 40 + 30 * (k % 3)
        x = (rnd(k, 2) * 1500 - t * sp) % 1500 - 200
        y = 300 + 130 * k + 30 * rnd(k, 5)
        for j in range(4):
            ctx.save()
            ctx.translate(x + j * 60, y + 10 * math.sin(j))
            ctx.scale(1, 0.35)
            circle(ctx, 0, 0, 70 + 30 * rnd(k, j), (1, 1, 1), 0.10 + 0.05 * (k % 2))
            ctx.restore()
    if haze:
        g = cairo.LinearGradient(0, 1050, 0, 1300)
        g.add_color_stop_rgba(0, 1, 1, 1, 0)
        g.add_color_stop_rgba(1, 0.85, 0.9, 1, 0.35 * (1 - dusk))
        ctx.rectangle(0, 1050, W, 250)
        ctx.set_source(g)
        ctx.fill()


TOP = [(0, -0.50), (0.025, -0.42), (0.045, -0.30), (0.055, -0.27), (0.15, -0.21), (0.15, -0.185), (0.065, -0.195),
       (0.085, -0.10), (0.37, 0.10), (0.375, 0.16), (0.13, 0.18), (0.11, 0.25), (0.25, 0.36), (0.25, 0.42),
       (0.09, 0.40), (0.075, 0.50), (0.025, 0.50), (0.02, 0.43), (0, 0.43)]


def flanker_top(ctx, x, y, s, c=CAMO, a=1.0, rot=0.0):
    """Twin-engine canard fighter seen from above, nose up; s = length in px."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    pts = TOP + [(-px, py) for px, py in reversed(TOP)]
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    rgba(ctx, c, a)
    ctx.fill_preserve()
    rgba(ctx, shade(c, 0.6), a)
    ctx.set_line_width(0.004)
    ctx.stroke()
    for sx in (-1, 1):                                   # engine nacelles + twin fins
        ctx.rectangle(sx * 0.07 - 0.025, 0.0, 0.05, 0.47)
        rgba(ctx, shade(c, 0.85), a)
        ctx.fill()
        line(ctx, [(sx * 0.10, 0.18), (sx * 0.11, 0.40)], shade(c, 0.5), 0.018, a)
    ctx.save()                                           # canopy
    ctx.translate(0, -0.33)
    ctx.scale(0.4, 1)
    circle(ctx, 0, 0, 0.06, hexc("#2C6DB5"), a)
    ctx.restore()
    for sx in (-1, 1):                                   # roundels on the wings
        for k, cc in enumerate((SAFFRON, (1, 1, 1), hexc("#138808"))):
            circle(ctx, sx * 0.25, 0.12, 0.03 - k * 0.009, cc, a)
    ctx.restore()


def flanker_side(ctx, x, y, L, ang, t, burner=0.0, a=1.0, c=CAMO, nozzle=0.0, missile=False, roundel=True):
    """Side view, nose along ang; nozzle = tilt of the exhaust (rad), missile = BrahMos under the belly."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(L, L)
    ctx.save()                                           # nozzle + flame swivel about the tail
    ctx.translate(-0.47, 0.035)
    ctx.rotate(nozzle)
    if burner > 0:
        for k, (fc, fa) in enumerate(((hexc("#FF6A2B"), 0.6), ((1, 0.85, 0.4), 0.8), ((1, 1, 0.9), 0.9))):
            f = burner * (1 + 0.2 * math.sin(t * 50 + k)) * (1 - 0.3 * k)
            ctx.move_to(-0.04, -0.025)
            ctx.line_to(-0.04 - 0.3 * f, 0)
            ctx.line_to(-0.04, 0.025)
            ctx.close_path()
            rgba(ctx, fc, fa * a)
            ctx.fill()
    rrect(ctx, -0.05, -0.028, 0.06, 0.056, 0.01)
    rgba(ctx, hexc("#4A4F57"), a)
    ctx.fill()
    ctx.restore()
    for k, cc in enumerate((shade(c, 0.75), c)):         # twin fins, far one darker
        dx = 0.03 * (1 - k)
        ctx.move_to(-0.24 + dx, -0.05)
        ctx.line_to(-0.38 + dx, -0.25)
        ctx.line_to(-0.45 + dx, -0.25)
        ctx.line_to(-0.43 + dx, -0.05)
        ctx.close_path()
        rgba(ctx, cc, a)
        ctx.fill()
    ctx.move_to(0.5, 0)                                  # fuselage with the raised cockpit hump
    ctx.curve_to(0.44, -0.03, 0.36, -0.045, 0.30, -0.05)
    ctx.curve_to(0.26, -0.095, 0.16, -0.095, 0.10, -0.06)
    ctx.line_to(-0.45, -0.05)
    ctx.line_to(-0.47, 0.06)
    ctx.line_to(0.05, 0.075)
    ctx.curve_to(0.3, 0.06, 0.45, 0.03, 0.5, 0)
    rgba(ctx, c, a)
    ctx.fill()
    ctx.move_to(0.05, 0.03)                              # wing
    ctx.line_to(-0.30, 0.04)
    ctx.line_to(-0.33, 0.10)
    ctx.close_path()
    rgba(ctx, shade(c, 0.7), a)
    ctx.fill()
    ctx.move_to(0.26, -0.01)                             # canard
    ctx.line_to(0.18, -0.005)
    ctx.line_to(0.17, 0.03)
    ctx.close_path()
    rgba(ctx, shade(c, 0.65), a)
    ctx.fill()
    ctx.move_to(0.29, -0.05)                             # canopy glass
    ctx.curve_to(0.25, -0.09, 0.17, -0.09, 0.13, -0.06)
    ctx.close_path()
    rgba(ctx, hexc("#2C6DB5"), a)
    ctx.fill()
    if roundel:
        for k, cc in enumerate((SAFFRON, (1, 1, 1), hexc("#138808"))):
            circle(ctx, -0.38, -0.15, 0.035 - k * 0.011, cc, a)
    if missile:
        rrect(ctx, -0.24, 0.085, 0.46, 0.05, 0.02)
        rgba(ctx, (0.93, 0.93, 0.95), a)
        ctx.fill()
        ctx.move_to(0.22, 0.085)
        ctx.line_to(0.29, 0.11)
        ctx.line_to(0.22, 0.135)
        ctx.close_path()
        rgba(ctx, (0.93, 0.93, 0.95), a)
        ctx.fill()
        ctx.rectangle(0.05, 0.085, 0.03, 0.05)
        rgba(ctx, RED, a)
        ctx.fill()
        for fx in (-0.24, 0.12):
            ctx.move_to(fx, 0.135)
            ctx.line_to(fx - 0.04, 0.17)
            ctx.line_to(fx + 0.02, 0.135)
            ctx.close_path()
            rgba(ctx, (0.75, 0.75, 0.8), a)
            ctx.fill()
    ctx.restore()


def counter(ctx, value, unit, c, u, y=330, title="", plus=False):
    if u <= 0:
        return
    k = max(0.01, ease_out_back(clamp(u / 0.3)))
    ctx.save()
    ctx.translate(540, y)
    ctx.scale(k, k)
    rrect(ctx, -330, -80, 660, 160, 22)
    rgba(ctx, PAL["panel"], 0.9)
    ctx.fill_preserve()
    rgba(ctx, c)
    ctx.set_line_width(5)
    ctx.stroke()
    if title:
        text(ctx, title, -300, -52, 26, c, font=lego.MONO, anchor="l")
    text(ctx, f"{int(round(value)):,}{'+' if plus else ''} {unit}".strip(), 0, 14, 104, c, font=CAPTION_FONT,
         bold=False, stroke=(0, 0, 0), stroke_w=8)
    ctx.restore()


def chip(ctx, s, x, y, c, u, size=38, fill=None):
    if u <= 0:
        return
    p = max(0.01, ease_out_back(clamp(u / 0.3)))
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(p, p)
    w = text_width(ctx, s, size, font=lego.MONO) + 44
    rrect(ctx, -w / 2, -size * 0.95, w, size * 1.9, size * 0.95)
    rgba(ctx, fill or PAL["panel"], 0.95)
    ctx.fill_preserve()
    rgba(ctx, c)
    ctx.set_line_width(4)
    ctx.stroke()
    text(ctx, s, 0, 2, size, (0.05, 0.05, 0.08) if fill else INK, font=lego.MONO)
    ctx.restore()


# ============================================================ scenes

class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"in": c("BHARAT", 0.4), "back": c("KHUD", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["in"] - 0.2, "whoosh"), (b["in"], "engine", 1.6), (b["in"] + 1.4, "thud"),
                (b["back"] - 0.2, "whoosh"), (b["back"] + 0.9, "zap")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        sky(ctx, t)
        tag(ctx, "RUSSIA", 230, 330, RUS, t / 0.6, size=46)
        tag(ctx, "BHARAT", 850, 330, SAFFRON, t / 0.6 - 0.3, size=46)
        for k in range(14):                                  # dotted route between the two
            x = lerp(300, 780, k / 13)
            circle(ctx, x, 430 - 80 * math.sin(math.pi * k / 13), 5, INK, 0.5 * clamp(t / 0.5))
        u = t - b["in"] + 0.3
        if u > 0:                                            # IAF Flanker crosses to BHARAT
            k = ease_in_out(clamp(u / 1.5))
            flanker_side(ctx, lerp(-260, 700, k), 640, 520, -0.04, t, burner=1.0)
            if k >= 1 and t < b["back"]:
                tag(ctx, "SU-30 MKI", 700, 820, SAFFRON, u - 1.5, size=40, sub="BHARAT KE LIYE")
        v = t - b["back"] + 0.2
        if v > 0:                                            # a grey one heads back to RUSSIA
            k = ease_in_out(clamp(v / 1.4))
            ctx.save()
            ctx.translate(lerp(1340, 380, k), 870)
            ctx.scale(-1, 1)
            flanker_side(ctx, 0, 0, 440, -0.03, t, burner=0.8, c=RUS, roundel=False)
            ctx.restore()
            if k >= 1:
                stamp(ctx, 400, 1030, v - 1.4, -0.03, 560, 110, RED, [("RUSSIA NE BHI LIYA", 0, 52, RED)])


class Name(Cued):
    def beats(self, d):
        c = self.cue
        return {"su": c("SUKHOI", 0.4), "q": c("MATLAB", d * 0.55), "in": c("INDIA", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(b["su"], "thud"), (b["su"] + 0.4, "pop"), (b["su"] + 0.55, "pop"), (b["su"] + 0.7, "pop"),
                (b["q"], "beep"), (b["in"], "dingdong")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        sky(ctx, t, dusk=0.55)
        flanker_top(ctx, 540, 700, 1000, a=0.18)
        u = t - b["su"]
        if u > 0:
            stamp(ctx, 540, 330, u, -0.02, 640, 170, HI, [("SUKHOI-30", 0, 110, INK)])
            for k, ch in enumerate("MKI"):                   # the three letters drop in one by one
                p = clamp((u - 0.4 - 0.15 * k) / 0.3)
                if p <= 0:
                    continue
                x = 330 + 210 * k
                isI = ch == "I"
                q = t - b["q"]
                lit = isI and q > 0
                if lit:
                    glow(ctx, x, 600, 160, SAFFRON, 0.35 + 0.2 * math.sin(t * 8))
                text(ctx, ch, x, lerp(480, 600, ease_out_cubic(p)), 230, SAFFRON if lit else INK,
                     font=CAPTION_FONT, bold=False, a=p, stroke=(0, 0, 0), stroke_w=14)
        w = t - b["in"]
        if w > 0:                                            # the I drops a tricolour line to INDIA
            k = ease_out_cubic(clamp(w / 0.4))
            for j, cc in enumerate((SAFFRON, (1, 1, 1), hexc("#138808"))):
                line(ctx, [(750 + (j - 1) * 14, 720), (750 + (j - 1) * 14, lerp(720, 860, k))], cc, 10)
            stamp(ctx, 540, 960, w - 0.3, 0.03, 620, 170, SAFFRON, [("= INDIA", 0, 120, SAFFRON)])


CHIPS = [("RUSSIA", "BADLA", (880, 1010), (575, 1060), RUS),
         ("FRANCE", "FRANCE", (190, 330), (540, 380), hexc("#5B8CFF")),
         ("ISRAEL", "ISRAEL", (900, 520), (730, 660), hexc("#7FD6FF")),
         ("BHARAT", "UPKARAN", (180, 760), (540, 640), SAFFRON)]


class Inside(Cued):
    def beats(self, d):
        c = self.cue
        return {"iaf": c("ZAROORAT", 0.3), **{name: c(key, d * (0.4 + 0.15 * k))
                                             for k, (name, key, *_) in enumerate(CHIPS)}}

    def events(self, d):
        b = self.beats(d)
        return [(b["iaf"], "beep")] + [(b[n], "pick") for n, *_ in CHIPS]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        sky(ctx, t, dusk=0.3, haze=False)
        grid = clamp(t / 0.5)                                # blueprint grid behind the jet
        for gx in range(0, W, 90):
            line(ctx, [(gx, 150), (gx, 1250)], UI, 1, 0.12 * grid)
        for gy in range(150, 1260, 90):
            line(ctx, [(0, gy), (W, gy)], UI, 1, 0.12 * grid)
        flanker_top(ctx, 540, 660, 900)
        if t < b["FRANCE"]:
            tag(ctx, "IAF KE HISAAB SE", 540, 240, UI, t - b["iaf"], size=44)
        for name, _, (cx, cy), (px, py), c in CHIPS:
            u = t - b[name]
            if u <= 0:
                continue
            k = ease_out_cubic(clamp(u / 0.35))
            line(ctx, [(cx, cy), (lerp(cx, px, k), lerp(cy, py, k))], c, 4)
            circle(ctx, px, py, 12 * k, c)
            chip(ctx, name, cx, cy, c, u, size=40)


class Nashik(Cued):
    def beats(self, d):
        c = self.cue
        return {"q": c("NASHIK", 0.2), "place": c("NASHIK", 0.3), "n": c("200", d * 0.5)}

    def events(self, d):
        b = self.beats(d)
        return [(b["q"], "pop"), (b["place"], "thud")] + [(b["n"] + 0.1 * k, "tick") for k in range(10)] + \
               [(b["n"] + 1.1, "kaching")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        g = cairo.LinearGradient(0, 0, 0, 1300)               # hangar interior
        g.add_color_stop_rgb(0, *hexc("#1B232C"))
        g.add_color_stop_rgb(1, *hexc("#3A434D"))
        ctx.rectangle(0, 0, W, H)
        ctx.set_source(g)
        ctx.fill()
        for k in range(7):                                   # roof trusses + lamps
            x = 80 + 155 * k
            line(ctx, [(x, 120), (540, 40)], (0.5, 0.55, 0.6), 4, 0.5)
            glow(ctx, x, 170, 90, (1, 0.9, 0.7), 0.25)
            circle(ctx, x, 170, 10, (1, 0.95, 0.8))
        ctx.rectangle(0, 1120, W, 180)
        rgba(ctx, hexc("#2A3038"))
        ctx.fill()
        line(ctx, [(0, 1120), (W, 1120)], HI, 4, 0.5)
        u = t - b["n"]
        n_on = int(clamp(u / 1.0) * 12) if u > 0 else 0
        for i in range(12):                                  # rows of jets fill the hangar
            col, row = i % 4, i // 4
            x, y = 180 + 240 * col, 500 + 200 * row
            if i < n_on or (u <= 0 and i < 2):
                flanker_top(ctx, x, y, 180, a=0.95)
        if t > b["q"] and t < b["place"]:
            tag(ctx, "KAHAN BANTA HAI?", 540, 330, SAFFRON, t - b["q"], size=50)
        if t > b["place"]:
            tag(ctx, "NASHIK • MAHARASHTRA", 540, 330 if u <= 0 else 1060, SAFFRON, t - b["place"], size=40,
                sub="HAL KA KARKHANA")
        if u > 0:
            counter(ctx, 200 * ease_in_out(clamp(u / 1.0)), "SUKHOI", SAFFRON, u + 0.3, y=330,
                    title="YAHIN JODE GAYE", plus=u > 1.0)


class Tvc(Cued):
    def beats(self, d):
        c = self.cue
        return {"mod": c("MOD", d * 0.2), "move": c("KARTAB", d * 0.55), "few": c("KAM", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "engine", 1.5), (b["mod"], "zap"), (b["move"] - 0.2, "whoosh"), (b["move"], "engine", 1.8),
                (b["few"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        sky(ctx, t, dusk=0.2)
        if t < b["move"]:                                    # close-up on the tail: two nozzles swivel ±15°
            ang = math.radians(15) * math.sin(max(0.0, t - b["mod"]) * 3.0) if t > b["mod"] else 0.0
            ctx.save()
            ctx.translate(1400, 640)
            flanker_side(ctx, 0, 0, 2200, 0.0, t, burner=1.0, nozzle=ang)
            ctx.restore()
            ctx.save()
            ctx.translate(1400, 760)
            flanker_side(ctx, 0, 0, 2200, 0.0, t, burner=1.0, nozzle=ang, a=0.55)
            ctx.restore()
            tag(ctx, "2 ENGINE", 760, 330, GREEN, t / 0.4, size=46)
            if t > b["mod"]:
                tag(ctx, "DHAAR MUDTI HAI: ±15°", 540, 1050, GREEN, t - b["mod"], size=42)
        else:                                                # pitch up past vertical and recover
            u = t - b["move"]
            p = clamp(u / 2.2)
            pitch = -math.radians(110) * math.sin(math.pi * p)
            x = lerp(260, 760, p)
            for k in range(18):                              # vapour trail
                q = clamp(p - k * 0.02)
                if q <= 0:
                    break
                tp = -math.radians(110) * math.sin(math.pi * q)
                tx = lerp(260, 760, q) - 260 * math.cos(tp) * 0.9
                ty = 620 - 260 * math.sin(tp) * 0.9
                circle(ctx, tx, ty, 14 + k, (1, 1, 1), 0.25 * (1 - k / 18))
            flanker_side(ctx, x, 620, 520, pitch, t, burner=1.0)
            if t > b["few"]:
                stamp(ctx, 540, 1050, t - b["few"], -0.03, 560, 130, GREEN, [("KAM HI JET", 0, 84, GREEN)])


class Brahmos(Cued):
    def beats(self, d):
        c = self.cue
        return {"big": c("BADI", 0.2), "bm": c("BRAHMOS", d * 0.3), "w": c("2.5", d * 0.45),
                "one": c("IKLAUTA", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(b["big"], "thud"), (b["bm"], "zap"), (b["w"], "beep"), (b["w"] + 1.0, "thud"), (b["one"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        sky(ctx, t, dusk=0.4)
        bob = 10 * math.sin(t * 1.6)
        flanker_side(ctx, 540, 640 + bob, 900, -0.02, t, burner=0.7, missile=True)
        if t < b["bm"]:
            tag(ctx, "SABSE BADI BAAT", 540, 300, RED, t - b["big"], size=50)
        u = t - b["bm"]
        if u > 0:
            glow(ctx, 520, 720 + bob, 260, RED, 0.25 + 0.1 * math.sin(t * 8))
            tag(ctx, "BRAHMOS-A", 540, 860 + bob, RED, u, size=42)
        w = t - b["w"]
        if w > 0 and t < b["one"]:
            counter(ctx, 2500 * ease_in_out(clamp(w / 1.0)), "KG", RED, w + 0.3, y=330, title="MISSILE KA WAZAN")
        if t > b["one"]:
            stamp(ctx, 540, 330, t - b["one"], -0.03, 700, 170, RED,
                  [("IKLAUTA FIGHTER", -24, 80, RED), ("JO BRAHMOS UTHATA HAI", 46, 38, INK)])


JETS = [("SU-30 MKI", True), ("RAFALE", False), ("TEJAS", False), ("MIRAGE 2000", False)]


class Ask(Cued):
    def beats(self, d):
        c = self.cue
        return {"j": c("NAZAR", 0.3), "q": c("DAMDAAR", d * 0.4), "cmt": c("COMMENT", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(b["j"] + 0.2 * k, "pick") for k in range(4)] + [(b["q"] + 0.05, "pop"), (b["cmt"], "dingdong"),
                                                                 (b["cmt"] + 1.1, "pick")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        sky(ctx, t, dusk=0.3 + 0.4 * clamp((t - b["q"]) / 0.4))
        flanker_side(ctx, (t * 220) % 1700 - 300, 990, 300, -0.03, t, burner=0.8, a=0.7)
        dim = 1 - 0.6 * clamp((t - b["q"]) / 0.4)
        late = t >= b["q"]                                   # 2x2 grid up top, then a row under the poll
        for k, (name, star) in enumerate(JETS):
            x, y = (160 + k * 253, 1040) if late else ((290, 790)[k % 2], 300 + 140 * (k // 2))
            chip(ctx, name, x, y, HI if star else UI, (t - b["j"] - 0.2 * k) * dim, size=28 if late else 44,
                 fill=HI if star else None)
        lego.ending(STORY, ctx, t, t - b["q"], t - b["cmt"], question=("SABSE DAMDAAR", "JET KAUN SA?"),
                    options=("SUKHOI-30 MKI", "RAFALE"), y=620)


SCENE_CLASSES = {"hook": Hook, "name": Name, "inside": Inside, "nashik": Nashik, "tvc": Tvc, "brahmos": Brahmos,
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
        "Su-30MKI Me 'I' Ka Matlab INDIA: Russia Ne Bhi Liya",
        "Russia Ne Bharat Ke Liye Banaya, Phir Khud Liya: Su-30MKI",
        "Su-30MKI: Akela Fighter Jo 2.5 Ton BrahMos Uthata Hai",
        "Su-30MKI Ka Sach: 4 Desh, 1 Jet, Nashik Me Bana",
        "Su-30MKI Kyun Khaas Hai? IAF Ki Reedh Ki Haddi",
        "Nashik Me Bane 200+ Sukhoi: Su-30MKI Ki Kahani",
        "Su-30MKI vs Baaki Jets: Ye Kartab Kam Hi Kar Paate",
        "MKI Ka Matlab Kya Hai? Su-30MKI Explained Hindi",
        "Su-30MKI: Russia Ka Jet, Bharat Ka Dimaag",
        "IAF Ka Su-30MKI: 2 Engine, Mudne Wali Dhaar, BrahMos",
    ],
    "title": "Su-30MKI Me 'I' Ka Matlab INDIA: Russia Ne Bhi Liya",
    "thumb_text": "I = INDIA",
    "queries": ["su 30 mki", "su 30 mki full form", "su 30 mki brahmos"],
    "description": """
Su 30 MKI (सुखोई 30 एमकेआई): Russia ne Bharat ki Air Force ke liye banaya, aur baad me apni Air Force ke liye Su-30SM isi design se liya.
Su 30 MKI full form: Modernizirovanny Kommercheskiy Indiyskiy - aakhri "I" matlab INDIA. Su 30 MKI BrahMos uthane wala iklauta fighter.

Is Short me:
• MKI = Modernizirovanny Kommercheskiy Indiyskiy: IAF ki zaroorat ke hisaab se badla gaya Su-30
• Russia, France, Israel aur Bharat ke upkaran ek hi jet me
• HAL Nashik me licence se bane: 272 ke order me se 200 se zyada yahin jode gaye
• 2 AL-31FP engine, jinki dhaar (thrust) ±15° mud sakti hai - isliye supermanoeuvrable
• BrahMos-A (~2.5 ton) uthane wala ab tak ka iklauta fighter jet (pehla air launch 22 Nov 2017)

Aapki nazar me IAF ka sabse damdaar jet kaun sa hai? Comment me likho - Jai Hind!
Nyoma airbase wala Short bhi dekho, Reality Shift pe.

Note: Russia ka Su-30SM, Su-30MKI/MKM ke export design par bana hai - bilkul same jet nahi. Video ke jets drawing hain.
Sources: HAL, PIB (22 Nov 2017), Irkut/UAC, Wikipedia (Su-30MKI, Su-30SM).
""",
    "tags": ["su 30 mki", "su 30 mki full form", "su 30 mki brahmos", "sukhoi 30 mki", "सुखोई 30 एमकेआई",
             "su30mki", "indian air force", "iaf fighter jet", "brahmos a", "hal nashik", "thrust vectoring",
             "su 30sm", "defence hindi", "iaf", "reality shift"],
    "hashtags": ["#Shorts", "#Su30MKI", "#IndianAirForce"],
}


def thumbnail(ctx):
    """1080x1920 cover: big 'I = INDIA' over a Flanker carrying BrahMos with afterburner."""
    sky(ctx, 0.5, dusk=0.45)
    flanker_side(ctx, 560, 980, 1000, -0.12, 0.5, burner=1.0, missile=True)
    g = cairo.LinearGradient(0, 1150, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.85)
    ctx.rectangle(0, 1150, W, H - 1150)
    ctx.set_source(g)
    ctx.fill()
    g = cairo.LinearGradient(0, 0, 0, 760)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.9)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 760)
    ctx.set_source(g)
    ctx.fill()
    vignette(ctx)
    text(ctx, "I = INDIA", 540, 280, 190, SAFFRON, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "SU-30 MKI", 540, 480, 130, INK, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    tag(ctx, "RUSSIA NE BHI LIYA", 540, 640, RED, 1.0, size=44)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, INK, a=0.7)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.su30")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
