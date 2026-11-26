"""Growth & monetization readiness system - command line.

  python growth.py video dr hanuman_cycle          7 validators + decision for one Short (pre- or post-publish)
  python growth.py dashboard [dr|rs|bb|all]         master dashboard (Markdown + JSON) from cached data
  python growth.py dashboard all --fetch            fetch fresh API numbers first, then build the dashboard
  python growth.py auth dr                          one-time Google login per channel (read-only scopes)
  python growth.py fetch dr                         pull Data + Analytics API numbers into the cache
  python growth.py studio-import dr export.csv      add Studio-only numbers (stayed to watch, shown in feed...)
  python growth.py market dr "barbarik ki kahani"   real competition snapshot for a topic (~101 quota units)
  python growth.py assets                           scan assets/ folders into the licence ledger
  python growth.py quota                            Data API units used today

Codes: dr = Divya Rahasya, rs = RealityShift, bb = Brain Blitz.
Reports land in data/growth/reports/ (latest dashboard: data/growth/reports/dashboard_latest.md).
Read-only: nothing here uploads, edits, publishes or deletes videos.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from growth import inventory, report, store, youtube_api   # noqa: E402
from growth.config import CHANNELS                           # noqa: E402
from growth.validators import copyright_policy               # noqa: E402


def _channels(arg: str) -> list[str]:
    if arg == "all":
        return list(CHANNELS)
    if arg not in CHANNELS:
        raise SystemExit(f"channel must be one of {', '.join(CHANNELS)} or all")
    return [arg]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("video")
    v.add_argument("channel")
    v.add_argument("name")
    v.add_argument("--market", help="also fetch a YouTube search snapshot for this query (~101 units)")
    v.add_argument("--json", action="store_true", help="print the JSON report instead of Markdown")
    d = sub.add_parser("dashboard")
    d.add_argument("channel", nargs="?", default="all")
    d.add_argument("--fetch", action="store_true")
    for c in ("auth", "fetch"):
        p = sub.add_parser(c)
        p.add_argument("channel")
    s = sub.add_parser("studio-import")
    s.add_argument("channel")
    s.add_argument("csv")
    m = sub.add_parser("market")
    m.add_argument("channel")
    m.add_argument("query")
    sub.add_parser("assets")
    sub.add_parser("quota")
    a = ap.parse_args()

    if a.cmd == "video":
        mk = youtube_api.market(a.market) if a.market else None
        rep = report.run_video(a.channel, a.name.removesuffix(".py"), market=mk)
        me = next(s for s in inventory.load_channel(a.channel) if s.name == rep["name"])
        paths = report.save_video(rep, next_to=me.mp4)
        print(json.dumps(rep, ensure_ascii=False, indent=1) if a.json else report.video_markdown(rep))
        print("saved:", *[str(p) for p in paths], sep="\n  ")
    elif a.cmd == "dashboard":
        chs = _channels(a.channel)
        if a.fetch:
            for ch in chs:
                try:
                    youtube_api.fetch(ch)
                except SystemExit as e:
                    print(f"[{ch}] fetch skipped: {e}")
        allsh = inventory.load_all()
        dashes = [report.run_channel(ch, allsh) for ch in chs]
        paths = report.save_dashboard(dashes)
        print(report.dashboard_markdown(dashes))
        print("saved:", *[str(p) for p in paths], sep="\n  ")
    elif a.cmd == "auth":
        print(youtube_api.authorize(_channels(a.channel)[0]))
    elif a.cmd == "fetch":
        out = youtube_api.fetch(_channels(a.channel)[0])
        print(f"{out['channel_title']}: {len(out['videos'])} videos, mode={out['mode']}")
        print(json.dumps(out["totals"], indent=1))
        for e in out["errors"]:
            print("  gap:", e)
    elif a.cmd == "studio-import":
        print(store.studio_import(_channels(a.channel)[0], Path(a.csv)))
    elif a.cmd == "market":
        print(json.dumps(youtube_api.market(a.query), ensure_ascii=False, indent=1))
    elif a.cmd == "assets":
        res = copyright_policy.scan_assets()
        print(f"{len(res['ledger']['assets'])} assets in ledger, {len(res['added'])} new (licence 'unknown' until "
              f"you fill them): data/growth/asset_ledger.json")
        for x in res["added"]:
            print("  +", x)
    elif a.cmd == "quota":
        print(f"Data API units used today: {youtube_api.used_today()} / budget {youtube_api.DAILY_BUDGET}")


if __name__ == "__main__":
    main()
