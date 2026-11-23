"""Daadi ka Morpankh: Karm Aur Kripa - a modern student fails three times, finds his late grandmother's mor-pankh in her
Gita ("karm kar beta, phal Kanha par chhod de"), works for a year and tops the list (~60 s, 8 scenes, length test).

Usage (from SanatanKatha/):
  python make.py daadi_morpankh --preview
  python make.py daadi_morpankh --check
  python make.py daadi_morpankh --kiki-split --check-voice
  python make.py daadi_morpankh --engine files

Kalpanik prerak katha (fictional). Mehnat first: the boy works hard every day; faith only gives him the strength to
get up again. Krishna appears only as a sign (the mor-pankh and its golden light). The last line ("yaad hai wo din
jab") loops into the hook ("teesri baar bhi list mein uska naam nahi tha").
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
from core.devta import group, place, smooth, ink, ell, limb, hand, sheen, eye, shade

from kathas.ghatotkach_akshauhini import ease_in
from kathas.eklavya_krishna import sparkle_burst, edge_glow

TOPIC = "KARM AUR KRIPA DAADI KA MORPANKH TEESRI BAAR FAIL STUDENT"
OUTPUTS = {"edge": "daadi_morpankh_short.mp4"}
MUSIC_STYLE = "pulse"     # modern, emotional; yuyutsu used ambient
MUSIC_BPM = 76            # >= 6 BPM away from the last kathas (82 / 89)
MUSIC_VOLUME = 0.11
TAIL_PAD = 0.22           # calm storytelling breath (user, 23 Nov)
MAX_GAP = 0.25
LENGTH_TEST_SECONDS = 80  # user-approved one-off test of a 60-75 s story Short (23 Nov 2026)
LENGTH_TEST_WORDS = 200

FEET = GROUND - 10
SKIN = hexc("#C68A5E")
HAIR = hexc("#1A120E")
TEE = hexc("#3A6EA8")
JEANS = hexc("#2C3A55")
PAPA_KURTA = hexc("#E8DFC8")
PAPA_SKIN = hexc("#B97E54")
GOLDEN = hexc("#FFD27A")

SOURCES = [
    "Original fictional story (Kalpanik prerak katha) - no scripture or real-event claim; labelled in the description.",
    "Bhagavad Gita 2.47 (karmanye vadhikaraste ma phaleshu kadachana): the grandmother's line 'karm kar beta, phal "
    "Kanha par chhod de' is its meaning in simple words.",
]


# =============================================================================
# Rooms and props
# =============================================================================
def room_bg(ctx, t, night=1.0, lamp=0.0):
    """Small middle-class room: warm wall, window with sky (night/day), bed, almirah, desk with lamp."""
    wall_top = hexc("#3A3550") if night > 0.5 else hexc("#C9A77E")
    wall_bot = hexc("#24203A") if night > 0.5 else hexc("#9C7A58")
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *wall_top)
    g.add_color_stop_rgb(0.62, *wall_bot)
    g.add_color_stop_rgb(1, *shade(wall_bot, 0.6))
    ctx.set_source(g)
    ctx.rectangle(-80, -80, W + 160, H + 160)
    ctx.fill()
    for k in range(9):                                      # faint wall texture
        line(ctx, [(-80, 300 + 90 * k), (W + 80, 300 + 90 * k)], shade(wall_bot, 1.15), 2, 0.12)
    window(ctx, 150, 330, 300, 340, t, night)
    ctx.rectangle(-80, GROUND - 30, W + 160, H)              # floor
    rgba(ctx, hexc("#4A3426") if night > 0.5 else hexc("#7A5A3E"))
    ctx.fill()
    for k in range(7):
        line(ctx, [(-80 + 180 * k, GROUND - 30), (-160 + 180 * k, H)], hexc("#2E2018"), 3, 0.35)
    if lamp > 0:
        glow(ctx, 860, 760, 420, hexc("#FFD9A0"), 0.35 * lamp)
    for i in range(18):                                      # dust in the lamp light
        x = (rnd(i, 3) * W + t * 12) % W
        y = 500 + 600 * rnd(i, 5) + 10 * math.sin(t + i)
        circle(ctx, x, y, 2 + 2 * rnd(i, 6), hexc("#FFE9C0"), 0.18)


def window(ctx, x, y, w, h, t, night):
    if night > 0.5:
        g = cairo.LinearGradient(0, y, 0, y + h)
        g.add_color_stop_rgb(0, *hexc("#0E1230"))
        g.add_color_stop_rgb(1, *hexc("#3A2A5A"))
    else:
        g = cairo.LinearGradient(0, y, 0, y + h)
        g.add_color_stop_rgb(0, *hexc("#7FB8E8"))
        g.add_color_stop_rgb(1, *hexc("#FFD9A0"))
    ctx.set_source(g)
    ctx.rectangle(x, y, w, h)
    ctx.fill()
    if night > 0.5:
        circle(ctx, x + w * 0.72, y + 80, 34, hexc("#F4EFD8"))
        glow(ctx, x + w * 0.72, y + 80, 90, hexc("#F4EFD8"), 0.4)
        for i in range(12):
            circle(ctx, x + w * rnd(i, 1), y + h * 0.5 * rnd(i, 2), 2, (1, 1, 1), 0.5 + 0.4 * math.sin(t * 3 + i))
    else:
        dv.sun_disc(ctx, x + w * 0.3, y + 90, 40, t, a=0.8, rays=10)
    for i in range(8):                                       # city skyline
        bw = w / 8
        bh = 60 + 90 * rnd(i, 7)
        ctx.rectangle(x + i * bw, y + h - bh, bw - 4, bh)
        rgba(ctx, hexc("#151228") if night > 0.5 else hexc("#6A7A8A"))
        ctx.fill()
        if night > 0.5:
            for j in range(3):
                circle(ctx, x + i * bw + 10 + 12 * j, y + h - bh + 20, 3, hexc("#FFD27A"), 0.7 * rnd(i, j))
    rrect(ctx, x - 14, y - 14, w + 28, h + 28, 6)
    rgba(ctx, hexc("#5A3A22"))
    ctx.set_line_width(16)
    ctx.stroke()
    line(ctx, [(x + w / 2, y), (x + w / 2, y + h)], hexc("#5A3A22"), 10)
    line(ctx, [(x, y + h / 2), (x + w, y + h / 2)], hexc("#5A3A22"), 10)


def bed(ctx, x, y, w=460):
    """Bed front, drawn over a seated character's legs."""
    rrect(ctx, x - w / 2, y - 120, w, 120, 14)
    ink(ctx, hexc("#7A4A2A"), 4)
    rrect(ctx, x - w / 2 + 10, y - 160, w - 20, 56, 20)
    ink(ctx, hexc("#C8D4E8"), 4)
    line(ctx, [(x - w / 2 + 20, y - 70), (x + w / 2 - 20, y - 70)], hexc("#5A3420"), 4, 0.6)


def almirah(ctx, x, y, t, shake=0.0, open_=0.0):
    ctx.save()
    ctx.translate(x + 4 * shake * math.sin(t * 60), y)
    rrect(ctx, -130, -700, 260, 700, 10)
    ink(ctx, hexc("#6A4428"), 5)
    line(ctx, [(0, -690), (0, -10)], hexc("#3A2414"), 5)
    for sx in (-20, 20):
        circle(ctx, sx, -360, 9, GOLD)
    if open_ > 0:                                            # right door swings, gold light inside
        glow(ctx, 60, -420, 200, GOLDEN, 0.5 * open_)
    ctx.restore()


def desk(ctx, x, y, t, lamp=1.0, feather=False, books=3):
    """Study desk front (covers a seated character's legs) with lamp, books and optional mor-pankh."""
    for k in range(books):
        rrect(ctx, x - 270 + 8 * k, y - 220 - 26 * k, 160, 24, 4)
        ink(ctx, hexc(("#B8321E", "#2E6A8A", "#3A8A4A", "#C88A2A")[k % 4]), 3)
    line(ctx, [(x + 230, y - 200), (x + 200, y - 340), (x + 250, y - 390)], hexc("#3A3A40"), 10)   # lamp arm
    ctx.move_to(x + 210, y - 390)
    ctx.line_to(x + 300, y - 370)
    ctx.line_to(x + 270, y - 330)
    ctx.close_path()
    ink(ctx, hexc("#E0B040"), 3)
    if lamp > 0:
        glow(ctx, x + 260, y - 300, 220, hexc("#FFE0A0"), 0.5 * lamp)
    if feather:
        dv.peacock_feather(ctx, x + 150, y - 206, -0.35, 150, t, a=1.0)
        glow(ctx, x + 180, y - 250, 80, GOLDEN, 0.25 + 0.1 * math.sin(t * 3))
    rrect(ctx, x - 320, y - 200, 640, 36, 6)                  # desk top
    ink(ctx, hexc("#8A5A34"), 4)
    rrect(ctx, x - 300, y - 164, 600, 164, 6)                 # desk front
    ink(ctx, hexc("#6A4428"), 4)
    rrect(ctx, x - 120, y - 140, 240, 60, 6)
    ink(ctx, hexc("#7A5034"), 3)
    circle(ctx, x, y - 110, 8, GOLD)


def phone(ctx, x, y, ang, t, glow_a=0.6, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    rrect(ctx, -26, -46, 52, 92, 9)
    ink(ctx, hexc("#1A1A22"), 3)
    rrect(ctx, -20, -38, 40, 74, 4)
    rgba(ctx, hexc("#9AD0FF"), a)
    ctx.fill()
    ctx.restore()
    if glow_a > 0:
        glow(ctx, x, y, 90, hexc("#9AD0FF"), glow_a * a)


def trunk(ctx, x, y, lid=0.0, books=0.0, glow_a=0.0):
    """Tin trunk (baksa). lid 0 = closed, 1 = fully open (lid raised)."""
    if glow_a > 0:
        glow(ctx, x, y - 120, 220, GOLDEN, 0.5 * glow_a)
    rrect(ctx, x - 170, y - 160, 340, 160, 10)
    ink(ctx, hexc("#3A6A5A"), 4)
    for k in (-1, 1):
        line(ctx, [(x + 110 * k, y - 160), (x + 110 * k, y)], hexc("#2A4A3E"), 6)
    if books > 0:
        for k in range(int(4 * books)):
            rrect(ctx, x - 140 + 70 * k, y - 190, 60, 40, 4)
            ink(ctx, hexc(("#B8321E", "#2E6A8A", "#3A8A4A", "#C88A2A")[k % 4]), 3)
    ctx.save()
    ctx.translate(x - 170, y - 160)
    ctx.rotate(-1.6 * lid)
    rrect(ctx, 0, -40, 340, 44, 10)
    ink(ctx, hexc("#4A7A6A"), 4)
    rrect(ctx, 150, -10, 40, 20, 4)
    ink(ctx, GOLD, 2)
    ctx.restore()


def gita_book(ctx, x, y, ang, open_=0.0, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    if open_ > 0.5:
        for side in (-1, 1):
            rrect(ctx, 0 if side > 0 else -110, -70, 110, 140, 6)
            ink(ctx, hexc("#F3E6C8"), 3)
            for k in range(6):
                line(ctx, [(side * 14, -50 + 18 * k), (side * 92, -50 + 18 * k)], hexc("#9A7A5A"), 3, 0.6)
    else:
        rrect(ctx, -70, -90, 140, 180, 8)
        ink(ctx, hexc("#A0281E"), 4)
        rrect(ctx, -52, -72, 104, 144, 6)
        rgba(ctx, GOLD, 0.8)
        ctx.set_line_width(4)
        ctx.stroke()
        circle(ctx, 0, 0, 22, GOLD)
    ctx.restore()


def daadi_photo(ctx, x, y, t, lit=0.0, s=1.0):
    """Framed photo of the late grandmother with a marigold garland and a diya below."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if lit > 0:
        glow(ctx, 0, 0, 230, GOLDEN, 0.45 * lit)
    rrect(ctx, -110, -140, 220, 280, 10)
    ink(ctx, hexc("#7A4A1E"), 5)
    rrect(ctx, -90, -120, 180, 240, 6)
    rgba(ctx, hexc("#D8C8A8"))
    ctx.fill()
    ell(ctx, 0, 90, 80, 50)                                  # shoulders in a white saree
    ink(ctx, hexc("#F4F0E6"), 3)
    ell(ctx, 0, -10, 46, 54)
    ink(ctx, hexc("#C8946A"), 3)
    ell(ctx, 0, -62, 50, 26)                                 # white hair
    ink(ctx, hexc("#EDEDED"), 3)
    circle(ctx, 0, -80, 18, hexc("#EDEDED"))
    for side in (-1, 1):                                     # spectacles + kind eyes
        ctx.arc(side * 18, -14, 13, 0, math.tau)
        rgba(ctx, hexc("#3A2A1A"))
        ctx.set_line_width(3)
        ctx.stroke()
        circle(ctx, side * 18, -14, 4, hexc("#2A1A10"))
    line(ctx, [(-14, 18), (0, 25), (14, 18)], hexc("#7A3A2A"), 3)
    circle(ctx, 0, -32, 4, hexc("#C8202A"))
    for k in range(13):                                      # garland
        ang = math.pi * (k / 12)
        circle(ctx, 112 * math.cos(ang) * 0.95, -150 + 150 * math.sin(ang) * 0.55 + 10, 11,
               hexc("#FF8A1E") if k % 2 else hexc("#FFC21E"))
    ctx.restore()
    dv.diya(ctx, x, y + 175 * s, 0.9 * s, t, a=1.0)


def home_altar(ctx, x, y, t, lit=1.0):
    """Small wall shelf mandir: Kanha ji's murti with a diya and marigolds (the family's faith, seen every night)."""
    glow(ctx, x, y - 90, 150, GOLDEN, 0.35 * lit + 0.05 * math.sin(t * 2))
    rrect(ctx, x - 90, y, 180, 18, 4)
    ink(ctx, hexc("#7A4A1E"), 3)
    smooth(ctx, [(x - 80, y), (x - 80, y - 150), (x, y - 200), (x + 80, y - 150), (x + 80, y)], k=0.05)
    rgba(ctx, hexc("#5A2A1E"), 0.85)
    ctx.fill()
    dv.krishna(ctx, x, y - 4, 0.2, t, pose="flute", aura=False)
    dv.diya(ctx, x + 60, y - 6, 0.45, t, a=1.0)
    for k in range(5):
        circle(ctx, x - 70 + 35 * k, y + 22, 8, hexc("#FF8A1E") if k % 2 else hexc("#FFC21E"))


def kanha_light(ctx, x, s, t, a=0.5, pose="bless"):
    """Kanha ji in golden light - a soft, translucent divine presence (no text)."""
    if a <= 0:
        return
    glow(ctx, x, FEET - 520 * s, 420 * s, GOLDEN, 0.45 * a)
    dv.krishna(ctx, x, FEET, s, t, pose=pose, a=a)


def temple_bg(ctx, t):
    """Neighbourhood temple at dusk: orange sky, small shikhara, bell, rows of diyas."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in ((0.0, "#2A1A3A"), (0.35, "#8A3A4A"), (0.55, "#FF9A4A"), (0.68, "#4A2A2A"), (1.0, "#2A1810")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.rectangle(-80, -80, W + 160, H + 160)
    ctx.fill()
    dv.sun_disc(ctx, 200, 820, 70, t, a=0.8, rays=12)
    smooth(ctx, [(560, 1040), (560, 640), (640, 470), (720, 330), (800, 470), (880, 640), (880, 1040)], k=0.06)
    ink(ctx, hexc("#E8C49A"), 5)
    for k in range(5):
        line(ctx, [(600 + 10 * k, 620 + 80 * k), (840 - 10 * k, 620 + 80 * k)], hexc("#B88A5A"), 4, 0.7)
    line(ctx, [(720, 330), (720, 260)], hexc("#7A4A1E"), 6)
    ctx.move_to(720, 260)
    ctx.line_to(790, 285)
    ctx.line_to(720, 305)
    ctx.close_path()
    ink(ctx, hexc("#FF7A1E"), 3)
    rrect(ctx, 650, 860, 140, 180, 60)                        # sanctum door with warm light
    rgba(ctx, hexc("#FFD27A"), 0.9)
    ctx.fill()
    glow(ctx, 720, 950, 200, GOLDEN, 0.5)
    dv.krishna(ctx, 720, 1036, 0.2, t, pose="flute", aura=False)   # Kanha ji's murti inside
    ctx.rectangle(-80, GROUND - 30, W + 160, H)
    rgba(ctx, hexc("#5A3A2A"))
    ctx.fill()
    for k in range(9):
        dv.diya(ctx, 80 + 115 * k, GROUND - 24, 0.55, t + k, a=1.0)


def bell(ctx, x, y, t, ring=0.0):
    sw = 0.35 * ring * math.sin(t * 14)
    ctx.save()
    ctx.translate(x, y)
    line(ctx, [(0, -80), (0, 0)], hexc("#5A3A1E"), 5)
    ctx.rotate(sw)
    smooth(ctx, [(-34, 70), (-28, 20), (-14, 0), (14, 0), (28, 20), (34, 70)], k=0.1)
    ink(ctx, GOLD, 4)
    circle(ctx, 0, 76, 9, GOLD_DK)
    ctx.restore()


def clock(ctx, x, y, t, ring=0.0):
    jit = 6 * ring * math.sin(t * 50)
    circle(ctx, x + jit, y, 64, hexc("#C8202A"))
    circle(ctx, x + jit, y, 52, hexc("#F4F0E6"))
    for side in (-1, 1):
        circle(ctx, x + jit + side * 46, y - 56, 18, hexc("#C8202A"))
    line(ctx, [(x + jit, y), (x + jit, y - 38)], hexc("#2A1A10"), 6)            # 4 o'clock
    line(ctx, [(x + jit, y), (x + jit + 26, y + 14)], hexc("#2A1A10"), 7)
    if ring > 0:
        for side in (-1, 1):
            for k in range(2):
                line(ctx, [(x + side * (80 + 16 * k), y - 30), (x + side * (100 + 16 * k), y - 50)], hexc("#FFE38A"),
                     4, ring)


def sweets_box(ctx, x, y, a=1.0):
    rrect(ctx, x - 60, y - 40, 120, 70, 8)
    rgba(ctx, hexc("#FF8A1E"), a)
    ctx.fill()
    line(ctx, [(x - 60, y - 6), (x + 60, y - 6)], hexc("#C8202A"), 8, a)
    line(ctx, [(x, y - 40), (x, y + 30)], hexc("#C8202A"), 8, a)


def relatives(ctx, x0, n, t, laugh=1.0, sweets=False, a=1.0):
    """Relatives as dark silhouettes in a doorway; bobbing when they laugh. sweets: front one holds a box."""
    for i in range(n):
        x = x0 + 120 * i
        bob = 10 * laugh * abs(math.sin(t * 9 + i * 1.3))
        y = FEET - 30 - bob
        s = 0.9 - 0.05 * (i % 2)
        c = hexc("#1A1424")
        ell(ctx, x, y - 280 * s, 70 * s, 150 * s)
        rgba(ctx, c, a)
        ctx.fill()
        circle(ctx, x, y - 470 * s, 52 * s, c, a)
        if i % 2 == 0:                                       # a cap / bun for variety
            circle(ctx, x + 10, y - 520 * s, 26 * s, c, a)
        if laugh > 0:                                        # open laughing mouths as a light slit
            ell(ctx, x + 14, y - 455 * s, 14 * s, 8 * s * (0.5 + 0.5 * abs(math.sin(t * 9 + i))))
            rgba(ctx, hexc("#8A6A7A"), 0.6 * a)
            ctx.fill()
        if sweets and i == 0:
            sweets_box(ctx, x + 70, y - 300 * s, a)


# =============================================================================
# The student (modern boy: short hair, blue t-shirt, jeans - no crown, no tilak)
# =============================================================================
def _boy_face(ctx, t, mood, look):
    rrect(ctx, -28, -600, 56, 64, 14)
    ink(ctx, SKIN)
    for side in (-1, 1):
        ell(ctx, side * 90, -684, 16, 24)
        ink(ctx, SKIN)
    ell(ctx, 0, -690, 90, 100)
    ink(ctx, SKIN)
    sheen(ctx, -30, -736, 32, 18, 0.12)
    closed = mood in ("sad", "cry_closed")
    for side in (-1, 1):
        eye(ctx, side * 34, -696, 20, 24, t, look=look, closed=closed, seed=7, iris=hexc("#2A1A10"), skin=SKIN,
            lid=0.3 if mood in ("tired", "low") else 0.0)
        if mood in ("sad", "low", "tired", "cry", "cry_closed"):
            line(ctx, [(side * 14, -738), (side * 36, -734), (side * 58, -722)], HAIR, 7)   # worried brows
        elif mood == "joy":
            line(ctx, [(side * 14, -744), (side * 36, -752), (side * 58, -744)], HAIR, 7)
        else:
            line(ctx, [(side * 14, -738), (side * 36, -742), (side * 58, -738)], HAIR, 7)
    ell(ctx, 0, -664, 10, 14)
    ink(ctx, shade(SKIN, 0.88), 3)
    if mood == "joy":
        ell(ctx, 0, -620, 26, 16)
        ink(ctx, hexc("#7A2A1E"), 3)
        ctx.rectangle(-20, -630, 40, 8)
        rgba(ctx, (1, 1, 1))
        ctx.fill()
    elif mood in ("sad", "low", "cry", "cry_closed", "tired"):
        line(ctx, [(-16, -612), (0, -620), (16, -612)], hexc("#5A2A1E"), 5)
    elif mood == "shock":
        ell(ctx, 0, -616, 11, 14)
        ink(ctx, hexc("#5A1A10"), 3)
    else:
        line(ctx, [(-14, -616), (14, -616)], hexc("#5A2A1E"), 5)
    if mood in ("cry", "cry_closed"):                        # tears
        for side in (-1, 1):
            fu = (t * 0.9 + (0.5 if side > 0 else 0)) % 1
            circle(ctx, side * 40, -676 + 60 * fu, 7, hexc("#9AD8FF"), 0.9 * (1 - fu))
    for k in range(10):                                      # short modern hair
        circle(ctx, -86 + 19 * k, -772 - 14 * math.sin(k / 9 * math.pi), 22, HAIR)
    ell(ctx, 0, -790, 86, 44)
    ink(ctx, HAIR, 3)
    smooth(ctx, [(-70, -790), (-10, -830), (60, -800), (20, -770)])
    ink(ctx, HAIR, 0)


def boy(ctx, x, y, s, t, pose="stand", mood="neutral", look=(0.0, 0.0), flip=False, a=1.0, seated=False):
    """pose: stand | phone | drop | carry | feather | write | tired | joy | namaste | hug.
    seated=True lowers the body 230 px so a bed/desk drawn afterwards hides the legs."""
    def draw():
        place(ctx, x, y + (150 * s if seated else 0), s, t, flip)
        slump = 30 if pose in ("drop", "tired") else 0
        if not seated:
            for side in (-1, 1):
                limb(ctx, [(side * 50, -330), (side * 54, -170), (side * 52, -34)], JEANS, 50)
                ell(ctx, side * 60, -16, 46, 18)
                ink(ctx, hexc("#F0F0F0"))
        rrect(ctx, -118, -360, 236, 50, 14)                  # jeans waist
        ink(ctx, JEANS)
        ctx.save()
        ctx.translate(0, slump)
        smooth(ctx, [(-130, -540), (-70, -560), (70, -560), (130, -540), (134, -440), (120, -350), (-120, -350),
                     (-134, -440)])
        ink(ctx, TEE)
        line(ctx, [(-40, -556), (0, -520), (40, -556)], shade(TEE, 0.7), 5)
        L, R = (-128, -525), (128, -525)
        if pose == "phone":
            arms = [(L, (-150, -420), (-40, -470)), (R, (150, -420), (40, -480))]
        elif pose == "drop":
            arms = [(L, (-150, -420), (-140, -330)), (R, (150, -420), (140, -330))]
        elif pose == "carry":
            arms = [(L, (-110, -420), (60, -440)), (R, (150, -430), (180, -450))]
        elif pose == "feather":
            arms = [(L, (-130, -430), (-20, -520)), (R, (130, -430), (20, -520))]
        elif pose == "write":
            arms = [(L, (-150, -420), (-60, -380)), (R, (150, -420), (90 + 20 * math.sin(t * 9), -380))]
        elif pose == "tired":
            arms = [(L, (-150, -440), (-30, -420)), (R, (150, -440), (30, -420))]
        elif pose == "joy":
            arms = [(L, (-200, -620), (-210, -760)), (R, (200, -620), (210, -760))]
        elif pose == "namaste":
            arms = [(L, (-120, -420), (-14, -500)), (R, (120, -420), (14, -500))]
        elif pose == "hug":
            arms = [(L, (-170, -460), (40, -470)), (R, (170, -480), (260, -470))]
        elif pose == "pour":                                 # pouring jal from a lota (added for bees_baar_reject)
            arms = [(L, (-110, -430), (110, -470)), (R, (150, -440), (160, -470))]
        elif pose == "ride":                                 # both hands forward on handlebars
            arms = [(L, (-90, -440), (150, -470)), (R, (160, -440), (210, -470))]
        else:
            arms = [(L, (-150, -420), (-150, -330)), (R, (150, -420), (150, -330))]
        for sh, el, hd in arms:
            mid = (lerp(sh[0], el[0], 0.55), lerp(sh[1], el[1], 0.55))
            limb(ctx, [mid, el, hd], SKIN, 40)               # bare forearm
            limb(ctx, [sh, mid], TEE, 52)                    # short sleeve
            if pose != "namaste":
                hand(ctx, *hd, SKIN, 22)
        if pose == "namaste":
            smooth(ctx, [(0, -540), (20, -505), (18, -460), (0, -440), (-18, -460), (-20, -505)])
            ink(ctx, SKIN)
        if pose == "phone":
            phone(ctx, 0, -490, 0.0, t, glow_a=0.5)
        if pose == "feather":
            dv.peacock_feather(ctx, 0, -520, -1.45, 180, t, a=1.0)
            glow(ctx, 0, -640, 120, GOLDEN, 0.4 + 0.15 * math.sin(t * 3))
        if pose == "pour":
            smooth(ctx, [(120, -500), (200, -500), (210, -450), (160, -420), (110, -450)])     # brass lota
            ink(ctx, GOLD, 3)
            for k in range(6):
                fu = (t * 2 + k / 6) % 1
                circle(ctx, 215 + 10 * fu, -470 + 260 * fu, 6, hexc("#9AD8FF"), 0.85)
        if pose == "carry":
            for k in range(4):
                rrect(ctx, 20 + 4 * k, -500 - 24 * k, 170, 22, 4)
                ink(ctx, hexc(("#B8321E", "#2E6A8A", "#3A8A4A", "#C88A2A")[k]), 3)
        ctx.translate(0, 40 if pose == "tired" else (20 if pose == "drop" else 0))
        _boy_face(ctx, t, mood, look)
        ctx.restore()
        ctx.restore()
    group(ctx, a, draw)


# =============================================================================
# Papa (cream kurta, greying hair, moustache, spectacles)
# =============================================================================
def papa(ctx, x, y, s, t, pose="stand", mood="sad", flip=False, a=1.0):
    """pose: stand | away (seen from behind, walking off) | hug (arms open around the son)."""
    def draw():
        place(ctx, x, y, s, t, flip)
        for side in (-1, 1):
            limb(ctx, [(side * 50, -320), (side * 54, -170), (side * 52, -34)], hexc("#D8D0BC"), 52)
            ell(ctx, side * 62, -16, 46, 18)
            ink(ctx, hexc("#5A3A22"))
        smooth(ctx, [(-140, -560), (140, -560), (150, -300), (130, -240), (-130, -240), (-150, -300)], k=0.12)
        ink(ctx, PAPA_KURTA)
        if pose != "away":
            for k in range(4):
                circle(ctx, 0, -530 + 40 * k, 5, hexc("#B8A880"))
        L, R = (-136, -535), (136, -535)
        if pose == "hug":
            arms = [(L, (-190, -470), (-60, -460)), (R, (190, -470), (60, -470))]
        else:
            arms = [(L, (-160, -420), (-150, -320)), (R, (160, -420), (150, -320))]
        for sh, el, hd in arms:
            limb(ctx, [sh, el, hd], PAPA_KURTA, 50)
            hand(ctx, *hd, PAPA_SKIN, 22)
        rrect(ctx, -28, -610, 56, 64, 14)
        ink(ctx, PAPA_SKIN)
        ell(ctx, 0, -700, 92, 102)
        ink(ctx, PAPA_SKIN)
        if pose == "away":                                   # back of the head
            ell(ctx, 0, -730, 92, 80)
            ink(ctx, hexc("#3A3434"), 3)
            for k in range(5):
                line(ctx, [(-50 + 25 * k, -790), (-46 + 25 * k, -680)], hexc("#8A8A8A"), 3, 0.6)
        else:
            for side in (-1, 1):
                eye(ctx, side * 34, -706, 19, 22, t, closed=mood in ("cry", "sad"), seed=11, iris=hexc("#2A1A10"),
                    skin=PAPA_SKIN, lid=0.25)
                ctx.arc(side * 34, -706, 28, 0, math.tau)    # spectacles
                rgba(ctx, hexc("#2A2A2A"))
                ctx.set_line_width(5)
                ctx.stroke()
            line(ctx, [(-6, -706), (6, -706)], hexc("#2A2A2A"), 5)
            smooth(ctx, [(-44, -652), (0, -664), (44, -652), (34, -638), (0, -646), (-34, -638)])   # moustache
            ink(ctx, hexc("#3A3434"), 2)
            if mood == "cry":
                line(ctx, [(-16, -620), (0, -628), (16, -620)], hexc("#5A2A1E"), 5)
                for side in (-1, 1):
                    fu = (t * 0.8 + (0.4 if side > 0 else 0)) % 1
                    circle(ctx, side * 40, -688 + 70 * fu, 7, hexc("#9AD8FF"), 0.9 * (1 - fu))
            else:
                line(ctx, [(-16, -624), (16, -624)], hexc("#5A2A1E"), 5)
            ell(ctx, 0, -786, 86, 36)                        # greying hair
            ink(ctx, hexc("#3A3434"), 3)
            for side in (-1, 1):
                ell(ctx, side * 80, -746, 16, 30)
                ink(ctx, hexc("#9A9A9A"), 2)
        ctx.restore()
    group(ctx, a, draw)


def door(ctx, x, y, open_=1.0, light=True):
    """Doorway to the hall; open_ 0 = shut."""
    rrect(ctx, x - 150, y - 760, 300, 760, 6)
    rgba(ctx, hexc("#FFD9A0") if light else hexc("#2A2030"), 0.95)
    ctx.fill()
    w = 300 * (1 - open_)
    if w > 2:
        ctx.rectangle(x - 150, y - 760, w, 760)
        rgba(ctx, hexc("#7A5034"))
        ctx.fill()
    rrect(ctx, x - 160, y - 770, 320, 780, 6)
    rgba(ctx, hexc("#5A3A22"))
    ctx.set_line_width(18)
    ctx.stroke()


# =============================================================================
# Story: 8 scenes, 197 spoken words (single narrator, no commas or pause signs)
# =============================================================================
SPEC = [
    {"key": "fail", "text": "", "visual": "Night room: the boy on his bed stares at the phone; it slips from his hand; silence",
     "vo": [("punch", [("तीसरी बार भी लिस्ट में", "TEESRI BAAR BHI LIST MEIN"), ("उसका नाम नहीं था।", "USKA NAAM NAHIN THA.")], 0.02),
            ("low", [("फोन हाथ से छूटा", "PHONE HAATH SE CHHOOTA"), ("और कमरे में", "AUR KAMRE MEIN"),
                     ("सन्नाटा छा गया।", "SANNATA CHHA GAYA.")], 0.04)]},
    {"key": "taane", "text": "", "visual": "Through the doorway relatives laugh as silhouettes; papa turns and walks away",
     "vo": [("tell", [("बाहर रिश्तेदार हंस रहे थे।", "BAAHAR RISHTEDAAR HANS RAHE THE.")], 0.02),
            ("low", [("कोई बोला", "KOI BOLA"), ("इससे कुछ नहीं होगा।", "ISSE KUCHH NAHIN HOGA.")], 0.02),
            ("low", [("और पापा बिना कुछ कहे", "AUR PAPA BINA KUCHH KAHE"), ("अपने कमरे में चले गए।", "APNE KAMRE MEIN CHALE GAYE.")], 0.04)]},
    {"key": "baksa", "text": "", "visual": "He packs his books into the tin trunk and slams the lid; the almirah trembles",
     "vo": [("low", [("उस रात उसने", "US RAAT USNE"), ("सारी किताबें बक्से में", "SAARI KITAABEN BAKSE MEIN"),
                     ("बंद कर दीं।", "BAND KAR DEEN.")], 0.02),
            ("whisper", [("पर तभी", "PAR TABHI"), ("कुछ अजीब हुआ।", "KUCHH AJEEB HUA.")], 0.04)]},
    {"key": "gita", "text": "", "visual": "Daadi's red Gita falls from the almirah; her garlanded photo glows; the Gita opens "
                                          "and a mor-pankh floats up in golden light",
     "vo": [("build", [("अलमारी से दादी की", "ALMAARI SE DAADI KI"), ("पुरानी गीता नीचे गिरी।", "PURAANI GEETA NEECHE GIRI.")], 0.02),
            ("low", [("वही दादी जो", "WAHI DAADI JO"), ("पिछले साल हमें", "PICHHLE SAAL HUMEIN"), ("छोड़ गई थीं।", "CHHOD GAYI THEEN.")], 0.02),
            ("awe", [("गीता खुली और उसमें से", "GEETA KHULI AUR USMEIN SE"), ("एक मोरपंख निकला।", "EK MORPANKH NIKLA.")], 0.04)]},
    {"key": "seekh", "text": "", "visual": "He holds the mor-pankh, tears; a soft memory of daadi glows beside him; he opens "
                                           "the trunk again",
     "vo": [("low", [("मोरपंख के नीचे", "MORPANKH KE NEECHE"), ("दादी की कांपती लिखावट थी।", "DAADI KI KAANPTI LIKHAWAT THI.")], 0.02),
            ("awe", [("कर्म कर बेटा", "KARM KAR BETA"), ("फल कान्हा पर छोड़ दे।", "PHAL KANHA PAR CHHOD DE.")], 0.02),
            ("low", [("उसे याद आया", "USE YAAD AAYA"), ("दादी कहती थीं", "DAADI KEHTI THEEN"), ("हारता वो है", "HAARTA WO HAI"),
                     ("जो रुक जाता है।", "JO RUK JAATA HAI.")], 0.02),
            ("build", [("उसने बक्सा", "USNE BAKSA"), ("फिर से खोल दिया।", "PHIR SE KHOL DIYA.")], 0.04)]},
    {"key": "mehnat", "text": "", "visual": "Montage: 4 AM alarm rings, he studies at the desk as day and night pass in the "
                                            "window, rings the temple bell at dusk, head down tired then up again; mor-pankh on the desk",
     "vo": [("tell", [("अब रोज़ सुबह", "AB ROZ SUBAH"), ("चार बजे उठता।", "CHAAR BAJE UTHTA.")], 0.02),
            ("tell", [("दिन भर पढ़ता", "DIN BHAR PADHTA"), ("और शाम को मंदिर में", "AUR SHAAM KO MANDIR MEIN"), ("दिया जलाता।", "DIYA JALAATA.")], 0.02),
            ("build", [("कई बार थका", "KAI BAAR THAKA"), ("कई बार रोया", "KAI BAAR ROYA"), ("पर रुका नहीं।", "PAR RUKA NAHIN.")], 0.02),
            ("tell", [("और मोरपंख हर दिन", "AUR MORPANKH HAR DIN"), ("उसकी मेज़ पर रखा रहा।", "USKI MEZ PAR RAKHA RAHA.")], 0.04)]},
    {"key": "result", "text": "", "visual": "Result day: shaking hands open the phone; the screen bursts with light; he leaps up",
     "vo": [("build", [("एक साल बाद", "EK SAAL BAAD"), ("रिजल्ट का दिन आया।", "RESULT KA DIN AAYA.")], 0.02),
            ("low", [("कांपते हाथों से", "KAANPTE HAATHON SE"), ("उसने फोन खोला।", "USNE PHONE KHOLA.")], 0.02),
            ("punch", [("और इस बार", "AUR IS BAAR"), ("लिस्ट में सबसे ऊपर", "LIST MEIN SABSE UPAR"), ("उसका नाम था।", "USKA NAAM THA.")], 0.04)]},
    {"key": "papa", "text": "", "visual": "The same relatives arrive with a sweets box; he looks past them to papa; papa cries "
                                          "and hugs him; cross-fade to the hook",
     "vo": [("tell", [("वही रिश्तेदार अब", "WAHI RISHTEDAAR AB"), ("मिठाई लेकर आए।", "MITHAI LEKAR AAYE.")], 0.02),
            ("low", [("पर उसकी नज़र", "PAR USKI NAZAR"), ("सिर्फ पापा पर थी।", "SIRF PAPA PAR THI.")], 0.02),
            ("awe", [("पापा रो पड़े और बोले", "PAPA RO PADE AUR BOLE"), ("याद है वो दिन जब", "YAAD HAI WO DIN JAB")], 0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "TEESRI": hexc("#FF6A5A"), "NAAM": GOLD_HI, "SANNATA": hexc("#9AB0D8"), "RISHTEDAAR": hexc("#FF8A5A"),
    "PAPA": hexc("#FFD08A"), "KITAABEN": hexc("#9AD8FF"), "AJEEB": GOLD_HI, "DAADI": hexc("#FFB347"),
    "GEETA": hexc("#FF6A5A"), "MORPANKH": hexc("#5AD8A0"), "KARM": GOLD_HI, "KANHA": hexc("#7FB2FF"),
    "HAARTA": hexc("#FF8A5A"), "RUK": hexc("#FF8A5A"), "CHAAR": GOLD_HI, "MANDIR": hexc("#FFB347"),
    "RUKA": hexc("#9BE07A"), "RESULT": GOLD_HI, "UPAR": hexc("#9BE07A"), "MITHAI": hexc("#FF8A1E"),
    "YAAD": GOLD_HI,
})


# =============================================================================
# Scenes
# =============================================================================
class Fail(Cued):
    def beats(self, d):
        c = self.cue
        return {"drop": c("PHONE HAATH", d * 0.45) + 0.3}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "tick"), (b["drop"] + 0.35, "soft_thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        room_bg(ctx, t, night=1.0)
        almirah(ctx, 960, FEET - 30, t)
        home_altar(ctx, 700, 700, t)
        dropped = t >= b["drop"]
        boy(ctx, 420, FEET - 30, 0.76, t, pose="drop" if dropped else "phone",
            mood="sad" if t > b["drop"] + 0.5 else ("shock" if dropped else "low"), look=(0.0, 0.5), seated=True)
        bed(ctx, 420, FEET - 10)
        if dropped:                                          # the phone falls to the floor, screen still glowing
            u = ease_in(clamp((t - b["drop"]) / 0.35))
            phone(ctx, 420 + 60 * u, lerp(FEET - 400, FEET - 20, u), 1.2 * u, t, glow_a=0.5)
        edge_glow(ctx, t, d, start=0.25, c=(0.7, 0.8, 1.0))


class Taane(Cued):
    def beats(self, d):
        c = self.cue
        return {"koi": c("KOI BOLA", d * 0.35), "papa": c("AUR PAPA", d * 0.62)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "pop"), (b["koi"], "pop"), (b["papa"] + 1.2, "soft_thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        room_bg(ctx, t, night=1.0)
        shut = clamp((t - b["papa"] - 0.9) / 0.4)
        door(ctx, 760, FEET - 30, open_=1 - shut)
        if shut < 1:
            ctx.save()
            ctx.rectangle(610, FEET - 790, 300, 760)
            ctx.clip()
            relatives(ctx, 660, 3, t, laugh=1.0)
            ctx.restore()
        walk = clamp((t - b["papa"]) / 1.0)
        if walk < 1:
            papa(ctx, lerp(560, 760, walk), FEET - 10, 0.74, t, pose="away" if walk > 0 else "stand", mood="sad",
                 a=1 - clamp((walk - 0.7) / 0.3))
        boy(ctx, 230, FEET - 10, 0.74, t, pose="drop", mood="cry" if t > b["koi"] else "low", look=(0.6, 0.0))


class Baksa(Cued):
    def beats(self, d):
        c = self.cue
        return {"band": c("BAND KAR", d * 0.4) + 0.2, "ajeeb": c("KUCHH AJEEB", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(b["band"], "thud"), (b["ajeeb"], "zap"), (b["ajeeb"] + 0.1, "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        room_bg(ctx, t, night=1.0)
        shake = clamp(1 - abs(t - b["ajeeb"] - 0.4) / 0.6)
        almirah(ctx, 900, FEET - 30, t, shake=shake, open_=shake)
        closed = t >= b["band"]
        lid = 1.0 - ease_in(clamp((t - b["band"] + 0.3) / 0.3))
        trunk(ctx, 520, FEET - 20, lid=lid, books=1.0 if not closed else 0.0)
        boy(ctx, 250, FEET - 10, 0.74, t, pose="carry" if t < b["band"] - 0.4 else "drop",
            mood="shock" if t >= b["ajeeb"] else "sad", look=(0.8, -0.2) if t >= b["ajeeb"] else (0.4, 0.4))
        if t >= b["ajeeb"]:
            glow(ctx, 900, FEET - 400, 300, GOLDEN, 0.3 * shake)


class Gita(Cued):
    def beats(self, d):
        c = self.cue
        return {"giri": c("PURAANI GEETA", d * 0.15) + 0.4, "daadi": c("WAHI DAADI", d * 0.4),
                "khuli": c("GEETA KHULI", d * 0.7), "pankh": c("EK MORPANKH", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(b["giri"] + 0.4, "soft_thud"), (b["daadi"], "ghanti"), (b["khuli"], "whoosh"), (b["pankh"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        room_bg(ctx, t, night=1.0)
        lit = clamp((t - b["daadi"]) / 0.6)
        daadi_photo(ctx, 300, 600, t, lit=lit, s=1.1)
        almirah(ctx, 900, FEET - 30, t, open_=0.6)
        fall = ease_in(clamp((t - b["giri"]) / 0.45))
        open_ = clamp((t - b["khuli"]) / 0.3)
        gx, gy = 860, lerp(FEET - 520, FEET - 60, fall)
        gita_book(ctx, gx, gy, 0.3 * (1 - fall) + 0.0, open_=open_)
        if open_ > 0:
            kanha_light(ctx, 860, 0.62, t, a=0.45 * clamp((t - b["pankh"] + 0.2) / 0.8), pose="flute")
            rise = ease_out_cubic(clamp((t - b["pankh"] + 0.3) / 1.0))
            glow(ctx, gx, gy - 100, 200 + 100 * rise, GOLDEN, 0.6 * open_)
            dv.peacock_feather(ctx, gx - 40 * rise, gy - 40 - 300 * rise, -1.3 + 0.3 * math.sin(t * 2), 190, t, a=open_)
            sparkle_burst(ctx, gx, gy - 80, (t - b["pankh"]) / 0.9, c=GOLDEN, r=180)
        boy(ctx, 560, FEET - 10, 0.72, t, pose="drop", mood="shock" if t > b["giri"] else "sad",
            look=(0.7, 0.3) if t < b["daadi"] or t > b["khuli"] else (-0.8, -0.4))


class Seekh(Cued):
    def beats(self, d):
        c = self.cue
        return {"karm": c("KARM KAR", d * 0.25), "yaad": c("USE YAAD", d * 0.5), "khol": c("USNE BAKSA", d * 0.82)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "shimmer"), (b["karm"], "ghanti"), (b["yaad"], "soft_thud"), (b["khol"] + 0.3, "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        room_bg(ctx, t, night=1.0, lamp=0.6)
        kanha = clamp((t - b["karm"] - 0.3) / 0.6) * (1 - clamp((t - b["yaad"] + 0.2) / 0.5))
        kanha_light(ctx, 700, 0.66, t, a=0.5 * kanha, pose="bless")
        mem = clamp((t - b["yaad"]) / 0.6) * (1 - clamp((t - b["khol"]) / 0.5))
        if mem > 0:                                          # a soft golden memory of daadi
            glow(ctx, 800, FEET - 450, 340, GOLDEN, 0.4 * mem)
            ctx.save()
            ctx.translate(800, 560)
            daadi_photo(ctx, 0, 0, t, lit=1.0, s=1.25)
            ctx.restore()
        opened = t >= b["khol"]
        trunk(ctx, 820, FEET - 20, lid=ease_out_cubic(clamp((t - b["khol"] - 0.2) / 0.5)) if opened else 0.0,
              books=1.0 if opened else 0.0, glow_a=clamp((t - b["khol"]) / 0.5))
        if t < b["karm"]:
            glow(ctx, 330, FEET - 560, 160, GOLDEN, 0.5)
        boy(ctx, 330, FEET - 10, 0.76, t, pose="feather" if not opened else "carry",
            mood="cry" if b["karm"] <= t < b["khol"] else ("neutral" if opened else "low"), look=(0.0, 0.4))


class Mehnat(Cued):
    def beats(self, d):
        c = self.cue
        return {"padh": c("DIN BHAR", d * 0.22), "mandir": c("AUR SHAAM", d * 0.35), "thaka": c("KAI BAAR THAKA", d * 0.55),
                "ruka": c("PAR RUKA", d * 0.72), "mez": c("AUR MORPANKH HAR", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "beep"), (0.5, "beep"), (b["padh"], "tick"), (b["mandir"] + 0.4, "ghanti"),
                (b["thaka"], "soft_thud"), (b["ruka"], "whoosh"), (b["mez"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        if b["mandir"] <= t < b["thaka"]:                    # evening: the temple and its bell
            temple_bg(ctx, t)
            ring = clamp(1 - abs(t - b["mandir"] - 0.5) / 0.8)
            bell(ctx, 470, 760, t, ring=ring)
            boy(ctx, 300, FEET - 10, 0.74, t, pose="namaste", mood="calm", look=(0.6, -0.3))
            dv.diya(ctx, 470, FEET - 40, 1.1, t, a=1.0)
            return
        day = t >= b["padh"] and t < b["mandir"]
        room_bg(ctx, t, night=0.0 if day else 1.0, lamp=0.0 if day else 1.0)
        if t < b["padh"]:                                    # 4 AM alarm
            clock(ctx, 820, 880, t, ring=clamp(1 - t / 1.4) + 0.3)
            boy(ctx, 420, FEET - 10, 0.74, t, pose="stand", mood="tired", look=(0.6, 0.0))
            return
        tired = b["thaka"] <= t < b["ruka"]
        home_altar(ctx, 930, 640, t, lit=1.0 if not day else 0.6)
        boy(ctx, 540, FEET - 30, 0.74, t, pose="tired" if tired else "write",
            mood="cry" if tired and t > (b["thaka"] + b["ruka"]) / 2 else ("tired" if tired else "neutral"),
            look=(0.0, 0.6), seated=True)
        desk(ctx, 540, FEET - 10, t, lamp=0.0 if day else 1.0, feather=True, books=3 + int(2 * clamp((t - b["ruka"]) / 1.5)))
        if t >= b["mez"]:
            glow(ctx, 700, FEET - 260, 120, GOLDEN, 0.4 + 0.1 * math.sin(t * 4))


class Result(Cued):
    def beats(self, d):
        c = self.cue
        return {"khola": c("USNE PHONE", d * 0.45), "naam": c("USKA NAAM", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "tick"), (0.6, "tock"), (b["khola"], "tick"), (b["naam"], "shimmer"), (b["naam"] + 0.1, "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        room_bg(ctx, t, night=0.0)
        home_altar(ctx, 640, 640, t, lit=0.6 + 0.6 * clamp((t - b["naam"]) / 0.5))
        desk(ctx, 820, FEET - 10, t, lamp=0.0, feather=True, books=5)
        won = t >= b["naam"]
        if not won:
            boy(ctx, 380, FEET - 10, 0.76, t, pose="phone", mood="low" if t < b["khola"] else "shock", look=(0.0, 0.5))
            if t >= b["khola"]:                              # shaking hands
                glow(ctx, 380, FEET - 380, 100, hexc("#9AD0FF"), 0.5)
        else:
            u = clamp((t - b["naam"]) / 0.5)
            jump = 60 * math.sin(math.pi * clamp((t - b["naam"]) / 0.6))
            boy(ctx, 380, FEET - 10 - jump, 0.76, t, pose="joy", mood="joy", look=(0.0, -0.5))
            sparkle_burst(ctx, 380, FEET - 520, u, c=GOLD_HI, r=260)
            dv.petals(ctx, t, n=30, seed=4, a=u)


class Papa(Cued):
    def beats(self, d):
        c = self.cue
        return {"nazar": c("PAR USKI", d * 0.4), "ro": c("PAPA RO", d * 0.62)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "pop"), (b["nazar"], "tick"), (b["ro"], "ghanti"), (d - 0.4, "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        room_bg(ctx, t, night=0.0)
        door(ctx, 860, FEET - 30, open_=1.0)
        ctx.save()
        ctx.rectangle(710, FEET - 790, 300, 760)
        ctx.clip()
        relatives(ctx, 760, 3, t, laugh=0.3, sweets=True, a=1.0 - clamp((t - b["nazar"]) / 0.6))
        ctx.restore()
        kanha_light(ctx, 860, 0.62, t, a=0.55 * clamp((t - b["ro"]) / 0.7), pose="bless")
        hug = ease_out_cubic(clamp((t - b["ro"]) / 0.6))
        papa(ctx, lerp(620, 460, hug), FEET - 10, 0.76, t, pose="hug" if hug > 0.3 else "stand",
             mood="cry" if t >= b["ro"] else "sad", flip=True)
        boy(ctx, lerp(240, 330, hug), FEET - 10, 0.74, t, pose="hug" if hug > 0.3 else "stand",
            mood="cry" if t >= b["ro"] else "neutral", look=(0.7, 0.0))
        if hug > 0:
            glow(ctx, 400, FEET - 500, 300, GOLDEN, 0.3 * hug)
            dv.petals(ctx, t, n=20, seed=9, a=hug)
        x = clamp((t - (d - 0.45)) / 0.45)                   # loop: fade into the hook's first frame
        if x > 0:
            ctx.push_group()
            Fail().draw(ctx, 0.0, d)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(x)


SCENE_CLASSES = {"fail": Fail, "taane": Taane, "baksa": Baksa, "gita": Gita, "seekh": Seekh, "mehnat": Mehnat,
                 "result": Result, "papa": Papa}

UPLOAD = {
    "titles": [
        "3 Baar Fail, Rishtedaar Hanse... Phir Daadi Ki Gita Se Gira Morpankh #shorts",
        "Daadi Ki Gita Se Gira Morpankh... Aur Sab Badal Gaya #shorts",
        "Teesri Baar Fail Hua... Daadi Ke Morpankh Ne Badal Di Zindagi #shorts",
    ],
    "thumb_text": "DAADI KA MORPANKH",
    "queries": [
        "motivational story hindi",
        "daadi ka morpankh",
        "3 baar fail motivational story",
    ],
    "description": """
3 baar fail, rishtedaar hanse, papa chup... phir Daadi ki purani Gita se ek morpankh gira. Daadi ka morpankh - 3 baar fail motivational story hindi
mein - mehnat aur Kanha par bharose ki kahani, har student ke liye jo exam ki taiyari kar raha hai.

"Karm kar beta, phal Kanha par chhod de" - Bhagavad Gita ka yahi sandesh. Haarta wo hai jo ruk jaata hai.

Kalpanik prerak katha (Karm Aur Kripa #1).

Aapko apni Daadi ya Nani ki kaunsi seekh aaj bhi yaad hai? Comment mein likho.
""",
    "tags": [
        "motivational story hindi", "krishna motivation", "student motivation hindi", "daadi ki seekh", "morpankh",
        "bhagavad gita motivation", "exam motivation", "karm aur kripa", "emotional story hindi", "divya rahasya",
        "hindi kahani", "shorts", "inspirational story", "jai shri krishna",
    ],
    "hashtags": ["#Shorts", "#Motivation", "#Krishna"],
    "pinned_comment": "\"Haarta wo hai jo ruk jaata hai\" - aapko apni Daadi ya Nani ki kaunsi seekh aaj bhi yaad hai? "
                      "🙏 Neeche likho. Aur agar kisi sapne ke liye mehnat kar rahe ho to wo bhi likho, hum sab milke "
                      "Kanha ji se aapke liye prarthana karenge.",
}


def thumbnail(ctx):
    room_bg(ctx, 0.5, night=1.0, lamp=1.0)
    daadi_photo(ctx, 790, 560, 0.5, lit=1.0, s=1.0)
    boy(ctx, 360, FEET - 10, 0.80, 0.5, pose="feather", mood="cry", look=(0.0, 0.4))
    text(ctx, "DAADI KA", 540, 1330, 120, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "MORPANKH", 540, 1470, 130, hexc("#5AD8A0"), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
