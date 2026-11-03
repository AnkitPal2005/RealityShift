"""Animated 9:16 YouTube Shorts generator.

Usage:
  python generate_video.py [--story dark_store|popcorn|reality_shift|reality_shift_defense] [--engine edge|elevenlabs]

Each story in stories/ defines its narration (Hindi for TTS + Hinglish captions),
animated scene classes and output file names; engine.py does the rest:
  1. TTS (edge-tts or ElevenLabs) -> narration + per-word timestamps
  2. numpy -> synthesised SFX + tension music, ffmpeg -> compression + loudnorm
  3. pycairo -> every frame drawn as vector motion graphics + kinetic captions
  4. MoviePy -> 1080x1920, 30fps, libx264/aac MP4 in output/shorts/ (all stories share it)
     (intermediate audio in output/work/<story>/<engine>/)

ElevenLabs needs the ELEVENLABS_API_KEY environment variable.
"""

import argparse
import importlib
from pathlib import Path

import engine

STORIES = sorted(p.stem for p in (Path(__file__).parent / "stories").glob("*.py") if p.stem != "__init__")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--story", choices=STORIES, default="dark_store")
    ap.add_argument("--engine", choices=("edge", "elevenlabs"), default="edge", help="narration TTS engine")
    args = ap.parse_args()
    engine.render(importlib.import_module(f"stories.{args.story}"), args.engine)


if __name__ == "__main__":
    main()
