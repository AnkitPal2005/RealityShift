# Growth & Monetization Readiness System

Read-only advisor for all three channels (`dr` Divya Rahasya, `rs` RealityShift, `bb` Brain Blitz).
It never uploads, edits, publishes or deletes; every decision is advice for the human who publishes.

## Commands (run from `story-pipeline/`)

| Command | What it does |
|---|---|
| `python growth.py video dr kanha_chai` | 5 pre-publish validators (+ performance if published) and a decision |
| `python growth.py dashboard all` | master dashboard from cached data -> `data/growth/reports/dashboard_latest.md` |
| `python growth.py dashboard all --fetch` | fetch fresh API numbers first |
| `python growth.py auth dr` | one-time Google login per channel (read-only scopes; pick the right brand channel) |
| `python growth.py fetch dr` | Data API + Analytics API pull into `data/growth/analytics_cache/` |
| `python growth.py studio-import dr export.csv` | Studio-only numbers (Stayed to watch, Shown in feed, Returning viewers) |
| `python growth.py market dr "barbarik ki kahani"` | real top-15 search results + view counts for a topic (~101 quota units) |
| `python growth.py assets` | scan `assets/` folders into the licence ledger |
| `python growth.py quota` | Data API units used today (budget: `GROWTH_QUOTA_BUDGET`, default 3000) |

Every new render also gets `<stem>_growth.md` next to its upload kit (hook in `core/upload_kit.py`, never blocks).

## Validators

1. **topic_demand**: overuse of a mega name or pillar, duplicate topics, debate question, demand from your OWN results and optional search snapshot. No search volume is ever estimated.
2. **originality**: script phrase overlap (all channels), channel boilerplate, hook/closing repeats, beat-structure twins, Lego template and music repeats. Channel-level "mass-produced" risk.
3. **copyright_policy**: outside media and the licence ledger, Community Guidelines words (from each channel's `core/policy.py` + extras), fiction labels and sources, synthetic-media disclosure, advertiser suitability. It never certifies clearance.
4. **title_metadata**: title curiosity/length, title words and numbers backed by the video, description, hashtag relevance, language rules (BB = English only).
5. **subscriber_conversion**: series/return reason, niche fit, channel name in metadata, natural vs begging prompts, subs per 1k views vs baseline.
6. **performance**: per-Short vs the channel's own 48 h+ median; pattern groups (length, title style, pillar, mega name, slot). n<3 = weak signal, never a recommendation.
7. **readiness**: Early YPP and full YPP progress shown separately (thresholds in `data/growth/ypp_thresholds.json`). Status: NOT READY / BUILDING AUDIENCE / EARLY YPP ELIGIBLE / FULL YPP THRESHOLD REACHED / APPLICATION REVIEW PENDING / MONETIZED. The last two come only from `channel_status.json`. Threshold reached is not approval.

Decision per video: any block -> **REJECTED**, any fix -> **NEEDS REVISION**, only warnings -> **APPROVED WITH IMPROVEMENTS**, else **APPROVED**.

## Files you fill by hand (`data/growth/`)

- `channel_status.json`: strikes, application status, monetized flag (not in any API). `null` = unknown.
- `asset_ledger.json`: owner/licence/proof for every logo, sound and image.
- `video_map.json` (optional): `{"rs:marut": "VIDEO_ID"}` when automatic title matching misses a Short.
- `ypp_thresholds.json`: confirm against YouTube's official page; the reported 2027 bar is marked unverified.

## What the APIs cannot give

Shown in feed, Stayed to watch / Swiped away and Returning viewers are Studio-only, so use `studio-import`.
Analytics views and watch time include non-public views; YPP counts valid public ones, so Studio -> Earn is authoritative.
