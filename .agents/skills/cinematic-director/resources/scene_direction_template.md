# Cinematic Scene Direction Template (Sanatan Katha)

This template defines the standardized 13-point scene direction specification for translating approved narration scripts into procedural Cairo animation for **Sanatan Katha** YouTube Shorts.

---

## Scene [Number]: [Scene Title]

- **1. Scene Objective**:
  [Narrative, theological, and emotional goal of this scene in 1–2 sentences.]

- **2. Voiceover Dialogue**:
  [Exact Hindi narration lines corresponding to this scene, including pause markers.]

- **3. Duration & Timestamps**:
  - *Scene Duration*: [e.g., 9.7s]
  - *Time Span*: [e.g., 00.0s – 09.7s (Provisional / Measured)]
  - *Word Count*: [e.g., 20 words]

- **4. Characters Present**:
  - [Character 1]: [Sprite name from devta.py, role, scale (0.68–0.80), initial coordinate (x, y)]
  - [Character 2]: [Sprite name, scale, coordinate (if applicable)]

- **5. Character Actions & Expressions**:
  - *Pose*: [e.g., pose="stand", "aim", "shot", "bless"]
  - *Gaze / Look*: [e.g., look=(0.0, 0.0), tracking camera or adversary]
  - *Expression & Mood*: [e.g., mood="fierce", "calm", smile=1.0]
  - *Living Movement*: [Breathing cycle, eye blinking, arm movement, bow draw]

- **6. Background & Environment**:
  - *Setting*: [e.g., Dusk Kurukshetra battlefield, Mahisagara Sangama shoreline, Brahmaloka]
  - *Sky Gradient*: [Top, mid, bottom hex colors]
  - *Scenery Elements*: [Hills, Peepal tree, fire altar, temple pillars, army silhouettes]

- **7. Layer Stacking Order**:
  - *Layer 1 (Far BG)*: [Sky gradient, celestial stars, sun/moon disc]
  - *Layer 2 (Mid BG)*: [Distant hills, silhouetted armies, trees]
  - *Layer 3 (Stage)*: [Ground platform (y = 1180), active characters, fire altar]
  - *Layer 4 (FG Atmosphere)*: [Drifting dust particles, leaping sparks, floating petals]
  - *Layer 5 (UI Overlays)*: [Diya header (y=78–146), Ribbon (y=280–320), Captions (y=1290)]

- **8. Camera Movement**:
  - *Camera Type*: [2D affine push-in, subtle pan, static locked, or impact shake]
  - *Math Transformation*: [e.g., scale = 1.0 + 0.12 * ease_out_cubic(tl / dur) centered on (540, 750)]

- **9. Lighting & Atmosphere**:
  - *Primary Light Source*: [e.g., Setting golden sun, leaping fire glow, divine blue halo]
  - *Radial Glows*: [Coordinates, radius, color, alpha]
  - *Mood Tint*: [Warm amber, twilight purple, radiant celestial white]

- **10. Particles & Visual Effects**:
  - *Particle Type*: [Floating lotus petals (dv.petals), drifting battle dust, leaping flame sparks]
  - *Special FX*: [Sudarshana Chakra spin, Amrita droplets, glowing arrow trail (polyline_at)]

- **11. Transition to Next Scene**:
  - *Transition Type*: [Cross-dissolve, divine white flash, hard cut, silhouette wipe]
  - *Duration*: [e.g., 0.4s flash, 0.6s dissolve]

- **12. Existing Engine Primitives Used**:
  - `dv.<primitive>`: [List exact functions from devta.py and katha.py: e.g., dv.barbarik, dv.krishna, dv.hill, dv.ribbon]

- **13. Unsupported Features / Technical Limitations**:
  - [Explicit identification of any non-procedural visual that must be simplified to fit 2D Cairo, e.g., no 3D cloth physics, no raster blur shaders.]

