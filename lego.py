"""Lego template: the frame of a Short split into interchangeable pieces.

A story picks one option per slot:

    LEGO = {"header": "radar", "caption": "chip", "transition": "scan", "palette": "amber", "ending": "prompt"}

and draws through lego.compose(story, idx, tl) (or lego.frame_maker(story) for engine.make_frame). The scene
illustrations stay the story's own; only the frame around them comes from here. policy.py reads LEGO and blocks:
  - the same full combination as any of the last COMBO_LOOKBACK Shorts,
  - one option used in the same slot MAX_PIECE_RUN + 1 Shorts in a row,
  - fewer than MIN_SLOTS_CHANGED slots changed from the previous Short.

Options (add one or two a week, see the content calendar):
  header      intel  - red bar + "// INTEL FILE" + FILE n/N (Chicken's Neck)
              radar  - mini radar scope with a live sweep + "TRACKING // TGT n" + segmented progress bar
  caption     typewriter - Hinglish chunk types itself into a dark box with a block cursor (Chicken's Neck)
              chip   - every word pops in as its own pill, hot words filled with their colour
  transition  shutter - two black plates part from the middle (Chicken's Neck)
              scan   - a bright scan line sweeps left to right and uncovers the new scene
  palette     intel  - teal-green HUD on near-black (Chicken's Neck)
              amber  - amber radar phosphor on warm black
  ending      poll   - HAAN / NAA poll card + COMMENT KARO bubble (Chicken's Neck)
              prompt - question card with a typing comment field and an arrow at the comment button
"""

import math

import cairo
import numpy as np

import engine
from engine import (CAPTION_FONT, H, PUNCT, W, circle, clamp, ease_in_out, ease_out_back, ease_out_cubic, hexc,
                    line, rgba, rrect, text, text_width, vignette)

MONO = "Consolas"
CAP_TOP, CAP_BOTTOM = 1150, 1250      # caption band, every caption style stays inside it
UI_CLEAR = H - 400                    # bottom 400px stay dark for the Shorts UI
SLOTS = ("header", "caption", "transition", "palette", "ending")

PALETTES = {
    "intel": {"ui": hexc("#7FD6B8"), "panel": (0.01, 0.02, 0.03), "alert": hexc("#FF3B3B"), "hi": hexc("#FFC83D"),
              "ink": (1, 1, 1)},
    "amber": {"ui": hexc("#FFB347"), "panel": (0.035, 0.022, 0.01), "alert": hexc("#FF4D2E"), "hi": hexc("#FFE07A"),
              "ink": hexc("#FFF4E0")},
}


# ============================================================ headers

def header_intel(ctx, idx, n, tl, dur, pal):
    rrect(ctx, 60, 70, 14, 50, 4)
    rgba(ctx, pal["alert"])
    ctx.fill()
    text(ctx, "REALITY SHIFT", 92, 95, 36, pal["ink"], a=0.9, anchor="l")
    text(ctx, "// INTEL FILE", 380, 95, 28, pal["ui"], font=MONO, a=0.75, anchor="l")
    if int(tl * 2) % 2 == 0:
        circle(ctx, W - 250, 95, 10, pal["alert"])
    text(ctx, f"FILE {idx + 1:02d}/{n:02d}", W - 70, 95, 30, pal["ink"], font=MONO, a=0.8, anchor="r")
    line(ctx, [(60, 140), (W - 60, 140)], pal["ui"], 1.5, 0.3)


def header_radar(ctx, idx, n, tl, dur, pal):
    cx, cy, r = 104, 104, 40
    circle(ctx, cx, cy, r, pal["panel"], 0.9)
    for k in (1.0, 0.62, 0.28):
        ctx.arc(cx, cy, r * k, 0, math.tau)
        rgba(ctx, pal["ui"], 0.55 if k == 1.0 else 0.3)
        ctx.set_line_width(2)
        ctx.stroke()
    ang = tl * 3.2 + idx * 1.3
    for k in range(12):  # sweep with a fading trail
        a0 = ang - k * 0.07
        ctx.move_to(cx, cy)
        ctx.arc(cx, cy, r, a0 - 0.07, a0)
        ctx.close_path()
        rgba(ctx, pal["ui"], 0.5 * (1 - k / 12))
        ctx.fill()
    bx, by = cx + 0.6 * r * math.cos(1.1 + idx), cy + 0.6 * r * math.sin(1.1 + idx)
    circle(ctx, bx, by, 5, pal["alert"], 0.5 + 0.5 * math.sin(tl * 9))
    text(ctx, "REALITY SHIFT", 166, 88, 36, pal["ink"], a=0.92, anchor="l")
    text(ctx, f"TRACKING // TGT {idx + 1:02d}", 166, 126, 24, pal["ui"], font=MONO, a=0.8, anchor="l")
    seg, gap = 46, 10
    x0 = W - 60 - n * seg - (n - 1) * gap
    for k in range(n):
        x = x0 + k * (seg + gap)
        rrect(ctx, x, 98, seg, 12, 4)
        rgba(ctx, pal["ui"], 0.22)
        ctx.fill()
        fill = 1.0 if k < idx else (clamp(tl / max(dur, 0.1)) if k == idx else 0.0)
        if fill > 0:
            rrect(ctx, x, 98, seg * fill, 12, 4)
            rgba(ctx, pal["hi"] if k == idx else pal["ui"], 0.95)
            ctx.fill()
    line(ctx, [(60, 168), (W - 60, 168)], pal["ui"], 1.5, 0.25)


HEADERS = {"intel": header_intel, "radar": header_radar}


# ============================================================ captions

def _current(sc, tl):
    cur = None
    for i, (start, _) in enumerate(sc["captions"]):
        if tl >= start - 0.03:
            cur = i
    return None if cur is None else sc["captions"][cur]


def caption_typewriter(ctx, sc, tl, accent, pal, hot):
    """The current Hinglish chunk types itself into a dark box with a block cursor."""
    cur = _current(sc, tl)
    if cur is None:
        return
    start, cap = cur
    shown = int(math.ceil(len(cap) * clamp((tl - start + 0.03) / 0.16)))
    size = 78
    words = cap.split(" ")
    ws = [text_width(ctx, w, size, font=CAPTION_FONT, bold=False) for w in words]
    gap = size * 0.28
    fit = min(1.0, 900 / (sum(ws) + gap * (len(ws) - 1)))
    h = CAP_BOTTOM - CAP_TOP
    rrect(ctx, 50, CAP_TOP, W - 100, h, 14)
    rgba(ctx, pal["panel"], 0.86)
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
        c = hot.get(w.strip(PUNCT + "."), pal["ink"])
        text(ctx, part, x, 0, size, c, font=CAPTION_FONT, bold=False, anchor="l", stroke=(0, 0, 0), stroke_w=8)
        x += (text_width(ctx, part, size, font=CAPTION_FONT, bold=False) if len(part) < len(w) else ww + gap)
        left -= len(w) + 1
    if shown < len(cap) or int(tl * 3) % 2 == 0:
        ctx.rectangle(x + 6, -size * 0.42, size * 0.38, size * 0.84)
        rgba(ctx, accent, 0.9)
        ctx.fill()
    ctx.restore()


def caption_chip(ctx, sc, tl, accent, pal, hot):
    """Every word of the current chunk pops in as its own pill; hot words are filled with their colour."""
    cur = _current(sc, tl)
    if cur is None:
        return
    start, cap = cur
    size, pad, gap, ch = 72, 20, 14, 100
    words = cap.split(" ")
    ws = [text_width(ctx, w, size, font=CAPTION_FONT, bold=False) + 2 * pad for w in words]
    total = sum(ws) + gap * (len(ws) - 1)
    fit = min(1.0, 980 / total)
    cy = (CAP_TOP + CAP_BOTTOM) / 2
    ctx.save()
    ctx.translate(W / 2, cy)
    ctx.scale(fit, fit)
    x = -total / 2
    for k, (w, ww) in enumerate(zip(words, ws)):
        u = tl - start + 0.03 - 0.06 * k
        if u < 0:
            break
        pop = ease_out_back(u / 0.2)
        c = hot.get(w.strip(PUNCT + "."))
        ctx.save()
        ctx.translate(x + ww / 2, 0)
        ctx.scale(pop, pop)
        rrect(ctx, -ww / 2, -ch / 2, ww, ch, ch / 2)
        rgba(ctx, c if c else pal["panel"], 0.95 if c else 0.88)
        ctx.fill_preserve()
        rgba(ctx, c if c else accent, 1.0 if c else 0.7)
        ctx.set_line_width(4)
        ctx.stroke()
        text(ctx, w, 0, 2, size, (0.04, 0.03, 0.02) if c else pal["ink"], font=CAPTION_FONT, bold=False)
        ctx.restore()
        x += ww + gap
    ctx.restore()


CAPTIONS = {"typewriter": caption_typewriter, "chip": caption_chip}


# ============================================================ transitions

def transition_shutter(ctx, tl, accent, pal):
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


def transition_scan(ctx, tl, accent, pal):
    u = ease_in_out(tl / 0.38)
    if u >= 1:
        return
    x = -40 + u * (W + 80)
    ctx.rectangle(x, 0, W - x, H)
    rgba(ctx, pal["panel"])
    ctx.fill()
    for gx in range(0, W, 60):  # the uncovered grid ahead of the line
        if gx > x:
            line(ctx, [(gx, 0), (gx, H)], pal["ui"], 1, 0.12)
    for gy in range(0, H, 60):
        line(ctx, [(max(x, 0), gy), (W, gy)], pal["ui"], 1, 0.12)
    g = cairo.LinearGradient(x - 160, 0, x, 0)
    g.add_color_stop_rgba(0, *accent, 0)
    g.add_color_stop_rgba(1, *accent, 0.45)
    ctx.rectangle(x - 160, 0, 160, H)
    ctx.set_source(g)
    ctx.fill()
    line(ctx, [(x, 0), (x, H)], accent, 22, 0.45)
    line(ctx, [(x, 0), (x, H)], (1, 1, 1), 5, 0.95)


TRANSITIONS = {"shutter": transition_shutter, "scan": transition_scan}


# ============================================================ endings (drawn by the story's last scene)

def ending_poll(ctx, t, u, uc, pal, question=("?",), options=("HAAN", "NAA"), y=560, **_):
    """Poll card: question, two options that pulse, then a COMMENT KARO bubble once uc > 0."""
    pop = ease_out_back(u / 0.35)
    ctx.save()
    ctx.translate(540, y)
    ctx.scale(pop, pop)
    rrect(ctx, -440, -330, 880, 640, 26)
    rgba(ctx, pal["panel"], 0.95)
    ctx.fill_preserve()
    rgba(ctx, pal["hi"])
    ctx.set_line_width(5)
    ctx.stroke()
    text(ctx, "POLL", -380, -270, 34, pal["hi"], font=MONO, anchor="l")
    for k, q in enumerate(question[:2]):
        text(ctx, q, 0, -190 + 90 * k, 84, pal["ink"] if k == 0 else pal["hi"], font=CAPTION_FONT, bold=False)
    for k, (opt, c) in enumerate(zip(options, (hexc("#138808"), pal["alert"]))):
        oy = 20 + k * 130
        hl = 0.5 + 0.5 * math.sin(t * 5 + k * math.pi)
        rrect(ctx, -360, oy - 50, 720, 100, 50)
        rgba(ctx, c, 0.18 + 0.2 * hl * clamp(uc / 0.3))
        ctx.fill_preserve()
        rgba(ctx, c)
        ctx.set_line_width(4)
        ctx.stroke()
        circle(ctx, -300, oy, 22, c)
        text(ctx, opt, -250, oy + 2, 64, pal["ink"], font=CAPTION_FONT, bold=False, anchor="l")
    if uc > 0:
        k = ease_out_back(uc / 0.3)
        ctx.save()
        ctx.translate(250, 290)
        ctx.scale(k, k)
        rrect(ctx, -200, -50, 400, 100, 30)
        ctx.move_to(-120, 50)
        ctx.line_to(-150, 90)
        ctx.line_to(-80, 50)
        rgba(ctx, pal["hi"])
        ctx.fill()
        text(ctx, "COMMENT KARO", 0, 2, 50, (0.05, 0.05, 0.05), font=CAPTION_FONT, bold=False)
        ctx.restore()
    ctx.restore()


def ending_prompt(ctx, t, u, uc, pal, question=("?",), suggestions=("...",), y=600, **_):
    """Question card with a comment field that types suggestions in turn; an arrow points at the comment button."""
    pop = ease_out_back(u / 0.35)
    ctx.save()
    ctx.translate(540, y)
    ctx.scale(pop, pop)
    rrect(ctx, -450, -300, 900, 560, 30)
    rgba(ctx, pal["panel"], 0.95)
    ctx.fill_preserve()
    rgba(ctx, pal["ui"])
    ctx.set_line_width(5)
    ctx.stroke()
    text(ctx, "> AAPKI BAARI", -390, -245, 34, pal["ui"], font=MONO, anchor="l")
    for k, q in enumerate(question[:2]):
        text(ctx, q, 0, -150 + 95 * k, 86, pal["ink"] if k == 0 else pal["hi"], font=CAPTION_FONT, bold=False)
    rrect(ctx, -390, 60, 780, 120, 24)  # the comment field
    rgba(ctx, (0, 0, 0), 0.6)
    ctx.fill_preserve()
    rgba(ctx, pal["hi"] if uc > 0 else pal["ui"], 0.9)
    ctx.set_line_width(4)
    ctx.stroke()
    if uc > 0:
        per = 1.1
        idx = int(uc / per) % len(suggestions)
        s = suggestions[idx]
        shown = s[:int(math.ceil(len(s) * clamp(((uc % per) - 0.05) / 0.45)))]
        tw = text(ctx, shown, -350, 120, 60, pal["ink"], font=CAPTION_FONT, bold=False, anchor="l") if shown else 0
    else:
        tw = text(ctx, "Comment likho...", -350, 120, 52, pal["ui"], font=CAPTION_FONT, bold=False, a=0.45,
                  anchor="l") * 0
    if int(t * 3) % 2 == 0:
        ctx.rectangle(-344 + tw, 92, 6, 56)
        rgba(ctx, pal["hi"])
        ctx.fill()
    ctx.restore()
    if uc > 0:  # arrow toward the Shorts comment button on the right edge
        k = ease_out_cubic(uc / 0.4)
        bob = 10 * math.sin(t * 6)
        x0, y0 = 930, y + 330
        x1, y1 = lerp_pt(x0, 1010, k), lerp_pt(y0, y + 500, k) + bob
        line(ctx, [(x0, y0), (x1, y1)], pal["hi"], 12)
        ang = math.atan2(y1 - y0, x1 - x0)
        ctx.move_to(x1 + 34 * math.cos(ang), y1 + 34 * math.sin(ang))
        for da in (2.4, -2.4):
            ctx.line_to(x1 + 30 * math.cos(ang + da), y1 + 30 * math.sin(ang + da))
        ctx.close_path()
        rgba(ctx, pal["hi"])
        ctx.fill()
        text(ctx, "COMMENT", x0 - 20, y0 - 2, 44, pal["hi"], font=CAPTION_FONT, bold=False, anchor="r",
             stroke=(0, 0, 0), stroke_w=8)


def lerp_pt(a, b, u):
    return a + (b - a) * u


ENDINGS = {"poll": ending_poll, "prompt": ending_prompt}
OPTIONS = {"header": HEADERS, "caption": CAPTIONS, "transition": TRANSITIONS, "palette": PALETTES, "ending": ENDINGS}


# ============================================================ assembly

def palette(story):
    return PALETTES[story.LEGO["palette"]]


def ending(story, ctx, t, u, uc, **kw):
    """Draw the story's chosen ending piece; u = time since the card appears, uc = time since the comment ask."""
    if u > 0:
        ENDINGS[story.LEGO["ending"]](ctx, t, u, uc, palette(story), **kw)


def compose(story, idx, tl, drift=14, push=0.04):
    sc = engine.SCENES[idx]
    spec = story.SPEC[idx]
    lego, pal = story.LEGO, palette(story)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    zoom = 1.0 + push * tl / sc["dur"]
    ctx.save()
    ctx.translate(W / 2 + drift * math.sin(tl * 0.5 + idx), H * 0.4)
    ctx.scale(zoom, zoom)
    ctx.translate(-W / 2, -H * 0.4)
    sc["obj"].draw(ctx, tl, sc["dur"])
    ctx.restore()
    vignette(ctx)
    g = cairo.LinearGradient(0, CAP_BOTTOM + 20, 0, UI_CLEAR)
    g.add_color_stop_rgba(0, *pal["panel"], 0)
    g.add_color_stop_rgba(1, *pal["panel"], 0.95)
    ctx.rectangle(0, CAP_BOTTOM + 20, W, H)
    ctx.set_source(g)
    ctx.fill()
    ctx.rectangle(0, UI_CLEAR, W, H - UI_CLEAR)
    rgba(ctx, pal["panel"], 0.95)
    ctx.fill()
    HEADERS[lego["header"]](ctx, idx, len(story.SPEC), tl, sc["dur"], pal)
    CAPTIONS[lego["caption"]](ctx, sc, tl, spec["accent"], pal, story.HOT)
    if idx:
        TRANSITIONS[lego["transition"]](ctx, tl, spec["accent"], pal)
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


def combo(lego: dict) -> str:
    return "/".join(lego[s] for s in SLOTS)
