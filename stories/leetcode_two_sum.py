"""Story: LeetCode #1 Two Sum — brute force O(N²) vs one-pass hash map O(N), as a 32 s coding Short.

Split screen: an animated coder on the left, a dark-mode IDE / whiteboard on the right running the
dry-run. Captions sit in the 1150-1250 px band; nothing is drawn in the bottom 400 px (YouTube UI).
"""

import math

import cairo

from engine import *  # noqa: F401,F403
from engine import _pt
from stories.reality_shift import stamp
from stories.reality_shift_defense import Cued, flash

TOPIC = "LEETCODE #1 · EASY"
WATERMARK = "TWO SUM"
OUTPUTS = {"edge": "leetcode_two_sum_32s.mp4", "elevenlabs": "leetcode_two_sum_32s_el.mp4"}
OUTPUT_DIR = OUT_DIR

CLEAN_PUNCTUATION = False
MAX_GAP = 0.2
TAIL_PAD = 0.12
TRIM = {"thresh": 0.006, "keep": 0.05, "keep_tail": 0.08}
MUSIC_BPM = 120
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"

YELLOW = hexc("#FFE14D")
CYAN = hexc("#22E4FF")
RED = hexc("#FF3B4E")
GREEN = hexc("#3CFF8F")
ORANGE = hexc("#FF9F43")
CAPTION_Y = 1200           # centre of the 1150-1250 safe band
CAPTION_SIZE = 112
HOT_COLOR = YELLOW
HOT_COLORS = {"TWO": YELLOW, "SUM": YELLOW, "O(N²)": YELLOW, "BARBAAD": YELLOW, "PASS": YELLOW,
              "FOLLOW": YELLOW, "HASH": CYAN, "MAP": CYAN, "O(N)": CYAN, "LINEAR": CYAN, "7": CYAN,
              "2": CYAN, "COMMENT": CYAN}
HOT_WORDS = set(HOT_COLORS)

NARRATION = {
    "hook": "क्या आप भी टू सम में दो-दो फॉर लूप लगाकर इंटरव्यूअर का दिमाग खराब कर रहे हैं?",
    "brute": "ब्रूट फोर्स तरीका हर एक जोड़े को चेक करेगा—जिसमें आपका O of N squared टाइम फालतू में बर्बाद होगा!",
    "hashmap": "असली ट्रिक है हैश मैप! हर नंबर पर बस ये पूछो: टारगेट माइनस करंट नंबर पहले से मैप में है या "
               "नहीं? सात आते ही दो मिल गया, और सिर्फ एक ही पास में खेल खत्म!",
    "outro": "टाइम कॉम्प्लेक्सिटी सीधा लीनियर O of N! अगला इंटरव्यू क्वेश्चन कौन सा सॉल्व करवाएं? कमेंट में बताएं "
             "और फॉलो करें!",
}

CHUNKS = {
    "hook": [
        ("क्या आप भी", "KYA AAP BHI"),
        ("टू सम में", "TWO SUM MEIN"),
        ("दो-दो फॉर लूप", "DO-DO FOR LOOP"),
        ("लगाकर", "LAGAKAR"),
        ("इंटरव्यूअर का", "INTERVIEWER KA"),
        ("दिमाग खराब", "DIMAAG KHARAB"),
        ("कर रहे हैं?", "KAR RAHE HAIN?"),
    ],
    "brute": [
        ("ब्रूट फोर्स तरीका", "BRUTE FORCE TAREEKA"),
        ("हर एक जोड़े को", "HAR EK JODE KO"),
        ("चेक करेगा—जिसमें", "CHECK KAREGA"),
        ("आपका", "JISMEIN AAPKA"),
        ("O of N squared", "O(N²)"),
        ("टाइम फालतू में", "TIME FAALTU MEIN"),
        ("बर्बाद होगा!", "BARBAAD HOGA!"),
    ],
    "hashmap": [
        ("असली ट्रिक है", "ASLI TRICK HAI"),
        ("हैश मैप!", "HASH MAP!"),
        ("हर नंबर पर", "HAR NUMBER PAR"),
        ("बस ये पूछो:", "BAS YE POOCHHO:"),
        ("टारगेट माइनस", "TARGET MINUS"),
        ("करंट नंबर", "CURRENT NUMBER"),
        ("पहले से मैप में", "PEHLE SE MAP MEIN"),
        ("है या नहीं?", "HAI YA NAHI?"),
        ("सात आते ही", "7 AATE HI"),
        ("दो मिल गया,", "2 MIL GAYA!"),
        ("और सिर्फ", "AUR SIRF"),
        ("एक ही पास में", "EK HI PASS MEIN"),
        ("खेल खत्म!", "KHEL KHATAM!"),
    ],
    "outro": [
        ("टाइम कॉम्प्लेक्सिटी", "TIME COMPLEXITY"),
        ("सीधा लीनियर", "SEEDHA LINEAR"),
        ("O of N!", "O(N)!"),
        ("अगला इंटरव्यू क्वेश्चन", "AGLA INTERVIEW QUESTION"),
        ("कौन सा", "KAUN SA"),
        ("सॉल्व करवाएं?", "SOLVE KARWAYEIN?"),
        ("कमेंट में बताएं", "COMMENT MEIN BATAYEIN"),
        ("और फॉलो करें!", "AUR FOLLOW KAREIN!"),
    ],
}

for _key, _chunks in CHUNKS.items():
    assert " ".join(h for h, _ in _chunks) == NARRATION[_key], f"caption chunks drift from narration: {_key}"

SCRIPT = [(key, CHUNKS[key]) for key in NARRATION]

STAMP_Y = 330              # HUD text lives in the top band, clear of captions and the YouTube UI
FLOOR_Y = 1110
CHAR_X = 225
PANEL = (440, 470, 600, 640)   # IDE window: x, y, w, h
MONO = "Consolas"
NUMS = (2, 7, 11, 15)
TARGET = 9


# ============================================================ coder character

HOODIE = hexc("#3B5BFF")
JEANS = hexc("#1D2540")
HAIR = hexc("#17100D")
SKIN_C = hexc("#D9A066")

# arm angles (back upper, back fore, front upper, front fore): 0 = straight down, +ve = toward the board
POSES = {
    "confused": (-2.26, 2.48, 2.26, -2.48),   # hands on head
    "explain": (-0.15, 0.25, 0.95, 1.95),
    "point": (-0.15, 0.3, 2.05, 2.2),         # arm out at the whiteboard
    "cheer": (-2.75, -3.0, 2.75, 3.0),
    "down": (-0.15, 0.25, 0.75, 0.55),        # pointing down at the follow button
}


def wiggle(name, t):
    if name == "confused":
        return (0.06 * math.sin(t * 9), 0, -0.06 * math.sin(t * 9), 0)
    if name == "explain":
        return (0, 0, 0.12 * math.sin(t * 4.5), 0.3 * math.sin(t * 6))
    if name == "point":
        return (0, 0, 0.04 * math.sin(t * 3), 0.05 * math.sin(t * 3))
    if name == "cheer":
        k = math.sin(t * 10)
        return (-0.18 * k, -0.25 * k, 0.18 * k, 0.25 * k)
    return (0, 0, 0.06 * math.sin(t * 7), 0.1 * math.sin(t * 7))


def pose_angles(sched, t):
    """Blend from the previous pose into the current one over 0.3 s; sched = [(start, pose), ...]."""
    i = max(k for k, (s, _) in enumerate(sched) if s <= t or k == 0)
    start, name = sched[i]
    prev = sched[i - 1][1] if i else name
    k = ease_in_out((t - start) / 0.3)
    a = [lerp(p, c, k) for p, c in zip(POSES[prev], POSES[name])]
    w = wiggle(name, t)
    return [x + dx for x, dx in zip(a, w)]


def coder(ctx, x, y, s, t, arms, mood="ok"):
    """Chibi developer (hoodie, glasses) standing on (x, y), facing the board on the right."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.save()
    ctx.scale(1, 0.16)
    circle(ctx, 10, 0, 120, (0, 0, 0), 0.4)
    ctx.restore()
    for dx, dim in ((-24, 0.75), (24, 1.0)):
        line(ctx, [(dx, -170), (dx * 1.1, -22)], shade(JEANS, dim), 42)
        rrect(ctx, dx * 1.1 - 22, -30, 64, 30, 14)
        rgba(ctx, shade(hexc("#F2F4F8"), dim))
        ctx.fill()
        ctx.rectangle(dx * 1.1 - 22, -8, 64, 8)
        rgba(ctx, shade(RED, dim))
        ctx.fill()
    sy = -330
    a1, a2, a3, a4 = arms

    def arm(sh, up, fore, dim):
        el = _pt(sh, up, 76)
        hd = _pt(el, fore, 70)
        line(ctx, [sh, el, hd], shade(HOODIE, dim), 34)
        circle(ctx, hd[0], hd[1], 19, shade(SKIN_C, dim))
        return el, hd

    arm((-56, sy + 22), a1, a2, 0.7)
    # torso: hoodie with pocket, strings and a </> logo
    rrect(ctx, -80, sy, 160, 200, 54)
    rgba(ctx, HOODIE)
    ctx.fill()
    rrect(ctx, -52, sy + 120, 104, 52, 18)
    rgba(ctx, shade(HOODIE, 0.8))
    ctx.fill()
    for dx in (-16, 16):
        line(ctx, [(dx, sy + 14), (dx * 1.2, sy + 70)], (0.95, 0.95, 1), 5)
    text(ctx, "</>", 22, sy + 92, 30, CYAN, font=MONO)
    # head
    hx, hy = 8, sy - 92
    ctx.rectangle(hx - 20, hy + 50, 40, 40)
    rgba(ctx, shade(SKIN_C, 0.85))
    ctx.fill()
    circle(ctx, hx - 62, hy + 8, 17, shade(SKIN_C, 0.9))
    circle(ctx, hx, hy, 74, SKIN_C)
    ctx.move_to(hx - 78, hy + 4)
    ctx.arc(hx, hy - 4, 78, math.pi, 2 * math.pi)
    for k in range(6):                                          # spiky fringe
        px = hx + 78 - k * 30
        ctx.line_to(px - 8, hy - 30 + 10 * (k % 2))
        ctx.line_to(px - 22, hy - 4)
    ctx.close_path()
    rgba(ctx, HAIR)
    ctx.fill()
    for k in range(5):                                          # top spikes
        a = math.pi * (1.1 + 0.2 * k)
        bx, by = hx + 70 * math.cos(a), hy - 4 + 70 * math.sin(a)
        ctx.move_to(bx - 18 * math.sin(a), by + 18 * math.cos(a))
        ctx.line_to(hx + 98 * math.cos(a + 0.08), hy - 4 + 98 * math.sin(a + 0.08))
        ctx.line_to(bx + 18 * math.sin(a), by - 18 * math.cos(a))
        ctx.close_path()
    ctx.fill()
    # glasses + eyes
    blink = (t % 3.3) < 0.12
    for ex in (hx - 8, hx + 46):
        rrect(ctx, ex - 25, hy - 4, 50, 40, 12)
        rgba(ctx, CYAN, 0.14)
        ctx.fill_preserve()
        rgba(ctx, (0.08, 0.08, 0.1))
        ctx.set_line_width(6)
        ctx.stroke()
        if blink:
            line(ctx, [(ex - 9, hy + 16), (ex + 9, hy + 16)], (0.08, 0.08, 0.1), 4)
        else:
            look = 4 if mood != "confused" else 3 * math.sin(t * 7)
            circle(ctx, ex + look, hy + 16, 7.5, (0.08, 0.08, 0.1))
            circle(ctx, ex + look + 2.5, hy + 13, 2.2, (1, 1, 1))
    line(ctx, [(hx + 17, hy + 12), (hx + 21, hy + 12)], (0.08, 0.08, 0.1), 5)
    line(ctx, [(hx - 33, hy + 8), (hx - 62, hy + 2)], (0.08, 0.08, 0.1), 5)
    # brows
    if mood == "confused":
        line(ctx, [(hx - 28, hy - 22), (hx + 8, hy - 14)], HAIR, 7)
        line(ctx, [(hx + 30, hy - 12), (hx + 66, hy - 26)], HAIR, 7)
    else:
        lift = 6 if mood == "happy" else 0
        line(ctx, [(hx - 26, hy - 16 - lift), (hx + 8, hy - 20 - lift)], HAIR, 7)
        line(ctx, [(hx + 30, hy - 20 - lift), (hx + 64, hy - 16 - lift)], HAIR, 7)
    # mouth: talking flap, wavy when confused, grin when happy
    mx, my = hx + 22, hy + 50
    talk = abs(math.sin(t * 13)) * (0.5 + 0.5 * abs(math.sin(t * 3.1)))
    if mood == "confused":
        pts = [(mx - 22 + i * 4, my + 4 * math.sin(i * 1.3 + t * 8)) for i in range(12)]
        line(ctx, pts, (0.35, 0.08, 0.08), 5)
    else:
        ctx.save()
        ctx.translate(mx, my)
        ctx.scale(1, 0.25 + talk * (0.9 if mood == "happy" else 0.7))
        ctx.arc(0, 0, 20, 0, math.pi) if mood == "happy" else ctx.arc(0, 0, 16, 0, 2 * math.pi)
        ctx.restore()
        rgba(ctx, (0.4, 0.08, 0.1))
        ctx.fill()
    if mood == "confused":                                      # sweat drops sliding off
        for k in range(2):
            u = (t * 0.9 + k * 0.5) % 1
            dx, dy = hx - 70 - k * 20, hy - 40 + 90 * u
            ctx.move_to(dx, dy - 16)
            ctx.curve_to(dx + 12, dy, dx + 10, dy + 12, dx, dy + 12)
            ctx.curve_to(dx - 10, dy + 12, dx - 12, dy, dx, dy - 16)
            rgba(ctx, hexc("#8FE3FF"), 0.9 * (1 - u))
            ctx.fill()
    _, hand = arm((56, sy + 22), a3, a4, 1.0)
    hand = ctx.user_to_device(*hand)
    ctx.restore()
    return hand


# ============================================================ IDE / whiteboard

KEYWORDS = {"def", "for", "in", "if", "return", "range", "not", "and"}


def mono_line(ctx, s, x, y, size, a=1.0, color=None):
    """Syntax-coloured monospace line with its baseline at y."""
    ctx.select_font_face(MONO, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)
    adv = ctx.text_extents("M")[4]
    col, word = 0, ""
    tokens, cur = [], ""
    for ch in s + " ":                                          # split into words / single symbols
        if ch.isalnum() or ch == "_":
            cur += ch
            continue
        if cur:
            tokens.append(cur)
            cur = ""
        tokens.append(ch)
    tokens = tokens[:-1]
    for tok in tokens:
        if color is not None:
            c = color
        elif tok in KEYWORDS:
            c = hexc("#FF7AC6")
        elif tok.isdigit():
            c = hexc("#FFB86C")
        elif tok[0].isalpha() or tok[0] == "_":
            c = hexc("#E6EDF3") if tok not in ("nums", "target", "seen") else hexc("#79C0FF")
        else:
            c = hexc("#8B949E")
        if not tok.isspace():
            rgba(ctx, c, a)
            ctx.move_to(x + col * adv, y)
            ctx.show_text(tok)
        col += len(tok)
    return adv


def code_block(ctx, lines, x, y, t0, t, size=23, lh=42, cps=60, hl=(), hl_c=RED):
    """Lines typed in from t0 at cps chars/s; hl = indices of lines to highlight."""
    shown = max(0, int((t - t0) * cps))
    ctx.select_font_face(MONO, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)
    adv = ctx.text_extents("M")[4]
    for i, s in enumerate(lines):
        ly = y + i * lh
        if i in hl:
            rrect(ctx, x - 56, ly - size * 0.95, PANEL[2] - 30, lh - 2, 6)
            rgba(ctx, hl_c, 0.18 + 0.08 * math.sin(t * 8))
            ctx.fill()
            pts = [(x + (len(s) - len(s.lstrip())) * adv + k * 8, ly + 8 + 3 * (-1) ** k)
                   for k in range(int(len(s.strip()) * adv / 8))]
            if len(pts) > 1:
                line(ctx, pts, hl_c, 2.5, 0.9)
        text(ctx, str(i + 1), x - 30, ly - size * 0.35, size * 0.8, hexc("#484F58"), font=MONO)
        vis = s[:max(0, shown)]
        shown -= len(s)
        mono_line(ctx, vis, x, ly, size)
        if 0 <= shown < 6 and len(vis) == len(s) or (0 < len(vis) < len(s)):
            if int(t * 3) % 2 == 0:                             # blinking cursor
                ctx.rectangle(x + len(vis) * adv + 2, ly - size * 0.85, 3, size)
                rgba(ctx, (1, 1, 1), 0.9)
                ctx.fill()


def ide(ctx, tab, t, border=CYAN):
    x, y, w, h = PANEL
    glow(ctx, x + w / 2, y + h / 2, 520, border, 0.18)
    rrect(ctx, x, y, w, h, 22)
    rgba(ctx, hexc("#0D1117"), 0.96)
    ctx.fill_preserve()
    rgba(ctx, border, 0.35 + 0.15 * math.sin(t * 4))
    ctx.set_line_width(4)
    ctx.stroke()
    rrect(ctx, x, y, w, 58, 22)
    rgba(ctx, hexc("#161B22"))
    ctx.fill()
    ctx.rectangle(x, y + 36, w, 22)
    ctx.fill()
    for k, c in enumerate(("#FF5F56", "#FFBD2E", "#27C93F")):
        circle(ctx, x + 32 + k * 30, y + 29, 9, hexc(c))
    rrect(ctx, x + 132, y + 12, 220, 46, 10)
    rgba(ctx, hexc("#0D1117"))
    ctx.fill()
    line(ctx, [(x + 140, y + 14), (x + 344, y + 14)], border, 3)
    text(ctx, tab, x + 242, y + 36, 22, (0.85, 0.88, 0.92), font=MONO)


def cells(ctx, x0, y, cw, ch, gap, states, t, idx=True, vals=NUMS):
    """Array boxes for vals; states[i] = (border colour or None, pop scale)."""
    for i, v in enumerate(vals):
        c, pop = states[i]
        if pop <= 0:
            continue
        cx = x0 + i * (cw + gap) + cw / 2
        ctx.save()
        ctx.translate(cx, y)
        ctx.scale(pop, pop)
        if c is not None:
            glow(ctx, 0, 0, cw * 0.95, c, 0.45)
        rrect(ctx, -cw / 2, -ch / 2, cw, ch, 14)
        rgba(ctx, hexc("#1B2230"))
        ctx.fill_preserve()
        rgba(ctx, c if c is not None else hexc("#3A4558"))
        ctx.set_line_width(6 if c is not None else 3)
        ctx.stroke()
        text(ctx, str(v), 0, 0, ch * 0.5, (1, 1, 1), font=MONO)
        if idx:
            text(ctx, str(i), 0, ch / 2 + 24, 22, hexc("#6E7681"), font=MONO)
        ctx.restore()


def cell_x(x0, cw, gap, i):
    return x0 + i * (cw + gap) + cw / 2


def arrow_head(ctx, x, y, ang, size, c, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.move_to(size, 0)
    ctx.line_to(-size * 0.6, -size * 0.7)
    ctx.line_to(-size * 0.6, size * 0.7)
    ctx.close_path()
    rgba(ctx, c, a)
    ctx.fill()
    ctx.restore()


def tick_mark(ctx, x, y, s, c, k=1.0):
    pts = [(x - s, y), (x - s * 0.3, y + s * 0.7), (x + s, y - s * 0.8)]
    if k < 1:
        seg = k * 2
        pts = pts[:1] + [(lerp(pts[0][0], pts[1][0], min(seg, 1)), lerp(pts[0][1], pts[1][1], min(seg, 1)))] + \
            ([(lerp(pts[1][0], pts[2][0], seg - 1), lerp(pts[1][1], pts[2][1], seg - 1))] if seg > 1 else [])
    line(ctx, pts, c, s * 0.32)


def cross_mark(ctx, x, y, s, c, a=1.0):
    line(ctx, [(x - s, y - s), (x + s, y + s)], c, s * 0.3, a)
    line(ctx, [(x + s, y - s), (x - s, y + s)], c, s * 0.3, a)


def chip(ctx, s, x, y, size, c, u, fill=(0.03, 0.04, 0.07), font=CAPTION_FONT, bold=False):
    """Rounded pill label that pops in (u = seconds since cue)."""
    if u < 0:
        return
    pop = max(ease_out_back(u / 0.28), 1e-3)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(pop, pop)
    w = text_width(ctx, s, size, font=font, bold=bold) + size * 1.1
    rrect(ctx, -w / 2, -size * 0.75, w, size * 1.5, size * 0.75)
    rgba(ctx, fill, 0.92)
    ctx.fill_preserve()
    rgba(ctx, c)
    ctx.set_line_width(4)
    ctx.stroke()
    text(ctx, s, 0, 0, size, c, font=font, bold=bold)
    ctx.restore()


def siren(ctx, x, y, t, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for k in range(2):                                          # rotating beams
        a = t * 7 + k * math.pi
        ctx.move_to(0, -20)
        ctx.arc(0, -20, 150, a - 0.25, a + 0.25)
        ctx.close_path()
        rgba(ctx, RED, 0.22 * (0.5 + 0.5 * math.cos(a)))
        ctx.fill()
    glow(ctx, 0, -20, 90, RED, 0.5 + 0.3 * math.sin(t * 14))
    rrect(ctx, -44, 18, 88, 22, 6)
    rgba(ctx, hexc("#3A3F4B"))
    ctx.fill()
    ctx.move_to(-32, 20)
    ctx.arc(0, 20 - 4, 32, math.pi, 2 * math.pi)
    ctx.line_to(32, 20)
    ctx.close_path()
    rgba(ctx, RED)
    ctx.fill()
    circle(ctx, -10, -2, 8, (1, 0.8, 0.8), 0.8)
    ctx.restore()


def down_arrow(ctx, x, y, s, c):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for px, py in ((-30, -90), (30, -90), (30, 0), (72, 0), (0, 80), (-72, 0), (-30, 0)):
        ctx.line_to(px, py)
    ctx.close_path()
    rgba(ctx, c)
    ctx.fill_preserve()
    rgba(ctx, (0, 0, 0))
    ctx.set_line_width(7)
    ctx.stroke()
    ctx.restore()


def badge(ctx, x, y, u, w, h, c, lines, rot=0.0):
    """Glowing pulsing badge built on stamp()."""
    if u < 0:
        return
    pulse = 1 + 0.04 * math.sin(u * 7)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(pulse, pulse)
    glow(ctx, 0, 0, w * 0.7, c, 0.35)
    stamp(ctx, 0, 0, u, rot, w, h, c, lines)
    ctx.restore()


def interviewer(ctx, ax, ay, pop, t, heat):
    """Interviewer avatar whose face reddens and steams as heat goes 0 -> 1."""
    ctx.save()
    ctx.translate(ax, ay)
    ctx.scale(pop, pop)
    face = (lerp(0.85, 1.0, heat), lerp(0.65, 0.25, heat), lerp(0.45, 0.2, heat))
    rrect(ctx, -60, 50, 120, 70, 30)
    rgba(ctx, hexc("#2B2F3A"))
    ctx.fill()
    circle(ctx, 0, 0, 58, face)
    line(ctx, [(-34, -22), (-8, -10)], (0.1, 0.05, 0.05), 7)
    line(ctx, [(34, -22), (8, -10)], (0.1, 0.05, 0.05), 7)
    circle(ctx, -18, 4, 6, (0.1, 0.05, 0.05))
    circle(ctx, 18, 4, 6, (0.1, 0.05, 0.05))
    line(ctx, [(-20, 34), (0, 26), (20, 34)], (0.1, 0.05, 0.05), 6)
    if heat > 0:                                                # steam puffs
        for k in range(3):
            v = (t * 1.6 + k / 3) % 1
            circle(ctx, (k - 1) * 40 + 10 * math.sin(t * 5 + k), -70 - 80 * v, 14 + 16 * v,
                   (0.9, 0.9, 0.95), 0.6 * (1 - v) * heat)
    ctx.restore()
    text(ctx, "INTERVIEWER", ax, ay + 150, 22, hexc("#8B949E"), font=MONO)


# ============================================================ scenes

class Board(Cued):
    """Split screen: coder on the left, IDE on the right. Subclasses define beats, poses,
    board (inside the IDE) and hud (top band, outside the camera)."""
    accent = CYAN
    tab = "two_sum.py"
    border = CYAN
    mood = "ok"

    def beats(self, d):
        return {}

    def poses(self, d, b):
        return [(0.0, "explain")]

    def camera(self, ctx, t, d, b):
        pass

    def board(self, ctx, t, d, b):
        pass

    def hud(self, ctx, t, d, b):
        pass

    def extras(self, ctx, t, d, b):
        pass

    def draw(self, ctx, t, d):
        b = self.beats(d)
        backdrop(ctx, hexc("#0B1124"), hexc("#03050B"), self.accent, 740, 780, t, motes=30)
        for i in range(-2, 14):                                 # faint blueprint grid
            line(ctx, [(i * 90 + (t * 8) % 90, 0), (i * 90 + (t * 8) % 90, H)], (1, 1, 1), 1, 0.035)
            line(ctx, [(0, i * 120), (W, i * 120)], (1, 1, 1), 1, 0.035)
        ctx.save()
        self.camera(ctx, t, d, b)
        g = cairo.LinearGradient(0, FLOOR_Y, 0, FLOOR_Y + 140)
        g.add_color_stop_rgba(0, *self.accent, 0.18)
        g.add_color_stop_rgba(1, *self.accent, 0)
        ctx.rectangle(0, FLOOR_Y, PANEL[0] - 10, 140)
        ctx.set_source(g)
        ctx.fill()
        line(ctx, [(20, FLOOR_Y), (PANEL[0] - 30, FLOOR_Y)], self.accent, 3, 0.6)
        coder(ctx, CHAR_X, FLOOR_Y, 1.18, t, pose_angles(self.poses(d, b), t), self.mood_at(t, b))
        self.extras(ctx, t, d, b)
        ide(ctx, self.tab, t, self.border)
        self.board(ctx, t, d, b)
        ctx.restore()
        self.hud(ctx, t, d, b)

    def mood_at(self, t, b):
        return self.mood


class Hook(Board):
    """GOOGLE INTERVIEW TRAP sirens; panicking coder with hands on head; nested-loop code typing
    in and lighting up red; interviewer fuming."""
    accent = RED
    border = RED
    mood = "confused"
    CODE = ("def twoSum(nums, target):",
            "    for i in range(n):",
            "        for j in range(n):",
            "            if nums[i]+nums[j]==target:",
            "                return [i, j]")

    def beats(self, d):
        c = self.cue
        return {"two": c("TWO", d * 0.15), "loop": c("LOOP", d * 0.35), "dimaag": c("DIMAAG", d * 0.7)}

    def poses(self, d, b):
        return [(0.0, "confused")]

    def events(self, d):
        b = self.beats(d)
        return [(0.0, "boom"), (0.12, "alarm"), (b["loop"], "zap"), (b["dimaag"], "thud")] + \
            [(0.35 + 0.11 * k, "tick" if k % 2 else "tock") for k in range(10)]

    def extras(self, ctx, t, d, b):
        for k in range(3):                                      # ??? floating up off the head
            u = (t * 0.7 + k / 3) % 1
            text(ctx, "?", CHAR_X + (-150, 150, -110)[k], 650 - 110 * u, 64 + 10 * k, YELLOW, font=CAPTION_FONT,
                 bold=False, a=math.sin(math.pi * u), stroke=(0, 0, 0), stroke_w=6)

    def board(self, ctx, t, d, b):
        x, y, w, h = PANEL
        hl = (1, 2) if t >= b["loop"] else ()
        code_block(ctx, self.CODE, x + 62, y + 120, 0.3, t, hl=hl)
        chip(ctx, "NESTED LOOP", x + 440, y + 330, 30, RED, t - b["loop"])
        # interviewer losing it
        u = t - b["dimaag"] + 0.6
        if u > 0:
            ax, ay = x + 150, y + 500
            interviewer(ctx, ax, ay, max(ease_out_back(u / 0.3), 1e-3), t, clamp((t - b["dimaag"]) / 0.6))
            if t > b["dimaag"]:
                text(ctx, "WHY O(N²)?!", x + 410, ay, 46, RED, font=CAPTION_FONT, bold=False,
                     a=clamp((t - b["dimaag"]) / 0.2), stroke=(0, 0, 0), stroke_w=8)

    def hud(self, ctx, t, d, b):
        if int(t * 4) % 2 == 0:                                 # red alarm edge pulse
            for k in range(6):
                rrect(ctx, k * 6, k * 6, W - k * 12, H - 400 - k * 12, 30)
                rgba(ctx, RED, 0.06)
                ctx.set_line_width(14)
                ctx.stroke()
        stamp(ctx, 540, STAMP_Y, t - 0.05, -0.03, 820, 230, RED,
              [("GOOGLE INTERVIEW", -52, 74, (1, 1, 1)), ("TRAP", 54, 118, RED)])
        if t > 0.25:
            for sx in (540 - 215, 540 + 215):
                siren(ctx, sx, STAMP_Y + 40, t, 0.85 * ease_out_back((t - 0.25) / 0.3))


class Brute(Board):
    """Array [2, 7, 11, 15] with red nested-loop arcs crawling through every pair while an
    N x N check grid fills and a TIME WASTED bar climbs; O(N²) slams in."""
    accent = RED
    border = ORANGE
    tab = "brute_force.py"
    STEP = 0.42
    PAIRS = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    CW, GAP = 112, 18

    def beats(self, d):
        c = self.cue
        return {"jode": c("JODE", d * 0.2), "n2": c("O(N²)", d * 0.55), "barbaad": c("BARBAAD", d * 0.82)}

    def poses(self, d, b):
        return [(0.0, "explain"), (b["barbaad"], "confused")]

    def mood_at(self, t, b):
        return "confused" if t >= b["barbaad"] else "ok"

    def step_len(self, d, b):
        return self.STEP

    def step_k(self, t, d, b):
        """Index of the pair being checked at t (-1 before the sweep starts)."""
        return int((t - b["jode"]) / self.step_len(d, b)) if t >= b["jode"] else -1

    def steps(self, d, b):
        return self.step_k(d - 1e-6, d, b) + 1

    def events(self, d):
        b = self.beats(d)
        ev = [(0.05 + 0.18 * k, "pop") for k in range(4)]
        ev += [(b["jode"] + k * self.step_len(d, b), "tick" if k % 2 else "tock") for k in range(self.steps(d, b))]
        return ev + [(b["n2"], "boom"), (b["barbaad"], "alarm")]

    def board(self, ctx, t, d, b):
        x, y, w, h = PANEL
        code = ("for i in range(n):", "  for j in range(i+1, n):", "    check(nums[i], nums[j])")
        k = self.step_k(t, d, b)
        hl = ((0, 1)[k % 2],) if k >= 0 else ()
        code_block(ctx, code, x + 62, y + 108, 0.0, t, size=23, lh=40, cps=90, hl=hl, hl_c=ORANGE)
        x0 = x + (w - (4 * self.CW + 3 * self.GAP)) / 2
        ay = y + 330
        i = j = None
        if k >= 0:
            i, j = self.PAIRS[k % len(self.PAIRS)]
        states = []
        for n in range(4):
            c = RED if n == i else (ORANGE if n == j else None)
            states.append((c, ease_out_back((t - 0.05 - 0.18 * n) / 0.3)))
        cells(ctx, x0, ay, self.CW, 100, self.GAP, states, t)
        if k >= 0:                                              # nested-loop arc i -> j
            sl = self.step_len(d, b)
            u = ease_out_cubic(min(t - b["jode"] - k * sl, sl) / (sl * 0.6))
            xi, xj = cell_x(x0, self.CW, self.GAP, i), cell_x(x0, self.CW, self.GAP, j)
            top = ay - 70 - 40 * (j - i)
            pts = []
            for s in range(25):
                v = s / 24 * u
                pts.append(((1 - v) ** 2 * xi + 2 * (1 - v) * v * (xi + xj) / 2 + v * v * xj,
                            (1 - v) ** 2 * (ay - 55) + 2 * (1 - v) * v * top + v * v * (ay - 55)))
            line(ctx, pts, RED, 7)
            if len(pts) > 1:
                (px, py), (qx, qy) = pts[-2], pts[-1]
                arrow_head(ctx, qx, qy, math.atan2(qy - py, qx - px), 18, RED)
            text(ctx, "i", xi, ay + 92, 30, RED, font=MONO)
            text(ctx, "j", xj, ay + 92, 30, ORANGE, font=MONO)
        # N x N grid of checks + counter + time bar
        gx, gy, gc = x + 70, y + 470, 34
        text(ctx, "N × N", gx + 2 * gc + 6, gy - 30, 24, hexc("#8B949E"), font=MONO)
        done = k + 1
        lit = {self.PAIRS[s % len(self.PAIRS)] for s in range(done)}
        for r in range(4):
            for c_ in range(4):
                on = (r, c_) in lit or (c_, r) in lit or (r == c_ and done > 3)
                cur = (i, j) in ((r, c_), (c_, r))
                rrect(ctx, gx + c_ * (gc + 6), gy + r * (gc + 6), gc, gc, 6)
                rgba(ctx, RED if cur else (shade(RED, 0.55) if on else hexc("#1B2230")))
                ctx.fill()
        tx = x + 300
        text(ctx, "CHECKS", tx + 100, gy + 4, 26, hexc("#8B949E"), font=MONO)
        text(ctx, str(max(0, done)), tx + 100, gy + 62, 72, RED, font=CAPTION_FONT, bold=False)
        bar = clamp((t - b["jode"]) / max(d - b["jode"], 0.5))
        rrect(ctx, tx, gy + 112, 220, 26, 13)
        rgba(ctx, hexc("#1B2230"))
        ctx.fill()
        if bar > 0:
            rrect(ctx, tx, gy + 112, 220 * bar, 26, 13)
            rgba(ctx, RED, 0.7 + 0.3 * math.sin(t * 12))
            ctx.fill()
        text(ctx, "TIME WASTED", tx + 110, gy + 160, 22, RED, font=MONO, a=0.9)

    def hud(self, ctx, t, d, b):
        if t < b["n2"]:
            stamp(ctx, 540, STAMP_Y, t - 0.05, 0.02, 700, 170, ORANGE, [("BRUTE FORCE", 0, 110, ORANGE)])
        else:
            badge(ctx, 540, STAMP_Y, t - b["n2"], 640, 200, RED,
                  [("TIME:", -50, 60, (1, 1, 1)), ("O(N²)", 30, 130, RED)], rot=-0.03)
            if t >= b["barbaad"]:
                text(ctx, "SLOW!", 860, STAMP_Y - 110, 64, YELLOW, font=CAPTION_FONT, bold=False,
                     a=0.6 + 0.4 * math.sin(t * 14), stroke=(0, 0, 0), stroke_w=8)


class HashMap(Board):
    """Camera pushes into the whiteboard; coder points at a glowing hash map. 2 -> 9-2=7 not in map,
    store it; 7 -> 9-7=2 found -> [0, 1]; ONE PASS."""
    accent = CYAN
    tab = "hash_map.py"
    CW, GAP = 104, 16

    def beats(self, d):
        c = self.cue
        return {"hash": c("HASH", d * 0.08), "har": c("HAR NUMBER", d * 0.18), "ask": c("TARGET", d * 0.3),
                "seven": c("7 AATE", d * 0.62), "two": c("2 MIL", d * 0.7), "pass": c("PASS", d * 0.85)}

    def poses(self, d, b):
        return [(0.0, "explain"), (b["hash"], "point"), (b["pass"], "cheer")]

    def mood_at(self, t, b):
        return "happy" if t >= b["two"] else "ok"

    def events(self, d):
        b = self.beats(d)
        return [(b["hash"], "zap"), (b["har"], "pick"), (b["ask"] + 0.9, "beep"), (b["ask"] + 1.5, "pop"),
                (b["seven"], "pick"), (b["two"], "kaching"), (b["pass"], "boom")]

    def camera(self, ctx, t, d, b):
        z = 1 + 0.12 * ease_in_out(t / 1.4)
        fx, fy = 780, 800
        ctx.translate(fx, fy)
        ctx.scale(z, z)
        ctx.translate(-fx, -fy)

    def board(self, ctx, t, d, b):
        x, y, w, h = PANEL
        chip(ctx, f"target = {TARGET}", x + w - 150, y + 100, 30, YELLOW, t - 0.1, font=MONO, bold=True)
        x0 = x + (w - (4 * self.CW + 3 * self.GAP)) / 2
        ay = y + 225
        cur = None
        if t >= b["har"]:
            cur = 0
        if t >= b["seven"]:
            cur = 1
        found = t >= b["two"]
        sweep = clamp((t - b["pass"]) / 0.7)
        states = []
        for n in range(4):
            c = GREEN if found and n < 2 else (CYAN if n == cur else None)
            if sweep > 0 and n >= 2 and sweep * 4 > n:
                c = None
            states.append((c, 1.0))
        cells(ctx, x0, ay, self.CW, 92, self.GAP, states, t)
        if cur is not None:                                     # sliding pointer
            px = cell_x(x0, self.CW, self.GAP, 0)
            if t >= b["seven"]:
                px = lerp(px, cell_x(x0, self.CW, self.GAP, 1), ease_out_cubic((t - b["seven"]) / 0.3))
            bob = 6 * math.sin(t * 8)
            arrow_head(ctx, px, ay - 76 + bob, math.pi / 2, 22, CYAN)
            text(ctx, "x", px, ay - 112 + bob, 28, CYAN, font=MONO)
        if sweep > 0:                                           # one-pass scan line
            sx = lerp(x0 - 10, x0 + 4 * self.CW + 3 * self.GAP + 10, sweep)
            line(ctx, [(x0 - 10, ay + 80), (sx, ay + 80)], YELLOW, 6)
            glow(ctx, sx, ay + 80, 40, YELLOW, 0.8)
        # complement equation
        ey = y + 350
        if t >= b["ask"] and cur is not None:
            xv = NUMS[cur]
            u = t - (b["seven"] if cur == 1 else b["ask"])
            a = clamp(u / 0.2)
            s = f"{TARGET} - {xv} = {TARGET - xv}"
            text(ctx, "target - x", x + 150, ey, 24, hexc("#8B949E"), font=MONO, a=a)
            text(ctx, s, x + 400, ey, 44, YELLOW, font=MONO, a=a)
            text(ctx, "in map?", x + 400, ey + 42, 24, CYAN, font=MONO, a=clamp((u - 0.3) / 0.2))
        # glowing hash map table
        tx, ty, tw, rh = x + 110, y + 470, 380, 52
        if t >= b["hash"]:
            u = t - b["hash"]
            pop = max(ease_out_back(u / 0.35), 1e-3)
            pulse = 0.5 + 0.5 * math.sin(t * 5)
            ctx.save()
            ctx.translate(tx + tw / 2, ty + 70)
            ctx.scale(pop, pop)
            ctx.translate(-(tx + tw / 2), -(ty + 70))
            glow(ctx, tx + tw / 2, ty + 70, 300, CYAN, 0.25 + 0.15 * pulse)
            rrect(ctx, tx, ty, tw, rh * 2 + 14, 14)
            rgba(ctx, hexc("#06202A"), 0.95)
            ctx.fill_preserve()
            rgba(ctx, CYAN, 0.25)
            ctx.set_line_width(16)
            ctx.stroke_preserve()
            rgba(ctx, CYAN)
            ctx.set_line_width(4)
            ctx.stroke()
            text(ctx, "HASH MAP", tx + tw / 2, ty - 26, 30, CYAN, font=CAPTION_FONT, bold=False)
            text(ctx, "NUM", tx + tw * 0.28, ty + rh / 2, 26, hexc("#8B949E"), font=MONO)
            text(ctx, "INDEX", tx + tw * 0.72, ty + rh / 2, 26, hexc("#8B949E"), font=MONO)
            line(ctx, [(tx + 12, ty + rh), (tx + tw - 12, ty + rh)], CYAN, 2, 0.5)
            line(ctx, [(tx + tw / 2, ty + 10), (tx + tw / 2, ty + rh * 2 + 4)], CYAN, 2, 0.5)
            ins = t - (b["ask"] + 1.5)
            if ins > 0:
                rp = max(ease_out_back(ins / 0.3), 1e-3)
                ry = ty + rh * 1.5 + 4
                if found:
                    rrect(ctx, tx + 8, ry - rh / 2 + 4, tw - 16, rh - 8, 10)
                    rgba(ctx, GREEN, 0.25 + 0.15 * math.sin(t * 10))
                    ctx.fill()
                ctx.save()
                ctx.translate(tx + tw / 2, ry)
                ctx.scale(rp, rp)
                col = GREEN if found else (1, 1, 1)
                text(ctx, "2", -tw * 0.22, 0, 38, col, font=MONO)
                text(ctx, "0", tw * 0.22, 0, 38, col, font=MONO)
                ctx.restore()
            ctx.restore()
            # lookup verdicts beside the table
            nu = t - (b["ask"] + 0.9)
            if 0 < nu and t < b["seven"]:
                cross_mark(ctx, tx + tw + 50, ty + 40, 20, RED, clamp(nu / 0.15))
                text(ctx, "NO", tx + tw + 50, ty + 92, 26, RED, font=CAPTION_FONT, bold=False)
                text(ctx, "→ store", tx + tw + 50, ty + 128, 20, hexc("#8B949E"), font=MONO)
            if found:
                tick_mark(ctx, tx + tw + 50, ty + 90, 26, GREEN, clamp((t - b["two"]) / 0.25))
        if found:
            chip(ctx, "FOUND  [0, 1]", x + w / 2, y + 614, 28, GREEN, t - b["two"] - 0.2)

    def extras(self, ctx, t, d, b):
        if t >= b["hash"] and t < b["pass"]:                    # sparkle trail from finger to table
            for k in range(5):
                v = (t * 1.5 + k / 5) % 1
                px, py = lerp(400, 560, v), lerp(700, 950, v)
                circle(ctx, px, py, 5 * (1 - v) + 2, CYAN, 0.8 * (1 - v))

    def hud(self, ctx, t, d, b):
        if t < b["pass"]:
            u = t - b["hash"] + 0.25
            badge(ctx, 540, STAMP_Y, u, 680, 170, CYAN, [("HASH MAP", 0, 120, CYAN)], rot=-0.02)
            if u < 0:
                stamp(ctx, 540, STAMP_Y, t, 0.02, 680, 150, YELLOW, [("ASLI TRICK", 0, 100, YELLOW)])
        else:
            u = t - b["pass"]
            badge(ctx, 540, STAMP_Y, u, 680, 170, YELLOW, [("ONE PASS", -10, 120, YELLOW)], rot=0.02)
            if u > 0.2:
                ctx.save()
                ctx.translate(820, STAMP_Y - 100)
                tick_mark(ctx, 0, 0, 34, GREEN, clamp((u - 0.2) / 0.3))
                ctx.restore()


class Outro(Board):
    """TIME: O(N) badge over an N vs N² growth chart, then a pulsing NEXT LEETCODE QUESTION? CTA
    with bouncing arrow and a FOLLOW button that gets clicked."""
    accent = CYAN
    tab = "complexity.md"

    def beats(self, d):
        c = self.cue
        return {"on": c("O(N)", d * 0.25), "agla": c("AGLA", d * 0.4), "comment": c("COMMENT", d * 0.75),
                "follow": c("FOLLOW", d * 0.88)}

    def click(self, d, b):
        return min(d - 0.3, b["follow"] + 0.35)

    def poses(self, d, b):
        return [(0.0, "cheer"), (b["agla"], "explain"), (b["comment"], "down")]

    def mood_at(self, t, b):
        return "happy"

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["on"], "kaching"), (b["agla"], "whoosh"), (b["comment"], "dingdong"),
                (self.click(d, b), "pick"), (self.click(d, b) + 0.05, "pop")]

    def board(self, ctx, t, d, b):
        x, y, w, h = PANEL
        if t < b["agla"]:                                       # N vs N² growth chart
            ox, oy, cw, chh = x + 90, y + 560, 440, 430
            line(ctx, [(ox, oy - chh), (ox, oy), (ox + cw, oy)], hexc("#6E7681"), 4)
            text(ctx, "time", ox - 40, oy - chh + 20, 22, hexc("#8B949E"), font=MONO)
            text(ctx, "N", ox + cw + 22, oy, 26, hexc("#8B949E"), font=MONO)
            k = ease_in_out(t / 1.2)
            for fn, c, lab in ((lambda v: v * v, RED, "O(N²)"), (lambda v: v * 0.45, CYAN, "O(N)")):
                pts = [(ox + cw * v * k, oy - chh * fn(v * k)) for v in (i / 40 for i in range(41))]
                line(ctx, pts, c, 8 if c == CYAN else 5, 1.0 if c == CYAN else 0.6)
                if k > 0.95:
                    lx, ly = pts[-1]
                    text(ctx, lab, lx - 20, ly - 34, 34, c, font=CAPTION_FONT, bold=False)
            if k > 0.95:
                glow(ctx, ox + cw, oy - chh * 0.45, 60, CYAN, 0.6 + 0.3 * math.sin(t * 8))
            chip(ctx, "LINEAR", ox + 140, oy - chh + 30, 30, GREEN, t - b["on"])
            return
        u = t - b["agla"]
        pulse = (1 + 0.06 * math.sin(t * 7)) * max(ease_out_back(u / 0.35), 1e-3)
        ctx.save()
        ctx.translate(x + w / 2, y + 260)
        ctx.scale(pulse, pulse)
        glow(ctx, 0, 0, 380, YELLOW, 0.3)
        text(ctx, "NEXT", 0, -120, 90, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=10)
        text(ctx, "LEETCODE", 0, -10, 108, YELLOW, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=12)
        text(ctx, "QUESTION?", 0, 105, 100, YELLOW, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=12)
        ctx.restore()
        if u > 0.25:
            down_arrow(ctx, x + w / 2, y + 470 + 26 * abs(math.sin(t * 7)), 0.8, YELLOW)
        if t >= b["comment"]:                                   # comment bubble
            cu = t - b["comment"]
            bp = max(ease_out_back(cu / 0.3), 1e-3)
            ctx.save()
            ctx.translate(x + 110, y + 500)
            ctx.scale(bp, bp)
            rrect(ctx, -60, -42, 120, 76, 20)
            ctx.move_to(-20, 30)
            ctx.line_to(-38, 58)
            ctx.line_to(4, 30)
            rgba(ctx, CYAN)
            ctx.fill()
            for k in range(3):
                circle(ctx, -30 + k * 30, -4, 8, hexc("#06202A"))
            ctx.restore()

    def hud(self, ctx, t, d, b):
        badge(ctx, 540, STAMP_Y, t - 0.05, 760, 200, CYAN,
              [("TIME:", -50, 60, (1, 1, 1)), ("O(N)", 30, 140, CYAN)], rot=-0.02)
        # FOLLOW button between the captions and the bottom UI zone (all of it above y = 1520)
        if t >= b["comment"]:
            u = t - b["comment"]
            clicked = t >= self.click(d, b)
            pop = max(ease_out_back(u / 0.3), 1e-3) * (0.9 if abs(t - self.click(d, b)) < 0.1 else 1.0)
            bx, by = 540, 1385
            ctx.save()
            ctx.translate(bx, by)
            ctx.scale(pop, pop)
            c = hexc("#2B2F3A") if clicked else RED
            glow(ctx, 0, 0, 260, c, 0.35)
            rrect(ctx, -200, -52, 400, 104, 52)
            rgba(ctx, c)
            ctx.fill()
            if clicked:
                text(ctx, "FOLLOWING", -24, 0, 50, (1, 1, 1), font=UI_FONT)
                tick_mark(ctx, 150, -2, 18, GREEN)
            else:
                text(ctx, "+ FOLLOW", 0, 0, 52, (1, 1, 1), font=UI_FONT)
            ctx.restore()
            cu = clamp((t - (self.click(d, b) - 0.6)) / 0.5)
            if cu > 0:                                          # cursor glides in and clicks
                cx, cy = lerp(900, bx + 120, ease_in_out(cu)), lerp(1440, by + 10, ease_in_out(cu))
                ctx.save()
                ctx.translate(cx, cy)
                ctx.move_to(0, 0)
                for px, py in ((0, 62), (16, 48), (28, 74), (40, 68), (28, 43), (48, 42)):
                    ctx.line_to(px, py)
                ctx.close_path()
                rgba(ctx, (1, 1, 1))
                ctx.fill_preserve()
                rgba(ctx, (0, 0, 0))
                ctx.set_line_width(3)
                ctx.stroke()
                ctx.restore()


SCENE_CLASSES = {"hook": Hook, "brute": Brute, "hashmap": HashMap, "outro": Outro}
