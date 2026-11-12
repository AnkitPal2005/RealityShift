"""Story: Reality Shift Short 2 — Defence & global power of Bharat (Modi ji ka vision)."""

import math

import cairo

from core.engine import *  # noqa: F401,F403
from shorts.reality_shift import (CAMO, FACE, GOLD, SAFFRON, TRICOLOR, _ellipse, embers, flag, globe, hero,
                                   mountains, stamp, subscribe_badge)

TOPIC = "BHARAT KI TAAKAT"
OUTPUTS = {"edge": "reality_shift_short2_defense.mp4", "elevenlabs": "reality_shift_short2_defense_el.mp4"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.3
TAIL_PAD = 0.0
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 108
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+5%"
EDGE_PITCH = "+0Hz"
HOT_COLOR = GOLD  # yellow/white kinetic type on the dark theme

NARRATION = {
    "hook": "एक वक्त था जब भारत अपनी सुरक्षा के लिए दूसरों के सामने हाथ फैलाता था... लेकिन आज? "
            "आज का नया भारत आंख झुकाकर नहीं, आंख मिलाकर बात करता है!",
    "make": "पहला— मोदी जी के एक विजन ने भारत को आयातक से निर्यातक बना दिया! आज तेजस लड़ाकू विमान, "
            "आईएनएस विक्रांत, और ब्रह्मोस जैसी मिसाइलें भारत खुद बना रहा है, और दुनिया हमसे खरीद रही है!",
    "resolve": "दूसरा— चाहे रूस-यूक्रेन युद्ध हो या महाशक्तियों का दबाव, कोई भी ताकत भारत को अपनी शर्तों पर "
               "नहीं झुका सकी। जहां बड़े-बड़े देश झुक गए, वहां मोदी जी ने सिर्फ और सिर्फ अपने देश का हित देखा!",
    "strike": "तीसरा— सर्जिकल स्ट्राइक से लेकर लाल आंख दिखाने तक, पूरी दुनिया को संदेश साफ है: अगर भारत को "
              "छेड़ा, तो घर में घुसकर जवाब मिलेगा!",
    "outro": "क्या आपको भी गर्व है आज के इस आत्मनिर्भर और मजबूत भारत पर? कमेंट में 'जय हिंद' जरूर लिखें, "
             "और इस नए भारत की ताकत देखने के लिए रियलिटी शिफ्ट को अभी सब्सक्राइब करें!",
}

CHUNKS = {
    "hook": [
        ("एक वक्त था", "EK WAQT THA"),
        ("जब भारत", "JAB BHARAT"),
        ("अपनी सुरक्षा के लिए", "APNI SURAKSHA KE LIYE"),
        ("दूसरों के सामने", "DOOSRON KE SAAMNE"),
        ("हाथ फैलाता था...", "HAATH FAILATA THA..."),
        ("लेकिन आज?", "LEKIN AAJ?"),
        ("आज का नया भारत", "AAJ KA NAYA BHARAT"),
        ("आंख झुकाकर नहीं,", "AANKH JHUKAKAR NAHI"),
        ("आंख मिलाकर", "AANKH MILAKAR"),
        ("बात करता है!", "BAAT KARTA HAI!"),
    ],
    "make": [
        ("पहला—", "PEHLA!"),
        ("मोदी जी के", "MODI JI KE"),
        ("एक विजन ने", "EK VISION NE"),
        ("भारत को आयातक से", "BHARAT KO AAYATAK SE"),
        ("निर्यातक बना दिया!", "NIRYATAK BANA DIYA!"),
        ("आज तेजस", "AAJ TEJAS"),
        ("लड़ाकू विमान,", "LADAKU VIMAAN"),
        ("आईएनएस विक्रांत,", "INS VIKRANT"),
        ("और ब्रह्मोस", "AUR BRAHMOS"),
        ("जैसी मिसाइलें", "JAISI MISSILES"),
        ("भारत खुद", "BHARAT KHUD"),
        ("बना रहा है,", "BANA RAHA HAI"),
        ("और दुनिया", "AUR DUNIYA"),
        ("हमसे खरीद रही है!", "HUMSE KHAREED RAHI HAI!"),
    ],
    "resolve": [
        ("दूसरा—", "DOOSRA!"),
        ("चाहे रूस-यूक्रेन", "CHAHE RUSSIA-UKRAINE"),
        ("युद्ध हो", "YUDDH HO"),
        ("या महाशक्तियों का", "YA MAHASHAKTIYON KA"),
        ("दबाव,", "DABAV"),
        ("कोई भी ताकत", "KOI BHI TAAKAT"),
        ("भारत को अपनी", "BHARAT KO APNI"),
        ("शर्तों पर", "SHARTON PAR"),
        ("नहीं झुका सकी।", "NAHI JHUKA SAKI!"),
        ("जहां बड़े-बड़े देश", "JAHAN BADE-BADE DESH"),
        ("झुक गए,", "JHUK GAYE"),
        ("वहां मोदी जी ने", "WAHAN MODI JI NE"),
        ("सिर्फ और सिर्फ", "SIRF AUR SIRF"),
        ("अपने देश का", "APNE DESH KA"),
        ("हित देखा!", "HIT DEKHA!"),
    ],
    "strike": [
        ("तीसरा—", "TEESRA!"),
        ("सर्जिकल स्ट्राइक से", "SURGICAL STRIKE SE"),
        ("लेकर लाल आंख", "LEKAR LAAL AANKH"),
        ("दिखाने तक,", "DIKHANE TAK"),
        ("पूरी दुनिया को", "POORI DUNIYA KO"),
        ("संदेश साफ है:", "SANDESH SAAF HAI:"),
        ("अगर भारत को", "AGAR BHARAT KO"),
        ("छेड़ा,", "CHHEDA"),
        ("तो घर में", "TO GHAR MEIN"),
        ("घुसकर जवाब मिलेगा!", "GHUSKAR JAWAB MILEGA!"),
    ],
    "outro": [
        ("क्या आपको भी", "KYA AAPKO BHI"),
        ("गर्व है", "GARV HAI"),
        ("आज के इस", "AAJ KE IS"),
        ("आत्मनिर्भर", "AATMANIRBHAR"),
        ("और मजबूत भारत पर?", "AUR MAZBOOT BHARAT PAR?"),
        ("कमेंट में", "COMMENT MEIN"),
        ("'जय हिंद'", "'JAI HIND'"),
        ("जरूर लिखें,", "ZAROOR LIKHEIN"),
        ("और इस नए भारत की", "AUR IS NAYE BHARAT KI"),
        ("ताकत देखने के लिए", "TAAKAT DEKHNE KE LIYE"),
        ("रियलिटी शिफ्ट को", "REALITY SHIFT KO"),
        ("अभी सब्सक्राइब करें!", "ABHI SUBSCRIBE KAREIN!"),
    ],
}

HOT_WORDS = {"SURAKSHA", "NAYA", "MILAKAR", "NIRYATAK", "TEJAS", "VIKRANT", "BRAHMOS", "KHUD", "DABAV",
             "JHUKA", "HIT", "SURGICAL", "STRIKE", "LAAL", "JAWAB", "AATMANIRBHAR", "JAI", "HIND", "SUBSCRIBE"}

for _key, _chunks in CHUNKS.items():
    assert " ".join(h for h, _ in _chunks) == NARRATION[_key], f"caption chunks drift from narration: {_key}"

SCRIPT = [(key, CHUNKS[key]) for key in NARRATION]

RED = hexc("#FF3B3B")
OLIVE = hexc("#4B5320")
STEEL = hexc("#8C96A6")
SEPIA = hexc("#B59A6A")


class Cued:
    """Scenes time their beats to the narration: cue(key) is the start of the first caption containing key."""

    def cue(self, key, default):
        for s in SCENES:
            if s["obj"] is self:
                return next((st for st, cap in s["captions"] if key in cap), default)
        return default


def hero_point(x, y, s, t, d, zoom, lx, ly):
    """World position of portrait-local point (lx, ly), following hero()'s push-in, float and breathing."""
    kb = zoom * (1 + 0.08 * ease_in_out(t / max(d, 0.1)))
    bob = 9 * math.sin(t * 1.6)
    breathe = 1 + 0.012 * math.sin(t * 2.3)
    return x + kb * lx * s, y + bob + 400 * s + kb * breathe * (ly - 400) * s


def glint(ctx, x, y, r, c, a=1.0):
    glow(ctx, x, y, r, c, 0.7 * a)
    for ang, ln in ((0, 1.7), (math.pi / 2, 1.7), (math.pi / 4, 0.6), (-math.pi / 4, 0.6)):
        dx, dy = r * ln * math.cos(ang), r * ln * math.sin(ang)
        line(ctx, [(x - dx, y - dy), (x + dx, y + dy)], (1, 1, 1), max(1.5, r * 0.06), a)


def gold_edge(ctx):
    """Glowing gold rim along the current path (path is consumed)."""
    rgba(ctx, GOLD, 0.25)
    ctx.set_line_width(14)
    ctx.stroke_preserve()
    rgba(ctx, GOLD, 0.95)
    ctx.set_line_width(3)
    ctx.stroke()


def flash(ctx, u, dur=0.25, a=0.6):
    if 0 <= u < dur:
        rgba(ctx, (1, 1, 1), a * (1 - u / dur))
        ctx.paint()


def label(ctx, s, x, y, u, size=58, c=GOLD):
    """Gold-bordered name plate that pops in (u = seconds since cue)."""
    if u < 0:
        return
    pop = ease_out_back(u / 0.3)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(pop, pop)
    w = text_width(ctx, s, size, font=CAPTION_FONT, bold=False) + 60
    rrect(ctx, -w / 2, -size * 0.7, w, size * 1.4, 14)
    rgba(ctx, (0.02, 0.02, 0.04), 0.82)
    ctx.fill_preserve()
    rgba(ctx, c)
    ctx.set_line_width(4)
    ctx.stroke()
    text(ctx, s, 0, 0, size, c, font=CAPTION_FONT, bold=False)
    ctx.restore()


# ============================================================ hardware

def tejas(ctx, x, y, s, rot, t, burner=1.0):
    """Plan view of the Tejas compound-delta fighter, nose along +x, with IAF roundels and afterburner."""
    half = [(215, 0), (185, -10), (140, -20), (70, -26), (30, -34), (-40, -92), (-128, -160), (-150, -162),
            (-150, -42), (-172, -30), (-186, -16)]
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    if burner:
        f = burner * (1 + 0.2 * math.sin(t * 40))
        glow(ctx, -200, 0, 110 * f, hexc("#FF8A1F"), 0.8)
        ctx.move_to(-186, -15)
        ctx.line_to(-186 - 150 * f, 0)
        ctx.line_to(-186, 15)
        ctx.close_path()
        rgba(ctx, hexc("#FFD36E"), 0.9)
        ctx.fill()
    glow(ctx, 0, 0, 260, GOLD, 0.18)

    def outline():
        ctx.move_to(*half[0])
        for p in half[1:]:
            ctx.line_to(*p)
        for px, py in reversed(half[1:]):
            ctx.line_to(px, -py)
        ctx.close_path()

    outline()
    g = cairo.LinearGradient(0, -160, 0, 160)
    g.add_color_stop_rgb(0, *hexc("#B9C2CF"))
    g.add_color_stop_rgb(0.5, *hexc("#7D8796"))
    g.add_color_stop_rgb(1, *hexc("#4C5563"))
    ctx.set_source(g)
    ctx.fill()
    outline()
    gold_edge(ctx)
    line(ctx, [(-40, 0), (-186, 0)], hexc("#3A414D"), 9)          # fin seen from above
    _ellipse(ctx, 118, 0, 40, 11)                                   # canopy
    rgba(ctx, hexc("#16243F"))
    ctx.fill()
    line(ctx, [(100, -4), (140, -4)], (1, 1, 1), 3, 0.6)
    for side in (-1, 1):                                            # roundels
        for r, c in zip((17, 11, 5), (SAFFRON, (1, 1, 1), hexc("#138808"))):
            circle(ctx, -95, side * 98, r, c)
    ctx.restore()


def brahmos(ctx, x, y, s, t, burn=1.0):
    """Vertical BrahMos missile with its nose at (x, y - 420 s) and the nozzle at (x, y)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if burn:
        f = burn * (1 + 0.25 * math.sin(t * 50))
        glow(ctx, 0, 40, 160 * f, hexc("#FF8A1F"), 0.85)
        ctx.move_to(-24, 0)
        ctx.curve_to(-30, 90 * f, -6, 200 * f, 0, 240 * f)
        ctx.curve_to(6, 200 * f, 30, 90 * f, 24, 0)
        ctx.close_path()
        rgba(ctx, hexc("#FFE08A"), 0.95)
        ctx.fill()
    glow(ctx, 0, -200, 230, GOLD, 0.2)

    def body():
        ctx.move_to(-28, 0)
        ctx.line_to(-28, -330)
        ctx.curve_to(-28, -380, -10, -415, 0, -425)
        ctx.curve_to(10, -415, 28, -380, 28, -330)
        ctx.line_to(28, 0)
        ctx.close_path()

    for side in (-1, 1):                                            # tail fins + mid wings
        ctx.move_to(side * 26, -10)
        ctx.line_to(side * 72, 0)
        ctx.line_to(side * 72, -30)
        ctx.line_to(side * 26, -95)
        ctx.close_path()
        ctx.move_to(side * 26, -170)
        ctx.line_to(side * 52, -190)
        ctx.line_to(side * 26, -245)
        ctx.close_path()
    rgba(ctx, hexc("#9AA3B0"))
    ctx.fill()
    body()
    g = cairo.LinearGradient(-28, 0, 28, 0)
    g.add_color_stop_rgb(0, *hexc("#C9CED6"))
    g.add_color_stop_rgb(0.45, *hexc("#FFFFFF"))
    g.add_color_stop_rgb(1, *hexc("#8E96A3"))
    ctx.set_source(g)
    ctx.fill()
    body()
    gold_edge(ctx)
    ctx.rectangle(-28, -360, 56, 16)
    rgba(ctx, SAFFRON)
    ctx.fill()
    ctx.save()
    ctx.translate(0, -200)
    ctx.rotate(-math.pi / 2)
    text(ctx, "BRAHMOS", 0, 0, 30, hexc("#1A2340"), font=CAPTION_FONT, bold=False)
    ctx.restore()
    ctx.restore()


def vikrant(ctx, x, y, s, t):
    """INS Vikrant side-on, bow to the right with its ski-jump, (x, y) at the waterline."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    def hull():
        ctx.move_to(-470, -60)
        ctx.line_to(370, -60)
        ctx.curve_to(410, -62, 440, -80, 470, -104)                # ski-jump
        ctx.line_to(490, -98)
        ctx.curve_to(470, -30, 440, 10, 420, 30)
        ctx.line_to(-440, 30)
        ctx.line_to(-480, -40)
        ctx.close_path()

    # island superstructure
    for bx, by, bw, bh in ((40, -150, 150, 92), (60, -210, 110, 64), (85, -260, 60, 54)):
        ctx.rectangle(bx, by, bw, bh)
        rgba(ctx, hexc("#5E6878"))
        ctx.fill()
        line(ctx, [(bx, by), (bx + bw, by)], GOLD, 3, 0.8)
    line(ctx, [(115, -260), (115, -340)], hexc("#AAB2C0"), 5)
    ctx.save()                                                      # spinning radar
    ctx.translate(115, -340)
    ctx.scale(abs(math.cos(t * 3)) + 0.05, 1)
    line(ctx, [(-34, 0), (34, 0)], hexc("#DDE3EC"), 7)
    ctx.restore()
    for k in range(4):                                              # bridge windows
        ctx.rectangle(70 + k * 26, -196, 16, 10)
    rgba(ctx, hexc("#FFE08A"), 0.9)
    ctx.fill()
    for k, jx in enumerate((-380, -270, -160, 260)):                # parked jets on deck
        ctx.move_to(jx - 34, -60)
        ctx.line_to(jx + 34, -60)
        ctx.line_to(jx + 22, -72)
        ctx.line_to(jx - 20, -74)
        ctx.close_path()
        rgba(ctx, hexc("#717B8A"))
        ctx.fill()
    hull()
    g = cairo.LinearGradient(0, -100, 0, 30)
    g.add_color_stop_rgb(0, *hexc("#6D7685"))
    g.add_color_stop_rgb(1, *hexc("#242A33"))
    ctx.set_source(g)
    ctx.fill()
    hull()
    gold_edge(ctx)
    line(ctx, [(-470, -42), (380, -42)], hexc("#3A414D"), 4)
    text(ctx, "R11", 380, -15, 42, (1, 1, 1), font=CAPTION_FONT, bold=False)
    ctx.restore()


def sea(ctx, top, t):
    g = cairo.LinearGradient(0, top, 0, H)
    g.add_color_stop_rgb(0, *hexc("#0E2340"))
    g.add_color_stop_rgb(1, *hexc("#01050C"))
    ctx.rectangle(0, top, W, H - top)
    ctx.set_source(g)
    ctx.fill()
    for i in range(28):  # gold glints on the swell
        y = top + 20 + (H - top) * rnd(i, 1) ** 1.6
        x = (rnd(i, 2) * W + t * 40 * (1 + rnd(i, 3))) % (W + 200) - 100
        ln = 40 + 90 * rnd(i, 4)
        line(ctx, [(x, y), (x + ln, y)], GOLD, 3, 0.15 + 0.35 * abs(math.sin(t * 2 + i)))


def smoke_trail(ctx, x, y0, y1, t):
    """Billowing exhaust column from y0 (ground) up to y1 (missile), lit gold near the flame."""
    if y1 >= y0:
        return
    n = int((y0 - y1) / 28)
    for k in range(n):
        u = k / max(n, 1)
        yy = y0 - (y0 - y1) * u
        r = 26 + 60 * (1 - u) + 10 * math.sin(k * 1.7 + t * 2)
        c = shade(GOLD, 0.9) if u > 0.85 else (0.55, 0.55, 0.6)
        circle(ctx, x + 14 * math.sin(k * 0.9 + t), yy, r, c, 0.10 + 0.12 * u)


def export_arcs(ctx, ox, oy, u):
    """Golden export routes fanning out from (ox, oy), drawn on over u seconds, with travelling dots."""
    dests = ((90, 330), (990, 300), (70, 1080), (1010, 1100), (540, 250))
    for k, (dx, dy) in enumerate(dests):
        v = ease_out_cubic((u - k * 0.12) / 0.7)
        if v <= 0:
            continue
        cx, cy = (ox + dx) / 2, min(oy, dy) - 260
        pts = []
        for i in range(31):
            w = i / 30 * v
            pts.append(((1 - w) ** 2 * ox + 2 * (1 - w) * w * cx + w * w * dx,
                        (1 - w) ** 2 * oy + 2 * (1 - w) * w * cy + w * w * dy))
        line(ctx, pts, GOLD, 12, 0.2)
        line(ctx, pts, GOLD, 4, 0.95)
        glow(ctx, *pts[-1], 40, GOLD, 0.8)
        circle(ctx, *pts[-1], 8, (1, 1, 1))


# ============================================================ people

def jawan(ctx, x, y, s, salute, t, k=0):
    """Soldier in camouflage with combat helmet, (x, y) at the feet; salute 0 -> 1 raises the hand."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    glow(ctx, 0, -300, 320, GOLD, 0.16)
    for side in (-1, 1):
        line(ctx, [(side * 30, -210), (side * 34, -30)], CAMO[1], 48)
        rrect(ctx, side * 34 - 32, -36, 64, 36, 12)
        rgba(ctx, hexc("#111111"))
        ctx.fill()

    def torso():
        rrect(ctx, -80, -430, 160, 250, 44)

    torso()
    rgba(ctx, CAMO[0])
    ctx.fill()
    ctx.save()
    torso()
    ctx.clip()
    for i in range(10):
        _ellipse(ctx, -80 + 160 * rnd(i, k + 1), -430 + 250 * rnd(i, k + 2), 26, 14)
        rgba(ctx, CAMO[1 + i % 2])
        ctx.fill()
    ctx.restore()
    torso()
    gold_edge(ctx)
    line(ctx, [(-78, -215), (78, -215)], hexc("#2A2416"), 16)
    line(ctx, [(-74, -410), (-98, -310), (-90, -220)], CAMO[0], 40)  # arm at the side
    circle(ctx, -90, -214, 20, FACE)
    ctx.rectangle(-22, -470, 44, 50)
    rgba(ctx, FACE)
    ctx.fill()
    circle(ctx, 0, -500, 52, FACE)
    ctx.arc(0, -508, 60, math.pi, 2 * math.pi)                         # helmet
    rgba(ctx, OLIVE)
    ctx.fill()
    rrect(ctx, -68, -514, 136, 16, 8)
    rgba(ctx, shade(OLIVE, 0.75))
    ctx.fill()
    for side in (-1, 1):
        circle(ctx, side * 18, -494, 5, hexc("#2A1A12"))
    v = ease_out_back(salute, 1.4)
    el = (lerp(98, 168, v), lerp(-310, -470, v))
    hd = (lerp(90, 52, v), lerp(-220, -520, v))
    line(ctx, [(74, -410), el, hd], CAMO[0], 40)
    circle(ctx, *hd, 21, FACE)
    ctx.restore()


def bowing_figure(ctx, x, y, s, bow, c=(0.32, 0.34, 0.4)):
    """Faceless suited figure, (x, y) at the feet, bending forward from the hips by bow radians."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for side in (-1, 1):
        line(ctx, [(side * 22, -190), (side * 26, 0)], shade(c, 0.8), 40)
    ctx.translate(0, -190)
    ctx.rotate(bow)
    rrect(ctx, -60, -230, 120, 240, 40)
    rgba(ctx, c)
    ctx.fill()
    circle(ctx, 0, -280, 46, shade(c, 1.2))
    ctx.restore()


# ============================================================ scenes

class Hook(Cued):
    """Sepia past (hands held out, imported crates lowered in) -> flash -> gold portrait of the new Bharat."""
    accent = GOLD

    def turn(self, d):
        return self.cue("LEKIN", d * 0.5)

    def events(self, d):
        turn = self.turn(d)
        return [(0.02, "soft_thud"), (self.cue("HAATH", turn * 0.7), "thud"), (turn - 0.05, "boom"),
                (turn + 0.25, "whoosh"), (self.cue("MILAKAR", d * 0.8), "zap")]

    def draw(self, ctx, t, d):
        turn = self.turn(d)
        if t < turn:
            self.past(ctx, t)
        else:
            self.now(ctx, t - turn, d - turn, self.cue("MILAKAR", d * 0.8) - turn)

    def past(self, ctx, t):
        backdrop(ctx, hexc("#3B3226"), hexc("#0E0B08"), hexc("#8A7A5C"), 540, 760, t, motes=0)
        for k, (cx, delay) in enumerate(((290, 0.0), (790, 0.3), (540, 0.6))):  # crates lowered in on cables
            v = ease_out_cubic((t - delay) / 1.3)
            cy = lerp(-220, (560, 600, 820)[k], v) + 6 * math.sin(t * 2 + k)
            sway = 0.04 * math.sin(t * 1.7 + k)
            line(ctx, [(cx, -40), (cx, cy - 90)], hexc("#6E6250"), 5)
            ctx.save()
            ctx.translate(cx, cy)
            ctx.rotate(sway)
            rrect(ctx, -140, -90, 280, 180, 10)
            rgba(ctx, hexc("#7A6446"))
            ctx.fill()
            for yy in (-45, 0, 45):
                line(ctx, [(-140, yy), (140, yy)], hexc("#5A4A33"), 4)
            text(ctx, "IMPORT", 0, 0, 62, hexc("#2A2016"), font=CAPTION_FONT, bold=False)
            ctx.restore()
        rise = lerp(260, 0, ease_out_cubic(t / 1.6))
        hy = 1270 + rise
        for side in (-1, 1):  # two open palms held out, rising from the bottom
            line(ctx, [(540 + side * 300, H + 60), (540 + side * 95, hy + 150)], hexc("#5C5040"), 130)
            ctx.save()
            ctx.translate(540 + side * 85, hy)
            ctx.rotate(side * 0.28)
            rrect(ctx, -75, -60, 150, 160, 50)
            rgba(ctx, SEPIA)
            ctx.fill()
            for f in range(4):
                fx = side * (-52 + f * 35)
                line(ctx, [(fx, -40), (fx * 1.1, -150 + 12 * abs(f - 1.5))], SEPIA, 32)
            line(ctx, [(side * 70, 40), (side * 130, -40)], SEPIA, 34)
            ctx.restore()
        # old-film look: flicker, grain and scratches
        rgba(ctx, (0, 0, 0), 0.12 * rnd(int(t * 24), 3))
        ctx.paint()
        f = int(t * 24)
        for i in range(70):
            circle(ctx, rnd(i, f) * W, rnd(i, f + 0.5) * H, 1.5, (1, 0.95, 0.85), 0.25)
        for k in range(2):
            sx = rnd(f // 3, k + 9) * W
            line(ctx, [(sx, 0), (sx + 10, H)], (1, 0.95, 0.85), 2, 0.12)

    def now(self, ctx, u, d, eyes_at):
        backdrop(ctx, hexc("#1C1003"), hexc("#050200"), GOLD, 540, 640, u, motes=24)
        embers(ctx, u, 26, GOLD, seed=3)
        zoom = lerp(1.3, 1.0, ease_out_cubic(u / 0.5))
        hero(ctx, 540, 900, 0.92, u, d, zoom=zoom, pose="command", jacket=hexc("#1F2A44"))
        e = u - eyes_at
        if e > 0:  # eye-to-eye: twin glints and a shockwave ring
            a = clamp(1 - (e - 0.6) / 0.8) if e > 0.6 else 1.0
            for side in (-1, 1):
                ex, ey = hero_point(540, 900, 0.92, u, d, zoom, side * 38, -150)
                glint(ctx, ex, ey, 55 * ease_out_back(e / 0.25), GOLD, a)
            ring = ease_out_cubic(e / 0.7)
            ctx.arc(540, 760, 120 + 700 * ring, 0, math.tau)
            rgba(ctx, GOLD, 0.6 * (1 - ring))
            ctx.set_line_width(10)
            ctx.stroke()
        v = u - 0.15
        if v > 0:
            pop = ease_out_back(v / 0.3)
            ctx.save()
            ctx.translate(540, 330)
            ctx.scale(pop, pop)
            ctx.rotate(-0.03)
            glow(ctx, 0, 0, 340, SAFFRON, 0.4 + 0.15 * math.sin(u * 7))
            text(ctx, "AAJ KA", 0, -88, 60, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=8)
            text(ctx, "NAYA BHARAT", 0, 10, 128, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=14)
            for k, c in enumerate(TRICOLOR):
                ctx.rectangle(-330 + k * 220, 92, 220, 12)
                rgba(ctx, c)
                ctx.fill()
            ctx.restore()
        flash(ctx, u, 0.3, 0.85)


class Make(Cued):
    """Portrait + IMPORTER -> EXPORTER, then Tejas, INS Vikrant and BrahMos with golden accents,
    MADE IN INDIA and export routes fanning out to the world."""
    accent = GOLD

    def beats(self, d):
        c = self.cue
        return {"imp": c("AAYATAK", d * 0.15), "exp": c("NIRYATAK", d * 0.25), "tej": c("TEJAS", d * 0.35),
                "vik": c("VIKRANT", d * 0.48), "bra": c("BRAHMOS", d * 0.58), "khud": c("KHUD", d * 0.72),
                "world": c("DUNIYA", d * 0.84)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["imp"], "thud"), (b["exp"] + 0.2, "kaching"), (b["tej"], "whoosh"),
                (b["vik"], "boom"), (b["bra"], "boom"), (b["bra"] + 0.1, "whoosh"), (b["khud"], "thud"),
                (b["world"], "zap")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        if t < b["tej"]:
            self.vision(ctx, t, d, b)
        else:
            self.arsenal(ctx, t, d, b)

    def vision(self, ctx, t, d, b):
        backdrop(ctx, hexc("#1A1206"), hexc("#040301"), SAFFRON, 540, 700, t, motes=30)
        embers(ctx, t, 20, GOLD, seed=5)
        hero(ctx, 540, 920, 0.9, t, b["tej"], pose="address", jacket=SAFFRON)
        u = t - b["imp"]
        if u > 0:
            pop = ease_out_back(u / 0.3)
            ctx.save()
            ctx.translate(540, 300)
            ctx.scale(pop, pop)
            text(ctx, "IMPORTER", 0, 0, 104, hexc("#9AA0AA"), font=CAPTION_FONT, bold=False,
                 stroke=(0, 0, 0), stroke_w=12)
            ctx.restore()
            v = t - b["exp"]
            if v > 0:
                k = ease_out_cubic(v / 0.18)
                line(ctx, [(300, 330), (lerp(300, 780, k), lerp(330, 270, k))], RED, 14)
        v = t - b["exp"] - 0.15
        if v > 0:
            stamp(ctx, 540, 470, v, -0.04, 640, 150, GOLD, [("EXPORTER", 0, 112, GOLD)])

    def arsenal(self, ctx, t, d, b):
        g = cairo.LinearGradient(0, 0, 0, 1200)
        g.add_color_stop_rgb(0, *hexc("#070B1E"))
        g.add_color_stop_rgb(1, *hexc("#1E1A2A"))
        ctx.set_source(g)
        ctx.paint()
        for i in range(70):
            circle(ctx, rnd(i, 1) * W, rnd(i, 2) * 1100, 1 + 2 * rnd(i, 3), (1, 1, 1),
                   0.25 + 0.4 * abs(math.sin(t * (1 + 2 * rnd(i, 4)) + i)))
        glow(ctx, 540, 1190, 820, SAFFRON, 0.45)                    # dawn on the horizon
        sea(ctx, 1190, t)
        # BrahMos rises from behind the horizon in slow motion
        u = t - b["bra"]
        if u > 0:
            my = 1190 - 60 - 380 * u - 40 * u * u
            smoke_trail(ctx, 230, 1190, my, t)
            brahmos(ctx, 230, my, 0.9, t)
            label(ctx, "BRAHMOS", 230, max(my - 470, 470), u - 0.3)
        # INS Vikrant sails in from the right
        u = t - b["vik"]
        if u > 0:
            vx = lerp(1700, 590, ease_out_cubic(u / 1.0))
            vikrant(ctx, vx, 1300 + 6 * math.sin(t * 1.5), 1.0, t)
            label(ctx, "INS VIKRANT", 700, 1440, u - 0.5)
        # Tejas streaks in and holds a hero shot top-right
        u = t - b["tej"]
        v = ease_out_cubic(u / 0.8)
        tx, ty = lerp(-300, 720, v), lerp(1150, 470, v) + 10 * math.sin(t * 2)
        tejas(ctx, tx, ty, 1.15, -0.62 + 0.03 * math.sin(t * 1.5), t)
        label(ctx, "TEJAS", 820, 700, u - 0.4)
        # MADE IN INDIA + exports to the world
        u = t - b["world"]
        if u > 0:
            export_arcs(ctx, 540, 900, u)
        u = t - b["khud"]
        if u > 0:
            stamp(ctx, 540, 900, u, -0.05, 700, 190, GOLD,
                  [("MADE IN INDIA", -16, 96, GOLD), ("AATMANIRBHAR BHARAT", 56, 40, (1, 1, 1))])
        flash(ctx, t - b["tej"])


class Resolve(Cued):
    """World forum: pressure arrows smash into a golden shield around the PM; others bow, India stands."""
    accent = hexc("#3AA0FF")
    SHIELD = (540, 780, 400)

    def beats(self, d):
        c = self.cue
        return {"war": c("RUSSIA", d * 0.08), "dabav": c("DABAV", d * 0.25), "hold": c("JHUKA", d * 0.5),
                "bow": c("JHUK GAYE", d * 0.65), "first": c("HIT", d * 0.9)}

    def events(self, d):
        b = self.beats(d)
        hits = [(b["dabav"] + 0.55 + k * 0.42, "thud") for k in range(int((b["hold"] - b["dabav"]) / 0.42))]
        return [(0.02, "boom"), (b["war"], "beep"), (b["hold"] + 0.1, "boom"), (b["first"], "kaching")] + hits

    def draw(self, ctx, t, d):
        b = self.beats(d)
        backdrop(ctx, hexc("#050B24"), hexc("#01020A"), self.accent, 540, 700, t, motes=0)
        globe(ctx, 540, 640, 380, t)
        for sx in (120, 960):  # forum spotlights
            ctx.move_to(sx - 20, 0)
            ctx.line_to(sx + 20, 0)
            ctx.line_to(800, 1500)
            ctx.line_to(280, 1500)
            ctx.close_path()
            g = cairo.LinearGradient(sx, 0, 540, 1500)
            g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.2)
            g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0.0)
            ctx.set_source(g)
            ctx.fill()
        # other powers bow
        u = t - b["bow"]
        if u > 0:
            a = ease_out_cubic(u / 0.3)
            for k, (x, sc) in enumerate(((95, 0.7), (230, 0.6), (850, 0.6), (985, 0.7))):
                side = 1 if x < 540 else -1
                bowing_figure(ctx, x, 1560, sc * a, side * 0.75 * ease_out_cubic((u - 0.2 - 0.1 * k) / 0.6))
        hero(ctx, 540, 900, 0.88, t, d, pose="address", jacket=hexc("#1F2A55"))
        sx, sy, sr = self.SHIELD
        hold = t >= b["hold"]
        u = t - b["dabav"]
        hit = 0.0
        if u > 0 and not hold:
            for k in range(6):  # red pressure arrows pushing in from both sides
                side = -1 if k % 2 else 1
                phase = u * 1.2 - k * 0.17
                if phase < 0:
                    continue
                frac = phase % 1.0
                yy = (560, 820, 1060)[k // 2]
                reach = sr * math.sqrt(max(0.0, 1 - ((yy - sy) / sr) ** 2))
                tip = sx + side * lerp(900, reach, ease_out_cubic(frac / 0.55))
                a = 1.0 if frac < 0.55 else clamp(1 - (frac - 0.55) / 0.3)
                if 0.55 <= frac < 0.75:
                    hit = max(hit, 1 - (frac - 0.55) / 0.2)
                    for i in range(8):
                        ang = rnd(i, k) * math.tau
                        ln = 30 + 70 * (frac - 0.55) / 0.2
                        line(ctx, [(tip, yy), (tip + side * abs(ln * math.cos(ang)), yy + ln * math.sin(ang))],
                             GOLD, 4, a)
                ctx.save()
                ctx.translate(tip, yy)
                ctx.scale(side, 1)
                ctx.move_to(0, 0)
                ctx.line_to(70, -60)
                ctx.line_to(70, -24)
                ctx.line_to(330, -24)
                ctx.line_to(330, 24)
                ctx.line_to(70, 24)
                ctx.line_to(70, 60)
                ctx.close_path()
                rgba(ctx, RED, 0.9 * a)
                ctx.fill_preserve()
                rgba(ctx, (0, 0, 0), a)
                ctx.set_line_width(4)
                ctx.stroke()
                ctx.restore()
                text(ctx, "DABAV", tip + side * 205, yy, 38, (1, 1, 1), font=CAPTION_FONT, bold=False, a=a)
        if u > 0:  # golden shield ring, flaring on each hit and once more when it holds
            hf = clamp(1 - (t - b["hold"]) / 0.6) if hold else 0.0
            pulse = max(hit, hf)
            glow(ctx, sx, sy, sr * 1.15, GOLD, 0.12 + 0.3 * pulse)
            ctx.arc(sx, sy, sr + 30 * hf, 0, math.tau)
            rgba(ctx, GOLD, 0.45 + 0.5 * pulse)
            ctx.set_line_width(8 + 10 * pulse)
            ctx.stroke()
        # war news ticker
        u = t - b["war"]
        if 0 < u and t < b["hold"] + 0.4:
            slide = ease_out_cubic(u / 0.35)
            ctx.save()
            ctx.translate(lerp(-W, 0, slide), 0)
            ctx.rectangle(0, 250, W, 84)
            rgba(ctx, RED, 0.92)
            ctx.fill()
            ctx.rectangle(0, 250, 190, 84)
            rgba(ctx, (1, 1, 1))
            ctx.fill()
            text(ctx, "GLOBAL", 95, 292, 44, RED, font=CAPTION_FONT, bold=False)
            text(ctx, "RUSSIA-UKRAINE WAR", 620, 292, 56, (1, 1, 1), font=CAPTION_FONT, bold=False)
            ctx.restore()
        u = t - b["hold"] - 0.1
        if u > 0 and t < b["first"]:
            stamp(ctx, 540, 330, u, 0.04, 640, 150, GOLD, [("NAHI JHUKA!", 0, 104, GOLD)])
        u = t - b["first"]
        if u > 0:
            stamp(ctx, 540, 330, u, -0.04, 700, 190, GOLD,
                  [("INDIA FIRST", -14, 112, GOLD), ("SIRF DESH KA HIT", 62, 40, (1, 1, 1))])
            flag(ctx, 900, 250, 130, 86, "in", t, pole=120)


class Strike(Cued):
    """Night-ops HUD: PM in camouflage flanked by saluting jawans; SURGICAL STRIKE, red eyes, and the reply."""
    accent = RED

    def beats(self, d):
        c = self.cue
        return {"surg": c("SURGICAL", d * 0.08), "laal": c("LAAL", d * 0.25), "msg": c("SANDESH", d * 0.5),
                "chheda": c("CHHEDA", d * 0.7), "ghar": c("GHAR", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["surg"], "zap"), (b["surg"] + 0.2, "thud"), (b["laal"], "boom"),
                (b["msg"], "beep"), (b["chheda"], "alarm"), (b["ghar"], "boom"), (b["ghar"] + 0.45, "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        backdrop(ctx, hexc("#08160C"), hexc("#010402"), hexc("#22C55E"), 540, 600, t, motes=30)
        u = t - b["ghar"]
        if u > 0:  # retaliation lights up the far ridge
            for k, (x, at) in enumerate(((220, 0.0), (820, 0.45), (520, 0.8))):
                e = u - at
                if 0 < e < 1.4:
                    glow(ctx, x, 1000, 420 * ease_out_cubic(e / 0.4), hexc("#FF8A1F"), 0.8 * clamp(1 - e / 1.4))
        mountains(ctx, t)
        for i in range(12):  # HUD grid + scan line
            line(ctx, [(0, i * 160), (W, i * 160)], hexc("#22C55E"), 1, 0.08)
            line(ctx, [(i * 100, 0), (i * 100, H)], hexc("#22C55E"), 1, 0.06)
        sy = (t * 420) % H
        line(ctx, [(0, sy), (W, sy)], hexc("#22C55E"), 3, 0.25)
        zoom = 1.0
        hero(ctx, 540, 880, 0.86, t, d, zoom=zoom, pose="command", jacket=OLIVE, camo=True)
        for k, (x, s) in enumerate(((115, 0.72), (300, 0.62), (780, 0.62), (965, 0.72))):
            jawan(ctx, x, 1580 - 60 * (s < 0.7), s, ease_in_out((t - 0.3 - 0.15 * k) / 0.6), t, k)
        u = t - b["laal"]
        if u > 0:  # laal aankh: red eyes + red pulse over the frame
            a = clamp(u / 0.2) * (0.75 + 0.25 * math.sin(t * 10))
            for side in (-1, 1):
                ex, ey = hero_point(540, 880, 0.86, t, d, zoom, side * 38, -150)
                glow(ctx, ex, ey, 70, RED, 0.9 * a)
                circle(ctx, ex, ey, 10, (1, 0.85, 0.85), a)
            if u < b["msg"] - b["laal"]:
                rgba(ctx, RED, 0.18 * clamp(1 - u / 1.2) + 0.06)
                ctx.paint()
        u = t - b["msg"]
        if u > 0 and t < b["ghar"]:  # the message going out worldwide: radar rings
            for k in range(3):
                r = ((u * 0.9 + k / 3) % 1.0)
                ctx.arc(540, 760, 100 + 900 * r, 0, math.tau)
                rgba(ctx, GOLD, 0.5 * (1 - r))
                ctx.set_line_width(6)
                ctx.stroke()
        # stamps along the top, clear of the face
        u = t - b["surg"]
        if u > 0 and t < b["chheda"]:
            stamp(ctx, 540, 340, u, -0.05, 720, 160, GOLD, [("SURGICAL STRIKE", 0, 100, GOLD)])
            ctx.save()  # target reticle
            ctx.translate(890, 560)
            ctx.rotate(t * 2)
            r = lerp(200, 70, ease_out_cubic(u / 0.4))
            ctx.arc(0, 0, r, 0, math.tau)
            rgba(ctx, RED, 0.9)
            ctx.set_line_width(6)
            ctx.stroke()
            for k in range(4):
                a = k * math.pi / 2
                line(ctx, [(r * 0.6 * math.cos(a), r * 0.6 * math.sin(a)),
                           (r * 1.3 * math.cos(a), r * 1.3 * math.sin(a))], RED, 6)
            ctx.restore()
        u = t - b["chheda"]
        if u > 0 and t < b["ghar"]:
            blink = 1.0 if int(t * 6) % 2 else 0.55
            stamp(ctx, 540, 340, u, 0.04, 560, 150, RED, [("WARNING", 0, 104, shade(RED, blink))])
        u = t - b["ghar"]
        if u > 0:
            stamp(ctx, 540, 340, u, -0.04, 760, 200, GOLD,
                  [("GHAR MEIN GHUSKAR", -24, 86, GOLD), ("JAWAB!", 60, 56, (1, 1, 1))])
            flash(ctx, u, 0.2, 0.5)


class Outro(Cued):
    """Tejas trio trailing tricolor smoke, smiling portrait, COMMENT 'JAI HIND' and the subscribe click."""
    accent = SAFFRON

    def click(self, d):
        return min(d - 0.4, self.cue("SUBSCRIBE", d * 0.8) + 0.6)

    def events(self, d):
        return [(0.02, "boom"), (0.3, "whoosh"), (self.cue("JAI", d * 0.4), "dingdong"),
                (self.click(d), "pick"), (self.click(d) + 0.05, "pop")]

    def draw(self, ctx, t, d):
        backdrop(ctx, hexc("#2A1204"), hexc("#070301"), self.accent, 540, 760, t, motes=20)
        ctx.save()  # tricolor sunburst
        ctx.translate(540, 700)
        ctx.rotate(t * 0.2)
        for k in range(24):
            a = k / 24 * math.tau
            ctx.move_to(0, 0)
            ctx.arc(0, 0, 1500, a, a + math.tau / 48)
            ctx.close_path()
            rgba(ctx, TRICOLOR[k % 3], 0.07)
            ctx.fill()
        ctx.restore()
        jx = lerp(-260, 1500, clamp(t / 3.2))  # formation flypast, smoke lingers
        for k, c in enumerate(TRICOLOR):
            y = 540 + (k - 1) * 70
            x = jx - abs(k - 1) * 90
            ctx.rectangle(-50, y - 22, max(0.0, x - 120), 44)
            g = cairo.LinearGradient(-50, 0, x, 0)
            g.add_color_stop_rgba(0, *c, 0.25 * clamp(1 - (t - 3.2) / 4))
            g.add_color_stop_rgba(1, *c, 0.85 * clamp(1 - (t - 3.2) / 4))
            ctx.set_source(g)
            ctx.fill()
            if x < W + 300:
                tejas(ctx, x, y, 0.42, 0.0, t)
        hero(ctx, 540, 860, 0.9, t, d, pose="wave", smile=True)
        for i in range(40):  # tricolor confetti
            fy = (rnd(i, 1) * H + t * (220 + 160 * rnd(i, 2))) % H
            fx = rnd(i, 3) * W + 40 * math.sin(t * 2 + i)
            ctx.save()
            ctx.translate(fx, fy)
            ctx.rotate(t * (2 + 3 * rnd(i, 4)) + i)
            ctx.rectangle(-9, -5, 18, 10)
            rgba(ctx, TRICOLOR[i % 3], 0.9)
            ctx.fill()
            ctx.restore()
        u = t - self.cue("COMMENT", d * 0.35)
        if u > 0:
            pop = ease_out_back(u / 0.35) * (1 + 0.06 * math.sin(t * 8))
            ctx.save()
            ctx.translate(540, 310)
            ctx.scale(pop, pop)
            ctx.rotate(-0.03)
            glow(ctx, 0, 0, 380, SAFFRON, 0.35)
            text(ctx, "COMMENT", -80, -62, 72, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
                 stroke_w=10)
            text(ctx, "'JAI HIND'", -80, 40, 116, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
                 stroke_w=14)
            flag(ctx, 220, -40, 150, 100, "in", t, pole=150)
            ctx.restore()
        else:
            pop = ease_out_back(t / 0.35)
            ctx.save()
            ctx.translate(540, 320)
            ctx.scale(pop, pop)
            glow(ctx, 0, 0, 360, GOLD, 0.35)
            text(ctx, "AATMANIRBHAR", 0, -40, 104, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
                 stroke_w=12)
            text(ctx, "BHARAT", 0, 60, 80, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=10)
            ctx.restore()
        clicked = t >= self.click(d)
        bx, by = subscribe_badge(ctx, 540, 1440, t, clicked)
        cu = clamp((t - (self.click(d) - 0.8)) / 0.7)
        if cu > 0 and t < self.click(d) + 0.9:
            cx, cy = lerp(1040, bx + 20, ease_in_out(cu)), lerp(1620, by + 20, ease_in_out(cu))
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


SCENE_CLASSES = {"hook": Hook, "make": Make, "resolve": Resolve, "strike": Strike, "outro": Outro}
