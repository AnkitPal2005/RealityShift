# RealityShift Cinematic Direction Package: [TOPIC NAME IN CAPITALIZED ROMAN]

**Document Type**: RealityShift Cinematic Direction Blueprint  
**Channel**: RealityShift (@RealityShiftByAnkit)  
**Format**: YouTube Shorts (9:16 Vertical / $1080 \times 1920\text{ px}$)  
**Target Duration**: [e.g. 54 Seconds]  
**Primary Pillar**: [Cosmic What-If / Frontier Astrophysics / AI & Singularity / Futuristic Paradox]  
**Source Script**: `.agents/skills/rs-script-writer/examples/[topic_script].md`  
**Source Brief**: `.agents/skills/rs-content-research/examples/[topic_brief].md`  
**Director Persona**: Senior Sci-Fi Film Director & VFX Supervisor  

---

## 1. Creative Vision & High-Concept Logline
- **Visual Logline**: [1-2 sentences capturing the visual journey and emotional arc].
- **Core Aesthetic Thesis**: [e.g. "Contrast the cold, clinical beauty of deep space with the fragile, sudden vulnerability of human coastal civilization under starlight"].
- **Visual Pacing Dynamic**: [How the visual intensity ramps from cold curiosity to systemic crisis to cosmic awe].

---

## 2. Overall Visual Treatment
- **Cinematography Format**: 9:16 Vertical ($1080 \times 1920$), 24fps cinematic aesthetic.
- **Optics & Lens Simulation**: [e.g. 65mm IMAX for deep space vistas, 35mm anamorphic for urban coastal shots].
- **Texture & Film Grain**: Subtle 35mm fine grain (ISO 250), soft optical highlight halation, zero digital noise.
- **Lighting Philosophy**: [e.g. Directional, unsoftened sunlight in vacuum contrasted with atmospheric twilight scattering on Earth].
- **Safe Zone Architecture**:
  - Primary Focal Zone: $y = 380 - 1150$ (central visual area).
  - HUD Ribbon Band: $y = 280 - 380$ (centered at $x = 540$).
  - Kinetic Caption Zone: Existing `lego.py` supported: $y = 1150 - 1250$; Proposed expanded target: $y = 1150 - 1320$.
  - Bottom Clear Zone: Existing `lego.py` clear band: $y > 1520$; Proposed mobile danger margin: $y > 1450$.

---

## 3. Color & Lighting Bible
- **Dominant Base Palette**:
  - Void / Deep Shadow: `#[Hex]`
  - Key Subject Tone: `#[Hex]`
  - Environmental Accent: `#[Hex]`
  - Hazard / Anomaly Vector: `#[Hex]`
- **Key Light Vector**: [e.g. Primary solar key light enters from camera-left at $45^\circ$ across all orbital scenes].
- **Atmospheric & Exposure Mood**: [Contrast ratios, shadow density, specular highlight control].

---

## 4. Subject & Environment Bible
- **Celestial Body 1 ([Name])**: [Defining visual features, surface albedo, crater textures, cloud patterns].
- **Environment 1 ([Name])**: [Atmospheric thickness, urban silhouettes, water reflectance, twilight horizon].
- **Key Hardware / Device ([Name])**: [Materials, geometric form, thruster plumes, surface finish].

---

## 5. Scene-by-Scene Narrative Flow
*Mapping the approved script scenes directly to the cinematic visual journey:*

- **Scene 01 (Hook)**: [Visual beat & intended audience sensation].
- **Scene 02 (Premise)**: [Visual beat & scale contrast].
- **Scene 03 (Sensory Shock / Myth Bust)**: [Visual beat & real-world grounding].
- **Scene 04 (Systemic Shift)**: [Visual beat & environmental realignment].
- **Scene 05 (Climax / Paradox)**: [Visual beat & deep-time cosmic perspective].
- **Scene 06 (Outro / CTA)**: [Visual beat & interactive contemplation].

---

## 6. Shot-by-Shot Timing & Camera Choreography

| Shot ID | Scene Ref | Timestamp | Dur (s) | Subject & Action | Framing & Angle | Camera Movement | FG / MG / BG Layers | Transition In / Out | Asset IDs | Media Type |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **S01-A** | Scene 01 | 0:00-0:04 | 4.0s | [Action] | EWS, High Orbit | Static Hold $\to$ Push | FG: Void / MG: Moon / BG: Earth | Hard Cut / Cut | AST-01, ENV-01 | AI Still + 2.5D |
| **S02-A** | Scene 02 | 0:04-0:13 | 9.0s | [Action] | WS, Orbital Grid | Slow Push-In | FG: HUD / MG: Earth-Moon / BG: Stars | Cut / Cut | AST-01, AST-02 | AI Still + HUD |
| **S03-A** | Scene 03 | 0:13-0:24 | 11.0s| [Action] | Split: City/Harbor| Slow Vertical Pan | FG: Rails / MG: Water / BG: Sky | Cut / Cut | ENV-02, PRP-01 | AI Video or 2.5D |
| **S04-A** | Scene 04 | 0:24-0:36 | 12.0s| [Action] | High Drone View | Slow Descent | FG: Rocks / MG: Mudflat / BG: Horizon| Cut / Cut | ENV-03, PRP-02 | AI Still + Shimmer|
| **S05-A** | Scene 05 | 0:36-0:49 | 13.0s| [Action] | Obliquity Drift | Slow Orbital Arc | FG: Obliquity vector / MG: Earth / BG: Cosmos | Cut / Cut | AST-02, OVR-02 | 3D Vector Composite|
| **S06-A** | Scene 06 | 0:49-0:55 | 6.0s | [Action] | Earth in Starlight | Slow Push-In | FG: Arrow / MG: Earth / BG: Starfield| Cut / Fade to Black| AST-02, OVR-03 | AI Still + Motion |

---

## 7. AI Image-Generation Prompts (Tool-Agnostic)

### Prompt AST-01 ([Subject Name])
- **Format**: 9:16 Vertical (`--ar 9:16`)
- **Type**: Photorealistic AI Still
- **Prompt**:
  `[Subject & Core Action]. [Physical Details & Surface Textures]. [Environment & Setting]. [Composition & Vertical Framing]. [Lighting & Exposure]. [Cinematography, Lens & Camera Type]. [Color Palette & Mood]. --ar 9:16 --style raw`
- **Negative Constraints**:
  `--no text, letters, words, watermark, logo, cartoon, anime, illustration, 3d render plastic, saturated neon, low quality, blurry`

*(Repeat for each registered still asset).*

---

## 8. AI Video-Generation Prompts (Temporal Dynamics)

### Video Prompt AST-XX-VID ([Subject Name])
- **Target Platform**: Runway Gen-3 / Luma Dream Machine / Kling / Sora
- **Duration**: [e.g. 4.0 seconds]
- **Camera Trajectory**: [Exact camera path: slow vertical pedestal, smooth dolly push, locked hold].
- **Subject Dynamics**: [Physical motion of subject, fluid dynamics, cloud rotation].
- **Atmosphere & Speed**: [Micro-motion, particle drift, fluid dissipation].

---

## 9. Image-to-Video (I2V) & 2.5D Motion Instructions
*For implementation via Ken Burns scale/pan scripts, depth-map parallax, and particle loops:*

- **Shot [ID]**:
  - *Base Image*: `[Asset ID]`
  - *Pan/Zoom Vector*: Start at $(x_1, y_1, s_1) \to$ End at $(x_2, y_2, s_2)$ using [ease-out-cubic / linear] curve.
  - *Layered Parallax*: Foreground translated by $[\Delta x, \Delta y]$, Midground by $[\Delta x, \Delta y]$, Background static.
  - *Atmospheric Overlay*: [e.g. Subtle drifting cosmic dust at 12% opacity, screen blend mode].

---

## 10. Procedural Graphics & Typography Instructions
*Vector overlays and typography rendered natively by the compositing engine:*

- **HUD Ribbon Specifications**:
  - Position: Centered horizontally at $x = 540$, vertical band $y = 280 - 380$.
  - Typography: Capitalized Roman Text (`Consolas` / `Impact` / `Segoe UI Bold` on Windows; `Liberation Sans Bold` / `DejaVu Sans Bold` / `Courier New` on Linux).
  - Text Content: `[EXACT ROMAN HUD STRING]`
  - Style: Semi-transparent dark panel (`panel` hex), sleek accent outline (`ui` hex).
- **Technical Overlays**:
  - [e.g. Faint vector orbital line, coordinate ticks, gravitational potential mesh].

---

## 11. Asset Registry with Unique IDs

| Asset ID | Category | Name & Description | Visual Seed Anchor | Referenced In |
| :--- | :--- | :--- | :--- | :--- |
| **AST-01** | Celestial | [Full Moon in Deep Space] | [Crater Tycho visible, silver-grey albedo] | S01-A, S02-A |
| **AST-02** | Celestial | [Earth Photorealistic Orbit] | [Sapphire oceans, delicate atmosphere limb] | S02-A, S05-A, S06-A |
| **ENV-01** | Space | [Deep Space Obsidian Void] | [Pinpoint non-twinkling stars, cold black] | S01-A, S02-A, S06-A |
| **ENV-02** | Urban | [Coastal City Waterfront] | [Metropolis skyline, dark sea reflections] | S03-A |
| **PRP-01** | Prop | [Stranded Coastal Fishing Boats]| [Wooden hulls resting in mudflats] | S04-A |
| **OVR-01** | Graphic | [HUD Ribbon: THOUGHT EXPERIMENT]| [Cyan border, capitalized Roman text] | S01-A |

---

## 12. Transition & Sound Design Plan

### 12.1 Transition Choreography
- **S01 $\to$ S02**: [Hard cut on beat / whip pan / cross-dissolve with storytelling rationale].
- **S02 $\to$ S03**: [Transition type & rationale].
- **S03 $\to$ S04**: [Transition type & rationale].
- **S04 $\to$ S05**: [Transition type & rationale].
- **S05 $\to$ S06**: [Transition type & rationale].

### 12.2 Audio Bed & SFX Integration
- **Music Style**: `[tension / ambient / pulse / march]` at [Target BPM].
- **Punctuation SFX**:
  - *Shot 01 ($t=0.0\text{s}$)*: [e.g. Sudden acoustic drop + sub-bass 40Hz impact].
  - *Shot 03 ($t=13.0\text{s}$)*: [e.g. Coastal ambient wind rush].
  - *Shot 05 ($t=36.0\text{s}$)*: [e.g. Resonant orchestral gong + vacuum drop].

---

## 13. Visual Continuity Ledger
- [ ] **Key Light Vector**: Sun position locked at [camera-left / camera-right] across all space scenes.
- [ ] **Planetary Texture & Albedo**: Earth and Moon maintain consistent surface maps and cloud structures.
- [ ] **Color Grade Consistency**: 35mm fine grain and black point calibrated across all shots.
- [ ] **Typography Uniformity**: HUD ribbons maintain uniform font, height, and safe-zone placement.

---

## 14. Scientific Accuracy & Epistemological Warnings
- **`[ESTABLISHED SCIENCE]` Protection**:
  - *Tidal Response*: Removing lunar tidal forcing does not cause universal instant coastal drainage. Solar tides remain. Depicting exposed mudflats is an illustrative local vignette, not a claim of global instantaneous drainage.
  - *Zero Barycenter Physical Lurch*: Earth does not physically shake or lurch when barycentric references shift.
- **`[THEORETICAL MODEL]` Framing**:
  - *Obliquity Variation*: Accurately frame Lissauer et al. (2012) as a modeled extent of obliquity (axial tilt) variation ($\Delta \varepsilon \sim 20^\circ - 25^\circ$) over hundreds of millions of years. Do not confuse with precession, do not present as an absolute tilt angle, and do not depict an immediate 85° flip.
- **Scale Compression Disclosure**: [Explicitly disclose any artistic compression of distance/scale].

---

## 15. Implementation Handoff Notes for Skill 4 (`rs-video-implementation`)

### 15.1 Current Verified Engine Capabilities (Ready for Execution)
- MoviePy / FFmpeg video compilation ($1080 \times 1920$, 30fps).
- High-precision audio mixing (KikiVoice split clips + synthesized music bed + procedural SFX).
- Whisper-synced kinetic subtitles in existing caption band (`CAP_TOP, CAP_BOTTOM = 1150, 1250`).
- Cairo-based procedural HUD ribbon rendering (`OVR-01` through `OVR-06`) at $y = 300$.
- 2.5D Ken Burns scale/pan animation on static high-resolution AI images.

### 15.2 Proposed Renderer Enhancements for Skill 4
- Optional expansion of caption band to $y = 1150 - 1320$ if multi-line kinetic text is required.
- Runtime font availability verification (checking Windows vs. Linux fallbacks).
- Ingesting external AI-generated stills dropped into `story-pipeline/RealityShift/output/work/<short>/images/`.

---

## 16. Final Cinematic QA Checklist
*(Verified against `resources/cinematic_qa_checklist.md`)*
- [ ] All 16 sections complete and internally consistent.
- [ ] Script order and narration references 100% faithful to approved script.
- [ ] 9:16 vertical safe zones respected for all focal subjects.
- [ ] Scientific boundary conditions strictly enforced.
- [ ] User approval gate established: `PENDING HUMAN APPROVAL`.
