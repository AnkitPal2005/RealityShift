"""Hanuman Ji Aur Tooti Cycle (Karm Aur Kripa): on a lonely night, a boy returning home with his mother's medicine
has his bicycle chain snap in the dark; with an empty pocket and a dead phone, he recites Hanuman Chalisa and keeps
walking with the broken cycle; an elder in a red gamchha appears, fixes the chain in two minutes without a word, and
vanishes leaving only the shadow of Hanuman ji's gada (~28 s, 9 scenes). Kalpanik prerak katha.

Usage (from SanatanKatha/):
  python make.py hanuman_cycle --preview
  python make.py hanuman_cycle --kiki-split --check-voice
  python make.py hanuman_cycle --engine files
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

from kathas.daadi_morpankh import boy, phone, GOLDEN, FEET
from kathas.eklavya_krishna import sparkle_burst
from kathas import panchmukhi as pm

TOPIC = "KARM AUR KRIPA HANUMAN JI TOOTI CYCLE RAAT BABA GADA CHHAYA"
OUTPUTS = {"edge": "hanuman_cycle_short.mp4"}
MUSIC_STYLE = "ambient"
MUSIC_BPM = 86
MUSIC_VOLUME = 0.11
TAIL_PAD = 0.35
MAX_GAP = 0.45
SCENE_WHOOSH = False
SFX_SCALE = 0.5

SAFF = hexc("#FF7A18")
RED_THREAD = hexc("#E02828")
SKIN = hexc("#D8A070")
SOURCES = [
    "Original fictional story (Kalpanik prerak katha) - no scripture or real-event claim; labelled in the description.",
    "Hanuman ji's form (sindoori, mukut, gada, abhaya) and red kalawa follow common bhakti iconography.",
]

S = 0.72


# =============================================================================
# Camera helper (zoom/pan around any focal point)
# =============================================================================
def cam_begin(ctx, cx, cy, zoom, tx=W / 2, ty=H * 0.55):
    ctx.save()
    ctx.translate(tx, ty)
    ctx.scale(zoom, zoom)
    ctx.translate(-cx, -cy)


def cam_end(ctx):
    ctx.restore()


# =============================================================================
# Places and props
# =============================================================================
def night_road(ctx, t, scroll=0.0, mandir=True, mist=0.35):
    """Lonely moonlit highway with trees, streetlamp, roadside Hanuman mandir, and asphalt road."""
    g = cairo.LinearGradient(0, -160, 0, GROUND)
    for at, c in ((0.0, "#080E20"), (0.55, "#162242"), (1.0, "#2A3A5C")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.rectangle(-250, -250, W + 500, GROUND + 300)
    ctx.fill()

    glow(ctx, 840, 290, 170, hexc("#FFF4CC"), 0.25)
    circle(ctx, 840, 290, 58, hexc("#FFF6D8"))

    for k in range(28):
        sx = (k * 173 + 40) % W
        sy = 80 + (k * 89) % 420
        circle(ctx, sx, sy, 2.2, (1, 1, 1), 0.4 + 0.4 * math.sin(t * 2 + k))

    pts = [(-250, GROUND - 200)]
    for k in range(12):
        pts.append((-250 + k * 145, GROUND - 240 - 60 * math.sin(k * 1.1 + scroll * 0.4)))
    pts.append((W + 250, GROUND - 200))
    pts.append((W + 250, GROUND))
    pts.append((-250, GROUND))
    smooth(ctx, pts, k=0.35)
    rgba(ctx, hexc("#10182C"))
    ctx.fill()

    if mandir:
        mx = 180 - (scroll * 160) % 1200
        if -150 < mx < W + 150:
            rrect(ctx, mx - 60, FEET - 210, 120, 210, 4)
            rgba(ctx, hexc("#D8C4A0"))
            ctx.fill()
            smooth(ctx, [(mx - 74, FEET - 210), (mx, FEET - 295), (mx + 74, FEET - 210)], k=0.05)
            ink(ctx, SAFF, 4)
            line(ctx, [(mx, FEET - 295), (mx, FEET - 355)], hexc("#8A5A2A"), 5)
            wave = 6 * math.sin(t * 5)
            smooth(ctx, [(mx, FEET - 355), (mx + 48, FEET - 342 + wave), (mx, FEET - 325)], k=0.2)
            rgba(ctx, SAFF)
            ctx.fill()
            rrect(ctx, mx - 28, FEET - 135, 56, 95, 24)
            rgba(ctx, hexc("#3A2018"))
            ctx.fill()
            glow(ctx, mx, FEET - 70, 85, GOLDEN, 0.55 + 0.1 * math.sin(t * 9))
            circle(ctx, mx, FEET - 68, 8, hexc("#FFB83A"))

    lx = 920 - (scroll * 220) % 1100
    if -100 < lx < W + 200:
        line(ctx, [(lx, FEET), (lx, 420), (lx - 85, 420)], hexc("#2A3242"), 12)
        glow(ctx, lx - 85, 438, 175, hexc("#FFE090"), 0.28)
        circle(ctx, lx - 85, 434, 14, hexc("#FFF2BA"))

    ctx.rectangle(-250, GROUND - 35, W + 500, H + 300)
    rgba(ctx, hexc("#1E222E"))
    ctx.fill()
    line(ctx, [(-250, GROUND - 35), (W + 250, GROUND - 35)], hexc("#3A4256"), 6)

    off = (scroll * 320) % 180
    for k in range(-2, 10):
        rx = k * 180 - off
        rrect(ctx, rx, FEET + 25, 95, 14, 4)
        rgba(ctx, hexc("#C8CDD8"), 0.55)
        ctx.fill()

    if mist > 0:
        glow(ctx, W / 2, FEET - 100, 520, hexc("#3A4A70"), 0.18 * mist)


def hanuman_aura(ctx, x, y, s, t, a=0.55, pose="abhaya"):
    def draw():
        glow(ctx, x, y - 280 * s, 260 * s, GOLDEN, 0.45 * a)
        pm.hanuman(ctx, x, y, s, t, pose=pose, aura=False)
    dv.group(ctx, a, draw)


def cycle(ctx, x, y, s, t, broken=False, roll=0.0, flip=False, beam=False):
    """Readable bicycle with optional headlight beam and snapped chain."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(-s if flip else s, s)
        wr = 68
        rear = (-115, -wr)
        front = (115, -wr)
        pedal = (-15, -wr + 12)
        seat = (-52, -182)
        stem = (72, -182)

        if beam:
            ctx.move_to(stem[0] + 15, stem[1] + 12)
            ctx.line_to(stem[0] + 340, stem[1] - 40)
            ctx.line_to(stem[0] + 340, stem[1] + 165)
            ctx.close_path()
            rgba(ctx, hexc("#FFF2A8"), 0.22)
            ctx.fill()

        for wx, wy in (rear, front):
            ctx.new_path()
            ctx.arc(wx, wy, wr, 0, math.tau)
            rgba(ctx, hexc("#14161E"))
            ctx.set_line_width(15)
            ctx.stroke()
            ctx.new_path()
            ctx.arc(wx, wy, wr - 7, 0, math.tau)
            rgba(ctx, hexc("#D8DDE6"))
            ctx.set_line_width(4)
            ctx.stroke()
            for k in range(6):
                ang = roll + k * math.pi / 3
                line(ctx, [(wx, wy), (wx + (wr - 9) * math.cos(ang), wy + (wr - 9) * math.sin(ang))],
                     hexc("#A8B2C2"), 2.5, 0.75)
            circle(ctx, wx, wy, 11, hexc("#6E788C"))

        if broken:
            smooth(ctx, [rear, (-70, -24), (-38, -4)], k=0.4)
            rgba(ctx, hexc("#9AA4B8"))
            ctx.set_line_width(6)
            ctx.stroke()
            smooth(ctx, [pedal, (-32, -26), (-50, -6)], k=0.4)
            rgba(ctx, hexc("#9AA4B8"))
            ctx.set_line_width(5)
            ctx.stroke()
        else:
            line(ctx, [rear, pedal], hexc("#4A5060"), 6)
            line(ctx, [(rear[0], rear[1] - 9), (pedal[0], pedal[1] - 4)], hexc("#4A5060"), 4)

        col = hexc("#D83838")
        line(ctx, [rear, seat, stem, pedal, rear], col, 10)
        line(ctx, [seat, pedal], col, 10)
        line(ctx, [stem, front], col, 10)
        line(ctx, [(stem[0], stem[1]), (stem[0] - 8, stem[1] - 32), (stem[0] - 28, stem[1] - 32)],
             hexc("#C0C8D4"), 9)
        circle(ctx, stem[0] + 10, stem[1] + 10, 10, hexc("#FFF09A") if beam else hexc("#8892A0"))
        rrect(ctx, seat[0] - 26, seat[1] - 12, 50, 14, 6)
        rgba(ctx, hexc("#2A2220"))
        ctx.fill()
        # Medicine bag
        rrect(ctx, stem[0] - 18, stem[1] - 6, 40, 50, 8)
        ink(ctx, hexc("#EAEAEA"), 3)
        line(ctx, [(stem[0] + 2, stem[1] + 10), (stem[0] + 2, stem[1] + 28)], RED_THREAD, 5)
        line(ctx, [(stem[0] - 7, stem[1] + 19), (stem[0] + 11, stem[1] + 19)], RED_THREAD, 5)
        ctx.restore()
    dv.group(ctx, 1.0, draw)


def boy_riding_cycle(ctx, x, y, s, t, roll=0.0):
    """Boy genuinely seated on the bicycle saddle, gripping handlebars and pedaling!"""
    cycle(ctx, x, y, s, t, broken=False, roll=roll, beam=True)

    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)
        # Saddle is at (-52, -182); handlebar grip at (44, -214); crank at (-15, -56)
        hip = (-50, -196)
        sho = (-22, -298)
        head = (-10, -356)
        bob = 3 * math.sin(roll * 2)

        # Back leg (darker)
        a1 = roll + math.pi
        ped1 = (-15 + 24 * math.cos(a1), -56 + 24 * math.sin(a1))
        knee1 = (-10 + 18 * math.cos(a1 * 0.5), -130 + 14 * math.sin(a1))
        limb(ctx, [hip, knee1, ped1], hexc("#1A263C"), 26)
        rrect(ctx, ped1[0] - 12, ped1[1] - 6, 30, 14, 6)
        rgba(ctx, (0.95, 0.95, 0.95))
        ctx.fill()

        # Torso leaning forward
        smooth(ctx, [(hip[0] - 24, hip[1]), (sho[0] - 26, sho[1] + bob),
                     (sho[0] + 24, sho[1] + bob), (hip[0] + 22, hip[1])], k=0.2)
        ink(ctx, hexc("#3B78C4"), 4)

        # Front leg
        a2 = roll
        ped2 = (-15 + 24 * math.cos(a2), -56 + 24 * math.sin(a2))
        knee2 = (-6 + 18 * math.cos(a2 * 0.5), -130 + 14 * math.sin(a2))
        limb(ctx, [hip, knee2, ped2], hexc("#263858"), 28)
        rrect(ctx, ped2[0] - 12, ped2[1] - 6, 30, 14, 6)
        ink(ctx, (0.95, 0.95, 0.95), 3)

        # Arm reaching to handlebar grip (44, -214)
        limb(ctx, [(sho[0] + 10, sho[1] + 15 + bob), (18, -245 + bob), (46, -214)], SKIN, 20)
        kalawa_glow(ctx, 36, -222, t, a=0.95)
        circle(ctx, 48, -214, 12, SKIN)

        # Head (side/three-quarter view)
        circle(ctx, head[0], head[1] + bob, 42, SKIN)
        ink(ctx, SKIN, 4)
        smooth(ctx, [(head[0] - 44, head[1] - 10 + bob), (head[0] - 10, head[1] - 54 + bob),
                     (head[0] + 38, head[1] - 22 + bob), (head[0] - 26, head[1] - 12 + bob)], k=0.35)
        rgba(ctx, hexc("#1A1614"))
        ctx.fill()
        eye(ctx, head[0] + 16, head[1] - 4 + bob, 7, 9, t, look=(0.8, 0.0))
        ctx.restore()
    dv.group(ctx, 1.0, draw)


def boy_pushing_cycle(ctx, x, y, s, t):
    """Boy walking sideways pushing the broken cycle along the road."""
    cycle(ctx, x + 130 * s, y, s, t, broken=True, roll=t * 2.5)

    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)
        ph = t * 5.0
        hip = (0, -215)
        sho = (8, -325)
        head = (14, -388)
        step = 34 * math.sin(ph)
        limb(ctx, [hip, (-step * 0.4, -110), (-step, -8)], hexc("#1A263C"), 28)
        limb(ctx, [hip, (step * 0.4, -110), (step, -8)], hexc("#263858"), 28)
        for fx in (-step, step):
            rrect(ctx, fx - 14, -14, 34, 14, 6)
            ink(ctx, (0.95, 0.95, 0.95), 3)
        smooth(ctx, [(-28, -215), (-26, -325), (34, -325), (30, -215)], k=0.2)
        ink(ctx, hexc("#3B78C4"), 4)
        # Arm holding handlebar
        limb(ctx, [(22, -310), (65, -260), (96, -212)], SKIN, 20)
        kalawa_glow(ctx, 84, -225, t, a=0.95)
        circle(ctx, head[0], head[1], 44, SKIN)
        ink(ctx, SKIN, 4)
        smooth(ctx, [(head[0] - 44, head[1] - 10), (head[0], head[1] - 56),
                     (head[0] + 40, head[1] - 20)], k=0.35)
        rgba(ctx, hexc("#1A1614"))
        ctx.fill()
        eye(ctx, head[0] + 18, head[1] - 4, 7, 9, t, look=(0.8, 0.0))
        ctx.restore()
    dv.group(ctx, 1.0, draw)


def kalawa_glow(ctx, x, y, t, a=0.9):
    glow(ctx, x, y, 42, RED_THREAD, 0.55 * a + 0.15 * math.sin(t * 7))
    rrect(ctx, x - 14, y - 6, 28, 12, 4)
    rgba(ctx, RED_THREAD, a)
    ctx.fill()


def baba_gamchha(ctx, x, y, s, t, pose="stand", flip=False, a=1.0):
    """Full-sized, detailed village elder in white kurta-dhoti, white mustache/beard, tilak, and saffron gamchha."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(-s if flip else s, s)
        bob = 4 * math.sin(t * 3) if pose == "stand" else 0
        if pose == "kneel":
            limb(ctx, [(-28, -155), (36, -92), (-15, -12)], hexc("#ECEAE2"), 42)
            limb(ctx, [(22, -155), (56, -72), (56, -12)], hexc("#ECEAE2"), 42)
            smooth(ctx, [(-60, -320), (54, -320), (62, -150), (-62, -150)], k=0.2)
            ink(ctx, hexc("#F6F4EC"), 5)
            smooth(ctx, [(-52, -320), (-14, -320), (-6, -180), (-44, -180)], k=0.2)
            ink(ctx, SAFF, 4)
            circle(ctx, 10, -382, 52, SKIN)
            ink(ctx, SKIN, 4)
            smooth(ctx, [(-42, -395), (10, -445), (62, -395)], k=0.3)
            rgba(ctx, hexc("#ECECEC"))
            ctx.fill()
            line(ctx, [(26, -408), (26, -382)], RED_THREAD, 7)
            eye(ctx, 32, -382, 8, 10, t, look=(0.7, 0.3))
            # White mustache
            smooth(ctx, [(16, -360), (36, -356), (52, -350)], k=0.4)
            rgba(ctx, hexc("#ECECEC"))
            ctx.set_line_width(9)
            ctx.stroke()
            limb(ctx, [(40, -295), (105, -195), (150, -110)], SKIN, 24)
            glow(ctx, 150, -110, 48, GOLDEN, 0.65)
        else:
            limb(ctx, [(-30, -210 + bob), (-32, -14)], hexc("#ECEAE2"), 44)
            limb(ctx, [(30, -210 + bob), (32, -14)], hexc("#ECEAE2"), 44)
            smooth(ctx, [(-68, -415 + bob), (68, -415 + bob), (76, -195 + bob), (-76, -195 + bob)], k=0.2)
            ink(ctx, hexc("#F6F4EC"), 5)
            smooth(ctx, [(-64, -415 + bob), (-18, -415 + bob), (-10, -250 + bob), (-54, -250 + bob)], k=0.2)
            ink(ctx, SAFF, 4)
            circle(ctx, 0, -478 + bob, 56, SKIN)
            ink(ctx, SKIN, 4)
            smooth(ctx, [(-56, -492 + bob), (0, -545 + bob), (56, -492 + bob)], k=0.35)
            rgba(ctx, hexc("#ECECEC"))
            ctx.fill()
            line(ctx, [(0, -504 + bob), (0, -478 + bob)], RED_THREAD, 7)
            eye(ctx, -18, -476 + bob, 9, 11, t)
            eye(ctx, 18, -476 + bob, 9, 11, t)
            smooth(ctx, [(-22, -452 + bob), (0, -458 + bob), (22, -452 + bob)], k=0.4)
            rgba(ctx, hexc("#ECECEC"))
            ctx.set_line_width(9)
            ctx.stroke()
            smooth(ctx, [(-14, -442 + bob), (0, -434 + bob), (14, -442 + bob)], k=0.4)
            rgba(ctx, hexc("#3A2014"))
            ctx.set_line_width(4)
            ctx.stroke()
            limb(ctx, [(60, -395 + bob), (82, -295 + bob), (74, -215 + bob)], SKIN, 24)
            limb(ctx, [(-60, -395 + bob), (-82, -295 + bob), (-74, -215 + bob)], SKIN, 24)
        ctx.restore()
    dv.group(ctx, a, draw)


def gada_shadow(ctx, x, y, s, t, a=0.75):
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)
        glow(ctx, 0, -210, 240, GOLDEN, 0.6 * a)
        line(ctx, [(0, 0), (0, -270)], hexc("#140E06"), 22, 0.9 * a)
        circle(ctx, 0, -310, 68, hexc("#140E06"), 0.9 * a)
        circle(ctx, 0, -310, 68, GOLDEN, 0.25 * a)
        ctx.restore()
    dv.group(ctx, a, draw)


# =============================================================================
# Script v2 (26 Nov, user-approved): every line = action -> "to/ki" -> result, so KikiVoice does not drag the
# last word; no nukta words, no 1-2 word lines; the miracle is the last story beat. 9 scenes, ~100 words.
# =============================================================================
SPEC = [
    {"key": "hook", "text": "SUNSAAN RAAT",
     "visual": "Night road, broken cycle, golden Hanuman ji behind the boy",
     "vo": [("low", [("माँ की दवाई लेकर लौटा तो", "MAA KI DAWAI LEKAR LAUTA TO"),
                     ("रात के बारह बज चुके थे।", "RAAT KE BAARAH BAJ CHUKE THE.")], 0.04)]},

    {"key": "dawai", "text": "MAA KI DAWAI",
     "visual": "Boy sitting on cycle and pedaling fast past roadside mandir",
     "vo": [("low", [("वो सुनसान सड़क पर", "WO SUNSAAN SADAK PAR"),
                     ("साइकिल दौड़ा रहा था", "CYCLE DAUDA RAHA THA")], 0.0)]},

    {"key": "chain", "text": "CHAIN TOOT GAYI",
     "visual": "Zoomed close-up of bicycle rear wheel and chain snapping with sparks",
     "vo": [("build", [("कि तभी चेन टूट गई।", "KI TABHI CHAIN TOOT GAYI.")], 0.04)]},

    {"key": "phone", "text": "PHONE BAND",
     "visual": "Medium close-up of boy holding dead phone with red empty battery",
     "vo": [("low", [("फोन निकाला तो", "PHONE NIKALA TO"),
                     ("वो भी बंद पड़ा था।", "WO BHI BAND PADA THA.")], 0.04)]},

    {"key": "chalisa", "text": "PAIDAL CHAL PADA",
     "visual": "Side view of boy pushing broken cycle forward; golden Hanuman beside him",
     "vo": [("build", [("घर चार किलोमीटर दूर था", "GHAR CHAAR KILOMETER DOOR THA"),
                       ("तो वो पैदल ही चल पड़ा।", "TO WO PAIDAL HI CHAL PADA.")], 0.04),
            ("build", [("रास्ते भर वो", "RAASTE BHAR WO"),
                       ("हनुमान चालीसा पढ़ता रहा।", "HANUMAN CHALISA PADHTA RAHA.")], 0.04)]},

    {"key": "baba", "text": "LAL GAMCHHA",
     "visual": "Full-sized elder in red gamchha emerges from night mist",
     "vo": [("tell", [("मोड़ पर पहुंचा तो", "MOD PAR PAHUNCHA TO"),
                      ("लाल गमछे वाला एक आदमी", "LAL GAMCHHE WALA EK AADMI"),
                      ("खड़ा मिला।", "KHADA MILA.")], 0.04)]},

    {"key": "jod_di", "text": "CHAIN JOD DI",
     "visual": "Close-up of Baba kneeling to fix the chain with golden sparkle burst",
     "vo": [("tell", [("उसने चुपचाप चेन जोड़ी", "USNE CHUPCHAP CHAIN JODI"),
                      ("और बोला जा", "AUR BOLA JA"),
                      ("माँ राह देख रही है।", "MAA RAAH DEKH RAHI HAI.")], 0.04)]},

    {"key": "chhaya", "text": "GADA KI CHHAYA",
     "visual": "Boy turns; baba is gone, only a red thread and gada shadow remain",
     "vo": [("awe", [("लड़के ने धन्यवाद कहने को", "LADKE NE DHANYAVAAD KEHNE KO"),
                     ("मुड़कर देखा तो", "MUDKAR DEKHA TO"),
                     ("सड़क खाली थी।", "SADAK KHALI THI.")], 0.04),
            ("awe", [("बस सड़क पर गदा की", "BAS SADAK PAR GADA KI"),
                     ("एक परछाईं रह गई थी।", "EK PARCHHAIN REH GAYI THI.")], 0.04)]},

    {"key": "jai", "text": "JAI BAJRANGBALI",
     "visual": "Full glowing Hanuman ji blesses the boy; smooth loop into hook",
     "vo": [("punch", [("जो मानता है वो लिखे", "JO MAANTA HAI WO LIKHE"),
                       ("जय बजरंगबली।", "JAI BAJRANGBALI.")], 0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "BAJRANGBALI": SAFF, "THEEK": GOLD_HI, "MAA": hexc("#9AD0FF"),
    "DAWAI": hexc("#9AD0FF"), "CHAIN": hexc("#FF5A5A"), "TOOT": hexc("#FF5A5A"),
    "BAND": hexc("#FF5A5A"), "HANUMAN": SAFF, "CHALISA": GOLD_HI, "PAIDAL": hexc("#9BE07A"),
    "GAMCHHE": SAFF, "BABA": GOLD_HI, "JOD": hexc("#9BE07A"), "GADA": GOLD_HI,
    "CHHAYA": GOLD_HI, "BAJRANGBALI.": SAFF, "AADMI": SAFF, "KHALI": GOLD_HI, "PARCHHAIN": GOLD_HI,
    "BAARAH": hexc("#9AD0FF"),
})


# =============================================================================
# Scene classes (with real camera variety!)
# =============================================================================
class Hook(Cued):
    def beats(self, d):
        return {"aaye": self.cue("AAYE", d * 0.65)}

    def events(self, d):
        return [(0.1, "shimmer"), (self.beats(d)["aaye"], "soft_thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        appear = ease_out_cubic(clamp(t / 0.8))
        zoom = 1.0 + 0.08 * clamp(t / d)
        cam_begin(ctx, W / 2, FEET - 280, zoom, W / 2, FEET - 280)
        night_road(ctx, t, scroll=0.0, mandir=True, mist=0.45)
        hanuman_aura(ctx, 680, FEET, 0.78, t, a=0.78 * appear, pose="abhaya")
        cycle(ctx, 430, FEET, 1.0, t, broken=True)
        boy(ctx, 290, FEET, S, t, pose="namaste", mood="low", look=(0.8, -0.3))
        if t >= b["aaye"]:
            sparkle_burst(ctx, 680, FEET - 320, clamp((t - b["aaye"]) / 0.5), c=GOLDEN, n=12, r=150)
        cam_end(ctx)


class Dawai(Cued):
    def events(self, d):
        return [(0.1, "tick")]

    def draw(self, ctx, t, d):
        night_road(ctx, t, scroll=t * 1.6, mandir=True, mist=0.25)
        hanuman_aura(ctx, 210, FEET - 40, 0.45, t, a=0.22, pose="abhaya")
        boy_riding_cycle(ctx, 480, FEET, 1.08, t, roll=t * 9.0)


class Chain(Cued):
    def beats(self, d):
        return {"toot": self.cue("TOOT", d * 0.55)}

    def events(self, d):
        return [(self.beats(d)["toot"], "zap")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        snapped = t >= b["toot"]
        shk = 10 * math.exp(-max(0, t - b["toot"]) * 5) if snapped else 0
        # Zoom directly onto the rear wheel & chain!
        cam_begin(ctx, 460 + shk * math.sin(t * 50), FEET - 75, 1.85, W * 0.5, H * 0.56)
        night_road(ctx, t, scroll=0.0 if snapped else t * 0.5, mandir=False, mist=0.35)
        hanuman_aura(ctx, 240, FEET - 20, 0.5, t, a=0.25, pose="abhaya")
        cycle(ctx, 560, FEET, 1.08, t, broken=snapped, roll=0 if snapped else t * 5)
        if snapped:
            sparkle_burst(ctx, 440, FEET - 55, clamp((t - b["toot"]) / 0.45), c=hexc("#FF5A2A"), n=14, r=110)
        cam_end(ctx)


class Phone(Cued):
    def events(self, d):
        return [(0.15, "beep")]

    def draw(self, ctx, t, d):
        # Medium close-up on boy & dead phone
        cam_begin(ctx, 410, FEET - 270, 1.48, W * 0.5, H * 0.52)
        night_road(ctx, t, scroll=0.0, mandir=False, mist=0.5)
        hanuman_aura(ctx, 680, FEET, 0.60, t, a=0.24, pose="abhaya")
        boy(ctx, 380, FEET, S, t, pose="phone", mood="low", look=(0.0, 0.3))
        phone(ctx, 425, FEET - 210 * S, -0.2, t, glow_a=0.0)
        # Clear red empty-battery icon on phone
        rrect(ctx, 412, FEET - 224 * S, 24, 14, 3)
        ink(ctx, RED_THREAD, 3)
        kalawa_glow(ctx, 420, FEET - 165, t, a=0.95)
        cam_end(ctx)


class Chalisa(Cued):
    def beats(self, d):
        return {"chala": self.cue("CHAL", d * 0.65)}

    def events(self, d):
        return [(0.1, "shimmer")]

    def draw(self, ctx, t, d):
        night_road(ctx, t, scroll=t * 0.7, mandir=True, mist=0.35)
        hanuman_aura(ctx, 290, FEET, 0.76, t, a=0.55 + 0.1 * math.sin(t * 3), pose="abhaya")
        boy_pushing_cycle(ctx, 440, FEET, 0.96, t)


class Baba(Cued):
    def beats(self, d):
        return {"aaye": self.cue("AAYE", d * 0.7)}

    def events(self, d):
        return [(0.15, "soft_thud")]

    def draw(self, ctx, t, d):
        enter = ease_out_cubic(clamp(t / 1.0))
        night_road(ctx, t, scroll=0.0, mandir=False, mist=0.5)
        cycle(ctx, 430, FEET, 0.96, t, broken=True)
        boy(ctx, 250, FEET, S, t, pose="stand", mood="shock", look=(1.0, -0.1))
        bx = lerp(940, 720, enter)
        glow(ctx, bx, FEET - 240, 220, SAFF, 0.4 * enter)
        baba_gamchha(ctx, bx, FEET, S * 1.38, t, pose="stand", flip=True, a=enter)


class JodDi(Cued):
    def beats(self, d):
        return {"jod": self.cue("JOD", d * 0.65)}

    def events(self, d):
        return [(self.beats(d)["jod"], "dingdong")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        fixed = t >= b["jod"]
        # Medium close-up on Baba fixing the chain
        cam_begin(ctx, 560, FEET - 150, 1.32, W * 0.5, H * 0.56)
        night_road(ctx, t, scroll=0.0, mandir=False, mist=0.3)
        hanuman_aura(ctx, 680, FEET - 20, 0.70, t, a=0.28 if fixed else 0.14, pose="abhaya")
        cycle(ctx, 450, FEET, 1.05, t, broken=not fixed)
        boy(ctx, 240, FEET, S, t, pose="stand", mood="joy" if fixed else "neutral", look=(0.9, 0.2))
        baba_gamchha(ctx, 690, FEET, S * 1.38, t, pose="kneel", flip=True, a=1.0)
        if fixed:
            sparkle_burst(ctx, 420, FEET - 60, clamp((t - b["jod"]) / 0.5), c=GOLDEN, n=16, r=140)
        cam_end(ctx)


class Chhaya(Cued):
    def beats(self, d):
        return {"chhaya": self.cue("CHHAYA", d * 0.55)}

    def events(self, d):
        return [(0.1, "shimmer"), (self.beats(d)["chhaya"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        rev = ease_out_cubic(clamp((t - b["chhaya"] + 0.3) / 0.7))
        night_road(ctx, t, scroll=0.0, mandir=False, mist=0.45)
        gada_shadow(ctx, 730, FEET, 1.18, t, a=0.88 * rev)
        glow(ctx, 690, FEET - 12, 60, RED_THREAD, 0.6 * rev)
        smooth(ctx, [(660, FEET - 8), (690, FEET - 14), (720, FEET - 6)], k=0.4)
        ink(ctx, RED_THREAD, 5)
        cycle(ctx, 410, FEET, 0.96, t, broken=False)
        boy(ctx, 260, FEET, S, t, pose="namaste", mood="shock", look=(1.0, -0.3))


class Jai(Cued):
    def beats(self, d):
        return {"jai": self.cue("BAJRANGBALI", d * 0.55)}

    def events(self, d):
        return [(0.1, "ghanti")]

    def draw(self, ctx, t, d):
        night_road(ctx, t, scroll=0.0, mandir=True, mist=0.25)
        rise = ease_out_cubic(clamp(t / 0.8))
        hanuman_aura(ctx, 700, FEET, 0.78, t, a=0.95 * rise, pose="abhaya")
        dv.petals(ctx, t, n=22, seed=11, a=0.85)
        cycle(ctx, 430, FEET, 0.96, t, broken=False)
        boy(ctx, 280, FEET, S, t, pose="namaste", mood="joy", look=(0.9, -0.4))
        x = clamp((t - (d - 0.45)) / 0.45)
        if x > 0:
            ctx.push_group()
            Hook().draw(ctx, 0.0, d)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(x)


SCENE_CLASSES = {"hook": Hook, "dawai": Dawai, "chain": Chain, "phone": Phone, "chalisa": Chalisa,
                 "baba": Baba, "jod_di": JodDi, "chhaya": Chhaya, "jai": Jai}

UPLOAD = {
    "titles": [
        "Sunsaan Raat Mein Tooti Cycle... Aur Bajrangbali Khud Aaye #shorts",
        "Raat Ko Maa Ki Dawai Le Ja Raha Tha... Phir Gada Ki Chhaya Dikhi #shorts",
        "Andhere Mein Cycle Ki Chain Tooti... Lal Gamchhe Mein Kaun Aaya? #shorts",
    ],
    "thumb_text": "KAUN AAYA?",
    "queries": [
        "hanuman ji ki kahani",
        "bajrangbali",
        "emotional story hindi",
    ],
    "description": """
Raat ke barah baje maa ki dawai lekar laut rahe bete ki cycle ki chain toot gayi... phone bhi band aur ghar chaar
kilometer door. Par usne haar nahi maani, Hanuman Chalisa padhta hua paidal chal pada. Mod par lal gamchhe wala kaun
khada tha? Jai Bajrangbali.

Kalpanik prerak katha. Mehnat aur himmat ke saath bhakti raasta dikhati hai.

Kya aapne kabhi mushkil waqt mein Bajrangbali ka saath mehsus kiya hai? Comment mein JAI BAJRANGBALI likhein.
""",
    "tags": [
        "hanuman ji ki kahani", "jai bajrangbali", "hanuman chalisa", "sankat mochan", "karm aur kripa",
        "emotional story hindi", "maa ki dawai", "cycle story", "divya rahasya", "prerak katha", "shorts",
    ],
    "hashtags": ["#Shorts", "#JaiBajrangbali", "#HanumanJi"],
    "pinned_comment": "Kya aapke saath bhi kabhi aisa hua jab mushkil waqt mein kisi anjaan ne madad ki? 🙏 "
                      "Comment mein JAI BAJRANGBALI likho, hum sab milke prarthana karenge.",
}


def thumbnail(ctx):
    night_road(ctx, 0.5, scroll=0.0, mandir=True, mist=0.35)
    hanuman_aura(ctx, 700, FEET, 0.78, 0.5, a=0.92, pose="abhaya")
    cycle(ctx, 410, FEET, 0.96, 0.5, broken=True)
    boy(ctx, 270, FEET, S, 0.5, pose="namaste", mood="shock", look=(0.9, -0.3))
    text(ctx, "RAAT MEIN", 540, 1330, 118, hexc("#FFFFFF"), font=CAPTION_FONT, bold=False,
         stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "KAUN AAYA?", 540, 1470, 134, SAFF, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
