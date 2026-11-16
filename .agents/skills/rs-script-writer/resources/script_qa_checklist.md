# RealityShift Script QA & Pre-Flight Verification Checklist

Before any script authored by `rs-script-writer` is submitted for review or handed to the visual director, it must satisfy 100% of the checks in this audit checklist.

---

## 1. Research Approval & Scientific Traceability

- [ ] **1.1 Research Dependency Approved**: Is the underlying research brief from `rs-content-research` completed, verified, and approved by the user?
- [ ] **1.2 Complete Claim Traceability**: Is every single fact, number, timescale, and causal mechanism traceable to the approved research brief?
- [ ] **1.3 Zero Hallucinations**: Has the script avoided inventing quotations from famous scientists, fabricated agency statements, or fictitious statistics?
- [ ] **1.4 Hypothetical Premise Clarified**: Are unphysical triggers (such as instantaneous mass disappearance) explicitly identified as impossible thought experiments or simulations rather than physical mechanisms?
- [ ] **1.5 Theoretical vs. Empirical Boundaries**:
  - Are established facts stated directly?
  - Are theoretical models explicitly attributed to simulations (*"Computer models batate hain..."*)?
  - Are climate consequences labeled as model-dependent rather than deterministic?
- [ ] **1.6 Specific Moonless Earth Checks (When Applicable)**:
  - Did the script avoid claiming ocean tides become "exactly half" or that tides universally realign with solar noon/midnight? Does it explain that lunar tidal constituents disappear while solar constituents remain, with actual coastal tide timing and amplitude depending on local geography, bathymetry, ocean-basin dynamics, and resonance?
  - Is Lissauer et al. (2012) described accurately as an extent of variation spanning $\approx 20^\circ - 25^\circ$ under modeled conditions, rather than an absolute tilt interval or conflated with Laskar's theoretical $0^\circ - 85^\circ$ chaotic zone?

---

## 2. Storytelling Quality & Retention Velocity

- [ ] **2.1 Original Storytelling Identity**: Has the script avoided imitating named creators or external channels? Does it embody RealityShift's evidence-based, curiosity-led identity?
- [ ] **2.2 High-Velocity Hook (0–4s)**: Does Scene 01 stop the scroll immediately using an impossible deviation, striking paradox, or urgent question?
- [ ] **2.3 Zero Generic Filler Openers**: Are clichés like *"Kya aapko pata hai?"*, *"Namaste doston"*, or *"Aaj hum baat karenge"* completely eliminated?
- [ ] **2.4 Logical Consequence Escalation**: Does the narrative follow an escalating domino cascade (immediate physical aftermath $\to$ systemic environmental shifts $\to$ long-term realignment)?
- [ ] **2.5 Mind-Bending Climax**: Does Scene 05 deliver an authentic counter-intuitive revelation or existential awe before the call-to-action?
- [ ] **2.6 Interactive Ending**: Does the closing scene ask a provocative, debatable question that stimulates comment discussion?

---

## 3. Conversational Hindi & TTS Pronunciation Safety

- [ ] **3.1 Natural Spoken Hindi**: Is the voiceover written in fluid, everyday conversational Hindi rather than hyper-Sanskritized textbook prose?
- [ ] **3.2 Pronunciation-Safe Terms**: Are English technical terms written in safe phonetic Devanagari (e.g. `कंप्यूटर`, `सैटेलाइट`, `किलोमीटर`, `ग्रेविटी`) or phrased naturally in Hindi to prevent robotic TTS accent switching?
- [ ] **3.3 Spoken Numbers & Units**: Are large numbers, dates, decimals, and measurements formatted naturally for speech (e.g., `4 लाख किलोमीटर`, `लगभग 1.3 सेकंड`, `20 से 25 डिग्री`) without awkward literal translation?
- [ ] **3.4 Clean Narration Export**: Does the clean voiceover export block contain **only** spoken Devanagari text and pause tags, with all camera angles, HUD text, and production directions excluded?
- [ ] **3.5 Mandatory Pronunciation Testing**: Has the creator been reminded that actual KikiVoice audio must be auditioned before final video rendering?

---

## 4. Multi-Track Structure & Pipeline Compatibility

- [ ] **4.1 Five Distinct Tracks Present**: Does every scene provide: (1) Spoken Hindi Voiceover, (2) Subtitle Chunks, (3) On-Screen Roman HUD Ribbon, (4) Visual Anchor & Camera Action, and (5) Audio/SFX Cue?
- [ ] **4.2 Typography & Tofu-Box Prevention**: Are all on-screen graphics, HUD ribbons, and cards strictly written in **Capitalized Roman Text** (e.g., `// THOUGHT EXPERIMENT`, `GRAVITY ANCHOR`) to prevent Cairo font tofu boxes (`□□□`)?
- [ ] **4.3 Pause-Tag Syntax Verified**: Do pause cues use the verified KikiVoice syntax (`((⏱=ms))` where ms is an integer, e.g. `((⏱=300))`), consistent with `core/voice_kit.py`?
- [ ] **4.4 Tone & Pacing Consistency**: Are delivery tones consistent with `core/delivery.py` rhythm curves (`hook`, `build`, `tell`, `punch`, `cta`)?
- [ ] **4.5 Flexible Duration Calibration**: Is the duration appropriately sized to the topic complexity (typically 45–60 seconds, $\approx 110 - 150\text{ words}$) without forcing artificial cuts?

---

## 5. Originality & Quality Gate

- [ ] **5.1 YPP Originality**: Is the script structure original, topic-specific, and non-repetitive? (Note: Adherence to originality guidelines does not guarantee YouTube monetization).
- [ ] **5.2 Complete Packaging Kit**: Are 5 scored title candidates, a pinned comment, and search tags included?
- [ ] **5.3 Stop Gate Enforced**: Is the script marked as `PENDING HUMAN APPROVAL`, explicitly halting work before `rs-cinematic-director` begins?
