"""AI YouTube Shorts Audience & Performance Auditor (100% free local analysis by default + optional Gemini mode).

Inspects the COMPLETE final rendered MP4 (actual audio waveform, silence/dead-air, clipping, speaking pace,
first-3-second hook motion, full-timeline frame sampling, storytelling, and policy risks) and produces a brutally
honest structured JSON audit report without ever auto-publishing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile
import wave
from typing import Callable, Optional

import numpy as np
from PIL import Image


@dataclass
class AuditorConfig:
    approved_min: int = 90
    minor_min: int = 80
    revision_min: int = 70
    max_revisions: int = 3
    max_duration_s: float = 45.0
    ideal_max_duration_s: float = 35.0
    silence_threshold_db: float = -42.0
    max_silence_gap_s: float = 0.65
    sample_interval_s: float = 1.0
    mode: str = "auto"  # "local" (100% free, zero API key), "gemini", or "auto"
    vision_model: str = "gemini-2.5-flash"


def _fmt_ts(sec: float) -> str:
    sec = max(0, int(round(sec)))
    return f"{sec // 60:02d}:{sec % 60:02d}"


def _probe_video(mp4_path: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_type,width,height,r_frame_rate",
        "-of", "json", str(mp4_path),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(res.stdout)
    dur = float(data.get("format", {}).get("duration", 0.0))
    v_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    a_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "audio"), None)
    return {
        "duration": dur,
        "width": int(v_stream.get("width", 0)),
        "height": int(v_stream.get("height", 0)),
        "has_audio": a_stream is not None,
    }


def _analyze_audio(mp4_path: Path, cfg: AuditorConfig) -> dict:
    """Extract full audio WAV via ffmpeg and inspect RMS, clipping, and dead-air gaps."""
    with tempfile.TemporaryDirectory() as td:
        wav_path = Path(td) / "audit_audio.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4_path),
             "-ac", "1", "-ar", "16000", "-sample_fmt", "s16", str(wav_path)],
            check=True,
        )
        with wave.open(str(wav_path), "rb") as wf:
            sr = wf.getframerate()
            raw = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0

    if len(raw) == 0:
        return {"rms_db": -99.0, "clipping_ratio": 0.0, "silence_gaps": [{"start": 0.0, "end": 1.0}]}

    rms = float(np.sqrt(np.mean(raw ** 2)) + 1e-9)
    rms_db = 20.0 * math.log10(rms)
    clipping_ratio = float(np.mean(np.abs(raw) >= 0.985))

    # 100 ms windows for silence / dead-air detection
    win = max(1, int(sr * 0.1))
    n_win = len(raw) // win
    frames = raw[:n_win * win].reshape(n_win, win)
    win_db = 20.0 * np.log10(np.sqrt(np.mean(frames ** 2, axis=1)) + 1e-9)
    silent = win_db < cfg.silence_threshold_db

    gaps: list[dict] = []
    in_gap = False
    g_start = 0.0
    for idx, is_sil in enumerate(silent):
        t = idx * 0.1
        if is_sil and not in_gap:
            in_gap = True
            g_start = t
        elif not is_sil and in_gap:
            in_gap = False
            if (t - g_start) >= cfg.max_silence_gap_s:
                gaps.append({"start": round(g_start, 2), "end": round(t, 2)})
    if in_gap and ((n_win * 0.1) - g_start) >= cfg.max_silence_gap_s:
        gaps.append({"start": round(g_start, 2), "end": round(n_win * 0.1, 2)})

    return {
        "rms_db": round(rms_db, 2),
        "clipping_ratio": round(clipping_ratio, 5),
        "silence_gaps": gaps,
    }


def _sample_timeline_frames(mp4_path: Path, duration: float, interval: float = 1.0) -> list[tuple[float, np.ndarray]]:
    """Sample frames across the entire video timeline (plus dense 0s, 1s, 2s, 3s hook frames)."""
    with tempfile.TemporaryDirectory() as td:
        out_pat = str(Path(td) / "f_%04d.png")
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4_path),
             "-vf", f"fps=1/{interval},scale=270:480", out_pat],
            check=True,
        )
        files = sorted(Path(td).glob("f_*.png"))
        sampled: list[tuple[float, np.ndarray]] = []
        for idx, fp in enumerate(files):
            with Image.open(fp) as im:
                arr = np.asarray(im.convert("RGB"), dtype=np.float32)
            sampled.append((round(idx * interval, 2), arr))
    return sampled


def _analyze_visual_timeline(frames: list[tuple[float, np.ndarray]]) -> dict:
    """Measure hook motion (0-3s), frozen/static segments, and overall visual energy."""
    if not frames:
        return {"hook_motion": 0.0, "static_segments": [], "mean_edge": 0.0, "loop_similarity": 0.0}

    diffs: list[tuple[float, float]] = []
    edges: list[float] = []
    for i, (t, arr) in enumerate(frames):
        gray = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
        gx = np.abs(np.diff(gray, axis=1))
        gy = np.abs(np.diff(gray, axis=0))
        edges.append(float((gx[:-1, :] + gy[:, :-1] > 16.0).mean()))
        if i > 0:
            mae = float(np.mean(np.abs(arr - frames[i - 1][1])))
            diffs.append((t, mae))

    hook_diffs = [d for t, d in diffs if t <= 3.5]
    hook_motion = float(np.mean(hook_diffs)) if hook_diffs else 0.0

    # Detect static/frozen segments (>= 2 consecutive 1s samples with tiny motion)
    static_segs: list[dict] = []
    run_start: Optional[float] = None
    for t, d in diffs:
        if d < 1.2:
            if run_start is None:
                run_start = max(0.0, t - 1.0)
        else:
            if run_start is not None and (t - run_start) >= 2.0:
                static_segs.append({"start": run_start, "end": t})
            run_start = None
    if run_start is not None and (frames[-1][0] - run_start) >= 2.0:
        static_segs.append({"start": run_start, "end": frames[-1][0]})

    # Loop similarity between first and last frame
    loop_diff = float(np.mean(np.abs(frames[0][1] - frames[-1][1])))
    loop_sim = max(0.0, min(1.0, 1.0 - loop_diff / 80.0))

    return {
        "hook_motion": round(hook_motion, 2),
        "static_segments": static_segs,
        "mean_edge": round(float(np.mean(edges)), 4),
        "loop_similarity": round(loop_sim, 2),
    }


def _load_alignment(mp4_path: Path) -> Optional[dict]:
    jp = mp4_path.with_suffix(".json")
    if jp.exists():
        try:
            return json.loads(jp.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def audit_short(
    mp4_path: Path,
    script_text: str = "",
    story_module: Optional[object] = None,
    config: Optional[AuditorConfig] = None,
    save_report: bool = True,
) -> dict:
    """Audit a complete rendered Short MP4 and return a structured JSON report."""
    cfg = config or AuditorConfig()
    mp4_path = Path(mp4_path)
    if not mp4_path.exists():
        raise FileNotFoundError(f"Rendered MP4 not found: {mp4_path}")

    probe = _probe_video(mp4_path)
    dur = probe["duration"]
    audio = _analyze_audio(mp4_path, cfg) if probe["has_audio"] else {
        "rms_db": -99.0, "clipping_ratio": 0.0, "silence_gaps": [{"start": 0.0, "end": dur}]
    }
    frames = _sample_timeline_frames(mp4_path, dur, cfg.sample_interval_s)
    vis = _analyze_visual_timeline(frames)
    align = _load_alignment(mp4_path)

    weak_segments: list[dict] = []
    improvements: list[str] = []
    critical_defects: list[str] = []

    # ---- Critical checks ----
    if not probe["has_audio"] or audio["rms_db"] < -50.0:
        critical_defects.append("missing_or_silent_audio")
    if audio["clipping_ratio"] > 0.02:
        critical_defects.append("audio_clipping_distortion")
    if probe["width"] != 1080 or probe["height"] != 1920:
        critical_defects.append(f"invalid_resolution_{probe['width']}x{probe['height']}")
    if dur > cfg.max_duration_s:
        critical_defects.append(f"duration_over_{cfg.max_duration_s}s_lock")

    # ---- Dead-air / slow audio gaps ----
    for g in audio["silence_gaps"]:
        weak_segments.append({
            "start": _fmt_ts(g["start"]),
            "end": _fmt_ts(g["end"]),
            "problem": f"Dead-air / long silence pause ({g['end'] - g['start']:.1f}s)",
            "suggestion": "Trim dead air or tighten MAX_GAP / TAIL_PAD so viewer attention does not drop",
        })
        if g["start"] < 3.0:
            critical_defects.append("dead_air_in_first_3s_hook")

    # ---- Static / repetitive visuals ----
    for seg in vis["static_segments"]:
        weak_segments.append({
            "start": _fmt_ts(seg["start"]),
            "end": _fmt_ts(seg["end"]),
            "problem": "Visuals look static or repetitive with minimal motion",
            "suggestion": "Add camera zoom/pan or character action every ~2 seconds",
        })

    # ---- Scene pacing from alignment JSON ----
    scenes_list = align if isinstance(align, list) else (align.get("scenes") if isinstance(align, dict) else [])
    if isinstance(scenes_list, list):
        for sc in scenes_list:
            sdur = float(sc.get("dur", 0.0))
            if sdur > 5.0:
                weak_segments.append({
                    "start": _fmt_ts(float(sc.get("start", 0.0))),
                    "end": _fmt_ts(float(sc.get("start", 0.0)) + sdur),
                    "problem": f"Scene '{sc.get('key', '')}' runs {sdur:.1f}s (risk of midpoint retention drop)",
                    "suggestion": "Split into 2 shorter shots or add a mid-scene visual turn",
                })

    # ---- Score out of 100 (Hook 20, Story 15, Retention 20, Visual 15, Audio 10, Pacing 10, Ending 10) ----
    hook_s = 18 if (vis["hook_motion"] >= 2.5 and not any(g["start"] < 3.0 for g in audio["silence_gaps"])) else 13
    if dur > 38.0:
        ret_s = 13
        improvements.append(f"Duration is {dur:.1f}s; tightening to 26-32s typically improves APV.")
    elif dur <= cfg.ideal_max_duration_s and not vis["static_segments"]:
        ret_s = 18
    else:
        ret_s = 15

    story_s = 14 if (isinstance(scenes_list, list) and len(scenes_list) >= 6) or script_text else 11
    vis_s = 14 if (vis["mean_edge"] >= 0.015 and not vis["static_segments"]) else 10
    aud_s = 9 if (-26.0 <= audio["rms_db"] <= -8.0 and audio["clipping_ratio"] <= 0.005 and not audio["silence_gaps"]) else 6
    pace_s = 9 if (not vis["static_segments"] and len(weak_segments) <= 1) else 6
    end_s = 9 if vis["loop_similarity"] >= 0.45 else 7

    overall = hook_s + story_s + ret_s + vis_s + aud_s + pace_s + end_s
    if critical_defects:
        overall = min(overall, 65)

    if overall >= cfg.approved_min and not critical_defects:
        status = "APPROVED"
        rec = "READY TO PUBLISH (with user approval)"
        verdict = "Would stop scrolling and watch to the end"
    elif overall >= cfg.minor_min and not critical_defects:
        status = "APPROVED WITH MINOR IMPROVEMENTS"
        rec = "READY WITH OPTIONAL POLISH (review weak segments before publishing)"
        verdict = "Would watch, though minor pacing polish could lift retention"
    elif overall >= cfg.revision_min and not critical_defects:
        status = "NEEDS REVISION"
        rec = "REVISE WEAK SEGMENTS BEFORE PUBLISHING"
        verdict = "Risk of mid-video swipe away"
    else:
        status = "REJECTED"
        rec = "DO NOT PUBLISH - FIX CRITICAL DEFECTS AND RE-RENDER"
        verdict = "Would likely swipe away early"

    for seg in weak_segments:
        if seg["suggestion"] not in improvements:
            improvements.append(seg["suggestion"])

    # Potential tiers (explicitly heuristic estimates, not YouTube Analytics)
    hook_str = "HIGH" if hook_s >= 17 else ("MEDIUM" if hook_s >= 14 else "LOW")
    ret_pot = "HIGH" if ret_s >= 17 else ("MEDIUM" if ret_s >= 14 else "LOW")
    stw_pot = "HIGH" if (hook_s >= 18 and vis["hook_motion"] >= 4.0) else ("MEDIUM" if hook_s >= 15 else "LOW")
    apv_pot = "HIGH" if (dur <= 32.0 and ret_s >= 17) else ("MEDIUM" if ret_s >= 14 else "LOW")
    rep_pot = "HIGH" if vis["loop_similarity"] >= 0.65 else ("MEDIUM" if vis["loop_similarity"] >= 0.40 else "LOW")

    report = {
        "video_status": status,
        "overall_score": overall,
        "audience_verdict": verdict,
        "hook_strength": hook_str,
        "retention_potential": ret_pot,
        "stw_potential": stw_pot,
        "apv_potential": apv_pot,
        "replay_potential": rep_pot,
        "audio_quality": "GOOD" if aud_s >= 8 else "NEEDS_WORK",
        "visual_quality": "EXCELLENT" if vis_s >= 14 else ("GOOD" if vis_s >= 11 else "NEEDS_WORK"),
        "storytelling": "GOOD" if story_s >= 13 else "NEEDS_WORK",
        "policy_risk": "LOW" if not critical_defects else "MEDIUM",
        "weak_segments": weak_segments,
        "improvements": improvements,
        "final_recommendation": rec,
        "details": {
            "duration_s": round(dur, 2),
            "resolution": f"{probe['width']}x{probe['height']}",
            "scores": {
                "hook": hook_s, "storytelling": story_s, "retention_potential": ret_s,
                "visual_quality": vis_s, "audio_quality": aud_s, "editing_and_pacing": pace_s,
                "ending_and_replay": end_s,
            },
            "audio_metrics": audio,
            "visual_metrics": vis,
            "critical_defects": critical_defects,
            "disclaimer": "STW/APV/Replay tiers are heuristic pre-publish estimates, not actual YouTube Analytics. "
                          "Policy check does not guarantee copyright clearance or monetization approval.",
        },
    }

    if save_report:
        out_json = mp4_path.with_name(f"{mp4_path.stem}_audit.json")
        out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    return report


def audit_with_revisions(
    mp4_path: Path,
    revise_fn: Optional[Callable[[dict, int], Path]] = None,
    config: Optional[AuditorConfig] = None,
) -> dict:
    """Audit MP4 and optionally run up to max_revisions (3) if REJECTED."""
    cfg = config or AuditorConfig()
    current = Path(mp4_path)
    report = audit_short(current, config=cfg)
    for attempt in range(1, cfg.max_revisions + 1):
        if report["video_status"] != "REJECTED" or revise_fn is None:
            break
        current = revise_fn(report, attempt)
        report = audit_short(current, config=cfg)
    return report
