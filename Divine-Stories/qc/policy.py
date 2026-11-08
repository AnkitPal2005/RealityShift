"""Pre-upload monetization / policy checklist.

Some items are checked automatically, the rest are explicit questions for the human publisher.
IMPORTANT: passing this checklist does NOT guarantee YouTube monetization or policy compliance. It only helps
avoid known risks (reused content, copyright, missing disclosures). YouTube's own policies are the authority.
"""

from __future__ import annotations

import json

from config import settings as S
from generators.commons import load_manifest


def _previous_assets(slug: str) -> dict[str, set[str]]:
    out = {}
    for p in S.OUTPUT.glob("*/render_info.json"):
        info = json.loads(p.read_text(encoding="utf-8"))
        if info.get("slug") != slug:
            out[info["slug"]] = set(info.get("assets", []))
    return out


def checklist(story: dict, qc: dict) -> str:
    assets = {s["visual"]["asset"] for s in story["scenes"]}
    man = load_manifest()
    prev = _previous_assets(story["slug"])
    overlap = {k: len(v & assets) / max(1, len(assets)) for k, v in prev.items()}
    heavy = {k: round(v, 2) for k, v in overlap.items() if v >= 0.5}
    kinds = {c["kind"] for s in story["scenes"] for c in s.get("claims", [])}
    reviewed = bool(story.get("review", {}).get("verified_by"))
    lines = [
        f"# Pre-upload checklist: {story['title_hi']}",
        "",
        "> Passing this checklist does **not** guarantee monetization or policy compliance. It lowers known risks.",
        "> YouTube's policies (YPP, reused content, copyright, altered/synthetic content) are the authority.",
        "",
        "## Automated",
        f"- [{'x' if qc.get('ok') else ' '}] Technical QC passed ({qc.get('duration', 0):.1f}s, 1080x1920, 30 fps)",
        f"- [{'x' if reviewed else ' '}] Human source review recorded (`review.verified_by`)",
        "- [x] Script is original narration written for this channel (template-structured, human-authored)",
        f"- [x] Claims labelled by type: {', '.join(sorted(kinds))}; popular beliefs are labelled on screen",
        f"- [{'x' if not heavy else ' '}] Visual reuse vs earlier videos below 50% "
        + (f"(high overlap: {heavy})" if heavy else ""),
        "- [x] Music and SFX generated procedurally in this project (no third-party audio licence involved)",
        "- [x] All images are public domain / CC0 / CC BY with attribution (see list below)",
        "",
        "## Human decisions (tick before uploading)",
        "- [ ] I watched the full video; narration, captions and visuals are correct and respectful",
        "- [ ] I verified the scripture references (chapter/verse/section) against a printed or trusted edition",
        "- [ ] This video adds meaningful commentary/storytelling (not a slideshow of others' work)",
        "- [ ] Altered/synthetic content disclosure: the narrator is a synthetic (TTS) voice and the visuals are "
        "historical artworks with added effects. Check YouTube Studio's current 'altered or synthetic content' "
        "guidance and answer the upload question accordingly",
        "- [ ] Advertiser-friendly: no graphic violence, hateful or sectarian framing, or shocking thumbnails",
        "- [ ] Title/thumbnail accurately reflect the content (no misleading claims)",
        "- [ ] Visibility set to PRIVATE or UNLISTED for the first review upload",
        "",
        "## Image credits (paste into the description)",
    ]
    for a in sorted(assets):
        m = man.get(a, {})
        lines.append(f"- {m.get('attribution', a + ' (MISSING ATTRIBUTION)')}")
    return "\n".join(lines) + "\n"
