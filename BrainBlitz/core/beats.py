"""Brain Blitz music beds - several really different styles (own synthesis, no samples, no copyrighted audio).

phonk.py gives the cowbell phonk only, so every "new" phonk beat still sounded the same (user, 25 Nov).
Here each STYLE has its own instruments, drum pattern, bass and tempo:

  phonk     808 cowbell riff, distorted 808, trap hats            (phonk.phonk_bed)
  chiptune  8-bit square arpeggios, triangle bass, noise drums    150-160 bpm  (video-game feel)
  house     four-on-the-floor kick, off-beat hats, saw chord stabs, off-beat sub   122-126 bpm
  marimba   half-time trap drums, marimba riff, clean long 808   140-146 bpm
  dnb       fast breakbeat, detuned "reese" bass, plucked-string riff   170-174 bpm

    from beats import music_bed
    bed = music_bed(26.0, style="chiptune", beat_no=5, seed=3, breaks=[(16, 17)], build=(4, 6.5))

Log every (style, beat_no) used in the Brain Blitz memory so no two Shorts share a bed.
"""
import numpy as np

import phonk as pk

SR = pk.SR
STYLES = ("phonk", "chiptune", "house", "marimba", "dnb")
_T = pk._t


# ----------------------------------------------------------------- instruments
def square_note(f, dur=0.11, duty=0.5, vol=0.22):
    t = _T(dur)
    ph = (f * t) % 1.0
    s = np.where(ph < duty, 1.0, -1.0)
    return s * np.exp(-t * 10) * np.clip(t / 0.002, 0, 1) * vol


def triangle_note(f, dur, vol=0.5):
    t = _T(dur)
    s = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * f * t))
    return s * np.clip(t / 0.004, 0, 1) * np.clip((dur - t) / 0.01, 0, 1) * vol


def noise_drum(seed, dur, decay, vol, lowpass=1):
    t = _T(dur)
    n = np.random.RandomState(seed).uniform(-1, 1, len(t))
    if lowpass > 1:
        n = np.convolve(n, np.ones(lowpass) / lowpass, mode="same")
    return n * np.exp(-t * decay) * vol


def chip_kick():
    t = _T(0.14)
    f = 60 + 300 * np.exp(-t * 40)
    return np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 18) * 0.6


def house_kick():
    t = _T(0.35)
    f = 50 + 90 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) * 1.0


def marimba_note(f, vol=0.45):
    t = _T(0.5)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 35)
    return s * np.exp(-t * 8) * np.clip(t / 0.002, 0, 1) * vol


def saw(f, t, harmonics=8):
    return sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, harmonics + 1)) * 0.6


def stab(f, vol=0.25):
    """Minor triad saw stab, softened."""
    t = _T(0.18)
    s = saw(f, t) + saw(f * 2 ** (3 / 12), t) + saw(f * 2 ** (7 / 12), t)
    s = np.convolve(s, np.ones(5) / 5, mode="same")
    return s * np.exp(-t * 12) * np.clip(t / 0.003, 0, 1) * vol / 3


_PLUCK = {}


def pluck(f, vol=0.4):
    """Karplus-Strong plucked string (cached per pitch)."""
    key = round(f, 2)
    if key not in _PLUCK:
        n = int(SR * 0.45)
        p = max(2, int(SR / f))
        buf = np.random.RandomState(int(f)).uniform(-1, 1, p)
        out = np.zeros(n)
        for i in range(n):
            out[i] = buf[i % p]
            buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
        _PLUCK[key] = out
    return _PLUCK[key] * vol


def reese(f, dur, vol=0.5):
    t = _T(dur)
    s = saw(f, t, 6) + saw(f * 1.006, t, 6)
    s = np.convolve(s, np.ones(24) / 24, mode="same")
    return np.tanh(s * 1.5) * np.clip(t / 0.01, 0, 1) * np.clip((dur - t) / 0.03, 0, 1) * vol


def sub_note(f, dur=0.2, vol=0.7):
    t = _T(dur)
    return np.sin(2 * np.pi * f * t) * np.clip(t / 0.003, 0, 1) * np.exp(-t * 6) * vol


# ----------------------------------------------------------------- styles
CONF = {
    "chiptune": dict(bpms=(150, 152, 156, 160), kicks={0, 8, 11}, snares={4, 12}),
    "house": dict(bpms=(122, 124, 126), kicks={0, 4, 8, 12}, snares={4, 12}),
    "marimba": dict(bpms=(140, 142, 144, 146), kicks={0, 7, 10}, snares={8}),
    "dnb": dict(bpms=(170, 172, 174), kicks={0, 10}, snares={4, 12}),
}
ARP = [0, 3, 7, 12, 7, 3, 0, 3, 7, 12, 15, 12, 7, 3, 7, 12]


def music_bed(dur, style="phonk", beat_no=1, seed=1, breaks=(), build=None):
    if style == "phonk":
        return pk.phonk_bed(dur, beat_no=beat_no, seed=seed, breaks=breaks, build=build)
    if style not in CONF:
        raise ValueError("unknown style " + style)
    v = pk.variant(beat_no if beat_no != 1 else 99)   # riff / key / progression from the beat number
    c = CONF[style]
    r = np.random.RandomState(2000 + beat_no)
    bpm = int(r.choice(c["bpms"]))
    root = v["root"]
    prog = [2 ** (s / 12) for s in v["prog"]]
    riffs = v["riffs"]
    n = int(SR * dur)
    drums, bass, lead = np.zeros(n), np.zeros(n), np.zeros(n)
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

    kick_sig = {"chiptune": chip_kick(), "house": house_kick(), "marimba": pk.kick(), "dnb": house_kick()}[style]
    step, x = 0, 0.0
    while x < dur:
        bar, st = divmod(step, 16)
        rf = root * prog[bar % 4]
        building = build and build[0] <= x < build[1]
        if not in_break(x):
            if st in c["kicks"]:
                put(drums, kick_sig, x, 0.9)
                i = int(x * SR)
                L = int(0.15 * SR)
                if i < n:
                    seg = min(L, n - i)
                    duck[i:i + seg] = np.minimum(duck[i:i + seg], 0.45 + 0.55 * np.linspace(0, 1, seg))
            if st in c["snares"]:
                if style == "chiptune":
                    put(drums, noise_drum(rnd.randint(1 << 30), 0.12, 25, 0.45), x)
                else:
                    put(drums, pk.clap(rnd.randint(1 << 30)), x, 0.7)
            if style == "dnb" and st in (7, 15):
                put(drums, pk.clap(rnd.randint(1 << 30)), x, 0.22)        # ghost snares
            # hats
            if style == "house":
                if st % 4 == 2:
                    put(drums, pk.hat(rnd.randint(1 << 30), open_=True), x, 0.4)
                elif st % 2 == 0:
                    put(drums, pk.hat(rnd.randint(1 << 30)), x, 0.15)
            elif style == "chiptune":
                if st % 2 == 0:
                    put(drums, noise_drum(rnd.randint(1 << 30), 0.03, 120, 0.18), x)
            elif style == "dnb":
                put(drums, pk.hat(rnd.randint(1 << 30)), x, 0.3 if st % 2 == 0 else 0.14)
            else:   # marimba trap hats with rolls
                put(drums, pk.hat(rnd.randint(1 << 30)), x, 0.3 if st % 2 else 0.2)
                if st >= 13 or building:
                    put(drums, pk.hat(rnd.randint(1 << 30)), x + s16 / 2, 0.2)
            if building and style != "marimba":
                put(drums, pk.hat(rnd.randint(1 << 30)), x + s16 / 2, 0.22)
            # bass
            if style == "chiptune" and st % 2 == 0:
                put(bass, triangle_note(rf * 2, s16 * 1.8), x, 0.6)
            elif style == "house" and st % 4 == 2:
                put(bass, sub_note(rf * 2, s16 * 1.8), x, 0.9)
            elif style == "marimba" and st in c["kicks"]:
                put(bass, np.tanh(1.2 * pk.bass808(rf, s16 * 5)), x, 0.75)
            elif style == "dnb" and st == 0:
                put(bass, reese(rf, s16 * 16), x, 0.55)
            # lead
            semi = riffs[bar % 2][st]
            if style == "chiptune":
                k = 2 ** ((ARP[st] + v["prog"][bar % 4]) / 12)
                put(lead, square_note(root * 8 * k, duty=0.25 if bar % 2 else 0.5), x)
            elif semi is not None:
                f = root * 8 * 2 ** (semi / 12)
                if style == "house":
                    put(lead, stab(f / 2), x)
                elif style == "marimba":
                    put(lead, marimba_note(f), x)
                else:
                    put(lead, pluck(f / 2), x)
        x += s16
        step += 1

    if build:
        a, b = build
        t = _T(b - a)
        sweep = np.sin(2 * np.pi * np.cumsum(300 + 1500 * (t / (b - a)) ** 2) / SR)
        nz = np.random.RandomState(seed + 7).uniform(-1, 1, len(t))
        put(drums, (nz * 0.2 + sweep * 0.3) * (t / (b - a)) ** 2, a, 0.6)
    for a, b in breaks:
        if b - a > 0.3:
            put(bass, sub_note(root, b - a, 0.6), a)

    mix = drums + bass * duck + lead * (0.65 + 0.35 * duck)
    mix = np.tanh(mix * 1.3) / np.tanh(1.3)
    return mix / (np.max(np.abs(mix)) + 1e-9)


if __name__ == "__main__":   # python core/beats.py -> 12 s demo of every style in output/beat_demos/
    import os
    import wave
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "beat_demos")
    os.makedirs(out, exist_ok=True)
    for k, s in enumerate(STYLES):
        b = music_bed(12.0, style=s, beat_no=5 + k, seed=3, build=(6, 8), breaks=[(8, 8.6)])
        with wave.open(os.path.join(out, f"{k + 1}_{s}.wav"), "w") as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
            wf.writeframes((b * 0.85 * 32767).astype(np.int16).tobytes())
    print("demos in", out)
