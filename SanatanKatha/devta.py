"""Devta character rig for Sanatan katha Shorts: cartoon characters drawn entirely in Cairo code.

Style: flat colours with a soft cel highlight, a dark ink outline round every shape, big expressive eyes
(blink, look direction) and gentle idle motion, so the same set can be reused in every katha.

Characters (each drawn standing on (x, y) = feet, scale s, time t):
  krishna(...)   blue skin, peacock-feather mukut, pitambar, vaijayanti mala; poses stand / flute / bless / ask
  brahmin(...)   old brahmin (Krishna's disguise): shikha, white beard, saffron dhoti, staff; poses stand / ask / point
  barbarik(...)  young warrior: gold mukut + kavach, curled moustache, quiver of 3 glowing arrows;
                 poses stand / draw (bow drawn, draw=0..1) / namaste; mood fierce / calm
  shyam(...)     the Khatu Shyam sheesh roop: dark face, big eyes, tall mukut with peacock feathers, flower garlands
  devi(...)      Chhathi Maiya / Shashthi Devi: red saree, gold mukut, sindoor, nath, lotus; poses bless / touch / open
  surya(...)     Surya Dev: rayed sun disc, kirit mukut, a lotus in each raised hand
  raja(...)      a king (Priyavrat): kalgi mukut, moustache, purple angarkha; pose hold (with baby) / stand; mood sad / happy
  vrati(...)     a Chhath vrati waist-deep in water raising her soop; also baby(), soop(), yagya_kund(), lotus(), sun_disc()
Props: peepal tree (leaves that can be marked by an arrow), divine arrow, bow, balance, diya, hill, army
silhouettes, petals, Kailash, ribbons/name plates.
Nothing here is traced from or copies anyone's artwork: shapes are built from ellipses and spline paths.
"""

import math

import cairo

from engine import (CAPTION_FONT, H, W, circle, clamp, ease_in_out, ease_out_back, ease_out_cubic, glow, hexc,
                    lerp, line, rgba, rnd, rrect, shade, text)

OUTLINE = hexc("#2A140A")
OW = 6.0                                  # outline width in character units
WHITE = (1.0, 0.98, 0.95)
GOLD = hexc("#F2B829")
GOLD_HI = hexc("#FFE38A")
GOLD_DK = hexc("#B07A12")
RED_GEM = hexc("#D61F3A")
GREEN_GEM = hexc("#1FA35B")
SAFFRON = hexc("#FF9933")
KRISHNA_SKIN = hexc("#4F86E0")
KRISHNA_HAIR = hexc("#1C1430")
PITAMBAR = hexc("#F7C531")
BRAHMIN_SKIN = hexc("#E2A877")
BARBARIK_SKIN = hexc("#A8653C")
SHYAM_FACE = hexc("#26304F")
HAIR = hexc("#17100C")
DIVINE = hexc("#9FE8FF")                  # glow of the three divine arrows


# ============================================================ drawing primitives

def ell(ctx, x, y, rx, ry, rot=0.0):
    """Ellipse path (adds to the current path)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(rx, ry)
    ctx.new_sub_path()
    ctx.arc(0, 0, 1, 0, math.tau)
    ctx.restore()


def ink(ctx, c, w=OW, a=1.0, edge=OUTLINE):
    """Fill the current path with c and ink its outline."""
    rgba(ctx, c, a)
    ctx.fill_preserve()
    rgba(ctx, edge, a)
    ctx.set_line_width(w)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.stroke()


def smooth(ctx, pts, closed=True, k=1 / 6):
    """Catmull-Rom spline through pts as a Cairo path."""
    n = len(pts)
    ctx.move_to(*pts[0])
    for i in range(n if closed else n - 1):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        ctx.curve_to(p1[0] + (p2[0] - p0[0]) * k, p1[1] + (p2[1] - p0[1]) * k,
                     p2[0] - (p3[0] - p1[0]) * k, p2[1] - (p3[1] - p1[1]) * k, *p2)
    if closed:
        ctx.close_path()


def mirror(pts):
    return [(-x, y) for x, y in pts]


def limb(ctx, pts, c, w):
    """Cartoon limb: an inked tube through pts."""
    line(ctx, pts, OUTLINE, w + 2 * OW)
    line(ctx, pts, c, w)


def sheen(ctx, x, y, rx, ry, a=0.18):
    """Soft cel highlight."""
    ell(ctx, x, y, rx, ry)
    rgba(ctx, (1, 1, 1), a)
    ctx.fill()


def blinking(t, seed):
    return ((t + seed * 1.37) % 3.9) < 0.11


def eye(ctx, x, y, rx, ry, t, look=(0.0, 0.0), iris=hexc("#3B2314"), closed=False, seed=0, lash=True,
        lid=0.0, skin=None, rim=OUTLINE):
    """Big cartoon eye. closed=True (or a blink) draws a soft closed arc; lid (0..1) lowers the upper lid."""
    if closed or blinking(t, seed):
        line(ctx, [(x - rx, y), (x - rx * 0.5, y + ry * 0.32), (x + rx * 0.5, y + ry * 0.32), (x + rx, y)], rim, 6)
        return
    ell(ctx, x, y, rx, ry)
    ink(ctx, WHITE, 3.5, edge=rim)
    ctx.save()
    ell(ctx, x, y, rx, ry)
    ctx.clip()
    ix, iy = x + look[0] * rx * 0.38, y + look[1] * ry * 0.3 + ry * 0.08
    circle(ctx, ix, iy, ry * 0.7, iris)
    circle(ctx, ix, iy, ry * 0.4, (0.04, 0.02, 0.02))
    circle(ctx, ix - ry * 0.22, iy - ry * 0.26, ry * 0.2, (1, 1, 1))
    circle(ctx, ix + ry * 0.2, iy + ry * 0.2, ry * 0.08, (1, 1, 1), 0.8)
    if lid > 0 and skin is not None:
        ctx.rectangle(x - rx - 2, y - ry - 2, 2 * rx + 4, 2 * ry * lid + 2)
        rgba(ctx, skin)
        ctx.fill()
    ctx.restore()
    if lash:   # thick upper lash line
        top = [(x + rx * math.cos(a), y - ry * (1 - 2 * lid) * math.sin(a) * (1 if lid < 0.5 else 0.2))
               for a in [math.pi * (1 - i / 10) for i in range(11)]]
        line(ctx, top, rim, 7)


def group(ctx, a, draw):
    """Draw with a whole-figure alpha (no overlap seams)."""
    if a <= 0:
        return
    if a >= 1:
        draw()
        return
    ctx.push_group()
    draw()
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(a)


def halo(ctx, x, y, r, t, c=GOLD, a=1.0):
    """Prabhamandal: soft glow, a gold ring and slowly turning petals."""
    glow(ctx, x, y, r * 2.0, c, 0.45 * a)
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(t * 0.18)
    for k in range(16):
        ctx.save()
        ctx.rotate(k / 16 * math.tau)
        ell(ctx, r * 1.08, 0, r * 0.12, r * 0.05)
        rgba(ctx, GOLD_HI, 0.55 * a)
        ctx.fill()
        ctx.restore()
    ctx.restore()
    ctx.arc(x, y, r, 0, math.tau)
    rgba(ctx, GOLD_HI, 0.8 * a)
    ctx.set_line_width(r * 0.04)
    ctx.stroke()
    ctx.arc(x, y, r * 0.93, 0, math.tau)
    rgba(ctx, GOLD, 0.5 * a)
    ctx.set_line_width(r * 0.02)
    ctx.stroke()


def place(ctx, x, y, s, t, flip=False, breathe=True):
    """Enter a character's local frame: feet at (x, y), y up is negative."""
    ctx.save()
    ctx.translate(x, y)
    b = 1 + (0.012 * math.sin(t * 2.2) if breathe else 0)
    ctx.scale(-s if flip else s, s * b)


# ============================================================ ornaments shared by the characters

def peacock_feather(ctx, x, y, ang, L, t, a=1.0):
    """Mor pankh rooted at (x, y), pointing along ang (0 = straight up)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang + 0.05 * math.sin(t * 1.7))
    vane = [(0, -L * 0.15), (-14, -L * 0.4), (-30, -L * 0.7), (-24, -L * 0.93), (0, -L * 1.02), (24, -L * 0.93),
            (30, -L * 0.7), (14, -L * 0.4)]
    smooth(ctx, vane)
    ink(ctx, hexc("#2F9E5B"), 4, a)
    for k in range(9):          # barbs
        yy = -L * (0.25 + 0.08 * k)
        w = 12 + 16 * math.sin(math.pi * (0.2 + 0.08 * k))
        for sgn in (-1, 1):
            line(ctx, [(0, yy), (sgn * w, yy - 14)], hexc("#7BD389"), 2, 0.7 * a)
    ex, ey = 0, -L * 0.78
    for rx, ry, c in ((26, 32, hexc("#C9B037")), (19, 24, hexc("#1FA6A0")), (12, 15, hexc("#0E1E5B")),
                      (5, 6, hexc("#2C4BB8"))):
        ell(ctx, ex, ey, rx, ry)
        rgba(ctx, c, a)
        ctx.fill()
    line(ctx, [(0, 0), (0, -L * 0.96)], hexc("#F6EBD0"), 3, a)
    ctx.restore()


def gem(ctx, x, y, r, c):
    ell(ctx, x, y, r, r * 1.15)
    ink(ctx, c, 2.5)
    circle(ctx, x - r * 0.3, y - r * 0.35, r * 0.3, (1, 1, 1), 0.8)


def pearls(ctx, pts, r=4.5):
    for x, y in pts:
        circle(ctx, x, y, r, WHITE)


def hand(ctx, x, y, skin, r=28):
    ell(ctx, x, y, r, r * 0.95)
    ink(ctx, skin)


def palm(ctx, x, y, skin, ang=0.0, s=1.0):
    """Open palm facing the viewer (abhaya / asking), fingers up along ang."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(s, s)
    for k, dx in enumerate((-20, -7, 7, 20)):
        L = (38, 46, 44, 36)[k]
        line(ctx, [(dx, -10), (dx, -10 - L)], OUTLINE, 14 + 2 * OW * 0.6)
        line(ctx, [(dx, -10), (dx, -10 - L)], skin, 14)
    line(ctx, [(-26, 10), (-44, -16)], OUTLINE, 16 + 2 * OW * 0.6)
    line(ctx, [(-26, 10), (-44, -16)], skin, 16)
    rrect(ctx, -30, -18, 60, 50, 18)
    ink(ctx, skin, OW * 0.6)
    ctx.restore()


# ============================================================ Shri Krishna

def _krishna_arms(pose, t):
    """[(shoulder, elbow, hand), ...] screen-left arm first."""
    L, R = (-118, -490), (118, -490)
    if pose == "flute":
        f = 4 * math.sin(t * 3)
        return [(L, (-55, -420), (70 + f, -596)), (R, (220, -470), (190 - f, -578))]
    if pose == "bless":
        return [(L, (-165, -390), (-152, -302)), (R, (200, -425), (178 + 3 * math.sin(t * 2), -565))]
    if pose == "ask":
        return [(L, (-165, -390), (-152, -302)), (R, (215, -415), (305, -440 + 4 * math.sin(t * 2.4)))]
    return [(L, (-160, -395), (-150, -305)), (R, (160, -395), (150, -305))]


def krishna(ctx, x, y, s, t, pose="flute", look=(0.0, 0.0), smile=1.0, flip=False, a=1.0, aura=True):
    """Shri Krishna, cartoon: blue skin, mor-pankh mukut, pitambar, vaijayanti mala, bansuri."""
    def draw():
        place(ctx, x, y, s, t, flip)
        if aura:
            halo(ctx, 0, -650, 175, t)
        _krishna_body(ctx, t, pose, look, smile)
        ctx.restore()
    group(ctx, a, draw)


def _flute(ctx, x0, y0, x1, y1):
    line(ctx, [(x0, y0), (x1, y1)], OUTLINE, 18 + 2 * 3)
    line(ctx, [(x0, y0), (x1, y1)], hexc("#C98A3C"), 18)
    for k in range(6):
        u = 0.35 + 0.09 * k
        circle(ctx, lerp(x0, x1, u), lerp(y0, y1, u), 3.6, OUTLINE)
    for u in (0.12, 0.92):
        line(ctx, [(lerp(x0, x1, u) - 2, lerp(y0, y1, u) - 9), (lerp(x0, x1, u) + 2, lerp(y0, y1, u) + 9)], GOLD, 5)
    # red tassel hanging from the end
    tx, ty = lerp(x0, x1, 0.95), lerp(y0, y1, 0.95)
    line(ctx, [(tx, ty), (tx + 4, ty + 34), (tx - 2, ty + 58)], RED_GEM, 6)
    circle(ctx, tx - 2, ty + 62, 8, RED_GEM)


def _krishna_body(ctx, t, pose, look, smile):
    skin = KRISHNA_SKIN
    # hair falling behind the shoulders
    for side in (-1, 1):
        smooth(ctx, [(side * 70, -700), (side * 122, -620), (side * 138, -540), (side * 128, -470), (side * 98, -480),
                      (side * 88, -560)])
        ink(ctx, KRISHNA_HAIR)
    ell(ctx, 0, -668, 116, 112)
    ink(ctx, KRISHNA_HAIR)
    # uttariya end, flowing behind the left arm
    sway = 10 * math.sin(t * 1.6)
    smooth(ctx, [(-120, -500), (-178 + sway, -390), (-170 + sway, -250), (-138 + sway, -262), (-140, -380)])
    ink(ctx, hexc("#E0502A"))
    # feet + anklets
    for fx in (-50, 50):
        ell(ctx, fx, -14, 44, 18)
        ink(ctx, skin)
        line(ctx, [(fx - 26, -30), (fx, -24), (fx + 26, -30)], GOLD, 7)
    # pitambar dhoti
    dhoti = [(-118, -345), (118, -345), (136, -200), (152, -44), (62, -32), (0, -64), (-62, -32), (-152, -44),
             (-136, -200)]
    smooth(ctx, dhoti)
    ink(ctx, PITAMBAR)
    line(ctx, [(150, -48), (62, -36), (0, -68), (-62, -36), (-150, -48)], hexc("#E8741E"), 13)
    for fx in (-60, -18, 26, 70):
        line(ctx, [(fx * 0.8, -330), (fx, -120)], shade(PITAMBAR, 0.82), 4, 0.8)
    smooth(ctx, [(-14, -345), (14, -345), (22, -200), (0, -150), (-22, -200)])      # front patka
    ink(ctx, hexc("#E0502A"), 4)
    line(ctx, [(-18, -190), (18, -190)], GOLD, 6)
    # torso
    smooth(ctx, [(-122, -500), (-60, -522), (60, -522), (122, -500), (128, -430), (100, -340), (-100, -340),
                 (-128, -430)])
    ink(ctx, skin)
    sheen(ctx, -30, -455, 60, 40, 0.14)
    circle(ctx, 0, -372, 4, shade(skin, 0.7))
    # sash across the chest
    smooth(ctx, [(-128, -505), (-88, -520), (118, -372), (96, -342)], k=0.1)
    ink(ctx, hexc("#E0502A"), 5)
    # kamarbandh
    rrect(ctx, -114, -366, 228, 34, 12)
    ink(ctx, GOLD, 5)
    for gx in (-70, 0, 70):
        gem(ctx, gx, -349, 8, RED_GEM if gx else GREEN_GEM)
    # gold necklace + vaijayanti mala
    line(ctx, [(-66, -516), (-30, -486), (0, -478), (30, -486), (66, -516)], GOLD, 8)
    gem(ctx, 0, -470, 9, RED_GEM)
    cols = (RED_GEM, WHITE, GOLD, GREEN_GEM, hexc("#9B4DCA"))
    for k in range(17):
        u = k / 16
        mx, my = -104 + 208 * u, -505 + 150 * math.sin(math.pi * u)
        ell(ctx, mx, my, 11, 11)
        ink(ctx, cols[k % len(cols)], 3)
    # neck + head
    rrect(ctx, -32, -566, 64, 64, 14)
    ink(ctx, skin)
    _krishna_head(ctx, t, look, smile)
    # arms (after the head so the flute hands sit on top)
    arms = _krishna_arms(pose, t)
    for sh, el, hd in arms:
        limb(ctx, [sh, el], skin, 50)
        limb(ctx, [el, hd], skin, 44)
        mx, my = lerp(sh[0], el[0], 0.45), lerp(sh[1], el[1], 0.45)
        line(ctx, [(mx - 22, my - 6), (mx + 22, my + 6)], GOLD, 10)             # bajuband
        wx, wy = lerp(el[0], hd[0], 0.78), lerp(el[1], hd[1], 0.78)
        circle(ctx, wx, wy, 26, GOLD)                                             # kangan
        circle(ctx, wx, wy, 19, skin)
    if pose == "flute":
        _flute(ctx, 14, -600, 310, -566)
        for _, _, hd in arms:
            hand(ctx, *hd, skin)
    elif pose in ("bless", "ask"):
        hd = arms[1][2]
        palm(ctx, *hd, skin, ang=0.0 if pose == "bless" else 1.35, s=1.0)
        lh = arms[0][2]
        _flute(ctx, lh[0] - 6, lh[1] - 150, lh[0] + 6, lh[1] + 120)
        hand(ctx, *lh, skin)
    else:
        for _, _, hd in arms:
            hand(ctx, *hd, skin)


def _krishna_head(ctx, t, look, smile):
    skin = KRISHNA_SKIN
    for side in (-1, 1):
        ell(ctx, side * 98, -640, 18, 28)
        ink(ctx, skin)
    ell(ctx, 0, -640, 100, 110)
    ink(ctx, skin)
    sheen(ctx, -36, -690, 40, 26, 0.14)
    for side in (-1, 1):                                  # makara kundal
        circle(ctx, side * 104, -604, 13, GOLD)
        ell(ctx, side * 104, -580, 9, 14)
        ink(ctx, GOLD, 3)
        ell(ctx, side * 52, -606, 20, 11)
        rgba(ctx, hexc("#FF7AA8"), 0.35)
        ctx.fill()
    for side in (-1, 1):
        eye(ctx, side * 38, -646, 25, 29, t, look=look, iris=hexc("#2A1810"), seed=1)
        line(ctx, [(side * 14, -686), (side * 38, -697), (side * 64, -688)], KRISHNA_HAIR, 7)
    line(ctx, [(2, -640), (-6, -618), (5, -613)], shade(skin, 0.65), 4)
    # smile
    ctx.move_to(-24, -594)
    ctx.curve_to(-10, -594 + 18 * smile, 10, -594 + 18 * smile, 24, -594)
    ctx.curve_to(10, -590 + 6 * smile, -10, -590 + 6 * smile, -24, -594)
    ctx.close_path()
    ink(ctx, hexc("#B5283C"), 3)
    # Vaishnav tilak
    line(ctx, [(-12, -714), (-9, -694), (0, -687), (9, -694), (12, -714)], hexc("#FFF2C4"), 6)
    line(ctx, [(0, -716), (0, -694)], hexc("#E2231A"), 5)
    # fringe curls under the crown
    for k in range(9):
        circle(ctx, -88 + 22 * k, -736 + 4 * abs(k - 4) * 0.4, 18, KRISHNA_HAIR)
    # feather goes behind the mukut front
    peacock_feather(ctx, 46, -812, 0.38, 170, t)
    rrect(ctx, -102, -776, 204, 36, 10)
    ink(ctx, GOLD, 5)
    smooth(ctx, [(-96, -772), (-74, -832), (-42, -812), (0, -884), (42, -812), (74, -832), (96, -772)], k=0.08)
    ink(ctx, GOLD, 5)
    smooth(ctx, [(-60, -784), (-40, -800), (0, -850), (40, -800), (60, -784)], k=0.08)
    rgba(ctx, GOLD_HI, 0.6)
    ctx.fill()
    gem(ctx, 0, -815, 15, RED_GEM)
    for gx, c in ((-62, GREEN_GEM), (62, GREEN_GEM), (-30, RED_GEM), (30, RED_GEM)):
        gem(ctx, gx, -758, 7, c)
    pearls(ctx, [(-96 + 12 * k, -772 + 0 * k) for k in range(17)], 3.2)


# ============================================================ Brahmin (Krishna's disguise)

def brahmin(ctx, x, y, s, t, pose="stand", mood="smile", look=(0.0, 0.0), flip=False, a=1.0, hint=0.0):
    """Old brahmin with shikha, white beard, saffron dhoti and a staff. hint (0..1) = a faint blue divine glow."""
    def draw():
        place(ctx, x, y, s, t, flip)
        if hint > 0:
            glow(ctx, 0, -560, 420, KRISHNA_SKIN, 0.45 * hint)
        _brahmin_body(ctx, t, pose, mood, look)
        ctx.restore()
    group(ctx, a, draw)


def _brahmin_body(ctx, t, pose, mood, look):
    skin = BRAHMIN_SKIN
    # staff in the screen-left hand
    line(ctx, [(-172, 12), (-176, -790)], OUTLINE, 18 + 2 * OW)
    line(ctx, [(-172, 12), (-176, -790)], hexc("#8A5A2B"), 18)
    ell(ctx, -176, -800, 18, 16)
    ink(ctx, hexc("#7A4A22"))
    # thin legs + feet
    for lx in (-42, 42):
        limb(ctx, [(lx, -250), (lx + 4, -40)], skin, 34)
        ell(ctx, lx + 6, -14, 38, 16)
        ink(ctx, skin)
    # knee-length saffron dhoti
    smooth(ctx, [(-112, -330), (112, -330), (124, -200), (72, -148), (0, -172), (-72, -148), (-124, -200)])
    ink(ctx, hexc("#E8862A"))
    line(ctx, [(122, -196), (72, -152), (0, -176), (-72, -152), (-122, -196)], hexc("#B5541A"), 9)
    # torso with a soft belly
    smooth(ctx, [(-106, -478), (-50, -500), (50, -500), (106, -478), (122, -400), (116, -330), (-116, -330),
                 (-122, -400)])
    ink(ctx, skin)
    sheen(ctx, 20, -390, 60, 40, 0.12)
    line(ctx, [(-80, -490), (-10, -420), (60, -370), (92, -338)], (1, 1, 1), 4)          # janeu
    for k in range(13):                                                                    # rudraksha mala
        u = k / 12
        circle(ctx, -60 + 120 * u, -500 + 80 * math.sin(math.pi * u), 8, hexc("#6B3410"))
    # white angavastram over the shoulders
    smooth(ctx, [(-128, -468), (-62, -506), (62, -506), (128, -468), (134, -410), (94, -436), (0, -466),
                 (-94, -436), (-134, -410)])
    ink(ctx, hexc("#F6EFE0"))
    # arms
    L, R = (-112, -468), (112, -468)
    if pose == "ask":
        arms = [(L, (-168, -420), (-172, -470)), (R, (190, -410), (262, -440 + 4 * math.sin(t * 2.2)))]
    elif pose == "point":
        arms = [(L, (-168, -420), (-172, -470)), (R, (190, -440), (200, -560))]
    else:
        arms = [(L, (-168, -420), (-172, -470)), (R, (150, -390), (150, -318))]
    for sh, el, hd in arms:
        limb(ctx, [sh, el, hd], skin, 40)
    hand(ctx, *arms[0][2], skin, 24)
    if pose == "ask":
        palm(ctx, *arms[1][2], skin, ang=1.35, s=0.85)
    elif pose == "point":
        hd = arms[1][2]
        line(ctx, [hd, (hd[0] + 4, hd[1] - 48)], OUTLINE, 14 + 4)
        line(ctx, [hd, (hd[0] + 4, hd[1] - 48)], skin, 14)
        hand(ctx, *hd, skin, 24)
    else:
        hand(ctx, *arms[1][2], skin, 24)
    # head
    rrect(ctx, -28, -548, 56, 56, 12)
    ink(ctx, skin)
    for side in (-1, 1):
        ell(ctx, side * 90, -610, 16, 26)
        ink(ctx, skin)
    ell(ctx, 0, -612, 92, 100)
    ink(ctx, skin)
    sheen(ctx, -30, -672, 40, 22, 0.2)
    smooth(ctx, [(-6, -706), (0, -742), (8, -760), (14, -744), (6, -706)])           # shikha
    ink(ctx, (1, 1, 1), 4)
    for side in (-1, 1):
        ell(ctx, side * 90, -655, 16, 26)
        ink(ctx, (1, 1, 1), 4)
        smooth(ctx, [(side * 12, -676), (side * 34, -688), (side * 60, -682), (side * 58, -674), (side * 34, -678)])
        ink(ctx, (1, 1, 1), 3)
    for k in (-1, 0, 1):
        line(ctx, [(-30, -692 + 8 * k), (30, -692 + 8 * k)], shade(skin, 0.85), 2.5, 0.7)
    line(ctx, [(0, -704), (0, -676)], hexc("#F2D7A0"), 9)
    circle(ctx, 0, -668, 5, RED_GEM)
    if mood == "smile":
        for side in (-1, 1):
            line(ctx, [(side * 34 - 16, -636), (side * 34, -646), (side * 34 + 16, -636)], OUTLINE, 6)
            line(ctx, [(side * 58, -632), (side * 66, -626)], shade(skin, 0.7), 3)
    else:
        for side in (-1, 1):
            eye(ctx, side * 34, -638, 17, 15, t, look=look, lid=0.35, skin=skin, seed=2, lash=False)
    ell(ctx, 0, -612, 13, 20)
    ink(ctx, shade(skin, 0.95), 4)
    # beard + moustache
    smooth(ctx, [(-86, -618), (-92, -560), (-70, -498), (-40, -452), (0, -432), (40, -452), (70, -498), (92, -560),
                 (86, -618), (60, -592), (30, -578), (0, -574), (-30, -578), (-60, -592)])
    ink(ctx, (0.97, 0.97, 0.95), 4)
    for k in range(5):
        line(ctx, [(-40 + 20 * k, -560), (-36 + 18 * k, -480)], hexc("#D9D6CF"), 3, 0.8)
    for side in (-1, 1):
        smooth(ctx, [(side * 2, -590), (side * 40, -598), (side * 64, -582), (side * 40, -574), (side * 2, -578)])
        ink(ctx, (1, 1, 1), 3.5)


# ============================================================ Barbarik

def barbarik(ctx, x, y, s, t, pose="stand", mood="fierce", draw_amt=0.0, arrows=3, look=(0.0, 0.0), flip=False,
             a=1.0, glow_a=0.0):
    """Barbarik, cartoon warrior. arrows = glowing arrows in the quiver (0..3); draw_amt 0..1 for pose='draw'.
    Returns nothing; use barbarik_hand() for the nocked arrow tip in pose 'draw'."""
    def draw():
        place(ctx, x, y, s, t, flip)
        if glow_a > 0:
            glow(ctx, 0, -500, 520, GOLD_HI, 0.6 * glow_a)
        _barbarik_body(ctx, t, pose, mood, draw_amt, arrows, look)
        ctx.restore()
    group(ctx, a, draw)


def divine_arrow(ctx, x, y, ang, L, t, a=1.0, trail=0.0):
    """Arrow centred on its head at (x, y), flying along ang (0 = right), with a blue-white divine glow."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    if trail > 0:
        g = cairo.LinearGradient(-L * 3, 0, 0, 0)
        g.add_color_stop_rgba(0, *DIVINE, 0)
        g.add_color_stop_rgba(1, *DIVINE, 0.55 * a * trail)
        ctx.rectangle(-L * 3, -10, L * 3, 20)
        ctx.set_source(g)
        ctx.fill()
    glow(ctx, 0, 0, 70, DIVINE, 0.7 * a)
    line(ctx, [(-L, 0), (-14, 0)], OUTLINE, 9, a)
    line(ctx, [(-L, 0), (-14, 0)], hexc("#F3E2BC"), 5, a)
    ctx.move_to(14, 0)
    ctx.line_to(-18, -13)
    ctx.line_to(-10, 0)
    ctx.line_to(-18, 13)
    ctx.close_path()
    ink(ctx, hexc("#E9FBFF"), 3, a)
    for sgn in (-1, 1):
        ctx.move_to(-L + 4, 0)
        ctx.line_to(-L - 14, sgn * 16)
        ctx.line_to(-L + 22, sgn * 4)
        ctx.close_path()
        ink(ctx, RED_GEM, 2.5, a)
    ctx.restore()


def bow(ctx, x, top, bottom, bulge, string_x=None, string_y=None, a=1.0):
    """Dhanush: limbs from (x, top) to (x, bottom) curving by bulge; the string optionally pulled to a point."""
    mid = (top + bottom) / 2
    pts = [(x, top), (x + bulge * 0.7, lerp(top, mid, 0.5)), (x + bulge, mid), (x + bulge * 0.7, lerp(mid, bottom, 0.5)),
           (x, bottom)]
    smooth(ctx, pts, closed=False)
    rgba(ctx, OUTLINE, a)
    ctx.set_line_width(20)
    ctx.stroke()
    smooth(ctx, pts, closed=False)
    rgba(ctx, hexc("#8E4B1C"), a)
    ctx.set_line_width(12)
    ctx.stroke()
    for yy in (lerp(top, mid, 0.85), lerp(mid, bottom, 0.15)):
        line(ctx, [(x + bulge * 0.95 - 10, yy), (x + bulge * 0.95 + 10, yy)], GOLD, 8, a)
    if string_x is None:
        line(ctx, [(x, top), (x, bottom)], (0.95, 0.92, 0.85), 3, a)
    else:
        line(ctx, [(x, top), (string_x, string_y), (x, bottom)], (0.95, 0.92, 0.85), 3, a)


def _barbarik_body(ctx, t, pose, mood, draw_amt, arrows, look):
    skin = BARBARIK_SKIN
    # long hair behind
    ell(ctx, 0, -690, 124, 122)
    ink(ctx, HAIR)
    for side in (-1, 1):
        smooth(ctx, [(side * 80, -700), (side * 132, -610), (side * 150, -520), (side * 122, -470), (side * 98, -560)])
        ink(ctx, HAIR)
    # quiver on the back with the glowing arrows
    ctx.save()
    ctx.translate(96, -560)
    ctx.rotate(0.42)
    for k in range(arrows):
        ax = -16 + 16 * k
        line(ctx, [(ax, -150), (ax, -250)], OUTLINE, 9)
        line(ctx, [(ax, -150), (ax, -250)], hexc("#F3E2BC"), 5)
        glow(ctx, ax, -262, 46, DIVINE, 0.75 + 0.2 * math.sin(t * 5 + k))
        ctx.move_to(ax, -282)
        ctx.line_to(ax - 10, -254)
        ctx.line_to(ax + 10, -254)
        ctx.close_path()
        ink(ctx, hexc("#E9FBFF"), 2.5)
    rrect(ctx, -36, -170, 72, 320, 22)
    ink(ctx, hexc("#7A4A22"))
    for yy in (-140, 110):
        rrect(ctx, -38, yy, 76, 18, 6)
        ink(ctx, GOLD, 3)
    ctx.restore()
    # legs + feet
    for side in (-1, 1):
        limb(ctx, [(side * 58, -330), (side * 66, -170), (side * 62, -34)], skin, 52)
        ell(ctx, side * 70, -14, 46, 18)
        ink(ctx, skin)
        line(ctx, [(side * 62 - 28, -46), (side * 62 + 28, -46)], GOLD, 9)
    # red dhoti, knee length, gold border
    smooth(ctx, [(-142, -352), (142, -352), (152, -236), (122, -150), (10, -172), (-122, -150), (-152, -236)])
    ink(ctx, hexc("#B3202A"))
    line(ctx, [(150, -232), (122, -156), (10, -178), (-122, -156), (-150, -232)], GOLD, 10)
    line(ctx, [(0, -350), (6, -180)], GOLD_DK, 6)
    # torso
    smooth(ctx, [(-150, -522), (-80, -548), (80, -548), (150, -522), (152, -440), (116, -352), (-116, -352),
                 (-152, -440)])
    ink(ctx, skin)
    # kavach (chest plate)
    smooth(ctx, [(-98, -524), (98, -524), (104, -442), (62, -400), (0, -390), (-62, -400), (-104, -442)])
    ink(ctx, GOLD)
    smooth(ctx, [(-70, -510), (70, -510), (74, -450), (40, -420), (0, -412), (-40, -420), (-74, -450)])
    rgba(ctx, GOLD_HI, 0.55)
    ctx.fill()
    for k in (-1, 1):
        line(ctx, [(k * 30, -500), (k * 56, -470), (k * 30, -440)], GOLD_DK, 4)
    gem(ctx, 0, -470, 20, RED_GEM)
    rrect(ctx, -126, -376, 252, 36, 10)
    ink(ctx, hexc("#3B2A18"))
    rrect(ctx, -26, -380, 52, 44, 8)
    ink(ctx, GOLD, 4)
    # arms per pose
    L, R = (-150, -515), (150, -515)
    if pose == "draw":
        hx = lerp(300, 70, ease_in_out(draw_amt))
        arms = [(L, (-90, -560), (hx, -560)), (R, (262, -545), (352, -552))]
    elif pose == "namaste":
        arms = [(L, (-120, -420), (-14, -480)), (R, (120, -420), (14, -480))]
    else:
        arms = [(L, (-205, -420), (-214, -330)), (R, (220, -430), (132, -362))]
    if pose == "stand":
        bow(ctx, -232, -700, -40, -70)
    for sh, el, hd in arms:
        limb(ctx, [sh, el], skin, 58)
        limb(ctx, [el, hd], skin, 50)
        mx, my = lerp(sh[0], el[0], 0.5), lerp(sh[1], el[1], 0.5)
        circle(ctx, mx, my, 32, GOLD)
        circle(ctx, mx, my, 25, skin)
        wx, wy = lerp(el[0], hd[0], 0.8), lerp(el[1], hd[1], 0.8)
        circle(ctx, wx, wy, 30, GOLD)
        circle(ctx, wx, wy, 22, skin)
    if pose == "namaste":
        smooth(ctx, [(0, -560), (24, -520), (22, -470), (0, -440), (-22, -470), (-24, -520)])
        ink(ctx, skin)
        line(ctx, [(0, -552), (0, -446)], shade(skin, 0.7), 3)
    else:
        for _, _, hd in arms:
            hand(ctx, *hd, skin, 30)
    for side in (-1, 1):                         # shoulder guards
        ell(ctx, side * 150, -520, 44, 32)
        ink(ctx, GOLD)
    if pose == "draw":
        hx = arms[0][2][0]
        bow(ctx, 352, -790, -320, 70, hx, -560)
        if arrows >= 0 and draw_amt > 0:
            divine_arrow(ctx, 430, -560, 0, 430 - hx, t)
    _barbarik_head(ctx, t, mood, look)


def _barbarik_head(ctx, t, mood, look):
    skin = BARBARIK_SKIN
    rrect(ctx, -34, -600, 68, 70, 14)
    ink(ctx, skin)
    for side in (-1, 1):
        ell(ctx, side * 100, -688, 18, 28)
        ink(ctx, skin)
        ctx.arc(side * 104, -650, 15, 0, math.tau)
        rgba(ctx, GOLD)
        ctx.set_line_width(6)
        ctx.stroke()
    ell(ctx, 0, -690, 100, 108)
    ink(ctx, skin)
    sheen(ctx, -36, -740, 38, 22, 0.16)
    for side in (-1, 1):                         # sideburns
        smooth(ctx, [(side * 96, -720), (side * 100, -660), (side * 84, -650), (side * 82, -712)])
        ink(ctx, HAIR, 3)
    calm = mood == "calm"
    for side in (-1, 1):
        eye(ctx, side * 38, -700, 24, 26, t, look=look, closed=calm, seed=3)
        if calm:
            line(ctx, [(side * 14, -738), (side * 38, -744), (side * 62, -738)], HAIR, 9)
        else:   # brows angled down toward the nose: focused warrior
            line(ctx, [(side * 12, -730), (side * 40, -742), (side * 66, -746)], HAIR, 11)
    ell(ctx, 0, -668, 12, 18)
    ink(ctx, shade(skin, 0.9), 3.5)
    # curled moustache
    for side in (-1, 1):
        smooth(ctx, [(side * 2, -640), (side * 34, -650), (side * 64, -642), (side * 82, -658), (side * 86, -676),
                     (side * 72, -666), (side * 54, -628), (side * 26, -628), (side * 2, -632)])
        ink(ctx, HAIR, 3)
    if calm:
        line(ctx, [(-22, -618), (0, -608), (22, -618)], hexc("#5A1E1E"), 5)
    else:
        line(ctx, [(-16, -616), (16, -616)], hexc("#5A1E1E"), 5)
    rrect(ctx, -5, -778, 10, 40, 4)                # red tilak
    rgba(ctx, hexc("#E2231A"))
    ctx.fill()
    # fringe + warrior mukut
    for k in range(9):
        circle(ctx, -88 + 22 * k, -768, 16, HAIR)
    smooth(ctx, [(-102, -796), (-84, -862), (-52, -812), (0, -904), (52, -812), (84, -862), (102, -796)], k=0.06)
    ink(ctx, GOLD, 5)
    rrect(ctx, -106, -806, 212, 38, 10)
    ink(ctx, GOLD, 5)
    gem(ctx, 0, -838, 16, RED_GEM)
    for gx in (-80, 80):
        gem(ctx, gx, -836, 8, hexc("#2D6FE0"))
    pearls(ctx, [(-96 + 16 * k, -787) for k in range(13)], 3.4)


# ============================================================ Khatu Shyam (sheesh roop)

def shyam(ctx, x, y, s, t, garland=1.0, a=1.0, aura=1.0):
    """The sheesh roop as worshipped at Khatu: dark face, wide eyes, tall mukut with peacock feathers and
    layered flower garlands. (x, y) = face centre."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s * (1 + 0.008 * math.sin(t * 2)))
        if aura > 0:
            glow(ctx, 0, -60, 620, GOLD, 0.45 * aura)
            ctx.save()
            ctx.rotate(t * 0.12)
            for k in range(24):
                ctx.move_to(0, 0)
                ang = k / 24 * math.tau
                ctx.arc(0, 0, 700, ang - 0.03, ang + 0.03)
                ctx.close_path()
            g = cairo.RadialGradient(0, 0, 120, 0, 0, 700)
            g.add_color_stop_rgba(0, *GOLD_HI, 0.3 * aura)
            g.add_color_stop_rgba(1, *GOLD_HI, 0)
            ctx.set_source(g)
            ctx.fill()
            ctx.restore()
        _shyam_face(ctx, t, garland)
        ctx.restore()
    group(ctx, a, draw)


def _flower(ctx, x, y, r, c, centre):
    for k in range(6):
        ang = k / 6 * math.tau
        ell(ctx, x + r * 0.5 * math.cos(ang), y + r * 0.5 * math.sin(ang), r * 0.55, r * 0.55)
    ink(ctx, c, 2)
    circle(ctx, x, y, r * 0.35, centre)


def _shyam_face(ctx, t, garland):
    face = SHYAM_FACE
    # peacock feathers fanned behind the mukut
    for ang in (-0.55, -0.25, 0.0, 0.25, 0.55):
        peacock_feather(ctx, ang * 40, -260, ang, 230, t + ang)
    # tall mukut
    smooth(ctx, [(-150, -110), (-138, -230), (-96, -200), (-70, -300), (-34, -252), (0, -360), (34, -252),
                 (70, -300), (96, -200), (138, -230), (150, -110)], k=0.07)
    ink(ctx, GOLD, 6)
    smooth(ctx, [(-110, -130), (-60, -230), (0, -300), (60, -230), (110, -130)], k=0.1)
    rgba(ctx, GOLD_HI, 0.55)
    ctx.fill()
    gem(ctx, 0, -230, 26, RED_GEM)
    for gx, gy, c in ((-70, -170, GREEN_GEM), (70, -170, GREEN_GEM), (-110, -150, hexc("#2D6FE0")),
                      (110, -150, hexc("#2D6FE0")), (-36, -150, RED_GEM), (36, -150, RED_GEM)):
        gem(ctx, gx, gy, 11, c)
    rrect(ctx, -150, -130, 300, 40, 12)
    ink(ctx, GOLD, 5)
    pearls(ctx, [(-140 + 14 * k, -110) for k in range(21)], 4)
    # pearl strings at the sides
    for side in (-1, 1):
        pearls(ctx, [(side * (150 - 2 * k), -100 + 16 * k) for k in range(12)], 5)
    # face
    ell(ctx, 0, 0, 122, 128)
    ink(ctx, face, 6)
    ell(ctx, 0, 0, 128, 134)
    rgba(ctx, GOLD, 0.8)
    ctx.set_line_width(4)
    ctx.stroke()
    sheen(ctx, -40, -50, 50, 30, 0.1)
    for side in (-1, 1):                                    # big gold kundal
        circle(ctx, side * 132, 30, 24, GOLD)
        circle(ctx, side * 132, 30, 12, RED_GEM)
        ell(ctx, side * 132, 74, 13, 20)
        ink(ctx, GOLD, 3)
    for side in (-1, 1):
        eye(ctx, side * 50, -10, 38, 32, t, iris=hexc("#120C08"), seed=5, rim=GOLD_DK)
        line(ctx, [(side * 18, -58), (side * 52, -70), (side * 90, -58)], GOLD_HI, 6)
    line(ctx, [(0, -10), (-6, 30), (6, 34)], shade(GOLD, 0.8), 4)
    for side in (-1, 1):                                    # moustache
        smooth(ctx, [(side * 2, 54), (side * 40, 46), (side * 74, 52), (side * 92, 36), (side * 96, 20),
                     (side * 84, 30), (side * 66, 64), (side * 30, 66), (side * 2, 62)])
        ink(ctx, hexc("#0B0B12"), 3, edge=GOLD_DK)
    line(ctx, [(-18, 84), (0, 92), (18, 84)], hexc("#C2283C"), 6)
    # tilak: white U with a red line
    line(ctx, [(-16, -112), (-12, -76), (0, -66), (12, -76), (16, -112)], WHITE, 8)
    line(ctx, [(0, -112), (0, -72)], hexc("#FF3B1F"), 7)
    if garland <= 0:
        return
    # garlands: jasmine, marigold, rose rows, then side strands
    rows = ((120, 230, 9, WHITE, GOLD), (150, 290, 15, hexc("#F59E0B"), hexc("#B45309")),
            (180, 350, 18, hexc("#C8102E"), hexc("#7A0A1C")))
    for k, (half, depth, r, c, cc) in enumerate(rows):
        n = int(16 * garland) + 2
        for i in range(n):
            u = i / max(n - 1, 1)
            gx = -half + 2 * half * u
            gy = 110 + (depth - 110) * math.sin(math.pi * u) * garland
            _flower(ctx, gx, gy, r, c, cc)
    for side in (-1, 1):
        for i in range(int(8 * garland)):
            _flower(ctx, side * 196, 120 + 34 * i, 16 if i % 2 else 13,
                    hexc("#F59E0B") if i % 2 else hexc("#C8102E"), GOLD_DK)


# ============================================================ props + scenery

LEAVES = []
for _i in range(30):                    # peepal canopy, in tree units (trunk foot at 0, 0)
    _a = rnd(_i, 41) * math.tau
    _r = math.sqrt(rnd(_i, 42))
    LEAVES.append((300 * _r * math.cos(_a), -560 + 190 * _r * math.sin(_a), (rnd(_i, 43) - 0.5) * 1.6,
                   0.9 + 0.35 * rnd(_i, 44)))
LEAVES.sort(key=lambda p: math.atan2(p[1] + 560, p[0]))


def leaf(ctx, x, y, ang, s, c=hexc("#3FAE4F"), mark=0.0, t=0.0):
    """Peepal leaf: broad heart base and a long drip tip. mark (0..1) = pierced by the divine arrow."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang + 0.05 * math.sin(t * 2 + x * 0.01))
    ctx.scale(s, s)
    smooth(ctx, [(0, 4), (-22, -6), (-34, 12), (-30, 36), (-16, 56), (0, 84), (16, 56), (30, 36), (34, 12), (22, -6)])
    ink(ctx, c, 3)
    line(ctx, [(0, -10), (0, 76)], shade(c, 0.7), 2.5)
    for k in range(3):
        for sgn in (-1, 1):
            line(ctx, [(0, 14 + 16 * k), (sgn * 20, 6 + 16 * k)], shade(c, 0.75), 1.6)
    if mark > 0:
        glow(ctx, 0, 30, 34, DIVINE, 0.8 * clamp(mark))
        circle(ctx, 0, 30, 6 * clamp(mark * 3), OUTLINE)
    ctx.restore()


def peepal(ctx, x, y, s, t, marks=None, hidden=None):
    """Peepal tree, trunk foot at (x, y). marks[i] = pierce amount for leaf i; hidden = set of leaf indexes
    not drawn on the tree. Returns the leaves' screen positions."""
    marks = marks or {}
    hidden = hidden or set()
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    smooth(ctx, [(-50, 0), (-36, -200), (-60, -380), (-20, -420), (20, -430), (60, -380), (40, -200), (56, 0)])
    ink(ctx, hexc("#6E4524"))
    for bx, by, ex, ey in ((-30, -380, -200, -560), (20, -400, 210, -580), (0, -420, -40, -700), (10, -420, 120, -690)):
        limb(ctx, [(bx, by), ((bx + ex) / 2, (by + ey) / 2 + 20), (ex, ey)], hexc("#6E4524"), 24)
    for k in range(7):                  # canopy masses behind the leaves
        cx = -220 + 75 * k
        ell(ctx, cx, -560 - 60 * math.sin(k * 1.3), 120, 100)
        rgba(ctx, hexc("#2B7A3A"), 0.9)
        ctx.fill()
    pos = []
    for i, (lx, ly, ang, ls) in enumerate(LEAVES):
        pos.append(ctx.user_to_device(lx, ly + 30 * ls))
        if i not in hidden:
            leaf(ctx, lx, ly, ang, ls * 1.15, mark=marks.get(i, 0.0), t=t)
    ctx.restore()
    return pos


def balance(ctx, x, y, s, tilt, t, labels=("JEET", "HAAR"), a=1.0):
    """Gold taraazu: tilt > 0 drops the left pan."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    line(ctx, [(0, 0), (0, 300)], OUTLINE, 22)
    line(ctx, [(0, 0), (0, 300)], GOLD, 14)
    ell(ctx, 0, 310, 90, 22)
    ink(ctx, GOLD)
    circle(ctx, 0, -10, 16, GOLD_HI)
    ctx.save()
    ctx.rotate(-tilt)
    line(ctx, [(-260, 0), (260, 0)], OUTLINE, 18)
    line(ctx, [(-260, 0), (260, 0)], GOLD, 10)
    for k, side in enumerate((-1, 1)):
        ctx.save()
        ctx.translate(side * 250, 0)
        ctx.rotate(tilt)
        line(ctx, [(0, 0), (-70, 160)], GOLD_DK, 3)
        line(ctx, [(0, 0), (70, 160)], GOLD_DK, 3)
        ctx.move_to(-90, 160)
        ctx.curve_to(-70, 220, 70, 220, 90, 160)
        ctx.close_path()
        ink(ctx, GOLD)
        text(ctx, labels[k], 0, 250, 46, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=OUTLINE, stroke_w=8)
        ctx.restore()
    ctx.restore()
    ctx.restore()


def diya(ctx, x, y, s, t, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    f = 1 + 0.12 * math.sin(t * 13) + 0.06 * math.sin(t * 29)
    glow(ctx, 0, -50, 160, hexc("#FFB347"), 0.55 * a)
    smooth(ctx, [(0, -40), (-14 * f, -64), (0, -110 * f), (14 * f, -64)])
    rgba(ctx, hexc("#FFD15C"), a)
    ctx.fill()
    smooth(ctx, [(0, -44), (-7, -60), (0, -84 * f), (7, -60)])
    rgba(ctx, (1, 1, 0.9), a)
    ctx.fill()
    ctx.move_to(-70, -36)
    ctx.curve_to(-60, 20, 60, 20, 70, -36)
    ctx.close_path()
    ink(ctx, hexc("#B4532A"), 5, a)
    ctx.restore()


def hill(ctx, x, y, w, h, c=hexc("#3D2A3F")):
    ctx.move_to(x - w, y)
    ctx.curve_to(x - w * 0.5, y - h * 0.2, x - w * 0.3, y - h, x, y - h)
    ctx.curve_to(x + w * 0.3, y - h, x + w * 0.5, y - h * 0.2, x + w, y)
    ctx.close_path()
    ink(ctx, c, 5)


def army(ctx, x0, x1, y, n, c, t, flag_c, seed=0, a=1.0):
    """Row of soldier silhouettes with spears and pennants between x0 and x1, feet on y."""
    for i in range(n):
        u = (i + 0.5) / n
        x = lerp(x0, x1, u) + 10 * math.sin(seed + i)
        h = 70 + 18 * rnd(i, seed)
        bob = 2 * math.sin(t * 3 + i)
        rgba(ctx, c, a)
        rrect(ctx, x - 13, y - h + bob, 26, h, 8)
        ctx.fill()
        circle(ctx, x, y - h - 12 + bob, 13, c, a)
        line(ctx, [(x + 16, y - 20 + bob), (x + 20, y - h - 60 + bob)], c, 4, a)
        if i % 3 == 0:
            ctx.move_to(x + 20, y - h - 60 + bob)
            ctx.line_to(x + 56 + 6 * math.sin(t * 5 + i), y - h - 48 + bob)
            ctx.line_to(x + 20, y - h - 36 + bob)
            ctx.close_path()
            rgba(ctx, flag_c, a)
            ctx.fill()


def petals(ctx, t, n=40, seed=0, a=1.0):
    """Marigold and rose petals drifting down."""
    for i in range(n):
        x = (rnd(i, seed + 1) * W + 40 * math.sin(t * 1.2 + i)) % W
        y = ((rnd(i, seed + 2) * H) + t * (140 + 80 * rnd(i, seed + 3))) % (H + 60) - 30
        c = hexc("#F59E0B") if i % 3 else hexc("#D7263D")
        ell(ctx, x, y, 12, 7, t * 2 + i)
        rgba(ctx, c, 0.9 * a)
        ctx.fill()


def sky(ctx, top, mid, bottom, mid_at=0.55):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *top)
    g.add_color_stop_rgb(mid_at, *mid)
    g.add_color_stop_rgb(1, *bottom)
    ctx.set_source(g)
    ctx.paint()


def stars(ctx, t, n=70, a=1.0):
    for i in range(n):
        tw = 0.5 + 0.5 * math.sin(t * (2 + 3 * rnd(i, 7)) + i)
        circle(ctx, rnd(i, 5) * W, rnd(i, 6) * 900, 1.5 + 2 * rnd(i, 8), (1, 1, 0.95), (0.3 + 0.6 * tw) * a)


def kailash(ctx, t, a=1.0):
    """Night Kailash: snow peak, crescent moon and a glowing trishul at the summit."""
    sky(ctx, hexc("#0B1033"), hexc("#27306B"), hexc("#3E2A5E"))
    stars(ctx, t, a=a)
    circle(ctx, 820, 250, 70, hexc("#FFF7D6"), a)
    circle(ctx, 850, 230, 62, hexc("#0F1440"), a)
    ctx.move_to(-50, 1250)
    ctx.line_to(260, 760)
    ctx.line_to(420, 520)
    ctx.line_to(540, 430)
    ctx.line_to(660, 520)
    ctx.line_to(830, 780)
    ctx.line_to(1130, 1250)
    ctx.close_path()
    rgba(ctx, hexc("#556C9E"), a)
    ctx.fill()
    ctx.move_to(420, 520)
    ctx.line_to(540, 430)
    ctx.line_to(660, 520)
    ctx.line_to(610, 560)
    ctx.line_to(560, 520)
    ctx.line_to(510, 580)
    ctx.line_to(470, 540)
    ctx.close_path()
    rgba(ctx, (0.96, 0.97, 1.0), a)
    ctx.fill()
    trishul(ctx, 540, 400, 0.9, t, a)


def trishul(ctx, x, y, s, t, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    glow(ctx, 0, -120, 260, hexc("#BFE6FF"), 0.6 * a)
    line(ctx, [(0, 40), (0, -230)], hexc("#DDE6F2"), 12, a)
    for sgn in (-1, 1):
        smooth(ctx, [(0, -150), (sgn * 60, -170), (sgn * 66, -250), (sgn * 52, -200), (0, -186)], k=0.1)
        rgba(ctx, hexc("#DDE6F2"), a)
        ctx.fill()
    ctx.move_to(0, -300)
    ctx.line_to(-16, -220)
    ctx.line_to(16, -220)
    ctx.close_path()
    ctx.fill()
    ell(ctx, 0, -120, 26, 18)        # damru tied to the shaft
    ink(ctx, hexc("#8A5A2B"), 3, a)
    ctx.restore()


def ribbon(ctx, label, x, y, u, c=hexc("#7A1424"), size=72, sub=None, rot=-0.03):
    """Maroon ribbon banner with gold edges that unfurls in (u = seconds since it appears)."""
    if u <= 0:
        return
    k = ease_out_back(clamp(u / 0.35), 1.4)
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(k, k)
    from engine import text_width
    w = text_width(ctx, label, size, font=CAPTION_FONT, bold=False) + 110
    h = size * 1.45 + (size * 0.55 if sub else 0)
    for sgn in (-1, 1):                  # folded tails
        ctx.move_to(sgn * (w / 2 - 20), -h / 2 + 24)
        ctx.line_to(sgn * (w / 2 + 50), -h / 2 + 24)
        ctx.line_to(sgn * (w / 2 + 20), 12)
        ctx.line_to(sgn * (w / 2 + 50), h / 2 + 24)
        ctx.line_to(sgn * (w / 2 - 20), h / 2 + 24)
        ctx.close_path()
        ink(ctx, shade(c, 0.7), 4)
    rrect(ctx, -w / 2, -h / 2, w, h, 14)
    ink(ctx, c, 5)
    rrect(ctx, -w / 2 + 10, -h / 2 + 10, w - 20, h - 20, 10)
    rgba(ctx, GOLD, 0.95)
    ctx.set_line_width(4)
    ctx.stroke()
    ty = -h / 2 + size * 0.78
    text(ctx, label, 0, ty, size, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=OUTLINE, stroke_w=8)
    if sub:
        text(ctx, sub, 0, ty + size * 0.78, size * 0.42, (1, 0.95, 0.85), font=CAPTION_FONT, bold=False)
    ctx.restore()


# ============================================================ Chhathi Maiya (Shashthi Devi)

DEVI_SKIN = hexc("#F2BE8E")
SAREE_RED = hexc("#C8102E")


def lotus(ctx, x, y, s, c=hexc("#F48FB1"), a=1.0):
    """Open lotus, centre of its base at (x, y)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for ang in (-1.0, -0.5, 0.5, 1.0, 0.0):
        ctx.save()
        ctx.rotate(ang * 0.8)
        smooth(ctx, [(0, 0), (-16, -24), (0, -58), (16, -24)])
        ink(ctx, c if ang else shade(c, 1.1), 3, a)
        ctx.restore()
    ell(ctx, 0, -6, 20, 8)
    ink(ctx, GOLD, 2.5, a)
    ctx.restore()


def devi(ctx, x, y, s, t, pose="bless", look=(0.0, 0.0), flip=False, a=1.0, aura=True):
    """Chhathi Maiya (Shashthi Devi), cartoon: red saree with gold border, gold mukut, sindoor, nath,
    a lotus in one hand. Poses: bless (abhaya hand) / touch (reaching down to a child) / open (both hands blessing)."""
    def draw():
        place(ctx, x, y, s, t, flip)
        if aura:
            halo(ctx, 0, -650, 170, t, c=hexc("#FFB347"))
        _devi_body(ctx, t, pose, look)
        ctx.restore()
    group(ctx, a, draw)


def _devi_body(ctx, t, pose, look):
    skin = DEVI_SKIN
    hair = hexc("#1A0F14")
    ell(ctx, 0, -655, 112, 118)                         # hair behind
    ink(ctx, hair)
    for side in (-1, 1):
        smooth(ctx, [(side * 70, -680), (side * 124, -560), (side * 128, -380), (side * 84, -372), (side * 82, -560)])
        ink(ctx, hair)
    for fx in (-48, 48):                                 # feet + payal
        ell(ctx, fx, -12, 40, 16)
        ink(ctx, skin)
        line(ctx, [(fx - 26, -26), (fx, -20), (fx + 26, -26)], GOLD, 6)
    smooth(ctx, [(-108, -345), (108, -345), (148, -160), (170, -26), (-170, -26), (-148, -160)])   # saree
    ink(ctx, SAREE_RED)
    line(ctx, [(-168, -34), (168, -34)], GOLD, 14)
    for fx in (-30, -8, 14, 36):                         # front pleats
        line(ctx, [(fx * 0.5, -330), (fx, -40)], GOLD_DK, 3, 0.8)
    smooth(ctx, [(-98, -425), (98, -425), (108, -345), (-108, -345)])                       # midriff
    ink(ctx, skin)
    smooth(ctx, [(-106, -500), (-56, -522), (56, -522), (106, -500), (102, -425), (-102, -425)])  # blouse
    ink(ctx, hexc("#1F7A4D"))
    smooth(ctx, [(-112, -506), (-66, -524), (112, -372), (104, -340), (52, -340)], k=0.08)         # pallu
    ink(ctx, SAREE_RED, 5)
    line(ctx, [(-66, -520), (110, -372)], GOLD, 7)
    rrect(ctx, -110, -360, 220, 24, 10)
    ink(ctx, GOLD, 4)
    gem(ctx, 0, -348, 8, GREEN_GEM)
    line(ctx, [(-62, -518), (-30, -488), (0, -478), (30, -488), (62, -518)], GOLD, 10)          # necklace
    for k in range(5):
        gem(ctx, -40 + 20 * k, -488 + 8 * (k in (1, 2, 3)) - 4 * (k == 2), 6, RED_GEM if k % 2 else GREEN_GEM)
    rrect(ctx, -30, -566, 60, 60, 14)
    ink(ctx, skin)
    _devi_head(ctx, t, look, hair)
    L, R = (-112, -492), (112, -492)
    if pose == "touch":
        arms = [(L, (-160, -400), (-150, -320)), (R, (200, -420), (270, -360))]
    elif pose == "open":
        arms = [(L, (-200, -440), (-185, -575)), (R, (200, -440), (185, -575))]
    else:
        arms = [(L, (-160, -400), (-150, -320)), (R, (195, -425), (176, -566))]
    for sh, el, hd in arms:
        limb(ctx, [sh, el], skin, 44)
        limb(ctx, [el, hd], skin, 38)
        wx, wy = lerp(el[0], hd[0], 0.8), lerp(el[1], hd[1], 0.8)
        for k in range(3):                               # red-and-gold bangles
            circle(ctx, wx + k * (hd[0] - el[0]) * 0.03, wy + k * (hd[1] - el[1]) * 0.03, 22,
                   (RED_GEM, GOLD, RED_GEM)[k])
        circle(ctx, wx, wy, 15, skin)
    if pose == "touch":
        palm(ctx, *arms[1][2], skin, ang=2.3, s=0.85)
    elif pose == "open":
        for _, _, hd in arms:
            palm(ctx, *hd, skin, s=0.85)
    else:
        palm(ctx, *arms[1][2], skin, s=0.85)
    if pose != "open":
        lh = arms[0][2]
        lotus(ctx, lh[0], lh[1] - 26, 0.9)
        hand(ctx, *lh, skin, 24)


def _devi_head(ctx, t, look, hair):
    skin = DEVI_SKIN
    for side in (-1, 1):
        ell(ctx, side * 88, -640, 15, 24)
        ink(ctx, skin)
        circle(ctx, side * 92, -606, 11, GOLD)                    # jhumka
        ctx.move_to(side * 92 - 16, -596)
        ctx.curve_to(side * 92 - 16, -566, side * 92 + 16, -566, side * 92 + 16, -596)
        ctx.close_path()
        ink(ctx, GOLD, 3)
        pearls(ctx, [(side * 92 - 12 + 6 * k, -566) for k in range(5)], 3)
    ell(ctx, 0, -640, 92, 104)
    ink(ctx, skin)
    sheen(ctx, -32, -690, 34, 20, 0.2)
    ell(ctx, 0, -728, 94, 34)                              # hair over the forehead, parted
    ink(ctx, hair)
    line(ctx, [(0, -760), (0, -716)], hexc("#E2231A"), 7)   # sindoor in the parting
    for side in (-1, 1):
        eye(ctx, side * 34, -646, 24, 25, t, look=look, iris=hexc("#3A1E12"), seed=6)
        line(ctx, [(side * 12, -680), (side * 36, -690), (side * 60, -682)], hair, 5)
        ell(ctx, side * 50, -606, 18, 10)
        rgba(ctx, hexc("#FF7AA8"), 0.35)
        ctx.fill()
    circle(ctx, 0, -700, 9, hexc("#E2231A"))                # bindi
    line(ctx, [(2, -636), (-5, -616), (5, -612)], shade(skin, 0.75), 4)
    ctx.new_sub_path()
    ctx.arc(20, -612, 11, -0.6, 3.6)                         # nath
    rgba(ctx, GOLD)
    ctx.set_line_width(4)
    ctx.stroke()
    ctx.move_to(-20, -590)
    ctx.curve_to(-8, -576, 8, -576, 20, -590)
    ctx.curve_to(8, -584, -8, -584, -20, -590)
    ctx.close_path()
    ink(ctx, hexc("#C2283C"), 3)
    smooth(ctx, [(-96, -748), (-80, -806), (-44, -790), (0, -846), (44, -790), (80, -806), (96, -748)], k=0.07)
    ink(ctx, GOLD, 5)
    rrect(ctx, -98, -760, 196, 30, 10)
    ink(ctx, GOLD, 4)
    gem(ctx, 0, -800, 14, RED_GEM)
    for gx in (-60, 60):
        gem(ctx, gx, -786, 7, GREEN_GEM)
    pearls(ctx, [(-88 + 12 * k, -745) for k in range(15)], 3)


# ============================================================ Surya Dev

SURYA_SKIN = hexc("#E39A55")


def sun_disc(ctx, x, y, r, t, a=1.0, rays=24):
    """Sun with turning triangular rays and a soft corona."""
    glow(ctx, x, y, r * 2.6, hexc("#FFB347"), 0.6 * a)
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(t * 0.15)
    for k in range(rays):
        ang = k / rays * math.tau
        L = r * (1.45 if k % 2 else 1.25)
        ctx.move_to(r * 0.9 * math.cos(ang - 0.09), r * 0.9 * math.sin(ang - 0.09))
        ctx.line_to(L * math.cos(ang), L * math.sin(ang))
        ctx.line_to(r * 0.9 * math.cos(ang + 0.09), r * 0.9 * math.sin(ang + 0.09))
        ctx.close_path()
    rgba(ctx, hexc("#FFC94A"), a)
    ctx.fill()
    ctx.restore()
    g = cairo.RadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r)
    g.add_color_stop_rgba(0, 1, 0.97, 0.75, a)
    g.add_color_stop_rgba(1, 1, 0.62, 0.15, a)
    ctx.new_sub_path()
    ctx.arc(x, y, r, 0, math.tau)
    ctx.set_source(g)
    ctx.fill()


def surya(ctx, x, y, s, t, a=1.0):
    """Surya Dev, cartoon: rayed sun disc behind, gold kirit mukut, a lotus raised in each hand."""
    def draw():
        place(ctx, x, y, s, t)
        sun_disc(ctx, 0, -650, 230, t)
        _surya_body(ctx, t)
        ctx.restore()
    group(ctx, a, draw)


def _surya_body(ctx, t):
    skin = SURYA_SKIN
    for fx in (-50, 50):
        ell(ctx, fx, -14, 42, 17)
        ink(ctx, skin)
    smooth(ctx, [(-116, -345), (116, -345), (136, -200), (150, -40), (60, -30), (0, -60), (-60, -30), (-150, -40),
                 (-136, -200)])
    ink(ctx, hexc("#D7263D"))
    line(ctx, [(148, -44), (60, -34), (0, -64), (-60, -34), (-148, -44)], GOLD, 12)
    smooth(ctx, [(-122, -500), (-60, -522), (60, -522), (122, -500), (128, -430), (100, -340), (-100, -340),
                 (-128, -430)])
    ink(ctx, skin)
    smooth(ctx, [(-96, -520), (96, -520), (100, -440), (0, -405), (-100, -440)])          # gold kavach
    ink(ctx, GOLD)
    gem(ctx, 0, -458, 16, RED_GEM)
    rrect(ctx, -114, -366, 228, 32, 12)
    ink(ctx, GOLD, 5)
    rrect(ctx, -30, -566, 60, 62, 14)
    ink(ctx, skin)
    for side in (-1, 1):
        ell(ctx, side * 98, -640, 18, 28)
        ink(ctx, skin)
        circle(ctx, side * 104, -604, 14, GOLD)
    ell(ctx, 0, -640, 100, 110)
    ink(ctx, skin)
    sheen(ctx, -36, -690, 40, 24, 0.18)
    for side in (-1, 1):
        eye(ctx, side * 38, -646, 23, 26, t, iris=hexc("#5A2A0A"), seed=7)
        line(ctx, [(side * 14, -686), (side * 38, -696), (side * 62, -688)], HAIR, 7)
    line(ctx, [(2, -640), (-6, -618), (5, -613)], shade(skin, 0.7), 4)
    ctx.move_to(-22, -594)
    ctx.curve_to(-8, -578, 8, -578, 22, -594)
    ctx.curve_to(8, -588, -8, -588, -22, -594)
    ctx.close_path()
    ink(ctx, hexc("#B5283C"), 3)
    line(ctx, [(0, -722), (0, -692)], hexc("#E2231A"), 8)
    for k in range(9):
        circle(ctx, -88 + 22 * k, -736, 17, HAIR)
    smooth(ctx, [(-98, -770), (-84, -850), (-50, -820), (-30, -900), (0, -950), (30, -900), (50, -820), (84, -850),
                 (98, -770)], k=0.06)                                                        # tall kirit mukut
    ink(ctx, GOLD, 5)
    smooth(ctx, [(-50, -790), (-24, -880), (0, -920), (24, -880), (50, -790)], k=0.08)
    rgba(ctx, GOLD_HI, 0.6)
    ctx.fill()
    rrect(ctx, -102, -778, 204, 36, 10)
    ink(ctx, GOLD, 5)
    gem(ctx, 0, -840, 18, RED_GEM)
    for side in (-1, 1):                                    # arms raised, a lotus in each hand
        sh, el, hd = (side * 118, -490), (side * 190, -420), (side * 178, -566)
        limb(ctx, [sh, el], skin, 50)
        limb(ctx, [el, hd], skin, 44)
        circle(ctx, lerp(el[0], hd[0], 0.78), lerp(el[1], hd[1], 0.78), 26, GOLD)
        lotus(ctx, hd[0], hd[1] - 22, 1.1)
        hand(ctx, *hd, skin)


# ============================================================ Raja, baby, vrati, soop, yagya

def baby(ctx, x, y, s, t, awake=False, a=1.0):
    """Baby in a swaddle, face at the top. awake=True: big eyes, open laugh and a waving hand."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if awake:
        glow(ctx, 0, -20, 150, GOLD_HI, 0.5 * a)
    ell(ctx, 0, 10, 62, 82, -0.2)
    ink(ctx, hexc("#FFF3E0"), 4, a)
    line(ctx, [(-50, 20), (50, -10)], hexc("#F48FB1"), 8, a)
    ell(ctx, -6, -48, 38, 36)
    ink(ctx, hexc("#F6C9A0"), 4, a)
    if awake:
        for side in (-1, 1):
            ell(ctx, -6 + side * 14, -54, 7, 8)
            ink(ctx, (0.1, 0.06, 0.05), 1.5, a)
            circle(ctx, -6 + side * 14 - 2, -57, 2.4, (1, 1, 1), a)
        ctx.move_to(-18, -38)
        ctx.curve_to(-12, -22, 0, -22, 6, -38)
        ctx.close_path()
        ink(ctx, hexc("#C2283C"), 2, a)
        wave = 0.4 * math.sin(t * 9)
        hx, hy = 40 + 10 * math.cos(wave), -60 + 10 * math.sin(wave)
        ell(ctx, hx, hy, 13, 13)
        ink(ctx, hexc("#F6C9A0"), 3, a)
    else:
        for side in (-1, 1):
            line(ctx, [(-6 + side * 14 - 7, -52), (-6 + side * 14, -48), (-6 + side * 14 + 7, -52)], OUTLINE, 3, a)
        line(ctx, [(-12, -34), (0, -34)], hexc("#C2283C"), 3, a)
    ell(ctx, -6, -80, 26, 12)
    ink(ctx, hexc("#F48FB1"), 3, a)
    ctx.restore()


def raja(ctx, x, y, s, t, pose="stand", mood="sad", child=None, a=1.0, flip=False):
    """King (Raja Priyavrat), cartoon: gold mukut with a white kalgi, curled moustache, purple angarkha.
    pose 'hold' cradles a baby (child = None / 'asleep' / 'awake'); mood sad (tear) / happy."""
    def draw():
        place(ctx, x, y, s, t, flip)
        _raja_body(ctx, t, pose, mood, child)
        ctx.restore()
    group(ctx, a, draw)


def _raja_body(ctx, t, pose, mood, child):
    skin = hexc("#D9965F")
    robe = hexc("#5B2A86")
    for side in (-1, 1):
        limb(ctx, [(side * 50, -260), (side * 54, -40)], hexc("#F3EDE0"), 46)
        ell(ctx, side * 60, -16, 44, 17)
        ink(ctx, hexc("#B5283C"))
    smooth(ctx, [(-124, -520), (-60, -546), (60, -546), (124, -520), (134, -400), (156, -230), (-156, -230),
                 (-134, -400)])
    ink(ctx, robe)
    line(ctx, [(-154, -236), (154, -236)], GOLD, 12)
    line(ctx, [(0, -540), (0, -240)], GOLD, 6)
    rrect(ctx, -126, -396, 252, 30, 10)
    ink(ctx, hexc("#E0502A"), 4)
    for k in range(3):                                     # pearl malas
        line(ctx, [(-60 + 6 * k, -536 + 10 * k), (0, -476 + 14 * k), (60 - 6 * k, -536 + 10 * k)], WHITE, 5)
    gem(ctx, 0, -446, 12, GREEN_GEM)
    rrect(ctx, -32, -590, 64, 64, 14)
    ink(ctx, skin)
    L, R = (-120, -510), (120, -510)
    if pose == "hold":
        arms = [(L, (-150, -420), (-30, -400)), (R, (150, -420), (40, -450))]
    else:
        arms = [(L, (-160, -420), (-150, -330)), (R, (160, -420), (150, -330))]
    for sh, el, hd in arms:
        limb(ctx, [sh, el], robe, 54)
    if pose == "hold" and child:
        baby(ctx, 0, -450, 1.0, t, awake=(child == "awake"))
    for sh, el, hd in arms:
        limb(ctx, [el, hd], robe, 48)
        hand(ctx, *hd, skin, 26)
    for side in (-1, 1):
        ell(ctx, side * 96, -680, 17, 27)
        ink(ctx, skin)
    ell(ctx, 0, -680, 98, 106)
    ink(ctx, skin)
    sheen(ctx, -34, -728, 36, 22, 0.16)
    sad = mood == "sad"
    for side in (-1, 1):
        if sad:
            eye(ctx, side * 36, -690, 20, 18, t, look=(0, 0.9), lid=0.45, skin=skin, seed=8, lash=False)
            line(ctx, [(side * 12, -722), (side * 36, -716), (side * 60, -708)], HAIR, 8)   # brows lifted inside
        else:
            line(ctx, [(side * 36 - 18, -686), (side * 36, -698), (side * 36 + 18, -686)], OUTLINE, 6)
            line(ctx, [(side * 14, -726), (side * 36, -734), (side * 60, -728)], HAIR, 8)
    if sad:
        u = (t * 0.6) % 1
        ell(ctx, -40, -668 + 60 * u, 6, 9)
        ink(ctx, hexc("#BFE6FF"), 2, 1 - u)
    ell(ctx, 0, -662, 11, 17)
    ink(ctx, shade(skin, 0.92), 3)
    for side in (-1, 1):
        smooth(ctx, [(side * 2, -636), (side * 30, -644), (side * 56, -638), (side * 70, -652), (side * 72, -664),
                     (side * 62, -656), (side * 46, -626), (side * 22, -626), (side * 2, -630)])
        ink(ctx, HAIR, 3)
    if not sad:
        line(ctx, [(-18, -612), (0, -602), (18, -612)], hexc("#5A1E1E"), 5)
    line(ctx, [(0, -760), (0, -732)], hexc("#E2231A"), 7)
    rrect(ctx, -102, -796, 204, 40, 12)
    ink(ctx, GOLD, 5)
    smooth(ctx, [(-96, -792), (-70, -850), (0, -880), (70, -850), (96, -792)], k=0.1)
    ink(ctx, GOLD, 5)
    gem(ctx, 0, -830, 14, RED_GEM)
    smooth(ctx, [(30, -870), (60, -960), (84, -990), (70, -930), (50, -868)])       # kalgi plume
    ink(ctx, WHITE, 3)
    pearls(ctx, [(-92 + 13 * k, -776) for k in range(15)], 3)


def soop(ctx, x, y, s, t, a=1.0):
    """Bamboo soop for the arghya: banana, coconut, thekua, apple and a lit diya."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(-110, -20)
    ctx.curve_to(-100, 40, 100, 40, 110, -20)
    ctx.line_to(80, -40)
    ctx.line_to(-80, -40)
    ctx.close_path()
    ink(ctx, hexc("#D8B26A"), 4, a)
    for k in range(6):
        line(ctx, [(-90 + 36 * k, -36), (-84 + 34 * k, 20)], hexc("#A9823E"), 2, a)
    ell(ctx, -50, -52, 30, 26)
    ink(ctx, hexc("#7A4A22"), 3, a)                       # coconut
    for k in range(3):                                     # bananas
        ctx.save()
        ctx.translate(20 + 10 * k, -60)
        ctx.rotate(-0.5 + 0.2 * k)
        ell(ctx, 0, 0, 12, 40)
        ink(ctx, hexc("#F5D33F"), 3, a)
        ctx.restore()
    for tx in (-80, 70):                                   # thekua
        ell(ctx, tx, -38, 22, 14)
        ink(ctx, hexc("#B5651D"), 2.5, a)
    circle(ctx, -10, -42, 16, hexc("#D7263D"), a)
    f = 1 + 0.15 * math.sin(t * 13)
    glow(ctx, 90, -80, 60, hexc("#FFB347"), 0.6 * a)
    smooth(ctx, [(90, -62), (82, -74), (90, -100 * f), (98, -74)])
    rgba(ctx, hexc("#FFD15C"), a)
    ctx.fill()
    ctx.restore()


def vrati(ctx, x, y, s, t, lift=1.0, a=1.0):
    """A woman keeping the Chhath vrat, standing waist-deep (y = water line), soop raised to the sun.
    Yellow saree with a red border, long orange sindoor from forehead to parting, pallu over the head."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    skin = hexc("#C98B5E")
    saree = hexc("#F2A900")
    smooth(ctx, [(-90, 0), (-92, -160), (-60, -200), (60, -200), (92, -160), (90, 0)])
    ink(ctx, saree, 5, a)
    line(ctx, [(-60, -196), (80, -20)], hexc("#C8102E"), 10, a)
    hy = lerp(-200, -360, lift)
    for side in (-1, 1):
        limb(ctx, [(side * 70, -180), (side * 96, -240), (side * 60, hy)], skin, 30)
        for k in range(2):
            circle(ctx, side * (78 - 6 * k), lerp(-240, hy, 0.7) + 8 * k, 14, (hexc("#C8102E"), GOLD)[k], a)
    ell(ctx, 0, -250, 50, 58)
    ink(ctx, skin, 5, a)
    smooth(ctx, [(0, -326), (-64, -290), (-70, -210), (-52, -196), (-46, -270), (46, -270), (52, -196), (70, -210),
                 (64, -290)])
    ink(ctx, saree, 4, a)
    line(ctx, [(-64, -290), (0, -326), (64, -290)], hexc("#C8102E"), 7, a)
    line(ctx, [(0, -300), (0, -262)], hexc("#FF6A00"), 7, a)           # long orange sindoor
    for side in (-1, 1):
        line(ctx, [(side * 20 - 9, -252), (side * 20, -246), (side * 20 + 9, -252)], OUTLINE, 4, a)
    line(ctx, [(-8, -226), (8, -226)], hexc("#B5283C"), 4, a)
    soop(ctx, 0, hy - 20, 0.75, t, a)
    ctx.restore()


def yagya_kund(ctx, x, y, s, t, a=1.0):
    """Square havan kund with a leaping fire."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    glow(ctx, 0, -80, 260, hexc("#FF8A2A"), 0.6 * a)
    for k in range(5):
        f = 1 + 0.18 * math.sin(t * (9 + k) + k * 1.7)
        dx = (k - 2) * 28
        smooth(ctx, [(dx - 26, -20), (dx - 14 * f, -70), (dx, -150 * f * (1 - 0.15 * abs(k - 2))), (dx + 14 * f, -70),
                     (dx + 26, -20)])
        rgba(ctx, (hexc("#FF5A1F"), hexc("#FFB347"), hexc("#FFE38A"))[k % 3], 0.9 * a)
        ctx.fill()
    for k in range(3):
        rrect(ctx, -120 + 10 * k, -20 + 22 * k, 240 - 20 * k, 24, 4)
        ink(ctx, hexc("#B5541A") if k % 2 else hexc("#C9663A"), 3, a)
    ctx.restore()


def silhouette(ctx, draw, c=hexc("#1A0A10"), a=1.0):
    """Draw anything as a flat backlit silhouette in colour c."""
    ctx.push_group()
    draw()
    pattern = ctx.pop_group()
    rgba(ctx, c, a)
    ctx.mask(pattern)
