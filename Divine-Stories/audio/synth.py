"""Procedural audio: tanpura-style drone score + synthesized SFX. Everything is generated here, so the
music and effects carry no third-party licence. Mono float32 at settings.SAMPLE_RATE unless noted."""

from __future__ import annotations

import math
from functools import lru_cache

import numpy as np

from config import settings as S

SR = S.SAMPLE_RATE


def _t(sec: float) -> np.ndarray:
    return np.arange(int(sec * SR)) / SR


def _rng(seed):
    return np.random.default_rng(seed)


def moving_avg(x: np.ndarray, k: int) -> np.ndarray:
    """Centred moving average in O(n) via cumulative sums (np.convolve is O(n*k) - far too slow for audio)."""
    k = max(1, int(k))
    c = np.cumsum(np.concatenate([np.zeros(1), np.pad(x, (k // 2, k - 1 - k // 2), mode="edge")]))
    return (c[k:] - c[:-k]) / k


def lowpass(x: np.ndarray, cutoff: float) -> np.ndarray:
    """Zero-phase FFT brick-ish lowpass with a soft roll-off (fine for synthesis, not for mastering)."""
    n = len(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    X = np.fft.rfft(x)
    X *= 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, n)


def bandpass(x, lo, hi):
    return lowpass(x, hi) - lowpass(x, lo)


def pink(n: int, seed: int = 0) -> np.ndarray:
    r = _rng(seed)
    X = np.fft.rfft(r.standard_normal(n))
    f = np.fft.rfftfreq(n)
    f[0] = 1
    y = np.fft.irfft(X / np.sqrt(f), n)
    return y / (np.abs(y).max() + 1e-9)


def norm(x, peak=0.9):
    return x * (peak / (np.abs(x).max() + 1e-9))


# ---------------------------------------------------------------- tanpura

@lru_cache(maxsize=16)
def tanpura_pluck(f0: float, dur: float = 5.0, seed: int = 0) -> np.ndarray:
    """One string pluck with 'jawari' buzz: a formant that sweeps up through the harmonics as it decays."""
    t = _t(dur)
    r = _rng(seed)
    out = np.zeros_like(t)
    centre = 3 + 11 * (1 - np.exp(-t / 1.4))          # sweeping emphasis -> the shimmering buzz
    for k in range(1, 26):
        detune = 1 + r.uniform(-0.0006, 0.0006)
        amp = (1 / k ** 0.85) * (1 + 1.8 * np.exp(-((k - centre) ** 2) / 6))
        decay = np.exp(-t / (3.2 / (1 + 0.08 * k)))
        out += amp * decay * np.sin(2 * np.pi * f0 * k * detune * t + r.uniform(0, 6.28))
    att = np.minimum(1, t / 0.012)
    return norm(out * att, 0.8)


def tanpura(dur: float, sa: float = 146.83, cycle: float = 3.4, seed: int = 1) -> np.ndarray:
    """Pa - Sa' - Sa' - Sa (low) cycle, the classic four-string pattern."""
    n = int(dur * SR)
    out = np.zeros(n + int((cycle + 6) * SR))   # room for the last cycle's plucks to ring out
    strings = [sa * 3 / 4, sa, sa, sa / 2]
    r = _rng(seed)
    t0 = 0.0
    while t0 < dur:
        for i, f in enumerate(strings):
            p = tanpura_pluck(round(f, 2), 5.0, i)
            s = int((t0 + i * cycle / 4 + r.uniform(-0.02, 0.02)) * SR)
            out[s:s + len(p)] += p * (0.9 if i != 3 else 1.1) * r.uniform(0.85, 1.0)
        t0 += cycle
    return out[:n]


def drone_pad(dur: float, sa: float = 146.83, seed: int = 2) -> np.ndarray:
    t = _t(dur)
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * t / 9.0)
    sub = np.sin(2 * np.pi * sa / 2 * t) * 0.5 + np.sin(2 * np.pi * sa * 3 / 4 * t + 1) * 0.18
    air = lowpass(pink(len(t), seed), 420) * 0.6
    return (sub * (0.6 + 0.4 * lfo) + air * (0.5 + 0.5 * lfo)) * 0.5


def drum_hit(seed=0, f_hi=90, f_lo=42, dur=1.2) -> np.ndarray:
    """Low cinematic drum (dhol/taiko-like): pitch-dropping sine body + short noise skin."""
    t = _t(dur)
    f = f_lo + (f_hi - f_lo) * np.exp(-t / 0.08)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.35)
    skin = lowpass(_rng(seed).standard_normal(len(t)), 1800) * np.exp(-t / 0.03) * 0.5
    return norm(body + skin, 0.95)


def reverb(x: np.ndarray, seconds: float = 2.4, wet: float = 0.28, seed: int = 5) -> np.ndarray:
    """Convolution with a synthetic exponentially decaying noise impulse (stereo out)."""
    r = _rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    out = []
    for ch in range(2):
        ir = r.standard_normal(n) * np.exp(-t * 6.9 / seconds)
        ir = lowpass(ir, 5200 if ch == 0 else 4800)
        ir[:int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))
        ir /= np.sqrt((ir ** 2).sum()) + 1e-9
        m = len(x) + n - 1
        size = 1 << (m - 1).bit_length()
        y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[:len(x)]
        out.append(x * (1 - wet) + y * wet * 3.0)
    return np.stack(out, axis=1)


# ---------------------------------------------------------------- score

INTENSITY = {"hook": 0.8, "setup": 0.45, "rising": 0.7, "climax": 0.95, "reveal": 1.0, "tradition": 0.5,
             "meaning": 0.75, "question": 0.4, "conclusion": 0.45}


def score(timeline: list[dict], total: float, sa: float = 146.83) -> np.ndarray:
    """Stereo music bed that follows the story's beats. timeline: [{start, dur, beat}]."""
    n = int(total * SR)
    tan = tanpura(total + 1, sa)[:n]
    pad = drone_pad(total + 1, sa)[:n]
    env = np.zeros(n)
    for sc in timeline:   # smooth per-scene intensity curve
        s, e = int(sc["start"] * SR), int((sc["start"] + sc["dur"]) * SR)
        env[s:e] = INTENSITY.get(sc["beat"], 0.6)
    k = int(0.8 * SR)
    env = moving_avg(env, k)
    drums = np.zeros(n)
    hit = drum_hit()
    for sc in timeline:   # slow heartbeat drums in tense beats (~66 bpm)
        if sc["beat"] in ("rising", "climax", "hook"):
            t = sc["start"] + 0.2
            while t < sc["start"] + sc["dur"] - 0.3:
                s = int(t * SR)
                seg = hit[: max(0, min(len(hit), n - s))]
                drums[s:s + len(seg)] += seg * (0.55 if sc["beat"] != "climax" else 0.75)
                t += 0.91
    mix = tan * 0.55 * (0.7 + 0.3 * env) + pad * (0.4 + 0.6 * env) + drums * 0.5
    fade_in, fade_out = int(0.6 * SR), int(2.0 * SR)
    mix[:fade_in] *= np.linspace(0, 1, fade_in)
    mix[-fade_out:] *= np.linspace(1, 0, fade_out)
    return norm(reverb(mix, 2.6, 0.3), 0.8)


# ---------------------------------------------------------------- SFX

def sfx(kind: str, seed: int = 0) -> np.ndarray:
    r = _rng(seed)
    if kind == "whoosh":
        d = 0.9
        t = _t(d)
        x = r.standard_normal(len(t))
        env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
        lo = lowpass(x, 700) * (1 - t / d) + lowpass(x, 3500) * (t / d)   # brightening sweep
        return norm(lo * env, 0.8)
    if kind == "boom":
        d = 2.8
        t = _t(d)
        f = 34 + 40 * np.exp(-t / 0.15)
        body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.9)
        rumble = lowpass(r.standard_normal(len(t)), 160) * np.exp(-t / 0.7) * 2.5
        return norm(body + rumble, 0.95)
    if kind == "thunder":
        d = 3.5
        t = _t(d)
        crack = bandpass(r.standard_normal(len(t)), 300, 5000) * np.exp(-t / 0.08)
        roll = lowpass(np.cumsum(r.standard_normal(len(t))) * 0.02, 240)
        roll = roll / (np.abs(roll).max() + 1e-9) * (1 - np.exp(-t / 0.15)) * np.exp(-t / 1.3)
        return norm(crack * 0.7 + roll, 0.95)
    if kind == "bell":   # temple bell: inharmonic partials, long decay
        d = 5.0
        t = _t(d)
        f0 = 392.0
        out = np.zeros_like(t)
        for ratio, amp, dec in ((0.5, 0.6, 3.5), (1.0, 1.0, 2.8), (1.19, 0.5, 2.0), (1.56, 0.45, 1.6),
                                (2.0, 0.35, 1.3), (2.51, 0.25, 0.9), (2.66, 0.2, 0.8), (3.01, 0.15, 0.6)):
            out += amp * np.exp(-t / dec) * np.sin(2 * np.pi * f0 * ratio * t * (1 + 0.0015 * np.sin(2 * np.pi * 3 * t)))
        out *= np.minimum(1, t / 0.004)
        return norm(out, 0.7)
    if kind == "shimmer":
        d = 2.5
        t = _t(d)
        out = sum(np.sin(2 * np.pi * f * t + r.uniform(0, 6)) * (0.5 + 0.5 * np.sin(2 * np.pi * (5 + i) * t))
                  for i, f in enumerate((1760, 2217, 2637, 3520, 4186)))
        env = np.minimum(1, t / 0.6) * np.exp(-np.maximum(0, t - 0.6) / 0.8)
        return norm(out * env, 0.5)
    if kind == "riser":
        d = 2.2
        t = _t(d)
        x = r.standard_normal(len(t))
        out = lowpass(x, 400) * (1 - t / d) + bandpass(x, 1500, 6000) * (t / d) ** 2
        tone = np.sin(2 * np.pi * np.cumsum(110 + 220 * (t / d) ** 2) / SR) * 0.4
        return norm((out + tone) * (t / d) ** 1.5, 0.75)
    if kind == "fire":
        d = 3.0
        t = _t(d)
        base = lowpass(pink(len(t), seed), 900) * 0.6
        crackle = np.zeros_like(t)
        for _ in range(90):
            p = r.integers(0, len(t) - 400)
            crackle[p:p + 400] += r.uniform(0.3, 1) * np.exp(-np.arange(400) / 40) * r.standard_normal(400)
        env = np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.8)
        return norm((base + bandpass(crackle, 1200, 7000)) * env, 0.6)
    if kind == "waves":
        d = 5.0
        t = _t(d)
        x = lowpass(pink(len(t), seed + 3), 1100)
        am = 0.35 + 0.65 * (0.5 + 0.5 * np.sin(2 * np.pi * t / 2.4 - 1.5)) ** 2
        env = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 1.2)
        return norm(x * am * env, 0.6)
    if kind == "wind":
        d = 5.5
        t = _t(d)
        x = bandpass(pink(len(t), seed + 4), 200, 1400)
        am = 0.5 + 0.5 * np.sin(2 * np.pi * t / 3.1) * np.sin(2 * np.pi * t / 1.7 + 1)
        env = np.minimum(1, t / 0.8) * np.minimum(1, (d - t) / 1.5)
        return norm(x * am * env, 0.6)
    raise ValueError(f"unknown sfx {kind}")


SFX_KINDS = ("whoosh", "boom", "thunder", "bell", "shimmer", "riser", "fire", "waves", "wind")
SFX_GAIN = {"whoosh": 0.55, "boom": 0.9, "thunder": 0.8, "bell": 0.45, "shimmer": 0.35, "riser": 0.5,
            "fire": 0.35, "waves": 0.45, "wind": 0.4}
