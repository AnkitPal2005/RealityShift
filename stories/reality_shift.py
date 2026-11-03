"""Story: Reality Shift — 2014 vs aaj ka Bharat (Modi ji ke faisle)."""

import math

import cairo

from engine import *  # noqa: F401,F403

TOPIC = "2014 VS AAJ KA BHARAT"
OUTPUTS = {"edge": "reality_shift_modi_free_voice.mp4", "elevenlabs": "reality_shift_modi_full_visual.mp4"}

# Narration goes to the TTS verbatim (punctuation drives the dramatic pacing); only
# breaths longer than MAX_GAP are shortened, and each scene lasts as long as its clip.
CLEAN_PUNCTUATION = False
MAX_GAP = 0.3
TAIL_PAD = 0.0
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 104
EDGE_VOICE = "hi-IN-MadhurNeural"     # authoritative Indian male
EDGE_RATE = "+5%"
EDGE_PITCH = "+0Hz"
EL_VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam: deep, authoritative narrator
EL_SETTINGS = {"stability": 0.40, "similarity_boost": 0.85, "style": 0.35}

# Exact Devanagari narration per scene (numbers spelled out so the voice says them right).
NARRATION = {
    "hook": "रुको! दो हज़ार चौदह से पहले का भारत, और आज का भारत। एक अकेले नेता ने कैसे पूरी दुनिया में "
            "देश का डंका बजा दिया? ये चार बड़े फैसले सुनकर हर भारतीय का सीना गर्व से चौड़ा हो जाएगा!",
    "mandir": "पहला— पाँच सौ साल का लंबा इंतज़ार खत्म! अयोध्या में भव्य राम मंदिर का निर्माण करवाया, "
              "और काशी से लेकर उज्जैन तक हमारी धरोहर को नया सम्मान दिलाया!",
    "iron": "दूसरा— जिसे कोई हाथ लगाने से डरता था, उस धारा तीन सौ सत्तर को एक झटके में खत्म करके कश्मीर "
            "को हमेशा के लिए भारत का अभिन्न अंग बनाया! और सर्जिकल स्ट्राइक से दुश्मन को घर में घुसकर "
            "जवाब दिया!",
    "world": "तीसरा— आज अमेरिका हो या रूस, कोई भारत को दबा नहीं सकता! सस्ता तेल खरीदना हो या चंद्रयान "
             "तीन को चांद पर उतारना, मोदी जी ने भारत को ग्लोबल सुपर-पावर बना दिया!",
    "outro": "क्या आपको लगता है नरेंद्र मोदी भारत के इतिहास के सबसे मजबूत प्रधानमंत्री हैं? कमेंट में "
             "'जय हिंद' ज़रूर लिखें, और ऐसी ही वीडियोज़ के लिए रियलिटी शिफ्ट को अभी सब्सक्राइब करें!",
}

# (hindi chunk, hinglish caption): chunks split only at spaces so they join back into
# NARRATION, and each caption is aligned to the edge-tts boundary of its first word.
CHUNKS = {
    "hook": [
        ("रुको!", "RUKO!"),
        ("दो हज़ार चौदह", "2014"),
        ("से पहले का भारत,", "SE PEHLE KA BHARAT"),
        ("और आज का भारत।", "AUR AAJ KA BHARAT!"),
        ("एक अकेले नेता ने", "EK AKELE NETA NE"),
        ("कैसे पूरी", "KAISE POORI"),
        ("दुनिया में", "DUNIYA MEIN"),
        ("देश का डंका", "DESH KA DANKA"),
        ("बजा दिया?", "BAJA DIYA?"),
        ("ये चार बड़े फैसले", "YEH 4 BADE FAISLE"),
        ("सुनकर हर", "SUNKAR HAR"),
        ("भारतीय का सीना", "BHARTIYA KA SEENA"),
        ("गर्व से चौड़ा", "GARV SE CHAUDA"),
        ("हो जाएगा!", "HO JAYEGA!"),
    ],
    "mandir": [
        ("पहला—", "PEHLA!"),
        ("पाँच सौ साल का", "500 SAAL KA"),
        ("लंबा इंतज़ार", "LAMBA INTEZAAR"),
        ("खत्म!", "KHATAM!"),
        ("अयोध्या में", "AYODHYA MEIN"),
        ("भव्य राम मंदिर", "BHAVYA RAM MANDIR"),
        ("का निर्माण करवाया,", "KA NIRMAN KARWAYA"),
        ("और काशी से", "AUR KASHI SE"),
        ("लेकर उज्जैन तक", "LEKAR UJJAIN TAK"),
        ("हमारी धरोहर को", "HAMARI DHAROHAR KO"),
        ("नया सम्मान", "NAYA SAMMAN"),
        ("दिलाया!", "DILAYA!"),
    ],
    "iron": [
        ("दूसरा—", "DOOSRA!"),
        ("जिसे कोई हाथ", "JISE KOI HAATH"),
        ("लगाने से डरता था,", "LAGANE SE DARTA THA"),
        ("उस धारा तीन सौ सत्तर को", "US DHARA 370 KO"),
        ("एक झटके में", "EK JHATKE MEIN"),
        ("खत्म करके", "KHATAM KARKE"),
        ("कश्मीर को", "KASHMIR KO"),
        ("हमेशा के लिए", "HAMESHA KE LIYE"),
        ("भारत का अभिन्न अंग", "BHARAT KA ABHINN ANG"),
        ("बनाया!", "BANAYA!"),
        ("और सर्जिकल स्ट्राइक से", "AUR SURGICAL STRIKE SE"),
        ("दुश्मन को घर में", "DUSHMAN KO GHAR MEIN"),
        ("घुसकर जवाब दिया!", "GHUSKAR JAWAB DIYA!"),
    ],
    "world": [
        ("तीसरा—", "TEESRA!"),
        ("आज अमेरिका हो", "AAJ AMERICA HO"),
        ("या रूस,", "YA RUSSIA"),
        ("कोई भारत को", "KOI BHARAT KO"),
        ("दबा नहीं सकता!", "DABA NAHI SAKTA!"),
        ("सस्ता तेल खरीदना हो", "SASTA TEL KHAREEDNA HO"),
        ("या चंद्रयान तीन को", "YA CHANDRAYAAN-3 KO"),
        ("चांद पर उतारना,", "CHAND PAR UTAARNA"),
        ("मोदी जी ने", "MODI JI NE"),
        ("भारत को ग्लोबल", "BHARAT KO GLOBAL"),
        ("सुपर-पावर", "SUPER-POWER"),
        ("बना दिया!", "BANA DIYA!"),
    ],
    "outro": [
        ("क्या आपको लगता है", "KYA AAPKO LAGTA HAI"),
        ("नरेंद्र मोदी", "NARENDRA MODI"),
        ("भारत के इतिहास के", "BHARAT KE ITIHAAS KE"),
        ("सबसे मजबूत", "SABSE MAZBOOT"),
        ("प्रधानमंत्री हैं?", "PRADHAN MANTRI HAIN?"),
        ("कमेंट में", "COMMENT MEIN"),
        ("'जय हिंद'", "'JAI HIND'"),
        ("ज़रूर लिखें,", "ZAROOR LIKHEIN"),
        ("और ऐसी ही", "AUR AISI HI"),
        ("वीडियोज़ के लिए", "VIDEOS KE LIYE"),
        ("रियलिटी शिफ्ट को", "REALITY SHIFT KO"),
        ("अभी सब्सक्राइब करें!", "ABHI SUBSCRIBE KAREIN!"),
    ],
}

HOT_WORDS = {"RUKO", "2014", "KHATAM", "MANDIR", "370", "SURGICAL", "JAWAB", "SUPER-POWER", "MAZBOOT",
             "JAI", "HIND", "SUBSCRIBE"}

for _key, _chunks in CHUNKS.items():
    assert " ".join(h for h, _ in _chunks) == NARRATION[_key], f"caption chunks drift from narration: {_key}"

SCRIPT = [(key, CHUNKS[key]) for key in NARRATION]

SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
NAVY = hexc("#000080")
GOLD = hexc("#FFD60A")
FACE = hexc("#C98E62")
FACE_SH = hexc("#A8714A")
HAIR = hexc("#EDEDED")
KURTA = hexc("#F4EFE3")
SIL = hexc("#07050C")
CAMO = [hexc(c) for c in ("#6B7A3A", "#2F3A1C", "#8A8F5A")]
TRICOLOR = (SAFFRON, (1.0, 1.0, 1.0), INDIA_GREEN)


# ============================================================ statesman portrait

def _ellipse(ctx, x, y, rx, ry):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(rx, ry)
    ctx.new_sub_path()
    ctx.arc(0, 0, 1, 0, math.tau)
    ctx.restore()


SHOULDERS = ((-195, 70), (195, 70))
BODY_LEN = 1300  # torso runs off the bottom of the frame, so there is no visible cut


def _arms(pose, t):
    """(elbow, hand) for the left and right arm in neck-base coordinates."""
    down = ((-250, 330), (-240, 560)), ((250, 330), (240, 560))
    if pose == "wave":
        sway = math.sin(t * 6)
        return down[0], ((330 + 10 * sway, -20), (355 + 30 * sway, -250 + 8 * math.cos(t * 6)))
    if pose == "namaste":
        return ((-235, 340), (-40, 270)), ((235, 340), (40, 270))
    if pose == "command":
        return ((-330, 290), (-215, 430)), ((330, 290), (215, 430))
    if pose == "address":
        return down[0], ((320, 250), (420, 70 + 15 * math.sin(t * 3)))
    return down


def _jacket_path(ctx, full):
    if full:  # army jacket covers the whole torso
        ctx.move_to(-70, 0)
        ctx.curve_to(-170, 5, -235, 40, -248, 150)
        ctx.line_to(-270, BODY_LEN)
        ctx.line_to(270, BODY_LEN)
        ctx.line_to(248, 150)
        ctx.curve_to(235, 40, 170, 5, 70, 0)
    else:     # sleeveless Nehru jacket over the kurta
        ctx.move_to(-62, 4)
        ctx.curve_to(-140, 10, -190, 40, -200, 150)
        ctx.line_to(-225, BODY_LEN)
        ctx.line_to(225, BODY_LEN)
        ctx.line_to(200, 150)
        ctx.curve_to(190, 40, 140, 10, 62, 4)
    ctx.close_path()


def _figure(ctx, t, pose, look, paint, detail):
    """One pass of the portrait; paint(c) maps every colour (identity, silhouette or rim)."""
    def fill(c, a=1.0):
        rgba(ctx, paint(c), a)
        ctx.fill()

    jacket, camo, smile = look["jacket"], look["camo"], look["smile"]
    kurta = look["kurta"]
    sleeve = jacket if camo else kurta
    # kurta torso
    ctx.move_to(-70, 0)
    ctx.curve_to(-170, 5, -235, 40, -248, 150)
    ctx.line_to(-268, BODY_LEN)
    ctx.line_to(268, BODY_LEN)
    ctx.line_to(248, 150)
    ctx.curve_to(235, 40, 170, 5, 70, 0)
    ctx.close_path()
    fill(kurta)
    if jacket:
        _jacket_path(ctx, camo)
        fill(jacket)
        if detail:
            if camo:
                ctx.save()
                _jacket_path(ctx, True)
                ctx.clip()
                for i in range(46):
                    _ellipse(ctx, -280 + 560 * rnd(i, 1), 900 * rnd(i, 2), 30 + 45 * rnd(i, 3), 16 + 26 * rnd(i, 4))
                    fill(CAMO[i % 3])
                ctx.restore()
            line(ctx, [(0, 30), (0, BODY_LEN)], paint(shade(jacket, 0.7)), 4)
            for k in range(6):
                circle(ctx, 16, 150 + k * 105, 9, paint(shade(jacket, 1.35) if not camo else hexc("#2F3A1C")))
            line(ctx, [(-165, 230), (-85, 224)], paint(shade(jacket, 0.7)), 6)
            for side in (-1, 1):
                line(ctx, [(side * 175, 560), (side * 85, 554)], paint(shade(jacket, 0.7)), 6)
            if not camo:  # saffron pocket square
                ctx.move_to(-160, 228)
                ctx.line_to(-130, 196)
                ctx.line_to(-100, 226)
                ctx.close_path()
                fill(SAFFRON if jacket != SAFFRON else KURTA)
    if look["stole"]:  # angavastram draped over the left shoulder
        ctx.move_to(-215, 60)
        ctx.line_to(-118, 26)
        ctx.curve_to(0, 240, 140, 430, 268, 600)
        ctx.line_to(268, 730)
        ctx.curve_to(120, 520, -20, 320, -150, 120)
        ctx.line_to(-160, BODY_LEN)
        ctx.line_to(-235, BODY_LEN)
        ctx.close_path()
        fill(SAFFRON)
        if detail:
            line(ctx, [(-118, 30), (0, 244), (140, 434), (268, 604)], paint(GOLD), 7)
            line(ctx, [(-150, 124), (-160, BODY_LEN)], paint(GOLD), 7)
    # neck + mandarin collar
    ctx.rectangle(-38, -70, 76, 82)
    fill(FACE)
    rrect(ctx, -66, -24, 132, 40, 14)
    fill(shade(jacket or kurta, 0.85))

    # ---- head (centre 0, -128)
    _ellipse(ctx, 0, -150, 112, 122)          # white hair behind
    fill(HAIR)
    for side in (-1, 1):
        _ellipse(ctx, side * 100, -130, 20, 32)
        fill(FACE_SH)
    _ellipse(ctx, 0, -128, 98, 114)
    fill(FACE)
    ctx.save()                                 # receding white hairline
    _ellipse(ctx, 0, -128, 98, 114)
    ctx.clip()
    _ellipse(ctx, 0, -258, 125, 75)
    fill(HAIR)
    ctx.restore()
    # full white beard
    ctx.move_to(-98, -140)
    ctx.curve_to(-100, -60, -70, 10, 0, 22)
    ctx.curve_to(70, 10, 100, -60, 98, -140)
    ctx.line_to(82, -140)
    ctx.curve_to(80, -95, 55, -72, 30, -80)
    ctx.curve_to(15, -90, -15, -90, -30, -80)
    ctx.curve_to(-55, -72, -80, -95, -82, -140)
    ctx.close_path()
    fill(HAIR)
    if detail:
        for side in (-1, 1):
            x = side * 38
            line(ctx, [(x - 26 * side, -176), (x, -186), (x + 26 * side, -178)], HAIR, 10)
            if smile:
                line(ctx, [(x - 14, -148), (x, -157), (x + 14, -148)], hexc("#2A1A12"), 5)
            else:
                _ellipse(ctx, x, -150, 12, 7)
                fill(hexc("#2A1A12"))
                circle(ctx, x + 4, -153, 2.5, (1, 1, 1))
        line(ctx, [(-2, -150), (-10, -108), (6, -102)], FACE_SH, 5)
        if smile:
            ctx.move_to(-30, -72)
            ctx.curve_to(-12, -46, 12, -46, 30, -72)
            ctx.close_path()
            fill(hexc("#5A1E1E"))
            ctx.move_to(-24, -70)
            ctx.curve_to(-10, -61, 10, -61, 24, -70)
            ctx.close_path()
            fill((1, 1, 1))
        else:
            line(ctx, [(-18, -64), (18, -64)], hexc("#5A1E1E"), 5)
    ctx.move_to(-42, -73)                      # moustache
    ctx.curve_to(-25, -99, 25, -99, 42, -73)
    ctx.curve_to(20, -82, -20, -82, -42, -73)
    ctx.close_path()
    fill(HAIR)
    if detail:                                 # rimless glasses
        for x in (-38, 38):
            rrect(ctx, x - 34, -172, 68, 44, 14)
            rgba(ctx, (1, 1, 1), 0.1)
            ctx.fill_preserve()
            rgba(ctx, hexc("#E8D9A8"), 0.7)
            ctx.set_line_width(3)
            ctx.stroke()
        line(ctx, [(-4, -158), (4, -158)], hexc("#E8D9A8"), 3, 0.8)
        for side in (-1, 1):
            line(ctx, [(side * 72, -158), (side * 97, -150)], hexc("#E8D9A8"), 3, 0.8)

    # ---- arms, in front of the torso
    for sh, (el, hd) in zip(SHOULDERS, _arms(pose, t)):
        wrist = (lerp(el[0], hd[0], 0.78), lerp(el[1], hd[1], 0.78))
        line(ctx, [sh, el, wrist], paint(sleeve), 80)
        line(ctx, [wrist, hd], paint(FACE), 50)
        if pose == "namaste":
            continue
        circle(ctx, *hd, 36, paint(FACE))
    if pose == "wave":
        hx, hy = _arms(pose, t)[1][1]
        tilt = 0.25 * math.sin(t * 6)
        for k, a in enumerate((-0.45, -0.15, 0.15, 0.45, -1.25)):
            ln = 45 if k == 4 else 66 - 6 * abs(k - 1.5)
            line(ctx, [(hx, hy), (hx + ln * math.sin(a + tilt), hy - ln * math.cos(a + tilt))], paint(FACE), 19)
    elif pose == "address":
        hx, hy = _arms(pose, t)[1][1]
        line(ctx, [(hx, hy), (hx + 6, hy - 64)], paint(FACE), 18)
    elif pose == "namaste":
        ctx.move_to(0, 95)
        ctx.curve_to(48, 135, 48, 245, 0, 290)
        ctx.curve_to(-48, 245, -48, 135, 0, 95)
        ctx.close_path()
        fill(FACE)
        if detail:
            line(ctx, [(0, 110), (0, 285)], FACE_SH, 4)


def leader(ctx, x, y, s, t, pose="stand", jacket=SAFFRON, kurta=KURTA, camo=False, stole=False,
           smile=False, shadow=False, rim=SAFFRON):
    """Stylised vector portrait of the PM (white hair and beard, rimless glasses, kurta +
    Nehru jacket) with (x, y) at the neck base, rim-lit in saffron/gold.
    shadow=True draws a backlit silhouette."""
    look = {"jacket": jacket, "kurta": kurta, "camo": camo, "stole": stole, "smile": smile}
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    # rim light: the outline offset outward, soft and wide first, then tight and hot
    for spread, a in ((20, 0.35), (8, 0.95)):
        ctx.push_group()
        for dx, dy in ((-spread, -spread * 0.4), (spread, -spread * 0.4), (0, -spread)):
            ctx.save()
            ctx.translate(dx, dy)
            _figure(ctx, t, pose, look, lambda c: rim if a > 0.5 else GOLD, False)
            ctx.restore()
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(a)
    _figure(ctx, t, pose, look, (lambda c: SIL) if shadow else (lambda c: c), not shadow)
    ctx.restore()


def aura(ctx, x, y, s, t, c):
    """Pulsing saffron/gold halo with slow god-rays, centred on the head."""
    p = 1 + 0.06 * math.sin(t * 2.2)
    glow(ctx, x, y + 220 * s, 760 * s * p, c, 0.45)
    glow(ctx, x, y, 400 * s * p, GOLD, 0.4)
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(t * 0.15)
    for k in range(18):
        a = k / 18 * math.tau
        ctx.move_to(0, 0)
        ctx.arc(0, 0, 1000 * s, a - 0.035, a + 0.035)
        ctx.close_path()
    g = cairo.RadialGradient(0, 0, 100 * s, 0, 0, 1000 * s)
    g.add_color_stop_rgba(0, *GOLD, 0.22)
    g.add_color_stop_rgba(1, *GOLD, 0)
    ctx.set_source(g)
    ctx.fill()
    ctx.restore()


def hero(ctx, x, y, s, t, d, zoom=1.0, **kw):
    """Character layer: aura + rim-lit portrait with a slow Ken Burns push-in, a gentle
    float and breathing, so it is never static."""
    kb = zoom * (1 + 0.08 * ease_in_out(t / max(d, 0.1)))
    bob = 9 * math.sin(t * 1.6)
    breathe = 1 + 0.012 * math.sin(t * 2.3)
    aura(ctx, x, y + bob - 135 * s * kb, s * kb, t, kw.get("rim", SAFFRON))
    ctx.save()
    ctx.translate(x, y + bob + 400 * s)
    ctx.scale(kb, kb * breathe)
    ctx.rotate(0.015 * math.sin(t * 1.1))
    ctx.translate(0, -400 * s)
    leader(ctx, 0, 0, s, t, **kw)
    ctx.restore()


# ============================================================ props

def chakra(ctx, x, y, r, rot=0.0, c=NAVY):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.arc(0, 0, r, 0, math.tau)
    rgba(ctx, c)
    ctx.set_line_width(r * 0.12)
    ctx.stroke()
    for k in range(24):
        a = k / 24 * math.tau
        line(ctx, [(0, 0), (r * 0.92 * math.cos(a), r * 0.92 * math.sin(a))], c, r * 0.05)
    circle(ctx, 0, 0, r * 0.16, c)
    ctx.restore()


def _flag_paint(ctx, kind, w, h):
    def band(x, y, bw, bh, col):
        ctx.rectangle(x, y, bw, bh)
        rgba(ctx, hexc(col) if isinstance(col, str) else col)
        ctx.fill()

    if kind == "in":
        for k, c in enumerate(TRICOLOR):
            band(0, k * h / 3, w, h / 3 + 1, c)
        chakra(ctx, w / 2, h / 2, h * 0.14)
    elif kind == "ru":
        for k, c in enumerate(("#FFFFFF", "#0039A6", "#D52B1E")):
            band(0, k * h / 3, w, h / 3 + 1, c)
    elif kind == "fr":
        for k, c in enumerate(("#0055A4", "#FFFFFF", "#EF4135")):
            band(k * w / 3, 0, w / 3 + 1, h, c)
    elif kind == "de":
        for k, c in enumerate(("#000000", "#DD0000", "#FFCE00")):
            band(0, k * h / 3, w, h / 3 + 1, c)
    elif kind == "jp":
        band(0, 0, w, h, "#FFFFFF")
        circle(ctx, w / 2, h / 2, h * 0.3, hexc("#BC002D"))
    elif kind == "us":
        for k in range(13):
            band(0, k * h / 13, w, h / 13 + 1, "#B22234" if k % 2 == 0 else "#FFFFFF")
        band(0, 0, w * 0.4, h * 7 / 13, "#3C3B6E")


def flag(ctx, x, y, w, h, kind, t, pole=0.0, phase=0.0):
    """Waving flag with its top-left corner at (x, y), sliced into strips that ripple."""
    if pole:
        line(ctx, [(x - 4, y - 10), (x - 4, y + pole)], hexc("#C9C9C9"), 7)
    n = 14
    for i in range(n):
        dy = 7 * math.sin(t * 5 - i * 0.6 + phase) * (i / n)
        ctx.save()
        ctx.rectangle(x + w * i / n, y + dy, w / n + 1, h)
        ctx.clip()
        ctx.translate(x, y + dy)
        _flag_paint(ctx, kind, w, h)
        ctx.restore()


def stamp(ctx, x, y, u, rot, w, h, c, lines):
    """Card that slams in (u = 0 -> 1) with a coloured border and stacked text lines."""
    if u < 0:
        return
    sc = lerp(2.6, 1.0, ease_out_cubic(u / 0.2))
    a = min(1.0, u / 0.12)
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(sc, sc)
    rrect(ctx, -w / 2, -h / 2, w, h, 16)
    rgba(ctx, (0.04, 0.04, 0.06), 0.85 * a)
    ctx.fill_preserve()
    rgba(ctx, c, a)
    ctx.set_line_width(9)
    ctx.stroke()
    for s, dy, size, col in lines:
        text(ctx, s, 0, dy, size, col, font=CAPTION_FONT, bold=False, a=a, stroke=(0, 0, 0), stroke_w=8)
    ctx.restore()


def embers(ctx, t, n, c, speed=90, seed=0):
    for i in range(n):
        x = (rnd(i, seed + 1) * W + 30 * math.sin(t * 1.3 + i)) % W
        y = H - ((rnd(i, seed + 2) * H + t * speed * (0.6 + rnd(i, seed + 3))) % (H * 1.05))
        r = 2 + 4 * rnd(i, seed + 4)
        glow(ctx, x, y, r * 5, c, 0.25)
        circle(ctx, x, y, r, shade(c, 1.2), 0.85)


# ============================================================ scenes

class Hook:
    """Backlit silhouette at a rally podium, tricolor lasers sweeping the crowd."""
    accent = SAFFRON
    TITLE = 0.8

    def events(self, d):
        return [(0.02, "boom"), (self.TITLE, "thud")] + [(1.4 + k * 1.6, "zap") for k in range(int(d / 1.6))]

    def lasers(self, ctx, t):
        for k in range(9):
            ox, oy = ((0, 1380), (540, 1260), (1080, 1380))[k % 3]
            base = (-0.55, 0.0, 0.55)[k % 3]
            a = -math.pi / 2 + base + 0.45 * math.sin(t * 1.3 + k * 0.8)
            c = TRICOLOR[k // 3]
            ex, ey = ox + 2400 * math.cos(a), oy + 2400 * math.sin(a)
            nx, ny = -math.sin(a) * 60, math.cos(a) * 60
            ctx.move_to(ox, oy)
            ctx.line_to(ex + nx, ey + ny)
            ctx.line_to(ex - nx, ey - ny)
            ctx.close_path()
            g = cairo.LinearGradient(ox, oy, ex, ey)
            g.add_color_stop_rgba(0, *c, 0.45)
            g.add_color_stop_rgba(0.6, *c, 0.0)
            ctx.set_source(g)
            ctx.fill()
            line(ctx, [(ox, oy), (lerp(ox, ex, 0.55), lerp(oy, ey, 0.55))], c, 3, 0.7)
        # fast tricolor streaks
        for k in range(12):
            c = TRICOLOR[k % 3]
            y0 = (rnd(k, 1) * H + t * (900 + 500 * rnd(k, 2))) % (H + 400) - 200
            x0 = (rnd(k, 3) * W * 1.4 - t * 600) % (W + 400) - 200
            line(ctx, [(x0, y0), (x0 + 160, y0 - 90)], c, 4, 0.55)

    def draw(self, ctx, t, d):
        backdrop(ctx, hexc("#0B0A1F"), hexc("#020206"), self.accent, 540, 650, t, motes=30)
        self.lasers(ctx, t)
        # fast zoom into the silhouette
        z = lerp(0.55, 1.0, ease_out_back(t / 0.55, 1.2))
        hero(ctx, 540, 830, 0.95, t, d, zoom=z, pose="wave", shadow=True)
        # podium
        px, py = 540, 1235
        for side in (-1, 1):
            line(ctx, [(px + side * 40, py), (px + side * 75, py - 120)], hexc("#1A1A1A"), 8)
            circle(ctx, px + side * 75, py - 128, 14, hexc("#2A2A2A"))
        ctx.move_to(px - 210, py)
        ctx.line_to(px + 210, py)
        ctx.line_to(px + 180, py + 360)
        ctx.line_to(px - 180, py + 360)
        ctx.close_path()
        g = cairo.LinearGradient(0, py, 0, py + 360)
        g.add_color_stop_rgb(0, *hexc("#3A2614"))
        g.add_color_stop_rgb(1, *hexc("#140C06"))
        ctx.set_source(g)
        ctx.fill()
        for k, c in enumerate(TRICOLOR):
            ctx.rectangle(px - 205 + k * 136.7, py + 30, 137, 46)
            rgba(ctx, c)
            ctx.fill()
        glow(ctx, px, py + 170, 90, GOLD, 0.5)
        chakra(ctx, px, py + 170, 52, t * 0.8, GOLD)
        # cheering crowd
        for row, (yy, r, col) in enumerate(((1360, 30, "#1A1426"), (1450, 40, "#100C18"), (1560, 52, "#06040A"))):
            n = 12 - row * 3
            for k in range(n + 1):
                hx = k * W / n + (row % 2) * W / (2 * n) - W / (4 * n)
                hy = yy - 14 * abs(math.sin(t * 4 + k * 1.3 + row))
                c = hexc(col)
                if rnd(k, row + 1) > 0.55:
                    arm = (hx + 18 * math.sin(t * 5 + k), hy - 2.6 * r)
                    line(ctx, [(hx + r * 0.6, hy + r * 0.4), arm], c, r * 0.45)
                    if rnd(k + int(t * 5), row + 7) > 0.8:
                        glow(ctx, arm[0], arm[1], r * 1.4, (1, 1, 1), 0.7)
                circle(ctx, hx, hy, r, c)
                rrect(ctx, hx - r * 1.6, hy + r * 0.8, r * 3.2, r * 4, r)
                rgba(ctx, c)
                ctx.fill()
        # 2014 VS AAJ title
        u = t - self.TITLE
        if u > 0:
            pop = ease_out_back(u / 0.3)
            ctx.save()
            ctx.translate(540, 330)
            ctx.scale(pop, pop)
            ctx.rotate(-0.04)
            text(ctx, "2014", -230, 0, 120, hexc("#8A8F9C"), font=CAPTION_FONT, bold=False,
                 stroke=(0, 0, 0), stroke_w=12)
            line(ctx, [(-330, 20), (-130, -20)], hexc("#FF3B3B"), 12)
            text(ctx, "VS", 0, 0, 70, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=10)
            glow(ctx, 230, 0, 170, SAFFRON, 0.5 + 0.2 * math.sin(t * 8))
            text(ctx, "AAJ", 230, 0, 130, SAFFRON, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=12)
            ctx.restore()


def temple(ctx, cx, base, s, t):
    """Golden Nagara-style temple: pillared hall, curved shikharas, kalash and saffron flag."""
    top = base - 300 * s
    glow(ctx, cx, base - 700 * s, 620 * s, GOLD, 0.55 + 0.1 * math.sin(t * 2))
    g = cairo.LinearGradient(0, base - 820 * s, 0, base)
    g.add_color_stop_rgb(0, *hexc("#FFE9A8"))
    g.add_color_stop_rgb(0.55, *hexc("#E3A332"))
    g.add_color_stop_rgb(1, *hexc("#8A5A12"))
    edge = hexc("#6E430A")
    spires = [(cx - 370 * s, 100 * s, 170 * s), (cx + 370 * s, 100 * s, 170 * s),
              (cx - 230 * s, 170 * s, 320 * s), (cx + 230 * s, 170 * s, 320 * s), (cx, 300 * s, 540 * s)]
    for x, w, h in spires:
        ctx.move_to(x - w / 2, top)
        ctx.curve_to(x - w / 2, top - h * 0.55, x - w * 0.18, top - h * 0.95, x, top - h)
        ctx.curve_to(x + w * 0.18, top - h * 0.95, x + w / 2, top - h * 0.55, x + w / 2, top)
        ctx.close_path()
        ctx.set_source(g)
        ctx.fill_preserve()
        rgba(ctx, edge, 0.7)
        ctx.set_line_width(3)
        ctx.stroke()
        for k in range(1, 7):  # horizontal ribs
            yy = top - h * k / 7.5
            hw = w / 2 * (1 - (k / 7.5) ** 2.2)
            line(ctx, [(x - hw, yy), (x + hw, yy)], edge, 2.5, 0.45)
        _ellipse(ctx, x, top - h, w * 0.16, w * 0.05)
        ctx.set_source(g)
        ctx.fill()
        circle(ctx, x, top - h - w * 0.09, w * 0.06, GOLD)
    # saffron flag on the main spire
    fx, fy = cx, top - 540 * s - 30 * s
    line(ctx, [(fx, fy), (fx, fy - 120 * s)], edge, 4)
    ctx.move_to(fx, fy - 120 * s)
    for i in range(9):
        u = i / 8
        ctx.line_to(fx + 110 * s * u, fy - 120 * s + 30 * s * u + 8 * s * math.sin(t * 6 - u * 4) * u)
    ctx.line_to(fx, fy - 60 * s)
    ctx.close_path()
    rgba(ctx, SAFFRON)
    ctx.fill()
    # pillared hall + plinth
    ctx.rectangle(cx - 420 * s, top, 840 * s, 260 * s)
    ctx.set_source(g)
    ctx.fill()
    for k in range(15):
        x = cx - 390 * s + k * 55.7 * s
        line(ctx, [(x, top + 30 * s), (x, top + 250 * s)], edge, 6 * s, 0.6)
    ctx.rectangle(cx - 470 * s, base - 40 * s, 940 * s, 40 * s)
    rgba(ctx, hexc("#B77A1E"))
    ctx.fill()


def diya(ctx, x, y, t, k):
    ctx.move_to(x - 46, y)
    ctx.curve_to(x - 40, y + 34, x + 40, y + 34, x + 46, y)
    ctx.close_path()
    rgba(ctx, hexc("#B5541C"))
    ctx.fill()
    f = 1 + 0.15 * math.sin(t * 13 + k * 2.1)
    glow(ctx, x, y - 20, 70, hexc("#FFB347"), 0.6)
    ctx.move_to(x, y - 48 * f)
    ctx.curve_to(x + 18, y - 20, x + 12, y - 2, x, y - 2)
    ctx.curve_to(x - 12, y - 2, x - 18, y - 20, x, y - 48 * f)
    rgba(ctx, hexc("#FFD36E"))
    ctx.fill()


class Mandir:
    """Ram Mandir glowing gold behind the PM, hands folded in prayer."""
    accent = hexc("#FFB000")
    SEAL = 0.55

    def events(self, d):
        return [(0.02, "boom"), (0.3, "dingdong"), (self.SEAL, "thud"), (d * 0.55, "dingdong")]

    def draw(self, ctx, t, d):
        backdrop(ctx, hexc("#3A1606"), hexc("#0A0402"), self.accent, 540, 520, t, motes=0)
        temple(ctx, 540, 1060, 1.0, t)
        embers(ctx, t, 36, hexc("#FFB347"))
        hero(ctx, 540, 960, 0.85, t, d, pose="namaste", jacket=None, kurta=hexc("#FFF4E0"), stole=True)
        for k in range(7):
            diya(ctx, 90 + k * 150, 1505 + 10 * math.sin(t * 2 + k), t, k)
        # AYODHYA plaque + 500 SAAL seal
        u = t - self.SEAL
        if u > 0:
            pop = ease_out_back(u / 0.3)
            ctx.save()
            ctx.translate(880, 1180)
            ctx.scale(pop, pop)
            ctx.rotate(-0.15 + 0.05 * math.sin(t * 2))
            glow(ctx, 0, 0, 170, SAFFRON, 0.5)
            circle(ctx, 0, 0, 112, hexc("#2A1206"))
            ctx.arc(0, 0, 100, 0, math.tau)
            rgba(ctx, GOLD)
            ctx.set_line_width(8)
            ctx.stroke()
            text(ctx, "500", 0, -14, 92, GOLD, font=CAPTION_FONT, bold=False)
            text(ctx, "SAAL", 0, 52, 36, (1, 1, 1), font=CAPTION_FONT, bold=False)
            ctx.restore()
            ctx.save()
            ctx.translate(200, 1180)
            ctx.scale(pop, pop)
            ctx.rotate(0.06)
            rrect(ctx, -150, -44, 300, 88, 18)
            rgba(ctx, hexc("#2A1206"), 0.9)
            ctx.fill_preserve()
            rgba(ctx, GOLD)
            ctx.set_line_width(5)
            ctx.stroke()
            text(ctx, "AYODHYA", 0, 0, 56, GOLD, font=CAPTION_FONT, bold=False)
            ctx.restore()


def mountains(ctx, t):
    for layer, (base, amp, col, n) in enumerate(((1060, 470, "#2A3B4C", 6), (1230, 300, "#141E28", 8))):
        drift = 18 * math.sin(t * 0.3) * (layer + 1)
        step = (W + 300) / n
        pts = []
        for k in range(n + 1):
            x = -150 + k * step + drift
            pts.append((x, base - amp * (0.5 + 0.5 * rnd(k, layer + 3))))
            pts.append((x + step / 2, base - amp * 0.18 * rnd(k, layer + 5)))
        ctx.move_to(-200, H)
        for p in pts:
            ctx.line_to(*p)
        ctx.line_to(W + 200, H)
        ctx.close_path()
        rgba(ctx, hexc(col))
        ctx.fill()
        if layer == 0:  # snow caps
            for i in range(0, len(pts) - 1, 2):
                (px, py), (qx, qy) = pts[i], pts[i + 1]
                lx, ly = pts[i - 1] if i else (px - step / 2, qy)
                ctx.move_to(px, py)
                ctx.line_to(lerp(px, qx, 0.25), lerp(py, qy, 0.25))
                ctx.line_to(px, py + (qy - py) * 0.15)
                ctx.line_to(lerp(px, lx, 0.25), lerp(py, ly, 0.25))
                ctx.close_path()
                rgba(ctx, hexc("#DCE6F0"), 0.85)
                ctx.fill()


def shield(ctx, x, y, w, h, t):
    def path():
        ctx.move_to(x - w / 2, y - h / 2 + 30)
        ctx.curve_to(x - w / 4, y - h / 2 - 10, x + w / 4, y - h / 2 - 10, x + w / 2, y - h / 2 + 30)
        ctx.line_to(x + w / 2, y)
        ctx.curve_to(x + w / 2, y + h * 0.3, x + w * 0.2, y + h * 0.42, x, y + h / 2)
        ctx.curve_to(x - w * 0.2, y + h * 0.42, x - w / 2, y + h * 0.3, x - w / 2, y)
        ctx.close_path()

    glow(ctx, x, y, w * 1.1, SAFFRON, 0.35)
    ctx.save()
    path()
    ctx.clip()
    for k, c in enumerate(TRICOLOR):
        ctx.rectangle(x - w / 2, y - h / 2 - 20 + k * (h + 20) / 3, w, (h + 20) / 3 + 1)
        rgba(ctx, c)
        ctx.fill()
    chakra(ctx, x, y - h * 0.06, h * 0.13, t * 0.6)
    ctx.restore()
    path()
    rgba(ctx, GOLD)
    ctx.set_line_width(16)
    ctx.stroke()


class Iron:
    """Camouflage jacket, commanding stance, mountains and a tricolor shield."""
    accent = hexc("#22C55E")

    def stamps(self, d):
        return d * 0.22, d * 0.66

    def events(self, d):
        s1, s2 = self.stamps(d)
        return [(0.02, "boom"), (s1 + 0.15, "thud"), (s2 + 0.15, "boom"), (s2 + 0.4, "zap")]

    def draw(self, ctx, t, d):
        backdrop(ctx, hexc("#0E1A24"), hexc("#03060A"), self.accent, 540, 600, t, motes=50)
        mountains(ctx, t)
        sh = ease_out_back((t - 0.15) / 0.5)
        if sh > 0:
            ctx.save()
            ctx.translate(540, 560)
            ctx.scale(sh, sh)
            ctx.translate(-540, -560)
            shield(ctx, 540, 560, 520, 580, t)
            ctx.restore()
        hero(ctx, 540, 900, 0.9, t, d, pose="command", jacket=hexc("#4B5320"), camo=True)
        s1, s2 = self.stamps(d)
        if t < s2:
            u = t - s1
            stamp(ctx, 540, 1320, u, -0.06, 620, 170, hexc("#FF3B3B"),
                  [("ARTICLE 370", -18, 90, (1, 1, 1)), ("KHATAM", 52, 40, hexc("#FF3B3B"))])
            if u > 0.25:  # red slash across it
                k = ease_out_cubic((u - 0.25) / 0.15)
                line(ctx, [(270, 1390), (lerp(270, 810, k), lerp(1390, 1250, k))], hexc("#FF3B3B"), 16)
        else:
            u = t - s2
            stamp(ctx, 540, 1320, u, 0.05, 700, 170, GOLD,
                  [("SURGICAL STRIKE", 0, 92, GOLD)])
            ctx.save()  # target reticle
            ctx.translate(880, 1180)
            ctx.rotate(t * 2)
            r = lerp(200, 70, ease_out_cubic(u / 0.4))
            ctx.arc(0, 0, r, 0, math.tau)
            rgba(ctx, hexc("#FF3B3B"), 0.9)
            ctx.set_line_width(6)
            ctx.stroke()
            for k in range(4):
                a = k * math.pi / 2
                line(ctx, [(r * 0.6 * math.cos(a), r * 0.6 * math.sin(a)),
                           (r * 1.3 * math.cos(a), r * 1.3 * math.sin(a))], hexc("#FF3B3B"), 6)
            ctx.restore()


def globe(ctx, x, y, r, t):
    g = cairo.RadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r)
    g.add_color_stop_rgba(0, 0.25, 0.6, 1.0, 0.35)
    g.add_color_stop_rgba(1, 0.05, 0.15, 0.45, 0.25)
    ctx.arc(x, y, r, 0, math.tau)
    ctx.set_source(g)
    ctx.fill()
    blue = hexc("#5AB4FF")
    for k in range(1, 6):  # latitudes
        ly = y + r * (k / 3 - 1)
        hw = math.sqrt(max(0.0, r * r - (ly - y) ** 2))
        _ellipse(ctx, x, ly, hw + 0.01, hw * 0.12 + 0.01)
        rgba(ctx, blue, 0.3)
        ctx.set_line_width(2)
        ctx.stroke()
    for k in range(10):  # rotating longitudes
        lon = k / 10 * math.pi + t * 0.4
        _ellipse(ctx, x, y, abs(r * math.cos(lon)) + 0.01, r)
        rgba(ctx, blue, 0.35)
        ctx.set_line_width(2)
        ctx.stroke()
    for i in range(60):  # landmass dots on the visible hemisphere
        lon = rnd(i, 1) * math.tau + t * 0.4
        lat = (rnd(i, 2) - 0.5) * 2.4
        if math.cos(lon) > 0:
            circle(ctx, x + r * math.sin(lon) * math.cos(lat), y + r * math.sin(lat) * 0.95, 4, blue,
                   0.4 + 0.5 * math.cos(lon))
    # India beacon
    p = 1 + 0.3 * math.sin(t * 5)
    glow(ctx, x + r * 0.35, y - r * 0.12, 60 * p, SAFFRON, 0.9)
    circle(ctx, x + r * 0.35, y - r * 0.12, 10, (1, 1, 1))
    ctx.arc(x, y, r, 0, math.tau)
    rgba(ctx, blue, 0.7)
    ctx.set_line_width(4)
    ctx.stroke()


class World:
    """World stage: globe hologram, international flags and Chandrayaan landing on the Moon."""
    accent = hexc("#3AA0FF")
    MOON = (900, 420, 95)

    def landing(self, d):
        return d * 0.6

    def events(self, d):
        return [(0.02, "boom"), (self.landing(d), "beep"), (d * 0.8, "boom")]

    def draw(self, ctx, t, d):
        backdrop(ctx, hexc("#050B24"), hexc("#01020A"), self.accent, 540, 700, t, motes=0)
        for i in range(90):  # stars
            circle(ctx, rnd(i, 1) * W, rnd(i, 2) * 1300, 1 + 2 * rnd(i, 3), (1, 1, 1),
                   0.3 + 0.5 * abs(math.sin(t * (1 + 2 * rnd(i, 4)) + i)))
        globe(ctx, 540, 700, 360, t)
        # spotlights
        for sx in (120, 960):
            ctx.move_to(sx - 20, 0)
            ctx.line_to(sx + 20, 0)
            ctx.line_to(540 + 260, 1500)
            ctx.line_to(540 - 260, 1500)
            ctx.close_path()
            g = cairo.LinearGradient(sx, 0, 540, 1500)
            g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.22)
            g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0.0)
            ctx.set_source(g)
            ctx.fill()
        # stage floor + flags
        _ellipse(ctx, 540, 1520, 720, 140)
        g = cairo.LinearGradient(0, 1380, 0, 1660)
        g.add_color_stop_rgb(0, *hexc("#1B2B55"))
        g.add_color_stop_rgb(1, *hexc("#050A18"))
        ctx.set_source(g)
        ctx.fill()
        for k, (x, kind) in enumerate(((40, "in"), (160, "us"), (280, "ru"), (680, "fr"), (800, "jp"), (920, "in"))):
            flag(ctx, x, 1090 + 15 * (k % 2), 110, 72, kind, t, pole=330, phase=k)
        hero(ctx, 540, 900, 0.88, t, d, pose="address", jacket=hexc("#1F2A55"))
        # Moon + Chandrayaan-3 lander
        mx, my, mr = self.MOON
        glow(ctx, mx, my, mr * 2, (0.9, 0.9, 1.0), 0.3)
        circle(ctx, mx, my, mr, hexc("#C9CCD6"))
        for i in range(7):
            circle(ctx, mx + (rnd(i, 1) - 0.5) * mr * 1.3, my + (rnd(i, 2) - 0.5) * mr * 1.3,
                   6 + 12 * rnd(i, 3), hexc("#9EA3B0"))
        land = self.landing(d)
        v = ease_out_cubic(t / land)
        lx, ly = mx, lerp(120, my - mr - 26, v)
        if t < land:
            ctx.move_to(lx - 14, ly + 26)
            ctx.line_to(lx + 14, ly + 26)
            ctx.line_to(lx, ly + 70 + 15 * math.sin(t * 40))
            ctx.close_path()
            rgba(ctx, hexc("#FFB347"), 0.9)
            ctx.fill()
        for side in (-1, 1):
            line(ctx, [(lx + side * 18, ly + 10), (lx + side * 34, ly + 30)], hexc("#B8BCC8"), 4)
        rrect(ctx, lx - 24, ly - 20, 48, 36, 6)
        rgba(ctx, hexc("#E8B64A"))
        ctx.fill()
        ctx.rectangle(lx - 52, ly - 14, 24, 16)
        ctx.rectangle(lx + 28, ly - 14, 24, 16)
        rgba(ctx, hexc("#2B4C9B"))
        ctx.fill()
        if t >= land:
            u = t - land
            flag(ctx, lx + 40, ly - 50, 46, 30, "in", t, pole=60)
            text(ctx, "CHANDRAYAAN-3", mx, my + mr + 45, 38, GOLD, font=CAPTION_FONT, bold=False,
                 a=min(1, u / 0.2), stroke=(0, 0, 0), stroke_w=6)
        # SUPER POWER headline
        u = t - d * 0.8
        if u > 0:
            pop = ease_out_back(u / 0.3) * (1 + 0.05 * math.sin(t * 9))
            ctx.save()
            ctx.translate(380, 300)
            ctx.scale(pop, pop)
            ctx.rotate(-0.05)
            glow(ctx, 0, 0, 300, SAFFRON, 0.5)
            text(ctx, "SUPER POWER", 0, 0, 104, GOLD, font=CAPTION_FONT, bold=False,
                 stroke=(0, 0, 0), stroke_w=12)
            ctx.restore()


def subscribe_badge(ctx, x, y, t, clicked):
    w, h = 780, 140
    rrect(ctx, x - w / 2, y - h / 2, w, h, 70)
    rgba(ctx, (0, 0, 0), 0.78)
    ctx.fill_preserve()
    rgba(ctx, GOLD)
    ctx.set_line_width(4)
    ctx.stroke()
    ax = x - w / 2 + 72
    g = cairo.RadialGradient(ax - 15, y - 15, 5, ax, y, 52)
    g.add_color_stop_rgb(0, *hexc("#FFC266"))
    g.add_color_stop_rgb(1, *hexc("#D9640A"))
    ctx.arc(ax, y, 52, 0, math.tau)
    ctx.set_source(g)
    ctx.fill()
    text(ctx, "RS", ax, y, 44, (1, 1, 1), font=CAPTION_FONT, bold=False)
    text(ctx, "REALITY SHIFT", x - w / 2 + 145, y, 52, (1, 1, 1), font=CAPTION_FONT, bold=False, anchor="l")
    bx = x + w / 2 - 150
    p = 1 + (0.06 * math.sin(t * 8) if not clicked else 0)
    ctx.save()
    ctx.translate(bx, y)
    ctx.scale(p, p)
    rrect(ctx, -125, -44, 250, 88, 44)
    rgba(ctx, hexc("#5A5A5A") if clicked else hexc("#FF0000"))
    ctx.fill()
    text(ctx, "SUBSCRIBED" if clicked else "SUBSCRIBE", 0, 0, 36, (1, 1, 1))
    ctx.restore()
    return bx, y


class Outro:
    """Smiling, waving portrait, pulsing JAI HIND call-out and the Reality Shift subscribe badge."""
    accent = SAFFRON

    def click(self, d):
        return d * 0.82

    def events(self, d):
        return [(0.02, "boom"), (self.click(d), "pick"), (self.click(d) + 0.05, "pop")]

    def draw(self, ctx, t, d):
        backdrop(ctx, hexc("#2A1204"), hexc("#070301"), self.accent, 540, 760, t, motes=20)
        ctx.save()  # tricolor sunburst
        ctx.translate(540, 700)
        ctx.rotate(t * 0.2)
        for k in range(24):
            a = k / 24 * math.tau
            ctx.move_to(0, 0)
            ctx.arc(0, 0, 1500, a, a + math.tau / 48)
            ctx.close_path()
            rgba(ctx, TRICOLOR[k % 3], 0.07)
            ctx.fill()
        ctx.restore()
        hero(ctx, 540, 840, 0.9, t, d, pose="wave", smile=True)
        for i in range(40):  # tricolor confetti
            fy = (rnd(i, 1) * H + t * (220 + 160 * rnd(i, 2))) % H
            fx = rnd(i, 3) * W + 40 * math.sin(t * 2 + i)
            ctx.save()
            ctx.translate(fx, fy)
            ctx.rotate(t * (2 + 3 * rnd(i, 4)) + i)
            ctx.rectangle(-9, -5, 18, 10)
            rgba(ctx, TRICOLOR[i % 3], 0.9)
            ctx.fill()
            ctx.restore()
        # COMMENT 'JAI HIND' + waving tiranga
        pop = ease_out_back(t / 0.35) * (1 + 0.06 * math.sin(t * 8))
        ctx.save()
        ctx.translate(540, 310)
        ctx.scale(pop, pop)
        ctx.rotate(-0.03)
        glow(ctx, 0, 0, 380, SAFFRON, 0.35)
        text(ctx, "COMMENT", -80, -62, 72, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=10)
        text(ctx, "'JAI HIND'", -80, 40, 116, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=14)
        flag(ctx, 220, -40, 150, 100, "in", t, pole=150)
        ctx.restore()
        # subscribe badge + cursor click
        clicked = t >= self.click(d)
        bx, by = subscribe_badge(ctx, 540, 1440, t, clicked)
        cu = clamp((t - (self.click(d) - 0.8)) / 0.7)
        if cu > 0 and t < self.click(d) + 0.9:
            cx, cy = lerp(1040, bx + 20, ease_in_out(cu)), lerp(1620, by + 20, ease_in_out(cu))
            sc = 0.85 if abs(t - self.click(d)) < 0.12 else 1.0
            ctx.save()
            ctx.translate(cx, cy)
            ctx.scale(sc, sc)
            ctx.move_to(0, 0)
            for px, py in ((0, 62), (16, 48), (28, 74), (40, 68), (28, 43), (48, 42)):
                ctx.line_to(px, py)
            ctx.close_path()
            rgba(ctx, (1, 1, 1))
            ctx.fill_preserve()
            rgba(ctx, (0, 0, 0))
            ctx.set_line_width(3)
            ctx.stroke()
            ctx.restore()


SCENE_CLASSES = {"hook": Hook, "mandir": Mandir, "iron": Iron, "world": World, "outro": Outro}
