"""Upload kit: title/thumbnail scoring, description, tags and a drawn thumbnail for a finished Short.

Usage:
  python upload_kit.py generate_chickens_neck_short      # after the Short is rendered

A story opts in by defining UPLOAD = {"titles": [...10 candidates...], "thumb_text": "MAX 3 WORDS",
"queries": [...3 searches it should win...], "description": "...", "tags": [...], "hashtags": [...]}
and thumbnail(ctx) that draws the 1080x1920 cover. An optional UPLOAD["title"] (the creator's pick)
ships instead of the top-ranked candidate. Writes output/shorts/<OUTPUT stem>_upload.md and
<OUTPUT stem>_thumb.png (plus a feed-size preview), and prints the scores.
Titles are scored by the yt-package skill's title.py; the rest by YouTube's published limits.
"""

import importlib
import importlib.util
import json
import re
import sys
from pathlib import Path

import cairo

import engine
import policy

TITLE_PY = [Path.home() / ".claude/skills/yt-package/title.py",
            engine.ROOT.parent / ".claude/skills/yt-package/title.py"]
TAG_LIMIT = 500        # YouTube: total characters across all tags
MAX_TAGS = 15          # yt-seo: past this it's stuffing
DESC_LIMIT = 5000
SHOWN_HASHTAGS = 3     # the first three show above the title
SHORTS_MAX = 180       # YouTube counts uploads up to 3 minutes as Shorts


def title_checker():
    path = next((p for p in TITLE_PY if p.exists()), None)
    if path is None:
        raise SystemExit("yt-package/title.py not found; install the yt-* skills first")
    spec = importlib.util.spec_from_file_location("yt_title", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.check


def words(s):
    return set(re.findall(r"[a-z0-9']+", s.lower()))


def metadata_checks(up, title, duration, name):
    """(ok, label, detail) rows for everything except the title score."""
    rows = []
    thumb_n = len(up["thumb_text"].split())
    rows.append((thumb_n <= 3, "thumbnail words", f"{thumb_n} (max 3)"))
    tags_len = sum(len(t) for t in up["tags"]) + 2 * (len(up["tags"]) - 1)
    rows.append((tags_len <= TAG_LIMIT and len(up["tags"]) <= MAX_TAGS, "tags",
                 f"{len(up['tags'])} tags, {tags_len}/{TAG_LIMIT} chars"))
    desc = up["description"].strip() + "\n\n" + " ".join(up["hashtags"])
    rows.append((len(desc) <= DESC_LIMIT, "description length", f"{len(desc)}/{DESC_LIMIT} chars"))
    rows.append(("#Shorts" in up["hashtags"][:SHOWN_HASHTAGS] and len(up["hashtags"]) <= SHOWN_HASHTAGS, "hashtags",
                 f"{' '.join(up['hashtags'])} (#Shorts + max {SHOWN_HASHTAGS})"))
    fold = title + " " + " ".join(up["description"].strip().splitlines()[:2])
    for q in up["queries"]:
        miss = words(q) - words(fold)
        rows.append((not miss, f'query "{q}"', "in title + first 2 lines" if not miss
                     else f"missing {', '.join(sorted(miss))}"))
    meta = " ".join([title, up["thumb_text"], up["description"], " ".join(up["tags"])])
    off = policy.OFF_PLATFORM.search(meta)
    rows.append((not off, "off-platform CTA", off.group(0) if off else "none"))
    bait = sorted({m.group(0) for m in policy.CLICKBAIT.finditer(meta)})
    rows.append((not bait, "clickbait words", ", ".join(bait) if bait else "none"))
    harsh = sorted({m.group(0) for rx in (policy.GRAPHIC, policy.DEROGATORY) for m in rx.finditer(meta)})
    rows.append((not harsh, "ad-safe wording", ", ".join(harsh) if harsh else "no graphic/derogatory words"))
    rows.append((duration <= SHORTS_MAX, "Shorts length", f"{duration:.1f}s (max {SHORTS_MAX}s)"))
    clash = [(n, t) for n, t in policy.load_history().get("titles", {}).items() if n != name and similar(title, t)]
    rows.append((not clash, "title vs past titles", "unique" if not clash
                 else f'too close to {clash[0][0]}: "{clash[0][1]}"'))
    return rows


TITLE_STOP = {"ka", "ki", "ke", "hai", "me", "mein", "se", "ko", "kya", "kyun", "aur", "the", "a", "of", "in", "vs"}


def similar(a, b):
    """Same opening frame (first 3 words) or half the meaningful words shared: reads as one title template."""
    wa, wb = re.findall(r"[a-z0-9']+", a.lower()), re.findall(r"[a-z0-9']+", b.lower())
    if wa[:3] == wb[:3]:
        return True
    ka, kb = set(wa) - TITLE_STOP, set(wb) - TITLE_STOP
    return bool(ka and kb) and len(ka & kb) >= max(2, min(len(ka), len(kb)) // 2)


def remember_title(name, title):
    """Keep each Short's chosen title in policy_history.json so the next kit can't reuse its frame."""
    history = policy.load_history()
    history.setdefault("titles", {})[name] = title
    policy.HISTORY.write_text(json.dumps(history, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render_thumbnail(story, out: Path) -> Path:
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, engine.W, engine.H)
    story.thumbnail(cairo.Context(surf))
    surf.write_to_png(str(out))
    small = cairo.ImageSurface(cairo.FORMAT_ARGB32, 180, 320)  # roughly its size in the Shorts shelf
    ctx = cairo.Context(small)
    ctx.scale(180 / engine.W, 320 / engine.H)
    ctx.set_source_surface(surf)
    ctx.get_source().set_filter(cairo.FILTER_GOOD)
    ctx.paint()
    small.write_to_png(str(out.with_name(out.stem + "_feed.png")))
    return out


def build(story, final: Path, duration: float) -> Path:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
    up = story.UPLOAD
    check = title_checker()
    topic = words(story.TOPIC)

    def rank(r):  # title.py caps at 100, so ties go to: names the topic, wins more queries, fewer issues, shorter
        tw = words(r["title"])
        return (-r["score"], -len(topic & tw), -sum(words(q) <= tw for q in up["queries"]), len(r["issues"]),
                r["chars"])

    ranked = sorted((check(t, up["thumb_text"]) for t in up["titles"]), key=rank)
    if up.get("title"):  # the creator picked a title: it ships, the ranking stays in the kit for comparison
        best = check(up["title"], up["thumb_text"])
        ranked = [best] + [r for r in ranked if r["title"] != best["title"]]
    else:
        best = ranked[0]
    name = story.__name__.split(".")[-1]
    rows = metadata_checks(up, best["title"], duration, name)
    passed = sum(ok for ok, *_ in rows)
    overall = round(0.6 * best["score"] + 40 * passed / len(rows))
    thumb = render_thumbnail(story, final.with_name(final.stem + "_thumb.png"))

    md = [f"# Upload kit — {story.TOPIC}", "",
          f"**Overall score: {overall}/100** (title {best['score']}/100 x 0.6 + metadata {passed}/{len(rows)} x 40)", "",
          "## Title", "", "```", best["title"], "```", "",
          "| # | Title | Chars | Score | Issues |", "|---|---|---|---|---|"]
    for k, r in enumerate(ranked[:3], 1):
        issues = "; ".join(f"{a}: {b}" for a, b in r["issues"]) or "none"
        md.append(f"| {k} | {r['title']} | {r['chars']} | {r['score']} | {issues} |")
    md += ["", "## Thumbnail", "", f"Text: **{up['thumb_text']}**  ", f"File: `{thumb.name}` (1080x1920; feed preview "
           f"`{thumb.stem}_feed.png`)  ", "Upload it in the YouTube app: Short -> Edit -> Thumbnail.", "",
           "## Description", "", "```", up["description"].strip(), "", " ".join(up["hashtags"]), "```", "",
           "## Tags", "", "```", ", ".join(up["tags"]), "```", "", "## Checks", "",
           "| | Check | Result |", "|---|---|---|"]
    md += [f"| {'OK' if ok else 'FIX'} | {label} | {detail} |" for ok, label, detail in rows]
    md += ["", "Ship it, or change it?", ""]
    path = final.with_name(final.stem + "_upload.md")
    path.write_text("\n".join(md), encoding="utf-8")
    remember_title(name, best["title"])

    print(f"[upload] overall {overall}/100 - best title ({best['score']}/100): {best['title']}")
    for ok, label, detail in rows:
        print(f"         {'ok ' if ok else 'FIX'} {label}: {detail}")
    print(f"[upload] {path}\n[upload] {thumb}")
    return path


def main() -> None:
    name = sys.argv[1].removesuffix(".py")
    try:
        story = importlib.import_module(name)
    except ModuleNotFoundError:
        story = importlib.import_module(f"stories.{name}")
    final = engine.shorts_dir(story) / (story.OUTPUTS.get("edge") or story.OUTPUTS["silent"])
    if not final.exists():
        raise SystemExit(f"render {name} first: {final} is missing")
    scenes = json.loads(final.with_suffix(".json").read_text(encoding="utf-8"))
    build(story, final, scenes[-1]["end"])


if __name__ == "__main__":
    main()
