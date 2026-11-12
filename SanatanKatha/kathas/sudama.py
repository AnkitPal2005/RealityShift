"""Sudama ki potli: Krishna ne doosri mutthi kyun nahi khayi? (~52-55s katha, eight scenes). Made 12 Nov 2026.
Rewritten 12 Nov to the master brief: one narrator (KikiVoice L028), ~137 words, ~650 chars (Kiki limit 1000).

Usage (from SanatanKatha/):
  python make.py sudama --preview
  python make.py sudama --kiki-export / --kiki-split --check-voice
  python make.py sudama

Rahasya: a poor brahmin walks to Dwarka with a handful of borrowed rice, asks for nothing, and comes home to find his
hut turned into a palace. Why? Krishna ate one handful; as he lifted the next, Rukmini held his hand - that one handful
had already given Sudama everything (Bhagavata Purana 10.81). The tears washing his feet are from the folk poem
'Sudama Charit' (Narottamdas), said as "kehte hain". Characters: Sudama = dv.brahmin, his wife = katha.mother,
Rukmini = dv.devi. Nothing graphic. KikiVoice style: one flowing paragraph per scene.
Output: output/shorts/sudama_short.mp4 (+ .json scene log, thumbnail, upload kit)
"""

from core.katha import *  # noqa: F401,F403  (engine helpers, devta as dv, scenery, Cued, story defaults)

TOPIC = "SUDAMA KRISHNA POTLI CHAWAL"
OUTPUTS = {"edge": "sudama_short.mp4"}
MUSIC_BPM = 80                      # Karna was 88

SOURCES = [
    "Sudama (Kuchela): Krishna's poor brahmin friend from Sandipani's gurukul; his wife urges him to visit Dwarka; he "
    "carries a few handfuls of flattened rice (chivda/poha) wrapped in cloth; Krishna runs to meet him, washes his "
    "feet, eats one handful, and Rukmini stops his hand at the next, saying that one handful already grants all "
    "wealth in this world and the next; Sudama asks for nothing and returns to find a palace - Bhagavata Purana, "
    "Canto 10, ch. 80-81 (Wikipedia 'Sudama')",
    "Krishna washing Sudama's feet with his tears ('nainan ke jal son pag dhoye') is from the 16th-century Awadhi "
    "poem 'Sudama Charit' by Narottamdas - told as 'kehte hain' (Wikipedia 'Narottamdas')",
    "Folk retellings say each handful gave Sudama a whole lok (two lokas, the third would be Krishna's own); this "
    "Short keeps the Bhagavata count (one handful eaten, the second stopped) and says it as 'kehte hain'",
]

# KikiVoice: one narrator (L028) tells each scene as ONE flowing paragraph; no character voices in this cut.
# Pure Hindi, no dashes, no hyphenated words, no Latin letters in the spoken text.
SPEC = [
    {"key": "hook", "text": "BINA MAANGE?",
     "visual": "Village road at dawn: thin Sudama with a tiny potli walks toward Dwarka's gold domes; then his broken "
               "hut flashes into a golden palace; 'BINA MAANGE?' ribbon",
     "vo": [("tell", [("एक गरीब ब्राह्मण,", "EK GAREEB BRAHMAN,"), ("मुट्ठी भर चावल लेकर", "MUTTHI BHAR CHAWAL LEKAR"),
                      ("द्वारका गया।", "DWARKA GAYA."), ("लौटा, तो उसकी झोपड़ी", "LAUTA, TO USKI JHOPDI"),
                      ("महल बन चुकी थी।", "MAHAL BAN CHUKI THI."), ("जबकि उसने", "JABKI USNE"),
                      ("कुछ माँगा ही नहीं था।", "KUCHH MAANGA HI NAHI THA.")])]},
    {"key": "who", "text": "SUDAMA",
     "visual": "Split: Krishna on a gold throne in Dwarka (left glow) vs Sudama at his cracked hut with an empty pot",
     "vo": [("tell", [("ये थे सुदामा,", "YE THE SUDAMA,"), ("कृष्ण के बचपन के दोस्त।", "KRISHNA KE BACHPAN KE DOST."),
                      ("पर इतने गरीब,", "PAR ITNE GAREEB,"), ("कि घर में कई बार", "KI GHAR MEIN KAI BAAR"),
                      ("चूल्हा भी नहीं जलता था।", "CHULHA BHI NAHI JALTA THA.")])]},
    {"key": "patni", "text": "THODE SE CHAWAL",
     "visual": "Inside the hut by a diya: his wife asks him to go; she ties a little rice into a cloth potli",
     "vo": [("tell", [("पत्नी के कहने पर,", "PATNI KE KEHNE PAR,"), ("वो पोटली में", "WO POTLI MEIN"),
                      ("थोड़े चावल बाँधकर", "THODE CHAWAL BAANDHKAR"), ("द्वारका चले।", "DWARKA CHALE.")])]},
    {"key": "milan", "text": "NANGE PAANV DAUDE",
     "visual": "Dwarka palace gate: Krishna runs barefoot from the throne to Sudama; they embrace in a burst of petals",
     "vo": [("tell", [("खबर मिलते ही", "KHABAR MILTE HI"), ("कृष्ण नंगे पाँव दौड़े आए,", "KRISHNA NANGE PAANV DAUDE AAYE,"),
                      ("और गले लगा लिया।", "AUR GALE LAGA LIYA.")])]},
    {"key": "potli", "text": "DOOSRI MUTTHI...",
     "visual": "Sudama hides the potli behind his back; Krishna smiles and opens it; rice grains glow",
     "vo": [("tell", [("सुदामा पोटली छुपा रहे थे,", "SUDAMA POTLI CHHUPA RAHE THE,"),
                      ("पर कृष्ण ने खुद खोल ली।", "PAR KRISHNA NE KHUD KHOL LI."),
                      ("एक मुट्ठी चावल खाए।", "EK MUTTHI CHAWAL KHAAYE."), ("दूसरी उठाई,", "DOOSRI UTHAYI,")])]},
    {"key": "rukmini", "text": "EK MUTTHI = SAB KUCHH",
     "visual": "Rukmini steps in and gently holds Krishna's wrist; the handful glows; a gold balance: EK MUTTHI vs "
               "SAB KUCHH",
     "vo": [("tell", [("तो रुक्मिणी जी ने", "TO RUKMINI JI NE"), ("हाथ थाम लिया।", "HAATH THAAM LIYA."),
                      ("क्यों?", "KYUN?"), ("मान्यता है,", "MAANYATA HAI,"),
                      ("उस एक मुट्ठी के बदले", "US EK MUTTHI KE BADLE"),
                      ("कृष्ण सब कुछ दे चुके थे।", "KRISHNA SAB KUCHH DE CHUKE THE.")])]},
    {"key": "ghar", "text": "SAB BADAL GAYA",
     "visual": "Sudama walks home empty-handed and smiling; at the village the cracked hut is gone, a golden palace "
               "stands",
     "vo": [("tell", [("सुदामा खाली हाथ लौटे।", "SUDAMA KHAALI HAATH LAUTE."), ("पर गाँव पहुँचे,", "PAR GAANV PAHUNCHE,"),
                      ("तो सब बदल चुका था।", "TO SAB BADAL CHUKA THA.")])]},
    {"key": "cta", "text": "SACHCHA DOST",
     "visual": "Krishna and Sudama side by side in soft light; comment card 'JAI SHRI KRISHNA'",
     "vo": [("warm", [("सच्चा दोस्त वही,", "SACHCHA DOST WAHI,"), ("जो बिना कहे समझ जाए।", "JO BINA KAHE SAMAJH JAAYE."),
                      ("ऐसे दोस्त को ये भेजो,", "AISE DOST KO YE BHEJO,"), ("और लिखो,", "AUR LIKHO,"),
                      ("जय श्री कृष्ण।", "JAI SHRI KRISHNA.")])]},
]
KIKI_TEMPO = {"narrator": 1.0}   # one voice now (L028); set after --kiki-split --check-voice shows the real pace
MAX_GAP = 0.6      # keep KikiVoice's own "..." beats inside a paragraph

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
RICE = hexc("#FFF4D6")
HOT = hot_words({"GAREEB": hexc("#FF9E7A"), "CHAWAL": RICE, "DWARKA": GOLD_HI, "TOOTI": hexc("#FF9E7A"),
                 "MAHAL": GOLD_HI, "MAANGA": GOLD_HI, "SUDAMA": SAFF, "SUDAMA.": SAFF, "KRISHNA": BLUE,
                 "GURUKUL": GOLD_HI, "RAJA": GOLD_HI, "GHANA": SAFF, "DAANA": RICE, "PATNI": hexc("#FFB3C7"),
                 "MITRA": GOLD_HI, "KHAALI": hexc("#FF9E7A"), "POTLI": SAFF, "NANGE": GOLD_HI, "DAUD": GOLD_HI,
                 "AANSUON": hexc("#9FE8FF"), "SHARAM": hexc("#FFB3C7"), "BHABHI": hexc("#FFB3C7"), "MUTTHI": RICE,
                 "DOOSRI": GOLD_HI, "RUKMINI": hexc("#FF6B8A"), "KYUN": GOLD_HI, "SAB": GOLD_HI, "KUCHH": GOLD_HI,
                 "SONE": GOLD_HI, "SACHCHA": GOLD_HI, "DOST": GOLD_HI, "BACHPAN": GOLD_HI, "CHULHA": hexc("#FF9E7A"),
                 "BADAL": GOLD_HI, "KHOL": GOLD_HI, "MAANYATA": GOLD_HI, "THAAM": hexc("#FF6B8A"), "LIKHO": GOLD_HI, "BHAI": SAFF, "COMMENT": GOLD_HI,
                 "JAI": GOLD_HI, "SHRI": GOLD_HI})


# ============================================================ props

def village(ctx, t, dusk=False):
    """Dry village fields under a pale sky."""
    if dusk:
        dv.sky(ctx, hexc("#3A1A3A"), hexc("#D9774A"), hexc("#5A2A1A"), 0.6)
    else:
        dv.sky(ctx, hexc("#9CC9E8"), hexc("#F6DDB0"), hexc("#E2B07A"), 0.6)
    for k, (c, yy) in enumerate(((hexc("#C9A16A"), 1000), (hexc("#A88250"), 1080))):
        ctx.move_to(0, yy)
        for x in range(0, W + 1, 60):
            ctx.line_to(x, yy - 24 * math.sin(x / 190 + k * 1.3))
        ctx.line_to(W, H)
        ctx.line_to(0, H)
        ctx.close_path()
        rgba(ctx, c)
        ctx.fill()
    ctx.rectangle(0, GROUND - 20, W, H)
    rgba(ctx, hexc("#8A6A40"))
    ctx.fill()
    for i in range(24):
        x = rnd(i, 21) * W
        y = GROUND + 50 * rnd(i, 22)
        line(ctx, [(x, y), (x - 5, y - 16)], hexc("#6A5030"), 3)


def hut(ctx, x, y, s, a=1.0):
    """Sudama's poor hut: cracked mud wall, sagging thatch with a gap, a crooked door."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.push_group()
    rrect(ctx, -220, -300, 440, 300, 10)
    dv.ink(ctx, hexc("#B9875A"))
    for pts in (((-150, -260), (-120, -200), (-140, -150)), ((120, -240), (150, -190), (130, -120))):
        line(ctx, list(pts), hexc("#6A4428"), 5)
    dv.smooth(ctx, [(-280, -280), (0, -470), (280, -280), (240, -260), (0, -420), (-240, -260)], k=0.05)
    dv.ink(ctx, hexc("#C9A24A"))
    for k in range(9):
        line(ctx, [(-250 + 60 * k, -290), (-200 + 50 * k, -380)], hexc("#9A7A30"), 4)
    dv.smooth(ctx, [(60, -400), (110, -360), (90, -350)], k=0.1)     # gap in the thatch
    rgba(ctx, hexc("#3A2A1A"))
    ctx.fill()
    ctx.move_to(-50, 0)
    ctx.line_to(-46, -170)
    ctx.line_to(56, -160)
    ctx.line_to(50, 0)
    ctx.close_path()
    dv.ink(ctx, hexc("#5A3A22"))
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(a)
    ctx.restore()


def gold_palace(ctx, x, y, s, t, a=1.0):
    """The palace that stands where the hut was: gold walls, three domes, a glowing door."""
    if a <= 0:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.push_group()
    glow(ctx, 0, -300, 520, GOLD_HI, 0.5)
    rrect(ctx, -330, -360, 660, 360, 12)
    dv.ink(ctx, GOLD)
    for k, (dx, r) in enumerate(((-220, 90), (0, 140), (220, 90))):
        dv.ell(ctx, dx, -360 - r * 0.55, r, r)
        dv.ink(ctx, GOLD_HI if k == 1 else GOLD)
        line(ctx, [(dx, -360 - r * 1.5), (dx, -360 - r * 1.9)], GOLD_DK, 8)
        circle(ctx, dx, -360 - r * 1.95, 12, dv.RED_GEM)
    for dx in (-220, 220):
        rrect(ctx, dx - 50, -280, 100, 130, 40)
        dv.ink(ctx, hexc("#7A1424"), 4)
    ctx.move_to(-70, 0)
    ctx.line_to(-70, -170)
    ctx.curve_to(-70, -250, 70, -250, 70, -170)
    ctx.line_to(70, 0)
    ctx.close_path()
    dv.ink(ctx, hexc("#FFF2B8"))
    line(ctx, [(-330, -40), (330, -40)], GOLD_DK, 6)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(a)
    ctx.restore()
    for i in range(8):     # sparkles
        ph = (t * 1.3 + rnd(i, 30)) % 1
        circle(ctx, x + s * (-320 + 640 * rnd(i, 31)), y - s * (80 + 520 * rnd(i, 32)), 6 * (1 - ph), (1, 1, 0.9), a * (1 - ph))


def dwarka_far(ctx, x, y, s):
    """Distant Dwarka: gold domes shining on the horizon."""
    glow(ctx, x, y - 60 * s, 260 * s, GOLD_HI, 0.6)
    for dx, r in ((-90, 40), (0, 64), (90, 40)):
        dv.ell(ctx, x + dx * s, y - r * s, r * s, r * s)
        dv.ink(ctx, GOLD, 3)
    rrect(ctx, x - 140 * s, y - 20 * s, 280 * s, 40 * s, 6)
    dv.ink(ctx, GOLD_DK, 3)


def potli(ctx, x, y, s, open_=0.0, t=0.0):
    """Small cloth bundle tied at the top; open_ (0..1) unties it and shows glowing rice."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if open_ > 0:
        glow(ctx, 0, -20, 120, GOLD_HI, 0.6 * open_)
        dv.ell(ctx, 0, 0, 80 + 30 * open_, 46 - 10 * open_)
        dv.ink(ctx, hexc("#B5541A"), 4)
        for i in range(18):
            gx = -60 * open_ + 120 * open_ * rnd(i, 40)
            gy = -16 + 24 * rnd(i, 41)
            dv.ell(ctx, gx, gy, 7, 4, rot=rnd(i, 42) * 3)
            rgba(ctx, RICE)
            ctx.fill()
    else:
        dv.smooth(ctx, [(-60, 20), (-70, -20), (-30, -50), (-12, -70), (12, -70), (30, -50), (70, -20), (60, 20),
                        (0, 34)])
        dv.ink(ctx, hexc("#C8642A"), 4)
        line(ctx, [(-24, -48), (24, -48)], hexc("#7A3A12"), 6)
        dv.smooth(ctx, [(-10, -70), (-24, -96), (0, -84), (24, -96), (10, -70)], k=0.1)
        dv.ink(ctx, hexc("#C8642A"), 3)
    ctx.restore()


def rice_fly(ctx, x0, y0, x1, y1, u, n=10):
    """A handful of rice grains arcing from (x0, y0) to (x1, y1) over 0.6 s."""
    if not 0 < u < 0.8:
        return
    k = clamp(u / 0.6)
    for i in range(n):
        x = lerp(x0, x1, k) + 20 * (rnd(i, 50) - 0.5)
        y = lerp(y0, y1, k) - 140 * math.sin(math.pi * k) + 20 * (rnd(i, 51) - 0.5)
        dv.ell(ctx, x, y, 7, 4)
        rgba(ctx, RICE, 1 - clamp((u - 0.6) / 0.2))
        ctx.fill()


def tears(ctx, x, y, u, n=6):
    """Blue tear drops falling from (x, y) into a gold thaal below."""
    for i in range(n):
        ph = (u * 1.1 + i / n) % 1
        if u <= 0:
            return
        circle(ctx, x + 10 * math.sin(i * 2.1), y + 260 * ph, 9, hexc("#9FE8FF"), 0.9 * (1 - ph * 0.6))


def thaal(ctx, x, y, s=1.0):
    dv.ell(ctx, x, y, 130 * s, 30 * s)
    dv.ink(ctx, GOLD, 4)
    dv.ell(ctx, x, y - 4 * s, 96 * s, 18 * s)
    rgba(ctx, hexc("#9FE8FF"), 0.7)
    ctx.fill()


def hut_inside(ctx, t):
    """Inside the hut by night: mud walls, a single diya, an empty pot."""
    dv.sky(ctx, hexc("#1A0E08"), hexc("#3A2414"), hexc("#140A06"), 0.5)
    glow(ctx, 540, 1000, 520, hexc("#FFB347"), 0.35)
    for k in range(5):
        line(ctx, [(0, 300 + 180 * k), (W, 320 + 180 * k)], hexc("#4A2E1A"), 3, 0.5)
    ctx.rectangle(0, GROUND - 30, W, H)
    rgba(ctx, hexc("#2A1A0E"))
    ctx.fill()
    dv.diya(ctx, 540, GROUND - 40, 1.0, t)


def empty_pot(ctx, x, y, s=1.0):
    dv.smooth(ctx, [(x - 70 * s, y), (x - 90 * s, y - 70 * s), (x - 50 * s, y - 120 * s), (x + 50 * s, y - 120 * s),
                    (x + 90 * s, y - 70 * s), (x + 70 * s, y)])
    dv.ink(ctx, hexc("#9A4A22"), 4)
    dv.ell(ctx, x, y - 120 * s, 50 * s, 12 * s)
    rgba(ctx, hexc("#2A1408"))
    ctx.fill()


def rukmini(ctx, x, y, s, t, pose="bless", a=1.0, flip=False):
    """Rukmini ji: the devi rig (red saree, mukut) with a soft pink aura."""
    glow(ctx, x, y - 560 * s, 320 * s, hexc("#FF8FB0"), 0.35 * a)
    dv.devi(ctx, x, y, s, t, pose=pose, a=a, flip=flip, aura=False)


# ============================================================ scenes

class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"dwarka": c("DWARKA", d * 0.25), "lauta": c("LAUTA", d * 0.45), "mahal": c("MAHAL", d * 0.6),
                "maanga": c("MAANGA", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "ghanti"), (b["dwarka"], "shimmer"), (b["lauta"], "whoosh"), (b["mahal"], "boom"),
                (b["maanga"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        if t < b["lauta"]:
            village(ctx, t)
            dwarka_far(ctx, 860, 980, 1.0)
            k = clamp(t / max(b["lauta"], 1))
            x = lerp(260, 560, k)
            dv.brahmin(ctx, x, GROUND, 0.72, t, pose="stand", mood="look", look=(0.8, -0.1))
            potli(ctx, x + 108 * 0.72, GROUND - 300 * 0.72, 0.5)
        else:
            u = t - b["lauta"]
            village(ctx, t, dusk=True)
            m = clamp((t - b["mahal"]) / 0.5)
            hut(ctx, 540, GROUND - 10, 1.2, a=1 - m)
            gold_palace(ctx, 540, GROUND - 10, 1.05, t, a=m)
            dv.brahmin(ctx, 220, GROUND, 0.62, t, pose="point" if m > 0 else "stand", mood="look", look=(1, -0.2),
                       a=clamp(u / 0.3))
            flash(ctx, t - b["mahal"], c=(1, 0.95, 0.7), dur=0.5)
        dv.ribbon(ctx, "BINA MAANGE?", 540, 300, t - b["maanga"], size=88)


class Who(Cued):
    def beats(self, d):
        c = self.cue
        return {"name": c("SUDAMA", d * 0.1), "raja": c("KRISHNA", d * 0.3), "gareeb": c("GAREEB", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["name"], "ghanti"), (b["raja"], "shimmer"), (b["gareeb"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        village(ctx, t)
        hut(ctx, 760, GROUND - 10, 0.9)
        empty_pot(ctx, 980, GROUND + 10, 0.7)
        dv.brahmin(ctx, 560, GROUND, 0.7, t, pose="stand", mood="look", look=(-0.4, 0))
        if t > b["raja"]:                       # the friend far away: Krishna glowing in a gold window
            u = t - b["raja"]
            k = ease_out_back(clamp(u / 0.4))
            ctx.save()
            ctx.translate(250, 640)
            ctx.scale(k, k)
            circle(ctx, 0, 0, 200, hexc("#2A0A14"), 0.92)
            glow(ctx, 0, 0, 210, GOLD_HI, 0.6)
            ctx.arc(0, 0, 190, 0, math.tau)
            ctx.clip()
            dv.krishna(ctx, 0, 330, 0.5, t, pose="bless")
            ctx.restore()
            if u > 0.3:
                text(ctx, "DWARKA KE RAJA", 250, 880, 46, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
                     stroke_w=10)
        dv.ribbon(ctx, "SUDAMA", 540, 300, t - b["name"], size=96, sub="KRISHNA KE BACHPAN KE DOST")


class Patni(Cued):
    def beats(self, d):
        c = self.cue
        return {"kaha": c("PATNI", d * 0.05), "khaali": c("POTLI", d * 0.4), "potli": c("CHAWAL", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["kaha"], "pop"), (b["khaali"], "thud"), (b["potli"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        hut_inside(ctx, t)
        mother(ctx, 300, GROUND, 0.75, t)
        dv.brahmin(ctx, 800, GROUND, 0.72, t, pose="stand", mood="look", look=(-0.7, 0), flip=True)
        if b["kaha"] < t < b["khaali"]:
            bubble(ctx, "EK BAAR MIL AAIYE", 520, 560, t - b["kaha"], (360, 700))
        if t > b["potli"] - 0.2:
            potli(ctx, 540, GROUND - 120, 0.9)
            dv.ribbon(ctx, "THODE SE CHAWAL", 540, 300, t - b["potli"], size=80)


class Milan(Cued):
    def beats(self, d):
        c = self.cue
        return {"aaya": c("KHABAR", d * 0.05), "daud": c("NANGE", d * 0.3), "gale": c("GALE", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "ghanti"), (b["aaya"], "pop"), (b["daud"], "whoosh"), (b["gale"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        palace(ctx, t)
        k = ease_in_out(clamp((t - b["daud"]) / 0.9))
        kx = lerp(980, 640, k)
        dv.brahmin(ctx, 360, GROUND, 0.72, t, pose="stand", mood="smile" if t > b["gale"] else "look",
                   look=(0.8, 0))
        dv.krishna(ctx, kx, GROUND, 0.74, t, pose="ask" if t > b["gale"] else "bless", flip=True)
        if t > b["gale"]:
            glow(ctx, 500, 760, 300, hexc("#FFB3C7"), 0.35)
            dv.petals(ctx, t - b["gale"], 24, seed=3)
        if t < b["gale"]:
            dv.ribbon(ctx, "SUDAMA AAYA HAI", 540, 300, t - b["aaya"], size=80)
        else:
            dv.ribbon(ctx, "NANGE PAANV DAUDE", 540, 300, t - b["gale"], size=80)


class Potli(Cued):
    def beats(self, d):
        c = self.cue
        return {"bhabhi": c("KRISHNA", d * 0.3), "khol": c("KHOL", d * 0.45), "kha": c("KHAAYE", d * 0.65),
                "doosri": c("DOOSRI", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["bhabhi"], "pop"), (b["khol"], "shimmer"), (b["kha"], "ghanti"),
                (b["doosri"], "whoosh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        palace(ctx, t)
        dv.brahmin(ctx, 330, GROUND, 0.74, t, pose="stand", mood="look", look=(0.6, 0.2))
        dv.krishna(ctx, 760, GROUND, 0.76, t, pose="ask" if t > b["bhabhi"] else "bless", flip=True)
        if t < b["khol"]:                       # hidden behind Sudama, the corner peeking out
            potli(ctx, 200, GROUND - 260, 0.7)
        else:
            potli(ctx, 540, GROUND - 330, 1.1, open_=clamp((t - b["khol"]) / 0.4), t=t)
            rice_fly(ctx, 540, GROUND - 350, 700, 690, t - b["kha"])
            if t > b["doosri"]:
                glow(ctx, 640, 640, 120, GOLD_HI, 0.6 + 0.3 * math.sin(t * 8))
        if b["bhabhi"] < t < b["khol"]:
            bubble(ctx, "KYA LAAYE HO?", 700, 540, t - b["bhabhi"], (760, 640))
        dv.ribbon(ctx, "DOOSRI MUTTHI...", 540, 300, t - b["doosri"], size=80)


class Rukmini(Cued):
    def beats(self, d):
        c = self.cue
        return {"pakad": c("HAATH", d * 0.12), "kyun": c("KYUN?", d * 0.3), "sab": c("SAB", d * 0.75),
                "apna": c("SAB", d * 0.75) + 0.6}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "shimmer"), (b["pakad"], "thud"), (b["kyun"], "pop"), (b["sab"], "boom"),
                (b["apna"], "shankh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        temple_bg(ctx, t)
        dv.krishna(ctx, 400, GROUND, 0.64, t, pose="ask")
        rukmini(ctx, 760, GROUND, 0.62, t, pose="touch", a=clamp(t / 0.4), flip=True)
        if t > b["pakad"]:
            glow(ctx, 590, 900, 90, GOLD_HI, 0.8)
        if t > b["kyun"]:
            tilt = 0.35 * ease_out_back(clamp((t - b["sab"]) / 0.6)) if t > b["sab"] else 0.0
            dv.balance(ctx, 540, 500, 0.7, tilt, t, labels=("EK MUTTHI", "SAB KUCHH"), a=clamp((t - b["kyun"]) / 0.4))
        if t > b["apna"]:
            dv.ribbon(ctx, "EK MUTTHI = SAB KUCHH", 540, 300, t - b["apna"], size=70)
        else:
            dv.ribbon(ctx, "RUKMINI NE ROKA", 540, 300, t - b["pakad"], size=78)


class Ghar(Cued):
    def beats(self, d):
        c = self.cue
        return {"gaanv": c("GAANV", d * 0.4), "sone": c("BADAL", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["gaanv"], "whoosh"), (b["sone"], "boom"), (b["sone"] + 0.1, "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        village(ctx, t, dusk=t > b["gaanv"])
        m = clamp((t - b["sone"]) / 0.5)
        if t > b["gaanv"]:
            hut(ctx, 640, GROUND - 10, 1.1, a=1 - m)
            gold_palace(ctx, 640, GROUND - 10, 1.0, t, a=m)
            x = 200
        else:
            dwarka_far(ctx, 200, 980, 0.8)
            x = lerp(300, 700, clamp(t / max(b["gaanv"], 1)))
        dv.brahmin(ctx, x, GROUND, 0.66, t, pose="point" if m > 0 else "stand", mood="smile", look=(1, 0))
        flash(ctx, t - b["sone"], c=(1, 0.95, 0.7), dur=0.5)
        if m > 0:
            dv.petals(ctx, t - b["sone"], 30, seed=8)
        dv.ribbon(ctx, "SAB BADAL GAYA", 540, 300, t - b["sone"], size=88)


class Cta(Cued):
    def beats(self, d):
        c = self.cue
        return {"comment": c("LIKHO", d * 0.7), "jai": c("JAI", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "ghanti"), (b["comment"], "pop"), (b["jai"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        temple_bg(ctx, t)
        glow(ctx, 540, 700, 420, GOLD_HI, 0.3)
        dv.brahmin(ctx, 330, 980, 0.56, t, pose="stand", mood="smile")
        dv.krishna(ctx, 750, 980, 0.58, t, pose="bless", flip=True)
        dv.ribbon(ctx, "SACHCHA DOST", 540, 300, t - 0.2, size=88)
        comment_card(ctx, t, b["comment"] - 0.3, b["jai"], "JAI SHRI KRISHNA", y=1000)


SCENE_CLASSES = {"hook": Hook, "who": Who, "patni": Patni, "milan": Milan, "potli": Potli, "rukmini": Rukmini,
                 "ghar": Ghar, "cta": Cta}


# ============================================================ upload kit (see upload_kit.py)

UPLOAD = {
    "titles": [
        "Why Did Rukmini Stop Krishna From Eating Sudama's Rice?",
        "Sudama Asked For Nothing. Krishna Gave Him Everything.",
        "Krishna And Sudama: The Handful Of Rice That Became A Palace",
        "Why Krishna Ate Only One Handful Of Sudama's Rice",
        "Sudama's Potli: The Real Story Of Krishna's Friendship",
        "Krishna Ran Barefoot For This Poor Friend",
        "What Was In Sudama's Potli? Krishna Sudama Story",
        "How Sudama's Hut Became A Golden Palace",
        "Krishna Sudama Ki Kahani: One Handful, Everything",
        "True Friendship: Krishna And Sudama Story In Hindi",
    ],
    "title": "Why Did Rukmini Stop Krishna From Eating Sudama's Rice?",
    "thumb_text": "DOOSRI MUTTHI?",
    "queries": ["krishna sudama ki kahani", "sudama ki potli", "krishna sudama dosti"],
    "description": """
Krishna Sudama ki kahani: garib Sudama ki potli mein mutthi bhar chawal the. Krishna sudama dosti ka rahasya,
Krishna ne ek mutthi khayi, to Rukmini ji ne doosri mutthi par haath kyun pakad liya?

Is Short me:
• Bachpan ke dost: Krishna Dwarka ke raja, Sudama itne gareeb ki chulha bhi na jale
• Patni ke kehne par, potli mein thode chawal
• Krishna nange paanv daude aaye
• Ek mutthi khayi, doosri par Rukmini ji ne haath thaam liya
• Bina maange, sab badal gaya

Comment me likho: Jai Shri Krishna.

Note: Katha Shrimad Bhagavat Mahapuran (Dasham Skandh, adhyay 80-81) se hai.
Kuch lok kathaon mein mutthiyon ki ginti alag hai.
""",
    "tags": ["krishna sudama", "krishna sudama ki kahani", "sudama ki potli", "krishna sudama dosti", "sudama charit",
             "krishna story in hindi", "rukmini", "dwarka", "bhagavat katha", "pauranik katha", "sachchi dosti",
             "krishna friendship", "divya rahasya", "shri krishna", "sudama"],
    "hashtags": ["#Shorts", "#Krishna", "#Sudama"],
}


def thumbnail(ctx):
    """1080x1920 cover: 'DOOSRI / MUTTHI?' over Krishna holding a glowing handful and Rukmini's hand on his wrist."""
    temple_bg(ctx, 0.3)
    glow(ctx, 540, 1000, 600, GOLD_HI, 0.45)
    dv.krishna(ctx, 400, 1760, 1.15, 0.3, pose="ask")
    rukmini(ctx, 900, 1800, 1.0, 0.3, pose="touch", flip=True)
    potli(ctx, 560, 1300, 1.6, open_=1.0)
    g = cairo.LinearGradient(0, 0, 0, 640)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.9)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 640)
    ctx.set_source(g)
    ctx.fill()
    text(ctx, "DOOSRI", 540, 230, 200, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "MUTTHI?", 540, 440, 210, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
