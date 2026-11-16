# RealityShift Final Delivery Package Template

Use this template to package the final deliverables, clickable links, and YouTube upload metadata for a completed RealityShift Short.

---

```markdown
# RealityShift Delivery Package: [EPISODE_TITLE]

- **Topic Slug**: `[topic_slug]`
- **Render Completion Timestamp**: `[YYYY-MM-DD HH:MM:SS UTC]`
- **Video Duration**: `[XX.XX]s` (Total frames: `[NNNN]`)
- **Render Engine**: RealityShift Core 2.0 (MoviePy + PyCairo + FFmpeg)

---

## 1. Master Output Deliverables (Clickable File Links)

- Master Video ($1080 \times 1920$, 30fps, H.264/AAC):
  - [final_output.mp4](file:///story-pipeline/RealityShift/output/work/[topic]/build/final_output.mp4)
- YouTube Thumbnail Master ($1080 \times 1920$ / $1280 \times 720$ extract):
  - [thumbnail_master.png](file:///story-pipeline/RealityShift/output/work/[topic]/build/thumbnail_master.png)
- Preview Frames Archive:
  - [preview_frames/](file:///story-pipeline/RealityShift/output/work/[topic]/build/preview_frames/)
- Render & QA Verification Log:
  - [render.log](file:///story-pipeline/RealityShift/output/work/[topic]/build/render.log)

---

## 2. YouTube Upload Kit

### 2.1 Title Options

- **Option A (High-Curiosity Cosmic What If)**:
  `[Title Option A - Under 60 characters]` (Character count: `[XX]`)
- **Option B (Cataclysmic Mystery)**:
  `[Title Option B - Under 60 characters]` (Character count: `[XX]`)
- **Option C (Astrophysics Question)**:
  `[Title Option C - Under 60 characters]` (Character count: `[XX]`)

### 2.2 Video Description

```
[HOOK_LINE - Visible before "...more" button on mobile, under 120 chars]

[CONCISE SCIENTIFIC SYNOPSIS - 2-3 sentences explaining the core physics without spoiling the climax]

Scientific Sources & Modeling:
1. [Primary Research Citation 1: Authors, Journal, Year]
2. [Primary Research Citation 2: Authors, Journal, Year]

Follow @RealityShiftByAnkit for mind-bending science, space exploration, and futuristic "What If" scenarios!

#Space #Science #Astronomy #WhatIf #CosmicScience #Astrophysics #RealityShift #Shorts
```

### 2.3 Pinned Community Comment

```
[A provocative, open-ended question designed to drive passionate discussion and debates in the comments section]
👇 Aapki kya rai hai? Let me know in the comments!
```

### 2.4 Video Tags (Metadata)

```
RealityShift, Ankit, Space, Science, Astrophysics, What If, Cosmic Mystery, Hindi Science, Space Documentary, [Topic Specific Tag 1], [Topic Specific Tag 2], [Topic Specific Tag 3], Science Shorts
```

---

## 3. QA Audit & Verification Sign-Off

| Metric / Check | Required Specification | Measured Value | Result |
| :--- | :--- | :--- | :--- |
| **Video Dimensions** | $1080 \times 1920$ px | `1080 x 1920` | PASS |
| **Frame Rate** | $30.000\text{ fps}$ CFR | `30.00 fps` | PASS |
| **Video Codec** | H.264 / `yuv420p` | `h264 (High)` | PASS |
| **Integrated Loudness**| $-14.0\text{ LUFS} \pm 1.0\text{ LUFS}$| `[-14.2] LUFS` | PASS |
| **True Peak Level** | $\le -1.0\text{ dBFS}$ | `[-1.2] dBFS` | PASS |
| **Black Frames** | 0 frames ($> 0.06\text{s}$) | `0 detected` | PASS |
| **A/V Sync Offset** | $\le 0.05\text{s}$ | `[0.01]s` | PASS |
| **Tofu Characters** | 0 missing glyphs (`□□□`) | `0 detected` | PASS |
| **Safe Zone Integrity**| Subtitles in $y \in [1150, 1320]$ | `Verified` | PASS |

---

## 4. Production Pipeline Archival Status

- Ingested AI Assets: Stored in `images/processed/` and cataloged in `manifest.json`.
- Whisper Audio Split Clips: Preserved in `files/` for re-render capability.
- Temporary Render Cache: Purged from `build/temp/`.
- Episode Status: **READY FOR UPLOAD**
```

