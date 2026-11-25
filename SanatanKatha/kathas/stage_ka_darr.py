"""Stage Ka Darr (Karm Aur Kripa #4): a girl who froze on stage and was laughed at practises every day before the
mirror; when her name is called again her hands shake, she closes her eyes and says "Jai Hanuman", speaks without a
single stumble - and on the hall window a monkey stands with folded hands as Hanuman ji's golden form rises behind
her (~28 s, 8 scenes). Kalpanik prerak katha.

Usage (from SanatanKatha/):
  python make.py stage_ka_darr --preview
  python make.py stage_ka_darr --kiki-split --check-voice
  python make.py stage_ka_darr --engine files

Hanuman ji in every scene (golden form, his picture in the hall and at home with a diya, the monkey sign, the final
blessing). Mehnat is hers (a month of mirror practice); faith gives her the courage to start.
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
from core.devta import smooth, ink, ell, limb, hand, eye, place, group, shade

from kathas.daadi_morpankh import room_bg, GOLDEN, FEET
from kathas.eklavya_krishna import sparkle_burst, edge_glow
from kathas import panchmukhi as pm
from longform.rickshaw_bharosa import gudiya

TOPIC = "KARM AUR KRIPA STAGE KA DARR HAKLAHAT LADKI HANUMAN JI BANDAR"
OUTPUTS = {"edge": "stage_ka_darr_short.mp4"}
MUSIC_STYLE = "tension"   # nervous build; maa_kangan pulse 82, papa_karz ambient 90
MUSIC_BPM = 96            # >= 6 BPM away from 82
MUSIC_VOLUME = 0.11
TAIL_PAD = 0.22           # calm storytelling breath (user, 23 Nov)
MAX_GAP = 0.25
SCENE_WHOOSH = False      # user, 25 Nov: too many tuni/whoosh/tan sounds - no whoosh on cuts
SFX_SCALE = 0.5           # and the few SFX left at half level

SAFF = hexc("#FF8C1A")
SOURCES = [
    "Original fictional story (Kalpanik prerak katha) - no scripture or real-event claim; labelled in the description.",
    "Hanuman ji's form (sindoori, golden mukut, gada, abhaya/namaste) follows common iconography; the monkey as his "
    "sign is a popular bhakti motif, shown respectfully (folded hands, no comedy).",
]


# =============================================================================
# Places and props
# =============================================================================
def hanuman_photo(ctx, x, y, t, s=1.0, lit=0.6):
    glow(ctx, x, y, 150 * s, GOLDEN, 0.35 * lit + 0.05 * math.sin(t * 2))
    rrect(ctx, x - 80 * s, y - 100 * s, 160 * s, 200 * s, 8)
    ink(ctx, hexc("#7A4A1E"), 4)
    ctx.save()
    ctx.rectangle(x - 70 * s, y - 90 * s, 140 * s, 180 * s)
    ctx.clip()
    rgba(ctx, hexc("#FFD08A"))
    ctx.paint()
    pm.hanuman(ctx, x, y + 260 * s, 0.3 * s, t, pose="abhaya", aura=False)
    ctx.restore()
    for k in range(9):
        ang = math.pi * (k / 8)
        circle(ctx, x + 84 * s * math.cos(ang), y - 108 * s + 70 * s * math.sin(ang) * 0.5, 8 * s,
               hexc("#FF8A1E") if k % 2 else hexc("#FFC21E"))


def hall_bg(ctx, t, lights=1.0, window=True, red=0.0):
    """School hall: warm back wall, a blank banner, a wooden stage with red curtains, a window at top-right,
    Hanuman ji's picture on the side wall, a spotlight cone."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in ((0.0, "#3A2A3A"), (0.5, "#5A3A3A"), (0.62, "#3A2420"), (1.0, "#1A1010")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.rectangle(-80, -80, W + 160, H + 160)
    ctx.fill()
    rrect(ctx, 260, 330, 560, 110, 12)                                    # blank banner (no text)
    rgba(ctx, hexc("#2E5A8A"))
    ctx.fill()
    for k in range(7):
        circle(ctx, 300 + 80 * k, 330, 12, hexc("#FFC21E") if k % 2 else hexc("#FF5A5A"))
    if window:
        rrect(ctx, 830, 230, 230, 250, 6)
        rgba(ctx, hexc("#7FB8E8"))
        ctx.fill()
        rrect(ctx, 830, 230, 230, 250, 6)
        rgba(ctx, hexc("#5A3A22"))
        ctx.set_line_width(12)
        ctx.stroke()
        line(ctx, [(945, 230), (945, 480)], hexc("#5A3A22"), 8)
        line(ctx, [(820, 480), (1070, 480)], hexc("#6A4428"), 18)        # sill
    hanuman_photo(ctx, 195, 310, t, s=0.66, lit=0.8)
    for side in (-1, 1):                                                   # curtains
        x0 = -80 if side < 0 else W + 80
        x1 = 120 if side < 0 else W - 120
        smooth(ctx, [(x0, 160), (x1, 160), (x1 + 40 * side, 700), (x1 - 20 * side, FEET), (x0, FEET)], k=0.1)
        rgba(ctx, hexc("#8A1A2A"))
        ctx.fill()
        for k in range(4):
            line(ctx, [(x0 + (x1 - x0) * (k + 1) / 5, 170), (x0 + (x1 - x0) * (k + 1) / 5, FEET)],
                 hexc("#6A1220"), 4, 0.7)
    rrect(ctx, -80, 120, W + 160, 60, 0)                                  # valance
    rgba(ctx, hexc("#A01E30"))
    ctx.fill()
    ctx.rectangle(-80, FEET - 20, W + 160, H)                             # stage floor
    rgba(ctx, hexc("#7A4A2A"))
    ctx.fill()
    for k in range(9):
        line(ctx, [(-80 + 150 * k, FEET - 20), (-80 + 150 * k, FEET + 110)], hexc("#5A3420"), 3, 0.6)
    ctx.rectangle(-80, FEET + 110, W + 160, H)                            # stage edge / dark pit
    rgba(ctx, hexc("#140C0A"))
    ctx.fill()
    if lights > 0:                                                         # spotlight cone
        ctx.move_to(440, -40)
        ctx.line_to(640, -40)
        ctx.line_to(760, FEET)
        ctx.line_to(320, FEET)
        ctx.close_path()
        rgba(ctx, hexc("#FFF2C8"), 0.12 * lights)
        ctx.fill()
        ell(ctx, 540, FEET - 4, 230, 30)
        rgba(ctx, hexc("#FFF2C8"), 0.25 * lights)
        ctx.fill()
    if red > 0:
        rgba(ctx, hexc("#C0101A"), 0.22 * red)
        ctx.paint()


def mic(ctx, x, y, t, rings=0.0):
    line(ctx, [(x, y), (x, y - 430)], hexc("#2A2A30"), 10)
    ell(ctx, x, y - 4, 70, 14)
    rgba(ctx, hexc("#2A2A30"))
    ctx.fill()
    line(ctx, [(x, y - 430), (x - 40, y - 470)], hexc("#2A2A30"), 8)
    rrect(ctx, x - 66, y - 500, 40, 60, 18)
    ink(ctx, hexc("#4A4A55"), 2)
    if rings > 0:                                                          # her voice: rings from the mic
        for i in range(4):
            u = (t * 0.9 + i / 4) % 1
            ctx.arc(x - 46, y - 470, 40 + 260 * u, -0.7, 0.7)
            rgba(ctx, GOLD_HI, rings * 0.7 * (1 - u))
            ctx.set_line_width(6)
            ctx.stroke()


def audience(ctx, t, laugh=0.0, clap=0.0, a=1.0, y=1150, xs=(50, 640, 760, 880, 1010)):
    """Front-row heads in silhouette at the screen edges, clear of the girl and the subtitles (bob when they laugh or clap)."""
    for i, x in enumerate(xs):
        bob = 10 * (laugh + clap) * abs(math.sin(t * 9 + i * 1.3))
        yy = y - bob
        ell(ctx, x, yy + 70, 70, 60)
        rgba(ctx, hexc("#120A10"), a)
        ctx.fill()
        circle(ctx, x, yy, 42, hexc("#1E1418"), a)
        if laugh > 0:
            ell(ctx, x + 10, yy + 12, 12, 7 * (0.5 + 0.5 * abs(math.sin(t * 9 + i))))
            rgba(ctx, hexc("#7A5A6A"), 0.7 * laugh * a)
            ctx.fill()
        if clap > 0:                                                       # hands meeting above the head
            gap = 16 + 16 * math.sin(t * 16 + i)
            for side in (-1, 1):
                circle(ctx, x + side * gap, yy - 70, 14, hexc("#3A2A2A"), a * clap)


def monkey(ctx, x, y, s, t, namaste=1.0, a=1.0):
    """A small brown monkey sitting on the window sill, hands folded (Hanuman ji's sign - respectful, no comedy)."""
    def draw():
        place(ctx, x, y, s, t, False)
        fur, face = hexc("#8A5A34"), hexc("#E8B48A")
        smooth(ctx, [(-120, 0), (120, 0), (100, -200), (60, -280), (-60, -280), (-100, -200)], k=0.15)
        ink(ctx, fur, 3)                                                   # body sitting
        ctx.move_to(110, -20)                                              # tail curling up
        ctx.curve_to(260, -20, 260, -260, 170, -300)
        rgba(ctx, fur)
        ctx.set_line_width(22)
        ctx.stroke()
        for side in (-1, 1):                                               # folded hands at the chest
            limb(ctx, [(side * 80, -240), (side * 70, -170), (side * 12 * namaste + side * 50 * (1 - namaste), -190)],
                 fur, 30)
        smooth(ctx, [(0, -230), (14, -200), (12, -160), (0, -150), (-12, -160), (-14, -200)])
        ink(ctx, face)
        circle(ctx, 0, -360, 100, fur)                                     # head
        for side in (-1, 1):
            circle(ctx, side * 98, -360, 30, face)
        ell(ctx, 0, -345, 72, 66)
        ink(ctx, face)
        for side in (-1, 1):
            eye(ctx, side * 26, -370, 13, 16, t, seed=71, iris=hexc("#2A1A10"), skin=face, lid=0.35)
        ctx.arc(0, -320, 20, 0.2 * math.pi, 0.8 * math.pi)
        rgba(ctx, hexc("#6A2A1A"))
        ctx.set_line_width(5)
        ctx.stroke()
        line(ctx, [(0, -420), (0, -400)], hexc("#E8501E"), 8)              # a touch of sindoor
        ctx.restore()
    group(ctx, a, draw)


def mirror(ctx, x, y, t, girl_pose="talk", mood="neutral"):
    rrect(ctx, x - 150, y - 260, 300, 420, 140)
    ink(ctx, hexc("#C8A060"), 8)
    ctx.save()
    rrect(ctx, x - 136, y - 246, 272, 392, 130)
    ctx.clip()
    g = cairo.LinearGradient(x - 136, y - 246, x + 136, y + 146)
    g.add_color_stop_rgb(0, *hexc("#BFE4F4"))
    g.add_color_stop_rgb(1, *hexc("#7AA8C8"))
    ctx.set_source(g)
    ctx.paint()
    gudiya(ctx, x, y + 420, 0.5, t, pose=girl_pose, mood=mood, look=(0.6, 0.0), flip=True)
    line(ctx, [(x - 100, y - 200), (x - 40, y - 240)], (1, 1, 1), 8, 0.5)
    ctx.restore()


def altar_hanuman(ctx, x, y, t, lit=1.0):
    glow(ctx, x, y - 90, 150, GOLDEN, 0.35 * lit + 0.05 * math.sin(t * 2))
    rrect(ctx, x - 90, y, 180, 18, 4)
    ink(ctx, hexc("#7A4A1E"), 3)
    smooth(ctx, [(x - 80, y), (x - 80, y - 150), (x, y - 200), (x + 80, y - 150), (x + 80, y)], k=0.05)
    rgba(ctx, hexc("#5A2A1E"), 0.85)
    ctx.fill()
    pm.hanuman(ctx, x, y - 4, 0.2, t, pose="abhaya", aura=False)
    dv.diya(ctx, x + 60, y - 6, 0.45, t, a=1.0)


def hanuman_light(ctx, x, s, t, a=0.5, pose="abhaya"):
    if a <= 0:
        return
    glow(ctx, x, FEET - 520 * s, 440 * s, GOLDEN, 0.5 * a)
    pm.hanuman(ctx, x, FEET, s, t, pose=pose, a=a)


# =============================================================================
# Story: 8 scenes, single narrator, no commas or pause signs
# =============================================================================
SPEC = [
    {"key": "peeche", "text": "", "visual": "Hall stage: the girl at the mic in a spotlight; Hanuman ji's golden form "
                                            "stands behind her; the front row in silhouette",
     "vo": [("punch", [("जो लड़की बोलते हुए", "JO LADKI BOLTE HUE"), ("अटकती थी", "ATAKTI THI"),
                       ("उसके पीछे खुद", "USKE PEECHHE KHUD"), ("हनुमान जी खड़े थे।", "HANUMAN JI KHADE THE.")], 0.04)]},
    {"key": "hanse", "text": "", "visual": "Flashback, red tint: she freezes at the mic, the front row bobs with laughter",
     "vo": [("low", [("पिछली बार स्टेज पर", "PICHHLI BAAR STAGE PAR"), ("वो अटकी", "WO ATKI"),
                     ("तो सब हंस पड़े।", "TO SAB HANS PADE.")], 0.04)]},
    {"key": "abhyas", "text": "", "visual": "Her room: she speaks to her reflection in the mirror, days and nights flick "
                                            "past; Hanuman ji's little altar glows with a diya",
     "vo": [("build", [("पर उसने रोज़", "PAR USNE ROZ"), ("आईने के सामने", "AAINE KE SAAMNE"),
                       ("अभ्यास किया।", "ABHYAAS KIYA.")], 0.04)]},
    {"key": "pukara", "text": "", "visual": "Hall again: she walks into the spotlight to the mic; her hands tremble",
     "vo": [("tell", [("आज फिर नाम पुकारा गया", "AAJ PHIR NAAM PUKAARA GAYA"),
                      ("तो हाथ कांपने लगे।", "TO HAATH KAANPNE LAGE.")], 0.04)]},
    {"key": "jai", "text": "", "visual": "Close: eyes closed, hands folded at the mic; a soft golden glow rises around "
                                         "her",
     "vo": [("whisper", [("उसने आंखें बंद कीं", "USNE AANKHEN BAND KEEN"), ("और बोली", "AUR BOLI"),
                         ("जय हनुमान।", "JAI HANUMAN.")], 0.04)]},
    {"key": "bola", "text": "", "visual": "She speaks with an open hand; golden rings flow from the mic; the front row "
                                          "is still and listening",
     "vo": [("build", [("फिर बोलना शुरू किया", "PHIR BOLNA SHURU KIYA"), ("और एक शब्द", "AUR EK SHABD"),
                       ("नहीं अटका।", "NAHI ATKA.")], 0.04)]},
    {"key": "taali", "text": "", "visual": "The whole front row claps, petals fall, she lifts both arms in joy",
     "vo": [("punch", [("पूरा हॉल", "POORA HALL"), ("तालियों से गूंज उठा।", "TAALIYON SE GOONJ UTHA.")], 0.04)]},
    {"key": "bandar", "text": "", "visual": "On the window sill a monkey stands with folded hands; it glows and Hanuman ji's "
                                            "golden form rises behind her, blessing; last frame on his smile",
     "vo": [("awe", [("तभी खिड़की पर बैठा", "TABHI KHIDKI PAR BAITHA"), ("एक बंदर भी", "EK BANDAR BHI"),
                     ("हाथ जोड़े खड़ा था।", "HAATH JODE KHADA THA.")], 0.04),
            ("punch", [("जो मानता है", "JO MAANTA HAI"), ("वो लिखे", "WO LIKHE"), ("जय बजरंगबली।", "JAI BAJRANGBALI.")],
             0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "ATAKTI": hexc("#FF5A5A"), "HANUMAN": SAFF, "STAGE": hexc("#FFB347"), "ATKI": hexc("#FF5A5A"),
    "HANS": hexc("#FF5A5A"), "ROZ": GOLD_HI, "AAINE": hexc("#9AD8FF"), "ABHYAAS": GOLD_HI, "NAAM": hexc("#FFB347"),
    "KAANPNE": hexc("#FF5A5A"), "AANKHEN": hexc("#9AD8FF"), "JAI": SAFF, "SHABD": GOLD_HI, "NAHI": hexc("#9BE07A"),
    "TAALIYON": GOLD_HI, "GOONJ": GOLD_HI, "KHIDKI": hexc("#9AD8FF"), "BANDAR": SAFF, "HAATH": GOLD_HI,
    "BAJRANGBALI": SAFF,
})

GX = 330             # the girl's spot at the mic
MIC_X = 470


# =============================================================================
# Scenes
# =============================================================================
class Peeche(Cued):
    def beats(self, d):
        return {"hanuman": self.cue("HANUMAN JI", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["hanuman"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        hall_bg(ctx, t, lights=1.0)
        hanuman_light(ctx, 760, 0.76, t, a=0.45 + 0.35 * clamp((t - b["hanuman"]) / 0.5), pose="abhaya")
        mic(ctx, MIC_X, FEET, t)
        gudiya(ctx, GX, FEET, 0.72, t, pose="stand", mood="shock", look=(0.4, 0.1), shake=0.6)
        audience(ctx, t, xs=(50,))
        edge_glow(ctx, t, d, start=0.0)


class Hanse(Cued):
    def beats(self, d):
        return {"hans": self.cue("HANS", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["hans"], "soft_thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        laugh = clamp((t - b["hans"] + 0.2) / 0.3)
        hall_bg(ctx, t, lights=0.7, red=0.6 + 0.4 * laugh)
        mic(ctx, MIC_X, FEET, t)
        gudiya(ctx, GX, FEET, 0.72, t, pose="cry" if laugh > 0.5 else "stand", mood="cry" if laugh > 0.5 else "shock",
               look=(0.4, 0.2), shake=1.0 - laugh)
        audience(ctx, t, laugh=laugh)


class Abhyas(Cued):
    def beats(self, d):
        return {"aaine": self.cue("AAINE", d * 0.35), "abhyas": self.cue("ABHYAAS", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["aaine"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night = 1.0 if (t > b["abhyas"] and int((t - b["abhyas"]) / 0.45) % 2) else 0.0
        room_bg(ctx, t, night=night, lamp=1.0 if night else 0.0)
        altar_hanuman(ctx, 880, 520, t, lit=1.0)
        mirror(ctx, 760, 820, t, girl_pose="talk", mood="neutral")
        gudiya(ctx, 300, FEET, 0.74, t * (1.6 if t > b["abhyas"] else 1.0), pose="talk", mood="neutral",
               look=(0.8, 0.0))


class Pukara(Cued):
    def beats(self, d):
        return {"haath": self.cue("HAATH", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return []

    def draw(self, ctx, t, d):
        b = self.beats(d)
        hall_bg(ctx, t, lights=clamp(t / 0.4))
        walk = ease_out_cubic(clamp(t / max(0.8, b["haath"] - 0.2)))
        x = lerp(-40, GX, walk)
        mic(ctx, MIC_X, FEET, t)
        shake = clamp((t - b["haath"]) / 0.3)
        gudiya(ctx, x, FEET, 0.72, t, pose="study" if shake > 0 else "stand", mood="shock" if shake > 0 else "neutral",
               look=(0.8, 0.1), shake=2.0 * shake)
        if shake > 0:                                                      # nervous sweat drops
            for i in range(3):
                u = (t * 1.2 + i / 3) % 1
                circle(ctx, x + 60 + 30 * i, FEET - 760 * 0.72 + 80 * u, 8, hexc("#9AD8FF"), 0.9 * (1 - u))
        audience(ctx, t)


class Jai(Cued):
    def beats(self, d):
        return {"jai": self.cue("JAI HANUMAN", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["jai"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        lit = clamp((t - b["jai"]) / 0.5)
        hall_bg(ctx, t, lights=1.0 - 0.5 * lit)
        rgba(ctx, (0, 0, 0), 0.35 * (1 - lit))                            # the world goes quiet
        ctx.paint()
        glow(ctx, GX, FEET - 420, 360, GOLDEN, 0.25 + 0.45 * lit)
        if lit > 0:
            hanuman_light(ctx, 760, 0.76, t, a=0.35 * lit, pose="namaste")
        mic(ctx, MIC_X, FEET, t)
        gudiya(ctx, GX, FEET, 0.72, t, pose="namaste", mood="sleep", shake=1.0 - lit)
        if lit > 0:
            sparkle_burst(ctx, GX, FEET - 600, lit, c=GOLD_HI, n=14, r=220)


class Bola(Cued):
    def beats(self, d):
        return {"nahi": self.cue("NAHI ATKA", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["nahi"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        hall_bg(ctx, t, lights=1.0)
        mic(ctx, MIC_X, FEET, t, rings=1.0)
        gudiya(ctx, GX, FEET, 0.72, t, pose="teach" if t > b["nahi"] else "talk",
               mood="joy" if t > b["nahi"] else "neutral", look=(0.6, 0.1))
        audience(ctx, t)
        if t > b["nahi"]:
            glow(ctx, GX, FEET - 560, 150, GOLDEN, 0.35)


class Taali(Cued):
    def beats(self, d):
        return {"goonj": self.cue("GOONJ", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["goonj"], "dingdong")]

    def draw(self, ctx, t, d):
        hall_bg(ctx, t, lights=1.0)
        dv.petals(ctx, t, n=30, seed=5, a=0.9)
        mic(ctx, MIC_X, FEET, t)
        gudiya(ctx, GX, FEET, 0.72, t, pose="joy", mood="joy", look=(0.6, -0.2))
        audience(ctx, t, clap=1.0)


class Bandar(Cued):
    def beats(self, d):
        return {"bandar": self.cue("BANDAR", d * 0.25), "haath": self.cue("HAATH JODE", d * 0.4),
                "jai": self.cue("JO MAANTA", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["bandar"], "shimmer"), (b["haath"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        hall_bg(ctx, t, lights=1.0)
        mk = clamp((t - b["bandar"] + 0.3) / 0.4)
        nam = clamp((t - b["haath"]) / 0.4)
        glow(ctx, 945, 380, 200, GOLDEN, 0.3 * mk + 0.4 * nam)
        monkey(ctx, 945, 478, 0.5, t, namaste=nam, a=mk)
        rise = ease_out_cubic(clamp((t - b["haath"] - 0.2) / 0.9))
        if rise > 0:
            glow(ctx, 760, FEET - 460, 460, GOLDEN, 0.55 * rise)
            pm.hanuman(ctx, 760, FEET + 60 * (1 - rise), 0.76, t, pose="abhaya" if t >= b["jai"] else "namaste",
                       a=0.9 * rise)
        if t >= b["jai"]:
            dv.petals(ctx, t, n=26, seed=11, a=0.9)
        mic(ctx, MIC_X, FEET, t)
        gudiya(ctx, GX, FEET, 0.72, t, pose="namaste" if t >= b["haath"] else "stand",
               mood="joy" if t >= b["haath"] else "shock", look=(0.9, -0.6))
        audience(ctx, t, clap=0.4, xs=(50,))
        x = clamp((t - (d - 0.45)) / 0.45)                                # loop into the hook's frame 0
        if x > 0:
            ctx.push_group()
            Peeche().draw(ctx, 0.0, d)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(x)


SCENE_CLASSES = {"peeche": Peeche, "hanse": Hanse, "abhyas": Abhyas, "pukara": Pukara, "jai": Jai, "bola": Bola,
                 "taali": Taali, "bandar": Bandar}

UPLOAD = {
    "titles": [
        "Stage Par Atakne Wali Ladki Ke Peeche Khud Hanuman Ji Khade The #shorts",
        "Sab Hanse The... Phir Usne Bola Jai Hanuman #shorts",
        "Khidki Par Baitha Bandar Bhi Haath Jode Khada Tha #shorts",
    ],
    "thumb_text": "PEECHHE HANUMAN JI",
    "queries": [
        "hanuman ji ki kahani",
        "stage fear story hindi",
        "jai bajrangbali story",
    ],
    "description": """
Jo ladki stage par bolte hue atakti thi, uske peeche khud Hanuman ji khade the. Pichhli baar sab hanse the... par
usne roz aaine ke saamne abhyas kiya. Hanuman ji ki kahani - mehnat aur Bajrangbali par bharose ki prerak katha.

Kalpanik prerak katha.

Stage ka darr - mehnat se jaata hai ya bharose se? Comment mein apni raay likho.
""",
    "tags": [
        "hanuman ji ki kahani", "jai bajrangbali", "jai hanuman", "stage fear", "stage ka darr", "bolne mein atakna",
        "motivational story hindi", "student motivation", "bhagwan ki kahani", "divya rahasya", "karm aur kripa",
        "prerak katha", "shorts", "hanuman bhakti",
    ],
    "hashtags": ["#Shorts", "#JaiBajrangbali", "#HanumanJi"],
    "pinned_comment": "Stage ka darr - mehnat se jaata hai ya bharose se? 🤔 Apni raay likho. Aur agar aapka bhi "
                      "koi exam, interview ya speech aane wala hai to likho - hum sab milke Hanuman ji se aapke liye "
                      "prarthana karenge. Jai Bajrangbali 🙏",
}


def thumbnail(ctx):
    hall_bg(ctx, 0.5, lights=1.0)
    hanuman_light(ctx, 760, 0.76, 0.5, a=0.8, pose="abhaya")
    monkey(ctx, 945, 478, 0.5, 0.5, namaste=1.0)
    mic(ctx, MIC_X, FEET, 0.5)
    gudiya(ctx, GX, FEET, 0.72, 0.5, pose="namaste", mood="sleep")
    text(ctx, "PEECHHE KHADE THE", 540, 1330, 100, hexc("#FFFFFF"), font=CAPTION_FONT, bold=False,
         stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "HANUMAN JI", 540, 1470, 130, SAFF, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
