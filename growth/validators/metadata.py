"""4. TITLE & METADATA VALIDATOR.

Title curiosity + relevance, misleading-claim detection (title promises the video does not deliver), description
quality, hashtag relevance and channel language rules. Complements core/upload_kit.py (which scores title wording);
this one checks that the metadata is TRUE to the video.
"""

from __future__ import annotations

import re

from ..text import ascii_ratio, content_words, is_devanagari, words
from .base import Result

CURIOSITY = re.compile(r"(\?|\.\.\.|…|\bphir\b|\blekin\b|\bpar\b|\bjab\b|\bkyun\b|\bkaun\b|\bkaise\b|\bvs\b|"
                       r"\bbut\b|\bwhy\b|\bwho\b|\bhow\b|\bwhat\b|\d)", re.IGNORECASE)
HINGLISH_MARK = {"ka", "ki", "ke", "hai", "mein", "kya", "kyun", "karo", "kaun", "jeetega", "likho", "batao", "nahi"}
FEED_TITLE = 70        # beyond this the Shorts feed truncates heavily
MIN_DESC = 150


NUM_WORDS = {
    1: ("ek", "एक"), 2: ("do", "दो"), 3: ("teen", "तीन"), 4: ("char", "chaar", "चार"), 5: ("paanch", "panch", "पांच",
    "पाँच"), 6: ("chhe", "chhah", "छह", "छः"), 7: ("saat", "सात"), 8: ("aath", "आठ"), 9: ("nau", "नौ"),
    10: ("das", "दस"), 11: ("gyarah", "ग्यारह"), 12: ("barah", "baarah", "बारह"), 13: ("terah", "तेरह"),
    14: ("chaudah", "चौदह"), 15: ("pandrah", "पंद्रह"), 16: ("solah", "सोलह"), 17: ("satrah", "सत्रह"),
    18: ("atharah", "अठारह"), 19: ("unnis", "उन्नीस"), 20: ("bees", "बीस"), 25: ("pachees", "पच्चीस"),
    30: ("tees", "तीस"), 40: ("chalis", "chaalis", "चालीस"), 50: ("pachaas", "pachas", "पचास"),
    60: ("saath", "साठ"), 70: ("sattar", "सत्तर"), 80: ("assi", "अस्सी"), 90: ("nabbe", "नब्बे"),
    100: ("sau", "सौ"), 1000: ("hazaar", "hazar", "हज़ार", "हजार"),
}


def _video_words(s) -> set[str]:
    up = s.upload or {}
    return content_words(" ".join([s.roman_text, s.spoken_text, s.topic, " ".join(s.scene_keys),
                                   up.get("thumb_text", "")]))


def _number_stated(n: str, body: str, body_words: set[str]) -> bool | None:
    """True if the number is in the video (as digits or Hindi/Roman words); None if we cannot tell."""
    if n in re.findall(r"\d+", body):
        return True
    names = NUM_WORDS.get(int(n))
    if names is None:
        return None
    return any(w in body_words for w in names)


def validate(me) -> Result:
    r = Result("title_metadata")
    up = me.upload or {}
    title = me.title
    if not up and not title:
        r.add("fix", "no UPLOAD kit (title/description/tags/pinned comment) in the module")
        return r.finalize()
    vw = _video_words(me)
    desc = (up.get("description") or "").strip()
    lang = {"dr": "hinglish", "rs": "hinglish", "bb": "english"}.get(me.channel, "hinglish")

    # --- title ------------------------------------------------------------------------------------
    plain = re.sub(r"#\w+", "", title).strip()
    r.data["title"] = title
    if len(title) > 100:
        r.add("fix", f"title is {len(title)} chars - YouTube cuts at 100")
    elif len(plain) > FEED_TITLE:
        r.add("warn", f"title is {len(plain)} chars without hashtags - the feed shows ~40-70, put the hook first")
    if not CURIOSITY.search(plain):
        r.add("warn", "title has no curiosity device (question, contrast, number, open loop)")
    tw = content_words(plain)
    if me.narration_hi or me.roman_text:
        missing = sorted(w for w in tw if w not in vw and not any(w in v or v in w for v in vw if len(v) > 3))
        rel = 1 - len(missing) / max(len(tw), 1)
        r.data["title_relevance"] = round(rel, 2)
        if rel < 0.4:
            r.add("fix", f"most title words never appear in the video: {', '.join(missing[:6])}")
        elif rel < 0.65:
            r.add("warn", f"title words not in the video's subtitles/scenes: {', '.join(missing[:6])}")
    nums = set(re.findall(r"\d+", plain))
    body = " ".join([me.roman_text, me.spoken_text, me.topic, desc])
    bw = set(words(body))
    stated = {n: _number_stated(n, body, bw) for n in nums}
    missing_n = [n for n, ok in stated.items() if ok is False]
    unsure = [n for n, ok in stated.items() if ok is None]
    if missing_n and me.roman_text:
        r.add("fix", f"number(s) in the title not stated in the video or description: {', '.join(missing_n)} "
                     f"(misleading metadata)")
    if unsure and me.roman_text:
        r.add("warn", f"check by ear that the video states {', '.join(unsure)} (spoken as words, not matched)")
    letters = [c for c in plain if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.6:
        r.add("warn", "title is mostly CAPS - reads as clickbait")
    if len(re.findall(r"[!]{2,}|[\U0001F300-\U0001FAFF]", title)) > 2:
        r.add("warn", "too many emojis / '!!' in the title")

    # --- language rules (AGENTS.md 10b / 16) ----------------------------------------------------
    if lang == "english":
        hing = sorted(set(words(title + " " + desc + " " + up.get("pinned_comment", ""))) & HINGLISH_MARK)
        if hing:
            r.add("fix", f"Brain Blitz is English-only (global) - Hinglish words found: {', '.join(hing)}")
    elif is_devanagari(title):
        r.add("warn", "Devanagari title on a Short - DR/RS Shorts titles stay Roman/Hinglish (Hindi script is "
                      "for DR long videos only)")

    # --- description --------------------------------------------------------------------------------
    if not desc:
        r.add("fix", "no description")
    else:
        if len(desc) < MIN_DESC:
            r.add("warn", f"description is {len(desc)} chars - write 2-3 lines that say what happens")
        if len(desc) > 5000:
            r.add("fix", "description over 5,000 chars")
        first2 = " ".join(desc.splitlines()[:2]).lower()
        qs = up.get("queries") or []
        if qs and not any(set(words(q)) <= set(words(first2)) for q in qs):
            r.add("warn", "none of the search queries appear in the first two description lines")
        drift = content_words(desc) - vw - tw
        r.data["description_relevance"] = round(1 - len(drift) / max(len(content_words(desc)), 1), 2)

    # --- hashtags + tags --------------------------------------------------------------------------
    tags = up.get("tags") or []
    hashtags = up.get("hashtags") or re.findall(r"#\w+", desc)
    if hashtags and not any(h.lower() == "#shorts" for h in hashtags) and "#shorts" not in title.lower():
        r.add("warn", "no #Shorts hashtag in title or description")
    if len(hashtags) > 15:
        r.add("fix", f"{len(hashtags)} hashtags - over 15 makes YouTube ignore all of them")
    ref = vw | tw | content_words(" ".join(tags)) | content_words(desc)
    for h in hashtags:
        hw = h.lstrip("#").lower()
        if hw in ("shorts", "short"):
            continue
        if not any(len(v) > 3 and (v in hw or hw in v) for v in ref):
            r.add("warn", f"hashtag {h} is not related to anything in the video or metadata")
    if sum(len(t) for t in tags) + 2 * len(tags) > 500:
        r.add("fix", "tags exceed YouTube's 500-character limit")

    # --- pinned comment ---------------------------------------------------------------------------
    pinned = up.get("pinned_comment") or up.get("pinned") or ""
    if not pinned:
        r.add("warn", "no pinned comment prepared (post + pin within 30 min of upload)")
    elif "?" not in pinned:
        r.add("warn", "pinned comment asks no question - viewers need something to answer")
    if lang == "english" and pinned and ascii_ratio(pinned) < 0.9:
        r.add("fix", "pinned comment is not English")
    return r.finalize()
