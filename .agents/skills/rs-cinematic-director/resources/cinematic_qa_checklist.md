# RealityShift Cinematic QA & Verification Checklist

Before any cinematic direction package authored by `rs-cinematic-director` is finalized or handed off to Skill 4 (`rs-video-implementation`), it must satisfy 100% of the checks in this audit checklist.

---

## 1. Input Integrity & Approval Gate Checks

- [ ] **1.1 Approved Research Brief Ingested**: Is the direction package based on a finalized, approved brief from `rs-content-research`?
- [ ] **1.2 Approved Script Ingested**: Is the direction package based on an approved script from `rs-script-writer` without any silent script rewrites?
- [ ] **1.3 Script Order & Timing Preserved**: Do the scene IDs, shot durations, and narration lines exactly match the approved script?

---

## 2. Scientific Accuracy & Visual Boundaries

- [ ] **2.1 Three-Tier Reality Boundary Maintained**: Are visuals categorized strictly as `[ESTABLISHED SCIENCE]`, `[THEORETICAL MODEL]`, or `[SPECULATIVE WHAT-IF]`?
- [ ] **2.2 Ocean & Tidal Response Rigor**:
  - In Moon-disappearance scenarios, does the direction avoid depicting instant universal ocean drainage or disappearing tides?
  - Does the direction distinguish between the removal of lunar forcing, the ocean's dynamic adjustment, and the persistence of solar tides?
  - Are low-tide harbor scenes explicitly marked as `[ILLUSTRATIVE VIGNETTE]` showing local altered tidal rhythms, not an established claim of immediate global drainage?
- [ ] **2.3 Obliquity vs. Precession Accuracy**:
  - Is the Lissauer et al. (2012) finding accurately described as an approximate extent of obliquity (axial tilt) variation ($\Delta \varepsilon \sim 20^\circ - 25^\circ$) under modeled conditions over hundreds of millions of years?
  - Has the director avoided confusing obliquity variation with gyroscopic precession or presenting 20°–25° as an absolute tilt interval?
  - Is an immediate axis shift or inevitable 85° tumble explicitly prohibited?
  - Is the obliquity visualization labeled as a theoretical/model-based simulation rather than a deterministic prediction of Earth's exact future motion?
- [ ] **2.4 Zero Disproven Visual Tropes**:
  - Are 500m mega-tsunamis completely prohibited?
  - Does the direction avoid depicting Earth violently shaking, cracking, or lurching when barycentric references shift?
- [ ] **2.5 Scale Compression Explicitly Disclosed**: Are any artistic compressions of astronomical distance or planetary scale clearly flagged with an `[ARTISTIC SCALE COMPRESSION]` notice?

---

## 3. Shorts-First Framing & Mobile Safe Zones

- [ ] **3.1 9:16 Vertical Canvas**: Is every shot natively composed for a $1080 \times 1920$ vertical canvas?
- [ ] **3.2 Primary Focal Zone Respected**: Are all primary subjects, faces, and critical action points positioned within the safe vertical window ($y = 380 - 1150$)?
- [ ] **3.3 HUD Ribbon Safe Zone Respected**: Are on-screen HUD text elements centered at $x = 540$ and placed in the $y = 280 - 380$ band?
- [ ] **3.4 Safe-Zone Compatibility Distinctions Made**:
  - Is the existing renderer's caption band (`lego.py`: $y = 1150 - 1250$) and clear margin ($y > 1520$) clearly distinguished from the proposed cinematic target ($y = 1150 - 1320$ caption band, $y > 1450$ mobile danger margin)?
  - Are any proposed safe-zone expansions documented as implementation requirements for Skill 4 rather than assumed existing features?

---

## 4. Prompt Engineering & Visual Continuity

- [ ] **4.1 Zero Text in AI Prompts**: Are AI image and video prompts completely devoid of requests for readable text, numbers, or logos?
- [ ] **4.2 Complete Prompt Architecture**: Does every image prompt specify Subject, Physical Details, Environment, Composition, Lighting, Lens/Camera, and Negative Constraints?
- [ ] **4.3 Tool-Agnostic Phrasing**: Are prompts formulated using optical/cinematic terms compatible with Midjourney, Flux, Stable Diffusion, or Runway without proprietary syntax locking?
- [ ] **4.4 Asset Registry Completeness**: Does every shot reference valid, pre-registered Asset IDs (`AST-XX`, `ENV-XX`, `PRP-XX`, `OVR-XX`)?
- [ ] **4.5 Key Light Vector Consistency**: Is the primary solar light angle consistent across sequential space shots?
- [ ] **4.6 Planetary Texture Consistency**: Do Earth and recurring celestial bodies maintain identical landmass, cloud, and atmospheric colors across different shots?

---

## 5. Implementation Feasibility & Font Verification

- [ ] **5.1 Verified vs. Future Capabilities Separated**: Does Section 15 clearly separate currently supported pipeline features (2.5D Ken Burns, MoviePy/Cairo composite, Whisper subtitles) from future/external requirements (AI image generation, Runway video generation)?
- [ ] **5.2 Font Compatibility Documented**: Are specified fonts (`Impact`, `Consolas`, `Segoe UI Bold`) documented as preferred candidates with cross-platform fallbacks (`Liberation Sans Bold`, `DejaVu Sans Bold`, `Courier New`), requiring runtime verification in Skill 4?
- [ ] **5.3 Motion Directions Feasible**: Are camera movements realistic for either Ken Burns programmatic pan/zoom or AI video generators, with complex moves flagged?
- [ ] **5.4 Sound Design Synchronized**: Do SFX cues and music bed shifts correspond to narrative turning points in the script?
- [ ] **5.5 Human Approval Gate Enforced**: Is the package marked as `PENDING HUMAN APPROVAL`, explicitly requiring user sign-off before Skill 4 video assembly begins?
