"""Central settings for Divine Stories. Every path resolves inside this project folder.

Nothing here reads or writes outside Divine-Stories/, and nothing imports Reality Shift.
Optional overrides come from a local .env (see .env.example); no API keys are needed.
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load_env(path: Path) -> None:
    """Tiny .env reader (KEY=VALUE lines) so we need no extra dependency."""
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_env(ROOT / ".env")

# ---------------------------------------------------------------- paths
ASSETS = ROOT / "assets"
ASSET_CACHE = ASSETS / "backgrounds" / "commons"     # downloaded public-domain / CC-BY images
ASSET_MANIFEST = ASSETS / "manifest.json"            # attribution + licence for every downloaded file
MUSIC_DIR = ASSETS / "music"
SFX_DIR = ASSETS / "sound_effects"
CHAR_PROFILES = ROOT / "characters" / "profiles"
STORY_LIBRARY = ROOT / "story" / "library"
OUTPUT = ROOT / "output"
TEMP = ROOT / "temp"
LOGS = ROOT / "logs"

# ---------------------------------------------------------------- video
W, H = 1080, 1920
FPS = 30
MIN_DURATION, MAX_DURATION = 40.0, 60.0
SAFE_BOTTOM = 420          # bottom px kept clear of captions/branding (Shorts title, buttons)
SAFE_RIGHT = 140           # right rail (like/comment/share)
SAFE_TOP = 150             # top bar (search / menu)
CRF = int(os.environ.get("DS_CRF", "18"))
X264_PRESET = os.environ.get("DS_PRESET", "medium")

# ---------------------------------------------------------------- voice (edge-tts, free)
VOICE = os.environ.get("DS_VOICE", "hi-IN-MadhurNeural")
VOICE_RATE = os.environ.get("DS_VOICE_RATE", "-4%")     # slower than default: calm, cinematic
VOICE_PITCH = os.environ.get("DS_VOICE_PITCH", "-6Hz")  # a little deeper
SAMPLE_RATE = 48000

# ---------------------------------------------------------------- audio mix
TARGET_LUFS = -14.0
MUSIC_GAIN_DB = -20.0      # music bed under the voice (before ducking)
DUCK_DB = -8.0             # extra music reduction while the narrator speaks
SFX_GAIN_DB = -9.0

# ---------------------------------------------------------------- assets / licensing
# Only licences that allow commercial reuse in a video WITHOUT share-alike/no-derivatives obligations.
ALLOWED_LICENSES = ("pd", "cc0", "cc-by")          # matched against Commons' machine "License" field
BLOCKED_LICENSE_MARKERS = ("-sa", "-nc", "-nd", "gfdl", "fair use", "non-free")
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
COMMONS_THUMB_WIDTH = 1920  # a standard Wikimedia thumbnail step
HTTP_USER_AGENT = os.environ.get(
    "DS_USER_AGENT", "DivineStoriesAssetFetcher/0.1 (local, non-commercial-tooling; python-requests)")

# ---------------------------------------------------------------- branding
CHANNEL_NAME = os.environ.get("DS_CHANNEL_NAME", "Divya Rahasya")
CHANNEL_NAME_HI = os.environ.get("DS_CHANNEL_NAME_HI", "दिव्य रहस्य")

# ---------------------------------------------------------------- fonts (system Nirmala UI, shaped by HarfBuzz)
DEVANAGARI_FONT = Path(os.environ.get("DS_FONT", r"C:\Windows\Fonts\Nirmala.ttc"))
FONT_FACE_REGULAR, FONT_FACE_BOLD, FONT_FACE_LIGHT = 0, 1, 2   # indices inside Nirmala.ttc

# ---------------------------------------------------------------- upload safety (manual upload only)
DEFAULT_VISIBILITY = "private"   # what the upload package recommends while testing


def story_out(slug: str) -> Path:
    p = OUTPUT / slug
    p.mkdir(parents=True, exist_ok=True)
    return p


def story_temp(slug: str) -> Path:
    p = TEMP / slug
    p.mkdir(parents=True, exist_ok=True)
    return p
