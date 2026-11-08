"""Colour grading for source artwork (applied once per source image, not per frame).

Old prints and miniatures are flat and bright; these grades push them toward a controlled cinematic look:
contrast curve, split-toning (cool shadows / warm highlights), saturation control and a gentle bloom.
No heavy glow: bloom strength is capped so faces don't wash out.
"""

from __future__ import annotations

import numpy as np
from PIL import Image, ImageFilter

GRADES = {
    #            contrast  sat   shadows tint        highlights tint      exposure  bloom
    "cinematic": (1.18, 0.92, (-0.02, 0.01, 0.04), (0.04, 0.015, -0.03), 0.96, 0.10),
    "night":     (1.20, 0.72, (-0.03, 0.00, 0.07), (0.00, 0.00, 0.02), 0.82, 0.06),
    "poison":    (1.30, 0.62, (-0.05, 0.06, 0.02), (0.00, 0.05, -0.02), 0.62, 0.06),
    "divine":    (1.12, 0.95, (-0.01, 0.00, 0.03), (0.06, 0.03, -0.02), 1.00, 0.16),
    "warm":      (1.14, 0.98, (0.00, -0.01, 0.01), (0.06, 0.025, -0.04), 0.97, 0.10),
    "cold":      (1.15, 0.80, (-0.03, 0.00, 0.06), (0.00, 0.01, 0.04), 0.88, 0.06),
}


def _s_curve(x: np.ndarray, k: float) -> np.ndarray:
    # contrast around mid-grey with soft shoulders (keeps highlights from clipping)
    y = 0.5 + (x - 0.5) * k
    return np.clip(y - 0.08 * (k - 1) * np.sin(2 * np.pi * x) / (2 * np.pi), 0, 1)


def apply(img: Image.Image, grade: str = "cinematic") -> Image.Image:
    contrast, sat, sh, hi, expo, bloom = GRADES[grade]
    a = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
    a = np.clip(a * expo, 0, 1)
    lum = (a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32))[..., None]
    a = np.clip(lum + (a - lum) * sat, 0, 1)
    a = _s_curve(a, contrast)
    lum = (a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32))[..., None]
    w_sh = np.clip(1 - lum * 2, 0, 1)
    w_hi = np.clip(lum * 2 - 1, 0, 1)
    a = np.clip(a + w_sh * np.array(sh, np.float32) + w_hi * np.array(hi, np.float32), 0, 1)
    out = Image.fromarray((a * 255).astype(np.uint8))
    if bloom > 0:
        bright = np.clip((a - 0.62) / 0.38, 0, 1)
        b = Image.fromarray((bright * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(max(4, img.width // 90)))
        bb = np.asarray(b, np.float32) / 255.0
        a = 1 - (1 - a) * (1 - bb * bloom)   # screen blend
        out = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    return out
