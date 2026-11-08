"""Story: The ₹450 Popcorn Scam (mad-scientist edition)."""

import math

import cairo

from engine import *  # noqa: F401,F403

TOPIC = "THE ₹450 POPCORN SCAM"
OUTPUTS = {"edge": "viral_popcorn_edge.mp4", "elevenlabs": "viral_popcorn_short.mp4"}

# Manic delivery: the narration is sent to ElevenLabs verbatim (punctuation is the
# pacing guide), internal pauses are left untouched, and each scene lasts exactly as
# long as its trimmed narration clip.
CLEAN_PUNCTUATION = False
MAX_GAP = None          # don't shorten pauses inside the narration
TAIL_PAD = 0.0          # scene_duration = trimmed audio duration
# Conservative edge trim (~-44 dBFS, with generous padding) so soft first/last
# syllables and breath tails are never clipped.
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 118
EL_VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam: deep, energetic narrator
# lower stability keeps the dramatic swings without the words running together
EL_SETTINGS = {"stability": 0.38, "similarity_boost": 0.85, "style": 0.30}

# Exact narration per scene (sent to the TTS as-is).
NARRATION = {
    "lab": "Ruko! Kabhi socha hai... 10 rupaye ki makki ka popcorn, PVR mein 450 rupaye ka "
           "kyun milta hai? Ek chhota sa packet—aur aadhi jeb KHAALI!",
    "projector": "Tumhe lagta hai wo film se kama rahe hain? Bilkul galat! Movie ticket ka "
                 "80 percent paisa... Bollywood ke bade producers cheen kar le jaate hain!",
    "canteen": "Toh cinema hall zinda kaise hain? Inka ASLI dhandha movie dikhana nahi... "
               "balki CANTEEN chalana hai! Jahan margin 80 se 90 PERCENT hota hai!",
    "decoy": "Aur sabse ganda khel—Decoy Effect! Chhota tub 350 ka... aur bada tub 450 ka! "
             "Tumhara dimaag chillata hai—are 100 rupaye mein double mil raha hai! "
             "Aur tum unke jaal mein phas gaye!",
    "point": "Toh agli baar popcorn lene se pehle—ye video apne us dost ko share karo jo hamesha "
             "bada tub khareedta hai! Aur aise hi hidden dark secrets ke liye... "
             "AnkitArts ko abhi FOLLOW karo!",
}

# Kinetic-caption chunks: split only at spaces so " ".join(chunks) == NARRATION.
CHUNKS = {
    "lab": ["Ruko!", "Kabhi socha hai...", "10 rupaye ki", "makki ka popcorn,", "PVR mein",
            "450 rupaye ka", "kyun milta hai?", "Ek chhota sa", "packet—aur aadhi jeb", "KHAALI!"],
    "projector": ["Tumhe lagta hai", "wo film se", "kama rahe hain?", "Bilkul galat!", "Movie ticket ka",
                  "80 percent paisa...", "Bollywood ke", "bade producers", "cheen kar le jaate hain!"],
    "canteen": ["Toh cinema hall", "zinda kaise hain?", "Inka ASLI dhandha", "movie dikhana nahi...",
                "balki CANTEEN", "chalana hai!", "Jahan margin", "80 se 90 PERCENT", "hota hai!"],
    "decoy": ["Aur sabse ganda", "khel—Decoy Effect!", "Chhota tub 350 ka...", "aur bada tub 450 ka!",
              "Tumhara dimaag", "chillata hai—are", "100 rupaye mein", "double mil raha hai!",
              "Aur tum unke", "jaal mein phas gaye!"],
    "point": ["Toh agli baar", "popcorn lene se", "pehle—ye video", "apne us dost ko", "share karo",
              "jo hamesha", "bada tub khareedta hai!", "Aur aise hi", "hidden dark secrets",
              "ke liye...", "AnkitArts ko", "abhi FOLLOW karo!"],
}

# Words stressed in the narration: drawn in red with a slam-in pop on the captions.
HOT_WORDS = {"KHAALI", "ASLI", "CANTEEN", "PERCENT", "FOLLOW"}


def _caption(chunk: str) -> str:
    cap = chunk.upper()
    return cap[:-1] if cap.endswith((",", ".")) and not cap.endswith("...") else cap


for _key, _chunks in CHUNKS.items():
    assert " ".join(_chunks) == NARRATION[_key], f"caption chunks drift from narration: {_key}"

SCRIPT = [(key, [(c, _caption(c)) for c in CHUNKS[key]]) for key in NARRATION]

COAT = hexc("#EEF1F6")
COAT_SH = hexc("#B9C0CF")
HAIR = hexc("#F4F4F4")
SHIRT = hexc("#2B2D42")
GOLD = hexc("#FFD60A")
CASH = hexc("#22E06B")
POPCORN = hexc("#FFF3C4")
BUTTER = hexc("#F7C948")


# ============================================================ props & characters

def scientist(ctx, x, y, s, t, pose="hold", held=None):
    """Front-facing mad scientist with (x, y) at the neck base.
    pose: "hold" (arms cradle a prop drawn by held(ctx) in local coords) or "point"."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    # coat
    ctx.move_to(-90, 0)
    ctx.curve_to(-200, 10, -250, 60, -262, 160)
    ctx.line_to(-285, 760)
    ctx.line_to(285, 760)
    ctx.line_to(262, 160)
    ctx.curve_to(250, 60, 200, 10, 90, 0)
    ctx.close_path()
    rgba(ctx, COAT)
    ctx.fill()
    ctx.move_to(-80, 0)
    ctx.line_to(0, 270)
    ctx.line_to(80, 0)
    ctx.close_path()
    rgba(ctx, SHIRT)
    ctx.fill()
    ctx.move_to(0, 22)
    ctx.line_to(-20, 70)
    ctx.line_to(0, 240)
    ctx.line_to(20, 70)
    ctx.close_path()
    rgba(ctx, CASH)
    ctx.fill()
    for side in (-1, 1):
        line(ctx, [(side * 92, 4), (side * 22, 262), (side * 22, 760)], COAT_SH, 6)
    rrect(ctx, 120, 300, 95, 75, 8)
    rgba(ctx, COAT_SH)
    ctx.set_line_width(5)
    ctx.stroke()
    for k, col in enumerate(("#FF3B3B", "#2F80ED", "#FFD60A")):
        line(ctx, [(140 + k * 22, 300), (140 + k * 22, 268)], hexc(col), 9)
    # neck
    rrect(ctx, -38, -60, 76, 80, 20)
    rgba(ctx, shade(SKIN, 0.9))
    ctx.fill()

    # head (manic jitter)
    jit = 4 * math.sin(t * 23)
    hy = -195
    ctx.save()
    ctx.translate(jit, 0)
    ctx.rotate(0.04 * math.sin(t * 5))
    # wild hair
    spikes = 26
    ctx.new_path()
    for i in range(spikes + 1):
        a = math.pi * 0.82 + (math.pi * 1.36) * i / spikes
        L = 60 + 55 * rnd(i, 4) + 10 * math.sin(t * 9 + i)
        for da, r in ((-0.06, 112), (0.0, 112 + L), (0.06, 112)):
            px, py = math.cos(a + da) * r, hy - 10 + math.sin(a + da) * r * 1.05
            ctx.line_to(px, py)
    ctx.close_path()
    rgba(ctx, HAIR)
    ctx.fill_preserve()
    rgba(ctx, hexc("#A9AFBD"))
    ctx.set_line_width(4)
    ctx.stroke()
    for side in (-1, 1):
        circle(ctx, side * 122, hy + 10, 27, shade(SKIN, 0.9))
    ctx.save()
    ctx.translate(0, hy)
    ctx.scale(1, 1.14)
    ctx.arc(0, 0, 120, 0, math.tau)
    ctx.restore()
    rgba(ctx, SKIN)
    ctx.fill()
    # goggles on forehead
    rrect(ctx, -124, hy - 108, 248, 24, 8)
    rgba(ctx, hexc("#3A2A1E"))
    ctx.fill()
    for side in (-1, 1):
        circle(ctx, side * 52, hy - 96, 42, hexc("#B8862B"))
        g = cairo.RadialGradient(side * 52 - 10, hy - 106, 4, side * 52, hy - 96, 32)
        g.add_color_stop_rgb(0, 0.85, 1, 1)
        g.add_color_stop_rgb(1, 0.1, 0.75, 0.85)
        ctx.set_source(g)
        ctx.arc(side * 52, hy - 96, 32, 0, math.tau)
        ctx.fill()
    # eyebrows (bouncing)
    b = 10 * abs(math.sin(t * 6))
    for side in (-1, 1):
        line(ctx, [(side * 18, hy - 50 - b), (side * 88, hy - 72 - b * 1.4)], hexc("#E6E6E6"), 16)
    # wide eyes with darting pupils
    for side in (-1, 1):
        ex, ey = side * 48, hy - 18
        circle(ctx, ex, ey, 40, (1, 1, 1))
        ctx.arc(ex, ey, 40, 0, math.tau)
        rgba(ctx, (0.1, 0.1, 0.12))
        ctx.set_line_width(4)
        ctx.stroke()
        px = ex + 13 * math.sin(t * 11 + side * 1.3)
        py = ey + 9 * math.cos(t * 7 + side * 2.1)
        circle(ctx, px, py, 14, (0.08, 0.08, 0.1))
        circle(ctx, px + 4, py - 5, 4, (1, 1, 1))
    # nose
    ctx.save()
    ctx.translate(0, hy + 28)
    ctx.scale(1, 1.35)
    circle(ctx, 0, 0, 16, shade(SKIN, 0.82))
    ctx.restore()
    # manic grin
    op = 0.35 + 0.65 * abs(math.sin(t * 13))
    my = hy + 66
    ctx.move_to(-82, my)
    ctx.curve_to(-40, my + 18, 40, my + 18, 82, my)
    ctx.curve_to(52, my + 30 + 46 * op, -52, my + 30 + 46 * op, -82, my)
    ctx.close_path()
    rgba(ctx, hexc("#3A0D12"))
    ctx.fill_preserve()
    ctx.save()
    ctx.clip()
    ctx.rectangle(-90, my - 5, 180, 26)
    rgba(ctx, (1, 1, 1))
    ctx.fill()
    for k in range(-3, 4):
        line(ctx, [(k * 22, my - 5), (k * 22, my + 20)], (0.8, 0.8, 0.8), 2)
    ctx.restore()
    ctx.restore()

    # arms
    if pose == "hold":
        for side in (-1, 1):
            line(ctx, [(side * 232, 90), (side * 262, 380), (side * 140, 470)], COAT, 74)
            line(ctx, [(side * 232, 90), (side * 262, 380), (side * 140, 470)], COAT_SH, 2)
        if held:
            held(ctx)
        for side in (-1, 1):
            circle(ctx, side * 132, 462, 36, SKIN)
    else:
        line(ctx, [(-232, 90), (-310, 340), (-205, 450)], COAT, 74)
        circle(ctx, -200, 450, 36, SKIN)
        # right arm thrust toward the camera: big foreshortened fist, index finger at the viewer
        jab = 1 + 0.25 * max(0.0, math.sin(t * 9))
        line(ctx, [(232, 90), (250, 300), (120, 360)], COAT, 92)
        ctx.save()
        ctx.translate(60, 330)
        ctx.scale(jab, jab)
        for k in range(12):  # "at YOU" impact lines
            a = k / 12 * math.tau + 0.2
            line(ctx, [(-30 + 150 * math.cos(a), -95 + 150 * math.sin(a)),
                       (-30 + 205 * math.cos(a), -95 + 205 * math.sin(a))], GOLD, 9, 0.9)
        rrect(ctx, -105, -70, 190, 160, 70)  # fist
        rgba(ctx, SKIN)
        ctx.fill()
        for k in range(3):  # curled fingers
            rrect(ctx, -95 + k * 58, 30, 56, 62, 26)
            rgba(ctx, shade(SKIN, 0.92))
            ctx.fill_preserve()
            rgba(ctx, shade(SKIN, 0.7))
            ctx.set_line_width(4)
            ctx.stroke()
        line(ctx, [(70, 40), (40, -10)], shade(SKIN, 0.85), 40)  # thumb
        circle(ctx, -30, -95, 62, shade(SKIN, 1.06))  # foreshortened index finger
        ctx.arc(-30, -95, 62, 0, math.tau)
        rgba(ctx, shade(SKIN, 0.7))
        ctx.set_line_width(5)
        ctx.stroke()
        ctx.save()
        ctx.translate(-30, -118)
        ctx.scale(1, 0.62)
        circle(ctx, 0, 0, 30, hexc("#F3D2B4"))
        ctx.restore()
        ctx.restore()
    ctx.restore()


def tub(ctx, x, y, s, price, t, glow_c=None):
    """Striped popcorn tub, (x, y) = bottom centre."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if glow_c:
        glow(ctx, 0, -200, 380, glow_c, 0.5 + 0.15 * math.sin(t * 6))
    ctx.move_to(-130, -300)
    ctx.line_to(130, -300)
    ctx.line_to(95, 0)
    ctx.line_to(-95, 0)
    ctx.close_path()
    rgba(ctx, (1, 1, 1))
    ctx.fill_preserve()
    ctx.save()
    ctx.clip()
    for k in range(-6, 7, 2):
        ctx.rectangle(k * 22 - 11, -300, 22, 300)
        rgba(ctx, hexc("#E63946"))
        ctx.fill()
    ctx.restore()
    rrect(ctx, -142, -318, 284, 30, 10)
    rgba(ctx, hexc("#B5202D"))
    ctx.fill()
    for i in range(46):
        px = -125 + 250 * rnd(i, 1)
        py = -322 - 80 * rnd(i, 2) * (1 - abs(px) / 160) + 3 * math.sin(t * 8 + i)
        r = 20 + 11 * rnd(i, 3)
        circle(ctx, px, py, r, POPCORN)
        circle(ctx, px + r * 0.3, py + r * 0.3, r * 0.45, BUTTER, 0.7)
    rrect(ctx, -95, -205, 190, 92, 22)
    rgba(ctx, GOLD)
    ctx.fill()
    text(ctx, price, 0, -159, 66, (0.1, 0.1, 0.1), font=CAPTION_FONT)
    ctx.restore()


def ticket(ctx, x, y, s, rot, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    rrect(ctx, -60, -32, 120, 64, 8)
    ctx.arc(-60, 0, 14, 0, math.tau)
    ctx.new_sub_path()
    ctx.arc(60, 0, 14, 0, math.tau)
    rgba(ctx, GOLD, a)
    ctx.fill()
    ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    line(ctx, [(28, -26), (28, 26)], hexc("#B8860B"), 3, a)
    text(ctx, "₹", -8, 0, 40, hexc("#7A5200"), a=a)
    ctx.restore()


def banknote(ctx, x, y, s, rot, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    glow(ctx, 0, 0, 90, CASH, 0.35 * a)
    rrect(ctx, -60, -30, 120, 60, 6)
    rgba(ctx, hexc("#1FA855"), a)
    ctx.fill()
    rrect(ctx, -52, -22, 104, 44, 4)
    rgba(ctx, hexc("#9CF7C0"), 0.8 * a)
    ctx.set_line_width(3)
    ctx.stroke()
    text(ctx, "₹", 0, 0, 36, hexc("#E9FFF1"), a=a)
    ctx.restore()


def brain(ctx, x, y, s, t):
    ctx.save()
    ctx.translate(x, y)
    p = 1 + 0.05 * math.sin(t * 8)
    ctx.scale(s * p, s * p)
    pink = hexc("#FF8FB1")
    for i in range(11):
        a = i / 11 * math.tau
        circle(ctx, 95 * math.cos(a), 60 * math.sin(a) - 10, 62, pink)
    circle(ctx, 0, -10, 90, pink)
    ctx.save()
    ctx.arc(0, -10, 150, 0, math.tau)
    ctx.clip()
    for k in range(-3, 4):
        ctx.move_to(-150, k * 30 - 10)
        for xx in range(-150, 151, 15):
            ctx.line_to(xx, k * 30 - 10 + 10 * math.sin(xx / 14 + k * 1.7))
        rgba(ctx, hexc("#D9577F"))
        ctx.set_line_width(6)
        ctx.stroke()
    ctx.restore()
    line(ctx, [(0, -75), (0, 55)], hexc("#C2416A"), 8)
    ctx.restore()


def arrow_laser(ctx, x0, y0, x1, y1, t, c):
    ang = math.atan2(y1 - y0, x1 - x0)
    ex, ey = x1 - 40 * math.cos(ang), y1 - 40 * math.sin(ang)
    for w_, a_ in ((34, 0.12), (18, 0.25)):
        line(ctx, [(x0, y0), (ex, ey)], c, w_, a_)
    ctx.set_dash([34, 22], -t * 260)
    line(ctx, [(x0, y0), (ex, ey)], c, 10)
    ctx.set_dash([])
    ctx.save()
    ctx.translate(x1, y1)
    ctx.rotate(ang)
    ctx.move_to(0, 0)
    ctx.line_to(-60, -32)
    ctx.line_to(-60, 32)
    ctx.close_path()
    rgba(ctx, c)
    ctx.fill()
    ctx.restore()


def flask(ctx, x, y, s, liquid, t, seed):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(-18, -120)
    ctx.line_to(-18, -60)
    ctx.line_to(-70, 0)
    ctx.line_to(70, 0)
    ctx.line_to(18, -60)
    ctx.line_to(18, -120)
    ctx.close_path()
    rgba(ctx, (1, 1, 1), 0.12)
    ctx.fill_preserve()
    rgba(ctx, (1, 1, 1), 0.5)
    ctx.set_line_width(4)
    ctx.stroke()
    ctx.move_to(-45, -28)
    ctx.line_to(45, -28)
    ctx.line_to(66, -3)
    ctx.line_to(-66, -3)
    ctx.close_path()
    rgba(ctx, liquid, 0.85)
    ctx.fill()
    glow(ctx, 0, -20, 90, liquid, 0.35)
    for k in range(5):
        age = (t * 0.9 + rnd(seed * 7 + k, 1)) % 1
        circle(ctx, -20 + 40 * rnd(seed * 7 + k, 2), -30 - age * 140, 5 + 6 * age, liquid, 0.8 * (1 - age))
    ctx.restore()


def lab_backdrop(ctx, t, accent):
    backdrop(ctx, hexc("#1A0F2E"), hexc("#05030B"), accent, 540, 700, t)
    for sx in (60, 760):
        rrect(ctx, sx, 640, 260, 14, 4)
        rgba(ctx, hexc("#3B2F55"))
        ctx.fill()
        for k, col in enumerate(("#22E06B", "#B14CFF", "#00C2FF")):
            flask(ctx, sx + 50 + k * 80, 640, 0.55, hexc(col), t, sx + k)


# ============================================================ scenes

class Lab:
    accent = hexc("#B14CFF")
    POP = 0.32

    def events(self, d):
        return [(0.02, "boom")] + [(k * self.POP + 0.3, "pop") for k in range(int(d / self.POP))]

    def draw(self, ctx, t, d):
        lab_backdrop(ctx, t, self.accent)
        # lightning flicker behind
        if (t % 2.3) < 0.12:
            rgba(ctx, (0.85, 0.75, 1), 0.18)
            ctx.paint()
        # ₹10 corn cob -> ₹450 tub
        cy = 1010 + 18 * math.sin(t * 3)
        ctx.save()
        ctx.translate(170, cy)
        ctx.rotate(-0.3 + 0.1 * math.sin(t * 2))
        for side in (-1, 1):
            ctx.move_to(0, 90)
            ctx.curve_to(side * 70, 40, side * 60, -40, side * 20, -80)
            ctx.line_to(0, 60)
            ctx.close_path()
            rgba(ctx, hexc("#4CAF50"))
            ctx.fill()
        ctx.save()
        ctx.scale(0.55, 1)
        circle(ctx, 0, -10, 80, hexc("#FFC93C"))
        ctx.restore()
        for r_ in range(-4, 4):
            for c_ in (-1, 0, 1):
                circle(ctx, c_ * 20, r_ * 18 - 5, 7, hexc("#F2A900"))
        ctx.restore()
        rrect(ctx, 105, cy + 95, 130, 60, 30)
        rgba(ctx, (1, 1, 1))
        ctx.fill()
        text(ctx, "₹10", 170, cy + 125, 44, (0.1, 0.1, 0.1), font=CAPTION_FONT)

        def held(c):
            tub(c, 0, 470, 0.95, "₹450", t, glow_c=GOLD)

        scientist(ctx, 560, 770, 0.95, t, pose="hold", held=held)
        # kernels popping out of the tub
        tx, ty = 560, 770 + (470 - 330) * 0.95
        for k in range(14):
            age = (t - k * self.POP - 0.3)
            if 0 <= age < 0.9:
                vx = 260 * (rnd(k, 5) - 0.5) * 2
                px = tx + vx * age
                py = ty - 700 * age + 900 * age * age
                circle(ctx, px, py, 14, POPCORN)
                circle(ctx, px + 4, py + 4, 6, BUTTER)
        # x45 arrow
        ctx.set_dash([18, 14], -t * 120)
        ctx.move_to(250, cy - 40)
        ctx.curve_to(300, 860, 360, 860, 400, 900)
        rgba(ctx, GOLD)
        ctx.set_line_width(7)
        ctx.stroke()
        ctx.set_dash([])
        p = 1 + 0.12 * math.sin(t * 9)
        ctx.save()
        ctx.translate(250, 830)
        ctx.scale(p, p)
        ctx.rotate(-0.15)
        text(ctx, "x45!", 0, 0, 84, GOLD, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=10)
        ctx.restore()


class Projector:
    accent = hexc("#FFB020")
    EVERY = 0.38
    LENS, SPLIT = (400, 445), (610, 560)
    SCREEN, VAULT = (920, 420), (820, 1060)

    def tickets(self, d):
        return [k * self.EVERY for k in range(int(d / self.EVERY) + 1)]

    def events(self, d):
        return [(t0 + 1.1, "pick") for k, t0 in enumerate(self.tickets(d)) if k % 5 and t0 + 1.1 < d]

    def draw(self, ctx, t, d):
        backdrop(ctx, hexc("#120C06"), hexc("#040302"), self.accent, 600, 600, t, motes=20)
        # theatre screen
        rrect(ctx, 790, 300, 260, 160, 10)
        rgba(ctx, hexc("#DCE6FF"), 0.85)
        ctx.fill()
        text(ctx, "THEATRE", 920, 380, 40, hexc("#3B4A6B"))
        # beams
        lx, ly = self.LENS
        sx, sy = self.SPLIT
        for (tx, ty), half, a in ((self.SCREEN, 70, 0.18), (self.VAULT, 170, 0.32)):
            ctx.move_to(lx, ly - 18)
            ctx.line_to(sx, sy - 40)
            ctx.line_to(tx + half * 0.7, ty - half * 0.7)
            ctx.line_to(tx - half * 0.7, ty + half * 0.7)
            ctx.line_to(sx, sy + 40)
            ctx.line_to(lx, ly + 18)
            ctx.close_path()
            g = cairo.LinearGradient(lx, ly, tx, ty)
            g.add_color_stop_rgba(0, 1, 0.92, 0.6, a + 0.1 * math.sin(t * 20))
            g.add_color_stop_rgba(1, 1, 0.92, 0.6, a * 0.3)
            ctx.set_source(g)
            ctx.fill()
        # vault
        vx, vy = self.VAULT
        text(ctx, "BOLLYWOOD", vx, vy - 250, 70, GOLD, font=CAPTION_FONT, stroke=(0.3, 0.2, 0), stroke_w=8)
        circle(ctx, vx, vy, 200, hexc("#2A2F3A"))
        g = cairo.RadialGradient(vx - 60, vy - 60, 20, vx, vy, 190)
        g.add_color_stop_rgb(0, *hexc("#C9D1DE"))
        g.add_color_stop_rgb(1, *hexc("#6B7487"))
        ctx.set_source(g)
        ctx.arc(vx, vy, 180, 0, math.tau)
        ctx.fill()
        for k in range(16):
            a = k / 16 * math.tau
            circle(ctx, vx + 160 * math.cos(a), vy + 160 * math.sin(a), 8, hexc("#3A4150"))
        circle(ctx, vx, vy, 95, hexc("#8C95A8"))
        wheel = t * 2.2
        for k in range(3):
            a = wheel + k * math.tau / 3
            line(ctx, [(vx, vy), (vx + 85 * math.cos(a), vy + 85 * math.sin(a))], hexc("#2B2F3A"), 14)
            circle(ctx, vx + 85 * math.cos(a), vy + 85 * math.sin(a), 16, GOLD)
        circle(ctx, vx, vy, 26, GOLD)
        rrect(ctx, vx - 170, vy + 215, 340, 64, 12)
        rgba(ctx, hexc("#1A1D24"))
        ctx.fill()
        text(ctx, "DISTRIBUTOR VAULT", vx, vy + 247, 34, GOLD)
        # tickets travelling along the beam, most vanish into the vault
        for k, t0 in enumerate(self.tickets(d)):
            u = t - t0
            if u < 0 or u > 1.2:
                continue
            target = self.SCREEN if k % 5 == 0 else self.VAULT
            if u < 0.5:
                v = ease_in_out(u / 0.5)
                px, py = lerp(lx, sx, v), lerp(ly, sy, v)
                sc = 0.6 + 0.4 * v
            else:
                v = ease_in_out((u - 0.5) / 0.6)
                px, py = lerp(sx, target[0], v), lerp(sy, target[1], v)
                sc = 1.0 if v < 0.75 else (1 - v) * 4
            if sc < 0.03:
                continue
            ticket(ctx, px, py, sc, u * 6 + k, a=min(1, sc + 0.2))
        # projector + spinning reels
        for rx in (190, 330):
            circle(ctx, rx, 290, 78, hexc("#2B2F3A"))
            for k in range(5):
                a = t * 6 + k * math.tau / 5
                circle(ctx, rx + 44 * math.cos(a), 290 + 44 * math.sin(a), 15, hexc("#120C06"))
            circle(ctx, rx, 290, 14, hexc("#8C95A8"))
        rrect(ctx, 110, 360, 260, 160, 20)
        rgba(ctx, hexc("#3A3F4E"))
        ctx.fill()
        rrect(ctx, 360, 410, 50, 70, 10)
        rgba(ctx, hexc("#1A1D24"))
        ctx.fill()
        glow(ctx, lx, ly, 70, hexc("#FFF4C2"), 0.9)
        # audience silhouettes
        for k in range(8):
            hx = 70 + k * 135 + 10 * math.sin(t * 2 + k)
            circle(ctx, hx, 1440, 50, hexc("#0D0F17"))
            rrect(ctx, hx - 80, 1480, 160, 120, 50)
            rgba(ctx, hexc("#0D0F17"))
            ctx.fill()


class Canteen:
    accent = hexc("#22E06B")
    CHING = 1.25

    def chings(self, d):
        return [0.25 + k * self.CHING for k in range(int(d / self.CHING) + 1) if 0.25 + k * self.CHING < d - 0.2]

    def events(self, d):
        return [(c, "kaching") for c in self.chings(d)]

    def draw(self, ctx, t, d):
        backdrop(ctx, hexc("#06200F"), hexc("#020805"), self.accent, 540, 700, t)
        # neon menu board
        rrect(ctx, 140, 290, 800, 330, 24)
        rgba(ctx, hexc("#0B0F0C"), 0.95)
        ctx.fill()
        rrect(ctx, 140, 290, 800, 330, 24)
        rgba(ctx, self.accent, 0.8)
        ctx.set_line_width(5)
        ctx.stroke()
        on = 1.0 if rnd(math.floor(t * 10), 2) > 0.08 else 0.4
        text(ctx, "MENU", 540, 345, 50, self.accent, a=on)
        for k, (item, price) in enumerate((("POPCORN", "₹450"), ("COLD DRINK", "₹350"), ("NACHOS", "₹400"))):
            y = 425 + k * 68
            text(ctx, item, 200, y, 46, (1, 1, 1), anchor="l", a=on)
            text(ctx, price, 880, y, 52, GOLD, font=CAPTION_FONT, anchor="r", a=on)
        # popcorn machine
        rrect(ctx, 50, 700, 250, 420, 16)
        rgba(ctx, hexc("#C1121F"))
        ctx.fill()
        rrect(ctx, 72, 760, 206, 300, 8)
        rgba(ctx, hexc("#FFE8A3"), 0.25)
        ctx.fill()
        text(ctx, "POPCORN", 175, 732, 38, (1, 1, 1))
        for i in range(24):
            circle(ctx, 85 + 180 * rnd(i, 1), 1040 - 40 * rnd(i, 2), 14, POPCORN)
        for i in range(10):
            age = (t * 1.8 + rnd(i, 3)) % 1
            circle(ctx, 95 + 160 * rnd(i, 4), 1010 - 230 * math.sin(math.pi * age), 11, POPCORN)
        # profit thermometer
        frac = 0.2 + 0.7 * ease_out_cubic(t / max(d * 0.7, 0.5))
        rrect(ctx, 930, 690, 80, 420, 40)
        rgba(ctx, (1, 1, 1), 0.15)
        ctx.fill()
        rrect(ctx, 945, 690 + 400 * (1 - frac), 50, 400 * frac + 10, 25)
        rgba(ctx, hexc("#FF3B3B"))
        ctx.fill()
        circle(ctx, 970, 1120, 55, hexc("#FF3B3B"))
        glow(ctx, 970, 690 + 400 * (1 - frac), 90, hexc("#FF3B3B"), 0.6)
        text(ctx, f"{int(frac * 100)}%", 960, 650, 54, hexc("#FF3B3B"), font=CAPTION_FONT,
             stroke=(0, 0, 0), stroke_w=8)
        text(ctx, "PROFIT", 970, 1200, 34, (1, 1, 1))
        # counter
        g = cairo.LinearGradient(0, 1130, 0, 1440)
        g.add_color_stop_rgb(0, *hexc("#7A4A2A"))
        g.add_color_stop_rgb(1, *hexc("#3A2212"))
        ctx.set_source(g)
        ctx.rectangle(0, 1130, W, 310)
        ctx.fill()
        ctx.rectangle(0, 1122, W, 16)
        rgba(ctx, hexc("#A8754E"))
        ctx.fill()
        # overflowing pile of cash grows with each ka-ching
        rang = sum(1 for c in self.chings(d) if c <= t)
        for i in range(min(40, rang * 9)):
            banknote(ctx, 300 + 480 * rnd(i, 6), 1120 - 20 * rnd(i, 7), 0.8, rnd(i, 8) * 2 - 1)
        # cash register
        last = max([c for c in self.chings(d) if c <= t], default=-9)
        u = t - last
        opened = ease_out_back(u / 0.25) if u < 0.9 else max(0.0, 1 - (u - 0.9) / 0.2)
        rx, ry = 540, 1120
        rrect(ctx, rx - 200, ry - 70 + 60 * opened, 400, 70, 10)
        rgba(ctx, hexc("#9C7A2E"))
        ctx.fill()
        ctx.move_to(rx - 220, ry - 70)
        ctx.line_to(rx + 220, ry - 70)
        ctx.line_to(rx + 175, ry - 350)
        ctx.line_to(rx - 175, ry - 350)
        ctx.close_path()
        g = cairo.LinearGradient(rx - 220, 0, rx + 220, 0)
        g.add_color_stop_rgb(0, *hexc("#B8862B"))
        g.add_color_stop_rgb(0.5, *hexc("#FFD36E"))
        g.add_color_stop_rgb(1, *hexc("#9C6F1E"))
        ctx.set_source(g)
        ctx.fill()
        pressed = int(t * 8) % 15
        for r_ in range(3):
            for c_ in range(5):
                idx = r_ * 5 + c_
                kx = rx - 130 + c_ * 65
                ky = ry - 290 + r_ * 70 + (5 if idx == pressed else 0)
                circle(ctx, kx, ky + 6, 24, hexc("#5A3E10"))
                circle(ctx, kx, ky, 24, hexc("#F5F0E1") if idx != pressed else hexc("#CFC8B0"))
        rrect(ctx, rx - 130, ry - 460, 260, 100, 14)
        rgba(ctx, hexc("#0B140E"))
        ctx.fill()
        amount = 450 * rang + int(40 * (t % self.CHING))
        text(ctx, f"₹{amount}", rx, ry - 410, 64, self.accent, font=CAPTION_FONT)
        if u < 0.9:  # pop-up flag + cash burst
            ctx.save()
            ctx.translate(rx + 250, ry - 330 - 40 * ease_out_back(u / 0.3))
            ctx.rotate(0.18)
            text(ctx, "KA-CHING!", 0, 0, 76, GOLD, font=CAPTION_FONT,
                 a=1 - u / 0.9, stroke=(0, 0, 0), stroke_w=10)
            ctx.restore()
            for k in range(8):
                vx = (rnd(k + rang * 8, 1) - 0.5) * 900
                px = rx + vx * u
                py = ry - 40 - 900 * u + 1100 * u * u
                banknote(ctx, px, py, 0.9, u * 8 * (rnd(k, 2) - 0.5), a=1 - u / 0.9 * 0.5)


class Decoy:
    accent = hexc("#FF3B3B")
    STAMP = 0.9
    ZAP = 0.85

    def events(self, d):
        return [(self.STAMP + 0.18, "boom")] + [(0.2 + k * self.ZAP, "zap") for k in range(int(d / self.ZAP))]

    def draw(self, ctx, t, d):
        backdrop(ctx, hexc("#24060A"), hexc("#080203"), self.accent, 540, 560, t)
        # brain in a cage = MIND TRAP
        bx, by = 540, 600
        brain(ctx, bx, by, 1.0, t)
        drop = ease_out_cubic((t - 0.3) / 0.4)
        cage_y = lerp(-400, 0, bounce_out((t - 0.3) / 0.6)) if t > 0.3 else -400
        if drop > 0:
            for k in range(-4, 5):
                line(ctx, [(bx + k * 42, by - 200 + cage_y), (bx + k * 42, by + 150 + cage_y)], hexc("#9AA0AE"), 10)
            ctx.arc(bx, by - 200 + cage_y, 175, math.pi, 2 * math.pi)
            rgba(ctx, hexc("#9AA0AE"))
            ctx.set_line_width(12)
            ctx.stroke()
            rrect(ctx, bx - 200, by + 150 + cage_y, 400, 26, 8)
            ctx.fill()
        # tubs
        small, big = (290, 1330), (780, 1330)
        tub(ctx, *small, 0.68, "₹350", t)
        bounce = abs(math.sin(t * 5)) * 30
        tub(ctx, big[0], big[1] - bounce, 1.0, "₹450", t, glow_c=GOLD)
        # lasers from both tubs into the trap
        arrow_laser(ctx, small[0] + 20, small[1] - 290, bx - 150, by + 300, t, self.accent)
        arrow_laser(ctx, big[0] - 60, big[1] - 420 - bounce, bx + 150, by + 300, t, self.accent)
        p = 1 + 0.08 * math.sin(t * 10)
        ctx.save()
        ctx.translate(bx, by + 250)
        ctx.scale(p, p)
        rrect(ctx, -190, -48, 380, 96, 48)
        rgba(ctx, self.accent)
        ctx.fill()
        text(ctx, "MIND TRAP", 0, 0, 64, (1, 1, 1), font=CAPTION_FONT)
        ctx.restore()
        # starburst on the big tub
        ctx.save()
        ctx.translate(big[0] + 150, big[1] - 470 - bounce)
        ctx.rotate(t * 1.5)
        ctx.new_path()
        for k in range(24):
            r = 105 if k % 2 == 0 else 75
            a = k / 24 * math.tau
            ctx.line_to(r * math.cos(a), r * math.sin(a))
        ctx.close_path()
        rgba(ctx, GOLD)
        ctx.fill()
        ctx.restore()
        text(ctx, "DOUBLE?!", big[0] + 150, big[1] - 470 - bounce, 46, (0.1, 0.1, 0.1), font=CAPTION_FONT)
        # DECOY stamp slams onto the small tub
        u = (t - self.STAMP) / 0.18
        if u >= 0:
            sc = lerp(3.0, 1.0, ease_out_cubic(u))
            ctx.save()
            ctx.translate(small[0] - 20, small[1] - 400)
            ctx.rotate(-0.2)
            ctx.scale(sc, sc)
            rrect(ctx, -130, -46, 260, 92, 12)
            rgba(ctx, self.accent, min(1, u))
            ctx.set_line_width(10)
            ctx.stroke()
            text(ctx, "DECOY", 0, 0, 72, self.accent, font=CAPTION_FONT, a=min(1, u))
            ctx.restore()


class Point:
    accent = hexc("#FFD60A")

    def events(self, d):
        return [(0.02, "boom"), (0.05, "alarm")]

    def draw(self, ctx, t, d):
        backdrop(ctx, hexc("#2A0606"), hexc("#070101"), hexc("#FF3B3B"), 540, 800, t)
        # manga focus lines
        ctx.save()
        ctx.translate(540, 900)
        for k in range(48):
            a = k / 48 * math.tau + 0.02 * math.sin(t * 20 + k)
            r0 = 420 + 80 * rnd(k + int(t * 12), 3)
            ctx.move_to(r0 * math.cos(a), r0 * math.sin(a))
            ctx.line_to(1500 * math.cos(a + 0.012), 1500 * math.sin(a + 0.012))
            ctx.line_to(1500 * math.cos(a - 0.012), 1500 * math.sin(a - 0.012))
            ctx.close_path()
            rgba(ctx, (1, 1, 1), 0.07)
            ctx.fill()
        ctx.restore()
        # rotating alarm beacons
        for bx in (110, 970):
            a = t * 7 + (0 if bx < 500 else math.pi)
            ctx.move_to(bx, 640)
            ctx.arc(bx, 640, 520, a - 0.3, a + 0.3)
            ctx.close_path()
            rgba(ctx, hexc("#FF3B3B"), 0.2)
            ctx.fill()
            ctx.arc(bx, 660, 46, math.pi, 2 * math.pi)
            rgba(ctx, hexc("#FF3B3B"))
            ctx.fill()
            glow(ctx, bx, 640, 110, hexc("#FF3B3B"), 0.5 + 0.4 * math.sin(t * 14))
        shake = 6 * math.sin(t * 40) * (1 if (t % 1.2) < 0.3 else 0.2)
        scientist(ctx, 540 + shake, 860, 0.92, t, pose="point")
        # headline
        pop = ease_out_back(t / 0.35)
        ctx.save()
        ctx.translate(540 + shake, 390)
        ctx.scale(pop, pop)
        ctx.rotate(-0.04)
        for k in range(-6, 7):
            ctx.move_to(k * 80 - 30, -150)
            ctx.line_to(k * 80 + 10, -150)
            ctx.line_to(k * 80 - 30, -118)
            ctx.line_to(k * 80 - 70, -118)
            ctx.close_path()
            rgba(ctx, GOLD)
            ctx.fill()
        text(ctx, "SHARE KARO", 0, -55, 96, (1, 1, 1), font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=12)
        text(ctx, "FOLLOW KARO!", 0, 55, 116, GOLD, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=14)
        ctx.restore()


SCENE_CLASSES = {"lab": Lab, "projector": Projector, "canteen": Canteen, "decoy": Decoy, "point": Point}
