"""Reality Shift long-form (16:9, ~7 min): Siliguri Corridor / Chicken's Neck - the full story.

Built on the channel's best Short (India vs China: 22 KM Ka Chicken's Neck, 1,728 views by 19 Nov 2026).
9 chapters: hook, geography, what flows through it, how it formed, China/Doklam, Bangladesh's new turn,
India's defences, the second routes (Kaladan, Sikkim rail), the comment question.

    python make_long.py chickens_neck --kiki-export | --preview | (render)
"""

import math

import cairo

from core.engine import (circle, clamp, ease_in_out, ease_out_back, ease_out_cubic, glow, hexc, lerp, line, rgba,
                         rnd, rrect, text, text_width)
from core.longform import H, W
from shorts.chickens_neck import (BANGLADESH, BD_TIP, BHUTAN, CHINA, CORRIDOR, MYANMAR, NEPAL, NEPAL_TIP,
                                  NORTH_EAST, SEA, SIKKIM)

TITLE = "Siliguri Corridor: Bharat Ki 22 KM Ki Gardan"
MUSIC_STYLE = "tension"
MUSIC_BPM = 84
MUSIC_SEED = 2211
MUSIC_LO, MUSIC_HI = 0.06, 0.15
KIKI_TEMPO = 1.0          # the user sets 1.10x inside KikiVoice; raise here only if the voice still drags

# ------------------------------------------------------------ palette
NAVY = hexc("#050B14")
INDIA_LAND = hexc("#13261F")
FOREIGN_LAND = hexc("#0B1016")
WATER = hexc("#03101C")
EDGE = hexc("#7FD6B8")
GOLD = hexc("#FFC845")
RED = hexc("#FF4040")
TEAL = hexc("#46E0B0")
CYAN = hexc("#5CE1E6")
SAFFRON = hexc("#FF9933")
GREEN = hexc("#2FBF5B")
OLIVE = hexc("#4E5B31")
STEEL = hexc("#9AA8B8")
WHITE = (0.95, 0.96, 0.98)
MONO = "Consolas"
IMPACT = "Impact"

HOT = {"22": GOLD, "20": GOLD, "8": GOLD, "KAT": RED, "SILIGURI": GOLD, "CORRIDOR": GOLD, "CHICKEN'S": GOLD,
       "NECK": GOLD, "CHINA": RED, "NEPAL": TEAL, "BANGLADESH": TEAL, "BHUTAN": TEAL, "SIKKIM": TEAL,
       "DOKLAM": RED, "73": GOLD, "1947": GOLD, "1962": GOLD, "1971": GOLD, "1975": GOLD, "2017": GOLD,
       "2024": GOLD, "2025": GOLD, "2027": GOLD, "TRISHAKTI": SAFFRON, "RAFALE": CYAN, "S-400": CYAN,
       "KALADAN": GOLD, "SITTWE": GOLD, "MIZORAM": TEAL, "GARDAN": RED, "NAS": RED, "LALMONIRHAT": RED,
       "DHUBRI": SAFFRON, "KISHANGANJ": SAFFRON, "CHOPRA": SAFFRON, "COMMENT": GOLD, "JAI": SAFFRON,
       "HIND": GREEN, "4.5": GOLD, "CRORE": GOLD, "CHUMBI": RED, "ADHOORI": RED, "BHAI": GOLD}

# ------------------------------------------------------------ places (lon, lat)
SILIGURI = (88.43, 26.71)
SUKNA = (88.33, 26.79)
HASIMARA = (89.36, 26.72)
DOKLAM = (88.93, 27.29)
CHUMBI = (88.95, 27.55)
LALMONIRHAT = (89.45, 25.92)
DHUBRI = (89.98, 26.02)
KISHANGANJ = (87.95, 26.10)
CHOPRA = (88.31, 26.38)
KOLKATA = (88.36, 22.57)
SITTWE = (92.90, 20.15)
PALETWA = (92.85, 21.30)
ZORINPUI = (92.80, 22.62)
AIZAWL = (92.72, 23.73)
SEVOKE = (88.47, 26.89)
RANGPO = (88.53, 27.18)
GANGTOK = (88.61, 27.33)
DHAKA = (90.41, 23.81)
GUWAHATI = (91.74, 26.14)
NE_STATES = [("ASSAM", 92.9, 26.3), ("ARUNACHAL", 94.6, 28.0), ("NAGALAND", 94.3, 26.0), ("MANIPUR", 93.9, 24.75),
             ("MIZORAM", 92.8, 23.3), ("TRIPURA", 91.75, 23.75), ("MEGHALAYA", 91.3, 25.55), ("SIKKIM", 88.5, 27.55)]
LABELS = {"nepal": ("NEPAL", 86.4, 27.45), "bhutan": ("BHUTAN", 90.5, 27.45), "china": ("CHINA", 89.8, 29.4),
          "bangladesh": ("BANGLADESH", 90.2, 24.1), "myanmar": ("MYANMAR", 95.9, 22.6), "india": ("INDIA", 85.0, 24.6)}
FOREIGN = {"nepal": NEPAL, "bhutan": BHUTAN, "china": CHINA, "bangladesh": BANGLADESH, "myanmar": MYANMAR}

# camera views: (centre lon, centre lat, px per degree)
EAST = (90.2, 25.4, 88)
NE_V = (92.0, 25.6, 120)
REGION = (89.2, 26.4, 230)
NECK = (88.7, 26.75, 480)
NECK_CLOSE = (88.45, 26.62, 900)
CHUMBI_V = (88.85, 27.15, 430)
BD_V = (89.9, 25.1, 190)
KALADAN_V = (90.6, 22.6, 150)
SIKKIM_V = (88.55, 27.0, 560)
MAP_CY = 520


# ============================================================ map

def proj(v, lon, lat):
    lon0, lat0, s = v
    return W / 2 + (lon - lon0) * s * 0.9, MAP_CY - (lat - lat0) * s


def poly(ctx, v, pts):
    ctx.move_to(*proj(v, *pts[0]))
    for p in pts[1:]:
        ctx.line_to(*proj(v, *p))
    ctx.close_path()


def cam(v0, v1, u, T):
    u = ease_in_out(u)
    lon = lerp(v0[0], v1[0], u) + 0.02 * math.sin(T * 0.3) * 40 / v0[2]
    lat = lerp(v0[1], v1[1], u) + 0.02 * math.cos(T * 0.25) * 40 / v0[2]
    return lon, lat, math.exp(lerp(math.log(v0[2]), math.log(v1[2]), u))


def draw_region(ctx, v, tint, labels):
    rgba(ctx, INDIA_LAND)
    ctx.paint()
    poly(ctx, v, SEA)
    rgba(ctx, WATER)
    ctx.fill()
    for name, pts in FOREIGN.items():
        poly(ctx, v, pts)
        rgba(ctx, FOREIGN_LAND)
        ctx.fill()
        if name in tint:
            c, k = tint[name]
            poly(ctx, v, pts)
            rgba(ctx, c, 0.30 * k)
            ctx.fill()
    s = v[2]
    step = 0.5 if s > 400 else (1 if s > 150 else 2)
    for k in range(-40, 41):
        x = proj(v, round(v[0] / step) * step + k * step, v[1])[0]
        if 0 < x < W:
            line(ctx, [(x, 0), (x, H)], EDGE, 1, 0.06)
        y = proj(v, v[0], round(v[1] / step) * step + k * step)[1]
        if 0 < y < H:
            line(ctx, [(0, y), (W, y)], EDGE, 1, 0.06)
    for name, pts in FOREIGN.items():
        c, k = tint.get(name, (EDGE, 0))
        poly(ctx, v, pts)
        rgba(ctx, c, 0.18 + 0.25 * k)
        ctx.set_line_width(8)
        ctx.stroke_preserve()
        rgba(ctx, c, 0.5 + 0.5 * k)
        ctx.set_line_width(2.5)
        ctx.stroke()
    ctx.set_dash([8, 8])
    poly(ctx, v, SIKKIM)
    rgba(ctx, EDGE, 0.3)
    ctx.set_line_width(1.5)
    ctx.stroke()
    ctx.set_dash([])
    for name in labels:
        s_, lon, lat = LABELS[name]
        x, y = proj(v, lon, lat)
        c, k = tint.get(name, ((0.75, 0.85, 0.82), 0))
        if 60 < x < W - 60 and 90 < y < 900:
            text(ctx, s_, x, y, 30, c, font=MONO, a=0.5 + 0.5 * k)


def mark(ctx, v, lon, lat, label, c, a=1.0, T=0.0, side="r", size=26):
    x, y = proj(v, lon, lat)
    glow(ctx, x, y, 40, c, 0.45 * a)
    r = 9 + 3 * math.sin(T * 5)
    ctx.arc(x, y, r + 8, 0, 2 * math.pi)
    rgba(ctx, c, 0.5 * a)
    ctx.set_line_width(2)
    ctx.stroke()
    circle(ctx, x, y, 7, c, a)
    if label:
        tw = text_width(ctx, label, size, font=MONO)
        bx = x + 22 if side == "r" else x - 22 - tw - 20
        rrect(ctx, bx, y - size * 0.75, tw + 20, size * 1.5, 6)
        rgba(ctx, (0.02, 0.04, 0.07), 0.82 * a)
        ctx.fill()
        text(ctx, label, bx + 10, y, size, c, font=MONO, anchor="l", a=a)


def path_partial(ctx, v, pts, u):
    xy = [proj(v, *p) for p in pts]
    seg = [math.dist(a, b) for a, b in zip(xy, xy[1:])]
    total, goal = sum(seg) or 1, sum(seg) * clamp(u)
    out, acc = [xy[0]], 0
    for (a, b), s in zip(zip(xy, xy[1:]), seg):
        if acc + s >= goal:
            k = (goal - acc) / (s or 1)
            out.append((lerp(a[0], b[0], k), lerp(a[1], b[1], k)))
            return out
        out.append(b)
        acc += s
    return out


def ship_icon(ctx, x, y, s, c):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(-22, 0)
    ctx.line_to(22, 0)
    ctx.line_to(16, 9)
    ctx.line_to(-18, 9)
    ctx.close_path()
    rgba(ctx, c)
    ctx.fill()
    ctx.rectangle(-8, -10, 16, 10)
    ctx.fill()
    ctx.restore()


def map_shot(ctx, S, v0, v1=None, tint=None, corridor=None, labels=("nepal", "bhutan", "china", "bangladesh", "india"),
             marks=(), route=None, route_c=GOLD, route_dash=False, route_icon=None, caliper=False, ne=0, cut=False,
             chicken=False, dome=False, arrows=(), chumbi=False, pulse=False, ne_fill=False, rings=()):
    v = cam(v0, v1 or v0, S.u, S.T)
    k = ease_out_cubic(S.t / 0.8)
    tint = {n: (c, k) for n, c in (tint or {}).items()}
    draw_region(ctx, v, tint, labels)
    if ne_fill:
        poly(ctx, v, NORTH_EAST)
        rgba(ctx, TEAL, (0.12 + 0.06 * math.sin(S.T * 3)) * k)
        ctx.fill()
    if chumbi:
        x, y = proj(v, *CHUMBI)
        glow(ctx, x, y, 160 * v[2] / 430, RED, 0.45 * k)
        a0 = proj(v, 88.95, 27.85)
        a1 = proj(v, 88.9, 27.18)
        line(ctx, [a0, (lerp(a0[0], a1[0], k), lerp(a0[1], a1[1], k))], RED, 5, 0.9)
        mark(ctx, v, *CHUMBI, "CHUMBI VALLEY", RED, k, S.T, side="r")
    if corridor:
        poly(ctx, v, CORRIDOR)
        rgba(ctx, corridor, (0.24 + 0.14 * math.sin(S.T * (9 if pulse else 5))) * k)
        ctx.fill_preserve()
        rgba(ctx, corridor, 0.95 * k)
        ctx.set_line_width(4 if not pulse else 4 + 3 * abs(math.sin(S.T * 4)))
        ctx.stroke()
    if caliper:
        a, b = proj(v, *NEPAL_TIP), proj(v, *BD_TIP)
        a = (a[0] - 4, a[1] - 60)
        b = (b[0] + 4, b[1] + 40)
        g = ease_out_cubic((S.t - 0.4) / 1.0)
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        pa = (lerp(mid[0], a[0], g), lerp(mid[1], a[1], g))
        pb = (lerp(mid[0], b[0], g), lerp(mid[1], b[1], g))
        line(ctx, [pa, pb], GOLD, 4)
        for p in (pa, pb):
            circle(ctx, *p, 7, GOLD)
        if g > 0.6:
            mark(ctx, v, (NEPAL_TIP[0] + BD_TIP[0]) / 2 - 0.02, (NEPAL_TIP[1] + BD_TIP[1]) / 2, "20-22 KM", GOLD,
                 clamp((g - 0.6) / 0.4), S.T, side="l", size=40)
    for i in range(min(ne, len(NE_STATES))):
        name, lon, lat = NE_STATES[i]
        a = clamp((S.u * len(NE_STATES) * 1.15 - i) / 0.6) if ne == 99 else k
        if a > 0:
            mark(ctx, v, lon, lat, name, TEAL, a, S.T + i)
    for (lon, lat, r_km, c) in rings:
        x, y = proj(v, lon, lat)
        r = r_km / 111 * v[2] * ease_out_cubic(S.t / 1.2)
        ctx.arc(x, y, r, 0, 2 * math.pi)
        rgba(ctx, c, 0.08)
        ctx.fill_preserve()
        rgba(ctx, c, 0.6)
        ctx.set_line_width(2)
        ctx.stroke()
    if route:
        pts = path_partial(ctx, v, route, (S.t - 0.3) / max(1.0, S.d * 0.75))
        if len(pts) > 1:
            if route_dash:
                ctx.set_dash([18, 12])
            line(ctx, pts, route_c, 6, 0.95)
            ctx.set_dash([])
            if route_icon == "ship":
                ship_icon(ctx, *pts[-1], 1.2, WHITE)
            elif route_icon:
                circle(ctx, *pts[-1], 10, WHITE)
    for (p0, p1, c) in arrows:
        a, b = proj(v, *p0), proj(v, *p1)
        g = ease_out_cubic((S.t - 0.3) / 1.2)
        e = (lerp(a[0], b[0], g), lerp(a[1], b[1], g))
        line(ctx, [a, e], c, 7, 0.9)
        ang = math.atan2(e[1] - a[1], e[0] - a[0])
        ctx.move_to(e[0] + 22 * math.cos(ang), e[1] + 22 * math.sin(ang))
        ctx.line_to(e[0] + 18 * math.cos(ang + 2.4), e[1] + 18 * math.sin(ang + 2.4))
        ctx.line_to(e[0] + 18 * math.cos(ang - 2.4), e[1] + 18 * math.sin(ang - 2.4))
        rgba(ctx, c)
        ctx.fill()
    for m in marks:
        label, (lon, lat), c = m[0], m[1], m[2]
        appear = m[3] if len(m) > 3 else 0.0
        side = m[4] if len(m) > 4 else "r"
        a = clamp((S.u - appear) / 0.12)
        if a > 0:
            mark(ctx, v, lon, lat, label, c, a, S.T, side=side)
    if cut:
        g = clamp((S.u - 0.35) / 0.25)
        if g > 0:
            a, b = proj(v, 88.05, 27.05), proj(v, 88.75, 26.2)
            e = (lerp(a[0], b[0], g), lerp(a[1], b[1], g))
            line(ctx, [a, e], RED, 12, 0.95)
            ctx.save()
            ctx.translate(30 * g, 0)
            poly(ctx, v, NORTH_EAST)
            rgba(ctx, RED, 0.18 * g)
            ctx.fill_preserve()
            rgba(ctx, RED, 0.8 * g)
            ctx.set_line_width(3)
            ctx.stroke()
            ctx.restore()
    if chicken:
        chicken_icon(ctx, *proj(v, *SILIGURI), clamp(S.t / 0.6), S.T)
    if dome:
        x, y = proj(v, *SILIGURI)
        shield_dome(ctx, x, y + 30, 260 * ease_out_back(clamp(S.t / 1.2)), S.T)
    vignette(ctx)


def chicken_icon(ctx, x, y, a, T):
    """A small chicken-head badge floating above the corridor, pointing down at it."""
    if a <= 0:
        return
    bx, by = x - 260, y - 250 + 6 * math.sin(T * 2)
    line(ctx, [(bx + 70, by + 70), (x - 10, y - 10)], GOLD, 3, 0.7 * a)
    circle(ctx, bx, by, 72, (0.02, 0.04, 0.07), 0.85 * a)
    ctx.arc(bx, by, 72, 0, 2 * math.pi)
    rgba(ctx, GOLD, a)
    ctx.set_line_width(3)
    ctx.stroke()
    circle(ctx, bx, by + 6, 30, WHITE, a)              # head
    ctx.move_to(bx + 26, by + 2)                       # beak
    ctx.line_to(bx + 50, by + 10)
    ctx.line_to(bx + 26, by + 16)
    rgba(ctx, GOLD, a)
    ctx.fill()
    for i in range(3):                                 # comb
        circle(ctx, bx - 12 + i * 12, by - 26 + (4 if i == 1 else 0), 9, RED, a)
    circle(ctx, bx + 10, by, 4, (0, 0, 0), a)
    ctx.rectangle(bx - 12, by + 30, 24, 40)            # long thin neck, lit red
    rgba(ctx, RED, a * (0.7 + 0.3 * math.sin(T * 6)))
    ctx.fill()


def shield_dome(ctx, x, y, r, T):
    if r <= 2:
        return
    ctx.save()
    ctx.arc(x, y, r, math.pi, 2 * math.pi)
    ctx.close_path()
    g = cairo.RadialGradient(x, y, r * 0.2, x, y, r)
    g.add_color_stop_rgba(0, CYAN[0], CYAN[1], CYAN[2], 0.05)
    g.add_color_stop_rgba(1, CYAN[0], CYAN[1], CYAN[2], 0.28)
    ctx.set_source(g)
    ctx.fill_preserve()
    ctx.clip()
    for i in range(-12, 13):
        for j in range(0, 10):
            hx = x + i * 46 + (23 if j % 2 else 0)
            hy = y - j * 40
            ctx.new_sub_path()
            for q in range(6):
                ang = math.pi / 3 * q + math.pi / 6
                ctx.line_to(hx + 22 * math.cos(ang), hy + 22 * math.sin(ang))
            ctx.close_path()
    rgba(ctx, CYAN, 0.18 + 0.08 * math.sin(T * 3))
    ctx.set_line_width(1.5)
    ctx.stroke()
    ctx.restore()
    ctx.arc(x, y, r, math.pi, 2 * math.pi)
    rgba(ctx, CYAN, 0.9)
    ctx.set_line_width(4)
    ctx.stroke()


def vignette(ctx):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, W * 0.62)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.62)
    ctx.set_source(g)
    ctx.paint()


# ============================================================ scenery helpers

def sky(ctx, top, mid, bottom, moon=None):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *top)
    g.add_color_stop_rgb(0.55, *mid)
    g.add_color_stop_rgb(1, *bottom)
    ctx.set_source(g)
    ctx.paint()
    for i in range(70):
        circle(ctx, rnd(i, 1) * W, rnd(i, 2) * H * 0.5, 1 + 1.5 * rnd(i, 3), WHITE, 0.15 + 0.3 * rnd(i, 4))
    if moon:
        glow(ctx, moon[0], moon[1], 220, (1, 0.95, 0.85), 0.25)
        circle(ctx, moon[0], moon[1], 46, (0.98, 0.95, 0.88), 0.95)


def ridge(ctx, base, amp, seed, c, T=0.0, speed=0.0, snow=False):
    off = T * speed
    pts = []
    for i in range(-2, 40):
        x = i * 60 - (off % 60)
        k = i + int(off // 60)
        y = base - amp * (0.5 + 0.5 * math.sin(k * 0.55 + seed)) * (0.6 + 0.4 * rnd(k, seed))
        pts.append((x, y))
    ctx.move_to(pts[0][0], H)
    for p in pts:
        ctx.line_to(*p)
    ctx.line_to(pts[-1][0], H)
    ctx.close_path()
    rgba(ctx, c)
    ctx.fill()
    if snow:
        for (x, y) in pts:
            if y < base - amp * 0.75:
                ctx.move_to(x - 18, y + 16)
                ctx.line_to(x, y)
                ctx.line_to(x + 18, y + 16)
                ctx.close_path()
                rgba(ctx, WHITE, 0.6)
                ctx.fill()


def hills_night(ctx, T, speed=0.0):
    sky(ctx, hexc("#040812"), hexc("#0E1A2E"), hexc("#1B2A3A"), moon=(1550, 190))
    ridge(ctx, 560, 260, 1.0, hexc("#18263A"), T, speed * 0.2, snow=True)
    ridge(ctx, 680, 170, 2.3, hexc("#122033"), T, speed * 0.45)
    ridge(ctx, 790, 110, 3.7, hexc("#0B1624"), T, speed * 0.75)


def soldier(ctx, x, y, s, c=OLIVE, flip=False, rifle=True, a=1.0, sway=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(-s if flip else s, s)
    ctx.rotate(sway)
    rgba(ctx, shade(c, 0.7), a)
    ctx.rectangle(-14, -70, 11, 70)                # legs
    ctx.rectangle(3, -70, 11, 70)
    ctx.fill()
    rgba(ctx, c, a)
    rrect(ctx, -20, -150, 40, 85, 10)               # torso
    ctx.fill()
    rgba(ctx, hexc("#C79B73"), a)
    circle(ctx, 0, -172, 17, hexc("#C79B73"), a)    # face
    rgba(ctx, shade(c, 0.85), a)
    ctx.arc(0, -178, 21, math.pi, 2 * math.pi)       # helmet
    ctx.fill()
    if rifle:
        line(ctx, [(-22, -80), (30, -150)], (0.12, 0.12, 0.12), 6, a)
    ctx.restore()


def shade(c, k):
    return tuple(min(1, x * k) for x in c)


def truck(ctx, x, y, s, body, cab=None, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rgba(ctx, body, a)
    rrect(ctx, -110, -80, 150, 64, 6)
    ctx.fill()
    rgba(ctx, cab or shade(body, 1.2), a)
    rrect(ctx, 44, -66, 56, 50, 8)
    ctx.fill()
    rgba(ctx, (0.6, 0.85, 1.0), 0.7 * a)
    ctx.rectangle(70, -58, 22, 18)
    ctx.fill()
    for wx in (-80, -30, 70):
        circle(ctx, wx, -12, 15, (0.05, 0.05, 0.06), a)
        circle(ctx, wx, -12, 6, STEEL, a)
    glow(ctx, 104, -30, 60, (1, 0.9, 0.6), 0.35 * a)
    ctx.restore()


def train(ctx, x, y, s, cars=6, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for i in range(cars):
        cx = -i * 190
        rgba(ctx, hexc("#2E5C8A") if i else hexc("#C0392B"), a)
        rrect(ctx, cx - 180, -90, 180, 76, 10)
        ctx.fill()
        for wnd in range(4):
            rgba(ctx, (1, 0.92, 0.6), 0.75 * a)
            ctx.rectangle(cx - 165 + wnd * 42, -76, 26, 22)
            ctx.fill()
        for wx in (cx - 150, cx - 30):
            circle(ctx, wx, -12, 12, (0.05, 0.05, 0.06), a)
    glow(ctx, 0, -50, 90, (1, 0.95, 0.7), 0.5 * a)
    ctx.restore()


def big_number(ctx, s, x, y, size, c, a=1.0, sub=None):
    text(ctx, s, x, y, size, c, font=IMPACT, a=a, stroke=(0, 0, 0), stroke_w=8)
    if sub:
        text(ctx, sub, x, y + size * 0.72, size * 0.3, WHITE, font=MONO, a=a)


# ============================================================ illustrated shots

def convoy(ctx, S, items=("truck", "train", "pipe"), blocked=False, army=False):
    """Side-on lifeline: highway trucks, a train above, the oil pipeline glowing under the ground."""
    stop = clamp((S.u - 0.45) / 0.2) if blocked else 0
    hills_night(ctx, S.T, speed=0 if blocked else 30)
    rgba(ctx, hexc("#0A121C"))
    ctx.rectangle(0, 790, W, H - 790)
    ctx.fill()
    if "train" in items:
        line(ctx, [(0, 735), (W, 735)], STEEL, 4, 0.8)
        for i in range(48):
            line(ctx, [(i * 40 - (S.T * 60 % 40), 738), (i * 40 - (S.T * 60 % 40), 746)], STEEL, 3, 0.4)
        tx = -200 + (S.T * 260 % (W + 1400)) if not blocked else lerp(-200 + S.t * 260, 700, stop)
        train(ctx, tx, 735, 0.75)
    rgba(ctx, hexc("#202A35"))
    ctx.rectangle(0, 800, W, 70)
    ctx.fill()
    for i in range(30):
        x = i * 90 - (0 if blocked and stop >= 1 else S.T * 200 % 90)
        line(ctx, [(x, 835), (x + 45, 835)], GOLD, 4, 0.6)
    if "truck" in items:
        for i in range(4):
            base = (i * 520 + S.t * 220) % (W + 600) - 300
            x = base if not blocked else min(base, 1150 - i * 260 + (1 - stop) * 900)
            truck(ctx, x, 862, 0.9, OLIVE if army else [hexc("#C0703A"), hexc("#3A7DC0"), hexc("#7A4AB0"), hexc("#C0A23A")][i])
    if "pipe" in items:
        rgba(ctx, hexc("#2A1E12"))
        ctx.rectangle(0, 930, W, 40)
        ctx.fill()
        rrect(ctx, -10, 938, W + 20, 24, 12)
        rgba(ctx, hexc("#56606B"))
        ctx.fill()
        for i in range(26):
            x = (i * 80 + S.T * (0 if blocked and stop >= 1 else 160)) % (W + 80) - 40
            circle(ctx, x, 950, 6, hexc("#FFB347"), 0.85)
    if blocked and stop > 0:
        bx = 1350
        for i in range(2):
            rgba(ctx, RED if i == 0 else WHITE, stop)
            ctx.rectangle(bx - 10, 640 + i * 0, 20, 260)
        rgba(ctx, RED, stop)
        ctx.rectangle(bx - 10, 620, 20, 300)
        ctx.fill()
        for j in range(5):
            rgba(ctx, RED if j % 2 == 0 else WHITE, stop)
            ctx.rectangle(bx - 200 + j * 80, 780, 80, 22)
            ctx.fill()
        line(ctx, [(bx + 120, 560), (bx + 300, 740)], RED, 18, stop)
        line(ctx, [(bx + 300, 560), (bx + 120, 740)], RED, 18, stop)
    vignette(ctx)


def walker(ctx, S):
    """A person walks a 22 km ruler while a clock runs 0 -> 5 hours."""
    sky(ctx, hexc("#08101E"), hexc("#14243A"), hexc("#1E3248"))
    ridge(ctx, 700, 140, 4.1, hexc("#0F1C2C"))
    rgba(ctx, hexc("#0B1622"))
    ctx.rectangle(0, 760, W, H)
    ctx.fill()
    x0, x1, y = 260, 1660, 780
    line(ctx, [(x0, y), (x1, y)], GOLD, 5)
    for i in range(23):
        x = lerp(x0, x1, i / 22)
        line(ctx, [(x, y - (22 if i % 5 == 0 else 12)), (x, y)], GOLD, 3)
        if i % 5 == 0 or i == 22:
            text(ctx, f"{i} KM", x, y + 34, 24, GOLD, font=MONO)
    u = ease_in_out(S.u * 1.05)
    px = lerp(x0, x1, u)
    ph = S.T * 7
    ctx.save()
    ctx.translate(px, y - 4)
    rgba(ctx, WHITE)
    for sgn in (1, -1):
        line(ctx, [(0, -70), (sgn * 22 * math.sin(ph), 0)], WHITE, 9)
        line(ctx, [(0, -130), (-sgn * 20 * math.sin(ph), -85)], WHITE, 8)
    line(ctx, [(0, -140), (0, -70)], WHITE, 12)
    circle(ctx, 0, -162, 18, WHITE)
    ctx.restore()
    hrs = 5 * u
    cx, cy = 1600, 300
    circle(ctx, cx, cy, 110, (0.03, 0.05, 0.09), 0.9)
    ctx.arc(cx, cy, 110, 0, 2 * math.pi)
    rgba(ctx, GOLD)
    ctx.set_line_width(4)
    ctx.stroke()
    ctx.arc(cx, cy, 96, -math.pi / 2, -math.pi / 2 + 2 * math.pi * hrs / 5)
    rgba(ctx, CYAN, 0.9)
    ctx.set_line_width(10)
    ctx.stroke()
    text(ctx, f"{hrs:0.1f} H", cx, cy, 52, WHITE, font=IMPACT)
    vignette(ctx)


def timeline_shot(ctx, S, focus=0):
    years = [("1947", "BATWARA"), ("1962", "CHINA YUDH"), ("1971", "BANGLADESH"), ("1975", "SIKKIM"),
             ("2017", "DOKLAM"), ("2025", "NAYE THIKANE")]
    sky(ctx, hexc("#060A12"), hexc("#0B1320"), hexc("#101A28"))
    gap = 420
    cxf = lerp(focus - 0.6, focus, ease_out_cubic(S.t / 1.2))
    y = 520
    line(ctx, [(0, y), (W, y)], STEEL, 3, 0.5)
    for i, (yr, lab) in enumerate(years):
        x = W / 2 + (i - cxf) * gap
        on = i == focus
        a = 1.0 if on else 0.35
        if on:
            glow(ctx, x, y, 200, GOLD, 0.35)
        circle(ctx, x, y, 22 if on else 12, GOLD if on else STEEL, a)
        text(ctx, yr, x, y - 90, 110 if on else 60, GOLD if on else WHITE, font=IMPACT, a=a)
        text(ctx, lab, x, y + 70, 34 if on else 24, WHITE, font=MONO, a=a)
    vignette(ctx)


def standoff(ctx, S, days=False, stop=False, villages=False):
    """Doklam plateau: a road pushes in from the left with a bulldozer, Indian soldiers stand across its path."""
    sky(ctx, hexc("#0A1424"), hexc("#2A3A55"), hexc("#55667A"))
    ridge(ctx, 520, 200, 5.5, hexc("#3A4A60"), snow=True)
    ridge(ctx, 650, 120, 6.2, hexc("#2B3A2E"))
    rgba(ctx, hexc("#2E3B26"))
    ctx.rectangle(0, 720, W, H)
    ctx.fill()
    reach = 700 * (1.0 if stop else ease_out_cubic(S.t / max(1.0, S.d * 0.6)))
    rgba(ctx, hexc("#6B6F73"))
    ctx.move_to(0, 780)
    ctx.line_to(reach + 160, 800)
    ctx.line_to(reach + 160, 860)
    ctx.line_to(0, 900)
    ctx.close_path()
    ctx.fill()
    bx = reach + 160
    rgba(ctx, hexc("#E0A21E"))                          # bulldozer
    rrect(ctx, bx - 150, 720, 130, 70, 6)
    ctx.fill()
    rrect(ctx, bx - 120, 680, 60, 48, 6)
    ctx.fill()
    line(ctx, [(bx - 20, 760), (bx + 10, 800)], hexc("#B8860B"), 10)
    rgba(ctx, (0.08, 0.08, 0.08))
    rrect(ctx, bx - 160, 785, 150, 30, 14)
    ctx.fill()
    for i in range(3):                                  # their soldiers by the road, grey
        soldier(ctx, bx - 260 - i * 80, 850, 0.8, hexc("#5E6670"), sway=0.01 * math.sin(S.T + i))
    for i in range(5):                                  # Indian soldiers in a line, facing left
        soldier(ctx, bx + 170 + i * 95, 860, 0.85, OLIVE, flip=True,
                sway=0.015 * math.sin(S.T * 1.3 + i))
    if stop:
        g = clamp((S.u - 0.3) / 0.2)
        rgba(ctx, RED, g)
        ctx.rectangle(bx + 60, 760, 26, 120)
        ctx.fill()
        for j in range(4):
            rgba(ctx, RED if j % 2 == 0 else WHITE, g)
            ctx.rectangle(bx + 10 + j * 40, 760, 40, 20)
            ctx.fill()
    if days:
        n = 1 + int(72 * ease_in_out(S.u * 1.1))
        rrect(ctx, 1500, 110, 340, 170, 14)
        rgba(ctx, (0.02, 0.03, 0.06), 0.82)
        ctx.fill()
        text(ctx, "DAY", 1670, 150, 30, STEEL, font=MONO)
        text(ctx, f"{n}", 1670, 222, 96, GOLD, font=IMPACT)
    vignette(ctx)


def villages(ctx, S):
    """Satellite-style view: new houses and road lines appear on a ridge."""
    rgba(ctx, hexc("#1E2A1E"))
    ctx.paint()
    for i in range(220):
        x, y = rnd(i, 7) * W, rnd(i, 8) * H
        circle(ctx, x, y, 30 + 60 * rnd(i, 9), hexc("#243324"), 0.6)
    pts = [(0, 700), (300, 640), (650, 600), (900, 520), (1250, 470), (1600, 400), (1920, 360)]
    line(ctx, pts, hexc("#8C8C80"), 10, 0.9)
    g = S.u * 1.2
    for i in range(18):
        a = clamp((g * 18 - i) / 1.5)
        if a <= 0:
            continue
        px = 820 + (i % 6) * 90 + (i // 6) * 30
        py = 360 + (i // 6) * 90
        rgba(ctx, hexc("#D0D3D6"), a)
        ctx.rectangle(px, py, 54, 38)
        ctx.fill()
        rgba(ctx, RED, 0.8 * a)
        ctx.rectangle(px, py, 54, 10)
        ctx.fill()
    for k in range(5):
        y = 260 + k * 160
        line(ctx, [(0, y), (W, y + 30)], hexc("#7FD6B8"), 1, 0.12)
    rrect(ctx, 60, 90, 420, 60, 8)
    rgba(ctx, (0.02, 0.03, 0.06), 0.8)
    ctx.fill()
    text(ctx, "SATELLITE VIEW // REPORTS", 80, 120, 24, CYAN, font=MONO, anchor="l")
    glow(ctx, 1050, 470, 380, RED, 0.12 + 0.05 * math.sin(S.T * 3))
    vignette(ctx)


def radar(ctx, S, blips=((0.3, -0.4, RED), (0.55, 0.2, RED), (-0.4, 0.5, CYAN)), label="AIR DEFENCE"):
    rgba(ctx, hexc("#020806"))
    ctx.paint()
    cx, cy, R = W / 2, 520, 400
    for k in range(1, 5):
        ctx.arc(cx, cy, R * k / 4, 0, 2 * math.pi)
        rgba(ctx, GREEN, 0.25)
        ctx.set_line_width(2)
        ctx.stroke()
    line(ctx, [(cx - R, cy), (cx + R, cy)], GREEN, 1, 0.25)
    line(ctx, [(cx, cy - R), (cx, cy + R)], GREEN, 1, 0.25)
    ang = S.T * 1.8
    for j in range(30):
        a = ang - j * 0.03
        ctx.move_to(cx, cy)
        ctx.arc(cx, cy, R, a - 0.03, a)
        ctx.close_path()
        rgba(ctx, GREEN, 0.22 * (1 - j / 30))
        ctx.fill()
    for (bx, by, c) in blips:
        x, y = cx + bx * R, cy + by * R
        da = (ang - math.atan2(by, bx)) % (2 * math.pi)
        a = max(0.2, 1 - da / 3)
        glow(ctx, x, y, 40, c, 0.6 * a)
        circle(ctx, x, y, 8, c, a)
    text(ctx, label, cx, cy + R + 50, 30, GREEN, font=MONO)
    vignette(ctx)


def rafale(ctx, x, y, s, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(120, 0)
    ctx.line_to(40, -12)
    ctx.line_to(-30, -80)
    ctx.line_to(-60, -80)
    ctx.line_to(-40, -14)
    ctx.line_to(-110, -10)
    ctx.line_to(-130, -40)
    ctx.line_to(-145, -40)
    ctx.line_to(-135, 0)
    ctx.line_to(-145, 40)
    ctx.line_to(-130, 40)
    ctx.line_to(-110, 10)
    ctx.line_to(-40, 14)
    ctx.line_to(-60, 80)
    ctx.line_to(-30, 80)
    ctx.line_to(40, 12)
    ctx.close_path()
    rgba(ctx, hexc("#8E9AA6"), a)
    ctx.fill()
    ctx.move_to(70, -6)
    ctx.line_to(30, -6)
    ctx.line_to(30, 6)
    ctx.line_to(70, 6)
    rgba(ctx, hexc("#2A3A4A"), a)
    ctx.fill()
    glow(ctx, -150, 0, 50, (1, 0.6, 0.2), 0.7 * a)
    ctx.restore()


def jets(ctx, S):
    hills_night(ctx, S.T, speed=80)
    for i in range(3):
        x = -300 + (S.t * 420 + i * 260) % (W + 600)
        y = 300 + i * 90 + 10 * math.sin(S.T * 2 + i)
        rafale(ctx, x, y, 0.9 - i * 0.12)
    rgba(ctx, hexc("#0A121C"))
    ctx.rectangle(0, 900, W, H)
    ctx.fill()
    for i in range(24):
        x = i * 90 - (S.T * 300 % 90)
        line(ctx, [(x, 930), (x + 50, 930)], WHITE, 4, 0.5)
    vignette(ctx)


def crowd(ctx, S):
    sky(ctx, hexc("#07101C"), hexc("#10233A"), hexc("#1A3048"))
    g = ease_out_cubic(S.t / max(1.0, S.d * 0.6))
    n = int(160 * g)
    for i in range(n):
        x = 80 + (i % 32) * 56 + 18 * rnd(i, 1)
        row = i // 32
        y = 600 + row * 70
        c = [TEAL, GOLD, SAFFRON, CYAN, WHITE][i % 5]
        circle(ctx, x, y - 34, 11, c, 0.75)
        rrect(ctx, x - 12, y - 22, 24, 34, 8)
        rgba(ctx, c, 0.55)
        ctx.fill()
    big_number(ctx, f"{4.5 * g:0.1f} CRORE+", W / 2, 300, 150, GOLD, sub="LOG  //  8 RAAJYA  (CENSUS 2011)")
    vignette(ctx)


def badge(ctx, S, title="33 CORPS", sub="TRISHAKTI CORPS  //  SUKNA"):
    sky(ctx, hexc("#0B0F14"), hexc("#151C24"), hexc("#1D252E"))
    g = ease_out_back(clamp(S.t / 0.9))
    cx, cy, R = W / 2, 470, 230 * g
    if R > 2:
        glow(ctx, cx, cy, R * 2, SAFFRON, 0.25)
        ctx.arc(cx, cy, R, 0, 2 * math.pi)
        rgba(ctx, hexc("#1A2230"))
        ctx.fill_preserve()
        rgba(ctx, GOLD)
        ctx.set_line_width(8)
        ctx.stroke()
        ctx.save()                                    # trident
        ctx.translate(cx, cy)
        ctx.scale(g, g)
        line(ctx, [(0, 150), (0, -130)], GOLD, 14)
        line(ctx, [(-80, -40), (-80, -100)], GOLD, 12)
        line(ctx, [(80, -40), (80, -100)], GOLD, 12)
        ctx.move_to(-80, -40)
        ctx.curve_to(-80, 20, 80, 20, 80, -40)
        rgba(ctx, GOLD)
        ctx.set_line_width(12)
        ctx.stroke()
        for x in (-80, 0, 80):
            ctx.move_to(x - 18, -100 if x else -130)
            ctx.line_to(x, -140 if x else -170)
            ctx.line_to(x + 18, -100 if x else -130)
            ctx.close_path()
            ctx.fill()
        ctx.restore()
    a = clamp((S.t - 0.6) / 0.4)
    text(ctx, title, cx, 790, 80, WHITE, font=IMPACT, a=a)
    text(ctx, sub, cx, 860, 32, SAFFRON, font=MONO, a=a)
    vignette(ctx)


def tunnel_rail(ctx, S):
    sky(ctx, hexc("#0A1626"), hexc("#25405A"), hexc("#3E5D72"))
    ridge(ctx, 520, 240, 7.7, hexc("#22394A"), snow=True)
    ctx.move_to(1050, H)                                # mountain with the tunnel mouth
    ctx.curve_to(1150, 300, 1650, 260, 1920, 420)
    ctx.line_to(1920, H)
    ctx.close_path()
    rgba(ctx, hexc("#1A2C24"))
    ctx.fill()
    ctx.arc(1240, 760, 90, math.pi, 2 * math.pi)
    ctx.line_to(1330, 760)
    ctx.close_path()
    rgba(ctx, (0.01, 0.01, 0.01))
    ctx.fill()
    ctx.arc(1240, 760, 90, math.pi, 2 * math.pi)
    rgba(ctx, STEEL)
    ctx.set_line_width(10)
    ctx.stroke()
    rgba(ctx, hexc("#3A2E22"))                         # bridge deck + piers over a river
    ctx.rectangle(0, 760, 1240, 18)
    ctx.fill()
    for px in range(80, 1200, 220):
        ctx.rectangle(px, 778, 22, 200)
        ctx.fill()
    rgba(ctx, hexc("#163A5A"))
    ctx.rectangle(0, 960, 1240, H)
    ctx.fill()
    tx = lerp(-400, 1300, ease_in_out(S.u))
    ctx.save()
    ctx.rectangle(0, 0, 1240, H)
    ctx.clip()
    train(ctx, tx, 760, 0.7)
    ctx.restore()
    rrect(ctx, 70, 90, 560, 110, 10)
    rgba(ctx, (0.02, 0.03, 0.06), 0.8)
    ctx.fill()
    text(ctx, "SEVOKE -> RANGPO  //  SIKKIM", 95, 125, 28, GOLD, font=MONO, anchor="l")
    text(ctx, "TARGET: DEC 2027", 95, 170, 28, WHITE, font=MONO, anchor="l")
    vignette(ctx)


def question(ctx, S):
    """Comment question: corridor map dimmed behind two option cards, an arrow pointing to the comments."""
    map_shot(ctx, S, NECK, NECK, corridor=GOLD, labels=("nepal", "bhutan", "bangladesh", "china"))
    rgba(ctx, (0, 0, 0), 0.45)
    ctx.paint()
    opts = [("A", "DOOSRA RAASTA TEZ KARO", TEAL), ("B", "GARDAN AUR MAZBOOT KARO", SAFFRON)]
    for i, (k, s, c) in enumerate(opts):
        g = ease_out_back(clamp((S.t - 0.3 - i * 0.35) / 0.6))
        if g <= 0:
            continue
        x = W / 2 - 430 + i * 860
        ctx.save()
        ctx.translate(x, 470)
        ctx.scale(g, g)
        rrect(ctx, -380, -110, 760, 220, 22)
        rgba(ctx, (0.03, 0.05, 0.09), 0.92)
        ctx.fill_preserve()
        rgba(ctx, c)
        ctx.set_line_width(5)
        ctx.stroke()
        circle(ctx, -290, 0, 56, c)
        text(ctx, k, -290, 0, 64, (0.02, 0.03, 0.05), font=IMPACT)
        text(ctx, s, 40, 0, 44, WHITE, font=IMPACT)
        ctx.restore()
    a = clamp((S.t - 1.2) / 0.4)
    yb = 760 + 14 * math.sin(S.T * 6)
    text(ctx, "COMMENT MEIN LIKHO", W / 2, 700, 46, GOLD, font=IMPACT, a=a)
    ctx.move_to(W / 2 - 34, yb)
    ctx.line_to(W / 2 + 34, yb)
    ctx.line_to(W / 2, yb + 50)
    ctx.close_path()
    rgba(ctx, GOLD, a)
    ctx.fill()


def finale(ctx, S):
    map_shot(ctx, S, NE_V, EAST, corridor=GOLD, ne_fill=True)
    a = clamp((S.t - 0.4) / 0.6)
    text(ctx, "JAI HIND", W / 2, 260, 150, SAFFRON, font=IMPACT, a=a, stroke=(0, 0, 0), stroke_w=8)


# ============================================================ script
# each line: (spoken Hindi for KikiVoice, Roman caption, shot, params)
M = map_shot
ALL = ("nepal", "bhutan", "china", "bangladesh", "india")

CHAPTERS = [
    {"key": "hook", "title": "22 KM KI GARDAN", "lines": [
        ("सोचो एक सुबह भारत के आठ राज्य अचानक बाकी देश से कट जाएं।",
         "SOCHO EK SUBAH BHARAT KE 8 RAAJYA ACHANAK BAAKI DESH SE KAT JAAYEIN", M,
         dict(v0=EAST, v1=REGION, corridor=RED, ne_fill=True, cut=True)),
        ("ना कोई ट्रेन जाए ना कोई ट्रक और ना ही फौज का सामान।",
         "NA KOI TRAIN JAAYE NA KOI TRUCK AUR NA HI FAUJ KA SAAMAN", convoy, dict(blocked=True)),
        ("ये किसी फिल्म की कहानी नहीं है भाई।",
         "YEH KISI FILM KI KAHANI NAHI HAI BHAI", M, dict(v0=EAST, v1=NECK, corridor=GOLD)),
        ("ये खतरा जुड़ा है ज़मीन की एक ऐसी पतली पट्टी से जो सिर्फ बीस से बाईस किलोमीटर चौड़ी है।",
         "YEH KHATRA JUDA HAI ZAMEEN KI EK AISI PATLI PATTI SE JO SIRF 20 SE 22 KILOMETER CHAUDI HAI", M,
         dict(v0=NECK, v1=NECK_CLOSE, corridor=GOLD, caliper=True)),
        ("इतनी दूरी तो एक आदमी पैदल चार पांच घंटे में पार कर ले।",
         "ITNI DOORI TOH EK AADMI PAIDAL 4-5 GHANTE MEIN PAAR KAR LE", walker, {}),
        ("इसका नाम है सिलीगुड़ी कॉरिडोर।",
         "ISKA NAAM HAI SILIGURI CORRIDOR", M,
         dict(v0=NECK_CLOSE, v1=NECK, corridor=GOLD, marks=[("SILIGURI", SILIGURI, GOLD, 0.1)])),
        ("और दुनिया इसे कहती है चिकन्स नेक।",
         "AUR DUNIYA ISE KEHTI HAI CHICKEN'S NECK", M, dict(v0=NECK, corridor=RED, chicken=True, pulse=True)),
        ("आज इस वीडियो में जानेंगे कि ये गर्दन बनी कैसे।",
         "AAJ IS VIDEO MEIN JAANENGE KI YEH GARDAN BANI KAISE", timeline_shot, dict(focus=0)),
        ("चीन की नज़र इस पर क्यों टिकी है।",
         "CHINA KI NAZAR IS PAR KYUN TIKI HAI", M,
         dict(v0=REGION, v1=CHUMBI_V, corridor=GOLD, tint={"china": RED}, chumbi=True)),
        ("भारत ने इसे बचाने के लिए क्या क्या तैयारी की है।",
         "BHARAT NE ISE BACHANE KE LIYE KYA KYA TAIYAARI KI HAI", M, dict(v0=NECK, corridor=GOLD, dome=True)),
        ("और आखिर में वो दूसरा रास्ता भी जिसके बारे में बहुत कम लोग जानते हैं।",
         "AUR AAKHIR MEIN WOH DOOSRA RAASTA BHI JISKE BAARE MEIN BAHUT KAM LOG JAANTE HAIN", M,
         dict(v0=KALADAN_V, route=[KOLKATA, (88.2, 21.3), (90.0, 20.6), (91.8, 20.0), SITTWE, PALETWA, ZORINPUI, AIZAWL],
              route_dash=True, route_icon="ship", labels=("bangladesh", "myanmar", "india"))),
    ]},
    {"key": "map", "title": "KYA HAI YEH GARDAN", "lines": [
        ("पहले नक्शे को ध्यान से देखो।", "PEHLE NAKSHE KO DHYAAN SE DEKHO", M, dict(v0=EAST, v1=REGION)),
        ("बाईं तरफ है नेपाल।", "BAAYIN TARAF HAI NEPAL", M, dict(v0=REGION, tint={"nepal": TEAL}, corridor=GOLD)),
        ("नीचे की तरफ है बांग्लादेश।", "NEECHE KI TARAF HAI BANGLADESH", M,
         dict(v0=REGION, tint={"bangladesh": TEAL}, corridor=GOLD)),
        ("ऊपर है भूटान।", "UPAR HAI BHUTAN", M, dict(v0=REGION, tint={"bhutan": TEAL}, corridor=GOLD)),
        ("और सिक्किम और भूटान के बीच से नीचे झांकती है चीन की चुंबी घाटी।",
         "AUR SIKKIM AUR BHUTAN KE BEECH SE NEECHE JHAANKTI HAI CHINA KI CHUMBI GHAATI", M,
         dict(v0=REGION, v1=CHUMBI_V, tint={"china": RED}, chumbi=True, corridor=GOLD)),
        ("इन सबके बीच में फंसी है भारत की ये पतली सी पट्टी।",
         "IN SABKE BEECH MEIN PHANSI HAI BHARAT KI YEH PATLI SI PATTI", M,
         dict(v0=CHUMBI_V, v1=NECK, corridor=RED, pulse=True,
              tint={"nepal": TEAL, "bangladesh": TEAL, "bhutan": TEAL, "china": RED})),
        ("एक तरफ बाकी पूरा भारत है।", "EK TARAF BAAKI POORA BHARAT HAI", M,
         dict(v0=REGION, v1=(86.0, 25.5, 160), corridor=GOLD)),
        ("और दूसरी तरफ आठ राज्य हैं।", "AUR DOOSRI TARAF 8 RAAJYA HAIN", M,
         dict(v0=REGION, v1=NE_V, corridor=GOLD, ne_fill=True)),
        ("असम अरुणाचल नागालैंड और मणिपुर।", "ASSAM ARUNACHAL NAGALAND AUR MANIPUR", M,
         dict(v0=NE_V, ne_fill=True, ne=99)),
        ("मिज़ोरम त्रिपुरा मेघालय और सिक्किम।", "MIZORAM TRIPURA MEGHALAYA AUR SIKKIM", M,
         dict(v0=NE_V, v1=EAST, ne_fill=True, ne=8, corridor=GOLD)),
        ("इन राज्यों में साढ़े चार करोड़ से ज़्यादा लोग रहते हैं।",
         "IN RAAJYON MEIN 4.5 CRORE SE ZYADA LOG REHTE HAIN", crowd, {}),
        ("और इन सबका बाकी भारत से ज़मीन वाला रिश्ता इसी पट्टी से होकर गुज़रता है।",
         "AUR IN SABKA BAAKI BHARAT SE ZAMEEN WALA RISHTA ISI PATTI SE HOKAR GUZARTA HAI", M,
         dict(v0=EAST, v1=NECK, corridor=GOLD, ne_fill=True,
              arrows=[((85.5, 25.8), (88.3, 26.6), GOLD), ((88.6, 26.7), (91.5, 26.3), GOLD)])),
    ]},
    {"key": "lifeline", "title": "IS NAS MEIN KYA BEHTA HAI", "lines": [
        ("अब सोचो इस पट्टी से रोज़ क्या क्या गुज़रता है।",
         "AB SOCHO IS PATTI SE ROZ KYA KYA GUZARTA HAI", convoy, {}),
        ("पूरब को जाने वाला बड़ा हाईवे यहीं से जाता है।",
         "PURAB KO JAANE WALA BADA HIGHWAY YAHIN SE JAATA HAI", convoy, dict(items=("truck",))),
        ("आठों राज्यों को जाने वाली रेल लाइन भी यहीं से गुज़रती है।",
         "AATHON RAAJYON KO JAANE WALI RAIL LINE BHI YAHIN SE GUZARTI HAI", convoy, dict(items=("train",))),
        ("तेल की पाइपलाइन भी इसी ज़मीन के नीचे से जाती है।",
         "TEL KI PIPELINE BHI ISI ZAMEEN KE NEECHE SE JAATI HAI", convoy, dict(items=("pipe", "truck"))),
        ("फौज का राशन और गोला बारूद भी इसी रास्ते से सरहद तक पहुंचता है।",
         "FAUJ KA RASHAN AUR GOLA BAAROOD BHI ISI RAASTE SE SARHAD TAK PAHUNCHTA HAI", convoy,
         dict(items=("truck",), army=True)),
        ("सिक्किम जाने वाली मुख्य सड़क भी यहीं से निकलती है।",
         "SIKKIM JAANE WALI MUKHYA SADAK BHI YAHIN SE NIKALTI HAI", M,
         dict(v0=NECK, v1=SIKKIM_V, corridor=GOLD, route=[SILIGURI, SEVOKE, RANGPO, GANGTOK],
              marks=[("GANGTOK", GANGTOK, TEAL, 0.6)])),
        ("यानी ये सिर्फ ज़मीन का एक टुकड़ा नहीं है।",
         "YAANI YEH SIRF ZAMEEN KA EK TUKDA NAHI HAI", M, dict(v0=NECK_CLOSE, v1=NECK, corridor=GOLD)),
        ("ये पूरब के भारत की सांस की नली है।",
         "YEH PURAB KE BHARAT KI SAANS KI NALI HAI", M, dict(v0=NECK, v1=REGION, corridor=RED, pulse=True,
                                                            ne_fill=True)),
        ("और अगर ये नली दब जाए तो सोचो क्या होगा।",
         "AUR AGAR YEH NALI DAB JAAYE TOH SOCHO KYA HOGA", M, dict(v0=REGION, corridor=RED, cut=True, ne_fill=True)),
    ]},
    {"key": "history", "title": "YEH GARDAN BANI KAISE", "lines": [
        ("ये गर्दन किसी ने जानबूझकर नहीं बनाई थी।", "YEH GARDAN KISI NE JAANBOOJHKAR NAHI BANAAYI THI",
         timeline_shot, dict(focus=0)),
        ("उन्नीस सौ सैंतालीस में देश का बंटवारा हुआ।", "1947 MEIN DESH KA BATWARA HUA", timeline_shot, dict(focus=0)),
        ("पूर्वी बंगाल अलग होकर पूर्वी पाकिस्तान बन गया।", "PURVI BANGAL ALAG HOKAR PURVI PAKISTAN BAN GAYA", M,
         dict(v0=BD_V, tint={"bangladesh": SAFFRON}, labels=("nepal", "bhutan", "india"),
              marks=[("PURVI PAKISTAN", (90.3, 23.9), SAFFRON, 0.2)])),
        ("और भारत के पास बची बस ये पतली सी ज़मीन।", "AUR BHARAT KE PAAS BACHI BAS YEH PATLI SI ZAMEEN", M,
         dict(v0=BD_V, v1=NECK, corridor=GOLD, tint={"bangladesh": SAFFRON}, labels=("nepal", "bhutan", "india"))),
        ("उन्नीस सौ बासठ में चीन से जंग हुई तो पहली बार ये डर सच लगने लगा।",
         "1962 MEIN CHINA SE JUNG HUI TOH PEHLI BAAR YEH DAR SACH LAGNE LAGA", timeline_shot, dict(focus=1)),
        ("चीनी फौज अरुणाचल के पहाड़ों से असम की तरफ बढ़ने लगी थी।",
         "CHINI FAUJ ARUNACHAL KE PAHAADON SE ASSAM KI TARAF BADHNE LAGI THI", M,
         dict(v0=NE_V, tint={"china": RED}, arrows=[((92.3, 28.6), (92.4, 27.2), RED)],
              marks=[("ASSAM", (92.9, 26.3), TEAL, 0.5)])),
        ("फिर उन्नीस सौ इकहत्तर में बांग्लादेश बना।", "PHIR 1971 MEIN BANGLADESH BANA", timeline_shot, dict(focus=2)),
        ("और उन्नीस सौ पचहत्तर में सिक्किम भारत का हिस्सा बना।", "AUR 1975 MEIN SIKKIM BHARAT KA HISSA BANA",
         timeline_shot, dict(focus=3)),
        ("नक्शा बदलता रहा लेकिन ये गर्दन वैसी की वैसी पतली रही।",
         "NAKSHA BADALTA RAHA LEKIN YEH GARDAN WAISI KI WAISI PATLI RAHI", M,
         dict(v0=REGION, v1=NECK_CLOSE, corridor=GOLD, caliper=True)),
        ("और सबसे बड़ा खतरा तो अभी बाकी है।", "AUR SABSE BADA KHATRA TOH ABHI BAAKI HAI", M,
         dict(v0=NECK, v1=CHUMBI_V, corridor=GOLD, tint={"china": RED})),
    ]},
    {"key": "china", "title": "CHINA KI NAZAR", "lines": [
        ("अब बात करते हैं असली खतरे की।", "AB BAAT KARTE HAIN ASLI KHATRE KI", radar,
         dict(label="EASTERN SECTOR // ALERT")),
        ("चीन की चुंबी घाटी इस गर्दन से ज़्यादा दूर नहीं है।", "CHINA KI CHUMBI GHAATI IS GARDAN SE ZYADA DOOR NAHI HAI",
         M, dict(v0=CHUMBI_V, v1=REGION, chumbi=True, tint={"china": RED}, corridor=GOLD)),
        ("घाटी के नीचे एक पहाड़ी इलाका है जिसे कहते हैं डोकलाम।",
         "GHAATI KE NEECHE EK PAHAADI ILAAKA HAI JISE KEHTE HAIN DOKLAM", M,
         dict(v0=CHUMBI_V, v1=(88.92, 27.25, 700), tint={"china": RED}, marks=[("DOKLAM", DOKLAM, RED, 0.25)])),
        ("ये ज़मीन भूटान की है लेकिन चीन इस पर अपना दावा करता है।",
         "YEH ZAMEEN BHUTAN KI HAI LEKIN CHINA IS PAR APNA DAAVA KARTA HAI", M,
         dict(v0=(88.92, 27.25, 700), tint={"bhutan": TEAL, "china": RED}, marks=[("DOKLAM", DOKLAM, GOLD)])),
        ("दो हज़ार सत्रह में चीन ने यहां सड़क बनानी शुरू कर दी।", "2017 MEIN CHINA NE YAHAN SADAK BANANI SHURU KAR DI",
         standoff, {}),
        ("सीधा भारत की इसी गर्दन की तरफ।", "SEEDHA BHARAT KI ISI GARDAN KI TARAF", M,
         dict(v0=(88.9, 27.1, 520), corridor=RED, pulse=True, tint={"china": RED},
              arrows=[((88.97, 27.6), (88.93, 27.2), RED)])),
        ("तब भारतीय सेना भूटान के साथ खड़ी होकर उस सड़क के सामने आ गई।",
         "TAB BHARATIYA SENA BHUTAN KE SAATH KHADI HOKAR US SADAK KE SAAMNE AA GAYI", standoff, dict(stop=False)),
        ("तिहत्तर दिन तक दोनों फौजें आमने सामने खड़ी रहीं।", "73 DIN TAK DONO FAUJEIN AAMNE SAAMNE KHADI RAHIN",
         standoff, dict(days=True, stop=True)),
        ("आखिर में दोनों पीछे हटीं और उस जगह सड़क का काम रुक गया।",
         "AAKHIR MEIN DONO PEECHHE HATIN AUR US JAGAH SADAK KA KAAM RUK GAYA", standoff, dict(stop=True)),
        ("लेकिन कहानी यहां खत्म नहीं हुई।", "LEKIN KAHANI YAHAN KHATAM NAHI HUI", radar,
         dict(label="DOKLAM // AFTER 2017")),
        ("रिपोर्ट्स के मुताबिक चीन ने उसके बाद आसपास नई सड़कें और गांव बसा दिए।",
         "REPORTS KE MUTABIK CHINA NE USKE BAAD AASPAAS NAYI SADKEIN AUR GAANV BASA DIYE", villages, {}),
        ("यानी खतरा टला नहीं बस थोड़ा पीछे खिसक गया।", "YAANI KHATRA TALA NAHI BAS THODA PEECHHE KHISAK GAYA", M,
         dict(v0=CHUMBI_V, v1=NECK, chumbi=True, tint={"china": RED}, corridor=RED)),
    ]},
    {"key": "bangladesh", "title": "BANGLADESH KA NAYA MOD", "lines": [
        ("और इब एक नया मोड़ आया है बांग्लादेश की तरफ से।", "AUR IB EK NAYA MOD AAYA HAI BANGLADESH KI TARAF SE", M,
         dict(v0=REGION, v1=BD_V, tint={"bangladesh": GOLD})),
        ("दो हज़ार चौबीस में वहां सरकार बदल गई।", "2024 MEIN WAHAN SARKAR BADAL GAYI", M,
         dict(v0=BD_V, tint={"bangladesh": GOLD}, marks=[("DHAKA", DHAKA, GOLD, 0.15)])),
        ("दो हज़ार पच्चीस में वहां की नई सरकार के मुखिया ने चीन जाकर एक बयान दिया।",
         "2025 MEIN WAHAN KI NAYI SARKAR KE MUKHIYA NE CHINA JAAKAR EK BAYAAN DIYA", M,
         dict(v0=BD_V, v1=EAST, tint={"bangladesh": GOLD, "china": RED},
              arrows=[(DHAKA, (91.5, 29.6), GOLD)])),
        ("कि भारत के ये आठ राज्य चारों तरफ ज़मीन से घिरे हैं और समंदर तक इनकी सीधी पहुंच नहीं है।",
         "KI BHARAT KE YEH 8 RAAJYA CHAARON TARAF ZAMEEN SE GHIRE HAIN AUR SAMANDAR TAK INKI SEEDHI PAHUNCH NAHI HAI", M,
         dict(v0=EAST, v1=NE_V, ne_fill=True, tint={"bangladesh": GOLD})),
        ("और बांग्लादेश को इस पूरे इलाके के समंदर का रखवाला बताया।",
         "AUR BANGLADESH KO IS POORE ILAAKE KE SAMANDAR KA RAKHWALA BATAAYA", M,
         dict(v0=NE_V, v1=KALADAN_V, tint={"bangladesh": GOLD}, arrows=[((90.2, 23.0), (90.4, 20.8), GOLD)],
              labels=("bangladesh", "myanmar", "india"))),
        ("भारत में इस बयान पर घणा हंगामा हुआ।", "BHARAT MEIN IS BAYAAN PAR GHANA HUNGAMA HUA", radar,
         dict(label="DELHI // REACTION", blips=((0.2, -0.3, GOLD), (-0.5, 0.1, GOLD), (0.4, 0.45, GOLD)))),
        ("फिर खबर आई लालमोनिरहाट की।", "PHIR KHABAR AAYI LALMONIRHAT KI", M,
         dict(v0=BD_V, v1=(89.2, 26.2, 420), tint={"bangladesh": GOLD}, corridor=GOLD,
              marks=[("LALMONIRHAT", LALMONIRHAT, RED, 0.2)])),
        ("ये बांग्लादेश का एक पुराना हवाई अड्डा है जो भारत की सरहद से करीब पंद्रह किलोमीटर दूर है।",
         "YEH BANGLADESH KA EK PURANA HAWAI ADDA HAI JO BHARAT KI SARHAD SE KAREEB 15 KILOMETER DOOR HAI", M,
         dict(v0=(89.2, 26.2, 420), tint={"bangladesh": GOLD}, corridor=GOLD,
              marks=[("LALMONIRHAT", LALMONIRHAT, RED)], rings=[(LALMONIRHAT[0], LALMONIRHAT[1], 15, RED)])),
        ("इसे फिर से चालू करने की बातें हुईं और कुछ रिपोर्ट्स में चीन की मदद का ज़िक्र आया।",
         "ISE PHIR SE CHAALU KARNE KI BAATEIN HUIN AUR KUCH REPORTS MEIN CHINA KI MADAD KA ZIKR AAYA", M,
         dict(v0=(89.2, 26.2, 420), v1=REGION, tint={"bangladesh": GOLD, "china": RED},
              marks=[("LALMONIRHAT", LALMONIRHAT, RED)], arrows=[((89.6, 28.6), (89.45, 26.1), RED)])),
        ("बांग्लादेश का कहना है कि ये सिर्फ आम लोगों की उड़ानों के लिए है।",
         "BANGLADESH KA KEHNA HAI KI YEH SIRF AAM LOGON KI UDAANON KE LIYE HAI", M,
         dict(v0=REGION, tint={"bangladesh": GOLD}, marks=[("CIVILIAN?", LALMONIRHAT, GOLD)])),
        ("लेकिन इतनी करीब किसी भी हलचल को भारत हल्के में नहीं ले सकता।",
         "LEKIN ITNI KAREEB KISI BHI HALCHAL KO BHARAT HALKE MEIN NAHI LE SAKTA", radar,
         dict(label="SILIGURI SECTOR // WATCH")),
    ]},
    {"key": "shield", "title": "BHARAT KI DEEWAR", "lines": [
        ("तो भारत ने क्या किया।", "TOH BHARAT NE KYA KIYA", M, dict(v0=REGION, v1=NECK, corridor=GOLD, dome=True)),
        ("इस गर्दन की रखवाली करती है सेना की तैंतीस कोर जिसे त्रिशक्ति कोर कहते हैं।",
         "IS GARDAN KI RAKHWALI KARTI HAI SENA KI 33 CORPS JISE TRISHAKTI CORPS KEHTE HAIN", badge, {}),
        ("इसका मुख्यालय सिलीगुड़ी के पास सुकना में है।", "ISKA MUKHYALAY SILIGURI KE PAAS SUKNA MEIN HAI", M,
         dict(v0=NECK, v1=NECK_CLOSE, corridor=GOLD, marks=[("SUKNA // 33 CORPS HQ", SUKNA, SAFFRON, 0.2)])),
        ("पास ही हासीमारा के हवाई अड्डे पर रफाल लड़ाकू विमानों का एक पूरा दस्ता तैनात है।",
         "PAAS HI HASIMARA KE HAWAI ADDE PAR RAFALE LADAKU VIMAANON KA EK POORA DASTA TAINAAT HAI", jets, {}),
        ("रिपोर्ट्स के मुताबिक एस चार सौ का पहला दस्ता भी इसी इलाके की सुरक्षा के लिए लगाया गया।",
         "REPORTS KE MUTABIK S-400 KA PEHLA DASTA BHI ISI ILAAKE KI SURAKSHA KE LIYE LAGAAYA GAYA", radar,
         dict(label="S-400 // EASTERN SECTOR (REPORTED)", blips=((0.35, -0.45, RED), (-0.2, -0.6, RED)))),
        ("और दो हज़ार पच्चीस के आखिर में सेना ने यहां तीन नए ठिकाने बनाए।",
         "AUR 2025 KE AAKHIR MEIN SENA NE YAHAN 3 NAYE THIKANE BANAAYE", M,
         dict(v0=REGION, corridor=GOLD, marks=[("HASIMARA", HASIMARA, CYAN, 0.1)])),
        ("असम में धुबरी।", "ASSAM MEIN DHUBRI", M,
         dict(v0=REGION, corridor=GOLD, marks=[("DHUBRI", DHUBRI, SAFFRON, 0.05)])),
        ("बिहार में किशनगंज।", "BIHAR MEIN KISHANGANJ", M,
         dict(v0=REGION, corridor=GOLD, marks=[("DHUBRI", DHUBRI, SAFFRON), ("KISHANGANJ", KISHANGANJ, SAFFRON, 0.05, "l")])),
        ("और बंगाल में चोपड़ा।", "AUR BANGAL MEIN CHOPRA", M,
         dict(v0=REGION, corridor=GOLD, marks=[("DHUBRI", DHUBRI, SAFFRON), ("KISHANGANJ", KISHANGANJ, SAFFRON, 0, "l"),
                                               ("CHOPRA", CHOPRA, SAFFRON, 0.05)])),
        ("ये तीनों मिलकर इस गर्दन के चारों तरफ एक मज़बूत तिकोना घेरा बनाते हैं।",
         "YEH TEENON MILKAR IS GARDAN KE CHAARON TARAF EK MAZBOOT TIKONA GHERA BANAATE HAIN", M,
         dict(v0=REGION, corridor=GOLD, route=[DHUBRI, KISHANGANJ, CHOPRA, DHUBRI], route_c=SAFFRON,
              marks=[("DHUBRI", DHUBRI, SAFFRON), ("KISHANGANJ", KISHANGANJ, SAFFRON, 0, "l"), ("CHOPRA", CHOPRA, SAFFRON)])),
        ("यानी अब इस नस को दबाना किसी के लिए भी आसान नहीं है।",
         "YAANI AB IS NAS KO DABANA KISI KE LIYE BHI AASAAN NAHI HAI", M, dict(v0=NECK, corridor=GOLD, dome=True)),
    ]},
    {"key": "routes", "title": "DOOSRA RAASTA", "lines": [
        ("लेकिन असली समझदारी है एक दूसरा रास्ता भी तैयार रखना।", "LEKIN ASLI SAMAJHDAARI HAI EK DOOSRA RAASTA BHI TAIYAAR RAKHNA",
         M, dict(v0=EAST, v1=KALADAN_V, corridor=GOLD, labels=("bangladesh", "myanmar", "india"))),
        ("पहला है कलादान प्रोजेक्ट।", "PEHLA HAI KALADAN PROJECT", M,
         dict(v0=KALADAN_V, labels=("bangladesh", "myanmar", "india"), marks=[("KALADAN", (92.85, 21.0), GOLD, 0.1)])),
        ("कोलकाता से जहाज़ समंदर के रास्ते म्यांमार के सित्तवे बंदरगाह तक जाएगा।",
         "KOLKATA SE JAHAAZ SAMANDAR KE RAASTE MYANMAR KE SITTWE BANDARGAH TAK JAAYEGA", M,
         dict(v0=KALADAN_V, route=[KOLKATA, (88.2, 21.3), (90.0, 20.6), (91.8, 20.0), SITTWE], route_icon="ship",
              labels=("bangladesh", "myanmar", "india"),
              marks=[("KOLKATA", KOLKATA, GOLD, 0, "l"), ("SITTWE", SITTWE, GOLD, 0.7)])),
        ("वहां से नदी के रास्ते पलेतवा तक।", "WAHAN SE NADI KE RAASTE PALETWA TAK", M,
         dict(v0=KALADAN_V, v1=(92.3, 21.5, 330), route=[SITTWE, (92.95, 20.7), PALETWA], route_c=CYAN,
              route_icon="ship", labels=("myanmar",),
              marks=[("SITTWE", SITTWE, GOLD), ("PALETWA", PALETWA, CYAN, 0.7)])),
        ("और फिर सड़क से सीधा मिज़ोरम।", "AUR PHIR SADAK SE SEEDHA MIZORAM", M,
         dict(v0=(92.3, 21.5, 330), v1=(92.6, 22.4, 300), route=[PALETWA, ZORINPUI, AIZAWL], route_c=TEAL,
              route_icon="dot", labels=("myanmar",), marks=[("PALETWA", PALETWA, CYAN), ("MIZORAM", AIZAWL, TEAL, 0.7)])),
        ("बंदरगाह तैयार है लेकिन आखिरी सड़क अभी अधूरी है क्योंकि म्यांमार में लड़ाई चल रही है।",
         "BANDARGAH TAIYAAR HAI LEKIN AAKHIRI SADAK ABHI ADHOORI HAI KYUNKI MYANMAR MEIN LADAAI CHAL RAHI HAI", M,
         dict(v0=(92.6, 22.0, 300), labels=("myanmar",), route=[PALETWA, ZORINPUI], route_c=RED, route_dash=True,
              marks=[("SITTWE: READY", SITTWE, GREEN), ("ROAD: ADHOORI", (92.82, 21.95), RED, 0.3)])),
        ("दूसरा काम है सिक्किम तक रेल।", "DOOSRA KAAM HAI SIKKIM TAK RAIL", M,
         dict(v0=REGION, v1=SIKKIM_V, corridor=GOLD, route=[SEVOKE, RANGPO], route_c=CYAN, route_dash=True,
              marks=[("SEVOKE", SEVOKE, CYAN, 0, "l"), ("RANGPO", RANGPO, CYAN, 0.6)])),
        ("सेवोक से रंगपो तक पहाड़ों में सुरंगें खोदकर रेल लाइन बन रही है।",
         "SEVOKE SE RANGPO TAK PAHAADON MEIN SURANGEIN KHODKAR RAIL LINE BAN RAHI HAI", tunnel_rail, {}),
        ("इसे दो हज़ार सत्ताईस के आखिर तक पूरा करने का लक्ष्य है।", "ISE 2027 KE AAKHIR TAK POORA KARNE KA LAKSHYA HAI",
         tunnel_rail, {}),
        ("और भूटान के साथ भी नई रेल लाइनों की योजना बनी है।", "AUR BHUTAN KE SAATH BHI NAYI RAIL LINON KI YOJANA BANI HAI", M,
         dict(v0=REGION, tint={"bhutan": TEAL}, corridor=GOLD,
              arrows=[((89.05, 26.6), (89.1, 26.92), CYAN), ((90.27, 26.4), (90.5, 26.87), CYAN)])),
        ("मकसद एक ही है कि अगर कभी ये गर्दन दबे तो भी पूरब का भारत अकेला ना पड़े।",
         "MAKSAD EK HI HAI KI AGAR KABHI YEH GARDAN DABE TOH BHI PURAB KA BHARAT AKELA NA PADE", M,
         dict(v0=KALADAN_V, v1=EAST, corridor=GOLD, ne_fill=True,
              route=[KOLKATA, (88.2, 21.3), (90.0, 20.6), (91.8, 20.0), SITTWE, PALETWA, ZORINPUI, AIZAWL],
              route_c=TEAL)),
    ]},
    {"key": "ask", "title": "AB THAARI BAARI", "lines": [
        ("तो बाईस किलोमीटर की ये पट्टी सिर्फ ज़मीन नहीं है।", "TOH 22 KILOMETER KI YEH PATTI SIRF ZAMEEN NAHI HAI", M,
         dict(v0=NECK, v1=NECK_CLOSE, corridor=GOLD, caliper=True)),
        ("ये वो डोर है जो पूरे भारत को एक साथ बांधे रखती है।", "YEH WOH DOR HAI JO POORE BHARAT KO EK SAATH BAANDHE RAKHTI HAI", M,
         dict(v0=REGION, v1=EAST, corridor=GOLD, ne_fill=True)),
        ("इब थारी बारी है भाई।", "IB THAARI BAARI HAI BHAI", question, {}),
        ("भारत को दूसरे रास्ते पर और तेज़ी से काम करना चाहिए या इसी गर्दन को और मज़बूत करना चाहिए।",
         "BHARAT KO DOOSRE RAASTE PAR AUR TEZI SE KAAM KARNA CHAHIYE YA ISI GARDAN KO AUR MAZBOOT KARNA CHAHIYE",
         question, {}),
        ("अपनी राय कमेंट में ज़रूर लिखो।", "APNI RAAY COMMENT MEIN ZAROOR LIKHO", question, {}),
        ("और भारत की ऐसी ही कहानियों के लिए चैनल को सब्सक्राइब कर लो।",
         "AUR BHARAT KI AISI HI KAHANIYON KE LIYE CHANNEL KO SUBSCRIBE KAR LO", finale, {}),
        ("जय हिंद।", "JAI HIND", finale, {}),
    ]},
]

SOURCES = [
    "Siliguri Corridor ~20-22 km at its narrowest (Nepal-Bangladesh), links the 8 North-East states incl. Sikkim "
    "(Wikipedia 'Siliguri Corridor'; The Hindu / BBC explainers)",
    "North-East population ~4.5 crore, Census 2011 (8 states incl. Sikkim)",
    "Doklam stand-off 16 Jun - 28 Aug 2017 (73 days), mutual disengagement (MEA statement, 28 Aug 2017); later "
    "reports/satellite imagery of new Chinese roads and villages near Doklam (e.g. NDTV/India Today 2021)",
    "Yunus remarks in China, March 2025, calling India's NE 'landlocked' and Bangladesh 'guardian of the ocean' "
    "(widely reported: Reuters, The Hindu, 31 Mar-1 Apr 2025)",
    "Lalmonirhat airbase ~12-15 km from the Indian border; revival talk + reported Chinese interest; Bangladesh says "
    "civilian, its army denied Chinese involvement (Business Today 20 May 2025; Organiser; NewsArena)",
    "33 Corps 'Trishakti', HQ Sukna; Rafale No. 101 Sqn at Hasimara (IAF, July 2021); S-400 first squadron reportedly "
    "deployed to cover this sector (media reports 2021-22 - phrased as 'reports')",
    "Three new garrisons Dhubri (Lachit Borphukan Military Station), Kishanganj, Chopra, late 2025; 'triangular grid' "
    "(The Hindu via VisionIAS 17 Nov 2025; The Hitavada 23 Aug 2026; CivilsDaily)",
    "Kaladan: Sittwe port operational (May 2023); Kaletwa-Zorinpui road still under construction, delayed by Myanmar "
    "conflict (Wikipedia KMTTP; Indian ambassador Jan 2026; UNI Oct 2026)",
    "Sevoke-Rangpo rail, 44.96 km, target Dec 2027 (IRCON to parliamentary committee; Swarajya Oct 2026)",
    "India-Bhutan rail links Kokrajhar-Gelephu and Banarhat-Samtse announced Sept 2025 (MEA / PIB)",
]

UPLOAD = {
    "title": "Siliguri Corridor: Bharat Ki 22 KM Ki Gardan | Full Story",
    "description": """
Bharat ke 8 raajya sirf 20-22 km chaudi ek patti se baaki desh se jude hain - Siliguri Corridor, jise duniya
Chicken's Neck kehti hai. Is video mein poori kahani: yeh gardan bani kaise (1947, 1962, 1971, 1975), China ki
Chumbi Valley aur Doklam 2017 ka 73 din ka standoff, Bangladesh ka naya mod aur Lalmonirhat airbase, Bharat ki
Trishakti Corps, Rafale, naye garrisons (Dhubri, Kishanganj, Chopra), aur doosra raasta - Kaladan project aur
Sevoke-Rangpo rail.

Aapki raay: doosre raaste par tezi se kaam ho ya isi gardan ko aur mazboot kiya jaye? Comment mein likho.

Saare facts public reports par based hain (sources neeche). Jahan baat sirf reports tak hai, wahan video mein
"reports ke mutabik" kaha gaya hai.
""",
    "hashtags": "#SiliguriCorridor #ChickensNeck #IndiaChina #Doklam #RealityShift",
    "tags": ["siliguri corridor", "chicken's neck", "chickens neck india", "siliguri corridor explained",
             "doklam standoff", "india china border", "north east india", "kaladan project", "lalmonirhat airbase",
             "trishakti corps", "india bangladesh", "sevoke rangpo railway", "india defence hindi",
             "reality shift"],
    "pinned": "Sawaal seedha hai: Bharat ko Kaladan jaise DOOSRE RAASTE par tezi se kaam karna chahiye (A) ya isi "
              "22 KM ki GARDAN ko aur mazboot karna chahiye (B)? A ya B likho - aur kyun.",
}


def thumbnail(ctx):
    """Corridor close-up in red, NE pulling away, '22 KM' huge on the left, China glowing behind."""
    S = type("S", (), {})()
    S.t, S.d, S.u, S.T = 3.0, 4.0, 1.0, 1.3
    v = (88.95, 26.9, 330)
    draw_region(ctx, v, {"china": (RED, 1.0), "bangladesh": (TEAL, 0.4), "nepal": (TEAL, 0.4)}, ("china",))
    poly(ctx, v, NORTH_EAST)
    rgba(ctx, TEAL, 0.18)
    ctx.fill()
    poly(ctx, v, CORRIDOR)
    rgba(ctx, RED, 0.55)
    ctx.fill_preserve()
    rgba(ctx, RED)
    ctx.set_line_width(7)
    ctx.stroke()
    x, y = proj(v, *SILIGURI)
    glow(ctx, x, y, 260, RED, 0.5)
    vignette(ctx)
    g = cairo.LinearGradient(0, 0, W * 0.6, 0)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.85)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g)
    ctx.paint()
    text(ctx, "22 KM", 70, 360, 300, GOLD, font=IMPACT, anchor="l", stroke=(0, 0, 0), stroke_w=14)
    text(ctx, "BHARAT KI GARDAN", 80, 590, 104, WHITE, font=IMPACT, anchor="l", stroke=(0, 0, 0), stroke_w=10)
    rrect(ctx, 80, 680, 640, 110, 14)
    rgba(ctx, RED)
    ctx.fill()
    text(ctx, "CHINA KI NAZAR", 400, 735, 76, WHITE, font=IMPACT, stroke=(0.3, 0, 0), stroke_w=4)
    chicken_icon(ctx, 1640, 930, 1.0, 0.4)
