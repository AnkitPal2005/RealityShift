"""Ashwatthama Rahasya: Kya Mahabharat Ka Chiranjeevi Aaj Bhi Asirgarh Mein Zinda Hai? (~28-30s katha, 5 scenes).

Usage (from SanatanKatha/):
  python make.py ashwatthama --preview       # preview contact sheet & thumbnail
  python make.py ashwatthama --kiki-split    # splits user audio into lines
  python make.py ashwatthama                 # final render with music & devta characters

Rahasya:
Guru Dronacharya's son Ashwatthama was born with a divine jewel (Chintamani) on his forehead
granting him invulnerability against hunger, thirst, weapons, and disease.
When he fired the apocalyptic Brahmashira at the womb of Uttara to exterminate the Pandava lineage,
Shri Krishna angrily extracted the jewel from his skull and cursed him to roam the earth till
the end of Kaliyuga with an unhealing festering wound, smelling of blood and pus, without shelter or companionship.
Even today, at the 10th-century Gupteshwar Mahadev temple inside the impregnable Asirgarh Fort (Madhya Pradesh),
priests report that every morning before the temple gates are unlocked, a fresh dewy red rose and
sandalwood tilak are found offered upon the Shiva lingam by an unseen 9-foot-tall ascetic.
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

TOPIC = "ASHWATTHAMA ASIRGARH RAHASYA"
OUTPUTS = {"edge": "ashwatthama_short.mp4"}
MUSIC_STYLE = "tension"   # Dark ancient mystery & devotional bed
MUSIC_BPM = 78            # Deep haunting pulse
MUSIC_VOLUME = 0.12       # Voiceover clarity
TAIL_PAD = 0.04           # Zero awkward silence between chunks
MAX_GAP = 0.04            # Seamless speech flow

WHITE = (1.0, 1.0, 1.0)
RED_GEM = hexc("#D61F3A")
GOLD_HI = hexc("#FFE066")
FIRE_ORANGE = hexc("#FF5500")
FIRE_YELLOW = hexc("#FFCC00")
BLOOD_RED = hexc("#8B0000")
SHIVA_BLUE = hexc("#1A2B4C")
ASH_GREY = hexc("#3A3D40")
FORT_STONE = hexc("#1E1B18")

SOURCES = [
    "Mahabharata (Sauptika Parva, Sections 15-16): Krishna curses Ashwatthama after the invocation of the Brahmashira missile targeting Uttara's womb; the jewel is excised from his forehead and he is cursed to wander solitary for thousands of years.",
    "Bhavishya Purana & Local Epigraphic Lore: Ashwatthama is numbered among the Sapta-Chiranjeevi (seven immortals) destined to survive until the arrival of Kalki Avatar.",
    "Gupteshwar Mahadev Temple (Asirgarh Fort, Burhanpur, Madhya Pradesh): Centuries-old documented phenomenon of daily pre-dawn offerings (fresh red rose, ittar, and bilva patra) inside locked inner sanctum.",
]


# -----------------------------------------------------------------------------
# Backgrounds: Asirgarh Fort Night & Sanctum
# -----------------------------------------------------------------------------
def asirgarh_fort_bg(ctx, t, storm=False):
    """Dramatic ancient hill fortress of Asirgarh at dark midnight with lightning."""
    if storm:
        dv.sky(ctx, hexc("#0A0512"), hexc("#22102A"), hexc("#451428"), 0.58)
        # Lightning flash
        flash = max(0.0, math.sin(t * 7.0)) ** 12
        if flash > 0.15:
            ctx.set_source_rgba(1.0, 0.95, 0.9, 0.35 * flash)
            ctx.paint()
            # Lightning bolt
            line(ctx, [(520, 0), (510, 220), (550, 240), (530, 520)], (1.0, 1.0, 1.0), 4 * flash)
    else:
        dv.sky(ctx, hexc("#060A14"), hexc("#121E34"), hexc("#283C5A"), 0.58)
        # Moon disc with eerie blue halo
        glow(ctx, 840, 320, 240, hexc("#64B5F6"), 0.25)
        circle(ctx, 840, 320, 55, hexc("#E1F5FE"), 0.85)

    # Distant Satpura mountain silhouettes
    ctx.move_to(0, 920)
    for x in range(0, W + 1, 30):
        ctx.line_to(x, 920 - 35 * math.sin(x / 140 + 0.5))
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    rgba(ctx, hexc("#10141D"))
    ctx.fill()

    # Massive ancient Asirgarh stone battlements / fortress wall
    ctx.set_source_rgb(0.08, 0.07, 0.06)
    ctx.move_to(0, 1050)
    # Fort battlements (crenels)
    for bx in range(0, W + 1, 70):
        ctx.line_to(bx, 1030)
        ctx.line_to(bx + 40, 1030)
        ctx.line_to(bx + 40, 1060)
        ctx.line_to(bx + 70, 1060)
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    ctx.fill()

    # Mysterious night fog drifting
    for i in range(8):
        fog_x = (i * 180 + int(t * 40)) % (W + 200) - 100
        fog_y = 1120 + (i % 3) * 35
        ell(ctx, fog_x, fog_y, 220, 45)
        rgba(ctx, hexc("#D0E0FF"), 0.12)
        ctx.fill()


def shivling_sanctum_bg(ctx, t):
    """Ancient stone sanctum of Gupteshwar Mahadev inside Asirgarh Fort."""
    # Dark ancient stone wall chamber
    dv.sky(ctx, hexc("#0D0B0A"), hexc("#1A1512"), hexc("#28221D"), 0.6)

    # Stone pillars framing the sanctum
    for px in (110, W - 110):
        rrect(ctx, px - 65, 0, 130, H, 14)
        rgba(ctx, hexc("#15120F"), 0.95)
        ctx.fill()
        rrect(ctx, px - 65, 0, 130, H, 14)
        rgba(ctx, hexc("#38302A"), 0.8)
        ctx.set_line_width(6)
        ctx.stroke()

    # Stone floor
    ctx.move_to(0, 1100)
    ctx.line_to(W, 1100)
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    rgba(ctx, hexc("#1A1816"))
    ctx.fill()

    # Mystical golden-blue glow radiating from the Shivling
    glow(ctx, 540, 940, 420, hexc("#4FC3F7"), 0.28)
    glow(ctx, 540, 960, 240, hexc("#FFD54F"), 0.22)


# -----------------------------------------------------------------------------
# Characters & Props
# -----------------------------------------------------------------------------
def shivling_shrine(ctx, x, y, s, t, fresh_flower=True):
    """The sacred black granite Shivalinga with brass snake and fresh red rose."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)

        # 1. Stone Pedestal (Yonipeeth / Argha)
        # Lower base
        rrect(ctx, -180, -20, 360, 45, 14)
        rgba(ctx, hexc("#212121"))
        ctx.fill()
        # Middle disc
        ell(ctx, 0, -35, 160, 35)
        rgba(ctx, hexc("#263238"))
        ctx.fill()
        # Snout (Abhisheka channel pointing left)
        smooth(ctx, [(-140, -45), (-260, -40), (-250, -20), (-130, -20)])
        rgba(ctx, hexc("#212121"))
        ctx.fill()

        # 2. Black Granite Shivalinga Dome
        smooth(ctx, [(-65, -35), (-70, -170), (-50, -260), (0, -290), (50, -260), (70, -170), (65, -35)])
        rgba(ctx, hexc("#101418"))
        ctx.fill()
        sheen(ctx, -20, -160, 35, 140, 0.25)

        # 3. Sacred White Tripundra Bhasma (3 horizontal stripes) & Red Kumkum Bindi
        for dy in (-185, -170, -155):
            line(ctx, [(-34, dy), (34, dy)], WHITE, 5, a=0.95)
        circle(ctx, 0, -170, 7, RED_GEM)

        # 4. Golden Brass Nag Devta (coiled snake)
        for loop_y in (-70, -110):
            line(ctx, [(-68, loop_y), (68, loop_y)], GOLD_HI, 6)
        # Serpent Hood flared over Shivling
        smooth(ctx, [(-35, -270), (-45, -325), (0, -355), (45, -325), (35, -270)])
        rgba(ctx, GOLD_HI, 0.95)
        ctx.fill()

        # 5. The Mystery Fresh Red Rose (Taza Gulab) offered on top
        if fresh_flower:
            # Gentle divine breathing glow
            rose_y = -295
            glow(ctx, 0, rose_y, 90, hexc("#FF1744"), 0.55 + 0.15 * math.sin(t * 4.0))

            # Green rose leaves
            smooth(ctx, [(-25, rose_y + 12), (-45, rose_y + 8), (-30, rose_y - 4)])
            rgba(ctx, hexc("#2E7D32"))
            ctx.fill()
            smooth(ctx, [(25, rose_y + 12), (45, rose_y + 8), (30, rose_y - 4)])
            rgba(ctx, hexc("#2E7D32"))
            ctx.fill()

            # Velvety Red Rose Petals
            for p_ang in range(6):
                p_rad = p_ang * (math.pi / 3.0) + (t * 0.2)
                px = math.cos(p_rad) * 16
                py = rose_y + math.sin(p_rad) * 10
                ell(ctx, px, py, 22, 18)
                rgba(ctx, hexc("#D50000"), 0.95)
                ctx.fill()
            # Rose center bud
            circle(ctx, 0, rose_y, 14, hexc("#B71C1C"))
            circle(ctx, 0, rose_y, 8, hexc("#FF5252"))

            # Floating divine petals and scent particles
            for pt_i in range(8):
                pt_x = 40 * math.sin(t * 3.0 + pt_i * 1.2)
                pt_y = rose_y - 20 - (int(t * 50 + pt_i * 25) % 110)
                circle(ctx, pt_x, pt_y, 3.5, hexc("#FF5252"), 0.75)

        ctx.restore()

    group(ctx, 1.0, draw)


def ashwatthama_figure(ctx, x, y, s, t, pose="wander", a=1.0, flip=False):
    """Ashwatthama: Towering 9-foot warrior-ascetic with bleeding forehead wound."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(-s if flip else s, s)

        skin = hexc("#8D6E63")   # Dusky warrior skin
        hair = hexc("#1A120E")

        # 1. Height & Stature: Imposing warrior frame
        # Tall matted Jata (ascetic dreadlocks) flowing down shoulders
        for side in (-1, 1):
            smooth(ctx, [(side * 65, -730), (side * 115, -640), (side * 135, -530), (side * 118, -440), (side * 80, -460)])
            ink(ctx, hair)
        ell(ctx, 0, -700, 110, 110)
        ink(ctx, hair)

        # 2. Feet & Stance
        for fx in (-55, 55):
            ell(ctx, fx, -16, 48, 20)
            ink(ctx, skin)

        # 3. Torn Dark Warrior / Ascetic Garments
        dhoti = [(-115, -360), (115, -360), (135, -200), (145, -45), (60, -32), (0, -60), (-60, -32), (-145, -45), (-135, -200)]
        smooth(ctx, dhoti)
        ink(ctx, hexc("#4E342E"))  # Muddy bark-cloth / torn warrior attire

        # Broad rugged chest
        chest = [(-125, -520), (-60, -545), (60, -545), (125, -520), (130, -435), (105, -360), (-105, -360), (-130, -435)]
        smooth(ctx, chest)
        ink(ctx, skin)
        # Old war scars across chest
        line(ctx, [(-50, -460), (40, -420)], hexc("#5D4037"), 4)

        # 4. Neck & Majestic Intense Face
        rrect(ctx, -32, -588, 64, 56, 12)
        ink(ctx, skin)
        ell(ctx, 0, -655, 95, 100)
        ink(ctx, skin)

        # Rugged warrior beard
        smooth(ctx, [(-55, -650), (-45, -590), (0, -570), (45, -590), (55, -650)])
        rgba(ctx, hair)
        ctx.fill()

        # Eyes: Burning with ancient sorrow and intensity
        for side in (-1, 1):
            eye(ctx, side * 34, -665, 22, 24, t, look=(0.0, -0.2), iris=hexc("#4E1515"), seed=2)
            line(ctx, [(side * 12, -690), (side * 34, -698), (side * 56, -692)], hexc("#1A100C"), 6)

        # 5. FOREHEAD WOUND OR JEWEL
        if pose == "jewel":
            # The shining Chintamani jewel before being snatched
            glow(ctx, 0, -725, 65, hexc("#FF1744"), 0.85)
            gem(ctx, 0, -725, 15, RED_GEM)
            circle(ctx, 0, -725, 8, GOLD_HI)
        else:
            # The Bleeding Hollow Wound (Mani Chheen Li Gayi)
            # Jagged excised cavity
            ell(ctx, 0, -725, 16, 18)
            rgba(ctx, hexc("#3E0000"))
            ctx.fill()
            circle(ctx, 0, -725, 12, BLOOD_RED)
            # Glowing dark ember pulse
            circle(ctx, 0, -725, 6, hexc("#FF3D00"), 0.8 * math.sin(t * 5.0))
            # Blood trickling down between eyebrows to bridge of nose
            line(ctx, [(0, -710), (0, -675)], BLOOD_RED, 5)
            line(ctx, [(0, -675), (4, -650)], BLOOD_RED, 3)

        # 6. Poses
        if pose == "agony":
            # Hands clutching head in immense agony / curse
            limb(ctx, [(-115, -505), (-165, -620), (-85, -690)], skin, 36)
            hand(ctx, -85, -690, skin, 22)
            limb(ctx, [(115, -505), (165, -620), (85, -690)], skin, 36)
            hand(ctx, 85, -690, skin, 22)
            # Open cry mouth
            ell(ctx, 0, -605, 16, 20)
            rgba(ctx, hexc("#2A0808"))
            ctx.fill()

        elif pose == "brahmastra":
            # Powerful warrior drawing heavy bow
            limb(ctx, [(-115, -505), (-170, -440), (-160, -340)], skin, 36)
            hand(ctx, -160, -330, skin, 22)
            # Mighty bow
            line(ctx, [(-160, -620), (-160, -80)], hexc("#3E2723"), 10)
            # Glowing fiery Brahmastra arrow
            line(ctx, [(-160, -340), (120, -340)], FIRE_ORANGE, 8)
            glow(ctx, 120, -340, 60, FIRE_YELLOW, 0.85)

        elif pose == "sanyasi":
            # Holding ascetic wooden staff (Danda) in right hand, kamandalu in left
            limb(ctx, [(115, -505), (150, -430), (135, -340)], skin, 36)
            hand(ctx, 135, -330, skin, 22)
            # Staff
            line(ctx, [(135, -750), (135, -10)], hexc("#4E342E"), 8)
            limb(ctx, [(-115, -505), (-145, -420), (-125, -330)], skin, 36)
            hand(ctx, -125, -320, skin, 22)

        else:
            # Wandering stance
            limb(ctx, [(-115, -505), (-145, -420), (-120, -330)], skin, 36)
            hand(ctx, -120, -320, skin, 22)
            limb(ctx, [(115, -505), (145, -420), (120, -330)], skin, 36)
            hand(ctx, 120, -320, skin, 22)

        ctx.restore()

    group(ctx, a, draw)


# -----------------------------------------------------------------------------
# Story specification: 5 scenes (~28-30s total, matching KikiVoice audio)
# -----------------------------------------------------------------------------
SPEC = [
    {
        "key": "hook",
        "text": "ASHWATTHAMA ZINDA HAI?",
        "visual": "Midnight storm over Asirgarh fort, towering 9-foot shadowed figure of Ashwatthama",
        "vo": [
            ("tell", [
                ("क्या महाभारत का अश्वत्थामा", "KYA MAHABHARAT KA ASHWATTHAMA"),
                ("आज भी ज़िंदा है?", "AAJ BHI ZINDA HAI?"),
            ], 0.04),
        ],
    },
    {
        "key": "brahmastra",
        "text": "MANI CHHEEN LI GAYI",
        "visual": "Ashwatthama firing Brahmastra; Shri Krishna in blazing golden aura excising the divine forehead jewel",
        "vo": [
            ("tell", [
                ("उत्तरा पर ब्रह्मास्त्र चलाने पर,", "UTTARA PAR BRAHMASTRA CHALANE PAR,"),
                ("श्रीकृष्ण ने उसके माथे से", "SHRI KRISHNA NE USKE MAATHE SE"),
                ("अमर मणि छीन ली थी!", "AMAR MANI CHHEEN LI THI!"),
            ], 0.04),
        ],
    },
    {
        "key": "curse",
        "text": "BHAYANAK SHRAAP",
        "visual": "Ashwatthama clutching bleeding forehead in agony, wandering through dark thorns till end of Kalyuga",
        "vo": [
            ("tell", [
                ("श्राप था—कलयुग के अंत तक,", "SHRAAP THA—KALYUG KE ANT TAK,"),
                ("रिसते घाव के साथ", "RISTE GHAAV KE SAATH"),
                ("तड़पते हुए भटकोगे!", "TADAPTE HUYE BHATKOGE!"),
            ], 0.04),
        ],
    },
    {
        "key": "asirgarh",
        "text": "ASIRGARH KA CHALTI RAHASYA",
        "visual": "Locked heavy iron doors of Asirgarh temple; inside, sacred black Shivling has fresh dewy red rose",
        "vo": [
            ("tell", [
                ("आज भी असीरगढ़ किले में,", "AAJ BHI ASIRGARH KILE MEIN,"),
                ("ताला खुलने से पहले", "TALA KHULNE SE PEHLE"),
                ("शिवलिंग पर ताज़ा लाल गुलाब", "SHIVLING PAR TAAZA LAAL GULAAB"),
                ("कौन चढ़ा जाता है?", "KAUN CHADHA JAATA HAI?"),
            ], 0.04),
        ],
    },
    {
        "key": "cta_poll",
        "text": "HAR HAR MAHADEV",
        "visual": "Mystic 9-foot sadhu bowing before Mahadev's glowing Trishul; prompt: 'COMMENT MEIN HAR HAR MAHADEV!'",
        "vo": [
            ("ask", [
                ("क्या अश्वत्थामा सच में ज़िंदा है?", "KYA ASHWATTHAMA SACH MEIN ZINDA HAI?"),
                ("कमेंट में हर हर महादेव लिखें", "COMMENT MEIN HAR HAR MAHADEV LIKHEN"),
                ("और सब्सक्राइब करें दिव्य रहस्य!", "AUR SUBSCRIBE KAREIN DIVYA RAHASYA!"),
            ], 0.04),
        ],
    },
]

DELIVERY = delivery.build(SPEC)
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "ASHWATTHAMA": dv.SAFFRON, "ZINDA": GOLD_HI, "MAHABHARAT": dv.SAFFRON,
    "BRAHMASTRA": FIRE_ORANGE, "KRISHNA": hexc("#4FC3F7"), "MANI": RED_GEM,
    "CHHEEN": FIRE_ORANGE, "SHRAAP": hexc("#E53935"), "KALYUG": hexc("#90A4AE"),
    "GHAAV": RED_GEM, "BHATKOGE": hexc("#FF7043"), "ASIRGARH": GOLD_HI,
    "KILE": hexc("#FFA726"), "TALA": hexc("#B0BEC5"), "SHIVLING": hexc("#4FC3F7"),
    "GULAAB": RED_GEM, "CHADHA": dv.SAFFRON, "MAHADEV": GOLD_HI,
    "COMMENT": hexc("#FFE066"), "SUBSCRIBE": dv.SAFFRON, "DIVYA": dv.SAFFRON, "RAHASYA": GOLD_HI
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".—!")] = HOT[_k]


# -----------------------------------------------------------------------------
# Scene Classes
# -----------------------------------------------------------------------------
class HookScene(katha.Cued):
    """Scene 1: Midnight storm over Asirgarh fort, towering 9-foot shadowed figure."""
    def beats(self, d):
        c = self.cue
        return {"ashwa": c("ASHWATTHAMA", 0.6), "zinda": c("ZINDA", d * 0.5)}

    def events(self, d):
        b = self.beats(d)
        return [(b["ashwa"], "shankh"), (b["zinda"], "thunder")]

    def draw(self, ctx, t, d):
        asirgarh_fort_bg(ctx, t, storm=True)
        # 9-foot tall shadowed Ashwatthama silhouette standing atop fort battlements
        ashwatthama_figure(ctx, 540, 1180, 0.82, t, pose="sanyasi", a=0.95)
        # Eye-catching question ribbon
        card_w, card_h = 760, 80
        rrect(ctx, 540 - card_w / 2, 280, card_w, card_h, 14)
        rgba(ctx, hexc("#100A14"), 0.92)
        ctx.fill()
        rrect(ctx, 540 - card_w / 2, 280, card_w, card_h, 14)
        rgba(ctx, dv.SAFFRON, 0.95)
        ctx.set_line_width(4)
        ctx.stroke()
        text(ctx, "3000 SAAL KA RAHASYA", 540, 335, 42, dv.SAFFRON, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=8)


class BrahmastraScene(katha.Cued):
    """Scene 2: Ashwatthama firing Brahmastra; Shri Krishna in golden aura excising jewel."""
    def beats(self, d):
        c = self.cue
        return {"brahma": c("BRAHMASTRA", 0.7), "krishna": c("KRISHNA", d * 0.4), "mani": c("MANI", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["brahma"], "arrow"), (b["krishna"], "shimmer"), (b["mani"], "zap")]

    def draw(self, ctx, t, d):
        asirgarh_fort_bg(ctx, t, storm=False)
        # Shri Krishna on left (commanding, glowing with divine aura)
        dv.krishna(ctx, 270, 1160, 0.75, t, pose="bless")

        # Ashwatthama on right losing his jewel
        ashwatthama_figure(ctx, 810, 1170, 0.78, t, pose="jewel", flip=True)

        # Laser/Cosmic golden ray connecting Krishna's hand to Ashwatthama's forehead
        line(ctx, [(270, 820), (810, 610)], GOLD_HI, 8, a=0.85)
        glow(ctx, 810, 610, 80, RED_GEM, 0.9)


class CurseScene(katha.Cued):
    """Scene 3: Ashwatthama clutching bleeding forehead in agony, wandering through wasteland."""
    def beats(self, d):
        c = self.cue
        return {"shraap": c("SHRAAP", 0.6), "ghaav": c("GHAAV", d * 0.4), "bhatak": c("BHATKOGE", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["shraap"], "bell"), (b["ghaav"], "zap"), (b["bhatak"], "whoosh")]

    def draw(self, ctx, t, d):
        # Desolate wasteland with blood-red horizon
        dv.sky(ctx, hexc("#1A0505"), hexc("#3D0C0C"), hexc("#5A1515"), 0.58)
        # Ashwatthama center stage clutching head in agony
        shake = 4 * math.sin(t * 18.0)
        ashwatthama_figure(ctx, 540 + shake, 1180, 0.82, t, pose="agony")
        # Floating dark blood particles
        for bp_i in range(12):
            bx = 540 + 70 * math.sin(t * 3.0 + bp_i)
            by = 640 + (int(t * 70 + bp_i * 30) % 240)
            circle(ctx, bx, by, 4, BLOOD_RED, 0.8)


class AsirgarhScene(katha.Cued):
    """Scene 4: The 15-18s Anti-Drop Reveal: Locked Asirgarh temple, fresh rose on Shivling."""
    def beats(self, d):
        c = self.cue
        return {"kile": c("ASIRGARH", 0.6), "tala": c("TALA", d * 0.35), "gulaab": c("GULAAB", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["kile"], "whoosh"), (b["tala"], "zap"), (b["gulaab"], "ghanti")]

    def draw(self, ctx, t, d):
        shivling_sanctum_bg(ctx, t)
        # Magnificent Shivalinga with fresh dewy red rose
        shivling_shrine(ctx, 540, 1120, 1.25, t, fresh_flower=True)

        # Foreground locked iron gate / chains silhouette
        gate_alpha = max(0.0, 1.0 - (t / (d * 0.4)))
        if gate_alpha > 0.05:
            ctx.set_source_rgba(0.05, 0.05, 0.05, 0.85 * gate_alpha)
            for bar_x in range(160, W - 140, 90):
                ctx.rectangle(bar_x, 0, 16, H)
                ctx.fill()
            # Golden lock hanging
            circle(ctx, 540, 800, 35, hexc("#FFA000"), 0.9 * gate_alpha)

        # Question banner
        rrect(ctx, 160, 310, 760, 85, 14)
        rgba(ctx, hexc("#100806"), 0.92)
        ctx.fill()
        rrect(ctx, 160, 310, 760, 85, 14)
        rgba(ctx, hexc("#FF1744"), 0.95)
        ctx.set_line_width(4)
        ctx.stroke()
        text(ctx, "BAND TALE MEIN TAAZA GULAAB?", 540, 365, 38, hexc("#FFD54F"), font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=8)


class CtaPollScene(katha.Cued):
    """Scene 5: 3-Second Snap CTA: Mahadev Trishul & 9-foot sadhu bowing."""
    def beats(self, d):
        c = self.cue
        return {"zinda": c("ZINDA", 0.5), "mahadev": c("MAHADEV", d * 0.4), "subscribe": c("SUBSCRIBE", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["zinda"], "shankh"), (b["mahadev"], "ghanti"), (b["subscribe"], "shimmer")]

    def draw(self, ctx, t, d):
        shivling_sanctum_bg(ctx, t)
        # Giant Mahadev Trishul in background
        place(ctx, 540, 950, 1.1, t)
        dv.trishul(ctx, 0, 0, 1.0)
        ctx.restore()
        # 9-foot sadhu figure bowing in devotion on left
        ashwatthama_figure(ctx, 320, 1180, 0.76, t, pose="sanyasi", a=0.92)

        # Engagement prompt card
        rrect(ctx, 140, 290, 800, 130, 16)
        rgba(ctx, hexc("#0C0806"), 0.94)
        ctx.fill()
        rrect(ctx, 140, 290, 800, 130, 16)
        rgba(ctx, dv.SAFFRON, 0.95)
        ctx.set_line_width(5)
        ctx.stroke()
        text(ctx, "COMMENT MEIN LIKHIYE", 540, 345, 34, WHITE, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=6)
        text(ctx, "'HAR HAR MAHADEV' 🔱", 540, 400, 44, GOLD_HI, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=8)

        # Animated pointer arrow pointing down to comment section
        arrow_y = 1260 + math.sin(t * 8.0) * 12
        ctx.set_source_rgb(GOLD_HI[0], GOLD_HI[1], GOLD_HI[2])
        ctx.move_to(540, arrow_y + 40)
        ctx.line_to(500, arrow_y)
        ctx.line_to(580, arrow_y)
        ctx.close_path()
        ctx.fill()


SCENE_CLASSES = {
    "hook": HookScene,
    "brahmastra": BrahmastraScene,
    "curse": CurseScene,
    "asirgarh": AsirgarhScene,
    "cta_poll": CtaPollScene,
}

UPLOAD = {
    "title": "Ashwatthama Aaj Bhi Zinda Hai? 😱 Asirgarh Kile Ka Rahasya! #shorts",
    "titles": [
        "Ashwatthama Aaj Bhi Zinda Hai? 😱 Asirgarh Kile Ka Rahasya! #shorts",
        "Mahabharat Ke Ashwatthama Ka 3000 Saal Purana Rahasya! 🚩 #shorts",
        "Shri Krishna Ka Shraap: Asirgarh Fort Mein Aaj Bhi Ashwatthama? #shorts",
        "Shivling Par Taaza Phool Kaun Chadhata Hai? Ashwatthama Rahasya #shorts",
        "Asirgarh Kile Ke Gupteshwar Mahadev Ka Sach: Ashwatthama Zinda? #shorts",
    ],
    "thumb_text": "ASHWATTHAMA ZINDA?",
    "queries": ["ashwatthama zinda hai", "asirgarh fort mystery", "ashwatthama mahabharat shraap"],
    "description": (
        "Kya Mahabharat ke Guru Drona ke putra Ashwatthama aaj bhi dharti par zinda bhatak rahe hain? "
        "Madhya Pradesh ke Asirgarh kile mein bane Gupteshwar Mahadev mandir ka tala khulne se pehle Shivling par "
        "taaza gulab aur tilak kaun laga jata hai? Jaaniye Bhagwan Shri Krishna ke us bhayanak shraap ki poori satya katha.\n\n"
        "Har Har Mahadev! Video pasand aaye toh like aur subscribe zaroor karein. 🙏🚩\n\n"
        "#Shorts #Ashwatthama #Mahabharat #Shiva #DivyaRahasya #SanatanKatha"
    ),
    "tags": [
        "ashwatthama", "ashwatthama real proof", "asirgarh fort", "ashwatthama alive in kalyug",
        "mahabharat", "krishna shraap ashwatthama", "gupteshwar mahadev", "sanatan katha",
        "divya rahasya", "shorts", "viral shorts sanatan"
    ],
    "hashtags": ["#Shorts", "#Ashwatthama", "#Mahabharat", "#Shiva"],
}


def thumbnail(ctx):
    """1080x1920 cover: 'ASHWATTHAMA ZINDA?' over 9-foot shadowed warrior and glowing Shivling."""
    asirgarh_fort_bg(ctx, 0.0, storm=True)
    shivling_shrine(ctx, 540, 1160, 1.15, 0.0, fresh_flower=True)
    ashwatthama_figure(ctx, 360, 1180, 0.76, 0.0, pose="sanyasi")

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

    text(ctx, "ASHWATTHAMA", 540, 290, 125, dv.GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "AAJ BHI ZINDA HAI?", 540, 430, 82, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "DIVYA RAHASYA", 540, 1800, 40, dv.GOLD_HI, a=0.8)


def main():
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(sys.modules[__name__], eng)
    upload_kit.build(sys.modules[__name__], final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
