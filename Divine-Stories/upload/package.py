"""Manual-upload package for YouTube Studio. Nothing is uploaded automatically and no credentials are used.

output/<slug>/upload/
    <slug>.mp4            final video
    <slug>_cover.png      Shorts cover (+ _feed_preview.png)
    metadata.md           title options, description (with sources + credits), tags, hashtags, settings
    checklist.md          pre-upload policy checklist (human ticks)
    qc_report.json        machine QC results
    READY or NOT_READY    status marker
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from config import settings as S
from generators.commons import load_manifest
from qc import policy
from story.schema import KIND_LABEL_HI


def description(story: dict) -> str:
    man = load_manifest()
    up = story.get("upload", {})
    # the first two lines show above "more" and are what search reads first: keep the search terms there
    lines = list(up.get("intro", [story["title_hi"]])) + ["", up.get("summary", story["topic"]), ""]
    if up.get("question"):
        lines += [up["question"], ""]
    lines += ["📜 स्रोत (Sources):"]
    for s in story["sources"]:
        lines.append(f"• [{KIND_LABEL_HI[s['kind']]}] {s['work']}: {s['ref']}" + (f" {s['url']}" if s.get("url") else ""))
    lines += ["", "जो बातें लोक मान्यता हैं, उन्हें वीडियो में अलग से 'लोक मान्यता' लिखा गया है।", "",
              "🎨 Image credits:"]
    for a in sorted({sc["visual"]["asset"] for sc in story["scenes"]}):
        lines.append(f"• {man[a]['attribution']}")
    lines += ["", "Music & sound design: original, generated for this channel.",
              "Narration: synthetic Hindi voice (text-to-speech).", "",
              " ".join(up.get("hashtags", ["#Shorts"]))]
    return "\n".join(lines)


TAG_LIMIT, MAX_TAGS, DESC_LIMIT, TITLE_LIMIT, SHOWN_HASHTAGS = 500, 15, 5000, 100, 3


def _latin_words(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9']+", s.lower()))


def metadata_checks(story: dict, title: str, duration: float) -> list[tuple[bool, str, str]]:
    """Same metadata rules as Reality Shift's upload kit (YouTube limits + search fold + policy words)."""
    from qc.ypp_gate import CLICKBAIT, OFF_PLATFORM

    up = story.get("upload", {})
    rows = [(len(title) <= TITLE_LIMIT, "title length", f"{len(title)}/{TITLE_LIMIT} chars")]
    thumb_n = len(up.get("thumb_text", "").split())
    rows.append((0 < thumb_n <= 3, "thumbnail words", f"{thumb_n} (max 3)"))
    tags = up.get("tags", [])
    tags_len = sum(len(t) for t in tags) + 2 * max(0, len(tags) - 1)
    rows.append((tags_len <= TAG_LIMIT and 0 < len(tags) <= MAX_TAGS, "tags",
                 f"{len(tags)} tags, {tags_len}/{TAG_LIMIT} chars"))
    desc = description(story)
    rows.append((len(desc) <= DESC_LIMIT, "description length", f"{len(desc)}/{DESC_LIMIT} chars"))
    hashtags = up.get("hashtags", [])
    rows.append(("#Shorts" in hashtags[:SHOWN_HASHTAGS] and len(hashtags) <= SHOWN_HASHTAGS, "hashtags",
                 f"{' '.join(hashtags)} (#Shorts + max {SHOWN_HASHTAGS})"))
    fold = title + " " + " ".join(desc.splitlines()[:2])
    for q in up.get("queries", []):
        miss = _latin_words(q) - _latin_words(fold)
        rows.append((not miss, f'query "{q}"', "in title + first 2 lines" if not miss else f"missing {', '.join(sorted(miss))}"))
    meta = " ".join([title, up.get("thumb_text", ""), desc, " ".join(tags)])
    off = OFF_PLATFORM.search(meta)
    rows.append((not off, "off-platform CTA", off.group(0) if off else "none"))
    bait = sorted({m.group(0) for m in CLICKBAIT.finditer(meta)})
    rows.append((not bait, "clickbait words", ", ".join(bait) if bait else "none"))
    rows.append((duration <= 60, "Shorts length", f"{duration:.1f}s"))
    return rows


def build(story: dict, video: Path, cover: Path, qc: dict) -> Path:
    out = S.story_out(story["slug"]) / "upload"
    out.mkdir(parents=True, exist_ok=True)
    for marker in ("READY", "NOT_READY"):
        (out / marker).unlink(missing_ok=True)
    shutil.copy2(video, out / video.name)
    shutil.copy2(cover, out / cover.name)
    prev = Path(str(cover).replace(".png", "_feed_preview.png"))
    if prev.exists():
        shutil.copy2(prev, out / prev.name)
    up = story.get("upload", {})
    titles = up.get("titles", [story["title_hi"]])
    rows = metadata_checks(story, titles[0], qc.get("duration", 0.0))
    passed = sum(ok for ok, _, _ in rows)
    md = [f"# Upload metadata: {story['slug']}", "",
          f"**Metadata checks: {passed}/{len(rows)} passed** (same rules as the Reality Shift upload kit). "
          "Titles are not auto-scored: no title scorer is installed, so no title number is shown.", "",
          f"**Recommended visibility:** {S.DEFAULT_VISIBILITY.upper()} (switch to public only after the checklist)",
          "**Audience:** not made for kids · **Category:** Education (or Entertainment)",
          "**Language:** Hindi · **Captions:** burned in (also upload `captions.srt` if you want CC)", "",
          "## Title (pick #1; others are alternatives)"] + [f"{i + 1}. {t}  ({len(t)} chars)" for i, t in enumerate(titles)]
    md += ["", f"**Thumbnail text:** {up.get('thumb_text', '')}", "", "## Description", "```", description(story), "```",
           "", "## Tags (paste as-is)", ", ".join(up.get("tags", [])), "", "## Hashtags (already at the end of the description)",
           " ".join(up.get("hashtags", ["#Shorts"])), "", "## Checks", "", "| | Check | Detail |", "|---|---|---|"]
    md += [f"| {'OK' if ok else 'FIX'} | {label} | {detail} |" for ok, label, detail in rows]
    md += ["", "## Scheduling", "Upload as Private, then set a schedule in YouTube Studio (target: 5 Shorts/week).", ""]
    (out / "metadata.md").write_text("\n".join(md), encoding="utf-8")
    (out / "checklist.md").write_text(policy.checklist(story, qc), encoding="utf-8")
    (out / "qc_report.json").write_text(json.dumps(qc, ensure_ascii=False, indent=2), encoding="utf-8")
    ready = qc.get("ok") and bool(story.get("review", {}).get("verified_by"))
    (out / ("READY" if ready else "NOT_READY")).write_text(
        "QC passed and human review recorded.\n" if ready else
        "Not ready: " + ("QC failed. " if not qc.get("ok") else "") +
        ("Human source review missing (story review.verified_by). " if not story.get("review", {}).get("verified_by") else "")
        + "\n", encoding="utf-8")
    return out


def write_srt(timeline: list[dict], story: dict, path: Path) -> None:
    from compositor.captions import align_tokens, chunk

    def ts(x):
        h, m = int(x // 3600), int(x % 3600 // 60)
        return f"{h:02d}:{m:02d}:{x % 60:06.3f}".replace(".", ",")

    n, lines = 1, []
    for sc, tl in zip(story["scenes"], timeline):
        for c in chunk(align_tokens(sc["narration"], tl["words"]), tl["start"] + tl["dur"]):
            end = min(c["end"], c["words"][-1]["t"] + c["words"][-1].get("d", 0.4) + 0.4)
            lines += [str(n), f"{ts(c['start'])} --> {ts(end)}", " ".join(w["disp"] for w in c["words"]), ""]
            n += 1
    path.write_text("\n".join(lines), encoding="utf-8")
