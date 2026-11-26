"""Official YouTube Data API v3 + YouTube Analytics API v2 client - READ-ONLY.

Scopes are youtube.readonly + yt-analytics.readonly, so this code cannot upload, edit, publish or delete.
Auth:   python growth.py auth <dr|rs|bb>   (browser login; pick the right brand channel) -> data/growth/auth/<ch>.json
        OAuth client = client_secret.json from the user's analyzer folder ("Desktop/youtube analytics") or
        data/growth/auth/client_secret.json.
Public: without OAuth, the Data API key (YOUTUBE_API_KEY in the analyzer's .env or the environment) reads public
        counts for channel_id in data/growth/channel_status.json.
Quota:  every Data API call is logged to data/growth/quota_log.jsonl; a run stops before passing DAILY_BUDGET units
        (default Data API quota is 10,000/day; search.list costs 100, list calls cost 1).
Missing metrics stay missing: Studio-only numbers (shown in feed, stayed to watch / swiped away, returning
viewers) are NOT in these APIs - import them from a Studio export with `growth.py studio-import`.
"""

from __future__ import annotations

import json
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from statistics import median
from typing import Optional

from .config import ANALYZER_DIR, AUTH, CACHE, QUOTA_LOG, channel_settings, ensure_dirs

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/yt-analytics.readonly"]
DAILY_BUDGET = int(os.environ.get("GROWTH_QUOTA_BUDGET", "3000"))
COST = {"search.list": 100}
IST = timezone(timedelta(hours=5, minutes=30))
# Ordered by importance; if the API rejects one (e.g. engagedViews on an old API version) it is dropped, not faked.
VIDEO_METRICS = ["views", "engagedViews", "estimatedMinutesWatched", "averageViewDuration",
                 "averageViewPercentage", "subscribersGained", "subscribersLost", "likes", "comments", "shares"]


class QuotaExceeded(RuntimeError):
    pass


# ---------------------------------------------------------------------------------------------------------
# quota
# ---------------------------------------------------------------------------------------------------------
def used_today() -> int:
    if not QUOTA_LOG.exists():
        return 0
    today = date.today().isoformat()
    total = 0
    for line in QUOTA_LOG.read_text(encoding="utf-8").splitlines():
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if rec.get("day") == today and rec.get("api") == "data":
            total += rec.get("units", 0)
    return total


def _charge(api: str, method: str, units: int = 1) -> None:
    ensure_dirs()
    if api == "data" and used_today() + units > DAILY_BUDGET:
        raise QuotaExceeded(f"Data API budget {DAILY_BUDGET} units/day reached ({used_today()} used). "
                            f"Raise GROWTH_QUOTA_BUDGET only if you know your project quota.")
    with QUOTA_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"t": datetime.now(IST).isoformat(timespec="seconds"), "day": date.today().isoformat(),
                            "api": api, "method": method, "units": units}) + "\n")


def _exec(req, api: str, method: str):
    _charge(api, method, COST.get(method, 1))
    return req.execute()


# ---------------------------------------------------------------------------------------------------------
# credentials
# ---------------------------------------------------------------------------------------------------------
def api_key() -> Optional[str]:
    if os.environ.get("YOUTUBE_API_KEY"):
        return os.environ["YOUTUBE_API_KEY"]
    env = ANALYZER_DIR / ".env"
    if env.exists():
        try:
            from dotenv import dotenv_values
            v = dotenv_values(env).get("YOUTUBE_API_KEY")
            if v and "your_" not in v:
                return v
        except ImportError:
            pass
    return None


def _client_secret() -> Optional[Path]:
    for p in (AUTH / "client_secret.json", ANALYZER_DIR / "client_secret.json"):
        if p.exists():
            return p
    return None


def token_path(ch: str) -> Path:
    return AUTH / f"{ch}.json"


def credentials(ch: str, interactive: bool = False):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    tp = token_path(ch)
    creds = None
    if tp.exists():
        creds = Credentials.from_authorized_user_file(str(tp), SCOPES)
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                tp.write_text(creds.to_json(), encoding="utf-8")
            except Exception:
                creds = None
    if (not creds or not creds.valid) and interactive:
        from google_auth_oauthlib.flow import InstalledAppFlow
        cs = _client_secret()
        if cs is None:
            raise SystemExit("No OAuth client found. Put client_secret.json (Google Cloud -> Desktop app) in "
                             f"{AUTH} or {ANALYZER_DIR}.")
        flow = InstalledAppFlow.from_client_secrets_file(str(cs), SCOPES)
        # select_account: always show the account/channel picker, so the right channel is chosen every time
        creds = flow.run_local_server(port=0, prompt="select_account consent")
        ensure_dirs()
        tp.write_text(creds.to_json(), encoding="utf-8")
    return creds if creds and creds.valid else None


def authorize(ch: str) -> str:
    creds = credentials(ch, interactive=True)
    from googleapiclient.discovery import build
    yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
    item = _exec(yt.channels().list(part="snippet", mine=True), "data", "channels.list")["items"][0]
    return f"authorized channel: {item['snippet']['title']} ({item['id']}) -> token saved for '{ch}'"


# ---------------------------------------------------------------------------------------------------------
# fetch
# ---------------------------------------------------------------------------------------------------------
def _iso_seconds(d: str) -> int:
    import re
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m:
        return 0
    dd, h, mi, s = (int(x or 0) for x in m.groups())
    return dd * 86400 + h * 3600 + mi * 60 + s


def fetch(ch: str, max_videos: int = 200) -> dict:
    """Pull channel + per-video numbers. Returns (and caches) a snapshot; never writes to YouTube."""
    from googleapiclient.discovery import build
    creds = credentials(ch)
    out: dict = {"channel": ch, "fetched_at": datetime.now(IST).isoformat(timespec="seconds"),
                 "mode": "oauth" if creds else "public", "errors": [], "videos": [], "totals": {}}
    if creds:
        yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
        resp = _exec(yt.channels().list(part="snippet,statistics,contentDetails", mine=True), "data", "channels.list")
    else:
        key, cid = api_key(), channel_settings(ch).get("channel_id")
        if not key or not cid:
            raise SystemExit(f"'{ch}': no OAuth token and no API key/channel_id. Run `python growth.py auth {ch}` "
                             f"(recommended) or set channel_id in data/growth/channel_status.json.")
        yt = build("youtube", "v3", developerKey=key, cache_discovery=False)
        resp = _exec(yt.channels().list(part="snippet,statistics,contentDetails", id=cid), "data", "channels.list")
    if not resp.get("items"):
        raise SystemExit(f"'{ch}': channel not found")
    c = resp["items"][0]
    stats = c.get("statistics", {})
    out["channel_id"] = c["id"]
    out["channel_title"] = c["snippet"]["title"]
    out["channel_published"] = c["snippet"].get("publishedAt", "")[:10]
    out["totals"].update({
        "subscribers": None if stats.get("hiddenSubscriberCount") else int(stats.get("subscriberCount", 0)),
        "subscribers_note": "Data API rounds subscriber counts above 1,000 to 3 significant figures",
        "lifetime_views": int(stats.get("viewCount", 0)),
        "video_count": int(stats.get("videoCount", 0)),
    })

    # uploads playlist -> video details
    uploads = c["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, page = [], None
    while len(ids) < max_videos:
        r = _exec(yt.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=50, pageToken=page),
                  "data", "playlistItems.list")
        ids += [it["contentDetails"]["videoId"] for it in r.get("items", [])]
        page = r.get("nextPageToken")
        if not page:
            break
    vids = {}
    for i in range(0, len(ids), 50):
        r = _exec(yt.videos().list(part="snippet,contentDetails,statistics,status", id=",".join(ids[i:i + 50])),
                  "data", "videos.list")
        for v in r.get("items", []):
            st, sn = v.get("statistics", {}), v["snippet"]
            dur = _iso_seconds(v["contentDetails"].get("duration", ""))
            vids[v["id"]] = {
                "video_id": v["id"], "title": sn.get("title", ""), "published_at": sn.get("publishedAt", ""),
                "duration_s": dur, "privacy": v.get("status", {}).get("privacyStatus"),
                "is_short": dur <= 180, "views": int(st.get("viewCount", 0)),
                "likes": int(st["likeCount"]) if "likeCount" in st else None,
                "comments": int(st["commentCount"]) if "commentCount" in st else None,
            }
    cutoff = (datetime.now(timezone.utc) - timedelta(days=90)).isoformat()
    out["totals"]["public_uploads_90d"] = sum(1 for v in vids.values()
                                              if v["privacy"] == "public" and v["published_at"] >= cutoff)

    if creds:
        _analytics(creds, out, vids)
    else:
        out["errors"].append("public mode: no Analytics API (APV, AVD, subs gained, 90-day Shorts views, watch "
                             "hours). Run `python growth.py auth " + ch + "`.")
    out["videos"] = sorted(vids.values(), key=lambda v: v["published_at"], reverse=True)
    ensure_dirs()
    stamp = datetime.now(IST).strftime("%Y%m%d_%H%M")
    for p in (CACHE / f"{ch}_{stamp}.json", CACHE / f"{ch}_latest.json"):
        p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def _analytics(creds, out: dict, vids: dict) -> None:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    yta = build("youtubeAnalytics", "v2", credentials=creds, cache_discovery=False)
    today = date.today()
    start_all = out.get("channel_published") or "2010-01-01"

    def q(method_label: str, **kw):
        _charge("analytics", method_label)
        return yta.reports().query(ids="channel==MINE", endDate=today.isoformat(), **kw).execute()

    def rows(resp):
        cols = [h["name"] for h in resp.get("columnHeaders", [])]
        return [dict(zip(cols, r)) for r in resp.get("rows", []) or []]

    # per-video lifetime metrics (drop unsupported metrics one by one instead of failing)
    metrics = list(VIDEO_METRICS)
    while metrics:
        try:
            resp = q("video_metrics", startDate=start_all, dimensions="video", metrics=",".join(metrics),
                     sort="-views", maxResults=200)
            break
        except HttpError as e:
            bad = next((m for m in metrics[1:] if m in str(e)), metrics[-1] if len(metrics) > 1 else None)
            out["errors"].append(f"Analytics rejected metric '{bad}': dropped (not estimated)")
            if bad is None:
                resp = None
                break
            metrics.remove(bad)
    else:
        resp = None
    names = {"engagedViews": "engaged_views", "estimatedMinutesWatched": "minutes_watched",
             "averageViewDuration": "avd_s", "averageViewPercentage": "apv", "subscribersGained": "subs_gained",
             "subscribersLost": "subs_lost", "views": "views_analytics", "likes": "likes_analytics",
             "comments": "comments_analytics", "shares": "shares"}
    for r in rows(resp) if resp else []:
        v = vids.get(r["video"])
        if v is not None:
            for k, val in r.items():
                if k != "video":
                    v[names.get(k, k)] = val

    # 90-day Shorts views + 365-day long-form watch hours (YPP paths)
    try:
        resp = q("shorts_90d", startDate=(today - timedelta(days=89)).isoformat(), dimensions="creatorContentType",
                 metrics="views,engagedViews")
        by = {str(r["creatorContentType"]).lower(): r for r in rows(resp)}
        sh = [r for t, r in by.items() if "short" in t]
        out["totals"]["shorts_views_90d"] = sum(int(r["views"]) for r in sh)
        out["totals"]["shorts_engaged_views_90d"] = sum(int(r.get("engagedViews", 0)) for r in sh)
    except Exception as e:
        out["errors"].append(f"90-day Shorts views: {e}")
    try:
        resp = q("watch_365d", startDate=(today - timedelta(days=364)).isoformat(), dimensions="creatorContentType",
                 metrics="estimatedMinutesWatched")
        mins = sum(int(r["estimatedMinutesWatched"]) for r in rows(resp)
                   if "short" not in str(r["creatorContentType"]).lower())
        out["totals"]["watch_hours_365d"] = round(mins / 60, 1)
    except Exception as e:
        out["errors"].append(f"365-day watch hours: {e}")
    try:
        resp = q("subs_daily", startDate=(today - timedelta(days=89)).isoformat(), dimensions="day",
                 metrics="views,subscribersGained,subscribersLost", sort="day")
        out["daily_90d"] = [{"day": r["day"], "views": int(r["views"]), "subs_gained": int(r["subscribersGained"]),
                             "subs_lost": int(r["subscribersLost"])} for r in rows(resp)]
    except Exception as e:
        out["errors"].append(f"daily trend: {e}")
    out["totals"]["analytics_note"] = ("Analytics counts ALL views/watch time; YPP counts only valid PUBLIC views "
                                       "and (for watch hours) excludes Shorts. Studio -> Earn is authoritative.")


def market(query: str, max_results: int = 15) -> dict:
    """Real competition snapshot for a topic query: top YouTube Shorts results + their public view counts.
    Costs ~101 Data API units. This is NOT search volume; it shows what already ranks and how fresh it is."""
    from googleapiclient.discovery import build
    key = api_key()
    if not key:
        raise SystemExit("market needs YOUTUBE_API_KEY (analyzer .env or environment)")
    yt = build("youtube", "v3", developerKey=key, cache_discovery=False)
    r = _exec(yt.search().list(q=query, part="id", type="video", videoDuration="short", maxResults=max_results,
                               relevanceLanguage="hi", order="relevance"), "data", "search.list")
    ids = [it["id"]["videoId"] for it in r.get("items", [])]
    if not ids:
        return {"query": query, "results": 0}
    v = _exec(yt.videos().list(part="snippet,statistics", id=",".join(ids)), "data", "videos.list")
    now = datetime.now(timezone.utc)
    rows = []
    for it in v.get("items", []):
        pub = datetime.fromisoformat(it["snippet"]["publishedAt"].replace("Z", "+00:00"))
        rows.append({"title": it["snippet"]["title"], "channel": it["snippet"]["channelTitle"],
                     "views": int(it["statistics"].get("viewCount", 0)), "age_days": (now - pub).days})
    views = [x["views"] for x in rows]
    return {"query": query, "fetched": date.today().isoformat(), "results": len(rows),
            "median_views": median(views) if views else None, "max_views": max(views) if views else None,
            "recent_30d": sum(1 for x in rows if x["age_days"] <= 30),
            "top": sorted(rows, key=lambda x: -x["views"])[:5]}


def latest(ch: str) -> Optional[dict]:
    p = CACHE / f"{ch}_latest.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None
