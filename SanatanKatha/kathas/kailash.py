"""Kailash Parvat Ka Rahasya: Aaj Tak Koi Kyun Nahi Chadh Paya? (~50-55s katha, seven scenes).

Usage (from SanatanKatha/):
  python make.py kailash --preview       # preview contact sheet
  python make.py kailash --kiki-export   # exports kiki_narrator text file
  python make.py kailash --kiki-split    # cuts the downloaded voice files into lines
  python make.py kailash                 # final render with music & devta characters

Rahasya:
Mount Everest (8,848m) has been climbed by thousands, yet Mount Kailash (6,638m), though lower,
remains completely unconquered. Trekkers experience rapid aging (hair and nails growing at 2-3x rate),
magnetic disorientation, and shifting weather. Famous mountaineer Reinhold Messner abandoned climbing it
out of sacred reverence. In Sanatan tradition, Kailash is the Axis Mundi—the cosmic center of the universe—
and the eternal divine abode of Lord Shiva.
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

TOPIC = "KAILASH PARVAT RAHASYA"
OUTPUTS = {"edge": "kailash_short.mp4"}
MUSIC_BPM = 90
WHITE = (1.0, 1.0, 1.0)
RED_GEM = hexc("#D61F3A")
ICE_CYAN = hexc("#A8E6FF")
GOLD_HI = hexc("#FFF099")

SOURCES = [
    "Skanda Purana (Maheshwara Khanda): Mount Kailash is the eternal sacred abode of Bhagavan Shiva and Mata Parvati.",
    "Mountaineering Expedition Records (1980s-2000s): Russian studies on Kailash's pyramid symmetry, rapid cellular aging, and mountaineer Reinhold Messner's refusal to climb.",
    "Puranic Cosmology: Kailash is revered as Mount Meru / Axis Mundi—the metaphysical and cosmic pillar connecting Heaven and Earth.",
]


def title_card(ctx, main, sub, a=1.0):
    rrect(ctx, 140, 240, 800, 140, 22)
    rgba(ctx, hexc("#0C142B"), 0.90 * a)
    ctx.fill_preserve()
    rgba(ctx, GOLD, 0.95 * a)
    ctx.set_line_width(3.5)
    ctx.stroke()
    text(ctx, main, 540, 292, 44, GOLD, bold=True, a=a)
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


# ============================================================ CUSTOM SCENERY & ELEMENTS

def kailash_peak(ctx, x, y, s, t, a=1.0):
    """Majestic snow-clad Mount Kailash four-sided pyramid peak with glowing summit and aura."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)

        # Cosmic halo behind peak
        glow(ctx, 0, -420, 480, hexc("#64B5F6"), 0.45)
        glow(ctx, 0, -420, 260, GOLD, 0.3)

        # Massive Pyramid mountain base
        ctx.move_to(-480, 0)
        ctx.line_to(-320, -220)
        ctx.line_to(-160, -360)
        ctx.line_to(0, -440)
        ctx.line_to(160, -360)
        ctx.line_to(320, -220)
        ctx.line_to(480, 0)
        ctx.close_path()
        rgba(ctx, hexc("#283454"), 0.96)
        ctx.fill()

        # Left shadowed rock face
        ctx.move_to(-480, 0)
        ctx.line_to(-160, -360)
        ctx.line_to(0, -440)
        ctx.line_to(0, 0)
        ctx.close_path()
        rgba(ctx, hexc("#1A2238"), 0.95)
        ctx.fill()

        # Right illuminated rock face
        ctx.move_to(0, -440)
        ctx.line_to(160, -360)
        ctx.line_to(480, 0)
        ctx.line_to(0, 0)
        ctx.close_path()
        rgba(ctx, hexc("#384870"), 0.95)
        ctx.fill()

        # Eternal Snow cap
        ctx.move_to(-180, -340)
        ctx.line_to(-90, -390)
        ctx.line_to(0, -440)
        ctx.line_to(90, -390)
        ctx.line_to(180, -340)
        ctx.line_to(110, -310)
        ctx.line_to(40, -330)
        ctx.line_to(-30, -300)
        ctx.line_to(-110, -330)
        ctx.close_path()
        rgba(ctx, hexc("#E8F4FD"), 0.98)
        ctx.fill()

        # Snow ridges running down
        for rx, w in [(-70, 16), (0, 22), (70, 18), (140, 14)]:
            line(ctx, [(rx, -330), (rx * 1.8, -120)], hexc("#D0E8FC"), w)

        # Sacred Crescent Moon & Star at summit
        circle(ctx, 160, -520, 36, hexc("#FFF9D2"), 0.95)
        circle(ctx, 175, -532, 32, hexc("#0C142B"), 1.0)

        # Golden Trishul at summit
        dv.trishul(ctx, 0, -440, 0.75, t, 1.0)

        ctx.restore()
    group(ctx, a, draw)


def cosmic_sky(ctx, t):
    """Deep indigo-violet Himalayan sky with swirling nebula and twinkling stars."""
    dv.sky(ctx, hexc("#080A1A"), hexc("#12193E"), hexc("#2D1D48"), 0.55)
    dv.stars(ctx, t, n=60)
    # Ethereal aurora / spiritual energy wave
    for i in range(3):
        ctx.move_to(0, 320 + i * 90)
        for x in range(0, W + 1, 60):
            ywav = 35 * math.sin(x / 180 + t * 0.8 + i) + 15 * math.cos(x / 90 - t * 0.5)
            ctx.line_to(x, 320 + i * 90 + ywav)
        ctx.line_to(W, 0)
        ctx.line_to(0, 0)
        ctx.close_path()
        rgba(ctx, hexc("#3878D8" if i % 2 == 0 else "#6838A8"), 0.08)
        ctx.fill()


def shiva_meditating(ctx, x, y, s, t, a=1.0):
    """Devadhidev Mahadev in serene Padmasana meditation with Rudraksha, snake and crescent."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)

        # Radiant Mahadev halo
        halo(ctx, 0, -660, 210, t, c=hexc("#82C4FF"))
        skin = hexc("#8BB8E8")   # Neelkanth pale blue
        hair = hexc("#1A1412")

        # Jata (Matted locks)
        ell(ctx, 0, -780, 85, 95)
        ink(ctx, hair)
        for side in (-1, 1):
            smooth(ctx, [(side * 40, -820), (side * 80, -760), (side * 95, -670), (side * 70, -680)])
            ink(ctx, hair)

        # Crescent moon in jata
        circle(ctx, -55, -810, 22, hexc("#FFF8D4"))
        circle(ctx, -46, -818, 19, hexc("#0B1033"))

        # Ganga stream emerging from top of jata
        ctx.move_to(0, -860)
        ctx.curve_to(30, -920, 50, -900, 35, -870)
        rgba(ctx, hexc("#C8E8FF"), 0.9)
        ctx.fill()

        # Head & Face
        ell(ctx, 0, -660, 92, 105)
        ink(ctx, skin)

        # Third eye (Trinetra) on forehead
        smooth(ctx, [(0, -725), (14, -705), (0, -685), (-14, -705)], k=0.1)
        rgba(ctx, hexc("#FFAA22"), 0.95)
        ctx.fill()
        line(ctx, [(0, -718), (0, -692)], hexc("#D02020"), 4)

        # Tripundra (three white horizontal sacred ash marks)
        for ty in (-730, -718, -706):
            line(ctx, [(-42, ty), (42, ty)], (1, 1, 1), 3.5)

        # Meditative closed eyes
        for side in (-1, 1):
            ctx.move_to(side * 22, -660)
            ctx.curve_to(side * 36, -652, side * 50, -652, side * 58, -660)
            ctx.set_line_width(4)
            rgba(ctx, hexc("#1C2A3A"))
            ctx.stroke()
            line(ctx, [(side * 18, -682), (side * 42, -688), (side * 62, -680)], hair, 6)

        # Calm smile
        ctx.move_to(-16, -616)
        ctx.curve_to(-6, -608, 6, -608, 16, -616)
        ctx.set_line_width(3.5)
        rgba(ctx, hexc("#A83248"))
        ctx.stroke()

        # Neck & Neelkanth blue throat
        rrect(ctx, -32, -580, 64, 55, 12)
        ink(ctx, skin)
        circle(ctx, 0, -555, 20, hexc("#285298"), 0.6)  # Neelkanth blue poison glow

        # Grand Trishul planted by Shiva's side
        dv.trishul(ctx, -175, -420, 1.25, t)
        # Saffron pataka / sacred banner tied to Trishul shaft fluttering
        flutter = 14 * math.sin(t * 5)
        ctx.move_to(-175, -520)
        ctx.line_to(-245 + flutter, -500)
        ctx.line_to(-225 + flutter, -465)
        ctx.line_to(-175, -490)
        ctx.close_path()
        rgba(ctx, hexc("#E8621A"), 0.95)
        ctx.fill()

        # Vasuki serpent prominently coiled around neck and chest
        ctx.move_to(-65, -570)
        ctx.curve_to(0, -520, 40, -530, 72, -565)
        ctx.set_line_width(20)
        rgba(ctx, hexc("#14321A"))
        ctx.stroke()
        ctx.move_to(-55, -545)
        ctx.curve_to(0, -505, 30, -512, 60, -545)
        ctx.set_line_width(15)
        rgba(ctx, hexc("#285E36"))
        ctx.stroke()
        # Golden scales pattern along snake body
        for sk in range(-40, 50, 18):
            circle(ctx, sk, -526 + 6 * math.sin(sk / 15), 3.5, GOLD, 0.85)

        # Raised Snake Hood (Phan) on Shiva's right shoulder
        ctx.save()
        ctx.translate(85, -595)
        ctx.rotate(0.22 + 0.05 * math.sin(t * 3))
        # Spread hood
        smooth(ctx, [(0, 0), (24, -25), (30, -62), (0, -88), (-30, -62), (-24, -25)])
        ink(ctx, hexc("#183E20"))
        # Hood inside scale glow
        smooth(ctx, [(0, -10), (16, -30), (20, -58), (0, -74), (-20, -58), (-16, -30)])
        rgba(ctx, hexc("#347842"), 0.92)
        ctx.fill()
        # Sacred golden hood gem
        gem(ctx, 0, -48, 8, GOLD_HI)
        # Glowing Ruby eyes
        circle(ctx, -11, -66, 3.8, RED_GEM)
        circle(ctx, 11, -66, 3.8, RED_GEM)
        # Flickering tongue
        t_flick = math.sin(t * 12)
        if t_flick > 0.15:
            line(ctx, [(0, -88), (0, -106)], hexc("#E02222"), 2.5)
            line(ctx, [(0, -106), (-6, -114)], hexc("#E02222"), 2)
            line(ctx, [(0, -106), (6, -114)], hexc("#E02222"), 2)
        ctx.restore()

        # Rudraksha mala
        for rk in range(9):
            rang = -0.8 + rk * 0.2
            circle(ctx, 46 * math.sin(rang), -525 + 18 * math.cos(rang), 6.5, hexc("#8B4822"))

        # Torso (broad ascetic chest)
        smooth(ctx, [(-135, -490), (-70, -515), (70, -515), (135, -490), (140, -390), (100, -290), (-100, -290), (-140, -390)])
        ink(ctx, skin)

        # Tiger skin dhoti (Vyaghrambar)
        smooth(ctx, [(-130, -300), (130, -300), (150, -130), (0, -110), (-150, -130)])
        ink(ctx, hexc("#D48828"))
        # Tiger stripes
        for sy in (-260, -210, -160):
            line(ctx, [(-110, sy), (-60, sy + 15)], hexc("#381A08"), 7)
            line(ctx, [(110, sy), (60, sy + 15)], hexc("#381A08"), 7)

        # Folded Legs in Padmasana
        ell(ctx, 0, -65, 210, 65)
        ink(ctx, skin)
        for side in (-1, 1):
            ell(ctx, side * 130, -70, 75, 45)
            ink(ctx, skin)
            circle(ctx, side * 75, -55, 18, skin)  # lotus feet

        # Arms in Dhyana Mudra (meditation lap pose)
        L, R = (-135, -490), (135, -490)
        limb(ctx, [L, (-130, -380), (-35, -280)], skin, 46)
        limb(ctx, [R, (130, -380), (35, -280)], skin, 46)
        # Hands resting in lap
        ell(ctx, 0, -270, 48, 22)
        ink(ctx, skin)

        ctx.restore()
    group(ctx, a, draw)


def nandi_bull(ctx, x, y, s, t, flip=False, a=1.0):
    """Divine Nandi Bail seated peacefully with hump, curved horns, bell garland and saddle."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        if flip:
            ctx.scale(-s, s)
        else:
            ctx.scale(s, s)

        body_col = hexc("#EAEFF5")
        shadow_col = hexc("#CBD6E2")
        dark_col = hexc("#222834")

        # Soft ground shadow under Nandi
        ell(ctx, 30, -8, 180, 32)
        rgba(ctx, (0, 0, 0), 0.35)
        ctx.fill()

        # Tail resting along hind leg
        smooth(ctx, [(-150, -100), (-180, -80), (-190, -35), (-170, -15)], k=0.1)
        ink(ctx, body_col, 10)
        # Tail tuft
        ell(ctx, -170, -14, 16, 10)
        ink(ctx, dark_col)

        # Hindquarters / Haunch
        ell(ctx, -100, -85, 90, 70)
        ink(ctx, shadow_col)
        ell(ctx, -95, -90, 85, 65)
        ink(ctx, body_col)

        # Main Body / Torso
        smooth(ctx, [(-120, -125), (0, -145), (90, -125), (110, -65), (90, -22), (-110, -22), (-140, -60)])
        ink(ctx, body_col)

        # Sacred Zebu Hump (Kukut) above front shoulders
        smooth(ctx, [(20, -145), (55, -220), (85, -220), (105, -155)], k=0.12)
        ink(ctx, body_col)
        # Hump gentle shading
        smooth(ctx, [(25, -145), (55, -215), (70, -215), (60, -145)], k=0.12)
        rgba(ctx, shadow_col, 0.5)
        ctx.fill()

        # Folded front leg
        smooth(ctx, [(70, -65), (110, -45), (125, -18), (85, -12), (60, -35)])
        ink(ctx, body_col)
        # Hoof
        rrect(ctx, 110, -20, 24, 15, 5)
        ink(ctx, dark_col)

        # Folded back leg / hoof
        rrect(ctx, -85, -18, 26, 15, 5)
        ink(ctx, dark_col)

        # Embroidered royal saddle cloth (Jhool) on back
        rrect(ctx, -60, -140, 105, 75, 10)
        ink(ctx, hexc("#B81E2E"))
        rrect(ctx, -55, -135, 95, 65, 8)
        rgba(ctx, GOLD, 0.9)
        ctx.set_line_width(3.5)
        ctx.stroke()
        # Gold bells/tassels on jhool hem
        for bx in range(-45, 45, 20):
            circle(ctx, bx, -65, 5, GOLD)

        # Neck & Dewlap (sacred throat fold)
        smooth(ctx, [(60, -135), (115, -185), (145, -155), (135, -85), (85, -75)])
        ink(ctx, body_col)
        # Dewlap folds
        ctx.move_to(105, -75)
        ctx.curve_to(125, -105, 140, -125, 130, -155)
        ctx.set_line_width(4)
        rgba(ctx, shadow_col)
        ctx.stroke()

        # Sacred Bell Necklace (Ghanti Mala)
        ctx.move_to(85, -140)
        ctx.curve_to(105, -120, 125, -110, 140, -120)
        ctx.set_line_width(8)
        rgba(ctx, hexc("#8A1820"))
        ctx.stroke()
        for gx, gy in [(90, -135), (105, -122), (120, -116), (135, -122)]:
            circle(ctx, gx, gy, 7, GOLD)
            circle(ctx, gx, gy + 7, 3, GOLD)

        # Head
        ctx.save()
        ctx.translate(145, -175)
        ctx.rotate(-0.15)
        # Head base & snout
        smooth(ctx, [(-25, -48), (35, -42), (65, -10), (60, 24), (20, 32), (-20, 18), (-35, -18)])
        ink(ctx, body_col)
        # Muzzle / Nose
        ell(ctx, 48, 10, 18, 13)
        ink(ctx, shadow_col)
        circle(ctx, 52, 12, 3.5, dark_col)  # nostril

        # Gentle devoted eye looking towards Shiva
        eye(ctx, 12, -16, 16, 12, t, look=(-0.4, -0.3), iris=hexc("#221810"), seed=1)

        # Curved Horns (Singh)
        for hx, hy, crv in [(-8, -46, -22), (14, -44, -12)]:
            ctx.move_to(hx, hy)
            ctx.curve_to(hx + crv, hy - 38, hx + crv + 10, hy - 62, hx + crv + 24, hy - 72)
            ctx.set_line_width(12)
            rgba(ctx, dark_col)
            ctx.stroke()
            # Gold horn ring
            circle(ctx, hx + crv + 21, hy - 70, 5, GOLD)

        # Soft ear
        smooth(ctx, [(-18, -28), (-44, -22), (-38, -8), (-16, -14)])
        ink(ctx, body_col)
        smooth(ctx, [(-22, -26), (-38, -20), (-34, -12), (-20, -16)])
        rgba(ctx, hexc("#FFCCD4"), 0.8)
        ctx.fill()

        # Sacred white Tilak on forehead
        line(ctx, [(2, -34), (18, -34)], (1, 1, 1), 3)
        circle(ctx, 10, -34, 3, hexc("#D02020"))

        ctx.restore()

        ctx.restore()
    group(ctx, a, draw)


# ============================================================ SCRIPT SPEC

SPEC = [
    {"key": "hook", "text": "KAILASH KOI KYUN NAHI CHADHA?",
     "visual": "Night Himalayas: Mount Kailash pyramid peak glows under crescent moon; Trishul shines; 'KAILASH KOI KYUN NAHI CHADHA?' ribbon",
     "vo": [("tell", [("माउंट एवरेस्ट पर चार हज़ार से ज़्यादा लोग चढ़ चुके हैं,", "MOUNT EVEREST PAR 4000 SE ZYADA LOG CHADH CHUKE HAIN,"),
                      ("लेकिन उससे छोटा होने पर भी...", "LEKIN USSE CHHOTA HONE PAR BHI..."),
                      ("कैलाश पर्वत पर आज तक", "KAILASH PARVAT PAR AAJ TAK"),
                      ("कोई क्यों नहीं चढ़ सका?", "KOI KYUN NAHI CHADH SAKA?")])]},

    {"key": "time", "text": "SAMAY KI GATI TEZ",
     "visual": "Whirling celestial clock & hourglass; mountain fog swirls; climbers get disoriented; nails and hair grow rapidly",
     "vo": [("tell", [("पर्वतारोही बताते हैं कि", "PARVATAROHI BATATE HAIN KI"),
                      ("कैलाश के पास जाते ही दिशाएं खो जाती हैं!", "KAILASH KE PAAS JAATE HI DISHAYEN KHO JAATI HAIN!"),
                      ("और समय इतनी तेज़ी से बीतता है,", "AUR SAMAY ITNI TEZI SE BEET-TA HAI,"),
                      ("कि नाखून और बाल यहाँ", "KI NAKHOON AUR BAAL YAHAN"),
                      ("सिर्फ़ दो दिन में बढ़ जाते हैं!", "SIRF DO DIN MEIN BADH JAATE HAIN!")])]},

    {"key": "messner", "text": "REINHOLD MESSNER KA INKAR",
     "visual": "World's greatest mountaineer Reinhold Messner stands in awe facing Kailash, bowing down his head with reverence",
     "vo": [("tell", [("महान पर्वतारोही राइनहोल्ड मेसनर को", "MAHAAN PARVATAROHI REINHOLD MESSNER KO"),
                      ("जब चढ़ने की अनुमति मिली,", "JAB CHADHNE KI ANUMATI MILI,"),
                      ("तो उन्होंने इनकार कर दिया!", "TO UNHONE INKAAR KAR DIYA!"),
                      ("और कहा— अगर हम इस पर्वत को जीतने जाएंगे,", "AUR KAHA— AGAR HUM IS PARVAT KO JEETNE JAYENGE,"),
                      ("तो अपनी ही आत्मा को हरा देंगे!", "TO APNI HI AATMA KO HARA DENGE!")])]},

    {"key": "axis", "text": "DHARTI KA KENDRA (AXIS MUNDI)",
     "visual": "Cosmic globe view: Kailash as the golden Axis Mundi radiating energy pillars connecting Heaven and Earth; AUM aura",
     "vo": [("tell", [("वैज्ञानिक भी मानते हैं कि", "VAIGYANIK BHI MAANTE HAIN KI"),
                      ("कैलाश धरती का भौगोलिक केंद्र है,", "KAILASH DHARTI KA BHAUGOLIK KENDRA HAI,"),
                      ("यानि 'एक्सिस मुंडी'!", "YAANI 'AXIS MUNDI'!"),
                      ("जहाँ से चारों ओर", "JAHAN SE CHAARON OR"),
                      ("अलौकिक चुंबकीय ऊर्जा प्रवाहित होती है!", "ALAUKIK CHUMBAKIYA OORJA PRAVAHIT HOTI HAI!")])]},

    {"key": "lakes", "text": "MANSAROVAR AUR RAKSHASTAL",
     "visual": "Dual lakes: Left serene golden-blue Lake Mansarovar (Sun); Right dark turbulent Lake Rakshastal (Moon)",
     "vo": [("tell", [("यहाँ दो रहस्यमयी झीलें हैं—", "YAHAN DO RAHASYAMAYI JHEELEN HAIN—"),
                      ("एक अमृत जैसी शांत 'मानसरोवर' (सूर्य रूप),", "EK AMRIT JAISI SHAANT MANSAROVAR (SURYA ROOP),"),
                      ("और दूसरी अशांत 'राक्षसताल',", "AUR DOOSRI ASHAANT RAKSHASTAL,"),
                      ("जो चंद्रमा का रहस्यमयी रूप है!", "JO CHANDRAMA KA RAHASYAMAYI ROOP HAI!")])]},

    {"key": "shiva", "text": "DEVADHIDEV MAHADEV KA DHAM",
     "visual": "Lord Shiva with Trishul & Nag Vasuki in serene meditation; sacred Nandi seated beside Him on Kailash",
     "vo": [("tell", [("सनातन शास्त्रों के अनुसार—", "SANATAN SHASTRAON KE ANUSAAR—"),
                      ("कैलाश कोई साधारण पर्वत नहीं,", "KAILASH KOI SADHARAN PARVAT NAHI,"),
                      ("बल्कि देवाधिदेव महादेव का", "BALKI DEVADHIDEV MAHADEV KA"),
                      ("साक्षात और शाश्वत निवास स्थान है!", "SAAKSHAAT AUR SHASHWAT NIWAS STHAAN HAI!")])]},

    {"key": "cta", "text": "HAR HAR MAHADEV",
     "visual": "Cosmic golden Shiva Lingam & glowing Trishul; sacred flowers shower down; Diya sparkles; animated comment ribbon",
     "vo": [("tell", [("जिस धाम में स्वयं शिव विराजते हों,", "JIS DHAM MEIN SWAYAM SHIV VIRAAJTE HON,"),
                      ("उसे इंसानी अहंकार कैसे छू सकता है?", "USE INSAANI AHANKAAR KAISE CHHOO SAKTA HAI?"),
                      ("कमेंट में लिखिए", "COMMENT MEIN LIKHIYE"),
                      ("हर हर महादेव!", "HAR HAR MAHADEV!"),
                      ("और सब्सक्राइब कीजिए", "AUR SUBSCRIBE KIJIYE"),
                      ("दिव्य रहस्य!", "DIVYA RAHASYA!")])]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)

HOT = {
    "EVEREST": WHITE, "KAILASH": GOLD, "PARVAT": GOLD, "CHADH": RED_GEM, "SAKA?": RED_GEM,
    "PARVATAROHI": WHITE, "DISHAYEN": GOLD, "SAMAY": GOLD_HI, "TEZI": RED_GEM, "NAKHOON": WHITE,
    "MESSNER": WHITE, "INKAAR": RED_GEM, "JEETNE": GOLD, "AATMA": GOLD_HI, "VAIGYANIK": WHITE,
    "AXIS": GOLD_HI, "MUNDI": GOLD_HI, "BHAUGOLIK": WHITE, "OORJA": GOLD, "MANSAROVAR": GOLD,
    "RAKSHASTAL": ICE_CYAN, "SURYA": GOLD, "CHANDRAMA": WHITE, "SANATAN": GOLD, "SHASTRAON": GOLD,
    "MAHADEV": GOLD_HI, "SHIV": GOLD_HI, "DHAM": GOLD, "AHANKAAR": RED_GEM, "HAR": GOLD,
    "MAHADEV!": GOLD_HI, "COMMENT": GOLD, "DIVYA": GOLD, "RAHASYA!": GOLD
}


# ============================================================ SCENES

class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"everest": c("EVEREST", 1.2), "kailash": c("KAILASH", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["everest"], "whoosh"), (b["kailash"], "shankh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        cosmic_sky(ctx, t)
        kailash_peak(ctx, 540, GROUND + 30, 0.88, t)

        title_card(ctx, "KAILASH PARVAT RAHASYA", "AAJ TAK KOI KYUN NAHI CHADHA?", 0.95)

        if t > b["kailash"]:
            ribbon(ctx, 540, 480, "KAILASH KOI KYUN NAHI CHADHA?", RED_GEM, t - b["kailash"])


class Time(Cued):
    def beats(self, d):
        c = self.cue
        return {"dishayen": c("DISHAYEN", 1.4), "samay": c("SAMAY", d * 0.5)}

    def events(self, d):
        b = self.beats(d)
        return [(b["dishayen"], "whoosh"), (b["samay"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        cosmic_sky(ctx, t)
        kailash_peak(ctx, 540, GROUND + 80, 0.72, t, a=0.5)

        # Mystical giant clock spinning fast
        ctx.save()
        ctx.translate(540, 780)
        circle(ctx, 0, 0, 180, hexc("#0A1428"), 0.85)
        circle(ctx, 0, 0, 180, GOLD, 0.9)
        ctx.set_line_width(5)
        ctx.stroke()
        for i in range(12):
            ang = i * (math.tau / 12)
            line(ctx, [(150 * math.cos(ang), 150 * math.sin(ang)), (170 * math.cos(ang), 170 * math.sin(ang))], GOLD, 4)

        # Clock hands spinning fast
        ang_sec = t * 14
        ang_min = t * 4
        line(ctx, [(0, 0), (120 * math.cos(ang_sec), 120 * math.sin(ang_sec))], hexc("#FF4444"), 4)
        line(ctx, [(0, 0), (90 * math.cos(ang_min), 90 * math.sin(ang_min))], GOLD_HI, 7)
        circle(ctx, 0, 0, 12, GOLD)
        ctx.restore()

        ribbon(ctx, 540, 360, "SAMAY KI GATI TEZ", hexc("#1E3A70"), 1.0)


class Messner(Cued):
    def beats(self, d):
        c = self.cue
        return {"messner": c("MESSNER", 1.2), "aatma": c("AATMA", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["messner"], "ghanti"), (b["aatma"], "shankh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        cosmic_sky(ctx, t)
        kailash_peak(ctx, 620, GROUND + 40, 0.82, t, a=0.75)

        # Mountaineer silhouette looking up with folded hands
        ctx.save()
        ctx.translate(260, GROUND - 10)
        ctx.scale(0.72, 0.72)
        # Body silhouette
        rrect(ctx, -60, -320, 120, 300, 24)
        rgba(ctx, hexc("#101828"), 0.95)
        ctx.fill()
        # Head tilted up
        circle(ctx, 0, -370, 48, hexc("#101828"), 0.95)
        # Mountaineer backpack
        rrect(ctx, -100, -310, 50, 160, 16)
        rgba(ctx, hexc("#1E2A40"), 0.95)
        ctx.fill()
        # Climbing staff
        line(ctx, [(80, -390), (70, 0)], hexc("#C0A060"), 8)
        ctx.restore()

        ribbon(ctx, 540, 360, "REINHOLD MESSNER KA INKAR", hexc("#5A1820"), 1.0)


class Axis(Cued):
    def beats(self, d):
        c = self.cue
        return {"axis": c("AXIS", 1.4), "oorja": c("OORJA", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["axis"], "boom"), (b["oorja"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        cosmic_sky(ctx, t)

        # Energetic Axis Mundi vertical beam of divine golden-blue light
        g = cairo.LinearGradient(440, 0, 640, 0)
        g.add_color_stop_rgba(0, 0.3, 0.7, 1.0, 0.0)
        g.add_color_stop_rgba(0.5, 1.0, 0.9, 0.4, 0.65 + 0.2 * math.sin(t * 5))
        g.add_color_stop_rgba(1, 0.3, 0.7, 1.0, 0.0)
        ctx.rectangle(420, 0, 240, H)
        ctx.set_source(g)
        ctx.fill()

        kailash_peak(ctx, 540, GROUND + 50, 0.84, t)

        # Concentric magnetic energy rings
        for r in [220, 340, 460]:
            ctx.save()
            ctx.translate(540, 820)
            ctx.scale(1.0, 0.4)
            circle(ctx, 0, 0, r + 20 * math.sin(t * 3 + r / 80), GOLD_HI, 0.4)
            ctx.set_line_width(3.5)
            ctx.stroke()
            ctx.restore()

        ribbon(ctx, 540, 360, "DHARTI KA KENDRA: AXIS MUNDI", hexc("#1A488E"), 1.0)


class Lakes(Cued):
    def beats(self, d):
        c = self.cue
        return {"mansarovar": c("MANSAROVAR", 1.3), "rakshastal": c("RAKSHASTAL", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["mansarovar"], "shimmer"), (b["rakshastal"], "whoosh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        cosmic_sky(ctx, t)
        kailash_peak(ctx, 540, 720, 0.58, t, a=0.7)

        # Ground partition
        ctx.rectangle(0, 880, W, H - 880)
        rgba(ctx, hexc("#0E1626"))
        ctx.fill()

        # Left Lake: Mansarovar (Sun, Calm, Golden)
        rrect(ctx, 60, 960, 440, 360, 28)
        rgba(ctx, hexc("#103254"), 0.92)
        ctx.fill_preserve()
        rgba(ctx, GOLD, 0.9)
        ctx.set_line_width(4)
        ctx.stroke()
        circle(ctx, 280, 1070, 45, GOLD, 0.9)
        text(ctx, "MANSAROVAR", 280, 1190, 34, GOLD_HI, bold=True)
        text(ctx, "AMRIT JAL (SURYA)", 280, 1240, 24, WHITE)

        # Right Lake: Rakshastal (Moon, Turbulent, Dark)
        rrect(ctx, 580, 960, 440, 360, 28)
        rgba(ctx, hexc("#22142E"), 0.92)
        ctx.fill_preserve()
        rgba(ctx, hexc("#8098B8"), 0.9)
        ctx.set_line_width(4)
        ctx.stroke()
        circle(ctx, 800, 1070, 45, hexc("#C0D0E8"), 0.85)
        text(ctx, "RAKSHASTAL", 800, 1190, 34, ICE_CYAN, bold=True)
        text(ctx, "VISH JAL (CHANDRA)", 800, 1240, 24, WHITE)

        ribbon(ctx, 540, 360, "MANSAROVAR AUR RAKSHASTAL", hexc("#1A385C"), 1.0)


class Shiva(Cued):
    def beats(self, d):
        c = self.cue
        return {"shastra": c("SHASTRAON", 1.2), "mahadev": c("MAHADEV", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["shastra"], "shankh"), (b["mahadev"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        cosmic_sky(ctx, t)
        kailash_peak(ctx, 540, GROUND + 90, 0.74, t, a=0.45)

        # Lord Shiva with Trishul & Nag Vasuki in serene deep meditation
        glow(ctx, 420, 850, 420, hexc("#70B5FF"), 0.5)
        shiva_meditating(ctx, 420, GROUND - 10, 0.74, t)

        # Sacred Nandi Bail seated beside Mahadev on the right facing Him
        nandi_bull(ctx, 810, GROUND - 10, 0.68, t, flip=True)

        ribbon(ctx, 540, 360, "DEVADHIDEV MAHADEV KA DHAM", hexc("#1B2A5E"), 1.0)


class Cta(Cued):
    def beats(self, d):
        c = self.cue
        return {"mahadev": c("MAHADEV!", 1.8), "comment": c("COMMENT", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["mahadev"], "shankh"), (b["comment"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        cosmic_sky(ctx, t)
        kailash_peak(ctx, 540, GROUND + 60, 0.82, t, a=0.6)

        # Golden Trishul & glowing aura in center
        glow(ctx, 540, 820, 360, GOLD, 0.7)
        dv.trishul(ctx, 540, 880, 1.2, t)

        # Floating spiritual petals & glowing diya
        for i in range(18):
            px = (rnd(i, 31) * W + t * 24 * (0.6 + rnd(i, 32))) % W
            py = 400 + 900 * rnd(i, 33)
            circle(ctx, px, py, 3 + 2.5 * rnd(i, 34), GOLD_HI, 0.4 + 0.3 * math.sin(t * 4 + i))

        # Top prompt ribbon
        ribbon(ctx, 540, 340, "COMMENT MEIN LIKHIYE:", hexc("#101828"), 1.0)
        text(ctx, "HAR HAR MAHADEV", 540, 440, 68, GOLD_HI, font=CAPTION_FONT, bold=True, stroke=(0, 0, 0), stroke_w=14)

        # Animated pointer arrow pointing towards YouTube Shorts comment button
        arrow_y = 1380 + 15 * math.sin(t * 6)
        ctx.save()
        ctx.translate(920, arrow_y)
        ctx.rotate(0.3)
        # Glowing arrow
        line(ctx, [(0, 60), (0, -40)], GOLD, 14)
        ctx.move_to(0, -65)
        ctx.line_to(-28, -25)
        ctx.line_to(28, -25)
        ctx.close_path()
        rgba(ctx, GOLD_HI)
        ctx.fill()
        ctx.restore()


SCENE_CLASSES = {
    "hook": Hook,
    "time": Time,
    "messner": Messner,
    "axis": Axis,
    "lakes": Lakes,
    "shiva": Shiva,
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
        "Kailash Parvat Ka Rahasya: Aaj Tak Koi Kyun Nahi Chadh Paya?",
        "Mount Kailash Mystery: Everest Par Hazaron Gaye, Par Kailash Par Koi Kyun Nahi?",
        "Kailash Parvat Par Samay Tez Kyun Chalta Hai? Vigyan Bhi Dang!",
        "Kailash Ka Rahasya: Reinhold Messner Ne Chadhne Se Kyun Inkar Kiya?",
        "Dharti Ka Kendra Kailash: Axis Mundi Aur Mahadev Ka Divya Dham",
    ],
    "title": "Kailash Parvat Ka Rahasya: Aaj Tak Koi Kyun Nahi Chadh Paya?",
    "thumb_text": "KOI NAHI CHADHA?",
    "queries": ["kailash parvat rahasya", "mount kailash mystery", "why no one climbed kailash"],
    "description": """Kailash Parvat Ka Rahasya: Aaj Tak Koi Kyun Nahi Chadh Paya?
Duniya ki sabse unchi choti Mount Everest (8,848m) par ab tak 4000 se zyada log chadh chuke hain...
Lekin usse 2000 meter chhota hone par bhi, Mount Kailash (6,638m) par aaj tak koi kyun nahi chadh saka?

Is katha me janiye:
• Kailash par samay ki tezi: baal aur nakhun 2 din me 2 hafte jaise badhna
• Parvat par magnetic energy aur dishaon ka bhatakna
• Vishva ke mahan parvatarohi Reinhold Messner ka saaf inkaar
• Kailash: Dharti ka cosmic center aur 'Axis Mundi'
• Mansarovar (Surya) aur Rakshastal (Chandra) jheelo ka adbhut rahasya
• Sanatan granthon me Bhagawan Shiva ka sakshaat divya adhishtan

Bhagawan Bholenath ki kripa ke liye comment me श्रद्धा se likhiye: Har Har Mahadev!
Subscribe kijiye Divya Rahasya channel ko aisi hi adbhut sanatan kathaon ke liye.

#Shorts #KailashParvat #HarHarMahadev
""",
    "tags": ["kailash parvat", "mount kailash mystery", "kailash rahasya", "shiva dham", "har har mahadev",
             "reinhold messner", "axis mundi", "mansarovar", "sanatan katha", "divya rahasya"],
    "hashtags": ["#Shorts", "#KailashParvat", "#HarHarMahadev"],
}


def thumbnail(ctx):
    """1080x1920 cover: Snow peak of Mount Kailash glowing with Lord Shiva, Trishul & Nandi Bull."""
    cosmic_sky(ctx, 0.5)
    kailash_peak(ctx, 540, 890, 0.65, 0.5)

    glow(ctx, 420, 1020, 380, hexc("#70B5FF"), 0.65)
    shiva_meditating(ctx, 420, GROUND - 10, 0.74, 0.5)
    nandi_bull(ctx, 810, GROUND - 10, 0.68, 0.5, flip=True)

    # Vignettes
    g = cairo.LinearGradient(0, 1150, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.92)
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
    text(ctx, "KOI NAHI CHADHA?", 540, 290, 130, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "KAILASH PARVAT", 540, 460, 105, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    ribbon(ctx, 540, 620, "AAJ TAK KA SABSE BADA RAHASYA", RED_GEM, 1.0)
    text(ctx, "DIVYA RAHASYA", 540, 1800, 40, GOLD, a=0.7)


def main() -> None:
    story = sys.modules[__name__]
    story.__name__ = "kathas.kailash"

    if "--check" in sys.argv:
        from core import policy
        policy.check(story, "kailash")
        print("[policy] OK - all checks passed!")
        return

    if "--preview" in sys.argv:
        import make
        make.preview("kailash")
        return

    engine.make_frame = katha.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
