"""Story: Reality Shift — S-400 vs DRDO's Project Kusha (India's layered air-defence shield).

Same rapid hard-cut camera as reality_shift_weapons, but every scene keeps its own framing
family: wide (hook), progressive zoom-in (S-400), tilted side angle (Kusha), centred hero
(outro). Captions sit in the 1150-1250 px band; nothing with text is drawn in the bottom
400 px (YouTube UI). Music stays at a flat 15 % under the voice (no ducking).
"""

import math

import cairo

from engine import *  # noqa: F401,F403
from stories.reality_shift import GOLD, SAFFRON, SIL, TRICOLOR, _ellipse, chakra, flag, stamp
from stories.reality_shift_defense import flash, label
from stories.reality_shift_weapons import CYAN, FIRE, RED, Rapid, fireball, ground, kick, shockwave, sky

TOPIC = "S-400 VS PROJECT KUSHA"
OUTPUTS = {"edge": "reality_shift_project_kusha.mp4", "elevenlabs": "reality_shift_project_kusha_el.mp4"}
WATERMARK = "Reality Shift"

CLEAN_PUNCTUATION = False
MAX_GAP = 0.12             # zero dead air
TAIL_PAD = 0.0
TRIM = {"thresh": 0.006, "keep": 0.05, "keep_tail": 0.08}
MUSIC_BPM = 120
MUSIC_DUCK = 0.0           # drum/drone bed held at exactly MUSIC_VOLUME (15 %)
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"

CAPTION_Y = 1200           # centre of the 1150-1250 safe band
CAPTION_SIZE = 100
HOT_COLOR = GOLD
HOT_COLORS = {"S-400": GOLD, "SUDARSHAN": GOLD, "CHAKRA": GOLD, "400": GOLD, "KM": GOLD,
              "DRDO": CYAN, "PROJECT": CYAN, "KUSHA": CYAN, "IRON": CYAN, "DOME": CYAN,
              "150": CYAN, "250": CYAN, "350": CYAN, "3": CYAN, "LAYERS": CYAN}

NARRATION = {
    "hook": "क्या आपको पता है? भारत का आसमान अब दुश्मन के लिए एक अभेद्य किला बन चुका है!",
    "s400": "पहला— एस चार सौ, जिसे वायुसेना कहती है सुदर्शन चक्र! स्टेल्थ जेट्स हों या सुपरसोनिक मिसाइलें, "
            "चार सौ किलोमीटर दूर से ही काम तमाम!",
    "kusha": "लेकिन असली खेल तो डीआरडीओ का प्रोजेक्ट कुशा है! भारत का अपना देसी आयरन डोम, जो डेढ़ सौ, "
             "ढाई सौ और साढ़े तीन सौ किलोमीटर की तीन परतों में दुश्मन को भून डालेगा!",
    "outro": "मतलब अब सुरक्षा के लिए किसी पर निर्भर नहीं रहना। क्या देसी कुशा एस चार सौ से बेहतर साबित होगा? "
             "कमेंट में 'जय हिंद' लिखकर बताएं!",
}

CHUNKS = {
    "hook": [
        ("क्या आपको पता है?", "KYA AAPKO PATA HAI?"),
        ("भारत का आसमान", "BHARAT KA AASMAAN"),
        ("अब दुश्मन के लिए", "AB DUSHMAN KE LIYE"),
        ("एक अभेद्य किला", "EK ABHEDYA KILA"),
        ("बन चुका है!", "BAN CHUKA HAI!"),
    ],
    "s400": [
        ("पहला—", "PEHLA!"),
        ("एस चार सौ,", "S-400"),
        ("जिसे वायुसेना कहती है", "JISE VAYUSENA KEHTI HAI"),
        ("सुदर्शन चक्र!", "SUDARSHAN CHAKRA!"),
        ("स्टेल्थ जेट्स हों", "STEALTH JETS HON"),
        ("या सुपरसोनिक मिसाइलें,", "YA SUPERSONIC MISSILES"),
        ("चार सौ किलोमीटर", "400 KM"),
        ("दूर से ही", "DOOR SE HI"),
        ("काम तमाम!", "KAAM TAMAAM!"),
    ],
    "kusha": [
        ("लेकिन असली खेल तो", "LEKIN ASLI KHEL TO"),
        ("डीआरडीओ का", "DRDO KA"),
        ("प्रोजेक्ट कुशा है!", "PROJECT KUSHA HAI!"),
        ("भारत का अपना", "BHARAT KA APNA"),
        ("देसी आयरन डोम,", "DESI IRON DOME"),
        ("जो डेढ़ सौ,", "JO 150,"),
        ("ढाई सौ", "250"),
        ("और साढ़े तीन सौ किलोमीटर", "AUR 350 KM"),
        ("की तीन परतों में", "KI 3 LAYERS MEIN"),
        ("दुश्मन को", "DUSHMAN KO"),
        ("भून डालेगा!", "BHOON DAALEGA!"),
    ],
    "outro": [
        ("मतलब अब सुरक्षा के लिए", "MATLAB AB SURAKSHA KE LIYE"),
        ("किसी पर निर्भर", "KISI PAR NIRBHAR"),
        ("नहीं रहना।", "NAHI REHNA!"),
        ("क्या देसी कुशा", "KYA DESI KUSHA"),
        ("एस चार सौ से", "S-400 SE"),
        ("बेहतर साबित होगा?", "BEHTAR SABIT HOGA?"),
        ("कमेंट में", "COMMENT MEIN"),
        ("'जय हिंद'", "'JAI HIND'"),
        ("लिखकर बताएं!", "LIKHKAR BATAYEIN!"),
    ],
}

HOT_WORDS = {"ABHEDYA", "KILA", "S-400", "SUDARSHAN", "CHAKRA", "STEALTH", "SUPERSONIC", "400", "KM", "TAMAAM",
             "DRDO", "PROJECT", "KUSHA", "IRON", "DOME", "150", "250", "350", "3", "LAYERS", "BHOON",
             "NIRBHAR", "BEHTAR", "JAI", "HIND"}

for _key, _chunks in CHUNKS.items():
    assert " ".join(h for h, _ in _chunks) == NARRATION[_key], f"caption chunks drift from narration: {_key}"

SCRIPT = [(key, CHUNKS[key]) for key in NARRATION]

RADAR = hexc("#22C55E")
STAMP_Y = 330              # all HUD text lives in the top third, clear of captions and the YouTube UI

# per-scene re-frame cycles: (zoom, dx, dy, roll)
WIDE = ((1.02, 0, 0, 0.0), (1.06, -30, -20, 0.006), (1.04, 30, 25, -0.006))
ZOOM_IN = ((1.04, 0, 0, 0.0), (1.1, 0, 20, 0.01), (1.16, -20, 30, -0.01), (1.22, 0, 40, 0.0),
           (1.12, 25, 10, 0.012), (1.26, 0, 40, -0.008))
SIDE = ((1.1, -50, 0, 0.035), (1.16, -80, -40, 0.045), (1.12, -30, 30, 0.03))
HERO = ((1.04, 0, 0, 0.0), (1.1, 0, -20, 0.0), (1.07, 0, 15, 0.0))


def blend(a, b, u):
    return tuple(lerp(x, y, clamp(u)) for x, y in zip(a, b))


def stars(ctx, n=70, ymax=H):
    for i in range(n):
        circle(ctx, rnd(i, 1) * W, rnd(i, 2) * ymax, 1 + 2 * rnd(i, 3), (1, 1, 1), 0.2 + 0.5 * rnd(i, 4))


# ============================================================ map, dome, icons

# India's outline as (lon, lat), clockwise from Kashmir
INDIA = ((74.5, 37.0), (77.8, 35.5), (79.0, 34.5), (78.8, 32.5), (79.5, 31.0), (81.0, 30.2), (84.0, 28.6),
         (88.0, 27.9), (88.2, 26.7), (89.8, 26.8), (92.0, 27.8), (95.5, 29.2), (97.2, 28.2), (96.0, 27.3),
         (95.0, 26.0), (94.6, 24.8), (93.3, 23.5), (92.6, 22.0), (91.8, 23.6), (91.2, 23.8), (92.0, 25.1),
         (90.0, 25.2), (89.0, 26.0), (88.7, 24.3), (88.9, 22.0), (87.0, 21.5), (86.5, 20.0), (84.8, 19.2),
         (82.3, 16.6), (80.3, 15.5), (80.2, 13.5), (79.8, 11.0), (79.3, 10.3), (78.2, 8.9), (77.5, 8.1),
         (76.5, 9.5), (75.8, 11.5), (74.8, 13.0), (73.9, 15.5), (73.0, 17.8), (72.8, 19.5), (72.6, 21.2),
         (70.5, 20.8), (69.0, 22.3), (70.2, 22.9), (68.4, 23.6), (70.0, 24.4), (71.0, 24.7), (69.6, 27.0),
         (71.5, 28.0), (73.5, 29.8), (74.6, 30.9), (73.7, 32.2), (74.4, 33.5), (73.8, 34.5))


def india_path(ctx, cx, cy, k):
    for i, (lon, lat) in enumerate(INDIA):
        p = (cx + (lon - 82.75) * k, cy + (22.5 - lat) * k * 1.05)
        ctx.move_to(*p) if i == 0 else ctx.line_to(*p)
    ctx.close_path()


def india_map(ctx, cx, cy, k, t, fill=hexc("#0B2A3A"), edge=SAFFRON, a=1.0):
    india_path(ctx, cx, cy, k)
    rgba(ctx, fill, 0.9 * a)
    ctx.fill_preserve()
    rgba(ctx, edge, 0.3 * a)
    ctx.set_line_width(16)
    ctx.stroke_preserve()
    rgba(ctx, edge, (0.8 + 0.2 * math.sin(t * 6)) * a)
    ctx.set_line_width(4)
    ctx.stroke()


def dome_pt(cx, cy, r, h, th, ph):
    """Screen point on a hemisphere (base ellipse squashed 0.5) at elevation th, azimuth ph."""
    return cx + r * math.cos(th) * math.cos(ph), cy + 0.5 * r * math.cos(th) * math.sin(ph) - h * math.sin(th)


def dome(ctx, cx, cy, r, h, t, c, a=1.0):
    """Glowing wireframe force-field hemisphere over (cx, cy)."""
    if r < 2 or h < 2:
        return
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(r, h)
    ctx.arc(0, 0, 1, math.pi, math.tau)
    ctx.restore()
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(r, 0.5 * r)
    ctx.arc(0, 0, 1, 0, math.pi)
    ctx.restore()
    g = cairo.LinearGradient(0, cy - h, 0, cy + 0.5 * r)
    g.add_color_stop_rgba(0, c[0], c[1], c[2], 0.28 * a)
    g.add_color_stop_rgba(1, c[0], c[1], c[2], 0.06 * a)
    ctx.set_source(g)
    ctx.fill()
    for k in range(12):  # rotating meridians, the near side brighter
        ph = k / 12 * math.tau + t * 0.35
        pts = [dome_pt(cx, cy, r, h, j / 12 * math.pi / 2, ph) for j in range(13)]
        line(ctx, pts, c, 2.5, (0.55 if math.sin(ph) > 0 else 0.15) * a)
    for th in (0.3, 0.65, 1.0, 1.3):
        _ellipse(ctx, cx, cy - h * math.sin(th), r * math.cos(th), 0.5 * r * math.cos(th))
        rgba(ctx, c, 0.3 * a)
        ctx.set_line_width(2)
        ctx.stroke()
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(r, h)
    ctx.arc(0, 0, 1, math.pi, math.tau)
    ctx.restore()
    rgba(ctx, c, 0.9 * a)
    ctx.set_line_width(5)
    ctx.stroke()
    glow(ctx, cx, cy - h, 160, c, 0.35 * a * (1 + 0.3 * math.sin(t * 4)))


def shield_icon(ctx, x, y, s, c):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(0, -50)
    ctx.curve_to(18, -38, 34, -36, 46, -40)
    ctx.line_to(46, 0)
    ctx.curve_to(46, 30, 20, 48, 0, 58)
    ctx.curve_to(-20, 48, -46, 30, -46, 0)
    ctx.line_to(-46, -40)
    ctx.curve_to(-34, -36, -18, -38, 0, -50)
    ctx.close_path()
    rgba(ctx, c)
    ctx.fill_preserve()
    rgba(ctx, (0, 0, 0))
    ctx.set_line_width(6)
    ctx.stroke()
    line(ctx, [(-22, -2), (-4, 18), (24, -20)], (0.04, 0.04, 0.06), 10)
    ctx.restore()


def down_arrow(ctx, x, y, s, c):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for px, py in ((-34, -110), (34, -110), (34, 0), (80, 0), (0, 90), (-80, 0), (-34, 0)):
        ctx.line_to(px, py)
    ctx.close_path()
    rgba(ctx, c)
    ctx.fill_preserve()
    rgba(ctx, (0, 0, 0))
    ctx.set_line_width(8)
    ctx.stroke()
    ctx.restore()


def sudarshan(ctx, x, y, r, rot, a=1.0):
    """Spinning Sudarshan Chakra emblem: serrated blazing rim around a spoked wheel."""
    if a <= 0:
        return
    glow(ctx, x, y, r * 1.9, GOLD, 0.5 * a)
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    for k in range(16):
        a0 = k / 16 * math.tau
        ctx.move_to(r * 0.9 * math.cos(a0), r * 0.9 * math.sin(a0))
        ctx.line_to(r * 1.28 * math.cos(a0 + 0.12), r * 1.28 * math.sin(a0 + 0.12))
        ctx.line_to(r * 0.9 * math.cos(a0 + 0.36), r * 0.9 * math.sin(a0 + 0.36))
        ctx.close_path()
        rgba(ctx, FIRE, a)
        ctx.fill()
    ctx.restore()
    ctx.push_group()
    chakra(ctx, x, y, r, -rot * 0.6, c=GOLD)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(a)


def stealth_jet(ctx, x, y, s, rot, c, a=1.0):
    """Top-down stealth fighter silhouette, nose along -y before rotation."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    for i, (px, py) in enumerate(((0, -60), (14, -30), (18, -5), (58, 18), (60, 30), (20, 26), (26, 48),
                                  (10, 46), (0, 40), (-10, 46), (-26, 48), (-20, 26), (-60, 30), (-58, 18),
                                  (-18, -5), (-14, -30))):
        ctx.move_to(px, py) if i == 0 else ctx.line_to(px, py)
    ctx.close_path()
    rgba(ctx, c, a)
    ctx.fill()
    ctx.restore()


def sam(ctx, x, y, ang, s, t, burn=1.0, nose=RED, body=(0.88, 0.9, 0.93)):
    """Surface-to-air missile, nose along angle ang, with plume and glow."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(s, s)
    if burn > 0:
        f = burn * (1 + 0.3 * math.sin(t * 60 + x))
        glow(ctx, -120, 0, 120 * f, FIRE, 0.85)
        ctx.move_to(-110, -12)
        ctx.line_to(-110 - 170 * f, 0)
        ctx.line_to(-110, 12)
        ctx.close_path()
        rgba(ctx, hexc("#FFE08A"))
        ctx.fill()
    rrect(ctx, -112, -13, 190, 26, 8)
    rgba(ctx, body)
    ctx.fill()
    ctx.move_to(76, -13)
    ctx.curve_to(100, -12, 118, -4, 124, 0)
    ctx.curve_to(118, 4, 100, 12, 76, 13)
    ctx.close_path()
    rgba(ctx, nose)
    ctx.fill()
    for side in (-1, 1):
        for fx in (-112, 10):
            ctx.move_to(fx, side * 13)
            ctx.line_to(fx - 14, side * 32)
            ctx.line_to(fx + 26, side * 13)
            ctx.close_path()
            rgba(ctx, shade(body, 0.7))
            ctx.fill()
    ctx.restore()


def tel(ctx, x, y, s, t, elev, body=hexc("#3E4A2A"), stripe=None, mono=None):
    """Side view of a canister transporter-erector-launcher facing right, (x, y) on the ground
    under its centre. elev 0 = canisters stowed, pi/2 = upright; mono paints it all one colour
    (horizon silhouettes). Returns the front canister's muzzle in user space."""
    col = (lambda c: mono) if mono is not None else (lambda c: c)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for wx in (-300, -190, 170, 280):
        circle(ctx, wx, -60, 60, col(hexc("#15171B")))
        circle(ctx, wx, -60, 26, col(hexc("#4A4F57")))
    rrect(ctx, -400, -150, 740, 70, 10)
    rgba(ctx, col(body))
    ctx.fill()
    ctx.move_to(260, -150)
    ctx.line_to(260, -320)
    ctx.line_to(380, -320)
    ctx.line_to(430, -230)
    ctx.line_to(430, -150)
    ctx.close_path()
    rgba(ctx, col(shade(body, 1.15)))
    ctx.fill()
    if mono is None:
        ctx.move_to(285, -300)
        ctx.line_to(370, -300)
        ctx.line_to(405, -240)
        ctx.line_to(285, -240)
        ctx.close_path()
        rgba(ctx, hexc("#8FC6E0"), 0.85)
        ctx.fill()
    a = -elev
    line(ctx, [(-120, -150), (-360 + 300 * math.cos(a) + 40 * math.sin(a), -170 + 300 * math.sin(a))],
         col(hexc("#2A2F22")), 22)                                         # hydraulic ram
    ctx.save()
    ctx.translate(-360, -170)
    ctx.rotate(a)
    for k in range(2):                                                     # back + front canister pair
        rrect(ctx, 0, -100 + k * 48, 600, 44, 12)
        rgba(ctx, col(shade(body, 0.8 + 0.35 * k)))
        ctx.fill()
        if stripe and mono is None:
            for j, c in enumerate(stripe):
                ctx.rectangle(420 + j * 30, -100 + k * 48, 30, 44)
                rgba(ctx, c)
                ctx.fill()
        rrect(ctx, 588, -102 + k * 48, 22, 48, 6)
        rgba(ctx, col(hexc("#1C1F18")))
        ctx.fill()
    ctx.restore()
    ctx.restore()
    lx, ly = 600, -55
    return (x + s * (-360 + lx * math.cos(a) - ly * math.sin(a)),
            y + s * (-170 + lx * math.sin(a) + ly * math.cos(a)))


def radar_mast(ctx, x, y, s, t, c, kind="panel", k=0):
    """Rotating air-defence radar on a mast, (x, y) on the ground: flat 'panel' array or 'dish'."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    line(ctx, [(0, 0), (0, -240)], c, 22)
    line(ctx, [(-70, 0), (0, -120), (70, 0)], c, 12)
    spin = math.cos(t * 1.6 + k * 1.3)
    if kind == "panel":
        rrect(ctx, -110 * abs(spin) - 6, -400, 220 * abs(spin) + 12, 170, 8)
        rgba(ctx, c)
        ctx.fill()
    else:
        ctx.save()
        ctx.translate(0, -300)
        ctx.scale(max(abs(spin), 0.08), 1)
        ctx.arc(0, 0, 110, math.pi * 0.15, math.pi * 0.85)
        ctx.arc_negative(0, -60, 90, math.pi * 0.85, math.pi * 0.15)
        ctx.close_path()
        rgba(ctx, c)
        ctx.fill()
        ctx.restore()
        line(ctx, [(0, -300), (0, -380)], c, 8)
    ctx.restore()


def pointing_jawan(ctx, x, y, s, t, rim=CYAN):
    """Air-defence officer in an alert stance, beret on, right arm thrust out pointing right;
    (x, y) at the feet. Returns the fingertip in user space."""
    aim = 8 * math.sin(t * 2.2)

    def body(c, a=1.0):
        line(ctx, [(-28, -230), (-78, 0)], c, 46, a)
        line(ctx, [(28, -230), (86, 0)], c, 46, a)
        rrect(ctx, -80, -470, 160, 260, 40)
        rgba(ctx, c, a)
        ctx.fill()
        line(ctx, [(-76, -450), (-112, -340), (-70, -262)], c, 38, a)         # arm holding the tablet
        rrect(ctx, -110, -300, 74, 92, 8)
        rgba(ctx, c, a)
        ctx.fill()
        line(ctx, [(70, -448), (190, -480 + aim * 0.5), (300, -515 + aim)], c, 38, a)
        line(ctx, [(300, -515 + aim), (346, -530 + aim)], c, 14, a)            # pointing finger
        rrect(ctx, -20, -500, 40, 40, 10)                                      # neck
        rgba(ctx, c, a)
        ctx.fill()
        circle(ctx, 4, -530, 50, c, a)
        ctx.move_to(50, -540)                                                  # nose / chin profile
        ctx.line_to(66, -520)
        ctx.line_to(48, -512)
        rgba(ctx, c, a)
        ctx.fill()
        ctx.save()
        ctx.translate(-10, -572)
        ctx.rotate(-0.22)
        ctx.scale(70, 26)
        ctx.arc(0, 0, 1, 0, math.tau)
        ctx.restore()
        rgba(ctx, c, a)
        ctx.fill()

    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for ox in (-8, 8):
        ctx.save()
        ctx.translate(ox, -6)
        body(rim, 0.85)
        ctx.restore()
    body(SIL)
    glow(ctx, -73, -254, 70, rim, 0.5)                                         # tablet screen glow
    ctx.restore()
    return x + s * 346, y + s * (-530 + aim)


# ============================================================ scenes

class Hook(Rapid):
    """Wide: India's map on a perspective ground plane with a radar sweep, a glowing 3D dome
    building over it; enemy missiles shatter on the dome, which flashes gold on KILA."""
    accent = CYAN
    frames = WIDE

    def beats(self, d):
        c = self.cue
        return {"bharat": c("BHARAT", d * 0.25), "dushman": c("DUSHMAN", d * 0.5), "kila": c("KILA", d * 0.72)}

    def shots(self, d):
        b = self.beats(d)
        return [(0.0, "shield"), (b["bharat"], "shield"), (b["dushman"], "shield"), (b["kila"], "shield")]

    def impacts(self, d, b):
        return [min(d - 0.1, b["dushman"] + 0.35 + 0.28 * k) for k in range(4)]

    def events(self, d):
        b = self.beats(d)
        ev = [(0.0, "boom"), (0.05, "zap"), (0.3, "beep"), (b["bharat"], "whoosh"), (b["bharat"] + 0.5, "beep"),
              (b["kila"], "boom"), (b["kila"] + 0.05, "kaching")]
        return ev + [(at, "thud") for at in self.impacts(d, b)]

    def shake(self, t, d, b):
        return kick(t, 0.6, 30) + sum(kick(t - at, 0.25, 12) for at in self.impacts(d, b)) + \
            kick(t - b["kila"], 0.8, 30)

    def shield(self, ctx, ts, t, d, b):
        sky(ctx, ((0, "#01030C"), (0.55, "#06122B"), (1, "#020409")))
        stars(ctx, 80, 900)
        cx, cy = 540, 1000
        ctx.save()
        ctx.translate(cx, cy)
        ctx.scale(1, 0.5)                                                   # tilted ground plane
        for i in range(-9, 10):
            line(ctx, [(i * 90, -760), (i * 90, 760)], CYAN, 2, 0.12)
            line(ctx, [(-900, i * 90), (900, i * 90)], CYAN, 2, 0.12)
        india_map(ctx, 0, 0, 24, t)
        sweep = t * 3.2
        ctx.move_to(0, 0)
        ctx.arc(0, 0, 520, sweep - 0.7, sweep)
        ctx.close_path()
        rgba(ctx, RADAR, 0.28)
        ctx.fill()
        line(ctx, [(0, 0), (520 * math.cos(sweep), 520 * math.sin(sweep))], RADAR, 4, 0.8)
        for k in range(1, 4):
            ctx.arc(0, 0, 170 * k, 0, math.tau)
            rgba(ctx, RADAR, 0.25)
            ctx.set_line_width(3)
            ctx.stroke()
        ctx.restore()
        grow = ease_out_cubic(t / 0.9)
        gold = clamp((t - b["kila"]) / 0.3)
        r, h = 480 * grow, 520 * grow
        dome(ctx, cx, cy, r, h, t, blend(CYAN, GOLD, gold), 1.0)
        for k, at in enumerate(self.impacts(d, b)):                         # enemy missiles break on the dome
            th, ph = 0.5 + 0.25 * (k % 2), 0.6 + 0.65 * k
            hx, hy = dome_pt(cx, cy, r, h, th, ph)
            sx, sy = (-200, 150) if k % 2 == 0 else (W + 200, 220)
            v = clamp((t - (at - 0.6)) / 0.6)
            if 0 < v < 1:
                px, py = lerp(sx, hx, v), lerp(sy, hy, v)
                line(ctx, [(lerp(sx, px, 0.7), lerp(sy, py, 0.7)), (px, py)], RED, 8, 0.6)
                glow(ctx, px, py, 60, RED, 0.9)
                circle(ctx, px, py, 10, (1, 1, 1))
            u = t - at
            if u >= 0:
                glow(ctx, hx, hy, 200 * ease_out_cubic(u / 0.2), FIRE, 0.9 * clamp(1 - u / 0.8))
                shockwave(ctx, hx, hy, u, 10, 220, blend(CYAN, GOLD, gold), 0.6, 6)
        if t >= b["kila"]:
            shockwave(ctx, cx, cy - h * 0.5, t - b["kila"], 100, 900, GOLD, 0.9, 14)
            flash(ctx, t - b["kila"], 0.2, 0.5)

    def hud(self, ctx, t, d, b):
        u = t - 0.1
        stamp(ctx, 540, STAMP_Y, u, -0.03, 900, 170, CYAN, [("INDIA'S SKY SHIELD", 0, 92, (1, 1, 1))])
        if u > 0.2:
            pop = max(ease_out_back((u - 0.2) / 0.3, 2.2), 1e-3)
            shield_icon(ctx, 975, STAMP_Y - 70, 1.15 * pop, GOLD if t >= b["kila"] else CYAN)


class S400(Rapid):
    """Dynamic zoom-in: S-400 launcher raises its canisters -> cold launch through a spinning
    Sudarshan Chakra -> radar scope tracking stealth jets and missiles -> 400 KM LOCK pop-up
    on a stealth jet -> intercept fireball."""
    accent = GOLD
    frames = ZOOM_IN

    def beats(self, d):
        c = self.cue
        return {"name": c("S-400", d * 0.08), "sud": c("SUDARSHAN", d * 0.3), "stealth": c("STEALTH", d * 0.45),
                "sonic": c("SUPERSONIC", d * 0.56), "lock": c("400 KM", d * 0.7), "tamaam": c("TAMAAM", d * 0.9)}

    def shots(self, d):
        b = self.beats(d)
        return [(0.0, "launcher"), (b["sud"], "launch"), (b["stealth"], "scope"), (b["lock"], "lock"),
                (b["tamaam"], "kill")]

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (0.35, "thud"), (b["name"], "zap"), (b["sud"], "boom"), (b["sud"] + 0.25, "whoosh"),
                (b["sud"] + 0.9, "whoosh"), (b["stealth"], "beep"), (b["stealth"] + 0.35, "beep"),
                (b["sonic"], "alarm"), (b["lock"], "beep"), (b["lock"] + 0.45, "pick"), (b["lock"] + 0.5, "zap"),
                (b["tamaam"], "boom"), (b["tamaam"] + 0.2, "boom")]

    def shake(self, t, d, b):
        return kick(t, 0.5, 24) + kick(t - b["sud"], 0.6, 30) + kick(t - b["tamaam"], 0.9, 42)

    def night(self, ctx, t):
        sky(ctx, ((0, "#030616"), (0.6, "#14224A"), (0.72, "#A8461A"), (1, "#05070C")))
        stars(ctx, 60, 1100)
        radar_mast(ctx, 930, 1400, 0.8, t, hexc("#1A2030"))
        ground(ctx, 1400, "#070A10")

    def launcher(self, ctx, ts, t, d, b):
        self.night(ctx, t)
        elev = math.pi / 2 * ease_in_out((ts - 0.2) / 1.3)
        mx, my = tel(ctx, 500, 1400, 0.95, t, elev)
        glow(ctx, mx, my, 120, GOLD, 0.25 + 0.15 * math.sin(t * 8))

    def launch(self, ctx, ts, t, d, b):
        self.night(ctx, t)
        sudarshan(ctx, 540, 560, 170, t * 4, clamp((ts - 0.1) / 0.3))
        mx, my = tel(ctx, 500, 1400, 0.95, t, math.pi / 2)
        for k, at in enumerate((0.0, 0.9)):                                 # cold launch, then ignition
            u = ts - at
            if u < 0:
                continue
            ox = mx - 46 * k
            y = my - 220 * clamp(u / 0.25) if u < 0.25 else my - 220 - 500 * (u - 0.25) - 2600 * (u - 0.25) ** 2
            if u > 0.25:
                for j in range(12):                                         # smoke column
                    sy = lerp(my, y + 140, j / 11)
                    circle(ctx, ox + 14 * math.sin(j + t * 3), sy, 30 + 50 * (1 - j / 11), (0.72, 0.72, 0.76), 0.2)
                glow(ctx, ox, my, 260 * clamp(1 - (u - 0.25) / 0.6), FIRE, 0.7)
            if y > -300:
                sam(ctx, ox, y, -math.pi / 2, 1.1, t, burn=1.0 if u > 0.25 else 0.0)

    def scope(self, ctx, ts, t, d, b):
        sky(ctx, ((0, "#021008"), (1, "#000502")))
        cx, cy, r = 540, 800, 360
        circle(ctx, cx, cy, r, hexc("#04230F"))
        for k in range(1, 5):
            ctx.arc(cx, cy, r * k / 4, 0, math.tau)
            rgba(ctx, GOLD if k == 4 else RADAR, 0.8 if k == 4 else 0.35)
            ctx.set_line_width(5 if k == 4 else 3)
            ctx.stroke()
        line(ctx, [(cx - r, cy), (cx + r, cy)], RADAR, 2, 0.35)
        line(ctx, [(cx, cy - r), (cx, cy + r)], RADAR, 2, 0.35)
        sweep = t * 5
        ctx.move_to(cx, cy)
        ctx.arc(cx, cy, r, sweep - 0.6, sweep)
        ctx.close_path()
        rgba(ctx, RADAR, 0.3)
        ctx.fill()
        targets = [(at, ang, s, kind) for at, ang, s, kind in
                   ((b["stealth"], -2.4, 0.08, "jet"), (b["stealth"] + 0.2, -0.7, 0.07, "jet"),
                    (b["stealth"] + 0.35, -1.6, 0.09, "jet"), (b["sonic"], -0.2, 0.3, "msl"),
                    (b["sonic"] + 0.15, -2.9, 0.28, "msl"))]
        for k, (at, ang, speed, kind) in enumerate(targets):
            u = t - at
            if u < 0:
                continue
            dist = r * (1.0 - speed * u)
            px, py = cx + dist * math.cos(ang), cy + dist * math.sin(ang)
            if kind == "jet":
                stealth_jet(ctx, px, py, 0.6, ang - math.pi / 2, RADAR)
            else:
                line(ctx, [(px, py), (px + 90 * math.cos(ang), py + 90 * math.sin(ang))], RED, 6, 0.6)
                circle(ctx, px, py, 10, RED)
            if u > 0.2:                                                     # lock brackets snap on
                bs = lerp(80, 46, ease_out_cubic((u - 0.2) / 0.2))
                col = RED if kind == "msl" else GOLD
                for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                    line(ctx, [(px + sx * bs, py + sy * bs * 0.5), (px + sx * bs, py + sy * bs),
                               (px + sx * bs * 0.5, py + sy * bs)], col, 4)
        label(ctx, "400 KM", cx + r * math.cos(-0.45), cy + r * math.sin(-0.45), ts, size=40)

    def sky_high(self, ctx, t):
        sky(ctx, ((0, "#050B22"), (0.6, "#1A2E5C"), (1, "#0A1024")))
        for i in range(8):                                                  # clouds rushing past
            cy = 200 + 1200 * rnd(i, 2)
            cx = (rnd(i, 1) * (W + 800) - t * 900) % (W + 800) - 400
            for j in range(4):
                circle(ctx, cx + j * 80, cy + 18 * math.sin(j), 60 + 20 * (j % 3), (0.7, 0.75, 0.9), 0.08)

    def lock(self, ctx, ts, t, d, b):
        self.sky_high(ctx, t)
        jx, jy = 540 + 20 * math.sin(t * 2), 600 + 10 * math.sin(t * 3)
        stealth_jet(ctx, jx, jy, 3.2, math.pi * 0.06, hexc("#0B0F1A"))
        glow(ctx, jx, jy + 170, 60, FIRE, 0.6)
        bs = lerp(420, 240, ease_out_cubic(ts / 0.4))
        col = RED if int(t * 8) % 2 else GOLD
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            line(ctx, [(jx + sx * bs, jy + sy * bs * 0.6), (jx + sx * bs, jy + sy * bs),
                       (jx + sx * bs * 0.6, jy + sy * bs)], col, 8)
        line(ctx, [(jx - bs * 0.3, jy), (jx + bs * 0.3, jy)], col, 3, 0.7)
        line(ctx, [(jx, jy - bs * 0.3), (jx, jy + bs * 0.3)], col, 3, 0.7)
        v = clamp((ts - 0.2) / 1.2)                                         # interceptor streak closing in
        ix, iy = lerp(160, jx - 60, v), lerp(1500, jy + 160, v)
        ang = math.atan2(jy + 160 - 1500, jx - 60 - 160)
        line(ctx, [(160, 1500), (ix, iy)], (0.9, 0.9, 0.95), 10, 0.3)
        sam(ctx, ix, iy, ang, 0.8, t)
        u = ts - 0.35
        if u > 0:                                                           # 400 KM LOCK pop-up
            pop = max(ease_out_back(u / 0.25, 2.4), 1e-3)
            ctx.save()
            ctx.translate(540, 960)
            ctx.scale(pop, pop)
            rrect(ctx, -330, -95, 660, 190, 22)
            rgba(ctx, (0.02, 0.02, 0.05), 0.85)
            ctx.fill_preserve()
            rgba(ctx, GOLD)
            ctx.set_line_width(6)
            ctx.stroke()
            text(ctx, "400 KM", -90, 0, 120, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=10)
            blink = 1.0 if int(t * 6) % 2 else 0.45
            text(ctx, "LOCK", 205, 0, 96, shade(RED, 1.0), font=CAPTION_FONT, bold=False, a=blink)
            ctx.restore()

    def kill(self, ctx, ts, t, d, b):
        self.sky_high(ctx, t)
        jx, jy = 540, 620
        for k in range(5):                                                  # wreckage tumbling away
            ang = -math.pi * (0.15 + 0.7 * rnd(k, 3))
            dist = 500 * clamp(ts / 1.0)
            px = jx + dist * math.cos(ang)
            py = jy + dist * math.sin(ang) + 700 * clamp(ts / 1.0) ** 2
            ctx.save()
            ctx.translate(px, py)
            ctx.rotate(ts * (4 + 3 * k))
            rrect(ctx, -40, -14, 80, 28, 6)
            rgba(ctx, hexc("#0B0F1A"))
            ctx.fill()
            ctx.restore()
        fireball(ctx, jx, jy, ts, 1.3, seed=4)
        shockwave(ctx, jx, jy, ts, 40, 800, GOLD, 0.8, 14)
        flash(ctx, ts, 0.25, 0.8)

    def hud(self, ctx, t, d, b):
        if b["name"] <= t < b["sud"]:
            stamp(ctx, 540, STAMP_Y, t - b["name"], -0.04, 560, 170, GOLD, [("S-400", 0, 130, GOLD)])
        if b["sud"] <= t < b["stealth"]:
            stamp(ctx, 540, STAMP_Y, t - b["sud"], 0.03, 920, 170, GOLD, [("SUDARSHAN CHAKRA", 0, 100, GOLD)])
        if b["stealth"] <= t < b["lock"]:
            blink = 1.0 if int(t * 6) % 2 else 0.6
            stamp(ctx, 540, STAMP_Y, t - b["stealth"], -0.03, 640, 170, RED, [("NO ESCAPE", 0, 116, shade(RED, blink))])
        if t >= b["tamaam"]:
            stamp(ctx, 540, STAMP_Y, t - b["tamaam"], 0.04, 760, 170, FIRE, [("KAAM TAMAAM!", 0, 116, FIRE)])


class Kusha(Rapid):
    """Side angle, multi-layer cutout: Kusha canisters rise and fire -> parallax war room with an
    officer pointing at the hologram: iron dome, then 150/250/350 KM rings expanding in turn,
    and incoming threats burned at each layer."""
    accent = CYAN
    frames = SIDE
    RINGS = ((95, "150 KM", "150"), (170, "250 KM", "250"), (245, "350 KM", "350"))
    CX, CY = 790, 760

    def beats(self, d):
        c = self.cue
        return {"drdo": c("DRDO", d * 0.1), "project": c("PROJECT", d * 0.17), "apna": c("APNA", d * 0.3),
                "iron": c("IRON", d * 0.38), "150": c("150", d * 0.47), "250": c("250", d * 0.54),
                "350": c("350", d * 0.62), "layers": c("LAYERS", d * 0.73), "bhoon": c("BHOON", d * 0.88)}

    def shots(self, d):
        b = self.beats(d)
        return [(0.0, "reveal"), (b["apna"], "room"), (b["iron"], "room"), (b["150"], "room"),
                (b["350"], "room"), (b["layers"], "room"), (b["bhoon"], "room")]

    def threats(self, d, b):
        """(spawn, intercept, angle, ring radius) of the enemy tracks burned on BHOON."""
        out = []
        for k in range(6):
            hit = min(d - 0.15, b["bhoon"] + 0.12 + 0.18 * k)
            out.append((min(b["layers"], hit - 0.6), hit, -1.25 + 0.3 * k, self.RINGS[2 - k % 3][0]))
        return out

    def events(self, d):
        b = self.beats(d)
        ev = [(0.02, "boom"), (b["drdo"], "thud"), (b["project"], "boom"), (b["project"] + 0.05, "whoosh"),
              (b["iron"], "zap"), (b["150"], "beep"), (b["250"], "beep"), (b["350"], "beep"),
              (b["layers"], "kaching")]
        return ev + [(hit, "boom" if k % 2 == 0 else "thud") for k, (_, hit, _, _) in enumerate(self.threats(d, b))]

    def shake(self, t, d, b):
        return kick(t - b["project"], 0.7, 34) + sum(kick(t - hit, 0.25, 14) for _, hit, _, _ in self.threats(d, b))

    def reveal(self, ctx, ts, t, d, b):
        sky(ctx, ((0, "#020A14"), (0.62, "#0A2A40"), (0.74, "#C25A1C"), (1, "#03070C")))
        stars(ctx, 50, 1000)
        ground(ctx, 1400, "#05090D")
        line(ctx, [(-200, 1400), (W + 200, 1400)], SAFFRON, 4, 0.7)
        elev = math.pi / 2 * ease_in_out(ts / max(b["project"] - 0.1, 0.6))
        mx, my = tel(ctx, 520, 1400, 0.95, t, elev, body=hexc("#2E4A2A"), stripe=TRICOLOR)
        u = t - b["project"]
        if u < 0:
            glow(ctx, mx, my, 110, CYAN, 0.25 + 0.15 * math.sin(t * 8))
            return
        y = my - 200 * u - 2800 * u * u
        for j in range(14):                                                 # tricolour exhaust plume
            sy = lerp(my, y + 140, j / 13)
            circle(ctx, mx + 12 * math.sin(j + t * 3), sy, 26 + 46 * (1 - j / 13), TRICOLOR[j % 3], 0.22)
        glow(ctx, mx, my, 340 * clamp(1 - u / 0.8), SAFFRON, 0.8)
        shockwave(ctx, mx, my, u, 40, 700, SAFFRON, 0.7, 12)
        if y > -300:
            sam(ctx, mx, y, -math.pi / 2, 1.2, t, nose=SAFFRON, body=(0.95, 0.95, 0.92))

    def room(self, ctx, ts, t, d, b):
        sky(ctx, ((0, "#021018"), (1, "#04212E")))
        drift = (t * 18) % 90                                               # layer 1: slow parallax grid
        for i in range(-2, 15):
            line(ctx, [(i * 90 - drift, 0), (i * 90 - drift - 160, H)], CYAN, 2, 0.08)
            line(ctx, [(-100, i * 140 + drift * 0.5), (W + 100, i * 140 + drift * 0.5 + 80)], CYAN, 2, 0.08)
        cx, cy = self.CX + 10 * math.sin(t * 0.8), self.CY                 # layer 2: hologram
        ctx.push_group()
        india_map(ctx, cx, cy, 20, t, fill=hexc("#06303A"), edge=CYAN, a=0.5)
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(0.6)
        glow(ctx, cx, cy, 120, CYAN, 0.5)
        sam(ctx, cx, cy + 40, -math.pi / 2, 0.55, t, burn=0.4, nose=SAFFRON)
        u = t - b["iron"]
        if u > 0:
            g = ease_out_cubic(u / 0.6)
            dome(ctx, cx, cy + 80, 270 * g, 300 * g, t, CYAN, 0.6)
        for k, (r, name, key) in enumerate(self.RINGS):                   # rings pop in on their cue
            u = t - b[key]
            if u < 0:
                continue
            rr = r * max(ease_out_back(u / 0.4), 0)
            hot = 1.0 + 1.5 * clamp(1 - abs(t - b["layers"] - 0.2 * k) / 0.25)
            ctx.arc(cx, cy, rr, 0, math.tau)
            rgba(ctx, CYAN, 0.12 * hot)
            ctx.set_line_width(26)
            ctx.stroke_preserve()
            rgba(ctx, CYAN, min(1.0, 0.85 * hot))
            ctx.set_line_width(5)
            ctx.set_dash([22, 12], -t * 60 * (k + 1))
            ctx.stroke()
            ctx.set_dash([])
            pulse = (t * 0.8 + k * 0.33) % 1.0                              # ripple expanding past the ring
            ctx.arc(cx, cy, rr * (1 + 0.35 * pulse), 0, math.tau)
            rgba(ctx, CYAN, 0.4 * (1 - pulse))
            ctx.set_line_width(3)
            ctx.stroke()
            label(ctx, name, cx, cy - rr, u - 0.1, size=38, c=CYAN if hot < 1.5 else GOLD)
        for spawn, hit, ang, r in self.threats(d, b):                     # enemies burned at each layer
            px0, py0 = cx + 900 * math.cos(ang), cy + 900 * math.sin(ang)
            hx, hy = cx + r * math.cos(ang), cy + r * math.sin(ang)
            v = clamp((t - spawn) / max(hit - spawn, 0.3))
            if t >= spawn and v < 1:
                px, py = lerp(px0, hx, v), lerp(py0, hy, v)
                line(ctx, [(lerp(px0, px, 0.7), lerp(py0, py, 0.7)), (px, py)], RED, 6, 0.6)
                circle(ctx, px, py, 9, RED)
            if 0 < hit - t < 0.3:                                           # interceptor leaves the centre
                w = 1 - (hit - t) / 0.3
                line(ctx, [(cx, cy), (lerp(cx, hx, w), lerp(cy, hy, w))], SAFFRON, 5, 0.9)
            u = t - hit
            if u >= 0:
                glow(ctx, hx, hy, 150 * ease_out_cubic(u / 0.2), FIRE, 0.95 * clamp(1 - u / 0.9))
                circle(ctx, hx, hy, 26 * clamp(1 - u / 0.5), (1, 0.95, 0.8))
                shockwave(ctx, hx, hy, u, 8, 150, hexc("#FFD36E"), 0.5, 5)
        hx, hy = pointing_jawan(ctx, 150, 1560, 1.4, t)                     # layer 3: foreground cutout
        line(ctx, [(hx, hy), (cx, cy)], CYAN, 3, 0.25 + 0.15 * math.sin(t * 6))

    def hud(self, ctx, t, d, b):
        if b["drdo"] <= t < b["project"]:
            stamp(ctx, 540, STAMP_Y, t - b["drdo"], -0.04, 440, 170, CYAN, [("DRDO", 0, 130, (1, 1, 1))])
        if t >= b["project"]:
            u = t - b["project"]
            stamp(ctx, 480, STAMP_Y, u, 0.03, 800, 180, CYAN, [("PROJECT KUSHA", 0, 120, CYAN)])
            if u > 0.2:
                pop = max(ease_out_back((u - 0.2) / 0.3), 1e-3)
                ctx.save()
                ctx.translate(955, STAMP_Y)
                ctx.scale(pop, pop)
                ctx.rotate(0.06)
                flag(ctx, -60, -40, 120, 80, "in", t)
                ctx.restore()


class Outro(Rapid):
    """Centred hero frame: giant waving tricolour over a horizon of air-defence radar and launcher
    silhouettes, big pulsing PROJECT KUSHA > S-400? comment trigger with a bouncing arrow."""
    accent = SAFFRON
    frames = HERO

    def beats(self, d):
        c = self.cue
        return {"nirbhar": c("NIRBHAR", d * 0.2), "kya": c("KYA DESI", d * 0.4), "comment": c("COMMENT", d * 0.72),
                "jai": c("JAI", d * 0.8)}

    def shots(self, d):
        b = self.beats(d)
        return [(0.0, "hero"), (b["kya"], "hero"), (b["comment"], "hero")]

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["nirbhar"], "thud"), (b["kya"], "whoosh"), (b["kya"] + 0.05, "pop"),
                (b["comment"], "kaching"), (b["jai"], "dingdong")]

    def shake(self, t, d, b):
        return kick(t, 0.4, 18) + kick(t - b["kya"], 0.4, 16)

    def hero(self, ctx, ts, t, d, b):
        sky(ctx, ((0, "#0B1A3D"), (0.45, "#3A2A5C"), (0.7, "#FF8A3C"), (1, "#2A1208")))
        ctx.save()
        ctx.translate(540, 760)
        ctx.rotate(t * 0.3)
        for k in range(18):
            a = k / 18 * math.tau
            ctx.move_to(0, 0)
            ctx.arc(0, 0, 1600, a, a + math.tau / 36)
            ctx.close_path()
            rgba(ctx, TRICOLOR[k % 3], 0.08)
            ctx.fill()
        ctx.restore()
        glow(ctx, 540, 1300, 700, SAFFRON, 0.6)
        rise = ease_out_cubic(t / 0.6)
        flag(ctx, 90, lerp(560, 400, rise), 900, 600, "in", t * 1.4)
        for x, kind, s, k in ((150, "dish", 0.9, 0), (780, "panel", 1.0, 1), (1000, "dish", 0.7, 2)):
            radar_mast(ctx, x, 1390, s, t, SIL, kind, k)
        tel(ctx, 430, 1390, 0.6, t, math.pi / 2, mono=SIL)
        ground(ctx, 1390, SIL)
        line(ctx, [(-200, 1390), (W + 200, 1390)], SAFFRON, 4, 0.9)

    def hud(self, ctx, t, d, b):
        if b["nirbhar"] <= t < b["comment"]:
            stamp(ctx, 540, STAMP_Y, t - b["nirbhar"], -0.03, 920, 170, SAFFRON,
                  [("AATMANIRBHAR BHARAT", 0, 92, (1, 1, 1))])
        if t >= b["comment"]:
            stamp(ctx, 540, STAMP_Y, t - b["comment"], 0.03, 900, 170, GOLD, [("COMMENT 'JAI HIND'", 0, 100, GOLD)])
        u = t - b["kya"]
        if u < 0:
            return
        pop = max(ease_out_back(u / 0.3, 2.2), 1e-3) * (1 + 0.05 * math.sin(t * 8))
        ctx.save()
        ctx.translate(540, 900)
        ctx.scale(pop, pop)
        ctx.rotate(-0.02)
        glow(ctx, 0, 0, 520, CYAN, 0.25 + 0.15 * math.sin(t * 8))
        rrect(ctx, -440, -150, 880, 300, 30)
        rgba(ctx, (0.02, 0.02, 0.05), 0.88)
        ctx.fill_preserve()
        rgba(ctx, CYAN)
        ctx.set_line_width(7)
        ctx.stroke()
        text(ctx, "PROJECT KUSHA", 0, -62, 118, CYAN, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=12)
        text(ctx, "> S-400?", -70, 72, 118, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=12)
        ctx.restore()
        if u > 0.2:
            down_arrow(ctx, 790, 950 + 24 * abs(math.sin(t * 7)), 0.6 * pop, GOLD)


SCENE_CLASSES = {"hook": Hook, "s400": S400, "kusha": Kusha, "outro": Outro}
