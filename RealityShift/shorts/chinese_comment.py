"""Reality Shift Short: Chinese Comment Reality Check - 1971 Surrender & 1967 Nathu La Response.

Topic: Response to a Chinese commenter claiming Indians never fought real wars and lack fighting spirit.
       Counters with factual military history: 1971 war (13 days, 93,000 Pakistani soldiers surrendered, largest
       since WWII) and 1967 Nathu La (300+ Chinese PLA soldiers killed, forced retreat).
Debate: "Kya Bharat ki sena ka shaurya duniya mein sabse mazboot hai?" - Audience mobilization in comments.
Format: Vertical 1080x1920 (9:16), ~35-41 s, payoff in call to action, loop into hook.
"""

import importlib
import json
import math
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cairo

from core import delivery, engine, lego
from core.engine import *  # noqa: F401,F403
from shorts.chabahar import Cued
from shorts.akashteer import ell, poly, seg01, burst, soldier
from shorts.reality_shift import flag

TOPIC = "CHINESE COMMENT RESPONSE - 1971 SURRENDER & 1967 NATHU LA"
OUTPUTS = {"edge": "chinese_comment_short.mp4"}
LEGO = {"header": "intel", "caption": "typewriter", "transition": "shutter", "palette": "intel", "ending": "prompt"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.25
TAIL_PAD = 0.12
TRIM = {"thresh": 0.006, "keep": 0.04, "keep_tail": 0.06}
MUSIC_BPM = 104
MUSIC_STYLE = "pulse"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 0
MAX_SECONDS = 45.0

SOURCES = [
    "Wikipedia - Indo-Pakistani War of 1971 (Instrument of Surrender signed on 16 December 1971 by Lt. Gen. A. A. K. "
    "Niazi; 93,000 Pakistani servicemen surrendered to Indian forces led by Lt. Gen. J. S. Aurora, the largest surrender "
    "in terms of personnel since World War II): https://en.wikipedia.org/wiki/Indo-Pakistani_War_of_1971",
    "Wikipedia - Nathu La and Cho La clashes (Clashes in September-October 1967 between Indian Army and People's "
    "Liberation Army; Indian Army repelled PLA aggression, estimated Chinese casualties over 340 killed and 450 wounded; "
    "decisive Indian tactical victory securing Sikkim border): https://en.wikipedia.org/wiki/Nathu_La_and_Cho_La_clashes",
]

PAL = lego.PALETTES["intel"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
WHITE = (1.0, 1.0, 1.0)
GOLD = hexc("#FFD166")
RED = hexc("#E2483A")
CYAN = hexc("#5FD3FF")
FIRE = hexc("#FF6A1A")
STEEL = hexc("#8C969E")
STEEL_DK = hexc("#4F575E")
MONO = "Consolas"
GROUND = 1120

SPEC = [
    # Scene 1: 00:00 - The Chinese Comment Shock
    {"key": "comment_shock", "accent": RED, "text": "",
     "visual": "Dark red radar room; an on-screen YouTube comment box pops up with Chinese flag badge and hostile text",
     "vo": [("hook", [("एक चीनी यूज़र ने", "EK CHINESE USER NE"),
                      ("हमारे वीडियो पर", "HAMARE VIDEO PAR"),
                      ("कमेंट करके भारतीयों को", "COMMENT KARKE BHARATIYON KO"),
                      ("कायर कह दिया।", "KAYAR KAH DIYA")]),
            ("hook", [("लिखता है कि भारत ने", "LIKHTA HAI KI BHARAT NE"),
                      ("कभी असली जंग", "KABHI ASLI JUNG"),
                      ("देखी ही नहीं", "DEKHI HI NAHI"),
                      ("और हम में लड़ने का", "AUR HUM MEIN LADNE KA"),
                      ("दम नहीं है।", "DAM NAHI HAI")])]},

    # Scene 2: 1971 Surrender
    {"key": "surrender_1971", "accent": FIRE, "text": "",
     "visual": "1971 War map, 13 DAYS counter, 93,000 Surrender ticker, enemy weapons laid on ground",
     "vo": [("punch", [("अरे इनको याद दिलाओ कि", "ARE INKO YAAD DILAO KI"),
                       ("उन्नीस सौ इकहत्तर में", "1971 MEIN"),
                       ("सिर्फ तेरह दिनों में।", "SIRF 13 DINON MEIN")]),
            ("punch", [("हमने इनके यार के", "HUMNE INKE YAAR KE"),
                       ("तिरानवे हज़ार सैनिकों को", "93,000 SAINIKON KO"),
                       ("घुटनों पर बिठा दिया था।", "GHUTNON PAR BITHA DIYA THA")]),
            ("tell", [("विश्व इतिहास में", "VISHWA ITIHAS MEIN"),
                      ("इतना बड़ा सरेंडर", "ITNA BADA SURRENDER"),
                      ("कभी किसी ने देखा है।", "KABHI KISI NE DEKHA HAI")])]},

    # Scene 3: 1967 Nathu La Clash
    {"key": "nathu_la_1967", "accent": CYAN, "text": "",
     "visual": "Snow-covered barbed wire border at Nathu La 1967, Indian jawans hold the line, Chinese soldiers retreat",
     "vo": [("punch", [("और उन्नीस सौ सरसठ में", "AUR 1967 MEIN"),
                       ("नाथू ला पर", "NATHU LA PAR"),
                       ("जब तुम चढ़े थे।", "JAB TUM CHADHE THE")]),
            ("punch", [("तो हमारे जवानों ने", "TO HAMARE JAWANON NE"),
                       ("तीन सौ से ज़्यादा", "300 SE ZYADA"),
                       ("चीनी सैनिकों को", "CHINESE SAINIKON KO"),
                       ("वहीं ढेर कर दिया था।", "WAHIN DHER KAR DIYA THA")])]},

    # Scene 4: Call to Action & Infinite Loop
    {"key": "call_to_action", "accent": GOLD, "text": "",
     "visual": "Tiranga waving, Indian soldier silhouette, pinned comment link card pointing down, loop transition",
     "vo": [("tell", [("मैंने कमेंट में", "MAINE COMMENT MEIN"),
                      ("उस वीडियो का", "US VIDEO KA"),
                      ("लिंक पिन कर दिया है।", "LINK PIN KAR DIYA HAI")]),
            ("ask", [("जाओ और इस चीनी को", "JAO AUR IS CHINESE KO"),
                     ("हमारी ताकत का", "HAMARI TAKAT KA"),
                     ("ऐसा जवाब दो कि", "AISA JAWAB DO KI"),
                     ("इसकी आने वाली पीढ़ियां भी", "ISKI AANE WALI PEEDHIYAN BHI"),
                     ("याद रखें।", "YAAD RAKHEIN")]),
            ("low", [("तभी तो जब", "TABHI TO JAB")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "CHINESE": RED, "USER": WHITE, "VIDEO": CYAN, "BHARATIYON": SAFFRON, "KAYAR": RED,
    "ASLI": FIRE, "JUNG": FIRE, "DAM": FIRE, "1971": GOLD, "13": GOLD, "DINON": GOLD,
    "93,000": FIRE, "SAINIKON": RED, "GHUTNON": RED, "SURRENDER": RED, "1967": GOLD,
    "NATHU": CYAN, "LA": CYAN, "300": FIRE, "DHER": FIRE, "LINK": CYAN, "PIN": GOLD,
    "TAKAT": SAFFRON, "JAWAB": FIRE, "PEEDHIYAN": GOLD, "YAAD": SAFFRON, "TABHI": GOLD,
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".")] = HOT[_k]


def at(scene, key, frac, d):
    return scene.cue(key, frac * d)


# ============================================================ Visual Helpers

# Load actual user comment screenshot directly (user_comment)
_COMMENT_IMG = _ROOT / "output" / "work" / "chinese_comment" / "files" / "comment_card.png"
USER_COMMENT_SURF = getattr(cairo.ImageSurface, "create_from_" + "png")(str(_COMMENT_IMG)) if _COMMENT_IMG.exists() else None


def draw_comment_box(ctx, x, y, w, h, t):
    """Draw actual real YouTube comment screenshot exactly as uploaded by user with hostile red glow."""
    rrect(ctx, x, y, w, h, 16)
    rgba(ctx, (0.05, 0.05, 0.07), 0.98)
    ctx.fill()
    rrect(ctx, x, y, w, h, 16)
    rgba(ctx, RED, 0.85 + 0.15 * math.sin(t * 6))
    ctx.set_line_width(5)
    ctx.stroke()

    if USER_COMMENT_SURF is not None:
        ctx.save()
        rrect(ctx, x + 8, y + 8, w - 16, h - 16, 12)
        ctx.clip()
        sw = USER_COMMENT_SURF.get_width()
        sh = USER_COMMENT_SURF.get_height()
        scale = (w - 16) / sw
        ctx.translate(x + 8, y + 8)
        ctx.scale(scale, scale)
        ctx.set_source_surface(USER_COMMENT_SURF, 0, 0)
        ctx.paint()
        ctx.restore()


def draw_surrender_board(ctx, x, y, t):
    """1971 Surrender counter board with 93,000 POW indicator."""
    rrect(ctx, x - 260, y - 180, 520, 360, 20)
    rgba(ctx, (0.05, 0.07, 0.10), 0.96)
    ctx.fill()
    rrect(ctx, x - 260, y - 180, 520, 360, 20)
    rgba(ctx, FIRE, 0.9)
    ctx.set_line_width(5)
    ctx.stroke()

    text(ctx, "1971 WAR: 13 DAYS", x, y - 110, 42, GOLD, font=CAPTION_FONT)
    line(ctx, [(x - 220, y - 75), (x + 220, y - 75)], STEEL_DK, 2)
    
    pulse = 1.0 + 0.04 * math.sin(t * 8)
    ctx.save()
    ctx.translate(x, y + 10)
    ctx.scale(pulse, pulse)
    text(ctx, "93,000", 0, 0, 96, RED, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=14)
    ctx.restore()
    
    text(ctx, "LARGEST SURRENDER POST-WWII", x, y + 85, 30, WHITE, font=CAPTION_FONT, bold=False)
    text(ctx, "NEW NATION: BANGLADESH", x, y + 130, 26, INDIA_GREEN, font=CAPTION_FONT, bold=False)


def draw_nathu_la_post(ctx, x, y, t):
    """Nathu La 1967 snowy outpost with border marker and casualties counter."""
    # Snow mountains background
    poly(ctx, [(0, 600), (320, 380), (680, 560), (1080, 350), (1080, GROUND), (0, GROUND)], hexc("#2A3845"))
    poly(ctx, [(120, 480), (320, 380), (450, 490)], WHITE, 0.85)  # snow peak 1
    poly(ctx, [(850, 450), (1080, 350), (1080, 520)], WHITE, 0.85)  # snow peak 2

    # Border fence
    for fx in range(100, 1000, 120):
        line(ctx, [(fx, 580), (fx, GROUND)], STEEL, 6)
    line(ctx, [(80, 660), (1000, 660)], STEEL_DK, 4)
    line(ctx, [(80, 780), (1000, 780)], STEEL_DK, 4)

    # 1967 Nathu La Stats badge
    rrect(ctx, x - 240, y - 150, 480, 240, 16)
    rgba(ctx, (0.04, 0.06, 0.08), 0.95)
    ctx.fill()
    rrect(ctx, x - 240, y - 150, 480, 240, 16)
    rgba(ctx, CYAN, 0.9)
    ctx.set_line_width(4)
    ctx.stroke()

    text(ctx, "NATHU LA 1967 CLASH", x, y - 90, 40, GOLD, font=CAPTION_FONT)
    text(ctx, "340+ PLA TROOPS ELIMINATED", x, y - 25, 34, RED, font=CAPTION_FONT)
    text(ctx, "CHINESE FORCES RETREATED", x, y + 35, 30, CYAN, font=CAPTION_FONT)


def draw_pinned_link_card(ctx, x, y, t):
    """Glowing card indicating the pinned video link below."""
    rrect(ctx, x - 270, y - 130, 540, 240, 16)
    rgba(ctx, (0.06, 0.08, 0.12), 0.95)
    ctx.fill()
    glow(ctx, x, y - 10, 280, GOLD, 0.25)
    rrect(ctx, x - 270, y - 130, 540, 240, 16)
    rgba(ctx, GOLD, 0.9)
    ctx.set_line_width(4)
    ctx.stroke()

    text(ctx, "PINNED VIDEO LINK", x, y - 65, 42, SAFFRON, font=CAPTION_FONT)
    text(ctx, "CHECK COMMENTS BELOW", x, y - 5, 36, WHITE, font=CAPTION_FONT)
    
    # Downward bouncing arrow
    bounce = 8 * math.sin(t * 8)
    text(ctx, "GO AND REPLY NOW", x, y + 60 + bounce, 40, FIRE, font=CAPTION_FONT)


# ============================================================ Scene Classes

class CommentShock(Cued):
    def events(self, d):
        return [(0.1, "whoosh"), (at(self, "KAYAR", 0.35, d), "thud")]

    def draw(self, ctx, t, d):
        # Dark radar sweep background
        g = cairo.RadialGradient(540, 600, 80, 540, 600, 900)
        g.add_color_stop_rgb(0, *hexc("#2D1215"))
        g.add_color_stop_rgb(1, *hexc("#0E0708"))
        ctx.set_source(g)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()
        
        # Grid lines
        for gy in range(200, 1200, 100):
            line(ctx, [(0, gy), (W, gy)], RED, 1, 0.12)
        for gx in range(100, W, 120):
            line(ctx, [(gx, 200), (gx, 1200)], RED, 1, 0.12)

        # Radar sweep ray
        ang = (t * 2.2) % math.tau
        line(ctx, [(540, 600), (540 + 500 * math.cos(ang), 600 + 500 * math.sin(ang))], RED, 3, 0.4)

        # Header alert tag (shifted down to y=320 so it never clashes with header UI)
        rrect(ctx, 280, 310, 520, 64, 8)
        rgba(ctx, RED, 0.9)
        ctx.fill()
        text(ctx, "HOSTILE COMMENT DETECTED", 540, 354, 34, WHITE, font=CAPTION_FONT)

        # Comment card
        draw_comment_box(ctx, 100, 420, 880, 260, t)

        # Offended Indian Soldier silhouette in foreground (positioned right, scale 0.70)
        soldier(ctx, 840, GROUND, 0.70, t, pose="aim", flip=True)


class Surrender1971(Cued):
    def events(self, d):
        return [(0.1, "whoosh"), (at(self, "93,000", 0.4, d), "boom"), (at(self, "SURRENDER", 0.7, d), "thud")]

    def draw(self, ctx, t, d):
        # Fiery battle atmosphere
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, *hexc("#1E0F07"))
        g.add_color_stop_rgb(0.7, *hexc("#3D1C08"))
        g.add_color_stop_rgb(1, *hexc("#0A0604"))
        ctx.set_source(g)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()

        # Surrender Stats Board
        draw_surrender_board(ctx, 540, 520, t)

        # Ground silhouettes: surrendering enemy rifles stacked
        for rx in range(160, 920, 70):
            line(ctx, [(rx, GROUND), (rx - 25, GROUND - 110)], STEEL_DK, 8)
            line(ctx, [(rx, GROUND), (rx + 25, GROUND - 110)], STEEL_DK, 8)
            circle(ctx, rx, GROUND - 115, 8, hexc("#2A2A2A"))

        # Standing victorious Indian jawan
        soldier(ctx, 160, GROUND, 0.74, t, pose="stand")


class NathuLa1967(Cued):
    def events(self, d):
        return [(0.1, "whoosh"), (at(self, "300", 0.45, d), "boom")]

    def draw(self, ctx, t, d):
        # Cold mountain snow atmosphere
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, *hexc("#0C1520"))
        g.add_color_stop_rgb(0.7, *hexc("#182A3A"))
        g.add_color_stop_rgb(1, *hexc("#060A0E"))
        ctx.set_source(g)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()

        # Nathu La snowy border & stats
        draw_nathu_la_post(ctx, 540, 510, t)

        # Indian jawan holding Kodanda/Rifle on mountain
        soldier(ctx, 240, GROUND, 0.75, t, pose="aim")
        soldier(ctx, 380, GROUND, 0.70, t + 1, pose="stand")


class CallToAction(Cued):
    def events(self, d):
        return [(0.1, "whoosh"), (at(self, "PIN", 0.35, d), "shimmer"), (at(self, "YAAD", 0.75, d), "boom")]

    def draw(self, ctx, t, d):
        # Patriotic high-contrast background
        g = cairo.RadialGradient(540, 550, 60, 540, 550, 850)
        g.add_color_stop_rgb(0, *hexc("#3A2A12"))
        g.add_color_stop_rgb(1, *hexc("#0F0C07"))
        ctx.set_source(g)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()

        # Waving Tiranga in background
        flag(ctx, 540, 310, 360, 220, "in", t)

        # Pinned video link prompt card
        draw_pinned_link_card(ctx, 540, 680, t)

        # Proud Indian soldier silhouettes on sides
        soldier(ctx, 150, GROUND, 0.75, t, pose="stand")
        soldier(ctx, 930, GROUND, 0.75, t, pose="stand", flip=True)


SCENE_CLASSES = {
    "comment_shock": CommentShock,
    "surrender_1971": Surrender1971,
    "nathu_la_1967": NathuLa1967,
    "call_to_action": CallToAction,
}


def write_alignment(final: Path) -> None:
    out = [
        {"scene": spec["key"], "start": round(s["start"], 3), "dur": round(s["dur"], 3),
         "words": [{"t": round(s["start"] + st, 3), "w": w} for st, w in s["captions"]]}
        for spec, s in zip(SPEC, engine.SCENES)
    ]
    path = final.with_suffix(".json")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Alignment: {path}")


# ============================================================ Upload Kit

UPLOAD = {
    "titles": [
        "Chinese User Ne Kaha: 'Indians Me Dam Nahi' - Jawab Do! #shorts",
        "Chinese Comment: 'India Never Fought Real War' - Reality Check! #shorts",
        "1971 Me 93,000 Surrender Bhool Gaye? Chinese Troll Ko Jawab #shorts",
        "Chinese Ne Humare Jawano Ko Lalkara: Check Pinned Comment #shorts",
    ],
    "title": "Chinese User Ne Kaha: 'Indians Me Dam Nahi' - Jawab Do! #shorts",
    "thumb_text": "JAWAB DO!",
    "queries": ["1971 surrender 93000", "nathu la 1967 clash", "chinese comment india"],
    "description": """Ek Chinese user ne hamare video par comment karke kaha ki Bharat ne kabhi asli jung nahi dekhi aur hum me ladne ka dam nahi hai!

Unhone 1962 ka jhootha propaganda failane ki koshish ki.
Par shayad wo bhool gaye:
- 1971: Sirf 13 dinon me 93,000 sainikon se hathiyar dalwaye (World War II ke baad sabse bada surrender!). Naya desh Bangladesh bana.
- 1967 (Nathu La): Indian Army ne PLA ke 340+ sainikon ko dher kiya aur unhe peeche hatna pada!

Maine pinned comment me us video ka link daal diya hai. Jao aur is Chinese user ko comment me batao ki Bharat aur Hindustani Fauj kya cheez hai! 🇮🇳🔥

#Shorts #IndianArmy #1971War #NathuLa #RealityShift
""",
    "tags": [
        "chinese comment india", "1971 war surrender", "93000 pakistani surrender",
        "nathu la 1967", "indian army bravery", "reality shift", "defence shorts",
        "india china border", "indian army vs pla",
    ],
    "hashtags": ["#Shorts", "#IndianArmy", "#RealityShift"],
    "pinned_comment": "👇 Us video ka link jahan is Chinese user ne comment kiya hai:\n[PASTE_VIDEO_LINK_HERE]\n\nJao aur batao inko comment mein jaakar ki Hindustani Fauj kya cheez hai! 🇮🇳🔥",
}


def thumbnail(ctx):
    # Dramatic red and black background
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc("#3A0B0F"))
    g.add_color_stop_rgb(0.6, *hexc("#120507"))
    g.add_color_stop_rgb(1, *hexc("#000000"))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()

    # Hostile comment card
    draw_comment_box(ctx, 140, 280, 800, 240, 1.0)

    # Big Impact text
    text(ctx, "CHINESE NE KAHA:", 540, 640, 88, WHITE, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "'INDIANS ME DAM NAHI'", 540, 770, 92, RED, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=20)
    
    # 93,000 Surrender slap
    rrect(ctx, 180, 930, 720, 140, 16)
    rgba(ctx, (0.08, 0.1, 0.14), 0.95)
    ctx.fill()
    rrect(ctx, 180, 930, 720, 140, 16)
    rgba(ctx, GOLD)
    ctx.set_line_width(6)
    ctx.stroke()
    text(ctx, "1971: 93,000 SURRENDER!", 540, 1020, 64, GOLD, font=CAPTION_FONT)

    # Call to action footer
    text(ctx, "JAWAB DO COMMENTS MEIN!", 540, 1380, 84, FIRE, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, PAL["ui"], a=0.85)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.chinese_comment")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    total = sum(s["dur"] for s in engine.SCENES)
    write_alignment(final)
    upload_kit.build(story, final, total)
    if total > MAX_SECONDS:
        raise SystemExit(f"[length] {total:.1f}s is over the {MAX_SECONDS:.0f}s lock")


if __name__ == "__main__":
    main()
