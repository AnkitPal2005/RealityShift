# RealityShift: Visual Continuity & Asset Bible Standards

This reference guide establishes the continuity protocols, naming conventions, and asset registry system to ensure visual coherence across all shots in a RealityShift episode.

---

## 1. The Visual Continuity Imperative

In AI-generated visual productions, the greatest danger is **drift**:
- Earth randomly switches from photorealistic satellite imagery to an oversaturated CGI cartoon.
- The Moon changes its surface color from silver-grey regolith to glowing neon blue.
- Lighting direction abruptly jumps from camera-left to camera-right between two sequential space shots without a camera turn.
- A spacecraft or tech asset changes its structural geometry between cutaways.

To eliminate drift, `rs-cinematic-director` enforces a strict **Visual Bible and Asset Registry System**.

---

## 2. Asset Registry & Naming Conventions

Every visual component required for production is cataloged in the **Asset Registry** before shot-by-shot generation begins. Asset IDs follow this standardized taxonomy:

```text
[AST-XX]  Core Foreground & Midground Visual Assets (Planets, Moons, Stars, Main Characters, Ships)
[ENV-XX]  Background Environments & Landscapes (Deep Space Void, Metropolis Harbor, Orbital Horizon)
[PRP-XX]  Props & Physical Objects (Technical Devices, Stranded Boats, Ocean Buoys)
[OVR-XX]  Graphic Overlays & Procedural HUDs (HUD Ribbons, Grid Lines, Technical Reticles, Vector Arrows)
```

### 2.1 Asset Ledger Structure
Every registered asset must specify:
1. **Asset ID**: Unique identifier (e.g., `AST-01`).
2. **Asset Name**: Human-readable title (e.g., `Photorealistic Earth (Orbital View)`).
3. **Asset Type**: Static Image / Animated Loop / 3D Vector / HUD Overlay.
4. **Visual Anchor & Seed Description**: Defining physical details that must remain locked across all shots.
5. **Key Lighting & Material Properties**: Specular reflection, surface albedo, texture maps, atmospheric limb color.
6. **Referenced In Shots**: Explicit list of shots utilizing this asset (e.g., `Shot 01, Shot 02, Shot 06`).

---

## 3. Four Pillars of Visual Continuity

### 3.1 Astronomical & Celestial Continuity
- **Earth Surface & Clouds**: When Earth appears across multiple scenes, its cloud systems, landmass textures (continents), and atmospheric limb glow must maintain identical color balance (`#1A4B75` oceans, `#38B6FF` atmospheric rim) and photographic fidelity.
- **The Sun & Lighting Vector**: The Sun is the primary key light in space. If sunlight strikes Earth from **camera-left** in Shot 01, it must continue striking from camera-left in Shot 02 unless the camera explicitly undergoes an orbital transit around the terminator.

### 3.2 Environmental & Architectural Continuity
- **Coastal Environments**: If a coastal city skyline (e.g. Mumbai Marine Drive) is shown in Shot 03 with distinctive curved promenade architecture, the subsequent low-tide harbor shot (Shot 04) must preserve identical atmospheric color grading, architectural style, and marine boat types.

### 3.3 Technological & Sci-Fi Asset Continuity
- **Hardware & Spacecraft**: Hull geometry, panel tiling, thruster color (e.g. `#00D2FF` cyan ion plume), and warning markings must stay locked. Generative prompts for recurring spacecraft must share identical prompt descriptors and negative prompt seeds.

### 3.4 Color Grading & Grain Uniformity
- All shots within an episode must share a unified color grade and grain profile (e.g. 35mm fine grain, neutral black point at `#04060B`, natural skin tones, controlled highlight rolloff). Never mix ultra-clean CGI renders with grainy archival film footage in the same narrative sequence without an explicit in-world storytelling justification.

---

## 4. Continuity Tracking Ledger in Direction Packages

Every cinematic direction package must conclude with an explicit **Continuity Ledger** checking off:
- [x] Primary Key Light Vector locked across space shots.
- [x] Celestial body surface textures and albedo verified across scenes.
- [x] Environmental transition logic maintained between day, twilight, and starlight.
- [x] HUD styling, typography, and palette locked to master theme.

