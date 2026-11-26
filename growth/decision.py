"""FINAL DECISION SYSTEM - per video.

  REJECTED                    any 'block' finding (copied script, same topic, downloaded media, hate words)
  NEEDS REVISION              any 'fix' finding (misleading title, unlabelled fiction, unlicensed asset...)
  APPROVED WITH IMPROVEMENTS  only 'warn' findings
  APPROVED                    nothing to fix

The decision is advice for the human who publishes. Nothing here uploads, schedules or deletes a video.
"""

from __future__ import annotations

from statistics import mean

from .validators.base import LEVELS, Result

DECISIONS = ["APPROVED", "APPROVED WITH IMPROVEMENTS", "NEEDS REVISION", "REJECTED"]
GATING = ("topic_demand", "originality", "copyright_policy", "title_metadata", "subscriber_conversion")


def decide(results: list[Result]) -> dict:
    gate = [r for r in results if r.validator in GATING]
    worst = max((LEVELS.index(r.worst) for r in gate), default=0)
    decision = ("REJECTED" if worst >= LEVELS.index("block") else "NEEDS REVISION" if worst >= LEVELS.index("fix")
                else "APPROVED WITH IMPROVEMENTS" if worst >= LEVELS.index("warn") else "APPROVED")
    scored = [r.score for r in gate if r.score is not None]
    reasons = [f"[{r.validator}] {f['msg']}" for r in gate for f in r.findings if f["level"] in ("block", "fix")]
    improve = [f"[{r.validator}] {f['msg']}" for r in gate for f in r.findings if f["level"] == "warn"]
    return {"decision": decision, "score": round(mean(scored)) if scored else None, "must_fix": reasons,
            "improve": improve, "human_control": "Advice only - publishing stays your decision in YouTube Studio."}
