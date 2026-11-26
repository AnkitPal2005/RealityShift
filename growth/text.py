"""Small text helpers shared by the validators (no external dependencies)."""

from __future__ import annotations

import re
import unicodedata

DEVANAGARI = re.compile(r"[ऀ-ॿ]")
PUNCT = ".,!?।…'\"—–-:;()[]{}#*“”‘’|/"

STOP = {
    # Roman Hindi
    "ka", "ki", "ke", "hai", "hain", "me", "mein", "se", "ko", "kya", "kyun", "kyon", "aur", "ne", "par", "to",
    "toh", "ye", "yeh", "wo", "woh", "vo", "ek", "jab", "tab", "bhi", "hi", "na", "nahi", "tha", "thi", "the",
    "kar", "diya", "liya", "raha", "rahi", "gaya", "gayi", "apne", "apni", "uska", "uski", "unke", "khud", "sab",
    # English
    "a", "an", "the", "of", "in", "on", "and", "or", "is", "are", "was", "to", "for", "with", "vs", "why", "how",
    "what", "who", "this", "that", "it", "its", "by", "at", "be", "your", "you", "can", "shorts", "short",
    # Hindi (Devanagari)
    "का", "की", "के", "है", "हैं", "में", "से", "को", "क्या", "और", "ने", "पर", "तो", "ये", "वो", "एक", "जब",
    "तब", "भी", "ही", "ना", "नहीं", "था", "थी", "थे", "कर", "दिया", "लिया", "रहा", "रही", "गया", "गई", "अपने",
    "अपनी", "उसकी", "उसका", "उनके", "खुद", "सब",
}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s or "")
    s = re.sub(r"#\w+", " ", s)                       # hashtags
    s = "".join(ch for ch in s if ch.isalnum() or ch.isspace() or DEVANAGARI.match(ch))
    return re.sub(r"\s+", " ", s).strip().lower()


def words(s: str) -> list[str]:
    return [w.strip(PUNCT) for w in norm(s).split() if w.strip(PUNCT)]


def content_words(s: str) -> set[str]:
    return {w for w in words(s) if w not in STOP and len(w) > 1}


def shingles(ws: list[str], n: int = 4) -> set[tuple]:
    return {tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def containment(a: set, b: set) -> float:
    """Share of a that also appears in b."""
    return len(a & b) / len(a) if a else 0.0


def is_devanagari(s: str) -> bool:
    return bool(DEVANAGARI.search(s or ""))


def ascii_ratio(s: str) -> float:
    letters = [c for c in s if c.isalpha()]
    return sum(c.isascii() for c in letters) / len(letters) if letters else 1.0
