"""Divya Rahasya long-form (16:9, ~6 min): Arjun ke Rath ka Poora Rahasya.

Expands the channel's best Short (Arjun rath, 2,127 views) into the whole life of the chariot:
the burning (hook) -> Agni's gift at Khandav -> Hanuman's promise to Bhim -> Krishna becomes sarathi at Dwarka ->
Gita on the chariot -> the weapons it absorbed (Bhishma, Bhagadatta's Vaishnav astra, Drona, Karna) ->
day 18: Arjun dismounts first, the chariot burns, Krishna explains -> comment ask.

Divya Rahasya rules: only subtitles on screen (CHROME False), Roman captions, characters act out every line,
character scale 0.56-0.62 in this 16:9 frame (crown top >= y 380, feet at y 960, captions at y 1028).

    python make_long.py arjun_rath_katha --kiki-export | --preview | (render)
"""

import math

import cairo

import core.devta as dv
from core.devta import ell, gem, hand, ink, limb, sheen, smooth, eye, group, place, halo
from core.engine import circle, clamp, ease_in_out, ease_out_back, ease_out_cubic, glow, hexc, lerp, line, rgba, \
    rnd, rrect, text
from core.longform import H, W
from kathas import abhimanyu as ab, arjun_rath as ar, ghatotkach_akshauhini as ga, panchmukhi as pm

TITLE = "Arjun Ke Rath Ka Poora Rahasya"
CHROME = False
MUSIC_STYLE = "divine"
MUSIC_BPM = 82
MUSIC_SEED = 1811
MUSIC_LO, MUSIC_HI = 0.07, 0.16
KIKI_TEMPO = 1.0

GROUND = 960
GOLD, GOLD_HI = dv.GOLD, dv.GOLD_HI
WHITE = (1, 1, 1)
FIRE_O, FIRE_Y, FIRE_R = hexc("#FF5A10"), hexc("#FFD040"), hexc("#D81B1B")
SAFF = hexc("#FF8C1A")
BLUE_GLOW = hexc("#8FD3FF")

HOT = {"KRISHNA": GOLD_HI, "ARJUN": GOLD_HI, "HANUMAN": SAFF, "RATH": GOLD_HI, "AAG": FIRE_O, "RAAKH": FIRE_O,
       "AGNI": FIRE_O, "GANDIV": GOLD_HI, "BHEEM": SAFF, "DURYODHAN": FIRE_R, "KARNA": GOLD_HI, "DRON": GOLD_HI,
       "BHISHMA": GOLD_HI, "GEETA": GOLD_HI, "18": GOLD_HI, "JAI": SAFF, "SHRI": SAFF, "VAAH": GOLD_HI,
       "NARAYANI": GOLD_HI, "MAALA": GOLD_HI, "BHAGDATT": FIRE_R, "KHANDAV": FIRE_O, "DWARKA": GOLD_HI,
       "VIRAT": GOLD_HI, "PEHLE": GOLD_HI}


# ============================================================ backgrounds (16:9, layered depth)

def sky(ctx, stops):
    g = cairo.LinearGradient(0, 0, 0, H)
    for k, c in stops:
        g.add_color_stop_rgb(k, *c)
    ctx.set_source(g)
    ctx.paint()


def hills(ctx, base, amp, seed, c, n=14, T=0.0, drift=0.0):
    ctx.move_to(-50, H)
    for i in range(n + 3):
        x = -100 + i * (W + 200) / n - (T * drift) % ((W + 200) / n)
        y = base - amp * (0.55 + 0.45 * math.sin(i * 1.3 + seed)) * (0.7 + 0.3 * rnd(i, seed))
        ctx.line_to(x, y)
    ctx.line_to(W + 50, H)
    ctx.close_path()
    rgba(ctx, c)
    ctx.fill()


def dust(ctx, T, c=(1, 0.85, 0.6), n=50, a=0.35):
    for i in range(n):
        x = (rnd(i, 1) * W + T * (10 + 25 * rnd(i, 2))) % W
        y = (rnd(i, 3) * H * 0.9 - T * (8 + 20 * rnd(i, 4))) % (H * 0.9)
        circle(ctx, x, y, 1.5 + 3 * rnd(i, 5), c, a * (0.3 + 0.7 * rnd(i, 6)))


def tree(ctx, x, y, s, c=hexc("#1E4A2A"), trunk=hexc("#3A2616")):
    rgba(ctx, trunk)
    ctx.rectangle(x - 10 * s, y - 120 * s, 20 * s, 120 * s)
    ctx.fill()
    for dx, dy, r in ((0, -190, 85), (-60, -150, 62), (60, -150, 62), (0, -250, 58)):
        circle(ctx, x + dx * s, y + dy * s, r * s, c)


def bg_dusk(ctx, T, smoke=1.0):
    """Kurukshetra at the end of the war: crimson-amber sky, low sun, hills, flags, broken wheels, drifting embers."""
    sky(ctx, [(0, hexc("#2A0F2E")), (0.35, hexc("#7A2335")), (0.62, hexc("#D2602A")), (1, hexc("#F2A54A"))])
    glow(ctx, 1450, 600, 420, hexc("#FFD27A"), 0.55)
    circle(ctx, 1450, 600, 95, hexc("#FFE2A0"), 0.95)
    hills(ctx, 690, 140, 1.2, hexc("#5A2A3A"))
    hills(ctx, 780, 90, 2.7, hexc("#3E1C2A"))
    rgba(ctx, hexc("#4A2A1E"))
    ctx.rectangle(0, 860, W, H - 860)
    ctx.fill()
    g = cairo.LinearGradient(0, 860, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.45)
    ctx.set_source(g)
    ctx.rectangle(0, 860, W, H - 860)
    ctx.fill()
    for i, x in enumerate((140, 380, 1650, 1820)):          # fallen flags and a broken wheel
        line(ctx, [(x, 900), (x + 40 - 80 * (i % 2), 760)], hexc("#2A1810"), 6)
        ctx.move_to(x + 40 - 80 * (i % 2), 760)
        ctx.line_to(x + 40 - 80 * (i % 2) + 60, 775 + 6 * math.sin(T * 2 + i))
        ctx.line_to(x + 40 - 80 * (i % 2), 795)
        rgba(ctx, hexc("#8A2A1A"), 0.8)
        ctx.fill()
    ctx.arc(260, 930, 46, math.pi, 2 * math.pi)
    rgba(ctx, hexc("#2A1810"))
    ctx.set_line_width(7)
    ctx.stroke()
    for k in range(6):
        ang = math.pi + k * math.pi / 5
        line(ctx, [(260, 930), (260 + 46 * math.cos(ang), 930 + 46 * math.sin(ang))], hexc("#2A1810"), 4)
    if smoke:
        for i in range(8):
            x = (i * 260 + T * 12) % (W + 300) - 150
            circle(ctx, x, 640 - 30 * math.sin(i), 120, hexc("#2A1A22"), 0.18 * smoke)
    dust(ctx, T, (1, 0.7, 0.4), 40, 0.4)


def bg_night(ctx, T):
    sky(ctx, [(0, hexc("#050818")), (0.5, hexc("#141E3E")), (1, hexc("#2A2A48"))])
    for i in range(90):
        circle(ctx, rnd(i, 1) * W, rnd(i, 2) * 600, 1 + 1.6 * rnd(i, 3), WHITE, 0.25 + 0.5 * rnd(i, 4))
    glow(ctx, 380, 220, 220, hexc("#DDE6FF"), 0.35)
    circle(ctx, 380, 220, 60, hexc("#F2F0E6"))
    hills(ctx, 720, 130, 3.1, hexc("#1C2238"))
    hills(ctx, 800, 80, 4.4, hexc("#141A2C"))
    rgba(ctx, hexc("#1E1A22"))
    ctx.rectangle(0, 860, W, H - 860)
    ctx.fill()
    dust(ctx, T, (0.8, 0.85, 1), 30, 0.25)


def bg_yamuna(ctx, T):
    """Yamuna bank by the Khandav forest: soft morning sky, sun, river, layered forest."""
    sky(ctx, [(0, hexc("#5FA8D8")), (0.55, hexc("#BFE3F0")), (1, hexc("#F6E7C1"))])
    glow(ctx, 1500, 260, 300, hexc("#FFF2B0"), 0.6)
    circle(ctx, 1500, 260, 70, hexc("#FFF6D0"))
    hills(ctx, 640, 120, 0.7, hexc("#6E9C7A"))
    for i in range(16):
        tree(ctx, i * 130 + 30 * rnd(i, 1), 700, 0.9 + 0.3 * rnd(i, 2), hexc("#2F6B3E"))
    rgba(ctx, hexc("#3A7FB0"))
    ctx.rectangle(0, 700, W, 70)
    ctx.fill()
    for i in range(30):
        x = (i * 80 + T * 30) % W
        line(ctx, [(x, 720 + 20 * rnd(i, 3)), (x + 40, 720 + 20 * rnd(i, 3))], WHITE, 3, 0.4)
    rgba(ctx, hexc("#C9A86A"))
    ctx.rectangle(0, 770, W, H - 770)
    ctx.fill()
    for i in range(40):
        x = rnd(i, 7) * W
        line(ctx, [(x, 900 + 60 * rnd(i, 8)), (x + 6, 880 + 60 * rnd(i, 8))], hexc("#6E8A3A"), 3)
    dust(ctx, T, (1, 1, 0.9), 25, 0.3)


def bg_forest(ctx, T):
    """Deep forest path (Bheem meets Hanuman): green light shafts, big trees, flowers on the path."""
    sky(ctx, [(0, hexc("#0F2A1E")), (0.6, hexc("#2C5A3A")), (1, hexc("#5A7A3A"))])
    for i in range(5):
        ctx.move_to(300 + i * 360, 0)
        ctx.line_to(420 + i * 360, 0)
        ctx.line_to(260 + i * 360, 900)
        ctx.line_to(160 + i * 360, 900)
        ctx.close_path()
        rgba(ctx, hexc("#FFF6C0"), 0.07)
        ctx.fill()
    for i in range(9):
        tree(ctx, i * 230 + 40, 820, 1.7, hexc("#173A24"), hexc("#2A1A10"))
    rgba(ctx, hexc("#6B5530"))
    ctx.move_to(0, 900)
    ctx.curve_to(600, 850, 1300, 860, W, 900)
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    ctx.fill()
    rgba(ctx, hexc("#2E4A22"))
    ctx.rectangle(0, 820, W, 50)
    ctx.fill()
    for i in range(30):
        circle(ctx, rnd(i, 4) * W, 840 + 30 * rnd(i, 5), 7, [hexc("#FFD84A"), hexc("#FF8AB0"), WHITE][i % 3], 0.85)
    dust(ctx, T, (1, 1, 0.8), 30, 0.3)


def bg_palace(ctx, T):
    """Dwarka palace chamber: carved pillars, arches, lamps, sea through the window."""
    sky(ctx, [(0, hexc("#3A1A12")), (0.6, hexc("#6A3A1E")), (1, hexc("#3A2010"))])
    rrect(ctx, 760, 180, 400, 420, 200)
    g = cairo.LinearGradient(0, 180, 0, 600)
    g.add_color_stop_rgb(0, *hexc("#6FB6E0"))
    g.add_color_stop_rgb(0.7, *hexc("#BFE6F5"))
    g.add_color_stop_rgb(1, *hexc("#2E7FB0"))
    ctx.set_source(g)
    ctx.fill()
    for i in range(6):
        line(ctx, [(790 + i * 60, 560 + 6 * math.sin(T + i)), (820 + i * 60, 560 + 6 * math.sin(T + i))], WHITE, 3, 0.6)
    for x in (120, 460, 1460, 1800):
        rrect(ctx, x - 45, 120, 90, 760, 10)
        rgba(ctx, hexc("#C99A4A"))
        ctx.fill()
        rgba(ctx, hexc("#8A5A20"))
        for k in range(6):
            ctx.rectangle(x - 45, 160 + k * 120, 90, 10)
        ctx.fill()
        glow(ctx, x, 330, 90, hexc("#FFC060"), 0.5)
        circle(ctx, x, 330, 14, hexc("#FFE09A"))
    rgba(ctx, hexc("#7A3A22"))
    ctx.rectangle(0, 880, W, H - 880)
    ctx.fill()
    for i in range(12):
        rgba(ctx, hexc("#9A5A2A") if i % 2 else hexc("#6A2A16"))
        ctx.rectangle(i * 160, 880, 160, 14)
        ctx.fill()
    dust(ctx, T, (1, 0.9, 0.6), 25, 0.25)


def bg_cosmos(ctx, T):
    sky(ctx, [(0, hexc("#05030F")), (0.5, hexc("#1A0F3A")), (1, hexc("#2A1240"))])
    for i in range(160):
        circle(ctx, rnd(i, 1) * W, rnd(i, 2) * H, 1 + 2 * rnd(i, 3), WHITE, 0.3 + 0.6 * rnd(i, 4))
    for k in range(3):
        glow(ctx, 400 + k * 600, 300 + 200 * math.sin(k), 380, [hexc("#7A3AFF"), hexc("#FF5AA0"), hexc("#3AB0FF")][k],
             0.18)


BGS = {"dusk": bg_dusk, "night": bg_night, "yamuna": bg_yamuna, "forest": bg_forest, "palace": bg_palace,
       "cosmos": bg_cosmos}


# ============================================================ new characters

BHEEM_SKIN = hexc("#C98B5E")
BHEEM_ARMOR = hexc("#2F6B3A")


def bheem(ctx, x, y, s, t, pose="stand", look=(0.0, 0.0), flip=False, a=1.0, strain=0.0):
    """Bheem: broad shoulders, green-and-gold armour, simple mukut, big gada. Poses stand / angry (points
    screen-right) / push (both hands down on the tail, straining) / namaste."""
    def draw():
        place(ctx, x, y, s, t, flip)
        _bheem_body(ctx, t, pose, look, strain)
        ctx.restore()
    group(ctx, a, draw)


def _bheem_body(ctx, t, pose, look, strain):
    skin, hair = BHEEM_SKIN, dv.HAIR
    shake = 4 * math.sin(t * 40) * strain
    ctx.translate(shake, 0)
    ell(ctx, 0, -680, 120, 112)
    ink(ctx, hair)
    for side in (-1, 1):
        limb(ctx, [(side * 62, -340), (side * 70, -170), (side * 70, -34)], skin, 58)
        ell(ctx, side * 76, -14, 46, 17)
        ink(ctx, skin)
    smooth(ctx, [(-140, -360), (140, -360), (156, -230), (120, -150), (0, -170), (-120, -150), (-156, -230)])
    ink(ctx, hexc("#E8C25A"))
    line(ctx, [(150, -228), (120, -156), (0, -176), (-120, -156), (-150, -228)], dv.GOLD, 10)
    smooth(ctx, [(-160, -525), (-84, -556), (84, -556), (160, -525), (160, -440), (120, -350), (-120, -350),
                 (-160, -440)])
    ink(ctx, BHEEM_ARMOR)
    smooth(ctx, [(-100, -515), (100, -515), (94, -420), (0, -384), (-94, -420)])
    ink(ctx, dv.GOLD, 5)
    sheen(ctx, -34, -470, 52, 26, 0.2)
    gem(ctx, 0, -455, 16, dv.GREEN_GEM)
    rrect(ctx, -128, -374, 256, 32, 10)
    ink(ctx, dv.GOLD)
    L, R = (-160, -515), (160, -515)
    if pose == "push":
        arms = [(L, (-150, -360), (-60, -250)), (R, (150, -360), (60, -250))]
    elif pose == "angry":
        arms = [(L, (-205, -420), (-200, -320)), (R, (260, -565), (370, -600))]
    elif pose == "namaste":
        arms = [(L, (-170, -400), (-16, -470)), (R, (170, -400), (16, -470))]
    else:
        arms = [(L, (-205, -420), (-200, -320)), (R, (215, -420), (150, -330))]
    if pose not in ("push", "namaste"):
        ga.gada(ctx, -200, -320, -215, -720, 60)
    for sh, el, hd in arms:
        limb(ctx, [sh, el], skin, 60)
        limb(ctx, [el, hd], skin, 50)
        circle(ctx, lerp(sh[0], el[0], 0.5), lerp(sh[1], el[1], 0.5), 30, dv.GOLD)
        circle(ctx, lerp(sh[0], el[0], 0.5), lerp(sh[1], el[1], 0.5), 22, skin)
    for side in (-1, 1):
        ell(ctx, side * 160, -520, 46, 32)
        ink(ctx, BHEEM_ARMOR)
    for sh, el, hd in arms:
        hand(ctx, hd[0], hd[1], skin, 30)
    rrect(ctx, -34, -600, 68, 70, 14)
    ink(ctx, skin)
    ell(ctx, 0, -690, 100, 106)
    ink(ctx, skin)
    sheen(ctx, -34, -740, 36, 20, 0.18)
    brow = 12 if pose in ("angry", "push") else 0
    for side in (-1, 1):
        line(ctx, [(side * 70, -742 - (0 if brow else 6)), (side * 22, -736 + brow)], hair, 11)
        eye(ctx, side * 38, -702, 23, 24, t, look=look, seed=9)
    ell(ctx, 0, -668, 12, 17)
    ink(ctx, dv.shade(skin, 0.88), 3.5)
    smooth(ctx, [(-46, -642), (0, -652), (46, -642), (30, -632), (0, -638), (-30, -632)], k=0.1)
    ink(ctx, hair, 3)
    if pose == "push":
        rrect(ctx, -20, -622, 40, 10, 5)
        ink(ctx, dv.OUTLINE, 3)
    else:
        line(ctx, [(-22, -614), (0, -606 if pose != "angry" else -620), (22, -614)], dv.OUTLINE, 6)
    for side in (-1, 1):
        ell(ctx, side * 100, -680, 16, 26)
        ink(ctx, skin)
    smooth(ctx, [(-100, -778), (-70, -840), (0, -880), (70, -840), (100, -778)], k=0.08)
    ink(ctx, dv.GOLD, 5)
    rrect(ctx, -104, -790, 208, 34, 10)
    ink(ctx, dv.GOLD, 5)
    gem(ctx, 0, -830, 13, dv.GREEN_GEM)


def agni_aura(ctx, x, y, s, t, k):
    """Agni dev's true form shown as a roaring flame body around the brahmin disguise (k 0..1)."""
    if k <= 0:
        return
    glow(ctx, x, y - 420 * s, 520 * s * k, FIRE_O, 0.55 * k)
    for i in range(18):
        ang = -math.pi / 2 + (i - 8.5) * 0.17
        L = (620 + 260 * math.cos((i - 8.5) / 8.5 * 1.4) + 120 * math.sin(t * 7 + i)) * s * k
        bx, by = x + (i - 8.5) * 46 * s, y - 60 * s
        ctx.move_to(bx - 22 * s, by)
        ctx.curve_to(bx - 10 * s, by - L * 0.5, bx + 20 * s * math.sin(t * 5 + i), by - L,
                     bx + 20 * s * math.sin(t * 5 + i), by - L)
        ctx.curve_to(bx + 20 * s * math.sin(t * 5 + i), by - L, bx + 12 * s, by - L * 0.5, bx + 22 * s, by)
        ctx.close_path()
        rgba(ctx, FIRE_R if i % 3 == 0 else FIRE_O, 0.55 * k)
        ctx.fill()


def tail(ctx, x0, y0, x1, y1, t, lift=0.0, a=1.0):
    """Hanuman's long tail lying across the path (lift > 0 = Bheem tugging, it barely moves)."""
    wob = 4 * math.sin(t * 30) * lift
    ctx.move_to(x0, y0)
    ctx.curve_to(lerp(x0, x1, 0.33), y0 + 30 + wob, lerp(x0, x1, 0.66), y1 + 20 - wob, x1, y1 - 40)
    rgba(ctx, dv.OUTLINE, a)
    ctx.set_line_width(34)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.stroke_preserve()
    rgba(ctx, pm.HANUMAN_ORANGE if hasattr(pm, "HANUMAN_ORANGE") else SAFF, a)
    ctx.set_line_width(24)
    ctx.stroke()
    circle(ctx, x1, y1 - 40, 20, hexc("#7A3A1A"), a)


def horse(ctx, x, y, s, t, run=0.0, a=1.0):
    """White chariot horse, side view facing right; run (0..1) animates a gallop."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)
        ph = t * 9
        bob = 6 * math.sin(ph * 2) * run
        ctx.translate(0, -bob)
        body, edge = hexc("#F4F1EA"), dv.OUTLINE
        for k, (hx, front) in enumerate(((-70, False), (-40, False), (70, True), (100, True))):
            sw = math.sin(ph + k * 1.6) * run
            kx = hx + 30 * sw
            limb(ctx, [(hx, -150), (hx + 10 * sw, -80), (kx, 0)], dv.shade(body, 0.86 if k in (1, 3) else 1), 20)
            ell(ctx, kx + 4, 2, 14, 8)
            ink(ctx, hexc("#3A2A20"))
        ell(ctx, 10, -175, 125, 58)
        ink(ctx, body)
        sheen(ctx, -10, -200, 60, 18, 0.25)
        smooth(ctx, [(95, -205), (140, -290), (175, -320), (215, -300), (205, -275), (165, -262), (140, -180)])
        ink(ctx, body)
        ell(ctx, 205, -290, 34, 22, 0.4)
        ink(ctx, body)
        circle(ctx, 196, -302, 5, (0.05, 0.05, 0.05))
        for i in range(6):                                   # mane
            smooth(ctx, [(120 + i * 10, -230 - i * 14), (100 + i * 10, -215 - i * 14), (110 + i * 10, -245 - i * 14)])
            ink(ctx, hexc("#D9D2C2"), 2)
        ctx.move_to(-110, -190)                              # tail
        ctx.curve_to(-170, -180 + 10 * math.sin(ph), -180, -120, -160, -90)
        rgba(ctx, hexc("#D9D2C2"))
        ctx.set_line_width(16)
        ctx.stroke()
        rrect(ctx, -40, -235, 90, 22, 8)                      # gold harness
        ink(ctx, dv.GOLD, 3)
        ctx.restore()
    group(ctx, a, draw)


def rath(ctx, x, y, s, t, burn=0.0, run=0.0, horses=True, han=1.0, han_fly=0.0, krishna=None, arjun=None,
         appear=1.0, garland=0.0):
    """The Kapidhwaj chariot, side view facing right: big wheel, carved deck, canopy, Hanuman on the dhwaj,
    four white horses. krishna / arjun = pose name to stand them on the deck (None = not on it)."""
    alive = clamp(1 - burn * 1.25) * appear
    if alive <= 0.02 and burn <= 0:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if appear < 1:
        glow(ctx, 0, -350, 600 * appear, GOLD_HI, 0.5 * (1 - appear) + 0.2)
    if alive > 0.02:
        ctx.push_group()
        if horses:
            for i, (hx, hs) in enumerate(((560, 0.95), (420, 0.95), (620, 1.0), (480, 1.0))):
                horse(ctx, hx, 0, hs, t + i * 0.37, run)
        spin = t * 6 * run
        for wx in (-60,):
            circle(ctx, wx, -125, 125, dv.OUTLINE)
            circle(ctx, wx, -125, 115, GOLD)
            circle(ctx, wx, -125, 95, hexc("#5A2008"))
            for k in range(12):
                ang = spin + k * math.pi / 6
                line(ctx, [(wx + 22 * math.cos(ang), -125 + 22 * math.sin(ang)),
                           (wx + 92 * math.cos(ang), -125 + 92 * math.sin(ang))], GOLD, 7)
            circle(ctx, wx, -125, 26, GOLD_HI)
        line(ctx, [(200, -200), (420, -190)], hexc("#6A3A12"), 14)       # yoke pole
        smooth(ctx, [(-300, -210), (230, -210), (260, -270), (230, -300), (-280, -300), (-320, -260)], k=0.1)
        ink(ctx, GOLD, 6)
        rrect(ctx, -270, -290, 480, 46, 10)
        ink(ctx, hexc("#E8A020"), 4)
        for k in range(6):
            gem(ctx, -230 + k * 85, -267, 10, dv.RED_GEM if k % 2 else dv.GREEN_GEM)
        for px in (-270, 190):
            line(ctx, [(px, -300), (px, -700)], GOLD, 12)
        smooth(ctx, [(-310, -690), (230, -690), (160, -780), (-40, -820), (-240, -780)], k=0.12)
        ink(ctx, GOLD, 5)
        gem(ctx, -40, -750, 16, dv.RED_GEM)
        line(ctx, [(-40, -820), (-40, -1090)], GOLD, 8)                   # dhwaj
        wave = 14 * math.sin(t * 4.5)
        ctx.move_to(-40, -1080)
        ctx.curve_to(40, -1070 + wave, 110, -1050 - wave, 170 + wave, -1030)
        ctx.line_to(-40, -980)
        ctx.close_path()
        rgba(ctx, hexc("#FF6A1A"))
        ctx.fill()
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(alive)
        if han > 0 and han_fly < 1:                                     # Hanuman seated on the flag
            hy = -1090 - 900 * ease_in_out(han_fly)
            pm.hanuman(ctx, -40, hy, 0.22, t, pose="gada" if han_fly <= 0 else "namaste",
                       a=alive * han * (1 - han_fly))
        if arjun:
            ar.arjuna(ctx, -150, -300, 0.4, t, pose=arjun, a=alive)
        if krishna:
            ar.krishna(ctx, 80, -300, 0.4, t, pose=krishna, a=alive)
            if garland > 0:
                garland_on(ctx, 80, -300, 0.4, t, garland)
            if horses:                                                   # reins to the horses
                for hx in (600, 660):
                    line(ctx, [(80 + 60, -300 - 0.4 * 450), (hx + 190, -290)], hexc("#3A2010"), 3, 0.8 * alive)
    if burn > 0.02:
        fire(ctx, 0, -60, 640, 760, t, burn)
    ctx.restore()


def fire(ctx, x, y, w, h, t, k):
    glow(ctx, x, y - h * 0.4, w * 0.9 * (0.6 + k * 0.6), FIRE_O, 0.7 * min(1, k * 1.5))
    for i in range(22):
        fx = x - w / 2 + i * w / 21
        L = (0.45 + 0.55 * abs(math.sin(i * 1.7 + t * 8))) * h * clamp(k * 1.4, 0.15, 1.1)
        c = 30 * math.sin(t * 7 + i)
        for (wd, col, kk) in ((32, FIRE_R if i % 3 == 0 else FIRE_O, 1.0), (16, FIRE_Y, 0.7)):
            ctx.move_to(fx - wd, y)
            ctx.curve_to(fx - wd * 0.6, y - L * kk * 0.6, fx + c, y - L * kk, fx + c, y - L * kk)
            ctx.curve_to(fx + c, y - L * kk, fx + wd * 0.6, y - L * kk * 0.6, fx + wd, y)
            ctx.close_path()
            rgba(ctx, col, 0.8)
            ctx.fill()
    for i in range(10):
        sx = x - w * 0.3 + i * w * 0.06 + 20 * math.sin(t * 2 + i)
        sy = y - h * 0.8 - (t * 90 + i * 40) % 300
        circle(ctx, sx, sy, 60 + 20 * math.sin(i + t), hexc("#1A1218"), 0.35 * min(1, k))
    if k > 0.55:
        ell(ctx, x, y + 10, w * 0.45 * k, 40 * k)
        rgba(ctx, hexc("#2B2D42"), 0.9)
        ctx.fill()
        for i in range(14):
            circle(ctx, x - w * 0.4 + i * w * 0.06, y + 4, 6, FIRE_O, 0.6 + 0.4 * math.sin(t * 6 + i))


def garland_on(ctx, x, y, s, t, k):
    """Vaijayanti mala: flowers appear one by one around Krishna's neck (feet at x, y)."""
    n = int(16 * k)
    for i in range(n):
        ang = math.pi * 0.05 + math.pi * 0.9 * i / 15
        fx = x + 120 * s * math.cos(ang)
        fy = y - 520 * s + 150 * s * math.sin(ang)
        circle(ctx, fx, fy, 14 * s * 2, [hexc("#FF5A8A"), hexc("#FFD84A"), WHITE][i % 3])
        circle(ctx, fx, fy, 5 * s * 2, GOLD)


def arrow(ctx, x0, y0, x1, y1, u, c=hexc("#E8D7A0"), glow_c=None, L=90):
    """Arrow flying from (x0, y0) to (x1, y1); the head always points along the flight."""
    if u <= 0 or u > 1.02:
        return
    u = clamp(u)
    x, y = lerp(x0, x1, u), lerp(y0, y1, u) - 60 * math.sin(math.pi * u)
    dx = (x1 - x0)
    dy = (y1 - y0) - 60 * math.pi * math.cos(math.pi * u)
    ang = math.atan2(dy, dx)
    if glow_c:
        glow(ctx, x, y, 70, glow_c, 0.6)
    tx, ty = x - L * math.cos(ang), y - L * math.sin(ang)
    line(ctx, [(tx, ty), (x, y)], c, 5)
    ctx.move_to(x + 20 * math.cos(ang), y + 20 * math.sin(ang))
    ctx.line_to(x + 12 * math.cos(ang + 2.5), y + 12 * math.sin(ang + 2.5))
    ctx.line_to(x + 12 * math.cos(ang - 2.5), y + 12 * math.sin(ang - 2.5))
    ctx.close_path()
    rgba(ctx, hexc("#C0C8D0"))
    ctx.fill()
    for sgn in (1, -1):
        line(ctx, [(tx, ty), (tx - 16 * math.cos(ang + sgn * 0.5), ty - 16 * math.sin(ang + sgn * 0.5))],
             hexc("#D04A3A"), 4)


def spark(ctx, x, y, k):
    if k <= 0:
        return
    glow(ctx, x, y, 120 * k, GOLD_HI, 0.8 * k)
    for i in range(10):
        ang = i * math.pi / 5
        line(ctx, [(x + 20 * k * math.cos(ang), y + 20 * k * math.sin(ang)),
                   (x + 80 * k * math.cos(ang), y + 80 * k * math.sin(ang))], GOLD_HI, 4, k)


# ============================================================ cast + stage

def _rig(who):
    return {"krishna": ar.krishna, "dkrishna": dv.krishna, "arjun": ar.arjuna, "hanuman": pm.hanuman,
            "duryodhan": ga.duryodhan, "karna": dv.karna, "drona": ab.drona, "brahmin": dv.brahmin, "bheem": bheem}[who]


def actor(ctx, S, who, x, pose=None, s=0.6, y=GROUND, flip=False, enter=None, fade=None, lie=False, bow=0.0,
          kw=None):
    """One character on stage. enter=(x0, seconds) walks it in; fade=(u0, u1) fades it out; lie lays it on a bed;
    bow (0..1) tips it forward to the feet (sharan)."""
    a = 1.0
    if enter:
        x = lerp(enter[0], x, ease_out_cubic(S.t / enter[1]))
    if fade:
        a = 1 - clamp((S.u - fade[0]) / max(0.01, fade[1] - fade[0]))
    kw = dict(kw or {})
    if pose:
        kw["pose"] = pose
    if flip:
        kw["flip"] = True
    ctx.save()
    if lie:
        ctx.translate(x, y)
        ctx.rotate(-math.pi / 2)
        _rig(who)(ctx, 0, 0, s, S.T, a=a, **kw)
    elif bow > 0:
        b = ease_in_out(bow)
        ctx.translate(x, y)
        ctx.rotate(0.9 * b * (-1 if flip else 1))
        _rig(who)(ctx, 0, 140 * s * b, s, S.T, a=a, **kw)
    else:
        _rig(who)(ctx, x, y, s, S.T, a=a, **kw)
    ctx.restore()


def stage(ctx, S, bg="dusk", cast=(), rath_kw=None, fx=(), zoom=None):
    """Background + optional chariot + characters + effects. zoom=(z0, z1, cx, cy) slow camera push."""
    ctx.save()
    if zoom:
        z = lerp(zoom[0], zoom[1], ease_in_out(S.u))
        ctx.translate(zoom[2], zoom[3])
        ctx.scale(z, z)
        ctx.translate(-zoom[2], -zoom[3])
    BGS[bg](ctx, S.T)
    behind = [f for f in fx if f[0] in ("forest_fire", "rain", "cosmic", "agni")]
    front = [f for f in fx if f not in behind]
    for f in behind:
        effect(ctx, S, *f)
    if rath_kw is not None:
        kw = dict(rath_kw)
        if kw.get("burn") == "ramp":
            kw["burn"] = clamp((S.u - kw.pop("burn_at", 0.15)) / 0.5)
        if kw.get("han_fly") == "ramp":
            kw["han_fly"] = clamp(S.u / 0.6)
        if kw.get("garland") == "ramp":
            kw["garland"] = clamp((S.u - 0.35) / 0.4)
        if kw.get("appear") == "ramp":
            kw["appear"] = clamp(S.u / 0.5)
        rx = kw.pop("x", 760)
        if "slide" in kw:
            sl = kw.pop("slide")
            rx -= sl * ease_out_cubic(clamp((S.u - 0.4) / 0.25))
        rath(ctx, rx, kw.pop("y", GROUND), kw.pop("s", 0.62), S.T, **kw)
    for c in cast:
        actor(ctx, S, **c)
    for f in front:
        effect(ctx, S, *f)
    ctx.restore()


def effect(ctx, S, kind, *p):
    u, T = S.u, S.T
    if kind == "forest_fire":
        for i in range(5):
            fire(ctx, 200 + i * 380, 800, 420, 520, T + i, clamp(u * 1.6))
    elif kind == "rain":
        rgba(ctx, hexc("#1A2A3A"), 0.35)
        ctx.paint()
        for i in range(5):
            circle(ctx, 200 + i * 400, 120, 200, hexc("#3A4A5A"), 0.85)
        for i in range(160):
            x = (rnd(i, 1) * W + T * 200) % W
            y = (rnd(i, 2) * H + T * 900) % H
            line(ctx, [(x, y), (x - 8, y + 30)], hexc("#BFD8F0"), 2, 0.6)
        if (T * 1.3) % 3 < 0.12:
            rgba(ctx, WHITE, 0.4)
            ctx.paint()
    elif kind == "agni":                                  # (x, s)
        agni_aura(ctx, p[0], GROUND, p[1], T, clamp((u - p[2]) / 0.3) if len(p) > 2 else 1.0)
    elif kind == "gift_bow":                              # golden Gandiv floats down to (x, y)
        k = ease_out_cubic(clamp(u / 0.6))
        x, y = p[0], lerp(200, p[1], k)
        glow(ctx, x, y, 200, GOLD_HI, 0.6)
        ctx.save()
        ctx.translate(x, y)
        ctx.arc(0, 0, 150, -1.1, 1.1)
        rgba(ctx, GOLD)
        ctx.set_line_width(14)
        ctx.stroke()
        line(ctx, [(150 * math.cos(-1.1), 150 * math.sin(-1.1)), (150 * math.cos(1.1), 150 * math.sin(1.1))],
             WHITE, 3)
        ctx.restore()
    elif kind == "gift_quiver":
        k = ease_out_cubic(clamp(u / 0.6))
        for j, x in enumerate((p[0] - 70, p[0] + 70)):
            y = lerp(150, p[1], k)
            glow(ctx, x, y, 140, GOLD_HI, 0.5)
            rrect(ctx, x - 26, y - 110, 52, 220, 20)
            ink(ctx, hexc("#8A4A1A"), 4)
            for a_ in range(5):
                line(ctx, [(x - 16 + a_ * 8, y - 110), (x - 16 + a_ * 8, y - 170)], hexc("#E8D7A0"), 4)
                circle(ctx, x - 16 + a_ * 8, y - 172, 6, hexc("#D04A3A"))
    elif kind == "arrows":                                # volley (x0, y0, x1, y1, n, glow)
        x0, y0, x1, y1, n = p[:5]
        gc = p[5] if len(p) > 5 else None
        for i in range(n):
            uu = (u * 2.2 - i * 0.12) % 1.2
            arrow(ctx, x0, y0 + 20 * (i % 3), x1 + 30 * math.sin(i), y1 + 20 * math.cos(i), uu, glow_c=gc)
            if 0.95 < uu < 1.15:
                spark(ctx, x1 + 30 * math.sin(i), y1 + 20 * math.cos(i), 1 - (uu - 0.95) / 0.2)
    elif kind == "one_arrow":                             # (x0, y0, x1, y1, u0, u1, glow)
        x0, y0, x1, y1, u0, u1 = p[:6]
        gc = p[6] if len(p) > 6 else None
        k = (u - u0) / (u1 - u0)
        arrow(ctx, x0, y0, x1, y1, k, glow_c=gc, L=120)
        if 1 < k < 1.6:
            spark(ctx, x1, y1, 1 - (k - 1) / 0.6)
    elif kind == "orb":                                   # Vaishnav astra (x0, y0, x1, y1)
        x0, y0, x1, y1 = p
        k = clamp(u / 0.35)
        if k < 1:
            x, y = lerp(x0, x1, ease_in_out(k)), lerp(y0, y1, ease_in_out(k))
            glow(ctx, x, y, 160, BLUE_GLOW, 0.8)
            circle(ctx, x, y, 34, WHITE)
            for i in range(8):
                ang = T * 8 + i * math.pi / 4
                line(ctx, [(x, y), (x + 60 * math.cos(ang), y + 60 * math.sin(ang))], BLUE_GLOW, 4)
        else:
            spark(ctx, x1, y1, clamp(1 - (u - 0.35) / 0.25))
    elif kind == "cosmic":                                # Virat roop rings behind (x, y)
        x, y = p
        for k in range(4):
            r = 260 + k * 120 + 20 * math.sin(T + k)
            ctx.save()
            ctx.translate(x, y)
            ctx.rotate(T * (0.2 + 0.1 * k) * (-1) ** k)
            ctx.arc(0, 0, r, 0, math.tau)
            rgba(ctx, GOLD_HI, 0.35)
            ctx.set_line_width(3)
            ctx.set_dash([20, 14])
            ctx.stroke()
            ctx.set_dash([])
            ctx.restore()
        glow(ctx, x, y, 700, GOLD_HI, 0.4)
    elif kind == "tail":                                  # (x0, y0, x1, y1, lift)
        tail(ctx, p[0], p[1], p[2], p[3], T, p[4] if len(p) > 4 else 0.0)
    elif kind == "glow":                                  # (x, y, r, colour)
        glow(ctx, p[0], p[1], p[2] * (0.9 + 0.1 * math.sin(T * 3)), p[3], 0.6)
    elif kind == "bed":                                   # (x, y)
        rrect(ctx, p[0] - 380, p[1] - 30, 760, 70, 16)
        rgba(ctx, hexc("#8A2A3A"))
        ctx.fill()
        rrect(ctx, p[0] - 400, p[1] + 30, 800, 40, 10)
        rgba(ctx, GOLD)
        ctx.fill()
    elif kind == "flowers":                               # petals falling
        for i in range(40):
            x = (rnd(i, 1) * W + T * 30) % W
            y = (rnd(i, 2) * H + T * (60 + 40 * rnd(i, 3))) % H
            circle(ctx, x, y, 6, [hexc("#FF8AB0"), hexc("#FFD84A")][i % 2], 0.8)
    elif kind == "bow_drop":                              # Gandiv slips to the ground at (x)
        k = ease_out_cubic(clamp(u / 0.5))
        ctx.save()
        ctx.translate(p[0], lerp(700, 940, k))
        ctx.rotate(lerp(0, 1.35, k))
        ctx.arc(0, 0, 120, -1.1, 1.1)
        rgba(ctx, GOLD)
        ctx.set_line_width(10)
        ctx.stroke()
        ctx.restore()


# ============================================================ shots

def sc(bg="dusk", cast=(), rath=None, fx=(), zoom=None):
    """Shot factory: returns (fn, params) for a stage."""
    return stage, dict(bg=bg, cast=list(cast), rath_kw=rath, fx=list(fx), zoom=zoom)


def C(who, x, pose=None, **kw):
    return dict(who=who, x=x, pose=pose, **kw)


L, R = 600, 1320          # two-character marks (~720 px apart, both clear of the edges)
RATH_ON = dict(krishna="reins", arjun="bow")


def line_(hi, roman, shot):
    fn, params = shot
    return (hi, roman, fn, params)


CHAPTERS = [
    {"key": "hook", "title": "RATH KYUN JALA", "lines": [
        line_("सोचो अठारह दिन का युद्ध अभी अभी खत्म हुआ है।", "SOCHO 18 DIN KA YUDDH ABHI ABHI KHATAM HUA HAI",
              sc("dusk", rath=dict(RATH_ON, x=640), zoom=(1.0, 1.06, 960, 600))),
        line_("पांडव जीत चुके हैं और अर्जुन का रथ शान से खड़ा है।", "PANDAV JEET CHUKE HAIN AUR ARJUN KA RATH SHAAN SE KHADA HAI",
              sc("dusk", rath=dict(krishna="stand", arjun="namaste", x=640), fx=[("flowers",)])),
        line_("तभी श्री कृष्ण धीरे से कहते हैं।", "TABHI SHRI KRISHNA DHEERE SE KEHTE HAIN",
              sc("dusk", rath=dict(krishna="command", arjun="bow", x=640), zoom=(1.0, 1.15, 760, 600))),
        line_("अर्जुन पहले तुम रथ से उतर जाओ।", "ARJUN PEHLE TUM RATH SE UTAR JAAO",
              sc("dusk", rath=dict(krishna="command", arjun="confused", x=640), zoom=(1.15, 1.2, 760, 600))),
        line_("अर्जुन हैरान रह जाता है क्योंकि हमेशा सारथी ही पहले उतरता है।",
              "ARJUN HAIRAAN REH JAATA HAI KYUNKI HAMESHA SAARTHI HI PEHLE UTARTA HAI",
              sc("dusk", rath=dict(krishna="command", arjun="shock", x=640))),
        line_("फिर भी वो चुपचाप नीचे उतर जाता है।", "PHIR BHI WOH CHUPCHAAP NEECHE UTAR JAATA HAI",
              sc("dusk", rath=dict(krishna="command", x=760), cast=[C("arjun", 320, "namaste", enter=(470, 1.2))])),
        line_("और जैसे ही कृष्ण भी नीचे उतरते हैं।", "AUR JAISE HI KRISHNA BHI NEECHE UTARTE HAIN",
              sc("dusk", rath=dict(x=760), cast=[C("arjun", 320, "namaste"), C("krishna", 1640, "stand", enter=(1250, 1.0))])),
        line_("उसी पल पूरा रथ आग पकड़ लेता है और देखते ही देखते राख बन जाता है।",
              "USI PAL POORA RATH AAG PAKAD LETA HAI AUR DEKHTE HI DEKHTE RAAKH BAN JAATA HAI",
              sc("dusk", rath=dict(x=760, burn="ramp", burn_at=0.05, han_fly="ramp"),
                 cast=[C("arjun", 320, "shock"), C("krishna", 1640, "bless")])),
        line_("ये रथ आखिर जला क्यों।", "YEH RATH AAKHIR JALA KYUN",
              sc("night", rath=dict(x=760, burn=0.95, horses=False), cast=[C("arjun", 320, "confused")])),
        line_("इसका जवाब छुपा है इस रथ की पूरी कहानी में।", "ISKA JAWAB CHHUPA HAI IS RATH KI POORI KAHANI MEIN",
              sc("cosmos", rath=dict(x=760, appear="ramp", run=0.0), fx=[("glow", 760, 600, 500, GOLD_HI)])),
        line_("तो चलो शुरू से सुनते हैं।", "TOH CHALO SHURU SE SUNTE HAIN",
              sc("cosmos", cast=[C("dkrishna", 960, "flute", s=0.62)], fx=[("cosmic", 960, 640)])),
    ]},
    {"key": "khandav", "title": "AGNI DEV KA VARDAAN", "lines": [
        line_("बहुत पहले की बात है।", "BAHUT PEHLE KI BAAT HAI", sc("yamuna", zoom=(1.08, 1.0, 960, 500))),
        line_("कृष्ण और अर्जुन यमुना किनारे घूम रहे थे।", "KRISHNA AUR ARJUN YAMUNA KINAARE GHOOM RAHE THE",
              sc("yamuna", cast=[C("dkrishna", 760, "flute", enter=(520, 3)), C("arjun", 420, "bow", enter=(180, 3))])),
        line_("तभी एक तेजस्वी ब्राह्मण उनके पास आया।", "TABHI EK TEJASVI BRAHMIN UNKE PAAS AAYA",
              sc("yamuna", cast=[C("dkrishna", 760, "bless"), C("arjun", 420, "namaste"),
                                 C("brahmin", 1360, "stand", enter=(1800, 2.2))])),
        line_("उसने कहा मुझे बहुत भूख लगी है।", "USNE KAHA MUJHE BAHUT BHOOKH LAGI HAI",
              sc("yamuna", cast=[C("dkrishna", 760, "bless"), C("arjun", 420, "namaste"), C("brahmin", 1360, "ask")])),
        line_("कृष्ण मुस्कुराए और बोले बताइए आपको क्या चाहिए।", "KRISHNA MUSKURAAYE AUR BOLE BATAAIYE AAPKO KYA CHAHIYE",
              sc("yamuna", cast=[C("dkrishna", 760, "ask"), C("arjun", 420, "namaste"), C("brahmin", 1360, "stand")])),
        line_("तब ब्राह्मण ने अपना असली रूप दिखाया।", "TAB BRAHMIN NE APNA ASLI ROOP DIKHAAYA",
              sc("yamuna", cast=[C("dkrishna", 760, "bless"), C("arjun", 420, "shock"), C("brahmin", 1360, "stand")],
                 fx=[("agni", 1360, 0.6, 0.15)])),
        line_("वो कोई और नहीं खुद अग्नि देव थे।", "WOH KOI AUR NAHI KHUD AGNI DEV THE",
              sc("yamuna", cast=[C("brahmin", 960, "stand", s=0.62)], fx=[("agni", 960, 0.7, 0.0)],
                 zoom=(1.0, 1.08, 960, 600))),
        line_("अग्नि देव खांडव वन को जलाकर अपनी भूख मिटाना चाहते थे।",
              "AGNI DEV KHANDAV VAN KO JALAAKAR APNI BHOOKH MITAANA CHAHTE THE", sc("yamuna", fx=[("forest_fire",)])),
        line_("लेकिन इंद्र देव हर बार बारिश करके वो आग बुझा देते थे।",
              "LEKIN INDRA DEV HAR BAAR BAARISH KARKE WOH AAG BUJHA DETE THE", sc("yamuna", fx=[("rain",)])),
        line_("अर्जुन ने कहा मैं आपकी मदद करूंगा लेकिन मेरे पास वैसा धनुष और रथ नहीं है।",
              "ARJUN NE KAHA MAIN AAPKI MADAD KARUNGA LEKIN MERE PAAS WAISA DHANUSH AUR RATH NAHI HAI",
              sc("yamuna", cast=[C("arjun", L, "namaste"), C("brahmin", R, "stand")], fx=[("agni", R, 0.6)])),
        line_("तब अग्नि देव ने वरुण देव से मांगकर अर्जुन को दिया गांडीव धनुष।",
              "TAB AGNI DEV NE VARUN DEV SE MAANGKAR ARJUN KO DIYA GANDIV DHANUSH",
              sc("yamuna", cast=[C("arjun", L, "bow"), C("brahmin", R, "stand")], fx=[("agni", R, 0.6), ("gift_bow", L, 520)])),
        line_("कभी खाली ना होने वाले दो तरकश।", "KABHI KHAALI NA HONE WAALE DO TARKASH",
              sc("yamuna", cast=[C("arjun", L, "namaste")], fx=[("gift_quiver", L + 300, 560)])),
        line_("और सफेद घोड़ों वाला एक दिव्य रथ जिसके झंडे पर वानर का निशान था।",
              "AUR SAFED GHODON WAALA EK DIVYA RATH JISKE JHANDE PAR VAANAR KA NISHAAN THA",
              sc("yamuna", rath=dict(x=700, appear="ramp", han=0.0), fx=[("flowers",)])),
        line_("यही था अर्जुन का रथ।", "YAHI THA ARJUN KA RATH",
              sc("yamuna", rath=dict(x=700, krishna="reins", arjun="bow", han=0.0, run=0.6), zoom=(1.0, 1.08, 960, 600))),
    ]},
    {"key": "hanuman", "title": "DHWAJ PAR HANUMAN", "lines": [
        line_("अब सवाल ये कि उस झंडे पर हनुमान जी कैसे आए।", "AB SAWAAL YEH KI US JHANDE PAR HANUMAN JI KAISE AAYE",
              sc("dusk", rath=dict(x=700), zoom=(1.0, 1.3, 680, 120))),
        line_("वनवास के दिनों में भीम जंगल में फूल लेने निकले।", "VANVAAS KE DINON MEIN BHEEM JANGAL MEIN PHOOL LENE NIKLE",
              sc("forest", cast=[C("bheem", 1100, "stand", enter=(1700, 4))])),
        line_("रास्ते में एक बूढ़ा वानर लेटा था और उसकी पूंछ रास्ता रोक रही थी।",
              "RAASTE MEIN EK BOODHA VAANAR LETA THA AUR USKI POONCHH RAASTA ROK RAHI THI",
              sc("forest", cast=[C("hanuman", 420, "think", s=0.56, kw=dict(aura=False))],
                 fx=[("tail", 500, 900, 1250, 950)])),
        line_("भीम ने गुस्से में कहा अपनी पूंछ हटाओ।", "BHEEM NE GUSSE MEIN KAHA APNI POONCHH HATAAO",
              sc("forest", cast=[C("hanuman", 420, "think", s=0.56, kw=dict(aura=False)), C("bheem", 1400, "angry", flip=True)],
                 fx=[("tail", 500, 900, 1250, 950)])),
        line_("वानर बोला मैं बहुत बूढ़ा हूं तुम खुद हटा दो।", "VAANAR BOLA MAIN BAHUT BOODHA HOON TUM KHUD HATA DO",
              sc("forest", cast=[C("hanuman", 420, "abhaya", s=0.56, kw=dict(aura=False)), C("bheem", 1400, "stand", flip=True)],
                 fx=[("tail", 500, 900, 1250, 950)])),
        line_("भीम ने पूरा ज़ोर लगाया लेकिन पूंछ हिली तक नहीं।", "BHEEM NE POORA ZOR LAGAAYA LEKIN POONCHH HILI TAK NAHI",
              sc("forest", cast=[C("hanuman", 420, "think", s=0.56, kw=dict(aura=False)),
                                 C("bheem", 1250, "push", kw=dict(strain=1.0))], fx=[("tail", 500, 900, 1250, 950, 1.0)])),
        line_("तब भीम समझ गए ये कोई साधारण वानर नहीं है।", "TAB BHEEM SAMAJH GAYE YEH KOI SADHARAN VAANAR NAHI HAI",
              sc("forest", cast=[C("hanuman", 420, "think", s=0.56, kw=dict(aura=False)), C("bheem", 1400, "namaste", flip=True)],
                 fx=[("tail", 500, 900, 1250, 950)])),
        line_("वो थे पवनपुत्र हनुमान जो भीम के बड़े भाई थे।", "WOH THE PAVANPUTRA HANUMAN JO BHEEM KE BADE BHAI THE",
              sc("forest", cast=[C("hanuman", L, "gada", s=0.6), C("bheem", R, "namaste", flip=True)],
                 fx=[("glow", L, 600, 300, GOLD_HI)])),
        line_("हनुमान जी ने भीम को आशीर्वाद दिया और एक वचन दिया।", "HANUMAN JI NE BHEEM KO AASHIRWAAD DIYA AUR EK VACHAN DIYA",
              sc("forest", cast=[C("hanuman", L, "abhaya", s=0.6), C("bheem", R, "namaste", flip=True)], fx=[("flowers",)])),
        line_("जब युद्ध होगा तब मैं अर्जुन के रथ के झंडे पर बैठूंगा।",
              "JAB YUDDH HOGA TAB MAIN ARJUN KE RATH KE JHANDE PAR BAITHUNGA",
              sc("dusk", rath=dict(RATH_ON, x=700, han=1.0), zoom=(1.3, 1.0, 680, 120))),
        line_("और मेरी गर्जना से दुश्मन कांप उठेंगे।", "AUR MERI GARJANA SE DUSHMAN KAANP UTHENGE",
              sc("dusk", rath=dict(RATH_ON, x=560, run=0.8),
                 cast=[C("duryodhan", 1560, "panic", s=0.56, flip=True)], fx=[("glow", 520, 300, 260, SAFF)])),
    ]},
    {"key": "sarathi", "title": "KRISHNA BANE SAARTHI", "lines": [
        line_("फिर आया युद्ध से पहले का समय।", "PHIR AAYA YUDDH SE PEHLE KA SAMAY", sc("palace", zoom=(1.08, 1.0, 960, 500))),
        line_("दुर्योधन और अर्जुन दोनों मदद मांगने द्वारका पहुंचे।",
              "DURYODHAN AUR ARJUN DONO MADAD MAANGNE DWARKA PAHUNCHE",
              sc("palace", cast=[C("duryodhan", 560, "point", s=0.58, enter=(200, 2.5)),
                                 C("arjun", 1360, "namaste", enter=(1720, 2.5))])),
        line_("कृष्ण सो रहे थे।", "KRISHNA SO RAHE THE",
              sc("palace", cast=[C("dkrishna", 1140, "rest", s=0.5, y=860, lie=True, kw=dict(aura=False))],
                 fx=[("bed", 960, 870)])),
        line_("दुर्योधन घमंड से सिरहाने बैठ गया।", "DURYODHAN GHAMAND SE SIRHAANE BAITH GAYA",
              sc("palace", cast=[C("dkrishna", 1140, "rest", s=0.5, y=860, lie=True, kw=dict(aura=False)),
                                 C("duryodhan", 400, "point", s=0.56)], fx=[("bed", 960, 870)])),
        line_("और अर्जुन हाथ जोड़कर पैरों की तरफ बैठ गया।", "AUR ARJUN HAATH JODKAR PAIRON KI TARAF BAITH GAYA",
              sc("palace", cast=[C("dkrishna", 1140, "rest", s=0.5, y=860, lie=True, kw=dict(aura=False)),
                                 C("duryodhan", 400, "point", s=0.56), C("arjun", 1500, "namaste", s=0.56)],
                 fx=[("bed", 960, 870)])),
        line_("कृष्ण की आंख खुली तो सबसे पहले अर्जुन दिखे।", "KRISHNA KI AANKH KHULI TOH SABSE PEHLE ARJUN DIKHE",
              sc("palace", cast=[C("dkrishna", 960, "bless", s=0.6), C("arjun", 1500, "namaste", s=0.58),
                                 C("duryodhan", 420, "point", s=0.56)])),
        line_("कृष्ण बोले एक तरफ मेरी पूरी नारायणी सेना है।", "KRISHNA BOLE EK TARAF MERI POORI NARAYANI SENA HAI",
              sc("dusk", cast=[C("dkrishna", 560, "ask", s=0.6)], fx=[("glow", 1300, 800, 400, GOLD)],
                 rath=None)),
        line_("और दूसरी तरफ मैं अकेला जो हथियार नहीं उठाऊंगा।", "AUR DOOSRI TARAF MAIN AKELA JO HATHIYAAR NAHI UTHAAUNGA",
              sc("cosmos", cast=[C("dkrishna", 960, "flute", s=0.62)], fx=[("glow", 960, 600, 400, GOLD_HI)])),
        line_("पहले चुनने का मौका अर्जुन को मिला।", "PEHLE CHUNNE KA MAUKA ARJUN KO MILA",
              sc("palace", cast=[C("dkrishna", 960, "ask", s=0.6, flip=True), C("arjun", 1500, "namaste", s=0.58),
                                 C("duryodhan", 420, "panic", s=0.56)])),
        line_("और अर्जुन ने बिना सोचे कहा मुझे सिर्फ आप चाहिए।", "AUR ARJUN NE BINA SOCHE KAHA MUJHE SIRF AAP CHAHIYE",
              sc("palace", cast=[C("dkrishna", 1100, "bless", s=0.6), C("arjun", 640, "namaste", s=0.58, bow=0.4)],
                 fx=[("flowers",)])),
        line_("दुर्योधन को लगा सेना मिल गई तो जीत पक्की है।", "DURYODHAN KO LAGA SENA MIL GAYI TOH JEET PAKKI HAI",
              sc("dusk", cast=[C("duryodhan", 960, "point", s=0.6, kw=dict(shout=1.0))])),
        line_("लेकिन अर्जुन को वो मिल गया था जो उसके रथ की लगाम थामेगा।",
              "LEKIN ARJUN KO WOH MIL GAYA THA JO USKE RATH KI LAGAAM THAAMEGA",
              sc("dusk", rath=dict(RATH_ON, x=700, run=0.7))),
    ]},
    {"key": "gita", "title": "ISI RATH PAR GEETA", "lines": [
        line_("युद्ध के पहले दिन अर्जुन ने सामने अपने ही दादा और गुरु देखे।",
              "YUDDH KE PEHLE DIN ARJUN NE SAAMNE APNE HI DAADA AUR GURU DEKHE",
              sc("dusk", cast=[C("arjun", 520, "confused"), C("drona", 1420, "command", s=0.58, flip=True)])),
        line_("उसका गांडीव हाथ से फिसल गया।", "USKA GANDIV HAATH SE PHISAL GAYA",
              sc("dusk", cast=[C("arjun", 860, "shock")], fx=[("bow_drop", 1060)], zoom=(1.0, 1.12, 860, 600))),
        line_("वो रथ पर बैठ गया और बोला मैं नहीं लड़ूंगा।", "WOH RATH PAR BAITH GAYA AUR BOLA MAIN NAHI LADUNGA",
              sc("dusk", rath=dict(krishna="stand", arjun="confused", x=700))),
        line_("तब इसी रथ पर खड़े होकर कृष्ण ने गीता का ज्ञान दिया।", "TAB ISI RATH PAR KHADE HOKAR KRISHNA NE GEETA KA GYAAN DIYA",
              sc("dusk", cast=[C("krishna", 1180, "bless"), C("arjun", 640, "namaste", s=0.56)],
                 fx=[("glow", 1180, 560, 360, GOLD_HI)])),
        line_("और अपना विराट रूप दिखाया।", "AUR APNA VIRAT ROOP DIKHAAYA",
              sc("cosmos", cast=[C("dkrishna", 1080, "dance", s=0.7), C("arjun", 380, "namaste", s=0.45, bow=0.5)],
                 fx=[("cosmic", 1080, 560)])),
        line_("यानी जिस रथ पर दुनिया का सबसे बड़ा ज्ञान दिया गया वो यही रथ था।",
              "YAANI JIS RATH PAR DUNIYA KA SABSE BADA GYAAN DIYA GAYA WOH YAHI RATH THA",
              sc("dusk", rath=dict(krishna="bless", arjun="namaste", x=700), fx=[("glow", 760, 600, 500, GOLD_HI)])),
    ]},
    {"key": "astra", "title": "RATH NE JHELE VAAR", "lines": [
        line_("अब युद्ध शुरू हुआ और हर बड़ा योद्धा इसी रथ को निशाना बनाने लगा।",
              "AB YUDDH SHURU HUA AUR HAR BADA YODDHA ISI RATH KO NISHAANA BANAANE LAGA",
              sc("dusk", rath=dict(RATH_ON, x=560, run=0.8), fx=[("arrows", 1900, 400, 700, 650, 6)])),
        line_("भीष्म पितामह के बाणों से कृष्ण का शरीर भी घायल हुआ।",
              "BHISHMA PITAMAH KE BAANON SE KRISHNA KA SHAREER BHI GHAYAL HUA",
              sc("dusk", rath=dict(krishna="reins", arjun="bow", x=600), fx=[("arrows", 1900, 300, 650, 690, 8)])),
        line_("एक दिन राजा भगदत्त ने अर्जुन पर विष्णु जी का दिया हुआ हथियार चला दिया।",
              "EK DIN RAJA BHAGDATT NE ARJUN PAR VISHNU JI KA DIYA HUA HATHIYAAR CHALA DIYA",
              sc("dusk", rath=dict(krishna="reins", arjun="shock", x=600), fx=[("orb", 1900, 300, 560, 720)])),
        line_("कृष्ण बीच में खड़े हो गए और वो वार अपनी छाती पर ले लिया।",
              "KRISHNA BEECH MEIN KHADE HO GAYE AUR WOH VAAR APNI CHHAATI PAR LE LIYA",
              sc("dusk", cast=[C("arjun", 520, "shock", s=0.56), C("krishna", 940, "stand")],
                 fx=[("orb", 1900, 350, 940, 690)])),
        line_("और वो हथियार उनके गले में फूलों की माला बन गया।", "AUR WOH HATHIYAAR UNKE GALE MEIN PHOOLON KI MAALA BAN GAYA",
              sc("dusk", rath=dict(krishna="bless", arjun="namaste", x=700, garland="ramp"),
                 zoom=(1.0, 1.35, 790, 560), fx=[("flowers",)])),
        line_("गुरु द्रोण ने भी रथ पर बड़े बड़े दिव्य बाण चलाए।", "GURU DRON NE BHI RATH PAR BADE BADE DIVYA BAAN CHALAAYE",
              sc("dusk", rath=dict(RATH_ON, x=480), cast=[C("drona", 1600, "command", s=0.56, flip=True)],
                 fx=[("arrows", 1480, 600, 600, 700, 5, FIRE_O)])),
        line_("और कर्ण के बाणों ने भी इस रथ पर लगातार वार किए।", "AUR KARNA KE BAANON NE BHI IS RATH PAR LAGAATAR VAAR KIYE",
              sc("dusk", rath=dict(RATH_ON, x=480), cast=[C("karna", 1600, "stand", s=0.56)],
                 fx=[("arrows", 1480, 560, 600, 700, 6, GOLD_HI)])),
        line_("लोक कथा कहती है कि एक बार कर्ण के बाण से ये रथ थोड़ा पीछे खिसक गया।",
              "LOK KATHA KEHTI HAI KI EK BAAR KARNA KE BAAN SE YEH RATH THODA PEECHHE KHISAK GAYA",
              sc("dusk", rath=dict(RATH_ON, x=520, slide=90), cast=[C("karna", 1600, "stand", s=0.56)],
                 fx=[("one_arrow", 1480, 560, 700, 700, 0.1, 0.42, GOLD_HI)])),
        line_("तब कृष्ण बोले वाह कर्ण वाह।", "TAB KRISHNA BOLE VAAH KARNA VAAH",
              sc("dusk", cast=[C("krishna", 960, "bless")], zoom=(1.0, 1.1, 960, 560))),
        line_("अर्जुन हैरान होकर बोला प्रभु मेरे बाण से तो उसका रथ बहुत दूर जाता है।",
              "ARJUN HAIRAAN HOKAR BOLA PRABHU MERE BAAN SE TOH USKA RATH BAHUT DOOR JAATA HAI",
              sc("dusk", cast=[C("arjun", L, "confused"), C("krishna", R, "stand")])),
        line_("कृष्ण मुस्कुराए और बोले इस रथ पर मैं और हनुमान दोनों बैठे हैं।",
              "KRISHNA MUSKURAAYE AUR BOLE IS RATH PAR MAIN AUR HANUMAN DONO BAITHE HAIN",
              sc("dusk", cast=[C("arjun", L, "namaste"), C("krishna", R, "bless")],
                 fx=[("glow", R, 560, 300, GOLD_HI)])),
        line_("फिर भी अगर ये रथ हिला तो सोचो उस बाण में कितनी ताकत होगी।",
              "PHIR BHI AGAR YEH RATH HILA TOH SOCHO US BAAN MEIN KITNI TAAKAT HOGI",
              sc("dusk", rath=dict(RATH_ON, x=640), zoom=(1.3, 1.0, 640, 500))),
    ]},
    {"key": "reveal", "title": "AATHARAHVAN DIN", "lines": [
        line_("अठारहवें दिन युद्ध खत्म हुआ और पांडव जीत गए।", "18VEIN DIN YUDDH KHATAM HUA AUR PANDAV JEET GAYE",
              sc("dusk", rath=dict(krishna="stand", arjun="namaste", x=700), fx=[("flowers",)])),
        line_("तब कृष्ण ने कहा अर्जुन अपना गांडीव और तरकश लेकर पहले उतरो।",
              "TAB KRISHNA NE KAHA ARJUN APNA GANDIV AUR TARKASH LEKAR PEHLE UTRO",
              sc("dusk", rath=dict(krishna="command", arjun="bow", x=700), zoom=(1.0, 1.15, 760, 560))),
        line_("अर्जुन उतरा तो हनुमान जी भी झंडे से उड़कर चले गए।", "ARJUN UTRA TOH HANUMAN JI BHI JHANDE SE UDKAR CHALE GAYE",
              sc("dusk", rath=dict(krishna="command", x=800, han_fly="ramp"), cast=[C("arjun", 330, "bow", enter=(520, 1.2))])),
        line_("फिर कृष्ण उतरे और रथ धू धू करके जलने लगा।", "PHIR KRISHNA UTRE AUR RATH DHOO DHOO KARKE JALNE LAGA",
              sc("dusk", rath=dict(x=800, han=0.0, burn="ramp", burn_at=0.2),
                 cast=[C("arjun", 330, "shock"), C("krishna", 1680, "stand", enter=(1300, 0.8))])),
        line_("घोड़े रथ और झंडा सब राख हो गया।", "GHODE RATH AUR JHANDA SAB RAAKH HO GAYA",
              sc("night", rath=dict(x=800, han=0.0, burn=0.9), cast=[C("arjun", 330, "shock"), C("krishna", 1680, "stand")])),
        line_("अर्जुन ने कांपते हुए पूछा प्रभु ये क्या हुआ।", "ARJUN NE KAANPTE HUE POOCHHA PRABHU YEH KYA HUA",
              sc("night", cast=[C("arjun", L, "shock"), C("krishna", R, "stand")], fx=[("glow", 960, 900, 300, FIRE_O)])),
        line_("कृष्ण बोले अर्जुन ये रथ तो द्रोण और कर्ण के बाणों से बहुत पहले ही जल चुका था।",
              "KRISHNA BOLE ARJUN YEH RATH TOH DRON AUR KARNA KE BAANON SE BAHUT PEHLE HI JAL CHUKA THA",
              sc("night", cast=[C("arjun", L, "confused"), C("krishna", R, "bless")],
                 fx=[("arrows", 1900, 300, 960, 760, 5, FIRE_O)])),
        line_("मैं इस पर बैठा था इसलिए ये अब तक टिका रहा।", "MAIN IS PAR BAITHA THA ISLIYE YEH AB TAK TIKA RAHA",
              sc("night", rath=dict(krishna="reins", x=800, horses=False), fx=[("glow", 860, 560, 420, GOLD_HI)])),
        line_("अगर मैं पहले उतरता तो तुम भी इसी आग में जल जाते।", "AGAR MAIN PEHLE UTARTA TOH TUM BHI ISI AAG MEIN JAL JAATE",
              sc("night", cast=[C("arjun", L, "shock")], fx=[("glow", 1200, 900, 400, FIRE_O)])),
        line_("ये सुनकर अर्जुन की आंखें भर आईं और वो कृष्ण के चरणों में गिर पड़ा।",
              "YEH SUNKAR ARJUN KI AANKHEIN BHAR AAYIN AUR WOH KRISHNA KE CHARANON MEIN GIR PADA",
              sc("night", cast=[C("krishna", 1180, "bless"), C("arjun", 700, "namaste", bow=0.9)],
                 fx=[("glow", 1180, 560, 360, GOLD_HI), ("flowers",)])),
    ]},
    {"key": "ask", "title": "JAI SHRI KRISHNA", "lines": [
        line_("सोचो जिस रथ को हम अपनी ताकत समझते हैं।", "SOCHO JIS RATH KO HUM APNI TAAKAT SAMAJHTE HAIN",
              sc("dusk", rath=dict(RATH_ON, x=700, run=0.6))),
        line_("हो सकता है उसे कोई और चुपचाप थामे बैठा हो।", "HO SAKTA HAI USE KOI AUR CHUPCHAAP THAAME BAITHA HO",
              sc("dusk", rath=dict(krishna="reins", arjun="bow", x=700), fx=[("glow", 760, 580, 520, GOLD_HI)],
                 zoom=(1.0, 1.2, 760, 560))),
        line_("आपको इस कहानी का कौन सा हिस्सा सबसे अच्छा लगा कमेंट में बताइए।",
              "AAPKO IS KAHANI KA KAUN SA HISSA SABSE ACHHA LAGA COMMENT MEIN BATAAIYE",
              sc("cosmos", cast=[C("dkrishna", 960, "bless", s=0.62)], fx=[("cosmic", 960, 600), ("flowers",)])),
        line_("और कमेंट में जय श्री कृष्ण ज़रूर लिखिए।", "AUR COMMENT MEIN JAI SHRI KRISHNA ZAROOR LIKHIYE",
              sc("cosmos", cast=[C("dkrishna", 960, "flute", s=0.62)], fx=[("cosmic", 960, 600), ("flowers",)])),
        line_("ऐसी ही दिव्य कहानियों के लिए दिव्य रहस्य को सब्सक्राइब कर लीजिए।",
              "AISI HI DIVYA KAHANIYON KE LIYE DIVYA RAHASYA KO SUBSCRIBE KAR LIJIYE",
              sc("dusk", rath=dict(RATH_ON, x=700, run=0.8), fx=[("flowers",)])),
    ]},
]

SOURCES = [
    "Mahabharata, Adi Parva (Khandava-daha, ch. 223-225): Agni comes to Krishna and Arjuna on the Yamuna bank as a "
    "brahmin, wants to consume the Khandava forest that Indra protects with rain; at Arjuna's request Agni has "
    "Varuna give Gandiva, two inexhaustible quivers and a chariot with white horses and the ape banner (kapidhvaja).",
    "Mahabharata, Vana Parva (ch. 146-151): Bhima, seeking the Saugandhika flower, finds an old monkey whose tail "
    "blocks the path and cannot lift it; Hanuman reveals himself (both sons of Vayu) and promises to sit on Arjuna's "
    "banner and roar to terrify the enemy.",
    "Mahabharata, Udyoga Parva (ch. 7): Duryodhana sits at Krishna's head, Arjuna at his feet; Krishna sees Arjuna first, "
    "offers the Narayani army or himself unarmed; Arjuna chooses Krishna; Duryodhana is pleased with the army.",
    "Bhagavad Gita ch. 1-2, 11: Arjuna's Gandiva slips, he sits down in the chariot; Krishna teaches the Gita; Vishvarupa.",
    "Mahabharata, Bhishma Parva: Krishna is wounded by Bhishma's arrows.",
    "Mahabharata, Drona Parva (ch. 29): Bhagadatta hurls the Vaishnava weapon at Arjuna; Krishna receives it on his chest, "
    "where it becomes the Vaijayanti garland.",
    "Folk tradition (not in Vyasa's text, told as 'lok katha'): Karna's arrow pushes the chariot back a little and "
    "Krishna praises him, because Krishna and Hanuman are on it.",
    "Mahabharata, Shalya Parva (ch. 62): after the war Krishna tells Arjuna to get down first with Gandiva and quivers; "
    "the ape leaves the banner; when Krishna dismounts the chariot burns to ashes; Krishna says it was already burnt "
    "by Drona's and Karna's celestial weapons and held together only by his presence.",
]

UPLOAD = {
    "title": "Why Arjuna's Chariot Burned After the Mahabharata War | Full Story",
    "description": """
Mahabharat yuddh khatam hote hi Shri Krishna ne Arjun ko pehle rath se utarne ko kaha - aur Krishna ke utarte hi
rath aag mein jalkar raakh ho gaya. Kyun? Is video mein Arjun ke rath ki poori kahani: Khandav van mein Agni dev ka
vardaan (Gandiv, akshay tarkash aur divya rath), Bheem aur Hanuman ji ki bhent aur dhwaj par baithne ka vachan,
Dwarka mein Krishna ka saarthi banna, isi rath par Geeta, Bhagdatt ka Vaishnav astra jo Vaijayanti maala ban gaya,
Dron aur Karna ke divya baan, aur 18ve din ka rahasya.

Aapko kahani ka kaunsa hissa sabse achha laga? Comment mein batayein aur JAI SHRI KRISHNA likhein.

Kathayein Mahabharat (Adi, Vana, Udyog, Drona aur Shalya Parva) par aadharit hain. Karna ke baan se rath khisakne
wala prasang lok katha hai, video mein bhi yahi kaha gaya hai.
""",
    "hashtags": "#Mahabharat #ShriKrishna #Arjun #Hanuman #DivyaRahasya",
    "tags": ["arjun rath", "arjuna chariot burned", "mahabharat story hindi", "krishna arjun", "kapidhwaj",
             "hanuman on arjun flag", "gandiv", "khandav van", "vaijayanti mala", "bhagdatt vaishnav astra",
             "karna arrow chariot", "mahabharat rahasya", "divya rahasya", "krishna katha"],
    "pinned": "Krishna ke utarte hi rath raakh ho gaya - aapke hisaab se is kahani ka sabse bada sandesh kya hai? "
              "Comment mein likhiye aur JAI SHRI KRISHNA zaroor likhiye.",
}


def thumbnail(ctx):
    """Burning chariot behind, Krishna blessing on the left, Arjun shocked, 'WHY DID IT BURN?'."""
    T = 1.7
    bg_dusk(ctx, T)
    rgba(ctx, (0.2, 0.02, 0.0), 0.35)
    ctx.paint()
    rath(ctx, 1240, 980, 0.66, T, burn=0.55, han=0.0)
    ar.krishna(ctx, 330, 1040, 0.64, T, pose="bless")
    ar.arjuna(ctx, 760, 1040, 0.56, T, pose="shock")
    g = cairo.LinearGradient(0, 0, 0, 300)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.75)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g)
    ctx.paint()
    text(ctx, "WHY DID IT BURN?", W / 2 + 120, 150, 150, hexc("#FFD84A"), font="Impact", stroke=(0.2, 0, 0),
         stroke_w=12)
