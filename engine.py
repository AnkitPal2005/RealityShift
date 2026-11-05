"""Shared engine for animated 9:16 Shorts: drawing helpers, character rig,
TTS (edge-tts / ElevenLabs), SFX + music synthesis, mixing, and the frame compositor.

Stories live in stories/<name>.py and define TOPIC, SCRIPT, SCENE_CLASSES, OUTPUTS
plus optional overrides (EL_VOICE_ID, EL_SETTINGS, CLEAN_PUNCTUATION, MAX_GAP, MUSIC_BPM,
MUSIC_DUCK, HOT_COLOR, HOT_COLORS, CAPTION_Y, CAPTION_SIZE, WATERMARK,
DELIVERY, BREATHS, ROOM, MUSIC_SEED, MUSIC_STYLE).
Every render first passes policy.check() (YouTube Partner Program reused/inauthentic content gate).
"""

import asyncio
import base64
import hashlib
import json
import math
import os
import subprocess
import wave
from pathlib import Path

import cairo
import edge_tts
import numpy as np
import requests
from moviepy import AudioFileClip, VideoClip


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "output"
SHORTS_DIR = OUT_DIR / "shorts"   # every finished Short lands here, whatever the story
WORK_DIR = OUT_DIR / "work"
SILENT_REALITY_DIR = OUT_DIR / "silent_reality"   # Silent Reality channel: no-voice 10-15s Shorts


def shorts_dir(story):
    """Finished-Short folder for a story: CHANNEL = "silent_reality" goes to its own folder."""
    return SILENT_REALITY_DIR if getattr(story, "CHANNEL", "") == "silent_reality" else SHORTS_DIR

W, H = 1080, 1920
FPS = 30
SR = 44100
VOICE = "hi-IN-MadhurNeural"   # alt: "hi-IN-SwaraNeural" (female)
RATE = "+22%"
PITCH = "+2Hz"
# ElevenLabs engine (--engine elevenlabs); key is read from ELEVENLABS_API_KEY
EL_VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam
EL_MODEL = "eleven_multilingual_v2"
EL_SETTINGS = {"stability": 0.50, "similarity_boost": 0.85, "style": 0.15}
TAIL_PAD = 0.05               # gap after each scene's (silence-trimmed) narration
MUSIC_VOLUME = 0.15
WATERMARK = "RealityShift"
TOPIC = ""                     # set from the story module
HOT_WORDS: set[str] = set()    # caption words drawn in HOT_COLOR (story module may set HOT_WORDS)
HOT_COLOR = (1.0, 0.18, 0.18)
HOT_COLORS: dict[str, tuple] = {}  # per-word override of HOT_COLOR (story module may set HOT_COLORS)
HOT_SCALE = 1.12
PUNCT = ",.;:!?…\"'"
CAPTION_FONT = "Impact"
CAPTION_Y = 1660               # vertical centre of the caption line (story module may set CAPTION_Y)
CAPTION_SIZE = 132
UI_FONT = "Segoe UI"


# Punctuation that makes the neural voice take long breaths between phrases.
PAUSE_CHARS = str.maketrans({c: " " for c in "।॥,.;:-–—…\"'"})


def clean_for_tts(chunks) -> str:
    return " ".join(" ".join(h.translate(PAUSE_CHARS).split()) for h, _ in chunks)


# ============================================================ helpers

def hexc(h: str) -> tuple[float, float, float]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def shade(c, k):
    return tuple(min(1.0, v * k) for v in c)


def rnd(i: float, salt: float = 0.0) -> float:
    """Deterministic hash noise in [0, 1)."""
    v = math.sin(i * 12.9898 + salt * 78.233) * 43758.5453
    return v - math.floor(v)


def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def lerp(a, b, u):
    return a + (b - a) * u


def ease_out_cubic(u):
    u = clamp(u)
    return 1 - (1 - u) ** 3


def ease_in_out(u):
    u = clamp(u)
    return u * u * (3 - 2 * u)


def ease_out_back(u, s=1.9):
    u = clamp(u) - 1
    return 1 + (s + 1) * u ** 3 + s * u ** 2


def bounce_out(u):
    u = clamp(u)
    n, d = 7.5625, 2.75
    if u < 1 / d:
        return n * u * u
    if u < 2 / d:
        u -= 1.5 / d
        return n * u * u + 0.75
    if u < 2.5 / d:
        u -= 2.25 / d
        return n * u * u + 0.9375
    u -= 2.625 / d
    return n * u * u + 0.984375


def rgba(ctx, c, a=1.0):
    ctx.set_source_rgba(c[0], c[1], c[2], a)


def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()


def circle(ctx, x, y, r, c, a=1.0):
    ctx.arc(x, y, r, 0, 2 * math.pi)
    rgba(ctx, c, a)
    ctx.fill()


def line(ctx, pts, c, w, a=1.0):
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    rgba(ctx, c, a)
    ctx.set_line_width(w)
    ctx.stroke()


def glow(ctx, x, y, r, c, a=0.5):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, c[0], c[1], c[2], a)
    g.add_color_stop_rgba(1, c[0], c[1], c[2], 0)
    ctx.set_source(g)
    ctx.arc(x, y, r, 0, 2 * math.pi)
    ctx.fill()


def text(ctx, s, x, y, size, c, font=UI_FONT, bold=True, a=1.0, anchor="c",
         stroke=None, stroke_w=0.0):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    if "₹" in s and font != UI_FONT:
        # Impact has no rupee glyph: lay out runs, borrowing "₹" from Segoe UI
        _, yb, _, th, _, _ = ctx.text_extents(s.replace("₹", "4"))
        runs = _rupee_runs(ctx, s, size, font, bold)
        tw = sum(adv for _, _, adv in runs)
        cx = x - tw / 2 if anchor == "c" else (x if anchor == "l" else x - tw)
        ty = y - th / 2 - yb
        for run, face, adv in runs:
            _select(ctx, face, size)
            ctx.move_to(cx, ty)
            ctx.text_path(run)
            cx += adv
    else:
        xb, yb, tw, th, _, _ = ctx.text_extents(s)
        tx = x - tw / 2 - xb if anchor == "c" else (x - xb if anchor == "l" else x - tw - xb)
        ty = y - th / 2 - yb
        ctx.move_to(tx, ty)
        ctx.text_path(s)
    if stroke is not None:
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        rgba(ctx, stroke, a)
        ctx.set_line_width(stroke_w)
        ctx.stroke_preserve()
    rgba(ctx, c, a)
    ctx.fill()
    return tw


def _select(ctx, face, size):
    font, bold = face
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)


def _rupee_runs(ctx, s, size, font, bold):
    """Split s into (run, face, advance) so '₹' renders in a font that has it."""
    runs = []
    for ch in s:
        face = (UI_FONT, True) if ch == "₹" else (font, bold)
        if runs and runs[-1][1] == face:
            runs[-1][0] += ch
        else:
            runs.append([ch, face])
    out = []
    for run, face in runs:
        _select(ctx, face, size)
        out.append((run, face, ctx.text_extents(run)[4]))
    return out


def text_width(ctx, s, size, font=UI_FONT, bold=True):
    if "₹" in s and font != UI_FONT:
        return sum(adv for _, _, adv in _rupee_runs(ctx, s, size, font, bold))
    _select(ctx, (font, bold), size)
    return ctx.text_extents(s)[2]


def backdrop(ctx, top, bottom, accent, gx, gy, t, motes=40):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *top)
    g.add_color_stop_rgb(1, *bottom)
    ctx.set_source(g)
    ctx.paint()
    glow(ctx, gx, gy, 900, accent, 0.35)
    # drifting dust motes
    for i in range(motes):
        x = (rnd(i, 1) * W + t * (12 + 25 * rnd(i, 2))) % W
        y = (rnd(i, 3) * H - t * (20 + 40 * rnd(i, 4))) % H
        circle(ctx, x, y, 1.5 + 3 * rnd(i, 5), (1, 1, 1), 0.06 + 0.1 * rnd(i, 6))


def vignette(ctx):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.3, W / 2, H / 2, H * 0.75)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.6)
    ctx.set_source(g)
    ctx.paint()


def box(ctx, x, y, w, h, c, rot=0.0, a=1.0, label=None):
    """Cardboard-style package centred at (x, y)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    rrect(ctx, -w / 2, -h / 2, w, h, 8)
    rgba(ctx, c, a)
    ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h * 0.28, 8)
    rgba(ctx, shade(c, 1.18), a)
    ctx.fill()
    ctx.rectangle(-w * 0.09, -h / 2, w * 0.18, h)
    rgba(ctx, shade(c, 0.78), a)
    ctx.fill()
    if label:
        text(ctx, label, 0, h * 0.12, h * 0.22, (1, 1, 1), a=a * 0.9)
    ctx.restore()


# ============================================================ character rig

SKIN = hexc("#C68B59")
PANTS = hexc("#22263A")


def _pt(p, a, l):
    """Point at angle a (0 = straight down, +ve = forward) and length l from p."""
    return (p[0] + l * math.sin(a), p[1] + l * math.cos(a))


def person(ctx, x, y, s, phase, shirt, mode="run", cap=None, t=0.0, flip=False):
    """Flat vector character standing on (x, y). Returns world pos of front hand."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(-s if flip else s, s)
    lean = {"run": 0.2, "carry": 0.14}.get(mode, 0.02)
    bob = -abs(math.sin(phase)) * 12 if mode in ("run", "carry") else 0
    hip = (0, -150 + bob)
    shoulder = _pt(hip, math.pi - lean, 100)
    head = _pt(shoulder, math.pi - lean, 58)

    def leg(ph):
        if mode in ("run", "carry"):
            a = 0.75 * math.sin(ph)
            return a, a - 0.2 - 1.1 * max(0.0, -math.sin(ph))
        return 0.04, 0.0

    def arm(ph, front):
        if mode == "run":
            a = -0.9 * math.sin(ph)
            return a, a + 1.3
        if mode == "carry":
            return 0.55, 1.75
        if mode == "pack":
            k = math.sin(t * 9 + (0 if front else 1.6))
            return 1.0 + 0.45 * k, 1.6 + 0.35 * k
        if mode == "wave" and front:
            return 2.6, 3.0 + 0.55 * math.sin(t * 11)
        return 0.15, 0.3

    hand = None
    for front in (False, True):
        ph = phase if front else phase + math.pi
        dim = 1.0 if front else 0.7
        a1, a2 = leg(ph)
        knee = _pt(hip, a1, 75)
        foot = _pt(knee, a2, 75)
        line(ctx, [hip, knee, foot], shade(PANTS, dim), 28)
        line(ctx, [foot, (foot[0] + 22, foot[1])], shade((0.1, 0.1, 0.1), dim), 20)
        if not front:
            u, f = arm(ph, False)
            el = _pt(shoulder, u, 58)
            hd = _pt(el, f, 55)
            line(ctx, [shoulder, el], shade(shirt, 0.7), 24)
            line(ctx, [el, hd], shade(SKIN, 0.7), 20)
            line(ctx, [hip, shoulder], shirt, 66)
            # head
            circle(ctx, head[0], head[1], 40, SKIN)
            circle(ctx, head[0] + 18, head[1] - 4, 4.5, (0.1, 0.1, 0.12))
            if cap:
                ctx.arc(head[0], head[1] - 4, 42, math.pi, 2 * math.pi)
                rgba(ctx, cap)
                ctx.fill()
                rrect(ctx, head[0] + 10, head[1] - 12, 44, 10, 5)
                ctx.fill()
            else:
                ctx.arc(head[0] - 3, head[1] - 6, 41, math.pi * 0.95, 2.05 * math.pi)
                rgba(ctx, (0.12, 0.08, 0.06))
                ctx.fill()
    u, f = arm(phase, True)
    el = _pt(shoulder, u, 58)
    hd = _pt(el, f, 55)
    line(ctx, [shoulder, el], shirt, 24)
    line(ctx, [el, hd], SKIN, 20)
    circle(ctx, hd[0], hd[1], 13, SKIN)
    hand = ctx.user_to_device(*hd)
    ctx.restore()
    return hand




# ============================================================ audio: narration

EDGE_PARALLEL = 4     # the edge-tts service answers 503 when a script fires ~25+ lines at once
EDGE_RETRIES = 4
_edge_slots: tuple | None = None   # (event loop, semaphore): a semaphore is bound to one loop


async def synth(text_: str, dest: Path, voice: str = VOICE, rate: str = RATE, pitch: str = PITCH,
                volume: str = "+0%") -> list[float]:
    """Save narration mp3 and return word start times in seconds."""
    global _edge_slots
    loop = asyncio.get_running_loop()
    if _edge_slots is None or _edge_slots[0] is not loop:
        _edge_slots = (loop, asyncio.Semaphore(EDGE_PARALLEL))
    async with _edge_slots[1]:
        for attempt in range(EDGE_RETRIES):
            try:
                starts = []
                comm = edge_tts.Communicate(text_, voice, rate=rate, pitch=pitch, volume=volume,
                                            boundary="WordBoundary")
                with dest.open("wb") as f:
                    async for msg in comm.stream():
                        if msg["type"] == "audio":
                            f.write(msg["data"])
                        elif msg["type"] == "WordBoundary":
                            starts.append(msg["offset"] / 1e7)
                return starts
            except Exception as e:
                if attempt == EDGE_RETRIES - 1:
                    raise
                print(f"      edge-tts retry {attempt + 1} for {dest.name}: {str(e)[:60]}")
                await asyncio.sleep(1.5 * 2 ** attempt)


def synth_elevenlabs(text_: str, dest: Path, voice_id: str = EL_VOICE_ID,
                     settings: dict = EL_SETTINGS) -> list[float]:
    """Save ElevenLabs narration mp3 and return word start times from its character alignment."""
    # reuse a previous render of the exact same request so re-runs don't spend credits
    cache = dest.with_suffix(".json")
    req_id = json.dumps([text_, voice_id, EL_MODEL, settings], ensure_ascii=False, sort_keys=True)
    if dest.exists() and cache.exists():
        cached = json.loads(cache.read_text(encoding="utf-8"))
        if cached.get("request") == req_id:
            return cached["starts"]
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise SystemExit("Set ELEVENLABS_API_KEY to use --engine elevenlabs")
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps",
        params={"output_format": "mp3_44100_128"},
        headers={"xi-api-key": key},
        json={"text": text_, "model_id": EL_MODEL, "voice_settings": settings},
        timeout=120,
    )
    if not r.ok:
        raise SystemExit(f"ElevenLabs error {r.status_code}: {r.text[:300]}")
    data = r.json()
    dest.write_bytes(base64.b64decode(data["audio_base64"]))
    chars = data["alignment"]["characters"]
    times = data["alignment"]["character_start_times_seconds"]
    starts = [tm for i, (ch, tm) in enumerate(zip(chars, times))
              if not ch.isspace() and (i == 0 or chars[i - 1].isspace())]
    cache.write_text(json.dumps({"request": req_id, "starts": starts}, ensure_ascii=False), encoding="utf-8")
    return starts


def decode(path: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def ffilter(x: np.ndarray, af: str) -> np.ndarray:
    """Run a mono float signal through an ffmpeg audio filter chain."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
         "-af", af, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-"],
        input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    y = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    return np.pad(y, (0, max(0, len(x) - len(y))))[:len(x)]


def trim_silence(audio: np.ndarray, thresh=0.012, keep=0.03, keep_tail=None,
                 min_keep=0.3) -> tuple[np.ndarray, float]:
    """Cut TTS lead-in/tail silence only (never inside the clip).
    Returns (trimmed, seconds removed from the start). Falls back to the untouched
    clip if nothing crosses the threshold or the result would be implausibly short."""
    keep_tail = keep if keep_tail is None else keep_tail
    loud = np.flatnonzero(np.abs(audio) > thresh)
    if not len(loud):
        print("      warning: no speech detected above threshold, keeping clip untrimmed")
        return audio, 0.0
    i0 = max(0, loud[0] - int(keep * SR))
    i1 = min(len(audio), loud[-1] + int(keep_tail * SR))
    if (i1 - i0) / SR < min(min_keep, len(audio) / SR):
        print("      warning: trim would leave a near-empty clip, keeping clip untrimmed")
        return audio, 0.0
    return audio[i0:i1], i0 / SR


def tighten_pauses(audio: np.ndarray, starts: list[float], max_gap=0.2, thresh=0.012):
    """Shorten any internal silence longer than max_gap (the neural voice breathes long
    after '?' / '!') and shift word timings to match."""
    hop = int(0.01 * SR)
    frames = np.abs(audio[:len(audio) // hop * hop]).reshape(-1, hop).max(axis=1)
    quiet = frames < thresh
    keep = np.ones(len(audio), dtype=bool)
    cuts = []  # (time in original audio, seconds removed)
    i = 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            gap = (j - i) * hop / SR
            if gap > max_gap and i > 0 and j < len(quiet):
                excess = gap - max_gap
                c0 = (i * hop) + int(max_gap / 2 * SR)
                keep[c0:c0 + int(excess * SR)] = False
                cuts.append((c0 / SR, excess))
            i = j
        else:
            i += 1
    shifted = [s - sum(ex for at, ex in cuts if at < s) for s in starts]
    return audio[keep], shifted


def align(chunks, starts, audio_len):
    """Map each caption chunk to the start time of its first Hindi word."""
    counts = [len(h.split()) for h, _ in chunks]
    total = sum(counts)
    if not starts:
        starts = [audio_len * i / total for i in range(total)]
    if len(starts) != total:
        print(f"      note: {len(starts)} word boundaries vs {total} tokens, scaling alignment")
    out, cum = [], 0
    for (_, cap), c in zip(chunks, counts):
        idx = min(len(starts) - 1, round(cum * len(starts) / total))
        out.append((starts[idx], cap))
        cum += c
    return out


# ============================================================ audio: performed narration
# A story may set DELIVERY = {scene_key: [(tone, line), ...]} to have edge-tts read a scene the
# way a narrator performs it: each line is synthesised with its own rate/pitch/volume, joined by
# a pause sized from its closing punctuation, with a soft inhale in the longer pauses. A line may
# also be (tone, line, pause_seconds), and a tone may be a literal (rate, pitch, volume) tuple.

TONES = {
    "tell":  ("+16%", "+0Hz", "+0%"),    # plain storytelling
    "hook":  ("+20%", "+5Hz", "+10%"),   # opening line, leaning in
    "ask":   ("+14%", "+4Hz", "+0%"),    # a question left hanging
    "low":   ("+12%", "-6Hz", "-5%"),    # serious, setting up the villain
    "sly":   ("+10%", "+8Hz", "-5%"),    # mocking, drawn out
    "build": ("+20%", "+2Hz", "+5%"),    # tension rising, quicker
    "punch": ("+10%", "+8Hz", "+20%"),    # the payoff, slow and loud
    "cta":   ("+16%", "+3Hz", "+8%"),    # warm, direct ask
}
LINE_PAUSE = {"?": 0.24, "!": 0.2, "।": 0.18, ".": 0.18, "…": 0.3, ",": 0.06}
BREATH_MIN_PAUSE = 0.2


def line_pause(line: str) -> float:
    end = line.rstrip("'\" ").rstrip("?!")
    if end.endswith(("...", "…")):
        return LINE_PAUSE["…"]
    return LINE_PAUSE.get(line.rstrip("'\" ")[-1:], 0.08)


def delivery_lines(spec) -> list[tuple[str, str, str, str, float]]:
    """[(tone, line[, pause])] -> [(line, rate, pitch, volume, pause_after)]."""
    out = []
    for tone, line_, *pause in spec:
        rate, pitch, volume = TONES[tone] if isinstance(tone, str) else tone
        out.append((line_, rate, pitch, volume, pause[0] if pause else line_pause(line_)))
    return out


def breath(dur: float, seed: int = 0) -> np.ndarray:
    """A quiet inhale: band-limited noise that swells and eases off (peak 1.0)."""
    n = int(dur * SR)
    u = np.arange(n) / n
    x = _noise(n, seed)
    x = _lowpass(x, 2400) - _lowpass(x, 450)
    x *= np.sin(np.pi * u ** 0.6) ** 2
    return x / (np.max(np.abs(x)) + 1e-9)


def perform(lines, clips, trim_kw, max_gap, breaths=True, seed=0):
    """Join separately synthesised lines into one take; returns (audio, word starts)."""
    kw = {**trim_kw, "keep": 0.03, "keep_tail": 0.07}
    parts, starts, t = [], [], 0.0
    fade = int(0.006 * SR)
    for i, ((_, _, _, _, pause), (mp3, st)) in enumerate(zip(lines, clips)):
        a, lead = trim_silence(decode(mp3), **kw)
        st = [max(0.0, s - lead) for s in st]
        if max_gap is not None:
            a, st = tighten_pauses(a, st, max_gap=max_gap)
        a = a.copy()
        a[:fade] *= np.linspace(0, 1, fade)
        a[-fade:] *= np.linspace(1, 0, fade)
        parts.append(a)
        starts += [t + s for s in st]
        t += len(a) / SR
        if i < len(lines) - 1:
            gap = np.zeros(int(pause * SR))
            if breaths and pause >= BREATH_MIN_PAUSE:
                b = breath(min(0.26, pause - 0.03), seed * 31 + i)
                at = len(gap) - len(b) - int(0.02 * SR)
                gap[at:at + len(b)] += 0.03 * np.max(np.abs(a)) * b
            parts.append(gap)
            t += pause
    return np.concatenate(parts), starts


def room(x: np.ndarray, wet: float) -> np.ndarray:
    """Small-room early reflections so the voice sits in a space instead of dead air."""
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    ir = _lowpass(_noise(n, 7) * np.exp(-t / 0.06), 3800)
    ir[:int(0.004 * SR)] = 0                       # predelay: reflections arrive after the dry voice
    ir /= np.sqrt(np.sum(ir ** 2))
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    rev = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[:len(x)]
    return x + wet * rev


# ============================================================ audio: SFX synthesis

def _env(n, attack=0.005, decay=10.0):
    t = np.arange(n) / SR
    return np.minimum(1, t / attack) * np.exp(-t * decay)


def _noise(n, seed=0):
    return np.random.default_rng(seed).uniform(-1, 1, n)


def _lowpass(x, cutoff):
    """One-pole lowpass with per-sample (array) or fixed cutoff in Hz."""
    cutoff = np.broadcast_to(cutoff, x.shape)
    alpha = 1 - np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += alpha[i] * (x[i] - acc)
        y[i] = acc
    return y


def sfx_bank() -> dict[str, np.ndarray]:
    def tone(freq, dur, decay, harmonics=((1, 1.0),)):
        n = int(dur * SR)
        t = np.arange(n) / SR
        return sum(a * np.sin(2 * np.pi * freq * h * t) for h, a in harmonics) * _env(n, 0.003, decay)

    bank = {}
    n = int(0.05 * SR)
    bank["tick"] = 0.6 * _noise(n, 1) * _env(n, 0.0005, 260) + tone(3200, 0.05, 160)
    bank["tock"] = 0.6 * _noise(n, 2) * _env(n, 0.0005, 260) + tone(2300, 0.05, 160)
    # alarm: rapid bell hammering
    n = int(0.7 * SR)
    t = np.arange(n) / SR
    bank["alarm"] = (np.sin(2 * np.pi * 2600 * t) + 0.5 * np.sin(2 * np.pi * 3900 * t)) \
        * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 22 * t))) * np.exp(-t * 3)
    bank["beep"] = tone(1850, 0.11, 8, ((1, 1.0), (2, 0.25)))
    n = int(0.08 * SR)
    t = np.arange(n) / SR
    bank["pick"] = np.sin(2 * np.pi * (900 - 3000 * t) * t) * _env(n, 0.002, 40)
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    thud = np.sin(2 * np.pi * np.cumsum(160 - 300 * t) / SR) * _env(n, 0.002, 14)
    thud += 0.3 * _lowpass(_noise(n, 3), 900) * _env(n, 0.001, 30)
    bank["thud"] = thud
    bank["soft_thud"] = 0.45 * thud
    # whoosh: noise through a sweeping lowpass with a swell envelope
    n = int(0.55 * SR)
    u = np.arange(n) / n
    bank["whoosh"] = 2.2 * _lowpass(_noise(n, 4), 300 + 4500 * np.sin(np.pi * u)) * np.sin(np.pi * u) ** 2
    # doorbell ding-dong
    ding = lambda f: tone(f, 1.3, 2.6, ((1, 1.0), (2, 0.35), (3, 0.15), (4.2, 0.08)))
    dd = np.zeros(int(1.9 * SR))
    a, b = ding(659.25), ding(523.25)
    dd[:len(a)] += a
    dd[int(0.45 * SR):int(0.45 * SR) + len(b)] += b
    bank["dingdong"] = dd
    # cash register: mechanical clack + bright bell "ka-ching"
    clack = 0.8 * _lowpass(_noise(int(0.06 * SR), 8), 2500) * _env(int(0.06 * SR), 0.001, 60)
    bell = tone(2093, 0.9, 4.5, ((1, 1.0), (2.76, 0.4), (5.4, 0.2))) + 0.6 * tone(2637, 0.9, 5, ((1, 1.0),))
    kc = np.zeros(int(1.0 * SR))
    kc[:len(clack)] += clack
    kc[int(0.08 * SR):int(0.08 * SR) + len(bell)] += bell[:len(kc) - int(0.08 * SR)]
    bank["kaching"] = kc
    # laser zap: fast downward chirp
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    bank["zap"] = np.sign(np.sin(2 * np.pi * np.cumsum(2400 * np.exp(-t * 14) + 200) / SR)) * _env(n, 0.002, 12)
    # popcorn pop: tiny filtered click
    n = int(0.04 * SR)
    bank["pop"] = _lowpass(_noise(n, 9), 3500) * _env(n, 0.0005, 120) + tone(700, 0.04, 90)
    # boom: sub drop + noise burst for big reveals
    n = int(1.0 * SR)
    t = np.arange(n) / SR
    bank["boom"] = np.sin(2 * np.pi * np.cumsum(30 + 90 * np.exp(-t * 6)) / SR) * _env(n, 0.003, 3.5)         + 0.5 * _lowpass(_noise(n, 10), 600) * _env(n, 0.002, 8)
    for k, v in bank.items():
        bank[k] = v / (np.max(np.abs(v)) + 1e-9)
    return bank


def engine_sound(dur: float) -> np.ndarray:
    """Scooter engine: sawtooth stack with rev-up, firing-rate AM, and rumble."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    freq = 48 + 40 * np.minimum(1, t / 0.9) + 6 * np.sin(2 * np.pi * 0.6 * t) + 10 * np.exp(-((t - 0.5) ** 2) * 20)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    saw = sum(np.sin(k * phase) / k for k in range(1, 9))
    am = 0.65 + 0.35 * np.sin(phase * 0.5)
    rumble = _lowpass(_noise(n, 5), 220) * 3
    fade = np.minimum(1, t / 0.15) * np.minimum(1, (dur - t) / 0.4)
    out = (0.6 * saw * am + rumble) * fade
    return out / (np.max(np.abs(out)) + 1e-9)


def tension_music(dur: float, bpm: float = 100, seed: int = 0) -> np.ndarray:
    """Dark documentary bed: drone + heartbeat kick + minor arpeggio (Am-F-Dm-E) + ticking hats.
    seed (one per story) picks the key, chord order, arpeggio and groove, so no two Shorts share a bed."""
    rng = np.random.default_rng(seed)
    key = 2 ** (int(rng.integers(-4, 6)) / 12)          # transpose -4..+5 semitones
    order = rng.permutation(4) if seed else np.arange(4)
    pattern = tuple(rng.permutation([0, 1, 2, 3, 2, 1, 2, 3])) if seed else (0, 1, 2, 3, 2, 1, 2, 3)
    kick_every = int(rng.choice([2, 2, 4])) if seed else 2
    n = int(dur * SR)
    t = np.arange(n) / SR
    beat = 60 / bpm
    out = np.zeros(n + 2 * SR)

    def place(sig, at, gain=1.0):
        i0 = int(at * SR)
        if i0 < n:
            out[i0:i0 + len(sig)] += gain * sig[:len(out) - i0]

    drone = (np.sin(2 * np.pi * 55 * key * t) + 0.6 * np.sin(2 * np.pi * 82.41 * key * t + 0.4 * np.sin(2 * np.pi * 0.1 * t))
             + 0.25 * np.sin(2 * np.pi * 110.4 * key * t)) * (0.7 + 0.3 * np.sin(2 * np.pi * t / (beat * 8)))
    out[:n] += 0.3 * drone

    tk = np.arange(int(0.3 * SR)) / SR
    kick = np.sin(2 * np.pi * np.cumsum(40 + 60 * np.exp(-tk * 25)) / SR) * np.exp(-tk * 13)
    tp = np.arange(int(0.4 * SR)) / SR
    hat = np.diff(_noise(int(0.05 * SR) + 1, 7)) * np.exp(-np.arange(int(0.05 * SR)) / SR * 90)
    chords = [(220.0, 261.63, 329.63, 440.0), (174.61, 220.0, 261.63, 349.23),
              (146.83, 174.61, 220.0, 293.66), (164.81, 207.65, 246.94, 329.63)]
    chords = [tuple(f * key for f in chords[i]) for i in order]
    for b in range(int(dur / beat) + 1):
        at = b * beat
        if b % kick_every == 0:  # lub-dub heartbeat
            place(kick, at, 0.9)
            place(kick, at + 0.17, 0.55)
        for h in range(4):
            place(hat, at + h * beat / 4, 0.25 if h == 2 else 0.1)
        chord = chords[(b // 4) % 4]
        for s in range(2):
            f = chord[pattern[(b * 2 + s) % 8]]
            place((np.sin(2 * np.pi * f * tp) + 0.3 * np.sin(4 * np.pi * f * tp)) * np.exp(-tp * 9),
                  at + s * beat / 2, 0.32)
    out = out[:n] * np.minimum(1, t / 1.0) * np.minimum(1, (dur - t) / 1.5)
    return out / (np.max(np.abs(out)) + 1e-9)


def _soft_lowpass(x: np.ndarray, cutoff: float) -> np.ndarray:
    """Gentle 4th-order-ish lowpass done in the frequency domain (fast on long beds)."""
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(np.fft.rfft(x) / (1 + (f / cutoff) ** 4), len(x))


def _saw(freq, t, n=8):
    return sum(np.sin(2 * np.pi * freq * k * t) / k for k in range(1, n + 1))


def _bed(dur, bpm, seed):
    """Shared set-up for the beds below: rng, transpose factor, beat length, output buffer and a placer."""
    rng = np.random.default_rng(seed)
    key = 2 ** (int(rng.integers(-4, 6)) / 12)
    n = int(dur * SR)
    out = np.zeros(n + 3 * SR)

    def place(sig, at, gain=1.0):
        i0 = int(at * SR)
        if 0 <= i0 < n:
            out[i0:i0 + len(sig)] += gain * sig[:len(out) - i0]

    return rng, key, n, 60 / bpm, out, place


def _finish(out, n, dur):
    t = np.arange(n) / SR
    out = out[:n]
    out = np.tanh(0.16 / (np.sqrt(np.mean(out ** 2)) + 1e-9) * out)  # match tension_music's loudness, soft-clip peaks
    out *= np.minimum(1, t / 1.0) * np.minimum(1, (dur - t) / 1.5)
    return out / (np.max(np.abs(out)) + 1e-9)


# minor-key progressions as semitone offsets from the root (i-VI-III-VII, i-iv-VI-v, i-VII-VI-VII)
PROGRESSIONS = ((0, 8, 3, 10), (0, 5, 8, 7), (0, 10, 8, 10))


def pulse_music(dur: float, bpm: float = 110, seed: int = 0) -> np.ndarray:
    """Driving explainer bed: eighth-note saw bass ostinato, soft pad chords, claps on 2 and 4, offbeat hats."""
    rng, key, n, beat, out, place = _bed(dur, bpm, seed)
    prog = PROGRESSIONS[int(rng.integers(len(PROGRESSIONS)))]
    root = 55.0 * key
    tn = np.arange(int(beat / 2 * SR)) / SR
    tp = np.arange(int(beat * 4 * SR)) / SR
    tc = np.arange(int(0.12 * SR)) / SR
    clap = _soft_lowpass(_noise(len(tc), seed + 1), 3000) * np.exp(-tc * 30)
    hat = np.diff(_noise(int(0.04 * SR) + 1, seed + 2)) * np.exp(-np.arange(int(0.04 * SR)) / SR * 120)
    accent = rng.permutation([1.0, 0.6, 0.8, 0.6, 1.0, 0.6, 0.8, 0.9])
    for bar in range(int(dur / (beat * 4)) + 1):
        f0 = root * 2 ** (prog[bar % 4] / 12)
        at = bar * beat * 4
        pad = sum(np.sin(2 * np.pi * f0 * 2 * 2 ** (s / 12) * tp) + 0.5 * np.sin(2 * np.pi * f0 * 2 * 2 ** (s / 12) * 1.003 * tp)
                  for s in (0, 3, 7))
        place(pad * np.minimum(1, tp / 0.6) * np.minimum(1, (tp[-1] - tp) / 0.4), at, 0.08)
        for k in range(8):
            f = f0 * (2 if k % 4 == 3 else 1)
            place(_saw(f, tn, 6) * np.exp(-tn * 7), at + k * beat / 2, 0.22 * accent[k])
            place(hat, at + k * beat / 2 + beat / 4, 0.12)
        for b in (1, 3):
            place(clap, at + b * beat, 0.5)
    return _finish(_soft_lowpass(out, 5000), n, dur)


def ambient_music(dur: float, bpm: float = 80, seed: int = 0) -> np.ndarray:
    """Slow documentary bed: evolving detuned pads, sub swells and sparse bell plucks, no drums."""
    rng, key, n, beat, out, place = _bed(dur, bpm, seed)
    prog = PROGRESSIONS[int(rng.integers(len(PROGRESSIONS)))]
    root = 110.0 * key
    span = beat * 8
    tp = np.arange(int((span + 1.5) * SR)) / SR
    tb = np.arange(int(1.6 * SR)) / SR
    for k in range(int(dur / span) + 1):
        f0 = root * 2 ** (prog[k % 4] / 12)
        env = np.minimum(1, tp / 1.5) * np.minimum(1, np.maximum(0, (tp[-1] - tp)) / 1.5)
        pad = sum(_saw(f0 * 2 ** (s / 12) * d, tp, 5) for s in (0, 3, 7, 12) for d in (0.997, 1.003))
        place(_soft_lowpass(pad, 900) * env * (0.8 + 0.2 * np.sin(2 * np.pi * 0.25 * tp)), k * span, 0.05)
        place(np.sin(2 * np.pi * f0 / 2 * tp) * env, k * span, 0.25)
        for _ in range(int(rng.integers(2, 5))):  # bells on random eighth notes
            f = f0 * 4 * 2 ** (int(rng.choice([0, 3, 7, 10, 12])) / 12)
            bell = (np.sin(2 * np.pi * f * tb) + 0.4 * np.sin(2 * np.pi * f * 2.76 * tb)) * np.exp(-tb * 3.5)
            place(bell, k * span + int(rng.integers(0, 16)) * beat / 2, 0.12)
    return _finish(out, n, dur)


def march_music(dur: float, bpm: float = 96, seed: int = 0) -> np.ndarray:
    """Military bed: snare cadence with rolls, bass drum on 1 and 3, low brass motif, timpani on phrase starts."""
    rng, key, n, beat, out, place = _bed(dur, bpm, seed)
    root = 73.42 * key                                                     # D2, transposed
    ts = np.arange(int(0.18 * SR)) / SR
    snare = 0.7 * _soft_lowpass(_noise(len(ts), seed + 3), 6000) * np.exp(-ts * 22) \
        + 0.5 * np.sin(2 * np.pi * 190 * ts) * np.exp(-ts * 30)
    tk = np.arange(int(0.35 * SR)) / SR
    kick = np.sin(2 * np.pi * np.cumsum(45 + 70 * np.exp(-tk * 20)) / SR) * np.exp(-tk * 9)
    tt = np.arange(int(1.2 * SR)) / SR
    timp = np.sin(2 * np.pi * root * tt) * np.exp(-tt * 3) + 0.3 * np.sin(2 * np.pi * root * 1.5 * tt) * np.exp(-tt * 4)
    cadence = [(0, 1.0), (2, 0.5), (3, 0.6), (4, 0.9), (6, 0.5), (7, 0.6)]  # sixteenth-note slots in a half bar
    motif = [(0, 2), (7, 1), (5, 1)] if rng.random() < 0.5 else [(0, 2), (3, 1), (7, 1)]
    for bar in range(int(dur / (beat * 4)) + 1):
        at = bar * beat * 4
        for half in (0, 2):
            for slot, g in cadence:
                place(snare, at + half * beat + slot * beat / 4, 0.28 * g)
        if bar % 4 == 3:  # roll into the next phrase
            for k in range(8):
                place(snare, at + 3 * beat + k * beat / 8, 0.12 + 0.04 * k)
        for b in (0, 2):
            place(kick, at + b * beat, 0.8)
        if bar % 4 == 0:
            place(timp, at, 0.6)
        if bar % 2 == 0:
            pos = at
            for semi, beats in motif:
                tn = np.arange(int(beats * beat * SR)) / SR
                note = _saw(root * 2 * 2 ** (semi / 12), tn, 10)
                place(_soft_lowpass(note, 1200) * np.minimum(1, tn / 0.05) * np.exp(-tn * 1.2), pos, 0.1)
                pos += beats * beat
    return _finish(out, n, dur)


MUSIC_STYLES = {"tension": tension_music, "pulse": pulse_music, "ambient": ambient_music, "march": march_music}


def moving_avg(x: np.ndarray, win: int) -> np.ndarray:
    c = np.cumsum(np.concatenate([[0.0], x]))
    y = (c[win:] - c[:-win]) / win
    return np.concatenate([np.full(win // 2, y[0]), y, np.full(len(x) - len(y) - win // 2, y[-1])])


SFX_GAIN = {"tick": 0.07, "tock": 0.07, "alarm": 0.16, "beep": 0.16, "pick": 0.14, "thud": 0.4,
            "soft_thud": 0.4, "whoosh": 0.32, "dingdong": 0.34, "engine": 0.13,
            "kaching": 0.3, "zap": 0.1, "pop": 0.12, "boom": 0.45}


def write_wav(path: Path, mono: np.ndarray) -> None:
    pcm = (np.clip(mono, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


# ============================================================ compositor

def draw_overlay(ctx, scene_idx, t_local, dur, captions):
    margin = 70
    accent = SCENES[scene_idx]["obj"].accent
    text(ctx, TOPIC, margin, 140, 30, (1, 1, 1), a=0.65, anchor="l")
    # watermark badge
    tw = text_width(ctx, WATERMARK, 36)
    bx1, by0 = W - margin, 100
    bx0 = bx1 - tw - 80
    rrect(ctx, bx0, by0, bx1 - bx0, 72, 36)
    rgba(ctx, (0, 0, 0), 0.6)
    ctx.fill_preserve()
    rgba(ctx, accent)
    ctx.set_line_width(3)
    ctx.stroke()
    circle(ctx, bx0 + 30, by0 + 36, 8 + 2 * math.sin(t_local * 6), accent)
    text(ctx, WATERMARK, bx0 + 50, by0 + 36, 36, (1, 1, 1), anchor="l")

    # kinetic caption: one chunk at a time, popping in with overshoot
    cur = None
    for i, (start, cap) in enumerate(captions):
        if t_local >= start - 0.04:
            cur = i
    if cur is None:
        return
    start, cap = captions[cur]
    u = t_local - start + 0.04
    pop = ease_out_back(u / 0.22)
    emph = cap.endswith(("!", "?"))
    color = hexc("#FFD60A") if emph else (1, 1, 1)
    size = CAPTION_SIZE
    # laid out word by word so HOT_WORDS can pop in red, slightly larger, with a gold glow
    words = [(w, w.strip(PUNCT) in HOT_WORDS) for w in cap.split(" ")]
    ws = [text_width(ctx, w, size, font=CAPTION_FONT, bold=False) * (HOT_SCALE if hot else 1) for w, hot in words]
    gap = size * 0.25
    tw = sum(ws) + gap * (len(ws) - 1)
    fit = min(1.0, 940 / tw)
    ctx.save()
    ctx.translate(W / 2, CAPTION_Y)
    ctx.rotate((0.035 if cur % 2 else -0.035) * (2 - pop))
    ctx.scale(pop * fit, pop * fit)
    x = -tw / 2
    for (w, hot), ww in zip(words, ws):
        ctx.save()
        ctx.translate(x + ww / 2, 0)
        hc = HOT_COLORS.get(w.strip(PUNCT), HOT_COLOR)
        if hot:
            slam = HOT_SCALE * (1 + 0.35 * (1 - ease_out_back(u / 0.3))) * (1 + 0.04 * math.sin(t_local * 14))
            ctx.scale(slam, slam)
            glow(ctx, 0, 0, size * 1.1, hc if HOT_COLORS else hexc("#FFD60A"), 0.55)
        text(ctx, w, 0, 10, size, (0, 0, 0), font=CAPTION_FONT, bold=False, a=0.45)
        text(ctx, w, 0, 0, size, hc if hot else color, font=CAPTION_FONT, bold=False,
             stroke=(0, 0, 0), stroke_w=18)
        ctx.restore()
        x += ww + gap
    ctx.restore()


SCENES: list[dict] = []


def make_frame(t: float) -> np.ndarray:
    idx = 0
    for i, sc in enumerate(SCENES):
        if t >= sc["start"]:
            idx = i
    sc = SCENES[idx]
    tl = t - sc["start"]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)

    # camera: punch-in on scene entry, then slow continuous push
    intro = ease_out_cubic(tl / 0.35)
    zoom = lerp(1.22, 1.0, intro) + 0.035 * (tl / sc["dur"])
    ctx.save()
    ctx.translate(W / 2, H * 0.45)
    ctx.scale(zoom, zoom)
    ctx.rotate(lerp(0.05 if idx % 2 else -0.05, 0, intro))
    ctx.translate(-W / 2, -H * 0.45)
    sc["obj"].draw(ctx, tl, sc["dur"])
    ctx.restore()
    vignette(ctx)
    draw_overlay(ctx, idx, tl, sc["dur"], sc["captions"])
    if tl < 0.25:  # flash transition
        rgba(ctx, (1, 1, 1), 0.55 * (1 - tl / 0.25))
        ctx.paint()

    surf.flush()
    buf = np.ndarray((H, W, 4), dtype=np.uint8, buffer=surf.get_data())
    return buf[:, :, 2::-1].copy()


def render(story, engine: str) -> Path:
    """Render a story module (see stories/) with the given TTS engine ("edge" or "elevenlabs")."""
    global TOPIC, HOT_WORDS, HOT_COLOR, HOT_COLORS, CAPTION_Y, CAPTION_SIZE, WATERMARK
    TOPIC = story.TOPIC
    WATERMARK = getattr(story, "WATERMARK", WATERMARK)
    HOT_WORDS = {w.upper() for w in getattr(story, "HOT_WORDS", ())}
    HOT_COLOR = getattr(story, "HOT_COLOR", HOT_COLOR)
    HOT_COLORS = {w.upper(): c for w, c in getattr(story, "HOT_COLORS", {}).items()}
    CAPTION_Y = getattr(story, "CAPTION_Y", CAPTION_Y)
    CAPTION_SIZE = getattr(story, "CAPTION_SIZE", CAPTION_SIZE)
    script, scene_classes = story.SCRIPT, story.SCENE_CLASSES
    clean = getattr(story, "CLEAN_PUNCTUATION", True)
    max_gap = getattr(story, "MAX_GAP", 0.2)          # None = keep internal pauses as spoken
    tail_pad = getattr(story, "TAIL_PAD", TAIL_PAD)
    trim_kw = getattr(story, "TRIM", {})               # trim_silence() overrides
    text_for = (lambda chunks: clean_for_tts(chunks)) if clean else \
        (lambda chunks: " ".join(h for h, _ in chunks))

    name = story.__name__.split(".")[-1]
    import policy   # YPP gate: refuses reused/repetitive Shorts before any TTS is spent
    policy.check(story, name)
    work = WORK_DIR / name / engine
    final = shorts_dir(story) / story.OUTPUTS[engine]   # per-channel folder
    work.mkdir(parents=True, exist_ok=True)
    final.parent.mkdir(parents=True, exist_ok=True)
    mp3s = [work / f"scene_{i + 1:02d}.mp3" for i in range(len(script))]
    delivery = {k: delivery_lines(v) for k, v in getattr(story, "DELIVERY", {}).items()} if engine == "edge" else {}

    if engine == "elevenlabs":
        voice_id = getattr(story, "EL_VOICE_ID", EL_VOICE_ID)
        settings = getattr(story, "EL_SETTINGS", EL_SETTINGS)
        print(f"[1/4] Generating narration + word timings with ElevenLabs ({EL_MODEL}, voice {voice_id}, {settings})...")
        word_starts = [synth_elevenlabs(text_for(chunks), p, voice_id, settings)
                       for (_, chunks), p in zip(script, mp3s)]
    else:
        voice = getattr(story, "EDGE_VOICE", VOICE)
        rate, pitch = getattr(story, "EDGE_RATE", RATE), getattr(story, "EDGE_PITCH", PITCH)
        how = f"performed delivery on {len(delivery)} scenes" if delivery else f"rate {rate}, pitch {pitch}"
        print(f"[1/4] Generating narration + word timings with {voice} ({how})...")

        async def scene(key, chunks, p):
            if key not in delivery:
                return await synth(text_for(chunks), p, voice, rate, pitch)
            lines = delivery[key]
            paths = [p.with_name(f"{p.stem}_l{j:02d}.mp3") for j in range(len(lines))]
            return list(zip(paths, await asyncio.gather(*(synth(ln[0], lp, voice, *ln[1:4])
                                                           for ln, lp in zip(lines, paths)))))

        async def run_all():
            return await asyncio.gather(*(scene(key, chunks, p) for (key, chunks), p in zip(script, mp3s)))

        word_starts = asyncio.run(run_all())

    SCENES.clear()
    t = 0.0
    voice_tracks = []
    diag = []
    breaths = getattr(story, "BREATHS", True)
    for i, ((key, chunks), starts) in enumerate(zip(script, word_starts)):
        if key in delivery:   # starts holds (line mp3, line word starts) pairs
            audio, starts = perform(delivery[key], starts, trim_kw, max_gap, breaths, seed=i)
            raw, lead = audio, 0.0
        else:
            raw = decode(mp3s[i])
            audio, lead = trim_silence(raw, **trim_kw)
            starts = [max(0.0, s - lead) for s in starts]
            if max_gap is not None:
                audio, starts = tighten_pauses(audio, starts, max_gap=max_gap)
        dur = max(len(audio) / SR, 1 / FPS) + tail_pad  # audio-first: the clip sets the scene length
        SCENES.append({"key": key, "obj": scene_classes[key](), "start": t, "dur": dur,
                       "captions": align(chunks, starts, len(audio) / SR)})
        voice_tracks.append((t, audio))
        diag.append((key, len(raw) / SR, lead, len(raw) / SR - lead - len(audio) / SR, len(audio) / SR, dur))
        t += dur
    total = t
    print("      scene        raw   -lead  -tail   audio   scene")
    for i, (key, raw_d, lead, tail, aud, dur) in enumerate(diag):
        print(f"      Scene {i + 1}: {raw_d:5.2f}s  {lead:4.2f}s  {tail:4.2f}s  {aud:5.2f}s  {dur:5.2f}s  ({key})")
    print(f"      Total narration: {sum(d[4] for d in diag):.2f}s   video: {total:.2f}s")

    print("[2/4] Mixing voice + music + SFX...")
    bank = sfx_bank()
    voice = np.zeros(int(total * SR) + SR)
    for start, audio in voice_tracks:
        i0 = int(start * SR)
        voice[i0:i0 + len(audio)] += audio
    # voice chain: rumble cut, presence lift, firm compression, peak normalise
    voice = ffilter(voice, "highpass=f=90,equalizer=f=3000:t=q:w=1.2:g=3,"
                           "acompressor=threshold=0.08:ratio=4:attack=4:release=70:makeup=2")
    if getattr(story, "ROOM", 0):
        voice = room(voice, story.ROOM)
    voice *= 0.9 / (np.max(np.abs(voice)) + 1e-9)
    # music ducks ~6 dB whenever the narrator is speaking (MUSIC_DUCK = 0 keeps it at a flat MUSIC_VOLUME)
    env = moving_avg(np.abs(voice), int(0.05 * SR))
    duck_amt = getattr(story, "MUSIC_DUCK", 0.5)
    duck = moving_avg(1 - duck_amt * np.clip(env / 0.04, 0, 1), int(0.15 * SR))
    music = MUSIC_STYLES[getattr(story, "MUSIC_STYLE", "tension")](
        len(voice) / SR, bpm=getattr(story, "MUSIC_BPM", 100),
        seed=getattr(story, "MUSIC_SEED", int(hashlib.md5(name.encode()).hexdigest()[:8], 16)))
    music = np.pad(music, (0, max(0, len(voice) - len(music))))[:len(voice)]
    mix = voice + MUSIC_VOLUME * music * duck
    events = [(max(0.0, s["start"] - 0.2), "whoosh") for s in SCENES[1:]]
    for s in SCENES:
        events += [(s["start"] + ev[0],) + tuple(ev[1:]) for ev in s["obj"].events(s["dur"])]
    for et, name, *extra in events:
        # an optional third element is the clip length for continuous sounds (engine)
        src = engine_sound(extra[0]) if name == "engine" else bank[name]
        clip = src * SFX_GAIN[name]
        i0 = int(et * SR)
        end = min(len(mix), i0 + len(clip))
        mix[i0:end] += clip[:end - i0]
    mix = mix[:int(total * SR)]
    # master bus: glue compression + loudness normalisation to the -14 LUFS streaming target
    mix = ffilter(mix, "acompressor=threshold=0.3:ratio=2.5:attack=5:release=120,"
                       "loudnorm=I=-14:TP=-1.5:LRA=9")
    mix = np.clip(mix, -0.99, 0.99)
    master = work / "master_audio.wav"
    write_wav(master, mix)
    print(f"      {len(events)} SFX events mixed")

    print(f"[3/4] Rendering {int(total * FPS)} animated frames...")
    video = VideoClip(make_frame, duration=total).with_audio(AudioFileClip(str(master)))

    print(f"[4/4] Encoding {final.relative_to(ROOT)}...")
    video.write_videofile(
        str(final), fps=FPS, codec="libx264", audio_codec="aac", audio_bitrate="192k",
        preset="medium", threads=8, ffmpeg_params=["-pix_fmt", "yuv420p", "-crf", "19"],
        temp_audiofile_path=str(work), logger="bar",
    )
    print(f"Done: {final}  ({total:.1f}s)")
    return final
