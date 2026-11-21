"""Ghatotkach Akshauhini: marte marte bhi poori sena kuchal di (~32s loop katha, 7 scenes).

Angle (new, not the "Krishna kyun naache" Short): the 14th-night battle of Kurukshetra. Ghatotkach grows sky-high
and rains fire, the Kaurava army breaks, Duryodhan screams at Karna to use Indra's Vasavi Shakti, Karna spends the
weapon he saved for Arjun - and the dying Ghatotkach grows mountain-sized and falls ON the Kaurava army.
The last words "...AUR" run straight into the opening line "MARTE MARTE BHI..." (seamless loop).
"""

import math

import cairo

from core.katha import *  # noqa: F401,F403
import core.devta as dv
from core.devta import ell, gem, hand, ink, limb, sheen, smooth, eye, palm

TOPIC = "GHATOTKACH AKSHAUHINI KUCHAL"
OUTPUTS = {"edge": "ghatotkach_akshauhini_short.mp4", "files": "ghatotkach_akshauhini_short.mp4"}
MUSIC_STYLE = "march"      # war-drum bed: "takadta bhadakta" energy, no shankh
MUSIC_BPM = 90
MUSIC_VOLUME = 0.12
TAIL_PAD = 0.04
MAX_GAP = 0.04
KIKI_PAUSE_MS = 200

FIRE_O = hexc("#FF6A1A")
FIRE_Y = hexc("#FFD24A")
EMBER = hexc("#FF8A3D")
BLOOD_MOON = hexc("#FF7246")
VASAVI = hexc("#FFF1A8")
GH_SKIN = hexc("#3D6F8E")
GH_HAIR = hexc("#1B0F1A")
BRONZE = hexc("#9A5A22")
KAURAV_RED = hexc("#8C1C2C")
DUR_SKIN = hexc("#D29A68")
DUR_ARMOR = hexc("#5A1B4F")

SOURCES = [
    "Mahabharata, Drona Parva (Ghatotkacha-vadha Parva, KM Ganguli trans. sections 173-179): in the night battle "
    "Ghatotkacha's maya grows, he rains weapons and rocks, the Kauravas break and urge Karna to use Indra's "
    "one-time Shakti (saved for Arjuna); Karna hurls it and Ghatotkacha is slain.",
    "Same section: as he fell, Ghatotkacha assumed a gigantic form and crushed with his body a full akshauhini of "
    "the Kaurava army (some retellings say 'a large part of the army' - noted in the description).",
]

SPEC = [
    {"key": "hook", "text": "MARTE MARTE BHI",
     "visual": "Giant Ghatotkach crashes down on the tiny Kaurava army; dust storm, screen shake, debris flying",
     "vo": [("punch", [("मरते मरते भी,", "MARTE MARTE BHI,"),
                       ("घटोत्कच ने,", "GHATOTKACH NE,"),
                       ("कौरवों की पूरी एक", "KAURAVON KI POORI EK"),
                       ("अक्षौहिणी कुचल दी!", "AKSHAUHINI KUCHAL DI!")], 0.04)]},
    {"key": "raat", "text": "CHAUDAHVIN RAAT",
     "visual": "Blood-moon night falls; Bhim's rakshasa son Ghatotkach roars as a violet maya aura doubles his power",
     "vo": [("build", [("चौदहवें दिन की,", "CHAUDAHVEN DIN KI,"),
                       ("रात हो चुकी थी।", "RAAT HO CHUKI THI."),
                       ("और रात में,", "AUR RAAT MEIN,"),
                       ("भीम के राक्षस बेटे की ताकत,", "BHEEM KE RAKSHAS BETE KI TAAKAT,"),
                       ("दुगनी हो जाती थी।", "DUGNI HO JAATI THI.")], 0.04)]},
    {"key": "maya", "text": "AASMAAN TAK",
     "visual": "Ghatotkach grows sky-high with gada raised and hurls fireballs; the Kaurava ranks break and run",
     "vo": [("fast", [("वो आसमान तक बढ़ा,", "WO AASMAAN TAK BADHA,"),
                      ("और आग के गोले बरसाए।", "AUR AAG KE GOLE BARSAAYE."),
                      ("कौरव सेना,", "KAURAV SENA,"),
                      ("जान बचाकर भागी।", "JAAN BACHAKAR BHAAGI.")], 0.04)]},
    {"key": "bhagdad", "text": "DURYODHAN CHEEKHA",
     "visual": "Under falling fire Duryodhan, gada in hand, screams and points at Karna",
     "vo": [("fast", [("दुर्योधन चीखा,", "DURYODHAN CHEEKHA,"),
                      ("कर्ण, वो शक्ति चलाओ,", "KARNA, WO SHAKTI CHALAO,"),
                      ("वरना आज कोई नहीं बचेगा!", "VARNA AAJ KOI NAHI BACHEGA!")], 0.04)]},
    {"key": "vasavi", "text": "VASAVI SHAKTI",
     "visual": "Karna lifts the blazing Vasavi Shakti, lowers his eyes at 'Arjun', then hurls it into Ghatotkach",
     "vo": [("low", [("वो इंद्र की शक्ति,", "WO INDRA KI SHAKTI,"),
                     ("जो बस एक बार चलती थी,", "JO BAS EK BAAR CHALTI THI,"),
                     ("जो अर्जुन के लिए", "JO ARJUN KE LIYE"),
                     ("बचाकर रखी थी...", "BACHAKAR RAKHI THI..."),
                     ("कर्ण ने,", "KARNA NE,"),
                     ("घटोत्कच पर चला दी।", "GHATOTKACH PAR CHALA DI.")], 0.04)]},
    {"key": "gira", "text": "PAHAAD JAISA GIRA",
     "visual": "Struck, Ghatotkach grows mountain-sized and topples onto the Kaurava army - dust, shake, flash",
     "vo": [("punch", [("शक्ति छाती में लगी,", "SHAKTI CHHAATI MEIN LAGI,"),
                       ("तो घटोत्कच,", "TO GHATOTKACH,"),
                       ("पहाड़ जितना बड़ा हुआ,", "PAHAAD JITNA BADA HUA,"),
                       ("और सीधा कौरव सेना पर गिरा।", "AUR SEEDHA KAURAV SENA PAR GIRA.")], 0.04)]},
    {"key": "twist", "text": "KRISHNA MUSKURAYE",
     "visual": "Dawn-gold light: Shri Krishna smiles with Abhaya mudra beside a safe, bowing Arjun; the fallen hero glows "
               "behind them; the last beat cuts back to the falling giant (loop)",
     "vo": [("awe", [("उधर कृष्ण मुस्कुराए...", "UDHAR KRISHNA MUSKURAAYE..."),
                     ("क्योंकि घटोत्कच ने,", "KYUNKI GHATOTKACH NE,"),
                     ("अपनी जान देकर,", "APNI JAAN DEKAR,"),
                     ("अर्जुन को बचाया था... और", "ARJUN KO BACHAAYA THA... AUR")], 0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "GHATOTKACH": FIRE_Y, "AKSHAUHINI": hexc("#FF5555"), "KUCHAL": hexc("#FF5555"), "MARTE": FIRE_Y,
    "KAURAV": hexc("#FF8A80"), "KAURAVON": hexc("#FF8A80"), "RAAT": hexc("#B39DDB"), "AASMAAN": hexc("#82C4FF"),
    "AAG": FIRE_O, "GOLE": FIRE_O, "DURYODHAN": hexc("#CE93D8"),
    "KARNA": GOLD_HI, "SHAKTI": VASAVI, "ARJUN": hexc("#82C4FF"), "CHALA": FIRE_O, "PAHAAD": FIRE_Y,
    "GIRA.": hexc("#FF5555"), "CHHAATI": FIRE_O, "SEEDHA": FIRE_Y, "DUGNI": hexc("#B388FF"),
    "BHEEM": hexc("#82C4FF"), "INDRA": GOLD_HI, "EK": FIRE_Y, "KRISHNA": hexc("#82C4FF"),
    "MUSKURAAYE...": GOLD_HI, "BACHAAYA": GOLD_HI, "BHAAGI": hexc("#FF5555"), "BACHEGA!": hexc("#FF5555"),
})


def ease_in(u):
    u = clamp(u)
    return u * u


# ============================================================ scenery + effects

def night_kurukshetra(ctx, t, fires=1.0, lightning=0.0):
    """Blood-moon night over Kurukshetra: 4-stop sky, moon, clouds, 3 hill layers, camp fires, wreckage, embers."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in ((0.0, "#05030F"), (0.30, "#1B0A2E"), (0.48, "#4E1230"), (0.60, "#A23A1C"), (0.75, "#2A0C14"),
                  (1.0, "#12060A")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.paint()
    dv.stars(ctx, t, n=55, a=0.7)
    # blood moon
    glow(ctx, 790, 380, 330, BLOOD_MOON, 0.45)
    circle(ctx, 790, 380, 118, BLOOD_MOON)
    circle(ctx, 790, 380, 118, hexc("#FFB08A"), 0.25)
    for cx, cy, r in ((755, 350, 22), (820, 410, 16), (800, 335, 10), (770, 420, 12)):
        circle(ctx, cx, cy, r, hexc("#C94A2C"), 0.45)
    # drifting cloud bands
    for k in range(4):
        x = ((t * (18 + 6 * k) + k * 330) % (W + 700)) - 350
        y = 300 + k * 95
        ell(ctx, x, y, 260, 26)
        rgba(ctx, hexc("#2A0F2A"), 0.75)
        ctx.fill()
    if lightning > 0 and int(t * 7) % 4 == 0:
        rgba(ctx, hexc("#CFE8FF"), 0.18 * lightning)
        ctx.paint()
        dv.smooth(ctx, [(300, 0), (340, 160), (300, 250), (360, 420)], closed=False, k=0)
        rgba(ctx, hexc("#E8F4FF"), 0.8 * lightning)
        ctx.set_line_width(5)
        ctx.stroke()
    # three hill layers
    for k, (c, yy, amp) in enumerate((("#3A1530", 930, 55), ("#2A0F22", 1005, 40), ("#1A0A14", 1070, 26))):
        ctx.move_to(-80, yy)
        for x in range(-80, W + 81, 40):
            ctx.line_to(x, yy - amp * math.sin(x / (150 + 40 * k) + k * 2) - 14 * math.sin(x / 53 + k))
        ctx.line_to(W + 80, H)
        ctx.line_to(-80, H)
        ctx.close_path()
        rgba(ctx, hexc(c))
        ctx.fill()
    # camp fires on the far hills
    if fires > 0:
        for i, (fx, fy) in enumerate(((120, 985), (330, 1000), (610, 975), (880, 995), (1010, 985))):
            f = 1 + 0.25 * math.sin(t * 9 + i * 2)
            glow(ctx, fx, fy, 70 * f, FIRE_O, 0.45 * fires)
            glow(ctx, fx, fy, 26 * f, FIRE_Y, 0.8 * fires)
    # near ground with wreckage
    ctx.rectangle(-80, GROUND - 40, W + 160, H)
    rgba(ctx, hexc("#1A0C0E"))
    ctx.fill()
    ctx.arc(70, GROUND - 52, 58, 0, math.tau)          # broken chariot wheel
    rgba(ctx, hexc("#0E0608"))
    ctx.set_line_width(10)
    ctx.stroke()
    for k in range(6):
        a = k * math.pi / 6 + 0.3
        line(ctx, [(70, GROUND - 52), (70 + 58 * math.cos(a), GROUND - 52 + 58 * math.sin(a))], hexc("#0E0608"), 6)
    for i, bx in enumerate((470, 990)):                    # leaning torn banners
        line(ctx, [(bx, GROUND - 30), (bx + 30, GROUND - 230)], hexc("#0E0608"), 7)
        wave = 8 * math.sin(t * 4 + i)
        ctx.move_to(bx + 30, GROUND - 230)
        ctx.line_to(bx + 95 + wave, GROUND - 215)
        ctx.line_to(bx + 26, GROUND - 180)
        ctx.close_path()
        rgba(ctx, KAURAV_RED if i else SAFF, 0.55)
        ctx.fill()
    for i in range(14):                                    # arrows stuck in the ground
        ax = 40 + i * 76 + 20 * rnd(i, 3)
        line(ctx, [(ax, GROUND - 28), (ax + 14, GROUND - 78)], hexc("#2E1A12"), 4)
    # embers rising
    for i in range(34):
        x = (rnd(i, 21) * W + 30 * math.sin(t * 1.5 + i)) % W
        y = H - 500 - ((t * (60 + 50 * rnd(i, 22)) + rnd(i, 23) * 1100) % 1100)
        circle(ctx, x, y, 2 + 3 * rnd(i, 24), EMBER, 0.55 * (0.5 + 0.5 * math.sin(t * 5 + i)))


def fireball(ctx, x, y, ang, r, t, a=1.0):
    """Fireball whose head is at (x, y), flying along ang, trail behind."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    g = cairo.LinearGradient(-r * 6, 0, 0, 0)
    g.add_color_stop_rgba(0, *FIRE_O, 0)
    g.add_color_stop_rgba(1, *FIRE_O, 0.7 * a)
    ctx.move_to(0, -r)
    ctx.line_to(-r * 6, 0)
    ctx.line_to(0, r)
    ctx.close_path()
    ctx.set_source(g)
    ctx.fill()
    ctx.restore()
    f = 1 + 0.15 * math.sin(t * 30 + x)
    glow(ctx, x, y, r * 2.6 * f, FIRE_O, 0.7 * a)
    circle(ctx, x, y, r * f, FIRE_Y, a)
    circle(ctx, x, y, r * 0.5, (1, 0.98, 0.85), a)


def blast(ctx, x, y, u, r=90):
    """Impact burst, u 0..1."""
    if not 0 <= u <= 1:
        return
    k = ease_out_cubic(u)
    glow(ctx, x, y, r * (0.6 + 1.4 * k), FIRE_O, 0.8 * (1 - u))
    glow(ctx, x, y, r * 0.6 * (1 + k), FIRE_Y, 0.9 * (1 - u))
    for i in range(9):
        a = i / 9 * math.tau + rnd(i, x) * 0.5
        L0, L1 = r * 0.3 * k, r * (0.5 + 0.9 * k)
        line(ctx, [(x + L0 * math.cos(a), y + L0 * math.sin(a)), (x + L1 * math.cos(a), y + L1 * math.sin(a))],
             FIRE_Y, 5 * (1 - u) + 1, 1 - u)


def dust_cloud(ctx, x, y, u, w, seed=0, a=1.0):
    """Rolling dust/smoke puffs spreading over width w around x, u 0..1+ (keeps hanging)."""
    if u <= 0:
        return
    k = ease_out_cubic(clamp(u / 0.8))
    fade = a * (1 - 0.5 * clamp((u - 1.2) / 2.0))
    for i in range(26):
        px = x + (rnd(i, seed) - 0.5) * w * (0.4 + 0.8 * k)
        py = y - 140 * k * rnd(i, seed + 1) - 10
        r = (40 + 70 * rnd(i, seed + 2)) * (0.3 + 0.9 * k)
        circle(ctx, px, py, r, hexc("#4A3530") if i % 3 else hexc("#6B4A3A"), 0.55 * fade)
    glow(ctx, x, y - 40, w * 0.5 * k, hexc("#FF9A5A"), 0.25 * fade)


def gada(ctx, x0, y0, x1, y1, r):
    """Mace: grip at (x0, y0), head centred at (x1, y1) with radius r (local units)."""
    line(ctx, [(x0, y0), (x1, y1)], dv.OUTLINE, r * 0.42 + 12)
    line(ctx, [(x0, y0), (x1, y1)], hexc("#5A3418"), r * 0.42)
    for f in (0.2, 0.55):
        line(ctx, [(lerp(x0, x1, f) - 1, lerp(y0, y1, f) - 1), (lerp(x0, x1, f + 0.06), lerp(y0, y1, f + 0.06))],
             dv.GOLD, r * 0.5)
    ang = math.atan2(y1 - y0, x1 - x0)
    for k in range(7):
        a = ang + (k - 3) * 0.5
        ctx.move_to(x1 + r * 0.8 * math.cos(a - 0.2), y1 + r * 0.8 * math.sin(a - 0.2))
        ctx.line_to(x1 + r * 1.35 * math.cos(a), y1 + r * 1.35 * math.sin(a))
        ctx.line_to(x1 + r * 0.8 * math.cos(a + 0.2), y1 + r * 0.8 * math.sin(a + 0.2))
        ctx.close_path()
        ink(ctx, dv.GOLD_HI, 3)
    ell(ctx, x1, y1, r, r)
    ink(ctx, BRONZE)
    ell(ctx, x1, y1, r * 0.62, r * 0.62)
    ink(ctx, dv.GOLD, 4)
    gem(ctx, x1, y1, r * 0.25, dv.RED_GEM)


def vasavi_spear(ctx, x, y, ang, L, t, a=1.0):
    """Indra's Vasavi Shakti: blazing gold spear, head at (x, y) pointing along ang, crackling with light."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    glow(ctx, -L * 0.4, 0, L * 0.8, VASAVI, 0.5 * a)
    glow(ctx, 0, 0, 120, (1, 1, 1), 0.6 * a)
    line(ctx, [(-L, 0), (-40, 0)], dv.OUTLINE, 18, a)
    line(ctx, [(-L, 0), (-40, 0)], dv.GOLD, 11, a)
    line(ctx, [(-L, -2), (-40, -2)], VASAVI, 4, a)
    ctx.move_to(40, 0)                                   # leaf-shaped head, tip forward (+x)
    ctx.curve_to(10, -26, -30, -22, -48, 0)
    ctx.curve_to(-30, 22, 10, 26, 40, 0)
    ctx.close_path()
    ink(ctx, VASAVI, 4, a)
    for i in range(5):                                   # crackling sparks along the shaft
        px = -L * rnd(i, int(t * 12))
        py = 24 * (rnd(i + 3, int(t * 12)) - 0.5)
        line(ctx, [(px, 0), (px + 10, py), (px + 22, -py * 0.6)], (1, 1, 1), 3, 0.8 * a)
    ctx.restore()


# ============================================================ characters

def ghatotkach(ctx, x, y, s, t, pose="roar", roar=1.0, hit=0.0, rot=0.0, look=(0.0, 0.0), a=1.0):
    """Ghatotkach, Bhima-Hidimba's rakshasa prince: storm-blue skin, flame hair, small horns, gold band-mukut,
    tusks, ember eyes, giant gada. Poses roar (gada overhead, fire in the other palm) / stand / hit (clutching
    the Shakti wound). rot tilts the whole body about the feet (falling to the right when rot > 0)."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(rot)
        b = 1 + 0.014 * math.sin(t * 2.4)
        ctx.scale(s, s * b)
        _ghatotkach_body(ctx, t, pose, roar, hit, look)
        ctx.restore()
    dv.group(ctx, a, draw)


def _ghatotkach_body(ctx, t, pose, roar, hit, look):
    skin = GH_SKIN
    dk = shade(skin, 0.72)
    # flame hair mass behind the head
    pts = []
    for k in range(15):
        ang = math.pi * (0.95 + 1.1 * k / 14)
        rr = (190 if k % 2 else 125) + 10 * math.sin(t * 6 + k)
        pts.append((rr * math.cos(ang), -800 + rr * math.sin(ang) * 1.05))
    pts += [(120, -700), (-120, -700)]
    smooth(ctx, pts, k=0.08)
    ink(ctx, GH_HAIR)
    for k in range(1, 14, 2):
        ang = math.pi * (0.95 + 1.1 * k / 14)
        line(ctx, [(120 * math.cos(ang), -800 + 120 * math.sin(ang)),
                   (175 * math.cos(ang), -800 + 182 * math.sin(ang))], hexc("#A3262E"), 7)
    # legs: wide warrior stance
    for side in (-1, 1):
        limb(ctx, [(side * 70, -380), (side * 122, -200), (side * 128, -40)], skin, 80)
        line(ctx, [(side * 128 - 40, -70), (side * 128 + 40, -70)], dv.GOLD, 12)
        ell(ctx, side * 142, -18, 60, 22)
        ink(ctx, skin)
    # dhoti + belt
    smooth(ctx, [(-150, -440), (150, -440), (178, -310), (150, -240), (60, -266), (0, -236), (-60, -266),
                 (-150, -240), (-178, -310)])
    ink(ctx, hexc("#B3202A"))
    line(ctx, [(-150, -246), (-60, -270), (0, -240), (60, -270), (150, -246)], dv.GOLD, 10)
    # massive torso
    smooth(ctx, [(-205, -690), (-120, -722), (120, -722), (205, -690), (196, -600), (150, -480), (112, -440),
                 (-112, -440), (-150, -480), (-196, -600)], k=0.12)
    ink(ctx, skin)
    sheen(ctx, -70, -640, 70, 34, 0.15)
    for side in (-1, 1):            # pecs + abs
        ctx.move_to(side * 150, -640)
        ctx.curve_to(side * 120, -585, side * 50, -580, side * 8, -600)
        rgba(ctx, dk)
        ctx.set_line_width(6)
        ctx.stroke()
    for yy in (-555, -515, -478):
        line(ctx, [(-40, yy), (40, yy)], dk, 5)
    line(ctx, [(0, -600), (0, -460)], dk, 5)
    line(ctx, [(-190, -690), (140, -452)], dv.OUTLINE, 34)     # bronze cross strap with studs
    line(ctx, [(-190, -690), (140, -452)], BRONZE, 24)
    for f in (0.15, 0.4, 0.65, 0.9):
        circle(ctx, lerp(-190, 140, f), lerp(-690, -452, f), 7, dv.GOLD_HI)
    rrect(ctx, -158, -462, 316, 46, 14)
    ink(ctx, dv.GOLD)
    gem(ctx, 0, -439, 14, dv.RED_GEM)
    if hit > 0:                      # the Shakti strikes the chest
        glow(ctx, 0, -590, 260 * hit, VASAVI, 0.85 * hit)
        glow(ctx, 0, -590, 120, (1, 1, 1), 0.9 * hit)
        for k in range(7):
            a = k / 7 * math.tau + t * 3
            line(ctx, [(0, -590), (60 * math.cos(a), -590 + 60 * math.sin(a)),
                       (130 * math.cos(a + 0.3), -590 + 130 * math.sin(a + 0.3))], VASAVI, 6, hit)
    # arms
    Ls, Rs = (-195, -682), (195, -682)
    if pose == "roar":
        arms = [(Ls, (-300, -800), (-262, -930)), (Rs, (300, -650), (372, -720))]
    elif pose == "hit":
        arms = [(Ls, (-245, -540), (-70, -600)), (Rs, (245, -540), (70, -610))]
    else:
        arms = [(Ls, (-262, -540), (-250, -410)), (Rs, (285, -540), (175, -470))]
    if pose == "roar":               # gada raised overhead, behind the arm
        gada(ctx, -262, -930, -150, -1120, 70)
    elif pose == "stand":
        gada(ctx, -250, -410, -268, -90, 66)
    for sh, el, hd in arms:
        limb(ctx, [sh, el], skin, 68)
        limb(ctx, [el, hd], skin, 60)
        circle(ctx, lerp(sh[0], el[0], 0.55), lerp(sh[1], el[1], 0.55), 34, dv.GOLD)
        circle(ctx, lerp(sh[0], el[0], 0.55), lerp(sh[1], el[1], 0.55), 25, skin)
        line(ctx, [(lerp(el[0], hd[0], 0.75) - 18, lerp(el[1], hd[1], 0.75)),
                   (lerp(el[0], hd[0], 0.75) + 18, lerp(el[1], hd[1], 0.75))], dv.GOLD, 14)
    if pose == "roar":
        hand(ctx, -262, -930, skin, 38)
        palm(ctx, 372, -730, skin, ang=0.5, s=1.3)
        f = 1 + 0.2 * math.sin(t * 14)
        glow(ctx, 420, -800, 120 * f, FIRE_O, 0.8)
        circle(ctx, 420, -800, 46 * f, FIRE_Y)
        circle(ctx, 420, -800, 22 * f, (1, 0.98, 0.85))
    else:
        for _, _, hd in arms:
            hand(ctx, *hd, skin, 38)
    for side in (-1, 1):             # spiked pauldrons
        for k in range(3):
            ctx.move_to(side * (170 + 22 * k), -712)
            ctx.line_to(side * (178 + 22 * k), -770 + 8 * k)
            ctx.line_to(side * (196 + 22 * k), -706)
            ctx.close_path()
            ink(ctx, dv.GOLD_HI, 3)
        ell(ctx, side * 196, -690, 62, 46)
        ink(ctx, BRONZE)
        circle(ctx, side * 196, -690, 18, dv.GOLD)
    # neck + head
    rrect(ctx, -56, -772, 112, 86, 22)
    ink(ctx, skin)
    for side in (-1, 1):             # pointed ears + gold ear rings
        smooth(ctx, [(side * 92, -820), (side * 140, -858), (side * 106, -782)], k=0.05)
        ink(ctx, skin)
        ctx.arc(side * 108, -748, 20, 0, math.tau)
        rgba(ctx, dv.GOLD)
        ctx.set_line_width(8)
        ctx.stroke()
    ell(ctx, 0, -805, 106, 112)
    ink(ctx, skin)
    sheen(ctx, -38, -862, 36, 20, 0.16)
    # horns + gold band mukut (he is a prince)
    for side in (-1, 1):
        smooth(ctx, [(side * 52, -892), (side * 104, -1000), (side * 86, -888)], k=0.05)
        ink(ctx, hexc("#F1E3C4"), 4)
    smooth(ctx, [(-100, -882), (-66, -935), (-34, -905), (0, -960), (34, -905), (66, -935), (100, -882)], k=0.06)
    ink(ctx, dv.GOLD, 5)
    rrect(ctx, -104, -900, 208, 34, 10)
    ink(ctx, dv.GOLD, 5)
    gem(ctx, 0, -883, 11, dv.RED_GEM)
    # fierce brows + ember eyes
    for side in (-1, 1):
        line(ctx, [(side * 98, -858), (side * 26, -834)], GH_HAIR, 16)
        glow(ctx, side * 46, -812, 46, FIRE_O, 0.55)
        eye(ctx, side * 46, -812, 27, 22, t, look=look, iris=hexc("#FF5A1F"), seed=4, lid=0.22, skin=skin)
    ell(ctx, 0, -776, 24, 16)
    ink(ctx, dk, 4)
    # moustache
    for side in (-1, 1):
        smooth(ctx, [(side * 6, -756), (side * 52, -764), (side * 82, -744), (side * 70, -736), (side * 40, -748)],
               k=0.12)
        ink(ctx, GH_HAIR, 3)
    # mouth: roaring or grim, with upward tusks
    if roar > 0.05:
        ell(ctx, 0, -712, 46, 14 + 22 * roar)
        ink(ctx, hexc("#4A0A10"), 5)
        rrect(ctx, -32, -712 - 14 - 22 * roar + 4, 64, 10, 3)
        rgba(ctx, dv.WHITE)
        ctx.fill()
    else:
        line(ctx, [(-34, -716), (0, -708), (34, -716)], dv.OUTLINE, 6)
    for side in (-1, 1):
        smooth(ctx, [(side * 30, -706), (side * 46, -758), (side * 20, -712)], k=0.05)
        ink(ctx, dv.WHITE, 3)


def duryodhan(ctx, x, y, s, t, pose="point", shout=0.0, look=(0.6, 0.0), flip=False, a=1.0):
    """Duryodhan: tall gold mukut, curled moustache, purple-maroon armour, upright gada. Poses point (arm towards
    screen-right, shouting) / panic (shielding his eyes, looking up)."""
    def draw():
        dv.place(ctx, x, y, s, t, flip)
        _duryodhan_body(ctx, t, pose, shout, look)
        ctx.restore()
    dv.group(ctx, a, draw)


def _duryodhan_body(ctx, t, pose, shout, look):
    skin = DUR_SKIN
    hair = dv.HAIR
    ell(ctx, 0, -680, 116, 112)
    ink(ctx, hair)
    for side in (-1, 1):
        smooth(ctx, [(side * 70, -700), (side * 124, -600), (side * 134, -500), (side * 106, -480), (side * 90, -560)])
        ink(ctx, hair)
    for side in (-1, 1):
        limb(ctx, [(side * 58, -340), (side * 64, -170), (side * 64, -34)], skin, 52)
        ell(ctx, side * 70, -14, 44, 17)
        ink(ctx, skin)
        line(ctx, [(side * 64 - 26, -46), (side * 64 + 26, -46)], dv.GOLD, 8)
    smooth(ctx, [(-136, -360), (136, -360), (150, -230), (116, -150), (0, -170), (-116, -150), (-150, -230)])
    ink(ctx, hexc("#3B1C5C"))
    line(ctx, [(146, -228), (116, -156), (0, -176), (-116, -156), (-146, -228)], dv.GOLD, 10)
    smooth(ctx, [(-146, -520), (-78, -548), (78, -548), (146, -520), (148, -440), (114, -350), (-114, -350),
                 (-148, -440)])
    ink(ctx, DUR_ARMOR)
    smooth(ctx, [(-96, -515), (96, -515), (90, -420), (0, -380), (-90, -420)])
    ink(ctx, dv.GOLD, 5)
    sheen(ctx, -30, -470, 50, 26, 0.22)
    gem(ctx, 0, -455, 16, dv.RED_GEM)
    rrect(ctx, -124, -374, 248, 32, 10)
    ink(ctx, dv.GOLD)
    L, R = (-146, -515), (146, -515)
    if pose == "panic":
        arms = [(L, (-196, -420), (-190, -320)), (R, (225, -630), (110, -712))]
    else:
        wag = 10 * math.sin(t * 9) * shout
        arms = [(L, (-196, -420), (-190, -320)), (R, (255, -565), (360, -610 + wag))]
    gada(ctx, -190, -320, -205, -690, 54)          # upright gada in the screen-left hand
    for sh, el, hd in arms:
        limb(ctx, [sh, el], skin, 54)
        limb(ctx, [el, hd], skin, 46)
        circle(ctx, lerp(sh[0], el[0], 0.5), lerp(sh[1], el[1], 0.5), 28, dv.GOLD)
        circle(ctx, lerp(sh[0], el[0], 0.5), lerp(sh[1], el[1], 0.5), 21, skin)
    for side in (-1, 1):
        ell(ctx, side * 146, -518, 42, 30)
        ink(ctx, DUR_ARMOR)
    hand(ctx, -190, -320, skin, 28)
    if pose == "panic":
        hand(ctx, 110, -712, skin, 28)
    else:
        hand(ctx, 360, -610, skin, 28)
        limb(ctx, [(380, -615), (440, -625)], skin, 14)   # pointing finger
    # head
    rrect(ctx, -32, -600, 64, 70, 14)
    ink(ctx, skin)
    ell(ctx, 0, -690, 98, 106)
    ink(ctx, skin)
    sheen(ctx, -34, -740, 36, 20, 0.18)
    for side in (-1, 1):
        line(ctx, [(side * 70, -748), (side * 20, -730)], hair, 11)       # angry brows down to the centre
        eye(ctx, side * 38, -702, 23, 24, t, look=look, seed=6)
    ell(ctx, 0, -668, 12, 17)
    ink(ctx, shade(skin, 0.88), 3.5)
    for side in (-1, 1):             # curled moustache
        smooth(ctx, [(side * 4, -646), (side * 50, -652), (side * 78, -672), (side * 70, -640), (side * 36, -636)],
               k=0.12)
        ink(ctx, hair, 3)
    if shout > 0.05:
        ell(ctx, 0, -616, 26, 10 + 16 * shout)
        ink(ctx, hexc("#4A0A10"), 4)
    else:
        line(ctx, [(-22, -612), (0, -620), (22, -612)], dv.OUTLINE, 6)
    for side in (-1, 1):
        ell(ctx, side * 98, -680, 16, 26)
        ink(ctx, skin)
        circle(ctx, side * 102, -640, 13, dv.GOLD)
    smooth(ctx, [(-104, -778), (-90, -860), (-50, -830), (-26, -905), (0, -950), (26, -905), (50, -830),
                 (90, -860), (104, -778)], k=0.06)
    ink(ctx, dv.GOLD, 5)
    rrect(ctx, -108, -790, 216, 38, 10)
    ink(ctx, dv.GOLD, 5)
    gem(ctx, 0, -870, 14, dv.RED_GEM)
    gem(ctx, -60, -771, 8, dv.GREEN_GEM)
    gem(ctx, 60, -771, 8, dv.GREEN_GEM)


def soldier(ctx, x, y, s, t, i, mode="stand", flip=False, a=1.0):
    """Small Kaurava foot soldier (crowd unit). mode stand / panic (running, arms up) / look (staring up)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(-s if flip else s, s)
    skin = hexc("#C98A5A")
    ph = t * 14 + i * 1.7
    run = mode == "panic"
    for side in (-1, 1):
        sw = 22 * math.sin(ph + (0 if side < 0 else math.pi)) if run else 0
        limb(ctx, [(side * 14, -70), (side * 16 + sw, -34), (side * 14 + sw * 1.4, 0)], skin, 14)
    rrect(ctx, -26, -126, 52, 64, 12)
    ink(ctx, KAURAV_RED, 4)
    line(ctx, [(-26, -70), (26, -70)], dv.GOLD, 5)
    if run:
        for side in (-1, 1):
            wv = 10 * math.sin(ph * 1.3 + side)
            limb(ctx, [(side * 22, -118), (side * 40, -150), (side * 30 + wv, -186)], skin, 12)
    else:
        limb(ctx, [(-22, -118), (-34, -84)], skin, 12)
        limb(ctx, [(22, -118), (36, -88)], skin, 12)
        line(ctx, [(40, -10), (44, -210)], hexc("#3B2516"), 5)          # spear
        ctx.move_to(44, -230)
        ctx.line_to(36, -206)
        ctx.line_to(52, -206)
        ctx.close_path()
        ink(ctx, hexc("#C8CCD4"), 2)
        ell(ctx, -36, -88, 22, 28)                                     # shield
        ink(ctx, BRONZE, 3)
    ell(ctx, 0, -150, 24, 26)
    ink(ctx, skin, 4)
    ctx.move_to(-27, -152)
    ctx.curve_to(-26, -190, 26, -190, 27, -152)
    ctx.close_path()
    ink(ctx, BRONZE, 3)
    up = mode in ("panic", "look")
    for side in (-1, 1):
        circle(ctx, side * 9, -150 - (4 if up else 0), 5 if up else 3.5, dv.WHITE if up else dv.OUTLINE)
        if up:
            circle(ctx, side * 9, -152, 2.2, dv.OUTLINE)
    if up:
        ell(ctx, 0, -134, 6, 8)
        ink(ctx, hexc("#4A0A10"), 2)
    ctx.restore()


def kaurava_mob(ctx, x0, x1, y, n, t, mode="stand", s=0.55, flee=0.0, seed=0, a=1.0):
    """Two rows of Kaurava soldiers between x0 and x1; flee > 0 runs them towards screen-right (wrapping)."""
    span = x1 - x0
    for row, (dy, rs, n_row) in enumerate(((-36, s * 0.78, n), (0, s, n))):
        for i in range(n_row):
            base = (i + 0.5 + 0.5 * row) / n_row * span + 18 * math.sin(seed + i * 3 + row)
            xx = x0 + ((base + flee * t * (150 + 40 * rnd(i, seed + row))) % span)
            m = mode
            if mode == "mixed":
                m = "panic" if (i + row) % 2 else "look"
            ctx.save()
            if row == 0:
                ctx.push_group()
            soldier(ctx, xx, y + dy, rs, t, i + 10 * row + seed, mode=m, flip=False)
            if row == 0:
                ctx.pop_group_to_source()
                ctx.paint_with_alpha(0.75 * a)
            ctx.restore()


def fire_rain(ctx, t, t0, src, targets, period=0.9, r=26):
    """Fireballs leaving src along an arc to each target in turn (staggered), each ending in a blast, repeating."""
    if t < t0:
        return
    for k, (tx, ty) in enumerate(targets):
        u = (t - t0 - k * period * 0.35) / period
        if u < 0:
            continue
        u = u % 1.6
        if u <= 1.0:
            px = lerp(src[0], tx, u)
            py = lerp(src[1], ty, u) - 260 * math.sin(math.pi * u)
            dx = (tx - src[0])
            dy = (ty - src[1]) - 260 * math.pi * math.cos(math.pi * u)
            fireball(ctx, px, py, math.atan2(dy, dx), r, t)
        else:
            blast(ctx, tx, ty, (u - 1.0) / 0.6, 110)


# ============================================================ scenes

class Hook(Cued):
    """Opens mid-fall (continuing the last frame of 'gira'): the giant slams onto the army at 0.5 s."""
    IMPACT = 0.5

    def beats(self, d):
        return {"kuchal": self.cue("KUCHAL", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "whoosh"), (self.IMPACT, "boom"), (self.IMPACT + 0.05, "thud"), (b["kuchal"], "soft_thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        u = t - self.IMPACT
        shake = 22 * math.exp(-u * 4) if u > 0 else 0
        ctx.save()
        ctx.translate(shake * math.sin(t * 47), shake * math.cos(t * 41))
        night_kurukshetra(ctx, t)
        kaurava_mob(ctx, 520, 1080, GROUND - 14, 7, t, mode="mixed", s=0.52, flee=0.0, seed=3)
        rot = lerp(1.05, 1.42, ease_in(t / self.IMPACT))
        ctx.save()                                         # long shadow on the army before the hit
        rgba(ctx, (0, 0, 0), 0.35 * clamp(1 - u * 3) if u > 0 else 0.35)
        ell(ctx, 700, GROUND - 6, 300 * (rot / 1.42), 26)
        ctx.fill()
        ctx.restore()
        if u > 0:                                          # main dust rolls up behind the fallen body
            dust_cloud(ctx, 700, GROUND - 10, u, 700, seed=7, a=0.85)
        ghatotkach(ctx, 230, GROUND - 10, 0.80, t, pose="hit", roar=0.8, hit=0.6 * clamp(1 - t / 1.5), rot=rot,
                   look=(0.4, -0.5))
        if u > 0:
            dust_cloud(ctx, 820, GROUND + 20, t - b["kuchal"], 380, seed=9, a=0.45)
            flash(ctx, u, c=(1, 0.85, 0.6), dur=0.35)
            for i in range(10):                            # helmets, spears, shields thrown up (no gore)
                k = u * (1.0 + 0.4 * rnd(i, 1))
                px = 520 + 520 * rnd(i, 2) + 120 * k * (rnd(i, 3) - 0.5)
                py = GROUND - 40 - 700 * k + 900 * k * k
                if py < GROUND:
                    ctx.save()
                    ctx.translate(px, py)
                    ctx.rotate(k * 9 + i)
                    if i % 3 == 0:
                        line(ctx, [(-40, 0), (40, 0)], hexc("#3B2516"), 5)
                    elif i % 3 == 1:
                        ell(ctx, 0, 0, 16, 12)
                        ink(ctx, BRONZE, 3)
                    else:
                        ell(ctx, 0, 0, 20, 24)
                        ink(ctx, KAURAV_RED, 3)
                    ctx.restore()
        ctx.restore()


class Raat(Cued):
    """Night falls; at 'dugni' a violet maya aura doubles Ghatotkach's power (he swells, eyes flare, roars)."""

    def beats(self, d):
        return {"bheem": self.cue("BHEEM", d * 0.55), "dugni": self.cue("DUGNI", d * 0.78)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["bheem"], "thud"), (b["dugni"], "whoosh"), (b["dugni"] + 0.25, "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_kurukshetra(ctx, t)
        kaurava_mob(ctx, 560, 1080, GROUND - 14, 6, t, mode="look" if t > b["dugni"] else "stand", s=0.5, seed=1)
        p = ease_out_back(clamp((t - b["dugni"]) / 0.6), s=1.4)
        s = lerp(0.62, 0.70, p)
        pulse = 0.5 + 0.5 * math.sin(t * 7)
        for k in range(3):                                   # doubled power: violet maya rings
            glow(ctx, 300, GROUND - 420 * s / 0.7, (260 + 90 * k) * (0.6 + 0.6 * p), hexc("#7A2BFF"),
                 (0.12 + 0.12 * pulse) * p + 0.06)
        ghatotkach(ctx, 300, GROUND - 10, s, t, pose="roar" if t > b["bheem"] else "stand",
                   roar=(0.5 + 0.5 * pulse) if t > b["bheem"] else 0.0, look=(0.6, 0.0))


class Maya(Cued):
    def beats(self, d):
        return {"grow": self.cue("AASMAAN", 0.0) + 0.15, "aag": self.cue("AAG", d * 0.35),
                "bhaagi": self.cue("BHAAGI", d * 0.7)}

    def events(self, d):
        b = self.beats(d)
        ev = [(0.02, "whoosh"), (b["grow"] + 0.35, "boom"), (b["aag"], "whoosh")]
        ev += [(b["aag"] + 0.35 * k + 0.6, "thud") for k in range(3)]
        return ev

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_kurukshetra(ctx, t, lightning=clamp((t - b["grow"]) * 2))
        alarm = t > b["aag"]
        kaurava_mob(ctx, 560, 1080, GROUND - 14, 6, t, mode="panic" if alarm else "look", s=0.5,
                    flee=(1.4 if t > b["bhaagi"] else 0.8) if alarm else 0.0, seed=1)
        g = ease_out_back(clamp((t - b["grow"]) / 0.8), s=1.2)
        s = lerp(0.70, 0.80, g)
        glow(ctx, 280, GROUND - 330 * s / 0.5, 300 * s / 0.6, hexc("#7A2BFF"), 0.25 + 0.2 * g)   # maya aura
        ghatotkach(ctx, 280, GROUND - 10, s, t, pose="roar", roar=0.4 + 0.6 * abs(math.sin(t * 2.2)),
                   look=(0.6, 0.0))
        hx, hy = 280 + 420 * s, GROUND - 10 - 800 * s
        fire_rain(ctx, t, b["aag"], (hx, hy), [(700, GROUND - 60), (900, GROUND - 50), (1000, GROUND - 70),
                                              (620, GROUND - 40)], period=0.8)


class Bhagdad(Cued):
    def beats(self, d):
        return {"cheekha": self.cue("CHEEKHA", 0.0) + 0.1, "chalao": self.cue("CHALAO", d * 0.4)}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (0.5, "boom"), (b["cheekha"], "whoosh"), (b["chalao"] + 0.4, "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        night_kurukshetra(ctx, t, lightning=0.6)
        # the giant looms behind the hills as a silhouette with ember eyes
        dv.silhouette(ctx, lambda: ghatotkach(ctx, 560, GROUND - 120, 0.80, t, pose="roar", roar=0.8),
                      c=hexc("#12060E"), a=0.85)
        for side in (-1, 1):
            glow(ctx, 560 + side * 46 * 0.8, GROUND - 120 - 812 * 0.8, 40, FIRE_O, 0.9)
        fire_rain(ctx, t, 0.0, (560 + 420 * 0.8, GROUND - 120 - 800 * 0.8),
                  [(420, GROUND - 120), (760, GROUND - 110), (980, GROUND - 130)], period=0.9, r=20)
        kaurava_mob(ctx, 0, W, GROUND - 100, 8, t, mode="panic", s=0.42, flee=1.4, seed=5)
        shouting = t >= b["cheekha"]
        duryodhan(ctx, 245, GROUND - 10, 0.72, t, pose="point" if shouting else "panic",
                  shout=0.4 + 0.6 * abs(math.sin(t * 9)) if shouting else 0.0,
                  look=(0.7, 0.0) if shouting else (0.2, -0.7))
        dv.karna(ctx, 820, GROUND - 10, 0.72, t, pose="stand", look=(-0.6, 0.0) if shouting else (0.0, -0.5))


class Vasavi(Cued):
    FLIGHT = 0.35

    def beats(self, d):
        throw = self.cue("CHALA DI", d * 0.82) + 0.3
        return {"lift": self.cue("INDRA", 0.0), "arjun": self.cue("ARJUN", d * 0.4), "throw": throw,
                "hit": throw + self.FLIGHT}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "shimmer"), (b["throw"], "arrow"), (b["hit"], "boom"), (b["hit"] + 0.05, "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        u = t - b["hit"]
        shake = 16 * math.exp(-u * 5) if u > 0 else 0
        ctx.save()
        ctx.translate(shake * math.sin(t * 50), shake * math.cos(t * 43))
        night_kurukshetra(ctx, t, lightning=0.8)
        kaurava_mob(ctx, 380, 700, GROUND - 120, 4, t, mode="look", s=0.36, seed=8)
        hit = clamp(1 - u / 1.2) if u > 0 else 0.0
        ghatotkach(ctx, 240, GROUND - 10, 0.76, t, pose="hit" if u > 0 else "roar",
                   roar=0.9 if u > 0 else 0.5 + 0.5 * abs(math.sin(t * 2)), hit=hit,
                   look=(0.5, -0.4) if u > 0 else (0.6, 0.0))
        kx, ks = 830, 0.72
        thrown = t >= b["throw"]
        # Karna lowers his eyes at "Arjun ke liye" (the weapon he saved), then hurls it
        doubt = b["arjun"] <= t < b["throw"]
        dv.karna(ctx, kx, GROUND - 10, ks, t, pose="throw" if thrown else "raise",
                 look=(0.0, 0.6) if doubt else (-0.7, 0.0))
        hx, hy = kx + 215 * ks, GROUND - 10 - 810 * ks         # raised hand (world)
        if not thrown:
            pulse = 0.85 + 0.15 * math.sin(t * 10)
            vasavi_spear(ctx, hx - 150, hy - 6, math.pi, 260, t, a=pulse)   # head points left, at Ghatotkach
        elif t < b["hit"]:
            f = (t - b["throw"]) / self.FLIGHT
            sx, sy = kx - 175 * ks, GROUND - 10 - 650 * ks
            tx, ty = 240, GROUND - 10 - 590 * 0.76
            px, py = lerp(sx, tx, f), lerp(sy, ty, f)
            vasavi_spear(ctx, px, py, math.atan2(ty - sy, tx - sx), 260, t)
        else:
            flash(ctx, u, c=(1, 0.98, 0.85), dur=0.4)
        ctx.restore()


class Gira(Cued):
    """Hit -> grows mountain-sized -> topples and slams onto the army on 'gira' (dust, shake, flash)."""
    FALL = 0.9

    def beats(self, d):
        seedha = self.cue("SEEDHA", d * 0.7)
        impact = min(seedha + 0.2 + self.FALL, d - 0.15)
        return {"pahaad": self.cue("PAHAAD", d * 0.45), "fall": impact - self.FALL, "impact": impact}

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["pahaad"], "whoosh"), (b["pahaad"] + 0.3, "thud"), (b["fall"], "whoosh"),
                (b["impact"], "boom"), (b["impact"] + 0.05, "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        grow = ease_out_back(clamp((t - b["pahaad"]) / 0.7), s=1.3)
        u = t - b["impact"]
        rumble = 9 * grow * (1 if t < b["fall"] else 0.5) + (24 * math.exp(-u * 4) if u > 0 else 0)
        ctx.save()
        ctx.translate(rumble * math.sin(t * 38), rumble * math.cos(t * 33))
        night_kurukshetra(ctx, t, lightning=1.0)
        kaurava_mob(ctx, 520, 1080, GROUND - 14, 7, t, mode="mixed" if t > b["fall"] else "look", s=0.52, seed=3)
        s = lerp(0.66, 0.80, grow)
        rot = 1.42 * ease_in((t - b["fall"]) / self.FALL)
        if 0 < rot and u <= 0:
            rgba(ctx, (0, 0, 0), 0.35 * rot / 1.42)
            ell(ctx, 700, GROUND - 6, 300 * rot / 1.42, 26)
            ctx.fill()
        if u > 0:
            dust_cloud(ctx, 700, GROUND - 10, u, 700, seed=7, a=0.85)
        glow(ctx, 230, GROUND - 400, 420 * s, hexc("#FF3B1F"), 0.3 * grow * (1 - clamp(rot)))
        gada(ctx, 120, GROUND - 30, 20, GROUND - 40, 40)      # the dropped gada lies at his feet
        ghatotkach(ctx, 230, GROUND - 10, s, t, pose="hit", roar=0.8, hit=clamp(1 - t / 1.4) * 0.8 + 0.3 * grow,
                   rot=rot, look=(0.4, -0.5))
        if u > 0:
            flash(ctx, u, c=(1, 0.85, 0.6), dur=0.35)
        ctx.restore()


class Twist(Cued):
    """Krishna smiles (abhaya) beside a safe Arjun bowing in gratitude; the fallen hero glows gold behind them.
    The last 0.45 s cross-fades into the hook's first frame (giant mid-fall) so 'aur...' loops to 'marte marte bhi'."""

    def beats(self, d):
        return {"krishna": self.cue("KRISHNA", 0.0), "arjun": self.cue("ARJUN", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(0.05, "shimmer"), (b["arjun"], "ghanti")]

    def draw(self, ctx, t, d):
        from kathas.ghatotkach import arjuna
        b = self.beats(d)
        night_kurukshetra(ctx, t, fires=0.6)
        glow(ctx, 540, 760, 620, GOLD_HI, 0.22)
        # the fallen hero far behind, lying over the broken ranks, bathed in gold
        glow(ctx, 520, GROUND - 190, 340, GOLD_HI, 0.35)
        ghatotkach(ctx, 400, GROUND - 175, 0.30, t, pose="hit", roar=0.0, hit=0.0, rot=1.48, look=(0.0, 0.0), a=0.75)
        dv.petals(ctx, t, n=30, seed=4, a=0.8)
        safe = t >= b["arjun"]
        arjuna(ctx, 270, GROUND - 10, 0.70, t, pose="namaste" if safe else "shock", flip=False)
        glow(ctx, 790, GROUND - 280, 340, GOLD_HI, 0.45 + 0.15 * math.sin(t * 3))
        dv.krishna(ctx, 790, GROUND - 10, 0.74, t, pose="bless", smile=1.0, flip=True)
        x = clamp((t - (d - 0.45)) / 0.45)
        if x > 0:
            ctx.push_group()
            Hook().draw(ctx, 0.0, d)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(x)


SCENE_CLASSES = {"hook": Hook, "raat": Raat, "maya": Maya, "bhagdad": Bhagdad, "vasavi": Vasavi, "gira": Gira,
                 "twist": Twist}


# ============================================================ thumbnail + upload kit

def thumbnail(ctx):
    night_kurukshetra(ctx, 0.4, lightning=0.0)
    glow(ctx, 330, 900, 520, hexc("#FF3B1F"), 0.35)
    kaurava_mob(ctx, 560, 1080, 1250, 6, 0.3, mode="panic", s=0.55, seed=1)
    ghatotkach(ctx, 330, 1260, 0.84, 0.3, pose="roar", roar=1.0, look=(0.6, 0.0))
    for k, (x, y) in enumerate(((800, 1000), (960, 1110))):
        fireball(ctx, x, y, 0.9, 30, 0.2 * k)
    blast(ctx, 900, 1230, 0.35, 140)
    vasavi_spear(ctx, 600, 840, math.pi - 0.3, 320, 0.1)       # the Shakti streaking in from the right, tip at his chest
    g = cairo.LinearGradient(0, 0, 0, 560)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.9)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 560)
    ctx.set_source(g)
    ctx.fill()
    g = cairo.LinearGradient(0, 1380, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.9)
    ctx.rectangle(0, 1380, W, H - 1380)
    ctx.set_source(g)
    ctx.fill()
    text(ctx, "MARTE MARTE BHI", 540, 230, 120, FIRE_Y, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "SENA KUCHAL DI", 540, 370, 128, hexc("#FF4A3A"), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0),
         stroke_w=24)
    text(ctx, "DIVYA RAHASYA", 540, 1820, 42, GOLD_HI, a=0.85)


UPLOAD = {
    "thumb_text": "MARTE MARTE BHI",
    "titles": [
        "Marte Marte Bhi Ghatotkach Ne Kaurav Sena Kuchal Di #shorts",
        "Ghatotkach Ka Aakhri Waar: Poori Akshauhini Khatam",
        "Ghatotkach vs Karna: Vasavi Shakti Ki Raat",
        "Ghatotkach Pahaad Jitna Bada Hokar Kaurav Sena Par Gira",
        "Karna Ne Arjun Wali Shakti Ghatotkach Par Kyun Chalai",
        "Mahabharat Ki Sabse Khatarnak Raat: Ghatotkach",
        "Ghatotkach Ki Maut Ne Ek Akshauhini Kuchal Di",
        "Ghatotkach Ka Balidaan: Kurukshetra Ki 14vi Raat",
        "Duryodhan Kyun Chillaya: Karna Vasavi Shakti Chalao",
        "Ghatotkach Ka Mayavi Roop: Mahabharat Rahasya",
    ],
    "queries": [
        "ghatotkach ki maut kaise hui",
        "ghatotkach vs karna vasavi shakti",
        "ghatotkach ne kitni sena mari",
    ],
    "description": (
        "Ghatotkach ki maut kaise hui? Kurukshetra ki 14vi raat Ghatotkach vs Karna: Duryodhan ne Karna se "
        "Vasavi Shakti chalwayi - wahi shakti jo Arjun ke liye bachakar rakhi thi. Aur marte marte bhi Ghatotkach "
        "pahaad jitna bada hokar Kaurav sena par gira.\n\n"
        "Is Short mein:\n"
        "- Ghatotkach ka mayavi roop aur aag ki baarish\n"
        "- Duryodhan ki cheekh aur Karna ka mushkil faisla\n"
        "- Indra ki Vasavi Shakti aur Ghatotkach ka aakhri waar\n"
        "- Krishna kyun muskuraye: Arjun ki jaan kaise bachi\n\n"
        "Source: Mahabharat, Drona Parva (Ghatotkacha-vadha Parva). Kuch sanskaranon mein 'ek poori akshauhini' "
        "likha hai, kuch mein 'sena ka bada hissa'.\n\n"
        "Comment mein batao: Ghatotkach ya Barbarik - Bhim ke parivaar ka sabse bada yodha kaun?\n\n"
        "#Shorts #Mahabharat #Ghatotkach #Karna #Kurukshetra"
    ),
    "tags": ["ghatotkach", "ghatotkacha", "ghatotkach vs karna", "vasavi shakti", "mahabharat", "karna",
             "duryodhan", "kurukshetra", "mahabharat shorts", "ghatotkach death", "akshauhini", "hindu mythology",
             "divya rahasya"],
    "hashtags": ["#Shorts", "#Mahabharat", "#Ghatotkach"],
}
