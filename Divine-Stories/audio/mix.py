"""Timeline + final audio mix: voice clips at scene starts, music bed with voice-driven ducking, SFX on cues,
then FFmpeg loudnorm to the platform loudness target."""

from __future__ import annotations

import subprocess
import zlib
from pathlib import Path

import numpy as np

from audio import synth
from config import settings as S
from voice.tts import read_wav, write_wav

SR = S.SAMPLE_RATE
LEAD_IN = 0.25       # silence before the first word
TAIL = 1.3           # music tail after the last word


def build_timeline(story: dict, voice: dict[str, dict]) -> list[dict]:
    """Scene start/duration on the global clock, word times made global, cues resolved."""
    t = LEAD_IN
    out = []
    for i, sc in enumerate(story["scenes"]):
        v = voice[sc["id"]]
        dur = v["dur"] + sc.get("pause_after", 0.35)
        if i == 0:
            dur += LEAD_IN
        if i == len(story["scenes"]) - 1:
            dur += TAIL
        start = 0.0 if i == 0 else t
        vo_start = LEAD_IN if i == 0 else t
        words = [{**w, "t": round(vo_start + w["t"], 3)} for w in v["words"]]
        out.append({"id": sc["id"], "beat": sc["beat"], "start": round(start, 3), "dur": round(dur, 3),
                    "vo_start": round(vo_start, 3), "vo_dur": v["dur"], "wav": v["wav"], "words": words})
        t = start + dur if i else dur
    return out


def resolve_cue(cue, scene_tl: dict) -> float:
    """'word:<text>' -> global time of the first matching word in the scene; number -> scene-relative seconds."""
    if isinstance(cue, (int, float)):
        return scene_tl["start"] + float(cue)
    if isinstance(cue, str) and cue.startswith("word:"):
        target = cue[5:]
        for w in scene_tl["words"]:
            if w["w"].strip("।,.?!…") == target:
                return w["t"]
        raise ValueError(f"cue {cue} not found in scene {scene_tl['id']}")
    raise ValueError(f"bad cue {cue!r}")


def mix(story: dict, timeline: list[dict], out_wav: Path) -> dict:
    total = timeline[-1]["start"] + timeline[-1]["dur"]
    n = int(total * SR) + SR
    voice = np.zeros(n)
    for tl in timeline:
        a = read_wav(S.ROOT / tl["wav"])
        s = int(tl["vo_start"] * SR)
        voice[s:s + len(a)] += a
    music = synth.score(timeline, n / SR)
    # ducking: smoothed voice envelope (fast attack, slow release)
    env = np.abs(voice)
    k = int(0.12 * SR)
    env = synth.moving_avg(env, k)
    env = np.clip(env / (env.max() + 1e-9) * 4, 0, 1)
    rel = int(0.35 * SR)
    env = np.maximum(env, synth.moving_avg(env, rel))
    duck = 10 ** ((S.MUSIC_GAIN_DB + S.DUCK_DB * env) / 20)
    sfx = np.zeros((n, 2))
    placed = []
    by_id = {tl["id"]: tl for tl in timeline}
    for sc in story["scenes"]:
        for j, cue in enumerate(sc.get("sfx", [])):
            t = resolve_cue(cue["at"], by_id[sc["id"]])
            clip = synth.sfx(cue["type"], seed=zlib.crc32(f"{sc['id']}:{j}".encode()) % 1000)
            gain = 10 ** (S.SFX_GAIN_DB / 20) * synth.SFX_GAIN[cue["type"]] * cue.get("gain", 1.0)
            s = int(t * SR)
            seg = clip[: max(0, min(len(clip), n - s))]
            pan = 0.5 + 0.25 * np.sin(j * 1.7)
            sfx[s:s + len(seg), 0] += seg * gain * (1 - pan) * 1.4
            sfx[s:s + len(seg), 1] += seg * gain * pan * 1.4
            placed.append({"scene": sc["id"], "type": cue["type"], "t": round(t, 3)})
    out = music[:n] * duck[:, None] + sfx + voice[:, None] * 0.95
    out = out[: int(total * SR)]
    pre = out_wav.with_name(out_wav.stem + "_pre.wav")
    write_wav(pre, np.clip(out / max(1.0, np.abs(out).max() / 0.98), -1, 1))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(pre), "-af",
                    f"loudnorm=I={S.TARGET_LUFS}:TP=-1.5:LRA=11", "-ar", str(SR), str(out_wav)], check=True)
    pre.unlink(missing_ok=True)
    return {"total": total, "sfx": placed}
