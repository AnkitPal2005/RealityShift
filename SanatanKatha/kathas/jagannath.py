"""Puri Jagannath Ka Dhadakta Hriday: Brahma Padartha Ka Rahasya (~50-55s katha, seven scenes).

Usage (from SanatanKatha/):
  python make.py jagannath --preview       # preview contact sheet
  python make.py jagannath --kiki-export   # exports kiki_narrator text file
  python make.py jagannath --kiki-split    # cuts the downloaded voice files into lines
  python make.py jagannath                 # final render with music & devta characters

Rahasya:
After Bhagavan Shri Krishna's departure from his mortal frame in Prabhasa Kshetra, the Pandavas
cremated his body. The entire body dissolved into the five elements, but his divine heart remained
unburnt and alive. Following divine instructions, it was released into the Mahodadhi (sea), where it
transformed into the sacred Daru Brahma log and washed ashore at Puri. Consecrated within Lord
Jagannath's idol, this living relic is known as the 'Brahma Padartha' and is secretly transferred to new
idols during the Nabakalebara ceremony in total darkness by a blindfolded priest.
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

TOPIC = "JAGANNATH BRAHMA PADARTHA RAHASYA"
OUTPUTS = {"edge": "jagannath_short.mp4"}
MUSIC_BPM = 82
WHITE = (1.0, 1.0, 1.0)
RED_GEM = hexc("#D61F3A")

SOURCES = [
    "Skanda Purana (Utkala Khanda): Manifestation of Lord Jagannath in Puri from the sacred Daru Brahma floating in the ocean.",
    "Madala Panji (Puri Temple Chronicle): Details the ancient Nabakalebara ritual, power outages, and the blindfolded transfer of the Brahma Padartha.",
    "Odia Mahabharata (Sarala Dasa): Describes the cremation of Shri Krishna's mortal frame where the divine heart remained unburnt, living and pulsating.",
]


def title_card(ctx, main, sub, a=1.0):
    rrect(ctx, 140, 240, 800, 140, 22)
    rgba(ctx, hexc("#10152B"), 0.88 * a)
    ctx.fill_preserve()
    rgba(ctx, GOLD, 0.95 * a)
    ctx.set_line_width(3.5)
    ctx.stroke()
    text(ctx, main, 540, 292, 46, GOLD, bold=True, a=a)
    text(ctx, sub, 540, 345, 26, WHITE, a=0.92 * a)


def ribbon(ctx, x, y, msg, col, u=1.0):
    if u <= 0:
        return
    p = max(0.01, ease_out_back(clamp(u / 0.4)))
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(p, p)
    w = text_width(ctx, msg, 36) + 60
    rrect(ctx, -w / 2, -32, w, 64, 20)
    rgba(ctx, col, 0.92)
    ctx.fill_preserve()
    rgba(ctx, GOLD, 0.95)
    ctx.set_line_width(3)
    ctx.stroke()
    text(ctx, msg, 0, 10, 36, (1, 1, 1), bold=True)
    ctx.restore()


# ============================================================ CUSTOM SCENERY & CHARACTERS

def puri_shikhara(ctx, x, y, s, t, a=1.0):
    """Grand silhouette of Jagannath Temple Shikhara with Neelachakra and fluttering flag."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)

        # Temple main tower outline
        shikhara_pts = [
            (-220, 0), (-200, -320), (-170, -600), (-130, -820),
            (-80, -960), (-30, -1040), (0, -1060),
            (30, -1040), (80, -960), (130, -820),
            (170, -600), (200, -320), (220, 0)
        ]
        smooth(ctx, shikhara_pts, k=0.1)
        rgba(ctx, hexc("#1C152B"), 0.96)
        ctx.fill()

        # Horizontal ridges (rekha deula architecture)
        for h in range(-150, -950, -65):
            w = 200 * (1 + h / 1150)
            line(ctx, [(-w, h), (w, h)], hexc("#2D2244"), 4)

        # Amla & Kalasha
        ell(ctx, 0, -1080, 55, 24)
        rgba(ctx, hexc("#2D2244"))
        ctx.fill()
        circle(ctx, 0, -1115, 20, hexc("#FFC83D"))

        # Neelachakra (Divine Blue Wheel)
        circle(ctx, 0, -1160, 42, hexc("#1A488E"), 0.95)
        circle(ctx, 0, -1160, 34, hexc("#3878D8"), 0.95)
        for i in range(8):
            ang = i * (math.tau / 8)
            line(ctx, [(0, -1160), (32 * math.cos(ang), -1160 + 32 * math.sin(ang))], hexc("#FFECA8"), 3)

        # Patita Pavana Flag (fluttering saffron flag on top)
        flag_y = -1190
        flutter = 15 * math.sin(t * 6)
        ctx.move_to(0, flag_y)
        ctx.line_to(90 + flutter, flag_y - 25)
        ctx.line_to(70 + flutter, flag_y + 15)
        ctx.close_path()
        rgba(ctx, hexc("#FF6B22"), 0.95)
        ctx.fill()

        ctx.restore()
    group(ctx, a, draw)


def ocean_bg(ctx, t):
    """Puri coastal beach with night sky, ocean waves and sacred glow."""
    dv.sky(ctx, hexc("#0A0E1F"), hexc("#121C38"), hexc("#1E3252"), 0.55)
    glow(ctx, 540, 720, 400, hexc("#4880D8"), 0.35)

    # Ocean water body
    ctx.rectangle(0, 840, W, H - 840)
    rgba(ctx, hexc("#0C182B"))
    ctx.fill()

    # Rolling sea waves
    for i, (wy, col, spd) in enumerate([(860, hexc("#162C4E"), 1.2), (920, hexc("#1C3860"), 1.8), (980, hexc("#234878"), 2.4)]):
        ctx.move_to(0, wy)
        for x in range(0, W + 1, 40):
            wav = 18 * math.sin(x / 140 + t * spd + i) + 8 * math.sin(x / 60 - t * 0.8)
            ctx.line_to(x, wy + wav)
        ctx.line_to(W, H)
        ctx.line_to(0, H)
        ctx.close_path()
        rgba(ctx, col)
        ctx.fill()

    # Golden beach sand
    ctx.rectangle(0, GROUND - 15, W, H - GROUND + 15)
    rgba(ctx, hexc("#1E1710"))
    ctx.fill()
    ctx.move_to(0, GROUND - 20)
    for x in range(0, W + 1, 50):
        ctx.line_to(x, GROUND - 20 + 6 * math.sin(x / 90))
    ctx.line_to(W, GROUND + 50)
    ctx.line_to(0, GROUND + 50)
    ctx.close_path()
    rgba(ctx, hexc("#2C2216"))
    ctx.fill()


def darubrahma_log(ctx, x, y, s, t, a=1.0):
    """Sacred divine wood log (Daru Brahma) floating with cosmic blue and golden aura."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)
        bob = 14 * math.sin(t * 3.5)
        ctx.translate(0, bob)

        # Divine pulsating aura
        pulse = 0.5 + 0.5 * math.sin(t * 5)
        glow(ctx, 0, 0, 160, hexc("#40A0FF"), 0.6 * pulse)
        glow(ctx, 0, 0, 90, GOLD_HI, 0.7)

        # Log trunk
        rrect(ctx, -140, -42, 280, 84, 28)
        rgba(ctx, hexc("#3B2214"))
        ctx.fill_preserve()
        rgba(ctx, GOLD, 0.8)
        ctx.set_line_width(4)
        ctx.stroke()

        # Sacred carvings & glowing ring knots
        for kx in (-80, 0, 80):
            circle(ctx, kx, 0, 18, hexc("#FFCC44"), 0.6 + 0.3 * math.sin(t * 4 + kx))
            circle(ctx, kx, 0, 8, hexc("#FFFFFF"), 0.8)

        # Water foam splash
        for k in range(8):
            fx = -120 + k * 35 + 8 * math.sin(t * 4 + k)
            circle(ctx, fx, 44, 7, (1, 1, 1), 0.55)

        ctx.restore()
    group(ctx, a, draw)


def pulsing_heart(ctx, x, y, s, t, a=1.0):
    """Brahma Padartha: glowing divine beating heart with cosmic rings and heartbeat pulses."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        # Realistic lub-dub heartbeat cycle
        beat_phase = (t * 2.2) % 1.0
        if beat_phase < 0.15:
            scale_pulse = 1.0 + 0.22 * math.sin(beat_phase / 0.15 * math.pi)
        elif 0.20 < beat_phase < 0.35:
            scale_pulse = 1.0 + 0.14 * math.sin((beat_phase - 0.20) / 0.15 * math.pi)
        else:
            scale_pulse = 1.0

        ctx.scale(s * scale_pulse, s * scale_pulse)

        # Shockwave rings
        glow(ctx, 0, 0, 240, hexc("#FF2848"), 0.45)
        glow(ctx, 0, 0, 140, GOLD_HI, 0.75)

        for r_step in (80, 130, 180):
            circle(ctx, 0, 0, r_step, GOLD, 0.25 * (1 - (t * 1.5) % 1.0))

        # Heart geometry
        ctx.move_to(0, 45)
        ctx.curve_to(-65, -15, -95, -75, -50, -115)
        ctx.curve_to(-20, -135, 0, -100, 0, -85)
        ctx.curve_to(0, -100, 20, -135, 50, -115)
        ctx.curve_to(95, -75, 65, -15, 0, 45)
        ctx.close_path()

        rgba(ctx, hexc("#E81838"), 0.95)
        ctx.fill_preserve()
        rgba(ctx, GOLD_HI, 0.95)
        ctx.set_line_width(6)
        ctx.stroke()

        # Sacred core light
        circle(ctx, 0, -55, 26, (1, 1, 1), 0.9)
        circle(ctx, 0, -55, 42, GOLD_HI, 0.6)

        # Ecg / life pulse line underneath
        wave_pts = [(-110, 85), (-60, 85), (-35, 45), (-15, 125), (10, 55), (30, 85), (110, 85)]
        line(ctx, wave_pts, GOLD_HI, 5)

        ctx.restore()
    group(ctx, a, draw)


def blindfolded_priest(ctx, x, y, s, t, a=1.0):
    """Temple Daitapati Pujari with eyes blindfolded and hands bound in silk cloth."""
    def draw():
        place(ctx, x, y, s, t, flip=False)
        skin = dv.KARNA_SKIN
        hair = hexc("#1A1208")

        # White dhoti
        smooth(ctx, [(-110, -340), (110, -340), (120, -180), (80, -40), (0, -70), (-80, -40), (-120, -180)])
        ink(ctx, hexc("#EFEFEF"))
        line(ctx, [(80, -42), (0, -72), (-80, -42)], GOLD, 8)

        # Torso (bare chested with Janeu sacred thread)
        smooth(ctx, [(-115, -500), (-55, -520), (55, -520), (115, -500), (118, -420), (90, -340), (-90, -340), (-118, -420)])
        ink(ctx, skin)

        # Janeu (Sacred white thread running across shoulder)
        line(ctx, [(-95, -508), (65, -340)], (1, 1, 1), 4)
        line(ctx, [(-90, -508), (70, -340)], GOLD_HI, 2)

        # Head & neck
        rrect(ctx, -28, -570, 56, 56, 12)
        ink(ctx, skin)
        ell(ctx, 0, -650, 88, 96)
        ink(ctx, skin)

        # Shaved head with traditional Shikha (topknot)
        ell(ctx, 0, -740, 22, 28)
        ink(ctx, hair)

        # Blindfold cloth wrapped tightly over eyes
        rrect(ctx, -92, -675, 184, 44, 10)
        rgba(ctx, hexc("#F8F8F8"), 0.96)
        ctx.fill_preserve()
        rgba(ctx, hexc("#C0A050"))
        ctx.set_line_width(4)
        ctx.stroke()
        # Knots of blindfold
        line(ctx, [(88, -655), (125, -640)], (1, 1, 1), 7)
        line(ctx, [(88, -655), (120, -665)], (1, 1, 1), 7)

        # Calm mouth
        line(ctx, [(-15, -605), (0, -610), (15, -605)], hexc("#5A1E1E"), 4)

        # Arms holding sacred relic box covered in red silk cloth
        L, R = (-115, -500), (115, -500)
        limb(ctx, [L, (-70, -420), (-25, -440)], skin, 42)
        limb(ctx, [R, (70, -420), (25, -440)], skin, 42)

        # Sacred golden reliquary box wrapped in red silk cloth
        rrect(ctx, -65, -485, 130, 95, 16)
        rgba(ctx, hexc("#C41E3A"), 0.95)
        ctx.fill_preserve()
        rgba(ctx, GOLD, 0.95)
        ctx.set_line_width(5)
        ctx.stroke()
        # Golden lock knot
        circle(ctx, 0, -438, 14, GOLD_HI)

        ctx.restore()
    group(ctx, a, draw)


def lord_jagannath(ctx, x, y, s, t, a=1.0):
    """Lord Jagannath iconic divine roop: large lotus eyes, black wooden face, grand crown and red smile."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)
        bob = 6 * math.sin(t * 3)
        ctx.translate(0, bob)

        # Aura
        halo(ctx, 0, -620, 220, t, c=GOLD_HI)
        glow(ctx, 0, -620, 360, hexc("#FFAA30"), 0.45)

        # Divine Dark Body / Base (Pitha)
        rrect(ctx, -140, -320, 280, 310, 40)
        rgba(ctx, hexc("#12141A"))
        ctx.fill_preserve()
        rgba(ctx, GOLD, 0.9)
        ctx.set_line_width(6)
        ctx.stroke()

        # Sacred yellow and red Pitambar cloth draping
        smooth(ctx, [(-135, -310), (135, -310), (145, -120), (0, -150), (-145, -120)])
        rgba(ctx, hexc("#D8262E"), 0.92)
        ctx.fill()
        rrect(ctx, -125, -140, 250, 130, 20)
        rgba(ctx, hexc("#FDB813"), 0.95)
        ctx.fill()

        # Sacred Chest Heart Glow (Brahma Padartha hidden inside)
        pulse = 0.5 + 0.5 * math.sin(t * 5)
        glow(ctx, 0, -220, 75, GOLD_HI, 0.8 * pulse)
        circle(ctx, 0, -220, 16, hexc("#FF2848"), 0.85)

        # Horizontal Arms extending forward in blessing (iconic Jagannath pose)
        for side in (-1, 1):
            rrect(ctx, 110 if side == 1 else -240, -470, 130, 55, 20)
            rgba(ctx, hexc("#12141A"))
            ctx.fill_preserve()
            rgba(ctx, GOLD)
            ctx.set_line_width(4)
            ctx.stroke()
            # Golden bangles
            line(ctx, [(side * 140, -470), (side * 140, -415)], GOLD_HI, 8)
            # Red divine palm
            ell(ctx, side * 225, -442, 22, 28)
            rgba(ctx, hexc("#D8262E"))
            ctx.fill()

        # Sacred Black Divine Head (Round & majestic)
        circle(ctx, 0, -600, 140, hexc("#12141A"))
        circle(ctx, 0, -600, 140, GOLD, a=0.3)

        # Iconic Round Lotus Eyes (Concentric rings)
        for side in (-1, 1):
            ex = side * 62
            ey = -610
            # Red outer boundary
            circle(ctx, ex, ey, 48, hexc("#D8262E"))
            # White inner eye
            circle(ctx, ex, ey, 38, (1, 1, 1))
            # Black round pupil
            circle(ctx, ex, ey, 22, hexc("#101015"))
            # Catchlight
            circle(ctx, ex - 6, ey - 6, 6, (1, 1, 1))

        # Sacred Chandan Urdhva-Pundra Tilak on forehead
        line(ctx, [(0, -710), (0, -655)], (1, 1, 1), 16)
        line(ctx, [(0, -700), (0, -660)], hexc("#D8262E"), 8)
        circle(ctx, 0, -650, 8, GOLD_HI)

        # Radiant Red Smile
        ctx.move_to(-70, -525)
        ctx.curve_to(-35, -485, 35, -485, 70, -525)
        ctx.set_line_width(14)
        rgba(ctx, hexc("#D8262E"))
        ctx.stroke()

        # Grand Royal Mukut (Jeweled Temple Crown)
        rrect(ctx, -120, -750, 240, 42, 12)
        rgba(ctx, GOLD, 0.95)
        ctx.fill()
        crown_tier = [(-110, -745), (-80, -840), (-40, -820), (0, -910), (40, -820), (80, -840), (110, -745)]
        smooth(ctx, crown_tier, k=0.1)
        rgba(ctx, GOLD, 0.95)
        ctx.fill()
        gem(ctx, 0, -840, 18, RED_GEM)
        gem(ctx, -60, -800, 12, hexc("#1A68D8"))
        gem(ctx, 60, -800, 12, hexc("#1A68D8"))

        ctx.restore()
    group(ctx, a, draw)


# ============================================================ SCRIPT SPEC

SPEC = [
    {"key": "hook", "text": "PURI KA DHADAKTA HRIDAY",
     "visual": "Dusk twilight: Jagannath Puri temple towering against sky; pulsating golden heart aura; 'PURI KA DHADAKTA HRIDAY' ribbon",
     "vo": [("tell", [("पुरी के जगन्नाथ मंदिर का वो रहस्य,", "PURI KE JAGANNATH MANDIR KA WO RAHASYA,"),
                      ("जिसे सुनकर वैज्ञानिक भी दंग हैं!", "JISE SUNKAR VAIGYANIK BHI DANG HAIN!"),
                      ("क्या किसी काष्ठ की मूर्ति में", "KYA KISI KAASHTH KI MURTI MEIN"),
                      ("आज भी एक जीवित दिल", "AAJ BHI EK JEEVIT DIL"),
                      ("धड़क सकता है?", "DHADAK SAKTA HAI?")])]},

    {"key": "pyre", "text": "AGNI MEIN NAHI JALA HRIDAY",
     "visual": "Prabhas Kshetra sacred pyre; divine flames; Pandavas standing with folded hands; Krishna's radiant heart remains unharmed",
     "vo": [("tell", [("द्वापर के अंत में जब श्रीकृष्ण ने देह त्यागी,", "DWAPAR KE ANT MEIN JAB SHRI KRISHNA NE DEH TYAGI,"),
                      ("तो पांडवों ने अंतिम संस्कार किया।", "TO PANDAVON NE ANTIM SANSKAR KIYA."),
                      ("पूरी देह पंचतत्व में विलीन हो गई,", "POORI DEH PANCHTATTVA MEIN VILEEN HO GAYI,"),
                      ("लेकिन उनका हृदय... आग में भी", "LEKIN UNKA HRIDAY... AAG MEIN BHI"),
                      ("धड़कता रहा!", "DHADAKTA RAHA!")])]},

    {"key": "ocean", "text": "SAMUDRA MEIN DARU BRAHMA",
     "visual": "Sacred blue ocean waves; glowing sacred log (Daru Brahma) floating towards Puri coast; golden divine rays",
     "vo": [("tell", [("अग्नि देव बोले—", "AGNI DEV BOLE—"),
                      ("मैं इस परमब्रह्म को नहीं जला सकता!", "MAIN IS PARAMBRAHMA KO NAHI JALA SAKTA!"),
                      ("तब उस धड़कते हृदय को समुद्र में बहाया गया,", "TAB US DHADAKTE HRIDAY KO SAMUDRA MEIN BAHAYA GAYA,"),
                      ("जो दिव्य काष्ठ बनकर", "JO DIVYA KAASHTH BANKAR"),
                      ("पुरी के तट पर पहुंचा।", "PURI KE TAT PAR PAHHUNCHA.")])]},

    {"key": "idol", "text": "MURTI MEIN BRAHMA PADARTHA",
     "visual": "Lord Jagannath's sacred manifestation; divine heart placed into the deity's chest; cosmic aura radiates",
     "vo": [("tell", [("उसी पवित्र काष्ठ से", "USI PAVITRA KAASHTH SE"),
                      ("भगवान जगन्नाथ का विग्रह बना,", "BHAGAWAN JAGANNATH KA VIGRAH BANA,"),
                      ("और प्रभु का अमर हृदय", "AUR PRABHU KA AMAR HRIDAY"),
                      ("मूर्ति के भीतर स्थापित किया गया—", "MURTI KE BHEETAR STHAPIT KIYA GAYA—"),
                      ("जिसे ब्रह्म पदार्थ कहते हैं!", "JISE BRAHMA PADARTHA KAHTE HAIN!")])]},

    {"key": "ritual", "text": "NABAKALEBARA GUPTA VIDHI",
     "visual": "Darkened temple sanctum; temple priest with blindfolded eyes and hands wrapped in cloth transferring the relic",
     "vo": [("tell", [("जब हर बारह या उन्नीस साल में", "JAB HAR BARAH YA UNNEES SAAL MEIN"),
                      ("मूर्तियां बदली जाती हैं,", "MURTIYAN BADLI JAATI HAIN,"),
                      ("तो पूरे शहर की बिजली काट दी जाती है!", "TO POORE SHAHAR KI BIJLI KAAT DI JAATI HAI!"),
                      ("पुजारी की आंखों पर पट्टी बांधी जाती है,", "PUJARI KI AANKHON PAR PATTI BAANDHI JAATI HAI,"),
                      ("ताकि कोई इसे देख न सके!", "TAAKI KOI ISSE DEKH NA SAKE!")])]},

    {"key": "mystery", "text": "AAJ BHI DHADAKTA HAI DIL",
     "visual": "Close-up of the pulsating glowing Brahma Padartha; golden heartbeat vibrations; cosmic spiritual dust",
     "vo": [("tell", [("पुजारी बताते हैं—", "PUJARI BATATE HAIN—"),
                      ("जब हम उस ब्रह्म पदार्थ को छूते हैं,", "JAB HUM US BRAHMA PADARTHA KO CHHOOTE HAIN,"),
                      ("तो वो आज भी एक जीवित दिल की तरह", "TO WO AAJ BHI EK JEEVIT DIL KI TARAH"),
                      ("धड़कता हुआ महसूस होता है!", "DHADAKTA HUA MAHSUS HOTA HAI!")])]},

    {"key": "cta", "text": "JAI JAGANNATH",
     "visual": "Lord Jagannath in full radiant divine splendour; flower petals shower; Diyas glow; animated pointer arrow to comments",
     "vo": [("tell", [("प्रभु का वह पवित्र हृदय आज भी पुरी में जीवित है!", "PRABHU KA WAH PAVITRA HRIDAY AAJ BHI PURI MEIN JEEVIT HAI!"),
                      ("कमेंट में लिखिए", "COMMENT MEIN LIKHIYE"),
                      ("जय जगन्नाथ!", "JAI JAGANNATH!"),
                      ("और ऐसे ही दिव्य रहस्यों के लिए सब्सक्राइब कीजिए", "AUR AISE HI DIVYA RAHASYON KE LIYE SUBSCRIBE KIJIYE"),
                      ("दिव्य रहस्य!", "DIVYA RAHASYA!")])]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)

HOT = {
    "PURI": GOLD, "JAGANNATH": GOLD, "MANDIR": GOLD, "RAHASYA,": RED_GEM, "VAIGYANIK": WHITE,
    "MURTI": GOLD, "JEEVIT": GOLD_HI, "DIL": RED_GEM, "DHADAK": RED_GEM, "DWAPAR": GOLD,
    "KRISHNA": GOLD, "PANDAVON": GOLD, "PANCHTATTVA": GOLD, "HRIDAY...": RED_GEM, "AGNI": RED_GEM,
    "PARAMBRAHMA": GOLD, "SAMUDRA": WHITE, "DIVYA": GOLD, "KAASHTH": GOLD, "VIGRAH": GOLD,
    "AMAR": GOLD, "BRAHMA": GOLD_HI, "PADARTHA": GOLD_HI, "NABAKALEBARA": GOLD, "SHAHAR": WHITE,
    "PUJARI": GOLD, "AANKHON": WHITE, "PATTI": WHITE, "SHAKTI": GOLD, "PAVITRA": GOLD,
    "JAI": GOLD, "JAGANNATH!": GOLD, "COMMENT": GOLD, "DIVYA": GOLD, "RAHASYA!": GOLD
}


# ============================================================ SCENES

class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"mandir": c("MANDIR", 1.5), "dil": c("DIL", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["mandir"], "shankh"), (b["dil"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dv.sky(ctx, hexc("#0A0E22"), hexc("#1A1838"), hexc("#381830"), 0.55)
        dv.stars(ctx, t, n=45)

        # Puri temple shikhara towering on left/center
        puri_shikhara(ctx, 320, GROUND + 50, 0.76, t)

        # Pulsing divine heart on right
        pulsing_heart(ctx, 760, 680, 0.88, t)

        title_card(ctx, "JAGANNATH PURI RAHASYA", "MURTI MEIN DHADAKTA DIL?", 0.95)

        if t > b["dil"]:
            ribbon(ctx, 540, 480, "PURI KA DHADAKTA HRIDAY", RED_GEM, t - b["dil"])


class Pyre(Cued):
    def beats(self, d):
        c = self.cue
        return {"krishna": c("KRISHNA", 1.2), "hriday": c("HRIDAY", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["krishna"], "whoosh"), (b["hriday"], "shankh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dv.sky(ctx, hexc("#1E0A0A"), hexc("#4A180E"), hexc("#8C3214"), 0.55)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#180A06"))
        ctx.fill()

        # Sacred Pyre wood logs
        rrect(ctx, 340, GROUND - 110, 400, 85, 18)
        rgba(ctx, hexc("#2D160C"))
        ctx.fill()

        # Sacred leaping flames
        for k in range(9):
            fx = 380 + k * 40
            h_flame = 140 + 45 * math.sin(t * 7 + k * 1.5)
            ctx.move_to(fx - 24, GROUND - 100)
            ctx.curve_to(fx - 15, GROUND - 100 - h_flame * 0.6, fx, GROUND - 100 - h_flame, fx, GROUND - 100 - h_flame)
            ctx.curve_to(fx, GROUND - 100 - h_flame, fx + 15, GROUND - 100 - h_flame * 0.6, fx + 24, GROUND - 100)
            ctx.close_path()
            rgba(ctx, hexc("#FFA024") if k % 2 == 0 else hexc("#FF4414"), 0.82)
            ctx.fill()

        # The unharmed glowing heart floating above the flames
        pulsing_heart(ctx, 540, GROUND - 210, 0.78, t)

        # Pandava in prayer on left
        dv.barbarik(ctx, 220, GROUND - 10, 0.68, t, pose="namaste", mood="sad")

        ribbon(ctx, 540, 320, "AGNI MEIN NAHI JALA HRIDAY", RED_GEM, t - b["hriday"])


class Ocean(Cued):
    def beats(self, d):
        c = self.cue
        return {"agni": c("AGNI", 1.0), "tat": c("TAT", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["agni"], "ghanti"), (b["tat"], "whoosh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        ocean_bg(ctx, t)

        # Daru Brahma floating on the waves
        darubrahma_log(ctx, 540, 840, 1.05, t)

        # Temple distant silhouette on right
        puri_shikhara(ctx, 900, GROUND - 100, 0.45, t, a=0.6)

        ribbon(ctx, 540, 320, "SAMUDRA MEIN DARU BRAHMA", GOLD, t - b["tat"])


class Idol(Cued):
    def beats(self, d):
        c = self.cue
        return {"vigrah": c("VIGRAH", 1.4), "brahma": c("BRAHMA", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["vigrah"], "ghanti"), (b["brahma"], "shankh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dv.sky(ctx, hexc("#100C22"), hexc("#281640"), hexc("#4A1838"), 0.5)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#140A18"))
        ctx.fill()

        # Lord Jagannath centered in glorious aura
        lord_jagannath(ctx, 540, GROUND - 10, 0.78, t)

        dv.petals(ctx, t, n=28)
        ribbon(ctx, 540, 260, "MURTI MEIN BRAHMA PADARTHA", GOLD_HI, t - b["brahma"])


class Ritual(Cued):
    def beats(self, d):
        c = self.cue
        return {"shahar": c("SHAHAR", 1.8), "patti": c("PATTI", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["shahar"], "whoosh"), (b["patti"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        # Deep mysterious darkness of the inner sanctum (Garbhagriha)
        ctx.rectangle(0, 0, W, H)
        rgba(ctx, hexc("#06060C"))
        ctx.fill()

        # Sacred soft lamp aura
        glow(ctx, 540, 680, 320, hexc("#FF9A28"), 0.3)

        # Blindfolded Priest holding the sacred relic box
        blindfolded_priest(ctx, 540, GROUND - 10, 0.74, t)

        # Outlined shadows of old and new deities
        lord_jagannath(ctx, 210, GROUND - 10, 0.66, t, a=0.35)
        lord_jagannath(ctx, 870, GROUND - 10, 0.66, t, a=0.35)

        ribbon(ctx, 540, 280, "NABAKALEBARA GUPTA VIDHI", GOLD, t - b["patti"])
        ribbon(ctx, 540, 360, "AANKHON PAR PATTI, SHAHAR MEIN ANDHERA", WHITE, t - b["patti"] - 0.2)


class Mystery(Cued):
    def beats(self, d):
        c = self.cue
        return {"pujari": c("PUJARI", 1.2), "dhadak": c("DHADAK", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["pujari"], "ghanti"), (b["dhadak"], "shankh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dv.sky(ctx, hexc("#080816"), hexc("#14102A"), hexc("#241434"), 0.5)
        dv.stars(ctx, t, n=50)

        # Close-up massive pulsating heart
        pulsing_heart(ctx, 540, 700, 1.35, t)

        title_card(ctx, "DIVYA PRATYAKSHA", "HAATHON MEIN DHADAKTA DIL", 0.95)

        ribbon(ctx, 540, 460, "AAJ BHI DHADAKTA HAI DIL", RED_GEM, t - b["dhadak"])


class Cta(Cued):
    def beats(self, d):
        c = self.cue
        return {"pavitra": c("PAVITRA", 1.2), "jai": c("JAI", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["pavitra"], "ghanti"), (b["jai"], "shankh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dv.sky(ctx, hexc("#160E2A"), hexc("#3C1844"), hexc("#65203E"), 0.5)

        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#140A18"))
        ctx.fill()

        # Lord Jagannath in full supreme darshan (no character obstruction)
        glow(ctx, 540, 680, 380, GOLD, 0.8)
        lord_jagannath(ctx, 540, GROUND - 10, 0.78, t)

        dv.petals(ctx, t, n=36)
        dv.diya(ctx, 200, GROUND - 15, 1.15, t)
        dv.diya(ctx, 880, GROUND - 15, 1.15, t)

        # Clean top ribbons
        ribbon(ctx, 540, 280, "JAI JAGANNATH", GOLD, t - b["jai"])
        ribbon(ctx, 540, 365, "COMMENT MEIN LIKHO", GOLD_HI, t - b["jai"] - 0.25)

        # Animated pointer toward comment button
        if t > b["jai"] + 0.3:
            k = ease_out_cubic(clamp((t - b["jai"] - 0.3) / 0.4))
            bob = 10 * math.sin(t * 6)
            x0, y0 = 840, 950
            x1, y1 = lerp(x0, 990, k), lerp(y0, 1150, k) + bob
            line(ctx, [(x0, y0), (x1, y1)], GOLD_HI, 10)
            ang = math.atan2(y1 - y0, x1 - x0)
            ctx.move_to(x1 + 28 * math.cos(ang), y1 + 28 * math.sin(ang))
            for da in (2.4, -2.4):
                ctx.line_to(x1 + 24 * math.cos(ang + da), y1 + 24 * math.sin(ang + da))
            ctx.close_path()
            rgba(ctx, GOLD_HI)
            ctx.fill()


SCENE_CLASSES = {
    "hook": Hook,
    "pyre": Pyre,
    "ocean": Ocean,
    "idol": Idol,
    "ritual": Ritual,
    "mystery": Mystery,
    "cta": Cta,
}
STORY = sys.modules[__name__]


def write_alignment(final):
    import json
    out = [
        {
            "scene": spec["key"],
            "start": round(s["start"], 3),
            "end": round(s["start"] + s["dur"], 3),
            "voiceover": NARRATION[spec["key"]],
            "on_screen_text": spec["text"],
            "visual": spec["visual"],
            "words": [{"t": round(s["start"] + st, 3), "w": w} for st, w in s["captions"]]
        }
        for spec, s in zip(SPEC, engine.SCENES)
    ]
    path = final.with_suffix(".json")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Alignment: {path}")


# ============================================================ UPLOAD KIT

UPLOAD = {
    "titles": [
        "Puri Jagannath Ka Dhadakta Dil: Brahma Padartha Ka Rahasya",
        "Jagannath Mandir Ka Rahasya: Murti Mein Aaj Bhi Dil Dhadakta Hai?",
        "Shri Krishna Ka Hriday: Puri Jagannath Mein Kaise Pahuncha?",
        "Brahma Padartha Rahasya: Nabakalebara Mein Puri Ki Bijli Kyun Kat-ti Hai?",
        "Puri Ke Jagannath: Aakhir Murti Ke Andar Kya Chhupa Hai?",
    ],
    "title": "Puri Jagannath Ka Dhadakta Dil: Brahma Padartha Ka Rahasya",
    "thumb_text": "DHADAKTA DIL?",
    "queries": ["puri jagannath mandir rahasya", "brahma padartha", "krishna hriday jagannath"],
    "description": """Puri Jagannath Ka Dhadakta Dil: Brahma Padartha Ka Rahasya:
Duniya ke sabse bade rahasyon me se ek— Puri ke Jagannath mandir ki murtiyon ke andar aakhir aisa kya hai jo aaj bhi dhadakta hai?
Kya sach me Bhagwan Shri Krishna ka hriday agni me nahi jala aur aaj bhi Puri me sthit hai?

Is katha me janiye:
• Shri Krishna ke dehaant ke baad Pandavon dwara antim sanskar
• Agni Dev dwara pavitra hriday ko na jala paana
• Samudra me tair kar Daru Brahma ban kar Puri pahunchna
• Bhagwan Jagannath ki murti me Brahma Padartha ki sthapana
• Nabakalebara ke waqt poore shahar ki bijli katne aur aankhon par patti baandhne ka rahasya

Bhagwan Jagannath ki is divya kripa ke liye comment me श्रद्धा se likhiye: Jai Jagannath!
Subscribe kijiye Divya Rahasya channel ko aisi hi adbhut sanatan kathaon ke liye.

#Shorts #JagannathPuri #BrahmaPadartha
""",
    "tags": ["jagannath puri", "brahma padartha", "puri mandir rahasya", "shri krishna hriday", "nabakalebara",
             "jagannath katha", "sanatan katha", "divya rahasya", "odisha", "hinduism rahasya"],
    "hashtags": ["#Shorts", "#JagannathPuri", "#BrahmaPadartha"],
}


def thumbnail(ctx):
    """1080x1920 cover: Lord Jagannath divine face with glowing pulsating heart & 'DHADAKTA DIL?' header."""
    dv.sky(ctx, hexc("#0A081C"), hexc("#1C102C"), hexc("#381636"), 0.5)
    puri_shikhara(ctx, 540, 920, 0.7, 0.5, a=0.35)

    glow(ctx, 540, 980, 420, GOLD, 0.85)
    lord_jagannath(ctx, 540, GROUND - 10, 0.82, 0.5)

    # Vignettes
    g = cairo.LinearGradient(0, 1150, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.9)
    ctx.rectangle(0, 1150, W, H - 1150)
    ctx.set_source(g)
    ctx.fill()

    g = cairo.LinearGradient(0, 0, 0, 780)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.94)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 780)
    ctx.set_source(g)
    ctx.fill()

    vignette(ctx)
    text(ctx, "DHADAKTA DIL?", 540, 290, 150, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "JAGANNATH PURI", 540, 470, 96, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    ribbon(ctx, 540, 620, "BRAHMA PADARTHA KA RAHASYA", RED_GEM, 1.0)
    text(ctx, "DIVYA RAHASYA", 540, 1800, 40, GOLD, a=0.7)


def main() -> None:
    story = sys.modules[__name__]
    story.__name__ = "kathas.jagannath"

    if "--check" in sys.argv:
        from core import policy
        policy.check(story, "jagannath")
        print("[policy] OK - all checks passed!")
        return

    if "--preview" in sys.argv:
        import make
        make.preview("jagannath")
        return

    engine.make_frame = katha.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()

