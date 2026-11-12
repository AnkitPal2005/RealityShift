"""Sita ji ka pehla Chhath: Munger ke Sita Charan ka rahasya (~50-55s katha, six scenes). For 13 Nov 2026 (Nahay Khay).

Usage (from SanatanKatha/):
  python make.py sita_chhath --preview
  python make.py sita_chhath --kiki-export / --kiki-split --check-voice
  python make.py sita_chhath

Rahasya: who kept the first Chhath vrat? In the Ganga at Munger (Bihar) a rock carries two footprints that people
believe are Sita ji's. The Munger tradition (citing Anand Ramayan): after Lanka, Ram and Sita came to Rishi Mudgal's
ashram to remove the dosh of killing Ravan (a brahmin); the rishi told Sita to worship Surya Dev, and she kept the
vrat on the Ganga bank, offering water to the setting and the rising sun. Where she stood, her feet left their mark:
today's Sita Charan mandir. Told throughout as maanyata / kehte hain, never as history. Ram is not drawn (no rig fits);
Sita = dv.devi, Rishi Mudgal = dv.brahmin. One narrator, KikiVoice L028, one flowing paragraph per scene.
Output: output/shorts/sita_chhath_short.mp4 (+ .json scene log, thumbnail, upload kit)
"""

from core.katha import *  # noqa: F401,F403  (engine helpers, devta as dv, scenery, Cued, story defaults)

TOPIC = "SITA PEHLA CHHATH MUNGER"
OUTPUTS = {"edge": "sita_chhath_short.mp4"}
MUSIC_BPM = 86                      # Sudama 80, Chhath 76

SOURCES = [
    "Munger tradition: Sita performed the first Chhath on the Ganga bank at Munger, as per Anand Ramayan; the site "
    "is the Sita Charan temple with her footprints on a large stone in the river; Rishi Mudgal advised Sita to "
    "worship Surya Dev and Chhathi Maiya after Ravan's killing (DNA India, 'Goddess Sita performed Chhath Puja at "
    "this temple in Munger district'; Wikipedia 'Munger')",
    "Manpatthar (Sita Charan): impression of two feet on a rock in the Ganga, believed to be Sita's, with a small "
    "mandir - Munger district official site, munger.nic.in/tourist-place/manpatthar-sita-charan/",
    "Versions differ: some say Vashishtha sent them to Mudgal, some place the vrat after the return to Ayodhya, "
    "others credit Draupadi, Karna or Priyavrat; this Short tells the Munger belief as 'maanyata hai'",
    "Chhath 2026: Nahay Khay 13 Nov, Kharna 14 Nov, Sandhya Arghya 15 Nov, Usha Arghya 16 Nov (DekhoPanchang)",
]

# KikiVoice: one narrator (L028) tells each scene as ONE flowing paragraph. Plain spoken Hindi, no Latin letters.
SPEC = [
    {"key": "hook", "text": "PEHLA CHHATH?",
     "visual": "Ganga at dusk: a big dark rock mid-river; two footprints on it start to glow; 'PEHLA CHHATH?' ribbon",
     "vo": [("tell", [("छठ का पहला व्रत,", "CHHATH KA PEHLA VRAT,"), ("किसने रखा था?", "KISNE RAKHA THA?"),
                      ("बिहार के मुंगेर में,", "BIHAR KE MUNGER MEIN,"), ("गंगा के बीच", "GANGA KE BEECH"),
                      ("एक पत्थर है।", "EK PATTHAR HAI."), ("उस पर दो पैरों के निशान हैं।", "US PAR DO PAIRON KE NISHAAN HAIN."),
                      ("और लोग मानते हैं,", "AUR LOG MAANTE HAIN,"), ("ये निशान...", "YE NISHAAN..."),
                      ("सीता माँ के हैं।", "SITA MAA KE HAIN.")])]},
    {"key": "lanka", "text": "LANKA KE BAAD",
     "visual": "Night sky over the sea, Lanka's gold towers far away and dim; Sita stands on the shore in a soft glow",
     "vo": [("tell", [("लंका के बाद", "LANKA KE BAAD"), ("राम जी और सीता माँ को,", "RAM JI AUR SITA MAA KO,"),
                      ("रावण वध का दोष मिटाना था।", "RAVAN VADH KA DOSH MITAANA THA."),
                      ("क्योंकि रावण ब्राह्मण था।", "KYUNKI RAVAN BRAHMAN THA.")])]},
    {"key": "rishi", "text": "MUDGAL RISHI",
     "visual": "Forest ashram by the Ganga: Rishi Mudgal under a tree by a havan kund raises his hand to Sita; a sun "
               "glows behind",
     "vo": [("tell", [("तब वो पहुँचे", "TAB WO PAHUNCHE"), ("मुद्गल ऋषि के आश्रम,", "MUDGAL RISHI KE AASHRAM,"),
                      ("जो आज का मुंगेर है।", "JO AAJ KA MUNGER HAI."),
                      ("ऋषि ने सीता माँ से कहा,", "RISHI NE SITA MAA SE KAHA,"),
                      ("सूर्य देव की पूजा करो।", "SURYA DEV KI POOJA KARO.")])]},
    {"key": "vrat", "text": "GANGA KINARE VRAT",
     "visual": "Dusk ghat: Sita waist-deep in the Ganga pours water from a lota to the setting sun; then dawn, the "
               "same to the rising sun",
     "vo": [("tell", [("सीता माँ ने", "SITA MAA NE"), ("गंगा किनारे व्रत रखा।", "GANGA KINARE VRAT RAKHA."),
                      ("शाम को डूबते सूरज को जल चढ़ाया,", "SHAAM KO DOOBTE SURAJ KO JAL CHADHAYA,"),
                      ("और सुबह,", "AUR SUBAH,"), ("उगते सूरज को।", "UGTE SURAJ KO.")])]},
    {"key": "charan", "text": "SITA CHARAN",
     "visual": "The rock in the river: glowing footprints settle into stone; a small white mandir rises on it; "
               "'SITA CHARAN MANDIR' ribbon",
     "vo": [("tell", [("कहते हैं,", "KEHTE HAIN,"), ("जिस पत्थर पर खड़ी होकर", "JIS PATTHAR PAR KHADI HOKAR"),
                      ("जल चढ़ाया,", "JAL CHADHAYA,"), ("उसी पर उनके निशान रह गए।", "USI PAR UNKE NISHAAN REH GAYE."),
                      ("आज वहाँ,", "AAJ WAHAN,"), ("सीता चरण मंदिर है।", "SITA CHARAN MANDIR HAI.")])]},
    {"key": "cta", "text": "JAI CHHATHI MAIYA",
     "visual": "Vratis at a dusk ghat raise their soops; Sita's soft glow in the sky; comment card 'JAI CHHATHI MAIYA'",
     "vo": [("warm", [("इस बार घाट पर", "IS BAAR GHAAT PAR"), ("सूप उठाओ,", "SOOP UTHAO,"),
                      ("याद रखना,", "YAAD RAKHNA,"), ("ये व्रत सीता माँ ने भी रखा था।", "YE VRAT SITA MAA NE BHI RAKHA THA."),
                      ("कमेंट में लिखो,", "COMMENT MEIN LIKHO,"), ("जय छठी मैया।", "JAI CHHATHI MAIYA.")])]},
]
KIKI_TEMPO = {"narrator": 1.0}     # set after --kiki-split --check-voice shows L028's real pace
MAX_GAP = 0.6                      # keep KikiVoice's own "..." beats inside a paragraph

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
SUN = hexc("#FFB347")
WATERC = hexc("#9FE8FF")
HOT = hot_words({"CHHATH": GOLD_HI, "PEHLA": GOLD_HI, "MUNGER": SAFF, "GANGA": WATERC, "PATTHAR": hexc("#C9B8A6"),
                 "NISHAAN": GOLD_HI, "NISHAAN...": GOLD_HI, "SITA": hexc("#FF6B8A"), "LANKA": hexc("#FF9E7A"),
                 "RAM": BLUE, "DOSH": hexc("#FF9E7A"), "RAVAN": hexc("#FF6B6B"), "BRAHMAN": SAFF, "VADH": hexc("#FF6B6B"),
                 "MUDGAL": SAFF, "AASHRAM,": SAFF, "SURYA": SUN, "VRAT": GOLD_HI, "DOOBTE": SUN, "UGTE": hexc("#FFE0A3"),
                 "JAL": WATERC, "CHARAN": GOLD_HI, "MANDIR": GOLD_HI, "SOOP": SAFF, "COMMENT": GOLD_HI, "JAI": GOLD_HI,
                 "CHHATHI": hexc("#FF6B6B"), "MAIYA.": hexc("#FF6B6B")})

WATER = 1090                      # waterline Sita and the vratis stand in
ROCK = (540, 1010)                # the Sita Charan rock, mid-river


# ============================================================ props

def rock(ctx, x, y, s, t, glow_amt=0.0, temple=0.0):
    """The Sita Charan rock in the river: a dark boulder with two footprints that can glow, and a small white mandir
    that rises on top (temple 0..1)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for i in range(5):                                        # ripples around it
        r = 300 + 40 * i + 18 * math.sin(t * 2 + i)
        dv.ell(ctx, 0, 70, r, r * 0.16)
        rgba(ctx, (1, 1, 1), 0.0)
        ctx.fill()
        ctx.set_line_width(3)
        dv.ell(ctx, 0, 70, r, r * 0.16)
        rgba(ctx, hexc("#FFD38A"), 0.25 * (1 - i / 5))
        ctx.stroke()
    dv.smooth(ctx, [(-280, 70), (-250, -40), (-150, -110), (20, -130), (180, -100), (270, -20), (290, 70)])
    dv.ink(ctx, hexc("#5A4A44"), 5)
    dv.smooth(ctx, [(-200, -30), (-120, -90), (40, -105), (170, -70), (200, -20), (0, -10)])
    rgba(ctx, hexc("#7A6A60"), 0.7)
    ctx.fill()
    if temple > 0:                                            # small white mandir with a saffron flag
        k = ease_out_back(clamp(temple))
        ctx.save()
        ctx.translate(150, -110)
        ctx.scale(k, k)
        rrect(ctx, -60, -110, 120, 110, 6)
        dv.ink(ctx, hexc("#F5F0E6"), 4)
        ctx.move_to(-70, -110)
        ctx.line_to(0, -220)
        ctx.line_to(70, -110)
        ctx.close_path()
        dv.ink(ctx, hexc("#FFF8EC"), 4)
        rrect(ctx, -22, -70, 44, 70, 18)
        dv.ink(ctx, hexc("#7A1424"), 3)
        line(ctx, [(0, -220), (0, -280)], GOLD_DK, 4)
        ctx.move_to(0, -280)
        ctx.line_to(56, -262)
        ctx.line_to(0, -244)
        ctx.close_path()
        rgba(ctx, SAFF)
        ctx.fill()
        ctx.restore()
    if glow_amt > 0:
        glow(ctx, -60, -70, 170, GOLD_HI, 0.55 * glow_amt)
    for dx, rot in ((-110, -0.15), (-20, 0.12)):              # two footprints
        c = GOLD_HI if glow_amt > 0 else hexc("#3A2E2A")
        a = 0.5 + 0.5 * glow_amt
        dv.ell(ctx, dx, -60, 26, 46, rot=rot)
        rgba(ctx, c, a)
        ctx.fill()
        for j in range(5):
            dv.ell(ctx, dx - 18 + 9 * j + 50 * math.sin(rot) * 0.3, -116 + 3 * abs(j - 1), 6, 7)
            rgba(ctx, c, a)
            ctx.fill()
    ctx.restore()


def river_dusk(ctx, t, sun_y=820):
    """The open Ganga at dusk (no sugarcane arch, no crowd): sun, far bank, wide water."""
    dv.sky(ctx, hexc("#2B1A4A"), hexc("#E9683F"), hexc("#FFC46B"), 0.42)
    dv.sun_disc(ctx, 820, sun_y, 100, t, rays=16)
    ctx.move_to(0, HORIZON)
    for x in range(0, W + 1, 40):
        ctx.line_to(x, HORIZON - 20 - 14 * math.sin(x / 80) - 10 * math.sin(x / 27))
    ctx.line_to(W, HORIZON + 10)
    ctx.line_to(0, HORIZON + 10)
    ctx.close_path()
    rgba(ctx, hexc("#2A1420"))
    ctx.fill()
    g = cairo.LinearGradient(0, HORIZON, 0, H)
    g.add_color_stop_rgb(0, *hexc("#C2603A"))
    g.add_color_stop_rgb(1, *hexc("#1E1030"))
    ctx.rectangle(0, HORIZON, W, H)
    ctx.set_source(g)
    ctx.fill()
    for i in range(22):
        y = HORIZON + 12 + i * 12
        w = 120 * (1 - i / 26) * (0.7 + 0.3 * math.sin(t * 3 + i))
        line(ctx, [(820 - w, y), (820 + w, y)], hexc("#FFD38A"), 5, 0.5 * (1 - i / 22))


def lanka_night(ctx, t):
    """Sea at night with Lanka's gold towers far off and dim."""
    dv.sky(ctx, hexc("#070A24"), hexc("#1A1A4A"), hexc("#3A1A3A"), 0.6)
    dv.stars(ctx, t)
    for k, (x, h) in enumerate(((760, 210), (840, 300), (920, 180), (690, 150), (990, 130))):
        rrect(ctx, x - 26, HORIZON - h, 52, h, 6)
        dv.ink(ctx, hexc("#8A6A2A"), 3)
        dv.ell(ctx, x, HORIZON - h, 30, 30)
        dv.ink(ctx, hexc("#A07A2A"), 3)
    ctx.rectangle(0, HORIZON, W, H)
    rgba(ctx, hexc("#0C1A3A"))
    ctx.fill()
    for i in range(10):
        y = HORIZON + 20 + i * 18
        line(ctx, [(80 + 40 * (i % 3), y), (1000 - 30 * (i % 2), y)], hexc("#3A5A8A"), 3, 0.3)
    ctx.rectangle(0, GROUND - 40, W, H)
    rgba(ctx, hexc("#C9A16A"))
    ctx.fill()


def ashram(ctx, t):
    """Forest ashram by the Ganga at golden hour: a leaf hut, a tree, a havan kund."""
    dv.sky(ctx, hexc("#F2B36A"), hexc("#FFE0A3"), hexc("#B8D98A"), 0.55)
    dv.sun_disc(ctx, 860, 520, 90, t, rays=16)
    ctx.rectangle(0, HORIZON - 20, W, 120)
    rgba(ctx, hexc("#7FB6C9"))
    ctx.fill()
    ctx.rectangle(0, HORIZON + 80, W, H)
    rgba(ctx, hexc("#7A9A4A"))
    ctx.fill()
    line(ctx, [(180, GROUND), (200, 700), (170, 520)], hexc("#5A3A22"), 34)       # tree
    for k in range(6):
        circle(ctx, 120 + 70 * (k % 3), 470 + 60 * (k // 3) - 20 * (k % 2), 90, hexc("#3E7A3A"), 0.95)
    ctx.move_to(780, GROUND)                                                     # leaf hut
    ctx.line_to(780, 980)
    ctx.line_to(1060, 980)
    ctx.line_to(1060, GROUND)
    ctx.close_path()
    dv.ink(ctx, hexc("#B9875A"))
    ctx.move_to(740, 990)
    ctx.line_to(920, 840)
    ctx.line_to(1100, 990)
    ctx.close_path()
    dv.ink(ctx, hexc("#C9A24A"))
    ctx.rectangle(0, GROUND - 20, W, H)
    rgba(ctx, hexc("#8A6A40"))
    ctx.fill()


def sita_in_river(ctx, x, t, pour=0.0, a=1.0, s=0.78):
    """Sita (devi rig) standing waist-deep, lota raised to the sun, water in front of her waist."""
    dv.devi(ctx, x, WATER + 300 * s, s, t, pose="open", a=a, aura=False)
    dv.lota(ctx, x + 150 * s, WATER - 200 * s, 0.8, tilt=0.6 * pour, pour=pour, t=t, a=a)
    ctx.rectangle(0, WATER, W, 160)
    rgba(ctx, hexc("#2A1224"), 0.6)
    ctx.fill()


# ============================================================ scenes

class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"q": c("KISNE", d * 0.12), "munger": c("MUNGER", d * 0.3), "nishaan": c("PAIRON", d * 0.55),
                "sita": c("SITA", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "ghanti"), (b["q"], "thud"), (b["munger"], "whoosh"), (b["nishaan"], "shimmer"),
                (b["sita"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        river_dusk(ctx, t)
        z = 1.0 + 0.25 * ease_in_out(clamp((t - b["munger"]) / max(d - b["munger"], 1.0)))
        rock(ctx, ROCK[0], ROCK[1], 1.15 * z, t, glow_amt=clamp((t - b["nishaan"]) / 0.6))
        if t > b["sita"]:
            glow(ctx, 540, 520, 260, hexc("#FF8FB0"), 0.4 * clamp((t - b["sita"]) / 0.5))
        flash(ctx, t - b["sita"], c=(1, 0.95, 0.8), dur=0.5)
        if t < b["munger"]:
            dv.ribbon(ctx, "PEHLA CHHATH?", 540, 300, t - b["q"], size=88)
        else:
            dv.ribbon(ctx, "MUNGER, BIHAR", 540, 300, t - b["munger"], size=80, sub="GANGA KE BEECH EK PATTHAR")


class Lanka(Cued):
    def beats(self, d):
        c = self.cue
        return {"lanka": c("LANKA", d * 0.12), "dosh": c("DOSH", d * 0.45), "ravan": c("RAVAN", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["lanka"], "whoosh"), (b["dosh"], "thud"), (b["ravan"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        lanka_night(ctx, t)
        glow(ctx, 360, 820, 300, hexc("#FFB3C7"), 0.35)
        dv.devi(ctx, 360, GROUND, 0.72, t, pose="bless", a=clamp(t / 0.5), aura=False)
        if t > b["ravan"]:
            dv.balance(ctx, 800, 560, 0.55, -0.3 * ease_out_back(clamp((t - b["ravan"]) / 0.6)), t,
                       labels=("VIJAY", "DOSH"), a=clamp((t - b["ravan"]) / 0.4))
        if t < b["dosh"]:
            dv.ribbon(ctx, "LANKA KE BAAD", 540, 300, t - b["lanka"], size=84)
        else:
            dv.ribbon(ctx, "EK DOSH", 540, 300, t - b["dosh"], size=88, sub="RAVAN BRAHMAN THA")


class Rishi(Cued):
    def beats(self, d):
        c = self.cue
        return {"mudgal": c("MUDGAL", d * 0.12), "munger": c("MUNGER", d * 0.35), "pooja": c("SURYA", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "ghanti"), (b["mudgal"], "pop"), (b["munger"], "shimmer"), (b["pooja"], "shankh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        ashram(ctx, t)
        dv.yagya_kund(ctx, 520, GROUND - 10, 0.6, t)
        dv.brahmin(ctx, 300, GROUND, 0.74, t, pose="point" if t > b["pooja"] else "stand", mood="smile",
                   look=(0.8, 0))
        dv.devi(ctx, 800, GROUND, 0.72, t, pose="bless", flip=True, aura=False)
        if t > b["pooja"]:
            glow(ctx, 860, 520, 240, SUN, 0.5 * clamp((t - b["pooja"]) / 0.5))
        if t < b["munger"]:
            dv.ribbon(ctx, "MUDGAL RISHI", 540, 300, t - b["mudgal"], size=84)
        else:
            dv.ribbon(ctx, "AAJ KA MUNGER", 540, 300, t - b["munger"], size=84)


class Vrat(Cued):
    def beats(self, d):
        c = self.cue
        return {"shaam": c("SHAAM", d * 0.3), "subah": c("SUBAH", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "ghanti"), (b["shaam"], "shimmer"), (b["subah"], "whoosh"), (b["subah"] + 0.3, "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        morning = t > b["subah"]
        if morning:
            sy = lerp(900, 760, ease_in_out(clamp((t - b["subah"]) / 1.2)))
        else:
            sy = lerp(700, 860, ease_in_out(clamp(t / max(b["subah"], 1.0))))
        ghat(ctx, t, sy, morning=morning, diyas=not morning)
        pour = clamp((t - (b["subah"] if morning else b["shaam"])) / 0.5)
        sita_in_river(ctx, 540, t, pour=pour)
        flash(ctx, t - b["subah"], c=(1, 0.95, 0.85), dur=0.4)
        if morning:
            dv.ribbon(ctx, "UGTE SURAJ KO", 540, 300, t - b["subah"], size=80)
        elif t > b["shaam"]:
            dv.ribbon(ctx, "DOOBTE SURAJ KO", 540, 300, t - b["shaam"], size=80)
        else:
            dv.ribbon(ctx, "GANGA KINARE VRAT", 540, 300, t - 0.2, size=76)


class Charan(Cued):
    def beats(self, d):
        c = self.cue
        return {"patthar": c("PATTHAR", d * 0.15), "nishaan": c("NISHAAN", d * 0.5), "mandir": c("MANDIR", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["nishaan"], "shimmer"), (b["mandir"], "shankh"), (b["mandir"] + 0.05, "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        river_dusk(ctx, t, sun_y=840)
        g = clamp((t - b["nishaan"]) / 0.5) * (1 - 0.4 * clamp((t - b["mandir"]) / 0.6))
        if b["patthar"] < t < b["nishaan"]:      # Sita's light fades onto the rock
            glow(ctx, ROCK[0] - 60, ROCK[1] - 160, 220, hexc("#FFB3C7"), 0.5 * clamp((t - b["patthar"]) / 0.4))
        rock(ctx, ROCK[0], ROCK[1] - 40, 1.4, t, glow_amt=g, temple=clamp((t - b["mandir"]) / 0.5))
        if t > b["mandir"]:
            dv.petals(ctx, t - b["mandir"], 26, seed=5)
            dv.ribbon(ctx, "SITA CHARAN MANDIR", 540, 300, t - b["mandir"], size=76)
        else:
            dv.ribbon(ctx, "PAIRON KE NISHAAN", 540, 300, t - b["nishaan"], size=78)


class Cta(Cued):
    def beats(self, d):
        c = self.cue
        return {"soop": c("SOOP", d * 0.2), "comment": c("COMMENT", d * 0.7), "jai": c("JAI", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "ghanti"), (b["soop"], "shimmer"), (b["comment"], "pop"), (b["jai"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        ghat(ctx, t, 830)
        glow(ctx, 540, 520, 300, hexc("#FFB3C7"), 0.35)
        dv.devi(ctx, 540, 700, 0.4, t, pose="open", a=0.8)
        for k, x in enumerate((200, 540, 880)):
            lift = ease_in_out(clamp((t - b["soop"] - 0.15 * k) / 0.8))
            dv.vrati(ctx, x, WATER + 10 * (k % 2), 0.78, t + k, lift=lift)
        ctx.rectangle(0, WATER, W, 120)
        rgba(ctx, hexc("#2A1224"), 0.55)
        ctx.fill()
        if t < b["comment"] - 0.3:
            dv.ribbon(ctx, "SITA MAA KA VRAT", 540, 300, t - 0.2, size=80)
        comment_card(ctx, t, b["comment"] - 0.3, b["jai"], "JAI CHHATHI MAIYA", y=1000)


SCENE_CLASSES = {"hook": Hook, "lanka": Lanka, "rishi": Rishi, "vrat": Vrat, "charan": Charan, "cta": Cta}


# ============================================================ upload kit (see upload_kit.py)

UPLOAD = {
    "titles": [
        "Chhath Ka Pehla Vrat Kisne Rakha Tha? Sita Maa Aur Munger",
        "Sita Maa Ne Kiya Tha Pehla Chhath? Munger Ka Rahasya",
        "Ganga Ke Beech Sita Maa Ke Pairon Ke Nishaan | Chhath Puja 2026",
        "Sita Charan Mandir Munger: Chhath Ki Ankahi Katha",
        "Who Did The First Chhath Puja? Sita Maa In Munger",
        "Chhath Puja 2026: Sita Maa Ka Pehla Chhath",
        "Munger Ke Patthar Par Sita Maa Ke Charan Kyun?",
        "Chhath Ki Kahani: Sita Maa Aur Mudgal Rishi",
        "Ram Sita Ne Munger Mein Chhath Kyun Kiya?",
        "Sita Maa Ke Pairon Ke Nishaan Aaj Bhi Ganga Mein",
    ],
    "title": "Munger Ke Patthar Par Sita Maa Ke Charan Kyun?",
    "thumb_text": "PEHLA CHHATH?",
    "queries": ["chhath puja ki kahani", "sita charan mandir munger", "chhath ka pehla vrat kisne rakha"],
    "description": """
Chhath puja ki kahani: Chhath ka pehla vrat kisne rakha tha? Munger (Bihar) mein Ganga ke beech Sita Charan mandir,
jahan patthar par Sita Maa ke pairon ke nishaan maane jaate hain.

Is Short me:
• Lanka ke baad, Ravan vadh ka dosh mitaane ki baat
• Mudgal Rishi ka aashram, aaj ka Munger
• Sita Maa ne Ganga kinare doobte aur ugte suraj ko jal chadhaya
• Sita Charan mandir: patthar par pairon ke nishaan

Chhath 2026: Nahay Khay 13 Nov, Kharna 14 Nov, Sandhya Arghya 15 Nov, Usha Arghya 16 Nov
(apne local panchang se samay zaroor milaa lein).

Comment me likho: Jai Chhathi Maiya.

Note: ye Munger ki lok maanyata hai (Anand Ramayan ka hawala diya jaata hai); Chhath se judi aur kathayein bhi hain
(Raja Priyavrat, Draupadi, Karna).
""",
    "tags": ["chhath puja", "chhath puja ki kahani", "sita charan mandir", "munger", "sita maa chhath",
             "chhath puja 2026", "pehla chhath", "chhathi maiya", "mudgal rishi", "chhath katha", "nahay khay",
             "bihar chhath", "ganga", "divya rahasya", "chhath vrat katha"],
    "hashtags": ["#Shorts", "#ChhathPuja", "#SitaMaa"],
}


def thumbnail(ctx):
    """1080x1920 cover: 'PEHLA / CHHATH?' over the river rock with Sita's glowing footprints and Sita above."""
    river_dusk(ctx, 0.3, sun_y=800)
    glow(ctx, 540, 760, 360, hexc("#FFB3C7"), 0.4)
    dv.devi(ctx, 540, 1000, 0.62, 0.3, pose="open", aura=True)
    rock(ctx, 540, 1400, 1.7, 0.3, glow_amt=1.0)
    g = cairo.LinearGradient(0, 0, 0, 640)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.9)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 640)
    ctx.set_source(g)
    ctx.fill()
    text(ctx, "PEHLA", 540, 230, 200, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "CHHATH?", 540, 440, 210, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
