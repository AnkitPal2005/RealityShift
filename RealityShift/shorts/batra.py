"""Reality Shift Short: Captain Vikram Batra - "Ye Dil Maange More!"

Topic: Kargil 1999. Captain Vikram Batra (13 JAK Rifles, 24) led the night assault up to Point 5140 (captured
       20 June 1999; success signal "Ye Dil Maange More"), then fell on 7 July 1999 on Point 4875 while rescuing an
       injured fellow officer. Param Vir Chakra (posthumous); Point 4875 is now called Batra Top.
Format: Vertical 1080x1920 (9:16), 22-25 s viral loop (AGENTS.md rule 11, Reality Shift target), 6 scenes,
        loop ending (the comment ask lives in the pinned comment).
Audio: user's own KikiVoice narrator recording (one paragraph, commas + pause tags only at beat ends), split per
       scene with --kiki-split.
Visuals: procedural Cairo Kargil heights - brown rock ranges with snow patches, enemy bunkers on the crest (only
         muzzle flashes, no enemy figures), night cliff climb, tricolour on the summit at dawn, rescue under fire,
         golden memory, memorial on Batra Top.
On-screen text: ONLY the dynamic subtitles (AGENTS.md rule 8).
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
from shorts.siachen import flag, mountains
from shorts.rezang_la import limb, mix, memorial

TOPIC = "CAPTAIN VIKRAM BATRA - YE DIL MAANGE MORE"
OUTPUTS = {"edge": "batra_short.mp4"}
LEGO = {"header": "intel", "caption": "chip", "transition": "shutter", "palette": "amber", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.28          # keep the even 0.23 s line pauses (the "lay"), squeeze anything longer
TAIL_PAD = 0.23
TRIM = {"thresh": 0.006, "keep": 0.04, "keep_tail": 0.06}
MUSIC_BPM = 110
MUSIC_STYLE = "pulse"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 0       # pauses are placed by hand at beat ends only (KIKI_TEXT below)

PAL = lego.PALETTES["amber"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
GOLD = hexc("#FFD24A")
RED = hexc("#FF3B3B")
WHITE = (1.0, 1.0, 1.0)
FIRE = hexc("#FF6A1A")
CAMO = hexc("#55603A")
CAMO_DK = hexc("#3A4226")
CAMO_LT = hexc("#7A7A4A")
SKIN = hexc("#B07A52")
SKIN_DK = hexc("#875A38")
BOOT = hexc("#17140F")
ROCK = hexc("#5B4A3C")
ROCK_DK = hexc("#3A2F27")
SAND = hexc("#8C7A5E")
GROUND = 1128

SOURCES = [
    "Gazette of India / Indian Army - Param Vir Chakra citation, Captain Vikram Batra, 13 JAK Rifles (posthumous), "
    "Operation Vijay 1999 (Point 5140, 20 June; Point 4875, 7 July 1999)",
    "Indian Army - Operation Vijay: capture of Point 5140, success signal 'Yeh Dil Maange More'; Point 4875 renamed "
    "Batra Top",
    "PIB / Ministry of Defence - Kargil Vijay Diwas releases on Captain Vikram Batra, PVC",
]

SPEC = [
    # 00:00-00:04 hook: action from frame 1 - the enemy holds the heights, firing down
    {"key": "bunkers", "accent": RED, "text": "",
     "visual": "Night, a high crest with three bunkers spitting muzzle flashes and tracers down the slope from the first "
               "frame; jawans pinned behind rocks look up, one points at the bunkers",
     "vo": [("hook", [("कारगिल की ऊँची चोटी पर,", "KARGIL KI OONCHI CHOTI PAR,"),
                ("दुश्मन बंकर में बैठा था,", "DUSHMAN BUNKER MEIN BAITHA THA,")])]},

    # 00:04-00:08 the climb
    {"key": "climb", "accent": SAFFRON, "text": "",
     "visual": "Captain Batra climbs a sheer night cliff hand over hand, rope swinging, a bunker flashing above",
     "vo": [("build", [("चौबीस साल का एक कैप्टन,", "24 SAAL KA EK CAPTAIN,"),
                ("रात में चट्टान चढ़ गया,", "RAAT MEIN CHATTAN CHADH GAYA,")])]},

    # 00:08-00:12 capture + the radio call
    {"key": "radio", "accent": GOLD, "text": "",
     "visual": "Dawn on the captured summit: the tricolour rises, Batra lifts the radio handset and shouts, jawans below "
               "cheer; golden pulse on MORE",
     "vo": [("build", [("सुबह चोटी पर तिरंगा था,", "SUBAH CHOTI PAR TIRANGA THA,"),
                ("रेडियो पर आवाज़ गूंजी,", "RADIO PAR AAWAZ GOONJI,"),
                ("ये दिल मांगे मोर,", "YE DIL MAANGE MORE!")])]},

    # 00:12-00:16 next mission, the rescue (rule 12: immediate impact)
    {"key": "rescue", "accent": FIRE, "text": "",
     "visual": "Smoke and shell bursts with screen shake; Batra runs carrying a wounded comrade on his shoulders; on "
               "SHAHEED he sinks to one knee as golden light falls from above (no gore)",
     "vo": [("build", [("अगले मिशन में फिर निकले,", "AGLE MISSION MEIN PHIR NIKLE,"),
                ("घायल साथी को बचाने,", "GHAYAL SAATHI KO BACHANE,"),
                ("और ख़ुद शहीद हो गए,", "AUR KHUD SHAHEED HO GAYE.")])]},

    # 00:16-00:20 the promise
    {"key": "promise", "accent": SAFFRON, "text": "",
     "visual": "Golden memory: Batra smiling in front of a huge waving tricolour; on LIPATKAR the flag glow sweeps "
               "around him",
     "vo": [("low", [("जाने से पहले कहा था,", "JAANE SE PEHLE KAHA THA,"),
                ("तिरंगा लहराकर आऊँगा,", "TIRANGA LEHRAKAR AAUNGA,"),
                ("या तिरंगे में लिपटकर,", "YA TIRANGE MEIN LIPATKAR.")])]},

    # 00:20-00:24 Batra Top + grammatical loop back into the first line
    {"key": "batra_top", "accent": INDIA_GREEN, "text": "",
     "visual": "Name reveal on Batra Top: memorial and tricolour at dawn, two jawans salute; at the end night falls and the bunker "
               "frame of scene 1 returns (seamless replay loop)",
     "vo": [("low", [("वो थे कैप्टन विक्रम बत्रा,", "WO THE CAPTAIN VIKRAM BATRA,"),
                ("और ये कहानी शुरू हुई,", "AUR YE KAHANI SHURU HUI")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

# KikiVoice text (user, 22 Nov 2026): KikiVoice rushes through long stretches, so the script is written as a steady
# "lay": every line 4-5 words of near-equal length, and the SAME short tag after EVERY line - one even rhythm.
KIKI_LINE_MS = 230
KIKI_TEXT = f" (({chr(0x23F1)}={KIKI_LINE_MS})) ".join(hi.rstrip(",") + "," for _, chunks in SCRIPT
                                                    for hi, _ in chunks).rstrip(",")

HOT = {
    "KARGIL": SAFFRON, "OONCHI": SAFFRON, "CHOTI": SAFFRON, "DUSHMAN": RED, "BUNKER": RED,
    "24": GOLD, "CAPTAIN": GOLD, "RAAT": SAFFRON, "CHATTAN": SAFFRON, "CHADH": SAFFRON,
    "SUBAH": GOLD, "TIRANGA": SAFFRON, "RADIO": GOLD, "GOONJI,": GOLD, "DIL": RED, "MAANGE": RED, "MORE!": GOLD,
    "MISSION": FIRE, "GHAYAL": RED, "SAATHI": SAFFRON, "KHUD": GOLD, "SHAHEED": GOLD,
    "TIRANGE": SAFFRON, "LEHRAKAR": INDIA_GREEN, "LIPATKAR.": GOLD,
    "VIKRAM": GOLD, "BATRA,": GOLD, "KAHANI": SAFFRON, "SHURU": SAFFRON,
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".—,?!")] = HOT[_k]


# ============================================================ world: Kargil heights

FAR = [(0, 600), (110, 470), (230, 560), (360, 400), (480, 520), (600, 360), (720, 500), (860, 420), (980, 540),
       (1080, 470)]
MID = [(0, 760), (150, 640), (300, 720), (450, 600), (620, 700), (780, 620), (930, 720), (1080, 660)]


def kargil(ctx, t, dawn=0.0, smoke=0.0):
    """Layered Kargil: night->dawn sky, moon or sun, two brown rock ranges with snow patches, dust motes."""
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    g.add_color_stop_rgb(0.00, *mix(hexc("#050812"), hexc("#3A3F6A"), dawn))
    g.add_color_stop_rgb(0.45, *mix(hexc("#121A33"), hexc("#B0708A"), dawn))
    g.add_color_stop_rgb(0.80, *mix(hexc("#2A2A40"), hexc("#F2A060"), dawn))
    g.add_color_stop_rgb(1.00, *mix(hexc("#3A2E36"), hexc("#FFD08A"), dawn))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    for i in range(70):
        circle(ctx, rnd(i, 11) * W, 180 + rnd(i, 12) * 380, 0.8 + 1.5 * rnd(i, 14), WHITE,
               0.5 * (1 - dawn) * (0.4 + 0.6 * abs(math.sin(t * 1.3 + i))))
    if dawn < 0.6:
        glow(ctx, 230, 300, 200, hexc("#A9C8FF"), 0.25 * (1 - dawn))
        circle(ctx, 230, 300, 44, hexc("#F1EEE2"), 0.95 * (1 - dawn))
    if dawn > 0.2:
        sy = 620 - 280 * dawn
        glow(ctx, 820, sy, 460, hexc("#FFB45C"), 0.5 * dawn)
        circle(ctx, 820, sy, 66, hexc("#FFE3A0"), dawn)
    mountains(ctx, FAR, GROUND, mix(hexc("#2A2633"), hexc("#8E7A86"), dawn),
              mix(hexc("#9AA2B8"), hexc("#FFEBDA"), dawn), cap=0.25)
    mountains(ctx, MID, GROUND, mix(hexc("#3A2F2A"), hexc("#9A7A62"), dawn),
              mix(hexc("#A8A6AE"), hexc("#FFF1E2"), dawn), cap=0.18)
    sl = cairo.LinearGradient(0, 900, 0, GROUND)   # rocky foreground slope
    sl.add_color_stop_rgb(0, *mix(hexc("#3E342C"), hexc("#A08468"), dawn))
    sl.add_color_stop_rgb(1, *mix(hexc("#241E19"), hexc("#6E5844"), dawn))
    ctx.move_to(0, GROUND)
    for x in range(0, W + 20, 20):
        ctx.line_to(x, 930 + 30 * math.sin(x * 0.008 + 0.6) + 14 * math.sin(x * 0.03))
    ctx.line_to(W, GROUND)
    ctx.close_path()
    ctx.set_source(sl)
    ctx.fill()
    for i in range(18):   # scattered boulders
        bx, by = rnd(i, 31) * W, 960 + rnd(i, 32) * 150
        ell(ctx, bx, by, 26 + 30 * rnd(i, 33), 14 + 14 * rnd(i, 34))
        rgba(ctx, mix(ROCK_DK, ROCK, dawn))
        ctx.fill()
    rgba(ctx, hexc("#0A0A0E"))
    ctx.rectangle(0, GROUND, W, H - GROUND)
    ctx.fill()
    if smoke > 0:
        for i in range(10):
            sx = (rnd(i, 41) * W + t * 30) % (W + 300) - 150
            sy = 640 + rnd(i, 42) * 400 - t * 12
            glow(ctx, sx, sy, 180 + 80 * rnd(i, 43), hexc("#5A5048"), 0.45 * smoke)
    for i in range(22):
        mx = (rnd(i, 51) * W + t * (8 + 14 * rnd(i, 52))) % W
        my = (300 + rnd(i, 53) * 760 - t * 10) % 800 + 260
        circle(ctx, mx, my, 1.5 + 2 * rnd(i, 54), hexc("#FFE6B0"), 0.06 + 0.07 * rnd(i, 55))


def crest(ctx, cx, top, half, dawn=0.0):
    """The tall rock crest the enemy held (Point 5140 style), apex at (cx, top)."""
    pts = [(cx - half, GROUND), (cx - half * 0.7, top + 260), (cx - half * 0.35, top + 90), (cx - 40, top + 20),
           (cx, top), (cx + 50, top + 30), (cx + half * 0.4, top + 120), (cx + half * 0.75, top + 300),
           (cx + half, GROUND)]
    poly(ctx, pts, mix(hexc("#2F2722"), hexc("#7E6650"), dawn))
    poly(ctx, [(cx - 40, top + 20), (cx, top), (cx + 50, top + 30), (cx + 10, top + 60)],
         mix(hexc("#B9B6BE"), hexc("#FFF2E6"), dawn))
    for k in range(9):   # rock strata
        y = top + 120 + k * 80
        line(ctx, [(cx - half * 0.5 + 30 * rnd(k, 3), y), (cx + half * 0.4, y + 20)], hexc("#1E1915"), 3, 0.4)


def bunker(ctx, x, y, t, firing=True, seed=0, a=1.0):
    """Stone-and-sandbag bunker with a firing slit; muzzle flashes only (no enemy figures)."""
    rrect(ctx, x - 70, y - 50, 140, 54, 14)
    rgba(ctx, hexc("#4A3E33"), a)
    ctx.fill()
    for k in range(4):
        ell(ctx, x - 52 + k * 35, y - 52, 20, 11)
        rgba(ctx, hexc("#6C5A46"), a)
        ctx.fill()
    rrect(ctx, x - 36, y - 30, 72, 12, 4)
    rgba(ctx, hexc("#0B0806"), a)
    ctx.fill()
    if firing and int(t * 12 + seed) % 3 == 0:
        glow(ctx, x, y - 24, 70, FIRE, 0.9 * a)
        circle(ctx, x, y - 24, 9, hexc("#FFF4C8"), a)


def down_tracers(ctx, sources, t, n=8):
    """Enemy tracers raining down from the bunkers onto the slope."""
    for k in range(n):
        sx, sy = sources[k % len(sources)]
        u = (t * 2.2 + k / n) % 1.0
        tx, ty = 120 + 860 * rnd(k, 71), 1000 + 80 * rnd(k, 72)
        bx, by = sx + (tx - sx) * u, sy + (ty - sy) * u
        ang = math.atan2(ty - sy, tx - sx)
        line(ctx, [(bx, by), (bx + 36 * math.cos(ang), by + 36 * math.sin(ang))], RED, 4, 0.8)
        line(ctx, [(bx, by), (bx + 36 * math.cos(ang), by + 36 * math.sin(ang))], hexc("#FFD0C0"), 1.5, 0.9)


# ============================================================ characters (1999: disruptive-pattern combat dress)

ARMS = {   # (near upper, near fore, far upper, far fore) - radians from straight down, + = forward
    "stand":  (0.15, 0.10, -0.15, -0.10),
    "cheer":  (2.95, 0.15, -2.70, -0.20),
    "radio":  (2.45, 2.05, -2.85, -0.15),
    "point":  (1.65, 0.05, -0.25, -0.40),
    "look_up": (0.50, 1.20, -0.30, -1.30),
    "climb":  (2.95, 0.10, 2.60, 0.20),
    "carry":  (2.55, 1.85, 2.25, 1.95),
    "kneel":  (0.90, 0.70, 0.30, 0.90),
    "salute": (1.95, 2.25, -0.15, -0.10),
    "smile":  (0.55, 1.75, -0.20, -0.30),   # hand resting at the chest
}


def fauji(ctx, x, y, s, t, pose="stand", flip=False, captain=False, a=1.0, glow_a=0.0):
    """1999 Indian Army soldier, feet at (x, y), facing right (flip faces left). captain=True draws Captain Batra:
    dark patka-style head scarf instead of a helmet, rank pips, radio handset in the radio pose, clean-shaven smile.
    Every save() is matched by a restore() (AGENTS.md rule 6)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(-s if flip else s, s)
    if glow_a > 0:
        glow(ctx, 0, -300, 380, GOLD, 0.45 * glow_a)
    ell(ctx, 0, 6, 84, 14)
    rgba(ctx, (0, 0, 0), 0.45 * a)
    ctx.fill()

    drop = 110 if pose == "kneel" else 0
    if pose == "kneel":
        line(ctx, [(-20, -170), (-70, -60), (-30, -4)], CAMO_DK, 40, a)
        line(ctx, [(20, -170), (90, -120), (80, -20)], CAMO_DK, 40, a)
        feet = (-30, 80)
    elif pose == "climb":
        k = math.sin(t * 6)
        line(ctx, [(-18, -230), (-30 + 30 * k, -120), (-24 + 20 * k, -10)], CAMO_DK, 40, a)
        line(ctx, [(18, -230), (60 - 30 * k, -170), (40 - 20 * k, -80)], CAMO_DK, 40, a)
        feet = (-24 + 20 * k, 40 - 20 * k)
    else:
        sw = math.sin(t * 11) if pose == "carry" else 0.0
        for side in (-1, 1):
            fx = side * 26 + 44 * sw * side
            line(ctx, [(side * 22, -230), (fx, -20)], CAMO_DK, 40, a)
        feet = (-26 + -44 * sw, 26 + 44 * sw)
    for fx in feet:
        rrect(ctx, fx - 20, -26 - (80 if pose == "climb" and fx == feet[1] else 0), 46, 26, 8)
        rgba(ctx, BOOT, a)
        ctx.fill()

    ctx.translate(0, drop)
    if pose == "carry":   # wounded comrade across the shoulders
        ctx.save()
        ctx.translate(0, -470)
        rrect(ctx, -150, -40, 260, 74, 30)
        rgba(ctx, CAMO_DK, a)
        ctx.fill()
        circle(ctx, 140, -6, 34, SKIN_DK, a)
        line(ctx, [(-150, 0), (-200, 70)], CAMO_DK, 30, a)
        line(ctx, [(-130, 10), (-170, 90)], CAMO_DK, 30, a)
        line(ctx, [(100, 20), (120, 110)], CAMO_DK, 24, a)
        ctx.restore()

    poly(ctx, [(-62, -430), (62, -430), (56, -225), (-56, -225)], CAMO, a)
    for k in range(10):   # disruptive pattern
        ell(ctx, -45 + 90 * rnd(k, 71 + captain), -410 + 170 * rnd(k, 72), 15, 9)
        rgba(ctx, CAMO_DK if k % 2 else CAMO_LT, 0.7 * a)
        ctx.fill()
    rrect(ctx, -58, -250, 116, 20, 5)
    rgba(ctx, hexc("#1F1A12"), a)
    ctx.fill()
    if captain:
        for sx in (-46, 46):
            for p in range(3):   # three pips: Captain
                circle(ctx, sx - 10 + p * 10, -426, 4, GOLD, a)
    else:
        for px in (-34, 0, 34):
            rrect(ctx, px - 13, -330, 26, 32, 5)
            rgba(ctx, CAMO_DK, a)
            ctx.fill()

    na1, na2, fa1, fa2 = ARMS[pose]
    if pose in ("cheer", "radio"):
        fa2 += 0.25 * math.sin(t * 9)
    lx, ly = limb(ctx, -58, -415, fa1, 105, fa2, 98, CAMO_DK, 30, a)
    circle(ctx, lx, ly, 15, SKIN_DK, a)
    rx, ry = limb(ctx, 58, -415, na1, 105, na2, 98, CAMO, 32, a)
    circle(ctx, rx, ry, 16, SKIN, a)
    if pose == "radio" and captain:   # handset at the ear, coiled cord
        rrect(ctx, rx - 12, ry - 30, 24, 60, 8)
        rgba(ctx, hexc("#1A1A1A"), a)
        ctx.fill()
        line(ctx, [(rx, ry + 30), (rx - 20, ry + 80), (rx + 10, ry + 120), (-20, -300)], hexc("#222222"), 3, a)

    line(ctx, [(0, -430), (0, -458)], SKIN_DK, 26, a)
    ctx.save()
    tilt = -0.28 if pose in ("look_up", "climb", "cheer") else 0.0
    ctx.translate(0, -505)
    ctx.rotate(tilt)
    ell(ctx, 0, 0, 46, 52)
    rgba(ctx, SKIN, a)
    ctx.fill()
    circle(ctx, -40, 4, 9, SKIN_DK, a)
    for ex in (16, 34):
        ell(ctx, ex, -8, 5, 5 if pose != "kneel" else 1.5)
        rgba(ctx, (0.05, 0.04, 0.04), a)
        ctx.fill()
    line(ctx, [(6, -26), (24, -30)], (0.1, 0.07, 0.05), 4, a)
    line(ctx, [(28, -30), (44, -24)], (0.1, 0.07, 0.05), 4, a)
    if not captain:
        line(ctx, [(10, 18), (40, 20)], (0.13, 0.09, 0.07), 6, a)
    if pose in ("cheer", "radio"):
        ell(ctx, 28, 30, 11, 12)
        rgba(ctx, (0.25, 0.05, 0.05), a)
        ctx.fill()
    elif pose in ("smile", "salute", "stand") and captain:
        ctx.arc(26, 18, 14, 0.2, math.pi - 0.2)
        rgba(ctx, (0.3, 0.1, 0.08), a)
        ctx.set_line_width(4)
        ctx.stroke()
    else:
        line(ctx, [(14, 26), (36, 26)], (0.3, 0.12, 0.1), 3, a)
    if captain:   # dark patka-style head scarf with a knot at the back
        ctx.move_to(-48, -10)
        ctx.curve_to(-50, -70, 48, -76, 50, -14)
        ctx.close_path()
        rgba(ctx, hexc("#1E2414"), a)
        ctx.fill()
        poly(ctx, [(-46, -24), (-84, -6), (-78, 14), (-44, -4)], hexc("#1E2414"), a)
    else:         # combat helmet with net
        ctx.move_to(-56, -16)
        ctx.curve_to(-56, -92, 58, -92, 60, -14)
        ctx.close_path()
        rgba(ctx, hexc("#3E4A26"), a)
        ctx.fill()
        for k in range(5):
            line(ctx, [(-44 + k * 22, -66), (-50 + k * 24, -20)], hexc("#2B3419"), 2, 0.8 * a)
    ctx.restore()
    ctx.restore()


def golden_rays(ctx, cx, u, t):
    """Light falling from above, u = 0..1 strength."""
    if u <= 0:
        return
    for k in range(9):
        ang = -math.pi / 2 + (k - 4) * 0.09 + 0.02 * math.sin(t + k)
        x1, y1 = cx + 1400 * math.cos(ang + math.pi), -200
        ctx.move_to(cx, GROUND - 300)
        ctx.line_to(x1 - 40, y1)
        ctx.line_to(x1 + 40, y1)
        ctx.close_path()
        rgba(ctx, GOLD, 0.10 * u)
        ctx.fill()
    glow(ctx, cx, GROUND - 300, 420, GOLD, 0.4 * u)


def big_flag(ctx, cx, cy, w, h, t, a=1.0):
    """Large waving tricolour filling the sky behind the memory scene."""
    n = 30
    for i in range(n):
        u = i / n
        dy = 26 * math.sin(t * 3 - u * 6) * u
        for k, c in enumerate((SAFFRON, (1, 1, 1), INDIA_GREEN)):
            ctx.rectangle(cx - w / 2 + w * u, cy - h / 2 + dy + k * h / 3, w / n + 1, h / 3 + 0.5)
            rgba(ctx, c, a)
            ctx.fill()
    mid_dy = 26 * math.sin(t * 3 - 3) * 0.5
    ctx.arc(cx, cy + mid_dy, h / 7, 0, math.tau)
    rgba(ctx, hexc("#000080"), a)
    ctx.set_line_width(4)
    ctx.stroke()


# ============================================================ scenes

def summit_frame(ctx, t, flag_a=1.0, batra_pose="radio", crowd="cheer"):
    """The captured summit at dawn: tricolour, Batra on the radio, jawans below."""
    kargil(ctx, t, dawn=0.75)
    crest(ctx, 640, 640, 480, dawn=0.75)
    if flag_a > 0:
        flag(ctx, 720, 650, t, a=flag_a)
    fauji(ctx, 620, 680, 0.62, t, pose=batra_pose, captain=True)
    fauji(ctx, 200, GROUND - 10, 0.74, t + 1, pose=crowd)
    fauji(ctx, 360, GROUND - 10, 0.70, t + 2, pose=crowd)


BUNKERS = [(470, 760), (560, 680), (690, 740)]


def bunker_frame(ctx, t, point=False):
    """Night, the enemy crest firing down on the jawans (scene 1 and the loop target)."""
    kargil(ctx, t, dawn=0.0)
    crest(ctx, 580, 600, 520)
    for k, (bx, by) in enumerate(BUNKERS):
        bunker(ctx, bx, by, t, firing=True, seed=k)
    down_tracers(ctx, [(bx, by - 24) for bx, by in BUNKERS], t)
    fauji(ctx, 230, GROUND - 10, 0.74, t, pose="look_up")
    fauji(ctx, 820, GROUND - 10, 0.76, t + 1, pose="point" if point else "look_up", flip=True)


class BunkersScene(Cued):
    """00:00-00:04 - hook: the crest is already firing on frame 1 (same frame the loop ends on)."""
    def beats(self, d):
        c = self.cue
        return {"dushman": c("DUSHMAN", d * 0.45), "bunker": c("BUNKERON", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "zap"), (0.3, "zap"), (b["dushman"], "alarm"), (b["bunker"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bunker_frame(ctx, t, point=t > b["bunker"] - 0.1)


class ClimbScene(Cued):
    """00:04-00:08 - the night climb up the sheer cliff."""
    def beats(self, d):
        c = self.cue
        return {"raat": c("RAAT", d * 0.4), "chadh": c("CHADH", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "whoosh"), (b["raat"], "pick"), (b["chadh"], "pick"), (b["chadh"] + 0.4, "pick")]

    def draw(self, ctx, t, d):
        kargil(ctx, t, dawn=0.0)
        cliff_x = 470   # sheer cliff face on the right half
        ctx.move_to(cliff_x, GROUND)
        for k in range(12):
            ctx.line_to(cliff_x + 30 * math.sin(k * 1.7), GROUND - k * 55)
        ctx.line_to(cliff_x - 10, 520)
        ctx.line_to(W, 520)
        ctx.line_to(W, GROUND)
        ctx.close_path()
        rgba(ctx, hexc("#2E2620"))
        ctx.fill()
        for k in range(10):
            line(ctx, [(cliff_x + 40, 560 + k * 56), (W, 580 + k * 56)], hexc("#1E1915"), 3, 0.35)
        bunker(ctx, 820, 520, t, firing=True, seed=2)
        line(ctx, [(cliff_x + 20, 520), (cliff_x - 6 + 10 * math.sin(t * 2), GROUND)], hexc("#C9B48A"), 3, 0.8)
        up = seg01(t, 0.1, d - 0.1)
        fauji(ctx, cliff_x - 60, lerp(GROUND - 10, 620, up), 0.70, t, pose="climb", captain=True)


class RadioScene(Cued):
    """00:08-00:12 - dawn on the summit: tricolour rises, the radio call, the cheer."""
    def beats(self, d):
        c = self.cue
        return {"tiranga": c("TIRANGA", d * 0.2), "radio": c("RADIO", d * 0.45), "more": c("MORE", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "shimmer"), (b["radio"], "beep"), (b["more"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        summit_frame(ctx, t, flag_a=seg01(t, 0.0, b["tiranga"] + 0.3),
                     batra_pose="radio" if t > b["radio"] - 0.1 else "point",
                     crowd="cheer" if t > b["more"] - 0.1 else "stand")
        if t > b["more"] - 0.05:
            u = clamp((t - b["more"]) / 1.0)
            ctx.arc(640, 560, 900 * ease_out_cubic(u), 0, math.tau)
            rgba(ctx, GOLD, 0.5 * (1 - u))
            ctx.set_line_width(16)
            ctx.stroke()


class RescueScene(Cued):
    BURSTS = [(300, 820), (760, 760), (520, 690)]

    def beats(self, d):
        c = self.cue
        return {"mission": c("MISSION", 0.05), "ghayal": c("GHAYAL", d * 0.35), "shaheed": c("SHAHEED", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        ev = [(self.hit_t(b, k), "boom") for k in range(3)]
        return ev + [(b["shaheed"], "soft_thud"), (b["shaheed"] + 0.3, "shimmer")]

    def hit_t(self, b, k):
        return [b["mission"] + 0.3, b["ghayal"], b["ghayal"] + 0.7][k]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        shake = 0.0
        for k in range(3):
            u = t - self.hit_t(b, k)
            if 0 < u < 0.3:
                shake = max(shake, 16 * (1 - u / 0.3))
        ctx.save()
        ctx.translate(shake * math.sin(t * 90), shake * math.cos(t * 77))
        fall = seg01(t, b["shaheed"], b["shaheed"] + 0.5)
        kargil(ctx, t, dawn=0.25, smoke=1.0 - 0.6 * fall)
        for k, (bx, by) in enumerate(self.BURSTS):
            burst(ctx, bx, by, (t - self.hit_t(b, k)) / 0.9, 170)
        if t < b["shaheed"]:
            x = lerp(820, 480, seg01(t, 0, b["shaheed"]))
            fauji(ctx, x, GROUND - 10, 0.72, t, pose="carry", captain=True, flip=True)
        else:
            golden_rays(ctx, 520, fall, t)
            fauji(ctx, 380, GROUND - 10, 0.70, 0.0, pose="kneel", flip=True)   # the comrade he got to safety
            fauji(ctx, 560, GROUND - 10, 0.72, t, pose="kneel", captain=True, glow_a=fall)
        ctx.restore()


class PromiseScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"tiranga": c("TIRANGA", d * 0.35), "lipat": c("LIPATKAR", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "shimmer"), (b["tiranga"], "whoosh"), (b["lipat"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        kargil(ctx, t, dawn=0.9)
        big_flag(ctx, 540, 520, 860, 520, t, a=0.35 + 0.55 * seg01(t, b["tiranga"] - 0.3, b["tiranga"] + 0.3))
        wrap = seg01(t, b["lipat"], b["lipat"] + 0.8)
        fauji(ctx, 540, GROUND - 10, 0.78, t, pose="smile", captain=True, glow_a=0.5 + 0.5 * wrap)
        if wrap > 0:   # the flag's glow sweeps around him
            for k, c in enumerate((SAFFRON, WHITE, INDIA_GREEN)):
                ctx.arc(540, GROUND - 230, 250 + k * 22, math.pi * (1.1 - 0.9 * wrap), math.pi * 1.9)
                rgba(ctx, c, 0.55 * wrap)
                ctx.set_line_width(14)
                ctx.stroke()


class BatraTopScene(Cued):
    def beats(self, d):
        c = self.cue
        return {"top": c("VIKRAM", d * 0.25), "yaad": c("KAHANI", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["top"], "shimmer"), (b["yaad"], "tick"), (d - 0.35, "whoosh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        back = seg01(t, b["yaad"], d - 0.05)
        kargil(ctx, t, dawn=0.85)
        crest(ctx, 560, 640, 480, dawn=0.85)
        memorial(ctx, 540, 700, 0.55, glow_a=seg01(t, b["top"] - 0.2, b["top"] + 0.4))
        flag(ctx, 640, 690, t)
        fauji(ctx, 230, GROUND - 10, 0.74, t, pose="salute")
        fauji(ctx, 840, GROUND - 10, 0.74, t + 1, pose="salute", flip=True)
        if back > 0:
            ctx.push_group()
            bunker_frame(ctx, t)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(back)


SCENE_CLASSES = {
    "bunkers": BunkersScene,
    "climb": ClimbScene,
    "radio": RadioScene,
    "rescue": RescueScene,
    "promise": PromiseScene,
    "batra_top": BatraTopScene,
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
        "24 Saal, 1 Radio Message: \"Ye Dil Maange More!\" 🇮🇳 #shorts",
        "Captain Vikram Batra: Ye Dil Maange More Ki Asli Kahani 🇮🇳 #shorts",
        "Kargil 1999: Jis Captain Ke Naam Par Hai Batra Top #shorts",
        "\"Tiranga Lehrakar Aaunga Ya Lipatkar\" - Captain Batra 🇮🇳 #shorts",
        "Ye Dil Maange More! Kargil Ka Sher Shah #shorts",
    ],
    "title": "24 Saal, 1 Radio Message: \"Ye Dil Maange More!\" 🇮🇳 #shorts",
    "thumb_text": "DIL MAANGE MORE",
    "queries": ["captain vikram batra", "ye dil maange more", "kargil war 1999", "batra top", "vikram batra kargil"],
    "description": """Captain Vikram Batra, Kargil war 1999 - "Ye Dil Maange More!" 13 JAK Rifles ke 24 saal ke Captain ne raat mein khadi chattan chadhkar Point 5140 jeeta (20 June 1999). Aaj Point 4875 "Batra Top" kehlata hai.
Agle mission mein Point 4875 par ghayal saathi ko bachate hue 7 July 1999 ko shaheed hue - Param Vir Chakra (maranoparant).
Jaate samay unhone kaha tha: "Ya toh tiranga lehrakar aaunga, ya tirange mein lipatkar aaunga, par aaunga zaroor."
Aaj Point 4875 ko "Batra Top" kaha jaata hai.

Is Short mein:
• Point 5140 ka capture aur "Ye Dil Maange More" signal
• Point 4875 par rescue aur balidan
• Batra Top

Sources: PVC citation (Gazette of India), Indian Army - Operation Vijay, PIB Kargil Vijay Diwas releases.
""",
    "tags": [
        "captain vikram batra", "ye dil maange more", "kargil war", "kargil 1999", "batra top", "param vir chakra",
        "13 jak rifles", "operation vijay", "indian army", "reality shift", "jai hind",
    ],
    "hashtags": ["#Shorts", "#VikramBatra", "#Kargil"],
    "pinned_comment": "\"Ya tiranga lehrakar aaunga, ya tirange mein lipatkar\" - Captain Vikram Batra, PVC 🇮🇳 "
                      "Unhe salaam karne ke liye comment mein likhein JAI HIND | Aisi aur sacchi kahaniyon ke liye "
                      "Reality Shift subscribe karein.",
}


def thumbnail(ctx):
    """High-CTR cover: Batra on the summit with the radio and the tricolour, jawans cheering."""
    kargil(ctx, 1.2, dawn=0.75)          # sky behind the shifted scene so the top never shows a void
    ctx.save()
    ctx.translate(0, 200)                # push the summit (not the sky) down so the title never covers his face
    crest(ctx, 640, 640, 480, dawn=0.75)
    flag(ctx, 720, 650, 1.2)
    glow(ctx, 640, 520, 420, GOLD, 0.25)
    fauji(ctx, 620, 680, 0.62, 1.2, pose="radio", captain=True)
    ctx.restore()
    fauji(ctx, 200, GROUND - 10, 0.74, 2.2, pose="cheer")
    fauji(ctx, 360, GROUND - 10, 0.70, 3.2, pose="cheer")
    text(ctx, "YE DIL", 540, 230, 140, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "MAANGE MORE!", 540, 380, 130, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "CAPTAIN BATRA", 540, 1300, 110, SAFFRON, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, GOLD, a=0.85)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.batra")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
