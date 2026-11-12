"""Voice-over from KikiVoice (free web TTS, no API): two files per Short instead of one clip per line.

    python make.py siachen --kiki-export     # 1. writes one text file per character
    (user pastes each file into kikivoice.ai, downloads e.g. major.mp3 and gappu.mp3 into the folder it prints)
    python make.py siachen --kiki-split     # 2. cuts each file into its lines, checks them
    python make.py siachen --engine files       # 3. renders with those clips

Each character's lines go into one file, a blank line between lines, so KikiVoice leaves a pause there. split
finds those pauses: of all the quiet stretches it picks the ones that sit closest to where each line should end
(by its share of the text) and are longest, so a "..." pause inside a line is not mistaken for a line break.
A file over KikiVoice's length limit can be made in parts: major_1.mp3, major_2.mp3 ... are joined in order.
--check transcribes every clip with Whisper so a wrong cut shows up before the render.
"""

import importlib
import json
import sys
from pathlib import Path

import numpy as np

from core import engine
from core import lego

AUDIO_EXT = (".mp3", ".wav", ".m4a", ".ogg", ".webm")
NAMES = {"M": "major", "G": "gappu"}     # file name per speaker prefix (see lego.SPEAKERS)
NARRATOR = "narrator"


def lines_of(story):
    """[(scene index, line index, speaker file name, text)] in story order, one per DELIVERY line."""
    from core import delivery as delivery_mod
    rows = getattr(story, "DELIVERY", None) or delivery_mod.build(story.SPEC)
    out = []
    for si, s in enumerate(story.SPEC):
        for li, ((tone, chunks, *_), row) in enumerate(zip(s["vo"], rows[s["key"]])):
            who, _ = lego.split_speaker(chunks[0][1])
            out.append((si, li, NAMES.get(who, NARRATOR), row[1]))
    return out


def folder(name):
    return engine.WORK_DIR / name / "files"


def export(name):
    story = importlib.import_module(f"shorts.{name}")
    d = folder(name)
    d.mkdir(parents=True, exist_ok=True)
    by = {}
    for _, _, who, text in lines_of(story):
        by.setdefault(who, []).append(text)
    print(f"Folder: {d}\n")
    for who, texts in by.items():
        p = d / f"kiki_{who}.txt"
        p.write_text("\n\n".join(texts) + "\n", encoding="utf-8")
        print(f"--- {who}: {len(texts)} lines -> {p.name}  (save the voice as {who}.mp3)")
        print("\n\n".join(texts), "\n")


def speech_frames(a, hop):
    frames = np.abs(a[:len(a) // hop * hop]).reshape(-1, hop).max(axis=1)
    floor = np.percentile(frames, 10)
    return frames < max(0.03, floor * 4)


_WHISPER = None
# small + script prompt + strict anchors is the default; medium is ~20x slower on this CPU (a 42s file took ~50 min
# on 12 Nov), use --model medium only when a --check shows a wrong cut
WHISPER_MODEL = "medium" if "--model" in sys.argv and "medium" in sys.argv else "small"


def _norm(w):
    return "".join(ch for ch in w if ch.isalnum() or "ऀ" <= ch <= "ॿ").replace("़", "")


def _align(audio, texts):
    """Whisper word timings aligned to the script words (Needleman-Wunsch on word similarity, so numbers Whisper
    writes as digits or misheard words just become gaps). Returns (script words [(norm, line k)], heard words
    [(norm, start, end)], {script index: heard index})."""
    global _WHISPER
    import difflib
    import warnings
    import whisper
    warnings.filterwarnings("ignore")
    if _WHISPER is None:
        _WHISPER = whisper.load_model(WHISPER_MODEL)
    # the script as Whisper's prompt: it then hears our words (and number words) instead of guessing,
    # which keeps the anchors right even when the voice runs scenes together with hardly a pause
    res = _WHISPER.transcribe(audio.astype(np.float32) if engine.SR == 16000 else
                              _resample16k(audio), language="hi", fp16=False, word_timestamps=True,
                              initial_prompt=" ".join(texts)[-800:], condition_on_previous_text=False)
    heard = [(_norm(w["word"]), w["start"], w["end"]) for s in res["segments"] for w in s.get("words", [])]
    heard = [h for h in heard if h[0]]
    exp = [(_norm(w), k) for k, t in enumerate(texts) for w in t.split() if _norm(w)]
    n, m, GAP = len(exp), len(heard), -0.45
    sc = np.zeros((n + 1, m + 1))
    sc[1:, 0] = GAP * np.arange(1, n + 1)
    sc[0, 1:] = GAP * np.arange(1, m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            sim = difflib.SequenceMatcher(None, exp[i - 1][0], heard[j - 1][0]).ratio()
            sc[i, j] = max(sc[i - 1, j - 1] + 2 * sim - 1, sc[i - 1, j] + GAP, sc[i, j - 1] + GAP)
    pairs, i, j = {}, n, m
    while i > 0 and j > 0:
        sim = difflib.SequenceMatcher(None, exp[i - 1][0], heard[j - 1][0]).ratio()
        if abs(sc[i, j] - (sc[i - 1, j - 1] + 2 * sim - 1)) < 1e-9:
            if sim >= 0.5:
                pairs[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif abs(sc[i, j] - (sc[i - 1, j] + GAP)) < 1e-9:
            i -= 1
        else:
            j -= 1
    return exp, heard, pairs


def word_starts(audio, text):
    """Start time (s) of every script word of one clip, as the engine's caption timings: Whisper-anchored words
    keep their heard time, the rest are spread between their anchored neighbours by word length."""
    words = text.split()
    exp, heard, pairs = _align(audio, [text])
    norm_idx = [i for i, w in enumerate(words) if _norm(w)]          # script word -> exp index mapping
    known = {norm_idx[ei]: heard[hj][1] for ei, hj in pairs.items()}
    dur = len(audio) / engine.SR
    known.setdefault(0, 0.05)
    known[len(words)] = dur
    pts = []
    for i, tm in sorted(known.items()):              # drop anchors that would run backwards in time
        if not pts or tm > pts[-1][1]:
            pts.append((i, tm))
    out = [0.0] * len(words)
    w = [len(x) + 2 for x in words] + [0]
    for (i0, t0), (i1, t1) in zip(pts, pts[1:]):
        span = sum(w[i0:i1]) or 1
        acc = 0
        for i in range(i0, min(i1, len(words))):
            out[i] = t0 + (t1 - t0) * acc / span
            acc += w[i]
    for i in range(1, len(out)):                                       # keep them in order
        out[i] = max(out[i], out[i - 1] + 0.05)
    return out


def heard_boundaries(audio, texts):
    """Where each line ends (s), from Whisper word timings aligned to the script; None where there is no anchor."""
    exp, heard, pairs = _align(audio, texts)
    ends, starts = {}, {}
    for ei, hj in pairs.items():
        k = exp[ei][1]
        ends[k] = max(ends.get(k, -1), heard[hj][2])
        starts[k] = min(starts.get(k, 1e9), heard[hj][1])
    out = []
    for k in range(len(texts) - 1):
        a, b = ends.get(k), starts.get(k + 1)
        out.append(None if a is None and b is None else ((a + b) / 2 if a is not None and b is not None
                                                         else (a + 0.15 if a is not None else b - 0.15)))
    return out


def _resample16k(audio):
    idx = np.arange(0, len(audio), engine.SR / 16000)
    return np.interp(idx, np.arange(len(audio)), audio).astype(np.float32)


def cut_points(audio, texts):
    """Sample indices where one line ends and the next begins (len(texts) - 1 of them)."""
    n = len(texts)
    if n == 1:
        return []
    a = audio / (np.max(np.abs(audio)) + 1e-9)
    hop = int(0.01 * engine.SR)
    quiet = speech_frames(a, hop)
    loud = np.flatnonzero(~quiet)
    first, last = loud[0], loud[-1]
    runs, i = [], first
    while i < last:
        if quiet[i]:
            j = i
            while j < last and quiet[j]:
                j += 1
            if j - i >= 8:                     # 80 ms or longer
                runs.append(((i + j) / 2, (j - i) * hop / engine.SR))
            i = j
        else:
            i += 1
    if len(runs) < n - 1:
        raise SystemExit(f"found only {len(runs)} pauses for {n} lines - leave a blank line between lines in "
                         f"KikiVoice (or add '...' at each line end) and download again")
    w = [len(t) + 6 for t in texts]
    span = last - first
    expect = [first + span * sum(w[:k + 1]) / sum(w) for k in range(n - 1)]       # by share of the text
    sure = [False] * (n - 1)
    for k, tb in enumerate(heard_boundaries(audio, texts)):                       # by what Whisper heard
        if tb is not None:
            expect[k], sure[k] = tb * engine.SR / hop, True
    # a voice that runs scenes together leaves no pause at a break: give every Whisper-anchored break a fallback
    # cut at the quietest frame within 0.15 s of it, scored below any real pause close by
    energy = np.abs(a[:len(a) // hop * hop]).reshape(-1, hop).max(axis=1)
    virtual = set()
    for k in range(n - 1):
        if sure[k]:
            e = int(expect[k])
            lo, hi = max(first, e - 15), min(last, e + 15)
            if hi > lo:
                runs.append((float(lo + int(np.argmin(energy[lo:hi]))), 0.0))
                virtual.add(len(runs) - 1)
    order = sorted(range(len(runs)), key=lambda j: runs[j][0])
    runs = [runs[j] for j in order]
    virtual = {i for i, j in enumerate(order) if j in virtual}
    # DP: pick n-1 runs in time order, maximising (pause length) - (distance from the expected line end);
    # a Whisper-anchored break weighs distance 4x, so a "..." pause inside a line can't win over the real break
    c = len(runs)
    NEG = -1e9
    best = [[NEG] * c for _ in range(n - 1)]
    back = [[-1] * c for _ in range(n - 1)]

    def score(k, j):
        mid, length = runs[j]
        dist = abs(mid - expect[k]) * hop / engine.SR
        if sure[k] and dist > 0.35:          # Whisper knows where this break is: never cut far from it
            return -1e6
        if j in virtual:
            return -0.6 - dist * 4.0
        return min(length, 1.2) * 2.0 - abs(mid - expect[k]) * hop / engine.SR * (4.0 if sure[k] else 1.0)

    for j in range(c):
        best[0][j] = score(0, j)
    for k in range(1, n - 1):
        run_best, run_arg = NEG, -1
        for j in range(c):
            if j > 0 and best[k - 1][j - 1] > run_best:
                run_best, run_arg = best[k - 1][j - 1], j - 1
            if run_arg >= 0:
                best[k][j] = run_best + score(k, j)
                back[k][j] = run_arg
    j = int(np.argmax(best[n - 2]))
    picks = []
    for k in range(n - 2, -1, -1):
        picks.append(j)
        j = back[k][j]
    return [int(runs[p][0] * hop) for p in sorted(picks)]


def load_parts(d, who):
    parts = sorted(p for p in d.iterdir() if p.suffix.lower() in AUDIO_EXT and
                   (p.stem.lower() == who or p.stem.lower().startswith(who + "_")))
    if not parts:
        raise SystemExit(f"no {who}.mp3 in {d} - make it in KikiVoice from kiki_{who}.txt")
    gap = np.zeros(int(0.8 * engine.SR))
    return np.concatenate([x for p in parts for x in (engine.decode(p), gap)]), [p.name for p in parts]


def split(name, check=False):
    story = importlib.import_module(f"shorts.{name}")
    d = folder(name)
    rows = lines_of(story)
    work = engine.WORK_DIR / name / "files"
    tempo = getattr(story, "KIKI_TEMPO", {})      # e.g. {"major": 1.08, "gappu": 1.15}: speed up, pitch kept
    clips = []
    for who in dict.fromkeys(r[2] for r in rows):
        mine = [r for r in rows if r[2] == who]
        audio, files = load_parts(d, who)
        cuts = [0] + cut_points(audio, [r[3] for r in mine]) + [len(audio)]
        print(f"{who}: {', '.join(files)} -> {len(mine)} lines")
        for (si, li, _, text), a0, a1 in zip(mine, cuts, cuts[1:]):
            out = work / f"scene_{si + 1:02d}_l{li:02d}.wav"
            clip = audio[a0:a1]
            if tempo.get(who, 1.0) != 1.0:
                clip = engine.ffilter(clip, f"atempo={tempo[who]}")   # padded with silence, trimmed at render
            engine.write_wav(out, clip)
            out.with_suffix(".json").write_text(json.dumps(word_starts(clip, text)), encoding="utf-8")
            clips.append((out, text))
            print(f"   {out.name}  {(a1 - a0) / engine.SR:5.2f}s  {text}")
    if check:
        import warnings
        import whisper
        warnings.filterwarnings("ignore")
        m = whisper.load_model("small")
        print("\nWhisper check (expected -> heard):")
        for out, text in sorted(clips):
            heard = m.transcribe(str(out), language="hi", fp16=False)["text"].strip()
            print(f"   {out.name}: {text}\n   {' ' * len(out.name)}  {heard}")
    print(f"\nNext: python {name}.py --engine files")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cmd, target = sys.argv[1], sys.argv[2].removesuffix(".py")
    if cmd == "export":
        export(target)
    elif cmd == "split":
        split(target, check="--check" in sys.argv)
    else:
        raise SystemExit("usage: python make.py <short> --kiki-export | --kiki-split [--check-voice]")
