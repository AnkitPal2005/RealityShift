"""6. PERFORMANCE INTELLIGENCE VALIDATOR.

Uses only fetched/imported numbers. Each Short is compared with the channel's OWN baseline (median of Shorts at
least MATURE_H hours old); patterns are grouped by length, title style, pillar, mega name and upload slot; any
group with fewer than MIN_N Shorts is shown but flagged as a weak signal and never drives a recommendation.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from statistics import median
from typing import Optional

from .base import Result, deities_in, pillar_of

MATURE_H = 48
MIN_N = 3
IST = timezone(timedelta(hours=5, minutes=30))
METRICS = [("views", "views"), ("engaged_views", "engaged views"), ("stayed_to_watch_pct", "stayed to watch %"),
           ("apv", "avg % viewed"), ("avd_s", "avg view duration s"), ("subs_per_1k", "subs / 1k views"),
           ("likes_per_1k", "likes / 1k views"), ("comments_per_1k", "comments / 1k views")]


def _age_h(v) -> float:
    try:
        pub = datetime.fromisoformat(v["published_at"].replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - pub).total_seconds() / 3600
    except Exception:
        return 0.0


def _derive(v: dict) -> dict:
    v = dict(v)
    views = v.get("views") or 0
    if views:
        if v.get("subs_gained") is not None:
            v["subs_per_1k"] = round(v["subs_gained"] / views * 1000, 2)
        if v.get("likes") is not None:
            v["likes_per_1k"] = round(v["likes"] / views * 1000, 1)
        if v.get("comments") is not None:
            v["comments_per_1k"] = round(v["comments"] / views * 1000, 2)
    return v


def _features(ch: str, v: dict) -> dict:
    t = v.get("title", "")
    d = v.get("duration_s") or 0
    try:
        hour = datetime.fromisoformat(v["published_at"].replace("Z", "+00:00")).astimezone(IST).hour
    except Exception:
        hour = None
    return {
        "length": "<25 s" if d < 25 else "25-32 s" if d <= 32 else "33-40 s" if d <= 40 else "41-60 s" if d <= 60
        else ">60 s",
        "title style": ("question" if "?" in t else "open loop (...)" if "..." in t or "…" in t
                        else "number" if re.search(r"\d", t) else "statement"),
        "pillar": pillar_of(ch, t + " " + v.get("local_text", "")),
        "mega name": (deities_in(t) or ["none"])[0] if ch == "dr" else "n/a",
        "slot (IST)": "n/a" if hour is None else ("morning <12" if hour < 12 else "noon 12-15" if hour < 15
                                                  else "afternoon 15-18" if hour < 18 else "evening 18+"),
    }


def _baseline(vs: list) -> dict:
    out = {}
    for k, _ in METRICS:
        vals = [v[k] for v in vs if v.get(k) is not None]
        out[k] = round(median(vals), 2) if vals else None
    return out


def analyze_channel(ch: str, pub: dict, shorts_text: Optional[dict] = None) -> Result:
    """Channel-level: baseline, best/worst, pattern groups, recommendations."""
    r = Result("performance")
    vids = [v for v in pub.get("_videos", []) if v.get("is_short") and v.get("privacy", "public") == "public"]
    if not vids:
        r.add("info", f"no published Shorts data - run `python growth.py fetch {ch}` (and `auth {ch}` for "
                      f"Analytics). Nothing is estimated.")
        r.score = None
        return r
    for v in vids:
        if shorts_text and v.get("local"):
            v["local_text"] = shorts_text.get(v["local"], "")
    vids = [_derive(v) for v in vids]
    mature = [v for v in vids if _age_h(v) >= MATURE_H]
    base = _baseline(mature or vids)
    r.data["baseline"] = base
    r.data["n_shorts"] = len(vids)
    r.data["n_mature"] = len(mature)
    have = {k for k, _ in METRICS if base.get(k) is not None}
    missing = [lbl for k, lbl in METRICS if k not in have]
    if missing:
        r.add("info", "not available (not fetched/imported, so not shown): " + ", ".join(missing))

    rank_key = "apv" if "apv" in have else "stayed_to_watch_pct" if "stayed_to_watch_pct" in have else "views"
    pool = mature or vids
    srt = sorted(pool, key=lambda v: (v.get(rank_key) is None, -(v.get(rank_key) or 0)))
    pick = lambda v: {k: v.get(k) for k in ("title", "video_id", "local", "views", "apv", "avd_s",
                                            "stayed_to_watch_pct", "subs_gained", "duration_s", "published_at")}
    r.data["rank_metric"] = rank_key
    r.data["best"] = [pick(v) for v in srt[:3]]
    ranked = [v for v in srt if v.get(rank_key) is not None]
    r.data["worst"] = [pick(v) for v in ranked[::-1][:3]]

    # pattern groups
    groups: dict = {}
    for v in pool:
        for dim, val in _features(ch, v).items():
            groups.setdefault(dim, {}).setdefault(val, []).append(v)
    table = {}
    for dim, vals in groups.items():
        table[dim] = []
        for val, vs in vals.items():
            row = {"group": val, "n": len(vs), "weak_signal": len(vs) < MIN_N}
            for k in ("views", rank_key, "subs_per_1k"):
                xs = [x[k] for x in vs if x.get(k) is not None]
                row[k] = round(median(xs), 2) if xs else None
            table[dim].append(row)
        table[dim].sort(key=lambda x: -(x.get(rank_key) or 0))
    r.data["patterns"] = table

    # recommendations: only from groups with n >= MIN_N
    table = {dim: rows for dim, rows in table.items() if len(rows) > 1}
    r.data["patterns"] = table
    for dim, rows in table.items():
        solid = [x for x in rows if not x["weak_signal"] and x.get(rank_key) is not None
                 and x["group"] not in ("Other", "none", "n/a")]
        if len(solid) < 2:
            continue
        hi, lo = solid[0], solid[-1]
        if lo[rank_key] and hi[rank_key] >= 1.15 * lo[rank_key]:
            r.suggest(f"{dim}: '{hi['group']}' beats '{lo['group']}' on {rank_key} ({hi[rank_key]} vs "
                      f"{lo[rank_key]}, n={hi['n']}/{lo['n']}) - script more '{hi['group']}'.")
    if not r.suggestions:
        r.add("info", f"no pattern has {MIN_N}+ Shorts on both sides with a clear gap yet - keep testing, "
                      f"one change at a time")
    else:
        r.add("info", "patterns are correlations on your own Shorts (topic, date and length overlap), not proof of "
                      "cause - change one thing at a time to confirm"
                      + (". Ranked on views only: retention data would be a better guide." if rank_key == "views"
                         else ""))
    young = [v for v in vids if _age_h(v) < MATURE_H]
    if young:
        r.add("info", f"{len(young)} Short(s) under {MATURE_H} h old are excluded from the baseline")
    r.score = None   # performance is reported, not scored against a made-up target
    return r


def video_vs_baseline(name: str, pub: dict, base: dict) -> Result:
    """One published Short vs the channel baseline."""
    r = Result("performance")
    v = pub.get(name)
    if not v:
        r.add("info", "not found on YouTube yet (or title differs - map it in data/growth/video_map.json)")
        return r
    v = _derive(v)
    r.data["video_id"] = v["video_id"]
    r.data["age_h"] = round(_age_h(v))
    comp = {}
    for k, lbl in METRICS:
        if v.get(k) is not None and base.get(k):
            ratio = v[k] / base[k]
            comp[lbl] = {"value": v[k], "baseline": base[k], "x": round(ratio, 2)}
            if ratio >= 1.3:
                r.add("ok", f"{lbl}: {v[k]} vs baseline {base[k]} ({ratio:.1f}x)")
            elif ratio <= 0.7:
                r.add("warn", f"{lbl}: {v[k]} vs baseline {base[k]} ({ratio:.1f}x)")
    r.data["vs_baseline"] = comp
    if r.data["age_h"] < MATURE_H:
        r.add("info", f"only {r.data['age_h']} h old - compare again after {MATURE_H} h")
    return r
