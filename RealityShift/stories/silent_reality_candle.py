"""Silent Reality Short - The Burning Candle (14s, no voice).

Usage:
  python silent.py silent_reality_candle

An ink sketch draws itself on parchment. Close-up: a calm face with a golden halo, rays falling on others -
it reads as a kind helper / angel. Then the halo turns out to be a flame on a wick, wax runs down the face
like tears, the body is a straight wax column and the feet melt into a puddle. Zoom out: the person is a
candle on a dish, small figures warming their hands at it. Punchline, then the ink fades back to blank
paper so the Short loops into its first frame.
"""

import math

import cairo

from engine import clamp, ease_in_out, ease_out_cubic, glow, lerp, rgba, text
from silent import INK, Stroke, arc, bezier, paper

CHANNEL = "silent_reality"
TOPIC = "THE BURNING CANDLE"
OUTPUTS = {"silent": "silent_reality_candle.mp4"}
DURATION = 14.0
MUSIC_STYLE = "ambient"   # slow pads + bells: emotional, no drums
MUSIC_BPM = 72
SFX = [(6.9, "whoosh", 0.12)]   # soft air as the camera pulls back

HOOK = ("The sad reality", "of kind people...")
PUNCH = ("They loved the light.", "Nobody noticed the candle.")
# the policy gate reads on-screen text as this Short's "script"
SCRIPT = [("hook", [(" ".join(HOOK), " ".join(HOOK))]),
          ("reveal", [(PUNCH[0], PUNCH[0]), (PUNCH[1], PUNCH[1])])]
BEATS = {"hook": (0.0, 4.3, "Close-up: calm face with a golden halo, rays of light falling on others"),
         "reveal": (4.3, 14.0, "Halo becomes a flame, wax drips like tears, zoom out: the person is a candle "
                               "warming small figures; punchline; ink fades back to blank paper (loop)")}

SOURCES = [
    "Idea - giving to others until it exhausts the giver: 'compassion fatigue', Figley, C.R. (ed.) (1995), "
    "Compassion Fatigue: Coping with Secondary Traumatic Stress Disorder, Brunner/Mazel",
    "Idea - helping others at a real cost to oneself: Oakley, B., Knafo, A., Madhavan, G., Wilson, D.S. (eds.) "
    "(2012), Pathological Altruism, Oxford University Press",
    "No factual numbers or quotes on screen; the drawing, both text lines and the music are original to this Short",
]

AMBER = (1.0, 0.68, 0.22)
GOLD = (0.86, 0.62, 0.18)
WAX_INK = (0.30, 0.20, 0.12)


def seg(a, b, n=24):
    return [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n + 1)]


def drip(x, y0, y1, seed, bulb=9):
    """A wax run: wavering line down, ending in a round drop."""
    pts = [(x + 3 * math.sin(i * 0.7 + seed), y0 + (y1 - y0) * i / 30) for i in range(31)]
    return pts + arc(pts[-1][0], y1 + bulb * 0.6, bulb * 0.8, bulb, -math.pi / 2, 3 * math.pi / 2, 20)


def person(cx, feet, s, t0, seed, facing):
    """Small figure, hands raised toward the warmth (facing = +1 looks right, -1 left)."""
    hy = feet - 150 * s
    d = 0.32 * (t0 % 1 + 0.6)
    return [
        Stroke(arc(cx, hy, 21 * s, 23 * s, 0, 2 * math.pi, 30), t0, t0 + 0.45, 3.4, seed=seed),
        Stroke(seg((cx, hy + 24 * s), (cx + 4 * facing, feet - 62 * s), 10), t0 + 0.3, t0 + 0.65, 3.6, seed=seed + 1),
        Stroke(seg((cx + 4 * facing, feet - 62 * s), (cx - 16 * s, feet), 8), t0 + 0.55, t0 + 0.8, 3.4, seed=seed + 2),
        Stroke(seg((cx + 4 * facing, feet - 62 * s), (cx + 18 * s, feet), 8), t0 + 0.6, t0 + 0.85, 3.4, seed=seed + 3),
        Stroke(bezier((cx, hy + 50 * s), (cx + 30 * s * facing, hy + 40 * s), (cx + 48 * s * facing, hy + 10 * s),
                      (cx + 58 * s * facing, hy - 6 * s), 16), t0 + 0.5 + d / 4, t0 + 0.95, 3.2, seed=seed + 4),
        Stroke(bezier((cx, hy + 58 * s), (cx + 28 * s * facing, hy + 60 * s), (cx + 50 * s * facing, hy + 34 * s),
                      (cx + 62 * s * facing, hy + 20 * s), 16), t0 + 0.6, t0 + 1.0, 3.2, seed=seed + 5),
    ]


def build_strokes():
    S = []
    # --- 0.3-3.4s: the calm face (reads as a kind helper)
    S.append(Stroke(bezier((440, 660), (430, 800), (470, 888), (540, 890), 40) +
                    bezier((540, 890), (610, 888), (650, 800), (640, 660), 40)[1:], 0.3, 1.9, 5.5, seed=1))
    S.append(Stroke(arc(540, 660, 100, 22, math.pi, 3 * math.pi, 60), 1.4, 2.2, 4.5, seed=2))   # top of head = wax rim
    S.append(Stroke(arc(500, 748, 22, 12, 0.15, math.pi - 0.15, 18), 1.6, 2.0, 4.2, seed=3))     # closed eyes
    S.append(Stroke(arc(580, 748, 22, 12, 0.15, math.pi - 0.15, 18), 1.75, 2.15, 4.2, seed=4))
    S.append(Stroke(arc(500, 728, 26, 9, math.pi + 0.3, 2 * math.pi - 0.3, 14), 1.9, 2.2, 3.2, seed=5))
    S.append(Stroke(arc(580, 728, 26, 9, math.pi + 0.3, 2 * math.pi - 0.3, 14), 2.0, 2.3, 3.2, seed=6))
    S.append(Stroke([(541, 762), (536, 790), (532, 802), (545, 806)], 2.1, 2.45, 3.6, seed=7))  # nose
    S.append(Stroke(arc(540, 828, 30, 12, 0.2, math.pi - 0.2, 20), 2.35, 2.75, 4.0, seed=8))   # soft smile
    for k, ang in enumerate((115, 128, 141, 39, 52, 65)):   # rays falling on others
        a = math.radians(ang)
        S.append(Stroke(seg((540 + 175 * math.cos(a), 770 + 175 * math.sin(a)),
                            (540 + 330 * math.cos(a), 770 + 330 * math.sin(a)), 14),
                        2.5 + 0.12 * k, 3.1 + 0.12 * k, 2.4, color=GOLD, seed=20 + k, alpha=0.7))
        S[-1].ray = True   # fades once the flame takes over
    # --- 3.0-6.0s: neck and shoulders flow into the straight sides of a column (ink runs downward)
    S.append(Stroke(seg((505, 884), (500, 930), 6) + bezier((500, 930), (470, 950), (425, 955), (420, 990), 14)[1:]
                    + seg((420, 990), (420, 1484), 50)[1:], 3.0, 6.0, 5.5, seed=30))
    S.append(Stroke(seg((575, 884), (580, 930), 6) + bezier((580, 930), (610, 950), (655, 955), (660, 990), 14)[1:]
                    + seg((660, 990), (660, 1484), 50)[1:], 3.15, 6.1, 5.5, seed=31))
    # --- 4.6-5.6s: the halo was a flame - wick + flame outline
    S.append(Stroke(seg((540, 660), (537, 622), 6), 4.6, 4.85, 5.0, seed=40))
    S.append(Stroke(bezier((540, 625), (488, 590), (512, 520), (542, 470), 30) +
                    bezier((542, 470), (566, 525), (590, 588), (540, 625), 30)[1:], 4.8, 5.6, 4.0, color=WAX_INK, seed=41))
    # --- 5.6-8.6s: wax runs down the face like tears, then down the body
    for k, (x, y0, y1, t0) in enumerate([(452, 668, 812, 5.6), (628, 670, 760, 5.85), (500, 760, 846, 6.1),
                                         (432, 1000, 1190, 6.6), (650, 1000, 1300, 6.9), (560, 950, 1110, 7.2),
                                         (470, 1150, 1330, 7.6)]):
        S.append(Stroke(drip(x, y0, y1, k), t0, t0 + 1.0, 4.2 if k > 2 else 3.6, color=WAX_INK, seed=50 + k))
    # --- 6.8-8.4s: feet melt into a puddle; 8.0-9.2s: the candle dish
    S.append(Stroke([(420 - 90 * u, 1484 + 18 * u + 6 * math.sin(u * 9)) for u in (i / 20 for i in range(21))] +
                    [(330 + 420 * u, 1502 + 14 * math.sin(u * 17) + 10 * math.sin(u * 5)) for u in (i / 60 for i in range(61))] +
                    [(750 - 90 * u, 1502 - 18 * u + 6 * math.sin(u * 9)) for u in (i / 20 for i in range(21))],
                    6.8, 8.0, 4.6, seed=60))
    S.append(Stroke(arc(458, 1494, 22, 12, math.pi, 2 * math.pi, 14), 7.6, 7.9, 3.6, seed=61))   # melted toes
    S.append(Stroke(arc(500, 1496, 18, 10, math.pi, 2 * math.pi, 14), 7.7, 8.0, 3.6, seed=62))
    S.append(Stroke(arc(590, 1496, 18, 10, math.pi, 2 * math.pi, 14), 7.8, 8.1, 3.6, seed=63))
    S.append(Stroke(arc(632, 1494, 22, 12, math.pi, 2 * math.pi, 14), 7.9, 8.2, 3.6, seed=64))
    S.append(Stroke(arc(540, 1528, 232, 44, 0, math.pi, 50), 8.0, 8.8, 5.0, seed=70))
    S.append(Stroke(arc(540, 1528, 232, 44, math.pi, 2 * math.pi, 50), 8.3, 9.0, 3.0, seed=71, alpha=0.6))
    S.append(Stroke(arc(792, 1530, 28, 22, -math.pi / 2, math.pi / 2, 20), 8.7, 9.1, 4.0, seed=72))   # handle
    # --- 7.8-9.8s: the people warming themselves at it
    for k, (cx, s, t0, face) in enumerate([(150, 0.95, 7.8, 1), (250, 1.1, 8.15, 1),
                                           (845, 1.05, 8.0, -1), (935, 0.9, 8.35, -1)]):
        S += person(cx, 1580, s, t0, 80 + 10 * k, face)
    return S


STROKES = build_strokes()
END_FADE = (13.0, 14.0)   # ink fades back to blank paper -> seamless loop to frame 0


def camera(ctx, t):
    """Close-up on the face, pulling back to reveal the whole candle (7.0-9.6s)."""
    u = ease_in_out(clamp((t - 7.0) / 2.6))
    z = lerp(1.9, 1.0, u)
    fx, fy = 540, lerp(740, 960, u)
    ay = lerp(900, 960, u)
    ctx.translate(540, ay)
    ctx.scale(z, z)
    ctx.translate(-fx, -fy)


def flame(ctx, t, k):
    """Filled flickering flame (k = 0..1 visibility)."""
    if k <= 0:
        return
    f = 6 * math.sin(t * 9.1) + 4 * math.sin(t * 15.7 + 1)
    tip = (542 + f, 468 + 4 * math.sin(t * 7))
    glow(ctx, 540, 560, 520, AMBER, 0.32 * k)
    for scale, col, a in ((1.0, (1.0, 0.55, 0.12), 0.85), (0.62, (1.0, 0.84, 0.35), 0.95), (0.3, (1, 0.98, 0.85), 1)):
        ctx.save()
        ctx.translate(540, 622)
        ctx.scale(scale, scale)
        ctx.translate(-540, -622)
        ctx.move_to(540, 625)
        ctx.curve_to(486, 592, 512, 522, *tip)
        ctx.curve_to(568, 525, 594, 590, 540, 625)
        rgba(ctx, col, a * k)
        ctx.fill()
        ctx.restore()


def words_in(ctx, s, y, size, t0, t, fade, per=0.18):
    """Text inked word by word, centred."""
    ws = s.split(" ")
    widths = []
    for i, w in enumerate(ws):   # the last word is bold: measure it that way so the line centres
        ctx.select_font_face("Georgia", cairo.FONT_SLANT_NORMAL,
                             cairo.FONT_WEIGHT_BOLD if i == len(ws) - 1 else cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(size)
        widths.append(ctx.text_extents(w)[4] + (ctx.text_extents(" ")[4] if i < len(ws) - 1 else 0))
    x = 540 - sum(widths) / 2
    for i, (w, wd) in enumerate(zip(ws, widths)):
        a = ease_out_cubic(clamp((t - t0 - i * per) / 0.35)) * fade
        if a > 0:
            text(ctx, w, x, y + 8 * (1 - a), size, INK, font="Georgia", bold=i == len(ws) - 1, a=a, anchor="l")
        x += wd


def draw(ctx, t, show_text=True):
    paper(ctx, t)
    fade = 1 - clamp((t - END_FADE[0]) / (END_FADE[1] - END_FADE[0]))
    ctx.save()
    camera(ctx, t)
    halo = clamp((t - 1.2) / 1.0) * (1 - clamp((t - 4.4) / 0.8))
    if halo > 0:   # the angel's halo: warm glow + a golden ring above the head
        glow(ctx, 540, 640, 300, AMBER, 0.28 * halo * fade)
        ctx.save()
        ctx.translate(540, 600)
        ctx.scale(1, 0.22)
        ctx.arc(0, 0, 82, 0, 2 * math.pi)
        ctx.restore()
        rgba(ctx, GOLD, 0.85 * halo * fade)
        ctx.set_line_width(6)
        ctx.stroke()
    flame(ctx, t, clamp((t - 5.0) / 0.9) * fade)
    warm = clamp((t - 8.0) / 1.5) * fade
    if warm > 0:   # the people are lit by it
        glow(ctx, 230, 1450, 260, AMBER, 0.22 * warm)
        glow(ctx, 850, 1450, 260, AMBER, 0.22 * warm)
    rays = fade * (1 - clamp((t - 6.2) / 1.0))
    for s in STROKES:
        s.draw(ctx, t, rays if getattr(s, "ray", False) else fade)
    ctx.restore()
    if show_text:
        hook = clamp((t - 0.2) / 0.3) * (1 - clamp((t - 3.9) / 0.4))
        if hook > 0:
            words_in(ctx, HOOK[0], 250, 80, 0.2, t, hook)
            words_in(ctx, HOOK[1], 345, 80, 0.8, t, hook)
        if t > 9.8:
            words_in(ctx, PUNCH[0], 250, 68, 9.8, t, fade, per=0.22)
            words_in(ctx, PUNCH[1], 340, 68, 11.0, t, fade, per=0.24)


UPLOAD = {
    "title": "The Candle Nobody Noticed",   # title says candle, thumbnail says kind people - no overlap
    "titles": [
        "The Sad Reality of Kind People",
        "Kind People Are Like Candles",
        "They Loved the Light, Not the Candle",
        "The Candle Nobody Noticed",
        "What Kindness Costs the Kind",
        "Kind People Give Light Until They Melt",
        "The Hidden Cost of Being Too Kind",
        "Everyone Loves the Light, Nobody Sees the Candle",
        "A Silent Drawing About Kind People",
        "Kindness, Burnout and the Candle",
    ],
    "thumb_text": "KIND PEOPLE...",
    "queries": ["sad reality of kind people", "kindness burnout", "taken for granted"],
    "description": (
        "The sad reality of kind people: everyone loves the light, nobody notices the candle melting.\n"
        "A silent ink drawing about kindness, burnout and being taken for granted.\n\n"
        "Who is the candle in your life? Tell me in the comments.\n"
        "Silent Reality - drawings that say it without words."
    ),
    "tags": ["kind people", "sad reality", "kindness", "candle drawing", "ink drawing", "sketch reveal",
             "deep meaning drawing", "emotional art", "burnout", "taken for granted", "silent reality"],
    "hashtags": ["#Shorts", "#art", "#kindness"],
}


def thumbnail(ctx):
    """1080x1920 cover: the revealed candle-person, lit, with KIND PEOPLE... in ink."""
    draw(ctx, 12.0, show_text=False)
    text(ctx, "KIND PEOPLE...", 540, 290, 100, INK, font="Georgia", bold=True)
