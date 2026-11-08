# Divine Stories: Hindi mythology Shorts, fully local and free

`Divine-Stories` is a standalone pipeline that turns a story file into a finished 1080×1920 Hindi YouTube Short
plus a folder ready for manual upload.

```
topic → story JSON (local template + human writing, sourced claims) → public-domain art (Wikimedia Commons)
      → camera moves + Cairo atmosphere → edge-tts narration with word timings → procedural music + SFX
      → captions → FFmpeg render → cover image → QC → policy checklist → upload package (manual)
```

- **No paid APIs.** No keys, accounts or billing. The only network use is edge-tts (Microsoft's free read-aloud service) and Wikimedia Commons.
- **No AI at runtime.** Claude was used only as a development assistant.
- **Separate from Reality Shift.** Divine Stories imports nothing from `../RealityShift`, keeps its own venv, and writes only inside this folder. `tests/test_pipeline.py` checks both.

## Setup

```powershell
cd Divine-Stories
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env      # optional; see the User-Agent note below
.\.venv\Scripts\python.exe -m pytest -q tests
```

Requirements: Python 3.12, FFmpeg and ffprobe on PATH, and the Windows Nirmala UI font (it ships with Windows).

## Making a Short

```powershell
$py = ".\.venv\Scripts\python.exe"
& $py main.py new --slug krishna_govardhan --topic "Why Krishna lifted Govardhan" --characters krishna
#   edit story\library\krishna_govardhan.json (narration, sources, claims, visuals)
& $py main.py search "Ravi Varma Krishna"        # find licence-approved art
& $py main.py validate krishna_govardhan
& $py main.py stills   krishna_govardhan         # contact sheet: check framing before the full render
& $py main.py all      krishna_govardhan         # assets, voice, mix, render, cover, QC, package
```

The result lands in `output\<slug>\upload\`:

| File | What it is |
|---|---|
| `<slug>.mp4` | The finished Short |
| `<slug>_cover.png` | Cover image, plus a feed-size preview |
| `metadata.md` | Title options, description (with sources and image credits), tags, hashtags |
| `checklist.md` | Pre-upload policy checklist with items for you to tick |
| `qc_report.json` | Machine QC results |
| `captions.srt` | Optional closed captions |
| `READY` / `NOT_READY` | Status marker |

Upload by hand in YouTube Studio, starting as **Private** or **Unlisted**.

## Story rules (enforced by `story/schema.py`)

- 8–12 scenes. The first beat must be `hook`; the last must be `question` or `conclusion`. Duration must be 40–60 s.
- Every claim has a `kind` (`scripture`, `regional_tradition` or `popular_interpretation`) and at least one source id.
- Popular beliefs are labelled on screen as "लोक मान्यता". Sources and credits go into the description.
- `review.verified_by` must be filled in by a person who has checked the verse and section numbers. Until then the package is marked `NOT_READY`.
- Visual coordinates (`focus`, `pan`, fx `point`/`origin`/`target`) are **normalized inside `visual.bounds`** (the crop that removes mounts, borders and stamps).

## Visuals: what is possible for free

- **No generative AI.** Photorealistic, consistent AI characters need an image model, which this free, local stack doesn't have.
- **Instead, public-domain classical art.** Raja Ravi Varma Press prints, Pahari and Mughal miniatures, Chola bronzes, CC0 photos of Kailash, and similar.
- **Motion comes from code.** Each still gets a graded virtual camera and procedural layers: light rays, fog, clouds, dust, embers, sparks, lightning, energy waves, poison smoke and a throat glow. The layers sit at different depths to give a 2.5D parallax.
- **Character consistency is per profile.** `characters/profiles/<id>.json` lists approved reference images by role. Close-ups must use `primary_portrait`, and QC rejects anything else.
- **Known limit.** Different paintings show the same deity differently. The profile keeps close-ups on one portrait, and other roles appear only in group or symbolic shots.
- **Resolution varies.** Some public-domain scans are small (about 900 px wide), and close-ups of those look soft.

## Licensing

`generators/commons.py` accepts only **public domain, CC0 and CC BY**. It rejects SA, NC, ND and GFDL. Every download is recorded in `assets/manifest.json` with author, licence, licence URL, source page and SHA-256.

`assets/rights_overrides.json` holds human rights decisions that override Commons' licence tags. Two examples:
- A Nandalal Bose illustration is blocked until **2027-01-01**. India's copyright term is life + 60 years.
- A "CC0" Gita Press magazine cover is blocked permanently.

Music and SFX are synthesised in `audio/synth.py`, so no third-party audio licence is involved.

**User-Agent and rate limits.** Wikimedia asks automated clients to identify themselves with contact info. Without it, original-size downloads get throttled (HTTP 429), and the fetcher falls back to 960 px thumbnails. Set `DS_USER_AGENT` in `.env` to a contact you choose to share.

## Layout

```
config/settings.py        all paths/specs; everything resolves inside this folder
story/                    schema + validation, narrative templates, library/*.json stories
characters/               profiles/*.json + consistency checks
generators/commons.py     Commons search/download, licence filter, manifest, rights overrides
visuals/                  grade.py (colour), camera.py (Ken Burns/clamp), effects.py (Cairo atmosphere)
voice/tts.py              edge-tts per scene, word timings, silence trim + pause capping, cache
audio/                    synth.py (tanpura score, SFX, reverb), mix.py (timeline, ducking, loudnorm)
compositor/               text.py (HarfBuzz→Cairo Devanagari), captions.py, render.py (frames→FFmpeg)
thumbnails/cover.py       Shorts cover
qc/                       checks.py (technical/licensing/consistency QC), policy.py (pre-upload checklist)
upload/package.py         manual-upload package (no API, no credentials)
tests/                    offline unit tests
```

## Costs

Running this costs nothing: no API is billed. The real costs are CPU time and your review time. A render takes a few minutes on a laptop CPU.

Caching means nothing is redone needlessly:
- Images are downloaded once (keyed by title).
- Narration clips are cached by a hash of the text and voice settings.
- Stills let you check framing without a full render.

The automated checklist does **not** guarantee monetization. YouTube's policies decide that.
