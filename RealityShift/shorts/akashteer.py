"""Reality Shift Short: Akashteer - Ek Raat, 400 Tak Drone.

Topic: Akashteer, the Army's automated air-defence control & reporting network (BEL), and the night of
       8-9 May 2025 (Operation Sindoor) when Pakistan sent 300-400 drones at 36 locations.
Format: Vertical 1080x1920 (9:16), <= 25 s viral loop (AGENTS.md rule 11), 5 scenes, loop ending (no CTA card).
Audio: user's own KikiVoice narrator recording (kiki_narrator text), split per scene with --kiki-split.
Visuals: procedural Cairo night battlefield - drone swarm over a lit city, jawan + commander characters,
         radar towers networking into a command vehicle, Akash launcher + L-70 gun intercepts, a golden shield dome.
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

TOPIC = "AKASHTEER AIR DEFENCE NETWORK"
OUTPUTS = {"edge": "akashteer_short.mp4"}
LEGO = {"header": "intel", "caption": "typewriter", "transition": "scan", "palette": "intel", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.04          # AGENTS.md rule 10: no stutter pauses
TAIL_PAD = 0.04
TRIM = {"thresh": 0.006, "keep": 0.04, "keep_tail": 0.06}
MUSIC_BPM = 104
MUSIC_STYLE = "tension"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 200     # only a cut marker for --kiki-split; MAX_GAP squeezes it back to 0.04 s in the render

PAL = lego.PALETTES["intel"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
GOLD = hexc("#FFD24A")
RED = hexc("#FF3B3B")
CYAN = hexc("#38E1FF")
HUD = hexc("#7FD6B8")
WHITE = (1.0, 1.0, 1.0)
FIRE = hexc("#FF6A1A")
OLIVE = hexc("#4B5A2E")
OLIVE_DK = hexc("#323D1E")
KHAKI = hexc("#6E7A45")
SKIN = hexc("#B9825A")
SKIN_DK = hexc("#8E5E3D")
BOOT = hexc("#17140F")
GROUND = 1128           # feet line; caption band starts at lego.CAP_TOP = 1150

SOURCES = [
    "PIB / Ministry of Defence - Operation Sindoor press briefings, 7-10 May 2025 "
    "(8-9 May: Pakistan attempted 300-400 drone intrusions at 36 locations; most neutralised)",
    "PIB / Ministry of Defence, May 2025 - 'Akashteer': indigenous automated Air Defence Control & Reporting "
    "System of the Army Air Defence, integrates radars & sensors into one real-time air picture",
    "Bharat Electronics Limited (BEL) - Akashteer project for Army Air Defence (contract, March 2023)",
    "Indian Army - Akash SAM and L-70 / ZU-23 / Shilka guns used in the counter-drone grid, May 2025",
]

SPEC = [
    # 00:00-00:03 shock hook (zero backstory)
    {"key": "swarm_hook", "accent": RED, "text": "",
     "visual": "Night city skyline, moon, stars; jawan on the ground looks up and steps back trembling as a red-blinking "
               "drone swarm pours in from the top-left",
     "vo": [("hook", [("पिछले साल मई,", "PICHHLE SAAL MAY,"),
                      ("एक ही रात,", "EK HI RAAT,"),
                      ("चार सौ तक ड्रोन!", "400 TAK DRONE!")])]},

    # 00:03-00:08 conflict
    {"key": "sky_full", "accent": SAFFRON, "text": "",
     "visual": "Swarm fills the sky; jawan (left) points up, commander (right) scans with binoculars; red alarm glow "
               "pulses on the horizon",
     "vo": [("build", [("ऑपरेशन सिंदूर के जवाब में", "OPERATION SINDOOR KE JAWAB MEIN"),
                       ("पाकिस्तान ने", "PAKISTAN NE"),
                       ("भारत का आसमान भर दिया।", "BHARAT KA AASMAAN BHAR DIYA.")])]},

    # 00:08-00:14 reveal - the network
    {"key": "akashteer_net", "accent": GOLD, "text": "",
     "visual": "Radar towers on three hills light up one by one; glowing data links converge into a command vehicle; "
               "operator at the console screen full of tracks, commander points at it; golden pulse on AKASHTEER",
     "vo": [("punch", [("पर भारत के पास था आकाशतीर,", "PAR BHARAT KE PAAS THA AKASHTEER,"),
                       ("जो रडारों को जोड़कर", "JO RADARON KO JODKAR"),
                       ("पूरा आसमान", "POORA AASMAAN"),
                       ("एक स्क्रीन पर ले आता है।", "EK SCREEN PAR LE AATA HAI.")])]},

    # 00:14-00:19 anti-drop: immediate impact, no lecture (rule 12)
    {"key": "intercept", "accent": FIRE, "text": "",
     "visual": "Akash launcher fires on NISHANA, missiles track their real flight angle into drones, L-70 tracers "
               "climb, mid-air bursts with screen shake on DHER; jawan fist-pumps",
     "vo": [("build", [("दुश्मन दिखा,", "DUSHMAN DIKHA,"),
                       ("निशाना बँटा,", "NISHANA BANTA,"),
                       ("और ज़्यादातर ड्रोन", "AUR ZYADATAR DRONE"),
                       ("हवा में ही ढेर!", "HAWA MEIN HI DHER!")])]},

    # 00:19-00:23 twist + grammatical loop back into "पिछले साल मई..."
    {"key": "kavach_loop", "accent": INDIA_GREEN, "text": "",
     "visual": "A golden shield dome glows over the sleeping city, jawan and commander salute; at the end the dome "
               "fades and the first drones re-appear top-left exactly like scene 1 (seamless replay loop)",
     "vo": [("low", [("ये है भारत का अदृश्य कवच,", "YEH HAI BHARAT KA ADRISHYA KAVACH,"),
                     ("जिसकी असली परीक्षा हुई थी...", "JISKI ASLI PAREEKSHA HUI THI...")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "MAY": SAFFRON, "RAAT": CYAN, "400": RED, "DRONE": RED,
    "OPERATION": SAFFRON, "SINDOOR": SAFFRON, "PAKISTAN": RED, "AASMAAN": CYAN,
    "BHARAT": SAFFRON, "AKASHTEER": GOLD, "RADARON": HUD, "JODKAR": HUD, "SCREEN": CYAN,
    "DUSHMAN": RED, "NISHANA": FIRE, "ZYADATAR": GOLD, "DHER": FIRE,
    "ADRISHYA": GOLD, "KAVACH": GOLD, "ASLI": SAFFRON, "PAREEKSHA": SAFFRON,
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".—,?!")] = HOT[_k]


# ============================================================ small helpers

def ell(ctx, x, y, rx, ry):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(max(rx, 0.01), max(ry, 0.01))
    ctx.arc(0, 0, 1.0, 0, 2 * math.pi)
    ctx.restore()


def poly(ctx, pts, c, a=1.0):
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    rgba(ctx, c, a)
    ctx.fill()


def seg01(t, t0, t1):
    """0 before t0, 1 after t1, eased in between."""
    return ease_in_out(clamp((t - t0) / max(t1 - t0, 1e-3)))


# ============================================================ world: night sky, city, hills

def night_world(ctx, t, alarm=0.0, dawn=0.0, city=True):
    """Layered night: multi-stop sky, moon + glow, twinkling stars, three hill ranges, a lit city skyline,
    a peepal tree, grass and drifting dust. alarm adds a red horizon pulse, dawn warms the sky (loop scene)."""
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    g.add_color_stop_rgb(0.00, 0.012, 0.020, 0.060)
    g.add_color_stop_rgb(0.35, 0.040, 0.050, 0.140 + 0.05 * dawn)
    g.add_color_stop_rgb(0.70, 0.120 + 0.20 * dawn, 0.080 + 0.08 * dawn, 0.200)
    g.add_color_stop_rgb(1.00, 0.330 + 0.35 * dawn, 0.170 + 0.15 * dawn, 0.160)
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()

    for i in range(90):   # stars
        sx, sy = rnd(i, 11) * W, 180 + rnd(i, 12) * 560
        tw = 0.35 + 0.65 * abs(math.sin(t * (0.8 + rnd(i, 13) * 2.2) + i))
        circle(ctx, sx, sy, 0.8 + 1.8 * rnd(i, 14), WHITE, 0.55 * tw * (1 - 0.6 * dawn))

    glow(ctx, 830, 330, 230, hexc("#9FC4FF"), 0.30)   # moon
    circle(ctx, 830, 330, 54, hexc("#F3F0E2"), 0.95)
    circle(ctx, 848, 318, 12, hexc("#D9D4C0"), 0.6)
    circle(ctx, 812, 346, 8, hexc("#D9D4C0"), 0.5)

    if alarm > 0:
        pulse = 0.55 + 0.45 * math.sin(t * 7.0)
        glow(ctx, 540, GROUND - 120, 820, RED, 0.28 * alarm * pulse)

    glow(ctx, 540, GROUND - 60, 700, hexc("#FFB060"), 0.18 + 0.12 * dawn)   # city light dome

    ranges = [(820, 0.006, 70, hexc("#1A1F3A")), (900, 0.009, 55, hexc("#141830")), (980, 0.013, 40, hexc("#0E1124"))]
    for k, (base, f, amp, col) in enumerate(ranges):
        ctx.move_to(0, GROUND)
        for x in range(0, W + 20, 20):
            ctx.line_to(x, base + amp * math.sin(x * f + k * 1.7) + 0.4 * amp * math.sin(x * f * 2.6 + k))
        ctx.line_to(W, GROUND)
        ctx.close_path()
        rgba(ctx, col)
        ctx.fill()

    if city:
        x = -10
        i = 0
        while x < W + 10:
            bw = 50 + 70 * rnd(i, 21)
            bh = 70 + 190 * rnd(i, 22)
            top = GROUND - 40 - bh
            rgba(ctx, hexc("#0A0C18"))
            ctx.rectangle(x, top, bw, bh + 40)
            ctx.fill()
            for wy in range(int(top) + 14, GROUND - 50, 22):
                for wx in range(int(x) + 8, int(x + bw) - 10, 16):
                    if rnd(wx * 0.37 + wy, 23) > 0.55:
                        flick = 0.65 + 0.35 * math.sin(t * 2 + wx + wy)
                        rgba(ctx, hexc("#FFD27A"), 0.55 * flick)
                        ctx.rectangle(wx, wy, 7, 10)
                        ctx.fill()
            x += bw + 6
            i += 1

    peepal(ctx, 70, GROUND, 1.0, t)

    g2 = cairo.LinearGradient(0, GROUND - 30, 0, lego.CAP_TOP + 80)   # ground + grass
    g2.add_color_stop_rgb(0, 0.06, 0.08, 0.05)
    g2.add_color_stop_rgb(1, 0.02, 0.03, 0.02)
    ctx.set_source(g2)
    ctx.rectangle(0, GROUND - 30, W, H - GROUND + 30)
    ctx.fill()
    for i in range(70):
        gx = rnd(i, 31) * W
        sway = 4 * math.sin(t * 1.6 + i)
        line(ctx, [(gx, GROUND - 26), (gx + sway, GROUND - 46 - 22 * rnd(i, 32))], hexc("#1E2E16"), 3, 0.9)

    for i in range(26):   # dust / smoke motes
        mx = (rnd(i, 41) * W + t * (10 + 18 * rnd(i, 42))) % W
        my = (240 + rnd(i, 43) * 820 - t * (8 + 14 * rnd(i, 44))) % 900 + 220
        circle(ctx, mx, my, 1.5 + 2.5 * rnd(i, 45), hexc("#FFE6B0"), 0.06 + 0.08 * rnd(i, 46))


def peepal(ctx, x, y, s, t):
    """Silhouetted peepal tree at the screen edge (depth layer)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    poly(ctx, [(-14, 0), (14, 0), (8, -170), (30, -260), (18, -262), (0, -190), (-20, -250), (-30, -246), (-8, -170)],
         hexc("#07080F"))
    for i in range(16):
        lx = -90 + 180 * rnd(i, 51) + 4 * math.sin(t * 1.2 + i)
        ly = -330 + 140 * rnd(i, 52)
        ell(ctx, lx, ly, 60 + 30 * rnd(i, 53), 40 + 20 * rnd(i, 54))
        rgba(ctx, hexc("#06070D"))
        ctx.fill()
    ctx.restore()


# ============================================================ drones

def drone(ctx, x, y, s, t, ang=0.0, seed=0, hit=0.0):
    """Small fixed-wing loitering drone, nose along ang, blinking red nav light."""
    if hit >= 1.0:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(s, s)
    a = 1.0 - hit
    glow(ctx, 0, 0, 60, hexc("#FF5A3C"), 0.16 * a)   # city-light rim so the swarm reads against the night
    shape = [(34, 0), (6, -6), (-4, -34), (-14, -34), (-10, -6), (-26, -4), (-34, -16), (-38, -16), (-34, 0),
             (-38, 16), (-34, 16), (-26, 4), (-10, 6), (-14, 34), (-4, 34), (6, 6)]
    poly(ctx, shape, hexc("#5C636E"), a)
    ctx.move_to(*shape[0])
    for p in shape[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    rgba(ctx, hexc("#C9D2DC"), 0.55 * a)
    ctx.set_line_width(2)
    ctx.stroke()
    line(ctx, [(30, 0), (-30, 0)], hexc("#2A2D33"), 3, 0.8 * a)
    blink = 1.0 if int(t * 4 + seed) % 2 == 0 else 0.3
    circle(ctx, -6, -30, 4.5, RED, blink * a)
    circle(ctx, -6, 30, 4.5, hexc("#3CFF6A"), blink * a)
    glow(ctx, -6, -30, 22, RED, 0.6 * blink * a)
    ctx.restore()


def swarm_pos(i, t, enter=0.0):
    """Drone i of the swarm: comes from the upper-left, drifts right/down; enter staggers arrivals."""
    lane_y = 230 + rnd(i, 61) * 560
    speed = 70 + 70 * rnd(i, 62)
    start = -120 - rnd(i, 63) * 900
    x = (start + (t - enter) * speed * 2.2 + 140 + 1100) % (W + 1200) - 1100   # wraps: the sky never empties
    y = lane_y + 0.22 * (x + 120) * (0.3 + 0.4 * rnd(i, 64)) * 0.3 + 10 * math.sin(t * 2 + i)
    return x, y, math.atan2(0.066 * (0.3 + 0.4 * rnd(i, 64)), 1.0)


def swarm(ctx, t, n, enter=0.0, scale=0.75, hit_fn=None):
    for i in range(n):
        x, y, ang = swarm_pos(i, t, enter)
        if -80 < x < W + 80:
            hit = hit_fn(i, x, y) if hit_fn else 0.0
            drone(ctx, x, y, scale * (0.65 + 0.5 * rnd(i, 65)), t, ang, i, hit)


# ============================================================ characters (jawan / commander)

def limb(ctx, x0, y0, a1, l1, a2, l2, c, w):
    """Two-segment limb from (x0, y0): upper at angle a1, lower at a1 + a2 (radians, 0 = pointing down)."""
    x1, y1 = x0 + l1 * math.sin(a1), y0 + l1 * math.cos(a1)
    x2, y2 = x1 + l2 * math.sin(a1 + a2), y1 + l2 * math.cos(a1 + a2)
    line(ctx, [(x0, y0), (x1, y1)], c, w)
    line(ctx, [(x1, y1), (x2, y2)], c, w * 0.9)
    return x2, y2


ARM_POSES = {   # (right upper, right fore, left upper, left fore) - angles from straight down, + = forward/up
    "stand":   (0.18, 0.10, -0.18, -0.10),
    "look_up": (0.45, 1.20, -0.30, -1.30),   # hands half up, startled
    "point":   (2.55, 0.15, -0.20, -0.25),
    "binocs":  (1.35, 1.75, 1.15, 1.95),
    "operate": (1.05, 0.55, 0.95, 0.60),
    "fist":    (2.70, 0.70, -0.20, -0.30),
    "salute":  (1.95, 2.25, -0.15, -0.10),
    "brief":   (1.70, 0.35, -0.25, -0.30),   # arm out at the console screen
}


def soldier(ctx, x, y, s, t, pose="stand", flip=False, commander=False, a=1.0):
    """Indian Army jawan (helmet) or commander (beret, rank tabs), feet at (x, y), ~560 units tall.
    Every save() here is matched by the restore() at the end (AGENTS.md rule 6)."""
    ctx.save()
    tremble = 2.5 * math.sin(t * 38) if pose == "look_up" else 0.0
    ctx.translate(x + tremble, y)
    ctx.scale(-s if flip else s, s)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)

    ell(ctx, 0, 6, 82, 14)
    rgba(ctx, (0, 0, 0), 0.5 * a)
    ctx.fill()

    stride = 16 if pose == "look_up" else 0
    for side in (-1, 1):   # legs + boots
        fx = side * 30 - (stride if side < 0 else 0)
        line(ctx, [(side * 22, -230), (fx, -20)], OLIVE_DK, 40, a)
        rrect(ctx, fx - 20, -26, 44, 26, 8)
        rgba(ctx, BOOT, a)
        ctx.fill()

    smooth_torso = [(-62, -430), (62, -430), (54, -225), (-54, -225)]
    poly(ctx, smooth_torso, OLIVE, a)
    for k in range(9):   # camo blotches
        ell(ctx, -45 + 90 * rnd(k, 71 + commander), -410 + 170 * rnd(k, 72), 14, 9)
        rgba(ctx, KHAKI if k % 2 else OLIVE_DK, 0.7 * a)
        ctx.fill()
    rrect(ctx, -58, -250, 116, 22, 5)   # belt
    rgba(ctx, hexc("#1F1A12"), a)
    ctx.fill()
    if not commander:   # webbing / vest pouches
        for px in (-36, 0, 36):
            rrect(ctx, px - 14, -330, 28, 34, 5)
            rgba(ctx, OLIVE_DK, a)
            ctx.fill()
    else:               # rank tabs + lanyard
        for sx in (-46, 46):
            rrect(ctx, sx - 14, -432, 28, 12, 3)
            rgba(ctx, GOLD, a)
            ctx.fill()
        line(ctx, [(-40, -420), (-20, -360), (10, -350)], hexc("#C9A23A"), 3, a)

    ra1, ra2, la1, la2 = ARM_POSES.get(pose, ARM_POSES["stand"])
    if pose == "fist":
        ra2 += 0.25 * math.sin(t * 9)
    if pose == "point":
        ra1 += 0.06 * math.sin(t * 3)
    # far arm first (left), then near arm (right) over the torso
    lx, ly = limb(ctx, -58, -415, -la1, 105, -la2, 98, OLIVE_DK, 30)
    circle(ctx, lx, ly, 15, SKIN_DK, a)
    rx, ry = limb(ctx, 58, -415, ra1, 105, ra2, 98, OLIVE, 32)
    circle(ctx, rx, ry, 16, SKIN, a)

    line(ctx, [(0, -430), (0, -458)], SKIN_DK, 26, a)   # neck
    ctx.save()
    tilt = -0.32 if pose in ("look_up", "point") else (-0.12 if pose == "binocs" else 0.0)
    ctx.translate(0, -470)
    ctx.rotate(tilt)
    ell(ctx, 0, -38, 46, 52)
    rgba(ctx, SKIN, a)
    ctx.fill()
    circle(ctx, 44, -36, 9, SKIN_DK, a)   # ear
    if pose == "binocs":
        rrect(ctx, 10, -58, 56, 30, 8)
        rgba(ctx, hexc("#111111"), a)
        ctx.fill()
        circle(ctx, 64, -50, 9, CYAN, 0.6 * a)
    else:
        blink = 0.15 if (t % 3.1) < 0.12 else 1.0
        wide = 1.6 if pose == "look_up" else 1.0
        for ex in (14, 34):
            ell(ctx, ex, -44, 5, 5 * wide * blink)
            rgba(ctx, (0.05, 0.04, 0.04), a)
            ctx.fill()
        line(ctx, [(4, -64), (22, -68)], (0.12, 0.08, 0.06), 4, a)   # brow
        line(ctx, [(26, -68), (42, -64)], (0.12, 0.08, 0.06), 4, a)
    if not commander:
        line(ctx, [(-6, -30), (34, -24)], (0.15, 0.1, 0.08), 5, a)   # moustache
    mouth = {"look_up": 9, "fist": 10, "point": 7}.get(pose, 0)
    if mouth:
        ell(ctx, 22, -12, 9, mouth)
        rgba(ctx, (0.25, 0.05, 0.05), a)
        ctx.fill()
    else:
        line(ctx, [(12, -12), (30, -12)], (0.3, 0.12, 0.1), 3, a)
    if commander:   # beret
        ell(ctx, -6, -86, 56, 22)
        rgba(ctx, hexc("#2F3A1A"), a)
        ctx.fill()
        circle(ctx, 22, -88, 7, GOLD, a)
    else:           # combat helmet with net
        ctx.move_to(-56, -60)
        ctx.curve_to(-56, -128, 58, -128, 60, -58)
        ctx.close_path()
        rgba(ctx, hexc("#3E4A26"), a)
        ctx.fill()
        for k in range(5):
            line(ctx, [(-44 + k * 22, -104), (-50 + k * 24, -62)], hexc("#2B3419"), 2, 0.8 * a)
        line(ctx, [(-58, -60), (62, -58)], hexc("#2B3419"), 6, a)
    ctx.restore()
    ctx.restore()


# ============================================================ hardware

def radar_tower(ctx, x, y, s, t, lit=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for k in range(6):   # lattice mast
        y0, y1 = -k * 40, -(k + 1) * 40
        line(ctx, [(-22 + k * 2, y0), (22 - k * 2, y1)], hexc("#3A4250"), 3)
        line(ctx, [(22 - k * 2, y0), (-22 + k * 2, y1)], hexc("#3A4250"), 3)
    line(ctx, [(-24, 0), (-10, -240)], hexc("#4A5363"), 5)
    line(ctx, [(24, 0), (10, -240)], hexc("#4A5363"), 5)
    sweep = math.cos(t * 2.6 + x)
    ell(ctx, 0, -262, 52 * abs(sweep) + 6, 30)
    rgba(ctx, hexc("#8C97A8"))
    ctx.fill()
    line(ctx, [(0, -262), (40 * sweep, -262)], hexc("#D7E0EA"), 3)
    if lit > 0:
        glow(ctx, 0, -262, 120, HUD, 0.45 * lit)
        for k in range(3):   # emitted rings
            r = ((t * 120 + k * 60) % 180)
            ctx.arc(0, -262, r, 0, math.tau)
            rgba(ctx, HUD, 0.35 * lit * (1 - r / 180))
            ctx.set_line_width(2)
            ctx.stroke()
    ctx.restore()


def command_vehicle(ctx, x, y, s, t, glow_a=1.0):
    """Mobile shelter truck with an antenna mast (the Akashteer node)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -170, -150, 250, 120, 10)   # shelter box
    rgba(ctx, hexc("#3F4A2A"))
    ctx.fill()
    rrect(ctx, 80, -110, 90, 80, 10)       # cab
    rgba(ctx, hexc("#4B5732"))
    ctx.fill()
    rrect(ctx, 110, -100, 46, 30, 5)
    rgba(ctx, CYAN, 0.35)
    ctx.fill()
    for wx in (-120, -30, 120):
        circle(ctx, wx, -22, 26, hexc("#111111"))
        circle(ctx, wx, -22, 10, hexc("#555555"))
    line(ctx, [(-40, -150), (-40, -300)], hexc("#6B7480"), 5)
    line(ctx, [(-70, -280), (-10, -280)], hexc("#6B7480"), 4)
    glow(ctx, -40, -300, 90 * glow_a + 10, GOLD, 0.55 * glow_a)
    circle(ctx, -40, -300, 8, GOLD, 0.9)
    ctx.restore()


def console_screen(ctx, cx, cy, r, t, tracks=1.0, locked=0.0):
    """The air picture: radar disc with many drone tracks (dots + vectors), no text."""
    circle(ctx, cx, cy, r + 16, hexc("#0B1112"))
    circle(ctx, cx, cy, r, hexc("#02130F"))
    for k in (1.0, 0.66, 0.33):
        ctx.arc(cx, cy, r * k, 0, math.tau)
        rgba(ctx, HUD, 0.35)
        ctx.set_line_width(2)
        ctx.stroke()
    ang = t * 2.4
    for k in range(14):
        a0 = ang - k * 0.06
        ctx.move_to(cx, cy)
        ctx.arc(cx, cy, r, a0 - 0.06, a0)
        ctx.close_path()
        rgba(ctx, HUD, 0.4 * (1 - k / 14))
        ctx.fill()
    n = int(40 * tracks)
    for i in range(n):
        rr = r * (0.25 + 0.7 * rnd(i, 81))
        aa = -math.pi * (0.15 + 0.7 * rnd(i, 82)) + 0.05 * t
        px, py = cx + rr * math.cos(aa), cy + rr * math.sin(aa)
        is_locked = rnd(i, 83) < locked
        col = GOLD if is_locked else RED
        circle(ctx, px, py, 5, col, 0.95)
        line(ctx, [(px, py), (px + 14 * math.cos(aa + 2.6), py + 14 * math.sin(aa + 2.6))], col, 2, 0.7)
        if is_locked:
            ctx.rectangle(px - 11, py - 11, 22, 22)
            rgba(ctx, GOLD, 0.9)
            ctx.set_line_width(2)
            ctx.stroke()


def akash_launcher(ctx, x, y, s, t, loaded=(True, True, True)):
    """Akash tracked launcher, three missiles on a rail raised to ~40 degrees, pointing right/up."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -150, -70, 300, 60, 18)   # hull
    rgba(ctx, hexc("#45512C"))
    ctx.fill()
    for k in range(6):
        circle(ctx, -125 + k * 50, -18, 20, hexc("#121212"))
    ctx.save()
    ctx.translate(-30, -80)
    ctx.rotate(-0.70)
    rrect(ctx, -20, -36, 240, 72, 8)
    rgba(ctx, hexc("#56623A"))
    ctx.fill()
    for k, ok in enumerate(loaded):
        if ok:
            my = -24 + k * 24
            rrect(ctx, 0, my - 9, 230, 18, 9)
            rgba(ctx, hexc("#E8E6DA"))
            ctx.fill()
            poly(ctx, [(230, my - 9), (262, my), (230, my + 9)], hexc("#C83A2A"))
    ctx.restore()
    ctx.restore()


def missile(ctx, x, y, ang, s=1.0, a=1.0):
    """Interceptor in flight; ang is its true flight angle (atan2), nose leads, flame trails (rule 7)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(s, s)
    g = cairo.RadialGradient(-46, 0, 2, -70, 0, 46)
    g.add_color_stop_rgba(0, 1, 0.95, 0.6, 0.95 * a)
    g.add_color_stop_rgba(0.4, 1, 0.45, 0.05, 0.8 * a)
    g.add_color_stop_rgba(1, 0.3, 0.05, 0, 0)
    ctx.set_source(g)
    ctx.arc(-58, 0, 46, 0, math.tau)
    ctx.fill()
    rrect(ctx, -40, -8, 80, 16, 8)
    rgba(ctx, hexc("#EEEDE4"), a)
    ctx.fill()
    poly(ctx, [(40, -8), (62, 0), (40, 8)], hexc("#C83A2A"), a)
    poly(ctx, [(-36, -8), (-48, -20), (-24, -8)], hexc("#9AA0A6"), a)
    poly(ctx, [(-36, 8), (-48, 20), (-24, 8)], hexc("#9AA0A6"), a)
    ctx.restore()


def burst(ctx, x, y, u, r=150):
    """Mid-air intercept fireball, u in 0..1."""
    if not 0 < u < 1:
        return
    rr = r * ease_out_cubic(u)
    fade = 1 - u
    g = cairo.RadialGradient(x, y, 4, x, y, rr)
    g.add_color_stop_rgba(0, 1, 1, 0.85, 0.95 * fade)
    g.add_color_stop_rgba(0.3, 1, 0.6, 0.1, 0.85 * fade)
    g.add_color_stop_rgba(0.75, 0.75, 0.15, 0.02, 0.45 * fade)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g)
    ctx.arc(x, y, rr, 0, math.tau)
    ctx.fill()
    for k in range(10):   # sparks
        aa = k * math.tau / 10 + x
        d = rr * (0.8 + 0.5 * rnd(k, x))
        circle(ctx, x + d * math.cos(aa), y + d * math.sin(aa) + 60 * u * u, 4 * fade, GOLD, fade)


def gun_tracers(ctx, x0, y0, ang, t, length=900):
    for k in range(10):
        off = (t * 1500 + k * 90) % length
        bx, by = x0 + off * math.cos(ang), y0 + off * math.sin(ang)
        tx, ty = bx + 30 * math.cos(ang), by + 30 * math.sin(ang)
        line(ctx, [(bx, by), (tx, ty)], FIRE, 5, 0.85)
        line(ctx, [(bx, by), (tx, ty)], hexc("#FFF3A0"), 2, 0.95)


def l70_gun(ctx, x, y, s, t, firing=False, ang=-1.05):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    poly(ctx, [(-70, 0), (70, 0), (50, -50), (-50, -50)], hexc("#3E4828"))
    rrect(ctx, -40, -100, 80, 54, 10)
    rgba(ctx, hexc("#4F5B33"))
    ctx.fill()
    ctx.save()
    ctx.translate(0, -80)
    ctx.rotate(ang)
    rrect(ctx, 0, -7, 170, 14, 5)
    rgba(ctx, hexc("#2A2F22"))
    ctx.fill()
    if firing and int(t * 20) % 2 == 0:
        glow(ctx, 180, 0, 50, FIRE, 0.9)
        circle(ctx, 178, 0, 10, WHITE, 0.95)
    ctx.restore()
    ctx.restore()


def shield_dome(ctx, u, t):
    """Golden 'adrishya kavach' dome over the city; u = 0..1 strength."""
    if u <= 0:
        return
    cx, cy, rx, ry = 540, GROUND, 620, 560
    g = cairo.RadialGradient(cx, cy, 80, cx, cy, rx)
    g.add_color_stop_rgba(0, 1, 0.85, 0.35, 0.0)
    g.add_color_stop_rgba(0.85, 1, 0.80, 0.30, 0.10 * u)
    g.add_color_stop_rgba(1, 1, 0.85, 0.40, 0.40 * u)
    ctx.save()
    ctx.rectangle(0, 0, W, cy)
    ctx.clip()
    ctx.set_source(g)
    ell(ctx, cx, cy, rx, ry)
    ctx.fill()
    for k in range(7):   # hex shimmer lines
        yy = cy - ry * (k + 1) / 8
        half = rx * math.sqrt(max(0.0, 1 - ((cy - yy) / ry) ** 2))
        line(ctx, [(cx - half, yy), (cx + half, yy)], GOLD, 1.5, 0.18 * u * (0.6 + 0.4 * math.sin(t * 3 + k)))
    ell(ctx, cx, cy, rx, ry)
    rgba(ctx, GOLD, 0.65 * u)
    ctx.set_line_width(4)
    ctx.stroke()
    ctx.restore()


# ============================================================ scenes

class SwarmHookScene(Cued):
    """00:00-00:03 - jawan looks up as the swarm pours in. Opens mid-action (same frame the loop ends on)."""
    def beats(self, d):
        c = self.cue
        return {"raat": c("RAAT", d * 0.35), "drone": c("DRONE", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "whoosh"), (b["raat"], "tick"), (b["drone"], "alarm")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_world(ctx, t, alarm=seg01(t, b["drone"], b["drone"] + 0.4))
        n = int(lerp(14, 40, seg01(t, 0, b["drone"] + 0.3)))
        swarm(ctx, t + 3.0, n, scale=1.15)
        soldier(ctx, 300, GROUND, 0.76, t, pose="look_up" if t > b["raat"] * 0.6 else "stand")


class SkyFullScene(Cued):
    """00:03-00:08 - jawan points, commander scans with binoculars; the sky is full."""
    def beats(self, d):
        c = self.cue
        return {"sindoor": c("SINDOOR", d * 0.2), "pak": c("PAKISTAN", d * 0.45), "bhar": c("BHAR", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(b["sindoor"], "whoosh"), (b["pak"], "alarm"), (b["bhar"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_world(ctx, t, alarm=0.6 + 0.4 * seg01(t, b["pak"], b["pak"] + 0.5))
        n = int(lerp(34, 70, seg01(t, b["pak"], b["bhar"] + 0.3)))
        swarm(ctx, t + 6.0, n, scale=1.0)
        soldier(ctx, 240, GROUND, 0.74, t, pose="point")
        soldier(ctx, 820, GROUND, 0.78, t, pose="binocs", flip=True, commander=True)


class AkashteerNetScene(Cued):
    """00:08-00:14 - towers light up, links converge into the vehicle, the whole sky on one screen."""
    def beats(self, d):
        c = self.cue
        return {"akash": c("AKASHTEER", d * 0.18), "jod": c("JODKAR", d * 0.4),
                "screen": c("SCREEN", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(b["akash"], "shimmer"), (b["jod"], "beep"), (b["jod"] + 0.35, "beep"),
                (b["jod"] + 0.7, "beep"), (b["screen"], "zap")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_world(ctx, t, alarm=0.25, city=False)
        swarm(ctx, t + 9.0, 40, scale=0.75)
        reveal = seg01(t, b["akash"], b["akash"] + 0.5)
        if reveal > 0:   # golden pulse on the name
            u = clamp((t - b["akash"]) / 0.9)
            if u < 1:
                ctx.arc(540, 820, 900 * ease_out_cubic(u), 0, math.tau)
                rgba(ctx, GOLD, 0.45 * (1 - u))
                ctx.set_line_width(14)
                ctx.stroke()
        hub = (430, GROUND - 120 - 300 * 0.9)
        towers = [(140, 930), (520, 900), (930, 950)]
        for k, (tx, ty) in enumerate(towers):
            lit = seg01(t, b["jod"] + 0.35 * k, b["jod"] + 0.35 * k + 0.3)
            radar_tower(ctx, tx, ty, 0.62, t, lit)
            if lit > 0:   # data link flowing into the vehicle
                sx, sy = tx, ty - 262 * 0.62
                ex, ey = hub
                line(ctx, [(sx, sy), (ex, ey)], HUD, 3, 0.6 * lit)
                for p in range(4):
                    u = ((t * 0.9 + p / 4) % 1.0)
                    circle(ctx, lerp(sx, ex, u), lerp(sy, ey, u), 6, GOLD, 0.9 * lit)
        command_vehicle(ctx, 470, GROUND - 120, 0.9, t, glow_a=reveal)
        on = seg01(t, b["screen"] - 0.2, b["screen"] + 0.3)
        console_screen(ctx, 780, 560, 150 + 20 * on, t, tracks=0.35 + 0.65 * on)
        soldier(ctx, 250, GROUND, 0.70, t, pose="operate")
        soldier(ctx, 850, GROUND, 0.76, t, pose="brief", flip=True, commander=True)


class InterceptScene(Cued):
    """00:14-00:19 - immediate impact: Akash launch, gun tracers, bursts, shake, fist pump."""
    TARGETS = [(760, 420), (560, 300), (900, 560), (380, 470), (690, 650)]

    def beats(self, d):
        c = self.cue
        return {"dikha": c("DIKHA", d * 0.1), "nishana": c("NISHANA", d * 0.3),
                "drone": c("ZYADATAR", d * 0.55), "dher": c("DHER", d * 0.82)}

    def events(self, d):
        b = self.beats(d)
        ev = [(b["dikha"], "beep"), (b["nishana"], "whoosh"), (b["nishana"] + 0.25, "whoosh")]
        for k in range(len(self.TARGETS)):
            ev.append((self.hit_time(b, k), "boom"))
        return ev

    def hit_time(self, b, k):
        return b["nishana"] + 0.55 + k * (b["dher"] + 0.2 - b["nishana"] - 0.55) / (len(self.TARGETS) - 1)

    def draw(self, ctx, t, d):
        b = self.beats(d)
        shake = 0.0
        for k in range(len(self.TARGETS)):
            u = t - self.hit_time(b, k)
            if 0 < u < 0.3:
                shake = max(shake, 14 * (1 - u / 0.3))
        ctx.save()
        ctx.translate(shake * math.sin(t * 90), shake * math.cos(t * 77))
        night_world(ctx, t, alarm=0.45)
        swarm(ctx, t + 12.0, 26, scale=0.8)

        lx, ly = 230, GROUND - 10
        mouth = (lx - 30 + 0.75 * 262 * math.cos(-0.70) * 0.95, ly - 80 * 0.75 - 0.75 * 262 * math.sin(0.70))
        fired = sum(t >= b["nishana"] + 0.25 * k for k in range(3))
        akash_launcher(ctx, lx, ly, 0.75, t, loaded=tuple(k >= fired for k in range(3)))
        for k, (tx, ty) in enumerate(self.TARGETS):
            hit = self.hit_time(b, k)
            launch = hit - 0.7
            if t < launch:
                drone(ctx, tx + 25 * math.sin(t * 2 + k), ty, 1.15, t, 0.06, k)
            elif t < hit:
                drone(ctx, tx + 25 * math.sin(t * 2 + k), ty, 1.15, t, 0.06, k)
                u = (t - launch) / 0.7
                # curved pursuit path; heading = true flight angle of the path (rule 7)
                p0, p2 = mouth, (tx, ty)
                p1 = (lerp(p0[0], p2[0], 0.3), min(p0[1], p2[1]) - 120)
                px = (1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0]
                py = (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]
                dx = 2 * (1 - u) * (p1[0] - p0[0]) + 2 * u * (p2[0] - p1[0])
                dy = 2 * (1 - u) * (p1[1] - p0[1]) + 2 * u * (p2[1] - p1[1])
                for s_ in range(1, 7):   # smoke trail
                    v = max(0.0, u - s_ * 0.05)
                    sx = (1 - v) ** 2 * p0[0] + 2 * (1 - v) * v * p1[0] + v * v * p2[0]
                    sy = (1 - v) ** 2 * p0[1] + 2 * (1 - v) * v * p1[1] + v * v * p2[1]
                    circle(ctx, sx, sy, 8 + s_ * 2, hexc("#C9C3B8"), 0.25 - s_ * 0.03)
                missile(ctx, px, py, math.atan2(dy, dx), 0.7)
            burst(ctx, tx, ty, (t - hit) / 0.9, 160)

        guns_on = t > b["nishana"]
        l70_gun(ctx, 900, GROUND - 6, 0.8, t, firing=guns_on, ang=-1.95)
        if guns_on:
            gun_tracers(ctx, 900 + 0.8 * 170 * math.cos(-1.95), GROUND - 70 + 0.8 * 170 * math.sin(-1.95), -1.95, t)
        pose = "fist" if t > b["dher"] - 0.1 else ("point" if t > b["dikha"] else "stand")
        soldier(ctx, 560, GROUND, 0.72, t, pose=pose)
        ctx.restore()


class KavachLoopScene(Cued):
    """00:19-00:23 - golden dome, salute; then the dome fades and the first drones return (loop to scene 1)."""
    def beats(self, d):
        c = self.cue
        return {"kavach": c("KAVACH", d * 0.3), "pareeksha": c("PAREEKSHA", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["kavach"], "shimmer"), (b["pareeksha"], "tick"), (d - 0.35, "whoosh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        back = seg01(t, d - 0.9, d - 0.1)   # fade back into the opening frame
        night_world(ctx, t, dawn=0.5 * (1 - back), alarm=0.0)
        dome = seg01(t, b["kavach"] - 0.2, b["kavach"] + 0.5) * (1 - back)
        shield_dome(ctx, dome, t)
        if back > 0:
            swarm(ctx, 3.0 + (t - (d - 0.9)), int(14 * back) + 1, scale=1.15)
        salute = dome > 0.3
        soldier(ctx, 300 if back > 0.5 else 250, GROUND, 0.76 if back > 0.5 else 0.74, t,
                pose="salute" if salute else ("look_up" if back > 0.5 else "stand"))
        if back < 0.5:
            soldier(ctx, 820, GROUND, 0.78, t, pose="salute" if salute else "stand", flip=True, commander=True)


SCENE_CLASSES = {
    "swarm_hook": SwarmHookScene,
    "sky_full": SkyFullScene,
    "akashteer_net": AkashteerNetScene,
    "intercept": InterceptScene,
    "kavach_loop": KavachLoopScene,
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
        "Ek Raat, 400 Drone! Akashteer Ne Kaise Roka? 🇮🇳 #shorts",
        "Operation Sindoor Ki Raat: 400 Drone vs Akashteer #shorts",
        "Pakistan Ke 400 Drone Aur Bharat Ka Adrishya Kavach #shorts",
        "Akashteer: Jis Network Ne Pura Aasmaan Ek Screen Par La Diya #shorts",
        "400 Drone Ek Raat Mein? Akashteer Ka Sach #shorts",
    ],
    "title": "Ek Raat, 400 Drone! Akashteer Ne Kaise Roka? 🇮🇳 #shorts",
    "thumb_text": "400 DRONE AKASHTEER",
    "queries": ["akashteer", "operation sindoor drone", "akashteer air defence", "400 drone"],
    "description": """Operation Sindoor ke baad, 8-9 May 2025 ki raat Pakistan ne 36 jagahon par 300-400 drone bheje.
Bharat ka jawab: Akashteer - Army Air Defence ka swadeshi network jo radaron ko jodkar poora aasmaan ek screen par le aata hai.

Is Short mein:
• Ek raat, 36 jagah, 300-400 drone (MoD briefing)
• Akashteer kya hai: BEL ka automated air-defence control & reporting system
• Akash missile aur L-70 / ZU-23 guns ne zyadatar drone hawa mein hi gira diye

Sources: PIB / Ministry of Defence briefings (May 2025), BEL.
""",
    "tags": [
        "akashteer", "operation sindoor", "akashteer air defence", "indian army air defence", "drone attack india",
        "akash missile", "bel akashteer", "defence shorts", "reality shift", "jai hind",
    ],
    "hashtags": ["#Shorts", "#Akashteer", "#OperationSindoor"],
    "pinned_comment": "Aapke hisaab se us raat ka asli hero kaun tha - Akashteer network, Akash missile ya L-70 guns? "
                      "Comment mein JAI HIND likhein 🇮🇳",
}


def thumbnail(ctx):
    """High-CTR cover: swarm crashing into the golden dome, jawan looking up, two-line hook."""
    night_world(ctx, 2.0, alarm=0.7)
    shield_dome(ctx, 1.0, 2.0)
    swarm(ctx, 9.0, 60, scale=0.8)
    for k, (bx, by) in enumerate([(380, 640), (700, 600), (560, 720)]):
        burst(ctx, bx, by, 0.35 + 0.1 * k, 170)
    soldier(ctx, 260, GROUND, 0.80, 0.4, pose="look_up")
    soldier(ctx, 830, GROUND, 0.80, 0.4, pose="point", flip=True, commander=True)
    text(ctx, "400 DRONE", 540, 250, 150, RED, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "EK RAAT!", 540, 400, 120, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "AKASHTEER", 540, 1300, 120, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, HUD, a=0.85)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.akashteer")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
