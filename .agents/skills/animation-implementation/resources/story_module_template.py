"""Template Katha Story Module for Sanatan Katha YouTube Shorts.

Validation Levels (Must complete all 5 before production sign-off):
  Level 1: python -m py_compile kathas/<story_name>.py    # AST syntax check ONLY
  Level 2: python -c "import kathas.<story_name>"          # Module import & constants check
  Level 3: python make.py <story_name> --check             # YPP policy & metadata verification
  Level 4: Scene draw() programmatic dry-run               # Headless Cairo execution test
  Level 5: python make.py <story_name> --preview           # Visual contact sheet & thumbnail inspection

Note: Passing Level 1 (py_compile) does NOT mean the module is production-ready.
All 5 levels must pass, culminating in human inspection of output/preview/<story_name>_sheet.png.
"""

import math
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cairo

from core import engine, katha, upload_kit
from core.katha import *  # noqa: F401,F403
import core.devta as dv
from core.devta import group, place, halo, smooth, ink, ell, gem, limb, hand, sheen, eye, shade

# ==============================================================================
# 1. STORY METADATA & AUDIO CONFIGURATION
# ==============================================================================
TOPIC = "STORY TOPIC IN UPPERCASE"
OUTPUTS = {"edge": "story_name_short.mp4"}

MUSIC_STYLE = "ambient"      # Devotional ambient pads (avoids repetitive flute/drone)
MUSIC_BPM = 88               # Balanced devotional tempo (80 - 92 BPM)
MUSIC_VOLUME = 0.12          # 0.10 - 0.12 allows spoken voiceover to remain clear
TAIL_PAD = 0.04              # Eliminates awkward pauses between scenes
MAX_GAP = 0.04               # Continuous spoken flow

# Project Theme Colors
WHITE = (1.0, 1.0, 1.0)
MYSTIC_PURPLE = hexc("#2B1238")
DIVINE_AMBER = hexc("#FFB347")

# ==============================================================================
# 2. SCRIPTURAL SOURCES & EVIDENCE BASE
# ==============================================================================
SOURCES = [
    "Primary Scriptural Source: Name of Purana/Itihasa, Khanda, Chapter, Verses.",
    "Secondary Source / Living Tradition: Recension details or audited folklore.",
]

# ==============================================================================
# 3. SCRIPT & SCENE SPECIFICATION (SPEC)
# ==============================================================================
# vo format: [(tone, [(spoken_hindi, CAPTION_ROMAN), ...], pause_duration), ...]
# Tone options from core/katha.py: "tell", "open", "build", "fast", "low", "whisper", "punch", "awe", "warm"
SPEC = [
    {
        "key": "hook",
        "text": "ON SCREEN TITLE 1",
        "visual": "Cinematic visual description from director's blueprint",
        "vo": [
            ("tell", [
                ("पहला हिंदी वाक्य,", "PEHLA HINDI VAKYA,"),
                ("जो दर्शकों को आकर्षित करे।", "JO DARSHAKON KO AAKARSHIT KARE."),
            ], 0.5)
        ]
    },
    {
        "key": "climax",
        "text": "ON SCREEN TITLE 2",
        "visual": "Divine reveal or dramatic turning point",
        "vo": [
            ("build", [
                ("कथा का मुख्य मोड़,", "KATHA KA MUKHYA MOD,"),
                ("जहाँ सत्य प्रकट होता है।", "JAHAN SATYA PRAKAT HOTA HAI."),
            ], 0.5)
        ]
    },
    {
        "key": "cta",
        "text": "JAI SHRI KRISHNA",
        "visual": "Blessing posture with unobscured deity and sleek prompt ribbon",
        "vo": [
            ("warm", [
                ("कमेंट में लिखिए,", "COMMENT MEIN LIKHIYE,"),
                ("जय श्री कृष्ण!", "JAI SHRI KRISHNA!"),
            ])
        ]
    },
]

# Process script into engine structures
DELIVERY, SCRIPT, NARRATION = script_of(SPEC)

# Caption highlight colors
HOT = hot_words({
    "HINDI": GOLD_HI,
    "SATYA": DIVINE,
    "KRISHNA!": BLUE,
    "COMMENT": GOLD_HI,
})


# ==============================================================================
# 4. CUSTOM PROCEDURAL CHARACTERS (IF NOT IN devta.py)
# ==============================================================================
def custom_divine_figure(ctx, x, y, s, t, pose="stand", flip=False, a=1.0):
    """Custom procedural deity adhering to context state isolation rules."""
    def draw():
        # MANDATORY: place() executes ctx.save() internally
        place(ctx, x, y, s, t, flip)
        
        # 1. Celestial aura
        halo(ctx, 0, -620, 180, t, c=GOLD_HI)
        
        # 2. Body anatomy (feet at local 0, head at negative y)
        skin = dv.KRISHNA_SKIN
        ell(ctx, 0, -640, 110, 120)
        ink(ctx, skin)
        
        # 3. Mukut & Robes
        smooth(ctx, [(-70, -740), (0, -880), (70, -740)])
        ink(ctx, GOLD_HI)
        
        # MANDATORY: Must restore context before exiting draw closure!
        ctx.restore()
        
    group(ctx, a, draw)


# ==============================================================================
# 5. SCENE CLASSES (Cued IMPLEMENTATION)
# ==============================================================================
class HookScene(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "reveal": c("PEHLA", d * 0.35),
            "accent": c("DARSHAKON", d * 0.70),
        }

    def events(self, d):
        b = self.beats(d)
        return [
            (0.02, "soft_thud"),
            (b["reveal"], "shimmer"),
        ]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        # Layer 1-4: Background & Terrain
        battlefield(ctx, t)
        
        # Layer 5-7: Central Deity / Character
        dv.krishna(ctx, 540, GROUND - 10, 0.74, t, pose="flute")
        
        # Layer 8-9: UI & Energy
        dv.ribbon(ctx, "ON SCREEN TITLE 1", 540, 280, t - b["reveal"], size=80)


class ClimaxScene(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "mod": c("KATHA", d * 0.40),
            "satya": c("SATYA", d * 0.75),
        }

    def events(self, d):
        b = self.beats(d)
        return [
            (0.02, "thud"),
            (b["satya"], "boom"),
        ]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        meadow(ctx, t)
        custom_divine_figure(ctx, 540, GROUND - 10, 0.72, t, pose="stand")
        dv.ribbon(ctx, "ON SCREEN TITLE 2", 540, 280, t - b["satya"], size=80)


class CtaScene(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "comment": c("COMMENT", d * 0.35),
            "krishna": c("KRISHNA", d * 0.65),
        }

    def events(self, d):
        b = self.beats(d)
        return [
            (0.02, "soft_thud"),
            (b["krishna"], "ghanti"),
        ]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        temple_bg(ctx, t)
        # Keep deity visible and unobstructed
        dv.krishna(ctx, 540, GROUND - 10, 0.74, t, pose="bless")
        dv.petals(ctx, t, count=30)
        
        # Single sleek ribbon at the top safe zone
        dv.ribbon(ctx, "JAI SHRI KRISHNA", 540, 280, t - b["krishna"], size=82)


# ==============================================================================
# 6. SCENE REGISTRY
# ==============================================================================
SCENE_CLASSES = {
    "hook": HookScene,
    "climax": ClimaxScene,
    "cta": CtaScene,
}


# ==============================================================================
# 7. YOUTUBE UPLOAD METADATA KIT
# ==============================================================================
UPLOAD = {
    "titles": [
        "Primary Catchy Title: Sanatan Mystery Explained",
        "Alternative Title 2",
        "Alternative Title 3",
        "Alternative Title 4",
        "Alternative Title 5",
        "Alternative Title 6",
        "Alternative Title 7",
        "Alternative Title 8",
        "Alternative Title 9",
        "Alternative Title 10",
    ],
    "title": "Primary Catchy Title: Sanatan Mystery Explained",
    "thumb_text": "HOOK PHRASE?",
    "queries": ["mythology search term 1", "mythology search term 2"],
    "description": """
Brief synopsis of the sacred story without spoilers.

Key spiritual moments:
• Point 1
• Point 2
• Point 3

Comment below: Jai Shri Krishna.

Note: Explanatory note on scriptural source tradition.
""",
    "tags": ["sanatan dharma", "hindu mythology shorts", "pauranik katha", "divya rahasya"],
    "hashtags": ["#Shorts", "#SanatanKatha", "#HinduMythology"],
}


# ==============================================================================
# 8. THUMBNAIL COVER ROUTINE
# ==============================================================================
def thumbnail(ctx):
    """1080x1920 high-contrast thumbnail cover."""
    temple_bg(ctx, 0.0)
    dv.krishna(ctx, 540, GROUND - 30, 0.85, 0.3, pose="flute")
    
    # Top gradient darkening for text legibility
    g = cairo.LinearGradient(0, 0, 0, 650)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.92)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    ctx.rectangle(0, 0, W, 650)
    ctx.set_source(g)
    ctx.fill()
    
    # Bold two-tone title
    text(ctx, "SANATAN", 540, 240, 190, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "RAHASYA?", 540, 440, 200, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)

