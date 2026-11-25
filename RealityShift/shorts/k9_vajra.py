"""Reality Shift Short: K9 Vajra - the gun built for the desert now stands in Ladakh's snow (25 Nov 2026).

Facts (see SOURCES): K9 Vajra-T = 155 mm / 52 cal tracked self-propelled gun, the Indian version of Hanwha's K9
Thunder, built by L&T at its Armoured Systems Complex in Hazira (Gujarat); first 100 ordered May 2017, all delivered by
Feb 2021; originally meant for desert operations, adapted for eastern Ladakh after the 2020 India-China standoff with a
winterisation package (special oils/lubricants, heating systems) so it does not freeze; Dec 2024 MoD signed Rs 7,629
crore with L&T for 100 more; range ~38-40 km (sources differ -> spoken as "lagbhag chalees kilometer").
Not used (sources disagree / unconfirmed): burst rate, regiment size in Ladakh, the 2026 "335 more" report.
Debate (no party, no person, no nation hate): "Desi ya videshi?" - Korean design vs made in Gujarat.
Format: 9:16, ~33 s, 6 scenes; turn by 0:08, spec callouts instead of exposition (Marut lesson).
"""

import importlib
import json
import math
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cairo

from core import delivery, engine, lego
from core.engine import *  # noqa: F401,F403
from shorts.chabahar import Cued
from shorts.reality_shift import flag
from shorts.akashteer import soldier
from shorts.zorawar import ridges, snow, smoke, flash, blast
from shorts.marut import balance

TOPIC = "K9 VAJRA - REGISTAN KI TOP LADAKH KI BARF MEIN"
OUTPUTS = {"edge": "k9_vajra_short.mp4"}
LEGO = {"header": "intel", "caption": "chip", "transition": "scan", "palette": "khaki", "ending": "prompt"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.25
TAIL_PAD = 0.22
TRIM = {"thresh": 0.006, "keep": 0.04, "keep_tail": 0.06}
MUSIC_BPM = 92           # >= 6 away from INSAS (84)
MUSIC_STYLE = "tension"  # kaveri march, insas ambient
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.05}
KIKI_PAUSE_MS = 0
MAX_SECONDS = 35.0

PAL = lego.PALETTES["khaki"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
WHITE = (1.0, 1.0, 1.0)
GOLD = hexc("#FFD166")
RED = hexc("#E2483A")
CYAN = hexc("#5FD3FF")
ICE = hexc("#CFF2FF")
FIRE = hexc("#FF6A1A")
OLIVE = hexc("#5E6B34")
SAND_GUN = hexc("#A8915A")
GROUND = 1040

SOURCES = [
    "L&T - K9 Vajra-T 155 mm / 52 cal tracked SP gun: https://www.larsentoubro.com/lt-pes/our-offerings/"
    "land-platforms-equipment-and-systems/land-platforms/artillery-systems/k9-vajra-t-55-mm-52-cal-tracked-self-propelled-sp-gun",
    "Business Standard, 20 Dec 2024 - MoD signs Rs 7,629 cr deal with L&T for additional K9 Vajra guns: "
    "https://business-standard.com/external-affairs-defence-security/news/mod-signs-rs-7-629-cr-deal-with-lt-for-"
    "additional-k9-vajra-artillery-guns-124122001200_1.html",
    "Janes - L&T completes deliveries of K9 Vajra-T SPHs (first 100, Hazira): https://www.janes.com/defence-intelligence-"
    "insights/defence-news/lt-completes-deliveries-of-k9-vajra-t-sphs-to-indian-army",
    "ThePrint - Army to order another 100 K9 Vajra (desert gun adapted for Ladakh, winterisation): "
    "https://theprint.in/defence/china-threat-in-mind-army-to-order-another-100-k9-vajra-howitzers-from-lt-more-to-follow/1144787",
    "AlphaDefense - K9 Vajra-T (range ~40 km, winterisation kit): https://alphadefense.in/encyclopedia/k9-vajra-t/",
]

SPEC = [
    {"key": "hook", "accent": SAFFRON, "text": "",
     "visual": "Desert dunes: the K9 rolls through sand with a dust trail; hard cut to Ladakh snow ridges - the same gun "
               "frosted white, a jawan with binoculars watching the dashed LAC",
     "vo": [("hook", [("ये तोप", "YE TOP"), ("रेगिस्तान के लिए बनी थी।", "REGISTAN KE LIYE BANI THI")]),
            ("punch", [("पर आज ये", "PAR AAJ YE"), ("लद्दाख की बर्फ में", "LADAKH KI BARF MEIN"),
                       ("चीन के सामने खड़ी है।", "CHINA KE SAAMNE KHADI HAI")])]},
    {"key": "tanav", "accent": RED, "text": "",
     "visual": "2020 chip flashes red; the K9 on a trailer climbs a zig-zag mountain road at night, headlights on",
     "vo": [("tell", [("दो हज़ार बीस में", "2020 MEIN"), ("चीन से तनाव बढ़ा।", "CHINA SE TANAAV BADHA")]),
            ("punch", [("तो सेना इसे", "TO SENA ISE"), ("पहाड़ों पर ले गई।", "PAHADON PAR LE GAYI")])]},
    {"key": "thand", "accent": ICE, "text": "",
     "visual": "A thermometer plunges to -20 C; an oil drop turns into an ice cube; frost creeps over the gun; the jawan "
               "shivers",
     "vo": [("build", [("पर वहां इतनी ठंड है", "PAR WAHAN ITNI THAND HAI"), ("कि तेल तक", "KI TEL TAK"),
                       ("जम जाता है।", "JAM JAATA HAI")])]},
    {"key": "kit", "accent": FIRE, "text": "",
     "visual": "Kit crates snap open (OIL / HEATER); an orange heater glow spreads, frost melts, exhaust smoke starts",
     "vo": [("tell", [("इसलिए इसे", "ISLIYE ISE"), ("खास तेल और हीटर वाली", "KHAAS TEL AUR HEATER WAALI"),
                      ("किट दी गई।", "KIT DI GAYI")])]},
    {"key": "dagti", "accent": GOLD, "text": "",
     "visual": "The barrel elevates and fires on 'gola'; the shell arcs over the ridges with a 40 KM range bar; then a "
               "line of new K9s rolls out with a +100 chip",
     "vo": [("build", [("अब ये लगभग", "AB YE LAGBHAG"), ("चालीस किलोमीटर दूर तक", "40 KILOMETER DOOR TAK"),
                       ("गोला दागती है।", "GOLA DAAGTI HAI")]),
            ("punch", [("और सेना ने", "AUR SENA NE"), ("सौ और मंगवा ली हैं।", "100 AUR MANGWA LI HAIN")])]},
    {"key": "debate", "accent": INDIA_GREEN, "text": "",
     "visual": "Balance: a Korean flag (design) vs the tricolour (made in Hazira, Gujarat); the poll asks DESI YA VIDESHI",
     "vo": [("tell", [("पर इसका डिज़ाइन", "PAR ISKA DESIGN"), ("कोरिया का है", "KOREA KA HAI"),
                      ("और ये बनती है गुजरात में।", "AUR YE BANTI HAI GUJARAT MEIN")]),
            ("punch", [("तो के नाइन वज्र", "TO K9 VAJRA"), ("देसी है या विदेशी।", "DESI HAI YA VIDESHI?")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "TOP": GOLD, "REGISTAN": SAFFRON, "LADAKH": ICE, "BARF": ICE, "CHINA": RED, "2020": RED, "TANAAV": RED,
    "PAHADON": ICE, "THAND": ICE, "TEL": GOLD, "JAM": CYAN, "KHAAS": FIRE, "HEATER": FIRE, "KIT": FIRE,
    "40": GOLD, "KILOMETER": GOLD, "GOLA": FIRE, "100": INDIA_GREEN, "KOREA": CYAN, "GUJARAT": SAFFRON,
    "K9": SAFFRON, "VAJRA": SAFFRON, "DESI": INDIA_GREEN, "VIDESHI?": CYAN, "VIDESHI": CYAN, "DESIGN": CYAN,
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".")] = HOT[_k]


def at(scene, key, frac, d):
    return scene.cue(key, frac * d)


def shade(c, k):
    return tuple(clamp(v * k) for v in c)


# ============================================================ the gun (side view, facing +x)

def k9(ctx, x, y, s, t, body=OLIVE, elev=0.0, recoil=0.0, roll=0.0, frost=0.0, flip=False, a=1.0):
    """K9 Vajra-T: 7 road wheels, low hull, big boxy rear turret, long barrel with fume extractor and muzzle brake.
    Track bottom at (x, y). elev = barrel elevation (rad). Returns the muzzle point in parent coordinates."""
    sx = -s if flip else s
    piv = (40, -190)                                              # trunnion (turret front)
    gl = 520
    mx = piv[0] + (gl - recoil) * math.cos(-elev)
    my = piv[1] + (gl - recoil) * math.sin(-elev)
    muzzle = (x + mx * sx, y + my * s)
    if a <= 0:
        return muzzle
    ctx.push_group()
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(sx, s)
    L, r = 480, 26
    rrect(ctx, -L / 2 - 8, -2 * r - 14, L + 16, 2 * r + 14, r + 6)          # track
    rgba(ctx, (0.1, 0.1, 0.09))
    ctx.fill()
    for i in range(7):
        wx = -L / 2 + r + 10 + i * (L - 2 * r - 20) / 6
        ctx.arc(wx, -r - 7, r, 0, math.tau)
        rgba(ctx, shade(body, 0.55))
        ctx.fill()
        for k in range(3):
            ang = roll + k * math.tau / 3
            line(ctx, [(wx, -r - 7), (wx + r * 0.8 * math.cos(ang), -r - 7 + r * 0.8 * math.sin(ang))],
                 (0.15, 0.15, 0.13), 3)
    ctx.move_to(-L / 2 - 6, -2 * r - 14)                                   # hull with sloped glacis
    ctx.line_to(L / 2 + 40, -2 * r - 14)
    ctx.line_to(L / 2 - 20, -2 * r - 74)
    ctx.line_to(-L / 2 + 6, -2 * r - 74)
    ctx.close_path()
    rgba(ctx, body)
    ctx.fill()
    ctx.rectangle(-L / 2 + 14, -2 * r - 44, L * 0.86, 6)
    rgba(ctx, shade(body, 0.7))
    ctx.fill()
    ctx.save()                                                             # barrel (behind the turret face)
    ctx.translate(*piv)
    ctx.rotate(-elev)
    ctx.rectangle(-30 - recoil, -14, gl, 28)
    rgba(ctx, shade(body, 0.8))
    ctx.fill()
    rrect(ctx, 200 - recoil, -20, 70, 40, 12)                              # fume extractor
    rgba(ctx, shade(body, 0.7))
    ctx.fill()
    ctx.rectangle(gl - 60 - recoil, -22, 56, 44)                           # muzzle brake
    rgba(ctx, shade(body, 0.55))
    ctx.fill()
    for k in range(3):
        ctx.rectangle(gl - 54 - recoil + 18 * k, -22, 6, 44)
        rgba(ctx, (0.08, 0.08, 0.08))
        ctx.fill()
    ctx.restore()
    ctx.move_to(-230, -2 * r - 74)                                         # turret: big box, sloped front
    ctx.line_to(90, -2 * r - 74)
    ctx.line_to(60, -270)
    ctx.line_to(-210, -280)
    ctx.close_path()
    rgba(ctx, shade(body, 1.12))
    ctx.fill()
    rrect(ctx, -150, -300, 90, 26, 6)                                      # commander hatch + MG
    rgba(ctx, shade(body, 0.9))
    ctx.fill()
    line(ctx, [(-110, -300), (-40, -318)], (0.2, 0.2, 0.2), 6)
    line(ctx, [(-200, -280), (-215, -380)], (0.2, 0.2, 0.2), 3)            # antenna
    for k in range(4):                                                     # stowage boxes
        rrect(ctx, -220 + 60 * k, -170, 50, 34, 4)
        rgba(ctx, shade(body, 0.78))
        ctx.fill()
    if frost > 0:                                                          # snow on top + icy tint
        for (x0, x1, yy) in ((-230, 90, -280), (-L / 2 + 6, L / 2 - 20, -2 * r - 74)):
            rrect(ctx, x0, yy - 14 * frost, x1 - x0, 18 * frost, 8)
            rgba(ctx, (0.95, 0.98, 1.0), 0.95)
            ctx.fill()
    ctx.restore()
    if frost > 0:
        ctx.set_operator(cairo.OPERATOR_ATOP)
        ctx.rectangle(x - 600 * s, y - 600 * s, 1300 * s, 700 * s)
        rgba(ctx, ICE, 0.35 * frost)
        ctx.fill()
        ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(a)
    return muzzle


# ============================================================ scenery & props

def desert(ctx, t, scroll=0.0):
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    for at_, c in ((0, "#F2B25A"), (0.55, "#F8D08A"), (1, "#E8B070")):
        g.add_color_stop_rgb(at_, *hexc(c))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    glow(ctx, 820, 300, 220, hexc("#FFF0C0"), 0.7)
    circle(ctx, 820, 300, 80, hexc("#FFF4D8"))
    for k, (yb, c, amp) in enumerate(((820, "#D89A50", 70), (930, "#C8863C", 50), (GROUND, "#B87430", 30))):
        ctx.move_to(-60, H)
        for xx in range(-60, W + 80, 40):
            ctx.line_to(xx, yb - amp * math.sin((xx + scroll * (k + 1) * 60) / 160 + k))
        ctx.line_to(W + 60, H)
        ctx.close_path()
        rgba(ctx, hexc(c))
        ctx.fill()


def snowfield(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    g.add_color_stop_rgb(0, *hexc("#0B1A30"))
    g.add_color_stop_rgb(0.7, *hexc("#3A5A80"))
    g.add_color_stop_rgb(1, *hexc("#8AA8C8"))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    glow(ctx, 860, 260, 120, hexc("#EEF4FF"), 0.5)
    circle(ctx, 860, 260, 44, hexc("#F4F6FF"))
    ridges(ctx, t)
    ctx.rectangle(0, GROUND - 20, W, H)
    rgba(ctx, hexc("#E6EEF8"))
    ctx.fill()


def lac(ctx, t, x0=560, x1=1060, y=700, a=1.0):
    ctx.set_dash([26, 18], -t * 40)
    line(ctx, [(x0, y), (x1, y - 40)], RED, 7, a)
    ctx.set_dash([])
    rrect(ctx, x1 - 150, y - 120, 130, 56, 8)
    rgba(ctx, (0, 0, 0), 0.55 * a)
    ctx.fill()
    text(ctx, "LAC", x1 - 85, y - 92, 40, RED, font=CAPTION_FONT, bold=False, a=a)


def chip(ctx, s, x, y, c, u, size=54):
    if u <= 0:
        return
    k = ease_out_back(clamp(u / 0.35))
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    w = text_width(ctx, s, size, font=CAPTION_FONT, bold=False) + 50
    rrect(ctx, -w / 2, -size * 0.75, w, size * 1.5, 12)
    rgba(ctx, (0.02, 0.03, 0.02), 0.85)
    ctx.fill()
    rrect(ctx, -w / 2, -size * 0.75, w, size * 1.5, 12)
    rgba(ctx, c)
    ctx.set_line_width(5)
    ctx.stroke()
    text(ctx, s, 0, 0, size, c, font=CAPTION_FONT, bold=False)
    ctx.restore()


def thermometer(ctx, x, y, level, t):
    """level 1 = warm, 0 = -20 C."""
    rrect(ctx, x - 34, y - 520, 68, 520, 34)
    rgba(ctx, (0.95, 0.97, 1.0))
    ctx.fill()
    c = mix_c(CYAN, RED, level)
    h = 60 + 400 * level
    rrect(ctx, x - 16, y - 40 - h, 32, h, 16)
    rgba(ctx, c)
    ctx.fill()
    circle(ctx, x, y - 10, 52, c)
    for k in range(6):
        line(ctx, [(x + 34, y - 100 - 70 * k), (x + 60, y - 100 - 70 * k)], (0.8, 0.85, 0.9), 4)


def oil_drop(ctx, x, y, frozen):
    if frozen < 1:
        ctx.move_to(x, y - 90)
        ctx.curve_to(x + 60, y - 10, x + 60, y + 60, x, y + 60)
        ctx.curve_to(x - 60, y + 60, x - 60, y - 10, x, y - 90)
        rgba(ctx, hexc("#E0A02A"), 1 - frozen)
        ctx.fill()
    if frozen > 0:
        k = ease_out_back(clamp(frozen))
        rrect(ctx, x - 70 * k, y - 60 * k, 140 * k, 130 * k, 18)
        rgba(ctx, ICE, 0.9 * frozen)
        ctx.fill()
        line(ctx, [(x - 40 * k, y - 30 * k), (x - 10 * k, y - 50 * k)], (1, 1, 1), 6, frozen)
        circle(ctx, x, y + 10, 26 * k, hexc("#C8902A"), 0.8 * frozen)


def crate(ctx, x, y, label, u, c):
    rrect(ctx, x - 130, y - 150, 260, 150, 10)
    rgba(ctx, hexc("#4A5A2E"))
    ctx.fill()
    ctx.save()                                                    # lid flips open
    ctx.translate(x - 130, y - 150)
    ctx.rotate(-1.1 * ease_out_back(clamp(u)))
    rrect(ctx, 0, -24, 260, 26, 8)
    rgba(ctx, hexc("#5E7038"))
    ctx.fill()
    ctx.restore()
    text(ctx, label, x, y - 75, 44, c, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=6)
    if u > 0.3:
        glow(ctx, x, y - 160, 140, c, 0.5 * clamp((u - 0.3) / 0.4))


def korea_flag(ctx, x, y, w, h):
    rrect(ctx, x, y, w, h, 4)
    rgba(ctx, (1, 1, 1))
    ctx.fill()
    cx, cy, r = x + w / 2, y + h / 2, h * 0.24
    ctx.arc(cx, cy, r, math.pi, math.tau)
    rgba(ctx, hexc("#CD2E3A"))
    ctx.fill()
    ctx.arc(cx, cy, r, 0, math.pi)
    rgba(ctx, hexc("#0047A0"))
    ctx.fill()
    for (dx, dy, ang) in ((-1, -1, 0.6), (1, 1, 0.6), (1, -1, -0.6), (-1, 1, -0.6)):
        ctx.save()
        ctx.translate(cx + dx * w * 0.32, cy + dy * h * 0.3)
        ctx.rotate(ang)
        for k in range(3):
            ctx.rectangle(-w * 0.07, -h * 0.07 + k * h * 0.05, w * 0.14, h * 0.03)
            rgba(ctx, (0, 0, 0))
            ctx.fill()
        ctx.restore()


def mix_c(a, b, u):
    return tuple(p + (q - p) * clamp(u) for p, q in zip(a, b))


# ============================================================ scenes

class Hook(Cued):
    """Desert run -> same gun in Ladakh snow facing the LAC, a jawan with binoculars."""

    def events(self, d):
        return [(0.05, "whoosh"), (at(self, "PAR AAJ", 0.4, d), "whoosh"), (at(self, "CHINA", 0.75, d), "alarm")]

    def draw(self, ctx, t, d):
        tp = at(self, "PAR AAJ", 0.4, d)
        if t < tp + 0.3:
            desert(ctx, t, scroll=t)
            k9(ctx, 420 + 60 * t, GROUND - 20, 1.0, t, body=SAND_GUN, roll=t * 6)
            for i in range(6):                                    # dust trail
                u = (t * 1.4 + i / 6) % 1
                circle(ctx, 120 + 60 * t - 200 * u, GROUND - 40 - 50 * u, 20 + 50 * u, hexc("#E8C890"), 0.5 * (1 - u))
        if t >= tp:
            ctx.push_group()
            snowfield(ctx, t)
            lac(ctx, t, a=clamp((t - at(self, "CHINA", 0.75, d)) / 0.4) if t > tp else 0)
            k9(ctx, 330, GROUND - 20, 0.92, t, elev=0.12, frost=1.0)
            soldier(ctx, 975, GROUND - 10, 0.62, t, pose="binocs", flip=True)
            snow(ctx, t, n=70)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(clamp((t - tp) / 0.25))


class Tanav(Cued):
    """2020 chip; the K9 on a trailer climbs a zig-zag mountain road at night."""

    def events(self, d):
        return [(0.1, "beep"), (at(self, "TO SENA", 0.5, d), "whoosh")]

    def draw(self, ctx, t, d):
        ts = at(self, "TO SENA", 0.5, d)
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, *hexc("#060C1C"))
        g.add_color_stop_rgb(1, *hexc("#1A2A44"))
        ctx.set_source(g)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()
        ridges(ctx, t)
        road = [(160, 1010), (760, 960), (260, 820), (860, 700), (420, 560)]
        line(ctx, road, hexc("#3A4658"), 46)
        ctx.set_dash([24, 22])
        line(ctx, road, hexc("#E8C040"), 4, 0.7)
        ctx.set_dash([])
        u = ease_in_out(clamp((t - ts + 0.2) / max(1.0, d - ts)))
        seg = u * (len(road) - 1)
        i = min(int(seg), len(road) - 2)
        f = seg - i
        px = lerp(road[i][0], road[i + 1][0], f)
        py = lerp(road[i][1], road[i + 1][1], f)
        s = lerp(0.62, 0.34, u)
        flip = road[i + 1][0] < road[i][0]
        rrect(ctx, px - 300 * s, py - 30 * s, 600 * s, 34 * s, 6)                 # trailer
        rgba(ctx, hexc("#2A2E36"))
        ctx.fill()
        mz = k9(ctx, px, py - 30 * s, s, t, roll=t * 5, flip=flip)
        hx = px + (330 * s if not flip else -330 * s)
        glow(ctx, hx, py - 60 * s, 160 * s, hexc("#FFF2B0"), 0.6)
        chip(ctx, "2020", 540, 300, RED, t / 0.4)
        if t > 0.3:
            chip(ctx, "INDIA - CHINA STANDOFF", 540, 400, WHITE, (t - 0.3) / 0.4, size=40)


class Thand(Cued):
    """Thermometer plunges, an oil drop freezes into ice, frost creeps over the gun, the jawan shivers."""

    def events(self, d):
        return [(0.1, "tick"), (at(self, "JAM", 0.7, d), "zap")]

    def draw(self, ctx, t, d):
        tj = at(self, "JAM", 0.7, d)
        snowfield(ctx, t)
        lvl = 1 - ease_in_out(clamp(t / max(0.8, tj)))
        frost = 1 - lvl
        k9(ctx, 660, GROUND - 20, 0.8, t, frost=frost)
        thermometer(ctx, 110, 900, lvl, t)
        chip(ctx, "-20 C", 130, 300, CYAN, (t - tj * 0.6) / 0.3, size=60)
        oil_drop(ctx, 840, 300, clamp((t - tj) / 0.5))
        soldier(ctx, 290, GROUND - 10, 0.56, t, pose="look_up")
        snow(ctx, t, n=110, k=1.0)


class Kit(Cued):
    """Crates snap open (OIL / HEATER); heater glow spreads, frost melts, exhaust smoke starts."""

    def events(self, d):
        return [(at(self, "KHAAS", 0.3, d), "pop"), (at(self, "HEATER", 0.55, d), "pop"), (at(self, "KIT", 0.8, d), "boom")]

    def draw(self, ctx, t, d):
        tk = at(self, "KHAAS", 0.3, d)
        th = at(self, "HEATER", 0.55, d)
        tki = at(self, "KIT", 0.8, d)
        snowfield(ctx, t)
        warm = ease_out_cubic(clamp((t - tki) / 0.8))
        glow(ctx, 600, GROUND - 200, 500, FIRE, 0.35 * warm)
        k9(ctx, 600, GROUND - 20, 0.86, t, frost=1 - warm)
        if warm > 0:
            smoke(ctx, 600 - 0.86 * 250, GROUND - 0.86 * 130, t, warm)
        crate(ctx, 230, GROUND + 150, "OIL", (t - tk) / 0.5, GOLD)
        crate(ctx, 850, GROUND + 150, "HEATER", (t - th) / 0.5, FIRE)
        snow(ctx, t, n=50, k=1 - 0.6 * warm)


class Dagti(Cued):
    """Barrel elevates and fires; shell arcs with a 40 KM range bar; then new K9s roll out (+100)."""

    def events(self, d):
        return [(at(self, "GOLA", 0.4, d), "boom"), (at(self, "GOLA", 0.4, d) + 1.0, "thud"),
                (at(self, "100", 0.75, d), "kaching")]

    def draw(self, ctx, t, d):
        tg = at(self, "GOLA", 0.4, d)
        t1 = at(self, "AUR SENA", 0.7, d)
        if t < t1:
            snowfield(ctx, t)
            elev = 0.5 * ease_in_out(clamp(t / max(0.6, tg - 0.1)))
            rec = 40 * math.exp(-max(0.0, t - tg) * 8) if t >= tg else 0
            sh = 10 * math.exp(-max(0.0, t - tg) * 6) if t >= tg else 0
            ctx.save()
            ctx.translate(sh * math.sin(t * 70), 0)
            mz = k9(ctx, 260, GROUND - 20, 0.8, t, elev=elev, recoil=rec)
            u = clamp((t - tg) / 1.0)
            if t >= tg:
                flash(ctx, *mz, t - tg)
                smoke(ctx, mz[0], mz[1], t, 1 - u * 0.5)
                bx, by = lerp(mz[0], 1000, u), mz[1] - 420 * math.sin(math.pi * u) * 0.8 + 380 * u
                ang = math.atan2(-420 * math.pi * math.cos(math.pi * u) * 0.8 + 380, 1000 - mz[0])
                if u < 1:
                    ctx.save()
                    ctx.translate(bx, by)
                    ctx.rotate(ang)
                    rrect(ctx, -30, -10, 60, 20, 10)
                    rgba(ctx, GOLD)
                    ctx.fill()
                    ctx.restore()
                    glow(ctx, bx, by, 60, FIRE, 0.6)
                blast(ctx, 1000, mz[1] + 380, clamp((t - tg - 1.0) / 0.8))
                w = 860 * ease_out_cubic(clamp((t - tg) / 0.9))          # range bar
                line(ctx, [(110, 300), (110 + w, 300)], GOLD, 10)
                chip(ctx, "~40 KM", 540, 220, GOLD, (t - tg - 0.3) / 0.4, size=58)
            ctx.restore()
            return
        snowfield(ctx, t)
        for k in range(4):                                               # new guns roll in
            u = ease_out_cubic(clamp((t - t1 - 0.15 * k) / 0.8))
            k9(ctx, lerp(-120, 860 - 230 * k, u), GROUND - 20 - 90 * (k % 2), 0.46, t, roll=t * 5)
        chip(ctx, "+100", 540, 320, INDIA_GREEN, (t - at(self, "100", 0.75, d)) / 0.4, size=96)


class Debate(Cued):
    """Balance: Korean flag (design) vs tricolour (built in Hazira, Gujarat); the poll asks."""

    def events(self, d):
        return [(0.15, "tick"), (at(self, "GUJARAT", 0.4, d), "pop"), (at(self, "DESI", 0.75, d), "pop")]

    def draw(self, ctx, t, d):
        tq = at(self, "TO K9", 0.65, d)
        g = cairo.RadialGradient(540, 600, 60, 540, 600, 900)
        g.add_color_stop_rgb(0, *hexc("#2A3420"))
        g.add_color_stop_rgb(1, *hexc("#0A0E08"))
        ctx.set_source(g)
        ctx.rectangle(0, 0, W, H)
        ctx.fill()
        k9(ctx, 540, GROUND - 10, 0.7, t, elev=0.08)
        if t < tq + 0.2:
            ku = clamp(t / 0.4)
            gu = clamp((t - at(self, "GUJARAT", 0.4, d)) / 0.4)
            balance(ctx, 540, 380, 0.16 * math.sin(t * 2.2), t)
            if ku > 0:
                korea_flag(ctx, 90, 470, 260 * ku, 170 * ku)
                text(ctx, "DESIGN", 220, 690, 46, CYAN, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=8, a=ku)
            if gu > 0:
                flag(ctx, 730, 470, 260 * gu, 170 * gu, "in", t)
                text(ctx, "HAZIRA", 860, 690, 46, SAFFRON, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=8,
                     a=gu)
        lego.ending(sys.modules[__name__], ctx, t, t - tq, t - tq - 0.8, question=("K9 VAJRA", "DESI YA VIDESHI?"),
                    suggestions=("DESI", "VIDESHI"), y=600)


SCENE_CLASSES = {"hook": Hook, "tanav": Tanav, "thand": Thand, "kit": Kit, "dagti": Dagti, "debate": Debate}


def write_alignment(final: Path) -> None:
    out = [
        {"scene": spec["key"], "start": round(s["start"], 3), "dur": round(s["dur"], 3),
         "words": [{"t": round(s["start"] + st, 3), "w": w} for st, w in s["captions"]]}
        for spec, s in zip(SPEC, engine.SCENES)
    ]
    path = final.with_suffix(".json")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Alignment: {path}")


UPLOAD = {
    "titles": [
        "Registan Ki Top Ladakh Ki Barf Mein Kyun? K9 Vajra Ka Sach #shorts",
        "K9 Vajra: Desi Ya Videshi? Korea Ka Design, Gujarat Mein Bani #shorts",
        "China Ke Saamne Khadi Ye Top Registan Ke Liye Bani Thi #shorts",
    ],
    "title": "Registan Ki Top Ladakh Ki Barf Mein Kyun? K9 Vajra Ka Sach #shorts",
    "thumb_text": "REGISTAN SE BARF?",
    "queries": ["k9 vajra", "k9 vajra ladakh", "k9 vajra desi ya videshi"],
    "description": """K9 Vajra ka sach: ye top registan ke liye bani thi, par aaj Ladakh ki barf mein China ke saamne khadi hai. Kaise aur kyun?

Is Short mein:
- K9 Vajra-T: 155 mm tracked self-propelled gun, Korea ki Hanwha K9 Thunder ka Indian version
- L&T ise Hazira (Gujarat) mein banata hai; pehli 100 top 2017 ke order se aayi
- 2020 ke India-China standoff ke baad ise Ladakh ke liye taiyaar kiya gaya
- Thand mein tel na jame, isliye winterisation kit: khaas oil/lubricant aur heating system
- Range lagbhag 40 km (alag sources 38-40 km batate hain)
- Dec 2024: Raksha Mantralaya ne L&T se 100 aur K9 Vajra ka Rs 7,629 crore ka sauda kiya

Debate: design Korea ka, banti Gujarat mein - to K9 Vajra desi hai ya videshi? Apna jawab comment mein likho.

Sources:
- L&T: K9 Vajra-T 155 mm / 52 cal SP gun
- Business Standard (20 Dec 2024): MoD signs Rs 7,629 cr deal with L&T
- Janes: L&T completes deliveries of K9 Vajra-T
- ThePrint: Army to order another 100 K9 Vajra
""",
    "tags": ["k9 vajra", "k9 vajra ladakh", "k9 vajra howitzer", "indian army artillery", "self propelled gun",
             "l&t defence", "hazira", "make in india defence", "ladakh", "lac", "k9 thunder", "reality shift",
             "defence shorts", "indian army"],
    "hashtags": ["#Shorts", "#K9Vajra", "#IndianArmy"],
    "pinned_comment": "Design Korea ka, banti Gujarat mein - K9 Vajra desi hai ya videshi? 🤔 Apna jawab likho 👇 "
                      "(DESI / VIDESHI)",
}


def thumbnail(ctx):
    snowfield(ctx, 1.0)
    k9(ctx, 500, GROUND - 20, 1.05, 1.0, elev=0.35, frost=1.0)
    snow(ctx, 1.0, n=80)
    text(ctx, "REGISTAN KI TOP", 540, 205, 100, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "LADAKH MEIN?", 540, 330, 120, CYAN, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=20)
    text(ctx, "K9 VAJRA", 540, 1330, 130, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, PAL["ui"], a=0.85)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.k9_vajra")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    total = sum(s["dur"] for s in engine.SCENES)
    write_alignment(final)
    upload_kit.build(story, final, total)
    if total > MAX_SECONDS:
        raise SystemExit(f"[length] {total:.1f}s is over the {MAX_SECONDS:.0f}s lock")


if __name__ == "__main__":
    main()
