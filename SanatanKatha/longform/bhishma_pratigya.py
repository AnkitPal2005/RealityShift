"""Divya Rahasya long-form (16:9, ~6 min): Bhishma Pitamah Ki Pratigya Aur 58 Din Ka Rahasya.

Story arc (mystery first 45 s per studio rules; Krishna present in every chapter):
  1. hook       - Kurukshetra Day 10: Bhishma on the bed of arrows, refusing to die for 58 days; Krishna smiles
  2. pratigya   - Clue 1 (Adi Parva): Devavrata's terrible vow for Satyavati & Shantanu's boon of Iccha-Mrityu
  3. amba       - Clue 2 (Udyoga Parva): Amba's tapasya & rebirth as Shikhandi; why Bhishma dropped his bow
  4. chakra     - Day 9 Kurukshetra: Bhishma's vow forces unarmed Krishna to lift a chariot wheel
  5. shaiya     - Day 10 & Baan Ki Shaiya + Arjun's arrow piercing the earth for Ganga water
  6. uttarayan  - Makar Sankranti / Uttarayan, Vishnu Sahasranama before Shri Krishna, moksha & ask

    python make_long.py bhishma_pratigya --kiki-export | --preview | (render)
"""

import math
import cairo

import core.devta as dv
from core.devta import ell, ink, limb, smooth, eye, group, place, halo  # noqa: F401
from core.engine import circle, clamp, ease_out_cubic, glow, hexc, lerp, line, rgba, rrect, text  # noqa: F401
from core.longform import H, W
from longform import arjun_rath_katha as ark
from longform.arjun_rath_katha import (
    BLUE_GLOW, C, FIRE_O, FIRE_R, GOLD, GOLD_HI, GROUND, L, R, SAFF, WHITE,
    bg_dusk, bg_night, bg_cosmos, line_,
)
from kathas import arjun_rath as ar

TITLE = "भीष्म पितामह बाणों की शय्या पर 58 दिन क्यों रुके रहे?"
CHROME = False
MUSIC_STYLE = "divine"
MUSIC_BPM = 78
MUSIC_SEED = 2711
MUSIC_LO, MUSIC_HI = 0.07, 0.16
KIKI_TEMPO = 1.0

HOT = {
    "BHISHMA": GOLD_HI, "KRISHNA": GOLD_HI, "ARJUN": GOLD_HI, "58": GOLD_HI, "DIN": GOLD_HI,
    "SHIKHANDI": SAFF, "PRATIGYA": GOLD_HI, "GANGA": BLUE_GLOW, "CHAKRA": FIRE_O,
    "SHAIYA": FIRE_O, "UTTARAYAN": GOLD_HI, "VISHNU": GOLD_HI, "JAI": SAFF, "SHRI": SAFF,
}


# ============================================================ Custom Bhishma & Baan-Shaiya visuals
def bhishma_char(ctx, x, y, s, t, pose="stand", flip=False):
    """Dignified white-bearded Kuru patriarch in silver-white armour & gold sash."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(-s if flip else s, s)
        # Feet & lower robe
        for lx in (-42, 42):
            rrect(ctx, lx - 22, -26, 44, 24, 10)
            ink(ctx, hexc("#D8D0B8"), 4)
        smooth(ctx, [(-95, -20), (-75, -310), (75, -310), (95, -20)], k=0.15)
        ink(ctx, hexc("#F2EFE6"), 5)
        # Torso armour
        smooth(ctx, [(-85, -305), (-105, -520), (105, -520), (85, -305)], k=0.2)
        ink(ctx, hexc("#D8DCE4"), 5)
        # Gold sash
        line(ctx, [(-80, -505), (75, -320)], GOLD, 18)
        # Arms
        if pose == "bow":
            limb(ctx, [(-92, -495), (-170, -470), (-220, -455)], hexc("#E2B892"), 28)
            limb(ctx, [(92, -495), (30, -460), (-40, -455)], hexc("#E2B892"), 28)
            ctx.save()
            ctx.translate(-210, -455)
            ctx.arc(0, 0, 145, 1.9, 4.4)
            rgba(ctx, GOLD)
            ctx.set_line_width(12)
            ctx.stroke()
            ctx.restore()
        elif pose == "namaste":
            limb(ctx, [(-85, -490), (-55, -410), (-10, -420)], hexc("#E2B892"), 26)
            limb(ctx, [(85, -490), (55, -410), (10, -420)], hexc("#E2B892"), 26)
        else:
            limb(ctx, [(-92, -495), (-115, -390), (-105, -290)], hexc("#E2B892"), 28)
            limb(ctx, [(92, -495), (115, -390), (105, -290)], hexc("#E2B892"), 28)
        # Head + white hair + long white beard + crown
        circle(ctx, 0, -595, 68, hexc("#E2B892"))
        ink(ctx, hexc("#E2B892"), 4)
        smooth(ctx, [(-68, -610), (0, -675), (68, -610)], k=0.3)
        rgba(ctx, WHITE)
        ctx.fill()
        # Crown
        smooth(ctx, [(-52, -645), (-32, -720), (0, -745), (32, -720), (52, -645)], k=0.1)
        ink(ctx, GOLD, 4)
        # White beard
        smooth(ctx, [(-48, -565), (0, -455), (48, -565)], k=0.35)
        rgba(ctx, WHITE)
        ctx.fill()
        eye(ctx, -22, -595, 9, 11, t)
        eye(ctx, 22, -595, 9, 11, t)
        line(ctx, [(0, -630), (0, -605)], SAFF, 6)
        ctx.restore()
    dv.group(ctx, 1.0, draw)


def baan_shaiya(ctx, x, y, s, t):
    """Bhishma resting peacefully on a bed of golden-tipped arrows."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    # Arrow bed supports
    for ax in range(-220, 230, 36):
        line(ctx, [(ax, 0), (ax + 12, -165)], hexc("#C8A860"), 6)
        circle(ctx, ax + 12, -168, 5, GOLD_HI)
    # Reclining body
    rrect(ctx, -230, -210, 360, 78, 32)
    ink(ctx, hexc("#ECEAE2"), 4)
    # Head resting on arrow pillow
    circle(ctx, 165, -215, 52, hexc("#E2B892"))
    ink(ctx, hexc("#E2B892"), 4)
    smooth(ctx, [(125, -235), (165, -275), (210, -230)], k=0.3)
    rgba(ctx, WHITE)
    ctx.fill()
    smooth(ctx, [(125, -190), (75, -175), (130, -165)], k=0.3)
    rgba(ctx, WHITE)
    ctx.fill()
    glow(ctx, 0, -190, 280, GOLD_HI, 0.25 + 0.08 * math.sin(t * 2))
    ctx.restore()


def stage_bhishma(ctx, S, bg="dusk", cast=(), rath_kw=None, fx=(), zoom=None):
    bg_map = "yamuna" if bg == "dawn" else bg
    base_cast = [c for c in cast if c.get("who") not in ("bhishma", "shaiya")]
    ark.stage(ctx, S, bg=bg_map, cast=base_cast, rath_kw=rath_kw, fx=fx, zoom=zoom)
    for item in cast:
        who = item.get("who")
        if who == "bhishma":
            bhishma_char(ctx, item["x"], GROUND, item.get("s", 0.58), S.T,
                         pose=item.get("pose", "stand"), flip=item.get("flip", False))
        elif who == "shaiya":
            baan_shaiya(ctx, item["x"], GROUND, item.get("s", 0.92), S.T)


def sc(bg="dusk", cast=(), rath=None, fx=(), zoom=None):
    return stage_bhishma, dict(bg=bg, cast=list(cast), rath_kw=rath, fx=list(fx), zoom=zoom)


def B(x, pose="stand", **kw):
    return dict(who="bhishma", x=x, pose=pose, **kw)


def SH(x, **kw):
    return dict(who="shaiya", x=x, **kw)


# ============================================================ Chapters (~6 min total)
CHAPTERS = [
    {"key": "hook", "title": "58 DIN KA RAHASYA", "lines": [
        line_("कुरुक्षेत्र के दसवें दिन महाभारत का सबसे बड़ा योद्धा धरती पर गिर पड़ा।",
              "KURUKSHETRA KE 10VEIN DIN MAHABHARAT KA SABSE BADA YODDHA DHARTI PAR GIR PADA",
              sc("dusk", cast=[SH(780, s=0.9), C("krishna", 1360, "stand")], fx=[("arrows", 200, 300, 780, 780, 7, FIRE_O)])),
        line_("पूरा शरीर बाणों से बिंधा था और नीचे थी सिर्फ बाणों की शय्या।",
              "POORA SHAREER BAANON SE BINDHA THA AUR NEECHE THI SIRF BAANON KI SHAIYA",
              sc("dusk", cast=[SH(860, s=0.95), C("arjun", 380, "namaste")], zoom=(1.0, 1.15, 860, 780))),
        line_("पांडव और कौरव दोनों हैरान थे कि पितामह ने प्राण क्यों नहीं छोड़े।",
              "PANDAV AUR KAURAV DONO HAIRAAN THE KI PITAMAH NE PRAAN KYUN NAHIN CHHODE",
              sc("dusk", cast=[SH(820, s=0.9), C("krishna", 1420, "bless"), C("arjun", 320, "bow")])),
        line_("एक दो दिन नहीं बल्कि पूरे अट्ठावन दिन तक भीष्म बाणों पर लेटे रहे।",
              "EK DO DIN NAHIN BALKI POORE 58 DIN TAK BHISHMA BAANON PAR LETE RAHE",
              sc("night", cast=[SH(840, s=0.95), C("krishna", 1400, "bless")], fx=[("glow", 840, 760, 380, GOLD_HI)])),
        line_("आखिर ऐसा कौन सा वरदान था और क्यों उन्होंने शिखंडी के आगे धनुष रख दिया।",
              "AAKHIR AISA KAUN SA VARDAAN THA AUR KYUN UNHONE SHIKHANDI KE AAGE DHANUSH RAKH DIYA",
              sc("night", cast=[B(620, "bow"), C("dkrishna", 1340, "bless", s=0.6)], fx=[("glow", 1340, 560, 360, GOLD_HI)])),
        line_("चलिए महाभारत के इस सबसे बड़े रहस्य को शुरू से समझते हैं।",
              "CHALIYE MAHABHARAT KE IS SABSE BADE RAHASYA KO SHURU SE SAMAJHTE HAIN",
              sc("dusk", cast=[B(640, "stand"), C("krishna", 1280, "flute")])),
    ]},
    {"key": "pratigya", "title": "BHISHMA PRATIGYA", "lines": [
        line_("इस कहानी की जड़ महाभारत के आदि पर्व में है जब उनका नाम देवव्रत था।",
              "IS KAHANI KI JAD MAHABHARAT KE AADI PARVA MEIN HAI JAB UNKA NAAM DEVAVRAT THA",
              sc("dawn", cast=[B(680, "stand"), C("dkrishna", 1350, "bless", s=0.55)], fx=[("glow", 1350, 560, 260, GOLD_HI)])),
        line_("राजा शांतनु सत्यवती से विवाह करना चाहते थे पर एक शर्त ने उन्हें चुप कर दिया।",
              "RAJA SHANTANU SATYAVATI SE VIVAAH KARNA CHAHTE THE PAR EK SHART NE UNHEIN CHUP KAR DIYA",
              sc("dawn", cast=[C("duryodhan", 520, "stand"), B(1260, "stand", flip=True)])),
        line_("सत्यवती के पिता चाहते थे कि राजगद्दी सिर्फ उनकी बेटी के पुत्र को मिले।",
              "SATYAVATI KE PITA CHAHTE THE KI RAJGADDI SIRF UNKI BETI KE PUTRA KO MILE",
              sc("dawn", cast=[B(960, "stand")], fx=[("glow", 960, 560, 320, GOLD_HI)])),
        line_("जब देवव्रत को ये पता चला तो उन्होंने भरी सभा में दो भीषण प्रतिज्ञाएं लीं।",
              "JAB DEVAVRAT KO YEH PATA CHALA TOH UNHONE BHARI SABHA MEIN DO BHISHAN PRATIGYAAN LEEN",
              sc("dusk", cast=[B(760, "namaste"), C("dkrishna", 1360, "stand", s=0.55)], zoom=(1.0, 1.15, 760, 580))),
        line_("पहली कि मैं कभी राजा नहीं बनूंगा और दूसरी कि मैं आजीवन विवाह नहीं करूंगा।",
              "PEHLI KI MAIN KABHI RAJA NAHIN BANOONGA AUR DOOSRI KI MAIN AAJEEVAN VIVAAH NAHIN KAROONGA",
              sc("dusk", cast=[B(760, "stand")], fx=[("glow", 760, 560, 420, GOLD_HI), ("flowers",)])),
        line_("इस अटल त्याग से प्रसन्न होकर पिता शांतनु ने उन्हें इच्छा मृत्यु का वरदान दिया।",
              "IS ATAL TYAAG SE PRASANN HOKAR PITA SHANTANU NE UNHEIN ICCHA MRITYU KA VARDAAN DIYA",
              sc("cosmos", cast=[B(720, "namaste"), C("dkrishna", 1300, "bless", s=0.6)], fx=[("cosmic", 1300, 600)])),
    ]},
    {"key": "amba", "title": "AMBA AUR SHIKHANDI", "lines": [
        line_("लेकिन कुरुक्षेत्र में उनका पतन एक पुराने वचन के कारण हुआ।",
              "LEKIN KURUKSHETRA MEIN UNKA PATAN EK PURANE VACHAN KE KAARAN HUA",
              sc("night", cast=[B(740, "bow"), C("krishna", 1340, "stand", s=0.58)])),
        line_("काशी की राजकुमारी अंबा ने भीष्म से बदला लेने के लिए घोर तपस्या की थी।",
              "KASHI KI RAJKUMARI AMBA NE BHISHMA SE BADLA LENE KE LIYE GHOR TAPASYA KI THI",
              sc("night", cast=[C("hanuman", 540, "namaste", s=0.55), C("dkrishna", 1340, "bless", s=0.55)], fx=[("glow", 540, 600, 320, SAFF)])),
        line_("अगले जन्म में वही अंबा राजा द्रुपद के घर शिखंडी के रूप में जन्मी।",
              "AGLE JANM MEIN WAHI AMBA RAJA DRUPAD KE GHAR SHIKHANDI KE ROOP MEIN JANMI",
              sc("dusk", cast=[C("arjun", 540, "stand"), C("krishna", 1300, "stand")])),
        line_("और भीष्म ने प्रण लिया था कि वो शिखंडी पर कभी शस्त्र नहीं उठाएंगे।",
              "AUR BHISHMA NE PRAN LIYA THA KI WO SHIKHANDI PAR KABHI SHASTRA NAHIN UTHAAYENGE",
              sc("dusk", cast=[B(680, "stand"), C("krishna", 1320, "bless")])),
    ]},
    {"key": "chakra", "title": "KRISHNA KA CHAKRA", "lines": [
        line_("युद्ध के नौवें दिन भीष्म ने पांडव सेना में हाहाकार मचा दिया।",
              "YUDDH KE 9VEIN DIN BHISHMA NE PANDAV SENA MEIN HAAHAAKAAR MACHA DIYA",
              sc("dusk", cast=[B(620, "bow"), C("arjun", 1320, "bow", flip=True)], fx=[("arrows", 660, 460, 1300, 560, 6, FIRE_O)])),
        line_("श्री कृष्ण ने प्रतिज्ञा ली थी कि वो युद्ध में कोई शस्त्र नहीं उठाएंगे।",
              "SHRI KRISHNA NE PRATIGYA LI THI KI WO YUDDH MEIN KOI SHASTRA NAHIN UTHAAYENGE",
              sc("dusk", rath=dict(krishna="reins", arjun="bow", x=800))),
        line_("पर अपने भक्त की लाज बचाने के लिए कृष्ण रथ का टूटा पहिया लेकर दौड़ पड़े।",
              "PAR APNE BHAKT KI LAAJ BACHANE KE LIYE KRISHNA RATH KA TOOTA PAHIYA LEKAR DAUD PADE",
              sc("dusk", cast=[C("krishna", 1180, "command"), B(560, "namaste")], fx=[("glow", 1180, 540, 440, GOLD_HI)])),
        line_("ये देखकर भीष्म ने धनुष रख दिया और बोले प्रभु आज मेरी भक्ति जीत गई।",
              "YEH DEKHKAR BHISHMA NE DHANUSH RAKH DIYA AUR BOLE PRABHU AAJ MERI BHAKTI JEET GAYI",
              sc("cosmos", cast=[B(660, "namaste"), C("dkrishna", 1280, "bless", s=0.6)], fx=[("cosmic", 1280, 600), ("flowers",)])),
    ]},
    {"key": "shaiya", "title": "BAAN KI SHAIYA", "lines": [
        line_("दसवें दिन पांडवों ने शिखंडी को आगे रखकर भीष्म पर बाणों की वर्षा की।",
              "10VEIN DIN PANDAVON NE SHIKHANDI KO AAGE RAKHKAR BHISHMA PAR BAANON KI VARSHA KI",
              sc("dusk", cast=[C("arjun", 400, "bow"), C("krishna", 680, "reins"), B(1360, "stand", flip=True)],
                 fx=[("arrows", 460, 460, 1360, 560, 8, GOLD_HI)])),
        line_("भीष्म ने शस्त्र त्याग दिए और अर्जुन के बाणों से उनका शरीर जमीन से ऊपर उठ गया।",
              "BHISHMA NE SHASTRA TYAAG DIYE AUR ARJUN KE BAANON SE UNKA SHAREER ZAMEEN SE OOPAR UTH GAYA",
              sc("dusk", cast=[SH(960, s=0.95), C("krishna", 1420, "stand")], fx=[("glow", 960, 760, 360, FIRE_O)])),
        line_("जब भीष्म ने प्यास लगने पर पानी मांगा तो किसी को समझ नहीं आया।",
              "JAB BHISHMA NE PYAAS LAGNE PAR PAANI MAANGA TOH KISI KO SAMAJH NAHIN AAYA",
              sc("dusk", cast=[SH(820, s=0.9), C("arjun", 380, "bow"), C("krishna", 1360, "stand")])),
        line_("तब अर्जुन ने धरती में बाण मारा और मां गंगा की धारा फूटकर भीष्म के मुख में पहुंची।",
              "TAB ARJUN NE DHARTI MEIN BAAN MAARA AUR MAA GANGA KI DHAARA PHOOTKAR BHISHMA KE MUKH MEIN PAHUNCHI",
              sc("dawn", cast=[SH(960, s=0.95), C("arjun", 360, "bow"), C("krishna", 1420, "bless")],
                 fx=[("glow", 960, 780, 380, BLUE_GLOW), ("flowers",)])),
    ]},
    {"key": "uttarayan", "title": "UTTARAYAN AUR MOKSHA", "lines": [
        line_("भीष्म ने इच्छा मृत्यु के वरदान से अट्ठावन दिन तक उत्तरायण की प्रतीक्षा की।",
              "BHISHMA NE ICCHA MRITYU KE VARDAAN SE 58 DIN TAK UTTARAYAN KI PRATIKSHA KI",
              sc("dawn", cast=[SH(840, s=0.95), C("krishna", 1400, "bless")], fx=[("glow", 840, 720, 420, GOLD_HI)])),
        line_("इसी बीच उन्होंने युधिष्ठिर को राजधर्म का उपदेश दिया और श्री कृष्ण के सामने विष्णु सहस्रनाम गाया।",
              "ISI BEECH UNHONE YUDHISHTHIR KO RAJDHARMA KA UPDESH DIYA AUR SHRI KRISHNA KE SAAMNE VISHNU SAHASRANAM GAAYA",
              sc("cosmos", cast=[SH(780, s=0.9), C("dkrishna", 1360, "bless", s=0.6)], fx=[("cosmic", 1360, 600), ("flowers",)])),
        line_("माघ शुक्ल अष्टमी को सूर्य के उत्तरायण होते ही उन्होंने श्री कृष्ण को देखते हुए प्राण त्यागे।",
              "MAGH SHUKLA ASHTAMI KO SURYA KE UTTARAYAN HOTE HI UNHONE SHRI KRISHNA KO DEKHTE HUE PRAAN TYAAGE",
              sc("cosmos", cast=[C("dkrishna", 960, "bless", s=0.64)], fx=[("cosmic", 960, 580), ("flowers",)])),
        line_("अगर आपको भी श्री कृष्ण और भीष्म पितामह की ये कथा अच्छी लगी तो कमेंट में जय श्री कृष्ण लिखिए।",
              "AGAR AAPKO BHI SHRI KRISHNA AUR BHISHMA PITAMAH KI YEH KATHA ACHHI LAGI TOH COMMENT MEIN JAI SHRI KRISHNA LIKHIYE",
              sc("cosmos", cast=[C("dkrishna", 960, "flute", s=0.62)], fx=[("cosmic", 960, 600), ("flowers",)])),
        line_("और ऐसी ही कहानियों के लिए दिव्य रहस्य से जुड़े रहिए।",
              "AUR AISI HI KAHANIYON KE LIYE DIVYA RAHASYA SE JUDE RAHIYE",
              sc("dawn", cast=[B(660, "namaste"), C("krishna", 1280, "bless")], fx=[("flowers",)])),
    ]},
]

SOURCES = [
    "Mahabharata, Adi Parva (Sambhava Parva): Devavrata's Bhishma Pratigya for Satyavati and Shantanu's boon of Iccha-Mrityu.",
    "Mahabharata, Udyoga Parva (Ambopakhyana): Amba's tapasya and rebirth as Shikhandi.",
    "Mahabharata, Bhishma Parva: Day 9 (Krishna lifting the chariot wheel) and Day 10 (Bhishma on the bed of arrows; Arjuna piercing the earth for water).",
    "Mahabharata, Shanti & Anushasana Parva: 58 days on the bed of arrows, Rajdharma, Vishnu Sahasranama, and departure in Uttarayan.",
]

UPLOAD = {
    "title": "भीष्म पितामह बाणों की शय्या पर 58 दिन क्यों रुके रहे? | Bhishma Pratigya Full Story",
    "description": """
Mahabharat ke 10vein din jab Bhishma Pitamah baanon ki shaiya par gire, toh wo 58 din tak kyun zinda rahe? Aur
unhone Shikhandi ke saamne apna dhanush kyun rakh diya? Is video mein dekhiye poori katha: Devavrata ki Bhishma
Pratigya, Iccha-Mrityu ka vardaan, Amba aur Shikhandi ka rahasya, 9vein din jab Shri Krishna ne rath ka pahiya
uthaya, Arjun ke baan se Maa Ganga ka jal, aur Uttarayan par Vishnu Sahasranama.

Aapko is katha ka kaunsa hissa sabse zyada pasand aaya? Comment mein batayein aur JAI SHRI KRISHNA likhein!
""",
    "hashtags": "#Mahabharat #BhishmaPitamah #ShriKrishna #BhishmaPratigya #DivyaRahasya",
    "tags": [
        "bhishma pitamah", "bhishma pratigya", "baan ki shaiya", "58 days", "mahabharat story hindi",
        "shri krishna", "shikhandi", "uttarayan", "vishnu sahasranama", "divya rahasya", "kurukshetra",
    ],
    "pinned": "Bhishma Pitamah ne 58 din baanon ki shaiya par ruk kar duniya ko kya sabse bada sandesh diya? "
              "Apni raay comment mein likhein aur JAI SHRI KRISHNA zaroor likhein! 🙏",
}


def thumbnail(ctx):
    T = 1.5
    bg_dusk(ctx, T)
    rgba(ctx, (0.2, 0.03, 0.0), 0.35)
    ctx.paint()
    baan_shaiya(ctx, 1180, GROUND, 0.98, T)
    ar.krishna(ctx, 420, GROUND + 60, 0.65, T, pose="bless")
    text(ctx, "58 DIN KYUN RUKE?", W / 2, 160, 130, hexc("#FFD84A"), font="Impact", stroke=(0.15, 0, 0), stroke_w=12)
