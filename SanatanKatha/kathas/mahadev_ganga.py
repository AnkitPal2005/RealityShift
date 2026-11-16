"""Mahadev Ka Krodh Aur Ganga Ka Ahankaar: 32 Din Ka Rahasya (~50-52s katha, seven scenes).

Usage (from SanatanKatha/):
  python make.py mahadev_ganga --preview       # preview contact sheet & thumbnail
  python make.py mahadev_ganga --kiki-export   # exports clean voice text files
  python make.py mahadev_ganga --kiki-split    # splits user audio into lines
  python make.py mahadev_ganga                 # final render with music & devta characters

Rahasya:
When King Bhagiratha's intense penance pleased Brahma to send celestial river Ganga to earth,
Ganga was proud of her untameable cosmic torrent and thought she would wash away Lord Shiva.
To shatter her pride, Devadhidev Mahadev untied his cosmic matted locks (Jataayein) on Mount Kailash.
Ganga fell like a thunderbolt, yet became completely lost in the maze of Shiva's locks for 32 days
without finding even a single drop's way out. Humbled, she prayed for forgiveness, and Mahadev
released her as the life-giving, purifying Bhagirathi.
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

TOPIC = "MAHADEV GANGA JATA RAHASYA"
OUTPUTS = {"edge": "mahadev_ganga_short.mp4"}
MUSIC_STYLE = "pulse"     # Dynamic sacred pulse bed
MUSIC_BPM = 72            # Distinct majestic tempo
MUSIC_VOLUME = 0.12       # Subtle background bed, dialogue stands out clearly
TAIL_PAD = 0.04           # Zero awkward pause between scenes
MAX_GAP = 0.04            # Seamless speech flow without stuttering
WHITE = (1.0, 1.0, 1.0)
RED_GEM = hexc("#D61F3A")
CYAN_WATER = hexc("#48CAE4")
GOLD_HI = hexc("#FFE066")

SOURCES = [
    "Valmiki Ramayana (Bala Kanda, Sarga 42-44): Bhagiratha's rigorous penance to bring Ganga from heaven to redeem the 60,000 sons of Sagara, and Shiva's containment of Ganga's tempestuous descent in his matted locks.",
    "Shiva Purana (Rudra Samhita, Sati Khanda): The humbling of Ganga's pride when she attempted to sweep away Lord Shiva into Patala, becoming trapped in his cosmic jata until her arrogance dissolved.",
    "Skanda Purana: The sacred lore of Bindu Sarovar where Mahadev released the sacred river in seven tranquil streams to sanctify the mortal realm.",
]


def ribbon(ctx, x, y, msg, col, u=1.0):
    """Single sleek ribbon at top: clean, zero overlap, Roman text (no tofu □□□)."""
    if u <= 0:
        return
    p = max(0.01, ease_out_back(clamp(u / 0.4)))
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(p, p)
    w = text_width(ctx, msg, 34) + 60
    rrect(ctx, -w / 2, -30, w, 60, 18)
    rgba(ctx, col, 0.92)
    ctx.fill_preserve()
    rgba(ctx, GOLD, 0.95)
    ctx.set_line_width(3)
    ctx.stroke()
    text(ctx, msg, 0, 10, 34, (1, 1, 1), bold=True)
    ctx.restore()


def himalaya_bg(ctx, t, cosmic=True):
    """Majestic snow-clad Himalayan peaks under cosmic star-filled sky."""
    if cosmic:
        dv.sky(ctx, hexc("#060A18"), hexc("#10193E"), hexc("#28163E"), 0.55)
        glow(ctx, 540, 600, 480, hexc("#4880FF"), 0.25)
    else:
        dv.sky(ctx, hexc("#081224"), hexc("#1B3058"), hexc("#3C2042"), 0.55)
        glow(ctx, 540, 650, 400, hexc("#FFAA48"), 0.3)

    # Distant glowing stars
    for i in range(25):
        sx = (i * 137 + 45) % W
        sy = (i * 93 + 60) % 550
        blink = (math.sin(t * 3.0 + i) + 1) / 2
        circle(ctx, sx, sy, 2 + blink * 2, WHITE, 0.4 + 0.5 * blink)

    # Mountain Layer 1 (Distant Snow Peaks)
    ctx.move_to(0, 940)
    for x in range(0, W + 1, 60):
        ctx.line_to(x, 940 - 55 * math.sin(x / 200 + 0.8) - 30 * math.sin(x / 75))
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    rgba(ctx, hexc("#1E284A") if cosmic else hexc("#2A1E3C"))
    ctx.fill()

    # Mountain Layer 2 (Snow Glaciers)
    ctx.move_to(0, 1040)
    for x in range(0, W + 1, 45):
        ctx.line_to(x, 1040 - 40 * math.sin(x / 140 + 1.5) - 20 * math.sin(x / 50))
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    rgba(ctx, hexc("#141C34") if cosmic else hexc("#161026"))
    ctx.fill()


def mahadev(ctx, x, y, s, t, pose="stand", jata_open=False, flip=False, a=1.0):
    """Devadhidev Mahadev: Neelkanth blue skin, Rudraksha, Vasuki snake, Trishul, and cosmic jata."""
    def draw():
        place(ctx, x, y, s, t, flip)
        halo(ctx, 0, -680, 210, t, c=hexc("#82C4FF"))
        skin = hexc("#8BB8E8")   # Neelkanth divine pale blue
        hair = hexc("#181412")

        # Matted Jata Locks
        if jata_open:
            # Cosmic wild jata spread across the sky
            wave = math.sin(t * 4) * 15
            for j_side in (-1, 1):
                smooth(ctx, [
                    (j_side * 40, -820),
                    (j_side * 180 + wave, -880),
                    (j_side * 280, -960),
                    (j_side * 360 + wave * 1.5, -920),
                    (j_side * 300, -840),
                    (j_side * 140, -780),
                ])
                ink(ctx, hair)
            # Center soaring locks
            smooth(ctx, [(0, -840), (-120, -960 + wave), (0, -1040), (120, -960 - wave), (0, -840)])
            ink(ctx, hair)
            # Glowing water droplets churning in locks
            for k in range(8):
                ang = t * 3 + k * (math.tau / 8)
                wx = math.cos(ang) * (90 + k * 12)
                wy = -920 + math.sin(ang) * 45
                circle(ctx, wx, wy, 8, CYAN_WATER, 0.8)
        else:
            # Regal topknot Jata
            ell(ctx, 0, -800, 90, 100)
            ink(ctx, hair)
            for side in (-1, 1):
                smooth(ctx, [(side * 40, -840), (side * 85, -780), (side * 100, -680), (side * 75, -690)])
                ink(ctx, hair)

        # Crescent Moon (Chandra) in Jata
        circle(ctx, -58, -825, 24, hexc("#FFF8D4"))
        circle(ctx, -48, -833, 21, hexc("#0B1033"))

        # Little Ganga sprout emerging at top
        ctx.move_to(0, -880)
        ctx.curve_to(30, -940, 50, -920, 35, -890)
        rgba(ctx, hexc("#C8E8FF"), 0.9)
        ctx.fill()

        # Feet with rudraksha bands
        for fx in (-52, 52):
            ell(ctx, fx, -14, 46, 20)
            ink(ctx, skin)
            line(ctx, [(fx - 24, -28), (fx, -22), (fx + 24, -28)], hexc("#5A2E14"), 8)

        # Tiger skin (Vyaghrambar) wrap
        tiger_pts = [(-116, -345), (116, -345), (132, -200), (145, -45), (60, -32), (0, -64), (-60, -32), (-145, -45), (-132, -200)]
        smooth(ctx, tiger_pts)
        ink(ctx, hexc("#C87220"))
        # Tiger stripes
        for ty in (-260, -180, -100):
            line(ctx, [(-100, ty), (-40, ty + 12)], hexc("#2A1204"), 7)
            line(ctx, [(40, ty + 12), (100, ty)], hexc("#2A1204"), 7)

        # Strong Torso (Ash-smeared Neelkanth)
        smooth(ctx, [(-128, -500), (-65, -524), (65, -524), (128, -500), (134, -430), (105, -340), (-105, -340), (-134, -430)])
        ink(ctx, skin)
        sheen(ctx, 0, -420, 80, 50, 0.14)

        # Rudraksha Mala across chest
        line(ctx, [(-95, -500), (-45, -450), (20, -390), (95, -330)], hexc("#4E220C"), 7)
        for rx, ry in [(-95, -500), (-65, -475), (-35, -440), (0, -410), (35, -380), (65, -350)]:
            circle(ctx, rx, ry, 7, hexc("#733212"))

        # Vasuki Naga coiled around neck
        ctx.move_to(-65, -570)
        ctx.curve_to(0, -520, 40, -530, 72, -565)
        ctx.set_line_width(20)
        rgba(ctx, hexc("#163A1E"))
        ctx.stroke()
        # Snake eye
        circle(ctx, 65, -575, 4, hexc("#FFCC00"))

        # Neck & Neelkanth blue throat
        rrect(ctx, -34, -575, 68, 62, 14)
        ink(ctx, skin)
        circle(ctx, 0, -550, 22, hexc("#2255A4"), 0.65)  # Poison mark glow

        # Head & Divine Face
        ell(ctx, 0, -650, 96, 108)
        ink(ctx, skin)

        # Tripundra (3 white ash lines) on forehead
        for ty in (-718, -706, -694):
            line(ctx, [(-38, ty), (38, ty)], WHITE, 4)

        # Third Eye (Trinetra) in vertical center
        smooth(ctx, [(0, -722), (12, -706), (0, -690), (-12, -706)], k=0.1)
        rgba(ctx, hexc("#FFAA22"), 0.95)
        ctx.fill()
        line(ctx, [(0, -716), (0, -696)], hexc("#D02020"), 4)

        # Serene or Commanding Eyes
        for side in (-1, 1):
            if pose == "meditate":
                ctx.move_to(side * 22, -652)
                ctx.curve_to(side * 36, -644, side * 50, -644, side * 58, -652)
                ctx.set_line_width(4)
                rgba(ctx, hexc("#1C2A3A"))
                ctx.stroke()
            else:
                eye(ctx, side * 36, -648, 23, 26, t, look=(0, 0), iris=hexc("#1C2E44"), seed=2)
            line(ctx, [(side * 14, -676), (side * 36, -684), (side * 60, -678)], hair, 6)

        # Calm smile
        ctx.move_to(-18, -604)
        ctx.curve_to(-6, -596, 6, -596, 18, -604)
        ctx.set_line_width(4)
        rgba(ctx, hexc("#A83248"))
        ctx.stroke()

        # Trishul & Damru
        trishul_x = -170
        dv.trishul(ctx, trishul_x, -430, 1.25, t)
        # Damru tied on Trishul
        circle(ctx, trishul_x + 15, -480, 12, hexc("#8E4B1C"))
        circle(ctx, trishul_x - 15, -480, 12, hexc("#8E4B1C"))

        # Arm Poses
        if pose == "bless":
            # Right hand in Abhaya Mudra
            limb(ctx, [(115, -480), (160, -420), (150, -330)], skin, 38)
            dv.palm(ctx, 150, -320, skin, ang=-0.1, s=1.15)
            # Left hand resting
            limb(ctx, [(-115, -480), (-150, -420), (-130, -340)], skin, 38)
            hand(ctx, -130, -330, skin, 22)
        elif pose == "open_jata":
            # Both hands raised to the jata in cosmic motion
            limb(ctx, [(-115, -480), (-160, -600), (-110, -720)], skin, 38)
            hand(ctx, -110, -730, skin, 22)
            limb(ctx, [(115, -480), (160, -600), (110, -720)], skin, 38)
            hand(ctx, 110, -730, skin, 22)
        else:
            # Holding Trishul with left, right resting
            limb(ctx, [(-115, -480), (-150, -430), (trishul_x, -430)], skin, 38)
            hand(ctx, trishul_x, -430, skin, 22)
            limb(ctx, [(115, -480), (145, -410), (120, -320)], skin, 38)
            hand(ctx, 120, -310, skin, 22)

        # STRICT Isolation: restore place() save
        ctx.restore()
    group(ctx, a, draw)


def bhagirath(ctx, x, y, s, t, pose="tapasya", flip=False, a=1.0):
    """Suryavanshi King Bhagiratha: Penance robes, ascetic devotion, standing on one leg / praying."""
    def draw():
        place(ctx, x, y, s, t, flip)
        skin = hexc("#DEAA78")
        hair = hexc("#28160C")

        # Feet / Legs
        if pose == "tapasya":
            # Standing on one leg (Left leg straight on ground, Right leg folded up on knee)
            # Left standing leg
            limb(ctx, [(-20, -310), (-20, -180), (-20, -20)], skin, 36)
            ell(ctx, -20, -14, 42, 18)
            ink(ctx, skin)
            # Right folded leg
            limb(ctx, [(-10, -310), (50, -230), (-10, -170)], skin, 34)
            ell(ctx, -10, -165, 34, 16, rot=-0.4)
            ink(ctx, skin)
        else:
            # Both legs standing in surrender
            for fx in (-35, 35):
                limb(ctx, [(fx, -310), (fx, -180), (fx, -20)], skin, 36)
                ell(ctx, fx, -14, 40, 18)
                ink(ctx, skin)

        # Saffron ascetic dhoti
        dhoti = [(-80, -320), (80, -320), (95, -190), (60, -70), (-60, -70), (-95, -190)]
        smooth(ctx, dhoti)
        ink(ctx, dv.SAFFRON)

        # Ascetic Torso
        smooth(ctx, [(-85, -480), (-40, -500), (40, -500), (85, -480), (75, -390), (65, -310), (-65, -310), (-75, -390)])
        ink(ctx, skin)

        # Head & Ascetic Beard/Jata
        rrect(ctx, -24, -540, 48, 48, 10)
        ink(ctx, skin)
        ell(ctx, 0, -590, 72, 80)
        ink(ctx, skin)
        # Ascetic topknot
        circle(ctx, 0, -680, 40, hair)
        # Sage beard
        smooth(ctx, [(-35, -590), (0, -520), (35, -590), (0, -570)])
        ink(ctx, hair)

        # Arms & Hands
        if pose == "tapasya":
            # Both arms raised high above head with folded palms in intense tapasya (Vrikshasana)
            limb(ctx, [(-75, -470), (-90, -620), (-20, -760)], skin, 32)
            limb(ctx, [(75, -470), (90, -620), (20, -760)], skin, 32)
            # Folded hands at apex
            circle(ctx, 0, -780, 20, skin)
        else:
            # Folded namaste at chest in gratitude / surrender
            limb(ctx, [(-75, -470), (-45, -430), (-15, -430)], skin, 30)
            limb(ctx, [(75, -470), (45, -430), (15, -430)], skin, 30)
            circle(ctx, 0, -440, 18, skin)

        ctx.restore()
    group(ctx, a, draw)


def cosmic_ganga_torrent(ctx, t, a=1.0):
    """Pralayankari swirling cosmic river Ganga cascading from the heavens."""
    ctx.save()
    # Cascading celestial river stream from top center
    for i in range(12):
        w_offset = math.sin(t * 3.5 + i * 0.6) * 45
        ctx.move_to(540 + w_offset * 0.5, 0)
        ctx.curve_to(
            520 + w_offset * 1.5, 250,
            580 - w_offset, 500,
            540 + w_offset * 0.8, 850
        )
        ctx.set_line_width(28 - i * 1.5)
        rgba(ctx, CYAN_WATER, 0.45 * a)
        ctx.stroke()

    # Core luminous white-blue stream
    ctx.move_to(540, 0)
    ctx.curve_to(510, 300, 570, 600, 540, 850)
    ctx.set_line_width(35)
    rgba(ctx, WHITE, 0.75 * a)
    ctx.stroke()

    # Divine water spray and glowing droplets
    for k in range(25):
        drop_x = 540 + math.sin(t * 5 + k) * (70 + k * 6)
        drop_y = (k * 40 + t * 450) % 900
        circle(ctx, drop_x, drop_y, 6 + (k % 4), hexc("#A8E6FF"), 0.8 * a)
    ctx.restore()


# -----------------------------------------------------------------------------
# SPEC: 7 Scenes with seamless audio flow (tight pauses <= 0.04s)
# -----------------------------------------------------------------------------
SPEC = [
    {
        "key": "hook",
        "text": "GANGA KA AHANKAAR?",
        "visual": "Cosmic river Ganga cascading from heaven; Lord Shiva standing serene on Himalayan summit",
        "vo": [
            ("ask", [("स्वर्ग की पावन कथा,", "SWARG KI PAWAN KATHA,")], 0.02),
            ("tell", [("जब गंगा स्वर्ग से धरती पर आ रही थीं...", "JAB GANGA SWARG SE DHARTI PAR AA RAHI THIN...")], 0.02),
            ("punch", [("तो उन्हें लगा वो महादेव को भी बहा ले जाएंगी?", "TO UNHEIN LAGA WO MAHADEV KO BHI BAHA LE JAAYENGI?")], 0.04),
        ],
    },
    {
        "key": "tapasya",
        "text": "BHAGIRATH KI TAPASYA",
        "visual": "Suryavanshi King Bhagirath performing severe tapasya standing on one foot",
        "vo": [
            ("tell", [("राजा भगीरथ ने अपने पूर्वजों के उद्धार के लिए,", "RAJA BHAGIRATH NE APNE POORVAJON KE UDDHAR KE LIYE,")], 0.02),
            ("build", [("हज़ारों साल तक घोर तपस्या की थी.", "HAZARON SAAL TAK GHOR TAPASYA KI THI.")], 0.04),
        ],
    },
    {
        "key": "veg",
        "text": "PRALAYANKARI VEG",
        "visual": "Furious raging cosmic torrent threatening to shatter the earth in two halves",
        "vo": [
            ("low", [("लेकिन गंगा का वेग इतना प्रचंड था,", "LEKIN GANGA KA VEG ITNA PRACHAND THA,")], 0.02),
            ("punch", [("कि अगर वो सीधे धरती पर गिरतीं...", "KI AGAR WO SEEDHE DHARTI PAR GIRTIN...")], 0.02),
            ("awe", [("तो पूरी पृथ्वी दो टुकड़ों में फट जाती!", "TO POORI PRITHVI DO TUKDON MEIN PHAT JAATI!")], 0.04),
        ],
    },
    {
        "key": "jata",
        "text": "MAHADEV NE KHOLI JATA",
        "visual": "Devadhidev Mahadev stepping forward, spreading his divine matted locks across the sky",
        "vo": [
            ("build", [("तब भगीरथ की पुकार पर...", "TAB BHAGIRATH KI PUKAAR PAR...")], 0.02),
            ("punch", [("देवाधिदेव महादेव आगे आए!", "DEVADHIDEV MAHADEV AAGE AAYE!")], 0.02),
            ("awe", [("और उन्होंने अपनी दिव्य जटाएं पूरे आकाश में फैला दीं!", "AUR UNHONE APNI DIVYA JATAAYEIN POORE AAKASH MEIN PHAILA DEEN!")], 0.04),
        ],
    },
    {
        "key": "qaid",
        "text": "32 DIN KA RAHASYA",
        "visual": "Furious Ganga plunging into Shiva's locks, trapped in an inescapable cosmic labyrinth",
        "vo": [
            ("fast", [("जैसे ही गंगा महादेव के शीश पर गिरीं,", "JAISE HI GANGA MAHADEV KE SHEESH PAR GIRTIN,")], 0.02),
            ("tell", [("शिव जी ने उन्हें अपनी जटाओं में समेट लिया!", "SHIV JI NE UNHEIN APNI JATAON MEIN SAMET LIYA!")], 0.02),
            ("punch", [("बत्तीस दिन तक गंगा को बाहर निकलने का एक बूँद रास्ता नहीं मिला!", "BATTEES DIN TAK GANGA KO BAHAR NIKALNE KA EK BOOND RASTA NAHI MILA!")], 0.04),
        ],
    },
    {
        "key": "sharan",
        "text": "AHANKAAR KA VINASH",
        "visual": "Humbled Ganga bowing in repentance; Shiva releasing a gentle, sanctifying stream",
        "vo": [
            ("warm", [("जब गंगा का सारा घमंड चूर-चूर हो गया...", "JAB GANGA KA SAARA GHAMAND CHOOR-CHOOR HO GAYA...")], 0.02),
            ("whisper", [("और उन्होंने क्षमा मांगी,", "AUR UNHONE KSHAMA MAANGI,")], 0.02),
            ("awe", [("तब भोलेनाथ ने एक छोटी सी पवित्र धार छोड़कर पृथ्वी को नया जीवन दिया.", "TAB BHOLENATH NE EK CHHOTI SI PAVITRA DHAAR CHHODKAR PRITHVI KO NAYA JEEVAN DIYA.")], 0.04),
        ],
    },
    {
        "key": "cta",
        "text": "HAR HAR MAHADEV",
        "visual": "Mahadev blessing Bhagirath and sacred Ganga flowing into the world; Top comment CTA",
        "vo": [
            ("tell", [("महादेव ने सिखाया कि चाहे कितनी भी शक्ति हो,", "MAHADEV NE SIKHAYA KI CHAHE KITNI BHI SHAKTI HO,")], 0.02),
            ("punch", [("अहंकार का अंत निश्चित है!", "AHANKAAR KA ANT NISHCHIT HAI!")], 0.02),
            ("cta", [("भोले के सच्चे भक्त कमेंट में लिखें—", "BHOLE KE SACCHE BHAKT COMMENT MEIN LIKHEIN—")], 0.02),
            ("punch", [("हर हर महादेव!", "HAR HAR MAHADEV!")], 0.04),
        ],
    },
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "GANGA": CYAN_WATER,
    "SWARG": GOLD_HI,
    "MAHADEV": hexc("#82C4FF"),
    "BHAGIRATH": GOLD,
    "TAPASYA": GOLD_HI,
    "PRACHAND": hexc("#FF5555"),
    "PRITHVI": hexc("#60D394"),
    "JATAAYEIN": GOLD_HI,
    "BATTEES": hexc("#FFAA48"),
    "GHAMAND": RED_GEM,
    "KSHAMA": WHITE,
    "JEEVAN": CYAN_WATER,
    "HAR": GOLD_HI,
    "COMMENT": GOLD_HI,
})


# -----------------------------------------------------------------------------
# Scene Visual Classes
# -----------------------------------------------------------------------------
class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "ganga": c("GANGA", 1.2),
            "swarg": c("SWARG", d * 0.45),
            "mahadev": c("MAHADEV", d * 0.75),
        }

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["ganga"], "whoosh"), (b["mahadev"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        himalaya_bg(ctx, t, cosmic=True)

        # Cosmic torrent from heavens
        cosmic_ganga_torrent(ctx, t, a=0.85)

        # Mahadev standing majestic and serene on Himalayan ridge
        mahadev(ctx, 540, GROUND - 10, 0.72, t, pose="stand", jata_open=False, flip=False)

        # Single sleek ribbon (Zero clutter)
        ribbon(ctx, 540, 300, "GANGA KA AHANKAAR?", RED_GEM, 1.0)


class Tapasya(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "bhagirath": c("BHAGIRATH", 1.0),
            "poorvajon": c("POORVAJON", d * 0.4),
            "tapasya": c("TAPASYA", d * 0.75),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["bhagirath"], "ghanti"), (b["tapasya"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        himalaya_bg(ctx, t, cosmic=False)

        # Golden penance aura glowing around Bhagirath
        glow(ctx, 660, 680, 260, GOLD, 0.35 + 0.1 * math.sin(t * 3))

        # Sacred Himalayan rock platform / stone altar for the Yagya Kund
        ctx.save()
        rrect(ctx, 160, GROUND - 160, 260, 160, 18)
        rgba(ctx, hexc("#221A28"))
        ctx.fill_preserve()
        rgba(ctx, hexc("#3E2D48"))
        ctx.set_line_width(4)
        ctx.stroke()
        # Top rim of rock altar
        rrect(ctx, 150, GROUND - 165, 280, 22, 6)
        rgba(ctx, hexc("#523C5E"))
        ctx.fill()
        ctx.restore()

        # Sacred sacrificial fire (Yagya Kund) raised high (completely above captions!)
        dv.yagya_kund(ctx, 290, GROUND - 165, 0.90, t)

        # Floating golden embers / sacred smoke rising from holy fire
        for i in range(12):
            ember_x = 290 + math.sin(t * 3.0 + i) * (25 + i * 4)
            ember_y = (GROUND - 180) - ((t * 80 + i * 35) % 360)
            alpha = max(0.0, 1.0 - ((GROUND - 180) - ember_y) / 360)
            circle(ctx, ember_x, ember_y, 4, hexc("#FFAA33"), alpha * 0.8)

        # King Bhagirath standing on one leg in austere penance (framed on right)
        bhagirath(ctx, 660, GROUND - 10, 0.72, t, pose="tapasya", flip=False)

        # Single sleek ribbon
        ribbon(ctx, 540, 300, "BHAGIRATH KI TAPASYA", GOLD, 1.0)


class Veg(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "veg": c("VEG", 1.0),
            "dharti": c("DHARTI", d * 0.45),
            "prithvi": c("PRITHVI", d * 0.75),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["veg"], "whoosh"), (b["prithvi"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        himalaya_bg(ctx, t, cosmic=True)

        # Violent churning cosmic flood
        cosmic_ganga_torrent(ctx, t, a=1.0)

        # Cracking earth fissure glow (prominently above captions)
        ctx.save()
        ctx.move_to(420, GROUND - 120)
        ctx.line_to(540, GROUND - 20)
        ctx.line_to(660, GROUND - 120)
        ctx.set_line_width(14)
        rgba(ctx, hexc("#FF4422"), 0.85)
        ctx.stroke()
        # Inner molten core
        line(ctx, [(430, GROUND - 115), (540, GROUND - 25), (650, GROUND - 115)], hexc("#FFE066"), 6)
        ctx.restore()

        # Bhagirath on left looking up in fear and awe
        bhagirath(ctx, 240, GROUND - 10, 0.68, t, pose="pray", flip=True)

        # Single sleek ribbon
        ribbon(ctx, 540, 300, "PRALAYANKARI VEG", hexc("#FF4444"), 1.0)


class Jata(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "pukaar": c("PUKAAR", 1.0),
            "mahadev": c("MAHADEV", d * 0.45),
            "jataayein": c("JATAAYEIN", d * 0.75),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["mahadev"], "ghanti"), (b["jataayein"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        himalaya_bg(ctx, t, cosmic=True)

        # Left: King Bhagirath praying with hands folded
        bhagirath(ctx, 230, GROUND - 10, 0.68, t, pose="pray", flip=True)

        # Center/Right: Mahadev opening his divine cosmic locks across the skies
        mahadev(ctx, 620, GROUND - 10, 0.74, t, pose="open_jata", jata_open=True, flip=False)

        # Single sleek ribbon
        ribbon(ctx, 540, 300, "MAHADEV NE KHOLI JATA", hexc("#82C4FF"), 1.0)


class Qaid(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "sheesh": c("SHEESH", 1.0),
            "samet": c("SAMET", d * 0.4),
            "battees": c("BATTEES", d * 0.7),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["sheesh"], "whoosh"), (b["battees"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        himalaya_bg(ctx, t, cosmic=True)

        # Cosmic torrent funneling into Shiva's glowing Jata
        ctx.save()
        for i in range(8):
            u = (math.sin(t * 4 + i) + 1) / 2
            circle(ctx, 540 + (i - 4) * 35, 450 - i * 35, 20 + u * 15, CYAN_WATER, 0.6)
        ctx.restore()

        # Mahadev holding the entire cosmic ocean in his serene locks
        mahadev(ctx, 540, GROUND - 10, 0.74, t, pose="stand", jata_open=True, flip=False)

        # Swirling labyrinth ring around Shiva's crown
        ctx.save()
        ctx.translate(540, GROUND - 680)
        ctx.rotate(t * 1.5)
        for r in (110, 160, 210):
            circle(ctx, 0, 0, r, CYAN_WATER, 0.3)
        ctx.restore()

        # Single sleek ribbon
        ribbon(ctx, 540, 300, "32 DIN TAK QAID!", GOLD_HI, 1.0)


class Sharan(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "ghamand": c("GHAMAND", 1.0),
            "kshama": c("KSHAMA", d * 0.45),
            "jeevan": c("JEEVAN", d * 0.75),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["kshama"], "soft_thud"), (b["jeevan"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        himalaya_bg(ctx, t, cosmic=False)

        # Gentle, pure, crystal-clear stream descending calmly from Shiva's crown
        ctx.save()
        ctx.move_to(540, GROUND - 620)
        ctx.curve_to(510, GROUND - 400, 580, GROUND - 200, 540, GROUND - 10)
        ctx.set_line_width(18)
        rgba(ctx, CYAN_WATER, 0.85)
        ctx.stroke()
        # Water ripple at ground
        for w_r in (30, 60, 90):
            circle(ctx, 540, GROUND - 10, w_r * ((t % 1.0)), CYAN_WATER, 0.5 * (1 - (t % 1.0)))
        ctx.restore()

        # Left: King Bhagirath bowing in joyful gratitude
        bhagirath(ctx, 240, GROUND - 10, 0.68, t, pose="pray", flip=True)

        # Center/Right: Mahadev giving Abhaya blessing
        mahadev(ctx, 620, GROUND - 10, 0.72, t, pose="bless", jata_open=False, flip=False)

        # Single sleek ribbon
        ribbon(ctx, 540, 300, "AHANKAAR KA VINASH", GOLD, 1.0)


class Cta(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "shakti": c("SHAKTI", 1.0),
            "ant": c("ANT", d * 0.35),
            "comment": c("COMMENT", d * 0.65),
            "har": c("HAR", d * 0.85),
        }

    def events(self, d):
        b = self.beats(d)
        return [(b["ant"], "ghanti"), (b["har"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        himalaya_bg(ctx, t, cosmic=True)

        # Celestial shower of divine petals
        dv.petals(ctx, t, n=50, seed=15, a=0.95)

        # Majestic Mahadev in full divine blessing darshan
        mahadev(ctx, 540, GROUND - 10, 0.74, t, pose="bless", jata_open=False, flip=False)

        # Single sleek ribbon
        ribbon(ctx, 540, 300, "COMMENT 'HAR HAR MAHADEV'!", RED_GEM, 1.0)


SCENE_CLASSES = {
    "hook": Hook,
    "tapasya": Tapasya,
    "veg": Veg,
    "jata": Jata,
    "qaid": Qaid,
    "sharan": Sharan,
    "cta": Cta,
}

UPLOAD = {
    "titles": [
        "Ganga Ke Ahankaar Ko Mahadev Ne Kaise Toda? 🔱 Har Har Mahadev #shorts",
        "32 Din Tak Kyun Mahadev Ki Jata Mein Qaid Rahin Ganga? 😱 #shorts",
        "Jab Swarg Se Aati Ganga Ka Ghamand Choor Hua! Shiv Leela #shorts",
        "Mahadev Ka Krodh Aur Ganga Ka Ahankaar: 32 Din Ka Rahasya #shorts",
        "Kyun Kholi Mahadev Ne Apni Divya Jataayein? Rahasya #shorts",
        "Shiv Ji Ne Kaise Bachaya Prithvi Ko Ganga Ke Veg Se? #shorts",
        "Ganga Avataran Ki Wo Sachchi Kahani Jo Koi Nahi Batata #shorts",
        "Bhole Baba Ke Aage Jab Haar Gaya Ganga Ka Veg! 🔱 #shorts",
    ],
    "thumb_text": "GANGA KA GHAMAND?",
    "queries": [
        "ganga ke ahankaar ko mahadev ne kaise toda",
        "ganga avataran shiv katha",
        "mahadev jata ganga rahasya",
    ],
    "description": """
Kyun Mahadev ne Ganga ko 32 din tak apni jataon mein qaid kar liya tha? Dekhiye Ganga Avataran aur Mahadev ki wo adbhut leela jahan 'Ahankaar' ka vinash hua!
Himalaya ke shikhar par jab Ganga ne apne veg ka ghamand kiya, tab Devadhidev Mahadev ne poori prithvi ki raksha ki.

Is pavitra katha ko poora dekhein aur comment mein 'HAR HAR MAHADEV' zaroor likhein. 🔱🚩
""",
    "tags": [
        "mahadev",
        "ganga avataran",
        "shiva jata",
        "ganga",
        "bhagirath tapasya",
        "har har mahadev",
        "sanatan katha",
        "divya rahasya",
        "shorts",
    ],
    "hashtags": [
        "#Shorts",
        "#HarHarMahadev",
        "#Mahadev",
    ],
}


def thumbnail(ctx):
    """1080x1920 cover: Cosmic torrent plunging into Mahadev's radiant jata on snow peak."""
    himalaya_bg(ctx, 0.5, cosmic=True)

    # Swirling cosmic water
    cosmic_ganga_torrent(ctx, 0.8, a=0.9)

    # Mahadev in majestic power
    mahadev(ctx, 540, GROUND - 10, 0.76, 0.5, pose="open_jata", jata_open=True, flip=False)

    # Impactful thumbnail text
    text(ctx, "GANGA KA", 540, 210, 120, GOLD_HI, font=CAPTION_FONT, bold=True, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "GHAMAND?", 540, 330, 110, hexc("#FF4444"), font=CAPTION_FONT, bold=True, stroke=(0, 0, 0), stroke_w=20)


def main() -> None:
    story = sys.modules[__name__]
    story.__name__ = "kathas.mahadev_ganga"
    engine.run(story)


if __name__ == "__main__":
    main()

