"""Divya Rahasya faith long (16:9, ~4.5 min): Rickshaw Wale Ka Bharosa. Kalpanik prerak katha.

A poor rickshaw puller (Shambhu) and his daughter Gudiya who wants to become a doctor. Relatives laugh, the first
attempt fails, Shambhu breaks down before Hanuman ji; that rainy midnight an old baba rides to the temple, says
"Bajrangi tere saath hai", ties a red thread on his wrist and vanishes. One more year of work, her name tops the
list - and the same red thread is on Hanuman ji's murti while Shambhu's wrist is empty. Hanuman ji smiles.

Divya Rahasya rules: only subtitles on screen (CHROME False), Roman captions, Hanuman ji present in every scene
(rickshaw picture, home altar, Chalisa, temple, golden form), character scale ~0.56-0.62 (feet y 960).

    python make_long.py rickshaw_bharosa --preview | (render)
"""

import math

import cairo

import core.devta as dv
from core.devta import ell, hand, ink, limb, smooth, eye, group, place
from core.engine import circle, clamp, ease_in_out, ease_out_back, ease_out_cubic, glow, hexc, lerp, line, rgba, \
    rnd, rrect, text
from core.longform import H, W
from kathas import panchmukhi as pm
from kathas.daadi_morpankh import boy, papa

TITLE = "Rickshaw Wale Ka Bharosa"
CHROME = False
MUSIC_STYLE = "divine"
MUSIC_BPM = 78
MUSIC_SEED = 2411
MUSIC_LO, MUSIC_HI = 0.07, 0.15
KIKI_TEMPO = 1.0

GROUND = 960
GOLD, GOLD_HI = dv.GOLD, dv.GOLD_HI
GOLDEN = hexc("#FFD27A")
SAFF = hexc("#FF8C1A")
SINDOOR = hexc("#E8501E")
RED_T = hexc("#E0182A")
WHITE = (1, 1, 1)

HOT = {"HANUMAN": SAFF, "BAJRANGBALI": SAFF, "BAJRANGI": SAFF, "BAJRANG": SAFF, "JAI": SAFF, "GUDIYA": GOLD_HI,
       "SHAMBHU": GOLD_HI, "DOCTOR": hexc("#9BE07A"), "SAPNA": GOLD_HI, "LAAL": RED_T, "DHAAGA": RED_T,
       "BAABA": GOLD_HI, "BABA": GOLD_HI, "GADA": SAFF, "MANDIR": SAFF, "MOORTI": SAFF, "RIKSHA": GOLD_HI,
       "HAZAAR": hexc("#FF6A5A"), "HANSE": hexc("#FF6A5A"), "BAARISH": hexc("#9AD8FF"), "SUNEHRI": GOLD_HI,
       "MEHNAT": GOLD_HI, "SAATH": GOLD_HI, "MADAD": GOLD_HI, "LADENGE": GOLD_HI, "UPAR": hexc("#9BE07A")}

SKIN_S = hexc("#9A6440")
SKIN_G = hexc("#B97E54")
SKIN_B = hexc("#B5794E")


# ============================================================ small helpers

def sky(ctx, stops):
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in stops:
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.rectangle(-200, -200, W + 400, H + 400)
    ctx.fill()


def petals(ctx, T, n=46, seed=0, a=1.0):
    for i in range(n):
        x = (rnd(i, seed + 1) * W + 40 * math.sin(T * 1.2 + i)) % W
        y = ((rnd(i, seed + 2) * H) + T * (120 + 70 * rnd(i, seed + 3))) % (H + 60) - 30
        ell(ctx, x, y, 12, 7, T * 2 + i)
        rgba(ctx, hexc("#F59E0B") if i % 3 else hexc("#D7263D"), 0.9 * a)
        ctx.fill()


def rain(ctx, T, a=1.0):
    for i in range(160):
        x = (rnd(i, 1) * (W + 300) - T * 120) % (W + 300) - 150
        y = (rnd(i, 2) * H + T * 1500) % H
        line(ctx, [(x, y), (x - 12, y + 50)], hexc("#B8C8E8"), 3, 0.4 * a)


def sparkles(ctx, x, y, T, r=200, n=18, a=1.0):
    for i in range(n):
        ang = rnd(i, 7) * math.tau + T * 0.6
        rr = r * (0.3 + 0.7 * rnd(i, 8))
        tw = 0.5 + 0.5 * math.sin(T * 6 + i)
        circle(ctx, x + rr * math.cos(ang), y + rr * math.sin(ang), 3 + 4 * tw, GOLD_HI, 0.8 * a * tw)


def red_thread(ctx, x, y, s=1.0, glow_a=0.6):
    if glow_a > 0:
        glow(ctx, x, y, 60 * s, RED_T, glow_a)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ell(ctx, 0, 0, 26, 9)
    rgba(ctx, RED_T)
    ctx.set_line_width(6)
    ctx.stroke()
    line(ctx, [(20, 4), (34, 22)], RED_T, 4)
    line(ctx, [(16, 6), (24, 26)], RED_T, 4)
    ctx.restore()


# ============================================================ characters

def _face(ctx, t, skin, mood, look, seed):
    for side in (-1, 1):
        if mood in ("cry", "sleep"):
            ctx.arc(side * 32, -700, 16, 0.15 * math.pi, 0.85 * math.pi)
            rgba(ctx, hexc("#2A1A10"))
            ctx.set_line_width(6)
            ctx.stroke()
        elif mood == "smile":
            ctx.arc(side * 32, -696, 16, 1.1 * math.pi, 1.9 * math.pi)
            rgba(ctx, hexc("#2A1A10"))
            ctx.set_line_width(6)
            ctx.stroke()
        else:
            eye(ctx, side * 32, -704, 18 if mood != "shock" else 21, 21 if mood != "shock" else 25, t, look=look,
                seed=seed, iris=hexc("#2A1A10"), skin=skin, lid=0.15)
    if mood == "cry":
        for side in (-1, 1):
            fu = (t * 0.8 + (0.4 if side > 0 else 0)) % 1
            circle(ctx, side * 38, -684 + 70 * fu, 7, hexc("#9AD8FF"), 0.9 * (1 - fu))
    if mood == "shock":
        ell(ctx, 0, -626, 14, 18)
        ink(ctx, hexc("#5A1A10"), 3)
    elif mood in ("smile", "joy"):
        ctx.arc(0, -640, 26, 0.15 * math.pi, 0.85 * math.pi)
        rgba(ctx, hexc("#6A2A1A"))
        ctx.set_line_width(6)
        ctx.stroke()
    elif mood in ("sad", "cry", "tired"):
        ctx.arc(0, -610, 22, 1.2 * math.pi, 1.8 * math.pi)
        rgba(ctx, hexc("#6A2A1A"))
        ctx.set_line_width(5)
        ctx.stroke()
    else:
        line(ctx, [(-16, -630), (16, -630)], hexc("#6A2A1A"), 5)


SHAMBHU_ARMS = {
    "stand": ((-150, -420, -146, -330), (150, -420, 146, -330)),
    "talk": ((-150, -420, -146, -330), (190, -450, 240, -530)),
    "namaste": ((-120, -430, -14, -500), (120, -430, 14, -500)),
    "cry": ((-150, -500, -34, -690), (150, -500, 34, -690)),
    "hug": ((-170, -470, 40, -470), (170, -480, 250, -470)),
    "show": ((-150, -420, -146, -330), (190, -560, 190, -700)),
    "count": ((-120, -430, -40, -420), (120, -430, 40, -420)),
    "pat": ((-150, -420, -140, -330), (200, -560, 300, -600)),
    "ride": ((-90, -440, 150, -470), (160, -440, 210, -470)),
    "run": ((-170, -440, -120, -360), (170, -460, 210, -540)),
    "wipe": ((-150, -420, -146, -330), (160, -600, 60, -760)),
    "sit": ((-150, -420, -120, -330), (150, -420, 130, -330)),
    "bow": ((-120, -430, -14, -500), (120, -430, 14, -500)),
    "kneel": ((-120, -430, -14, -500), (120, -430, 14, -500)),
    "kneelcry": ((-150, -500, -34, -690), (150, -500, 34, -690)),
}


def shambhu(ctx, x, y, s, t, pose="stand", mood="neutral", look=(0.0, 0.0), flip=False, a=1.0, thread=0.0, wet=0.0):
    """Rickshaw-puller father: lean, cream vest, checked red gamchha, rolled dhoti, grey-black hair, moustache.
    thread > 0 draws the red thread on his right wrist."""
    def draw():
        place(ctx, x, y, s, t, flip)
        sitting = pose in ("sit", "pat", "ride")
        kneel = pose in ("kneel", "kneelcry")
        if kneel:                                                     # kneeling, shins folded under
            ctx.translate(0, 250)
            for side in (-1, 1):
                limb(ctx, [(side * 50, -330), (side * 70, -250), (side * 60 - 90, -240)], hexc("#E8E0CC"), 56)
        elif sitting:
            ctx.translate(0, 150)
            for side in (-1, 1):
                limb(ctx, [(side * 44, -330), (side * 44 + 150, -320)], hexc("#E8E0CC"), 56)
                limb(ctx, [(side * 44 + 150, -320), (side * 44 + 160, -170)], SKIN_S, 34)
                ell(ctx, side * 44 + 176, -160, 40, 15)
                ink(ctx, hexc("#3A2A1E"))
        else:
            run = 26 * math.sin(t * 12) if pose == "run" else 0
            for side in (-1, 1):
                limb(ctx, [(side * 46, -330), (side * 50 + run * side, -200)], hexc("#E8E0CC"), 58)
                limb(ctx, [(side * 50 + run * side, -200), (side * 50 + run * side * 1.4, -40)], SKIN_S, 32)
                ell(ctx, side * 56 + run * side * 1.4, -16, 44, 16)
                ink(ctx, hexc("#3A2A1E"))
        smooth(ctx, [(-120, -360), (120, -360), (130, -220), (-130, -220)], k=0.1)     # dhoti waist
        ink(ctx, hexc("#E8E0CC"))
        smooth(ctx, [(-124, -545), (124, -545), (130, -340), (-130, -340)], k=0.1)      # vest
        ink(ctx, hexc("#EDE6D4") if wet < 0.5 else hexc("#C8D0D8"))
        smooth(ctx, [(-110, -560), (-40, -560), (60, -380), (10, -360), (-120, -470)], k=0.1)  # gamchha
        ink(ctx, hexc("#C8282A"), 3)
        for k in range(3):
            line(ctx, [(-90 + 30 * k, -540), (-10 + 30 * k, -400)], hexc("#F4E8D0"), 3, 0.6)
        (le, re) = SHAMBHU_ARMS.get(pose, SHAMBHU_ARMS["stand"])
        for sh, (ex, ey, hx, hy) in (((-122, -528), le), ((122, -528), re)):
            limb(ctx, [sh, (ex, ey), (hx, hy)], SKIN_S, 38)
            if pose not in ("namaste", "bow", "kneel"):
                hand(ctx, hx, hy, SKIN_S, 22)
        if pose in ("namaste", "bow", "kneel"):
            smooth(ctx, [(0, -540), (18, -505), (16, -462), (0, -446), (-16, -462), (-18, -505)])
            ink(ctx, SKIN_S)
        if pose == "count":
            for k in range(3):
                rrect(ctx, -60 + 6 * k, -440 - 8 * k, 120, 50, 4)
                ink(ctx, hexc("#B8D8A8"), 2)
        if thread > 0:
            hx, hy = re[2], re[3]
            red_thread(ctx, hx - 6, hy + 26 if pose not in ("show",) else hy + 30, 0.9, 0.5 * thread)
        rrect(ctx, -26, -610, 52, 60, 14)
        ink(ctx, SKIN_S)
        ell(ctx, 0, -700, 88, 100)
        ink(ctx, SKIN_S)
        ell(ctx, 0, -778, 84, 38)                                     # hair
        ink(ctx, hexc("#2A2622"), 2)
        for side in (-1, 1):
            ell(ctx, side * 82, -738, 14, 28)
            ink(ctx, hexc("#6A6460"), 2)
            ell(ctx, side * 90, -690, 14, 22)
            ink(ctx, SKIN_S, 2)
        _face(ctx, t, SKIN_S, mood, look, 31)
        smooth(ctx, [(-50, -660), (0, -672), (50, -660), (40, -642), (0, -652), (-40, -642)])     # moustache
        ink(ctx, hexc("#2A2622"), 2)
        if pose == "wipe" or wet > 0:
            for k in range(3):
                fu = (t * 1.1 + k / 3) % 1
                circle(ctx, -60 + 50 * k, -760 + 50 * fu, 6, hexc("#BFE4FF"), 0.8 * (1 - fu))
        ctx.restore()
    group(ctx, a, draw)


GUDIYA_ARMS = {
    "stand": ((-130, -420, -126, -330), (130, -420, 126, -330)),
    "talk": ((-130, -420, -126, -330), (170, -450, 220, -540)),
    "namaste": ((-110, -430, -14, -500), (110, -430, 14, -500)),
    "joy": ((-190, -620, -200, -760), (190, -620, 200, -760)),
    "cry": ((-130, -500, -32, -690), (130, -500, 32, -690)),
    "phone": ((-130, -420, -36, -480), (130, -420, 36, -490)),
    "study": ((-120, -420, -60, -400), (120, -420, 60, -400)),
    "write": ((-120, -420, -60, -400), (130, -420, lambda t: 90 + 20 * math.sin(t * 9), -390)),
    "press": ((-110, -420, 60, -300), (120, -420, 150, -300)),
    "hug": ((-160, -470, 40, -470), (160, -480, 240, -470)),
    "carry": ((-110, -420, 60, -440), (140, -430, 170, -450)),
    "teach": ((-130, -420, -126, -330), (180, -560, 240, -660)),
}


def gudiya(ctx, x, y, s, t, pose="stand", mood="neutral", look=(0.0, 0.0), flip=False, a=1.0, seated=False,
           coat=False, shake=0.0):
    """Daughter (~17): plum kurta, mustard dupatta, white salwar, two braids, small bindi. coat=True = doctor's
    white coat with a stethoscope (the dream)."""
    def draw():
        place(ctx, x + shake * 4 * math.sin(t * 40), y, s, t, flip)
        if seated:
            ctx.translate(0, 190)
            ell(ctx, 0, -300, 170, 60)                                 # cross-legged lap
            ink(ctx, hexc("#F0ECE4") if not coat else hexc("#F8F8F8"))
        else:
            for side in (-1, 1):
                limb(ctx, [(side * 42, -320), (side * 46, -40)], hexc("#F0ECE4"), 50)
                ell(ctx, side * 52, -16, 40, 15)
                ink(ctx, hexc("#C8322A"))
        body = hexc("#F8F8F8") if coat else hexc("#8A2A5A")
        smooth(ctx, [(-112, -545), (112, -545), (140, -260), (-140, -260)], k=0.12)     # kurta / coat
        ink(ctx, body)
        if coat:
            line(ctx, [(0, -545), (0, -270)], hexc("#C8C8C8"), 4)
            smooth(ctx, [(-60, -540), (-80, -440), (-30, -380), (30, -380), (80, -440), (60, -540)], k=0.2,
                   closed=False)
            rgba(ctx, hexc("#2A2A2A"))
            ctx.set_line_width(6)
            ctx.stroke()
            circle(ctx, 30, -380, 12, hexc("#8A8A8A"))
        else:
            smooth(ctx, [(-112, -545), (-30, -545), (120, -300), (70, -280), (-120, -450)], k=0.1)   # dupatta
            ink(ctx, hexc("#E8B020"), 3)
        le, re = GUDIYA_ARMS.get(pose, GUDIYA_ARMS["stand"])
        for sh, (ex, ey, hx, hy) in (((-110, -525), le), ((110, -525), re)):
            hx = hx(t) if callable(hx) else hx
            sleeve = body
            limb(ctx, [sh, (ex, ey), (hx, hy)], SKIN_G, 34)
            limb(ctx, [sh, (lerp(sh[0], ex, 0.6), lerp(sh[1], ey, 0.6))], sleeve, 44)
            if pose != "namaste":
                hand(ctx, hx, hy, SKIN_G, 20)
        if pose == "namaste":
            smooth(ctx, [(0, -540), (16, -505), (14, -462), (0, -448), (-14, -462), (-16, -505)])
            ink(ctx, SKIN_G)
        if pose in ("study", "write"):
            smooth(ctx, [(-90, -430), (0, -415), (90, -430), (90, -370), (0, -355), (-90, -370)], k=0.05)  # open book
            ink(ctx, hexc("#F8F4E8"), 3)
            line(ctx, [(0, -415), (0, -355)], hexc("#B8A888"), 3)
            rrect(ctx, 30, -412, 40, 50, 4)                             # the little Chalisa booklet
            ink(ctx, SAFF, 2)
        if pose == "phone":
            rrect(ctx, -30, -540, 60, 100, 8)
            ink(ctx, hexc("#1A1A2A"), 3)
        if pose == "carry":
            for k in range(4):
                rrect(ctx, 30 + 4 * k, -500 - 22 * k, 160, 20, 4)
                ink(ctx, hexc(("#B8321E", "#2E6A8A", "#3A8A4A", "#C88A2A")[k]), 3)
        for side in (-1, 1):                                            # braids behind the shoulders
            limb(ctx, [(side * 70, -700), (side * 96, -600), (side * 92, -470)], hexc("#1A120E"), 26)
            circle(ctx, side * 92, -462, 12, hexc("#C8282A"))
        rrect(ctx, -24, -610, 48, 60, 14)
        ink(ctx, SKIN_G)
        ell(ctx, 0, -700, 84, 96)
        ink(ctx, SKIN_G)
        smooth(ctx, [(-88, -700), (-80, -780), (0, -812), (80, -780), (88, -700), (60, -760), (0, -770),
                     (-60, -760)], k=0.12)                              # hair, centre parting
        ink(ctx, hexc("#1A120E"), 2)
        _face(ctx, t, SKIN_G, "smile" if mood == "joy" else mood, look, 41)
        circle(ctx, 0, -748, 6, hexc("#C8102A"))                        # bindi
        ctx.restore()
    group(ctx, a, draw)


def baba(ctx, x, y, s, t, pose="stand", mood="smile", flip=False, a=1.0, divine=0.0, seated=False):
    """Old baba (Hanuman ji in disguise): white pagdi, long white beard, sindoor tilak, maroon blanket over a white
    kurta, wooden lathi with a round knob. pose: stand | walk | hail (hand raised) | talk | bless | tie."""
    def draw():
        if divine > 0:
            glow(ctx, x, y - 480 * s, 360 * s, GOLDEN, 0.45 * divine)
        place(ctx, x, y, s, t, flip)
        if seated:
            ctx.translate(0, 150)
            for side in (-1, 1):
                limb(ctx, [(side * 44, -330), (side * 44 + 140, -320), (side * 44 + 150, -170)], hexc("#EDEAE4"), 50)
        else:
            sw = 10 * math.sin(t * 6) if pose == "walk" else 0
            for side in (-1, 1):
                limb(ctx, [(side * 44, -330), (side * 46 + sw * side, -40)], hexc("#EDEAE4"), 52)
                ell(ctx, side * 50 + sw * side, -16, 42, 15)
                ink(ctx, hexc("#5A3A1E"))
        smooth(ctx, [(-118, -545), (118, -545), (136, -280), (-136, -280)], k=0.12)
        ink(ctx, hexc("#F2EEE6"))
        smooth(ctx, [(-140, -570), (140, -570), (160, -380), (100, -330), (-100, -330), (-160, -380)], k=0.15)
        ink(ctx, hexc("#6A1E24"))                                       # maroon blanket shawl
        if pose in ("stand", "walk") and not seated:                    # lathi with a round knob (a gada hint)
            limb(ctx, [(-180, -30), (-184, -700)], hexc("#7A4A22"), 16)
            circle(ctx, -184, -712, 26, hexc("#8A5A2A"))
        arms = {"hail": ((-170, -440, -176, -700), (150, -420, 140, -330)),
                "talk": ((-160, -420, -150, -330), (170, -460, 220, -520)),
                "bless": ((-160, -420, -150, -330), (190, -560, 190, -690)),
                "tie": ((-120, -430, 80, -440), (130, -430, 190, -450))}
        le, re = arms.get(pose, ((-176, -440, -180, -400), (150, -420, 140, -330)))
        for sh, (ex, ey, hx, hy) in (((-130, -540), le), ((130, -540), re)):
            limb(ctx, [sh, (ex, ey), (hx, hy)], hexc("#6A1E24"), 46)
            if pose == "bless" and hx == 190:
                dv.palm(ctx, hx, hy, SKIN_B, ang=0.0, s=1.0)
            else:
                hand(ctx, hx, hy, SKIN_B, 21)
        rrect(ctx, -26, -610, 52, 60, 14)
        ink(ctx, SKIN_B)
        ell(ctx, 0, -700, 86, 98)
        ink(ctx, SKIN_B)
        smooth(ctx, [(-92, -740), (-80, -810), (0, -840), (80, -810), (92, -740), (0, -760)], k=0.15)   # pagdi
        ink(ctx, hexc("#F4F0E6"), 3)
        for k in range(3):
            line(ctx, [(-80, -760 - 22 * k), (80, -770 - 22 * k)], hexc("#D8D2C4"), 3, 0.7)
        for side in (-1, 1):
            if mood == "smile":
                ctx.arc(side * 32, -700, 15, 1.1 * math.pi, 1.9 * math.pi)
                rgba(ctx, hexc("#2A1A10"))
                ctx.set_line_width(6)
                ctx.stroke()
            else:
                eye(ctx, side * 32, -704, 16, 19, t, seed=51, iris=hexc("#2A1A10"), skin=SKIN_B, lid=0.35)
            line(ctx, [(side * 14, -730), (side * 50, -736)], hexc("#EDEAE4"), 6)
        smooth(ctx, [(-62, -730), (-40, -780), (0, -790), (40, -780), (62, -730)], k=0.2, closed=False)
        line(ctx, [(0, -726), (0, -768)], SINDOOR, 10)                  # sindoor tilak
        smooth(ctx, [(-74, -680), (-60, -600), (-20, -520), (0, -500), (20, -520), (60, -600), (74, -680),
                     (30, -650), (0, -656), (-30, -650)], k=0.12)        # long beard
        ink(ctx, hexc("#EDEAE4"), 2)
        smooth(ctx, [(-46, -666), (0, -676), (46, -666), (32, -652), (0, -658), (-32, -652)])
        ink(ctx, hexc("#F8F6F2"), 2)
        ctx.arc(0, -652, 20, 0.2 * math.pi, 0.8 * math.pi)
        rgba(ctx, hexc("#7A3A2A"))
        ctx.set_line_width(5)
        ctx.stroke()
        ctx.restore()
    group(ctx, a, draw)


def hanuman(ctx, x, y, s, t, pose="abhaya", flip=False, a=1.0, aura=True, thread=0.0):
    pm.hanuman(ctx, x, y, s, t, pose=pose, flip=flip, a=a, aura=aura)
    if thread > 0 and pose == "abhaya":
        red_thread(ctx, x + (-1 if flip else 1) * 176 * s, y - 360 * s, s * 1.6, 0.6 * thread)


def relatives(ctx, x0, T, n=3, laugh=1.0, sweets=False, point=True, a=1.0):
    """Relatives as dark silhouettes laughing at the door (no faces - nobody real is mocked)."""
    for k in range(n):
        x = x0 + 170 * k
        bob = -10 * abs(math.sin(T * 9 + k)) * laugh
        if k % 2:
            dv.silhouette(ctx, lambda x=x, bob=bob: gudiya(ctx, x, GROUND + bob, 0.56, T, pose="talk" if point else "stand",
                                                           flip=True), c=hexc("#24161E"), a=a)
        else:
            dv.silhouette(ctx, lambda x=x, bob=bob: papa(ctx, x, GROUND + bob, 0.58, T, flip=True),
                          c=hexc("#1E1418"), a=a)
        if sweets:
            rrect(ctx, x - 60, GROUND - 330, 120, 50, 6)
            ink(ctx, hexc("#F0A020"), 3)
            line(ctx, [(x - 60, GROUND - 305), (x + 60, GROUND - 305)], hexc("#C8282A"), 6)


def rickshaw(ctx, x, y, s, T, rider=True, rider_pose="ride", passenger=None, move=0.0, wet=0.0, thread=0.0):
    """Cycle rickshaw facing right: a small Hanuman ji picture on the front, hooded passenger seat at the back."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    spin = T * 6 * move
    for wx, r in ((-260, 120), (60, 120), (420, 110)):
        circle(ctx, wx, -r, r, hexc("#1A1A1A"))
        circle(ctx, wx, -r, r - 14, hexc("#5A5A5A"))
        for k in range(8):
            ang = spin + k * math.pi / 4
            line(ctx, [(wx, -r), (wx + (r - 14) * math.cos(ang), -r + (r - 14) * math.sin(ang))], hexc("#9A9A9A"), 3)
    smooth(ctx, [(-420, -170), (-120, -170), (-80, -320), (-420, -320)], k=0.05)    # seat box
    ink(ctx, hexc("#2E6A3A"), 4)
    smooth(ctx, [(-440, -320), (-460, -560), (-300, -640), (-100, -560), (-90, -320)], k=0.2)   # hood
    ink(ctx, hexc("#1E3A6A"), 4)
    line(ctx, [(-120, -200), (420, -200)], hexc("#3A3A3A"), 14)                    # frame
    line(ctx, [(140, -200), (160, -420)], hexc("#3A3A3A"), 12)
    line(ctx, [(380, -420), (420, -110)], hexc("#3A3A3A"), 12)
    line(ctx, [(340, -470), (460, -470)], hexc("#3A3A3A"), 12)                     # handlebar
    rrect(ctx, 360, -460, 90, 100, 8)                                              # Hanuman ji picture
    ink(ctx, hexc("#F4C46A"), 4)
    ctx.save()
    rrect(ctx, 366, -454, 78, 88, 6)
    ctx.clip()
    pm.hanuman(ctx, 405, -330, 0.12, T, pose="gada", aura=False)
    ctx.restore()
    glow(ctx, 405, -410, 70, GOLDEN, 0.25)
    for k in range(5):
        circle(ctx, 370 + 18 * k, -468, 6, hexc("#FF8A1E") if k % 2 else hexc("#FFC21E"))
    if passenger is not None:
        passenger(ctx)
    if rider:
        shambhu(ctx, 150, -40, 0.72, T * (1 + move), pose=rider_pose, mood="neutral", wet=wet, thread=thread)
    ctx.restore()


# ============================================================ backgrounds

def bg_room(ctx, T, night=True, lamp=1.0, altar=1.0):
    """One-room home: plaster walls, small window, cot, tin trunk, Hanuman ji's corner altar with a diya."""
    sky(ctx, (((0.0, "#2A2234"), (1.0, "#3A2A30")) if night else ((0.0, "#C8A880"), (1.0, "#9A7A5A"))))
    rrect(ctx, 820, 170, 300, 260, 6)                                              # window
    ink(ctx, hexc("#5A3A22"), 6)
    ctx.save()
    rrect(ctx, 832, 182, 276, 236, 4)
    ctx.clip()
    sky(ctx, (((0.0, "#0A1030"), (1.0, "#2A3A6A")) if night else ((0.0, "#7AB8F0"), (1.0, "#F8E0B0"))))
    if night:
        circle(ctx, 1040, 250, 34, hexc("#F4F4FF"))
    ctx.restore()
    line(ctx, [(970, 182), (970, 418)], hexc("#5A3A22"), 6)
    for k in range(5):                                                             # wall cracks / plaster
        line(ctx, [(200 + 300 * k, 120 + 60 * (k % 2)), (230 + 300 * k, 200)], hexc("#2A1A20") if night else
             hexc("#8A6A4A"), 3, 0.4)
    rrect(ctx, 260, 250, 150, 190, 4)                                              # calendar
    ink(ctx, hexc("#F4ECD8"), 3)
    for r in range(4):
        for c in range(5):
            rrect(ctx, 274 + 27 * c, 320 + 28 * r, 20, 20, 2)
            rgba(ctx, hexc("#B8A888"), 0.8)
            ctx.fill()
    rrect(ctx, 1390, 470, 300, 22, 4)                                              # altar shelf
    ink(ctx, hexc("#7A4A1E"), 3)
    glow(ctx, 1540, 380, 220, GOLDEN, (0.25 + 0.05 * math.sin(T * 2.3)) * lamp * altar)
    smooth(ctx, [(1420, 470), (1420, 300), (1540, 230), (1660, 300), (1660, 470)], k=0.05)
    rgba(ctx, hexc("#5A2A1E"), 0.9)
    ctx.fill()
    pm.hanuman(ctx, 1540, 466, 0.2, T, pose="gada", aura=False)
    dv.diya(ctx, 1640, 466, 0.55 * lamp + 0.01, T, a=altar)
    for k in range(7):
        circle(ctx, 1410 + 44 * k, 500, 9, hexc("#FF8A1E") if k % 2 else hexc("#FFC21E"))
    ctx.rectangle(-200, GROUND - 40, W + 400, H)
    rgba(ctx, hexc("#3A2A22") if night else hexc("#7A5A40"))
    ctx.fill()
    rrect(ctx, 60, GROUND - 190, 520, 40, 6)                                       # charpai (cot)
    ink(ctx, hexc("#8A5A2A"), 4)
    for k in range(10):
        line(ctx, [(80 + 50 * k, GROUND - 186), (100 + 50 * k, GROUND - 154)], hexc("#D8C098"), 3)
    for lx in (80, 560):
        line(ctx, [(lx, GROUND - 150), (lx, GROUND - 40)], hexc("#6A4A22"), 14)
    rrect(ctx, 1700, GROUND - 190, 180, 150, 8)                                    # tin trunk
    ink(ctx, hexc("#4A6A8A"), 4)
    if night:
        rgba(ctx, (0.02, 0.02, 0.1), 0.25 * (1 - 0.4 * lamp))
        ctx.paint()


def bg_street(ctx, T, mode="day", u_sky=None):
    """City lane with shops, lamp posts and a road. mode: dawn | day | dusk | night | rain."""
    skies = {"dawn": ((0.0, "#3A4A8A"), (0.5, "#F8A070"), (1.0, "#F8D8A0")),
             "day": ((0.0, "#6AA8E8"), (0.6, "#CDE4F4"), (1.0, "#F4E8C8")),
             "dusk": ((0.0, "#2A1A3A"), (0.45, "#B8564A"), (1.0, "#F0A060")),
             "night": ((0.0, "#060A1E"), (0.6, "#1A2040"), (1.0, "#2A2A40")),
             "rain": ((0.0, "#0A0E1A"), (0.6, "#1E2634"), (1.0, "#2A303C"))}
    sky(ctx, skies[mode])
    if mode in ("day", "dawn"):
        dv.sun_disc(ctx, 1600, 200 if mode == "day" else 420, 70, T, a=0.9, rays=14)
    elif mode == "dusk":
        dv.sun_disc(ctx, 1600, 520, 70, T, a=0.8, rays=12)
    elif mode == "night":
        glow(ctx, 1600, 180, 120, hexc("#EEF2FF"), 0.4)
        circle(ctx, 1600, 180, 44, hexc("#F4F4FF"))
    dark = mode in ("night", "rain")
    for k in range(9):                                                             # buildings
        bx = -100 + 240 * k
        bh = 360 + 140 * rnd(k, 4)
        rrect(ctx, bx, GROUND - 120 - bh, 230, bh, 3)
        rgba(ctx, hexc("#2A2430") if dark else hexc(("#C89A7A", "#A8B0B8", "#D8B888")[k % 3]))
        ctx.fill()
        for r in range(int(bh // 110)):
            for c in range(2):
                lit = rnd(k * 7 + r, c) > 0.45
                rrect(ctx, bx + 40 + 90 * c, GROUND - 80 - bh + 40 + 110 * r, 56, 66, 3)
                rgba(ctx, hexc("#FFC86A") if (dark and lit) else (hexc("#5A6A7A") if not dark else hexc("#14121A")), 0.9)
                ctx.fill()
        rrect(ctx, bx + 20, GROUND - 120 - 10, 190, 12, 2)
        rgba(ctx, hexc(("#C8282A", "#2E6A8A", "#E8A020")[k % 3]), 0.9)
        ctx.fill()
    for lx in (380, 1240):                                                         # lamp posts
        line(ctx, [(lx, GROUND - 40), (lx, GROUND - 520)], hexc("#2A2A2A"), 10)
        line(ctx, [(lx, GROUND - 520), (lx + 70, GROUND - 520)], hexc("#2A2A2A"), 8)
        if dark or mode == "dusk":
            glow(ctx, lx + 70, GROUND - 500, 160, hexc("#FFD08A"), 0.45)
        circle(ctx, lx + 70, GROUND - 505, 14, hexc("#FFE6A0") if dark else hexc("#C8C8C8"))
    ctx.rectangle(-200, GROUND - 120, W + 400, 80)                                 # footpath
    rgba(ctx, hexc("#4A4A52") if dark else hexc("#A89A88"))
    ctx.fill()
    ctx.rectangle(-200, GROUND - 40, W + 400, H)                                   # road
    rgba(ctx, hexc("#24242C") if dark else hexc("#5A5A62"))
    ctx.fill()
    for k in range(8):
        rrect(ctx, 60 + 250 * k, GROUND + 30, 130, 10, 4)
        rgba(ctx, hexc("#E8E8E8"), 0.5)
        ctx.fill()
    if mode == "rain":
        for i in range(10):                                                        # puddle shine
            ell(ctx, 200 + 180 * i, GROUND + 70, 60, 8)
            rgba(ctx, hexc("#8AA8C8"), 0.25)
            ctx.fill()


def bg_temple(ctx, T, mode="dusk", light=0.0, murti=True, thread=0.0, crowd=False):
    """Hanuman mandir: sindoori shikhara, saffron flags, wide steps, the murti with gada in an open sanctum."""
    skies = {"dusk": ((0.0, "#2A1A3A"), (0.45, "#C85A3A"), (1.0, "#F4A860")),
             "night": ((0.0, "#060A1E"), (0.6, "#1A2040"), (1.0, "#2A2A40")),
             "day": ((0.0, "#6AA8E8"), (0.6, "#CDE4F4"), (1.0, "#F4E8C8"))}
    sky(ctx, skies[mode])
    if mode == "dusk":
        dv.sun_disc(ctx, 260, 560, 70, T, a=0.8, rays=12)
    smooth(ctx, [(640, 860), (640, 420), (800, 230), (960, 80), (1120, 230), (1280, 420), (1280, 860)], k=0.05)
    ink(ctx, hexc("#E8743A"), 5)
    for k in range(6):
        line(ctx, [(680 + 14 * k, 400 + 70 * k), (1240 - 14 * k, 400 + 70 * k)], hexc("#B8502A"), 4, 0.6)
    for fx, top in ((960, 80), (700, 380), (1220, 380)):
        line(ctx, [(fx, top), (fx, top - 90)], hexc("#7A4A1E"), 6)
        ctx.move_to(fx, top - 90)
        ctx.line_to(fx + 80 + 10 * math.sin(T * 4), top - 64)
        ctx.line_to(fx, top - 40)
        ctx.close_path()
        ink(ctx, SAFF, 3)
    smooth(ctx, [(780, 880), (780, 540), (960, 420), (1140, 540), (1140, 880)], k=0.08)    # sanctum
    rgba(ctx, hexc("#4A1A14"))
    ctx.fill()
    glow(ctx, 960, 680, 280, GOLDEN, 0.4 + 0.5 * light)
    if light > 0:
        for k in range(12):
            ang = -math.pi / 2 + (k - 5.5) * 0.22
            line(ctx, [(960, 680), (960 + 1200 * math.cos(ang), 680 + 1200 * math.sin(ang))], GOLD_HI, 12, 0.18 * light)
    rrect(ctx, 870, 820, 180, 50, 6)                                               # pedestal
    ink(ctx, hexc("#D8C8A8"), 4)
    if murti:
        hanuman(ctx, 960, 822, 0.34, T, pose="abhaya", aura=False, thread=thread)
    for k in range(9):
        circle(ctx, 810 + 37.5 * k, 540 - 70 * math.sin(math.pi * k / 8), 9, hexc("#FF8A1E") if k % 2 else hexc("#FFC21E"))
    for bx in (700, 1220):                                                         # bells
        line(ctx, [(bx, 470), (bx, 540)], hexc("#5A3A1E"), 5)
        smooth(ctx, [(bx - 30, 600), (bx - 24, 556), (bx - 12, 540), (bx + 12, 540), (bx + 24, 556), (bx + 30, 600)], k=0.1)
        ink(ctx, GOLD, 3)
    ctx.rectangle(-200, GROUND - 100, W + 400, H)
    rgba(ctx, hexc("#7A5A44") if mode != "night" else hexc("#3A3034"))
    ctx.fill()
    for k in range(4):                                                             # steps
        rrect(ctx, 560 - 40 * k, 870 + 22 * k, 800 + 80 * k, 22, 3)
        rgba(ctx, hexc("#C8B090") if mode != "night" else hexc("#5A5058"))
        ctx.fill()
    for k in range(12):
        dv.diya(ctx, 80 + 160 * k, GROUND - 96, 0.5, T + k, a=1.0)
    if crowd:
        for k in range(10):
            xx = 680 + 60 * k
            dv.silhouette(ctx, lambda xx=xx: papa(ctx, xx, 880, 0.26, T), c=hexc("#2A1A20"), a=0.8)


def bg_ocean(ctx, T):
    """Hanuman ji's leap over the ocean (the father's lesson)."""
    sky(ctx, ((0.0, "#1A2A6A"), (0.5, "#F8A060"), (0.62, "#FFD9A0"), (1.0, "#1A4A7A")))
    dv.sun_disc(ctx, 1500, 560, 90, T, a=0.9, rays=16)
    ctx.rectangle(-200, 620, W + 400, H)
    g = cairo.LinearGradient(0, 620, 0, H)
    g.add_color_stop_rgb(0, *hexc("#2A6A9A"))
    g.add_color_stop_rgb(1, *hexc("#0A2A4A"))
    ctx.set_source(g)
    ctx.fill()
    for i in range(40):
        x = (rnd(i, 3) * W + T * 40) % W
        y = 640 + rnd(i, 4) * 400
        line(ctx, [(x, y), (x + 60, y)], hexc("#BFE4FF"), 3, 0.35)
    smooth(ctx, [(-200, 760), (0, 640), (220, 620), (360, 700), (380, H), (-200, H)], k=0.1)   # this shore
    ink(ctx, hexc("#3A5A2A"), 3)
    smooth(ctx, [(1700, H), (1720, 700), (1860, 640), (2120, 680), (2120, H)], k=0.1)          # Lanka shore
    ink(ctx, hexc("#4A3A2A"), 3)


BGS = {"room": lambda c, T, **k: bg_room(c, T, night=True, **k), "roomday": lambda c, T, **k: bg_room(c, T, night=False, **k),
       "street": lambda c, T, **k: bg_street(c, T, "day", **k), "dawn": lambda c, T, **k: bg_street(c, T, "dawn", **k),
       "dusk": lambda c, T, **k: bg_street(c, T, "dusk", **k), "night": lambda c, T, **k: bg_street(c, T, "night", **k),
       "rain": lambda c, T, **k: bg_street(c, T, "rain", **k), "temple": lambda c, T, **k: bg_temple(c, T, "dusk", **k),
       "templenight": lambda c, T, **k: bg_temple(c, T, "night", **k), "templeday": lambda c, T, **k: bg_temple(c, T, "day", **k),
       "ocean": lambda c, T, **k: bg_ocean(c, T)}


# ============================================================ stage

RIGS = {"shambhu": shambhu, "gudiya": gudiya, "baba": baba, "hanuman": hanuman,
        "kid": lambda ctx, x, y, s, t, **k: boy(ctx, x, y, s, t, seated=True, **k)}


def actor(ctx, S, who, x, pose=None, s=0.6, y=GROUND, flip=False, enter=None, fade=None, appear=None, bow=0.0,
          kw=None):
    """enter=(x0, seconds) walks in; fade=(u0, u1) fades out; appear=(u0, u1) fades in; bow tips forward."""
    a = 1.0
    if enter:
        x = lerp(enter[0], x, ease_out_cubic(clamp(S.t / enter[1])))
    if fade:
        a *= 1 - clamp((S.u - fade[0]) / max(0.01, fade[1] - fade[0]))
    if appear:
        a *= clamp((S.u - appear[0]) / max(0.01, appear[1] - appear[0]))
    if a <= 0.01:
        return
    kw = dict(kw or {})
    if pose:
        kw["pose"] = pose
    if flip:
        kw["flip"] = True
    ctx.save()
    if bow > 0:
        b = ease_in_out(bow)
        ctx.translate(x, y)
        ctx.rotate(0.8 * b * (-1 if flip else 1))
        RIGS[who](ctx, 0, 120 * s * b, s, S.T, a=a, **kw)
    else:
        RIGS[who](ctx, x, y, s, S.T, a=a, **kw)
    ctx.restore()


def stage(ctx, S, bg="room", bgkw=None, cast=(), fx=(), zoom=None, rick=None):
    ctx.save()
    if zoom:
        z = lerp(zoom[0], zoom[1], ease_in_out(S.u))
        ctx.translate(zoom[2], zoom[3])
        ctx.scale(z, z)
        ctx.translate(-zoom[2], -zoom[3])
    BGS[bg](ctx, S.T, **(bgkw or {}))
    behind = [f for f in fx if f[0] in ("glow", "rays", "dream", "hanuman_light")]
    for f in behind:
        effect(ctx, S, *f)
    if rick is not None:
        k = dict(rick)
        rx = k.pop("x", 960)
        if "drive" in k:
            x0, x1 = k.pop("drive")
            rx = lerp(x0, x1, S.u)
        if k.get("passenger") == "baba":
            k["passenger"] = lambda c, T=S.T: baba(c, -260, -150, 0.66, T, pose="stand", seated=True)
        rickshaw(ctx, rx, GROUND + 40, k.pop("s", 0.62), S.T, **k)
    for c in cast:
        actor(ctx, S, **c)
    for f in fx:
        if f not in behind:
            effect(ctx, S, *f)
    ctx.restore()


def effect(ctx, S, kind, *p):
    u, T = S.u, S.T
    if kind == "glow":
        x, y, r, c = p
        glow(ctx, x, y, r, c, 0.5)
    elif kind == "rays":
        x, y = p[:2]
        k = clamp(u / 0.4)
        for i in range(14):
            ang = i * math.tau / 14 + T * 0.2
            line(ctx, [(x, y), (x + 1300 * math.cos(ang), y + 1300 * math.sin(ang))], GOLD_HI, 14, 0.16 * k)
        glow(ctx, x, y, 380, GOLD_HI, 0.6 * k)
    elif kind == "petals":
        petals(ctx, T, a=p[0] if p else 1.0)
    elif kind == "rain":
        rain(ctx, T, a=p[0] if p else 1.0)
    elif kind == "lightning":
        at = p[0] if p else 0.4
        f = clamp(1 - abs(u - at) / 0.08)
        if f > 0:
            rgba(ctx, (0.9, 0.95, 1.0), 0.75 * f)
            ctx.paint()
    elif kind == "shadow_gada":                                    # Hanuman ji's shadow with the gada on the wall
        x, at = p
        f = clamp((u - at + 0.08) / 0.1)
        if f > 0:
            glow(ctx, x, GROUND - 450, 520, hexc("#C8D8FF"), 0.35 * f)
            dv.silhouette(ctx, lambda: pm.hanuman(ctx, x, GROUND - 60, 0.95, T, pose="gada", aura=False),
                          c=hexc("#05050C"), a=0.9 * f)
    elif kind == "hanuman_light":
        x, s, a = p
        k = clamp(u / 0.35) * a
        glow(ctx, x, GROUND - 480 * s, 480 * s, GOLDEN, 0.5 * k)
        hanuman(ctx, x, GROUND, s, T, pose="abhaya", a=k)
    elif kind == "sparkles":
        x, y = p[:2]
        sparkles(ctx, x, y, T, r=p[2] if len(p) > 2 else 200, a=clamp(u / 0.3))
    elif kind == "dream":                                           # golden ghost: Gudiya as a doctor
        x, a = p
        k = clamp(u / 0.4) * a
        glow(ctx, x, GROUND - 420, 320, GOLDEN, 0.4 * k)
        gudiya(ctx, x, GROUND - 30, 0.5, T, pose="stand", mood="smile", coat=True, a=0.6 * k)
    elif kind == "thread":
        x, y, s = p
        red_thread(ctx, x, y, s, 0.5 + 0.3 * math.sin(T * 4))
    elif kind == "money":                                           # tall stack (fees) vs small stack (earning)
        x, n, c = p
        for k in range(int(n * clamp(u / 0.5 + 0.2))):
            rrect(ctx, x - 70, GROUND - 60 - 18 * k, 140, 16, 3)
            ink(ctx, hexc(c), 2)
    elif kind == "empty_box":
        x = p[0]
        rrect(ctx, x - 90, GROUND - 160, 180, 120, 8)
        ink(ctx, hexc("#4A6A8A"), 4)
        rrect(ctx, x - 90, GROUND - 230 - 40 * clamp(u / 0.3), 180, 26, 6)
        ink(ctx, hexc("#5A7A9A"), 3)
        glow(ctx, x, GROUND - 120, 90, hexc("#FF4A4A"), 0.25 * clamp(u / 0.4))
    elif kind == "phone":                                           # big phone screen with a list (no text)
        x, y, state = p
        rrect(ctx, x - 150, y - 260, 300, 520, 26)
        ink(ctx, hexc("#14141C"), 4)
        rrect(ctx, x - 130, y - 230, 260, 460, 12)
        rgba(ctx, hexc("#F4F6FA"))
        ctx.fill()
        for r in range(9):
            top = state == "top" and r == 0 and u > 0.3
            rrect(ctx, x - 110, y - 200 + 48 * r, 220, 30, 4)
            rgba(ctx, GOLD_HI if top else hexc("#C8CCD8"), 1.0 if top else 0.8)
            ctx.fill()
        if state == "top" and u > 0.3:
            sparkles(ctx, x, y - 185, T, r=170)
            glow(ctx, x, y - 185, 160, GOLD_HI, 0.5)
        if state == "miss":
            glow(ctx, x, y, 260, hexc("#FF3A3A"), 0.3 * clamp(u / 0.3))
    elif kind == "calendar":                                        # pages flying off = time passing
        x, y = p
        for k in range(8):
            fu = clamp(u * 8 - k)
            if 0 < fu < 1:
                ctx.save()
                ctx.translate(x + 500 * fu, y - 300 * fu)
                ctx.rotate(fu * 2)
                rrect(ctx, -90, -110, 180, 220, 6)
                ink(ctx, hexc("#F4ECD8"), 3)
                ctx.restore()
        rrect(ctx, x - 90, y - 110, 180, 220, 6)
        ink(ctx, hexc("#F4ECD8"), 3)
        rrect(ctx, x - 90, y - 110, 180, 50, 6)
        rgba(ctx, hexc("#C8282A"))
        ctx.fill()
    elif kind == "clock":
        x, y = p
        circle(ctx, x, y, 70, hexc("#F4ECD8"))
        ctx.arc(x, y, 70, 0, math.tau)
        rgba(ctx, hexc("#3A2A1E"))
        ctx.set_line_width(6)
        ctx.stroke()
        for ang, L in ((T * 3, 50), (T * 0.25, 34)):
            line(ctx, [(x, y), (x + L * math.sin(ang), y - L * math.cos(ang))], hexc("#2A1A10"), 6)
    elif kind == "timetable":
        x, y = p
        rrect(ctx, x - 160, y - 200, 320, 400, 6)
        ink(ctx, hexc("#F8F4E8"), 3)
        for r in range(7):
            for c in range(4):
                if r * 4 + c < int(28 * clamp(u / 0.8)):
                    rrect(ctx, x - 140 + 72 * c, y - 180 + 54 * r, 60, 40, 4)
                    rgba(ctx, hexc(("#9BE07A", "#FFC86A", "#9AD8FF", "#F4A0B0")[c]), 0.9)
                    ctx.fill()
    elif kind == "chai":                                            # roadside chai stall he walks past
        x = p[0]
        rrect(ctx, x - 160, GROUND - 260, 320, 220, 8)
        ink(ctx, hexc("#8A5A2A"), 4)
        circle(ctx, x - 60, GROUND - 290, 40, hexc("#5A5A5A"))
        for k in range(3):
            fu = (T * 0.6 + k / 3) % 1
            circle(ctx, x - 60 + 10 * math.sin(T * 3 + k), GROUND - 340 - 120 * fu, 16 + 10 * fu, hexc("#F4F4F4"),
                   0.4 * (1 - fu))
        for k in range(4):
            rrect(ctx, x + 10 + 30 * k, GROUND - 300, 22, 30, 4)
            ink(ctx, hexc("#F4E8D0"), 2)
    elif kind == "bookclose":
        x, y = p
        k = clamp(u / 0.5)
        ctx.save()
        ctx.translate(x, y)
        smooth(ctx, [(-160 * (1 - k) - 10, 0), (0, -10), (0, 120), (-160 * (1 - k) - 10, 120)], k=0.02)
        ink(ctx, hexc("#F8F4E8"), 3)
        smooth(ctx, [(0, -10), (160, 0), (160, 120), (0, 120)], k=0.02)
        ink(ctx, hexc("#2E6A8A"), 3)
        ctx.restore()
    elif kind == "chalisa":                                         # close-up: orange Hanuman Chalisa booklet
        x, y = p
        glow(ctx, x, y, 260, GOLDEN, 0.45 + 0.1 * math.sin(T * 3))
        rrect(ctx, x - 170, y - 230, 340, 460, 14)
        ink(ctx, SAFF, 5)
        ctx.save()
        rrect(ctx, x - 140, y - 200, 280, 300, 10)
        ctx.clip()
        rgba(ctx, hexc("#FFE2A8"))
        ctx.paint()
        pm.hanuman(ctx, x, y + 230, 0.38, T, pose="namaste", aura=False)
        ctx.restore()
        for r in range(3):
            line(ctx, [(x - 120, y + 140 + 28 * r), (x + 120, y + 140 + 28 * r)], hexc("#7A2A10"), 6, 0.6)
    elif kind == "vignette":
        g = cairo.RadialGradient(W / 2, H / 2, 300, W / 2, H / 2, 1100)
        g.add_color_stop_rgba(0, 0, 0, 0, 0)
        g.add_color_stop_rgba(1, 0, 0, 0, p[0] if p else 0.6)
        ctx.set_source(g)
        ctx.paint()


def sc(bg="room", cast=(), fx=(), zoom=None, rick=None, bgkw=None, sfx=None):
    d = dict(bg=bg, cast=list(cast), fx=list(fx), zoom=zoom, rick=rick, bgkw=bgkw)
    if sfx:
        d["_sfx"] = sfx
    return stage, d


def C(who, x, pose=None, **kw):
    out = dict(who=who, x=x, pose=pose)
    for k in ("s", "y", "flip", "enter", "fade", "appear", "bow"):
        if k in kw:
            out[k] = kw.pop(k)
    if kw:
        out["kw"] = kw
    return out


def L_(hi, roman, shot):
    fn, params = shot
    return (hi, roman, fn, params)


SL, SR_ = 640, 1280          # two-character marks
ALTAR = (1540, 380)
MURTI_WRIST = (960 + 176 * 0.34, 822 - 360 * 0.34)

# ============================================================ story (10 chapters)

CHAPTERS = [
    {"key": "hook", "title": "HANUMAN JI KA BHAKT", "lines": [
        L_("आज हम हनुमान जी के एक ऐसे भक्त की बात करेंगे।", "AAJ HUM HANUMAN JI KE EK AISE BHAKT KI BAAT KARENGE",
           sc("temple", cast=[C("shambhu", 520, "namaste", s=0.56, mood="smile")], zoom=(1.0, 1.12, 960, 600), sfx="ghanti")),
        L_("जिसकी मदद करने खुद हनुमान जी आए।", "JISKI MADAD KARNE KHUD HANUMAN JI AAYE",
           sc("temple", bgkw=dict(light=1.0, murti=False), fx=[("hanuman_light", 960, 0.62, 1.0), ("petals",)], sfx="shimmer")),
        L_("वो था एक गरीब रिक्शा वाला।", "WO THA EK GAREEB RIKSHA WAALA",
           sc("dusk", rick=dict(drive=(-300, 900), move=1.0))),
        L_("जिसकी बेटी का सपना था डॉक्टर बनना।", "JISKI BETI KA SAPNA THA DOCTOR BANNA",
           sc("room", cast=[C("gudiya", 640, "study", seated=True, mood="neutral", look=(0.4, 0.5))],
              fx=[("dream", 1060, 1.0)])),
        L_("अगर आप भी हनुमान जी के भक्त हो तो ये कहानी पूरी सुनकर जाना।",
           "AGAR AAP BHI HANUMAN JI KE BHAKT HO TO YE KAHANI POORI SUNKAR JAANA",
           sc("temple", cast=[C("shambhu", 560, "namaste", s=0.56), C("gudiya", 1360, "namaste", s=0.54, flip=True)],
              fx=[("petals", 0.7)])),
        L_("तो कहानी शुरू होती है एक छोटे से कमरे से।", "TO KAHANI SHURU HOTI HAI EK CHHOTE SE KAMRE SE",
           sc("room", zoom=(1.5, 1.0, 970, 300))),
    ]},
    {"key": "sapna", "title": "SAPNA", "lines": [
        L_("शंभू दिन भर रिक्शा चलाता था।", "SHAMBHU DIN BHAR RIKSHA CHALAATA THA",
           sc("street", rick=dict(drive=(1900, 500), move=1.0), fx=[])),
        L_("रिक्शा के आगे हनुमान जी की छोटी सी तस्वीर लगी थी।", "RIKSHA KE AAGE HANUMAN JI KI CHHOTI SI TASVEER LAGI THI",
           sc("street", rick=dict(x=760), zoom=(1.0, 2.2, 1010, 700))),
        L_("हर सवारी से पहले वो बोलता जय बजरंगबली।", "HAR SAWAARI SE PEHLE WO BOLTA JAI BAJRANGBALI",
           sc("street", cast=[C("shambhu", 1300, "namaste", s=0.58, mood="smile")], rick=dict(x=640, rider=False),
              fx=[("glow", 891, 616, 120, GOLDEN)])),
        L_("घर में बस एक ही कमरा था।", "GHAR MEIN BAS EK HI KAMRA THA", sc("roomday", zoom=(1.12, 1.0, 960, 540))),
        L_("और कोने में हनुमान जी का छोटा सा मंदिर।", "AUR KONE MEIN HANUMAN JI KA CHHOTA SA MANDIR",
           sc("roomday", zoom=(1.0, 1.9, 1540, 400))),
        L_("गुड़िया रोज़ रात उसी दिए की रोशनी में पढ़ती थी।", "GUDIYA ROZ RAAT USI DIYE KI ROSHNI MEIN PADHTI THI",
           sc("room", cast=[C("gudiya", 1240, "write", seated=True, look=(0.3, 0.6))], fx=[("glow", 1450, 760, 300, GOLDEN)])),
        L_("एक दिन पापा के पैरों में छाले देखकर वो बोली।", "EK DIN PAPA KE PAIRON MEIN CHHAALE DEKHKAR WO BOLI",
           sc("room", cast=[C("shambhu", 300, "sit", s=0.58, mood="tired", y=GROUND - 150),
                            C("gudiya", 700, "press", seated=True, s=0.56, flip=True, mood="sad", look=(-0.5, 0.5))],
              fx=[("glow", 500, GROUND - 120, 90, hexc("#FF5A3A"))])),
        L_("पापा मैं डॉक्टर बनूंगी।", "PAPA MAIN DOCTOR BANUNGI",
           sc("room", cast=[C("shambhu", 300, "sit", s=0.58, mood="shock", y=GROUND - 150),
                            C("gudiya", 820, "talk", s=0.56, flip=True, mood="neutral")], fx=[("dream", 1280, 0.9)])),
        L_("फिर आपको कभी दर्द नहीं होगा।", "PHIR AAPKO KABHI DARD NAHIN HOGA",
           sc("room", cast=[C("shambhu", 760, "hug", s=0.58, mood="smile"), C("gudiya", 960, "hug", s=0.56, flip=True,
                                                                                mood="joy")])),
        L_("शंभू हंस दिया पर उसकी आंखें भीग गईं।", "SHAMBHU HANS DIYA PAR USKI AANKHEIN BHEEG GAYIN",
           sc("room", cast=[C("shambhu", 960, "stand", s=0.6, mood="cry")], zoom=(1.0, 1.6, 960, 520))),
        L_("उस रात उसने हनुमान जी से बस इतना कहा।", "US RAAT USNE HANUMAN JI SE BAS ITNA KAHA",
           sc("room", cast=[C("shambhu", 1180, "namaste", s=0.58, look=(0.6, -0.5))], bgkw=dict(lamp=0.8))),
        L_("बाबा मेरी बेटी का सपना टूटने मत देना।", "BAABA MERI BETI KA SAPNA TOOTNE MAT DENA",
           sc("room", cast=[C("shambhu", 1180, "namaste", s=0.58, mood="cry")], zoom=(1.0, 1.7, 1450, 420))),
        L_("मैं अपनी तरफ से कोई कमी नहीं छोड़ूंगा।", "MAIN APNI TARAF SE KOI KAMI NAHIN CHHODUNGA",
           sc("room", cast=[C("shambhu", 960, "stand", s=0.6, mood="neutral")], fx=[("glow", 1540, 380, 260, GOLDEN)],
              sfx="ghanti")),
    ]},
    {"key": "musibat", "title": "MUSIBAT", "lines": [
        L_("पर सपने सस्ते नहीं होते।", "PAR SAPNE SASTE NAHIN HOTE",
           sc("dusk", cast=[C("gudiya", 960, "stand", s=0.56, mood="sad", look=(0.0, -0.6))], fx=[("vignette", 0.5)])),
        L_("कोचिंग की फीस थी पूरे साठ हज़ार रुपये।", "COACHING KI FEES THI POORE SAATH HAZAAR RUPAYE",
           sc("dusk", cast=[C("gudiya", 600, "stand", s=0.56, mood="shock", look=(0.8, -0.4))],
              fx=[("money", 1200, 26, "#F4A0A0")], sfx="kaching")),
        L_("और शंभू महीने में मुश्किल से आठ हज़ार कमाता था।", "AUR SHAMBHU MAHINE MEIN MUSHKIL SE AATH HAZAAR KAMAATA THA",
           sc("room", cast=[C("shambhu", 700, "count", s=0.58, mood="sad", look=(0.0, 0.6))],
              fx=[("money", 1150, 4, "#B8D8A8")])),
        L_("रिश्तेदारों को पता चला तो सब हंसे।", "RISHTEDAARON KO PATA CHALA TO SAB HANSE",
           sc("roomday", cast=[C("shambhu", 360, "stand", s=0.58, mood="sad"),
                               C("gudiya", 560, "stand", s=0.54, mood="sad")],
              fx=[("_rel", 1150)])),
        L_("बोले रिक्शा वाले की बेटी डॉक्टर बनेगी।", "BOLE RIKSHA WAALE KI BETI DOCTOR BANEGI",
           sc("roomday", cast=[C("gudiya", 520, "stand", s=0.54, mood="cry")], fx=[("_rel", 1000)], zoom=(1.0, 1.15, 1200, 600))),
        L_("पहले घर का किराया तो भर ले।", "PEHLE GHAR KA KIRAAYA TO BHAR LE",
           sc("roomday", cast=[C("shambhu", 420, "stand", s=0.58, mood="sad", look=(0.0, 0.7))], fx=[("_rel", 1000)])),
        L_("गुड़िया चुपचाप अंदर चली गई।", "GUDIYA CHUPCHAAP ANDAR CHALI GAYI",
           sc("roomday", cast=[C("gudiya", 1500, "stand", s=0.54, mood="cry", enter=(700, 2.5), fade=(0.7, 1.0))])),
        L_("उस रात उसने अपनी किताबें बंद कर दीं।", "US RAAT USNE APNI KITAABEN BAND KAR DEEN",
           sc("room", cast=[C("gudiya", 760, "cry", seated=True, s=0.56)], fx=[("bookclose", 1100, 820)])),
        L_("तब शंभू उसके पास आकर बैठा।", "TAB SHAMBHU USKE PAAS AAKAR BAITHA",
           sc("room", cast=[C("gudiya", 900, "cry", seated=True, s=0.56),
                            C("shambhu", 560, "sit", s=0.58, y=GROUND - 150, mood="sad", enter=(-100, 2.0))])),
        L_("बोला बेटी लोग हंसते हैं तो हंसने दे।", "BOLA BETI LOG HANSTE HAIN TO HANSNE DE",
           sc("room", cast=[C("shambhu", 600, "pat", s=0.58, y=GROUND - 150, mood="smile"),
                            C("gudiya", 930, "stand", seated=True, s=0.56, mood="sad", look=(-0.6, -0.3))])),
        L_("हनुमान जी ने किसी से नहीं पूछा था कि समुद्र कितना बड़ा है।",
           "HANUMAN JI NE KISI SE NAHIN POOCHHA THA KI SAMUDRA KITNA BADA HAI",
           sc("ocean", cast=[C("hanuman", 260, "gada", s=0.5, y=700)], fx=[("glow", 260, 450, 260, GOLDEN)])),
        L_("उन्होंने बस छलांग लगा दी थी।", "UNHONE BAS CHHALAANG LAGA DI THI",
           sc("ocean", fx=[("_leap",)], sfx="whoosh")),
        L_("उसी दिन से शंभू ने दो शिफ्ट में रिक्शा चलाना शुरू किया।",
           "USI DIN SE SHAMBHU NE DO SHIFT MEIN RIKSHA CHALAANA SHURU KIYA",
           sc("dawn", rick=dict(drive=(-300, 1500), move=1.2))),
    ]},
    {"key": "mehnat", "title": "MEHNAT", "lines": [
        L_("सुबह पांच बजे से रात ग्यारह बजे तक।", "SUBAH PAANCH BAJE SE RAAT GYAARAH BAJE TAK",
           sc("night", rick=dict(drive=(1900, 300), move=1.2), fx=[("clock", 1700, 200)])),
        L_("धूप हो या बारिश रिक्शा कभी रुकता नहीं था।", "DHOOP HO YA BAARISH RIKSHA KABHI RUKTA NAHIN THA",
           sc("rain", rick=dict(drive=(-200, 1500), move=1.0, wet=1.0), fx=[("rain",)])),
        L_("गुड़िया ने कोचिंग का सपना छोड़ दिया।", "GUDIYA NE COACHING KA SAPNA CHHOD DIYA",
           sc("roomday", cast=[C("gudiya", 960, "stand", s=0.56, mood="sad", look=(0.4, 0.3))])),
        L_("वो पुरानी किताबें मांग कर लाई और खुद पढ़ने लगी।", "WO PURAANI KITAABEN MAANG KAR LAAYI AUR KHUD PADHNE LAGI",
           sc("roomday", cast=[C("gudiya", 900, "carry", s=0.56, mood="smile", enter=(1900, 2.0))])),
        L_("उसकी हर किताब में हनुमान चालीसा रखी रहती थी।", "USKI HAR KITAAB MEIN HANUMAN CHALISA RAKHI REHTI THI",
           sc("room", fx=[("chalisa", 960, 500)])),
        L_("जब नींद आती तो वो धीरे से बोलती।", "JAB NEEND AATI TO WO DHEERE SE BOLTI",
           sc("room", cast=[C("gudiya", 960, "study", seated=True, s=0.56, mood="sleep")], fx=[("clock", 1700, 200)])),
        L_("संकट कटे मिटे सब पीरा।", "SANKAT KATE MITE SAB PEERA",
           sc("room", cast=[C("gudiya", 760, "namaste", seated=True, s=0.56, mood="sleep")],
              fx=[("hanuman_light", 1300, 0.5, 0.45), ("glow", 760, 600, 220, GOLDEN)], sfx="shimmer")),
        L_("और फिर से पढ़ने बैठ जाती।", "AUR PHIR SE PADHNE BAITH JAATI",
           sc("room", cast=[C("gudiya", 960, "write", seated=True, s=0.56, look=(0.2, 0.6))])),
        L_("पापा रात को आते तो वो उनके पैर दबाती।", "PAPA RAAT KO AATE TO WO UNKE PAIR DABAATI",
           sc("room", cast=[C("shambhu", 300, "sit", s=0.58, y=GROUND - 150, mood="tired"),
                            C("gudiya", 700, "press", seated=True, s=0.56, flip=True, mood="smile")])),
        L_("और पापा उसके सिर पर हाथ रखकर सो जाते।", "AUR PAPA USKE SIR PAR HAATH RAKHKAR SO JAATE",
           sc("room", cast=[C("shambhu", 300, "pat", s=0.58, y=GROUND - 150, mood="sleep"),
                            C("gudiya", 640, "stand", seated=True, s=0.56, mood="sleep")], fx=[("vignette", 0.5)])),
        L_("एक साल ऐसे ही बीत गया।", "EK SAAL AISE HI BEET GAYA",
           sc("roomday", fx=[("calendar", 335, 345)], zoom=(1.0, 1.3, 335, 400))),
        L_("फिर आया पेपर का दिन।", "PHIR AAYA PAPER KA DIN",
           sc("street", cast=[C("gudiya", 1100, "namaste", s=0.56, mood="neutral"),
                              C("shambhu", 700, "talk", s=0.58, mood="smile")], rick=dict(x=300, rider=False))),
    ]},
    {"key": "haar", "title": "TOOTA HAUSLA", "lines": [
        L_("रिजल्ट आया।", "RESULT AAYA",
           sc("roomday", cast=[C("gudiya", 600, "phone", s=0.56, mood="neutral", look=(0.0, 0.6), shake=1.0)],
              fx=[("phone", 1260, 520, "wait")], sfx="beep")),
        L_("और गुड़िया का नाम लिस्ट में नहीं था।", "AUR GUDIYA KA NAAM LIST MEIN NAHIN THA",
           sc("roomday", cast=[C("gudiya", 600, "phone", s=0.56, mood="shock")], fx=[("phone", 1260, 520, "miss")])),
        L_("बस कुछ नंबरों से रह गई थी।", "BAS KUCHH NUMBERON SE REH GAYI THI",
           sc("roomday", cast=[C("gudiya", 960, "cry", s=0.58)], zoom=(1.0, 1.4, 960, 520))),
        L_("घर में सन्नाटा छा गया।", "GHAR MEIN SANNAATA CHHA GAYA",
           sc("room", cast=[C("shambhu", 360, "sit", s=0.58, y=GROUND - 150, mood="sad"),
                            C("gudiya", 900, "cry", seated=True, s=0.54)], bgkw=dict(lamp=0.4), fx=[("vignette", 0.7)])),
        L_("जोड़े हुए सारे पैसे भी अब जा चुके थे।", "JODE HUE SAARE PAISE BHI AB JA CHUKE THE",
           sc("room", cast=[C("shambhu", 1450, "stand", s=0.58, mood="sad", look=(0.6, 0.6))], fx=[("empty_box", 1790)])),
        L_("रिश्तेदार फिर आए और बोले।", "RISHTEDAAR PHIR AAYE AUR BOLE",
           sc("roomday", cast=[C("shambhu", 420, "stand", s=0.58, mood="sad")], fx=[("_rel", 1050)])),
        L_("देख लिया ना हमने तो पहले ही कहा था।", "DEKH LIYA NA HUMNE TO PEHLE HI KAHA THA",
           sc("roomday", cast=[C("gudiya", 420, "cry", s=0.54)], fx=[("_rel", 900)], zoom=(1.0, 1.15, 1100, 600))),
        L_("उस रात शंभू पहली बार हनुमान जी के आगे रो पड़ा।", "US RAAT SHAMBHU PEHLI BAAR HANUMAN JI KE AAGE RO PADA",
           sc("room", cast=[C("shambhu", 1200, "kneel", s=0.58, mood="cry", look=(0.6, -0.6))], bgkw=dict(lamp=0.6))),
        L_("बोला बाबा मैं हार गया।", "BOLA BAABA MAIN HAAR GAYA",
           sc("room", cast=[C("shambhu", 1200, "cry", s=0.6)], zoom=(1.0, 1.5, 1250, 500))),
        L_("अब मुझसे और नहीं होगा।", "AB MUJHSE AUR NAHIN HOGA",
           sc("room", cast=[C("shambhu", 1200, "kneelcry", s=0.58, mood="cry")], fx=[("vignette", 0.7)])),
        L_("और उसी रात कुछ ऐसा हुआ जो उसने कभी सोचा भी नहीं था।",
           "AUR USI RAAT KUCHH AISA HUA JO USNE KABHI SOCHA BHI NAHIN THA",
           sc("room", bgkw=dict(lamp=1.0), fx=[("glow", 1540, 380, 380, GOLD_HI), ("lightning", 0.6)],
              zoom=(1.0, 1.4, 1540, 400), sfx="shimmer")),
    ]},
    {"key": "sawari", "title": "ANJAAN SAWARI", "lines": [
        L_("रात के बारह बजे थे।", "RAAT KE BAARAH BAJE THE", sc("rain", fx=[("rain",), ("clock", 1700, 180)])),
        L_("बारिश हो रही थी और सड़क बिल्कुल खाली थी।", "BAARISH HO RAHI THI AUR SADAK BILKUL KHAALI THI",
           sc("rain", rick=dict(drive=(-300, 700), move=0.7, wet=1.0), fx=[("rain",)])),
        L_("तभी एक बूढ़े आदमी ने हाथ उठाया।", "TABHI EK BOODHE AADMI NE HAATH UTHAAYA",
           sc("rain", cast=[C("baba", 1400, "hail", s=0.58)], rick=dict(x=700, wet=1.0),
              fx=[("glow", 1310, 460, 200, hexc("#FFD08A")), ("rain",)])),
        L_("बोले बेटा मंदिर तक छोड़ दोगे।", "BOLE BETA MANDIR TAK CHHOD DOGE",
           sc("rain", cast=[C("baba", 1320, "talk", s=0.58)], rick=dict(x=760, wet=1.0), fx=[("rain",)])),
        L_("शंभू ने उन्हें बैठा लिया।", "SHAMBHU NE UNHEN BAITHA LIYA",
           sc("rain", rick=dict(x=900, wet=1.0, passenger="baba"), fx=[("rain",)])),
        L_("रास्ते भर वो बूढ़े बाबा चुप रहे।", "RAASTE BHAR WO BOODHE BAABA CHUP RAHE",
           sc("rain", rick=dict(drive=(300, 1300), move=0.8, wet=1.0, passenger="baba"), fx=[("rain", 0.7)])),
        L_("फिर अचानक धीरे से बोले।", "PHIR ACHAANAK DHEERE SE BOLE",
           sc("rain", rick=dict(x=960, move=0.4, wet=1.0, passenger="baba"), fx=[("rain", 0.6)],
              zoom=(1.0, 1.9, 800, 560))),
        L_("जो डरता है वो हारता है।", "JO DARTA HAI WO HAARTA HAI",
           sc("rain", cast=[C("baba", 960, "talk", s=0.62)], fx=[("glow", 960, 520, 300, GOLDEN), ("rain", 0.5)])),
        L_("तेरी बेटी फिर से लड़ेगी।", "TERI BETI PHIR SE LADEGI",
           sc("rain", rick=dict(drive=(500, 1100), move=0.8, wet=1.0, passenger="baba"), fx=[("rain", 0.6),
                                                                                              ("glow", 600, 600, 260, GOLDEN)])),
        L_("बजरंगी तेरे साथ है।", "BAJRANGI TERE SAATH HAI",
           sc("rain", cast=[C("baba", 960, "bless", s=0.62, divine=1.0)], fx=[("sparkles", 960, 520, 300)], sfx="shimmer")),
        L_("शंभू ने चौंक कर पीछे देखा।", "SHAMBHU NE CHAUNK KAR PEECHHE DEKHA",
           sc("rain", cast=[C("shambhu", 960, "stand", s=0.6, mood="shock", look=(-0.9, 0.0), wet=1.0)],
              fx=[("rain", 0.6)], zoom=(1.0, 1.3, 960, 500))),
        L_("बिजली चमकी और बाबा की परछाई में एक गदा दिखाई दी।", "BIJLI CHAMKI AUR BAABA KI PARCHHAAI MEIN EK GADA DIKHAAI DI",
           sc("night", cast=[C("baba", 700, "stand", s=0.58)], fx=[("rain", 0.8), ("lightning", 0.4), ("shadow_gada", 1300, 0.4)], sfx="boom")),
        L_("मंदिर आया तो शंभू बोला बाबा आपसे पैसे नहीं लूंगा।", "MANDIR AAYA TO SHAMBHU BOLA BAABA AAPSE PAISE NAHIN LOONGA",
           sc("templenight", cast=[C("shambhu", SR_, "namaste", s=0.58, flip=True, wet=1.0), C("baba", SL, "stand", s=0.58)],
              fx=[("rain", 0.4)])),
        L_("बाबा मुस्कुराए और उसकी कलाई पर एक लाल धागा बांध दिया।",
           "BAABA MUSKURAAYE AUR USKI KALAAI PAR EK LAAL DHAAGA BAANDH DIYA",
           sc("templenight", cast=[C("baba", 820, "tie", s=0.6, divine=0.5), C("shambhu", 1180, "show", s=0.6, flip=True,
                                                                                mood="shock", thread=1.0)],
              zoom=(1.0, 1.35, 1000, 520), sfx="shimmer")),
        L_("और मंदिर की भीड़ में कहीं खो गए।", "AUR MANDIR KI BHEED MEIN KAHIN KHO GAYE",
           sc("templenight", bgkw=dict(crowd=True), cast=[C("baba", 960, "walk", s=0.5, y=880, fade=(0.3, 0.8), divine=0.6),
                                                          C("shambhu", 1500, "stand", s=0.6, mood="shock", flip=True, thread=1.0)],
              fx=[("sparkles", 960, 640, 220)])),
    ]},
    {"key": "phir", "title": "PHIR SE", "lines": [
        L_("अगली सुबह शंभू घर आया।", "AGLI SUBAH SHAMBHU GHAR AAYA",
           sc("roomday", cast=[C("shambhu", 800, "stand", s=0.58, mood="neutral", enter=(-150, 2.0), thread=1.0)])),
        L_("गुड़िया को लाल धागा दिखाया और बोला।", "GUDIYA KO LAAL DHAAGA DIKHAAYA AUR BOLA",
           sc("roomday", cast=[C("shambhu", SL, "show", s=0.58, mood="smile", thread=1.0),
                               C("gudiya", SR_, "stand", s=0.56, flip=True, look=(-0.6, -0.4))])),
        L_("बेटी हम फिर से लड़ेंगे।", "BETI HUM PHIR SE LADENGE",
           sc("roomday", cast=[C("shambhu", 760, "hug", s=0.58, mood="smile", thread=1.0),
                               C("gudiya", 960, "hug", s=0.56, flip=True, mood="joy")], fx=[("glow", 1540, 380, 300, GOLDEN)],
              sfx="ghanti")),
        L_("इस बार गुड़िया ने खुद पढ़ाई का पूरा प्लान बनाया।", "IS BAAR GUDIYA NE KHUD PADHAAI KA POORA PLAN BANAAYA",
           sc("roomday", cast=[C("gudiya", 640, "teach", s=0.56, mood="neutral")], fx=[("timetable", 1000, 420)])),
        L_("दिन में छोटे बच्चों को ट्यूशन पढ़ाती और रात में खुद पढ़ती।",
           "DIN MEIN CHHOTE BACHCHON KO TUITION PADHAATI AUR RAAT MEIN KHUD PADHTI",
           sc("roomday", cast=[C("gudiya", 500, "teach", s=0.56, mood="smile"), C("kid", 900, None, s=0.3, look=(-0.6, -0.4)),
                               C("kid", 1100, None, s=0.3, look=(-0.6, -0.4)), C("kid", 1300, None, s=0.3, look=(-0.6, -0.4))])),
        L_("शंभू ने पैसे बचाने के लिए दोपहर की चाय तक छोड़ दी।", "SHAMBHU NE PAISE BACHAANE KE LIYE DOPAHAR KI CHAAY TAK CHHOD DI",
           sc("street", cast=[C("shambhu", 1400, "wipe", s=0.58, mood="tired", enter=(500, 4.0), thread=1.0)],
              fx=[("chai", 700)])),
        L_("जब भी हिम्मत टूटती वो कलाई का धागा देखता।", "JAB BHI HIMMAT TOOTTI WO KALAAI KA DHAAGA DEKHTA",
           sc("dusk", cast=[C("shambhu", 960, "show", s=0.6, mood="tired", thread=1.0, look=(0.6, -0.6))],
              zoom=(1.0, 1.6, 1060, 500))),
        L_("और फिर से रिक्शा लेकर निकल पड़ता।", "AUR PHIR SE RIKSHA LEKAR NIKAL PADTA",
           sc("dusk", rick=dict(drive=(400, 2100), move=1.2, thread=1.0))),
        L_("एक साल फिर बीता।", "EK SAAL PHIR BEETA", sc("roomday", fx=[("calendar", 335, 345)], zoom=(1.0, 1.3, 335, 400))),
        L_("और फिर से रिजल्ट का दिन आया।", "AUR PHIR SE RESULT KA DIN AAYA",
           sc("roomday", cast=[C("gudiya", 1100, "namaste", s=0.56, mood="sleep")], fx=[("glow", 1540, 380, 300, GOLDEN)])),
    ]},
    {"key": "result", "title": "RESULT", "lines": [
        L_("गुड़िया के हाथ कांप रहे थे।", "GUDIYA KE HAATH KAANP RAHE THE",
           sc("roomday", cast=[C("gudiya", 960, "phone", s=0.6, mood="neutral", shake=1.0, look=(0.0, 0.6))],
              zoom=(1.0, 1.4, 960, 560))),
        L_("उसने धीरे से फोन खोला।", "USNE DHEERE SE PHONE KHOLA",
           sc("roomday", cast=[C("gudiya", 600, "phone", s=0.56)], fx=[("phone", 1260, 520, "wait")], sfx="tick")),
        L_("और लिस्ट में सबसे ऊपर उसका नाम था।", "AUR LIST MEIN SABSE UPAR USKA NAAM THA",
           sc("roomday", cast=[C("gudiya", 600, "phone", s=0.56, mood="shock")], fx=[("phone", 1260, 520, "top")],
              sfx="shimmer")),
        L_("गुड़िया ज़ोर से बोली पापा।", "GUDIYA ZOR SE BOLI PAPA",
           sc("roomday", cast=[C("gudiya", 960, "joy", s=0.58, mood="joy")], fx=[("petals", 0.8)])),
        L_("शंभू रिक्शा छोड़ कर दौड़ा आया।", "SHAMBHU RIKSHA CHHOD KAR DAUDA AAYA",
           sc("street", cast=[C("shambhu", 1500, "run", s=0.58, mood="shock", enter=(400, 2.0), thread=1.0)],
              rick=dict(x=260, rider=False), sfx="whoosh")),
        L_("वही रिश्तेदार आज मिठाई लेकर दरवाज़े पर खड़े थे।", "WAHI RISHTEDAAR AAJ MITHAAI LEKAR DARWAAZE PAR KHADE THE",
           sc("roomday", cast=[C("gudiya", 420, "stand", s=0.56, mood="joy")], fx=[("_rel_sweets", 1000)])),
        L_("पर शंभू को बस एक इंसान की तलाश थी।", "PAR SHAMBHU KO BAS EK INSAAN KI TALAASH THI",
           sc("dusk", cast=[C("shambhu", 960, "stand", s=0.6, mood="neutral", look=(math.sin(1.0), -0.2), thread=1.0)],
              zoom=(1.0, 1.3, 960, 500))),
        L_("वो बूढ़े बाबा।", "WO BOODHE BAABA",
           sc("dusk", cast=[C("baba", 960, "stand", s=0.6, appear=(0.0, 0.4), divine=0.8)], fx=[("vignette", 0.6)])),
    ]},
    {"key": "raaz", "title": "LAAL DHAAGE KA RAAZ", "lines": [
        L_("शंभू पूरे शहर में घूमा।", "SHAMBHU POORE SHAHAR MEIN GHOOMA",
           sc("street", cast=[C("shambhu", 1700, "stand", s=0.58, mood="neutral", look=(0.6, 0.0), enter=(200, 4.0), thread=1.0)])),
        L_("उसी रात वाले रास्ते पर गया।", "USI RAAT WAALE RAASTE PAR GAYA",
           sc("night", cast=[C("shambhu", 900, "stand", s=0.58, mood="sad", look=(0.6, -0.2), thread=1.0)],
              fx=[("glow", 1310, 460, 200, hexc("#FFD08A"))])),
        L_("किसी ने उन बाबा को कभी नहीं देखा था।", "KISI NE UN BAABA KO KABHI NAHIN DEKHA THA",
           sc("night", cast=[C("shambhu", 600, "talk", s=0.58, mood="sad", thread=1.0)], fx=[("_rel_no", 1100)])),
        L_("थक कर वो उसी मंदिर पहुंचा।", "THAK KAR WO USI MANDIR PAHUNCHA",
           sc("temple", cast=[C("shambhu", 760, "wipe", s=0.56, mood="tired", enter=(-200, 3.0), thread=1.0)])),
        L_("और हनुमान जी की मूर्ति के सामने रुक गया।", "AUR HANUMAN JI KI MOORTI KE SAAMNE RUK GAYA",
           sc("temple", cast=[C("shambhu", 600, "namaste", s=0.56, look=(0.8, -0.4), thread=1.0)], zoom=(1.0, 1.3, 900, 650))),
        L_("मूर्ति की कलाई पर वही लाल धागा बंधा था।", "MOORTI KI KALAAI PAR WAHI LAAL DHAAGA BANDHA THA",
           sc("temple", bgkw=dict(thread=1.0), zoom=(1.0, 3.2, MURTI_WRIST[0], MURTI_WRIST[1]), sfx="shimmer")),
        L_("उसने अपनी कलाई देखी तो वो खाली थी।", "USNE APNI KALAAI DEKHI TO WO KHAALI THI",
           sc("temple", bgkw=dict(thread=1.0), cast=[C("shambhu", 960, "show", s=0.62, mood="shock", look=(0.6, -0.6))],
              zoom=(1.0, 1.5, 1070, 520))),
        L_("तभी मूर्ति से एक सुनहरी रोशनी निकली।", "TABHI MOORTI SE EK SUNEHRI ROSHNI NIKLI",
           sc("temple", bgkw=dict(thread=1.0, light=1.0), cast=[C("shambhu", 500, "namaste", s=0.56, mood="shock")],
              fx=[("rays", 960, 680)], sfx="zap")),
        L_("हनुमान जी मुस्कुरा रहे थे।", "HANUMAN JI MUSKURA RAHE THE",
           sc("temple", bgkw=dict(thread=1.0, light=1.0, murti=False),
              cast=[C("hanuman", 1200, "abhaya", s=0.62, thread=1.0), C("shambhu", 520, "namaste", s=0.56, mood="cry")],
              fx=[("petals", 0.6)], sfx="shimmer")),
        L_("जैसे कह रहे हों मेहनत तुम्हारी थी।", "JAISE KEH RAHE HON MEHNAT TUMHAARI THI",
           sc("temple", bgkw=dict(light=1.0, murti=False), cast=[C("hanuman", 960, "abhaya", s=0.64, thread=1.0)],
              fx=[("glow", 960, 520, 420, GOLDEN)], zoom=(1.0, 1.2, 960, 520))),
        L_("मैं तो बस साथ था।", "MAIN TO BAS SAATH THA",
           sc("temple", bgkw=dict(light=1.0, murti=False),
              cast=[C("hanuman", 1200, "abhaya", s=0.62, thread=1.0), C("shambhu", 600, "kneel", s=0.56, mood="cry", look=(0.8, -0.6))],
              fx=[("petals", 0.8)])),
        L_("शंभू वहीं सीढ़ियों पर बैठ कर रो पड़ा।", "SHAMBHU WAHIN SEEDHIYON PAR BAITH KAR RO PADA",
           sc("temple", bgkw=dict(thread=1.0, light=0.5),
              cast=[C("shambhu", 860, "cry", s=0.58, y=GROUND - 40), C("gudiya", 1250, "hug", s=0.56, flip=True,
                                                                          mood="joy", appear=(0.3, 0.6))])),
        L_("उस दिन उसे समझ आया कि उसकी मदद करने खुद हनुमान जी आए थे।",
           "US DIN USE SAMAJH AAYA KI USKI MADAD KARNE KHUD HANUMAN JI AAYE THE",
           sc("temple", bgkw=dict(thread=1.0, light=1.0), cast=[C("shambhu", 520, "namaste", s=0.56, mood="smile"),
                                                                C("gudiya", 1400, "namaste", s=0.54, flip=True, mood="smile")],
              fx=[("petals",)], zoom=(1.0, 1.25, 960, 600))),
    ]},
    {"key": "ask", "title": "JAI BAJRANGBALI", "lines": [
        L_("अगर आपको भी हनुमान जी पर भरोसा है तो कमेंट में जय बजरंगबली लिखो।",
           "AGAR AAPKO BHI HANUMAN JI PAR BHAROSA HAI TO COMMENT MEIN JAI BAJRANGBALI LIKHO",
           sc("temple", bgkw=dict(light=1.0, murti=False), fx=[("hanuman_light", 960, 0.64, 1.0), ("petals",)])),
        L_("और ऐसी ही कहानियों के लिए दिव्य रहस्य से जुड़े रहो।", "AUR AISI HI KAHANIYON KE LIYE DIVYA RAHASYA SE JUDE RAHO",
           sc("temple", bgkw=dict(light=1.0, murti=False), cast=[C("shambhu", 420, "namaste", s=0.54, mood="smile"),
                                                                 C("gudiya", 1500, "namaste", s=0.52, flip=True, mood="smile")],
              fx=[("hanuman_light", 960, 0.62, 1.0), ("petals",)])),
    ]},
]


def _extra_effect(ctx, S, kind, *p):
    if kind == "_rel":
        relatives(ctx, p[0], S.T, n=3, laugh=1.0)
    elif kind == "_rel_sweets":
        relatives(ctx, p[0], S.T, n=3, laugh=0.3, sweets=True, point=False)
    elif kind == "_rel_no":
        for k in range(3):
            x = p[0] + 200 * k
            dv.silhouette(ctx, lambda x=x: papa(ctx, x, GROUND, 0.56, S.T, flip=True), c=hexc("#14101A"))
    elif kind == "_leap":                                           # Hanuman ji's arc over the ocean
        u = S.u
        x = lerp(200, 1750, u)
        y = 760 - 300 * math.sin(math.pi * u)
        glow(ctx, x, y - 200, 260, GOLDEN, 0.5)
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(-0.5 + u)
        pm.hanuman(ctx, 0, 0, 0.42, S.T, pose="gada", aura=True)
        ctx.restore()
        for k in range(10):
            uu = max(0.0, u - k * 0.02)
            circle(ctx, lerp(200, 1750, uu), 760 - 300 * math.sin(math.pi * uu) - 160, 10 - k * 0.8, GOLD_HI, 0.5 - k * 0.04)


_base_effect = effect


def effect(ctx, S, kind, *p):  # noqa: F811
    if kind.startswith("_"):
        return _extra_effect(ctx, S, kind, *p)
    return _base_effect(ctx, S, kind, *p)


SOURCES = [
    "Original fictional story (Kalpanik prerak katha) - no real person or event; labelled in the description.",
    "Hanuman ji's leap over the ocean to Lanka - Valmiki Ramayana, Sundara Kanda (sarga 1).",
    "'Sankat kate mite sab peera' - Hanuman Chalisa (Goswami Tulsidas), chaupai 36.",
    "Bhagwan helping a devotee in the form of an old stranger is a common motif of bhakti folk stories.",
]

UPLOAD = {
    "title": "रिक्शा वाले की बेटी डॉक्टर बनी... पर वो बूढ़े बाबा कौन थे?",
    "description": """
Hanuman ji ke ek aise bhakt ki kahani jiski madad karne khud Hanuman ji aaye. Ek garib rickshaw wala Shambhu, jiski
beti Gudiya doctor banna chahti thi. Rishtedaar hanse, pehli baar haar mili, paise khatam... aur phir ek baarish ki
raat ek budhe baba uske rickshaw mein baithe. "Jo darta hai wo haarta hai... Bajrangi tere saath hai."

Mehnat aur Hanuman ji par bharose ki prerak katha. Kalpanik prerak katha.

Aapne budhe baba ko kab pehchana? Comment mein batayein aur JAI BAJRANGBALI zaroor likhein.
""",
    "hashtags": "#Hanuman #JaiBajrangbali #HanumanJi #PrerakKatha #DivyaRahasya",
    "tags": ["hanuman ji ki kahani", "jai bajrangbali", "hanuman story hindi", "rickshaw wale ki beti doctor",
             "motivational story hindi", "emotional story hindi", "bhagwan ki kahani", "hanuman chalisa",
             "prerak katha", "divya rahasya", "hanuman ji ka chamatkar", "beti doctor bani", "bhakti story",
             "kalpanik prerak katha"],
    "pinned": "Aapne budhe baba ko kab pehchana - baarish wali raat ya laal dhaage par? 🙏 Comment mein likho aur "
              "JAI BAJRANGBALI zaroor likho. Agar aap bhi kisi sapne ke liye mehnat kar rahe ho to wo bhi likho - "
              "hum sab milke Hanuman ji se aapke liye prarthana karenge.",
}


def thumbnail(ctx):
    """Rainy night: old baba in the rickshaw, Hanuman ji's golden shadow with gada behind, Shambhu looking back."""
    T = 1.3
    bg_street(ctx, T, "rain")
    glow(ctx, 1380, 520, 520, GOLDEN, 0.55)
    pm.hanuman(ctx, 1380, GROUND - 40, 0.9, T, pose="abhaya", aura=True, a=0.55)
    rickshaw(ctx, 820, GROUND + 40, 0.66, T, wet=1.0,
             passenger=lambda c: baba(c, -260, -150, 0.66, T, pose="stand", seated=True))
    rain(ctx, T, 0.8)
    g = cairo.LinearGradient(0, 0, 0, 320)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.8)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g)
    ctx.paint()
    text(ctx, "WO BUDHA BABA KAUN THA?", W / 2, 150, 120, hexc("#FFD84A"), font="Impact", stroke=(0.15, 0, 0),
         stroke_w=12)
