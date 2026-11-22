"""Reality Shift Short: Rezang La 1962 - 120 vs 3000.

Topic: Battle of Rezang La, 18 Nov 1962 (Chushul, Ladakh). C Company, 13 Kumaon (120 men) under Major Shaitan Singh
       held the pass against a far larger Chinese assault; 114 fell, Major Shaitan Singh was awarded the Param Vir
       Chakra (posthumous). Three months later (Feb 1963) the men were found frozen at their posts, weapons in hand.
Format: Vertical 1080x1920 (9:16), 22-25 s viral loop (AGENTS.md rule 11, Reality Shift target), 5 scenes,
        loop ending (no CTA card - the comment ask lives in the pinned comment).
Audio: user's own KikiVoice narrator recording, split per scene with --kiki-split.
Visuals: procedural Cairo Ladakh night - snow ridge, stone sangar trenches, 1962 jawans in wool greatcoats with
         .303 rifles, Major Shaitan Singh, an advancing wave of silhouettes, illumination flares, blizzard,
         snow time-lapse, golden reveal, memorial + tricolour.
On-screen text: ONLY the dynamic subtitles (AGENTS.md rule 8). No cards, ribbons or telemetry blocks.
"""

import importlib
import json
import math
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cairo

from core import delivery, engine, lego
from core.engine import *  # noqa: F401,F403
from shorts.chabahar import Cued
from shorts.akashteer import ell, poly, seg01, burst
from shorts.siachen import FAR, NEAR, mountains, snow, flag

TOPIC = "REZANG LA 1962 - 120 VS 3000"
OUTPUTS = {"edge": "rezang_la_short.mp4"}
LEGO = {"header": "radar", "caption": "typewriter", "transition": "shutter", "palette": "glacier", "ending": "prompt"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.45          # user, 22 Nov 2026: keep the dramatic KikiVoice pause tags (0.3-0.5 s) - all-comma read was too fast
TAIL_PAD = 0.30         # breath between scenes so it never sounds like a paragraph read in one go
TRIM = {"thresh": 0.006, "keep": 0.04, "keep_tail": 0.06}
MUSIC_BPM = 96
MUSIC_STYLE = "march"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 0       # user, 22 Nov 2026: no pause tags / no '...' - KikiVoice must read it in one flow; split uses Whisper

PAL = lego.PALETTES["glacier"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
GOLD = hexc("#FFD24A")
RED = hexc("#FF3B3B")
ICE = hexc("#9FE3FF")
WHITE = (1.0, 1.0, 1.0)
FIRE = hexc("#FF6A1A")
COAT = hexc("#5A5A36")
COAT_DK = hexc("#3F3F25")
WOOL_CAP = hexc("#3A3420")
STOCK = hexc("#7A4A22")
BARREL = hexc("#26262A")
BRASS = hexc("#D4A63A")
SKIN = hexc("#A9724A")
SKIN_DK = hexc("#80532F")
FROST_SKIN = hexc("#B9D3E0")
BOOT = hexc("#17140F")
STONE = hexc("#5E6670")
STONE_DK = hexc("#3E444C")
RAIDER = hexc("#2A2620")
GROUND = 1128           # feet line; caption band starts at lego.CAP_TOP = 1150
WALL_TOP = 1000         # top of the stone sangar parapet the jawans fire over

SOURCES = [
    "Gazette of India / Indian Army - Param Vir Chakra citation, Major Shaitan Singh, 13 Kumaon (posthumous), "
    "Rezang La, 18 November 1962",
    "Ministry of Defence, History Division - History of the Conflict with China, 1962 (Chushul sector, "
    "C Company 13 Kumaon at Rezang La: 120 men, 114 killed; bodies found at their posts in February 1963)",
    "PIB / Ministry of Defence, 18 Nov 2021 - Raksha Mantri rededicates the renovated Rezang La War Memorial, "
    "Chushul, Ladakh",
]

SPEC = [
    # 00:00-00:04 shock hook (zero backstory, action from frame 1)
    {"key": "wave_hook", "accent": RED, "text": "",
     "visual": "Ladakh night ridge, flares in the sky; two 1962 jawans behind a stone sangar startle, then aim as a "
               "wave of enemy silhouettes pours down the snow slope",
     "vo": [("hook", [("लद्दाख की बर्फ़ में,", "LADAKH KI BARF MEIN,"),
                      ("एक सौ बीस भारतीय जवानों पर,", "120 BHARATIYA JAWANON PAR,"),
                      ("हज़ारों चीनी सैनिक", "HAZARON CHINI SAINIK"),
                      ("टूट पड़े,", "TOOT PADE!")])]},

    # 00:04-00:09 conflict
    {"key": "cold_ammo", "accent": ICE, "text": "",
     "visual": "Blizzard; jawans fire bolt-action rifles, the row of brass rounds on the parapet empties, a jawan "
               "works an empty bolt; on PEETH NAHIN the second jawan fixes his bayonet and rises",
     "vo": [("build", [("माइनस तीस डिग्री,", "MINUS 30 DEGREE,"),
                       ("गोलियां ख़त्म होने लगीं,", "GOLIYAAN KHATAM HONE LAGIN,"),
                       ("फिर भी किसी ने", "PHIR BHI KISI NE"),
                       ("पीठ नहीं दिखाई,", "PEETH NAHIN DIKHAYI!")])]},

    # 00:09-00:14 the commander
    {"key": "major", "accent": SAFFRON, "text": "",
     "visual": "Major Shaitan Singh runs crouched between two sangars under shellfire, staggers when hit (bandaged arm), "
               "drops to one knee and keeps pointing the men forward; screen shake on each burst",
     "vo": [("punch", [("मेजर शैतान सिंह,", "MAJOR SHAITAN SINGH,"),
                       ("घायल होकर भी,", "GHAYAL HOKAR BHI,"),
                       ("आख़िरी सांस तक", "AAKHRI SAANS TAK"),
                       ("मोर्चा संभाले रहे,", "MORCHA SAMBHALE RAHE.")])]},

    # 00:14-00:20 twist + immediate impact (rule 12)
    {"key": "frozen_reveal", "accent": GOLD, "text": "",
     "visual": "Snow buries the trench in a fast time-lapse, days and nights flash past, then dawn melts it away: the jawans "
               "are still at their posts in firing position, frosted; golden pulse + aura on RIFLE",
     "vo": [("build", [("तीन महीने बाद", "3 MAHINE BAAD"),
                       ("जब बर्फ़ हटी,", "JAB BARF HATI,"),
                       ("तो सब हैरान रह गए,", "TO SAB HAIRAN REH GAYE!")]),
            ("punch", [("जवान अपने मोर्चे पर थे,", "JAWAN APNE MORCHE PAR THE,"),
                       ("हाथ में अब भी राइफ़ल,", "HAATH MEIN AB BHI RIFLE!")])]},

    # 00:20-00:24 meaning + grammatical loop back into "लद्दाख की बर्फ़ में..."
    {"key": "amar_loop", "accent": INDIA_GREEN, "text": "",
     "visual": "Rezang La memorial and tricolour at dawn, golden spirits of the jawans salute; then night falls, flares "
               "light and the enemy wave reappears exactly like scene 1 (seamless replay loop)",
     "vo": [("low", [("इसीलिए रेज़ांग ला अमर है,", "ISILIYE REZANG LA AMAR HAI,"),
                     ("क्योंकि उस रात", "KYUNKI US RAAT")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "LADAKH": ICE, "BARF": ICE, "120": SAFFRON, "BHARATIYA": SAFFRON, "JAWANON": SAFFRON,
    "HAZARON": RED, "CHINI": RED, "TOOT": RED, "PADE!": RED,
    "MINUS": ICE, "30": ICE, "GOLIYAAN": BRASS, "KHATAM": RED, "PEETH": SAFFRON, "NAHIN": SAFFRON,
    "MAJOR": GOLD, "SHAITAN": GOLD, "SINGH": GOLD, "GHAYAL": RED, "AAKHRI": SAFFRON, "SAANS": SAFFRON,
    "MORCHA": GOLD, "HAIRAN": RED, "3": ICE, "MAHINE": ICE, "HATI": ICE, "MORCHE": GOLD,
    "RIFLE": GOLD, "REZANG": GOLD, "LA": GOLD, "AMAR": SAFFRON, "RAAT": ICE,
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".—,?!")] = HOT[_k]


def mix(a, b, u):
    u = clamp(u)
    return tuple(x + (y - x) * u for x, y in zip(a, b))


# ============================================================ world: Ladakh ridge at night / dawn

NEAR_LOW = [(x, y + 70) for x, y in NEAR]


def ladakh(ctx, t, dawn=0.0, wind=1.0, flares=0, stars=True):
    """Layered Ladakh: multi-stop night->dawn sky, moon or sun, two snow ranges, the slope the wave walks down,
    illumination flares and falling snow."""
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    g.add_color_stop_rgb(0.00, *mix(hexc("#03060F"), hexc("#2C3E66"), dawn))
    g.add_color_stop_rgb(0.40, *mix(hexc("#0B1530"), hexc("#6B6F9A"), dawn))
    g.add_color_stop_rgb(0.75, *mix(hexc("#1D2C4E"), hexc("#E08F6A"), dawn))
    g.add_color_stop_rgb(1.00, *mix(hexc("#2C3E62"), hexc("#FFC98A"), dawn))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()

    if stars:
        for i in range(80):
            tw = 0.35 + 0.65 * abs(math.sin(t * (0.7 + 2 * rnd(i, 13)) + i))
            circle(ctx, rnd(i, 11) * W, 180 + rnd(i, 12) * 420, 0.8 + 1.6 * rnd(i, 14), WHITE, 0.55 * tw * (1 - dawn))
    if dawn < 0.6:   # moon
        glow(ctx, 840, 300, 220, hexc("#A9C8FF"), 0.28 * (1 - dawn))
        circle(ctx, 840, 300, 50, hexc("#F1EEE2"), 0.95 * (1 - dawn))
    if dawn > 0.2:   # sun rising behind the far range
        sy = 640 - 260 * dawn
        glow(ctx, 300, sy, 420, hexc("#FFB45C"), 0.45 * dawn)
        circle(ctx, 300, sy, 62, hexc("#FFE3A0"), dawn)

    mountains(ctx, FAR, GROUND, mix(hexc("#18243C"), hexc("#7A7FA8"), dawn), mix(hexc("#8EA2C0"), hexc("#FFE9D2"), dawn))
    mountains(ctx, NEAR_LOW, GROUND, mix(hexc("#22314F"), hexc("#8F9CC0"), dawn),
              mix(hexc("#B6C6DC"), hexc("#FFF6EA"), dawn), cap=0.4)

    ctx.move_to(0, GROUND)   # the snow slope the wave comes down
    for x in range(0, W + 20, 20):
        ctx.line_to(x, 860 + 26 * math.sin(x * 0.006 + 1.2) + 12 * math.sin(x * 0.017))
    ctx.line_to(W, GROUND)
    ctx.close_path()
    sl = cairo.LinearGradient(0, 840, 0, GROUND)
    sl.add_color_stop_rgb(0, *mix(hexc("#8D9DB8"), hexc("#F4E6D8"), dawn))
    sl.add_color_stop_rgb(1, *mix(hexc("#55647E"), hexc("#D9CFC6"), dawn))
    ctx.set_source(sl)
    ctx.fill()

    for k in range(flares):   # illumination flares drifting down on parachutes
        fx = 220 + 640 * rnd(k, 101)
        fy = 260 + ((t * 30 + 180 * k) % 320)
        flick = 0.8 + 0.2 * math.sin(t * 23 + k)
        glow(ctx, fx, fy, 520, hexc("#FFF1C2"), 0.22 * flick)
        circle(ctx, fx, fy, 9, hexc("#FFFBE8"), 0.95)
        line(ctx, [(fx, fy), (fx + 6 * math.sin(t + k), fy - 60)], (1, 1, 1), 1.5, 0.35)

    rgba(ctx, hexc("#0A0D14"))   # ground below the feet line
    ctx.rectangle(0, GROUND, W, H - GROUND)
    ctx.fill()
    snow(ctx, t, int(30 + 40 * wind), wind)


def sangar(ctx, x0, x1, top=WALL_TOP, snowcap=1.0):
    """Stone breastwork (sangar) from x0 to x1, snow lying on the top course."""
    rows = 5
    hgt = (GROUND + 8 - top) / rows
    for r in range(rows):
        y = top + r * hgt
        off = 0 if r % 2 == 0 else 34
        x = x0 - off
        k = 0
        while x < x1:
            w = 58 + 26 * rnd(r * 31 + k, 7)
            rrect(ctx, max(x, x0), y + 2, min(w, x1 - max(x, x0)) - 4, hgt - 4, 10)
            rgba(ctx, mix(STONE, STONE_DK, rnd(r * 17 + k, 9) * 0.7))
            ctx.fill()
            x += w
            k += 1
    if snowcap > 0:
        ctx.move_to(x0 - 6, top + 10)
        for x in range(int(x0), int(x1) + 20, 20):
            ctx.line_to(min(x, x1 + 6), top - 8 - 8 * rnd(x, 5))
        ctx.line_to(x1 + 6, top + 10)
        ctx.close_path()
        rgba(ctx, hexc("#EEF4FA"), snowcap)
        ctx.fill()


# ============================================================ enemy wave (respectful silhouettes)

def raider(ctx, x, y, s, t, seed, a=1.0):
    """Distant advancing soldier in a padded winter uniform, rifle forward; a silhouette, no caricature."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(-s, s)     # walks toward the Indian trench on the left of frame
    step = math.sin(t * 7 + seed)
    line(ctx, [(-8, -120), (-14 - 18 * step, 0)], RAIDER, 22, a)
    line(ctx, [(8, -120), (14 + 18 * step, 0)], RAIDER, 22, a)
    poly(ctx, [(-34, -260), (34, -260), (30, -112), (-30, -112)], RAIDER, a)
    ell(ctx, 4, -292, 28, 30)
    rgba(ctx, RAIDER, a)
    ctx.fill()
    ell(ctx, 0, -314, 34, 14)   # padded cap with flaps
    rgba(ctx, RAIDER, a)
    ctx.fill()
    line(ctx, [(10, -230), (120, -246)], RAIDER, 9, a)   # rifle carried forward
    line(ctx, [(-20, -244), (60, -230)], RAIDER, 14, a)
    ctx.restore()


def wave(ctx, t, n, push=0.0):
    """n silhouettes coming down the slope; push (0..1) moves the whole wave closer."""
    men = []
    for i in range(n):
        p = clamp(((rnd(i, 91) * 0.8 + t * 0.035 * (0.6 + rnd(i, 92))) % 0.8) + 0.2 * push)
        x = 120 + rnd(i, 93) * 900 + 18 * math.sin(t * 0.8 + i)
        men.append((p, x, i))
    for p, x, i in sorted(men):
        y = 862 + 100 * p
        raider(ctx, x, y, 0.09 + 0.15 * p, t, i, 0.35 + 0.45 * p)


def tracers(ctx, x0, y0, t, n=6, spread=1.0):
    """Rifle tracers flying from the trench toward the slope."""
    for k in range(n):
        u = (t * 2.6 + k / n) % 1.0
        tx = 520 + 420 * rnd(k, 121) * spread
        ty = 880 + 70 * rnd(k, 122)
        bx, by = x0 + (tx - x0) * u, y0 + (ty - y0) * u
        ang = math.atan2(ty - y0, tx - x0)
        line(ctx, [(bx, by), (bx + 34 * math.cos(ang), by + 34 * math.sin(ang))], FIRE, 4, 0.8)
        line(ctx, [(bx, by), (bx + 34 * math.cos(ang), by + 34 * math.sin(ang))], hexc("#FFF3A0"), 1.6, 0.9)


# ============================================================ characters (1962: wool greatcoats, .303 rifles)

def trench_jawan(ctx, x, y, s, t, pose="aim", fire=0.0, frozen=0.0, a=1.0, tint=None):
    """1962 Kumaoni jawan behind a sangar, origin at the parapet top, facing right.
    pose: aim / startle / reload / bayonet / salute. frozen 0..1 adds frost and closes the eyes.
    tint (rgb) paints him as a single glowing colour (memorial spirits). Every save() has its restore()."""
    ctx.save()
    lift = -60 if pose == "bayonet" else 0
    shiver = 2.0 * math.sin(t * 40) if pose == "startle" else 0.0
    ctx.translate(x + shiver, y + lift)
    ctx.scale(s, s)
    coat = tint or COAT
    coat_dk = tint or COAT_DK
    skin = tint or mix(SKIN, FROST_SKIN, frozen)

    rifle_ang, pivot = {"aim": (-0.05, (30, -172)), "startle": (-0.95, (30, -150)),
                        "reload": (-0.45, (30, -165)), "bayonet": (-0.12, (30, -172)),
                        "salute": (-1.57, (-58, -40))}[pose]
    kick = -10 * fire if pose == "aim" else 0.0

    def rp(px, py):
        ca, sa = math.cos(rifle_ang), math.sin(rifle_ang)
        return (pivot[0] + kick + px * ca - py * sa, pivot[1] + px * sa + py * ca)

    def arm(sh, hand, col, w, drop=36):
        el = ((sh[0] + hand[0]) / 2 - 6, (sh[1] + hand[1]) / 2 + drop)
        line(ctx, [sh, el, hand], col, w, a)
        circle(ctx, hand[0], hand[1], w * 0.5, skin if tint is None else tint, a)

    far_hand = rp(170, 0) if pose != "salute" else rp(70, 0)
    arm((-26, -180), far_hand, coat_dk, 26)                       # far arm under the forend

    poly(ctx, [(-62, 70), (62, 70), (52, -192), (-52, -192)], coat, a)   # greatcoat torso
    for bx in (-8, 12):
        for by in (-150, -100, -50):
            circle(ctx, bx + 10, by, 4, BRASS if tint is None else tint, 0.8 * a)
    line(ctx, [(-52, -192), (0, -170), (52, -192)], coat_dk, 10, a)       # collar

    ctx.save()                                                   # .303 rifle
    ctx.translate(*rp(0, 0))
    ctx.rotate(rifle_ang)
    line(ctx, [(-8, 6), (120, -2)], tint or STOCK, 18, a)
    line(ctx, [(108, -2), (238, -6)], tint or BARREL, 8, a)
    line(ctx, [(150, -6), (220, -6)], tint or STOCK, 12, a)
    if pose == "bayonet":
        line(ctx, [(236, -6), (306, -8)], tint or hexc("#C9CED6"), 5, a)
    if fire > 0 and tint is None:
        glow(ctx, 248, -6, 70, FIRE, 0.9 * fire)
        circle(ctx, 246, -6, 12 * fire, hexc("#FFF6C8"), fire)
    if frozen > 0:
        line(ctx, [(10, -10), (230, -14)], hexc("#F4FAFF"), 5, 0.85 * frozen)
    ctx.restore()

    if pose == "salute":
        arm((34, -176), (40, -262), coat, 28, drop=-30)
    else:
        bolt = 10 * math.sin(t * 12) if pose == "reload" else 0.0
        near_hand = rp(118 + bolt, -12) if pose == "reload" else rp(92, 6)
        arm((34, -176), near_hand, coat, 28)

    line(ctx, [(4, -192), (6, -212)], skin, 24, a)                   # neck
    ctx.save()
    tilt = {"startle": -0.25, "salute": -0.05}.get(pose, 0.06)
    ctx.translate(8, -248)
    ctx.rotate(tilt)
    ell(ctx, 0, 0, 40, 46)
    rgba(ctx, skin, a)
    ctx.fill()
    if tint is None:
        circle(ctx, -30, 2, 8, SKIN_DK, a)                          # ear
        if frozen > 0.5:
            for ex in (14, 30):
                line(ctx, [(ex - 6, -6), (ex + 6, -6)], (0.15, 0.1, 0.1), 3, a)
        else:
            wide = 1.7 if pose == "startle" else 1.0
            blink = 0.15 if (t % 2.9) < 0.1 else 1.0
            for ex in (14, 30):
                ell(ctx, ex, -6, 4.5, 4.5 * wide * blink)
                rgba(ctx, (0.05, 0.04, 0.04), a)
                ctx.fill()
            line(ctx, [(4, -24), (20, -26)], (0.12, 0.08, 0.06), 4, a)
            line(ctx, [(22, -26), (38, -22)], (0.12, 0.08, 0.06), 4, a)
        line(ctx, [(10, 18), (40, 20)], (0.13, 0.09, 0.07), 6, a)   # moustache
        if pose in ("startle", "bayonet"):
            ell(ctx, 26, 30, 7, 6)
            rgba(ctx, (0.25, 0.05, 0.05), a)
            ctx.fill()
    ell(ctx, -2, -34, 44, 20)                                     # wool cap comforter
    rgba(ctx, tint or WOOL_CAP, a)
    ctx.fill()
    line(ctx, [(-42, -26), (40, -24)], tint or hexc("#2A2516"), 7, a)
    if frozen > 0:
        ell(ctx, -2, -50, 40, 12)
        rgba(ctx, hexc("#F4FAFF"), 0.95 * frozen)
        ctx.fill()
    ctx.restore()
    if frozen > 0:                                               # snow on the shoulders
        for sx in (-40, 36):
            ell(ctx, sx, -194, 26, 9)
            rgba(ctx, hexc("#F4FAFF"), 0.9 * frozen)
            ctx.fill()
    ctx.restore()


OFFICER_ARMS = {   # (near upper, near fore, far upper, far fore) - radians from straight down, + = forward
    "run":     (1.10, 0.90, -0.70, -0.60),
    "command": (1.65, 0.05, -0.25, -0.40),
    "hit":     (0.35, 1.90, -0.30, -0.20),
    "kneel":   (1.75, 0.10, 0.30, 0.90),
    "salute":  (1.95, 2.25, -0.15, -0.10),
}


def limb(ctx, x0, y0, a1, l1, a2, l2, c, w, a=1.0):
    x1, y1 = x0 + l1 * math.sin(a1), y0 + l1 * math.cos(a1)
    x2, y2 = x1 + l2 * math.sin(a1 + a2), y1 + l2 * math.cos(a1 + a2)
    line(ctx, [(x0, y0), (x1, y1)], c, w, a)
    line(ctx, [(x1, y1), (x2, y2)], c, w * 0.9, a)
    return x2, y2


def major(ctx, x, y, s, t, pose="command", wounded=0.0, a=1.0):
    """Major Shaitan Singh, full figure, feet at (x, y), facing right: wool greatcoat, officer's cap, moustache,
    binoculars on the chest; wounded draws a field bandage on the far arm. save()/restore() balanced."""
    ctx.save()
    stagger = 10 * math.sin(t * 30) * wounded if pose == "hit" else 0.0
    ctx.translate(x + stagger, y)
    ctx.scale(s, s)
    ell(ctx, 0, 6, 84, 14)
    rgba(ctx, (0, 0, 0), 0.45 * a)
    ctx.fill()

    drop = 120 if pose == "kneel" else (40 if pose == "run" else 0)
    if pose == "kneel":
        line(ctx, [(-20, -170), (-70, -60), (-30, -4)], COAT_DK, 40, a)   # back leg, knee on the snow
        line(ctx, [(20, -170), (90, -120), (80, -20)], COAT_DK, 40, a)    # front leg, foot planted
        for fx in (-30, 80):
            rrect(ctx, fx - 20, -26, 46, 26, 8)
            rgba(ctx, BOOT, a)
            ctx.fill()
    else:
        sw = math.sin(t * 11) if pose == "run" else 0.0
        for side in (-1, 1):
            fx = side * 26 + 48 * sw * side
            line(ctx, [(side * 22, -230 + drop), (fx, -20)], COAT_DK, 40, a)
            rrect(ctx, fx - 20, -26, 46, 26, 8)
            rgba(ctx, BOOT, a)
            ctx.fill()

    ctx.translate(18 if pose == "run" else 0, drop)
    lean = 0.22 if pose == "run" else (0.10 if pose == "hit" else 0.0)
    ctx.rotate(lean)
    poly(ctx, [(-64, -430), (64, -430), (74, -170), (-74, -170)], COAT, a)   # greatcoat to the knee
    line(ctx, [(-64, -430), (0, -400), (64, -430)], COAT_DK, 12, a)
    rrect(ctx, -66, -262, 132, 20, 5)
    rgba(ctx, hexc("#3A2A16"), a)
    ctx.fill()
    for sx in (-50, 50):                                         # rank on the shoulders
        rrect(ctx, sx - 14, -434, 28, 10, 3)
        rgba(ctx, GOLD, a)
        ctx.fill()
    rrect(ctx, -6, -372, 34, 26, 6)                              # binoculars
    rgba(ctx, hexc("#151515"), a)
    ctx.fill()

    na1, na2, fa1, fa2 = OFFICER_ARMS[pose]
    if pose == "command":
        na1 += 0.08 * math.sin(t * 4)
    fx_, fy_ = limb(ctx, -58, -415, fa1, 105, fa2, 98, COAT_DK, 30, a)
    if wounded > 0:   # field dressing on the far upper arm
        bx, by = -58 + 60 * math.sin(fa1), -415 + 60 * math.cos(fa1)
        ell(ctx, bx, by, 22, 16)
        rgba(ctx, hexc("#F2EEE4"), wounded * a)
        ctx.fill()
    circle(ctx, fx_, fy_, 15, SKIN_DK, a)
    nx, ny = limb(ctx, 58, -415, na1, 105, na2, 98, COAT, 32, a)
    circle(ctx, nx, ny, 16, SKIN, a)

    line(ctx, [(0, -430), (0, -458)], SKIN_DK, 26, a)
    ctx.save()
    ctx.translate(0, -505)
    ell(ctx, 0, 0, 46, 52)
    rgba(ctx, SKIN, a)
    ctx.fill()
    circle(ctx, -40, 4, 9, SKIN_DK, a)
    for ex in (16, 34):
        ell(ctx, ex, -8, 5, 5)
        rgba(ctx, (0.05, 0.04, 0.04), a)
        ctx.fill()
    line(ctx, [(6, -28), (24, -32)], (0.1, 0.07, 0.05), 5, a)   # determined brows
    line(ctx, [(28, -32), (44, -26)], (0.1, 0.07, 0.05), 5, a)
    ctx.move_to(4, 22)                                           # full Rajput moustache
    ctx.curve_to(18, 12, 40, 12, 52, 26)
    ctx.curve_to(42, 22, 24, 24, 4, 30)
    ctx.close_path()
    rgba(ctx, hexc("#1A120C"), a)
    ctx.fill()
    if pose in ("command", "kneel", "run"):
        ell(ctx, 28, 38, 8, 6)
        rgba(ctx, (0.25, 0.05, 0.05), a)
        ctx.fill()
    ell(ctx, -4, -46, 54, 20)                                    # officer's cap
    rgba(ctx, hexc("#2E3A1C"), a)
    ctx.fill()
    rrect(ctx, -52, -44, 104, 16, 6)
    rgba(ctx, hexc("#232C14"), a)
    ctx.fill()
    circle(ctx, 18, -48, 8, GOLD, a)
    ctx.restore()
    ctx.restore()


def rounds(ctx, x, y, n, left):
    """Row of brass .303 rounds on the parapet; only `left` of them are still there."""
    for k in range(n):
        if k < left:
            rrect(ctx, x + k * 22, y - 34, 12, 34, 4)
            rgba(ctx, BRASS)
            ctx.fill()
            circle(ctx, x + k * 22 + 6, y - 36, 5, hexc("#B07D2A"))


def memorial(ctx, x, y, s, glow_a=0.0):
    """Simple stone obelisk memorial on the ridge (Rezang La War Memorial, Chushul)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if glow_a > 0:
        glow(ctx, 0, -200, 320, GOLD, 0.35 * glow_a)
    rrect(ctx, -110, -40, 220, 40, 6)
    rgba(ctx, hexc("#7C838C"))
    ctx.fill()
    poly(ctx, [(-46, -40), (46, -40), (26, -400), (0, -440), (-26, -400)], hexc("#9AA1AA"))
    poly(ctx, [(0, -40), (46, -40), (26, -400), (0, -440)], hexc("#848B94"))
    circle(ctx, 0, -300, 20, GOLD, 0.85)
    ctx.restore()


# ============================================================ scenes

class WaveHookScene(Cued):
    """00:00-00:04 - flares, the wave pours down, jawans startle then open fire. Same frame the loop ends on."""
    def beats(self, d):
        c = self.cue
        return {"jawan": c("JAWANON", d * 0.35), "hazar": c("HAZARON", d * 0.6), "toot": c("TOOT", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "whoosh"), (b["jawan"], "tick"), (b["hazar"], "alarm"), (b["toot"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        ladakh(ctx, t, wind=1.0, flares=2)
        n = int(lerp(18, 60, seg01(t, 0, b["toot"] + 0.3)))
        wave(ctx, t + 4.0, n, push=seg01(t, b["hazar"], b["toot"] + 0.5))
        firing = t > b["toot"]
        if firing:
            tracers(ctx, 200 + 190, WALL_TOP - 130, t)
        for k, jx in enumerate((200, 610)):
            flash = 1.0 if firing and int(t * 7 + k * 3) % 4 == 0 else 0.0
            trench_jawan(ctx, jx, WALL_TOP, 0.78, t + k, pose="aim" if firing else "startle", fire=flash)
        sangar(ctx, -10, W + 10)


class ColdAmmoScene(Cued):
    """00:04-00:09 - blizzard, rounds run out, empty bolt, then a bayonet goes on and he rises."""
    def beats(self, d):
        c = self.cue
        return {"minus": c("MINUS", 0.05), "goli": c("GOLIYAAN", d * 0.3), "khatam": c("KHATAM", d * 0.45),
                "peeth": c("PEETH", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(b["minus"], "whoosh"), (b["goli"], "tick"), (b["goli"] + 0.3, "tick"),
                (b["khatam"] + 0.4, "pick"), (b["peeth"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        gust = 1.0 + 1.4 * seg01(t, 0, 0.6)
        ladakh(ctx, t, wind=gust, flares=1)
        wave(ctx, t + 8.0, 50, push=0.6)
        left = int(round(lerp(10, 0, seg01(t, b["goli"], b["khatam"] + 0.6))))
        empty = left == 0
        p1 = "reload" if empty and t < b["peeth"] else "aim"
        flash1 = 1.0 if (not empty) and int(t * 6) % 3 == 0 else 0.0
        if not empty:
            tracers(ctx, 390, WALL_TOP - 130, t, n=4)
        trench_jawan(ctx, 200, WALL_TOP, 0.78, t, pose=p1, fire=flash1)
        rise = t > b["peeth"]
        trench_jawan(ctx, 610, WALL_TOP, 0.78 if not rise else 0.80, t + 1, pose="bayonet" if rise else "aim",
                     fire=0.0 if rise else (1.0 if int(t * 5 + 2) % 3 == 0 and not empty else 0.0))
        sangar(ctx, -10, W + 10)
        rounds(ctx, 420, WALL_TOP - 4, 10, left)
        if t > b["peeth"]:   # heavier snow sweeping across as he stands his ground
            snow(ctx, t * 1.4, 40, 2.2)


class MajorScene(Cued):
    """00:09-00:14 - Major runs between sangars under fire, hit, kneels, keeps commanding."""
    BURSTS = [(330, 820), (760, 760), (520, 700)]

    def beats(self, d):
        c = self.cue
        return {"major": c("MAJOR", 0.05), "ghayal": c("GHAYAL", d * 0.35), "aakhri": c("AAKHRI", d * 0.6),
                "morcha": c("MORCHA", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        ev = [(b["major"], "whoosh")]
        ev += [(self.hit_t(b, k), "boom") for k in range(len(self.BURSTS))]
        return ev + [(b["morcha"], "thud")]

    def hit_t(self, b, k):
        return [b["major"] + 0.4, b["ghayal"], b["aakhri"] + 0.3][k]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        shake = 0.0
        for k in range(len(self.BURSTS)):
            u = t - self.hit_t(b, k)
            if 0 < u < 0.3:
                shake = max(shake, 16 * (1 - u / 0.3))
        ctx.save()
        ctx.translate(shake * math.sin(t * 90), shake * math.cos(t * 77))
        ladakh(ctx, t, wind=1.2, flares=2)
        wave(ctx, t + 12.0, 46, push=0.7)
        for k, (bx, by) in enumerate(self.BURSTS):
            burst(ctx, bx, by, (t - self.hit_t(b, k)) / 0.9, 170)
        trench_jawan(ctx, 120, WALL_TOP, 0.72, t, pose="aim", fire=1.0 if int(t * 6) % 3 == 0 else 0.0)
        trench_jawan(ctx, 820, WALL_TOP, 0.72, t + 2, pose="aim", fire=1.0 if int(t * 6 + 1) % 3 == 0 else 0.0)
        sangar(ctx, -10, 330)
        sangar(ctx, 740, W + 10)
        if t < b["ghayal"]:
            mx, pose, w = lerp(380, 520, seg01(t, 0, b["ghayal"])), "run", 0.0
        elif t < b["aakhri"]:
            mx, pose, w = 520, "hit", 1.0
        else:
            mx, pose, w = 520, "kneel" if t > b["aakhri"] + 0.15 else "hit", 1.0
        if pose == "kneel" and t > b["morcha"]:
            pose = "kneel"
        major(ctx, mx, GROUND - 10, 0.74, t, pose=pose if pose != "kneel" else "kneel", wounded=w)
        if t > b["morcha"]:   # his order carries: gold pulse from the commander
            u = clamp((t - b["morcha"]) / 0.9)
            ctx.arc(mx + 40, GROUND - 300, 700 * ease_out_cubic(u), 0, math.tau)
            rgba(ctx, GOLD, 0.4 * (1 - u))
            ctx.set_line_width(12)
            ctx.stroke()
        ctx.restore()


class FrozenRevealScene(Cued):
    """00:14-00:20 - snow buries the post, days flash by, dawn melts it: still in firing position. Gold pulse."""
    def beats(self, d):
        c = self.cue
        return {"mahine": c("MAHINE", 0.05), "hati": c("HATI", d * 0.25), "hairan": c("HAIRAN", d * 0.4),
                "rifle": c("RIFLE", d * 0.82)}

    def events(self, d):
        b = self.beats(d)
        return [(b["mahine"], "whoosh"), (b["hati"], "shimmer"), (b["hairan"], "tock"), (b["rifle"], "zap"),
                (b["rifle"] + 0.05, "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bury = seg01(t, 0.0, 0.45)
        melt = seg01(t, b["hati"], b["hati"] + 0.8)
        cover = bury * (1 - melt)
        days = seg01(t, 0.3, b["hati"])
        dawn = 0.55 * melt + (0.5 + 0.5 * math.sin(days * 6 * math.pi)) * 0.6 * (days if melt == 0 else 0)
        ladakh(ctx, t, dawn=dawn, wind=1.6 * (1 - melt) + 0.2, flares=0, stars=melt < 0.5)
        for k, jx in enumerate((200, 610)):
            trench_jawan(ctx, jx, WALL_TOP, 0.78, 0.0, pose="aim", frozen=1.0)
        sangar(ctx, -10, W + 10, snowcap=1.0)
        if cover > 0:   # snow drift rising over the trench
            top = lerp(GROUND, WALL_TOP - 290, cover)
            ctx.move_to(0, H)
            for x in range(0, W + 20, 20):   # wind-sculpted drift: mounds where the men are
                mound = 50 * math.exp(-((x - 290) / 160) ** 2) + 50 * math.exp(-((x - 700) / 160) ** 2)
                ctx.line_to(x, top - mound * cover + 14 * math.sin(x * 0.02 + 1) + 8 * rnd(x, 3))
            ctx.line_to(W, H)
            ctx.close_path()
            dg = cairo.LinearGradient(0, top - 60, 0, GROUND)
            dg.add_color_stop_rgb(0, *hexc("#F4F8FC"))
            dg.add_color_stop_rgb(1, *hexc("#AFC3D8"))
            ctx.set_source(dg)
            ctx.fill()
            for i in range(30):   # glints on the drift
                gx, gy = rnd(i, 61) * W, top + 30 + rnd(i, 62) * (GROUND - top)
                circle(ctx, gx, gy, 2 + 2 * rnd(i, 63), WHITE, 0.5 + 0.5 * math.sin(t * 6 + i))
        if t > b["rifle"] - 0.1:   # golden pulse + aura on the men who never left
            u = clamp((t - b["rifle"]) / 1.0)
            for jx in (200, 610):
                glow(ctx, jx + 90, WALL_TOP - 160, 300, GOLD, 0.35 * (0.6 + 0.4 * math.sin(t * 5)))
            ctx.arc(420, WALL_TOP - 170, 820 * ease_out_cubic(u), 0, math.tau)
            rgba(ctx, GOLD, 0.5 * (1 - u))
            ctx.set_line_width(16)
            ctx.stroke()


class AmarLoopScene(Cued):
    """00:20-00:24 - memorial + tricolour at dawn, golden spirits salute; then night, flares and the wave return."""
    def beats(self, d):
        c = self.cue
        return {"amar": c("AMAR", d * 0.3), "raat": c("RAAT", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["amar"], "shimmer"), (b["raat"], "tick"), (d - 0.35, "whoosh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        back = seg01(t, b["raat"], d - 0.05)
        ladakh(ctx, t, dawn=0.8, wind=0.4, flares=0, stars=False)
        memorial(ctx, 540, 880, 0.9, glow_a=seg01(t, b["amar"] - 0.2, b["amar"] + 0.4))
        flag(ctx, 700, 880, t)
        spirit = seg01(t, 0.1, b["amar"])
        for k, jx in enumerate((200, 610)):
            glow(ctx, jx, WALL_TOP - 200, 260, GOLD, 0.45 * spirit)
            trench_jawan(ctx, jx, WALL_TOP, 0.78, t + k, pose="salute", a=0.6 + 0.4 * spirit)
        sangar(ctx, -10, W + 10)
        if back > 0:   # night falls back into the opening frame of scene 1
            ctx.push_group()
            ladakh(ctx, t, wind=1.0, flares=2)
            wave(ctx, 4.0 + (t - b["raat"]), 18)
            for k, jx in enumerate((200, 610)):
                trench_jawan(ctx, jx, WALL_TOP, 0.78, t + k, pose="startle")
            sangar(ctx, -10, W + 10)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(back)


SCENE_CLASSES = {
    "wave_hook": WaveHookScene,
    "cold_ammo": ColdAmmoScene,
    "major": MajorScene,
    "frozen_reveal": FrozenRevealScene,
    "amar_loop": AmarLoopScene,
}


def write_alignment(final: Path) -> None:
    out = [
        {"scene": spec["key"], "start": round(s["start"], 3), "dur": round(s["dur"], 3),
         "words": [{"t": round(s["start"] + st, 3), "w": w} for st, w in s["captions"]]}
        for spec, s in zip(SPEC, engine.SCENES)
    ]
    path = final.with_suffix(".json")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Alignment: {path}")


# ============================================================ upload kit
UPLOAD = {
    "titles": [
        "120 vs 3000! Rezang La Mein Aakhri Goli Tak Lade 🇮🇳 #shorts",
        "Rezang La 1962: 120 Jawan, Aakhri Goli, Aakhri Saans 🇮🇳 #shorts",
        "3 Mahine Baad Mile Jawan - Haath Mein Ab Bhi Rifle! #shorts",
        "Major Shaitan Singh: Rezang La Ka Amar Yoddha 🇮🇳 #shorts",
        "-30 Degree, 120 Jawan, Hazaron Dushman: Rezang La #shorts",
    ],
    "title": "120 vs 3000! Rezang La Mein Aakhri Goli Tak Lade 🇮🇳 #shorts",
    "thumb_text": "120 vs 3000",
    "queries": ["rezang la", "rezang la 1962", "major shaitan singh", "13 kumaon rezang la", "1962 war ladakh"],
    "description": """Rezang La 1962 - India China war, Ladakh. Major Shaitan Singh aur 13 Kumaon ki C Company: sirf 120 jawan, saamne hazaron chini sainik (18 November 1962, Chushul).
Minus 30 degree, goliyan khatam hone lagi, phir bhi kisi ne peeth nahi dikhayi. 120 mein se 114 jawan shaheed hue.
Major Shaitan Singh ghayal hokar bhi aakhri saans tak morcha sambhale rahe - Param Vir Chakra (maranoparant).
Teen mahine baad, February 1963 mein, jawan apne morchon par mile - haath mein ab bhi hathiyar.

Is Short mein:
• Rezang La ki ladai, 18 Nov 1962 - 13 Kumaon, C Company
• Major Shaitan Singh, PVC
• 3 mahine baad mila sach

(Chini sena ki sankhya Indian Army ke anumaan par hai.)
Sources: PVC citation (Gazette of India), MoD History Division - 1962 conflict history, PIB (Rezang La War Memorial, 2021).
""",
    "tags": [
        "rezang la", "rezang la 1962", "major shaitan singh", "13 kumaon", "1962 india china war",
        "battle of rezang la", "param vir chakra", "indian army", "ladakh", "reality shift", "jai hind",
    ],
    "hashtags": ["#Shorts", "#RezangLa", "#IndianArmy"],
    "pinned_comment": "120 jawan, aakhri goli tak. Major Shaitan Singh aur 13 Kumaon ke veeron ko salaam karne ke liye "
                      "comment mein likhein JAI HIND 🇮🇳 | Aisi aur sacchi kahaniyon ke liye Reality Shift subscribe karein.",
}


def thumbnail(ctx):
    """High-CTR cover: flares over the snow ridge, the wave coming down, jawan firing, Major commanding."""
    ladakh(ctx, 2.0, wind=1.4, flares=2)
    wave(ctx, 6.0, 70, push=0.8)
    tracers(ctx, 390, WALL_TOP - 130, 0.3, n=6)
    trench_jawan(ctx, 180, WALL_TOP, 0.80, 0.4, pose="aim", fire=1.0)
    sangar(ctx, -10, 640)
    major(ctx, 800, GROUND - 10, 0.78, 0.2, pose="command", wounded=1.0)
    text(ctx, "120 vs 3000", 540, 250, 150, RED, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "AAKHRI GOLI TAK!", 540, 400, 92, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "REZANG LA 1962", 540, 1300, 110, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, ICE, a=0.85)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.rezang_la")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
