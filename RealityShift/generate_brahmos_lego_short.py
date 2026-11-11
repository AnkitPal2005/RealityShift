"""Reality Shift Short - BrahMos: ~3x the speed of sound, why it is so hard to stop (~40s).

Usage:
  python generate_brahmos_lego_short.py

First Short on the Lego template (lego.py): radar header, word-chip captions, scan-line wipes, amber palette,
comment-prompt ending. Five scenes: radar scope hook (30 seconds) -> speed (Mach 2.8, ~1 km/s, Delhi-Agra in
~3 min) -> side view: sea-skimming under the ship's radar horizon (10 m, seen ~30 km out = ~30 s) -> India + Russia,
Brahmaputra + Moskva, Philippines export -> "which missile next?" comment prompt.
The 30 s figure is arithmetic, not a quoted spec: a sea-skimmer is first seen near the radar horizon (~30 km for
a mast-top radar against a target ~10 m up), and at ~1 km/s that leaves ~30 s.
"""

import importlib
import json
import math

import cairo

import engine
import lego
from engine import *  # noqa: F401,F403
from generate_chabahar_short import Cued, partial
from generate_rupee_short import VOICE_TONES
from stories.reality_shift import flag, stamp

TOPIC = "BRAHMOS"
OUTPUTS = {"edge": "brahmos_short.mp4"}
LEGO = {"header": "radar", "caption": "chip", "transition": "scan", "palette": "amber", "ending": "prompt"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.3
TAIL_PAD = 0.35
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 118
MUSIC_STYLE = "pulse"      # driving synth pulse for a speed story (Chicken's Neck was march @ 96)
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"

PAL = lego.PALETTES["amber"]
AMBER = PAL["ui"]
HI = PAL["hi"]
RED = PAL["alert"]
TEAL = hexc("#46E0B0")
SEA_BLUE = hexc("#2F8FD8")
STEEL = hexc("#C9CED6")
INK = PAL["ink"]
MONO = lego.MONO

SOURCES = [
    "Speed Mach 2.8 (~3x speed of sound), range 290 km original / ~450-500 km extended, cruise up to 15 km, terminal "
    "altitude as low as 10 m (BrahMos Aerospace 'BrahMos' product page; DRDO / PIB releases)",
    "BrahMos Aerospace: India (DRDO) - Russia (NPO Mashinostroyeniya) joint venture, 1998; name from the Brahmaputra "
    "and Moskva rivers (BrahMos Aerospace 'About us')",
    "Philippines: USD 375M deal for shore-based BrahMos batteries signed Jan 2022, first delivery Apr 2024 "
    "(PIB / MoD release; Reuters, The Hindu, Apr 2024)",
    "Arithmetic: Mach 2.8 at sea level ~ 950 m/s ~ 1 km/s; Delhi-Agra ~180 km straight line -> ~3 min; radar horizon "
    "d ~ 4.12*(sqrt(h_radar)+sqrt(h_target)) km = 4.12*(sqrt 25 + sqrt 10) ~ 34 km -> 'kareeb 30 km', ~30 s",
]

# each line: (tone, [(spoken Hindi, Hinglish caption), ...], pause after)
SPEC = [
    {"key": "scope", "accent": RED, "text": "30 SECOND",
     "visual": "Ship's radar scope, a contact streaks in from the edge, 00:30 countdown, BrahMos slices across",
     "vo": [("hook", [("ये मिसाइल", "YEH MISSILE"), ("रडार पर दिखे...", "RADAR PAR DIKHE...")], 0.5),
            ("punch", [("तो जहाज़ के पास", "TOH JAHAAZ KE PAAS"), ("बचते हैं", "BACHTE HAIN"),
                       ("बस तीस सेकंड।", "BAS 30 SECOND!")], 0.4),
            ("tell", [("नाम है", "NAAM HAI"), ("ब्रह्मोस।", "BRAHMOS.")], 0)]},
    {"key": "speed", "accent": HI, "text": "MACH 2.8",
     "visual": "Missile tears through speed lines; sound vs BrahMos bars (1x vs 2.8x); 1 KM/SEC; Delhi -> Agra in ~3 min",
     "vo": [("build", [("आवाज़ से", "AAWAZ SE"), ("लगभग तीन गुना तेज़।", "LAGBHAG 3 GUNA TEZ!")], 0.35),
            ("punch", [("हर सेकंड में", "HAR SECOND MEIN"), ("करीब एक किलोमीटर।", "KAREEB 1 KILOMETER!")], 0.35),
            ("tell", [("दिल्ली से आगरा जितनी दूरी,", "DELHI SE AGRA JITNI DOORI,"),
                      ("सिर्फ तीन मिनट में।", "SIRF 3 MINUTE MEIN!")], 0)]},
    {"key": "skim", "accent": TEAL, "text": "10 METER",
     "visual": "Side view over a curved sea: missile dives to 10 m, hides in the radar shadow, detected ~30 km out",
     "vo": [("build", [("पर असली चाल", "PAR ASLI CHAAL"), ("कुछ और है...", "KUCH AUR HAI...")], 0.45),
            ("low", [("आखिर में ये", "AAKHIR MEIN YEH"), ("समुद्र से", "SAMUDRA SE"),
                     ("सिर्फ दस मीटर ऊपर", "SIRF 10 METER UPAR"), ("उड़ती है।", "UDTI HAI!")], 0.35),
            ("tell", [("इतनी नीचे, कि जहाज़ का रडार", "ITNI NEECHE, KI JAHAAZ KA RADAR"),
                      ("इसे करीब तीस किलोमीटर", "ISE KAREEB 30 KM"), ("दूर से ही देख पाता है।", "DOOR SE HI DEKH PAATA HAI.")],
             0.4),
            ("punch", [("और तीस किलोमीटर...", "AUR 30 KM..."), ("मतलब तीस सेकंड।", "MATLAB 30 SECOND!")], 0)]},
    {"key": "made", "accent": AMBER, "text": "INDIA + RUSSIA",
     "visual": "India and Russia flags, two rivers meet and spell BRAHMOS, then the Philippines flag + EXPORT stamp",
     "vo": [("tell", [("इसे भारत और रूस ने", "ISE BHARAT AUR RUSS NE"), ("मिलकर बनाया है।", "MILKAR BANAYA HAI.")], 0.3),
            ("sly", [("नाम दो नदियों से बना,", "NAAM DO NADIYON SE BANA,"),
                     ("ब्रह्मपुत्र और मॉस्कवा।", "BRAHMAPUTRA + MOSKVA!")], 0.4),
            ("punch", [("और आज फिलीपींस भी", "AUR AAJ PHILIPPINES BHI"),
                       ("इसे भारत से खरीद चुका है।", "ISE BHARAT SE KHAREED CHUKA HAI!")], 0)]},
    {"key": "ask", "accent": HI, "text": "AGLI MISSILE?",
     "visual": "Dim radar sweep behind a question card; the comment field types missile names; arrow at comment button",
     "vo": [("ask", [("अगली कहानी", "AGLI KAHANI"), ("किस मिसाइल की चाहिए?", "KIS MISSILE KI CHAHIYE?")], 0.6),
            ("cta", [("नाम कमेंट में लिखो,", "NAAM COMMENT MEIN LIKHO,"), ("और रियलिटी शिफ्ट को", "AUR REALITY SHIFT KO"),
                     ("सब्सक्राइब करो!", "SUBSCRIBE KARO!")], 0)]},
]

DELIVERY = {s["key"]: [(VOICE_TONES[tone], " ".join(hi for hi, _ in chunks), pause) for tone, chunks, pause in s["vo"]]
            for s in SPEC}
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {"RADAR": AMBER, "30": RED, "SECOND!": RED, "BRAHMOS": HI, "3": HI, "GUNA": HI, "TEZ!": HI, "1": HI,
       "KILOMETER!": HI, "DELHI": TEAL, "AGRA": TEAL, "MINUTE": HI, "CHAAL": RED, "10": TEAL, "METER": TEAL,
       "SAMUDRA": TEAL, "KM": RED, "KM...": RED, "BHARAT": AMBER, "RUSS": AMBER, "BRAHMAPUTRA": SEA_BLUE,
       "MOSKVA": SEA_BLUE, "PHILIPPINES": HI, "AGLI": HI, "MISSILE": HI, "COMMENT": HI, "SUBSCRIBE": RED}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".")] = HOT[_k]


# ============================================================ props

def bg(ctx, top=(0.05, 0.035, 0.02), bottom=(0.01, 0.008, 0.005)):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *top)
    g.add_color_stop_rgb(1, *bottom)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()


def missile(ctx, x, y, length, ang, t, flame=1.0, label=True):
    """Side view of the missile, centre at (x, y), nose along angle ang."""
    d = length * 0.085
    L = length
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    if flame > 0:
        for k, (c, a) in enumerate(((RED, 0.55), (AMBER, 0.8), ((1, 0.97, 0.85), 0.95))):
            f = (1 + 0.22 * math.sin(t * 47 + k * 2.1)) * flame * (1 - 0.28 * k)
            ctx.move_to(-L / 2, -d * (0.42 - 0.1 * k))
            ctx.curve_to(-L / 2 - L * 0.18 * f, -d * 0.3, -L / 2 - L * 0.32 * f, -d * 0.05, -L / 2 - L * 0.38 * f, 0)
            ctx.curve_to(-L / 2 - L * 0.32 * f, d * 0.05, -L / 2 - L * 0.18 * f, d * 0.3, -L / 2, d * (0.42 - 0.1 * k))
            ctx.close_path()
            rgba(ctx, c, a)
            ctx.fill()
        glow(ctx, -L / 2 - L * 0.1, 0, L * 0.18, AMBER, 0.35 * flame)
    nose = L * 0.2
    for sgn in (-1, 1):  # rear fins
        ctx.move_to(-L / 2 + L * 0.02, sgn * d * 0.45)
        ctx.line_to(-L / 2 - L * 0.01, sgn * d * 1.35)
        ctx.line_to(-L / 2 + L * 0.13, sgn * d * 0.45)
        ctx.close_path()
        rgba(ctx, shade(STEEL, 0.6))
        ctx.fill()
        ctx.move_to(-L * 0.02, sgn * d * 0.45)  # mid wings
        ctx.line_to(L * 0.02, sgn * d * 0.95)
        ctx.line_to(L * 0.1, sgn * d * 0.45)
        ctx.close_path()
        rgba(ctx, shade(STEEL, 0.7))
        ctx.fill()
    g = cairo.LinearGradient(0, -d / 2, 0, d / 2)
    g.add_color_stop_rgb(0, 0.95, 0.96, 0.98)
    g.add_color_stop_rgb(0.55, 0.72, 0.75, 0.8)
    g.add_color_stop_rgb(1, 0.38, 0.4, 0.45)
    ctx.move_to(-L / 2, -d / 2)
    ctx.line_to(L / 2 - nose, -d / 2)
    ctx.curve_to(L / 2 - nose * 0.35, -d / 2, L / 2 - nose * 0.05, -d * 0.18, L / 2, 0)
    ctx.curve_to(L / 2 - nose * 0.05, d * 0.18, L / 2 - nose * 0.35, d / 2, L / 2 - nose, d / 2)
    ctx.line_to(-L / 2, d / 2)
    ctx.close_path()
    ctx.set_source(g)
    ctx.fill()
    ctx.rectangle(L / 2 - nose - L * 0.04, -d / 2, L * 0.025, d)
    rgba(ctx, (0.12, 0.13, 0.16))
    ctx.fill()
    ctx.rectangle(-L / 2, -d / 2, L * 0.05, d)
    rgba(ctx, (0.2, 0.21, 0.24))
    ctx.fill()
    if label and L > 300:
        text(ctx, "BRAHMOS", -L * 0.08, 1, d * 0.5, (0.1, 0.12, 0.2), font=CAPTION_FONT, bold=False)
    ctx.restore()


def scope(ctx, cx, cy, r, t, a=1.0, labels=True):
    """Ship's radar PPI: rings, crosshair, range labels and a sweep with a fading trail."""
    circle(ctx, cx, cy, r, (0.02, 0.016, 0.008), 0.92 * a)
    for k in range(1, 4):
        ctx.arc(cx, cy, r * k / 3, 0, math.tau)
        rgba(ctx, AMBER, 0.35 * a)
        ctx.set_line_width(2.5)
        ctx.stroke()
        if labels:
            text(ctx, f"{10 * k} KM", cx + 12, cy - r * k / 3 + 22, 24, AMBER, font=MONO, a=0.6 * a, anchor="l")
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        line(ctx, [(cx + r * 0.96 * math.cos(rad), cy + r * 0.96 * math.sin(rad)),
                   (cx + r * math.cos(rad), cy + r * math.sin(rad))], AMBER, 3, 0.6 * a)
    line(ctx, [(cx - r, cy), (cx + r, cy)], AMBER, 1.5, 0.25 * a)
    line(ctx, [(cx, cy - r), (cx, cy + r)], AMBER, 1.5, 0.25 * a)
    ang = t * 2.4
    for k in range(24):
        a0 = ang - k * 0.04
        ctx.move_to(cx, cy)
        ctx.arc(cx, cy, r, a0 - 0.045, a0)
        ctx.close_path()
        rgba(ctx, AMBER, 0.38 * (1 - k / 24) * a)
        ctx.fill()
    line(ctx, [(cx, cy), (cx + r * math.cos(ang), cy + r * math.sin(ang))], HI, 3, 0.9 * a)
    ctx.arc(cx, cy, r, 0, math.tau)
    rgba(ctx, AMBER, 0.8 * a)
    ctx.set_line_width(5)
    ctx.stroke()


def ship_icon(ctx, x, y, s, c):
    ctx.move_to(x, y - 26 * s)
    ctx.line_to(x + 14 * s, y + 18 * s)
    ctx.line_to(x - 14 * s, y + 18 * s)
    ctx.close_path()
    rgba(ctx, c)
    ctx.fill()


def tag(ctx, s, x, y, c, u, size=40, sub=None):
    """Bracketed mono label that wipes open, centred on (x, y)."""
    if u <= 0:
        return
    w = max(text_width(ctx, s, size, font=MONO), text_width(ctx, sub, size * 0.65, font=MONO) if sub else 0) + 50
    h = size * (2.3 if sub else 1.5)
    k = ease_out_cubic(u / 0.25)
    ctx.save()
    ctx.translate(x, y)
    ctx.rectangle(-w / 2, -h / 2 - 10, w * k, h + 20)
    ctx.clip()
    rrect(ctx, -w / 2, -h / 2, w, h, 8)
    rgba(ctx, (0.02, 0.015, 0.01), 0.9)
    ctx.fill()
    for sx in (-1, 1):
        for sy in (-1, 1):
            px, py = sx * w / 2, sy * h / 2
            line(ctx, [(px - sx * 22, py), (px, py), (px, py - sy * 22)], c, 4)
    text(ctx, s, 0, -size * 0.42 if sub else 0, size, INK, font=MONO)
    if sub:
        text(ctx, sub, 0, size * 0.62, size * 0.65, c, font=MONO)
    ctx.restore()


def ph_flag(ctx, x, y, w, h, t):
    """Philippines flag (blue over red, white hoist triangle with sun and three stars), waving in strips."""
    n = 14
    for i in range(n):
        dy = 7 * math.sin(t * 5 - i * 0.6) * (i / n)
        ctx.save()
        ctx.rectangle(x + w * i / n, y + dy, w / n + 1, h)
        ctx.clip()
        ctx.translate(x, y + dy)
        ctx.rectangle(0, 0, w, h / 2)
        rgba(ctx, hexc("#0038A8"))
        ctx.fill()
        ctx.rectangle(0, h / 2, w, h / 2)
        rgba(ctx, hexc("#CE1126"))
        ctx.fill()
        tw = h * 0.866
        ctx.move_to(0, 0)
        ctx.line_to(tw, h / 2)
        ctx.line_to(0, h)
        ctx.close_path()
        rgba(ctx, (1, 1, 1))
        ctx.fill()
        sun = hexc("#FCD116")
        circle(ctx, tw * 0.36, h / 2, h * 0.09, sun)
        for k in range(8):
            a = k * math.pi / 4
            line(ctx, [(tw * 0.36 + h * 0.11 * math.cos(a), h / 2 + h * 0.11 * math.sin(a)),
                       (tw * 0.36 + h * 0.17 * math.cos(a), h / 2 + h * 0.17 * math.sin(a))], sun, h * 0.025)
        for sx, sy in ((h * 0.07, h * 0.1), (h * 0.07, h * 0.9), (tw * 0.86, h / 2)):
            circle(ctx, sx, sy, h * 0.035, sun)
        ctx.restore()


def speed_lines(ctx, t, n=46, speed=2600, c=AMBER, y0=170, y1=1130):
    for i in range(n):
        y = y0 + rnd(i, 3) * (y1 - y0)
        ln = 80 + 260 * rnd(i, 5)
        x = W + 300 - ((rnd(i, 7) * (W + 600) + t * speed * (0.6 + rnd(i, 9))) % (W + 600))
        line(ctx, [(x, y), (x + ln, y)], c, 2 + 3 * rnd(i, 11), 0.15 + 0.3 * rnd(i, 13))


# ============================================================ scenes

class Scope(Cued):
    """Radar scope: a contact streaks in from the rim, 00:30 countdown, then BrahMos slices across."""

    CX, CY, R = 540, 650, 390

    def beats(self, d):
        c = self.cue
        return {"radar": c("RADAR", d * 0.1), "sec": c("30", d * 0.5), "name": c("BRAHMOS", d * 0.82)}

    def events(self, d):
        b = self.beats(d)
        ticks = [(b["sec"] + 0.25 + k * 0.5, "tick" if k % 2 else "tock") for k in range(int((b["name"] - b["sec"]) / 0.5))]
        return [(0.02, "boom"), (0.3, "beep"), (b["radar"], "alarm"), (b["radar"] + 0.4, "beep"),
                (b["sec"], "thud"), (b["name"] - 0.15, "whoosh"), (b["name"], "boom")] + ticks

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx)
        cx, cy, r = self.CX, self.CY, self.R
        scope(ctx, cx, cy, r, t)
        ship_icon(ctx, cx, cy, 1.2, TEAL)
        text(ctx, "YOUR SHIP", cx, cy + 50, 24, TEAL, font=MONO, a=0.8)
        u = t - b["radar"]
        if u > 0:  # the contact runs in from the rim toward the ship
            k = clamp(u / max(d - b["radar"], 1.0))
            ang = -2.35
            for j in range(10):
                rr = r * (0.98 - 0.55 * clamp(k - j * 0.012))
                circle(ctx, cx + rr * math.cos(ang), cy + rr * math.sin(ang), 12 - j, RED, 0.8 * (1 - j / 10))
            rr = r * (0.98 - 0.55 * k)
            bx, by = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
            ring = (t * 1.6) % 1
            ctx.arc(bx, by, 18 + 50 * ring, 0, math.tau)
            rgba(ctx, RED, 0.9 * (1 - ring))
            ctx.set_line_width(4)
            ctx.stroke()
            glow(ctx, bx, by, 40, RED, 0.8)
            label = "BRAHMOS" if t > b["name"] else "UNKNOWN • FAST"
            tag(ctx, label, clamp(bx + 40, 280, 800), by - 70, RED, u, size=34)
        u = t - b["sec"]
        if u > 0 and t < b["name"]:
            left = max(0.0, 30 - u)
            stamp(ctx, cx, cy + 210, u, -0.03, 470, 170, RED,
                  [(f"00:{int(math.ceil(left)):02d}", -12, 130, RED), ("SECONDS LEFT", 62, 30, INK)])
        u = t - b["name"]
        if u > 0:
            x = lerp(-400, W + 500, ease_in_out(u / 1.1))
            missile(ctx, x, cy + 40, 720, -0.06, t)
            stamp(ctx, 540, 1035, u - 0.2, -0.03, 700, 160, HI,
                  [("BRAHMOS", -16, 104, HI), ("SUPERSONIC CRUISE MISSILE", 52, 32, INK)])


class Speed(Cued):
    """Speed lines; sound vs BrahMos bars; ~1 KM / SEC; Delhi -> Agra in ~3 minutes."""

    def beats(self, d):
        c = self.cue
        return {"guna": c("GUNA", d * 0.18), "km": c("KILOMETER", d * 0.42), "delhi": c("DELHI", d * 0.6),
                "min": c("MINUTE", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "whoosh"), (0.1, "engine", 1.2), (b["guna"], "zap"), (b["guna"] + 0.1, "thud"),
                (b["km"], "kaching"), (b["delhi"], "beep"), (b["delhi"] + 0.2, "whoosh"), (b["min"], "dingdong")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx, (0.06, 0.04, 0.03), (0.01, 0.01, 0.02))
        speed_lines(ctx, t)
        shake = 3 * math.sin(t * 60)
        missile(ctx, 520, 370 + shake, 660, 0, t)
        text(ctx, "MACH 2.8", 540, 230, 54, HI, font=MONO, a=clamp((t - b["guna"]) / 0.3))
        panel_y = 600
        rrect(ctx, 80, panel_y - 70, W - 160, 300, 20)
        rgba(ctx, (0.02, 0.015, 0.01), 0.88)
        ctx.fill()
        unit = 250
        rows = (("AAWAZ", 1.0, TEAL, "1x", 0.0), ("BRAHMOS", 2.8, HI, "~2.8x", b["guna"]))
        for k, (name, mult, c, lab, start) in enumerate(rows):
            y = panel_y + k * 120
            text(ctx, name, 110, y - 30, 30, c, font=MONO, anchor="l")
            grow = ease_out_cubic(clamp((t - start) / 0.6)) if start else ease_out_cubic(clamp(t / 0.5))
            rrect(ctx, 110, y, unit * 3.4, 46, 10)
            rgba(ctx, c, 0.12)
            ctx.fill()
            if grow > 0:
                rrect(ctx, 110, y, unit * mult * grow, 46, 10)
                rgba(ctx, c, 0.95)
                ctx.fill()
                text(ctx, lab, 130 + unit * mult * grow, y + 23, 34, INK, font=MONO, anchor="l", a=grow)
        u = t - b["km"]
        if u > 0 and t < b["delhi"]:
            tag(ctx, "~1 KM / SECOND", 540, 950, HI, u, size=58)
        u = t - b["delhi"]
        if u > 0:
            x0, x1, y = 190, 890, 990
            k = clamp(u / max(b["min"] - b["delhi"] + 0.4, 0.8))
            ctx.set_dash([18, 14])
            line(ctx, [(x0, y), (x1, y)], AMBER, 6, 0.5)
            ctx.set_dash([])
            line(ctx, [(x0, y), (lerp(x0, x1, k), y)], HI, 10)
            for x, name in ((x0, "DELHI"), (x1, "AGRA")):
                circle(ctx, x, y, 18, TEAL)
                text(ctx, name, x, y + 56, 38, TEAL, font=MONO)
            glow(ctx, lerp(x0, x1, k), y, 40, HI, 0.9)
            missile(ctx, lerp(x0, x1, k), y - 50, 160, 0, t, label=False)
            m = 3 * k
            text(ctx, f"{int(m)}:{int(round((m % 1) * 60)) % 60:02d} MIN", 540, y - 140, 64, INK, font=MONO)
            text(ctx, "~180 KM", 540, y + 56, 32, AMBER, font=MONO, a=0.8)


class Skim(Cued):
    """Side view over a curved sea: the missile dives to ~10 m, stays in the radar shadow, is seen ~30 km out."""

    # exaggerated curvature so the radar shadow beyond the horizon is visible: horizon near x=500, wedge ~80px deep
    SHIP_X, SEA0, DROP = 900, 760, 486
    MAST = (905, 664)

    def sea_y(self, x):
        k = self.DROP / self.SHIP_X ** 2
        return self.SEA0 + k * max(self.SHIP_X - x, 0) ** 2

    def tangent_x(self):
        """Where the ship's radar line of sight just grazes the curved sea (the radar horizon)."""
        mx, my = self.MAST
        k = self.DROP / self.SHIP_X ** 2
        best, xt = 1e9, 0
        for x in range(0, self.SHIP_X - 20, 2):
            slope = (self.sea_y(x) - my) / (x - mx)
            err = abs(slope - (-2 * k * (self.SHIP_X - x)))
            if err < best:
                best, xt = err, x
        return xt

    def beats(self, d):
        c = self.cue
        return {"chaal": c("CHAAL", d * 0.03), "dive": c("AAKHIR", d * 0.16), "ten": c("10", d * 0.28),
                "radar": c("RADAR", d * 0.48), "seen": c("KAREEB", d * 0.6), "pay": c("MATLAB", d * 0.88)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["chaal"], "beep"), (b["dive"], "whoosh"), (b["ten"], "pick"),
                (b["radar"], "beep"), (b["radar"] + 0.5, "beep"), (b["seen"], "alarm"), (b["pay"], "boom")]

    def path(self, t, d, b, xt):
        xs = [(0.0, 130), (b["seen"], xt + 10), (d, xt + 250)]
        x = xs[-1][1]
        for (t0, a), (t1, c) in zip(xs, xs[1:]):
            if t <= t1:
                x = lerp(a, c, clamp((t - t0) / max(t1 - t0, 0.05)))
                break
        dive = ease_in_out(clamp((t - b["dive"]) / 0.8))
        y = lerp(360, self.sea_y(x) - 24, dive)
        return x, y, dive

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx, (0.03, 0.03, 0.06), (0.02, 0.02, 0.03))
        for i in range(40):  # stars
            circle(ctx, rnd(i, 21) * W, 180 + rnd(i, 23) * 500, 1.5 + 2 * rnd(i, 25), INK, 0.25 + 0.3 * rnd(i, 27))
        xt = self.tangent_x()
        mx, my = self.MAST
        sea = [(x, self.sea_y(x)) for x in range(0, W + 1, 12)]
        ctx.move_to(0, H)
        for p in sea:
            ctx.line_to(*p)
        ctx.line_to(W, H)
        ctx.close_path()
        g = cairo.LinearGradient(0, self.SEA0 - 40, 0, 1250)
        g.add_color_stop_rgb(0, 0.05, 0.2, 0.32)
        g.add_color_stop_rgb(1, 0.01, 0.04, 0.08)
        ctx.set_source(g)
        ctx.fill()
        for k in range(4):  # moving wave lines just under the surface
            pts = [(x, self.sea_y(x) + 14 + 22 * k + 5 * math.sin(x * 0.03 + t * 3 + k)) for x in range(0, W + 1, 16)]
            line(ctx, pts, SEA_BLUE, 2, 0.35 - 0.07 * k)
        line(ctx, sea, TEAL, 3, 0.8)
        # radar line of sight from the mast, grazing the sea at the horizon and running on beyond it
        ty = self.sea_y(xt)
        slope = (ty - my) / (xt - mx)
        far = (0, my + slope * (0 - mx))
        pulse = 0.5 + 0.5 * math.sin(t * 6) if t > b["radar"] else 0.3
        ctx.move_to(mx, my)
        ctx.line_to(*far)
        ctx.line_to(0, far[1] - 260)
        ctx.close_path()
        rgba(ctx, AMBER, 0.08 + 0.08 * pulse)
        ctx.fill()
        line(ctx, [(mx, my), far], AMBER, 4, 0.75)
        ctx.move_to(*far)  # the shadow zone: under the line of sight, above the sea, beyond the horizon
        for x in range(0, xt + 1, 12):
            ctx.line_to(x, my + slope * (x - mx))
        for x in range(xt, -1, -12):
            ctx.line_to(x, self.sea_y(x))
        ctx.close_path()
        rgba(ctx, (0, 0, 0), 0.45)
        ctx.fill()
        if t > b["radar"]:
            ly = my + slope * (60 - mx)
            text(ctx, "RADAR KO NAHI DIKHTA ↓", 60, ly - 40, 30, AMBER, font=MONO, a=clamp((t - b["radar"]) / 0.4),
                 anchor="l")
            circle(ctx, xt, ty, 10, AMBER)
            text(ctx, "RADAR HORIZON", xt + 20, ty - 34, 26, AMBER, font=MONO, anchor="l")
        self.ship(ctx, t)
        x, y, dive = self.path(t, d, b, xt)
        nx, ny = self.path(t + 0.05, d, b, xt)[:2]
        ang = clamp(math.atan2(ny - y, nx - x), -0.6, 0.6)
        missile(ctx, x, y, 210, ang, t, label=False)
        u = t - b["ten"]
        if u > 0 and t < b["seen"]:
            sy = self.sea_y(x)
            k = ease_out_cubic(u / 0.3)
            line(ctx, [(x + 20, y + 14), (x + 20, lerp(y + 14, sy, k))], TEAL, 5)
            for yy in (y + 14, lerp(y + 14, sy, k)):
                line(ctx, [(x + 4, yy), (x + 36, yy)], TEAL, 5)
            tag(ctx, "~10 M", clamp(x + 40, 160, 860), y - 110, TEAL, u, size=50)
        u = t - b["seen"]
        if u > 0:
            ring = (t * 1.8) % 1
            ctx.arc(x, y, 30 + 60 * ring, 0, math.tau)
            rgba(ctx, RED, 0.9 * (1 - ring))
            ctx.set_line_width(5)
            ctx.stroke()
            k = ease_out_cubic(u / 0.4)
            yy = 600
            line(ctx, [(x, yy), (lerp(x, mx, k), yy)], RED, 6)
            for xx in (x, lerp(x, mx, k)):
                line(ctx, [(xx, yy - 18), (xx, yy + 18)], RED, 6)
            text(ctx, "~30 KM", lerp(x, mx, 0.5), yy - 34, 34, RED, font=MONO, a=k)
            tag(ctx, "DETECTED: ~30 KM", 540, 300, RED, u, size=48)
        u = t - b["pay"]
        if u > 0:
            stamp(ctx, 540, 470, u, -0.03, 720, 170, RED, [("30 KM = 30 SEC", 0, 104, INK)])

    def ship(self, ctx, t):
        x, y = self.SHIP_X, self.sea_y(self.SHIP_X)
        bob = 3 * math.sin(t * 2)
        ctx.move_to(x - 130, y - 22 + bob)
        ctx.line_to(x + 190, y - 22 + bob)
        ctx.line_to(x + 160, y + 14 + bob)
        ctx.line_to(x - 105, y + 14 + bob)
        ctx.close_path()
        rgba(ctx, hexc("#56606E"))
        ctx.fill()
        rrect(ctx, x - 50, y - 58 + bob, 120, 38, 6)
        rgba(ctx, hexc("#6B7584"))
        ctx.fill()
        mx, my = self.MAST
        line(ctx, [(mx, y - 58 + bob), (mx, my + bob)], hexc("#8A94A3"), 7)
        rrect(ctx, mx - 30, my - 8 + bob, 60, 14, 5)
        rgba(ctx, AMBER)
        ctx.fill()
        text(ctx, "SHIP", x + 105, y - 40 + bob, 24, INK, font=MONO, a=0.85)


class Made(Cued):
    """India + Russia flags; Brahmaputra + Moskva rivers meet and spell BRAHMOS; Philippines flag + EXPORT."""

    def beats(self, d):
        c = self.cue
        return {"jv": c("RUSS", d * 0.04), "nadi": c("NADIYON", d * 0.3), "names": c("BRAHMAPUTRA", d * 0.45),
                "ph": c("PHILIPPINES", d * 0.68)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["jv"], "pop"), (b["jv"] + 0.25, "pop"), (b["nadi"], "whoosh"),
                (b["names"] + 0.6, "dingdong"), (b["ph"], "boom"), (b["ph"] + 0.3, "kaching")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx)
        dim = 1 - 0.75 * clamp((t - b["ph"]) / 0.3)
        for k, (kind, x, name) in enumerate((("in", 110, "INDIA"), ("ru", 670, "RUSSIA"))):
            u = t - b["jv"] - 0.25 * k
            if u > 0:
                pop = ease_out_back(u / 0.35)
                ctx.save()
                ctx.translate(x + 150, 330)
                ctx.scale(pop, pop)
                ctx.translate(-x - 150, -330)
                flag(ctx, x, 240, 300, 190, kind, t, phase=k)
                text(ctx, name, x + 150, 480, 40, INK, font=MONO, a=dim)
                ctx.restore()
        if t > b["jv"] + 0.3:
            text(ctx, "+", 540, 335, 110, HI, font=CAPTION_FONT, bold=False, a=dim)
        u = t - b["nadi"]
        if u > 0:
            k = clamp(u / 1.1)
            meet = (540, 900)
            for sgn, start, name, part in ((-1, (150, 580), "BRAHMAPUTRA", "BRAHM"), (1, (930, 580), "MOSKVA", "MOS")):
                pts = [(lerp(start[0], meet[0], s) + sgn * 60 * math.sin(s * math.pi * 2.2), lerp(start[1], meet[1], s))
                       for s in [i / 30 for i in range(31)]]
                drawn, _ = partial(pts, k)
                line(ctx, drawn, SEA_BLUE, 26, 0.35 * dim)
                line(ctx, drawn, SEA_BLUE, 12, 0.95 * dim)
                if t > b["names"]:  # river name, with the letters that made it into BRAHMOS lit up
                    a = clamp((t - b["names"]) / 0.3) * dim
                    full_w = text_width(ctx, name, 52, font=CAPTION_FONT, bold=False)
                    left = 70 if sgn < 0 else W - 70 - full_w
                    text(ctx, name, left, 560, 52, INK, font=CAPTION_FONT, bold=False, anchor="l", a=a * 0.55)
                    text(ctx, part, left, 560, 52, HI, font=CAPTION_FONT, bold=False, anchor="l", a=a)
            u2 = t - b["names"] - 0.6
            if u2 > 0 and t < b["ph"] + 0.3:
                pop = ease_out_back(u2 / 0.35)
                ctx.save()
                ctx.translate(540, 1010)
                ctx.scale(pop, pop)
                glow(ctx, 0, 0, 260, HI, 0.35)
                text(ctx, "BRAHMOS", 0, 0, 150, HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=12)
                ctx.restore()
        u = t - b["ph"]
        if u > 0:
            pop = ease_out_back(u / 0.4)
            ctx.save()
            ctx.translate(540, 640)
            ctx.scale(pop, pop)
            ph_flag(ctx, -230, -140, 460, 260, t)
            ctx.restore()
            missile(ctx, lerp(-300, W + 300, clamp(u / 1.4)), 880, 300, -0.05, t, label=False)
            stamp(ctx, 540, 1030, u - 0.25, -0.03, 760, 170, HI,
                  [("EXPORT: PHILIPPINES", -14, 78, HI), ("2022 DEAL  •  DELIVERED 2024", 52, 32, INK)])


class Ask(Cued):
    """Dim radar sweep behind the comment-prompt card (Lego ending 'prompt')."""

    def beats(self, d):
        c = self.cue
        return {"q": c("AGLI", 0.05), "cmt": c("COMMENT", d * 0.45), "sub": c("SUBSCRIBE", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["q"] + 0.05, "pop"), (b["cmt"], "dingdong"), (b["cmt"] + 1.1, "pick"),
                (b["cmt"] + 2.2, "pick"), (b["sub"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        bg(ctx)
        scope(ctx, 540, 650, 470, t, a=0.35, labels=False)
        lego.ending(STORY, ctx, t, t - b["q"], t - b["cmt"], question=("AGLI KAHANI", "KIS MISSILE KI?"),
                    suggestions=("AGNI-V", "AKASH", "NIRBHAY", "PRALAY"), y=590)
        u = t - b["sub"]
        if u > 0:
            stamp(ctx, 500, 1030, u, -0.03, 760, 120, RED, [("SUBSCRIBE • REALITY SHIFT", 0, 56, INK)])


SCENE_CLASSES = {"scope": Scope, "speed": Speed, "skim": Skim, "made": Made, "ask": Ask}
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
        "Aawaz Se 3 Guna Tez: BrahMos Ko Rokna Kyun Mushkil?",
        "BrahMos Ko Rokna Kyun Mushkil? Sirf 30 Second Milte Hain",
        "BrahMos Missile: Samudra Se Sirf 10 Meter Upar 😳",
        "Radar Pe Dikhi Toh Bas 30 Second: BrahMos Ki Asli Chaal",
        "BrahMos Speed: Delhi Se Agra Sirf 3 Minute Mein",
        "Mach 2.8 BrahMos: Jahaaz Ke Paas Kitna Time Bachta Hai?",
        "BrahMos Ka Naam Kahan Se Aaya? Brahmaputra + Moskva",
        "Philippines Ne Bharat Se BrahMos Kyun Khareeda?",
        "BrahMos Missile Hindi: Radar Se Kaise Bachti Hai?",
        "1 KM Har Second: Bharat Ki BrahMos Missile",
    ],
    "title": "Aawaz Se 3 Guna Tez: BrahMos Ko Rokna Kyun Mushkil?",   # creator's pick, still scored
    "thumb_text": "SIRF 30 SECOND",
    "queries": ["brahmos missile", "brahmos speed", "brahmos missile hindi"],
    "description": """
BrahMos missile ki speed aawaz se lagbhag 3 guna (Mach 2.8) hai, yaani har second kareeb 1 KM.
BrahMos missile hindi me: aakhri hisse me ye samudra se sirf ~10 meter upar udti hai, isliye jahaaz ka radar ise der se dekhta hai.

Is Short me:
• BrahMos speed: Mach 2.8, Delhi se Agra jitni doori kareeb 3 minute me
• Sea-skimming: ~10 meter ki oonchai aur radar horizon (~30 KM)
• 30 KM ÷ ~1 KM/second = ~30 second, bas itna time milta hai
• Bharat (DRDO) + Russia ka joint venture, naam Brahmaputra + Moskva nadi se
• Philippines ne 2022 me BrahMos khareedi, delivery 2024 me hui

Agli kahani kis missile ki chahiye? Naam comment me likho.
Aisi aur defence stories ke liye Reality Shift ko subscribe karo.

Note: animation schematic hai, scale pe nahi. 30 second ek seedha hisaab hai (30 KM ÷ ~1 KM/s), official spec nahi.
""",
    "tags": ["brahmos", "brahmos missile", "brahmos speed", "brahmos missile hindi", "supersonic cruise missile",
             "indian missile", "indian navy", "drdo", "india russia", "brahmos philippines", "sea skimming missile",
             "indian defence shorts", "defence hindi", "mach 2.8", "reality shift"],
    "hashtags": ["#Shorts", "#BrahMos", "#IndianDefence"],
}


def thumbnail(ctx):
    """1080x1920 cover: SIRF 30 / SECOND over a radar scope with the missile streaking at the ship."""
    bg(ctx)
    scope(ctx, 540, 1180, 520, 0.7, labels=False)
    ship_icon(ctx, 540, 1180, 2.2, TEAL)
    for j in range(14):
        rr = 520 * (0.95 - 0.04 * j)
        circle(ctx, 540 + rr * math.cos(-2.35), 1180 + rr * math.sin(-2.35), 18 - j, RED, 0.85 * (1 - j / 14))
    missile(ctx, 520, 860, 900, 0.38, 0.2)
    g = cairo.LinearGradient(0, 0, 0, 820)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.95)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 820)
    ctx.set_source(g)
    ctx.fill()
    vignette(ctx)
    glow(ctx, 540, 420, 560, RED, 0.25)
    text(ctx, "SIRF 30", 540, 310, 240, INK, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "SECOND", 540, 560, 250, RED, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=24)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, INK, a=0.7)


def main() -> None:
    import upload_kit
    story = importlib.import_module("generate_brahmos_lego_short")
    engine.make_frame = lego.frame_maker(story)
    final = engine.render(story, "edge")
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
