# RealityShift Render Quality Assurance Checklist

This checklist must be executed and fully marked before any RealityShift Short is finalized, exported, or presented for upload delivery.

---

## Phase 1: Pre-Render Ingestion & Code Audit

- [ ] **Dependency Alignment**:
  - [ ] Research brief (`research_brief.md`) is approved and scientifically verified.
  - [ ] Script (`script_approved.md`) matches the approved research without overclaims.
  - [ ] Cinematic direction package (`direction_package.md`) is complete and approved.
- [ ] **Voiceover Audio Presence**:
  - [ ] Creator voiceover file is placed at `files/narrator.mp3` (or renamed from `kikivoice-*.mp3`).
  - [ ] Whisper forced alignment has completed, producing `scene_XX_l00.wav` and `scene_XX_l00.json`.
  - [ ] Ground-truth Whisper timestamps are loaded; no estimated timings remain active.
- [ ] **Asset Validation**:
  - [ ] All AI still plates are $\ge 1080 \times 1920$ (recommended $\ge 1440 \times 2560$) and sRGB.
  - [ ] All AI video clips are constant 30.0 fps, `yuv420p`, and 1080x1920.
  - [ ] Asset checksums match `manifest.json`.
- [ ] **Code & Policy Safety**:
  - [ ] Policy modification in `core/policy.py` to allow `images/processed/` has explicit user approval.
  - [ ] Zero unescaped PyCairo coordinate transforms (every `ctx.save()` paired with `ctx.restore()`).
  - [ ] Zero Devanagari text fed to PyCairo functions (100% Roman transliteration for on-screen HUD).

---

## Phase 2: Visual Composition & Motion Audit

- [ ] **Camera Motion Safety**:
  - [ ] Minimum scale $S_{min} \ge 1.04\times$ enforced on all Ken Burns clips.
  - [ ] Pan coordinates clamped strictly inside image boundaries; zero black voids or borders.
  - [ ] Easing curves applied (no robotic linear panning).
- [ ] **YouTube Shorts Safe Zones**:
  - [ ] Top header ($y \in [0, 180]$) contains no critical graphics or text.
  - [ ] Focal visual subjects centered within $x \in [180, 900]$ and $y \in [240, 1150]$.
  - [ ] Kinetic subtitle band centered in $y \in [1150, 1320]$.
  - [ ] Bottom UI danger band ($y \ge 1450$, and right-side $x \ge 880, y \ge 800$) is 100% clear.
- [ ] **Typography & Glyphs**:
  - [ ] Zero tofu boxes (`□□□`) across all frames.
  - [ ] High contrast maintained between captions and background plates.
  - [ ] Active spoken word highlighted accurately in gold (`#FFE600`).
- [ ] **Optical Cohesion**:
  - [ ] Master film grain overlay ($2\text{--}4\%$) applied uniformly across all scenes.
  - [ ] Color grade harmonizes AI visuals with Cairo vector elements.

---

## Phase 3: Audio Engineering & Sync Audit

- [ ] **Loudness & Dynamics**:
  - [ ] Integrated master loudness within $-14.0\text{ LUFS} \pm 1.0\text{ LUFS}$.
  - [ ] True peak never exceeds $-1.0\text{ dBFS}$ (Zero clipping or digital distortion).
  - [ ] Dynamic ducking actively reduces music bed by $-5\text{ to } -7\text{ dB}$ during speech.
- [ ] **Intelligibility**:
  - [ ] Hindi voiceover is $100\%$ crisp, intelligible, and dominant across all scenes.
  - [ ] Mid-frequency notch EQ ($1.5\text{ kHz}$) applied to music bed to carve room for voice.
- [ ] **Transition Synchronization**:
  - [ ] Whoosh / riser SFX peaks land exactly on visual cut boundaries ($t = 0.0\text{s}$).
  - [ ] Inter-chunk pause duration between scenes is tight ($0.02\text{--}0.04\text{s}$).

---

## Phase 4: Automated Container & Stream Verification

- [ ] **Video Stream**:
  - [ ] Dimensions: exactly $1080 \times 1920$.
  - [ ] Frame rate: exactly $30.000\text{ fps}$ CFR.
  - [ ] Codec: `h264` (High Profile, Level 4.2).
  - [ ] Pixel format: `yuv420p`.
- [ ] **Audio Stream**:
  - [ ] Codec: `aac`.
  - [ ] Bitrate: $320\text{ kbps}$.
  - [ ] Sample rate: $44.1\text{ kHz}$ or $48.0\text{ kHz}$.
- [ ] **Container Integrity**:
  - [ ] `+faststart` moov atom located at container header.
  - [ ] Audio and video stream duration delta $\le 0.05\text{s}$.
  - [ ] Black frame detector reports zero continuous black gaps $> 0.06\text{s}$.

---

## Phase 5: Human Audition & Final Sign-Off

- [ ] Played on mobile screen or mobile viewport emulator.
- [ ] First 3-second hook tested for immediate retention hold.
- [ ] Scientific visual representations adhere to 3-tier boundary (no speculative claims shown as facts).
- [ ] **Gate 7 Final Delivery Approved**: [ YES / NO ]
- **Reviewer Signature**: `_______________________`
- **Date**: `YYYY-MM-DD`

