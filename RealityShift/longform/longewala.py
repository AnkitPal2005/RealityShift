"""Reality Shift long-form (16:9, ~6 min): Longewala 1971 - 120 jawan, ~45 tank, aur ek sawaal: jeet kiski?

A DEBATE video: the army side (the post held the column all night) vs the air-force side (the Hunters destroyed most
tanks at dawn), told fairly; no party, no person attacked. 8 chapters: hook (payoff shown in the first 45 s, the
mystery "why did the tanks stop?" promised), why the post mattered, the midnight choice, the wire secret, the dawn
Hunters, losses and honours, the debate, the A/B comment question.

Facts are hedged where sources differ ("karib", "kai kisson ke mutabik", "zyaadatar srot").
Fresh vector scenes: night desert post, tank column with headlights, schematic map (not to scale), radio choice,
wire + MINES? fear, burning fuel drums, stuck tracks, Hunter dives, medal, film reel, split debate, A/B cards.

    python make_long.py longewala --kiki-export | --preview | (render)
"""

import math

import cairo

from core.engine import (circle, clamp, ease_in_out, ease_out_back, ease_out_cubic, glow, hexc, lerp, line, rgba,
                         rnd, rrect, text, text_width)
from core.longform import H, W
from longform.arjun_tank import tag, big, vignette, dust, flash, tank as atank
from shorts.akashteer import soldier
from shorts.reality_shift import flag
from shorts.nyoma import jet
from shorts.reality_shift_weapons import fireball

TITLE = "Longewala 1971: 120 Jawan vs 45 Tank - Jeet Kiski Thi?"
MUSIC_STYLE = "pulse"
MUSIC_BPM = 82
MUSIC_SEED = 2611
KIKI_TEMPO = 1.0          # the user sets 1.10x inside KikiVoice

GOLD = hexc("#FFC845")
RED = hexc("#FF4040")
CYAN = hexc("#5CE1E6")
SAFFRON = hexc("#FF9933")
GREEN = hexc("#2FBF5B")
STEEL = hexc("#9AA8B8")
WHITE = (0.95, 0.96, 0.98)
INK = (0.02, 0.03, 0.05)
ENEMY_C = hexc("#8C7A52")         # the column: plain khaki, no markings
IMPACT = "Impact"
GROUND = 800
POST_X = 520

HOT = {"120": SAFFRON, "45": RED, "TANK": RED, "LONGEWALA": GOLD, "JAWANON": SAFFRON, "JAWAN": SAFFRON,
       "VAYU": CYAN, "SENA": CYAN, "HUNTER": CYAN, "CHANDPURI": SAFFRON, "KULDIP": SAFFRON, "JAISALMER": GOLD,
       "RAMGARH": GOLD, "SURANG": RED, "SURANGEIN": RED, "TAAR": GOLD, "RUKENGE": GREEN, "MAHAVIR": GOLD,
       "CHAKRA": GOLD, "BORDER": GOLD, "A": SAFFRON, "B": CYAN, "JAI": SAFFRON, "HIND": GREEN, "RAAZ": GOLD}


# ============================================================ scenery

def sky_desert(ctx, T, night=1.0):
    """Thar sky: night (stars, moon) blending to dawn (orange horizon)."""
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    for p, cn, cd in ((0, "#03060F", "#1B1336"), (0.6, "#0B1530", "#6E2E45"), (0.85, "#16223E", "#D2683A"),
                      (1, "#1C2A48", "#F2AA5E")):
        a, b = hexc(cn), hexc(cd)
        g.add_color_stop_rgb(p, *(q + (r - q) * (1 - night) for q, r in zip(a, b)))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, GROUND + 10)
    ctx.fill()
    if night > 0.2:
        for i in range(110):
            circle(ctx, rnd(i, 3) * W, rnd(i, 4) * 600, 1.4 + 1.6 * rnd(i, 5), WHITE,
                   night * (0.35 + 0.35 * math.sin(T * 2 + i)))
        circle(ctx, 1560, 170, 46, hexc("#E8ECF4"), 0.85 * night)
    if night < 0.85:
        glow(ctx, 1460, 700, 420, hexc("#FFB45A"), 0.55 * (1 - night))
        circle(ctx, 1460, 760, 70, hexc("#FFE0A0"), 0.95 * (1 - night))
    for k, (base, amp, cn, cd) in enumerate(((700, 40, "#1E2740", "#B5714A"), (760, 28, "#232C48", "#C98A58"),
                                            (805, 18, "#2A3250", "#D9A066"))):
        ctx.move_to(0, H)
        for x in range(0, W + 40, 40):
            ctx.line_to(x, base + amp * math.sin(x * 0.004 + k * 1.7) + 0.4 * amp * math.sin(x * 0.013))
        ctx.line_to(W, H)
        ctx.close_path()
        a, b = hexc(cn), hexc(cd)
        rgba(ctx, tuple(q + (r - q) * (1 - night) for q, r in zip(a, b)))
        ctx.fill()


def sandbags(ctx, x0, x1, y, night=1.0):
    c0, c1 = hexc("#B88B55"), hexc("#4A4A5A")
    for row in range(3):
        for k in range(int((x1 - x0) / 56) + 1):
            bx = x0 + k * 56 + (28 if row % 2 else 0)
            if bx > x1:
                continue
            ctx.save()
            ctx.translate(bx, y - 18 - row * 30)
            ctx.scale(32, 16)
            ctx.arc(0, 0, 1, 0, math.tau)
            ctx.restore()
            rgba(ctx, tuple(p + (q - p) * night * 0.7 for p, q in zip(c0, c1)))
            ctx.fill()


def post(ctx, T, x=POST_X, night=1.0, n=3, pose="stand", flag_on=True, s=0.42):
    if flag_on:
        line(ctx, [(x + 120, GROUND + 60), (x + 120, GROUND - 260)], hexc("#C9C9C9"), 6)
        flag(ctx, x + 124, GROUND - 230, 130, 84, "in", T)
    poses = [pose, "binocs", "point"]
    for i in range(n):
        soldier(ctx, x - 160 + 110 * i, GROUND + 70, s, T + i, pose=poses[i % 3])
    sandbags(ctx, x - 260, x + 220, GROUND + 90, night)


def wire(ctx, x, a=1.0):
    for y in range(GROUND - 30, GROUND + 120, 22):
        line(ctx, [(x - 40, y), (x + 40, y + 16)], hexc("#B0B4BA"), 3, 0.85 * a)
    for y in range(GROUND - 40, GROUND + 120, 60):
        line(ctx, [(x, y), (x + 10, y + 50)], hexc("#7A6A52"), 6, a)


def column(ctx, T, x0=1000, advance=1.0, moving=True, night=1.0, n=6, wreck=None, stuck=False):
    """Tank column facing left, spread back to the horizon; headlights at night."""
    slots = [(0, 70, 0.42), (230, 20, 0.36), (420, -20, 0.31), (600, -50, 0.27), (760, -70, 0.24), (900, -85, 0.21)]
    out = []
    for i, (dx, dy, s) in reversed(list(enumerate(slots[:n]))):
        x = x0 + dx + 260 * (1 - advance)
        y = GROUND + dy + (3 * math.sin(T * 9 + i) if moving else 0)
        w = wreck[i] if wreck else 0.0
        body = tuple(p * (1 - 0.7 * w) for p in ENEMY_C)
        roll = -T * 6 if (moving and w == 0) else (T * 14 if stuck else 0)
        atank(ctx, x, y, s, "t72", T=T, flip=True, body=body, roll=roll)
        if stuck and w == 0:
            dust(ctx, x + 120 * s, y, T + i, 0.6)
        if night > 0.3 and w == 0:
            glow(ctx, x - 250 * s, y - 70 * s, 80 * s * 2, hexc("#FFF2B0"), 0.6 * night)
        if w > 0:
            for k in range(7):
                u = (T * 0.5 + k / 7) % 1
                circle(ctx, x + 20 * math.sin(k + T), y - 120 * s - 380 * u * s, (30 + 80 * u) * s,
                       (0.12, 0.11, 0.1), 0.55 * (1 - u) * min(1.0, w * 2))
            glow(ctx, x, y - 60 * s, 160 * s, hexc("#FF7A2A"), 0.5 * w)
        out.append((x, y, s))
    return out


def hunter(ctx, x, y, L, T, dive=0.0, burner=0.6):
    """IAF jet flying LEFT, upright (mirrored, never rotated by pi)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(-1, 1)
    jet(ctx, 0, 0, L, dive, T, burner=burner, c=STEEL)
    ctx.restore()


# ============================================================ shots

def night_post(ctx, S, mode="calm", label=None):
    """mode: calm | column | near | fire | wire | stuck | burn_day"""
    night = 0.0 if mode == "burn_day" else 1.0
    sky_desert(ctx, S.T, night)
    if mode in ("column", "near", "fire", "wire", "stuck"):
        adv = {"column": 0.2 + 0.3 * S.u, "near": 0.5 + 0.5 * S.u}.get(mode, 1.0)
        column(ctx, S.T, x0=1000, advance=adv, moving=mode in ("column", "near"), night=1.0,
               stuck=mode == "stuck")
    if mode == "wire":
        wire(ctx, 900)
        p = 1 + 0.06 * math.sin(S.T * 10)
        ctx.save()
        ctx.translate(900, 420)
        ctx.scale(p, p)
        tag(ctx, "MINES?", 0, 0, RED, 64, a=clamp(S.t / 0.4))
        ctx.restore()
    if mode == "fire":
        u = S.t - 0.4
        line(ctx, [(POST_X + 60, GROUND + 20), (lerp(POST_X + 60, 1010, clamp(u / 0.3)), GROUND + 50)],
             hexc("#FFE38A"), 5, 0.9 if 0 < u < 0.35 else 0)
        fireball(ctx, 1010, GROUND + 60, u - 0.3, size=0.55, seed=3)
        for i in range(4):                                       # shells landing around the post
            v = (S.t * 0.9 + rnd(i, 11)) % 1.5
            if v < 0.7:
                fireball(ctx, 200 + 260 * i + 40 * rnd(i, 12), GROUND + 110, v, size=0.3, seed=i)
    if mode == "burn_day":
        wr = [clamp((S.t - 0.3 - 0.3 * i) / 0.6) for i in range(6)]
        column(ctx, S.T, x0=1000, advance=1.0, moving=False, night=0.0, wreck=wr)
    post(ctx, S.T, night=night, pose="fist" if mode in ("fire", "burn_day") else "stand")
    if label:
        tag(ctx, label, W / 2, 200, GOLD, 44, a=clamp(S.t / 0.4))
    vignette(ctx, 0.5)


def count_card(ctx, S, left=("120", "JAWAN"), right=("~45", "TANK")):
    night_post(ctx, S, mode="column")
    rgba(ctx, (0, 0, 0), 0.35)
    ctx.paint()
    for i, ((n, lab), c, x) in enumerate(((left, SAFFRON, 560), (right, RED, 1360))):
        g = ease_out_back(clamp((S.t - 0.2 - 0.5 * i) / 0.5))
        if g <= 0:
            continue
        ctx.save()
        ctx.translate(x, 330)
        ctx.scale(g, g)
        big(ctx, n, 0, -30, 170, c)
        text(ctx, lab, 0, 100, 56, WHITE, font=IMPACT)
        ctx.restore()
    text(ctx, "VS", W / 2, 320, 90, WHITE, font=IMPACT, a=clamp((S.t - 0.6) / 0.3))


def map_card(ctx, S, focus="post", arrows=False):
    """Schematic map (not to scale): border on the left, Longewala post, Ramgarh, Jaisalmer to the east."""
    rgba(ctx, hexc("#120E0A"))
    ctx.paint()
    rrect(ctx, 160, 110, W - 320, 760, 26)
    rgba(ctx, hexc("#2A2016"))
    ctx.fill()
    for i in range(14):                                          # dune hatching
        x0 = 260 + 110 * i
        line(ctx, [(x0, 640 + 30 * math.sin(i)), (x0 + 50, 610 + 30 * math.sin(i)), (x0 + 100, 640 + 30 * math.sin(i))],
             hexc("#5A4A30"), 3, 0.6)
    ctx.set_dash([24, 14])
    line(ctx, [(380, 140), (330, 400), (400, 640), (350, 860)], RED, 6, 0.9)
    ctx.set_dash([])
    text(ctx, "SARHAD", 300, 170, 30, RED, font=IMPACT)
    pts = {"LONGEWALA": (720, 470), "RAMGARH": (1100, 330), "JAISALMER": (1500, 560)}
    if arrows:
        route = [(400, 420), pts["LONGEWALA"], pts["RAMGARH"], pts["JAISALMER"]]
        n = len(route) - 1
        seg = clamp(S.t / 2.2) * n
        drawn = [route[0]]
        for i in range(n):
            if seg <= i:
                break
            f = clamp(seg - i)
            drawn.append((lerp(route[i][0], route[i + 1][0], f), lerp(route[i][1], route[i + 1][1], f)))
        if len(drawn) > 1:
            ctx.set_dash([30, 16])
            line(ctx, drawn, RED, 10, 0.9)
            ctx.set_dash([])
    for name, (x, y) in pts.items():
        hot = name.startswith(focus.upper()) or (focus == "post" and name == "LONGEWALA")
        if hot:
            glow(ctx, x, y, 110, GOLD, 0.45 + 0.15 * math.sin(S.T * 4))
        circle(ctx, x, y, 18 if hot else 12, GOLD if hot else WHITE)
        text(ctx, name, x, y - 50, 40 if hot else 32, GOLD if hot else WHITE, font=IMPACT)
    text(ctx, "NOT TO SCALE", W - 260, 840, 22, hexc("#8A7A60"), font="Consolas")
    text(ctx, "THAR  //  RAJASTHAN", 340, 830, 26, hexc("#8A7A60"), font="Consolas", anchor="l")


def war_start(ctx, S):
    """3 Dec 1971: night sky with air-raid flashes over the desert."""
    sky_desert(ctx, S.T, 1.0)
    for i in range(5):
        u = (S.t * 0.8 + i * 0.37) % 1.4
        flash(ctx, 300 + 330 * i, 650, u, c=hexc("#FFB45A"))
        if u < 0.5:
            glow(ctx, 300 + 330 * i, 660, 200, hexc("#FF8A3A"), 0.5 * (1 - u / 0.5))
    for i in range(6):
        y = 200 + 60 * i
        line(ctx, [(0, y), (W, y - 300)], hexc("#AFC8FF"), 2, 0.08)
    tag(ctx, "3 DEC 1971", W / 2, 200, GOLD, 56, a=clamp(S.t / 0.4))
    vignette(ctx, 0.5)


def commander(ctx, S, pose="stand", label="MAJ KULDIP SINGH CHANDPURI", sub="23 PUNJAB  //  A COY", stamp=None):
    sky_desert(ctx, S.T, 1.0)
    glow(ctx, 760, 600, 420, SAFFRON, 0.14 + 0.06 * math.sin(S.T * 3))
    line(ctx, [(1180, GROUND + 80), (1180, 300)], hexc("#C9C9C9"), 8)
    flag(ctx, 1184, 340, 220, 140, "in", S.T)
    soldier(ctx, 760, GROUND + 130, 0.7, S.T, pose=pose, commander=True)
    sandbags(ctx, 420, 1300, GROUND + 150)
    tag(ctx, label, 760, 150, WHITE, 36, a=clamp(S.t / 0.4))
    tag(ctx, sub, 760, 215, SAFFRON, 28, a=clamp((S.t - 0.3) / 0.4))
    if stamp:
        k = 1 + 1.2 * (1 - ease_out_cubic(clamp((S.t - 0.5) / 0.25)))
        if S.t > 0.5:
            ctx.save()
            ctx.translate(1350, 560)
            ctx.rotate(-0.12)
            ctx.scale(k, k)
            w = text_width(ctx, stamp, 70, font=IMPACT) + 60
            rrect(ctx, -w / 2, -60, w, 120, 10)
            rgba(ctx, GREEN)
            ctx.set_line_width(9)
            ctx.stroke()
            text(ctx, stamp, 0, 0, 70, GREEN, font=IMPACT)
            ctx.restore()
    vignette(ctx, 0.5)


def radio(ctx, S, choice=False, note=None):
    """Night: the commander with the radio handset; optional two choice cards."""
    sky_desert(ctx, S.T, 1.0)
    rgba(ctx, (0, 0, 0), 0.3)
    ctx.paint()
    soldier(ctx, 480, GROUND + 130, 0.66, S.T, pose="binocs", commander=True)
    rrect(ctx, 600, 560, 110, 150, 10)                            # radio set
    rgba(ctx, hexc("#3A4A2E"))
    ctx.fill()
    line(ctx, [(690, 560), (720, 300)], hexc("#2A2A2A"), 5)
    for k in range(3):
        u = (S.T * 1.2 + k / 3) % 1
        ctx.arc(720, 300, 30 + 90 * u, -2.4, -0.7)
        rgba(ctx, CYAN, 0.6 * (1 - u))
        ctx.set_line_width(4)
        ctx.stroke()
    if note:
        tag(ctx, note, 1300, 300, GOLD, 40, a=clamp(S.t / 0.4))
    if choice:
        for i, (s, c) in enumerate((("CHAUKI PAR DATE RAHO", GREEN), ("PEECHHE HAT JAAO", RED))):
            g = ease_out_back(clamp((S.t - 0.2 - 0.4 * i) / 0.5))
            if g <= 0:
                continue
            ctx.save()
            ctx.translate(1300, 470 + 170 * i)
            ctx.scale(g, g)
            rrect(ctx, -330, -60, 660, 120, 18)
            rgba(ctx, (0.03, 0.05, 0.09), 0.92)
            ctx.fill_preserve()
            rgba(ctx, c)
            ctx.set_line_width(5)
            ctx.stroke()
            text(ctx, s, 0, 0, 50, WHITE, font=IMPACT)
            ctx.restore()
    vignette(ctx, 0.5)


def patrol(ctx, S, sound=True):
    sky_desert(ctx, S.T, 1.0)
    for i in range(3):
        soldier(ctx, 300 + 150 * i + 30 * S.u, GROUND + 90, 0.42, S.T + i, pose="binocs" if i == 1 else "stand")
    if sound:
        for k in range(4):
            u = (S.T * 0.9 + k / 4) % 1
            ctx.arc(1500, 620, 60 + 260 * u, math.pi * 0.7, math.pi * 1.3)
            rgba(ctx, GOLD, 0.6 * (1 - u))
            ctx.set_line_width(6)
            ctx.stroke()
        tag(ctx, "GHAD GHAD GHAD...", 1450, 360, GOLD, 36, a=clamp(S.t / 0.4))
    vignette(ctx, 0.55)


def clock_card(ctx, S, label="MADAD: SUBAH SE PEHLE NAHI"):
    sky_desert(ctx, S.T, 1.0)
    rgba(ctx, (0, 0, 0), 0.45)
    ctx.paint()
    cx, cy, r = W / 2, 470, 210
    circle(ctx, cx, cy, r + 12, hexc("#1A2030"))
    circle(ctx, cx, cy, r, hexc("#E8E4D8"))
    for k in range(12):
        a = k * math.tau / 12
        line(ctx, [(cx + (r - 30) * math.sin(a), cy - (r - 30) * math.cos(a)),
                   (cx + (r - 10) * math.sin(a), cy - (r - 10) * math.cos(a))], INK, 6)
    ah = S.T * 0.6
    am = S.T * 6
    line(ctx, [(cx, cy), (cx + 110 * math.sin(ah), cy - 110 * math.cos(ah))], INK, 12)
    line(ctx, [(cx, cy), (cx + 170 * math.sin(am), cy - 170 * math.cos(am))], RED, 7)
    tag(ctx, label, cx, 800, GOLD, 46, a=clamp(S.t / 0.4))


def hunters(ctx, S, mode="dive", label=None):
    """mode: takeoff | aerial | dive | burn"""
    if mode == "takeoff":
        sky_desert(ctx, S.T, 0.1)
        rrect(ctx, 0, GROUND + 40, W, 80, 0)
        rgba(ctx, hexc("#3A3A40"))
        ctx.fill()
        for k in range(12):
            line(ctx, [(80 + 160 * k, GROUND + 80), (150 + 160 * k, GROUND + 80)], WHITE, 5, 0.7)
        for k in range(2):
            u = clamp((S.t - 0.5 * k) / 2.4)
            x = lerp(1700, 200, u)
            y = GROUND - 400 * max(0, u - 0.35) ** 1.4 + 20
            hunter(ctx, x, y - 30 * k, 300, S.T, dive=-0.25 * clamp((u - 0.35) * 3), burner=0.9)
        tag(ctx, label or "JAISALMER AIRFIELD", W / 2, 200, CYAN, 44, a=clamp(S.t / 0.4))
        return
    sky_desert(ctx, S.T, 0.0)
    if mode == "aerial":
        column(ctx, S.T, x0=700, advance=1.0, moving=False, night=0.0)
        for k in range(2):
            hunter(ctx, 1500 - 600 * S.u - 200 * k, 200 + 60 * k, 260, S.T, burner=0.5)
    else:
        hits = [0.6 + 0.45 * i for i in range(6)] if mode == "burn" else [0.9 + 0.7 * i for i in range(3)] + [99] * 3
        wr = [clamp((S.t - h) / 0.6) for h in hits]
        col = column(ctx, S.T, x0=700, advance=1.0, moving=False, night=0.0, wreck=wr)
        for (x, y, s), h in zip(sorted(col, key=lambda c: -c[2]), hits):
            fireball(ctx, x, y - 30, S.t - h, size=0.55 * s / 0.3, seed=int(x))
        u = (S.t * 0.6) % 1.4
        if u < 1:
            hunter(ctx, lerp(1900, -200, u), lerp(150, 520, u), 280, S.T, dive=0.32)
            hunter(ctx, lerp(2250, 150, u), lerp(110, 470, u), 240, S.T, dive=0.32)
    if label:
        tag(ctx, label, W / 2, 180, CYAN, 46, a=clamp(S.t / 0.4))
    vignette(ctx, 0.45)


def tally(ctx, S):
    rgba(ctx, hexc("#0A0D14"))
    ctx.paint()
    rows = [("DUSHMAN KE TANK", "20+", "ZYAADATAR SROT", RED), ("BHARAT KA NUKSAAN", "BAHUT KAM", "", GREEN)]
    for i, (lab, val, sub, c) in enumerate(rows):
        a = clamp((S.t - 0.3 - 0.6 * i) / 0.4)
        y = 330 + 260 * i
        text(ctx, lab, 520, y, 56, WHITE, font=IMPACT, a=a)
        big(ctx, val, 1300, y, 120, c, a=a)
        if sub:
            text(ctx, sub, 1300, y + 90, 28, hexc("#9AA0AA"), font="Consolas", a=a)
    text(ctx, "GINTI ALAG ALAG SROTON MEIN ALAG", W / 2, 860, 30, GOLD, font="Consolas", a=clamp((S.t - 1.2) / 0.4))


def medal(ctx, S, label="MAHA VIR CHAKRA", sub="MAJ (LATER BRIG) KULDIP SINGH CHANDPURI"):
    g = cairo.RadialGradient(W / 2, 460, 40, W / 2, 460, 900)
    g.add_color_stop_rgb(0, *hexc("#2A1E10"))
    g.add_color_stop_rgb(1, *hexc("#06070B"))
    ctx.set_source(g)
    ctx.paint()
    sw = 1 + 0.03 * math.sin(S.T * 2)
    line(ctx, [(W / 2 - 60, 120), (W / 2, 330)], SAFFRON, 50)
    line(ctx, [(W / 2 + 60, 120), (W / 2, 330)], WHITE, 50)
    ctx.save()
    ctx.translate(W / 2, 470)
    ctx.scale(sw, sw)
    glow(ctx, 0, 0, 260, GOLD, 0.35)
    for k in range(5):                                            # a five-point star medal (stylised)
        a0 = -math.pi / 2 + k * math.tau / 5
        a1 = a0 + math.tau / 10
        ctx.line_to(150 * math.cos(a0), 150 * math.sin(a0))
        ctx.line_to(62 * math.cos(a1), 62 * math.sin(a1))
    ctx.close_path()
    rgba(ctx, hexc("#D8DCE2"))
    ctx.fill()
    circle(ctx, 0, 0, 52, GOLD)
    ctx.restore()
    big(ctx, label, W / 2, 740, 84, GOLD, a=clamp(S.t / 0.4))
    text(ctx, sub, W / 2, 830, 32, WHITE, font="Consolas", a=clamp((S.t - 0.3) / 0.4))


def film(ctx, S):
    rgba(ctx, hexc("#08090D"))
    ctx.paint()
    off = (S.T * 120) % 160
    for y0 in (150, 790):
        rrect(ctx, 0, y0, W, 120, 0)
        rgba(ctx, hexc("#1A1A1E"))
        ctx.fill()
        for k in range(14):
            rrect(ctx, -160 + k * 160 + off, y0 + 35, 70, 50, 8)
            rgba(ctx, hexc("#E8E4D8"), 0.9)
            ctx.fill()
    rrect(ctx, 260, 290, W - 520, 480, 10)
    rgba(ctx, hexc("#2A2418"))
    ctx.fill()
    big(ctx, "BORDER  (1997)", W / 2, 470, 110, GOLD, a=clamp(S.t / 0.4))
    text(ctx, "ISI LADAAI SE PRERIT", W / 2, 620, 46, WHITE, font=IMPACT, a=clamp((S.t - 0.3) / 0.4))


def split(ctx, S, lit=None):
    """Left: the post (JAWAN), right: the Hunters (AIR FORCE)."""
    for x0, x1, side in ((0, W / 2, "army"), (W / 2, W, "air")):
        ctx.save()
        ctx.rectangle(x0, 0, x1 - x0, H)
        ctx.clip()
        if side == "army":
            sky_desert(ctx, S.T, 1.0)
            post(ctx, S.T, x=520, pose="fist")
        else:
            sky_desert(ctx, S.T, 0.0)
            column(ctx, S.T, x0=1300, advance=1.0, moving=False, night=0.0, n=4, wreck=[1, 0.8, 0, 0])
            hunter(ctx, 1500 + 80 * math.sin(S.T), 260, 300, S.T, dive=0.2)
        dim = lit is not None and lit != side
        if dim:
            rgba(ctx, (0, 0, 0), 0.6)
            ctx.paint()
        ctx.restore()
    line(ctx, [(W / 2, 0), (W / 2, H)], WHITE, 6, 0.9)
    tag(ctx, "JAWAN", W / 4, 160, SAFFRON, 60, a=0.4 if lit == "air" else 1.0)
    tag(ctx, "AIR FORCE", 3 * W / 4, 160, CYAN, 60, a=0.4 if lit == "army" else 1.0)


def title_card(ctx, S):
    night_post(ctx, S, mode="burn_day")
    rgba(ctx, (0, 0, 0), 0.4)
    ctx.paint()
    g = ease_out_back(clamp(S.t / 0.6))
    ctx.save()
    ctx.translate(W / 2, 360)
    ctx.scale(g, g)
    big(ctx, "LONGEWALA", 0, 0, 200, GOLD)
    text(ctx, "4 - 5 DECEMBER 1971", 0, 150, 52, WHITE, font=IMPACT)
    ctx.restore()


def question(ctx, S):
    split(ctx, S)
    rgba(ctx, (0, 0, 0), 0.5)
    ctx.paint()
    for i, (k, s, c) in enumerate((("A", "JEET JAWANON KI", SAFFRON), ("B", "JEET AIR FORCE KI", CYAN))):
        g = ease_out_back(clamp((S.t - 0.3 - i * 0.35) / 0.6))
        if g <= 0:
            continue
        ctx.save()
        ctx.translate(W / 2 - 430 + i * 860, 450)
        ctx.scale(g, g)
        rrect(ctx, -390, -110, 780, 220, 22)
        rgba(ctx, (0.03, 0.05, 0.09), 0.92)
        ctx.fill_preserve()
        rgba(ctx, c)
        ctx.set_line_width(5)
        ctx.stroke()
        circle(ctx, -290, 0, 60, c)
        text(ctx, k, -290, 0, 70, INK, font=IMPACT)
        text(ctx, s, 60, 0, 56, WHITE, font=IMPACT)
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
    sky_desert(ctx, S.T, 0.2)
    post(ctx, S.T, x=W / 2, pose="fist", s=0.5)
    big(ctx, "JAI HIND", W / 2, 260, 150, SAFFRON, a=clamp(S.t / 0.5))
    text(ctx, "REALITY SHIFT", W / 2, 390, 40, WHITE, font="Consolas", a=clamp((S.t - 0.3) / 0.4))
    vignette(ctx, 0.45)


# ============================================================ script
# each line: (spoken Hindi for KikiVoice, Roman caption, shot, params)
NP = night_post

CHAPTERS = [
    {"key": "hook", "title": "120 VS 45", "lines": [
        ("चार दिसंबर उन्नीस सौ इकहत्तर की रात थार के रेगिस्तान में एक छोटी सी चौकी थी।",
         "4 DECEMBER 1971 KI RAAT THAR KE REGISTAAN MEIN EK CHHOTI SI CHAUKI THI", NP, dict(mode="calm")),
        ("उस चौकी पर करीब एक सौ बीस जवान थे।", "US CHAUKI PAR KAREEB 120 JAWAN THE", NP,
         dict(mode="calm", label="~120 JAWAN")),
        ("और आधी रात को सामने से टैंकों की आवाज़ आने लगी...", "AUR AADHI RAAT KO SAAMNE SE TANKON KI AAWAZ AANE LAGI",
         NP, dict(mode="column")),
        ("करीब पैंतालीस टैंक और उनके पीछे हज़ारों सैनिक।", "KAREEB 45 TANK AUR UNKE PEECHHE HAZAARON SAINIK",
         count_card, {}),
        ("जवानों के पास न टैंक थे न बड़ी तोपें।", "JAWANON KE PAAS NA TANK THE NA BADI TOPEIN", NP, dict(mode="column")),
        ("और ऊपर से जवाब आया, कि चाहो तो चौकी छोड़कर पीछे हट जाओ।",
         "AUR OOPAR SE JAWAB AAYA KI CHAAHO TO CHAUKI CHHODKAR PEECHHE HAT JAAO", radio, dict(choice=True)),
        ("पर कंपनी कमांडर ने कहा हम यहीं रुकेंगे।", "PAR COMPANY COMMANDER NE KAHA HUM YAHIN RUKENGE", commander,
         dict(pose="fist", stamp="HUM YAHIN RUKENGE")),
        ("सुबह होते होते रेत में दुश्मन के टैंक जल रहे थे।", "SUBAH HOTE HOTE RET MEIN DUSHMAN KE TANK JAL RAHE THE",
         NP, dict(mode="burn_day")),
        ("ये है लोंगेवाला की लड़ाई।", "YE HAI LONGEWALA KI LADAAI", title_card, {}),
        ("पर इस जीत पर, आज तक एक बहस चलती है...", "PAR IS JEET PAR AAJ TAK EK BEHES CHALTI HAI", split, {}),
        ("ये जीत जवानों की थी, या वायु सेना की।", "YE JEET JAWANON KI THI YA VAYU SENA KI", split, dict(lit="army")),
        ("और एक राज़ भी है कि इतने टैंक एक छोटी सी चौकी के सामने रुक क्यों गए...",
         "AUR EK RAAZ BHI HAI KI ITNE TANK EK CHHOTI SI CHAUKI KE SAAMNE RUK KYUN GAYE", NP, dict(mode="wire")),
        ("आज पूरी कहानी सुनेंगे, और आखिर में फैसला आपके हाथ में होगा।",
         "AAJ POORI KAHANI SUNENGE AUR AAKHIR MEIN FAISLA AAPKE HAATH MEIN HOGA", question, {}),
    ]},
    {"key": "chauki", "title": "YE CHAUKI KYUN ZAROORI THI", "lines": [
        ("लोंगेवाला राजस्थान के जैसलमेर ज़िले में है।", "LONGEWALA RAJASTHAN KE JAISALMER ZILE MEIN HAI", map_card,
         dict(focus="post")),
        ("सरहद से कुछ ही किलोमीटर दूर।", "SARHAD SE KUCHH HI KILOMETER DOOR", map_card, dict(focus="post")),
        ("तीन दिसंबर को पाकिस्तान के हवाई हमलों के साथ जंग शुरू हो चुकी थी।",
         "3 DECEMBER KO PAKISTAN KE HAWAI HAMLON KE SAATH JUNG SHURU HO CHUKI THI", war_start, {}),
        ("और पश्चिम के इस रेगिस्तान में दुश्मन ने एक बड़ा दांव खेला।",
         "AUR PASHCHIM KE IS REGISTAAN MEIN DUSHMAN NE EK BADA DAANV KHELA", map_card, dict(focus="post", arrows=True)),
        ("कहा जाता है कि इरादा लोंगेवाला से रामगढ़, और फिर जैसलमेर तक पहुंचने का था।",
         "KAHA JAATA HAI KI IRAADA LONGEWALA SE RAMGARH AUR PHIR JAISALMER TAK PAHUNCHNE KA THA", map_card,
         dict(focus="jaisalmer", arrows=True)),
        ("और रास्ते की पहली रुकावट थी यही चौकी...", "AUR RAASTE KI PEHLI RUKAAVAT THI YAHI CHAUKI", map_card,
         dict(focus="post", arrows=True)),
        ("यहां तेईस पंजाब बटालियन की एक कंपनी तैनात थी।", "YAHAN 23 PUNJAB BATALIYAN KI EK COMPANY TAINAAT THI", NP,
         dict(mode="calm", label="23 PUNJAB  //  A COMPANY")),
        ("और उसकी कमान थी मेजर कुलदीप सिंह चांदपुरी के हाथ में।",
         "AUR USKI KAMAAN THI MAJOR KULDIP SINGH CHANDPURI KE HAATH MEIN", commander, {}),
        ("चौकी के चारों तरफ रेत के टीले थे, और कांटेदार तार की बाड़।",
         "CHAUKI KE CHAARON TARAF RET KE TEELE THE AUR KAANTEDAAR TAAR KI BAAD", NP, dict(mode="calm")),
        ("हथियारों में कुछ मशीनगन, मोर्टार और जीप पर लगी एक टैंक तोड़ने वाली तोप थी।",
         "HATHIYAARON MEIN KUCHH MACHINE GUN MORTAR AUR JEEP PAR LAGI EK TANK TODNE WAALI TOP THI", NP,
         dict(mode="calm", label="MMG  //  MORTAR  //  JEEP RCL")),
    ]},
    {"key": "raat", "title": "AADHI RAAT KA FAISLA", "lines": [
        ("चार दिसंबर की रात एक गश्ती दल बाहर निकला था।", "4 DECEMBER KI RAAT EK GASHTI DAL BAAHAR NIKLA THA", patrol,
         dict(sound=False)),
        ("उसकी अगुवाई कर रहे थे सेकंड लेफ्टिनेंट धरम वीर भान।",
         "USKI AGUVAAI KAR RAHE THE SECOND LIEUTENANT DHARAM VIR BHAN", patrol, dict(sound=False)),
        ("अंधेरे में उन्हें भारी इंजनों की गड़गड़ाहट सुनाई दी।", "ANDHERE MEIN UNHEN BHAARI ENGINON KI GADGADAHAT SUNAAI DI",
         patrol, {}),
        ("ये कोई छोटी टुकड़ी नहीं थी, बल्कि टैंकों का पूरा काफिला था।",
         "YE KOI CHHOTI TUKDI NAHI THI BALKI TANKON KA POORA KAAFILA THA", NP, dict(mode="column")),
        ("खबर चौकी तक पहुंची, और मेजर चांदपुरी ने तुरंत मुख्यालय से बात की।",
         "KHABAR CHAUKI TAK PAHUNCHI AUR MAJOR CHANDPURI NE TURANT MUKHYAALAY SE BAAT KI", radio, {}),
        ("जवाब आया कि मदद सुबह से पहले नहीं पहुंच सकती...", "JAWAB AAYA KI MADAD SUBAH SE PEHLE NAHI PAHUNCH SAKTI",
         clock_card, {}),
        ("रात में वायु सेना के हंटर विमान भी हमला नहीं कर सकते थे।",
         "RAAT MEIN VAYU SENA KE HUNTER VIMAAN BHI HAMLA NAHI KAR SAKTE THE", clock_card,
         dict(label="HUNTER: RAAT MEIN NAHI")),
        ("और उन्हें दो रास्ते दिए गए।", "AUR UNHEN DO RAASTE DIYE GAYE", radio, dict(choice=True)),
        ("या तो चौकी पर डटे रहो, या जवानों को लेकर पीछे हट जाओ।",
         "YA TO CHAUKI PAR DATE RAHO YA JAWANON KO LEKAR PEECHHE HAT JAAO", radio, dict(choice=True)),
        ("पीछे हटना कोई शर्म की बात नहीं होती।", "PEECHHE HATNA KOI SHARM KI BAAT NAHI HOTI", radio, dict(choice=True)),
        ("पर अगर चौकी छूटती, तो जैसलमेर का रास्ता खुल सकता था।",
         "PAR AGAR CHAUKI CHHOOTTI TO JAISALMER KA RAASTA KHUL SAKTA THA", map_card, dict(focus="jaisalmer", arrows=True)),
        ("मेजर चांदपुरी ने फैसला किया कि हम यहीं रुकेंगे।", "MAJOR CHANDPURI NE FAISLA KIYA KI HUM YAHIN RUKENGE",
         commander, dict(pose="fist", stamp="HUM YAHIN RUKENGE")),
        ("जवानों ने खाइयों में पोज़िशन ली, और इंतज़ार शुरू हुआ।", "JAWANON NE KHAAIYON MEIN POSITION LI AUR INTEZAAR SHURU HUA",
         NP, dict(mode="calm")),
    ]},
    {"key": "taar", "title": "TAAR KA RAAZ", "lines": [
        ("आधी रात के बाद टैंकों का काफिला चौकी के पास पहुंच गया।",
         "AADHI RAAT KE BAAD TANKON KA KAAFILA CHAUKI KE PAAS PAHUNCH GAYA", NP, dict(mode="near")),
        ("और फिर वो हुआ जिसकी उम्मीद किसी को नहीं थी...", "AUR PHIR WO HUA JISKI UMEED KISI KO NAHI THI", NP,
         dict(mode="near")),
        ("टैंक कांटेदार तार के पास आकर रुक गए।", "TANK KAANTEDAAR TAAR KE PAAS AAKAR RUK GAYE", NP, dict(mode="wire")),
        ("दुश्मन को लगा कि तार के आगे बारूदी सुरंगें बिछी हैं।", "DUSHMAN KO LAGA KI TAAR KE AAGE BAROODI SURANGEIN BICHHI HAIN",
         NP, dict(mode="wire")),
        ("कई किस्सों के मुताबिक वहां पूरी सुरंगें बिछी ही नहीं थीं।",
         "KAI KISSON KE MUTABIK WAHAN POORI SURANGEIN BICHHI HI NAHI THIN", NP, dict(mode="wire")),
        ("पर इस डर ने टैंकों को घंटों तक रोके रखा।", "PAR IS DAR NE TANKON KO GHANTON TAK ROKE RAKHA", clock_card,
         dict(label="GHANTON KI DER")),
        ("इसी बीच, जीप पर लगी तोप ने सामने के टैंकों पर निशाना लगाया।",
         "ISI BEECH JEEP PAR LAGI TOP NE SAAMNE KE TANKON PAR NISHANA LAGAAYA", NP, dict(mode="fire")),
        ("कुछ टैंकों के बाहर लगे ईंधन के ड्रम में आग लग गई।", "KUCHH TANKON KE BAAHAR LAGE EENDHAN KE DRUM MEIN AAG LAG GAYI",
         NP, dict(mode="fire")),
        ("और उस आग की रोशनी में बाकी टैंक भी साफ दिखने लगे।", "AUR US AAG KI ROSHNI MEIN BAAKI TANK BHI SAAF DIKHNE LAGE",
         NP, dict(mode="fire")),
        ("कई गाड़ियां नरम रेत में फंस गईं।", "KAI GAADIYAN NARAM RET MEIN PHANS GAYIN", NP, dict(mode="stuck")),
        ("पूरी रात गोले बरसते रहे, पर चौकी नहीं गिरी।", "POORI RAAT GOLE BARASTE RAHE PAR CHAUKI NAHI GIRI", NP,
         dict(mode="fire")),
        ("करीब एक सौ बीस जवान हज़ारों के सामने रात भर डटे रहे।", "KAREEB 120 JAWAN HAZAARON KE SAAMNE RAAT BHAR DATE RAHE",
         count_card, dict(right=("1000s", "SAINIK"))),
    ]},
    {"key": "hunter", "title": "SUBAH KE HUNTER", "lines": [
        ("और फिर पूरब में रोशनी हुई...", "AUR PHIR POORAB MEIN ROSHNI HUI", NP, dict(mode="calm")),
        ("जैसलमेर के हवाई अड्डे से वायु सेना के हंटर विमान उड़े।",
         "JAISALMER KE HAWAI ADDE SE VAYU SENA KE HUNTER VIMAAN UDE", hunters, dict(mode="takeoff")),
        ("पायलट ऊपर पहुंचे, तो नीचे का नज़ारा हैरान करने वाला था।",
         "PILOT OOPAR PAHUNCHE TO NEECHE KA NAZAARA HAIRAAN KARNE WAALA THA", hunters, dict(mode="aerial")),
        ("खुले रेगिस्तान में टैंक बिना किसी आड़ के खड़े थे।", "KHULE REGISTAAN MEIN TANK BINA KISI AAD KE KHADE THE", hunters,
         dict(mode="aerial")),
        ("और ऊपर से उन्हें बचाने वाला कोई हवाई कवर नहीं था।", "AUR OOPAR SE UNHEN BACHAANE WAALA KOI HAWAI COVER NAHI THA",
         hunters, dict(mode="aerial", label="NO AIR COVER")),
        ("हंटर विमानों ने एक के बाद एक हमले किए।", "HUNTER VIMAANON NE EK KE BAAD EK HAMLE KIYE", hunters, dict(mode="dive")),
        ("रेत में टैंक एक एक करके जलने लगे।", "RET MEIN TANK EK EK KARKE JALNE LAGE", hunters, dict(mode="burn")),
        ("जो टैंक पीछे मुड़े वो भी रेत में धीमे पड़ गए।", "JO TANK PEECHHE MUDE WO BHI RET MEIN DHEEME PAD GAYE", NP,
         dict(mode="stuck")),
        ("दिन भर ये हमले चलते रहे।", "DIN BHAR YE HAMLE CHALTE RAHE", hunters, dict(mode="dive")),
        ("और दुश्मन का पूरा हमला बिखर गया।", "AUR DUSHMAN KA POORA HAMLA BIKHAR GAYA", hunters, dict(mode="burn")),
    ]},
    {"key": "samman", "title": "NUKSAAN AUR SAMMAN", "lines": [
        ("इस लड़ाई में दुश्मन के कितने टैंक तबाह हुए, इस पर अलग अलग गिनती मिलती है।",
         "IS LADAAI MEIN DUSHMAN KE KITNE TANK TABAAH HUE IS PAR ALAG ALAG GINTI MILTI HAI", tally, {}),
        ("पर ज़्यादातर स्रोत बीस से ज़्यादा टैंक बताते हैं।", "PAR ZYAADATAR SROT 20 SE ZYAADA TANK BATAATE HAIN", tally, {}),
        ("वहीं भारत की तरफ नुकसान बहुत कम हुआ।", "WAHIN BHARAT KI TARAF NUKSAAN BAHUT KAM HUA", tally, {}),
        ("मेजर कुलदीप सिंह चांदपुरी को महावीर चक्र मिला।", "MAJOR KULDIP SINGH CHANDPURI KO MAHAVIR CHAKRA MILA", medal, {}),
        ("जो युद्ध में देश का दूसरा सबसे बड़ा वीरता सम्मान है।", "JO YUDDH MEIN DESH KA DOOSRA SABSE BADA VEERTA SAMMAN HAI",
         medal, {}),
        ("बाद में वो ब्रिगेडियर बनकर रिटायर हुए।", "BAAD MEIN WO BRIGADIER BANKAR RETIRE HUE", medal, {}),
        ("उन्नीस सौ सत्तानवे की फिल्म बॉर्डर इसी लड़ाई से प्रेरित थी।",
         "1997 KI FILM BORDER ISI LADAAI SE PRERIT THI", film, {}),
        ("पर फिल्म में कहानी के लिए कई बातें बदली गई थीं।", "PAR FILM MEIN KAHANI KE LIYE KAI BAATEIN BADLI GAYI THIN", film,
         {}),
        ("और यहीं से शुरू होती है वो बहस...", "AUR YAHIN SE SHURU HOTI HAI WO BEHES", split, {}),
    ]},
    {"key": "behes", "title": "JEET KISKI", "lines": [
        ("एक पक्ष कहता है कि असली जीत जवानों की थी।", "EK PAKSH KEHTA HAI KI ASLI JEET JAWANON KI THI", split,
         dict(lit="army")),
        ("अगर वो रात में चौकी छोड़ देते, तो सुबह तक टैंक बहुत आगे निकल चुके होते।",
         "AGAR WO RAAT MEIN CHAUKI CHHOD DETE TO SUBAH TAK TANK BAHUT AAGE NIKAL CHUKE HOTE", map_card,
         dict(focus="jaisalmer", arrows=True)),
        ("उन्होंने पूरे काफिले को एक जगह रोके रखा।", "UNHONE POORE KAAFILE KO EK JAGAH ROKE RAKHA", NP, dict(mode="wire")),
        ("और इसी वजह से सुबह हंटर को खुले में निशाना मिला।", "AUR ISI VAJAH SE SUBAH HUNTER KO KHULE MEIN NISHANA MILA",
         hunters, dict(mode="aerial")),
        ("दूसरा पक्ष कहता है, कि ज़्यादातर टैंक तो हवाई हमलों में तबाह हुए।",
         "DOOSRA PAKSH KEHTA HAI KI ZYAADATAR TANK TO HAWAI HAMLON MEIN TABAAH HUE", split, dict(lit="air")),
        ("उनके हिसाब से एक कंपनी पूरी टैंक ब्रिगेड को दिन भर नहीं रोक सकती थी।",
         "UNKE HISAAB SE EK COMPANY POORI TANK BRIGADE KO DIN BHAR NAHI ROK SAKTI THI", hunters, dict(mode="burn")),
        ("दोनों तरफ के पुराने अफसरों ने, इस पर अपनी अपनी बात रखी है।",
         "DONON TARAF KE PURAANE AFSARON NE IS PAR APNI APNI BAAT RAKHI HAI", split, {}),
        ("और सच ये है, कि ये लड़ाई ज़मीन और आसमान ने मिलकर जीती।",
         "AUR SACH YE HAI KI YE LADAAI ZAMEEN AUR AASMAAN NE MILKAR JEETI", split, {}),
        ("पर अगर आपको एक को चुनना हो तो...", "PAR AGAR AAPKO EK KO CHUNNA HO TO", question, {}),
    ]},
    {"key": "aap", "title": "AAPKI BAARI", "lines": [
        ("कमेंट में लिखो।", "COMMENT MEIN LIKHO", question, {}),
        ("ए अगर जीत जवानों की थी।", "A AGAR JEET JAWANON KI THI", question, {}),
        ("बी अगर जीत वायु सेना की थी।", "B AGAR JEET VAYU SENA KI THI", question, {}),
        ("और साथ में एक लाइन में वजह भी लिखना।", "AUR SAATH MEIN EK LINE MEIN VAJAH BHI LIKHNA", question, {}),
        ("ऐसी ही जंग की अनसुनी कहानियों के लिए रियलिटी शिफ्ट से जुड़े रहो।",
         "AISI HI JUNG KI ANSUNI KAHANIYON KE LIYE REALITY SHIFT SE JUDE RAHO", finale, {}),
        ("जय हिंद।", "JAI HIND", finale, {}),
    ]},
]

SOURCES = [
    "Battle of Longewala, 4-7 Dec 1971: A Coy 23 Punjab (~120 men) under Maj Kuldip Singh Chandpuri held the post "
    "against a Pakistani brigade group with roughly 40-45 tanks (sources give 40-65); the column halted at the wire "
    "fearing mines; a jeep-mounted 106 mm RCL engaged tanks; external fuel drums caught fire; IAF Hunters from "
    "Jaisalmer attacked from first light (Wikipedia 'Battle of Longewala', citing official and published histories)",
    "Kuldip Singh Chandpuri: Maha Vir Chakra; retired as Brigadier (Wikipedia 'Kuldip Singh Chandpuri')",
    "2nd Lt Dharam Vir Bhan led the patrol that detected the column (Wikipedia 'Battle of Longewala')",
    "Army-vs-air-force credit debate among veterans and the film 'Border' (1997) being inspired by the battle with "
    "dramatised changes (Wikipedia 'Battle of Longewala', 'Border (1997 film)')",
    "Tank losses: figures differ by source; 'more than 20' is used as the safe common floor; Indian losses were light "
    "(Wikipedia; IAF history pages)",
]

UPLOAD = {
    "title": "Longewala 1971: 120 Jawan vs 45 Tank - Jeet Kiski Thi?",
    "description": """
4 December 1971 ki raat, Thar ke Longewala post par kareeb 120 jawan - aur saamne kareeb 45 tank. Peechhe hatne ki
chhoot thi, phir bhi Major Kuldip Singh Chandpuri ne kaha: hum yahin rukenge. Subah IAF ke Hunter aaye aur tank ek
ek karke jalne lage. Par aaj tak bahas hai - Longewala ki jeet jawanon ki thi ya Vayu Sena ki?

Is video mein: chauki kyun zaroori thi, aadhi raat ka faisla, taar ka raaz (tank ruke kyun), subah ke Hunter,
nuksaan aur samman, aur dono paksh ki poori baat.

Ye ek debate video hai - dono ki bahaduri ko salaam. Kisi party ya vyakti par hamla nahi.

Aapki raay: A = jeet jawanon ki, B = jeet Air Force ki. Comment mein likho - aur vajah bhi.

Jahan sources mein sankhya alag hai, wahan video mein "kareeb" ya "zyaadatar srot" kaha gaya hai. Sources:
- Wikipedia: Battle of Longewala
- Wikipedia: Kuldip Singh Chandpuri
- Wikipedia: Border (1997 film)
- Indian Air Force history pages: Longewala, Hunters from Jaisalmer
""",
    "hashtags": "#Longewala #IndianArmy #IndianAirForce #1971War #RealityShift",
    "tags": ["longewala", "battle of longewala", "longewala 1971", "longewala ki ladai", "1971 war", "kuldip singh chandpuri",
             "23 punjab", "hawker hunter", "indian air force", "border movie real story", "india pakistan 1971",
             "indian army history hindi", "thar desert war", "reality shift"],
    "pinned": "Seedha sawaal: Longewala 1971 ki jeet kiski thi? A = raat bhar chauki na chhodne wale JAWAN, B = subah "
              "aaye HUNTER pilots. A ya B likho - aur ek line mein vajah bhi.",
}


def thumbnail(ctx):
    """Night post with a raised fist on the left, burning tank column and a Hunter on the right; '120 VS 45 TANK'."""
    class _S:
        T = 1.2
        t = 2.0
        u = 1.0
    sky_desert(ctx, 1.0, 0.45)
    column(ctx, 1.0, x0=1050, advance=1.0, moving=False, night=0.4, wreck=[0.9, 0, 0.7, 0, 0, 0])
    fireball(ctx, 1060, GROUND + 20, 0.35, size=0.8)
    hunter(ctx, 1450, 330, 380, 1.0, dive=0.25, burner=0.8)
    post(ctx, 1.0, x=430, pose="fist", s=0.55)
    vignette(ctx, 0.55)
    g = cairo.LinearGradient(0, 0, 0, H * 0.5)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.8)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g)
    ctx.paint()
    big(ctx, "120 JAWAN VS 45 TANK", W / 2, 160, 170, GOLD)
    rrect(ctx, W / 2 - 430, 290, 860, 120, 16)
    rgba(ctx, RED)
    ctx.fill()
    text(ctx, "JEET KISKI THI?", W / 2, 350, 90, WHITE, font=IMPACT, stroke=(0.3, 0, 0), stroke_w=4)
