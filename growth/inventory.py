"""Read every Short the pipeline knows about, per channel, without importing (or rendering) the modules.

Story modules are parsed with `ast`: top-level literals (TOPIC, SOURCES, UPLOAD, MUSIC_*, LEGO, ...) are read
with literal_eval, and the narration is every ("हिंदी", "ROMAN") string pair inside SPEC/SCRIPT, in source order.
Render order + shipped titles come from <channel>/data/policy_history.json; duration and audit from output/.
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .config import CHANNELS
from .text import is_devanagari

LITERALS = ("TOPIC", "SOURCES", "UPLOAD", "MUSIC_STYLE", "MUSIC_BPM", "LEGO", "OUTPUTS", "CHANNEL", "NAME", "STYLE",
            "BEAT_NO", "SERIES", "LABEL")

MEDIA_PATTERNS = [
    r"\.(mp4|mov|mkv|webm|avi|gif|png|jpe?g|webp|mp3|wav|m4a|aac|ogg|flac)\b",
    r"\b(VideoFileClip|ImageClip|ImageSequenceClip|AudioFileClip|create_from_png|cv2\.imread|Image\.open)\b",
    r"\b(yt_dlp|youtube_dl|pytube|urlopen|requests\.get|httpx\.get|wget)\b",
]
# Files the engines write themselves (clips, mixes, renders, previews) are not outside media.
GENERATED = re.compile(r'(scene_\{|_l\{|master_audio\.wav|\.mp3"\)|OUTPUTS\s*=|^Output:|"\.json"|mp3_44100|'
                       r'audio\.wav|narrator\.mp3|kikivoice|_thumb|thumbnail\.png|p\d\d_|preview|OUT\b|os\.path\.join\(OUT|'
                       r'output/|usage:|\.cache)',
                       re.IGNORECASE)


@dataclass
class Short:
    name: str
    channel: str
    path: Path
    order: int                                  # position in render history (-1 = not rendered via the gate)
    topic: str = ""
    sources: list = field(default_factory=list)
    upload: dict = field(default_factory=dict)
    music_style: Optional[str] = None
    music_bpm: Optional[float] = None
    lego: Optional[dict] = None
    scene_keys: list = field(default_factory=list)
    tones: list = field(default_factory=list)
    narration_hi: list = field(default_factory=list)      # spoken chunks (Devanagari)
    narration_roman: list = field(default_factory=list)   # on-screen subtitle chunks (Roman)
    media_refs: list = field(default_factory=list)        # (line_no, text) of outside-media references
    shipped_title: Optional[str] = None
    mp4: Optional[Path] = None
    duration: Optional[float] = None
    audit: Optional[dict] = None
    extra: dict = field(default_factory=dict)

    @property
    def spoken_text(self) -> str:
        return " ".join(self.narration_hi)

    @property
    def roman_text(self) -> str:
        return " ".join(self.narration_roman)

    @property
    def title(self) -> str:
        return self.shipped_title or self.upload.get("title") or (self.upload.get("titles") or [""])[0]

    @property
    def key(self) -> str:
        return f"{self.channel}:{self.name}"


def _literal(node):
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def _ordered(nodes):
    return sorted(nodes, key=lambda n: (getattr(n, "lineno", 0), getattr(n, "col_offset", 0)))


def _narration(node) -> tuple[list, list, list, list]:
    """(hindi chunks, roman chunks, scene keys, tones) from a SPEC / SCRIPT AST node."""
    pairs, keys, tones = [], [], []
    for n in _ordered([n for n in ast.walk(node) if isinstance(n, (ast.Tuple, ast.Dict))]):
        if isinstance(n, ast.Dict):
            for k, v in zip(n.keys, n.values):
                if isinstance(k, ast.Constant) and k.value == "key" and isinstance(v, ast.Constant):
                    keys.append(str(v.value))
            continue
        el = n.elts
        if (len(el) == 2 and all(isinstance(e, ast.Constant) and isinstance(e.value, str) for e in el)
                and is_devanagari(el[0].value)):
            pairs.append((el[0].value, el[1].value))
        elif (len(el) >= 2 and isinstance(el[0], ast.Constant) and isinstance(el[0].value, str)
              and re.fullmatch(r"[a-z_]{2,12}", el[0].value) and isinstance(el[1], (ast.List, ast.Tuple))):
            tones.append(el[0].value)
    return [p[0] for p in pairs], [p[1] for p in pairs], keys, tones


def parse_module(path: Path) -> dict:
    src = path.read_text(encoding="utf-8", errors="replace")
    out: dict = {"src": src}
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        out["error"] = f"syntax error: {e}"
        return out
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for t in node.targets:
            if not isinstance(t, ast.Name):
                continue
            if t.id in LITERALS:
                out[t.id] = _literal(node.value)
            if t.id in ("SPEC", "SCRIPT") and "narration" not in out:
                hi, ro, keys, tones = _narration(node.value)
                if hi:
                    out["narration"] = (hi, ro, keys, tones)
    refs = []
    for i, line in enumerate(src.splitlines(), 1):
        s = line.strip()
        if s.startswith("#") or GENERATED.search(s):
            continue
        if any(re.search(p, s, re.IGNORECASE) for p in MEDIA_PATTERNS):
            refs.append((i, s[:140]))
    out["media_refs"] = refs
    return out


def _history(root: Path) -> dict:
    p = root / "data" / "policy_history.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"order": [], "titles": {}}


def _outputs(root: Path, name: str, outputs) -> tuple[Optional[Path], Optional[float], Optional[dict]]:
    shorts = root / "output" / "shorts"
    cands = []
    if isinstance(outputs, dict):
        cands += [shorts / v for v in outputs.values() if isinstance(v, str)]
    cands += [shorts / f"{name}_short.mp4", shorts / f"{name}.mp4", root / "output" / name / f"{name}.mp4"]
    mp4 = next((c for c in cands if c.exists()), None)
    dur, audit = None, None
    if mp4:
        meta = mp4.with_suffix(".json")
        if meta.exists():
            try:
                scenes = json.loads(meta.read_text(encoding="utf-8"))
                if isinstance(scenes, list) and scenes and "end" in scenes[-1]:
                    dur = float(scenes[-1]["end"])
                elif isinstance(scenes, list) and scenes and "dur" in scenes[-1]:
                    dur = float(scenes[-1]["start"]) + float(scenes[-1]["dur"])
            except Exception:
                pass
        a = mp4.with_name(mp4.stem + "_audit.json")
        if a.exists():
            try:
                audit = json.loads(a.read_text(encoding="utf-8"))
                dur = dur or audit.get("details", {}).get("duration_s")
            except Exception:
                pass
    return mp4, dur, audit


def _module_files(ch: str) -> list[Path]:
    cfg = CHANNELS[ch]
    d = cfg["root"] / cfg["modules"]
    files = [p for p in d.glob("*.py") if not p.stem.startswith("_")]
    if ch == "bb":   # puzzle modules only, not the shared engine files
        files = [p for p in files if re.match(r"(lanes_\d+|spot_diff_\d+)", p.stem)]
    return files


def load_channel(ch: str) -> list[Short]:
    cfg = CHANNELS[ch]
    hist = _history(cfg["root"])
    order = {n: i for i, n in enumerate(hist.get("order", []))}
    titles = hist.get("titles", {})
    shorts = []
    for p in _module_files(ch):
        m = parse_module(p)
        hi, ro, keys, tones = m.get("narration", ([], [], [], []))
        upload = m.get("UPLOAD") if isinstance(m.get("UPLOAD"), dict) else {}
        mp4, dur, audit = _outputs(cfg["root"], p.stem, m.get("OUTPUTS"))
        bpm = m.get("MUSIC_BPM")
        s = Short(name=p.stem, channel=ch, path=p, order=order.get(p.stem, -1),
                  topic=str(m.get("TOPIC") or m.get("NAME") or p.stem), sources=m.get("SOURCES") or [],
                  upload=upload, music_style=m.get("MUSIC_STYLE") or m.get("STYLE"),
                  music_bpm=float(bpm) if isinstance(bpm, (int, float)) else None,
                  lego=m.get("LEGO") if isinstance(m.get("LEGO"), dict) else None,
                  scene_keys=keys, tones=tones, narration_hi=hi, narration_roman=ro,
                  media_refs=m.get("media_refs", []), shipped_title=titles.get(p.stem), mp4=mp4, duration=dur,
                  audit=audit, extra={k: m.get(k) for k in ("BEAT_NO", "SERIES", "LABEL") if m.get(k) is not None})
        if "error" in m:
            s.extra["parse_error"] = m["error"]
        if ch == "bb" and mp4 is None:
            out = cfg["root"] / "output" / p.stem
            s.mp4 = next(iter(sorted(out.glob("*.mp4"))), None) if out.exists() else None
        shorts.append(s)
    # render order first (gate history), then everything else by file time
    shorts.sort(key=lambda s: (s.order if s.order >= 0 else 10_000, s.path.stat().st_mtime))
    return shorts


def find(ch: str, name: str) -> tuple[Short, list[Short]]:
    """The Short + every Short of the same channel rendered BEFORE it (the comparison set)."""
    allc = load_channel(ch)
    me = next((s for s in allc if s.name == name.removesuffix(".py")), None)
    if me is None:
        raise SystemExit(f"no module '{name}' in {CHANNELS[ch]['root'] / CHANNELS[ch]['modules']}")
    others = [s for s in allc if s.name != me.name]
    return me, others


def load_all() -> dict[str, list[Short]]:
    return {ch: load_channel(ch) for ch in CHANNELS}
