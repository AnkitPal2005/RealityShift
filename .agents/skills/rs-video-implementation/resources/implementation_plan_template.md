# RealityShift Video Implementation Plan Template

Use this standardized template when creating the technical video implementation plan for any RealityShift YouTube Short.

---

```markdown
# RealityShift Implementation Plan: [EPISODE_TITLE]

- **Topic Slug**: `[topic_slug]`
- **Target Duration**: `[XX]s` (Estimated) / `[YY]s` (Whisper-Verified)
- **Target Resolution**: 1080 x 1920 (9:16 Vertical)
- **Target Frame Rate**: 30.0 fps (CFR)
- **Status**: [DRAFT | PENDING_APPROVAL | APPROVED_FOR_RENDER | RENDER_COMPLETE]
- **Approval Gate Status**: Gate 1 [X] | Gate 2 [X] | Gate 3 [X] | Gate 4 [ ] | Gate 5 [ ] | Gate 6 [ ] | Gate 7 [ ]

---

## 1. Upstream Dependency Verification

| Dependency | File Path | Verification Status | Hash / Timestamp |
| :--- | :--- | :--- | :--- |
| **Research Brief** | `story-pipeline/RealityShift/output/work/[topic]/direction/research_brief.md` | [VERIFIED / PENDING] | [SHA-256 / Date] |
| **Approved Script** | `story-pipeline/RealityShift/output/work/[topic]/direction/script_approved.md` | [VERIFIED / PENDING] | [SHA-256 / Date] |
| **Direction Package**| `story-pipeline/RealityShift/output/work/[topic]/direction/direction_package.md` | [VERIFIED / PENDING] | [SHA-256 / Date] |
| **Master Voiceover** | `story-pipeline/RealityShift/output/work/[topic]/files/narrator.mp3` | [VERIFIED / PENDING] | [SHA-256 / Date] |
| **Whisper Split Clips**| `story-pipeline/RealityShift/output/work/[topic]/files/scene_*_l00.wav` | [VERIFIED / PENDING] | [Clip count & duration] |

---

## 2. Technical Capability Classification

| Feature / Requirement | Classification Tier | Engine Module / Tool | Implementation Approach |
| :--- | :--- | :--- | :--- |
| **Cairo Vector Overlays** | 1. Existing & Verified | `core/engine.py`, `core/lego.py` | Native PyCairo drawing routines. |
| **Whisper Alignment** | 1. Existing & Verified | `core/voice_kit.py` | Local Whisper forced alignment. |
| **Audio Multi-Track Mix** | 1. Existing & Verified | `core/engine.py` | MoviePy AudioFileClip + procedural bed. |
| **Ken Burns 2.5D Motion** | 2. Current Deps (New Code)| `core/engine.py` extension | Parametric scale/pan generator with cubic easing. |
| **Multi-Layer Composite** | 2. Current Deps (New Code)| `core/engine.py` extension | MoviePy CompositeVideoClip stacking 5 layers. |
| **Media Policy Whitelist** | 2. Current Deps (New Code)| `core/policy.py` modification | Formal user approval to whitelist `images/processed/`. |
| **AI Visual Generation** | 3. External Tool | Midjourney / Flux / Runway | Offline generation by creator/director. |

---

## 3. Scene-by-Scene Implementation Matrix

### Scene [XX]: [SCENE_TITLE]
- **Timecode**: `00:[SS] - 00:[EE]` (Duration: `[DD]s`)
- **Timing Status**: [Estimated (Script) / Ground-Truth (Whisper)]
- **Spoken Voiceover (Hindi)**: `[Exact narration text]`
- **Voiceover Audio Clip**: `files/scene_[XX]_l00.wav`

#### Layer Stacking Specifications:
1. **Layer 1 (Base Visual)**:
   - Asset Source: `images/processed/[ASSET_ID].png` (Resolution: `[W]x[H]`)
   - Motion Dynamics: [None / Cosmic Push-In / Cataclysmic Drift] ($S: [S_{start}] \to [S_{end}]$, Easing: `[function]`)
   - Pan Coordinates: Center $([X_1], [Y_1]) \to ([X_2], [Y_2])$
2. **Layer 2 (Atmospheric & Color Bed)**:
   - Palette Grade: [Cosmic Cyan / Singularity Violet / Deep Void / Magma Ember]
   - Border Vignette: [15% / 20% / 25%] opacity
3. **Layer 3 (PyCairo Vector Overlays & HUD)**:
   - Telemetry Elements: `draw_telemetry_box(..., label="[LABEL]", value="[VALUE]")`
   - Safe Zone Check: All elements within $x \in [180, 900]$, $y \in [240, 1150]$
   - Font Used: `[Consolas / Impact]` (Platform fallback verified)
   - Tofu Prevention: 100% Roman transliteration verified.
4. **Layer 4 (Kinetic Subtitles)**:
   - Text Ribbon: `[ROMAN TRANSLITERATION OF SPOKEN TEXT]`
   - Position: $y = 1220$ (Safe zone compliant)
   - Highlight Color: Gold (`#FFE600`) synchronized to `scene_[XX]_l00.json` word timestamps.
5. **Layer 5 (Master Optical Texture)**:
   - Film Grain: 3% opacity procedural noise.

#### Audio & Transition Engineering:
- **Incoming Transition**: [Hard Cut / Whip Pan (0.20s) / Micro Cross-Dissolve (0.20s)]
- **SFX Trigger**: `[sfx_file.wav]` at $t = [SS.ss]$, Volume: `[-X] dBFS`
- **Music Bed Volume**: `[0.10 - 0.12]`, Ducking: `-6 dB` active during narration.

---

## 4. Asset Manifest Audit Summary

- Total Static Image Plates: `[N]`
- Total Dynamic Video Clips: `[N]`
- Total Audio Clips: `[N]`
- Total SFX Elements: `[N]`
- Ingestion Verification: 100% Pass (No corrupt files, no non-sRGB spaces, no aspect violations).

---

## 5. Render Configuration

- **Target Output Path**: `story-pipeline/RealityShift/output/work/[topic]/build/final_output.mp4`
- **Render Profile**: [Preview / Master]
- **FFmpeg Codec**: `libx264` (Profile High, Level 4.2, `yuv420p`, `+faststart`)
- **Audio Codec**: `aac` (320 kbps, 44.1 kHz, Stereo)
- **Target Loudness**: $-14.0\text{ LUFS} \pm 0.5\text{ LUFS}$

---

## 6. Pre-Render & Post-Render Quality Assurance Plan

### Pre-Render Checklist:
- [ ] Research and script consistency verified.
- [ ] No Devanagari text fed to Cairo engine.
- [ ] All image scales clamped $\ge 1.04\times$ (Zero black borders).
- [ ] Policy whitelist approved by user.

### Post-Render Verification:
- [ ] FFprobe stream validation passed ($1080 \times 1920$, $30\text{ fps}$, `yuv420p`).
- [ ] Zero unrendered black frames detected.
- [ ] Master audio true peak $\le -1.0\text{ dBFS}$.
- [ ] Visual audition on mobile safe zone mask passed.

---

## 7. Approval Sign-Off Block

- **Implementation Architect**: `[Agent / Role]`
- **Gate 4 Code Modification Approved By**: `[User Name / Date]`
- **Gate 7 Final Master Approved By**: `[User Name / Date]`
```

