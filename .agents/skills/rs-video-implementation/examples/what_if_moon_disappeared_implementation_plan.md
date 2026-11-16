# RealityShift Video Implementation Plan: What If The Moon Disappeared?

- **Episode Title**: What If The Moon Suddenly Disappeared? (Kya Ho Agar Chaand Achanak Gayab Ho Jaye?)
- **Topic Slug**: `what_if_moon_disappeared`
- **Target Duration**: 58.0s (Estimated Script) / 57.4s (Whisper-Verified Audio)
- **Target Dimensions**: $1080 \times 1920$ (Native 9:16 Vertical)
- **Target Frame Rate**: $30.000\text{ fps}$ CFR (1,722 frames)
- **Status**: APPROVED_FOR_RENDER
- **Approval Gate Progress**:
  - Gate 1: Upstream Asset & Direction Validation [ PASSED ]
  - Gate 2: Technical Feasibility & Capability Check [ PASSED ]
  - Gate 3: Implementation Plan Review [ PASSED ]
  - Gate 4: Production Code & Policy Modification [ APPROVED BY USER ]
  - Gate 5: Pre-Render Asset Verification [ PASSED ]
  - Gate 6: Render Execution & Automated QA [ READY TO EXECUTE ]
  - Gate 7: Human Verification & Final Sign-Off [ PENDING RENDER ]

---

## 1. Upstream Dependency Verification

| Dependency | File Path | Status | Verification Hash / Notes |
| :--- | :--- | :--- | :--- |
| **Research Brief** | `.agents/skills/rs-content-research/examples/what_if_moon_disappeared.md` | VERIFIED | Strict Laskar/Lissauer distinction; light-travel time delay; equilibrium tidal ratio $\approx 0.46$. |
| **Approved Script** | `.agents/skills/rs-script-writer/examples/what_if_moon_disappeared_script.md` | VERIFIED | Conversational Hindi, 7-scene structure, no universal noon/midnight overclaim. |
| **Direction Package**| `.agents/skills/rs-cinematic-director/examples/what_if_moon_disappeared_direction.md` | VERIFIED | Complete 16-section package, 9:16 vertical compositions, safe zones, tool-agnostic prompts. |
| **Master Voiceover** | `story-pipeline/RealityShift/output/work/what_if_moon_disappeared/files/narrator.mp3` | VERIFIED | Recorded audio, 44.1 kHz stereo, -14.2 LUFS. |
| **Whisper Split Clips**| `.../files/scene_01_l00.wav` through `scene_07_l00.wav` | VERIFIED | 7 scene audio files aligned with word-level JSON timestamps. |

---

## 2. Technical Capability Classification

```
1. EXISTING & VERIFIED IN PRODUCTION ENGINE:
   - PyCairo vector rendering and dynamic HUD telemetry (core/engine.py, core/lego.py).
   - Whisper local speech-to-text alignment and timestamp extraction (core/voice_kit.py).
   - Multi-track MoviePy audio mixing and procedural bed generation (core/engine.py).
   - Upload kit packaging and thumbnail metadata (core/upload_kit.py).

2. POSSIBLE WITH CURRENT DEPENDENCIES (REQUIRING NEW COMPOSITOR CODE):
   - 2.5D Ken Burns parametric pan/zoom engine on static AI plates.
   - 5-layer composite stack (Base Visual -> Atmo Grade -> Cairo HUD -> Captions -> Grain).
   - Topic-specific media policy whitelist for output/work/what_if_moon_disappeared/images/processed/.

3. REQUIRES EXTERNAL TOOL / AI MODEL:
   - AI visual plate generation (Midjourney v6 / Flux.1 Pro) generated offline.
   - Master voiceover generation via KikiVoice (user-provided).

4. NOT CURRENTLY FEASIBLE (OUT OF SCOPE):
   - Real-time 3D orbital physics simulation inside MoviePy runtime.
```

---

## 3. Scene-by-Scene Implementation Plan

### Scene 01: The Vanishing (00:00 - 00:05 | Duration: 5.0s | Frames 0 to 149)
- **Narrative Beat**: Hook & Premise Drop.
- **Whisper Voiceover**: *"Agar agle hi pal Chaand achanak gayab ho jaye... toh Earth par kya hoga?"*
- **Audio Clip**: `files/scene_01_l00.wav` ($d = 4.88\text{s}$, padding to $5.00\text{s}$).

#### Visual Compositing Stack:
1. **Layer 1 (Base Visual)**:
   - Source: `images/processed/RS_MOON_SH01_A.png` ($1440 \times 2560$, 9:16).
   - Motion Dynamics: **Cosmic Push-In**. Scale $S(\tau): 1.04 \to 1.16$, Easing: `ease_in_out_cubic`. Center: $(720, 1280) \to (720, 1200)$. Zero black border guaranteed ($S_{min} \ge 1.04$).
2. **Layer 2 (Atmospheric Grade)**:
   - Grade: Singularity Violet to Deep Void. Radial vignette: $18\%$ opacity.
3. **Layer 3 (PyCairo Vector Overlays & HUD)**:
   - Function: `draw_telemetry_box(ctx, x=180, y=280, w=320, h=72, label="ANOMALY EVENT", value="T = 0.00S | MASS LOSS")`.
   - Fonts: `Impact` (Title), `Consolas` (Telemetry). Zero Devanagari text.
4. **Layer 4 (Kinetic Subtitles)**:
   - Ribbon Text: `AGAR AGLE HI PAL CHAAND ACHANAK GAYAB HO JAYE...`
   - Center Position: $x = 540, y = 1220$. Active word highlight: Gold (`#FFE600`).
5. **Layer 5 (Optical Texture)**:
   - 3% procedural grain overlay.

#### Sound Design:
- $t = 0.00\text{s}$: Low sub-bass impact drop (`-4.0 dBFS`).
- $t = 2.40\text{s}$: Vanish sound effect (high-frequency frequency drop + reverb decay).
- Music Bed: Synthesized `tension` bed at nominal volume $0.11$, ducked to $-6.5\text{ dB}$ under narration.

---

### Scene 02: The Speed of Gravity (00:05 - 00:11 | Duration: 6.0s | Frames 150 to 329)
- **Narrative Beat**: Astrophysics Grounding & Gravitational Delay.
- **Whisper Voiceover**: *"Sabse pehle, humein turant kuch pata nahi chalega. Einstein ke mutabiq, gravity light ki speed se travel karti hai. Yaani chaand gayab hone ke kareeb sava second baad tak, Earth ko pata bhi nahi chalega!"*
- **Audio Clip**: `files/scene_02_l00.wav` ($d = 5.92\text{s}$).

#### Visual Compositing Stack:
1. **Layer 1 (Base Visual)**:
   - Source: `images/processed/RS_MOON_SH02_A.png` ($1440 \times 2560$).
   - Motion Dynamics: **Astrophysics Sweep**. Scale $S(\tau): 1.06 \to 1.12$, Pan $C_x: 720 \to 780$.
2. **Layer 2 (Atmospheric Grade)**:
   - Grade: Cosmic Cyan. Vignette: $15\%$.
3. **Layer 3 (PyCairo Vector Overlays & HUD)**:
   - Vector Ripple: Concentric circular wavefront expanding outward from former lunar locus at $c \approx 3 \times 10^5\text{ km/s}$.
   - Telemetry Ribbon: `GRAVITATIONAL DELAY: ~1.28 SEC | BARYCENTER RE-CENTERING: 4,670 KM -> 0 KM`.
   - Bounds: Within safe zone $x \in [180, 900], y \in [240, 1150]$.
4. **Layer 4 (Kinetic Subtitles)**:
   - Ribbon Text: `EINSTEIN KE MUTABIQ, GRAVITY LIGHT KI SPEED SE TRAVEL KARTI HAI`
   - Position: $y = 1220$. Safe zone compliant.
5. **Layer 5 (Optical Texture)**:
   - 3% procedural grain.

#### Sound Design:
- Incoming: Micro cross-dissolve ($0.18\text{s}$) with subtle high-pass whoosh (`-12 dBFS`).
- $t = 1.28\text{s}$ into scene: Subtle gravitational shock pulse (`telemetry_blip` + sub rumble).

---

### Scene 03: Tidal Realignment & Dynamic Oceans (00:11 - 00:20 | Duration: 9.0s | Frames 330 to 599)
- **Narrative Beat**: Escalating Environmental Consequences.
- **Whisper Voiceover**: *"Lekin fir samundar mein badlav aayega. Chaand ke bina, lunar gravitational tides khatam ho jayengi, aur sirf sooraj ki tides bachengi. Ocean basins aur local geography ke mutabiq, samundari lehrein pehle se behad shant aur choti ho jayengi!"*
- **Audio Clip**: `files/scene_03_l00.wav` ($d = 8.86\text{s}$).

#### Visual Compositing Stack:
1. **Layer 1 (Base Visual)**:
   - Source: `images/processed/RS_MOON_SH03_A.png` ($1440 \times 2560$).
   - Motion Dynamics: **Cataclysmic Drift**. Scale $S(\tau): 1.14 \to 1.06$, Pan $C_y: 1240 \to 1340$ (downward reveal of receding shoreline).
2. **Layer 2 (Atmospheric Grade)**:
   - Grade: Deep Ocean Indigo. Vignette: $20\%$.
3. **Layer 3 (PyCairo Vector Overlays & HUD)**:
   - Shoreline Telemetry: Vector water level caliper indicating reduced tidal amplitude.
   - Telemetry Tag: `SOLAR EQUILIBRIUM TIDE: ~46% | BASIN RESONANCE ACTIVE`.
   - Note: Strictly avoids claiming tidal drop is universally 54% or aligned strictly with solar noon/midnight.
4. **Layer 4 (Kinetic Subtitles)**:
   - Ribbon Text: `OCEAN BASINS AUR LOCAL GEOGRAPHY KE MUTABIQ, LEHREIN CHOTI HO JAYENGI`
   - Position: $y = 1220$.
5. **Layer 5 (Optical Texture)**:
   - 3% procedural grain.

#### Sound Design:
- Incoming: Directional whip pan ($0.20\text{s}$) with procedural whoosh (`procedural_whoosh()`).
- Foley: Distant ocean surf rolling back into calm stillness.

---

### Scene 04: The Void of Night & Ecology (00:20 - 00:30 | Duration: 10.0s | Frames 600 to 899)
- **Narrative Beat**: Sensory Escalation & Biosphere Impact.
- **Whisper Voiceover**: *"Aur raat ka aalam? Raat achanak behad kaali ho jayegi. Full moon ki roshni starlight se hazaron guna zyada hoti hai. Iske bina, raat mein shikar karne wale janwar aur marine creatures ka poora ecosystem disorient ho jayega."*
- **Audio Clip**: `files/scene_04_l00.wav` ($d = 9.80\text{s}$).

#### Visual Compositing Stack:
1. **Layer 1 (Base Visual)**:
   - Source: `images/processed/RS_MOON_SH04_A.png` ($1440 \times 2560$).
   - Motion Dynamics: **Cosmic Push-In**. Scale $S(\tau): 1.05 \to 1.15$, Pan Center: $(720, 1280)$.
2. **Layer 2 (Atmospheric Grade)**:
   - Grade: Deep Space Obsidian & Starlight Silver. Vignette: $24\%$.
3. **Layer 3 (PyCairo Vector Overlays & HUD)**:
   - Illuminance Caliper: `ILLUMINANCE DROP: ~0.2 LUX -> 0.001 LUX (STARLIGHT)`.
   - Ecological Radar: Targeting reticle tracking disoriented nocturnal owl in silhouette.
4. **Layer 4 (Kinetic Subtitles)**:
   - Ribbon Text: `FULL MOON KI ROSHNI STARLIGHT SE HAZARON GUNA ZYADA HOTI HAI`
   - Position: $y = 1220$.
5. **Layer 5 (Optical Texture)**:
   - 3% procedural grain.

#### Sound Design:
- Night forest ambience (subtle crickets and wind) abruptly cut off into cold stellar silence.
- Music Bed: Eerie low-frequency drone pad (`tension` profile).

---

### Scene 05: Chaotic Obliquity vs. Long-Term Evolution (00:30 - 00:43 | Duration: 13.0s | Frames 900 to 1289)
- **Narrative Beat**: Scientific Climax & Axial Stability.
- **Whisper Voiceover**: *"Lekin sabse bada khatra hai Earth ka tilt. Chaand hamari 23.5 degree axial tilt ko stabilize karta hai. Iske bina, models dikhate hain ki carodon saalon mein Earth ka tilt chaotic ho sakta hai—jisse climate mein achanak aur bhayanak badlav aa sakte hain!"*
- **Audio Clip**: `files/scene_05_l00.wav` ($d = 12.75\text{s}$).

#### Visual Compositing Stack:
1. **Layer 1 (Base Visual)**:
   - Source: `images/processed/RS_MOON_SH05_A.png` ($1440 \times 2560$).
   - Motion Dynamics: **Astrophysics Sweep with Axial Drift**. Scale $S(\tau): 1.08 \to 1.15$, subtle rotation $\theta: -0.8^\circ \to +0.8^\circ$.
2. **Layer 2 (Atmospheric Grade)**:
   - Grade: Magma Red & Glacial Cyan dual split (representing extreme seasonal variation). Vignette: $18\%$.
3. **Layer 3 (PyCairo Vector Overlays & HUD)**:
   - Vector Orbital Overlay: Earth rotational axis rendered with dynamic dashed cone showing modeled obliquity variation extent of $\approx 20^\circ\text{--}25^\circ$ over hundreds of millions of years.
   - Telemetry Readout: `OBLIQUITY VARIATION EXTENT: ~20-25 DEG (LISSAUER ET AL. 2012) | THEORETICAL CHAOTIC ZONE: 0-85 DEG (LASKAR ET AL. 1993)`.
   - Scientific Accuracy: Explicitly labeled as modeled evolution over hundreds of millions of years; no claim of immediate seasonal catastrophe.
4. **Layer 4 (Kinetic Subtitles)**:
   - Ribbon Text: `CHAAND HAMARI 23.5 DEGREE AXIAL TILT KO STABILIZE KARTA HAI`
   - Position: $y = 1220$.
5. **Layer 5 (Optical Texture)**:
   - 3% procedural grain.

#### Sound Design:
- $t = 0.00\text{s}$: Resonant cinematic sub-bass impact (`-3.0 dBFS`).
- Music Bed: Dramatic orchestral swell (`march` bed with synthesized brass layer), ducked to $-5.5\text{ dB}$.

---

### Scene 06: The Silent Cosmic Anchor (00:43 - 00:52 | Duration: 9.0s | Frames 1290 to 1559)
- **Narrative Beat**: Philosophical Realization & Synthesis.
- **Whisper Voiceover**: *"Toh Chaand sirf aasman ki sundarta nahi hai... balki yeh hamare planet ko stable rakhne wala ek silent cosmic anchor hai."*
- **Audio Clip**: `files/scene_06_l00.wav` ($d = 8.74\text{s}$).

#### Visual Compositing Stack:
1. **Layer 1 (Base Visual)**:
   - Source: `images/processed/RS_MOON_SH06_A.png` ($1440 \times 2560$).
   - Motion Dynamics: **Introspective Float**. Scale $S(\tau): 1.12 \to 1.06$, Easing: `smoothstep`.
2. **Layer 2 (Atmospheric Grade)**:
   - Grade: Cosmic Cyan & Gold. Vignette: $16\%$.
3. **Layer 3 (PyCairo Vector Overlays & HUD)**:
   - Vector Anchor: Gravitational bonding tether rendered between Earth and Moon with glowing pulse.
   - Telemetry Ribbon: `EARTH-MOON SYSTEM: DUAL GRAVITATIONAL EQUILIBRIUM`.
4. **Layer 4 (Kinetic Subtitles)**:
   - Ribbon Text: `CHAAND HAMARE PLANET KO STABLE RAKHNE WALA SILENT COSMIC ANCHOR HAI`
   - Position: $y = 1220$.
5. **Layer 5 (Optical Texture)**:
   - 3% procedural grain.

#### Sound Design:
- Ambient harmonic chime + warm pad swell.

---

### Scene 07: Climax Question & Channel CTA (00:52 - 00:58 | Duration: 6.0s | Frames 1560 to 1721)
- **Narrative Beat**: Curiosity Loop & Community Action.
- **Whisper Voiceover**: *"Agar Chaand ki jagah Mars hamare orbit mein hota... toh kya hota? Comment karke batao, aur RealityShift ko subscribe karo!"*
- **Audio Clip**: `files/scene_07_l00.wav` ($d = 5.82\text{s}$).

#### Visual Compositing Stack:
1. **Layer 1 (Base Visual)**:
   - Source: `images/processed/RS_MOON_SH07_A.png` ($1440 \times 2560$).
   - Motion Dynamics: **Cosmic Push-In**. Scale $S(\tau): 1.05 \to 1.16$, Pan Center: $(720, 1260)$.
2. **Layer 2 (Atmospheric Grade)**:
   - Grade: Rust Red (Mars) & Cyan. Vignette: $20\%$.
3. **Layer 3 (PyCairo Vector Overlays & HUD)**:
   - Interactive CTA Arrow: Minimal animated chevron pointing towards YouTube Shorts subscribe button.
   - Top Ribbon ($y = 280$): `WHAT IF: MARS ORBITED EARTH?`
   - Clean Screen Rule: Central Martian disc completely unobstructed ($y \in [450, 1100]$ free of clutter).
4. **Layer 4 (Kinetic Subtitles)**:
   - Ribbon Text: `COMMENT KARKE BATAO, AUR REALITYSHIFT KO SUBSCRIBE KARO!`
   - Position: $y = 1220$.
5. **Layer 5 (Optical Texture)**:
   - 3% procedural grain.

#### Sound Design:
- Rhythmic electronic pulse + crisp subscription click SFX.

---

## 4. Master Audio Mixing Schedule

```
Timeline: 00:00 --------------------------------------------------------> 00:58
Track 1 (Voiceover):  [Sc01] [Sc02]  [Sc03]   [Sc04]    [Sc05]    [Sc06]  [Sc07]
Track 2 (Impact SFX): |Hit   |Pulse  |Whip    |Silence  |Swell    |Chime  |Click
Track 3 (Diegetic):   [Vanish]       [Tide Out]         [Rumble]  [Harmonics]
Track 4 (Music Bed):  === Ducked to -6.5 dB during voice; swells +6dB at cuts ===
```

- Master Integrated Loudness Target: $-14.0\text{ LUFS} \pm 0.5\text{ LUFS}$.
- True Peak Ceiling: $-1.2\text{ dBFS}$.
- Zero clipping or audible ducking pumping.

---

## 5. Automated Post-Render QA Verification Plan

1. **FFprobe Integrity**:
   - Verify dimensions are strictly $1080 \times 1920$.
   - Verify frame rate is strictly $30.000\text{ fps}$.
   - Verify duration is $57.40\text{s}$ ($\pm 0.05\text{s}$).
2. **Black Frame Scan**:
   - `ffmpeg -vf "blackdetect=d=0.06:pix_th=0.10" -f null -` must report 0 black intervals.
3. **Devanagari Safety**:
   - All PyCairo strings verified strictly ASCII/Roman transliteration.
4. **Physical Mobile Audit**:
   - Verify all 7 scenes on vertical mobile emulator.
   - Ensure right-side icons and bottom bar do not obstruct shoreline, nocturnal animals, or Mars disc.

