"""Project Kusha vs S-400: Inside India's Ultra Long-Range Air Defense Shield
Full Long-Form 16:9 (1920x1080) Widescreen Documentary Renderer with Dynamic Characters for RealityShift.
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
NAVY = (0.06, 0.10, 0.18)

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

def ease_in_out(u):
    u = clamp(u)
    return u * u * (3.0 - 2.0 * u)

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

def draw_bg_grid(ctx, t):
    ctx.set_source_rgb(*BG_DARK)
    ctx.paint()
    
    ctx.set_line_width(1)
    for x in range(0, W, 80):
        alpha = 0.08 if x % 240 == 0 else 0.03
        line(ctx, [(x, 0), (x, H)], BG_GRID, 1, alpha)
    for y in range(0, H, 80):
        alpha = 0.08 if y % 240 == 0 else 0.03
        line(ctx, [(0, y), (W, y)], BG_GRID, 1, alpha)
        
    vg = cairo.RadialGradient(W / 2, H / 2, 400, W / 2, H / 2, 1100)
    vg.add_color_stop_rgba(0, 0, 0, 0, 0.0)
    vg.add_color_stop_rgba(1, 0, 0, 0, 0.65)
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
    
    # Text with shadow
    draw_text(ctx, sub_text, W / 2 + 2, py + 2, size=36, c=(0, 0, 0), font="Impact", anchor="c")
    draw_text(ctx, sub_text, W / 2, py, size=36, c=WHITE, font="Impact", anchor="c")

# ============================================================
# ANIMATED CHARACTERS ENGINE
# ============================================================

def draw_iaf_pilot(ctx, cx, cy, s, t, alert=False, label="IAF SUKHOI PILOT"):
    """Fighter pilot in cockpit with dynamic HUD visor, oxygen mask & instrument glow."""
    ctx.save()
    ctx.translate(cx, cy + 6 * math.sin(t * 3.5))
    ctx.scale(s, s)
    
    # Cockpit canopy arch
    ctx.arc(0, -180, 240, math.pi * 0.78, math.pi * 2.22)
    rgba(ctx, (0.1, 0.35, 0.55), 0.3)
    ctx.fill()
    ctx.arc(0, -180, 240, math.pi * 0.78, math.pi * 2.22)
    rgba(ctx, CYAN, 0.7)
    ctx.set_line_width(5)
    ctx.stroke()
    
    # Canopy glint reflection moving with time
    glint_x = -120 + 240 * ((t * 0.5) % 1.0)
    line(ctx, [(glint_x, -360), (glint_x + 60, -80)], WHITE, 4, 0.4)
    
    # Shoulders & Flight Suit
    ctx.move_to(-170, 220)
    ctx.curve_to(-160, 50, -80, -30, -50, -50)
    ctx.line_to(50, -50)
    ctx.curve_to(80, -30, 160, 50, 170, 220)
    ctx.close_path()
    rgba(ctx, OLIVE, 0.95)
    ctx.fill()
    
    # Harness straps
    line(ctx, [(-50, -50), (-80, 220)], (0.1, 0.12, 0.1), 16)
    line(ctx, [(50, -50), (80, 220)], (0.1, 0.12, 0.1), 16)
    
    # Indian Tricolor arm patch
    rrect(ctx, -145, 80, 36, 24, 4)
    rgba(ctx, SAFFRON, 1.0)
    ctx.fill()
    rrect(ctx, -145, 88, 36, 8, 0)
    rgba(ctx, WHITE, 1.0)
    ctx.fill()
    rrect(ctx, -145, 96, 36, 8, 4)
    rgba(ctx, GREEN, 1.0)
    ctx.fill()
    
    # Flight Helmet
    circle(ctx, 0, -140, 92, (0.24, 0.30, 0.28), 1.0)
    # IAF Roundel on helmet
    circle(ctx, -60, -160, 16, SAFFRON, 1.0)
    circle(ctx, -60, -160, 10, WHITE, 1.0)
    circle(ctx, -60, -160, 5, GREEN, 1.0)
    
    # Visor (Gold / Tinted mirror HUD)
    ctx.arc(0, -145, 72, math.pi * 0.08, math.pi * 0.92)
    ctx.close_path()
    vis_c = RED if alert else GOLD
    rgba(ctx, vis_c, 0.88)
    ctx.fill()
    ctx.set_line_width(3)
    rgba(ctx, WHITE, 0.9)
    ctx.stroke()
    
    # Dynamic HUD reticle on visor
    ret_pulse = 0.5 + 0.5 * math.sin(t * 10)
    circle(ctx, 0, -135, 20, (1, 1, 1), 0.85, fill=False, w=1.5)
    line(ctx, [(-35, -135), (-15, -135)], (1, 1, 1), 2, 0.8)
    line(ctx, [(15, -135), (35, -135)], (1, 1, 1), 2, 0.8)
    line(ctx, [(0, -155), (0, -140)], (1, 1, 1), 2, 0.8)
    line(ctx, [(0, -130), (0, -115)], (1, 1, 1), 2, 0.8)
    
    # Oxygen mask & breathing tube
    ctx.move_to(-42, -95)
    ctx.line_to(42, -95)
    ctx.line_to(28, -40)
    ctx.line_to(-28, -40)
    ctx.close_path()
    rgba(ctx, (0.12, 0.14, 0.16), 1.0)
    ctx.fill()
    
    # Corrugated breathing tube
    tube_pulse = 4 * math.sin(t * 4)
    ctx.move_to(0, -40)
    ctx.curve_to(18 + tube_pulse, -10, -18 + tube_pulse, 30, 0, 90)
    ctx.set_line_width(18)
    rgba(ctx, (0.10, 0.11, 0.13), 1.0)
    ctx.stroke()
    
    # Cockpit Control Panel & MFD Screens
    rrect(ctx, -240, 130, 480, 120, 14)
    rgba(ctx, (0.05, 0.07, 0.10), 0.98)
    ctx.fill()
    rgba(ctx, CYAN, 0.4)
    ctx.set_line_width(2)
    ctx.stroke()
    
    # Left & Right MFD screens
    rrect(ctx, -210, 145, 120, 80, 6)
    rgba(ctx, (0.02, 0.15, 0.08), 1.0)
    ctx.fill()
    draw_text(ctx, "RADAR LOCK", -150, 185, size=14, c=GREEN, font="Impact")
    
    rrect(ctx, 90, 145, 120, 80, 6)
    rgba(ctx, (0.15, 0.05, 0.05) if alert else (0.02, 0.10, 0.18), 1.0)
    ctx.fill()
    draw_text(ctx, "MISSILE LOCK" if alert else "AIR SYS OK", 150, 185, size=14, c=RED if alert else CYAN, font="Impact")
    
    # Pilot Callout Badge
    rrect(ctx, -160, 240, 320, 38, 19)
    rgba(ctx, (0.05, 0.08, 0.15), 0.95)
    ctx.fill()
    rgba(ctx, GOLD, 0.7)
    ctx.set_line_width(1.5)
    ctx.stroke()
    draw_text(ctx, label, 0, 259, size=18, c=GOLD, font="Impact", anchor="c")
    
    ctx.restore()

def draw_commander_console(ctx, cx, cy, s, t, alert=False, label="AIR DEFENSE COMMANDER"):
    """Commander at war room tactical terminal giving launch authority."""
    ctx.save()
    ctx.translate(cx, cy + 3 * math.sin(t * 2))
    ctx.scale(s, s)
    
    # Bunker background panels
    rrect(ctx, -280, -280, 560, 540, 20)
    rgba(ctx, (0.04, 0.06, 0.11), 0.9)
    ctx.fill()
    rgba(ctx, CYAN, 0.35)
    ctx.set_line_width(2)
    ctx.stroke()
    
    # Commander Torso in military uniform
    ctx.move_to(-160, 220)
    ctx.curve_to(-150, 30, -90, -40, -50, -60)
    ctx.line_to(50, -60)
    ctx.curve_to(90, -40, 150, 30, 160, 220)
    ctx.close_path()
    rgba(ctx, (0.18, 0.22, 0.20), 1.0)
    ctx.fill()
    
    # Collar & Indian Army rank stars on epaulets
    rrect(ctx, -120, 0, 40, 20, 4)
    rgba(ctx, GOLD, 0.9)
    ctx.fill()
    rrect(ctx, 80, 0, 40, 20, 4)
    rgba(ctx, GOLD, 0.9)
    ctx.fill()
    
    # Neck & Head
    rrect(ctx, -24, -80, 48, 40, 8)
    rgba(ctx, (0.78, 0.58, 0.44), 1.0) # skin tone
    ctx.fill()
    
    circle(ctx, 0, -120, 56, (0.78, 0.58, 0.44), 1.0)
    
    # Peaked Military Cap / Beret
    ctx.arc(0, -145, 68, math.pi * 0.9, math.pi * 2.1)
    rgba(ctx, (0.12, 0.16, 0.14), 1.0)
    ctx.fill()
    # Cap Crown & Golden Insignia
    rrect(ctx, -65, -165, 130, 30, 10)
    rgba(ctx, (0.12, 0.16, 0.14), 1.0)
    ctx.fill()
    circle(ctx, 0, -150, 10, GOLD, 1.0)
    # Visor shade
    rrect(ctx, -55, -140, 110, 14, 6)
    rgba(ctx, (0.05, 0.05, 0.06), 1.0)
    ctx.fill()
    
    # Tactical Comms Headset with boom mic
    circle(ctx, -56, -120, 16, (0.1, 0.12, 0.15), 1.0)
    circle(ctx, 56, -120, 16, (0.1, 0.12, 0.15), 1.0)
    line(ctx, [(-56, -140), (0, -180), (56, -140)], (0.2, 0.22, 0.25), 6)
    # Boom mic
    line(ctx, [(56, -120), (30, -95), (10, -95)], (0.15, 0.18, 0.2), 4)
    circle(ctx, 8, -95, 6, RED if alert else AMBER, 0.9)
    
    # Confident Eyes & Eyebrows
    line(ctx, [(-28, -125), (-10, -122)], (0.2, 0.15, 0.12), 3)
    line(ctx, [(10, -122), (28, -125)], (0.2, 0.15, 0.12), 3)
    circle(ctx, -18, -116, 4, (0.1, 0.1, 0.1), 1.0)
    circle(ctx, 18, -116, 4, (0.1, 0.1, 0.1), 1.0)
    
    # Interactive Holographic Command Table in front
    rrect(ctx, -240, 120, 480, 100, 14)
    rgba(ctx, (0.06, 0.09, 0.15), 0.95)
    ctx.fill()
    rgba(ctx, CYAN, 0.5)
    ctx.set_line_width(2)
    ctx.stroke()
    
    # Glowing radar ring on console
    circle(ctx, 0, 170, 36, CYAN, 0.25, fill=True)
    circle(ctx, 0, 170, 36, CYAN, 0.7, fill=False, w=1.5)
    line(ctx, [(0, 134), (0, 206)], CYAN, 1.5, 0.5)
    line(ctx, [(-36, 170), (36, 170)], CYAN, 1.5, 0.5)
    
    # Blinking red alert / threat blip
    pulse = 0.5 + 0.5 * math.sin(t * 8)
    circle(ctx, 16, 158, 5, RED, pulse)
    
    # Commander Badge
    rrect(ctx, -160, 235, 320, 36, 18)
    rgba(ctx, (0.05, 0.08, 0.15), 0.95)
    ctx.fill()
    rgba(ctx, GOLD, 0.8)
    ctx.set_line_width(1.5)
    ctx.stroke()
    draw_text(ctx, label, 0, 253, size=18, c=GOLD, font="Impact", anchor="c")
    
    ctx.restore()

def draw_drdo_scientist(ctx, cx, cy, s, t, label="DRDO CHIEF SCIENTIST"):
    """DRDO Missile Scientist with security badge and blueprint tablet."""
    ctx.save()
    ctx.translate(cx, cy + 2 * math.sin(t * 2.5))
    ctx.scale(s, s)
    
    # Lab backdrop card
    rrect(ctx, -260, -270, 520, 530, 20)
    rgba(ctx, (0.03, 0.06, 0.10), 0.9)
    ctx.fill()
    rgba(ctx, GOLD, 0.35)
    ctx.set_line_width(2)
    ctx.stroke()
    
    # Shoulders in Lab Coat
    ctx.move_to(-150, 220)
    ctx.curve_to(-140, 40, -80, -30, -45, -50)
    ctx.line_to(45, -50)
    ctx.curve_to(80, -30, 140, 40, 150, 220)
    ctx.close_path()
    rgba(ctx, (0.88, 0.92, 0.95), 1.0) # White lab coat
    ctx.fill()
    
    # Inner blue formal shirt & tie
    line(ctx, [(0, -50), (0, 140)], (0.1, 0.15, 0.25), 8)
    
    # DRDO Security Lanyard with ID Card
    line(ctx, [(-30, -50), (-15, 60)], (0.9, 0.5, 0.1), 3)
    line(ctx, [(30, -50), (15, 60)], (0.9, 0.5, 0.1), 3)
    rrect(ctx, -25, 60, 50, 65, 4)
    rgba(ctx, WHITE, 1.0)
    ctx.fill()
    rrect(ctx, -25, 60, 50, 15, 4)
    rgba(ctx, (0.1, 0.3, 0.6), 1.0)
    ctx.fill()
    draw_text(ctx, "DRDO", 0, 71, size=9, c=WHITE, font="Impact", anchor="c")
    
    # Head & Face
    circle(ctx, 0, -110, 52, (0.80, 0.62, 0.48), 1.0)
    # Hair
    ctx.arc(0, -125, 54, math.pi * 0.85, math.pi * 2.15)
    rgba(ctx, (0.15, 0.15, 0.18), 1.0)
    ctx.fill()
    
    # Glasses
    rrect(ctx, -38, -118, 30, 20, 4)
    rgba(ctx, CYAN, 0.3)
    ctx.fill()
    rgba(ctx, STEEL, 1.0)
    ctx.set_line_width(2)
    ctx.stroke()
    
    rrect(ctx, 8, -118, 30, 20, 4)
    rgba(ctx, CYAN, 0.3)
    ctx.fill()
    rgba(ctx, STEEL, 1.0)
    ctx.set_line_width(2)
    ctx.stroke()
    line(ctx, [(-8, -108), (8, -108)], STEEL, 2)
    
    # Tablet in hand
    rrect(ctx, 70, 70, 140, 110, 10)
    rgba(ctx, (0.05, 0.08, 0.12), 1.0)
    ctx.fill()
    rgba(ctx, CYAN, 0.8)
    ctx.set_line_width(2)
    ctx.stroke()
    # Missile blueprint on tablet
    line(ctx, [(140, 90), (140, 160)], GOLD, 4)
    line(ctx, [(130, 150), (150, 150)], AMBER, 2)
    draw_text(ctx, "M3: 400KM", 140, 105, size=12, c=CYAN, font="Impact", anchor="c")
    
    # Scientist Label
    rrect(ctx, -160, 230, 320, 36, 18)
    rgba(ctx, (0.05, 0.08, 0.15), 0.95)
    ctx.fill()
    rgba(ctx, GOLD, 0.8)
    ctx.set_line_width(1.5)
    ctx.stroke()
    draw_text(ctx, label, 0, 248, size=18, c=GOLD, font="Impact", anchor="c")
    
    ctx.restore()

def draw_missile_soldier(ctx, cx, cy, s, t, action="salute", label="AIR DEFENSE OPERATOR"):
    """Combat Soldier in digital camo saluting or operating missile launcher."""
    ctx.save()
    ctx.translate(cx, cy + 2 * math.sin(t * 3))
    ctx.scale(s, s)
    
    # Backdrop
    rrect(ctx, -260, -270, 520, 530, 20)
    rgba(ctx, (0.03, 0.05, 0.08), 0.9)
    ctx.fill()
    rgba(ctx, GREEN, 0.35)
    ctx.set_line_width(2)
    ctx.stroke()
    
    # Camouflage Uniform Torso
    ctx.move_to(-160, 220)
    ctx.curve_to(-150, 40, -80, -30, -50, -50)
    ctx.line_to(50, -50)
    ctx.curve_to(80, -30, 150, 40, 160, 220)
    ctx.close_path()
    rgba(ctx, (0.28, 0.34, 0.26), 1.0) # Camo olive
    ctx.fill()
    
    # Tactical Combat Vest
    rrect(ctx, -90, 0, 180, 180, 14)
    rgba(ctx, (0.18, 0.22, 0.18), 1.0)
    ctx.fill()
    # Mag pouches
    rrect(ctx, -70, 60, 40, 70, 6)
    rgba(ctx, (0.14, 0.17, 0.14), 1.0)
    ctx.fill()
    rrect(ctx, -15, 60, 40, 70, 6)
    rgba(ctx, (0.14, 0.17, 0.14), 1.0)
    ctx.fill()
    rrect(ctx, 40, 60, 40, 70, 6)
    rgba(ctx, (0.14, 0.17, 0.14), 1.0)
    ctx.fill()
    
    # Head & Ballistic Combat Helmet
    circle(ctx, 0, -115, 52, (0.78, 0.58, 0.44), 1.0)
    # Tactical Helmet with NVG mount
    ctx.arc(0, -125, 66, math.pi * 0.85, math.pi * 2.15)
    rgba(ctx, (0.22, 0.26, 0.20), 1.0)
    ctx.fill()
    # NVG mount bracket
    rrect(ctx, -15, -165, 30, 22, 4)
    rgba(ctx, (0.1, 0.1, 0.1), 1.0)
    ctx.fill()
    # Chinstrap
    line(ctx, [(-45, -120), (-25, -70), (25, -70), (45, -120)], (0.1, 0.1, 0.1), 4)
    
    # Saluting Arm or Launch Button
    if action == "salute":
        # Raised right saluting arm
        line(ctx, [(75, -20), (140, -60), (55, -145)], (0.28, 0.34, 0.26), 34)
        line(ctx, [(75, -20), (140, -60), (55, -145)], (0.18, 0.22, 0.18), 28)
        # Saluting hand at brow
        rrect(ctx, 35, -158, 30, 16, 6)
        rgba(ctx, (0.78, 0.58, 0.44), 1.0)
        ctx.fill()
    else: # launch action
        # Hand on launch console
        rrect(ctx, -140, 130, 280, 80, 10)
        rgba(ctx, (0.08, 0.1, 0.14), 1.0)
        ctx.fill()
        # Big Red Launch Button
        circle(ctx, 0, 170, 24, RED, 1.0)
        circle(ctx, 0, 170, 32, GOLD, 0.8, fill=False, w=3)
        draw_text(ctx, "FIRE", 0, 170, size=14, c=WHITE, font="Impact", anchor="c")
        
    # Soldier Label
    rrect(ctx, -160, 230, 320, 36, 18)
    rgba(ctx, (0.05, 0.08, 0.15), 0.95)
    ctx.fill()
    rgba(ctx, GREEN, 0.8)
    ctx.set_line_width(1.5)
    ctx.stroke()
    draw_text(ctx, label, 0, 248, size=18, c=GREEN, font="Impact", anchor="c")
    
    ctx.restore()

# ============================================================
# 8 DYNAMIC SCENES (WITH 5-SECOND CHARACTER ROTATION)
# ============================================================

def draw_scene_1(ctx, t, d):
    # Scene 1: LAC Threat & Opening Hook
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 1, "The 50-Stealth Threat at LAC", t)
    
    # Every 6s alternate between Character Focus & Weapon Focus
    cycle = (t % 12.0)
    
    if cycle < 6.0: # Character Phase: IAF Pilot in Cockpit + Radar Alert
        draw_iaf_pilot(ctx, 420, 520, 1.15, t, alert=True, label="WING COMMANDER // COMBAT ALERT")
        
        # Right: Threat Telemetry Box
        rx, ry, rw, rh = 840, 160, 1000, 680
        rrect(ctx, rx, ry, rw, rh, 16)
        rgba(ctx, (0.04, 0.06, 0.10), 0.9)
        ctx.fill()
        rgba(ctx, RED, 0.6)
        ctx.set_line_width(2)
        ctx.stroke()
        
        draw_text(ctx, "EMERGENCY DEFCON 1 // LAC THEATRE", rx + 40, ry + 60, size=28, c=RED, font="Impact", anchor="l")
        line(ctx, [(rx + 40, ry + 90), (rx + rw - 40, ry + 90)], RED, 1.5, 0.4)
        
        draw_text(ctx, "ALERT: 50+ ENEMY STEALTH TARGETS DETECTED", rx + 40, ry + 150, size=24, c=WHITE, font="Impact", anchor="l")
        draw_text(ctx, "VELOCITY: MACH 3.5+ // INCOMING CRUISE MISSILES", rx + 40, ry + 210, size=22, c=AMBER, font="Impact", anchor="l")
        draw_text(ctx, "INTERCEPTION ASSET: S-400 & PROJECT KUSHA ACTIVE", rx + 40, ry + 270, size=22, c=CYAN, font="Impact", anchor="l")
        
        # Dynamic warning pulse banner
        pulse = 0.5 + 0.5 * math.sin(t * 8)
        rrect(ctx, rx + 40, ry + 360, rw - 80, 120, 14)
        rgba(ctx, (0.8 * pulse, 0.1, 0.1), 0.85)
        ctx.fill()
        draw_text(ctx, "PILOT HUD: TARGET LOCK DETECTED", rx + rw / 2, ry + 420, size=32, c=WHITE, font="Impact", anchor="c")
        
    else: # Weapon Phase: Tactical Radar Map
        rcx, rcy, rr = 500, 500, 320
        circle(ctx, rcx, rcy, rr, (0.05, 0.1, 0.15), 0.5, fill=True)
        circle(ctx, rcx, rcy, rr, CYAN, 0.4, fill=False, w=2)
        circle(ctx, rcx, rcy, rr * 0.66, CYAN, 0.25, fill=False, w=1.5)
        
        sweep_ang = (t * 2.5) % (2 * math.pi)
        sx = rcx + rr * math.cos(sweep_ang)
        sy = rcy + rr * math.sin(sweep_ang)
        line(ctx, [(rcx, rcy), (sx, sy)], CYAN, 2.5, 0.9)
        
        for k, (bx, by, lbl) in enumerate([
            (rcx - 120, rcy - 140, "J-20 [STEALTH]"),
            (rcx + 80, rcy - 190, "J-20 [STEALTH]"),
            (rcx - 180, rcy + 40, "HYPERSONIC CRUISE"),
            (rcx + 160, rcy - 70, "SWARM DRONES"),
        ]):
            pulse = 0.5 + 0.5 * math.sin(t * 8 + k)
            circle(ctx, bx, by, 8, RED, 0.9)
            circle(ctx, bx, by, 16 * pulse + 8, RED, 0.4 * (1 - pulse), fill=False, w=2)
            draw_text(ctx, lbl, bx + 18, by, size=16, c=RED, font="Impact", anchor="l")
            
        card_x, card_y, card_w, card_h = 980, 180, 860, 640
        rrect(ctx, card_x, card_y, card_w, card_h, 16)
        rgba(ctx, (0.04, 0.06, 0.1), 0.85)
        ctx.fill()
        rgba(ctx, AMBER, 0.4)
        ctx.set_line_width(2)
        ctx.stroke()
        draw_text(ctx, "TACTICAL SIMULATION: AIR ENGAGEMENT", card_x + 40, card_y + 60, size=28, c=AMBER, font="Impact", anchor="l")
        line(ctx, [(card_x + 40, card_y + 90), (card_x + card_w - 40, card_y + 90)], AMBER, 1.5, 0.4)
        
        draw_text(ctx, "Can our skies hold against 50 stealth jets?", card_x + 40, card_y + 160, size=28, c=WHITE, font="Impact", anchor="l")
        draw_text(ctx, "The answer lies in DRDO's Secret Project Kusha!", card_x + 40, card_y + 220, size=24, c=GOLD, font="Impact", anchor="l")

def draw_scene_2(ctx, t, d):
    # Scene 2: S-400 Russian Titan
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 2, "The Russian Titan: S-400 Triumf in India", t)
    
    cycle = (t % 12.0)
    if cycle < 6.0: # Character Phase: Air Defense Commander at Console
        draw_commander_console(ctx, 420, 520, 1.15, t, alert=False, label="S-400 SQUADRON COMMANDER")
        
        # Right: S-400 Specs
        rx, ry, rw, rh = 840, 160, 1000, 680
        rrect(ctx, rx, ry, rw, rh, 16)
        rgba(ctx, (0.04, 0.06, 0.10), 0.9)
        ctx.fill()
        rgba(ctx, CYAN, 0.4)
        ctx.set_line_width(2)
        ctx.stroke()
        
        draw_text(ctx, "S-400 TRIUMF: 3 SQUADRONS DEPLOYED", rx + 40, ry + 60, size=28, c=CYAN, font="Impact", anchor="l")
        line(ctx, [(rx + 40, ry + 90), (rx + rw - 40, ry + 90)], CYAN, 1.5, 0.4)
        
        draw_text(ctx, "• 91N6E RADAR: 600 KM SURVEILLANCE RANGE", rx + 40, ry + 160, size=24, c=WHITE, font="Impact", anchor="l")
        draw_text(ctx, "• TRACKS 300 TARGETS SIMULTANEOUSLY", rx + 40, ry + 220, size=24, c=WHITE, font="Impact", anchor="l")
        draw_text(ctx, "• 40N6E MISSILE: 400 KM RANGE // MACH 14 SPEED", rx + 40, ry + 280, size=24, c=GOLD, font="Impact", anchor="l")
        draw_text(ctx, "• ENEMY AWACS CANNOT APPROACH INDIAN BORDERS!", rx + 40, ry + 360, size=26, c=GREEN, font="Impact", anchor="l")
    else: # Weapon Phase: S-400 Launcher Vehicle
        lx, ly = 460, 480
        rrect(ctx, 80, 140, 800, 680, 16)
        rgba(ctx, (0.03, 0.05, 0.09), 0.85)
        ctx.fill()
        rgba(ctx, CYAN, 0.3)
        ctx.set_line_width(2)
        ctx.stroke()
        
        draw_text(ctx, "S-400 TRIUMF TEL LAUNCHER", 120, 190, size=28, c=CYAN, font="Impact", anchor="l")
        
        elev = min(math.pi / 2.8, t * 0.15)
        rrect(ctx, lx - 260, ly + 80, 520, 70, 10)
        rgba(ctx, (0.15, 0.2, 0.25), 0.9)
        ctx.fill()
        for wx in [-200, -120, -40, 60, 140, 220]:
            circle(ctx, lx + wx, ly + 155, 30, (0.1, 0.12, 0.15), 1.0)
            circle(ctx, lx + wx, ly + 155, 14, STEEL, 1.0)
            
        ctx.save()
        ctx.translate(lx - 120, ly + 80)
        ctx.rotate(-elev)
        rrect(ctx, 0, -45, 360, 90, 8)
        rgba(ctx, (0.22, 0.28, 0.35), 0.95)
        ctx.fill()
        for ty in [-30, -10, 10, 30]:
            circle(ctx, 360, ty, 10, (0.1, 0.12, 0.15), 1.0)
            circle(ctx, 360, ty, 7, AMBER, 0.8)
        ctx.restore()
        
        # Right info
        rx, rw = 940, 900
        rrect(ctx, rx, 140, rw, 680, 16)
        rgba(ctx, (0.04, 0.06, 0.1), 0.85)
        ctx.fill()
        draw_text(ctx, "PUNJAB, RAJASTHAN & LADAKH AIR BORDERS", rx + 40, 220, size=26, c=GOLD, font="Impact", anchor="l")
        draw_text(ctx, "Total Deal: ₹40,000 Crore with Russia", rx + 40, 280, size=24, c=WHITE, font="Impact", anchor="l")

def draw_scene_3(ctx, t, d):
    # Scene 3: Foreign Supply Risk & J-20
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 3, "Why India Needs Kusha: Supply Crisis & Stealth", t)
    
    cycle = (t % 12.0)
    if cycle < 6.0: # Character Phase: Chinese J-20 Adversary Pilot
        draw_iaf_pilot(ctx, 420, 520, 1.15, t, alert=False, label="CHENGDU J-20 STEALTH PILOT")
        
        rx, ry, rw, rh = 840, 160, 1000, 680
        rrect(ctx, rx, ry, rw, rh, 16)
        rgba(ctx, (0.04, 0.06, 0.10), 0.9)
        ctx.fill()
        rgba(ctx, AMBER, 0.5)
        ctx.set_line_width(2)
        ctx.stroke()
        
        draw_text(ctx, "CHALLENGE: ENEMY 5TH GEN STEALTH FLEET", rx + 40, ry + 60, size=28, c=AMBER, font="Impact", anchor="l")
        line(ctx, [(rx + 40, ry + 90), (rx + rw - 40, ry + 90)], AMBER, 1.5, 0.4)
        
        draw_text(ctx, "• J-20 Radar Cross Section (RCS) is less than 0.01 m²", rx + 40, ry + 160, size=24, c=WHITE, font="Impact", anchor="l")
        draw_text(ctx, "• Traditional PESA radars cannot track stealth at long ranges.", rx + 40, ry + 220, size=24, c=GRAY, font="Impact", anchor="l")
        draw_text(ctx, "• Foreign supply bottleneck during Russia-Ukraine war.", rx + 40, ry + 280, size=24, c=RED, font="Impact", anchor="l")
        draw_text(ctx, "• Bharat needs 100% indigenous defense autonomy!", rx + 40, ry + 360, size=28, c=GOLD, font="Impact", anchor="l")
    else: # Infographic Phase: Foreign Risk Analysis
        rrect(ctx, 80, 140, 840, 680, 16)
        rgba(ctx, (0.04, 0.05, 0.08), 0.88)
        ctx.fill()
        draw_text(ctx, "CRITICAL FOREIGN RISKS", 120, 200, size=28, c=RED, font="Impact", anchor="l")
        draw_text(ctx, "1. Squadron 4 & 5 delivery delays from Russia", 120, 270, size=22, c=WHITE, font="Impact", anchor="l")
        draw_text(ctx, "2. Spare parts cutoff risk during full war escalation", 120, 330, size=22, c=WHITE, font="Impact", anchor="l")
        draw_text(ctx, "3. Remote control must stay in Indian hands!", 120, 390, size=24, c=GOLD, font="Impact", anchor="l")
        
        rx = 980
        rrect(ctx, rx, 140, 860, 680, 16)
        rgba(ctx, (0.04, 0.06, 0.1), 0.88)
        ctx.fill()
        draw_text(ctx, "THE SOLUTION: PROJECT KUSHA", rx + 40, 200, size=28, c=GOLD, font="Impact", anchor="l")
        draw_text(ctx, "Indigenous DRDO Gallium Nitride GaN AESA Radar", rx + 40, 270, size=22, c=CYAN, font="Impact", anchor="l")

def draw_scene_4(ctx, t, d):
    # Scene 4: Project Kusha DRDO
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 4, "Project Kusha: DRDO's Ultra Long-Range Shield", t)
    
    cycle = (t % 12.0)
    if cycle < 6.0: # Character Phase: DRDO Chief Scientist
        draw_drdo_scientist(ctx, 420, 520, 1.15, t, label="PROJECT KUSHA MISSION DIRECTOR")
        
        rx, ry, rw, rh = 840, 160, 1000, 680
        rrect(ctx, rx, ry, rw, rh, 16)
        rgba(ctx, (0.04, 0.06, 0.10), 0.9)
        ctx.fill()
        rgba(ctx, GOLD, 0.5)
        ctx.set_line_width(2)
        ctx.stroke()
        
        draw_text(ctx, "CABINET COMMITTEE ON SECURITY APPROVAL", rx + 40, ry + 60, size=28, c=GOLD, font="Impact", anchor="l")
        line(ctx, [(rx + 40, ry + 90), (rx + rw - 40, ry + 90)], GOLD, 1.5, 0.4)
        
        draw_text(ctx, "BUDGET: ₹21,700 CRORE OFFICIALLY ALLOCATED", rx + 40, ry + 160, size=28, c=WHITE, font="Impact", anchor="l")
        draw_text(ctx, "DEVELOPER: DEFENCE RESEARCH & DEVELOPMENT ORG (DRDO)", rx + 40, ry + 220, size=22, c=CYAN, font="Impact", anchor="l")
        draw_text(ctx, "TEST FACILITY: APJ ABDUL KALAM ISLAND, ODISHA", rx + 40, ry + 280, size=22, c=GREEN, font="Impact", anchor="l")
        draw_text(ctx, "THREE-TIER MOBILE SURFACE-TO-AIR INTERCEPTORS", rx + 40, ry + 360, size=26, c=AMBER, font="Impact", anchor="l")
    else: # 3 Missiles Display Phase
        col_w = 540
        gap = 70
        start_x = 80
        tiers = [
            ("TIER 1 INTERCEPTOR", "150 KM RANGE", "MEDIUM ALTITUDE", CYAN),
            ("TIER 2 INTERCEPTOR", "250 KM RANGE", "DUAL-PULSE MOTOR", AMBER),
            ("TIER 3 HEAVY INTERCEPTOR", "400 KM RANGE", "BALLISTIC HIT-TO-KILL", GOLD),
        ]
        for i, (ttl, rng, tech, clr) in enumerate(tiers):
            cx = start_x + i * (col_w + gap)
            cy = 180
            ch = 640
            rrect(ctx, cx, cy, col_w, ch, 14)
            rgba(ctx, (0.04, 0.06, 0.1), 0.85)
            ctx.fill()
            rgba(ctx, clr, 0.4)
            ctx.set_line_width(2)
            ctx.stroke()
            draw_text(ctx, ttl, cx + col_w / 2, cy + 45, size=24, c=clr, font="Impact", anchor="c")
            draw_text(ctx, rng, cx + col_w / 2, cy + 95, size=32, c=WHITE, font="Impact", anchor="c")
            draw_text(ctx, tech, cx + col_w / 2, cy + 480, size=22, c=clr, font="Impact", anchor="c")

def draw_scene_5(ctx, t, d):
    # Scene 5: Tech Duel (GaN AESA & Hit-to-Kill)
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 5, "Tech Duel: S-400 vs Project Kusha", t)
    
    cycle = (t % 12.0)
    if cycle < 6.0: # Character Phase: Missile Operator slamming Launch
        draw_missile_soldier(ctx, 420, 520, 1.15, t, action="launch", label="AIR DEFENSE LAUNCH OPERATOR")
        
        rx, ry, rw, rh = 840, 160, 1000, 680
        rrect(ctx, rx, ry, rw, rh, 16)
        rgba(ctx, (0.04, 0.06, 0.10), 0.9)
        ctx.fill()
        rgba(ctx, GOLD, 0.5)
        ctx.set_line_width(2)
        ctx.stroke()
        
        draw_text(ctx, "HIT-TO-KILL KINETIC DESTRUCTION", rx + 40, ry + 60, size=28, c=GOLD, font="Impact", anchor="l")
        line(ctx, [(rx + 40, ry + 90), (rx + rw - 40, ry + 90)], GOLD, 1.5, 0.4)
        
        draw_text(ctx, "• S-400 uses Proximity Fragmentation (shrapnel blast).", rx + 40, ry + 160, size=22, c=GRAY, font="Impact", anchor="l")
        draw_text(ctx, "• Project Kusha uses Direct Kinetic Hit-to-Kill (bullet hitting bullet).", rx + 40, ry + 220, size=24, c=WHITE, font="Impact", anchor="l")
        draw_text(ctx, "• 100% kinetic energy release instantly vaporizes incoming warhead!", rx + 40, ry + 280, size=24, c=GOLD, font="Impact", anchor="l")
        draw_text(ctx, "• GaN AESA Radar micro-beams penetrate J-20 stealth coating.", rx + 40, ry + 360, size=24, c=CYAN, font="Impact", anchor="l")
    else: # Tech Duel Comparison Cards
        rrect(ctx, 80, 140, 840, 680, 16)
        rgba(ctx, (0.04, 0.06, 0.1), 0.85)
        ctx.fill()
        draw_text(ctx, "S-400 (RUSSIA)", 120, 190, size=28, c=AMBER, font="Impact", anchor="l")
        draw_text(ctx, "• PESA Radar (Passive Array)", 120, 260, size=24, c=WHITE, font="Impact", anchor="l")
        draw_text(ctx, "• Proximity Fragmentation Shrapnel", 120, 320, size=24, c=WHITE, font="Impact", anchor="l")
        
        rx = 980
        rrect(ctx, rx, 140, 860, 680, 16)
        rgba(ctx, (0.03, 0.09, 0.06), 0.85)
        ctx.fill()
        draw_text(ctx, "PROJECT KUSHA (BHARAT)", rx + 40, 190, size=28, c=GREEN, font="Impact", anchor="l")
        draw_text(ctx, "• GaN AESA (3X Power Density, Stealth Killer)", rx + 40, 260, size=24, c=GOLD, font="Impact", anchor="l")
        draw_text(ctx, "• Hit-to-Kill Kinetic Interception (Mach 15+)", rx + 40, 320, size=24, c=GOLD, font="Impact", anchor="l")

def draw_scene_6(ctx, t, d):
    # Scene 6: IACCS & 5-Layer Shield (Layers 1-3)
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 6, "Bharat's 5-Layer Iron Dome: The Outer Citadel", t)
    
    cycle = (t % 12.0)
    if cycle < 6.0: # Character Phase: Air Defense Commander coordinating IACCS
        draw_commander_console(ctx, 420, 520, 1.15, t, alert=False, label="IACCS JOINT AIR COMMAND")
        
        rx, ry, rw, rh = 840, 160, 1000, 680
        rrect(ctx, rx, ry, rw, rh, 16)
        rgba(ctx, (0.04, 0.06, 0.10), 0.9)
        ctx.fill()
        rgba(ctx, CYAN, 0.4)
        ctx.set_line_width(2)
        ctx.stroke()
        
        draw_text(ctx, "IACCS: INTEGRATED COMMAND NETWORK", rx + 40, ry + 60, size=28, c=CYAN, font="Impact", anchor="l")
        line(ctx, [(rx + 40, ry + 90), (rx + rw - 40, ry + 90)], CYAN, 1.5, 0.4)
        
        draw_text(ctx, "• Netra AWACS + INS Vikrant + Ground Mountain Radars", rx + 40, ry + 160, size=22, c=WHITE, font="Impact", anchor="l")
        draw_text(ctx, "• All data feeds into Kusha launch computer in real-time.", rx + 40, ry + 220, size=22, c=WHITE, font="Impact", anchor="l")
        draw_text(ctx, "• LAYER 1: Project Kusha & S-400 (400 KM)", rx + 40, ry + 290, size=26, c=GOLD, font="Impact", anchor="l")
        draw_text(ctx, "• LAYER 2: MRSAM Barak-8 (70 - 100 KM)", rx + 40, ry + 350, size=24, c=CYAN, font="Impact", anchor="l")
        draw_text(ctx, "• LAYER 3: Akash Prime & Akash-NG (30 - 45 KM)", rx + 40, ry + 410, size=24, c=GREEN, font="Impact", anchor="l")
    else: # Tactical 3-Layer Display
        rrect(ctx, 80, 140, W - 160, 680, 16)
        rgba(ctx, (0.04, 0.06, 0.1), 0.85)
        ctx.fill()
        draw_text(ctx, "BHARAT'S 5-LAYER AIR DEFENSE: OUTER LAYERS", 120, 200, size=32, c=GOLD, font="Impact", anchor="l")
        draw_text(ctx, "Layer 1: Project Kusha & S-400 (350 - 400 KM Outer Citadel)", 120, 280, size=26, c=GOLD, font="Impact", anchor="l")
        draw_text(ctx, "Layer 2: MRSAM Barak-8 (70 - 100 KM Extended Shield)", 120, 360, size=26, c=CYAN, font="Impact", anchor="l")
        draw_text(ctx, "Layer 3: Akash Prime & Akash-NG (30 - 45 KM The Workhorse)", 120, 440, size=26, c=GREEN, font="Impact", anchor="l")

def draw_scene_7(ctx, t, d):
    # Scene 7: Point Defense & Terminal Iron Fist (Layers 4 & 5)
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 7, "Layers 4 & 5: Point Defense & Terminal Iron Fist", t)
    
    cycle = (t % 12.0)
    if cycle < 6.0: # Character Phase: Jawan in Combat Gear
        draw_missile_soldier(ctx, 420, 520, 1.15, t, action="salute", label="POINT DEFENSE CREW")
        
        rx, ry, rw, rh = 840, 160, 1000, 680
        rrect(ctx, rx, ry, rw, rh, 16)
        rgba(ctx, (0.04, 0.06, 0.10), 0.9)
        ctx.fill()
        rgba(ctx, GREEN, 0.4)
        ctx.set_line_width(2)
        ctx.stroke()
        
        draw_text(ctx, "POINT DEFENSE & TERMINAL SHIELD", rx + 40, ry + 60, size=28, c=GREEN, font="Impact", anchor="l")
        line(ctx, [(rx + 40, ry + 90), (rx + rw - 40, ry + 90)], GREEN, 1.5, 0.4)
        
        draw_text(ctx, "• LAYER 4: QRSAM (15 - 30 KM) Mobile Armor Umbrella", rx + 40, ry + 160, size=24, c=AMBER, font="Impact", anchor="l")
        draw_text(ctx, "• Protects moving tank columns with < 6 second reaction time.", rx + 40, ry + 220, size=22, c=WHITE, font="Impact", anchor="l")
        draw_text(ctx, "• LAYER 5: VSHORADS & Auto-Cannons (0 - 6 KM)", rx + 40, ry + 300, size=24, c=RED, font="Impact", anchor="l")
        draw_text(ctx, "• Directed Energy Lasers vaporize kamikaze drone swarms!", rx + 40, ry + 360, size=24, c=GOLD, font="Impact", anchor="l")
    else: # Concentric 5-Layer Dome Graphic
        rx = 400
        rw = 1120
        rrect(ctx, rx, 140, rw, 680, 16)
        rgba(ctx, (0.04, 0.06, 0.1), 0.85)
        ctx.fill()
        draw_text(ctx, "COMPLETE 5-LAYER AIR DEFENSE UMBRELLA OVER INDIA", W / 2, 200, size=28, c=CYAN, font="Impact", anchor="c")
        dcx, dcy = W / 2, 700
        domes = [
            (320, GOLD, "L1: KUSHA (400 KM)"),
            (240, CYAN, "L2: MRSAM (100 KM)"),
            (170, GREEN, "L3: AKASH (45 KM)"),
            (110, AMBER, "L4: QRSAM (30 KM)"),
            (50, RED, "L5: VSHORADS (6 KM)"),
        ]
        for r_dome, c_dome, lbl in domes:
            ctx.arc(dcx, dcy, r_dome, math.pi, 2 * math.pi)
            rgba(ctx, c_dome, 0.1)
            ctx.fill()
            ctx.arc(dcx, dcy, r_dome, math.pi, 2 * math.pi)
            rgba(ctx, c_dome, 0.7)
            ctx.set_line_width(2)
            ctx.stroke()
            draw_text(ctx, lbl, dcx, dcy - r_dome + 16, size=14, c=c_dome, font="Impact", anchor="c")

def draw_scene_8(ctx, t, d):
    # Scene 8: Strategic Sovereignty & Outro
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 8, "Strategic Sovereignty: The Road to 2028", t)
    
    cycle = (t % 12.0)
    if cycle < 6.0: # Character Phase: Saluting Soldier with Tricolor
        draw_missile_soldier(ctx, 420, 520, 1.15, t, action="salute", label="BHARAT KA VEER JAWAN")
        
        rx, ry, rw, rh = 840, 160, 1000, 680
        rrect(ctx, rx, ry, rw, rh, 16)
        rgba(ctx, (0.04, 0.06, 0.10), 0.9)
        ctx.fill()
        rgba(ctx, GOLD, 0.5)
        ctx.set_line_width(2)
        ctx.stroke()
        
        draw_text(ctx, "ATMANIRBHAR BHARAT: AIR SUPREMACY", rx + 40, ry + 60, size=28, c=GOLD, font="Impact", anchor="l")
        line(ctx, [(rx + 40, ry + 90), (rx + rw - 40, ry + 90)], GOLD, 1.5, 0.4)
        
        draw_text(ctx, "• 2028: Project Kusha enters full operational service.", rx + 40, ry + 160, size=24, c=WHITE, font="Impact", anchor="l")
        draw_text(ctx, "• The keys to Indian airspace belong solely to India!", rx + 40, ry + 220, size=24, c=GOLD, font="Impact", anchor="l")
        draw_text(ctx, "• Comment below: Should India invest 100% in Kusha?", rx + 40, ry + 300, size=24, c=CYAN, font="Impact", anchor="l")
        draw_text(ctx, "• Subscribe to RealityShift // Jai Hind, Vande Mataram!", rx + 40, ry + 380, size=26, c=SAFFRON, font="Impact", anchor="l")
    else: # Community Poll Card
        rrect(ctx, 160, 180, W - 320, 620, 16)
        rgba(ctx, (0.04, 0.07, 0.12), 0.9)
        ctx.fill()
        rgba(ctx, AMBER, 0.5)
        ctx.set_line_width(2.5)
        ctx.stroke()
        
        draw_text(ctx, "THE STRATEGIC QUESTION FOR YOU:", W / 2, 250, size=32, c=AMBER, font="Impact", anchor="c")
        draw_text(ctx, "Kya Bharat ko foreign weapons lene chahiye ya 100% Project Kusha par focus karna chahiye?", W / 2, 320, size=24, c=WHITE, font="Impact", anchor="c")
        
        rrect(ctx, 240, 400, 680, 120, 12)
        rgba(ctx, (0.06, 0.09, 0.15), 0.85)
        ctx.fill()
        draw_text(ctx, "[ OPTION A ]", 280, 435, size=22, c=CYAN, font="Impact", anchor="l")
        draw_text(ctx, "Buy more foreign systems for immediate cover.", 280, 475, size=18, c=GRAY, font="Impact", anchor="l")
        
        rrect(ctx, 1000, 400, 680, 120, 12)
        rgba(ctx, (0.04, 0.12, 0.08), 0.85)
        ctx.fill()
        draw_text(ctx, "[ OPTION B ]", 1040, 435, size=22, c=GREEN, font="Impact", anchor="l")
        draw_text(ctx, "100% focus on Project Kusha indigenous shield!", 1040, 475, size=18, c=WHITE, font="Impact", anchor="l")

SCENE_DRAWERS = [
    draw_scene_1,
    draw_scene_2,
    draw_scene_3,
    draw_scene_4,
    draw_scene_5,
    draw_scene_6,
    draw_scene_7,
    draw_scene_8,
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
    
    # Subtitle cues from ROMAN_SCRIPTS
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
        drawer = SCENE_DRAWERS[sc["index"]]
        
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
