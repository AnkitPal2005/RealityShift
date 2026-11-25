"""Mummy Ke 27 Missed Call (Karm Aur Kripa #5): a boy living away from home keeps cutting his mother's calls; one
night he has a high fever, his phone is dead and no one is near - the neighbour aunty walks in with hot khichdi
"teri mummy ne bheji hai", a mor-pankh tucked in the cloth - and he calls her himself: "mummy sorry" (~26 s,
9 scenes). Kalpanik prerak katha.

Usage (from SanatanKatha/):
  python make.py mummy_missed_call --preview
  python make.py mummy_missed_call --kiki-split --check-voice
  python make.py mummy_missed_call --engine files

Relatable-first script (user, 25 Nov): the moment people live themselves (27 missed calls, "har baat pe phone mat
kiya karo"). Natural voice speed (no speed-up), so fewer words and one scene per line (user, 25 Nov).
Kanha ji in every scene: the little altar mummy gave him (diya), his faint golden form watching, the altar in
mummy's home, the mor-pankh in the cloth, the final blessing.
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
from core.devta import smooth, ink, ell, limb, place, group, shade  # noqa: F401

from kathas.daadi_morpankh import boy, room_bg, bed, phone, home_altar, kanha_light, door, GOLDEN, FEET
from kathas.eklavya_krishna import sparkle_burst, edge_glow
from kathas import maa_kangan as mk
from kathas.maa_kangan import maa, dark_phone

TOPIC = "KARM AUR KRIPA MUMMY KE MISSED CALL BUKHAR PADOS AUNTY KHICHDI MOR PANKH KANHA"
OUTPUTS = {"edge": "mummy_missed_call_short.mp4"}
MUSIC_STYLE = "ambient"   # soft and emotional; stage_ka_darr tension 96, maa_kangan pulse 82
MUSIC_BPM = 88            # >= 6 BPM away from 96
MUSIC_VOLUME = 0.11
TAIL_PAD = 0.35           # natural breaths - no squeezing (user, 25 Nov: "speed natural rakhenge")
MAX_GAP = 0.45
SCENE_WHOOSH = False      # user, 25 Nov: no whoosh on cuts
SFX_SCALE = 0.5           # the few SFX at half level

PINK = hexc("#FF7AA8")
SOURCES = [
    "Original fictional story (Kalpanik prerak katha) - no scripture or real-event claim; labelled in the description.",
    "Shri Krishna's form (mor-pankh, flute, pitambar, blessing hand) follows common Bhagavata iconography; the "
    "mor-pankh as his sign is a popular bhakti motif.",
]

BX = 380              # the boy on his bed
ALT = (650, 540)      # the small Kanha altar mummy gave him (shelf above the bed)


# =============================================================================
# People and props
# =============================================================================
def aunty(ctx, x, y, s, t, **kw):
    """The neighbour aunty: same rig as Maa, her own saree colours (teal with orange border, maroon blouse)."""
    keep = mk.SAREE, mk.SAREE_BORDER, mk.BLOUSE
    mk.SAREE, mk.SAREE_BORDER, mk.BLOUSE = hexc("#1E7A7A"), hexc("#FF8A1E"), hexc("#7A1E2A")
    try:
        maa(ctx, x, y, s, t, kangan=0.0, **kw)
    finally:
        mk.SAREE, mk.SAREE_BORDER, mk.BLOUSE = keep


def mummy_on_phone(ctx, x, s, t, mood="sad", a=1.0):
    """Mummy with the phone at her ear (the 'wipe' arm puts her right hand at her face)."""
    maa(ctx, x, FEET, s, t, pose="wipe", mood=mood, a=a)
    phone(ctx, x + 40 * s, FEET - 700 * s, 0.35, t, glow_a=0.25, a=a)


def call_buzz(ctx, x, y, t, n, ring=1.0):
    """Phone lying on the bed, buzzing; n red missed-call dots stack up beside it (no text on screen)."""
    jit = 5 * ring * math.sin(t * 70)
    phone(ctx, x + jit, y, math.pi / 2, t, glow_a=0.6 * ring)
    if ring > 0:
        for i in range(3):                                                   # vibration arcs
            u = (t * 2 + i / 3) % 1
            for side in (-1, 1):
                ctx.arc(x + side * (60 + 40 * u), y, 30 + 20 * u, -0.6 if side > 0 else math.pi - 0.6,
                        0.6 if side > 0 else math.pi + 0.6)
                rgba(ctx, hexc("#FF5A5A"), 0.7 * (1 - u))
                ctx.set_line_width(4)
                ctx.stroke()
    for i in range(int(n)):                                                   # missed-call dots
        cx = x - 70 + (i % 9) * 18
        cy = y - 70 - (i // 9) * 18
        circle(ctx, cx, cy, 7, hexc("#FF3A3A"))


def blanket(ctx, x, s, t, shiver=0.0):
    jx = 4 * shiver * math.sin(t * 45)
    top = FEET + 150 * s - 470 * s       # from the shoulders down - the face stays visible
    smooth(ctx, [(x - 150 * s + jx, top + 30), (x + jx, top - 10), (x + 150 * s + jx, top + 30),
                 (x + 175 * s + jx, FEET - 140), (x - 175 * s + jx, FEET - 140)], k=0.15)
    ink(ctx, hexc("#6A4A8A"), 4)
    for k in range(4):
        line(ctx, [(x - 120 * s + 60 * k * s + jx, top + 60), (x - 130 * s + 64 * k * s + jx, FEET - 150)],
             hexc("#4E3470"), 4, 0.7)


def khichdi(ctx, x, y, t, a=1.0, open_=0.0, steam=1.0):
    """A steel bowl wrapped in a checked cloth, steam rising; open_ 1 = the knot opens."""
    def draw():
        ell(ctx, x, y, 90, 26)
        ink(ctx, hexc("#C8CCD4"), 3)
        smooth(ctx, [(x - 90, y), (x - 70, y + 60), (x + 70, y + 60), (x + 90, y)], k=0.2)
        ink(ctx, hexc("#A8ACB4"), 3)
        if open_ < 1:
            k = 1 - open_
            smooth(ctx, [(x - 100, y + 10), (x - 60, y - 40 * k), (x, y - 70 * k), (x + 60, y - 40 * k),
                         (x + 100, y + 10), (x, y + 30)], k=0.2)
            ink(ctx, hexc("#C8322A"), 3)
            for j in range(4):
                line(ctx, [(x - 70 + 45 * j, y - 30 * k), (x - 60 + 45 * j, y + 20)], hexc("#FFD27A"), 4, 0.8)
            circle(ctx, x, y - 70 * k, 16, hexc("#A8221E"))
        else:
            ell(ctx, x, y - 4, 74, 18)
            rgba(ctx, hexc("#F2C84A"))
            ctx.fill()
            for k in range(2):                                                 # cloth opened flat
                side = -1 if k == 0 else 1
                smooth(ctx, [(x + side * 80, y + 6), (x + side * 170, y - 10), (x + side * 160, y + 50),
                             (x + side * 80, y + 40)], k=0.2)
                ink(ctx, hexc("#C8322A"), 3)
        for i in range(3):
            u = (t * 0.7 + i / 3) % 1
            sx = x - 30 + 30 * i + 12 * math.sin(t * 3 + i)
            line(ctx, [(sx, y - 40 - 160 * u), (sx + 10, y - 70 - 160 * u)], (1, 1, 1), 6,
                 0.5 * steam * math.sin(math.pi * u))
    group(ctx, a, draw)


def boy_room(ctx, t, night=1.0, altar=1.0, red=0.0, dim=0.0):
    room_bg(ctx, t, night=night, lamp=0.0)
    home_altar(ctx, ALT[0], ALT[1], t, lit=altar)
    if red > 0:
        rgba(ctx, hexc("#C0201A"), 0.18 * red)
        ctx.paint()
    if dim > 0:
        rgba(ctx, (0, 0, 0), 0.35 * dim)
        ctx.paint()


def mummy_home(ctx, t, lit=1.0):
    """Mummy's home at night: warm lamp-lit wall, her own Kanha mandir with a diya."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in ((0.0, "#5A3A2A"), (0.6, "#7A4A2E"), (1.0, "#3A2418")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.rectangle(-80, -80, W + 160, H + 160)
    ctx.fill()
    glow(ctx, 760, 520, 420, hexc("#FFD9A0"), 0.35)
    ctx.rectangle(-80, GROUND - 30, W + 160, H)
    rgba(ctx, hexc("#4A2E1E"))
    ctx.fill()
    home_altar(ctx, 960, 560, t, lit=lit)
    for i in range(10):                                                       # a string of marigolds
        circle(ctx, 600 + 46 * i, 300 + 26 * math.sin(i * 0.6), 13, hexc("#FF8A1E") if i % 2 else hexc("#FFC21E"))


def split(ctx, t, left, right):
    """Phone-call split screen: his room on the left, mummy's home on the right, a soft glowing seam."""
    for x0, x1, fn in ((-80, 540, left), (540, W + 80, right)):
        ctx.save()
        ctx.rectangle(x0, -80, x1 - x0, H + 160)
        ctx.clip()
        fn()
        ctx.restore()
    ctx.move_to(540, -80)
    for k in range(24):
        ctx.line_to(540 + (10 if k % 2 else -10), -80 + k * 90)
    rgba(ctx, (1, 1, 1), 0.85)
    ctx.set_line_width(6)
    ctx.stroke()


def memory_bubble(ctx, x, y, r, t, a, draw_inside):
    if a <= 0:
        return
    for i, rr in enumerate((18, 30)):                                         # thought dots towards the boy
        circle(ctx, x - r - 30 - 50 * i, y + r * 0.6 + 40 * i, rr - 8 * i, (1, 1, 1), 0.8 * a)
    ctx.save()
    ctx.arc(x, y, r, 0, 2 * math.pi)
    ctx.clip()
    ctx.push_group()
    draw_inside()
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(a)
    ctx.restore()
    ctx.arc(x, y, r, 0, 2 * math.pi)
    rgba(ctx, (1, 1, 1), a)
    ctx.set_line_width(8)
    ctx.stroke()


# =============================================================================
# Story: 9 lines = 9 scenes, single narrator, no commas or pause signs (same text as kiki_narrator.txt)
# =============================================================================
SPEC = [
    {"key": "calls", "text": "", "visual": "Night room: the boy studies on his bed; the phone beside him buzzes again and "
                                           "again, red missed-call dots stack up; he flips it face down; Kanha's faint "
                                           "golden form stands by the little altar, watching",
     "vo": [("punch", [("मम्मी के सत्ताईस", "MUMMY KE SATTAIS"), ("मिस्ड कॉल थे", "MISSED CALL THE"),
                       ("और कान्हा", "AUR KANHA"), ("सब देख रहे थे।", "SAB DEKH RAHE THE.")], 0.04)]},
    {"key": "mat", "text": "", "visual": "Split screen: he snaps into the phone in his room; on the right mummy stands at her "
                                         "Kanha mandir with the phone at her ear and her face falls",
     "vo": [("tell", [("वो बोलता था", "WO BOLTA THA"), ("मम्मी हर बात पे", "MUMMY HAR BAAT PE"),
                      ("फ़ोन मत किया करो।", "PHONE MAT KIYA KARO.")], 0.04)]},
    {"key": "bukhar", "text": "", "visual": "Same room, red pulse: he sits wrapped in a blanket, shivering and sweating; the "
                                            "altar diya still burns",
     "vo": [("low", [("उस रात उसे", "US RAAT USE"), ("तेज़ बुखार चढ़ गया।", "TEZ BUKHAAR CHADH GAYA.")], 0.04)]},
    {"key": "band", "text": "", "visual": "Darker: he reaches for the phone - it is dead; he looks at the shut door; nobody; "
                                          "only Kanha's diya glows",
     "vo": [("low", [("फ़ोन बंद था", "PHONE BAND THA"), ("और पास कोई नहीं था।", "AUR PAAS KOI NAHI THA.")], 0.04)]},
    {"key": "aunty", "text": "", "visual": "The door swings open, warm light spills in; the neighbour aunty walks in with a "
                                           "steaming bowl wrapped in a red cloth",
     "vo": [("tell", [("तभी पड़ोस वाली आंटी", "TABHI PADOS WALI AUNTY"), ("गरम खिचड़ी लेकर आईं।", "GARAM KHICHDI LEKAR AAYIN.")],
             0.04)]},
    {"key": "bheji", "text": "", "visual": "Aunty holds out the bowl at his bed; a thought bubble shows mummy on the phone "
                                           "asking aunty for help, her Kanha mandir behind her",
     "vo": [("tell", [("बोलीं", "BOLIN"), ("तेरी मम्मी ने भेजी है।", "TERI MUMMY NE BHEJI HAI.")], 0.04)]},
    {"key": "pankh", "text": "", "visual": "The red cloth opens: a mor-pankh lies on top, glowing gold; he lifts it, Kanha's "
                                           "golden form brightens behind him",
     "vo": [("awe", [("खिचड़ी के कपड़े में", "KHICHDI KE KAPDE MEIN"), ("एक मोर पंख रखा था।", "EK MOR PANKH RAKHA THA.")],
             0.04)]},
    {"key": "sorry", "text": "", "visual": "Split screen: he calls with tears; mummy answers at her mandir - on 'sorry' both cry "
                                           "and smile, both altars glow",
     "vo": [("low", [("उसने खुद फ़ोन मिलाया", "USNE KHUD PHONE MILAAYA"), ("और बोला", "AUR BOLA"),
                     ("मम्मी सॉरी।", "MUMMY SORRY.")], 0.04)]},
    {"key": "jai", "text": "", "visual": "Kanha ji's golden form rises in the room, smiling and blessing, petals fall; the boy "
                                         "folds his hands holding the mor-pankh; last frame on Kanha's smile, fades into "
                                         "the hook",
     "vo": [("punch", [("जो आज मम्मी को", "JO AAJ MUMMY KO"), ("फ़ोन करेगा", "PHONE KAREGA"), ("वो लिखे", "WO LIKHE"),
                       ("जय श्री कृष्ण।", "JAI SHRI KRISHNA.")], 0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "MUMMY": PINK, "SATTAIS": hexc("#FF5A5A"), "MISSED": hexc("#FF5A5A"), "KANHA": GOLD_HI, "DEKH": GOLD_HI,
    "PHONE": hexc("#9AD0FF"), "MAT": hexc("#FF5A5A"), "BUKHAAR": hexc("#FF5A5A"), "BAND": hexc("#FF5A5A"),
    "AKELA": hexc("#9AD0FF"), "AUNTY": hexc("#FFB347"), "KHICHDI": hexc("#FFD27A"), "BHEJI": PINK,
    "MOR": GOLD_HI, "PANKH": GOLD_HI, "KHUD": hexc("#9BE07A"), "SORRY.": PINK, "SORRY": PINK, "JAI": GOLD_HI,
    "KRISHNA": GOLD_HI,
})

S = 0.72


# =============================================================================
# Scenes
# =============================================================================
class Calls(Cued):
    def beats(self, d):
        return {"kanha": self.cue("KANHA", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["kanha"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        boy_room(ctx, t)
        watch = clamp((t - b["kanha"] + 0.2) / 0.6)
        kanha_light(ctx, 850, 0.70, t, a=0.18 + 0.32 * watch)
        boy(ctx, BX, FEET, S, t, pose="write", mood="low", look=(0.7, 0.6), seated=True)
        bed(ctx, BX + 40, FEET + 10, w=640)
        flip = clamp((t - d * 0.7) / 0.3)                                     # he turns it face down at the end
        n = min(27, 3 + int(t / max(0.1, d * 0.7) * 24))
        if flip < 1:
            call_buzz(ctx, 620, FEET - 175, t, n, ring=1.0 - flip)
        else:
            phone(ctx, 620, FEET - 175, math.pi / 2, t, glow_a=0.0)
            rrect(ctx, 620 - 37, FEET - 175 - 21, 74, 42, 8)
            rgba(ctx, hexc("#1A1A22"))
            ctx.fill()
            for i in range(27):
                circle(ctx, 550 + (i % 9) * 18, FEET - 245 - (i // 9) * 18, 7, hexc("#FF3A3A"))
        edge_glow(ctx, t, d, start=0.0)


class Mat(Cued):
    def beats(self, d):
        return {"mat": self.cue("PHONE MAT", d * 0.6)}

    def events(self, d):
        return []

    def draw(self, ctx, t, d):
        b = self.beats(d)
        hurt = clamp((t - b["mat"]) / 0.4)

        def left():
            boy_room(ctx, t, altar=0.6)
            boy(ctx, 270, FEET, S, t, pose="phone", mood="low", look=(0.6, 0.3))

        def right():
            mummy_home(ctx, t, lit=0.8)
            mummy_on_phone(ctx, 760, S, t, mood="sad" if hurt > 0.3 else "neutral")
            if hurt > 0:
                kanha_light(ctx, 960, 0.4, t, a=0.0)
        split(ctx, t, left, right)


class Bukhar(Cued):
    def beats(self, d):
        return {"bukhar": self.cue("BUKHAAR", d * 0.5)}

    def events(self, d):
        b = self.beats(d)
        return [(b["bukhar"], "soft_thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        hot = clamp((t - b["bukhar"] + 0.2) / 0.4)
        boy_room(ctx, t, altar=0.7, red=hot * (0.7 + 0.3 * math.sin(t * 4)))
        jx = 4 * hot * math.sin(t * 45)
        boy(ctx, BX + jx, FEET, S, t, pose="tired", mood="low", look=(0.2, 0.4), seated=True)
        blanket(ctx, BX, S, t, shiver=hot)
        bed(ctx, BX + 40, FEET + 10, w=640)
        dark_phone(ctx, 640, FEET - 175)
        if hot > 0:                                                            # sweat drops
            for i in range(3):
                u = (t * 1.1 + i / 3) % 1
                circle(ctx, BX + 70 + 26 * i, FEET + 108 - 760 * S + 90 * u, 8, hexc("#9AD8FF"), 0.9 * (1 - u))


class Band(Cued):
    def beats(self, d):
        return {"band": self.cue("BAND", d * 0.3), "koi": self.cue("KOI", d * 0.6)}

    def events(self, d):
        return []

    def draw(self, ctx, t, d):
        b = self.beats(d)
        boy_room(ctx, t, altar=1.0, dim=0.6)
        door(ctx, 900, FEET, open_=0.0, light=False)
        glow(ctx, ALT[0], ALT[1] - 90, 180, GOLDEN, 0.25 + 0.1 * math.sin(t * 3))   # only the diya's light
        look = (0.9, 0.0) if t > b["koi"] else (0.6, 0.7)
        boy(ctx, BX, FEET, S, t, pose="drop" if t > b["koi"] else "phone", mood="cry" if t > b["koi"] else "low",
            look=look, seated=True)
        blanket(ctx, BX, S, t, shiver=0.6)
        bed(ctx, BX + 40, FEET + 10, w=640)
        if t <= b["koi"]:
            px, py = BX + 20, FEET + 150 * S - 400 * S
            dark_phone(ctx, px, py)
        else:
            dark_phone(ctx, 640, FEET - 175)


class Aunty(Cued):
    def beats(self, d):
        return {"aunty": self.cue("AUNTY", d * 0.2)}

    def events(self, d):
        b = self.beats(d)
        return [(b["aunty"], "soft_thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        op = ease_out_cubic(clamp((t - b["aunty"] + 0.3) / 0.5))
        boy_room(ctx, t, altar=1.0, dim=0.6 * (1 - op))
        door(ctx, 900, FEET, open_=op, light=True)
        if op > 0:
            ctx.move_to(750, FEET - 760)
            ctx.line_to(1050, FEET - 760)
            ctx.line_to(900, FEET)
            ctx.line_to(420, FEET + 40)
            ctx.close_path()
            rgba(ctx, hexc("#FFE0A0"), 0.12 * op)
            ctx.fill()
        boy(ctx, BX, FEET, S, t, pose="tired", mood="shock" if op > 0.5 else "low", look=(1.0, -0.2), seated=True)
        blanket(ctx, BX, S, t, shiver=0.3)
        bed(ctx, BX + 40, FEET + 10, w=640)
        walk = ease_out_cubic(clamp((t - b["aunty"] - 0.2) / 1.2))
        if walk > 0:
            ax = lerp(960, 790, walk)
            aunty(ctx, ax, FEET, S, t, pose="give", mood="neutral", look=(-0.6, 0.2), flip=True, a=clamp(walk * 3))
            khichdi(ctx, ax - 150 * S, FEET - 470 * S, t, a=clamp(walk * 3))


class Bheji(Cued):
    def beats(self, d):
        return {"mummy": self.cue("MUMMY", d * 0.4)}

    def events(self, d):
        b = self.beats(d)
        return [(b["mummy"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        boy_room(ctx, t, altar=1.0)
        door(ctx, 900, FEET, open_=1.0, light=True)
        boy(ctx, BX, FEET, S, t, pose="offer" if t > b["mummy"] else "tired", mood="shock", look=(1.0, -0.3),
            seated=True)
        blanket(ctx, BX, S, t, shiver=0.2)
        bed(ctx, BX + 40, FEET + 10, w=640)
        aunty(ctx, 760, FEET, S, t, pose="give", mood="joy", look=(-0.6, 0.2), flip=True)
        khichdi(ctx, 760 - 150 * S, FEET - 470 * S, t)
        mem = clamp((t - b["mummy"] + 0.1) / 0.4)

        def inside():
            mummy_home(ctx, t, lit=1.0)
            mummy_on_phone(ctx, 760, S, t, mood="cry")
        ctx.save()
        memory_bubble(ctx, 900, 300, 160, t, mem, lambda: _scaled(ctx, 900, 300, 0.32, inside))
        ctx.restore()


def _scaled(ctx, cx, cy, k, fn):
    """Draw a full-screen picture fn() shrunk by k around (cx, cy) (for the memory bubble)."""
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(k, k)
    ctx.translate(-760, -(FEET - 420))
    fn()
    ctx.restore()


class Pankh(Cued):
    def beats(self, d):
        return {"mor": self.cue("MOR PANKH", d * 0.5)}

    def events(self, d):
        b = self.beats(d)
        return [(b["mor"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        boy_room(ctx, t, altar=1.0)
        reveal = clamp((t - b["mor"] + 0.4) / 0.5)
        lift = clamp((t - b["mor"] - 0.4) / 0.5)
        kanha_light(ctx, 820, 0.72, t, a=0.15 + 0.4 * lift)
        boy(ctx, BX, FEET, S, t, pose="feather" if lift > 0 else "offer", mood="cry" if lift > 0 else "shock",
            look=(0.3, 0.2), seated=True)
        bed(ctx, BX + 40, FEET + 10, w=640)
        khichdi(ctx, 640, FEET - 200, t, open_=reveal)
        if reveal > 0 and lift <= 0:
            glow(ctx, 640, FEET - 230, 150, GOLDEN, 0.6 * reveal)
            dv.peacock_feather(ctx, 600, FEET - 222, -0.15, 130, t, a=reveal)
            sparkle_burst(ctx, 640, FEET - 240, reveal, c=GOLD_HI, n=12, r=160)
        if lift > 0:
            glow(ctx, BX, FEET + 108 - 640 * S, 160, GOLDEN, 0.4 * lift)


class Sorry(Cued):
    def beats(self, d):
        return {"sorry": self.cue("SORRY", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["sorry"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        joy = clamp((t - b["sorry"]) / 0.4)

        def left():
            boy_room(ctx, t, altar=0.6 + 0.4 * joy)
            boy(ctx, 270, FEET, S, t, pose="phone", mood="cry", look=(0.5, 0.3))

        def right():
            mummy_home(ctx, t, lit=0.7 + 0.5 * joy)
            mummy_on_phone(ctx, 760, S, t, mood="cry" if joy < 0.5 else "joy")
            if joy > 0:
                glow(ctx, 760, FEET - 520, 260, GOLDEN, 0.3 * joy)
        split(ctx, t, left, right)
        if joy > 0:
            dv.petals(ctx, t, n=16, seed=4, a=0.8 * joy)


class Jai(Cued):
    def beats(self, d):
        return {"jai": self.cue("JAI", d * 0.7)}

    def events(self, d):
        return [(0.1, "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        boy_room(ctx, t, altar=1.0)
        rise = ease_out_cubic(clamp(t / 0.9))
        glow(ctx, 760, FEET - 460, 460, GOLDEN, 0.5 * rise)
        dv.krishna(ctx, 760, FEET + 60 * (1 - rise), 0.76, t, pose="bless" if t > b["jai"] - 0.6 else "flute",
                   a=0.9 * rise)
        dv.petals(ctx, t, n=26, seed=11, a=0.9)
        boy(ctx, 300, FEET, S, t, pose="namaste", mood="joy", look=(0.9, -0.5))
        x = clamp((t - (d - 0.45)) / 0.45)                                     # loop into the hook's frame 0
        if x > 0:
            ctx.push_group()
            Calls().draw(ctx, 0.0, d)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(x)


SCENE_CLASSES = {"calls": Calls, "mat": Mat, "bukhar": Bukhar, "band": Band, "aunty": Aunty, "bheji": Bheji,
                 "pankh": Pankh, "sorry": Sorry, "jai": Jai}

UPLOAD = {
    "titles": [
        "Mummy Ke 27 Missed Call... Aur Kanha Sab Dekh Rahe The #shorts",
        "Mummy Har Baat Pe Phone Mat Kiya Karo... Phir Us Raat #shorts",
        "Khichdi Ke Kapde Mein Mor Pankh Tha #shorts",
    ],
    "thumb_text": "MUMMY SORRY",
    "queries": [
        "maa ki kahani",
        "krishna ki kahani",
        "emotional maa story hindi",
    ],
    "description": """
Mummy ke 27 missed call the... aur Kanha sab dekh rahe the. Ghar se door rehne wale har bachche ki kahani -
bukhaar ki raat, band phone, aur mummy ki bheji khichdi mein rakha ek mor pankh. Jai Shri Krishna.

Kalpanik prerak katha.

Aakhri baar aapne mummy ko khud phone kab kiya tha? Comment mein likho - aur aaj ek baar zaroor kar lena.
""",
    "tags": [
        "maa ki kahani", "mummy", "emotional story hindi", "krishna ki kahani", "jai shri krishna", "kanha",
        "mor pankh", "hostel life", "ghar se door", "maa beta", "divya rahasya", "karm aur kripa", "prerak katha",
        "shorts",
    ],
    "hashtags": ["#Shorts", "#JaiShriKrishna", "#Maa"],
    "pinned_comment": "Sach batao 🥺 aakhri baar mummy ko khud phone kab kiya tha? Aaj ek baar zaroor karna. Aur agar "
                      "aap bhi ghar se door ho to likho - hum sab milke Kanha ji se aapke ghar walon ke liye prarthana "
                      "karenge. Jai Shri Krishna 🙏",
}


def thumbnail(ctx):
    def left():
        boy_room(ctx, 0.5, altar=1.0)
        boy(ctx, 270, FEET, S, 0.5, pose="phone", mood="cry", look=(0.5, 0.3))

    def right():
        mummy_home(ctx, 0.5, lit=1.2)
        glow(ctx, 760, FEET - 520, 260, GOLDEN, 0.3)
        mummy_on_phone(ctx, 760, S, 0.5, mood="cry")
    split(ctx, 0.5, left, right)
    text(ctx, "27 MISSED CALL", 540, 1330, 104, hexc("#FFFFFF"), font=CAPTION_FONT, bold=False,
         stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "MUMMY SORRY", 540, 1470, 130, PINK, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
