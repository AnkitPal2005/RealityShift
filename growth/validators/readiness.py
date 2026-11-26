"""7. CHANNEL MONETIZATION READINESS AUDITOR.

Progress toward Early YPP and full ad monetization, tracked separately, from fetched numbers + the manual
data/growth/channel_status.json. Reaching a threshold is NOT approval: YouTube reviews every application by hand
(originality / reused-content review included), so the status ladder never jumps to MONETIZED by itself.
"""

from __future__ import annotations

from ..config import channel_settings, thresholds
from .base import Result

STATUSES = ["NOT READY", "BUILDING AUDIENCE", "EARLY YPP ELIGIBLE", "FULL YPP THRESHOLD REACHED",
            "APPLICATION REVIEW PENDING", "MONETIZED"]


def _pct(have, need):
    if have is None or not need:
        return None
    return round(min(100.0, 100 * have / need), 1)


def _tier(t: dict, totals: dict) -> dict:
    subs, uploads = totals.get("subscribers"), totals.get("public_uploads_90d")
    sv, wh = totals.get("shorts_views_90d"), totals.get("watch_hours_365d")
    rows = {"subscribers": (subs, t["subscribers"], _pct(subs, t["subscribers"]))}
    if "public_uploads_90d" in t:
        rows["public uploads (90 d)"] = (uploads, t["public_uploads_90d"], _pct(uploads, t["public_uploads_90d"]))
    rows["Shorts views (90 d)"] = (sv, t["shorts_views_90d"], _pct(sv, t["shorts_views_90d"]))
    rows["long-form watch hours (365 d)"] = (wh, t["watch_hours_365d"], _pct(wh, t["watch_hours_365d"]))
    base_ok = (subs is not None and subs >= t["subscribers"]
               and ("public_uploads_90d" not in t or (uploads is not None and uploads >= t["public_uploads_90d"])))
    path_sv = sv is not None and sv >= t["shorts_views_90d"]
    path_wh = wh is not None and wh >= t["watch_hours_365d"]
    unknown = [k for k, (have, _, _) in rows.items() if have is None]
    met = base_ok and (path_sv or path_wh)
    if not met and (subs is None or sv is None or wh is None or ("public_uploads_90d" in t and uploads is None)):
        met = None   # cannot tell: a required number was not fetched
    return {"label": t["label"], "rows": rows, "met": met,
            "path": "Shorts views" if path_sv else "watch hours" if path_wh else None, "unknown": unknown}


def audit(ch: str, snapshot: dict | None, originality_risk: int | None, copyright_risk: int | None,
          policy_risk: int | None) -> Result:
    r = Result("monetization_readiness")
    cfg = thresholds()
    prof_name = cfg.get("active_profile", "current")
    prof = cfg["profiles"][prof_name]
    manual = channel_settings(ch)
    totals = (snapshot or {}).get("totals", {}) if snapshot else {}
    r.data.update({"profile": prof_name, "thresholds_checked": cfg.get("last_checked"), "totals": totals,
                   "manual": manual})

    early, full = _tier(prof["early"], totals), _tier(prof["full"], totals)
    r.data["early"], r.data["full"] = early, full
    if "reported_2027" in cfg["profiles"] and prof_name != "reported_2027":
        r.data["full_reported_2027"] = _tier(cfg["profiles"]["reported_2027"]["full"], totals)

    strikes = manual.get("community_guidelines_strikes")
    cstrikes = manual.get("copyright_strikes")
    blockers = []
    if strikes is None:
        r.add("warn", "Community Guidelines strikes: unknown - fill data/growth/channel_status.json from Studio")
    elif strikes > 0:
        blockers.append(f"{strikes} active Community Guidelines strike(s) - YPP needs zero")
    if cstrikes:
        blockers.append(f"{cstrikes} copyright strike(s)")
    for label, v, lim in (("originality (mass-produced) risk", originality_risk, 60),
                          ("copyright risk", copyright_risk, 50), ("policy risk", policy_risk, 50)):
        if v is not None and v >= lim:
            blockers.append(f"{label} {v}/100 - the human YPP review would likely reject this")
    if totals.get("public_uploads_90d") is not None and totals["public_uploads_90d"] < 3:
        blockers.append("fewer than 3 public uploads in 90 days")
    for b in blockers:
        r.add("fix", b)
    if not snapshot:
        r.add("info", f"no channel numbers fetched - run `python growth.py fetch {ch}`")
    elif snapshot.get("mode") != "oauth":
        r.add("info", "public mode: Shorts views (90 d) and watch hours (365 d) need `growth.py auth " + ch + "`")

    # status ladder (manual facts first, never inferred)
    if manual.get("ads_monetized"):
        status = "MONETIZED"
    elif manual.get("application_status") == "pending":
        status = "APPLICATION REVIEW PENDING"
    elif blockers:
        status = "NOT READY"
    elif full["met"]:
        status = "FULL YPP THRESHOLD REACHED"
    elif early["met"]:
        status = "EARLY YPP ELIGIBLE"
    else:
        status = "BUILDING AUDIENCE"
    r.data["status"] = status
    if status in ("EARLY YPP ELIGIBLE", "FULL YPP THRESHOLD REACHED"):
        r.add("info", "threshold reached = you may APPLY (Studio -> Earn). It is not approval; YouTube reviews the "
                      "channel by hand and can refuse (reused / inauthentic content is the main risk here).")
    if manual.get("application_status") == "rejected":
        r.add("warn", "last application was rejected - fix the stated reason before re-applying (30-day wait)")
    if early["met"] and manual.get("early_ypp_member") is None and status not in ("MONETIZED",):
        r.suggest("Early YPP thresholds look met - check Studio -> Earn and apply if you want fan funding.")

    # the gap that matters most
    sv = totals.get("shorts_views_90d")
    if sv is not None and not full["met"]:
        need = prof["full"]["shorts_views_90d"] - sv
        r.suggest(f"Full YPP via Shorts: {need:,.0f} more qualified views in the rolling 90 days "
                  f"(~{need / 90:,.0f}/day sustained).")
    wh = totals.get("watch_hours_365d")
    if wh is not None and not full["met"]:
        r.suggest(f"Full YPP via long-form: {max(0, prof['full']['watch_hours_365d'] - wh):,.0f} more public "
                  f"watch hours in 365 days.")
    r.score = None
    return r
