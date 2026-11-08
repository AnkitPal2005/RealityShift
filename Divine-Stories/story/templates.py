"""Local narrative templates (no runtime LLM).

A template is an ordered list of beats with guidance. `scaffold()` turns a topic into a skeleton story JSON
that a human fills in: narration, sources, claims and visual choices. `validate()` (story/schema.py) then
enforces the channel rules before anything is rendered.
"""

from __future__ import annotations

import json
from pathlib import Path

from config import settings as S

TEMPLATES: dict[str, list[tuple[str, str]]] = {
    # beat, guidance for the writer
    "mystery_reveal": [
        ("hook", "2-3 s. A striking image or question. No context yet."),
        ("setup", "Who/where. Name the scripture or tradition early."),
        ("setup", "The situation in one vivid line."),
        ("rising", "Complication: something goes wrong."),
        ("rising", "Stakes grow: the danger becomes universal."),
        ("rising", "Characters turn to the hero."),
        ("climax", "The decisive act (cite the source in narration)."),
        ("reveal", "The name / meaning that comes from the act."),
        ("tradition", "A regional tradition or popular interpretation, clearly labelled as such."),
        ("meaning", "What it means today - one line."),
        ("question", "Ask the audience a specific question + CTA."),
    ],
    "lesser_known_fact": [
        ("hook", "A surprising claim the video will justify."),
        ("setup", "Context: which text, which character."),
        ("setup", "What most people believe."),
        ("rising", "What the text actually says (quote/paraphrase with reference)."),
        ("rising", "Detail 1."),
        ("rising", "Detail 2."),
        ("reveal", "The twist / why it matters."),
        ("tradition", "How regional traditions differ."),
        ("question", "Question + CTA."),
    ],
    "teaching": [
        ("hook", "A life problem the teaching answers."),
        ("setup", "The scene in the text (e.g. Kurukshetra, Gita ch. X)."),
        ("rising", "The doubt / question asked."),
        ("rising", "The teaching, part 1."),
        ("rising", "The teaching, part 2."),
        ("climax", "The key verse idea (with reference)."),
        ("meaning", "Practical meaning today."),
        ("meaning", "One-line takeaway."),
        ("question", "Question + CTA."),
    ],
}


def scaffold(slug: str, topic: str, template: str = "mystery_reveal", characters: list[str] | None = None) -> Path:
    if template not in TEMPLATES:
        raise ValueError(f"unknown template {template}; choose from {sorted(TEMPLATES)}")
    story = {
        "slug": slug,
        "topic": topic,
        "template": template,
        "title_hi": "TODO: हिंदी शीर्षक",
        "characters": characters or [],
        "sources": [{"id": "src1", "work": "TODO", "ref": "TODO chapter/verse", "kind": "scripture",
                     "url": "", "note": ""}],
        "scenes": [
            {"id": f"s{i + 1:02d}", "beat": beat, "guidance": guide, "narration": "", "highlight": [],
             "label": "", "claims": [], "pause_after": 0.35,
             "visual": {"asset": "", "character": None, "focus": [0.5, 0.5], "zoom": [1.0, 1.12], "pan": [0, 0],
                        "grade": "cinematic", "effects": ["dust"]},
             "sfx": []}
            for i, (beat, guide) in enumerate(TEMPLATES[template])
        ],
        "upload": {"titles": [], "tags": [], "hashtags": ["#Shorts"]},
        "review": {"verified_by": "", "verified_on": "", "notes": ""},
    }
    S.STORY_LIBRARY.mkdir(parents=True, exist_ok=True)
    path = S.STORY_LIBRARY / f"{slug}.json"
    if path.exists():
        raise FileExistsError(f"{path} already exists - not overwriting")
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
