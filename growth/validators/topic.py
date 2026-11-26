"""1. TOPIC DEMAND VALIDATOR.

Demand is judged ONLY from real signals:
  - this channel's own published results for related topics (Analytics/Data API, when fetched)
  - optional YouTube search results for the topic query (real view counts of real videos, `growth.py market`)
  - how often the channel has already used this subject (overuse)
No search volume or trend number is ever estimated. When no data exists, the result says so.
"""

from __future__ import annotations

from collections import Counter
from statistics import median
from typing import Optional

from ..text import content_words, jaccard
from .base import Result, deities_in, pillar_of, short_text

RECENT = 10          # look-back window for overuse
OVERUSE_WARN = 4     # same mega name in this many of the last RECENT Shorts
OVERUSE_FIX = 6
DUP_TOPIC = 0.6      # topic-word jaccard that counts as the same topic
MIN_N = 3            # below this a group is a weak signal


def _subject_words(s) -> set[str]:
    return content_words(s.topic + " " + s.title) - {"karm", "kripa", "shorts", "rahasya", "katha"}


def validate(me, others: list, perf: Optional[dict] = None, market: Optional[dict] = None) -> Result:
    r = Result("topic_demand")
    ch = me.channel
    prior = [o for o in others if o.order < me.order or me.order < 0][-RECENT:] if others else []
    subj = _subject_words(me)
    my_deities = deities_in(short_text(me))
    pillar = pillar_of(ch, short_text(me))
    r.data.update({"subject_words": sorted(subj)[:15], "mega_names": my_deities, "pillar": pillar,
                   "demand_basis": []})

    # --- duplicate / overused subject -------------------------------------------------------------
    for o in others:
        j = jaccard(subj, _subject_words(o))
        if j >= DUP_TOPIC:
            r.add("block", f"same topic as '{o.name}' (topic-word overlap {j:.0%}) - YouTube treats re-uploads "
                           f"of a topic as reused content")
    dcount = Counter(d for o in prior for d in deities_in(short_text(o)))
    for d in my_deities:
        n = dcount.get(d, 0)
        if n >= OVERUSE_FIX:
            r.add("fix", f"{d} appears in {n} of the last {len(prior)} Shorts - overused, viewers see a repeat")
        elif n >= OVERUSE_WARN:
            r.add("warn", f"{d} appears in {n} of the last {len(prior)} Shorts - rotate the mega name soon")
    pcount = Counter(pillar_of(ch, short_text(o)) for o in prior)
    r.data["recent_pillars"] = dict(pcount)

    # --- AGENTS.md rules: mega name + debate question ---------------------------------------------
    if ch == "dr" and not my_deities:
        r.add("warn", "no mega name (Krishna / Ram / Hanuman / Shiv...) in topic, title or script - rule #8")
    up = me.upload or {}
    q_text = " ".join([me.title, up.get("pinned_comment", "") or up.get("pinned", "")])
    if ch in ("dr", "rs") and "?" not in q_text and " ya " not in f" {q_text.lower()} ":
        r.add("warn", "no two-sided question in title or pinned comment - debate rule #3 drives comments")

    # --- demand from this channel's own results ---------------------------------------------------
    if perf:
        views_all = [m["views"] for m in perf.values() if m.get("views") is not None]
        if views_all:
            ch_med = median(views_all)
            r.data["channel_median_views"] = ch_med
            for d in my_deities:
                vs = [perf[o.name]["views"] for o in others if o.name in perf and d in deities_in(short_text(o))
                      and perf[o.name].get("views") is not None]
                if vs:
                    med = median(vs)
                    weak = " (weak signal)" if len(vs) < MIN_N else ""
                    r.data["demand_basis"].append(f"{d}: median {med:,.0f} views over {len(vs)} Shorts vs channel "
                                                  f"median {ch_med:,.0f}{weak}")
                    if len(vs) >= MIN_N and med < 0.6 * ch_med:
                        r.add("warn", f"{d} Shorts have under-performed on this channel (median {med:,.0f} vs "
                                      f"{ch_med:,.0f}, n={len(vs)})")
            pv = [perf[o.name]["views"] for o in others if o.name in perf
                  and pillar_of(ch, short_text(o)) == pillar and perf[o.name].get("views") is not None]
            if pv:
                r.data["demand_basis"].append(f"pillar '{pillar}': median {median(pv):,.0f} views over {len(pv)} "
                                              f"Shorts{' (weak signal)' if len(pv) < MIN_N else ''}")
            # alternatives: mega names that did well here and are not overused right now
            ranked = []
            for d in {d for o in others for d in deities_in(short_text(o))}:
                vs = [perf[o.name]["views"] for o in others if o.name in perf and d in deities_in(short_text(o))
                      and perf[o.name].get("views") is not None]
                if len(vs) >= MIN_N and d not in my_deities and dcount.get(d, 0) < OVERUSE_WARN:
                    ranked.append((median(vs), d, len(vs)))
            for med, d, n in sorted(ranked, reverse=True)[:3]:
                if med > ch_med:
                    r.suggest(f"Stronger angle from your own data: a little-known {d} story (median {med:,.0f} "
                              f"views, n={n}, used {dcount.get(d, 0)}x in the last {len(prior)}).")
    if market:
        r.data["market"] = market
        mv = market.get("median_views")
        r.data["demand_basis"].append(
            f"YouTube search '{market['query']}' ({market.get('fetched', '?')}): {market['results']} results read, "
            f"median views {f'{mv:,.0f}' if mv is not None else 'n/a'}, {market.get('recent_30d', 0)} uploaded in "
            f"the last 30 days")
        if market.get("recent_30d", 0) >= 8:
            r.add("warn", f"crowded: {market['recent_30d']} of the top {market['results']} results for "
                          f"'{market['query']}' are under 30 days old - pick a less-told angle")
    if not r.data["demand_basis"]:
        r.add("info", "no demand data yet: run `python growth.py fetch " + ch + "` (own results) or "
                      "`python growth.py market " + ch + " \"<query>\"` (search results). No estimate is made.")

    # pillar rotation hint (AGENTS.md #9 mix)
    if pcount and pcount.most_common(1)[0][0] == pillar and pcount[pillar] >= 0.7 * len(prior) and len(prior) >= 6:
        others_p = [p for p in pcount if p != pillar] or ["another pillar"]
        r.suggest(f"{pcount[pillar]} of the last {len(prior)} Shorts are '{pillar}'. Mix in {', '.join(others_p)}.")
    return r.finalize()
