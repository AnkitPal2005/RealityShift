"""Jab Shri Ram Ne Hanuman Par Teer Chalaya: Ram Se Bada Ram Ka Naam (~50-55s katha, seven scenes).

Usage (from SanatanKatha/):
  python make.py ram_hanuman --preview       # preview contact sheet & thumbnail
  python make.py ram_hanuman --kiki-export   # exports clean voice text files
  python make.py ram_hanuman --kiki-split    # splits user audio into lines
  python make.py ram_hanuman                 # final render with music & devta characters

Rahasya:
The legendary test of devotion from Ananda Ramayana (Yayati Charitra).
When Maharshi Vishwamitra commanded Shri Rama to punish King Yayati, Yayati took refuge
at the feet of Hanuman. To honor both Rama's vow and Hanuman's pledge to protect a refugee,
Rama had to shoot arrows at his dearest devotee. Chanting the Holy Name 'RAM', Hanuman
rendered even the cosmic Brahmastra powerless, proving that God's name is greater than God himself.
"""

import math
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cairo

from core import engine, katha, upload_kit
from core.katha import *  # noqa: F401,F403
import core.devta as dv
from core.devta import group, place, halo, smooth, ink, ell, gem, limb, hand, sheen, eye, shade

TOPIC = "RAM HANUMAN DHARMA YUDDH LEELA"
OUTPUTS = {"edge": "ram_hanuman_short.mp4"}
MUSIC_STYLE = "ambient"   # Fresh cinematic ambient pads (no repetitive flute/drone)
MUSIC_BPM = 88            # Distinct tempo
MUSIC_VOLUME = 0.12       # Subtle background bed, dialogue stands out clearly
TAIL_PAD = 0.04           # Zero awkward pause between scenes
MAX_GAP = 0.04            # Seamless speech flow without stuttering
WHITE = (1.0, 1.0, 1.0)
RED_GEM = hexc("#D61F3A")
HANUMAN_ORANGE = hexc("#E05B16")
HANUMAN_SHADE = hexc("#B44208")

SOURCES = [
    "Ananda Ramayana (Yayati Charitra): Sri Rama confronts Hanuman due to Maharshi Vishwamitra's command regarding King Yayati, demonstrating the supremacy of the Holy Name of Rama over Rama himself.",
    "Krittivasi Ramayana and folk traditions: King Yayati seeks refuge under Hanuman's mother Anjana; Hanuman pledges protection, leading to the divine test where Rama's arrows turn to flowers upon contacting the vibration of Ram-Naam.",
    "Padma Purana (Uttara Khanda): Highlights how the continuous chanting of the two syllables 'RA-MA' creates an impenetrable spiritual armor that shields the devotee from any worldly or celestial weapon.",
]


def ribbon(ctx, x, y, msg, col, u=1.0):
    if u <= 0:
        return
    p = max(0.01, ease_out_back(clamp(u / 0.4)))
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(p, p)
    w = text_width(ctx, msg, 34) + 60
    rrect(ctx, -w / 2, -30, w, 60, 18)
    rgba(ctx, col, 0.92)
    ctx.fill_preserve()
    rgba(ctx, GOLD, 0.95)
    ctx.set_line_width(3)
    ctx.stroke()
    text(ctx, msg, 0, 10, 34, (1, 1, 1), bold=True)
    ctx.restore()


def battlefield_bg(ctx, t, sunset=True):
    """Sacred battlefield and forest atmosphere."""
    if sunset:
        dv.sky(ctx, hexc("#10142A"), hexc("#60253B"), hexc("#CB6430"), 0.58)
        glow(ctx, 540, 680, 420, hexc("#FFAA48"), 0.45)
        circle(ctx, 540, 680, 80, hexc("#FFECA8"), 0.85)
    else:
        dv.sky(ctx, hexc("#0A1022"), hexc("#182548"), hexc("#381836"), 0.58)
        glow(ctx, 540, 650, 360, hexc("#6BA4FF"), 0.3)

    # Distant mountain silhouettes
    ctx.move_to(0, 920)
    for x in range(0, W + 1, 50):
        ctx.line_to(x, 920 - 35 * math.sin(x / 240 + 0.5))
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    rgba(ctx, hexc("#281C38") if sunset else hexc("#151C33"))
    ctx.fill()

    # Forest silhouette
    ctx.move_to(0, 1020)
    for x in range(0, W + 1, 40):
        ctx.line_to(x, 1020 - 25 * math.sin(x / 160 + 1.8) - 15 * math.sin(x / 65))
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    rgba(ctx, hexc("#180D20") if sunset else hexc("#0E1220"))
    ctx.fill()


def shri_ram(ctx, x, y, s, t, pose="bow", flip=False, a=1.0):
    """Maryada Purushottam Shri Ram: Royal warrior mukut, Kodanda bow, Raghuvanshi tilak."""
    def draw():
        place(ctx, x, y, s, t, flip)
        halo(ctx, 0, -650, 175, t, c=GOLD_HI)
        skin = dv.KRISHNA_SKIN
        hair = dv.KRISHNA_HAIR

        # Hair behind shoulders
        for side in (-1, 1):
            smooth(ctx, [(side * 70, -700), (side * 122, -620), (side * 138, -540), (side * 128, -470), (side * 98, -480), (side * 88, -560)])
            ink(ctx, hair)
        ell(ctx, 0, -668, 116, 112)
        ink(ctx, hair)

        # Feet + golden anklets
        for fx in (-50, 50):
            ell(ctx, fx, -14, 44, 18)
            ink(ctx, skin)
            line(ctx, [(fx - 26, -30), (fx, -24), (fx + 26, -30)], GOLD, 7)

        # Saffron dhoti
        dhoti = [(-118, -345), (118, -345), (136, -200), (152, -44), (62, -32), (0, -64), (-62, -32), (-152, -44), (-136, -200)]
        smooth(ctx, dhoti)
        ink(ctx, dv.SAFFRON)
        line(ctx, [(150, -48), (62, -36), (0, -68), (-62, -36), (-150, -48)], hexc("#E8741E"), 13)

        # Torso
        smooth(ctx, [(-122, -500), (-60, -522), (60, -522), (122, -500), (128, -430), (100, -340), (-100, -340), (-128, -430)])
        ink(ctx, skin)

        # Angavastra sash across chest
        smooth(ctx, [(-128, -505), (-88, -520), (118, -372), (96, -342)], k=0.1)
        ink(ctx, hexc("#E0502A"), 5)

        # Kamarbandh
        rrect(ctx, -114, -366, 228, 34, 12)
        ink(ctx, GOLD, 5)
        gem(ctx, 0, -349, 9, RED_GEM)

        # Gold necklace
        line(ctx, [(-66, -516), (-30, -486), (0, -478), (30, -486), (66, -516)], GOLD, 8)
        gem(ctx, 0, -470, 10, RED_GEM)

        # Neck & Head
        rrect(ctx, -32, -566, 64, 64, 14)
        ink(ctx, skin)
        for side in (-1, 1):
            ell(ctx, side * 98, -640, 18, 28)
            ink(ctx, skin)
            circle(ctx, side * 104, -604, 13, GOLD)
        ell(ctx, 0, -640, 100, 110)
        ink(ctx, skin)
        sheen(ctx, -36, -690, 40, 26, 0.14)

        # Noble calm eyes
        for side in (-1, 1):
            eye(ctx, side * 38, -646, 25, 29, t, look=(0, 0), iris=hexc("#2A1810"), seed=2)
            line(ctx, [(side * 14, -686), (side * 38, -697), (side * 64, -688)], hair, 7)

        line(ctx, [(2, -640), (-6, -618), (5, -613)], shade(skin, 0.65), 4)
        ctx.move_to(-20, -594)
        ctx.curve_to(-8, -586, 8, -586, 20, -594)
        ctx.set_line_width(4)
        rgba(ctx, hexc("#B5283C"))
        ctx.stroke()

        # Raghuvanshi tilak (red center + gold chandan)
        line(ctx, [(0, -730), (0, -684)], hexc("#E2231A"), 7)
        line(ctx, [(-6, -720), (-6, -690)], GOLD_HI, 3)
        line(ctx, [(6, -720), (6, -690)], GOLD_HI, 3)

        # Royal warrior mukut (NO peacock feather!)
        mukut = [(-84, -734), (-64, -840), (0, -900), (64, -840), (84, -734), (0, -748)]
        smooth(ctx, mukut)
        ink(ctx, GOLD, 6)
        rrect(ctx, -90, -736, 180, 24, 8)
        ink(ctx, GOLD_HI, 4)
        gem(ctx, 0, -820, 14, RED_GEM)
        gem(ctx, -36, -780, 9, hexc("#00B4D8"))
        gem(ctx, 36, -780, 9, hexc("#00B4D8"))

        # Arms and Kodanda Bow
        if pose == "bow":
            # Left arm holding bow forward
            limb(ctx, [(-112, -490), (-160, -420), (-170, -320)], skin, 38)
            hand(ctx, -170, -310, skin, 22)
            # Kodanda Bow
            ctx.save()
            ctx.translate(-180, -310)
            ctx.rotate(0.12)
            dv.bow(ctx, 0, -320, 320, -70, string_x=10, string_y=0, a=1.0)
            ctx.restore()

            # Right arm drawing or by side
            limb(ctx, [(112, -490), (145, -420), (120, -320)], skin, 38)
            hand(ctx, 120, -310, skin, 22)
        elif pose == "aim":
            # Left arm forward with bow
            limb(ctx, [(-112, -490), (-180, -450), (-220, -450)], skin, 38)
            hand(ctx, -220, -450, skin, 22)
            # Bow drawn
            ctx.save()
            ctx.translate(-230, -450)
            dv.bow(ctx, 0, -320, 320, -85, string_x=70, string_y=0, a=1.0)
            ctx.restore()
            # Right arm pulling string to ear
            limb(ctx, [(112, -490), (150, -520), (30, -520)], skin, 38)
            hand(ctx, 20, -520, skin, 22)
            # Arrow ready - pointing forward towards target (Hanuman)
            dv.divine_arrow(ctx, -330, -450, math.pi, 270, t, a=1.0, trail=0.0)
        elif pose == "shot":
            # Left arm forward with bow
            limb(ctx, [(-112, -490), (-180, -450), (-220, -450)], skin, 38)
            hand(ctx, -220, -450, skin, 22)
            # Bow released (string straight)
            ctx.save()
            ctx.translate(-230, -450)
            dv.bow(ctx, 0, -320, 320, -75, a=1.0)
            ctx.restore()
            # Right arm recoiled / follow-through
            limb(ctx, [(112, -490), (155, -460), (130, -370)], skin, 38)
            hand(ctx, 130, -360, skin, 22)
        elif pose == "embrace" or pose == "bless":
            # Abhaya mudra
            limb(ctx, [(-112, -490), (-145, -420), (-120, -320)], skin, 38)
            hand(ctx, -120, -310, skin, 22)
            limb(ctx, [(112, -490), (160, -430), (150, -340)], skin, 38)
            dv.palm(ctx, 150, -330, skin, ang=0.1, s=1.1)
            # Bow slung over shoulder
            ctx.save()
            ctx.translate(-110, -520)
            ctx.rotate(-0.4)
            dv.bow(ctx, 0, -220, 220, -40, a=0.9)
            ctx.restore()
        else:
            limb(ctx, [(-112, -490), (-145, -420), (-120, -320)], skin, 38)
            hand(ctx, -120, -310, skin, 22)
            limb(ctx, [(112, -490), (145, -420), (120, -320)], skin, 38)
            hand(ctx, 120, -310, skin, 22)
        ctx.restore()
    group(ctx, a, draw)


def hanuman(ctx, x, y, s, t, pose="namaste", flip=False, a=1.0):
    """Pawanputra Hanuman: Divine glowing sindoori skin, vanara grace, golden mukut, folded hands / dhyan / abhaya."""
    def draw():
        place(ctx, x, y, s, t, flip)
        halo(ctx, 0, -620 if pose != "dhyan" else -480, 185, t, c=GOLD)
        skin = HANUMAN_ORANGE
        shade_skin = HANUMAN_SHADE

        if pose == "dhyan":
            # -------------------------------------------------------------
            # Seated in true Padmasana (Lotus Posture) on ground
            # -------------------------------------------------------------
            # Vanara Tail resting peacefully on ground behind
            tail_pts = [(-40, -120), (-120, -140), (-160, -200), (-130, -320), (-80, -360)]
            limb(ctx, tail_pts, skin, 26)
            circle(ctx, -80, -360, 14, skin)

            # Hair/Fur behind shoulders
            for side in (-1, 1):
                smooth(ctx, [(side * 50, -520), (side * 105, -450), (side * 115, -380), (side * 95, -320), (side * 70, -330)])
                ink(ctx, hexc("#5A2008"))
            ell(ctx, 0, -498, 100, 100)
            ink(ctx, hexc("#5A2008"))

            # Folded Cross-Legged Base (Padmasana)
            limb(ctx, [(-80, -180), (-150, -80), (-40, -25)], skin, 50)
            limb(ctx, [(80, -180), (150, -80), (40, -25)], skin, 50)

            # Lotus feet turned upward on thighs with golden anklets
            ell(ctx, -60, -28, 44, 22, rot=-0.15)
            ink(ctx, skin)
            line(ctx, [(-80, -36), (-60, -30), (-40, -36)], GOLD, 7)
            ell(ctx, 60, -28, 44, 22, rot=0.15)
            ink(ctx, skin)
            line(ctx, [(40, -36), (60, -30), (80, -36)], GOLD, 7)

            # Saffron / Golden Dhoti wrapping lap
            smooth(ctx, [(-150, -130), (150, -130), (120, -20), (-120, -20)])
            ink(ctx, GOLD)
            line(ctx, [(-140, -120), (0, -30), (140, -120)], hexc("#E8741E"), 10)

            # Torso (sitting upright)
            smooth(ctx, [(-118, -360), (-60, -384), (60, -384), (118, -360), (124, -280), (95, -170), (-95, -170), (-124, -280)])
            ink(ctx, skin)
            sheen(ctx, 0, -280, 75, 45, 0.12)

            # Janeu thread & Garland
            line(ctx, [(-90, -370), (-45, -330), (20, -270), (85, -200)], WHITE, 4)
            line(ctx, [(-65, -370), (-30, -335), (0, -320), (30, -335), (65, -370)], GOLD, 7)
            gem(ctx, 0, -315, 9, RED_GEM)

            # Hands resting peacefully in lap in Dhyana Mudra
            limb(ctx, [(-110, -350), (-65, -240), (0, -190)], skin, 36)
            limb(ctx, [(110, -350), (65, -240), (0, -190)], skin, 36)
            circle(ctx, -26, -190, 15, GOLD)
            circle(ctx, 26, -190, 15, GOLD)
            # Both palms flat in lap
            smooth(ctx, [(-30, -195), (0, -210), (30, -195), (20, -175), (-20, -175)])
            ink(ctx, skin)

            # Neck & Head
            rrect(ctx, -32, -426, 64, 56, 14)
            ink(ctx, skin)
            for side in (-1, 1):
                ell(ctx, side * 92, -486, 18, 24)
                ink(ctx, skin)
                circle(ctx, side * 98, -456, 11, GOLD)
            ell(ctx, 0, -486, 92, 98)
            ink(ctx, skin)

            # Muzzle / Jaw
            smooth(ctx, [(-40, -450), (40, -450), (34, -408), (0, -398), (-34, -408)])
            ink(ctx, hexc("#F4803A"))

            # Tilak
            line(ctx, [(0, -560), (0, -520)], hexc("#E2231A"), 8)
            line(ctx, [(-5, -554), (-5, -526)], GOLD_HI, 3)
            line(ctx, [(5, -554), (5, -526)], GOLD_HI, 3)

            # Eyes closed in divine bliss
            for side in (-1, 1):
                ctx.move_to(side * 34 - 16, -492)
                ctx.curve_to(side * 34, -484, side * 34, -484, side * 34 + 16, -492)
                ctx.set_line_width(4)
                rgba(ctx, hexc("#3B1808"))
                ctx.stroke()
                line(ctx, [(side * 12, -518), (side * 34, -526), (side * 56, -520)], hexc("#5A2008"), 6)

            # Peaceful smile
            ctx.move_to(-16, -424)
            ctx.curve_to(-5, -416, 5, -416, 16, -424)
            ctx.set_line_width(4)
            rgba(ctx, hexc("#8A1810"))
            ctx.stroke()

            # Golden Mukut
            mukut = [(-72, -568), (-52, -658), (0, -710), (52, -658), (72, -568), (0, -580)]
            smooth(ctx, mukut)
            ink(ctx, GOLD, 5)
            gem(ctx, 0, -640, 11, RED_GEM)

        else:
            # -------------------------------------------------------------
            # Standing Pose (namaste, abhaya, gada)
            # -------------------------------------------------------------
            # Vanara Tail curving elegantly behind
            tail_pts = [(-50, -310), (-140, -360), (-180, -480), (-160, -620), (-90, -700), (-40, -720)]
            limb(ctx, tail_pts, skin, 28)
            circle(ctx, -40, -720, 16, skin)

            # Hair/Fur behind shoulders
            for side in (-1, 1):
                smooth(ctx, [(side * 60, -660), (side * 115, -590), (side * 125, -520), (side * 110, -460), (side * 80, -470), (side * 75, -540)])
                ink(ctx, hexc("#5A2008"))
            ell(ctx, 0, -638, 108, 106)
            ink(ctx, hexc("#5A2008"))

            # Strong legs & feet with golden anklets
            for fx in (-52, 52):
                ell(ctx, fx, -14, 46, 20)
                ink(ctx, skin)
                line(ctx, [(fx - 26, -30), (fx, -24), (fx + 26, -30)], GOLD, 7)

            # Golden & Saffron Dhoti / Langot
            dhoti = [(-110, -330), (110, -330), (128, -200), (142, -50), (60, -36), (0, -60), (-60, -36), (-142, -50), (-128, -200)]
            smooth(ctx, dhoti)
            ink(ctx, GOLD)
            line(ctx, [(140, -52), (60, -38), (0, -62), (-60, -38), (-140, -52)], hexc("#E8741E"), 10)

            # Muscular Torso
            smooth(ctx, [(-128, -480), (-65, -506), (65, -506), (128, -480), (134, -410), (105, -330), (-105, -330), (-134, -410)])
            ink(ctx, skin)
            sheen(ctx, 0, -410, 80, 50, 0.12)

            # Sacred Janeu thread
            line(ctx, [(-100, -490), (-50, -450), (20, -390), (95, -330)], WHITE, 4)

            # Pearl and gold garland
            line(ctx, [(-70, -490), (-35, -455), (0, -440), (35, -455), (70, -490)], GOLD, 7)
            gem(ctx, 0, -435, 10, RED_GEM)

            # Kamarbandh
            rrect(ctx, -112, -350, 224, 30, 10)
            ink(ctx, GOLD, 5)
            gem(ctx, 0, -335, 8, RED_GEM)

            # Neck & Divine Vanara Head
            rrect(ctx, -34, -546, 68, 60, 14)
            ink(ctx, skin)
            for side in (-1, 1):
                ell(ctx, side * 96, -616, 20, 26)
                ink(ctx, skin)
                circle(ctx, side * 102, -586, 12, GOLD)
            ell(ctx, 0, -616, 96, 102)
            ink(ctx, skin)

            # Muzzle/jaw
            smooth(ctx, [(-42, -580), (42, -580), (36, -538), (0, -528), (-36, -538)])
            ink(ctx, hexc("#F4803A"))

            # Tilak
            line(ctx, [(0, -690), (0, -650)], hexc("#E2231A"), 8)
            line(ctx, [(-6, -684), (-6, -656)], GOLD_HI, 3)
            line(ctx, [(6, -684), (6, -656)], GOLD_HI, 3)

            # Eyes
            for side in (-1, 1):
                eye(ctx, side * 36, -624, 23, 26, t, look=(0, 0), iris=hexc("#3B1808"), seed=1)
                line(ctx, [(side * 14, -652), (side * 36, -660), (side * 60, -654)], hexc("#5A2008"), 6)

            # Divine smile
            ctx.move_to(-18, -554)
            ctx.curve_to(-6, -546, 6, -546, 18, -554)
            ctx.set_line_width(4)
            rgba(ctx, hexc("#8A1810"))
            ctx.stroke()

            # Mukut
            mukut = [(-76, -698), (-56, -788), (0, -840), (56, -788), (76, -698), (0, -710)]
            smooth(ctx, mukut)
            ink(ctx, GOLD, 5)
            gem(ctx, 0, -770, 12, RED_GEM)

            # Arm poses
            if pose == "abhaya":
                # Right hand forward in Abhaya blessing (protecting Yayati)
                limb(ctx, [(118, -470), (170, -420), (160, -320)], skin, 38)
                dv.palm(ctx, 160, -310, skin, ang=-0.1, s=1.15)
                # Left hand at waist or holding gada
                limb(ctx, [(-118, -470), (-145, -410), (-110, -340)], skin, 36)
                hand(ctx, -110, -330, skin, 22)
            elif pose == "namaste":
                limb(ctx, [(-118, -470), (-70, -420), (-25, -420)], skin, 36)
                limb(ctx, [(118, -470), (70, -420), (25, -420)], skin, 36)
                circle(ctx, -26, -420, 16, GOLD)
                circle(ctx, 26, -420, 16, GOLD)
                smooth(ctx, [(-20, -440), (0, -460), (20, -440), (12, -410), (-12, -410)])
                ink(ctx, skin)
            elif pose == "gada":
                limb(ctx, [(118, -470), (155, -410), (140, -320)], skin, 36)
                hand(ctx, 140, -310, skin, 22)
                line(ctx, [(140, -220), (140, -450)], GOLD_HI, 12)
                circle(ctx, 140, -450, 42, GOLD)
                gem(ctx, 140, -450, 14, RED_GEM)
                limb(ctx, [(-118, -470), (-150, -410), (-130, -320)], skin, 36)
                dv.palm(ctx, -130, -310, skin, ang=0.1, s=1.0)
            else:
                limb(ctx, [(-118, -470), (-145, -410), (-120, -320)], skin, 36)
                hand(ctx, -120, -310, skin, 22)
                limb(ctx, [(118, -470), (145, -410), (120, -320)], skin, 36)
                hand(ctx, 120, -310, skin, 22)
        ctx.restore()
    group(ctx, a, draw)


def raja_yayati(ctx, x, y, s, t, pose="sharan", flip=False, a=1.0):
    """King Yayati: Royal golden mukut, silk robes, kneeling at Hanuman's feet in surrender."""
    def draw():
        place(ctx, x, y, s, t, flip)
        skin = hexc("#D49666")
        robe = hexc("#542472")

        # Kneeling legs folded on ground
        limb(ctx, [(-45, -160), (-90, -70), (-25, -15)], hexc("#E8D8C0"), 42)
        limb(ctx, [(45, -160), (90, -70), (25, -15)], hexc("#E8D8C0"), 42)
        ell(ctx, -25, -15, 30, 16)
        ink(ctx, hexc("#901828"))
        ell(ctx, 25, -15, 30, 16)
        ink(ctx, hexc("#901828"))

        # Torso bowing forward in humble surrender
        smooth(ctx, [(-85, -360), (85, -360), (100, -180), (60, -130), (-60, -130), (-100, -180)])
        ink(ctx, robe)
        line(ctx, [(0, -360), (0, -140)], GOLD, 6)

        # Royal gold necklace
        line(ctx, [(-45, -350), (0, -295), (45, -350)], GOLD_HI, 6)
        gem(ctx, 0, -290, 10, RED_GEM)

        # Arms outstretched forward in pleading
        limb(ctx, [(-75, -340), (-120, -270), (-150, -200)], skin, 30)
        limb(ctx, [(75, -340), (20, -270), (-120, -200)], skin, 30)
        smooth(ctx, [(-160, -210), (-140, -185), (-120, -210)])
        ink(ctx, skin)

        # Head bowing low
        rrect(ctx, -28, -410, 56, 52, 12)
        ink(ctx, skin)
        ell(ctx, 0, -450, 72, 76)
        ink(ctx, skin)

        # Worried pleading eyes
        eye(ctx, -24, -455, 17, 19, t, look=(-0.3, -0.2), iris=hexc("#201008"))
        eye(ctx, 24, -455, 17, 19, t, look=(-0.3, -0.2), iris=hexc("#201008"))
        # Moustache
        line(ctx, [(-28, -425), (0, -430), (28, -425)], hexc("#22120C"), 5)

        # Royal Mukut
        mukut = [(-56, -500), (-42, -570), (0, -610), (42, -570), (56, -500), (0, -510)]
        smooth(ctx, mukut)
        ink(ctx, GOLD, 5)
        gem(ctx, 0, -550, 9, RED_GEM)
        ctx.restore()
    group(ctx, a, draw)


def rishi_vishwamitra(ctx, x, y, s, t, flip=False, a=1.0):
    """Maharshi Vishwamitra: Ascetic robes, flowing white beard, rudraksha mala."""
    def draw():
        place(ctx, x, y, s, t, flip)
        halo(ctx, 0, -620, 150, t, c=hexc("#FFCC66"), a=0.7)
        skin = hexc("#D29E74")

        # Robes (Gerua / Saffron)
        robe = [(-110, -500), (110, -500), (130, -50), (50, -30), (0, -40), (-50, -30), (-130, -50)]
        smooth(ctx, robe)
        ink(ctx, hexc("#C85520"))

        # Rudraksha Mala
        line(ctx, [(-60, -500), (-30, -440), (0, -420), (30, -440), (60, -500)], hexc("#5A2610"), 8)

        # Head & Ascetic Topknot
        rrect(ctx, -30, -540, 60, 50, 12)
        ink(ctx, skin)
        ell(ctx, 0, -600, 85, 90)
        ink(ctx, skin)
        # Jata / matted hair topknot
        circle(ctx, 0, -690, 50, hexc("#4A3020"))

        # White Beard
        beard = [(-55, -590), (55, -590), (40, -500), (0, -450), (-40, -500)]
        smooth(ctx, beard)
        ink(ctx, hexc("#ECEAE6"))

        # Eyes & Stern brow
        for side in (-1, 1):
            eye(ctx, side * 30, -610, 20, 22, t, look=(0, 0), iris=hexc("#221008"))
            line(ctx, [(side * 12, -630), (side * 45, -634)], hexc("#ECEAE6"), 5)

        # Raised command hand
        limb(ctx, [(95, -480), (140, -430), (130, -340)], skin, 32)
        dv.palm(ctx, 130, -330, skin, ang=0.0, s=0.95)
        ctx.restore()
    group(ctx, a, draw)


# -----------------------------------------------------------------------------
# Story specification: 8 scenes (~50-55s total)
# -----------------------------------------------------------------------------
SPEC = [
    {
        "key": "hook",
        "text": "RAM VS HANUMAN?",
        "visual": "Shri Ram with Kodanda bow facing Hanuman kneeling with folded hands in devotion",
        "vo": [
            ("open", [("सोचो...", "SOCHO...")], 0.04),
            ("punch", [("जब स्वयं भगवान श्री राम ने,", "JAB SWAYAM BHAGWAN SHRI RAM NE,")], 0.02),
            ("awe", [("अपने सबसे प्रिय भक्त हनुमान पर...", "APNE SABSE PRIYA BHAKTA HANUMAN PAR...")], 0.02),
            ("ask", [("धनुष तान दिया!", "DHANUSH TAAN DIYA!")], 0.04),
        ],
    },
    {
        "key": "leela",
        "text": "ANANDA RAMAYANA LEELA",
        "visual": "Golden sacred scriptures glowing in celestial light: Treta Yuga divine test",
        "vo": [
            ("tell", [("आनंद रामायण की इस अद्भुत लीला में,", "ANANDA RAMAYANA KI IS ADBHUT LEELA MEIN,")], 0.02),
            ("awe", [("भक्ति और धर्म की...", "BHAKTI AUR DHARMA KI...")], 0.02),
            ("punch", [("सबसे बड़ी परीक्षा हुई थी!", "SABSE BADI PAREEKSHA HUI THI!")], 0.04),
        ],
    },
    {
        "key": "vachan",
        "text": "GURU AADESH & SHARAN",
        "visual": "Maharshi Vishwamitra's stern command vs King Yayati taking refuge at Hanuman's feet",
        "vo": [
            ("tell", [("ऋषि विश्वामित्र के आदेश पर,", "RISHI VISHWAMITRA KE AADESH PAR,")], 0.02),
            ("build", [("श्री राम को राजा ययाति पर बाण चलाना था.", "SHRI RAM KO RAJA YAYATI PAR BAAN CHALANA THA.")], 0.02),
            ("punch", [("लेकिन ययाति ने हनुमान जी की शरण ले ली!", "LEKIN YAYATI NE HANUMAN JI KI SHARAN LE LI!")], 0.04),
        ],
    },
    {
        "key": "sankat",
        "text": "DHARMA SANKAT",
        "visual": "Rama's royal pledge vs Hanuman's sacred vow of protecting a refugee",
        "vo": [
            ("low", [("अब एक तरफ श्री राम का गुरु-वचन,", "AB EK TARAF SHRI RAM KA GURU-VACHAN,")], 0.02),
            ("tell", [("दूसरी तरफ हनुमान जी का शरणागत धर्म!", "DOOSRI TARAF HANUMAN JI KA SHARANAGAT DHARMA!")], 0.02),
            ("punch", [("दोनों में से कोई पीछे नहीं हट सकता था.", "DONO MEIN SE KOI PEECHHE NAHI HAT SAKTA THA.")], 0.04),
        ],
    },
    {
        "key": "dhyan",
        "text": "DIVYA BAAN & DHYAN",
        "visual": "Battlefield: Rama releases divine arrows while Hanuman closes his eyes and meditates",
        "vo": [
            ("fast", [("रणभूमि में श्री राम ने बाण छोड़े,", "RANBHUMI MEIN SHRI RAM NE BAAN CHHODE,")], 0.02),
            ("punch", [("पर हनुमान जी ने लड़ने से मना कर दिया!", "PAR HANUMAN JI NE LADNE SE MANA KAR DIYA!")], 0.02),
            ("whisper", [("वे आँखें मूँद कर बस ध्यान में बैठ गए.", "VE AANKHEIN MOOND KAR BAS DHYAN MEIN BAITH GAYE.")], 0.04),
        ],
    },
    {
        "key": "chamatkar",
        "text": "RAM SE BADA RAM KA NAAM",
        "visual": "Rama's blazing arrows touch Hanuman's glowing aura and turn into fragrant flowers",
        "vo": [
            ("awe", [("हनुमान जी के मुख से गूँज रहा था—", "HANUMAN JI KE MUKH SE GOONJ RAHA THA—"),
                    ("'राम... राम... राम...',", "'RAM... RAM... RAM...',")], 0.04),
            ("punch", [("और राम जी के सारे दिव्य बाण,", "AUR RAM JI KE SAARE DIVYA BAAN,")], 0.02),
            ("awe", [("हनुमान के चरणों में फूल बन कर गिर पड़े!", "HANUMAN KE CHARNON MEIN PHOOL BAN KAR GIR PADE!")], 0.04),
        ],
    },
    {
        "key": "brahmastra",
        "text": "BRAHMASTRA BHI JHUKA",
        "visual": "Blazing Brahmastra bows and circles Hanuman; Sage Vishwamitra stops the divine duel",
        "vo": [
            ("build", [("जब श्री राम ने ब्रह्मास्त्र उठाया,", "JAB SHRI RAM NE BRAHMASTRA UTHAYA,")], 0.02),
            ("punch", [("तो वह भी 'राम-नाम' के आगे नतमस्तक हो गया!", "TO WAH BHI 'RAM-NAAM' KE AAGE NATMASTAK HO GAYA!")], 0.04),
            ("warm", [("विश्वामित्र ने मुस्कुरा कर लीला समाप्त की.", "VISHWAMITRA NE MUSKURA KAR LEELA SAMAPT KI.")], 0.04),
        ],
    },
    {
        "key": "cta",
        "text": "JAI SHRI RAM",
        "visual": "Shri Ram embracing Hanuman in divine love with celestial flowers; top comment prompt",
        "vo": [
            ("warm", [("इस लीला ने सिद्ध किया कि...", "IS LEELA NE SIDDH KIYA KI...")], 0.02),
            ("punch", [("स्वयं भगवान से भी बड़ा भगवान का नाम है!", "SWAYAM BHAGWAN SE BHI BADA BHAGWAN KA NAAM HAI!")], 0.04),
            ("cta", [("कमेंट में लिखो—", "COMMENT MEIN LIKHO—")], 0.02),
            ("punch", [("जय श्री राम!", "JAI SHRI RAM!")], 0.04),
        ],
    },
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "SOCHO": GOLD_HI,
    "RAM": GOLD_HI,
    "HANUMAN": hexc("#FFAA48"),
    "DHANUSH": hexc("#E8741E"),
    "GURU-VACHAN": GOLD,
    "DHARMA": GOLD_HI,
    "BAAN": hexc("#E8741E"),
    "PHOOL": hexc("#F48FB1"),
    "BRAHMASTRA": hexc("#FF5555"),
    "JAI": GOLD_HI,
    "COMMENT": GOLD_HI,
})


# -----------------------------------------------------------------------------
# Scene Visual Classes
# -----------------------------------------------------------------------------
class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "ram": c("RAM", 1.2),
            "hanuman": c("HANUMAN", d * 0.45),
            "dhanush": c("DHANUSH", d * 0.75),
        }

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["hanuman"], "ghanti"), (b["dhanush"], "whoosh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        battlefield_bg(ctx, t, sunset=True)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#1A0C06"))
        ctx.fill()

        # Left: Shri Ram holding Kodanda bow aiming right
        shri_ram(ctx, 240, GROUND - 10, 0.70, t, pose="aim" if t > b["dhanush"] else "bow", flip=True)

        # Right: Hanuman Ji with folded hands in surrender
        hanuman(ctx, 810, GROUND - 10, 0.70, t, pose="namaste", flip=True)

        # Single sleek top ribbon (Zero clutter)
        ribbon(ctx, 540, 300, "RAM VS HANUMAN?", RED_GEM, 1.0)


class Leela(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "ramayan": c("ANANDA", 1.0),
            "bhakti": c("BHAKTI", d * 0.45),
            "pariksha": c("PAREEKSHA", d * 0.75),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["bhakti"], "shimmer"), (b["pariksha"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        battlefield_bg(ctx, t, sunset=False)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#0A1428"))
        ctx.fill()

        # Sacred glowing scripture mandala in center
        cx, cy = 540, 520
        circle(ctx, cx, cy, 170, GOLD, 0.22)
        circle(ctx, cx, cy, 120, hexc("#142240"), 0.90)

        # Floating spiritual petals
        dv.petals(ctx, t, n=35, seed=5, a=0.85)

        # Left: Shri Ram calm silhouette
        shri_ram(ctx, 230, GROUND - 10, 0.68, t, pose="bless", flip=True)

        # Right: Hanuman Ji folded hands
        hanuman(ctx, 840, GROUND - 10, 0.68, t, pose="namaste", flip=True)

        # Single sleek top ribbon
        ribbon(ctx, 540, 300, "ANANDA RAMAYANA LEELA", GOLD, 1.0)


class Vachan(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "rishi": c("VISHWAMITRA", 1.0),
            "yayati": c("YAYATI", d * 0.4),
            "sharan": c("SHARAN", d * 0.7),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["rishi"], "thud"), (b["sharan"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        battlefield_bg(ctx, t, sunset=False)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#0E1626"))
        ctx.fill()

        # Left: Maharshi Vishwamitra ordering
        rishi_vishwamitra(ctx, 180, GROUND - 10, 0.66, t, flip=True)

        # Center: King Yayati prostrating at Hanuman's feet in surrender
        raja_yayati(ctx, 520, GROUND - 10, 0.62, t, pose="sharan", flip=False)

        # Right: Hanuman Ji shielding Yayati with Abhaya Mudra
        hanuman(ctx, 840, GROUND - 10, 0.70, t, pose="abhaya", flip=True)

        # Single sleek top ribbon
        ribbon(ctx, 540, 300, "YAYATI NE LI SHARAN", RED_GEM, 1.0)


class Sankat(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "vachan": c("GURU-VACHAN", 1.0),
            "dharma": c("DHARMA", d * 0.5),
            "peeche": c("PEECHHE", d * 0.75),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["dharma"], "soft_thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        battlefield_bg(ctx, t, sunset=True)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#1A0E18"))
        ctx.fill()

        # Divine Dharma scales in sky
        dv.balance(ctx, 540, 480, 0.88, 0.08 * math.sin(t * 2.0), t, labels=("GURU VACHAN", "SHARANAGAT"), a=0.95)

        # Shri Ram on left facing right
        shri_ram(ctx, 230, GROUND - 10, 0.68, t, pose="bow", flip=True)

        # Hanuman Ji on right facing left
        hanuman(ctx, 840, GROUND - 10, 0.68, t, pose="namaste", flip=True)

        # Single sleek top ribbon
        ribbon(ctx, 540, 300, "DHARMA SANKAT", GOLD, 1.0)


class Dhyan(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "baan": c("BAAN", 1.2),
            "mana": c("MANA", d * 0.5),
            "dhyan": c("DHYAN", d * 0.75),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["baan"], "arrow"), (b["dhyan"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        battlefield_bg(ctx, t, sunset=True)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#1E0C06"))
        ctx.fill()

        # Left: Shri Ram aiming bow to the right (releases arrow at b["baan"])
        shri_ram(ctx, 230, GROUND - 10, 0.70, t, pose="aim" if t < b["baan"] else "shot", flip=True)

        # Right: Hanuman Ji seated in Padmasana on ground
        hanuman(ctx, 820, GROUND - 10, 0.70, t, pose="dhyan", flip=True)

        # Arrow flying towards Hanuman from the bow
        arrow_progress = clamp((t - b["baan"]) / 1.4)
        if 0 < arrow_progress < 1.0:
            ax = 460 + 320 * arrow_progress
            ay = (GROUND - 325) + ((GROUND - 80) - (GROUND - 325)) * (arrow_progress ** 1.2)
            dv.divine_arrow(ctx, ax, ay, 0.35, 140, t, a=1.0, trail=0.8)

        # Single sleek top ribbon
        ribbon(ctx, 540, 300, "HANUMAN IN DHYAN", GOLD, 1.0)


class Chamatkar(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "ram_naam": c("RAM", 1.0),
            "divya": c("DIVYA", d * 0.45),
            "phool": c("PHOOL", d * 0.75),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["ram_naam"], "shimmer"), (b["phool"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        battlefield_bg(ctx, t, sunset=False)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#121E2C"))
        ctx.fill()

        # Left: Shri Ram releasing divine arrows
        shri_ram(ctx, 180, GROUND - 10, 0.66, t, pose="aim", flip=True)

        # Right: Hanuman in Padmasana surrounded by golden soundwaves of 'RAM RAM'
        hx, hy = 780, GROUND - 10
        hanuman(ctx, hx, hy, 0.70, t, pose="dhyan", flip=True)

        # Glowing golden soundwaves of 'RAM RAM'
        pulse = (math.sin(t * 4.0) + 1) / 2
        circle(ctx, hx, hy - 320, 210 + 25 * pulse, GOLD_HI, 0.25)
        circle(ctx, hx, hy - 320, 150 + 15 * pulse, GOLD, 0.35)

        # Live Transformation: Flying Arrows turn into Lotus Flowers!
        arrow_specs = [
            (0.3, 1.8, 680),
            (2.0, 3.5, 740),
            (3.8, 5.2, 800),
        ]
        for t_start, t_hit, target_x in arrow_specs:
            if t_start <= t < t_hit:
                u = (t - t_start) / (t_hit - t_start)
                ax = 400 + (target_x - 400) * u
                ay = (GROUND - 310) + ((GROUND - 25) - (GROUND - 310)) * (u ** 1.3)
                dv.divine_arrow(ctx, ax, ay, 0.40, 130, t, a=1.0, trail=0.8)
            elif t >= t_hit:
                elapsed = t - t_hit
                if elapsed < 0.6:
                    circle(ctx, target_x, GROUND - 25, 45 * (elapsed / 0.6), GOLD_HI, 0.8 * (1 - elapsed / 0.6))
                    circle(ctx, target_x, GROUND - 25, 20, hexc("#FFE066"), 0.9)
                bloom = min(0.68, 0.68 * (elapsed / 0.3) if elapsed < 0.3 else 0.68)
                dv.lotus(ctx, target_x, GROUND - 20, bloom, c=hexc("#F48FB1"), a=0.98)

        # Extra floating petals around Hanuman's feet
        dv.petals(ctx, t, n=40, seed=7, a=0.95)

        # Single sleek top ribbon
        ribbon(ctx, 540, 300, "RAM SE BADA RAM KA NAAM", GOLD, 1.0)


class Brahmastra(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "brahma": c("BRAHMASTRA", 1.2),
            "jhuka": c("NATMASTAK", d * 0.5),
            "shant": c("LEELA", d * 0.8),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["brahma"], "boom"), (b["jhuka"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        battlefield_bg(ctx, t, sunset=True)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#1A0C0E"))
        ctx.fill()

        # Far Left: Maharshi Vishwamitra smiling and raising hand to stop duel
        rishi_vishwamitra(ctx, 120, GROUND - 10, 0.64, t, flip=True)

        # Left: Shri Ram with bow lowered in reverence
        shri_ram(ctx, 240, GROUND - 10, 0.68, t, pose="bless", flip=True)

        # Right: Hanuman Ji seated in Padmasana with glowing aura
        hanuman(ctx, 820, GROUND - 10, 0.70, t, pose="dhyan", flip=True)

        # Brahmastra celestial disc flying towards Hanuman, stopping and bowing
        bx = 360 + 200 * min(1.0, t / 1.5)
        by = 500
        tilt = 0.5 * min(1.0, max(0.0, (t - b["jhuka"]) / 1.0))
        by += tilt * 80

        ctx.save()
        ctx.translate(bx, by)
        ctx.rotate(tilt)

        circle(ctx, 0, 0, 80, hexc("#FF5533"), 0.5)
        circle(ctx, 0, 0, 54, GOLD_HI, 0.85)

        for i in range(12):
            ang = t * 2.5 + i * (math.tau / 12)
            px = 70 * math.cos(ang)
            py = 70 * math.sin(ang)
            circle(ctx, px, py, 6, GOLD_HI, 0.9)
        ctx.restore()

        # Single sleek top ribbon
        ribbon(ctx, 540, 300, "BRAHMASTRA BHI JHUKA", GOLD, 1.0)


class Cta(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "siddh": c("SIDDH", 1.0),
            "bada": c("BADA", d * 0.35),
            "comment": c("COMMENT", d * 0.65),
            "jai": c("JAI", d * 0.85),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["bada"], "ghanti"), (b["jai"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        battlefield_bg(ctx, t, sunset=True)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#1A1020"))
        ctx.fill()

        # Heavenly shower of petals
        dv.petals(ctx, t, n=50, seed=12, a=0.95)

        # Divine Darshan: Shri Ram lovingly placing hand on Hanuman
        shri_ram(ctx, 380, GROUND - 10, 0.70, t, pose="bless", flip=True)
        hanuman(ctx, 690, GROUND - 10, 0.70, t, pose="namaste", flip=True)

        # Single sleek top ribbon
        ribbon(ctx, 540, 300, "COMMENT 'JAI SHRI RAM'!", RED_GEM, 1.0)


SCENE_CLASSES = {
    "hook": Hook,
    "leela": Leela,
    "vachan": Vachan,
    "sankat": Sankat,
    "dhyan": Dhyan,
    "chamatkar": Chamatkar,
    "brahmastra": Brahmastra,
    "cta": Cta,
}

UPLOAD = {
    "titles": [
        "Jab Shri Ram Ne Hanuman Par Dhanush Uthaya! 🏹 Shocking Leela #shorts",
        "Kyun Shri Ram Ko Hanuman Par Chalana Pada Teer? 😱 #shorts",
        "Ram Se Bada Ram Ka Naam: Jab Brahmastra Bhi Haar Gaya! 🏹 #shorts",
        "Jab Hanuman Ji Par Chale Ram Ke Baan! Divya Rahasya #shorts",
        "Shri Ram vs Hanuman: Yuddh Ka Asli Rahasya Jo Koi Nahi Batata #shorts",
        "Hanuman Par Kyun Beasar Ho Gaye Shri Ram Ke Saare Baan? #shorts",
        "Jab Vishwamitra Ke Aadesh Par Ram Ne Uthaya Dhanush! #shorts",
        "Ram-Naam Ki Wo Shakti Jiske Aage Brahmastra Bhi Jhuk Gaya #shorts",
        "Ramayan Ki Wo Anokhi Leela: Ram Aur Hanuman Ka Yuddh #shorts",
        "Kyun Chalaye Ram Ji Ne Apne Priya Bhakt Par Teer? #shorts",
    ],
    "thumb_text": "RAM VS HANUMAN?",
    "queries": [
        "jab shri ram ne hanuman par teer chalaya",
        "ram vs hanuman katha",
        "ram se bada ram ka naam kahani",
    ],
    "description": """
Jab Shri Ram ne Hanuman par teer chalaya toh kya hua? Dekhiye yeh adbhut Ram vs Hanuman katha jahan Ram se bada Ram ka naam kahani ka chamatkar dekhne mila! 
Ananda Ramayana ki wo pavitra leela jahan 'Ram-Naam' ki shakti ne Brahmastra ko bhi nishfal kar diya.

Is divya katha ko poora dekhein aur comment mein 'JAI SHRI RAM' zaroor likhein. 🚩
""",
    "tags": [
        "ram vs hanuman",
        "jab ram ne hanuman par teer chalaya",
        "ram se bada ram ka naam",
        "hanuman ji",
        "shri ram",
        "ananda ramayana",
        "divya rahasya",
        "sanatan katha",
        "shorts",
    ],
    "hashtags": [
        "#Shorts",
        "#JaiShriRam",
        "#Hanuman",
    ],
}


def thumbnail(ctx):
    battlefield_bg(ctx, 0.3, sunset=True)
    ctx.rectangle(0, GROUND - 25, W, H)
    rgba(ctx, hexc("#1A0C06"))
    ctx.fill()

    # Left: Shri Ram aiming Kodanda Bow to the right
    shri_ram(ctx, 240, GROUND - 10, 0.72, 0.5, pose="aim", flip=True)

    # Right: Hanuman Ji in Dhyan / Namaste with brilliant aura
    hanuman(ctx, 810, GROUND - 10, 0.72, 0.5, pose="namaste", flip=True)

    # Big impactful text
    text(ctx, "RAM VS", 540, 220, 120, GOLD_HI, font=CAPTION_FONT, bold=True, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "HANUMAN?", 540, 340, 110, hexc("#FF4444"), font=CAPTION_FONT, bold=True, stroke=(0, 0, 0), stroke_w=20)
