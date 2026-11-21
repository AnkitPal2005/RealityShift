"""Reality Shift Short - "Great Nicobar: China Ka Unsinkable Aircraft Carrier" (~45-50s).

Usage:
  python make.py great_nicobar --kiki-export     # exports text for KikiVoice
  python make.py great_nicobar --check           # policy check
  python make.py great_nicobar --engine edge     # preview render with edge-tts
  python make.py great_nicobar                   # final render from KikiVoice files

Strategic overview:
Great Nicobar Island (Indira Point) sits right at the entrance of the Malacca Strait (~80% of China's oil imports).
India's ₹72,000 crore mega infrastructure and military base creates an unsinkable aircraft carrier.
"""

import importlib
import json
import math
import sys

import cairo
import numpy as np

from core import engine
from core import delivery
from core import lego
from core.engine import *  # noqa: F401,F403
from shorts.brahmos_lego import tag
from shorts.chabahar import Cued
from shorts.reality_shift import stamp, flag
from shorts.malacca import (
    draw_map, poly, proj, ROUTE, GN, INDIRA_POINT, GALATHEA, GATE, ACEH,
    CAMPBELL_BAY, MALACCA, WIDE, CHANNEL, MID, tanker, warship, jet, airbase, crane, caliper
)

TOPIC = "GREAT NICOBAR PROJECT"
OUTPUTS = {"edge": "great_nicobar_short.mp4"}
LEGO = {"header": "radar", "caption": "chip", "transition": "scan", "palette": "amber", "ending": "prompt"}

CLEAN_PUNCTUATION = False
MAX_GAP = 0.6
TAIL_PAD = 0.25
TRIM = {"thresh": 0.006, "keep": 0.08, "keep_tail": 0.15}
MUSIC_BPM = 108
MUSIC_STYLE = "march"
EDGE_VOICE = "hi-IN-MadhurNeural"
EDGE_RATE = "+10%"
EDGE_PITCH = "+0Hz"
KIKI_TEMPO = {"narrator": 1.0}
KIKI_PAUSE_MS = 500

PAL = lego.PALETTES["amber"]
UI = PAL["ui"]
HI = PAL["hi"]
RED = PAL["alert"]
INK = PAL["ink"]
SAFFRON = hexc("#FF9933")
GREEN = hexc("#3DDC84")
SONAR = hexc("#3FD1FF")
STEEL = hexc("#AEB8C2")
GOLD = hexc("#FFD700")

SOURCES = [
    "Great Nicobar Infrastructure Project: ₹72,000 crore ($9 billion) mega project at Galathea Bay, including International "
    "Container Transshipment Terminal (ICTT), dual-use military-civil international airport, power plant and township "
    "(PIB, Ministry of Ports, Shipping and Waterways; The Hindu; Economic Times; Times of India)",
    "Strategic location: Great Nicobar Island (Indira Point) sits directly adjacent to the Six Degree Channel overlooking "
    "the western entrance of the Malacca Strait, through which ~80% of China's crude oil imports pass (The Malacca Dilemma, "
    "CSIS, US Naval War College, ORF)",
    "Tri-service Andaman and Nicobar Command (ANC), operation of P-8I Neptune maritime patrol aircraft, Su-30MKI deployment, "
    "INS Baaz expansion, and anti-submarine warfare (ASW) sonar surveillance to monitor Chinese PLAN submarines entering the "
    "Indian Ocean (IDSA, Observer Research Foundation)",
]

SPEC = [
    {"key": "hook", "accent": RED, "text": "80% KACHCHA TEL KA TRAP",
     "visual": "Wide Indian Ocean map; oil tankers stream toward Malacca Strait; red choke point locks in",
     "vo": [("hook", [("दुनिया की सबसे बड़ी सेना रखने वाले", "DUNIYA KI SABSE BADI"),
                      ("चीन की सबसे कमज़ोर नस कहाँ है?", "CHEEN KI SABSE KAMZOR NAS KAHAN HAI?"),
                      ("पता है?", "PATA HAI?"),
                      ("उसकी गर्दन फँसी है मलक्का के समुद्री रास्ते में,", "USKI GARDAN FASI HAI MALACCA MEIN,"),
                      ("जहाँ से चीन का अस्सी प्रतिशत कच्चा तेल गुज़रता है!", "JAHAN SE 80% KACHCHA TEL GUZARTA HAI!")])]},

    {"key": "gate", "accent": HI, "text": "GREAT NICOBAR: THE CHOKEPOINT",
     "visual": "Map zooms to Great Nicobar (Indira Point); radar sweeps over Six Degree Channel; distance caliper to Malacca",
     "vo": [("tell", [("और इसी रास्ते पर", "AUR ISI RAASTE PAR"),
                      ("भारत का अभेद्य द्वीप है,", "BHARAT KA ABHEDYA DWEEP HAI,"),
                      ("ग्रेट निकोबार।", "GREAT NICOBAR."),
                      ("ये इतना पास है कि", "YE ITNA PAAS HAI KI"),
                      ("यहाँ से दूरबीन लगाने पर", "YAHAN SE DOORBEEN LAGANE PAR"),
                      ("चीन का हर जहाज़ साफ़ दिखाई देता है!", "CHEEN KA HAR JAHAZ SAAF DIKHTA HAI!")])]},

    {"key": "build", "accent": SAFFRON, "text": "₹72,000 CRORE MASTERSTROKE",
     "visual": "Galathea Bay deep-water port, cranes, runway outlines; counter ticks 0 to ₹72,000 CRORE",
     "vo": [("tell", [("अब भारत ने यहाँ", "AB BHARAT NE YAHAN"),
                      ("बहत्तर हज़ार करोड़ का", "72,000 CRORE KA"),
                      ("ऐसा चक्रव्यूह तैयार किया है,", "AISA CHAKRAVYUH TAIYAAR KIYA HAI,"),
                      ("जिसने बीजिंग की नींद उड़ा दी है।", "JISNE BEIJING KI NEEND UDA DI HAI.")])]},

    {"key": "carrier", "accent": STEEL, "text": "UNSINKABLE AIRCRAFT CARRIER",
     "visual": "Aircraft carrier with torpedo vulnerability vs huge island base fortress; 'UNSINKABLE' stamp",
     "vo": [("tell", [("सोचिए, एयरक्राफ्ट कैरियर भी", "SOCHIYE, AIRCRAFT CARRIER BHI"),
                      ("एक टॉरपीडो से समंदर में डूब सकता है,", "TORPEDO SE DOOB SAKTA HAI,"),
                      ("लेकिन एक पूरा द्वीप?", "LEKIN EK POORA DWEEP?"),
                      ("उसे कोई मिसाइल नहीं डुबा सकती!", "USE KOI MISSILE NAHI DUBA SAKTI!")])]},

    {"key": "weapons", "accent": GREEN, "text": "SUKHOI • BRAHMOS • P-8I",
     "visual": "Su-30MKI, BrahMos coastal launcher and P-8I Neptune submarine hunter sonar sweep underwater submarine",
     "vo": [("tell", [("यहाँ तैनात होंगे सुखोई तीस जेट्स,", "YAHAN TAINAAT HONGE SU-30 JETS,"),
                      ("ब्रह्मोस मिसाइलें और पी एट आई सबमरीन हंटर्स।", "BRAHMOS AUR P-8I SUBMARINE HUNTERS."),
                      ("यानी चीनी नौसेना ने रुख भी किया,", "YAANI CHEENI NAUSENA NE RUKH BHI KIYA,"),
                      ("तो समंदर के नीचे ही काम तमाम हो जाएगा!", "TO SAMANDAR KE NEECHE KAAM TAMAAM!")])]},

    {"key": "block", "accent": RED, "text": "24 GHANTE MEIN BLOCK",
     "visual": "Indian Navy fleet forms a blockade across the channel; red energy cutoff stamp; padlock icon",
     "vo": [("tell", [("सीधी बात है, अगर युद्ध हुआ", "SEEDHI BAAT HAI, AGAR YUDDH HUA"),
                      ("तो भारतीय नौसेना", "TOH BHARATIYA NAUSENA"),
                      ("चौबीस घंटे में चीन की सांस रोक सकती है,", "24 GHANTE MEIN CHEEN KI SAANS ROK SAKTI HAI,"),
                      ("बिना उनकी सीमा में घुसे!", "BINA UNKI SEEMA MEIN GHUSE!")])]},

    {"key": "ask", "accent": HI, "text": "CHEEN KA NIGHTMARE?",
     "visual": "Tricolour crest over Great Nicobar; comment prompt card pops; 'CHEEN KA NIGHTMARE?' question",
     "vo": [("ask", [("क्या भारत का ये अनसिंकेबल एयरक्राफ्ट कैरियर", "KYA BHARAT KA YEH UNSINKABLE CARRIER"),
                     ("चीन की दादागीरी खत्म कर देगा?", "CHEEN KI DAADAAGEERI KHATM KAR DEGA?"),
                     ("कमेंट में बताइए,", "COMMENT MEIN BATAIYE,"),
                     ("और सब्सक्राइब कीजिए रियलिटी शिफ्ट!", "AUR SUBSCRIBE KIJIYE REALITY SHIFT!"),
                     ("जय हिंद!", "JAI HIND!")])]},
]

DELIVERY = delivery.build(SPEC)
BREATHS = False
ROOM = 0
SCRIPT = [(s["key"], [chunk for _, chunks, *_ in s["vo"] for chunk in chunks]) for s in SPEC]
NARRATION = {key: " ".join(hi for hi, _ in chunks) for key, chunks in SCRIPT}

HOT = {
    "DUNIYA": HI, "SABSE": HI, "BADI": HI, "CHEEN": RED, "KAMZOR": RED, "NAS": RED, "PATA": HI,
    "MALACCA": RED, "80%": RED, "KACHCHA": SAFFRON, "TEL": SAFFRON, "BHARAT": SAFFRON, "ABHEDYA": HI,
    "DWEEP": HI, "GREAT": SAFFRON, "NICOBAR.": SAFFRON, "NICOBAR": SAFFRON, "72,000": GOLD, "CRORE": GOLD,
    "CHAKRAVYUH": SAFFRON, "BEIJING": RED, "AIRCRAFT": STEEL, "CARRIER": STEEL, "TORPEDO": RED, "DOOB": RED,
    "UNSINKABLE": GREEN, "MISSILE": RED, "SU-30": HI, "JETS,": HI, "BRAHMOS": RED, "P-8I": SONAR,
    "SUBMARINE": SONAR, "HUNTERS.": SONAR, "NAUSENA": SAFFRON, "TAMAAM!": RED, "YUDDH": RED, "24": RED,
    "GHANTE": RED, "SAANS": RED, "ROK": RED, "COMMENT": HI, "SUBSCRIBE": HI, "JAI": SAFFRON, "HIND!": SAFFRON
}
for _k in list(HOT):
    HOT[_k.strip(PUNCT + ".—")] = HOT[_k]


# ============================================================ SCENE CLASSES

class Hook(Cued):
    def beats(self, d):
        c = self.cue
        return {"pata": c("PATA", 2.2), "oil": c("80%", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["pata"], "pick"), (b["oil"], "pop"), (b["oil"] + 0.3, "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        draw_map(ctx, WIDE, t, tint={"china": (RED, 0.4), "india": (SAFFRON, 0.5)})
        
        # Stream tankers along route
        for i, off in enumerate((0.15, 0.35, 0.55, 0.75)):
            u = (t * 0.08 + off) % 1.0
            if u < 0.85:
                px, py = proj(WIDE, *ROUTE[int(u * (len(ROUTE) - 1))])
                tanker(ctx, px, py, -0.2, 1.2)

        # Pulse red choke ring at Malacca
        mx, my = proj(WIDE, *MALACCA)
        pulse = 1.0 + 0.3 * math.sin(t * 8)
        circle(ctx, mx, my, 60 * pulse, RED, 0.4)
        circle(ctx, mx, my, 35, RED, 0.8)
        tag(ctx, "MALACCA CHOKEPOINT", mx, my - 60, RED, 1.0, size=36)

        if t > b["oil"]:
            tag(ctx, "80% KACHCHA TEL", 540, 480, RED, t - b["oil"], size=50, sub="CHINA'S FATAL TRAP")


class Gate(Cued):
    def beats(self, d):
        c = self.cue
        return {"gn": c("NICOBAR", 2.0), "door": c("DOORBEEN", d * 0.6)}

    def events(self, d):
        b = self.beats(d)
        return [(b["gn"], "pop"), (b["door"], "pick")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        v = CHANNEL
        draw_map(ctx, v, t, tint={"india": (SAFFRON, 0.7)})

        gx, gy = proj(v, *GN)
        ix, iy = proj(v, *INDIRA_POINT)
        ax, ay = proj(v, *ACEH)

        # Great Nicobar indicator
        circle(ctx, gx, gy, 80 + 20 * math.sin(t * 4), SONAR, 0.3)
        circle(ctx, gx, gy, 40, SAFFRON, 0.9)
        tag(ctx, "GREAT NICOBAR", gx, gy - 60, SAFFRON, 1.0, size=44, sub="INDIRA POINT")

        # Caliper / Distance line to Malacca entrance
        caliper(ctx, (ix, iy), (ax, ay), clamp(t - 0.5), GOLD, "~50 KM SIX DEGREE CHANNEL")

        if t > b["door"]:
            tag(ctx, "EYES ON EVERY CHINESE SHIP", 540, 420, HI, t - b["door"], size=42)


class Build(Cued):
    def beats(self, d):
        c = self.cue
        return {"cr": c("CRORE", 1.8), "bj": c("BEIJING", d * 0.65)}

    def events(self, d):
        b = self.beats(d)
        return [(b["cr"], "pop"), (b["cr"] + 0.2, "kaching"), (b["bj"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        v = MID
        draw_map(ctx, v, t, tint={"india": (SAFFRON, 0.8)})

        gx, gy = proj(v, *GALATHEA)
        
        # Deep Port & Airbase graphics
        crane(ctx, gx - 80, gy - 20, 1.2, clamp(t / 2.0))
        airbase(ctx, gx + 60, gy + 40, 1.2, SONAR, clamp(t / 2.0))
        
        # ₹72,000 CRORE counter
        progress = clamp(t / max(b["cr"], 0.1))
        amt = int(progress * 72000)
        text(ctx, f"₹{amt:,} CRORE", 540, 460, 90, GOLD, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=16)
        tag(ctx, "GALATHEA BAY MEGA PROJECT", 540, 560, SAFFRON, 1.0, size=38)

        if t > b["bj"]:
            stamp(ctx, 540, 720, t - b["bj"], -0.04, 600, 130, RED, [("BEIJING KA TRAP", 0, 76, RED)])


class Carrier(Cued):
    def beats(self, d):
        c = self.cue
        return {"doob": c("TORPEDO", 2.2), "dweep": c("DWEEP", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["doob"], "pop"), (b["dweep"], "dingdong"), (b["dweep"] + 0.2, "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        
        # Tactical Blue Background
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, *hexc("#0A192F"))
        g.add_color_stop_rgb(1, *hexc("#020C1B"))
        ctx.rectangle(0, 0, W, H)
        ctx.set_source(g)
        ctx.fill()

        # Split screen comparison
        line(ctx, [(540, 260), (540, 1000)], UI, 2, 0.4)

        # Left: Floating Aircraft Carrier (vulnerable)
        warship(ctx, 270, 600, 0.0, 1.6)
        text(ctx, "CARRIER", 270, 740, 44, STEEL, bold=True)
        if t > b["doob"]:
            circle(ctx, 270, 600, 70, RED, 0.8)
            text(ctx, "VULNERABLE", 270, 810, 36, RED)

        # Right: Island Fortress (Unsinkable)
        circle(ctx, 810, 600, 120, SAFFRON, 0.25)
        circle(ctx, 810, 600, 80, GREEN, 0.4)
        jet(ctx, 810, 560, -0.2, 1.5, (1, 1, 1))
        text(ctx, "GREAT NICOBAR", 810, 740, 40, SAFFRON, bold=True)
        
        if t > b["dweep"]:
            stamp(ctx, 540, 400, t - b["dweep"], 0.03, 620, 130, GREEN, [("UNSINKABLE CARRIER", 0, 74, GREEN)])


class Weapons(Cued):
    def beats(self, d):
        c = self.cue
        return {"jets": c("SU-30", 1.8), "sub": c("SUBMARINE", d * 0.55), "kill": c("TAMAAM", d * 0.85)}

    def events(self, d):
        b = self.beats(d)
        return [(b["jets"], "pick"), (b["sub"], "pop"), (b["kill"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        
        # Sonar HUD view
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, *hexc("#031B2A"))
        g.add_color_stop_rgb(1, *hexc("#010912"))
        ctx.rectangle(0, 0, W, H)
        ctx.set_source(g)
        ctx.fill()

        # Radar / Sonar grid sweep
        cx, cy = 540, 640
        for r in (150, 300, 450):
            circle(ctx, cx, cy, r, SONAR, 0.25)
        line(ctx, [(cx - 450, cy), (cx + 450, cy)], SONAR, 1, 0.2)
        line(ctx, [(cx, cy - 450), (cx, cy + 450)], SONAR, 1, 0.2)

        # Weapons chips
        tag(ctx, "SUKHOI-30 MKI", 280, 380, HI, t - b["jets"], size=36)
        tag(ctx, "BRAHMOS COASTAL", 800, 380, RED, t - b["jets"], size=36)
        tag(ctx, "P-8I NEPTUNE ASW", 540, 460, SONAR, t - b["sub"], size=40)

        # Chinese submarine crosshair target lock
        sx, sy = 540, 800
        circle(ctx, sx, sy, 45, RED, 0.9)
        line(ctx, [(sx - 65, sy), (sx + 65, sy)], RED, 3, 0.9)
        line(ctx, [(sx, sy - 65), (sx, sy + 65)], RED, 3, 0.9)
        text(ctx, "TARGET LOCK: SUBMARINE", sx, sy + 75, 30, RED, font=lego.MONO)

        if t > b["kill"]:
            stamp(ctx, 540, 940, t - b["kill"], -0.02, 580, 110, RED, [("SUBMARINE KILL ZONE", 0, 68, RED)])


class Block(Cued):
    def beats(self, d):
        c = self.cue
        return {"navy": c("NAUSENA", 1.8), "hrs": c("24", d * 0.55)}

    def events(self, d):
        b = self.beats(d)
        return [(b["navy"], "pop"), (b["hrs"], "thud")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        v = CHANNEL
        draw_map(ctx, v, t, tint={"india": (SAFFRON, 0.6)})

        # Naval blockade line of warships across the channel
        ix, iy = proj(v, *INDIRA_POINT)
        ax, ay = proj(v, *ACEH)
        line(ctx, [(ix, iy), (ax, ay)], RED, 8, 0.8)

        for off in (0.2, 0.5, 0.8):
            wx = lerp(ix, ax, off)
            wy = lerp(iy, ay, off)
            warship(ctx, wx, wy, -0.6, 1.2)

        tag(ctx, "NAVAL BLOCKADE CORDON", 540, 420, RED, 1.0, size=44)

        if t > b["hrs"]:
            stamp(ctx, 540, 560, t - b["hrs"], 0.04, 660, 140, RED, [("24 GHANTE MEIN BLOCK", 0, 78, RED)])


class Ask(Cued):
    def beats(self, d):
        c = self.cue
        return {"q": c("CARRIER", 1.5), "cmt": c("COMMENT", d * 0.75)}

    def events(self, d):
        b = self.beats(d)
        return [(b["q"], "pop"), (b["cmt"], "dingdong"), (b["cmt"] + 1.0, "pick")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        v = WIDE
        draw_map(ctx, v, t, tint={"india": (SAFFRON, 0.6)})

        gx, gy = proj(v, *GN)
        circle(ctx, gx, gy, 120 + 30 * math.sin(t * 3), SAFFRON, 0.4)
        flag(ctx, gx - 45, gy - 90, 90, 60, "india", t)

        lego.ending(
            STORY, ctx, t, t - b["q"], t - b["cmt"],
            question=("CHEEN KA", "NIGHTMARE?"),
            suggestions=("MASTERSTROKE", "JAI HIND", "SAHI KADAM", "BLOCKADE"),
            y=560
        )


SCENE_CLASSES = {
    "hook": Hook,
    "gate": Gate,
    "build": Build,
    "carrier": Carrier,
    "weapons": Weapons,
    "block": Block,
    "ask": Ask,
}
STORY = importlib.import_module(__name__)


def write_alignment(final):
    out = [
        {
            "scene": spec["key"],
            "start": round(s["start"], 3),
            "end": round(s["start"] + s["dur"], 3),
            "voiceover": NARRATION[spec["key"]],
            "on_screen_text": spec["text"],
            "visual": spec["visual"],
            "words": [{"t": round(s["start"] + st, 3), "w": w} for st, w in s["captions"]]
        }
        for spec, s in zip(SPEC, engine.SCENES)
    ]
    path = final.with_suffix(".json")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Alignment: {path}")


# ============================================================ UPLOAD KIT

UPLOAD = {
    "titles": [
        "Great Nicobar: China Ka 'Unsinkable Aircraft Carrier' Nightmare",
        "Malacca Chokepoint: Bharat Ka ₹72,000 Crore Mega Base",
        "Great Nicobar Mega Project: China Ka Tel 24 Ghante Me Block?",
        "China Ka Malacca Trap: Great Nicobar Se 80% Tel Block?",
        "₹72,000 Cr Ka Great Nicobar: China Ke Liye Sabse Bada Khatra",
        "Andaman Nicobar Ka Masterstroke: China Ka Khel Khatam?",
        "Great Nicobar Island: Indian Navy Ka Strategic Chokepoint",
        "Galathea Bay Port: China Ka Malacca Dilemma Explained",
    ],
    "title": "Great Nicobar: China Ka 'Unsinkable Aircraft Carrier' Nightmare",
    "thumb_text": "₹72,000 CR",
    "queries": ["great nicobar project", "great nicobar mega port", "malacca dilemma"],
    "description": """Great Nicobar Project: China ke Malacca Strait chokepoint ke theek gate par Bharat ka ₹72,000 crore ka mega project.
Great Nicobar mega port aur international airport se China ka Malacca dilemma shuru ho chuka hai.
Duniya ki sabse badi sena rakhne wale China ki sabse kamzor nas Malacca Strait hai, jahan se unka 80% kachcha tel guzarta hai. Aur theek iske munh par baitha hai Bharat ka Great Nicobar dweep.

Is Short me:
• 80% Crude Oil: China ka Malacca Dilemma aur unki sabse kamzor nas
• Great Nicobar: Malacca ke pravesh dwar (Six Degree Channel) par Bharat ka abhedya dweep
• ₹72,000 Crore Project: Galathea Bay mega port aur military dual-use airport
• Unsinkable Aircraft Carrier: Dweep jise duniya ki koi torpedo ya missile nahi duba sakti
• Su-30MKI, BrahMos aur P-8I Neptune: Hind Mahasagar me Chinese submarines ka shikar
• 24 Ghante me Blockade: Takraav ki sthiti me China ki poori energy lifeline par Bharat ka pehra

Aapke hisaab se kya Bharat ka yeh move China ke String of Pearls ko hamesha ke liye tod dega? Comment me likho - Jai Hind!
Subscribe to Reality Shift for hard-hitting defence and geopolitical analysis.

Note: Map animations schematic aur geopolitical analysis ke liye hain. Sources: PIB India, CSIS, ORF, The Hindu, Economic Times.
""",
    "tags": ["great nicobar project", "great nicobar", "malacca dilemma", "malacca strait", "galathea bay port",
             "indian navy", "andaman nicobar command", "china oil blockade", "su30mki", "p8i neptune",
             "brahmos missile", "defence hindi", "geopolitics hindi", "reality shift"],
    "hashtags": ["#Shorts", "#GreatNicobar", "#IndianNavy"],
}


def thumbnail(ctx):
    """1080x1920 cover: '₹72,000 CR' over the glowing Malacca chokepoint and Great Nicobar."""
    v = CHANNEL
    draw_map(ctx, v, 0.5, tint={"india": (SAFFRON, 0.8), "china": (RED, 0.5)})
    
    gx, gy = proj(v, *GN)
    circle(ctx, gx, gy, 90, SAFFRON, 0.5)
    flag(ctx, gx - 45, gy - 110, 90, 60, "india", 0.0)

    g = cairo.LinearGradient(0, 1150, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.88)
    ctx.rectangle(0, 1150, W, H - 1150)
    ctx.set_source(g)
    ctx.fill()

    g = cairo.LinearGradient(0, 0, 0, 780)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.92)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, 780)
    ctx.set_source(g)
    ctx.fill()

    vignette(ctx)
    text(ctx, "₹72,000 CR", 540, 290, 180, GOLD, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=22)
    text(ctx, "GREAT NICOBAR", 540, 480, 110, INK, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=18)
    tag(ctx, "UNSINKABLE AIRCRAFT CARRIER", 540, 640, RED, 1.0, size=42)
    text(ctx, "REALITY SHIFT", 540, 1800, 40, INK, a=0.7)


def main() -> None:
    from core import upload_kit
    story = importlib.import_module("shorts.great_nicobar")
    engine.make_frame = lego.frame_maker(story)
    eng = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "files"
    final = engine.render(story, eng)
    write_alignment(final)
    upload_kit.build(story, final, sum(s["dur"] for s in engine.SCENES))


if __name__ == "__main__":
    main()
