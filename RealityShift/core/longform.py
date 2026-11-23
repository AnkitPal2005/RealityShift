"""Long-form 16:9 documentary engine (1920x1080) for Reality Shift.

A long-form module (longform/<name>.py) defines:
  TITLE, SOURCES, UPLOAD (title/description/tags/pinned), MUSIC_STYLE, MUSIC_BPM, MUSIC_SEED, KIKI_TEMPO,
  HOT (caption word -> colour), CHAPTERS = [{"key", "title", "lines": [(hindi, roman, shot_fn, params), ...]}],
  thumbnail(ctx)  (drawn on a 1920x1080 canvas, saved as 1280x720).

Every line is one visual beat: its shot is drawn for exactly as long as the voice speaks that line, so the
picture changes with the narration (~4-7 s per beat). Shot functions are called as fn(ctx, S, **params) where
S.t = seconds into the beat, S.d = beat length, S.u = t/d (0..1), S.T = seconds into the video.

Voice (KikiVoice, made by the user): one file per chapter, ch01.mp3 ... chNN.mp3 (parts ch01_1.mp3, ch01_2.mp3
are joined), saved in output/work/<name>/files/. Whisper word timings put every line on its own time.
"""

import json
import math
import subprocess
import time
from pathlib import Path
from types import SimpleNamespace

import cairo
import numpy as np

from core import engine
from core.engine import (SR, clamp, decode, ease_out_cubic, ffilter, hexc, moving_avg, rgba, rrect, sfx_bank,
                         text, text_width, trim_silence, write_wav)

W, H = 1920, 1080
FPS = 30
WPS = 2.7                 # KikiVoice words per second, for the preview timeline only
CH_GAP = 0.55             # silence between chapters (a whoosh plays there)
XFADE = 0.22              # crossfade between beats inside a chapter
CAP_Y = 990
CAP_SIZE = 50
CAP_FONT = "Impact"
WHITE = (0.96, 0.97, 0.98)
CYAN = hexc("#5CE1E6")
GOLD = hexc("#FFC845")
RED = hexc("#FF4040")

OUT = engine.OUT_DIR / "longform"
AUDIO_EXT = (".mp3", ".wav", ".m4a")


def work(name):
    d = engine.WORK_DIR / name / "files"
    d.mkdir(parents=True, exist_ok=True)
    return d


# ============================================================ KikiVoice export

def export(mod, name):
    d = work(name)
    total_w = total_c = 0
    print(f"\nKikiVoice text files -> {d}")
    for i, ch in enumerate(mod.CHAPTERS, 1):
        body = "\n".join(hi for hi, *_ in ch["lines"]) + "\n"
        (d / f"kiki_ch{i:02d}.txt").write_text(body, encoding="utf-8")
        w, c = len(body.split()), len(body)
        total_w += w
        total_c += c
        print(f"  kiki_ch{i:02d}.txt  {w:4d} words  {c:5d} chars   ->  save the voice as ch{i:02d}.mp3")
    print(f"  total {total_w} words, {total_c} chars, ~{total_w / WPS / 60:.1f} min of voice")


def _rename_kiki_defaults(d, n):
    """KikiVoice downloads as kikivoice-*.mp3: if exactly the missing chapters' worth exist, name them by time."""
    have = {p.stem.split("_")[0].lower() for p in d.iterdir() if p.suffix.lower() in AUDIO_EXT}
    missing = [f"ch{i:02d}" for i in range(1, n + 1) if f"ch{i:02d}" not in have]
    kiki = sorted((p for p in d.iterdir() if p.name.lower().startswith("kikivoice") and
                   p.suffix.lower() in AUDIO_EXT), key=lambda p: p.stat().st_mtime)
    if missing and len(kiki) == len(missing):
        for p, m in zip(kiki, missing):
            p.rename(d / f"{m}{p.suffix.lower()}")
            print(f"  renamed {p.name} -> {m}{p.suffix.lower()}")
    elif kiki:
        print(f"  {len(kiki)} kikivoice-* files but {len(missing)} chapters missing - rename them to chNN.mp3 by hand")


def _chapter_audio(d, i, tempo):
    parts = sorted(p for p in d.iterdir() if p.suffix.lower() in AUDIO_EXT and
                   (p.stem.lower() == f"ch{i:02d}" or p.stem.lower().startswith(f"ch{i:02d}_")))
    if not parts:
        return None
    gap = np.zeros(int(0.25 * SR))
    a = np.concatenate([x for p in parts for x in (trim_silence(decode(p), 0.01, 0.05, 0.12)[0], gap)])[:-len(gap)]
    if abs(tempo - 1.0) > 1e-3:
        a = ffilter(a, f"atempo={tempo}").astype(np.float32)
        a = a[:int(len(a) / tempo) + SR // 10]
        a, _ = trim_silence(a, 0.01, 0.05, 0.12)
    return a


def _line_times(audio, texts):
    """Start time of each line in one chapter clip, from Whisper words aligned to the script."""
    from core import voice_kit
    exp, heard, pairs = voice_kit._align(audio, texts)
    starts = {}
    for ei, hj in pairs.items():
        k = exp[ei][1]
        starts[k] = min(starts.get(k, 1e9), heard[hj][1])
    dur = len(audio) / SR
    share = np.cumsum([0] + [len(t) for t in texts])
    share = share / share[-1]
    known = {0: 0.0, len(texts): dur}
    for k, s in starts.items():
        if k > 0:
            known[k] = s - 0.08
    pts = []
    for k, s in sorted(known.items()):          # drop anchors that run backwards
        if not pts or s > pts[-1][1] + 0.4:
            pts.append((k, s))
    if pts[-1][0] != len(texts):
        pts[-1] = (len(texts), dur)
    known = {k: s for k, s in pts}
    out = []
    for k in range(len(texts)):
        for (k0, s0), (k1, s1) in zip(pts, pts[1:]):
            if k0 <= k <= k1:
                u = (share[k] - share[k0]) / max(1e-9, share[k1] - share[k0])
                out.append(s0 + (s1 - s0) * u if k not in known else known[k])
                break
    anchored = sum(1 for k in range(1, len(texts)) if k in starts)
    return out, dur, anchored


# ============================================================ timeline

def timeline(mod, name, need_audio):
    """Beats with start/end in seconds. With voice files: real Whisper timings (cached); else estimated."""
    d = work(name)
    n = len(mod.CHAPTERS)
    if need_audio:
        _rename_kiki_defaults(d, n)
    cache = d / "timings.json"
    stamp = {p.name: p.stat().st_mtime for p in sorted(d.iterdir()) if p.stem.lower().startswith("ch")
             and p.suffix.lower() in AUDIO_EXT}
    stamp["tempo"] = getattr(mod, "KIKI_TEMPO", 1.0)
    stamp["script"] = [[hi for hi, *_ in ch["lines"]] for ch in mod.CHAPTERS]
    cached = json.loads(cache.read_text(encoding="utf-8")) if cache.exists() else {}
    beats, audio_parts, t = [], [], 0.0
    have_all = all(any(p.stem.lower().split("_")[0] == f"ch{i:02d}" for p in d.iterdir()
                       if p.suffix.lower() in AUDIO_EXT) for i in range(1, n + 1))
    if need_audio and not have_all:
        missing = [f"ch{i:02d}" for i in range(1, n + 1) if not any(
            p.stem.lower().split("_")[0] == f"ch{i:02d}" for p in d.iterdir() if p.suffix.lower() in AUDIO_EXT)]
        raise SystemExit(f"voice missing in {d}: {', '.join(missing)}.mp3  (run --kiki-export first)")
    use_cache = have_all and cached.get("stamp") == stamp
    new_cache = {"stamp": stamp, "chapters": []}
    for i, ch in enumerate(mod.CHAPTERS, 1):
        texts = [hi for hi, *_ in ch["lines"]]
        if have_all and need_audio:
            a = _chapter_audio(d, i, stamp["tempo"])
            if use_cache:
                st, dur = cached["chapters"][i - 1]["starts"], cached["chapters"][i - 1]["dur"]
            else:
                print(f"  aligning ch{i:02d} with Whisper ...", flush=True)
                st, dur, anchored = _line_times(a, texts)
                print(f"    {dur:5.1f}s, {anchored}/{len(texts) - 1} line starts anchored")
            dur = len(a) / SR
            audio_parts.append((t, a))
        else:
            lens = [max(2.0, len(x.split()) / WPS + 0.25) for x in texts]
            st = list(np.cumsum([0] + lens[:-1]))
            dur = sum(lens)
        new_cache["chapters"].append({"starts": [float(x) for x in st], "dur": float(dur)})
        for k, (hi, roman, fn, params) in enumerate(ch["lines"]):
            s0 = t + st[k]
            s1 = t + (st[k + 1] if k + 1 < len(st) else dur + CH_GAP)
            beats.append(SimpleNamespace(ch=i - 1, k=k, hi=hi, roman=roman, fn=fn, params=params or {},
                                         start=s0 if k else t, end=s1, chapter_start=(k == 0)))
        t += dur + CH_GAP
    if have_all and need_audio:
        cache.write_text(json.dumps(new_cache, ensure_ascii=False, indent=1), encoding="utf-8")
    return beats, audio_parts, t


def chapter_marks(mod, beats):
    return [(b.start, mod.CHAPTERS[b.ch]["title"]) for b in beats if b.chapter_start]


# ============================================================ audio mix

def mix(mod, audio_parts, total, beats, dest):
    n = int((total + 0.5) * SR)
    voice = np.zeros(n)
    for t0, a in audio_parts:
        i0 = int(t0 * SR)
        voice[i0:i0 + len(a)] += a[:n - i0]
    peak = np.max(np.abs(voice)) or 1
    voice *= 0.89 / peak
    style = getattr(mod, "MUSIC_STYLE", "tension")
    bed = {"tension": engine.tension_music, "ambient": engine.ambient_music, "pulse": engine.pulse_music,
           "march": engine.march_music}[style](total + 0.5, getattr(mod, "MUSIC_BPM", 86), getattr(mod, "MUSIC_SEED", 7))
    bed = np.pad(bed, (0, max(0, n - len(bed))))[:n]
    bed /= (np.max(np.abs(bed)) or 1)
    env = moving_avg(np.abs(voice), int(0.25 * SR))
    duck = np.clip(env / 0.04, 0, 1)
    lo, hi = getattr(mod, "MUSIC_LO", 0.07), getattr(mod, "MUSIC_HI", 0.16)
    fade = np.minimum(1, np.arange(n) / (1.5 * SR)) * np.minimum(1, (n - np.arange(n)) / (3 * SR))
    out = voice + bed * (hi - (hi - lo) * duck) * fade
    bank = sfx_bank()
    for b in beats:                     # whoosh into every chapter, soft tick on beats that ask for one
        cue = "whoosh" if b.chapter_start and b.ch > 0 else b.params.get("_sfx")
        if cue and cue in bank:
            s = bank[cue] * engine.SFX_GAIN.get(cue, 0.2)
            i0 = max(0, int((b.start - (0.35 if cue == "whoosh" else 0)) * SR))
            out[i0:i0 + len(s)] += s[:n - i0]
    out /= max(1.0, np.max(np.abs(out)) / 0.97)
    write_wav(dest, out)
    return dest


# ============================================================ captions & frame chrome

def caption_cues(beats):
    """Roman caption chunks (<= 5 words / ~30 chars) spread over each beat by length."""
    cues = []
    for b in beats:
        words, chunks, cur = b.roman.split(), [], []
        for w in words:
            if cur and (len(cur) >= 5 or len(" ".join(cur + [w])) > 30):
                chunks.append(" ".join(cur))
                cur = []
            cur.append(w)
        if cur:
            chunks.append(" ".join(cur))
        speak_end = b.end - (CH_GAP if b.k == len_of(b) else 0.12)
        span = max(0.5, speak_end - b.start - 0.05)
        tot = sum(len(c) + 4 for c in chunks)
        acc = b.start + 0.05
        for c in chunks:
            d = span * (len(c) + 4) / tot
            cues.append((acc, acc + d, c))
            acc += d
    return cues


_LAST = {}


def len_of(b):
    return _LAST.get(b.ch, -1)


def draw_caption(ctx, s, hot):
    size = CAP_SIZE
    words = s.split()
    widths = [text_width(ctx, w, size, font=CAP_FONT) for w in words]
    space = size * 0.28
    tw = sum(widths) + space * (len(words) - 1)
    rrect(ctx, W / 2 - tw / 2 - 30, CAP_Y - 40, tw + 60, 80, 16)
    rgba(ctx, (0.01, 0.02, 0.04), 0.62)
    ctx.fill()
    x = W / 2 - tw / 2
    for w, ww in zip(words, widths):
        key = w.strip(".,!?:'").upper()
        c = hot.get(key, WHITE)
        text(ctx, w, x, CAP_Y, size, c, font=CAP_FONT, anchor="l", stroke=(0, 0, 0), stroke_w=6)
        x += ww + space


def draw_chrome(ctx, mod, beats, b, T, total):
    """Top chapter-progress bar, a small brand tag and the chapter card at each chapter start."""
    n = len(mod.CHAPTERS)
    starts = [x.start for x in beats if x.chapter_start] + [total]
    x0, x1, y = 60, W - 60, 26
    seg = (x1 - x0) / n
    for i in range(n):
        u = clamp((T - starts[i]) / max(0.1, starts[i + 1] - starts[i]))
        rrect(ctx, x0 + i * seg + 3, y, seg - 6, 6, 3)
        rgba(ctx, WHITE, 0.16)
        ctx.fill()
        if u > 0:
            rrect(ctx, x0 + i * seg + 3, y, (seg - 6) * u, 6, 3)
            rgba(ctx, GOLD if i == b.ch else CYAN, 0.85)
            ctx.fill()
    text(ctx, "REALITY SHIFT", W - 64, 62, 22, WHITE, font="Consolas", anchor="r", a=0.45)
    first = next(x for x in beats if x.ch == b.ch and x.chapter_start)
    lt = T - first.start
    if b.ch > 0 and lt < 3.2:
        a = clamp(lt / 0.3) * clamp((3.2 - lt) / 0.4)
        slide = 1 - ease_out_cubic(lt / 0.45)
        title = mod.CHAPTERS[b.ch]["title"]
        tw = max(text_width(ctx, title, 46, font=CAP_FONT), 260)
        bx = 70 - 60 * slide
        rrect(ctx, bx, 80, tw + 70, 110, 10)
        rgba(ctx, (0.02, 0.03, 0.06), 0.78 * a)
        ctx.fill()
        ctx.rectangle(bx, 80, 8, 110)
        rgba(ctx, GOLD, a)
        ctx.fill()
        text(ctx, f"CHAPTER {b.ch}", bx + 36, 108, 24, GOLD, font="Consolas", anchor="l", a=a)
        text(ctx, title, bx + 36, 154, 46, WHITE, font=CAP_FONT, anchor="l", a=a)


# ============================================================ frames

def draw_beat(ctx, b, T):
    S = SimpleNamespace(t=T - b.start, d=b.end - b.start, T=T)
    S.u = clamp(S.t / max(0.1, S.d))
    ctx.save()
    b.fn(ctx, S, **{k: v for k, v in b.params.items() if not k.startswith("_")})
    ctx.restore()


def frame(ctx, mod, beats, i, T, cues, total):
    b = beats[i]
    draw_beat(ctx, b, T)
    lt = T - b.start
    if i > 0 and not b.chapter_start and lt < XFADE:     # crossfade from the previous beat's last frame
        ctx.push_group()
        draw_beat(ctx, beats[i - 1], beats[i - 1].end)
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(1 - lt / XFADE)
    if b.chapter_start and b.ch > 0 and lt < 0.35:        # dip from black into a new chapter
        ctx.set_source_rgba(0, 0, 0, 1 - lt / 0.35)
        ctx.paint()
    draw_chrome(ctx, mod, beats, b, T, total)
    for s0, s1, c in cues:
        if s0 <= T < s1:
            draw_caption(ctx, c, mod.HOT)
            break


def _index(beats):
    for b in beats:
        _LAST[b.ch] = max(_LAST.get(b.ch, -1), b.k)


def render(mod, name):
    beats, parts, total = timeline(mod, name, need_audio=True)
    _index(beats)
    OUT.mkdir(parents=True, exist_ok=True)
    wav = work(name) / "longform_mix.wav"
    print(f"  mixing {total:.1f}s of audio ({total / 60:.2f} min) ...", flush=True)
    mix(mod, parts, total, beats, wav)
    cues = caption_cues(beats)
    out = OUT / f"{name}.mp4"
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    nf, bi, t0 = int(total * FPS), 0, time.time()
    for f in range(nf):
        T = f / FPS
        while bi < len(beats) - 1 and T >= beats[bi + 1].start:
            bi += 1
        frame(ctx, mod, beats, bi, T, cues, total)
        surf.flush()
        proc.stdin.write(surf.get_data())
        if f % (FPS * 30) == 0:
            el = time.time() - t0
            print(f"  frame {f}/{nf}  {f / max(el, 1e-3):.1f} fps  eta {(nf - f) / max(f / max(el, 1e-3), 1e-3) / 60:.1f} min",
                  flush=True)
    proc.stdin.close()
    proc.wait()
    print(f"  video -> {out}")
    write_kit(mod, name, beats, total)
    thumbnail(mod, name)
    return out


# ============================================================ preview, thumbnail, upload kit

def preview(mod, name):
    beats, _, total = timeline(mod, name, need_audio=False)
    _index(beats)
    cues = caption_cues(beats)
    OUT.mkdir(parents=True, exist_ok=True)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    tw, th, cols = 480, 270, 5
    per = 30
    sheets = []
    for s in range(0, len(beats), per):
        chunk = beats[s:s + per]
        rows = math.ceil(len(chunk) / cols)
        sheet = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * tw, rows * (th + 34))
        sc = cairo.Context(sheet)
        sc.set_source_rgb(0.05, 0.05, 0.07)
        sc.paint()
        for j, b in enumerate(chunk):
            T = b.start + (b.end - b.start) * 0.6
            frame(ctx, mod, beats, s + j, T, cues, total)
            x, y = (j % cols) * tw, (j // cols) * (th + 34)
            sc.save()
            sc.translate(x, y)
            sc.scale(tw / W, th / H)
            sc.set_source_surface(surf, 0, 0)
            sc.paint()
            sc.restore()
            text(sc, f"{b.ch}.{b.k + 1}  {b.roman[:44]}", x + 8, y + th + 17, 15, WHITE, font="Consolas", anchor="l")
        p = OUT / f"{name}_sheet_{s // per + 1}.png"
        sheet.write_to_png(str(p))
        sheets.append(p)
    print(f"  {len(beats)} beats, est. {total / 60:.1f} min")
    for p in sheets:
        print(f"  sheet -> {p}")
    thumbnail(mod, name)
    write_kit(mod, name, beats, total, estimated=True)
    return sheets


def thumbnail(mod, name):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720)
    ctx = cairo.Context(surf)
    ctx.scale(1280 / W, 720 / H)
    mod.thumbnail(ctx)
    p = OUT / f"{name}_thumb.png"
    surf.write_to_png(str(p))
    print(f"  thumbnail -> {p}")
    return p


def _ts(s):
    s = int(s)
    return f"{s // 60}:{s % 60:02d}"


def write_kit(mod, name, beats, total, estimated=False):
    u = mod.UPLOAD
    marks = chapter_marks(mod, beats)
    chap = "\n".join(f"{_ts(0 if i == 0 else t)} {title.title()}" for i, (t, title) in enumerate(marks))
    note = "\n> Chapter times are ESTIMATES (no voice yet) - they are rewritten from the real voice on render.\n" \
        if estimated else ""
    md = f"""# {u['title']}

**Length:** {_ts(total)}{' (estimated)' if estimated else ''}  |  **Format:** 16:9 long-form  |  **Title length:** {len(u['title'])} chars
{note}
## Title
{u['title']}

## Description
{u['description'].strip()}

Chapters:
{chap}

{u.get('hashtags', '')}

## Tags
{', '.join(u['tags'])}

## Pinned comment
{u['pinned']}

## Sources (verify before upload)
""" + "\n".join(f"- {s}" for s in mod.SOURCES) + "\n"
    p = OUT / f"{name}_upload.md"
    p.write_text(md, encoding="utf-8")
    print(f"  upload kit -> {p}")
    return p
