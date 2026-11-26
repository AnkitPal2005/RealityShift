"""Shared result type + channel knowledge (pillars, mega names) used by several validators."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Optional

# Severity ladder -> decision: block = REJECTED, fix = NEEDS REVISION, warn = APPROVED WITH IMPROVEMENTS.
LEVELS = ("info", "ok", "warn", "fix", "block")


@dataclass
class Result:
    validator: str
    score: Optional[int] = None          # 0-100, None = could not be evaluated (missing data)
    findings: list = field(default_factory=list)
    suggestions: list = field(default_factory=list)
    data: dict = field(default_factory=dict)

    def add(self, level: str, msg: str) -> None:
        assert level in LEVELS, level
        self.findings.append({"level": level, "msg": msg})

    def suggest(self, msg: str) -> None:
        if msg not in self.suggestions:
            self.suggestions.append(msg)

    @property
    def worst(self) -> str:
        ranks = [LEVELS.index(f["level"]) for f in self.findings] or [0]
        return LEVELS[max(ranks)]

    @property
    def status(self) -> str:
        if self.score is None and not self.findings:
            return "N/A"
        return {"info": "PASS", "ok": "PASS", "warn": "WARN", "fix": "FAIL", "block": "BLOCK"}[self.worst]

    def finalize(self, base: int = 100) -> "Result":
        """Score = base minus a fixed cost per finding (only if the validator did not set its own score)."""
        if self.score is None:
            cost = {"info": 0, "ok": 0, "warn": 6, "fix": 18, "block": 45}
            self.score = max(0, base - sum(cost[f["level"]] for f in self.findings))
        return self

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status
        return d


# Mega names (AGENTS.md #8): every Divya Rahasya topic should tie to one of these.
DEITIES = {
    "Krishna": ["krishna", "kanha", "kanhaiya", "shyam", "murlidhar", "gopal", "govind", "keshav", "madhav",
                "कृष्ण", "कान्हा", "श्याम", "गोपाल"],
    "Ram": ["shri ram", "ram ji", "raam", "raghav", "raghunandan", "ramayan", " ram ", "राम"],
    "Hanuman": ["hanuman", "bajrangbali", "bajrang", "maruti", "pawanputra", "हनुमान", "बजरंगबली"],
    "Shiv": ["shiv", "shiva", "mahadev", "bholenath", "shankar", "neelkanth", "kailash", "शिव", "महादेव", "भोले"],
    "Devi": ["durga", "kali", "maa sherawali", "lakshmi", "parvati", "sita", "tulsi", "दुर्गा", "काली", "सीता"],
    "Ganesh": ["ganesh", "ganpati", "vinayak", "गणेश", "गणपति"],
    "Vishnu": ["vishnu", "narayan", "jagannath", "vamana", "विष्णु", "नारायण"],
}

PILLARS = {
    "dr": {
        "Karm Aur Kripa (modern faith)": ["karm aur kripa", "kalpanik", "interview", "exam", "reject", "papa",
                                          "mummy", "phone", "icu", "cycle", "chai", "stage", "kangan", "karz",
                                          "missed call", "daadi"],
        "Scripture secret": ["mahabharat", "ramayan", "karna", "arjun", "bhishma", "abhimanyu", "ghatotkach",
                             "barbarik", "eklavya", "ashwatthama", "ravan", "sudama", "yuyutsu", "rath",
                             "shraap", "vardaan", "rahasya", "katha"],
        "Temple / festival": ["mandir", "temple", "chhath", "tulsi vivah", "jagannath", "lepakshi", "kailash",
                              "puja", "vrat", "parv"],
    },
    "rs": {
        "Defence tech": ["missile", "rocket", "jet", "fighter", "tank", "submarine", "radar", "brahmos", "pinaka",
                         "agni", "akash", "tejas", "amca", "marut", "kaveri", "prachand", "insas", "drdo", "engine",
                         "kusha", "arihant", "nag", "rifle", "drone", "k9"],
        "Military history": ["1947", "1962", "1965", "1967", "1971", "1999", "kargil", "longewala", "nathu la",
                             "haji pir", "trident", "cactus", "operation", "batra", "war", "yudh", "jung"],
        "Geopolitics": ["china", "pakistan", "chabahar", "malacca", "imec", "maldives", "nicobar", "corridor",
                        "chicken", "border", "lithium", "rupee", "trade"],
    },
    "bb": {"Math puzzle": ["bodmas", "pemdas", "lanes", "race", "math", "puzzle", "riddle", "quiz"],
           "Visual puzzle": ["spot", "diff", "difference", "find"]},
}


def haystack(*parts: str) -> str:
    return " " + " ".join(p for p in parts if p).lower() + " "


def deities_in(text: str) -> list[str]:
    t = haystack(text)
    return [d for d, keys in DEITIES.items() if any(k in t for k in keys)]


def pillar_of(ch: str, text: str) -> str:
    t = haystack(text)
    best, hits = "Other", 0
    for name, keys in PILLARS.get(ch, {}).items():
        n = sum(1 for k in keys if re.search(r"(?<![a-z])" + re.escape(k) + r"(?![a-z])", t))
        if n > hits:
            best, hits = name, n
    return best


def short_text(s) -> str:
    """Everything that describes a Short, for keyword classification."""
    up = s.upload or {}
    return " ".join([s.topic, s.title, s.roman_text, up.get("description", ""), " ".join(up.get("tags", []))])
