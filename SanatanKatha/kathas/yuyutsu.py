"""Yuyutsu: the one Kaurava who crossed over - and the one son of Dhritarashtra who survived (~38 s loop, 7 scenes).

Angle (new topic): Dhritarashtra's hundred sons all fell at Kurukshetra; the only son left was Yuyutsu, born of a
Vaishya maid, who walked over to the Pandavas when Yudhishthir called out just before the battle. Yudhishthir told
him Dhritarashtra's line and funeral offerings now rested on him - and after the war it was he who saw to the last
rites. Debate: ghar ka bhedi ya dharm ka saathi. The last word "KYUNKI" runs into the opening line
"DHRITARASHTRA KE SAU BETE..." (seamless loop).
"""

import math

import cairo

from core.katha import *  # noqa: F401,F403
import core.devta as dv
from core.devta import ell, gem, hand, ink, limb, sheen, smooth, eye, palm
from kathas.ghatotkach_akshauhini import duryodhan, kaurava_mob, dust_cloud

TOPIC = "YUYUTSU KAURAV JO PANDAV PAKSH MEIN GAYA"
OUTPUTS = {"edge": "yuyutsu_short.mp4", "files": "yuyutsu_short.mp4"}
MUSIC_STYLE = "ambient"    # previous Short (eklavya_krishna) used tension: rotate; calm, complete story
MUSIC_BPM = 89             # >= 6 BPM away from eklavya_krishna (82)
MUSIC_VOLUME = 0.12
TAIL_PAD = 0.22          # calm storytelling breath (user, 23 Nov)
MAX_GAP = 0.25
KIKI_PAUSE_MS = 150

YU_SKIN = hexc("#B97B52")
YU_SASH = hexc("#2FB3A3")
YU_SASH_DK = hexc("#1C7D72")
YU_DHOTI = hexc("#173F4A")
SILVER = hexc("#CBD5DE")
YD_SKIN = hexc("#C68E5E")
YD_ROBE = hexc("#F3EAD6")
YD_BLUE = hexc("#3F72C2")
KAURAV_RED = hexc("#8C1C2C")
PANDAV_SAFF = hexc("#F08A1C")
POISON = hexc("#7CFF6B")
FIRE_O = hexc("#FF6A1A")
FIRE_Y = hexc("#FFD24A")
EMBER = hexc("#FF8A3D")

SOURCES = [
    "Mahabharata, Bhishma Parva (Bhagavad-Gita Parva, KM Ganguli trans. section 43): before the first arrow "
    "Yudhishthir calls out amid all the warriors 'He who will choose us, him we shall choose for our ally'; "
    "Yuyutsu alone leaves the Kauravas and goes over 'with beat of drums and cymbals'. Yudhishthir accepts him: "
    "'On thee rests, it seems, the thread of Dhritarashtra's line as also his funeral cake.'",
    "Adi Parva (Sambhava Parva, sec. 115-117): Yuyutsu is Dhritarashtra's son by a Vaishya maid who served "
    "Gandhari (later texts name her Sauvali / Sugadha); Gandhari's hundred sons all fall in the war.",
    "Stri Parva (sec. 26): after the war Yudhishthir charges Sudharman, Dhaumya, Sanjaya, Vidura and Yuyutsu to "
    "perform the funeral rites of the slain. Yuyutsu is among the few warriors who survive the war.",
    "Mahaprasthanika Parva (sec. 1): leaving for the Himalayas, Yudhishthir makes Parikshit king and hands the "
    "care of the kingdom to Yuyutsu, son of the Vaishya wife.",
    "VARIANT: some retellings (e.g. Ramesh Menon's version, folk/TV adaptations) say Yuyutsu warned the Pandavas "
    "of Duryodhan's plot to poison Bheem - not a clear line in the critical text; marked 'kehte hain' in the "
    "voice-over and as a variant in the description.",
]

SPEC = [
    {"key": "hook", "text": "SAU BETE GAYE, EK BACHA",
     "visual": "Ash-grey dusk over the fallen field: a sea of broken red Kaurava banners and smoke; Yuyutsu stands "
               "alone, head bowed, in a shaft of light, then turns to the glowing saffron Pandava flag and walks to it",
     "vo": [("punch", [("धृतराष्ट्र के सौ बेटे", "DHRITARASHTRA KE SAU BETE"),
                       ("युद्ध में मारे गए।", "YUDDH MEIN MAARE GAYE"),
                       ("बचा सिर्फ एक बेटा", "BACHA SIRF EK BETA"),
                       ("जो दुश्मन की तरफ", "JO DUSHMAN KI TARAF"),
                       ("चला गया था।", "CHALA GAYA THA")], 0.04)]},
    {"key": "kaun", "text": "YUYUTSU",
     "visual": "Hastinapur palace at night: blind king on the throne and a veiled maid as silhouettes behind Yuyutsu; "
               "Duryodhan slides in with a glowing poison bowl, Yuyutsu throws out a stopping palm and the bowl falls",
     "vo": [("tell", [("ये था युयुत्सु।", "YE THA YUYUTSU"),
                      ("धृतराष्ट्र और", "DHRITARASHTRA AUR"),
                      ("एक दासी का बेटा।", "EK DAASI KA BETA"),
                      ("कहते हैं उसने भीम को", "KEHTE HAIN USNE BHEEM KO"),
                      ("जहर से बचाया था।", "JAHAR SE BACHAYA THA")], 0.04)]},
    {"key": "senayein", "text": "KURUKSHETRA",
     "visual": "Dawn wide shot: the saffron Pandava army marches in from the left, the red Kaurava army from the right, "
               "both halt face to face; conch-bearers lift their conches",
     "vo": [("build", [("फिर कुरुक्षेत्र में", "PHIR KURUKSHETRA MEIN"),
                       ("दोनों सेनाएं", "DONON SENAYEIN"),
                       ("आमने सामने आ गईं।", "AAMNE SAAMNE AA GAYIN"),
                       ("शंख बजने ही वाले थे।", "SHANKH BAJNE HI WAALE THE")], 0.04)]},
    {"key": "pukaar", "text": "YUDHISHTHIR KI PUKAAR",
     "visual": "Close on Yudhishthir: he throws both arms open and calls out, golden rings roll across the field; far "
               "in the Kaurava ranks one teal-sashed prince looks up",
     "vo": [("low", [("तभी युधिष्ठिर ने", "TABHI YUDHISHTHIR NE"),
                     ("पुकारा।", "PUKAARA"),
                     ("जो हमें चुनेगा", "JO HUMEIN CHUNEGA"),
                     ("हम उसे अपना लेंगे।", "HUM USE APNA LENGE")], 0.04)]},
    {"key": "chala", "text": "AKELA CHAL PADA",
     "visual": "Low side shot: the silent Kaurava ranks stare as Yuyutsu steps out alone and walks across the empty "
               "ground towards the Pandava line, dust at every step",
     "vo": [("tell", [("पूरी कौरव सेना", "POORI KAURAV SENA"),
                      ("चुप रही।", "CHUP RAHI"),
                      ("और एक योद्धा अकेला", "AUR EK YODHA AKELA"),
                      ("उस पार चल पड़ा।", "US PAAR CHAL PADA")], 0.04)]},
    {"key": "cheekh", "text": "DURYODHAN CHEEKHA",
     "visual": "Duryodhan (left) erupts, pointing and shouting with his gada; on the right Yudhishthir lays a hand on "
               "Yuyutsu's shoulder and Yuyutsu bows with folded hands as gold light gathers on him",
     "vo": [("build", [("दुर्योधन गुस्से से", "DURYODHAN GUSSE SE"),
                       ("चीख पड़ा।", "CHEEKH PADA"),
                       ("पर युधिष्ठिर बोले", "PAR YUDHISHTHIR BOLE"),
                       ("अब धृतराष्ट्र का वंश", "AB DHRITARASHTRA KA VANSH"),
                       ("तुमसे चलेगा।", "TUMSE CHALEGA")], 0.04)]},
    {"key": "payoff", "text": "BHEDI YA SAATHI",
     "visual": "Night after the war: a row of funeral pyres; Yuyutsu kneels and offers water from cupped hands; a torn "
               "red Kaurava banner glows on 'ghar ka bhedi', a saffron one on 'dharm ka saathi'; he looks up, and the "
               "frame dissolves into the opening shot",
     "vo": [("punch", [("और वही हुआ।", "AUR WAHI HUA"),
                       ("युद्ध के बाद", "YUDDH KE BAAD"),
                       ("भाइयों का अंतिम संस्कार", "BHAIYON KA ANTIM SANSKAR"),
                       ("उसी ने करवाया।", "USI NE KARWAYA"),
                       ("कोई उसे", "KOI USE"),
                       ("घर का भेदी कहता है", "GHAR KA BHEDI KEHTA HAI"),
                       ("और कोई धर्म का साथी।", "AUR KOI DHARM KA SAATHI"),
                       ("क्योंकि", "KYUNKI")], 0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "DHRITARASHTRA": hexc("#E0B0FF"), "SAU": hexc("#FF5555"), "MAARE": hexc("#FF5555"), "BACHA": GOLD_HI,
    "EK": GOLD_HI, "DUSHMAN": hexc("#FF8A80"), "YUYUTSU": hexc("#5FF0DC"), "DAASI": hexc("#FFCF99"),
    "BHEEM": hexc("#82C4FF"), "JAHAR": POISON, "BACHAYA": GOLD_HI, "KURUKSHETRA": FIRE_Y,
    "AAMNE": FIRE_Y, "SAAMNE": FIRE_Y, "SHANKH": GOLD_HI, "YUDHISHTHIR": hexc("#9CC8FF"), "PUKAARA": GOLD_HI,
    "CHUNEGA": GOLD_HI, "APNA": GOLD_HI, "KAURAV": hexc("#FF8A80"), "CHUP": hexc("#B0BEC5"),
    "AKELA": hexc("#5FF0DC"), "CHAL": hexc("#5FF0DC"), "DURYODHAN": hexc("#CE93D8"), "CHEEKH": hexc("#FF5555"),
    "VANSH": GOLD_HI, "TUMSE": GOLD_HI, "WAHI": GOLD_HI, "ANTIM": FIRE_Y, "SANSKAR": FIRE_Y,
    "BHEDI": hexc("#FF5555"), "DHARM": GOLD_HI, "SAATHI": GOLD_HI, "KYUNKI": hexc("#5FF0DC"),
})


def ease_in(u):
    u = clamp(u)
    return u * u


# ============================================================ scenery + props

def _hills(ctx, layers):
    for k, (c, yy, amp) in enumerate(layers):
        ctx.move_to(-80, yy)
        for x in range(-80, W + 81, 40):
            ctx.line_to(x, yy - amp * math.sin(x / (150 + 40 * k) + k * 2) - 14 * math.sin(x / 53 + k))
        ctx.line_to(W + 80, H)
        ctx.line_to(-80, H)
        ctx.close_path()
        rgba(ctx, hexc(c))
        ctx.fill()


def banner(ctx, x, y, h, c, t, lean=0.0, torn=False, a=1.0, glow_a=0.0):
    """Battle standard planted at (x, y): pole of height h leaning by lean (rad), pennant waving."""
    tx, ty = x + h * math.sin(lean), y - h * math.cos(lean)
    if glow_a > 0:
        glow(ctx, tx + 40, ty + 40, 160, c, 0.6 * glow_a)
    line(ctx, [(x, y), (tx, ty)], hexc("#2A160C"), 8, a)
    wave = 10 * math.sin(t * 4 + x)
    ctx.move_to(tx, ty)
    if torn:
        ctx.line_to(tx + 70 + wave, ty + 18)
        ctx.line_to(tx + 40, ty + 34)
        ctx.line_to(tx + 62 + wave, ty + 52)
        ctx.line_to(tx, ty + 60)
    else:
        ctx.curve_to(tx + 50, ty - 8 + wave, tx + 90, ty + 14 - wave, tx + 120 + wave, ty + 30)
        ctx.line_to(tx + 4, ty + 70)
    ctx.close_path()
    ink(ctx, c, 3, a)


def ashes_field(ctx, t, beam=0.0, beam_x=560, flag_glow=0.0):
    """Post-war dusk: ash-violet sky, low red sun, smoke columns, crows, a sea of fallen Kaurava banners."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in ((0.0, "#120E1E"), (0.28, "#2E2238"), (0.46, "#6A3A44"), (0.58, "#B8603A"), (0.70, "#4A2A26"),
                  (1.0, "#140C0C")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.paint()
    dv.stars(ctx, t, n=25, a=0.4)
    glow(ctx, 820, 880, 340, hexc("#FF5A2A"), 0.5)
    circle(ctx, 820, 880, 96, hexc("#FF8A5A"), 0.9)
    for k in range(3):                                    # drifting ash clouds
        x = ((t * (14 + 5 * k) + k * 420) % (W + 700)) - 350
        ell(ctx, x, 330 + k * 110, 280, 28)
        rgba(ctx, hexc("#3A2A34"), 0.7)
        ctx.fill()
    for i in range(6):                                    # crows circling
        ang = t * 0.6 + i * 1.05
        cx, cy = 560 + 300 * math.cos(ang) + 60 * i - 150, 420 + 70 * math.sin(ang * 1.3) + 25 * i
        flap = 10 * math.sin(t * 9 + i)
        line(ctx, [(cx - 18, cy - flap), (cx, cy), (cx + 18, cy - flap)], hexc("#120A10"), 4)
    _hills(ctx, (("#3A2432", 930, 50), ("#2A1824", 1000, 36), ("#1C1016", 1065, 24)))
    for i, sx in enumerate((160, 420, 700, 960)):         # smoke columns from the far field
        for k in range(9):
            u = ((t * 0.25 + k / 9 + rnd(i, 4)) % 1.0)
            circle(ctx, sx + 40 * math.sin(u * 5 + i) + 60 * u, 1000 - 600 * u, 26 + 70 * u, hexc("#4A3A44"),
                   0.35 * (1 - u))
    # Pandava saffron standard far left, on the hill
    banner(ctx, 120, 960, 230, PANDAV_SAFF, t, lean=0.05, glow_a=flag_glow)
    ctx.rectangle(-80, GROUND - 40, W + 160, H)
    rgba(ctx, hexc("#1E1012"))
    ctx.fill()
    if beam > 0:                                          # shaft of light on the lone survivor
        ctx.move_to(beam_x - 60, 0)
        ctx.line_to(beam_x + 60, 0)
        ctx.line_to(beam_x + 230, GROUND)
        ctx.line_to(beam_x - 230, GROUND)
        ctx.close_path()
        g = cairo.LinearGradient(0, 0, 0, GROUND)
        g.add_color_stop_rgba(0, *GOLD_HI, 0.0)
        g.add_color_stop_rgba(1, *GOLD_HI, 0.22 * beam)
        ctx.set_source(g)
        ctx.fill()
    # the sea of fallen Kaurava banners, helmets and broken spears
    for i in range(30):
        bx = -40 + (i * 41 + 300 * rnd(i, 7)) % (W + 80)
        by = GROUND - 60 + 120 * rnd(i, 8)
        if abs(bx - beam_x) < 120 and by > GROUND - 10:
            continue
        lean = (rnd(i, 9) - 0.5) * 2.2
        banner(ctx, bx, by, 90 + 70 * rnd(i, 10), KAURAV_RED, t * 0.2, lean=lean, torn=True, a=0.9)
    for i in range(10):
        hx, hy = 40 + i * 105 + 30 * rnd(i, 11), GROUND + 20 + 50 * rnd(i, 12)
        ctx.move_to(hx - 22, hy)
        ctx.curve_to(hx - 20, hy - 30, hx + 20, hy - 30, hx + 22, hy)
        ctx.close_path()
        ink(ctx, hexc("#7A4A22"), 3)
    ctx.arc(960, GROUND - 40, 62, 0, math.tau)            # broken chariot wheel
    rgba(ctx, hexc("#0E0608"))
    ctx.set_line_width(10)
    ctx.stroke()
    for k in range(5):
        a = k * math.pi / 5 + 0.4
        line(ctx, [(960, GROUND - 40), (960 + 62 * math.cos(a), GROUND - 40 + 62 * math.sin(a))], hexc("#0E0608"), 6)
    for i in range(26):                                   # embers / ash drifting up
        x = (rnd(i, 21) * W + 30 * math.sin(t * 1.5 + i)) % W
        y = H - 520 - ((t * (40 + 40 * rnd(i, 22)) + rnd(i, 23) * 1000) % 1000)
        circle(ctx, x, y, 2 + 3 * rnd(i, 24), EMBER, 0.45 * (0.5 + 0.5 * math.sin(t * 5 + i)))


def dawn_field(ctx, t, haze=0.0, armies=True):
    """Kurukshetra at dawn before the battle: 6-stop sky, rising sun, cloud bands, birds, 3 hills, far armies."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in ((0.0, "#141A3F"), (0.26, "#3B2A63"), (0.44, "#9A4A6A"), (0.56, "#F08A4B"), (0.66, "#FFC779"),
                  (0.80, "#7A4A2E"), (1.0, "#2A160E")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.paint()
    dv.stars(ctx, t, n=30, a=0.5)
    glow(ctx, 540, 860, 420, hexc("#FFD38A"), 0.6)
    circle(ctx, 540, 860, 92, hexc("#FFE6AE"))
    for k in range(4):
        x = ((t * (16 + 6 * k) + k * 300) % (W + 700)) - 350
        ell(ctx, x, 360 + k * 90, 250, 22)
        rgba(ctx, hexc("#6A3A5E"), 0.55)
        ctx.fill()
    for i in range(5):                                    # birds
        bx = (t * 60 + i * 190) % (W + 200) - 100
        by = 520 + 30 * math.sin(i * 2.1)
        flap = 9 * math.sin(t * 8 + i)
        line(ctx, [(bx - 14, by - flap), (bx, by), (bx + 14, by - flap)], hexc("#2A1626"), 3)
    _hills(ctx, (("#5A3550", 920, 50), ("#3F2238", 990, 36), ("#2A1626", 1050, 24)))
    if armies:                                            # far armies on the hills
        dv.army(ctx, -20, 420, 985, 11, hexc("#24121E"), t, PANDAV_SAFF, seed=3, a=0.8)
        dv.army(ctx, 660, 1100, 985, 11, hexc("#24121E"), t, KAURAV_RED, seed=4, a=0.8)
    ctx.rectangle(-80, GROUND - 40, W + 160, H)
    rgba(ctx, hexc("#3A2216"))
    ctx.fill()
    for i in range(36):                                   # grass tufts
        x = rnd(i, 9) * W
        y = GROUND - 30 + 70 * rnd(i, 10)
        line(ctx, [(x, y), (x - 6, y - 20)], hexc("#5A6A2A"), 4)
        line(ctx, [(x, y), (x + 6, y - 18)], hexc("#5A6A2A"), 4)
    for i in range(28):                                   # dust motes in the low sun
        x = (rnd(i, 3) * W + t * 30 * (0.5 + rnd(i, 4))) % W
        circle(ctx, x, 700 + 450 * rnd(i, 5), 2 + 3 * rnd(i, 6), hexc("#FFE0A8"), 0.25)
    if haze > 0:
        rgba(ctx, hexc("#FFB070"), 0.12 * haze)
        ctx.paint()


def palace_night(ctx, t):
    """Hastinapur hall by lamplight: arches, pillars, a moonlit window, hanging diyas, carpet."""
    palace(ctx, t)
    rrect(ctx, 760, 470, 200, 300, 90)                    # moon window in the back wall
    ink(ctx, hexc("#16224A"), 6, edge=GOLD_DK)
    circle(ctx, 880, 560, 42, hexc("#FFF7D6"))
    glow(ctx, 880, 560, 120, hexc("#CFE0FF"), 0.35)
    for i in range(3):                                    # flicker of torches
        fx = 90 + 450 * i
        f = 1 + 0.2 * math.sin(t * 11 + i)
        glow(ctx, fx, 700, 120 * f, FIRE_O, 0.35)
    ctx.rectangle(-80, GROUND - 20, W + 160, 60)
    rgba(ctx, hexc("#6A1A20"))
    ctx.fill()
    for k in range(12):
        line(ctx, [(-40 + 100 * k, GROUND - 14), (10 + 100 * k, GROUND + 30)], GOLD_DK, 4)


def throne_king(ctx, x, y, s, a):
    """Blind king on his throne as a backlit silhouette (Dhritarashtra), small, in the back of the hall."""
    if a <= 0:
        return

    glow(ctx, x, y - 420 * s, 520 * s, hexc("#FFB347"), 0.55 * a)     # lamplight behind the throne

    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)
        rrect(ctx, -170, -620, 340, 620, 60)
        ink(ctx, GOLD)
        smooth(ctx, [(-120, -620), (0, -760), (120, -620)], k=0.08)
        ink(ctx, GOLD)
        smooth(ctx, [(-110, -420), (110, -420), (140, -60), (-140, -60)])
        ink(ctx, hexc("#5A1B4F"))
        ell(ctx, 0, -500, 60, 66)
        ink(ctx, YD_SKIN)
        smooth(ctx, [(-60, -560), (-40, -620), (0, -640), (40, -620), (60, -560)], k=0.06)
        ink(ctx, GOLD)
        ctx.restore()
    dv.silhouette(ctx, draw, c=hexc("#1A0408"), a=0.9 * a)


def veiled_maid(ctx, x, y, s, a):
    if a <= 0:
        return
    glow(ctx, x, y - 420 * s, 480 * s, hexc("#FFB347"), 0.55 * a)
    dv.silhouette(ctx, lambda: mother(ctx, x, y, s, 0.0), c=hexc("#1A0408"), a=0.9 * a)


def poison_bowl(ctx, x, y, s, t, tilt=0.0, a=1.0):
    """Gold bowl brimming with glowing green poison, tilted by tilt."""
    glow(ctx, x, y - 20 * s, 110 * s, POISON, 0.45 * a)
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(tilt)
    ctx.scale(s, s)
    ell(ctx, 0, -18, 52, 14)
    ink(ctx, POISON, 3, a)
    ctx.move_to(-56, -18)
    ctx.curve_to(-50, 30, 50, 30, 56, -18)
    ctx.close_path()
    ink(ctx, dv.GOLD, 4, a)
    for k in range(3):                                    # rising fumes
        u = (t * 0.8 + k / 3) % 1.0
        circle(ctx, -20 + 20 * k + 8 * math.sin(t * 4 + k), -30 - 70 * u, 9 + 8 * u, POISON, 0.5 * (1 - u) * a)
    ctx.restore()


def pyre(ctx, x, y, s, t, i, lit=1.0):
    """Funeral pyre: stacked logs, flames and rising smoke (no bodies drawn)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for k in range(4):
        rrect(ctx, -110 + 8 * k, -24 - 24 * k, 220 - 16 * k, 22, 8)
        ink(ctx, hexc("#4A2A16"), 4)
    if lit > 0:
        f = 1 + 0.18 * math.sin(t * 12 + i * 2)
        glow(ctx, 0, -150, 200 * f * lit, FIRE_O, 0.55 * lit)
        for k in range(5):
            fx = -60 + 30 * k
            fh = (120 + 60 * rnd(k, i)) * lit * (1 + 0.2 * math.sin(t * 10 + k + i))
            smooth(ctx, [(fx - 26, -100), (fx, -100 - fh), (fx + 26, -100)], k=0.12)
            ink(ctx, FIRE_O if k % 2 else FIRE_Y, 2)
        for k in range(6):
            u = (t * 0.3 + k / 6 + rnd(i, 3)) % 1.0
            circle(ctx, 30 * math.sin(u * 6 + i) + 40 * u, -260 - 520 * u, 30 + 60 * u, hexc("#3A3040"), 0.4 * (1 - u))
    ctx.restore()


def night_pyres(ctx, t, lit=1.0):
    """Night after the war: violet-navy sky, moon, stars, hills and a row of burning pyres on the field."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in ((0.0, "#060818"), (0.30, "#141A3A"), (0.50, "#2E1E44"), (0.62, "#5A2A3A"), (0.76, "#1E1018"),
                  (1.0, "#0C0608")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.paint()
    dv.stars(ctx, t, n=70, a=0.9)
    glow(ctx, 860, 300, 200, hexc("#CFE0FF"), 0.3)
    circle(ctx, 860, 300, 64, hexc("#FFF7D6"))
    _hills(ctx, (("#2A1C34", 930, 46), ("#1E1428", 990, 32), ("#140C1A", 1050, 22)))
    for i, (px, py, ps) in enumerate(((620, 1010, 0.45), (820, 1000, 0.40), (1000, 1015, 0.42), (500, 1060, 0.55),
                                      (760, 1075, 0.62), (980, 1090, 0.6))):
        pyre(ctx, px, py, ps, t, i, lit)
    ctx.rectangle(-80, GROUND - 40, W + 160, H)
    rgba(ctx, hexc("#1A0E0E"))
    ctx.fill()
    glow(ctx, 800, GROUND - 60, 420, FIRE_O, 0.18 * lit)
    for i in range(30):
        x = (rnd(i, 31) * W + 25 * math.sin(t * 1.3 + i)) % W
        y = H - 560 - ((t * (50 + 40 * rnd(i, 32)) + rnd(i, 33) * 1000) % 1000)
        circle(ctx, x, y, 2 + 3 * rnd(i, 34), EMBER, 0.5 * (0.5 + 0.5 * math.sin(t * 6 + i)))


# ============================================================ crowd

def warrior(ctx, x, y, s, t, i, tunic, mode="stand", flip=False, a=1.0):
    """Small foot soldier (crowd unit), tunic colour per army. mode stand / look (staring, mouth open) / march."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(-s if flip else s, s)
    skin = hexc("#C98A5A")
    ph = t * 10 + i * 1.7
    walk = mode == "march"
    for side in (-1, 1):
        sw = 16 * math.sin(ph + (0 if side < 0 else math.pi)) if walk else 0
        limb(ctx, [(side * 14, -70), (side * 16 + sw, -34), (side * 14 + sw * 1.4, 0)], skin, 14)
    rrect(ctx, -26, -126, 52, 64, 12)
    ink(ctx, tunic, 4)
    line(ctx, [(-26, -70), (26, -70)], dv.GOLD, 5)
    limb(ctx, [(-22, -118), (-34, -84)], skin, 12)
    limb(ctx, [(22, -118), (36, -88)], skin, 12)
    line(ctx, [(40, -10), (44, -210)], hexc("#3B2516"), 5)
    ctx.move_to(44, -230)
    ctx.line_to(36, -206)
    ctx.line_to(52, -206)
    ctx.close_path()
    ink(ctx, hexc("#C8CCD4"), 2)
    ell(ctx, -36, -88, 22, 28)
    ink(ctx, hexc("#9A5A22"), 3)
    ell(ctx, 0, -150, 24, 26)
    ink(ctx, skin, 4)
    ctx.move_to(-27, -152)
    ctx.curve_to(-26, -190, 26, -190, 27, -152)
    ctx.close_path()
    ink(ctx, hexc("#9A5A22"), 3)
    up = mode == "look"
    for side in (-1, 1):
        circle(ctx, side * 9, -150, 5 if up else 3.5, dv.WHITE if up else dv.OUTLINE)
        if up:
            circle(ctx, side * 9 - 2, -150, 2.2, dv.OUTLINE)
    if up:
        ell(ctx, 0, -134, 5, 7)
        ink(ctx, hexc("#4A0A10"), 2)
    ctx.restore()


def pandava_mob(ctx, x0, x1, y, n, t, mode="stand", s=0.5, seed=0, a=1.0):
    """Two rows of saffron Pandava soldiers between x0 and x1 (back row smaller, 75 % alpha)."""
    span = x1 - x0
    for row, (dy, rs) in enumerate(((-36, s * 0.78), (0, s))):
        for i in range(n):
            xx = x0 + (i + 0.5 + 0.5 * row) / n * span + 14 * math.sin(seed + i * 3 + row)
            if row == 0:
                ctx.push_group()
            warrior(ctx, xx, y + dy, rs, t, i + 10 * row + seed, PANDAV_SAFF, mode=mode, flip=True)
            if row == 0:
                ctx.pop_group_to_source()
                ctx.paint_with_alpha(0.75 * a)


# ============================================================ characters

def yuyutsu(ctx, x, y, s, t, pose="stand", look=(0.0, 0.0), mood="calm", flip=False, a=1.0, aura=0.0, pour=0.0):
    """Yuyutsu, Dhritarashtra's son by a Vaishya maid: warm-brown skin, young clean-shaven face, high topknot under a
    low gold coronet with one teal gem, bare chest with a teal sash, deep-teal dhoti, silver bracers, sheathed sword.
    (Not a Duryodhan / Arjun clone: no tall mukut, no kavach, no quiver, no moustache.)
    Poses: stand / sad / walk / warn (stopping palm) / namaste / kneel / tarpan (kneeling, water from cupped hands,
    pour 0..1). mood calm / sad / resolve."""
    def draw():
        dv.place(ctx, x, y, s, t, flip)
        if aura > 0:
            glow(ctx, 0, -520, 460, GOLD_HI, 0.4 * aura)
        _yuyutsu_body(ctx, t, pose, look, mood, pour)
        ctx.restore()
    dv.group(ctx, a, draw)


def _yuyutsu_body(ctx, t, pose, look, mood, pour):
    skin = YU_SKIN
    kneel = pose in ("kneel", "tarpan")
    walk = pose == "walk"
    ph = t * 6.5
    drop = 240 if kneel else 0
    # long hair behind the head and shoulders
    ctx.save()
    ctx.translate(0, drop)
    smooth(ctx, [(-90, -720), (-112, -610), (-108, -520), (-78, -480), (78, -480), (108, -520), (112, -610),
                 (90, -720), (0, -790)])
    ink(ctx, dv.HAIR)
    ctx.restore()
    # legs
    if kneel:
        limb(ctx, [(50, -120), (175, -138)], skin, 50)            # front knee up
        limb(ctx, [(175, -138), (172, -30)], skin, 46)
        ell(ctx, 192, -14, 44, 16)
        ink(ctx, skin)
        limb(ctx, [(-50, -120), (-80, -24)], skin, 50)            # back knee on the ground
        limb(ctx, [(-80, -24), (-215, -18)], skin, 44)
        ell(ctx, -238, -16, 30, 14)
        ink(ctx, skin)
        smooth(ctx, [(-125, -170), (125, -170), (200, -150), (205, -100), (90, -90), (-60, -40), (-120, -60),
                     (-140, -110)])
        ink(ctx, YU_DHOTI)
        line(ctx, [(200, -102), (90, -94), (-60, -44)], dv.GOLD, 7)
    else:
        for k, side in enumerate((-1, 1)):
            sw = 60 * math.sin(ph + k * math.pi) if walk else 0
            lift = 26 * max(0.0, math.cos(ph + k * math.pi)) if walk else 0
            limb(ctx, [(side * 55, -340), (side * 58 + sw * 0.5, -178 - lift * 0.5), (side * 60 + sw, -34 - lift)],
                 skin, 48)
            ell(ctx, side * 66 + sw, -14 - lift, 42, 16)
            ink(ctx, skin)
            line(ctx, [(side * 60 + sw - 22, -44 - lift), (side * 60 + sw + 22, -44 - lift)], SILVER, 7)
        sway = 10 * math.sin(ph) if walk else 0
        smooth(ctx, [(-128, -370), (128, -370), (146, -250), (120 + sway, -165), (40, -185), (0, -150), (-40, -185),
                     (-120 + sway, -165), (-146, -250)])
        ink(ctx, YU_DHOTI)
        line(ctx, [(140, -244), (118 + sway, -170), (40, -190), (0, -156), (-40, -190), (-118 + sway, -170)],
             dv.GOLD, 7)
        smooth(ctx, [(-30, -360), (30, -360), (24 + sway, -170), (-24 + sway, -170)])     # pleated front fold
        ink(ctx, YU_SASH_DK, 3)
    ctx.save()
    ctx.translate(0, drop)
    lean = 0.04 * math.sin(ph * 2) if walk else 0.0
    ctx.rotate(lean)
    if not kneel:                                          # sheathed sword on the left hip (behind the arm)
        line(ctx, [(-96, -372), (-190, -150)], dv.OUTLINE, 26)
        line(ctx, [(-96, -372), (-190, -150)], hexc("#4A2A18"), 18)
        circle(ctx, -190, -150, 12, dv.GOLD)
        line(ctx, [(-120, -398), (-70, -376)], dv.GOLD, 12)
        line(ctx, [(-92, -390), (-80, -440)], hexc("#2A160C"), 12)
    # torso: slim bare chest, teal sash across, silver belt
    smooth(ctx, [(-130, -520), (-72, -546), (72, -546), (130, -520), (132, -440), (104, -356), (-104, -356),
                 (-132, -440)], k=0.12)
    ink(ctx, skin)
    sheen(ctx, -40, -480, 50, 26, 0.18)
    dk = shade(skin, 0.78)
    for side in (-1, 1):
        ctx.move_to(side * 100, -490)
        ctx.curve_to(side * 80, -455, side * 36, -452, side * 6, -466)
        rgba(ctx, dk)
        ctx.set_line_width(5)
        ctx.stroke()
    ctx.arc(0, -530, 60, 0.15 * math.pi, 0.85 * math.pi)  # thin gold chain + pendant
    rgba(ctx, dv.GOLD)
    ctx.set_line_width(6)
    ctx.stroke()
    gem(ctx, 0, -470, 9, YU_SASH)
    line(ctx, [(-118, -528), (112, -372)], dv.OUTLINE, 50)
    line(ctx, [(-118, -528), (112, -372)], YU_SASH, 40)
    line(ctx, [(-110, -536), (118, -382)], hexc("#7FE6D8"), 6)
    rrect(ctx, -116, -384, 232, 30, 10)
    ink(ctx, SILVER)
    gem(ctx, 0, -369, 11, YU_SASH)
    # arms
    L, R = (-130, -515), (130, -515)
    sw = 34 * math.sin(ph) if walk else 0
    if pose == "warn":
        arms = [(L, (-168, -410), (-110, -380)), (R, (240, -560), (330, -600))]
    elif pose in ("namaste", "kneel"):
        arms = [(L, (-150, -420), (-16, -478)), (R, (150, -420), (16, -478))]
    elif pose == "tarpan":
        arms = [(L, (-40, -420), (150, -452)), (R, (180, -430), (176, -456))]
    elif pose == "sad":
        arms = [(L, (-158, -400), (-140, -292)), (R, (158, -400), (140, -292))]
    elif walk:
        arms = [(L, (-162 + sw * 0.4, -410), (-150 + sw, -305)), (R, (162 - sw * 0.4, -410), (150 - sw, -305))]
    else:
        arms = [(L, (-170, -410), (-104, -384)), (R, (165, -410), (160, -305))]
    for sh, el, hd in arms:
        limb(ctx, [sh, el], skin, 44)
        limb(ctx, [el, hd], skin, 38)
        circle(ctx, lerp(sh[0], el[0], 0.5), lerp(sh[1], el[1], 0.5), 24, dv.GOLD)
        circle(ctx, lerp(sh[0], el[0], 0.5), lerp(sh[1], el[1], 0.5), 17, skin)
        line(ctx, [(lerp(el[0], hd[0], 0.35), lerp(el[1], hd[1], 0.35)),
                   (lerp(el[0], hd[0], 0.8), lerp(el[1], hd[1], 0.8))], dv.OUTLINE, 34)
        line(ctx, [(lerp(el[0], hd[0], 0.35), lerp(el[1], hd[1], 0.35)),
                   (lerp(el[0], hd[0], 0.8), lerp(el[1], hd[1], 0.8))], SILVER, 26)
    if pose == "warn":
        hand(ctx, -110, -380, skin, 24)
        palm(ctx, 336, -612, skin, ang=0.25, s=1.05)
    elif pose in ("namaste", "kneel"):
        smooth(ctx, [(-16, -470), (0, -540), (16, -470), (0, -455)], k=0.1)
        ink(ctx, skin)
    elif pose == "tarpan":
        ell(ctx, 170, -458, 40, 22)                        # cupped hands
        ink(ctx, skin)
        ell(ctx, 170, -468, 28, 8)
        rgba(ctx, hexc("#BFE6FF"), 0.9)
        ctx.fill()
        if pour > 0:
            pts = [(196 + 6 * math.sin(t * 9 + k), -458 + 52 * k * pour) for k in range(9) if -458 + 52 * k * pour < -drop - 12]
            if len(pts) > 1:
                line(ctx, pts, hexc("#BFE6FF"), 12, 0.85)
                line(ctx, pts, (1, 1, 1), 4, 0.7)
    else:
        for _, _, hd in arms:
            hand(ctx, *hd, skin, 24)
    for side in (-1, 1):                                   # sash knot / shoulder cloth
        ell(ctx, side * 128, -520, 30, 22)
        ink(ctx, YU_SASH_DK if side < 0 else skin)
    # neck + head
    rrect(ctx, -28, -605, 56, 72, 14)
    ink(ctx, skin)
    for side in (-1, 1):
        ell(ctx, side * 90, -688, 14, 24)
        ink(ctx, skin)
        ctx.arc(side * 92, -654, 11, 0, math.tau)
        rgba(ctx, dv.GOLD)
        ctx.set_line_width(5)
        ctx.stroke()
    circle(ctx, 0, -812, 44, dv.HAIR)                      # high topknot
    line(ctx, [(-40, -790), (40, -790)], YU_SASH, 10)
    ell(ctx, 0, -690, 90, 98)
    ink(ctx, skin)
    sheen(ctx, -32, -738, 32, 18, 0.18)
    smooth(ctx, [(-92, -690), (-84, -760), (-30, -790), (30, -790), (84, -760), (92, -690), (66, -732), (0, -750),
                 (-66, -732)], k=0.12)
    ink(ctx, dv.HAIR)
    # low gold coronet with three small points and one teal gem
    smooth(ctx, [(-86, -748), (-54, -786), (-30, -762), (0, -800), (30, -762), (54, -786), (86, -748)], k=0.06)
    ink(ctx, dv.GOLD, 4)
    rrect(ctx, -90, -764, 180, 22, 8)
    ink(ctx, dv.GOLD, 4)
    gem(ctx, 0, -770, 10, YU_SASH)
    line(ctx, [(0, -726), (0, -708)], hexc("#F4E6C8"), 6)  # sandal tilak
    # brows by mood
    for side in (-1, 1):
        if mood == "sad":
            line(ctx, [(side * 62, -716), (side * 18, -732)], dv.HAIR, 9)
        elif mood == "resolve":
            line(ctx, [(side * 64, -734), (side * 18, -722)], dv.HAIR, 10)
        else:
            line(ctx, [(side * 62, -728), (side * 18, -726)], dv.HAIR, 9)
        eye(ctx, side * 36, -694, 20, 22, t, look=look, seed=9, iris=hexc("#2E1A0E"),
            lid=0.25 if mood == "sad" else 0.0, skin=skin)
    ell(ctx, 0, -662, 9, 14)
    ink(ctx, shade(skin, 0.86), 3)
    if mood == "sad":
        line(ctx, [(-20, -628), (0, -634), (20, -628)], dv.OUTLINE, 5)
    else:
        line(ctx, [(-20, -634), (0, -628), (20, -634)], dv.OUTLINE, 5)
    ctx.restore()


def yudhishthir(ctx, x, y, s, t, pose="stand", look=(0.0, 0.0), speak=0.0, flip=False, a=1.0, aura=0.0):
    """Yudhishthir (Dharmaraj): ivory robes with a sky-blue uttariya, rounded pearl-strung mukut, short black beard,
    calm brows, spear planted at his side. Poses: stand (hand on spear) / call (both arms flung open) /
    welcome (arm reaching out low, to a shoulder) / bless."""
    def draw():
        dv.place(ctx, x, y, s, t, flip)
        if aura > 0:
            glow(ctx, 0, -560, 420, GOLD_HI, 0.35 * aura)
        _yudhishthir_body(ctx, t, pose, look, speak)
        ctx.restore()
    dv.group(ctx, a, draw)


def _yudhishthir_body(ctx, t, pose, look, speak):
    skin = YD_SKIN
    for side in (-1, 1):                                   # hair to the shoulders
        smooth(ctx, [(side * 70, -720), (side * 122, -620), (side * 128, -520), (side * 98, -500), (side * 84, -600)])
        ink(ctx, dv.HAIR)
    line(ctx, [(-190, -20), (-190, -880)], dv.OUTLINE, 20)  # spear planted at his side
    line(ctx, [(-190, -20), (-190, -880)], hexc("#6A4222"), 12)
    ctx.move_to(-190, -940)
    ctx.curve_to(-170, -900, -170, -880, -190, -860)
    ctx.curve_to(-210, -880, -210, -900, -190, -940)
    ink(ctx, hexc("#D8DEE6"), 4)
    line(ctx, [(-212, -858), (-168, -858)], dv.GOLD, 10)
    for side in (-1, 1):
        ell(ctx, side * 60, -14, 42, 16)
        ink(ctx, skin)
    smooth(ctx, [(-120, -380), (120, -380), (150, -200), (150, -40), (0, -30), (-150, -40), (-150, -200)])
    ink(ctx, YD_ROBE)                                       # long ivory dhoti to the ankles
    line(ctx, [(-148, -48), (0, -38), (148, -48)], YD_BLUE, 12)
    line(ctx, [(0, -370), (0, -40)], shade(YD_ROBE, 0.85), 5)
    smooth(ctx, [(-138, -522), (-72, -548), (72, -548), (138, -522), (140, -440), (112, -362), (-112, -362),
                 (-140, -440)], k=0.12)
    ink(ctx, YD_ROBE)
    for side in (-1, 1):                                   # sky-blue uttariya over both shoulders
        line(ctx, [(side * 120, -530), (side * 30, -380)], dv.OUTLINE, 42)
        line(ctx, [(side * 120, -530), (side * 30, -380)], YD_BLUE, 32)
    dv.pearls(ctx, [(64 * math.cos(a), -530 + 56 * math.sin(a)) for a in [math.pi * (0.15 + 0.07 * k) for k in range(11)]],
              r=6)
    gem(ctx, 0, -470, 12, YD_BLUE)
    rrect(ctx, -122, -392, 244, 30, 10)
    ink(ctx, dv.GOLD)
    L, R = (-138, -515), (138, -515)
    if pose == "call":
        arms = [(L, (-250, -600), (-320, -710)), (R, (250, -600), (320, -710))]
    elif pose == "welcome":
        arms = [(L, (-196, -430), (-190, -470)), (R, (230, -470), (330, -470))]
    elif pose == "bless":
        arms = [(L, (-196, -430), (-190, -470)), (R, (220, -560), (232, -660))]
    else:
        arms = [(L, (-196, -430), (-190, -470)), (R, (170, -410), (150, -318))]
    for sh, el, hd in arms:
        limb(ctx, [sh, el], skin, 46)
        limb(ctx, [el, hd], skin, 40)
        circle(ctx, lerp(sh[0], el[0], 0.5), lerp(sh[1], el[1], 0.5), 25, dv.GOLD)
        circle(ctx, lerp(sh[0], el[0], 0.5), lerp(sh[1], el[1], 0.5), 18, skin)
        line(ctx, [(lerp(el[0], hd[0], 0.7) - 14, lerp(el[1], hd[1], 0.7)),
                   (lerp(el[0], hd[0], 0.7) + 14, lerp(el[1], hd[1], 0.7))], dv.GOLD, 12)
    if pose == "call":
        palm(ctx, -324, -722, skin, ang=-0.5, s=1.05)
        palm(ctx, 324, -722, skin, ang=0.5, s=1.05)
    elif pose == "bless":
        hand(ctx, -190, -470, skin, 26)
        palm(ctx, 232, -672, skin, ang=0.1, s=1.05)
    else:
        for _, _, hd in arms:
            hand(ctx, *hd, skin, 26)
    for side in (-1, 1):
        ell(ctx, side * 136, -520, 34, 24)
        ink(ctx, YD_BLUE)
    rrect(ctx, -30, -606, 60, 72, 14)
    ink(ctx, skin)
    for side in (-1, 1):
        ell(ctx, side * 94, -690, 15, 25)
        ink(ctx, skin)
        circle(ctx, side * 96, -652, 12, dv.GOLD)
    ell(ctx, 0, -692, 94, 102)
    ink(ctx, skin)
    sheen(ctx, -32, -742, 32, 18, 0.18)
    smooth(ctx, [(-80, -660), (-70, -610), (-36, -582), (0, -576), (36, -582), (70, -610), (80, -660), (40, -626),
                 (0, -620), (-40, -626)], k=0.12)
    ink(ctx, dv.HAIR)                                       # short beard
    # rounded pearl-strung mukut
    smooth(ctx, [(-98, -766), (-94, -830), (-60, -872), (0, -892), (60, -872), (94, -830), (98, -766)], k=0.1)
    ink(ctx, dv.GOLD, 5)
    for k in range(-2, 3):
        dv.pearls(ctx, [(k * 30, -790 - 18 * j) for j in range(4 - abs(k))], r=6)
    rrect(ctx, -102, -780, 204, 26, 8)
    ink(ctx, dv.GOLD, 5)
    gem(ctx, 0, -846, 13, YD_BLUE)
    for side in (-1, 1):
        line(ctx, [(side * 64, -734), (side * 20, -732)], dv.HAIR, 9)
        eye(ctx, side * 37, -700, 20, 21, t, look=look, seed=3, iris=hexc("#2A1A10"))
    ell(ctx, 0, -668, 10, 15)
    ink(ctx, shade(skin, 0.86), 3)
    for side in (-1, 1):                                   # moustache
        smooth(ctx, [(side * 4, -640), (side * 40, -646), (side * 56, -632), (side * 30, -632)], k=0.12)
        ink(ctx, dv.HAIR, 3)
    if speak > 0.05:
        ell(ctx, 0, -616, 20, 6 + 12 * speak)
        ink(ctx, hexc("#4A0A10"), 4)
    else:
        line(ctx, [(-18, -620), (0, -614), (18, -620)], dv.OUTLINE, 5)


# ============================================================ scenes

class Hook(Cued):
    """Lone survivor among the fallen banners; light finds him on 'bacha', he turns to the saffron flag on
    'dushman ki taraf' and walks towards it on 'chala gaya'."""

    def beats(self, d):
        return {"bacha": self.cue("BACHA", d * 0.36), "dushman": self.cue("DUSHMAN", d * 0.54),
                "chala": self.cue("CHALA GAYA", d * 0.72)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["bacha"], "shimmer"), (b["dushman"], "whoosh"), (b["chala"] + 0.1, "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        beam = 0.45 + 0.55 * clamp((t - b["bacha"]) / 0.5)
        walk_u = ease_in_out(clamp((t - b["chala"]) / 1.6))
        x = lerp(600, 470, walk_u)
        ashes_field(ctx, t, beam=beam, beam_x=x, flag_glow=clamp((t - b["dushman"]) / 0.5))
        if t < b["dushman"]:
            pose, look, mood = "sad", (0.0, 0.7) if t < b["bacha"] else (0.0, -0.2), "sad"
        elif t < b["chala"]:
            pose, look, mood = "stand", (-0.9, -0.1), "resolve"
        else:
            pose, look, mood = ("walk" if walk_u < 1 else "stand"), (-0.9, 0.0), "resolve"
        yuyutsu(ctx, x, GROUND - 10, 0.76, t, pose=pose, look=look, mood=mood, aura=0.3 * beam)
        for i, (fx, fl) in enumerate(((330, -0.9), (820, 0.8), (240, 0.6))):   # fallen banners in front of him
            banner(ctx, fx, GROUND + 60, 120, KAURAV_RED, t * 0.2, lean=fl, torn=True)


class Kaun(Cued):
    """Palace: who he was (blind king + maid silhouettes), then Duryodhan's poison bowl - Yuyutsu stops it."""

    def beats(self, d):
        return {"daasi": self.cue("DAASI", d * 0.36), "bheem": self.cue("BHEEM", d * 0.54),
                "jahar": self.cue("JAHAR", d * 0.72)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["daasi"], "ghanti"), (b["bheem"], "whoosh"), (b["jahar"] + 0.3, "pop"),
                (b["jahar"] + 0.9, "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        palace_night(ctx, t)
        lineage = clamp(t / 0.4) * (1 - clamp((t - b["bheem"]) / 0.5))
        throne_king(ctx, 200, GROUND - 70, 0.55, lineage)
        veiled_maid(ctx, 1000, GROUND - 70, 0.55, clamp((t - b["daasi"]) / 0.4) * (1 - clamp((t - b["bheem"]) / 0.5)))
        enter = ease_out_cubic(clamp((t - b["bheem"]) / 0.7))
        dx = lerp(1300, 870, enter)
        knock = b["jahar"] + 0.3
        stopped = t >= knock
        if t >= b["bheem"]:
            duryodhan(ctx, dx, GROUND - 10, 0.72, t, pose="panic" if stopped else "point",
                      shout=0.0 if stopped else 0.3, look=(-0.6, 0.0) if not stopped else (-0.3, 0.5), flip=True)
            hx, hy = dx - 360 * 0.72, GROUND - 10 - 610 * 0.72
            if not stopped:
                poison_bowl(ctx, hx, hy - 20, 1.0, t)
            else:
                u = clamp((t - knock) / 0.55)
                bx, by = lerp(hx, hx + 60, u), hy - 20 + (GROUND - 30 - hy) * u * u
                if u < 1:
                    poison_bowl(ctx, bx, by, 1.0, t, tilt=2.6 * u)
                else:
                    poison_bowl(ctx, hx + 60, GROUND - 20, 0.9, t, tilt=2.6, a=0.8)
                    for k in range(6):                     # spilled poison fizzles away on the floor
                        v = ((t - knock) * 0.9 + k / 6) % 1.0
                        circle(ctx, hx + 20 + 18 * k, GROUND - 20 - 120 * v, 12 + 14 * v, POISON, 0.45 * (1 - v))
        step = ease_out_cubic(clamp((t - knock + 0.25) / 0.4))
        yx = lerp(360, 410, step)
        if t < b["bheem"]:
            pose, look, mood = "stand", (0.0, 0.0), "calm"
        elif not stopped:
            pose, look, mood = "stand", (0.8, 0.0), "resolve"
        else:
            pose, look, mood = "warn", (0.8, 0.0), "resolve"
        yuyutsu(ctx, yx, GROUND - 10, 0.74, t, pose=pose, look=look, mood=mood)


class Senayein(Cued):
    """Wide dawn shot: both armies march in from the edges and halt face to face; conches are lifted."""

    def beats(self, d):
        return {"aamne": self.cue("AAMNE", d * 0.36), "shankh": self.cue("SHANKH", d * 0.54)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "whoosh")] + [(0.3 + 0.45 * k, "soft_thud") for k in range(5)] + \
               [(b["aamne"] + 0.4, "thud"), (b["shankh"] + 0.3, "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dawn_field(ctx, t)
        u = ease_out_cubic(clamp(t / (b["aamne"] + 0.6)))
        marching = u < 0.98
        off = lerp(520, 0, u)
        glow(ctx, 540, GROUND - 40, 160, GOLD_HI, 0.25 * u)          # the empty strip between them
        for side, c, bx in ((-1, PANDAV_SAFF, 150), (1, KAURAV_RED, 930)):
            ctx.save()
            ctx.translate(side * off, 0)
            banner(ctx, bx, GROUND - 60, 300, c, t, lean=0.03 * side)
            if side < 0:
                pandava_mob(ctx, 0, 420, GROUND - 40, 6, t, mode="march" if marching else "stand", s=0.52, seed=2)
                yudhishthir(ctx, 400, GROUND - 10, 0.32, t, pose="stand", look=(0.8, 0.0))
            else:
                kaurava_mob(ctx, 660, 1080, GROUND - 40, 6, t, mode="stand", s=0.52, seed=6)
                yuyutsu(ctx, 690, GROUND - 10, 0.31, t, pose="walk" if marching else "stand", look=(-0.8, 0.0),
                        mood="calm", flip=True)
                duryodhan(ctx, 860, GROUND - 10, 0.33, t, pose="point", shout=0.0, look=(-0.6, 0.0), flip=True)
            ctx.restore()
            if marching:
                dust_cloud(ctx, 540 + side * (300 + off), GROUND - 10, 0.5, 240, seed=3 + side, a=0.35)
        lift = ease_out_back(clamp((t - b["shankh"]) / 0.5))
        if lift > 0:
            for k, (cx, cy) in enumerate(((330, GROUND - 175), (760, GROUND - 175))):
                yy = cy - 50 * lift
                glow(ctx, cx, yy, 70, GOLD_HI, 0.6 * lift)
                ell(ctx, cx, yy, 30, 18, 0.5 if k == 0 else -0.5)
                ink(ctx, hexc("#FFF6E6"), 3)
                for r in range(2):                                  # anticipation shimmer rings
                    rr = 40 + 40 * (((t - b["shankh"]) * 1.2 + r * 0.5) % 1.0)
                    ctx.arc(cx, yy, rr, 0, math.tau)
                    rgba(ctx, GOLD_HI, 0.5 * (1 - (rr - 40) / 40))
                    ctx.set_line_width(4)
                    ctx.stroke()


class Pukaar(Cued):
    """Yudhishthir flings his arms open and calls; golden rings roll out; one prince far off looks up."""

    def beats(self, d):
        return {"pukaara": self.cue("PUKAARA", d * 0.18), "chunega": self.cue("CHUNEGA", d * 0.45),
                "apna": self.cue("APNA", d * 0.68)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["pukaara"], "whoosh"), (b["pukaara"] + 0.2, "boom"),
                (b["chunega"] + 0.2, "shimmer"), (b["apna"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dawn_field(ctx, t, haze=0.6, armies=False)
        kaurava_mob(ctx, 600, 1080, GROUND - 150, 7, t, mode="look" if t > b["pukaara"] + 0.3 else "stand",
                    s=0.42, seed=11)
        noticed = clamp((t - b["chunega"]) / 0.4)
        if noticed > 0:
            glow(ctx, 820, GROUND - 260, 120, YU_SASH, 0.6 * noticed)
        yuyutsu(ctx, 820, GROUND - 140, 0.30, t, pose="stand", look=(-0.9, -0.2) if noticed > 0 else (0.0, 0.3),
                mood="resolve" if noticed > 0 else "calm")
        banner(ctx, 90, GROUND - 20, 380, PANDAV_SAFF, t)
        calling = t >= b["pukaara"]
        if calling:                                          # golden call rings rolling across the field
            for k in range(4):
                u = ((t - b["pukaara"]) * 0.7 + k * 0.25) % 1.0
                ctx.arc(330, GROUND - 560, 120 + 700 * u, -0.5, 0.5)
                rgba(ctx, GOLD_HI, 0.55 * (1 - u))
                ctx.set_line_width(8)
                ctx.stroke()
        pose = "welcome" if t >= b["apna"] else ("call" if calling else "stand")
        speak = 0.4 + 0.6 * abs(math.sin(t * 8)) if calling else 0.0
        yudhishthir(ctx, 330, GROUND - 10, 0.76, t, pose=pose, look=(0.8, 0.0), speak=speak,
                    aura=0.4 if calling else 0.0)


class Chala(Cued):
    """Low side shot: silent Kaurava ranks; Yuyutsu steps out alone and walks across towards the Pandava line."""

    def beats(self, d):
        return {"chup": self.cue("CHUP", d * 0.2), "ek": self.cue("EK YODHA", d * 0.45),
                "paar": self.cue("US PAAR", d * 0.68)}

    def events(self, d):
        b = self.beats(d)
        ev = [(0.02, "soft_thud"), (b["ek"], "whoosh")]
        ev += [(b["ek"] + 0.3 + 0.48 * k, "tock") for k in range(6)]
        return ev

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dawn_field(ctx, t, haze=0.3, armies=False)
        pandava_mob(ctx, -20, 260, GROUND - 90, 4, t, s=0.45, seed=7)
        banner(ctx, 60, GROUND - 120, 260, PANDAV_SAFF, t)
        banner(ctx, 1010, GROUND - 60, 300, KAURAV_RED, t * 0.5, lean=0.06)
        kaurava_mob(ctx, 640, 1080, GROUND - 40, 6, t, mode="look" if t > b["chup"] else "stand", s=0.55, seed=9)
        u = clamp((t - b["ek"]) / (d * 0.97 - b["ek"]))
        x = lerp(820, 460, u)
        moving = 0 < u < 1
        if moving:
            for k in range(5):                               # dust puff behind every step
                px = x + 60 + 70 * k
                if px < 840:
                    circle(ctx, px, GROUND - 6, 18 + 6 * k, hexc("#B08A6A"), 0.3 * (1 - k / 5))
        yuyutsu(ctx, x, GROUND - 10, 0.74, t, pose="walk" if moving else "stand",
                look=(-0.9, 0.0) if u > 0 else (-0.3, 0.1), mood="resolve", flip=True)


class Cheekh(Cued):
    """Duryodhan erupts (left); Yudhishthir's hand on Yuyutsu's shoulder (right), Yuyutsu bows - gold gathers."""

    def beats(self, d):
        return {"cheekh": self.cue("CHEEKH", d * 0.18), "bole": self.cue("BOLE", d * 0.36),
                "vansh": self.cue("VANSH", d * 0.54)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["cheekh"], "whoosh"), (b["cheekh"] + 0.1, "boom"), (b["bole"], "soft_thud"),
                (b["vansh"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        u = t - b["cheekh"]
        shake = 10 * math.exp(-u * 5) if u > 0 else 0
        ctx.save()
        ctx.translate(shake * math.sin(t * 47), shake * math.cos(t * 41))
        dawn_field(ctx, t, armies=True)
        rage = clamp(u / 0.3) if u > 0 else 0
        glow(ctx, 175, GROUND - 420, 380, hexc("#FF2A1A"), 0.35 * rage)
        blessed = clamp((t - b["vansh"]) / 0.6)
        glow(ctx, 620, GROUND - 400, 360, GOLD_HI, 0.35 * blessed)
        shouting = u > 0
        duryodhan(ctx, 175, GROUND - 10, 0.70, t, pose="point" if shouting else "panic",
                  shout=0.4 + 0.6 * abs(math.sin(t * 9)) if shouting else 0.0,
                  look=(0.8, 0.0) if shouting else (0.4, -0.3))
        welcomed = t >= b["bole"]
        yuyutsu(ctx, 620, GROUND - 10, 0.70, t, pose="namaste" if welcomed else "stand",
                look=(0.7, 0.0) if welcomed else (-0.8, 0.0), mood="calm" if welcomed else "resolve",
                aura=0.6 * blessed)
        yudhishthir(ctx, 920, GROUND - 10, 0.74, t, pose="welcome" if welcomed else "stand", look=(-0.8, 0.1),
                    speak=0.4 + 0.6 * abs(math.sin(t * 7)) if welcomed and t < d * 0.95 else 0.0, flip=True)
        if blessed > 0:
            dv.petals(ctx, t, n=18, seed=2, a=0.7 * blessed)
        ctx.restore()


class Payoff(Cued):
    """Pyres at night: Yuyutsu kneels and gives water (last rites). Red banner glows on 'ghar ka bhedi', saffron on
    'dharm ka saathi'; he looks up on 'kyunki' and the last 0.45 s dissolve into the hook's first frame."""

    def beats(self, d):
        return {"wahi": self.cue("WAHI", 0.0), "sanskar": self.cue("SANSKAR", d * 0.25),
                "bhedi": self.cue("BHEDI", d * 0.56), "saathi": self.cue("SAATHI", d * 0.67),
                "kyunki": self.cue("KYUNKI", d * 0.79)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "soft_thud"), (b["sanskar"], "shimmer"), (b["bhedi"], "thud"), (b["saathi"], "ghanti"),
                (b["kyunki"], "whoosh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_pyres(ctx, t, lit=0.5 + 0.5 * clamp(t / 0.8))
        red = clamp((t - b["bhedi"]) / 0.4) * (1 - 0.6 * clamp((t - b["saathi"]) / 0.4))
        gold = clamp((t - b["saathi"]) / 0.4)
        banner(ctx, 90, GROUND - 30, 330, KAURAV_RED, t, lean=-0.12, torn=True, glow_a=red)
        banner(ctx, 560, GROUND - 30, 330, PANDAV_SAFF, t, lean=0.08, glow_a=gold)
        if red > 0:
            glow(ctx, 140, 760, 520, hexc("#FF2A2A"), 0.45 * red)
        if gold > 0:
            glow(ctx, 600, 760, 520, GOLD_HI, 0.4 * gold)
        giving = t >= b["sanskar"]
        pour = clamp((t - b["sanskar"]) / 0.5) if giving else 0.0
        look = (0.0, -0.1) if t >= b["kyunki"] else ((0.8, 0.2) if giving else (0.3, 0.6))
        yuyutsu(ctx, 300, GROUND - 10, 0.76, t, pose="tarpan" if giving else "kneel", look=look,
                mood="sad" if t < b["kyunki"] else "resolve", pour=pour, aura=0.25 + 0.3 * gold)
        x = clamp((t - (d - 0.45)) / 0.45)
        if x > 0:
            ctx.push_group()
            Hook().draw(ctx, 0.0, d)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(x)


SCENE_CLASSES = {"hook": Hook, "kaun": Kaun, "senayein": Senayein, "pukaar": Pukaar, "chala": Chala,
                 "cheekh": Cheekh, "payoff": Payoff}


# ============================================================ thumbnail + upload kit

def thumbnail(ctx):
    dawn_field(ctx, 0.4, armies=False)
    glow(ctx, 270, 1000, 420, hexc("#FF2A1A"), 0.35)       # red Kaurava side / gold Pandava side
    glow(ctx, 820, 1000, 420, GOLD_HI, 0.35)
    kaurava_mob(ctx, 600, 1080, 1180, 6, 0.3, mode="look", s=0.55, seed=9)
    pandava_mob(ctx, -20, 330, 1130, 4, 0.3, s=0.48, seed=7)
    banner(ctx, 990, 1140, 330, KAURAV_RED, 0.3, lean=0.06)
    banner(ctx, 70, 1100, 300, PANDAV_SAFF, 0.3)
    duryodhan(ctx, 930, 1150, 0.44, 0.3, pose="point", shout=1.0, look=(-0.7, 0.0), flip=True)
    yuyutsu(ctx, 520, 1260, 0.84, 0.35, pose="walk", look=(-0.9, 0.0), mood="resolve", flip=True, aura=0.6)
    g = cairo.LinearGradient(0, 0, 0, 560)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.9)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 560)
    ctx.set_source(g)
    ctx.fill()
    g = cairo.LinearGradient(0, 1380, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.9)
    ctx.rectangle(0, 1380, W, H - 1380)
    ctx.set_source(g)
    ctx.fill()
    text(ctx, "BHEDI YA", 540, 220, 140, hexc("#FF4A3A"), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
         stroke_w=22)
    text(ctx, "SAATHI?", 540, 370, 140, FIRE_Y, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
         stroke_w=20)
    text(ctx, "DIVYA RAHASYA", 540, 1820, 42, GOLD_HI, a=0.85)


UPLOAD = {
    "thumb_text": "BHEDI YA SAATHI?",
    "titles": [
        "Dhritarashtra Ke 100 Bete Mare, Bacha Sirf Yuyutsu #shorts",
        "Yuyutsu: Wo Kaurav Jo Pandavon Ki Taraf Chala Gaya",
        "Yuyutsu Ghar Ka Bhedi Tha Ya Dharm Ka Saathi?",
        "Mahabharat Ka Akela Kaurav Jo Yuddh Ke Baad Zinda Bacha",
        "Yudhishthir Ki Ek Pukaar Aur Yuyutsu Ne Paksh Badal Liya",
        "Duryodhan Ka Bhai Jo Pandavon Se Mil Gaya: Yuyutsu",
        "Kaurav Sena Chup Rahi, Sirf Yuyutsu Aage Badha",
        "Yuyutsu Ki Kahani: Dhritarashtra Ka 101va Beta",
        "Kurukshetra Shuru Hone Se Pehle Kisne Paksh Badla?",
        "Yuyutsu Kaun Tha? Mahabharat Ka Anjaan Yoddha",
    ],
    "queries": [
        "yuyutsu kaun tha",
        "yuyutsu mahabharat",
        "dhritarashtra ke 100 bete",
    ],
    "description": (
        "Yuyutsu kaun tha? Dhritarashtra ke sau bete Kurukshetra mein maare gaye - bacha sirf Yuyutsu, "
        "Dhritarashtra aur ek Vaishya daasi ka beta, jo yuddh shuru hone se theek pehle Kaurav sena chhodkar "
        "Pandavon ki taraf chala gaya tha.\n\n"
        "Is Short mein:\n"
        "- Yudhishthir ki pukaar: 'jo humein chunega, hum use apna lenge'\n"
        "- Poori Kaurav sena chup, sirf Yuyutsu akela us paar gaya\n"
        "- Yudhishthir ne kaha: Dhritarashtra ka vansh aur pind ab tum par hai\n"
        "- Yuddh ke baad apne bhaiyon ka antim sanskar usi ne karwaya\n\n"
        "Source: Mahabharat - Bhishma Parva (adhyay 43, paksh badalna), Adi Parva (janm), Stri Parva "
        "(antim sanskar), Mahaprasthanika Parva (Pandavon ke jaane par rajya ki dekh-rekh Yuyutsu ko). "
        "Kuch sanskaranon mein ye bhi kaha jaata hai ki Yuyutsu ne Bheem ko Duryodhan ki zeher wali saazish se "
        "bachaya tha - ye ek variant kahani hai, mool granth mein spasht nahi.\n\n"
        "Aapki raay: Yuyutsu ghar ka bhedi tha ya dharm ka saathi? Comment mein batao.\n\n"
        "#Shorts #Mahabharat #Yuyutsu #Kurukshetra #Yudhishthir"
    ),
    "tags": ["yuyutsu", "yuyutsu mahabharat", "yuyutsu story", "kaurav", "pandav", "yudhishthir", "duryodhan",
             "dhritarashtra", "kurukshetra", "mahabharat shorts", "mahabharat facts", "hindu mythology",
             "divya rahasya"],
    "hashtags": ["#Shorts", "#Mahabharat", "#Yuyutsu"],
    "pinned_comment": "Yuyutsu ghar ka bhedi tha ya dharm ka saathi? Aapka jawab 👇",
}
