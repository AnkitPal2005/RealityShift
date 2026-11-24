import os, math
import cairo
import numpy as np
import wave

BASE = r"c:\Users\WottaCore - 01\Desktop\Youtube-Agent\story-pipeline\BrainBlitz"
OUT_DIR = os.path.join(BASE, "output")
AUDIO_DIR = os.path.join(BASE, "assets", "audio")
IMG_DIR = os.path.join(BASE, "assets", "images")

for d in [OUT_DIR, AUDIO_DIR, IMG_DIR, os.path.join(BASE, "core")]:
    os.makedirs(d, exist_ok=True)

# 1. Synthesize SFX
SR = 44100
def write_wav(path, samples):
    samples = np.clip(samples, -1.0, 1.0)
    int_samples = (samples * 32767).astype(np.int16)
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
        wf.writeframes(int_samples.tobytes())

# Tick sound
dur = 0.08; t = np.linspace(0, dur, int(SR*dur), False)
tick = (np.sin(2*np.pi*2200*t)*np.exp(-t*90) + (np.random.rand(len(t))*2-1)*np.exp(-t*120)*0.4)
write_wav(os.path.join(AUDIO_DIR, 'tick.wav'), tick)

# Ding sound
dur = 0.8; t = np.linspace(0, dur, int(SR*dur), False)
ding = (np.sin(2*np.pi*1200*t)*0.7 + np.sin(2*np.pi*2400*t)*0.3)*np.exp(-t*6)
write_wav(os.path.join(AUDIO_DIR, 'ding.wav'), ding)

# Whoosh sound
dur = 1.0; t = np.linspace(0, dur, int(SR*dur), False)
freq = np.linspace(150, 800, len(t))
whoosh = np.sin(2*np.pi*np.cumsum(freq)/SR) * (t/dur) * np.exp(-(1.0-t)*2) * 0.8
write_wav(os.path.join(AUDIO_DIR, 'whoosh.wav'), whoosh)

# Mix 16s soundtrack
total_s = int(16.0 * SR)
master = np.zeros(total_s, dtype=np.float32)

def overlay(sound, st, vol=1.0):
    si = int(st * SR); ei = min(len(master), si + len(sound))
    master[si:ei] += sound[:ei-si] * vol

overlay(whoosh, 0.0, 0.8)
for sec in range(2, 12):
    overlay(tick, float(sec), 0.9)
    if sec >= 9: overlay(tick, float(sec) + 0.5, 0.7)

overlay(ding, 13.0, 1.0)
overlay(ding, 13.8, 1.0)
overlay(ding, 14.6, 1.0)

write_wav(os.path.join(OUT_DIR, 'soundtrack.wav'), master)
print("Pipeline setup completed!")
