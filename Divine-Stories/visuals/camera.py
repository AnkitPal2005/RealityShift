"""Virtual camera over a still image: Ken Burns zoom/pan with easing, a subtle handheld drift,
clamping so the frame never shows outside the artwork, and image->screen mapping for anchored effects."""

from __future__ import annotations

import math
from dataclasses import dataclass

from PIL import Image, ImageFilter

from config import settings as S
from visuals import grade as G


def ease(u: float) -> float:
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def prepare(path, bounds=(0, 0, 1, 1), grade="cinematic", max_zoom=1.6) -> Image.Image:
    """Crop to the artwork bounds, grade, and resample once so the tightest zoom is still ~1:1 or close."""
    im = Image.open(path).convert("RGB")
    w, h = im.size
    x0, y0, x1, y1 = bounds
    im = im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
    w, h = im.size
    cover = max(S.W / w, S.H / h)
    need = min(cover * max_zoom, 3.2)          # cap memory; beyond this we accept softness
    if need > 1.0:
        im = im.resize((int(w * need), int(h * need)), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=70, threshold=2))
    return G.apply(im, grade)


@dataclass
class Shot:
    src: Image.Image
    focus: tuple[float, float]          # normalized centre at t=0
    pan: tuple[float, float]            # normalized shift of the centre over the shot
    zoom: tuple[float, float]           # zoom multipliers relative to "cover" at t=0 and t=end
    dur: float

    def rect(self, t: float) -> tuple[float, float, float, float]:
        u = ease(t / max(self.dur, 1e-3))
        sw, sh = self.src.size
        z = self.zoom[0] + (self.zoom[1] - self.zoom[0]) * u
        cover = max(S.W / sw, S.H / sh)
        vw, vh = S.W / (cover * z), S.H / (cover * z)
        cx = (self.focus[0] + self.pan[0] * u) * sw + math.sin(t * 0.7) * sw * 0.0025
        cy = (self.focus[1] + self.pan[1] * u) * sh + math.cos(t * 0.53) * sh * 0.0025
        cx = min(max(cx, vw / 2), sw - vw / 2)
        cy = min(max(cy, vh / 2), sh - vh / 2)
        return cx - vw / 2, cy - vh / 2, cx + vw / 2, cy + vh / 2

    def frame(self, t: float) -> Image.Image:
        return self.src.transform((S.W, S.H), Image.EXTENT, self.rect(t), Image.BILINEAR)

    def to_screen(self, t: float, p: tuple[float, float]) -> tuple[float, float]:
        """Map a normalized point in the (cropped) artwork to screen pixels at time t."""
        x0, y0, x1, y1 = self.rect(t)
        sw, sh = self.src.size
        return (p[0] * sw - x0) / (x1 - x0) * S.W, (p[1] * sh - y0) / (y1 - y0) * S.H

    def scale(self, t: float) -> float:
        x0, _, x1, _ = self.rect(t)
        return S.W / (x1 - x0)
