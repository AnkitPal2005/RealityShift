# RealityShift Audio Synchronization and Mixing Reference

This reference defines the multi-track audio architecture, hierarchical mixing parameters, ducking curves, KikiVoice audio ingestion, and Whisper synchronization protocols for the RealityShift pipeline.

---

## 1. Multi-Track Audio Hierarchy

A RealityShift soundscape is structured across four synchronized audio layers to achieve cinematic immersion without drowning out scientific narration:

```
+-------------------------------------------------------------+
| TRACK 1: Voiceover Narration (KikiVoice Master Recording)   |  0 dB Ref (-14 LUFS)
+-------------------------------------------------------------+
| TRACK 2: Impact & Transition SFX (Whooshes, Hits, Risers)   |  -6 to -10 dB Rel
+-------------------------------------------------------------+
| TRACK 3: Sci-Fi Diegetic SFX (Telemetry, Space Hum, Drone)  |  -14 to -18 dB Rel
+-------------------------------------------------------------+
| TRACK 4: Cinematic Music Bed (Procedural or Mastered Track) |  -18 to -22 dB Rel
+-------------------------------------------------------------+
```

### 1.1 Track Calibration Standards

| Audio Track | Target Integrated Loudness | Peak Level (dBFS) | Frequency Focus | Spatial Positioning |
| :--- | :--- | :--- | :--- | :--- |
| **Track 1: Voiceover** | $-14.0\text{ to } -15.5\text{ LUFS}$ | $-1.0\text{ dBFS}$ | $120\text{ Hz}\text{--}8.0\text{ kHz}$ (Presence) | Center (Mono or Centered Dual Mono) |
| **Track 2: Impact SFX** | $-20.0\text{ to } -24.0\text{ LUFS}$ | $-2.5\text{ dBFS}$ | Low sub ($40\text{--}80\text{ Hz}$) + High air ($3\text{--}10\text{ kHz}$) | Stereo ($100\%$ spread) |
| **Track 3: Diegetic Foley**| $-28.0\text{ to } -32.0\text{ LUFS}$ | $-8.0\text{ dBFS}$ | Mid-range ($400\text{ Hz}\text{--}4\text{ kHz}$) | Balanced Stereo ($60\text{--}80\%$ spread) |
| **Track 4: Music Bed** | $-22.0\text{ to } -26.0\text{ LUFS}$ (unducked) | $-6.0\text{ dBFS}$ | Full spectrum with $1.5\text{ kHz}$ notch | Wide Stereo ($100\%$ spread) |

---

## 2. Dynamic Audio Ducking Architecture

To preserve $100\%$ intelligibility of the conversational Hindi narration, all underlying audio tracks (especially Music Bed and Diegetic Foley) must be dynamically ducked whenever voiceover speech is present.

### 2.1 Ducking Parameters
- **Ducking Attenuation**: $-5.0\text{ dB}$ to $-7.0\text{ dB}$ relative to the music bed's nominal level.
- **Attack Time**: $40\text{ ms}$ (smooth fade-down before the first voiced phoneme).
- **Hold Time**: $80\text{ ms}$ (prevents "pumping" artifacts during short intra-sentence pauses).
- **Release Time**: $250\text{ ms}$ (gentle swell back to nominal volume after speech ends).

```
Voiceover:        [=== SPOKEN PHRASE ===]
                  ^                     ^
Music Level: 1.0  |                     |  /----- 1.0
             \---/                       --/
             Ducked Level (0.42 = -7.5 dB)
             Attack: 40ms                Release: 250ms
```

---

## 3. KikiVoice Ingestion & Whisper Synchronization Protocol

### 3.1 Timing Classification Standard
All scene and caption timings in RealityShift exist in one of two distinct states:
1. **Estimated Timing**: The mathematical pacing projection generated during scripting (`rs-script-writer`) based on syllable-per-second models ($\approx 3.2\text{--}3.8\text{ words/s}$).
2. **Whisper-Verified Timing**: The ground-truth millisecond timestamps extracted directly from the creator's recorded audio via OpenAI Whisper.
- **Rule**: Rendering must never proceed on estimated timings once recorded audio is provided. Ground-truth Whisper timestamps supersede script estimates.

### 3.2 Automated Ingestion & Split Pipeline (`core/voice_kit.py`)
1. **Script Export**: Script text formatted with KikiVoice pause tags `((⏱=ms))` is exported to `output/work/<topic>/files/kiki_narrator.txt`.
2. **Audio Drop**: The creator drops their voiceover file into `output/work/<topic>/files/`:
   - If named `kikivoice-tts-file-*.mp3`, the engine automatically renames it to `narrator.mp3`.
3. **Whisper Transcription & Forced Alignment**:
   - The engine processes `narrator.mp3` with Whisper (local `base` or `small` model).
   - Generates scene audio clips (`scene_01_l00.wav` through `scene_08_l00.wav`).
   - Generates corresponding JSON files (`scene_01_l00.json`) containing word-level start and end timestamps.
4. **Inter-Chunk Pause Hygiene**:
   - Split clip padding: `TAIL_PAD = 0.04s`, `MAX_GAP = 0.04s`.
   - Never insert manual dead-air pauses ($\ge 0.30s$) that break conversational momentum.

---

## 4. Procedural Audio Synthesis via RealityShift Core

The RealityShift engine (`core/engine.py`) provides built-in procedural synthesis routines for sci-fi sound design without external sample libraries:

### 4.1 Built-in Audio Generators
- `procedural_whoosh(duration=0.3, freq_start=150, freq_end=800)`: Frequency-swept filtered noise for whip transitions and fast pans.
- `sub_bass_drop(duration=1.2, f_start=90, f_end=35)`: Deep resonant sine drop for cataclysmic revelations and title hits.
- `telemetry_blip(freq=1200, duration=0.05)`: High-frequency sine burst for HUD telemetry updates.
- `cosmic_ambient_bed(duration=60.0, style="tension")`: Synthesized multi-oscillator bed with low-frequency drone and slow harmonic modulation.

### 4.2 Master Bus Limiting & Anti-Clipping Guardrail
Before final muxing with the video stream, the master audio mix is processed through a soft-knee lookahead peak limiter:
$$\text{Output Peak} \le -1.0\text{ dBFS}$$
$$\text{Total Harmonic Distortion (THD)} < 0.1\%$$
If any frame in the audio buffer exceeds $-0.5\text{ dBFS}$, the pipeline triggers an automatic gain reduction pass and logs a warning.

