"""Reality Shift Short: HF-24 Marut - India's first indigenous jet fighter, and why it was shut down.

Topic: HAL HF-24 Marut. Designed at HAL by Kurt Tank's team, first flight 17 June 1961, flew ground attack in the
       1971 war (reportedly also over Longewala), designed for Mach 2 but stuck below Mach 1 on two un-reheated
       Bristol Siddeley Orpheus 703s. The planned Orpheus BOr-12 was dropped and the Egyptian E-300 engine project
       came to nothing; the type was phased out by the late 1980s (last unit 1990). Today's Tejas still flies on
       the American GE F404.
Debate (not politics): "Galti engine ki thi ya sarkar ki soch ki?" - engineering vs policy choices, nobody named.
Format: Vertical 1080x1920 (9:16), 30-45 s (user, 23 Nov 2026: never over 45 s), 6 scenes, payoff in the last
        line and a grammatical loop back into the hook ("...wahin se shuru hui jab" -> "Bharat ka pehla desi jet
        fighter..."). No CTA card: the comment ask lives in the pinned comment.
Audio: user's own KikiVoice narrator recording (no punctuation signs, no pause tags), split with --kiki-split.
Visuals: procedural Cairo - hangar at dusk with a garlanded Marut and a shutter coming down, 1961 sepia take-off,
         Kurt Tank at the drafting table, Thar desert tank column, Mach gauge stuck under 1, Egyptian engine test
         stand fading out, engineer vs official at a desk, tarp over a retired Marut, the engine-vs-policy balance,
         Tejas with its imported engine highlighted, then the hangar again (loop).
On-screen text: the dynamic subtitles plus only prop markings (blueprint "HF-24", gauge numerals) - ASCII only.
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
from shorts.akashteer import ell, poly, seg01, burst, soldier
from shorts.reality_shift import flag
from shorts.tejas_mk1a import draw_tejas_fighter

TOPIC = "HF-24 MARUT - INDIA'S FIRST DESI FIGHTER SHUT DOWN"
OUTPUTS = {"edge": "marut_short.mp4"}
LEGO = {"header": "radar", "caption": "chip", "transition": "scan", "palette": "khaki", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.30          # keep KikiVoice's own breaths short; the line gaps below set the pace
TAIL_PAD = 0.12
TRIM = {"thresh": 0.006, "keep": 0.04, "keep_tail": 0.06}
MUSIC_BPM = 90
MUSIC_STYLE = "tension"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 0       # user: no pause tags and no punctuation signs in the KikiVoice text
MAX_SECONDS = 45.0      # user, 23 Nov 2026: a Short may never run longer than this

PAL = lego.PALETTES["khaki"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
WHITE = (1.0, 1.0, 1.0)
GOLD = hexc("#FFD166")
RED = hexc("#E2483A")
CYAN = hexc("#5FD3FF")
FIRE = hexc("#FF6A1A")
STEEL = hexc("#8C969E")
STEEL_DK = hexc("#4F575E")
CAMO_A = hexc("#7D8466")
CAMO_B = hexc("#5D6448")
CAMO_C = hexc("#9A9B80")
SAND = hexc("#D9B27A")
SAND_DK = hexc("#B88B55")
BLUEPRINT = hexc("#1F4E8C")
MARIGOLD = hexc("#FFA41B")
MARIGOLD_2 = hexc("#FFD23F")
MONO = "Consolas"
GROUND = 1120           # feet line; the caption band starts at lego.CAP_TOP = 1150

SOURCES = [
    "Wikipedia - HAL HF-24 Marut (Kurt Tank design team at HAL; first flight 17 June 1961; two un-reheated Bristol "
    "Siddeley Orpheus 703; designed for Mach 2, never exceeded Mach 1 in service; Egyptian Brandner E-300 testbed "
    "1967, team recalled 1969; 300+ sorties in 1971; IAF called it 'no longer operationally viable' by 1982; phased "
    "out late 1980s, retired 1990): https://en.wikipedia.org/wiki/HAL_HF-24_Marut",
    "HistoryNet - 'Kurt Tank's Indian Storm' (first flight 17 June 1961 by Wg Cdr Suranjan Das; Britain cancelled "
    "funding for the afterburning Orpheus BOr-12; Egypt cancelled the E-300 after 1967; ground attack with No. 10 "
    "and No. 220 Squadrons in 1971; in service until 1990): https://historynet.com/kurt-tanks-indian-storm/",
    "Wikipedia - Battle of Longewala (IAF HF-24 Maruts and Hawker Hunters sent to assist the post; Hunters did most "
    "of the anti-tank work - Marut role hedged as 'reports ke mutabik'): https://en.wikipedia.org/wiki/Battle_of_Longewala",
    "Business Today, 13 Jul 2026 - HAL gets 7th GE F404 engine for Tejas Mk1A (Tejas flies on the American GE "
    "F404-IN20): https://www.businesstoday.in/india/story/hal-gets-7th-ge-f404-engine-for-tejas-mk1a-fault-in-"
    "earlier-engine-resolved-542588-2026-07-13",
]

# Voice text: no commas, no "...", no "!" or "?", no pause tags (user's approved KikiVoice style). Every line ends
# in a purnaviram; the last line has none because it runs straight back into the first.
SPEC = [
    # 00:00-00:04 paradox hook
    {"key": "shutter_hook", "accent": RED, "text": "",
     "visual": "Dusk; a garlanded Marut inside a hangar, a pilot salutes it; on BAND a crewman pulls the chain and the "
               "shutter rolls down over the jet",
     "vo": [("hook", [("भारत का पहला", "BHARAT KA PEHLA"),
                      ("देसी फाइटर", "DESI FIGHTER"),
                      ("जंग जीतकर भी", "JUNG JEETKAR BHI"),
                      ("बंद कर दिया गया।", "BAND KAR DIYA GAYA")])]},

    # 00:04-00:09 what it was
    {"key": "birth", "accent": GOLD, "text": "",
     "visual": "Sepia 1961 take-off with two engineers cheering; then Kurt Tank at the drafting table, an Indian "
               "engineer points at the HF-24 blueprint on the wall",
     "vo": [("tell", [("उन्नीस सौ इकसठ में", "1961 MEIN"),
                      ("उड़ा मरुत।", "UDA MARUT")]),
            ("tell", [("जर्मनी के कर्ट टैंक ने", "GERMANY KE KURT TANK NE"),
                      ("इसे एच ए एल में बनाया।", "ISE HAL MEIN BANAYA")])]},

    # 00:09-00:15 what it achieved
    {"key": "war_1971", "accent": FIRE, "text": "",
     "visual": "Thar desert at dusk, an Indian post with sandbags and a tricolour, a tank column rolls in; two Maruts "
               "dive and fire rockets, the tanks are knocked out, the jawan raises his fist",
     "vo": [("punch", [("इकहत्तर की जंग में", "1971 KI JUNG MEIN"),
                       ("रिपोर्ट्स के मुताबिक", "REPORTS KE MUTABIK"),
                       ("लोंगेवाला में भी", "LONGEWALA MEIN BHI"),
                       ("ये टैंकों पर टूट पड़ा।", "YE TANKON PAR TOOT PADA")])]},

    # 00:15-00:23 why it died: the engine
    {"key": "engine", "accent": CYAN, "text": "",
     "visual": "Marut at altitude, a ghost needle on a Mach gauge swings to 2 (the dream); the real needle stalls under "
               "1 and the engine coughs smoke; then an Egyptian test stand where the new engine fades to a wireframe",
     "vo": [("build", [("सपना था आवाज़ से", "SAPNA THA AWAAZ SE"),
                       ("दोगुनी रफ़्तार।", "DOGUNI RAFTAAR")]),
            ("punch", [("पर कमज़ोर इंजन ने", "PAR KAMZOR ENGINE NE"),
                       ("इसे सुपरसोनिक", "ISE SUPERSONIC"),
                       ("नहीं बनने दिया।", "NAHI BANNE DIYA")]),
            ("low", [("मिस्र वाला नया इंजन भी", "MISR WALA NAYA ENGINE BHI"),
                     ("अधूरा रह गया।", "ADHURA REH GAYA")])]},

    # 00:23-00:30 why it died: the choices
    {"key": "policy", "accent": SAFFRON, "text": "",
     "visual": "An engineer holds out a better-engine blueprint, the official at the desk waves it away beside an "
               "empty cash box while foreign jets fly past the window; then a tarp is pulled over a parked Marut",
     "vo": [("tell", [("बेहतर इंजन पर", "BEHTAR ENGINE PAR"),
                      ("पैसा नहीं लगा", "PAISA NAHI LAGA"),
                      ("और विदेशी जेट", "AUR VIDESHI JET"),
                      ("आसान रास्ता बने।", "AASAAN RAASTA BANE")]),
            ("low", [("अस्सी के दशक तक", "80 KE DASHAK TAK"),
                     ("मरुत रिटायर हो गया।", "MARUT RETIRE HO GAYA")])]},

    # 00:30-00:39 debate -> payoff in the last line -> loop into the hook
    {"key": "debate_loop", "accent": GOLD, "text": "",
     "visual": "A balance scale: an engine on one pan, a policy file on the other, rocking; the engineer and the "
               "official on either side. Payoff: a Tejas with its American engine highlighted. Loop: fade back to the "
               "scene-1 hangar",
     "vo": [("ask", [("तो गलती इंजन की थी", "TO GALTI ENGINE KI THI"),
                     ("या सरकार की सोच की।", "YA SARKAR KI SOCH KI?")]),
            ("punch", [("आज भी तेजस", "AAJ BHI TEJAS"),
                       ("अमेरिकी इंजन से उड़ता है।", "AMERICAN ENGINE SE UDTA HAI")]),
            ("low", [("ये कहानी", "YE KAHANI"),
                     ("वहीं से शुरू हुई जब", "WAHIN SE SHURU HUI JAB")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "BHARAT": SAFFRON, "PEHLA": SAFFRON, "DESI": SAFFRON, "JET": CYAN, "FIGHTER": CYAN, "JUNG": FIRE,
    "JEETKAR": INDIA_GREEN, "BAND": RED, "1961": GOLD, "MARUT": GOLD, "GERMANY": GOLD, "KURT": GOLD, "TANK": GOLD,
    "HAL": SAFFRON, "1971": FIRE, "LONGEWALA": FIRE, "DUSHMAN": RED, "TANKON": RED, "TOOT": FIRE, "PADA": FIRE,
    "AWAAZ": CYAN, "DOGUNI": CYAN, "RAFTAAR": CYAN, "KAMZOR": RED, "ENGINE": CYAN, "NAHI": RED, "SAPNA": GOLD, "SUPERSONIC": CYAN,
    "MISR": GOLD, "ADHURA": RED, "BEHTAR": CYAN, "PAISA": GOLD, "VIDESHI": RED, "AASAAN": GOLD, "80": GOLD,
    "DASHAK": GOLD, "RETIRE": RED, "GALTI": RED, "SARKAR": SAFFRON, "SOCH": SAFFRON, "TEJAS": SAFFRON,
    "AMERICAN": CYAN, "KAHANI": GOLD, "SHURU": GOLD,
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".")] = HOT[_k]


def mix(a, b, u):
    u = clamp(u)
    return tuple(x + (y - x) * u for x, y in zip(a, b))


def at(scene, key, frac, d):
    """Start of the first caption containing key, or frac of the scene when there are no captions (preview)."""
    return scene.cue(key, frac * d)


# ============================================================ the Marut (side view, nose to +x)

FUSE = [(305, 2), (250, -12), (190, -26), (120, -34), (0, -36), (-150, -36), (-250, -30), (-292, -22),
        (-292, 20), (-240, 30), (-100, 36), (100, 34), (190, 24), (250, 12)]


def marut(ctx, x, y, s, ang=0.0, exhaust=0.0, smoke=0.0, garland=0.0, gear=False, t=0.0, outline=None, a=1.0):
    """HF-24 Marut in profile: long pointed nose, bubble canopy, swept wings and fin, twin jet pipes, IAF roundel
    and fin flash in 1971 camouflage. outline=colour draws only white blueprint lines. Balanced save/restore."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(s, s)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    far_wing = [(10, -20), (-90, -20), (-160, -58), (-122, -58)]
    near_wing = [(40, 8), (-120, 10), (-205, 60), (-155, 62)]
    fin = [(-175, -34), (-250, -128), (-292, -132), (-286, -34)]
    stab = [(-225, 14), (-292, 14), (-330, 50), (-296, 52)]

    if outline is not None:
        for shape in (far_wing, FUSE, near_wing, fin, stab):
            ctx.move_to(*shape[0])
            for p in shape[1:]:
                ctx.line_to(*p)
            ctx.close_path()
            rgba(ctx, outline, a)
            ctx.set_line_width(3 / s)
            ctx.stroke()
        ctx.move_to(150, -30)
        ctx.curve_to(130, -68, 70, -70, 50, -34)
        rgba(ctx, outline, a)
        ctx.stroke()
        for k in range(-260, 300, 60):   # station lines
            line(ctx, [(k, -46), (k, 46)], outline, 1 / s, 0.35 * a)
        ctx.restore()
        return

    if exhaust > 0:   # jet wash: hot flame core
        g = cairo.LinearGradient(-300, 0, -300 - 230 * exhaust, 0)
        g.add_color_stop_rgba(0, 1, 0.92, 0.6, 0.95 * a)
        g.add_color_stop_rgba(0.35, 1, 0.5, 0.12, 0.75 * a)
        g.add_color_stop_rgba(1, 0.8, 0.2, 0.0, 0)
        ctx.set_source(g)
        ctx.move_to(-292, -16)
        ctx.line_to(-300 - 230 * exhaust, 0 + 4 * math.sin(t * 40))
        ctx.line_to(-292, 16)
        ctx.close_path()
        ctx.fill()
    if smoke > 0:     # a coughing engine: grey puffs drifting back
        for k in range(7):
            u = ((t * 1.6 + k / 7) % 1.0)
            px = -310 - 260 * u
            py = -10 * math.sin(k * 1.7) - 40 * u
            circle(ctx, px, py, 16 + 46 * u, (0.35, 0.35, 0.36), smoke * 0.55 * (1 - u) * a)

    poly(ctx, far_wing, CAMO_B, a)
    poly(ctx, stab[:2] + [(-320, -20), (-290, -20)], CAMO_B, a)   # far tailplane
    poly(ctx, FUSE, CAMO_A, a)
    ctx.save()                                                     # camouflage blotches clipped to the body
    ctx.move_to(*FUSE[0])
    for p in FUSE[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    ctx.clip()
    for k in range(9):
        ell(ctx, -260 + 62 * k, -18 + 22 * math.sin(k * 2.1), 38, 16)
        rgba(ctx, CAMO_B if k % 2 else CAMO_C, 0.8 * a)
        ctx.fill()
    ctx.rectangle(-300, 14, 620, 30)                               # pale belly
    rgba(ctx, hexc("#B9BDB0"), 0.85 * a)
    ctx.fill()
    ctx.restore()
    ctx.move_to(*FUSE[0])
    for p in FUSE[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    rgba(ctx, (0.12, 0.13, 0.1), a)
    ctx.set_line_width(3 / s)
    ctx.stroke()
    poly(ctx, [(305, 2), (262, -9), (262, 10)], hexc("#2B2E28"), a)   # radome tip
    poly(ctx, fin, CAMO_A, a)
    for k, c in enumerate((SAFFRON, WHITE, INDIA_GREEN)):          # fin flash
        x0 = -268 + k * 9
        poly(ctx, [(x0, -100), (x0 + 9, -100), (x0 + 9 + 10, -62), (x0 + 10, -62)], c, a)
    poly(ctx, [(60, 4), (100, 0), (102, 26), (58, 26)], hexc("#1A1C18"), a)   # intake
    ctx.move_to(150, -30)                                          # canopy
    ctx.curve_to(130, -68, 70, -70, 50, -34)
    ctx.close_path()
    g = cairo.LinearGradient(60, -66, 130, -34)
    g.add_color_stop_rgba(0, 0.75, 0.88, 0.95, a)
    g.add_color_stop_rgba(1, 0.2, 0.35, 0.45, a)
    ctx.set_source(g)
    ctx.fill_preserve()
    rgba(ctx, (0.1, 0.1, 0.1), a)
    ctx.set_line_width(2.5 / s)
    ctx.stroke()
    circle(ctx, 98, -46, 10, (0.12, 0.12, 0.14), 0.8 * a)          # pilot helmet
    poly(ctx, near_wing, CAMO_A, a)
    line(ctx, [(-120, 10), (-155, 62)], (0.15, 0.16, 0.13), 2.5 / s, a)
    poly(ctx, stab, CAMO_A, a)
    for dy in (-12, 10):                                           # twin jet pipes
        rrect(ctx, -300, dy - 8, 14, 16, 4)
        rgba(ctx, hexc("#2A2A2A"), a)
        ctx.fill()
    circle(ctx, -60, 0, 17, SAFFRON, a)                            # IAF roundel
    circle(ctx, -60, 0, 11, WHITE, a)
    circle(ctx, -60, 0, 5, INDIA_GREEN, a)
    if gear:
        for gx, gl in ((200, 41), (-70, 38)):
            line(ctx, [(gx, 30), (gx, 30 + gl)], (0.2, 0.2, 0.2), 6 / s, a)
            circle(ctx, gx, 34 + gl, 13 if gx < 0 else 10, (0.08, 0.08, 0.08), a)
    if garland > 0:                                                # victory garland under the nose
        for k in range(17):
            u = k / 16
            gx = 225 - 120 * u
            gy = 24 + 70 * math.sin(math.pi * u) * garland
            circle(ctx, gx, gy, 9, MARIGOLD if k % 2 else MARIGOLD_2, a)
    ctx.restore()


# ============================================================ people (feet at (x, y), ~560 units tall, face +x)

OUTFIT = {
    "designer": {"top": hexc("#5C6470"), "legs": hexc("#454B55"), "skin": hexc("#E6C1A4"), "hair": hexc("#E8E8E2"),
                 "glasses": True, "tie": hexc("#7A1F1F"), "bald": True},
    "engineer": {"top": hexc("#EFEDE2"), "legs": hexc("#2E3440"), "skin": hexc("#9C6B45"), "hair": hexc("#141414")},
    "engineer2": {"top": hexc("#BFD7EA"), "legs": hexc("#3B3F47"), "skin": hexc("#8A5A38"), "hair": hexc("#1C1C1C"),
                  "glasses": True},
    "official": {"top": hexc("#8E8A78"), "legs": hexc("#8E8A78"), "skin": hexc("#A87850"), "hair": hexc("#2A2A2A"),
                 "glasses": True, "moustache": True},
    "pilot": {"top": hexc("#5E6B3A"), "legs": hexc("#5E6B3A"), "skin": hexc("#A06A44"), "hair": hexc("#151515"),
              "helmet": True},
    "crew": {"top": hexc("#2F4E7A"), "legs": hexc("#2F4E7A"), "skin": hexc("#93613E"), "hair": hexc("#151515"),
             "cap": hexc("#24405F")},
}
POSES = {   # (near upper, near fore, far upper, far fore) - radians from straight down, + = forward / up
    "stand": (0.15, 0.10, -0.15, -0.10),
    "salute": (1.95, 2.30, -0.12, -0.10),
    "cheer": (2.75, 0.30, 2.55, 0.25),
    "point": (1.75, 0.10, -0.15, -0.20),
    "write": (1.10, 0.95, 0.80, 1.10),
    "pull": (2.85, 0.05, 2.65, 0.10),
    "plead": (1.45, 0.30, 1.30, 0.40),
    "wave_off": (1.20, 1.60, -0.10, -0.10),
    "think": (0.55, 2.55, 0.35, 1.40),
    "shrug": (0.55, 1.75, -0.55, -1.75),
    "hold": (0.95, 1.05, 0.75, 1.15),
}


def _limb(ctx, x0, y0, a1, l1, a2, l2, c, w, a):
    x1, y1 = x0 + l1 * math.sin(a1), y0 + l1 * math.cos(a1)
    x2, y2 = x1 + l2 * math.sin(a1 + a2), y1 + l2 * math.cos(a1 + a2)
    line(ctx, [(x0, y0), (x1, y1)], c, w, a)
    line(ctx, [(x1, y1), (x2, y2)], c, w * 0.9, a)
    return x2, y2


def person(ctx, x, y, s, t, kind="engineer", pose="stand", flip=False, prop=None, a=1.0):
    """A civilian / aircrew figure. prop: 'pencil', 'blueprint', 'file', 'clipboard'. Every save() is restored."""
    o = OUTFIT[kind]
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(-s if flip else s, s)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ell(ctx, 0, 6, 78, 13)
    rgba(ctx, (0, 0, 0), 0.4 * a)
    ctx.fill()
    for side in (-1, 1):
        fx = side * 26
        line(ctx, [(side * 20, -235), (fx, -22)], o["legs"], 40, a)
        rrect(ctx, fx - 18, -26, 46, 24, 9)
        rgba(ctx, hexc("#17140F"), a)
        ctx.fill()
    poly(ctx, [(-60, -440), (60, -440), (52, -228), (-52, -228)], o["top"], a)
    if kind == "designer":   # jacket lapels, shirt and tie, black-red-gold pin
        poly(ctx, [(-12, -440), (12, -440), (0, -380)], (0.95, 0.95, 0.93), a)
        poly(ctx, [(-5, -430), (5, -430), (8, -320), (0, -305), (-8, -320)], o["tie"], a)
        line(ctx, [(-14, -440), (-30, -330)], hexc("#3F454E"), 4, a)
        line(ctx, [(14, -440), (30, -330)], hexc("#3F454E"), 4, a)
        for k, c in enumerate(((0, 0, 0), hexc("#DD0000"), hexc("#FFCE00"))):
            ctx.rectangle(30, -410 + k * 5, 16, 5)
            rgba(ctx, c, a)
            ctx.fill()
    elif kind == "official":   # safari suit pockets
        for px in (-34, 34):
            rrect(ctx, px - 16, -400, 32, 30, 4)
            rgba(ctx, hexc("#77735F"), a)
            ctx.fill()
        line(ctx, [(0, -440), (0, -235)], hexc("#77735F"), 3, a)
    elif kind == "pilot":      # flight suit zip + patch
        line(ctx, [(4, -440), (4, -240)], hexc("#3E4728"), 4, a)
        circle(ctx, -30, -390, 10, SAFFRON, a)
        circle(ctx, -30, -390, 4, INDIA_GREEN, a)
    elif kind == "crew":
        rrect(ctx, -30, -400, 60, 40, 6)
        rgba(ctx, hexc("#24405F"), a)
        ctx.fill()

    nu, nf, fu, ff = POSES.get(pose, POSES["stand"])
    if pose == "cheer":
        nf += 0.25 * math.sin(t * 9)
    if pose == "wave_off":
        nf += 0.35 * math.sin(t * 7)
    if pose == "pull":
        tug = 0.12 * math.sin(t * 6)
        nu, fu = nu + tug, fu + tug
    sleeve_far = tuple(c * 0.82 for c in o["top"])
    lx, ly = _limb(ctx, -54, -425, fu, 100, ff, 92, sleeve_far, 28, a)
    circle(ctx, lx, ly, 14, tuple(c * 0.85 for c in o["skin"]), a)
    rx, ry = _limb(ctx, 54, -425, nu, 100, nf, 92, o["top"], 30, a)
    circle(ctx, rx, ry, 15, o["skin"], a)
    if prop == "pencil":
        line(ctx, [(rx, ry), (rx + 26, ry + 22)], hexc("#F2C230"), 6, a)
    elif prop == "blueprint":
        ctx.save()
        ctx.translate((rx + lx) / 2 + 30, (ry + ly) / 2 - 20)
        ctx.rotate(-0.12)
        rrect(ctx, -10, -70, 150, 110, 6)
        rgba(ctx, BLUEPRINT, a)
        ctx.fill()
        line(ctx, [(10, -20), (120, -30), (110, -10), (20, 0)], WHITE, 3, 0.85 * a)
        circle(ctx, 40, -44, 14, WHITE, 0.0)
        ctx.arc(40, -44, 14, 0, math.tau)
        rgba(ctx, WHITE, 0.8 * a)
        ctx.set_line_width(3)
        ctx.stroke()
        ctx.restore()
    elif prop in ("file", "clipboard"):
        rrect(ctx, rx - 10, ry - 70, 90, 110, 6)
        rgba(ctx, hexc("#C9A86A") if prop == "file" else hexc("#6B4A2B"), a)
        ctx.fill()
        if prop == "clipboard":
            rrect(ctx, rx, ry - 58, 70, 88, 3)
            rgba(ctx, WHITE, a)
            ctx.fill()
        else:
            line(ctx, [(rx + 35, ry - 70), (rx + 35, ry + 40)], RED, 5, a)   # red tape

    line(ctx, [(0, -440), (0, -466)], tuple(c * 0.85 for c in o["skin"]), 26, a)
    ctx.save()
    tilt = {"salute": -0.05, "cheer": -0.25, "think": 0.12, "shrug": 0.1, "point": -0.1, "pull": -0.3}.get(pose, 0.0)
    ctx.translate(0, -478)
    ctx.rotate(tilt)
    ell(ctx, 0, -36, 44, 50)
    rgba(ctx, o["skin"], a)
    ctx.fill()
    ell(ctx, 42, -30, 9, 11)                                       # nose
    rgba(ctx, tuple(c * 0.9 for c in o["skin"]), a)
    ctx.fill()
    circle(ctx, -26, -34, 9, tuple(c * 0.85 for c in o["skin"]), a)   # ear
    if o.get("helmet"):
        ctx.move_to(-50, -40)
        ctx.curve_to(-52, -112, 50, -112, 50, -52)
        ctx.close_path()
        rgba(ctx, hexc("#E9E9E4"), a)
        ctx.fill()
        rrect(ctx, 10, -66, 40, 14, 4)
        rgba(ctx, hexc("#2C3E50"), a)
        ctx.fill()
    elif o.get("bald"):                                            # receding white hair at the back and sides
        ctx.move_to(-44, -26)
        ctx.curve_to(-52, -70, -20, -92, 6, -88)
        ctx.line_to(-6, -70)
        ctx.curve_to(-26, -66, -34, -46, -30, -26)
        ctx.close_path()
        rgba(ctx, o["hair"], a)
        ctx.fill()
    else:
        ctx.move_to(-46, -30)
        ctx.curve_to(-50, -96, 40, -100, 44, -56)
        ctx.curve_to(20, -70, -10, -68, -30, -50)
        ctx.close_path()
        rgba(ctx, o["hair"], a)
        ctx.fill()
    if o.get("cap"):
        ctx.move_to(-46, -56)
        ctx.curve_to(-40, -100, 40, -100, 44, -60)
        ctx.close_path()
        rgba(ctx, o["cap"], a)
        ctx.fill()
        rrect(ctx, 20, -64, 46, 10, 4)
        rgba(ctx, o["cap"], a)
        ctx.fill()
    blink = 0.15 if (t % 3.3) < 0.12 else 1.0
    for ex in (14, 32):
        ell(ctx, ex, -42, 4.5, 4.5 * blink)
        rgba(ctx, (0.06, 0.05, 0.05), a)
        ctx.fill()
    if o.get("glasses"):
        for ex in (14, 32):
            ctx.arc(ex, -42, 10, 0, math.tau)
            rgba(ctx, (0.1, 0.1, 0.1), a)
            ctx.set_line_width(2.5)
            ctx.stroke()
        line(ctx, [(-26, -44), (4, -44)], (0.1, 0.1, 0.1), 2.5, a)
    line(ctx, [(6, -60), (22, -63)], (0.15, 0.1, 0.08), 3.5, a)   # brows
    line(ctx, [(26, -63), (40, -60)], (0.15, 0.1, 0.08), 3.5, a)
    if pose == "think" or pose == "shrug":
        line(ctx, [(6, -60), (22, -56)], (0.15, 0.1, 0.08), 3.5, a)
    if o.get("moustache"):
        line(ctx, [(10, -20), (40, -16)], (0.15, 0.1, 0.08), 6, a)
    if pose in ("cheer", "plead", "point"):
        ell(ctx, 26, -10, 8, 8 if pose == "cheer" else 5)
        rgba(ctx, (0.3, 0.06, 0.06), a)
        ctx.fill()
    elif pose == "shrug":
        line(ctx, [(16, -8), (34, -12)], (0.3, 0.12, 0.1), 3, a)
    else:
        line(ctx, [(14, -10), (34, -10)], (0.3, 0.12, 0.1), 3, a)
    ctx.restore()
    ctx.restore()


# ============================================================ worlds and props

def hangar(ctx, t, shutter=0.0, roof_flag=True):
    """Hangar front at dusk: twilight sky, distant hills and runway lights, a lit interior with the garlanded Marut,
    and a slatted shutter coming down to `shutter` (0..1) of the opening."""
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    g.add_color_stop_rgb(0.0, *hexc("#141B33"))
    g.add_color_stop_rgb(0.45, *hexc("#4A3A5C"))
    g.add_color_stop_rgb(0.8, *hexc("#C9714A"))
    g.add_color_stop_rgb(1.0, *hexc("#F2A65A"))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    glow(ctx, 880, 420, 260, hexc("#FFB45C"), 0.35)
    circle(ctx, 880, 420, 46, hexc("#FFD9A0"), 0.9)
    for i in range(40):
        circle(ctx, rnd(i, 3) * W, 190 + rnd(i, 4) * 200, 1.3, WHITE, 0.35 * abs(math.sin(t + i)))
    # hangar body: curved roof, walls and the big opening
    ctx.move_to(-20, 380)
    ctx.curve_to(240, 210, 840, 210, 1100, 380)
    ctx.line_to(1100, GROUND + 40)
    ctx.line_to(-20, GROUND + 40)
    ctx.close_path()
    rgba(ctx, hexc("#3B4046"))
    ctx.fill()
    for k in range(12):
        x = 40 + k * 92
        line(ctx, [(x, 300 + 40 * abs(math.cos(k / 11 * math.pi))), (x, GROUND)], hexc("#2E3236"), 4)
    ox0, ox1, oy0 = 80, 1000, 420
    g = cairo.LinearGradient(0, oy0, 0, GROUND)
    g.add_color_stop_rgb(0, *hexc("#2A2620"))
    g.add_color_stop_rgb(0.6, *hexc("#6B5536"))
    g.add_color_stop_rgb(1, *hexc("#A8875A"))
    ctx.rectangle(ox0, oy0, ox1 - ox0, GROUND - oy0)
    ctx.set_source(g)
    ctx.fill()
    for lx in (250, 540, 830):   # roof lamps + cones of light
        ctx.move_to(lx - 20, oy0 + 10)
        ctx.line_to(lx - 170, GROUND)
        ctx.line_to(lx + 170, GROUND)
        ctx.line_to(lx + 20, oy0 + 10)
        ctx.close_path()
        rgba(ctx, hexc("#FFE2A8"), 0.08)
        ctx.fill()
        circle(ctx, lx, oy0 + 14, 10, hexc("#FFE9C0"))
    if roof_flag:
        flag(ctx, 548, 222, 120, 76, "in", t, pole=40)
    ctx.rectangle(0, GROUND - 6, W, H - GROUND + 6)   # concrete apron down to the frame edge
    rgba(ctx, hexc("#3A3834"))
    ctx.fill()
    marut(ctx, 560, GROUND - 100, 1.18, garland=1.0, gear=True, t=t)
    if shutter > 0:   # slats rolling down over the opening
        hgt = (GROUND - oy0) * shutter
        ctx.rectangle(ox0, oy0, ox1 - ox0, hgt)
        rgba(ctx, hexc("#7C838A"))
        ctx.fill()
        for k in range(int(hgt // 26) + 1):
            line(ctx, [(ox0, oy0 + k * 26), (ox1, oy0 + k * 26)], hexc("#555B61"), 3)
        line(ctx, [(ox0, oy0 + hgt), (ox1, oy0 + hgt)], hexc("#2E3236"), 10)
    line(ctx, [(ox0, oy0), (ox1, oy0)], hexc("#24282C"), 16)
    line(ctx, [(ox0, oy0), (ox0, GROUND)], hexc("#24282C"), 12)
    line(ctx, [(ox1, oy0), (ox1, GROUND)], hexc("#24282C"), 12)


def desert(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    g.add_color_stop_rgb(0.0, *hexc("#2B2448"))
    g.add_color_stop_rgb(0.5, *hexc("#B4566A"))
    g.add_color_stop_rgb(0.85, *hexc("#F29E5C"))
    g.add_color_stop_rgb(1.0, *hexc("#F7C77A"))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    glow(ctx, 760, 760, 300, hexc("#FFC46B"), 0.45)
    circle(ctx, 760, 760, 70, hexc("#FFE0A0"), 0.95)
    for layer, (base, amp, col) in enumerate(((880, 40, "#C98A58"), (960, 30, "#D9A066"), (1030, 22, SAND))):
        ctx.move_to(0, GROUND + 40)
        for x in range(0, W + 30, 30):
            ctx.line_to(x, base + amp * math.sin(x * 0.006 + layer * 1.7) + 0.4 * amp * math.sin(x * 0.019))
        ctx.line_to(W, GROUND + 40)
        ctx.close_path()
        rgba(ctx, hexc(col) if isinstance(col, str) else col)
        ctx.fill()
    for k in range(10):   # scrub bushes
        bx = 40 + k * 113 + 20 * math.sin(k)
        ell(ctx, bx, 1090 + 10 * math.sin(k * 3), 26, 12)
        rgba(ctx, hexc("#6E6B3A"), 0.8)
        ctx.fill()


def tank(ctx, x, y, s, t, wreck=0.0, moving=True):
    """Generic tank facing left (no national markings); wreck 0..1 blackens it and droops the barrel."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    body = mix(hexc("#8A7A55"), hexc("#2A2622"), wreck)
    dark = mix(hexc("#5E5338"), hexc("#151311"), wreck)
    rrect(ctx, -130, -60, 260, 60, 22)   # tracks
    rgba(ctx, dark)
    ctx.fill()
    for k in range(6):
        circle(ctx, -100 + k * 40, -28, 17, hexc("#2A2620"))
        ang = (-t * 6 if moving and wreck == 0 else 0) + k
        line(ctx, [(-100 + k * 40, -28), (-100 + k * 40 + 12 * math.cos(ang), -28 + 12 * math.sin(ang))],
             hexc("#6A6050"), 3)
    poly(ctx, [(-140, -60), (130, -60), (110, -100), (-120, -100)], body)
    poly(ctx, [(-60, -100), (60, -100), (40, -140), (-40, -140)], body)
    droop = 0.3 * wreck
    line(ctx, [(-50, -122), (-50 - 150 * math.cos(droop), -122 + 150 * math.sin(droop))], dark, 12)
    ctx.restore()
    if wreck > 0:   # rising black smoke
        for k in range(8):
            u = (t * 0.5 + k / 8) % 1.0
            circle(ctx, x + 20 * s * math.sin(k + t), y - 140 * s - 300 * u * s, (24 + 70 * u) * s,
                   (0.12, 0.11, 0.1), 0.55 * (1 - u) * min(1.0, wreck * 2))


def sandbags(ctx, x0, x1, y):
    for row in range(3):
        for k in range(int((x1 - x0) / 60) + 1):
            bx = x0 + k * 60 + (30 if row % 2 else 0)
            if bx > x1:
                continue
            ell(ctx, bx, y - 20 - row * 34, 34, 18)
            rgba(ctx, mix(SAND_DK, hexc("#8C6A3E"), row / 3))
            ctx.fill()


def rocket(ctx, x0, y0, x1, y1, u):
    """A rocket fired from (x0, y0) toward (x1, y1); u 0..1 is its flight. Smoke trail behind, nose ahead."""
    if not 0 < u < 1:
        return
    px, py = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    line(ctx, [(x0 + (x1 - x0) * max(0, u - 0.35), y0 + (y1 - y0) * max(0, u - 0.35)), (px, py)],
         (0.85, 0.85, 0.82), 6, 0.6)
    ang = math.atan2(y1 - y0, x1 - x0)
    ctx.save()
    ctx.translate(px, py)
    ctx.rotate(ang)
    rrect(ctx, -22, -4, 30, 8, 3)
    rgba(ctx, WHITE)
    ctx.fill()
    poly(ctx, [(8, -4), (20, 0), (8, 4)], RED)
    glow(ctx, -26, 0, 20, FIRE, 0.9)
    ctx.restore()


def sky(ctx, t, warm=0.0):
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    g.add_color_stop_rgb(0.0, *mix(hexc("#0E2A55"), hexc("#3A2A4A"), warm))
    g.add_color_stop_rgb(0.6, *mix(hexc("#2F6DA8"), hexc("#B8667A"), warm))
    g.add_color_stop_rgb(1.0, *mix(hexc("#9FCBEA"), hexc("#F2B077"), warm))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    for k in range(6):   # drifting cloud banks
        cx = (rnd(k, 21) * (W + 600) - t * (30 + 20 * rnd(k, 22))) % (W + 600) - 300
        cy = 300 + rnd(k, 23) * 700
        for j in range(4):
            ell(ctx, cx + j * 70, cy + 12 * math.sin(j * 2 + k), 90 - 10 * j, 34)
            rgba(ctx, WHITE, 0.16)
            ctx.fill()


def mach_gauge(ctx, cx, cy, r, value, ghost=0.0, alarm=0.0, t=0.0):
    """Mach dial 0..2: red barrier mark at 1, gold target at 2, a ghost 'dream' needle and the real needle."""
    a0, a1 = math.radians(150), math.radians(390)

    def ang(v):
        return a0 + (a1 - a0) * clamp(v / 2.0)

    circle(ctx, cx, cy, r + 14, (0.03, 0.04, 0.03), 0.9)
    ctx.arc(cx, cy, r, a0, a1)
    rgba(ctx, PAL["ui"], 0.8)
    ctx.set_line_width(8)
    ctx.stroke()
    ctx.arc(cx, cy, r, ang(1.0), a1)
    rgba(ctx, GOLD, 0.5)
    ctx.set_line_width(8)
    ctx.stroke()
    for k in range(11):
        v = k * 0.2
        aa = ang(v)
        inner = r - (30 if k % 5 == 0 else 16)
        line(ctx, [(cx + inner * math.cos(aa), cy + inner * math.sin(aa)),
                   (cx + r * math.cos(aa), cy + r * math.sin(aa))], PAL["ink"], 4 if k % 5 == 0 else 2)
    for v, lab in ((0, "0"), (1, "1"), (2, "2")):
        aa = ang(v)
        text(ctx, lab, cx + (r - 62) * math.cos(aa), cy + (r - 62) * math.sin(aa), 44,
             RED if v == 1 else (GOLD if v == 2 else PAL["ink"]), font=CAPTION_FONT, bold=False)
    text(ctx, "MACH", cx, cy + r * 0.45, 40, PAL["ui"], font=CAPTION_FONT, bold=False)
    aa = ang(1.0)
    pulse = 0.5 + 0.5 * math.sin(t * 10)
    circle(ctx, cx + r * math.cos(aa), cy + r * math.sin(aa), 16 + 10 * alarm * pulse, RED, 0.6 + 0.4 * alarm)
    if ghost > 0:
        ga = ang(2.0 * ghost)
        line(ctx, [(cx, cy), (cx + (r - 20) * math.cos(ga), cy + (r - 20) * math.sin(ga))], GOLD, 10, 0.45)
    na = ang(value)
    line(ctx, [(cx, cy), (cx + (r - 18) * math.cos(na), cy + (r - 18) * math.sin(na))], WHITE, 10)
    circle(ctx, cx, cy, 18, WHITE)


def jet_engine(ctx, x, y, s, solid=1.0, t=0.0):
    """Turbojet on a test stand; solid 1 = finished metal, 0 = only a faint wireframe (an unfinished project)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    line(ctx, [(-150, 60), (-170, 170)], STEEL_DK, 14)   # stand legs
    line(ctx, [(150, 60), (170, 170)], STEEL_DK, 14)
    line(ctx, [(-170, 170), (170, 170)], STEEL_DK, 10)
    body = [(-220, -60), (160, -70), (230, -40), (230, 40), (160, 70), (-220, 60)]
    if solid > 0.01:
        g = cairo.LinearGradient(0, -70, 0, 70)
        g.add_color_stop_rgba(0, 0.75, 0.78, 0.8, solid)
        g.add_color_stop_rgba(0.5, 0.45, 0.48, 0.5, solid)
        g.add_color_stop_rgba(1, 0.25, 0.27, 0.3, solid)
        ctx.move_to(*body[0])
        for p in body[1:]:
            ctx.line_to(*p)
        ctx.close_path()
        ctx.set_source(g)
        ctx.fill()
        ell(ctx, -220, 0, 22, 60)
        rgba(ctx, (0.1, 0.1, 0.12), solid)
        ctx.fill()
        for k in range(6):
            circle(ctx, -220, 0, 10 + k * 8, STEEL, 0.0)
    ctx.move_to(*body[0])
    for p in body[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    rgba(ctx, CYAN, 0.8)
    ctx.set_line_width(3)
    ctx.stroke()
    for k in range(-180, 220, 40):
        line(ctx, [(k, -64), (k, 64)], CYAN, 1.5, 0.35 + 0.4 * (1 - solid))
    ctx.restore()


def pyramids(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    g.add_color_stop_rgb(0.0, *hexc("#1E2547"))
    g.add_color_stop_rgb(0.55, *hexc("#8E5A6E"))
    g.add_color_stop_rgb(1.0, *hexc("#F0B070"))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    glow(ctx, 220, 640, 220, hexc("#FFC46B"), 0.4)
    circle(ctx, 220, 640, 48, hexc("#FFE0A0"), 0.9)
    for px, ph, pw in ((640, 330, 300), (900, 250, 230), (420, 190, 170)):
        poly(ctx, [(px - pw, 960), (px, 960 - ph), (px + pw, 960)], hexc("#B98252"))
        poly(ctx, [(px, 960 - ph), (px + pw, 960), (px + pw * 0.15, 960)], hexc("#8E5E36"))
    ctx.rectangle(0, 940, W, GROUND - 900)
    rgba(ctx, SAND)
    ctx.fill()


def egypt_flag(ctx, x, y, w, h):
    for k, c in enumerate((hexc("#CE1126"), WHITE, (0.0, 0.0, 0.0))):
        ctx.rectangle(x, y + k * h / 3, w, h / 3 + 1)
        rgba(ctx, c)
        ctx.fill()
    circle(ctx, x + w / 2, y + h / 2, h * 0.11, hexc("#C09300"))


def office(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    g.add_color_stop_rgb(0, *hexc("#3E4A3A"))
    g.add_color_stop_rgb(1, *hexc("#5B6650"))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    ctx.rectangle(0, 1000, W, GROUND - 980)
    rgba(ctx, hexc("#4A3B2C"))
    ctx.fill()
    for k in range(10):   # floor boards
        line(ctx, [(k * 120, 1000), (k * 120 - 60, GROUND + 40)], hexc("#3A2E22"), 2)


def balance(ctx, cx, cy, tilt, t):
    """Balance scale: engine on the left pan, a policy file on the right pan."""
    line(ctx, [(cx, cy), (cx, cy + 520)], hexc("#B08D57"), 16)
    poly(ctx, [(cx - 120, cy + 560), (cx + 120, cy + 560), (cx + 70, cy + 520), (cx - 70, cy + 520)], hexc("#8C6D3F"))
    circle(ctx, cx, cy, 22, GOLD)
    half = 300
    lx, ly = cx - half * math.cos(tilt), cy - half * math.sin(tilt)
    rx, ry = cx + half * math.cos(tilt), cy + half * math.sin(tilt)
    line(ctx, [(lx, ly), (rx, ry)], hexc("#D4B06A"), 14)
    for px, py, side in ((lx, ly, -1), (rx, ry, 1)):
        pan_y = py + 230
        line(ctx, [(px, py), (px - 110, pan_y)], hexc("#C9A86A"), 3)
        line(ctx, [(px, py), (px + 110, pan_y)], hexc("#C9A86A"), 3)
        ctx.move_to(px - 130, pan_y)
        ctx.curve_to(px - 100, pan_y + 50, px + 100, pan_y + 50, px + 130, pan_y)
        ctx.close_path()
        rgba(ctx, hexc("#D4B06A"))
        ctx.fill()
        if side < 0:
            jet_engine(ctx, px, pan_y - 46, 0.36, solid=1.0, t=t)
        else:
            ctx.save()
            ctx.translate(px, pan_y - 50)
            ctx.rotate(-0.08)
            rrect(ctx, -80, -50, 160, 100, 8)
            rgba(ctx, hexc("#C9A86A"))
            ctx.fill()
            rrect(ctx, -80, -50, 160, 22, 6)
            rgba(ctx, hexc("#A88A50"))
            ctx.fill()
            line(ctx, [(0, -50), (0, 50)], RED, 7)
            circle(ctx, 0, 10, 16, RED)
            ctx.restore()


# ============================================================ scenes

class ShutterHook(Cued):
    """Garlanded Marut in the hangar; the shutter starts down on BAND."""

    def events(self, d):
        return [(0.1, "whoosh"), (at(self, "BAND", 0.55, d) + 0.1, "thud")]

    def draw(self, ctx, t, d):
        tb = at(self, "BAND", 0.55, d)
        shut = 0.62 * seg01(t, tb - 0.2, tb + 1.4)
        hangar(ctx, t, shutter=shut)
        person(ctx, 140, GROUND, 0.62, t, "pilot", "salute")
        person(ctx, 1000, GROUND, 0.6, t, "crew", "pull" if shut > 0 else "stand", flip=True)
        if shut > 0:   # the shutter chain the crewman hauls
            line(ctx, [(985, GROUND - 330), (985, 420)], (0.6, 0.6, 0.6), 4)


class Birth(Cued):
    """1961 sepia take-off, then Kurt Tank at the HAL drafting table."""

    def events(self, d):
        return [(0.2, "whoosh"), (at(self, "GERMANY", 0.45, d), "pop")]

    def draw(self, ctx, t, d):
        tg = at(self, "GERMANY", 0.45, d)
        if t < tg + 0.3:
            self.takeoff(ctx, t)
            sep = cairo.LinearGradient(0, 0, 0, H)   # sepia film wash + scratches
            sep.add_color_stop_rgba(0, 0.45, 0.32, 0.15, 0.35)
            sep.add_color_stop_rgba(1, 0.3, 0.2, 0.08, 0.35)
            ctx.rectangle(0, 0, W, H)
            ctx.set_source(sep)
            ctx.fill()
            for k in range(3):
                sx = rnd(int(t * 12) + k, 5) * W
                line(ctx, [(sx, 0), (sx + 6, GROUND)], (1, 0.95, 0.85), 1.5, 0.25)
        if t >= tg:
            a = clamp((t - tg) / 0.3)
            ctx.push_group()
            self.drafting(ctx, t)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(a)

    def takeoff(self, ctx, t):
        sky(ctx, t, warm=0.5)
        ctx.move_to(0, GROUND)
        ctx.line_to(W, GROUND)
        ctx.line_to(W, 960)
        ctx.line_to(0, 1010)
        ctx.close_path()
        rgba(ctx, hexc("#55534A"))
        ctx.fill()
        for k in range(8):
            line(ctx, [(k * 150 - (t * 300) % 150, 1000 - k * 6), (k * 150 + 70 - (t * 300) % 150, 998 - k * 6)],
                 WHITE, 5, 0.8)
        u = clamp(t / 2.4)
        jx, jy = 240 + 520 * u, 930 - 380 * u * u
        marut(ctx, jx, jy, 0.82, ang=-0.08 - 0.22 * u, exhaust=0.7, gear=u < 0.4, t=t)
        person(ctx, 140, GROUND, 0.56, t, "engineer", "cheer")
        person(ctx, 300, GROUND, 0.54, t + 1, "engineer2", "cheer")

    def drafting(self, ctx, t):
        office(ctx, t)
        rrect(ctx, 150, 280, 780, 400, 10)   # blueprint on the wall
        rgba(ctx, BLUEPRINT)
        ctx.fill()
        for gx in range(170, 930, 40):
            line(ctx, [(gx, 290), (gx, 670)], WHITE, 1, 0.12)
        for gy in range(300, 680, 40):
            line(ctx, [(160, gy), (920, gy)], WHITE, 1, 0.12)
        draw_u = clamp((t - 0.2) / 2.0)
        ctx.save()
        ctx.rectangle(150, 280, 140 + 640 * max(draw_u, 0.35), 400)
        ctx.clip()
        marut(ctx, 560, 500, 1.0, outline=WHITE)
        ctx.restore()
        text(ctx, "HF-24", 210, 320, 40, WHITE, font=MONO, anchor="l", a=0.9)
        poly(ctx, [(160, 940), (620, 900), (640, 960), (180, 1000)], hexc("#C8B48A"))   # drafting table
        line(ctx, [(240, 990), (230, GROUND)], hexc("#4A3B2C"), 12)
        line(ctx, [(560, 960), (580, GROUND)], hexc("#4A3B2C"), 12)
        person(ctx, 290, GROUND, 0.66, t, "designer", "write", prop="pencil")
        person(ctx, 840, GROUND, 0.66, t, "engineer", "point", flip=True)


class War1971(Cued):
    """Thar desert, the post, the tank column; two Maruts dive and knock the tanks out."""

    def events(self, d):
        ta = at(self, "LONGEWALA", 0.4, d)
        return [(0.2, "whoosh"), (ta - 0.6, "whoosh"), (ta + 0.9, "boom"), (ta + 1.5, "boom")]

    def draw(self, ctx, t, d):
        ta = at(self, "LONGEWALA", 0.4, d)
        desert(ctx, t)
        hits = [ta + 0.9, ta + 1.3, ta + 1.7]
        for k, (tx0, ht) in enumerate(zip((640, 830, 1010), hits)):
            roll = 0.0 if t > ht else -18 * min(t, ht)
            tank(ctx, tx0 + roll + 30 * k, GROUND - 10 - 6 * k, 0.72, t, wreck=clamp((t - ht) / 0.3),
                 moving=t < ht)
        for k, ht in enumerate(hits):
            tx = 640 + 30 * k + 190 * k - 18 * ht
            burst(ctx, tx, GROUND - 90, clamp((t - ht) / 0.9), r=170)
        sandbags(ctx, 20, 380, GROUND)
        flag(ctx, 300, 760, 110, 70, "in", t, pole=330)
        hit_any = t > hits[0]
        soldier(ctx, 190, GROUND - 60, 0.6, t, pose="fist" if hit_any else "binocs")
        sandbags(ctx, 60, 340, GROUND + 18)
        for k in range(2):   # two Maruts diving left to right, firing as they pass
            u = clamp((t - (ta - 0.8) - 0.25 * k) / 2.6)
            if 0 < u < 1:
                jx, jy = -250 + 1500 * u, 330 + 120 * k + 260 * u
                marut(ctx, jx, jy, 0.62, ang=0.17, exhaust=0.5, t=t)
                if k == 0:
                    for j, ht in enumerate(hits):
                        fire_t = ht - 0.55
                        rocket(ctx, -250 + 1500 * clamp((fire_t - (ta - 0.8)) / 2.6) + 110,
                               330 + 260 * clamp((fire_t - (ta - 0.8)) / 2.6) + 30,
                               640 + 220 * j - 18 * ht, GROUND - 90, clamp((t - fire_t) / 0.55))


class Engine(Cued):
    """Mach dream vs reality, then the Egyptian test stand where the new engine fades away."""

    def events(self, d):
        return [(0.2, "whoosh"), (at(self, "KAMZOR", 0.35, d), "alarm"), (at(self, "MISR", 0.68, d), "whoosh")]

    def draw(self, ctx, t, d):
        tk = at(self, "KAMZOR", 0.35, d)
        tm = at(self, "MISR", 0.68, d)
        if t < tm + 0.3:
            self.speed(ctx, t, tk)
        if t >= tm:
            ctx.push_group()
            self.stand(ctx, t - tm)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(clamp((t - tm) / 0.3))

    def speed(self, ctx, t, tk):
        sky(ctx, t)
        weak = clamp((t - tk) / 0.5)
        wob = 0.04 * weak * math.sin(t * 9)
        jx = 470 + 30 * math.sin(t * 1.3)
        dream = clamp(t / 1.2) * (1 - weak)
        if dream > 0:   # the Mach 2 dream: a shock cone ahead of the nose
            ctx.move_to(jx + 260, 560)
            ctx.line_to(jx + 60, 380)
            ctx.move_to(jx + 260, 560)
            ctx.line_to(jx + 60, 740)
            rgba(ctx, WHITE, 0.5 * dream)
            ctx.set_line_width(5)
            ctx.stroke()
        marut(ctx, jx, 560, 0.95, ang=wob + 0.06 * weak, exhaust=0.8 * (1 - weak) + 0.25 * weak,
              smoke=weak, t=t)
        v = 0.93 * clamp(t / max(tk, 0.5)) + 0.03 * weak * math.sin(t * 13)
        mach_gauge(ctx, 540, 930, 170, v, ghost=dream, alarm=weak, t=t)

    def stand(self, ctx, t):
        pyramids(ctx, t)
        fade = clamp((t - 0.6) / 1.4)
        jet_engine(ctx, 560, 830, 0.95, solid=1 - 0.85 * fade, t=t)
        egypt_flag(ctx, 640, 600, 110, 70)
        flag(ctx, 770, 600, 110, 70, "in", t)
        line(ctx, [(636, 600), (636, 760)], STEEL, 5)
        person(ctx, 180, GROUND, 0.64, t, "engineer2", "shrug" if fade > 0.5 else "hold",
               prop=None if fade > 0.5 else "clipboard")
        if fade > 0.6:   # red cross over the abandoned engine
            k = clamp((fade - 0.6) / 0.3)
            line(ctx, [(380, 720), (380 + 360 * k, 720 + 220 * k)], RED, 14, 0.85)
            line(ctx, [(740, 720), (740 - 360 * k, 720 + 220 * k)], RED, 14, 0.85)


class Policy(Cued):
    """Engineer vs official at the desk while imports fly past; then a tarp over the retired Marut."""

    def events(self, d):
        return [(0.2, "whoosh"), (at(self, "VIDESHI", 0.3, d), "whoosh"), (at(self, "DASHAK", 0.62, d), "thud")]

    def draw(self, ctx, t, d):
        tv = at(self, "VIDESHI", 0.3, d)
        td = at(self, "DASHAK", 0.62, d)
        if t < td + 0.3:
            self.desk(ctx, t, tv)
        if t >= td:
            ctx.push_group()
            self.tarp(ctx, t - td)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(clamp((t - td) / 0.3))

    def desk(self, ctx, t, tv):
        office(ctx, t)
        rrect(ctx, 520, 270, 480, 360, 8)   # window
        g = cairo.LinearGradient(0, 270, 0, 630)
        g.add_color_stop_rgb(0, *hexc("#3D6FA8"))
        g.add_color_stop_rgb(1, *hexc("#F2B077"))
        ctx.set_source(g)
        ctx.fill()
        ctx.save()
        rrect(ctx, 520, 270, 480, 360, 8)
        ctx.clip()
        u = clamp((t - tv + 0.3) / 2.2)
        for k in range(3):   # foreign jets crossing the window (generic delta / swept silhouettes, no markings)
            jx = 1050 - 700 * u - 90 * k
            jy = 380 + 60 * k
            ctx.save()
            ctx.translate(jx, jy)
            ctx.scale(-0.7, 0.7)
            poly(ctx, [(70, 0), (10, -8), (-30, -40), (-45, -40), (-30, -6), (-60, -4), (-60, 4), (-30, 6),
                       (-45, 40), (-30, 40), (10, 8)], hexc("#2A2E36"), 0.9)
            ctx.restore()
        ctx.restore()
        line(ctx, [(760, 270), (760, 630)], hexc("#2E2A24"), 10)
        line(ctx, [(520, 450), (1000, 450)], hexc("#2E2A24"), 10)
        rrect(ctx, 520, 270, 480, 360, 8)
        rgba(ctx, hexc("#2E2A24"))
        ctx.set_line_width(14)
        ctx.stroke()
        person(ctx, 820, GROUND, 0.66, t, "official", "wave_off", flip=True)
        rrect(ctx, 560, 930, 480, 200, 10)   # desk front hides the official's legs
        rgba(ctx, hexc("#6B4A2B"))
        ctx.fill()
        rrect(ctx, 540, 910, 520, 30, 6)
        rgba(ctx, hexc("#8A6238"))
        ctx.fill()
        rrect(ctx, 620, 850, 130, 60, 6)   # empty open cash box
        rgba(ctx, hexc("#3A3A3A"))
        ctx.fill()
        rrect(ctx, 632, 860, 106, 40, 4)
        rgba(ctx, (0.08, 0.08, 0.08))
        ctx.fill()
        poly(ctx, [(620, 850), (750, 850), (770, 790), (640, 790)], hexc("#4A4A4A"))
        rrect(ctx, 860, 880, 120, 30, 4)   # file on the desk
        rgba(ctx, hexc("#C9A86A"))
        ctx.fill()
        person(ctx, 250, GROUND, 0.66, t, "engineer", "plead", prop="blueprint")

    def tarp(self, ctx, t):
        sky(ctx, t, warm=0.9)
        ctx.rectangle(0, 1000, W, GROUND)
        rgba(ctx, hexc("#6E6A4A"))
        ctx.fill()
        for k in range(40):   # grass grown around the parked jet
            gx = rnd(k, 31) * W
            line(ctx, [(gx, GROUND), (gx + 6, GROUND - 30 - 30 * rnd(k, 32))], hexc("#4E5A2E"), 4, 0.8)
        marut(ctx, 560, GROUND - 93, 1.1, gear=True, t=t)
        cover = clamp(t / 2.0)
        if cover > 0:   # tarp sliding from the tail forward over the jet
            x1 = 160 + 720 * cover
            ctx.move_to(160, GROUND - 210)
            ctx.curve_to(160 + (x1 - 160) * 0.5, GROUND - 240, x1 - 40, GROUND - 160, x1, GROUND - 120)
            ctx.line_to(x1 + 20, GROUND - 60)
            ctx.curve_to(x1 - 200, GROUND - 40, 300, GROUND - 50, 150, GROUND - 60)
            ctx.close_path()
            rgba(ctx, hexc("#3E4A3A"), 0.97)
            ctx.fill()
            for k in range(5):
                fx = 200 + k * (x1 - 200) / 5
                line(ctx, [(fx, GROUND - 200), (fx + 30, GROUND - 70)], hexc("#2E3A2A"), 3)
        person(ctx, 960, GROUND, 0.6, t, "crew", "pull", flip=True)


class DebateLoop(Cued):
    """Engine vs policy balance, payoff on the Tejas engine, then fade back into the scene-1 hangar."""

    def events(self, d):
        return [(0.15, "tick"), (at(self, "TEJAS", 0.42, d), "whoosh"), (at(self, "WAHIN", 0.78, d), "shimmer")]

    def draw(self, ctx, t, d):
        tt = at(self, "TEJAS", 0.42, d)
        tw = at(self, "WAHIN", 0.78, d)
        if t < tt + 0.3:
            self.debate(ctx, t)
        if t >= tt and t < tw + 0.6:
            ctx.push_group()
            self.tejas(ctx, t - tt)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(clamp((t - tt) / 0.3))
        if t >= tw:   # loop: the exact opening frame of scene 1 (shutter up) fades in
            ctx.push_group()
            hangar(ctx, t - tw, shutter=0.0)
            person(ctx, 140, GROUND, 0.62, t - tw, "pilot", "salute")
            person(ctx, 1000, GROUND, 0.6, t - tw, "crew", "stand", flip=True)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(clamp((t - tw) / 0.6))

    def debate(self, ctx, t):
        g = cairo.RadialGradient(540, 600, 60, 540, 600, 900)
        g.add_color_stop_rgb(0, *hexc("#4A4A32"))
        g.add_color_stop_rgb(1, *hexc("#141810"))
        ctx.set_source(g)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()
        ctx.rectangle(0, 1060, W, GROUND)
        rgba(ctx, hexc("#2A2A1E"))
        ctx.fill()
        balance(ctx, 540, 400, 0.16 * math.sin(t * 2.2), t)
        person(ctx, 120, GROUND, 0.6, t, "engineer", "point")
        person(ctx, 960, GROUND, 0.6, t, "official", "think", flip=True, prop=None)

    def tejas(self, ctx, t):
        sky(ctx, t, warm=0.35)
        ang = math.radians(-28)
        cx, cy, s = 540, 640, 2.2
        glow(ctx, cx, cy, 380, SAFFRON, 0.18)
        draw_tejas_fighter(ctx, cx, cy, scale=s, angle=ang, afterburner=True)
        ex, ey = cx + (-55 * s) * math.cos(ang), cy + (-55 * s) * math.sin(ang)   # engine bay, world coords
        pulse = 0.5 + 0.5 * math.sin(t * 7)
        ctx.arc(ex, ey, 70 + 8 * pulse, 0, math.tau)
        rgba(ctx, CYAN, 0.9)
        ctx.set_line_width(6)
        ctx.stroke()
        glow(ctx, ex, ey, 90, CYAN, 0.35)
        k = clamp(t / 0.4)
        line(ctx, [(ex - 50, ey + 50), (ex - 150 * k, ey + 200 * k)], CYAN, 5)
        if k >= 1:
            flag(ctx, ex - 290, ey + 200, 150, 90, "us", t)
            rrect(ctx, ex - 296, ey + 194, 162, 102, 6)
            rgba(ctx, CYAN)
            ctx.set_line_width(4)
            ctx.stroke()


SCENE_CLASSES = {
    "shutter_hook": ShutterHook,
    "birth": Birth,
    "war_1971": War1971,
    "engine": Engine,
    "policy": Policy,
    "debate_loop": DebateLoop,
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
        "HF-24 Marut: India Ka Pehla Desi Fighter Band Kyun Hua? #shorts",
        "Marut Fighter Jet: Jung Jeeti, Phir Bhi Band! Engine Ya Soch? #shorts",
        "Tejas Se Pehle Tha Marut: India Ka Pehla Desi Fighter Jet #shorts",
        "Kurt Tank Ka Bharatiya Fighter: HF-24 Marut Ki Adhuri Kahani #shorts",
        "India First Fighter Jet HF-24 Marut: Galti Engine Ki Ya Soch Ki? #shorts",
    ],
    "title": "HF-24 Marut: India Ka Pehla Desi Fighter Band Kyun Hua? #shorts",
    "thumb_text": "ENGINE YA SOCH?",
    "queries": ["hf-24 marut", "india pehla desi fighter", "marut fighter jet"],
    "description": """HF-24 Marut - India ka pehla desi fighter jet (India first fighter jet). Jung jeeti, phir bhi band kyun hua?
Marut fighter jet HAL ne German designer Kurt Tank ki team ke saath banaya, pehli udaan 17 June 1961.

Is Short mein:
- 1961: HF-24 Marut ki pehli udaan (HAL, Bangalore)
- 1971 ki jung: Maruts ne ground attack mission udaaye; reports ke mutabik Longewala mein bhi Hawker Hunters ke saath bheje gaye
- Design Mach 2 ka tha, par do Orpheus 703 engine (bina afterburner) ki wajah se ye kabhi Mach 1 paar nahi kar paya
- Behtar engine ki koshishein (Orpheus BOr-12, Egypt ka E-300 project) adhoori reh gayi
- 1980s ke aakhir tak phase out (aakhri unit 1990), phir dashakon tak import jets
- Aaj bhi Tejas Mk1A American GE F404 engine par udta hai

Debate: galti engine ki thi ya sarkar ki soch ki? Ye kisi party ya neta ki baat nahi - engineering vs policy choices ka sawaal hai. Apna jawab comment mein likho.

Sources:
- Wikipedia: HAL HF-24 Marut
- HistoryNet: Kurt Tank's Indian Storm
- Wikipedia: Battle of Longewala (Marut + Hunter deployment; Hunters ne zyada tank roke)
- Business Today (13 Jul 2026): HAL gets 7th GE F404 engine for Tejas Mk1A
""",
    "tags": [
        "hf-24 marut", "marut fighter jet", "india first fighter jet", "hal marut", "kurt tank",
        "indian air force history", "1971 war", "longewala", "tejas engine", "kaveri engine", "indian fighter jet",
        "reality shift", "defence shorts",
    ],
    "hashtags": ["#Shorts", "#HF24Marut", "#IndianAirForce"],
    "pinned_comment": "Marut ko band karna sahi tha ya galti? Aapka jawab 👇",
}


def thumbnail(ctx):
    """High-CTR cover: the garlanded Marut in its hangar with the shutter half down, the paradox in big type."""
    hangar(ctx, 1.0, shutter=0.42, roof_flag=False)
    person(ctx, 140, GROUND, 0.62, 1.0, "pilot", "salute")
    person(ctx, 1000, GROUND, 0.6, 1.0, "crew", "pull", flip=True)
    line(ctx, [(985, GROUND - 330), (985, 420)], (0.6, 0.6, 0.6), 4)
    text(ctx, "PEHLA DESI FIGHTER", 540, 205, 92, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "BAND KYUN?", 540, 330, 150, RED, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "HF-24 MARUT", 540, 1290, 120, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "ENGINE YA SOCH?", 540, 1430, 96, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, PAL["ui"], a=0.85)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.marut")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    total = sum(s["dur"] for s in engine.SCENES)
    write_alignment(final)
    upload_kit.build(story, final, total)
    if total > MAX_SECONDS:
        raise SystemExit(f"[length] {total:.1f}s is over the {MAX_SECONDS:.0f}s lock - re-record faster "
                         f"(KikiVoice tempo 1.05-1.10) or trim a line, then render again")


if __name__ == "__main__":
    main()
