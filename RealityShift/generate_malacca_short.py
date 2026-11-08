"""Reality Shift Short — China's "Malacca Dilemma" and India's Great Nicobar at the mouth of the strait (~45s).

Usage:
  python generate_malacca_short.py

New "naval brief" layout (not Chicken's Neck's intel file): emblem header with a live lat/long readout of the
camera and a 4-segment progress bar, drawn map of the Indian Ocean -> South China Sea, pop-in Hinglish captions
with a growing underline in the 1150-1250 band, sonar-iris wipes between scenes, bottom 400px clean.
Ends on a HAAN / NAHI tile card and an arrow toward the comment button; no subscribe badge / bell / cursor.
Facts (as commonly reported): ~80% of China's crude imports pass through the Strait of Malacca ("Malacca Dilemma",
Hu Jintao 2003); Great Nicobar's southern tip (Indira Point) is ~150 km from Sumatra across the Six Degree Channel;
INS Baaz is the Indian Navy air station at Campbell Bay, Great Nicobar (commissioned 2012); the Great Nicobar
project (transshipment port at Galathea Bay, airport, township) is costed at ~Rs 72,000 crore.
The patrol line is framed as a capability ("pehra bitha sakti hai"), not a claim about timing.
"""

import importlib
import json
import math

import cairo
import numpy as np

import engine
from engine import *  # noqa: F401,F403
from generate_chabahar_short import Cued, partial
from generate_chickens_neck_short import view_at
from generate_maldives_short import CN_RED, CN_YELLOW
from generate_rupee_short import VOICE_TONES
from stories.reality_shift import GOLD, INDIA_GREEN, SAFFRON, flag, stamp

TOPIC = "MALACCA DILEMMA"
OUTPUTS = {"edge": "malacca_short.mp4"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.3
TAIL_PAD = 0.3
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 100
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"

RED = hexc("#FF3B3B")
SONAR = hexc("#3FD1FF")
MONO = "Consolas"

# each line: (tone, [(spoken Hindi, Hinglish caption), ...], pause after)
SPEC = [
    {"key": "oil", "accent": CN_YELLOW, "text": "CHINA KA 80% OIL BLOCK?",
     "visual": "Tankers stream from the Gulf to China, 80% gauge fills, route pinches red at Malacca, a key "
               "appears there and flies to India's Andaman & Nicobar islands",
     "vo": [("hook", [("चीन का अस्सी प्रतिशत तेल...", "CHINA KA 80% TEL...")], 0.45),
            ("punch", [("सिर्फ़ एक रास्ते से", "SIRF EK RAASTE SE"), ("आता है।", "AATA HAI!")], 0.35),
            ("low", [("और उस रास्ते की चाबी,", "AUR US RAASTE KI CHAABI,")], 0.15),
            ("punch", [("भारत के पास है।", "BHARAT KE PAAS HAI!")], 0)]},
    {"key": "dilemma", "accent": SONAR, "text": "MALACCA DILEMMA",
     "visual": "Zoom to the strait full of tankers, MALACCA DILEMMA card, Six Degree Channel gate glows, "
               "Great Nicobar pinged with a ~150 KM caliper to Sumatra, INS Baaz marker, a jet takes off",
     "vo": [("tell", [("इसे कहते हैं चीन का", "ISE KEHTE HAIN CHINA KA"), ("मलक्का डिलेमा।", "MALACCA DILEMMA.")], 0.4),
            ("low", [("मलक्का स्ट्रेट के", "MALACCA STRAIT KE"), ("ठीक मुहाने पर बैठा है", "THEEK MUHAANE PAR BAITHA HAI")],
             0.12),
            ("punch", [("भारत का ग्रेट निकोबार,", "BHARAT KA GREAT NICOBAR,")], 0.15),
            ("tell", [("और वहाँ का नौसैनिक एयरबेस,", "AUR WAHAN KA NAVAL AIRBASE,"), ("आईएनएस बाज़।", "INS BAAZ!")],
             0)]},
    {"key": "build", "accent": SAFFRON, "text": "₹72,000 CR PROJECT",
     "visual": "Close on Great Nicobar: Rs 72,000 CR counter, port with cranes rises at Galathea Bay, airstrip draws; "
               "alarm, zoom out, warships fan into a patrol line, tankers queue and turn red",
     "vo": [("build", [("अब भारत यहाँ", "AB BHARAT YAHAN"), ("बहत्तर हज़ार करोड़ का", "72,000 CRORE KA"),
                       ("मेगा पोर्ट और एयरपोर्ट", "MEGA PORT AUR AIRPORT"), ("बना रहा है।", "BANA RAHA HAI!")], 0.4),
            ("low", [("मतलब, टकराव हुआ,", "MATLAB, TAKRAAV HUA,")], 0.15),
            ("punch", [("तो भारतीय नौसेना", "TOH INDIAN NAVY"), ("इस संकरे रास्ते पर", "IS SANKRE RAASTE PAR"),
                       ("पहरा बिठा सकती है,", "PEHRA BITHA SAKTI HAI,")], 0.15),
            ("punch", [("और बीजिंग की एनर्जी लाइफलाइन", "AUR BEIJING KI ENERGY LIFELINE"),
                       ("ख़तरे में पड़ जाएगी।", "KHATRE MEIN PAD JAAYEGI!")], 0)]},
    {"key": "ask", "accent": INDIA_GREEN, "text": "AUR MAZBOOT?",
     "visual": "Wide map: Great Nicobar sends sonar rings, China flashes ALERT, then a HAAN / NAHI tile card and an "
               "arrow toward the comment button",
     "vo": [("tell", [("इसीलिए चीन,", "ISILIYE CHINA,"), ("ग्रेट निकोबार से", "GREAT NICOBAR SE"),
                      ("सबसे ज़्यादा घबराता है।", "SABSE ZYAADA GHABRAATA HAI!")], 0.5),
            ("ask", [("क्या भारत को यह बेस", "KYA BHARAT KO YEH BASE"), ("और मज़बूत करना चाहिए?", "AUR MAZBOOT KARNA CHAHIYE?")],
             0.5),
            ("cta", [("कमेंट में बताइए।", "COMMENT MEIN BATAIYE!")], 0)]},
]

DELIVERY = {s["key"]: [(VOICE_TONES[tone], " ".join(hi for hi, _ in chunks), pause) for tone, chunks, pause in s["vo"]]
            for s in SPEC}
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {"80%": CN_YELLOW, "TEL": CN_YELLOW, "EK": RED, "CHAABI": GOLD, "BHARAT": SAFFRON, "MALACCA": CN_YELLOW,
       "DILEMMA": RED, "MUHAANE": SONAR, "GREAT": SAFFRON, "NICOBAR": SAFFRON, "INS": SONAR, "BAAZ": SONAR,
       "72,000": GOLD, "CRORE": GOLD, "PORT": SONAR, "AIRPORT": SONAR, "TAKRAAV": RED, "NAVY": SAFFRON,
       "PEHRA": SAFFRON, "BEIJING": RED, "LIFELINE": RED, "KHATRE": RED, "CHINA": RED, "GHABRAATA": RED,
       "MAZBOOT": INDIA_GREEN, "COMMENT": GOLD}

CAP_TOP, CAP_BOTTOM = 1150, 1250
UI_CLEAR = H - 400
MAP_CY = 600


# ============================================================ map: Indian Ocean -> South China Sea (schematic)

LAND = [  # one mainland path: Arabia + Gulf, Pakistan, India, Bangladesh, Myanmar, Malay Peninsula, Indochina, China
    (40, 50), (40, 14.0), (43.4, 12.7), (45.0, 12.8), (49.0, 14.5), (52.2, 15.6), (55.4, 17.8), (57.8, 19.0),
    (58.5, 20.5), (59.8, 22.5), (58.6, 23.6), (57.2, 23.9), (56.4, 24.9), (56.3, 26.3), (55.4, 25.4), (54.5, 24.3),
    (52.0, 24.0), (51.6, 25.9), (50.1, 26.5), (48.5, 28.4), (47.9, 29.9), (48.8, 30.4), (50.3, 30.0), (51.4, 27.9),
    (53.5, 26.8), (55.4, 26.7), (56.3, 27.2), (57.3, 25.9), (58.8, 25.5), (61.6, 25.15), (64.6, 25.2), (66.6, 25.45),
    (67.3, 24.2), (68.2, 23.7), (70.0, 22.9), (69.1, 22.4), (70.6, 20.9), (72.6, 21.4), (72.9, 19.0), (73.3, 17.0),
    (73.8, 15.5), (74.8, 12.9), (75.9, 11.0), (76.9, 8.6), (77.5, 8.1), (78.2, 8.9), (79.0, 9.3), (79.9, 10.3),
    (79.8, 11.9), (80.3, 13.1), (80.2, 15.5), (81.3, 16.3), (82.3, 16.6), (84.0, 18.3), (85.8, 19.8), (87.0, 21.0),
    (88.2, 21.8), (89.0, 21.7), (90.0, 22.0), (91.8, 22.4), (92.3, 21.2), (93.5, 19.5), (94.3, 18.0), (94.5, 16.0),
    (95.4, 15.7), (97.6, 16.5), (97.7, 15.0), (98.6, 13.0), (98.5, 10.0), (98.3, 8.0), (99.6, 7.0), (100.1, 6.4),
    (100.3, 5.4), (100.9, 4.0), (101.4, 3.0), (102.25, 2.2), (103.5, 1.3), (104.3, 1.4), (103.8, 2.4), (103.3, 3.8),
    (103.4, 5.3), (102.2, 6.2), (100.6, 7.2), (100.3, 8.4), (99.9, 9.5), (99.2, 10.4), (99.9, 12.5), (100.0, 13.5),
    (101.0, 12.7), (102.7, 12.0), (103.5, 10.6), (104.8, 8.6), (106.8, 10.4), (109.2, 11.9), (109.3, 13.4),
    (108.8, 15.4), (106.6, 17.5), (105.7, 19.0), (106.7, 20.7), (108.0, 21.5), (109.8, 21.4), (110.5, 20.3),
    (111.0, 21.5), (113.5, 22.2), (116.5, 23.0), (119.0, 25.5), (121.9, 30.9), (121.5, 32.0), (130, 40), (130, 50),
]
INDIA = [(68.2, 23.7), (70.0, 22.9), (69.1, 22.4), (70.6, 20.9), (72.6, 21.4), (72.9, 19.0), (73.3, 17.0), (73.8, 15.5),
         (74.8, 12.9), (75.9, 11.0), (76.9, 8.6), (77.5, 8.1), (78.2, 8.9), (79.0, 9.3), (79.9, 10.3), (79.8, 11.9),
         (80.3, 13.1), (80.2, 15.5), (81.3, 16.3), (82.3, 16.6), (84.0, 18.3), (85.8, 19.8), (87.0, 21.0), (88.2, 21.8),
         (89.0, 21.9), (88.7, 24.3), (88.1, 26.5), (88.2, 27.9), (86.0, 28.0), (80.1, 30.4), (79.0, 32.5), (76.0, 35.5),
         (74.5, 34.5), (73.5, 32.0), (71.0, 28.5), (69.5, 27.0), (70.5, 25.5)]
CHINA = [(97.5, 28.2), (98.6, 25.5), (99.3, 22.5), (101.2, 21.6), (102.4, 22.6), (105.5, 23.2), (106.7, 22.8),
         (108.0, 21.5), (109.8, 21.4), (110.5, 20.3), (111.0, 21.5), (113.5, 22.2), (116.5, 23.0), (119.0, 25.5),
         (121.9, 30.9), (121.5, 32.0), (130, 40), (130, 50), (73, 50), (74.5, 37.0), (79.0, 35.5), (79.0, 32.5),
         (80.1, 30.4), (86.0, 28.0), (88.2, 27.9), (92.0, 27.9)]
HAINAN = [(108.6, 19.2), (110.0, 20.1), (111.0, 19.6), (110.2, 18.3), (109.0, 18.4)]
SRI_LANKA = [(79.85, 9.8), (80.9, 9.0), (81.9, 7.0), (81.6, 6.2), (80.6, 5.9), (80.0, 6.5), (79.8, 8.0)]
SUMATRA = [(95.3, 5.55), (97.1, 5.2), (98.7, 3.8), (100.4, 2.2), (101.5, 1.6), (103.7, -0.9), (104.8, -2.2),
           (106.0, -3.3), (105.8, -5.8), (104.5, -5.9), (102.3, -4.0), (100.9, -2.0), (100.3, -0.9), (99.0, 1.0),
           (97.6, 2.4), (96.4, 4.2), (95.2, 5.2)]
JAVA = [(105.2, -6.8), (108.0, -6.3), (111.0, -6.5), (114.5, -7.7), (114.4, -8.7), (110.0, -8.1), (106.4, -7.4)]
BORNEO = [(109.0, 1.5), (109.6, -1.0), (110.2, -3.0), (114.5, -4.0), (116.3, -2.5), (117.6, 1.0), (119.0, 5.0),
          (116.8, 7.0), (115.0, 5.0), (113.0, 3.2), (111.0, 1.7)]
ANDAMAN = [(92.75, 13.65), (93.05, 13.4), (92.95, 12.5), (92.8, 11.6), (92.7, 11.0), (92.55, 10.55), (92.4, 10.75),
           (92.55, 11.6), (92.6, 12.4), (92.7, 13.2)]
CAR_NICOBAR = [(92.7, 9.25), (92.82, 9.22), (92.8, 9.1), (92.7, 9.12)]
NANCOWRY = [(93.35, 8.05), (93.6, 8.1), (93.62, 7.9), (93.4, 7.88)]
LITTLE_NICOBAR = [(93.62, 7.42), (93.75, 7.4), (93.73, 7.28), (93.62, 7.3)]
GREAT_NICOBAR = [(93.72, 7.23), (93.84, 7.21), (93.91, 7.12), (93.94, 7.0), (93.92, 6.9), (93.88, 6.8), (93.84, 6.75),
                 (93.79, 6.8), (93.72, 6.9), (93.66, 7.02), (93.67, 7.14)]
INDIA_ISLANDS = [ANDAMAN, CAR_NICOBAR, NANCOWRY, LITTLE_NICOBAR, GREAT_NICOBAR]
FOREIGN_ISLANDS = [SRI_LANKA, SUMATRA, JAVA, BORNEO]

# oil route, Strait of Hormuz -> Six Degree Channel -> Malacca -> Singapore -> South China coast
ROUTE = [(56.5, 26.4), (58.6, 24.0), (60.5, 22.0), (64.0, 18.0), (70.0, 12.0), (76.0, 6.8), (80.4, 5.3), (86.0, 5.6),
         (92.0, 6.1), (94.5, 6.2), (96.8, 5.6), (98.6, 4.3), (100.3, 3.0), (101.6, 2.25), (103.0, 1.35), (104.4, 1.15),
         (105.3, 2.2), (107.5, 6.0), (110.0, 10.0), (112.0, 15.0), (113.8, 20.0), (113.9, 21.8)]
STRAIT_SEG = ROUTE[10:16]
GN = (93.82, 6.98)
INDIRA_POINT = (93.84, 6.75)
ACEH = (95.3, 5.55)
CAMPBELL_BAY = (93.93, 7.0)
GALATHEA = (93.885, 6.82)
MALACCA = (101.0, 2.6)
GATE = [(93.86, 6.72), (95.28, 5.62)]
QUEUE = [(94.1, 6.19), (93.65, 6.17), (93.2, 6.15), (92.75, 6.13), (92.3, 6.11)]
CHANNEL = (94.6, 5.85, 260)   # camera on the Six Degree Channel

LABELS = [("INDIA", 78.5, 21.0, "land"), ("CHINA", 108.0, 28.0, "land"), ("MYANMAR", 96.0, 20.5, "land"),
          ("THAILAND", 101.5, 15.5, "land"), ("MALAYSIA", 102.0, 4.3, "land"), ("SUMATRA", 101.8, -1.6, "land"),
          ("SRI LANKA", 80.8, 7.6, "land"), ("BAY OF BENGAL", 88.0, 15.0, "sea"), ("INDIAN OCEAN", 78.0, -1.0, "sea"),
          ("SOUTH CHINA SEA", 113.0, 13.0, "sea"), ("ARABIAN SEA", 64.0, 14.0, "sea")]

WATER_TOP, WATER_BOT = hexc("#04192B"), hexc("#020A14")
FOREIGN_LAND = hexc("#1A222C")
INDIA_LAND = hexc("#1C2A22")
COAST = hexc("#6FB8D8")
TANKER = hexc("#B0413A")
STEEL = hexc("#8FA3B5")


def proj(v, lon, lat):
    lon0, lat0, s = v
    return W / 2 + (lon - lon0) * s * 0.9, MAP_CY - (lat - lat0) * s


def poly(ctx, v, pts):
    ctx.move_to(*proj(v, *pts[0]))
    for p in pts[1:]:
        ctx.line_to(*proj(v, *p))
    ctx.close_path()


def draw_map(ctx, v, t, tint=None):
    """Sea, graticule, land; tint = {"china" | "india": (colour, 0..1)}."""
    tint = tint or {}
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *WATER_TOP)
    g.add_color_stop_rgb(1, *WATER_BOT)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()
    s = v[2]
    step = 0.25 if s > 700 else (1 if s > 160 else (2 if s > 60 else 10))
    lon0, lat0, _ = v
    for k in range(-40, 41):
        x = proj(v, round(lon0 / step) * step + k * step, lat0)[0]
        if -5 < x < W + 5:
            line(ctx, [(x, 0), (x, H)], SONAR, 1, 0.06)
        y = proj(v, lon0, round(lat0 / step) * step + k * step)[1]
        if -5 < y < H + 5:
            line(ctx, [(0, y), (W, y)], SONAR, 1, 0.06)
    for pts in [LAND, HAINAN] + FOREIGN_ISLANDS:
        poly(ctx, v, pts)
        rgba(ctx, FOREIGN_LAND)
        ctx.fill()
    c, k = tint.get("china", (CN_RED, 0))
    for pts in (CHINA, HAINAN):
        poly(ctx, v, pts)
        rgba(ctx, c, 0.3 * k)
        ctx.fill()
    ci, ki = tint.get("india", (SAFFRON, 0))
    for pts in [INDIA] + INDIA_ISLANDS:
        poly(ctx, v, pts)
        rgba(ctx, INDIA_LAND)
        ctx.fill_preserve()
        rgba(ctx, ci, 0.3 * ki)
        ctx.fill()
    for pts in [LAND, HAINAN] + FOREIGN_ISLANDS:
        poly(ctx, v, pts)
        rgba(ctx, COAST, 0.18)
        ctx.set_line_width(7)
        ctx.stroke_preserve()
        rgba(ctx, COAST, 0.6)
        ctx.set_line_width(2)
        ctx.stroke()
    for pts, (cc, kk) in [(CHINA, (c, k))] + [(p, (ci, ki)) for p in [INDIA] + INDIA_ISLANDS]:
        poly(ctx, v, pts)
        rgba(ctx, cc if kk else COAST, 0.35 + 0.6 * kk)
        ctx.set_line_width(2.5 + 2 * kk)
        ctx.stroke()
    for name, lon, lat, kind in LABELS:
        x, y = proj(v, lon, lat)
        if 60 < x < W - 60 and 190 < y < CAP_TOP - 50:
            col = (0.55, 0.75, 0.88) if kind == "sea" else (0.85, 0.9, 0.9)
            if name == "CHINA" and k:
                col = c
            if name == "INDIA" and ki:
                col = ci
            text(ctx, name, x, y, 26 if kind == "sea" else 34, col, font=MONO, a=0.45 if kind == "sea" else 0.75)


def along(pts, u):
    """(x, y, heading) at fraction u along a screen polyline."""
    u = clamp(u, 0, 0.998)
    _, a = partial(pts, u)
    _, b = partial(pts, u + 0.002)
    return a[0], a[1], math.atan2(b[1] - a[1], b[0] - a[0])


# ============================================================ props

def tanker(ctx, x, y, ang, s, c=TANKER, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(s, s)
    ctx.move_to(-30, -9)
    ctx.line_to(22, -9)
    ctx.line_to(33, 0)
    ctx.line_to(22, 9)
    ctx.line_to(-30, 9)
    ctx.close_path()
    rgba(ctx, (0, 0, 0), 0.5 * a)
    ctx.set_line_width(5)
    ctx.stroke_preserve()
    rgba(ctx, c, a)
    ctx.fill()
    line(ctx, [(-18, 0), (16, 0)], shade(c, 0.6), 3, a)
    ctx.rectangle(-28, -6, 9, 12)
    rgba(ctx, (0.95, 0.95, 0.95), a)
    ctx.fill()
    ctx.restore()


def warship(ctx, x, y, ang, s, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(s, s)
    ctx.move_to(-42, -9)
    ctx.line_to(28, -9)
    ctx.line_to(48, 0)
    ctx.line_to(28, 9)
    ctx.line_to(-42, 9)
    ctx.close_path()
    rgba(ctx, (0, 0, 0), 0.5 * a)
    ctx.set_line_width(5)
    ctx.stroke_preserve()
    rgba(ctx, STEEL, a)
    ctx.fill()
    rrect(ctx, -18, -6, 26, 12, 3)
    rgba(ctx, shade(STEEL, 1.25), a)
    ctx.fill()
    circle(ctx, 18, 0, 4, shade(STEEL, 0.6), a)
    ctx.rectangle(-40, -3, 12, 6)
    rgba(ctx, SAFFRON, a)
    ctx.fill()
    ctx.restore()


def key_icon(ctx, x, y, s, c, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    glow(ctx, 0, 0, 90, c, 0.5)
    ctx.arc(-38, 0, 24, 0, math.tau)
    rgba(ctx, (0, 0, 0), 0.6)
    ctx.set_line_width(18)
    ctx.stroke_preserve()
    rgba(ctx, c)
    ctx.set_line_width(11)
    ctx.stroke()
    line(ctx, [(-14, 0), (54, 0)], (0, 0, 0), 18, 0.6)
    line(ctx, [(-14, 0), (54, 0)], c, 11)
    for px, h in ((36, 20), (50, 15)):
        line(ctx, [(px, 0), (px, h)], c, 10)
    ctx.restore()


def ping(ctx, x, y, t, c, rmax=150, n=3):
    for k in range(n):
        r = (t * 0.7 + k / n) % 1.0
        ctx.arc(x, y, 16 + rmax * r, 0, math.tau)
        rgba(ctx, c, 0.75 * (1 - r))
        ctx.set_line_width(3)
        ctx.stroke()
    glow(ctx, x, y, 46, c, 0.9)
    circle(ctx, x, y, 9, (1, 1, 1))


def callout(ctx, s, x, y, c, u, size=40, sub=None, pin=None):
    """Pill with an accent bar that wipes open, optional leader line to a map pin."""
    if u <= 0:
        return
    w = max(text_width(ctx, s, size, font=MONO), text_width(ctx, sub, size * 0.62, font=MONO) if sub else 0) + 60
    h = size * (2.2 if sub else 1.45)
    k = ease_out_cubic(u / 0.3)
    if pin:
        px, py = pin
        line(ctx, [(px, py), (lerp(px, x, k), lerp(py, y, k))], c, 3, 0.9)
        circle(ctx, px, py, 7, c)
    ctx.save()
    ctx.translate(x, y)
    ctx.rectangle(-w / 2, -h / 2 - 6, w * k, h + 12)
    ctx.clip()
    rrect(ctx, -w / 2, -h / 2, w, h, h / 2)
    rgba(ctx, (0.01, 0.03, 0.05), 0.9)
    ctx.fill_preserve()
    rgba(ctx, c, 0.9)
    ctx.set_line_width(3)
    ctx.stroke()
    circle(ctx, -w / 2 + 26, -size * 0.42 if sub else 0, 8, c)
    text(ctx, s, 12, -size * 0.42 if sub else 0, size, (1, 1, 1), font=MONO)
    if sub:
        text(ctx, sub, 12, size * 0.55, size * 0.62, c, font=MONO)
    ctx.restore()


def gauge(ctx, x, y, r, frac, c, label):
    ctx.arc(x, y, r, 0, math.tau)
    rgba(ctx, (0.01, 0.03, 0.05), 0.85)
    ctx.fill()
    ctx.arc(x, y, r - 14, 0, math.tau)
    rgba(ctx, c, 0.18)
    ctx.set_line_width(20)
    ctx.stroke()
    if frac > 0:
        ctx.arc(x, y, r - 14, -math.pi / 2, -math.pi / 2 + math.tau * frac)
        rgba(ctx, c)
        ctx.set_line_width(20)
        ctx.stroke()
    text(ctx, f"{round(frac * 100)}%", x, y - 6, r * 0.62, (1, 1, 1), font=CAPTION_FONT, bold=False,
         stroke=(0, 0, 0), stroke_w=6)
    text(ctx, label, x, y + r + 30, 24, c, font=MONO, stroke=(0, 0, 0), stroke_w=5)


def caliper(ctx, p0, p1, u, c, label):
    if u <= 0:
        return
    k = ease_out_cubic(u / 0.5)
    b = lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k)
    ctx.set_dash([14, 10])
    line(ctx, [p0, b], c, 5)
    ctx.set_dash([])
    for p in (p0, b):
        circle(ctx, *p, 9, c)
    mx, my = lerp(p0[0], p1[0], 0.5), lerp(p0[1], p1[1], 0.5)
    callout(ctx, label, mx + 150, my + 40, c, u - 0.3, size=48)


def airbase(ctx, x, y, s, c, u):
    """Round marker with a runway and a plane glyph."""
    if u <= 0:
        return
    k = ease_out_back(u / 0.35)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s * k, s * k)
    circle(ctx, 0, 0, 44, (0.01, 0.03, 0.05), 0.9)
    ctx.arc(0, 0, 44, 0, math.tau)
    rgba(ctx, c)
    ctx.set_line_width(4)
    ctx.stroke()
    ctx.rotate(-0.5)
    rrect(ctx, -8, -30, 16, 60, 3)
    rgba(ctx, (0.6, 0.65, 0.7))
    ctx.fill()
    ctx.restore()
    jet(ctx, x + 4 * s, y, -0.5 - math.pi / 2, 0.7 * s * k, (1, 1, 1))


def jet(ctx, x, y, ang, s, c, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(s, s)
    ctx.move_to(30, 0)
    ctx.line_to(-6, -6)
    ctx.line_to(-12, -28)
    ctx.line_to(-20, -28)
    ctx.line_to(-16, -5)
    ctx.line_to(-28, -4)
    ctx.line_to(-34, -14)
    ctx.line_to(-38, -14)
    ctx.line_to(-36, 0)
    ctx.line_to(-38, 14)
    ctx.line_to(-34, 14)
    ctx.line_to(-28, 4)
    ctx.line_to(-16, 5)
    ctx.line_to(-20, 28)
    ctx.line_to(-12, 28)
    ctx.line_to(-6, 6)
    ctx.close_path()
    rgba(ctx, c, a)
    ctx.fill()
    ctx.restore()


def crane(ctx, x, y, s, u, c=GOLD):
    """Dock crane rising from (x, y): mast grows, then the jib swings out."""
    if u <= 0:
        return
    m = ease_out_cubic(u / 0.5)
    top = y - 120 * s * m
    line(ctx, [(x - 14 * s, y), (x, top), (x + 14 * s, y)], c, 4 * s)
    line(ctx, [(x, y), (x, top)], c, 6 * s)
    j = ease_out_cubic((u - 0.4) / 0.4)
    if j > 0:
        line(ctx, [(x - 20 * s, top), (x + 80 * s * j, top)], c, 5 * s)
        line(ctx, [(x + 70 * s * j, top), (x + 70 * s * j, top + 40 * s)], (0.8, 0.8, 0.8), 2)


# ============================================================ scenes

WIDE = (89.0, 13.0, 17)
MID = (96.0, 11.0, 26)


class Oil(Cued):
    """Tankers Gulf -> China, 80% gauge, the route pinches at Malacca, a key appears and flies to India."""

    def beats(self, d):
        c = self.cue
        return {"tel": c("80%", 0.05), "raasta": c("EK RAASTE", d * 0.3), "chaabi": c("CHAABI", d * 0.6),
                "bharat": c("BHARAT KE", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        ticks = [(b["tel"] + 0.15 + k * 0.06, "tick" if k % 2 else "tock") for k in range(12)]
        return [(0.02, "boom"), (b["tel"] + 0.1, "beep"), (b["raasta"], "thud"), (b["raasta"] + 0.08, "alarm"),
                (b["chaabi"], "dingdong"), (b["bharat"], "boom"), (b["bharat"] + 0.1, "whoosh")] + ticks

    def draw(self, ctx, t, d):
        b = self.beats(d)
        v = self.view = view_at([(0.0, WIDE), (b["raasta"] + 0.1, WIDE), (b["bharat"] + 0.3, MID)], t)
        india = clamp((t - b["bharat"]) / 0.4)
        draw_map(ctx, v, t, {"china": (CN_RED, 0.55), "india": (SAFFRON, india)})
        pts = [proj(v, *p) for p in ROUTE]
        line(ctx, pts, GOLD, 12, 0.15)
        ctx.set_dash([18, 12], -t * 90)
        line(ctx, pts, GOLD, 4, 0.8)
        ctx.set_dash([])
        s = clamp(v[2] / 22, 0.75, 1.2)
        for k in range(10):
            tanker(ctx, *along(pts, (t * 0.04 + k / 10) % 1), s)
        mx, my = proj(v, *MALACCA)
        u = t - b["raasta"]
        if u > 0:  # the whole route funnels through one strait
            seg = [proj(v, *p) for p in STRAIT_SEG]
            line(ctx, seg, RED, 22, 0.3 * clamp(u / 0.3))
            line(ctx, seg, RED, 9, clamp(u / 0.3))
            ping(ctx, mx, my, t, RED, 130)
            if t < b["bharat"]:
                callout(ctx, "1 ROUTE: MALACCA", 650, my - 170, RED, u, size=40, pin=(mx, my - 14))
        u = t - b["chaabi"]
        gx, gy = proj(v, *GN)
        if u > 0:
            fly = ease_in_out((t - b["bharat"]) / 0.7) if t > b["bharat"] else 0.0
            kx, ky = lerp(mx + 20, gx + 60, fly), lerp(my + 110, gy - 40, fly) + 8 * math.sin(t * 4)
            key_icon(ctx, kx, ky, ease_out_back(u / 0.35), GOLD, -0.3 + 0.3 * fly)
        u = t - b["bharat"]
        if u > 0:
            ping(ctx, gx, gy, t, SAFFRON, 170)
            callout(ctx, "ANDAMAN & NICOBAR", 330, gy + 160, SAFFRON, u - 0.4, size=36, sub="INDIA", pin=(gx, gy))
        u = t - b["tel"]
        if u > 0 and t < b["bharat"]:
            gauge(ctx, 220, 920, 120, 0.8 * ease_out_cubic(u / 1.0), CN_YELLOW, "CHINA OIL IMPORTS")
        if t < 3.0:  # the cold-open hook text, first 3 seconds
            ctx.push_group()
            stamp(ctx, 540, 270, t, -0.03, 940, 190, CN_YELLOW,
                  [("CHINA KA 80% OIL", -34, 80, (1, 1, 1)), ("BLOCK?", 48, 80, CN_YELLOW)])
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(clamp((3.0 - t) / 0.25))


class Dilemma(Cued):
    """Strait full of tankers, MALACCA DILEMMA card, Six Degree gate, Great Nicobar ~150 KM, INS Baaz + jet."""

    def beats(self, d):
        c = self.cue
        return {"dil": c("DILEMMA", d * 0.12), "strait": c("MALACCA STRAIT", d * 0.3), "muh": c("MUHAANE", d * 0.4),
                "gn": c("GREAT NICOBAR", d * 0.55), "base": c("NAVAL AIRBASE", d * 0.72), "baaz": c("INS BAAZ", d * 0.88)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["dil"], "boom"), (b["strait"], "whoosh"), (b["muh"], "beep"),
                (b["muh"] + 0.2, "beep"), (b["gn"], "thud"), (b["gn"] + 0.3, "pick"), (b["base"], "pop"),
                (b["baaz"], "zap"), (b["baaz"] + 0.1, "engine", 1.2)]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        v = self.view = view_at([(0.0, MID), (b["strait"], (98.5, 4.5, 100)), (b["gn"] - 0.1, (98.5, 4.5, 100)),
                                 (b["gn"] + 0.4, (95.0, 6.2, 190)), (b["base"] + 0.2, (95.0, 6.2, 190)),
                                 (b["baaz"] + 0.4, (94.2, 6.75, 420))], t)
        draw_map(ctx, v, t, {"china": (CN_RED, 0.4), "india": (SAFFRON, 0.45)})
        pts = [proj(v, *p) for p in ROUTE]
        ctx.set_dash([18, 12], -t * 90)
        line(ctx, pts, GOLD, 3, 0.5)
        ctx.set_dash([])
        s = clamp(v[2] / 90, 0.8, 1.6)
        for k in range(26):
            tanker(ctx, *along(pts, (t * 0.012 + k / 26) % 1), s)
        u = t - b["strait"]
        if u > 0:  # name the strait along its axis
            p0, p1 = proj(v, 99.0, 4.6), proj(v, 102.2, 1.9)
            ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
            ctx.save()
            ctx.translate(lerp(p0[0], p1[0], 0.5) + 60 * math.sin(ang), lerp(p0[1], p1[1], 0.5) - 60 * math.cos(ang))
            ctx.rotate(ang)
            text(ctx, "MALACCA STRAIT", 0, 0, 38, CN_YELLOW, font=MONO, a=clamp(u / 0.3), stroke=(0, 0, 0), stroke_w=6)
            ctx.restore()
        g0, g1 = proj(v, *GATE[0]), proj(v, *GATE[1])
        u = t - b["muh"]
        if u > 0:  # the mouth of the strait: the Six Degree Channel
            k = ease_out_cubic(u / 0.5)
            end = (lerp(g0[0], g1[0], k), lerp(g0[1], g1[1], k))
            line(ctx, [g0, end], SONAR, 22, 0.25 + 0.1 * math.sin(t * 6))
            line(ctx, [g0, end], SONAR, 5)
            if t < b["gn"]:
                callout(ctx, "SIX DEGREE CHANNEL", 600, lerp(g0[1], g1[1], 0.5) + 230, SONAR, u, size=38,
                        sub="STRAIT KA MUHAANA", pin=(lerp(g0[0], g1[0], 0.5), lerp(g0[1], g1[1], 0.5)))
        gx, gy = proj(v, *GN)
        u = t - b["gn"]
        if u > 0:
            ping(ctx, gx, gy, t, SAFFRON, 160)
            flag(ctx, gx - 140, gy - 150, 90, 60, "in", t, pole=110)
            if t < b["baaz"]:
                callout(ctx, "GREAT NICOBAR", 330, gy - 230, SAFFRON, u, size=46, sub="INDIA", pin=(gx, gy - 20))
                caliper(ctx, proj(v, *INDIRA_POINT), proj(v, *ACEH), u - 0.3, GOLD, "~150 KM")
        bx, by = proj(v, *CAMPBELL_BAY)
        u = t - b["base"]
        if u > 0:
            airbase(ctx, bx + 120, by + 40, 1.0, SONAR, u)
            line(ctx, [(bx, by), (bx + 80, by + 30)], SONAR, 3, 0.9)
        u = t - b["baaz"]
        if u > 0:
            stamp(ctx, 540, 300, u, -0.03, 560, 170, SONAR,
                  [("INS BAAZ", -26, 96, (1, 1, 1)), ("NAVAL AIR STATION", 50, 34, SONAR)])
            k = ease_in_out(u / 1.2)
            jx, jy = lerp(bx + 120, 980, k), lerp(by + 40, 560, k * k)
            for q in range(1, 6):  # contrail
                circle(ctx, lerp(bx + 120, jx, 1 - q * 0.08), lerp(by + 40, jy, 1 - q * 0.08), 8 - q, (1, 1, 1),
                       0.35 - 0.05 * q)
            jet(ctx, jx, jy, math.atan2(560 - by, 980 - bx) * 0.3 - 0.4, 1.3, (1, 1, 1))
        if t < b["gn"] and t > b["dil"]:
            stamp(ctx, 540, 280, t - b["dil"], 0.03, 760, 180, CN_RED,
                  [("MALACCA DILEMMA", -28, 92, CN_YELLOW), ("CHINA KA SABSE BADA DAR", 50, 38, (1, 1, 1))])


class Build(Cued):
    """Great Nicobar close-up: Rs 72,000 CR, port + cranes, airstrip; then the navy patrol line and the tanker queue."""

    def beats(self, d):
        c = self.cue
        return {"cr": c("72,000", d * 0.1), "port": c("MEGA PORT", d * 0.2), "bana": c("BANA RAHA", d * 0.3),
                "tak": c("TAKRAAV", d * 0.42), "navy": c("INDIAN NAVY", d * 0.52), "pehra": c("PEHRA", d * 0.66),
                "life": c("LIFELINE", d * 0.8), "khatre": c("KHATRE", d * 0.9)}

    def events(self, d):
        b = self.beats(d)
        ticks = [(b["cr"] + k * 0.06, "tick" if k % 2 else "tock") for k in range(12)]
        return [(0.02, "whoosh"), (b["cr"], "kaching"), (b["port"], "thud"), (b["port"] + 0.3, "thud"),
                (b["bana"], "pick"), (b["tak"], "alarm"), (b["tak"] + 0.05, "boom"), (b["navy"], "engine", 1.4),
                (b["pehra"], "thud"), (b["pehra"] + 0.2, "beep"), (b["life"], "alarm"), (b["khatre"], "boom")] + ticks

    def draw(self, ctx, t, d):
        b = self.beats(d)
        close = (93.83, 6.98, 1150)
        v = self.view = view_at([(0.0, (94.2, 6.75, 420)), (b["cr"], close), (b["tak"], close),
                                 (b["navy"] + 0.3, CHANNEL)], t)
        draw_map(ctx, v, t, {"china": (CN_RED, 0.4), "india": (SAFFRON, 0.4)})
        sz = v[2] / 1150
        px, py = proj(v, *GALATHEA)
        u = t - b["port"]
        if u > 0 and sz > 0.3:  # transshipment port: pier, containers, cranes, a docked ship
            k = ease_out_cubic(u / 0.5)
            rrect(ctx, px, py - 110 * sz, 70 * sz * k, 220 * sz, 6)
            rgba(ctx, (0.45, 0.48, 0.5))
            ctx.fill()
            for i in range(8):
                if u > 0.15 + 0.06 * i:
                    ctx.rectangle(px + 8 * sz, py - 100 * sz + i * 26 * sz, 26 * sz, 20 * sz)
                    rgba(ctx, (SAFFRON, SONAR, CN_YELLOW, INDIA_GREEN)[i % 4])
                    ctx.fill()
            for i in range(3):
                crane(ctx, px + 58 * sz, py - 70 * sz + i * 70 * sz, sz, u - 0.2 - 0.15 * i)
            if u > 0.6:
                tanker(ctx, px + 130 * sz, py, -math.pi / 2, 3.2 * sz, STEEL, clamp((u - 0.6) / 0.3))
        u = t - b["port"] - 0.4
        if u > 0 and sz > 0.3:  # new airstrip across the island
            a0, a1 = proj(v, 93.79, 7.13), proj(v, 93.82, 6.93)
            k = ease_out_cubic(u / 0.6)
            end = (lerp(a0[0], a1[0], k), lerp(a0[1], a1[1], k))
            line(ctx, [a0, end], (0.12, 0.12, 0.14), 34 * sz)
            ctx.set_dash([16 * sz, 14 * sz])
            line(ctx, [a0, end], (1, 1, 1), 3 * sz, 0.9)
            ctx.set_dash([])
            if t < b["tak"]:
                callout(ctx, "AIRPORT", end[0] - 260 * sz, end[1] - 40, SONAR, u, size=38, pin=end)
        if b["port"] < t < b["tak"]:
            callout(ctx, "MEGA PORT", px + 160 * sz, py + 150 * sz, GOLD, t - b["port"], size=38,
                    sub="GALATHEA BAY", pin=(px + 40 * sz, py + 100 * sz))
        u = t - b["cr"]
        if u > 0 and t < b["tak"]:
            val = round(72 * ease_out_cubic(u / 0.8)) * 1000
            stamp(ctx, 540, 280, 1.0 if u > 0.2 else u, -0.02, 640, 180, GOLD,
                  [(f"₹{val:,} CR", -24, 92, GOLD), ("GREAT NICOBAR PROJECT", 52, 34, (1, 1, 1))])
        pts = [proj(v, *p) for p in ROUTE]
        g0, g1 = proj(v, *GATE[0]), proj(v, *GATE[1])
        if t < b["pehra"]:
            for k in range(26):
                tanker(ctx, *along(pts, (t * 0.012 + k / 26) % 1), clamp(v[2] / 90, 0.8, 1.6))
        u = t - b["navy"]
        if u > 0:  # warships fan out from the island into a line across the channel
            gx, gy = proj(v, 93.9, 6.85)
            for i in range(5):
                f = 0.1 + 0.2 * i
                tx, ty = lerp(g0[0], g1[0], f), lerp(g0[1], g1[1], f)
                k = ease_in_out((u - 0.12 * i) / 0.9)
                if k > 0:
                    x, y = lerp(gx, tx, k), lerp(gy, ty, k)
                    ang = math.atan2(ty - gy, tx - gx) if k < 0.85 else math.pi   # end facing the incoming tankers
                    if k < 1:
                        line(ctx, [(gx, gy), (x, y)], (1, 1, 1), 2, 0.25)
                    warship(ctx, x, y + 3 * math.sin(t * 2 + i), ang, 0.95)
        u = t - b["pehra"]
        if u > 0:
            k = ease_out_cubic(u / 0.5)
            ctx.set_dash([20, 12], -t * 40)
            line(ctx, [g0, (lerp(g0[0], g1[0], k), lerp(g0[1], g1[1], k))], SAFFRON, 6, 0.9)
            ctx.set_dash([])
            line(ctx, [g0, g1], SAFFRON, 28, 0.15 * k)
            if t < b["life"]:
                callout(ctx, "NAVY PATROL LINE", 560, 300, SAFFRON, u, size=44, sub="PEHRA",
                        pin=(lerp(g0[0], g1[0], 0.5), lerp(g0[1], g1[1], 0.5)))
            red = clamp((t - b["life"]) / 0.4)
            for i, q in enumerate(QUEUE):  # tankers held up before the line
                qx, qy = proj(v, *q)
                c = tuple(lerp(a, bb, red) for a, bb in zip(STEEL, RED))
                tanker(ctx, qx, qy + 2 * math.sin(t * 2 + i), 0.0, 1.25, c, clamp((u - 0.1 * i) / 0.3))
            if red:  # the line beyond the gate to Beijing flickers out
                ctx.set_dash([10, 14])
                line(ctx, pts[9:], RED, 5, red * (0.5 + 0.4 * math.sin(t * 12)))
                ctx.set_dash([])
                if t < b["khatre"]:
                    callout(ctx, "BEIJING KI LIFELINE", 560, 300, RED, t - b["life"], size=44)
        u = t - b["tak"]
        if u > 0:  # red alarm wash
            pulse = 0.5 + 0.5 * math.sin(u * 9)
            g = cairo.RadialGradient(W / 2, MAP_CY, 300, W / 2, MAP_CY, 1100)
            g.add_color_stop_rgba(0, *RED, 0)
            g.add_color_stop_rgba(1, *RED, (0.12 + 0.12 * pulse) * clamp(u / 0.2))
            ctx.rectangle(0, 0, W, H)
            ctx.set_source(g)
            ctx.fill()
            if t < b["navy"]:
                stamp(ctx, 540, 300, u, 0.03, 520, 150, RED, [("TAKRAAV?", 0, 100, RED)])
        u = t - b["khatre"]
        if u > 0:
            stamp(ctx, 540, 300, u, -0.04, 820, 150, RED, [("LIFELINE KHATRE MEIN", 0, 80, (1, 1, 1))])


class Ask(Cued):
    """Great Nicobar sends sonar rings, China flashes ALERT; HAAN / NAHI tiles and an arrow to the comment button."""

    def beats(self, d):
        c = self.cue
        return {"chn": c("ISILIYE", 0.05), "gn": c("GREAT NICOBAR SE", d * 0.12), "ghab": c("GHABRAATA", d * 0.25),
                "q": c("KYA BHARAT", d * 0.45), "cmt": c("COMMENT", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "whoosh"), (b["gn"], "beep"), (b["ghab"], "alarm"), (b["ghab"] + 0.1, "boom"),
                (b["q"], "whoosh"), (b["q"] + 0.3, "pop"), (b["q"] + 0.45, "pop"), (b["cmt"], "dingdong")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        v = self.view = view_at([(0.0, CHANNEL), (b["gn"] + 0.3, (103.0, 18.0, 30))], t)
        alert = clamp((t - b["ghab"]) / 0.3)
        draw_map(ctx, v, t, {"china": (CN_RED, 0.5 + 0.5 * alert * (0.6 + 0.4 * math.sin(t * 10))),
                             "india": (SAFFRON, 0.6)})
        gx, gy = proj(v, *GN)
        ping(ctx, gx, gy, t, SAFFRON, 420 if t > b["gn"] else 150, n=4)
        if t > b["gn"]:
            callout(ctx, "GREAT NICOBAR", gx + 40, gy + 150, SAFFRON, t - b["gn"], size=40, pin=(gx, gy))
        u = t - b["ghab"]
        if u > 0:
            cx, cy = proj(v, 110.0, 26.5)
            for i in range(3):  # shaking alert triangles over China
                ax = cx - 150 + 150 * i + 6 * math.sin(t * 40 + i)
                k = ease_out_back((u - 0.1 * i) / 0.3)
                if k > 0:
                    ctx.save()
                    ctx.translate(ax, cy + 40)
                    ctx.scale(k, k)
                    ctx.move_to(0, -44)
                    ctx.line_to(42, 30)
                    ctx.line_to(-42, 30)
                    ctx.close_path()
                    rgba(ctx, CN_YELLOW)
                    ctx.fill()
                    text(ctx, "!", 0, 4, 58, (0.1, 0.05, 0.05), font=CAPTION_FONT, bold=False)
                    ctx.restore()
            if t < b["q"]:
                stamp(ctx, 540, 290, u, 0.03, 520, 150, CN_RED, [("CHINA ALERT", 0, 90, CN_YELLOW)])
        u = t - b["q"]
        if u > 0:
            ctx.rectangle(0, 0, W, H)
            rgba(ctx, (0.01, 0.02, 0.03), 0.65 * clamp(u / 0.35))
            ctx.fill()
            self.card(ctx, t, u, t - b["cmt"])

    @staticmethod
    def card(ctx, t, u, uc):
        pop = ease_out_back(u / 0.35)
        ctx.save()
        ctx.translate(540, 600)
        ctx.scale(pop, pop)
        rrect(ctx, -460, -300, 920, 600, 30)
        rgba(ctx, (0.01, 0.04, 0.06), 0.95)
        ctx.fill_preserve()
        rgba(ctx, SONAR)
        ctx.set_line_width(4)
        ctx.stroke()
        text(ctx, "// AAPKI RAAY", -400, -250, 30, SONAR, font=MONO, anchor="l")
        text(ctx, "YEH BASE", 0, -160, 90, (1, 1, 1), font=CAPTION_FONT, bold=False)
        text(ctx, "AUR MAZBOOT?", 0, -60, 90, SAFFRON, font=CAPTION_FONT, bold=False)
        for k, (opt, c, sx) in enumerate((("HAAN", INDIA_GREEN, -215), ("NAHI", RED, 215))):
            ku = ease_out_back((u - 0.3 - 0.15 * k) / 0.3)
            if ku <= 0:
                continue
            hl = 0.5 + 0.5 * math.sin(t * 5 + k * math.pi)
            ctx.save()
            ctx.translate(sx, 140)
            ctx.scale(ku, ku)
            rrect(ctx, -190, -100, 380, 200, 24)
            rgba(ctx, c, 0.15 + 0.2 * hl)
            ctx.fill_preserve()
            rgba(ctx, c)
            ctx.set_line_width(5)
            ctx.stroke()
            text(ctx, opt, 0, 0, 96, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=6)
            ctx.restore()
        ctx.restore()
        if uc > 0:  # arrow sweeps toward the comment button on the right rail
            k = ease_out_cubic(uc / 0.5)
            p0, p1, p2 = (700, 930), (980, 980), (1000, 1300)
            pts = [(lerp(lerp(p0[0], p1[0], s), lerp(p1[0], p2[0], s), s),
                    lerp(lerp(p0[1], p1[1], s), lerp(p1[1], p2[1], s), s)) for s in np.linspace(0, k, 24)]
            line(ctx, pts, (0, 0, 0), 20, 0.6)
            line(ctx, pts, GOLD, 12)
            (ax, ay), (bx, by) = pts[-2], pts[-1]
            ang = math.atan2(by - ay, bx - ax)
            ctx.move_to(bx + 34 * math.cos(ang), by + 34 * math.sin(ang))
            for da in (2.3, -2.3):
                ctx.line_to(bx + 30 * math.cos(ang + da), by + 30 * math.sin(ang + da))
            ctx.close_path()
            rgba(ctx, GOLD)
            ctx.fill()
            b = ease_out_back(uc / 0.3)
            ctx.save()
            ctx.translate(560, 980)
            ctx.scale(b, b)
            rrect(ctx, -220, -48, 440, 96, 48)
            rgba(ctx, GOLD)
            ctx.fill()
            text(ctx, "COMMENT KARO", 0, 2, 54, (0.05, 0.05, 0.05), font=CAPTION_FONT, bold=False)
            ctx.restore()


SCENE_CLASSES = {"oil": Oil, "dilemma": Dilemma, "build": Build, "ask": Ask}


# ============================================================ compositor ("naval brief")

def header(ctx, idx, tl, dur, view):
    ex, ey = 86, 102
    ctx.arc(ex, ey, 24, 0, math.tau)
    rgba(ctx, SONAR)
    ctx.set_line_width(3)
    ctx.stroke()
    line(ctx, [(ex - 30, ey), (ex + 30, ey)], SONAR, 2, 0.7)
    line(ctx, [(ex, ey - 30), (ex, ey + 30)], SONAR, 2, 0.7)
    sweep = tl * 2.2
    line(ctx, [(ex, ey), (ex + 24 * math.cos(sweep), ey + 24 * math.sin(sweep))], (1, 1, 1), 3)
    text(ctx, "REALITY SHIFT", 128, 90, 34, (1, 1, 1), a=0.92, anchor="l")
    text(ctx, "NAVAL BRIEF // MALACCA", 128, 124, 22, SONAR, font=MONO, a=0.8, anchor="l")
    lon, lat = view[0], view[1]
    text(ctx, f"{abs(lat):05.2f}°{'N' if lat >= 0 else 'S'}  {lon:06.2f}°E", W - 60, 90, 28, (1, 1, 1),
         font=MONO, a=0.85, anchor="r")
    x0, x1, gap = W - 330, W - 60, 8
    seg = (x1 - x0 - gap * (len(SPEC) - 1)) / len(SPEC)
    for i in range(len(SPEC)):
        x = x0 + i * (seg + gap)
        ctx.rectangle(x, 118, seg, 8)
        rgba(ctx, (1, 1, 1), 0.18)
        ctx.fill()
        fill = 1.0 if i < idx else (clamp(tl / dur) if i == idx else 0.0)
        if fill:
            ctx.rectangle(x, 118, seg * fill, 8)
            rgba(ctx, SPEC[idx]["accent"])
            ctx.fill()


def caption(ctx, sc, tl, accent):
    """Pop-in caption: the current Hinglish chunk rises into place, hot words coloured, underline grows."""
    cur = None
    for i, (start, _) in enumerate(sc["captions"]):
        if tl >= start - 0.03:
            cur = i
    if cur is None:
        return
    start, cap = sc["captions"][cur]
    u = tl - start + 0.03
    k = ease_out_back(clamp(u / 0.2))
    size = 84
    words_ = cap.split(" ")
    ws = [text_width(ctx, w, size, font=CAPTION_FONT, bold=False) for w in words_]
    gap = size * 0.26
    tw = sum(ws) + gap * (len(ws) - 1)
    fit = min(1.0, 940 / tw)
    cy = (CAP_TOP + CAP_BOTTOM) / 2
    ctx.save()
    ctx.translate(W / 2, cy + 22 * (1 - ease_out_cubic(clamp(u / 0.2))))
    ctx.scale(fit * (0.85 + 0.15 * k), fit * (0.85 + 0.15 * k))
    x = -tw / 2
    a = clamp(u / 0.1)
    for w, ww in zip(words_, ws):
        c = HOT.get(w.strip(PUNCT + "."), (1, 1, 1))
        text(ctx, w, x, 0, size, c, font=CAPTION_FONT, bold=False, a=a, anchor="l", stroke=(0, 0, 0), stroke_w=10)
        x += ww + gap
    bar = tw * ease_out_cubic(clamp((u - 0.05) / 0.3))
    rrect(ctx, -bar / 2, size * 0.55, bar, 8, 4)
    rgba(ctx, accent, a)
    ctx.fill()
    ctx.restore()


def iris(ctx, tl, accent):
    """Sonar iris: the new scene opens from a circle growing out of the map centre."""
    u = ease_out_cubic(tl / 0.38)
    if u >= 1:
        return
    r = 1250 * u
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    ctx.rectangle(0, 0, W, H)
    ctx.arc(W / 2, MAP_CY, r, 0, math.tau)
    rgba(ctx, (0, 0, 0))
    ctx.fill()
    ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    ctx.arc(W / 2, MAP_CY, r, 0, math.tau)
    rgba(ctx, accent, 0.9 * (1 - u))
    ctx.set_line_width(10)
    ctx.stroke()


def compose(idx, tl):
    sc = engine.SCENES[idx]
    spec = SPEC[idx]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    zoom = 1.0 + 0.03 * tl / sc["dur"]
    ctx.save()
    ctx.translate(W / 2 + 10 * math.sin(tl * 0.6 + idx), MAP_CY)
    ctx.scale(zoom, zoom)
    ctx.translate(-W / 2, -MAP_CY)
    sc["obj"].draw(ctx, tl, sc["dur"])
    ctx.restore()
    vignette(ctx)
    g = cairo.LinearGradient(0, 0, 0, 200)  # header plate
    g.add_color_stop_rgba(0, 0.0, 0.01, 0.02, 0.9)
    g.add_color_stop_rgba(1, 0.0, 0.01, 0.02, 0.0)
    ctx.rectangle(0, 0, W, 200)
    ctx.set_source(g)
    ctx.fill()
    g = cairo.LinearGradient(0, CAP_TOP - 90, 0, UI_CLEAR)  # caption bed fading into the clean bottom 400px
    g.add_color_stop_rgba(0, 0.0, 0.01, 0.02, 0.0)
    g.add_color_stop_rgba(0.35, 0.0, 0.01, 0.02, 0.7)
    g.add_color_stop_rgba(1, 0.0, 0.01, 0.02, 0.95)
    ctx.rectangle(0, CAP_TOP - 90, W, UI_CLEAR - CAP_TOP + 90)
    ctx.set_source(g)
    ctx.fill()
    ctx.rectangle(0, UI_CLEAR, W, H - UI_CLEAR)
    rgba(ctx, (0.0, 0.01, 0.02), 0.95)
    ctx.fill()
    header(ctx, idx, tl, sc["dur"], getattr(sc["obj"], "view", WIDE))
    caption(ctx, sc, tl, spec["accent"])
    if idx:
        iris(ctx, tl, spec["accent"])
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
        "China Ka Malacca Trap: Bharat Ka Masterstroke! 🇮🇳",
        "Malacca Dilemma: China Ka Sabse Bada Dar",
        "China Ka 80% Tel Ek Raaste Se, Chaabi Bharat Ke Paas",
        "Great Nicobar: China Kyun Ghabrata Hai?",
        "INS Baaz: Malacca Ke Muhane Par Bharat",
        "₹72,000 Crore Ka Great Nicobar Plan Kya Hai?",
        "Malacca Strait Band Hua Toh China Ka Kya Hoga?",
        "Bharat Ke Paas Hai China Ke Tel Ki Chaabi",
        "Malacca Dilemma Explained in 45 Seconds",
        "Great Nicobar Port: Bharat Ka Naval Masterplan",
    ],
    "thumb_text": "80% OIL BLOCK?",
    "queries": ["malacca dilemma", "great nicobar", "ins baaz"],
    "description": """
Malacca Dilemma: China ka lagbhag 80% kachcha tel ek hi raaste, Malacca Strait, se hokar aata hai.
Aur is raaste ke muhane par baitha hai Bharat ka Great Nicobar, jahan Indian Navy ka air station INS Baaz hai.

Is Short me:
• "Malacca Dilemma" kya hai aur China ise apna sabse bada dar kyun maanta hai
• Great Nicobar ka dakshini sira (Indira Point) Sumatra se ~150 KM, Six Degree Channel ke paar
• INS Baaz: Campbell Bay, Great Nicobar ka naval air station (2012 se)
• ~₹72,000 crore ka Great Nicobar project: transshipment port (Galathea Bay), airport, township

Aapki raay: kya Bharat ko yeh base aur mazboot karna chahiye? HAAN ya NAHI, comment me likho.
Aisi aur geopolitics ke liye Reality Shift ko subscribe karo.

Note: video ka map schematic hai, scale pe nahi. 80% ek aam taur pe quote kiya jaane wala anumaan hai.
""",
    "tags": ["malacca dilemma", "malacca strait", "great nicobar", "great nicobar project", "ins baaz",
             "india vs china", "indian navy", "andaman nicobar", "six degree channel", "geopolitics hindi",
             "indian defence shorts", "india china oil", "bharat news shorts", "world affairs hindi", "reality shift"],
    "hashtags": ["#Shorts", "#MalaccaDilemma", "#IndianNavy"],
}


def thumbnail(ctx):
    """1080x1920 cover: 80% OIL / BLOCK? over the Malacca map, the route red with a lock at the strait."""
    v = (98.0, 13.5, 62)
    ctx.save()
    draw_map(ctx, v, 0.0, {"china": (CN_RED, 0.6), "india": (SAFFRON, 0.8)})
    pts = [proj(v, *p) for p in ROUTE]
    line(ctx, pts, (0, 0, 0), 18, 0.6)
    line(ctx, pts, RED, 10)
    for k in range(12):
        tanker(ctx, *along(pts, 0.35 + k * 0.03), 1.3)
    mx, my = proj(v, *MALACCA)
    glow(ctx, mx, my, 220, RED, 0.6)
    rrect(ctx, mx - 50, my - 20, 100, 80, 12)  # padlock on the strait
    rgba(ctx, CN_YELLOW)
    ctx.fill()
    ctx.arc(mx, my - 20, 32, math.pi, 2 * math.pi)
    rgba(ctx, CN_YELLOW)
    ctx.set_line_width(14)
    ctx.stroke()
    circle(ctx, mx, my + 18, 10, (0.1, 0.05, 0.05))
    ping(ctx, *proj(v, *GN), 0.3, SAFFRON, 200)
    ctx.restore()
    g = cairo.LinearGradient(0, 0, 0, 900)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.95)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 900)
    ctx.set_source(g)
    ctx.fill()
    vignette(ctx)
    glow(ctx, 540, 500, 600, CN_YELLOW, 0.2)
    text(ctx, "80% OIL", 540, 380, 250, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "BLOCK?", 540, 650, 280, CN_YELLOW, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=24)
    text(ctx, "REALITY SHIFT", 540, 1780, 40, (1, 1, 1), a=0.7)


def main() -> None:
    import upload_kit
    story = importlib.import_module("generate_malacca_short")  # a named module, so work files land in work/<name>/
    engine.make_frame = story.make_frame
    final = engine.render(story, "edge")
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
