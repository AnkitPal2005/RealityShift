# RealityShift Render Quality Assurance Reference

This reference defines the automated inspection routines, threshold matrices, forensic validation checks, and human verification protocols required before any video is approved for publication.

---

## 1. Automated QA Testing Suite (FFprobe & FFmpeg)

Before presenting any rendered video for human review, the implementation pipeline must run an automated quality control suite.

### 1.1 Technical Stream Validation
```bash
# Extract stream properties in JSON format
ffprobe -v quiet -print_format json -show_format -show_streams build/final_output.mp4 > build/stream_audit.json
```

**Pass Criteria Matrix**:
- `streams[0].width` == 1080
- `streams[0].height` == 1920
- `streams[0].r_frame_rate` == "30/1"
- `streams[0].pix_fmt` == "yuv420p"
- `streams[0].codec_name` == "h264"
- `streams[1].codec_name` == "aac"
- `streams[1].sample_rate` == "44100" (or "48000")
- `abs(format.duration - streams[0].duration) <= 0.05` (A/V sync container alignment)

### 1.2 Black Frame & Dropout Detection
Detects accidental unrendered frames, missing assets, or transition clipping:
```bash
ffmpeg -v error -i build/final_output.mp4 -vf "blackdetect=d=0.06:pix_th=0.10" -f null - 2> build/black_frames.log
```
- **Rule**: `black_frames.log` must be empty. Any continuous black duration $> 0.06\text{s}$ (2 frames) triggers an immediate build failure unless explicitly tagged as a deliberate narrative blackout in the direction package.

### 1.3 Audio Peak & Loudness Audit
Verifies that the master audio mix complies with YouTube delivery standards and contains zero clipping:
```bash
ffmpeg -i build/final_output.mp4 -filter:a ebur128=framelog=verbose -f null - 2> build/loudness.log
```
**Pass Criteria Matrix**:
- **Integrated Loudness ($I$)**: $-14.0\text{ LUFS} \pm 1.0\text{ LUFS}$.
- **Loudness Range ($LRA$)**: $6.0\text{ to } 10.0\text{ LU}$.
- **True Peak ($TP$)**: $\le -1.0\text{ dBTP}$ (Absolute zero clipping allowed).

---

## 2. Automated Visual Defect Inspection

### 2.1 Missing Glyph / Tofu Detection (`□□□`)
- **Risk**: Devanagari text rendered into a Latin font produces blank rectangular boxes (`□□□`).
- **Check**: Parse all text strings passed to PyCairo. Assert that every character belongs to the ASCII / Basic Latin + Latin-1 Supplement range:
  ```python
  def verify_cairo_text_safety(text_string: str):
      for char in text_string:
          if ord(char) > 255:
              raise ValueError(f"UNSAFE CAIRO CHARACTER: '{char}' (U+{ord(char):04X}) detected. All Cairo text must use Roman transliteration!")
  ```

### 2.2 Aspect Ratio & Black Border Scan
- Verify that every ingested image asset covers the vertical viewport without letterboxing or pillarboxing:
  ```python
  def verify_no_letterbox(frame_rgb):
      # Sample edge strips (top 5px, bottom 5px, left 5px, right 5px)
      top_strip = frame_rgb[0:5, :, :]
      bottom_strip = frame_rgb[-5:, :, :]
      left_strip = frame_rgb[:, 0:5, :]
      right_strip = frame_rgb[:, -5:, :]
      for name, strip in [("top", top_strip), ("bottom", bottom_strip), ("left", left_strip), ("right", right_strip)]:
          if strip.mean() < 2.0 and strip.std() < 1.0:
              raise ValueError(f"POSSIBLE LETTERBOX DETECTED: {name} edge appears solid black.")
  ```

---

## 3. Human Quality Review Protocols

Even with $100\%$ automated passes, every short must be audited on a physical mobile device or mobile viewport emulator.

### 3.1 The 4-Point Audition Checklist
1. **Auditory Intelligibility Test**:
   - Play the video at $50\%$ phone volume without headphones in a room with background noise.
   - *Pass*: Is every word of the Hindi voiceover immediately clear without straining?
2. **Visual Safe Zone Test**:
   - Overlay YouTube Shorts UI masks ($y \in [0, 180]$, $y \ge 1450$, and right-side icon zone $x \ge 880, y \ge 800$).
   - *Pass*: Are all scientific diagrams, planet surfaces, and kinetic subtitles unobstructed?
3. **Pacing & Hook Resonance Test**:
   - Watch the first 3 seconds with sound.
   - *Pass*: Does the visual hook and opening line create an irresistible curiosity gap?
4. **Emotional & Narrative Arc Test**:
   - Watch the entire 60-second arc without pausing.
   - *Pass*: Does the transition from immediate shock to escalating physics to philosophical climax feel organic and earned?

---

## 4. Defect Triage & Remediation Matrix

| Defect Observed | Probable Root Cause | Remediation Protocol |
| :--- | :--- | :--- |
| **Voiceover drowned out by music** | Ducking attenuation too low or release time too slow. | Increase sidechain attenuation to $-7.0\text{ dB}$; ensure music bed has $1.5\text{ kHz}$ notch EQ. |
| **Subtitles jumping or drifting** | Desynchronized audio clip lengths; estimated vs Whisper timings. | Re-run Whisper alignment; verify `scene_XX.json` timestamps match audio clip frames exactly. |
| **Black borders during pan** | Camera scale factor dipped below minimum bound $S_{min}$. | Apply $S_{min} \ge 1.04$; clamp pan centers strictly within source bounds. |
| **Flickering textures in AI video** | Temporal instability in AI video generator. | Extract clean still plate and replace with 2.5D Ken Burns zoom. |
| **Missing characters (`□□□`) in HUD**| Raw Hindi string accidentally fed into Cairo. | Convert string to capitalized Roman transliteration. |

