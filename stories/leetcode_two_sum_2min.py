"""Story: LeetCode #1 Two Sum, the ~2 minute deep-dive — problem, brute force, why it is O(N²),
the complement trick, a 5-step dry run, the check-before-store edge case, the code, complexity.

Same split screen and safe zones as leetcode_two_sum (coder left, IDE right, captions in the
1150-1250 px band, nothing in the bottom 400 px); the drawing helpers are shared from there.
"""

import math

from engine import *  # noqa: F401,F403
from stories.leetcode_two_sum import (CYAN, GREEN, MONO, ORANGE, PANEL, RED, STAMP_Y, YELLOW, Board, Brute,
                                      Hook, Outro, arrow_head, badge, cell_x, cells, chip, code_block,
                                      cross_mark, interviewer, mono_line, tick_mark)
from stories.reality_shift import stamp

TOPIC = "LEETCODE #1 · TWO SUM"
WATERMARK = "2 MIN DSA"
OUTPUTS = {"edge": "leetcode_two_sum_2min.mp4", "elevenlabs": "leetcode_two_sum_2min_el.mp4"}
OUTPUT_DIR = OUT_DIR

CLEAN_PUNCTUATION = False
MAX_GAP = 0.22
TAIL_PAD = 0.15
TRIM = {"thresh": 0.006, "keep": 0.05, "keep_tail": 0.08}
MUSIC_BPM = 110
MUSIC_DUCK = 0.6
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"

CAPTION_Y = 1200
CAPTION_SIZE = 108
HOT_COLOR = YELLOW
HOT_COLORS = {"TWO": YELLOW, "SUM": YELLOW, "O(N²)": YELLOW, "N²": YELLOW, "BRUTE": YELLOW, "FORCE": YELLOW,
              "KARODON": YELLOW, "TEZ": YELLOW, "PALATNA!": YELLOW, "KITNA": YELLOW, "STORE": YELLOW,
              "GALAT": YELLOW, "FOLLOW": YELLOW, "HASH": CYAN, "MAP": CYAN, "O(N)": CYAN, "LINEAR": CYAN,
              "TURANT": CYAN, "CHECK": CYAN, "SAHI": CYAN, "NEED": CYAN, "DICTIONARY": CYAN,
              "COMMENT": CYAN, "TARGET": CYAN}
HOT_WORDS = set(HOT_COLORS)

NARRATION = {
    "hook": "क्या आप भी टू सम में दो-दो फॉर लूप लगाते हैं? आज सिर्फ दो मिनट में समझिए वो ट्रिक, जो हर "
            "इंटरव्यूअर सुनना चाहता है!",
    "problem": "सवाल ये है: आपको नंबरों का एक ऐरे मिलेगा, जैसे दो, सात, ग्यारह, पंद्रह, और एक टारगेट, नौ। "
               "ऐसे दो नंबर ढूंढो जिनका जोड़ टारगेट के बराबर हो, और उनके इंडेक्स रिटर्न करो। यहां दो प्लस "
               "सात बराबर नौ, तो जवाब है ज़ीरो और वन!",
    "brute": "सबसे सीधा तरीका है ब्रूट फोर्स: दो लूप लगाओ, और हर नंबर को बाकी हर नंबर के साथ जोड़कर चेक करो। "
             "अगर जवाब आखिरी जोड़े में हो, तो पहले दो और सात, फिर दो और ग्यारह... हर एक जोड़ा चेक होगा।",
    "cost": "पर दिक्कत ये है कि एन नंबर हों, तो करीब एन स्क्वेयर चेक। दस हज़ार नंबर, यानी करोड़ों चेक! इसे "
            "कहते हैं O of N squared, और इंटरव्यूअर यहीं पूछेगा: क्या इससे तेज़ हो सकता है?",
    "idea": "असली ट्रिक है सवाल पलटना! ये मत पूछो कि इसे किससे जोड़ूं, ये पूछो: मुझे कितना चाहिए? यानी "
            "टारगेट माइनस करंट नंबर। और जो नंबर देख चुके हो, उन्हें एक हैश मैप में याद रखो, जहां ढूंढना "
            "तुरंत होता है!",
    "dryrun": "चलो ड्राई रन करें। ऐरे है तीन, आठ, चार, ग्यारह, छह, और टारगेट दस। तीन आया: चाहिए सात, मैप "
              "में नहीं, तो तीन स्टोर करो। आठ आया: चाहिए दो, नहीं है, स्टोर। चार आया: चाहिए छह, नहीं है, "
              "स्टोर। ग्यारह: चाहिए माइनस एक, स्टोर। और छह आया: चाहिए चार... चार मैप में है, इंडेक्स दो "
              "पर! जवाब: दो और चार।",
    "edge": "एक ज़रूरी बात: पहले चेक करो, फिर स्टोर करो। अगर ऐरे है पाँच, एक, पाँच और टारगेट दस, और आपने "
            "पहले स्टोर किया, तो पहला पाँच खुद से ही जुड़ जाएगा, और गलत जवाब आएगा ज़ीरो, ज़ीरो! सही जवाब "
            "है ज़ीरो और दो।",
    "code": "कोड बस कुछ ही लाइन का है: एक खाली डिक्शनरी बनाओ। हर नंबर के लिए नीड निकालो, यानी टारगेट "
            "माइनस एक्स। नीड मैप में है तो दोनों इंडेक्स रिटर्न करो, वरना नंबर को उसके इंडेक्स के साथ "
            "स्टोर कर दो।",
    "outro": "टाइम कॉम्प्लेक्सिटी सीधा लीनियर O of N, क्योंकि ऐरे पर सिर्फ एक बार चले। स्पेस भी O of N, मैप "
             "के लिए। थोड़ी मेमोरी देकर ढेर सारा टाइम बचाया! अगला इंटरव्यू क्वेश्चन कौन सा सॉल्व करवाएं? "
             "कमेंट में बताएं और फॉलो करें!",
}

CHUNKS = {
    "hook": [
        ("क्या आप भी", "KYA AAP BHI"),
        ("टू सम में", "TWO SUM MEIN"),
        ("दो-दो फॉर लूप", "DO-DO FOR LOOP"),
        ("लगाते हैं?", "LAGATE HAIN?"),
        ("आज सिर्फ", "AAJ SIRF"),
        ("दो मिनट में समझिए", "2 MINUTE MEIN SAMJHIYE"),
        ("वो ट्रिक,", "WO TRICK"),
        ("जो हर इंटरव्यूअर", "JO HAR INTERVIEWER"),
        ("सुनना चाहता है!", "SUNNA CHAHTA HAI!"),
    ],
    "problem": [
        ("सवाल ये है:", "SAWAAL YE HAI:"),
        ("आपको नंबरों का", "AAPKO NUMBERS KA"),
        ("एक ऐरे मिलेगा,", "EK ARRAY MILEGA"),
        ("जैसे दो, सात, ग्यारह, पंद्रह,", "JAISE 2, 7, 11, 15"),
        ("और एक टारगेट, नौ।", "AUR EK TARGET = 9"),
        ("ऐसे दो नंबर ढूंढो", "AISE 2 NUMBER DHOONDHO"),
        ("जिनका जोड़", "JINKA JOD"),
        ("टारगेट के बराबर हो,", "TARGET KE BARABAR HO"),
        ("और उनके इंडेक्स", "AUR UNKE INDEX"),
        ("रिटर्न करो।", "RETURN KARO"),
        ("यहां दो प्लस सात", "YAHAN 2 + 7"),
        ("बराबर नौ,", "= 9"),
        ("तो जवाब है", "TO JAWAAB HAI"),
        ("ज़ीरो और वन!", "[0, 1]!"),
    ],
    "brute": [
        ("सबसे सीधा तरीका है", "SABSE SEEDHA TAREEKA"),
        ("ब्रूट फोर्स:", "BRUTE FORCE:"),
        ("दो लूप लगाओ,", "2 LOOP LAGAO"),
        ("और हर नंबर को", "AUR HAR NUMBER KO"),
        ("बाकी हर नंबर के साथ", "BAAKI HAR NUMBER KE SAATH"),
        ("जोड़कर चेक करो।", "JODKAR CHECK KARO"),
        ("अगर जवाब", "AGAR JAWAAB"),
        ("आखिरी जोड़े में हो,", "AAKHIRI JODE MEIN HO"),
        ("तो पहले दो और सात,", "TO PEHLE 2 AUR 7"),
        ("फिर दो और ग्यारह...", "PHIR 2 AUR 11..."),
        ("हर एक जोड़ा", "HAR EK JODA"),
        ("चेक होगा।", "CHECK HOGA"),
    ],
    "cost": [
        ("पर दिक्कत ये है", "PAR DIKKAT YE HAI"),
        ("कि एन नंबर हों,", "KI N NUMBER HON"),
        ("तो करीब एन स्क्वेयर चेक।", "TO KAREEB N² CHECK"),
        ("दस हज़ार नंबर,", "10,000 NUMBER"),
        ("यानी करोड़ों चेक!", "YAANI KARODON CHECK!"),
        ("इसे कहते हैं", "ISE KEHTE HAIN"),
        ("O of N squared,", "O(N²)"),
        ("और इंटरव्यूअर", "AUR INTERVIEWER"),
        ("यहीं पूछेगा:", "YAHIN POOCHHEGA:"),
        ("क्या इससे तेज़", "KYA ISSE TEZ"),
        ("हो सकता है?", "HO SAKTA HAI?"),
    ],
    "idea": [
        ("असली ट्रिक है", "ASLI TRICK HAI"),
        ("सवाल पलटना!", "SAWAAL PALATNA!"),
        ("ये मत पूछो", "YE MAT POOCHHO"),
        ("कि इसे किससे जोड़ूं,", "KI ISE KISSE JODUN"),
        ("ये पूछो:", "YE POOCHHO:"),
        ("मुझे कितना चाहिए?", "MUJHE KITNA CHAHIYE?"),
        ("यानी टारगेट माइनस", "YAANI TARGET MINUS"),
        ("करंट नंबर।", "CURRENT NUMBER"),
        ("और जो नंबर", "AUR JO NUMBER"),
        ("देख चुके हो,", "DEKH CHUKE HO"),
        ("उन्हें एक हैश मैप में", "UNHE EK HASH MAP MEIN"),
        ("याद रखो,", "YAAD RAKHO"),
        ("जहां ढूंढना", "JAHAN DHOONDHNA"),
        ("तुरंत होता है!", "TURANT HOTA HAI!"),
    ],
    "dryrun": [
        ("चलो ड्राई रन करें।", "CHALO DRY RUN KAREIN"),
        ("ऐरे है", "ARRAY HAI"),
        ("तीन, आठ, चार, ग्यारह, छह,", "[3, 8, 4, 11, 6]"),
        ("और टारगेट दस।", "AUR TARGET 10"),
        ("तीन आया:", "3 AAYA:"),
        ("चाहिए सात,", "CHAHIYE 7"),
        ("मैप में नहीं,", "MAP MEIN NAHI"),
        ("तो तीन स्टोर करो।", "TO 3 STORE KARO"),
        ("आठ आया:", "8 AAYA:"),
        ("चाहिए दो,", "CHAHIYE 2"),
        ("नहीं है, स्टोर।", "NAHI HAI, STORE"),
        ("चार आया:", "4 AAYA:"),
        ("चाहिए छह,", "CHAHIYE 6"),
        ("नहीं है, स्टोर।", "NAHI HAI, STORE"),
        ("ग्यारह:", "11:"),
        ("चाहिए माइनस एक, स्टोर।", "CHAHIYE -1, STORE"),
        ("और छह आया:", "AUR 6 AAYA:"),
        ("चाहिए चार...", "CHAHIYE 4..."),
        ("चार मैप में है,", "4 MAP MEIN HAI!"),
        ("इंडेक्स दो पर!", "INDEX 2 PAR!"),
        ("जवाब: दो और चार।", "JAWAAB: [2, 4]"),
    ],
    "edge": [
        ("एक ज़रूरी बात:", "EK ZAROORI BAAT:"),
        ("पहले चेक करो,", "PEHLE CHECK KARO"),
        ("फिर स्टोर करो।", "PHIR STORE KARO"),
        ("अगर ऐरे है", "AGAR ARRAY HAI"),
        ("पाँच, एक, पाँच", "[5, 1, 5]"),
        ("और टारगेट दस,", "AUR TARGET 10"),
        ("और आपने", "AUR AAPNE"),
        ("पहले स्टोर किया,", "PEHLE STORE KIYA"),
        ("तो पहला पाँच", "TO PEHLA 5"),
        ("खुद से ही जुड़ जाएगा,", "KHUD SE HI JUD JAYEGA"),
        ("और गलत जवाब आएगा", "AUR GALAT JAWAAB AAYEGA"),
        ("ज़ीरो, ज़ीरो!", "[0, 0]!"),
        ("सही जवाब है", "SAHI JAWAAB HAI"),
        ("ज़ीरो और दो।", "[0, 2]"),
    ],
    "code": [
        ("कोड बस", "CODE BAS"),
        ("कुछ ही लाइन का है:", "KUCH HI LINE KA HAI:"),
        ("एक खाली डिक्शनरी बनाओ।", "EK KHAALI DICTIONARY BANAO"),
        ("हर नंबर के लिए", "HAR NUMBER KE LIYE"),
        ("नीड निकालो,", "NEED NIKALO"),
        ("यानी टारगेट माइनस एक्स।", "YAANI TARGET MINUS X"),
        ("नीड मैप में है", "NEED MAP MEIN HAI"),
        ("तो दोनों इंडेक्स", "TO DONO INDEX"),
        ("रिटर्न करो,", "RETURN KARO"),
        ("वरना नंबर को", "VARNA NUMBER KO"),
        ("उसके इंडेक्स के साथ", "USKE INDEX KE SAATH"),
        ("स्टोर कर दो।", "STORE KAR DO"),
    ],
    "outro": [
        ("टाइम कॉम्प्लेक्सिटी", "TIME COMPLEXITY"),
        ("सीधा लीनियर O of N,", "SEEDHA LINEAR O(N)"),
        ("क्योंकि ऐरे पर", "KYUNKI ARRAY PAR"),
        ("सिर्फ एक बार चले।", "SIRF EK BAAR CHALE"),
        ("स्पेस भी O of N,", "SPACE BHI O(N)"),
        ("मैप के लिए।", "MAP KE LIYE"),
        ("थोड़ी मेमोरी देकर", "THODI MEMORY DEKAR"),
        ("ढेर सारा टाइम बचाया!", "DHER SAARA TIME BACHAYA!"),
        ("अगला इंटरव्यू क्वेश्चन", "AGLA INTERVIEW QUESTION"),
        ("कौन सा", "KAUN SA"),
        ("सॉल्व करवाएं?", "SOLVE KARWAYEIN?"),
        ("कमेंट में बताएं", "COMMENT MEIN BATAYEIN"),
        ("और फॉलो करें!", "AUR FOLLOW KAREIN!"),
    ],
}

for _key, _chunks in CHUNKS.items():
    assert " ".join(h for h, _ in _chunks) == NARRATION[_key], f"caption chunks drift from narration: {_key}"

SCRIPT = [(key, CHUNKS[key]) for key in NARRATION]

GREY = hexc("#8B949E")
DIM = hexc("#6E7681")


def row_x0(n, cw, gap):
    """Left edge that centres n cells in the IDE panel."""
    return PANEL[0] + (PANEL[2] - (n * cw + (n - 1) * gap)) / 2


def pops(t, t0, n, every=0.22):
    return [ease_out_back((t - t0 - every * k) / 0.3) for k in range(n)]


def seen_table(ctx, tx, ty, tw, rh, rows, t, t_on, green=None, nrows=4):
    """Glowing hash map table: rows = [(num, idx, t_insert)], green = num whose row lights up."""
    u = t - t_on
    if u < 0:
        return
    pop = max(ease_out_back(u / 0.35), 1e-3)
    h = rh * (nrows + 1) + 10
    ctx.save()
    ctx.translate(tx + tw / 2, ty + h / 2)
    ctx.scale(pop, pop)
    ctx.translate(-(tx + tw / 2), -(ty + h / 2))
    glow(ctx, tx + tw / 2, ty + h / 2, tw * 0.8, CYAN, 0.2 + 0.1 * math.sin(t * 5))
    rrect(ctx, tx, ty, tw, h, 14)
    rgba(ctx, hexc("#06202A"), 0.95)
    ctx.fill_preserve()
    rgba(ctx, CYAN, 0.25)
    ctx.set_line_width(14)
    ctx.stroke_preserve()
    rgba(ctx, CYAN)
    ctx.set_line_width(4)
    ctx.stroke()
    text(ctx, "HASH MAP  (seen)", tx + tw / 2, ty - 22, 24, CYAN, font=MONO)
    text(ctx, "NUM", tx + tw * 0.28, ty + rh / 2 + 4, 22, GREY, font=MONO)
    text(ctx, "INDEX", tx + tw * 0.72, ty + rh / 2 + 4, 22, GREY, font=MONO)
    line(ctx, [(tx + 12, ty + rh + 4), (tx + tw - 12, ty + rh + 4)], CYAN, 2, 0.5)
    line(ctx, [(tx + tw / 2, ty + 10), (tx + tw / 2, ty + h - 10)], CYAN, 2, 0.5)
    for r, (num, idx, ti) in enumerate(rows):
        v = t - ti
        if v < 0:
            continue
        ry = ty + rh * (r + 1.5) + 4
        if green == num:
            rrect(ctx, tx + 8, ry - rh / 2 + 3, tw - 16, rh - 6, 10)
            rgba(ctx, GREEN, 0.28 + 0.15 * math.sin(t * 10))
            ctx.fill()
        rp = max(ease_out_back(v / 0.3), 1e-3)
        ctx.save()
        ctx.translate(tx + tw / 2, ry)
        ctx.scale(rp, rp)
        col = GREEN if green == num else (1, 1, 1)
        text(ctx, str(num), -tw * 0.22, 0, 32, col, font=MONO)
        text(ctx, str(idx), tw * 0.22, 0, 32, col, font=MONO)
        ctx.restore()
    ctx.restore()


def loop_arc(ctx, xa, xb, y, lift, u, c, w=7):
    """Arrow arcing over the cells from xa to xb (drawn up to fraction u); xa == xb loops back on itself."""
    pts = []
    for s in range(31):
        v = s / 30 * u
        if xa == xb:
            a = math.pi * (1 + 2 * v)
            pts.append((xa + 46 * math.cos(a) * 0.9 + 46 * 0.9, y - lift * 0.5 + 46 * math.sin(a)))
        else:
            pts.append(((1 - v) ** 2 * xa + 2 * (1 - v) * v * (xa + xb) / 2 + v * v * xb,
                        (1 - v) ** 2 * y + 2 * (1 - v) * v * (y - lift) + v * v * y))
    line(ctx, pts, c, w)
    if len(pts) > 1 and u > 0.05:
        (px, py), (qx, qy) = pts[-2], pts[-1]
        arrow_head(ctx, qx, qy, math.atan2(qy - py, qx - px), 18, c)


def fmt_in(n):
    """Indian digit grouping: 49995000 -> 4,99,95,000."""
    s = str(int(n))
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    groups = []
    while len(head) > 2:
        groups.insert(0, head[-2:])
        head = head[:-2]
    return ",".join([head] + groups + [tail]) if head else ",".join(groups + [tail])


def stopwatch(ctx, x, y, r, t, c):
    circle(ctx, x, y - r - 10, r * 0.18, c)
    ctx.arc(x, y, r, 0, math.tau)
    rgba(ctx, hexc("#0D1117"))
    ctx.fill_preserve()
    rgba(ctx, c)
    ctx.set_line_width(r * 0.16)
    ctx.stroke()
    a = t * 4 - math.pi / 2
    line(ctx, [(x, y), (x + r * 0.7 * math.cos(a), y + r * 0.7 * math.sin(a))], c, r * 0.1)
    circle(ctx, x, y, r * 0.1, c)


# ============================================================ scenes

class Hook2(Hook):
    """Hook from the Short, then the promise: 2 MINUTE stamp with a ticking stopwatch."""

    def beats(self, d):
        c = self.cue
        return {"two": c("TWO", d * 0.1), "loop": c("LOOP", d * 0.2), "dimaag": c("INTERVIEWER", d * 0.8),
                "aaj": c("AAJ", d * 0.45)}

    def poses(self, d, b):
        return [(0.0, "confused"), (b["aaj"], "explain")]

    def mood_at(self, t, b):
        return "confused" if t < b["aaj"] else "happy"

    def events(self, d):
        b = self.beats(d)
        return super().events(d) + [(b["aaj"], "whoosh"), (b["aaj"] + 0.1, "kaching")]

    def hud(self, ctx, t, d, b):
        if t < b["aaj"]:
            super().hud(ctx, t, d, b)
            return
        u = t - b["aaj"]
        stamp(ctx, 540, STAMP_Y, u, 0.02, 760, 200, CYAN,
              [("SAMJHO SIRF", -48, 64, (1, 1, 1)), ("2 MINUTE MEIN", 42, 96, CYAN)])
        if u > 0.2:
            stopwatch(ctx, 985, STAMP_Y + 10, 44 * ease_out_back((u - 0.2) / 0.3), t, YELLOW)


class Problem(Board):
    """Problem statement: array pops in number by number, target 9, the pair condition, 2 + 7 = 9 -> [0, 1]."""
    tab = "problem.md"
    CW, GAP = 112, 18

    def beats(self, d):
        c = self.cue
        return {"arr": c("ARRAY", d * 0.12), "jaise": c("JAISE", d * 0.2), "tgt": c("TARGET =", d * 0.3),
                "find": c("DHOONDHO", d * 0.4), "idx": c("INDEX", d * 0.55), "plus": c("2 + 7", d * 0.7),
                "ans": c("[0, 1]", d * 0.88)}

    def poses(self, d, b):
        return [(0.0, "explain"), (b["plus"], "point")]

    def mood_at(self, t, b):
        return "happy" if t >= b["ans"] else "ok"

    def events(self, d):
        b = self.beats(d)
        return [(b["jaise"] + 0.22 * k, "pop") for k in range(4)] + \
            [(b["tgt"], "beep"), (b["plus"], "pick"), (b["ans"], "kaching")]

    def board(self, ctx, t, d, b):
        x, y, w, h = PANEL
        text(ctx, "1. Two Sum", x + 40, y + 100, 34, (1, 1, 1), font=MONO, anchor="l")
        chip(ctx, "Easy", x + w - 90, y + 100, 24, GREEN, t - 0.2, font=MONO, bold=True)
        x0 = row_x0(4, self.CW, self.GAP)
        ay = y + 250
        if t >= b["arr"]:
            text(ctx, "nums =", x + 40, ay - 90, 26, hexc("#79C0FF"), font=MONO, anchor="l",
                 a=clamp((t - b["arr"]) / 0.2))
        hit = t >= b["plus"]
        ps = pops(t, b["jaise"], 4)
        states = [(GREEN if hit and n < 2 else None, ps[n]) for n in range(4)]
        cells(ctx, x0, ay, self.CW, 100, self.GAP, states, t, idx=t >= b["idx"])
        chip(ctx, "target = 9", x + w - 150, ay - 90, 28, YELLOW, t - b["tgt"], font=MONO, bold=True)
        if t >= b["find"]:
            a = clamp((t - b["find"]) / 0.25)
            text(ctx, "nums[i] + nums[j] == target", x + w / 2, y + 400, 28, (1, 1, 1), font=MONO, a=a)
            text(ctx, "i ≠ j", x + w / 2, y + 445, 24, GREY, font=MONO, a=a)
        if t >= b["idx"] and not hit:
            for n in range(4):
                glow(ctx, cell_x(x0, self.CW, self.GAP, n), ay + 74, 30, YELLOW, 0.5 + 0.3 * math.sin(t * 8))
        if hit:
            u = t - b["plus"]
            xa, xb = cell_x(x0, self.CW, self.GAP, 0), cell_x(x0, self.CW, self.GAP, 1)
            loop_arc(ctx, xa, xb, ay - 58, 70, ease_out_cubic(u / 0.4), GREEN)
            text(ctx, "2 + 7 = 9", x + w / 2, y + 520, 48, GREEN, font=MONO, a=clamp(u / 0.2))
        chip(ctx, "return [0, 1]", x + w / 2, y + 595, 32, GREEN, t - b["ans"], font=MONO, bold=True)

    def hud(self, ctx, t, d, b):
        stamp(ctx, 540, STAMP_Y, t - 0.05, -0.02, 640, 160, CYAN, [("SAWAAL KYA HAI?", 0, 96, CYAN)])


class Brute2(Brute):
    """Brute force code, then the worst case: target 26 sits in the last pair, so all 6 pairs get checked."""
    STEPS = 6

    def beats(self, d):
        c = self.cue
        return {"loop": c("2 LOOP", d * 0.15), "har": c("AUR HAR NUMBER", d * 0.25),
                "aakhiri": c("AAKHIRI", d * 0.55), "jode": c("PEHLE 2", d * 0.65),
                "n2": d + 1, "barbaad": d + 1}

    def step_len(self, d, b):
        return max(0.3, (d - 0.9 - b["jode"]) / self.STEPS)

    def step_k(self, t, d, b):
        if t < b["jode"]:
            return -1
        return min(self.STEPS - 1, int((t - b["jode"]) / self.step_len(d, b)))

    def found_at(self, d, b):
        return b["jode"] + self.STEPS * self.step_len(d, b) - 0.25

    def events(self, d):
        b = self.beats(d)
        return [ev for ev in super().events(d) if ev[0] < d] + [(self.found_at(d, b), "kaching")]

    def board(self, ctx, t, d, b):
        super().board(ctx, t, d, b)
        x, y, w, h = PANEL
        chip(ctx, "target = 26", x + w - 105, y + 150, 24, YELLOW, t - b["aakhiri"], font=MONO, bold=True)
        u = t - self.found_at(d, b)
        if u > 0:
            chip(ctx, "11 + 15 = 26", x + w / 2 - 20, y + 445, 28, GREEN, u, font=MONO, bold=True)
            tick_mark(ctx, x + w / 2 + 150, y + 445, 20, GREEN, clamp((u - 0.2) / 0.25))


class Cost(Board):
    """N² growth: curve shoots up, counters roll to 10,000 numbers -> ~5 crore pairs, O(N²), interviewer asks."""
    accent = RED
    border = RED
    tab = "complexity.md"

    def beats(self, d):
        c = self.cue
        return {"n": c("N NUMBER", d * 0.08), "n2": c("N²", d * 0.18), "tenk": c("10,000", d * 0.3),
                "crore": c("KARODON", d * 0.4), "on2": c("O(N²)", d * 0.55), "poochh": c("INTERVIEWER", d * 0.65),
                "tez": c("TEZ", d * 0.8)}

    def poses(self, d, b):
        return [(0.0, "explain"), (b["crore"], "confused"), (b["poochh"], "explain")]

    def mood_at(self, t, b):
        return "confused" if b["crore"] <= t < b["poochh"] else "ok"

    def events(self, d):
        b = self.beats(d)
        ev = [(b["tenk"] + 0.08 * k, "tick") for k in range(10)]
        return ev + [(b["crore"], "boom"), (b["on2"], "zap"), (b["tez"], "dingdong")]

    def board(self, ctx, t, d, b):
        x, y, w, h = PANEL
        ox, oy, cw, chh = x + 80, y + 330, 300, 230
        line(ctx, [(ox, oy - chh), (ox, oy), (ox + cw, oy)], DIM, 4)
        text(ctx, "checks", ox + 8, oy - chh - 14, 20, GREY, font=MONO, anchor="l")
        text(ctx, "N", ox + cw + 18, oy, 24, GREY, font=MONO)
        k = ease_in_out((t - b["n"]) / 1.2)
        if k > 0:
            pts = [(ox + cw * v * k, oy - chh * (v * k) ** 2) for v in (i / 40 for i in range(41))]
            line(ctx, pts, RED, 7)
            glow(ctx, *pts[-1], 40, RED, 0.7)
        if t >= b["n2"]:
            text(ctx, "≈ N²", ox + cw - 10, oy - chh + 10, 40, RED, font=CAPTION_FONT, bold=False,
                 a=clamp((t - b["n2"]) / 0.2))
        rx = x + 470
        if t >= b["tenk"]:
            v = ease_out_cubic((t - b["tenk"]) / 1.0)
            n = int(lerp(4, 10000, v))
            text(ctx, "N", rx, y + 120, 24, GREY, font=MONO)
            text(ctx, fmt_in(n), rx, y + 165, 40, (1, 1, 1), font=MONO)
            text(ctx, "pairs", rx, y + 230, 24, GREY, font=MONO)
            text(ctx, fmt_in(n * (n - 1) // 2), rx, y + 275, 32, RED, font=MONO)
        chip(ctx, "≈ 5 CRORE CHECKS", x + w / 2, y + 400, 38, RED, t - b["crore"])
        if t >= b["poochh"]:
            u = t - b["poochh"]
            interviewer(ctx, x + 140, y + 505, max(ease_out_back(u / 0.3), 1e-3), t, 0.0)
            bu = t - b["tez"]
            if bu > 0:
                bp = max(ease_out_back(bu / 0.3), 1e-3)
                ctx.save()
                ctx.translate(x + 400, y + 500)
                ctx.scale(bp, bp)
                rrect(ctx, -160, -60, 320, 120, 30)
                ctx.move_to(-150, 20)
                ctx.line_to(-200, 50)
                ctx.line_to(-130, 40)
                rgba(ctx, (1, 1, 1))
                ctx.fill()
                text(ctx, "FASTER?", 0, -14, 50, hexc("#0D1117"), font=CAPTION_FONT, bold=False)
                text(ctx, "better than N²", 0, 34, 22, hexc("#30363D"), font=MONO)
                ctx.restore()

    def hud(self, ctx, t, d, b):
        if t < b["on2"]:
            stamp(ctx, 540, STAMP_Y, t - 0.05, 0.02, 640, 160, RED, [("DIKKAT KYA HAI?", 0, 96, RED)])
        else:
            badge(ctx, 540, STAMP_Y, t - b["on2"], 640, 200, RED,
                  [("TIME:", -50, 60, (1, 1, 1)), ("O(N²)", 30, 130, RED)], rot=-0.03)


class Idea(Board):
    """Flip the question: 'kisse jodun?' crossed out -> 'kitna chahiye?', need = target - x, and a hash map
    with O(1) lookup. Camera pushes into the board."""
    tab = "idea.txt"

    def beats(self, d):
        c = self.cue
        return {"palat": c("PALATNA", d * 0.08), "mat": c("YE MAT", d * 0.15), "kitna": c("KITNA", d * 0.35),
                "minus": c("TARGET MINUS", d * 0.45), "dekh": c("DEKH CHUKE", d * 0.65),
                "hm": c("HASH MAP", d * 0.75), "turant": c("TURANT", d * 0.9)}

    def poses(self, d, b):
        return [(0.0, "explain"), (b["kitna"], "point"), (b["turant"], "cheer")]

    def mood_at(self, t, b):
        return "happy" if t >= b["kitna"] else "ok"

    def events(self, d):
        b = self.beats(d)
        return [(b["palat"], "whoosh"), (b["mat"], "pop"), (b["kitna"], "zap"), (b["kitna"] + 0.1, "pop"),
                (b["minus"], "beep"), (b["hm"], "zap"), (b["turant"], "kaching")]

    def camera(self, ctx, t, d, b):
        z = 1 + 0.1 * ease_in_out((t - b["kitna"]) / 1.2)
        ctx.translate(780, 800)
        ctx.scale(z, z)
        ctx.translate(-780, -800)

    def board(self, ctx, t, d, b):
        x, y, w, h = PANEL
        cx = x + w / 2
        if t >= b["mat"]:
            chip(ctx, "ISE KISSE JODUN?", cx, y + 125, 44, GREY, t - b["mat"])
            if t >= b["kitna"]:
                k = ease_out_cubic((t - b["kitna"]) / 0.25)
                line(ctx, [(cx - 230, y + 130), (lerp(cx - 230, cx + 230, k), y + 118)], RED, 9)
        chip(ctx, "MUJHE KITNA CHAHIYE?", cx, y + 235, 46, YELLOW, t - b["kitna"])
        if t >= b["minus"]:
            a = clamp((t - b["minus"]) / 0.25)
            glow(ctx, cx, y + 335, 200, YELLOW, 0.2 * a)
            mono_line(ctx, "need = target - x", x + 70, y + 348, 36, a=a)
        rows = [(2, 0, b["hm"] + 0.3), (7, 1, b["hm"] + 0.6)]
        seen_table(ctx, x + 110, y + 440, 380, 44, rows if t >= b["hm"] else [], t, b["dekh"], nrows=2)
        if t >= b["turant"]:
            chip(ctx, "LOOKUP = O(1)", cx, y + 605, 30, GREEN, t - b["turant"], font=MONO, bold=True)

    def hud(self, ctx, t, d, b):
        if t < b["hm"]:
            stamp(ctx, 540, STAMP_Y, t - 0.05, -0.02, 680, 160, YELLOW, [("ASLI TRICK", 0, 110, YELLOW)])
        else:
            badge(ctx, 540, STAMP_Y, t - b["hm"], 680, 170, CYAN, [("HASH MAP", 0, 120, CYAN)], rot=0.02)


class DryRun(Board):
    """[3, 8, 4, 11, 6], target 10: four misses get stored, then 6 needs 4 -> found at index 2 -> [2, 4]."""
    tab = "dry_run.py"
    VALS = (3, 8, 4, 11, 6)
    TARGET = 10
    CW, GAP = 96, 14

    def beats(self, d):
        c = self.cue
        b = {"intro": c("ARRAY HAI", d * 0.06), "arr": c("[3,", d * 0.1), "tgt": c("TARGET 10", d * 0.15),
             "found": c("4 MAP", d * 0.82), "ans": c("JAWAAB", d * 0.92)}
        keys = ("3 AAYA", "8 AAYA", "4 AAYA", "11:", "6 AAYA")
        b["s"] = [c(k, d * (0.2 + 0.13 * i)) for i, k in enumerate(keys)]
        return b

    def store_at(self, k, b):
        return b["s"][k + 1] - 0.35

    def poses(self, d, b):
        return [(0.0, "explain"), (b["s"][0], "point"), (b["ans"], "cheer")]

    def mood_at(self, t, b):
        return "happy" if t >= b["found"] else "ok"

    def events(self, d):
        b = self.beats(d)
        ev = [(b["arr"] + 0.15 * k, "pop") for k in range(5)] + [(b["tgt"], "beep")]
        for k in range(5):
            ev.append((b["s"][k], "pick"))
            if k < 4:
                ev += [(b["s"][k] + 0.7, "tock"), (self.store_at(k, b), "pop")]
        return ev + [(b["found"], "kaching"), (b["ans"], "boom")]

    def board(self, ctx, t, d, b):
        x, y, w, h = PANEL
        s = b["s"]
        cur = max([k for k in range(5) if s[k] <= t], default=None)
        found = t >= b["found"]
        if cur is not None:
            text(ctx, f"step {cur + 1}/5", x + 40, y + 100, 24, GREY, font=MONO, anchor="l")
        chip(ctx, f"target = {self.TARGET}", x + w - 130, y + 100, 26, YELLOW, t - b["tgt"], font=MONO, bold=True)
        x0 = row_x0(5, self.CW, self.GAP)
        ay = y + 240
        ps = pops(t, b["arr"], 5, 0.15)
        states = []
        for n in range(5):
            c = None
            if t >= b["ans"] and n in (2, 4):
                c = GREEN
            elif n == cur:
                c = CYAN
            elif cur is not None and n < cur:
                c = hexc("#2E5A66")
            states.append((c, ps[n]))
        cells(ctx, x0, ay, self.CW, 84, self.GAP, states, t, vals=self.VALS)
        if cur is not None:                                     # pointer slides between cells
            u = ease_out_cubic((t - s[cur]) / 0.3)
            px = lerp(cell_x(x0, self.CW, self.GAP, max(cur - 1, 0)), cell_x(x0, self.CW, self.GAP, cur), u)
            bob = 5 * math.sin(t * 8)
            arrow_head(ctx, px, ay - 66 + bob, math.pi / 2, 20, CYAN)
            text(ctx, "x", px, ay - 100 + bob, 26, CYAN, font=MONO)
            xv = self.VALS[cur]
            a = clamp((t - s[cur] - 0.15) / 0.2)
            text(ctx, f"{self.TARGET} - {xv} = {self.TARGET - xv}", x + w / 2, y + 360, 42, YELLOW, font=MONO, a=a)
            text(ctx, "in map?", x + w / 2, y + 400, 22, CYAN, font=MONO, a=a)
        rows = [(self.VALS[k], k, self.store_at(k, b)) for k in range(4)]
        seen_table(ctx, x + 50, y + 450, 300, 36, rows, t, b["intro"], green=4 if found else None)
        vx = x + 470
        if cur is not None and cur < 4 and t >= s[cur] + 0.7:
            cross_mark(ctx, vx, y + 480, 20, RED, clamp((t - s[cur] - 0.7) / 0.15))
            text(ctx, "NAHI", vx, y + 525, 26, RED, font=CAPTION_FONT, bold=False)
            if t >= self.store_at(cur, b):
                text(ctx, "→ store", vx, y + 560, 22, GREY, font=MONO)
        if found:
            tick_mark(ctx, vx, y + 490, 26, GREEN, clamp((t - b["found"]) / 0.25))
            text(ctx, "4 @ index 2", vx, y + 540, 22, GREEN, font=MONO)
        chip(ctx, "[2, 4]", vx, y + 595, 34, GREEN, t - b["ans"], font=MONO, bold=True)

    def hud(self, ctx, t, d, b):
        stamp(ctx, 540, STAMP_Y, t - 0.05, 0.02, 560, 160, CYAN, [("DRY RUN", 0, 116, CYAN)])


class Edge(Board):
    """Order matters: CHECK then STORE. [5, 1, 5] target 10 — storing first makes 5 match itself ([0, 0]);
    the right order finds [0, 2]."""
    accent = ORANGE
    border = ORANGE
    tab = "edge_case.py"
    VALS = (5, 1, 5)
    CW, GAP = 120, 30

    def beats(self, d):
        c = self.cue
        return {"chk": c("PEHLE CHECK", d * 0.08), "sto": c("PHIR STORE", d * 0.15), "arr": c("[5,", d * 0.28),
                "tgt": c("TARGET 10", d * 0.35), "wrong": c("PEHLE STORE KIYA", d * 0.45),
                "self": c("KHUD SE", d * 0.58), "galat": c("[0, 0]", d * 0.72), "sahi": c("SAHI", d * 0.82)}

    def poses(self, d, b):
        return [(0.0, "explain"), (b["self"], "point"), (b["galat"], "confused"), (b["sahi"], "cheer")]

    def mood_at(self, t, b):
        if t >= b["sahi"]:
            return "happy"
        return "confused" if t >= b["galat"] else "ok"

    def events(self, d):
        b = self.beats(d)
        return [(b["chk"], "pop"), (b["sto"], "pop"), (b["arr"], "pick"), (b["wrong"], "beep"),
                (b["self"], "zap"), (b["galat"], "alarm"), (b["sahi"], "kaching")]

    def board(self, ctx, t, d, b):
        x, y, w, h = PANEL
        chip(ctx, "1. CHECK", x + 170, y + 110, 34, CYAN, t - b["chk"], font=MONO, bold=True)
        if t >= b["sto"]:
            arrow_head(ctx, x + 300, y + 110, 0, 16, (1, 1, 1))
        chip(ctx, "2. STORE", x + 430, y + 110, 34, YELLOW, t - b["sto"], font=MONO, bold=True)
        x0 = row_x0(3, self.CW, self.GAP)
        ay = y + 290
        sahi = t >= b["sahi"]
        wrong = b["wrong"] <= t < b["sahi"]
        states = [((GREEN if sahi and n in (0, 2) else (RED if wrong and t >= b["self"] and n == 0 else None)),
                   p) for n, p in enumerate(pops(t, b["arr"], 3, 0.18))]
        cells(ctx, x0, ay, self.CW, 100, self.GAP, states, t, vals=self.VALS)
        chip(ctx, "target = 10", x + w - 120, y + 190, 24, YELLOW, t - b["tgt"], font=MONO, bold=True)
        xa, xc = cell_x(x0, self.CW, self.GAP, 0), cell_x(x0, self.CW, self.GAP, 2)
        if wrong:
            text(ctx, "store → check", x + w / 2, y + 420, 30, RED, font=MONO)
            text(ctx, "seen = {5: 0}  then 10-5 = 5 in seen?", x + w / 2, y + 462, 20, GREY, font=MONO)
            if t >= b["self"]:
                loop_arc(ctx, xa - 46 * 0.9, xa - 46 * 0.9, ay - 60, 60,
                         ease_out_cubic((t - b["self"]) / 0.5), RED)
                text(ctx, "khud se!", xa + 120, ay - 110, 30, RED, font=CAPTION_FONT, bold=False)
            if t >= b["galat"]:
                u = t - b["galat"]
                text(ctx, "[0, 0]", x + w / 2, y + 550, 70, RED, font=MONO, a=clamp(u / 0.15))
                cross_mark(ctx, x + w / 2, y + 550, 60, RED, clamp((u - 0.2) / 0.15))
        if sahi:
            u = t - b["sahi"]
            text(ctx, "check → store", x + w / 2, y + 420, 30, GREEN, font=MONO)
            loop_arc(ctx, xc, xa, ay - 58, 90, ease_out_cubic(u / 0.5), GREEN)
            text(ctx, "[0, 2]", x + w / 2, y + 540, 70, GREEN, font=MONO, a=clamp(u / 0.2))
            tick_mark(ctx, x + w / 2 + 160, y + 540, 26, GREEN, clamp((u - 0.2) / 0.25))

    def hud(self, ctx, t, d, b):
        if t < b["sahi"]:
            stamp(ctx, 540, STAMP_Y, t - 0.05, -0.02, 620, 160, ORANGE, [("EDGE CASE!", 0, 110, ORANGE)])
        else:
            badge(ctx, 540, STAMP_Y, t - b["sahi"], 760, 170, GREEN, [("CHECK, PHIR STORE", 0, 92, GREEN)])


class Code(Board):
    """The solution typed out; each line lights up as the narrator explains it, with a plain-language note."""
    tab = "two_sum.py"
    CODE = ("def twoSum(nums, target):",
            "    seen = {}",
            "    for i, x in enumerate(nums):",
            "        need = target - x",
            "        if need in seen:",
            "            return [seen[need], i]",
            "        seen[x] = i")

    def beats(self, d):
        c = self.cue
        return {"dict": c("DICTIONARY", d * 0.18), "har": c("HAR NUMBER", d * 0.32), "need": c("NEED NIKALO", d * 0.4),
                "inmap": c("NEED MAP", d * 0.55), "ret": c("RETURN", d * 0.68), "varna": c("VARNA", d * 0.75)}

    def stages(self, b):
        return [(b["dict"], (1,), "number → index yaad rakho"), (b["har"], (2,), "ek hi loop, ek hi pass"),
                (b["need"], (3,), "kitna chahiye?"), (b["inmap"], (4,), "lookup = O(1)"),
                (b["ret"], (5,), "mil gaya → dono index"), (b["varna"], (6,), "nahi mila → store")]

    def poses(self, d, b):
        return [(0.0, "explain"), (b["dict"], "point")]

    def mood_at(self, t, b):
        return "happy"

    def events(self, d):
        b = self.beats(d)
        ev = [(0.15 + 0.12 * k, "tick" if k % 2 else "tock") for k in range(14)]
        return ev + [(s, "pick") for s, _, _ in self.stages(b)]

    def board(self, ctx, t, d, b):
        x, y, w, h = PANEL
        stage = [s for s in self.stages(b) if s[0] <= t]
        hl, note = (stage[-1][1], stage[-1][2]) if stage else ((), None)
        code_block(ctx, self.CODE, x + 62, y + 115, 0.1, t, size=24, lh=46, cps=70, hl=hl, hl_c=CYAN)
        if note:
            chip(ctx, note, x + w / 2, y + 560, 28, YELLOW, t - stage[-1][0], font=MONO, bold=True)

    def hud(self, ctx, t, d, b):
        stamp(ctx, 540, STAMP_Y, t - 0.05, 0.02, 620, 160, CYAN, [("THE CODE", 0, 116, CYAN)])


class Outro2(Outro):
    """O(N) chart, then a Brute vs Hash Map scorecard (time/space trade-off), then the CTA and FOLLOW click."""

    def beats(self, d):
        b = super().beats(d)
        b["space"] = self.cue("SPACE", d * 0.3)
        b["memory"] = self.cue("MEMORY", d * 0.4)
        return b

    def events(self, d):
        b = self.beats(d)
        return super().events(d) + [(b["space"], "pop"), (b["memory"], "kaching")]

    def board(self, ctx, t, d, b):
        if not b["space"] <= t < b["agla"]:
            super().board(ctx, t, d, b)
            return
        x, y, w, h = PANEL
        u = t - b["space"]
        cols = (x + 130, x + 300, x + 470)
        text(ctx, "BRUTE", cols[1], y + 120, 34, RED, font=CAPTION_FONT, bold=False)
        text(ctx, "HASH MAP", cols[2], y + 120, 34, CYAN, font=CAPTION_FONT, bold=False)
        line(ctx, [(x + 40, y + 155), (x + w - 40, y + 155)], DIM, 2)
        for r, (lab, bv, hv, hc) in enumerate((("TIME", "O(N²)", "O(N)", GREEN), ("SPACE", "O(1)", "O(N)", YELLOW))):
            ry = y + 220 + r * 110
            a = clamp((u - 0.2 * r) / 0.25)
            text(ctx, lab, cols[0], ry, 28, GREY, font=MONO, a=a)
            text(ctx, bv, cols[1], ry, 40, RED if r == 0 else (1, 1, 1), font=MONO, a=a)
            text(ctx, hv, cols[2], ry, 40, hc, font=MONO, a=a)
        if t >= b["memory"]:
            mu = t - b["memory"]
            chip(ctx, "thodi memory  →  bahut time", x + w / 2, y + 480, 28, YELLOW, mu, font=MONO, bold=True)
            tick_mark(ctx, x + w / 2, y + 580, 34, GREEN, clamp((mu - 0.3) / 0.3))


SCENE_CLASSES = {"hook": Hook2, "problem": Problem, "brute": Brute2, "cost": Cost, "idea": Idea,
                 "dryrun": DryRun, "edge": Edge, "code": Code, "outro": Outro2}
