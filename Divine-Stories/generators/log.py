"""Project-local logging: prints and appends to logs/divine_stories.log (never outside the project)."""

from __future__ import annotations

import datetime as _dt

from config import settings as S


def log(stage: str, msg: str) -> None:
    line = f"{_dt.datetime.now():%Y-%m-%d %H:%M:%S} [{stage}] {msg}"
    print(line, flush=True)
    S.LOGS.mkdir(parents=True, exist_ok=True)
    with (S.LOGS / "divine_stories.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")
