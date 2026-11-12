"""Reality Shift Short - "China se 25 KM: Nyoma airbase" (~40s, single voice, recorded in KikiVoice).

Usage:
  python make.py nyoma --kiki-export     # narrator text for KikiVoice
  python make.py nyoma --kiki-split --check-voice
  python make.py nyoma                      # renders from the KikiVoice clips (--engine edge = preview)

Published on the base's first anniversary (operationalised 12 Nov 2025). Seven scenes on a drawn Ladakh valley:
hook (25 KM counter to a dashed LAC line, a fighter touches down) -> opened a year ago today (runway lights come
on, NYOMA name card) -> 13,700 ft altitude gauge and world-record stamp -> before/after: dirt strip becomes a
2.7 km paved runway with hangars and tower, Rs 218 crore by BRO -> reach: schematic Leh -> 180 km -> Nyoma ->
~25 km -> LAC strip -> the catch: thin air, sea level vs 13,700 ft air boxes, jet takes off lighter -> Ladakh's
four bases (Leh, Kargil, Thoise, Nyoma) behind the comment prompt. The LAC strip is a schematic, not a map.
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

TOPIC = "NYOMA AIRBASE LAC"
OUTPUTS = {"edge": "nyoma_short.mp4"}
LEGO = {"header": "intel", "caption": "chip", "transition": "scan", "palette": "glacier", "ending": "prompt"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.6              # keep the voice's own comma / '...' pauses, only clip dead air
TAIL_PAD = 0.25
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 100
MUSIC_STYLE = "tension"    # border stakes (Siachen was ambient @ 80)
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}    # this read came out brisk (145 words in 42s), keep it natural

PAL = lego.PALETTES["glacier"]
ICE = PAL["ui"]
HI = PAL["hi"]
RED = PAL["alert"]
INK = PAL["ink"]
SAFFRON = hexc("#FF9933")
GREEN = hexc("#3DDC84")
STEEL = hexc("#C3CBD4")
TARMAC = hexc("#3A3F46")

SOURCES = [
    "Mudh-Nyoma airbase operationalised 12 Nov 2025: Air Chief Marshal A.P. Singh landed a C-130J; 2.7 km runway for "
    "fighters, transports and helicopters; Rs 218 crore, built by BRO; fourth IAF base in Ladakh after Leh, Kargil and "
    "Thoise; on the Indus, ~180 km southeast of Leh (Tribune India 'IAF chief inaugurates Mudh-Nyoma airbase near LAC'; "
    "Deccan Herald; The Statesman; Daily Excelsior; Vajiram & Ravi current affairs)",
    "Altitude ~13,700 ft, described as the world's highest fighter-capable airfield (WION; Gulf News; Tribune India). "
    "Some reports give ~13,000 ft / 13,629 ft",
    "Distance to the LAC: 23 km (Tribune), ~25 km (Deccan Herald, Free Press Journal), 35 km at the closest point "
    "(Airpower Asia, Jan 2026) - said as 'lagbhag 25 KM'; the description notes the range",
    "Thin air limits aircraft performance at that altitude (Deccan Herald, Nov 2025; Tribune India 'Nyoma airbase to "
    "boost operational logistical capability but vulnerabilities persist') - jets take off with less load",
    "Before the upgrade Nyoma was an Advanced Landing Ground (unpaved strip) (Tribune India 'IAF to get Ladakh's 4th "
    "base at Nyoma'; Vayu Aerospace 2023)",
]

# Written for KikiVoice: one flowing paragraph per scene, and the punctuation sets the pace (user, 12 Nov: "gap ka
# khel to sara comma etc sign ka hai"). "," = a short breath, "..." = a held beat before a reveal, "।" = full stop,
# "?" = lift. One vo line per scene, so the voice's own pauses inside a scene are kept; we only cut between scenes.
# Chunks are just caption groups (3-6 words), split on the same commas the voice breathes at.
SPEC = [
    {"key": "hook", "accent": RED, "text": "25 KM SE LAC",
     "visual": "Ladakh valley; a counter rolls 0 -> 25 KM toward a dashed red LAC line; a fighter touches down",
     "vo": [("hook", [("चीन की सीमा...", "CHEEN KI SEEMA..."), ("बस पच्चीस किलोमीटर दूर।", "BAS 25 KM DOOR."),
                      ("और वहीं, भारत ने बना दिया,", "AUR WAHIN, BHARAT NE BANA DIYA,"),
                      ("लड़ाकू विमानों का अड्डा।", "LADAAKU VIMAANON KA ADDA.")])]},
    {"key": "open", "accent": HI, "text": "12 NOV 2025",
     "visual": "Runway edge lights switch on one by one; '12 NOV 2025' stamp; 'NYOMA • LADAKH' name card",
     "vo": [("tell", [("ठीक एक साल पहले,", "THEEK 1 SAAL PEHLE,"), ("बारह नवंबर को, ये चालू हुआ।", "12 NOVEMBER KO, YE CHAALU HUA."),
                      ("नाम है... न्योमा।", "NAAM HAI... NYOMA.")])]},
    {"key": "height", "accent": ICE, "text": "13,700 FT",
     "visual": "Altitude gauge climbs to 13,700 FT; 'DUNIYA KA SABSE OONCHA FIGHTER AIRBASE' stamp",
     "vo": [("tell", [("इसकी ऊँचाई?", "ISKI OONCHAI?"), ("तेरह हज़ार सात सौ फ़ीट।", "13,700 FEET."),
                      ("जहाँ साँस लेना भी भारी पड़ता है...", "JAHAN SAANS LENA BHI BHAARI PADTA HAI..."),
                      ("वहीं है, दुनिया का सबसे ऊँचा,", "WAHIN HAI, DUNIYA KA SABSE OONCHA,"),
                      ("लड़ाकू हवाई अड्डा।", "LADAAKU HAWAI ADDA.")])]},
    {"key": "build", "accent": SAFFRON, "text": "2.7 KM RUNWAY",
     "visual": "A dirt strip turns into a paved runway (measure '2.7 KM'), hangars and a control tower pop up; "
               "'₹218 CRORE • BRO' tag",
     "vo": [("tell", [("पहले यहाँ, बस मिट्टी की कच्ची पट्टी थी।", "PEHLE YAHAN, BAS MITTI KI KACHCHI PATTI THI."),
                      ("आज, करीब पौने तीन किलोमीटर की", "AAJ, ~2.7 KM KI"), ("पक्की हवाई पट्टी है।", "PAKKI HAWAI PATTI HAI."),
                      ("ख़र्चा?", "KHARCHA?"), ("दो सौ अठारह करोड़ रुपये।", "₹218 CRORE.")])]},
    {"key": "reach", "accent": GREEN, "text": "LEH SE 180 KM AAGE",
     "visual": "Schematic strip: LEH pin -> 180 KM -> NYOMA pin -> ~25 KM -> dashed LAC; a jet icon hops from Nyoma",
     "vo": [("tell", [("और सबसे बड़ी बात...", "AUR SABSE BADI BAAT..."), ("ये लेह से,", "YE LEH SE,"),
                      ("एक सौ अस्सी किलोमीटर आगे है।", "180 KM AAGE HAI."),
                      ("यानी ज़रूरत पड़ी, तो हमारे विमान,", "YAANI ZAROORAT PADI, TO HAMARE VIMAAN,"),
                      ("सीमा के पास से ही उड़ेंगे।", "SEEMA KE PAAS SE HI UDENGE.")])]},
    {"key": "catch", "accent": RED, "text": "PATLI HAWA",
     "visual": "Two air boxes: SEA LEVEL (dense dots) vs 13,700 FT (sparse dots); a jet lifts off carrying less; "
               "'KAM WAZAN' stamp, then 'NAAMUMKIN NAHI'",
     "vo": [("low", [("लेकिन भाई,", "LEKIN BHAI,"), ("यहाँ हवा बहुत पतली है।", "YAHAN HAWA BAHUT PATLI HAI."),
                     ("इसलिए विमान,", "ISLIYE VIMAAN,"), ("कम वज़न लेकर ही उड़ पाते हैं।", "KAM WAZAN LEKAR HI UD PAATE HAIN."),
                     ("मुश्किल है...", "MUSHKIL HAI..."), ("पर नामुमकिन नहीं।", "PAR NAAMUMKIN NAHI.")])]},
    {"key": "ask", "accent": HI, "text": "CHEEN KO SANDESH?",
     "visual": "Ladakh's four IAF bases as chips (LEH, KARGIL, THOISE, NYOMA - the new one glows) behind the "
               "comment prompt 'CHEEN KO / KYA SANDESH?'",
     "vo": [("ask", [("लद्दाख में, वायुसेना का", "LADAKH MEIN, IAF KA"), ("ये चौथा अड्डा है।", "YE CHAUTHA ADDA HAI."),
                     ("अब आप बताइए...", "AB AAP BATAIYE..."), ("चीन को, इससे क्या संदेश गया?", "CHEEN KO, ISSE KYA SANDESH GAYA?"),
                     ("कमेंट में...", "COMMENT MEIN..."), ("जय हिंद!", "JAI HIND!")])]},
]

DELIVERY = delivery.build(SPEC)   # gaps between lines; KikiVoice supplies the performance itself
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {"CHEEN": RED, "25": RED, "KM...": RED, "FIGHTER": HI, "JET!": HI, "1": HI, "SAAL": HI, "12": HI,
       "NOVEMBER": HI, "CHAALU": GREEN, "NYOMA": HI, "OONCHAI?": ICE, "13,700": ICE, "FEET!": ICE, "OONCHA": ICE,
       "KACHCHI": SAFFRON, "~2.7": SAFFRON, "PAKKA": SAFFRON, "RUNWAY": SAFFRON, "₹218": SAFFRON, "CRORE": SAFFRON,
       "BRO": SAFFRON, "LEH": GREEN, "180": GREEN, "SEEDHA": GREEN, "SEEMA": RED, "MUSHKIL": RED, "PATLI": RED,
       "HAWA": RED, "KAM": RED, "WAZAN": RED, "CHAUTHA": HI, "SANDESH?": HI, "MHAARE": SAFFRON, "BHAI": SAFFRON,
       "COMMENT": HI, "DOOR": RED, "AISA": HI, "NAAM": HI, "KHARCH": SAFFRON, "UDAAN": GREEN,
       "PAATE": RED, "MITTI": SAFFRON, "PAKKI": SAFFRON, "PATTI": SAFFRON, "KHARCHA?": SAFFRON, "BADI": GREEN,
       "BAAT...": GREEN, "VIMAAN,": GREEN, "BAHUT": RED, "BATAIYE...": HI, "SOCHO...": HI, "HAMARE": SAFFRON, "SAANS": ICE, "BHAARI": ICE, "KAMAAL": SAFFRON,
       "ZAROORAT": GREEN, "NAAMUMKIN": GREEN, "JAI": SAFFRON, "HIND!": SAFFRON, "YAAD": HI, "HAWAI": HI, "ADDA,": HI, "ADDA": HI, "VIMAANON": ICE, "LADAAKU": ICE, "MEIN.": SAFFRON, "BATAO...": HI, "AIRBASE": HI}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".—")] = HOT[_k]

# ============================================================ world

VY = 880                   # runway line in the valley
RUN_X0, RUN_X1 = 90, 860
LAC_X = 1010            # kept well clear of the runway: the base is ~25 km from the LAC, not on it


def mix(a, b, u):
    return tuple(lerp(x, y, clamp(u)) for x, y in zip(a, b))


FAR = [(0, 600), (110, 470), (230, 560), (350, 430), (470, 540), (600, 400), (720, 520), (850, 440), (960, 540),
       (1080, 460)]
NEAR = [(0, 760), (150, 640), (300, 730), (430, 620), (580, 740), (720, 650), (870, 760), (1000, 660), (1080, 720)]


def ridge(ctx, pts, base, body, snow, cap=0.22):
    ctx.move_to(pts[0][0], base)
    for p in pts:
        ctx.line_to(*p)
    ctx.line_to(pts[-1][0], base)
    ctx.close_path()
    rgba(ctx, body)
    ctx.fill()
    for i in range(1, len(pts) - 1):
        (x0, y0), (px, py), (x1, y1) = pts[i - 1], pts[i], pts[i + 1]
        if py >= y0 or py >= y1:
            continue
        ctx.move_to(px, py)
        ctx.line_to(lerp(px, x1, cap), lerp(py, y1, cap))
        ctx.line_to(lerp(px, x1, cap * 0.5), lerp(py, y1, cap) - 8)
        ctx.line_to(px, lerp(py, y1, cap * 0.8))
        ctx.line_to(lerp(px, x0, cap * 0.5), lerp(py, y0, cap) - 6)
        ctx.line_to(lerp(px, x0, cap), lerp(py, y0, cap))
        ctx.close_path()
        rgba(ctx, snow)
        ctx.fill()


def valley(ctx, t, dusk=0.0):
    """Bright Ladakh day: deep blue sky, bare ochre ridges with thin snow caps, the Indus and the airfield flat."""
    g = cairo.LinearGradient(0, 0, 0, 760)
    g.add_color_stop_rgb(0, *mix(hexc("#0E3B8C"), hexc("#06142E"), dusk))
    g.add_color_stop_rgb(1, *mix(hexc("#7FB8EC"), hexc("#2A3F66"), dusk))
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()
    glow(ctx, 860, 260, 220, (1, 0.97, 0.85), 0.35 * (1 - dusk))
    ridge(ctx, FAR, 900, hexc("#8E7458"), hexc("#F2F6FA"))
    ridge(ctx, NEAR, 900, hexc("#B08A5E"), hexc("#EDE3D3"), cap=0.15)
    g = cairo.LinearGradient(0, 760, 0, 1160)
    g.add_color_stop_rgb(0, *hexc("#C9A672"))
    g.add_color_stop_rgb(1, *hexc("#8C6E45"))
    ctx.rectangle(0, 760, W, H)
    ctx.set_source(g)
    ctx.fill()
    ctx.move_to(0, 1010)                               # the Indus
    for x in range(0, W + 40, 40):
        ctx.line_to(x, 1010 + 18 * math.sin(x / 140 + 1.2) + 6 * math.sin(t * 1.5 + x / 60))
    for x in range(W, -40, -40):
        ctx.line_to(x, 1050 + 14 * math.sin(x / 120 + 0.5) + 6 * math.sin(t * 1.5 + x / 60))
    ctx.close_path()
    rgba(ctx, hexc("#4AA3D9"))
    ctx.fill()


def runway(ctx, t, u=1.0, lights=1.0, paved=1.0, a=1.0):
    """Runway band across the valley; u = how much of its length is built, paved 0 = dirt strip."""
    x1 = lerp(RUN_X0, RUN_X1, clamp(u))
    rrect(ctx, RUN_X0, VY - 26, x1 - RUN_X0, 52, 6)
    rgba(ctx, mix(hexc("#A88A5C"), TARMAC, paved), a)
    ctx.fill()
    if paved > 0.5:
        for x in range(RUN_X0 + 40, int(x1) - 30, 70):
            ctx.rectangle(x, VY - 3, 36, 6)
            rgba(ctx, (1, 1, 1), 0.85 * a)
            ctx.fill()
    n = 14
    for k in range(n):                                   # edge lights switch on left to right
        x = lerp(RUN_X0 + 10, RUN_X1 - 10, k / (n - 1))
        if x > x1:
            break
        on = clamp(lights * n - k)
        for y in (VY - 32, VY + 32):
            circle(ctx, x, y, 5, (1, 0.85, 0.4) if on else (0.4, 0.4, 0.4), a)
            if on:
                glow(ctx, x, y, 22, (1, 0.8, 0.3), 0.45 * on * a)


def lac(ctx, t, a=1.0, x=LAC_X, label=True):
    """Dashed red line standing for the LAC (schematic)."""
    for y in range(380, 1000, 36):
        line(ctx, [(x, y), (x, y + 20)], RED, 6, a)
    if label:
        tag(ctx, "LAC", x - 40, 340, RED, 1.0 if a >= 1 else a, size=40, sub="CHEEN")


def jet(ctx, x, y, L, ang, t, burner=0.0, a=1.0, c=STEEL):
    """Generic delta-wing fighter, side view, nose along ang."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    if burner > 0:
        for k, (fc, fa) in enumerate(((hexc("#FF6A2B"), 0.6), ((1, 0.85, 0.4), 0.8), ((1, 1, 0.9), 0.9))):
            f = burner * (1 + 0.2 * math.sin(t * 50 + k)) * (1 - 0.3 * k)
            ctx.move_to(-L * 0.5, -L * 0.03)
            ctx.line_to(-L * 0.5 - L * 0.3 * f, 0)
            ctx.line_to(-L * 0.5, L * 0.03)
            ctx.close_path()
            rgba(ctx, fc, fa * a)
            ctx.fill()
    ctx.move_to(L * 0.5, 0)                                  # fuselage
    ctx.curve_to(L * 0.4, -L * 0.045, L * 0.3, -L * 0.055, L * 0.15, -L * 0.055)
    ctx.line_to(-L * 0.5, -L * 0.045)
    ctx.line_to(-L * 0.5, L * 0.045)
    ctx.line_to(L * 0.2, L * 0.05)
    ctx.curve_to(L * 0.35, L * 0.045, L * 0.45, L * 0.02, L * 0.5, 0)
    rgba(ctx, c, a)
    ctx.fill()
    ctx.move_to(L * 0.12, L * 0.03)                          # delta wing
    ctx.line_to(-L * 0.42, L * 0.03)
    ctx.line_to(-L * 0.42, L * 0.1)
    ctx.close_path()
    rgba(ctx, shade(c, 0.75), a)
    ctx.fill()
    ctx.move_to(-L * 0.26, -L * 0.05)                        # tail fin
    ctx.line_to(-L * 0.48, -L * 0.05)
    ctx.line_to(-L * 0.46, -L * 0.24)
    ctx.line_to(-L * 0.38, -L * 0.24)
    ctx.close_path()
    rgba(ctx, shade(c, 0.85), a)
    ctx.fill()
    ctx.save()                                               # canopy
    ctx.translate(L * 0.26, -L * 0.055)
    ctx.scale(1, 0.45)
    circle(ctx, 0, 0, L * 0.09, hexc("#2C6DB5"), a)
    ctx.restore()
    for k, cc in enumerate((SAFFRON, (1, 1, 1), hexc("#138808"))):   # roundel-style tricolour flash on the fin
        circle(ctx, -L * 0.42, -L * 0.15, L * 0.045 - k * L * 0.013, cc, a)
    ctx.restore()


def counter(ctx, value, unit, c, u, y=330, title=""):
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
    text(ctx, f"{int(round(value)):,} {unit}", 0, 14, 104, c, font=CAPTION_FONT, bold=False,
         stroke=(0, 0, 0), stroke_w=8)
    ctx.restore()


# ============================================================ scenes

class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"km": c("25", 0.3), "jet": c("LADAAKU", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["km"], "zap"), (b["km"] + 0.9, "thud"), (b["jet"] - 0.3, "whoosh"),
                (b["jet"] + 0.15, "engine", 1.4), (b["jet"] + 1.2, "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        valley(ctx, t)
        runway(ctx, t)
        lac(ctx, t, ease_out_cubic(clamp(t / 0.4)))
        v = lerp(0, 25, ease_in_out(clamp((t - b["km"]) / 0.9)))
        counter(ctx, v, "KM", RED, t - b["km"] + 0.3, title="LAC SE DOORI")
        u = t - b["jet"] + 0.4                          # fighter glides in and touches down
        if u > 0:
            k = ease_out_cubic(clamp(u / 1.6))
            x = lerp(-200, 520, k)
            y = lerp(560, VY - 30, k)
            jet(ctx, x, y, 320, lerp(0.12, 0.0, k), t, burner=0.3 * (1 - k))
            if k >= 1:
                for j in range(3):
                    puff = (t * 2 + j / 3) % 1
                    circle(ctx, 420 - 120 * puff, VY + 10, 10 + 25 * puff, (0.9, 0.85, 0.75), 0.5 * (1 - puff))


class Open(Cued):
    def beats(self, d):
        c = self.cue
        return {"date": c("12", d * 0.3), "on": c("CHAALU", d * 0.6), "name": c("NYOMA", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(b["date"], "thud"), (b["on"], "beep")] + [(b["on"] + 0.08 * k, "tick") for k in range(8)] + \
               [(b["name"], "dingdong")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        valley(ctx, t, dusk=0.7 - 0.3 * clamp((t - b["on"]) / 1.0))
        runway(ctx, t, lights=clamp((t - b["on"]) / 1.0))
        jet(ctx, 560, VY - 30, 300, 0.0, t)
        if t > b["date"]:
            stamp(ctx, 540, 360, t - b["date"], -0.04, 560, 150, HI, [("12 NOV 2025", 0, 96, HI)])
        if t > b["name"]:
            tag(ctx, "NYOMA", 540, 560, ICE, t - b["name"], size=70, sub="LADAKH • SINDHU KINARE")


class Height(Cued):
    def beats(self, d):
        c = self.cue
        return {"q": c("OONCHAI", 0.1), "ft": c("13,700", d * 0.25), "rec": c("DUNIYA", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["q"], "pop"), (b["ft"], "zap"), (b["ft"] + 1.0, "thud"), (b["rec"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        valley(ctx, t)
        runway(ctx, t)
        jet(ctx, 560, VY - 30, 300, 0.0, t)
        k = ease_in_out(clamp((t - b["ft"]) / 1.0))
        x0, y0, y1 = 110, 1060, 260                      # altitude gauge, sea level at the bottom
        line(ctx, [(x0, y0), (x0, y1)], (1, 1, 1), 10, 0.25)
        for ft in range(0, 15001, 2500):
            yy = lerp(y0, y1, ft / 15000)
            line(ctx, [(x0 - 18, yy), (x0 + 18, yy)], (1, 1, 1), 3, 0.6)
            text(ctx, f"{ft:,}", x0 + 30, yy, 24, INK, font=lego.MONO, anchor="l", a=0.8, stroke=(0, 0, 0),
                 stroke_w=4)
        yk = lerp(y0, lerp(y0, y1, 13700 / 15000), k)
        line(ctx, [(x0, y0), (x0, yk)], ICE, 10)
        circle(ctx, x0, yk, 16, ICE)
        if t > b["ft"]:
            counter(ctx, 13700 * k, "FT", ICE, t - b["ft"] + 0.3, y=330, title="NYOMA KI OONCHAI")
        if t > b["rec"]:
            stamp(ctx, 600, 560, t - b["rec"], -0.03, 760, 170, HI,
                  [("DUNIYA KA SABSE OONCHA", -30, 56, INK), ("FIGHTER AIRBASE", 40, 70, HI)])


class Build(Cued):
    def beats(self, d):
        c = self.cue
        return {"dirt": c("KACHCHI", 0.3), "pave": c("~2.7", d * 0.35), "cost": c("₹218", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["dirt"], "soft_thud"), (b["pave"], "whoosh"), (b["pave"] + 0.5, "thud"),
                (b["pave"] + 0.8, "pop"), (b["pave"] + 1.0, "pop"), (b["cost"], "kaching")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        valley(ctx, t)
        u = t - b["pave"]
        paved = ease_in_out(clamp(u / 0.8)) if u > 0 else 0.0
        runway(ctx, t, u=lerp(0.45, 1.0, paved), paved=paved, lights=0 if u < 0.8 else 1)
        if u > 0.6:                                      # hangars and the control tower pop up
            for k, hx in enumerate((210, 330)):
                p = max(0.01, ease_out_back(clamp((u - 0.6 - 0.15 * k) / 0.35)))
                ctx.save()
                ctx.translate(hx, VY - 60)
                ctx.scale(1, p)
                ctx.move_to(-55, 0)
                ctx.curve_to(-55, -70, 55, -70, 55, 0)
                ctx.close_path()
                rgba(ctx, hexc("#7C8792"))
                ctx.fill()
                ctx.restore()
            p = max(0.01, ease_out_back(clamp((u - 0.9) / 0.35)))
            ctx.save()
            ctx.translate(820, VY - 60)
            ctx.scale(1, p)
            ctx.rectangle(-14, -150, 28, 150)
            rgba(ctx, hexc("#E6E1D6"))
            ctx.fill()
            rrect(ctx, -40, -195, 80, 50, 8)
            rgba(ctx, hexc("#2C6DB5"))
            ctx.fill()
            ctx.restore()
        if u > 0.3:                                      # length measure along the runway
            k = ease_out_cubic(clamp((u - 0.3) / 0.6))
            yy = VY + 70
            line(ctx, [(RUN_X0, yy), (lerp(RUN_X0, RUN_X1, k), yy)], SAFFRON, 5)
            for xx in (RUN_X0, lerp(RUN_X0, RUN_X1, k)):
                line(ctx, [(xx, yy - 16), (xx, yy + 16)], SAFFRON, 5)
            tag(ctx, "~2.7 KM", 540, yy + 60, SAFFRON, u - 0.5, size=40)
        if u <= 0 and t > b["dirt"]:
            tag(ctx, "PEHLE: KACHCHI PATTI", 540, 360, SAFFRON, t - b["dirt"], size=44)
        if t > b["cost"]:
            stamp(ctx, 540, 400, t - b["cost"], 0.03, 600, 160, SAFFRON,
                  [("₹218 CRORE", -24, 84, SAFFRON), ("BANAYA BRO NE", 48, 40, INK)])


STRIP_Y = 420
PIN = {"LEH": 140, "NYOMA": 760, "LAC": 940}


class Reach(Cued):
    def beats(self, d):
        c = self.cue
        return {"leh": c("LEH", 0.1), "km": c("180", d * 0.2), "go": c("SEEMA", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(b["leh"], "beep"), (b["km"], "zap"), (b["km"] + 1.0, "beep"), (b["go"], "whoosh"),
                (b["go"] + 0.1, "engine", 1.2)]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        valley(ctx, t)
        runway(ctx, t)
        rrect(ctx, 50, STRIP_Y - 150, 980, 300, 24)       # schematic strip, not a map
        rgba(ctx, PAL["panel"], 0.88)
        ctx.fill_preserve()
        rgba(ctx, GREEN, 0.9)
        ctx.set_line_width(4)
        ctx.stroke()
        text(ctx, "SCHEMATIC • NOT TO SCALE", 80, STRIP_Y - 120, 22, GREEN, font=lego.MONO, anchor="l", a=0.8)
        k = ease_in_out(clamp((t - b["km"]) / 1.0))
        line(ctx, [(PIN["LEH"], STRIP_Y), (lerp(PIN["LEH"], PIN["NYOMA"], k), STRIP_Y)], GREEN, 8)
        for yy in range(STRIP_Y - 110, STRIP_Y + 120, 26):
            line(ctx, [(PIN["LAC"], yy), (PIN["LAC"], yy + 14)], RED, 6)
        text(ctx, "LAC", PIN["LAC"], STRIP_Y + 125, 30, RED, font=lego.MONO)
        circle(ctx, PIN["LEH"], STRIP_Y, 18, INK)
        text(ctx, "LEH", PIN["LEH"], STRIP_Y + 50, 36, INK, font=lego.MONO)
        if k > 0:
            text(ctx, f"~{int(180 * k)} KM", lerp(PIN["LEH"], PIN["NYOMA"], 0.5), STRIP_Y - 44, 46, GREEN,
                 font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=6)
        if k >= 1:
            pulse = 0.5 + 0.5 * math.sin(t * 6)
            glow(ctx, PIN["NYOMA"], STRIP_Y, 60, HI, 0.4 * pulse)
            circle(ctx, PIN["NYOMA"], STRIP_Y, 20, HI)
            text(ctx, "NYOMA", PIN["NYOMA"], STRIP_Y + 50, 36, HI, font=lego.MONO)
            line(ctx, [(PIN["NYOMA"] + 24, STRIP_Y), (PIN["LAC"] - 12, STRIP_Y)], RED, 4, 0.8)
            text(ctx, "~25 KM", (PIN["NYOMA"] + PIN["LAC"]) / 2, STRIP_Y - 40, 34, RED, font=CAPTION_FONT,
                 bold=False, stroke=(0, 0, 0), stroke_w=5)
        u = t - b["go"]
        if u > 0:                                        # a jet takes off from the valley toward the border
            kk = ease_in_out(clamp(u / 1.6))
            jet(ctx, lerp(400, 1250, kk), lerp(VY - 30, 640, kk ** 1.5), 300, -0.18 * kk, t, burner=1.0)


class Catch(Cued):
    def beats(self, d):
        c = self.cue
        return {"m": c("BHAI", 0.1), "air": c("PATLI", d * 0.25), "w": c("WAZAN", d * 0.5),
                "nm": c("NAAMUMKIN", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(b["m"], "thud"), (b["air"], "whoosh"), (b["w"], "boom"), (b["nm"], "dingdong")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        valley(ctx, t, dusk=0.25)
        runway(ctx, t)
        u = t - b["air"]
        if t > b["m"] and u <= 0:
            tag(ctx, "EK MUSHKIL", 540, 380, RED, t - b["m"], size=56)
        if u > 0:                                        # sea level vs 13,700 ft: same box, fewer air molecules
            for k, (lab, n, c, bx) in enumerate((("SEA LEVEL", 64, ICE, 290), ("13,700 FT", 38, RED, 790))):
                p = max(0.01, ease_out_back(clamp((u - 0.2 * k) / 0.35)))
                ctx.save()
                ctx.translate(bx, 430)
                ctx.scale(p, p)
                rrect(ctx, -210, -150, 420, 300, 20)
                rgba(ctx, PAL["panel"], 0.9)
                ctx.fill_preserve()
                rgba(ctx, c)
                ctx.set_line_width(5)
                ctx.stroke()
                for i in range(n):
                    x = -180 + rnd(i, 3 + k) * 360 + 6 * math.sin(t * 3 + i)
                    y = -100 + rnd(i, 9 + k) * 210 + 6 * math.cos(t * 2.6 + i)
                    circle(ctx, x, y, 8, c, 0.85)
                text(ctx, lab, 0, -122, 30, c, font=lego.MONO)
                ctx.restore()
        w = t - b["w"]
        if w > 0:                                        # jet lifts off, light load
            kk = ease_in_out(clamp(w / 1.5))
            jet(ctx, lerp(300, 1150, kk), VY - 30 - 260 * kk ** 2, 280, -0.15 * kk, t, burner=1.0)
            if t < b["nm"]:
                stamp(ctx, 540, 700, w, -0.03, 460, 130, RED, [("KAM WAZAN", 0, 84, RED)])
            else:
                stamp(ctx, 540, 700, t - b["nm"], 0.03, 620, 130, GREEN, [("NAAMUMKIN NAHI", 0, 80, GREEN)])
        else:
            jet(ctx, 300, VY - 30, 280, 0.0, t)


BASES = [("LEH", False), ("KARGIL", False), ("THOISE", False), ("NYOMA", True)]


class Ask(Cued):
    def beats(self, d):
        c = self.cue
        return {"b": c("CHAUTHA", 0.4), "q": c("SANDESH", d * 0.55), "cmt": c("COMMENT", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(b["b"] + 0.2 * k, "pick") for k in range(4)] + [(b["q"] + 0.05, "pop"), (b["cmt"], "dingdong"),
                                                                 (b["cmt"] + 1.1, "pick")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        valley(ctx, t, dusk=0.4 * clamp((t - b["q"]) / 0.4))
        runway(ctx, t)
        dim = 1 - 0.6 * clamp((t - b["q"]) / 0.4)
        for k, (name, new) in enumerate(BASES):
            u = t - b["b"] - 0.2 * k
            if u <= 0:
                continue
            p = max(0.01, ease_out_back(clamp(u / 0.3)))
            x = 160 + k * 253
            ctx.save()
            ctx.translate(x, 1000)
            ctx.scale(p, p)
            w = text_width(ctx, name, 34, font=lego.MONO) + 40
            rrect(ctx, -w / 2, -32, w, 64, 32)
            rgba(ctx, HI if new else PAL["panel"], 0.95 * dim)
            ctx.fill_preserve()
            rgba(ctx, HI if new else ICE, dim)
            ctx.set_line_width(3)
            ctx.stroke()
            text(ctx, name, 0, 2, 34, (0.05, 0.05, 0.08) if new else INK, font=lego.MONO, a=dim)
            ctx.restore()
        if t < b["q"]:
            tag(ctx, "LADAKH KE 4 IAF BASE", 540, 400, ICE, t - b["b"] + 0.2, size=46)
        lego.ending(STORY, ctx, t, t - b["q"], t - b["cmt"], question=("CHEEN KO", "KYA SANDESH?"),
                    suggestions=("SEEDHA JAWAB", "HUM TAIYAAR", "JAI HIND", "AUR BASE"), y=560)


SCENE_CLASSES = {"hook": Hook, "open": Open, "height": Height, "build": Build, "reach": Reach, "catch": Catch,
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
        "Nyoma Airbase: China Se Sirf 25 KM Door",
        "China Se Sirf 25 KM: Bharat Ka Naya Fighter Airbase",
        "Nyoma Airbase: Duniya Ka Sabse Ooncha Fighter Base",
        "13,700 Feet Par Nyoma Airbase: China Se 25 KM",
        "Nyoma Airbase Ka 1 Saal: China Se 25 KM Door",
        "LAC Ke Paas Nyoma Airbase: China Ko Kya Sandesh?",
        "Nyoma Airbase Ladakh: Kachchi Patti Se Fighter Base",
        "₹218 Crore Ka Nyoma Airbase: China Se 25 KM",
        "Ladakh Ka 4th Airbase Nyoma: Kya Hai Khaas?",
        "Nyoma Airbase Explained: 25 KM, 13,700 Feet",
    ],
    "title": "Nyoma Airbase: China Se Sirf 25 KM Door",   # search name first (anniversary searches), hook after
    "thumb_text": "13,700 FT",
    "queries": ["nyoma airbase", "nyoma airbase ladakh", "mudh nyoma airbase"],
    "description": """
Nyoma airbase Ladakh: China ki seema (LAC) se sirf ~25 KM door, 13,700 feet par duniya ka sabse ooncha fighter airbase.
Mudh-Nyoma airbase (न्योमा एयरबेस) 12 November 2025 ko chaalu hua - aaj iska pehla saal poora hua.

Is Short me:
• 12 Nov 2025: Air Chief Marshal A.P. Singh C-130J se utre, Mudh-Nyoma airbase operational hua
• 13,700 feet: duniya ka sabse ooncha fighter-capable airbase, jahan saans lena bhi bhaari padta hai
• Pehle mitti ki kachchi patti, aaj ~2.7 KM ki pakki hawai patti; kharcha ₹218 crore, banaya BRO ne
• Leh se ~180 KM aage: zaroorat padi to IAF ke vimaan seema ke paas se hi udenge
• Mushkil: patli hawa, isliye jet kam wazan lekar udte hain - mushkil hai, par naamumkin nahi
• Ladakh me IAF ka chautha airbase: Leh, Kargil, Thoise ke baad Nyoma

Aapke hisaab se Nyoma airbase se China ko kya sandesh gaya? Comment me likho - Jai Hind!
Agni 1 se Agni 5 tak ki range wala Short bhi dekho, Reality Shift pe.

Note: LAC se doori alag reports me 23 se 35 KM tak di gayi hai; yahan "lagbhag 25 KM" liya hai. Video ki strip
schematic hai, asli map nahi. Sources: Tribune India, Deccan Herald, The Statesman, WION (Nov 2025).
""",
    "tags": ["nyoma airbase", "nyoma airbase ladakh", "mudh nyoma airbase", "न्योमा एयरबेस", "nyoma airfield",
             "mudh airbase", "nyoma", "highest fighter airbase in world", "ladakh airbase", "indian air force",
             "iaf", "india china border", "lac ladakh", "defence hindi", "reality shift"],
    "hashtags": ["#Shorts", "#NyomaAirbase", "#IndianAirForce"],
}


def thumbnail(ctx):
    """1080x1920 cover: '13,700 FT' over the lit runway, a fighter touching down, the LAC dashed on the right."""
    valley(ctx, 0.5, dusk=0.35)
    runway(ctx, 0.5, lights=1.0)
    lac(ctx, 0.5, 1.0, label=False)
    jet(ctx, 470, VY - 120, 560, 0.05, 0.5, burner=0.4)
    g = cairo.LinearGradient(0, 1100, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.85)
    ctx.rectangle(0, 1100, W, H - 1100)
    ctx.set_source(g)
    ctx.fill()
    g = cairo.LinearGradient(0, 0, 0, 800)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.9)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 800)
    ctx.set_source(g)
    ctx.fill()
    vignette(ctx)
    text(ctx, "13,700", 540, 260, 230, INK, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "FT", 540, 480, 220, HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    tag(ctx, "DUNIYA KA SABSE OONCHA FIGHTER BASE", 540, 660, RED, 1.0, size=40)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, INK, a=0.7)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.nyoma")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
