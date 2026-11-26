"""Mahadev Aur ICU Ki Raat (Karm Aur Kripa): the doctors had little hope for a mother in the ICU; her son sits on
the hospital stairs calling Mahadev, then runs all night to arrange blood and money; in the morning he puts a bhabhuti
tilak on her forehead; a six-hour operation succeeds - and the doctor says someone else was holding his hand inside
(~27 s, 9 scenes). Kalpanik prerak katha.

Usage (from SanatanKatha/):
  python make.py mahadev_icu --preview
  python make.py mahadev_icu --kiki-split --check-voice
  python make.py mahadev_icu --engine files

Safety (user agreed 26 Nov): the DOCTOR performs the operation and the son does the hard work (blood, money);
Mahadev is present as strength and blessing - never a cure that replaces treatment (no medical claim).
Retention fix (26 Nov data, 0:04-0:08 drop): line 2 is a twist ("only the doctor knew"), not backstory.
Mahadev in every scene: hospital wall mandir, rudraksh, bhabhuti, his blue form behind the OT door, the hand.
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
from core.devta import smooth, ink, ell  # noqa: F401

from kathas import daadi_morpankh as dm
from kathas.daadi_morpankh import boy, phone, clock, GOLDEN, FEET
from kathas.ravan import mahadev, shivling
from kathas.eklavya_krishna import sparkle_burst
from kathas.bees_baar_reject import mahadev_photo, rudraksh, SHIV_BLUE
from kathas.maa_kangan import maa, notes

TOPIC = "KARM AUR KRIPA MAHADEV ICU KI RAAT MAA OPERATION BHABHUTI DOCTOR KA HAATH"
OUTPUTS = {"edge": "mahadev_icu_short.mp4"}
MUSIC_STYLE = "pulse"     # tender heartbeat; mummy_missed_call ambient 88, stage_ka_darr tension 96
MUSIC_BPM = 80            # >= 6 BPM away from 88
MUSIC_VOLUME = 0.11
TAIL_PAD = 0.12           # user 26 Nov: new voice keeps its own breaths; target ~27 s
MAX_GAP = 0.25            # user 26 Nov: new voice, 1.08x + shorter long pauses (~27 s)
SCENE_WHOOSH = False
SFX_SCALE = 0.5

WHITE_COAT = hexc("#F2F4F6")
WALL = hexc("#B8CCC4")
RED_LAMP = hexc("#FF3A2A")
ASH = hexc("#ECECEC")
SOURCES = [
    "Original fictional story (Kalpanik prerak katha) - no scripture, medical or real-event claim; labelled in the "
    "description. The doctors treat the patient; faith is shown only as strength and blessing.",
    "Mahadev's form (jatajuta, crescent, Ganga, Neelkanth, trishul, damru, rudraksha) and bhabhuti/tripundra follow "
    "common Shaiva iconography.",
]

S = 0.72
DOOR_X = 760


# =============================================================================
# Places and props
# =============================================================================
def corridor(ctx, t, night=1.0, lamp=1.0, mandir=1.0):
    """Hospital corridor: pale green walls, tube lights, tiled floor, the ICU double door with a red lamp, a bench
    and a small wall mandir with Mahadev's photo and a diya."""
    top = WALL if night < 0.5 else shade(WALL, 0.55)
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *shade(top, 0.9))
    g.add_color_stop_rgb(0.6, *top)
    g.add_color_stop_rgb(1, *shade(top, 0.5))
    ctx.set_source(g)
    ctx.rectangle(-80, -80, W + 160, H + 160)
    ctx.fill()
    for x in (180, 620):                                       # tube lights
        rrect(ctx, x, 230, 240, 18, 9)
        rgba(ctx, hexc("#F4FAFF"), 0.9)
        ctx.fill()
        glow(ctx, x + 120, 240, 220, hexc("#E8F4FF"), 0.25)
    rrect(ctx, -80, 820, W + 160, 30, 0)                       # dado stripe
    rgba(ctx, shade(top, 0.75))
    ctx.fill()
    ctx.rectangle(-80, GROUND - 30, W + 160, H)                 # tiled floor
    rgba(ctx, hexc("#8A9894") if night < 0.5 else hexc("#4A5654"))
    ctx.fill()
    for k in range(9):
        line(ctx, [(-80 + 150 * k, GROUND - 30), (-300 + 190 * k, H)], hexc("#2E3634"), 3, 0.3)
    for k in range(5):
        line(ctx, [(-80, GROUND + 40 * k * k), (W + 80, GROUND + 40 * k * k)], hexc("#2E3634"), 3, 0.25)
    # ICU double door
    rrect(ctx, DOOR_X - 170, FEET - 760, 340, 760, 6)
    rgba(ctx, hexc("#D8E2E6"))
    ctx.fill()
    line(ctx, [(DOOR_X, FEET - 760), (DOOR_X, FEET)], hexc("#7A8A90"), 6)
    for side in (-1, 1):
        rrect(ctx, DOOR_X + side * 85 - 50, FEET - 640, 100, 140, 8)    # door windows
        rgba(ctx, hexc("#9AD0E8"), 0.7)
        ctx.fill()
    rrect(ctx, DOOR_X - 180, FEET - 770, 360, 780, 6)
    rgba(ctx, hexc("#6A7A80"))
    ctx.set_line_width(14)
    ctx.stroke()
    pulse = 0.6 + 0.4 * math.sin(t * 4)
    glow(ctx, DOOR_X, FEET - 820, 90, RED_LAMP, 0.6 * pulse * lamp)
    rrect(ctx, DOOR_X - 60, FEET - 840, 120, 40, 12)
    rgba(ctx, RED_LAMP, 0.4 + 0.6 * pulse * lamp)
    ctx.fill()
    # small wall mandir
    if mandir > 0:
        mahadev_photo(ctx, 200, 560, t, s=0.8, lit=0.7 * mandir)
        rrect(ctx, 120, 660, 160, 18, 4)
        rgba(ctx, hexc("#7A4A1E"))
        ctx.fill()
        dv_diya(ctx, 200, 650, t)
    if night > 0.5:
        rgba(ctx, hexc("#0A1020"), 0.28 * night)
        ctx.paint()


def dv_diya(ctx, x, y, t):
    ell(ctx, x, y, 24, 9)
    rgba(ctx, hexc("#B8642A"))
    ctx.fill()
    f = 1 + 0.15 * math.sin(t * 13)
    glow(ctx, x, y - 22, 46, GOLDEN, 0.6)
    smooth(ctx, [(x, y - 40 * f), (x + 9, y - 14), (x, y - 6), (x - 9, y - 14)], k=0.3)
    ink(ctx, hexc("#FFB23A"))


def stairs(ctx, t):
    """Hospital stairwell at night: steps rising to the left, a railing, the diya's glow from the corridor."""
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc("#2A3640"))
    g.add_color_stop_rgb(1, *hexc("#141A20"))
    ctx.set_source(g)
    ctx.rectangle(-80, -80, W + 160, H + 160)
    ctx.fill()
    window_moon(ctx, 820, 420)
    for k in range(9):
        y = FEET - 60 * k
        x0 = -80
        x1 = 620 - 70 * k
        ctx.rectangle(x0, y - 60, x1 - x0, 60)
        rgba(ctx, shade(hexc("#6A7880"), 0.7 + 0.03 * k))
        ctx.fill()
        line(ctx, [(x0, y - 60), (x1, y - 60)], hexc("#9AA8B0"), 3, 0.6)
    line(ctx, [(660, FEET - 200), (60, FEET - 740)], hexc("#B8C2C8"), 8)               # railing
    for k in range(7):
        x = 620 - 90 * k
        line(ctx, [(x, FEET - 60 - 60 * k * 0.9), (x, FEET - 236 - 80 * k)], hexc("#8A969C"), 5, 0.8)
    ctx.rectangle(-80, GROUND - 30, W + 160, H)
    rgba(ctx, hexc("#20282E"))
    ctx.fill()


def window_moon(ctx, x, y):
    rrect(ctx, x - 140, y - 160, 280, 320, 10)
    rgba(ctx, hexc("#0A1430"))
    ctx.fill()
    circle(ctx, x + 50, y - 50, 40, hexc("#E8ECF4"), 0.9)
    glow(ctx, x + 50, y - 50, 120, hexc("#C8D8FF"), 0.3)
    line(ctx, [(x, y - 160), (x, y + 160)], hexc("#3A4650"), 10)
    line(ctx, [(x - 140, y), (x + 140, y)], hexc("#3A4650"), 10)
    rrect(ctx, x - 150, y - 170, 300, 340, 10)
    rgba(ctx, hexc("#4A5660"))
    ctx.set_line_width(14)
    ctx.stroke()


def icu_room(ctx, t, morning=1.0):
    """ICU bay: morning window light, monitor with a green heartbeat, IV stand, Mahadev photo by the bed."""
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc("#C8DCD6"))
    g.add_color_stop_rgb(0.65, *hexc("#A8C2BA"))
    g.add_color_stop_rgb(1, *hexc("#5A6E68"))
    ctx.set_source(g)
    ctx.rectangle(-80, -80, W + 160, H + 160)
    ctx.fill()
    rrect(ctx, 60, 260, 320, 380, 10)                          # window with sunrise
    gw = cairo.LinearGradient(0, 260, 0, 640)
    gw.add_color_stop_rgb(0, *hexc("#7AA8E0"))
    gw.add_color_stop_rgb(1, *hexc("#FFD29A"))
    ctx.set_source(gw)
    ctx.fill()
    dv.sun_disc(ctx, 220, 560, 46, t, a=0.8 * morning, rays=12)
    line(ctx, [(220, 260), (220, 640)], hexc("#E8EEF0"), 10)
    glow(ctx, 380, 700, 520, hexc("#FFE6B8"), 0.3 * morning)
    rrect(ctx, 800, 360, 200, 150, 12)                         # monitor
    rgba(ctx, hexc("#1A2228"))
    ctx.fill()
    pts = []
    for i in range(40):
        x = 815 + i * 4.3
        ph = (i / 40 * 3 - t * 1.4) % 1
        y = 440 - (60 if ph < 0.05 else (-25 if ph < 0.09 else 0))
        pts.append((x, y))
    line(ctx, pts, hexc("#3AFF8A"), 4)
    line(ctx, [(900, 510), (900, FEET - 20)], hexc("#8A969C"), 8)
    line(ctx, [(960, 300), (960, FEET - 20)], hexc("#A8B2B8"), 6)                      # IV stand
    rrect(ctx, 930, 300, 60, 90, 14)
    rgba(ctx, hexc("#E8F4FF"), 0.8)
    ctx.fill()
    mahadev_photo(ctx, 560, 380, t, s=0.7, lit=0.8)
    ctx.rectangle(-80, GROUND - 30, W + 160, H)
    rgba(ctx, hexc("#6E7E7A"))
    ctx.fill()


def hospital_bed(ctx, x, y, w=620):
    rrect(ctx, x - w / 2, y - 210, w, 70, 16)                  # mattress
    rgba(ctx, hexc("#EEF2F4"))
    ctx.fill()
    rrect(ctx, x - w / 2, y - 150, w, 24, 6)
    rgba(ctx, hexc("#8A969C"))
    ctx.fill()
    for side in (-1, 1):
        line(ctx, [(x + side * (w / 2 - 20), y - 140), (x + side * (w / 2 - 20), y)], hexc("#7A868C"), 10)
    line(ctx, [(x - w / 2 + 10, y - 300), (x - w / 2 + 10, y - 150)], hexc("#7A868C"), 12)


def maa_lying(ctx, x, y, t, mood="sad", tilak=0.0, a=1.0):
    """Maa lying on the bed (head to the left), a sheet over her up to the shoulders; tilak 0..1 = bhabhuti lines."""
    ctx.save()                                                 # x, y = her feet; she lies with her head to the left
    ctx.translate(x, y)
    ctx.rotate(-math.pi / 2)
    maa(ctx, 0, 0, 0.6, t, mood=mood, a=a)
    ctx.restore()
    smooth(ctx, [(x - 330, y - 70), (x + 20, y - 60), (x + 30, y + 60), (x - 330, y + 60)], k=0.15)
    ink(ctx, hexc("#8AB8D8"), 3)                               # sheet up to the shoulders
    if tilak > 0:                                              # tripundra on the forehead
        hx, hy = x - 0.6 * 735, y
        for k in range(3):
            line(ctx, [(hx - 4 + 10 * k, hy - 28), (hx - 4 + 10 * k, hy + 28)], ASH, 5, tilak)
        glow(ctx, hx + 10, hy, 60, SHIV_BLUE, 0.6 * tilak)


def doctor(ctx, x, s, t, mood="sad", flip=False, a=1.0, shake=0.0):
    """The doctor: the papa rig in a white coat, with a stethoscope."""
    keep = dm.PAPA_KURTA
    dm.PAPA_KURTA = WHITE_COAT
    try:
        dx = 10 * shake * math.sin(t * 9)
        dm.papa(ctx, x + dx, FEET, s, t, pose="stand", mood=mood, flip=flip, a=a)
    finally:
        dm.PAPA_KURTA = keep
    sx = x + dx
    smooth(ctx, [(sx - 70 * s, FEET - 600 * s), (sx - 60 * s, FEET - 470 * s), (sx, FEET - 430 * s),
                 (sx + 60 * s, FEET - 470 * s), (sx + 70 * s, FEET - 600 * s)], k=0.2)
    ctx.set_source_rgba(0.15, 0.2, 0.25, a)
    ctx.set_line_width(7)
    ctx.stroke()
    circle(ctx, sx, FEET - 425 * s, 14 * s, hexc("#B8C2C8"), a)


def medicine(ctx, x, y, a=1.0):
    """A white medicine box with a green cross and a strip of tablets."""
    rrect(ctx, x - 70, y - 50, 140, 100, 10)
    rgba(ctx, hexc("#F4F6F8"), a)
    ctx.fill()
    rrect(ctx, x - 12, y - 34, 24, 68, 4)
    rgba(ctx, hexc("#2AA85A"), a)
    ctx.fill()
    rrect(ctx, x - 34, y - 12, 68, 24, 4)
    rgba(ctx, hexc("#2AA85A"), a)
    ctx.fill()
    rrect(ctx, x - 60, y + 60, 120, 40, 8)
    rgba(ctx, hexc("#C8D0D8"), a)
    ctx.fill()
    for k in range(4):
        circle(ctx, x - 40 + 27 * k, y + 80, 9, hexc("#FFFFFF"), a)


def shiv_form(ctx, x, s, t, a, pose="bless"):
    if a <= 0:
        return
    glow(ctx, x, FEET - 520 * s, 460 * s, SHIV_BLUE, 0.45 * a)
    mahadev(ctx, x, FEET, s, t, pose=pose, a=a)


# =============================================================================
# Story: 9 lines = 9 scenes, single narrator, no commas or pause signs (same text as kiki_narrator.txt)
# =============================================================================
SPEC = [
    {"key": "umeed", "text": "", "visual": "Night corridor outside the ICU: the doctor shakes his head at the son; on "
                                           "'Mahadev' a faint blue form of Mahadev appears in the ICU door's glow",
     "vo": [("punch", [("डॉक्टर ने उम्मीद", "DOCTOR NE UMEED"), ("छोड़ दी थी,", "CHHOD DI THI"),
                       ("पर उस रात महादेव", "PAR US RAAT MAHADEV"), ("खुद अस्पताल में थे...", "KHUD ASPATAAL MEIN THE.")],
             0.04)]},
    {"key": "raaz", "text": "", "visual": "The doctor turns and freezes - he sees the blue light at the door; the son, head "
                                          "down, does not",
     "vo": [("low", [("और ये बात", "AUR YE BAAT"), ("सिर्फ डॉक्टर को", "SIRF DOCTOR KO"), ("पता चली।", "PATA CHALI.")],
             0.04)]},
    {"key": "pukaar", "text": "", "visual": "Hospital stairs at night: the son sits on a step, hands folded, rudraksh on his "
                                            "wrist glowing faintly; moon through the window",
     "vo": [("low", [("बेटा सीढ़ियों पर बैठा,", "BETA SEEDHIYON PAR BAITHA"), ("महादेव को", "MAHADEV KO"),
                     ("पुकारता रहा।", "PUKAARTA RAHA.")], 0.04)]},
    {"key": "intezaam", "text": "", "visual": "Effort montage in the corridor: he talks on the phone, a medicine box, cash notes, "
                                              "the wall clock's hands race; the diya keeps burning",
     "vo": [("build", [("फिर रात भर", "PHIR RAAT BHAR"), ("दवा और पैसों का", "DAWA AUR PAISON KA"),
                       ("इंतज़ाम किया।", "INTEZAAM KIYA.")], 0.04)]},
    {"key": "bhabhuti", "text": "", "visual": "Morning ICU bay: Maa lies on the bed; he puts a bhabhuti tilak on her "
                                              "forehead - three white lines glow soft blue; Mahadev photo by the bed",
     "vo": [("tell", [("सुबह उसने", "SUBAH USNE"), ("मां के माथे पर", "MAA KE MAATHE PAR"),
                      ("भभूत का तिलक लगाया।", "BHABHOOT KA TILAK LAGAAYA.")], 0.04)]},
    {"key": "operation", "text": "", "visual": "The OT door's red lamp burns; the clock spins through hours; he waits with "
                                               "folded hands; a blue glow behind the door",
     "vo": [("build", [("ऑपरेशन", "OPERATION"), ("छह घंटे चला...", "CHHAH GHANTE CHALA.")], 0.04)]},
    {"key": "safal", "text": "", "visual": "The red lamp goes off; the doctor walks out tired and smiles; the son's face "
                                           "breaks into joy",
     "vo": [("tell", [("डॉक्टर बाहर आए", "DOCTOR BAAHAR AAYE"), ("और बोले,", "AUR BOLE"),
                      ("ऑपरेशन सफल रहा।", "OPERATION SAFAL RAHA.")], 0.04)]},
    {"key": "haath", "text": "", "visual": "Payoff: the doctor looks at his own hand; behind him Mahadev's blue form, his "
                                           "hand on the doctor's hand",
     "vo": [("awe", [("पर अंदर", "PAR ANDAR"), ("कोई और भी,", "KOI AUR BHI"), ("मेरा हाथ थामे", "MERA HAATH THAAME"),
                     ("खड़ा था।", "KHADA THA.")], 0.04)]},
    {"key": "har", "text": "", "visual": "Mahadev's form glows and blesses; the son folds his hands by the corridor mandir; "
                                         "last frame on Mahadev's smile, fades into the hook",
     "vo": [("punch", [("जो मानता है,", "JO MAANTA HAI"), ("वो लिखे", "WO LIKHE"), ("हर हर महादेव।", "HAR HAR MAHADEV.")],
             0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "DOCTOR": hexc("#9AD0FF"), "UMEED": hexc("#FF5A5A"), "MAHADEV": SHIV_BLUE, "KHUD": GOLD_HI, "SIRF": GOLD_HI,
    "SEEDHIYON": hexc("#9AD0FF"), "PUKAARTA": SHIV_BLUE, "DAWA": hexc("#9AD0FF"), "PAISON": hexc("#9BE07A"),
    "INTEZAAM": hexc("#9BE07A"), "BHABHOOT": hexc("#F4F4F4"), "TILAK": GOLD_HI, "CHHAH": hexc("#FFB347"),
    "GHANTE": hexc("#FFB347"), "SAFAL": hexc("#9BE07A"), "HAATH": SHIV_BLUE, "THAAME": SHIV_BLUE, "HAR": SHIV_BLUE,
    "MAHADEV.": SHIV_BLUE,
})


# =============================================================================
# Scenes
# =============================================================================
class Umeed(Cued):
    def beats(self, d):
        return {"mahadev": self.cue("MAHADEV", d * 0.55)}

    def events(self, d):
        return [(self.beats(d)["mahadev"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        corridor(ctx, t)
        form = clamp((t - b["mahadev"]) / 0.6)
        shiv_form(ctx, DOOR_X, 0.62, t, 0.35 * form)
        doctor(ctx, 640, S, t, mood="sad", flip=True, shake=1.0 if t < b["mahadev"] else 0.0)
        boy(ctx, 280, FEET, S, t, pose="drop", mood="cry", look=(0.7, -0.2))


class Raaz(Cued):
    def beats(self, d):
        return {"doctor": self.cue("DOCTOR", d * 0.3)}

    def events(self, d):
        return [(self.beats(d)["doctor"], "zap")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        corridor(ctx, t)
        see = clamp((t - b["doctor"] + 0.2) / 0.4)
        shiv_form(ctx, DOOR_X, 0.62, t, 0.35 + 0.25 * see)
        doctor(ctx, 560, S, t, mood="neutral", flip=see < 0.5)
        if see > 0:
            glow(ctx, 560, FEET - 700 * S, 80, SHIV_BLUE, 0.4 * see)
        boy(ctx, 240, FEET, S, t, pose="tired", mood="cry", look=(0.0, 0.8))


class Pukaar(Cued):
    def beats(self, d):
        return {"mahadev": self.cue("MAHADEV", d * 0.45)}

    def events(self, d):
        return [(self.beats(d)["mahadev"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        stairs(ctx, t)
        g = clamp((t - b["mahadev"]) / 0.5)
        bx, by = 520, FEET + 50                     # sitting on the bottom step (top at FEET - 60), feet on the floor
        hip = by + 150 * S - 335 * S
        for side in (-1, 1):                        # legs: thigh forward over the step edge, shin down to the floor
            dv.limb(ctx, [(bx + side * 36 * S, hip), (bx + side * 48 * S, FEET - 40), (bx + side * 50 * S, FEET - 12)],
                    dm.JEANS, 48 * S)
            ell(ctx, bx + side * 58 * S, FEET - 6, 44 * S, 17 * S)
            ink(ctx, hexc("#F0F0F0"))
        boy(ctx, bx, by, S, t, pose="namaste", mood="cry", look=(0.3, -0.6), seated=True)
        rudraksh(ctx, bx, by + 150 * S - 470 * S, t, glow_a=0.2 + 0.5 * g)
        glow(ctx, 900, 900, 300, SHIV_BLUE, 0.12 + 0.18 * g)
        mahadev_photo(ctx, 880, 820, t, s=0.55, lit=0.4 + 0.6 * g)


class Intezaam(Cued):
    def beats(self, d):
        return {"khoon": self.cue("DAWA", d * 0.4), "paise": self.cue("PAISON", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["khoon"], "tick"), (b["paise"], "kaching")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        corridor(ctx, t, night=0.8)
        clock(ctx, 520, 420, t * 6)
        hand = (t * 3) % math.tau
        line(ctx, [(520, 420), (520 + 40 * math.sin(hand), 420 - 40 * math.cos(hand))], hexc("#C8202A"), 4)
        walk = 260 + 140 * math.sin(t * 1.6)
        boy(ctx, walk, FEET, S, t, pose="phone", mood="neutral", look=(0.6, 0.2))
        medicine(ctx, 900, 840, a=clamp((t - b["khoon"]) / 0.3))
        notes(ctx, 880, 1020, 4, a=clamp((t - b["paise"]) / 0.3))


class Bhabhuti(Cued):
    def beats(self, d):
        return {"tilak": self.cue("TILAK", d * 0.75)}

    def events(self, d):
        return [(self.beats(d)["tilak"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        icu_room(ctx, t)
        tl = clamp((t - b["tilak"] + 0.2) / 0.5)
        boy(ctx, 560, FEET - 40, S, t, pose="offer", mood="cry", look=(-0.8, 0.4), flip=True)
        hospital_bed(ctx, 560, FEET)
        maa_lying(ctx, 840, FEET - 270, t, mood="sad", tilak=tl)
        if tl > 0:
            sparkle_burst(ctx, 840 - 0.6 * 735, FEET - 270, tl, c=SHIV_BLUE, n=10, r=120)


class Operation(Cued):
    def beats(self, d):
        return {"chhah": self.cue("CHHAH", d * 0.4)}

    def events(self, d):
        return [(0.1, "tick"), (self.beats(d)["chhah"], "tock")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        corridor(ctx, t, night=0.4, lamp=1.0)
        shiv_form(ctx, DOOR_X, 0.62, t, 0.22 + 0.08 * math.sin(t * 2))
        spin = clamp((t - b["chhah"]) / max(0.4, d - b["chhah"]))
        clock(ctx, 420, 420, t)
        for k, (L, w, sp) in enumerate(((40, 6, 2.0), (30, 8, 0.4))):
            ang = (t * sp * (1 + 10 * spin)) % math.tau
            line(ctx, [(420, 420), (420 + L * math.sin(ang), 420 - L * math.cos(ang))], hexc("#2A1A10"), w)
        boy(ctx, 330, FEET, S, t, pose="namaste", mood="low", look=(0.9, -0.3))


class Safal(Cued):
    def beats(self, d):
        return {"safal": self.cue("SAFAL", d * 0.75)}

    def events(self, d):
        return [(0.2, "soft_thud"), (self.beats(d)["safal"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        joy = clamp((t - b["safal"]) / 0.4)
        corridor(ctx, t, night=0.3, lamp=0.0)
        walk = ease_out_cubic(clamp(t / 1.0))
        doctor(ctx, lerp(DOOR_X, 660, walk), S, t, mood="neutral", flip=True)
        boy(ctx, 280, FEET, S, t, pose="joy" if joy > 0.5 else "namaste", mood="joy" if joy > 0.3 else "shock",
            look=(0.8, -0.2))
        if joy > 0:
            dv.petals(ctx, t, n=14, seed=3, a=0.7 * joy)


class Haath(Cued):
    def beats(self, d):
        return {"haath": self.cue("HAATH", d * 0.55)}

    def events(self, d):
        return [(0.15, "shimmer"), (self.beats(d)["haath"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        corridor(ctx, t, night=0.6, lamp=0.0)
        rgba(ctx, hexc("#0A1430"), 0.35)
        ctx.paint()
        appear = ease_out_cubic(clamp((t - 0.1) / 0.8))
        hold = clamp((t - b["haath"] + 0.2) / 0.5)
        shiv_form(ctx, 690, 0.74, t, 0.85 * appear, pose="catch_hand" if hold > 0 else "bless")
        doctor(ctx, 460, S, t, mood="neutral", flip=False)
        hx, hy = 460 + 150 * S, FEET - 320 * S
        if hold > 0:
            glow(ctx, hx, hy, 120, SHIV_BLUE, 0.8 * hold)
            sparkle_burst(ctx, hx, hy, hold, c=SHIV_BLUE, n=12, r=150)


class Har(Cued):
    def beats(self, d):
        return {"har": self.cue("HAR", d * 0.6)}

    def events(self, d):
        return [(0.1, "ghanti")]

    def draw(self, ctx, t, d):
        corridor(ctx, t, night=0.2, lamp=0.0)
        rise = ease_out_cubic(clamp(t / 0.9))
        shiv_form(ctx, 720, 0.76, t, 0.95 * rise, pose="bless")
        dv.petals(ctx, t, n=24, seed=8, a=0.85)
        boy(ctx, 300, FEET, S, t, pose="namaste", mood="joy", look=(0.9, -0.5))
        x = clamp((t - (d - 0.45)) / 0.45)                                     # loop into the hook's frame 0
        if x > 0:
            ctx.push_group()
            Umeed().draw(ctx, 0.0, d)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(x)


SCENE_CLASSES = {"umeed": Umeed, "raaz": Raaz, "pukaar": Pukaar, "intezaam": Intezaam, "bhabhuti": Bhabhuti,
                 "operation": Operation, "safal": Safal, "haath": Haath, "har": Har}

UPLOAD = {
    "titles": [
        "Doctor Ne Umeed Chhod Di... Par Us Raat Mahadev Khud Aaye #shorts",
        "6 Ghante Ka Operation... Aur Doctor Ka Haath Kisne Thama? #shorts",
        "ICU Ke Bahar Wo Raat Bhar Mahadev Ko Pukarta Raha #shorts",
    ],
    "thumb_text": "HAATH KISNE THAMA",
    "queries": [
        "mahadev ki kahani",
        "maa ki kahani",
        "emotional story hindi",
    ],
    "description": """
Doctor ne umeed chhod di thi... par us raat Mahadev khud aspataal mein the. ICU ke bahar beta raat bhar Mahadev ko
pukarta raha - phir khud daud kar khoon aur paison ka intezaam kiya. Operation doctor ne kiya, mehnat bete ne ki...
aur saath kaun tha? Har Har Mahadev.

Kalpanik prerak katha. Bimari mein hamesha doctor ki salah aur ilaaj lein - bhakti himmat deti hai, ilaaj ki jagah
nahi leti.

Aapke ghar mein koi beemar hai? Comment mein naam likho - hum sab milke Mahadev se unke liye prarthana karenge.
""",
    "tags": [
        "mahadev ki kahani", "har har mahadev", "bholenath", "shiv ji", "maa ki kahani", "emotional story hindi",
        "icu", "operation", "bhabhuti", "mahadev bhakt", "divya rahasya", "karm aur kripa", "prerak katha", "shorts",
    ],
    "hashtags": ["#Shorts", "#HarHarMahadev", "#Mahadev"],
    "pinned_comment": "Aapke ghar mein koi beemar hai? 🙏 Neeche unka naam likho - hum sab milke Mahadev se unke liye "
                      "prarthana karenge. Ilaaj doctor karein, himmat Bholenath dein. HAR HAR MAHADEV likh ke jaana.",
}


def thumbnail(ctx):
    corridor(ctx, 0.5, night=0.6)
    rgba(ctx, hexc("#0A1430"), 0.3)
    ctx.paint()
    shiv_form(ctx, 690, 0.74, 0.5, 0.9, pose="catch_hand")
    doctor(ctx, 460, S, 0.5, mood="neutral")
    glow(ctx, 460 + 150 * S, FEET - 320 * S, 130, SHIV_BLUE, 0.85)
    text(ctx, "HAATH KISNE", 540, 1330, 116, hexc("#FFFFFF"), font=CAPTION_FONT, bold=False,
         stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "THAMA?", 540, 1470, 140, SHIV_BLUE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
