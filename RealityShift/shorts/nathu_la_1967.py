"""Reality Shift Short: 1967 Nathu La Clash - Maj Gen Sagat Singh's artillery response.

Facts (see SOURCES): In September 1967 at Nathu La pass (Sikkim), Indian troops laying a wire fence faced sudden
Chinese gunfire; Maj Gen Sagat Singh ordered heavy Indian artillery fire that destroyed Chinese bunkers at the pass.
After 1967, the Sikkim border remained quiet for decades.
"""

import importlib
import math
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cairo

from core import delivery, engine, lego  # noqa: F401
from core.engine import *  # noqa: F401,F403
from shorts.chabahar import Cued
from shorts.haji_pir import chip, stamp

TOPIC = "1967 NATHU LA CLASH INDIA CHINA ARTILLERY"
OUTPUTS = {"edge": "nathu_la_1967_short.mp4"}
LEGO = {"header": "radar", "caption": "speech", "transition": "shutter", "palette": "khaki", "ending": "poll"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.45
TAIL_PAD = 0.35
TRIM = {"thresh": 0.006, "keep": 0.04, "keep_tail": 0.06}
MUSIC_BPM = 90
MUSIC_STYLE = "tension"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+12%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 0
MAX_SECONDS = 35.0

PAL = lego.PALETTES["khaki"]
SAFFRON = hexc("#FF9933")
INDIA_GREEN = hexc("#138808")
WHITE = (1.0, 1.0, 1.0)
GOLD = hexc("#FFD166")
RED = hexc("#E2483A")
CYAN = hexc("#5FD3FF")
FIRE = hexc("#FF6A1A")
OLIVE = hexc("#566442")

SOURCES = [
    "Wikipedia - Nathu La and Cho La clashes (1967): "
    "https://en.wikipedia.org/wiki/Nathu_La_and_Cho_La_clashes",
    "Wikipedia - Sagat Singh: https://en.wikipedia.org/wiki/Sagat_Singh",
]

# Script v2 (26 Nov, user-approved after a KikiVoice test): tension builds line by line and the artillery order is
# the last story beat (AGENTS.md #2, #18). The last line loops into the first ("...शुरू हुआ था जब" -> "सीमा पर...").
SPEC = [
    {"key": "hook", "accent": CYAN, "text": "",
     "visual": "Indian soldiers laying a wire fence on the snowy pass; an enemy bunker glows on the ridge",
     "vo": [("hook", [("सीमा पर बस एक तार", "SEEMA PAR BAS EK TAAR"),
                      ("लगाया जा रहा था।", "LAGAYA JA RAHA THA.")])]},
    {"key": "fire", "accent": RED, "text": "",
     "visual": "Red tracers from the bunker hit the wire line; soldiers duck",
     "vo": [("build", [("और उसी तार पर", "AUR USI TAAR PAR"),
                       ("चीन ने गोलियां चला दीं।", "CHINA NE GOLIYAN CHALA DEEN.")])]},
    {"key": "open", "accent": RED, "text": "",
     "visual": "Wide empty snowfield: soldiers exposed, no cover anywhere, tracers overhead",
     "vo": [("build", [("हमारे जवान खुले मैदान में थे", "HAMARE JAWAN KHULE MAIDAN MEIN THE"),
                       ("ना कोई बंकर ना कोई आड़।", "NA KOI BUNKER NA KOI AAD.")])]},
    {"key": "fall", "accent": RED, "text": "",
     "visual": "Soldiers go down one after another in the snow (no blood, respectful)",
     "vo": [("build", [("एक के बाद एक", "EK KE BAAD EK"),
                       ("जवान गिरने लगे।", "JAWAN GIRNE LAGE.")])]},
    {"key": "sagat", "accent": SAFFRON, "text": "",
     "visual": "Every soldier turns to one officer on the ridge: Maj Gen Sagat Singh with binoculars",
     "vo": [("tell", [("अब सबकी नजर", "AB SABKI NAZAR"),
                      ("एक आदमी पर थी।", "EK AADMI PAR THI.")]),
            ("punch", [("मेजर जनरल सगत सिंह।", "MAJOR GENERAL SAGAT SINGH.")])]},
    {"key": "faisla", "accent": SAFFRON, "text": "",
     "visual": "Close on the officer, silent guns behind him; he raises his arm on HUKM",
     "vo": [("tell", [("उनके सामने एक ऐसा फैसला था", "UNKE SAAMNE EK AISA FAISLA THA"),
                      ("जो आसान नहीं था।", "JO AASAN NAHIN THA.")]),
            ("build", [("और फिर उन्होंने", "AUR PHIR UNHONE"),
                       ("वो हुक्म दे दिया।", "WO HUKM DE DIYA.")])]},
    {"key": "tope", "accent": FIRE, "text": "",
     "visual": "A row of Indian field guns fires together on DO: muzzle flash and recoil",
     "vo": [("punch", [("तोपें खोल दो।", "TOPEIN KHOL DO.")])]},
    {"key": "boom", "accent": FIRE, "text": "",
     "visual": "Shells arc over the pass and the enemy bunkers blow up one by one",
     "vo": [("punch", [("दुश्मन के बंकर", "DUSHMAN KE BUNKER"),
                       ("एक एक करके उड़ गए।", "EK EK KARKE UD GAYE.")])]},
    {"key": "end", "accent": CYAN, "text": "",
     "visual": "Calm again: the wire fence on the pass, same framing as the first frame (loop)",
     "vo": [("tell", [("और ये सब शुरू हुआ था जब", "AUR YE SAB SHURU HUA THA JAB")])]},
]

DELIVERY = delivery.build(SPEC)
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}
HOT = {
    "TAAR": CYAN, "CHINA": RED, "GOLIYAN": RED, "MAIDAN": GOLD, "BUNKER": FIRE, "GIRNE": RED,
    "SAGAT": GOLD, "SINGH.": GOLD, "FAISLA": SAFFRON, "HUKM": SAFFRON, "TOPEIN": FIRE, "KHOL": FIRE,
    "UD": FIRE,
}


def smooth(ctx, pts, k=0.2):
    ctx.move_to(*pts[0])
    for x, y in pts[1:]:
        ctx.line_to(x, y)
    ctx.close_path()


def mountain_bg(ctx, t, flash=0.0):
    g = cairo.LinearGradient(0, 0, 0, 1100)
    g.add_color_stop_rgb(0, *hexc("#0E1828"))
    g.add_color_stop_rgb(1, *hexc("#2B4160"))
    ctx.set_source(g)
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    if flash > 0:
        glow(ctx, 760, 780, 380, FIRE, 0.55 * flash)
    # Distant snow peaks
    smooth(ctx, [(0, 960), (210, 560), (460, 820), (760, 520), (1080, 920), (1080, H), (0, H)], k=0.1)
    rgba(ctx, hexc("#1E2C40"))
    ctx.fill()
    # Snow caps
    for px, py in ((210, 560), (760, 520)):
        smooth(ctx, [(px, py), (px - 75, py + 95), (px + 75, py + 95)], k=0.1)
        rgba(ctx, WHITE, 0.35)
        ctx.fill()
    # Foreground ridge
    smooth(ctx, [(0, 1140), (340, 940), (700, 1020), (1080, 880), (1080, H), (0, H)], k=0.15)
    rgba(ctx, hexc("#121B28"))
    ctx.fill()


def soldier(ctx, x, y, s, pose="stand", fall=0.0, arm=0.0, crouch=0.0, fall_dir=-1):
    """pose: stand | wire | officer. fall 0..1 tips him over at the feet (no blood; fall_dir -1 = left,
    1 = right); arm 0..1 raises the right arm (the order); crouch 0..1 ducks."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s * (1 - 0.3 * crouch))
    if fall > 0:
        ctx.rotate(fall_dir * math.pi / 2 * ease_out_cubic(clamp(fall)))
    if pose == "officer":
        rrect(ctx, -24, -120, 20, 120, 6)
        rgba(ctx, OLIVE)
        ctx.fill()
        rrect(ctx, 4, -120, 20, 120, 6)
        rgba(ctx, OLIVE)
        ctx.fill()
        rrect(ctx, -32, -230, 64, 115, 10)
        rgba(ctx, hexc("#5B6A45"))
        ctx.fill()
        circle(ctx, 0, -262, 26, hexc("#D8A478"))
        rrect(ctx, -30, -300, 60, 22, 6)                         # peaked cap with red band (general officer)
        rgba(ctx, hexc("#4A5636"))
        ctx.fill()
        rrect(ctx, -30, -284, 60, 7, 2)
        rgba(ctx, RED)
        ctx.fill()
        a = math.radians(75 - 190 * ease_out_cubic(clamp(arm)))  # 75 deg = hanging down, -115 deg = raised
        line(ctx, [(24, -215), (24 + 95 * math.cos(a), -215 + 95 * math.sin(a))], hexc("#5B6A45"), 16)
        ctx.restore()
        return
    # Legs
    rrect(ctx, -24, -120, 20, 120, 6)
    rgba(ctx, OLIVE)
    ctx.fill()
    rrect(ctx, 4, -120, 20, 120, 6)
    rgba(ctx, OLIVE)
    ctx.fill()
    # Jacket
    rrect(ctx, -32, -230, 64, 115, 10)
    rgba(ctx, hexc("#66764E"))
    ctx.fill()
    # Helmet & face
    circle(ctx, 0, -262, 26, hexc("#D8A478"))
    smooth(ctx, [(-30, -268), (0, -304), (30, -268)], k=0.25)
    rgba(ctx, hexc("#3B472D"))
    ctx.fill()
    if pose == "wire":
        line(ctx, [(22, -210), (75, -185)], OLIVE, 14)
    ctx.restore()


def howitzer(ctx, x, y, s, t, recoil=0.0):
    """Detailed Indian artillery field gun with gun shield, heavy wheel, barrel, and breech."""
    ctx.save()
    ctx.translate(x - 22 * recoil, y)
    ctx.scale(s, s)
    # Barrel + muzzle brake
    line(ctx, [(-45, -15), (155, -120)], hexc("#7A8862"), 24)
    rrect(ctx, 140, -135, 32, 32, 4)
    rgba(ctx, hexc("#4A543B"))
    ctx.fill()
    # Gun shield
    smooth(ctx, [(5, -95), (38, -95), (28, 12), (-8, 12)], k=0.05)
    rgba(ctx, OLIVE)
    ctx.fill()
    # Trail spade
    line(ctx, [(-155, 35), (-35, -5)], hexc("#4C583E"), 20)
    # Large artillery wheel
    circle(ctx, -12, 16, 46, hexc("#252B1E"))
    circle(ctx, -12, 16, 22, hexc("#6E7A58"))
    ctx.restore()


def bunker(ctx, x, y, s, hit=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -110, -70, 220, 70, 12)
    rgba(ctx, hexc("#444A54"))
    ctx.fill()
    rrect(ctx, -65, -45, 130, 18, 4)
    rgba(ctx, hexc("#14181E"))
    ctx.fill()
    if hit > 0:
        glow(ctx, 0, -55, 200 * hit, FIRE, 0.9)
        circle(ctx, 0, -65, 62 * hit, FIRE, 0.85)
    ctx.restore()


def wire_fence(ctx, grow=1.0):
    """Posts + three strands of wire, laid left to right as grow goes 0 -> 1."""
    posts = (180, 400, 620, 840)
    xe = lerp(180, 900, clamp(grow))
    for px in posts:
        if px <= xe + 1:
            line(ctx, [(px, 1060), (px, 870)], hexc("#A8B4C0"), 10)
    for wy in (905, 960, 1015):
        line(ctx, [(180, wy), (xe, wy)], WHITE, 4, 0.75)


def tracers(ctx, t, n=4, speed=2.4, x0=740, y0=850, x1=180, y1=1030):
    for k in range(n):
        u = (t * speed + k / n) % 1.0
        sx, sy = lerp(x0, x1, u), lerp(y0, y1, u)
        line(ctx, [(sx + 65, sy - 14), (sx, sy)], RED, 8, 0.9)


def enemy_bunker(ctx, t, glow_a=0.35):
    """The Chinese post on the ridge, its slit glowing (menace before the first shot)."""
    bunker(ctx, 810, 870, 0.95)
    glow(ctx, 810, 840, 120, RED, glow_a * (0.75 + 0.25 * math.sin(t * 5)))


class Hook(Cued):
    """Line 1 - first frame = the quiet pass and the wire (the loop lands here again)."""
    def events(self, d):
        return [(0.15, "tick")]

    def draw(self, ctx, t, d):
        mountain_bg(ctx, t)
        enemy_bunker(ctx, t, 0.25 + 0.25 * clamp(t / d))
        wire_fence(ctx, 0.55 + 0.45 * clamp(t / d))
        soldier(ctx, 300, 1060, 1.1, pose="wire")
        soldier(ctx, 560, 1060, 1.1, pose="wire")


class Fire(Cued):
    """Line 2 - the shots come exactly on GOLIYAN; the soldiers duck."""
    def beats(self, d):
        return {"shot": self.cue("GOLIYAN", d * 0.45)}

    def events(self, d):
        return [(self.beats(d)["shot"], "zap")]

    def draw(self, ctx, t, d):
        shot = self.beats(d)["shot"]
        u = clamp((t - shot) / 0.25)
        mountain_bg(ctx, t, flash=0.35 * u)
        enemy_bunker(ctx, t, 0.4 + 0.5 * u)
        wire_fence(ctx)
        if u > 0:
            tracers(ctx, t - shot)
        soldier(ctx, 300, 1060, 1.1, pose="wire", crouch=u)
        soldier(ctx, 560, 1060, 1.1, pose="wire", crouch=u)


class Open(Cued):
    """Line 3 - pull back: a wide empty snowfield, nowhere to hide."""
    def events(self, d):
        return [(0.1, "whoosh")]

    def draw(self, ctx, t, d):
        z = 1.18 - 0.18 * ease_out_cubic(clamp(t / d))          # slow pull-back = exposure (never below 1: no borders)
        ctx.save()
        ctx.translate(540, 960)
        ctx.scale(z, z)
        ctx.translate(-540, -960)
        mountain_bg(ctx, t, flash=0.2)
        rrect(ctx, -200, 1060, 1480, 600, 0)                     # bare snow, no cover anywhere
        rgba(ctx, hexc("#C9D4E0"), 0.18)
        ctx.fill()
        enemy_bunker(ctx, t, 0.7)
        tracers(ctx, t, n=6, speed=2.0, x1=60, y1=860)
        for i, x in enumerate((220, 430, 640, 850)):
            soldier(ctx, x, 1100, 0.9, pose="stand", crouch=0.35 + 0.1 * math.sin(t * 3 + i))
        ctx.restore()


class Fall(Cued):
    """Line 4 - one after another they go down (respectful: no blood, no wounds)."""
    XS = (150, 450, 750)            # 300 px apart: a fallen soldier (~240 px) never lies on the next one

    def times(self, d):
        return [0.15 * d + i * 0.22 * d for i in range(len(self.XS))]

    def events(self, d):
        return [(tt, "soft_thud") for tt in self.times(d)]

    def draw(self, ctx, t, d):
        mountain_bg(ctx, t, flash=0.25)
        enemy_bunker(ctx, t, 0.7)
        tracers(ctx, t, n=5, speed=2.2, x1=120, y1=1000)
        for x, tt in zip(self.XS, self.times(d)):
            soldier(ctx, x, 1100, 0.8, fall=(t - tt) / 0.45, fall_dir=1)


class Sagat(Cued):
    """Lines 5-6 - every soldier turns to one man: the officer with binoculars on the ridge."""
    def events(self, d):
        return [(self.cue("SAGAT", d * 0.6), "soft_thud")]

    def draw(self, ctx, t, d):
        mountain_bg(ctx, t, flash=0.15)
        glow(ctx, 540, 820, 330, GOLD, 0.25 * clamp(t / 0.8))   # spotlight on him
        soldier(ctx, 540, 1060, 1.35, pose="officer", arm=0.0)   # arm stays down until the order (Faisla)
        for x in (150, 300, 780, 930):                            # soldiers looking at him
            soldier(ctx, x, 1120, 0.8, crouch=0.2)


class Faisla(Cued):
    """Lines 7-8 - silence, guns waiting; the arm goes up on HUKM."""
    def beats(self, d):
        return {"hukm": self.cue("HUKM", d * 0.75)}

    def events(self, d):
        return [(0.2, "tick"), (self.beats(d)["hukm"], "soft_thud")]

    def draw(self, ctx, t, d):
        hukm = self.beats(d)["hukm"]
        mountain_bg(ctx, t)
        howitzer(ctx, 760, 1040, 1.2, t)
        z = 1.0 + 0.12 * clamp(t / d)                              # slow push-in = tension
        ctx.save()
        ctx.translate(380, 1060)
        ctx.scale(z, z)
        ctx.translate(-380, -1060)
        soldier(ctx, 380, 1060, 1.45, pose="officer", arm=clamp((t - hukm) / 0.35))
        ctx.restore()


class Tope(Cued):
    """Line 9 - 'तोपें खोल दो': the whole battery fires together on DO."""
    def beats(self, d):
        return {"fire": self.cue("DO", d * 0.7)}

    def events(self, d):
        return [(self.beats(d)["fire"], "boom")]

    def draw(self, ctx, t, d):
        f = self.beats(d)["fire"]
        since = t - f
        flash = math.exp(-max(0.0, since) * 3) if since >= 0 else 0.0
        mountain_bg(ctx, t, flash=flash)
        for i, x in enumerate((180, 470, 760)):
            rec = math.exp(-since * 5) if since >= 0 else 0.0
            howitzer(ctx, x, 1040 + 30 * i, 1.0, t, recoil=rec)
            if flash > 0.05:
                glow(ctx, x + 165, 1040 + 30 * i - 125, 90, FIRE, flash)


class Boom(Cued):
    """Line 10 - shells arc over the pass; the bunkers go up one by one ('एक एक करके')."""
    BX = ((640, 900), (800, 860), (960, 900))

    def times(self, d):
        return [0.2 * d + i * 0.22 * d for i in range(len(self.BX))]

    def events(self, d):
        return [(0.05, "whoosh")] + [(tt, "boom") for tt in self.times(d)]

    def draw(self, ctx, t, d):
        hits = [clamp((t - tt + 0.15) / 0.5) for tt in self.times(d)]
        mountain_bg(ctx, t, flash=max(hits))
        for (bx, by), h, tt in zip(self.BX, hits, self.times(d)):
            bunker(ctx, bx, by, 0.75, hit=h)
            u = clamp((t - (tt - 0.45)) / 0.45)
            if 0 < u < 1:
                x, y = lerp(200, bx, u), lerp(1000, by - 40, u) - 260 * math.sin(u * math.pi)
                circle(ctx, x, y, 9, GOLD)


class End(Cued):
    """Line 11 - calm again on the wire, same framing as the first frame, so the loop is seamless."""
    def events(self, d):
        return [(0.2, "shimmer")]

    def draw(self, ctx, t, d):
        mountain_bg(ctx, t)
        enemy_bunker(ctx, t, 0.25 * clamp(t / d))
        wire_fence(ctx, 0.55 * clamp(t / d))
        soldier(ctx, 300, 1060, 1.1, pose="wire")
        soldier(ctx, 560, 1060, 1.1, pose="wire")


SCENE_CLASSES = {"hook": Hook, "fire": Fire, "open": Open, "fall": Fall, "sagat": Sagat,
                 "faisla": Faisla, "tope": Tope, "boom": Boom, "end": End}

UPLOAD = {
    "titles": [
        "China Ne Goli Chalayi... Phir Aaya Hukm: Topein Khol Do #shorts",
        "Maj Gen Sagat Singh Ka Wo Faisla... Jo Aasan Nahi Tha #shorts",
        "1967 Nathu La: Jab Indian Artillery Ne China Ke Bunkers Udaye #shorts",
    ],
    "thumb_text": "NATHU LA 1967",
    "queries": ["nathu la 1967", "sagat singh", "india china 1967"],
    "description": """1967 mein Sikkim ke Nathu La par tar laga rahe Indian jawanon par achanak firing hui. Jawan khule
maidan mein the, tab Maj Gen Sagat Singh ne Indian artillery se seedha jawab diya aur dushman ke bunker ud gaye.

Debate: 1967 mein China ko peeche hatane ka sabse bada kaaran kya tha - jawanon ka jigar ya artillery ka jawab?

Sources:
- Wikipedia: Nathu La and Cho La clashes (1967)
- Wikipedia: Sagat Singh
""",
    "tags": ["nathu la 1967", "sagat singh", "india china 1967", "indian army", "indian artillery",
             "sikkim border", "reality shift", "defence shorts", "military history"],
    "hashtags": ["#Shorts", "#IndianArmy", "#NathuLa1967"],
    "pinned_comment": "1967 Nathu La jeet ka sabse bada turning point kya tha - jawanon ka JIGAR ya Sagat Singh ki "
                      "ARTILLERY ka faisla? Apni raay comments mein likhein! 🇮🇳🫡",
}


def thumbnail(ctx):
    mountain_bg(ctx, 0.5, flash=0.9)
    howitzer(ctx, 270, 1020, 1.45, 0.5)
    bunker(ctx, 790, 880, 1.2, hit=1.0)
    text(ctx, "1967 CLASH", 540, 210, 118, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=16)
    text(ctx, "BUNKERS UDAYE", 540, 340, 110, WHITE, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "NATHU LA", 540, 1340, 120, SAFFRON, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, PAL["ui"], a=0.85)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.nathu_la_1967")
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
