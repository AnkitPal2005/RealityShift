"""Per-video reports and the MASTER DASHBOARD (Markdown + JSON), saved with timestamps for history."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean
from typing import Optional

from . import inventory, store
from .config import CHANNELS, REPORTS, ensure_dirs
from .decision import decide
from .validators import copyright_policy, metadata, originality, performance, readiness, subscriber, topic
from .validators.base import short_text

IST = timezone(timedelta(hours=5, minutes=30))
RECENT = 10
ICON = {"info": "·", "ok": "OK", "warn": "WARN", "fix": "FIX", "block": "BLOCK"}


def _stamp() -> str:
    return datetime.now(IST).strftime("%Y%m%d_%H%M")


def _fmt(v, nd=0) -> str:
    if v is None:
        return "n/a"
    if isinstance(v, (int, float)):
        return f"{v:,.{nd}f}"
    return str(v)


# ---------------------------------------------------------------------------------------------------------
# per video
# ---------------------------------------------------------------------------------------------------------
def run_video(ch: str, name: str, market: Optional[dict] = None, all_shorts: Optional[dict] = None,
              pub: Optional[dict] = None, base: Optional[dict] = None) -> dict:
    all_shorts = all_shorts or inventory.load_all()
    me = next((s for s in all_shorts[ch] if s.name == name), None)
    if me is None:
        raise SystemExit(f"no Short '{name}' on channel '{ch}'")
    others = [s for s in all_shorts[ch] if s.name != name]
    every = [s for ss in all_shorts.values() for s in ss]
    if pub is None:
        pub = store.published(ch, all_shorts[ch])
    perf = {k: v for k, v in pub.items() if not k.startswith("_")}
    results = [
        topic.validate(me, others, perf=perf or None, market=market),
        originality.validate(me, others, all_channels=every),
        copyright_policy.validate(me),
        metadata.validate(me),
        subscriber.validate(me, others, perf=perf or None),
    ]
    if name in perf:
        if base is None:
            base = performance.analyze_channel(ch, pub).data.get("baseline", {})
        results.append(performance.video_vs_baseline(name, pub, base))
    dec = decide(results)
    return {"channel": ch, "name": name, "title": me.title, "duration": me.duration,
            "generated": datetime.now(IST).isoformat(timespec="seconds"), "decision": dec,
            "published": name in perf, "results": [r.to_dict() for r in results]}


def video_markdown(rep: dict) -> str:
    d = rep["decision"]
    md = [f"# Growth check - {rep['name']} ({CHANNELS[rep['channel']]['name']})", "",
          f"**Decision: {d['decision']}**  (validator average {_fmt(d['score'])}/100)  ", f"Title: {rep['title']}  ",
          f"Length: {_fmt(rep['duration'], 1)} s · Generated {rep['generated']}", "", f"_{d['human_control']}_", ""]
    if d["must_fix"]:
        md += ["## Must fix", ""] + [f"- {x}" for x in d["must_fix"]] + [""]
    if d["improve"]:
        md += ["## Improve", ""] + [f"- {x}" for x in d["improve"]] + [""]
    md += ["## Validators", "", "| Validator | Status | Score |", "|---|---|---|"]
    md += [f"| {r['validator']} | {r['status']} | {_fmt(r['score'])} |" for r in rep["results"]]
    for r in rep["results"]:
        md += ["", f"### {r['validator']}", ""]
        md += [f"- {ICON[f['level']]} {f['msg']}" for f in r["findings"]] or ["- nothing found"]
        md += [f"- Suggestion: {s}" for s in r["suggestions"]]
        keep = {k: v for k, v in r["data"].items() if k in ("demand_basis", "synthetic_disclosure", "made_for_kids",
                                                             "copyright_risk", "policy_risk", "disclaimer",
                                                             "max_script_overlap", "pillar", "vs_baseline")}
        for k, v in keep.items():
            md.append(f"- {k}: {json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v}")
    return "\n".join(md) + "\n"


def save_video(rep: dict, next_to: Optional[Path] = None) -> list[Path]:
    ensure_dirs()
    d = REPORTS / "videos"
    d.mkdir(exist_ok=True)
    base = d / f"{rep['channel']}_{rep['name']}_{_stamp()}"
    paths = [base.with_suffix(".json"), base.with_suffix(".md")]
    paths[0].write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    paths[1].write_text(video_markdown(rep), encoding="utf-8")
    if next_to:
        p = next_to.with_name(next_to.stem + "_growth.md")
        p.write_text(video_markdown(rep), encoding="utf-8")
        paths.append(p)
    return paths


# ---------------------------------------------------------------------------------------------------------
# channel dashboard
# ---------------------------------------------------------------------------------------------------------
def _sub_trend(daily: list) -> list:
    if not daily:
        return []
    out = []
    for i in range(0, len(daily), 30):
        chunk = daily[i:i + 30]
        g, l, v = (sum(d[k] for d in chunk) for k in ("subs_gained", "subs_lost", "views"))
        out.append({"from": chunk[0]["day"], "to": chunk[-1]["day"], "net_subs": g - l, "views": v,
                    # a ratio on a few hundred views is noise, not a trend
                    "subs_per_1k_views": round((g - l) / v * 1000, 2) if v >= 1000 else None})
    return out


def run_channel(ch: str, all_shorts: Optional[dict] = None) -> dict:
    all_shorts = all_shorts or inventory.load_all()
    shorts = all_shorts[ch]
    pub = store.published(ch, shorts)
    snap = pub.get("_snapshot")
    texts = {s.name: short_text(s) for s in shorts}
    perf_r = performance.analyze_channel(ch, pub, texts)
    base = perf_r.data.get("baseline", {})
    orig = originality.channel_risk(shorts)
    recent = [s for s in shorts if s.order >= 0][-RECENT:] or shorts[-RECENT:]
    cp = [copyright_policy.validate(s) for s in recent]
    copy_risk = max((r.data["copyright_risk"] for r in cp), default=None)
    pol_risk = round(mean(r.data["policy_risk"] for r in cp)) if cp else None
    ready = readiness.audit(ch, snap, orig.get("risk"), copy_risk, pol_risk)
    ident = subscriber.channel_identity(ch, shorts)

    # decisions for the most recent Shorts (latest render first)
    decisions = []
    for s in list(reversed(recent))[:6]:
        rep = run_video(ch, s.name, all_shorts=all_shorts, pub=pub, base=base)
        decisions.append({"name": s.name, "title": s.title, "decision": rep["decision"]["decision"],
                          "score": rep["decision"]["score"], "published": rep["published"],
                          "top_issue": (rep["decision"]["must_fix"] or rep["decision"]["improve"] or ["-"])[0]})

    vids = [v for v in pub.get("_videos", []) if v.get("is_short") and v.get("privacy", "public") == "public"]
    totals = (snap or {}).get("totals", {})
    avg = lambda k: round(mean(v[k] for v in vids if v.get(k) is not None), 1) \
        if any(v.get(k) is not None for v in vids) else None
    dash = {
        "channel": ch, "name": CHANNELS[ch]["name"], "generated": datetime.now(IST).isoformat(timespec="seconds"),
        "data_fetched": (snap or {}).get("fetched_at"), "data_mode": (snap or {}).get("mode"),
        "data_errors": (snap or {}).get("errors", []),
        "totals": {
            "videos_published": totals.get("video_count"), "public_shorts_read": len(vids),
            "local_shorts_built": len(shorts), "subscribers": totals.get("subscribers"),
            "qualified_shorts_views_90d": totals.get("shorts_views_90d"),
            "qualified_watch_hours_365d": totals.get("watch_hours_365d"),
            "public_uploads_90d": totals.get("public_uploads_90d"),
            "avg_stayed_to_watch_pct": avg("stayed_to_watch_pct"), "avg_apv": avg("apv"),
        },
        "best": perf_r.data.get("best", []), "worst": perf_r.data.get("worst", []),
        "rank_metric": perf_r.data.get("rank_metric"), "baseline": base,
        "patterns": perf_r.data.get("patterns", {}), "performance_notes": perf_r.findings,
        "recommendations": perf_r.suggestions,
        "subscriber_trend": _sub_trend((snap or {}).get("daily_90d") or []),
        "identity": ident, "originality_risk": orig, "copyright_risk": copy_risk, "policy_risk": pol_risk,
        "asset_ledger": copyright_policy.ledger_status(ch),
        "readiness": ready.to_dict(), "status": ready.data["status"], "decisions": decisions,
    }
    dash["next_actions"] = next_actions(dash, ready)
    dash["previous"] = _previous(ch)
    return dash


def next_actions(d: dict, ready) -> list[str]:
    acts = [f["msg"] for f in ready.findings if f["level"] == "fix"]
    if not d["data_fetched"]:
        acts.append(f"Fetch real numbers: `python growth.py auth {d['channel']}` once, then "
                    f"`python growth.py fetch {d['channel']}`.")
    elif d["totals"]["avg_stayed_to_watch_pct"] is None:
        acts.append(f"Import Studio 'Stayed to watch' per Short (not in the API): `python growth.py studio-import "
                    f"{d['channel']} <export.csv>`.")
    for x in d["decisions"]:
        if x["decision"] in ("REJECTED", "NEEDS REVISION") and not x["published"]:
            acts.append(f"{x['name']}: {x['decision']} - {x['top_issue']}")
    if d["asset_ledger"]["unknown"]:
        acts.append(f"Record owner/licence for {len(d['asset_ledger']['unknown'])} asset(s) in "
                    f"data/growth/asset_ledger.json.")
    r = d["originality_risk"].get("risk")
    if r is not None and r >= 40:
        a = d["originality_risk"]["most_alike"][0]
        acts.append(f"Originality risk {r}/100: '{a[1]}' and '{a[2]}' are {a[0]:.0%} alike - change structure/"
                    f"template on the next Shorts.")
    acts += d["recommendations"][:3] + ready.suggestions[:2]
    return acts


def _previous(ch: str) -> Optional[dict]:
    prev = sorted((REPORTS / "channels").glob(f"{ch}_*.json")) if (REPORTS / "channels").exists() else []
    if not prev:
        return None
    p = json.loads(prev[-1].read_text(encoding="utf-8"))
    return {"generated": p.get("generated"), "totals": p.get("totals"), "status": p.get("status")}


def dashboard_markdown(dashes: list[dict]) -> str:
    md = ["# Growth & Monetization Dashboard", "",
          f"Generated {datetime.now(IST).strftime('%d %b %Y %H:%M')} IST. Numbers come only from the YouTube APIs, "
          "your Studio imports and the local pipeline; 'n/a' means not fetched, never estimated. "
          "Threshold reached is not YPP approval.", ""]
    md += ["| Channel | Status | Subs | Shorts views 90d | Watch h 365d | Avg APV | Avg STW | Orig. risk | "
           "Copyright risk |", "|---|---|---|---|---|---|---|---|---|"]
    for d in dashes:
        t = d["totals"]
        md.append(f"| {d['name']} | **{d['status']}** | {_fmt(t['subscribers'])} | "
                  f"{_fmt(t['qualified_shorts_views_90d'])} | {_fmt(t['qualified_watch_hours_365d'], 1)} | "
                  f"{_fmt(t['avg_apv'], 1)} | {_fmt(t['avg_stayed_to_watch_pct'], 1)} | "
                  f"{_fmt(d['originality_risk'].get('risk'))} | {_fmt(d['copyright_risk'])} |")
    for d in dashes:
        t = d["totals"]
        rd = d["readiness"]["data"]
        md += ["", f"## {d['name']} - {d['status']}", "",
               f"Data: {d['data_mode'] or 'not fetched'} ({d['data_fetched'] or '-'})", ""]
        if d["previous"] and d["previous"].get("totals"):
            p = d["previous"]["totals"]
            ch = [f"{k.replace('_', ' ')} {_fmt(p.get(k))} -> {_fmt(t.get(k))}" for k in
                  ("subscribers", "qualified_shorts_views_90d", "avg_apv") if p.get(k) != t.get(k)]
            if ch:
                md += [f"Since {d['previous']['generated'][:16]}: " + "; ".join(ch), ""]
        md += ["| Metric | Value |", "|---|---|"]
        for k, v in t.items():
            md.append(f"| {k.replace('_', ' ')} | {_fmt(v, 1 if isinstance(v, float) else 0)} |")
        for tier in ("early", "full", "full_reported_2027"):
            if tier not in rd:
                continue
            x = rd[tier]
            state = "MET" if x["met"] else "UNKNOWN (missing: " + ", ".join(x["unknown"]) + ")" \
                if x["met"] is None else "not met"
            md += ["", f"**{x['label']}** - {state}"
                       f"{' via ' + x['path'] if x['path'] else ''}", "", "| Requirement | Have | Need | % |",
                   "|---|---|---|---|"]
            md += [f"| {k} | {_fmt(h)} | {_fmt(n)} | {_fmt(p, 1)} |" for k, (h, n, p) in x["rows"].items()]
        if d["best"]:
            md += ["", f"**Best Shorts** (by {d['rank_metric']})", ""]
            md += [f"- {b['title']} - views {_fmt(b['views'])}, APV {_fmt(b['apv'], 1)}, STW "
                   f"{_fmt(b['stayed_to_watch_pct'], 1)}, subs {_fmt(b['subs_gained'])}" for b in d["best"]]
            md += ["", f"**Weakest Shorts** (by {d['rank_metric']})", ""]
            md += [f"- {b['title']} - views {_fmt(b['views'])}, APV {_fmt(b['apv'], 1)}, STW "
                   f"{_fmt(b['stayed_to_watch_pct'], 1)}" for b in d["worst"]]
        if d["subscriber_trend"]:
            md += ["", "**Subscriber conversion (30-day blocks)**", ""]
            md += [f"- {x['from']} to {x['to']}: net {x['net_subs']:+,} subs, {x['views']:,} views, "
                   f"{_fmt(x['subs_per_1k_views'], 2)} subs/1k" for x in d["subscriber_trend"]]
        o = d["originality_risk"]
        md += ["", f"**Originality risk:** {_fmt(o.get('risk'))}/100 (last {o.get('n')} Shorts, mean pair "
                   f"similarity {_fmt(o.get('mean_pair_similarity'), 2)}) · **Copyright risk:** "
                   f"{_fmt(d['copyright_risk'])}/100 · **Policy risk:** {_fmt(d['policy_risk'])}/100 · **Identity:** "
                   f"{_fmt(d['identity'].get('identity'))}% of recent Shorts in the top 2 pillars"]
        if d["decisions"]:
            md += ["", "**Recent Shorts - decisions**", "", "| Short | Decision | Score | Published | Top issue |",
                   "|---|---|---|---|---|"]
            md += [f"| {x['name']} | {x['decision']} | {_fmt(x['score'])} | {'yes' if x['published'] else 'no'} | "
                   f"{x['top_issue'][:110]} |" for x in d["decisions"]]
        if d["patterns"]:
            md += ["", "**Patterns** (groups with n<3 are weak signals)", ""]
            for dim, rows in d["patterns"].items():
                cells = ", ".join(f"{r['group']} {_fmt(r.get(d['rank_metric']), 1)} (n={r['n']}"
                                  f"{', weak' if r['weak_signal'] else ''})" for r in rows)
                md.append(f"- {dim}: {cells}")
        if d["data_errors"]:
            md += ["", "Data gaps: " + "; ".join(d["data_errors"])]
        md += ["", "**Recommended next actions**", ""] + [f"{i}. {a}" for i, a in enumerate(d["next_actions"], 1)]
    return "\n".join(md) + "\n"


def save_dashboard(dashes: list[dict]) -> list[Path]:
    ensure_dirs()
    (REPORTS / "channels").mkdir(exist_ok=True)
    stamp = _stamp()
    paths = []
    for d in dashes:
        p = REPORTS / "channels" / f"{d['channel']}_{stamp}.json"
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        paths.append(p)
        with (REPORTS / "history.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps({"t": d["generated"], "channel": d["channel"], "status": d["status"],
                                **d["totals"], "originality_risk": d["originality_risk"].get("risk"),
                                "copyright_risk": d["copyright_risk"]}, default=str) + "\n")
    md = dashboard_markdown(dashes)
    for p in (REPORTS / f"dashboard_{stamp}.md", REPORTS / "dashboard_latest.md"):
        p.write_text(md, encoding="utf-8")
        paths.append(p)
    return paths
