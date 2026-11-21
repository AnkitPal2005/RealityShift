"""Reality Shift Short - "Siachen: minus 50 me ek raat?" (~45s, first two-character Short).

Usage:
  python make.py siachen

First Short in the "Major Saab + Gappu" format (user idea, 12 Nov 2026, with our own invented characters instead
of real politicians): Major Saab explains, Gappu shows off and the physics teaches him. Two voices from the
same MadhurNeural (Major lower and steadier, Gappu higher and faster), the new Lego "speech" caption names the
speaker, and the new "glacier" palette fits the snow. Six scenes: hook (-50 C, Gappu in a T-shirt) -> freeze
(frostbite in minutes) -> oxygen (21,000 ft, under half the oxygen per breath; Gappu on a "treadmill") -> egg
(rock-hard, bounces off a hammer) -> salute (Operation Meghdoot, 13 Apr 1984, 42 years) -> HAAN/NAA poll.
The jokes are always on Gappu and the cold, never on the soldiers.
"""

import importlib
import json
import math
import sys

import cairo

from core import engine
from core import delivery
from core import lego
from core.engine import *  # noqa: F401,F403
from shorts.brahmos_lego import tag
from shorts.chabahar import Cued
from shorts.reality_shift import stamp

TOPIC = "SIACHEN MINUS 50"
OUTPUTS = {"edge": "siachen_short.mp4"}
LEGO = {"header": "radar", "caption": "speech", "transition": "shutter", "palette": "glacier", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.3
TAIL_PAD = 0.25
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 80
MUSIC_STYLE = "ambient"    # cold, open air under the dialogue (Agni was pulse @ 112)
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"

PAL = lego.PALETTES["glacier"]
ICE = PAL["ui"]
HI = PAL["hi"]
RED = PAL["alert"]
INK = PAL["ink"]
OLIVE = hexc("#4B5E2E")
GOLD = hexc("#E8B93A")
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
NAVY = hexc("#000080")
MAJOR_C = lego.SPEAKERS["M"][1]
GAPPU_C = lego.SPEAKERS["G"][1]

SOURCES = [
    "Siachen: world's highest battlefield; hostile weather, sub-zero temperature, low oxygen (Tribune India archive "
    "'story-192077'; Indian Defence Review 'Siachen Glacier: battling on the roof of the world')",
    "Temperatures below minus 50 C (reported figures range -40 to -60 C and lower in winter); posts above 21,000 ft "
    "(Indian Defence Review; USI of India 'Forty Years of Operation Meghdoot'; Business Standard, 13 Apr 2024)",
    "Operation Meghdoot launched 13 April 1984 by the Indian Army to secure the glacier (USI of India, 2024; PIB via "
    "GlobalSecurity 'india-240413-india-pib01'; Deccan Chronicle 40th anniversary) - 2026 - 1984 = 42 years",
    "Oxygen per breath: at 18,000 ft each breath has half the oxygen found at sea level, falling further above it "
    "(FAA pilot safety brochure 'Hypoxia'; CDC NIOSH altitude document) - so at ~21,000 ft it is under half",
    "Frozen food: June 2019 video posted by the Indian Military Academy - Siachen soldiers hit eggs with a hammer, "
    "eggs don't crack and bounce off; juice packs frozen solid (Tribune India; Business Standard / IANS, 8 Jun 2019; "
    "The Quint)",
    "Frostbite: exposed skin can freeze within minutes at extreme wind-chill (-40 C and below) (US National Weather "
    "Service wind-chill chart)",
    "Major Saab and Gappu are invented cartoon characters; Gappu's jokes are about the cold, not about any real person",
]

# each line: (tone, [(spoken, "M|" or "G|" + caption), ...][, gap before the next line in s]) - prefix = speaker.
# Written as a real back-and-forth: short replies, a deadpan "dono", Gappu cutting in with "Arre?!".
# Voices: both characters are recorded in KikiVoice (user choice, 12 Nov) - voice_kit.py export / split.
SPEC = [
    {"key": "hook", "accent": ICE, "text": "MINUS 50°C",
     "visual": "Snow peaks at night, a temperature panel rolls +25 -> -50 C; Major Saab in an extreme-cold parka; "
               "Gappu walks in wearing a T-shirt, shorts, chappals and sunglasses, hands on hips",
     "vo": [("punch", [("माइनस पचास।", "M|MINUS 50.")], 0.06),
            ("sly", [("बस?", "G|BAS?")], 0.05),
            ("build", [("यार, मैं तो टी-शर्ट में ही चल लूँगा!", "G|YAAR, MAIN TOH T-SHIRT MEIN HI CHAL LOONGA!")]),
            ("sly", [("अच्छा? चल के दिखा।", "M|ACHHA? CHAL KE DIKHA.")])]},
    {"key": "freeze", "accent": RED, "text": "FROSTBITE",
     "visual": "'SIACHEN' tag; Gappu shivers, turns blue, icicles on his nose and an ice block closes round him; "
               "'FROSTBITE / KUCH MINUTE MEIN' stamp",
     "vo": [("tell", [("सियाचिन है ये—", "M|SIACHEN HAI YE—"),
                      ("दुनिया का सबसे ऊँचा जंग का मैदान।", "M|DUNIYA KA SABSE OONCHA JANG KA MAIDAAN.")]),
            ("low", [("मेजर साब... यार...", "G|MAJOR SAAB... YAAR...")]),
            ("punch", [("मैं तो बरफ़ बन गया!", "G|MAIN TOH BARAF BAN GAYA!")]),
            ("tell", [("खुली चमड़ी पे,", "M|KHULI CHAMDI PE,")]),
            ("punch", [("कुछ ही मिनट में फ्रॉस्टबाइट।", "M|KUCH HI MINUTE MEIN FROSTBITE.")])]},
    {"key": "air", "accent": HI, "text": "21,000 FT",
     "visual": "Gappu marches on the spot while the snow scrolls under him like a treadmill, puffing vapour; "
               "'21,000 FT' tag; an O2 meter drops from 10 cells to under 5",
     "vo": [("build", [("चलो चलो, फटाफट ऊपर!", "G|CHALO CHALO, PHATAPHAT UPAR!")], 0.02),
            ("tell", [("रुक! इक्कीस हज़ार फ़ीट पे—", "M|RUK! 21,000 FEET PE—")]),
            ("punch", [("हर साँस में आधी से भी कम ऑक्सीजन।", "M|HAR SAANS MEIN AADHI SE BHI KAM OXYGEN.")]),
            ("sly", [("भाई... ये पहाड़ है या ट्रेडमिल?", "G|BHAI... YE PAHAAD HAI YA TREADMILL?")], 0.1),
            ("low", [("दोनों।", "M|DONO.")])]},
    {"key": "egg", "accent": GAPPU_C, "text": "ANDA = PATHAR",
     "visual": "Gappu taps an egg on a rock - it bounces; a hammer slams down - TONK - the egg jumps, not a crack; "
               "'ANDA = PATHAR' stamp; the egg rolls away like a marble",
     "vo": [("build", [("एक एग दे दो यार।", "G|EK EGG DE DO YAAR.")]),
            ("tell", [("ले। पर यहाँ अंडा भी पत्थर है।", "M|LE. PAR YAHAN ANDA BHI PATHAR HAI.")], -0.08),
            ("sly", [("अरे?!", "G|ARRE?!")], 0.05),
            ("punch", [("हथौड़ा मार, फिर भी नहीं टूटेगा।", "M|HATHAUDA MAAR, PHIR BHI NAHI TOOTEGA.")]),
            ("sly", [("ये एग है या कंचा?!", "G|YE EGG HAI YA KANCHA?!")])]},
    {"key": "salute", "accent": SAFFRON, "text": "OPERATION MEGHDOOT",
     "visual": "A drawn tricolour on the highest peak; '13 APRIL 1984 / OPERATION MEGHDOOT' tag; Major Saab "
               "salutes, then Gappu salutes too; '42 SAAL SE' stamp",
     "vo": [("tell", [("तो यहाँ रहता कौन है?", "G|TOH YAHAN REHTA KAUN HAI?")]),
            ("low", [("म्हारे जवान।", "M|MHAARE JAWAN.")]),
            ("tell", [("तेरह अप्रैल उन्नीस सौ चौरासी,", "M|13 APRIL 1984,"),
                      ("ऑपरेशन मेघदूत—", "M|OPERATION MEGHDOOT—")]),
            ("punch", [("तब से हर दिन, यहीं।", "M|TAB SE HAR DIN, YAHIN.")]),
            ("low", [("सैल्यूट है, भाई।", "G|SALUTE HAI, BHAI.")])]},
    {"key": "ask", "accent": HI, "text": "EK RAAT TIK PAATE?",
     "visual": "Gappu wrapped head to toe in a blanket, only his nose out; the HAAN / NAA poll card pops in",
     "vo": [("sly", [("मैं तो... कंबल में ही सही हूँ।", "G|MAIN TOH... KAMBAL MEIN HI SAHI HOON.")]),
            ("ask", [("तुम बताओ—", "M|TUM BATAO—"), ("यहाँ एक रात टिक पाते?", "M|YAHAN EK RAAT TIK PAATE?")]),
            ("cta", [("हाँ या ना, कमेंट करो!", "M|HAAN YA NAA, COMMENT KARO!")])]},
]

# two real voices: Major = Madhur, a touch lower and steady; Gappu = Prabhat, quicker and a little higher
VOICES = {"M": ("hi-IN-MadhurNeural", -3, 4), "G": ("hi-IN-MadhurNeural", 22, 12)}   # (voice, pitch Hz, rate %)
# ^ edge-tts fallback only; the real voices come from KikiVoice (voice_kit.py, render --engine files)
PAUSE_SCALE = 0.5              # same speaker: half the narrator's pauses, so the talk keeps moving
SWITCH_GAP = 0.08              # other character answers almost at once, like people talking
KIKI_TEMPO = {"major": 1.0, "gappu": 1.0}   # raise to 1.08-1.15 if a KikiVoice voice reads slowly


def _shift(val, d, unit):
    return f"{int(val.rstrip(unit)) + d:+d}{unit}"


def voiced(spec, rows_by_key):
    """delivery.build() rows -> per-speaker voice, pitch and rate; tight turn-taking.
    A line's own 3rd element sets the gap after it (negative = the next speaker cuts in)."""
    out = {}
    for s in spec:
        rows, lines = [], s["vo"]
        for i, ((tone, chunks, *gap), (tt, line_, pause)) in enumerate(zip(lines, rows_by_key[s["key"]])):
            who = chunks[0][1][0]
            nxt = lines[i + 1][1][0][1][0] if i + 1 < len(lines) else who
            voice, dp, dr = VOICES[who]
            rate, pitch, vol = tt
            if gap:
                pause = gap[0]
            elif nxt != who and pause:
                pause = SWITCH_GAP
            rows.append(((_shift(rate, dr, "%"), _shift(pitch, dp, "Hz"), vol, voice), line_, pause))
        out[s["key"]] = rows
    return out


DELIVERY = voiced(SPEC, delivery.build(SPEC, pause_scale=PAUSE_SCALE))
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {"MINUS": ICE, "50": ICE, "DEGREE!": ICE, "T-SHIRT": GAPPU_C, "SIACHEN": ICE, "OONCHA": HI, "JANG": HI,
       "JAM": ICE, "FROSTBITE!": RED, "MINUTE": RED, "21,000": HI, "FEET": HI, "AADHI": RED, "KAM": RED,
       "OXYGEN!": RED, "TREADMILL?": GAPPU_C, "ANDA": GAPPU_C, "PATHAR": HI, "HATHAUDE": HI, "NAHI": RED,
       "KANCHA?!": GAPPU_C, "BAS?": GAPPU_C, "BARAF": ICE, "DONO": HI, "EGG": GAPPU_C, "SALUTE": SAFFRON,
       "ACHHA?": HI, "RUK!": RED, "TOOTEGA": RED, "HATHAUDA": HI, "MHAARE": SAFFRON, "JAWAN...": SAFFRON, "1984": SAFFRON, "OPERATION": SAFFRON,
       "MEGHDOOT": SAFFRON, "HAR": HI, "DIN": HI, "SALAAM": SAFFRON, "KAMBAL": GAPPU_C, "RAAT": HI, "TIK": HI,
       "HAAN": INDIA_GREEN, "NAA,": RED, "COMMENT": HI, "BHAI": GAPPU_C, "BHAI!": GAPPU_C, "BHAI...": GAPPU_C}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".—")] = HOT[_k]

# ============================================================ world

GY = 1080                  # ground line: characters stand here, the caption bubble sits just below
MAJOR_X, GAPPU_X = 300, 760


def mix(a, b, u):
    return tuple(lerp(x, y, clamp(u)) for x, y in zip(a, b))


FAR = [(0, 640), (90, 520), (190, 600), (300, 430), (420, 560), (540, 380), (660, 540), (780, 450), (900, 580),
       (1000, 470), (1080, 560)]
NEAR = [(0, 820), (140, 700), (260, 790), (380, 660), (520, 800), (650, 700), (800, 820), (930, 690), (1080, 780)]


def mountains(ctx, pts, base, body, snow, cap=0.32):
    ctx.move_to(pts[0][0], base)
    for p in pts:
        ctx.line_to(*p)
    ctx.line_to(pts[-1][0], base)
    ctx.close_path()
    rgba(ctx, body)
    ctx.fill()
    for i in range(1, len(pts) - 1):
        (x0, y0), (px, py), (x1, y1) = pts[i - 1], pts[i], pts[i + 1]
        if py >= y0 or py >= y1:
            continue
        l = (lerp(px, x0, cap), lerp(py, y0, cap))
        r = (lerp(px, x1, cap), lerp(py, y1, cap))
        ctx.move_to(px, py)
        ctx.line_to(*r)
        for k in range(1, 4):           # jagged snow line back to the left edge
            u = k / 4
            ctx.line_to(lerp(r[0], l[0], u), lerp(r[1], l[1], u) + (14 if k % 2 else -6))
        ctx.line_to(*l)
        ctx.close_path()
        rgba(ctx, snow)
        ctx.fill()


def flag(ctx, x, y, t, a=1.0):
    """Drawn tricolour waving on a pole, pole foot at (x, y)."""
    line(ctx, [(x, y), (x, y - 170)], (0.85, 0.87, 0.9), 6, a)
    fw, fh, n = 120, 78, 12
    for i in range(n):
        dy = 6 * math.sin(t * 6 - i * 0.7) * (i / n)
        for k, c in enumerate((SAFFRON, (1, 1, 1), INDIA_GREEN)):
            ctx.rectangle(x + fw * i / n, y - 168 + dy + k * fh / 3, fw / n + 1, fh / 3 + 0.5)
            rgba(ctx, c, a)
            ctx.fill()
    ctx.arc(x + fw * 0.5, y - 168 + fh / 2 + 3 * math.sin(t * 6 - 6 * 0.7) * 0.5, 9, 0, math.tau)
    rgba(ctx, NAVY, a)
    ctx.set_line_width(3)
    ctx.stroke()


def scenery(ctx, t, wind=1.0, scroll=0.0, flag_a=0.0, dark=0.0):
    g = cairo.LinearGradient(0, 0, 0, GY)
    g.add_color_stop_rgb(0, *mix(hexc("#081428"), (0, 0, 0), dark))
    g.add_color_stop_rgb(1, *mix(hexc("#3D6E9C"), (0, 0, 0), dark))
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()
    for i in range(40):                  # stars
        circle(ctx, rnd(i, 7) * W, 180 + rnd(i, 8) * 300, 1.5 + rnd(i, 9) * 2, (1, 1, 1),
               0.3 + 0.4 * (0.5 + 0.5 * math.sin(t * 2 + i)))
    mountains(ctx, FAR, GY, hexc("#284769"), hexc("#C9DDEE"))
    if flag_a:
        flag(ctx, 540, 380, t, flag_a)
    mountains(ctx, NEAR, GY, hexc("#4F769C"), hexc("#E6F1FA"), cap=0.4)
    g = cairo.LinearGradient(0, GY - 60, 0, H)
    g.add_color_stop_rgb(0, *hexc("#E9F3FA"))
    g.add_color_stop_rgb(1, *hexc("#8FB0C8"))
    ctx.rectangle(0, GY - 60, W, H)
    ctx.set_source(g)
    ctx.fill()
    for i in range(14):                  # drift lines on the snow; they slide when scroll moves (treadmill)
        x = (rnd(i, 3) * W * 1.4 - scroll * 520) % (W * 1.4) - 160
        y = GY - 40 + rnd(i, 4) * 120
        line(ctx, [(x, y), (x + 70 + 60 * rnd(i, 5), y + 4)], hexc("#A9C4D8"), 5, 0.8)
    snow(ctx, t, 70, wind)


def snow(ctx, t, n, wind=1.0):
    for i in range(n):
        x = (rnd(i, 1) * W - t * wind * 70 * (0.5 + rnd(i, 4)) + 25 * math.sin(t * 1.7 + i)) % W
        y = (rnd(i, 2) * H + t * 140 * (0.6 + rnd(i, 3))) % H
        circle(ctx, x, y, 2 + 4 * rnd(i, 5), (1, 1, 1), 0.75)
    if wind > 1.2:                       # gusts
        for i in range(8):
            x = (rnd(i, 11) * W - t * 900 * (0.8 + rnd(i, 12))) % (W + 300) - 150
            y = 250 + rnd(i, 13) * 800
            line(ctx, [(x, y), (x + 160, y - 6)], (1, 1, 1), 3, 0.35)


# ============================================================ characters

PARKA = hexc("#E3E9EF")
PARKA_SH = hexc("#AEBBC8")
TROUSER = hexc("#C2CDD8")
BOOT = hexc("#1B1B1F")
SKIN_M = hexc("#B97A50")
MUST = hexc("#2A1A10")
TEE = GAPPU_C
SHORTS_C = hexc("#2F6FD6")
SKIN_G = hexc("#D69A6A")
ICE_SKIN = hexc("#A8DDF2")
HAIR = hexc("#16110D")
BLANKET = hexc("#8C2F39")


def mouth_open(t, talk):
    return 0.25 + 0.75 * abs(math.sin(t * 15)) if talk else 0.0


def arm(ctx, pts, sleeve, hand, w=38):
    line(ctx, pts, sleeve, w)
    circle(ctx, *pts[-1], w * 0.55, hand)


def major(ctx, x, y, t, pose="stand", talk=False, s=1.0):
    """Major Saab, facing right: white extreme-cold parka, olive beret with a gold badge, handlebar moustache."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    br = 2.5 * math.sin(t * 2.2)
    for lx in (-30, 30):
        line(ctx, [(lx, -190), (lx, -36)], TROUSER, 46)
        rrect(ctx, lx - 30, -42, 70, 42, 14)
        rgba(ctx, BOOT)
        ctx.fill()
    arm(ctx, [(-74, -338 + br), (-92, -255), (-86, -182)], PARKA_SH, OLIVE)
    rrect(ctx, -96, -372 + br, 192, 206, 48)
    rgba(ctx, PARKA)
    ctx.fill_preserve()
    rgba(ctx, PARKA_SH)
    ctx.set_line_width(5)
    ctx.stroke()
    line(ctx, [(0, -356 + br), (0, -176)], PARKA_SH, 4)
    for k, c in enumerate((SAFFRON, (1, 1, 1), INDIA_GREEN)):   # small tricolour patch on the sleeve side
        ctx.rectangle(30, -318 + br + k * 9, 36, 9)
        rgba(ctx, c)
        ctx.fill()
    ctx.save()                                                   # fur collar
    ctx.translate(0, -372 + br)
    ctx.scale(1.0, 0.32)
    circle(ctx, 0, 0, 92, hexc("#8A7A66"))
    ctx.restore()
    hx, hy = 4, -432 + br
    circle(ctx, hx - 48, hy + 6, 13, shade(SKIN_M, 0.9))
    circle(ctx, hx, hy, 54, SKIN_M)
    ctx.save()                                                   # beret
    ctx.translate(hx - 8, hy - 42)
    ctx.rotate(-0.22)
    ctx.scale(1.28, 0.55)
    circle(ctx, 0, 0, 54, OLIVE)
    ctx.restore()
    circle(ctx, hx + 24, hy - 50, 9, GOLD)
    line(ctx, [(hx + 4, hy - 18), (hx + 34, hy - 23)], MUST, 9)
    if (t * 0.8) % 3.2 < 0.12:
        line(ctx, [(hx + 16, hy - 5), (hx + 30, hy - 5)], MUST, 4)
    else:
        circle(ctx, hx + 23, hy - 5, 6.5, MUST)
    circle(ctx, hx + 50, hy + 6, 11, shade(SKIN_M, 0.88))
    m = mouth_open(t, talk)
    if m:
        ctx.save()
        ctx.translate(hx + 42, hy + 38)
        ctx.scale(1, 0.3 + m)
        circle(ctx, 0, 0, 10, hexc("#5A1A1A"))
        ctx.restore()
    ctx.move_to(hx + 20, hy + 24)                                # handlebar moustache with curled tips
    ctx.curve_to(hx + 28, hy + 12, hx + 58, hy + 12, hx + 66, hy + 22)
    ctx.curve_to(hx + 76, hy + 28, hx + 82, hy + 18, hx + 82, hy + 8)
    ctx.curve_to(hx + 90, hy + 26, hx + 74, hy + 38, hx + 58, hy + 31)
    ctx.curve_to(hx + 44, hy + 28, hx + 30, hy + 36, hx + 20, hy + 24)
    rgba(ctx, MUST)
    ctx.fill()
    if pose == "point":
        arm(ctx, [(62, -338 + br), (150, -322), (232, -330)], PARKA, OLIVE)
        line(ctx, [(232, -330), (262, -334)], OLIVE, 12)
    elif pose == "salute":
        arm(ctx, [(62, -338 + br), (132, -390 + br), (hx + 30, hy - 30)], PARKA, OLIVE, w=36)
    elif pose == "open":
        arm(ctx, [(62, -338 + br), (130, -300), (170, -360 + 8 * math.sin(t * 3))], PARKA, OLIVE)
    else:
        arm(ctx, [(62, -338 + br), (80, -255), (76, -182)], PARKA, OLIVE)
    ctx.restore()


def gappu(ctx, x, y, t, pose="stand", talk=False, freeze=0.0, huff=0.0, walk=None, s=1.0, egg_in_hand=False):
    """Gappu, facing left (toward Major Saab): round belly in a yellow T-shirt, shorts, chappals, sunglasses.
    freeze 0..1 turns him blue, adds icicles and an ice block; huff puffs vapour; walk = leg phase."""
    shiver = 5 * clamp(freeze) * math.sin(t * 70)
    skin = mix(SKIN_G, ICE_SKIN, freeze)
    ctx.save()
    ctx.translate(x + shiver, y)
    ctx.scale(-s, s)                      # drawn facing right, mirrored to face left
    if pose == "blanket":
        ctx.move_to(-130, 0)
        ctx.curve_to(-150, -200, -110, -400, 0, -430)
        ctx.curve_to(110, -400, 150, -200, 130, 0)
        ctx.close_path()
        rgba(ctx, BLANKET)
        ctx.fill()
        for k in range(3):
            line(ctx, [(-120 + 10 * k, -90 - 60 * k), (120 - 10 * k, -90 - 60 * k)], GOLD, 7, 0.8)
        hx, hy = 10, -372
        ctx.save()
        ctx.rectangle(hx - 70, hy - 80, 140, 120)
        ctx.clip()
        circle(ctx, hx, hy + 10, 50, skin)
        ctx.restore()
        ctx.arc(hx, hy + 10, 64, math.pi * 1.05, math.pi * 1.95)          # hood edge
        rgba(ctx, shade(BLANKET, 0.8))
        ctx.set_line_width(22)
        ctx.stroke()
        circle(ctx, hx + 46, hy + 14, 13, hexc("#E46D6D"))               # cold red nose
        for k, ex in enumerate((hx + 4, hx + 28)):
            circle(ctx, ex, hy - 2, 5, HAIR)
        ctx.restore()
        return
    for k, lx in enumerate((-32, 32)):
        sw = 24 * math.sin(walk + k * math.pi) if walk is not None else 0
        lift = -10 * max(0.0, math.sin(walk + k * math.pi)) if walk is not None else 0
        line(ctx, [(lx, -150), (lx + sw, -22 + lift)], skin, 30)
        ctx.save()
        ctx.translate(lx + sw + 10, -8 + lift)
        ctx.scale(1.6, 0.45)
        circle(ctx, 0, 0, 24, hexc("#7A4B2A"))
        ctx.restore()
    rrect(ctx, -72, -216, 144, 84, 22)
    rgba(ctx, SHORTS_C)
    ctx.fill()
    if pose != "salute":
        arm(ctx, [(-70, -340), (-112, -268), (-94, -205)], shade(TEE, 0.8), skin, w=30)
    ctx.save()
    ctx.translate(0, -282)
    ctx.scale(1.0, 1.06)
    circle(ctx, 0, 0, 110, TEE)
    ctx.restore()
    ctx.save()                            # "SHER" on the shirt, un-mirrored so it reads
    ctx.translate(18, -270)
    ctx.scale(-1, 1)
    text(ctx, "SHER", 0, 0, 46, hexc("#7A3E00"), font=CAPTION_FONT, bold=False, a=0.85)
    ctx.restore()
    hx, hy = 6, -444
    circle(ctx, hx, hy, 60, skin)
    for k in range(7):                    # spiky hair
        a0 = math.pi * (1.08 + 0.12 * k)
        bx, by = hx + 58 * math.cos(a0), hy + 58 * math.sin(a0)
        tx, ty = hx + 92 * math.cos(a0 + 0.06), hy + 92 * math.sin(a0 + 0.06)
        ctx.move_to(bx - 14 * math.sin(a0), by + 14 * math.cos(a0))
        ctx.line_to(tx, ty)
        ctx.line_to(bx + 14 * math.sin(a0), by - 14 * math.cos(a0))
        ctx.close_path()
        rgba(ctx, mix(HAIR, (0.9, 0.95, 1.0), freeze * 0.8))
        ctx.fill()
    rrect(ctx, hx + 2, hy - 26, 58, 30, 12)          # sunglasses
    rgba(ctx, mix(hexc("#101418"), (0.85, 0.93, 1.0), freeze * 0.7))
    ctx.fill()
    line(ctx, [(hx - 40, hy - 14), (hx + 4, hy - 14)], hexc("#101418"), 5)
    circle(ctx, hx + 58, hy + 8, 12, shade(skin, 0.9))
    m = mouth_open(t, talk)
    if freeze > 0.5 and not huff:          # chattering teeth
        rrect(ctx, hx + 22, hy + 26, 34, 18, 5)
        rgba(ctx, (1, 1, 1))
        ctx.fill()
        for k in range(3):
            line(ctx, [(hx + 30 + 8 * k, hy + 26), (hx + 30 + 8 * k, hy + 44)], (0.6, 0.6, 0.65), 2)
        line(ctx, [(hx + 22, hy + 35 + 2 * math.sin(t * 60)), (hx + 56, hy + 35)], (0.6, 0.6, 0.65), 2)
    elif huff or m:
        o = max(m, huff)
        ctx.save()
        ctx.translate(hx + 40, hy + 34)
        ctx.scale(1, 0.4 + 0.8 * o)
        circle(ctx, 0, 0, 12, hexc("#5A1A1A"))
        ctx.restore()
    else:                                  # cocky grin
        ctx.arc(hx + 38, hy + 22, 18, 0.2, math.pi * 0.8)
        rgba(ctx, hexc("#5A1A1A"))
        ctx.set_line_width(5)
        ctx.stroke()
    if freeze > 0.3:                       # icicles off the nose and chin
        for k, (ix, iy, ln) in enumerate(((hx + 58, hy + 18, 26), (hx + 30, hy + 52, 34), (hx + 10, hy + 56, 22))):
            L = ln * clamp((freeze - 0.3) / 0.5)
            ctx.move_to(ix - 5, iy)
            ctx.line_to(ix, iy + L)
            ctx.line_to(ix + 5, iy)
            ctx.close_path()
            rgba(ctx, (0.85, 0.96, 1.0), 0.95)
            ctx.fill()
    if pose == "proud":
        arm(ctx, [(70, -340), (128, -272), (86, -222)], TEE, skin, w=30)
    elif pose == "egg":
        arm(ctx, [(70, -340), (140, -310), (182, -330)], TEE, skin, w=30)
        if egg_in_hand:
            egg(ctx, 196, -352, 0)
    elif pose == "salute":
        arm(ctx, [(-70, -340), (-112, -268), (-94, -205)], shade(TEE, 0.8), skin, w=30)
        arm(ctx, [(70, -340), (134, -400), (hx + 32, hy - 34)], TEE, skin, w=28)
    else:
        arm(ctx, [(70, -340), (92, -262), (84, -200)], TEE, skin, w=30)
    if huff:                               # vapour puffs drifting out of the mouth
        for k in range(4):
            u = (t * 1.6 + k / 4) % 1.0
            circle(ctx, hx + 70 + 110 * u, hy + 30 - 30 * u, 10 + 26 * u, (1, 1, 1), 0.55 * (1 - u) * huff)
        dx, dy = hx - 46, hy - 40 + 40 * ((t * 1.3) % 1.0)          # sweat drop
        circle(ctx, dx, dy, 7, hexc("#BFE6FF"), 0.9 * huff)
    ctx.restore()
    if freeze > 0:                         # ice block closes round him
        k = clamp((freeze - 0.55) / 0.35)
        if k > 0:
            top = y - 580 * s
            hgt = (590 * s) * ease_out_cubic(k)
            rrect(ctx, x - 175 * s, y + 10 - hgt, 350 * s, hgt, 28)
            rgba(ctx, (0.75, 0.92, 1.0), 0.38)
            ctx.fill_preserve()
            rgba(ctx, (1, 1, 1), 0.85)
            ctx.set_line_width(5)
            ctx.stroke()
            if k > 0.6:
                for j in range(3):
                    line(ctx, [(x - 120 * s + 40 * j, top + 60 + 30 * j), (x - 60 * s + 40 * j, top + 10 + 30 * j)],
                         (1, 1, 1), 6, 0.6)


def egg(ctx, x, y, rot, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(0.78, 1.0)
    circle(ctx, 0, 0, 24, hexc("#F3E6D2"), a)
    circle(ctx, -8, -8, 7, (1, 1, 1), 0.7 * a)
    ctx.restore()


def rock(ctx, x, y):
    ctx.move_to(x - 90, y)
    ctx.curve_to(x - 96, y - 50, x - 40, y - 74, x + 10, y - 70)
    ctx.curve_to(x + 70, y - 66, x + 100, y - 30, x + 92, y)
    ctx.close_path()
    rgba(ctx, hexc("#55606D"))
    ctx.fill()
    ctx.move_to(x - 60, y - 52)
    ctx.curve_to(x - 20, y - 70, x + 30, y - 68, x + 70, y - 46)
    rgba(ctx, hexc("#EEF6FB"))
    ctx.set_line_width(12)
    ctx.stroke()


def hammer(ctx, x, y, ang):
    """Hammer pivoting at (x, y), head at the end; ang 0 = head straight down."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    line(ctx, [(0, 0), (0, 150)], hexc("#8B5A2B"), 16)
    rrect(ctx, -46, 140, 92, 46, 8)
    rgba(ctx, hexc("#7D8894"))
    ctx.fill()
    ctx.restore()


def panel(ctx, u, title, c, y=330, w=760, h=170):
    """Readout card the props draw into; returns False until it has popped in."""
    if u <= 0:
        return False
    k = ease_out_back(clamp(u / 0.3))
    ctx.save()
    ctx.translate(540, y)
    ctx.scale(k, k)
    rrect(ctx, -w / 2, -h / 2, w, h, 22)
    rgba(ctx, PAL["panel"], 0.9)
    ctx.fill_preserve()
    rgba(ctx, c)
    ctx.set_line_width(5)
    ctx.stroke()
    text(ctx, title, -w / 2 + 30, -h / 2 + 28, 26, c, font=lego.MONO, anchor="l")
    ctx.restore()
    return True


def thermo(ctx, value, u):
    if not panel(ctx, u, "TEMPERATURE // SIACHEN", ICE):
        return
    k = ease_out_back(clamp(u / 0.3))
    ctx.save()
    ctx.translate(540, 330)
    ctx.scale(k, k)
    rrect(ctx, -330, 18, 360, 26, 13)                 # mercury track, +30 (right) .. -60 (left)
    rgba(ctx, (1, 1, 1), 0.15)
    ctx.fill()
    f = clamp((value + 60) / 90)
    c = mix(ICE, RED, clamp((value + 10) / 35))
    rrect(ctx, -330, 18, max(26, 360 * f), 26, 13)
    rgba(ctx, c)
    ctx.fill()
    circle(ctx, -330, 31, 26, c)
    text(ctx, f"{int(round(value)):+d}°C".replace("+0", "0"), 330, 10, 104, c, font=CAPTION_FONT, bold=False,
         anchor="r", stroke=(0, 0, 0), stroke_w=8)
    ctx.restore()


def o2_meter(ctx, frac, u, lab):
    if not panel(ctx, u, "OXYGEN // HAR SAANS", HI):
        return
    k = ease_out_back(clamp(u / 0.3))
    ctx.save()
    ctx.translate(540, 330)
    ctx.scale(k, k)
    for i in range(10):
        fill = clamp(frac * 10 - i)
        rrect(ctx, -330 + i * 50, -6, 40, 64, 8)
        rgba(ctx, (1, 1, 1), 0.12)
        ctx.fill()
        if fill > 0:
            rrect(ctx, -330 + i * 50, -6 + 64 * (1 - fill), 40, 64 * fill, 8)
            rgba(ctx, mix(RED, ICE, frac * 1.6))
            ctx.fill()
    text(ctx, lab, 330, 26, 62, INK, font=CAPTION_FONT, bold=False, anchor="r", stroke=(0, 0, 0), stroke_w=6)
    ctx.restore()


# ============================================================ scenes

class Scene(Cued):
    """Adds speaker lookup: which character's caption is on screen, and is he still talking."""

    def speaking(self, t):
        for s in engine.SCENES:
            if s["obj"] is self:
                cur, nxt = None, None
                for i, (st, cap) in enumerate(s["captions"]):
                    if t >= st - 0.03:
                        cur = (st, cap)
                        nxt = s["captions"][i + 1][0] if i + 1 < len(s["captions"]) else None
                if cur is None:
                    return None
                who, cap = lego.split_speaker(cur[1])
                end = min(cur[0] + 0.3 * len(cap.split()) + 0.15, nxt if nxt else 1e9)
                return who if t < end else None
        return None


class Hook(Scene):
    def beats(self, d):
        c = self.cue
        return {"m": c("MINUS", 0.05), "g": c("BAS", d * 0.3), "ts": c("T-SHIRT", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "whoosh"), (b["m"] + 0.1, "zap"), (b["m"] + 0.9, "thud"), (b["g"] - 0.6, "pop"),
                (b["ts"], "pick")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        who = self.speaking(t)
        scenery(ctx, t, wind=1.5)
        v = lerp(25, -50, ease_in_out(clamp((t - b["m"]) / 0.9)))
        thermo(ctx, v, t - b["m"] + 0.25)
        major(ctx, MAJOR_X, GY, t, pose="point" if t > b["g"] else "stand", talk=who == "M")
        k = ease_out_cubic(clamp((t - (b["g"] - 0.9)) / 0.9))
        gx = lerp(1300, GAPPU_X, k)
        gappu(ctx, gx, GY, t, pose="proud" if k >= 1 else "stand", talk=who == "G",
              walk=t * 9 if k < 1 else None)
        if t > b["ts"]:
            tag(ctx, "T-SHIRT + CHAPPAL", GAPPU_X, 560, GAPPU_C, t - b["ts"], size=34)


class Freeze(Scene):
    def beats(self, d):
        c = self.cue
        return {"s": c("SIACHEN", 0.3), "g": c("MAJOR", d * 0.35), "jam": c("BARAF", d * 0.5),
                "fb": c("FROSTBITE", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(b["s"], "beep"), (b["jam"], "zap"), (b["jam"] + 0.4, "pick"), (b["fb"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        who = self.speaking(t)
        scenery(ctx, t, wind=2.0)
        f = 0.25 * clamp(t / 1.0) + 0.75 * ease_in_out(clamp((t - b["jam"] + 0.2) / 0.8))
        tag(ctx, "SIACHEN", 540, 300, ICE, t - b["s"], size=60, sub="DUNIYA KA SABSE OONCHA JANG KA MAIDAAN")
        major(ctx, MAJOR_X, GY, t, pose="point", talk=who == "M")
        gappu(ctx, GAPPU_X, GY, t, pose="stand", talk=who == "G" and f < 0.5, freeze=f)
        if t > b["fb"]:
            stamp(ctx, 540, 470, t - b["fb"], -0.04, 560, 170, RED,
                  [("FROSTBITE", -28, 84, RED), ("KUCH MINUTE MEIN", 46, 44, INK)])


class Air(Scene):
    def beats(self, d):
        c = self.cue
        return {"go": c("CHALO", 0.05), "ft": c("21,000", d * 0.3), "o2": c("AADHI", d * 0.55),
                "tm": c("TREADMILL", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(b["go"], "whoosh"), (b["ft"], "beep"), (b["o2"], "alarm"), (b["tm"], "pop")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        who = self.speaking(t)
        huff = clamp((t - b["ft"]) / 1.2)
        scenery(ctx, t, wind=1.2, scroll=t * 1.1)
        frac = lerp(1.0, 0.45, ease_in_out(clamp((t - b["o2"]) / 0.8)))
        o2_meter(ctx, frac, t - b["ft"] + 0.2, "SEA LEVEL" if t < b["o2"] else "< 1/2")
        if t > b["ft"]:
            tag(ctx, "21,000 FT", 540, 520, HI, t - b["ft"], size=44, sub="CHAUKIYAAN")
        major(ctx, MAJOR_X, GY, t, pose="stand", talk=who == "M")
        gappu(ctx, GAPPU_X, GY, t, pose="stand", talk=who == "G", huff=huff, walk=t * (10 - 4 * huff))
        if t > b["tm"]:
            tag(ctx, "TREADMILL?", GAPPU_X, 600, GAPPU_C, t - b["tm"], size=36)


ROCK_X = 545


class Egg(Scene):
    def beats(self, d):
        c = self.cue
        return {"le": c("LE.", d * 0.2), "tap": c("PATHAR", d * 0.35), "ham": c("HATHAUDA", d * 0.6), "k": c("KANCHA", d * 0.82)}

    def events(self, d):
        b = self.beats(d)
        return [(b["tap"], "pick"), (b["tap"] + 0.35, "pick"), (b["ham"] + 0.35, "thud"), (b["ham"] + 0.4, "pick"),
                (b["k"], "pop")]

    def egg_pos(self, t, b):
        """Egg path: in Gappu's hand -> lands on the rock and bounces -> jumps when the hammer hits -> rolls off."""
        hand = (GAPPU_X - 196, GY - 352)
        top = (ROCK_X, GY - 94)
        if t < b["tap"]:
            return hand, 0.0, t > b["le"]
        u = t - b["tap"]
        if u < 0.35:
            k = ease_in_out(u / 0.35)
            return (lerp(hand[0], top[0], k), lerp(hand[1], top[1], k) - 80 * math.sin(math.pi * k)), u * 6, False
        hit = b["ham"] + 0.35
        if t < hit:
            v = t - b["tap"] - 0.35
            return (top[0], top[1] - 70 * abs(math.sin(v * 7)) * math.exp(-v * 3)), 0.0, False
        v = t - hit
        if t < b["k"]:
            return (top[0], top[1] - 160 * abs(math.sin(v * 5)) * math.exp(-v * 2)), v * 4, False
        w = t - b["k"]
        return (top[0] - 200 * ease_out_cubic(clamp(w / 1.2)), top[1] + 60 * clamp(w / 0.3)), w * 9, False

    def draw(self, ctx, t, d):
        b = self.beats(d)
        who = self.speaking(t)
        scenery(ctx, t, wind=1.0)
        rock(ctx, ROCK_X, GY - 10)
        major(ctx, MAJOR_X - 40, GY, t, pose="open" if who == "M" else "stand", talk=who == "M")
        (ex, ey), rot, held = self.egg_pos(t, b)
        gappu(ctx, GAPPU_X, GY, t, pose="egg" if t < b["tap"] + 0.4 else "stand", talk=who == "G",
              egg_in_hand=held)
        if not held and t >= b["tap"]:      # before Major hands it over there is no egg at all
            egg(ctx, ex, ey, rot)
        u = t - b["ham"]
        if 0 < u < 1.4:                   # hammer swings down on the egg, then lifts away
            ang = lerp(-1.6, 0.0, ease_in_out(clamp(u / 0.35))) if u < 0.6 else lerp(0.0, -1.2, clamp((u - 0.6) / 0.6))
            hammer(ctx, ROCK_X - 150, GY - 300, ang - 0.6)
        for at in (b["tap"] + 0.35, b["ham"] + 0.35):
            v = t - at
            if 0 < v < 0.6:
                text(ctx, "TONK!", ROCK_X + 130, GY - 200 - 60 * v, 64 + 30 * v, HI, font=CAPTION_FONT, bold=False,
                     a=1 - v / 0.6, stroke=(0, 0, 0), stroke_w=8)
        if t > b["ham"] + 0.5:
            stamp(ctx, 540, 360, t - b["ham"] - 0.5, 0.03, 560, 150, HI,
                  [("ANDA = PATHAR", 0, 84, HI)])


class Salute(Scene):
    def beats(self, d):
        c = self.cue
        return {"j": c("JAWAN", 0.1), "y": c("1984", d * 0.25), "din": c("DIN", d * 0.6), "s": c("SALUTE", d * 0.88)}

    def events(self, d):
        b = self.beats(d)
        return [(b["j"], "whoosh"), (b["y"], "beep"), (b["din"], "boom"), (b["s"], "dingdong")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        who = self.speaking(t)
        scenery(ctx, t, wind=0.8, flag_a=ease_out_cubic(clamp((t - b["j"]) / 0.6)), dark=0.2)
        glow(ctx, 600, 300, 300, SAFFRON, 0.15 * clamp((t - b["j"]) / 0.6))
        if t > b["y"]:
            tag(ctx, "13 APRIL 1984", 540, 520, SAFFRON, t - b["y"], size=46, sub="OPERATION MEGHDOOT")
        major(ctx, MAJOR_X, GY, t, pose="salute" if t > b["j"] + 0.3 else "stand", talk=who == "M")
        gappu(ctx, GAPPU_X, GY, t, pose="salute" if t > b["s"] else "stand", talk=who == "G")
        if t > b["din"]:
            stamp(ctx, 528, 830, t - b["din"], -0.03, 300, 110, SAFFRON, [("42 SAAL SE", 0, 66, SAFFRON)])


class Ask(Scene):
    def beats(self, d):
        c = self.cue
        return {"q": c("BATA", d * 0.4), "cmt": c("COMMENT", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["q"] + 0.05, "pop"), (b["cmt"], "dingdong"), (b["cmt"] + 1.1, "pick")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        who = self.speaking(t)
        scenery(ctx, t, wind=1.6)
        k = ease_in_out(clamp((t - b["q"]) / 0.4))
        s = lerp(1.0, 0.62, k)
        major(ctx, lerp(MAJOR_X, 230, k), GY, t, pose="point" if who == "M" else "stand", talk=who == "M", s=s)
        gappu(ctx, lerp(GAPPU_X, 850, k), GY, t, pose="blanket", s=s)
        lego.ending(STORY, ctx, t, t - b["q"], t - b["cmt"], question=("EK RAAT TIK", "PAATE?"),
                    options=("HAAN", "NAA"), y=480)


SCENE_CLASSES = {"hook": Hook, "freeze": Freeze, "air": Air, "egg": Egg, "salute": Salute, "ask": Ask}
STORY = importlib.import_module(__name__)


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
        "Siachen Me Minus 50°C: T-Shirt Me Ek Raat?",
        "Minus 50°C Wala Siachen: Yahan Anda Bhi Pathar",
        "Siachen Glacier Ka Sach: Minus 50°C Aur Aadhi Oxygen",
        "Siachen Me Ek Raat Tik Paoge? Minus 50°C",
        "Duniya Ka Sabse Ooncha Jang Ka Maidaan: Siachen",
        "Siachen Temperature Minus 50: Jawan Kaise Rehte Hain",
        "21,000 Feet, Minus 50°C: Siachen Ka Sach",
        "Siachen Me Anda Hathaude Se Bhi Nahi Tootta",
        "Siachen Glacier: 42 Saal Se Har Din Duty",
        "T-Shirt Me Siachen? Gappu Ka Bura Haal",
        "T-Shirt Me Siachen? Ek Raat Tik Paoge?",
    ],
    "title": "T-Shirt Me Siachen? Ek Raat Tik Paoge?",   # thumbnail carries the -50°C, title the dare
    "thumb_text": "MINUS 50°C",
    "queries": ["siachen", "siachen temperature", "siachen glacier"],
    "description": """
Siachen glacier, minus 50°C: duniya ka sabse ooncha jang ka maidaan. Siachen temperature me ek raat T-shirt me?
Gappu ne koshish ki, Major Saab ne samjhaya ki wahan jawan kaise rehte hain.

Is Short me:
• Siachen me temperature minus 50°C se bhi neeche chala jata hai
• Khuli chamdi pe kuch hi minute me frostbite
• 21,000 feet tak ki chaukiyaan: har saans me aadhi se bhi kam oxygen
• Anda pathar jaisa jam jata hai, hathaude se bhi nahi tootta (2019 me jawanon ka video)
• 13 April 1984, Operation Meghdoot: tab se 42 saal, har din jawan wahin date hain

Aap Siachen me ek raat tik paate? HAAN ya NAA, comment me likho.
Agni missile ki range wala Short bhi dekho, Reality Shift pe.

Note: Major Saab aur Gappu cartoon characters hain, kisi asli insaan pe based nahi. Temperature aur oonchai ke
figures alag-alag sources me thode alag hain; yahan commonly reported numbers liye gaye hain.
""",
    "tags": ["siachen", "siachen glacier", "siachen temperature", "siachen army", "siachen minus 50",
             "operation meghdoot", "indian army", "highest battlefield", "siachen jawan", "siachen life",
             "indian army shorts", "defence hindi", "fauji life", "reality shift"],
    "hashtags": ["#Shorts", "#Siachen", "#IndianArmy"],
}


def thumbnail(ctx):
    """1080x1920 cover: 'MINUS 50°C' over Gappu frozen in an ice block, Major Saab beside him."""
    scenery(ctx, 0.4, wind=2.0)
    major(ctx, 300, 1500, 0.4, pose="point", s=1.25)
    gappu(ctx, 770, 1500, 0.4, freeze=1.0, s=1.25)
    g = cairo.LinearGradient(0, 0, 0, 760)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.9)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 760)
    ctx.set_source(g)
    ctx.fill()
    vignette(ctx)
    glow(ctx, 540, 360, 520, ICE, 0.25)
    text(ctx, "MINUS", 540, 250, 220, INK, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "50°C", 540, 490, 250, ICE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    tag(ctx, "SIACHEN", 540, 680, RED, 1.0, size=56)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, INK, a=0.7)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.siachen")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
