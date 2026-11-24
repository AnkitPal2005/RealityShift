"""Original procedural phonk-style beat (no samples, no copyrighted audio).

Elements: 808-style cowbell melody, distorted gliding 808 bass, punchy kick, clap,
trap hi-hats with rolls, sidechain pump. Everything is synthesised with numpy.

    bed = phonk_bed(dur=16.0, bpm=132, seed=1, breaks=[(10.0, 11.0)], build=(7.0, 10.0))
"""
import numpy as np

SR = 44100


def _t(dur):
    return np.arange(int(SR * dur)) / SR


def kick():
    t = _t(0.45)
    f = 45 + 110 * np.exp(-t * 35)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(2.2 * np.sin(ph) * np.exp(-t * 7))


def clap(seed):
    t = _t(0.22)
    n = np.random.RandomState(seed).uniform(-1, 1, len(t))
    n = n - np.convolve(n, np.ones(8) / 8, mode="same")        # crude high-pass
    env = np.exp(-t * 22) * (1 + 0.6 * (np.sin(2 * np.pi * 90 * t) > 0) * (t < 0.03))
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.5
    return (n * env + body) * 0.8


def hat(seed, open_=False):
    t = _t(0.12 if open_ else 0.04)
    n = np.random.RandomState(seed).uniform(-1, 1, len(t))
    n = np.diff(np.concatenate([[0], n]))                       # high-pass
    return n * np.exp(-t * (25 if open_ else 110)) * 0.5


def cowbell(semi):
    """TR-808 style cowbell: two square-ish tones ~540/800 Hz, pitched by semitones."""
    t = _t(0.32)
    k = 2 ** (semi / 12)
    s = np.sign(np.sin(2 * np.pi * 540 * k * t)) + np.sign(np.sin(2 * np.pi * 800 * k * t))
    s = np.convolve(s, np.ones(6) / 6, mode="same")              # soften the edges
    env = np.exp(-t * 14) * 0.7 + np.exp(-t * 60) * 0.3
    return s * env * 0.35


def bass808(f0, dur, glide_to=None):
    t = _t(dur)
    f = np.full(len(t), f0)
    if glide_to:
        g = np.clip((t - dur * 0.45) / (dur * 0.4), 0, 1)
        f = f0 + (glide_to - f0) * g
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.clip(t / 0.005, 0, 1) * np.exp(-t * 1.6)
    return np.tanh(3.0 * np.sin(ph) * env) * 0.8


SCALE = [-2, 0, 0, 3, 5, 7, 10, 12]          # minor-pentatonic-ish, weighted to the root
RHYTHMS = [
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0],
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0],
    [1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0],
]
KICKS = [{0, 6, 10}, {0, 7, 10}, {0, 3, 8, 11}, {0, 6, 9, 12}]
PROGS = [[0, 0, -4, -5], [0, -2, -4, -2], [0, 3, -2, -4], [0, 0, -5, -7]]
ROOTS = [73.42, 69.30, 77.78, 65.41, 82.41]   # D, C#, D#, C, E


def variant(beat_no):
    """beat_no 1 = the approved original. Every other number gives a new riff, key,
    tempo, kick pattern and bass progression (same phonk vibe, never the same beat)."""
    if beat_no == 1:
        return dict(bpm=132, root=73.42, kicks={0, 6, 10}, prog=[0, 0, -4, -5],
                    riffs=[[0, None, 0, 3, None, 0, 5, None, 3, None, 0, None, -2, None, 0, None],
                           [0, None, 0, 3, None, 0, 7, None, 5, None, 3, None, 0, None, -2, None]])
    r = np.random.RandomState(1000 + beat_no)
    riffs = []
    for _ in range(2):
        rhythm = RHYTHMS[r.randint(len(RHYTHMS))]
        riffs.append([int(SCALE[r.randint(len(SCALE))]) if (on and k) else (0 if on else None)
                      for k, on in enumerate(rhythm)])
    return dict(bpm=int(r.choice([126, 128, 130, 134, 136, 140])), root=float(r.choice(ROOTS)),
                kicks=KICKS[r.randint(len(KICKS))], prog=PROGS[r.randint(len(PROGS))], riffs=riffs)


def phonk_bed(dur, beat_no=1, seed=1, breaks=(), build=None):
    """beat_no: which beat (1 = approved original; use a new number per Short).
    breaks: list of (start, end) seconds where the beat drops out (808 tail rings).
    build: (start, end) where hats double and a riser climbs."""
    v = variant(beat_no)
    bpm, root = v["bpm"], v["root"]
    n = int(SR * dur)
    drums = np.zeros(n)
    bass = np.zeros(n)
    bell = np.zeros(n)
    duck = np.ones(n)
    s16 = 60 / bpm / 4
    rnd = np.random.RandomState(seed)

    def put(buf, sig, at, vol=1.0):
        i = int(at * SR)
        j = min(n, i + len(sig))
        if 0 <= i < n:
            buf[i:j] += sig[:j - i] * vol

    def in_break(x):
        return any(a <= x < b for a, b in breaks)

    riffs = v["riffs"]                                            # semitones, None = rest
    bass_roots = [2 ** (s / 12) for s in v["prog"]]
    kick_steps = v["kicks"]
    klen = sorted(kick_steps) + [16]
    kdur = {k: max(3, klen[j + 1] - k) + 0.5 for j, k in enumerate(klen[:-1])}
    kick_sig = kick()
    step = 0
    x = 0.0
    while x < dur:
        bar, st = divmod(step, 16)
        if not in_break(x):
            building = build and build[0] <= x < build[1]
            if st in kick_steps:
                put(drums, kick_sig, x, 0.9)
                i = int(x * SR)
                L = int(0.18 * SR)
                if i < n:
                    seg = min(L, n - i)
                    duck[i:i + seg] = np.minimum(duck[i:i + seg], 0.35 + 0.65 * np.linspace(0, 1, seg))
                root_f = root * bass_roots[bar % 4]
                glide = root_f * 2 ** (-5 / 12) if (st == max(kick_steps) and bar % 2) else None
                put(bass, bass808(root_f, s16 * kdur[st], glide), x, 0.9)
            if st in (4, 12):
                put(drums, clap(rnd.randint(1 << 30)), x, 0.7)
            # hats: 16ths, 32nd rolls at bar ends and during the build
            put(drums, hat(rnd.randint(1 << 30), open_=(st == 14)), x, 0.35 if st % 2 else 0.22)
            if building or st >= 14:
                put(drums, hat(rnd.randint(1 << 30)), x + s16 / 2, 0.25)
            semi = riffs[bar % 2][st]
            if semi is not None:
                put(bell, cowbell(semi), x, 0.9)
        x += s16
        step += 1

    # riser during the build
    if build:
        a, b = build
        t = _t(b - a)
        nz = np.random.RandomState(seed + 7).uniform(-1, 1, len(t))
        sweep = np.sin(2 * np.pi * np.cumsum(300 + 1500 * (t / (b - a)) ** 2) / SR)
        put(drums, (nz * 0.25 + sweep * 0.35) * (t / (b - a)) ** 2, a, 0.6)
    # 808 drop slide into each break
    for a, b in breaks:
        put(bass, bass808(root, b - a, glide_to=root * 0.5), a, 1.0)

    mix = drums + bass * duck + bell * (0.6 + 0.4 * duck)
    mix = np.tanh(mix * 1.4) / np.tanh(1.4)
    return mix / (np.max(np.abs(mix)) + 1e-9)
