"""Tulsi Vivah & Shaligram Rahasya: Ek Pativrata Stri Ke Shraap Se Vishnu Bane Patthar (~22s loop katha, 6 scenes).

Angle:
Asura Jalandhar was invincible due to the unyielding pativrata vow of his chaste wife Vrinda.
To save the cosmos and devatas from destruction, Bhagavan Vishnu disguised Himself as Jalandhar
to break the vow. Upon discovering the truth, an anguished Vrinda cursed Vishnu to turn into stone.
Lord Vishnu willingly accepted the curse, transforming into the sacred Shaligram stone, and granted
her the supreme boon that she would eternally reside as the holy Tulsi plant, inseparable from His worship.
The final phrase "...KYUNKI" loops seamlessly back into the opening hook line:
"EK PATIVRATA STRI KE SHRAAP SE... KHUD BHAGAVAN VISHNU, PATTHAR BAN GAYE!".
"""

import math
import cairo

from core.katha import *  # noqa: F401,F403
import core.devta as dv
from core.devta import ell, gem, hand, ink, limb, sheen, smooth, eye, palm, rrect, line, lerp, clamp, ease_out_cubic, ease_out_back, rnd

TOPIC = "TULSI VIVAH SHALIGRAM VRINDA"
OUTPUTS = {"edge": "tulsi_vivah_short.mp4", "files": "tulsi_vivah_short.mp4"}
MUSIC_STYLE = "ambient"    # Devotional mystery & sacred transformation
MUSIC_BPM = 76             # >= 6 away from abhimanyu (84), peaceful devotional tempo
MUSIC_VOLUME = 0.12
TAIL_PAD = 0.04
MAX_GAP = 0.04
KIKI_PAUSE_MS = 150

# Color palette
GOLD_HI = dv.GOLD_HI
GOLD = dv.GOLD
WHITE = dv.WHITE
VISHNU_BLUE = hexc("#4A7CB8")   # Radiant celestial Neel-varn
PEETAMBAR = hexc("#F0B429")     # Vibrant divine Pitambar yellow
VRINDA_SKIN = hexc("#E8A77E")   # Pure pious wheatish skin
VRINDA_SAREE = hexc("#D4384A")  # Sacred red suhagan saree
VRINDA_AURA = hexc("#FFAA44")   # Pativrata tapasya glow
JALANDHAR_ARMOR = hexc("#282D3A") # Asura king iron armor
JALANDHAR_SKIN = hexc("#7C5340")
SHALIGRAM_STONE = hexc("#1A1D24") # Polished black ammonite stone
SHALIGRAM_GOLD = hexc("#E6C265")  # Natural golden spiral imprint
TULSI_GREEN = hexc("#2D6E3F")   # Sacred Tulsi green
TULSI_LIGHT = hexc("#52A86B")
POT_BRONZE = hexc("#8C4F2B")    # Traditional copper/terracotta vrindavan pot

SOURCES = [
    "Shiva Purana, Rudra Samhita (Yuddha Khanda, chapters 13-24): The tale of Shankhachuda/Jalandhar, "
    "Vrinda's steadfast chastity, Bhagavan Vishnu assuming Jalandhar's guise to break the vow, and the subsequent curse.",
    "Padma Purana, Uttara Khanda: Sati Vrinda's curse upon Vishnu turning Him into Shaligram stone, His boon of Tulsi, "
    "and the sacred tradition of Tulsi Vivah on Kartika Shukla Dvadashi / Dev Uthani.",
]

SPEC = [
    {"key": "hook", "text": "EK SACHHI PATNI KA SHRAAP",
     "visual": "Radiant four-armed Vishnu surrounded by divine aura is visibly cursed by weeping Vrinda and turns to black Shaligram",
     "vo": [("punch", [("एक सच्ची पत्नी के", "EK SACHHI PATNI KE"),
                       ("श्राप से,", "SHRAAP SE,"),
                       ("खुद विष्णु", "KHUD VISHNU"),
                       ("पत्थर बन गए!", "PATTHAR BAN GAYE!")], 0.04)]},
    {"key": "asur", "text": "JALANDHAR THA AJEYA",
     "visual": "Ferocious asura king Jalandhar stands towering with raised scimitar; Vrinda meditates in an unyielding circle of sacred fire",
     "vo": [("build", [("असुर जालंधर अजेय था,", "ASUR JALANDHAR AJEYA THA,"),
                       ("पत्नी वृंदा की", "PATNI VRINDA KI"),
                       ("तपस्या से।", "TAPASYA SE.")], 0.04)]},
    {"key": "chhal", "text": "DEVTAON KO BACHANE ROOP BADLA",
     "visual": "Vishnu projects a gentle illusionary light disguise of Jalandhar peacefully arriving before Vrinda, who opens eyes in surprise",
     "vo": [("fast", [("देवताओं को बचाने,", "DEVTAON KO BACHANE,"),
                      ("विष्णु ने वो", "VISHNU NE WO"),
                      ("तपस्या तोड़ी।", "TAPASYA TODI.")], 0.04)]},
    {"key": "shraap", "text": "VRINDA NE SHRAAP DIYA",
     "visual": "Disguise dissolves into cosmic blue Vishnu; Vrinda raises hands in grief and disbelief, crying out her curse with righteous tapasya flash",
     "vo": [("punch", [("वृंदा ने रोकर", "VRINDA NE ROKAR"),
                       ("श्राप दिया,", "SHRAAP DIYA,"),
                       ("पत्थर बन जाओ!", "PATTHAR BAN JAO!")], 0.04)]},
    {"key": "vardan", "text": "SHALIGRAM BANE PRABHU",
     "visual": "Vishnu humbly bows His crowned head as golden rays cocoon Him into the Shaligram stone; Tulsi plant manifests with holy fragrance",
     "vo": [("tell", [("प्रभु शालिग्राम बने,", "PRABHU SHALIGRAM BANE,"),
                      ("और वरदान दिया,", "AUR VARDAN DIYA,"),
                      ("तुलसी बनकर तुम", "TULSI BANKAR TUM"),
                      ("सदा पूजी जाओगी।", "SADA POOJI JAOGI.")], 0.04)]},
    {"key": "loop", "text": "TULSI VIVAH HOTA HAI... KYUNKI",
     "visual": "Sacred Tulsi pot adorned with wedding veil stands beside the glowing Shaligram in Kartika twilight; seamless crossfade into frame 0 opening",
     "vo": [("awe", [("इसीलिए हर साल", "ISILIYE HAR SAAL"),
                     ("तुलसी विवाह", "TULSI VIVAH"),
                     ("होता है,", "HOTA HAI,"),
                     ("क्योंकि", "KYUNKI")], 0.0)]},
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "PATIVRATA": hexc("#FF5555"), "STRI": hexc("#FF5555"), "SHRAAP": hexc("#FF3333"), "SE...": hexc("#FF3333"),
    "KHUD": GOLD_HI, "BHAGAVAN": GOLD_HI, "VISHNU,": hexc("#529BFF"), "PATTHAR": hexc("#FFDD55"), "BAN": hexc("#FFDD55"), "GAYE!": hexc("#FF5555"),
    "ASUR": hexc("#FF4444"), "JALANDHAR": hexc("#FF4444"), "AJEYA": hexc("#FF5555"), "THA...": hexc("#FF5555"),
    "VRINDA": hexc("#FFAA44"), "PATIVRAT": hexc("#FFAA44"), "SE.": hexc("#FFAA44"),
    "DEVTAON": GOLD_HI, "BACHANE,": GOLD_HI, "ROOP": hexc("#529BFF"), "DHARKAR,": hexc("#529BFF"), "VRAT": hexc("#FFAA44"), "TODA.": hexc("#FF4444"),
    "SACH": hexc("#FF5555"), "JAANTE": hexc("#FF5555"), "JAO!": hexc("#FF3333"),
    "PRABHU": GOLD_HI, "SHALIGRAM": hexc("#529BFF"), "BANE,": hexc("#529BFF"), "VARDAN": GOLD_HI, "DIYA...": GOLD_HI,
    "TULSI": hexc("#55D468"), "BANKAR,": hexc("#55D468"), "POOJA": GOLD_HI, "RAHOGI.": GOLD_HI,
    "ISILIYE": GOLD_HI, "KARTIK,": GOLD_HI, "VIVAH": hexc("#FFAA44"), "HOTA": hexc("#FFAA44"), "HAI...": hexc("#FFAA44"),
    "KYUNKI": GOLD_HI,
})

def ease_in(u):
    u = clamp(u)
    return u * u * u

# ============================================================ Background Environments

def vaikuntha_sky(ctx, t):
    """Divine celestial twilight with purple-indigo gradient and floating sacred petals."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in ((0.0, "#0F0B1E"), (0.35, "#1B173B"), (0.65, "#38235A"), (0.85, "#4F2C58"), (1.0, "#190D22")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.paint()
    
    # Celestial halo disc
    glow(ctx, 540, 420, 360, GOLD_HI, 0.35)
    ell(ctx, 540, 420, 60, 60)
    ink(ctx, WHITE, 0.9)
    
    # Sacred mountains / horizon
    smooth(ctx, [(0, 840), (280, 800), (560, 830), (840, 790), (W, 820), (W, H), (0, H)], closed=True)
    ink(ctx, hexc("#140A1A"))
    smooth(ctx, [(0, GROUND - 20), (380, GROUND - 50), (740, GROUND - 15), (W, GROUND - 35), (W, H), (0, H)], closed=True)
    ink(ctx, hexc("#0B050E"))
    
    # Floating celestial dust
    for p in range(16):
        px = (p * 74 + int(t * 30)) % W
        py = (340 + p * 48 - int(t * 18)) % (GROUND - 60)
        ctx.arc(px, py, 2.4, 0, math.tau)
        rgba(ctx, GOLD_HI, 0.4)
        ctx.fill()

def asur_battle_sky(ctx, t):
    """Fiery volcanic crimson sky reflecting Jalandhar's untamed asuric conquests."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in ((0.0, "#260608"), (0.35, "#521215"), (0.65, "#82221B"), (0.85, "#3D1012"), (1.0, "#140406")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.paint()
    
    # Blazing crimson sun
    glow(ctx, 540, 360, 300, hexc("#FF3A1A"), 0.5)
    ell(ctx, 540, 360, 52, 52)
    ink(ctx, hexc("#FFB588"), 0.85)
    
    # Jagged asura fort silhouettes
    smooth(ctx, [(0, 820), (220, 770), (450, 840), (750, 760), (W, 830), (W, H), (0, H)], closed=True)
    ink(ctx, hexc("#170407"))
    smooth(ctx, [(0, GROUND - 10), (500, GROUND - 40), (W, GROUND - 20), (W, H), (0, H)], closed=True)
    ink(ctx, hexc("#0C0204"))

def sacred_ashram_sky(ctx, t):
    """Serene sacred twilight forest for Vrinda's hermitage."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, c in ((0.0, "#08131C"), (0.35, "#0E2433"), (0.65, "#18404E"), (0.85, "#253F3A"), (1.0, "#0B1512")):
        g.add_color_stop_rgb(at, *hexc(c))
    ctx.set_source(g)
    ctx.paint()
    
    # Holy full moon / Kartika moon
    glow(ctx, 540, 320, 260, hexc("#FFF6D4"), 0.45)
    ell(ctx, 540, 320, 48, 48)
    ink(ctx, WHITE, 0.95)
    
    # Forest hill silhouettes
    smooth(ctx, [(0, 800), (320, 760), (640, 810), (900, 770), (W, 790), (W, H), (0, H)], closed=True)
    ink(ctx, hexc("#0A1716"))
    smooth(ctx, [(0, GROUND - 20), (420, GROUND - 40), (820, GROUND - 15), (W, GROUND - 30), (W, H), (0, H)], closed=True)
    ink(ctx, hexc("#050D0C"))

# ============================================================ Custom Rigs (Strictly No Clones)

def chaturbhuj_vishnu(ctx, x, y, s=0.74, t=0.0, pose="bless", look=(0, 0), flip=False):
    """Bhagavan Shri Vishnu rig: Chaturbhuj (4 arms: Shankh, Chakra, Gada, Padma),
    celestial Neel-varn blue skin, grand golden Kirita-mukut, Peetambar silk, Kaustubha gem."""
    def _draw():
        c = ctx
        c.save()
        c.translate(x, y)
        if flip:
            c.scale(-s, s)
        else:
            c.scale(s, s)
            
        skin = VISHNU_BLUE
        gold = GOLD
        gem_col = hexc("#E63946") # Kaustubha jewel
        
        # Divine golden radiant aura
        glow(c, 0, -560, 280, GOLD_HI, 0.45 + 0.08 * math.sin(t * 3.0))
        dv.halo(c, 0, -620, 150, t)
        
        # Rear Arms (Upper Left: Panchajanya Shankh; Upper Right: Sudarshana Chakra)
        # Upper Right Arm (Chakra)
        c.save()
        c.translate(130, -510)
        c.rotate(-0.35 + 0.05 * math.sin(t * 2.0))
        limb(c, [(0, 0), (60, -90), (40, -180)], skin, 38)
        hand(c, 40, -180, skin, 22)
        # Spinning Sudarshana Chakra
        c.save()
        c.translate(40, -210)
        c.rotate(t * 5.0)
        glow(c, 0, 0, 70, GOLD_HI, 0.6)
        circle(c, 0, 0, 36, gold)
        circle(c, 0, 0, 28, skin)
        for sp in range(8):
            ang = sp * (math.tau / 8)
            line(c, [(0, 0), (34 * math.cos(ang), 34 * math.sin(ang))], gold, 5)
        gem(c, 0, 0, 9, gem_col)
        c.restore()
        c.restore()
        
        # Upper Left Arm (Shankh)
        c.save()
        c.translate(-130, -510)
        c.rotate(0.35 - 0.05 * math.sin(t * 2.0))
        limb(c, [(0, 0), (-60, -90), (-40, -180)], skin, 38)
        hand(c, -40, -180, skin, 22)
        # Panchajanya Shankh
        c.save()
        c.translate(-40, -205)
        smooth(c, [(0, -24), (20, -10), (16, 20), (-12, 22), (-22, 0)], closed=True)
        ink(c, WHITE)
        line(c, [(0, -22), (4, 18)], gold, 4)
        c.restore()
        c.restore()
        
        # Feet & golden Charan-Paduka/anklets
        for fx in (-48, 48):
            ell(c, fx, -14, 42, 18)
            ink(c, skin)
            line(c, [(fx - 24, -28), (fx, -22), (fx + 24, -28)], gold, 6)
            
        # Peetambar yellow silk dhoti
        dhoti = [(-115, -340), (115, -340), (135, -200), (150, -44), (60, -32), (0, -60), (-60, -32), (-150, -44), (-135, -200)]
        smooth(c, dhoti)
        ink(c, PEETAMBAR)
        line(c, [(148, -48), (60, -36), (0, -64), (-60, -36), (-148, -48)], gold, 12)
        
        # Torso
        smooth(c, [(-120, -500), (-58, -524), (58, -524), (120, -500), (125, -425), (96, -335), (-96, -335), (-125, -425)])
        ink(c, skin)
        
        # Vanamala (fragrant celestial garland reaching down)
        smooth(c, [(-90, -510), (-110, -420), (-70, -280), (0, -240), (70, -280), (110, -420), (90, -510)], closed=False)
        c.set_line_width(14)
        c.set_source_rgb(*WHITE)
        c.stroke()
        for v in range(9):
            vang = -0.8 + v * 0.2
            vx = 85 * math.sin(vang)
            vy = -380 + 130 * math.cos(vang)
            circle(c, vx, vy, 6, hexc("#FF5577"))
            
        # Royal Kamarbandh & Kaustubha Mani
        rrect(c, -110, -360, 220, 32, 10)
        ink(c, gold, 4)
        gem(c, 0, -475, 14, gem_col) # Kaustubha at chest
        
        # Neck & Head
        rrect(c, -30, -565, 60, 60, 12)
        ink(c, skin)
        for side in (-1, 1):
            ell(c, side * 96, -635, 16, 26)
            ink(c, skin)
            circle(c, side * 102, -600, 12, gold)
        ell(c, 0, -635, 96, 106)
        ink(c, skin)
        sheen(c, -34, -680, 38, 24, 0.16)
        
        # Calm divine eyes
        for side in (-1, 1):
            eye(c, side * 36, -640, 24, 28, t, look=look, iris=hexc("#1E2A38"), seed=1)
            line(c, [(side * 14, -678), (side * 36, -688), (side * 62, -680)], hexc("#141820"), 6)
            
        line(c, [(2, -635), (-5, -615), (4, -610)], shade(skin, 0.65), 4)
        # Gentle compassionate smile
        c.move_to(-18, -590)
        c.curve_to(-8, -582, 8, -582, 18, -590)
        c.set_line_width(4)
        rgba(c, hexc("#B83248"))
        c.stroke()
        
        # Vaishnava Urdhva Pundra Tilak (white chandan U-shape with central red line)
        line(c, [(-12, -710), (-8, -668), (0, -660), (8, -668), (12, -710)], WHITE, 5)
        line(c, [(0, -715), (0, -662)], hexc("#E63946"), 4)
        
        # Majestic Kirita-Mukut (Grand Vishnu Crown, NO peacock feather!)
        rrect(c, -100, -765, 200, 34, 10)
        ink(c, gold, 5)
        smooth(c, [(-92, -760), (-70, -840), (-35, -825), (0, -910), (35, -825), (70, -840), (92, -760)], k=0.08)
        ink(c, gold, 5)
        smooth(c, [(-55, -775), (-35, -805), (0, -875), (35, -805), (55, -775)], k=0.08)
        rgba(c, GOLD_HI, 0.75)
        c.fill()
        gem(c, 0, -835, 16, gem_col)
        
        # Front Lower Arms
        L, R = (-115, -490), (115, -490)
        if pose == "bow" or pose == "accept":
            # Folded hands / compassionate acceptance of curse
            limb(c, [L, (-60, -420), (-20, -460)], skin, 38)
            limb(c, [R, (60, -420), (20, -460)], skin, 38)
            palm(c, 0, -460, gold, 26)
        elif pose == "vardan":
            # Right hand Abhaya Mudra / boon giving; Left hand Kaumodaki Gada resting down
            limb(c, [R, (160, -430), (140, -350)], skin, 38)
            palm(c, 140, -350, gold, 26) # Blessing palm
            glow(c, 140, -350, 48, GOLD_HI, 0.5)
            limb(c, [L, (-150, -420), (-130, -320)], skin, 38)
            hand(c, -130, -320, skin, 22)
            # Divine Gada head on ground
            line(c, [(-130, -320), (-130, -100)], gold, 12)
            ell(c, -130, -100, 30, 40)
            ink(c, gold, 4)
        else: # Default "bless"
            limb(c, [R, (150, -430), (135, -360)], skin, 38)
            palm(c, 135, -360, gold, 26)
            limb(c, [L, (-140, -420), (-120, -330)], skin, 38)
            hand(c, -120, -330, skin, 22)
            
        c.restore()

    dv.group(ctx, 1.0, _draw)


def vrinda(ctx, x, y, s=0.72, t=0.0, pose="pray", look=(0, 0), flip=False):
    """Pativrata Sati Vrinda rig: Devout ascetic yet royal queen, red suhagan saree with gold border,
    sacred bindi, gold bangles, spiritual aura."""
    def _draw():
        c = ctx
        c.save()
        c.translate(x, y)
        if flip:
            c.scale(-s, s)
        else:
            c.scale(s, s)
            
        skin = VRINDA_SKIN
        saree = VRINDA_SAREE
        gold = GOLD
        
        # Spiritual Pativrata aura
        glow(c, 0, -500, 240, VRINDA_AURA, 0.35 + 0.06 * math.sin(t * 2.5))
        
        # Feet
        for fx in (-36, 36):
            ell(c, fx, -12, 34, 15)
            ink(c, skin)
            line(c, [(fx - 18, -22), (fx, -18), (fx + 18, -22)], gold, 4)
            
        # Red Saree skirt
        skirt = [(-95, -300), (95, -300), (120, -180), (135, -35), (50, -25), (0, -45), (-50, -25), (-135, -35), (-120, -180)]
        smooth(c, skirt)
        ink(c, saree)
        line(c, [(132, -38), (50, -28), (0, -48), (-50, -28), (-132, -38)], gold, 9)
        
        # Torso & Saree Pallu drape
        smooth(c, [(-85, -450), (-40, -470), (40, -470), (85, -450), (85, -380), (70, -295), (-70, -295), (-85, -380)])
        ink(c, saree)
        # Diagonal gold-bordered pallu across chest
        smooth(c, [(-90, -455), (-50, -470), (80, -340), (60, -310)], k=0.1)
        ink(c, gold, 4)
        
        # Neck & Head
        rrect(c, -22, -510, 44, 48, 10)
        ink(c, skin)
        ell(c, 0, -560, 80, 90)
        ink(c, skin)
        sheen(c, -25, -600, 30, 20, 0.14)
        
        # Hair knot behind
        ell(c, 0, -600, 90, 60)
        ink(c, hexc("#1A0F0D"))
        
        # Eyes
        for side in (-1, 1):
            eye(c, side * 28, -565, 20, 22, t, look=look, iris=hexc("#2B1810"), seed=4)
            line(c, [(side * 10, -596), (side * 28, -604), (side * 48, -598)], hexc("#1A0F0D"), 5)
            
        line(c, [(2, -562), (-4, -545), (3, -542)], shade(skin, 0.7), 3)
        # Lips
        c.move_to(-14, -526)
        if pose == "shraap":
            # Expressive mouth shouting curse
            c.curve_to(-6, -516, 6, -516, 14, -526)
            c.set_line_width(4)
            rgba(c, hexc("#961B28"))
            c.stroke()
        else:
            c.curve_to(-6, -520, 6, -520, 14, -526)
            c.set_line_width(3)
            rgba(c, hexc("#B82838"))
            c.stroke()
            
        # Vermilion Bindi & Sindoor
        circle(c, 0, -582, 6, hexc("#E62232"))
        line(c, [(0, -625), (0, -595)], hexc("#E62232"), 4)
        
        # Delicate maang-tika & earrings
        circle(c, 0, -625, 5, gold)
        for side in (-1, 1):
            circle(c, side * 84, -540, 8, gold)
            
        # Arms based on pose
        L, R = (-80, -440), (80, -440)
        if pose == "shraap":
            # Right arm raised with pointing curse index; Left arm curled in grief
            limb(c, [R, (130, -470), (160, -540)], skin, 30)
            hand(c, 160, -540, skin, 20)
            # Flash of tapasya wrath at fingertips
            glow(c, 160, -540, 45, hexc("#FF3A2A"), 0.7)
            limb(c, [L, (-110, -420), (-90, -360)], skin, 30)
            hand(c, -90, -360, skin, 18)
        elif pose == "shock":
            # Hands raised to chest in disbelief
            limb(c, [R, (80, -420), (45, -450)], skin, 30)
            hand(c, 45, -450, skin, 18)
            limb(c, [L, (-80, -420), (-45, -450)], skin, 30)
            hand(c, -45, -450, skin, 18)
        elif pose == "meditate":
            # Seated in deep tapasya
            limb(c, [R, (90, -380), (40, -320)], skin, 30)
            palm(c, 40, -320, skin, 20)
            limb(c, [L, (-90, -380), (-40, -320)], skin, 30)
            palm(c, -40, -320, skin, 20)
        else: # "pray"
            limb(c, [R, (60, -390), (20, -420)], skin, 30)
            limb(c, [L, (-60, -390), (-20, -420)], skin, 30)
            palm(c, 0, -420, skin, 22)
            
        c.restore()

    dv.group(ctx, 1.0, _draw)


def jalandhar_king(ctx, x, y, s=0.76, t=0.0, pose="roar", look=(0, 0), flip=False):
    """Asura King Jalandhar rig: Towering, dark-bronze muscular form, fierce spiked iron crown,
    dark demonic armor, brandishing a massive war scimitar."""
    def _draw():
        c = ctx
        c.save()
        c.translate(x, y)
        if flip:
            c.scale(-s, s)
        else:
            c.scale(s, s)
            
        skin = JALANDHAR_SKIN
        armor = JALANDHAR_ARMOR
        
        # Fierce asuric dark red aura
        glow(c, 0, -520, 260, hexc("#80151E"), 0.4)
        
        # Boots
        for fx in (-55, 55):
            ell(c, fx, -16, 48, 22)
            ink(c, hexc("#1A1D24"))
            
        # War skirt
        skirt = [(-125, -340), (125, -340), (145, -200), (160, -40), (70, -25), (0, -50), (-70, -25), (-160, -40), (-145, -200)]
        smooth(c, skirt)
        ink(c, armor)
        line(c, [(155, -42), (70, -28), (0, -54), (-70, -28), (-155, -42)], hexc("#8C222C"), 12)
        
        # Muscular Torso & heavy iron breastplate
        smooth(c, [(-135, -510), (-65, -535), (65, -535), (135, -510), (140, -435), (110, -335), (-110, -335), (-140, -435)])
        ink(c, armor)
        line(c, [(0, -525), (0, -350)], hexc("#8C222C"), 8)
        
        # Neck & Fierce Head
        rrect(c, -35, -575, 70, 65, 14)
        ink(c, skin)
        ell(c, 0, -640, 105, 115)
        ink(c, skin)
        
        # Sharp fierce eyes & fiery pupils
        for side in (-1, 1):
            eye(c, side * 42, -645, 26, 28, t, look=look, iris=hexc("#FF2A1A"), seed=5)
            line(c, [(side * 15, -688), (side * 42, -700), (side * 72, -685)], hexc("#150A0A"), 8)
            
        line(c, [(2, -640), (-6, -615), (5, -610)], shade(skin, 0.6), 5)
        # Snarl
        c.move_to(-24, -590)
        c.curve_to(-10, -580, 10, -580, 24, -590)
        c.set_line_width(5)
        rgba(c, hexc("#520C12"))
        c.stroke()
        
        # Asuric Jagged Iron Crown
        rrect(c, -110, -760, 220, 36, 10)
        ink(c, armor, 5)
        smooth(c, [(-100, -755), (-80, -855), (-40, -810), (0, -890), (40, -810), (80, -855), (100, -755)], k=0.05)
        ink(c, armor, 5)
        line(c, [(-80, -855), (-40, -810), (0, -890), (40, -810), (80, -855)], hexc("#FF2A1A"), 5)
        
        # Arms & Massive Scimitar
        L, R = (-130, -495), (130, -495)
        if pose == "roar":
            limb(c, [R, (180, -480), (170, -600)], skin, 46)
            hand(c, 170, -600, skin, 26)
            # Scimitar blade
            smooth(c, [(170, -600), (220, -740), (280, -820), (260, -850), (190, -750), (160, -610)], closed=True)
            ink(c, hexc("#D0D5E0"))
            line(c, [(160, -610), (260, -850)], hexc("#FF4422"), 4)
            limb(c, [L, (-180, -450), (-160, -380)], skin, 46)
            hand(c, -160, -380, skin, 26)
        else: # Stand
            limb(c, [R, (160, -440), (150, -340)], skin, 46)
            hand(c, 150, -340, skin, 26)
            limb(c, [L, (-160, -440), (-150, -340)], skin, 46)
            hand(c, -150, -340, skin, 26)
            
        c.restore()

    dv.group(ctx, 1.0, _draw)


def shaligram_stone(ctx, x, y, s=1.0, t=0.0):
    """Sacred Shaligram: Polished, smooth oval black sacred stone with natural golden spiral chakra imprint."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    
    # Celestial golden halo radiating around the stone
    glow(ctx, 0, 0, 160, GOLD_HI, 0.6 + 0.1 * math.sin(t * 3.0))
    
    # Smooth sacred black ammonite body
    ell(ctx, 0, 0, 85, 105)
    ink(ctx, SHALIGRAM_STONE)
    sheen(ctx, -28, -35, 38, 52, 0.22)
    
    # Natural Golden Chakra imprint / spiral fossil markings
    ctx.save()
    ctx.set_line_width(5)
    ctx.set_source_rgb(*SHALIGRAM_GOLD)
    ctx.arc(0, 0, 32, 0, math.tau)
    ctx.stroke()
    for sp in range(6):
        ang = sp * (math.tau / 6) + t * 0.5
        line(ctx, [(0, 0), (30 * math.cos(ang), 30 * math.sin(ang))], SHALIGRAM_GOLD, 4)
    gem(ctx, 0, 0, 8, GOLD_HI)
    ctx.restore()
    
    # Golden floral offerings at base
    for fl in (-40, -15, 15, 40):
        circle(ctx, fl, 95, 7, hexc("#FFAA22"))
    ctx.restore()


def tulsi_plant(ctx, x, y, s=1.0, t=0.0):
    """Holy Tulsi Vrindavan pot & sacred green Tulsi plant with Manjari (seeds)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    
    # Divine green-gold glow
    glow(ctx, 0, -120, 180, hexc("#55D468"), 0.45)
    
    # Terracotta Vrindavan base pot (traditional temple square pot)
    smooth(ctx, [(-65, 0), (65, 0), (55, -80), (75, -85), (75, -100), (-75, -100), (-75, -85), (-55, -80)], closed=True)
    ink(ctx, POT_BRONZE)
    # Sacred yellow chandan band on pot
    line(ctx, [(-72, -92), (72, -92)], hexc("#FFCC33"), 6)
    
    # Tulsi branches & aromatic green leaves
    ctx.save()
    ctx.translate(0, -100)
    # Main stem
    line(ctx, [(0, 0), (0, -140)], hexc("#3B2212"), 8)
    
    # Leaf clusters
    for idx, (bx, by, ang) in enumerate([
        (-25, -40, -0.6), (25, -40, 0.6),
        (-35, -80, -0.7), (35, -80, 0.7),
        (-20, -120, -0.5), (20, -120, 0.5),
        (0, -150, 0.0)
    ]):
        sway = 0.05 * math.sin(t * 2.0 + idx)
        ctx.save()
        ctx.translate(bx, by)
        ctx.rotate(ang + sway)
        ell(ctx, 0, 0, 18, 30)
        ink(ctx, TULSI_GREEN)
        sheen(ctx, -5, -6, 7, 14, 0.25)
        # Tulsi Manjari (holy aromatic flower cluster)
        if idx >= 4:
            line(ctx, [(0, -25), (0, -42)], hexc("#90B865"), 4)
            for m in (-4, 0, 4):
                circle(ctx, m, -36, 3, hexc("#B58842"))
        ctx.restore()
    ctx.restore()
    ctx.restore()

# ============================================================ Scene Implementations

class Hook(Cued):
    """Scene 1: 'एक पतिव्रता स्त्री के श्राप से... खुद भगवान विष्णु, पत्थर बन गए!'
    Visual: Shocking transformation - radiant Chaturbhuj Vishnu bows compassionately
    under Vrinda's agonized curse, turning into the dark Shaligram stone."""
    def beats(self, d):
        # Spoken cues: SHRAAP SE -> VISHNU -> PATTHAR BAN GAYE
        return [
            self.cue("SHRAAP SE...", d * 0.28),
            self.cue("VISHNU,", d * 0.55),
            self.cue("PATTHAR BAN GAYE!", d * 0.82),
        ]
        
    def events(self, d):
        b = self.beats(d)
        return [
            (b[0], "whoosh"),
            (b[1], "shimmer"),
            (b[2], "boom"),
        ]
        
    def draw(self, ctx, t, d):
        b = self.beats(d)
        vaikuntha_sky(ctx, t)
        
        # Ground
        smooth(ctx, [(0, GROUND - 10), (W, GROUND - 10), (W, H), (0, H)], closed=True)
        ink(ctx, hexc("#100818"))
        
        # Weeping Vrinda on left casting curse
        vrinda(ctx, 280, GROUND - 10, 0.74, t, pose="shraap", look=(0.6, -0.3), flip=False)
        
        # Transformation of Vishnu into Shaligram stone
        t_curse = b[2]
        if t < t_curse:
            # Vishnu bows compassionately
            pose = "bow" if t >= b[0] else "bless"
            chaturbhuj_vishnu(ctx, 760, GROUND - 10, 0.76, t, pose=pose, look=(-0.6, -0.2), flip=True)
        else:
            # Dramatic cosmic burst on "PATTHAR BAN GAYE" and Shaligram stone manifests
            u = clamp((t - t_curse) / 0.5)
            # Flash & screen shake
            flash = (1.0 - u) * 0.6
            if flash > 0.05:
                ctx.save()
                ctx.set_source_rgba(1, 1, 1, flash)
                ctx.paint()
                ctx.restore()
                
            # Shaligram stone on altar/lotus seat
            s_scale = lerp(0.4, 1.25, ease_out_back(u))
            shaligram_stone(ctx, 760, GROUND - 130, s_scale, t)


class Asur(Cued):
    """Scene 2: 'असुर जालंधर अजेय था... पत्नी वृंदा के पतिव्रत से।'
    Visual: Towering Asura king Jalandhar raises heavy scimitar on left;
    Vrinda meditates in an unyielding circle of sacred fire on right."""
    def beats(self, d):
        return [
            self.cue("JALANDHAR", d * 0.25),
            self.cue("AJEYA THA...", d * 0.45),
            self.cue("PATIVRAT SE.", d * 0.80),
        ]
        
    def events(self, d):
        b = self.beats(d)
        return [
            (b[0], "thud"),
            (b[1], "whoosh"),
            (b[2], "shimmer"),
        ]
        
    def draw(self, ctx, t, d):
        b = self.beats(d)
        asur_battle_sky(ctx, t)
        
        # Ground
        smooth(ctx, [(0, GROUND - 10), (W, GROUND - 10), (W, H), (0, H)], closed=True)
        ink(ctx, hexc("#140407"))
        
        # Jalandhar dominating left side
        j_scale = lerp(0.72, 0.80, ease_out_cubic(clamp(t / (b[1] + 0.1))))
        jalandhar_king(ctx, 320, GROUND - 10, j_scale, t, pose="roar", look=(0.6, -0.2), flip=False)
        
        # Vrinda meditates peacefully in sacred tapasya fire ring on right
        vrinda(ctx, 780, GROUND - 10, 0.72, t, pose="meditate", look=(0, 0), flip=True)
        
        # Golden Tapasya protective fire ring around Vrinda
        ctx.save()
        ctx.translate(780, GROUND - 30)
        glow(ctx, 0, -80, 190, GOLD_HI, 0.5 + 0.15 * math.sin(t * 4.0))
        for f in range(12):
            fang = f * (math.tau / 12) + t * 0.8
            fx = 120 * math.cos(fang)
            fy = 30 * math.sin(fang)
            ell(ctx, fx, fy - 20, 16, 32)
            rgba(ctx, hexc("#FFAA22"), 0.65)
            ctx.fill()
        ctx.restore()


class Chhal(Cued):
    """Scene 3: 'देवताओं को बचाने, विष्णु ने जालंधर का रूप धरकर, वो व्रत तोड़ा।'
    Visual: Vishnu gracefully projects a luminous illusion disguise of Jalandhar
    to preserve Dharma; Vrinda rises in astonishment. Modest and reverent."""
    def beats(self, d):
        return [
            self.cue("DEVTAON KO", d * 0.15),
            self.cue("ROOP DHARKAR,", d * 0.52),
            self.cue("VRAT TODA.", d * 0.85),
        ]
        
    def events(self, d):
        b = self.beats(d)
        return [
            (b[0], "soft_thud"),
            (b[1], "shimmer"),
            (b[2], "whoosh"),
        ]
        
    def draw(self, ctx, t, d):
        b = self.beats(d)
        sacred_ashram_sky(ctx, t)
        
        # Sacred hermitage ground
        smooth(ctx, [(0, GROUND - 10), (W, GROUND - 10), (W, H), (0, H)], closed=True)
        ink(ctx, hexc("#0C1514"))
        
        # Vrinda on right looking in surprise
        v_pose = "shock" if t >= b[1] else "pray"
        vrinda(ctx, 780, GROUND - 10, 0.72, t, pose=v_pose, look=(-0.6, -0.2), flip=True)
        
        # Vishnu illusionary disguise transformation
        t_shift = b[1]
        u = clamp((t - t_shift) / 0.8)
        
        if t < t_shift:
            # Celestial Vishnu standing before ashram
            chaturbhuj_vishnu(ctx, 320, GROUND - 10, 0.74, t, pose="bless", look=(0.6, -0.2), flip=False)
        else:
            # Luminous celestial shimmer veil revealing the disguise
            glow(ctx, 320, GROUND - 320, 260, GOLD_HI, 0.4 * (1.0 - u))
            # Disguised appearance (royal Jalandhar standing calmly with hands open, no scimitar)
            jalandhar_king(ctx, 320, GROUND - 10, 0.74, t, pose="stand", look=(0.6, -0.2), flip=False)


class Shraap(Cued):
    """Scene 4: 'सच जानते ही वृंदा ने श्राप दिया... पत्थर बन जाओ!'
    Visual: The disguise dissolves; Vrinda, overcome with sorrow and righteous fury,
    raises her hand casting the fateful curse upon Vishnu."""
    def beats(self, d):
        return [
            self.cue("SACH JAANTE HI", d * 0.18),
            self.cue("VRINDA NE", d * 0.42),
            self.cue("PATTHAR BAN JAO!", d * 0.78),
        ]
        
    def events(self, d):
        b = self.beats(d)
        return [
            (b[0], "whoosh"),
            (b[1], "alarm"),
            (b[2], "zap"),
        ]
        
    def draw(self, ctx, t, d):
        b = self.beats(d)
        vaikuntha_sky(ctx, t)
        
        smooth(ctx, [(0, GROUND - 10), (W, GROUND - 10), (W, H), (0, H)], closed=True)
        ink(ctx, hexc("#120818"))
        
        # Vrinda on left steps forward with fiery grief
        vrinda(ctx, 280, GROUND - 10, 0.75, t, pose="shraap", look=(0.7, -0.2), flip=False)
        
        # Beam of tapasya wrath firing towards Vishnu on "PATTHAR BAN JAO!"
        if t >= b[2]:
            u = clamp((t - b[2]) / 0.4)
            glow(ctx, 540, GROUND - 380, 180, hexc("#FF3A2A"), 0.6)
            line(ctx, [(380, GROUND - 420), (660, GROUND - 420)], hexc("#FFAA44"), 8)
            
        # True Chaturbhuj Vishnu stands on right, head bowed in sorrowful acceptance
        chaturbhuj_vishnu(ctx, 760, GROUND - 10, 0.76, t, pose="accept", look=(-0.6, 0.2), flip=True)


class Vardan(Cued):
    """Scene 5: 'प्रभु शालिग्राम बने, और वरदान दिया... तुलसी बनकर, तुम सदा मेरी पूजा में रहोगी।'
    Visual: Prabhu transforms into Shaligram stone; alongside, the sacred Tulsi plant
    manifests, embraced by divine rays of eternity."""
    def beats(self, d):
        return [
            self.cue("SHALIGRAM BANE,", d * 0.22),
            self.cue("VARDAN DIYA...", d * 0.48),
            self.cue("TULSI BANKAR,", d * 0.72),
            self.cue("POOJA MEIN", d * 0.88),
        ]
        
    def events(self, d):
        b = self.beats(d)
        return [
            (b[0], "boom"),
            (b[1], "shimmer"),
            (b[2], "ghanti"),
            (b[3], "shimmer"),
        ]
        
    def draw(self, ctx, t, d):
        b = self.beats(d)
        vaikuntha_sky(ctx, t)
        
        smooth(ctx, [(0, GROUND - 10), (W, GROUND - 10), (W, H), (0, H)], closed=True)
        ink(ctx, hexc("#100A1A"))
        
        # Golden altar platform at center
        rrect(ctx, 260, GROUND - 40, 560, 40, 10)
        ink(ctx, GOLD, 6)
        
        # Shaligram Stone on right of altar
        shaligram_stone(ctx, 680, GROUND - 140, 1.15, t)
        
        # Sacred Tulsi plant manifesting on left on "TULSI BANKAR"
        t_tulsi = b[2]
        if t >= t_tulsi:
            u = clamp((t - t_tulsi) / 0.5)
            t_scale = lerp(0.3, 1.1, ease_out_back(u))
            tulsi_plant(ctx, 400, GROUND - 40, t_scale, t)
        else:
            # Vrinda peacefully dissolving into golden light
            vrinda(ctx, 400, GROUND - 10, 0.72, t, pose="pray", look=(0.6, -0.2), flip=False)


class Loop(Cued):
    """Scene 6: 'इसीलिए हर कार्तिक, तुलसी और शालिग्राम का विवाह होता है... क्योंकि'
    Visual: Beautiful Tulsi Vivah mandap in Kartika evening light;
    final 0.45s seamless crossfade back to Scene 1 opening frame."""
    def beats(self, d):
        return [
            self.cue("ISILIYE HAR", d * 0.20),
            self.cue("VIVAH HOTA", d * 0.55),
            self.cue("KYUNKI", d * 0.88),
        ]
        
    def events(self, d):
        b = self.beats(d)
        return [
            (b[0], "ghanti"),
            (b[1], "shimmer"),
            (b[2], "whoosh"),
        ]
        
    def draw(self, ctx, t, d):
        b = self.beats(d)
        sacred_ashram_sky(ctx, t)
        
        # Holy Kartika evening festival ambiance
        smooth(ctx, [(0, GROUND - 10), (W, GROUND - 10), (W, H), (0, H)], closed=True)
        ink(ctx, hexc("#0E1618"))
        
        # Festival Diya lamps along the ground
        for dx in (160, 260, 820, 920):
            dv.diya(ctx, dx, GROUND - 20, 0.7, t)
            
        # Festive Vivah Mandap altar
        rrect(ctx, 280, GROUND - 50, 520, 50, 12)
        ink(ctx, GOLD, 6)
        
        # Sacred Tulsi plant (left) with auspicious red bridal chunri veil
        tulsi_plant(ctx, 420, GROUND - 50, 1.1, t)
        # Red wedding veil ribbon
        line(ctx, [(380, GROUND - 180), (460, GROUND - 180)], VRINDA_SAREE, 10)
        
        # Sacred Shaligram Stone (right) crowned with golden chandan
        shaligram_stone(ctx, 660, GROUND - 150, 1.1, t)
        
        # Golden sacred thread / garland connecting Tulsi and Shaligram
        line(ctx, [(420, GROUND - 150), (540, GROUND - 110), (660, GROUND - 150)], GOLD_HI, 6)
        
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
    "asur": Asur,
    "chhal": Chhal,
    "shraap": Shraap,
    "vardan": Vardan,
    "loop": Loop,
}
SCENES = SCENE_CLASSES

# ============================================================ Thumbnail & Upload Kit

def thumbnail(ctx):
    vaikuntha_sky(ctx, 0.5)
    glow(ctx, 540, 880, 520, GOLD_HI, 0.6)
    
    # Left: Devout Vrinda casting curse with tears and tapasya aura
    vrinda(ctx, 240, 1260, 0.78, 0.5, pose="shraap", look=(0.7, -0.2), flip=False)
    
    # Center-Right: Chaturbhuj Vishnu transforming
    chaturbhuj_vishnu(ctx, 780, 1260, 0.78, 0.5, pose="bow", look=(-0.6, 0.1), flip=True)
    
    # Center: Shaligram Stone glowing brightly
    shaligram_stone(ctx, 520, 1150, 1.25, 0.5)
    
    # Cinematic contrast gradients
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
    
    # Title Typography (Capitalized Roman, Impact font, zero tofu squares)
    text(ctx, "VRINDA KA SHRAAP", 540, 230, 115, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "VISHNU BANE PATTHAR", 540, 370, 105, hexc("#FF4A3A"), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=24)
    text(ctx, "DIVYA RAHASYA", 540, 1820, 42, GOLD_HI, a=0.85)


UPLOAD = {
    "thumb_text": "VISHNU BANE PATTHAR",
    "titles": [
        "Ek Pativrata Ke Shraap Se Vishnu Bane Patthar? #shorts",
        "Tulsi Vivah Rahasya: Vishnu Kyun Bane Shaligram?",
        "Vrinda Ka Shraap: Jab Bhagavan Vishnu Ko Patthar Banna Pada",
        "Kyun Hota Hai Tulsi Aur Shaligram Ka Vivah? #devuthani",
        "Jalandhar Vadh Aur Vrinda Ka Shraap: Asli Rahasya",
    ],
    "queries": [
        "tulsi vivah katha dev uthani ekadashi",
        "vrinda ke shraap se vishnu shaligram kyun bane",
        "jalandhar vadh vishnu chhal katha",
        "tulsi shaligram vivah rahasya shiva purana",
    ],
    "description": (
        "Dev Uthani Ekadashi aur Tulsi Vivah ka sabse bada rahasya!\n\n"
        "Asur Jalandhar ko harana asambhav tha kyunki uski patni Vrinda ka pativrat atoot tha. "
        "Devtaon ki raksha ke liye Bhagavan Vishnu ne roop badal kar wo vrat toda. "
        "Sach jaan kar pukaar uthi Vrinda aur diya krodh mein shraap—patthar ban jao!\n\n"
        "Bhagavan ne shraap swikar kiya, Shaligram bane aur vardan diya ki Tulsi ke bina unki pooja sada adhoori rahegi.\n\n"
        "Sources: Shiva Purana (Rudra Samhita, Yuddha Khanda) & Padma Purana (Uttara Khanda).\n\n"
        "Comment mein likhiye: Jai Tulsi Maharani! Jai Shri Hari Vishnu! 🙏\n\n"
        "#Shorts #TulsiVivah #DevUthani #Shaligram #Vishnu #DivyaRahasya #SanatanDharma"
    ),
    "tags": [
        "tulsi vivah", "shaligram", "vrinda", "jalandhar", "vishnu", "dev uthani ekadashi",
        "shiva purana", "padma purana", "divya rahasya", "sanatan dharma", "mythology"
    ],
    "hashtags": ["#Shorts", "#TulsiVivah", "#DevUthani"],
}
