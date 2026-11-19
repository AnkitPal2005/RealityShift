"""Ghatotkacha Rahasya: Shri Krishna Maut Par Kyun Naache? (~20-22s katha, 4 scenes).

Topic from YouTube Studio AI official recommendation:
The untold tactical sacrifice behind Ghatotkacha's death in the Mahabharata, 
where Krishna's celebration saved Arjuna from Karna's invincible Vasavi Shakti weapon.
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
from core.devta import group, place, halo, smooth, ink, ell, gem, limb, hand, sheen, eye, shade, bow, line, circle, rrect, text

TOPIC = "GHATOTKACH KRISHNA RAHASYA"
OUTPUTS = {"edge": "ghatotkach_short.mp4", "files": "ghatotkach_short.mp4"}
MUSIC_STYLE = "divine"
MUSIC_BPM = 96
MUSIC_VOLUME = 0.12
TAIL_PAD = 0.0
MAX_GAP = None

WHITE = (1.0, 1.0, 1.0)
GOLD_HI = hexc("#FFE066")
CYAN_AURA = hexc("#82C4FF")
FIRE_ORANGE = hexc("#FF5500")
FIRE_YELLOW = hexc("#FFCC00")
DEEP_NIGHT = hexc("#0C0614")
WAR_RED = hexc("#8B0000")

SOURCES = [
    "Mahabharata (Drona Parva, Ghatotkacha-badha Parva): Karna is compelled to use Indra's Amogha Vasavi Shakti dart against Ghatotkacha during the night battle, saving Arjuna's life.",
    "Mahabharata: Krishna dances and rejoices upon Ghatotkacha's death, revealing to an aggrieved Arjuna that Karna's invincible one-time weapon has been spent, securing Dharma's victory.",
]

SPEC = [
    {
        "key": "hook",
        "text": "GHATOTKACH GIRA KRISHNA NAACHE",
        "visual": "Night Kurukshetra: Giant Ghatotkacha falls; Pandavas weeping while Shri Krishna raises his hands with a divine radiant aura",
        "vo": [
            ("punch", [("घटोत्कच का शरीर ज़मीन पर गिरा", "GHATOTKACH KA SHAREER ZAMEEN PAR GIRA"),
                       ("और पूरी पांडव सेना रोने लगी।", "AUR POORI PANDAV SENA RONE LAGI."),
                       ("लेकिन तभी, श्रीकृष्ण खुशी से नाचने लगे!", "LEKIN TABHI, SHRI KRISHNA KHUSHI SE NAACHNE LAGE!")], 0.04),
        ],
    },
    {
        "key": "outrage",
        "text": "ARJUN KA KRODH",
        "visual": "Arjun confronting Shri Krishna in shock and agony; Krishna smiling calmly, raising his blessing palm",
        "vo": [
            ("tell", [("अर्जुन भड़क गए कि", "ARJUN BHADAK GAYE KI"),
                      ("भतीजे की मौत पर उत्सव क्यों?", "BHATIJE KI MAUT PAR UTSAV KYUN?"),
                      ("तब कृष्ण बोले,", "TAB KRISHNA BOLE,")], 0.04),
        ],
    },
    {
        "key": "vasavi",
        "text": "INDRA KA VASAVI SHAKTI ASTRA",
        "visual": "Karna holding the blinding golden lightning spear Vasavi Shakti; ominous doom aura targeting Arjuna",
        "vo": [
            ("build", [("कर्ण के पास इंद्र का वो अमोघ अस्त्र था,", "KARNA KE PAAS INDRA KA WO AMOGH ASTRA THA,"),
                       ("जो सिर्फ एक बार चल सकता था", "JO SIRF EK BAAR CHAL SAKTA THA"),
                       ("और तुम्हारा वध तय था!", "AUR TUMHARA VADH TAY THA!")], 0.04),
        ],
    },
    {
        "key": "sacrifice",
        "text": "GHATOTKACH KA AMAR BALIDAAN",
        "visual": "Ghatotkacha's heroic cosmic sacrifice; golden floral shower, Arjuna protected under Krishna's divine light",
        "vo": [
            ("awe", [("घटोत्कच ने कर्ण को वो अस्त्र खुद पर", "GHATOTKACH NE KARNA KO WO ASTRA KHUD PAR"),
                     ("चलाने पर मजबूर कर दिया,", "CHALAANE PAR MAJBOOR KAR DIYA,"),
                     ("अपने प्राण देकर उसने अर्जुन और पूरे धर्म को बचा लिया!", "APNE PRAN DEKAR USNE ARJUN AUR POORE DHARM KO BACHA LIYA!")], 0.04),
        ],
    },
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "GHATOTKACH": GOLD_HI,
    "KRISHNA": CYAN_AURA,
    "PANDAV": hexc("#60D394"),
    "NAACHNE": GOLD_HI,
    "ARJUN": CYAN_AURA,
    "MAUT": hexc("#FF5555"),
    "UTSAV": GOLD_HI,
    "KARNA": hexc("#FFB74D"),
    "INDRA": GOLD_HI,
    "VASAVI": GOLD_HI,
    "SHAKTI": GOLD_HI,
    "AMOGH": GOLD_HI,
    "ASTRA": hexc("#FF5500"),
    "DHARM": GOLD_HI,
    "BALIDAAN": GOLD_HI,
})


def night_battlefield(ctx, t, fire=True):
    """Night Kurukshetra: dark sky, distant bonfires, silhouettes of war."""
    dv.sky(ctx, hexc("#06020E"), hexc("#1A0822"), hexc("#34101A"), 0.6)
    dv.stars(ctx, t, n=60, a=0.8)
    
    # Distant burning fires
    if fire:
        for fx in (150, 420, 780, 960):
            glow_sz = 90 + 20 * math.sin(t * 8.0 + fx)
            glow(ctx, fx, GROUND - 40, glow_sz, FIRE_ORANGE, 0.4)
            glow(ctx, fx, GROUND - 40, glow_sz * 0.5, FIRE_YELLOW, 0.6)
            
    # Ground silhouette
    ctx.move_to(0, GROUND - 20)
    for x in range(0, W + 1, 40):
        ctx.line_to(x, GROUND - 20 - 8 * math.sin(x / 60))
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    rgba(ctx, hexc("#12060C"))
    ctx.fill()


def arjuna(ctx, x, y, s, t, pose="bow", flip=False, a=1.0):
    """Maharathi Dhanurdhar Arjuna: Royal warrior mukut with ruby crest, armored chestplate, Gandiva."""
    def draw():
        place(ctx, x, y, s, t, flip)
        halo(ctx, 0, -650, 160, t, c=GOLD_HI)
        skin = hexc("#E8A87C")
        hair = dv.HAIR

        # Hair locks flowing behind shoulders
        for side in (-1, 1):
            smooth(ctx, [(side * 65, -690), (side * 115, -610), (side * 128, -530), (side * 118, -460), (side * 88, -470), (side * 80, -550)])
            ink(ctx, hair)
        ell(ctx, 0, -658, 108, 102)
        ink(ctx, hair)

        # Quiver with arrows slung across back
        ctx.save()
        ctx.translate(-70, -480)
        ctx.rotate(-0.35)
        rrect(ctx, -20, -120, 40, 240, 8)
        ink(ctx, hexc("#6E260E"), 5)
        for arr_i in (-12, 0, 12):
            line(ctx, [(arr_i, -120), (arr_i, -165)], dv.GOLD, 5)
            line(ctx, [(arr_i - 8, -155), (arr_i, -165), (arr_i + 8, -155)], dv.RED_GEM, 4)
        ctx.restore()

        # Strong warrior feet & greaves (armored boots)
        for fx in (-48, 48):
            ell(ctx, fx, -14, 44, 18)
            ink(ctx, skin)
            line(ctx, [(fx - 24, -28), (fx, -22), (fx + 24, -28)], dv.GOLD, 7)

        # White/Saffron Dhoti
        dhoti = [(-112, -340), (112, -340), (130, -200), (145, -45), (60, -32), (0, -60), (-60, -32), (-145, -45), (-130, -200)]
        smooth(ctx, dhoti)
        ink(ctx, dv.WHITE)
        line(ctx, [(140, -48), (60, -35), (0, -62), (-60, -35), (-140, -48)], dv.GOLD, 8)

        # Golden Armored Kavach (Chestplate)
        chest = [(-118, -500), (-60, -525), (60, -525), (118, -500), (125, -425), (96, -340), (-96, -340), (-125, -425)]
        smooth(ctx, chest)
        ink(ctx, dv.GOLD, 6)
        sheen(ctx, 0, -430, 75, 45, 0.2)
        circle(ctx, 0, -430, 24, dv.RED_GEM)
        circle(ctx, 0, -430, 16, dv.GOLD_HI)

        # Angavastra sash
        smooth(ctx, [(-122, -502), (-82, -518), (112, -370), (92, -340)], k=0.1)
        ink(ctx, dv.SAFFRON, 4)

        # Kamarbandh
        rrect(ctx, -110, -360, 220, 32, 10)
        ink(ctx, dv.GOLD, 5)
        gem(ctx, 0, -344, 9, dv.RED_GEM)

        # Neck & Divine Warrior Face
        rrect(ctx, -30, -568, 60, 56, 12)
        ink(ctx, skin)
        ell(ctx, 0, -638, 90, 94)
        ink(ctx, skin)

        # Warrior Tilak
        line(ctx, [(0, -710), (0, -670)], hexc("#D01010"), 7)
        circle(ctx, 0, -664, 4, dv.WHITE)

        # Big Expressive Eyes
        eye_look = (0.2, 0.0) if flip else (-0.2, 0.0)
        if pose == "shock":
            eye_look = (0.0, -0.4)
        for side in (-1, 1):
            eye(ctx, side * 34, -644, 22, 24, t, look=eye_look, iris=hexc("#2D1E16"), seed=1)
            line(ctx, [(side * 12, -670), (side * 34, -676), (side * 54, -670)], hexc("#1A100C"), 5)

        # Expressions (Mouth)
        if pose == "shock":
            ell(ctx, 0, -572, 12, 16)
            ink(ctx, hexc("#521414"), 3)
        else:
            ctx.move_to(-16, -574)
            ctx.curve_to(-6, -566, 6, -566, 16, -574)
            ctx.set_line_width(4)
            rgba(ctx, hexc("#6A1810"))
            ctx.stroke()

        # Royal Warrior Mukut (Properly seated on head)
        mukut = [(-70, -715), (-50, -805), (0, -855), (50, -805), (70, -715), (0, -725)]
        smooth(ctx, mukut)
        ink(ctx, dv.GOLD, 5)
        gem(ctx, 0, -785, 12, dv.RED_GEM)
        gem(ctx, -32, -750, 8, hexc("#1FA35B"))
        gem(ctx, 32, -750, 8, hexc("#1FA35B"))

        # Poses & Weapons
        if pose == "shock":
            limb(ctx, [(-108, -485), (-160, -440), (-150, -360)], skin, 34)
            dv.palm(ctx, -150, -350, skin, ang=0.3, s=1.1)
            limb(ctx, [(108, -485), (160, -440), (150, -360)], skin, 34)
            dv.palm(ctx, 150, -350, skin, ang=-0.3, s=1.1)

        elif pose in ("namaste", "bow"):
            limb(ctx, [(-108, -485), (-70, -440), (0, -410)], skin, 34)
            limb(ctx, [(108, -485), (70, -440), (0, -410)], skin, 34)
            smooth(ctx, [(-22, -430), (0, -470), (22, -430), (0, -390)])
            ink(ctx, skin, 4)

        elif pose == "vow":
            # Furious Gandiva raised high overhead taking terrible oath
            limb(ctx, [(-108, -485), (-160, -620), (-140, -780)], skin, 36)
            hand(ctx, -140, -780, skin, 24)
            # Heavy Gandiva bow held high in left fist
            ctx.save()
            ctx.translate(-140, -780)
            ctx.rotate(0.2)
            ctx.move_to(0, -260)
            ctx.curve_to(-70, -130, -70, 130, 0, 260)
            ctx.set_line_width(14)
            rgba(ctx, dv.GOLD)
            ctx.stroke()
            line(ctx, [(0, -260), (0, 260)], dv.WHITE, 4)
            ctx.restore()
            # Right arm clenched fist at chest
            limb(ctx, [(108, -485), (140, -420), (40, -440)], skin, 36)
            hand(ctx, 40, -440, skin, 24)

        else:
            limb(ctx, [(-108, -485), (-150, -420), (-140, -320)], skin, 34)
            hand(ctx, -140, -310, skin, 20)
            bow_x = -150
            ctx.move_to(bow_x, -580)
            ctx.curve_to(bow_x - 60, -450, bow_x - 60, -250, bow_x, -120)
            ctx.set_line_width(12)
            rgba(ctx, dv.GOLD)
            ctx.stroke()
            line(ctx, [(bow_x, -580), (bow_x, -120)], dv.WHITE, 3)

            limb(ctx, [(108, -485), (140, -420), (130, -330)], skin, 34)
            hand(ctx, 130, -320, skin, 20)

        ctx.restore()

    group(ctx, a, draw)


def pandava_soldiers(ctx, x, y, s, t, a=1.0):
    """Pandava army warriors weeping in deep grief, with realistic cartoon helmets, armor, tears, and banner."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    
    skin = hexc("#F0B88A")         # Bright warm Kshatriya skin tone
    green = hexc("#1B4D3E")        # Pandava emerald green
    gold = dv.GOLD
    gold_hi = dv.GOLD_HI
    hair = dv.HAIR

    # ----------------- Warrior 1: Standing with Pandava Flag & Wiping Tears -----------------
    ctx.save()
    ctx.translate(-85, 0)
    wob = 3 * math.sin(t * 3.0)
    
    # Flagstaff & Pandava Banner fluttering
    line(ctx, [(-55, 0), (-55, -600)], hexc("#5A3E26"), 12)
    smooth(ctx, [(-55, -590), (70 + 10 * math.sin(t * 4), -550), (60 + 10 * math.sin(t * 4), -440), (-55, -460)], closed=True)
    ink(ctx, green, 4)
    line(ctx, [(-55, -460), (60 + 10 * math.sin(t * 4), -440)], gold, 6)
    circle(ctx, 5 + 8 * math.sin(t * 4), -500, 16, gold)

    # Feet
    for fx in (-28, 28):
        ell(ctx, fx, -14, 32, 16)
        ink(ctx, skin, 4)
        line(ctx, [(fx - 16, -24), (fx + 16, -24)], gold, 6)

    # Emerald Green Dhoti with gold hem
    smooth(ctx, [(-65, -240), (65, -240), (75, -35), (0, -50), (-75, -35)], closed=True)
    ink(ctx, green, 5)
    line(ctx, [(-75, -35), (0, -50), (75, -35)], gold, 7)

    # Golden Armored Torso (Kavach breastplate)
    smooth(ctx, [(-70, -360), (70, -360), (60, -235), (-60, -235)], closed=True)
    ink(ctx, gold, 5)
    sheen(ctx, 0, -300, 45, 30, 0.25)
    # Pandava green sash across chest
    line(ctx, [(-65, -360), (55, -240)], green, 10)

    # Neck
    rrect(ctx, -20, -400, 40, 45, 8)
    ink(ctx, skin, 4)

    # Head & Face
    ell(ctx, 0, -440, 56, 62)
    ink(ctx, skin, 5)

    # Red warrior tilak
    line(ctx, [(0, -480), (0, -450)], hexc("#DC2626"), 6)
    circle(ctx, 0, -445, 3, dv.WHITE)

    # Golden Warrior Helmet with emerald plume
    smooth(ctx, [(-54, -460), (-38, -540), (0, -570), (38, -540), (54, -460), (0, -475)], closed=True)
    ink(ctx, gold_hi, 5)
    gem(ctx, 0, -515, 8, dv.RED_GEM)
    line(ctx, [(0, -570), (16, -610)], green, 10)

    # Big Expressive Cartoon Eyes (Sad, weeping)
    for side in (-1, 1):
        eye(ctx, side * 22, -438, 14, 16, t, look=(0.0, 0.2), iris=hexc("#2D1E16"), seed=2)
        # Shiny cartoon tears streaming down cheek
        tear_y = -410 + ((t * 45 + side * 18) % 45)
        circle(ctx, side * 22, tear_y, 5, hexc("#56CFE1"))
        circle(ctx, side * 22 - 2, tear_y - 2, 2, dv.WHITE)

    # Sad mouth
    ctx.arc(0, -402, 10, math.pi + 0.3, 2 * math.pi - 0.3)
    ctx.set_line_width(4)
    rgba(ctx, hexc("#6A1810"))
    ctx.stroke()

    # Arms: Left arm holding flag, right arm raised wiping eyes
    limb(ctx, [(-60, -350), (-85, -290), (-55, -270)], skin, 26)
    hand(ctx, -55, -270, skin, 16)
    limb(ctx, [(60, -350), (75, -400), (32, -430)], skin, 26)
    hand(ctx, 32, -430, skin, 16)
    ctx.restore()

    # ----------------- Warrior 2: Kneeling on ground in sorrow -----------------
    ctx.save()
    ctx.translate(65, 0)
    
    # Kneeling green dhoti on ground
    smooth(ctx, [(-60, -125), (60, -125), (70, 0), (-70, 0)], closed=True)
    ink(ctx, green, 5)
    line(ctx, [(-70, 0), (70, 0)], gold, 6)

    # Golden Torso bent forward in sorrow
    smooth(ctx, [(-60, -250), (60, -250), (55, -125), (-55, -125)], closed=True)
    ink(ctx, gold, 5)

    # Bowed Head
    ell(ctx, 0, -305, 52, 56)
    ink(ctx, skin, 5)

    # Helmet
    smooth(ctx, [(-48, -325), (-34, -390), (0, -420), (34, -390), (48, -325)], closed=True)
    ink(ctx, gold_hi, 5)

    # Sad weeping cartoon eyes
    for side in (-1, 1):
        eye(ctx, side * 18, -302, 12, 14, t, look=(0.0, 0.3), iris=hexc("#2D1E16"), seed=3)
        circle(ctx, side * 18, -282 + ((t * 40 + side * 15) % 35), 4, hexc("#56CFE1"))

    # Both hands covering face in grief
    limb(ctx, [(-55, -240), (-38, -295), (-12, -305)], skin, 24)
    limb(ctx, [(55, -240), (38, -295), (12, -305)], skin, 24)
    hand(ctx, -12, -305, skin, 16)
    hand(ctx, 12, -305, skin, 16)

    # Bronze Pandava shield on ground
    circle(ctx, 55, -55, 50, hexc("#8C5A28"))
    ink(ctx, gold, 5)
    circle(ctx, 55, -55, 20, gold)
    ctx.restore()

    ctx.restore()


def ghatotkach_fallen(ctx, x, y, s, t, a=1.0):
    """Mighty Rakshasa-Kshatriya Prince Ghatotkacha resting heroically after supreme sacrifice.
    Features: Mystic storm-blue skin, royal horns/gold crown, white tusks, glowing Vasavi Shakti lightning crack, giant Gada.
    """
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    skin = hexc("#5F728D")         # Clearly visible, vibrant dusky storm-blue Rakshasa hero skin!
    gold = dv.GOLD
    gold_hi = dv.GOLD_HI
    dhoti_col = hexc("#C92A2A")    # Crimson Kshatriya warrior dhoti
    armor_col = hexc("#E67E22")    # Heavy golden-bronze armor
    hair_col = dv.HAIR

    # Soft divine radiance around his noble sacrifice
    glow(ctx, 40, -120, 260, gold_hi, 0.5 * a)
    glow(ctx, 40, -120, 420, CYAN_AURA, 0.35 * a)

    # ----------------- Giant Mace (Kaumodaki Gada) Fallen on Ground -----------------
    ctx.save()
    ctx.translate(-190, -25)
    ctx.rotate(-0.12)
    # Heavy ornate handle
    line(ctx, [(-140, 0), (80, 0)], hexc("#3E2723"), 18)
    line(ctx, [(-140, 0), (80, 0)], gold, 7)
    # Spiked golden mace head
    circle(ctx, 110, 0, 56, gold)
    circle(ctx, 110, 0, 42, hexc("#B45309"))
    circle(ctx, 110, 0, 22, dv.RED_GEM)
    for sp_ang in (0, math.pi/3, 2*math.pi/3, math.pi, 4*math.pi/3, 5*math.pi/3):
        sx = 110 + 66 * math.cos(sp_ang)
        sy = 66 * math.sin(sp_ang)
        circle(ctx, sx, sy, 10, gold_hi)
    ctx.restore()

    # ----------------- Legs & Dhoti (Resting horizontally on earth) -----------------
    limb(ctx, [(-130, -80), (-200, -45), (-260, -25)], skin, 54)
    ell(ctx, -270, -22, 38, 20)
    ink(ctx, skin, 5)

    # Crimson warrior dhoti draped across hips and thighs
    smooth(ctx, [(-160, -130), (-40, -130), (0, -30), (-180, -30)], closed=True)
    ink(ctx, dhoti_col, 5)
    line(ctx, [(-40, -130), (0, -30)], gold, 14)  # Kamarbandh

    # ----------------- Colossal Muscular Torso -----------------
    smooth(ctx, [(-50, -165), (105, -165), (120, -40), (-40, -40)], closed=True)
    ink(ctx, armor_col, 6)

    # Golden Kavach Plates on chest
    smooth(ctx, [(-35, -150), (85, -150), (95, -55), (-25, -55)], closed=True)
    ink(ctx, gold, 5)

    # Glowing Vasavi Shakti Divine Lightning Crack on chest!
    pulse = 0.25 * math.sin(t * 6.0)
    glow(ctx, 35, -100, 95, gold_hi, (0.8 + pulse) * a)
    line(ctx, [(15, -140), (30, -105), (22, -90), (55, -70)], gold_hi, 9)
    line(ctx, [(15, -140), (30, -105), (22, -90), (55, -70)], dv.WHITE, 4)
    line(ctx, [(30, -105), (65, -112)], gold_hi, 6)

    # ----------------- Arms Resting on Ground -----------------
    # Left muscular arm resting forward on earth
    limb(ctx, [(-30, -150), (-15, -55), (65, -30)], skin, 46)
    circle(ctx, lerp(-30, -15, 0.5), lerp(-150, -55, 0.5), 28, gold)
    hand(ctx, 65, -30, skin, 26)

    # Right arm resting back
    limb(ctx, [(95, -150), (135, -90), (165, -35)], skin, 44)
    hand(ctx, 165, -35, skin, 24)

    # Spiked heavy pauldrons on shoulder
    circle(ctx, -30, -150, 34, hexc("#78350F"))
    circle(ctx, -30, -150, 18, gold)

    # ----------------- Head & Face (Tilted heroically back in peaceful sacrifice) -----------------
    ctx.save()
    ctx.translate(145, -160)
    ctx.rotate(0.2)

    # Wild thick Rakshasa hair spreading behind head
    for h_side in (-1, 0, 1):
        smooth(ctx, [(-70, -25), (-105 + h_side * 25, 35), (-50 + h_side * 30, 70), (0, 35)], closed=True)
        ink(ctx, hair_col, 4)
    ell(ctx, -25, 0, 90, 78)
    ink(ctx, hair_col, 4)

    # Head
    ell(ctx, 0, 0, 80, 74)
    ink(ctx, skin, 6)

    # Red Kshatriya warrior tilak
    line(ctx, [(-10, -32), (22, -32)], hexc("#DC2626"), 8)
    circle(ctx, 6, -32, 5, dv.WHITE)

    # Peaceful closed eyes in divine sacrifice
    line(ctx, [(-38, -10), (-22, -4), (-6, -10)], dv.OUTLINE, 6)
    line(ctx, [(10, -10), (26, -4), (42, -10)], dv.OUTLINE, 6)

    # Serene heroic smile
    ctx.arc(0, 22, 20, 0.15, math.pi - 0.15)
    ctx.set_line_width(5)
    rgba(ctx, hexc("#5A1820"))
    ctx.stroke()

    # Cute Rakshasa Ivory Tusks curving up from jaw corners!
    smooth(ctx, [(-30, 24), (-42, 4), (-26, 14)], closed=True)
    ink(ctx, dv.WHITE, 3)

    smooth(ctx, [(30, 24), (42, 4), (26, 14)], closed=True)
    ink(ctx, dv.WHITE, 3)

    # Royal Horned Rakshasa Mukut (Crown with twin horns and glowing ruby)
    smooth(ctx, [(-55, -42), (-80, -115), (-42, -90), (0, -115), (42, -90), (80, -115), (55, -42)], closed=True)
    ink(ctx, gold_hi, 6)
    gem(ctx, 0, -75, 14, dv.RED_GEM)

    ctx.restore()

    # Floating divine light embers rising into the night sky
    for pi in range(6):
        sp_x = -70 + pi * 50 + 12 * math.sin(t * 3.0 + pi)
        sp_y = -120 - ((t * 65 + pi * 40) % 200)
        circle(ctx, sp_x, sp_y, 5, gold_hi)
        glow(ctx, sp_x, sp_y, 16, gold_hi, 0.65 * a)

    ctx.restore()


# ============================================================ Scene Classes

class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "gira": c("GIRA", d * 0.25),
            "roye": c("RONE", d * 0.5),
            "krishna": c("KRISHNA", d * 0.7),
            "naache": c("NAACHNE", d * 0.85),
        }

    def events(self, d):
        b = self.beats(d)
        return [
            (0.02, "boom"),
            (b["gira"], "thud"),
            (b["krishna"], "ghanti"),
            (b["naache"], "shimmer"),
        ]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_battlefield(ctx, t, fire=True)
        
        # Left: Pandava soldiers weeping in grief with banner and tears
        pandava_soldiers(ctx, 160, GROUND - 10, 0.75, t, a=0.95)

        # Center: Mighty Rakshasa-Kshatriya prince Ghatotkacha fallen heroically
        fall_y = ease_out_back(clamp(t / max(b["gira"], 0.5)))
        ghatotkach_fallen(ctx, 470, GROUND - 10 + 20 * (1.0 - fall_y), 0.95, t, a=1.0)
        
        # Right: Shri Krishna dancing in joyful divine celebration!
        u = t - b["krishna"]
        if u > 0:
            k_a = clamp(u / 0.4)
            glow(ctx, 840, GROUND - 250, 320, GOLD_HI, 0.5 * k_a)
            dv.krishna(ctx, 840, GROUND - 10, 0.74, t, pose="dance", smile=1.0, flip=False, a=k_a)


class Outrage(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "arjun": c("ARJUN", d * 0.2),
            "utsav": c("UTSAV", d * 0.55),
            "bole": c("BOLE,", d * 0.8),
        }

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["utsav"], "boom"), (b["bole"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_battlefield(ctx, t, fire=False)
        
        # Left: Arjuna in emotional shock / confronting
        arjuna(ctx, 320, GROUND - 10, 0.72, t, pose="shock", flip=False)
        
        # Right: Shri Krishna smiling calmly, divine protector
        glow(ctx, 760, GROUND - 250, 300, GOLD_HI, 0.35)
        dv.krishna(ctx, 760, GROUND - 10, 0.72, t, pose="stand", smile=1.0, flip=True)


class Vasavi(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "karna": c("KARNA", d * 0.15),
            "astra": c("ASTRA", d * 0.45),
            "vadh": c("VADH", d * 0.8),
        }

    def events(self, d):
        b = self.beats(d)
        return [
            (0.02, "thud"),
            (b["astra"], "shimmer"),
            (b["astra"] + 0.1, "whoosh"),
            (b["vadh"], "boom"),
        ]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_battlefield(ctx, t, fire=True)
        
        # Lightning storm in sky
        if int(t * 6) % 3 == 0:
            glow(ctx, 540, 200, 600, CYAN_AURA, 0.25)
            
        # Karna standing in golden armor on right
        glow(ctx, 720, GROUND - 260, 320, hexc("#FF8800"), 0.4)
        dv.karna(ctx, 720, GROUND - 10, 0.74, t, pose="stand", kavach=1.0, flip=True)
        
        # Karna holding the blinding Vasavi Shakti golden lightning dart
        u = t - b["astra"]
        if u > 0:
            sp_y = GROUND - 380 + 10 * math.sin(t * 8)
            glow(ctx, 640, sp_y, 220, GOLD_HI, 0.8)
            # Golden lightning spear
            line(ctx, [(560, sp_y - 200), (680, sp_y + 120)], GOLD_HI, 14)
            line(ctx, [(560, sp_y - 200), (680, sp_y + 120)], WHITE, 6)
            # Spearhead
            circle(ctx, 560, sp_y - 200, 24, GOLD_HI)
            circle(ctx, 560, sp_y - 200, 12, WHITE)
            
        # On-screen visual highlight (subtle text in safe zone)
        text(ctx, "VASAVI SHAKTI", 540, 260, 72, GOLD_HI, font=CAPTION_FONT, stroke=dv.OUTLINE, stroke_w=6)


class Sacrifice(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "ghatotkach": c("GHATOTKACH", d * 0.15),
            "arjun": c("ARJUN", d * 0.55),
            "dharm": c("DHARM", d * 0.8),
        }

    def events(self, d):
        b = self.beats(d)
        return [
            (0.02, "soft_thud"),
            (b["arjun"], "shimmer"),
            (b["dharm"], "ghanti"),
        ]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_battlefield(ctx, t, fire=False)
        
        # Divine golden light bathing the battlefield
        glow(ctx, 540, 500, 500, GOLD_HI, 0.3)
        dv.petals(ctx, t, n=45, seed=12, a=0.9)
        
        # Center-Left: Arjuna bowing with folded hands in deep gratitude
        arjuna(ctx, 360, GROUND - 10, 0.72, t, pose="bow", flip=False)
        
        # Center-Right: Shri Krishna with divine golden halo protecting Arjuna and Dharma
        glow(ctx, 720, GROUND - 260, 360, GOLD_HI, 0.6)
        dv.krishna(ctx, 720, GROUND - 10, 0.74, t, pose="bless", smile=1.0, flip=True)


SCENE_CLASSES = {
    "hook": Hook,
    "outrage": Outrage,
    "vasavi": Vasavi,
    "sacrifice": Sacrifice,
}


def thumbnail(ctx):
    """High-CTR YouTube Shorts cover: Krishna dancing, Pandavas weeping, Ghatotkach fallen."""
    night_battlefield(ctx, 0.0, fire=True)
    glow(ctx, 540, 950, 450, GOLD_HI, 0.4)
    
    # Left: Weeping Pandava soldiers with fluttering banner
    pandava_soldiers(ctx, 160, 1260, 0.82, 0.0, a=0.95)
    
    # Center: Mighty Ghatotkacha fallen heroically with giant mace & Vasavi Shakti mark
    ghatotkach_fallen(ctx, 480, 1260, 1.05, 0.0, a=1.0)
    
    # Right: Shri Krishna dancing in joyful divine ecstasy
    glow(ctx, 840, 1200 - 250, 340, GOLD_HI, 0.6)
    dv.krishna(ctx, 840, 1200, 0.78, 0.25, pose="dance", smile=1.0, flip=False, a=1.0)

    # Top & Bottom vignettes
    g = cairo.LinearGradient(0, 0, 0, 650)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.92)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 650)
    ctx.set_source(g)
    ctx.fill()

    g = cairo.LinearGradient(0, 1400, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.88)
    ctx.rectangle(0, 1400, W, H - 1400)
    ctx.set_source(g)
    ctx.fill()

    # YouTube AI Approved Title Text
    text(ctx, "KRISHNA", 540, 260, 130, CYAN_AURA, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "HASE KYUN?", 540, 395, 135, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=24)
    text(ctx, "DIVYA RAHASYA", 540, 1820, 42, GOLD_HI, a=0.85)

# ============================================================ Upload Kit

UPLOAD = {
    "thumb_text": "KRISHNA HASE KYUN?",
    "titles": [
        "Ghatotkacha Ki Maut Par Krishna Kyun Naache? 😱 #shorts",
        "Karna Ka Vasavi Shakti: Krishna Ka Masterplan",
        "Mahabharat Ka Rahasya: Ghatotkacha Ka Balidaan",
        "Krishna Ne Arjun Ko Kaise Bachaya: Ghatotkacha",
        "Ghatotkacha Death: Krishna Celebration Secret",
    ],
    "queries": [
        "ghatotkacha ki maut par krishna kyun hase",
        "karna vasavi shakti ghatotkacha",
        "ghatotkacha sacrifice mahabharat",
        "krishna saves arjuna from indrastra",
    ],
    "description": (
        "Ghatotkacha ki maut par poori Pandav sena ro rahi thi, lekin Shri Krishna achanak utsav kyun manane lage? "
        "Janiye Mahabharat ka wo gupt rahasya jahan Ghatotkacha ke amar balidaan ne Arjun aur poore Dharma ki raksha ki!\n\n"
        "Is Short me:\n"
        "• Karna ka amogh astra: Indra ki Vasavi Shakti\n"
        "• Ghatotkacha ka mayavi aakraman aur amar balidaan\n"
        "• Shri Krishna ki yudh-neeti aur Arjun ki raksha\n\n"
        "Comment me likhiye: Jai Shri Krishna! 🙏\n\n"
        "#Shorts #Mahabharat #ShriKrishna #Ghatotkacha #Karna #Arjun #SanatanDharma"
    ),
    "tags": [
        "ghatotkacha", "shri krishna", "mahabharat", "karna", "arjun", "vasavi shakti",
        "ghatotkacha death", "krishna dance", "mahabharat shorts", "hindu mythology",
        "kurukshetra war", "drona parva", "sanatan dharma", "barbarik pita"
    ],
    "hashtags": ["#Shorts", "#Mahabharat", "#ShriKrishna", "#Ghatotkacha", "#Karna"],
}
