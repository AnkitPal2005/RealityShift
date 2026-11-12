"""Reality Shift Short — the Siliguri Corridor ("Chicken's Neck"), India's ~22 km lifeline to the North-East (~47s).

Usage:
  python make.py chickens_neck

New "intel file" layout (not Chabahar's compose()): HUD header with file counter, drawn map of the eastern
Himalaya, Hinglish typewriter captions in the 1150-1250 band, shutter wipes between scenes instead of flash cuts,
slow drifting camera, bottom 400px clean. Ends on a HAAN / NAA comment poll card, no subscribe badge / bell / cursor.
Facts: corridor ~20-22 km at its narrowest (Nepal to Bangladesh); links 8 North-East states (7 + Sikkim);
Doklam 2017 stand-off lasted 73 days (16 Jun - 28 Aug) and the road work at the face-off point stopped;
Indian Army 33 Corps ("Trishakti Corps", HQ Sukna near Siliguri) guards it.
"""

import importlib
import json
import math

import cairo
import numpy as np

from core import engine
from core.engine import *  # noqa: F401,F403
from shorts.chabahar import Cued, partial
from shorts.maldives import CN_RED, CN_YELLOW
from shorts.rupee import VOICE_TONES
from shorts.reality_shift import GOLD, INDIA_GREEN, SAFFRON, flag, stamp

TOPIC = "CHICKEN'S NECK"
OUTPUTS = {"edge": "chickens_neck_short.mp4"}
# its frame pieces, as named in lego.py (drawn locally here; the gate reads this to rotate the next Shorts)
LEGO = {"header": "intel", "caption": "typewriter", "transition": "shutter", "palette": "intel", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.3
TAIL_PAD = 0.35            # the breath between scenes
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 96
MUSIC_STYLE = "march"     # snare cadence + low brass for an Army story; rotate per Short
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"

RED = hexc("#FF3B3B")
TEAL = hexc("#46E0B0")
MONO = "Consolas"

# where every number / claim comes from (policy.py requires these; verify before upload)
SOURCES = [
    "Siliguri Corridor: ~20-22 km wide at its narrowest between Nepal and Bangladesh, links the 8 North-East "
    "states (Encyclopaedia/Wikipedia 'Siliguri Corridor'; widely reported explainers, e.g. The Hindu, BBC)",
    "Doklam stand-off 16 June - 28 August 2017 (73 days), ended by mutual disengagement; road work at the "
    "face-off site stopped (MEA press statement 'Recent developments in Doklam', 28 Aug 2017)",
    "Indian Army 33 Corps 'Trishakti Corps', HQ Sukna near Siliguri (Indian Army / PIB releases)",
    "North-East population 'crores': ~4.5 crore in Census 2011 (8 states incl. Sikkim)",
]

# each line: (tone, [(spoken Hindi, Hinglish caption), ...], pause after) - pauses as approved on the voice sample:
# ~0.15 after a comma, ~0.35 after a sentence, ~0.5 after a "..." setup, ~0.6 before the CTA
SPEC = [
    {"key": "neck", "accent": RED, "text": "22 KM LIFELINE",
     "visual": "Map dives from India into a pulsing strip at Siliguri, 22 KM caliper, strip cut, North-East drifts away",
     "vo": [("hook", [("भारत की", "BHARAT KI"), ("सबसे पतली नस...", "SABSE PATLI NAS...")], 0.5),
            ("punch", [("सिर्फ बाईस", "SIRF 22"), ("किलोमीटर चौड़ी है।", "KILOMETER CHAUDI HAI!")], 0.35),
            ("build", [("अगर ये रास्ता", "AGAR YEH RAASTA"), ("बंद हुआ...", "BAND HUA...")], 0.5),
            ("punch", [("तो आठ राज्य,", "TOH 8 RAAJYA,")], 0.15),
            ("punch", [("करोड़ों लोग,", "CRORON LOG,")], 0.15),
            ("punch", [("बाकी भारत से", "BAAKI BHARAT SE"), ("कट जाएंगे।", "KAT JAAYENGE!")], 0)]},
    {"key": "neighbours", "accent": GOLD, "text": "SILIGURI CORRIDOR",
     "visual": "Corridor named, chicken icon, Nepal / Bangladesh / Bhutan light up in turn, then China glows red behind",
     "vo": [("tell", [("नाम है", "NAAM HAI"), ("सिलीगुड़ी कॉरिडोर।", "SILIGURI CORRIDOR.")], 0.4),
            ("sly", [("दुनिया इसे कहती है", "DUNIYA ISE KEHTI HAI")], 0.12),
            ("punch", [("चिकन्स नेक।", "CHICKEN'S NECK!")], 0.4),
            ("low", [("एक तरफ नेपाल,", "EK TARAF NEPAL,")], 0.15),
            ("low", [("दूसरी तरफ बांग्लादेश,", "DOOSRI TARAF BANGLADESH,")], 0.15),
            ("low", [("ऊपर भूटान...", "UPAR BHUTAN...")], 0.45),
            ("tell", [("और उसके ठीक पीछे", "AUR USKE THEEK PEECHHE"), ("है चीन।", "HAI CHINA!")], 0)]},
    {"key": "doklam", "accent": CN_RED, "text": "DOKLAM 2017",
     "visual": "Zoom to Doklam: China's road creeps south toward the neck, Indian soldiers block it, DAY 1-73, road stops",
     "vo": [("build", [("दो हज़ार सत्रह में,", "2017 MEIN,")], 0.15),
            ("build", [("चीन ने डोकलाम में", "CHINA NE DOKLAM MEIN"), ("सड़क बनानी शुरू की,", "SADAK BANANI SHURU KI,")],
             0.15),
            ("low", [("सीधा इसी", "SEEDHA ISI"), ("गर्दन की तरफ।", "GARDAN KI TARAF!")], 0.35),
            ("punch", [("भारतीय सेना", "BHARATIYA SENA"), ("सामने खड़ी हो गई।", "SAAMNE KHADI HO GAYI!")], 0.35),
            ("tell", [("तिहत्तर दिन तक", "73 DIN TAK"), ("आमने सामने...", "AAMNE SAAMNE...")], 0.5),
            ("punch", [("और वो सड़क", "AUR WOH SADAK"), ("वहीं रुक गई।", "WAHIN RUK GAYI!")], 0)]},
    {"key": "answer", "accent": SAFFRON, "text": "TRISHAKTI CORPS",
     "visual": "Shield dome rises over Siliguri, 33 CORPS badge, then a HAAN / NAA poll card asks for a comment",
     "vo": [("punch", [("आज इस गर्दन की", "AAJ IS GARDAN KI"), ("सुरक्षा करती है,", "SURAKSHA KARTI HAI,"),
                       ("भारतीय सेना की", "INDIAN ARMY KI"), ("त्रिशक्ति कोर।", "TRISHAKTI CORPS!")], 0.45),
            ("ask", [("क्या भारत को", "KYA BHARAT KO"), ("यहां एक दूसरा रास्ता", "YAHAN EK DOOSRA RAASTA"),
                     ("बनाना चाहिए?", "BANANA CHAHIYE?")], 0.6),
            ("cta", [("हाँ या ना,", "HAAN YA NAA,"), ("कमेंट में लिखो।", "COMMENT MEIN LIKHO!")], 0.3),
            ("cta", [("भारत की ऐसी और कहानियों के लिए,", "BHARAT KI AISI AUR KAHANIYON KE LIYE,"), ("सब्सक्राइब करो!", "SUBSCRIBE KARO!")], 0)]},
]

# the approved Reality Shift narrator: Rupee VOICE_TONES as-is (one pitch, no extra speed-up), pauses from SPEC
DELIVERY = {s["key"]: [(VOICE_TONES[tone], " ".join(hi for hi, _ in chunks), pause) for tone, chunks, pause in s["vo"]]
            for s in SPEC}
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {"22": GOLD, "PATLI": RED, "BAND": RED, "8": GOLD, "KAT": RED, "SILIGURI": GOLD, "CORRIDOR": GOLD,
       "CHICKEN'S": GOLD, "NECK": GOLD, "NEPAL": TEAL, "BANGLADESH": TEAL, "BHUTAN": TEAL, "CHINA": RED,
       "2017": GOLD, "DOKLAM": RED, "GARDAN": RED, "SENA": SAFFRON, "73": GOLD, "RUK": TEAL,
       "TRISHAKTI": SAFFRON, "SURAKSHA": SAFFRON, "DOOSRA": GOLD, "HAAN": INDIA_GREEN, "NAA": RED, "COMMENT": GOLD, "SUBSCRIBE": RED}

CAP_TOP, CAP_BOTTOM = 1150, 1250
UI_CLEAR = H - 400
MAP_CY = 620


# ============================================================ map of the eastern Himalaya

NEPAL = [(80.06, 28.84), (81.1, 30.2), (82.2, 30.1), (83.5, 29.3), (84.1, 28.6), (85.2, 28.6), (86.0, 27.95),
         (87.2, 27.85), (88.1, 27.9), (88.05, 27.3), (88.2, 26.9), (88.18, 26.55), (87.3, 26.4), (86.0, 26.6),
         (85.0, 26.9), (84.1, 27.5), (83.3, 27.35), (81.9, 27.9), (81.0, 28.4), (80.1, 28.6)]
SIKKIM = [(88.05, 27.3), (88.1, 27.9), (88.6, 28.1), (88.85, 27.85), (88.8, 27.4), (88.75, 27.15), (88.4, 27.1),
          (88.2, 26.9)]
BHUTAN = [(88.92, 27.3), (89.0, 27.75), (89.6, 28.2), (90.4, 28.1), (91.3, 28.05), (92.1, 27.8), (92.1, 26.85),
          (91.2, 26.8), (90.3, 26.85), (89.4, 26.75), (88.85, 26.95)]
CHINA = [(76.0, 37.0), (101.0, 37.0), (101.0, 28.5), (97.4, 28.2), (96.0, 29.4), (94.0, 29.3), (92.1, 27.8),
         (91.3, 28.05), (90.4, 28.1), (89.6, 28.2), (89.0, 27.75), (88.92, 27.3), (88.8, 27.4), (88.85, 27.85),
         (88.6, 28.1), (88.1, 27.9), (87.2, 27.85), (86.0, 27.95), (85.2, 28.6), (84.1, 28.6), (83.5, 29.3),
         (82.2, 30.1), (81.1, 30.2), (80.06, 28.84), (79.0, 30.5), (78.5, 32.5), (76.0, 34.0)]
BANGLADESH = [(88.38, 26.45), (88.95, 26.25), (89.85, 26.0), (89.85, 25.3), (90.6, 25.2), (92.0, 25.1), (92.4, 24.3),
              (92.2, 23.7), (91.8, 23.0), (92.3, 21.2), (92.0, 21.3), (91.4, 22.6), (90.6, 22.3), (89.8, 21.8),
              (89.0, 21.7), (89.0, 22.8), (88.6, 23.6), (88.7, 24.3), (88.0, 24.6), (88.45, 25.2), (88.1, 25.7),
              (88.5, 26.2)]
MYANMAR = [(92.3, 21.2), (92.6, 22.0), (93.3, 21.95), (93.4, 23.0), (94.2, 23.8), (94.6, 24.6), (95.0, 25.5),
           (95.2, 26.6), (97.1, 27.0), (97.4, 28.2), (101.0, 28.5), (101.0, 14.0), (94.0, 14.0)]
SEA = [(78.0, 14.0), (80.0, 15.8), (82.3, 16.6), (84.0, 18.3), (85.8, 19.8), (87.0, 21.0), (88.2, 21.6), (89.0, 21.7),
       (89.8, 21.8), (90.6, 22.3), (91.4, 22.6), (92.0, 21.3), (92.3, 21.2), (94.0, 14.0)]
NORTH_EAST = [(89.85, 25.3), (89.85, 26.78), (90.3, 26.85), (91.2, 26.8), (92.1, 26.85), (92.1, 27.8), (94.0, 29.3),
              (96.0, 29.4), (97.4, 28.2), (97.1, 27.0), (95.2, 26.6), (95.0, 25.5), (94.6, 24.6), (94.2, 23.8),
              (93.4, 23.0), (93.3, 21.95), (92.6, 22.0), (92.2, 23.7), (92.4, 24.3), (92.0, 25.1), (90.6, 25.2)]
CORRIDOR = [(88.18, 26.55), (88.2, 26.9), (88.4, 27.1), (88.75, 27.15), (88.85, 26.95), (89.4, 26.75),
            (89.85, 26.78), (89.85, 26.0), (88.95, 26.25), (88.38, 26.45)]
FOREIGN = {"nepal": NEPAL, "bhutan": BHUTAN, "china": CHINA, "bangladesh": BANGLADESH, "myanmar": MYANMAR}
LABELS = {"nepal": ("NEPAL", 86.2, 27.45), "bhutan": ("BHUTAN", 90.6, 27.4), "china": ("CHINA", 89.6, 29.2),
          "bangladesh": ("BANGLADESH", 90.1, 24.2), "myanmar": ("MYANMAR", 96.2, 23.5),
          "india": ("INDIA", 85.2, 24.6), "ne": ("NORTH-EAST", 93.6, 26.2)}
SILIGURI = (88.43, 26.71)
NEPAL_TIP, BD_TIP = (88.18, 26.55), (88.38, 26.45)
DOKLAM = (88.93, 27.29)
ROAD = [(88.98, 27.64), (88.95, 27.46), (88.93, 27.3), (88.97, 27.2)]

INDIA_LAND = hexc("#14251E")
FOREIGN_LAND = hexc("#0C1117")
WATER = hexc("#030B14")
EDGE = hexc("#7FD6B8")


def proj(v, lon, lat):
    """Equirectangular projection for view v = (centre lon, centre lat, px per degree)."""
    lon0, lat0, s = v
    return W / 2 + (lon - lon0) * s * 0.9, MAP_CY - (lat - lat0) * s


def view_at(keys, t):
    """Eased camera between (time, view) keyframes; keyframe times are forced to increase, zoom is geometric."""
    fixed, last = [], -1e9
    for k, view in keys:
        last = max(k, last + 0.05)
        fixed.append((last, view))
    if t <= fixed[0][0]:
        return fixed[0][1]
    for (t0, a), (t1, b) in zip(fixed, fixed[1:]):
        if t < t1:
            u = ease_in_out((t - t0) / (t1 - t0))
            return lerp(a[0], b[0], u), lerp(a[1], b[1], u), math.exp(lerp(math.log(a[2]), math.log(b[2]), u))
    return fixed[-1][1]


def poly(ctx, v, pts):
    ctx.move_to(*proj(v, *pts[0]))
    for p in pts[1:]:
        ctx.line_to(*proj(v, *p))
    ctx.close_path()


def draw_region(ctx, v, t, tint=None, labels=("nepal", "bhutan", "china", "bangladesh", "india")):
    """India land with its neighbours darker; tint = {country: (colour, 0..1)} lights a neighbour up."""
    tint = tint or {}
    rgba(ctx, INDIA_LAND)
    ctx.paint()
    poly(ctx, v, SEA)
    rgba(ctx, WATER)
    ctx.fill()
    for name, pts in FOREIGN.items():
        poly(ctx, v, pts)
        rgba(ctx, FOREIGN_LAND)
        ctx.fill()
        c, k = tint.get(name, (None, 0))
        if k > 0:
            poly(ctx, v, pts)
            rgba(ctx, c, 0.32 * k)
            ctx.fill()
    s = v[2]
    step = 0.5 if s > 400 else (1 if s > 150 else 2)
    lon0, lat0, _ = v
    for k in range(-30, 31):  # graticule
        x = proj(v, round(lon0 / step) * step + k * step, lat0)[0]
        if -5 < x < W + 5:
            line(ctx, [(x, 0), (x, H)], EDGE, 1, 0.07)
        y = proj(v, lon0, round(lat0 / step) * step + k * step)[1]
        if -5 < y < H + 5:
            line(ctx, [(0, y), (W, y)], EDGE, 1, 0.07)
    for name, pts in FOREIGN.items():
        c, k = tint.get(name, (EDGE, 0))
        poly(ctx, v, pts)
        rgba(ctx, c, 0.2 + 0.25 * k)
        ctx.set_line_width(8)
        ctx.stroke_preserve()
        rgba(ctx, c, 0.55 + 0.45 * k)
        ctx.set_line_width(2.5)
        ctx.stroke()
    ctx.set_dash([8, 8])
    poly(ctx, v, SIKKIM)
    rgba(ctx, EDGE, 0.3)
    ctx.set_line_width(1.5)
    ctx.stroke()
    ctx.set_dash([])
    for name in labels:
        s_, lon, lat = LABELS[name]
        x, y = proj(v, lon, lat)
        c, k = tint.get(name, ((0.75, 0.85, 0.82), 0))
        if -100 < x < W + 100 and 40 < y < CAP_TOP - 40:
            text(ctx, s_, x, y, 34, c, font=MONO, a=0.55 + 0.45 * k)


def corridor_glow(ctx, v, t, c, k=1.0):
    poly(ctx, v, CORRIDOR)
    rgba(ctx, c, (0.22 + 0.12 * math.sin(t * 7)) * k)
    ctx.fill_preserve()
    rgba(ctx, c, 0.9 * k)
    ctx.set_line_width(4)
    ctx.stroke()


# ============================================================ HUD props

def tag(ctx, s, x, y, c, u, size=36, sub=None):
    """Mono label in a bracketed box that wipes open left-to-right, centred on (x, y)."""
    if u <= 0:
        return
    w = max(text_width(ctx, s, size, font=MONO), text_width(ctx, sub, size * 0.7, font=MONO) if sub else 0) + 48
    h = size * (2.3 if sub else 1.5)
    open_ = ease_out_cubic(u / 0.25)
    ctx.save()
    ctx.translate(x, y)
    ctx.rectangle(-w / 2, -h / 2 - 10, w * open_, h + 20)
    ctx.clip()
    ctx.rectangle(-w / 2, -h / 2, w, h)
    rgba(ctx, (0.01, 0.02, 0.03), 0.88)
    ctx.fill()
    for sx in (-1, 1):  # bracket corners
        for sy in (-1, 1):
            px, py = sx * w / 2, sy * h / 2
            line(ctx, [(px - sx * 22, py), (px, py), (px, py - sy * 22)], c, 4)
    text(ctx, s, 0, -size * 0.45 if sub else 0, size, (1, 1, 1), font=MONO)
    if sub:
        text(ctx, sub, 0, size * 0.62, size * 0.7, c, font=MONO)
    ctx.restore()


def caliper(ctx, p0, p1, u, c, label):
    """Measuring line between two screen points, ticks at both ends, label above the middle."""
    if u <= 0:
        return
    k = ease_out_cubic(u / 0.5)
    mx, my = lerp(p0[0], p1[0], 0.5), lerp(p0[1], p1[1], 0.5)
    a = lerp(mx, p0[0], k), lerp(my, p0[1], k)
    b = lerp(mx, p1[0], k), lerp(my, p1[1], k)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0]) + math.pi / 2
    nx, ny = 34 * math.cos(ang), 34 * math.sin(ang)
    line(ctx, [a, b], c, 16, 0.25)
    line(ctx, [a, b], c, 6)
    for px, py in (a, b):
        line(ctx, [(px - nx, py - ny), (px + nx, py + ny)], c, 6)
        circle(ctx, px, py, 9, (1, 1, 1))
    tag(ctx, label, mx, my - 120, c, u - 0.2, size=64)


def ripple(ctx, x, y, t, c, n=3):
    for k in range(n):
        r = ((t * 0.8 + k / n) % 1.0)
        ctx.arc(x, y, 20 + 140 * r, 0, math.tau)
        rgba(ctx, c, 0.7 * (1 - r))
        ctx.set_line_width(4)
        ctx.stroke()
    glow(ctx, x, y, 50, c, 0.9)
    circle(ctx, x, y, 10, (1, 1, 1))


def chicken(ctx, x, y, s, t):
    """Cartoon chicken head on a long thin neck (the neck lights red), neck base at (x, y)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    bob = 6 * math.sin(t * 5)
    neck = [(-16, 0), (-12, -150 + bob), (12, -150 + bob), (16, 0)]
    ctx.move_to(*neck[0])
    for p in neck[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    rgba(ctx, RED)
    ctx.fill()
    for k in range(3):  # comb
        circle(ctx, -22 + 20 * k, -232 + bob - 6 * (k == 1), 18, RED)
    circle(ctx, 0, -190 + bob, 52, (0.97, 0.95, 0.9))
    ctx.move_to(46, -200 + bob)  # beak
    ctx.line_to(92, -186 + bob)
    ctx.line_to(46, -172 + bob)
    ctx.close_path()
    rgba(ctx, hexc("#FFB020"))
    ctx.fill()
    _drop(ctx, 40, -160 + bob, 14, RED)
    circle(ctx, 18, -202 + bob, 8, (0.05, 0.05, 0.05))
    circle(ctx, 21, -205 + bob, 2.5, (1, 1, 1))
    ctx.restore()


def _drop(ctx, x, y, r, c):
    ctx.move_to(x, y - r)
    ctx.curve_to(x + r, y, x + r, y + r * 1.4, x, y + r * 1.6)
    ctx.curve_to(x - r, y + r * 1.4, x - r, y, x, y - r)
    rgba(ctx, c)
    ctx.fill()


def soldier(ctx, x, y, s, c=hexc("#5D6B3A")):
    """Standing soldier silhouette with a helmet and slung rifle, feet at (x, y)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    line(ctx, [(-10, 0), (-10, -60)], shade(c, 0.7), 16)
    line(ctx, [(10, 0), (10, -60)], shade(c, 0.7), 16)
    rrect(ctx, -26, -130, 52, 78, 12)
    rgba(ctx, c)
    ctx.fill()
    line(ctx, [(-34, -48), (30, -140)], (0.12, 0.12, 0.1), 7)
    circle(ctx, 0, -150, 20, hexc("#C68B59"))
    ctx.arc(0, -154, 25, math.pi, 2 * math.pi)
    rgba(ctx, shade(c, 0.85))
    ctx.fill()
    ctx.restore()


def dome(ctx, x, y, r, t, c, u):
    """Hex-lattice shield dome rising over (x, y)."""
    if u <= 0:
        return
    k = ease_out_back(u / 0.5)
    rr = r * k
    ctx.save()
    ctx.arc(x, y, rr, math.pi, 2 * math.pi)
    ctx.close_path()
    g = cairo.LinearGradient(0, y - rr, 0, y)
    g.add_color_stop_rgba(0, *c, 0.35)
    g.add_color_stop_rgba(1, *c, 0.08)
    ctx.set_source(g)
    ctx.fill_preserve()
    ctx.clip()
    hs = 34
    for i in range(-12, 13):
        for j in range(0, 12):
            hx = x + i * hs * 1.5
            hy = y - j * hs * 1.732 - (hs * 0.866 if i % 2 else 0)
            ctx.move_to(hx + hs, hy)
            for m in range(1, 7):
                ctx.line_to(hx + hs * math.cos(m * math.pi / 3), hy + hs * math.sin(m * math.pi / 3))
    rgba(ctx, c, 0.25 + 0.15 * math.sin(t * 4))
    ctx.set_line_width(2)
    ctx.stroke()
    ctx.restore()
    ctx.arc(x, y, rr, math.pi, 2 * math.pi)
    rgba(ctx, c, 0.95)
    ctx.set_line_width(6)
    ctx.stroke()
    line(ctx, [(x - rr, y), (x + rr, y)], c, 6)


# ============================================================ scenes

class Neck(Cued):
    """India -> dive into the Siliguri strip; 22 KM caliper; strip cut on 'बंद'; North-East drifts off on 'कट'."""

    def beats(self, d):
        c = self.cue
        return {"naz": c("PATLI", d * 0.08), "num": c("22", d * 0.22), "band": c("BAND", d * 0.45),
                "states": c("RAAJYA", d * 0.6), "log": c("CRORON", d * 0.7), "kat": c("KAT", d * 0.88)}

    def events(self, d):
        b = self.beats(d)
        ticks = [(b["num"] + 0.2 + k * 0.05, "tick" if k % 2 else "tock") for k in range(10)]
        return [(0.02, "boom"), (b["naz"], "beep"), (b["num"], "thud"), (b["band"], "alarm"),
                (b["band"] + 0.25, "thud"), (b["states"], "whoosh"), (b["log"], "pick"), (b["kat"], "boom")] + ticks

    def draw(self, ctx, t, d):
        b = self.beats(d)
        near = (88.3, 26.62, 950)
        v = view_at([(0.0, (87.0, 24.5, 70)), (b["num"] - 0.1, near), (b["states"] - 0.15, near),
                     (b["states"] + 0.6, (91.2, 26.0, 115))], t)
        drift = ease_in_out((t - b["kat"]) / 0.8) if t > b["kat"] else 0.0
        draw_region(ctx, v, t, labels=("nepal", "bhutan", "bangladesh", "china", "india", "ne") if t > b["states"]
                    else ("nepal", "bangladesh", "india"))
        lit = clamp((t - b["states"]) / 0.4)
        if lit:
            if drift:  # the North-East pulls away and leaves a void behind
                poly(ctx, v, NORTH_EAST)
                rgba(ctx, (0, 0, 0))
                ctx.fill()
            ctx.save()
            ctx.translate(60 * drift, -25 * drift)
            poly(ctx, v, NORTH_EAST)
            rgba(ctx, INDIA_LAND)
            ctx.fill_preserve()
            rgba(ctx, GOLD if not drift else RED, 0.25 * lit)
            ctx.fill_preserve()
            rgba(ctx, GOLD if not drift else RED, lit)
            ctx.set_line_width(4)
            ctx.stroke()
            ctx.restore()
        corridor_glow(ctx, v, t, RED, clamp(t / 0.6))
        sx, sy = proj(v, *SILIGURI)
        ripple(ctx, sx, sy, t, RED)
        p0, p1 = proj(v, *NEPAL_TIP), proj(v, *BD_TIP)
        u = t - b["num"]
        if u > 0 and t < b["states"]:
            km = round(22 * ease_out_cubic(u / 0.7))
            caliper(ctx, p0, p1, u, GOLD, f"{km} KM")
        u = t - b["band"]
        if u > 0 and t < b["states"]:  # the strip is cut
            k = ease_out_cubic(u / 0.25)
            line(ctx, [p0, (lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k))], RED, 26)
            stamp(ctx, 540, 300, u, -0.05, 560, 150, RED, [("BLOCKED", 0, 110, RED)])
        u = t - b["states"]
        if u > 0:
            tag(ctx, "8 STATES", 760, 300, GOLD, u, size=58, sub="SIKKIM + 7 SISTERS")
        u = t - b["log"]
        if u > 0 and t < b["kat"]:
            tag(ctx, "CRORES OF PEOPLE", 760, 470, GOLD, u, size=44)
        u = t - b["kat"]
        if u > 0:
            stamp(ctx, 540, 860, u, 0.05, 620, 160, RED, [("CUT OFF", 0, 120, RED)])


class Neighbours(Cued):
    """Corridor named with a chicken icon; Nepal, Bangladesh, Bhutan light up in turn; China glows red behind."""

    def beats(self, d):
        c = self.cue
        return {"name": c("SILIGURI", d * 0.06), "neck": c("CHICKEN'S", d * 0.3), "nepal": c("NEPAL", d * 0.48),
                "bd": c("BANGLADESH", d * 0.58), "bhutan": c("BHUTAN", d * 0.72), "china": c("CHINA", d * 0.9)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["name"], "dingdong"), (b["neck"], "pop"), (b["neck"] + 0.15, "pop"),
                (b["nepal"], "beep"), (b["bd"], "beep"), (b["bhutan"], "beep"), (b["china"], "boom"),
                (b["china"] + 0.05, "alarm")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        v = view_at([(0.0, (88.55, 26.75, 360)), (b["nepal"] - 0.2, (88.55, 26.75, 300)),
                     (b["china"] - 0.1, (88.9, 27.3, 210))], t)
        on = lambda key: clamp((t - b[key]) / 0.3)
        tint = {"nepal": (TEAL, on("nepal")), "bangladesh": (TEAL, on("bd")), "bhutan": (TEAL, on("bhutan")),
                "china": (CN_RED, on("china") * (0.8 + 0.2 * math.sin(t * 8)))}
        draw_region(ctx, v, t, tint)
        corridor_glow(ctx, v, t, GOLD)
        sx, sy = proj(v, *SILIGURI)
        ripple(ctx, sx, sy, t, GOLD)
        u = t - b["name"]
        if u > 0 and t < b["nepal"]:
            tag(ctx, "SILIGURI CORRIDOR", 540, 260, GOLD, u, size=56, sub="WEST BENGAL, INDIA")
        u = t - b["neck"]
        if u > 0 and t < b["nepal"]:
            pop = ease_out_back(u / 0.35)
            ctx.save()
            ctx.translate(820, 980)
            ctx.scale(pop, pop)
            chicken(ctx, 0, 0, 0.9, t)
            ctx.restore()
            stamp(ctx, 360, 900, u - 0.1, -0.05, 560, 130, GOLD, [("CHICKEN'S NECK", 0, 84, GOLD)])
        for key, name, lonlat in (("nepal", "NEPAL", (87.75, 26.95)), ("bd", "BANGLADESH", (89.0, 25.85)),
                                  ("bhutan", "BHUTAN", (90.0, 27.25))):
            u = t - b[key]
            if u > 0:
                x, y = proj(v, *lonlat)
                tag(ctx, name, clamp(x, 200, 880), clamp(y, 200, 1060), TEAL, u, size=46)
        u = t - b["china"]
        if u > 0:  # Chumbi valley arrow pointing down at the neck
            cx, cy = proj(v, 88.88, 27.75)
            k = ease_out_cubic(u / 0.4)
            ex, ey = lerp(cx, sx, 0.75 * k), lerp(cy, sy, 0.75 * k)
            line(ctx, [(cx, cy), (ex, ey)], CN_RED, 14)
            ang = math.atan2(ey - cy, ex - cx)
            ctx.move_to(ex + 34 * math.cos(ang), ey + 34 * math.sin(ang))
            for da in (2.4, -2.4):
                ctx.line_to(ex + 30 * math.cos(ang + da), ey + 30 * math.sin(ang + da))
            ctx.close_path()
            rgba(ctx, CN_RED)
            ctx.fill()
            stamp(ctx, 540, 200, u, 0.04, 420, 140, CN_RED, [("CHINA", 0, 110, CN_YELLOW)])


class Doklam(Cued):
    """Doklam 2017: China's road creeps south toward the neck, soldiers block it, DAY 1 -> 73, road stops."""

    def beats(self, d):
        c = self.cue
        return {"yr": c("2017", d * 0.02), "dok": c("DOKLAM", d * 0.1), "road": c("SADAK BANANI", d * 0.2),
                "gardan": c("GARDAN", d * 0.35), "sena": c("SENA", d * 0.5), "days": c("73", d * 0.68),
                "stop": c("RUK", d * 0.88)}

    def events(self, d):
        b = self.beats(d)
        ticks = [(b["days"] + k * 0.07, "tick" if k % 2 else "tock") for k in range(12)]
        return [(0.02, "boom"), (b["dok"], "beep"), (b["road"], "engine", 1.4), (b["gardan"], "alarm"),
                (b["sena"], "thud"), (b["sena"] + 0.18, "thud"), (b["stop"], "boom"), (b["stop"] + 0.05, "thud")] \
            + ticks

    def draw(self, ctx, t, d):
        b = self.beats(d)
        v = view_at([(0.0, (88.75, 27.0, 380)), (b["dok"], (88.9, 27.2, 680)),
                     (b["gardan"] + 0.4, (88.8, 27.1, 600))], t)
        draw_region(ctx, v, t, {"china": (CN_RED, 0.6), "bhutan": (TEAL, 0.3)})
        corridor_glow(ctx, v, t, GOLD, 0.7)
        sx, sy = proj(v, *SILIGURI)
        ripple(ctx, sx, sy, t, GOLD)
        text(ctx, "SILIGURI", sx, sy + 70, 36, GOLD, font=MONO)
        dx, dy = proj(v, *DOKLAM)
        u = t - b["dok"]
        if u > 0:
            tag(ctx, "DOKLAM", min(dx + 250, 840), dy - 70, CN_RED, u, size=44, sub="CHINA-BHUTAN-INDIA")
        stopped = t > b["stop"]
        grow = clamp((t - b["road"]) / max(b["gardan"] - b["road"], 0.6))
        pts, head = partial([proj(v, *p) for p in ROAD], grow)
        if grow > 0:
            c = (0.55, 0.55, 0.58) if stopped else CN_YELLOW
            line(ctx, pts, (0, 0, 0), 22, 0.6)
            line(ctx, pts, c, 14)
            ctx.set_dash([16, 14], 0 if stopped else -t * 60)
            line(ctx, pts, (0.1, 0.1, 0.1), 3)
            ctx.set_dash([])
            if not stopped:
                glow(ctx, *head, 40, CN_YELLOW, 0.8)
        u = t - b["gardan"]
        if u > 0 and not stopped:  # where the road was heading
            k = ease_out_cubic(u / 0.5)
            ex, ey = lerp(head[0], sx, k), lerp(head[1], sy, k)
            ctx.set_dash([20, 16], -t * 120)
            line(ctx, [head, (ex, ey)], CN_RED, 8, 0.9)
            ctx.set_dash([])
            if t < b["sena"]:
                tag(ctx, "TARGET: THE NECK", 540, 230, CN_RED, u, size=50)
        u = t - b["sena"]
        if u > 0:
            mx, my = lerp(head[0], sx, 0.4), lerp(head[1], sy, 0.4)
            for k in range(5):
                us = u - 0.08 * k
                if us > 0:
                    soldier(ctx, mx - 160 + 80 * k, my + 60 * (1 - ease_out_back(us / 0.3)) + 30, 0.75)
            flag(ctx, mx - 330, my - 120, 120, 80, "in", t, pole=150)
            if t < b["days"]:
                tag(ctx, "FACE-OFF", 540, 230, SAFFRON, u, size=60)
        u = t - b["yr"]
        if u > 0 and t < b["sena"]:
            stamp(ctx, 250, 300, u, -0.05, 300, 120, CN_RED, [("2017", 0, 96, (1, 1, 1))])
        u = t - b["days"]
        if u > 0:
            day = 1 + round(72 * ease_in_out(u / 1.0))
            stamp(ctx, 540, 230, 1.0, -0.03, 520, 150, GOLD, [(f"DAY {day:02d}", 0, 110, GOLD)])
        u = t - b["stop"]
        if u > 0:
            red_x = ease_out_cubic(u / 0.2)
            hx, hy = head
            for sgn in (-1, 1):
                line(ctx, [(hx - 50 * red_x, hy - sgn * 50 * red_x), (hx + 50 * red_x, hy + sgn * 50 * red_x)], RED, 14)
            stamp(ctx, 540, 880, u, 0.04, 640, 150, TEAL, [("ROAD STOPPED", 0, 96, TEAL)])


class Answer(Cued):
    """Shield over the neck with the 33 CORPS badge, then the HAAN / NAA poll card asking for a comment."""

    def beats(self, d):
        c = self.cue
        return {"hif": c("SURAKSHA", d * 0.08), "corps": c("TRISHAKTI", d * 0.22), "q": c("DOOSRA", d * 0.4),
                "cmt": c("COMMENT", d * 0.68), "sub": c("SUBSCRIBE", d * 0.88)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["hif"], "zap"), (b["corps"], "boom"), (b["corps"] + 0.1, "kaching"),
                (b["q"], "whoosh"), (b["q"] + 0.3, "pop"), (b["cmt"], "dingdong"), (b["sub"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        v = (88.55 + 0.02 * math.sin(t * 0.4), 26.85, 330)
        draw_region(ctx, v, t, {"china": (CN_RED, 0.35)})
        corridor_glow(ctx, v, t, SAFFRON, 0.8)
        sx, sy = proj(v, *SILIGURI)
        dome(ctx, sx, sy + 30, 300, t, SAFFRON, t - b["hif"])
        ripple(ctx, sx, sy, t, SAFFRON)
        u = t - b["corps"]
        if u > 0 and t < b["q"]:
            stamp(ctx, 540, 260, u, -0.03, 700, 190, SAFFRON,
                  [("33 CORPS", -30, 100, SAFFRON), ("TRISHAKTI  |  HQ SUKNA", 52, 40, (1, 1, 1))])
            for k in range(3):
                soldier(ctx, sx - 90 + 90 * k, sy + 250, 0.8)
        u = t - b["q"]
        if u > 0:  # the map steps back behind the poll card
            ctx.rectangle(0, 0, W, H)
            rgba(ctx, (0.01, 0.02, 0.03), 0.6 * clamp(u / 0.35))
            ctx.fill()
            self.poll(ctx, t, u, t - b["cmt"])
        u = t - b["sub"]
        if u > 0:
            stamp(ctx, 540, 1000, u, -0.04, 760, 120, RED, [("SUBSCRIBE • REALITY SHIFT", 0, 58, (1, 1, 1))])

    @staticmethod
    def poll(ctx, t, u, uc):
        pop = ease_out_back(u / 0.35)
        ctx.save()
        ctx.translate(540, 560)
        ctx.scale(pop, pop)
        rrect(ctx, -440, -330, 880, 640, 26)
        rgba(ctx, (0.02, 0.03, 0.05), 0.95)
        ctx.fill_preserve()
        rgba(ctx, GOLD)
        ctx.set_line_width(5)
        ctx.stroke()
        text(ctx, "POLL", -380, -270, 34, GOLD, font=MONO, anchor="l")
        text(ctx, "DOOSRA RAASTA", 0, -190, 84, (1, 1, 1), font=CAPTION_FONT, bold=False)
        text(ctx, "BANNA CHAHIYE?", 0, -100, 84, GOLD, font=CAPTION_FONT, bold=False)
        for k, (opt, c) in enumerate((("HAAN", INDIA_GREEN), ("NAA", RED))):
            y = 20 + k * 130
            hl = 0.5 + 0.5 * math.sin(t * 5 + k * math.pi)
            rrect(ctx, -360, y - 50, 720, 100, 50)
            rgba(ctx, c, 0.18 + 0.2 * hl * clamp(uc / 0.3))
            ctx.fill_preserve()
            rgba(ctx, c)
            ctx.set_line_width(4)
            ctx.stroke()
            circle(ctx, -300, y, 22, c)
            text(ctx, opt, -250, y + 2, 64, (1, 1, 1), font=CAPTION_FONT, bold=False, anchor="l")
        if uc > 0:  # "comment karo" speech bubble
            k = ease_out_back(uc / 0.3)
            ctx.save()
            ctx.translate(250, 290)
            ctx.scale(k, k)
            rrect(ctx, -200, -50, 400, 100, 30)
            ctx.move_to(-120, 50)
            ctx.line_to(-150, 90)
            ctx.line_to(-80, 50)
            rgba(ctx, GOLD)
            ctx.fill()
            text(ctx, "COMMENT KARO", 0, 2, 50, (0.05, 0.05, 0.05), font=CAPTION_FONT, bold=False)
            ctx.restore()
        ctx.restore()


SCENE_CLASSES = {"neck": Neck, "neighbours": Neighbours, "doklam": Doklam, "answer": Answer}


# ============================================================ compositor ("intel file")

def header(ctx, idx, t):
    rrect(ctx, 60, 70, 14, 50, 4)
    rgba(ctx, RED)
    ctx.fill()
    text(ctx, "REALITY SHIFT", 92, 95, 36, (1, 1, 1), a=0.9, anchor="l")
    text(ctx, "// INTEL FILE", 380, 95, 28, EDGE, font=MONO, a=0.75, anchor="l")
    if int(t * 2) % 2 == 0:
        circle(ctx, W - 250, 95, 10, RED)
    text(ctx, f"FILE {idx + 1:02d}/{len(SPEC):02d}", W - 70, 95, 30, (1, 1, 1), font=MONO, a=0.8, anchor="r")
    line(ctx, [(60, 140), (W - 60, 140)], EDGE, 1.5, 0.3)


def caption(ctx, sc, tl, accent):
    """Typewriter caption: the current Hinglish chunk types itself into a box in the 1150-1250 band."""
    cur = None
    for i, (start, _) in enumerate(sc["captions"]):
        if tl >= start - 0.03:
            cur = i
    if cur is None:
        return
    start, cap = sc["captions"][cur]
    shown = int(math.ceil(len(cap) * clamp((tl - start + 0.03) / 0.16)))
    size = 78
    words = cap.split(" ")
    ws = [text_width(ctx, w, size, font=CAPTION_FONT, bold=False) for w in words]
    gap = size * 0.28
    tw = sum(ws) + gap * (len(ws) - 1)
    fit = min(1.0, 900 / tw)
    h = CAP_BOTTOM - CAP_TOP
    rrect(ctx, 50, CAP_TOP, W - 100, h, 14)
    rgba(ctx, (0.01, 0.02, 0.03), 0.86)
    ctx.fill()
    ctx.rectangle(50, CAP_TOP, 12, h)
    rgba(ctx, accent)
    ctx.fill()
    ctx.save()
    ctx.translate(100, CAP_TOP + h / 2)
    ctx.scale(fit, fit)
    x, left = 0.0, shown
    for w, ww in zip(words, ws):
        if left <= 0:
            break
        part = w[:left]
        c = HOT.get(w.strip(PUNCT + "."), (1, 1, 1))
        text(ctx, part, x, 0, size, c, font=CAPTION_FONT, bold=False, anchor="l", stroke=(0, 0, 0), stroke_w=8)
        x += (text_width(ctx, part, size, font=CAPTION_FONT, bold=False) if len(part) < len(w) else ww + gap)
        left -= len(w) + 1
    if shown < len(cap) or int(tl * 3) % 2 == 0:  # block cursor
        ctx.rectangle(x + 6, -size * 0.42, size * 0.38, size * 0.84)
        rgba(ctx, accent, 0.9)
        ctx.fill()
    ctx.restore()


def shutter(ctx, tl, accent):
    """Two black plates part from the middle of the frame on every cut."""
    u = ease_out_cubic(tl / 0.32)
    if u >= 1:
        return
    cover = (1 - u) * H / 2
    ctx.rectangle(0, 0, W, cover)
    ctx.rectangle(0, H - cover, W, cover)
    rgba(ctx, (0.0, 0.0, 0.0))
    ctx.fill()
    for y in (cover, H - cover):
        line(ctx, [(0, y), (W, y)], accent, 18, 0.35 * (1 - u))
        line(ctx, [(0, y), (W, y)], (1, 1, 1), 4, 0.9 * (1 - u))


def compose(idx, tl):
    sc = engine.SCENES[idx]
    spec = SPEC[idx]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    # camera: a slow sideways drift and push, no punch-in
    zoom = 1.0 + 0.04 * tl / sc["dur"]
    ctx.save()
    ctx.translate(W / 2 + 14 * math.sin(tl * 0.5 + idx), H * 0.4)
    ctx.scale(zoom, zoom)
    ctx.translate(-W / 2, -H * 0.4)
    sc["obj"].draw(ctx, tl, sc["dur"])
    ctx.restore()
    vignette(ctx)
    g = cairo.LinearGradient(0, CAP_BOTTOM + 20, 0, UI_CLEAR)  # bottom 400px stays clean and dark
    g.add_color_stop_rgba(0, 0.01, 0.01, 0.02, 0)
    g.add_color_stop_rgba(1, 0.01, 0.01, 0.02, 0.95)
    ctx.rectangle(0, CAP_BOTTOM + 20, W, H)
    ctx.set_source(g)
    ctx.fill()
    ctx.rectangle(0, UI_CLEAR, W, H - UI_CLEAR)
    rgba(ctx, (0.01, 0.01, 0.02), 0.95)
    ctx.fill()
    header(ctx, idx, tl)
    caption(ctx, sc, tl, spec["accent"])
    if idx:
        shutter(ctx, tl, spec["accent"])
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
        "Sirf 22 KM Ka Rasta Jo Bharat Ko Jodta Hai | Chicken's Neck",
        "Chicken's Neck: Bharat Ka Sabse Naazuk 22 KM 😳",
        "Siliguri Corridor: 22 KM Jahan China Ki Nazar Hai",
        "Ye 22 KM Band Hue Toh 8 Rajya Bharat Se Alag",
        "Doklam 2017: China Ki Sadak Kis Taraf Ja Rahi Thi?",
        "India vs China: 22 KM Ka Chicken's Neck Kyun Ahem Hai?",
        "73 Din Aamne-Saamne: Doklam Me Kya Hua Tha?",
        "8 Rajya, 22 KM: Siliguri Corridor Ki Kahani",
        "Chicken's Neck Kya Hai? Bharat Ki 22 KM Lifeline",
        "Siliguri Corridor Explained in 40 Seconds",
    ],
    "thumb_text": "KAT GAYA TOH?",
    "queries": ["siliguri corridor", "chicken's neck", "doklam 2017"],
    "description": """
Siliguri Corridor yaani Chicken's Neck: sirf ~22 KM chauda rasta jo poore North-East (8 rajya) ko baaki Bharat se jodta hai.
Doklam 2017 me China ki sadak isi gardan ki taraf badh rahi thi, aur Indian Army 73 din aamne-saamne khadi rahi.

Is Short me:
• Siliguri Corridor kahan hai aur sabse patli jagah kitni chaudi hai (~20-22 KM)
• Chaaron taraf kaun: Nepal, Bangladesh, Bhutan aur peeche China
• Doklam stand-off (16 June - 28 August 2017) aur sadak ka kaam kaise ruka
• 33 Corps "Trishakti", jo is gardan ki hifaazat karti hai

Aapki raay: kya Bharat ko yahan doosra rasta banana chahiye? HAAN ya NAA, comment me likho.
Aisi aur geopolitics ke liye Reality Shift ko subscribe karo.

Note: video ka map schematic hai, scale pe nahi.
""",
    "tags": ["siliguri corridor", "chicken's neck", "chicken neck india", "doklam", "doklam 2017", "india vs china",
             "indian army", "trishakti corps", "north east india", "geopolitics hindi", "indian defence shorts",
             "india foreign policy", "bharat news shorts", "world affairs hindi", "reality shift"],
    "hashtags": ["#Shorts", "#SiliguriCorridor", "#IndiaVsChina"],
}


def thumbnail(ctx):
    """1080x1920 cover: KAT GAYA / TOH? over the map, the neck cut in red and the North-East pulling away."""
    v = (89.9, 26.3, 175)
    ctx.save()
    ctx.translate(0, 470)
    draw_region(ctx, v, 0.4, {"china": (CN_RED, 0.5)}, labels=("china", "bangladesh", "india"))
    poly(ctx, v, NORTH_EAST)
    rgba(ctx, (0, 0, 0))
    ctx.fill()
    ctx.save()
    ctx.translate(55, -22)
    poly(ctx, v, NORTH_EAST)
    rgba(ctx, INDIA_LAND)
    ctx.fill_preserve()
    rgba(ctx, RED, 0.35)
    ctx.fill_preserve()
    rgba(ctx, RED)
    ctx.set_line_width(6)
    ctx.stroke()
    text(ctx, "NORTH-EAST", *proj(v, 91.9, 26.1), 46, (1, 1, 1), font=MONO)
    ctx.restore()
    corridor_glow(ctx, v, 0.0, RED)
    p0, p1 = proj(v, *NEPAL_TIP), proj(v, *BD_TIP)
    glow(ctx, *p0, 220, RED, 0.6)
    line(ctx, [(p0[0] - 40, p0[1] - 30), (p1[0] + 40, p1[1] + 20)], (0, 0, 0), 40)
    line(ctx, [(p0[0] - 40, p0[1] - 30), (p1[0] + 40, p1[1] + 20)], RED, 26)
    ripple(ctx, *proj(v, *SILIGURI), 0.3, GOLD)
    ctx.restore()
    g = cairo.LinearGradient(0, 0, 0, 900)  # dark top so the words hold contrast at feed size
    g.add_color_stop_rgba(0, 0, 0, 0, 0.95)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 900)
    ctx.set_source(g)
    ctx.fill()
    vignette(ctx)
    glow(ctx, 540, 520, 600, RED, 0.25)
    text(ctx, "KAT GAYA", 540, 380, 250, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "TOH?", 540, 650, 300, RED, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=24)
    chicken(ctx, 170, 1640, 1.0, 0.0)
    text(ctx, "REALITY SHIFT", 540, 1780, 40, (1, 1, 1), a=0.7)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.chickens_neck")  # a named module, so work files land in work/<name>/
    engine.make_frame = story.make_frame
    final = engine.render(story, "edge")
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
