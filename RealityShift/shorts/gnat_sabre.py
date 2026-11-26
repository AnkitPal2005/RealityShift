"""Reality Shift Short: Folland Gnat, the 'Sabre Slayer' - India's smallest fighter in the 1965 air war (Desi Engine / Ek Jung Ek Raaz, 26 Nov 2026).

Facts (see SOURCES): the Folland Gnat (built under licence by HAL) was a very small, light fighter; in 1965 the
Pakistan Air Force flew the US-built F-86 Sabre; on 3 Sep 1965 over Chhamb, Sqn Ldr Trevor Keelor in a Gnat shot down
a Sabre - widely recorded as the IAF's first air-to-air kill of that war (Vir Chakra); the Gnat earned the nickname
"Sabre Slayer". Its small size made it hard to see in a dogfight.
Not used: total kill tallies (both sides dispute them), any claim that it was invisible to radar.
Debate: "Jeet chhote vimaan ki thi ya pilot ke hausle ki?" (no person attacked).
Format: 9:16, ~26 s, 7 scenes; size paradox in line 1, the upset in line 2.
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
from shorts.haji_pir import chip, stamp

TOPIC = "FOLLAND GNAT - SABRE SLAYER (1965 AIR WAR)"
OUTPUTS = {"edge": "gnat_sabre_short.mp4"}
LEGO = {"header": "radar", "caption": "typewriter", "transition": "scan", "palette": "glacier", "ending": "prompt"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.45            # natural breaths, no speed-up (user, 25 Nov)
TAIL_PAD = 0.35
TRIM = {"thresh": 0.006, "keep": 0.04, "keep_tail": 0.06}
MUSIC_BPM = 96           # >= 6 away from Longewala (88)
MUSIC_STYLE = "ambient"  # longewala pulse, haji_pir march
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 0
MAX_SECONDS = 35.0

PAL = lego.PALETTES["glacier"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
WHITE = (1.0, 1.0, 1.0)
GOLD = hexc("#FFD166")
RED = hexc("#E2483A")
CYAN = hexc("#5FD3FF")
GREY = hexc("#8A8F96")
GNAT_C = hexc("#A7B0B8")
SABRE_C = hexc("#C9CDD2")
FIRE = hexc("#FF6A1A")

SOURCES = [
    "Wikipedia - Folland Gnat (Indian service, 'Sabre Slayer'): https://en.wikipedia.org/wiki/Folland_Gnat",
    "Wikipedia - Trevor Keelor (first IAF air kill of the 1965 war, Vir Chakra): "
    "https://en.wikipedia.org/wiki/Trevor_Keelor",
    "Wikipedia - North American F-86 Sabre (Pakistan Air Force service): "
    "https://en.wikipedia.org/wiki/North_American_F-86_Sabre",
]

SPEC = [
    {"key": "hook", "accent": GOLD, "text": "",
     "visual": "Blue sky: a tiny Gnat beside a huge outline; a SABSE CHHOTA chip; the camera pulls back to show how small",
     "vo": [("hook", [("भारत का सबसे छोटा", "BHARAT KA SABSE CHHOTA"), ("लड़ाकू विमान।", "LADAAKU VIMAAN")])]},
    {"key": "ulat", "accent": RED, "text": "",
     "visual": "A big Sabre crosses the frame, gets hit and trails black smoke down",
     "vo": [("punch", [("और उसने अमेरिका के बने", "AUR USNE AMERICA KE BANE"), ("सेबर जेट गिरा दिए।", "SABRE JET GIRA DIYE")])]},
    {"key": "bharosa", "accent": GREY, "text": "",
     "visual": "1965: a formation of four Sabres sweeps across the sky; F-86 SABRE chip",
     "vo": [("tell", [("उन्नीस सौ पैंसठ में", "1965 MEIN"), ("पाकिस्तान को अपने सेबर पर", "PAKISTAN KO APNE SABRE PAR"),
                      ("बहुत भरोसा था।", "BAHUT BHAROSA THA")])]},
    {"key": "chhota", "accent": CYAN, "text": "",
     "visual": "Size check: Sabre outline vs Gnat outline side by side; then the Gnat slips into a cloud and is gone",
     "vo": [("build", [("भारत के पास था नैट", "BHARAT KE PAAS THA GNAT"), ("जो इतना छोटा था", "JO ITNA CHHOTA THA"),
                       ("कि आसमान में", "KI AASMAAN MEIN"), ("दिखता भी नहीं था।", "DIKHTA BHI NAHIN THA")])]},
    {"key": "chhamb", "accent": SAFFRON, "text": "",
     "visual": "Dogfight over Chhamb: the Gnat comes out of the sun behind a Sabre, tracer lines, a puff of fire",
     "vo": [("build", [("तीन सितंबर को", "3 SEPTEMBER KO"), ("छंब के ऊपर", "CHHAMB KE OOPAR"),
                       ("स्क्वाड्रन लीडर ट्रेवर कीलर ने", "SQUADRON LEADER TREVOR KEELOR NE"),
                       ("एक सेबर को निशाना बनाया।", "EK SABRE KO NISHANA BANAYA")])]},
    {"key": "jeet", "accent": INDIA_GREEN, "text": "",
     "visual": "The Gnat climbs past the camera; a SABRE SLAYER stamp slams down",
     "vo": [("tell", [("उस जंग में ये वायु सेना की", "US JUNG MEIN YE VAYU SENA KI"), ("पहली हवाई जीत", "PEHLI HAWAI JEET"),
                      ("मानी जाती है।", "MAANI JAATI HAI")]),
            ("punch", [("तभी से नैट को नाम मिला", "TABHI SE GNAT KO NAAM MILA"), ("सेबर स्लेयर।", "SABRE SLAYER")])]},
    {"key": "debate", "accent": GOLD, "text": "",
     "visual": "The Gnat circles small in the sky; the card asks VIMAAN YA PILOT",
     "vo": [("punch", [("तो जीत छोटे विमान की थी", "TO JEET CHHOTE VIMAAN KI THI"),
                       ("या पायलट के हौसले की।", "YA PILOT KE HAUSLE KI?")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "CHHOTA": GOLD, "SABSE": GOLD, "SABRE": RED, "GIRA": RED, "AMERICA": GREY, "1965": GREY, "BHAROSA": GREY,
    "GNAT": CYAN, "DIKHTA": CYAN, "NAHIN": CYAN, "3": SAFFRON, "SEPTEMBER": SAFFRON, "CHHAMB": SAFFRON,
    "TREVOR": SAFFRON, "KEELOR": SAFFRON, "NISHANA": RED, "PEHLI": INDIA_GREEN, "JEET": INDIA_GREEN,
    "SLAYER": GOLD, "PILOT": CYAN, "HAUSLE": SAFFRON, "KI?": SAFFRON, "VIMAAN": GOLD,
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".")] = HOT[_k]


def at(scene, key, frac, d):
    return scene.cue(key, frac * d)


# ============================================================ scenery & props

def sky(ctx, t, warm=0.0):
    g = cairo.LinearGradient(0, 0, 0, H)
    for at_, c, cw in ((0, "#0E3A78", "#2A2A5A"), (0.55, "#3F86C8", "#C2687A"), (1, "#BFE0F6", "#F4B27A")):
        a, b = hexc(c), hexc(cw)
        g.add_color_stop_rgb(at_, *(p + (q - p) * warm for p, q in zip(a, b)))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    glow(ctx, 860, 300, 260, hexc("#FFF4D0"), 0.45)
    circle(ctx, 860, 300, 64, hexc("#FFF8E6"), 0.95)
    for k in range(7):                                             # drifting cumulus
        cx = (rnd(k, 31) * (W + 700) - t * (40 + 30 * rnd(k, 32))) % (W + 700) - 350
        cy = 380 + rnd(k, 33) * 800
        for j in range(5):
            ell(ctx, cx + j * 64, cy + 14 * math.sin(j * 2.1 + k), 96 - 9 * j, 40)
            rgba(ctx, WHITE, 0.55)
            ctx.fill()
    ctx.move_to(0, H)                                              # far hills of Chhamb
    for x in range(0, W + 40, 40):
        ctx.line_to(x, 1180 + 40 * math.sin(x * 0.008) + 18 * math.sin(x * 0.03))
    ctx.line_to(W, H)
    ctx.close_path()
    rgba(ctx, hexc("#3E5A44"), 0.85)
    ctx.fill()


def ell(ctx, x, y, rx, ry):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, math.tau)
    ctx.restore()


def fighter(ctx, x, y, L, ang=0.0, c=GNAT_C, roundel=True, smoke=0.0, t=0.0, a=1.0, flip=False):
    """Swept-wing fighter in side view, nose to the right (flip=True mirrors it to fly left, upright).
    roundel=True paints the tricolour fin flash (Gnat); False = plain (Sabre, no national marking)."""
    ctx.save()
    ctx.translate(x, y)
    if flip:
        ctx.scale(-1, 1)
    ctx.rotate(ang)
    ctx.move_to(L * 0.5, 0)                                        # fuselage
    ctx.curve_to(L * 0.42, -L * 0.07, L * 0.2, -L * 0.08, -L * 0.1, -L * 0.07)
    ctx.line_to(-L * 0.5, -L * 0.04)
    ctx.line_to(-L * 0.5, L * 0.04)
    ctx.curve_to(-L * 0.1, L * 0.07, L * 0.3, L * 0.07, L * 0.5, 0)
    rgba(ctx, c, a)
    ctx.fill()
    ctx.move_to(L * 0.1, L * 0.02)                                 # swept wing
    ctx.line_to(-L * 0.22, L * 0.22)
    ctx.line_to(-L * 0.32, L * 0.22)
    ctx.line_to(-L * 0.12, L * 0.02)
    ctx.close_path()
    rgba(ctx, shade(c, 0.72), a)
    ctx.fill()
    ctx.move_to(-L * 0.3, -L * 0.05)                               # swept fin
    ctx.line_to(-L * 0.46, -L * 0.26)
    ctx.line_to(-L * 0.52, -L * 0.26)
    ctx.line_to(-L * 0.48, -L * 0.04)
    ctx.close_path()
    rgba(ctx, shade(c, 0.85), a)
    ctx.fill()
    ctx.save()                                                     # canopy
    ctx.translate(L * 0.22, -L * 0.07)
    ctx.scale(1, 0.5)
    circle(ctx, 0, 0, L * 0.08, hexc("#2C6DB5"), a)
    ctx.restore()
    if roundel:
        for k, cc in enumerate((SAFFRON, WHITE, INDIA_GREEN)):
            circle(ctx, -L * 0.45, -L * 0.17, L * 0.04 - k * L * 0.012, cc, a)
    ctx.restore()
    if smoke > 0:                                                  # trailing black smoke behind a hit jet
        dx = -1 if not flip else 1
        for k in range(10):
            u = (k / 10 + t * 0.8) % 1
            circle(ctx, x + dx * (L * 0.5 + 160 * u) * math.cos(ang), y - 60 * u + L * 0.0,
                   (14 + 46 * u) * L / 300, (0.15, 0.14, 0.13), 0.6 * (1 - u) * smoke)
        glow(ctx, x - dx * L * 0.2, y, L * 0.25, FIRE, 0.7 * smoke)


def tracer(ctx, x0, y0, x1, y1, t, n=5):
    for k in range(n):
        u = (t * 3 + k / n) % 1
        px, py = lerp(x0, x1, u), lerp(y0, y1, u)
        line(ctx, [(px, py), (px + (x1 - x0) * 0.06, py + (y1 - y0) * 0.06)], hexc("#FFE38A"), 5, 0.9)


def outline_compare(ctx, cx, cy, L, c, label, u):
    if u <= 0:
        return
    ctx.push_group()
    fighter(ctx, cx, cy, L, c=c, roundel=label == "GNAT")
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(clamp(u / 0.4))
    text(ctx, label, cx, cy + L * 0.33, 46, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=8,
         a=clamp(u / 0.4))


# ============================================================ scenes

class Hook(Cued):
    """A tiny Gnat in a big sky; SABSE CHHOTA."""

    def events(self, d):
        return [(0.1, "whoosh"), (at(self, "CHHOTA", 0.5, d), "pop")]

    def draw(self, ctx, t, d):
        tc = at(self, "CHHOTA", 0.5, d)
        sky(ctx, t)
        zoom = lerp(1.0, 0.45, ease_in_out(clamp(t / max(1.0, d))))
        fighter(ctx, 540 + 30 * math.sin(t * 1.5), 760 + 12 * math.sin(t * 2), 520 * zoom, ang=-0.05, t=t)
        chip(ctx, "SABSE CHHOTA", 540, 330, GOLD, (t - tc) / 0.4, size=64)


class Ulat(Cued):
    """A big Sabre crosses, gets hit and trails smoke down."""

    def events(self, d):
        return [(at(self, "GIRA", 0.6, d), "boom")]

    def draw(self, ctx, t, d):
        tg = at(self, "GIRA", 0.6, d)
        sky(ctx, t)
        hit = clamp((t - tg) / 0.4)
        fall = clamp((t - tg) / 1.4)
        x = lerp(1250, 420, clamp(t / max(1.0, d)))
        y = 620 + 420 * fall * fall
        fighter(ctx, x, y, 560, ang=-0.45 * fall, c=SABRE_C, roundel=False, smoke=hit, t=t, flip=True)
        if hit > 0:
            fighter(ctx, lerp(-100, 900, clamp((t - tg + 0.3) / 1.2)), 380, 220, ang=-0.25, t=t)
        chip(ctx, "F-86 SABRE", 540, 300, RED, t / 0.4, size=58)
        if t >= tg:
            stamp(ctx, "GIRA DIYE", 540, 450, t - tg, c=RED, size=70)


class Bharosa(Cued):
    """1965: a formation of four Sabres sweeps across the sky."""

    def events(self, d):
        return [(0.1, "whoosh"), (at(self, "BHAROSA", 0.7, d), "thud")]

    def draw(self, ctx, t, d):
        sky(ctx, t, warm=0.15)
        u = clamp(t / max(1.0, d))
        for k, (ox, oy) in enumerate(((0, 0), (170, 110), (340, 220), (170, -110))):
            fighter(ctx, lerp(1300, 200, u) + ox, 640 + oy, 300, ang=0.03, c=SABRE_C, roundel=False, t=t, flip=True)
        chip(ctx, "1965", 540, 300, GREY, t / 0.4, size=70)
        chip(ctx, "F-86 SABRE", 540, 410, WHITE, (t - 0.3) / 0.4, size=44)


class Chhota(Cued):
    """Size check: Sabre vs Gnat; the Gnat slips into a cloud."""

    def events(self, d):
        return [(at(self, "GNAT", 0.2, d), "pop"), (at(self, "DIKHTA", 0.7, d), "shimmer")]

    def draw(self, ctx, t, d):
        tg = at(self, "GNAT", 0.2, d)
        td = at(self, "DIKHTA", 0.7, d)
        sky(ctx, t)
        rgba(ctx, hexc("#0A1A30"), 0.35)
        ctx.paint()
        hide = clamp((t - td) / 0.8)
        outline_compare(ctx, 540, 560, 640, SABRE_C, "SABRE", t)
        if hide < 1:
            ctx.push_group()
            outline_compare(ctx, 540 + 300 * hide, 900 - 120 * hide, 330, GNAT_C, "GNAT", t - tg)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(1 - hide)
        if hide > 0:
            for j in range(6):
                ell(ctx, 760 + j * 60, 780 + 12 * math.sin(j * 2), 120 - 10 * j, 60)
                rgba(ctx, WHITE, 0.85 * hide)
                ctx.fill()
            chip(ctx, "DIKHTA BHI NAHIN", 540, 1080, CYAN, (t - td) / 0.4, size=50)


class Chhamb(Cued):
    """Over Chhamb: the Gnat out of the sun behind a Sabre, tracers, a puff of fire."""

    def events(self, d):
        tn = at(self, "NISHANA", 0.75, d)
        return [(0.1, "tick"), (tn - 0.3, "zap"), (tn + 0.2, "boom")]

    def draw(self, ctx, t, d):
        tn = at(self, "NISHANA", 0.75, d)
        sky(ctx, t, warm=0.25)
        bank = 0.25 * math.sin(t * 1.6)
        sx, sy = 650 + 40 * math.sin(t * 1.2), 640 + 50 * math.cos(t * 1.4)
        hit = clamp((t - tn - 0.2) / 0.4)
        fighter(ctx, sx, sy, 380, ang=bank, c=SABRE_C, roundel=False, smoke=hit, t=t)
        gx, gy = 220 + 30 * math.sin(t * 1.3), 760 + 40 * math.cos(t * 1.1)
        fighter(ctx, gx, gy, 230, ang=bank * 0.8 - 0.1, t=t)
        if tn - 0.4 < t < tn + 0.4:
            tracer(ctx, gx + 120, gy - 10, sx - 60, sy, t)
        if hit > 0:
            glow(ctx, sx, sy, 160, FIRE, 0.7 * (1 - clamp((t - tn - 0.2) / 1.2)))
        chip(ctx, "3 SEP 1965  -  CHHAMB", 540, 290, SAFFRON, t / 0.4, size=46)
        chip(ctx, "SQN LDR TREVOR KEELOR", 540, 390, WHITE, (t - at(self, "SQUADRON", 0.4, d)) / 0.4, size=40)


class Jeet(Cued):
    """The Gnat climbs past the camera; SABRE SLAYER stamp."""

    def events(self, d):
        return [(at(self, "PEHLI", 0.3, d), "shimmer"), (at(self, "SLAYER", 0.85, d), "thud")]

    def draw(self, ctx, t, d):
        tp = at(self, "PEHLI", 0.3, d)
        ts = at(self, "SLAYER", 0.85, d)
        sky(ctx, t, warm=0.35)
        u = clamp(t / max(1.0, d))
        fighter(ctx, lerp(260, 640, u), lerp(1000, 640, u), lerp(300, 520, u), ang=-0.35, t=t)
        glow(ctx, 540, 700, 360, GOLD, 0.15 + 0.1 * math.sin(t * 3))
        chip(ctx, "PEHLI HAWAI JEET", 540, 300, INDIA_GREEN, (t - tp) / 0.4, size=54)
        stamp(ctx, "SABRE SLAYER", 540, 450, t - ts, c=GOLD, size=78, ang=-0.1)


class Debate(Cued):
    """The Gnat circles small; card asks VIMAAN YA PILOT."""

    def events(self, d):
        return [(0.1, "tick"), (at(self, "PILOT", 0.6, d), "pop")]

    def draw(self, ctx, t, d):
        sky(ctx, t, warm=0.4)
        rgba(ctx, (0, 0, 0), 0.25)
        ctx.paint()
        fighter(ctx, 540 + 330 * math.cos(t * 0.9), 1180 + 60 * math.sin(t * 0.9), 160, ang=0.1 * math.sin(t), t=t,
                flip=math.sin(t * 0.9) > 0)
        lego.ending(sys.modules[__name__], ctx, t, t - 0.05, t - 0.85, question=("JEET KISKI?", "VIMAAN YA PILOT?"),
                    suggestions=("GNAT", "PILOT"), y=640)


SCENE_CLASSES = {"hook": Hook, "ulat": Ulat, "bharosa": Bharosa, "chhota": Chhota, "chhamb": Chhamb, "jeet": Jeet,
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
        "Bharat Ka Sabse Chhota Jet... Jisne Sabre Gira Diye #shorts",
        "Gnat vs Sabre 1965: Jeet Vimaan Ki Ya Pilot Ki? #shorts",
        "Sabre Slayer: 1965 Ka Chhota Desi Fighter #shorts",
    ],
    "title": "Bharat Ka Sabse Chhota Jet... Jisne Sabre Gira Diye #shorts",
    "thumb_text": "CHHOTA JET, BADA KAAM",
    "queries": ["gnat sabre slayer", "folland gnat", "1965 air war"],
    "description": """Gnat - Bharat ka sabse chhota fighter, jisne 1965 mein American Sabre gira diye aur naam paaya "Sabre Slayer".

Is Short mein:
- 1965 mein Pakistan Air Force ke paas American F-86 Sabre the
- IAF ke paas tha Folland Gnat (HAL ne licence par banaya) - itna chhota ki dogfight mein dikhta bhi mushkil se tha
- 3 September 1965, Chhamb ke upar Squadron Leader Trevor Keelor ne Gnat se ek Sabre ko nishana banaya (Vir Chakra)
- Isse us jung ki IAF ki pehli hawai jeet mana jaata hai
- Tabhi se Gnat ka naam pada "Sabre Slayer"

Debate: jeet chhote vimaan ki thi ya pilot ke hausle ki? Apni raay comment mein likho.

Sources:
- Wikipedia: Folland Gnat
- Wikipedia: Trevor Keelor
- Wikipedia: North American F-86 Sabre
""",
    "tags": ["folland gnat", "sabre slayer", "gnat vs sabre", "1965 war", "1965 air war", "trevor keelor",
             "indian air force", "iaf history", "f-86 sabre", "chhamb 1965", "reality shift", "defence shorts",
             "ek jung ek raaz"],
    "hashtags": ["#Shorts", "#IndianAirForce", "#SabreSlayer"],
    "pinned_comment": "1965 mein Sabre girane wali jeet kiski thi - chhote GNAT vimaan ki ya PILOT ke hausle ki? 🤔 "
                      "Apni raay likho 👇 (GNAT / PILOT)",
}


def thumbnail(ctx):
    sky(ctx, 1.0, warm=0.3)
    fighter(ctx, 700, 880, 640, ang=0.12, c=SABRE_C, roundel=False, smoke=1.0, t=1.0, flip=True)
    fighter(ctx, 300, 640, 300, ang=-0.25, t=1.0)
    tracer(ctx, 420, 620, 640, 860, 0.2)
    text(ctx, "CHHOTA JET", 540, 205, 120, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "BADA KAAM", 540, 335, 120, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "SABRE SLAYER", 540, 1330, 120, RED, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, PAL["ui"], a=0.85)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.gnat_sabre")
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
