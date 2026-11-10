"""Reality Shift Short — K9 Vajra: 3 shells in 15 seconds, all landing at the same moment (MRSI) (~35s).

Usage:
  python generate_k9_vajra_short.py

New "fire mission" layout (not the speed file, naval-brief map, defence-lab blueprint or intel file): dusk
mountain range with an olive ground band, a crosshair emblem + FIRE MISSION header top-left, a 4-shell mission
counter top-right, captions on a khaki "stencil tape" that squashes in vertically at 1180-1280, a muzzle-flash
cut between scenes, bottom 400px clean. Ends on a 3-gun poll board (K9 VAJRA / DHANUSH / ATAGS) with a target
reticle hopping between rows; no subscribe badge / bell / cursor and no missile-to-comment flight.
Facts (as commonly reported): K9 Vajra-T is a 155 mm / 52-calibre tracked self-propelled howitzer built by L&T at
Hazira under licence from South Korea's Hanwha (K9 Thunder). Burst rate: 3 rounds in ~15 s; it can fire a 3-round
MRSI (multiple rounds simultaneous impact) by changing elevation so all three land together. Range ~40 km with
extended-range ammunition (less with plain HE). First 100 ordered 2017; first sent to the western desert, moved to
eastern Ladakh after 2020; MoD signed for 100 more with L&T in Dec 2024 (~Rs 7,629 crore). Shoot-and-scoot: it fires
and moves off before counter-battery fire arrives (shown schematically, not a timed claim).
"""

import importlib
import json
import math

import cairo
import numpy as np

import engine
from engine import *  # noqa: F401,F403
from generate_brahmos_short import big_readout, chip
from generate_chabahar_short import Cued
from generate_rupee_short import VOICE_TONES
from stories.reality_shift import GOLD, INDIA_GREEN, SAFFRON, stamp

TOPIC = "K9 VAJRA 3 SHELLS IN 15 SECONDS"
OUTPUTS = {"edge": "k9_vajra_short.mp4"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.18
TAIL_PAD = 0.12
TRIM = {"thresh": 0.006, "keep": 0.04, "keep_tail": 0.06}
MUSIC_BPM = 112
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"

RED = hexc("#FF4436")
KHAKI = hexc("#D8C27A")
OLIVE = hexc("#56663A")
OLIVE_D = hexc("#2E3820")
STEEL = hexc("#9AA8B6")
FLAME = hexc("#FFA033")
SNOW = hexc("#E9F1F7")
SAND = hexc("#C99A5B")
SKY_TOP, SKY_BOT = hexc("#120E22"), hexc("#7A3B2A")
MONO = "Consolas"

# each line: (tone, [(spoken Hindi, Hinglish caption), ...], pause after)
SPEC = [
    {"key": "burst", "accent": GOLD, "text": "15 SEC = 3 ROUNDS",
     "visual": "K9 Vajra side-on at dusk fires three times; a fast-forward mission clock jumps 0 -> 5 -> 10 -> 15 s "
               "while three shell pips fill; K9 VAJRA-T / 155 MM stamp",
     "vo": [("tell", [("सिर्फ पंद्रह सेकंड...", "SIRF 15 SECOND...")], 0.5),
            ("punch", [("और तीन गोले!", "AUR 3 GOLE!")], 0.2),
            ("tell", [("यह है के नाइन वज्र,", "YEH HAI K9 VAJRA,"), ("जो एक सौ पचपन एमएम के गोले,", "JO 155 MM KE GOLE,"),
                      ("लगातार दागती है।", "LAGATAAR DAAGTI HAI!")], 0)]},
    {"key": "mrsi", "accent": RED, "text": "MRSI: SAME TIME IMPACT",
     "visual": "Side cross-section: the gun fires high, middle, then low arcs; the three shells fly together and hit "
               "the target in the same instant; a timeline shows staggered launches ending on one impact line",
     "vo": [("slow", [("पर असली खेल?", "PAR ASLI KHEL?")], 0.3),
            ("tell", [("तीनों गोले", "TEENON GOLE"), ("अलग-अलग रास्तों से उड़ते हैं...", "ALAG-ALAG RASTON SE UDTE HAIN...")],
             0.4),
            ("punch", [("लेकिन टारगेट पर,", "LEKIN TARGET PAR,"), ("एक ही सेकंड में गिरते हैं!", "EK HI SECOND ME GIRTE HAIN!")],
             0.25),
            ("tell", [("इसे कहते हैं,", "ISE KEHTE HAIN,"), ("एम आर एस आई तकनीक।", "MRSI TAKNEEK!")], 0)]},
    {"key": "scoot", "accent": KHAKI, "text": "40 KM RANGE | SHOOT & SCOOT",
     "visual": "Top-down tactical map: a ~40 KM range ring sweeps out; enemy counter-fire traces back to the gun, "
               "but the K9 has driven off along the road; the incoming round hits an empty spot (MISS)",
     "vo": [("fast", [("चालीस किलोमीटर दूर तक", "40 KM DOOR TAK"), ("सटीक वार!", "SATEEK VAAR!")], 0.25),
            ("tell", [("और दुश्मन पलटकर जवाब दे...", "AUR DUSHMAN PALATKAR JAWAAB DE...")], 0.35),
            ("tell", [("उससे पहले,", "USSE PEHLE,")], 0.2),
            ("punch", [("यह अपनी जगह", "YEH APNI JAGAH"), ("बदल चुकी होती है।", "BADAL CHUKI HOTI HAI!")], 0)]},
    {"key": "poll", "accent": INDIA_GREEN, "text": "SABSE KHATARNAK KAUN?",
     "visual": "Deployment tiles DESERT -> LADAKH; then a poll board K9 VAJRA / DHANUSH / ATAGS, the reticle locking "
               "onto each gun as it is named",
     "vo": [("punch", [("रेगिस्तान से लेकर,", "REGISTAAN SE LEKAR,"), ("लद्दाख की बर्फीली चोटियों तक", "LADAKH KI BARFEELI CHOTIYON TAK"),
                       ("तैनात!", "TAINAAT!")], 0.35),
            ("tell", [("आपके हिसाब से", "AAPKE HISAAB SE"), ("भारत की सबसे ख़तरनाक तोप", "BHARAT KI SABSE KHATARNAK TOP"),
                      ("कौन सी है?", "KAUN SI HAI?")], 0.3),
            ("tell", [("के नाइन,", "K9,")], 0.5),
            ("tell", [("धनुष...", "DHANUSH...")], 0.5),
            ("tell", [("या फिर एटैग्स?", "YA PHIR ATAGS?")], 0.3),
            ("punch", [("कमेंट्स में बताइए!", "COMMENTS ME BATAIYE!")], 0)]},
]

# one narrator: pitch stays fixed (pitch swings read as two voices); pace and loudness carry the delivery
K9_TONES = {"tell": ("+12%", "+0Hz", "+10%"), "punch": ("+10%", "+0Hz", "+20%"),
            "slow": ("+4%", "+0Hz", "+8%"), "fast": ("+18%", "+0Hz", "+18%")}
DELIVERY = {s["key"]: [(K9_TONES[tone], " ".join(hi for hi, _ in chunks), pause) for tone, chunks, pause in s["vo"]]
            for s in SPEC}
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {"15": GOLD, "SECOND": GOLD, "3": GOLD, "GOLE": GOLD, "K9": SAFFRON, "VAJRA": SAFFRON, "155": KHAKI,
       "MM": KHAKI, "LAGATAAR": RED, "KHEL": RED, "TEENON": GOLD, "RASTON": KHAKI, "EK": RED, "PAL": RED,
       "MRSI": RED, "40": KHAKI, "KM": KHAKI, "MAAR": RED, "DUSHMAN": RED, "JAWAAB": RED, "PEHLE": GOLD,
       "JAGAH": GOLD, "BADAL": GOLD, "REGISTAAN": SAND, "LADAKH": SNOW, "BARFEELI": SNOW, "CHOTIYON": SNOW,
       "KHATARNAK": RED, "KAUN": GOLD, "DHANUSH": SAFFRON, "ATAGS": INDIA_GREEN, "COMMENTS": GOLD, "SIRF": GOLD,
       "TARGET": RED, "TAKNEEK": RED, "SATEEK": RED, "VAAR": RED, "PALATKAR": RED, "BHARAT": SAFFRON}

CAP_TOP, CAP_BOTTOM = 1180, 1280
UI_CLEAR = H - 400
GROUND = 1000


# ============================================================ drawing kit

def ridge(ctx, base, amp, seed, c, a=1.0, drift=0.0, snow=False):
    """Jagged mountain silhouette; snow caps on the peaks if asked."""
    pts = []
    for i in range(41):
        x = i / 40 * (W + 200) - 100 - drift
        h = amp * (0.45 + 0.55 * abs(math.sin(i * 0.9 + seed)) * (0.6 + 0.4 * rnd(i, seed)))
        pts.append((x, base - h))
    ctx.move_to(-100, base + 400)
    for p in pts:
        ctx.line_to(*p)
    ctx.line_to(W + 100, base + 400)
    ctx.close_path()
    rgba(ctx, c, a)
    ctx.fill()
    if snow:
        for i, (x, y) in enumerate(pts[1:-1], 1):
            if y < pts[i - 1][1] and y < pts[i + 1][1] and base - y > amp * 0.7:
                ctx.move_to(x, y)
                ctx.line_to(x - 28, y + 34)
                ctx.line_to(x - 8, y + 26)
                ctx.line_to(x + 6, y + 38)
                ctx.line_to(x + 26, y + 30)
                ctx.close_path()
                rgba(ctx, SNOW, 0.85 * a)
                ctx.fill()


def terrain(ctx, t, ground=GROUND):
    """Dusk sky, two Ladakh-style ridges drifting slowly, olive ground with grass flecks."""
    g = cairo.LinearGradient(0, 0, 0, ground)
    g.add_color_stop_rgb(0, *SKY_TOP)
    g.add_color_stop_rgb(1, *SKY_BOT)
    ctx.rectangle(0, 0, W, ground)
    ctx.set_source(g)
    ctx.fill()
    for i in range(40):
        circle(ctx, rnd(i, 1) * W, rnd(i, 2) * 420 + 160, 1 + 1.3 * rnd(i, 3), (1, 1, 1), 0.15 + 0.3 * rnd(i, 4))
    glow(ctx, 820, ground - 120, 380, FLAME, 0.22)
    ridge(ctx, ground, 360, 1.3, hexc("#3A2638"), drift=t * 6, snow=True)
    ridge(ctx, ground, 200, 4.1, hexc("#24182A"), drift=t * 14)
    g = cairo.LinearGradient(0, ground, 0, H)
    g.add_color_stop_rgb(0, *OLIVE)
    g.add_color_stop_rgb(1, *OLIVE_D)
    ctx.rectangle(0, ground, W, H - ground)
    ctx.set_source(g)
    ctx.fill()
    for i in range(50):
        x, y = rnd(i, 5) * W, ground + 8 + rnd(i, 6) * 140
        line(ctx, [(x, y), (x + 4, y - 10 - 8 * rnd(i, 7))], KHAKI, 2, 0.25)


PIVOT = (55, -182)   # barrel trunnion, hull coordinates
BARREL = 430


def muzzle(x, y, s, elev):
    return x + s * (PIVOT[0] + BARREL * math.cos(elev)), y + s * (PIVOT[1] - BARREL * math.sin(elev))


def k9(ctx, x, y, s, t, elev=0.45, recoil=0.0, a=1.0, moving=0.0):
    """Side view facing right: tracks + six road wheels, sloped hull, boxy turret, long 52-cal barrel."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -240, -72, 480, 72, 34)   # track run
    rgba(ctx, (0.08, 0.08, 0.07), a)
    ctx.fill()
    for i in range(6):
        wx = -180 + i * 72
        circle(ctx, wx, -36, 27, (0.24, 0.26, 0.2), a)
        circle(ctx, wx, -36, 10, (0.5, 0.52, 0.42), a)
        sp = t * 8 * moving + i
        line(ctx, [(wx, -36), (wx + 18 * math.cos(sp), -36 + 18 * math.sin(sp))], (0.1, 0.1, 0.1), 3, a)
    for k in range(24):   # track teeth
        tx = (-230 + k * 20 + (t * 160 * moving) % 20)
        line(ctx, [(tx, -72), (tx + 8, -72)], (0.35, 0.35, 0.3), 4, a)
    ctx.move_to(-238, -70)   # hull
    ctx.line_to(-238, -140)
    ctx.line_to(150, -140)
    ctx.line_to(248, -98)
    ctx.line_to(248, -70)
    ctx.close_path()
    rgba(ctx, OLIVE, a)
    ctx.fill_preserve()
    rgba(ctx, OLIVE_D, a)
    ctx.set_line_width(3)
    ctx.stroke()
    ctx.save()   # barrel (behind the turret face)
    ctx.translate(*PIVOT)
    ctx.rotate(-elev)
    r = recoil
    ctx.rectangle(-60 - r, -11, BARREL + 60 - 40, 22)
    rgba(ctx, shade(OLIVE, 0.85), a)
    ctx.fill()
    rrect(ctx, 150 - r, -16, 46, 32, 8)   # fume extractor
    rgba(ctx, shade(OLIVE, 0.75), a)
    ctx.fill()
    rrect(ctx, BARREL - 48 - r, -17, 48, 34, 5)   # muzzle brake
    rgba(ctx, (0.2, 0.22, 0.18), a)
    ctx.fill()
    for k in range(3):
        ctx.rectangle(BARREL - 42 - r + k * 14, -17, 6, 34)
        rgba(ctx, (0.05, 0.05, 0.05), a)
        ctx.fill()
    ctx.restore()
    ctx.move_to(-212, -140)   # turret
    ctx.line_to(-212, -222)
    ctx.line_to(24, -226)
    ctx.line_to(86, -186)
    ctx.line_to(86, -140)
    ctx.close_path()
    rgba(ctx, shade(OLIVE, 1.12), a)
    ctx.fill_preserve()
    rgba(ctx, OLIVE_D, a)
    ctx.set_line_width(3)
    ctx.stroke()
    rrect(ctx, -150, -246, 70, 24, 6)   # commander's hatch
    rgba(ctx, shade(OLIVE, 0.9), a)
    ctx.fill()
    line(ctx, [(-115, -246), (-60, -262)], (0.15, 0.15, 0.12), 6, a)   # roof MG
    for k, c in enumerate((SAFFRON, (1, 1, 1), INDIA_GREEN)):   # tricolour roundel
        circle(ctx, -150, -182, 26 - 8 * k, c, a)
    text(ctx, "K9", -60, -182, 40, KHAKI, font=CAPTION_FONT, bold=False, a=a)
    ctx.restore()


def shot_fx(ctx, x, y, s, elev, t, shots):
    """Muzzle flash, blast ring and drifting smoke for every shot time in `shots`; returns current recoil."""
    mx, my = muzzle(x, y, s, elev)
    recoil = 0.0
    for ts in shots:
        u = t - ts
        if u < 0:
            continue
        recoil = max(recoil, 46 * math.exp(-u * 7) * (1 - math.exp(-u * 60)))
        for q in range(6):   # smoke puffs
            k = clamp(u / 2.2)
            px = mx + (40 + 120 * k) * math.cos(-elev + (q - 2.5) * 0.35) * s / 0.9
            py = my - 40 * k - 30 * q * k
            circle(ctx, px, py, s * (30 + 70 * k + 8 * q), (0.75, 0.72, 0.66), 0.32 * (1 - k))
        if u < 0.16:
            k = u / 0.16
            glow(ctx, mx, my, s * 420, FLAME, 0.9 * (1 - k))
            glow(ctx, mx, my, s * 160, (1, 1, 0.85), 1 - k)
            ctx.save()
            ctx.translate(mx, my)
            ctx.rotate(-elev)
            ctx.move_to(0, -26 * s)
            ctx.line_to(260 * s * (1 - 0.5 * k), 0)
            ctx.line_to(0, 26 * s)
            ctx.close_path()
            rgba(ctx, (1, 0.9, 0.6), 1 - k)
            ctx.fill()
            ctx.restore()
        if u < 0.5:
            ctx.arc(mx, my, s * (40 + 520 * ease_out_cubic(u / 0.5)), 0, math.tau)
            rgba(ctx, (1, 0.95, 0.85), 0.5 * (1 - u / 0.5))
            ctx.set_line_width(5)
            ctx.stroke()
    return recoil


def shell_icon(ctx, x, y, s, c, a=1.0):
    """Upright 155 mm shell: ogive nose, body, driving band."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(-14, 30)
    ctx.line_to(-14, -10)
    ctx.curve_to(-14, -28, -4, -40, 0, -46)
    ctx.curve_to(4, -40, 14, -28, 14, -10)
    ctx.line_to(14, 30)
    ctx.close_path()
    rgba(ctx, c, a)
    ctx.fill()
    ctx.rectangle(-15, 18, 30, 6)
    rgba(ctx, (0.7, 0.4, 0.2), a)
    ctx.fill()
    ctx.restore()


def blast(ctx, x, y, u, size=1.0):
    """Ground impact: flash, shock ring, dirt plume."""
    if u < 0:
        return
    k = clamp(u / 0.7)
    glow(ctx, x, y, 320 * size, FLAME, 0.9 * (1 - k))
    glow(ctx, x, y, 120 * size, (1, 1, 0.85), 1 - clamp(u / 0.25))
    ctx.arc(x, y, (40 + 360 * ease_out_cubic(k)) * size, 0, math.tau)
    rgba(ctx, (1, 0.9, 0.7), 0.7 * (1 - k))
    ctx.set_line_width(7)
    ctx.stroke()
    for i in range(14):
        ang = -math.pi * (0.1 + 0.8 * rnd(i, 21))
        dist = (60 + 200 * rnd(i, 22)) * size * ease_out_cubic(clamp(u / 0.9))
        circle(ctx, x + dist * math.cos(ang), y + dist * math.sin(ang) + 120 * clamp(u / 0.9) ** 2,
               (6 + 10 * rnd(i, 23)) * size, (0.3, 0.24, 0.18), 1 - clamp(u / 1.2))


def reticle(ctx, x, y, r, c, a=1.0, spin=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(spin)
    ctx.arc(0, 0, r, 0, math.tau)
    rgba(ctx, c, a)
    ctx.set_line_width(5)
    ctx.stroke()
    for k in range(4):
        ang = k * math.pi / 2
        line(ctx, [(math.cos(ang) * r * 0.55, math.sin(ang) * r * 0.55), (math.cos(ang) * r * 1.3,
                                                                          math.sin(ang) * r * 1.3)], c, 5, a)
    ctx.restore()
    circle(ctx, x, y, 5, c, a)


def piecewise(t, pts):
    if t <= pts[0][0]:
        return pts[0][1]
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if t <= t1:
            return lerp(v0, v1, (t - t0) / max(1e-6, t1 - t0))
    return pts[-1][1]


# ============================================================ scenes

class Burst(Cued):
    """Three shots with a fast-forward 0 -> 15 s mission clock and filling shell pips."""

    def beats(self, d):
        c = self.cue
        return {"gole": c("3 GOLE", d * 0.18), "k9": c("K9", d * 0.35), "mm": c("155", d * 0.55),
                "lag": c("LAGATAAR", d * 0.75)}

    def shots(self, d):
        b = self.beats(d)
        return [b["gole"], b["k9"] + 0.15, b["lag"] + 0.1]

    def events(self, d):
        b = self.beats(d)
        ev = [(0.02, "thud"), (0.05, "alarm"), (b["mm"], "pick"), (d - 0.3, "kaching")]
        for ts in self.shots(d):
            ev += [(ts, "boom"), (ts + 0.02, "thud"), (ts + 0.08, "whoosh")]
        return ev + [(k * 0.25, "tick" if k % 2 else "tock") for k in range(int(b["gole"] / 0.25))]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        shots = self.shots(d)
        terrain(ctx, t)
        gx, gs, elev = 420, 1.25, 0.5
        recoil = shot_fx(ctx, gx, GROUND + 10, gs, elev, t, shots)
        k9(ctx, gx, GROUND + 10, gs, t, elev=elev, recoil=recoil)
        mx, my = muzzle(gx, GROUND + 10, gs, elev)
        for ts in shots:   # shells streak off the top-right
            u = t - ts
            if 0 < u < 0.35:
                k = u / 0.35
                sx, sy = mx + 900 * k * math.cos(elev), my - 900 * k * math.sin(elev)
                line(ctx, [(sx - 90 * math.cos(elev), sy + 90 * math.sin(elev)), (sx, sy)], (1, 0.9, 0.6), 6, 1 - k)
        clock = piecewise(t, [(shots[0], 0), (shots[1], 5), (shots[2], 10), (d - 0.3, 15)])
        done = t > d - 0.3
        big_readout(ctx, f"00:{clock:04.1f}", 300, 480, 130, GOLD if done else (1, 1, 1))
        text(ctx, ">> FAST-FORWARD", 300, 560, 28, KHAKI, font=MONO, stroke=(0, 0, 0), stroke_w=4)
        for i, ts in enumerate(shots):
            lit = t >= ts
            shell_icon(ctx, 200 + i * 100, 660, 1.3 if lit else 1.1, GOLD if lit else (1, 1, 1), 1.0 if lit else 0.25)
        if t < b["k9"]:
            stamp(ctx, 540, 300, t, -0.03, 820, 170, GOLD, [("15 SEC = 3 ROUNDS", 4, 92, GOLD)])
        else:
            stamp(ctx, 540, 300, t - b["k9"], 0.02, 760, 190, SAFFRON,
                  [("K9 VAJRA-T", -26, 100, (1, 1, 1)), ("SELF-PROPELLED HOWITZER", 52, 34, SAFFRON)])
        chip(ctx, "155 MM / 52 CAL", 540, 1090, KHAKI, t - b["mm"], size=40)


class Mrsi(Cued):
    """High, middle, low arcs fired in turn; all three shells hit the target together."""

    D_GUN = (150, 1000)
    TARGET = (930, 1000)

    def beats(self, d):
        c = self.cue
        return {"teen": c("TEENON", d * 0.15), "pal": c("EK HI SECOND", d * 0.6), "mrsi": c("MRSI", d * 0.85)}

    def plan(self, d):
        b = self.beats(d)
        t0 = b["teen"] + 0.1
        impact = b["pal"] + 0.55
        gap = (impact - t0) * 0.22
        fires = [t0 + k * gap for k in range(3)]
        flights = [impact - f for f in fires]
        heights = [540 * (fl / flights[0]) ** 2 for fl in flights]
        return fires, flights, heights, impact

    def events(self, d):
        fires, _, _, impact = self.plan(d)
        b = self.beats(d)
        ev = [(0.02, "whoosh"), (0.1, "beep"), (impact, "boom"), (impact + 0.03, "boom"), (impact + 0.06, "thud"),
              (b["mrsi"], "zap"), (b["mrsi"] + 0.05, "kaching")]
        for f in fires:
            ev += [(f, "thud"), (f + 0.05, "pop"), (f + 0.1, "whoosh")]
        return ev

    def draw(self, ctx, t, d):
        b = self.beats(d)
        fires, flights, heights, impact = self.plan(d)
        terrain(ctx, t * 0.4)
        gx, gy = self.D_GUN
        tx, ty = self.TARGET
        gs = 0.45
        span = tx - gx
        elevs = [math.atan(4 * h / span) for h in heights]
        # the barrel steps down from high to low between shots
        cur = piecewise(t, [(fires[0] - 0.4, elevs[0]), (fires[0], elevs[0]), (fires[1], elevs[1]),
                            (fires[2], elevs[2])])
        mx, my = muzzle(gx, gy + 8, gs, cur)
        rrect(ctx, tx - 70, ty - 60, 140, 60, 10)   # enemy bunker
        rgba(ctx, (0.18, 0.14, 0.12))
        ctx.fill()
        ctx.rectangle(tx - 40, ty - 40, 80, 12)
        rgba(ctx, (0.02, 0.02, 0.02))
        ctx.fill()
        reticle(ctx, tx, ty - 30, 70, RED, 0.8 if t < impact else 0.0, spin=t * 0.6)
        cols = (GOLD, SAFFRON, KHAKI)
        for i, (f, fl, h) in enumerate(zip(fires, flights, heights)):
            if t < f:
                continue
            ex, ey = muzzle(gx, gy + 8, gs, elevs[i])
            pts = [(lerp(ex, tx, p), lerp(ey, ty - 20, p) - 4 * h * p * (1 - p)) for p in np.linspace(0, 1, 50)]
            ctx.set_dash([12, 12])
            line(ctx, pts, cols[i], 3, 0.45)
            ctx.set_dash([])
            p = clamp((t - f) / fl)
            if p < 1:
                n = max(2, int(50 * p))
                line(ctx, pts[max(0, n - 8):n], cols[i], 7, 0.9)
                sx, sy = pts[min(49, n)]
                glow(ctx, sx, sy, 40, cols[i], 0.7)
                circle(ctx, sx, sy, 9, (1, 1, 1))
            ax, ay = pts[25]
            if t < impact:
                chip(ctx, f"GOLA {i + 1}", ax, ay - 50, cols[i], t - f - 0.15, size=30)
        recoil = shot_fx(ctx, gx, gy + 8, gs, cur, t, fires)
        k9(ctx, gx, gy + 8, gs, t, elev=cur, recoil=recoil)
        blast(ctx, tx, ty - 20, t - impact, 1.3)
        # timeline: staggered launches, one impact line
        tl_x0, tl_x1, tl_y = 140, 940, 1080
        if t > fires[0]:
            line(ctx, [(tl_x1, tl_y - 30), (tl_x1, tl_y + 70)], RED, 4, 0.9)
            for i, (f, fl) in enumerate(zip(fires, flights)):
                x0 = lerp(tl_x0, tl_x1, (f - fires[0]) / flights[0])
                x1 = lerp(tl_x0, tl_x1, clamp((t - fires[0]) / flights[0]))
                if x1 > x0:
                    line(ctx, [(x0, tl_y - 16 + i * 22), (x1, tl_y - 16 + i * 22)], cols[i], 12, 0.9)
                    circle(ctx, x0, tl_y - 16 + i * 22, 8, cols[i])
            text(ctx, "FIRE", tl_x0, tl_y + 60, 26, (1, 1, 1), font=MONO, a=0.8)
            text(ctx, "IMPACT", tl_x1, tl_y + 60, 26, RED, font=MONO, a=0.8)
        if t < b["teen"]:
            stamp(ctx, 540, 300, t, -0.03, 640, 170, RED, [("ASLI KHEL?", 4, 110, RED)])
        elif impact <= t < b["mrsi"]:
            stamp(ctx, 540, 300, t - impact, 0.03, 820, 170, GOLD, [("SAME TIME IMPACT!", 4, 84, GOLD)])
        elif t >= b["mrsi"]:
            stamp(ctx, 540, 300, t - b["mrsi"], -0.02, 900, 200, RED,
                  [("MRSI", -30, 110, (1, 1, 1)), ("MULTIPLE ROUNDS SIMULTANEOUS IMPACT", 58, 30, RED)])


class Scoot(Cued):
    """Top-down map: ~40 KM range ring, enemy counter-fire, the K9 already gone (MISS)."""

    G0, G1 = (250, 960), (620, 1080)
    ENEMY = (850, 470)

    def beats(self, d):
        c = self.cue
        return {"km": c("40 KM", 0.05), "dush": c("DUSHMAN", d * 0.4), "pehle": c("USSE PEHLE", d * 0.6),
                "jagah": c("JAGAH", d * 0.72)}

    def events(self, d):
        b = self.beats(d)
        hit = d - 0.55
        return [(0.02, "whoosh"), (b["km"] + 0.1, "zap"), (b["dush"], "alarm"), (b["dush"] + 0.3, "beep"),
                (b["pehle"], "engine", 1.6), (hit, "boom"), (hit + 0.05, "thud"), (hit + 0.3, "dingdong")]

    def map_bg(self, ctx, t):
        ctx.rectangle(0, 0, W, H)
        rgba(ctx, hexc("#2F3A24"))
        ctx.fill()
        for k in range(9):   # contour loops
            cx, cy = 300 + 520 * rnd(k, 31), 380 + 700 * rnd(k, 32)
            for ring in range(4):
                ctx.new_path()
                for j in range(41):
                    a_ = j / 40 * math.tau
                    r = (40 + ring * 34) * (1 + 0.25 * math.sin(a_ * 3 + k))
                    ctx.line_to(cx + r * 1.4 * math.cos(a_), cy + r * math.sin(a_))
                ctx.close_path()
                rgba(ctx, KHAKI, 0.12)
                ctx.set_line_width(2)
                ctx.stroke()
        for x in range(0, W, 120):
            line(ctx, [(x, 180), (x, UI_CLEAR)], (1, 1, 1), 1, 0.08)
        for y in range(180, UI_CLEAR, 120):
            line(ctx, [(0, y), (W, y)], (1, 1, 1), 1, 0.08)
        road = [(0, 1000), (250, 960), (440, 1010), (620, 1080), (1080, 1120)]
        line(ctx, road, (0.55, 0.5, 0.38), 26, 0.7)
        ctx.set_dash([18, 16])
        line(ctx, road, KHAKI, 3, 0.6)
        ctx.set_dash([])

    def gun_top(self, ctx, x, y, ang, a=1.0):
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(ang)
        rrect(ctx, -46, -26, 92, 52, 8)
        rgba(ctx, OLIVE, a)
        ctx.fill_preserve()
        rgba(ctx, KHAKI, a)
        ctx.set_line_width(3)
        ctx.stroke()
        line(ctx, [(0, 0), (82, 0)], KHAKI, 7, a)
        circle(ctx, -4, 0, 18, shade(OLIVE, 1.2), a)
        ctx.restore()

    def draw(self, ctx, t, d):
        b = self.beats(d)
        self.map_bg(ctx, t)
        g0 = self.G0
        ex, ey = self.ENEMY
        hit = d - 0.55
        u = t - b["km"]
        if u > 0:   # range ring
            r = 760 * ease_out_cubic(clamp(u / 0.9))
            ctx.arc(*g0, r, -math.pi * 0.62, math.pi * 0.12)
            rgba(ctx, KHAKI, 0.9)
            ctx.set_line_width(5)
            ctx.stroke()
            ctx.move_to(*g0)
            ctx.arc(*g0, r, -math.pi * 0.62, math.pi * 0.12)
            ctx.close_path()
            rgba(ctx, KHAKI, 0.08)
            ctx.fill()
            chip(ctx, "~40 KM", 330, 560, KHAKI, u - 0.4, size=46, sub="RANGE (AMMO PAR NIRBHAR)")
        # enemy battery
        a_en = clamp((t - b["dush"]) / 0.3)
        if a_en > 0:
            ctx.rectangle(ex - 40, ey - 40, 80, 80)
            rgba(ctx, RED, 0.25 * a_en)
            ctx.fill()
            ctx.rectangle(ex - 40, ey - 40, 80, 80)
            rgba(ctx, RED, a_en)
            ctx.set_line_width(5)
            ctx.stroke()
            text(ctx, "DUSHMAN", ex, ey + 75, 34, RED, font=MONO, a=a_en, stroke=(0, 0, 0), stroke_w=5)
            sweep = t * 2.4
            line(ctx, [(ex, ey), (ex + 240 * math.cos(sweep), ey + 240 * math.sin(sweep))], RED, 3, 0.6 * a_en)
            ctx.set_dash([14, 12])
            line(ctx, [(ex, ey), g0], RED, 3, 0.7 * a_en)
            ctx.set_dash([])
            chip(ctx, "COUNTER-FIRE", 660, 700, RED, t - b["dush"] - 0.3, size=32)
        # the gun drives off from "USSE PEHLE"
        k = ease_in_out(clamp((t - b["pehle"]) / 1.4))
        road = [(250, 960), (440, 1010), (620, 1080)]
        seg = k * (len(road) - 1)
        i = min(int(seg), len(road) - 2)
        f = seg - i
        gx, gy = lerp(road[i][0], road[i + 1][0], f), lerp(road[i][1], road[i + 1][1], f)
        ang = math.atan2(road[i + 1][1] - road[i][1], road[i + 1][0] - road[i][0]) * clamp(k * 4)
        ang = lerp(-0.9, ang, clamp(k * 4))   # faces the enemy until it moves
        if k > 0:
            for q in range(1, 9):   # track marks behind it
                pq = max(0.0, seg - q * 0.06)
                j = min(int(pq), len(road) - 2)
                fx = pq - j
                circle(ctx, lerp(road[j][0], road[j + 1][0], fx), lerp(road[j][1], road[j + 1][1], fx), 5,
                       (0.1, 0.1, 0.08), 0.5)
        self.gun_top(ctx, gx, gy, ang)
        text(ctx, "K9", gx, gy - 60, 36, SAFFRON, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=5)
        # incoming counter-battery round
        t_in = b["dush"] + 0.5
        p = clamp((t - t_in) / max(0.5, hit - t_in))
        if t_in < t < hit:
            sx, sy = lerp(ex, g0[0], p), lerp(ey, g0[1], p) - 220 * math.sin(math.pi * p)
            glow(ctx, sx, sy, 50, RED, 0.7)
            circle(ctx, sx, sy, 10, (1, 1, 1))
            reticle(ctx, *g0, 60, RED, 0.9, spin=t)
        blast(ctx, g0[0], g0[1], t - hit, 0.9)
        if t > hit:
            stamp(ctx, 540, 300, t - hit, 0.03, 600, 170, GOLD, [("MISS!", 4, 120, GOLD)])
        elif t > b["jagah"]:
            stamp(ctx, 540, 300, t - b["jagah"], -0.02, 760, 170, KHAKI, [("SHOOT & SCOOT", 4, 90, KHAKI)])


class Poll(Cued):
    """Desert -> Ladakh tiles and the +100 order, then the 3-gun poll board with a hopping reticle."""

    ROWS = (("K9 VAJRA", "155/52 SP", SAFFRON), ("DHANUSH", "155/45 TOWED", GOLD), ("ATAGS", "155/52 TOWED",
                                                                                    INDIA_GREEN))

    def beats(self, d):
        c = self.cue
        return {"ladakh": c("REGISTAAN", 0.05), "snow": c("LADAKH", d * 0.12), "tain": c("TAINAAT", d * 0.25),
                "sabse": c("AAPKE", d * 0.35), "k9": c("K9", d * 0.6), "dh": c("DHANUSH", d * 0.7),
                "at": c("ATAGS", d * 0.8), "cmt": c("COMMENTS", d * 0.9)}

    def events(self, d):
        b = self.beats(d)
        locks = [(b[k], "beep") for k in ("k9", "dh", "at")]
        return [(0.02, "whoosh"), (b["ladakh"] + 0.3, "pop"), (b["snow"], "pop"), (b["tain"], "kaching"),
                (b["sabse"], "boom"), (b["sabse"] + 0.2, "pop"), (b["cmt"], "dingdong")] + locks

    def tile(self, ctx, x, y, w, h, kind, label, a):
        ctx.save()
        rrect(ctx, x, y, w, h, 22)
        ctx.clip()
        if kind == "desert":
            g = cairo.LinearGradient(0, y, 0, y + h)
            g.add_color_stop_rgb(0, *hexc("#F0B35E"))
            g.add_color_stop_rgb(1, *hexc("#9B5A2A"))
            ctx.rectangle(x, y, w, h)
            ctx.set_source(g)
            ctx.fill()
            for k in range(3):
                ctx.move_to(x, y + h * (0.6 + 0.12 * k))
                ctx.curve_to(x + w * 0.3, y + h * (0.48 + 0.12 * k), x + w * 0.6, y + h * (0.72 + 0.1 * k), x + w,
                             y + h * (0.56 + 0.12 * k))
                ctx.line_to(x + w, y + h)
                ctx.line_to(x, y + h)
                ctx.close_path()
                rgba(ctx, shade(SAND, 1 - 0.12 * k))
                ctx.fill()
        else:
            g = cairo.LinearGradient(0, y, 0, y + h)
            g.add_color_stop_rgb(0, *hexc("#2B4A72"))
            g.add_color_stop_rgb(1, *hexc("#9CB8D0"))
            ctx.rectangle(x, y, w, h)
            ctx.set_source(g)
            ctx.fill()
            ctx.save()
            ctx.translate(x, y + h * 0.2)
            ctx.scale(w / W, 0.5)
            ridge(ctx, h * 1.4, 300, 2.2, hexc("#5E6F86"), snow=True)
            ctx.restore()
            ctx.rectangle(x, y + h * 0.82, w, h)
            rgba(ctx, SNOW)
            ctx.fill()
        k9(ctx, x + w * 0.45, y + h * 0.9, 0.42, 0, elev=0.35)
        ctx.restore()
        rrect(ctx, x, y, w, h, 22)
        rgba(ctx, (1, 1, 1), 0.9 * a)
        ctx.set_line_width(4)
        ctx.stroke()
        text(ctx, label, x + w / 2, y + h + 46, 48, (1, 1, 1), font=CAPTION_FONT, bold=False, a=a, stroke=(0, 0, 0),
             stroke_w=6)

    def draw(self, ctx, t, d):
        b = self.beats(d)
        terrain(ctx, t * 0.5)
        a = clamp((b["sabse"] - t) / 0.2)
        if a > 0:
            u = t - b["ladakh"]
            k = ease_out_cubic(clamp(u / 0.35))
            ctx.save()
            ctx.translate(0, 60 * (1 - k))
            ctx.push_group()
            self.tile(ctx, 70, 420, 420, 380, "desert", "REGISTAAN", 1)
            k2 = ease_out_cubic(clamp((t - b["snow"]) / 0.35))
            if k2 > 0:
                self.tile(ctx, 590, 420, 420, 380, "ladakh", "LADAKH", 1)
                line(ctx, [(500, 610), (580, 610)], GOLD, 10, k2)
                ctx.move_to(586, 610)
                ctx.line_to(556, 588)
                ctx.line_to(556, 632)
                ctx.close_path()
                rgba(ctx, GOLD, k2)
                ctx.fill()
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(a * k)
            ctx.restore()
            if t < b["tain"]:
                stamp(ctx, 540, 300, u, -0.02, 840, 160, SAND, [("REGISTAAN SE LADAKH", 4, 76, SAND)])
            else:
                stamp(ctx, 540, 300, t - b["tain"], 0.02, 700, 160, SNOW, [("TAINAAT!", 4, 100, SNOW)])
            return
        u = t - b["sabse"]
        text(ctx, "SABSE KHATARNAK KAUN?", 540, 300, 76, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
             stroke_w=8, a=clamp(u / 0.2))
        ys = (500, 700, 900)
        for i, ((name, sub, c), y) in enumerate(zip(self.ROWS, ys)):
            k = ease_out_cubic(clamp((u - 0.12 * i) / 0.35))
            if k <= 0:
                continue
            ctx.save()
            ctx.translate(lerp(W, 0, k), 0)
            rrect(ctx, 90, y - 80, 900, 160, 26)
            rgba(ctx, (0.03, 0.04, 0.03), 0.9)
            ctx.fill_preserve()
            rgba(ctx, c)
            ctx.set_line_width(4)
            ctx.stroke()
            text(ctx, str(i + 1), 170, y, 80, c, font=CAPTION_FONT, bold=False)
            text(ctx, name, 250, y - 14, 72, (1, 1, 1), font=CAPTION_FONT, bold=False, anchor="l")
            text(ctx, sub, 252, y + 48, 28, c, font=MONO, anchor="l")
            ctx.restore()
        if t > b["k9"]:   # reticle locks onto each gun as it is named, then settles in the middle
            settled = t > b["cmt"]
            row = 2 if t > b["at"] else (1 if t > b["dh"] else 0)
            ry = 700 if settled else ys[row]
            reticle(ctx, 880, ry, 58, GOLD, 1.0, spin=t * 1.5)
            if settled:
                pop = ease_out_back(clamp((t - b["cmt"]) / 0.35))
                ctx.save()
                ctx.translate(540, 1080)
                ctx.scale(pop, pop)
                rrect(ctx, -300, -52, 600, 104, 52)
                rgba(ctx, GOLD)
                ctx.fill()
                text(ctx, "1, 2 YA 3? COMMENT", 0, 2, 50, (0.05, 0.05, 0.05), font=CAPTION_FONT, bold=False)
                ctx.restore()


SCENE_CLASSES = {"burst": Burst, "mrsi": Mrsi, "scoot": Scoot, "poll": Poll}


# ============================================================ compositor ("fire mission")

def header(ctx, idx, t_global):
    reticle(ctx, 84, 104, 22, GOLD, 1.0)
    text(ctx, "REALITY SHIFT", 128, 90, 34, (1, 1, 1), a=0.92, anchor="l")
    text(ctx, "FIRE MISSION // K9 VAJRA", 128, 124, 22, KHAKI, font=MONO, a=0.85, anchor="l")
    text(ctx, f"FM {idx + 1}/{len(SPEC)}", W - 60, 84, 28, (1, 1, 1), font=MONO, a=0.9, anchor="r")
    for i in range(len(SPEC)):
        lit = i <= idx
        shell_icon(ctx, W - 60 - (len(SPEC) - 1 - i) * 34 - 12, 132, 0.45, SPEC[i]["accent"] if lit else (1, 1, 1),
                   1.0 if lit else 0.25)


def caption(ctx, sc, tl, accent):
    """Stencil tape: the current Hinglish chunk on a khaki-edged olive strip that squashes in vertically."""
    cur = None
    for i, (start, _) in enumerate(sc["captions"]):
        if tl >= start - 0.03:
            cur = i
    if cur is None:
        return
    start, cap = sc["captions"][cur]
    u = tl - start + 0.03
    k = ease_out_back(clamp(u / 0.18), 2.4)
    size = 80
    words_ = cap.split(" ")
    ws = [text_width(ctx, w, size, font=CAPTION_FONT, bold=False) for w in words_]
    gap = size * 0.26
    tw = sum(ws) + gap * (len(ws) - 1)
    fit = min(1.0, 880 / tw)
    cy = (CAP_TOP + CAP_BOTTOM) / 2
    ctx.save()
    ctx.translate(W / 2, cy)
    ctx.scale(fit, fit * max(0.05, k))
    pad = 50
    hh = size * 0.74
    rrect(ctx, -tw / 2 - pad, -hh, tw + 2 * pad, 2 * hh, 6)
    rgba(ctx, OLIVE_D, 0.92)
    ctx.fill()
    for sgn in (-1, 1):   # chevron edges in the scene accent
        y0 = sgn * hh
        x = -tw / 2 - pad
        while x < tw / 2 + pad - 20:
            ctx.move_to(x, y0)
            ctx.line_to(x + 18, y0)
            ctx.line_to(x + 30, y0 - sgn * 10)
            ctx.line_to(x + 12, y0 - sgn * 10)
            ctx.close_path()
            rgba(ctx, accent, 0.9)
            ctx.fill()
            x += 38
    x = -tw / 2
    for w, ww in zip(words_, ws):
        c = HOT.get(w.strip(PUNCT + ".").split("-")[0], (1, 1, 1))
        text(ctx, w, x, 0, size, c, font=CAPTION_FONT, bold=False, anchor="l", stroke=(0, 0, 0), stroke_w=8)
        x += ww + gap
    ctx.restore()


def flash_cut(ctx, tl):
    """Muzzle-flash cut: a warm white-out that burns off, with a blast ring from the centre."""
    if tl >= 0.35:
        return
    k = tl / 0.35
    ctx.rectangle(0, 0, W, H)
    rgba(ctx, (1, 0.93, 0.8), 0.85 * (1 - k) ** 2)
    ctx.fill()
    ctx.arc(W / 2, 700, 100 + 1200 * ease_out_cubic(k), 0, math.tau)
    rgba(ctx, FLAME, 0.7 * (1 - k))
    ctx.set_line_width(30 * (1 - k) + 2)
    ctx.stroke()


def compose(idx, tl):
    sc = engine.SCENES[idx]
    spec = SPEC[idx]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    shake = 9 * max(0.0, 1 - tl / 0.3)
    for ts in (getattr(sc["obj"], "shots", lambda _d: [])(sc["dur"])):   # recoil jolts on every shot
        shake += 10 * max(0.0, 1 - (tl - ts) / 0.25) * (tl >= ts)
    ctx.save()
    ctx.translate(shake * math.sin(tl * 83), shake * math.cos(tl * 67))
    sc["obj"].draw(ctx, tl, sc["dur"])
    ctx.restore()
    vignette(ctx)
    g = cairo.LinearGradient(0, 0, 0, 200)
    g.add_color_stop_rgba(0, 0.02, 0.02, 0.01, 0.9)
    g.add_color_stop_rgba(1, 0.02, 0.02, 0.01, 0.0)
    ctx.rectangle(0, 0, W, 200)
    ctx.set_source(g)
    ctx.fill()
    g = cairo.LinearGradient(0, CAP_TOP - 60, 0, UI_CLEAR)
    g.add_color_stop_rgba(0, 0.02, 0.02, 0.01, 0.0)
    g.add_color_stop_rgba(1, 0.02, 0.02, 0.01, 0.9)
    ctx.rectangle(0, CAP_TOP - 60, W, UI_CLEAR - CAP_TOP + 60)
    ctx.set_source(g)
    ctx.fill()
    ctx.rectangle(0, UI_CLEAR, W, H - UI_CLEAR)
    rgba(ctx, (0.02, 0.02, 0.01), 0.9)
    ctx.fill()
    header(ctx, idx, sc["start"] + tl)
    caption(ctx, sc, tl, spec["accent"])
    if idx:
        flash_cut(ctx, tl)
    return surf


def make_frame(t: float) -> np.ndarray:
    scenes = engine.SCENES
    idx = max(i for i, s in enumerate(scenes) if t >= s["start"] or i == 0)
    surf = compose(idx, t - scenes[idx]["start"])
    surf.flush()
    buf = np.ndarray((H, W, 4), dtype=np.uint8, buffer=surf.get_data())
    return buf[:, :, 2::-1].copy()


def write_alignment(final):
    out = [{"scene": spec["key"], "start": round(s["start"], 3), "end": round(s["start"] + s["dur"], 3),
            "voiceover": NARRATION[spec["key"]], "on_screen_text": spec["text"], "visual": spec["visual"],
            "words": [{"t": round(s["start"] + st, 3), "w": w} for st, w in s["captions"]]}
           for spec, s in zip(SPEC, engine.SCENES)]
    path = final.with_suffix(".json")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Alignment: {path}")


# ============================================================ upload kit (see upload_kit.py)

UPLOAD = {
    "titles": [
        "15 Second Me 3 Shells! K9 Vajra Ka Khauf! 🇮🇳",
        "15 Second Me 3 Gole, Teeno Ek Saath Hit! K9 Vajra 🇮🇳",
        "K9 Vajra: 3 Gole Alag Raaste Se, Ek Hi Pal Me! (MRSI)",
        "K9 Vajra Ka MRSI: Dushman Ko Sambhalne Ka Mauka Nahi",
        "K9 Vajra Shoot & Scoot: Fire Karo Aur Gayab!",
        "Registaan Se Ladakh Tak: K9 Vajra Ki Taakat",
        "K9 Vajra Howitzer Kitni Khatarnak Hai? 15 Sec Me 3 Gole",
        "K9 Vajra, Dhanush Ya ATAGS: Sabse Khatarnak Top Kaun?",
    ],
    "thumb_text": "3 GOLE!",
    "queries": ["k9 vajra", "k9 vajra howitzer", "mrsi"],
    "description": """
K9 Vajra howitzer sirf ~15 second me 3 gole (155 MM) daag sakti hai, aur MRSI mode me teeno gole alag raaston se ek hi pal me target par girte hain.
Phir shoot and scoot: dushman jawaab de, usse pehle K9 Vajra jagah badal leti hai.

Is Short me:
• K9 Vajra-T: 155 mm / 52 calibre tracked self-propelled howitzer, L&T (Hazira) dwara Hanwha (South Korea, K9 Thunder) ke saath banayi
• Burst rate: ~15 second me 3 round
• MRSI (Multiple Rounds Simultaneous Impact): barrel ka angle badal kar 3 gole ek saath target par
• Range: ~40 KM tak (extended-range gole ke saath; aam HE gole ki range kam hoti hai)
• Pehle 100 guns (2017 order) pehle registaan ke liye, 2020 ke baad Ladakh me bhi tainaat
• Dec 2024: Raksha Mantralaya ne L&T ke saath 100 aur K9 Vajra ka ~₹7,629 crore ka contract kiya

Aapke hisaab se sabse khatarnak Indian top kaun: K9 Vajra, Dhanush ya ATAGS? 1, 2 ya 3 comment karo.
Aisi aur defence aur geopolitics ke liye Reality Shift ko subscribe karo.

Note: graphics schematic hain, scale par nahi. "15 second" mission clock fast-forward me dikhaya gaya hai; shoot-and-scoot ka scene samjhane ke liye hai, kisi asli ghatna ka nahi.
""",
    "tags": ["k9 vajra", "k9 vajra howitzer", "k9 vajra t", "mrsi", "self propelled howitzer", "indian army artillery",
             "155mm howitzer", "shoot and scoot", "k9 thunder", "l&t defence", "ladakh", "atags", "dhanush",
             "defence shorts hindi", "reality shift"],
    "hashtags": ["#Shorts", "#K9Vajra", "#IndianArmy"],
}


def thumbnail(ctx):
    """1080x1920 cover: 3 GOLE! over a K9 mid-shot with a huge muzzle flash and a 00:15 clock."""
    terrain(ctx, 0.2, 1250)
    gx, gs, elev = 420, 1.7, 0.42
    mx, my = muzzle(gx, 1260, gs, elev)
    glow(ctx, mx, my, 700, FLAME, 0.55)
    glow(ctx, mx, my, 260, (1, 1, 0.85), 0.95)
    for i in range(3):   # three shell streaks fanning out
        a_ = elev + 0.18 - 0.18 * i
        line(ctx, [(mx + 120 * math.cos(a_), my - 120 * math.sin(a_)), (mx + 700 * math.cos(a_),
                                                                         my - 700 * math.sin(a_))],
             (1, 0.9, 0.6), 10, 0.8)
    k9(ctx, gx, 1260, gs, 0, elev=elev, recoil=30)
    g = cairo.LinearGradient(0, 0, 0, 820)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.9)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 820)
    ctx.set_source(g)
    ctx.fill()
    vignette(ctx)
    glow(ctx, 540, 470, 600, GOLD, 0.18)
    text(ctx, "3 GOLE!", 540, 400, 280, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=24)
    rrect(ctx, 290, 580, 500, 150, 30)
    rgba(ctx, (0, 0, 0), 0.8)
    ctx.fill_preserve()
    rgba(ctx, (1, 1, 1))
    ctx.set_line_width(6)
    ctx.stroke()
    text(ctx, "00:15", 540, 657, 130, (1, 1, 1), font=CAPTION_FONT, bold=False)
    text(ctx, "REALITY SHIFT", 540, 1780, 40, (1, 1, 1), a=0.7)


def main() -> None:
    import upload_kit
    story = importlib.import_module("generate_k9_vajra_short")  # a named module, so work files land in work/<name>/
    engine.make_frame = story.make_frame
    final = engine.render(story, "edge")
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
