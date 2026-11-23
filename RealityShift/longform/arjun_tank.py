"""Reality Shift long-form (16:9, ~7-8 min): Arjun tank - desi tank jise army ne poora nahi apnaya. Arjun ya T-90.

A DEBATE video: both sides fairly (Arjun's fans vs the army's logic), engineering / cost / doctrine only.
9 chapters: hook paradox, 1974 origin, what Arjun is, the 2010 desert trials, the weight problem (bridges, rail,
logistics), the T-90 Bhishma side, Mk1A + the engine problem, the future (FRCV), the A/B comment question.

Fresh vector scenes (no maps): side-view Arjun / T-90 / T-72 / FRCV tanks, desert duel, blueprint callouts,
weighbridge, canal bridge, rail wagon, terrain panels, fleet pictograms, factory line, engine bay, calendar.

    python make_long.py arjun_tank --kiki-export | --preview | (render)
"""

import math

import cairo

from core.engine import (circle, clamp, ease_in_out, ease_out_back, ease_out_cubic, glow, hexc, lerp, line, rgba,
                         rnd, rrect, text, text_width)
from core.longform import H, W

TITLE = "Arjun Tank: Desi Tank Jise Army Ne Poora Nahi Apnaya"
MUSIC_STYLE = "tension"
MUSIC_BPM = 88
MUSIC_SEED = 2311
MUSIC_LO, MUSIC_HI = 0.06, 0.15
KIKI_TEMPO = 1.0          # the user sets 1.10x inside KikiVoice

# ------------------------------------------------------------ palette
GOLD = hexc("#FFC845")
RED = hexc("#FF4040")
CYAN = hexc("#5CE1E6")
TEAL = hexc("#46E0B0")
SAFFRON = hexc("#FF9933")
GREEN = hexc("#2FBF5B")
STEEL = hexc("#9AA8B8")
WHITE = (0.95, 0.96, 0.98)
INK = (0.02, 0.03, 0.05)
SAND_TANK = hexc("#B8955A")      # Arjun: desert sand
SAND_1A = hexc("#9C8452")        # Arjun Mk1A: darker sand
OLIVE_TANK = hexc("#56633A")     # T-90: olive green
T72_C = hexc("#6B6F55")          # T-72: grey olive
FRCV_C = hexc("#4B5A6E")         # FRCV: blue grey
BP = hexc("#0A2440")             # blueprint background
BP_LINE = hexc("#7CC4FF")
MONO = "Consolas"
IMPACT = "Impact"
GROUND = 800

ARJ_C = GOLD                     # Arjun side colour in every comparison
T90_C = CYAN                     # T-90 side colour

HOT = {"ARJUN": GOLD, "T-90": CYAN, "BHISHMA": CYAN, "T-72": CYAN, "124": GOLD, "118": GOLD, "1974": GOLD,
       "1989": GOLD, "1995": GOLD, "2000": GOLD, "2004": GOLD, "2010": GOLD, "2013": GOLD, "2015": GOLD,
       "2019": GOLD, "2020": GOLD, "2021": GOLD, "68": RED, "58.5": GOLD, "46": CYAN, "20": RED, "70": RED,
       "120": GOLD, "125": CYAN, "1400": GOLD, "1500": GOLD, "72": GOLD, "14": GOLD, "464": CYAN, "1770": GOLD,
       "7,523": GOLD, "307": GOLD, "15.5": GOLD, "75": RED, "VAZAN": RED, "TAN": RED, "PUL": RED, "INJAN": RED,
       "ENGINE": RED, "DESI": SAFFRON, "MK1A": GOLD, "FRCV": TEAL, "DATRAN": TEAL, "CAG": RED, "KANCHAN": GOLD,
       "REPORTS": STEEL, "MUTABIK": STEEL, "RAJASTHAN": SAFFRON, "MAHAJAN": SAFFRON, "LADAKH": TEAL,
       "PUNJAB": TEAL, "DRDO": SAFFRON, "AVADI": SAFFRON, "A": GOLD, "B": CYAN, "COMMENT": GOLD, "JAI": SAFFRON,
       "HIND": GREEN, "BHAI": GOLD, "SUBSCRIBE": RED}


# ============================================================ small helpers

def shade(c, k):
    return tuple(min(1, x * k) for x in c)


def vignette(ctx, k=0.6):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, W * 0.62)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, k)
    ctx.set_source(g)
    ctx.paint()


def tag(ctx, s, x, y, c, size=28, a=1.0, anchor="c", fill=INK):
    """Boxed monospace label centred (or left/right anchored) on x, y."""
    if a <= 0:
        return
    tw = text_width(ctx, s, size, font=MONO)
    bx = x - tw / 2 - 14 if anchor == "c" else (x - 14 if anchor == "l" else x - tw - 14)
    rrect(ctx, bx, y - size * 0.8, tw + 28, size * 1.6, 8)
    rgba(ctx, fill, 0.85 * a)
    ctx.fill_preserve()
    rgba(ctx, c, 0.9 * a)
    ctx.set_line_width(2)
    ctx.stroke()
    text(ctx, s, bx + 14, y, size, c, font=MONO, anchor="l", a=a)


def big(ctx, s, x, y, size, c, a=1.0, anchor="c"):
    text(ctx, s, x, y, size, c, font=IMPACT, a=a, anchor=anchor, stroke=(0, 0, 0), stroke_w=max(4, size / 14))


def tick(ctx, x, y, r, a=1.0):
    circle(ctx, x, y, r, GREEN, a)
    line(ctx, [(x - r * 0.45, y + 0.02 * r), (x - r * 0.1, y + r * 0.38), (x + r * 0.5, y - r * 0.35)], WHITE,
         r * 0.22, a)


def cross(ctx, x, y, r, a=1.0):
    circle(ctx, x, y, r, RED, a)
    d = r * 0.42
    line(ctx, [(x - d, y - d), (x + d, y + d)], WHITE, r * 0.22, a)
    line(ctx, [(x + d, y - d), (x - d, y + d)], WHITE, r * 0.22, a)


def arrow(ctx, a, b, c, w=7, al=1.0, head=24):
    line(ctx, [a, b], c, w, al)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    ctx.move_to(b[0] + head * math.cos(ang), b[1] + head * math.sin(ang))
    ctx.line_to(b[0] + head * 0.85 * math.cos(ang + 2.4), b[1] + head * 0.85 * math.sin(ang + 2.4))
    ctx.line_to(b[0] + head * 0.85 * math.cos(ang - 2.4), b[1] + head * 0.85 * math.sin(ang - 2.4))
    ctx.close_path()
    rgba(ctx, c, al)
    ctx.fill()


# ============================================================ tanks (side view, facing +x, origin = track bottom)

TANKS = {
    "arjun":   dict(L=560, hh=72, r=26, n=7, gun=330, body=SAND_TANK, turret="box", era=False, skirt=True),
    "arjun1a": dict(L=570, hh=74, r=26, n=7, gun=330, body=SAND_1A, turret="box", era=True, skirt=True),
    "t90":     dict(L=470, hh=58, r=25, n=6, gun=300, body=OLIVE_TANK, turret="dome", era=True, skirt=False),
    "t72":     dict(L=470, hh=58, r=25, n=6, gun=290, body=T72_C, turret="dome", era=False, skirt=False),
    "frcv":    dict(L=500, hh=60, r=24, n=6, gun=300, body=FRCV_C, turret="wedge", era=False, skirt=True),
}


def tank(ctx, x, y, s, kind, T=0.0, flip=False, a=1.0, outline=None, reveal=1.0, recoil=0.0, roll=0.0, rot=0.0,
         body=None, elev=0.0):
    """Draw a tank; returns the muzzle point in the caller's coordinates."""
    P = TANKS[kind]
    L, r, hh, gl = P["L"], P["r"], P["hh"], P["gun"]
    body = body or P["body"]
    base = -(2 * r + 14)
    top = base - hh
    if P["turret"] == "box":
        tx0, tx1, th = -190, 150, 88
    elif P["turret"] == "dome":
        tx0, tx1, th = -130, 110, 70
    else:
        tx0, tx1, th = -150, 140, 66
    gy = top - th * 0.5
    gx = tx1 - 10
    sx = -s if flip else s

    def to_parent(lx, ly):
        px, py = lx * sx, ly * s
        return x + px * math.cos(rot) - py * math.sin(rot), y + px * math.sin(rot) + py * math.cos(rot)

    muzzle = to_parent(gx + (gl - recoil) * math.cos(elev), gy - (gl - recoil) * math.sin(elev))
    if reveal <= 0 or a <= 0:
        return muzzle
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot if not flip else -rot)
    ctx.scale(sx, s)
    if reveal < 1:
        ctx.rectangle(-L / 2 - 60, top - th - 200, (L + gl + 120) * reveal, 700)
        ctx.clip()

    def paint(c, al=1.0):
        if outline:
            rgba(ctx, outline, 0.95 * a * al)
            ctx.set_line_width(3.0 / s)
            ctx.stroke()
        else:
            rgba(ctx, c, a * al)
            ctx.fill()

    # track + wheels
    rrect(ctx, -L / 2 - 8, base, L + 16, 2 * r + 14, r + 7)
    paint((0.09, 0.09, 0.08))
    if not outline:
        for i in range(int(L / 18)):                       # track links
            lx = -L / 2 + i * 18 + (roll * 6) % 18
            ctx.rectangle(lx, base + 2 * r + 9, 9, 5)
        rgba(ctx, (0.25, 0.25, 0.22), a)
        ctx.fill()
    for i in range(P["n"]):
        wx = -L / 2 + r + 16 + i * (L - 2 * r - 32) / (P["n"] - 1)
        ctx.arc(wx, base + r + 7, r, 0, math.tau)
        paint(shade(body, 0.5))
        for k in range(3):
            ang = roll + k * math.tau / 3
            ctx.move_to(wx, base + r + 7)
            ctx.line_to(wx + r * 0.8 * math.cos(ang), base + r + 7 + r * 0.8 * math.sin(ang))
        rgba(ctx, outline or (0.14, 0.14, 0.12), a)
        ctx.set_line_width(2.5 / s)
        ctx.stroke()
    # hull
    nose = 46 if P["turret"] == "box" else 34
    ctx.move_to(-L / 2 - 4, base)
    ctx.line_to(L / 2 + nose, base)
    ctx.line_to(L / 2 - 26, top)
    ctx.line_to(-L / 2 + 4, top)
    ctx.close_path()
    paint(body)
    if P["skirt"]:
        rrect(ctx, -L / 2 + 6, base - 4, L - 4, r + 6, 4)
        paint(shade(body, 0.82))
        if P["era"] and not outline:
            for i in range(11):
                ctx.rectangle(-L / 2 + 14 + i * (L - 30) / 11, base, (L - 30) / 11 - 6, r - 4)
            rgba(ctx, shade(body, 0.68), a)
            ctx.fill()
    ctx.rectangle(-L / 2 + 14, top + hh * 0.45, L * 0.82, 5)
    paint(shade(body, 0.7))
    # gun (drawn before turret so the mantlet covers its root)
    ctx.save()
    ctx.translate(gx, gy)
    ctx.rotate(-elev)
    ctx.rectangle(-30 - recoil, -9, gl + 30, 18 if P["turret"] == "box" else 15)
    paint(shade(body, 0.72))
    ctx.rectangle(gl * 0.45 - recoil, -12, 46, 24)            # fume extractor
    paint(shade(body, 0.62))
    ctx.restore()
    # turret
    if P["turret"] == "box":
        ctx.move_to(tx0, top)
        ctx.line_to(tx1 + 30, top)
        ctx.line_to(tx1, top - th * 0.62)
        ctx.line_to(tx1 - 40, top - th)
        ctx.line_to(tx0 + 20, top - th)
        ctx.line_to(tx0 - 26, top - th * 0.55)
        ctx.close_path()
        paint(shade(body, 1.1))
        ctx.rectangle(tx0 - 10, top - th * 0.5, (tx1 - tx0) * 0.75, 4)
        paint(shade(body, 0.8))
        rrect(ctx, -40, top - th - 22, 56, 22, 5)             # commander sight
        paint(shade(body, 0.9))
        rrect(ctx, 40, top - th - 16, 44, 16, 4)              # gunner sight
        paint(shade(body, 0.85))
    elif P["turret"] == "dome":
        ctx.save()
        ctx.translate((tx0 + tx1) / 2, top)
        ctx.scale((tx1 - tx0) / 2, th)
        ctx.arc(0, 0, 1, math.pi, 2 * math.pi)
        ctx.restore()
        ctx.close_path()
        paint(shade(body, 1.12))
        rrect(ctx, -20, top - th - 16, 46, 18, 6)
        paint(shade(body, 0.9))
        if P["era"]:
            ctx.move_to(tx1 - 70, top - th * 0.92)              # ERA brow on the turret front
            ctx.line_to(tx1 + 18, top - th * 0.42)
            ctx.line_to(tx1 + 8, top - th * 0.12)
            ctx.line_to(tx1 - 60, top - th * 0.62)
            ctx.close_path()
            paint(shade(body, 0.8))
            if not outline:
                for k in range(2):                              # dazzler lights
                    circle(ctx, tx1 - 40 + k * 18, top - th * 0.32, 6, (1, 0.15, 0.1), a)
    else:
        ctx.move_to(tx0, top)
        ctx.line_to(tx1 + 40, top)
        ctx.line_to(tx1 - 10, top - th)
        ctx.line_to(tx0 + 10, top - th)
        ctx.close_path()
        paint(shade(body, 1.12))
        rrect(ctx, -10, top - th - 26, 40, 26, 4)               # remote weapon station
        paint(shade(body, 0.9))
    if P["era"] and P["turret"] == "box" and not outline:
        for i in range(3):
            for j in range(2):
                ctx.rectangle(tx1 - 44 + i * 18 - j * 6, top - th * 0.82 + j * 26, 15, 22)
        rgba(ctx, shade(body, 0.72), a)
        ctx.fill()
    ctx.move_to(tx0 + 30, top - th)                            # antenna
    ctx.line_to(tx0 + 10, top - th - 110)
    rgba(ctx, outline or (0.15, 0.15, 0.15), a)
    ctx.set_line_width(2.5 / s)
    ctx.stroke()
    ctx.restore()
    return muzzle


def mini_tank(ctx, x, y, w, kind, c, a=1.0):
    """Flat pictogram tank w px wide (for fleet counts and icons)."""
    s = w / 100
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rgba(ctx, c, a)
    rrect(ctx, -50, -14, 100, 14, 7)
    ctx.fill()
    ctx.move_to(-46, -14)
    ctx.line_to(50, -14)
    ctx.line_to(40, -26)
    ctx.line_to(-44, -26)
    ctx.close_path()
    ctx.fill()
    if kind.startswith("arjun"):
        ctx.rectangle(-26, -40, 44, 14)
    else:
        ctx.arc(-4, -26, 22, math.pi, 2 * math.pi)
    ctx.fill()
    ctx.rectangle(10, -36, 48, 5)
    ctx.fill()
    ctx.restore()


def dust(ctx, x, y, T, k=1.0, c=(0.85, 0.72, 0.5)):
    for i in range(8):
        u = (T * 0.8 + i / 8) % 1.0
        circle(ctx, x - 160 * u - 20 * math.sin(i * 3), y - 50 * u - 10, 14 + 46 * u, c, 0.35 * (1 - u) * k)


def flash(ctx, x, y, u, c=GOLD):
    if 0 <= u < 0.35:
        k = 1 - u / 0.35
        glow(ctx, x, y, 220 * k + 40, c, 0.9 * k)
        circle(ctx, x, y, 34 * k, (1, 1, 1), k)


# ============================================================ backgrounds

def desert(ctx, T, night=False, speed=0.0, sun=(1460, 470)):
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    if night:
        stops = [(0, "#03060F"), (0.6, "#0B1530"), (1, "#1C2A48")]
    else:
        stops = [(0, "#1B1336"), (0.45, "#6E2E45"), (0.8, "#D2683A"), (1, "#F2AA5E")]
    for p, h in stops:
        g.add_color_stop_rgb(p, *hexc(h))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, GROUND + 10)
    ctx.fill()
    for i in range(80 if night else 30):
        circle(ctx, rnd(i, 1) * W, rnd(i, 2) * GROUND * 0.5, 1 + 1.6 * rnd(i, 3), WHITE,
               (0.2 + 0.4 * rnd(i, 4)) * (1 if night else 0.35))
    if night:
        glow(ctx, 1500, 200, 200, (0.9, 0.95, 1), 0.2)
        circle(ctx, 1500, 200, 40, (0.95, 0.95, 0.9), 0.95)
    else:
        glow(ctx, sun[0], sun[1], 360, (1, 0.75, 0.4), 0.45)
        circle(ctx, sun[0], sun[1], 90, (1, 0.86, 0.55), 0.95)
    layers = [(640, 70, 1.3, "#3A2340" if not night else "#0E1730", 0.15),
              (700, 55, 2.1, "#7A4430" if not night else "#152038", 0.35),
              (760, 40, 3.4, "#A8703F" if not night else "#1B2840", 0.65)]
    for base, amp, seed, col, sp in layers:
        off = T * speed * sp
        ctx.move_to(0, H)
        for i in range(0, 41):
            xx = i * 50
            k = (xx + off) / 50
            yy = base - amp * (0.5 + 0.5 * math.sin(k * 0.22 + seed)) - 18 * math.sin(k * 0.61 + seed * 2)
            ctx.line_to(xx, yy)
        ctx.line_to(W, H)
        ctx.close_path()
        rgba(ctx, hexc(col))
        ctx.fill()
    g = cairo.LinearGradient(0, GROUND - 20, 0, H)
    g.add_color_stop_rgb(0, *(hexc("#C9995C") if not night else hexc("#223047")))
    g.add_color_stop_rgb(1, *(hexc("#6E4C2A") if not night else hexc("#0B111C")))
    ctx.set_source(g)
    ctx.rectangle(0, GROUND - 4, W, H)
    ctx.fill()
    for i in range(40):                                     # ripples / shrubs in the sand
        xx = (rnd(i, 7) * W * 1.2 - (T * speed) % (W * 1.2)) % (W * 1.2) - 60
        yy = GROUND + 20 + rnd(i, 8) * 200
        line(ctx, [(xx, yy), (xx + 40 + 30 * rnd(i, 9), yy - 3)], (0, 0, 0), 2, 0.12)


def blueprint_bg(ctx):
    rgba(ctx, BP)
    ctx.paint()
    for x in range(0, W, 40):
        line(ctx, [(x, 0), (x, H)], BP_LINE, 1, 0.12 if x % 200 else 0.25)
    for y in range(0, H, 40):
        line(ctx, [(0, y), (W, y)], BP_LINE, 1, 0.12 if y % 200 else 0.25)


def studio_bg(ctx, c1="#0A0F18", c2="#162232"):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc(c1))
    g.add_color_stop_rgb(1, *hexc(c2))
    ctx.set_source(g)
    ctx.paint()


# ============================================================ shots

def duel(ctx, S, mode="face", lit=None, labels=True):
    """Desert: Arjun (left, facing right) vs T-90 (right, facing left).
    mode: face | fire_arjun | fire_both | race | night | versus"""
    night = mode == "night"
    race = mode == "race"
    desert(ctx, S.T, night=night, speed=260 if race else 8)
    if race:
        xa = 420 + 40 * math.sin(S.T * 1.3)
        xt = 1100 + 30 * math.sin(S.T * 1.1 + 1)
        dust(ctx, xa - 300, GROUND - 10, S.T, 1.0)
        dust(ctx, xt - 260, GROUND - 10, S.T + 0.4, 0.9)
        tank(ctx, xa, GROUND + 6 + 2 * math.sin(S.T * 9), 0.7, "arjun", roll=-S.T * 8)
        tank(ctx, xt, GROUND + 6 + 2 * math.sin(S.T * 8), 0.66, "t90", roll=-S.T * 8)
        if labels:
            tag(ctx, "ARJUN", xa, 470, ARJ_C, 32)
            tag(ctx, "T-90", xt, 500, T90_C, 32)
        vignette(ctx)
        return
    dim_a = 1.0 if lit in (None, "arjun") else 0.35
    dim_t = 1.0 if lit in (None, "t90") else 0.35
    fire_u = (S.t - 0.6) / 0.9
    rec = 18 * max(0.0, 1 - abs(fire_u - 0.1) * 6) if mode in ("fire_arjun", "fire_both", "night") else 0
    ma = tank(ctx, 440, GROUND + 6, 0.72, "arjun", recoil=rec, a=1.0)
    mt = tank(ctx, 1480, GROUND + 6, 0.70, "t90", flip=True, a=1.0,
              recoil=rec if mode == "fire_both" else 0)
    for (left, d) in ((True, dim_a), (False, dim_t)):
        if d < 1:
            g = cairo.LinearGradient(0 if left else W, 0, W / 2 if left else W / 2, 0)
            g.add_color_stop_rgba(0, 0, 0, 0, 0.62)
            g.add_color_stop_rgba(0.8, 0, 0, 0, 0.5)
            g.add_color_stop_rgba(1, 0, 0, 0, 0)
            ctx.set_source(g)
            ctx.rectangle(0 if left else W / 2, 0, W / 2, H)
            ctx.fill()
    if mode in ("fire_arjun", "fire_both", "night"):
        flash(ctx, *ma, fire_u)
        g = clamp(fire_u)
        tx = 1880
        if 0 < g < 1:
            sx = lerp(ma[0], tx, g)
            line(ctx, [(max(ma[0], sx - 160), ma[1]), (sx, ma[1])], GOLD, 5, 0.9)
        if g >= 1:
            k = clamp((S.t - 1.5) / 0.6)
            glow(ctx, tx - 20, ma[1], 120, (1, 0.6, 0.2), 0.7 * (1 - 0.6 * k))
        if mode == "fire_both":
            flash(ctx, *mt, fire_u - 0.25, CYAN)
    if night:
        rgba(ctx, (0.1, 0.9, 0.4), 0.18)
        ctx.paint()
        for yy in range(0, H, 6):
            line(ctx, [(0, yy), (W, yy)], (0, 0, 0), 1, 0.12)
        tag(ctx, "NIGHT FIRING  //  THERMAL SIGHT", W / 2, 220, (0.6, 1, 0.7), 30)
    if mode == "versus":
        k = ease_out_back(clamp(S.t / 0.7))
        big(ctx, "VS", W / 2, 520, 150 * k + 1, WHITE)
    if labels:
        tag(ctx, "ARJUN  //  BHARAT", 440, 360, ARJ_C, 32, a=dim_a)
        tag(ctx, "T-90 BHISHMA", 1480, 380, T90_C, 32, a=dim_t)
    vignette(ctx)


def blueprint(ctx, S, kind="arjun", callouts=(), title=None, name=None):
    """Blueprint grid; the tank is drawn as a stroke, then filled; callouts pop in one by one."""
    blueprint_bg(ctx)
    draw = ease_out_cubic(S.t / 1.2)
    fill = clamp((S.t - 1.0) / 0.8)
    cx, cy, s = 860, 760, 1.15
    tank(ctx, cx, cy, s, kind, outline=BP_LINE, reveal=draw)
    tank(ctx, cx, cy, s, kind, a=0.85 * fill)
    if title:
        big(ctx, title, W / 2, 230, 84, WHITE, a=clamp(S.t / 0.4))
    if name:
        tag(ctx, name, W / 2, 310, BP_LINE, 30, a=clamp((S.t - 0.2) / 0.4))
    n = max(1, len(callouts))
    for i, (lab, px, py, lx, ly) in enumerate(callouts):
        a = clamp((S.u * (n + 1.5) - i - 0.6) / 0.6) if n > 1 else clamp((S.t - 0.8) / 0.4)
        if a <= 0:
            continue
        p = (cx + px * s, cy + py * s)
        circle(ctx, *p, 9, GOLD, a)
        line(ctx, [p, (lx, ly)], GOLD, 3, a)
        tag(ctx, lab, lx, ly, GOLD, 32, a=a, anchor="l" if lx > p[0] else "r")
    vignette(ctx, 0.5)


# callout anchor points on the big blueprint tank (local px at s=1, origin = track bottom centre)
GUN_PT = (430, -205)
ENGINE_PT = (-210, -120)
ARMOR_PT = (130, -215)
CREW_PT = (-60, -250)
TRACK_PT = (0, -30)


def timeline(ctx, S, focus=0):
    years = [("1974", "SHURUAAT"), ("1989", "PROTOTYPE"), ("2004", "PEHLI REGIMENT"), ("2010", "DESERT TRIALS"),
             ("2021", "MK1A ORDER"), ("2026", "ENGINE KA INTEZAAR")]
    studio_bg(ctx, "#070B12", "#131C2A")
    gap = 470
    cxf = lerp(focus - 0.7, focus, ease_out_cubic(S.t / 1.2))
    y = 560
    for i in range(-1, 50):                                 # film strip holes
        xx = (i * 60 - cxf * 90) % (W + 60) - 30
        rrect(ctx, xx, y - 150, 30, 18, 4)
        rgba(ctx, WHITE, 0.08)
        ctx.fill()
        rrect(ctx, xx, y + 140, 30, 18, 4)
        ctx.fill()
    line(ctx, [(0, y), (W, y)], STEEL, 3, 0.5)
    for i, (yr, lab) in enumerate(years):
        x = W / 2 + (i - cxf) * gap
        if x < -300 or x > W + 300:
            continue
        on = i == focus
        a = 1.0 if on else 0.32
        if on:
            glow(ctx, x, y, 230, GOLD, 0.3)
        circle(ctx, x, y, 22 if on else 12, GOLD if on else STEEL, a)
        big(ctx, yr, x, y - 85, 120 if on else 62, GOLD if on else WHITE, a=a)
        text(ctx, lab, x, y + 80, 36 if on else 24, WHITE, font=MONO, a=a)
    if focus in (1, 2, 4):
        mini_tank(ctx, W / 2, y + 230, 220, "arjun", SAND_TANK, clamp((S.t - 0.6) / 0.5))
    vignette(ctx)


def fleet(ctx, S, groups, per=10, note=None):
    """Pictogram: each icon = `per` tanks. groups = [(title, value, shown, colour, kind)]."""
    studio_bg(ctx)
    n = len(groups)
    colw = W / n
    for gi, (title, value, shown, c, kind) in enumerate(groups):
        x0 = gi * colw
        icons = value / per
        cols = 10 if icons > 20 else 5
        rows = math.ceil(icons / cols)
        iw = min(150 if n == 1 else 110, (colw - 160) / cols)
        ih = min(iw * 0.55, 440 / max(1, rows))
        iw = min(iw, ih / 0.5)
        top_y = 420 + (440 - rows * ih) / 2
        gx = x0 + colw / 2 - cols * iw / 2
        grow = clamp((S.t - 0.3) / max(0.8, S.d * 0.5))
        shown_n = icons * ease_out_cubic(grow)
        big(ctx, shown if grow >= 1 else f"{int(value * ease_out_cubic(grow))}", x0 + colw / 2, 210, 120, c)
        text(ctx, title, x0 + colw / 2, 310, 36, WHITE, font=MONO)
        for k in range(math.ceil(icons)):
            if k >= shown_n:
                break
            part = min(1.0, icons - k)
            xx = gx + (k % cols) * iw + iw / 2
            yy = top_y + (k // cols) * ih + ih * 0.8
            if part < 1:
                ctx.save()
                ctx.rectangle(xx - iw / 2, yy - ih, iw * part, ih + 4)
                ctx.clip()
            mini_tank(ctx, xx, yy, iw * 0.86, kind, c, 0.95)
            if part < 1:
                ctx.restore()
        if gi > 0:
            line(ctx, [(x0, 170), (x0, 880)], WHITE, 2, 0.15)
    text(ctx, note or f"1 ICON = {per} TANKS", W / 2, 915, 26, STEEL, font=MONO)
    vignette(ctx, 0.45)


def factory(ctx, S, kind="arjun", sign="HEAVY VEHICLES FACTORY  //  AVADI", lab=False):
    """Factory hall: girders, hulls rolling down the line, welding sparks."""
    studio_bg(ctx, "#0B0E13", "#1E2430")
    for i in range(9):                                       # roof trusses
        x = i * 240 - 40
        line(ctx, [(x, 120), (x + 120, 40), (x + 240, 120)], STEEL, 4, 0.25)
        line(ctx, [(x, 120), (x, 760)], STEEL, 10, 0.18)
        glow(ctx, x + 120, 140, 110, (1, 0.9, 0.7), 0.18)
    line(ctx, [(0, 120), (W, 120)], STEEL, 6, 0.3)
    rgba(ctx, hexc("#2A2F38"))
    ctx.rectangle(0, 780, W, H - 780)
    ctx.fill()
    rgba(ctx, hexc("#3A404A"))
    ctx.rectangle(0, 760, W, 26)
    ctx.fill()
    for i in range(30):
        xx = (i * 90 + S.T * 40) % (W + 90) - 45
        line(ctx, [(xx, 773), (xx + 40, 773)], GOLD, 3, 0.5)
    off = S.T * 40
    for i in range(4):
        x = (i * 620 + off) % (W + 900) - 450
        stage = i % 3
        if stage == 0:
            tank(ctx, x, 770, 0.55, kind, outline=STEEL)
        else:
            tank(ctx, x, 770, 0.55, kind, a=0.75 + 0.25 * (stage == 2))
        sx, sy = x + 60, 640
        for k in range(10):
            ang = -math.pi / 2 + (rnd(k, int(S.T * 12) + i) - 0.5) * 2.4
            dd = 20 + 70 * rnd(k + 3, int(S.T * 12))
            line(ctx, [(sx, sy), (sx + dd * math.cos(ang), sy + dd * math.sin(ang))], (1, 0.8, 0.3), 2, 0.8)
        glow(ctx, sx, sy, 60, (1, 0.8, 0.4), 0.5 + 0.3 * math.sin(S.T * 20 + i))
    if lab:
        rrect(ctx, 1220, 200, 560, 300, 14)
        rgba(ctx, INK, 0.85)
        ctx.fill_preserve()
        rgba(ctx, BP_LINE, 0.9)
        ctx.set_line_width(2)
        ctx.stroke()
        text(ctx, "DRDO LAB  //  CVRDE", 1500, 245, 30, BP_LINE, font=MONO)
        tank(ctx, 1500, 440, 0.4, "arjun", outline=BP_LINE, reveal=ease_out_cubic(S.t / 1.5))
    tag(ctx, sign, W / 2 if not lab else 620, 210, GOLD, 30)
    vignette(ctx)


def money(ctx, S, start=0.0, end=15.5, label="RS 15.5 CRORE", sub="1974 KA ANDAAZA", fmt="{:.1f}", c=GOLD):
    """Note stacks growing while a counter runs."""
    studio_bg(ctx, "#08100C", "#16261C")
    u = ease_out_cubic(clamp((S.t - 0.2) / max(1.0, S.d * 0.55)))
    val = lerp(start, end, u)
    stacks = 7
    for i in range(stacks):
        h = 40 + 380 * u * (0.45 + 0.55 * (i + 1) / stacks) * (end / max(end, 400) * 3 if end > 50 else 0.5)
        h = min(h, 440)
        x = 300 + i * 200
        for j in range(int(h / 16)):
            rrect(ctx, x - 70, 820 - j * 16 - 14, 140, 13, 3)
            rgba(ctx, hexc("#4F9A5E") if j % 2 else hexc("#3F7F4D"), 0.95)
            ctx.fill()
        rrect(ctx, x - 70, 820 - int(h / 16) * 16 - 14, 140, 13, 3)
        rgba(ctx, hexc("#9AD3A6"), 0.9)
        ctx.fill()
    big(ctx, ("RS " + fmt.format(val) + " CR") if u < 1 else label, W / 2, 230, 130, c)
    text(ctx, sub, W / 2, 330, 36, WHITE, font=MONO)
    vignette(ctx)


def weighbridge(ctx, S, items=(("arjun", 58.5, "ARJUN MK1"),), diff=False):
    """Tanks parked on weighbridge plates with digital tonnage readouts."""
    studio_bg(ctx, "#0B0D12", "#1A1F28")
    n = len(items)
    colw = W / n
    for i, (kind, t, lab) in enumerate(items):
        cx = colw * (i + 0.5)
        k = ease_out_cubic(clamp((S.t - 0.2 - i * 0.35) / 0.8))
        drop = (1 - k) * -260
        rrect(ctx, cx - 300, 790, 600, 26, 6)
        rgba(ctx, hexc("#3A414C"))
        ctx.fill()
        for j in range(6):
            line(ctx, [(cx - 280 + j * 112, 795), (cx - 220 + j * 112, 811)], GOLD, 3, 0.4)
        sc = 0.62 if n > 1 else 0.85
        sc = min(sc, (colw - 60) / 900 + 0.0) if n > 2 else sc
        tank(ctx, cx - 40 * sc, 790 + drop, sc, kind, a=k)
        shown = t * clamp((S.t - 0.6 - i * 0.35) / 0.7)
        rrect(ctx, cx - 150, 190, 300, 120, 12)
        rgba(ctx, (0.02, 0.02, 0.02), 0.95)
        ctx.fill_preserve()
        c = RED if t >= 60 else (GOLD if t > 50 else CYAN)
        rgba(ctx, c, 0.9)
        ctx.set_line_width(3)
        ctx.stroke()
        s = f"{shown:.1f} T" if t % 1 else f"{shown:.0f} T"
        text(ctx, s, cx, 250, 72, c, font=MONO)
        text(ctx, lab, cx, 360, 34, WHITE, font=MONO)
    if diff and n >= 2:
        a = clamp((S.t - 1.8) / 0.5)
        big(ctx, "20+ TON KA FARAK", W / 2, 470, 90, RED, a=a)
    vignette(ctx, 0.5)


def bridge(ctx, S, kind="arjun", limit="LOAD LIMIT", fail=True, sign2=None):
    """Canal + small bridge. Heavy Arjun waits at the edge with a red warning; T-90 rolls across."""
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc("#0E1A2C"))
    g.add_color_stop_rgb(0.6, *hexc("#3E5A6E"))
    g.add_color_stop_rgb(1, *hexc("#1E2A22"))
    ctx.set_source(g)
    ctx.paint()
    for i in range(14):                                      # tree line (Punjab fields)
        x = i * 150 + 40 * rnd(i, 2)
        circle(ctx, x, 600, 60 + 20 * rnd(i, 3), hexc("#1C2E22"))
    rgba(ctx, hexc("#2C4A2A"))
    ctx.rectangle(0, 640, W, 300)
    ctx.fill()
    # canal
    rgba(ctx, hexc("#123A5A"))
    ctx.rectangle(700, 760, 520, 320)
    ctx.fill()
    for i in range(12):
        xx = 720 + (i * 60 + S.T * 30) % 480
        line(ctx, [(xx, 860 + 12 * (i % 3)), (xx + 30, 860 + 12 * (i % 3))], WHITE, 2, 0.25)
    sag = 0
    cross_u = clamp((S.u - 0.15) / 0.7)
    if kind == "arjun":
        tx = lerp(140, 430, ease_out_cubic(cross_u))
        if fail:
            sag = 14 * clamp((S.u - 0.45) / 0.2) * (0.7 + 0.3 * math.sin(S.T * 20))
    else:
        tx = lerp(240, 1600, ease_in_out(cross_u))
    # bridge deck
    ctx.move_to(660, 770)
    ctx.curve_to(860, 770 + sag, 1060, 770 + sag, 1260, 770)
    ctx.line_to(1260, 800)
    ctx.curve_to(1060, 800 + sag, 860, 800 + sag, 660, 800)
    ctx.close_path()
    rgba(ctx, hexc("#7C7F86"))
    ctx.fill()
    for xx in (820, 1100):
        ctx.rectangle(xx - 14, 800 + sag * 0.6, 28, 260)
        rgba(ctx, hexc("#5E6168"))
        ctx.fill()
    for i in range(12):
        line(ctx, [(680 + i * 50, 770 + sag * math.sin(math.pi * i / 11)),
                   (680 + i * 50, 740 + sag * math.sin(math.pi * i / 11))], STEEL, 3, 0.7)
    line(ctx, [(660, 740), (1260, 740)], STEEL, 4, 0.7)
    rgba(ctx, hexc("#3B3A2E"))
    ctx.rectangle(0, 770, 700, 40)
    ctx.rectangle(1220, 770, 700, 40)
    ctx.fill()
    on_deck = 660 < tx < 1260
    ty = 772 + (sag * 0.9 if on_deck else 0)
    tank(ctx, tx, ty, 0.55, kind, roll=-S.T * 6)
    # sign
    sx, sy = 1400, 560
    line(ctx, [(sx, sy + 70), (sx, 770)], STEEL, 8)
    rrect(ctx, sx - 120, sy - 60, 240, 130, 12)
    rgba(ctx, (0.98, 0.95, 0.85))
    ctx.fill()
    rrect(ctx, sx - 108, sy - 48, 216, 106, 8)
    rgba(ctx, RED)
    ctx.set_line_width(8)
    ctx.stroke()
    text(ctx, limit, sx, sy + 4, 40 if len(limit) > 5 else 64, INK, font=IMPACT)
    if kind == "arjun" and fail:
        a = clamp((S.u - 0.5) / 0.15)
        cross(ctx, 960, 560, 70, a)
        if sign2:
            tag(ctx, sign2, 960, 440, RED, 34, a=a)
        for k in range(5):
            cx_ = 760 + k * 100
            line(ctx, [(cx_, 790 + sag), (cx_ + 18, 806 + sag), (cx_ + 6, 822 + sag)], (0.1, 0.1, 0.1), 3, a)
    if kind != "arjun":
        a = clamp((S.u - 0.75) / 0.15)
        tick(ctx, 960, 560, 64, a)
    vignette(ctx)


def rail(ctx, S, kind="arjun", note="SPECIAL WAGON CHAHIYE"):
    """A tank on a rail flat wagon; dashed loading-gauge box shows the overhang in red."""
    studio_bg(ctx, "#0A1220", "#24344A")
    for i in range(14):
        circle(ctx, i * 150 + 60, 650, 50 + 30 * rnd(i, 1), hexc("#1A2638"))
    rgba(ctx, hexc("#1B1F26"))
    ctx.rectangle(0, 720, W, H)
    ctx.fill()
    slide = (1 - ease_out_cubic(clamp(S.t / 1.4))) * -900
    for i in range(60):
        xx = (i * 40 + slide * 0) % W
        line(ctx, [(xx, 860), (xx, 872)], hexc("#5A4A3A"), 10, 0.9)
    line(ctx, [(0, 858), (W, 858)], STEEL, 5)
    cx = W / 2 + slide
    wl = 760
    rrect(ctx, cx - wl / 2, 790, wl, 34, 4)
    rgba(ctx, hexc("#4A3A30"))
    ctx.fill()
    for bx in (cx - wl / 2 + 90, cx - wl / 2 + 170, cx + wl / 2 - 170, cx + wl / 2 - 90):
        circle(ctx, bx, 842, 18, hexc("#2A2A2A"))
    tank(ctx, cx - 30, 790, 0.95 if kind.startswith("arjun") else 0.88, kind)
    a = clamp((S.t - 1.4) / 0.5)
    if a > 0:
        ctx.set_dash([14, 10])
        ctx.rectangle(cx - wl / 2, 520, wl, 270)
        rgba(ctx, WHITE, 0.7 * a)
        ctx.set_line_width(3)
        ctx.stroke()
        ctx.set_dash([])
        text(ctx, "WAGON KI HAD", cx - wl / 2 + 10, 500, 26, WHITE, font=MONO, anchor="l", a=a)
        if kind.startswith("arjun"):
            for side in (-1, 1):
                x0 = cx + side * wl / 2
                ctx.rectangle(min(x0, x0 + side * 70), 700, 70, 90)
                rgba(ctx, RED, 0.35 * a)
                ctx.fill()
            tag(ctx, note, W / 2, 320, RED, 36, a=a)
        else:
            tag(ctx, "AARAM SE FIT", W / 2, 320, GREEN, 36, a=a)
    vignette(ctx)


def terrain(ctx, S, kind="arjun", marks=("ok", "x", "x"), hi=None):
    """Three panels: desert / Punjab canals / Ladakh mountains, each with a tick or cross for the tank."""
    rgba(ctx, (0.03, 0.04, 0.06))
    ctx.paint()
    names = ["RAJASTHAN REGISTAAN", "PUNJAB KI NAHAREIN", "LADAKH KE PAHAD"]
    pw, gap = 580, 30
    x0 = (W - 3 * pw - 2 * gap) / 2
    for i in range(3):
        x = x0 + i * (pw + gap)
        k = ease_out_cubic(clamp((S.t - i * 0.25) / 0.6))
        ctx.save()
        rrect(ctx, x, 200 + 40 * (1 - k), pw, 560, 18)
        ctx.clip()
        if i == 0:
            g = cairo.LinearGradient(0, 200, 0, 760)
            g.add_color_stop_rgb(0, *hexc("#E07A3E"))
            g.add_color_stop_rgb(1, *hexc("#F3C07A"))
            ctx.set_source(g)
            ctx.paint()
            for j in range(3):
                ctx.move_to(x, 620 + j * 30)
                for q in range(13):
                    ctx.line_to(x + q * 50, 600 + j * 40 - 30 * math.sin(q * 0.6 + j))
                ctx.line_to(x + pw, 800)
                ctx.line_to(x, 800)
                ctx.close_path()
                rgba(ctx, hexc(["#C98A4A", "#B37538", "#9A6230"][j]))
                ctx.fill()
        elif i == 1:
            g = cairo.LinearGradient(0, 200, 0, 760)
            g.add_color_stop_rgb(0, *hexc("#6FA7C9"))
            g.add_color_stop_rgb(1, *hexc("#C7E0D0"))
            ctx.set_source(g)
            ctx.paint()
            rgba(ctx, hexc("#4E8A3A"))
            ctx.rectangle(x, 560, pw, 200)
            ctx.fill()
            for j in range(6):
                line(ctx, [(x, 590 + j * 30), (x + pw, 580 + j * 30)], hexc("#7FB060"), 3, 0.7)
            rgba(ctx, hexc("#2F6FA8"))
            ctx.rectangle(x + pw * 0.45, 560, 60, 200)
            ctx.fill()
            rgba(ctx, hexc("#8A8D92"))
            ctx.rectangle(x + pw * 0.45 - 20, 640, 100, 16)
            ctx.fill()
        else:
            g = cairo.LinearGradient(0, 200, 0, 760)
            g.add_color_stop_rgb(0, *hexc("#203A66"))
            g.add_color_stop_rgb(1, *hexc("#9DB4CC"))
            ctx.set_source(g)
            ctx.paint()
            for j, (px, ph) in enumerate(((0.2, 260), (0.55, 320), (0.85, 230))):
                ctx.move_to(x + pw * px - 220, 760)
                ctx.line_to(x + pw * px, 760 - ph - 120)
                ctx.line_to(x + pw * px + 220, 760)
                ctx.close_path()
                rgba(ctx, hexc(["#4A5A70", "#3C4A5E", "#56667C"][j]))
                ctx.fill()
                ctx.move_to(x + pw * px - 50, 760 - ph - 120 + 60)
                ctx.line_to(x + pw * px, 760 - ph - 120)
                ctx.line_to(x + pw * px + 50, 760 - ph - 120 + 60)
                ctx.close_path()
                rgba(ctx, WHITE, 0.85)
                ctx.fill()
        mini_tank(ctx, x + pw / 2, 740, 170, kind, SAND_TANK if kind.startswith("arjun") else OLIVE_TANK)
        ctx.restore()
        on = hi is None or hi == i
        rrect(ctx, x, 200 + 40 * (1 - k), pw, 560, 18)
        rgba(ctx, GOLD if (hi == i) else WHITE, 0.9 if hi == i else 0.25)
        ctx.set_line_width(5 if hi == i else 2)
        ctx.stroke()
        if not on:
            rrect(ctx, x, 200, pw, 560, 18)
            rgba(ctx, (0, 0, 0), 0.5)
            ctx.fill()
        text(ctx, names[i], x + pw / 2, 810, 30, WHITE, font=MONO, a=k)
        m = marks[i]
        a = clamp((S.t - 0.8 - i * 0.3) / 0.4)
        if m == "ok":
            tick(ctx, x + pw - 70, 270, 44, a)
        elif m == "x":
            cross(ctx, x + pw - 70, 270, 44, a)
        elif m == "q":
            circle(ctx, x + pw - 70, 270, 44, SAFFRON, a)
            text(ctx, "MUSHKIL", x + pw - 70, 335, 24, SAFFRON, font=MONO, a=a)
    lab = "ARJUN" if kind.startswith("arjun") else "T-90"
    tag(ctx, lab, W / 2, 130, ARJ_C if kind.startswith("arjun") else T90_C, 34)
    vignette(ctx, 0.4)


def crew(ctx, S, n=4, kind="arjun", autoloader=False):
    """Cutaway turret with crew seats lighting up one by one."""
    blueprint_bg(ctx)
    tank(ctx, 960, 900, 1.6, kind, outline=BP_LINE)
    names = ["COMMANDER", "GUNNER", "DRIVER", "LOADER"][:n] if n == 4 else ["COMMANDER", "GUNNER", "DRIVER"]
    pos = [(860, 470), (1080, 500), (1260, 700), (700, 520)]
    for i, nm in enumerate(names):
        a = clamp((S.t - 0.3 - i * 0.35) / 0.4)
        px, py = pos[i]
        glow(ctx, px, py, 80, GOLD if kind.startswith("arjun") else CYAN, 0.4 * a)
        circle(ctx, px, py - 30, 20, WHITE, a)
        rrect(ctx, px - 24, py - 8, 48, 60, 12)
        rgba(ctx, WHITE, a)
        ctx.fill()
        text(ctx, nm, px, py + 90, 24, WHITE, font=MONO, a=a)
    if autoloader:
        a = clamp((S.t - 1.4) / 0.4)
        cx, cy = 760, 760
        for k in range(10):
            ang = k / 10 * math.tau + S.T * 1.5
            circle(ctx, cx + 70 * math.cos(ang), cy + 22 * math.sin(ang), 12, CYAN, a)
        tag(ctx, "AUTOLOADER", cx, cy + 80, CYAN, 26, a=a)
    big(ctx, f"{n} JAWAN", W / 2, 200, 100, GOLD if kind.startswith("arjun") else CYAN)
    vignette(ctx, 0.5)


def engine_shot(ctx, S, mode="import"):
    """Engine block. import: arrives by ship; cut: the supply chain snaps; heat: gauge in red; datran: test bench."""
    studio_bg(ctx, "#0B0D12", "#1D2230")
    cx, cy = 760 if mode in ("import", "cut") else 960, 600
    rrect(ctx, cx - 260, cy - 150, 520, 300, 24)
    rgba(ctx, hexc("#3E4654"))
    ctx.fill()
    for i in range(5):
        rrect(ctx, cx - 220 + i * 92, cy - 230 + 10 * math.sin(S.T * 12 + i * 1.3), 64, 100, 8)
        rgba(ctx, hexc("#59626F"))
        ctx.fill()
    for k in range(3):
        line(ctx, [(cx - 240, cy - 60 + k * 50), (cx + 240, cy - 60 + k * 50)], hexc("#2A303A"), 6)
    circle(ctx, cx + 300, cy + 40, 90, hexc("#2E343F"))
    for k in range(8):
        ang = S.T * 4 + k * math.tau / 8
        line(ctx, [(cx + 300, cy + 40), (cx + 300 + 80 * math.cos(ang), cy + 40 + 80 * math.sin(ang))], STEEL, 5, 0.7)
    if mode == "import":
        a = clamp((S.t - 0.4) / 0.5)
        tag(ctx, "1400 HP  //  IMPORTED ENGINE", cx, cy + 230, GOLD, 32, a=a)
        g = ease_out_cubic(clamp((S.t - 0.6) / 1.2))
        arrow(ctx, (1820, 300), (lerp(1820, 1180, g), lerp(300, 480, g)), STEEL, 8, a)
        text(ctx, "VIDESHI SUPPLY", 1600, 250, 30, STEEL, font=MONO, a=a)
    elif mode == "cut":
        g = clamp((S.t - 0.8) / 0.5)
        for i in range(8):
            x = 1100 + i * 90 + (40 * g if i >= 4 else 0)
            y = 440 + (40 * g * (i - 3.5) / 4 if i >= 4 else 0)
            ctx.save()
            ctx.translate(x, y)
            ctx.rotate(0.4 * g if i >= 4 else 0)
            rrect(ctx, -40, -20, 80, 40, 20)
            rgba(ctx, STEEL if g < 0.3 or i < 4 else RED, 0.9)
            ctx.set_line_width(10)
            ctx.stroke()
            ctx.restore()
        tag(ctx, "PRODUCTION BAND  //  REPORTS", 1430, 600, RED, 30, a=g)
    elif mode == "heat":
        gx, gy = 1500, 420
        ctx.arc(gx, gy, 150, math.pi, 2 * math.pi)
        rgba(ctx, STEEL, 0.6)
        ctx.set_line_width(8)
        ctx.stroke()
        ctx.arc(gx, gy, 150, 1.65 * math.pi, 2 * math.pi)
        rgba(ctx, RED, 0.9)
        ctx.set_line_width(14)
        ctx.stroke()
        ang = math.pi + math.pi * clamp(0.3 + S.u * 0.75, 0, 0.97)
        line(ctx, [(gx, gy), (gx + 130 * math.cos(ang), gy + 130 * math.sin(ang))], WHITE, 6)
        circle(ctx, gx, gy, 14, WHITE)
        text(ctx, "ENGINE TEMP", gx, gy + 60, 30, WHITE, font=MONO)
        for k in range(6):
            u = (S.T * 0.7 + k / 6) % 1
            circle(ctx, cx - 120 + k * 50, cy - 260 - 120 * u, 14 + 30 * u, (0.7, 0.7, 0.7), 0.35 * (1 - u))
        tag(ctx, "TRIALS 1993-96: OVERHEATING", 960, 920, RED, 30)
    elif mode == "datran":
        val = 1500 * ease_out_cubic(clamp((S.t - 0.3) / 1.5))
        big(ctx, f"{val:.0f} HP", 960, 220, 130, TEAL)
        tag(ctx, "DATRAN  //  DESI ENGINE  //  TESTING", 960, 870, TEAL, 32)
        for k in range(6):
            line(ctx, [(cx - 300 - k * 30, cy + 170), (cx + 300 + k * 30, cy + 170)], TEAL, 2, 0.2)
    vignette(ctx)


def calendar(ctx, S):
    """Delivery calendar pages flip forward: plan 2024 -> later (reports)."""
    studio_bg(ctx)
    years = ["2024", "2025", "2026", "2027", "2028+"]
    u = clamp((S.t - 0.4) / max(1.0, S.d * 0.6))
    idx = min(len(years) - 1, int(u * len(years)))
    cx, cy = W / 2, 560
    for k in range(3):
        rrect(ctx, cx - 260 + k * 10, cy - 260 + k * 10, 520, 520, 24)
        rgba(ctx, (0.85, 0.86, 0.9), 0.3 + 0.2 * k)
        ctx.fill()
    rrect(ctx, cx - 260, cy - 260, 520, 520, 24)
    rgba(ctx, WHITE)
    ctx.fill()
    ctx.rectangle(cx - 260, cy - 260, 520, 110)
    rgba(ctx, RED)
    ctx.fill()
    text(ctx, "MK1A DELIVERY", cx, cy - 205, 40, WHITE, font=IMPACT)
    big(ctx, years[idx], cx, cy + 50, 170, INK if idx == 0 else RED)
    text(ctx, "PLAN" if idx == 0 else "AAGE KHISKI", cx, cy + 190, 40, INK, font=MONO)
    tag(ctx, "TAAREEKH: REPORTS KE MUTABIK", W / 2, 160, STEEL, 28)
    vignette(ctx, 0.5)


def grounded(ctx, S, frac=0.75):
    """Tank park: most Arjuns stand with red NO SPARES tags."""
    studio_bg(ctx, "#0C0F14", "#262A30")
    rgba(ctx, hexc("#30343A"))
    ctx.rectangle(0, 560, W, H)
    ctx.fill()
    n = 8
    for i in range(n):
        row = i // 4
        x = 250 + (i % 4) * 420 + row * 80
        y = 640 + row * 260
        s = 0.34 + row * 0.04
        bad = i not in (2, 5)
        tank(ctx, x, y, s, "arjun", a=0.95)
        a = clamp((S.t - 0.5 - i * 0.12) / 0.3)
        if bad:
            rrect(ctx, x - 80, y - 152, 160, 44, 8)
            rgba(ctx, RED, 0.9 * a)
            ctx.fill()
            text(ctx, "NO SPARES", x, y - 130, 24, WHITE, font=MONO, a=a)
        else:
            tick(ctx, x, y - 130, 26, a)
    big(ctx, f"~{int(frac * 100)}% KHADE", W / 2, 230, 110, RED, a=clamp((S.t - 1.2) / 0.4))
    text(ctx, "2013-2015  //  REPORTS KE MUTABIK", W / 2, 330, 30, STEEL, font=MONO)
    vignette(ctx)


def sealed(ctx, S, title="TRIAL RESULTS", stamp="POORE NATEEJE PUBLIC NAHI"):
    """A file folder that stays shut, stamped."""
    studio_bg(ctx, "#0D0B08", "#24201A")
    cx, cy = W / 2, 560
    rrect(ctx, cx - 420, cy - 280, 840, 560, 20)
    rgba(ctx, hexc("#C9A56A"))
    ctx.fill()
    rrect(ctx, cx - 420, cy - 320, 300, 60, 14)
    ctx.fill()
    text(ctx, title, cx, cy - 150, 64, INK, font=IMPACT)
    text(ctx, "MAHAJAN RANGE  //  2010", cx, cy - 70, 32, INK, font=MONO)
    k = ease_out_back(clamp((S.t - 0.6) / 0.5))
    if k > 0:
        ctx.save()
        ctx.translate(cx, cy + 90)
        ctx.rotate(-0.12)
        ctx.scale(k, k)
        tw = text_width(ctx, stamp, 46, font=IMPACT)
        rrect(ctx, -tw / 2 - 30, -50, tw + 60, 100, 10)
        rgba(ctx, RED, 0.9)
        ctx.set_line_width(8)
        ctx.stroke()
        text(ctx, stamp, 0, 0, 46, RED, font=IMPACT)
        ctx.restore()
    vignette(ctx)


def scoreboard(ctx, S, rows=("FIREPOWER", "ACCURACY", "RET MEIN RAFTAAR"), note="REPORTS KE MUTABIK  //  2010"):
    """Qualitative bars, Arjun vs T-90 - no invented numbers."""
    studio_bg(ctx)
    text(ctx, "ARJUN", 760, 230, 54, ARJ_C, font=IMPACT)
    text(ctx, "T-90", 1300, 230, 54, T90_C, font=IMPACT)
    for i, r in enumerate(rows):
        y = 380 + i * 160
        text(ctx, r, 460, y, 34, WHITE, font=MONO, anchor="r")
        g = ease_out_cubic(clamp((S.t - 0.3 - i * 0.3) / 0.8))
        for j, (c, full) in enumerate(((ARJ_C, 0.92), (T90_C, 0.74))):
            yy = y - 30 + j * 46
            rrect(ctx, 500, yy, 1100, 34, 8)
            rgba(ctx, WHITE, 0.08)
            ctx.fill()
            rrect(ctx, 500, yy, 1100 * full * g, 34, 8)
            rgba(ctx, c, 0.9)
            ctx.fill()
        if g >= 1:
            tick(ctx, 1660, y - 13, 26)
    tag(ctx, note, W / 2, 900, STEEL, 28)
    vignette(ctx, 0.45)


def balance(ctx, S, left="ARJUN", right="T-90", tilt=0.12, title="EK JAISE PAIMAANE NAHI"):
    """Uneven balance scale."""
    studio_bg(ctx, "#0C0A10", "#211A28")
    cx, cy = W / 2, 400
    ang = tilt * ease_out_back(clamp((S.t - 0.3) / 0.9)) + 0.01 * math.sin(S.T * 2)
    line(ctx, [(cx, cy), (cx, 860)], STEEL, 14)
    rrect(ctx, cx - 160, 850, 320, 30, 10)
    rgba(ctx, STEEL)
    ctx.fill()
    dx, dy = 420 * math.cos(ang), 420 * math.sin(ang)
    line(ctx, [(cx - dx, cy - dy), (cx + dx, cy + dy)], GOLD, 10)
    circle(ctx, cx, cy, 20, GOLD)
    for side, lab, c in ((-1, left, ARJ_C), (1, right, T90_C)):
        px, py = cx + side * dx, cy + side * dy
        line(ctx, [(px, py), (px - 110, py + 200)], STEEL, 3, 0.8)
        line(ctx, [(px, py), (px + 110, py + 200)], STEEL, 3, 0.8)
        ctx.move_to(px - 150, py + 200)
        ctx.line_to(px + 150, py + 200)
        ctx.line_to(px + 100, py + 240)
        ctx.line_to(px - 100, py + 240)
        ctx.close_path()
        rgba(ctx, c, 0.9)
        ctx.fill()
        mini_tank(ctx, px, py + 196, 160, "arjun" if side < 0 else "t90", shade(c, 0.8))
        text(ctx, lab, px, py + 290, 40, c, font=IMPACT)
    tag(ctx, title, W / 2, 180, RED, 34, a=clamp((S.t - 0.8) / 0.4))
    vignette(ctx)


def missile(ctx, S):
    """T-90 fires a gun-launched missile at a far target."""
    desert(ctx, S.T, speed=4, sun=(400, 430))
    m = tank(ctx, 520, GROUND + 6, 0.72, "t90", elev=0.03)
    u = clamp((S.t - 0.5) / 1.6)
    flash(ctx, *m, (S.t - 0.5), CYAN)
    tx, ty = 1780, GROUND - 60
    if 0 < u < 1:
        x = lerp(m[0], tx, u)
        y = lerp(m[1], ty, u) - 60 * math.sin(math.pi * u)
        pts = [(lerp(m[0], tx, v), lerp(m[1], ty, v) - 60 * math.sin(math.pi * v)) for v in
               [u * q / 12 for q in range(13)]]
        line(ctx, pts, (0.85, 0.85, 0.85), 6, 0.5)
        circle(ctx, x, y, 8, WHITE)
        glow(ctx, x, y, 50, (1, 0.7, 0.3), 0.8)
    if u >= 1:
        k = clamp((S.t - 2.1) / 0.8)
        glow(ctx, tx, ty, 200 * (1 - k * 0.5), (1, 0.55, 0.2), 0.8 * (1 - k))
    rrect(ctx, tx - 50, ty - 40, 100, 70, 8)
    rgba(ctx, (0.2, 0.2, 0.2), 0.9)
    ctx.fill()
    tag(ctx, "TOP SE MISSILE", 960, 260, CYAN, 34)
    vignette(ctx)


def network(ctx, S, mode="family"):
    """Logistics web: T-72 / T-90 share workshops, spares and training; Arjun stands on its own island."""
    studio_bg(ctx)
    hub = [(500, 560, "T-72"), (900, 560, "T-90")]
    nodes = [(700, 300, "WORKSHOP"), (380, 820, "SPARES"), (1020, 820, "TRAINING"), (700, 860, "RAIL WAGONS")]
    for (x, y, lab) in nodes:
        for (hx, hy, _) in hub:
            g = clamp((S.t - 0.4) / 0.8)
            line(ctx, [(hx, hy), (lerp(hx, x, g), lerp(hy, y, g))], CYAN, 4, 0.5)
    for (x, y, lab) in nodes:
        a = clamp((S.t - 0.8) / 0.4)
        tag(ctx, lab, x, y, CYAN, 28, a=a)
    for (x, y, lab) in hub:
        circle(ctx, x, y, 90, (0.04, 0.08, 0.12))
        ctx.arc(x, y, 90, 0, math.tau)
        rgba(ctx, CYAN)
        ctx.set_line_width(4)
        ctx.stroke()
        mini_tank(ctx, x, y + 14, 120, "t90", OLIVE_TANK if lab == "T-90" else T72_C)
        text(ctx, lab, x, y + 130, 38, CYAN, font=IMPACT)
    if mode in ("family", "arjun"):
        a = clamp((S.t - 1.0) / 0.5)
        ax, ay = 1520, 560
        ctx.set_dash([12, 10])
        ctx.arc(ax, ay, 210, 0, math.tau)
        rgba(ctx, GOLD, 0.7 * a)
        ctx.set_line_width(3)
        ctx.stroke()
        ctx.set_dash([])
        mini_tank(ctx, ax, ay + 20, 200, "arjun", SAND_TANK, a)
        text(ctx, "ARJUN", ax, ay + 110, 40, GOLD, font=IMPACT, a=a)
        text(ctx, "ALAG INTEZAAM", ax, ay - 130, 28, GOLD, font=MONO, a=a)
    tag(ctx, "EK HI PARIVAAR" if mode == "family" else "PEHLE SE TAIYAAR DHAANCHA", 700, 160, CYAN, 32)
    vignette(ctx, 0.45)


def low_profile(ctx, S):
    """Height comparison: Arjun vs T-90 side by side with a height ruler."""
    blueprint_bg(ctx)
    tank(ctx, 560, 820, 0.95, "arjun", outline=GOLD)
    tank(ctx, 1380, 820, 0.95, "t90", outline=CYAN)
    ha = 820 - (2 * 26 + 14 + 72 + 88 + 22) * 0.95
    ht = 820 - (2 * 25 + 14 + 58 + 70 + 16) * 0.95
    g = ease_out_cubic(clamp((S.t - 0.4) / 0.8))
    for y, c in ((ha, GOLD), (ht, CYAN)):
        ctx.set_dash([10, 8])
        line(ctx, [(120, y), (lerp(120, W - 120, g), y)], c, 3, 0.8)
        ctx.set_dash([])
    text(ctx, "ARJUN", 560, 900, 44, GOLD, font=IMPACT)
    text(ctx, "T-90", 1380, 900, 44, CYAN, font=IMPACT)
    tag(ctx, "NEECHA = DUSHMAN KO KAM DIKHE", W / 2, 230, CYAN, 32, a=clamp((S.t - 1.0) / 0.4))
    vignette(ctx, 0.5)


def montage(ctx, S):
    """Five issue icons: weight, bridge, rail, engine, money."""
    studio_bg(ctx)
    items = [("VAZAN", RED), ("PUL", SAFFRON), ("RAIL", CYAN), ("ENGINE", GOLD), ("PAISA", GREEN)]
    for i, (lab, c) in enumerate(items):
        x = 260 + i * 350
        y = 520
        a = ease_out_back(clamp((S.t - 0.2 - i * 0.22) / 0.5))
        if a <= 0:
            continue
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(a, a)
        circle(ctx, 0, 0, 130, (0.04, 0.06, 0.1))
        ctx.arc(0, 0, 130, 0, math.tau)
        rgba(ctx, c)
        ctx.set_line_width(6)
        ctx.stroke()
        if i == 0:
            ctx.move_to(-50, 50)
            ctx.line_to(50, 50)
            ctx.line_to(36, -30)
            ctx.line_to(-36, -30)
            ctx.close_path()
            rgba(ctx, c)
            ctx.fill()
            ctx.arc(0, -40, 18, 0, math.tau)
            ctx.set_line_width(8)
            ctx.stroke()
            text(ctx, "T", 0, 14, 50, INK, font=IMPACT)
        elif i == 1:
            ctx.move_to(-80, 10)
            ctx.curve_to(-30, -40, 30, -40, 80, 10)
            rgba(ctx, c)
            ctx.set_line_width(12)
            ctx.stroke()
            line(ctx, [(-90, 20), (90, 20)], c, 10)
            for xx in (-40, 40):
                line(ctx, [(xx, 20), (xx, 70)], c, 10)
        elif i == 2:
            rrect(ctx, -80, -20, 160, 40, 6)
            rgba(ctx, c)
            ctx.fill()
            for xx in (-50, 50):
                circle(ctx, xx, 36, 16, c)
            line(ctx, [(-100, 58), (100, 58)], c, 5)
        elif i == 3:
            rrect(ctx, -60, -30, 120, 70, 10)
            rgba(ctx, c)
            ctx.fill()
            for k in range(3):
                ctx.rectangle(-50 + k * 38, -62, 24, 32)
            ctx.fill()
        else:
            for k in range(4):
                rrect(ctx, -60, 40 - k * 26, 120, 20, 4)
                rgba(ctx, c)
                ctx.fill()
        ctx.restore()
        text(ctx, lab, x, y + 190, 44, c, font=IMPACT, a=clamp(a))
    vignette(ctx, 0.45)


def regiment(ctx, S, label="43 ARMOURED REGIMENT  //  2004"):
    """A line of Arjuns rolling past at dawn."""
    desert(ctx, S.T, speed=0, sun=(300, 500))
    for i in range(4):
        x = 2200 - ((S.t * 160 + i * 520) % 2900)
        tank(ctx, x, GROUND + 4 + i * 0, 0.5, "arjun", flip=True, roll=S.T * 6)
        dust(ctx, x + 300, GROUND - 6, S.T + i, 0.5)
    tag(ctx, label, W / 2, 230, GOLD, 34, a=clamp(S.t / 0.4))
    vignette(ctx)


def hero(ctx, S, kind="arjun", label="ARJUN", sub="MAIN BATTLE TANK  //  MADE IN INDIA", c=GOLD):
    """Slow push-in on one tank at sunset with its name."""
    desert(ctx, S.T, speed=6)
    s = lerp(0.85, 0.95, ease_in_out(S.u))
    tank(ctx, 860, GROUND + 30, s, kind, roll=S.T)
    k = ease_out_cubic(clamp((S.t - 0.3) / 0.6))
    big(ctx, label, W / 2, 290, 150 * (0.8 + 0.2 * k), c, a=k)
    text(ctx, sub, W / 2, 395, 34, WHITE, font=MONO, a=k)
    vignette(ctx)


def future(ctx, S, mode="frcv"):
    """FRCV: T-72 fades to a blueprint of a lighter next-gen tank."""
    blueprint_bg(ctx)
    if mode == "frcv":
        k = clamp((S.t - 0.4) / 1.0)
        tank(ctx, 900, 820, 1.0, "t72", a=1 - k)
        tank(ctx, 900, 820, 1.0, "frcv", outline=TEAL, reveal=ease_out_cubic(k))
        big(ctx, "FRCV", W / 2, 230, 130, TEAL, a=k)
        text(ctx, "FUTURE READY COMBAT VEHICLE  //  T-72 KI JAGAH", W / 2, 330, 32, WHITE, font=MONO, a=k)
    elif mode == "lineage":
        a1 = clamp(S.t / 0.5)
        a2 = clamp((S.t - 0.9) / 0.5)
        tank(ctx, 480, 760, 0.7, "arjun", a=a1)
        tank(ctx, 1460, 760, 0.7, "frcv", outline=TEAL, reveal=a2)
        arrow(ctx, (800, 560), (lerp(800, 1080, a2), 560), GOLD, 8, a2)
        text(ctx, "50 SAAL KA TAJURBA", 940, 500, 34, GOLD, font=MONO, a=a2)
        text(ctx, "ARJUN", 480, 830, 40, GOLD, font=IMPACT, a=a1)
        text(ctx, "AGLA DESI TANK", 1460, 830, 40, TEAL, font=IMPACT, a=a2)
    else:  # agile: light tank zips over terrain
        x = lerp(-300, W + 300, S.u)
        for i in range(3):
            ctx.move_to(0, 900)
            for q in range(0, 21):
                ctx.line_to(q * 100, 820 - 40 * math.sin(q * 0.7 + i))
            ctx.line_to(W, 900)
            ctx.close_path()
            rgba(ctx, BP_LINE, 0.08 + 0.05 * i)
            ctx.fill()
        tank(ctx, x, 830 - 40 * math.sin((x / 100) * 0.7 + 2), 0.6, "frcv", outline=TEAL, roll=-S.T * 8)
        tag(ctx, "MADHYAM VAZAN  //  FURTILA", W / 2, 230, TEAL, 34)
    vignette(ctx, 0.5)


def question(ctx, S):
    """A/B cards over a dimmed duel, arrow down to the comments."""
    duel(ctx, S, mode="face", labels=False)
    rgba(ctx, (0, 0, 0), 0.5)
    ctx.paint()
    opts = [("A", "ARJUN BEHTAR", ARJ_C), ("B", "T-90 BEHTAR", T90_C)]
    for i, (k, s, c) in enumerate(opts):
        g = ease_out_back(clamp((S.t - 0.3 - i * 0.35) / 0.6))
        if g <= 0:
            continue
        x = W / 2 - 430 + i * 860
        ctx.save()
        ctx.translate(x, 450)
        ctx.scale(g, g)
        rrect(ctx, -380, -110, 760, 220, 22)
        rgba(ctx, (0.03, 0.05, 0.09), 0.92)
        ctx.fill_preserve()
        rgba(ctx, c)
        ctx.set_line_width(5)
        ctx.stroke()
        circle(ctx, -280, 0, 60, c)
        text(ctx, k, -280, 0, 70, INK, font=IMPACT)
        text(ctx, s, 50, 0, 58, WHITE, font=IMPACT)
        ctx.restore()
    a = clamp((S.t - 1.2) / 0.4)
    yb = 770 + 14 * math.sin(S.T * 6)
    text(ctx, "COMMENT MEIN A YA B LIKHO", W / 2, 700, 46, GOLD, font=IMPACT, a=a)
    ctx.move_to(W / 2 - 34, yb)
    ctx.line_to(W / 2 + 34, yb)
    ctx.line_to(W / 2, yb + 50)
    ctx.close_path()
    rgba(ctx, GOLD, a)
    ctx.fill()


def finale(ctx, S):
    hero(ctx, S, kind="arjun1a", label="JAI HIND", sub="REALITY SHIFT", c=SAFFRON)


# ============================================================ script
# each line: (spoken Hindi for KikiVoice, Roman caption, shot, params)
D = duel
BPR = blueprint

CHAPTERS = [
    {"key": "hook", "title": "DESI TANK KA PARADOX", "lines": [
        ("सोचो भारत में बना एक टैंक रेगिस्तान में टी नब्बे से सीधा मुकाबला करता है।",
         "SOCHO BHARAT MEIN BANA EK TANK REGISTAAN MEIN T-90 SE SEEDHA MUKABLA KARTA HAI", D, dict(mode="face")),
        ("और रिपोर्ट्स के मुताबिक कई मामलों में उससे बेहतर निकलता है।",
         "AUR REPORTS KE MUTABIK KAI MAAMLON MEIN USSE BEHTAR NIKALTA HAI", D, dict(mode="fire_arjun")),
        ("निशाना भी पक्का और रेत पर रफ्तार भी अच्छी।",
         "NISHANA BHI PAKKA AUR RET PAR RAFTAAR BHI ACHCHHI", D, dict(mode="race")),
        ("फिर भी फौज ने पहले उसके सिर्फ एक सौ चौबीस टैंक लिए।",
         "PHIR BHI FAUJ NE PEHLE USKE SIRF 124 TANK LIYE", fleet,
         dict(groups=[("ARJUN MK1", 124, "124", ARJ_C, "arjun")])),
        ("जबकि टी नब्बे हज़ार से भी ज़्यादा लिए गए।",
         "JABKI T-90 HAZAAR SE BHI ZYADA LIYE GAYE", fleet,
         dict(groups=[("ARJUN MK1", 124, "124", ARJ_C, "arjun"), ("T-90 BHISHMA", 1000, "1000+", T90_C, "t90")],
              per=20)),
        ("इस देसी टैंक का नाम है अर्जुन।", "IS DESI TANK KA NAAM HAI ARJUN", hero, {}),
        ("और इसकी कहानी करीब पचास साल पुरानी है।", "AUR ISKI KAHANI KAREEB 50 SAAL PURANI HAI", timeline,
         dict(focus=0)),
        ("तो क्या फौज ने अपने ही देसी टैंक के साथ नाइंसाफी की।",
         "TOH KYA FAUJ NE APNE HI DESI TANK KE SAATH NAINSAAFI KI", D, dict(mode="versus", lit="arjun")),
        ("या फिर फौज के पास अपनी ठोस वजहें थीं।", "YA PHIR FAUJ KE PAAS APNI THOS VAJAHEIN THIN", D,
         dict(mode="versus", lit="t90")),
        ("आज दोनों तरफ की बात सुनेंगे भाई।", "AAJ DONON TARAF KI BAAT SUNENGE BHAI", D, dict(mode="versus")),
        ("वज़न पुल रेल इंजन और पैसा सब कुछ।", "VAZAN PUL RAIL ENGINE AUR PAISA SAB KUCHH", montage, {}),
        ("और आखिर में फैसला आपके हाथ में होगा।", "AUR AAKHIR MEIN FAISLA AAPKE HAATH MEIN HOGA", question, {}),
    ]},
    {"key": "origin", "title": "1974 KA SAPNA", "lines": [
        ("बात शुरू होती है उन्नीस सौ चौहत्तर से।", "BAAT SHURU HOTI HAI 1974 SE", timeline, dict(focus=0)),
        ("सरकार ने तय किया कि भारत अपना खुद का बड़ा टैंक बनाएगा।",
         "SARKAR NE TAY KIYA KI BHARAT APNA KHUD KA BADA TANK BANAYEGA", BPR,
         dict(kind="arjun", title="APNA TANK", name="PROJECT  //  1974")),
        ("बाद में ये काम डी आर डी ओ की उस लैब को मिला जो चेन्नई के पास आवडी में है।",
         "BAAD MEIN YEH KAAM DRDO KI US LAB KO MILA JO CHENNAI KE PAAS AVADI MEIN HAI", factory,
         dict(lab=True, sign="AVADI  //  CHENNAI")),
        ("उस वक्त अंदाज़ा था कि खर्च करीब साढ़े पंद्रह करोड़ रुपये आएगा।",
         "US WAQT ANDAAZA THA KI KHARCH KAREEB 15.5 CRORE RUPAYE AAYEGA", money, {}),
        ("पर टैंक बनाना आसान काम नहीं होता।", "PAR TANK BANANA AASAAN KAAM NAHI HOTA", BPR,
         dict(kind="arjun", callouts=[("TOP", *GUN_PT, 1500, 330), ("ENGINE", *ENGINE_PT, 300, 380)])),
        ("इंजन गियरबॉक्स तोप और कवच सब कुछ एक साथ सही बैठना चाहिए।",
         "ENGINE GEARBOX TOP AUR KAVACH SAB KUCHH EK SAATH SAHI BAITHNA CHAHIYE", BPR,
         dict(kind="arjun", callouts=[("ENGINE", *ENGINE_PT, 300, 380), ("GEARBOX", -250, -60, 260, 520),
                                      ("TOP", *GUN_PT, 1500, 330), ("KAVACH", *ARMOR_PT, 1400, 470)])),
        ("पहला प्रोटोटाइप बना उन्नीस सौ नवासी में।", "PEHLA PROTOTYPE BANA 1989 MEIN", timeline, dict(focus=1)),
        ("फिर सालों तक ट्रायल चले और कमियां भी निकलीं।", "PHIR SAALON TAK TRIAL CHALE AUR KAMIYAN BHI NIKLIN",
         D, dict(mode="race", labels=False)),
        ("इंजन गरम होने जैसी शिकायतें आईं और फौज की मांगें भी बदलती रहीं।",
         "ENGINE GARAM HONE JAISI SHIKAYATEIN AAYIN AUR FAUJ KI MAANGEIN BHI BADALTI RAHIN", engine_shot,
         dict(mode="heat")),
        ("उन्नीस सौ पचानवे तक विकास का खर्च बढ़कर करीब तीन सौ सात करोड़ हो गया।",
         "1995 TAK VIKAS KA KHARCH BADHKAR KAREEB 307 CRORE HO GAYA", money,
         dict(start=15.5, end=307.48, label="RS 307 CRORE", sub="1995 TAK VIKAS KA KHARCH", fmt="{:.0f}")),
        ("आखिर सन दो हज़ार में फौज ने एक सौ चौबीस अर्जुन का ऑर्डर दिया।",
         "AAKHIR SAN 2000 MEIN FAUJ NE 124 ARJUN KA ORDER DIYA", fleet,
         dict(groups=[("PEHLA ORDER  //  2000", 124, "124", ARJ_C, "arjun")])),
        ("और दो हज़ार चार में पहली रेजिमेंट को ये टैंक मिल गए।",
         "AUR 2004 MEIN PEHLI REGIMENT KO YEH TANK MIL GAYE", regiment, {}),
    ]},
    {"key": "power", "title": "ARJUN KI TAAKAT", "lines": [
        ("अब देखते हैं कि अर्जुन में खास क्या है।", "AB DEKHTE HAIN KI ARJUN MEIN KHAAS KYA HAI", BPR,
         dict(kind="arjun", name="ARJUN MK1")),
        ("इसमें एक सौ बीस मिलीमीटर की बड़ी तोप है।", "ISMEIN 120 MILLIMETER KI BADI TOP HAI", BPR,
         dict(kind="arjun", callouts=[("120 MM TOP", *GUN_PT, 1450, 330)])),
        ("और चलते चलते भी ये निशाना साध सकता है।", "AUR CHALTE CHALTE BHI YEH NISHANA SAADH SAKTA HAI", D,
         dict(mode="fire_arjun", labels=False)),
        ("इसके अंदर चार जवान बैठते हैं।", "ISKE ANDAR 4 JAWAN BAITHTE HAIN", crew, dict(n=4, kind="arjun")),
        ("इसका इंजन चौदह सौ हॉर्सपावर का है।", "ISKA ENGINE 1400 HORSEPOWER KA HAI", BPR,
         dict(kind="arjun", callouts=[("1400 HP ENGINE", *ENGINE_PT, 300, 380)])),
        ("और इसके कवच को कंचन कवच कहा जाता है जो भारत में ही बना।",
         "AUR ISKE KAVACH KO KANCHAN KAVACH KAHA JAATA HAI JO BHARAT MEIN HI BANA", BPR,
         dict(kind="arjun", callouts=[("KANCHAN KAVACH", *ARMOR_PT, 1400, 450)])),
        ("पहले मॉडल का वज़न करीब साढ़े अट्ठावन टन था।", "PEHLE MODEL KA VAZAN KAREEB 58.5 TAN THA", weighbridge,
         dict(items=[("arjun", 58.5, "ARJUN MK1")])),
        ("यानी ये बड़ा मज़बूत और भारी टैंक है।", "YAANI YEH BADA MAZBOOT AUR BHAARI TANK HAI", hero,
         dict(sub="BHAARI  //  MAZBOOT")),
        ("इसके फैन कहते हैं कि ये अपने जवानों को ज़्यादा अच्छे से बचाता है।",
         "ISKE FAN KEHTE HAIN KI YEH APNE JAWANON KO ZYADA ACHCHHE SE BACHATA HAI", crew, dict(n=4, kind="arjun")),
        ("और यहीं से शुरू होती है असली बहस।", "AUR YAHIN SE SHURU HOTI HAI ASLI BEHES", D, dict(mode="versus")),
    ]},
    {"key": "trials", "title": "RAJASTHAN KA MUKABLA", "lines": [
        ("साल दो हज़ार दस में फौज ने एक बड़ा मुकाबला करवाया।", "SAAL 2010 MEIN FAUJ NE EK BADA MUKABLA KARWAYA",
         timeline, dict(focus=3)),
        ("राजस्थान के रेगिस्तान में बीकानेर के पास महाजन रेंज में।",
         "RAJASTHAN KE REGISTAAN MEIN BIKANER KE PAAS MAHAJAN RANGE MEIN", hero,
         dict(kind="arjun", label="MAHAJAN RANGE", sub="BIKANER  //  RAJASTHAN  //  2010", c=SAFFRON)),
        ("एक तरफ चौदह अर्जुन और दूसरी तरफ चौदह टी नब्बे।", "EK TARAF 14 ARJUN AUR DOOSRI TARAF 14 T-90", fleet,
         dict(groups=[("ARJUN", 14, "14", ARJ_C, "arjun"), ("T-90", 14, "14", T90_C, "t90")], per=1,
              note="1 ICON = 1 TANK  //  EK SQUADRON VS EK SQUADRON")),
        ("रेत में दूर तक दौड़ना था और निशाना भी लगाना था।", "RET MEIN DOOR TAK DAUDNA THA AUR NISHANA BHI LAGANA THA",
         D, dict(mode="race")),
        ("रात में भी गोले दागने थे।", "RAAT MEIN BHI GOLE DAAGNE THE", D, dict(mode="night", labels=False)),
        ("इस मुकाबले के पूरे नतीजे कभी खुलकर सामने नहीं आए।",
         "IS MUKABLE KE POORE NATEEJE KABHI KHULKAR SAAMNE NAHI AAYE", sealed, {}),
        ("पर रिपोर्ट्स के मुताबिक अर्जुन ने कई पैमानों पर टी नब्बे को पीछे छोड़ दिया।",
         "PAR REPORTS KE MUTABIK ARJUN NE KAI PAIMAANON PAR T-90 KO PEECHHE CHHOD DIYA", scoreboard, {}),
        ("निशाने में भी और रेत पर रफ्तार में भी।", "NISHANE MEIN BHI AUR RET PAR RAFTAAR MEIN BHI", D,
         dict(mode="fire_both")),
        ("बाद में देश के ऑडिटर सी ए जी की एक रिपोर्ट ने एक और बात कही।",
         "BAAD MEIN DESH KE AUDITOR CAG KI EK REPORT NE EK AUR BAAT KAHI", sealed,
         dict(title="CAG REPORT", stamp="AUDIT KI NAZAR")),
        ("कि दोनों टैंकों को एक जैसे पैमाने पर नहीं परखा गया था।",
         "KI DONON TANKON KO EK JAISE PAIMAANE PAR NAHI PARKHA GAYA THA", balance, {}),
        ("अर्जुन के फैन आज भी यही ट्रायल याद दिलाते हैं।", "ARJUN KE FAN AAJ BHI YAHI TRIAL YAAD DILAATE HAIN",
         hero, dict(sub="2010 KA TRIAL  //  FANS KI DALEEL")),
        ("पर फौज का जवाब कुछ और था।", "PAR FAUJ KA JAWAB KUCHH AUR THA", D, dict(mode="versus", lit="t90")),
    ]},
    {"key": "weight", "title": "68 TAN KA SAWAAL", "lines": [
        ("फौज की सबसे बड़ी चिंता थी अर्जुन का वज़न।", "FAUJ KI SABSE BADI CHINTA THI ARJUN KA VAZAN", weighbridge,
         dict(items=[("arjun", 58.5, "ARJUN MK1")])),
        ("नया मॉडल मार्क वन ए करीब अड़सठ टन का है।", "NAYA MODEL MK1A KAREEB 68 TAN KA HAI", weighbridge,
         dict(items=[("arjun", 58.5, "ARJUN MK1"), ("arjun1a", 68, "ARJUN MK1A")])),
        ("जबकि टी नब्बे करीब छियालीस टन का है।", "JABKI T-90 KAREEB 46 TAN KA HAI", weighbridge,
         dict(items=[("arjun1a", 68, "ARJUN MK1A"), ("t90", 46, "T-90")])),
        ("यानी दोनों में बीस टन से भी ज़्यादा का फर्क।", "YAANI DONON MEIN 20 TAN SE BHI ZYADA KA FARAK", weighbridge,
         dict(items=[("arjun1a", 68, "ARJUN MK1A"), ("t90", 46, "T-90")], diff=True)),
        ("अब सोचो जंग के वक्त टैंक को एक नहर पार करनी है।", "AB SOCHO JUNG KE WAQT TANK KO EK NAHAR PAAR KARNI HAI",
         bridge, dict(kind="arjun", fail=False)),
        ("तो सरहद के पास के कई पुल इतने भारी वज़न के लिए बने ही नहीं।",
         "TOH SARHAD KE PAAS KE KAI PUL ITNE BHAARI VAZAN KE LIYE BANE HI NAHI", bridge,
         dict(kind="arjun", sign2="ITNA VAZAN NAHI")),
        ("रिपोर्ट्स के मुताबिक सत्तर टन वाले पुल वहां ज़्यादा नहीं हैं।",
         "REPORTS KE MUTABIK 70 TAN WAALE PUL WAHAN ZYADA NAHI HAIN", bridge,
         dict(kind="arjun", limit="70 T", sign2="70 TAN KE PUL KAM")),
        ("फिर टैंक को ट्रेन से एक मोर्चे से दूसरे मोर्चे तक ले जाना होता है।",
         "PHIR TANK KO TRAIN SE EK MORCHE SE DOOSRE MORCHE TAK LE JAANA HOTA HAI", rail, dict(kind="t90")),
        ("और अर्जुन के लिए खास तरह के डिब्बे चाहिए।", "AUR ARJUN KE LIYE KHAAS TARAH KE DIBBE CHAHIYE", rail,
         dict(kind="arjun1a")),
        ("उसकी मरम्मत और पुर्ज़ों का इंतज़ाम भी अलग रखना पड़ता है।",
         "USKI MARAMMAT AUR PURZON KA INTEZAAM BHI ALAG RAKHNA PADTA HAI", network, dict(mode="family")),
        ("इसलिए अर्जुन ज़्यादातर पश्चिमी रेगिस्तान तक ही सीमित रहा।",
         "ISLIYE ARJUN ZYADATAR PASHCHIMI REGISTAAN TAK HI SEEMIT RAHA", terrain,
         dict(kind="arjun", marks=("ok", None, None), hi=0)),
        ("पंजाब की नहरों और लद्दाख के पहाड़ों में उसे ले जाना मुश्किल माना गया।",
         "PUNJAB KI NAHARON AUR LADAKH KE PAHADON MEIN USE LE JAANA MUSHKIL MAANA GAYA", terrain,
         dict(kind="arjun", marks=("ok", "x", "x"))),
    ]},
    {"key": "t90", "title": "T-90 KA PAKSH", "lines": [
        ("अब फौज की तरफ से टी नब्बे की बात करते हैं।", "AB FAUJ KI TARAF SE T-90 KI BAAT KARTE HAIN", hero,
         dict(kind="t90", label="T-90", sub="FAUJ KA PAKSH", c=CYAN)),
        ("भारत में इसे भीष्म कहा जाता है।", "BHARAT MEIN ISE BHISHMA KAHA JAATA HAI", hero,
         dict(kind="t90", label="BHISHMA", sub="T-90S  //  BHARAT KI FAUJ MEIN", c=CYAN)),
        ("ये हल्का है और नीचा है तो दुश्मन को कम दिखता है।",
         "YEH HALKA HAI AUR NEECHA HAI TOH DUSHMAN KO KAM DIKHTA HAI", low_profile, {}),
        ("इसकी तोप एक सौ पच्चीस मिलीमीटर की है और गोले अपने आप लोड होते हैं।",
         "ISKI TOP 125 MILLIMETER KI HAI AUR GOLE APNE AAP LOAD HOTE HAIN", crew,
         dict(n=3, kind="t90", autoloader=True)),
        ("इसलिए इसमें तीन ही जवान बैठते हैं।", "ISLIYE ISMEIN 3 HI JAWAN BAITHTE HAIN", crew,
         dict(n=3, kind="t90", autoloader=True)),
        ("और ये अपनी तोप से मिसाइल भी दाग सकता है।", "AUR YEH APNI TOP SE MISSILE BHI DAAG SAKTA HAI", missile, {}),
        ("सबसे बड़ी बात ये कि फौज का पूरा ढांचा पहले से ऐसे टैंकों के लिए बना था।",
         "SABSE BADI BAAT YEH KI FAUJ KA POORA DHAANCHA PEHLE SE AISE TANKON KE LIYE BANA THA", network,
         dict(mode="ready")),
        ("टी बहत्तर और टी नब्बे एक ही परिवार के टैंक हैं।", "T-72 AUR T-90 EK HI PARIVAAR KE TANK HAIN", network,
         dict(mode="family")),
        ("तो ट्रेनिंग पुर्ज़े और वर्कशॉप सब पहले से तैयार थे।",
         "TOH TRAINING PURZE AUR WORKSHOP SAB PEHLE SE TAIYAAR THE", network, dict(mode="ready")),
        ("और ये टैंक आवडी की उसी फैक्ट्री में लाइसेंस से बनने लगे।",
         "AUR YEH TANK AVADI KI USI FACTORY MEIN LICENCE SE BANNE LAGE", factory, dict(kind="t90")),
        ("दो हज़ार उन्नीस में चार सौ चौंसठ और टी नब्बे का ऑर्डर दिया गया।",
         "2019 MEIN 464 AUR T-90 KA ORDER DIYA GAYA", fleet,
         dict(groups=[("NAYA ORDER  //  2019", 464, "464", T90_C, "t90")])),
        ("दो हज़ार बीस में लद्दाख तक में ऐसे टैंक तैनात होने की खबरें आईं।",
         "2020 MEIN LADAKH TAK MEIN AISE TANK TAINAAT HONE KI KHABREIN AAYIN", terrain,
         dict(kind="t90", marks=(None, None, "ok"), hi=2)),
        ("फौज का तर्क सीधा है कि टैंक वही जो हर मोर्चे तक पहुंच सके।",
         "FAUJ KA TARK SEEDHA HAI KI TANK WAHI JO HAR MORCHE TAK PAHUNCH SAKE", terrain,
         dict(kind="t90", marks=("ok", "ok", "ok"))),
    ]},
    {"key": "mk1a", "title": "MK1A AUR ENGINE KA PENCH", "lines": [
        ("फिर भी अर्जुन की कहानी खत्म नहीं हुई।", "PHIR BHI ARJUN KI KAHANI KHATM NAHI HUI", hero,
         dict(kind="arjun1a", label="ARJUN MK1A", sub="NAYA MODEL")),
        ("दो हज़ार इक्कीस में सरकार ने एक सौ अठारह अर्जुन मार्क वन ए का ऑर्डर दिया।",
         "2021 MEIN SARKAR NE 118 ARJUN MK1A KA ORDER DIYA", fleet,
         dict(groups=[("ARJUN MK1A  //  2021", 118, "118", ARJ_C, "arjun1a")])),
        ("ये सौदा करीब सात हज़ार पांच सौ तेईस करोड़ रुपये का था।",
         "YEH SAUDA KAREEB 7,523 CRORE RUPAYE KA THA", money,
         dict(start=0, end=7523, label="RS 7,523 CRORE", sub="118 TANKS  //  SEPT 2021", fmt="{:,.0f}")),
        ("नए मॉडल में बहत्तर सुधार किए गए जिनमें चौदह बड़े सुधार थे।",
         "NAYE MODEL MEIN 72 SUDHAAR KIYE GAYE JINMEIN 14 BADE SUDHAAR THE", BPR,
         dict(kind="arjun1a", title="72 SUDHAAR", name="14 BADE  //  58 CHHOTE",
              callouts=[("NAYA KAVACH", *ARMOR_PT, 1400, 470), ("BEHTAR SIGHT", *CREW_PT, 300, 400)])),
        ("पर एक बड़ी दिक्कत आज तक पीछा नहीं छोड़ रही।", "PAR EK BADI DIKKAT AAJ TAK PEECHHA NAHI CHHOD RAHI",
         engine_shot, dict(mode="import")),
        ("अर्जुन का दिल यानी इंजन जर्मनी की एक कंपनी से आता था।",
         "ARJUN KA DIL YAANI ENGINE GERMANY KI EK COMPANY SE AATA THA", engine_shot, dict(mode="import")),
        ("रिपोर्ट्स के मुताबिक वो इंजन अब बनना बंद हो चुका है।",
         "REPORTS KE MUTABIK WOH ENGINE AB BANNA BAND HO CHUKA HAI", engine_shot, dict(mode="cut")),
        ("इसलिए नए टैंकों की डिलीवरी सालों पीछे खिसक गई है।", "ISLIYE NAYE TANKON KI DELIVERY SAALON PEECHHE KHISAK GAYI HAI",
         calendar, {}),
        ("इससे पहले भी पुर्ज़ों की कमी ने अर्जुन को बहुत परेशान किया।",
         "ISSE PEHLE BHI PURZON KI KAMI NE ARJUN KO BAHUT PARESHAAN KIYA", grounded, {}),
        ("रिपोर्ट्स के मुताबिक दो हज़ार तेरह से पंद्रह के बीच करीब पचहत्तर फीसदी अर्जुन खड़े रह गए थे।",
         "REPORTS KE MUTABIK 2013 SE 2015 KE BEECH KAREEB 75 PERCENT ARJUN KHADE REH GAYE THE", grounded, {}),
        ("अब भारत अपना देसी इंजन बना रहा है जिसका नाम डेट्रान है।",
         "AB BHARAT APNA DESI ENGINE BANA RAHA HAI JISKA NAAM DATRAN HAI", engine_shot, dict(mode="datran")),
        ("पंद्रह सौ हॉर्सपावर का ये इंजन अभी टेस्ट हो रहा है।", "1500 HORSEPOWER KA YEH ENGINE ABHI TEST HO RAHA HAI",
         engine_shot, dict(mode="datran")),
    ]},
    {"key": "future", "title": "AAGE KA RAASTA", "lines": [
        ("अब बात भविष्य की।", "AB BAAT BHAVISHYA KI", future, dict(mode="frcv")),
        ("फौज पुराने टी बहत्तर टैंकों की जगह नए टैंक लाना चाहती है।",
         "FAUJ PURANE T-72 TANKON KI JAGAH NAYE TANK LAANA CHAHTI HAI", future, dict(mode="frcv")),
        ("इस योजना का नाम है एफ आर सी वी।", "IS YOJANA KA NAAM HAI FRCV", future, dict(mode="frcv")),
        ("दो हज़ार इक्कीस में फौज ने करीब सत्रह सौ सत्तर ऐसे टैंकों के लिए जानकारी मांगी।",
         "2021 MEIN FAUJ NE KAREEB 1770 AISE TANKON KE LIYE JAANKARI MAANGI", fleet,
         dict(groups=[("FRCV  //  RFI 2021", 1770, "1770", TEAL, "frcv")], per=20)),
        ("और शर्त थी कि टैंक मध्यम वज़न का हो।", "AUR SHART THI KI TANK MADHYAM VAZAN KA HO", future, dict(mode="agile")),
        ("यानी फौज ने साफ कर दिया कि उसे भारी नहीं फुर्तीला टैंक चाहिए।",
         "YAANI FAUJ NE SAAF KAR DIYA KI USE BHAARI NAHI PHURTILA TANK CHAHIYE", future, dict(mode="agile")),
        ("पर अर्जुन बनाने में जो पचास साल का तजुर्बा मिला वो बेकार नहीं गया।",
         "PAR ARJUN BANANE MEIN JO 50 SAAL KA TAJURBA MILA WOH BEKAAR NAHI GAYA", future, dict(mode="lineage")),
        ("तोप कवच और इंजन की यही समझ अगले देसी टैंक की नींव बनेगी।",
         "TOP KAVACH AUR ENGINE KI YAHI SAMAJH AGLE DESI TANK KI NEENV BANEGI", future, dict(mode="lineage")),
        ("और यहां दोनों तरफ के लोग एक बात पर सहमत हैं।", "AUR YAHAN DONON TARAF KE LOG EK BAAT PAR SAHMAT HAIN", D,
         dict(mode="face")),
        ("कि भारत को अपना टैंक आखिर में खुद ही बनाना होगा।", "KI BHARAT KO APNA TANK AAKHIR MEIN KHUD HI BANANA HOGA",
         factory, dict(kind="arjun1a")),
    ]},
    {"key": "ask", "title": "AAPKA FAISLA", "lines": [
        ("तो एक तरफ है अर्जुन जिसने ट्रायल में दम दिखाया।", "TOH EK TARAF HAI ARJUN JISNE TRIAL MEIN DUM DIKHAYA", D,
         dict(mode="versus", lit="arjun")),
        ("और दूसरी तरफ है टी नब्बे जो हर मोर्चे पर फिट बैठता है।",
         "AUR DOOSRI TARAF HAI T-90 JO HAR MORCHE PAR FIT BAITHTA HAI", D, dict(mode="versus", lit="t90")),
        ("इब थारी बारी है भाई।", "IB THAARI BAARI HAI BHAI", question, {}),
        ("आपके हिसाब से अर्जुन बेहतर है या टी नब्बे।", "AAPKE HISAAB SE ARJUN BEHTAR HAI YA T-90", question, {}),
        ("अर्जुन के लिए ए लिखो और टी नब्बे के लिए बी लिखो।", "ARJUN KE LIYE A LIKHO AUR T-90 KE LIYE B LIKHO", question,
         {}),
        ("और साथ में अपनी वजह भी ज़रूर लिखना।", "AUR SAATH MEIN APNI VAJAH BHI ZAROOR LIKHNA", question, {}),
        ("ऐसी ही देसी हथियारों की कहानियों के लिए चैनल को सब्सक्राइब कर लो।",
         "AISI HI DESI HATHIYAARON KI KAHANIYON KE LIYE CHANNEL KO SUBSCRIBE KAR LO", finale, {}),
        ("जय हिंद।", "JAI HIND", finale, {}),
    ]},
]

SOURCES = [
    "Arjun programme authorised 1974; CVRDE (DRDO, Avadi) set up 1976; first prototype 1989; cost estimate Rs 15.50 "
    "crore (1974) -> development cost Rs 307.48 crore (1995); 1993-96 trial defects incl. engine overheating "
    "(Wikipedia 'Arjun (tank)', citing DRDO/CAG/parliament records)",
    "124 Arjun Mk1 ordered 2000; 43 Armoured Regiment equipped 2004, 75 Armoured Regiment by 2009 (Wikipedia; "
    "Ministry of Defence statements)",
    "Mk1: 120 mm rifled gun, 4 crew, MTU MB 838 Ka-501 1,400 hp engine (German), Kanchan armour, ~58.5 t "
    "(Wikipedia 'Arjun (tank)')",
    "2010 comparative trials, Mahajan Ranges near Bikaner: one squadron (14) Arjun vs 14 T-90; official results not "
    "published; participants told Business Standard the Arjun did better (Ajai Shukla, Business Standard, 25 Mar 2010; "
    "DRDO newsletter via LiveFist). CAG later said the two tanks were not judged on a level playing field (Tribune)",
    "Mk1A order: 118 tanks, ~Rs 7,523 crore, HVF Avadi, 23 Sept 2021; 72 improvements (14 major, 58 minor) "
    "(PIB/MoD via Deccan Herald, Business Today, Tribune 24 Sept 2021); Mk1A ~68 t (Wikipedia; ThePrint says 68.5 t)",
    "Weight/logistics criticism: few 70-t class bridges near the border, special rail wagons, separate logistics, "
    "Arjun largely limited to the western desert; ThePrint called 2021 the likely last order (ThePrint 'Why the "
    "army's order for 118 Arjuns is its last'; The Wire; Asian Age 26 Feb 2018)",
    "Spares shortage: ~75% of Arjuns grounded 2013-2015, resolved by 2016 (Wikipedia, citing parliamentary/press "
    "reports) - phrased as 'reports ke mutabik'",
    "Engine problem: MTU 838 out of production, Mk1A deliveries delayed; DATRAN 1500 hp indigenous engine, first "
    "test 2023, retested March 2024 (Wikipedia; ThePrint; Janes 'India's Arjun Mk 1A programme faces delay'; "
    "idrw.org / 19FortyFive 2026 - delivery dates are estimates, phrased as 'reports ke mutabik')",
    "T-90S 'Bhishma': ~46 t, 125 mm smoothbore gun with autoloader, 3 crew, gun-launched missile; licence-built at "
    "HVF Avadi; 464 more ordered Nov 2019 (~USD 2.8 bn) (Janes 11 Nov 2019; army-technology.com; DDP MoD page)",
    "T-90 and T-72 deployed in eastern Ladakh during the 2020 stand-off (widely reported, 2020) - phrased as "
    "'khabrein aayin'",
    "FRCV: RFI June 2021 for ~1,770 medium-weight future tanks to replace the T-72 fleet (Janes 'Indian Army issues "
    "RFI for 1,770 future tanks'; Shephard Media)",
]

UPLOAD = {
    "title": "Arjun Tank: Desi Tank Jise Army Ne Poora Nahi Apnaya | Arjun vs T-90",
    "description": """
Desi Arjun tank ne 2010 ke desert trials mein (reports ke mutabik) T-90 ko kai paimaanon par peechhe chhoda -
phir bhi Army ne pehle sirf 124 Arjun liye aur T-90 Bhishma hazaar se zyada. Kyun? Is video mein dono taraf ki
poori baat: 1974 se shuru hua DRDO ka sapna, Arjun ki 120 mm top aur Kanchan kavach, Mahajan range ka mukabla,
68 tan ka vazan aur pul-rail ki mushkil, T-90 ka paksh (halka, neecha, autoloader, ek hi parivaar ka dhaancha),
Arjun Mk1A ka Rs 7,523 crore ka order, engine ki dikkat aur desi DATRAN engine, aur aage ka raasta - FRCV.

Yeh ek debate video hai: engineering, kharch aur fauj ki zaroorat ki baat - kisi party ya desh par hamla nahi.

Aapki raay: Arjun behtar hai (A) ya T-90 (B)? Comment mein likho - aur vajah bhi.

Saare facts public reports par based hain (sources neeche). Jahan baat sirf reports tak hai, wahan video mein
"reports ke mutabik" kaha gaya hai. Sources:
- Wikipedia: Arjun (tank) - development history, specs, trials, spares
- PIB / Deccan Herald / Business Today (24 Sept 2021): 118 Arjun Mk1A, Rs 7,523 crore, 72 improvements
- Business Standard, Ajai Shukla (25 Mar 2010): Arjun vs T-90 trials at Mahajan
- The Tribune: CAG on the 2010 trial benchmarks
- ThePrint: why the 118 Arjun order is the last; The Wire / Asian Age: weight and deployment limits
- Janes: T-90 order of 464 (Nov 2019); Arjun Mk1A delay; FRCV RFI for 1,770 tanks (2021)
""",
    "hashtags": "#ArjunTank #T90 #IndianArmy #DRDO #RealityShift",
    "tags": ["arjun tank", "arjun vs t90", "arjun mk1a", "arjun tank kyun nahi liya", "t-90 bhishma",
             "indian army tanks", "drdo arjun", "arjun tank explained hindi", "frcv india", "datran engine",
             "main battle tank india", "arjun mbt", "india defence hindi", "reality shift"],
    "pinned": "Seedha sawaal: Aapke hisaab se ARJUN behtar hai (A) ya T-90 BHISHMA (B)? A ya B likho - aur ek "
              "line mein vajah bhi. Vazan, pul aur logistics jeetne chahiye ya trial ka performance?",
}


def thumbnail(ctx):
    """Arjun (left, sunlit gold) vs T-90 (right, cold cyan) nose to nose; 'ARJUN YA T-90' + red question box."""
    desert(ctx, 0.0, speed=0, sun=(960, 560))
    glow(ctx, 960, 600, 520, (1, 0.6, 0.25), 0.35)
    tank(ctx, 520, 960, 1.0, "arjun")
    tank(ctx, 1420, 960, 0.95, "t90", flip=True)
    glow(ctx, 380, 760, 300, GOLD, 0.18)
    glow(ctx, 1540, 760, 300, CYAN, 0.16)
    vignette(ctx, 0.55)
    g = cairo.LinearGradient(0, 0, 0, H * 0.5)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.8)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g)
    ctx.paint()
    gap = 50
    tw1 = text_width(ctx, "ARJUN", 210, font=IMPACT) + gap
    tw2 = text_width(ctx, "YA", 210, font=IMPACT) + gap
    tw3 = text_width(ctx, "T-90", 210, font=IMPACT)
    x = W / 2 - (tw1 + tw2 + tw3) / 2
    big(ctx, "ARJUN", x, 170, 210, GOLD, anchor="l")
    big(ctx, "YA", x + tw1, 170, 210, WHITE, anchor="l")
    big(ctx, "T-90", x + tw1 + tw2, 170, 210, CYAN, anchor="l")
    rrect(ctx, W / 2 - 520, 310, 1040, 120, 16)
    rgba(ctx, RED)
    ctx.fill()
    text(ctx, "ARMY NE KYUN NAHI APNAYA", W / 2, 370, 84, WHITE, font=IMPACT, stroke=(0.3, 0, 0), stroke_w=4)
