"""Bees Baar Reject: a delivery boy who pours jal on the shivling every morning is rejected twenty times; in the rain
he tells Mahadev "main haarunga nahi", Mahadev gives darshan ("tu mehnat kar, main tere saath hoon"), and the next
interview he clears himself (~42 s, 7 scenes). Kalpanik prerak katha.

Usage (from SanatanKatha/):
  python make.py bees_baar_reject --preview
  python make.py bees_baar_reject --kiki-split --check-voice
  python make.py bees_baar_reject --engine files

Mahadev is present in every scene (shivling, trishul on the bike, photo on the wall, darshan, rudraksh, smile).
Loop: "...kyunki wo tha" -> "roz Shiv ji ko jal chadhane wala wo ladka bees baar reject hua".
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
from core.devta import smooth, ink, ell

from kathas.daadi_morpankh import boy, room_bg, desk, relatives, GOLDEN, FEET
from kathas.ravan import mahadev, shivling
from kathas.eklavya_krishna import sparkle_burst, edge_glow

TOPIC = "BEES BAAR REJECT DELIVERY BOY MAHADEV DARSHAN MEHNAT"
OUTPUTS = {"edge": "bees_baar_reject_short.mp4"}
MUSIC_STYLE = "tension"   # rain + struggle; daadi_morpankh used pulse
MUSIC_BPM = 84            # >= 6 BPM away from daadi_morpankh (76)
MUSIC_VOLUME = 0.11
TAIL_PAD = 0.22           # calm storytelling breath (user, 23 Nov)
MAX_GAP = 0.25

SHIV_BLUE = hexc("#9FD0FF")
SOURCES = [
    "Original fictional story (Kalpanik prerak katha) - no scripture or real-event claim; labelled in the description.",
    "Mahadev's form (jata with crescent and Ganga, trishul, damru, rudraksh, tiger skin) follows common Shaiva "
    "iconography; jal-abhishek on the shivling is a common daily practice.",
]


# =============================================================================
# Scenery
# =============================================================================
def shiv_temple(ctx, t, night=False, rain=0.0, light=0.0):
    """Small Shiv temple: shikhara with a saffron flag, open sanctum with the shivling, bell; dawn or rainy night."""
    g = cairo.LinearGradient(0, 0, 0, H)
    stops = ((0.0, "#0A0E22"), (0.4, "#1E2A4A"), (0.6, "#3A4A6A"), (1.0, "#101420")) if night else \
            ((0.0, "#3A4A8A"), (0.35, "#E89A6A"), (0.55, "#FFD9A0"), (1.0, "#4A3A2A"))
    for at, c in stops:
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.rectangle(-80, -80, W + 160, H + 160)
    ctx.fill()
    if not night:
        dv.sun_disc(ctx, 880, 700, 70, t, a=0.85, rays=14)
    for k, (yy, c) in enumerate(((930, "#2A2A3E" if night else "#7A5A4A"), (1010, "#1A1A2A" if night else "#5A4034"))):
        ctx.move_to(-80, H)
        for x in range(-80, W + 81, 40):
            ctx.line_to(x, yy - 50 * abs(math.sin(x / 170 + k)))
        ctx.line_to(W + 80, H)
        ctx.close_path()
        rgba(ctx, hexc(c))
        ctx.fill()
    smooth(ctx, [(460, 1060), (460, 700), (540, 520), (620, 380), (700, 520), (780, 700), (780, 1060)], k=0.06)
    ink(ctx, hexc("#C8B8A0") if night else hexc("#EED8B8"), 5)
    for k in range(5):
        line(ctx, [(500 + 10 * k, 680 + 70 * k), (740 - 10 * k, 680 + 70 * k)], hexc("#9A8A70"), 4, 0.6)
    line(ctx, [(620, 380), (620, 300)], hexc("#5A3A1E"), 6)
    ctx.move_to(620, 300)
    ctx.line_to(690, 322)
    ctx.line_to(620, 344)
    ctx.close_path()
    ink(ctx, hexc("#FF7A1E"), 3)
    rrect(ctx, 530, 860, 180, 200, 70)                         # sanctum opening
    rgba(ctx, hexc("#FFD27A") if not night else hexc("#4A3A2A"), 0.95)
    ctx.fill()
    if light > 0:
        glow(ctx, 620, 960, 420, SHIV_BLUE, 0.7 * light)
    ctx.rectangle(-80, GROUND - 30, W + 160, H)
    rgba(ctx, hexc("#2A2A34") if night else hexc("#6A5040"))
    ctx.fill()
    for k in range(4):                                         # temple steps
        rrect(ctx, 380 - 20 * k, GROUND - 30 + 16 * k, 480 + 40 * k, 16, 3)
        rgba(ctx, hexc("#4A4A58") if night else hexc("#9A8068"))
        ctx.fill()
    if rain > 0:
        for i in range(90):
            x = (rnd(i, 1) * (W + 200) - t * 260 * 0.4) % (W + 200) - 100
            y = (rnd(i, 2) * H + t * 1400) % H
            line(ctx, [(x, y), (x - 10, y + 46)], hexc("#B8C8E8"), 3, 0.45 * rain)
        for i in range(14):                                    # splashes
            x = rnd(i, 5) * W
            u = (t * 2 + rnd(i, 6)) % 1
            ctx.arc(x, GROUND - 20, 6 + 18 * u, math.pi, math.tau)
            rgba(ctx, hexc("#B8C8E8"), 0.5 * (1 - u) * rain)
            ctx.set_line_width(2)
            ctx.stroke()


def mahadev_photo(ctx, x, y, t, s=1.0, lit=0.6):
    """Framed Mahadev picture on the wall (the hero's faith at home)."""
    glow(ctx, x, y, 150 * s, SHIV_BLUE, 0.35 * lit)
    rrect(ctx, x - 80 * s, y - 100 * s, 160 * s, 200 * s, 8)
    ink(ctx, hexc("#7A4A1E"), 4)
    ctx.save()
    ctx.rectangle(x - 70 * s, y - 90 * s, 140 * s, 180 * s)
    ctx.clip()
    rgba(ctx, hexc("#2A3A6A"))
    ctx.paint()
    mahadev(ctx, x, y + 260 * s, 0.32 * s, t, pose="bless")
    ctx.restore()
    for k in range(9):
        ang = math.pi * (k / 8)
        circle(ctx, x + 84 * s * math.cos(ang), y - 108 * s + 70 * s * math.sin(ang) * 0.5, 8 * s,
               hexc("#FF8A1E") if k % 2 else hexc("#FFC21E"))


def scooter(ctx, x, y, t, a=1.0):
    """Delivery scooter with a box on the back, a small trishul sticker and rudraksh on the handle."""
    wob = 3 * math.sin(t * 14)
    for wx in (x - 150, x + 150):
        circle(ctx, wx, y - 50 + wob * 0.2, 50, hexc("#1A1A1A"))
        circle(ctx, wx, y - 50 + wob * 0.2, 22, hexc("#8A8A8A"))
    smooth(ctx, [(x - 200, y - 90), (x + 40, y - 110), (x + 150, y - 170), (x + 180, y - 100), (x - 190, y - 60)], k=0.1)
    ink(ctx, hexc("#C8202A"), 4)
    line(ctx, [(x + 150, y - 170), (x + 170, y - 300)], hexc("#3A3A3A"), 10)
    line(ctx, [(x + 130, y - 300), (x + 210, y - 300)], hexc("#3A3A3A"), 10)
    for k in range(5):                                          # rudraksh hanging on the handle
        circle(ctx, x + 175, y - 290 + 14 * k, 5, hexc("#6A3A1E"))
    line(ctx, [(x - 60, y - 140), (x - 60, y - 100)], hexc("#FFD27A"), 4)            # small trishul sticker
    for dx in (-10, 0, 10):
        line(ctx, [(x - 60 + dx, y - 150), (x - 60 + dx * 0.6, y - 138)], hexc("#FFD27A"), 3)
    rrect(ctx, x - 250, y - 250, 120, 110, 8)                   # delivery box
    ink(ctx, hexc("#E8A020"), 4)


def interview_room(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc("#D8DCE4"))
    g.add_color_stop_rgb(0.62, *hexc("#AEB4C0"))
    g.add_color_stop_rgb(1, *hexc("#6A707C"))
    ctx.set_source(g)
    ctx.rectangle(-80, -80, W + 160, H + 160)
    ctx.fill()
    for k in range(4):                                          # office windows
        rrect(ctx, 80 + 250 * k, 320, 200, 300, 6)
        rgba(ctx, hexc("#9AC8E8"))
        ctx.fill()
    ctx.rectangle(-80, GROUND - 30, W + 160, H)
    rgba(ctx, hexc("#5A606C"))
    ctx.fill()


def temple_ghanta(ctx, x, y, t, ring=0.0):
    """Big brass temple ghanta on a chain; swings and glows when it rings by itself."""
    sw = 0.45 * ring * math.sin(t * 12)
    ctx.save()
    ctx.translate(x, y - 140)
    for k in range(6):
        ell(ctx, 0, 18 * k, 7, 10)
        rgba(ctx, GOLD_DK)
        ctx.set_line_width(4)
        ctx.stroke()
    ctx.translate(0, 110)
    ctx.rotate(sw)
    if ring > 0:
        glow(ctx, 0, 60, 120, GOLD_HI, 0.5 * ring)
    smooth(ctx, [(-46, 100), (-38, 30), (-18, 0), (18, 0), (38, 30), (46, 100)], k=0.1)
    ink(ctx, GOLD, 4)
    line(ctx, [(-44, 90), (44, 90)], GOLD_DK, 5)
    circle(ctx, 0, 108, 12, GOLD_DK)
    ctx.restore()


def rudraksh(ctx, x, y, t, glow_a=0.0):
    for k in range(9):
        ang = math.pi * (0.15 + 0.7 * k / 8)
        circle(ctx, x + 46 * math.cos(ang), y - 30 + 34 * math.sin(ang), 7, hexc("#6A3A1E"))
    if glow_a > 0:
        glow(ctx, x, y + 6, 70, SHIV_BLUE, glow_a)


# =============================================================================
# Story: 7 scenes, ~105 words (single narrator, no commas or pause signs)
# =============================================================================
SPEC = [
    {"key": "jal", "text": "", "visual": "Dawn temple: he pours jal on the shivling; cut to his phone flashing red",
     "vo": [("punch", [("रोज़ शिव जी को", "ROZ SHIV JI KO"), ("जल चढ़ाने वाला वो लड़का", "JAL CHADHAANE WAALA WO LADKA"),
                       ("बीस बार रिजेक्ट हुआ।", "BEES BAAR REJECT HUA.")], 0.04)]},
    {"key": "sangharsh", "text": "", "visual": "Delivery scooter by day, night study under Mahadev's photo; parents shake their heads",
     "vo": [("tell", [("दिन में डिलीवरी करता", "DIN MEIN DELIVERY KARTA"), ("और रात को पढ़ाई।", "AUR RAAT KO PADHAI.")], 0.02),
            ("low", [("घर वाले बोले", "GHAR WAALE BOLE"), ("छोड़ दे ये सपना।", "CHHOD DE YE SAPNA.")], 0.04)]},
    {"key": "barish", "text": "", "visual": "Rainy night: soaked, he climbs the temple steps and folds his hands before the shivling",
     "vo": [("low", [("उस रात बारिश में", "US RAAT BAARISH MEIN"), ("भीगता हुआ वो मंदिर पहुंचा।", "BHEEGTA HUA WO MANDIR PAHUNCHA.")], 0.02),
            ("low", [("आंखों में आंसू थे", "AANKHON MEIN AANSU THE"), ("पर शिकायत नहीं।", "PAR SHIKAYAT NAHIN.")], 0.02),
            ("build", [("बस इतना बोला", "BAS ITNA BOLA"), ("महादेव मैं हारूंगा नहीं।", "MAHADEV MAIN HAARUNGA NAHIN.")], 0.04)]},
    {"key": "darshan", "text": "", "visual": "The bell swings by itself, light bursts from the shivling, Mahadev appears in full glory",
     "vo": [("whisper", [("तभी मंदिर की घंटी", "TABHI MANDIR KI GHANTI"), ("अपने आप बजी।", "APNE AAP BAJI.")], 0.02),
            ("build", [("और शिवलिंग से", "AUR SHIVLING SE"), ("एक तेज़ रोशनी निकली।", "EK TEZ ROSHNI NIKLI.")], 0.02),
            ("punch", [("सामने महादेव खड़े थे।", "SAAMNE MAHADEV KHADE THE.")], 0.04)]},
    {"key": "vachan", "text": "", "visual": "Mahadev blesses him; the boy looks up, golden light on his face",
     "vo": [("awe", [("बोले बेटा तू मेहनत कर", "BOLE BETA TU MEHNAT KAR"), ("मैं तेरे साथ हूं।", "MAIN TERE SAATH HOON.")], 0.04)]},
    {"key": "interview", "text": "", "visual": "Next morning's interview: he sits straight, rudraksh glowing; calm hands",
     "vo": [("tell", [("अगली सुबह वो फिर", "AGLI SUBAH WO PHIR"), ("इंटरव्यू देने गया।", "INTERVIEW DENE GAYA.")], 0.02),
            ("build", [("इस बार हाथ नहीं कांपे।", "IS BAAR HAATH NAHIN KAANPE.")], 0.04)]},
    {"key": "naukri", "text": "", "visual": "Phone glows green, he cries with joy and runs to the temple; Mahadev smiles; loop",
     "vo": [("punch", [("और शाम को फोन आया", "AUR SHAAM KO PHONE AAYA"), ("आपकी नौकरी पक्की हो गई।", "AAPKI NAUKRI PAKKI HO GAYI.")], 0.02),
            ("awe", [("वो रोता हुआ मंदिर भागा", "WO ROTA HUA MANDIR BHAAGA"), ("क्योंकि वो था", "KYUNKI WO THA")], 0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "SHIV": SHIV_BLUE, "JAL": hexc("#9AD8FF"), "BEES": hexc("#FF5A5A"), "REJECT": hexc("#FF5A5A"),
    "DELIVERY": hexc("#FFB347"), "SAPNA.": GOLD_HI, "BAARISH": hexc("#9AD8FF"), "AANSU": hexc("#9AD8FF"),
    "MAHADEV": SHIV_BLUE, "HAARUNGA": GOLD_HI, "GHANTI": GOLD_HI, "SHIVLING": SHIV_BLUE, "ROSHNI": GOLD_HI,
    "MEHNAT": GOLD_HI, "SAATH": SHIV_BLUE, "INTERVIEW": hexc("#FFB347"), "HAATH": hexc("#9BE07A"),
    "NAUKRI": hexc("#9BE07A"), "PAKKI": hexc("#9BE07A"), "MANDIR": hexc("#FFB347"),
})


def shiv_light(ctx, x, s, t, a):
    if a <= 0:
        return
    glow(ctx, x, FEET - 520 * s, 460 * s, SHIV_BLUE, 0.5 * a)
    mahadev(ctx, x, FEET, s, t, pose="bless", a=a)


# =============================================================================
# Scenes
# =============================================================================
class Jal(Cued):
    def beats(self, d):
        c = self.cue
        return {"reject": c("BEES BAAR", d * 0.62)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "ghanti"), (b["reject"], "beep"), (b["reject"] + 0.25, "beep")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        shiv_temple(ctx, t, night=False)
        shivling(ctx, 640, FEET - 20, 1.25, t)
        if t < b["reject"]:
            boy(ctx, 330, FEET - 10, 0.76, t, pose="pour", mood="calm", look=(0.6, 0.3))
        else:                                                    # the phone flashes red: rejected again
            boy(ctx, 330, FEET - 10, 0.76, t, pose="phone", mood="sad", look=(0.0, 0.5))
            blink = 0.5 + 0.5 * math.sin((t - b["reject"]) * 14)
            glow(ctx, 330, FEET - 372, 130, hexc("#FF3A3A"), 0.6 * blink)
        edge_glow(ctx, t, d, start=0.25)


class Sangharsh(Cued):
    def beats(self, d):
        c = self.cue
        return {"raat": c("AUR RAAT", d * 0.25), "ghar": c("GHAR WAALE", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "whoosh"), (b["raat"], "tick"), (b["ghar"], "soft_thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        if t < b["raat"]:                                       # day: delivery on the scooter
            shiv_temple(ctx, t, night=False)
            ride = clamp(t / max(0.5, b["raat"]))
            x = lerp(150, 620, ride)
            scooter(ctx, x, FEET, t)
            boy(ctx, x + 20, FEET - 120, 0.72, t, pose="ride", mood="neutral", look=(0.6, 0.0), seated=True)
            return
        room_bg(ctx, t, night=1.0, lamp=1.0)
        mahadev_photo(ctx, 820, 560, t, s=1.0)
        if t < b["ghar"]:
            boy(ctx, 480, FEET - 30, 0.74, t, pose="write", mood="tired", look=(0.0, 0.6), seated=True)
            desk(ctx, 480, FEET - 10, t, lamp=1.0, books=4)
        else:                                                    # parents shake their heads in the doorway light
            ctx.save()
            ctx.rectangle(560, FEET - 760, 420, 740)
            ctx.clip()
            rgba(ctx, hexc("#FFD9A0"), 0.9)
            ctx.paint()
            relatives(ctx, 660, 2, t, laugh=0.0)
            ctx.restore()
            boy(ctx, 260, FEET - 10, 0.74, t, pose="drop", mood="cry", look=(0.7, 0.0))


class Barish(Cued):
    def beats(self, d):
        c = self.cue
        return {"aansu": c("AANKHON MEIN", d * 0.4), "bola": c("BAS ITNA", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "soft_thud"), (b["aansu"], "tick"), (b["bola"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        shiv_temple(ctx, t, night=True, rain=1.0)
        shivling(ctx, 640, FEET - 20, 1.25, t)
        walk = ease_out_cubic(clamp(t / max(0.6, b["aansu"] - 0.2)))
        boy(ctx, lerp(80, 330, walk), FEET - 10, 0.74, t, pose="drop" if t < b["aansu"] else "namaste",
            mood="cry", look=(0.7, -0.2))
        if t >= b["bola"]:
            glow(ctx, 330, FEET - 520, 140, SHIV_BLUE, 0.3)


class Darshan(Cued):
    def beats(self, d):
        c = self.cue
        return {"ghanti": c("TABHI MANDIR", 0.1) + 0.4, "roshni": c("AUR SHIVLING", d * 0.4),
                "mahadev": c("SAAMNE MAHADEV", d * 0.72)}

    def events(self, d):
        b = self.beats(d)
        return [(b["ghanti"], "ghanti"), (b["roshni"], "zap"), (b["roshni"] + 0.1, "shimmer"), (b["mahadev"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        light = clamp((t - b["roshni"]) / 0.5)
        shiv_temple(ctx, t, night=True, rain=1.0 - light, light=light)
        ring = clamp(1 - abs(t - b["ghanti"] - 0.6) / 1.0)
        temple_ghanta(ctx, 440, 760, t, ring=ring)
        shivling(ctx, 640, FEET - 20, 1.25, t)
        if light > 0:
            for k in range(10):                                  # rays from the shivling
                ang = -math.pi / 2 + (k - 4.5) * 0.18
                line(ctx, [(640, FEET - 120), (640 + 900 * math.cos(ang), FEET - 120 + 900 * math.sin(ang))],
                     SHIV_BLUE, 10, 0.25 * light)
        appear = ease_out_back(clamp((t - b["mahadev"] + 0.2) / 0.7))
        shiv_light(ctx, 870, 0.62 + 0.12 * appear, t, a=clamp(appear))
        boy(ctx, 280, FEET - 10, 0.72, t, pose="namaste", mood="shock" if t >= b["mahadev"] else "cry",
            look=(0.8, -0.5))
        sparkle_burst(ctx, 870, FEET - 520, (t - b["mahadev"]) / 0.9, c=SHIV_BLUE, r=260)


class Vachan(Cued):
    def beats(self, d):
        return {"saath": self.cue("MAIN TERE", d * 0.5)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "shimmer"), (b["saath"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        shiv_temple(ctx, t, night=True, light=1.0)
        dv.petals(ctx, t, n=26, seed=6, a=0.8)
        shiv_light(ctx, 700, 0.76, t, a=1.0)
        boy(ctx, 300, FEET - 10, 0.72, t, pose="namaste", mood="cry" if t < b["saath"] else "calm", look=(0.8, -0.6))
        if t >= b["saath"]:
            glow(ctx, 300, FEET - 560, 160, GOLDEN, 0.5)


class Interview(Cued):
    def beats(self, d):
        return {"haath": self.cue("IS BAAR", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "tick"), (b["haath"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        interview_room(ctx, t)
        glow(ctx, 330, FEET - 500, 260, SHIV_BLUE, 0.25 + 0.15 * clamp((t - b["haath"]) / 0.5))
        dv.silhouette(ctx, lambda: boy(ctx, 820, FEET - 30, 0.74, t, pose="stand", flip=True, seated=True),
                      c=hexc("#2A2E3A"))                         # interviewer
        boy(ctx, 330, FEET - 30, 0.74, t, pose="namaste" if t < b["haath"] else "write",
            mood="calm", look=(0.7, 0.0), seated=True)
        rudraksh(ctx, 330, FEET - 30 + 150 * 0.74 - 540 * 0.74, t, glow_a=0.6 * clamp((t - b["haath"]) / 0.4))
        rrect(ctx, 120, FEET - 230, 840, 40, 6)                  # interview table
        ink(ctx, hexc("#6A5040"), 4)
        rrect(ctx, 150, FEET - 190, 780, 180, 6)
        ink(ctx, hexc("#5A4034"), 4)


class Naukri(Cued):
    def beats(self, d):
        c = self.cue
        return {"pakki": c("AAPKI NAUKRI", d * 0.3), "bhaaga": c("WO ROTA", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "dingdong"), (b["pakki"], "shimmer"), (b["bhaaga"], "whoosh"), (d - 0.5, "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        if t < b["bhaaga"]:
            room_bg(ctx, t, night=0.0)
            mahadev_photo(ctx, 820, 560, t, s=1.0, lit=1.0)
            won = t >= b["pakki"]
            boy(ctx, 380, FEET - 10, 0.76, t, pose="joy" if won else "phone", mood="cry" if won else "shock",
                look=(0.0, -0.4 if won else 0.5))
            if not won:
                glow(ctx, 380, FEET - 372, 120, hexc("#3AE07A"), 0.6)
            else:
                sparkle_burst(ctx, 380, FEET - 520, (t - b["pakki"]) / 0.6, c=hexc("#9BE07A"), r=240)
        else:                                                    # he runs to the temple; Mahadev smiles
            shiv_temple(ctx, t, night=False, light=0.5)
            shivling(ctx, 640, FEET - 20, 1.25, t)
            run = ease_out_cubic(clamp((t - b["bhaaga"]) / 1.0))
            shiv_light(ctx, 880, 0.62, t, a=0.5 * run)
            boy(ctx, lerp(-60, 330, run), FEET - 10, 0.74, t, pose="namaste" if run >= 1 else "stand", mood="cry",
                look=(0.7, -0.3))
            dv.petals(ctx, t, n=24, seed=2, a=run)
        x = clamp((t - (d - 0.45)) / 0.45)                       # loop into the hook's first frame
        if x > 0:
            ctx.push_group()
            Jal().draw(ctx, 0.0, d)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(x)


SCENE_CLASSES = {"jal": Jal, "sangharsh": Sangharsh, "barish": Barish, "darshan": Darshan, "vachan": Vachan,
                 "interview": Interview, "naukri": Naukri}

UPLOAD = {
    "titles": [
        "20 Baar Reject Hua... Phir Mahadev Ne Darshan Diye #shorts",
        "Delivery Boy 20 Baar Reject Hua... Phir Mahadev Aaye #shorts",
        "Mahadev Ne Kaha Tu Mehnat Kar Main Tere Saath Hoon #shorts",
    ],
    "thumb_text": "20 BAAR REJECT",
    "queries": [
        "mahadev motivational story",
        "20 baar reject hua",
        "har har mahadev story",
    ],
    "description": """
20 baar reject hua, ghar wale bole sapna chhod de... phir barish ki raat Mahadev ne darshan diye. Mahadev motivational
story hindi mein - mehnat aur Bholenath par bharose ki kahani. Har har mahadev story har us insaan ke liye jo haar
nahi maanta.

"Beta tu mehnat kar, main tere saath hoon."

Kalpanik prerak katha.

Aapko bhi Mahadev par bharosa hai? Comment mein HAR HAR MAHADEV likho.
""",
    "tags": [
        "mahadev motivational story", "har har mahadev", "mahadev status", "bholenath story", "shiv ji ki kahani",
        "motivational story hindi", "mehnat motivation", "emotional story hindi", "divya rahasya", "mahadev darshan",
        "shorts", "inspirational story", "job motivation", "never give up hindi",
    ],
    "hashtags": ["#Shorts", "#Mahadev", "#HarHarMahadev"],
    "pinned_comment": "Aapko bhi Mahadev par bharosa hai? 🙏 Comment mein HAR HAR MAHADEV likho",
}


def thumbnail(ctx):
    shiv_temple(ctx, 0.5, night=True, rain=0.6, light=1.0)
    shivling(ctx, 640, FEET - 20, 1.25, 0.5)
    shiv_light(ctx, 880, 0.74, 0.5, a=1.0)
    boy(ctx, 280, FEET - 10, 0.76, 0.5, pose="namaste", mood="cry", look=(0.8, -0.5))
    text(ctx, "20 BAAR REJECT", 540, 1330, 116, hexc("#FF5A5A"), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
         stroke_w=18)
    text(ctx, "PHIR MAHADEV AAYE", 540, 1470, 100, SHIV_BLUE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
         stroke_w=18)
