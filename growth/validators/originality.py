"""2. ORIGINALITY VALIDATOR (YPP 'inauthentic / reused content').

Compares one Short with the channel's earlier Shorts on four layers:
  script    - 4-word phrase overlap with any other Short (any channel), and channel boilerplate phrases
  hook      - same opening words / near-identical first line as a recent Short; copied closing line
  structure - same beat pattern (tone sequence + scene count) as recent Shorts
  visual    - same Lego template combination / music style + tempo as recent Shorts
and gives a channel-level 'mass-production' risk from how alike the last Shorts are to each other.
These are similarity measures, not a ruling by YouTube; a human still judges the creative value.
"""

from __future__ import annotations

from collections import Counter
from difflib import SequenceMatcher
from itertools import combinations
from statistics import mean

from ..text import containment, jaccard, shingles, words
from .base import Result

SCRIPT_BLOCK = 0.25      # same limit as policy.py MAX_OVERLAP
SCRIPT_WARN = 0.12
HOOK_WORDS = 4
HOOK_LOOKBACK = 5
STRUCT_LOOKBACK = 5
STRUCT_SIM = 0.85
BOILERPLATE_SHARE = 0.3  # a 4-gram in >= this share of the channel's Shorts is template text
LEGO_LOOKBACK = 10


def _w(s):
    return words(s.spoken_text)


def _first_line(s):
    return set(words(s.narration_hi[0])) if s.narration_hi else set()


def _last_line(s):
    return words(" ".join(s.narration_hi[-2:]))[-6:] if s.narration_hi else []


def structure_sim(a, b) -> float:
    if not a.tones or not b.tones:
        return 0.0
    seq = SequenceMatcher(None, a.tones, b.tones).ratio()
    same_len = 1.0 if len(a.scene_keys) == len(b.scene_keys) else 0.85
    return seq * same_len


def pair_similarity(a, b) -> float:
    """0-1 blend of script, hook, structure and template likeness between two Shorts."""
    sa, sb = shingles(_w(a)), shingles(_w(b))
    script = max(containment(sa, sb), containment(sb, sa))
    hook = jaccard(_first_line(a), _first_line(b))
    struct = structure_sim(a, b)
    lego = 0.0
    if a.lego and b.lego:
        keys = set(a.lego) | set(b.lego)
        lego = sum(a.lego.get(k) == b.lego.get(k) for k in keys) / len(keys)
    music = 1.0 if (a.music_style and a.music_style == b.music_style) else 0.0
    return 0.35 * script + 0.15 * hook + 0.25 * struct + 0.15 * lego + 0.10 * music


def validate(me, others: list, all_channels: list | None = None) -> Result:
    r = Result("originality")
    if not me.narration_hi and me.channel != "bb":
        r.add("warn", "no narration found in the module (SPEC/SCRIPT) - script originality not checked")
    prior = [o for o in others if me.order < 0 or 0 <= o.order < me.order] or others
    recent = prior[-STRUCT_LOOKBACK:]

    # --- script copy (every channel) --------------------------------------------------------------
    mine = shingles(_w(me))
    worst, worst_name = 0.0, None
    for o in (all_channels or others):
        if o.key == me.key or not o.narration_hi:
            continue
        c = containment(mine, shingles(_w(o)))
        if c > worst:
            worst, worst_name = c, o.key
    r.data["max_script_overlap"] = round(worst, 3)
    if worst > SCRIPT_BLOCK:
        r.add("block", f"{worst:.0%} of this script's phrases are in '{worst_name}' - rewrite, don't reword")
    elif worst > SCRIPT_WARN:
        r.add("warn", f"{worst:.0%} phrase overlap with '{worst_name}' - make the wording fresher")

    # --- channel boilerplate (phrases most Shorts share) ------------------------------------------
    counts = Counter(g for o in others for g in shingles(_w(o)))
    n_other = max(len([o for o in others if o.narration_hi]), 1)
    boiler = {g for g, c in counts.items() if c / n_other >= BOILERPLATE_SHARE}
    share = containment(mine, boiler)
    r.data["boilerplate_share"] = round(share, 3)
    if share > 0.15:
        r.add("warn", f"{share:.0%} of the script is phrases used in most of the channel's Shorts (template text)")

    # --- hook / closing ---------------------------------------------------------------------------
    head = _w(me)[:HOOK_WORDS]
    for o in prior[-HOOK_LOOKBACK:]:
        if head and _w(o)[:HOOK_WORDS] == head:
            r.add("fix", f"opens with the same {HOOK_WORDS} words as '{o.name}': \"{' '.join(head)}\"")
        elif jaccard(_first_line(me), _first_line(o)) >= 0.6:
            r.add("warn", f"first line is near-identical to '{o.name}'")
        if _last_line(me) and _last_line(me) == _last_line(o):
            r.add("warn", f"same closing line as '{o.name}'")

    # --- structure ---------------------------------------------------------------------------------
    sims = [(structure_sim(me, o), o.name) for o in recent]
    alike = [n for s, n in sims if s >= STRUCT_SIM]
    r.data["structure_twins"] = alike
    if len(alike) >= 3:
        r.add("fix", f"same beat pattern (tones + scene count) as {len(alike)} of the last {len(recent)} Shorts: "
                     f"{', '.join(alike)} - change the story shape (POV, order, ending device)")
    elif alike:
        r.add("warn", f"beat pattern close to {', '.join(alike)}")

    # --- visual template + music -------------------------------------------------------------------
    if me.lego:
        for o in prior[-LEGO_LOOKBACK:]:
            if o.lego == me.lego:
                r.add("fix", f"identical Lego template combination to '{o.name}'")
    if prior and me.music_style and prior[-1].music_style == me.music_style and me.music_bpm and prior[-1].music_bpm \
            and abs(me.music_bpm - prior[-1].music_bpm) < 6:
        r.add("warn", f"same music style and tempo as the previous Short ('{prior[-1].name}')")

    if not [f for f in r.findings if f["level"] in ("warn", "fix", "block")]:
        r.add("ok", "script, hook, structure and template all differ from recent Shorts")
    r.suggest("Originality value comes from the research, the story angle and your own pinned-comment replies - "
              "keep each Short's angle something viewers cannot get from the last one.")
    return r.finalize()


def channel_risk(shorts: list, window: int = 10) -> dict:
    """0-100 'mass-produced' risk: mean pairwise likeness of the last `window` Shorts (100 = all the same)."""
    recent = [s for s in shorts if s.narration_hi or s.tones][-window:]
    if len(recent) < 3:
        return {"risk": None, "n": len(recent), "note": "need 3+ Shorts"}
    pairs = [pair_similarity(a, b) for a, b in combinations(recent, 2)]
    avg = mean(pairs)
    # Calibrated so ordinary same-channel likeness (same voice, same subtitle style) sits low.
    risk = max(0, min(100, round((avg - 0.08) / 0.35 * 100)))
    return {"risk": risk, "n": len(recent), "mean_pair_similarity": round(avg, 3),
            "most_alike": sorted(((round(pair_similarity(a, b), 2), a.name, b.name)
                                  for a, b in combinations(recent, 2)), reverse=True)[:3]}
