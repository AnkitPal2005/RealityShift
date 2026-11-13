"""Krishna aur Bali: Shri Krishna ko teer kyun laga? (~50-55s katha, seven scenes).

Usage (from SanatanKatha/):
  python make.py krishna_bali --preview       # preview contact sheet
  python make.py krishna_bali --kiki-export   # exports kiki_narrator and kiki_char text files
  python make.py krishna_bali --kiki-split    # cuts the downloaded voice files into lines
  python make.py krishna_bali                 # final render with music & devta characters

Rahasya:
Shri Krishna's departure from his earthly body in Prabhasa Kshetra.
The hunter Jara was the reincarnation of Vanara King Vali (Bali) from Treta Yuga,
fulfilling the divine promise given by Shri Rama, demonstrating that the law of Karma
applies equally to all, even to God himself.
"""

import math
import sys
import cairo

from core.katha import *  # noqa: F401,F403
import core.devta as dv
from core.devta import group, place, halo, smooth, ink, ell, gem, limb, hand, sheen, eye, shade

TOPIC = "KRISHNA BALI KARMA RAHASYA"
OUTPUTS = {"edge": "krishna_bali_short.mp4"}
MUSIC_BPM = 74
WHITE = (1.0, 1.0, 1.0)
RED_GEM = hexc("#D61F3A")

SOURCES = [
    "Mahabharata (Mausala Parva, Section 4): Bhagavan Krishna departs his mortal body in the forest of Prabhasa when "
    "the hunter Jara, mistaking Krishna's left foot with the lotus mark for a resting deer, shoots an iron-tipped arrow.",
    "Skanda Purana and Padma Purana: Reveal Jara the hunter is the reincarnation of the Vanara King Vali (Bali) from the "
    "Ramayana (Treta Yuga). Rama, who had struck Vali from behind a tree, granted him the boon that Vali would be the cause "
    "of Rama's departure in his next avatar as Krishna, illustrating the inexorable law of Karma.",
    "Srimad Bhagavatam (Canto 11, Chapter 30): Krishna comforts the trembling hunter Jara, blesses him, and reveals that it "
    "was all part of the supreme divine will.",
]


def title_card(ctx, main, sub, a=1.0):
    rrect(ctx, 140, 250, 800, 140, 22)
    rgba(ctx, hexc("#10152B"), 0.88 * a)
    ctx.fill_preserve()
    rgba(ctx, GOLD, 0.95 * a)
    ctx.set_line_width(3.5)
    ctx.stroke()
    text(ctx, main, 540, 302, 46, GOLD, bold=True, a=a)
    text(ctx, sub, 540, 355, 26, WHITE, a=0.92 * a)


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


def prabhas_bg(ctx, t, sunset=True):
    """Prabhasa Kshetra sacred forest background with rolling hills and divine glow."""
    if sunset:
        dv.sky(ctx, hexc("#0E162B"), hexc("#5A2338"), hexc("#C86032"), 0.58)
        glow(ctx, 540, 700, 420, hexc("#FFAA48"), 0.45)
        circle(ctx, 540, 700, 80, hexc("#FFECA8"), 0.85)
    else:
        dv.sky(ctx, hexc("#0A1224"), hexc("#1C2C4E"), hexc("#3C1E3C"), 0.58)
        glow(ctx, 540, 660, 360, hexc("#6BA4FF"), 0.3)

    # Layer 1: Distant hills
    ctx.move_to(0, 920)
    for x in range(0, W + 1, 50):
        ctx.line_to(x, 920 - 35 * math.sin(x / 240 + 0.5))
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    rgba(ctx, hexc("#281C38") if sunset else hexc("#151C33"))
    ctx.fill()

    # Layer 2: Forest silhouette
    ctx.move_to(0, 1020)
    for x in range(0, W + 1, 40):
        ctx.line_to(x, 1020 - 25 * math.sin(x / 160 + 1.8) - 15 * math.sin(x / 65))
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    rgba(ctx, hexc("#1B2E1E") if sunset else hexc("#0F201C"))
    ctx.fill()

    # Layer 3: Sacred ground
    ctx.rectangle(0, GROUND - 25, W, H)
    rgba(ctx, hexc("#142212"))
    ctx.fill()

    # Grass tufts
    for i in range(35):
        gx = rnd(i, 11) * W
        gy = GROUND - 15 + 40 * rnd(i, 12)
        c = hexc("#2A4822") if sunset else hexc("#1A321A")
        line(ctx, [(gx, gy), (gx - 5, gy - 18)], c, 3)
        line(ctx, [(gx, gy), (gx + 5, gy - 16)], c, 3)

    # Twilight sparkles
    for i in range(16):
        px = (rnd(i, 21) * W + t * 18 * (0.6 + rnd(i, 22))) % W
        py = 720 + 380 * rnd(i, 23)
        circle(ctx, px, py, 2.5 + 2 * rnd(i, 24), GOLD_HI, 0.25 + 0.2 * math.sin(t * 3 + i))


# ============================================================ CUSTOM CHARACTERS

def shri_ram(ctx, x, y, s, t, pose="bow", flip=False, a=1.0):
    """Maryada Purushottam Shri Ram: Shyamal roop, royal warrior mukut (no mor-pankh), Kodanda bow."""
    def draw():
        place(ctx, x, y, s, t, flip)
        halo(ctx, 0, -650, 175, t, c=GOLD_HI)
        skin = dv.KRISHNA_SKIN
        hair = dv.KRISHNA_HAIR
        
        # Hair behind shoulders
        for side in (-1, 1):
            smooth(ctx, [(side * 70, -700), (side * 122, -620), (side * 138, -540), (side * 128, -470), (side * 98, -480), (side * 88, -560)])
            ink(ctx, hair)
        ell(ctx, 0, -668, 116, 112)
        ink(ctx, hair)
        
        # Feet + golden anklets
        for fx in (-50, 50):
            ell(ctx, fx, -14, 44, 18)
            ink(ctx, skin)
            line(ctx, [(fx - 26, -30), (fx, -24), (fx + 26, -30)], GOLD, 7)
            
        # Saffron dhoti
        dhoti = [(-118, -345), (118, -345), (136, -200), (152, -44), (62, -32), (0, -64), (-62, -32), (-152, -44), (-136, -200)]
        smooth(ctx, dhoti)
        ink(ctx, dv.SAFFRON)
        line(ctx, [(150, -48), (62, -36), (0, -68), (-62, -36), (-150, -48)], hexc("#E8741E"), 13)
        
        # Torso
        smooth(ctx, [(-122, -500), (-60, -522), (60, -522), (122, -500), (128, -430), (100, -340), (-100, -340), (-128, -430)])
        ink(ctx, skin)
        
        # Angavastra sash across chest
        smooth(ctx, [(-128, -505), (-88, -520), (118, -372), (96, -342)], k=0.1)
        ink(ctx, hexc("#E0502A"), 5)
        
        # Kamarbandh
        rrect(ctx, -114, -366, 228, 34, 12)
        ink(ctx, GOLD, 5)
        gem(ctx, 0, -349, 9, RED_GEM)
        
        # Gold necklace
        line(ctx, [(-66, -516), (-30, -486), (0, -478), (30, -486), (66, -516)], GOLD, 8)
        gem(ctx, 0, -470, 10, RED_GEM)
        
        # Neck & Head
        rrect(ctx, -32, -566, 64, 64, 14)
        ink(ctx, skin)
        for side in (-1, 1):
            ell(ctx, side * 98, -640, 18, 28)
            ink(ctx, skin)
            circle(ctx, side * 104, -604, 13, GOLD)
        ell(ctx, 0, -640, 100, 110)
        ink(ctx, skin)
        sheen(ctx, -36, -690, 40, 26, 0.14)
        
        # Calm eyes
        for side in (-1, 1):
            eye(ctx, side * 38, -646, 25, 29, t, look=(0, 0), iris=hexc("#2A1810"), seed=2)
            line(ctx, [(side * 14, -686), (side * 38, -697), (side * 64, -688)], hair, 7)
            
        line(ctx, [(2, -640), (-6, -618), (5, -613)], shade(skin, 0.65), 4)
        ctx.move_to(-20, -594)
        ctx.curve_to(-8, -586, 8, -586, 20, -594)
        ctx.set_line_width(4)
        rgba(ctx, hexc("#B5283C"))
        ctx.stroke()
        
        # Raghuvanshi tilak (red + gold chandan)
        line(ctx, [(0, -730), (0, -684)], hexc("#E2231A"), 7)
        line(ctx, [(-6, -720), (-6, -690)], GOLD_HI, 3)
        line(ctx, [(6, -720), (6, -690)], GOLD_HI, 3)
        
        # Royal Suryavanshi Mukut (Warrior gold crown, NO peacock feather!)
        rrect(ctx, -104, -776, 208, 36, 10)
        ink(ctx, GOLD, 5)
        smooth(ctx, [(-96, -772), (-74, -840), (-40, -820), (0, -895), (40, -820), (74, -840), (96, -772)], k=0.08)
        ink(ctx, GOLD, 5)
        smooth(ctx, [(-60, -784), (-40, -805), (0, -860), (40, -805), (60, -784)], k=0.08)
        rgba(ctx, GOLD_HI, 0.7)
        ctx.fill()
        gem(ctx, 0, -825, 16, RED_GEM)
        
        # Arms: holding divine Kodanda Bow on left shoulder
        L, R = (-120, -500), (120, -500)
        limb(ctx, [L, (-190, -420), (-160, -480)], skin, 46)
        hand(ctx, -160, -480, skin, 26)
        limb(ctx, [R, (160, -420), (150, -320)], skin, 46)
        hand(ctx, 150, -320, skin, 26)
        
        # Divine Kodanda Bow
        dv.bow(ctx, -165, -840, -100, -55)
        ctx.restore()
    group(ctx, a, draw)


def jara_hunter(ctx, x, y, s, t, pose="stand", mood="calm", flip=False, a=1.0):
    """Hunter Jara: rustic forest hunter attire, quiver with arrows, hunter's bow, forest topknot."""
    def draw():
        place(ctx, x, y, s, t, flip)
        skin = dv.KARNA_SKIN
        hair = hexc("#1A100A")
        
        # Hair behind
        ell(ctx, 0, -680, 110, 110)
        ink(ctx, hair)
        
        # Legs
        for side in (-1, 1):
            limb(ctx, [(side * 52, -310), (side * 56, -160), (side * 54, -30)], skin, 46)
            ell(ctx, side * 58, -14, 40, 16)
            ink(ctx, skin)
            
        # Rustic forest dhoti (earthy brown)
        smooth(ctx, [(-120, -340), (120, -340), (130, -220), (100, -140), (0, -160), (-100, -140), (-130, -220)])
        ink(ctx, hexc("#8C4E28"))
        
        # Leather belt
        rrect(ctx, -110, -360, 220, 28, 8)
        ink(ctx, hexc("#3D1E0C"))
        circle(ctx, 0, -346, 12, GOLD)
        
        # Torso
        smooth(ctx, [(-120, -500), (-60, -520), (60, -520), (120, -500), (124, -420), (96, -340), (-96, -340), (-124, -420)])
        ink(ctx, skin)
        
        # Quiver strap
        line(ctx, [(-120, -500), (100, -340)], hexc("#3D1E0C"), 14)
        line(ctx, [(-120, -500), (100, -340)], hexc("#8C5A32"), 8)
        
        # Quiver on back with arrows
        rrect(ctx, 70, -580, 48, 220, 14)
        ink(ctx, hexc("#4A2812"))
        for k in range(3):
            line(ctx, [(82 + 12 * k, -570), (82 + 12 * k, -640)], hexc("#F5E6CC"), 5)
            ctx.move_to(82 + 12 * k, -650)
            ctx.line_to(76 + 12 * k, -635)
            ctx.line_to(88 + 12 * k, -635)
            ctx.close_path()
            rgba(ctx, hexc("#A0A0A0"))
            ctx.fill()
            
        # Head
        rrect(ctx, -30, -580, 60, 60, 12)
        ink(ctx, skin)
        ell(ctx, 0, -670, 92, 98)
        ink(ctx, skin)
        
        # Eyes & expressions
        for side in (-1, 1):
            if mood == "sad":
                eye(ctx, side * 34, -670, 20, 18, t, look=(0, 0.6), seed=3)
                line(ctx, [(side * 12, -700), (side * 34, -694), (side * 56, -686)], hair, 7)
            else:
                eye(ctx, side * 34, -670, 22, 24, t, look=(0.3, 0), seed=3)
                line(ctx, [(side * 12, -696), (side * 34, -704), (side * 56, -698)], hair, 7)
                
        if mood == "sad":
            # Tear rolling down cheek
            u = (t * 0.7) % 1
            circle(ctx, -38, -650 + 40 * u, 5, hexc("#90D0FF"), 1 - u)
            line(ctx, [(-16, -622), (0, -628), (16, -622)], hexc("#5A1E1E"), 4)
        else:
            line(ctx, [(-16, -622), (0, -616), (16, -622)], hexc("#5A1E1E"), 4)
            
        # Forest dweller headband & topknot (NO crown!)
        rrect(ctx, -85, -745, 170, 24, 6)
        ink(ctx, hexc("#A83220"))
        ell(ctx, 0, -775, 42, 34)
        ink(ctx, hair)
        
        # Arms
        L, R = (-120, -500), (120, -500)
        if pose == "namaste":
            arms = [(L, (-90, -420), (-14, -460)), (R, (90, -420), (14, -460))]
            for sh, el, hd in arms:
                limb(ctx, [sh, el, hd], skin, 44)
            smooth(ctx, [(0, -540), (22, -500), (20, -450), (0, -420), (-20, -450), (-22, -500)])
            ink(ctx, skin)
        else:
            arms = [(L, (-180, -420), (-190, -340)), (R, (170, -420), (160, -340))]
            for sh, el, hd in arms:
                limb(ctx, [sh, el, hd], skin, 44)
                hand(ctx, *hd, skin, 24)
            dv.bow(ctx, -195, -740, -100, -50)
            
        ctx.restore()
    group(ctx, a, draw)


# ============================================================ SCRIPT SPEC

SPEC = [
    {"key": "hook", "text": "KRISHNA KO TEER KYUN?",
     "visual": "Dusk forest: Shri Krishna resting under a sacred peepal tree; an arrow glows in flight; 'KRISHNA KO TEER KYUN?' ribbon",
     "vo": [("tell", [("सोचिए,", "SOCHIYE,"),
                      ("जिसने पूरी दुनिया को गीता का ज्ञान दिया,", "JISNE POORI DUNIYA KO GITA KA GYAN DIYA,"),
                      ("काल भी जिनके आगे नतमस्तक था...", "KAAL BHI JINKE AAGE NATMASTAK THA..."),
                      ("उन भगवान श्रीकृष्ण का देहावसान,", "UN BHAGAWAN SHRI KRISHNA KA DEHAWASAN,"),
                      ("एक साधारण शिकारी के तीर से", "EK SADHARAN SHIKARI KE TEER SE"),
                      ("कैसे हो गया?", "KAISE HO GAYA?")])]},

    {"key": "forest", "text": "JARA KA TEER",
     "visual": "Prabhasa forest: Hunter Jara draws his bow mistaking Krishna's lotus foot for a deer; the arrow strikes",
     "vo": [("tell", [("प्रभास के शांत वन में,", "PRABHASA KE SHAANT VAN MEIN,"),
                      ("श्रीकृष्ण पीपल के नीचे विश्राम कर रहे थे।", "SHRI KRISHNA PEEPAL KE NEECHE VISHRAM KAR RAHE THE."),
                      ("तभी 'जरा' नाम के शिकारी ने,", "TABHI JARA NAAM KE SHIKARI NE,"),
                      ("उनके चरण को हिरण समझकर...", "UNKE CHARAN KO HIRAN SAMAJHKAR..."),
                      ("दूर से तीर चला दिया!", "DOOR SE TEER CHALA DIYA!")])]},

    {"key": "guilt", "text": "SHIKARI KA PASHTAWA",
     "visual": "Jara drops his bow in horror and falls weeping at Krishna's lotus feet; tears flow",
     "vo": [("tell", [("पास आकर जब शिकारी ने देखा", "PAAS AAKAR JAB SHIKARI NE DEKHA"),
                      ("कि तीर प्रभु को लगा है,", "KI TEER PRABHU KO LAGA HAI,"),
                      ("तो वो चरणों में गिरकर", "TO WO CHARNON MEIN GIRKAR"),
                      ("फूट-फूट कर रोने लगा...", "FOOT-FOOT KAR RONE LAGA...")]),
            ("char", [("हे प्रभु!", "HEY PRABHU!"),
                      ("मुझसे ये क्या अनर्थ हो गया!", "MUJHSE YE KYA ANARTH HO GAYA!"),
                      ("मुझे क्षमा कर दीजिए प्रभु,", "MUJHE KSHAMA KAR DIJIYE PRABHU,"),
                      ("मुझे मृत्युदंड दीजिए!", "MUJHE MRITYUDAND DIJIYE!")])]},

    {"key": "reveal", "text": "MERA HI VIDHAAN HAI",
     "visual": "Shri Krishna smiles gently, radiant blue aura expands, blessing Jara with his raised hand",
     "vo": [("tell", [("भगवान श्रीकृष्ण मुस्कुराए", "BHAGAWAN SHRI KRISHNA MUSKURAYE"),
                      ("और बोले—", "AUR BOLE—"),
                      ("उठो जरा, डरो मत!", "UTHO JARA, DARO MAT!"),
                      ("ये तो मेरा ही रचा हुआ", "YE TO MERA HI RACHA HUA"),
                      ("विधान है।", "VIDHAAN HAI.")])]},

    {"key": "bali", "text": "TRETA YUG KA BADLA",
     "visual": "Flashback to Treta Yuga: Shri Rama behind a tree loosing an arrow at King Bali; Bali falls",
     "vo": [("tell", [("प्रभु ने रहस्य खोला—", "PRABHU NE RAHASYA KHOLA—"),
                      ("त्रेतायुग में जब मैं श्रीराम था,", "TRETA YUG MEIN JAB MAIN SHRI RAM THA,"),
                      ("तब मैंने सुग्रीव की रक्षा के लिए,", "TAB MAINE SUGREEVA KI RAKSHA KE LIYE,"),
                      ("पेड़ के पीछे छिपकर", "PED KE PEECHE CHHIPKAR"),
                      ("बालि को बाण मारा था!", "BALI KO BAAN MAARA THA!")])]},

    {"key": "karma", "text": "KARM KA ATAL CHAKRA",
     "visual": "Golden glowing wheel of Karma spinning; Rama's arrow transforms into Jara's arrow; cosmic balance",
     "vo": [("tell", [("मरते समय बालि ने पूछा था—", "MARTE SAMAY BALI NE POOCHHA THA—"),
                      ("प्रभु, छिपकर क्यों मारा?", "PRABHU, CHHIPKAR KYUN MARA?"),
                      ("तब श्रीराम ने वचन दिया था,", "TAB SHRI RAM NE VACHAN DIYA THA,"),
                      ("कि द्वापर में तुम शिकारी बनकर", "KI DWAPAR MEIN TUM SHIKARI BANKAR"),
                      ("पेड़ के पीछे से ही", "PED KE PEECHE SE HI"),
                      ("मेरी लीला का अंत करोगे!", "MERI LEELA KA ANT KAROGE!")])]},

    {"key": "cta", "text": "JAI SHRI KRISHNA",
     "visual": "Shri Krishna in his supreme divine roop; golden flower petals shower down; Diya glows; comment card pops",
     "vo": [("tell", [("कर्म का चक्र इतना अटल है,", "KARM KA CHAKRA ITNA ATAL HAI,"),
                      ("कि स्वयं भगवान भी इससे नहीं बचते!", "KI SWAYAM BHAGAWAN BHI ISSE NAHI BACHTE!"),
                      ("कमेंट में लिखिए", "COMMENT MEIN LIKHIYE"),
                      ("जय श्री कृष्ण!", "JAI SHRI KRISHNA!"),
                      ("और सब्सक्राइब कीजिए", "AUR SUBSCRIBE KIJIYE"),
                      ("दिव्य रहस्य!", "DIVYA RAHASYA!")])]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)

HOT = {
    "SOCHIYE,": GOLD, "GITA": GOLD, "GYAN": GOLD, "KAAL": RED_GEM, "KRISHNA": GOLD, "DEHAWASAN,": WHITE,
    "SHIKARI": GOLD, "TEER": RED_GEM, "PRABHASA": WHITE, "PEEPAL": GOLD, "JARA": GOLD, "CHARAN": GOLD,
    "HIRAN": WHITE, "PRABHU": GOLD, "ANARTH": RED_GEM, "KSHAMA": WHITE, "MRITYUDAND": RED_GEM,
    "MUSKURAYE": GOLD, "VIDHAAN": GOLD, "TRETA": GOLD, "RAM": GOLD, "BALI": GOLD, "BAAN": RED_GEM,
    "KARM": GOLD, "CHAKRA": GOLD, "ATAL": GOLD, "JAI": GOLD, "SHRI": GOLD, "KRISHNA!": GOLD,
    "DIVYA": GOLD, "RAHASYA!": GOLD, "COMMENT": GOLD
}


# ============================================================ SCENES

class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"gita": c("GITA", 1.8), "krishna": c("KRISHNA", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["gita"], "shankh"), (b["krishna"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        prabhas_bg(ctx, t, sunset=True)
        
        # Sacred Peepal tree
        dv.peepal(ctx, 840, GROUND, 0.85, t)
        
        # Krishna standing in divine serenity
        dv.krishna(ctx, 420, GROUND - 10, 0.74, t, pose="stand")
        
        # Title card
        title_card(ctx, "SHRI KRISHNA LEELA", "KRISHNA KO TEER KYUN LAGA?", 0.95)
        
        if t > b["krishna"]:
            shimmer = 0.5 + 0.5 * math.sin(t * 5)
            glow(ctx, 420, 700, 200, GOLD, 0.45 * shimmer)


class Forest(Cued):
    def beats(self, d):
        c = self.cue
        return {"jara": c("JARA", 1.8), "teer": c("TEER", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(b["jara"], "whoosh"), (b["teer"], "arrow")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        prabhas_bg(ctx, t, sunset=True)
        
        # Peepal tree behind Krishna on right
        dv.peepal(ctx, 880, GROUND, 0.82, t)
        
        # Krishna standing on right
        dv.krishna(ctx, 760, GROUND - 10, 0.72, t, pose="stand", flip=True)
        
        # Hunter Jara on left aiming bow
        jara_hunter(ctx, 240, GROUND - 10, 0.70, t, pose="stand", mood="calm")
        
        # Arrow in flight
        if t > b["teer"]:
            u = clamp((t - b["teer"]) / 0.45)
            ax = lerp(290, 720, u)
            ay = lerp(780, 1130, u)
            ang = math.atan2(1130 - 780, 720 - 290)
            dv.divine_arrow(ctx, ax, ay, ang, 120, t, a=1.0)
            circle(ctx, ax, ay, 7, RED_GEM)
            
        ribbon(ctx, 540, 320, "JARA KA TEER", RED_GEM, t - b["teer"])


class Guilt(Cued):
    def beats(self, d):
        c = self.cue
        return {"paas": c("PAAS", 1.5), "char": c("ANARTH", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["paas"], "whoosh"), (b["char"], "pop")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        prabhas_bg(ctx, t, sunset=False)
        
        # Peepal tree on right
        dv.peepal(ctx, 880, GROUND, 0.80, t)
        
        # Krishna standing compassionate
        dv.krishna(ctx, 740, GROUND - 10, 0.74, t, pose="bless", flip=True)
        
        # Hunter weeping and prostrating at feet (NO awkward crown, real tear!)
        jara_hunter(ctx, 360, GROUND - 10, 0.68, t, pose="namaste", mood="sad")
        
        # Clean ribbon instead of broken giant text bubble
        ribbon(ctx, 540, 320, "KSHAMA PRABHU!", RED_GEM, t - b["char"])
        ribbon(ctx, 540, 400, "SHIKARI KA PASHTAWA", GOLD, t - b["char"] - 0.25)


class Reveal(Cued):
    def beats(self, d):
        c = self.cue
        return {"musk": c("MUSKURAYE", 1.2), "vidhaan": c("VIDHAAN", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["musk"], "ghanti"), (b["vidhaan"], "shankh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dv.sky(ctx, hexc("#1A1238"), hexc("#3C1E64"), hexc("#5A2648"), 0.5)
        
        # Rotating golden divine rays
        ctx.save()
        ctx.translate(540, 720)
        ctx.rotate(t * 0.1)
        for k in range(16):
            ang = k / 16 * math.tau
            ctx.move_to(0, 0)
            ctx.arc(0, 0, 1200, ang - 0.04, ang + 0.04)
            ctx.close_path()
        rgba(ctx, GOLD, 0.08)
        ctx.fill()
        ctx.restore()
        
        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#1A1024"))
        ctx.fill()
        
        # Krishna centered in radiant divine glory
        glow(ctx, 540, 720, 340, GOLD, 0.75 + 0.15 * math.sin(t * 4))
        dv.krishna(ctx, 540, GROUND - 10, 0.80, t, pose="bless", smile=1.0)
        
        dv.petals(ctx, t, n=30)
        ribbon(ctx, 540, 320, "YE TO MERA HI VIDHAAN HAI", GOLD, t - b["vidhaan"])


class Bali(Cued):
    def beats(self, d):
        c = self.cue
        return {"ram": c("RAM", 1.8), "bali": c("BALI", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["ram"], "whoosh"), (b["bali"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        
        # Warm Treta Yuga nostalgic sky & forest
        dv.sky(ctx, hexc("#3B1408"), hexc("#7A3212"), hexc("#C25B1E"), 0.55)
        glow(ctx, 540, 680, 400, hexc("#FFA440"), 0.4)
        
        # Kishkindha forest hills
        ctx.move_to(0, 960)
        for x in range(0, W + 1, 50):
            ctx.line_to(x, 960 - 30 * math.sin(x / 180 + 1.2))
        ctx.line_to(W, H)
        ctx.line_to(0, H)
        ctx.close_path()
        rgba(ctx, hexc("#2A1208"))
        ctx.fill()
        
        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#1E0C06"))
        ctx.fill()
        
        # Tree in center
        dv.peepal(ctx, 500, GROUND, 0.85, t)
        
        # Shri Rama on left with Kodanda Bow
        shri_ram(ctx, 240, GROUND - 10, 0.72, t, pose="bow")
        
        # King Bali on right
        dv.barbarik(ctx, 800, GROUND - 10, 0.72, t, pose="namaste", mood="calm", flip=True)
        
        title_card(ctx, "TRETA YUGA", "SHRI RAM AUR BALI KA VACHAN", 0.95)
        
        if t > b["bali"]:
            ribbon(ctx, 540, 480, "PED KE PEECHE SE TEER", RED_GEM, t - b["bali"])


class Karma(Cued):
    def beats(self, d):
        c = self.cue
        return {"bali": c("BALI", 1.5), "leela": c("LEELA", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(b["bali"], "ghanti"), (b["leela"], "shankh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dv.sky(ctx, hexc("#0A0D22"), hexc("#161E42"), hexc("#28163C"), 0.5)
        dv.stars(ctx, t, n=60)
        
        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#0D1124"))
        ctx.fill()
        
        # Cosmic Karma wheel in sky
        cx, cy, r = 540, 480, 140
        circle(ctx, cx, cy, r + 22, GOLD, 0.4)
        circle(ctx, cx, cy, r, hexc("#141D38"), 0.92)
        
        for i in range(8):
            ang = t * 1.5 + i * (math.tau / 8)
            line(ctx, [(cx, cy), (cx + r * math.cos(ang), cy + r * math.sin(ang))], GOLD, 4, 0.8)
        circle(ctx, cx, cy, 32, hexc("#FFC83D"), 0.92)
        
        # Pure Roman text: NO tofu squares!
        text(ctx, "KARM CHAKRA", cx, cy + 8, 30, hexc("#141D38"), bold=True)
        
        # Treta Yug: Shri Rama on left (with bow, warrior mukut)
        shri_ram(ctx, 230, GROUND - 10, 0.70, t, pose="bow")
        ribbon(ctx, 230, 480, "TRETA: SHRI RAM", GOLD, 1.0)
        
        # Dwapara Yug: Shri Krishna on right (with mor-pankh, blessing)
        dv.krishna(ctx, 850, GROUND - 10, 0.70, t, pose="bless", flip=True)
        ribbon(ctx, 850, 480, "DWAPAR: KRISHNA", GOLD, 1.0)
        
        ribbon(ctx, 540, 240, "KARM KA ATAL CHAKRA", GOLD, t - b["leela"])


class Cta(Cued):
    def beats(self, d):
        c = self.cue
        return {"karm": c("KARM", 1.2), "jai": c("JAI", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["karm"], "ghanti"), (b["jai"], "shankh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dv.sky(ctx, hexc("#1A1238"), hexc("#451E52"), hexc("#702B48"), 0.5)
        
        ctx.rectangle(0, GROUND - 25, W, H)
        rgba(ctx, hexc("#1A1024"))
        ctx.fill()
        
        # Shri Krishna full glorious darshan (NO giant card covering his body!)
        glow(ctx, 540, 720, 360, GOLD, 0.8)
        dv.krishna(ctx, 540, GROUND - 10, 0.78, t, pose="bless", smile=1.0)
        
        dv.petals(ctx, t, n=36)
        dv.diya(ctx, 220, GROUND - 15, 1.1, t)
        dv.diya(ctx, 860, GROUND - 15, 1.1, t)
        
        # Clean top ribbons
        ribbon(ctx, 540, 290, "JAI SHRI KRISHNA", GOLD, t - b["jai"])
        ribbon(ctx, 540, 375, "COMMENT MEIN LIKHO", GOLD_HI, t - b["jai"] - 0.25)
        
        # Animated pointer toward comment section
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
    "forest": Forest,
    "guilt": Guilt,
    "reveal": Reveal,
    "bali": Bali,
    "karma": Karma,
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
        "Shri Krishna Ko Teer Kyun Laga? Bali Ka Badla Aur Rahasya",
        "Karm Ka Chakra: Krishna Ne Bali Ka Karz Kaise Chukaya?",
        "Shri Krishna Ki Mrityu Ka Rahasya: Shikari Kaun Tha?",
        "Shri Krishna Aur Bali: Bhagwan Bhi Karm Se Nahi Bach Sake",
        "Krishna Leela Ant: Prabhas Van Ka Adbhut Rahasya",
    ],
    "title": "Shri Krishna Ko Teer Kyun Laga? Bali Ka Badla Aur Rahasya",
    "thumb_text": "TEER KYUN?",
    "queries": ["shri krishna bali", "krishna teer rahasya", "bali ka badla"],
    "description": """Shri Krishna Ko Teer Kyun Laga? Bali Ka Badla Aur Rahasya:
Duniya ko Gita ka gyan dene wale Bhagwan Shri Krishna ko ek sadharan shikari ka teer kaise laga?
Aakhir wo shikari Jara kaun tha, aur Treta Yug ke Bali se uska kya sambandh tha?

Is katha me janiye:
• Prabhasa kshetra me Shri Krishna ka dehaant
• Shikari Jara ka pashchatap aur Shri Krishna ki kripa
• Treta Yug me Shri Ram dwara Bali vadh ka rahasya
• Bhagwan Ram ka Bali ko diya gaya antim vachan
• Karm ka atal niyam: Bhagwan bhi karm ke vidhan se upar nahi hain

Shri Krishna ki is divya leela ke liye comment me likhiye: Jai Shri Krishna!
Subscribe kijiye Divya Rahasya channel ko aisi hi prernadayak sanatan kathaon ke liye.

#Shorts #ShriKrishna #Karma
""",
    "tags": ["shri krishna", "krishna leela", "shri krishna mrityu rahasya", "bali vadh", "shikari jara",
             "karm ka niyam", "mahabharat", "ramayan", "sanatan katha", "divya rahasya"],
    "hashtags": ["#Shorts", "#ShriKrishna", "#Karma"],
}


def thumbnail(ctx):
    """1080x1920 cover: Shri Krishna under the Peepal tree with glowing aura and 'TEER KYUN?' bold header."""
    prabhas_bg(ctx, 0.5, sunset=True)
    dv.peepal(ctx, 820, GROUND, 0.85, 0.5)
    
    glow(ctx, 480, 720, 320, GOLD, 0.8)
    dv.krishna(ctx, 480, GROUND - 10, 0.82, 0.5, pose="bless")

    # Bottom vignette
    g = cairo.LinearGradient(0, 1150, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.9)
    ctx.rectangle(0, 1150, W, H - 1150)
    ctx.set_source(g)
    ctx.fill()

    # Top dark gradient for text
    g = cairo.LinearGradient(0, 0, 0, 780)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.92)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 780)
    ctx.set_source(g)
    ctx.fill()

    vignette(ctx)
    text(ctx, "TEER KYUN?", 540, 290, 170, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "SHRI KRISHNA", 540, 480, 105, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    ribbon(ctx, 540, 640, "BALI KA BADLA AUR RAHASYA", RED_GEM, 1.0)
    text(ctx, "DIVYA RAHASYA", 540, 1800, 40, GOLD, a=0.7)


def main() -> None:
    from core import upload_kit
    story = sys.modules[__name__]
    engine.make_frame = katha.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
