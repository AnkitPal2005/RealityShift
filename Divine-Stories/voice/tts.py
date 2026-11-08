"""Hindi narration via edge-tts (free; hi-IN-MadhurNeural by default), one clip per scene.

- WordBoundary events give word-level timing for caption sync.
- Clips are cached by a hash of (text, voice, rate, pitch): re-running never re-requests unchanged lines.
- Leading/trailing silence is trimmed and word times are shifted to match.
Note: edge-tts uses Microsoft Edge's online read-aloud service; it needs internet but no key or account.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import subprocess
import wave
from pathlib import Path

import edge_tts
import numpy as np

from audio.synth import moving_avg
from config import settings as S
from generators.log import log


def _key(text: str) -> str:
    return hashlib.sha1(f"{text}|{S.VOICE}|{S.VOICE_RATE}|{S.VOICE_PITCH}|{PROCESS_VERSION}".encode()).hexdigest()[:12]


async def _synth(text: str, mp3: Path) -> list[dict]:
    words = []
    comm = edge_tts.Communicate(text, S.VOICE, rate=S.VOICE_RATE, pitch=S.VOICE_PITCH, boundary="WordBoundary")
    with mp3.open("wb") as f:
        async for msg in comm.stream():
            if msg["type"] == "audio":
                f.write(msg["data"])
            elif msg["type"] == "WordBoundary":
                words.append({"t": msg["offset"] / 1e7, "d": msg["duration"] / 1e7, "w": msg["text"]})
    return words


def read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path)) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        return a.reshape(-1, w.getnchannels()).mean(axis=1)


def write_wav(path: Path, a: np.ndarray, sr: int = S.SAMPLE_RATE) -> None:
    a = np.asarray(a, np.float32)
    ch = 1 if a.ndim == 1 else a.shape[1]
    with wave.open(str(path), "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


def _trim(a: np.ndarray, thresh: float = 0.01, keep: float = 0.04) -> tuple[np.ndarray, float]:
    env = moving_avg(np.abs(a), 240)
    idx = np.nonzero(env > thresh)[0]
    if not len(idx):
        raise RuntimeError("TTS clip is silent")
    k = int(keep * S.SAMPLE_RATE)
    s, e = max(0, idx[0] - k), min(len(a), idx[-1] + k * 3)
    return a[s:e], s / S.SAMPLE_RATE


MAX_GAP = 0.32   # longest pause kept inside a clip (edge-tts pauses ~0.7-1 s on "..." and "।")
PROCESS_VERSION = "v2-gapcap"


def _cap_gaps(a: np.ndarray, words: list[dict], thresh: float = 0.008) -> np.ndarray:
    """Shorten internal silences longer than MAX_GAP; shift word timings to match."""
    sr = S.SAMPLE_RATE
    env = moving_avg(np.abs(a), 480) > thresh
    cuts = []                       # (start_sample, n_removed)
    i, n = 0, len(env)
    while i < n:
        if not env[i]:
            j = i
            while j < n and not env[j]:
                j += 1
            run = j - i
            if run > MAX_GAP * sr and i > 0 and j < n:
                keep = int(MAX_GAP * sr)
                cuts.append((i + keep // 2, run - keep))
            i = j
        else:
            i += 1
    if not cuts:
        return a
    parts, prev = [], 0
    for s, k in cuts:
        parts.append(a[prev:s])
        prev = s + k
    parts.append(a[prev:])
    for w in words:
        ts = w["t"] * sr
        shift = 0
        for s, k in cuts:
            if ts >= s + k:
                shift += k
            elif ts > s:
                shift += ts - s
        w["t"] = (ts - shift) / sr
    return np.concatenate(parts)


def scene_voice(text: str, out_dir: Path, retries: int = 4) -> dict:
    """Return {"wav": path, "dur": seconds, "words": [{t, d, w}]} for one scene's narration."""
    out_dir.mkdir(parents=True, exist_ok=True)
    key = _key(text)
    wav, meta = out_dir / f"vo_{key}.wav", out_dir / f"vo_{key}.json"
    if wav.exists() and meta.exists():
        return json.loads(meta.read_text(encoding="utf-8"))
    mp3 = out_dir / f"vo_{key}.mp3"
    last = None
    for attempt in range(retries):
        try:
            words = asyncio.run(_synth(text, mp3))
            if mp3.stat().st_size < 2000:
                raise RuntimeError("empty audio from edge-tts")
            break
        except Exception as e:  # network hiccups are common; retry with backoff
            last = e
            log("voice", f"edge-tts failed ({e}); retry {attempt + 1}/{retries}")
            import time
            time.sleep(2 * (attempt + 1))
    else:
        raise RuntimeError(f"edge-tts failed: {last}")
    raw = out_dir / f"vo_{key}_raw.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp3), "-ac", "1", "-ar", str(S.SAMPLE_RATE), str(raw)],
                   check=True)
    a, shift = _trim(read_wav(raw))
    for w in words:
        w["t"] = max(0.0, w["t"] - shift)
    a = _cap_gaps(a, words)
    write_wav(wav, a)
    raw.unlink(missing_ok=True)
    for w in words:
        w["t"] = round(w["t"], 3)
        w["d"] = round(w["d"], 3)
    info = {"wav": str(wav.relative_to(S.ROOT).as_posix()), "dur": round(len(a) / S.SAMPLE_RATE, 3),
            "words": words, "text": text, "voice": S.VOICE, "rate": S.VOICE_RATE, "pitch": S.VOICE_PITCH}
    meta.write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    log("voice", f"{len(words)} words, {info['dur']:.2f}s: {text[:40]}")
    return info


def story_voice(story: dict) -> dict[str, dict]:
    out = S.story_temp(story["slug"]) / "voice"
    return {sc["id"]: scene_voice(sc["narration"], out) for sc in story["scenes"]}
