"""Maa Ke Kangan (Karm Aur Kripa #3): a boy scrolls reels at 3 AM while, that same night, his mother sells her
kangan for his fees; Kanha ji switches his phone off, appears with the flute and asks "Maa ne sab de diya, ab tu
kya dega?"; the phone stays at Kanha's feet, nine months later the first salary comes, he puts new kangan on
Maa's wrists - and Kanha stands behind them, smiling (~30 s, 9 scenes). Kalpanik prerak katha.

Usage (from SanatanKatha/):
  python make.py maa_kangan --preview
  python make.py maa_kangan --kiki-split --check-voice
  python make.py maa_kangan --engine files

Kanha ji is present in every scene (home altar with a diya, his picture in the jeweller's shop, the golden darshan,
the floor chowki murti, the golden form at the end). Mehnat is the boy's own; Kanha only wakes him up.
The last frame stays on Kanha's smile (comment-prompt test, AGENTS.md #14) and cross-fades into the hook.
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

from kathas.daadi_morpankh import (boy, room_bg, bed, desk, phone, home_altar, kanha_light, GOLDEN, FEET)
from kathas.eklavya_krishna import sparkle_burst, edge_glow

TOPIC = "KARM AUR KRIPA MAA KE KANGAN REELS PHONE KANHA BANSURI PEHLI TANKHWAH"
OUTPUTS = {"edge": "maa_kangan_short.mp4"}
MUSIC_STYLE = "pulse"     # emotional modern; papa_karz ambient 90, bees_baar_reject tension 84
MUSIC_BPM = 82            # >= 6 BPM away from 90 / 76
MUSIC_VOLUME = 0.11
TAIL_PAD = 0.22           # calm storytelling breath (user, 23 Nov)
MAX_GAP = 0.25

MAA_SKIN = hexc("#C08458")
SAREE = hexc("#8A1E3A")
SAREE_BORDER = hexc("#E8B020")
BLOUSE = hexc("#2E6A4A")
KANGAN_GOLD = hexc("#FFC83A")
SOURCES = [
    "Original fictional story (Kalpanik prerak katha) - no scripture or real-event claim; labelled in the description.",
    "Shri Krishna's form (mor-pankh, flute, pitambar) follows common Bhagavata iconography. Bhagavad Gita 2.47 "
    "(karm kar, phal ki chinta mat kar) is the spirit of the boy's change.",
]


# =============================================================================
# Maa (modern mother: saree with gold border, bun, sindoor, bindi, mangalsutra; kangan on both wrists)
# =============================================================================
MAA_ARMS = {
    "stand": ((-150, -420, -146, -330), (150, -420, 146, -330)),
    "give": ((-80, -440, 90, -460), (170, -430, 200, -460)),        # both hands forward over a counter
    "wipe": ((-150, -420, -146, -330), (150, -560, 44, -690)),      # wiping a tear with the right hand
    "wrists": ((-70, -430, 100, -430), (170, -420, 210, -430)),     # both wrists held out (new kangan)
    "namaste": ((-120, -430, -14, -500), (120, -430, 14, -500)),
    "bless": ((-150, -420, -146, -330), (190, -560, 200, -700)),
}


def maa(ctx, x, y, s, t, pose="stand", mood="neutral", look=(0.0, 0.0), flip=False, a=1.0, kangan=1.0,
        new_kangan=0.0):
    """kangan 0..1 = the old kangan on her wrists (fade out when sold); new_kangan 0..1 = the new ones (glowing)."""
    def draw():
        place(ctx, x, y, s, t, flip)
        smooth(ctx, [(-120, -560), (120, -560), (150, -300), (170, -30), (-170, -30), (-150, -300)], k=0.12)
        ink(ctx, SAREE)                                                   # saree
        line(ctx, [(-168, -40), (168, -40)], SAREE_BORDER, 14)
        for k in range(5):                                                # pleats
            line(ctx, [(-30 + 18 * k, -300), (-40 + 22 * k, -46)], shade(SAREE, 0.8), 3, 0.7)
        for side in (-1, 1):
            ell(ctx, side * 56, -18, 40, 14)
            ink(ctx, hexc("#C8322A"))
        smooth(ctx, [(-120, -560), (-40, -560), (130, -320), (80, -290), (-130, -440)], k=0.1)   # pallu
        ink(ctx, shade(SAREE, 1.15), 3)
        line(ctx, [(-40, -560), (130, -320)], SAREE_BORDER, 8)
        le, re = MAA_ARMS.get(pose, MAA_ARMS["stand"])
        for side, (sh, (ex, ey, hx, hy)) in enumerate((((-112, -530), le), ((112, -530), re))):
            mid = (lerp(sh[0], ex, 0.5), lerp(sh[1], ey, 0.5))
            limb(ctx, [mid, (ex, ey), (hx, hy)], MAA_SKIN, 34)
            limb(ctx, [sh, mid], BLOUSE, 44)
            if pose != "namaste":
                hand(ctx, hx, hy, MAA_SKIN, 20)
            wx, wy = lerp(ex, hx, 0.78), lerp(ey, hy, 0.78)              # wrist
            ang = math.atan2(hy - ey, hx - ex) + math.pi / 2
            for kk, (amt, col) in enumerate(((kangan, KANGAN_GOLD), (new_kangan, hexc("#FFE27A")))):
                if amt <= 0:
                    continue
                if kk == 1:
                    glow(ctx, wx, wy, 70, GOLDEN, 0.6 * amt)
                for j in (-1, 1):
                    ctx.save()
                    ctx.translate(wx + j * 7 * math.cos(ang - math.pi / 2), wy + j * 7 * math.sin(ang - math.pi / 2))
                    ctx.rotate(ang)
                    ell(ctx, 0, 0, 26, 9)
                    rgba(ctx, col, amt)
                    ctx.set_line_width(7)
                    ctx.stroke()
                    ctx.restore()
        if pose == "namaste":
            smooth(ctx, [(0, -540), (16, -505), (14, -462), (0, -448), (-14, -462), (-16, -505)])
            ink(ctx, MAA_SKIN)
        rrect(ctx, -24, -610, 48, 60, 14)                                 # neck + mangalsutra
        ink(ctx, MAA_SKIN)
        ctx.arc(0, -585, 30, 0.1 * math.pi, 0.9 * math.pi)
        rgba(ctx, hexc("#1A1A1A"))
        ctx.set_line_width(4)
        ctx.stroke()
        circle(ctx, 0, -556, 6, GOLD)
        ell(ctx, 0, -700, 84, 96)
        ink(ctx, MAA_SKIN)
        smooth(ctx, [(-88, -690), (-84, -778), (0, -808), (84, -778), (88, -690), (60, -756), (0, -768),
                     (-60, -756)], k=0.12)                                # hair with centre parting
        ink(ctx, hexc("#1A120E"), 2)
        circle(ctx, -70, -770, 34, hexc("#1A120E"))                       # bun
        line(ctx, [(0, -806), (0, -766)], hexc("#D8102A"), 6)             # sindoor
        circle(ctx, 0, -742, 7, hexc("#C8102A"))                          # bindi
        for side in (-1, 1):
            circle(ctx, side * 86, -680, 7, GOLD)                         # earrings
            if mood in ("cry", "cry_closed"):
                ctx.arc(side * 32, -704, 16, 0.15 * math.pi, 0.85 * math.pi)
                rgba(ctx, hexc("#2A1A10"))
                ctx.set_line_width(6)
                ctx.stroke()
            elif mood == "joy":
                ctx.arc(side * 32, -700, 16, 1.1 * math.pi, 1.9 * math.pi)
                rgba(ctx, hexc("#2A1A10"))
                ctx.set_line_width(6)
                ctx.stroke()
            else:
                eye(ctx, side * 32, -704, 18, 21, t, look=look, seed=31, iris=hexc("#2A1A10"), skin=MAA_SKIN,
                    lid=0.2)
            line(ctx, [(side * 14, -738), (side * 34, -742), (side * 54, -736)], hexc("#1A120E"), 5)
        if mood in ("cry", "cry_closed", "sad"):
            line(ctx, [(-14, -632), (0, -638), (14, -632)], hexc("#7A2A2A"), 5)
        if mood in ("cry", "cry_closed"):
            for side in (-1, 1):
                fu = (t * 0.8 + (0.4 if side > 0 else 0)) % 1
                circle(ctx, side * 38, -684 + 70 * fu, 7, hexc("#9AD8FF"), 0.9 * (1 - fu))
        elif mood == "joy":
            ctx.arc(0, -644, 24, 0.15 * math.pi, 0.85 * math.pi)
            rgba(ctx, hexc("#7A2A2A"))
            ctx.set_line_width(6)
            ctx.stroke()
        elif mood != "sad":
            line(ctx, [(-14, -634), (14, -634)], hexc("#7A2A2A"), 5)
        ctx.restore()
    group(ctx, a, draw)


# =============================================================================
# Props and places
# =============================================================================
def kangan_pair(ctx, x, y, a=1.0, glow_a=0.0, new=False):
    """Two gold bangles lying flat (on the counter / in a small red box)."""
    if glow_a > 0:
        glow(ctx, x, y, 90, GOLDEN, glow_a * a)
    if new:
        rrect(ctx, x - 70, y - 10, 140, 44, 8)
        rgba(ctx, hexc("#B8182A"), a)
        ctx.fill()
    for j in (-1, 1):
        ell(ctx, x + j * 30, y, 34, 14)
        rgba(ctx, KANGAN_GOLD if not new else hexc("#FFE27A"), a)
        ctx.set_line_width(8)
        ctx.stroke()


def notes(ctx, x, y, n, a=1.0):
    for k in range(n):
        ctx.save()
        ctx.translate(x + 6 * k, y - 8 * k)
        ctx.rotate(-0.08 + 0.05 * k)
        rrect(ctx, -60, -26, 120, 52, 4)
        rgba(ctx, hexc("#A8C890"), a)
        ctx.fill()
        rrect(ctx, -60, -26, 120, 52, 4)
        rgba(ctx, hexc("#4A6A3A"), a)
        ctx.set_line_width(3)
        ctx.stroke()
        circle(ctx, 0, 0, 12, hexc("#6A8A5A"), a)
        ctx.restore()


def kanha_photo(ctx, x, y, t, s=1.0, lit=0.6):
    """Framed Kanha ji picture with a marigold garland."""
    glow(ctx, x, y, 150 * s, GOLDEN, 0.35 * lit + 0.05 * math.sin(t * 2))
    rrect(ctx, x - 80 * s, y - 100 * s, 160 * s, 200 * s, 8)
    ink(ctx, hexc("#7A4A1E"), 4)
    ctx.save()
    ctx.rectangle(x - 70 * s, y - 90 * s, 140 * s, 180 * s)
    ctx.clip()
    rgba(ctx, hexc("#9AC8F2"))
    ctx.paint()
    dv.krishna(ctx, x, y + 250 * s, 0.28 * s, t, pose="flute", aura=False)
    ctx.restore()
    for k in range(9):
        ang = math.pi * (k / 8)
        circle(ctx, x + 84 * s * math.cos(ang), y - 108 * s + 70 * s * math.sin(ang) * 0.5, 8 * s,
               hexc("#FF8A1E") if k % 2 else hexc("#FFC21E"))


def jeweller_bg(ctx, t):
    """Small jeweller's shop at night: warm wall, glass showcase with glowing gold, Kanha ji's photo, tube light."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in ((0.0, "#2A1A2E"), (0.4, "#5A3A3A"), (0.7, "#3A2626"), (1.0, "#1A1214")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.rectangle(-80, -80, W + 160, H + 160)
    ctx.fill()
    rrect(ctx, 640, 380, 380, 300, 6)                                     # wall showcase
    ink(ctx, hexc("#6A4428"), 5)
    rrect(ctx, 656, 396, 348, 268, 4)
    rgba(ctx, hexc("#3A2A1E"))
    ctx.fill()
    for r in range(2):
        for k in range(4):
            cx, cy = 700 + 85 * k, 470 + 120 * r
            glow(ctx, cx, cy, 40, GOLDEN, 0.3 + 0.1 * math.sin(t * 3 + k))
            ctx.arc(cx, cy, 22, 0, math.tau)
            rgba(ctx, KANGAN_GOLD)
            ctx.set_line_width(6)
            ctx.stroke()
    kanha_photo(ctx, 400, 520, t, s=0.8, lit=0.8)
    line(ctx, [(160, 300), (560, 300)], hexc("#F4F8FF"), 12)              # tube light
    glow(ctx, 360, 300, 260, hexc("#E8F0FF"), 0.25)
    ctx.rectangle(-80, GROUND - 30, W + 160, H)
    rgba(ctx, hexc("#3A2A20"))
    ctx.fill()


def counter(ctx, x, y, t):
    """Glass counter front (drawn over the jeweller's legs); top at y - 330."""
    rrect(ctx, x - 300, y - 330, 600, 30, 4)
    ink(ctx, hexc("#8A5A34"), 3)
    rrect(ctx, x - 290, y - 300, 580, 300, 4)
    rgba(ctx, hexc("#6A8AA0"), 0.55)
    ctx.fill()
    for k in range(5):                                                    # gold in the glass
        glow(ctx, x - 220 + 110 * k, y - 160, 34, GOLDEN, 0.35)
        circle(ctx, x - 220 + 110 * k, y - 160, 16, KANGAN_GOLD)
    line(ctx, [(x - 290, y - 300), (x - 200, y - 60)], (1, 1, 1), 4, 0.25)


def chowki(ctx, x, y, t, lit=1.0):
    """Low floor chowki with a Kanha murti, diya and marigolds (where the phone will rest)."""
    glow(ctx, x, y - 160, 220, GOLDEN, 0.3 + 0.3 * lit)
    rrect(ctx, x - 170, y - 90, 340, 30, 6)
    ink(ctx, hexc("#8A1E1E"), 3)                                          # red cloth
    for side in (-1, 1):
        line(ctx, [(x + side * 140, y - 60), (x + side * 140, y)], hexc("#6A4428"), 14)
    dv.krishna(ctx, x, y - 92, 0.3, t, pose="flute", aura=False)
    dv.diya(ctx, x - 120, y - 96, 0.6, t, a=1.0)
    for k in range(5):
        circle(ctx, x + 60 + 22 * k, y - 96, 9, hexc("#FF8A1E") if k % 2 else hexc("#FFC21E"))


def clock3(ctx, x, y):
    """Round wall clock showing 3 o'clock."""
    circle(ctx, x, y, 62, hexc("#2A2A3A"))
    circle(ctx, x, y, 52, hexc("#E8E4D8"))
    for k in range(12):
        ang = k / 12 * math.tau
        circle(ctx, x + 42 * math.cos(ang), y + 42 * math.sin(ang), 3, hexc("#2A1A10"))
    line(ctx, [(x, y), (x, y - 40)], hexc("#2A1A10"), 5)                  # minute hand at 12
    line(ctx, [(x, y), (x + 30, y)], hexc("#2A1A10"), 7)                  # hour hand at 3


def reel_tiles(ctx, x, y, t, a=1.0):
    """Bright reel tiles flicking up out of the phone (no text)."""
    cols = ("#FF4A7A", "#4AC8FF", "#FFC21E", "#9A6AFF", "#4AE88A")
    for i in range(6):
        u = (t * 0.9 + i / 6) % 1
        tx = x + 140 * math.sin(i * 2.1) * u
        ty = y - 380 * u
        ctx.save()
        ctx.translate(tx, ty)
        ctx.rotate(0.3 * math.sin(i * 1.7))
        rrect(ctx, -34, -54, 68, 108, 10)
        rgba(ctx, hexc(cols[i % 5]), a * 0.85 * (1 - u))
        ctx.fill()
        ctx.move_to(-10, -16)                                             # play triangle
        ctx.line_to(16, 0)
        ctx.line_to(-10, 16)
        ctx.close_path()
        rgba(ctx, (1, 1, 1), a * 0.9 * (1 - u))
        ctx.fill()
        ctx.restore()


def dark_phone(ctx, x, y, a=1.0):
    phone(ctx, x, y, 0.0, 0.0, glow_a=0.0)
    rrect(ctx, x - 20, y - 38, 40, 74, 4)
    rgba(ctx, hexc("#0A0A12"), a)
    ctx.fill()


def flute_notes(ctx, x, y, t, a=1.0):
    for i in range(7):
        u = (t * 0.5 + i / 7) % 1
        nx = x + 260 * u * (1 if i % 2 else -1) + 30 * math.sin(t * 3 + i)
        ny = y - 260 * u
        al = a * math.sin(math.pi * u)
        ell(ctx, nx, ny, 14, 10)
        rgba(ctx, GOLD_HI, al)
        ctx.fill()
        line(ctx, [(nx + 12, ny), (nx + 12, ny - 46)], GOLD_HI, 4, al)
        line(ctx, [(nx + 12, ny - 46), (nx + 30, ny - 32)], GOLD_HI, 4, al)


def phone_pos(x, s, seated=True):
    """World position of the phone in the boy's 'phone' pose."""
    return x, FEET + (150 * s if seated else 0) - 490 * s


# =============================================================================
# Story: 9 scenes, single narrator, no commas or pause signs (same text as kiki_narrator.txt of 24 Nov)
# =============================================================================
SPEC = [
    {"key": "band", "text": "", "visual": "3 AM, dark room: boy on the bed lit by his phone; a golden light from the home altar "
                                          "flies into it and the screen dies on 'band'; he freezes",
     "vo": [("punch", [("उस रात कान्हा ने", "US RAAT KANHA NE"), ("खुद उस लड़के का", "KHUD US LADKE KA"),
                       ("फोन बंद कर दिया।", "PHONE BAND KAR DIYA.")], 0.04)]},
    {"key": "reels", "text": "", "visual": "Flashback minutes earlier: the clock shows 3, tired red eyes, reel tiles "
                                           "flicking out of the phone; Kanha's altar diya glows unseen behind",
     "vo": [("low", [("वो रात के", "WO RAAT KE"), ("तीन बजे भी", "TEEN BAJE BHI"), ("रील्स देख रहा था।", "REELS DEKH RAHA THA.")],
             0.04)]},
    {"key": "kangan", "text": "", "visual": "Jeweller's shop: Maa slips her kangan off onto the counter, takes the notes "
                                            "for his fees and wipes a tear; Kanha ji's photo on the wall",
     "vo": [("tell", [("और उसी रात", "AUR USI RAAT"), ("मां ने उसकी", "MAA NE USKI"), ("फीस के लिए", "FEES KE LIYE"),
                      ("कंगन बेच दिए थे।", "KANGAN BECH DIYE THE.")], 0.04)]},
    {"key": "bansuri", "text": "", "visual": "Dark room again: flute notes float in, golden light; Kanha ji appears playing "
                                             "the flute; the boy jumps off the bed in shock",
     "vo": [("whisper", [("अंधेरे कमरे में", "ANDHERE KAMRE MEIN"), ("बांसुरी बजी", "BANSURI BAJI")], 0.02),
            ("awe", [("और सामने", "AUR SAAMNE"), ("कान्हा खड़े थे।", "KANHA KHADE THE.")], 0.04)]},
    {"key": "kya_dega", "text": "", "visual": "Kanha asks with an open palm; a soft memory of Maa's bare wrists at the "
                                              "counter glows above; the boy breaks down with folded hands",
     "vo": [("low", [("बोले", "BOLE"), ("मां ने सब दे दिया", "MAA NE SAB DE DIYA"), ("अब तू क्या देगा।", "AB TU KYA DEGA.")],
             0.04)]},
    {"key": "charan", "text": "", "visual": "He lays the phone at the Kanha murti's feet on the floor chowki; then days "
                                            "and nights of study at the desk",
     "vo": [("build", [("उस दिन से", "US DIN SE"), ("फोन कान्हा के", "PHONE KANHA KE"), ("चरणों में", "CHARNON MEIN"),
                       ("रहने लगा।", "REHNE LAGA.")], 0.04)]},
    {"key": "tankhwah", "text": "", "visual": "Calendar pages fly; the phone at the chowki lights up green, coins burst; "
                                              "he jumps with joy",
     "vo": [("build", [("नौ महीने बाद", "NAU MAHINE BAAD"), ("पहली तनख्वाह आई।", "PEHLI TANKHWAH AAYI.")], 0.04)]},
    {"key": "pehnaye", "text": "", "visual": "Morning room: he slides two new glowing kangan onto Maa's wrists; she cries "
                                             "with joy",
     "vo": [("tell", [("उसने मां को", "USNE MAA KO"), ("नए कंगन पहनाए।", "NAYE KANGAN PEHNAAYE.")], 0.04)]},
    {"key": "muskaan", "text": "", "visual": "Kanha ji's golden form rises behind Maa and son, smiling and blessing; petals; "
                                             "last frame on his smile, cross-fade into the hook",
     "vo": [("awe", [("और पीछे खड़े", "AUR PEECHHE KHADE"), ("कान्हा मुस्कुरा रहे थे।", "KANHA MUSKURA RAHE THE.")],
             0.04),
            ("punch", [("जो मानता है", "JO MAANTA HAI"), ("वो लिखे", "WO LIKHE"), ("जय श्री कृष्ण।", "JAI SHRI KRISHNA.")],
             0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "KANHA": GOLD_HI, "PHONE": hexc("#9AD0FF"), "BAND": hexc("#FF5A5A"), "TEEN": hexc("#FFB347"),
    "REELS": hexc("#FF4A7A"), "MAA": hexc("#FFB347"), "FEES": hexc("#9BE07A"), "KANGAN": KANGAN_GOLD,
    "BECH": hexc("#FF5A5A"), "BANSURI": GOLD_HI, "SAB": hexc("#FFB347"), "DEGA": GOLD_HI, "CHARNON": GOLD_HI,
    "TANKHWAH": hexc("#9BE07A"), "NAYE": KANGAN_GOLD, "MUSKURA": GOLD_HI, "JAI": GOLD_HI, "KRISHNA": GOLD_HI,
})

BOY_X = 470          # boy on the bed in the night scenes


def night_room(ctx, t, glow_altar=0.6):
    room_bg(ctx, t, night=1.0, lamp=0.0)
    home_altar(ctx, 880, 560, t, lit=glow_altar)


# =============================================================================
# Scenes
# =============================================================================
class Band(Cued):
    def beats(self, d):
        return {"band": self.cue("PHONE BAND", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "shimmer"), (b["band"] + 0.25, "zap"), (b["band"] + 0.45, "soft_thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        off = t >= b["band"] + 0.3
        night_room(ctx, t, glow_altar=1.0)
        kanha_light(ctx, 880, 0.70, t, a=0.32 + 0.08 * math.sin(t * 2))   # faint presence behind the altar
        boy(ctx, BOY_X, FEET, 0.72, t, pose="phone", mood="shock" if off else "tired",
            look=(0.0, 0.5) if not off else (0.7, -0.3), seated=True)
        bed(ctx, BOY_X, FEET + 10, w=560)
        px, py = phone_pos(BOY_X, 0.72)
        if not off:
            glow(ctx, px, py - 80, 200, hexc("#9AD0FF"), 0.35)            # blue glow on his face
        fly = clamp((t - (b["band"] - 0.5)) / 0.8)                        # golden spark from altar to phone
        if 0 < fly < 1:
            sx, sy = 880, 470
            u = ease_in_out(fly)
            fx, fy = lerp(sx, px, u), lerp(sy, py, u) - 160 * math.sin(math.pi * u)
            glow(ctx, fx, fy, 70, GOLDEN, 0.8)
            dv.peacock_feather(ctx, fx, fy, math.atan2(py - sy, px - sx), 90, t, a=1.0)
        if off:
            dark_phone(ctx, px, py)
            sparkle_burst(ctx, px, py, clamp((t - b["band"] - 0.3) / 0.7), c=GOLD_HI, n=14, r=180)
            flash(ctx, (t - b["band"] - 0.3) / 0.4, c=(1, 0.92, 0.7))
        edge_glow(ctx, t, d, start=0.0)


class Reels(Cued):
    def beats(self, d):
        return {"reels": self.cue("REELS", d * 0.5)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "tick"), (0.6, "tock"), (b["reels"], "pop"), (b["reels"] + 0.4, "pop")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_room(ctx, t, glow_altar=0.5)
        clock3(ctx, 300, 360)
        x = 640
        boy(ctx, x, FEET, 0.74, t, pose="phone", mood="tired", look=(0.0, 0.6), seated=True)
        bed(ctx, x, FEET + 10, w=600)
        px, py = phone_pos(x, 0.74)
        glow(ctx, px, py - 80, 220, hexc("#9AD0FF"), 0.4 + 0.1 * math.sin(t * 11))
        if t >= b["reels"] - 0.2:
            reel_tiles(ctx, px, py - 40, t, a=clamp((t - b["reels"] + 0.2) / 0.3))


class Kangan(Cued):
    def beats(self, d):
        return {"maa": self.cue("MAA NE", d * 0.3), "bech": self.cue("BECH", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["maa"], "soft_thud"), (b["bech"], "pick"), (b["bech"] + 0.5, "kaching")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        jeweller_bg(ctx, t)
        jx = 800
        dv.silhouette(ctx, lambda: maa_jeweller(ctx, jx, t), c=hexc("#1A1018"))
        counter(ctx, jx - 40, FEET, t)
        off = ease_in_out(clamp((t - b["maa"] - 0.2) / 0.8))              # kangan slide off onto the counter
        sold = t >= b["bech"] + 0.2
        pose = "wipe" if sold and t > b["bech"] + 0.9 else "give"
        maa(ctx, 300, FEET, 0.74, t, pose=pose, mood="cry" if sold else "sad", look=(0.8, 0.2), kangan=1 - off)
        if off > 0:
            kx = lerp(300 + 150 * 0.74, 560, off) if not sold else 560
            kangan_pair(ctx, kx, FEET - 335 - 30 * (1 - off), glow_a=0.4)
        if sold:                                                          # jeweller slides the notes over
            u = ease_out_cubic(clamp((t - b["bech"] - 0.2) / 0.6))
            notes(ctx, lerp(720, 470, u), FEET - 345, 3)


def maa_jeweller(ctx, x, t):
    """The jeweller as a dark silhouette behind his counter (an ordinary man, no face shown)."""
    from kathas.daadi_morpankh import papa
    papa(ctx, x, FEET, 0.72, t, pose="stand", mood="neutral", flip=True)


class Bansuri(Cued):
    def beats(self, d):
        return {"bansuri": self.cue("BANSURI", d * 0.3), "kanha": self.cue("KANHA KHADE", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["bansuri"], "shimmer"), (b["kanha"] - 0.2, "whoosh"), (b["kanha"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_room(ctx, t, glow_altar=0.6 + 0.4 * clamp((t - b["bansuri"]) / 0.5))
        ka = ease_out_cubic(clamp((t - b["kanha"] + 0.3) / 0.7))
        if t >= b["bansuri"]:
            flute_notes(ctx, 800, 700, t, a=clamp((t - b["bansuri"]) / 0.4))
        if ka > 0:
            glow(ctx, 800, FEET - 420, 420, GOLDEN, 0.55 * ka)
            dv.krishna(ctx, 800, FEET, 0.76, t, pose="flute", smile=1.0, flip=True, a=ka)
        jump = t >= b["kanha"]
        if not jump:
            boy(ctx, 280, FEET, 0.72, t, pose="drop", mood="shock" if t > b["bansuri"] else "low",
                look=(0.9, -0.2), seated=True)
            bed(ctx, 280, FEET + 10, w=480)
            dark_phone(ctx, 340, FEET - 170)
        else:
            u = clamp((t - b["kanha"]) / 0.35)
            boy(ctx, 260, FEET - 40 * math.sin(math.pi * u), 0.72, t, pose="drop", mood="shock", look=(0.9, -0.3))
            dark_phone(ctx, 300, FEET - 20)
        flash(ctx, (t - b["kanha"] + 0.2) / 0.5, c=(1, 0.93, 0.75))


class KyaDega(Cued):
    def beats(self, d):
        return {"maa": self.cue("MAA NE SAB", d * 0.3), "dega": self.cue("KYA DEGA", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["maa"], "shimmer"), (b["dega"], "soft_thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_room(ctx, t, glow_altar=1.0)
        glow(ctx, 800, FEET - 420, 420, GOLDEN, 0.5)
        dv.krishna(ctx, 800, FEET, 0.76, t, pose="ask", smile=0.6, flip=True)
        mem = clamp((t - b["maa"]) / 0.5) * (1 - clamp((t - b["dega"] - 0.6) / 0.5))
        if mem > 0:                                                       # memory: Maa at the counter
            cx, cy, r = 300, 330, 170
            glow(ctx, cx, cy, r + 40, GOLDEN, 0.4 * mem)
            ctx.save()
            ctx.arc(cx, cy, r, 0, math.tau)
            ctx.clip()
            rgba(ctx, hexc("#5A3A3A"), mem)
            ctx.paint()
            maa(ctx, cx - 20, cy + 300, 0.42, t, pose="give", mood="cry", look=(0.8, 0.2), kangan=0.0,
                a=mem)
            kangan_pair(ctx, cx + 90, cy + 160, a=mem, glow_a=0.5)
            ctx.restore()
            ctx.arc(cx, cy, r, 0, math.tau)
            rgba(ctx, GOLD_HI, 0.8 * mem)
            ctx.set_line_width(6)
            ctx.stroke()
        broke = t >= b["dega"]
        boy(ctx, 280, FEET, 0.72, t, pose="namaste" if broke else "drop", mood="cry" if broke else "shock",
            look=(0.9, -0.4))


class Charan(Cued):
    def beats(self, d):
        return {"charan": self.cue("CHARNON", d * 0.45), "rehne": self.cue("REHNE", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(b["charan"], "soft_thud"), (b["charan"] + 0.2, "ghanti"), (b["rehne"], "tick"),
                (b["rehne"] + 0.5, "tock")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        if t < b["rehne"]:
            room_bg(ctx, t, night=0.0)
            chowki(ctx, 760, FEET, t, lit=clamp((t - b["charan"]) / 0.4))
            walk = ease_out_cubic(clamp(t / max(0.6, b["charan"] - 0.1)))
            bx = lerp(120, 420, walk)
            boy(ctx, bx, FEET, 0.72, t, pose="offer", mood="calm", look=(0.8, 0.2))
            put = ease_in_out(clamp((t - b["charan"]) / 0.5))
            ox, oy = bx + 155 * 0.72, FEET - 455 * 0.72
            px, py = lerp(ox, 760, put), lerp(oy, FEET - 120, put)
            dark_phone(ctx, px, py)
            if put >= 1:
                sparkle_burst(ctx, 760, FEET - 160, clamp((t - b["charan"] - 0.5) / 0.6), c=GOLD_HI, n=12, r=140)
            return
        night = 1.0 if int((t - b["rehne"]) / 0.45) % 2 else 0.0          # days and nights at the desk
        room_bg(ctx, t, night=night, lamp=1.0 if night else 0.0)
        home_altar(ctx, 880, 560, t, lit=0.8)
        boy(ctx, 380, FEET, 0.74, t * 1.6, pose="write", mood="neutral", look=(0.0, 0.7), seated=True)
        desk(ctx, 380, FEET + 10, t, lamp=night, books=3 + int((t - b["rehne"]) / 0.45) % 3)


class Tankhwah(Cued):
    def beats(self, d):
        return {"tankhwah": self.cue("PEHLI", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "whoosh"), (0.4, "whoosh"), (b["tankhwah"], "beep"), (b["tankhwah"] + 0.3, "kaching")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        room_bg(ctx, t, night=0.0)
        chowki(ctx, 760, FEET, t, lit=1.0)
        hit = t >= b["tankhwah"]
        for k in range(9):                                                # calendar pages flying off
            u = clamp((t - k * 0.12) / 0.7)
            if 0 < u < 1:
                ctx.save()
                ctx.translate(lerp(630, 300 + 300 * (k % 3), u), lerp(380, 120, u))
                ctx.rotate(1.5 * u * (1 if k % 2 else -1))
                rrect(ctx, -70, -80, 140, 160, 6)
                rgba(ctx, hexc("#F4F0E6"), 1 - u)
                ctx.fill()
                rrect(ctx, -70, -80, 140, 40, 6)
                rgba(ctx, hexc("#C8202A"), 1 - u)
                ctx.fill()
                ctx.restore()
        rrect(ctx, 560, 300, 140, 160, 6)                                 # the calendar on the wall
        ink(ctx, hexc("#F4F0E6"), 3)
        rrect(ctx, 560, 300, 140, 40, 6)
        rgba(ctx, hexc("#C8202A"))
        ctx.fill()
        phx, phy = 760, FEET - 120
        if hit:
            u = clamp((t - b["tankhwah"]) / 0.8)
            glow(ctx, phx, phy, 160, hexc("#7AE88A"), 0.7)
            for i in range(10):                                           # coins bursting up
                ang = -math.pi / 2 + (i - 4.5) * 0.25
                circle(ctx, phx + 260 * u * math.cos(ang), phy + 260 * u * math.sin(ang) + 200 * u * u, 16,
                       GOLD_HI, 1 - u * 0.6)
        phone(ctx, phx, phy, 0.0, t, glow_a=0.0)
        if hit:
            rrect(ctx, phx - 20, phy - 38, 40, 74, 4)
            rgba(ctx, hexc("#4AD86A"))
            ctx.fill()
        boy(ctx, 330, FEET, 0.74, t, pose="joy" if hit else "stand", mood="joy" if hit else "neutral",
            look=(0.8, 0.3))


class Pehnaye(Cued):
    def beats(self, d):
        return {"kangan": self.cue("NAYE KANGAN", d * 0.5)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "ghanti"), (b["kangan"], "shimmer"), (b["kangan"] + 0.6, "dingdong")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        room_bg(ctx, t, night=0.0)
        home_altar(ctx, 540, 520, t, lit=1.0)
        on = ease_in_out(clamp((t - b["kangan"]) / 0.7))
        maa(ctx, 780, FEET, 0.74, t, pose="wrists", mood="cry" if on > 0.5 else "neutral", look=(-0.8, 0.2),
            kangan=0.0, new_kangan=on, flip=True)
        boy(ctx, 280, FEET, 0.74, t, pose="offer", mood="joy" if on > 0.5 else "calm", look=(0.8, 0.0))
        if on < 1:                                                        # the bangles travel from his box
            kx = lerp(280 + 155 * 0.74, 780 - 140 * 0.74, on)
            kangan_pair(ctx, kx, FEET - 455 * 0.74 + 10, a=1 - 0.8 * on, glow_a=0.5, new=on < 0.05)
        else:
            sparkle_burst(ctx, 780 - 140 * 0.74, FEET - 320, clamp((t - b["kangan"] - 0.7) / 0.6), c=GOLD_HI,
                          n=12, r=150)


class Muskaan(Cued):
    def beats(self, d):
        return {"kanha": self.cue("KANHA MUSKURA", d * 0.3), "jai": self.cue("JO MAANTA", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["kanha"], "shimmer"), (b["jai"], "ghanti"), (d - 0.6, "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        room_bg(ctx, t, night=0.0)
        home_altar(ctx, 540, 360, t, lit=1.0)
        rise = ease_out_cubic(clamp((t - b["kanha"] + 0.4) / 0.9))
        if rise > 0:
            glow(ctx, 540, FEET - 460, 480, GOLDEN, 0.6 * rise)
            dv.krishna(ctx, 540, FEET + 60 * (1 - rise), 0.74, t, pose="flute" if t < b["jai"] else "bless",
                       smile=1.0, a=0.9 * rise)
        if t >= b["jai"]:
            dv.petals(ctx, t, n=30, seed=9, a=0.9)
        maa(ctx, 860, FEET, 0.70, t, pose="namaste" if t >= b["jai"] else "stand", mood="joy", look=(-0.6, -0.4),
            kangan=0.0, new_kangan=1.0, flip=True)
        boy(ctx, 220, FEET, 0.70, t, pose="namaste" if t >= b["jai"] else "stand", mood="joy", look=(0.6, -0.4))
        x = clamp((t - (d - 0.45)) / 0.45)                                # loop: fade into the hook's frame 0
        if x > 0:
            ctx.push_group()
            Band().draw(ctx, 0.0, d)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(x)


SCENE_CLASSES = {"band": Band, "reels": Reels, "kangan": Kangan, "bansuri": Bansuri, "kya_dega": KyaDega,
                 "charan": Charan, "tankhwah": Tankhwah, "pehnaye": Pehnaye, "muskaan": Muskaan}

UPLOAD = {
    "titles": [
        "मां ने कंगन बेचे... और कान्हा ने बेटे का फोन बंद कर दिया #shorts",
        "रात तीन बजे रील्स देख रहा था... तभी कान्हा आए #shorts",
        "मां ने सब दे दिया... अब तू क्या देगा #shorts",
    ],
    "thumb_text": "KANHA NE PHONE BAND KIYA",
    "queries": [
        "krishna ki kahani",
        "maa ki kahani emotional",
        "kanha ji ki kahani",
    ],
    "description": """
Maa ne fees ke liye apne kangan bech diye... aur beta raat ke 3 baje bhi reels dekh raha tha. Usi raat Kanha ne khud
uska phone band kar diya. Andhere kamre mein bansuri baji - "Maa ne sab de diya... ab tu kya dega?"
Krishna ki kahani - mehnat aur Kanha ji par bharose ki prerak katha.

Kalpanik prerak katha.

Reels ka time - aaram ka haq ya Maa ke sapnon se dhokha? Comment mein apni raay likho.
""",
    "tags": [
        "krishna ki kahani", "kanha ji ki kahani", "maa ki kahani", "maa emotional story", "jai shri krishna",
        "bhagwan ki kahani", "motivational story hindi", "reels addiction", "phone addiction story",
        "divya rahasya", "karm aur kripa", "prerak katha", "shorts", "krishna bhakti",
    ],
    "hashtags": ["#Shorts", "#JaiShriKrishna", "#Kanha"],
    "pinned_comment": "Raat ko reels dekhna - thakan utaarne ka haq hai ya Maa ke sapnon se dhokha? 🤔 Apni raay "
                      "likho. Aur agar aap bhi phone chhod ke mehnat shuru kar rahe ho to likho - hum sab milke "
                      "Kanha ji se aapke liye prarthana karenge. Jai Shri Krishna 🙏",
}


def thumbnail(ctx):
    night_room(ctx, 0.5, glow_altar=1.0)
    glow(ctx, 800, FEET - 420, 420, GOLDEN, 0.55)
    dv.krishna(ctx, 800, FEET, 0.76, 0.5, pose="ask", smile=0.6, flip=True)
    boy(ctx, 280, FEET, 0.72, 0.5, pose="drop", mood="shock", look=(0.9, -0.3))
    dark_phone(ctx, 300, FEET - 20)
    cx, cy, r = 300, 330, 170
    glow(ctx, cx, cy, r + 40, GOLDEN, 0.4)
    ctx.save()
    ctx.arc(cx, cy, r, 0, math.tau)
    ctx.clip()
    rgba(ctx, hexc("#5A3A3A"))
    ctx.paint()
    maa(ctx, cx - 20, cy + 300, 0.42, 0.5, pose="give", mood="cry", look=(0.8, 0.2), kangan=0.0)
    kangan_pair(ctx, cx + 90, cy + 160, glow_a=0.5)
    ctx.restore()
    ctx.arc(cx, cy, r, 0, math.tau)
    rgba(ctx, GOLD_HI, 0.8)
    ctx.set_line_width(6)
    ctx.stroke()
