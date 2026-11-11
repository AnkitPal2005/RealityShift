"""Karna aur Surya: daanveer Karna ne kavach kyun de diya? (~80s katha, seven scenes). Upload 12 Nov 2026 (Chhath week).

Usage (from SanatanKatha/):
  python make.py karna

Rahasya: a king who stood waist-deep every morning offering water to the sun and never refused anyone at that hour -
and that very habit took his greatest armour. Karna, Surya's son, set afloat by Kunti, born with the kavach-kundal;
king of Ang Desh (today's Bhagalpur-Munger, Bihar); Surya warns him in a dream that Indra will come; Indra comes as a
brahmin and asks for the kavach-kundal; Karna knows and still gives them with a smile - Daanveer Karna. Folk belief
ties Chhath's standing-in-water arghya to Karna, said as "kehte hain".
The kavach is shown lifting off as golden light, nothing graphic. Spoken words kept simple for the TTS.
Output: output/shorts/karna_short.mp4 (+ .json scene log, thumbnail, upload kit)
"""

from katha import *  # noqa: F401,F403  (engine helpers, devta as dv, scenery, Cued, story defaults)

TOPIC = "KARNA KAVACH KUNDAL DAAN"
OUTPUTS = {"edge": "karna_short.mp4"}
MUSIC_BPM = 88                      # Chhath was 76

SOURCES = [
    "Karna: son of Surya and Kunti, born with kavach (armour) and kundal (earrings), set afloat in a basket on the "
    "river and raised by Adhiratha and Radha - Mahabharata, Adi Parva and Vana Parva (Wikipedia 'Karna')",
    "Made king of Anga by Duryodhana; Anga's capital Champa lay near today's Bhagalpur, and the region covers "
    "Bhagalpur-Munger in Bihar (Wikipedia 'Anga'; 'Champapuri')",
    "Kundalaharana: Surya warns Karna in a dream that Indra will come as a brahmin to take his kavach-kundal for "
    "Arjuna's sake; Karna's vow to refuse nothing asked at his sun worship; he gives them anyway, Indra is moved and "
    "gives him the Vasavi Shakti - Mahabharata, Vana Parva (Kundalaharana Parva) (Wikipedia 'Karna')",
    "Folk belief in Bihar links Chhath's standing-in-water arghya to Karna's daily Surya worship - said as 'kehte "
    "hain' (common in Chhath explainers; not in the Mahabharata itself)",
]

# Simple spoken words only (no अर्घ्य / सूर्य / जन्म ...): see the voice memory and README.
SPEC = [
    {"key": "hook", "text": "SABSE BADA KAVACH?",
     "visual": "Dawn ghat: Karna waist-deep pours water to the rising sun, gold coins sparkle out to people; his "
               "kavach flickers; 'SABSE BADA KAVACH?' ribbon",
     "vo": [("open", [("सोचो...", "SOCHO...")], 0.4),
            ("tell", [("एक राजा,", "EK RAJA,"), ("जो रोज़ कमर तक पानी में खड़ा होकर", "JO ROZ KAMAR TAK PAANI MEIN KHADA HOKAR"),
                      ("सूरज को जल चढ़ाता था।", "SURAJ KO JAL CHADHATA THA.")], 0.3),
            ("build", [("और उस वक्त", "AUR US WAQT"), ("जो कोई कुछ भी माँगता,", "JO KOI KUCHH BHI MAANGTA,"),
                       ("वो कभी मना नहीं करता।", "WO KABHI MANA NAHI KARTA.")], 0.4),
            ("low", [("एक दिन", "EK DIN"), ("यही आदत...", "YAHI AADAT...")], 0.3),
            ("punch", [("उसका सबसे बड़ा कवच", "USKA SABSE BADA KAVACH"), ("ले गई!", "LE GAYI!")])]},
    {"key": "who", "text": "KARNA",
     "visual": "Dusk river: a reed basket with a glowing baby floats past; Kunti on the bank; then grown Karna with "
               "the golden kavach and shining kundal",
     "vo": [("tell", [("ये था कर्ण—", "YE THA KARNA—"), ("सूरज देवता का बेटा।", "SURAJ DEVTA KA BETA.")], 0.35),
            ("low", [("कुंती ने डर के मारे", "KUNTI NE DAR KE MAARE"), ("उसे टोकरी में रखकर", "USE TOKRI MEIN RAKHKAR"),
                     ("नदी में बहा दिया था।", "NADI MEIN BAHA DIYA THA.")], 0.35),
            ("awe", [("पर पैदा होते ही", "PAR PAIDA HOTE HI"), ("उसके शरीर पर", "USKE SHAREER PAR"),
                     ("सोने का कवच और कुंडल थे—", "SONE KA KAVACH AUR KUNDAL THE—")], 0.25),
            ("punch", [("जब तक वो पहने रहे,", "JAB TAK WO PEHNE RAHE,"), ("कोई उसे हरा नहीं सकता था!", "KOI USE HARA NAHI SAKTA THA!")])]},
    {"key": "raja", "text": "ANG DESH = BIHAR",
     "visual": "Royal hall: Karna as king, 'ANG DESH / AAJ KA BHAGALPUR-MUNGER' ribbon; then the ghat at dawn, Karna "
               "pouring water, gold coins given away",
     "vo": [("tell", [("बड़ा होकर कर्ण", "BADA HOKAR KARNA"), ("अंग देश का राजा बना—", "ANG DESH KA RAJA BANA—")], 0.25),
            ("warm", [("आज का भागलपुर-मुंगेर,", "AAJ KA BHAGALPUR-MUNGER,"), ("यानी अपना बिहार!", "YAANI APNA BIHAR!")], 0.35),
            ("tell", [("कहते हैं, वो रोज़ पानी में खड़ा होकर", "KEHTE HAIN, WO ROZ PAANI MEIN KHADA HOKAR"),
                      ("सूरज की पूजा करता,", "SURAJ KI POOJA KARTA,")], 0.2),
            ("build", [("और फिर जो माँगो,", "AUR PHIR JO MAANGO,"), ("दान में दे देता।", "DAAN MEIN DE DETA.")])]},
    {"key": "sapna", "text": "SAPNE MEIN SURAJ DEVTA",
     "visual": "Night: 'INDRA DEV / ARJUN KE PITA' ribbon; Karna asleep standing in the moonlight; a dream cloud opens "
               "with Surya Dev inside, warning him",
     "vo": [("low", [("ये बात इंद्र देव तक पहुँची,", "YE BAAT INDRA DEV TAK PAHUNCHI,")], 0.2),
            ("tell", [("जो युद्ध में", "JO YUDH MEIN"), ("अपने बेटे अर्जुन को बचाना चाहते थे।", "APNE BETE ARJUN KO BACHANA CHAHTE THE.")], 0.4),
            ("whisper", [("उसी रात,", "USI RAAT,"), ("कर्ण के सपने में", "KARNA KE SAPNE MEIN"), ("सूरज देवता आए—", "SURAJ DEVTA AAYE—")], 0.35),
            ("deva", [("बेटा, कल इंद्र आएगा।", "BETA, KAL INDRA AAYEGA."), ("कवच मत देना।", "KAVACH MAT DENA.")])]},
    {"key": "indra", "text": "KAVACH-KUNDAL DO",
     "visual": "Next dawn at the ghat: an old brahmin with a faint golden glow wades up to Karna mid-worship and asks "
               "for the kavach-kundal",
     "vo": [("tell", [("अगली सुबह,", "AGLI SUBAH,"), ("पूजा के वक्त", "POOJA KE WAQT"), ("एक ब्राह्मण आया...", "EK BRAHMAN AAYA...")], 0.4),
            ("char", [("बोला— राजा,", "BOLA— RAJA,"), ("मुझे तेरा कवच और कुंडल चाहिए।", "MUJHE TERA KAVACH AUR KUNDAL CHAHIYE.")], 0.5),
            ("ask", [("अब कर्ण क्या करता?", "AB KARNA KYA KARTA?")])]},
    {"key": "daan", "text": "DAANVEER KARNA",
     "visual": "Karna smiles and holds out his hands; the kavach and kundal lift off as golden light into the "
               "brahmin's hands; the brahmin glows gold (Indra); 'DAANVEER KARNA' ribbon",
     "vo": [("low", [("कर्ण सब जानता था।", "KARNA SAB JAANTA THA.")], 0.4),
            ("awe", [("फिर भी उसने", "PHIR BHI USNE"), ("मुस्कुराकर", "MUSKURAKAR"),
                     ("कवच-कुंडल उतार के दे दिए।", "KAVACH-KUNDAL UTAAR KE DE DIYE.")], 0.4),
            ("whisper", [("इंद्र भी", "INDRA BHI"), ("हैरान रह गए...", "HAIRAAN REH GAYE...")], 0.35),
            ("punch", [("उस दिन से दुनिया उसे कहती है—", "US DIN SE DUNIYA USE KEHTI HAI—"), ("दानवीर कर्ण!", "DAANVEER KARNA!")])]},
    {"key": "cta", "text": "JAI DAANVEER KARNA",
     "visual": "Dusk ghat with vratis raising their soops, Karna faint in the sky; comment card 'JAI DAANVEER KARNA'",
     "vo": [("warm", [("और कहते हैं,", "AUR KEHTE HAIN,"), ("छठ में पानी में खड़े होकर", "CHHATH MEIN PAANI MEIN KHADE HOKAR"),
                      ("जल चढ़ाने की रीत", "JAL CHADHANE KI REET"), ("यहीं से आई।", "YAHIN SE AAYI.")], 0.35),
            ("cta", [("घणा बड़ा दिल था भाई!", "GHANA BADA DIL THA BHAI!"), ("कमेंट में लिखो—", "COMMENT MEIN LIKHO—")], 0.2),
            ("punch", [("जय हो दानवीर कर्ण की!", "JAI HO DAANVEER KARNA KI!")])]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
SUN = hexc("#FFB347")
HOT = hot_words({"SOCHO": GOLD_HI, "JAL": hexc("#9FE8FF"), "SURAJ": SUN, "MAANGTA": GOLD_HI, "MANA": hexc("#FF6B6B"),
                 "AADAT": GOLD_HI, "KAVACH": GOLD_HI, "KARNA": SAFF, "KARNA—": SAFF, "KUNTI": hexc("#FFB3C7"),
                 "TOKRI": SAFF, "NADI": hexc("#9FE8FF"), "SONE": GOLD_HI, "KUNDAL": GOLD_HI, "HARA": hexc("#FF6B6B"),
                 "ANG": SAFF, "BHAGALPUR-MUNGER": SAFF, "BIHAR": GOLD_HI, "DAAN": GOLD_HI, "INDRA": hexc("#BFE6FF"),
                 "ARJUN": hexc("#BFE6FF"), "SAPNE": hexc("#BFE6FF"), "BETA": SUN, "MAT": hexc("#FF6B6B"),
                 "BRAHMAN": SAFF, "KYA": GOLD_HI, "JAANTA": GOLD_HI, "MUSKURAKAR": GOLD_HI, "KAVACH-KUNDAL": GOLD_HI,
                 "HAIRAAN": hexc("#BFE6FF"), "DAANVEER": GOLD_HI, "CHHATH": GOLD_HI, "GHANA": SAFF, "BHAI": SAFF,
                 "JAI": GOLD_HI, "CHHATHI": hexc("#FF6B6B"), "MAIYA": hexc("#FF6B6B"), "COMMENT": GOLD_HI})

WATER = 1090


def water_front(ctx, morning=True):
    """Water in front of anyone standing in the river: hides the legs, with a few ripples."""
    g = cairo.LinearGradient(0, WATER, 0, H)
    g.add_color_stop_rgba(0, *(hexc("#C98A6A") if morning else hexc("#7A3A3A")), 1.0)
    g.add_color_stop_rgba(1, *(hexc("#2E4A6A") if morning else hexc("#2A1224")), 1.0)
    ctx.rectangle(0, WATER, W, H)
    ctx.set_source(g)
    ctx.fill()
    for i in range(6):
        y = WATER + 14 + 16 * i
        line(ctx, [(60 + 30 * i, y), (W - 60 - 30 * i, y)], (1, 1, 1), 2, 0.18)


def in_water(s):
    """Feet y for a character of scale s standing waist-deep at the WATER line."""
    return WATER + 350 * s


def coins(ctx, t, x, y, u, n=14, seed=1):
    """Gold coins flying out from (x, y), u = seconds since they were given."""
    if u <= 0:
        return
    for i in range(n):
        ang = -math.pi * (0.15 + 0.7 * rnd(i, seed))
        v = 380 + 200 * rnd(i, seed + 1)
        k = min(u, 1.6)
        cx = x + v * math.cos(ang) * k
        cy = y + v * math.sin(ang) * k + 300 * k * k
        a = 1 - clamp((u - 1.2) / 0.4)
        circle(ctx, cx, cy, 13, GOLD, a)
        circle(ctx, cx, cy, 7, GOLD_HI, a)


def dream_cloud(ctx, x, y, r, u, t):
    """Dream bubble with Surya Dev inside, popping open over u seconds."""
    if u <= 0:
        return
    k = ease_out_back(clamp(u / 0.5))
    for i, (dx, dy, rr) in enumerate(((-260, 380, 22), (-210, 300, 34))):
        circle(ctx, x + dx, y + dy, rr * k, (1, 1, 1), 0.85)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    for j in range(10):
        ang = j / 10 * math.tau
        circle(ctx, r * 0.78 * math.cos(ang), r * 0.62 * math.sin(ang), r * 0.42, (1, 1, 1), 0.88)
    dv.ell(ctx, 0, 0, r * 0.95, r * 0.75)
    rgba(ctx, (1, 0.98, 0.94), 0.95)
    ctx.fill()
    ctx.restore()
    if k > 0.6:
        ctx.save()
        ctx.rectangle(x - r * 0.9, y - r * 0.72, r * 1.8, r * 1.44)
        ctx.clip()
        dv.surya(ctx, x, y + r * 0.95, 0.42, t, a=clamp((u - 0.3) / 0.4))
        ctx.restore()


class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"maang": c("MAANGTA", d * 0.4), "aadat": c("AADAT", d * 0.65), "kavach": c("KAVACH", d * 0.82)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "ghanti"), (0.6, "whoosh"), (b["maang"], "kaching"), (b["aadat"], "soft_thud"),
                (b["kavach"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        ghat(ctx, t, lerp(860, 760, ease_in_out(clamp(t / d))), morning=True, diyas=False)
        flick = 1.0 if t < b["kavach"] else 0.55 + 0.45 * abs(math.sin((t - b["kavach"]) * 9))
        dv.karna(ctx, 540, in_water(0.8), 0.8, t, pose="arghya", pour=clamp((t - 0.4) / 0.5), kavach=flick)
        water_front(ctx)
        coins(ctx, t, 540, 760, t - b["maang"])
        dv.ribbon(ctx, "SABSE BADA KAVACH?", 540, 300, t - b["kavach"], size=76)


class Who(Cued):
    def beats(self, d):
        c = self.cue
        return {"kunti": c("KUNTI", d * 0.25), "paida": c("PAIDA", d * 0.55), "hara": c("HARA", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["kunti"], "whoosh"), (b["paida"], "shimmer"), (b["hara"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        if t < b["paida"]:
            ghat(ctx, t, 830, diyas=False)
            mother(ctx, 170, GROUND - 20, 0.62, t)
            k = clamp((t - b["kunti"] + 0.4) / max(b["paida"] - b["kunti"] + 0.4, 1.0))
            dv.basket(ctx, lerp(320, 980, k), 1010, 0.9, t)
            dv.ribbon(ctx, "KARNA", 540, 300, t - 0.2, size=90, sub="SURAJ DEVTA KA BETA")
        else:
            u = t - b["paida"]
            palace(ctx, t)
            dv.sun_disc(ctx, 540, 520, 150, t, a=0.5)
            dv.karna(ctx, 540, GROUND, 0.82, t, pose="stand", a=clamp(u / 0.4))
            dv.ribbon(ctx, "KAVACH + KUNDAL", 540, 300, u - 0.3, size=80)
            if t > b["hara"]:
                glow(ctx, 540, 840, 380, GOLD_HI, 0.35 * abs(math.sin(t * 3)))
        flash(ctx, t - b["paida"], c=(1, 0.95, 0.7), dur=0.5)


class Raja(Cued):
    def beats(self, d):
        c = self.cue
        return {"ang": c("ANG", d * 0.15), "bihar": c("BIHAR", d * 0.35), "pooja": c("POOJA", d * 0.6),
                "daan": c("DAAN", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["bihar"], "ghanti"), (b["pooja"], "whoosh"), (b["daan"], "kaching")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        if t < b["pooja"]:
            palace(ctx, t)
            dv.karna(ctx, 540, GROUND, 0.82, t, pose="stand", look=(0, -0.2))
            dv.ribbon(ctx, "ANG DESH", 540, 300, t - b["ang"], size=90, sub="AAJ KA BHAGALPUR-MUNGER, BIHAR")
        else:
            ghat(ctx, t, 790, morning=True, diyas=False)
            dv.karna(ctx, 540, in_water(0.8), 0.8, t, pose="arghya", pour=clamp((t - b["pooja"]) / 0.5))
            water_front(ctx)
            coins(ctx, t, 540, 760, t - b["daan"], n=18, seed=4)
        flash(ctx, t - b["pooja"], c=(1, 0.9, 0.7), dur=0.4)


class Sapna(Cued):
    def beats(self, d):
        c = self.cue
        return {"indra": c("INDRA", 0.2), "raat": c("RAAT", d * 0.45), "sapne": c("SAPNE", d * 0.55),
                "mat": c("MAT", d * 0.88)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["raat"], "whoosh"), (b["sapne"], "shimmer"), (b["mat"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_river(ctx, t)
        if t < b["raat"]:
            dv.ribbon(ctx, "INDRA DEV", 540, 300, t - b["indra"], size=84, sub="ARJUN KE PITA")
            glow(ctx, 540, 560, 300, hexc("#BFE6FF"), 0.3 + 0.2 * math.sin(t * 7))
            for k in range(3):   # a few lightning flickers in the clouds
                if int(t * 6 + k) % 7 == 0:
                    line(ctx, [(300 + 220 * k, 420), (280 + 220 * k, 500), (320 + 220 * k, 520), (300 + 220 * k, 600)],
                         hexc("#E9FBFF"), 6, 0.8)
        dv.karna(ctx, 300, GROUND, 0.72, t, pose="namaste", mood="smile")
        dream_cloud(ctx, 700, 640, 280, t - b["sapne"], t)
        if t > b["mat"]:
            dv.ribbon(ctx, "KAVACH MAT DENA", 700, 300, t - b["mat"], size=72)


class Indra(Cued):
    def beats(self, d):
        c = self.cue
        return {"aaya": c("BRAHMAN", d * 0.3), "bola": c("BOLA", d * 0.45), "kya": c("KYA", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "ghanti"), (b["aaya"], "whoosh"), (b["bola"], "pop"), (b["kya"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        ghat(ctx, t, 800, morning=True, diyas=False)
        dv.karna(ctx, 360, in_water(0.75), 0.75, t, pose="arghya", pour=1.0 if t < b["bola"] else 0.0,
                 look=(0.6, 0))
        k = ease_in_out(clamp((t - b["aaya"] + 0.5) / 1.2))
        dv.brahmin(ctx, lerp(1150, 790, k), WATER + 330 * 0.7, 0.7, t, pose="ask" if t > b["bola"] else "stand",
                   mood="look", look=(0.8, 0), flip=True, hint=0.25, hint_c=GOLD_HI)
        water_front(ctx)
        if b["bola"] < t < b["kya"] + 0.2:
            bubble(ctx, "KAVACH-KUNDAL DO", 700, 520, t - b["bola"] - 0.2, (760, 600))
        dv.ribbon(ctx, "AB KYA KAREGA?", 540, 300, t - b["kya"], size=80)


class Daan(Cued):
    def beats(self, d):
        c = self.cue
        return {"muskura": c("MUSKURAKAR", d * 0.3), "hairaan": c("HAIRAAN", d * 0.65), "veer": c("DAANVEER", d * 0.88)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["muskura"], "shimmer"), (b["muskura"] + 1.0, "ghanti"),
                (b["hairaan"], "shimmer"), (b["veer"], "shankh"), (b["veer"] + 0.05, "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        ghat(ctx, t, 790, morning=True, diyas=False)
        u = t - b["muskura"]
        kav = 1 - clamp(u / 1.2) if u > 0 else 1.0
        dv.karna(ctx, 360, in_water(0.75), 0.75, t, pose="give" if u > 0 else "namaste",
                 mood="smile" if u > 0 else "calm", kavach=kav)
        glow_in = clamp((t - b["hairaan"]) / 0.6)
        dv.brahmin(ctx, 790, WATER + 330 * 0.7, 0.7, t, pose="ask", mood="smile", flip=True,
                   hint=0.3 + 0.7 * glow_in, hint_c=GOLD_HI)
        water_front(ctx)
        if 0 < u < 2.2:   # the kavach-kundal travel as golden light into the brahmin's hands
            k = ease_in_out(clamp(u / 1.6))
            x, y = lerp(360, 790 - 262 * 0.7, k), lerp(in_water(0.75) - 460 * 0.75, WATER + 330 * 0.7 - 440 * 0.7, k) - 120 * math.sin(math.pi * k)
            glow(ctx, x, y, 110, GOLD_HI, 0.9)
            dv.sun_disc(ctx, x, y, 26, t, rays=12)
        if u > 0:
            dv.petals(ctx, u, 26, seed=6)
        dv.ribbon(ctx, "DAANVEER KARNA", 540, 300, t - b["veer"], size=88)


class Cta(Cued):
    def beats(self, d):
        c = self.cue
        return {"comment": c("COMMENT", d * 0.6), "jai": c("JAI", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "ghanti"), (b["comment"], "pop"), (b["jai"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        ghat(ctx, t, 840)
        dv.karna(ctx, 540, 820, 0.42, t, pose="arghya", pour=1.0, a=0.55)
        def row():
            for k, x in enumerate((170, 420, 670, 920)):
                dv.vrati(ctx, x, WATER + 8 * (k % 2), 0.66, t + k, lift=1.0)
        row()
        dv.silhouette(ctx, row, hexc("#3A0E1A"), a=0.45)
        water_front(ctx, morning=False)
        comment_card(ctx, t, b["comment"] - 0.3, b["jai"], "JAI DAANVEER KARNA", y=1000)


SCENE_CLASSES = {"hook": Hook, "who": Who, "raja": Raja, "sapna": Sapna, "indra": Indra, "daan": Daan, "cta": Cta}


# ============================================================ upload kit (see upload_kit.py)

UPLOAD = {
    "titles": [
        "Karna Ne Apna Kavach Kyun De Diya? Daanveer Karna Ki Kahani",
        "Daanveer Karna: Suraj Devta Ki Chetavni Ke Baad Bhi Daan",
        "Karna Aur Indra: Kavach Kundal Ki Kahani",
        "Bihar Ka Raja Karna: Ang Desh Aur Surya Pooja",
        "Karna Ki Kahani: Suraj Ka Beta Jo Kabhi Mana Nahi Karta Tha",
        "Kavach Kundal Kyun Diye? Mahabharat Ki Katha",
        "Chhath Aur Karna Ka Rishta: Paani Mein Khade Hokar Jal",
        "Karna Kavach Kundal Story In Hindi",
        "Indra Brahman Bankar Kyun Aaye? Karna Ki Katha",
        "Sapne Mein Suraj Devta Ne Karna Ko Kya Kaha?",
    ],
    "title": "Karna Ne Apna Kavach Kyun De Diya? Daanveer Karna Ki Kahani",
    "thumb_text": "SAB JAANTA THA",
    "queries": ["karna ki kahani", "karna kavach kundal", "daanveer karna"],
    "description": """
Karna ki kahani: Suraj devta ka beta, jo janam se sone ka kavach kundal pehne tha. Daanveer Karna ne Indra ko
apna kavach kyun de diya, jabki sapne mein Suraj devta ne mana kiya tha?

Is Short me:
• Kunti ne Karna ko tokri mein nadi mein bahaya
• Paida hote hi sone ka kavach aur kundal
• Ang Desh ka raja: aaj ka Bhagalpur-Munger, Bihar
• Roz paani mein khade hokar Surya pooja, phir jo maango wo daan
• Sapne mein Suraj devta ki chetavni, aur Indra ka brahman bankar aana
• Sab jaante hue bhi muskura kar diya daan: Daanveer Karna

Comment me likho: Jai Daanveer Karna.

Note: Karna ki katha Mahabharat (Vana Parva, Kundalaharana) se hai. Chhath ka Karna se jod lok maanyata hai.
""",
    "tags": ["karna", "karna ki kahani", "daanveer karna", "karna kavach kundal", "karna and indra",
             "mahabharat ki kahani", "surya putra karna", "ang desh", "chhath puja", "chhath katha",
             "karna story in hindi", "mahabharat story", "pauranik katha", "divya rahasya", "bihar"],
    "hashtags": ["#Shorts", "#Karna", "#Mahabharat"],
}


def thumbnail(ctx):
    """1080x1920 cover: 'SAB JAANTA / THA' over Karna glowing with his kavach and the brahmin's open hand."""
    ghat(ctx, 0.3, 800, morning=True, diyas=False)
    glow(ctx, 540, 1000, 600, GOLD_HI, 0.5)
    dv.karna(ctx, 470, in_water(1.15) + 80, 1.15, 0.3, pose="give", mood="smile")
    dv.brahmin(ctx, 930, WATER + 330 * 0.9 + 60, 0.9, 0.3, pose="ask", mood="smile", flip=True, hint=0.8, hint_c=GOLD_HI)
    water_front(ctx)
    g = cairo.LinearGradient(0, 0, 0, 640)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.9)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 640)
    ctx.set_source(g)
    ctx.fill()
    text(ctx, "SAB JAANTA", 540, 230, 190, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "THA!", 540, 430, 220, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
