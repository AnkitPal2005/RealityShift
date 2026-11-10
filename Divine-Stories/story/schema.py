"""Story JSON schema + validation.

A story is authored offline (by a human, optionally helped by a dev assistant) from a template in
story/templates.py. Nothing here calls an LLM. Validation enforces the channel rules:
  - 8-12 scenes, first beat is a hook, last beat ends with a question / CTA
  - estimated narration 40-60 s
  - every factual claim has a kind (scripture | regional_tradition | popular_interpretation)
    and at least one source id that exists in the story's source list
  - every scene names a visual asset and (if it shows a deity) the character profile id
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CLAIM_KINDS = ("scripture", "regional_tradition", "popular_interpretation")
KIND_LABEL_HI = {"scripture": "शास्त्र", "regional_tradition": "क्षेत्रीय परंपरा", "popular_interpretation": "लोक मान्यता"}
EFFECTS = {"dust", "embers", "sparks", "fog", "clouds", "rays", "lightning", "energy_wave", "poison_smoke",
           "throat_glow", "ocean_mist", "rain_light", "rain"}
GRADES = {"cinematic", "night", "poison", "divine", "warm", "cold"}
WORDS_PER_SEC = 2.45   # measured after pause capping: hi-IN-MadhurNeural, -4% rate, -6Hz (pre-TTS estimate only)


class StoryError(ValueError):
    pass


def load(path: str | Path, strict_duration: bool = True) -> dict:
    story = json.loads(Path(path).read_text(encoding="utf-8"))
    validate(story, strict_duration=strict_duration)
    return story


def words(text: str) -> list[str]:
    return [w for w in re.split(r"\s+", text.replace("...", " ").replace("…", " ")) if w.strip("।,.?!—-")]


def estimate_seconds(story: dict) -> float:
    n = sum(len(words(s["narration"])) for s in story["scenes"])
    pauses = sum(s.get("pause_after", 0.35) for s in story["scenes"])
    return n / WORDS_PER_SEC + pauses


def validate(story: dict, strict_duration: bool = True) -> list[str]:
    """Raise StoryError on hard failures; return a list of warnings."""
    errs, warns = [], []
    for key in ("slug", "title_hi", "topic", "scenes", "sources", "characters"):
        if key not in story:
            errs.append(f"missing top-level key: {key}")
    if errs:
        raise StoryError("; ".join(errs))
    if not re.fullmatch(r"[a-z0-9_]+", story["slug"]):
        errs.append("slug must be lowercase a-z0-9_")
    scenes = story["scenes"]
    if not 8 <= len(scenes) <= 12:
        errs.append(f"need 8-12 scenes, got {len(scenes)}")
    if scenes and scenes[0].get("beat") != "hook":
        errs.append("first scene beat must be 'hook'")
    if scenes and scenes[-1].get("beat") not in ("question", "conclusion"):
        errs.append("last scene beat must be 'question' or 'conclusion'")
    if scenes and len(words(scenes[0]["narration"])) > 9:
        warns.append("hook is longer than ~9 words (aim for a 2-3 second hook)")
    src_ids = {s["id"] for s in story["sources"]}
    for s in story["sources"]:
        if s.get("kind") not in CLAIM_KINDS:
            errs.append(f"source {s.get('id')}: kind must be one of {CLAIM_KINDS}")
        for k in ("work", "ref"):
            if not s.get(k):
                errs.append(f"source {s.get('id')}: missing {k}")
    chars = set(story["characters"])
    seen_ids = set()
    for i, sc in enumerate(scenes):
        tag = sc.get("id", f"#{i}")
        if tag in seen_ids:
            errs.append(f"duplicate scene id {tag}")
        seen_ids.add(tag)
        if not sc.get("narration", "").strip():
            errs.append(f"{tag}: empty narration")
        v = sc.get("visual") or {}
        if not v.get("asset"):
            errs.append(f"{tag}: visual.asset missing")
        if v.get("grade", "cinematic") not in GRADES:
            errs.append(f"{tag}: unknown grade {v.get('grade')}")
        bad = set(v.get("effects", [])) - EFFECTS
        if bad:
            errs.append(f"{tag}: unknown effects {sorted(bad)}")
        if v.get("character") and v["character"] not in chars:
            errs.append(f"{tag}: character {v['character']} not listed in story.characters")
        for c in sc.get("claims", []):
            if c.get("kind") not in CLAIM_KINDS:
                errs.append(f"{tag}: claim kind must be one of {CLAIM_KINDS}")
            if not c.get("sources"):
                errs.append(f"{tag}: claim without sources: {c.get('text', '')[:40]}")
            for sid in c.get("sources", []):
                if sid not in src_ids:
                    errs.append(f"{tag}: unknown source id {sid}")
        for w in sc.get("highlight", []):
            if w not in sc.get("narration", ""):
                warns.append(f"{tag}: highlight word '{w}' not in narration")
    est = estimate_seconds(story)
    if strict_duration and not 38 <= est <= 62:
        errs.append(f"estimated duration {est:.1f}s outside 40-60s (before TTS)")
    if not story.get("review", {}).get("verified_by"):
        warns.append("no human source review yet (review.verified_by is empty) - upload package will be marked NOT READY")
    if errs:
        raise StoryError("; ".join(errs))
    return warns
