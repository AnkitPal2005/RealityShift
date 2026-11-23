"""Reality Shift Short - "Akash: Armenia ne Bharat se kharidi" (~23s, single voice, recorded in KikiVoice).

Usage:
  python make.py akash --kiki-export     # narrator text for KikiVoice
  python make.py akash --kiki-split --check-voice
  python make.py akash                   # renders from the KikiVoice clips

Five scenes, 68 spoken words, loop ending ("...तभी तो" -> "भारत की आकाश मिसाइल..."):
hook (launcher fires, the trail arcs from BHARAT to ARMENIA) -> first foreign buyer, 15 systems (launcher icons pop)
-> Rajendra radar sweep spots jets and drones, 25 KM ring, interceptors hit -> four targets hit at once (4/4) ->
before/after: arrows into India flip to arrows out, frame settles back on the opening launcher for the loop.
Voice text follows AGENTS rule 21: no commas / ! / ? / ..., one thought per line ending in ।, simple words.
"""

import importlib
import json
import math
import sys

import cairo

from core import delivery, engine, lego
from core.engine import *  # noqa: F401,F403
from shorts.brahmos_lego import tag
from shorts.chabahar import Cued
from shorts.reality_shift import stamp

TOPIC = "AKASH MISSILE ARMENIA EXPORT"
OUTPUTS = {"edge": "akash_short.mp4"}
LEGO = {"header": "intel", "caption": "chip", "transition": "shutter", "palette": "intel", "ending": "prompt"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.04
TAIL_PAD = 0.04
TRIM = {"thresh": 0.006, "keep": 0.06, "keep_tail": 0.10}
MUSIC_BPM = 104
MUSIC_STYLE = "pulse"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 0

PAL = lego.PALETTES["intel"]
UI, HI, RED, INK = PAL["ui"], PAL["hi"], PAL["alert"], PAL["ink"]
SAFFRON = hexc("#FF9933")
GREEN = hexc("#3DDC84")
OLIVE = hexc("#4E5B31")
STEEL = hexc("#B8C2CC")
FIRE = hexc("#FF6A1A")
AM_RED, AM_BLUE, AM_ORANGE = hexc("#D90012"), hexc("#0033A0"), hexc("#F2A800")

SOURCES = [
    "Armenia is the first foreign buyer of Akash; first battery flagged off by BEL/MoD in Bengaluru, Nov 2024; the 2022 "
    "order is reported as 15 Akash systems (~Rs 6,000 crore, figures vary by outlet) (ETV Bharat 12 Nov 2024; "
    "Asianet Newsable; Raksha Anirveda; Caspian Post; airforce-technology.com)",
    "Akash: DRDO surface-to-air missile, range ~25 km against aircraft, cruise missiles and drones; each battery has one "
    "Rajendra 3D PESA radar and four launchers (BEL / PIB; reports above)",
    "Dec 2023 'Astrashakti' exercise: a single Akash firing unit engaged four aerial targets simultaneously at ~25-30 km "
    "(PIB / MoD press release, 17 Dec 2023)",
    "India remains among the world's largest arms importers while defence exports rose to record highs (SIPRI 2024-25; "
    "MoD export figures FY24/FY25) - hence 'हथियार भी खरीद रही है', not 'only seller'",
]

# AGENTS rule 21 voice: no signs except ।, one thought per line, simple spoken Hindi, numbers as words.
SPEC = [
    {"key": "hook", "accent": HI, "text": "AKASH",
     "visual": "Night sky; an Akash launcher fires; the trail arcs from a BHARAT pin to an ARMENIA pin with its flag",
     "vo": [("hook", [("भारत की आकाश मिसाइल", "BHARAT KI AKASH MISSILE"),
                      ("अब दूसरे देश का", "AB DOOSRE DESH KA"), ("आसमान बचाएगी।", "AASMAAN BACHAYEGI")])]},
    {"key": "deal", "accent": SAFFRON, "text": "15 SYSTEM",
     "visual": "Armenia flag waves; 'PEHLA VIDESHI KHAREEDAR' tag; a 0 -> 15 counter while 15 launcher icons pop in",
     "vo": [("tell", [("आर्मेनिया पहला देश है", "ARMENIA PEHLA DESH HAI"), ("जिसने इसे खरीदा।", "JISNE ISE KHAREEDA")]),
            ("punch", [("पंद्रह सिस्टम का", "15 SYSTEM KA"), ("पूरा सौदा हुआ।", "POORA SAUDA HUA")])]},
    {"key": "radar", "accent": UI, "text": "25 KM",
     "visual": "Rajendra radar panel turns, sweep finds a jet and drones; a 25 KM ring opens; interceptors climb and hit",
     "vo": [("tell", [("इसका रडार दूर से", "ISKA RADAR DOOR SE"), ("दुश्मन पकड़ लेता है।", "DUSHMAN PAKAD LETA HAI")]),
            ("punch", [("और पच्चीस किलोमीटर तक", "AUR 25 KM TAK"), ("विमान और ड्रोन", "VIMAAN AUR DRONE"),
                       ("गिरा देता है।", "GIRA DETA HAI")])]},
    {"key": "four", "accent": RED, "text": "4 / 4",
     "visual": "Four targets in a row; four interceptors strike together; a '4/4 EK SAATH' stamp",
     "vo": [("punch", [("एक बार इसने", "EK BAAR ISNE"), ("एक साथ चार", "EK SAATH 4"), ("निशाने गिरा दिए।", "NISHAANE GIRA DIYE")])]},
    {"key": "loop", "accent": GREEN, "text": "IB DUNIYA KHAREED RAHI",
     "visual": "Arrows flow INTO India (PEHLE), then flip to flow OUT (IB); the frame settles on the resting launcher "
               "of the opening shot for the loop",
     "vo": [("low", [("भारत हमेशा", "BHARAT HAMESHA"), ("हथियार खरीदने", "HATHIYAAR KHAREEDNE"),
                     ("वाला देश", "WAALA DESH"), ("माना गया।", "MAANA GAYA")]),
            ("punch", [("इब दुनिया म्हारे हथियार", "IB DUNIYA MHAARE HATHIYAAR"), ("भी खरीद रही है", "BHI KHAREED RAHI HAI"),
                       ("तभी तो।", "TABHI TOH")])]},
]

DELIVERY = delivery.build(SPEC)
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {"AKASH": HI, "MISSILE": HI, "AASMAAN": UI, "BACHAYEGI": UI, "ARMENIA": SAFFRON, "PEHLA": SAFFRON,
       "15": HI, "SAUDA": HI, "RADAR": UI, "DUSHMAN": RED, "25": HI, "KM": HI, "VIMAAN": RED, "DRONE": RED,
       "GIRA": RED, "4": RED, "EK": HI, "SAATH": HI, "NISHAANE": RED, "KHAREEDNE": STEEL, "IB": GREEN,
       "MHAARE": SAFFRON, "DUNIYA": GREEN, "TABHI": HI, "TOH": HI, "BHARAT": SAFFRON}

GROUND_Y = 1000


# ============================================================ props

def sky(ctx, t, warm=0.0):
    g = cairo.LinearGradient(0, 0, 0, GROUND_Y)
    g.add_color_stop_rgb(0, *lerp_c(hexc("#030812"), hexc("#140A12"), warm))
    g.add_color_stop_rgb(0.7, *lerp_c(hexc("#0B1A2C"), hexc("#3A1A22"), warm))
    g.add_color_stop_rgb(1, *lerp_c(hexc("#16304A"), hexc("#7A3A2A"), warm))
    ctx.set_source(g)
    ctx.paint()
    for i in range(80):
        circle(ctx, rnd(i, 1) * W, rnd(i, 2) * 820, 1 + 1.6 * rnd(i, 3), (1, 1, 1), 0.2 + 0.5 * rnd(i, 4))
    ctx.move_to(0, GROUND_Y)
    for i in range(13):
        ctx.line_to(i * 90, GROUND_Y - 80 - 60 * math.sin(i * 1.4) * rnd(i, 5))
    ctx.line_to(W, GROUND_Y)
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    rgba(ctx, hexc("#0D1A16"))
    ctx.fill()
    rgba(ctx, hexc("#13241C"))
    ctx.rectangle(0, GROUND_Y, W, H - GROUND_Y)
    ctx.fill()


def lerp_c(a, b, u):
    return tuple(lerp(x, y, u) for x, y in zip(a, b))


def missile(ctx, x, y, ang, L, burner=0.0, a=1.0):
    """Akash missile: white body, red nose, four mid-body wings; points along ang (radians, 0 = right)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    if burner > 0:
        g = cairo.LinearGradient(-L / 2, 0, -L / 2 - L * 0.9 * burner, 0)
        g.add_color_stop_rgba(0, 1, 0.95, 0.6, a)
        g.add_color_stop_rgba(0.4, 1, 0.45, 0.1, 0.9 * a)
        g.add_color_stop_rgba(1, 1, 0.2, 0, 0)
        ctx.move_to(-L / 2, -L * 0.06)
        ctx.line_to(-L / 2 - L * 0.9 * burner, 0)
        ctx.line_to(-L / 2, L * 0.06)
        ctx.close_path()
        ctx.set_source(g)
        ctx.fill()
    rrect(ctx, -L / 2, -L * 0.05, L * 0.85, L * 0.1, L * 0.04)
    rgba(ctx, (0.94, 0.95, 0.96), a)
    ctx.fill()
    ctx.move_to(L * 0.35, -L * 0.05)
    ctx.line_to(L / 2, 0)
    ctx.line_to(L * 0.35, L * 0.05)
    ctx.close_path()
    rgba(ctx, RED, a)
    ctx.fill()
    for sgn in (1, -1):
        ctx.move_to(-L * 0.05, sgn * L * 0.05)
        ctx.line_to(-L * 0.2, sgn * L * 0.16)
        ctx.line_to(-L * 0.25, sgn * L * 0.05)
        ctx.close_path()
        rgba(ctx, STEEL, a)
        ctx.fill()
    ctx.restore()


def launcher(ctx, x, y, s, t, elev=0.6, loaded=3, a=1.0):
    """Tracked Akash launcher seen from the side, facing right: hull, tracks, a turret with up to 3 missiles."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -230, -70, 460, 60, 22)
    rgba(ctx, hexc("#1A1E1A"), a)
    ctx.fill()
    for k in range(7):
        circle(ctx, -195 + k * 65, -40, 24, hexc("#3A3F3A"), a)
        circle(ctx, -195 + k * 65, -40, 9, STEEL, a)
    rrect(ctx, -220, -150, 440, 85, 14)
    rgba(ctx, OLIVE, a)
    ctx.fill()
    rrect(ctx, 120, -200, 100, 60, 10)
    rgba(ctx, shade(OLIVE, 0.85), a)
    ctx.fill()
    circle(ctx, 0, -160, 34, shade(OLIVE, 0.7), a)
    ctx.save()
    ctx.translate(0, -170)
    ctx.rotate(-elev)
    rrect(ctx, -170, -14, 300, 28, 8)
    rgba(ctx, shade(OLIVE, 0.75), a)
    ctx.fill()
    for k in range(loaded):
        missile(ctx, -10, -40 - k * 42, 0.0, 300, a=a)
    ctx.restore()
    ctx.restore()


def radar_panel(ctx, x, y, s, t, a=1.0):
    """Rajendra-style phased-array radar on a vehicle: a tilted square face that slowly turns."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -200, -80, 400, 70, 20)
    rgba(ctx, hexc("#1A1E1A"), a)
    ctx.fill()
    for k in range(6):
        circle(ctx, -160 + k * 64, -30, 22, hexc("#3A3F3A"), a)
    rrect(ctx, -190, -170, 380, 95, 14)
    rgba(ctx, OLIVE, a)
    ctx.fill()
    turn = 0.5 + 0.5 * math.cos(t * 0.9)
    w = 120 + 120 * turn
    ctx.move_to(-w, -470)
    ctx.line_to(w, -470)
    ctx.line_to(w * 0.9, -190)
    ctx.line_to(-w * 0.9, -190)
    ctx.close_path()
    rgba(ctx, hexc("#2C3528"), a)
    ctx.fill_preserve()
    rgba(ctx, UI, 0.7 * a)
    ctx.set_line_width(3)
    ctx.stroke()
    for i in range(1, 6):
        yy = -470 + i * 280 / 6
        line(ctx, [(-w * (1 - 0.1 * i / 6), yy), (w * (1 - 0.1 * i / 6), yy)], UI, 1.5, 0.35 * a)
    for i in range(1, 8):
        xx = -w + i * 2 * w / 8
        line(ctx, [(xx, -470), (xx * 0.9, -190)], UI, 1.5, 0.35 * a)
    ctx.restore()


def jet(ctx, x, y, s, ang, c=hexc("#5A5F68")):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(s, s)
    ctx.move_to(60, 0)
    for p in ((20, -8), (-10, -40), (-22, -40), (-14, -8), (-40, -16), (-44, 0), (-40, 16), (-14, 8), (-22, 40),
              (-10, 40), (20, 8)):
        ctx.line_to(*p)
    ctx.close_path()
    rgba(ctx, c)
    ctx.fill()
    ctx.restore()


def drone(ctx, x, y, s, t):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -30, -6, 60, 12, 6)
    rgba(ctx, hexc("#4A4F58"))
    ctx.fill()
    line(ctx, [(-8, 0), (-20, -22)], hexc("#4A4F58"), 5)
    line(ctx, [(-8, 0), (-20, 22)], hexc("#4A4F58"), 5)
    circle(ctx, 30, 0, 5, RED, 0.6 + 0.4 * math.sin(t * 10))
    ctx.restore()


def boom(ctx, x, y, u, r=90):
    if not 0 < u < 1:
        return
    glow(ctx, x, y, r * (0.6 + u), FIRE, 0.9 * (1 - u))
    circle(ctx, x, y, r * 0.45 * (0.5 + u), hexc("#FFE08A"), 0.9 * (1 - u))
    for k in range(10):
        ang = k * math.tau / 10
        circle(ctx, x + r * u * 1.3 * math.cos(ang), y + r * u * 1.3 * math.sin(ang), 6 * (1 - u), FIRE, 1 - u)


def armenia_flag(ctx, x, y, w, h, t):
    """Waving tricolour (red / blue / apricot) with its top-left corner at (x, y)."""
    n = 24
    for i in range(n):
        dx = w / n
        wave = 10 * math.sin(t * 4 + i * 0.4) * (i / n)
        for k, c in enumerate((AM_RED, AM_BLUE, AM_ORANGE)):
            ctx.rectangle(x + i * dx, y + wave + k * h / 3, dx + 1, h / 3 + 1)
            rgba(ctx, c)
            ctx.fill()
    line(ctx, [(x - 4, y - 10), (x - 4, y + h + 260)], hexc("#C9C9C9"), 7)


def india_flag(ctx, x, y, w, h, t):
    n = 24
    for i in range(n):
        dx = w / n
        wave = 10 * math.sin(t * 4 + i * 0.4 + 1) * (i / n)
        for k, c in enumerate((SAFFRON, (1, 1, 1), hexc("#138808"))):
            ctx.rectangle(x + i * dx, y + wave + k * h / 3, dx + 1, h / 3 + 1)
            rgba(ctx, c)
            ctx.fill()
    ctx.arc(x + w / 2, y + h / 2 + 5 * math.sin(t * 4 + 13), h * 0.13, 0, math.tau)
    rgba(ctx, hexc("#000080"))
    ctx.set_line_width(3)
    ctx.stroke()


def crate(ctx, x, y, c, a):
    """Shipping crate with a small missile mark: arms trade, never shown as an attack."""
    if a <= 0:
        return
    rrect(ctx, x - 34, y - 24, 68, 48, 6)
    rgba(ctx, hexc("#6B5530"), a)
    ctx.fill_preserve()
    rgba(ctx, c, a)
    ctx.set_line_width(3)
    ctx.stroke()
    line(ctx, [(x - 20, y), (x + 16, y)], (1, 1, 1), 5, a)
    ctx.move_to(x + 24, y)
    ctx.line_to(x + 14, y - 7)
    ctx.line_to(x + 14, y + 7)
    ctx.close_path()
    rgba(ctx, RED, a)
    ctx.fill()


def pin(ctx, x, y, label, c, u, below=False):
    if u <= 0:
        return
    k = ease_out_back(clamp(u / 0.35))
    glow(ctx, x, y, 70 * k, c, 0.5)
    circle(ctx, x, y, 16 * k, c)
    circle(ctx, x, y, 6 * k, (0.05, 0.05, 0.08))
    tag(ctx, label, x, y + (70 if below else -70), c, u, size=40)


def arc_pts(a, b, lift, u):
    """Point on a lifted arc from a to b at u, and its heading."""
    mx, my = (a[0] + b[0]) / 2, min(a[1], b[1]) - lift
    x = (1 - u) ** 2 * a[0] + 2 * (1 - u) * u * mx + u * u * b[0]
    y = (1 - u) ** 2 * a[1] + 2 * (1 - u) * u * my + u * u * b[1]
    dx = 2 * (1 - u) * (mx - a[0]) + 2 * u * (b[0] - mx)
    dy = 2 * (1 - u) * (my - a[1]) + 2 * u * (b[1] - my)
    return x, y, math.atan2(dy, dx)


# ============================================================ scenes

LAUNCH = (330, 960)          # where the launcher stands in the hook and the loop shot


class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"fire": c("AKASH", 0.15), "arc": c("DOOSRE", d * 0.4), "land": c("AASMAAN", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(b["fire"], "boom"), (b["fire"] + 0.05, "whoosh"), (b["land"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        sky(ctx, t)
        launcher(ctx, *LAUNCH, 0.9, t, elev=0.75, loaded=3 if t < b["fire"] else 2)
        BH, AM = (300, 760), (800, 300)
        u = clamp((t - b["fire"]) / max(0.6, b["land"] - b["fire"]))
        if t >= b["fire"]:
            pts = [arc_pts(BH, AM, 380, k * u / 30) for k in range(31)]
            line(ctx, [(p[0], p[1]) for p in pts], (1, 0.85, 0.6), 6, 0.55)
            x, y, ang = pts[-1]
            if u < 1:
                missile(ctx, x, y, ang, 140, burner=1.0)
            else:
                glow(ctx, *AM, 160, UI, 0.5)
        pin(ctx, 170, 560, "BHARAT", SAFFRON, t - b["fire"] + 0.2)
        pin(ctx, *AM, "ARMENIA", HI, t - b["arc"])
        if t > b["land"]:
            armenia_flag(ctx, 700, 400, 200, 120, t)


class Deal(Cued):
    def beats(self, d):
        c = self.cue
        return {"first": c("PEHLA", 0.3), "n": c("15", d * 0.5)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "whoosh"), (b["first"], "thud")] + [(b["n"] + 0.07 * k, "tick") for k in range(15)] + \
               [(b["n"] + 1.15, "kaching")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        sky(ctx, t, warm=0.2)
        armenia_flag(ctx, 120, 220, 400, 240, t)
        india_flag(ctx, 620, 250, 330, 200, t)
        tag(ctx, "PEHLA VIDESHI KHAREEDAR", 540, 560, SAFFRON, t - b["first"], size=44)
        n = int(15 * ease_in_out(clamp((t - b["n"]) / 1.1)))
        if t > b["n"]:
            text(ctx, f"{n}", 540, 740, 190, HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=12)
            text(ctx, "AKASH SYSTEM", 540, 860, 40, INK, font=lego.MONO)
            for k in range(n):
                x = 120 + (k % 8) * 120
                y = 960 + (k // 8) * 80
                launcher(ctx, x, y, 0.16, t, elev=0.6)


class Radar(Cued):
    def beats(self, d):
        c = self.cue
        return {"spot": c("DUSHMAN", d * 0.25), "ring": c("25", d * 0.5), "hit": c("GIRA", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.1, "beep"), (b["spot"], "alarm"), (b["ring"], "zap"), (b["hit"] - 0.6, "whoosh"),
                (b["hit"], "boom"), (b["hit"] + 0.2, "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        sky(ctx, t)
        cx, cy = 300, 980
        for k in range(3):
            r = ((t * 260 + k * 230) % 700)
            ctx.arc(cx, cy - 330, r, -math.pi * 0.5, 0.1)
            rgba(ctx, UI, 0.5 * (1 - r / 700))
            ctx.set_line_width(4)
            ctx.stroke()
        radar_panel(ctx, cx, cy, 0.62, t)
        rr = 640 * ease_out_cubic(clamp((t - b["ring"]) / 0.7))
        if rr > 0:
            ctx.arc(cx, cy - 300, rr, -math.pi * 0.62, 0.05)
            rgba(ctx, HI, 0.9)
            ctx.set_line_width(5)
            ctx.set_dash([20, 14])
            ctx.stroke()
            ctx.set_dash([])
            if rr > 500:
                tag(ctx, "25 KM", 760, 300, HI, t - b["ring"] - 0.5, size=48)
        targets = [("jet", 860, 420), ("drone", 700, 560), ("drone", 930, 650)]
        for i, (kind, tx, ty) in enumerate(targets):
            if t < b["spot"] - 0.4:
                continue
            x = tx + 60 * math.sin(t * 0.7 + i) - 40 * max(0, t - b["spot"])
            hit_u = (t - b["hit"] - 0.15 * i) / 0.8
            if hit_u < 0:
                jet(ctx, x, ty, 1.4, math.pi) if kind == "jet" else drone(ctx, x, ty, 1.2, t)
                if t > b["spot"]:
                    ctx.rectangle(x - 60, ty - 50, 120, 100)
                    rgba(ctx, RED, 0.8)
                    ctx.set_line_width(3)
                    ctx.stroke()
                fly = clamp((t - (b["hit"] - 0.9 + 0.15 * i)) / 0.9)
                if fly > 0:
                    sx, sy = cx + 40, cy - 380
                    mx, my = lerp(sx, x, fly), lerp(sy, ty, fly)
                    missile(ctx, mx, my, math.atan2(ty - sy, x - sx), 110, burner=1.0)
            else:
                boom(ctx, x, ty, hit_u)


class Four(Cued):
    def beats(self, d):
        c = self.cue
        return {"four": c("4", d * 0.35), "hit": c("NISHAANE", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["four"] + 0.1 * k, "beep") for k in range(4)] + [(b["hit"], "boom"), (b["hit"] + 0.5, "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        sky(ctx, t, warm=0.3)
        xs = [190, 420, 650, 880]
        for k, x in enumerate(xs):
            y = 380 + 40 * math.sin(k * 1.7)
            hit_u = (t - b["hit"]) / 0.8
            if hit_u < 0:
                jet(ctx, x, y, 1.1, math.pi * 0.95) if k % 2 == 0 else drone(ctx, x, y, 1.1, t)
                if t > b["four"] + 0.1 * k:
                    ctx.arc(x, y, 62, 0, math.tau)
                    rgba(ctx, RED, 0.9)
                    ctx.set_line_width(4)
                    ctx.stroke()
                fly = clamp((t - (b["hit"] - 0.8)) / 0.8)
                if fly > 0:
                    sx, sy = 540, 1000
                    missile(ctx, lerp(sx, x, fly), lerp(sy, y, fly), math.atan2(y - sy, x - sx), 110, burner=1.0)
            else:
                boom(ctx, x, y, hit_u, r=110)
        if t > b["hit"] + 0.4:
            stamp(ctx, 540, 760, t - b["hit"] - 0.4, -0.04, 560, 170, RED, [("4 / 4  EK SAATH", 0, 70, RED)])


class Loop(Cued):
    def beats(self, d):
        c = self.cue
        return {"flip": c("IB", d * 0.5), "end": c("TABHI", d * 0.88)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "soft_thud"), (b["flip"], "whoosh"), (b["flip"] + 0.3, "kaching")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        settle = clamp((t - b["end"] + 0.3) / 0.5)
        sky(ctx, t, warm=0.2 * (1 - settle))
        india_flag(ctx, 380, 420, 320, 190, t)
        flip = ease_in_out(clamp((t - b["flip"]) / 0.6))
        world = [(110, 230), (970, 260), (120, 840), (960, 820)]
        for k, (wx, wy) in enumerate(world):          # trade crates (not missiles): in = buying, out = selling
            for j in range(3):
                u = (t * 0.8 + j / 3 + k * 0.17) % 1
                a0, a1 = ((wx, wy), (540, 515)) if flip < 0.5 else ((540, 515), (wx, wy))
                x, y = lerp(a0[0], a1[0], u), lerp(a0[1], a1[1], u)
                crate(ctx, x, y, STEEL if flip < 0.5 else GREEN, (1 - settle) * min(1, u * 4, (1 - u) * 4))
        lab = ("PEHLE: SIRF KHAREEDAR", STEEL) if flip < 0.5 else ("IB: BECHNE WAALA BHI", GREEN)
        tag(ctx, lab[0], 540, 760, lab[1], (t - (0 if flip < 0.5 else b["flip"])) * (1 - settle) + 0.01, size=44)
        if settle > 0:                                   # dissolve back to the opening launcher -> seamless loop
            ctx.push_group()
            sky(ctx, t)
            launcher(ctx, *LAUNCH, 0.9, t, elev=0.75, loaded=3)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(settle)


SCENE_CLASSES = {"hook": Hook, "deal": Deal, "radar": Radar, "four": Four, "loop": Loop}
STORY = importlib.import_module(__name__)


def write_alignment(final):
    out = [{"scene": spec["key"], "start": round(s["start"], 3), "end": round(s["start"] + s["dur"], 3),
            "voiceover": NARRATION[spec["key"]], "visual": spec["visual"],
            "words": [{"t": round(s["start"] + st, 3), "w": w} for st, w in s["captions"]]}
           for spec, s in zip(SPEC, engine.SCENES)]
    path = final.with_suffix(".json")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Alignment: {path}")


UPLOAD = {
    "titles": [
        "Armenia Ne Kharidi Bharat Ki Akash Missile",
        "Akash Missile: Pehla Videshi Khareedar Armenia",
        "Bharat Ki Akash Missile Ab Armenia Ka Aasmaan Bachayegi",
        "Akash Ne Ek Saath 4 Nishane Giraye",
        "15 Akash System Armenia Ko: Bharat Ka Bada Export",
        "Akash Missile System: 25 KM Tak Drone Aur Jet Saaf",
        "Bharat Ab Hathiyar Bechta Bhi Hai: Akash Armenia Deal",
        "Akash Missile Armenia Deal Explained",
    ],
    "title": "Armenia Ne Kharidi Bharat Ki Akash Missile",
    "thumb_text": "ARMENIA",
    "queries": ["akash missile", "akash missile armenia", "akash missile system"],
    "description": """
Akash missile Armenia: Bharat ki desi Akash air defence missile ka pehla videshi khareedar Armenia bana.
आकाश मिसाइल (Akash missile system) - DRDO ki banayi, 25 KM tak dushman ke vimaan aur drone girane wali.

Is Short me:
• Armenia ne 2022 me Akash ka order diya - reports me 15 system (lagbhag Rs 6,000 crore, alag reports me figure alag)
• Pehli battery November 2024 me Bengaluru se bheji gayi
• Rajendra radar door se dushman pakadta hai, missile 25 KM tak vimaan aur drone girati hai
• Dec 2023 ke Astrashakti abhyas me ek hi Akash unit ne ek saath 4 nishane giraye
• Bharat abhi bhi bade hathiyar khareedne wale deshon me hai - par ab hathiyar bechta bhi hai

Aapke hisaab se Akash ka agla khareedar kaun hoga? Comment me likho - Jai Hind!

Sources: PIB / MoD, BEL, ETV Bharat, Raksha Anirveda (Nov 2024), PIB (Dec 2023).
""",
    "tags": ["akash missile", "akash missile armenia", "akash missile system", "आकाश मिसाइल", "india armenia defence deal",
             "akash air defence", "drdo akash", "india defence export", "rajendra radar", "indian army",
             "defence hindi", "reality shift"],
    "hashtags": ["#Shorts", "#AkashMissile", "#IndianDefence"],
    "pinned": "Akash ka agla khareedar kaun hona chahiye? Apna jawab likho - aur JAI HIND!",
}


def thumbnail(ctx):
    """1080x1920 cover: 'ARMENIA' over the firing launcher, the missile trail arcing to the Armenian flag."""
    sky(ctx, 0.5, warm=0.25)
    launcher(ctx, 380, 1180, 1.1, 0.5, elev=0.75, loaded=2)
    a, bb = (360, 900), (820, 520)
    pts = [arc_pts(a, bb, 300, k / 30) for k in range(31)]
    line(ctx, [(p[0], p[1]) for p in pts], (1, 0.85, 0.6), 10, 0.7)
    missile(ctx, pts[-1][0], pts[-1][1], pts[-1][2], 200, burner=1.0)
    armenia_flag(ctx, 640, 380, 300, 180, 0.7)
    g = cairo.LinearGradient(0, 0, 0, 700)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.9)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 700)
    ctx.set_source(g)
    ctx.fill()
    text(ctx, "AKASH", 540, 170, 200, HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "AB ARMENIA KA", 540, 320, 96, INK, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=12)
    vignette(ctx)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, INK, a=0.7)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.akash")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
