"""Reality Shift Short — Chabahar Port vs CPEC (~32s, pure Devanagari edge-tts voiceover).

Usage:
  python generate_chabahar_short.py

engine.render() does the narration (hi-IN-MadhurNeural, +10%), audio-first timing (each scene lasts
its trimmed narration + 0.08s), music/SFX mix and the 1080x1920 / 30fps / libx264 + aac encode.
This module swaps in its own compositor for the Golden Safe Zone layout:
  - "• REALITY SHIFT •" watermark top-centre, subtle grey
  - each scene's on-screen text in a high-contrast badge clipped to Y 1150-1250
  - bottom 400px faded to a clean dark band for the YouTube UI
and ends on a subscribe CTA scene.
Output: render_chabahar/chabahar_port_bypass_short.mp4 (+ a .json with the scene/word alignment).
"""

import importlib
import json
import math

import cairo
import numpy as np

import engine
from engine import *  # noqa: F401,F403
from stories.reality_shift import GOLD, INDIA_GREEN, SAFFRON, FACE, _ellipse, flag, stamp, subscribe_badge

TOPIC = "CHABAHAR VS CPEC"
OUTPUT_DIR = ROOT / "render_chabahar"
OUTPUTS = {"edge": "chabahar_port_bypass_short.mp4"}

CLEAN_PUNCTUATION = False      # keep ? ! … so the voice phrases the Devanagari naturally
MAX_GAP = 0.3
TAIL_PAD = 0.08                # scene length = audio duration + 0.08s
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 112
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"

RED = hexc("#FF3B3B")
NEON = hexc("#2BFF88")
STEEL = hexc("#8C96A6")

SPEC = [
    {"key": "hook", "window": "0:00-0:05", "icon": "siren", "accent": RED,
     "vo": "क्या आपको पता है? चीन का बासठ बिलियन डॉलर का ग्वादर प्रोजेक्ट भारत के सिर्फ एक मूव से फेल हो गया!",
     "text": "CPEC FAIL?",
     "visual": "Arabian Sea map zoom, Gwadar red cross ($62B CPEC), Chabahar green glowing flag"},
    {"key": "blocked", "window": "0:05-0:13", "icon": None, "accent": RED,
     "vo": "पाकिस्तान सालों से सोच रहा था कि वो भारत का ज़मीनी रास्ता रोककर हमें सेंट्रल एशिया जाने से रोक लेगा।",
     "text": "NO LAND ROUTE NEEDED",
     "visual": "Pakistan border fence + red BLOCKED stamp -> Indian cargo ships sailing freely"},
    {"key": "corridor", "window": "0:13-0:24", "icon": "flag", "accent": NEON,
     "vo": "लेकिन भारत ने ईरान के चाबहार पोर्ट का दस साल का कंट्रोल लेकर पूरा खेल ही पलट दिया। अब बिना पाकिस्तान "
           "की ज़मीन को छुए, भारतीय सामान सीधा अफगानिस्तान, रूस और यूरोप पहुंचेगा।",
     "text": "INSTC CORRIDOR ACTIVE",
     "visual": "Route Mumbai -> Chabahar (Iran) -> Afghanistan -> Russia -> Europe via INSTC"},
    {"key": "masterstroke", "window": "0:24-0:32", "icon": "bolt", "accent": GOLD,
     "vo": "चीन और पाकिस्तान के अरबों डॉलर बर्बाद करके भारत ने ये साबित कर दिया कि नया भारत अब किसी के रोके "
           "नहीं रुकता!",
     "text": "MASTERSTROKE",
     "visual": "Split screen Xi Jinping / Shehbaz Sharif stressed, golden bolt down the split"},
    {"key": "cta", "window": "end", "icon": "bell", "accent": hexc("#FF0000"),
     "vo": "ऐसी ही और ज़बरदस्त खबरों के लिए रियलिटी शिफ्ट को अभी सब्सक्राइब करें!",
     "text": "SUBSCRIBE NOW",
     "visual": "Tricolor sunburst, ringing bell, Reality Shift subscribe button clicked by a cursor"},
]

NARRATION = {s["key"]: s["vo"] for s in SPEC}
# one chunk per word: engine.align() then hands every scene a per-word timeline to cue its beats from
SCRIPT = [(s["key"], [(w, w) for w in s["vo"].split()]) for s in SPEC]

BADGE_TOP, BADGE_BOTTOM = 1150, 1250
UI_CLEAR = H - 400             # nothing below this line but the dark band
MAP_CY = 640


class Cued:
    """cue(word) is the start of the first narrated word containing it (fallback: default)."""

    def cue(self, key, default):
        for s in engine.SCENES:
            if s["obj"] is self:
                return next((st for st, cap in s["captions"] if key in cap), default)
        return default


# ============================================================ map

LAND = [
    (32.5, 29.9), (34.9, 29.5), (35.0, 28.0), (36.6, 25.9), (37.5, 24.2), (39.1, 21.5), (40.5, 19.2), (41.5, 17.5),
    (42.8, 14.5), (43.4, 12.7), (45.0, 12.8), (47.5, 13.6), (49.0, 14.5), (52.2, 15.6), (54.0, 16.9), (55.4, 17.8),
    (56.8, 18.6), (57.8, 19.0), (58.5, 20.5), (59.8, 22.5), (58.6, 23.6), (57.2, 23.9), (56.4, 24.9), (56.3, 26.3),
    (55.5, 25.4), (54.5, 24.3), (52.0, 24.0), (51.6, 24.6), (51.6, 25.9), (51.0, 26.0), (50.8, 24.8), (50.1, 26.5),
    (49.5, 27.2), (48.5, 28.4), (47.9, 29.9), (48.8, 30.4), (50.3, 30.0), (51.4, 27.9), (53.5, 26.8), (55.4, 26.7),
    (56.3, 27.2), (57.3, 25.9), (58.8, 25.5), (59.8, 25.4), (60.4, 25.3), (60.64, 25.29), (61.0, 25.2), (61.6, 25.15),
    (62.33, 25.13), (63.5, 25.25), (64.6, 25.2), (65.7, 25.35), (66.6, 25.45), (67.0, 24.85), (67.3, 24.2),
    (67.6, 23.8), (68.2, 23.7), (68.8, 23.2), (70.0, 22.9), (69.1, 22.4), (69.6, 21.8), (70.6, 20.9), (71.6, 21.0),
    (72.2, 21.6), (72.6, 21.4), (72.8, 20.4), (72.9, 19.0), (73.1, 18.0), (73.3, 17.0), (73.8, 15.5), (74.4, 14.3),
    (74.8, 12.9), (75.4, 11.8), (75.9, 11.0), (76.3, 9.9), (76.9, 8.6), (77.5, 8.1), (78.2, 8.9), (79.0, 9.3),
    (79.9, 10.3), (79.8, 11.9), (80.3, 13.1), (80.2, 15.5), (81.3, 16.3), (82.3, 16.6), (84.0, 18.3), (85.8, 19.8),
    (87.0, 21.0), (88.2, 21.8), (90.0, 22.0), (92.0, 21.5), (94.0, 18.0), (98.0, 16.0), (110, 10), (110, 72),
    (15, 72), (15, 38.5), (19.5, 40.0), (21.0, 38.0), (23.0, 36.5), (24.0, 38.0), (26.5, 40.1), (27.0, 38.4),
    (27.5, 37.0), (28.5, 36.6), (30.6, 36.8), (32.8, 36.1), (34.6, 36.8), (36.2, 36.6), (35.9, 35.4), (35.5, 34.0),
    (34.9, 32.6), (34.3, 31.3), (32.5, 31.2), (30.4, 31.5), (28.0, 31.1), (25.0, 31.6), (20.0, 30.8), (15, 32.0),
    (15, -5), (40, -5), (42, -0.5), (44.5, 1.8), (47.5, 4.6), (49.5, 8.0), (51.2, 11.8), (49.0, 11.3), (45.0, 10.4),
    (43.2, 11.5), (42.5, 13.0), (41.0, 14.8), (39.5, 15.5), (38.5, 17.8), (37.3, 18.8), (36.5, 22.0), (35.6, 23.5),
    (34.6, 25.8), (33.5, 27.5), (32.6, 29.4),
]
CASPIAN = [
    (46.9, 44.8), (47.6, 43.0), (48.6, 41.8), (49.6, 40.4), (48.9, 38.5), (49.2, 37.6), (50.4, 37.1), (51.8, 36.7),
    (53.9, 36.9), (54.0, 37.8), (53.1, 39.4), (53.4, 40.6), (52.8, 41.9), (52.6, 42.8), (51.4, 43.2), (50.8, 44.6),
    (51.4, 45.3), (53.0, 45.3), (53.2, 46.7), (51.2, 47.1), (49.2, 46.4), (47.4, 45.6),
]
BLACK_SEA = [
    (27.6, 42.0), (28.0, 43.4), (28.7, 44.4), (29.7, 45.2), (30.7, 46.5), (31.8, 46.6), (33.6, 46.1), (32.6, 45.4),
    (33.5, 44.5), (35.2, 44.9), (36.5, 45.3), (38.2, 46.9), (39.3, 47.2), (37.7, 45.0), (39.7, 43.9), (41.6, 42.0),
    (41.5, 41.4), (38.5, 40.9), (36.0, 41.7), (34.0, 42.0), (31.4, 41.2), (29.1, 41.2), (28.0, 41.6),
]
PAKISTAN = [
    (61.6, 25.15), (62.33, 25.13), (63.5, 25.25), (64.6, 25.2), (65.7, 25.35), (66.6, 25.45), (67.0, 24.85),
    (67.3, 24.2), (67.6, 23.8), (68.2, 23.7), (69.6, 24.3), (71.1, 24.4), (70.6, 25.7), (70.1, 26.6), (71.9, 27.9),
    (73.4, 29.9), (74.6, 31.0), (75.3, 32.3), (74.0, 33.0), (73.5, 33.6), (73.0, 34.3), (72.6, 35.5), (71.6, 36.2),
    (71.2, 35.5), (71.1, 34.4), (69.9, 34.0), (70.3, 33.3), (69.3, 31.9), (68.5, 31.7), (66.7, 31.2), (66.3, 29.9),
    (64.5, 29.6), (62.5, 29.4), (60.9, 29.8), (61.8, 28.6), (62.8, 28.2), (62.8, 27.3), (63.3, 26.7), (61.8, 26.2),
]
BORDERS = [
    [(60.9, 29.8), (61.0, 31.4), (60.6, 33.5), (61.2, 35.6)],                                    # Iran-Afghanistan
    [(61.2, 35.6), (62.5, 35.3), (64.5, 36.3), (66.5, 37.4), (68.0, 37.1), (70.0, 37.6), (71.5, 37.9),
     (73.5, 37.4), (74.9, 37.2)],                                                                # Afghanistan north
    [(61.2, 35.6), (60.4, 36.6), (57.3, 38.2), (54.0, 37.4)],                                    # Iran north-east
    [(48.0, 30.0), (47.6, 31.0), (47.7, 32.5), (46.1, 33.0), (45.4, 33.9), (45.9, 35.0), (45.0, 36.8),
     (44.3, 39.4)],                                                                              # Iran-Iraq/Turkey
]
COUNTRY_LABELS = (("IRAN", 58.6, 27.4), ("PAKISTAN", 64.3, 27.0), ("AFGHANISTAN", 65.6, 33.4), ("INDIA", 77.0, 22.0),
                  ("ARABIAN SEA", 63.0, 23.6), ("OMAN", 56.8, 21.0), ("RUSSIA", 44.0, 52.5), ("CHINA", 82.0, 37.0))
CITIES = {"MUMBAI": (72.88, 19.08), "CHABAHAR": (60.64, 25.29), "GWADAR": (62.33, 25.13), "KABUL": (69.18, 34.53),
          "TEHRAN": (51.39, 35.69), "MOSCOW": (37.62, 55.75), "KASHGAR": (75.99, 39.47), "EUROPE": (23.0, 52.2)}

CPEC = [CITIES["KASHGAR"], (74.3, 36.8), (73.05, 33.7), (71.5, 30.2), (68.4, 27.0), (65.5, 26.3), CITIES["GWADAR"]]
SEA_LEG = [CITIES["MUMBAI"], (70.5, 19.6), (66.5, 22.6), (63.0, 24.5), CITIES["CHABAHAR"]]
AFG_LEG = [CITIES["CHABAHAR"], (60.9, 27.2), (60.86, 29.5), (61.9, 31.0), (63.4, 32.2), (65.7, 31.6), (68.0, 33.2),
           CITIES["KABUL"]]
RU_LEG = [CITIES["CHABAHAR"], (58.4, 29.1), (55.5, 32.6), CITIES["TEHRAN"], (49.5, 37.47), (50.0, 40.5), (48.6, 43.5),
          (48.03, 46.35), (44.5, 48.7), (40.0, 52.0), CITIES["MOSCOW"]]
EU_LEG = [CITIES["MOSCOW"], (30.5, 54.0), CITIES["EUROPE"]]


def proj(v, lon, lat):
    """Equirectangular projection for view v = (centre lon, centre lat, px per degree)."""
    lon0, lat0, s = v
    return W / 2 + (lon - lon0) * s * 0.9, MAP_CY - (lat - lat0) * s


def view_at(keys, t):
    """Eased camera between (time, view) keyframes; zoom interpolates geometrically."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, a), (t1, b) in zip(keys, keys[1:]):
        if t < t1:
            u = ease_in_out((t - t0) / max(t1 - t0, 1e-3))
            return lerp(a[0], b[0], u), lerp(a[1], b[1], u), math.exp(lerp(math.log(a[2]), math.log(b[2]), u))
    return keys[-1][1]


def poly(ctx, v, pts):
    ctx.move_to(*proj(v, *pts[0]))
    for p in pts[1:]:
        ctx.line_to(*proj(v, *p))
    ctx.close_path()


def draw_map(ctx, v, t, pak=0.0):
    """Dark tactical map: ocean grid, land, coastline glow, borders, Pakistan tint (pak = 0..1)."""
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc("#06182B"))
    g.add_color_stop_rgb(1, *hexc("#01060D"))
    ctx.set_source(g)
    ctx.paint()
    lon0, lat0, s = v
    step = 5 if s < 90 else 1
    for k in range(-40, 41):  # graticule
        lon = round(lon0 / step) * step + k * step
        x = proj(v, lon, lat0)[0]
        if -10 < x < W + 10:
            line(ctx, [(x, 0), (x, H)], hexc("#2E8BC0"), 1, 0.12)
        lat = round(lat0 / step) * step + k * step
        y = proj(v, lon0, lat)[1]
        if -10 < y < H + 10:
            line(ctx, [(0, y), (W, y)], hexc("#2E8BC0"), 1, 0.12)
    poly(ctx, v, LAND)
    rgba(ctx, hexc("#152133"))
    ctx.fill()
    for sea in (CASPIAN, BLACK_SEA):
        poly(ctx, v, sea)
        rgba(ctx, hexc("#06182B"))
        ctx.fill()
    if pak > 0:
        poly(ctx, v, PAKISTAN)
        rgba(ctx, RED, 0.28 * pak)
        ctx.fill()
        ctx.save()
        poly(ctx, v, PAKISTAN)
        ctx.clip()
        for k in range(-30, 30):  # warning hatch
            x = k * 38 + (t * 30) % 38
            line(ctx, [(x, 0), (x + H, H)], RED, 5, 0.22 * pak)
        ctx.restore()
    for shape in (LAND, CASPIAN, BLACK_SEA):
        poly(ctx, v, shape)
        rgba(ctx, hexc("#4CC3FF"), 0.18)
        ctx.set_line_width(9)
        ctx.stroke_preserve()
        rgba(ctx, hexc("#4CC3FF"), 0.75)
        ctx.set_line_width(2.5)
        ctx.stroke()
    ctx.set_dash([10, 8])
    for b in BORDERS + [PAKISTAN[9:]]:
        line(ctx, [proj(v, *p) for p in b], STEEL, 2, 0.45)
    ctx.set_dash([])
    if pak > 0:
        poly(ctx, v, PAKISTAN)
        rgba(ctx, RED, 0.9 * pak)
        ctx.set_line_width(4)
        ctx.stroke()
    for name, lon, lat in COUNTRY_LABELS:
        x, y = proj(v, lon, lat)
        if -200 < x < W + 200 and 0 < y < UI_CLEAR:
            col = RED if (name == "PAKISTAN" and pak > 0) else (0.8, 0.86, 0.95)
            text(ctx, name, x, y, 30, col, a=0.5 + 0.4 * (pak if name == "PAKISTAN" else 0))


def partial(pts, u):
    """Polyline pts cut at fraction u of its length; returns (points, head)."""
    lens = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    target = clamp(u) * sum(lens)
    out = [pts[0]]
    for (a, b), ln in zip(zip(pts, pts[1:]), lens):
        if target <= ln:
            k = target / ln if ln else 0
            out.append((lerp(a[0], b[0], k), lerp(a[1], b[1], k)))
            return out, out[-1]
        out.append(b)
        target -= ln
    return out, out[-1]


def route(ctx, v, lonlat, u, c, t, w=7, a=1.0):
    """Glowing route drawn on to fraction u with flowing dashes; returns the head position."""
    if u <= 0:
        return None
    pts, head = partial([proj(v, *p) for p in lonlat], u)
    line(ctx, pts, c, w * 3.2, 0.22 * a)
    line(ctx, pts, c, w, 0.95 * a)
    ctx.set_dash([18, 22], -t * 90)
    line(ctx, pts, (1, 1, 1), w * 0.45, 0.75 * a)
    ctx.set_dash([])
    if u < 1:
        glow(ctx, *head, 40, c, 0.9 * a)
        circle(ctx, *head, 8, (1, 1, 1), a)
    return head


def plate(ctx, s, x, y, c, u=1.0, size=40, sub=None):
    """Name plate centred on (x, y) that pops in over u seconds."""
    if u <= 0:
        return
    pop = ease_out_back(u / 0.3)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(pop, pop)
    w = max(text_width(ctx, s, size, font=CAPTION_FONT, bold=False),
            text_width(ctx, sub, size * 0.7, font=CAPTION_FONT, bold=False) if sub else 0) + 44
    h = size * (2.2 if sub else 1.4)
    rrect(ctx, -w / 2, -size * 0.7, w, h, 12)
    rgba(ctx, (0.02, 0.02, 0.04), 0.86)
    ctx.fill_preserve()
    rgba(ctx, c)
    ctx.set_line_width(4)
    ctx.stroke()
    text(ctx, s, 0, 0, size, (1, 1, 1), font=CAPTION_FONT, bold=False)
    if sub:
        text(ctx, sub, 0, size * 0.95, size * 0.7, c, font=CAPTION_FONT, bold=False)
    ctx.restore()


def pin(ctx, x, y, c, u, t):
    if u <= 0:
        return
    pop = ease_out_back(u / 0.3)
    r = ((t * 0.9) % 1.0)
    ctx.arc(x, y, 14 + 60 * r, 0, math.tau)
    rgba(ctx, c, 0.6 * (1 - r))
    ctx.set_line_width(4)
    ctx.stroke()
    glow(ctx, x, y, 46 * pop, c, 0.8)
    circle(ctx, x, y, 11 * pop, (1, 1, 1))


def green_flag(ctx, x, y, u, t):
    """Chabahar marker: tricolor on a pole, rising out of a pulsing neon-green glow."""
    if u <= 0:
        return
    rise = ease_out_back(u / 0.45)
    p = 1 + 0.15 * math.sin(t * 6)
    glow(ctx, x, y - 70, 190 * p * min(1.0, rise), NEON, 0.55)
    glow(ctx, x, y, 70 * p, NEON, 0.9)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(rise, rise)
    flag(ctx, 4, -160, 116, 78, "in", t, pole=160)
    ctx.restore()
    circle(ctx, x, y, 10, (1, 1, 1))


def red_cross(ctx, x, y, u, size=95):
    if u <= 0:
        return
    k = lerp(2.4, 1.0, ease_out_cubic(u / 0.18))
    glow(ctx, x, y, size * 2.2, RED, 0.6 * clamp(u / 0.1))
    for sx in (-1, 1):
        line(ctx, [(x - size * k, y - sx * size * k), (x + size * k, y + sx * size * k)], (0, 0, 0), 40)
        line(ctx, [(x - size * k, y - sx * size * k), (x + size * k, y + sx * size * k)], RED, 28)


def no_entry(ctx, x, y, r, u):
    if u <= 0:
        return
    pop = ease_out_back(u / 0.3)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(pop, pop)
    circle(ctx, 0, 0, r, RED)
    ctx.arc(0, 0, r, 0, math.tau)
    rgba(ctx, (1, 1, 1))
    ctx.set_line_width(6)
    ctx.stroke()
    rrect(ctx, -r * 0.65, -r * 0.16, r * 1.3, r * 0.32, 4)
    rgba(ctx, (1, 1, 1))
    ctx.fill()
    ctx.restore()


# ============================================================ props

def truck_rear(ctx, x, y, s, brake):
    """Container truck seen from behind, (x, y) at the road under the rear wheels."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for wx in (-125, 85):
        rrect(ctx, wx, -46, 42, 56, 10)
        rgba(ctx, hexc("#0C0C0E"))
        ctx.fill()
    ctx.rectangle(-150, -70, 300, 30)
    rgba(ctx, hexc("#2A2C31"))
    ctx.fill()
    rrect(ctx, -165, -300, 330, 236, 8)
    rgba(ctx, hexc("#D8D2C4"))
    ctx.fill()
    for k in range(1, 6):
        line(ctx, [(-165 + k * 55, -296), (-165 + k * 55, -68)], hexc("#A9A293"), 4)
    for k, c in enumerate((SAFFRON, (1, 1, 1), INDIA_GREEN)):
        ctx.rectangle(-165, -250 + k * 16, 330, 16)
        rgba(ctx, c)
        ctx.fill()
    text(ctx, "BHARAT CARGO", 0, -150, 40, hexc("#1A2340"), font=CAPTION_FONT, bold=False)
    for side in (-1, 1):
        lx = side * 140
        if brake:
            glow(ctx, lx, -82, 70, RED, 0.85)
        rrect(ctx, lx - 16, -92, 32, 20, 4)
        rgba(ctx, RED if brake else shade(RED, 0.5))
        ctx.fill()
    ctx.restore()


def container_ship(ctx, x, y, s, t, seed=0):
    """Side-on container ship, bow to the right, (x, y) on the waterline, flying the tricolor."""
    ctx.save()
    ctx.translate(x, y + 4 * math.sin(t * 1.6 + seed))
    ctx.rotate(0.012 * math.sin(t * 1.2 + seed))
    ctx.scale(s, s)
    colors = (SAFFRON, hexc("#E8E8E8"), INDIA_GREEN, hexc("#2F6FB3"), hexc("#C0392B"))
    for row in range(4):
        for col in range(10):
            cx = -230 + col * 54
            if row == 3 and col in (0, 9):
                continue
            rrect(ctx, cx, -102 - row * 34, 52, 32, 3)
            rgba(ctx, colors[int(rnd(row * 10 + col, seed) * 5)])
            ctx.fill()
    ctx.rectangle(-365, -240, 115, 170)
    rgba(ctx, hexc("#DCE3EA"))
    ctx.fill()
    for k in range(4):
        ctx.rectangle(-355 + k * 26, -228, 18, 12)
    rgba(ctx, hexc("#1A2A44"))
    ctx.fill()
    ctx.rectangle(-325, -282, 40, 42)
    rgba(ctx, SAFFRON)
    ctx.fill()
    line(ctx, [(-395, -70), (-395, -330)], hexc("#C9C9C9"), 6)
    flag(ctx, -393, -330, 84, 56, "in", t, phase=seed)

    def hull():
        ctx.move_to(-410, -70)
        ctx.line_to(330, -70)
        ctx.line_to(410, -112)
        ctx.line_to(372, 22)
        ctx.line_to(-385, 22)
        ctx.line_to(-418, -40)
        ctx.close_path()

    hull()
    rgba(ctx, hexc("#1B2A44"))
    ctx.fill()
    ctx.save()
    hull()
    ctx.clip()
    ctx.rectangle(-500, 0, 1000, 40)
    rgba(ctx, hexc("#8E1B1B"))
    ctx.fill()
    ctx.restore()
    text(ctx, "BHARAT CARGO", 10, -36, 40, (1, 1, 1), font=CAPTION_FONT, bold=False)
    for k in range(5):  # bow wave + wake foam
        f = 0.5 + 0.5 * math.sin(t * 8 + k)
        _ellipse(ctx, 390 - k * 18, 14 + k * 3, 40 - k * 4, 8)
        rgba(ctx, (1, 1, 1), 0.35 + 0.35 * f)
        ctx.fill()
    for k in range(6):
        wx = -420 - k * 90 - (t * 60) % 90
        line(ctx, [(wx, 20 + k * 4), (wx - 70, 22 + k * 5)], (1, 1, 1), 5, 0.5 - k * 0.07)
    ctx.restore()


def bust(ctx, x, y, s, t, suit, tie, hair, k, mood="stressed"):
    """Stylised suited leader bust. mood "stressed": shiver, worried brows, frown, sweat, stress marks;
    "smug": steady, level brows and a grin."""
    ctx.save()
    ctx.translate(x + (0 if mood == "smug" else 3 * math.sin(t * 38 + k)), y)
    ctx.scale(s, s)
    rrect(ctx, -240, 150, 480, 520, 130)
    rgba(ctx, suit)
    ctx.fill()
    ctx.move_to(-70, 150)
    ctx.line_to(70, 150)
    ctx.line_to(0, 330)
    ctx.close_path()
    rgba(ctx, (0.95, 0.95, 0.95))
    ctx.fill()
    ctx.move_to(-18, 165)
    ctx.line_to(18, 165)
    ctx.line_to(26, 310)
    ctx.line_to(0, 340)
    ctx.line_to(-26, 310)
    ctx.close_path()
    rgba(ctx, tie)
    ctx.fill()
    ctx.rectangle(-45, 60, 90, 100)
    rgba(ctx, shade(FACE, 0.85))
    ctx.fill()
    for side in (-1, 1):
        circle(ctx, side * 104, -20, 24, shade(FACE, 0.9))
    _ellipse(ctx, 0, -30, 106, 128)
    rgba(ctx, FACE)
    ctx.fill()
    if k == 0:  # dark, full, combed back
        ctx.arc(0, -52, 110, math.pi * 1.02, math.pi * 1.98)
        ctx.close_path()
        rgba(ctx, hexc("#121214"))
        ctx.fill()
    else:       # receding grey sides
        for side in (-1, 1):
            _ellipse(ctx, side * 92, -70, 30, 58)
            rgba(ctx, hair)
            ctx.fill()
        ctx.arc(0, -70, 100, math.pi * 1.15, math.pi * 1.85)
        rgba(ctx, hair, 0.55)
        ctx.set_line_width(14)
        ctx.stroke()
    smug = mood == "smug"
    for side in (-1, 1):
        _ellipse(ctx, side * 40, -30, 13, 9)
        rgba(ctx, hexc("#1A1210"))
        ctx.fill()
        brow = [(side * 16, -70), (side * 66, -74)] if smug else [(side * 16, -78), (side * 66, -60)]
        line(ctx, brow, hexc("#1A1210"), 9)
    if smug:
        ctx.arc(0, 30, 40, math.pi * 0.2, math.pi * 0.8)                      # grin
    else:
        line(ctx, [(-12, -96), (12, -96)], shade(FACE, 0.75), 4)
        ctx.arc(0, 78, 38, math.pi * 1.2, math.pi * 1.8)                      # frown
    rgba(ctx, hexc("#5A2A22"))
    ctx.set_line_width(8)
    ctx.stroke()
    if smug:
        ctx.restore()
        return
    for d in range(3):  # sweat drops sliding off the temple
        u = (t * 0.8 + d / 3) % 1.0
        sx, sy = (118 if d % 2 else -118), -70 + 220 * u
        ctx.move_to(sx, sy - 22)
        ctx.curve_to(sx + 14, sy, sx + 12, sy + 14, sx, sy + 14)
        ctx.curve_to(sx - 12, sy + 14, sx - 14, sy, sx, sy - 22)
        rgba(ctx, hexc("#8FD3FF"), 0.9 * (1 - u))
        ctx.fill()
    for j in range(3):  # comic stress marks
        a = -2.2 + j * 0.35 + 0.08 * math.sin(t * 12 + j)
        line(ctx, [(170 * math.cos(a), -40 + 170 * math.sin(a)), (215 * math.cos(a), -40 + 215 * math.sin(a))],
             (1, 1, 1), 8, 0.8)
    ctx.restore()


def bolt(ctx, x, y, s, c, a=1.0):
    pts = ((10, -40), (-18, 6), (0, 6), (-10, 40), (20, -8), (2, -8), (12, -40))
    ctx.move_to(x + pts[0][0] * s, y + pts[0][1] * s)
    for px, py in pts[1:]:
        ctx.line_to(x + px * s, y + py * s)
    ctx.close_path()
    rgba(ctx, c, a)
    ctx.fill_preserve()
    rgba(ctx, (0, 0, 0), a)
    ctx.set_line_width(max(2.0, 2 * s))
    ctx.stroke()


def siren(ctx, x, y, t):
    on = int(t * 6) % 2 == 0
    if on:
        glow(ctx, x, y, 60, RED, 0.8)
        for k in range(5):
            a = math.pi * (1.1 + k * 0.2)
            line(ctx, [(x + 34 * math.cos(a), y + 34 * math.sin(a)), (x + 46 * math.cos(a), y + 46 * math.sin(a))],
                 GOLD, 5)
    ctx.arc(x, y + 6, 22, math.pi, 2 * math.pi)
    rgba(ctx, RED if on else shade(RED, 0.7))
    ctx.fill()
    rrect(ctx, x - 28, y + 6, 56, 14, 4)
    rgba(ctx, (0.85, 0.85, 0.88))
    ctx.fill()


# ============================================================ scenes

class Hook(Cued):
    """Arabian Sea map: CPEC line to Gwadar, zoom in, Chabahar green flag, red cross slams on Gwadar."""

    def beats(self, d):
        c = self.cue
        return {"china": c("चीन", d * 0.2), "gwadar": c("ग्वादर", d * 0.45), "india": c("भारत", d * 0.6),
                "fail": c("फेल", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["china"], "beep"), (b["gwadar"], "whoosh"), (b["india"], "zap"),
                (b["fail"], "thud"), (b["fail"] + 0.03, "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        v = view_at([(0.0, (67.0, 30.5, 30)), (b["gwadar"] + 0.7, (61.5, 25.4, 150))], t)
        draw_map(ctx, v, t)
        failed = t >= b["fail"]
        flicker = 0.35 + 0.25 * math.sin(t * 30) if failed else 1.0
        route(ctx, v, CPEC, ease_in_out((t - b["china"]) / 1.1), RED, t, w=6, a=flicker)
        u = t - b["china"] - 0.4
        if u > 0 and v[2] < 70:
            mx, my = proj(v, 71.5, 31.5)
            ctx.save()
            ctx.translate(mx - 180, my)
            plate(ctx, "CPEC", 0, 0, RED, u, size=44, sub="$62 BILLION")
            ctx.restore()
        gx, gy = proj(v, *CITIES["GWADAR"])
        cx, cy = proj(v, *CITIES["CHABAHAR"])
        pin(ctx, gx, gy, RED, t - b["gwadar"], t)
        green_flag(ctx, cx, cy, t - b["india"], t)
        plate(ctx, "GWADAR", gx + 70, gy + 130, RED, t - b["gwadar"] - 0.2, size=46, sub="$62B CPEC")
        plate(ctx, "CHABAHAR", cx - 30, cy - 240, NEON, t - b["india"] - 0.15, size=46, sub="IRAN · INDIA")
        u = t - b["fail"]
        red_cross(ctx, gx, gy, u)
        if 0 <= u < 0.3:
            rgba(ctx, RED, 0.3 * (1 - u / 0.3))
            ctx.paint()


class Blocked(Cued):
    """Pakistan border fence, truck halts, BLOCKED stamp -> diagonal wipe to Indian cargo ships at sea."""

    def beats(self, d):
        c = self.cue
        return {"stamp": c("रोककर", d * 0.42), "swap": c("सेंट्रल", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (1.4, "soft_thud"), (b["stamp"], "boom"), (b["stamp"] + 0.02, "thud"),
                (b["swap"] - 0.1, "whoosh"), (b["swap"] + 0.5, "dingdong")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        u = (t - b["swap"]) / 0.4
        if u > 0:
            self.ships(ctx, t - b["swap"], t)
        if u < 1:
            ctx.save()
            if u > 0:  # diagonal wipe: fence survives left of the sweeping edge
                ex = lerp(W + 400, -400, ease_in_out(u))
                ctx.move_to(-10, -10)
                ctx.line_to(ex + 300, -10)
                ctx.line_to(ex - 300, H + 10)
                ctx.line_to(-10, H + 10)
                ctx.close_path()
                ctx.clip()
            self.fence(ctx, t, b["stamp"])
            ctx.restore()
            if u > 0:
                ex = lerp(W + 400, -400, ease_in_out(u))
                line(ctx, [(ex + 300, -10), (ex - 300, H + 10)], GOLD, 18, 0.9)
                line(ctx, [(ex + 300, -10), (ex - 300, H + 10)], (1, 1, 1), 6)

    def fence(self, ctx, t, st):
        su = t - st
        if 0 < su < 0.35:  # impact shake
            ctx.translate(16 * (1 - su / 0.35) * math.sin(su * 90), 10 * (1 - su / 0.35) * math.cos(su * 70))
        g = cairo.LinearGradient(0, 0, 0, 880)
        g.add_color_stop_rgb(0, *hexc("#1E0A0C"))
        g.add_color_stop_rgb(1, *hexc("#4A1A12"))
        ctx.set_source(g)
        ctx.paint()
        glow(ctx, 540, 860, 760, RED, 0.25)
        g = cairo.LinearGradient(0, 880, 0, H)
        g.add_color_stop_rgb(0, *hexc("#3A2818"))
        g.add_color_stop_rgb(1, *hexc("#0A0705"))
        ctx.rectangle(0, 880, W, H - 880)
        ctx.set_source(g)
        ctx.fill()
        ctx.move_to(480, 880)
        ctx.line_to(600, 880)
        ctx.line_to(940, H)
        ctx.line_to(140, H)
        ctx.close_path()
        rgba(ctx, hexc("#1C1816"))
        ctx.fill()
        for k in range(8):
            v = k / 8
            y0, y1 = lerp(890, H, v ** 1.6), lerp(890, H, (v + 0.06) ** 1.6)
            line(ctx, [(540, y0), (540, y1)], GOLD, lerp(3, 16, v), 0.7)
        # watchtower + sweeping searchlight
        for lx0, lx1 in ((892, 908), (968, 952)):
            line(ctx, [(lx0, 890), (lx1, 610)], hexc("#3A3D44"), 10)
        ctx.rectangle(870, 540, 110, 74)
        rgba(ctx, hexc("#2A2C31"))
        ctx.fill()
        sw = math.sin(t * 1.4) * 0.5
        ctx.move_to(925, 575)
        ctx.line_to(925 - 900 * math.cos(sw - 0.12) , 575 + 900 * math.sin(sw + 0.9))
        ctx.line_to(925 - 900 * math.cos(sw + 0.12), 575 + 900 * math.sin(sw + 1.1))
        ctx.close_path()
        g = cairo.RadialGradient(925, 575, 0, 925, 575, 900)
        g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.35)
        g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0)
        ctx.set_source(g)
        ctx.fill()
        # chain-link mesh, posts, razor-wire coil
        ctx.save()
        ctx.rectangle(0, 590, W, 300)
        ctx.clip()
        for k in range(-20, 70):
            line(ctx, [(k * 28, 590), (k * 28 + 300, 890)], STEEL, 2, 0.35)
            line(ctx, [(k * 28, 590), (k * 28 - 300, 890)], STEEL, 2, 0.35)
        ctx.restore()
        for x in range(-20, W + 120, 135):
            ctx.rectangle(x - 9, 560, 18, 330)
            rgba(ctx, hexc("#5B5F66"))
            ctx.fill()
            glow(ctx, x, 556, 26, GOLD, 0.6 + 0.3 * math.sin(t * 5 + x))
        for x in range(0, W + 30, 30):
            _ellipse(ctx, x, 560, 22, 18)
            rgba(ctx, hexc("#B5BCC6"), 0.7)
            ctx.set_line_width(3)
            ctx.stroke()
        plate(ctx, "PAKISTAN BORDER", 540, 420, RED, t - 0.1, size=52)
        # road sign on the fence
        rrect(ctx, 370, 690, 340, 120, 14)
        rgba(ctx, hexc("#0F6B3A"))
        ctx.fill_preserve()
        rgba(ctx, (1, 1, 1))
        ctx.set_line_width(5)
        ctx.stroke()
        text(ctx, "CENTRAL ASIA", 515, 750, 46, (1, 1, 1), font=CAPTION_FONT, bold=False)
        ctx.move_to(650, 728)
        ctx.line_to(690, 750)
        ctx.line_to(650, 772)
        ctx.close_path()
        rgba(ctx, (1, 1, 1))
        ctx.fill()
        drive = ease_out_cubic(t / 1.6)
        truck_rear(ctx, 540, lerp(1320, 1110, drive), lerp(1.0, 0.72, drive), brake=t > 1.3)
        if su > 0:
            stamp(ctx, 540, 720, su, -0.1, 760, 190, RED, [("BLOCKED", 0, 150, RED)])

    def ships(self, ctx, u, t):
        g = cairo.LinearGradient(0, 0, 0, 780)
        g.add_color_stop_rgb(0, *hexc("#0A2342"))
        g.add_color_stop_rgb(0.7, *hexc("#7A4A6A"))
        g.add_color_stop_rgb(1, *hexc("#F08A3C"))
        ctx.set_source(g)
        ctx.paint()
        glow(ctx, 790, 760, 420, GOLD, 0.6)
        circle(ctx, 790, 770, 80, hexc("#FFD27A"))
        g = cairo.LinearGradient(0, 780, 0, H)
        g.add_color_stop_rgb(0, *hexc("#16507A"))
        g.add_color_stop_rgb(1, *hexc("#03101C"))
        ctx.rectangle(0, 780, W, H - 780)
        ctx.set_source(g)
        ctx.fill()
        for i in range(30):
            y = 790 + 520 * rnd(i, 1) ** 1.5
            x = (rnd(i, 2) * W - t * 50 * (1 + rnd(i, 3))) % (W + 200) - 100
            line(ctx, [(x, y), (x + 40 + 80 * rnd(i, 4), y)], GOLD, 3, 0.15 + 0.4 * abs(math.sin(t * 2 + i)))
        for k in range(3):  # gulls
            gx, gy = (200 + 300 * k + t * 70) % (W + 100) - 50, 400 + 70 * k + 10 * math.sin(t * 3 + k)
            fl = 14 * math.sin(t * 9 + k)
            line(ctx, [(gx - 24, gy - fl), (gx, gy), (gx + 24, gy - fl)], (0.1, 0.1, 0.15), 4)
        container_ship(ctx, lerp(780, 1010, clamp(u / 6)), 820, 0.36, t, seed=3)
        container_ship(ctx, lerp(200, 520, ease_out_cubic(u / 2.5)) + 18 * u, 1030, 0.92, t)
        plate(ctx, "OPEN SEA ROUTE", 540, 300, NEON, u - 0.3, size=54)


class Corridor(Cued):
    """INSTC map: Mumbai -> Chabahar by sea, Pakistan bypassed, then Afghanistan, Russia and Europe."""

    def beats(self, d):
        c = self.cue
        return {"chabahar": c("चाबहार", d * 0.15), "ten": c("दस", d * 0.22), "flip": c("पलट", d * 0.35),
                "bina": c("बिना", d * 0.45), "afg": c("अफगानिस्तान", d * 0.7), "ru": c("रूस", d * 0.8),
                "eu": c("यूरोप", d * 0.87)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["chabahar"], "zap"), (b["ten"], "thud"), (b["flip"], "boom"),
                (b["bina"], "alarm"), (b["afg"], "whoosh"), (b["ru"], "whoosh"), (b["eu"], "kaching")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        v0, v1, v2 = (66.0, 23.6, 66), (64.0, 28.5, 40), (48.5, 38.0, 21)
        v = view_at([(b["bina"] - 0.1, v0), (b["bina"] + 0.8, v1), (b["ru"] - 0.1, v1), (b["ru"] + 1.1, v2)], t)
        pak = clamp((t - b["bina"]) / 0.4) * (0.75 + 0.25 * math.sin(t * 7))
        draw_map(ctx, v, t, pak=pak)
        sea = route(ctx, v, SEA_LEG, ease_in_out((t - b["chabahar"] - 0.2) / 1.6), SAFFRON, t)
        if sea is not None and t < b["chabahar"] + 1.8:  # cargo ship riding the sea leg
            container_ship(ctx, sea[0], sea[1] + 6, 0.12, t)
        route(ctx, v, AFG_LEG, ease_in_out((t - b["afg"]) / 0.9), NEON, t)
        route(ctx, v, RU_LEG, ease_in_out((t - b["ru"]) / 1.2), NEON, t)
        route(ctx, v, EU_LEG, ease_in_out((t - b["eu"]) / 0.7), GOLD, t)
        mx, my = proj(v, *CITIES["MUMBAI"])
        pin(ctx, mx, my, SAFFRON, t, t)
        plate(ctx, "MUMBAI", mx - 60, my + 80, SAFFRON, t - 0.2, size=40)
        cx, cy = proj(v, *CITIES["CHABAHAR"])
        green_flag(ctx, cx, cy, t - b["chabahar"], t)
        if t < b["ru"]:
            plate(ctx, "CHABAHAR", cx + 60, cy + 90, NEON, t - b["chabahar"] - 0.1, size=42, sub="IRAN")
        u = t - b["flip"]
        if u > 0:  # game flipped: shockwave from Chabahar
            r = ease_out_cubic(u / 0.8)
            ctx.arc(cx, cy, 40 + 600 * r, 0, math.tau)
            rgba(ctx, NEON, 0.7 * (1 - r))
            ctx.set_line_width(10)
            ctx.stroke()
        if b["ten"] <= t < b["bina"] + 0.6:
            stamp(ctx, 540, 300, t - b["ten"], -0.05, 700, 180, NEON,
                  [("10-YEAR CONTROL", -20, 88, NEON), ("CHABAHAR PORT · 2024", 52, 38, (1, 1, 1))])
        px, py = proj(v, 68.6, 29.3)
        no_entry(ctx, px, py, 46, t - b["bina"] - 0.3)
        if b["bina"] + 0.3 <= t < b["ru"]:
            plate(ctx, "NO ENTRY NEEDED", px, py + 90, RED, t - b["bina"] - 0.4, size=36)
        for city, key, c, dx, dy in (("KABUL", "afg", NEON, 0, -70), ("MOSCOW", "ru", NEON, 120, 0),
                                     ("EUROPE", "eu", GOLD, 70, -80)):
            at = b[key] + (1.2 if key == "ru" else 0.7)
            x, y = proj(v, *CITIES[city])
            pin(ctx, x, y, c, t - at, t)
            plate(ctx, city, x + dx, y + dy, c, t - at - 0.1, size=40)
        if t >= b["ru"] + 0.4:
            plate(ctx, "INSTC", 330, 950, NEON, t - b["ru"] - 0.4, size=64,
                  sub="NORTH-SOUTH TRANSPORT CORRIDOR")
        flash(ctx, t - b["flip"], 0.25, 0.5)


class Masterstroke(Cued):
    """Split screen China / Pakistan leaders sweating as billions burn; golden bolt down the split."""

    def beats(self, d):
        c = self.cue
        return {"waste": c("बर्बाद", d * 0.35), "india": c("भारत", d * 0.55), "proof": c("साबित", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["waste"], "thud"), (b["waste"] + 0.25, "kaching"), (b["india"], "zap"),
                (b["india"] + 0.03, "boom"), (b["proof"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        split = [(620, -10), (460, H + 10)]
        for side, (top, bottom) in ((0, ("#6A0C0C", "#1A0202")), (1, ("#07502A", "#011208"))):
            ctx.save()
            if side == 0:
                ctx.move_to(-10, -10)
                ctx.line_to(*split[0])
                ctx.line_to(*split[1])
                ctx.line_to(-10, H + 10)
            else:
                ctx.move_to(W + 10, -10)
                ctx.line_to(*split[0])
                ctx.line_to(*split[1])
                ctx.line_to(W + 10, H + 10)
            ctx.close_path()
            ctx.clip()
            g = cairo.LinearGradient(0, 0, 0, H)
            g.add_color_stop_rgb(0, *hexc(top))
            g.add_color_stop_rgb(1, *hexc(bottom))
            ctx.set_source(g)
            ctx.paint()
            if side == 0:  # star motif
                for k, (sx, sy, r) in enumerate(((120, 260, 60), (220, 180, 22), (260, 270, 22), (250, 360, 22))):
                    self.star(ctx, sx, sy, r, t * 0.3 + k, hexc("#FFD60A"), 0.3)
            else:          # crescent motif
                circle(ctx, 930, 260, 80, (1, 1, 1), 0.25)
                circle(ctx, 960, 240, 70, hexc("#07502A"))
                self.star(ctx, 900, 220, 24, 0.3, (1, 1, 1), 0.3)
            # crashing chart behind each leader
            base = 160 if side == 0 else 640
            pts = [(base + k * 75, 420 + 95 * k + 40 * math.sin(k * 2.1)) for k in range(6)]
            drawn, head = partial(pts, ease_in_out((t - 0.3) / 1.6))
            line(ctx, drawn, RED, 14, 0.85)
            if t > 0.3:
                ctx.save()
                ctx.translate(*head)
                ctx.rotate(math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0]))
                ctx.move_to(30, 0)
                ctx.line_to(-12, -24)
                ctx.line_to(-12, 24)
                ctx.close_path()
                rgba(ctx, RED)
                ctx.fill()
                ctx.restore()
            ctx.restore()
        bust(ctx, 270, 620, 0.9, t, hexc("#1C2233"), hexc("#B3121F"), None, 0)
        bust(ctx, 815, 660, 0.86, t, hexc("#151515"), hexc("#0E6B37"), hexc("#9A9A9A"), 1)
        plate(ctx, "XI JINPING", 270, 1050, RED, t - 0.15, size=48)
        plate(ctx, "SHEHBAZ SHARIF", 790, 1050, NEON, t - 0.3, size=48)
        u = t - b["waste"]
        if u > 0:  # dollar bills burning as they fall
            for i in range(18):
                fy = -80 + (rnd(i, 1) * 300 + u * (380 + 200 * rnd(i, 2))) % 1200
                fx = rnd(i, 3) * W + 40 * math.sin(u * 2 + i)
                ctx.save()
                ctx.translate(fx, fy)
                ctx.rotate(u * (1 + 2 * rnd(i, 4)) + i)
                burn = clamp((fy - 300) / 600)
                glow(ctx, 0, 0, 60, hexc("#FF8A1F"), 0.6 * burn)
                rrect(ctx, -44, -22, 88, 44, 4)
                rgba(ctx, (lerp(0.35, 0.15, burn), lerp(0.6, 0.12, burn), lerp(0.3, 0.05, burn)))
                ctx.fill()
                text(ctx, "$", 0, 0, 34, (1, 1, 1), font=CAPTION_FONT, bold=False, a=1 - burn * 0.7)
                ctx.restore()
            stamp(ctx, 540, 290, u, -0.05, 640, 170, RED, [("-$62B", -10, 110, RED), ("WASTED", 60, 40, (1, 1, 1))])
        u = t - b["india"]
        if u > 0:  # golden bolt down the split
            k = ease_out_cubic(u / 0.2)
            jag = [(lerp(620, 460, y / H) + (36 if j % 2 else -36), y) for j, y in enumerate(range(-10, H, 120))]
            drawn, _ = partial(jag, k)
            line(ctx, drawn, GOLD, 34, 0.35)
            line(ctx, drawn, (1, 1, 0.85), 12)
            for c, dy in zip((SAFFRON, (1, 1, 1), INDIA_GREEN), (-14, 0, 14)):
                line(ctx, [(0, 1110 + dy), (W * ease_out_cubic(u / 0.5), 1110 + dy)], c, 10, 0.9)
            flash(ctx, u, 0.25, 0.7)
        u = t - b["proof"]
        if u > 0:
            ctx.save()
            ctx.translate(540, 560)
            pop = ease_out_back(u / 0.3)
            ctx.scale(pop, pop)
            glow(ctx, 0, 0, 260, GOLD, 0.6)
            bolt(ctx, 0, 0, 4.2, GOLD)
            ctx.restore()

    @staticmethod
    def star(ctx, x, y, r, rot, c, a):
        for k in range(10):
            ang = rot + k * math.pi / 5 - math.pi / 2
            rr = r if k % 2 == 0 else r * 0.42
            (ctx.move_to if k == 0 else ctx.line_to)(x + rr * math.cos(ang), y + rr * math.sin(ang))
        ctx.close_path()
        rgba(ctx, c, a)
        ctx.fill()


def flash(ctx, u, dur=0.25, a=0.6):
    if 0 <= u < dur:
        rgba(ctx, (1, 1, 1), a * (1 - u / dur))
        ctx.paint()


def bell(ctx, x, y, s, t, ring=1.0):
    """Notification bell centred on (x, y), swinging while ring > 0."""
    ctx.save()
    ctx.translate(x, y - 30 * s)
    ctx.rotate(0.35 * ring * math.sin(t * 18))
    ctx.scale(s, s)
    ctx.move_to(-30, 34)
    ctx.curve_to(-30, -10, -26, -34, 0, -36)
    ctx.curve_to(26, -34, 30, -10, 30, 34)
    ctx.line_to(38, 44)
    ctx.line_to(-38, 44)
    ctx.close_path()
    rgba(ctx, GOLD)
    ctx.fill_preserve()
    rgba(ctx, (0, 0, 0))
    ctx.set_line_width(3)
    ctx.stroke()
    circle(ctx, 0, -40, 6, GOLD)
    circle(ctx, 0, 52, 9, GOLD)
    ctx.restore()


class Cta(Cued):
    """Tricolor sunburst, ringing bell, Reality Shift subscribe button clicked by a cursor."""

    def click(self, d):
        return min(d - 0.5, self.cue("सब्सक्राइब", d * 0.75) + 0.3)

    def events(self, d):
        return [(0.02, "boom"), (0.25, "dingdong"), (self.click(d), "pick"), (self.click(d) + 0.05, "pop")]

    def draw(self, ctx, t, d):
        backdrop(ctx, hexc("#2A1204"), hexc("#070301"), SAFFRON, 540, 640, t, motes=20)
        ctx.save()
        ctx.translate(540, 640)
        ctx.rotate(t * 0.2)
        for k in range(24):
            a = k / 24 * math.tau
            ctx.move_to(0, 0)
            ctx.arc(0, 0, 1500, a, a + math.tau / 48)
            ctx.close_path()
            rgba(ctx, (SAFFRON, (1, 1, 1), INDIA_GREEN)[k % 3], 0.07)
            ctx.fill()
        ctx.restore()
        clicked = t >= self.click(d)
        pop = ease_out_back(t / 0.35)
        ctx.save()
        ctx.translate(540, 360)
        ctx.scale(pop, pop)
        glow(ctx, 0, 0, 360, GOLD, 0.35)
        text(ctx, "INDIA KI", 0, -70, 70, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=10)
        text(ctx, "GEO-POLITICS", 0, 40, 120, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=14)
        ctx.restore()
        glow(ctx, 540, 640, 170, GOLD, 0.5 + 0.2 * math.sin(t * 8))
        bell(ctx, 540, 660, 2.2, t, ring=1.0 if not clicked else clamp(1 - (t - self.click(d)) / 0.4) + 0.6)
        if clicked:  # bell burst once subscribed
            r = ease_out_cubic((t - self.click(d)) / 0.6)
            ctx.arc(540, 640, 120 + 260 * r, 0, math.tau)
            rgba(ctx, GOLD, 0.7 * (1 - r))
            ctx.set_line_width(8)
            ctx.stroke()
        bx, by = subscribe_badge(ctx, 540, 960, t, clicked)
        cu = clamp((t - (self.click(d) - 0.8)) / 0.7)
        if cu > 0:
            cx, cy = lerp(1040, bx + 20, ease_in_out(cu)), lerp(1110, by + 20, ease_in_out(cu))
            sc = 0.85 if abs(t - self.click(d)) < 0.12 else 1.0
            ctx.save()
            ctx.translate(cx, cy)
            ctx.scale(sc, sc)
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


SCENE_CLASSES = {"hook": Hook, "blocked": Blocked, "corridor": Corridor, "masterstroke": Masterstroke, "cta": Cta}


# ============================================================ compositor (Golden Safe Zone)

# badge icons standing in for the brief's emoji: name -> draw(ctx, x, y, t), centred on (x, y)
ICONS = {
    "siren": siren,
    "flag": lambda ctx, x, y, t: flag(ctx, x - 38, y - 25, 76, 50, "in", t),
    "bolt": lambda ctx, x, y, t: bolt(ctx, x, y, 1.0, GOLD),
    "bell": lambda ctx, x, y, t: bell(ctx, x, y, 0.7, t),
}


def badge(ctx, spec, u, t):
    """Scene's on-screen text in a high-contrast badge, hard-clipped to Y BADGE_TOP..BADGE_BOTTOM."""
    if u <= 0:
        return
    size = 66
    tw = text_width(ctx, spec["text"], size, font=CAPTION_FONT, bold=False)
    iw = 92 if spec["icon"] else 0
    w = tw + iw + 96
    if w > 1000:
        size *= (1000 - iw - 96) / tw
        tw, w = 1000 - iw - 96, 1000
    h = BADGE_BOTTOM - BADGE_TOP
    ctx.save()
    ctx.rectangle(0, BADGE_TOP, W, h)
    ctx.clip()
    ctx.translate(W / 2, BADGE_TOP + h / 2)
    ctx.scale(max(ease_out_back(u / 0.32), 1e-3), 1)  # horizontal pop only: the band never grows
    rrect(ctx, -w / 2, -h / 2, w, h, 24)
    rgba(ctx, (0.02, 0.02, 0.03), 0.95)
    ctx.fill()
    ctx.save()
    rrect(ctx, -w / 2, -h / 2, w, h, 24)
    ctx.clip()
    gx = -w / 2 - 200 + ((t * 0.5) % 1.4) * (w + 400)  # gloss sweep
    ctx.move_to(gx, -h)
    ctx.line_to(gx + 70, -h)
    ctx.line_to(gx - 30, h)
    ctx.line_to(gx - 100, h)
    ctx.close_path()
    rgba(ctx, (1, 1, 1), 0.08)
    ctx.fill()
    ctx.restore()
    rrect(ctx, -w / 2 + 4, -h / 2 + 4, w - 8, h - 8, 21)
    rgba(ctx, spec["accent"])
    ctx.set_line_width(6)
    ctx.stroke()
    x0 = -w / 2 + 48
    if spec["icon"]:
        ICONS[spec["icon"]](ctx, x0 + 36, 0, t)
    text(ctx, spec["text"], x0 + iw, 3, size, (1, 1, 1), font=CAPTION_FONT, bold=False, anchor="l")
    ctx.restore()


def compose(idx, tl, spec=SPEC):
    sc = engine.SCENES[idx]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    # camera: slow push for the whole scene, plus a punch-in on every cut
    zoom = 1.0 + 0.03 * tl / sc["dur"]
    if idx:
        zoom += 0.08 * (1 - ease_out_cubic(tl / 0.35))
    ctx.save()
    ctx.translate(W / 2, H * 0.4)
    ctx.scale(zoom, zoom)
    ctx.translate(-W / 2, -H * 0.4)
    sc["obj"].draw(ctx, tl, sc["dur"])
    ctx.restore()
    if idx:
        flash(ctx, tl, 0.2, 0.5)
    vignette(ctx)
    g = cairo.LinearGradient(0, BADGE_BOTTOM + 10, 0, UI_CLEAR)  # bottom 400px: clean dark band
    g.add_color_stop_rgba(0, 0.01, 0.01, 0.02, 0)
    g.add_color_stop_rgba(1, 0.01, 0.01, 0.02, 0.94)
    ctx.rectangle(0, BADGE_BOTTOM + 10, W, H)
    ctx.set_source(g)
    ctx.fill()
    ctx.rectangle(0, UI_CLEAR, W, H - UI_CLEAR)
    rgba(ctx, (0.01, 0.01, 0.02), 0.94)
    ctx.fill()
    text(ctx, "• REALITY SHIFT •", W / 2, 92, 32, hexc("#B8BCC6"), a=0.55)
    badge(ctx, spec[idx], tl - 0.15, tl)
    return surf


def make_frame(t: float) -> np.ndarray:
    scenes = engine.SCENES
    idx = max(i for i, s in enumerate(scenes) if t >= s["start"] or i == 0)
    surf = compose(idx, t - scenes[idx]["start"])
    surf.flush()
    buf = np.ndarray((H, W, 4), dtype=np.uint8, buffer=surf.get_data())
    return buf[:, :, 2::-1].copy()


def write_alignment(final, specs=SPEC):
    out = []
    for spec, s in zip(specs, engine.SCENES):
        vo = spec["vo"] if isinstance(spec["vo"], str) else " ".join(line[1] for line in spec["vo"])  # performed lines
        out.append({"scene": spec["key"], "spec_window": spec["window"], "start": round(s["start"], 3),
                    "end": round(s["start"] + s["dur"], 3), "voiceover": vo, "on_screen_text": spec["text"],
                    "visual": spec["visual"],
                    "words": [{"t": round(s["start"] + st, 3), "w": w} for st, w in s["captions"]]})
    path = final.with_suffix(".json")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Alignment: {path}")


def main() -> None:
    story = importlib.import_module("generate_chabahar_short")  # a named module, so work files land in work/<name>/
    engine.make_frame = story.make_frame
    final = engine.render(story, "edge")
    write_alignment(final)


if __name__ == "__main__":
    main()
