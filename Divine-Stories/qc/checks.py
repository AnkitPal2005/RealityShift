"""Quality control on the finished render. Any FAIL rejects the output (the upload package is not built).

Checks: container/stream specs, duration window, decodable frames with no blank or frozen-black scenes,
audio present / not silent / not clipping, captions inside their scenes and in order, every asset present
with an approved licence + attribution and not blocked by the rights review, every claim sourced, and
character consistency against the approved reference library.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np

from characters import library as chars
from config import settings as S
from generators.commons import license_ok, load_manifest, rights_block
from story import schema


def _probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def _frames_at(path: Path, times: list[float], w=270, h=480) -> list[np.ndarray]:
    frames = []
    for t in times:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1",
                              "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             capture_output=True, check=True).stdout
        frames.append(np.frombuffer(raw, np.uint8).reshape(h, w, 3) if len(raw) == w * h * 3 else None)
    return frames


def _audio(path: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le",
                          "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def run(story: dict, timeline: list[dict], video: Path) -> dict:
    res = []

    def check(name, ok, detail="", level="FAIL"):
        res.append({"check": name, "status": "PASS" if ok else level, "detail": detail})

    # -- story / sources
    try:
        warns = schema.validate(story)
        check("story schema", True, "; ".join(warns))
    except schema.StoryError as e:
        check("story schema", False, str(e))
    unsourced = [c["text"] for s in story["scenes"] for c in s.get("claims", []) if not c.get("sources")]
    check("claims sourced", not unsourced, "; ".join(unsourced))
    check("human source review", bool(story.get("review", {}).get("verified_by")),
          "review.verified_by empty: verify verse/section numbers before publishing", level="WARN")
    # -- assets / licences
    man = load_manifest()
    problems = []
    for s in story["scenes"]:
        a = s["visual"]["asset"]
        m = man.get(a)
        if not m:
            problems.append(f"{s['id']}: {a} not in manifest")
        elif not (S.ROOT / m["local"]).exists():
            problems.append(f"{s['id']}: file missing {m['local']}")
        elif not license_ok(m["license"], m["license_name"]):
            problems.append(f"{s['id']}: licence not allowed {m['license']}")
        elif rights_block(a):
            problems.append(f"{s['id']}: blocked by rights review")
        elif not m.get("attribution"):
            problems.append(f"{s['id']}: no attribution")
    check("assets present + licensed", not problems, "; ".join(problems))
    cc = chars.check_story(story)
    check("character consistency", not cc, "; ".join(cc))
    # -- container
    if not video.exists():
        check("video exists", False, str(video))
        return {"ok": False, "results": res}
    info = _probe(video)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    check("video stream 1080x1920", v is not None and v["width"] == S.W and v["height"] == S.H,
          f"{v and v['width']}x{v and v['height']}")
    fps = eval(v["r_frame_rate"]) if v else 0  # "30/1"
    check("30 fps", abs(fps - S.FPS) < 0.01, f"{fps}")
    check("h264 + yuv420p", v is not None and v["codec_name"] == "h264" and v.get("pix_fmt") == "yuv420p",
          f"{v and v['codec_name']} {v and v.get('pix_fmt')}")
    dur = float(info["format"]["duration"])
    check("duration 40-60 s", S.MIN_DURATION <= dur <= S.MAX_DURATION, f"{dur:.2f}s")
    check("audio stream", a is not None and a["codec_name"] == "aac", a and a["codec_name"])
    # -- frames: one sample per second + every scene midpoint
    times = sorted(set([round(t, 2) for t in np.arange(0.5, dur - 0.2, 1.0)] +
                       [round(x["start"] + x["dur"] / 2, 2) for x in timeline]))
    frames = _frames_at(video, times)
    broken = [t for t, f in zip(times, frames) if f is None]
    check("frames decodable", not broken, f"undecodable at {broken}")
    blank = [t for t, f in zip(times, frames) if f is not None and (f.std() < 8 or f.mean() < 12 or f.mean() > 245)]
    check("no blank frames", not blank, f"blank/flat at {blank}")
    frozen = []
    for x in timeline:   # each scene must move (camera/effects)
        f1, f2 = _frames_at(video, [x["start"] + x["dur"] * 0.3, x["start"] + x["dur"] * 0.7])
        if f1 is not None and f2 is not None and np.abs(f1.astype(int) - f2.astype(int)).mean() < 0.6:
            frozen.append(x["id"])
    check("no frozen scenes", not frozen, ", ".join(frozen))
    # -- audio
    au = _audio(video)
    peak = float(np.abs(au).max()) if len(au) else 0
    rms = float(np.sqrt((au ** 2).mean())) if len(au) else 0
    check("audio not silent", rms > 0.02, f"rms {rms:.3f}")
    clip_frac = float((np.abs(au) > 0.999).mean()) if len(au) else 0
    check("audio not clipping", clip_frac < 1e-4, f"peak {peak:.3f}, clipped {clip_frac:.2e}")
    silent_scenes = []
    for x in timeline:
        s0, s1 = int(x["vo_start"] * 16000), int((x["vo_start"] + x["vo_dur"]) * 16000)
        seg = au[s0:s1]
        if len(seg) == 0 or np.sqrt((seg ** 2).mean()) < 0.02:
            silent_scenes.append(x["id"])
    check("narration audible in every scene", not silent_scenes, ", ".join(silent_scenes))
    # -- caption sync
    sync = []
    for x in timeline:
        ts = [w["t"] for w in x["words"]]
        if ts != sorted(ts):
            sync.append(f"{x['id']}: word times out of order")
        if ts and (ts[0] < x["vo_start"] - 0.01 or ts[-1] > x["vo_start"] + x["vo_dur"] + 0.01):
            sync.append(f"{x['id']}: words outside narration window")
        n_words = len(schema.words(next(s for s in story["scenes"] if s["id"] == x["id"])["narration"]))
        if abs(len(ts) - n_words) > 2:
            sync.append(f"{x['id']}: {len(ts)} timed words vs {n_words} in script")
    check("captions synced to narration", not sync, "; ".join(sync))
    ok = all(r["status"] != "FAIL" for r in res)
    return {"ok": ok, "duration": dur, "results": res}
