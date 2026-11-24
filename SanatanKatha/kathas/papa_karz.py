"""Papa Ka Karz (Karm Aur Kripa): creditors shut papa's shop, the son washes dishes at a dhaba; one night an old
sadhu asks for food, the boy gives his last roti, the sadhu says "himmat mat haarna, Ram tere saath hai" and vanishes;
six months of hard work clear the debt, and at the temple Ram ji's murti wears the same smile (~29 s, 9 scenes).
Kalpanik prerak katha.

Usage (from SanatanKatha/):
  python make.py papa_karz --preview
  python make.py papa_karz --kiki-split --check-voice
  python make.py papa_karz --engine files

Ram ji is present in every scene (photo in the shop and the dhaba with a diya, the sadhu = Ram ji in disguise,
the murti, the golden form). The last frame stays on Ram ji's blessing smile (comment-prompt test, AGENTS.md #14).
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
from core.devta import smooth, ink, ell, limb, hand, eye, place, group

from kathas.daadi_morpankh import boy, papa, GOLDEN, FEET
from kathas.ram_hanuman import shri_ram          # royal mukut, Kodanda bow, Raghuvanshi tilak (no mor-pankh)
from kathas.eklavya_krishna import sparkle_burst, edge_glow

TOPIC = "KARM AUR KRIPA PAPA KA KARZ DHABA SADHU AAKHRI ROTI RAM JI"
OUTPUTS = {"edge": "papa_karz_short.mp4"}
MUSIC_STYLE = "ambient"   # devotional; bees_baar_reject used tension, daadi_morpankh pulse
MUSIC_BPM = 90            # >= 6 BPM away from 84 / 76
MUSIC_VOLUME = 0.11
TAIL_PAD = 0.22           # calm storytelling breath (user, 23 Nov)
MAX_GAP = 0.25

SAFFRON = hexc("#E8741E")
SADHU_SKIN = hexc("#B5794E")
SOURCES = [
    "Original fictional story (Kalpanik prerak katha) - no scripture or real-event claim; labelled in the description.",
    "Bhagwan testing a devotee in the form of a hungry sadhu is a common motif of Indian bhakti folk stories. "
    "Shri Ram's form (mukut, Kodanda bow, saffron/pitambar) follows common Ramayana iconography.",
]


# =============================================================================
# Characters and props
# =============================================================================
def sadhu(ctx, x, y, s, t, pose="stand", smile=0.6, divine=0.0, flip=False, a=1.0):
    """Old sadhu (Ram ji in disguise): saffron robe, white beard and bun, Ramanandi tilak, rudraksh, wooden staff.
    pose: stand | walk | receive (both hands forward) | bless (right palm raised). divine 0..1 = golden aura."""
    def draw():
        if divine > 0:
            glow(ctx, x, y - 520 * s, 380 * s, GOLDEN, 0.5 * divine)
        place(ctx, x, y, s, t, flip)
        sway = 10 * math.sin(t * 7) if pose == "walk" else 0
        for side in (-1, 1):                                  # sandals
            ell(ctx, side * 48 + (sway * side if pose == "walk" else 0), -14, 44, 16)
            ink(ctx, hexc("#5A3A1E"))
        smooth(ctx, [(-130, -560), (130, -560), (150, -300), (160 + sway, -40), (-160 + sway, -40),
                     (-150, -300)], k=0.12)                   # long saffron robe
        ink(ctx, SAFFRON)
        smooth(ctx, [(-130, -560), (-40, -560), (110, -300), (60, -280), (-140, -420)], k=0.1)   # shawl
        ink(ctx, hexc("#F4A04A"), 3)
        # staff (held in the left hand when standing/walking)
        if pose in ("stand", "walk"):
            smooth(ctx, [(-176, -40), (-186, -400), (-180, -780), (-168, -790), (-170, -400), (-160, -40)], k=0.1)
            ink(ctx, hexc("#7A4A22"), 3)
        L, R = (-134, -535), (134, -535)
        if pose == "receive":
            arms = [(L, (-110, -430), (40, -450)), (R, (110, -430), (120, -450))]
        elif pose == "bless":
            arms = [(L, (-170, -420), (-172, -330)), (R, (190, -560), (190, -700))]
        else:
            arms = [(L, (-176, -440), (-176, -400)), (R, (160, -420), (150, -320))]
        for sh, el, hd in arms:
            limb(ctx, [sh, el, hd], SAFFRON, 50)
            if pose == "bless" and hd == arms[1][2]:
                dv.palm(ctx, hd[0], hd[1], SADHU_SKIN, ang=0.0, s=1.0)
            else:
                hand(ctx, *hd, SADHU_SKIN, 22)
        for k in range(11):                                   # rudraksh mala
            ang = math.pi * (0.1 + 0.8 * k / 10)
            circle(ctx, 70 * math.cos(ang), -560 + 120 * math.sin(ang), 8, hexc("#6A3A1E"))
        rrect(ctx, -28, -610, 56, 64, 14)
        ink(ctx, SADHU_SKIN)
        ell(ctx, 0, -700, 90, 100)
        ink(ctx, SADHU_SKIN)
        circle(ctx, 0, -812, 40, hexc("#EDEAE4"))             # white jata bun
        ell(ctx, 0, -772, 88, 34)
        ink(ctx, hexc("#EDEAE4"), 2)
        for side in (-1, 1):
            ell(ctx, side * 86, -700, 16, 40)
            ink(ctx, hexc("#EDEAE4"), 2)
            if smile > 0.5:                                   # kind, half-closed smiling eyes
                ctx.arc(side * 32, -704, 16, math.pi * 1.1, math.pi * 1.9)
                rgba(ctx, hexc("#2A1A10"))
                ctx.set_line_width(6)
                ctx.stroke()
            else:
                eye(ctx, side * 32, -708, 17, 20, t, seed=21, iris=hexc("#2A1A10"), skin=SADHU_SKIN, lid=0.3)
            line(ctx, [(side * 14, -738), (side * 50, -742)], hexc("#EDEAE4"), 6)    # white brows
        line(ctx, [(-22, -748), (-12, -780)], hexc("#F4F0E8"), 5)                     # Ramanandi tilak
        line(ctx, [(22, -748), (12, -780)], hexc("#F4F0E8"), 5)
        line(ctx, [(0, -746), (0, -784)], hexc("#D8202A"), 6)
        smooth(ctx, [(-70, -680), (-50, -630), (0, -560), (50, -630), (70, -680), (30, -660), (0, -664),
                     (-30, -660)], k=0.12)                    # beard
        ink(ctx, hexc("#EDEAE4"), 2)
        smooth(ctx, [(-44, -668), (0, -678), (44, -668), (30, -656), (0, -662), (-30, -656)])      # moustache
        ink(ctx, hexc("#F8F6F2"), 2)
        if smile > 0:
            ctx.arc(0, -660, 22, 0.2 * math.pi, 0.8 * math.pi)
            rgba(ctx, hexc("#7A3A2A"), smile)
            ctx.set_line_width(5)
            ctx.stroke()
        ctx.restore()
    group(ctx, a, draw)


def ram_photo(ctx, x, y, t, s=1.0, lit=0.6):
    """Framed Ram ji picture with a marigold garland (the family's faith, in the shop and at the dhaba)."""
    glow(ctx, x, y, 150 * s, GOLDEN, 0.35 * lit + 0.05 * math.sin(t * 2))
    rrect(ctx, x - 80 * s, y - 100 * s, 160 * s, 200 * s, 8)
    ink(ctx, hexc("#7A4A1E"), 4)
    ctx.save()
    ctx.rectangle(x - 70 * s, y - 90 * s, 140 * s, 180 * s)
    ctx.clip()
    rgba(ctx, hexc("#F2C46A"))
    ctx.paint()
    shri_ram(ctx, x, y + 260 * s, 0.3 * s, t, pose="bless")
    ctx.restore()
    for k in range(9):
        ang = math.pi * (k / 8)
        circle(ctx, x + 84 * s * math.cos(ang), y - 108 * s + 70 * s * math.sin(ang) * 0.5, 8 * s,
               hexc("#FF8A1E") if k % 2 else hexc("#FFC21E"))


def ram_light(ctx, x, s, t, a):
    """Shri Ram in golden light - translucent divine presence."""
    if a <= 0:
        return
    glow(ctx, x, FEET - 520 * s, 460 * s, GOLDEN, 0.5 * a)
    shri_ram(ctx, x, FEET, s, t, pose="bless", a=a)


def thali(ctx, x, y, roti=1.0, a=1.0):
    ell(ctx, x, y, 70, 20)
    rgba(ctx, hexc("#C8CCD4"), a)
    ctx.fill()
    ell(ctx, x, y - 2, 56, 14)
    rgba(ctx, hexc("#E4E8EE"), a)
    ctx.fill()
    if roti > 0:
        ell(ctx, x, y - 10, 44, 13)
        rgba(ctx, hexc("#D8A05A"), a * roti)
        ctx.fill()
        for k in range(4):
            circle(ctx, x - 24 + 16 * k, y - 12, 4, hexc("#8A5A2A"), a * roti)


def lane_bg(ctx, t, shutter=1.0, lit=1.0):
    """Market lane at dusk with papa's small shop; shutter 0 = open, 1 = shut and locked."""
    dv.sky(ctx, hexc("#2A1A3A"), hexc("#B8564A"), hexc("#3A2A2A"), 0.55)
    dv.sun_disc(ctx, 900, 520, 60, t, a=0.7, rays=12)
    for k, (x0, w, h, c) in enumerate(((-80, 260, 760, "#3A2A34"), (720, 440, 820, "#34262E"))):
        rrect(ctx, x0, GROUND - 30 - h, w, h, 4)
        rgba(ctx, hexc(c))
        ctx.fill()
        for j in range(3):
            rrect(ctx, x0 + 40 + 120 * (j % 2), GROUND - h + 60 + 160 * j, 70, 90, 4)
            rgba(ctx, hexc("#FFC86A"), 0.6)
            ctx.fill()
    rrect(ctx, 200, 420, 520, 740, 6)                         # shop front
    ink(ctx, hexc("#8A5A3A"), 5)
    rrect(ctx, 220, 440, 480, 80, 4)                          # blank signboard (icons only, no text)
    ink(ctx, hexc("#E8A020"), 3)
    for k in range(5):
        circle(ctx, 280 + 90 * k, 480, 16, hexc("#C8321E") if k % 2 else hexc("#2E6A8A"))
    rrect(ctx, 230, 540, 460, 600, 4)                         # inside: shelves with goods
    rgba(ctx, hexc("#FFE0A8"))
    ctx.fill()
    for r in range(3):
        line(ctx, [(240, 700 + 140 * r), (680, 700 + 140 * r)], hexc("#7A4A1E"), 8)
        for k in range(7):
            rrect(ctx, 250 + 60 * k, 640 + 140 * r, 44, 56, 4)
            rgba(ctx, hexc(("#C8321E", "#2E6A8A", "#3A8A4A", "#E8A020")[(k + r) % 4]))
            ctx.fill()
    ram_photo(ctx, 460, 620, t, s=0.55, lit=lit)
    yb = lerp(540, GROUND - 40, shutter)                      # rolling shutter
    rrect(ctx, 226, 536, 468, yb - 536, 2)
    rgba(ctx, hexc("#6A7078"))
    ctx.fill()
    yy = 550
    while yy < yb - 6:
        line(ctx, [(230, yy), (690, yy)], hexc("#4A5058"), 4)
        yy += 22
    if shutter > 0.97:                                        # padlock
        rrect(ctx, 440, GROUND - 120, 44, 40, 6)
        ink(ctx, GOLD_DK, 3)
        ctx.arc(462, GROUND - 120, 16, math.pi, math.tau)
        rgba(ctx, hexc("#3A3A3A"))
        ctx.set_line_width(6)
        ctx.stroke()
    ctx.rectangle(-80, GROUND - 30, W + 160, H)
    rgba(ctx, hexc("#3A2C28"))
    ctx.fill()


def dhaba_bg(ctx, t, night=1.0, lamp=1.0):
    """Roadside dhaba: tin roof, string bulbs, tandoor fire, charpai, back wall with Ram ji's photo and a diya."""
    if night > 0.5:
        dv.sky(ctx, hexc("#0A0E22"), hexc("#2A2A5A"), hexc("#1A1420"), 0.5)
        dv.stars(ctx, t, n=50, a=0.8)
        glow(ctx, 880, 260, 120, hexc("#EEF2FF"), 0.5)
        circle(ctx, 880, 260, 46, hexc("#F4F4FF"))
    else:
        dv.sky(ctx, hexc("#5A8AD8"), hexc("#FFD9A0"), hexc("#E8B070"), 0.55)
        dv.sun_disc(ctx, 880, 280, 70, t, a=0.9, rays=14)
    for k, (yy, c) in enumerate(((760, "#2A2A40" if night > 0.5 else "#7A8A6A"),)):
        ctx.move_to(-80, 900)
        for x in range(-80, W + 81, 40):
            ctx.line_to(x, yy - 60 * abs(math.sin(x / 190 + k)))
        ctx.line_to(W + 80, 900)
        ctx.close_path()
        rgba(ctx, hexc(c))
        ctx.fill()
    rrect(ctx, -80, 420, W + 160, GROUND - 450, 0)            # back wall
    rgba(ctx, hexc("#6A4A34") if night > 0.5 else hexc("#B8875A"))
    ctx.fill()
    for r in range(7):                                        # brick lines
        line(ctx, [(-80, 480 + 100 * r), (W + 80, 480 + 100 * r)], hexc("#4A3424"), 3, 0.5)
    smooth(ctx, [(-80, 440), (W + 80, 440), (W + 80, 360), (-80, 330)], k=0.02)   # tin roof
    ink(ctx, hexc("#5A6068"), 4)
    for x in (40, W - 40):
        line(ctx, [(x, 440), (x, GROUND - 30)], hexc("#3A2A1E"), 16)
    for k in range(14):                                       # string bulbs
        u = k / 13
        bx = lerp(40, W - 40, u)
        by = 470 + 60 * math.sin(math.pi * u)
        glow(ctx, bx, by, 30, hexc("#FFD27A"), 0.5 * lamp)
        circle(ctx, bx, by, 9, hexc("#FFE6A0"))
    ram_photo(ctx, 540, 640, t, s=0.8, lit=1.0)
    rrect(ctx, 600, 740, 120, 14, 3)                          # little shelf with a diya
    ink(ctx, hexc("#7A4A1E"), 2)
    dv.diya(ctx, 660, 738, 0.5, t, a=1.0)
    smooth(ctx, [(880, GROUND - 30), (900, 930), (1000, 900), (1100, 930), (1120, GROUND - 30)], k=0.08)  # tandoor
    ink(ctx, hexc("#9A5A3A"), 4)
    glow(ctx, 1000, 900, 90, hexc("#FF7A2A"), 0.55 + 0.1 * math.sin(t * 9))
    ctx.rectangle(-80, GROUND - 30, W + 160, H)
    rgba(ctx, hexc("#3A2A20"))
    ctx.fill()


def wash_tub(ctx, x, y, t, plates=6):
    """Washing tub on a low stand, a pile of plates beside it, soap bubbles."""
    for k in range(plates):
        ell(ctx, x - 190, y - 8 - 12 * k, 64, 16)
        ink(ctx, hexc("#C8CCD4"), 2)
    rrect(ctx, x - 40, y - 120, 80, 120, 4)
    ink(ctx, hexc("#5A3A22"), 3)
    smooth(ctx, [(x - 130, y - 230), (x + 130, y - 230), (x + 110, y - 120), (x - 110, y - 120)], k=0.05)
    ink(ctx, hexc("#4A7AA8"), 4)
    for i in range(8):
        u = (t * 0.7 + rnd(i, 3)) % 1
        circle(ctx, x - 100 + 200 * rnd(i, 4), y - 240 - 120 * u, 8 + 6 * rnd(i, 5), hexc("#EAF4FF"), 0.7 * (1 - u))


def ram_mandir_bg(ctx, t, light=0.0):
    """Ram mandir at dawn: saffron flags, a big sanctum arch, Ram ji's murti on a pedestal, diyas, bells."""
    dv.sky(ctx, hexc("#3A4A8A"), hexc("#FFB070"), hexc("#5A3A2A"), 0.5)
    dv.sun_disc(ctx, 170, 640, 64, t, a=0.8, rays=12)
    smooth(ctx, [(260, 1160), (260, 560), (400, 330), (540, 180), (680, 330), (820, 560), (820, 1160)], k=0.05)
    ink(ctx, hexc("#F0D8B0"), 5)
    for x0, top in ((540, 180), (300, 470), (780, 470)):
        line(ctx, [(x0, top), (x0, top - 90)], hexc("#7A4A1E"), 6)
        ctx.move_to(x0, top - 90)
        ctx.line_to(x0 + 70 + 10 * math.sin(t * 4), top - 66)
        ctx.line_to(x0, top - 44)
        ctx.close_path()
        ink(ctx, SAFFRON, 3)
    smooth(ctx, [(340, 1150), (340, 640), (540, 500), (740, 640), (740, 1150)], k=0.08)   # sanctum
    rgba(ctx, hexc("#5A2A1A"))
    ctx.fill()
    glow(ctx, 540, 820, 330, GOLDEN, 0.45 + 0.4 * light)
    rrect(ctx, 430, 1060, 220, 70, 8)                         # pedestal
    ink(ctx, hexc("#D8C8A8"), 4)
    shri_ram(ctx, 540, 1060, 0.52, t, pose="bless")           # the murti
    for k in range(9):
        circle(ctx, 380 + 40 * k, 640 - 90 * math.sin(math.pi * k / 8), 10,
               hexc("#FF8A1E") if k % 2 else hexc("#FFC21E"))
    ctx.rectangle(-80, GROUND - 30, W + 160, H)
    rgba(ctx, hexc("#6A4A34"))
    ctx.fill()
    for k in range(9):
        dv.diya(ctx, 80 + 115 * k, GROUND - 24, 0.55, t + k, a=1.0)


# =============================================================================
# Story: 9 scenes, 83 words (single narrator, no commas or pause signs)
# =============================================================================
SPEC = [
    {"key": "dukaan", "text": "", "visual": "Dusk lane: creditors pull papa's shutter down and lock it; papa's head drops, son beside him",
     "vo": [("punch", [("कर्ज़ वालों ने", "KARZ WAALON NE"), ("पापा की दुकान", "PAPA KI DUKAAN"),
                       ("बंद करा दी।", "BAND KARA DI.")], 0.04)]},
    {"key": "dhaba", "text": "", "visual": "Night dhaba: the son scrubs dishes in a tub; Ram ji's photo and a diya on the wall",
     "vo": [("low", [("बेटा ढाबे पर", "BETA DHAABE PAR"), ("बर्तन धोने लगा।", "BARTAN DHONE LAGA.")], 0.04)]},
    {"key": "sadhu", "text": "", "visual": "An old sadhu with a staff walks in from the dark and stops; the boy looks up",
     "vo": [("whisper", [("एक रात", "EK RAAT"), ("एक बूढ़ा साधु आया", "EK BOODHA SAADHU AAYA")], 0.02),
            ("low", [("और बोला", "AUR BOLA"), ("बेटा भूख लगी है।", "BETA BHOOKH LAGI HAI.")], 0.04)]},
    {"key": "roti", "text": "", "visual": "The boy lifts his own plate with the last roti and hands it to the sadhu",
     "vo": [("tell", [("उसने अपनी", "USNE APNI"), ("आखिरी रोटी", "AAKHRI ROTI"), ("उन्हें दे दी।", "UNHEN DE DI.")], 0.04)]},
    {"key": "ashirvad", "text": "", "visual": "The sadhu smiles and raises his palm over the boy; golden light, Ram ji's faint form behind",
     "vo": [("awe", [("साधु मुस्कुराए", "SAADHU MUSKURAAYE"), ("और बोले", "AUR BOLE"),
                     ("हिम्मत मत हारना", "HIMMAT MAT HAARNA"), ("राम तेरे साथ है।", "RAM TERE SAATH HAI.")], 0.04)]},
    {"key": "gayab", "text": "", "visual": "Flash: the sadhu dissolves into golden sparkles; the boy looks around in shock",
     "vo": [("build", [("और पलक झपकते ही", "AUR PALAK JHAPAKTE HI"), ("गायब हो गए।", "GAAYAB HO GAYE.")], 0.04)]},
    {"key": "mehnat", "text": "", "visual": "Day-night montage of washing; then the shop shutter rolls up and papa hugs him",
     "vo": [("build", [("छह महीने", "CHHAH MAHINE"), ("दिन रात मेहनत की", "DIN RAAT MEHNAT KI"),
                       ("और पूरा कर्ज़", "AUR POORA KARZ"), ("उतर गया।", "UTAR GAYA.")], 0.04)]},
    {"key": "murti", "text": "", "visual": "Ram mandir: he folds his hands; the sadhu's smile fades into the murti's smile",
     "vo": [("awe", [("वो मंदिर पहुंचा", "WO MANDIR PAHUNCHA"), ("तो राम जी की", "TO RAM JI KI"),
                     ("मूर्ति में", "MOORTI MEIN"), ("वही मुस्कान थी।", "WAHI MUSKAAN THI.")], 0.04)]},
    {"key": "jai", "text": "", "visual": "Ram ji's golden form blesses papa and son; petals; last frame on Ram ji's smile",
     "vo": [("punch", [("जो मानता है", "JO MAANTA HAI"), ("वो लिखे", "WO LIKHE"), ("जय श्री राम।", "JAI SHRI RAM.")], 0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "KARZ": hexc("#FF5A5A"), "DUKAAN": hexc("#FFB347"), "BAND": hexc("#FF5A5A"), "BARTAN": hexc("#9AD8FF"),
    "SAADHU": SAFFRON, "BHOOKH": hexc("#FFB347"), "AAKHRI": GOLD_HI, "ROTI": GOLD_HI, "HIMMAT": GOLD_HI,
    "RAM": GOLD_HI, "SAATH": GOLD_HI, "GAAYAB": hexc("#9AD8FF"), "MEHNAT": GOLD_HI, "UTAR": hexc("#9BE07A"),
    "MANDIR": hexc("#FFB347"), "MUSKAAN": GOLD_HI, "JAI": GOLD_HI, "SHRI": GOLD_HI,
})


# =============================================================================
# Scenes
# =============================================================================
class Dukaan(Cued):
    def beats(self, d):
        return {"band": self.cue("BAND KARA", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "whoosh"), (b["band"] + 0.5, "thud"), (b["band"] + 0.7, "pick")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        shut = ease_in_out(clamp((t - b["band"] + 0.2) / 0.7))
        lane_bg(ctx, t, shutter=shut, lit=1.0 - 0.6 * shut)
        for k, x in enumerate((820, 980)):                    # creditors as dark silhouettes
            dv.silhouette(ctx, lambda x=x: papa(ctx, x, FEET, 0.72, t, pose="stand", flip=True), c=hexc("#1A1018"))
        papa(ctx, 230, FEET, 0.72, t, pose="stand", mood="cry" if shut > 0.9 else "sad")
        boy(ctx, 560, FEET, 0.70, t, pose="drop" if shut > 0.9 else "stand", mood="sad", look=(-0.6, 0.2))
        edge_glow(ctx, t, d, start=0.25)


class Dhaba(Cued):
    def events(self, d):
        return [(0.1, "tick"), (d * 0.5, "tock")]

    def draw(self, ctx, t, d):
        dhaba_bg(ctx, t, night=1.0)
        boy(ctx, 300, FEET, 0.74, t, pose="wash", mood="tired", look=(0.0, 0.6))
        wash_tub(ctx, 300, FEET, t, plates=5 + int(t * 2) % 4)


class Sadhu(Cued):
    def beats(self, d):
        return {"bola": self.cue("AUR BOLA", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(0.2, "soft_thud"), (0.8, "soft_thud"), (b["bola"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dhaba_bg(ctx, t, night=1.0)
        walk = ease_out_cubic(clamp(t / max(0.8, b["bola"] - 0.2)))
        sadhu(ctx, lerp(1180, 790, walk), FEET, 0.74, t, pose="walk" if walk < 1 else "stand",
              smile=0.2 if walk < 1 else 0.7, divine=0.12, flip=True)
        looked = t > b["bola"] * 0.5
        boy(ctx, 300, FEET, 0.74, t, pose="wash" if not looked else "stand", mood="tired" if not looked else "neutral",
            look=(0.0, 0.6) if not looked else (0.8, -0.2))
        wash_tub(ctx, 300, FEET, t, plates=6)


class Roti(Cued):
    def beats(self, d):
        return {"aakhri": self.cue("AAKHRI ROTI", d * 0.3), "dedi": self.cue("UNHEN DE", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["aakhri"], "tick"), (b["dedi"], "whoosh"), (b["dedi"] + 0.5, "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dhaba_bg(ctx, t, night=1.0)
        give = ease_in_out(clamp((t - b["dedi"]) / 0.6))
        sadhu(ctx, 790, FEET, 0.74, t, pose="receive" if give > 0.5 else "stand", smile=0.8, divine=0.15, flip=True)
        boy(ctx, 330, FEET, 0.74, t, pose="offer", mood="calm", look=(0.8, 0.0))
        px = lerp(330 + 155 * 0.74, 790 - 80 * 0.74, give)    # plate travels from his hands to the sadhu's
        py = FEET - 450 * 0.74
        if t < b["aakhri"]:
            py = lerp(FEET - 300 * 0.74, py, clamp(t / max(0.3, b["aakhri"])))
        glow(ctx, px, py - 10, 80, GOLDEN, 0.3)
        thali(ctx, px, py, roti=1.0)


class Ashirvad(Cued):
    def beats(self, d):
        return {"himmat": self.cue("HIMMAT MAT", d * 0.4), "ram": self.cue("RAM TERE", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "shimmer"), (b["himmat"], "ghanti"), (b["ram"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dhaba_bg(ctx, t, night=1.0)
        ram_a = clamp((t - b["ram"]) / 0.6)
        if ram_a > 0:                                         # Ram ji's faint form rises behind the sadhu
            ram_light(ctx, 760, 0.80, t, a=0.35 * ram_a)
        sadhu(ctx, 700, FEET, 0.74, t, pose="bless" if t >= b["himmat"] else "stand", smile=1.0,
              divine=0.3 + 0.5 * ram_a, flip=True)
        boy(ctx, 330, FEET, 0.72, t, pose="namaste", mood="cry" if t < b["ram"] else "calm", look=(0.8, -0.4))
        if t >= b["himmat"]:
            glow(ctx, 330, FEET - 560, 150, GOLDEN, 0.35 + 0.2 * ram_a)


class Gayab(Cued):
    def beats(self, d):
        return {"gaayab": self.cue("GAAYAB", d * 0.5)}

    def events(self, d):
        b = self.beats(d)
        return [(b["gaayab"] - 0.1, "zap"), (b["gaayab"], "shimmer"), (b["gaayab"] + 0.3, "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dhaba_bg(ctx, t, night=1.0)
        u = clamp((t - b["gaayab"] + 0.3) / 0.6)
        sadhu(ctx, 700, FEET, 0.74, t, pose="bless", smile=1.0, divine=0.6 + 0.4 * u, flip=True, a=1 - u)
        sparkle_burst(ctx, 700, FEET - 420, u, c=GOLD_HI, n=22, r=320)
        if u >= 1:
            glow(ctx, 700, FEET - 20, 140, GOLDEN, 0.5)       # glowing footprints where he stood
            for side in (-1, 1):
                ell(ctx, 700 + side * 36, FEET - 12, 30, 10)
                rgba(ctx, GOLD_HI, 0.7)
                ctx.fill()
        look = (0.8, -0.2) if u < 1 else (math.sin((t - b["gaayab"]) * 5), -0.2)
        boy(ctx, 330, FEET, 0.72, t, pose="namaste" if u < 0.5 else "stand", mood="shock" if u > 0.3 else "calm",
            look=look)
        flash(ctx, (t - b["gaayab"] + 0.1) / 0.5)


class Mehnat(Cued):
    def beats(self, d):
        return {"karz": self.cue("AUR POORA", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "tick"), (0.6, "tock"), (1.1, "tick"), (b["karz"], "whoosh"), (b["karz"] + 0.6, "kaching")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        if t < b["karz"]:                                     # days and nights flash past at the tub
            night = 1.0 if int(t / 0.5) % 2 else 0.0
            dhaba_bg(ctx, t, night=night)
            boy(ctx, 300, FEET, 0.74, t * 1.8, pose="wash", mood="tired", look=(0.0, 0.6))
            wash_tub(ctx, 300, FEET, t * 2, plates=4 + int(t / 0.5) % 5)
            for k in range(min(6, int(t / 0.4) + 1)):         # savings envelopes stacking up
                rrect(ctx, 820, FEET - 40 - 36 * k, 140, 30, 4)
                ink(ctx, hexc("#F4E8C8"), 3)
            return
        u = ease_out_cubic(clamp((t - b["karz"]) / 0.9))
        lane_bg(ctx, t, shutter=1.0 - u, lit=1.0)
        hug = t > b["karz"] + 0.9
        papa(ctx, 700, FEET, 0.72, t, pose="hug" if hug else "stand", mood="cry")
        boy(ctx, 440 if hug else 330, FEET, 0.70, t, pose="hug" if hug else "joy", mood="joy", look=(0.7, -0.2))
        if hug:
            dv.petals(ctx, t, n=20, seed=4, a=0.8)


class Murti(Cued):
    def beats(self, d):
        return {"murti": self.cue("MOORTI", d * 0.5), "muskaan": self.cue("WAHI MUSKAAN", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "ghanti"), (b["murti"], "shimmer"), (b["muskaan"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        smile_u = clamp((t - b["muskaan"]) / 0.5)
        ram_mandir_bg(ctx, t, light=smile_u)
        ghost = clamp(1 - abs(t - b["muskaan"]) / 0.7)        # the sadhu's smiling face melts into the murti
        if ghost > 0:
            sadhu(ctx, 540, 1060, 0.52, t, pose="stand", smile=1.0, divine=0.6, a=0.55 * ghost)
        if smile_u > 0:
            sparkle_burst(ctx, 540, 720, smile_u, c=GOLD_HI, n=16, r=220)
        walk = ease_out_cubic(clamp(t / 1.0))
        boy(ctx, lerp(-60, 170, walk), FEET, 0.70, t, pose="namaste" if walk >= 1 else "stand",
            mood="shock" if t >= b["muskaan"] else "calm", look=(0.8, -0.5))


class Jai(Cued):
    def events(self, d):
        return [(0.1, "ghanti"), (d * 0.5, "shimmer")]

    def draw(self, ctx, t, d):
        ram_mandir_bg(ctx, t, light=1.0)
        dv.petals(ctx, t, n=30, seed=9, a=0.9)
        ram_light(ctx, 540, 0.78, t, a=clamp(t / 0.6))
        papa(ctx, 880, FEET, 0.68, t, pose="stand", mood="cry")
        boy(ctx, 200, FEET, 0.68, t, pose="namaste", mood="calm", look=(0.8, -0.5))


SCENE_CLASSES = {"dukaan": Dukaan, "dhaba": Dhaba, "sadhu": Sadhu, "roti": Roti, "ashirvad": Ashirvad,
                 "gayab": Gayab, "mehnat": Mehnat, "murti": Murti, "jai": Jai}

UPLOAD = {
    "titles": [
        "Bhookhe Sadhu Ko Aakhri Roti Di... Wo Khud Ram Ji The #shorts",
        "Papa Ka Karz Chukane Wale Bete Ke Paas Aaye Ram Ji #shorts",
        "Dhabe Par Aaya Budha Sadhu... Phir Gayab Ho Gaya #shorts",
    ],
    "thumb_text": "AAKHRI ROTI",
    "queries": [
        "ram ji ki kahani",
        "jai shri ram story",
        "bhagwan sadhu roop kahani",
    ],
    "description": """
Papa ki dukaan band ho gayi, beta dhabe par bartan dhone laga... phir ek raat ek budha sadhu aaya aur bola "beta
bhookh lagi hai". Usne apni aakhri roti de di. Ram ji ki kahani - mehnat aur Shri Ram par bharose ki prerak katha.

"Himmat mat haarna... Ram tere saath hai."

Kalpanik prerak katha.

Papa ka karz chukane ke liye padhai chhodna - sahi ya galat? Comment mein apni raay likho.
""",
    "tags": [
        "ram ji ki kahani", "jai shri ram", "shri ram story", "bhagwan ki kahani", "sadhu roop mein bhagwan",
        "motivational story hindi", "emotional story hindi", "papa ka karz", "divya rahasya", "ram bhakti",
        "shorts", "inspirational story", "karm aur kripa", "prerak katha",
    ],
    "hashtags": ["#Shorts", "#JaiShriRam", "#RamJi"],
    "pinned_comment": "Papa ka karz chukane ke liye padhai chhodna - sahi ya galat? 🤔 Apni raay likho. Aur agar aap "
                      "bhi ghar ki zimmedari utha rahe ho to bataao - hum sab milke Ram ji se aapke liye prarthana "
                      "karenge. Jai Shri Ram 🙏",
}


def thumbnail(ctx):
    dhaba_bg(ctx, 0.5, night=1.0)
    ram_light(ctx, 760, 0.80, 0.5, a=0.4)
    sadhu(ctx, 720, FEET, 0.74, 0.5, pose="receive", smile=1.0, divine=0.8, flip=True)
    boy(ctx, 300, FEET, 0.74, 0.5, pose="offer", mood="calm", look=(0.8, 0.0))
    thali(ctx, 300 + 155 * 0.74, FEET - 450 * 0.74, roti=1.0)
    text(ctx, "AAKHRI ROTI", 540, 1330, 116, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "WO KHUD RAM JI THE", 540, 1470, 96, hexc("#FFFFFF"), font=CAPTION_FONT, bold=False,
         stroke=(0, 0, 0), stroke_w=18)
