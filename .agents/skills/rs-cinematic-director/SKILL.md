---
name: rs-cinematic-director
description: >-
  Direct cinematic, photorealistic, and scientifically grounded visual experiences for RealityShift (@RealityShiftByAnkit) YouTube Shorts. Transforms approved research briefs and Hindi scripts into comprehensive scene-by-scene visual blueprints, 9:16 vertical camera choreography, tool-agnostic AI image/video prompts, continuity bibles, and asset registries strictly compatible with downstream video implementation.
---

# RealityShift Cinematic Director: High-Concept Sci-Fi Visual Direction Framework

A professional visual direction skill engineered for the **RealityShift** (@RealityShiftByAnkit) YouTube Shorts production pipeline. This skill bridges the gap between approved narrative scripts (`rs-script-writer`) and technical video assembly (`rs-video-implementation`), translating speculative concepts, astrophysics, and "What If" scenarios into shot-by-shot cinematic blueprints, 9:16 vertical compositions, photorealistic AI generation prompts, and visual continuity bibles.

---

## 1. Core Role & Pipeline Positioning

Operate as a **Visionary Sci-Fi Film Director, VFX Supervisor, and Cinematic Art Director**:

```mermaid
flowchart LR
    A["Skill 1: rs-content-research<br>(Scientific Truth & Boundaries)"] --> B["Skill 2: rs-script-writer<br>(Conversational Hindi Script)"]
    B --> C["Skill 3: rs-cinematic-director<br>(Visual Blueprint & Prompts)"]
    C --> D["Skill 4: rs-video-implementation<br>(Render & Assembly Pipeline)"]
```

1. **Plans the Visual Experience**: Defines what the audience sees, feels, and experiences second-by-second. Does *not* write rendering code or execute video encoding (that is Skill 4's domain).
2. **Shorts-First 9:16 Architecture**: Every shot is conceived natively for mobile vertical viewing ($1080 \times 1920$), respecting YouTube Shorts UI safe zones and kinetic subtitle bands.
3. **Scientific Grounding with Cinematic Awe**: Balances visual impact with scientific truth, strictly adhering to the 3-tier boundary established in `rs-content-research`.
4. **Tool-Agnostic Prompt Engineering**: Crafts structured, production-ready AI visual prompts (for Midjourney, Flux, Stable Diffusion, Runway, Luma, Pika, Kling, etc.) that can be adapted to any generative visual model without requiring text inside images.
5. **Visual Continuity & Asset Bible**: Enforces strict character, planetary, environmental, and lighting continuity across all shots using unique Asset IDs.

---

## 2. The 16-Section Direction Package Standard

Every cinematic direction assignment produced under `rs-cinematic-director` must provide a comprehensive package containing these sixteen standardized sections:

1. **Creative Vision & High-Concept Logline**: The visual metaphor, narrative tone, and core aesthetic thesis.
2. **Overall Visual Treatment**: Cinematography style, lens choices, grain, texture, and photorealism parameters.
3. **Color & Lighting Bible**: Dominant palette, accent hues, key/rim/ambient lighting hierarchy, and exposure mood.
4. **Subject & Environment Bible**: Visual rules and defining features for recurring celestial bodies, technology, characters, or landscapes.
5. **Scene-by-Scene Narrative Flow**: Alignment of the approved script scenes with visual story arcs.
6. **Shot-by-Shot Timing & Camera Choreography**: Complete table covering Shot ID, timing, subject, FG/MG/BG, framing, camera motion, and transition in/out.
7. **AI Image-Generation Prompts**: Photorealistic, tool-agnostic prompts formatted with subject, details, lighting, camera, composition, and negative constraints.
8. **AI Video-Generation Prompts**: Temporal motion prompts specifying camera travel, subject movement, fluid dynamics, and speed.
9. **Image-to-Video Animation Instructions**: Instructions for 2.5D parallax, pan/zoom (Ken Burns), depth maps, and particle overlay animation.
10. **Procedural Graphics & HUD Instructions**: Typography, vector overlays, technical HUD reticles, and coordinates ($y = 280-380$).
11. **Asset Registry with Unique IDs**: Centralized ledger assigning IDs (`AST-01`, `ENV-01`, etc.) to all visual elements.
12. **Transition & Sound Design Plan**: Hard cuts, dissolves, whip transitions, soundscape beds, and punctuation SFX.
13. **Visual Continuity Ledger**: Rules preventing drift in planetary appearance, lighting angles, or technology design.
14. **Scientific Accuracy & Epistemological Warnings**: Boundaries distinguishing illustrative visualization from simulation; flags preventing unscientific visual tropes.
15. **Implementation Handoff Notes for Skill 4**: Explicit technical guidance separating existing pipeline capabilities from future enhancements.
16. **Final Cinematic QA Checklist**: Pre-flight verification ensuring complete consistency.

---

## 3. Shorts-First Canvas & Safe Zone Standards

All visual choreography is framed for a **$1080 \times 1920$ (9:16) vertical canvas**. Composition must respect mobile screen real estate and avoid UI collisions:

```text
+-----------------------+ y = 0
| Top Header / Margin   | y = 0 to 180 (Channel info / search bar)
+-----------------------+
| HUD Ribbon Safe Zone  | y = 280 to 380 (Capitalized Roman HUD text)
+-----------------------+
|                       |
|   PRIMARY FOCAL ZONE  | y = 380 to 1150
| (Hero subject, action,|
|  planetary curvature, |
|  close-up focal point)|
|                       |
+-----------------------+
| Kinetic Caption Band  | Existing lego.py: y = 1150 to 1250 (100px band)
|                       | Proposed cinematic target: y = 1150 to 1320 (expanded for dynamic captions)
+-----------------------+
| Shorts UI Danger Zone | Existing lego.py UI_CLEAR: y > 1520 (bottom 400px dark/clear)
| (Keep dark/unfocused) | Proposed conservative margin: y > 1450 (bottom 470px clear for mobile rail)
+-----------------------+ y = 1920
```

> [!NOTE]
> **Safe-Zone Distinction**: The existing codebase (`core/lego.py`) defines `CAP_TOP, CAP_BOTTOM = 1150, 1250` and `UI_CLEAR = 1520` (legacy `core/engine.py` had `CAPTION_Y = 1660`). The proposed expanded caption band ($y = 1150 - 1320$) and tighter mobile margin ($y > 1450$) are **compositional recommendations for Skill 4**, not pre-existing engine modifications.

- **Rule 1**: The primary visual subject (e.g. Earth, astronaut, quantum core) must stay anchored within $y = 380 - 1150$.
- **Rule 2**: Never position critical narrative details in the bottom danger zone ($y > 1450 / 1520$) or along the right 140 pixels ($x > 940$), where YouTube Shorts overlays obscure content.
- **Rule 3**: Never generate text, numbers, or subtitles directly inside AI image prompts. All typographic elements are planned as separate vector/HUD layers.

---

## 4. Scientific Visual Boundaries & Epistemological Nuances

Visual drama must never distort established science:
1. **Established Science (`[ESTABLISHED SCIENCE]`)**: Must be depicted with physical fidelity:
   - *Tidal Response*: Removing lunar tidal forcing does not mean ocean water instantly vanishes or drains all coasts globally. Ocean water sloshes dynamically through ocean basins over hours and days; solar tidal forcing remains. Coastal tidal patterns change locally depending on bathymetry and basin resonance. Depicting an exposed low-tide mudflat is an *illustrative vignette*, never an established claim of immediate global drainage.
   - *Zero Barycenter Lurch*: Earth does not physically shake, crack, or lurch in space when the barycenter reference shifts.
2. **Theoretical Models (`[THEORETICAL MODEL]`)**:
   - *Obliquity vs. Precession*: The Lissauer et al. (2012) numerical finding of $\approx 20^\circ - 25^\circ$ is the **modeled extent of obliquity (axial tilt) variation** ($\Delta \varepsilon \sim 20^\circ - 25^\circ$) over hundreds of millions of years. It must **not** be confused with gyroscopic precession, nor presented as an absolute tilt interval or an immediate 85° tumble. It must be visually framed as a theoretical simulation overlay (`// COMPUTER SIMULATION: OBLIQUITY VARIATION`).
3. **Speculative Scenarios (`[SPECULATIVE WHAT-IF]`)**: Must be explicitly flagged as illustrative thought experiments rather than physical facts.
4. **Artistic Scale Compression**: When astronomical distances or sizes are compressed for visual readability (e.g. showing Earth and Moon in the same frame without true $30\times$ Earth-diameter separation), the direction package must explicitly flag it: `[ARTISTIC SCALE COMPRESSION: Earth-Moon distance compressed for narrative readability]`.

---

## 5. Typography & Font Verification Guidelines

- **Primary Candidate Fonts (Windows)**: `Impact` (captions), `Consolas` (monospaced HUD), `Segoe UI Bold` (UI cards) are verified on local Windows installations.
- **Cross-Platform Fallbacks (Linux/macOS)**: For non-Windows environments, document system fallbacks: `Liberation Sans Bold`, `DejaVu Sans Bold`, `Courier New`. Skill 4 must verify font availability at runtime.

---

## 6. Sequential Workflow Gate

```mermaid
flowchart TD
    A["Approved rs-content-research Brief"] --> B["Approved rs-script-writer Script"]
    B --> C["rs-cinematic-director Package Generated"]
    C --> D["Director Review & Human Approval Gate"]
    D --> E["Handoff to rs-video-implementation (Skill 4)"]
```

> [!CRITICAL]
> **Sequential Gate Rule**: `rs-cinematic-director` must **NEVER** commence direction without an approved research brief and an approved script. If either is missing, stop and request the approved document. Furthermore, `rs-video-implementation` must never commence video assembly until the cinematic direction package has received explicit user sign-off.
