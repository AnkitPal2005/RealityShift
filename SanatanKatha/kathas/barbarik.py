"""Barbarik: Krishna ne sheesh kyun maanga? (~99s katha, ten scenes). First Sanatan katha Short.

Usage (from SanatanKatha/):
  python make.py barbarik

Characters from devta.py (Shri Krishna, the brahmin disguise, Barbarik, the Khatu Shyam sheesh roop, his mother),
told in the kathavachak voice (katha.TONES): hook (3 baan, sheesh?) -> who he is (Mahadev's 3 arrows) -> his
mother's words -> the brahmin's test (one arrow pierces every peepal leaf) -> the leaf under the foot -> the
brahmin is Krishna -> why (he would keep switching sides) -> sheesh daan -> Khatu Shyam -> "Jai Shri Shyam".
The sheesh daan is shown as light and petals only, nothing graphic.
Output: output/shorts/barbarik_short.mp4 (+ .json scene log, thumbnail, upload kit)
"""

from core.katha import *  # noqa: F401,F403  (engine helpers, devta as dv, scenery, Cued, story defaults)

TOPIC = "BARBARIK KHATU SHYAM"
OUTPUTS = {"edge": "barbarik_short.mp4"}

MUSIC_BPM = 84

SOURCES = [
    "Barbarika: son of Ghatotkacha (so Bhima's grandson); his story is told in the Skanda Purana (Kaumarika "
    "Khanda) and in Rajasthan/Haryana folk tradition, not in the core Vyasa Mahabharata - so the narration says "
    "'kehte hain' (Wikipedia 'Barbarika'; Wikipedia 'Khatushyam Temple')",
    "Three infallible arrows after tapasya to Shiva; vow to his mother to fight for the losing side; Krishna, "
    "disguised as a brahmin, tests him: one arrow marks every peepal leaf and stops at the leaf under Krishna's foot "
    "(Wikipedia 'Barbarika'; Khatu Shyam temple tradition; widely told in Times of India / NDTV Khatu Shyam explainers)",
    "Krishna reasons his support would keep switching sides until only he remains; Barbarika gives his head (sheesh "
    "daan), asks to watch the war, the head is placed on a hill; Krishna's boon: worshipped in Kali Yuga by Krishna's "
    "own name, Shyam, at Khatu (Sikar, Rajasthan), 'Haare ka Sahara' (Wikipedia 'Barbarika', 'Khatushyam Temple')",
    "Versions differ (some give the arrows from the Devis, some say the head was asked as the bravest warrior's "
    "sacrifice before the war); this Short follows the most widely told Khatu tradition",
]

# KikiVoice version (12 Nov 2026): the kathavachak tells each scene as ONE flowing paragraph, so the voice breathes
# where the punctuation says - "," breath, "..." the storyteller's held beat, "।" stop, "?" lift. Characters keep
# their own lines (and their own KikiVoice voice): "maa" = mother, "char" = the old brahmin, "deva" = Shri Krishna.
# The 3rd element is the silence after a line, kept between voices. No dashes and no hyphenated words (TTS trips).
SPEC = [
    {"key": "hook", "text": "3 BAAN SE YUDDH KHATAM",
     "visual": "Dusk Kurukshetra: Barbarik on rock with 3 divine glowing arrows; Shri Krishna appears asking the question",
     "vo": [("punch", [("महाभारत का वो अजेय योद्धा,", "MAHABHARAT KA WO AJEYA YODDHA,"),
                       ("जिसके तीन बाण एक मिनट में", "JISKE TEEN BAAN EK MINUTE MEIN"),
                       ("युद्ध खत्म कर सकते थे,", "YUDDH KHATAM KAR SAKTE THE,"),
                       ("वो थे बर्बरीक!", "WO THE BARBARIK!"),
                       ("लेकिन श्रीकृष्ण ने उनसे", "LEKIN SHRI KRISHNA NE UNSE"),
                       ("शीश क्यों मांग लिया?", "SHEESH KYUN MAANG LIYA?")], 0.04)]},

    {"key": "who", "text": "MATA KA VACHAN",
     "visual": "Barbarik remembering mother's vow with folded hands and glowing aura",
     "vo": [("tell", [("क्योंकि उन्हें माता का वचन था,", "KYUN KI UNHE MATA KA VACHAN THA,"),
                      ("हारे हुए का साथ देना!", "HAARE HUE KA SAATH DENA!")], 0.04)]},

    {"key": "daan", "text": "DONO SENAON KA SARVANASH",
     "visual": "Battlefield dilemma: armies in balance, cosmic destruction prevented by divine sacrifice",
     "vo": [("build", [("अगर कौरव हारते, तो बर्बरीक", "AGAR KAURAV HAARTE, TO BARBARIK"),
                       ("उनकी तरफ लड़ते,", "UNKI TARAF LADTE,"),
                       ("और दोनों सेनाओं का सर्वनाश हो जाता!", "AUR DONO SENAON KA SARVANASH HO JAATA!")], 0.04)]},

    {"key": "khatu", "text": "KHATU SHYAM JI",
     "visual": "Khatu Shyam Ji divine darshan; golden halo, floral rain, Haare Ka Sahara",
     "vo": [("awe", [("इसीलिए कृष्ण ने शीश दान लेकर", "ISI LIYE KRISHNA NE SHEESH DAAN LEKAR"),
                     ("उन्हें वरदान दिया,", "UNHE VARDAAN DIYA,"),
                     ("कलयुग के खाटू श्याम,", "KALYUG KE KHATU SHYAM,"),
                     ("हारे का सहारा!", "HAARE KA SAHARA!")], 0.04)]},
]
DELIVERY, SCRIPT, NARRATION = script_of(SPEC)   # kathavachak tones + held pauses (katha.TONES)

HOT = hot_words({"3": DIVINE, "BAAN": DIVINE, "BAAN!": DIVINE, "SHEESH": GOLD_HI, "KRISHNA": BLUE, "BARBARIK": SAFF,
       "BARBARIK!": SAFF, "SHIV": DIVINE, "ACHOOK": DIVINE, "VACHAN": GOLD_HI, "HAAR": hexc("#FF6B6B"),
       "BRAHMAN": SAFF, "PEEPAL": hexc("#6BD47A"), "PATTA": hexc("#6BD47A"), "PAIR": GOLD_HI, "KHUD": BLUE,
       "DAAN": GOLD_HI, "HANSTE-HANSTE": GOLD_HI, "KHATU": GOLD_HI, "SHYAM!": GOLD_HI, "SAHARA!": GOLD_HI,
       "JAI": GOLD_HI, "SHRI": GOLD_HI, "SOCHO": GOLD_HI, "BETA": hexc("#FFB3C7"), "MAHADEV": DIVINE,
       "HATAO": GOLD_HI, "GHOOMA": DIVINE, "KYUN": GOLD_HI, "EK-EK": hexc("#6BD47A"), "DAR": hexc("#FF6B6B"), "VARDAAN": GOLD_HI, "KALYUG": SAFF, "BHAI,": SAFF, "IB": SAFF,
       "SIRF": SAFF, "PAALA": hexc("#FF6B6B"), "COMMENT": GOLD_HI})



# ============================================================ scenes

class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"arrows": c("TEEN", d * 0.22), "yudh": c("YUDDH", d * 0.4), "krishna": c("KRISHNA", d * 0.65),
                "sheesh": c("SHEESH", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["arrows"], "shimmer"), (b["arrows"] + 0.2, "arrow"), (b["yudh"] + 0.4, "boom"),
                (b["krishna"], "ghanti"), (b["sheesh"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        wipe = clamp((t - b["yudh"] - 0.4) / 0.5)
        battlefield(ctx, t, dim=1 - wipe)
        u = t - b["yudh"] - 0.4
        if u > 0:   # shockwave from the three arrows
            r = 1400 * ease_out_cubic(u / 0.8)
            ctx.arc(540, GROUND - 120, r, 0, math.tau)
            rgba(ctx, DIVINE, 0.6 * (1 - clamp(u / 0.8)))
            ctx.set_line_width(30)
            ctx.stroke()
        dv.hill(ctx, 540, GROUND + 20, 360, 200, hexc("#2E1A1A"))
        glow(ctx, 540, 600, 420, GOLD, 0.25)
        dv.barbarik(ctx, 540, GROUND - 150, 0.62, t, pose="stand", arrows=0)
        for k in range(3):
            v = t - b["arrows"] - 0.22 * k
            if v > 0:
                x = 400 + 140 * k
                y = 330 - 30 * (k == 1) + 8 * math.sin(t * 3 + k)
                dv.divine_arrow(ctx, x, lerp(y + 80, y, ease_out_back(clamp(v / 0.4))), -math.pi / 2, 150, t,
                                a=clamp(v / 0.2))
        u = t - b["krishna"]
        if u > 0:
            glow(ctx, 1000, 700, 500, BLUE, 0.5 * clamp(u / 0.5))
            dv.krishna(ctx, lerp(1200, 920, ease_out_cubic(u / 0.8)), GROUND - 40, 0.55, t, pose="flute",
                       a=clamp(u / 0.4), look=(-0.6, 0))


class Who(Cued):
    def beats(self, d):
        c = self.cue
        return {"shiv": c("MAHADEV", d * 0.55), "baan": c("ACHOOK", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["shiv"], "ghanti")] + [(b["baan"] + 0.3 * k, "arrow") for k in range(3)] + \
            [(b["baan"] + 1.0, "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dv.sky(ctx, hexc("#3B1A4A"), hexc("#B85A3C"), hexc("#2A1410"))
        dv.group(ctx, clamp((t - b["shiv"]) / 0.6), lambda: dv.kailash(ctx, t))
        ctx.rectangle(0, GROUND - 30, W, H)
        rgba(ctx, hexc("#2A1A22"))
        ctx.fill()
        landed = sum(1 for k in range(3) if t > b["baan"] + 0.3 * k + 0.45)
        dv.barbarik(ctx, 540, GROUND, 0.82, t, pose="stand", arrows=landed, look=(0, -0.2))
        tip = (540 + 203 * 0.82, GROUND - 800 * 0.82)
        for k in range(3):
            u = (t - b["baan"] - 0.3 * k) / 0.45
            if 0 < u < 1:
                y = lerp(-120, tip[1] - 40, ease_in_out(u))
                dv.divine_arrow(ctx, tip[0] + (k - 1) * 14, y, math.pi / 2, 160, t, trail=1.0)


class Vow(Cued):
    def beats(self, d):
        c = self.cue
        return {"haar": c("HAARE", d * 0.5), "ladu": c("VACHAN", d * 0.3)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["haar"], "ghanti"), (b["ladu"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dv.sky(ctx, hexc("#1E0A10"), hexc("#4A1A1A"), hexc("#120608"))
        for k in range(5):     # warm arches
            ctx.arc(108 + 216 * k, 700, 100, math.pi, 0)
            rgba(ctx, hexc("#2A0E12"))
            ctx.set_line_width(26)
            ctx.stroke()
        ctx.rectangle(0, GROUND - 20, W, H)
        rgba(ctx, hexc("#2A120C"))
        ctx.fill()
        dv.diya(ctx, 540, GROUND - 10, 1.2, t)
        mother(ctx, 250, GROUND, 0.88, t)
        dv.barbarik(ctx, 800, GROUND, 0.7, t, pose="namaste", mood="calm", arrows=3)
        u = t - b["haar"]
        if u > 0:
            k = ease_out_back(clamp(u / 0.4))
            tilt = 0.28 * ease_in_out(clamp((u - 0.2) / 0.8))
            ctx.save()
            ctx.translate(540, 380)
            ctx.scale(k, k)
            ctx.translate(-540, -380)
            glow(ctx, 540, 420, 380, GOLD, 0.3)
            dv.balance(ctx, 540, 300, 0.75, tilt, t, labels=("JEET", "HAAR"))
            ctx.restore()
            v = t - b["ladu"]
            if v > 0:   # the divine arrow chooses the losing side
                px, py = 540 + 250 * 0.75 * math.cos(tilt), 300 - 250 * 0.75 * math.sin(tilt) + 170
                bob = 10 * math.sin(t * 6)
                dv.divine_arrow(ctx, px, lerp(py + 300, py + 70, ease_out_back(clamp(v / 0.4))) + bob, -math.pi / 2,
                                150, t)


HIDDEN = 12                  # the leaf the brahmin keeps under his foot
TREE = (870, GROUND, 0.85)
BARB_TEST = (230, 0.6)       # Barbarik's x and scale in the test scene


def leaf_xy(i):
    lx, ly, _, ls = dv.LEAVES[i]
    x, y, s = TREE
    return x + lx * s, y + (ly + 30 * ls) * s


class Test(Cued):
    def beats(self, d):
        c = self.cue
        r = c("CHHODA", d * 0.55)
        return {"brahman": c("BRAHMAN", 0.3), "bola": c("BOLA", d * 0.25), "release": r + 0.5,
                "patta": c("EK-EK", d * 0.82)}

    def flight(self, d):
        b = self.beats(d)
        bx, s = BARB_TEST
        start = (bx + 440 * s, GROUND - 560 * s)
        order = [i for i in range(len(dv.LEAVES)) if i != HIDDEN]
        pts = [start, (640, 560)] + [leaf_xy(i) for i in order] + [(1200, 260)]
        dur = max(1.4, d - b["release"] - 0.2)
        return b["release"], dur, pts, order

    def events(self, d):
        b = self.beats(d)
        r, dur, pts, order = self.flight(d)
        hits = [(r + (j + 2) / (len(pts) - 1) * dur, "tick") for j in range(0, len(order), 3)]
        return [(0.02, "soft_thud"), (b["bola"], "pop"), (r - 0.9, "pick"), (r, "arrow")] + hits + \
            [(b["patta"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        r, dur, pts, order = self.flight(d)
        meadow(ctx, t)
        marks = {}
        for j, i in enumerate(order):
            at = r + (j + 2) / (len(pts) - 1) * dur
            if t > at:
                marks[i] = clamp((t - at) / 0.2)
        dv.peepal(ctx, *TREE, t, marks=marks, hidden={HIDDEN})
        bx, s = BARB_TEST
        if t < r - 0.9:
            dv.barbarik(ctx, bx, GROUND, s, t, pose="stand", arrows=3, look=(0.6, 0))
        else:
            amt = ease_in_out(clamp((t - (r - 0.9)) / 0.7)) if t < r else 0.0
            dv.barbarik(ctx, bx, GROUND, s, t, pose="draw", draw_amt=amt, arrows=2 if t >= r else 3)
        dv.brahmin(ctx, 590, GROUND, 0.55, t, pose="ask" if t > b["bola"] else "stand", mood="look",
                   look=(0.8, 0), flip=True)
        if t < r - 0.6:
            bubble(ctx, "3 BAAN SE?", 600, 600, t - b["bola"] - 0.3, (600, 700))
        u = (t - r) / dur
        if 0 < u < 1:
            (x, y), ang = polyline_at(pts, u)
            dv.divine_arrow(ctx, x, y, ang, 130, t, trail=1.0)
        dv.ribbon(ctx, "1 BAAN = HAR PATTA", 540, 300, t - b["patta"] - 0.2, size=70)


FOOT = (588, 1136)


class Foot(Cued):
    def beats(self, d):
        c = self.cue
        return {"chhupa": c("CHUPKE", d * 0.3), "baan": c("AAYA", d * 0.55), "ruka": c("HATAO", d * 0.88)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["chhupa"], "whoosh"), (b["baan"] - 0.2, "arrow"), (b["baan"] + 0.5, "arrow"),
                (b["ruka"], "thud"), (b["ruka"] + 0.05, "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        meadow(ctx, t)
        ctx.rectangle(0, 0, W, H)
        rgba(ctx, (0.05, 0.02, 0.1), 0.25)
        ctx.fill()
        lx = lerp(860, FOOT[0] - 30, ease_in_out(clamp((t - 0.2) / max(b["chhupa"] + 0.4, 0.6))))
        dv.leaf(ctx, lx, FOOT[1] + 4, -math.pi / 2, 1.3, t=0)
        if t > b["chhupa"]:
            glow(ctx, FOOT[0] + 40, FOOT[1], 120, hexc("#9BE36B"), 0.35)
        dv.brahmin(ctx, 540, GROUND - 30, 1.0, t, pose="stand", mood="look", look=(0.35, 0.9),
                   hint=0.35 * clamp((t - b["baan"]) / 1.0))
        u = t - b["baan"] + 0.2
        stop = b["ruka"]
        if u > 0:
            cx, cy = FOOT[0] + 20, FOOT[1] - 60
            if t < stop:   # circles the foot, closing in
                k = clamp(u / max(stop - b["baan"] + 0.2, 0.4))
                rad = lerp(520, 150, ease_in_out(k))
                ang = -math.pi / 2 + 4.2 * math.pi * ease_in_out(k)
                x, y = cx + rad * math.cos(ang), cy + rad * 0.55 * math.sin(ang)
                dv.divine_arrow(ctx, x, y, ang + math.pi / 2, 130, t, trail=1.0)
            else:          # stops over the foot, pointing down at it
                v = t - stop
                bob = 8 * math.sin(t * 5)
                for k in range(3):
                    rr = 40 + 120 * ((v * 0.8 + k / 3) % 1)
                    dv.ell(ctx, FOOT[0] + 20, FOOT[1], rr, rr * 0.35)
                    rgba(ctx, DIVINE, 0.7 * (1 - (v * 0.8 + k / 3) % 1))
                    ctx.set_line_width(5)
                    ctx.stroke()
                dv.divine_arrow(ctx, FOOT[0] + 20, FOOT[1] - 120 + bob, math.pi / 2, 150, t)
                dv.ribbon(ctx, "PAIR KE NEECHE!", 540, 300, v - 0.1, size=74)


class Reveal(Cued):
    def beats(self, d):
        c = self.cue
        return {"koi": c("KOI", d * 0.3), "khud": c("KHUD", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["koi"], "shimmer"), (b["khud"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dv.sky(ctx, hexc("#0E0A2A"), hexc("#2A2A6A"), hexc("#120A1E"))
        dv.stars(ctx, t)
        ctx.rectangle(0, GROUND - 30, W, H)
        rgba(ctx, hexc("#1A1430"))
        ctx.fill()
        u = t - b["khud"]
        hint = 0.3 + 0.7 * clamp(t / max(b["khud"], 0.4))
        if u < 0.35:
            dv.brahmin(ctx, 540, GROUND, 0.95, t, pose="stand", mood="smile", hint=hint,
                       a=1 - clamp(u / 0.35) if u > 0 else 1.0)
        if u > 0:
            ctx.save()
            ctx.translate(540, 560)
            ctx.rotate(t * 0.2)
            for k in range(16):
                ang = k / 16 * math.tau
                ctx.move_to(0, 0)
                ctx.arc(0, 0, 1300, ang - 0.04, ang + 0.04)
                ctx.close_path()
            rgba(ctx, BLUE, 0.12 * clamp(u / 0.5))
            ctx.fill()
            ctx.restore()
            dv.krishna(ctx, 540, GROUND, 0.95, t, pose="bless", a=clamp(u / 0.3))
            dv.petals(ctx, u, 36, seed=4)
            dv.ribbon(ctx, "SHRI KRISHNA", 540, 300, u - 0.4, size=84, c=hexc("#1E3A8A"))
        flash(ctx, u, dur=0.7)


class Logic(Cued):
    def beats(self, d):
        c = self.cue
        return {"jidhar": c("KAURAV", d * 0.15), "paala": c("BARBARIK", d * 0.4), "aakhir": c("SARVANASH", d * 0.75)}

    def jumps(self, d):
        b = self.beats(d)
        gap = max(0.25, (b["aakhir"] - b["paala"]) / 5)
        times = [b["jidhar"]] + [b["paala"] + gap * k for k in range(5)]
        return times, gap

    def events(self, d):
        b = self.beats(d)
        times, _ = self.jumps(d)
        return [(0.02, "thud")] + [(tm, "whoosh") for tm in times] + [(b["aakhir"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        times, gap = self.jumps(d)
        dv.sky(ctx, hexc("#2B1238"), hexc("#B8442E"), hexc("#2A120C"), 0.5)
        ctx.rectangle(0, GROUND - 60, W, H)
        rgba(ctx, hexc("#2A120C"))
        ctx.fill()
        left = (1 - clamp((t - b["jidhar"]) / max(b["aakhir"] - b["jidhar"], 0.5)))
        n = int(round(9 * left))
        side_x = [540]
        for k, tm in enumerate(times):
            side_x.append(290 if k % 2 == 0 else 790)
        # current hop: which jump we are in
        x, y = 540, 860          # feet of the little Barbarik floating above the armies
        for k, tm in enumerate(times):
            if t >= tm:
                v = clamp((t - tm) / min(0.45, gap * 0.9))
                x = lerp(side_x[k], side_x[k + 1], ease_in_out(v))
                y = 860 - 180 * math.sin(math.pi * v)
        on_left = x < 540
        ending = clamp((t - b["aakhir"]) / 0.6)
        for k, (x0, x1, flag) in enumerate(((40, 480, SAFF), (600, 1040, hexc("#8C1C2C")))):
            mine = (k == 0) == on_left and t > b["jidhar"]
            if mine and ending < 1:
                glow(ctx, (x0 + x1) / 2, GROUND - 120, 300, GOLD, 0.35)
            dv.army(ctx, x0, x1, GROUND - 70, max(n, 0), hexc("#160A0A"), t, flag, seed=k + 1,
                    a=1 - ending)
        if ending > 0:
            x = lerp(x, 540, ending)
            y = lerp(y, GROUND - 60, ending)
            g = cairo.LinearGradient(540, 0, 540, GROUND)
            g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0)
            g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0.35 * ending)
            ctx.move_to(440, 0)
            ctx.line_to(640, 0)
            ctx.line_to(760, GROUND)
            ctx.line_to(320, GROUND)
            ctx.close_path()
            ctx.set_source(g)
            ctx.fill()
        s = lerp(0.34, 0.6, ending)
        dv.barbarik(ctx, x, y, s, t, pose="stand", arrows=3)


class Daan(Cued):
    def beats(self, d):
        c = self.cue
        return {"sheesh": c("SHEESH", d * 0.3), "socha": c("DAR", d * 0.62), "hanste": c("HANSTE", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["sheesh"], "thud"), (b["socha"], "ghanti"), (b["hanste"], "shimmer"),
                (b["hanste"] + 0.9, "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dv.sky(ctx, hexc("#24123E"), hexc("#D9824A"), hexc("#2A140E"), 0.6)
        glow(ctx, 540, 820, 600, hexc("#FFCE80"), 0.4)
        ctx.rectangle(0, GROUND - 40, W, H)
        rgba(ctx, hexc("#30180E"))
        ctx.fill()
        dv.krishna(ctx, 790, GROUND, 0.78, t, pose="ask", flip=True, look=(0.5, 0.1), smile=0.6)
        u = t - b["hanste"]
        glow_a = clamp(u / 0.8) if u > 0 else 0.0
        fade = 1 - clamp((u - 0.9) / 0.5) if u > 0 else 1.0
        mood = "calm" if t > b["socha"] else "fierce"
        dv.barbarik(ctx, 300, GROUND, 0.78, t, pose="namaste", mood=mood, arrows=2, glow_a=glow_a, a=fade)
        if u > 0.9:
            v = u - 0.9
            oy = lerp(GROUND - 500, 260, ease_in_out(clamp(v / 1.6)))
            glow(ctx, 300, oy, 160, GOLD_HI, 0.9)
            circle(ctx, 300, oy, 34, (1, 1, 0.92))
            dv.petals(ctx, v, 44, seed=7)
        flash(ctx, u - 0.9, c=(1, 0.93, 0.7), dur=0.7)


class Khatu(Cued):
    def beats(self, d):
        c = self.cue
        return {"vardaan": c("VARDAAN", d * 0.35), "khatu": c("KHATU", d * 0.72), "sahara": c("SAHARA", d * 0.86)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["vardaan"], "shimmer"), (b["khatu"], "ghanti"),
                (b["sahara"], "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dawn = clamp((t - b["khatu"]) / 1.0)
        dv.sky(ctx, hexc("#120A2A"), hexc("#4A2A5A"), hexc("#1A0E14"))
        ctx.rectangle(0, 0, W, H)
        rgba(ctx, hexc("#FF9A4A"), 0.25 * dawn)
        ctx.fill()
        dv.stars(ctx, t, a=1 - dawn)
        for k, (x0, x1) in enumerate(((20, 330), (750, 1060))):
            dv.army(ctx, x0, x1, GROUND - 10, 5, hexc("#0E0608"), t, SAFF if k == 0 else hexc("#8C1C2C"), seed=k + 3,
                    a=1 - dawn)
        dv.hill(ctx, 540, GROUND + 40, 470, 460, hexc("#2E1E36"))
        u = t - b["khatu"]
        grow = ease_in_out(clamp(u / 0.9))
        sx, sy = 540, lerp(GROUND + 40 - 460 - 50, 600, grow)
        v = t - b["vardaan"]
        if v > 0 and u < 0.8:
            dv.krishna(ctx, 220, 900, 0.42, t, pose="bless", a=clamp(v / 0.4) * (1 - clamp(u / 0.6)))
        dv.shyam(ctx, sx, sy, lerp(0.38, 0.78, grow), t, garland=grow, aura=lerp(0.5, 1.0, grow))
        if u > 0:
            dv.petals(ctx, u, 40, seed=9)


class Cta(Cued):
    def beats(self, d):
        c = self.cue
        return {"comment": c("COMMENT", d * 0.45), "jai": c("JAI", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "ghanti"), (b["comment"], "pop"), (b["jai"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        temple_bg(ctx, t)
        dv.shyam(ctx, 540, 400, 0.6, t, garland=1.0)
        dv.diya(ctx, 130, GROUND - 40, 1.1, t)
        dv.diya(ctx, 950, GROUND - 40, 1.1, t + 1)
        u = t - b["comment"] + 0.3
        if u <= 0:
            return
        pop = ease_out_back(clamp(u / 0.35))
        ctx.save()
        ctx.translate(540, 960)
        ctx.scale(pop, pop)
        rrect(ctx, -440, -150, 880, 300, 30)
        dv.ink(ctx, hexc("#1A0A0E"), 5, edge=GOLD)
        text(ctx, "COMMENT MEIN LIKHO", 0, -88, 54, GOLD_HI, font=CAPTION_FONT, bold=False)
        rrect(ctx, -390, -30, 780, 130, 24)
        dv.ink(ctx, (0.06, 0.03, 0.04), 4, edge=GOLD if t > b["jai"] else GOLD_DK)
        msg = "JAI SHRI SHYAM"
        shown = msg[:int(len(msg) * clamp((t - b["jai"]) / 0.7))] if t > b["jai"] else ""
        tw = text(ctx, shown, -350, 35, 76, (1, 1, 1), font=CAPTION_FONT, bold=False, anchor="l") if shown else 0
        if int(t * 3) % 2 == 0:
            ctx.rectangle(-344 + tw, -5, 7, 80)
            rgba(ctx, GOLD_HI)
            ctx.fill()
        ctx.restore()
        if t > b["jai"]:   # arrow toward the Shorts comment button
            k = ease_out_cubic(clamp((t - b["jai"]) / 0.4))
            bob = 10 * math.sin(t * 6)
            x0, y0 = 880, 1130
            x1, y1 = lerp(x0, 1010, k), lerp(y0, 1330, k) + bob
            line(ctx, [(x0, y0), (x1, y1)], GOLD_HI, 12)
            ang = math.atan2(y1 - y0, x1 - x0)
            ctx.move_to(x1 + 34 * math.cos(ang), y1 + 34 * math.sin(ang))
            for da in (2.4, -2.4):
                ctx.line_to(x1 + 30 * math.cos(ang + da), y1 + 30 * math.sin(ang + da))
            ctx.close_path()
            rgba(ctx, GOLD_HI)
            ctx.fill()


SCENE_CLASSES = {
    "hook": Hook,
    "who": Vow,
    "daan": Logic,
    "khatu": Khatu,
}


# ============================================================ upload kit (see upload_kit.py)

UPLOAD = {
    "titles": [
        "Khatu Shyam Ki Kahani: Krishna Ne Sheesh Kyun Maanga?",
        "Barbarik Ki Kahani: 3 Baan Wala Yoddha",
        "Krishna Ne Barbarik Se Sheesh Daan Kyun Liya?",
        "Haare Ka Sahara: Khatu Shyam Kaun Hain?",
        "Barbarik Story In Hindi: Ek Baan, Har Patta",
        "Mahabharat Ka Sabse Bada Daani: Barbarik",
        "Peepal Ke Patte Aur Krishna Ki Pareeksha",
        "Barbarik Aur Shri Krishna: Sheesh Daan Ki Katha",
        "Khatu Shyam Baba Ki Katha: Barbarik Kaun Tha?",
        "Wo Yoddha Jo Ek Pal Mein Yudh Khatam Kar Deta",
    ],
    "title": "Khatu Shyam Ki Kahani: Krishna Ne Sheesh Kyun Maanga?",
    "thumb_text": "SHEESH KYUN MAANGA?",
    "queries": ["khatu shyam ki kahani", "barbarik ki kahani", "barbarik krishna"],
    "description": """
Barbarik ki kahani: Bheem ka pota, Ghatotkach ka beta, jiske 3 baan poora yudh khatam kar sakte the.
Shri Krishna ne usse sheesh kyun maanga, aur wo Khatu Shyam kaise bane? Poori katha is Short me.

Is Short me:
• Shiv ji ki tapasya se 3 achook baan
• Maa ki seekh: jo haar raha ho, uska saath dena
• Brahman ki pareeksha: ek baan, peepal ka har patta, aur pair ke neeche chhupa patta
• Brahman asal me Shri Krishna the
• Sheesh daan, aur Krishna ka vardaan: Kalyug me Khatu Shyam, Haare ka Sahara

Comment me likho: Jai Shri Shyam.

Note: Barbarik ki katha mool Mahabharat me nahi, Skanda Puran aur lok parampara se aati hai; alag jagah iske
thode alag roop sunaye jaate hain. Yahan Khatu ki sabse prachalit katha li gayi hai.
""",
    "tags": ["khatu shyam", "barbarik", "barbarik ki kahani", "khatu shyam ki kahani", "khatu shyam baba",
             "haare ka sahara", "shri krishna", "mahabharat ki kahani", "sheesh ke daani", "jai shri shyam",
             "krishna katha", "hindu mythology shorts", "mahabharat story hindi", "barbarik krishna",
             "pauranik katha"],
    "hashtags": ["#Shorts", "#KhatuShyam", "#Barbarik"],
}


def thumbnail(ctx):
    """1080x1920 cover: 'SHEESH KYUN / MAANGA?' over the Khatu Shyam roop with three divine arrows."""
    temple_bg(ctx, 0.0)
    dv.shyam(ctx, 540, 1060, 1.0, 0.3, garland=1.0)
    for k in range(3):
        dv.divine_arrow(ctx, 330 + 210 * k, 640 - 40 * (k == 1), -math.pi / 2, 160, 0.3)
    g = cairo.LinearGradient(0, 0, 0, 640)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.9)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 640)
    ctx.set_source(g)
    ctx.fill()
    text(ctx, "SHEESH KYUN", 540, 230, 190, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "MAANGA?", 540, 430, 200, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    dv.krishna(ctx, 930, 1900, 0.5, 0.3, pose="ask", flip=True)

