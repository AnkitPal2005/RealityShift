# Animation Quality Control (QC) & Validation Checklist

## Overview
This document serves as the operational gate check before and during procedural code implementation in `story-pipeline/SanatanKatha/`. Every katha module must pass 100% of these checks before being presented for human review or rendering.

---

## 1. Pre-Implementation Audit (Input Verification)

- [ ] **Scriptural Research Report Approved**: Verified that the topic has a completed 13-section research report from `content-research` distinguishing Canonical Sanskrit vs. Regional Folk Lore.
- [ ] **Narration Script Frozen**: Verified that the 7–8 scene narration from `katha-writer` is approved with exact word counts, conversational Hindi vocabulary, and explicit pause markers.
- [ ] **Cinematic Blueprint Validated**: Verified that `cinematic-director` has produced scene staging, camera motions, character scales, and 3-tier capability assignments.
- [ ] **Audio Policy Respected**: Voiceover generation is strictly deferred; all provisional timings use $2.3\text{ words/sec} + \text{pauses}$.

---

## 2. Cairo Context & Mathematical State Audit

- [ ] **Context Lifecycle & Ownership**: 
  - Verified that `place(ctx, x, y, s, t, flip)` in `core/devta.py` calls `ctx.save()`, but does **not** call `ctx.restore()`.
  - The custom function or closure invoking `place()` owns the obligation to call `ctx.restore()`.
  - When `Scene.draw(ctx, t, d)` invokes a native or custom character (e.g. `dv.krishna()`), `Scene.draw` does **NOT** call `ctx.restore()`.
- [ ] **Zero Global Matrix Leaks & Unmatched Calls**: Verified that no `ctx.scale(-s, s)` or `ctx.rotate()` operations remain unpopped, and no premature or unmatched `ctx.restore()` calls exist that could pop the compositor camera.
- [ ] **Transform Scoping**: Local transformations (e.g. rotating weapons, scaling cards) are wrapped cleanly inside:
  ```python
  ctx.save()
  try:
      ctx.translate(x, y)
      ctx.scale(s, s)
      # drawing code...
  finally:
      ctx.restore()
  ```
- [ ] **Easing Boundaries**: All progress fractions passed to easing functions are bounded with `clamp(u, 0.0, 1.0)`.

---

## 3. Visual Layout, Framing, & Typography Audit

- [ ] **Character Scale Consistency**: 
  - Recommended standard range for full-body standing dialogue is **`0.68` to `0.80`**.
  - Verified permitted framing exceptions:
    - *Distant/ambient/entering*: $s = 0.30 - 0.60$
    - *Seated figures (Padmasana/lotus throne)*: $s = 0.74 - 0.85$ (with adjusted $y$)
    - *Composite deities (Hari-Hara)*: $s = 0.72 - 0.78$
    - *Close-up busts / Sheesh roop*: $s = 0.85 - 1.10$
    - *Thumbnail covers*: $s = 0.85 - 1.10$
- [ ] **Ground Baseline Alignment**: Characters' feet sit at `GROUND - 10` ($y \approx 1170$).
- [ ] **Headroom & Header Clearance**: The top of the highest crown or peacock feather stays at or below $y \approx 500–550$, leaving ample clearance beneath the top diya header ($y = 78–146$).
- [ ] **Caption Clearance**: No character body or prop intersects the bottom kinetic caption zone ($y = 1290 \pm 100$).
- [ ] **Two-Character Separation**: In two-character encounters, figures are staged at $x \approx 230–250$ and $x \approx 750–850$ (~500px separation), avoiding edge clipping.
- [ ] **Zero Tofu Glyphs (`□□□`)**: All text strings passed to `dv.ribbon()`, `title_card()`, or `text()` with `CAPTION_FONT = "Impact"` use capitalized Roman transliteration (e.g. `"KARM CHAKRA"`, `"SHEESH KYUN?"`).
- [ ] **Clean Screen Rule**: At most **one** single sleek ribbon per scene positioned at $x = 540, y = 280–320$. No stacked ribbons or overlapping cards.
- [ ] **Unobscured Deities**: Central deities in blessing or CTA scenes are never blocked by commentary boxes or large speech bubbles.

---

## 4. Audio, Music, & SFX Audit

- [ ] **Devotional Ambient Bed**: Module sets `MUSIC_STYLE = "ambient"`, avoiding repetitive flute or generic drone tracks.
- [ ] **Tempo & Volume Balance**: `MUSIC_BPM` is set between $80$ and $92$; `MUSIC_VOLUME` is set to $0.10–0.12$.
- [ ] **Zero Awkward Gaps**: `TAIL_PAD = 0.04` and `MAX_GAP = 0.04` to maintain tight, professional storyteller pacing.
- [ ] **No Conch Horn Overuse**: The loud conch horn (`shankh`) is not used repeatedly or trivially; reserved strictly for monumental epic moments.
- [ ] **Valid SFX Keys**: Every SFX string in `events(d)` matches a verified synthetic generator in `core/engine.py:sfx_bank()` (`soft_thud`, `thud`, `boom`, `shimmer`, `ghanti`, `arrow`, `whoosh`).

---

## 5. Scriptural Reverence & Non-Violence Audit

- [ ] **Non-Violent Symbolism**: All sacrifices, martyrdoms, or divine weapon impacts are visualized through radiant light dissolution, golden halos, and showering lotus petals (`dv.petals()`), never gore or physical violence.
- [ ] **Iconographic Accuracy**:
  - Shri Rama wears royal warrior mukut (NO peacock feather!), Raghuvanshi tilak, Kodanda bow.
  - Shri Krishna wears peacock feather (*mor-pankh*), yellow pitambar dhoti, flute or Abhaya mudra.
  - Ascetics, rishis, or hunters (e.g. Jara) do NOT wear royal golden crowns.

---

## 6. The 5-Level Validation Gate & Testing Protocol

Execute all 5 levels in sequence before declaring any story module or template ready:

1. **Level 1 — Python AST Syntax Check**:
   ```bash
   python -m py_compile story-pipeline/SanatanKatha/kathas/<story_name>.py
   ```
   *Gate Rule*: Confirms AST grammar. Does NOT verify imports or runtime behavior.
2. **Level 2 — Module Import Resolution**:
   ```bash
   python -c "import sys; sys.path.insert(0, 'story-pipeline/SanatanKatha'); import kathas.<story_name>"
   ```
   *Gate Rule*: Confirms all symbols and global variables execute without NameError.
3. **Level 3 — Engine Policy & Metadata Gate**:
   ```bash
   python make.py <story_name> --check
   ```
   *Gate Rule*: Confirms YPP originality, hot-words dictionary, and SPEC integrity.
4. **Level 4 — Procedural Drawing Execution (Headless Dry-Run)**:
   *Gate Rule*: Instantiates scene classes and executes `draw(ctx, t, d)` without runtime crashes.
5. **Level 5 — Visual Preview Validation**:
   ```bash
   python make.py <story_name> --preview
   ```
   *Gate Rule*: Renders `output/preview/<story_name>_sheet.png` and `output/preview/<story_name>_thumb.png`.

### Visual Verification Steps:
1. Open `output/preview/<story_name>_sheet.png`:
   - Inspect Row 1 ($t = d \times 0.35$): Verify scene entry, character placement, initial staging.
   - Inspect Row 2 ($t = d \times 0.97$): Verify scene climax, ribbon pop-in, visual payoff.
   - Confirm zero mirrored text, zero tofu boxes, zero overlapping elements.
2. Open `output/preview/<story_name>_thumb.png`:
   - Verify 1080×1920 cover legibility at mobile scale.
   - Verify strong contrast between title typography and background.
   - Verify deity form is prominent and inspiring.

> [!CAUTION]
> Never describe a template or script as "production-tested" merely because it passes Level 1 (`py_compile`). It is only production-tested after completing Level 5 with visual inspection of rendered pixels.

---

## 7. Rollback & Emergency Recovery Protocol

If an animation implementation introduces defects or regressions:
1. **Immediate Reversion**: Revert `kathas/<story_name>.py` to the previous working git commit or backup snapshot:
   ```bash
   git checkout HEAD -- story-pipeline/SanatanKatha/kathas/<story_name>.py
   ```
2. **Clean Preview Output**: Delete stale preview files in `output/preview/<story_name>_*` to prevent caching confusion.
3. **Isolate Root Cause**:
   - Run a Python syntax check: `python -m py_compile kathas/<story_name>.py`.
   - If subtitles are mirrored, search for missing `ctx.restore()` calls following `place()`.
   - If characters are clipped, verify character scale $s \le 0.80$.

