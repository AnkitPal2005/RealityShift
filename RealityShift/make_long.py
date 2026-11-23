"""Long-form (16:9) entry point for Reality Shift. Run from this folder.

    python make_long.py chickens_neck --kiki-export   # 1. one KikiVoice text file per chapter
    python make_long.py chickens_neck --preview       # 2. contact sheets + thumbnail + upload kit (no voice)
    (user makes ch01.mp3 ... chNN.mp3 in KikiVoice, saves them in output/work/<name>/files/)
    python make_long.py chickens_neck                 # 3. Whisper-aligned full render -> output/longform/
"""

import importlib
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)

from core import longform  # noqa: E402


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    name = sys.argv[1]
    mod = importlib.import_module(f"longform.{name}")
    work = f"{name}_long"
    if "--kiki-export" in sys.argv:
        longform.export(mod, work)
    elif "--preview" in sys.argv:
        longform.preview(mod, work)
    elif "--thumb" in sys.argv:
        longform.thumbnail(mod, work)
    else:
        longform.render(mod, work)


if __name__ == "__main__":
    main()
