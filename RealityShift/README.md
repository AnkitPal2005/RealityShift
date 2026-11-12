# Reality Shift

YouTube Shorts pipeline for the **Reality Shift** channel: Hindi defence and geopolitics explainers (30-90 s,
9:16) with Cairo-drawn motion graphics, a KikiVoice or edge-tts voice-over and a synthesized music bed.

It is separate from `SanatanKatha/` on purpose: its own engine, YPP gate, outputs and
`data/policy_history.json`.

## Commands (run from this folder)

```
python make.py --list                 # every Short and whether it is rendered
python make.py nyoma --check          # YPP policy gate only (no voice spent, nothing rendered)
python make.py nyoma --kiki-export    # KikiVoice: one text file per voice
python make.py nyoma --kiki-split     # cut the downloaded KikiVoice files into lines (+ --check-voice)
python make.py nyoma                  # full render -> output/shorts/nyoma_short.mp4 + upload kit
python make.py nyoma --engine edge    # preview with edge-tts instead of the KikiVoice clips
python make.py nyoma --kit            # rebuild only the upload kit + thumbnail of a rendered Short
```

Every full render writes to `output/shorts/`: `<name>_short.mp4`, `<name>_short.json` (scene log),
`<name>_short_thumb.png` (+ `_feed.png` preview) and `<name>_short_upload.md` (title, description, tags, scores).

## Folder

```
RealityShift/
├── make.py                  the only entry point
├── shorts/                  one module per Short (SPEC/SCRIPT, scenes, LEGO, UPLOAD, thumbnail)
├── core/                    the engine, shared by every Short
├── data/
│   └── policy_history.json  render order + shipped titles the YPP gate compares against (committed)
└── output/                  renders and work files (git-ignored)
    ├── shorts/  work/<short>/{edge,files}/
```

| Path | What it is |
|---|---|
| `core/engine.py` | TTS, music beds (tension, pulse, ambient, march), SFX, captions, mixing and encoding |
| `core/lego.py` | Lego template: interchangeable header / caption / transition / palette / ending pieces |
| `core/delivery.py` | Turns SPEC lines into the performed voice: tones and held pauses |
| `core/voice_kit.py` | KikiVoice: exports one text file per voice, then cuts the downloaded audio into line clips |
| `core/policy.py` | YPP gate: original script, topic, layout, music and ending rotation, sources, upload kit |
| `core/upload_kit.py` | Title scoring, description and tag checks, thumbnail |
| `shorts/reality_shift*.py` | The first Shorts; also shared drawing helpers (`stamp`, `flag`, ...) other Shorts import |
| `shorts/chabahar.py`, `rupee.py`, `maldives.py`, `brahmos_lego.py` | Older Shorts whose helpers (`Cued`, `tag`, `VOICE_TONES`, ...) newer Shorts reuse |

## Making a new Short

1. Copy the latest Lego Short (e.g. `shorts/nyoma.py`) to `shorts/<name>.py`.
2. Change the script, the scenes, and pick a new `LEGO` combination, music style and tempo.
3. Run `python make.py <name> --check` until the YPP gate passes.
4. Voice: `--kiki-export`, make the files in KikiVoice, put them in the printed folder, `--kiki-split`.
5. Run `python make.py <name>` and watch the result.
