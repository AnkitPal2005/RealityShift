"""Karna Rahasya: Mahabharat Ka Sabse Bada Chhal (~21-23s katha, 4 scenes).

Usage (from SanatanKatha/):
  python make.py karna --preview       # preview contact sheet & thumbnail
  python make.py karna --kiki-split    # splits user audio into lines
  python make.py karna                 # final render with music & devta characters

Rahasya:
Daanveer Karna was born with celestial Kavach (armor) and Kundal (earrings) granted by Surya Dev,
rendering him completely invincible to any weapon in creation.
To protect his son Arjuna, Devraj Indra took the disguise of an impoverished Brahmin during Karna's
sacred dawn worship and asked for his flesh-grown golden armor. Karna, fully aware of the deception,
sliced the armor off his own chest with a smile.
Compounded by Guru Parashurama's curse that caused him to forget the Brahmastra invocation when facing death,
and the curse of the earth sinking his chariot wheel, Karna was slain unarmed on Kurukshetra.
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
from core.devta import group, place, halo, smooth, ink, ell, gem, limb, hand, sheen, eye, shade, bow, line, circle, rrect, text

TOPIC = "KARNA KAVACH KUNDAL RAHASYA"
OUTPUTS = {"edge": "karna_short.mp4"}
MUSIC_STYLE = "tension"   # Dramatic mythological conflict & mystery
MUSIC_BPM = 82            # Focused tension pulse
MUSIC_VOLUME = 0.12       # Voiceover clarity
TAIL_PAD = 0.0            # Zero gap between scenes - seamless flow
MAX_GAP = None            # Keep audio 100% natural, uncut and continuous (no syllable chopping!)

WHITE = (1.0, 1.0, 1.0)
GOLD_HI = hexc("#FFE066")
FIRE_ORANGE = hexc("#FF5500")
FIRE_YELLOW = hexc("#FFCC00")
BLOOD_RED = hexc("#B71C1C")
DEEP_RED = hexc("#8B0000")
WAR_SMOKE = hexc("#211A1E")
MUD_BROWN = hexc("#3E2723")

SOURCES = [
    "Mahabharata (Vana Parva, Kundalaharana Parva): Indra disguised as a Brahmin begs for Karna's Kavach and Kundal; Karna slices the armor from his body despite Surya's warning.",
    "Mahabharata (Shanti Parva): Guru Parashurama curses Karna that the invocation of the supreme Brahmastra will fail him at the decisive hour of his death.",
    "Mahabharata (Karna Parva): The earth swallows Karna's left chariot wheel; Arjuna slays the unarmed Karna with the Anjalika arrow at Krishna's command.",
]

SPEC = [
    {"key": "hook", "text": "SABSE BADA CHHAL?",
     "visual": "Dawn battlefield: Karna slicing chest armor with golden light and blood-tinted divine glow",
     "vo": [("punch", [("कर्ण को कोई अस्त्र नहीं,", "KARNA KO KOI ASTRA NAHI,"),
                       ("उसका अपना कवच मार गया!", "USKA APNA KAVACH MAAR GAYA!")])]},
    {"key": "shraap", "text": "INDRA AUR PARASHURAM",
     "visual": "Left: trembling Indra receiving golden kavach; Right: Parashurama with blazing fiery eyes and Parashu axe",
     "vo": [("tell", [("जब दान में कुंडल कटे,", "JAB DAAN MEIN KUNDAL KATE,"),
                      ("तब इंद्र भी कांप उठे!", "TAB INDRA BHI KAANP UTHE!"),
                      ("लेकिन सबसे बड़ा वार तब हुआ", "LEKIN SABSE BADA WAAR TAB HUA"),
                      ("जब गुरु परशुराम के श्राप ने", "JAB GURU PARASHURAM KE SHRAAP NE"),
                      ("ब्रह्मास्त्र की विद्या ही छीन ली!", "BRAHMASTRA KI VIDYA HI CHHEEN LI!")])]},
    {"key": "climax", "text": "KURUKSHETRA CHHAL",
     "visual": "Kurukshetra mud: Chariot wheel sunk; Arjuna drawing Gandiva; Krishna pointing; unarmed Karna lifting wheel",
     "vo": [("fast", [("कुरुक्षेत्र में धंसा पहिया", "KURUKSHETRA MEIN DHANSA PAHIYA"),
                      ("और आखिरी श्राप जाग उठा!", "AUR AAKHIRI SHRAAP JAAG UTHA!"),
                      ("निहत्थे कर्ण पर बाण चला,", "NIHATTHE KARNA PAR BAAN CHALA,"),
                      ("फिर भी दुनिया जानती है...", "PHIR BHI DUNIYA JAANTI HAI...")])]},
    {"key": "loop", "text": "ASLI YODDHA KAUN?",
     "visual": "Invincible Karna close-up with golden eyes and calm smile; question card: ARJUN YA KARNA?",
     "vo": [("whisper", [("कि अगर छल का यह खेल", "KI AGAR CHHAL KA YEH KHEL"),
                         ("न रचा गया होता,", "NA RACHA GAYA HOTA,"),
                         ("तो...", "TO...")])]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)

HOT = hot_words({
    "KARNA": dv.SAFFRON, "ASTRA": hexc("#FF5252"), "KAVACH": GOLD_HI, "KUNDAL": GOLD_HI,
    "INDRA": hexc("#BFE6FF"), "PARASHURAM": hexc("#FF5252"), "SHRAAP": hexc("#FF1744"),
    "BRAHMASTRA": GOLD_HI, "KURUKSHETRA": dv.SAFFRON, "PAHIYA": GOLD_HI, "BAAN": hexc("#FF5252"),
    "CHHAL": hexc("#FF1744"), "ARJUN": hexc("#BFE6FF")
})


# -----------------------------------------------------------------------------
# Backgrounds & Custom Visual Elements
# -----------------------------------------------------------------------------
def dawn_surya_bg(ctx, t, glow_int=1.0):
    """Dramatic early dawn sky with rising crimson-gold Surya Dev disc."""
    dv.sky(ctx, hexc("#0A0314"), hexc("#380D24"), hexc("#7A1C16"), 0.55)
    # Divine Surya Disc
    sun_x, sun_y = 540, 480
    halo(ctx, sun_x, sun_y, 220, t, c=FIRE_ORANGE, a=0.45 * glow_int)
    halo(ctx, sun_x, sun_y, 140, t, c=GOLD_HI, a=0.75 * glow_int)
    circle(ctx, sun_x, sun_y, 75, hexc("#FFF9C4"), 0.95)

    # Holy River Ganga / Ghat waters at bottom
    g = cairo.LinearGradient(0, 1050, 0, H)
    g.add_color_stop_rgba(0, 0.45, 0.12, 0.08, 0.8)
    g.add_color_stop_rgba(1, 0.15, 0.04, 0.06, 0.95)
    ctx.rectangle(0, 1050, W, H - 1050)
    ctx.set_source(g)
    ctx.fill()
    # Water ripples
    for ri in range(5):
        ry = 1080 + ri * 40
        line(ctx, [(120 + ri * 40, ry), (W - 120 - ri * 30, ry)], GOLD_HI, 2.5, 0.35)


def kurukshetra_dusk_bg(ctx, t, smoke=True):
    """War-torn dusk battlefield of Kurukshetra with smoke and fire haze."""
    dv.sky(ctx, hexc("#1A050B"), hexc("#4A1016"), hexc("#7E2412"), 0.58)
    # Distant flaming chariots & war flags silhouette
    if smoke:
        for si in range(8):
            sx = 80 + si * 135
            sy = 680 + 35 * math.sin(t * 2.0 + si)
            circle(ctx, sx, sy, 70 + si * 8, WAR_SMOKE, 0.45)
    # Blood-soaked earth of Kurukshetra
    g = cairo.LinearGradient(0, 1020, 0, H)
    g.add_color_stop_rgb(0, 0.22, 0.08, 0.08)
    g.add_color_stop_rgb(0.5, 0.15, 0.06, 0.06)
    g.add_color_stop_rgb(1, 0.08, 0.04, 0.04)
    ctx.rectangle(0, 1020, W, H - 1020)
    ctx.set_source(g)
    ctx.fill()


def parashurama(ctx, x, y, s, t, flip=False, a=1.0):
    """Maharishi Parashurama: Towering warrior sage with flaming aura and golden Parashu axe."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(-s if flip else s, s)

        skin = hexc("#8D6E63")
        hair = hexc("#E0E0E0")  # Venerable grey-white sage locks

        # Fiery anger aura
        halo(ctx, 0, -560, 200, t, c=FIRE_ORANGE, a=0.55)

        # Matted sage dreadlocks (Jata)
        for side in (-1, 1):
            smooth(ctx, [(side * 60, -700), (side * 110, -600), (side * 125, -480), (side * 95, -440), (side * 70, -540)])
            ink(ctx, hair)
        ell(ctx, 0, -680, 105, 105)
        ink(ctx, hair)

        # Body: Saffron ascetic vastra
        smooth(ctx, [(-110, -350), (110, -350), (120, -200), (95, -120), (0, -140), (-95, -120), (-120, -200)])
        ink(ctx, dv.SAFFRON)
        # Bare torso with Rudraksha malas and Janeu
        smooth(ctx, [(-115, -500), (115, -500), (110, -350), (-110, -350)])
        ink(ctx, skin)
        line(ctx, [(-90, -500), (70, -350)], WHITE, 4)  # Sacred Thread (Janeu)

        # Face & Fiery Blazing Eyes
        ell(ctx, 0, -560, 68, 76)
        ink(ctx, skin)
        for ex in (-28, 28):
            circle(ctx, ex, -570, 11, WHITE)
            circle(ctx, ex, -570, 7, FIRE_ORANGE)
            circle(ctx, ex, -570, 4, hexc("#FFE082"))
            # Glowing laser rage
            line(ctx, [(ex, -570), (ex - 80, -590)], FIRE_ORANGE, 3, 0.8)

        # White sage beard
        smooth(ctx, [(-55, -540), (55, -540), (35, -420), (0, -370), (-35, -420)])
        ink(ctx, hair)

        # Legendary Parashu Battle Axe in right hand
        axe_x, axe_y = -140, -480
        # Shaft
        line(ctx, [(axe_x, -760), (axe_x + 30, -240)], hexc("#4E342E"), 14)
        # Golden crescent axe blade
        ctx.move_to(axe_x - 10, -720)
        ctx.curve_to(axe_x - 90, -680, axe_x - 90, -580, axe_x - 10, -540)
        ctx.curve_to(axe_x - 30, -630, axe_x - 30, -630, axe_x - 10, -720)
        ctx.close_path()
        ink(ctx, GOLD_HI, 4)
        sheen(ctx, axe_x - 45, -630, 25, 45, 0.35)

        # Left hand raised in fiery curse mudra
        limb(ctx, [(95, -490), (150, -470), (170, -540)], skin, 42)
        hand(ctx, 170, -540, skin, 26)
        # Curse lightning sparks
        for sp in range(5):
            sp_rad = sp * (math.pi / 2.5) + t * 4.0
            line(ctx, [(170, -540), (170 + 40 * math.cos(sp_rad), -540 + 40 * math.sin(sp_rad))], FIRE_YELLOW, 3.5, 0.85)

        ctx.restore()

    group(ctx, a, draw)


def sunken_chariot_wheel(ctx, x, y, s, t):
    """The cursed heavy wooden chariot wheel sinking deep into Kurukshetra mud."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # Mud crater mound
    smooth(ctx, [(-150, 40), (150, 40), (130, -20), (50, -50), (-60, -45), (-140, -10)])
    ink(ctx, MUD_BROWN)

    # Wheel tilted at 18 degrees, half buried in mud
    ctx.rotate(math.radians(-18))
    circle(ctx, 0, 0, 110, hexc("#5D4037"))
    circle(ctx, 0, 0, 92, hexc("#271C19"))
    circle(ctx, 0, 0, 32, GOLD_HI)

    # 12 heavy wooden spokes
    for i in range(12):
        ang = i * (2 * math.pi / 12) + math.sin(t * 1.5) * 0.05
        line(ctx, [(28 * math.cos(ang), 28 * math.sin(ang)), (90 * math.cos(ang), 90 * math.sin(ang))], hexc("#8D6E63"), 7)

    # Mud splatters over the wheel
    ctx.rotate(math.radians(18))
    for mi in (-70, -20, 30, 80):
        ell(ctx, mi, 10, 24, 14)
        ink(ctx, hexc("#1B0000"))

    ctx.restore()


# -----------------------------------------------------------------------------
# Scene Implementations (4 Scenes strictly matched to 21-23s voiceover)
# -----------------------------------------------------------------------------
class HookScene(katha.Cued):
    """Scene 1: 0:00 to 0:03 - Frame 0 Shock. Karna slicing chest armor with golden light & blood glow."""
    def beats(self, d):
        c = self.cue
        return {"karna": c("KARNA", 0.1), "astra": c("ASTRA", d * 0.35), "kavach": c("KAVACH", d * 0.70)}

    def events(self, d):
        b = self.beats(d)
        return [(b["karna"], "whoosh"), (b["astra"], "zap"), (b["kavach"], "boom")]

    def draw(self, ctx, t, d):
        dawn_surya_bg(ctx, t, glow_int=1.2)

        # Karna in center slicing his golden chest armor
        # Pulsing divine golden aura and blood-tinted sacrificial glow
        u = min(1.0, t / (d * 0.7))
        kavach_cut = max(0.1, 1.0 - u * 0.6)

        halo(ctx, 540, 780, 240, t, c=GOLD_HI, a=0.75)
        halo(ctx, 540, 780, 160, t, c=BLOOD_RED, a=0.45 * u)

        # Draw Karna
        dv.karna(ctx, 540, 1170, 0.76, t, pose="give", kavach=kavach_cut, mood="calm")

        # Golden Light Rays erupting from chest
        for ray_i in range(8):
            ray_ang = ray_i * (math.pi / 4.0) + (t * 1.5)
            r_len = 160 + 50 * math.sin(t * 6.0 + ray_i)
            line(ctx, [(540, 780), (540 + r_len * math.cos(ray_ang), 780 + r_len * math.sin(ray_ang))], GOLD_HI, 6, 0.8)

        # Dagger in hand with blood and gold glint
        dagger_x = 540 + 30 * math.sin(t * 3.0)
        dagger_y = 790
        line(ctx, [(dagger_x - 30, dagger_y - 40), (dagger_x + 20, dagger_y + 30)], WHITE, 8)
        circle(ctx, dagger_x + 20, dagger_y + 30, 9, BLOOD_RED, 0.9)

        # Frame 0 Punchy Top Ribbon (Safe from overlays)
        rrect(ctx, 160, 310, 760, 85, 14)
        rgba(ctx, hexc("#100806"), 0.94)
        ctx.fill()
        rrect(ctx, 160, 310, 760, 85, 14)
        rgba(ctx, hexc("#FF1744"), 0.95)
        ctx.set_line_width(4)
        ctx.stroke()
        text(ctx, "SABSE BADA CHHAL?", 540, 365, 42, GOLD_HI, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=8)


class DaanShraapScene(katha.Cued):
    """Scene 2: 0:03 to 0:11 - Left: Indra receiving armor; Right: Parashurama's blazing curse."""
    def beats(self, d):
        c = self.cue
        return {
            "kundal": c("KUNDAL", 0.4),
            "indra": c("INDRA", d * 0.3),
            "parashuram": c("PARASHURAM", d * 0.6),
            "brahmastra": c("BRAHMASTRA", d * 0.85)
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["kundal"], "shimmer"), (b["indra"], "whoosh"), (b["parashuram"], "boom"), (b["brahmastra"], "zap")]

    def draw(self, ctx, t, d):
        dawn_surya_bg(ctx, t, glow_int=0.9)

        # Split dynamics:
        # Left: Brahmin Indra receiving golden Kavach
        dv.brahmin(ctx, 250, 1170, 0.74, t, pose="beg", mood="smile", flip=False)

        # Floating glowing Kavach Kundal between Indra and Karna
        float_y = 820 + 15 * math.sin(t * 3.5)
        halo(ctx, 400, float_y, 75, t, c=GOLD_HI, a=0.85)
        # Golden armor scales floating
        for sc in (-20, 0, 20):
            circle(ctx, 400 + sc, float_y, 18, GOLD_HI, 0.95)
            circle(ctx, 400 + sc, float_y, 9, WHITE, 0.9)

        # Karna in middle standing noble without armor
        dv.karna(ctx, 520, 1170, 0.74, t, pose="stand", kavach=0.2, mood="smile", flip=True)

        # Right: Maharishi Parashurama standing with fiery battle axe and blazing eyes!
        parashurama(ctx, 840, 1170, 0.76, t, flip=True)

        # Top indicator ribbon
        rrect(ctx, 150, 310, 780, 85, 14)
        rgba(ctx, hexc("#100806"), 0.92)
        ctx.fill()
        rrect(ctx, 150, 310, 780, 85, 14)
        rgba(ctx, FIRE_ORANGE, 0.95)
        ctx.set_line_width(4)
        ctx.stroke()
        text(ctx, "INDRA KA DAAN & GURU KA SHRAAP", 540, 365, 36, WHITE, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=8)


class KurukshetraClimaxScene(katha.Cued):
    """Scene 3: 0:11 to 0:17 - Kurukshetra: Sunken wheel, Arjuna's Gandiva bow, Krishna's command."""
    def beats(self, d):
        c = self.cue
        return {
            "kurukshetra": c("KURUKSHETRA", 0.3),
            "pahiya": c("PAHIYA", d * 0.35),
            "nihatthe": c("NIHATTHE", d * 0.65),
            "duniya": c("DUNIYA", d * 0.85)
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["kurukshetra"], "whoosh"), (b["pahiya"], "boom"), (b["nihatthe"], "zap"), (b["duniya"], "whoosh")]

    def draw(self, ctx, t, d):
        kurukshetra_dusk_bg(ctx, t, smoke=True)

        # Left: Sunken Chariot Wheel in the deep mud
        sunken_chariot_wheel(ctx, 290, 1100, 1.15, t)

        # Karna on left: Unarmed, struggling in mud to lift the sunken wheel
        # Using custom bent pose trying to heave wheel
        dv.karna(ctx, 330, 1170, 0.74, t, pose="stand", kavach=0.0, mood="calm", flip=False)

        # Center-Right: Shri Krishna as divine charioteer pointing forward with decisive authority
        dv.krishna(ctx, 620, 1170, 0.72, t, pose="bless", flip=True, a=0.95)

        # Far Right: Arjuna drawing Gandiva bow with glowing divine arrow
        dv.barbarik(ctx, 850, 1170, 0.74, t, pose="shoot", mood="fierce", draw_amt=0.85, arrows=1, flip=True)

        # Glowing arrow flying or aimed towards Karna
        arrow_tip_x = 760 - (t * 80) % 220
        dv.divine_arrow(ctx, arrow_tip_x, 830, math.pi, 90, t, a=0.9, trail=0.6)

        # Tension ribbon
        rrect(ctx, 160, 310, 760, 85, 14)
        rgba(ctx, hexc("#100806"), 0.92)
        ctx.fill()
        rrect(ctx, 160, 310, 760, 85, 14)
        rgba(ctx, BLOOD_RED, 0.95)
        ctx.set_line_width(4)
        ctx.stroke()
        text(ctx, "KURUKSHETRA MEIN NIHATTHA KARNA", 540, 365, 34, GOLD_HI, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=8)


class LoopEndingScene(katha.Cued):
    """Scene 4: 0:17 to 0:21 - Infinite Loop: Invincible Karna smiling, seamless loop to frame 0."""
    def beats(self, d):
        c = self.cue
        return {
            "khel": c("KHEL", 0.3),
            "racha": c("RACHA", d * 0.45),
            "to": c("TO", d * 0.8)
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["khel"], "whoosh"), (b["racha"], "shimmer"), (b["to"], "ghanti")]

    def draw(self, ctx, t, d):
        dawn_surya_bg(ctx, t, glow_int=1.3)

        # Maharathi Karna standing tall with divine golden aura and serene smile
        halo(ctx, 540, 750, 220, t, c=GOLD_HI, a=0.85)
        dv.karna(ctx, 540, 1170, 0.78, t, pose="stand", kavach=0.9, mood="smile")

        # Floating golden divine particles and petals
        dv.petals(ctx, t, n=30, a=0.9)

        # High-Engagement Debate Prompt Card
        rrect(ctx, 120, 290, 840, 130, 16)
        rgba(ctx, hexc("#0C0806"), 0.94)
        ctx.fill()
        rrect(ctx, 120, 290, 840, 130, 16)
        rgba(ctx, GOLD_HI, 0.95)
        ctx.set_line_width(5)
        ctx.stroke()
        text(ctx, "ARJUN YA KARNA: ASLI YODDHA KAUN?", 540, 345, 34, WHITE, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=6)
        text(ctx, "COMMENT MEIN APNI RAYE DEIN", 540, 400, 38, GOLD_HI, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=8)

        # Animated pointer arrow pointing to the YouTube Shorts comment button
        arrow_y = 1260 + math.sin(t * 8.0) * 12
        ctx.set_source_rgb(GOLD_HI[0], GOLD_HI[1], GOLD_HI[2])
        ctx.move_to(540, arrow_y + 40)
        ctx.line_to(500, arrow_y)
        ctx.line_to(580, arrow_y)
        ctx.close_path()
        ctx.fill()


SCENE_CLASSES = {
    "hook": HookScene,
    "shraap": DaanShraapScene,
    "climax": KurukshetraClimaxScene,
    "loop": LoopEndingScene,
}

UPLOAD = {
    "title": "Karna Ko Kisne Mara: Shraap Ya Chhal? 😱 #shorts",
    "titles": [
        "Karna Ko Kisne Mara: Shraap Ya Chhal? 😱 #shorts",
        "Mahabharat Ka Sabse Bada Chhal: Karna Ka Rahasya #shorts",
        "Karna Ka Kavach Kundal Rahasya! 😱 #shorts",
        "Arjun vs Karna: Bina Chhal Ke Kaun Jeetta? #shorts",
        "Parashuram Ka Shraap Aur Karna Ka Ant #shorts",
    ],
    "thumb_text": "SABSE BADA CHHAL?",
    "queries": ["karna kavach kundal", "who killed karna", "karna vs arjun mahabharat"],
    "description": (
        "Daanveer Karna ko koi astra nahi, uska apna kavach maar gaya!\n"
        "Devraj Indra ka chhal, Guru Parashurama ka Brahmastra shraap, aur Kurukshetra mein dhasa pahiya...\n"
        "Kya Arjun sach mein Karna ko bina chhal ke hara sakte the? Apni raye comment mein zaroor batayein!\n\n"
        "Video pasand aaye toh like karein aur subscribe karein Divya Rahasya! 🙏🚩\n\n"
        "#Shorts #Karna #Mahabharat #Krishna #Arjun #DivyaRahasya #SanatanKatha"
    ),
    "tags": [
        "karna", "daanveer karna", "karna kavach kundal", "mahabharat", "arjun vs karna",
        "krishna", "parashuram shraap", "karna death", "divya rahasya", "shorts", "viral shorts sanatan"
    ],
    "hashtags": ["#Shorts", "#Karna", "#Mahabharat", "#Krishna"],
}


def thumbnail(ctx):
    """High-CTR YouTube Shorts cover: Karna slicing glowing armor, 'SABSE BADA CHHAL?' text."""
    dawn_surya_bg(ctx, 0.0, glow_int=1.4)
    halo(ctx, 540, 780, 240, 0.0, c=GOLD_HI, a=0.85)
    dv.karna(ctx, 540, 1170, 0.78, 0.0, pose="give", kavach=0.8, mood="calm")

    g = cairo.LinearGradient(0, 1150, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.88)
    ctx.rectangle(0, 1150, W, H - 1150)
    ctx.set_source(g)
    ctx.fill()

    g = cairo.LinearGradient(0, 0, 0, 780)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.92)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 780)
    ctx.set_source(g)
    ctx.fill()

    text(ctx, "SABSE BADA", 540, 290, 115, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "CHHAL?", 540, 420, 130, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "DIVYA RAHASYA", 540, 1800, 40, GOLD_HI, a=0.8)


def main():
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(sys.modules[__name__], eng)
    upload_kit.build(sys.modules[__name__], final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
