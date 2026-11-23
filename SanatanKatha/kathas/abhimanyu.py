"""Abhimanyu Chakravyuh: 16 saal ke veer balak ki katha (22s loop katha, 6 scenes).

Angle: 16-year-old Abhimanyu penetrated the Chakravyuh alone. The seven Maharathis of Kauravas
grew terrified of the young lion and conspired in adharma: severing his bow from behind.
Even with bow and chariot shattered, Abhimanyu hoisted a heavy chariot wheel and fought
to his last breath, never surrendering.
The final phrase "...TABHI TO" loops seamlessly back into "SAAT MAHARATHI... EK SOLAH SAAL KE BAALAK SE, DAR GAYE THE!".
"""

import math
import cairo

from core.katha import *  # noqa: F401,F403
import core.devta as dv
from core.devta import ell, gem, hand, ink, limb, sheen, smooth, eye, palm, rrect, line, lerp, clamp, ease_out_cubic, ease_out_back, rnd
from kathas.ghatotkach_akshauhini import duryodhan, gada, soldier, kaurava_mob

TOPIC = "CHAKRAVYUH SAAT DARWAZE ABHIMANYU"
OUTPUTS = {"edge": "abhimanyu_short.mp4", "files": "abhimanyu_short.mp4"}
MUSIC_STYLE = "tension"    # War tension & Chakravyuh siege
MUSIC_BPM = 84             # Pacing 84 BPM (strictly within 80-92 range, distinct from ghatotkach 90)
MUSIC_VOLUME = 0.12
TAIL_PAD = 0.04
MAX_GAP = 0.04
KIKI_PAUSE_MS = 150

# Distinct palettes per character_design.md
FIRE_O = hexc("#FF6A1A")
FIRE_Y = hexc("#FFD24A")
GOLD_HI = dv.GOLD_HI
VASAVI = hexc("#FFF1A8")
ABHI_SKIN = hexc("#E0A572")   # Youthful golden-wheatish
ABHI_DHOTI = hexc("#F5F5FA")  # Pure white silk with gold hem
ABHI_ARMOR = hexc("#E8A824")  # Radiant golden armour
DRONA_SKIN = hexc("#CFA07A")  # Venerable aged warrior sage
DRONA_BEARD = hexc("#F0EDE6") # Pure white beard and ascetic matted hair
DRONA_ROBE = hexc("#D96E28")  # Saffron sage wrap
DUR_ARMOR = hexc("#3B1C5C")   # Purple-maroon Kaurava armor
DUR_SKIN = hexc("#D29A68")
WHEEL_WOOD = hexc("#5A3618")  # Weathered teak
WHEEL_IRON = hexc("#2D3138")  # Studded iron rim

SOURCES = [
    "Mahabharata, Drona Parva (Abhimanyu-badha Parva, KM Ganguli trans. sections 31-49): 16-year-old Abhimanyu "
    "breaches the impenetrable Chakravyuh alone, throwing the Kaurava army into widespread panic and retreat.",
    "Mahabharata, Drona Parva (section 48): Unable to defeat the youth in direct single combat, Dronacharya "
    "instructs Karna to sever Abhimanyu's bow from behind, violating all sacred warrior codes (Dharma-yuddha).",
    "Mahabharata, Drona Parva (section 49): Disarmed and chariot shattered, Abhimanyu heaves a massive chariot wheel "
    "and fights seven Maharathis to his final breath until he attains supreme Veergati.",
]

SPEC = [
    {"key": "hook", "text": "SAAT MAHARATHI... EK BAALAK",
     "visual": "Seven Maharathis stepping back in fear and hesitation around 16-year-old Abhimanyu at center",
     "vo": [("punch", [("सात महारथी...", "SAAT MAHARATHI..."),
                       ("एक सोलह साल के", "EK SOLAH SAAL KE"),
                       ("बालक से, डर गए थे!", "BAALAK SE, DAR GAYE THE!")], 0.04)]},
    {"key": "ghus", "text": "CHAKRAVYUH KE SAATON DARWAZE",
     "visual": "Abhimanyu enters and breaches the rotating 7-tier Chakravyuh; Kaurava soldiers scatter in panic",
     "vo": [("build", [("चक्रव्यूह के सातों दरवाज़े,", "CHAKRAVYUH KE SAATON DARWAZE,"),
                       ("अभिमन्यु भेदता गया...", "ABHIMANYU BHEDTA GAYA..."),
                       ("कौरव सेना बिखर गई।", "KAURAV SENA BIKHAR GAYI.")], 0.04)]},
    {"key": "dhanush", "text": "YUDDHA KA NIYAM TODA",
     "visual": "Drona commands Karna from behind; treacherous arrow shatters Abhimanyu's bow, violating warrior code",
     "vo": [("fast", [("द्रोण ने युद्ध नियम तोड़ा...", "DRONA NE YUDDHA NIYAM TODA..."),
                       ("बोले, कर्ण... पीछे से", "BOLE, KARNA... PEECHHE SE"),
                       ("धनुष काटो!", "DHANUSH KAATO!")], 0.04)]},
    {"key": "pahiya", "text": "RATH KA PAHIYA UTHA LIYA",
     "visual": "Chariot shattered; Abhimanyu heaves a massive iron-studded chariot wheel overhead with blazing resolve",
     "vo": [("punch", [("धनुष टूटा, रथ टूटा...", "DHANUSH TOOTA, RATH TOOTA..."),
                       ("तो उसने रथ का", "TO USNE RATH KA"),
                       ("पहिया उठा लिया!", "PAHIYA UTHA LIYA!")], 0.04)]},
    {"key": "akela", "text": "LADTA RAHA AAKHIRI SAANS TAK",
     "visual": "Seven surround the unarmed hero tightly; Abhimanyu fights valiantly, then peaceful veergati with floral rain",
     "vo": [("tell", [("सातों ने निहत्थे", "SAATON NE NIHATTHE"),
                       ("बालक को घेरा...", "BAALAK KO GHERA..."),
                       ("वो लड़ा,", "WO LADA,"),
                       ("आखिरी साँस तक।", "AAKHIRI SAANS TAK.")], 0.04)]},
    {"key": "loop", "text": "JHUKNA NAHIN... TABHI TO",
     "visual": "Solitary Abhimanyu looks back at the sealed labyrinth; seamless crossfade into frame 0 opening",
     "vo": [("awe", [("उसे निकलना", "USE NIKALNA"),
                     ("नहीं आता था...", "NAHIN AATA THA..."),
                     ("पर झुकना भी नहीं।", "PAR JHUKNA BHI NAHIN."),
                     ("तभी तो", "TABHI TO")], 0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "SAAT": FIRE_O, "MAHARATHI...": hexc("#FF5555"), "SOLAH": GOLD_HI, "SAAL": GOLD_HI,
    "BAALAK": FIRE_Y, "DAR": hexc("#FF5555"), "GAYE": hexc("#FF5555"), "THE!": hexc("#FF5555"),
    "CHAKRAVYUH": hexc("#FF5555"), "SAATON": FIRE_Y, "DARWAZE,": FIRE_Y, "ABHIMANYU": FIRE_Y,
    "BHEDTA": FIRE_O, "GAYA...": FIRE_O, "KAURAV": hexc("#82C4FF"), "SENA": hexc("#82C4FF"),
    "BIKHAR": FIRE_O, "GAYI.": FIRE_O, "DRONA": dv.GOLD, "YUDDHA": hexc("#FF5555"), "NIYAM": hexc("#FF5555"),
    "TODA...": hexc("#FF5555"), "BOLE,": dv.GOLD, "KARNA...": GOLD_HI, "PEECHHE": FIRE_O,
    "DHANUSH": GOLD_HI, "KAATO!": hexc("#FF5555"), "TOOTA,": hexc("#FF5555"), "TOOTA...": hexc("#FF5555"),
    "RATH": FIRE_O, "PAHIYA": FIRE_Y, "UTHA": FIRE_Y, "LIYA!": FIRE_Y, "SAATON": FIRE_O,
    "NIHATTHE": hexc("#FF5555"), "GHERA...": FIRE_O, "LADA,": FIRE_Y, "SAANS": GOLD_HI, "TAK.": GOLD_HI,
    "NIKALNA": hexc("#FF5555"), "NAHIN": hexc("#FF5555"), "AATA": hexc("#FF5555"), "THA...": hexc("#FF5555"),
    "JHUKNA": FIRE_Y, "BHI": FIRE_Y, "TABHI": GOLD_HI, "TO": GOLD_HI,
})

def ease_in(u):
    u = clamp(u)
    return u * u * u

# ============================================================ Background Environments

def kurukshetra_day(ctx, t, haze=1.0):
    """Daytime Kurukshetra dust sky: golden-ochre to amber dust, distant banners and hills."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in ((0.0, "#3D1A10"), (0.35, "#7A3518"), (0.60, "#C96A2C"), (0.78, "#8A4520"), (1.0, "#2A150D")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.paint()
    
    # Golden sun burning through battlefield dust
    glow(ctx, 540, 320, 260, GOLD_HI, 0.45 * haze)
    ell(ctx, 540, 320, 48, 48)
    ink(ctx, dv.WHITE, 0.85)
    
    # Layered distant dust hills
    for idx, (hy, col) in enumerate(((780, "#28120A"), (920, "#1F0C06"), (GROUND, "#150804"))):
        smooth(ctx, [
            (0, hy), (260, hy - 40 - 15 * idx), (560, hy + 30), (840, hy - 35), (W, hy),
            (W, H), (0, H)
        ], closed=True)
        ink(ctx, hexc(col))
        
    # Floating ash & war particles
    for p in range(16):
        px = (p * 68 + int(t * 35)) % W
        py = (320 + p * 52 - int(t * 22)) % (GROUND - 80)
        ctx.arc(px, py, 2.2, 0, math.tau)
        rgba(ctx, hexc("#FFE8B0"), 0.35)
        ctx.fill()

def siege_red_sky(ctx, t):
    """Ominous crimson-blood battlefield sunset sky for the unjust siege."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in ((0.0, "#2A060A"), (0.35, "#5E1117"), (0.65, "#96231C"), (0.85, "#420F12"), (1.0, "#180507")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.paint()
    
    # Smoldering war sun
    glow(ctx, 540, 360, 320, hexc("#FF2A1A"), 0.55)
    ell(ctx, 540, 360, 56, 56)
    ink(ctx, hexc("#FFB588"), 0.9)
    
    # Dark silhouettes of jagged Kurukshetra terrain
    smooth(ctx, [(0, 840), (320, 780), (680, 850), (920, 800), (W, 830), (W, H), (0, H)], closed=True)
    ink(ctx, hexc("#1C0608"))
    smooth(ctx, [(0, GROUND - 30), (420, GROUND - 60), (780, GROUND - 20), (W, GROUND - 40), (W, H), (0, H)], closed=True)
    ink(ctx, hexc("#100304"))

# ============================================================ Procedural Props & Formations

def chakravyuh_formation(ctx, cx, cy, r_max, t, broken=False):
    """Dynamic procedural 7-tier rotating spiral labyrinth of the military Chakravyuh."""
    ctx.save()
    ctx.translate(cx, cy)
    n_tiers = 7
    for tier in range(1, n_tiers + 1):
        r = r_max * (tier / n_tiers)
        speed = 0.12 * (1.0 if tier % 2 == 1 else -0.8)
        ang_offset = t * speed + tier * 0.4
        
        ctx.arc(0, 0, r, 0, math.tau)
        ctx.set_line_width(4.5 if tier < 7 else 8.0)
        rgba(ctx, FIRE_O if tier == 7 else hexc("#C97034"), 0.45)
        ctx.stroke()
        
        # Rotating defensive phalanxes (shield & spear units along each tier ring)
        n_units = 6 + tier * 3
        for u in range(n_units):
            th = ang_offset + u * (math.tau / n_units)
            if broken and tier <= 4 and (abs(th % math.tau - 1.2) < 0.6):
                continue
            ux = r * math.cos(th)
            uy = r * math.sin(th) * 0.42 # Perspective squash
            
            ctx.save()
            ctx.translate(ux, uy)
            ctx.rotate(th + math.pi / 2)
            smooth(ctx, [(-9, -14), (9, -14), (6, 12), (-6, 12)], closed=True)
            ink(ctx, hexc("#4A2016"))
            line(ctx, [(0, 10), (0, -28)], dv.OUTLINE, 3)
            ctx.restore()
    ctx.restore()

def chariot_wheel(ctx, x, y, r, ang=0.0, broken=False):
    """Massive, heavy wooden & iron-studded Kurukshetra chariot wheel wielded by Abhimanyu."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    
    # Outer studded iron rim
    ctx.arc(0, 0, r, 0, math.tau)
    ctx.set_line_width(28)
    ink(ctx, WHEEL_IRON)
    ctx.stroke()
    
    # Wooden interior rim
    ctx.arc(0, 0, r - 14, 0, math.tau)
    ctx.set_line_width(18)
    ink(ctx, WHEEL_WOOD)
    ctx.stroke()
    
    # Heavy teak spokes
    n_spokes = 12
    for s in range(n_spokes):
        th = s * (math.tau / n_spokes)
        if broken and (s in (2, 3)):
            continue
        sx = (r - 20) * math.cos(th)
        sy = (r - 20) * math.sin(th)
        line(ctx, [(0, 0), (sx, sy)], WHEEL_WOOD, 11)
        line(ctx, [(0, 0), (sx, sy)], hexc("#381F0D"), 3)
        
    # Central heavy iron axle hub
    ell(ctx, 0, 0, 36, 36)
    ink(ctx, WHEEL_IRON)
    ell(ctx, 0, 0, 20, 20)
    ink(ctx, hexc("#8A5A2B"))
    
    # Iron perimeter studs
    for st in range(16):
        sth = st * (math.tau / 16)
        px = r * math.cos(sth)
        py = r * math.sin(sth)
        ctx.arc(px, py, 4.5, 0, math.tau)
        ink(ctx, hexc("#7A828F"))
    ctx.restore()

def dust_cloud(ctx, x, y, u, w, seed=0, a=1.0):
    """Dynamic expanding dust puffs kicked up by running, chariot collapse, or combat."""
    u = clamp(u)
    if u <= 0.0 or a <= 0.0:
        return
    for i in range(9):
        ang = seed * 1.7 + i * 0.72
        dist = (20 + 75 * u) * (0.6 + 0.4 * rnd(seed + i))
        px = x + dist * math.cos(ang)
        py = y + (dist * 0.45) * math.sin(ang) - 25 * u
        rad = (18 + 55 * u) * (0.8 + 0.3 * rnd(seed + i * 2))
        alpha = a * (1.0 - u) * 0.42
        ell(ctx, px, py, rad, rad * 0.75)
        rgba(ctx, hexc("#C29368"), alpha)

def blast(ctx, x, y, u, r=90):
    u = clamp(u)
    if u <= 0.0 or u >= 1.0:
        return
    alpha = (1.0 - u)
    glow(ctx, x, y, r * (0.4 + 1.2 * u), FIRE_Y, alpha * 0.7)
    glow(ctx, x, y, r * (0.2 + 0.8 * u), dv.WHITE, alpha * 0.9)

# ============================================================ Character Rigs

def abhimanyu(ctx, x, y, s, t, pose="bow", look=(0.0, 0.0), rot=0.0, a=1.0, flip=False):
    """16-year-old warrior prince Abhimanyu: golden armor, white dhoti, heroic youth mukut."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        if flip:
            ctx.scale(-1, 1)
        if rot != 0.0:
            ctx.rotate(rot)
        b = 1 + 0.012 * math.sin(t * 3.5)
        ctx.scale(s, s * b)
        _abhimanyu_body(ctx, t, pose, look)
        ctx.restore()
    dv.group(ctx, a, draw)

def _abhimanyu_body(ctx, t, pose, look):
    skin = ABHI_SKIN
    Ls, Rs = (-120, -540), (120, -540)
    
    # 1. Legs & Dhoti depending on Pose
    if pose == "run":
        stride = math.sin(t * 12.0)
        leg_l = [(-50, -320), (-50 - 55 * stride, -170), (-50 - 80 * stride, -15)]
        leg_r = [(50, -320), (50 + 55 * stride, -170), (50 + 80 * stride, -15)]
        limb(ctx, leg_l, skin, 46)
        limb(ctx, leg_r, skin, 46)
        ell(ctx, leg_l[2][0], leg_l[2][1], 36, 16)
        ink(ctx, skin)
        ell(ctx, leg_r[2][0], leg_r[2][1], 36, 16)
        ink(ctx, skin)
    elif pose == "kneel":
        limb(ctx, [(-55, -300), (-110, -180), (-140, -15)], skin, 46)
        ell(ctx, -140, -15, 42, 16)
        ink(ctx, skin)
        limb(ctx, [(55, -300), (95, -160), (40, -15)], skin, 46)
        ell(ctx, 40, -15, 38, 16)
        ink(ctx, skin)
    elif pose in ("fallen", "hit"):
        limb(ctx, [(-60, -280), (-110, -160), (-150, -15)], skin, 44)
        limb(ctx, [(60, -280), (120, -150), (160, -15)], skin, 44)
    else:
        for side in (-1, 1):
            fx = side * 60
            limb(ctx, [(side * 50, -320), (side * 58, -160), (fx, -15)], skin, 46)
            ell(ctx, fx + side * 6, -10, 36, 16)
            ink(ctx, skin)
            line(ctx, [(fx - 16, -22), (fx + 16, -22)], hexc("#4A2810"), 6)
            
    # 2. Pure White Silk Dhoti with Gold Border
    smooth(ctx, [(-125, -350), (125, -350), (140, -180), (85, -75), (0, -140), (-85, -75), (-140, -180)], closed=True)
    ink(ctx, ABHI_DHOTI)
    line(ctx, [(-140, -180), (-85, -75), (0, -140), (85, -75), (140, -180)], dv.GOLD_HI, 6)
    for pleat_x in (-50, 0, 50):
        line(ctx, [(pleat_x, -340), (pleat_x * 0.7, -90)], dv.GOLD, 3)
        
    # 3. Dynamic Torso & Golden Armor
    if pose == "run":
        ctx.rotate(0.18)
    elif pose == "kneel":
        ctx.translate(0, 70)
        ctx.rotate(0.12)
        
    smooth(ctx, [(-125, -540), (125, -540), (115, -380), (-115, -380)], closed=True)
    ink(ctx, ABHI_ARMOR)
    sheen(ctx, 0, -460, 80, 60, 0.22)
    smooth(ctx, [(-125, -380), (125, -380), (120, -345), (-120, -345)], closed=True)
    ink(ctx, dv.GOLD, 4)
    gem(ctx, 0, -362, 14, dv.RED_GEM)
    ctx.arc(0, -470, 22, 0, math.tau)
    ink(ctx, dv.GOLD_HI, 4)
    gem(ctx, 0, -470, 10, dv.RED_GEM)
    
    # 4. Arms & Weapon depending on Pose
    if pose == "run":
        arm_swing = math.sin(t * 12.0)
        arms = [(Ls, (-180, -510 + 40 * arm_swing), (-260, -460 + 60 * arm_swing)),
                (Rs, (160, -510 - 40 * arm_swing), (240, -440 - 60 * arm_swing))]
        for shoulder, elbow, wrist in arms:
            limb(ctx, [shoulder, elbow, wrist], skin, 40)
        dv.bow(ctx, -260, -680 + 60 * arm_swing, -220, 65, string_x=-220, string_y=-460 + 60 * arm_swing)
        hand(ctx, -260, -460 + 60 * arm_swing, skin, 26)
        hand(ctx, 240, -440 - 60 * arm_swing, skin, 26)
    elif pose == "draw":
        arms = [(Ls, (-240, -510), (-320, -500)), (Rs, (140, -510), (-20, -530))]
        for shoulder, elbow, wrist in arms:
            limb(ctx, [shoulder, elbow, wrist], skin, 38)
        dv.bow(ctx, -320, -780, -280, 75, string_x=-20, string_y=-530)
        hand(ctx, -320, -500, skin, 24)
        hand(ctx, -20, -530, skin, 24)
    elif pose == "shot":
        arms = [(Ls, (-220, -510), (-300, -520)), (Rs, (140, -510), (220, -460))]
        for shoulder, elbow, wrist in arms:
            limb(ctx, [shoulder, elbow, wrist], skin, 38)
        dv.bow(ctx, -300, -780, -260, 75, string_x=-260, string_y=-520)
        hand(ctx, -300, -520, skin, 24)
        hand(ctx, 220, -460, skin, 24)
    elif pose == "look_back":
        arms = [(Ls, (-180, -480), (-140, -420)), (Rs, (180, -540), (280, -600))]
        for shoulder, elbow, wrist in arms:
            limb(ctx, [shoulder, elbow, wrist], skin, 38)
        dv.bow(ctx, -140, -640, -100, 65, string_x=-100, string_y=-420)
        hand(ctx, -140, -420, skin, 24)
        hand(ctx, 280, -600, skin, 24)
        limb(ctx, [(295, -605), (360, -615)], skin, 13)
    elif pose == "kneel":
        arms = [(Ls, (-180, -440), (-150, -320)), (Rs, (180, -440), (150, -320))]
        for shoulder, elbow, wrist in arms:
            limb(ctx, [shoulder, elbow, wrist], skin, 40)
        hand(ctx, -150, -320, skin, 26)
        hand(ctx, 150, -320, skin, 26)
        line(ctx, [(-180, -80), (-110, -30)], dv.GOLD, 9)
        line(ctx, [(110, -80), (180, -30)], dv.GOLD, 9)
    elif pose == "wheel":
        arms = [(Ls, (-180, -680), (-140, -820)), (Rs, (180, -680), (140, -820))]
        for shoulder, elbow, wrist in arms:
            limb(ctx, [shoulder, elbow, wrist], skin, 40)
            sheen(ctx, elbow[0], elbow[1], 20, 20, 0.2)
        chariot_wheel(ctx, 0, -880, 160, ang=t * 0.6)
        hand(ctx, -140, -820, skin, 26)
        hand(ctx, 140, -820, skin, 26)
    elif pose == "hit":
        arms = [(Ls, (-210, -460), (-180, -350)), (Rs, (180, -480), (100, -560))]
        for shoulder, elbow, wrist in arms:
            limb(ctx, [shoulder, elbow, wrist], skin, 38)
        hand(ctx, -180, -350, skin, 24)
        hand(ctx, 100, -560, skin, 24)
    elif pose == "fallen":
        arms = [(Ls, (-160, -420), (-120, -320)), (Rs, (160, -420), (120, -320))]
        for shoulder, elbow, wrist in arms:
            limb(ctx, [shoulder, elbow, wrist], skin, 38)
    else: # "bow"
        arms = [(Ls, (-220, -510), (-290, -500)), (Rs, (140, -510), (40, -520))]
        for shoulder, elbow, wrist in arms:
            limb(ctx, [shoulder, elbow, wrist], skin, 38)
        dv.bow(ctx, -290, -780, -240, 75, string_x=-250, string_y=-500)
        hand(ctx, -290, -500, skin, 24)
        hand(ctx, 40, -520, skin, 24)
        
    for side in (-1, 1):
        sx = side * 135
        ell(ctx, sx, -520, 42, 28)
        ink(ctx, dv.GOLD, 4)
        gem(ctx, sx, -520, 9, dv.RED_GEM)
    
    # 5. Neck & Head
    limb(ctx, [(0, -540), (0, -590)], skin, 46)
    ell(ctx, 0, -660, 68, 76)
    ink(ctx, skin)
    sheen(ctx, 15, -675, 24, 30, 0.22)
    
    smooth(ctx, [(0, -710), (-6, -675), (6, -675)], closed=True)
    ink(ctx, hexc("#C62828"), 1)
    
    smooth(ctx, [(-64, -700), (64, -700), (52, -780), (0, -825), (-52, -780)], closed=True)
    ink(ctx, dv.GOLD, 4)
    gem(ctx, 0, -750, 14, dv.RED_GEM)
    
    if pose == "look_back":
        eye(ctx, -24, -665, 13, 9, t, look=(-0.8, 0.0), iris=hexc("#3A2010"), seed=1)
        eye(ctx, 24, -665, 13, 9, t, look=(-0.8, 0.0), iris=hexc("#3A2010"), seed=2)
    elif pose in ("fallen", "hit"):
        line(ctx, [(-34, -665), (-14, -665)], dv.OUTLINE, 3)
        line(ctx, [(14, -665), (34, -665)], dv.OUTLINE, 3)
    else:
        eye(ctx, -24, -665, 14, 10, t, look=look, iris=hexc("#3A2010"), seed=1)
        eye(ctx, 24, -665, 14, 10, t, look=look, iris=hexc("#3A2010"), seed=2)
        
    line(ctx, [(-38, -680), (-12, -676)], dv.OUTLINE, 4)
    line(ctx, [(38, -680), (12, -676)], dv.OUTLINE, 4)
    
    if pose in ("wheel", "shot", "run"):
        ell(ctx, 0, -620, 16, 12)
        ink(ctx, hexc("#6A1A1A"), 2)
    elif pose in ("fallen", "hit"):
        line(ctx, [(-12, -625), (12, -625)], dv.OUTLINE, 3)
    else:
        line(ctx, [(-14, -625), (14, -625)], dv.OUTLINE, 3)

def drona(ctx, x, y, s, t, pose="command", look=(0.0, 0.0), a=1.0, flip=False):
    """Acharya Drona: Brahmin warrior-sage. White beard, ascetic jata-mukut, natural saffron robes."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        if flip:
            ctx.scale(-1, 1)
        b = 1 + 0.012 * math.sin(t * 2.0)
        ctx.scale(s, s * b)
        _drona_body(ctx, t, pose, look)
        ctx.restore()
    dv.group(ctx, a, draw)

def _drona_body(ctx, t, pose, look):
    skin = DRONA_SKIN
    Ls, Rs = (-125, -520), (125, -520)
    for side in (-1, 1):
        smooth(ctx, [(side * 60, -680), (side * 115, -600), (side * 125, -480), (side * 95, -490), (side * 80, -560)], closed=True)
        ink(ctx, DRONA_BEARD)
    ell(ctx, 0, -670, 88, 98)
    ink(ctx, DRONA_BEARD)
    
    for side in (-1, 1):
        fx = side * 60
        limb(ctx, [(side * 50, -340), (side * 58, -170), (fx, -20)], skin, 44)
        ell(ctx, fx + side * 6, -12, 38, 16)
        ink(ctx, skin)
        line(ctx, [(fx - 18, -26), (fx + 18, -26)], hexc("#3D2214"), 6)
        
    smooth(ctx, [(-120, -360), (120, -360), (135, -200), (85, -90), (0, -160), (-85, -90), (-135, -200)], closed=True)
    ink(ctx, DRONA_ROBE)
    line(ctx, [(-135, -200), (-85, -90), (0, -160), (85, -90), (135, -200)], hexc("#9E4010"), 6)
    
    smooth(ctx, [(-125, -520), (125, -520), (115, -360), (-115, -360)], closed=True)
    ink(ctx, hexc("#B8551E"))
    sheen(ctx, 0, -450, 70, 45, 0.16)
    line(ctx, [(-110, -510), (105, -370)], dv.WHITE, 4)
    for by in range(-500, -380, 26):
        ctx.arc(-15, by, 7, 0, math.tau)
        ink(ctx, hexc("#5C2B14"))
        
    if pose == "command":
        arms = [(Ls, (-190, -480), (-250, -430)), (Rs, (210, -580), (330, -620))]
        for shoulder, elbow, wrist in arms:
            limb(ctx, [shoulder, elbow, wrist], skin, 42)
        dv.bow(ctx, -250, -780, -210, 70, string_x=-210, string_y=-430)
        hand(ctx, -250, -430, skin, 26)
        hand(ctx, 330, -620, skin, 26)
        limb(ctx, [(345, -625), (410, -635)], skin, 13)
    elif pose == "panic":
        arms = [(Ls, (-190, -480), (-140, -580)), (Rs, (160, -480), (100, -600))]
        for shoulder, elbow, wrist in arms:
            limb(ctx, [shoulder, elbow, wrist], skin, 42)
        hand(ctx, -140, -580, skin, 26)
        hand(ctx, 100, -600, skin, 26)
    else:
        arms = [(Ls, (-190, -470), (-240, -420)), (Rs, (160, -460), (120, -380))]
        for shoulder, elbow, wrist in arms:
            limb(ctx, [shoulder, elbow, wrist], skin, 40)
        dv.bow(ctx, -240, -750, -200, 65, string_x=-200, string_y=-420)
        hand(ctx, -240, -420, skin, 24)
        hand(ctx, 120, -380, skin, 24)
        
    limb(ctx, [(0, -520), (0, -580)], skin, 46)
    ell(ctx, 0, -650, 66, 74)
    ink(ctx, skin)
    sheen(ctx, -18, -670, 26, 20, 0.15)
    
    smooth(ctx, [(-56, -630), (56, -630), (42, -500), (0, -440), (-42, -500)], closed=True)
    ink(ctx, DRONA_BEARD, 3)
    
    smooth(ctx, [(-42, -710), (42, -710), (32, -785), (0, -820), (-32, -785)], closed=True)
    ink(ctx, hexc("#5A5852"), 4)
    ell(ctx, 0, -825, 24, 20)
    ink(ctx, hexc("#484642"))
    ctx.arc(0, -750, 9, 0, math.tau)
    ink(ctx, hexc("#5C2B14"))
    
    eye(ctx, -24, -655, 14, 10, t, look=look, iris=hexc("#3A2010"), seed=4)
    eye(ctx, 24, -655, 14, 10, t, look=look, iris=hexc("#3A2010"), seed=5)
    line(ctx, [(-36, -672), (-12, -665)], hexc("#E8E6E0"), 5)
    line(ctx, [(36, -672), (12, -665)], hexc("#E8E6E0"), 5)
    
    if pose in ("command", "panic"):
        ell(ctx, 0, -610, 18, 12)
        ink(ctx, hexc("#5A1212"), 2)
    else:
        line(ctx, [(-14, -615), (14, -615)], dv.OUTLINE, 4)

# ============================================================ Scene Classes (Strictly 6 Scenes, Viral Loop)

class Hook(Cued):
    """Scene 1: Hook - Seven Maharathis terrified of a 16-year-old boy, stepping back in hesitation."""
    def beats(self, d):
        c = self.cue
        return {
            "maharathi": c("MAHARATHI", d * 0.22),
            "solah": c("SOLAH", d * 0.45),
            "dar": c("DAR", d * 0.75),
        }

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "boom"), (b["dar"], "whoosh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        
        # Camera shake on DAR GAYE cue
        shake_dt = t - b["dar"]
        if 0.0 <= shake_dt <= 0.45:
            shake_amp = (1.0 - shake_dt / 0.45) * 16.0
            ctx.translate(math.sin(shake_dt * 36.0) * shake_amp, math.cos(shake_dt * 28.0) * shake_amp * 0.5)
            
        siege_red_sky(ctx, t)
        
        # Dynamic ease_out retreat away from Abhimanyu
        u_fear = ease_out_cubic(clamp(t / (d * 0.55)))
        
        # Back line Maharathis: Deep encircling arena
        # Back-left silhouette
        def draw_mah_l():
            ctx.save()
            ctx.translate(340 - 55 * u_fear, GROUND - 110)
            ctx.scale(0.46, 0.46)
            limb(ctx, [(0, -320), (0, -160), (0, -20)], hexc("#2A0B10"), 44)
            smooth(ctx, [(-85, -480), (85, -480), (75, -320), (-75, -320)], closed=True)
            ink(ctx, hexc("#2A0B10"))
            ell(ctx, 0, -560, 52, 60)
            ink(ctx, hexc("#2A0B10"))
            line(ctx, [(0, -400), (-40, -680)], dv.OUTLINE, 8)
            ctx.restore()
        dv.group(ctx, 0.85, draw_mah_l)
        
        # Back-center-left silhouette
        def draw_mah_cl():
            ctx.save()
            ctx.translate(440 - 35 * u_fear, GROUND - 135)
            ctx.scale(0.42, 0.42)
            limb(ctx, [(0, -320), (0, -160), (0, -20)], hexc("#2A0B10"), 44)
            smooth(ctx, [(-85, -480), (85, -480), (75, -320), (-75, -320)], closed=True)
            ink(ctx, hexc("#2A0B10"))
            ell(ctx, 0, -560, 52, 60)
            ink(ctx, hexc("#2A0B10"))
            line(ctx, [(0, -400), (-30, -680)], dv.OUTLINE, 8)
            ctx.restore()
        dv.group(ctx, 0.8, draw_mah_cl)
        
        # Back-center-right silhouette
        def draw_mah_cr():
            ctx.save()
            ctx.translate(640 + 35 * u_fear, GROUND - 135)
            ctx.scale(0.42, 0.42)
            limb(ctx, [(0, -320), (0, -160), (0, -20)], hexc("#2A0B10"), 44)
            smooth(ctx, [(-85, -480), (85, -480), (75, -320), (-75, -320)], closed=True)
            ink(ctx, hexc("#2A0B10"))
            ell(ctx, 0, -560, 52, 60)
            ink(ctx, hexc("#2A0B10"))
            line(ctx, [(0, -400), (30, -680)], dv.OUTLINE, 8)
            ctx.restore()
        dv.group(ctx, 0.8, draw_mah_cr)
        
        # Back-right: Karna recoiling back with eyes wide looking up
        dv.karna(ctx, 740 + 50 * u_fear, GROUND - 100, 0.50, t, pose="stand", kavach=1.0, look=(0.0, -0.6), flip=True)
        
        # Front line left: Duryodhan in full panic posture, shield arm raised, open mouth, stepping back
        duryodhan(ctx, 220 - 75 * u_fear, GROUND - 10, 0.68, t, pose="panic", shout=1.0, look=(0.0, -0.6), flip=False)
        
        # Front line right: Drona in defensive shield posture, eyes looking up in shock, stepping back
        drona(ctx, 860 + 75 * u_fear, GROUND - 10, 0.68, t, pose="panic", look=(0.0, -0.6), flip=True)
        
        # Center & Front: Towering 16-year-old Abhimanyu (scale 0.78, sabse bada)
        u_pulse = clamp((t - b["dar"]) / 0.5) if t >= b["dar"] else 0.0
        aura_rad = 280 + 140 * math.sin(u_pulse * math.pi)
        aura_alpha = 0.5 + 0.3 * math.sin(u_pulse * math.pi)
        glow(ctx, 540, GROUND - 260, aura_rad, GOLD_HI, aura_alpha)
        glow(ctx, 540, GROUND - 260, aura_rad * 0.6, FIRE_Y, aura_alpha * 1.2)
        abhimanyu(ctx, 540, GROUND - 10, 0.78, t, pose="draw", look=(0.0, 0.0), flip=False)


class Ghus(Cued):
    """Scene 2: Abhimanyu breaches the Chakravyuh alone; Kaurava soldiers scatter outward in panic."""
    def beats(self, d):
        c = self.cue
        return {
            "abhimanyu": c("ABHIMANYU", d * 0.25),
            "ghusa": c("GHUSA", d * 0.50),
            "bikhar": c("BIKHAR", d * 0.78),
        }

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "whoosh"), (b["ghusa"], "arrow"), (b["bikhar"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        kurukshetra_day(ctx, t, haze=1.1)
        
        broken = t >= b["bikhar"]
        chakravyuh_formation(ctx, 540, GROUND - 250, 480, t, broken=broken)
        
        # Kaurava soldier crowd on screen-right: standing first, fleeing in panic on BIKHAR cue
        if not broken:
            kaurava_mob(ctx, 580, 1080, GROUND - 14, 6, t, mode="stand", s=0.50, flee=0.0, seed=3)
        else:
            u_flee = clamp((t - b["bikhar"]) / 1.2)
            dust_cloud(ctx, 840, GROUND - 10, u_flee, 300, seed=4)
            kaurava_mob(ctx, 580, 1080, GROUND - 14, 6, t, mode="panic", s=0.50, flee=2.4, seed=3)
            
        # Abhimanyu sprinting inward and firing divine arrows into the Kaurava army
        if t < b["ghusa"]:
            u_run = clamp(t / b["ghusa"])
            ax = lerp(160, 460, u_run)
            dust_cloud(ctx, ax - 40, GROUND - 10, u_run, 80, seed=1)
            abhimanyu(ctx, ax, GROUND - 10, 0.74, t, pose="run", flip=False)
        elif t < b["bikhar"]:
            abhimanyu(ctx, 460, GROUND - 10, 0.74, t, pose="draw", flip=False)
            u_arr = clamp((t - b["ghusa"]) / 0.35)
            sx, sy = 460, GROUND - 380
            tx, ty = 820, GROUND - 300
            ang = math.atan2(ty - sy, tx - sx)
            dv.divine_arrow(ctx, lerp(sx, tx, u_arr), lerp(sy, ty, u_arr), ang, 85, t, a=1.0)
            if u_arr >= 0.85:
                blast(ctx, 820, GROUND - 300, (t - b["ghusa"] - 0.28) / 0.3, r=80)
        else:
            glow(ctx, 520, GROUND - 240, 260, GOLD_HI, 0.5)
            abhimanyu(ctx, 520, GROUND - 10, 0.74, t, pose="shot", flip=False)
            u_arr2 = clamp((t - b["bikhar"]) / 0.35)
            if u_arr2 < 1.0:
                ang2 = math.atan2(0, 1)
                dv.divine_arrow(ctx, lerp(520, 950, u_arr2), GROUND - 340, ang2, 85, t, a=1.0)


class Dhanush(Cued):
    """Scene 3: Drona commands Karna; treacherous arrow snaps Abhimanyu's bow from behind."""
    def beats(self, d):
        c = self.cue
        return {
            "drona": c("DRONA", d * 0.22),
            "karna": c("KARNA", d * 0.42),
            "peechhe": c("PEECHHE", d * 0.62),
            "kaato": c("KAATO", d * 0.82),
        }

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["drona"], "whoosh"), (b["kaato"], "arrow"), (b["kaato"] + 0.08, "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        siege_red_sky(ctx, t)
        
        # 1. Back line silhouettes at x=300 and x=450
        for sx in (300, 450):
            def draw_mah(x=sx):
                ctx.save()
                ctx.translate(x, GROUND - 90)
                ctx.scale(0.50, 0.50)
                limb(ctx, [(0, -320), (0, -160), (0, -20)], hexc("#2A0B10"), 44)
                smooth(ctx, [(-85, -480), (85, -480), (75, -320), (-75, -320)], closed=True)
                ink(ctx, hexc("#2A0B10"))
                ell(ctx, 0, -560, 52, 60)
                ink(ctx, hexc("#2A0B10"))
                line(ctx, [(0, -400), (0, -720)], dv.OUTLINE, 8)
                ctx.restore()
            dv.group(ctx, 0.8, draw_mah)
            
        # 2. Back line right: Karna (x=700, y=GROUND-90, scale 0.52) shooting from behind
        dv.karna(ctx, 700, GROUND - 90, 0.52, t, pose="stand", kavach=1.0, look=(-0.7, 0.0), flip=True)
        
        # 3. Front line left: Duryodhana (x=210, y=GROUND-10, scale 0.68) facing Abhimanyu
        duryodhan(ctx, 210, GROUND - 10, 0.68, t, pose="point", shout=0.8, look=(0.7, 0.0), flip=False)
        
        # 4. Front line right: Acharya Drona (x=870, y=GROUND-10, scale 0.68) commanding
        drona(ctx, 870, GROUND - 10, 0.68, t, pose="command", look=(-0.6, 0.0), flip=True)
        
        # Arrow flight from Karna (sx=700, sy=GROUND-330) to Abhimanyu's bow (tx=540, ty=GROUND-360)
        struck = t >= (b["kaato"] + 0.35)
        if t >= b["kaato"]:
            u_arr = clamp((t - b["kaato"]) / 0.35)
            sx, sy = 700, GROUND - 330
            tx, ty = 540, GROUND - 360
            ang = math.atan2(ty - sy, tx - sx)
            arr_x = lerp(sx, tx, u_arr)
            arr_y = lerp(sy, ty, u_arr)
            dv.divine_arrow(ctx, arr_x, arr_y, ang, 75, t, a=1.0)
            if u_arr >= 0.85:
                blast(ctx, 540, GROUND - 360, (t - b["kaato"] - 0.28) / 0.3, r=70)
                
        # 5. Center Front: Abhimanyu at (x=540, y=GROUND-10, scale 0.74)
        glow(ctx, 540, GROUND - 240, 240, GOLD_HI, 0.4)
        abhimanyu(ctx, 540, GROUND - 10, 0.74, t, pose="kneel" if struck else "bow", look=(-0.6, 0.0), flip=False)


class Pahiya(Cued):
    """Scene 4: Bow and chariot shattered; Abhimanyu heaves the heavy chariot wheel overhead."""
    def beats(self, d):
        c = self.cue
        return {
            "toota": c("TOOTA", d * 0.22),
            "rath": c("RATH", d * 0.45),
            "pahiya": c("PAHIYA", d * 0.68),
            "utha": c("UTHA", d * 0.82),
        }

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "thud"), (b["toota"], "boom"), (b["pahiya"], "whoosh"), (b["utha"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        kurukshetra_day(ctx, t, haze=1.3)
        
        # Shattered chariot debris falling and kicking up dust
        u_shatter = clamp(t / (d * 0.4))
        dust_cloud(ctx, 360, GROUND - 10, u_shatter, 160, seed=5)
        dust_cloud(ctx, 720, GROUND - 10, u_shatter, 160, seed=8)
        
        # Broken chariot frame fragments
        line(ctx, [(340, GROUND - 80), (410, GROUND - 20)], WHEEL_WOOD, 14)
        line(ctx, [(670, GROUND - 70), (740, GROUND - 15)], WHEEL_WOOD, 14)
        chariot_wheel(ctx, 710, GROUND - 30, 70, ang=0.4, broken=True)
        
        u_lift = clamp((t - b["pahiya"]) / 0.55)
        
        # Abhimanyu heaving the massive chariot wheel overhead
        glow(ctx, 540, GROUND - 320, 320, FIRE_Y, 0.6)
        glow(ctx, 540, GROUND - 320, 200, FIRE_O, 0.7)
        s = lerp(0.70, 0.78, ease_out_back(u_lift))
        abhimanyu(ctx, 540, GROUND - 10, s, t, pose="wheel", look=(0.0, -0.2))


class Akela(Cued):
    """Scene 5: Seven surround the unarmed hero tightly; Abhimanyu fights to his last breath until veergati."""
    def beats(self, d):
        c = self.cue
        return {
            "saaton": c("SAATON", d * 0.18),
            "ghera": c("GHERA", d * 0.42),
            "ladta": c("LADTA", d * 0.65),
            "saans": c("SAANS", d * 0.85),
        }

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "soft_thud"), (b["ghera"], "whoosh"), (b["ladta"], "boom"), (b["saans"], "shimmer")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        siege_red_sky(ctx, t)
        
        # Ghera closing in tight
        u_tight = clamp(t / (d * 0.65))
        
        # Back line silhouettes closing inward
        for sx in (300 + 40 * u_tight, 450 + 20 * u_tight):
            def draw_mah(x=sx):
                ctx.save()
                ctx.translate(x, GROUND - 90)
                ctx.scale(0.50, 0.50)
                limb(ctx, [(0, -320), (0, -160), (0, -20)], hexc("#2A0B10"), 44)
                smooth(ctx, [(-85, -480), (85, -480), (75, -320), (-75, -320)], closed=True)
                ink(ctx, hexc("#2A0B10"))
                ell(ctx, 0, -560, 52, 60)
                ink(ctx, hexc("#2A0B10"))
                line(ctx, [(0, -400), (0, -720)], dv.OUTLINE, 8)
                ctx.restore()
            dv.group(ctx, 0.8, draw_mah)
            
        # Back line right: Karna closing inward
        dv.karna(ctx, 700 - 30 * u_tight, GROUND - 90, 0.52, t, pose="stand", kavach=1.0, look=(-0.7, 0.0), flip=True)
        
        # Front line left: Duryodhan closing inward
        duryodhan(ctx, 210 + 50 * u_tight, GROUND - 10, 0.68, t, pose="point", shout=0.9, look=(0.7, 0.0), flip=False)
        
        # Front line right: Drona closing inward
        drona(ctx, 870 - 50 * u_tight, GROUND - 10, 0.68, t, pose="command", look=(-0.6, 0.0), flip=True)
        
        # Abhimanyu fighting with wheel then peaceful veergati (no blood)
        u_fall = clamp((t - b["saans"]) / (d * 0.15))
        if u_fall >= 0.1:
            rot = 1.35 * ease_in(u_fall)
            dust_cloud(ctx, 540, GROUND - 10, u_fall, w=500, seed=18)
            abhimanyu(ctx, 540, GROUND - 10, 0.74, t, pose="fallen" if u_fall >= 0.7 else "hit", rot=rot)
            glow(ctx, 540, GROUND - 120, 280, GOLD_HI, 0.6)
            dv.petals(ctx, t, n=35, a=clamp((u_fall - 0.2) / 0.6))
        else:
            glow(ctx, 540, GROUND - 320, 260, FIRE_Y, 0.6)
            abhimanyu(ctx, 540, GROUND - 10, 0.76, t, pose="wheel", look=(0.0, -0.2))


class Loop(Cued):
    """Scene 6: Solitary Abhimanyu at the sealed gate; unyielding spirit loops into opening frame."""
    def beats(self, d):
        c = self.cue
        return {
            "nikalna": c("NIKALNA", d * 0.25),
            "aata": c("AATA", d * 0.45),
            "haar": c("HAAR", d * 0.68),
            "tabhi": c("TABHI", d * 0.88),
        }

    def events(self, d):
        b = self.beats(d)
        return [(0.02, "ghanti"), (b["haar"], "shimmer"), (b["tabhi"], "whoosh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        
        # Atmospheric battlefield sunset
        g = cairo.LinearGradient(0, 0, 0, H)
        for at, c in ((0.0, "#360A0C"), (0.35, "#781418"), (0.65, "#B83A14"), (1.0, "#220808")):
            g.add_color_stop_rgb(at, *hexc(c))
        ctx.set_source(g)
        ctx.paint()
        
        # Massive sealed labyrinth gate in deep background
        chakravyuh_formation(ctx, 540, GROUND - 300, 380, t * 0.5, broken=False)
        
        # Solitary Abhimanyu looking back at sealed path with unyielding resolve
        glow(ctx, 540, GROUND - 260, 320, FIRE_O, 0.65 + 0.15 * math.sin(t * 6.0))
        glow(ctx, 540, GROUND - 260, 200, GOLD_HI, 0.55)
        abhimanyu(ctx, 540, GROUND - 10, 0.74, t, pose="look_back", look=(-0.8, 0.0), flip=False)
        
        # Final 0.45s seamless crossfade back to Scene 1 opening frame
        rem = d - t
        if rem <= 0.45:
            x_fade = (0.45 - rem) / 0.45
            ctx.push_group()
            Hook().draw(ctx, 0.0, d)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(x_fade)


SCENE_CLASSES = {
    "hook": Hook,
    "ghus": Ghus,
    "dhanush": Dhanush,
    "pahiya": Pahiya,
    "akela": Akela,
    "loop": Loop,
}
SCENES = SCENE_CLASSES

# ============================================================ Thumbnail & Upload Kit

def thumbnail(ctx):
    kurukshetra_day(ctx, 0.4, haze=1.2)
    glow(ctx, 540, 880, 480, FIRE_Y, 0.55)
    chakravyuh_formation(ctx, 540, 920, 420, 0.5, broken=True)
    abhimanyu(ctx, 540, 1260, 0.82, 0.5, pose="wheel", look=(0.0, -0.3))
    duryodhan(ctx, 190, 1270, 0.65, 0.5, pose="point", shout=0.8, look=(0.6, -0.4), flip=False)
    drona(ctx, 890, 1270, 0.65, 0.5, pose="command", look=(-0.6, -0.4), flip=True)
    
    g = cairo.LinearGradient(0, 0, 0, 560)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.92)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 560)
    ctx.set_source(g)
    ctx.fill()
    g = cairo.LinearGradient(0, 1380, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.92)
    ctx.rectangle(0, 1380, W, H - 1380)
    ctx.set_source(g)
    ctx.fill()
    
    text(ctx, "SAAT MAHARATHI", 540, 230, 115, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "EK BAALAK SE DARE", 540, 370, 115, hexc("#FF4A3A"), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=24)
    text(ctx, "DIVYA RAHASYA", 540, 1820, 42, GOLD_HI, a=0.85)


UPLOAD = {
    "thumb_text": "GUPT NIYAM TODA",
    "titles": [
        "Chakravyuh Ke 7 Darwaze Aur Abhimanyu Vadh Ka Gupt Niyam #shorts",
        "16 Saal Ke Veer Se Kyun Dar Gaye 7 Maharathi? #shorts",
        "Chakravyuh Mein 7 Maharathiyon Ne Toda Gupt Niyam! 😱 #shorts",
        "Dhanush Toota To Uthaya Rath Ka Pahiya: Veer Abhimanyu",
        "Mahabharat Ka Sabse Bada Chhal: Abhimanyu Vadh Rahasya",
    ],
    "queries": [
        "chakravyuh ke 7 darwaze abhimanyu vadh ka gupt niyam",
        "abhimanyu chakravyuh 7 maharathi kyun dare",
        "drona ne karna se dhanush kyun katwaya",
        "abhimanyu vadh dharmayuddha niyam mahabharat",
    ],
    "description": (
        "Mahabharat ke 13ve din 16 saal ke veer Abhimanyu ne Chakravyuh ke saaton darwaze akele tod diye. "
        "Jab Kaurav sena kaanpne lagi, to 7 Maharathiyon ne Dharmayuddha ka gupt niyam tod diya!\n\n"
        "Drona ke aadesh par Karna ne peechhe se Abhimanyu ka dhanush kaata. Fir bhi us veer ne rath ka "
        "pahiya uthakar aakhiri saans tak ladai ki!\n\n"
        "Sources: Mahabharata, Drona Parva (Abhimanyu-badha Parva, KM Ganguli trans. sections 31-49).\n\n"
        "Comment mein likhiye: Jai Veer Abhimanyu! 🙏\n\n"
        "#Shorts #Mahabharat #Abhimanyu #Chakravyuh #DivyaRahasya #SanatanDharma"
    ),
    "tags": [
        "abhimanyu", "chakravyuh", "saat darwaze", "gupt niyam", "mahabharat", "drona",
        "karna", "duryodhan", "veer abhimanyu", "rath ka pahiya", "divya rahasya", "adharm"
    ],
    "hashtags": ["#Shorts", "#Mahabharat", "#Abhimanyu", "#Chakravyuh"],
}
