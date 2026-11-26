"""5. SUBSCRIBER CONVERSION VALIDATOR.

A viewer subscribes when they expect MORE of something specific. Checks: a clear reason to come back (series /
recurring promise), niche consistency with the channel's recent Shorts, recognisable identity, and natural
(not begging) subscribe prompts. With published data it also compares subscribers gained per 1,000 views.
"""

from __future__ import annotations

import re
from collections import Counter
from statistics import median
from typing import Optional

from .base import Result, pillar_of, short_text

BEG = re.compile(r"(subscribe|सब्सक्राइब|सब्स्क्राइब|bell icon|bell dabao|like share|like karo|share karo)",
                 re.IGNORECASE)
SERIES = re.compile(r"(karm aur kripa|part \d|ep(isode)? ?\d|bhag \d|series|next (short|video)|agla (bhag|part))",
                    re.IGNORECASE)
NATURAL = {
    "dr": "Aisi aur chhupi kathaon ke liye Divya Rahasya se jude rahiye.",
    "rs": "Bharat ki aisi aur asli kahaniyon ke liye RealityShift follow karein.",
    "bb": "New puzzle every day - follow Brain Blitz to keep your streak.",
}
WINDOW = 15


def validate(me, others: list, perf: Optional[dict] = None) -> Result:
    r = Result("subscriber_conversion")
    up = me.upload or {}
    ch = me.channel
    recent = [o for o in others if me.order < 0 or 0 <= o.order < me.order][-WINDOW:] or others[-WINDOW:]

    # niche consistency
    mine = pillar_of(ch, short_text(me))
    pc = Counter(pillar_of(ch, short_text(o)) for o in recent)
    r.data.update({"pillar": mine, "recent_pillars": dict(pc)})
    if recent:
        share = pc.get(mine, 0) / len(recent)
        r.data["niche_share"] = round(share, 2)
        if mine == "Other":
            r.add("warn", "does not fit any of the channel's content pillars - viewers who like it may not "
                          "subscribe for the rest")
        elif share < 0.15:
            r.add("warn", f"pillar '{mine}' is rare on this channel ({pc.get(mine, 0)}/{len(recent)} recent) - "
                          f"fine as a test, but it does not build the identity viewers subscribe for")

    # reason to come back
    meta = " ".join([me.topic, me.title, up.get("description", ""), up.get("pinned_comment", ""),
                     " ".join(up.get("tags", [])), str(me.extra.get("SERIES", ""))])
    in_series = bool(SERIES.search(meta))
    r.data["series"] = in_series
    if in_series:
        r.add("ok", "part of a named series - gives a reason to subscribe for the next one")
    else:
        r.suggest("Tie it to a named, recurring series (like 'Karm Aur Kripa') and say what comes next in the "
                  "pinned comment - a reason to return converts better than a request.")

    # prompts: natural, not begging
    spoken = me.spoken_text + " " + me.roman_text
    asks_spoken = len(BEG.findall(spoken))
    asks_meta = len(BEG.findall(up.get("description", "") + " " + up.get("pinned_comment", "")))
    r.data.update({"subscribe_asks_in_video": asks_spoken, "subscribe_asks_in_metadata": asks_meta})
    if asks_spoken > 1 or asks_spoken + asks_meta > 2:
        r.add("warn", f"{asks_spoken + asks_meta} like/subscribe requests - this reads as begging and the "
                      f"loop ending loses its punch")
    if asks_spoken and ch in ("dr", "rs"):
        r.add("warn", "subscribe request inside the narration - rule #13 keeps the ending a loop, not a request")
    if asks_spoken + asks_meta == 0:
        r.suggest(f"One natural line in the description or pinned comment: \"{NATURAL.get(ch, '')}\"")

    # identity: channel name in metadata
    name = {"dr": "divya rahasya", "rs": "realityshift", "bb": "brain blitz"}.get(ch, "")
    if name and name.replace(" ", "") not in meta.lower().replace(" ", ""):
        r.add("warn", f"channel name '{name.title()}' is not in description/tags - weak brand recall")

    # published data
    if perf and me.name in perf:
        m = perf[me.name]
        rates = [p["subs_gained"] / p["views"] * 1000 for p in perf.values()
                 if p.get("subs_gained") is not None and p.get("views")]
        if m.get("subs_gained") is not None and m.get("views") and rates:
            mine_rate = m["subs_gained"] / m["views"] * 1000
            base = median(rates)
            r.data.update({"subs_per_1k_views": round(mine_rate, 2), "channel_median_subs_per_1k": round(base, 2)})
            if base and mine_rate < 0.5 * base:
                r.add("warn", f"converted {mine_rate:.2f} subs per 1k views vs channel median {base:.2f}")
            elif base and mine_rate > 1.5 * base:
                r.add("ok", f"converted {mine_rate:.2f} subs per 1k views - {mine_rate / base:.1f}x the channel "
                            f"median, repeat this format")
    return r.finalize()


def channel_identity(ch: str, shorts: list) -> dict:
    """Share of the last WINDOW Shorts in the channel's top-2 pillars (higher = clearer identity)."""
    recent = shorts[-WINDOW:]
    if not recent:
        return {"identity": None}
    pc = Counter(pillar_of(ch, short_text(s)) for s in recent)
    top2 = sum(n for _, n in pc.most_common(2))
    return {"identity": round(100 * top2 / len(recent)), "pillars": dict(pc), "n": len(recent)}
