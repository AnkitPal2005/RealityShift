"""Reality Shift Short: Haji Pir - India won this pass in the 1965 war and then gave it back (Ek Jung Ek Raaz, 25 Nov 2026).

Facts (see SOURCES): in Aug 1965 (Operation Gibraltar) infiltrators entered Kashmir through the Haji Pir route; 1 Para
under Major (later Lt Gen) Ranjit Singh Dayal climbed through the night of 27 Aug in heavy rain and took Haji Pir Pass
on the morning of 28 Aug 1965; holding it would have cut the Jammu-Poonch-Uri-Srinagar route by over 200 km; under the
Tashkent Declaration (Jan 1966) both sides went back to pre-5 Aug 1965 positions and India handed the pass back; Dayal
later said "It was a mistake to hand it back." Not used: exact road km before/after (sources differ), any leader blame.
Debate (no party, no person attacked): "Shanti ke liye sahi tha ya galti?"
Format: 9:16, ~30 s, 6 scenes; conflict by 0:04, map callout instead of exposition.
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
from shorts.akashteer import soldier
from shorts.zorawar import ridges
from shorts.akashteer import ell

TOPIC = "HAJI PIR - JEETA HUA DARRA WAPAS KYUN DIYA (1965)"
OUTPUTS = {"edge": "haji_pir_short.mp4"}
LEGO = {"header": "radar", "caption": "typewriter", "transition": "shutter", "palette": "amber", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.25
TAIL_PAD = 0.22
TRIM = {"thresh": 0.006, "keep": 0.04, "keep_tail": 0.06}
MUSIC_BPM = 100          # >= 6 away from K9 Vajra (92)
MUSIC_STYLE = "march"    # k9 tension, insas ambient
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.05}
KIKI_PAUSE_MS = 0
MAX_SECONDS = 35.0

PAL = lego.PALETTES["amber"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
WHITE = (1.0, 1.0, 1.0)
GOLD = hexc("#FFD166")
RED = hexc("#E2483A")
CYAN = hexc("#5FD3FF")
GREY = hexc("#8A8F96")
GROUND = 1040

SOURCES = [
    "Wikipedia - Battle of Haji Pir Pass (1965): https://en.wikipedia.org/wiki/Battle_of_Haji_Pir_Pass_(1965)",
    "The Tribune - Return of Haji Pir still haunts us (Dayal: 'It was a mistake to hand it back'; route shorter by "
    "over 200 km): https://www.tribuneindia.com/news/archive/return-of-haji-pir-still-haunts-us-287239",
    "IDSA Journal of Defence Studies 9(3) 2015 - The Battle of Haji Pir: "
    "https://www.idsa.in/system/files/jds/jds_9_3_2015_BattleofHajiPir.pdf",
    "Indian Defence Review - Capture of Hajipir Pass, a saga of guts and glory: "
    "https://indiandefencereview.com/capture-of-hajipir-pass-a-saga-of-guts-and-glory/",
    "WION - Operation Gibraltar: infiltration through Haji Pir Pass: https://www.wionews.com/india-news/operation-"
    "gibraltar-the-day-when-pakistan-infiltrated-deep-within-india-through-haji-pir-pass-323788",
]

SPEC = [
    {"key": "hook", "accent": SAFFRON, "text": "",
     "visual": "A mountain pass at dawn: the tricolour rises on the peak; then a red HANDED BACK stamp slams down and "
               "the flag fades",
     "vo": [("hook", [("भारत ने ये दर्रा", "BHARAT NE YE DARRA"), ("जंग में जीता।", "JUNG MEIN JEETA")]),
            ("punch", [("और फिर खुद ही", "AUR PHIR KHUD HI"), ("वापस दे दिया।", "WAPAS DE DIYA")])]},
    {"key": "ghuspaith", "accent": RED, "text": "",
     "visual": "Night, 1965 chip: dark infiltrator silhouettes file through the pass along a dashed red path into "
               "the valley",
     "vo": [("tell", [("उन्नीस सौ पैंसठ में", "1965 MEIN"), ("यहीं से घुसपैठिए", "YAHIN SE GHUSPAITHIYE"),
                      ("कश्मीर में आ रहे थे।", "KASHMIR MEIN AA RAHE THE")])]},
    {"key": "chadhai", "accent": GOLD, "text": "",
     "visual": "Rain at night: a file of soldiers climbs a steep ridge; dawn breaks and the tricolour goes up on the "
               "top with a 28 AUG 1965 chip",
     "vo": [("build", [("तो मेजर रंजीत सिंह दयाल", "TO MAJOR RANJIT SINGH DAYAL"), ("रात भर", "RAAT BHAR"),
                       ("बारिश में चढ़े।", "BAARISH MEIN CHADHE")]),
            ("punch", [("और अट्ठाईस अगस्त की सुबह", "AUR 28 AUGUST KI SUBAH"), ("हाजी पीर पर", "HAJI PIR PAR"),
                       ("तिरंगा लहरा दिया।", "TIRANGA LEHRA DIYA")])]},
    {"key": "raasta", "accent": INDIA_GREEN, "text": "",
     "visual": "Map callout: Jammu to Srinagar - a long red road around the mountains vs a short green line through "
               "Haji Pir; a -200 KM chip",
     "vo": [("build", [("इस दर्रे से", "IS DARRE SE"), ("जम्मू से श्रीनगर का रास्ता", "JAMMU SE SRINAGAR KA RAASTA"),
                       ("दो सौ किलोमीटर तक", "200 KILOMETER TAK"), ("छोटा हो जाता।", "CHHOTA HO JAATA")])]},
    {"key": "tashkent", "accent": GREY, "text": "",
     "visual": "A long table, a treaty paper and a pen signing; on the map the Haji Pir dot turns grey; TASHKENT 1966 "
               "chip",
     "vo": [("tell", [("पर ताशकंद समझौते में", "PAR TASHKENT SAMJHAUTE MEIN"), ("भारत ने इसे", "BHARAT NE ISE"),
                      ("लौटा दिया।", "LAUTA DIYA")])]},
    {"key": "debate", "accent": SAFFRON, "text": "",
     "visual": "The officer stands with a GALTI THI chip; the poll asks SHANTI KE LIYE SAHI YA GALTI",
     "vo": [("tell", [("खुद दयाल ने कहा", "KHUD DAYAL NE KAHA"), ("ये गलती थी।", "YE GALTI THI")]),
            ("punch", [("तो हाजी पीर लौटाना", "TO HAJI PIR LAUTANA"), ("शांति के लिए सही था", "SHANTI KE LIYE SAHI THA"),
                       ("या गलती।", "YA GALTI?")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "DARRA": GOLD, "JEETA": INDIA_GREEN, "WAPAS": RED, "1965": RED, "GHUSPAITHIYE": RED, "KASHMIR": SAFFRON,
    "RANJIT": SAFFRON, "DAYAL": SAFFRON, "BAARISH": CYAN, "28": GOLD, "AUGUST": GOLD, "HAJI": GOLD, "PIR": GOLD,
    "TIRANGA": SAFFRON, "200": INDIA_GREEN, "KILOMETER": INDIA_GREEN, "CHHOTA": INDIA_GREEN, "TASHKENT": GREY,
    "LAUTA": RED, "GALTI": RED, "GALTI?": RED, "SHANTI": CYAN, "SAHI": INDIA_GREEN,
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".")] = HOT[_k]


def at(scene, key, frac, d):
    return scene.cue(key, frac * d)


# ============================================================ scenery & props

PEAK = (600, 430)


def valley(ctx, t, night=0.0, rain=0.0):
    """Pir Panjal ridges: green lower slopes, rock above, the pass notch at PEAK."""
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    if night > 0.5:
        for at_, c in ((0, "#060A18"), (1, "#1A2638")):
            g.add_color_stop_rgb(at_, *hexc(c))
    else:
        for at_, c in ((0, "#3A5A8A"), (0.6, "#E8A86A"), (1, "#F4D0A0")):
            g.add_color_stop_rgb(at_, *hexc(c))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    ridges(ctx, t)
    ctx.move_to(-60, GROUND)                                       # the near ridge with the pass notch
    for x, y in ((-60, 900), (200, 700), (420, 520), (PEAK[0], PEAK[1]), (780, 500), (960, 640), (1140, 760),
                 (1140, GROUND)):
        ctx.line_to(x, y)
    ctx.close_path()
    rgba(ctx, hexc("#24301E") if night > 0.5 else hexc("#4A6A34"))
    ctx.fill()
    ctx.rectangle(0, GROUND - 10, W, H)
    rgba(ctx, hexc("#1A2214") if night > 0.5 else hexc("#3A5228"))
    ctx.fill()
    if rain > 0:
        for i in range(120):
            x = (rnd(i, 1) * (W + 300) - t * 300) % (W + 300) - 150
            y = (rnd(i, 2) * H + t * 1400) % H
            line(ctx, [(x, y), (x - 14, y + 44)], (0.75, 0.85, 1.0), 2, 0.45 * rain)


def chip(ctx, s, x, y, c, u, size=54):
    if u <= 0:
        return
    k = ease_out_back(clamp(u / 0.35))
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    w = text_width(ctx, s, size, font=CAPTION_FONT, bold=False) + 50
    rrect(ctx, -w / 2, -size * 0.75, w, size * 1.5, 12)
    rgba(ctx, (0.03, 0.02, 0.01), 0.85)
    ctx.fill()
    rrect(ctx, -w / 2, -size * 0.75, w, size * 1.5, 12)
    rgba(ctx, c)
    ctx.set_line_width(5)
    ctx.stroke()
    text(ctx, s, 0, 0, size, c, font=CAPTION_FONT, bold=False)
    ctx.restore()


def stamp(ctx, s, x, y, u, c=RED, size=84, ang=-0.18):
    if u <= 0:
        return
    k = 1 + 1.2 * (1 - ease_out_cubic(clamp(u / 0.25)))
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(k, k)
    w = text_width(ctx, s, size, font=CAPTION_FONT, bold=False) + 60
    rrect(ctx, -w / 2, -size * 0.8, w, size * 1.6, 10)
    rgba(ctx, c, clamp(u / 0.25))
    ctx.set_line_width(10)
    ctx.stroke()
    text(ctx, s, 0, 0, size, c, font=CAPTION_FONT, bold=False, a=clamp(u / 0.25))
    ctx.restore()


def climber(ctx, x, y, s, t, k=0, dark=True):
    """Small soldier silhouette climbing (rifle on the back), stepping in place."""
    c = (0.07, 0.09, 0.06) if dark else hexc("#3A4A2A")
    step = math.sin(t * 6 + k)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.rotate(-0.25)
    line(ctx, [(0, -60), (-14 + 10 * step, 0)], c, 12)
    line(ctx, [(0, -60), (16 - 10 * step, -4)], c, 12)
    rrect(ctx, -18, -130, 36, 76, 12)
    rgba(ctx, c)
    ctx.fill()
    circle(ctx, 2, -150, 18, c)
    ell(ctx, 2, -162, 22, 9)
    rgba(ctx, c)
    ctx.fill()
    line(ctx, [(-24, -150), (-10, -40)], c, 6)                        # rifle
    line(ctx, [(14, -110), (40, -80 + 8 * step)], c, 9)              # reaching arm
    ctx.restore()


def map_panel(ctx, t, u_long, u_short, grey=0.0):
    """Schematic map (not to scale): Jammu at the bottom, Srinagar at the top, Poonch and Uri on the west side;
    the long road loops east, the short line runs Poonch - Haji Pir - Uri."""
    rrect(ctx, 80, 300, 920, 760, 24)
    rgba(ctx, hexc("#1A140C"), 0.92)
    ctx.fill()
    rrect(ctx, 80, 300, 920, 760, 24)
    rgba(ctx, PAL["ui"], 0.6)
    ctx.set_line_width(4)
    ctx.stroke()
    for i in range(5):                                             # mountain hatching
        x0 = 380 + 80 * i
        line(ctx, [(x0, 700), (x0 + 40, 640), (x0 + 80, 700)], hexc("#6A5A3A"), 4, 0.7)
    pts = {"JAMMU": (720, 980), "POONCH": (260, 780), "HAJI PIR": (300, 620), "URI": (330, 470),
           "SRINAGAR": (640, 380)}
    long_road = [pts["JAMMU"], (880, 820), (900, 600), (820, 460), pts["SRINAGAR"]]
    n = len(long_road) - 1
    seg = u_long * n
    drawn = [long_road[0]]
    for i in range(n):
        if seg <= i:
            break
        f = clamp(seg - i)
        drawn.append((lerp(long_road[i][0], long_road[i + 1][0], f), lerp(long_road[i][1], long_road[i + 1][1], f)))
    if len(drawn) > 1:
        line(ctx, drawn, RED, 12, 0.9)
    short = [pts["JAMMU"], pts["POONCH"], pts["HAJI PIR"], pts["URI"], pts["SRINAGAR"]]
    n = len(short) - 1
    seg = u_short * n
    drawn = [short[0]]
    for i in range(n):
        if seg <= i:
            break
        f = clamp(seg - i)
        drawn.append((lerp(short[i][0], short[i + 1][0], f), lerp(short[i][1], short[i + 1][1], f)))
    if len(drawn) > 1:
        ctx.set_dash([28, 14])
        line(ctx, drawn, INDIA_GREEN, 12, 0.95)
        ctx.set_dash([])
    for name, (x, y) in pts.items():
        hp = name == "HAJI PIR"
        c = mix_c(GOLD, GREY, grey) if hp else WHITE
        if hp:
            glow(ctx, x, y, 70, c, 0.5 * (1 - grey))
        circle(ctx, x, y, 16 if hp else 11, c)
        text(ctx, name, x + (0 if name in ("JAMMU", "SRINAGAR") else 120), y - 36 if name != "JAMMU" else y + 44,
             34 if hp else 30, c, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=6)
    text(ctx, "NOT TO SCALE", 880, 1030, 22, GREY, font=CAPTION_FONT, bold=False)


def mix_c(a, b, u):
    return tuple(p + (q - p) * clamp(u) for p, q in zip(a, b))


def treaty_table(ctx, t, sign):
    g = cairo.RadialGradient(540, 700, 60, 540, 700, 900)
    g.add_color_stop_rgb(0, *hexc("#4A3A2A"))
    g.add_color_stop_rgb(1, *hexc("#120C08"))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    for x in (200, 880):                                           # two empty chairs
        rrect(ctx, x - 70, 560, 140, 200, 16)
        rgba(ctx, hexc("#5A2A1E"))
        ctx.fill()
    rrect(ctx, 80, 760, 920, 60, 10)                               # table
    rgba(ctx, hexc("#6A4428"))
    ctx.fill()
    rrect(ctx, 80, 820, 920, 220, 4)
    rgba(ctx, hexc("#2A5A3A"))
    ctx.fill()
    ctx.save()                                                     # treaty paper
    ctx.translate(540, 720)
    ctx.rotate(-0.06)
    rrect(ctx, -170, -110, 340, 220, 6)
    rgba(ctx, hexc("#F4EEDC"))
    ctx.fill()
    for k in range(6):
        line(ctx, [(-140, -80 + 26 * k), (140 - 40 * (k % 2), -80 + 26 * k)], hexc("#9A8A6A"), 4, 0.8)
    if sign > 0:                                                   # signature scribble
        pts = [(-20 + 120 * u, 70 + 12 * math.sin(u * 18)) for u in [i / 30 * clamp(sign) for i in range(31)]]
        line(ctx, pts, hexc("#1A2A6A"), 5)
    ctx.restore()
    px = -20 + 120 * clamp(sign) + 540
    ctx.save()                                                     # pen
    ctx.translate(px, 790 + 12 * math.sin(clamp(sign) * 18))
    ctx.rotate(-0.8)
    rrect(ctx, -8, -120, 16, 120, 6)
    rgba(ctx, hexc("#1A1A1A"))
    ctx.fill()
    ctx.restore()


# ============================================================ scenes

class Hook(Cued):
    """The tricolour rises on the pass; HANDED BACK stamp; the flag fades."""

    def events(self, d):
        return [(at(self, "JEETA", 0.3, d), "whoosh"), (at(self, "WAPAS", 0.75, d), "thud")]

    def draw(self, ctx, t, d):
        tj = at(self, "JEETA", 0.3, d)
        tw = at(self, "WAPAS", 0.75, d)
        valley(ctx, t)
        rise = ease_out_cubic(clamp((t - tj + 0.3) / 0.8))
        fade = clamp((t - tw) / 0.6)
        fx, fy = PEAK[0] - 4, PEAK[1] - 40 - 120 * rise
        line(ctx, [(PEAK[0] - 8, PEAK[1] + 10), (PEAK[0] - 8, PEAK[1] - 200)], hexc("#C9C9C9"), 7)
        ctx.push_group()
        flag(ctx, fx, fy, 210, 132, "in", t)
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(1 - 0.75 * fade)
        soldier(ctx, 230, GROUND - 10, 0.62, t, pose="fist" if t < tw else "look_up")
        soldier(ctx, 880, GROUND - 10, 0.6, t, pose="point" if t < tw else "look_up", flip=True)
        stamp(ctx, "HANDED BACK", 540, 860, t - tw)


class Ghuspaith(Cued):
    """Night, 1965: infiltrator silhouettes file through the pass along a dashed red path."""

    def events(self, d):
        return [(0.1, "beep"), (at(self, "KASHMIR", 0.7, d), "alarm")]

    def draw(self, ctx, t, d):
        valley(ctx, t, night=1.0)
        path = [(PEAK[0] + 40, PEAK[1] - 10), (700, 620), (520, 780), (760, 960), (560, 1100)]
        ctx.set_dash([20, 16], -t * 60)
        line(ctx, path, RED, 6, 0.85)
        ctx.set_dash([])
        for i in range(6):                                          # figures walking down the path
            u = (t * 0.12 + i / 6) % 1
            seg = u * (len(path) - 1)
            j = min(int(seg), len(path) - 2)
            f = seg - j
            x = lerp(path[j][0], path[j + 1][0], f)
            y = lerp(path[j][1], path[j + 1][1], f)
            climber(ctx, x, y, 0.55 + 0.4 * u, t, k=i)
        chip(ctx, "1965", 540, 280, RED, t / 0.4, size=64)
        chip(ctx, "OPERATION GIBRALTAR", 540, 390, WHITE, (t - 0.4) / 0.4, size=38)


class Chadhai(Cued):
    """Rain at night, soldiers climb; dawn; the tricolour goes up on the top (28 AUG 1965)."""

    def events(self, d):
        return [(0.1, "soft_thud"), (at(self, "TIRANGA", 0.8, d), "shimmer")]

    def draw(self, ctx, t, d):
        tm = at(self, "AUR 28", 0.55, d)
        tt = at(self, "TIRANGA", 0.8, d)
        dawn = ease_in_out(clamp((t - tm) / 0.8))
        if dawn < 1:
            valley(ctx, t, night=1.0, rain=1.0 - dawn)
        if dawn > 0:
            ctx.push_group()
            valley(ctx, t, night=0.0)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(dawn)
        for i in range(5):                                          # the file of climbers up the ridge
            u = clamp(t / max(1.0, tm) * 0.8 + i * 0.05)
            x = lerp(80 + 60 * i, PEAK[0] - 120 + 30 * i, u)
            y = lerp(1000 - 20 * i, PEAK[1] + 120 + 10 * i, u)
            climber(ctx, x, y, 0.8, t, k=i, dark=dawn < 0.5)
        if t >= tt - 0.3:
            rise = ease_out_cubic(clamp((t - tt + 0.3) / 0.7))
            line(ctx, [(PEAK[0] - 8, PEAK[1] + 10), (PEAK[0] - 8, PEAK[1] - 200)], hexc("#C9C9C9"), 7)
            flag(ctx, PEAK[0] - 4, PEAK[1] - 40 - 120 * rise, 210, 132, "in", t)
            glow(ctx, PEAK[0] + 100, PEAK[1] - 120, 220, GOLD, 0.35 * rise)
        chip(ctx, "1 PARA", 760, 860, WHITE, (t - 0.3) / 0.4, size=44)
        chip(ctx, "28 AUG 1965", 760, 960, GOLD, (t - tm) / 0.4, size=56)


class Raasta(Cued):
    """Map: long red road vs short green line through Haji Pir; -200 KM chip."""

    def events(self, d):
        return [(at(self, "JAMMU", 0.3, d), "whoosh"), (at(self, "200", 0.6, d), "pop")]

    def draw(self, ctx, t, d):
        tj = at(self, "JAMMU", 0.3, d)
        t2 = at(self, "200", 0.6, d)
        valley(ctx, t)
        rgba(ctx, (0, 0, 0), 0.45)
        ctx.paint()
        map_panel(ctx, t, clamp((t - tj) / 1.0), clamp((t - t2 + 0.3) / 0.8))
        chip(ctx, "-200 KM", 540, 230, INDIA_GREEN, (t - t2) / 0.4, size=72)


class Tashkent(Cued):
    """Treaty signed at a table; on the map the Haji Pir dot turns grey."""

    def events(self, d):
        return [(at(self, "TASHKENT", 0.3, d), "tick"), (at(self, "LAUTA", 0.75, d), "thud")]

    def draw(self, ctx, t, d):
        tl = at(self, "LAUTA", 0.75, d)
        if t < tl:
            treaty_table(ctx, t, clamp((t - 0.3) / max(0.6, tl - 0.4)))
            chip(ctx, "TASHKENT  1966", 540, 300, GREY, t / 0.4, size=56)
            return
        valley(ctx, t)
        rgba(ctx, (0, 0, 0), 0.45)
        ctx.paint()
        g = clamp((t - tl) / 0.6)
        map_panel(ctx, t, 1.0, 1.0 - g, grey=g)
        stamp(ctx, "LAUTA DIYA", 540, 230, t - tl - 0.2, size=70)


class Debate(Cued):
    """The officer with a GALTI THI chip; poll asks SAHI YA GALTI."""

    def events(self, d):
        return [(at(self, "GALTI THI", 0.3, d), "pop"), (at(self, "TO HAJI", 0.6, d), "tick")]

    def draw(self, ctx, t, d):
        tq = at(self, "TO HAJI", 0.6, d)
        valley(ctx, t)
        rgba(ctx, (0, 0, 0), 0.35)
        ctx.paint()
        soldier(ctx, 540, GROUND - 10, 0.66, t, pose="stand" if t < tq else "point", commander=True)
        if t < tq + 0.2:
            chip(ctx, "\"GALTI THI\"", 540, 360, RED, (t - at(self, "GALTI THI", 0.3, d)) / 0.4, size=64)
            chip(ctx, "- LT GEN RANJIT SINGH DAYAL", 540, 460, WHITE, (t - 0.4) / 0.4, size=30)
        lego.ending(sys.modules[__name__], ctx, t, t - tq, t - tq - 0.8, question=("HAJI PIR LAUTANA", "SAHI YA GALTI?"),
                    options=("SAHI", "GALTI"), y=600)


SCENE_CLASSES = {"hook": Hook, "ghuspaith": Ghuspaith, "chadhai": Chadhai, "raasta": Raasta, "tashkent": Tashkent,
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
        "Jung Mein Jeeta Haji Pir Wapas Kyun Diya? 1965 Ka Raaz #shorts",
        "Haji Pir Lautana: Shanti Ke Liye Sahi Ya Galti? #shorts",
        "Bharat Ne Jeeta Hua Darra Khud Wapas De Diya #shorts",
    ],
    "title": "Jung Mein Jeeta Haji Pir Wapas Kyun Diya? 1965 Ka Raaz #shorts",
    "thumb_text": "JEETA... PHIR LAUTAYA?",
    "queries": ["haji pir", "haji pir pass", "1965 war haji pir"],
    "description": """Haji Pir ka sach: Bharat ne 1965 ki jung mein Haji Pir darra jeeta - aur phir Tashkent samjhaute mein khud hi wapas de diya.

Is Short mein:
- Aug 1965 (Operation Gibraltar): ghuspaithiye Haji Pir ke raaste Kashmir mein aa rahe the
- 1 Para ke Major Ranjit Singh Dayal ne raat bhar baarish mein chadhai ki aur 28 August 1965 ki subah Haji Pir jeeta
- Is darre se Jammu-Poonch-Uri-Srinagar ka raasta 200 km se zyada chhota ho jaata
- Jan 1966 Tashkent Declaration: dono desh 5 August 1965 se pehle ki position par laute, Haji Pir lauta diya gaya
- Baad mein Lt Gen Dayal ne kaha: "It was a mistake to hand it back."

Debate: Haji Pir lautana shanti ke liye sahi tha ya galti? Ye kisi party ya neta ki baat nahi - apni raay comment mein likho.

Sources:
- Wikipedia: Battle of Haji Pir Pass (1965)
- The Tribune: Return of Haji Pir still haunts us
- IDSA Journal of Defence Studies (2015): The Battle of Haji Pir
- Indian Defence Review: Capture of Hajipir Pass
""",
    "tags": ["haji pir", "haji pir pass", "1965 war", "india pakistan war 1965", "tashkent agreement",
             "ranjit singh dayal", "operation gibraltar", "indian army history", "1 para", "kashmir history",
             "reality shift", "defence shorts", "ek jung ek raaz"],
    "hashtags": ["#Shorts", "#HajiPir", "#IndianArmy"],
    "pinned_comment": "Jung mein jeeta hua Haji Pir lautana - shanti ke liye sahi tha ya galti? 🤔 Apni raay likho 👇 "
                      "(SAHI / GALTI)",
}


def thumbnail(ctx):
    valley(ctx, 1.0)
    line(ctx, [(PEAK[0] - 8, PEAK[1] + 10), (PEAK[0] - 8, PEAK[1] - 200)], hexc("#C9C9C9"), 7)
    flag(ctx, PEAK[0] - 4, PEAK[1] - 160, 210, 132, "in", 1.0)
    soldier(ctx, 230, GROUND - 10, 0.66, 1.0, pose="fist")
    stamp(ctx, "HANDED BACK", 560, 860, 1.0)
    text(ctx, "JEETA...", 540, 205, 110, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "PHIR LAUTAYA?", 540, 330, 116, RED, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "HAJI PIR 1965", 540, 1330, 120, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, PAL["ui"], a=0.85)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.haji_pir")
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
