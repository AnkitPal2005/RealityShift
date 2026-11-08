"""Character reference library: profiles + approved assets + consistency checks."""

from __future__ import annotations

import json
from functools import lru_cache

from config import settings as S


@lru_cache(maxsize=None)
def profile(char_id: str) -> dict:
    path = S.CHAR_PROFILES / f"{char_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"no character profile {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def approved(char_id: str) -> dict[str, str]:
    return profile(char_id)["approved_assets"]


def check_story(story: dict) -> list[str]:
    """Problems with character usage (empty list = consistent)."""
    problems = []
    for sc in story["scenes"]:
        v = sc["visual"]
        cid = v.get("character")
        if not cid:
            continue
        roles = approved(cid)
        if v["asset"] not in roles.values():
            problems.append(f"{sc['id']}: asset {v['asset']} is not an approved {cid} reference")
            continue
        role = next(r for r, a in roles.items() if a == v["asset"])
        if v.get("shot") == "closeup" and role != "primary_portrait":
            problems.append(f"{sc['id']}: close-up of {cid} must use primary_portrait, not {role}")
    return problems
