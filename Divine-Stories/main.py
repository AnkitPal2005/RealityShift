"""Divine Stories: topic -> script -> assets -> voice -> music/SFX -> render -> thumbnail -> QC -> upload package.

Fully local + free: no paid APIs, no keys. Network is used only for edge-tts and Wikimedia Commons downloads.

  python main.py new --slug shiva_tandav --topic "..." [--template mystery_reveal] [--characters shiva]
  python main.py validate story/library/shiva_neelkanth.json
  python main.py search "Ravi Varma Krishna"           # licence-filtered Commons search
  python main.py assets   <story.json>                  # download + record licences/attribution (cached)
  python main.py voice    <story.json>                  # edge-tts per scene (cached)
  python main.py stills   <story.json>                  # contact sheet of composed frames for review
  python main.py render   <story.json> [--workers N]    # audio mix + video
  python main.py thumb    <story.json>
  python main.py qc       <story.json>
  python main.py package  <story.json>
  python main.py all      <story.json>                  # everything above in order
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from config import settings as S
from generators.log import log


def _story(path: str, strict=True) -> tuple[dict, Path]:
    from story import schema

    p = Path(path)
    if not p.exists():
        p = S.STORY_LIBRARY / f"{path}.json"
    story = schema.load(p, strict_duration=strict)
    for w in schema.validate(story, strict_duration=strict):
        log("story", f"warning: {w}")
    return story, p


def _paths(story: dict) -> dict[str, Path]:
    out = S.story_out(story["slug"])
    return {"video": out / f"{story['slug']}.mp4", "audio": S.story_temp(story["slug"]) / "mix.wav",
            "cover": out / f"{story['slug']}_cover.png", "timeline": out / "timeline.json",
            "qc": out / "qc_report.json", "info": out / "render_info.json", "srt": out / "captions.srt"}


def cmd_assets(story):
    from generators import commons

    titles = sorted({s["visual"]["asset"] for s in story["scenes"]})
    got = commons.ensure(titles)
    missing = [t for t in titles if t not in got]
    if missing:
        raise SystemExit(f"assets not available or not licence-approved: {missing}")
    log("assets", f"{len(got)} assets ready (licences + attribution in assets/manifest.json)")


def cmd_timeline(story):
    from audio.mix import build_timeline
    from voice import tts

    tl = build_timeline(story, tts.story_voice(story))
    _paths(story)["timeline"].write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
    total = tl[-1]["start"] + tl[-1]["dur"]
    log("voice", f"timeline {total:.2f}s over {len(tl)} scenes")
    if not S.MIN_DURATION <= total <= S.MAX_DURATION:
        raise SystemExit(f"narration timeline {total:.1f}s is outside {S.MIN_DURATION}-{S.MAX_DURATION}s: edit the script")
    return tl


def cmd_render(story, path, workers=None):
    from audio.mix import mix
    from compositor import render
    from qc import ypp_gate
    from upload.package import write_srt

    ypp_gate.check(story)          # YPP reused/repetitive/misleading-content gate: blocks before any work
    tl = cmd_timeline(story)
    P = _paths(story)
    t0 = time.time()
    info = mix(story, tl, P["audio"])
    log("audio", f"mixed {info['total']:.2f}s, {len(info['sfx'])} SFX cues ({time.time() - t0:.0f}s)")
    t0 = time.time()
    render.render(path, tl, P["audio"], P["video"], workers)
    log("render", f"{P['video'].name} in {time.time() - t0:.0f}s")
    write_srt(tl, story, P["srt"])
    P["info"].write_text(json.dumps({"slug": story["slug"], "assets": sorted({s["visual"]["asset"] for s in story["scenes"]}),
                                     "template": story.get("template"), "rendered": time.strftime("%Y-%m-%d %H:%M"),
                                     "sfx": info["sfx"]}, ensure_ascii=False, indent=1), encoding="utf-8")
    return tl


def cmd_thumb(story):
    from thumbnails import cover

    r = cover.build(story, _paths(story)["cover"])
    log("thumb", f"cover from {r['asset']}: {r['headline']}")


def cmd_qc(story):
    from qc import checks

    P = _paths(story)
    tl = json.loads(P["timeline"].read_text(encoding="utf-8"))
    res = checks.run(story, tl, P["video"])
    P["qc"].write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    for r in res["results"]:
        log("qc", f"{r['status']:<4} {r['check']}" + (f"  ({r['detail']})" if r["detail"] else ""))
    log("qc", "PASSED" if res["ok"] else "REJECTED")
    return res


def cmd_package(story, qc=None):
    from upload import package

    P = _paths(story)
    qc = qc or json.loads(P["qc"].read_text(encoding="utf-8"))
    if not qc["ok"]:
        raise SystemExit("QC failed: output rejected, no upload package built")
    out = package.build(story, P["video"], P["cover"], qc)
    shutil_copy = P["srt"]
    if shutil_copy.exists():
        (out / "captions.srt").write_bytes(shutil_copy.read_bytes())
    log("package", f"upload package: {out}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Divine Stories Shorts pipeline")
    ap.add_argument("cmd", choices=["new", "validate", "search", "assets", "voice", "stills", "render", "thumb", "qc",
                                    "package", "all"])
    ap.add_argument("target", nargs="?")
    ap.add_argument("--slug")
    ap.add_argument("--topic")
    ap.add_argument("--template", default="mystery_reveal")
    ap.add_argument("--characters", default="")
    ap.add_argument("--workers", type=int)
    a = ap.parse_args(argv)

    if a.cmd == "new":
        from story.templates import scaffold

        p = scaffold(a.slug, a.topic, a.template, [c for c in a.characters.split(",") if c])
        print(f"created {p} - fill in narration, sources, claims and visuals, then run: python main.py validate {p}")
        return
    if a.cmd == "search":
        from generators.commons import search

        for x in search(a.target, limit=40):
            print(f"{x.width}x{x.height}  {x.license:<12} {x.title}  | {x.artist[:60]}")
        return
    story, path = _story(a.target, strict=a.cmd != "validate")
    if a.cmd == "validate":
        from qc import ypp_gate
        from story import schema

        print(f"OK - {len(story['scenes'])} scenes, ~{schema.estimate_seconds(story):.1f}s estimated")
        problems, warnings = ypp_gate.evaluate(story)
        for w in warnings:
            print(f"[ypp] WARNING: {w}")
        print("[ypp] would BLOCK the render:\n  - " + "\n  - ".join(problems) if problems else "[ypp] gate: OK")
        return
    if a.cmd == "assets":
        cmd_assets(story)
    elif a.cmd == "voice":
        cmd_timeline(story)
    elif a.cmd == "stills":
        from compositor import render

        tl = cmd_timeline(story)
        out = render.stills(story, tl, [x["start"] + x["dur"] * 0.6 for x in tl], _paths(story)["video"].with_name("stills.png"))
        log("stills", str(out))
    elif a.cmd == "render":
        cmd_render(story, path, a.workers)
    elif a.cmd == "thumb":
        cmd_thumb(story)
    elif a.cmd == "qc":
        cmd_qc(story)
    elif a.cmd == "package":
        cmd_package(story)
    elif a.cmd == "all":
        cmd_assets(story)
        cmd_render(story, path, a.workers)
        cmd_thumb(story)
        res = cmd_qc(story)
        if not res["ok"]:
            sys.exit(1)
        cmd_package(story, res)


if __name__ == "__main__":
    main()
