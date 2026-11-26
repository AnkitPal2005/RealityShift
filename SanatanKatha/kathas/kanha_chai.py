"""Kanha Ji Aur Chaiwala (Karm Aur Kripa): a hungry boy waiting hours for a job interview refuses to quit and keeps
revising his notes; a gentle tea-seller with a peacock feather gives him hot chai without taking money and reminds him
Kanha is with him; after clearing the interview he steps out to thank him, only to find a morpankh on the empty cup
and Kanha ji's golden darshan (~29 s, 9 scenes). Kalpanik prerak katha.

Usage (from SanatanKatha/):
  python make.py kanha_chai --preview
  python make.py kanha_chai --kiki-export
  python make.py kanha_chai --kiki-split --check-voice
  python make.py kanha_chai --engine files
"""

import math
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cairo

from core import engine, katha, upload_kit  # noqa: F401
from core.katha import *  # noqa: F401,F403
import core.devta as dv
from core.devta import smooth, ink, ell, limb, hand, eye, place, group, shade  # noqa: F401

from kathas.daadi_morpankh import boy, kanha_light, GOLDEN, FEET
from kathas.eklavya_krishna import sparkle_burst

TOPIC = "KARM AUR KRIPA KANHA JI CHAIWALA INTERVIEW KHALI PET MORPANKH"
OUTPUTS = {"edge": "kanha_chai_short.mp4"}
MUSIC_STYLE = "pulse"
MUSIC_BPM = 92
MUSIC_VOLUME = 0.11
TAIL_PAD = 0.35
MAX_GAP = 0.45
SCENE_WHOOSH = False
SFX_SCALE = 0.5

SKIN = hexc("#D8A070")
PITAMBAR = hexc("#F4B824")
SAFF = hexc("#FF8C1A")
SOURCES = [
    "Original fictional story (Kalpanik prerak katha) - no scripture or real-event claim; labelled in the description.",
    "Shri Krishna iconography (morpankh, pitambar, bansuri, abhaya) follows common bhakti tradition.",
]

S = 0.72


def cam_begin(ctx, cx, cy, zoom, tx=W / 2, ty=H * 0.55):
    ctx.save()
    ctx.translate(tx, ty)
    ctx.scale(zoom, zoom)
    ctx.translate(-cx, -cy)


def cam_end(ctx):
    ctx.restore()


# =============================================================================
# Places & props
# =============================================================================
def office_corridor(ctx, t, glass=True):
    g = cairo.LinearGradient(0, -150, 0, GROUND)
    for at, c in ((0.0, "#2C3848"), (0.6, "#46566C"), (1.0, "#647488")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.rectangle(-250, -250, W + 500, GROUND + 300)
    ctx.fill()
    if glass:
        rrect(ctx, 120, 260, 840, 620, 12)
        rgba(ctx, hexc("#88B8D8"), 0.28)
        ctx.fill()
        for kx in (400, 680):
            line(ctx, [(kx, 260), (kx, 880)], hexc("#2A3644"), 10)
        line(ctx, [(120, 560), (960, 560)], hexc("#2A3644"), 10)
    # Waiting bench
    rrect(ctx, 180, FEET - 120, 420, 24, 6)
    ink(ctx, hexc("#6E4424"), 4)
    for lx in (210, 560):
        ctx.rectangle(lx, FEET - 96, 16, 96)
        rgba(ctx, hexc("#3A281C"))
        ctx.fill()
    # Floor
    ctx.rectangle(-250, GROUND - 30, W + 500, H + 300)
    rgba(ctx, hexc("#2E3440"))
    ctx.fill()
    line(ctx, [(-250, GROUND - 30), (W + 250, GROUND - 30)], hexc("#505C6E"), 5)


def outside_gate(ctx, t):
    g = cairo.LinearGradient(0, -150, 0, GROUND)
    for at, c in ((0.0, "#1A2844"), (0.6, "#324A72"), (1.0, "#5C789E")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.rectangle(-250, -250, W + 500, GROUND + 300)
    ctx.fill()
    # Morning sun glow
    glow(ctx, 820, 320, 240, hexc("#FFE49A"), 0.35)
    circle(ctx, 820, 320, 62, hexc("#FFF2C0"))
    # Office building silhouette
    rrect(ctx, 110, 340, 460, FEET - 340, 10)
    rgba(ctx, hexc("#2A364C"))
    ctx.fill()
    for row in range(5):
        for col in range(4):
            rrect(ctx, 145 + col * 100, 380 + row * 120, 68, 74, 4)
            rgba(ctx, hexc("#9AC8E8"), 0.45)
            ctx.fill()
    ctx.rectangle(-250, GROUND - 30, W + 500, H + 300)
    rgba(ctx, hexc("#242832"))
    ctx.fill()


def cabin_desk(ctx, t):
    g = cairo.LinearGradient(0, -150, 0, GROUND)
    for at, c in ((0.0, "#243040"), (1.0, "#425268")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.rectangle(-250, -250, W + 500, GROUND + 300)
    ctx.fill()
    ctx.rectangle(-250, GROUND - 30, W + 500, H + 300)
    rgba(ctx, hexc("#282C36"))
    ctx.fill()
    # Desk
    rrect(ctx, 320, FEET - 210, 460, 26, 6)
    ink(ctx, hexc("#7A4E2A"), 4)
    ctx.rectangle(360, FEET - 184, 380, 184)
    rgba(ctx, hexc("#54361E"))
    ctx.fill()


def chai_cup(ctx, x, y, s, t, steam=True):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    smooth(ctx, [(-22, -46), (22, -46), (16, 0), (-16, 0)], k=0.1)
    ink(ctx, hexc("#D89A60"), 3)
    smooth(ctx, [(-18, -42), (18, -42), (16, -34), (-16, -34)], k=0.1)
    rgba(ctx, hexc("#8A4A1C"))
    ctx.fill()
    if steam:
        for k in (-1, 1):
            w = 6 * math.sin(t * 5 + k)
            smooth(ctx, [(k * 7, -52), (k * 7 + w, -72), (k * 7 - w, -94)], k=0.4)
            rgba(ctx, (1, 1, 1), 0.55)
            ctx.set_line_width(4)
            ctx.stroke()
    ctx.restore()


def morpankh(ctx, x, y, s, ang, t):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang + 0.04 * math.sin(t * 3))
    ctx.scale(s, s)
    line(ctx, [(0, 28), (0, -28)], hexc("#8A5A2A"), 4)
    ell(ctx, 0, -28, 16, 24)
    ink(ctx, hexc("#1B8A5A"), 2)
    ell(ctx, 0, -28, 10, 16)
    rgba(ctx, hexc("#1A48A8"))
    ctx.fill()
    ell(ctx, 0, -26, 5, 8)
    rgba(ctx, hexc("#121830"))
    ctx.fill()
    ctx.restore()


def notebook(ctx, x, y, t):
    ctx.save()
    ctx.translate(x, y)
    rrect(ctx, -46, -32, 92, 64, 6)
    ink(ctx, hexc("#F6F2E8"), 4)
    line(ctx, [(0, -30), (0, 30)], hexc("#C8B89A"), 3)
    morpankh(ctx, 22, -38, 0.45, 0.3, t)
    ctx.restore()


def chaiwala(ctx, x, y, s, t, pose="pour", flip=False, a=1.0):
    """Proper expressive cartoon chaiwala: ears, brows, mustache, collared yellow kurta, sleeves, dhoti, shoes & morpankh."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(-s if flip else s, s)
        bob = 3 * math.sin(t * 3)
        # Legs & sandals
        for lx in (-26, 26):
            rrect(ctx, lx - 16, -210 + bob, 32, 195, 10)
            ink(ctx, hexc("#F2EDE0"), 4)
            rrect(ctx, lx - 22, -24, 44, 20, 8)
            ink(ctx, hexc("#4A2E1B"), 4)
        # Kurta torso with shoulders & collar
        smooth(ctx, [(-70, -200 + bob), (-82, -405 + bob), (-42, -430 + bob),
                     (42, -430 + bob), (82, -405 + bob), (70, -200 + bob)], k=0.2)
        ink(ctx, PITAMBAR, 5)
        # Collar & placket
        smooth(ctx, [(-26, -430 + bob), (0, -402 + bob), (26, -430 + bob)], k=0.1)
        ink(ctx, hexc("#FFE082"), 3)
        line(ctx, [(0, -402 + bob), (0, -320 + bob)], hexc("#C88A10"), 4)
        # White gamchha draped on shoulder
        smooth(ctx, [(-68, -420 + bob), (-26, -426 + bob), (-18, -230 + bob), (-58, -230 + bob)], k=0.15)
        ink(ctx, hexc("#FAF8F0"), 4)
        # Neck & ears
        rrect(ctx, -18, -455 + bob, 36, 32, 8)
        ink(ctx, SKIN, 3)
        for ex in (-56, 56):
            ell(ctx, ex, -482 + bob, 11, 16)
            ink(ctx, SKIN, 3)
        # Head
        circle(ctx, 0, -488 + bob, 56, SKIN)
        ink(ctx, SKIN, 4)
        # Turban/cap + morpankh
        smooth(ctx, [(-56, -504 + bob), (-42, -552 + bob), (0, -562 + bob), (42, -552 + bob), (56, -504 + bob)], k=0.25)
        ink(ctx, PITAMBAR, 4)
        morpankh(ctx, -30, -558 + bob, 0.58, -0.35, t)
        # Brows, eyes, nose, gentle mustache & smile
        line(ctx, [(-30, -500 + bob), (-10, -504 + bob)], hexc("#2A1A10"), 4)
        line(ctx, [(10, -504 + bob), (30, -500 + bob)], hexc("#2A1A10"), 4)
        eye(ctx, -20, -485 + bob, 9, 11, t)
        eye(ctx, 20, -485 + bob, 9, 11, t)
        ell(ctx, 0, -470 + bob, 6, 8)
        ink(ctx, shade(SKIN, 0.88), 2)
        smooth(ctx, [(-22, -456 + bob), (0, -462 + bob), (22, -456 + bob)], k=0.35)
        rgba(ctx, hexc("#3A2A20"))
        ctx.set_line_width(6)
        ctx.stroke()
        smooth(ctx, [(-14, -445 + bob), (0, -437 + bob), (14, -445 + bob)], k=0.4)
        rgba(ctx, hexc("#3A2014"))
        ctx.set_line_width(4)
        ctx.stroke()
        # Sleeves & arms
        limb(ctx, [(-76, -395 + bob), (-96, -320 + bob), (-82, -245 + bob)], PITAMBAR, 28)
        circle(ctx, -82, -240 + bob, 14, SKIN)
        if pose == "offer":
            limb(ctx, [(76, -395 + bob), (118, -345 + bob), (152, -352 + bob)], PITAMBAR, 28)
            circle(ctx, 154, -352 + bob, 14, SKIN)
            chai_cup(ctx, 166, -335 + bob, 1.35, t)
        else:
            limb(ctx, [(76, -395 + bob), (96, -320 + bob), (82, -245 + bob)], PITAMBAR, 28)
            circle(ctx, 82, -240 + bob, 14, SKIN)
        ctx.restore()
    dv.group(ctx, a, draw)


def interviewer(ctx, x, y, s, t):
    """Proper cartoon corporate interviewer seated on an office chair behind desk: suit, white shirt, tie, glasses."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(-s, s)
        # Office chair backrest behind him
        rrect(ctx, -78, -465, 156, 250, 24)
        ink(ctx, hexc("#1A202C"), 5)
        # Trousers & shoes under desk
        for lx in (-28, 28):
            rrect(ctx, lx - 16, -200, 32, 185, 8)
            ink(ctx, hexc("#1E2430"), 4)
            rrect(ctx, lx - 20, -22, 44, 20, 8)
            ink(ctx, hexc("#101218"), 4)
        # Suit jacket torso
        smooth(ctx, [(-74, -200), (-86, -405), (-38, -430), (38, -430), (86, -405), (74, -200)], k=0.2)
        ink(ctx, hexc("#24344D"), 5)
        # White shirt V + tie
        smooth(ctx, [(-26, -430), (0, -330), (26, -430)], k=0.05)
        ink(ctx, (0.97, 0.97, 0.99), 3)
        smooth(ctx, [(-7, -420), (7, -420), (10, -330), (0, -310), (-10, -330)], k=0.05)
        ink(ctx, hexc("#C83232"), 2)
        # Neck & ears
        rrect(ctx, -18, -455, 36, 30, 8)
        ink(ctx, SKIN, 3)
        for ex in (-54, 54):
            ell(ctx, ex, -482, 10, 15)
            ink(ctx, SKIN, 3)
        # Head & neat hair
        circle(ctx, 0, -488, 54, SKIN)
        ink(ctx, SKIN, 4)
        smooth(ctx, [(-54, -498), (-40, -548), (0, -556), (44, -544), (54, -498), (24, -514), (-24, -514)], k=0.3)
        rgba(ctx, hexc("#222024"))
        ctx.fill()
        # Glasses + friendly eyes & smile
        eye(ctx, -19, -484, 8, 10, t)
        eye(ctx, 19, -484, 8, 10, t)
        for gx in (-19, 19):
            rrect(ctx, gx - 16, -497, 32, 26, 6)
            rgba(ctx, hexc("#141820"))
            ctx.set_line_width(3.5)
            ctx.stroke()
        line(ctx, [(-3, -484), (3, -484)], hexc("#141820"), 3.5)
        smooth(ctx, [(-14, -450), (0, -441), (14, -450)], k=0.4)
        rgba(ctx, hexc("#3A2014"))
        ctx.set_line_width(4)
        ctx.stroke()
        # Arms resting forward on desk
        limb(ctx, [(-80, -395), (-98, -320), (-74, -265)], hexc("#24344D"), 28)
        circle(ctx, -72, -262, 14, SKIN)
        limb(ctx, [(80, -395), (105, -325), (118, -265)], hexc("#24344D"), 28)
        circle(ctx, 120, -262, 14, SKIN)
        ctx.restore()
    dv.group(ctx, 1.0, draw)


# =============================================================================
# Script (9 scenes, ~72 words)
# =============================================================================
SPEC = [
    {"key": "hook", "text": "KHALI PET INTERVIEW",
     "visual": "Outside office gate; hungry boy with resume, golden Kanha ji behind tea stall",
     "vo": [("low", [("खाली पेट इंटरव्यू देने गए", "KHALI PET INTERVIEW DENE GAYE"),
                     ("लड़के के पास कान्हा जी", "LADKE KE PAAS KANHA JI"),
                     ("खुद चायवाले बनकर आए।", "KHUD CHAIWALE BANKAR AAYE.")], 0.04)]},

    {"key": "bhookh", "text": "SUBAH SE BHOOKHA",
     "visual": "Close-up of hungry boy holding empty tiffin, golden morpankh glow",
     "vo": [("low", [("वो सुबह से भूखा", "WO SUBAH SE BHOOKHA"),
                     ("बाहर खड़ा था।", "BAAHAR KHADA THA.")], 0.04)]},

    {"key": "line", "text": "MEHNAT JAARI",
     "visual": "Boy on corridor bench revising notes with morpankh bookmark",
     "vo": [("build", [("भीड़ बहुत थी", "BHEED BAHUT THI"),
                       ("पर वो अपने नोट्स पढ़ता रहा।", "PAR WO APNE NOTES PADHTA RAHA.")], 0.04)]},

    {"key": "chaiwala", "text": "GARAM CHAI",
     "visual": "Smiling chaiwala with morpankh on cap hands him steaming hot chai",
     "vo": [("tell", [("तभी एक चायवाले ने", "TABHI EK CHAIWALE NE"),
                      ("उसे गरम चाय दी।", "USE GARAM CHAI DI.")], 0.04)]},

    {"key": "paise", "text": "KANHA SAATH HAIN",
     "visual": "Chaiwala refuses money gently, points up with warm golden glow",
     "vo": [("tell", [("पैसे लौटाकर बोले", "PAISE LAUTAKAR BOLE"),
                      ("मेहनत कर कान्हा साथ हैं।", "MEHNAT KAR KANHA SAATH HAIN.")], 0.04)]},

    {"key": "interview", "text": "INTERVIEW PASS",
     "visual": "Inside office cabin; boy answers confidently with Kanha aura behind",
     "vo": [("build", [("अंदर जाते ही", "ANDAR JAATE HI"),
                       ("उसका इंटरव्यू पक्का हो गया।", "USKA INTERVIEW PAKKA HO GAYA.")], 0.04)]},

    {"key": "bahar", "text": "KHALI CUP PAR MORPANKH",
     "visual": "Boy comes out looking for chaiwala; only a glowing morpankh on the cup",
     "vo": [("awe", [("बाहर देखा तो कप पर", "BAAHAR DEKHA TO CUP PAR"),
                     ("सिर्फ एक मोरपंख रखा था।", "SIRF EK MORPANKH RAKHA THA.")], 0.04)]},

    {"key": "darshan", "text": "KANHA KA DARSHAN",
     "visual": "Golden Shri Krishna appears smiling with flute and Abhaya blessing",
     "vo": [("awe", [("और हवा में बंसी की", "AUR HAWA MEIN BANSI KI"),
                     ("मीठी धुन गूंज उठी।", "MEETHI DHUN GOONJ UTHI.")], 0.04)]},

    {"key": "jai", "text": "JAI SHRI KRISHNA",
     "visual": "Boy folds hands in joy with Kanha blessing; smooth loop into hook",
     "vo": [("punch", [("जो मानता है वो लिखे", "JO MAANTA HAI WO LIKHE"),
                       ("जय श्री कृष्ण।", "JAI SHRI KRISHNA.")], 0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "INTERVIEW": hexc("#9AD0FF"), "KANHA": GOLD_HI, "CHAIWALE": SAFF, "BHOOKHA": hexc("#FF5A5A"),
    "NOTES": hexc("#9BE07A"), "CHAI": SAFF, "MEHNAT": hexc("#9BE07A"), "PAKKA": hexc("#9BE07A"),
    "MORPANKH": GOLD_HI, "BANSI": GOLD_HI, "KRISHNA.": GOLD_HI,
})


# =============================================================================
# Scene classes
# =============================================================================
class Hook(Cued):
    def events(self, d):
        return [(0.1, "shimmer")]

    def draw(self, ctx, t, d):
        outside_gate(ctx, t)
        kanha_light(ctx, 720, 0.78, t, a=0.72 * ease_out_cubic(clamp(t / 0.8)))
        boy(ctx, 300, FEET, S, t, pose="namaste", mood="low", look=(0.8, -0.2))


class Bhookh(Cued):
    def events(self, d):
        return [(0.1, "soft_thud")]

    def draw(self, ctx, t, d):
        cam_begin(ctx, 450, FEET - 330, 1.45, W / 2, H * 0.5)
        outside_gate(ctx, t)
        kanha_light(ctx, 720, 0.65, t, a=0.25)
        boy(ctx, 430, FEET, S, t, pose="stand", mood="low", look=(0.0, 0.2))
        cam_end(ctx)


class Line(Cued):
    def events(self, d):
        return [(0.15, "tick")]

    def draw(self, ctx, t, d):
        office_corridor(ctx, t)
        kanha_light(ctx, 810, 0.62, t, a=0.22)
        boy(ctx, 390, FEET - 90, S * 0.92, t, pose="stand", mood="neutral", look=(0.0, 0.3))
        notebook(ctx, 430, FEET - 210, t)


class Chaiwala(Cued):
    def beats(self, d):
        return {"chai": self.cue("CHAI", d * 0.65)}

    def events(self, d):
        return [(self.beats(d)["chai"], "dingdong")]

    def draw(self, ctx, t, d):
        office_corridor(ctx, t)
        boy(ctx, 290, FEET, S, t, pose="stand", mood="neutral", look=(0.9, 0.0))
        chaiwala(ctx, 700, FEET, S * 1.38, t, pose="offer", flip=True, a=1.0)


class Paise(Cued):
    def events(self, d):
        return [(0.15, "shimmer")]

    def draw(self, ctx, t, d):
        cam_begin(ctx, 510, FEET - 320, 1.25, W / 2, H * 0.52)
        office_corridor(ctx, t)
        boy(ctx, 300, FEET, S, t, pose="namaste", mood="joy", look=(0.9, -0.1))
        chaiwala(ctx, 700, FEET, S * 1.38, t, pose="stand", flip=True, a=1.0)
        glow(ctx, 700, FEET - 350, 200, GOLDEN, 0.4)
        cam_end(ctx)


class Interview(Cued):
    def beats(self, d):
        return {"pakka": self.cue("PAKKA", d * 0.7)}

    def events(self, d):
        return [(self.beats(d)["pakka"], "dingdong")]

    def draw(self, ctx, t, d):
        cabin_desk(ctx, t)
        kanha_light(ctx, 250, 0.72, t, a=0.35)
        boy(ctx, 260, FEET, S, t, pose="stand", mood="joy", look=(0.9, 0.0))
        interviewer(ctx, 780, FEET, S * 1.38, t)
        # Re-draw desk front over interviewer's lower legs so he sits cleanly behind the desk!
        rrect(ctx, 360, FEET - 210, 440, 26, 6)
        ink(ctx, hexc("#7A4E2A"), 4)
        ctx.rectangle(400, FEET - 184, 360, 184)
        rgba(ctx, hexc("#54361E"))
        ctx.fill()


class Bahar(Cued):
    def beats(self, d):
        return {"mor": self.cue("MORPANKH", d * 0.6)}

    def events(self, d):
        return [(self.beats(d)["mor"], "shimmer")]

    def draw(self, ctx, t, d):
        cam_begin(ctx, 520, FEET - 220, 1.25, W / 2, H * 0.54)
        outside_gate(ctx, t)
        boy(ctx, 300, FEET, S, t, pose="namaste", mood="shock", look=(0.9, 0.3))
        # Bench/table with cup and glowing morpankh
        rrect(ctx, 630, FEET - 120, 140, 20, 6)
        ink(ctx, hexc("#6E4424"), 4)
        chai_cup(ctx, 700, FEET - 120, 1.3, t, steam=False)
        glow(ctx, 700, FEET - 175, 90, GOLDEN, 0.65)
        morpankh(ctx, 700, FEET - 165, 0.85, 0.25, t)
        cam_end(ctx)


class Darshan(Cued):
    def events(self, d):
        return [(0.1, "ghanti")]

    def draw(self, ctx, t, d):
        outside_gate(ctx, t)
        kanha_light(ctx, 700, 0.78, t, a=0.95 * ease_out_cubic(clamp(t / 0.8)))
        dv.petals(ctx, t, n=22, seed=14, a=0.85)
        boy(ctx, 280, FEET, S, t, pose="namaste", mood="joy", look=(0.9, -0.3))


class Jai(Cued):
    def events(self, d):
        return [(0.1, "ghanti")]

    def draw(self, ctx, t, d):
        outside_gate(ctx, t)
        kanha_light(ctx, 700, 0.78, t, a=0.95)
        dv.petals(ctx, t, n=24, seed=19, a=0.9)
        boy(ctx, 280, FEET, S, t, pose="namaste", mood="joy", look=(0.9, -0.4))
        x = clamp((t - (d - 0.45)) / 0.45)
        if x > 0:
            ctx.push_group()
            Hook().draw(ctx, 0.0, d)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(x)


SCENE_CLASSES = {"hook": Hook, "bhookh": Bhookh, "line": Line, "chaiwala": Chaiwala, "paise": Paise,
                 "interview": Interview, "bahar": Bahar, "darshan": Darshan, "jai": Jai}

UPLOAD = {
    "titles": [
        "Khali Pet Interview Dene Gaya... Kanha Ji Khud Chaiwale Banke Aaye #shorts",
        "4 Ghante Bhookha Line Mein Khada Tha... Phir Cup Par Morpankh Mila #shorts",
        "Chaiwale Ne Paise Kyun Nahi Liye? Jai Shri Krishna #shorts",
    ],
    "thumb_text": "MORPANKH MILA",
    "queries": ["krishna ki kahani", "jai shri krishna", "emotional story hindi"],
    "description": """
Khali pet interview dene gaya ladka haar nahi maanta aur line mein baithkar mehnat karta rehta hai. Tabhi ek
muskurata chaiwala use garam chai deta hai... aur baad mein cup par milta hai sirf ek morpankh. Jai Shri Krishna.

Kalpanik prerak katha. Mehnat aur vishwas saath chalein to raasta zaroor khulta hai.

Kya aapne bhi kabhi kisi anjaan ke roop mein Kanha ki kripa mehsus ki hai? Comment mein JAI SHRI KRISHNA likhein.
""",
    "tags": [
        "krishna ki kahani", "jai shri krishna", "kanha ji", "karm aur kripa", "interview motivation",
        "emotional story hindi", "morpankh", "divya rahasya", "prerak katha", "shorts",
    ],
    "hashtags": ["#Shorts", "#JaiShriKrishna", "#Kanha"],
    "pinned_comment": "Kya aapne bhi kabhi kisi anjaan insaan ke roop mein Kanha ji ki madad mehsus ki hai? 🙏 "
                      "Comment mein JAI SHRI KRISHNA zaroor likhein.",
}


def thumbnail(ctx):
    outside_gate(ctx, 0.5)
    kanha_light(ctx, 700, 0.78, 0.5, a=0.92)
    boy(ctx, 270, FEET, S, 0.5, pose="namaste", mood="shock", look=(0.9, -0.3))
    text(ctx, "CUP PAR", 540, 1330, 118, hexc("#FFFFFF"), font=CAPTION_FONT, bold=False,
         stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "MORPANKH!", 540, 1470, 132, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
