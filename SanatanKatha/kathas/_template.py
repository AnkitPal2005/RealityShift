"""<Katha ka naam>: <hook sawal> (~75-90s katha).   <- copy this file to kathas/<name>.py and fill it in

Usage (from SanatanKatha/):
  python make.py <name> --preview   # check the visuals first (no voice spent)
  python make.py <name> --check     # YPP gate only
  python make.py <name>             # full render + upload kit
Output: output/shorts/<name>_short.mp4
"""

from core.katha import *  # noqa: F401,F403  (engine helpers, devta as dv, scenery, Cued, story defaults)

TOPIC = "NAYI KATHA"                      # unique across every katha (policy checks it)
OUTPUTS = {"edge": "nayi_katha_short.mp4"}
MUSIC_BPM = 80                            # move it >= 6 BPM away from the previous katha (78-92 works)

SOURCES = [                               # >= 2: where each story fact comes from; note the versions that differ
    "Granth / adhyay ... (Wikipedia '...')",
    "Lok parampara / mandir ki katha ... (...)",
]

# Kathavachak rules (README.md): told, not read. Each line = (tone, [(spoken Hindi, CAPTION), ...], pause seconds).
# Tones (katha.TONES): open, tell, build, fast, low, whisper, punch, awe, ask, warm, cta, char, deva, maa.
SPEC = [
    {"key": "hook", "text": "HOOK?",
     "visual": "What the viewer sees in this scene",
     "vo": [("open", [("सोचो...", "SOCHO...")], 0.45),
            ("punch", [("एक ऐसा सवाल,", "EK AISA SAWAL,"), ("जिसका जवाब...", "JISKA JAWAB...")], 0.4),
            ("ask", [("क्या था?", "KYA THA?")])]},
    {"key": "cta", "text": "COMMENT",
     "visual": "Comment card",
     "vo": [("warm", [("कहानी अच्छी लगी हो, भाई,", "KAHANI ACHHI LAGI HO, BHAI,")], 0.3),
            ("cta", [("कमेंट में लिखो—", "COMMENT MEIN LIKHO—")], 0.2),
            ("punch", [("जय श्री कृष्ण!", "JAI SHRI KRISHNA!")])]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({"SOCHO": GOLD_HI, "JAI": GOLD_HI, "KRISHNA": BLUE, "COMMENT": GOLD_HI})


class Hook(Cued):
    """cue("WORD", default) = when the caption containing WORD starts, so visuals land on the spoken word."""

    def beats(self, d):
        return {"q": self.cue("KYA", d * 0.8)}

    def events(self, d):          # SFX: boom thud whoosh pop ghanti shankh arrow shimmer ...
        return [(0.02, "boom"), (self.beats(d)["q"], "shankh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        temple_bg(ctx, t)
        dv.krishna(ctx, 540, GROUND, 0.9, t, pose="flute")
        dv.ribbon(ctx, "HOOK?", 540, 300, t - b["q"], size=84)


class Cta(Cued):
    def events(self, d):
        return [(0.02, "ghanti")]

    def draw(self, ctx, t, d):
        temple_bg(ctx, t)
        dv.krishna(ctx, 540, GROUND, 0.9, t, pose="bless")


SCENE_CLASSES = {"hook": Hook, "cta": Cta}

UPLOAD = {
    "titles": ["Title 1", "Title 2", "Title 3", "Title 4", "Title 5", "Title 6", "Title 7", "Title 8", "Title 9",
               "Title 10"],
    "thumb_text": "MAX 3 WORDS",
    "queries": ["search jo log likhte hain", "dusri search", "teesri search"],
    "description": """
Pehli 2 lines mein queries ke shabd.
""",
    "tags": ["tag1", "tag2"],
    "hashtags": ["#Shorts", "#Krishna", "#Katha"],
}


def thumbnail(ctx):
    temple_bg(ctx, 0.0)
    dv.krishna(ctx, 540, 1700, 1.4, 0.3, pose="bless")
    text(ctx, "MAX 3", 540, 260, 190, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
