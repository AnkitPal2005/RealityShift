"""Animated Hindi captions synced to edge-tts word boundaries, plus on-screen labels, title cards and branding."""

from __future__ import annotations

import math

import cairo

from compositor import text as T
from config import settings as S

GOLD = (1.0, 0.80, 0.32)
SAFFRON = (1.0, 0.56, 0.16)
WHITE = (1.0, 1.0, 1.0)
SKY = (0.55, 0.80, 1.0)
CAP_SIZE = 84
CAP_Y = 1290                    # caption centre; bottom of captions stays well above H - SAFE_BOTTOM (1500)
CAP_MAX_W = 800
CAP_CX = (S.W - S.SAFE_RIGHT) / 2 + 30   # nudge left of the right-rail buttons
PUNCT = "।,.?!…;:\"'"


def _ease_back(u):
    u = min(1.0, max(0.0, u))
    c = 1.7
    return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2


def align_tokens(narration: str, words: list[dict]) -> list[dict]:
    """Attach the display token (with its punctuation) from the narration to each timed boundary word."""
    toks = [t for t in narration.replace("...", "… ").split() if t.strip(PUNCT)]
    out, j = [], 0
    for w in words:
        disp = w["w"]
        while j < len(toks):
            core = toks[j].strip(PUNCT)
            j += 1
            if core == w["w"] or core.startswith(w["w"]) or w["w"].startswith(core):
                disp = toks[j - 1]
                break
        out.append({**w, "disp": disp})
    return out


def chunk(words: list[dict], scene_end: float) -> list[dict]:
    """Group words into caption chunks (3 words, width-limited, break after punctuation).
    A 4th word is allowed when it closes the phrase, so a sentence never leaves a one-word orphan."""
    chunks, cur = [], []
    for w in words:
        trial = " ".join(x["disp"].strip("…,।;:") for x in cur + [w])
        closes = w["disp"][-1:] in "।,?!…"
        limit = 4 if closes else 3
        if cur and (len(cur) >= limit or T.width(trial, CAP_SIZE) > CAP_MAX_W):
            chunks.append(cur)
            cur = []
        cur.append(w)
        if w["disp"][-1:] in "।,?!…":
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        end = chunks[i + 1][0]["t"] if i + 1 < len(chunks) else scene_end
        out.append({"start": c[0]["t"], "end": end, "words": c})
    return out


def draw_caption(ctx: cairo.Context, chunks: list[dict], t: float, highlight: set[str]) -> None:
    cur = next((c for c in chunks if c["start"] - 0.06 <= t < c["end"]), None)
    if cur is None:
        return
    u = (t - cur["start"] + 0.06) / 0.18
    k = _ease_back(u)
    a = min(1.0, max(0.0, u * 1.5))
    disp = [w["disp"].strip("…,।;:\"") for w in cur["words"]]
    gap = CAP_SIZE * 0.28
    ws = [T.width(d, CAP_SIZE) for d in disp]
    total = sum(ws) + gap * (len(ws) - 1)
    ctx.save()
    ctx.translate(CAP_CX, CAP_Y + (1 - k) * 26)
    ctx.scale(0.9 + 0.1 * k, 0.9 + 0.1 * k)
    # soft dark backing so captions read on any painting
    g = cairo.RadialGradient(0, 0, 10, 0, 0, total * 0.7 + 60)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.42 * a)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g)
    ctx.save()
    ctx.scale(1, 0.32)
    ctx.arc(0, 0, total * 0.7 + 60, 0, math.tau)
    ctx.fill()
    ctx.restore()
    x = -total / 2
    for w, d, ww in zip(cur["words"], disp, ws):
        active = w["t"] <= t < w["t"] + max(w.get("d", 0.3), 0.18) + 0.08
        core = d.strip(PUNCT)
        color = GOLD if core in highlight else WHITE
        sc = 1.0
        if active:
            sc = 1.08
            color = GOLD if core in highlight else (1.0, 0.95, 0.82)
        ctx.save()
        ctx.translate(x + ww / 2, 0)
        ctx.scale(sc, sc)
        T.draw(ctx, d, 0, 0, CAP_SIZE, color, a, anchor="c", stroke=11, stroke_color=(0.04, 0.02, 0.0),
               shadow=5)
        if active and core in highlight:
            ctx.set_source_rgba(*GOLD, 0.9 * a)
            ctx.rectangle(-ww / 2, CAP_SIZE * 0.62, ww, 6)
            ctx.fill()
        ctx.restore()
        x += ww + gap
    ctx.restore()


def draw_label(ctx, label: str, t: float, popular: bool) -> None:
    if not label:
        return
    a = min(1.0, max(0.0, (t - 0.15) / 0.35))
    if a <= 0:
        return
    size = 34
    w = T.width(label, size, S.FONT_FACE_REGULAR)
    x, y, h = 60 - (1 - a) * 30, 262, 62
    col = SKY if popular else GOLD
    ctx.save()
    ctx.new_path()
    r = 14
    ctx.arc(x + r, y - h / 2 + r, r, math.pi, 1.5 * math.pi)
    ctx.arc(x + w + 48 - r, y - h / 2 + r, r, 1.5 * math.pi, 2 * math.pi)
    ctx.arc(x + w + 48 - r, y + h / 2 - r, r, 0, 0.5 * math.pi)
    ctx.arc(x + r, y + h / 2 - r, r, 0.5 * math.pi, math.pi)
    ctx.close_path()
    ctx.set_source_rgba(0.03, 0.02, 0.01, 0.62 * a)
    ctx.fill_preserve()
    ctx.set_source_rgba(*col, 0.85 * a)
    ctx.set_line_width(2.5)
    ctx.stroke()
    ctx.rectangle(x + 12, y - 14, 5, 28)
    ctx.fill()
    T.draw(ctx, label, x + 30, y, size, (1, 0.96, 0.9), a, S.FONT_FACE_REGULAR, anchor="l")
    ctx.restore()


def draw_title(ctx, title: str, u: float, y: float = 700) -> None:
    """Big reveal word (e.g. नीलकंठ). u = seconds since the title cue."""
    if not title or u < 0:
        return
    k = _ease_back(u / 0.45)
    a = min(1.0, u / 0.25)
    size = 168
    ctx.save()
    ctx.translate(S.W / 2, y)
    ctx.scale(0.75 + 0.25 * k, 0.75 + 0.25 * k)
    w = T.width(title, size)
    g = cairo.RadialGradient(0, 0, 20, 0, 0, w * 0.75)
    g.add_color_stop_rgba(0, 1.0, 0.75, 0.3, 0.28 * a)
    g.add_color_stop_rgba(1, 1.0, 0.75, 0.3, 0)
    ctx.set_source(g)
    ctx.arc(0, 0, w * 0.75, 0, math.tau)
    ctx.fill()
    T.draw(ctx, title, 0, 0, size, GOLD, a, anchor="c", stroke=16, stroke_color=(0.08, 0.03, 0.0), shadow=8)
    ctx.restore()


def draw_branding(ctx, t: float) -> None:
    """Small channel mark top-left (below the Shorts top bar): a trishul glyph + channel name."""
    x, y = 62, 190
    ctx.save()
    ctx.set_source_rgba(*GOLD, 0.92)
    ctx.set_line_width(4)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(x, y + 26)
    ctx.line_to(x, y - 22)
    ctx.stroke()
    ctx.move_to(x - 15, y - 16)
    ctx.curve_to(x - 15, y - 2, x + 15, y - 2, x + 15, y - 16)
    ctx.stroke()
    for dx in (-15, 0, 15):
        ctx.move_to(x + dx - 5, y - 16 - (8 if dx == 0 else 0))
        ctx.line_to(x + dx, y - 28 - (8 if dx == 0 else 0))
        ctx.line_to(x + dx + 5, y - 16 - (8 if dx == 0 else 0))
        ctx.close_path()
        ctx.fill()
    T.draw(ctx, S.CHANNEL_NAME_HI, x + 32, y, 36, (1, 0.97, 0.9), 0.92, S.FONT_FACE_BOLD, anchor="l",
           stroke=4, stroke_color=(0, 0, 0))
    ctx.restore()
