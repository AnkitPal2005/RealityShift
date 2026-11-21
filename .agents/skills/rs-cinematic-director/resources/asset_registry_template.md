# RealityShift Asset Registry & Continuity Ledger: [TOPIC NAME]

This template catalogs all visual, audio, and graphic assets required to produce a single RealityShift YouTube Short.

---

## 1. Asset Registry Overview

| Project Topic | Target Runtime | Canvas Format | Aspect Ratio | Color Profile | Master Font |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **[TOPIC NAME]** | [e.g. 54s] | $1080 \times 1920\text{ px}$ | 9:16 Vertical | Rec.709 (sRGB) | Consolas / Impact |

---

## 2. Master Asset Ledger

```text
TAXONOMY:
AST-XX = Celestial Bodies, Main Characters, Hero Technology, Primary Subject Stills
ENV-XX = Environments, Space Voids, Cityscapes, Ocean Harbors
PRP-XX = Physical Props, Stranded Ships, Debris, Instruments
OVR-XX = Procedural Overlays, HUD Ribbons, Vector Cones, Reticles
AUD-XX = Master Voiceover Clips, Synthesized Music Bed, Specific SFX
```

### Table of Registered Assets

| Asset ID | Category | Asset Name | Media Format | Visual / Audio Anchor Description | Source / Tool | Referenced in Shots |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AST-01** | Celestial | [Full Moon in Space] | PNG (9:16, 2160x3840) | Silver-grey regolith, sharp Tycho crater, razor-sharp shadows | Midjourney / Flux | S01-A, S02-A |
| **AST-02** | Celestial | [Earth Orbital View] | PNG (9:16, 2160x3840) | Deep sapphire oceans, thin blue atmospheric rim, cloud bands | Midjourney / Flux | S02-A, S05-A, S06-A |
| **ENV-01** | Space | [Deep Space Void] | PNG (9:16, 2160x3840) | True obsidian black (#04060B), non-twinkling pinhole stars | Midjourney / Flux | S01-A, S02-A, S06-A |
| **ENV-02** | Urban | [Metropolis Coastal Shore]| PNG (9:16, 2160x3840) | Curved waterfront promenade, dark street reflections, twilight | Midjourney / Flux | S03-A |
| **ENV-03** | Marine | [Exposed Harbor Mudflats]| PNG (9:16, 2160x3840) | Wet bronze mud, shallow tidal pools, coastal horizon under stars | Midjourney / Flux | S04-A |
| **PRP-01** | Prop | [Stranded Wooden Boats] | PNG (9:16, 2160x3840) | Traditional coastal fishing craft tilted on mudflats | Midjourney / Flux | S04-A |
| **OVR-01** | Graphic | [HUD: THOUGHT EXPERIMENT] | SVG / Cairo Vector | Cyan-bordered ribbon (#7FD6B8), capitalized Roman font | Cairo Engine | S01-A |
| **OVR-02** | Graphic | [HUD: AXIS VARIATION] | SVG / Cairo Vector | Amber-bordered ribbon (#FFB347), technical vector arrow | Cairo Engine | S05-A |
| **AUD-01** | Audio | [KikiVoice Master Voice] | WAV (44.1kHz, 16-bit) | Narrator audio split across scene clips via Whisper | KikiVoice | All Shots |
| **AUD-02** | Audio | [Music Bed: Tension 96BPM]| WAV (44.1kHz, 16-bit) | Procedural tension pulse generated via core/engine.py | core/engine.py | S01-A to S04-A |
| **AUD-03** | Audio | [Music Bed: Ambient Pad] | WAV (44.1kHz, 16-bit) | Ethereal cosmic pad generated via core/engine.py | core/engine.py | S05-A to S06-A |

---

## 3. Continuity Constraints Checklist
- [ ] **Lighting Angle Locked**: All orbital space scenes place the primary solar key light at [Direction].
- [ ] **Texture Fidelity**: Earth's continental shapes and cloud patterns match exactly across AST-02 instances.
- [ ] **Resolution Standard**: All AI-generated stills generated at minimum $2160 \times 3840\text{ px}$ (2x oversampled for crisp vertical downsampling to $1080 \times 1920$).
- [ ] **No In-Image Typography**: Confirmed zero text, logos, or numbers present in AI-generated files.

