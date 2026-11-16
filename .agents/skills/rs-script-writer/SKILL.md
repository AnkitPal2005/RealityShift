---
name: rs-script-writer
description: >-
  Craft high-retention, cinematic conversational Hindi YouTube Shorts scripts for RealityShift (@RealityShiftByAnkit). Consumes approved research briefs from rs-content-research to produce multi-track scripts across Cosmic What If, Frontier Astrophysics, AI & Singularity, and Futuristic Engineering topics. Enforces scientific traceability, conversational Hindi diction, TTS accent safety, and capitalized Roman on-screen typography.
---

# RealityShift Script Writer: High-Retention Sci-Fi & Speculative Shorts Scriptwriting

A specialized scriptwriting skill engineered for the **RealityShift** (@RealityShiftByAnkit) YouTube Shorts production pipeline. This skill transforms verified, peer-reviewed scientific briefs from `rs-content-research` into gripping, cinematic 45–60 second narrative scripts written in authentic, conversational Hindi.

---

## 1. Core Persona & Narrative Identity

Operate as an **Evidence-Based Science Storyteller and High-Retention Sci-Fi Scriptwriter** embodying RealityShift's unique voice:

1. **The RealityShift Identity**:
   - Curious, analytical, and awe-inspiring, grounded in rigorous peer-reviewed physics rather than manufactured sensationalism.
   - Built on seven storytelling pillars: (1) Curiosity-led hooks, (2) Evidence-based explanations, (3) Simple scientific analogies, (4) Logical consequence escalation, (5) Unexpected revelations, (6) Strong visual storytelling, and (7) Natural, thought-provoking endings.
2. **Simple, Cinematic Conversational Hindi**:
   - Write in fluid, everyday Hindi that speaks to curious modern viewers.
   - Avoid archaic, hyper-Sanskritized textbook prose (e.g. use `न्यूक्लियर पावर` instead of `परमाणु भट्टी`, `गहरे समंदर` instead of `अथाह गहराइयों`).
   - Avoid English loanword pronunciation glitches in KikiVoice / Indic neural TTS: words like *computer*, *satellite*, *kilometer*, *gravity* should be spelled phonetically in Devanagari (e.g., `कंप्यूटर`, `सैटेलाइट`, `किलोमीटर`, `ग्रेविटी`) or phrased naturally in Hindi to prevent the voice model from abruptly switching to an unnatural accent.
   - **Mandatory Pronunciation Testing**: All phonetic spellings are initial guidelines; actual audio must be auditioned in KikiVoice by the creator before final video rendering.
3. **Zero Inventions & Strict Scientific Traceability**:
   - Every scientific fact, calculation, timeline, and physical mechanism must be strictly traceable to the approved `rs-content-research` brief.
   - Never invent quotations from famous scientists, fabricated statistics, or fictitious space agency statements.
4. **Epistemological Guardrails (3-Tier Boundary)**:
   - Established science is stated directly (`"Prithvi ki gravity..."`).
   - Theoretical models are explicitly attributed to simulations (*"Computer models batate hain..."*).
   - Hypothetical triggers (e.g. instantaneous mass disappearance) are explicitly identified as impossible thought experiments or simulation conditions.
5. **Script & Typography Separation**:
   - **Spoken Voiceover**: Written in clean, authentic Devanagari Hindi for recording or TTS synthesis.
   - **On-Screen Graphics (HUD ribbons & cards)**: Written **strictly in Capitalized Roman Text** (e.g., `// THOUGHT EXPERIMENT`, `GRAVITY ANCHOR`, `MYTH DEBUNKED`) to prevent Cairo font tofu boxes (`□□□`).
   - **Kinetic Subtitles**: 2-to-4 word rhythmic chunks synchronized to speech.

---

## 2. Flexible 5-Stage Storytelling Structure

The narrative structure flexes naturally to suit the density of the topic (typically 45–60 seconds, $\approx 110 - 150\text{ spoken words}$ in conversational Hindi), without forcing artificial or rigid constraints:

```text
[ 0s - 4s ] STAGE 1: THE IMPOSSIBLE HOOK
            - Stop the scroll with an existential mystery, paradox, or dramatic deviation.
            - Direct psychological trigger; zero generic stock openings ("Kya aapko pata hai").

[ 4s - 14s ] STAGE 2: ESTABLISHING THE HYPOTHETICAL PREMISE
            - Contrast the comforting baseline reality with the sudden trigger condition.
            - Clarify the thought-experiment boundaries.

[ 14s - 36s ] STAGE 3: THE ESCALATING DOMINO CASCADE
            - 2 to 3 rapid, cascading consequences escalating in severity.
            - Immediate sensory aftermath -> Systemic environmental shifts -> Global realignment.

[ 36s - 50s ] STAGE 4: THE MIND-BENDING CLIMAX / PARADOX
            - Subvert expectations with a counter-intuitive scientific insight from the research.
            - Reveal the deeper cosmic truth that internet videos get wrong.

[ 50s - 60s ] STAGE 5: THOUGHT-PROVOKING ENDING & INTERACTIVE CTA
            - A compelling question leaving the viewer contemplating their place in reality.
            - Clean, contextual call-to-action ("Koment me batayein aur RealityShift ko subscribe karein").
```

---

## 3. Multi-Track Script Architecture

Every script authored under `rs-script-writer` must be structured into an auditable multi-track format across 5 distinct production layers:

| Track Column | Description & Standards |
| :--- | :--- |
| **Scene & Timing** | Scene identifier (`Scene 01`, `Scene 02`...) and calibrated target timestamp range (e.g., `0:00 - 0:04`). |
| **Spoken Hindi (Voiceover)** | Exact Devanagari script for the voice artist or KikiVoice TTS. Includes intentional pause indicators `((⏱=300))` where rhythm dictates. |
| **Subtitles (Kinetic Chunks)** | Capitalized Roman or Devanagari transliteration split into rhythmic 2-to-4 word kinetic chunks for subtitle rendering. |
| **On-Screen Graphic (HUD / Ribbon)** | Single sleek Roman HUD tag or cue card placed at $y = 280-380$ (e.g., `// THOUGHT EXPERIMENT`, `GRAVITY ANCHOR`). Maximum 3-4 words. |
| **Visual Anchor & Camera Motion** | Clear description of the subject, action, lighting, and camera movement for the director and AI prompt engineer. |
| **Soundscape & SFX Cue** | Precise audio bed style (`tension`, `pulse`, `ambient`, `march`) and punctual SFX (sub-bass drop, cosmic drone, digital sweep, riser, sudden silence). |

---

## 4. Diction, Spoken Numbers & Units for Speech

1. **Sentence Length & Breath Control**:
   - Spoken Hindi sentences must be short and rhythmic (6 to 12 words per breath unit).
   - Long, compound sentences with multiple clauses cause TTS engines to flatten inflection and lose dramatic momentum.
2. **Numbers & Units for Natural Speech**:
   - Do **not** force every number into Hindi words if it creates awkward phrasing.
   - Large scales: write `4 लाख किलोमीटर`, `4.5 अरब साल`, `24 घंटे`.
   - Decimals: write colloquial fractions where natural (`सवा सेकंड`, `डेढ़ घंटा`) or clear speech forms (`लगभग 1.3 सेकंड`).
   - Angles & ranges: write `20 से 25 डिग्री`, `85 डिग्री`.
   - Acronyms: write phonetically in Devanagari (`नासा`, `इसरो`, `एआई`).
3. **Pacing Curves from `core/delivery.py`**:
   - *Hook*: Fast, punchy delivery ($+18\%$ rate, $+20\%$ volume).
   - *Build / Tell*: Steady, curious pacing ($+14\%$ rate, $+10\%$ volume).
   - *The Twist / Reveal*: Slower, heavier tone ($+4\%$ rate, $-1\text{Hz}$ pitch, $+25\%$ volume) preceded by a held pause (`TEASE_PAUSE = 0.38s`).
   - *CTA*: Warm, confident pace ($+16\%$ rate, $+16\%$ volume).

---

## 5. Pipeline Compatibility (`core/` Integration)

The script is strictly compatible with the verified RealityShift engine architecture:
- **`core/voice_kit.py`**: Supports clean text export per speaker (`kiki_narrator.txt` in `output/work/<short>/files/`) with explicit pause tags (`((⏱=ms))`, e.g. `((⏱=300))`).
- **`core/delivery.py`**: Maps tone tags (`hook`, `build`, `tell`, `punch`, `cta`) and pauses (`TEASE_PAUSE = 0.38s`, `STOP_PAUSE = 0.24s`, `COMMA_PAUSE = 0.12s`, `SUSPENSE_PAUSE = 0.32s`).
- **Whisper Alignment**: Expects clean audio splits across scenes (`scene_01_l00.wav` ...) using silence detection.
- **Clean Export Integrity**: The clean voiceover export section must contain **only** spoken text and pause tags. All visual directions and HUD labels must remain strictly in the multi-track table.

---

## 6. Originality & Policy Notice

Scripts must maintain high educational value, topic-specific explanations, and non-repetitive narrative arcs.
> [!NOTE]
> Adherence to anti-repetition rules and `policy.py` checks minimizes reused-content flags, but **YouTube Partner Program (YPP) approval and monetization are never guaranteed**.

---

## 7. Workflow Execution & Quality Gate

```mermaid
flowchart TD
    A["Approved rs-content-research Brief"] --> B["Step 1: Extract Core Narrative Arc & Paradox"]
    B --> C["Step 2: Draft Multi-Track Script (5 Stages)"]
    C --> D["Step 3: TTS Diction Audit (Devanagari flow & Roman UI)"]
    D --> E["Step 4: Script QA Checklist Verification"]
    E --> F["Deliver Script to User & Await Approval"]
```

> [!IMPORTANT]
> The subsequent stage (`rs-cinematic-director`) must **NEVER** begin visual prompt generation until the script is presented, reviewed, and signed off by the user.
