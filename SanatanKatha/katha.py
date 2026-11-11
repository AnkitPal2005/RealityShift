"""Shared frame of every Sanatan katha Short: storyteller voice tones, scene helpers, scenery, the diya header,
scroll captions, the compositor and the one-call renderer.

A katha (kathas/<name>.py) only writes its own story: SPEC (lines + pauses), scene classes, UPLOAD and thumbnail().
See README.md for the full recipe and the storytelling rules.
"""

import importlib
import json
import math

import cairo
import numpy as np

import delivery
import devta as dv
import engine
from engine import *  # noqa: F401,F403

CHANNEL_NAME = "DIVYA RAHASYA"   # the channel (old Apni Kahaniya / Silent Reality, 4,110 subs); a katha may set HEADER
GROUND = 1180                  # ground line every scene stands on
GOLD, GOLD_HI, GOLD_DK = dv.GOLD, dv.GOLD_HI, dv.GOLD_DK
SAFF = dv.SAFFRON
BLUE = dv.KRISHNA_SKIN
DIVINE = dv.DIVINE

# story defaults: `from katha import *` hands these to every katha, which may override any of them
CHANNEL = "sanatan"
WATERMARK = ""
CLEAN_PUNCTUATION = False
MAX_GAP = 0.3
TAIL_PAD = 0.15
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_STYLE = "divine"       # the channel's signature bed; key + melody change with every katha (seeded by name)
MUSIC_VOLUME = 0.2
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+8%"
EDGE_PITCH = "+0Hz"
BREATHS = False
ROOM = 0.14                  # a little temple air on the voice


# Kathavachak delivery (user, 11 Nov 2026: "jaise koi 20 saal ka tajurbekaar story telling kar raha ho"):
# a seasoned narrator never reads at one speed. He drops to a hush to pull you in, speeds up in the action,
# holds silence before the reveal, and gives each character a voice of its own. Every line carries its own
# held pause (honor_pauses), so the silences are written into the script like a storyteller's breath.
TONES = {
    "open":    ("+0%", "-6Hz", "+0%"),       # hushed opening that leans in: "socho..."
    "tell":    ("+14%", "-3Hz", "+8%"),       # steady narrator
    "build":   ("+20%", "-1Hz", "+14%"),     # rising tension
    "fast":    ("+28%", "+1Hz", "+18%"),     # action, the arrow in flight
    "low":     ("+4%", "-7Hz", "+0%"),       # lowered voice, a secret
    "whisper": ("+0%", "-8Hz", "-10%"),     # near-whisper before a reveal
    "punch":   ("+6%", "-4Hz", "+28%"),      # the payoff, heavy and slow
    "awe":     ("+4%", "-2Hz", "+12%"),      # wonder, reverence
    "ask":     ("+10%", "+4Hz", "+12%"),      # a question left hanging
    "warm":    ("+10%", "-2Hz", "+8%"),       # talking to the viewer like family
    "cta":     ("+16%", "+1Hz", "+14%"),
    "char":    ("+8%", "+6Hz", "+6%"),       # the old brahmin's lighter, teasing voice
    "deva":    ("+0%", "-9Hz", "+18%"),      # Shri Krishna: deep and unhurried
    "maa":     ("+2%", "-2Hz", "+4%", "hi-IN-SwaraNeural"),   # the mother speaks in her own voice
}


def script_of(spec):
    """SPEC -> (DELIVERY, SCRIPT, NARRATION) with the kathavachak tones and each line's own held pause."""
    deliv = delivery.build(spec, tones=TONES, honor_pauses=True, pause_scale=0.75)
    script = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in spec]
    narration = {key: " ".join(hi for hi, _ in chunks) for key, chunks in script}
    return deliv, script, narration


def hot_words(hot):
    """Caption colour map that also matches each word without its punctuation."""
    out = dict(hot)
    for k in list(out):
        out[k.strip(PUNCT + ".—")] = out[k]
    return out


class Cued:
    """cue(word) = start of the first caption chunk containing it in this scene (fallback: default)."""

    def cue(self, key, default):
        for s in engine.SCENES:
            if s["obj"] is self:
                return next((st for st, cap in s["captions"] if key in cap), default)
        return default



# ============================================================ shared scenery

def battlefield(ctx, t, dim=1.0, armies=True):
    dv.sky(ctx, hexc("#2B1238"), hexc("#C2492E"), hexc("#3A1A12"), 0.5)
    glow(ctx, 540, 900, 520, hexc("#FFB347"), 0.55)
    circle(ctx, 540, 900, 110, hexc("#FFD38A"), 0.9)
    for k, (c, yy) in enumerate(((hexc("#5A2436"), 960), (hexc("#3E1A28"), 1030))):
        ctx.move_to(0, yy)
        for x in range(0, W + 1, 60):
            ctx.line_to(x, yy - 40 * math.sin(x / 170 + k * 2) - 20 * math.sin(x / 61 + k))
        ctx.line_to(W, H)
        ctx.line_to(0, H)
        ctx.close_path()
        rgba(ctx, c)
        ctx.fill()
    ctx.rectangle(0, GROUND - 60, W, H)
    rgba(ctx, hexc("#2A120C"))
    ctx.fill()
    if armies:
        dv.army(ctx, 30, 470, GROUND - 70, 9, hexc("#160A0A"), t, SAFF, seed=1, a=dim)
        dv.army(ctx, 610, 1050, GROUND - 70, 9, hexc("#160A0A"), t, hexc("#8C1C2C"), seed=2, a=dim)
    for i in range(30):          # dust drifting across
        x = (rnd(i, 3) * W + t * 40 * (0.5 + rnd(i, 4))) % W
        circle(ctx, x, 900 + 300 * rnd(i, 5), 2 + 4 * rnd(i, 6), hexc("#FFCF99"), 0.15)


def meadow(ctx, t):
    dv.sky(ctx, hexc("#7EC8F2"), hexc("#FCE3B0"), hexc("#F4B66A"), 0.62)
    glow(ctx, 160, 760, 380, hexc("#FFE3A0"), 0.7)
    for k, (c, yy) in enumerate(((hexc("#86B86A"), 1010), (hexc("#5E9B4C"), 1090))):
        ctx.move_to(0, yy)
        for x in range(0, W + 1, 60):
            ctx.line_to(x, yy - 30 * math.sin(x / 210 + k * 1.7))
        ctx.line_to(W, H)
        ctx.line_to(0, H)
        ctx.close_path()
        rgba(ctx, c)
        ctx.fill()
    ctx.rectangle(0, GROUND - 20, W, H)
    rgba(ctx, hexc("#4E8A3E"))
    ctx.fill()
    for i in range(40):          # grass tufts
        x = rnd(i, 9) * W
        y = GROUND - 10 + 60 * rnd(i, 10)
        line(ctx, [(x, y), (x - 6, y - 22)], hexc("#3C7230"), 4)
        line(ctx, [(x, y), (x + 6, y - 20)], hexc("#3C7230"), 4)


def temple_bg(ctx, t):
    dv.sky(ctx, hexc("#2A0A14"), hexc("#5A1424"), hexc("#1A060C"), 0.5)
    ctx.save()
    ctx.translate(540, 560)
    ctx.rotate(t * 0.05)
    for k in range(20):
        ang = k / 20 * math.tau
        ctx.move_to(0, 0)
        ctx.arc(0, 0, 1400, ang - 0.05, ang + 0.05)
        ctx.close_path()
    rgba(ctx, GOLD, 0.06)
    ctx.fill()
    ctx.restore()


def mother(ctx, x, y, s, t):
    """Barbarik's mother, veiled in a saree pallu, eyes closed, one hand raised in blessing."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    glow(ctx, 0, -500, 380, hexc("#FFB347"), 0.35)
    dv.smooth(ctx, [(-70, -540), (70, -540), (128, -300), (160, 0), (-160, 0), (-128, -300)])
    dv.ink(ctx, hexc("#8C1C3C"))
    line(ctx, [(-160, -6), (160, -6)], GOLD, 12)
    line(ctx, [(70, -540), (128, -300), (160, -10)], GOLD, 6)
    dv.limb(ctx, [(90, -470), (170, -470), (190, -600)], hexc("#9A6848"), 40)
    dv.palm(ctx, 190, -600, hexc("#9A6848"), s=0.8)
    dv.smooth(ctx, [(0, -716), (-82, -668), (-100, -560), (-70, -520), (70, -520), (100, -560), (82, -668)])
    dv.ink(ctx, hexc("#C2410C"))
    dv.ell(ctx, 0, -616, 50, 58)
    dv.ink(ctx, hexc("#9A6848"))
    for side in (-1, 1):
        line(ctx, [(side * 30 - 12, -622), (side * 30, -614), (side * 30 + 12, -622)], dv.OUTLINE, 5)
    line(ctx, [(-12, -588), (0, -582), (12, -588)], hexc("#7A1424"), 4)
    circle(ctx, 0, -650, 6, dv.RED_GEM)
    line(ctx, [(-82, -668), (0, -716), (82, -668)], GOLD, 6)
    ctx.restore()


def bubble(ctx, label, x, y, u, tail):
    if u <= 0:
        return
    k = ease_out_back(clamp(u / 0.3))
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    w = text_width(ctx, label, 58, font=CAPTION_FONT, bold=False) + 70
    rrect(ctx, -w / 2, -55, w, 110, 40)
    ctx.move_to(tail[0] - x - 18, 40)
    ctx.line_to(tail[0] - x, tail[1] - y)
    ctx.line_to(tail[0] - x + 18, 40)
    dv.ink(ctx, (1, 1, 1), 5)
    text(ctx, label, 0, 2, 58, dv.OUTLINE, font=CAPTION_FONT, bold=False)
    ctx.restore()


def flash(ctx, u, c=(1, 0.97, 0.88), dur=0.6):
    if 0 < u < dur:
        rgba(ctx, c, 1 - u / dur)
        ctx.paint()


def polyline_at(pts, u):
    """Point and heading at fraction u (0..1) along pts, each segment taking equal time."""
    m = len(pts) - 1
    f = clamp(u) * m
    i = min(int(f), m - 1)
    a, b = pts[i], pts[i + 1]
    k = f - i
    return (lerp(a[0], b[0], k), lerp(a[1], b[1], k)), math.atan2(b[1] - a[1], b[0] - a[0])


# ============================================================ frame: diya header + scroll captions

CAP_Y = 1290


def header(ctx, story, idx, n, tl):
    text(ctx, f"~ {getattr(story, 'HEADER', CHANNEL_NAME)} ~", 540, 78, 34, GOLD_HI, font=CAPTION_FONT, bold=False, a=0.85,
         stroke=(0, 0, 0), stroke_w=6)
    x0 = 540 - (n - 1) * 42
    for k in range(n):
        x = x0 + k * 84
        lit = k < idx or (k == idx)
        ctx.move_to(x - 22, 128)
        ctx.curve_to(x - 18, 146, x + 18, 146, x + 22, 128)
        ctx.close_path()
        dv.ink(ctx, hexc("#B4532A") if lit else hexc("#4A2A20"), 3)
        if lit:
            f = 1 + 0.15 * math.sin(tl * 12 + k)
            glow(ctx, x, 112, 34, hexc("#FFB347"), 0.6)
            dv.smooth(ctx, [(x, 126), (x - 7 * f, 116), (x, 96 - 6 * f), (x + 7 * f, 116)])
            rgba(ctx, hexc("#FFD15C"))
            ctx.fill()


def caption(ctx, sc, tl, hot):
    cur = None
    for i, (start, cap) in enumerate(sc["captions"]):
        if tl >= start - 0.03:
            cur = (start, cap)
    if cur is None:
        return
    start, cap = cur
    size, gap = 78, 22
    words = cap.split(" ")
    ws = [text_width(ctx, w, size, font=CAPTION_FONT, bold=False) for w in words]
    total = sum(ws) + gap * (len(ws) - 1)
    fit = min(1.0, 880 / total)
    bw = min(980, total * fit + 110)
    rrect(ctx, 540 - bw / 2, CAP_Y - 70, bw, 140, 26)
    dv.ink(ctx, hexc("#3A0A14"), 5, a=0.92, edge=GOLD)
    for sgn in (-1, 1):   # scroll ends
        dv.ell(ctx, 540 + sgn * bw / 2, CAP_Y, 18, 74)
        dv.ink(ctx, GOLD, 4)
    ctx.save()
    ctx.translate(540, CAP_Y)
    ctx.scale(fit, fit)
    x = -total / 2
    for k, (w, ww) in enumerate(zip(words, ws)):
        u = tl - start + 0.03 - 0.07 * k
        if u < 0:
            break
        pop = ease_out_back(clamp(u / 0.22))
        c = hot.get(w.strip(PUNCT + ".—"), hexc("#FFF4E0"))
        ctx.save()
        ctx.translate(x + ww / 2, 0)
        ctx.scale(pop, pop)
        text(ctx, w, 0, 2, size, c, font=CAPTION_FONT, bold=False, stroke=(0.1, 0.02, 0.04), stroke_w=10)
        ctx.restore()
        x += ww + gap
    ctx.restore()


def compose(story, idx, tl):
    sc = engine.SCENES[idx]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    zoom = 1.0 + 0.045 * tl / sc["dur"]
    ctx.save()
    ctx.translate(W / 2 + 8 * math.sin(tl * 0.5 + idx), H * 0.4)
    ctx.scale(zoom, zoom)
    ctx.translate(-W / 2, -H * 0.4)
    sc["obj"].draw(ctx, tl, sc["dur"])
    ctx.restore()
    g = cairo.RadialGradient(W / 2, H * 0.4, H * 0.3, W / 2, H * 0.4, H * 0.8)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0.12, 0.02, 0.04, 0.55)
    ctx.set_source(g)
    ctx.paint()
    g = cairo.LinearGradient(0, GROUND, 0, H - 400)
    g.add_color_stop_rgba(0, 0.1, 0.02, 0.04, 0)
    g.add_color_stop_rgba(1, 0.1, 0.02, 0.04, 0.96)
    ctx.rectangle(0, GROUND, W, H)
    ctx.set_source(g)
    ctx.fill()
    ctx.rectangle(0, H - 400, W, 400)
    rgba(ctx, (0.1, 0.02, 0.04), 0.96)
    ctx.fill()
    header(ctx, story, idx, len(story.SPEC), tl)
    caption(ctx, sc, tl, story.HOT)
    if idx and tl < 0.35:          # golden light between scenes
        glow(ctx, W / 2, H * 0.4, 1300, (1, 0.9, 0.6), 0.85 * (1 - tl / 0.35))
    return surf


def frame_maker(story):
    def make_frame(t: float) -> np.ndarray:
        scenes = engine.SCENES
        idx = max(i for i, s in enumerate(scenes) if t >= s["start"] or i == 0)
        surf = compose(story, idx, t - scenes[idx]["start"])
        surf.flush()
        buf = np.ndarray((H, W, 4), dtype=np.uint8, buffer=surf.get_data())
        return buf[:, :, 2::-1].copy()
    return make_frame


def write_alignment(story, final):
    out = [{"scene": spec["key"], "start": round(s["start"], 3), "end": round(s["start"] + s["dur"], 3),
            "voiceover": story.NARRATION[spec["key"]], "on_screen_text": spec["text"], "visual": spec["visual"],
            "words": [{"t": round(s["start"] + st, 3), "w": w} for st, w in s["captions"]]}
           for spec, s in zip(story.SPEC, engine.SCENES)]
    path = final.with_suffix(".json")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Alignment: {path}")


# ============================================================ render

def run(name):
    """Render kathas/<name>.py end to end: YPP gate, voice, music, frames, scene log, upload kit."""
    import upload_kit
    story = importlib.import_module(f"kathas.{name}")
    engine.make_frame = frame_maker(story)
    final = engine.render(story, "edge")
    write_alignment(story, final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))
    return final


# ============================================================ more scenery (Chhath set) + comment card

HORIZON = 880


def ghat(ctx, t, sun_y, morning=False, sun_x=540, diyas=True):
    """River ghat at sunset (or sunrise): sun over the far bank, its reflection on the water, sugarcane,
    floating diyas. Vratis are drawn by the scene on top, waist-deep at y ~ 1080."""
    if morning:
        dv.sky(ctx, hexc("#5E9BD6"), hexc("#F7B7A3"), hexc("#FFE0A3"), 0.42)
    else:
        dv.sky(ctx, hexc("#2B1A4A"), hexc("#E9683F"), hexc("#FFC46B"), 0.42)
    dv.sun_disc(ctx, sun_x, sun_y, 110, t, rays=16)
    ctx.move_to(0, HORIZON)
    for x in range(0, W + 1, 40):
        ctx.line_to(x, HORIZON - 24 - 18 * math.sin(x / 70) - 14 * math.sin(x / 23))
    ctx.line_to(W, HORIZON + 10)
    ctx.line_to(0, HORIZON + 10)
    ctx.close_path()
    rgba(ctx, hexc("#3A2A40") if morning else hexc("#2A1420"))
    ctx.fill()
    g = cairo.LinearGradient(0, HORIZON, 0, H)
    g.add_color_stop_rgb(0, *(hexc("#E9A27A") if morning else hexc("#C2603A")))
    g.add_color_stop_rgb(1, *(hexc("#2E4A6A") if morning else hexc("#2A1224")))
    ctx.rectangle(0, HORIZON, W, H)
    ctx.set_source(g)
    ctx.fill()
    for i in range(26):                     # sun's reflection, broken by ripples
        y = HORIZON + 12 + i * 12
        w = 150 * (1 - i / 30) * (0.7 + 0.3 * math.sin(t * 3 + i))
        line(ctx, [(sun_x - w, y), (sun_x + w, y)], hexc("#FFD38A"), 5, 0.55 * (1 - i / 26))
    for side in (-1, 1):                    # sugarcane arch on the bank
        bx = 540 + side * 470
        for k in range(3):
            pts = [(bx + side * 10 * k, GROUND), (bx - side * (40 + 8 * k), 760), (bx - side * (120 + 10 * k), 520)]
            line(ctx, pts, hexc("#5E7A2A"), 14)
            for j in range(4):
                lx, ly = lerp(pts[1][0], pts[2][0], j / 4), lerp(pts[1][1], pts[2][1], j / 4)
                line(ctx, [(lx, ly), (lx + side * 60, ly - 40 + 10 * math.sin(t * 2 + j))], hexc("#7BA33A"), 6)
    if diyas:
        for i in range(8):
            x = (rnd(i, 51) * W + t * 12 * (0.5 + rnd(i, 52))) % W
            y = HORIZON + 60 + 220 * rnd(i, 53)
            dv.diya(ctx, x, y, 0.35, t + i)


def palace(ctx, t):
    """Royal hall: maroon walls, gold-edged arches, hanging lamps."""
    dv.sky(ctx, hexc("#3A0E1A"), hexc("#6A1E2A"), hexc("#2A0A10"), 0.6)
    for k in range(3):
        x = 180 + 360 * k
        ctx.move_to(x - 130, GROUND)
        ctx.line_to(x - 130, 620)
        ctx.curve_to(x - 130, 440, x + 130, 440, x + 130, 620)
        ctx.line_to(x + 130, GROUND)
        ctx.close_path()
        rgba(ctx, hexc("#24060C"))
        ctx.fill_preserve()
        rgba(ctx, GOLD, 0.8)
        ctx.set_line_width(8)
        ctx.stroke()
    for x in (0, 360, 720, 1080):
        rrect(ctx, x - 26, 420, 52, GROUND - 420, 10)
        dv.ink(ctx, hexc("#8A2A2A"), 4)
    for k, x in enumerate((180, 540, 900)):
        line(ctx, [(x, 0), (x, 300)], GOLD_DK, 3)
        dv.diya(ctx, x, 330, 0.6, t + k)
    ctx.rectangle(0, GROUND - 30, W, H)
    rgba(ctx, hexc("#4A1A12"))
    ctx.fill()


def night_river(ctx, t):
    dv.sky(ctx, hexc("#070A24"), hexc("#16204A"), hexc("#0A0E26"))
    dv.stars(ctx, t)
    circle(ctx, 860, 260, 60, hexc("#FFF7D6"))
    ctx.rectangle(0, HORIZON, W, H)
    rgba(ctx, hexc("#0C1A3A"))
    ctx.fill()
    for i in range(14):
        y = HORIZON + 14 + i * 16
        line(ctx, [(860 - 60 + 4 * i, y), (860 + 60 - 4 * i, y)], hexc("#FFF7D6"), 3, 0.4 * (1 - i / 14))
    ctx.rectangle(0, GROUND - 40, W, H)
    rgba(ctx, hexc("#1A1410"))
    ctx.fill()


def comment_card(ctx, t, ask_t, type_t, msg, y=960):
    """Comment card that pops in at ask_t, types msg from type_t, then points at the Shorts comment button."""
    u = t - ask_t
    if u <= 0:
        return
    pop = ease_out_back(clamp(u / 0.35))
    ctx.save()
    ctx.translate(540, y)
    ctx.scale(pop, pop)
    rrect(ctx, -440, -150, 880, 300, 30)
    dv.ink(ctx, hexc("#1A0A0E"), 5, edge=GOLD)
    text(ctx, "COMMENT MEIN LIKHO", 0, -88, 54, GOLD_HI, font=CAPTION_FONT, bold=False)
    rrect(ctx, -390, -30, 780, 130, 24)
    dv.ink(ctx, (0.06, 0.03, 0.04), 4, edge=GOLD if t > type_t else GOLD_DK)
    shown = msg[:int(len(msg) * clamp((t - type_t) / 0.7))] if t > type_t else ""
    tw = text(ctx, shown, -350, 35, 72, (1, 1, 1), font=CAPTION_FONT, bold=False, anchor="l") if shown else 0
    if int(t * 3) % 2 == 0:
        ctx.rectangle(-344 + tw, -5, 7, 80)
        rgba(ctx, GOLD_HI)
        ctx.fill()
    ctx.restore()
    if t > type_t:
        k = ease_out_cubic(clamp((t - type_t) / 0.4))
        bob = 10 * math.sin(t * 6)
        x0, y0 = 880, y + 170
        x1, y1 = lerp(x0, 1010, k), lerp(y0, y + 370, k) + bob
        line(ctx, [(x0, y0), (x1, y1)], GOLD_HI, 12)
        ang = math.atan2(y1 - y0, x1 - x0)
        ctx.move_to(x1 + 34 * math.cos(ang), y1 + 34 * math.sin(ang))
        for da in (2.4, -2.4):
            ctx.line_to(x1 + 30 * math.cos(ang + da), y1 + 30 * math.sin(ang + da))
        ctx.close_path()
        rgba(ctx, GOLD_HI)
        ctx.fill()
