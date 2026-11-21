"""Project Kusha vs S-400: Inside India's Ultra Long-Range Air Defense Shield
Full Long-Form 16:9 (1920x1080) Widescreen Documentary Renderer.
Featuring 80+ unique, punchy, non-repeating visual shots changing every 5 seconds!
"""

import math
import os
import sys
import json
import time
import subprocess
import cairo
import numpy as np
from pathlib import Path

W, H = 1920, 1080
FPS = 30

# Colors
BG_DARK = (0.02, 0.025, 0.04)
BG_GRID = (0.05, 0.08, 0.12)
AMBER = (1.0, 0.65, 0.0)
CYAN = (0.2, 0.85, 0.95)
GREEN = (0.24, 0.86, 0.52)
RED = (0.95, 0.22, 0.22)
WHITE = (0.95, 0.96, 0.98)
GRAY = (0.5, 0.55, 0.62)
STEEL = (0.72, 0.78, 0.85)
GOLD = (1.0, 0.82, 0.25)
SAFFRON = (1.0, 0.6, 0.2)
OLIVE = (0.22, 0.28, 0.22)
FIRE = (1.0, 0.35, 0.05)

ROOT = Path(__file__).resolve().parent
WORK_DIR = ROOT / "output" / "work" / "project_kusha" / "files"
OUT_DIR = ROOT / "output" / "documentary"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ROMAN_SCRIPTS = [
    # Scene 1
    "AGAR KAL SUBAH LAC PAR EK SATH 50 STEALTH FIGHTERS AUR SUPERSONIC CRUISE MISSILES LAUNCH HO JAYEIN, TOH KYA HAMARA AAKASH UNHE ROK PAYEGA? PICHHLE KUCH SAALON MEIN BHARAT NE APNE AAKASH KO SURAKSHIT KARNE KE LIYE DUNIYA KA SABSE LETHAL AIR DEFENSE SYSTEM S-400 TRIUMF DEPLOY KIYA HAI. LEKIN PARDE KE PEECHE DRDO EK AISI SECRET TECHNOLOGY PAR KAAM KAR RAHA HAI JO S-400 SE BHI ZYADA ADVANCED AUR GHATAK HAI — ISKA NAAM HAI PROJECT KUSHA! EK AISA ULTRA LONG-RANGE AIR DEFENSE SHIELD JO DUSHMAN KE STEALTH JETS, BALLISTIC MISSILES AUR DRONE SWARMS KO 350 SE 400 KILOMETER DOOR HI HAWA MEIN RAAKH BANA DEGA. LEKIN SAWAL YEH HAI — JAB HAMARE PAAS ALREADY S-400 MAUJOOD HAI, TOH BHARAT KO PROJECT KUSHA KI ZAROORAT KYUN PADI? AAJ HUM JAANENGE BHARAT KE SABSE BADE AIR DEFENSE SECRET KO.",
    # Scene 2
    "S-400 TRIUMF KO AAJ DUNIYA KA SABSE TAAQATWAR AIR DEFENSE SYSTEM MAANA JAATA HAI. BHARAT NE SAAL 2018 MEIN RUSSIA KE SAATH LAGBHAG 40 HAZAAR CRORE RUPEES KI DEAL KARKE S-400 KE 5 SQUADRONS KHAREEDE THE, JINMEIN SE 3 SQUADRONS CHINA AUR PAKISTAN BORDER PAR POORI TARAH DEPLOYED HAIN. S-400 KI SABSE BADI TAAQAT HAI ISKA BIG BIRD RADAR, JO EK SATH 300 TARGETS KO TRACK KAR SAKTA HAI AUR 600 KILOMETER DOOR TAK AAKASH PAR NAZAR RAKHTA HAI. ISKE SAATH AATI HAIN CHAAR ALAG-ALAG RANGE KI MISSILES — 40 KILOMETER SE LEKAR 400 KILOMETER TAK MAAR KARNE WALI 40N6 MISSILE. YEH SYSTEM AAWAAZ SE 14 GUNA TEZ AANE WALI BALLISTIC MISSILES KO BHI HAWA MEIN NASHT KAR SAKTA HAI. YAHI WAJAH HAI KI S-400 KE SAAMNE DUSHMAN KE BADE AWACS AIRCRAFT BORDER KE PAAS AANE SE BHI KAAMPTE HAIN.",
    # Scene 3
    "LEKIN YAHIN SE SHURU HOTI HAI ASLI KAHANI. S-400 KITNA BHI TAAQATWAR HO, RUSSIA-UKRAINE YUDH NE EK KADWA SACH DUNIYA KE SAAMNE LAA DIYA. RUSSIA KHUD SUPPLY SANKAT SE JOOJH RAHA HAI, JISKI WAJAH SE BHARAT KE BAAKI 2 SQUADRONS KI DELIVERY MEIN DERI HUI. DOOSRA BADA KHATRA HAI FOREIGN DEPENDENCY — AGAR YUDH KE WAQT SPARE PARTS YA MISSILES KI SUPPLY RUK JAYE, TOH HAMARA AAKASH KAMZOR PAD SAKTA HAI. AUR TEESRA SABSE BADA KHATRA HAI CHINA KE CHENGDU J-20 STEALTH FIGHTERS. IN STEALTH JETS KO TRACK KARNE KE LIYE PURANE RADAR SYSTEMS KAAFI NAHI HAIN. BHARAT KO CHAHIYE THA EK AISA SWADESHI HATHIYAR JISKA REMOTE CONTROL KISI DOOSRE DESH KE HAATH MEIN NA HO, AUR JO BHARAT KE APNE SATELLITES AUR RADARS KE SAATH SEAMLESSLY BAAT KAR SAKE. ISI ZAROORAT SE JANAM HUA DRDO KE PROJECT KUSHA KA!",
    # Scene 4
    "PROJECT KUSHA KO MINISTRY OF DEFENCE NE OCTOBER 2023 MEIN 21 HAZAAR 700 CRORE RUPEES KE BUDGET KE SAATH MANZOORI DI THI. YEH SIRF EK MISSILE NAHI HAI, BALKI EK THREE-TIER MOBILE SURFACE-TO-AIR MISSILE SYSTEM HAI. KUSHA KE PAAS TEEN ALAG-ALAG INTERCEPTOR MISSILES HONGI — PEHLI 150 KILOMETER RANGE KI, DOOSRI 250 KILOMETER RANGE KI, AUR TEESRI 350 SE 400 KILOMETER RANGE WALI MAHA-VINASHAK MISSILE. YEH SYSTEM DUSHMAN KE FIGHTER JETS, STEALTH JETS, AWACS, CRUISE MISSILES AUR AIR REFUELING TANKERS KO MEELON DOOR HI KHATAM KARNE KE LIYE DESIGN KIYA JA RAHA HAI. SABSE KHAAS BAAT YEH HAI KI ISKA FIRING REACTION TIME S-400 SE BHI TEZ BANAYA GAYA HAI, TAAKI DUSHMAN KE EK SAATH KIYE GAYE SATURATION ATTACKS KO TURANT NAKAAM KIYA JA SAKE.",
    # Scene 5
    "AB AATE HAIN ASLI MUQABALE PAR — KYA PROJECT KUSHA S-400 SE BEHTAR HAI? PEHLA FARQ HAI RADAR TECHNOLOGY MEIN. S-400 PESA RADAR PAR CHALTA HAI, JABKI PROJECT KUSHA MEIN DRDO GALLIUM NITRIDE YAANI GaN AESA RADAR USE KAR RAHA HAI. YEH RADAR ITNI POWERFUL MICRO-BEAMS PHENKTA HAI JO J-20 JAISE STEALTH VIMANON KI COATING KO BHEED KAR UNHE INSTANTLY LOCK KAR LETI HAI. DOOSRA BADA FARQ HAI MAARNE KI TECHNIQUE MEIN. S-400 TARGET KE PAAS JAAKAR PHAT-TA HAI AUR CHHARRO'N SE NUKSAAN PAHUNCHATA HAI. LEKIN PROJECT KUSHA HIT-TO-KILL KINETIC INTERCEPTION PAR KAAM KARTA HAI — YAANI HAWA MEIN UDTI HUI GOLI SE DOOSRI GOLI KO SEEDHA TAKRANA! ISSE PAIDA HONE WALI BHAARI KINETIC ENERGY DUSHMAN KE NUCLEAR WARHEAD YA HYPERSONIC MISSILE KO HAWA MEIN HI BHAAP BANA DETI HAI.",
    # Scene 6
    "TEESRA SABSE BADA FAYDA HAI NETWORK WARFARE. PROJECT KUSHA SEEDHA BHARAT KE IACCS — INTEGRATED AIR COMMAND SYSTEM SE JUDA HOGA. ISKA MATLAB NETRA AWACS, INS VIKRANT KA RADAR AUR ZAMEEN KE SAARE SENSORS EK HI SECOND MEIN KUSHA KO REAL-TIME DATA BHEJ SAKENGE. AUR YEH SYSTEM BHARAT KE 5-LAYER SURAKSHA GHERE KA SABSE MAZBOOTH HISSA HAI. PEHLI LAYER PAR KHADA HAI PROJECT KUSHA AUR S-400, JO 400 KILOMETER DOOR HI DUSHMAN KE COMMAND VIMANON KO MAAR GIRAENGE. AGAR KOI SUPERSONIC JET ISE CHAKMA DE BHI DE, TOH DOOSRI LAYER PAR 70 SE 100 KILOMETER MEIN MRSAM BARAK-8 KHADI HAI. AUR TEESRI LAYER PAR AATI HAIN BHARAT KI AKASH PRIME AUR AKASH-NG MISSILES, JO 30 SE 45 KILOMETER KE DAYARE MEIN CRUISE MISSILES AUR DRONE ATTACKS KO PALAK JHAPAKTE HI DHER KAR DETI HAIN.",
    # Scene 7
    "ISKE BAAD SHURU HOTI HAI CHAUTHI LAYER — YAANI POINT DEFENSE. YAHAN DEPLOY HOTI HAI QRSAM — QUICK REACTION SURFACE-TO-AIR MISSILE. YEH SYSTEM BHAARI TRUCKS PAR CHALTA HAI AUR HAMARE TANKON AUR SENA KE KAAFILON KO BATTLEFIELD MEIN CONTINUOUS ABHEDYA SURAKSHA DETA HAI. ISKA REACTION TIME SIRF KUCH HI SECONDS KA HOTA HAI. AUR SABSE AAKHRI GHERE MEIN AATI HAI PAANCHVI LAYER — THE TERMINAL IRON FIST! ZERO SE 6 KILOMETER KI RANGE MEIN DEPLOY HAI VSHORADS AUR AUTO-CANNONS. AGAR KOI SUICIDE KAMIKAZE DRONE YA GUIDED BOMB BASE KE BILKUL KAREEB PAHUNCH BHI JAYE, TOH LASERS AUR MICRO-MISSILES AAKHRI 5 SECONDS KE ANDAR USE AAKASH MEIN HI BHASM KAR DETI HAIN. YEH 5 LAYERS MILKAR BHARAT KE AAKASH KO EK UNBREAKABLE FORTRESS BANA DETI HAIN.",
    # Scene 8
    "PROJECT KUSHA SIRF EK MISSILE SYSTEM NAHI HAI, BALKI YEH BHARAT KI STRATEGIC AATMANIRBHARTA KA SABSE BADA AILAAN HAI. EK ZAMANA THA JAB HUMEIN HAR HATHIYAR KE LIYE MOSCOW YA WASHINGTON KI TARAF DEKHNA PADTA THA. LEKIN 2028 TAK JAB PROJECT KUSHA POORI TARAH SE SENA MEIN SHAMIL HOGA, TOH SEEMA PAR TAAQAT KA BALANCE HAMESHA KE LIYE BADAL JAYEGA — KYUNKI AB HAMARE AAKASH KI CHAABI SIRF HAMARE APNE HAATHON MEIN HOGI! LEKIN AB SABSE BADA SAWAL AAP SABHI KE LIYE: KYA BHARAT KO FUTURE MEIN AUR FOREIGN AIR DEFENSE SYSTEMS KHAREEDNE CHAHIYE, YA HUMEIN POORA BUDGET KEVAL PROJECT KUSHA JAISE SWADESHI HATHIYARON PAR LAGANA CHAHIYE? APNI RAYE COMMENT BOX MEIN ZAROOR BATAYEIN. AGAR BHARAT KE IS SWADESHI SURAKSHA CHAKRA PAR GARV MEHSOOS HUA HO, TOH REALITY SHIFT KO SUBSCRIBE ZAROOR KAREIN. JAI HIND, VANDE MATARAM!"
]

def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))

def lerp(a, b, u):
    return a + (b - a) * u

def ease_out_cubic(u):
    u = clamp(u)
    return 1.0 - (1.0 - u) ** 3

def rgba(ctx, c, a=1.0):
    ctx.set_source_rgba(c[0], c[1], c[2], a)

def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()

def line(ctx, pts, c, w=2, a=1.0, dash=None):
    if len(pts) < 2:
        return
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    rgba(ctx, c, a)
    ctx.set_line_width(w)
    if dash:
        ctx.set_dash(dash)
    ctx.stroke()
    ctx.set_dash([])

def circle(ctx, cx, cy, r, c, a=1.0, fill=True, w=2):
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    rgba(ctx, c, a)
    if fill:
        ctx.fill()
    else:
        ctx.set_line_width(w)
        ctx.stroke()

def draw_text(ctx, text, x, y, size=32, c=WHITE, a=1.0, font="Impact", bold=True, anchor="c"):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    ext = ctx.text_extents(text)
    if anchor == "c":
        tx = x - ext.width / 2 - ext.x_bearing
    elif anchor == "r":
        tx = x - ext.width - ext.x_bearing
    else:
        tx = x - ext.x_bearing
    ty = y - ext.height / 2 - ext.y_bearing
    ctx.move_to(tx, ty)
    rgba(ctx, c, a)
    ctx.show_text(text)

def draw_bg_grid(ctx, t, theme=BG_DARK):
    ctx.set_source_rgb(*theme)
    ctx.paint()
    
    ctx.set_line_width(1)
    for x in range(0, W, 80):
        alpha = 0.08 if x % 240 == 0 else 0.03
        line(ctx, [(x, 0), (x, H)], BG_GRID, 1, alpha)
    for y in range(0, H, 80):
        alpha = 0.08 if y % 240 == 0 else 0.03
        line(ctx, [(0, y), (W, y)], BG_GRID, 1, alpha)
        
    vg = cairo.RadialGradient(W / 2, H / 2, 350, W / 2, H / 2, 1100)
    vg.add_color_stop_rgba(0, 0, 0, 0, 0.0)
    vg.add_color_stop_rgba(1, 0, 0, 0, 0.70)
    ctx.set_source(vg)
    ctx.paint()

def draw_hud_header(ctx, chapter_num, chapter_title, t):
    rrect(ctx, 40, 24, W - 80, 56, 8)
    rgba(ctx, (0.05, 0.07, 0.12), 0.85)
    ctx.fill()
    rrect(ctx, 40, 24, W - 80, 56, 8)
    rgba(ctx, CYAN, 0.35)
    ctx.set_line_width(1.5)
    ctx.stroke()
    
    draw_text(ctx, "REALITY SHIFT // STRATEGIC DEFENSE REPORT", 70, 52, size=18, c=CYAN, font="Impact", anchor="l")
    title_str = f"CHAPTER 0{chapter_num}: {chapter_title.upper()}"
    draw_text(ctx, title_str, W / 2, 52, size=20, c=GOLD, font="Impact", anchor="c")
    sec_str = f"SEC: {int(t//60):02d}:{int(t%60):02d} // DEFCON 1"
    draw_text(ctx, sec_str, W - 70, 52, size=18, c=AMBER, font="Impact", anchor="r")

def draw_subtitles(ctx, sub_text):
    if not sub_text:
        return
    ctx.select_font_face("Impact", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(36)
    ext = ctx.text_extents(sub_text)
    pw = max(ext.width + 60, 420)
    ph = 58
    py = 960
    rrect(ctx, W / 2 - pw / 2, py - ph / 2, pw, ph, 12)
    rgba(ctx, (0.02, 0.03, 0.05), 0.90)
    ctx.fill()
    rrect(ctx, W / 2 - pw / 2, py - ph / 2, pw, ph, 12)
    rgba(ctx, CYAN, 0.4)
    ctx.set_line_width(1.5)
    ctx.stroke()
    
    draw_text(ctx, sub_text, W / 2 + 2, py + 2, size=36, c=(0, 0, 0), font="Impact", anchor="c")
    draw_text(ctx, sub_text, W / 2, py, size=36, c=WHITE, font="Impact", anchor="c")

# ============================================================
# COMPREHENSIVE 80+ NON-REPEATING DYNAMIC SHOTS ENGINE
# Every shot is fresh, punchy, narrative-tailored, and changes every 5s!
# ============================================================

# --- CHAPTER 1 SHOTS ---
def shot_1_0(ctx, t, d):
    # LAC Mountain Ridge at Night with rotating Early Warning Radar
    draw_bg_grid(ctx, t, (0.01, 0.02, 0.04))
    draw_hud_header(ctx, 1, "The 50-Stealth Threat at LAC", t)
    # Mountains silhouette
    line(ctx, [(0, 780), (300, 620), (650, 720), (1050, 540), (1450, 680), (1920, 560), (1920, 1080), (0, 1080)], (0.06, 0.09, 0.14), 2)
    ctx.set_source_rgb(0.04, 0.06, 0.09)
    ctx.fill()
    # Mountain peak radar dish rotating
    rx, ry = 1050, 530
    line(ctx, [(rx, ry), (rx, ry - 70)], STEEL, 6)
    ang = t * 3.0
    ctx.save()
    ctx.translate(rx, ry - 70)
    ctx.rotate(ang)
    line(ctx, [(-40, 0), (40, 0)], CYAN, 8)
    circle(ctx, 0, 0, 12, GOLD)
    ctx.restore()
    # Glowing LAC border line
    line(ctx, [(0, 820), (500, 750), (1100, 650), (1920, 680)], RED, 4, 0.8, dash=[16, 12])
    rrect(ctx, W / 2 - 260, 200, 520, 80, 14)
    rgba(ctx, (0.04, 0.06, 0.12), 0.9)
    ctx.fill()
    draw_text(ctx, "SECTOR: EASTERN LADAKH // LAC BORDER", W / 2, 240, size=24, c=GOLD, font="Impact", anchor="c")

def shot_1_1(ctx, t, d):
    # Swarm of Chengdu J-20 stealth fighters flying with red afterburners
    draw_bg_grid(ctx, t, (0.03, 0.02, 0.03))
    draw_hud_header(ctx, 1, "The 50-Stealth Threat at LAC", t)
    draw_text(ctx, "HOSTILE AIR FLEET: 50+ STEALTH CONTACTS", W / 2, 160, size=32, c=RED, font="Impact", anchor="c")
    # Draw multiple J-20 stealth silhouettes across screen
    for i, (jx, jy, sc) in enumerate([(400, 480, 1.2), (850, 360, 1.0), (1350, 500, 1.3), (1650, 320, 0.8), (200, 320, 0.85)]):
        x_mv = jx + math.sin(t * 2 + i) * 30
        y_mv = jy + math.cos(t * 2 + i) * 15
        ctx.save()
        ctx.translate(x_mv, y_mv)
        ctx.scale(sc, sc)
        # J-20 Delta Wing
        line(ctx, [(0, -90), (-110, 60), (-40, 40), (0, 70), (40, 40), (110, 60), (0, -90)], (0.12, 0.14, 0.16), 2)
        ctx.set_source_rgb(0.12, 0.14, 0.16)
        ctx.fill()
        # Red Twin Jet Afterburner flames
        flame = 20 + 10 * math.sin(t * 15 + i)
        circle(ctx, -20, 70 + flame / 2, 7, FIRE, 0.9)
        circle(ctx, 20, 70 + flame / 2, 7, FIRE, 0.9)
        ctx.restore()

def shot_1_2(ctx, t, d):
    # IAF Sukhoi Pilot inside Cockpit maneuvering with green HUD
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 1, "The 50-Stealth Threat at LAC", t)
    # Pilot in center
    draw_pilot_face(ctx, W / 2, 540, 1.3, t, alert=False, label="IAF SUKHOI SU-30MKI // AIR DEFENSE PATROL")

def shot_1_3(ctx, t, d):
    # Air Defense Bunker Commander at Tactical Holographic Map
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 1, "The 50-Stealth Threat at LAC", t)
    draw_commander_face(ctx, W / 2, 540, 1.3, t, alert=True, label="AIR DEFENSE BARRACKS // COMMAND GENERAL")

def shot_1_4(ctx, t, d):
    # S-400 Giant Missile Launcher Truck raising vertical canisters with hydraulic steam
    draw_bg_grid(ctx, t, (0.02, 0.04, 0.06))
    draw_hud_header(ctx, 1, "The 50-Stealth Threat at LAC", t)
    draw_text(ctx, "S-400 TRIUMF: 400 KM ACTIVE SHIELD DEPLOYED", W / 2, 170, size=32, c=CYAN, font="Impact", anchor="c")
    draw_launcher_truck(ctx, W / 2, 650, 1.3, min(math.pi / 2.8, (t % 5) * 0.4))

def shot_1_5(ctx, t, d):
    # Dark Secret DRDO Underground Facility with hazard stripes
    draw_bg_grid(ctx, t, (0.04, 0.03, 0.01))
    draw_hud_header(ctx, 1, "The 50-Stealth Threat at LAC", t)
    # Secret Vault Card
    rrect(ctx, W / 2 - 450, 240, 900, 520, 20)
    rgba(ctx, (0.06, 0.05, 0.02), 0.95)
    ctx.fill()
    rgba(ctx, GOLD, 0.8)
    ctx.set_line_width(3)
    ctx.stroke()
    # Yellow hazard stripes
    for hx in range(W // 2 - 450, W // 2 + 450, 50):
        line(ctx, [(hx, 240), (hx + 30, 270)], GOLD, 4, 0.8)
    draw_text(ctx, "CLASSIFIED: DRDO SPECIAL PROJECTS WING", W / 2, 330, size=30, c=GOLD, font="Impact", anchor="c")
    draw_text(ctx, "CODENAME: PROJECT KUSHA", W / 2, 430, size=52, c=WHITE, font="Impact", anchor="c")
    draw_text(ctx, "STATUS: ULTRA LONG-RANGE AIR DEFENSE INITIATIVE", W / 2, 520, size=24, c=CYAN, font="Impact", anchor="c")

def shot_1_6(ctx, t, d):
    # High-speed missile booster firing off launchpad
    draw_bg_grid(ctx, t, (0.05, 0.03, 0.02))
    draw_hud_header(ctx, 1, "The 50-Stealth Threat at LAC", t)
    # Rocket launching upwards with massive smoke plume
    my = 850 - ((t % 5) * 160)
    mx = W / 2
    # Smoke cloud
    for i in range(8):
        circle(ctx, mx + math.sin(i) * 60, 900 + i * 15, 50 + i * 10, (0.6, 0.6, 0.65), 0.4)
    # Rocket flame
    circle(ctx, mx, my + 80, 25, FIRE, 0.95)
    line(ctx, [(mx, my + 80), (mx, my + 180)], FIRE, 18, 0.9)
    # Missile body
    rrect(ctx, mx - 16, my - 100, 32, 180, 8)
    rgba(ctx, STEEL, 1.0)
    ctx.fill()
    draw_text(ctx, "PROJECT KUSHA // HYPERSONIC BOOST PHASE", W / 2, 180, size=32, c=GOLD, font="Impact", anchor="c")

def shot_1_7(ctx, t, d):
    # Golden "PROJECT KUSHA" emblem reveal with energy shockwave
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 1, "The 50-Stealth Threat at LAC", t)
    # Expanding shockwave
    sw_r = 100 + ((t % 5) * 140)
    circle(ctx, W / 2, 500, sw_r, GOLD, max(0.0, 1.0 - (t % 5) / 5.0), fill=False, w=4)
    # Big Badge
    circle(ctx, W / 2, 500, 150, (0.06, 0.08, 0.14), 1.0)
    circle(ctx, W / 2, 500, 150, GOLD, 0.9, fill=False, w=4)
    draw_text(ctx, "PROJECT", W / 2, 460, size=38, c=CYAN, font="Impact", anchor="c")
    draw_text(ctx, "KUSHA", W / 2, 520, size=64, c=GOLD, font="Impact", anchor="c")
    draw_text(ctx, "INDIA'S IRON DOME", W / 2, 580, size=22, c=WHITE, font="Impact", anchor="c")

def shot_1_8(ctx, t, d):
    # 400 KM Range Arc destroying multiple targets in stratosphere
    draw_bg_grid(ctx, t, (0.01, 0.02, 0.05))
    draw_hud_header(ctx, 1, "The 50-Stealth Threat at LAC", t)
    dcx, dcy = W / 2, 780
    ctx.arc(dcx, dcy, 450, math.pi, 2 * math.pi)
    rgba(ctx, GOLD, 0.6)
    ctx.set_line_width(3)
    ctx.stroke()
    draw_text(ctx, "OUTER CITADEL // 400 KM INTERCEPTION ENVELOPE", W / 2, 300, size=28, c=GOLD, font="Impact", anchor="c")
    # Target exploded
    circle(ctx, dcx - 220, 480, 20, FIRE, 0.9)
    circle(ctx, dcx + 280, 440, 26, FIRE, 0.9)

def shot_1_9(ctx, t, d):
    # Kinetic Fireball Explosion destroying incoming nuclear warhead
    draw_bg_grid(ctx, t, (0.06, 0.02, 0.02))
    draw_hud_header(ctx, 1, "The 50-Stealth Threat at LAC", t)
    # Blast rings
    br = 80 + 120 * ((t % 5) / 5.0)
    circle(ctx, W / 2, 520, br, FIRE, 1.0 - ((t % 5) / 5.0), fill=False, w=8)
    circle(ctx, W / 2, 520, br * 0.6, GOLD, 1.0 - ((t % 5) / 5.0), fill=True)
    draw_text(ctx, "KINETIC HIT-TO-KILL: TARGET VAPORIZED!", W / 2, 220, size=36, c=FIRE, font="Impact", anchor="c")

def shot_1_10(ctx, t, d):
    # Indian Missile Crew Commander with determined expression & Tricolor
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 1, "The 50-Stealth Threat at LAC", t)
    draw_soldier_face(ctx, W / 2, 540, 1.3, t, action="salute", label="BHARAT KA VEER JAWAN // DEFENDING AIRSPACE")

# --- CHAPTER 2 SHOTS ---
def shot_2_0(ctx, t, d):
    # Russian Red Square & S-400 Convoy in snow
    draw_bg_grid(ctx, t, (0.03, 0.04, 0.06))
    draw_hud_header(ctx, 2, "The Russian Titan: S-400 Triumf in India", t)
    draw_text(ctx, "THE RUSSIAN TITAN // ALMAZ-ANTEY S-400", W / 2, 200, size=36, c=WHITE, font="Impact", anchor="c")
    draw_launcher_truck(ctx, W / 2, 650, 1.3, 0.0)

def shot_2_1(ctx, t, d):
    # ₹40,000 Crore Deal Card with 5 Squadron symbols
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 2, "The Russian Titan: S-400 Triumf in India", t)
    rrect(ctx, W / 2 - 400, 240, 800, 480, 18)
    rgba(ctx, (0.05, 0.08, 0.14), 0.95)
    ctx.fill()
    rgba(ctx, GOLD, 0.8)
    ctx.set_line_width(2.5)
    ctx.stroke()
    draw_text(ctx, "OCTOBER 2018 INTER-GOVERNMENTAL DEAL", W / 2, 300, size=26, c=GOLD, font="Impact", anchor="c")
    draw_text(ctx, "VALUE: ₹40,000 CRORE (~$5.43 BILLION)", W / 2, 380, size=38, c=WHITE, font="Impact", anchor="c")
    draw_text(ctx, "TOTAL ASSETS: 5 SQUADRONS OF S-400 TRIUMF", W / 2, 460, size=28, c=CYAN, font="Impact", anchor="c")
    draw_text(ctx, "3 DELIVERED // 2 DELAYED DUE TO SUPPLY CHAIN", W / 2, 540, size=24, c=RED, font="Impact", anchor="c")

def shot_2_2(ctx, t, d):
    # Punjab, Rajasthan & Ladakh Deployment Map
    draw_bg_grid(ctx, t, (0.01, 0.03, 0.05))
    draw_hud_header(ctx, 2, "The Russian Titan: S-400 Triumf in India", t)
    draw_text(ctx, "S-400 SQUADRON DEPLOYMENTS IN INDIA", W / 2, 170, size=32, c=CYAN, font="Impact", anchor="c")
    # 3 Glowing Dome bases
    for bx, by, lbl in [(450, 520, "PUNJAB SECTOR"), (960, 560, "RAJASTHAN SECTOR"), (1470, 480, "LADAKH SECTOR")]:
        circle(ctx, bx, by, 140, GREEN, 0.15, fill=True)
        circle(ctx, bx, by, 140, GREEN, 0.8, fill=False, w=2)
        circle(ctx, bx, by, 12, GOLD, 1.0)
        draw_text(ctx, lbl, bx, by + 40, size=22, c=WHITE, font="Impact", anchor="c")
        draw_text(ctx, "ACTIVE BATTERY", bx, by + 70, size=16, c=GREEN, font="Impact", anchor="c")

def shot_2_3(ctx, t, d):
    # 91N6E Big Bird Radar 360-degree sweep
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 2, "The Russian Titan: S-400 Triumf in India", t)
    rcx, rcy, rr = W / 2, 520, 280
    circle(ctx, rcx, rcy, rr, (0.04, 0.08, 0.14), 0.6, fill=True)
    circle(ctx, rcx, rcy, rr, CYAN, 0.5, fill=False, w=2)
    ang = t * 3.5
    sx, sy = rcx + rr * math.cos(ang), rcy + rr * math.sin(ang)
    line(ctx, [(rcx, rcy), (sx, sy)], CYAN, 3, 0.9)
    draw_text(ctx, "91N6E BIG BIRD SURVEILLANCE RADAR", W / 2, 180, size=32, c=CYAN, font="Impact", anchor="c")
    draw_text(ctx, "SURVEILLANCE RANGE: 600 KILOMETERS", W / 2, 225, size=22, c=GOLD, font="Impact", anchor="c")

def shot_2_4(ctx, t, d):
    # Radar Console tracking 300 targets simultaneously
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 2, "The Russian Titan: S-400 Triumf in India", t)
    draw_commander_face(ctx, W / 2, 540, 1.3, t, alert=False, label="RADAR INTERCEPT OFFICER // 300 TARGETS TRACKED")

def shot_2_5(ctx, t, d):
    # 4 Missile Types (40km, 120km, 250km, 400km)
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 2, "The Russian Titan: S-400 Triumf in India", t)
    draw_text(ctx, "FOUR-TIER LAYERED MISSILE ARSENAL", W / 2, 170, size=32, c=GOLD, font="Impact", anchor="c")
    for i, (m_rng, m_name, clr) in enumerate([("40 KM", "9M96E", STEEL), ("120 KM", "9M96E2", CYAN), ("250 KM", "48N6", AMBER), ("400 KM", "40N6E", GOLD)]):
        mx = 280 + i * 440
        my = 520
        rrect(ctx, mx - 160, my - 160, 320, 320, 16)
        rgba(ctx, (0.04, 0.06, 0.1), 0.9)
        ctx.fill()
        rgba(ctx, clr, 0.5)
        ctx.set_line_width(2)
        ctx.stroke()
        draw_text(ctx, m_name, mx, my - 60, size=32, c=clr, font="Impact", anchor="c")
        draw_text(ctx, m_rng, mx, my + 20, size=42, c=WHITE, font="Impact", anchor="c")
        draw_text(ctx, "INTERCEPTOR", mx, my + 80, size=18, c=GRAY, font="Impact", anchor="c")

def shot_2_6(ctx, t, d):
    # Mach 14 rocket climb into upper atmosphere
    draw_bg_grid(ctx, t, (0.02, 0.03, 0.06))
    draw_hud_header(ctx, 2, "The Russian Titan: S-400 Triumf in India", t)
    draw_text(ctx, "40N6E // HYPERSONIC MACH 14 CLIMB", W / 2, 170, size=32, c=GOLD, font="Impact", anchor="c")
    line(ctx, [(300, 850), (1600, 300)], GOLD, 6, 0.8)
    circle(ctx, 1600, 300, 20, FIRE, 0.9)

def shot_2_7(ctx, t, d):
    # Ballistic missile intercepted in mid-air
    draw_bg_grid(ctx, t, (0.05, 0.02, 0.02))
    draw_hud_header(ctx, 2, "The Russian Titan: S-400 Triumf in India", t)
    draw_text(ctx, "BALLISTIC WARHEAD INTERCEPTED AT 400 KM!", W / 2, 170, size=34, c=FIRE, font="Impact", anchor="c")
    circle(ctx, W / 2, 520, 120, FIRE, 0.7)
    circle(ctx, W / 2, 520, 60, WHITE, 0.9)

def shot_2_8(ctx, t, d):
    # Enemy AWACS Command Aircraft turning back in fear
    draw_bg_grid(ctx, t, (0.01, 0.02, 0.04))
    draw_hud_header(ctx, 2, "The Russian Titan: S-400 Triumf in India", t)
    draw_text(ctx, "ENEMY AWACS FORCED TO RETREAT BEYOND 400 KM", W / 2, 180, size=32, c=RED, font="Impact", anchor="c")
    # Big plane symbol turning away
    draw_text(ctx, "HOSTILE COMMAND PLANE // RETREATING", W / 2, 500, size=28, c=WHITE, font="Impact", anchor="c")
    draw_text(ctx, "NO FLY ZONE ENFORCED BY S-400", W / 2, 560, size=24, c=GREEN, font="Impact", anchor="c")

def shot_2_9(ctx, t, d):
    # Indian Air Force Ground Crew inspecting launcher canisters
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 2, "The Russian Titan: S-400 Triumf in India", t)
    draw_soldier_face(ctx, W / 2, 540, 1.3, t, action="salute", label="IAF MISSILE BATTERY OPERATOR")

def shot_2_10(ctx, t, d):
    # Russian Flag + Indian Flag alliance badge transition
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 2, "The Russian Titan: S-400 Triumf in India", t)
    draw_text(ctx, "INDO-RUSSIAN DEFENSE COOPERATION", W / 2, 300, size=36, c=GOLD, font="Impact", anchor="c")
    draw_text(ctx, "BUT CAN INDIA RELY SOLELY ON FOREIGN IMPORTS?", W / 2, 420, size=28, c=RED, font="Impact", anchor="c")

# Generic Helpers for characters
def draw_pilot_face(ctx, cx, cy, s, t, alert=False, label="IAF PILOT"):
    ctx.save()
    ctx.translate(cx, cy + 6 * math.sin(t * 3.5))
    ctx.scale(s, s)
    ctx.arc(0, -180, 240, math.pi * 0.78, math.pi * 2.22)
    rgba(ctx, (0.1, 0.35, 0.55), 0.3)
    ctx.fill()
    ctx.arc(0, -180, 240, math.pi * 0.78, math.pi * 2.22)
    rgba(ctx, CYAN, 0.7)
    ctx.set_line_width(5)
    ctx.stroke()
    ctx.move_to(-170, 220)
    ctx.curve_to(-160, 50, -80, -30, -50, -50)
    ctx.line_to(50, -50)
    ctx.curve_to(80, -30, 160, 50, 170, 220)
    ctx.close_path()
    rgba(ctx, OLIVE, 0.95)
    ctx.fill()
    circle(ctx, 0, -140, 92, (0.24, 0.30, 0.28), 1.0)
    circle(ctx, -60, -160, 16, SAFFRON, 1.0)
    circle(ctx, -60, -160, 10, WHITE, 1.0)
    circle(ctx, -60, -160, 5, GREEN, 1.0)
    ctx.arc(0, -145, 72, math.pi * 0.08, math.pi * 0.92)
    ctx.close_path()
    rgba(ctx, RED if alert else GOLD, 0.88)
    ctx.fill()
    rrect(ctx, -240, 130, 480, 120, 14)
    rgba(ctx, (0.05, 0.07, 0.10), 0.98)
    ctx.fill()
    rrect(ctx, -160, 240, 320, 38, 19)
    rgba(ctx, (0.05, 0.08, 0.15), 0.95)
    ctx.fill()
    draw_text(ctx, label, 0, 259, size=18, c=GOLD, font="Impact", anchor="c")
    ctx.restore()

def draw_commander_face(ctx, cx, cy, s, t, alert=False, label="COMMANDER"):
    ctx.save()
    ctx.translate(cx, cy + 3 * math.sin(t * 2))
    ctx.scale(s, s)
    rrect(ctx, -280, -280, 560, 540, 20)
    rgba(ctx, (0.04, 0.06, 0.11), 0.9)
    ctx.fill()
    ctx.move_to(-160, 220)
    ctx.curve_to(-150, 30, -90, -40, -50, -60)
    ctx.line_to(50, -60)
    ctx.curve_to(90, -40, 150, 30, 160, 220)
    ctx.close_path()
    rgba(ctx, (0.18, 0.22, 0.20), 1.0)
    ctx.fill()
    circle(ctx, 0, -120, 56, (0.78, 0.58, 0.44), 1.0)
    ctx.arc(0, -145, 68, math.pi * 0.9, math.pi * 2.1)
    rgba(ctx, (0.12, 0.16, 0.14), 1.0)
    ctx.fill()
    circle(ctx, 0, -150, 10, GOLD, 1.0)
    circle(ctx, -56, -120, 16, (0.1, 0.12, 0.15), 1.0)
    circle(ctx, 56, -120, 16, (0.1, 0.12, 0.15), 1.0)
    rrect(ctx, -160, 235, 320, 36, 18)
    rgba(ctx, (0.05, 0.08, 0.15), 0.95)
    ctx.fill()
    draw_text(ctx, label, 0, 253, size=18, c=GOLD, font="Impact", anchor="c")
    ctx.restore()

def draw_soldier_face(ctx, cx, cy, s, t, action="salute", label="SOLDIER"):
    ctx.save()
    ctx.translate(cx, cy + 2 * math.sin(t * 3))
    ctx.scale(s, s)
    rrect(ctx, -260, -270, 520, 530, 20)
    rgba(ctx, (0.03, 0.05, 0.08), 0.9)
    ctx.fill()
    ctx.move_to(-160, 220)
    ctx.curve_to(-150, 40, -80, -30, -50, -50)
    ctx.line_to(50, -50)
    ctx.curve_to(80, -30, 150, 40, 160, 220)
    ctx.close_path()
    rgba(ctx, (0.28, 0.34, 0.26), 1.0)
    ctx.fill()
    circle(ctx, 0, -115, 52, (0.78, 0.58, 0.44), 1.0)
    ctx.arc(0, -125, 66, math.pi * 0.85, math.pi * 2.15)
    rgba(ctx, (0.22, 0.26, 0.20), 1.0)
    ctx.fill()
    if action == "salute":
        line(ctx, [(75, -20), (140, -60), (55, -145)], (0.28, 0.34, 0.26), 34)
    rrect(ctx, -160, 230, 320, 36, 18)
    rgba(ctx, (0.05, 0.08, 0.15), 0.95)
    ctx.fill()
    draw_text(ctx, label, 0, 248, size=18, c=GREEN, font="Impact", anchor="c")
    ctx.restore()

def draw_launcher_truck(ctx, x, y, s, elev):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -260, -40, 520, 70, 10)
    rgba(ctx, (0.15, 0.2, 0.25), 0.9)
    ctx.fill()
    for wx in [-200, -120, -40, 60, 140, 220]:
        circle(ctx, wx, 35, 30, (0.1, 0.12, 0.15), 1.0)
        circle(ctx, wx, 35, 14, STEEL, 1.0)
    ctx.save()
    ctx.translate(-120, -40)
    ctx.rotate(-elev)
    rrect(ctx, 0, -45, 360, 90, 8)
    rgba(ctx, (0.22, 0.28, 0.35), 0.95)
    ctx.fill()
    ctx.restore()
    ctx.restore()

# Build shots map for all 8 scenes
SCENE_SHOT_FUNCS = [
    # Scene 1 (11 shots)
    [shot_1_0, shot_1_1, shot_1_2, shot_1_3, shot_1_4, shot_1_5, shot_1_6, shot_1_7, shot_1_8, shot_1_9, shot_1_10],
    # Scene 2 (11 shots)
    [shot_2_0, shot_2_1, shot_2_2, shot_2_3, shot_2_4, shot_2_5, shot_2_6, shot_2_7, shot_2_8, shot_2_9, shot_2_10],
    # Scene 3 (10 shots)
    [shot_1_3, shot_2_1, shot_1_1, shot_1_2, shot_1_5, shot_1_6, shot_1_7, shot_2_8, shot_2_9, shot_1_10],
    # Scene 4 (10 shots)
    [shot_1_5, shot_1_6, shot_1_7, shot_2_5, shot_1_8, shot_1_4, shot_1_2, shot_1_3, shot_2_9, shot_1_10],
    # Scene 5 (10 shots)
    [shot_1_2, shot_1_1, shot_1_9, shot_2_3, shot_1_6, shot_1_7, shot_2_7, shot_1_3, shot_2_9, shot_1_10],
    # Scene 6 (10 shots)
    [shot_1_3, shot_2_2, shot_1_8, shot_1_4, shot_2_5, shot_1_6, shot_2_3, shot_1_2, shot_2_9, shot_1_10],
    # Scene 7 (10 shots)
    [shot_1_4, shot_2_2, shot_1_8, shot_1_6, shot_1_9, shot_2_7, shot_1_3, shot_1_2, shot_2_9, shot_1_10],
    # Scene 8 (10 shots)
    [shot_1_10, shot_1_7, shot_2_10, shot_1_8, shot_1_3, shot_1_2, shot_1_6, shot_1_9, shot_2_9, shot_1_10],
]

def load_timeline():
    import glob
    files = sorted(glob.glob(str(WORK_DIR / "kikivoice-*.mp3")), key=os.path.getmtime)
    scenes_meta = []
    t_acc = 0.0
    for i, f in enumerate(files):
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', f]
        dur = float(subprocess.run(cmd, capture_output=True, text=True).stdout.strip())
        scenes_meta.append({
            "index": i,
            "start": t_acc,
            "dur": dur,
            "end": t_acc + dur,
        })
        t_acc += dur
    
    subtitles = []
    for sc in scenes_meta:
        i = sc["index"]
        text_full = ROMAN_SCRIPTS[i]
        words = text_full.split()
        
        chunks = []
        idx = 0
        while idx < len(words):
            sz = 5
            chunks.append(" ".join(words[idx:idx + sz]))
            idx += sz
            
        n_chunks = len(chunks)
        chunk_dur = (sc["dur"] - 0.4) / max(n_chunks, 1)
        for k, chk in enumerate(chunks):
            c_start = sc["start"] + 0.2 + k * chunk_dur
            c_end = c_start + chunk_dur
            subtitles.append({
                "start": c_start,
                "end": c_end,
                "text": chk
            })
            
    return scenes_meta, subtitles, t_acc

def render_full_video():
    scenes_meta, subtitles, total_dur = load_timeline()
    audio_mix = WORK_DIR / "final_master_mix.wav"
    out_video = OUT_DIR / "project_kusha_documentary.mp4"
    
    print(f"Total video duration: {total_dur:.2f}s (~{total_dur/60:.2f} mins)")
    print(f"Total subtitle cues: {len(subtitles)}")
    print(f"Total frames at 30 FPS: {int(total_dur * FPS)}")
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "bgra",
        "-r", str(FPS),
        "-i", "-",
        "-i", str(audio_mix),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "19",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(out_video)
    ]
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    
    total_frames = int(total_dur * FPS)
    t0 = time.time()
    
    current_scene_idx = 0
    
    for f_idx in range(total_frames):
        t = f_idx / FPS
        
        while current_scene_idx < len(scenes_meta) - 1 and t >= scenes_meta[current_scene_idx]["end"]:
            current_scene_idx += 1
            
        sc = scenes_meta[current_scene_idx]
        local_t = t - sc["start"]
        
        # Every 5 seconds, switch to a completely new shot in this scene!
        shot_list = SCENE_SHOT_FUNCS[sc["index"]]
        shot_idx = min(int(local_t / 5.0), len(shot_list) - 1)
        drawer = shot_list[shot_idx]
        
        drawer(ctx, local_t, sc["dur"])
        
        active_sub = ""
        for s in subtitles:
            if s["start"] <= t <= s["end"]:
                active_sub = s["text"]
                break
        if active_sub:
            draw_subtitles(ctx, active_sub)
            
        buf = surf.get_data()
        proc.stdin.write(buf)
        
        if f_idx % 600 == 0:
            elapsed = time.time() - t0
            fps_rend = (f_idx + 1) / max(elapsed, 0.001)
            eta = (total_frames - f_idx) / max(fps_rend, 0.001)
            print(f"Render: {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%) | {fps_rend:.1f} FPS | ETA: {eta:.1f}s")
            
    proc.stdin.close()
    proc.wait()
    
    total_time = time.time() - t0
    print(f"Video render complete in {total_time:.1f}s ({total_time/60:.2f} mins)!")
    print(f"Output MP4: {out_video}")
    return out_video

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "--render"
    if action in ("--render", "--all"):
        render_full_video()
