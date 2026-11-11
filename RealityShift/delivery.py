"""Catchy voice delivery for Reality Shift (edge-tts hi-IN-MadhurNeural), shared by every new Short.

A story writes SPEC lines as (tone, [(spoken Hindi, caption), ...][, pause]) and sets
    DELIVERY = delivery.build(SPEC)
Rhythm rules (user, 11 Nov 2026: "pace thik kar, bolne ka tarika catchy bana jisse audience ruke"):
  - build/tell lines run quick, so the story keeps moving,
  - a short held beat (TEASE_PAUSE) right before every punch line, so the payoff lands,
  - punch lines a touch slower and louder, with a slightly lower pitch: the number/reveal sounds heavy,
  - low lines drop pace and volume for contrast; questions lift the pitch,
  - small gaps after commas, medium after sentences. The old per-line 3rd element is ignored: the rules decide.
"""

TONES = {               # (rate, pitch, volume) per line; replaces the story's EDGE_RATE
    "hook":  ("+18%", "+2Hz", "+20%"),
    "build": ("+20%", "+1Hz", "+14%"),
    "tell":  ("+15%", "+0Hz", "+10%"),
    "sly":   ("+10%", "+2Hz", "+10%"),
    "low":   ("+6%", "-2Hz", "+4%"),
    "punch": ("+4%", "-1Hz", "+25%"),
    "ask":   ("+10%", "+3Hz", "+14%"),
    "cta":   ("+16%", "+1Hz", "+16%"),
}
TEASE_PAUSE = 0.38      # held beat before a punch line
COMMA_PAUSE = 0.12      # after a line ending in , or —
STOP_PAUSE = 0.24       # after a sentence (। ! ? .)
SUSPENSE_PAUSE = 0.32   # after a line ending in ...


def _pause(line: str, nxt) -> float:
    if nxt is not None and nxt[0] == "punch":
        return TEASE_PAUSE
    end = line.rstrip("'\" ")
    if end.endswith(("...", "…")):
        return SUSPENSE_PAUSE
    if end.endswith((",", "—", "-")):
        return COMMA_PAUSE
    return STOP_PAUSE


def build(spec) -> dict:
    """SPEC -> engine DELIVERY {scene: [((rate, pitch, volume), line, pause_after), ...]}."""
    out = {}
    for s in spec:
        lines = s["vo"]
        rows = []
        for i, (tone, chunks, *pause) in enumerate(lines):
            text = " ".join(hi for hi, _ in chunks)
            nxt = lines[i + 1] if i + 1 < len(lines) else None
            p = _pause(text, nxt)
            rows.append((TONES[tone], text, 0 if nxt is None else p))
        out[s["key"]] = rows
    return out
