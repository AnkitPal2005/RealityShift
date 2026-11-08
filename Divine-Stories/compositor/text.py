"""Correct Devanagari text for Cairo: HarfBuzz shapes the string, glyph outlines become Cairo paths.

Cairo's own text API does no complex-script shaping (matras and conjuncts break), and this Pillow build has
no libraqm. uharfbuzz (free, pip wheel) does full OpenType shaping with the system Nirmala UI font, and we
draw the glyph outlines ourselves, which also gives us clean strokes/outlines for captions.
"""

from __future__ import annotations

from functools import lru_cache

import cairo
import uharfbuzz as hb

from config import settings as S


@lru_cache(maxsize=None)
def _blob():
    return hb.Blob.from_file_path(str(S.DEVANAGARI_FONT))


@lru_cache(maxsize=None)
def _font(face_idx: int):
    face = hb.Face(_blob(), face_idx)
    return face, hb.Font(face)


class _Pen:
    """fontTools-style pen that writes into a Cairo context (font units -> pixels, y flipped)."""

    def __init__(self, ctx, x, y, sc):
        self.ctx, self.x, self.y, self.sc = ctx, x, y, sc
        self.cur = (0, 0)

    def _p(self, p):
        return self.x + p[0] * self.sc, self.y - p[1] * self.sc

    def moveTo(self, p):
        self.ctx.move_to(*self._p(p))
        self.cur = p

    def lineTo(self, p):
        self.ctx.line_to(*self._p(p))
        self.cur = p

    def curveTo(self, a, b, c):
        self.ctx.curve_to(*self._p(a), *self._p(b), *self._p(c))
        self.cur = c

    def qCurveTo(self, a, b):
        x0, y0 = self.cur
        c1 = (x0 + 2 / 3 * (a[0] - x0), y0 + 2 / 3 * (a[1] - y0))
        c2 = (b[0] + 2 / 3 * (a[0] - b[0]), b[1] + 2 / 3 * (a[1] - b[1]))
        self.curveTo(c1, c2, b)

    def closePath(self):
        self.ctx.close_path()

    def endPath(self):
        pass


@lru_cache(maxsize=4096)
def shape(txt: str, face_idx: int = S.FONT_FACE_BOLD) -> tuple[tuple[tuple[int, int, int], ...], int, int]:
    """Return (glyphs as (gid, x, y) in font units, total advance, upem)."""
    face, font = _font(face_idx)
    buf = hb.Buffer()
    buf.add_str(txt)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    x, out = 0, []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        out.append((info.codepoint, x + pos.x_offset, pos.y_offset))
        x += pos.x_advance
    return tuple(out), x, face.upem


def width(txt: str, size: float, face_idx: int = S.FONT_FACE_BOLD) -> float:
    _, adv, upem = shape(txt, face_idx)
    return adv * size / upem


def path(ctx: cairo.Context, txt: str, x: float, y: float, size: float, face_idx: int = S.FONT_FACE_BOLD) -> float:
    """Append the text outline to ctx's current path with its baseline-left at (x, y). Returns advance in px."""
    glyphs, adv, upem = shape(txt, face_idx)
    sc = size / upem
    _, font = _font(face_idx)
    for gid, gx, gy in glyphs:
        font.draw_glyph_with_pen(gid, _Pen(ctx, x + gx * sc, y - gy * sc, sc))
    return adv * sc


def draw(ctx: cairo.Context, txt: str, x: float, y: float, size: float, color=(1, 1, 1), alpha: float = 1.0,
         face_idx: int = S.FONT_FACE_BOLD, anchor: str = "c", stroke: float = 0.0, stroke_color=(0, 0, 0),
         shadow: float = 0.0) -> float:
    """Draw text vertically centred on y (approx.), horizontally anchored l/c/r on x. Returns width."""
    w = width(txt, size, face_idx)
    x0 = x - w / 2 if anchor == "c" else (x - w if anchor == "r" else x)
    base = y + size * 0.36          # Nirmala: visual centre of Devanagari ~0.36 em above baseline
    if shadow > 0:
        ctx.new_path()
        path(ctx, txt, x0 + shadow * 0.4, base + shadow * 0.6, size, face_idx)
        ctx.set_source_rgba(0, 0, 0, 0.45 * alpha)
        ctx.fill()
    ctx.new_path()
    path(ctx, txt, x0, base, size, face_idx)
    if stroke > 0:
        ctx.set_source_rgba(*stroke_color, alpha)
        ctx.set_line_width(stroke)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke_preserve()
    ctx.set_source_rgba(*color, alpha)
    ctx.fill()
    return w
