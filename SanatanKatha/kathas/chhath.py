"""Chhath: doobte suraj ko arghya kyun? (~75-85s katha, seven scenes). For Chhath Puja, 13-16 Nov 2026.

Usage (from SanatanKatha/):
  python make.py chhath

Rahasya: every other day the world bows to the rising sun, Chhath offers arghya to the setting sun first. Why?
Story (Brahmavaivarta Puran tradition): Raja Priyavrat had no child; Maharshi Kashyap's yagya; the newborn would not
open his eyes; Shashthi (Chhathi) Devi came down, touched him and he laughed; her worship on Kartik Shukla Shashthi = Chhath,
she is Chhathi Maiya (and, by popular belief, Surya Dev's sister). The answer: the evening arghya is to Pratyusha
(the sun's last ray), the morning one to Usha (the first ray) - and what sets is what rises again.
The baby is shown asleep, never anything distressing; the devi's touch wakes him with a laugh.
Output: output/shorts/chhath_short.mp4 (+ .json scene log, thumbnail, upload kit)
"""

from core.katha import *  # noqa: F401,F403  (engine helpers, devta as dv, scenery, Cued, story defaults)

TOPIC = "CHHATH DOOBTA SURAJ ARGHYA"
OUTPUTS = {"edge": "chhath_short.mp4"}
MUSIC_BPM = 76                      # Barbarik was 84

SOURCES = [
    "Shashthi Devi (Devsena), 'the sixth part of Prakriti', protector of children; the story of King Priyavrat and "
    "Queen Malini, Maharshi Kashyap's putreshti yagya and the child revived by the devi, after which her worship "
    "began on Shukla Shashthi - Brahmavaivarta Purana, Prakriti Khanda (Wikipedia 'Shashthi (goddess)', 'Chhath')",
    "Chhathi Maiya regarded as Surya Dev's sister; evening arghya to Pratyusha (the sun's last ray) and morning "
    "arghya to Usha (the first ray) - popular Chhath belief, widely explained in Hindi media Chhath explainers "
    "(e.g. Dainik Jagran, Navbharat Times); said as 'maanyata hai'",
    "Chhath Puja 2026: Nahay Khay 13 Nov, Kharna 14 Nov, Sandhya Arghya 15 Nov, Usha Arghya 16 Nov "
    "(Hindutone Chhath 2026 calendar; DekhoPanchang) - check a local panchang",
    "Versions differ (some tell of Sita, Draupadi or Karna keeping the vrat); this Short follows the Priyavrat katha",
]

# kathavachak lines: (tone, [(spoken Hindi, CAPTION), ...], held pause)
# Words are kept to everyday spoken Hindi the TTS says cleanly (user, 11 Nov 2026): no अर्घ्य / हरी-भरी / षष्ठी /
# पर्व / संतान / मान्यता - say "jal chadhana", "chhathi", "tyohaar", "aulaad", "log maante hain" instead.
SPEC = [
    {"key": "hook", "text": "DOOBTA SURAJ?",
     "visual": "Sunrise over an empty river, then dusk: vratis waist-deep raise their soops to a setting sun; "
               "'DOOBTA SURAJ?' ribbon",
     "vo": [("open", [("दुनिया उगते सूरज को", "DUNIYA UGTE SURAJ KO"), ("हाथ जोड़ती है...", "HAATH JODTI HAI...")], 0.4),
            ("low", [("पर एक त्योहार ऐसा है,", "PAR EK TYOHAAR AISA HAI,")], 0.2),
            ("build", [("जहाँ पहले", "JAHAN PEHLE"), ("डूबते सूरज को", "DOOBTE SURAJ KO"),
                       ("जल चढ़ाया जाता है।", "JAL CHADHAYA JAATA HAI.")], 0.4),
            ("ask", [("क्यों?", "KYUN?")], 0.35),
            ("punch", [("ये रहस्य शुरू होता है", "YE RAHASYA SHURU HOTA HAI"), ("एक राजा के आँसुओं से।", "EK RAJA KE AANSUON SE.")])]},
    {"key": "raja", "text": "RAJA PRIYAVRAT",
     "visual": "Royal hall: the sad king and queen; Rishi Kashyap's havan fire; the queen holds a baby who sleeps on, "
               "eyes shut; the colours dim",
     "vo": [("tell", [("कहते हैं, राजा प्रियव्रत के घर", "KEHTE HAIN, RAJA PRIYAVRAT KE GHAR"), ("कोई औलाद नहीं थी।", "KOI AULAAD NAHI THI.")], 0.3),
            ("tell", [("ऋषि कश्यप ने हवन करवाया,", "RISHI KASHYAP NE HAVAN KARWAYA,"), ("और रानी की गोद भरी—", "AUR RANI KI GOD BHARI—")], 0.4),
            ("whisper", [("पर बच्चा...", "PAR BACHCHA..."), ("आँखें ही नहीं खोल रहा था।", "AANKHEIN HI NAHI KHOL RAHA THA.")])]},
    {"key": "devi", "text": "CHHATHI DEVI",
     "visual": "Night river: the king sits with the sleeping baby; a beam of light; the devi appears and touches "
               "the child, who opens his eyes and laughs",
     "vo": [("low", [("रोता हुआ राजा", "ROTA HUA RAJA"), ("नदी किनारे जा बैठा...", "NADI KINARE JA BAITHA...")], 0.4),
            ("build", [("तभी आसमान से", "TABHI AASMAAN SE"), ("एक रोशनी उतरी—", "EK ROSHNI UTRI—")], 0.3),
            ("maa", [("मैं छठी देवी हूँ,", "MAIN CHHATHI DEVI HOON,"), ("हर बच्चे की रक्षा करती हूँ।", "HAR BACHCHE KI RAKSHA KARTI HOON.")], 0.4),
            ("punch", [("देवी ने बच्चे को छुआ,", "DEVI NE BACHCHE KO CHHUA,"), ("और बच्चा", "AUR BACHCHA"),
                       ("खिलखिला उठा!", "KHILKHILA UTHA!")])]},
    {"key": "vrat", "text": "CHHATHI MAIYA",
     "visual": "Dusk ghat full of vratis; 'KARTIK KA CHHATHA DIN' ribbon; a golden 'CHHATH' ribbon; Chhathi Maiya "
               "glows in the sky above them",
     "vo": [("tell", [("उसी दिन से—", "USI DIN SE—"), ("कार्तिक महीने के छठे दिन", "KARTIK MAHINE KE CHHATHE DIN"),
                      ("उनकी पूजा होने लगी।", "UNKI POOJA HONE LAGI.")], 0.3),
            ("awe", [("छठे दिन से नाम पड़ा—", "CHHATHE DIN SE NAAM PADA—")], 0.25),
            ("punch", [("छठ!", "CHHATH!")], 0.3),
            ("awe", [("और देवी कहलाईं—", "AUR DEVI KEHLAYIN—"), ("छठी मैया।", "CHHATHI MAIYA.")])]},
    {"key": "surya", "text": "BHAI-BEHEN",
     "visual": "Surya Dev with his rayed disc beside Chhathi Maiya; 'BHAI • BEHEN' ribbon",
     "vo": [("tell", [("और लोग मानते हैं,", "AUR LOG MAANTE HAIN,"), ("छठी मैया", "CHHATHI MAIYA"),
                      ("सूरज देवता की बहन हैं।", "SURAJ DEVTA KI BEHEN HAIN.")], 0.3),
            ("build", [("इसलिए छठ में", "ISLIYE CHHATH MEIN"), ("भाई-बहन दोनों की", "BHAI-BEHEN DONO KI"),
                       ("पूजा होती है।", "POOJA HOTI HAI.")])]},
    {"key": "rahasya", "text": "PRATYUSHA • USHA",
     "visual": "Dusk: a vrati offers water to the last ray ('PRATYUSHA'); dawn: the first ray ('USHA'); the sun sets "
               "and rises again; 'BURE WAQT MEIN BHI HAATH JODO'",
     "vo": [("low", [("अब असली रहस्य—", "AB ASLI RAHASYA—")], 0.35),
            ("tell", [("शाम का जल", "SHAAM KA JAL"), ("सूरज की आखिरी किरण को,", "SURAJ KI AAKHIRI KIRAN KO,"),
                      ("जिसे प्रत्युषा कहते हैं।", "JISE PRATYUSHA KEHTE HAIN.")], 0.3),
            ("tell", [("और सुबह का जल", "AUR SUBAH KA JAL"), ("पहली किरण को,", "PEHLI KIRAN KO,"),
                      ("जिसे उषा कहते हैं।", "JISE USHA KEHTE HAIN.")], 0.4),
            ("awe", [("जो डूबता है,", "JO DOOBTA HAI,"), ("वही कल फिर उगता है।", "WAHI KAL PHIR UGTA HAI.")], 0.3),
            ("punch", [("छठ सिखाता है—", "CHHATH SIKHATA HAI—"), ("बुरे वक्त में भी", "BURE WAQT MEIN BHI"),
                       ("हाथ जोड़े रखो!", "HAATH JODE RAKHO!")])]},
    {"key": "cta", "text": "JAI CHHATHI MAIYA",
     "visual": "Chhathi Maiya blessing with both hands above a comment card that types 'JAI CHHATHI MAIYA'",
     "vo": [("warm", [("छठी मैया", "CHHATHI MAIYA"), ("सबके घर खुशियाँ भरें।", "SABKE GHAR KHUSHIYAN BHAREIN.")], 0.3),
            ("cta", [("घणे प्यार से, भाई,", "GHANE PYAAR SE, BHAI,"), ("कमेंट में लिखो—", "COMMENT MEIN LIKHO—")], 0.2),
            ("punch", [("जय छठी मैया!", "JAI CHHATHI MAIYA!")])]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)   # kathavachak tones + held pauses (katha.TONES)
SUN = hexc("#FFB347")
HOT = hot_words({"JAL": hexc("#9FE8FF"), "CHADHAYA": hexc("#9FE8FF"), "TYOHAAR": SAFF, "AULAAD": SAFF,
                 "HAVAN": SUN, "CHHATHE": GOLD_HI, "KIRAN": SUN, "HAATH": GOLD_HI, "JODE": GOLD_HI, "KHUSHIYAN": GOLD_HI,
                 "GHANE": SAFF, "DEVTA": SUN, "DOOBTE": SUN, "SURAJ": SUN, "ARGHYA": GOLD_HI, "KYUN?": GOLD_HI, "RAHASYA": GOLD_HI,
                 "AANSUON": hexc("#BFE6FF"), "PRIYAVRAT": SAFF, "KASHYAP": SAFF, "YAGYA": SUN, "BACHCHA": hexc("#FFB3C7"),
                 "BACHCHA...": hexc("#FFB3C7"), "AANKHEIN": hexc("#FFB3C7"), "ROSHNI": GOLD_HI, "SHASHTHI": GOLD_HI,
                 "RAKSHA": GOLD_HI, "KHILKHILA": GOLD_HI, "KARTIK": SAFF, "CHHATH!": GOLD_HI, "CHHATH": GOLD_HI,
                 "CHHATHI": hexc("#FF6B6B"), "MAIYA": hexc("#FF6B6B"), "SURYA": SUN, "BEHEN": hexc("#FFB3C7"),
                 "BHAI-BEHEN": hexc("#FFB3C7"), "AAKHIRI": SUN, "PRATYUSHA": SUN, "PEHLI": hexc("#FFE0A3"),
                 "USHA": hexc("#FFE0A3"), "DOOBTA": SUN, "UGTA": hexc("#FFE0A3"), "BURE": hexc("#FF6B6B"),
                 "PRANAM!": GOLD_HI, "GHANI": SAFF, "BHAI": SAFF, "JAI": GOLD_HI, "COMMENT": GOLD_HI})

WATER = 1090                      # waterline the vratis stand in


def vratis(ctx, t, xs, s=0.85, sil=True, lift_t=0.0):
    """A row of vratis raising their soops; backlit silhouettes by default."""
    def draw():
        for k, x in enumerate(xs):
            lift = ease_in_out(clamp((t - lift_t - 0.15 * k) / 0.8))
            dv.vrati(ctx, x, WATER + 10 * (k % 2), s * (1 - 0.08 * (k % 2)), t + k, lift=lift)
    draw()
    if sil:   # backlit by the low sun: colours stay readable under a warm shadow
        dv.silhouette(ctx, draw, hexc("#3A0E1A"), a=0.45)
    ctx.rectangle(0, WATER, W, 120)               # water in front of their waists
    rgba(ctx, hexc("#2A1224"), 0.55)
    ctx.fill()


class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"parv": c("PARV", d * 0.2), "doob": c("DOOBTE", d * 0.4), "kyun": c("KYUN", d * 0.6),
                "aansu": c("AANSUON", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "ghanti"), (b["parv"], "whoosh"), (b["doob"], "shimmer"), (b["kyun"], "thud"),
                (b["aansu"], "soft_thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        if t < b["parv"]:
            ghat(ctx, t, lerp(900, 760, ease_in_out(clamp(t / max(b["parv"], 0.5)))), morning=True, diyas=False)
        else:
            u = t - b["parv"]
            ghat(ctx, t, lerp(720, 870, ease_in_out(clamp(u / max(d - b["parv"], 1.0)))))
            vratis(ctx, t, (200, 540, 880), s=0.8, lift_t=b["doob"] - 0.4)
        flash(ctx, t - b["parv"], c=(1, 0.8, 0.5), dur=0.4)
        dv.ribbon(ctx, "DOOBTA SURAJ?", 540, 300, t - b["kyun"], size=84)


class Raja(Cued):
    def beats(self, d):
        c = self.cue
        return {"yagya": c("KASHYAP", d * 0.3), "god": c("GOD", d * 0.55), "bachcha": c("BACHCHA", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["yagya"], "ghanti"), (b["god"], "shimmer"), (b["bachcha"], "soft_thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        palace(ctx, t)
        ya = clamp((t - b["yagya"]) / 0.4) * (1 - clamp((t - b["god"]) / 0.5))
        if ya > 0:
            dv.group(ctx, ya, lambda: (dv.brahmin(ctx, 540, GROUND - 160, 0.55, t, mood="smile"),
                                       dv.yagya_kund(ctx, 540, GROUND - 10, 0.75, t)))
        dv.raja(ctx, 260, GROUND, 0.72, t, pose="stand", mood="sad")
        mother(ctx, 800, GROUND, 0.82, t)
        if t > b["god"]:
            dv.baby(ctx, 760, 760, 0.75 * ease_out_back(clamp((t - b["god"]) / 0.4)), t, awake=False)
        dv.ribbon(ctx, "RAJA PRIYAVRAT", 540, 300, t - 0.3, size=76)
        dim = clamp((t - b["bachcha"]) / 0.8)
        if dim > 0:
            ctx.rectangle(0, 0, W, H)
            rgba(ctx, (0.08, 0.08, 0.14), 0.45 * dim)
            ctx.fill()


class Devi(Cued):
    def beats(self, d):
        c = self.cue
        return {"roshni": c("ROSHNI", d * 0.3), "main": c("CHHATHI", d * 0.5), "chhua": c("CHHUA", d * 0.72),
                "khil": c("KHILKHILA", d * 0.88)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["roshni"], "shimmer"), (b["roshni"] + 0.3, "ghanti"), (b["chhua"], "shimmer"),
                (b["khil"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_river(ctx, t)
        u = t - b["roshni"]
        if u > 0:   # beam of light down onto the bank
            k = clamp(u / 0.6)
            g = cairo.LinearGradient(0, 0, 0, GROUND)
            g.add_color_stop_rgba(0, 1, 0.95, 0.75, 0.0)
            g.add_color_stop_rgba(1, 1, 0.9, 0.6, 0.45 * k)
            ctx.move_to(640, 0)
            ctx.line_to(760, 0)
            ctx.line_to(880, GROUND)
            ctx.line_to(520, GROUND)
            ctx.close_path()
            ctx.set_source(g)
            ctx.fill()
        awake = t > b["khil"]
        dv.raja(ctx, 290, GROUND, 0.8, t, pose="hold", mood="happy" if awake else "sad",
                child="awake" if awake else "asleep")
        if u > 0.2:
            pose = "touch" if t > b["chhua"] else "bless"
            dv.devi(ctx, 700, GROUND, 0.8, t, pose=pose, flip=True, a=clamp((u - 0.2) / 0.6))
        v = t - b["chhua"]
        if v > 0:   # a stream of light from her palm to the child
            pts = [(700 - 270 * 0.8, GROUND - 360 * 0.8), (420, 760), (290, GROUND - 450 * 0.8)]
            line(ctx, pts, GOLD_HI, 10, 0.7 * clamp(v / 0.4) * (1 - clamp((v - 1.6) / 0.6)))
        if awake:
            dv.petals(ctx, t - b["khil"], 30, seed=3)
        dv.ribbon(ctx, "CHHATHI DEVI", 540, 300, t - b["main"], size=80)


class Vrat(Cued):
    def beats(self, d):
        c = self.cue
        return {"kartik": c("KARTIK", d * 0.15), "chhath": c("CHHATH!", d * 0.55), "maiya": c("MAIYA", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "ghanti"), (b["kartik"], "pop"), (b["chhath"], "shankh"), (b["chhath"] + 0.05, "boom"),
                (b["maiya"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        ghat(ctx, t, 820)
        u = t - b["maiya"]
        if u > 0:
            glow(ctx, 540, 600, 420, hexc("#FFB347"), 0.5 * clamp(u / 0.5))
            dv.devi(ctx, 540, 790, 0.5, t, pose="open", a=clamp(u / 0.6))
        vratis(ctx, t, (150, 400, 680, 930), s=0.68, lift_t=0.3)
        if t < b["chhath"]:
            dv.ribbon(ctx, "KARTIK KA CHHATHA DIN", 540, 300, t - b["kartik"], size=64)
        elif u <= 0:
            dv.ribbon(ctx, "CHHATHA DIN  →  CHHATH", 540, 300, t - b["chhath"], size=84)
        else:
            dv.ribbon(ctx, "CHHATHI MAIYA", 540, 250, u, size=84)


class Surya(Cued):
    def beats(self, d):
        c = self.cue
        return {"behen": c("BEHEN", d * 0.4), "arghya": c("POOJA", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "shimmer"), (b["behen"], "ghanti"), (b["arghya"], "pop")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dv.sky(ctx, hexc("#4A1A3A"), hexc("#F29A4A"), hexc("#3A1A12"), 0.6)
        ctx.rectangle(0, GROUND - 30, W, H)
        rgba(ctx, hexc("#3A1A12"))
        ctx.fill()
        dv.surya(ctx, 300, GROUND, 0.7, t)
        dv.devi(ctx, 790, GROUND, 0.72, t, pose="bless", a=clamp((t - b["behen"] + 0.6) / 0.5))
        dv.ribbon(ctx, "BHAI  •  BEHEN", 540, 300, t - b["behen"], size=84)


class Rahasya(Cued):
    def beats(self, d):
        c = self.cue
        return {"shaam": c("SHAAM", d * 0.12), "subah": c("SUBAH", d * 0.35), "doob": c("DOOBTA", d * 0.6),
                "sikh": c("SIKHATA", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["shaam"], "ghanti"), (b["subah"], "shimmer"), (b["doob"], "whoosh"),
                (b["sikh"], "shankh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        if t < b["subah"]:
            ghat(ctx, t, 850)
            vratis(ctx, t, (540,), s=1.0, sil=False, lift_t=b["shaam"])
            dv.ribbon(ctx, "PRATYUSHA", 540, 300, t - b["shaam"] - 0.4, size=84, sub="SURYA KI AAKHIRI KIRAN")
        elif t < b["doob"]:
            ghat(ctx, t, lerp(900, 780, ease_in_out(clamp((t - b["subah"]) / 1.5))), morning=True)
            vratis(ctx, t, (540,), s=1.0, sil=False, lift_t=b["subah"])
            dv.ribbon(ctx, "USHA", 540, 300, t - b["subah"] - 0.3, size=90, sub="PEHLI KIRAN")
        else:   # the sun sets and rises again
            k = clamp((t - b["doob"]) / max(b["sikh"] - b["doob"], 1.0))
            sy = 760 + 160 * math.sin(math.pi * k)
            ghat(ctx, t, sy, morning=k > 0.5)
            vratis(ctx, t, (300, 540, 780), s=0.8, lift_t=b["doob"])
            if t > b["sikh"]:
                dv.ribbon(ctx, "BURE WAQT MEIN BHI HAATH JODO", 540, 300, t - b["sikh"] - 0.2, size=54)
        flash(ctx, t - b["subah"], c=(1, 0.95, 0.85), dur=0.4)


class Cta(Cued):
    def beats(self, d):
        c = self.cue
        return {"comment": c("COMMENT", d * 0.5), "jai": c("JAI", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "ghanti"), (b["comment"], "pop"), (b["jai"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        temple_bg(ctx, t)
        dv.devi(ctx, 540, 800, 0.6, t, pose="open")
        dv.diya(ctx, 130, GROUND - 40, 1.1, t)
        dv.diya(ctx, 950, GROUND - 40, 1.1, t + 1)
        comment_card(ctx, t, b["comment"] - 0.3, b["jai"], "JAI CHHATHI MAIYA", y=990)


SCENE_CLASSES = {"hook": Hook, "raja": Raja, "devi": Devi, "vrat": Vrat, "surya": Surya, "rahasya": Rahasya,
                 "cta": Cta}


# ============================================================ upload kit (see upload_kit.py)

UPLOAD = {
    "titles": [
        "Chhath Puja 2026: Why Offer Arghya To The Setting Sun?",
        "Who Is Chhathi Maiya? The Story Behind Chhath Puja",
        "Chhath Puja 2026: Doobte Suraj Ko Arghya Kyon?",
        "Chhath Puja Ki Kahani: Doobte Suraj Ko Arghya Kyon?",
        "Chhathi Maiya Kaun Hain? Chhath Ka Rahasya",
        "Doobte Suraj Ko Arghya Kyon Dete Hain? Chhath Katha",
        "Chhath Ki Pehli Katha: Raja Priyavrat Aur Shashthi Devi",
        "Chhath Puja 2026: Shaam Ka Arghya Kiske Liye?",
        "Pratyusha Aur Usha: Chhath Ke Do Arghya Ka Rahasya",
        "Chhathi Maiya Aur Surya Dev: Bhai-Behen Ki Puja",
        "Chhath Kyon Manate Hain? Poori Katha 1 Minute Mein",
        "Shashthi Se Chhath Kaise Bana? Pauranik Katha",
    ],
    "title": "Chhath Puja 2026: Why Offer Arghya To The Setting Sun?",
    "thumb_text": "DOOBTA SURAJ KYUN?",
    "queries": ["chhath puja 2026", "doobte suraj ko arghya kyon", "chhathi maiya kaun hai"],
    "description": """
Chhath puja ki kahani: doobte suraj ko arghya (jal) kyon diya jaata hai, aur Chhathi Maiya kaun hai?
Raja Priyavrat aur Chhathi (Shashthi) Devi ki katha se samjho Chhath ka rahasya. Chhath Puja 2026: 13-16 November.

Is Short me:
• Raja Priyavrat ke ghar aulaad nahi thi, Rishi Kashyap ne havan karwaya
• Chhathi Devi ka aashirwad: bachcha khilkhila utha
• Kartik mahine ke chhathe din se naam pada Chhath, aur devi kehlaayin Chhathi Maiya
• Log maante hain: Chhathi Maiya Suraj Devta (Surya Dev) ki behen hain
• Shaam ka arghya Pratyusha (aakhiri kiran) ko, subah ka Usha (pehli kiran) ko

Chhath 2026: Nahay Khay 13 Nov, Kharna 14 Nov, Sandhya Arghya 15 Nov, Usha Arghya 16 Nov
(apne local panchang se samay zaroor milaa lein).

Comment me likho: Jai Chhathi Maiya.

Note: ye katha Brahmavaivarta Puran ki parampara se hai; alag jagah Chhath se judi aur kathayein bhi sunaai jaati
hain (Sita, Draupadi, Karna). Pratyusha-Usha wali baat lok maanyata hai.
""",
    "tags": ["chhath puja", "chhath puja ki kahani", "chhathi maiya", "chhath katha", "doobte suraj ko arghya",
             "chhath puja 2026", "sandhya arghya", "shashthi devi", "surya dev", "chhath vrat katha",
             "chhath kyon manate hain", "chhath puja story", "chhath ki kahani", "why arghya to setting sun", "kharna"],
    "hashtags": ["#Shorts", "#ChhathPuja", "#ChhathiMaiya"],
}


def thumbnail(ctx):
    """1080x1920 cover: 'DOOBTA SURAJ / KYUN?' over a dusk ghat with vratis raising their soops."""
    ghat(ctx, 0.3, 800)
    for i in range(10):                      # more diyas floating up the river
        dv.diya(ctx, 80 + 100 * i + 30 * (i % 2), 1290 + 120 * (i % 3) + 40 * rnd(i, 3), 0.6, i)
    vratis(ctx, 0.3, (200, 540, 880), s=1.0, lift_t=-2)
    g = cairo.LinearGradient(0, 0, 0, 640)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.9)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 640)
    ctx.set_source(g)
    ctx.fill()
    text(ctx, "DOOBTA SURAJ", 540, 230, 170, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "KYUN?", 540, 430, 220, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
