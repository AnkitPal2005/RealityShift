"""Eklavya Krishna: jis Eklavya ne guru ko angootha diya, use baad mein khud Shri Krishna ne maara (~36-40s, 7 scenes).

Usage (from SanatanKatha/):
  python make.py eklavya_krishna --preview       # contact sheet + thumbnail
  python make.py eklavya_krishna --check         # YPP policy gate
  python make.py eklavya_krishna --kiki-export   # KikiVoice text
  python make.py eklavya_krishna --kiki-split    # cut the narrator voice into line clips (Whisper anchored)
  python make.py eklavya_krishna --engine files  # final render from the user's KikiVoice clips

Rahasya (Mahabharata, Drona Parva - after Ghatotkach falls, Krishna explains to Arjun):
"For your good, Jarasandh, Shishupal and the Nishada Eklavya were slain one after another. Had they lived they
would have fought for Duryodhan; Eklavya with his thumb could not have been beaten even by the gods."
The famous half (Adi Parva): clay Drona in the forest, Eklavya out-shoots Arjun, Drona asks the thumb as dakshina.
The hidden half: Eklavya, a great archer even with four fingers, joins Jarasandh's side against the Yadavas
(Harivamsha) and falls to Krishna. The last line ("isiliye") loops into the hook ("jis Eklavya ne...").

Debate (pinned comment): Kya Krishna ka Eklavya ko maarna dharm tha? Kept on Krishna's neeti, never on caste.
"""

import math
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cairo

from core import engine, katha, upload_kit  # noqa: F401
from core.katha import *  # noqa: F401,F403
import core.devta as dv
from core.devta import group, place, smooth, ink, ell, gem, limb, hand, sheen, eye, shade

from kathas.abhimanyu import drona                                  # Acharya Drona: poses command / stand
from kathas.arjun_rath import arjuna                                # Arjun: poses bow / shock / namaste
from kathas.ghatotkach_akshauhini import night_kurukshetra, kaurava_mob, dust_cloud, ease_in

TOPIC = "EKLAVYA KO KRISHNA NE MAARA DRONA PARVA RAHASYA ANGOOTHA KE BAAD"
OUTPUTS = {"edge": "eklavya_krishna_short.mp4"}
MUSIC_STYLE = "tension"   # mystery + a hidden truth; sapt_saal used ambient
MUSIC_BPM = 82            # >= 6 BPM away from sapt_saal (90)
MUSIC_VOLUME = 0.11
TAIL_PAD = 0.12           # calm storytelling (user, 23 Nov): a small breath between lines, never a dead gap
MAX_GAP = 0.2

FEET = GROUND - 10
EK_SKIN = hexc("#9A6238")
EK_HAIR = hexc("#1A100A")
HIDE = hexc("#C49A62")
HIDE_DK = hexc("#7A5430")
BAND = hexc("#B8321E")
CLAY = hexc("#B9773E")
CHAKRA_GOLD = hexc("#FFD24A")

SOURCES = [
    "Mahabharata, Adi Parva (Sambhava Parva, Drona's pupils): Eklavya builds a clay image of Drona in the forest, "
    "out-shoots Arjun, and gives his right thumb as guru dakshina without hesitation.",
    "Mahabharata, Drona Parva (Ghatotkacha-vadha, Krishna to Arjun, KMG section 181): Jarasandh, Shishupal and the "
    "Nishada Eklavya were slain for the Pandavas' good; had they lived they would have sided with Duryodhan; "
    "Eklavya with his thumb could not be beaten even by gods, Danavas and Rakshasas together.",
    "Harivamsha: Eklavya fights on Jarasandh's side against the Yadavas (variant details of how he falls differ "
    "between texts, so the script only says 'Krishna ke haathon').",
]


# =============================================================================
# Scenery and props
# =============================================================================
def forest_bg(ctx, t, warm=1.0):
    """Deep forest at golden dawn: 4-stop sky, sun disc, three tree-line layers, peepal, ferns, floating dust."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in ((0.0, "#1C2A4A"), (0.28, "#4A5A7A"), (0.46, "#E39A5A"), (0.58, "#FFD08A"), (0.70, "#2E4A26"),
                  (1.0, "#1A2A14")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.rectangle(-80, -80, W + 160, H + 160)
    ctx.fill()
    dv.sun_disc(ctx, 560, 720, 80, t, a=0.85 * warm, rays=18)
    for k, (yy, c, amp, step) in enumerate(((860, "#3A5A34", 70, 70), (930, "#2C4A28", 90, 54), (1010, "#1E3A1C", 60, 40))):
        ctx.move_to(-80, H)
        for x in range(-80, W + 81, step):
            bump = amp * (0.55 + 0.45 * abs(math.sin(x / (90 + 30 * k) + k * 1.3)))
            ctx.line_to(x, yy - bump)
        ctx.line_to(W + 80, H)
        ctx.close_path()
        rgba(ctx, hexc(c))
        ctx.fill()
    for i, x in enumerate((40, 1030)):                         # big framing trunks
        smooth(ctx, [(x - 46, GROUND + 20), (x - 30, 300), (x + 30, 300), (x + 46, GROUND + 20)], k=0.08)
        ink(ctx, hexc("#3A2616"), 4)
        for k in range(5):
            r = 120 - 14 * k
            circle(ctx, x + (40 if i == 0 else -40) + 30 * math.sin(k * 2 + t * 0.6), 260 + 70 * k, r,
                   hexc("#244A20"), 0.95)
    ctx.rectangle(-80, GROUND - 20, W + 160, H)
    rgba(ctx, hexc("#24361A"))
    ctx.fill()
    for i in range(46):                                        # ferns and grass tufts
        x = rnd(i, 21) * W
        y = GROUND - 8 + 60 * rnd(i, 22)
        for a in (-0.6, -0.2, 0.2, 0.6):
            line(ctx, [(x, y), (x + 34 * math.sin(a + 0.05 * math.sin(t + i)), y - 30 * math.cos(a))],
                 hexc("#4E7A36"), 5, 0.85)
    for i in range(26):                                        # light motes
        x = (rnd(i, 3) * W + t * 22 * (0.4 + rnd(i, 4))) % W
        y = 520 + 600 * rnd(i, 5) + 14 * math.sin(t * 1.3 + i)
        circle(ctx, x, y, 2 + 3 * rnd(i, 6), hexc("#FFE9B0"), 0.25 + 0.2 * math.sin(t * 2 + i))


def war_camp_bg(ctx, t):
    """Jarasandh's camp at dusk: blood-red sky, smoke columns, spear line on the ridge."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in ((0.0, "#120616"), (0.30, "#3A0E24"), (0.50, "#9A2A1A"), (0.62, "#E0662A"), (0.72, "#2A0E10"),
                  (1.0, "#140608")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.rectangle(-80, -80, W + 160, H + 160)
    ctx.fill()
    dv.sun_disc(ctx, 820, 760, 90, t, a=0.7, rays=12)
    for k in range(3):                                         # smoke columns
        x0 = 160 + 360 * k
        for j in range(8):
            yy = 900 - j * 70 - (t * 30) % 70
            circle(ctx, x0 + 30 * math.sin(j * 0.8 + t * 0.5 + k), yy, 40 + j * 8, hexc("#2A1A1E"), 0.18)
    for k, (yy, c, amp) in enumerate(((930, "#4A1624", 60), (1010, "#2A0C16", 45))):
        ctx.move_to(-80, H)
        for x in range(-80, W + 81, 40):
            ctx.line_to(x, yy - amp * abs(math.sin(x / 160 + k)))
        ctx.line_to(W + 80, H)
        ctx.close_path()
        rgba(ctx, hexc(c))
        ctx.fill()
    for i in range(30):                                        # spear line on the ridge
        x = 20 + i * 36
        y = 935 - 50 * abs(math.sin(x / 160))
        line(ctx, [(x, y), (x + 4, y - 70)], hexc("#1A0A0C"), 4)
    ctx.rectangle(-80, GROUND - 20, W + 160, H)
    rgba(ctx, hexc("#2A1410"))
    ctx.fill()
    for i in range(24):                                        # embers
        x = (rnd(i, 7) * W + t * 40) % W
        y = 1100 - ((t * 60 * (0.5 + rnd(i, 8)) + rnd(i, 9) * 600) % 700)
        circle(ctx, x, y, 3 + 2 * rnd(i, 10), hexc("#FF9A3A"), 0.6)


def clay_drona(ctx, x, y, s, t, a=1.0):
    """The clay image of Drona Eklavya made: Drona's form as a flat clay silhouette on a mud platform."""
    rrect(ctx, x - 150, y - 40, 300, 50, 12)
    ink(ctx, hexc("#6A4222"), 4)
    for k in range(5):                                         # offered flowers
        circle(ctx, x - 100 + 50 * k, y - 46, 12, hexc("#FF8A2A") if k % 2 else hexc("#FFD24A"), a)
    dv.silhouette(ctx, lambda: drona(ctx, x, y - 40, s, 0.0, pose="stand", flip=True), c=CLAY, a=a)
    glow(ctx, x, y - 40 - 520 * s, 120, hexc("#FFE0A0"), 0.25 * a + 0.05 * math.sin(t * 2))
    for k in range(6):                                         # clay cracks / tool marks
        yy = y - 120 - 70 * k
        line(ctx, [(x - 30 + 8 * k, yy), (x + 10 + 6 * k, yy - 14)], shade(CLAY, 0.7), 3, 0.7 * a)


def target_tree(ctx, x, t, hits=0):
    """A tree with a painted target ring; hits = arrows stuck in the centre."""
    smooth(ctx, [(x - 40, GROUND + 10), (x - 26, 640), (x + 26, 640), (x + 40, GROUND + 10)], k=0.08)
    ink(ctx, hexc("#5A3A20"), 4)
    for k in range(4):
        circle(ctx, x + 40 * math.sin(k * 2.1), 600 - 60 * k, 110 - 12 * k, hexc("#2E5A28"), 0.95)
    for r, c in ((46, "#F3E2BC"), (32, "#B8321E"), (16, "#F3E2BC")):
        circle(ctx, x, 800, r, hexc(c))
    for k in range(hits):
        ang = math.pi + (k - (hits - 1) / 2) * 0.12
        x1, y1 = x - 6, 800 + (k - (hits - 1) / 2) * 6
        line(ctx, [(x1, y1), (x1 + 110 * math.cos(ang), y1 + 110 * math.sin(ang))], hexc("#F3E2BC"), 5)
        circle(ctx, x1 + 110 * math.cos(ang), y1 + 110 * math.sin(ang), 7, BAND)


def plain_arrow(ctx, x, y, ang, L=150, a=1.0):
    """Ordinary forest arrow (no divine glow), head at (x, y) pointing along ang."""
    bx, by = x - L * math.cos(ang), y - L * math.sin(ang)
    line(ctx, [(bx, by), (x, y)], dv.OUTLINE, 9, a)
    line(ctx, [(bx, by), (x, y)], hexc("#E8D2A0"), 5, a)
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.move_to(14, 0)
    ctx.line_to(-12, -10)
    ctx.line_to(-12, 10)
    ctx.close_path()
    rgba(ctx, hexc("#C8C8D0"), a)
    ctx.fill()
    ctx.restore()
    for side in (-1, 1):
        line(ctx, [(bx, by), (bx - 22 * math.cos(ang + side * 0.5), by - 22 * math.sin(ang + side * 0.5))], BAND, 5, a)


def sudarshan(ctx, x, y, r, t, a=1.0):
    """Spinning Sudarshan Chakra: glowing gold disc with teeth."""
    if a <= 0:
        return
    glow(ctx, x, y, r * 3.2, CHAKRA_GOLD, 0.6 * a)
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(t * 12)
    for k in range(12):
        ctx.save()
        ctx.rotate(k / 12 * math.tau)
        ctx.move_to(r * 0.8, -r * 0.16)
        ctx.line_to(r * 1.28, 0)
        ctx.line_to(r * 0.8, r * 0.16)
        ctx.close_path()
        rgba(ctx, GOLD_HI, a)
        ctx.fill()
        ctx.restore()
    ctx.arc(0, 0, r, 0, math.tau)
    rgba(ctx, CHAKRA_GOLD, a)
    ctx.fill()
    ctx.arc(0, 0, r * 0.62, 0, math.tau)
    rgba(ctx, hexc("#FFF6D0"), a)
    ctx.fill()
    for k in range(8):
        ang = k / 8 * math.tau
        line(ctx, [(0, 0), (r * 0.62 * math.cos(ang), r * 0.62 * math.sin(ang))], GOLD_DK, 4, a)
    circle(ctx, 0, 0, r * 0.18, GOLD_DK, a)
    ctx.restore()


def jarasandh_shadow(ctx, x, y, s, t, a=1.0):
    """Jarasandh on the far ridge: a huge king's silhouette with crown and gada, ember eyes."""
    if a <= 0:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    glow(ctx, 0, -420, 380, hexc("#C0301A"), 0.4 * a)
    c = hexc("#140608")
    smooth(ctx, [(-170, -480), (170, -480), (190, -240), (120, 0), (-120, 0), (-190, -240)], k=0.12)
    rgba(ctx, c, a)
    ctx.fill()
    ell(ctx, 0, -600, 100, 110)
    rgba(ctx, c, a)
    ctx.fill()
    ctx.move_to(-96, -680)
    for k, px in enumerate((-96, -66, -40, -14, 14, 40, 66, 96)):
        ctx.line_to(px, -730 if k % 2 == 0 else -790)
    ctx.line_to(96, -680)
    ctx.close_path()
    rgba(ctx, c, a)
    ctx.fill()
    limb(ctx, [(170, -460), (260, -330), (300, -520)], c, 60)
    line(ctx, [(300, -500), (320, -820)], c, 34, a)
    circle(ctx, 324, -880, 80, c, a)                            # gada head
    for side in (-1, 1):
        circle(ctx, side * 34, -610, 11, hexc("#FF4A2A"), a * (0.8 + 0.2 * math.sin(t * 7)))
    ctx.restore()


def bez(p0, p1, p2, p3, u):
    v = 1 - u
    x = v ** 3 * p0[0] + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u ** 3 * p3[0]
    y = v ** 3 * p0[1] + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u ** 3 * p3[1]
    return x, y


def edge_glow(ctx, t, d, start=0.0, end=0.0, c=(1, 0.9, 0.6)):
    if start and t < start:
        glow(ctx, W / 2, H * 0.4, 1300, c, 0.85 * (1 - t / start))
    if end and t > d - end:
        glow(ctx, W / 2, H * 0.4, 1300, c, 0.85 * (t - (d - end)) / end)


def shake_at(ctx, t, hits, amp=12):
    for h in hits:
        u = t - h
        if 0 <= u < 0.4:
            ctx.translate(amp * (1 - u / 0.4) * math.sin(u * 90), amp * 0.6 * (1 - u / 0.4) * math.cos(u * 70))


def sparkle_burst(ctx, x, y, u, c=GOLD_HI, n=14, r=160):
    if not 0 <= u <= 1:
        return
    glow(ctx, x, y, r * (0.5 + u), c, 0.8 * (1 - u))
    for i in range(n):
        ang = i / n * math.tau + 0.3
        rr = r * (0.3 + u)
        circle(ctx, x + rr * math.cos(ang), y + rr * math.sin(ang), 6 * (1 - u) + 2, c, 1 - u)


# =============================================================================
# Eklavya: Nishada youth of the forest. Earthy skin, hair in a top-knot with a red cloth band (NO crown, no
# peacock feather), deer-hide dhoti, bead necklace, plain bamboo bow and a quiver of ordinary arrows.
# Faces right (towards Drona / Krishna) when not flipped.
# =============================================================================
def _ek_head(ctx, t, mood, look):
    skin = EK_SKIN
    rrect(ctx, -30, -600, 60, 66, 14)                         # neck
    ink(ctx, skin)
    for side in (-1, 1):                                       # ears + wooden ear rings
        ell(ctx, side * 94, -684, 17, 26)
        ink(ctx, skin)
        ctx.arc(side * 98, -648, 13, 0, math.tau)
        rgba(ctx, hexc("#6A3A18"))
        ctx.set_line_width(6)
        ctx.stroke()
    ell(ctx, 0, -688, 94, 102)
    ink(ctx, skin)
    sheen(ctx, -34, -736, 36, 20, 0.14)
    calm = mood in ("calm", "offer")
    hurt = mood == "hurt"
    for side in (-1, 1):
        eye(ctx, side * 36, -696, 22, 25, t, look=look, closed=calm, seed=5, iris=hexc("#2A160A"), skin=skin)
        if calm:
            line(ctx, [(side * 14, -734), (side * 36, -740), (side * 58, -734)], EK_HAIR, 8)
        elif hurt:
            line(ctx, [(side * 12, -744), (side * 36, -734), (side * 60, -728)], EK_HAIR, 9)
        else:                                                  # focused archer
            line(ctx, [(side * 12, -728), (side * 38, -740), (side * 62, -742)], EK_HAIR, 10)
    ell(ctx, 0, -664, 11, 16)
    ink(ctx, shade(skin, 0.88), 3.5)
    if calm:
        line(ctx, [(-22, -622), (0, -612), (22, -622)], hexc("#4A1A12"), 5)          # serene smile
    elif hurt:
        ell(ctx, 0, -618, 14, 10)
        ink(ctx, hexc("#4A1A12"), 3)
    else:
        line(ctx, [(-16, -618), (16, -618)], hexc("#4A1A12"), 5)
    for k in (-1, 0, 1):                                       # three ash lines (forest devotee), no royal tilak
        line(ctx, [(-28, -770 + 9 * k), (28, -770 + 9 * k)], hexc("#EDE4D2"), 4, 0.85)
    for k in range(9):                                         # hair line
        circle(ctx, -82 + 20.5 * k, -768 - 8 * math.sin(k / 8 * math.pi), 15, EK_HAIR)
    ell(ctx, 0, -812, 74, 38)                                  # hair mass
    ink(ctx, EK_HAIR, 3)
    circle(ctx, 0, -872, 40, EK_HAIR)                          # top-knot
    ctx.arc(0, -872, 40, 0, math.tau)
    rgba(ctx, dv.OUTLINE)
    ctx.set_line_width(4)
    ctx.stroke()
    rrect(ctx, -92, -794, 184, 22, 8)                          # red cloth band
    ink(ctx, BAND, 3)
    smooth(ctx, [(-86, -786), (-130, -770), (-150, -720), (-120, -740), (-96, -772)])   # band tail
    ink(ctx, BAND, 3)


def _ek_quiver(ctx, t):
    ctx.save()
    ctx.translate(-80, -560)
    ctx.rotate(-0.4)
    for k in range(4):
        ax = -18 + 12 * k
        line(ctx, [(ax, -140), (ax, -220)], dv.OUTLINE, 8)
        line(ctx, [(ax, -140), (ax, -220)], hexc("#E8D2A0"), 4)
        smooth(ctx, [(ax, -220), (ax - 9, -250), (ax + 9, -250)])
        ink(ctx, BAND, 2)
    rrect(ctx, -34, -160, 68, 300, 20)
    ink(ctx, HIDE_DK)
    for yy in (-130, 100):
        line(ctx, [(-34, yy), (34, yy)], hexc("#3A2210"), 6)
    ctx.restore()


def _ek_torso(ctx, t):
    skin = EK_SKIN
    smooth(ctx, [(-138, -520), (-74, -546), (74, -546), (138, -520), (142, -440), (110, -352), (-110, -352),
                 (-142, -440)])
    ink(ctx, skin)
    line(ctx, [(-40, -470), (-10, -420)], shade(skin, 0.85), 4)            # chest shading
    line(ctx, [(40, -470), (10, -420)], shade(skin, 0.85), 4)
    line(ctx, [(-120, -530), (110, -360)], HIDE_DK, 14)                    # quiver strap
    for k in range(11):                                                     # seed-bead necklace with a claw
        ang = math.pi * (0.15 + 0.7 * k / 10)
        circle(ctx, 70 * math.cos(ang), -540 + 50 * math.sin(ang), 8, hexc("#C8A060") if k % 2 else hexc("#7A2A1A"))
    smooth(ctx, [(-8, -484), (8, -484), (0, -456)])
    ink(ctx, hexc("#F3E8D0"), 2)
    rrect(ctx, -118, -374, 236, 30, 10)                                    # rope belt
    ink(ctx, hexc("#6A4A26"), 3)


def _ek_dhoti(ctx):
    pts = [(-136, -352), (136, -352), (146, -240), (120, -168), (90, -186), (60, -160), (24, -184), (-12, -158),
           (-48, -184), (-84, -160), (-120, -170), (-146, -240)]
    smooth(ctx, pts, k=0.08)
    ink(ctx, HIDE)
    for i in range(9):                                                      # deer-hide spots
        circle(ctx, -100 + 25 * i, -300 + 40 * math.sin(i * 1.7), 8, HIDE_DK, 0.7)


def _ek_legs(ctx, skin):
    for side in (-1, 1):
        limb(ctx, [(side * 56, -330), (side * 62, -170), (side * 60, -34)], skin, 48)
        ell(ctx, side * 68, -14, 44, 17)
        ink(ctx, skin)
        line(ctx, [(side * 60 - 24, -44), (side * 60 + 24, -44)], hexc("#6A4A26"), 6)   # string anklet


def _ek_arm(ctx, sh, el, hd, skin):
    limb(ctx, [sh, el], skin, 52)
    limb(ctx, [el, hd], skin, 44)
    wx, wy = lerp(el[0], hd[0], 0.8), lerp(el[1], hd[1], 0.8)
    line(ctx, [(wx - 18, wy - 4), (wx + 18, wy + 4)], hexc("#6A4A26"), 7)               # leather wrist band


def eklavya(ctx, x, y, s, t, pose="stand", mood="focus", look=(0.5, 0.0), draw_amt=1.0, rot=0.0, flip=False,
            a=1.0, glow_hand=0.0):
    """pose: stand (bow at side) | aim (string drawn, arrow nocked) | shot (release follow-through)
    | offer (kneeling, both palms held out with the guru dakshina glow) | hit (thrown back, bow flying).
    rot rotates the whole figure about the feet (a fall backwards = negative rot)."""
    def draw():
        place(ctx, x, y, s, t, flip)
        if rot:
            ctx.rotate(rot)
        skin = EK_SKIN
        if pose == "offer":
            _ek_offer(ctx, t, glow_hand)
            ctx.restore()
            return
        _ek_quiver(ctx, t)
        _ek_legs(ctx, skin)
        _ek_dhoti(ctx)
        _ek_torso(ctx, t)
        L, R = (-138, -515), (138, -515)
        if pose == "aim":
            hx = lerp(300, 60, ease_in_out(draw_amt))
            arms = [(L, (-60, -575), (hx, -562)), (R, (250, -548), (340, -556))]
        elif pose == "shot":
            arms = [(L, (-190, -600), (-250, -690)), (R, (250, -548), (340, -556))]
        elif pose == "hit":
            arms = [(L, (-210, -620), (-260, -760)), (R, (210, -640), (250, -790))]
        else:
            arms = [(L, (-196, -420), (-206, -330)), (R, (196, -430), (180, -340))]
        if pose == "stand":
            dv.bow(ctx, 196, -760, 40, 64)
        for sh, el, hd in arms:
            _ek_arm(ctx, sh, el, hd, skin)
            hand(ctx, *hd, skin, 26)
        if pose == "aim":
            hx = arms[0][2][0]
            dv.bow(ctx, 340, -800, -310, 64, hx, -562)
            plain_arrow(ctx, 430, -562, 0.0, 430 - hx + 20)
        elif pose == "shot":
            dv.bow(ctx, 340, -800, -310, 64)
        elif pose == "hit":                                                  # bow knocked out of the hand
            ctx.save()
            ctx.translate(330, -900)
            ctx.rotate(0.9 + t * 3)
            dv.bow(ctx, 0, -230, 230, 54)
            ctx.restore()
        _ek_head(ctx, t, "hurt" if pose == "hit" else mood, look)
        ctx.restore()
    group(ctx, a, draw)


def _ek_offer(ctx, t, glow_hand):
    """Kneeling: right knee down (shin flat behind), left foot forward, both palms held out and up."""
    skin = EK_SKIN
    dv.bow(ctx, -230, -240, -20, 30)                                        # bow laid on the ground behind
    limb(ctx, [(-20, -40), (-200, -30)], skin, 46)                          # back shin on the ground
    ell(ctx, -222, -20, 40, 16)
    ink(ctx, skin)
    limb(ctx, [(30, -200), (120, -200), (124, -40)], skin, 50)              # front thigh + shin (knee up)
    ell(ctx, 140, -16, 44, 17)
    ink(ctx, skin)
    ctx.save()
    ctx.translate(0, 170)                                                    # upper body lowered by the kneel
    _ek_quiver(ctx, t)
    smooth(ctx, [(-130, -352), (130, -352), (150, -250), (90, -190), (-40, -200), (-150, -250)], k=0.1)
    ink(ctx, HIDE)
    for i in range(6):
        circle(ctx, -90 + 34 * i, -290 + 20 * math.sin(i * 1.7), 8, HIDE_DK, 0.7)
    _ek_torso(ctx, t)
    arms = [((-138, -515), (60, -470), (230, -500)), ((138, -515), (200, -455), (250, -470))]
    for sh, el, hd in arms:
        _ek_arm(ctx, sh, el, hd, skin)
    ell(ctx, 250, -490, 46, 26)                                             # cupped palms
    ink(ctx, skin)
    if glow_hand > 0:
        glow(ctx, 250, -520, 120, GOLD_HI, 0.85 * glow_hand)
        circle(ctx, 250, -520, 16, hexc("#FFF6D0"), glow_hand)
    _ek_head(ctx, t, "offer", (0.4, 0.2))
    ctx.restore()


# =============================================================================
# Shri Krishna with the Sudarshan raised (dv.krishna "bless" pose + chakra above the raised hand)
# =============================================================================
def chakra_pos(x, s, flip=True):
    """Where the chakra spins: just above Krishna's raised (bless) hand."""
    return x + (-175 if flip else 175) * s, FEET - 720 * s


def krishna_chakra(ctx, x, y, s, t, chakra=1.0, flip=True, a=1.0):
    dv.krishna(ctx, x, y, s, t, pose="bless", flip=flip, a=a)
    cx, cy = chakra_pos(x, s, flip)
    sudarshan(ctx, cx, cy, 46, t, a=chakra * a)


# =============================================================================
# Story: 7 scenes, 112 spoken words. Simple Hindi, no commas or pause signs (user's voice rule); every line ends
# with a purnaviram. Loop: "...इसीलिए" -> "जिस एकलव्य ने गुरु को अपना अंगूठा दे दिया...".
# =============================================================================
SPEC = [
    {"key": "hook", "text": "", "visual": "Eklavya kneels and offers the glowing dakshina to Drona; cut: Krishna "
                                          "raises the Sudarshan and Eklavya falls back in a burst of light",
     "vo": [("punch", [("जिस एकलव्य ने", "JIS EKLAVYA NE"), ("गुरु को अपना अंगूठा दे दिया।", "GURU KO APNA ANGOOTHA DE DIYA.")], 0.02),
            ("low", [("उसे बाद में", "USE BAAD MEIN"), ("खुद श्री कृष्ण ने मारा था।", "KHUD SHRI KRISHNA NE MAARA THA.")], 0.04)]},
    {"key": "jungle", "text": "", "visual": "Forest dawn: clay image of Drona; Eklavya shoots arrow after arrow into a "
                                            "target; Arjun steps in, shocked",
     "vo": [("tell", [("जंगल में एकलव्य ने", "JUNGLE MEIN EKLAVYA NE"), ("द्रोण की मिट्टी की मूर्ति बनाई।", "DRONA KI MITTI KI MOORTI BANAI.")], 0.02),
            ("build", [("और अकेले ही", "AUR AKELE HI"), ("अर्जुन से आगे निकल गया।", "ARJUN SE AAGE NIKAL GAYA.")], 0.04)]},
    {"key": "dakshina", "text": "", "visual": "Drona points and demands; Eklavya kneels and holds out his palms; a "
                                              "golden glow rises from them; petals",
     "vo": [("low", [("तब द्रोण ने दक्षिणा में", "TAB DRONA NE DAKSHINA MEIN"), ("उसका अंगूठा माँग लिया।", "USKA ANGOOTHA MAANG LIYA.")], 0.02),
            ("awe", [("और एकलव्य ने", "AUR EKLAVYA NE"), ("बिना सोचे अंगूठा दे दिया।", "BINA SOCHE ANGOOTHA DE DIYA.")], 0.04)]},
    {"key": "jarasandh", "text": "", "visual": "Red war camp: Jarasandh's giant shadow rises; Eklavya, older, walks in "
                                               "with his bow; the army behind him; Krishna appears glowing on the right",
     "vo": [("whisper", [("पर कहानी यहाँ", "PAR KAHANI YAHAN"), ("खत्म नहीं होती।", "KHATAM NAHIN HOTI.")], 0.02),
            ("build", [("बिना अंगूठे के भी", "BINA ANGOOTHE KE BHI"), ("एकलव्य बड़ा योद्धा बना।", "EKLAVYA BADA YODDHA BANA.")], 0.02),
            ("fast", [("और जरासंध की सेना में", "AUR JARASANDH KI SENA MEIN"), ("कृष्ण के सामने आ खड़ा हुआ।", "KRISHNA KE SAAMNE AA KHADA HUA.")], 0.04)]},
    {"key": "vadh", "text": "", "visual": "Eklavya fires at Krishna, the arrow burns up in the aura; Krishna sends the "
                                          "Sudarshan; flash; Eklavya is thrown back and fades into light",
     "vo": [("punch", [("और वहीं", "AUR WAHIN"), ("कृष्ण के हाथों मारा गया।", "KRISHNA KE HAATHON MAARA GAYA.")], 0.04)]},
    {"key": "raaz", "text": "", "visual": "Night Kurukshetra camp fires: Krishna explains, Arjun listens shocked",
     "vo": [("low", [("कुरुक्षेत्र में कृष्ण ने", "KURUKSHETRA MEIN KRISHNA NE"), ("खुद अर्जुन को ये राज़ बताया।", "KHUD ARJUN KO YE RAAZ BATAYA.")], 0.04)]},
    {"key": "payoff", "text": "", "visual": "Eklavya's golden shadow rises among the Kaurava army drawing his bow; the "
                                            "sky fills with arrows; Krishna and Arjun look up; cross-fade to the hook",
     "vo": [("low", [("अगर एकलव्य जिंदा होता", "AGAR EKLAVYA ZINDA HOTA"), ("तो कौरवों की तरफ से लड़ता।", "TO KAURAVON KI TARAF SE LADTA.")], 0.02),
            ("punch", [("और उसे देवता भी", "AUR USE DEVTA BHI"), ("नहीं हरा पाते।", "NAHIN HARA PAATE.")], 0.02),
            ("whisper", [("इसीलिए", "ISILIYE")], 0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "EKLAVYA": hexc("#FFB347"), "ANGOOTHA": GOLD_HI, "KRISHNA": hexc("#7FB2FF"), "MAARA": hexc("#FF5A5A"),
    "DRONA": hexc("#FFD08A"), "MITTI": hexc("#D8A060"), "ARJUN": hexc("#FFE38A"), "AAGE": hexc("#9BE07A"),
    "DAKSHINA": GOLD_HI, "MAANG": hexc("#FF8A5A"), "BINA": hexc("#9AD8FF"), "KAHANI": GOLD_HI,
    "YODDHA": hexc("#FFB347"), "JARASANDH": hexc("#FF5A5A"), "SAAMNE": hexc("#FF8A5A"), "HAATHON": hexc("#7FB2FF"),
    "RAAZ": GOLD_HI, "ZINDA": hexc("#9BE07A"), "KAURAVON": hexc("#FF5A5A"), "DEVTA": GOLD_HI, "ISILIYE": GOLD_HI,
})


# =============================================================================
# Scenes
# =============================================================================
class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"diya": c("GURU KO", d * 0.2) + 0.5, "cut": c("USE BAAD", d * 0.45),
                "maara": c("KHUD SHRI", d * 0.7) + 0.6}

    def events(self, d):
        b = self.beats(d)
        return [(b["diya"], "shimmer"), (b["cut"], "whoosh"), (b["maara"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        if t < b["cut"]:                                     # the famous half: the thumb offered to the guru
            forest_bg(ctx, t)
            dv.petals(ctx, t, n=20, seed=3, a=0.7)
            drona(ctx, 800, FEET, 0.74, t, pose="command" if t < b["diya"] else "stand", flip=True)
            eklavya(ctx, 300, FEET, 0.74, t, pose="offer", glow_hand=clamp((t - b["diya"]) / 0.4))
            sparkle_burst(ctx, 300 + 250 * 0.74, FEET - 350 * 0.74, (t - b["diya"]) / 0.8)
            edge_glow(ctx, t, d, start=0.25)
            return
        u = t - b["cut"]
        shake_at(ctx, t, [b["maara"]], amp=16)
        war_camp_bg(ctx, t)
        fall = ease_in(clamp((t - b["maara"]) / 0.55))
        fly = clamp((t - b["cut"] - 0.2) / max(0.2, b["maara"] - b["cut"] - 0.2))
        krishna_chakra(ctx, 800, FEET, 0.74, t, chakra=1.0 if fly <= 0 else 0.0)
        cx, cy = bez(chakra_pos(800, 0.74), (650, 380), (450, 420), (420, FEET - 520), ease_in_out(fly))
        if 0 < fly < 1:
            sudarshan(ctx, cx, cy, 46, t)
        eklavya(ctx, 420, FEET, 0.74, t, pose="hit" if t >= b["maara"] else "aim", rot=-0.5 * fall,
                a=1.0 - 0.6 * clamp((t - b["maara"] - 0.6) / 0.6))
        sparkle_burst(ctx, 420, FEET - 500, (t - b["maara"]) / 0.7, c=CHAKRA_GOLD, r=220)
        flash(ctx, u, dur=0.3)
        flash(ctx, t - b["maara"], c=(1, 0.9, 0.5), dur=0.4)


class Jungle(Cued):
    def beats(self, d):
        c = self.cue
        return {"aur": c("AUR AKELE", d * 0.5), "arjun": c("ARJUN SE", d * 0.72)}

    def events(self, d):
        b = self.beats(d)
        shots = [b["aur"] + 0.1 + 0.45 * k for k in range(3)]
        return [(0.1, "soft_thud")] + [(s_, "arrow") for s_ in shots] + [(b["arjun"] + 0.2, "pop")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        forest_bg(ctx, t)
        shots = [b["aur"] + 0.1 + 0.45 * k for k in range(3)]
        hits = sum(1 for s_ in shots if t >= s_ + 0.3)
        target_tree(ctx, 930, t, hits)
        rise = ease_out_back(clamp(t / 0.8))
        clay_drona(ctx, 120, FEET - 30, 0.46, t, a=rise)
        if t < b["aur"]:
            pose, amt = "aim", clamp(t / max(0.5, b["aur"] - 0.2))
        else:
            last = max([s_ for s_ in shots if s_ <= t], default=None)
            pose = "shot" if last is not None and t - last < 0.25 else "aim"
            amt = 1.0 if last is None else clamp((t - last - 0.25) / 0.2)
        eklavya(ctx, 340, FEET, 0.72, t, pose=pose, draw_amt=amt)
        for s_ in shots:                                     # arrows in flight: true angle, head to the target
            u = (t - s_) / 0.3
            if 0 <= u < 1:
                sx, sy = 340 + 430 * 0.72, FEET - 562 * 0.72
                ex, ey = 924, 800
                ax, ay = lerp(sx, ex, u), lerp(sy, ey, u)
                plain_arrow(ctx, ax, ay, math.atan2(ey - sy, ex - sx), 110)
        if t >= b["arjun"]:                                  # Arjun steps in from the right, shocked
            k = ease_out_cubic(clamp((t - b["arjun"]) / 0.5))
            arjuna(ctx, lerp(1180, 790, k), FEET + 6, 0.68, t, pose="shock", flip=True)


class Dakshina(Cued):
    def beats(self, d):
        c = self.cue
        return {"maang": c("USKA ANGOOTHA", d * 0.3), "diya": c("BINA SOCHE", d * 0.75) + 0.4}

    def events(self, d):
        b = self.beats(d)
        return [(b["maang"], "thud"), (b["diya"], "shimmer"), (b["diya"] + 0.1, "ghanti")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        forest_bg(ctx, t, warm=0.7)
        clay_drona(ctx, 1000, FEET - 20, 0.40, t, a=0.8)
        arjuna(ctx, 900, FEET - 40, 0.62, t, pose="namaste", flip=True)
        drona(ctx, 720, FEET, 0.76, t, pose="command" if t >= b["maang"] - 0.2 else "stand", flip=True)
        g = clamp((t - b["diya"]) / 0.5)
        eklavya(ctx, 250, FEET, 0.76, t, pose="offer", glow_hand=g)
        if g > 0:
            dv.petals(ctx, t, n=30, seed=8, a=g)
            sparkle_burst(ctx, 250 + 250 * 0.76, FEET - 350 * 0.76, (t - b["diya"]) / 0.9)


class Jarasandh(Cued):
    def beats(self, d):
        c = self.cue
        return {"yoddha": c("BINA ANGOOTHE", d * 0.3), "sena": c("AUR JARASANDH", d * 0.6),
                "saamne": c("KRISHNA KE SAAMNE", d * 0.8)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "soft_thud"), (b["yoddha"], "whoosh"), (b["sena"], "boom"), (b["saamne"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        war_camp_bg(ctx, t)
        rise = ease_out_cubic(clamp((t - b["sena"]) / 0.7))
        jarasandh_shadow(ctx, 150, lerp(1100, 1000, rise), 0.62, t, a=rise)
        kaurava_mob(ctx, 260, 700, FEET - 70, 5, t, mode="stand", s=0.40, a=0.4 + 0.6 * rise)
        walk = ease_in_out(clamp(t / max(0.6, b["sena"])))
        pose = "stand" if t < b["yoddha"] else ("aim" if t >= b["saamne"] else "stand")
        eklavya(ctx, lerp(120, 360, walk), FEET, 0.76, t, pose=pose,
                draw_amt=clamp((t - b["saamne"]) / 0.5), look=(0.6, 0.0))
        if t >= b["saamne"] - 0.1:
            k = ease_out_back(clamp((t - b["saamne"] + 0.1) / 0.5))
            dv.halo(ctx, 820, FEET - 560, 150 * k, t, a=k)
            dv.krishna(ctx, 820, FEET, lerp(0.62, 0.74, k), t, pose="bless", flip=True, a=k)


class Vadh(Cued):
    def beats(self, d):
        c = self.cue
        rel = 0.35
        return {"rel": rel, "burn": rel + 0.55, "send": c("KRISHNA KE", d * 0.4), "hit": c("MAARA", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(b["rel"], "arrow"), (b["burn"], "zap"), (b["send"], "whoosh"), (b["hit"], "boom"),
                (b["hit"] + 0.1, "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        shake_at(ctx, t, [b["hit"]], amp=18)
        war_camp_bg(ctx, t)
        dust = clamp((t - b["hit"]) / 1.2)
        fly = clamp((t - b["send"]) / max(0.2, b["hit"] - b["send"]))
        krishna_chakra(ctx, 820, FEET, 0.76, t, chakra=1.0 if t < b["send"] else 0.0)
        sx, sy = 240 + 430 * 0.76, FEET - 562 * 0.76
        if b["rel"] <= t < b["burn"]:                        # Eklavya's arrow flies at Krishna and burns up
            u = (t - b["rel"]) / (b["burn"] - b["rel"])
            ex, ey = 700, FEET - 560
            plain_arrow(ctx, lerp(sx, ex, u), lerp(sy, ey, u), math.atan2(ey - sy, ex - sx), 120)
        sparkle_burst(ctx, 700, FEET - 560, (t - b["burn"]) / 0.5, c=CHAKRA_GOLD, r=90)
        hx, hy = chakra_pos(820, 0.76)
        cx, cy = lerp(hx, 380, ease_in(fly)), lerp(hy, FEET - 480, ease_in(fly))
        if 0 < fly < 1:
            for k in range(6):                               # chakra trail
                circle(ctx, lerp(cx, hx, k * 0.06), lerp(cy, hy, k * 0.06), 30 - 4 * k, CHAKRA_GOLD, 0.4 - k * 0.06)
            sudarshan(ctx, cx, cy, 46, t)
        if t < b["hit"]:
            pose = "aim" if t < b["rel"] else "shot"
            eklavya(ctx, 240, FEET, 0.76, t, pose=pose, draw_amt=clamp(t / 0.3))
        else:
            fall = ease_in(clamp((t - b["hit"]) / 0.6))
            fade = clamp((t - b["hit"] - 0.7) / 0.9)
            eklavya(ctx, 420 - 20 * fall, FEET, 0.76, t, pose="hit", rot=-0.4 * fall, a=1 - 0.85 * fade)
            for i in range(14):                              # rising light motes as he fades
                yy = FEET - 200 - 500 * ((fade + rnd(i, 3)) % 1)
                circle(ctx, 280 + 160 * rnd(i, 4), yy, 5, GOLD_HI, 0.8 * fade)
            dust_cloud(ctx, 320, FEET, dust, 240, seed=4, a=1 - dust)
        sparkle_burst(ctx, 360, FEET - 480, (t - b["hit"]) / 0.6, c=CHAKRA_GOLD, r=240)


class Raaz(Cued):
    def beats(self, d):
        c = self.cue
        return {"raaz": c("KHUD ARJUN", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "tick"), (b["raaz"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_kurukshetra(ctx, t, fires=1.0)
        lean = ease_out_cubic(clamp((t - b["raaz"]) / 0.4))
        dv.krishna(ctx, 270, FEET, 0.76, t, pose="ask" if t >= b["raaz"] - 0.3 else "bless", look=(0.5, 0.0))
        arjuna(ctx, lerp(820, 790, lean), FEET, 0.74, t, pose="shock" if t >= b["raaz"] else "namaste", flip=True)
        if t >= b["raaz"]:
            glow(ctx, 540, FEET - 520, 260, GOLD_HI, 0.25 * lean)


class Payoff(Cued):
    def beats(self, d):
        c = self.cue
        return {"zinda": c("AGAR EKLAVYA", 0.1) + 0.3, "devta": c("AUR USE", d * 0.55),
                "isiliye": c("ISILIYE", d * 0.88)}

    def events(self, d):
        b = self.beats(d)
        return [(b["zinda"], "shimmer"), (b["devta"], "boom"), (b["devta"] + 0.5, "arrow"), (b["isiliye"], "whoosh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_kurukshetra(ctx, t, fires=0.6, lightning=clamp(1 - abs(t - b["devta"]) / 0.25))
        kaurava_mob(ctx, 300, 1060, FEET - 120, 7, t, mode="stand", s=0.40)
        rise = ease_out_back(clamp((t - b["zinda"]) / 0.8))
        if rise > 0:                                         # the "what if": a giant golden Eklavya with the Kauravas
            glow(ctx, 760, FEET - 520, 420, GOLD_HI, 0.35 * rise)
            dv.silhouette(ctx, lambda: eklavya(ctx, 700, FEET - 60, 0.66 + 0.10 * rise, t, pose="aim",
                                                draw_amt=clamp((t - b["devta"] + 0.4) / 0.4)),
                          c=hexc("#FFD27A"), a=0.75 * rise)
        if t >= b["devta"]:                                  # a sky full of arrows: no one could stop him
            for i in range(18):
                u = ((t - b["devta"]) * 1.4 + rnd(i, 5)) % 1
                ax, ay = lerp(760 - 60 * rnd(i, 6), -60, u), lerp(620 - 200 * rnd(i, 7), 200 + 500 * rnd(i, 8), u)
                ang = math.atan2((200 + 500 * rnd(i, 8)) - (620 - 200 * rnd(i, 7)), -60 - (760 - 60 * rnd(i, 6)))
                plain_arrow(ctx, ax, ay, ang, 90, a=0.85)
        dv.krishna(ctx, 165, FEET, 0.70, t, pose="ask", look=(0.6, -0.4))
        arjuna(ctx, 440, FEET + 10, 0.66, t, pose="shock", flip=True)
        x = clamp((t - (d - 0.45)) / 0.45)                   # loop: cross-fade into the hook's first frame
        if x > 0:
            ctx.push_group()
            Hook().draw(ctx, 0.0, d)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(x)


SCENE_CLASSES = {"hook": Hook, "jungle": Jungle, "dakshina": Dakshina, "jarasandh": Jarasandh, "vadh": Vadh,
                 "raaz": Raaz, "payoff": Payoff}

UPLOAD = {
    "titles": [
        "Eklavya Ko Kisne Maara? Mahabharat Ka Chhupa Sach #shorts",
        "Eklavya Ko Krishna Ne Kyun Maara? Drona Parva Raaz #shorts",
        "Angootha Dene Ke Baad Eklavya Ka Kya Hua? #shorts",
    ],
    "thumb_text": "ANGOOTHE KE BAAD",
    "queries": [
        "eklavya ko kisne maara",
        "krishna ne eklavya ko kyun maara",
        "eklavya angootha ke baad kya hua",
    ],
    "description": """
Eklavya ko kisne maara? Angootha dene ke baad Eklavya ka kya hua - Mahabharat ka ye sach bahut kam log jaante hain.
Jungle mein Eklavya ne Drona ki mitti ki moorti banakar dhanush seekha aur Arjun se aage nikal gaya. Guru dakshina mein
Drona ne angootha maanga aur Eklavya ne bina soche de diya. Par kahani yahan khatam nahi hoti.

Bina angoothe ke bhi Eklavya bada yoddha bana aur Jarasandh ki taraf se Krishna ke saamne aaya. Kurukshetra mein
Ghatotkach ke girne ke baad Shri Krishna ne khud Arjun ko bataya ki Jarasandh, Shishupal aur Eklavya Pandavon ke
hit ke liye maare gaye - agar wo zinda hote to Duryodhan ki taraf se ladte.

Ek taraf: Krishna ne dharm ki jeet ke liye aage ka khatra pehle hi rok diya.
Doosri taraf: Eklavya ne guru ke liye sab kuch de diya tha - kya uske saath nyay hua?
Aap kya sochte ho? Comment mein likho.

Source: Mahabharat, Adi Parva (Eklavya aur Drona); Drona Parva (Krishna ka Arjun ko batana, KMG section 181).
Harivamsha mein Eklavya Jarasandh ki taraf se Yadavon se lada (kuch granthon mein vivran alag hai).
""",
    "tags": [
        "eklavya", "eklavya ko kisne maara", "krishna eklavya", "eklavya angootha", "mahabharat", "drona parva",
        "dronacharya eklavya", "shri krishna", "jarasandh", "mahabharat ke rahasya", "divya rahasya", "sanatan katha",
        "shorts", "mahabharat katha",
    ],
    "hashtags": ["#Shorts", "#Mahabharat", "#Krishna"],
    "pinned_comment": "Kya Shri Krishna ka Eklavya ko maarna dharm tha? Haan ya Nahi - apna jawab likho 👇",
}


def thumbnail(ctx):
    war_camp_bg(ctx, 0.4)
    krishna_chakra(ctx, 800, FEET, 0.76, 0.5, chakra=1.0)
    eklavya(ctx, 270, FEET, 0.76, 0.5, pose="aim", draw_amt=1.0)
    text(ctx, "ANGOOTHE KE BAAD", 540, 1330, 112, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
         stroke_w=18)
    text(ctx, "KRISHNA NE MAARA?", 540, 1470, 104, hexc("#FF6A3A"), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
         stroke_w=18)
