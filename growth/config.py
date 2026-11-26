"""Paths, channel registry and the editable data files under story-pipeline/data/growth/."""

from __future__ import annotations

import json
from pathlib import Path

PIPELINE = Path(__file__).resolve().parent.parent          # story-pipeline/
DATA = PIPELINE / "data" / "growth"
REPORTS = DATA / "reports"            # every dashboard / video report, timestamped (history)
CACHE = DATA / "analytics_cache"      # raw API pulls, one file per channel per run
AUTH = DATA / "auth"                  # OAuth tokens per channel (private, never share)
QUOTA_LOG = DATA / "quota_log.jsonl"

# The user's existing analyzer holds the API key (.env) and the OAuth client (client_secret.json).
ANALYZER_DIR = PIPELINE.parent.parent / "youtube analytics"

CHANNELS = {
    "dr": {"name": "Divya Rahasya", "root": PIPELINE / "SanatanKatha", "modules": "kathas",
           "language": "hinglish", "kind": "katha"},
    "rs": {"name": "RealityShift", "root": PIPELINE / "RealityShift", "modules": "shorts",
           "language": "hinglish", "kind": "facts"},
    "bb": {"name": "Brain Blitz", "root": PIPELINE / "BrainBlitz", "modules": "core",
           "language": "english", "kind": "puzzle"},
}


def ensure_dirs() -> None:
    for d in (DATA, REPORTS, CACHE, AUTH):
        d.mkdir(parents=True, exist_ok=True)


def load_json(name: str, default):
    p = DATA / name
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def save_json(name: str, obj) -> Path:
    ensure_dirs()
    p = DATA / name
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def thresholds() -> dict:
    return load_json("ypp_thresholds.json", {})


def channel_settings(ch: str) -> dict:
    """Manual, human-entered facts the APIs do not expose (strikes, application status, channel id)."""
    return load_json("channel_status.json", {}).get(ch, {})
