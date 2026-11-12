# Youtube-Generator

YouTube Shorts pipelines, one folder per channel. Every frame is drawn in code and every sound is synthesized
or voiced in KikiVoice, so nothing is reused content. Each pipeline has its own engine, YPP policy gate and
outputs, so changing one can never break the other.

| Folder | Channel | What it makes |
|---|---|---|
| [`RealityShift/`](RealityShift/) | Reality Shift | Hindi defence and geopolitics Shorts with Cairo-drawn visuals |
| [`SanatanKatha/`](SanatanKatha/) | Divya Rahasya | Animated mythology kathas: code-drawn devta cartoons, kathavachak voice, devotional music |

## Layout

```
story-pipeline/
├── README.md
├── requirements.txt         shared Python dependencies
├── .editorconfig  .gitignore
├── RealityShift/
│   ├── make.py              entry point: python make.py <short> [--check|--kit|--kiki-export|--kiki-split]
│   ├── core/                engine, lego template, voice kit, YPP gate, upload kit
│   ├── shorts/              one module per Short
│   ├── data/                policy_history.json
│   └── output/              renders (git-ignored)
└── SanatanKatha/
    ├── make.py              entry point: python make.py <katha> [--check|--preview|--kiki-export|--kiki-split]
    ├── core/                engine, katha scenes, devta rig, voice kit, YPP gate, upload kit
    ├── kathas/              one module per katha (+ _template.py)
    ├── data/                policy_history.json
    └── output/              renders and previews (git-ignored)
```

## Setup

```
pip install -r requirements.txt      # Python 3.14, ffmpeg on PATH
cd RealityShift && python make.py --list
```

Always run `make.py` from inside its channel folder. See each folder's README for the full workflow.
