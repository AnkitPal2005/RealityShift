"""Story: Reality Shift — two Made-in-India weapons that shook the world (BrahMos + Pinaka).

Ultra-fast cut: every scene hard-cuts on its narration beats and re-frames the camera in
between, so no shot holds longer than ~1.5 s. Captions sit in the 1150-1250 px band; nothing
with text is drawn in the bottom 400 px (YouTube UI).
"""

import math

import cairo

from engine import *  # noqa: F401,F403
from stories.reality_shift import GOLD, SAFFRON, SIL, TRICOLOR, flag, globe, leader, stamp, subscribe_badge
from stories.reality_shift_defense import Cued, bowing_figure, brahmos, flash, label

TOPIC = "MADE IN INDIA HATHIYAR"
OUTPUTS = {"edge": "reality_shift_32s_weapons.mp4", "elevenlabs": "reality_shift_32s_weapons_el.mp4"}
OUTPUT_DIR = OUT_DIR

CLEAN_PUNCTUATION = False
MAX_GAP = 0.12             # zero dead air
TAIL_PAD = 0.0
TRIM = {"thresh": 0.006, "keep": 0.05, "keep_tail": 0.08}
MUSIC_BPM = 128
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"

CYAN = hexc("#22E4FF")
RED = hexc("#FF3B3B")
CAPTION_Y = 1200           # centre of the 1150-1250 safe band
CAPTION_SIZE = 112
HOT_COLOR = GOLD
HOT_COLORS = {"BRAHMOS": GOLD, "MACH": GOLD, "3": GOLD, "SUPERSONIC": GOLD,
              "PINAKA": CYAN, "44": CYAN, "SECONDS": CYAN, "12": CYAN, "4": CYAN}

NARRATION = {
    "hook": "दुनिया को लगा था भारत सिर्फ हथियार खरीदेगा... पर इन दो मेड-इन-इंडिया हथियारों ने पूरी दुनिया को "
            "हिला दिया!",
    "brahmos": "पहला— ब्रह्मोस! दुनिया की सबसे तेज़ सुपरसोनिक क्रूज़ मिसाइल। इसकी मैक थ्री की रफ्तार को रोकना "
               "नामुमकिन है, और आज बड़े-बड़े देश इसके लिए लाइन लगाकर खड़े हैं!",
    "pinaka": "दूसरा— पिनाका सिस्टम! सिर्फ चौवालिस सेकंड में बारह रॉकेट्स दागकर चार स्क्वायर किलोमीटर का इलाका "
              "तबाह कर देता है। इसकी ताकत देखकर विदेशी सेनाएं भी हैरान हैं!",
    "outro": "इन दोनों में से आपको सबसे खतरनाक कौन सा लगा? कमेंट में 'जय हिंद' ज़रूर लिखें, और ऐसी ही ताकत "
             "देखने के लिए रियलिटी शिफ्ट को सब्सक्राइब करें!",
}

CHUNKS = {
    "hook": [
        ("दुनिया को लगा था", "DUNIYA KO LAGA THA"),
        ("भारत सिर्फ", "BHARAT SIRF"),
        ("हथियार खरीदेगा...", "HATHIYAR KHAREEDEGA..."),
        ("पर इन दो", "PAR IN DO"),
        ("मेड-इन-इंडिया", "MADE IN INDIA"),
        ("हथियारों ने", "HATHIYARON NE"),
        ("पूरी दुनिया को", "POORI DUNIYA KO"),
        ("हिला दिया!", "HILA DIYA!"),
    ],
    "brahmos": [
        ("पहला—", "PEHLA!"),
        ("ब्रह्मोस!", "BRAHMOS!"),
        ("दुनिया की सबसे तेज़", "DUNIYA KI SABSE TEZ"),
        ("सुपरसोनिक", "SUPERSONIC"),
        ("क्रूज़ मिसाइल।", "CRUISE MISSILE"),
        ("इसकी मैक थ्री", "ISKI MACH 3"),
        ("की रफ्तार को", "KI RAFTAAR KO"),
        ("रोकना नामुमकिन है,", "ROKNA NAMUMKIN HAI"),
        ("और आज बड़े-बड़े देश", "AUR AAJ BADE-BADE DESH"),
        ("इसके लिए", "ISKE LIYE"),
        ("लाइन लगाकर खड़े हैं!", "LINE LAGAKAR KHADE HAIN!"),
    ],
    "pinaka": [
        ("दूसरा—", "DOOSRA!"),
        ("पिनाका सिस्टम!", "PINAKA SYSTEM!"),
        ("सिर्फ चौवालिस सेकंड में", "SIRF 44 SECONDS MEIN"),
        ("बारह रॉकेट्स", "12 ROCKETS"),
        ("दागकर", "DAAGKAR"),
        ("चार स्क्वायर किलोमीटर", "4 SQ. KM"),
        ("का इलाका", "KA ILAAKA"),
        ("तबाह कर देता है।", "TABAAH KAR DETA HAI!"),
        ("इसकी ताकत देखकर", "ISKI TAAKAT DEKHKAR"),
        ("विदेशी सेनाएं", "VIDESHI SENAYEN"),
        ("भी हैरान हैं!", "BHI HAIRAN HAIN!"),
    ],
    "outro": [
        ("इन दोनों में से", "IN DONO MEIN SE"),
        ("आपको सबसे खतरनाक", "AAPKO SABSE KHATARNAK"),
        ("कौन सा लगा?", "KAUN SA LAGA?"),
        ("कमेंट में", "COMMENT MEIN"),
        ("'जय हिंद'", "'JAI HIND'"),
        ("ज़रूर लिखें,", "ZAROOR LIKHEIN"),
        ("और ऐसी ही ताकत", "AUR AISI HI TAAKAT"),
        ("देखने के लिए", "DEKHNE KE LIYE"),
        ("रियलिटी शिफ्ट को", "REALITY SHIFT KO"),
        ("सब्सक्राइब करें!", "SUBSCRIBE KAREIN!"),
    ],
}

HOT_WORDS = {"MADE", "INDIA", "HILA", "BRAHMOS", "SUPERSONIC", "MACH", "3", "NAMUMKIN", "PINAKA", "44",
             "SECONDS", "12", "4", "TABAAH", "HAIRAN", "KHATARNAK", "JAI", "HIND", "SUBSCRIBE"}

for _key, _chunks in CHUNKS.items():
    assert " ".join(h for h, _ in _chunks) == NARRATION[_key], f"caption chunks drift from narration: {_key}"

SCRIPT = [(key, CHUNKS[key]) for key in NARRATION]

FIRE = hexc("#FF8A1F")
SMOKE = (0.42, 0.42, 0.46)
STAMP_Y = 330              # all HUD text lives in the top third, clear of captions and the YouTube UI


# ============================================================ rapid-cut camera

# re-frames cycled on every cut: (zoom, dx, dy, roll); zoom > 1 so shake never shows an edge
FRAMES = ((1.06, 0, 0, 0.0), (1.18, -40, -70, 0.012), (1.1, 45, 50, -0.012), (1.24, 0, -110, 0.0))
MAX_SHOT = 1.5
GRID = 1.35


class Rapid(Cued):
    """Scene made of named shots (methods) that hard-cut on narration beats; long shots are
    split by camera re-frames every GRID seconds. Subclasses define beats, shots, hud, shake
    and may swap the re-frame cycle (frames)."""
    accent = GOLD
    frames = FRAMES

    def shots(self, d):
        raise NotImplementedError

    def hud(self, ctx, t, d, b):
        pass

    def shake(self, t, d, b):
        return 0.0

    def cuts(self, d):
        out = [0.0]
        for m in [s for s, _ in self.shots(d)[1:]] + [d]:
            while m - out[-1] > MAX_SHOT:
                out.append(out[-1] + GRID)
            if m >= d:
                break
            if m - out[-1] > 0.5 or len(out) == 1:
                out.append(m)
            else:
                out[-1] = m  # snap the nearest re-frame onto the beat
        return out

    def draw(self, ctx, t, d):
        b = self.beats(d)
        cuts = self.cuts(d)
        i = max(k for k, c in enumerate(cuts) if c <= t)
        u = t - cuts[i]
        z, dx, dy, roll = self.frames[i % len(self.frames)]
        amp = self.shake(t, d, b)
        f = int(t * 45)
        ctx.save()
        ctx.translate(W / 2 + dx + amp * (2 * rnd(f, 1) - 1), H * 0.42 + dy + amp * (2 * rnd(f, 2) - 1))
        z *= lerp(1.12, 1.0, ease_out_cubic(u / 0.22))
        ctx.scale(z, z)
        ctx.rotate(roll)
        ctx.translate(-W / 2, -H * 0.42)
        start, name = [s for s in self.shots(d) if s[0] <= t][-1]
        getattr(self, name)(ctx, t - start, t, d, b)
        ctx.restore()
        self.hud(ctx, t, d, b)
        if i > 0:
            flash(ctx, u, 0.12, 0.4)


def kick(u, dur=0.6, amp=36.0):
    """Shake amplitude that hits at u = 0 and decays over dur."""
    return amp * (1 - u / dur) ** 2 if 0 <= u < dur else 0.0


def sky(ctx, stops):
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in stops:
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.paint()


def ground(ctx, y, c, a=1.0):
    ctx.rectangle(-300, y, W + 600, H)
    rgba(ctx, c if isinstance(c, tuple) else hexc(c), a)
    ctx.fill()


def speed_lines(ctx, t, n, c, speed=2600, y0=0, y1=H, a=0.5):
    for i in range(n):
        y = y0 + (y1 - y0) * rnd(i, 7)
        ln = 120 + 380 * rnd(i, 8)
        x = W + 400 - (rnd(i, 9) * (W + 800) + t * speed * (0.7 + 0.6 * rnd(i, 10))) % (W + 800)
        line(ctx, [(x, y), (x + ln, y)], c, 2 + 4 * rnd(i, 11), a * (0.4 + 0.6 * rnd(i, 12)))


def shockwave(ctx, x, y, u, r0, r1, c, dur=0.7, w=10):
    if 0 <= u < dur:
        k = ease_out_cubic(u / dur)
        ctx.arc(x, y, lerp(r0, r1, k), 0, math.tau)
        rgba(ctx, c, 0.8 * (1 - k))
        ctx.set_line_width(w)
        ctx.stroke()


def fireball(ctx, x, y, u, size=1.0, seed=0):
    """Ground impact: flash, layered fire, rising smoke and flying debris (u = seconds since impact)."""
    if u < 0:
        return
    k = ease_out_cubic(u / 0.5)
    fade = clamp(1 - (u - 0.4) / 1.6)
    for i in range(10):  # smoke column
        v = clamp(u / 1.8)
        sy = y - 420 * size * v * (i / 10) - 40 * size
        sr = (60 + 90 * (i / 10)) * size * (0.4 + 0.6 * k)
        circle(ctx, x + 30 * size * math.sin(i * 1.9 + seed), sy, sr, (0.16, 0.13, 0.12), 0.55 * clamp(u / 0.3))
    glow(ctx, x, y - 60 * size, 420 * size * k, FIRE, 0.9 * fade)
    for i, (c, r) in enumerate(((hexc("#B3260B"), 170), (FIRE, 125), (hexc("#FFD36E"), 80), ((1, 1, 0.9), 40))):
        for j in range(5):
            ox = 70 * size * (rnd(j, seed + i) - 0.5) * 2
            oy = -60 * size * rnd(j, seed + i + 3) - 40 * size * k
            circle(ctx, x + ox * k, y + oy, r * size * k * (0.7 + 0.4 * rnd(j, seed + 9)), c, fade)
    for i in range(14):  # debris
        ang = -math.pi * rnd(i, seed + 20)
        dist = 520 * size * clamp(u / 0.9)
        px, py = x + dist * math.cos(ang), y + dist * math.sin(ang) + 500 * size * clamp(u / 0.9) ** 2
        circle(ctx, px, py, 6 * size, (0.1, 0.08, 0.06), fade)


def rocket(ctx, x, y, ang, s, t, burn=1.0):
    """Small artillery rocket, nose along angle ang, with flame and glow."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(s, s)
    f = burn * (1 + 0.3 * math.sin(t * 60 + x))
    glow(ctx, -60, 0, 90 * f, FIRE, 0.8)
    ctx.move_to(-48, -8)
    ctx.line_to(-48 - 110 * f, 0)
    ctx.line_to(-48, 8)
    ctx.close_path()
    rgba(ctx, hexc("#FFE08A"))
    ctx.fill()
    rrect(ctx, -50, -10, 90, 20, 6)
    rgba(ctx, hexc("#D8DCE2"))
    ctx.fill()
    ctx.move_to(40, -10)
    ctx.line_to(70, 0)
    ctx.line_to(40, 10)
    ctx.close_path()
    rgba(ctx, CYAN)
    ctx.fill()
    for side in (-1, 1):
        ctx.move_to(-50, side * 10)
        ctx.line_to(-64, side * 24)
        ctx.line_to(-34, side * 10)
        ctx.close_path()
        rgba(ctx, hexc("#9AA3B0"))
        ctx.fill()
    ctx.restore()


# ============================================================ figures (silhouettes)

def soldier(ctx, x, y, s, salute, rim=SAFFRON):
    """Saluting jawan silhouette, rim-lit from behind; (x, y) at the feet."""
    v = ease_out_back(salute, 1.4)

    def body(c, a=1.0):
        for side in (-1, 1):
            line(ctx, [(side * 28, -230), (side * 32, 0)], c, 46, a)
        rrect(ctx, -78, -470, 156, 260, 40)
        rgba(ctx, c, a)
        ctx.fill()
        line(ctx, [(-104, -500), (-112, -150)], c, 14, a)                    # rifle
        line(ctx, [(-74, -450), (-96, -330), (-100, -240)], c, 38, a)
        line(ctx, [(74, -450), (lerp(98, 168, v), lerp(-330, -480, v)),
                   (lerp(90, 50, v), lerp(-240, -530, v))], c, 38, a)        # saluting arm
        circle(ctx, 0, -520, 50, c, a)
        ctx.arc(0, -530, 62, math.pi, math.tau)                              # helmet
        rgba(ctx, c, a)
        ctx.fill()
        rrect(ctx, -70, -536, 140, 16, 8)
        ctx.fill()

    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for ox in (-7, 7):
        ctx.save()
        ctx.translate(ox, -5)
        body(rim, 0.85)
        ctx.restore()
    body(SIL)
    ctx.restore()


def officer(ctx, x, y, s, t, k, rim=FIRE):
    """Foreign officer silhouette in a peaked cap, binoculars raised; (x, y) at the waist."""
    ctx.save()
    ctx.translate(x, y + 4 * math.sin(t * 3 + k))
    ctx.scale(s, s)

    def body(c, a=1.0):
        ctx.move_to(-150, 0)
        ctx.curve_to(-150, -170, -110, -230, -40, -240)
        ctx.line_to(40, -240)
        ctx.curve_to(110, -230, 150, -170, 150, 0)
        ctx.close_path()
        rgba(ctx, c, a)
        ctx.fill()
        circle(ctx, 0, -320, 70, c, a)
        rrect(ctx, -95, -405, 190, 44, 18)                                 # cap crown
        ctx.fill()
        rrect(ctx, -70, -370, 140, 22, 10)                                  # visor
        ctx.fill()
        for side in (-1, 1):
            line(ctx, [(side * 120, -200), (side * 130, -260), (side * 40, -320)], c, 40, a)
            rrect(ctx, side * 34 - 26, -350, 52, 70, 14)                    # binocular barrels
            ctx.fill()

    for ox in (-7, 7):
        ctx.save()
        ctx.translate(ox, -5)
        body(rim, 0.9)
        ctx.restore()
    body(SIL)
    for side in (-1, 1):                                                    # lens glints
        circle(ctx, side * 34, -318, 20, hexc("#9FD8FF"), 0.5 + 0.4 * abs(math.sin(t * 4 + k + side)))
    ctx.restore()


def pinaka_truck(ctx, x, y, s, t, elev, fired, recoil=0.0):
    """Side view of the Pinaka launcher truck facing right, (x, y) at ground under the centre.
    elev = pod elevation (rad), fired = tubes already emptied. Returns the launch transform
    (pivot x, pivot y, angle) in user space for spawning rockets."""
    ctx.save()
    ctx.translate(x - 8 * recoil, y)
    ctx.scale(s, s)
    for wx in (-300, -170, 150, 280):                                       # 8x8 wheels
        circle(ctx, wx, -60, 60, hexc("#15171B"))
        circle(ctx, wx, -60, 26, hexc("#4A4F57"))
    rrect(ctx, -390, -150, 720, 70, 10)                                     # chassis + bed
    rgba(ctx, hexc("#4B5320"))
    ctx.fill()
    ctx.move_to(250, -150)                                                  # cab
    ctx.line_to(250, -320)
    ctx.line_to(370, -320)
    ctx.line_to(420, -230)
    ctx.line_to(420, -150)
    ctx.close_path()
    rgba(ctx, hexc("#56602A"))
    ctx.fill()
    ctx.move_to(275, -300)
    ctx.line_to(360, -300)
    ctx.line_to(395, -240)
    ctx.line_to(275, -240)
    ctx.close_path()
    rgba(ctx, hexc("#8FC6E0"), 0.85)
    ctx.fill()
    line(ctx, [(-260, -150), (-260, -200)], hexc("#2F3418"), 26)            # turret pivot
    ctx.save()
    ctx.translate(-260, -200)
    ctx.rotate(-elev)
    rrect(ctx, -170, -150, 470, 150, 10)                                    # twin 6-tube pods
    rgba(ctx, hexc("#5E6A2E"))
    ctx.fill()
    for r in range(6):
        ry = -138 + r * 24
        line(ctx, [(-160, ry + 10), (290, ry + 10)], hexc("#3B4320"), 4)
        hot = r * 2 < fired
        circle(ctx, 292, ry + 10, 10, FIRE if hot else hexc("#1C1F10"), 0.9 if hot else 1.0)
    line(ctx, [(-170, -75), (300, -75)], hexc("#2F3418"), 6)
    ctx.restore()
    ctx.restore()
    return x - 8 * recoil + s * (-260 + 300 * math.cos(-elev) + 75 * math.sin(-elev)), \
        y + s * (-200 + 300 * math.sin(-elev) - 75 * math.cos(-elev)), -elev


# ============================================================ scenes

class Hook(Rapid):
    """GAME CHANGER slam with screen shake -> PM inspecting saluting jawans in silhouette ->
    two Made-in-India strikes rock the globe."""
    accent = SAFFRON

    def beats(self, d):
        c = self.cue
        return {"buy": c("KHAREEDEGA", d * 0.2), "made": c("MADE", d * 0.5), "poori": c("POORI", d * 0.75),
                "hila": c("HILA", d * 0.86)}

    def shots(self, d):
        b = self.beats(d)
        return [(0.0, "game_changer"), (min(1.3, b["buy"]), "inspect"), (b["poori"], "world")]

    def events(self, d):
        b = self.beats(d)
        return [(0.0, "boom"), (0.05, "zap"), (b["made"], "kaching"), (b["poori"], "whoosh"),
                (b["hila"], "boom"), (b["hila"] + 0.3, "boom")]

    def shake(self, t, d, b):
        return kick(t, 0.7, 40) + kick(t - b["hila"], 0.9, 34)

    def game_changer(self, ctx, ts, t, d, b):
        sky(ctx, ((0, "#200400"), (0.5, "#4A0E02"), (1, "#0A0100")))
        ctx.save()
        ctx.translate(540, 760)
        ctx.rotate(t * 0.6)
        for k in range(20):
            a = k / 20 * math.tau
            ctx.move_to(0, 0)
            ctx.arc(0, 0, 1600, a, a + math.tau / 40)
            ctx.close_path()
            rgba(ctx, TRICOLOR[k % 3], 0.12)
            ctx.fill()
        ctx.restore()
        glow(ctx, 540, 760, 700, SAFFRON, 0.55)
        pop = max(ease_out_back(ts / 0.25, 2.4), 1e-3)
        ctx.save()
        ctx.translate(540, 780)
        ctx.scale(pop, pop)
        ctx.rotate(-0.04)
        text(ctx, "GAME", 0, -150, 190, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
        glow(ctx, 0, 40, 420, GOLD, 0.35)
        text(ctx, "CHANGER", 0, 40, 210, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
        flag(ctx, -110, 200, 220, 146, "in", t, pole=0)
        ctx.restore()

    def inspect(self, ctx, ts, t, d, b):
        sky(ctx, ((0, "#2A0A04"), (0.45, "#C2410C"), (0.7, "#FF9A3C"), (0.8, "#FFD27A"), (1, "#FFD27A")))
        glow(ctx, 540, 1430, 760, hexc("#FFE3A0"), 0.85)
        circle(ctx, 540, 1480, 210, hexc("#FFF1CF"), 0.95)                   # setting sun
        for i in range(5):
            line(ctx, [(-100, 520 + i * 90), (W + 100, 500 + i * 95)], hexc("#7A2A0A"), 6, 0.25)
        for k, x in enumerate((640, 780, 920, 1060)):
            soldier(ctx, x, 1520, 0.8, ease_in_out((ts - 0.15 - 0.18 * k) / 0.45))
        lx = lerp(250, 430, ease_in_out(ts / max(b["poori"] - 1.3, 1.0)))
        leader(ctx, lx, 1090, 0.42, t, pose="stand", shadow=True)
        ground(ctx, 1520, SIL)
        line(ctx, [(-200, 1520), (W + 200, 1520)], SAFFRON, 4, 0.8)

    def world(self, ctx, ts, t, d, b):
        sky(ctx, ((0, "#02040F"), (1, "#0A1230")))
        for i in range(80):
            circle(ctx, rnd(i, 1) * W, rnd(i, 2) * H, 1 + 2 * rnd(i, 3), (1, 1, 1), 0.2 + 0.5 * rnd(i, 4))
        gx, gy = 540, 760
        globe(ctx, gx, gy, 340, t)
        hit = t - b["hila"]
        for k, (c, sx, sy) in enumerate(((GOLD, -150, 200), (CYAN, W + 150, 260))):  # two strikes inbound
            v = clamp((t - b["poori"]) / max(b["hila"] - b["poori"], 0.3))
            if v < 1:
                px, py = lerp(sx, gx + (k * 2 - 1) * 120, v), lerp(sy, gy - 120, v ** 1.4)
                line(ctx, [(lerp(sx, px, 0.6), lerp(sy, py, 0.6)), (px, py)], c, 10, 0.5)
                glow(ctx, px, py, 70, c, 0.9)
                circle(ctx, px, py, 12, (1, 1, 1))
        if hit > 0:
            for k, c in enumerate((GOLD, CYAN)):
                fx = gx + (k * 2 - 1) * 120
                glow(ctx, fx, gy - 120, 300 * ease_out_cubic(hit / 0.3), c, 0.9 * clamp(1 - hit / 1.2))
                for r in range(3):
                    shockwave(ctx, fx, gy - 120, hit - r * 0.15, 40, 700, c, 0.8, 12)
            for i in range(9):  # cracks across the globe
                a = rnd(i, 30) * math.tau
                ln = 340 * ease_out_cubic(hit / 0.25)
                pts = [(gx, gy - 60)]
                for j in range(1, 5):
                    pts.append((gx + ln * j / 4 * math.cos(a) + 20 * (rnd(i, j) - 0.5),
                                gy - 60 + ln * j / 4 * math.sin(a) + 20 * (rnd(i, j + 5) - 0.5)))
                line(ctx, pts, (1, 0.95, 0.8), 4, 0.9 * clamp(1 - hit / 2))

    def hud(self, ctx, t, d, b):
        if b["buy"] <= t < b["made"]:
            stamp(ctx, 540, STAMP_Y, t - b["buy"], -0.04, 620, 150, (0.6, 0.6, 0.65),
                  [("SIRF KHAREEDAR?", 0, 84, (0.85, 0.85, 0.9))])
        if t >= b["made"]:
            stamp(ctx, 540, STAMP_Y, t - b["made"], 0.03, 720, 170, GOLD,
                  [("MADE IN INDIA", 0, 110, GOLD)])
            flag(ctx, 830, STAMP_Y - 150, 120, 80, "in", t, pole=90)


class BrahMos(Rapid):
    """Vertical launch -> sea-skimming streak with spray -> sonic cone -> MACH 3 gauge ->
    radar that can't lock -> nations lining up for orders."""
    accent = GOLD

    def beats(self, d):
        c = self.cue
        return {"name": c("BRAHMOS", d * 0.05), "tez": c("TEZ", d * 0.14), "sonic": c("SUPERSONIC", d * 0.24),
                "mach": c("MACH", d * 0.4), "rokna": c("ROKNA", d * 0.55), "desh": c("DESH", d * 0.7),
                "line": c("LINE", d * 0.85)}

    def shots(self, d):
        b = self.beats(d)
        return [(0.0, "launch"), (b["tez"], "skim"), (b["mach"], "gauge"), (b["rokna"], "radar"),
                (b["desh"], "queue")]

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (0.1, "whoosh"), (b["tez"], "whoosh"), (b["sonic"], "boom"),
                (b["sonic"] + 0.05, "zap"), (b["mach"], "beep"), (b["mach"] + 0.6, "thud"),
                (b["rokna"], "alarm"), (b["desh"], "thud"), (b["line"], "kaching")]

    def shake(self, t, d, b):
        return kick(t, 0.5, 26) + kick(t - b["sonic"], 0.6, 30) + 4 * (b["tez"] <= t < b["mach"])

    def launch(self, ctx, ts, t, d, b):
        sky(ctx, ((0, "#030616"), (0.62, "#1B2A55"), (0.7, "#E06A1A"), (1, "#05070C")))
        for i in range(60):
            circle(ctx, rnd(i, 1) * W, rnd(i, 2) * 1100, 1 + 2 * rnd(i, 3), (1, 1, 1), 0.3 + 0.4 * rnd(i, 4))
        ground(ctx, 1340, "#061226")
        for i in range(24):
            y = 1360 + 260 * rnd(i, 1) ** 1.5
            x = (rnd(i, 2) * W + t * 60) % (W + 200) - 100
            line(ctx, [(x, y), (x + 60 + 80 * rnd(i, 3), y)], GOLD, 3, 0.3)
        rrect(ctx, 120, 1250, 840, 110, 18)                                  # warship deck
        rgba(ctx, hexc("#2A313C"))
        ctx.fill()
        rrect(ctx, 470, 1170, 140, 90, 8)                                   # launch cell
        rgba(ctx, hexc("#3E4756"))
        ctx.fill()
        my = 1240 - 300 * ts - 900 * ts * ts
        for k in range(14):                                                 # exhaust cloud on deck
            circle(ctx, 540 + 260 * (rnd(k, 3) - 0.5) * 2 * clamp(ts / 0.6), 1230 - 40 * rnd(k, 4),
                   90 + 60 * rnd(k, 5), (0.75, 0.72, 0.7), 0.35)
        for k in range(int(max(0.0, 1240 - my) / 30)):                      # smoke column
            yy = 1240 - k * 30
            circle(ctx, 540 + 10 * math.sin(k + t * 3), yy, 34 + 30 * (k / 40), (0.7, 0.7, 0.74), 0.18)
        brahmos(ctx, 540, my, 0.9, t)
        glow(ctx, 540, 1240, 360, FIRE, 0.6)

    def _missile_h(self, ctx, x, y, s, t):
        ctx.save()
        ctx.translate(x - 212 * s, y)
        ctx.rotate(math.pi / 2)
        brahmos(ctx, 0, 0, s, t)
        ctx.restore()

    def skim(self, ctx, ts, t, d, b, cone=True):
        sky(ctx, ((0, "#0B1C3A"), (0.5, "#5B7FB0"), (0.56, "#FFC07A"), (1, "#031021")))
        water = 1060
        ground(ctx, water, "#0A2E52")
        for i in range(70):                                                 # water rushing past
            y = water + 10 + (H - water) * rnd(i, 1) ** 1.8
            x = W + 300 - (rnd(i, 2) * (W + 600) + t * 3200 * (0.4 + (y - water) / 600)) % (W + 600)
            line(ctx, [(x, y), (x + 80 + 220 * rnd(i, 3), y)], (0.8, 0.9, 1), 3, 0.25)
        speed_lines(ctx, t, 26, (1, 1, 1), y0=200, y1=water - 40, a=0.35)
        mx, my = 560 + 30 * math.sin(t * 2), water - 70 + 8 * math.sin(t * 13)
        nozzle = mx - 212 * 0.8
        for i in range(70):                                                 # spray wake cutting the surface
            age = (t * 2.6 + rnd(i, 4)) % 1.0
            px = nozzle - 40 - age * 900
            py = water - math.sin(age * math.pi) * (40 + 140 * rnd(i, 5))
            circle(ctx, px, py, 5 + 12 * rnd(i, 6) * (1 - age), (0.92, 0.97, 1), 0.75 * (1 - age))
        ctx.rectangle(-200, water - 6, nozzle + 200, 14)
        rgba(ctx, (1, 1, 1), 0.55)
        ctx.fill()
        self._missile_h(ctx, mx, my, 0.8, t)
        u = t - b["sonic"]
        if cone and u > 0:                                                   # sonic cone + vapour collar
            nose = mx + 212 * 0.8
            a = clamp(u / 0.2)
            for side in (-1, 1):
                line(ctx, [(nose, my), (nose - 620, my + side * 330)], (1, 1, 1), 5, 0.7 * a)
                line(ctx, [(nose - 60, my), (nose - 680, my + side * 330)], (1, 1, 1), 2, 0.4 * a)
            _ellipse_ring(ctx, mx + 40, my, 40 + 30 * clamp(u / 0.3), 120 + 40 * clamp(u / 0.3), a)

    def gauge(self, ctx, ts, t, d, b):
        self.skim(ctx, ts, t, d, b, cone=False)
        rgba(ctx, (0.0, 0.02, 0.06), 0.6)
        ctx.paint()
        cx, cy, r = 540, 780, 300
        a0, a1 = math.radians(135), math.radians(405)
        val = 3.0 * ease_out_cubic(ts / 0.7) + (0.04 * math.sin(t * 40) if ts > 0.7 else 0)
        ctx.arc(cx, cy, r, a0, a1)
        rgba(ctx, (1, 1, 1), 0.15)
        ctx.set_line_width(36)
        ctx.stroke()
        ctx.arc(cx, cy, r, a0, lerp(a0, a1, val / 3.4))
        rgba(ctx, GOLD)
        ctx.set_line_width(36)
        ctx.stroke()
        glow(ctx, cx, cy, r * 1.3, GOLD, 0.25)
        for m in range(4):
            a = lerp(a0, a1, m / 3.4)
            line(ctx, [(cx + (r - 70) * math.cos(a), cy + (r - 70) * math.sin(a)),
                       (cx + (r - 30) * math.cos(a), cy + (r - 30) * math.sin(a))], (1, 1, 1), 6)
            text(ctx, str(m), cx + (r - 115) * math.cos(a), cy + (r - 115) * math.sin(a), 52, (1, 1, 1),
                 font=CAPTION_FONT, bold=False)
        a = lerp(a0, a1, val / 3.4)
        line(ctx, [(cx, cy), (cx + (r - 40) * math.cos(a), cy + (r - 40) * math.sin(a))], RED, 12)
        circle(ctx, cx, cy, 26, (1, 1, 1))
        text(ctx, f"MACH {val:.1f}", cx, cy + 150, 78, GOLD, font=CAPTION_FONT, bold=False,
             stroke=(0, 0, 0), stroke_w=10)

    def radar(self, ctx, ts, t, d, b):
        sky(ctx, ((0, "#021008"), (1, "#000502")))
        cx, cy, r = 540, 760, 360
        circle(ctx, cx, cy, r, hexc("#04230F"))
        for k in range(1, 5):
            ctx.arc(cx, cy, r * k / 4, 0, math.tau)
            rgba(ctx, hexc("#22C55E"), 0.35)
            ctx.set_line_width(3)
            ctx.stroke()
        line(ctx, [(cx - r, cy), (cx + r, cy)], hexc("#22C55E"), 2, 0.35)
        line(ctx, [(cx, cy - r), (cx, cy + r)], hexc("#22C55E"), 2, 0.35)
        sweep = t * 5
        ctx.move_to(cx, cy)
        ctx.arc(cx, cy, r, sweep - 0.6, sweep)
        ctx.close_path()
        rgba(ctx, hexc("#22C55E"), 0.3)
        ctx.fill()
        v = clamp(ts / 1.4)                                                 # BrahMos blip too fast to lock
        bx, by = lerp(cx - r + 30, cx + r - 30, v), cy - 140 + 60 * math.sin(v * 3)
        line(ctx, [(lerp(cx - r + 30, bx, 0.3), by + 10), (bx, by)], GOLD, 8, 0.6)
        glow(ctx, bx, by, 60, GOLD, 0.9)
        circle(ctx, bx, by, 12, (1, 1, 1))
        for k in range(3):                                                  # interceptors arrive too late
            u = ts - 0.2 - 0.25 * k
            if u > 0:
                ix = lerp(cx + 40 * (k - 1), bx - 220 - 90 * k, clamp(u / 0.7))
                iy = lerp(cy + r - 40, by + 60 * (k - 1), clamp(u / 0.7))
                circle(ctx, ix, iy, 10, RED)
                if u > 0.7:
                    text(ctx, "MISS", ix, iy + 40, 34, RED, font=CAPTION_FONT, bold=False, a=clamp((u - 0.7) / 0.2))

    def queue(self, ctx, ts, t, d, b):
        sky(ctx, ((0, "#0A1030"), (1, "#020309")))
        glow(ctx, 860, 760, 700, GOLD, 0.35)
        ground(ctx, 1460, "#05070F")
        brahmos(ctx, 860, 1440, 1.0, t, burn=0)
        label(ctx, "BRAHMOS", 860, 960, ts - 0.2, size=52)
        for k in range(6):                                                  # buyers shuffle into line
            x = lerp(-120, 110 + k * 110, ease_out_cubic((ts - 0.1 * k) / 0.6))
            sc = 0.62 - 0.03 * k
            bowing_figure(ctx, x, 1460, sc, 0.05 * math.sin(t * 3 + k), c=(0.3, 0.33, 0.42))
            u = ts - 0.5 - 0.12 * k
            if u > 0:
                pop = ease_out_back(u / 0.25)
                ctx.save()
                ctx.translate(x, 1010 - 30 * (k % 2))
                ctx.scale(pop, pop)
                rrect(ctx, -54, -26, 108, 52, 8)
                rgba(ctx, (1, 1, 1))
                ctx.fill()
                text(ctx, "ORDER", 0, 0, 28, hexc("#0A1030"), font=CAPTION_FONT, bold=False)
                ctx.restore()

    def hud(self, ctx, t, d, b):
        if b["name"] <= t < b["mach"]:
            stamp(ctx, 540, STAMP_Y, t - b["name"], -0.04, 640, 170, GOLD, [("BRAHMOS", 0, 124, GOLD)])
        if b["mach"] <= t < b["rokna"]:
            stamp(ctx, 540, STAMP_Y, t - b["mach"], 0.03, 760, 180, GOLD,
                  [("MACH 3 SPEED", 0, 116, GOLD)])
        if b["rokna"] <= t < b["desh"]:
            blink = 1.0 if int(t * 6) % 2 else 0.6
            stamp(ctx, 540, STAMP_Y, t - b["rokna"], -0.03, 760, 170, RED, [("UNSTOPPABLE", 0, 112, shade(RED, blink))])
        if t >= b["desh"]:
            stamp(ctx, 540, STAMP_Y, t - b["desh"], 0.03, 760, 170, GOLD, [("GLOBAL DEMAND", 0, 100, GOLD)])


def _ellipse_ring(ctx, x, y, rx, ry, a):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, math.tau)
    ctx.restore()
    rgba(ctx, (1, 1, 1), 0.5 * a)
    ctx.set_line_width(6)
    ctx.stroke()


class Pinaka(Rapid):
    """Launcher raises its pods -> 12-rocket ripple fire with counter -> 4 sq km target grid
    lighting up -> ground explosions -> foreign officers watching, stunned."""
    accent = CYAN

    def beats(self, d):
        c = self.cue
        return {"name": c("PINAKA", d * 0.05), "fire": c("44", d * 0.16), "sq": c("SQ", d * 0.42),
                "tabaah": c("TABAAH", d * 0.58), "videshi": c("TAAKAT", d * 0.72), "hairan": c("HAIRAN", d * 0.9)}

    def shots(self, d):
        b = self.beats(d)
        return [(0.0, "raise_"), (b["fire"], "barrage"), (b["sq"], "grid"), (b["tabaah"], "blast"),
                (b["videshi"], "stunned")]

    def launches(self, b):
        span = max(b["sq"] - b["fire"] - 0.2, 1.2)
        return [b["fire"] + 0.1 + k * span / 12 for k in range(12)]

    def impacts(self, b):
        span = max(b["tabaah"] - b["sq"] - 0.2, 1.0)
        return [b["sq"] + 0.1 + k * span / 12 for k in range(12)]

    def events(self, d):
        b = self.beats(d)
        ev = [(0.02, "boom"), (0.2, "thud"), (b["tabaah"], "boom"), (b["tabaah"] + 0.25, "boom"),
              (b["videshi"], "zap"), (b["hairan"], "alarm")]
        ev += [(at, "thud") for at in self.launches(b)] + [(self.launches(b)[0], "whoosh")]
        ev += [(at, "soft_thud") for at in self.impacts(b)]
        return ev

    def shake(self, t, d, b):
        amp = sum(kick(t - at, 0.18, 10) for at in self.launches(b))
        return amp + kick(t - b["tabaah"], 1.0, 44) + kick(t - b["tabaah"] - 0.25, 0.8, 30)

    def desert(self, ctx, t):
        sky(ctx, ((0, "#140A1E"), (0.5, "#6B2E2A"), (0.66, "#E88A3A"), (1, "#2A1A0C")))
        glow(ctx, 760, 1250, 520, hexc("#FFB060"), 0.6)
        for k in range(3):
            ctx.move_to(-300, 1300)
            for i in range(9):
                ctx.line_to(-300 + i * 220, 1240 - 60 * k - 50 * rnd(i, k + 3))
            ctx.line_to(W + 300, 1300)
            ctx.close_path()
            rgba(ctx, shade(hexc("#5A3A1E"), 0.6 + 0.2 * k), 0.8)
            ctx.fill()
        ground(ctx, 1300, "#3A2614")

    def raise_(self, ctx, ts, t, d, b):
        self.desert(ctx, t)
        elev = 0.62 * ease_in_out((ts - 0.15) / 0.9)
        pinaka_truck(ctx, 560, 1420, 1.15, t, elev, 0)
        glow(ctx, 560, 1100, 500, CYAN, 0.12 + 0.08 * math.sin(t * 6))

    def barrage(self, ctx, ts, t, d, b):
        self.desert(ctx, t)
        launches = self.launches(b)
        fired = sum(1 for at in launches if t >= at)
        last = max((at for at in launches if t >= at), default=-9)
        px, py, ang = pinaka_truck(ctx, 560, 1420, 1.15, t, 0.62, fired, recoil=clamp(1 - (t - last) / 0.15))
        for k, at in enumerate(launches):                                   # smoke puffs linger
            u = t - at
            if u > 0:
                circle(ctx, px - 160 + 140 * rnd(k, 2) - 70 * u, py + 40 - 80 * u * rnd(k, 3),
                       60 + 140 * clamp(u / 1.5), (0.8, 0.76, 0.7), 0.4 * clamp(1 - u / 2.5))
        for k, at in enumerate(launches):                                   # rockets streak out
            u = t - at
            if 0 < u < 0.9:
                dist = 600 * u + 2200 * u * u
                off = ((k % 6) - 2.5) * 22
                rx = px + dist * math.cos(ang) - off * math.sin(ang)
                ry = py + dist * math.sin(ang) + off * math.cos(ang)
                line(ctx, [(px, py), (rx, ry)], (0.85, 0.85, 0.9), 10, 0.25 * (1 - u))
                rocket(ctx, rx, ry, ang, 1.3, t)
            if 0 <= u < 0.12:
                glow(ctx, px, py, 260, FIRE, 0.9 * (1 - u / 0.12))

    def grid(self, ctx, ts, t, d, b):
        sky(ctx, ((0, "#0C1410"), (1, "#050806")))
        for i in range(-2, 14):                                             # map grid
            line(ctx, [(i * 90, 0), (i * 90 - 120, H)], hexc("#2E4A3A"), 2, 0.5)
            line(ctx, [(-100, i * 140), (W + 100, i * 140 + 60)], hexc("#2E4A3A"), 2, 0.5)
        cx, cy, half = 540, 820, 270
        ctx.rectangle(cx - half, cy - half, 2 * half, 2 * half)
        rgba(ctx, CYAN, 0.1 + 0.06 * math.sin(t * 8))
        ctx.fill_preserve()
        rgba(ctx, CYAN)
        ctx.set_line_width(6)
        ctx.set_dash([28, 16], -t * 120)
        ctx.stroke()
        ctx.set_dash([])
        ctx.save()
        ctx.translate(cx - half - 40, cy)
        ctx.rotate(-math.pi / 2)
        text(ctx, "2 KM", 0, 0, 44, CYAN, font=CAPTION_FONT, bold=False)
        ctx.restore()
        for k, at in enumerate(self.impacts(b)):
            u = t - at
            ix = cx + (2 * rnd(k, 40) - 1) * half * 0.8
            iy = cy + (2 * rnd(k, 41) - 1) * half * 0.8
            if -0.25 < u <= 0:                                              # incoming streak
                line(ctx, [(ix + 300 * (-u / 0.25) + 60, iy - 900 * (-u / 0.25) - 160),
                           (ix + 300 * (-u / 0.25), iy - 900 * (-u / 0.25))], (1, 1, 1), 5, 0.8)
            if u > 0:
                circle(ctx, ix, iy, 60, (0.06, 0.04, 0.03), 0.7)            # scorch
                glow(ctx, ix, iy, 170 * ease_out_cubic(u / 0.25), FIRE, 0.9 * clamp(1 - u / 1.2))
                shockwave(ctx, ix, iy, u, 10, 160, hexc("#FFD36E"), 0.5, 5)

    def blast(self, ctx, ts, t, d, b):
        sky(ctx, ((0, "#1A0602"), (0.6, "#5A1A06"), (1, "#120602")))
        for k, (x, w_, h_) in enumerate(((120, 160, 120), (330, 200, 90), (620, 150, 140), (860, 220, 100))):
            rrect(ctx, x - w_ / 2, 1300 - h_, w_, h_, 10)                     # target bunkers on the horizon
            rgba(ctx, hexc("#120A06"))
            ctx.fill()
        ground(ctx, 1300, "#170D06")
        for k, (x, at, sz) in enumerate(((300, 0.0, 1.1), (760, 0.18, 1.25), (540, 0.4, 1.4), (150, 0.6, 0.8),
                                         (930, 0.75, 0.9))):
            fireball(ctx, x, 1300, ts - at, sz, seed=k * 3)
        flash(ctx, ts, 0.25, 0.8)

    def stunned(self, ctx, ts, t, d, b):
        sky(ctx, ((0, "#05030A"), (0.55, "#3A1206"), (0.68, "#FF7A1A"), (1, "#0A0402")))
        for k, x in enumerate((180, 520, 880)):                             # distant blasts keep flickering
            glow(ctx, x, 1180, 300 + 80 * math.sin(t * 9 + k), FIRE, 0.4 + 0.2 * rnd(int(t * 12), k))
        ground(ctx, 1240, "#0A0503")
        for k, (x, y, s) in enumerate(((230, 1440, 0.95), (540, 1400, 1.1), (850, 1440, 0.95))):
            officer(ctx, x, y, s, t, k)
            u = t - b["hairan"] - 0.1 * k
            if u > 0:
                pop = ease_out_back(u / 0.25)
                ctx.save()
                ctx.translate(x + 60, y - 560 * s)
                ctx.scale(pop, pop)
                text(ctx, "!", 0, 0, 120, RED, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=10)
                ctx.restore()

    def hud(self, ctx, t, d, b):
        if b["name"] <= t < b["fire"]:
            stamp(ctx, 540, STAMP_Y, t - b["name"], -0.04, 620, 170, CYAN, [("PINAKA", 0, 130, CYAN)])
        if b["fire"] <= t < b["sq"]:
            stamp(ctx, 540, STAMP_Y, t - b["fire"], 0.03, 740, 180, CYAN, [("44 SECONDS", 0, 120, CYAN)])
            fired = sum(1 for at in self.launches(b) if t >= at)
            text(ctx, f"ROCKETS {fired}/12", 540, STAMP_Y + 150, 64, (1, 1, 1), font=CAPTION_FONT, bold=False,
                 stroke=(0, 0, 0), stroke_w=10)
        if b["sq"] <= t < b["tabaah"]:
            stamp(ctx, 540, STAMP_Y, t - b["sq"], -0.03, 620, 150, CYAN, [("4 SQ KM", 0, 108, CYAN)])
        if b["tabaah"] <= t < b["videshi"]:
            stamp(ctx, 540, STAMP_Y, t - b["tabaah"], 0.04, 640, 170, FIRE, [("TABAAH!", 0, 130, FIRE)])
        if t >= b["videshi"]:
            stamp(ctx, 540, STAMP_Y, t - b["videshi"], -0.03, 780, 170, RED, [("WORLD SHOCKED", 0, 104, (1, 1, 1))])


class Outro(Rapid):
    """BRAHMOS vs PINAKA face-off -> giant flying tiranga, COMMENT JAI HIND with a bouncing arrow,
    Reality Shift subscribe badge and click."""
    accent = SAFFRON

    def beats(self, d):
        c = self.cue
        return {"vs": c("KHATARNAK", d * 0.1), "comment": c("COMMENT", d * 0.32), "jai": c("JAI", d * 0.4),
                "sub": c("SUBSCRIBE", d * 0.85)}

    def click(self, d, b):
        return min(d - 0.35, b["sub"] + 0.3)

    def shots(self, d):
        b = self.beats(d)
        return [(0.0, "versus"), (b["comment"], "tiranga")]

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["vs"], "thud"), (b["comment"], "whoosh"), (b["jai"], "dingdong"),
                (self.click(d, b), "pick"), (self.click(d, b) + 0.05, "pop")]

    def shake(self, t, d, b):
        return kick(t - b["vs"], 0.4, 22)

    def versus(self, ctx, ts, t, d, b):
        sky(ctx, ((0, "#05060C"), (1, "#020205")))
        ctx.move_to(-300, -300)                                             # diagonal split
        ctx.line_to(640, -300)
        ctx.line_to(440, H + 300)
        ctx.line_to(-300, H + 300)
        ctx.close_path()
        rgba(ctx, shade(GOLD, 0.22))
        ctx.fill()
        ctx.move_to(640, -300)
        ctx.line_to(W + 300, -300)
        ctx.line_to(W + 300, H + 300)
        ctx.line_to(440, H + 300)
        ctx.close_path()
        rgba(ctx, shade(CYAN, 0.2))
        ctx.fill()
        glow(ctx, 270, 760, 420, GOLD, 0.4)
        glow(ctx, 820, 760, 420, CYAN, 0.4)
        sl = ease_out_cubic(ts / 0.35)
        brahmos(ctx, lerp(-200, 270, sl), 1060, 0.95, t)
        ctx.save()
        ctx.translate(lerp(1300, 820, sl), 800)
        ctx.rotate(-0.9)
        for r in range(4):
            rocket(ctx, 0, (r - 1.5) * 60, 0, 2.2, t, burn=0.6)
        ctx.restore()
        line(ctx, [(640, 300), (500, 760), (600, 760), (440, 1150)], (1, 1, 1), 8, 0.8)
        u = ts - 0.25
        if u > 0:
            pop = ease_out_back(u / 0.25, 2.6)
            ctx.save()
            ctx.translate(540, 760)
            ctx.scale(pop, pop)
            glow(ctx, 0, 0, 200, RED, 0.6)
            text(ctx, "VS", 0, 0, 180, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=RED, stroke_w=16)
            ctx.restore()
        label(ctx, "BRAHMOS", 270, 640, ts - 0.4, size=56, c=GOLD)
        label(ctx, "PINAKA", 820, 640, ts - 0.5, size=56, c=CYAN)

    def tiranga(self, ctx, ts, t, d, b):
        sky(ctx, ((0, "#0A2A6B"), (0.6, "#4D8BD6"), (1, "#BFE0FF")))
        for i in range(6):                                                  # clouds drifting by
            cx = (rnd(i, 1) * (W + 600) - t * 160) % (W + 600) - 300
            cy = 300 + 1100 * rnd(i, 2)
            for j in range(4):
                circle(ctx, cx + j * 70, cy + 20 * math.sin(j), 70 + 20 * (j % 3), (1, 1, 1), 0.25)
        fly = ease_out_cubic(ts / 0.5)
        line(ctx, [(140, lerp(1500, 560, fly) - 30), (140, H + 100)], hexc("#D9D9D9"), 14)
        flag(ctx, 150, lerp(1500, 560, fly), 820, 540, "in", t * 1.6, pole=0)
        for i in range(40):                                                 # tricolor confetti
            fy = (rnd(i, 1) * H + t * (260 + 160 * rnd(i, 2))) % H
            fx = rnd(i, 3) * W + 40 * math.sin(t * 2 + i)
            ctx.save()
            ctx.translate(fx, fy)
            ctx.rotate(t * (2 + 3 * rnd(i, 4)) + i)
            ctx.rectangle(-9, -5, 18, 10)
            rgba(ctx, TRICOLOR[i % 3], 0.9)
            ctx.fill()
            ctx.restore()

    def hud(self, ctx, t, d, b):
        if b["vs"] <= t < b["comment"]:
            stamp(ctx, 540, STAMP_Y, t - b["vs"], -0.03, 860, 170, RED, [("KAUN ZYADA KHATARNAK?", 0, 76, (1, 1, 1))])
            return
        u = t - b["comment"]
        if u < 0:
            return
        pop = max(ease_out_back(u / 0.3), 1e-3) * (1 + 0.05 * math.sin(t * 8))
        ctx.save()
        ctx.translate(500, 380)
        ctx.scale(pop, pop)
        ctx.rotate(-0.03)
        glow(ctx, 0, 0, 400, SAFFRON, 0.4)
        text(ctx, "COMMENT", 0, -70, 96, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=12)
        text(ctx, "JAI HIND", 0, 60, 150, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
        ctx.restore()
        if u > 0.2:                                                         # bouncing down arrow (the emoji cue)
            by = 300 + 30 * abs(math.sin(t * 7))
            ctx.save()
            ctx.translate(930, by)
            ctx.scale(pop, pop)
            ctx.move_to(-34, -110)
            ctx.line_to(34, -110)
            ctx.line_to(34, 0)
            ctx.line_to(80, 0)
            ctx.line_to(0, 90)
            ctx.line_to(-80, 0)
            ctx.line_to(-34, 0)
            ctx.close_path()
            rgba(ctx, GOLD)
            ctx.fill_preserve()
            rgba(ctx, (0, 0, 0))
            ctx.set_line_width(8)
            ctx.stroke()
            ctx.restore()
        clicked = t >= self.click(d, b)
        bx, by = subscribe_badge(ctx, 540, 1400, t, clicked)
        cu = clamp((t - (self.click(d, b) - 0.7)) / 0.6)
        if cu > 0:
            cx, cy = lerp(1000, bx + 20, ease_in_out(cu)), lerp(1500, by + 20, ease_in_out(cu))
            sc = 0.85 if abs(t - self.click(d, b)) < 0.12 else 1.0
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


SCENE_CLASSES = {"hook": Hook, "brahmos": BrahMos, "pinaka": Pinaka, "outro": Outro}
