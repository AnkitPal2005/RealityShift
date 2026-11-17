"""Arjun Ka Rath Bhashm: Mahabharat Yuddh Ke Baad Rath Rakh Kyun Bana? (~30-33s katha, six scenes).

Usage (from SanatanKatha/):
  python make.py arjun_rath --preview       # preview contact sheet & thumbnail
  python make.py arjun_rath --kiki-export   # exports clean voice text files
  python make.py arjun_rath --kiki-split    # splits user audio into lines
  python make.py arjun_rath                 # final render with music & devta characters

Rahasya:
After 18 ferocious days of the Mahabharata war, when victory was sealed for the Pandavas,
Bhagavan Shri Krishna commanded Arjuna to dismount immediately before himself.
Per ancient warrior code, the charioteer (Sarathi) always dismounts first.
Arjuna obeyed reluctantly. But the moment Shri Krishna stepped off the chariot and released
the divine reins, the celestial chariot instantly burst into cosmic flames and was reduced to ashes.
A shocked Arjuna learned the truth: the celestial weapons (Divyastras) of Bhishma, Drona, and Karna
had incinerated the chariot long ago during the war; it was only sustained in physical form by
the divine feet and cosmic energy of Shri Krishna!
"""

import math
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cairo

from core import engine, katha, upload_kit
from core.katha import *  # noqa: F401,F403
import core.devta as dv
from core.devta import group, place, halo, smooth, ink, ell, gem, limb, hand, sheen, eye, shade

TOPIC = "ARJUN RATH BHASHM RAHASYA"
OUTPUTS = {"edge": "arjun_rath_short.mp4"}
MUSIC_STYLE = "tension"   # Dramatic mystery & cosmic revelation bed
MUSIC_BPM = 76            # Distinct intense tempo
MUSIC_VOLUME = 0.12       # Clear voiceover clarity
TAIL_PAD = 0.04           # Zero awkward silence between chunks
MAX_GAP = 0.04            # Seamless speech flow

WHITE = (1.0, 1.0, 1.0)
RED_GEM = hexc("#D61F3A")
GOLD_HI = hexc("#FFE066")
FIRE_ORANGE = hexc("#FF5500")
FIRE_YELLOW = hexc("#FFCC00")
FIRE_RED = hexc("#D81B1B")
ASH_COLOR = hexc("#2B2D42")
SKY_CRIMSON = hexc("#4A1525")
SKY_AMBER = hexc("#C85A17")

SOURCES = [
    "Mahabharata (Shalya Parva, Section 62): After the war concludes, Krishna commands Arjuna to dismount first with his Gandiva. When Krishna dismounts, the Kapi-dhwaja chariot bursts into flames.",
    "Bhagavata Purana & Vyasa Mahabharata: Krishna reveals to Arjuna that the chariot had already been consumed by the Brahmastras of Bhishma and Drona and the weapons of Karna, but was preserved only by His divine presence.",
    "Sanatan Dharma Philosophy: Illustrates supreme divine protection where God silently absorbs all destructive forces shielding His true devotee.",
]


# -----------------------------------------------------------------------------
# Background: Kurukshetra Battlefield Twilight
# -----------------------------------------------------------------------------
def kurukshetra_bg(ctx, t, intense=False):
    """Dramatic Kurukshetra battlefield sky at twilight with smoke and war embers."""
    if intense:
        dv.sky(ctx, hexc("#1A050B"), hexc("#6A1B29"), hexc("#D94A1E"), 0.56)
        glow(ctx, 540, 720, 440, hexc("#FF5500"), 0.45)
        circle(ctx, 540, 720, 85, hexc("#FFAA33"), 0.85)
    else:
        dv.sky(ctx, hexc("#10081C"), hexc("#481E32"), hexc("#BD5324"), 0.56)
        glow(ctx, 540, 700, 380, hexc("#FF7B25"), 0.35)
        circle(ctx, 540, 700, 75, hexc("#FFD580"), 0.80)

    # Distant smoky haze & silhouette hills
    ctx.move_to(0, 910)
    for x in range(0, W + 1, 50):
        ctx.line_to(x, 910 - 28 * math.sin(x / 180 + 0.8) - 15 * math.cos(x / 70))
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    rgba(ctx, hexc("#28121E") if intense else hexc("#1C1020"))
    ctx.fill()

    # Battlefield silhouettes: distant flags and spears
    ctx.set_line_width(3)
    for fx, fh in [(120, 140), (280, 110), (840, 150), (960, 120)]:
        line(ctx, [(fx, 910), (fx, 910 - fh)], hexc("#150A10"), 4)
        # Triangular torn war banner
        ctx.move_to(fx, 910 - fh)
        ctx.line_to(fx + 35 + 8 * math.sin(t * 3 + fx), 910 - fh + 15)
        ctx.line_to(fx, 910 - fh + 30)
        ctx.close_path()
        rgba(ctx, hexc("#3D141C"))
        ctx.fill()

    # Ground plain with war-trodden earth
    ctx.move_to(0, 1030)
    for x in range(0, W + 1, 40):
        ctx.line_to(x, 1030 - 15 * math.sin(x / 130 + 1.2))
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    rgba(ctx, hexc("#180A08") if intense else hexc("#120B10"))
    ctx.fill()

    # Floating battlefield sparks/embers
    for i in range(22):
        sp_x = (i * 157 + int(t * 90)) % W
        sp_y = 1100 - (int(t * 110 + i * 47) % 650)
        spark_r = 2.5 + 1.5 * math.sin(t * 5 + i)
        circle(ctx, sp_x, sp_y, spark_r, FIRE_YELLOW if i % 2 == 0 else FIRE_ORANGE, 0.65)


# -----------------------------------------------------------------------------
# Props & Characters
# -----------------------------------------------------------------------------
def rath_chariot(ctx, x, y, s, t, burn=0.0, a=1.0):
    """The grand golden Kapi-Dhwaja chariot. If burn > 0, roars into flames and collapses."""
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)

        # Dissolve factor when burning
        alive_alpha = max(0.0, 1.0 - burn * 1.2)

        if alive_alpha > 0.05:
            # Chariot Main Body (Carved Gold & Teak wood)
            # Big rear spoked wheel
            wheel_y = -80
            for side in (-120, 120):
                circle(ctx, side, wheel_y, 75, GOLD, 0.95 * alive_alpha)
                circle(ctx, side, wheel_y, 60, hexc("#5A2008"), 0.95 * alive_alpha)
                circle(ctx, side, wheel_y, 22, GOLD_HI, 0.95 * alive_alpha)
                # Spokes
                for ang_idx in range(8):
                    rot = ang_idx * (math.pi / 4)
                    line(ctx, [(side + 20 * math.cos(rot), wheel_y + 20 * math.sin(rot)),
                               (side + 58 * math.cos(rot), wheel_y + 58 * math.sin(rot))], GOLD, 4 * alive_alpha)

            # Chariot chassis platform
            chassis = [(-220, -110), (220, -110), (190, -170), (140, -220), (-160, -220), (-200, -160)]
            smooth(ctx, chassis)
            ink(ctx, GOLD, 6, a=alive_alpha)
            # Ornate golden reliefs
            rrect(ctx, -180, -190, 360, 45, 12)
            ink(ctx, hexc("#E8A020"), 4, a=alive_alpha)
            gem(ctx, 0, -168, 14, RED_GEM)

            # Chariot Canopy / Dome pillars
            line(ctx, [(-130, -220), (-130, -420)], GOLD, 8 * alive_alpha)
            line(ctx, [(130, -220), (130, -420)], GOLD, 8 * alive_alpha)
            line(ctx, [(0, -220), (0, -440)], GOLD, 6 * alive_alpha)

            # Golden Arch Canopy
            canopy = [(-160, -420), (160, -420), (110, -500), (0, -540), (-110, -500)]
            smooth(ctx, canopy)
            ink(ctx, GOLD, 5, a=alive_alpha)
            gem(ctx, 0, -480, 16, RED_GEM)

            # Hanuman Ji's Sacred Banner (Kapi Dhwaja) atop the chariot mast
            line(ctx, [(0, -540), (0, -740)], GOLD, 6 * alive_alpha)
            flag_wave = 12 * math.sin(t * 4.5)
            flag_pts = [(0, -730), (120 + flag_wave, -690), (0, -650)]
            smooth(ctx, flag_pts)
            ink(ctx, hexc("#FF5500"), 4, a=alive_alpha)
            # Small golden Hanuman symbol on the flag
            circle(ctx, 45 + flag_wave * 0.4, -690, 15, GOLD_HI, 0.9 * alive_alpha)

        # BURNING / EXPLODING EFFECTS (When burn > 0.0)
        if burn > 0.02:
            glow(ctx, 0, -260, 320 * (1 + burn * 0.5), FIRE_ORANGE, 0.7 * min(1.0, burn * 1.5))
            glow(ctx, 0, -200, 180 * (1 + burn * 0.4), FIRE_YELLOW, 0.85 * min(1.0, burn * 1.8))

            # Dynamic procedural fire flames
            num_flames = 16
            for idx in range(num_flames):
                fx = -190 + (idx * 26)
                base_h = 180 + 140 * math.sin(idx * 1.7 + t * 9.0)
                flame_h = base_h * clamp(burn * 1.4, 0.2, 1.2)
                curv = 25 * math.sin(t * 8.0 + idx)

                # Outer fire tongue
                ctx.move_to(fx - 22, -100)
                ctx.curve_to(fx - 15, -100 - flame_h * 0.6, fx + curv, -100 - flame_h, fx + curv, -100 - flame_h)
                ctx.curve_to(fx + curv, -100 - flame_h, fx + 15, -100 - flame_h * 0.6, fx + 22, -100)
                ctx.close_path()
                rgba(ctx, FIRE_RED if idx % 3 == 0 else FIRE_ORANGE, 0.75)
                ctx.fill()

                # Inner intense yellow core
                ctx.move_to(fx - 12, -100)
                ctx.curve_to(fx - 8, -100 - flame_h * 0.4, fx + curv * 0.6, -100 - flame_h * 0.75, fx + curv * 0.6, -100 - flame_h * 0.75)
                ctx.curve_to(fx + curv * 0.6, -100 - flame_h * 0.75, fx + 8, -100 - flame_h * 0.4, fx + 12, -100)
                ctx.close_path()
                rgba(ctx, FIRE_YELLOW, 0.9)
                ctx.fill()

            # Billowing black & gray smoke
            for s_idx in range(12):
                smk_x = -140 + (s_idx * 28) + 20 * math.sin(t * 2.5 + s_idx)
                smk_y = -350 - (s_idx * 35 * burn) - (int(t * 80 + s_idx * 30) % 250)
                smk_r = 45 + 25 * math.sin(s_idx + t)
                circle(ctx, smk_x, smk_y, smk_r, hexc("#1A1218"), 0.45 * clamp(burn * 1.5, 0.0, 0.8))

            # Collapsing ash pile
            if burn > 0.4:
                ash_w = 260 * burn
                ash_h = 35 * burn
                ell(ctx, 0, -10, ash_w, ash_h)
                rgba(ctx, ASH_COLOR, 0.85)
                ctx.fill()
                for c_idx in range(15):
                    cx = -180 + c_idx * 25
                    cy = -12 - 8 * abs(math.sin(c_idx * 1.3))
                    circle(ctx, cx, cy, 5, FIRE_ORANGE, 0.75 * math.sin(t * 6 + c_idx))

        ctx.restore()

    group(ctx, a, draw)


def arjuna(ctx, x, y, s, t, pose="bow", flip=False, a=1.0):
    """Maharathi Dhanurdhar Arjuna: Royal warrior mukut with ruby crest, armored chestplate, Gandiva."""
    def draw():
        place(ctx, x, y, s, t, flip)
        halo(ctx, 0, -650, 160, t, c=GOLD_HI)
        skin = hexc("#E8A87C")
        hair = dv.HAIR

        # Hair locks flowing behind shoulders
        for side in (-1, 1):
            smooth(ctx, [(side * 65, -690), (side * 115, -610), (side * 128, -530), (side * 118, -460), (side * 88, -470), (side * 80, -550)])
            ink(ctx, hair)
        ell(ctx, 0, -658, 108, 102)
        ink(ctx, hair)

        # Quiver with arrows slung across back
        ctx.save()
        ctx.translate(-70, -480)
        ctx.rotate(-0.35)
        rrect(ctx, -20, -120, 40, 240, 8)
        ink(ctx, hexc("#6E260E"), 5)
        # Golden arrow feathers protruding
        for arr_i in (-12, 0, 12):
            line(ctx, [(arr_i, -120), (arr_i, -165)], GOLD, 5)
            line(ctx, [(arr_i - 8, -155), (arr_i, -165), (arr_i + 8, -155)], RED_GEM, 4)
        ctx.restore()

        # Strong warrior feet & greaves (armored boots)
        for fx in (-48, 48):
            ell(ctx, fx, -14, 44, 18)
            ink(ctx, skin)
            line(ctx, [(fx - 24, -28), (fx, -22), (fx + 24, -28)], GOLD, 7)

        # White/Saffron Dhoti
        dhoti = [(-112, -340), (112, -340), (130, -200), (145, -45), (60, -32), (0, -60), (-60, -32), (-145, -45), (-130, -200)]
        smooth(ctx, dhoti)
        ink(ctx, WHITE)
        line(ctx, [(140, -48), (60, -35), (0, -62), (-60, -35), (-140, -48)], GOLD, 8)

        # Golden Armored Kavach (Chestplate)
        chest = [(-118, -500), (-60, -525), (60, -525), (118, -500), (125, -425), (96, -340), (-96, -340), (-125, -425)]
        smooth(ctx, chest)
        ink(ctx, GOLD, 6)
        sheen(ctx, 0, -430, 75, 45, 0.2)
        # Warrior emblem on armor
        circle(ctx, 0, -430, 24, RED_GEM)
        circle(ctx, 0, -430, 16, GOLD_HI)

        # Angavastra sash
        smooth(ctx, [(-122, -502), (-82, -518), (112, -370), (92, -340)], k=0.1)
        ink(ctx, dv.SAFFRON, 4)

        # Kamarbandh
        rrect(ctx, -110, -360, 220, 32, 10)
        ink(ctx, GOLD, 5)
        gem(ctx, 0, -344, 9, RED_GEM)

        # Neck & Divine Warrior Face
        rrect(ctx, -30, -568, 60, 56, 12)
        ink(ctx, skin)
        ell(ctx, 0, -638, 90, 94)
        ink(ctx, skin)

        # Warrior Tilak (Red with sandalwood white dot)
        line(ctx, [(0, -710), (0, -670)], hexc("#D01010"), 7)
        circle(ctx, 0, -664, 4, WHITE)

        # Big Expressive Eyes
        eye_look = (0.2, 0.0) if flip else (-0.2, 0.0)
        if pose == "shock":
            eye_look = (0.0, -0.4)  # Eyes wide open looking up/straight
        for side in (-1, 1):
            eye(ctx, side * 34, -644, 22, 24, t, look=eye_look, iris=hexc("#2D1E16"), seed=1)
            line(ctx, [(side * 12, -670), (side * 34, -676), (side * 54, -670)], hexc("#1A100C"), 5)

        # Expressions (Mouth)
        if pose == "shock":
            # Shocked open 'O' mouth
            ell(ctx, 0, -572, 12, 16)
            ink(ctx, hexc("#521414"), 3)
        elif pose == "confused":
            # Slight curious tilt / frown
            line(ctx, [(-14, -574), (0, -570), (14, -576)], hexc("#6A1810"), 4)
        else:
            # Determined noble smile
            ctx.move_to(-16, -574)
            ctx.curve_to(-6, -566, 6, -566, 16, -574)
            ctx.set_line_width(4)
            rgba(ctx, hexc("#6A1810"))
            ctx.stroke()

        # Royal Warrior Mukut (Crown with sun crest and red jewels)
        mukut = [(-70, -715), (-50, -805), (0, -855), (50, -805), (70, -715), (0, -725)]
        smooth(ctx, mukut)
        ink(ctx, GOLD, 5)
        gem(ctx, 0, -785, 12, RED_GEM)
        gem(ctx, -32, -750, 8, hexc("#1FA35B"))
        gem(ctx, 32, -750, 8, hexc("#1FA35B"))

        # Poses & Weapons
        if pose == "bow":
            # Holding Gandiva bow with left arm, right hand resting
            limb(ctx, [(-108, -485), (-150, -420), (-140, -320)], skin, 34)
            hand(ctx, -140, -310, skin, 20)
            # Gandiva Bow (Massive ornate recurve bow)
            bow_x = -150
            ctx.move_to(bow_x, -580)
            ctx.curve_to(bow_x - 60, -450, bow_x - 60, -250, bow_x, -120)
            ctx.set_line_width(12)
            rgba(ctx, GOLD)
            ctx.stroke()
            line(ctx, [(bow_x, -580), (bow_x, -120)], WHITE, 3)

            # Right arm relaxed
            limb(ctx, [(108, -485), (140, -420), (130, -330)], skin, 34)
            hand(ctx, 130, -320, skin, 20)

        elif pose == "confused":
            # Left hand holding bow, right hand touching temple/head in doubt
            limb(ctx, [(-108, -485), (-140, -420), (-130, -320)], skin, 34)
            hand(ctx, -130, -310, skin, 20)
            # Right arm raised to chin/temple
            limb(ctx, [(108, -485), (150, -460), (70, -580)], skin, 34)
            hand(ctx, 60, -590, skin, 20)

        elif pose == "shock":
            # Both hands raised back in astonishment
            limb(ctx, [(-108, -485), (-160, -440), (-150, -360)], skin, 34)
            dv.palm(ctx, -150, -350, skin, ang=0.3, s=1.1)
            limb(ctx, [(108, -485), (160, -440), (150, -360)], skin, 34)
            dv.palm(ctx, 150, -350, skin, ang=-0.3, s=1.1)

        elif pose == "namaste":
            # Both hands folded in deep reverence / pranam
            limb(ctx, [(-108, -485), (-70, -440), (0, -410)], skin, 34)
            limb(ctx, [(108, -485), (70, -440), (0, -410)], skin, 34)
            smooth(ctx, [(-22, -430), (0, -470), (22, -430), (0, -390)])
            ink(ctx, skin, 4)

        ctx.restore()

    group(ctx, a, draw)


def krishna(ctx, x, y, s, t, pose="stand", flip=False, a=1.0):
    """Bhagavan Shri Krishna: Divine blue skin, pitambar, peacock feather mukut, Sarathi grace."""
    def draw():
        place(ctx, x, y, s, t, flip)
        halo(ctx, 0, -650, 185, t, c=GOLD_HI)
        skin = dv.KRISHNA_SKIN
        hair = dv.KRISHNA_HAIR

        # Hair behind shoulders
        for side in (-1, 1):
            smooth(ctx, [(side * 68, -700), (side * 120, -620), (side * 135, -540), (side * 125, -470), (side * 95, -480), (side * 85, -560)])
            ink(ctx, hair)
        ell(ctx, 0, -668, 114, 110)
        ink(ctx, hair)

        # Feet with golden anklets
        for fx in (-48, 48):
            ell(ctx, fx, -14, 44, 18)
            ink(ctx, skin)
            line(ctx, [(fx - 24, -28), (fx, -22), (fx + 24, -28)], GOLD, 7)

        # Pitambar Yellow Dhoti
        dhoti = [(-115, -340), (115, -340), (132, -200), (148, -44), (60, -32), (0, -62), (-60, -32), (-148, -44), (-132, -200)]
        smooth(ctx, dhoti)
        ink(ctx, dv.PITAMBAR)
        line(ctx, [(142, -48), (60, -35), (0, -64), (-60, -35), (-142, -48)], hexc("#E6A010"), 8)

        # Torso
        smooth(ctx, [(-120, -495), (-60, -518), (60, -518), (120, -495), (126, -425), (98, -335), (-98, -335), (-126, -425)])
        ink(ctx, skin)

        # Angavastra sash & Vaijayanti Mala
        smooth(ctx, [(-125, -500), (-85, -515), (115, -368), (95, -338)], k=0.1)
        ink(ctx, hexc("#FF5533"), 5)
        # Floral garland
        line(ctx, [(-75, -490), (-40, -450), (0, -430), (40, -450), (75, -490)], WHITE, 8)
        circle(ctx, 0, -425, 8, RED_GEM)

        # Kamarbandh
        rrect(ctx, -112, -362, 224, 32, 11)
        ink(ctx, GOLD, 5)
        gem(ctx, 0, -346, 9, RED_GEM)

        # Head & Divine Face
        rrect(ctx, -30, -568, 60, 56, 12)
        ink(ctx, skin)
        ell(ctx, 0, -638, 90, 96)
        ink(ctx, skin)

        # Vaishnava Urdhva Pundra Tilak
        line(ctx, [(0, -712), (0, -670)], hexc("#E2231A"), 8)
        circle(ctx, 0, -664, 4, GOLD)

        # Eyes & Divine Smile
        look_dir = (-0.2, 0.0) if flip else (0.2, 0.0)
        for side in (-1, 1):
            eye(ctx, side * 34, -644, 22, 24, t, look=look_dir, iris=hexc("#1B2A4A"), seed=0)
            line(ctx, [(side * 12, -670), (side * 34, -678), (side * 54, -672)], hexc("#0E1628"), 5)

        # Divine Serene / Knowing Smile
        ctx.move_to(-16, -568)
        ctx.curve_to(-6, -558, 6, -558, 16, -568)
        ctx.set_line_width(4.5)
        rgba(ctx, hexc("#8A1810"))
        ctx.stroke()

        # Mukut with Peacock Feather (Mor-Pankh)
        mukut = [(-70, -718), (-50, -808), (0, -858), (50, -808), (70, -718), (0, -728)]
        smooth(ctx, mukut)
        ink(ctx, GOLD, 5)
        gem(ctx, 0, -788, 11, RED_GEM)

        # Peacock feather (Mor-Pankh)
        pankh = [(0, -855), (35, -925), (0, -960), (-35, -925)]
        smooth(ctx, pankh)
        ink(ctx, hexc("#0E8A54"), 3)
        circle(ctx, 0, -925, 14, hexc("#1A408A"))
        circle(ctx, 0, -925, 7, GOLD_HI)

        # Arms & Poses
        if pose == "reins":
            # Holding chariot reins forward with authority
            limb(ctx, [(-110, -485), (-140, -420), (-110, -360)], skin, 34)
            dv.palm(ctx, -110, -350, skin, ang=0.1, s=1.0)
            limb(ctx, [(110, -485), (140, -420), (110, -360)], skin, 34)
            dv.palm(ctx, 110, -350, skin, ang=-0.1, s=1.0)
            # Reins rope
            line(ctx, [(-110, -350), (-250, -320)], GOLD_HI, 4)
            line(ctx, [(110, -350), (250, -320)], GOLD_HI, 4)

        elif pose == "bless":
            # Right hand raised in Abhaya mudra blessing, left hand resting on hip
            limb(ctx, [(110, -485), (155, -425), (135, -330)], skin, 34)
            dv.palm(ctx, 135, -320, skin, ang=-0.1, s=1.1)
            limb(ctx, [(-110, -485), (-145, -420), (-115, -330)], skin, 34)
            hand(ctx, -115, -320, skin, 20)

        elif pose == "command":
            # Pointing right index finger authoritatively, left arm relaxed
            limb(ctx, [(110, -485), (160, -430), (170, -360)], skin, 34)
            dv.palm(ctx, 170, -350, skin, ang=-0.3, s=1.1)
            limb(ctx, [(-110, -485), (-140, -420), (-120, -330)], skin, 34)
            hand(ctx, -120, -320, skin, 20)

        else:
            # Gentle standing pose
            limb(ctx, [(-110, -485), (-135, -415), (-115, -330)], skin, 34)
            hand(ctx, -115, -320, skin, 20)
            limb(ctx, [(110, -485), (135, -415), (115, -330)], skin, 34)
            hand(ctx, 115, -320, skin, 20)

        ctx.restore()

    group(ctx, a, draw)


# -----------------------------------------------------------------------------
# Story specification: 6 scenes (~30-33s total, 98 spoken Hindi words)
# -----------------------------------------------------------------------------
SPEC = [
    {
        "key": "hook",
        "text": "RATH SE NEECHE KUDO!",
        "visual": "Kurukshetra twilight: Krishna as Sarathi on chariot commanding Arjuna with high urgency",
        "vo": [
            ("tell", [
                ("श्रीकृष्ण के बहुत कम भक्त जानते हैं,", "SHRI KRISHNA KE BAHUT KAM BHAKT JAANTE HAIN,"),
                ("कि महाभारत जीतने के बाद प्रभु ने", "KI MAHABHARAT JEETNE KE BAAD PRABHU NE"),
                ("अर्जुन को तुरंत रथ से कूदने को क्यों कहा था!", "ARJUN KO TURANT RATH SE KUDNE KO KYUN KAHA THA!"),
            ], 0.04),
        ],
    },
    {
        "key": "confusion",
        "text": "RATH KA NIYAM",
        "visual": "Arjun on ground confused; traditionally driver gets down first",
        "vo": [
            ("tell", [
                ("नियम तो ये था कि रथ चलाने वाला पहले उतरे,", "NIYAM TO YE THA KI RATH CHALANE WALA PEHLE UTRE,"),
                ("लेकिन अर्जुन चुपचाप नीचे कूद गए।", "LEKIN ARJUN CHUPCHAP NEECHE KOOD GAYE."),
            ], 0.04),
        ],
    },
    {
        "key": "descend",
        "text": "PRABHU KA KADAM",
        "visual": "Krishna calmly releases the reins and steps down onto the battlefield earth",
        "vo": [
            ("tell", [
                ("फिर जैसे ही श्रीकृष्ण", "PHIR JAISE HI SHRI KRISHNA"),
                ("रथ से नीचे उतरे...", "RATH SE NEECHE UTRE..."),
            ], 0.04),
        ],
    },
    {
        "key": "explosion",
        "text": "RATH MEIN AAG!",
        "visual": "Massive explosion! Chariot incinerates in violent flames into ashes; Arjun shocked",
        "vo": [
            ("punch", [
                ("उसी पल, पूरे रथ में भयानक आग लग गई", "USI PAL, POORE RATH MEIN BHAYANAK AAG LAG GAYI"),
                ("और वो जलकर राख बन गया!", "AUR WO JALKAR RAAKH BAN GAYA!"),
                ("अर्जुन दंग रह गए!", "ARJUN DANG RAH GAYE!"),
            ], 0.04),
        ],
    },
    {
        "key": "reveal",
        "text": "ASLI RAHASYA",
        "visual": "Krishna reveals the secret with divine golden aura; Bhishma & Karna's weapons",
        "vo": [
            ("tell", [
                ("श्रीकृष्ण बोले—अर्जुन!", "SHRI KRISHNA BOLE—ARJUN!"),
                ("भीष्म और कर्ण के तीरों से", "BHEESHMA AUR KARNA KE TEERON SE"),
                ("ये रथ पहले ही जल चुका था।", "YE RATH PEHLE HI JAL CHUKA THA."),
                ("बस मेरे पैर इसे संभाले हुए थे!", "BAS MERE PAIR ISE SAMBHALE HUYE THE!"),
            ], 0.04),
        ],
    },
    {
        "key": "cta",
        "text": "JAI SHRI KRISHNA",
        "visual": "Arjuna bowing with folded hands; Krishna blessing with supreme radiant smile",
        "vo": [
            ("warm", [
                ("जिनके साथ भगवान हों,", "JINKE SAATH BHAGWAN HON,"),
                ("उनका कोई कुछ नहीं बिगाड़ सकता।", "UNKA KOI KUCH NAHI BIGAAD SAKTA."),
                ("कमेंट में लिखिए—जय श्रीकृष्ण!", "COMMENT MEIN LIKHIYE—JAI SHRI KRISHNA!"),
            ], 0.04),
        ],
    },
]

DELIVERY, SCRIPT, NARRATION = script_of(SPEC)
HOT = hot_words({
    "MAHABHARAT": GOLD_HI,
    "KRISHNA": GOLD_HI,
    "ARJUN": hexc("#90CAF9"),
    "RATH": GOLD_HI,
    "KUDO": FIRE_YELLOW,
    "NIYAM": GOLD_HI,
    "CHALANE": hexc("#FFAA48"),
    "CHUPCHAP": GOLD_HI,
    "NEECHE": GOLD_HI,
    "AAG": FIRE_YELLOW,
    "RAAKH": hexc("#B0BEC5"),
    "DANG": FIRE_YELLOW,
    "BHEESHMA": GOLD_HI,
    "KARNA": FIRE_YELLOW,
    "TEERON": GOLD_HI,
    "JAL": FIRE_ORANGE,
    "PAIR": GOLD_HI,
    "BHAGWAN": GOLD_HI,
    "COMMENT": GOLD_HI,
    "JAI": GOLD_HI,
})


# -----------------------------------------------------------------------------
# Scene Visual Classes (Zero On-Screen Clutter - Only Subtitles Rule)
# -----------------------------------------------------------------------------
class SceneHook:
    """Scene 1: Kurukshetra twilight. Krishna commands Arjun to jump off the chariot immediately."""
    def beats(self, d):
        return {"cmd": 0.45 * d}

    def events(self, d):
        return [(0.1, "whoosh")]

    def draw(self, ctx, t, d):
        kurukshetra_bg(ctx, t, intense=False)
        # Chariot in center-left background
        rath_chariot(ctx, 420, 1140, 0.85, t, burn=0.0)

        # Krishna as Sarathi on chariot, turning and commanding
        krishna(ctx, 330, 1020, 0.72, t, pose="command", flip=False)

        # Arjun on chariot listening with Gandiva bow
        arjuna(ctx, 520, 1010, 0.72, t, pose="bow", flip=True)


class SceneConfusion:
    """Scene 2: Arjun on ground confused; protocol dictates charioteer leaves first."""
    def beats(self, d):
        return {"conf": 0.35 * d}

    def events(self, d):
        return [(0.35 * d, "soft_thud")]

    def draw(self, ctx, t, d):
        kurukshetra_bg(ctx, t, intense=False)
        # Chariot parked on left
        rath_chariot(ctx, 280, 1150, 0.80, t, burn=0.0)
        # Krishna still seated holding reins
        krishna(ctx, 210, 1030, 0.70, t, pose="reins", flip=False)

        # Arjun standing on ground at right, scratching head in confusion
        b = self.beats(d)
        u_conf = clamp((t - b["conf"]) / 0.5)
        pose_arj = "confused" if u_conf > 0.1 else "bow"
        arjuna(ctx, 740, 1170, 0.74, t, pose=pose_arj, flip=True)


class SceneDescend:
    """Scene 3: Krishna releases reins, steps down from chariot onto the battlefield earth."""
    def beats(self, d):
        return {"step": 0.40 * d}

    def events(self, d):
        return [(0.1, "shimmer"), (0.40 * d, "ghanti")]

    def draw(self, ctx, t, d):
        kurukshetra_bg(ctx, t, intense=True)
        # Chariot
        rath_chariot(ctx, 260, 1150, 0.80, t, burn=0.0)

        b = self.beats(d)
        u_step = clamp((t - b["step"]) / 0.6)

        # Krishna descending from chariot to ground
        kx = lerp(200, 360, ease_in_out(u_step))
        ky = lerp(1030, 1170, ease_in_out(u_step))
        krishna(ctx, kx, ky, 0.74, t, pose="stand" if u_step > 0.5 else "reins", flip=False)

        # Golden lotus glow appearing where Krishna's feet touch earth
        if u_step > 0.3:
            glow(ctx, 360, 1165, 120 * u_step, GOLD_HI, 0.6 * u_step)

        # Arjun watching reverently from right
        arjuna(ctx, 780, 1170, 0.74, t, pose="bow", flip=True)


class SceneExplosion:
    """Scene 4: Chariot violently bursts into flames and dissolves into ashes! Arjun shocked."""
    def beats(self, d):
        return {"blast": 0.25 * d, "shock": 0.45 * d}

    def events(self, d):
        return [(0.25 * d, "boom"), (0.55 * d, "whoosh")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        u_blast = clamp((t - b["blast"]) / (d * 0.75))

        # Fiery intense red-orange sky during explosion
        kurukshetra_bg(ctx, t, intense=True)

        # Screen camera shake on blast
        shake_x = 0
        shake_y = 0
        if 0.0 < u_blast < 0.6:
            decay = 1.0 - (u_blast / 0.6)
            shake_x = 18 * math.sin(t * 35) * decay
            shake_y = 14 * math.cos(t * 32) * decay

        ctx.save()
        ctx.translate(shake_x, shake_y)

        # Chariot incinerating violently into ashes
        rath_chariot(ctx, 320, 1150, 0.85, t, burn=u_blast)

        # Krishna standing calm and untouched in divine serenity on the left
        krishna(ctx, 160, 1170, 0.74, t, pose="stand", flip=False)

        # Arjun stepping back in extreme shock!
        pose_arj = "shock" if u_blast > 0.2 else "bow"
        arjuna(ctx, 840, 1170, 0.74, t, pose=pose_arj, flip=True)

        ctx.restore()


class SceneReveal:
    """Scene 5: Krishna reveals the secret of Bhishma, Drona and Karna's divyastras."""
    def beats(self, d):
        return {"reveal": 0.35 * d}

    def events(self, d):
        return [(0.05, "shimmer"), (0.35 * d, "ghanti")]

    def draw(self, ctx, t, d):
        kurukshetra_bg(ctx, t, intense=False)

        # Golden ash mound where chariot stood
        ell(ctx, 420, 1160, 180, 24)
        rgba(ctx, ASH_COLOR, 0.85)
        ctx.fill()
        for i in range(12):
            sp_x = 340 + i * 16
            sp_y = 1155 - 6 * abs(math.sin(i))
            circle(ctx, sp_x, sp_y, 4, FIRE_YELLOW, 0.7 * math.sin(t * 5 + i))

        # Krishna radiating divine golden aura explaining the truth
        glow(ctx, 300, 750, 460, GOLD_HI, 0.45)
        krishna(ctx, 300, 1170, 0.75, t, pose="bless", flip=False)

        # Arjun listening with bowed head and folded hands (Pranam / Namaste)
        arjuna(ctx, 760, 1170, 0.74, t, pose="namaste", flip=True)


class SceneCTA:
    """Scene 6: Final divine blessing. Krishna smiling with radiant light; Arjun in devotion."""
    def beats(self, d):
        return {"cta": 0.30 * d}

    def events(self, d):
        return [(0.1, "ghanti"), (0.30 * d, "shimmer")]

    def draw(self, ctx, t, d):
        kurukshetra_bg(ctx, t, intense=False)

        # Divine golden flower shower & cosmic aura
        glow(ctx, 540, 700, 520, GOLD_HI, 0.4)
        for i in range(18):
            px = (i * 123 + int(t * 60)) % W
            py = (int(t * 120 + i * 85) % H)
            circle(ctx, px, py, 6 + 3 * math.sin(t * 4 + i), GOLD_HI, 0.6)

        # Krishna in supreme blessing posture
        krishna(ctx, 360, 1170, 0.76, t, pose="bless", flip=False)

        # Arjun in devotion with hands folded
        arjuna(ctx, 740, 1170, 0.74, t, pose="namaste", flip=True)


SCENE_CLASSES = {
    "hook": SceneHook,
    "confusion": SceneConfusion,
    "descend": SceneDescend,
    "explosion": SceneExplosion,
    "reveal": SceneReveal,
    "cta": SceneCTA,
}


# -----------------------------------------------------------------------------
# YouTube Upload Kit (SEO, Title, Tags, Description)
# -----------------------------------------------------------------------------
UPLOAD = {
    "title": "Mahabharat Jeetne Ke Baad Arjun Ka Rath Rakh Kyun Bana? 😱🔥 #shorts",
    "titles": [
        "Mahabharat Jeetne Ke Baad Arjun Ka Rath Rakh Kyun Bana? 😱🔥 #shorts",
        "Shri Krishna Ne Arjun Ko Rath Se Koodne Ko Kyun Kaha? #shorts",
        "Kyun Bhashm Hua Arjun Ka Rath? Mahabharat Ka Rahasya #shorts",
        "Krishna Ne Chhodi Lagaam Aur Bhashm Ho Gaya Rath! ⚡ #shorts",
        "Bhishma Aur Karna Ke Divyastra Ka Sach! Arjun Rath Rahasya #shorts",
    ],
    "thumb_text": "RATH MEIN AAG?",
    "queries": [
        "arjun ka rath kyu jala",
        "mahabharat ke baad arjun ka rath",
        "krishna ne arjun ko rath se kyu utara",
    ],
    "description": """
Mahabharat yuddh jeetne ke baad Shri Krishna ne Arjun se achanak rath se neeche koodne ko kyun kaha?
Jaise hi Bhagwan Shri Krishna ne rath chhoda aur apne kadam dharti par rakhe, divya rath aag ki lapton mein bhashm hokar rakh ban gaya!
Jaaniye Bhishma, Drona aur Karna ke divyastron ka sabse bada rahasya jo Shri Krishna ne Arjun ko bataya.

Is pavitra gyan ko poora dekhein aur comment mein 'JAI SHRI KRISHNA' zaroor likhein. 🙏🚩
""",
    "tags": [
        "krishna",
        "arjun",
        "mahabharat",
        "arjun ka rath",
        "karna",
        "bhishma",
        "drona",
        "sanatan katha",
        "divya rahasya",
        "shorts",
    ],
    "hashtags": [
        "#Shorts",
        "#Krishna",
        "#Mahabharat",
    ],
}


def thumbnail(ctx):
    """High-CTR YouTube Shorts cover: Chariot exploding into flames, Krishna with divine aura."""
    kurukshetra_bg(ctx, 1.5, intense=True)

    # Chariot exploding violently with roaring flames
    rath_chariot(ctx, 520, 1140, 0.90, 1.8, burn=0.65)

    # Krishna on left with radiant golden halo and knowing smile
    glow(ctx, 240, 720, 380, GOLD_HI, 0.5)
    krishna(ctx, 240, 1170, 0.78, 1.2, pose="bless", flip=False)

    # Arjun on right in total shock
    arjuna(ctx, 830, 1170, 0.76, 1.2, pose="shock", flip=True)

    # Top dramatic title ribbon
    ctx.save()
    rrect(ctx, 80, 140, 920, 140, 24)
    rgba(ctx, hexc("#1A0808"), 0.92)
    ctx.fill_preserve()
    rgba(ctx, FIRE_YELLOW, 0.95)
    ctx.set_line_width(4)
    ctx.stroke()
    text(ctx, "RATH BHASHM KYUN HUA?", 540, 195, 52, FIRE_YELLOW, bold=True)
    text(ctx, "MAHABHARAT KA SABSE BADA RAHASYA", 540, 250, 28, WHITE, bold=True)
    ctx.restore()


def main() -> None:
    story = sys.modules[__name__]
    story.__name__ = "kathas.arjun_rath"
    engine.run(story)


if __name__ == "__main__":
    main()
