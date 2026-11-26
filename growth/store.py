"""Join published-video numbers (API snapshot + Studio-only import) onto the pipeline's local Shorts.

Studio-only metrics (Shown in feed, Stayed to watch / Swiped away, Returning viewers) are not in any public API.
`python growth.py studio-import <ch> <file.csv>` reads a Studio export or the template
data/growth/studio_template.csv; headers are matched loosely. Values are stored exactly as given.
Local Short <-> YouTube video mapping: data/growth/video_map.json ({"dr:hanuman_cycle": "VIDEO_ID"}) wins,
otherwise the shipped title is matched to the YouTube title (>= 0.75 word overlap).
"""

from __future__ import annotations

import csv
import re
from datetime import date
from pathlib import Path

from .config import load_json, save_json
from .text import content_words, jaccard
from .youtube_api import latest

STUDIO = "studio_metrics.json"
MAP = "video_map.json"
MATCH = 0.5   # min title similarity for an automatic local<->YouTube match (manual map overrides)

HEADERS = [  # (field, substrings that identify the column; first match wins)
    ("video_id", ["video id", "content", "videoid"]),
    ("title", ["video title", "title"]),
    ("shown_in_feed", ["shown in feed", "shown in the feed", "impressions"]),
    ("stayed_to_watch_pct", ["stayed to watch", "viewed (%)", "viewed vs swiped", "stayed"]),
    ("swiped_away_pct", ["swiped away", "swiped"]),
    ("returning_viewers", ["returning viewers", "returning"]),
    ("new_viewers", ["new viewers"]),
    ("engaged_views", ["engaged views"]),
]


def _num(v: str):
    v = (v or "").strip().replace(",", "").replace("%", "")
    if not v or v.lower() in ("n/a", "-", "—"):
        return None
    try:
        return float(v) if "." in v else int(v)
    except ValueError:
        return None


def studio_import(ch: str, path: Path) -> dict:
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit("empty CSV")
    cols = {}
    for field, keys in HEADERS:
        for h in rows[0].keys():
            hl = (h or "").lower().strip()
            if h not in cols.values() and any(k in hl for k in keys):
                cols[field] = h
                break
    if "video_id" not in cols and "title" not in cols:
        raise SystemExit(f"CSV needs a 'Video ID'/'Content' or 'Video title' column. Got: {list(rows[0])}")
    db = load_json(STUDIO, {})
    chdb = db.setdefault(ch, {})
    n = 0
    for r in rows:
        vid = (r.get(cols.get("video_id", ""), "") or "").strip()
        title = (r.get(cols.get("title", ""), "") or "").strip()
        if not vid and not title or vid.lower() == "total":
            continue
        rec = {"title": title, "imported": date.today().isoformat(), "source_file": path.name}
        for field, _ in HEADERS[2:]:
            if field in cols:
                val = _num(r.get(cols[field], ""))
                if val is not None:
                    rec[field] = val
        if "stayed_to_watch_pct" in rec and "swiped_away_pct" not in rec:
            rec["swiped_away_pct"] = round(100 - rec["stayed_to_watch_pct"], 1)
        chdb[vid or f"title:{title}"] = {**chdb.get(vid or f"title:{title}", {}), **rec}
        n += 1
    save_json(STUDIO, db)
    return {"rows": n, "columns": cols}


def _clean(t: str) -> set[str]:
    return content_words(re.sub(r"#\w+", "", t or ""))


def published(ch: str, shorts: list) -> dict:
    """{local short name: merged metrics dict} for Shorts that are found on YouTube. Also returns the list of
    every published video (mapped or not) under key '_videos'."""
    snap = latest(ch)
    if not snap:
        return {"_videos": [], "_snapshot": None}
    studio = load_json(STUDIO, {}).get(ch, {})
    manual = load_json(MAP, {})
    videos = []
    for v in snap["videos"]:
        rec = dict(v)
        st = studio.get(v["video_id"]) or next((s for k, s in studio.items() if k.startswith("title:")
                                                and jaccard(_clean(s.get("title", "")), _clean(v["title"])) >= 0.75),
                                               None)
        if st:
            rec.update({k: val for k, val in st.items() if k not in ("title",)})
        if rec.get("views_analytics") is not None:
            rec["views"] = max(rec["views"], rec["views_analytics"])
        videos.append(rec)
    by_id = {v["video_id"]: v for v in videos}
    out: dict = {"_videos": videos, "_snapshot": {k: snap.get(k) for k in ("fetched_at", "mode", "errors", "totals",
                                                                           "channel_title", "daily_90d")}}
    # 1) manual map wins
    taken = set()
    for s in shorts:
        vid = manual.get(s.key)
        if vid and vid in by_id:
            by_id[vid]["local"] = s.name
            out[s.name] = by_id[vid]
            taken.add(vid)
    # 2) best title/topic match, one-to-one, strongest pairs first (titles are often edited at upload)
    cands = []
    for s in shorts:
        if s.name in out:
            continue
        mine = _clean(s.title) | _clean(s.topic)
        for v in videos:
            if v["video_id"] in taken:
                continue
            theirs = _clean(v["title"])
            score = max(jaccard(_clean(s.title), theirs),
                        len(mine & theirs) / max(len(theirs), 1) if len(mine & theirs) >= 3 else 0)
            if score >= MATCH:
                cands.append((score, s.name, v["video_id"]))
    for score, name, vid in sorted(cands, reverse=True):
        if name in out or vid in taken:
            continue
        by_id[vid]["local"] = name
        by_id[vid]["match_score"] = round(score, 2)
        out[name] = by_id[vid]
        taken.add(vid)
    return out
