"""Project Kusha vs S-400: Inside India's Ultra Long-Range Air Defense Shield
Full Long-Form 16:9 (1920x1080) Widescreen Documentary Renderer for RealityShift.
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

ROOT = Path(__file__).resolve().parent
WORK_DIR = ROOT / "output" / "work" / "project_kusha" / "files"
OUT_DIR = ROOT / "output" / "documentary"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Helper functions
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
    
    # Subtle moving radar / telemetry grid
    ctx.set_line_width(1)
    for x in range(0, W, 80):
        alpha = 0.08 if x % 240 == 0 else 0.03
        line(ctx, [(x, 0), (x, H)], BG_GRID, 1, alpha)
    for y in range(0, H, 80):
        alpha = 0.08 if y % 240 == 0 else 0.03
        line(ctx, [(0, y), (W, y)], BG_GRID, 1, alpha)
        
    # Vignette
    vg = cairo.RadialGradient(W / 2, H / 2, 400, W / 2, H / 2, 1100)
    vg.add_color_stop_rgba(0, 0, 0, 0, 0.0)
    vg.add_color_stop_rgba(1, 0, 0, 0, 0.65)
    ctx.set_source(vg)
    ctx.paint()

def draw_hud_header(ctx, chapter_num, chapter_title, t):
    # Top bar background
    rrect(ctx, 40, 24, W - 80, 56, 8)
    rgba(ctx, (0.05, 0.07, 0.12), 0.85)
    ctx.fill()
    rrect(ctx, 40, 24, W - 80, 56, 8)
    rgba(ctx, CYAN, 0.35)
    ctx.set_line_width(1.5)
    ctx.stroke()
    
    # Left channel tag
    draw_text(ctx, "REALITY SHIFT // STRATEGIC DEFENSE REPORT", 70, 52, size=18, c=CYAN, font="Impact", anchor="l")
    
    # Center Chapter title
    title_str = f"CHAPTER 0{chapter_num}: {chapter_title.upper()}"
    draw_text(ctx, title_str, W / 2, 52, size=20, c=GOLD, font="Impact", anchor="c")
    
    # Right telemetry tag
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
    rgba(ctx, CYAN, 0.35)
    ctx.set_line_width(1.5)
    ctx.stroke()
    
    # Text with shadow
    draw_text(ctx, sub_text, W / 2 + 2, py + 2, size=36, c=(0, 0, 0), font="Impact", anchor="c")
    draw_text(ctx, sub_text, W / 2, py, size=36, c=WHITE, font="Impact", anchor="c")

# Scene drawing routines
def draw_scene_1(ctx, t, d):
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 1, "The 50-Stealth Threat at LAC", t)
    
    rcx, rcy, rr = 500, 500, 320
    circle(ctx, rcx, rcy, rr, (0.05, 0.1, 0.15), 0.5, fill=True)
    circle(ctx, rcx, rcy, rr, CYAN, 0.4, fill=False, w=2)
    circle(ctx, rcx, rcy, rr * 0.66, CYAN, 0.25, fill=False, w=1.5)
    circle(ctx, rcx, rcy, rr * 0.33, CYAN, 0.2, fill=False, w=1)
    
    sweep_ang = (t * 2.5) % (2 * math.pi)
    sx = rcx + rr * math.cos(sweep_ang)
    sy = rcy + rr * math.sin(sweep_ang)
    line(ctx, [(rcx, rcy), (sx, sy)], CYAN, 2.5, 0.9)
    
    for k, (bx, by, lbl) in enumerate([
        (rcx - 120, rcy - 140, "J-20 [STEALTH]"),
        (rcx + 80, rcy - 190, "J-20 [STEALTH]"),
        (rcx - 180, rcy + 40, "HYPERSONIC CRUISE"),
        (rcx + 160, rcy - 70, "SWARM DRONES"),
        (rcx - 50, rcy - 230, "BALLISTIC ASM")
    ]):
        pulse = 0.5 + 0.5 * math.sin(t * 8 + k)
        circle(ctx, bx, by, 7, RED, 0.9)
        circle(ctx, bx, by, 14 * pulse + 7, RED, 0.4 * (1 - pulse), fill=False, w=2)
        draw_text(ctx, lbl, bx + 16, by, size=16, c=RED, font="Impact", anchor="l")
        
    card_x, card_y, card_w, card_h = 980, 220, 860, 580
    rrect(ctx, card_x, card_y, card_w, card_h, 16)
    rgba(ctx, (0.04, 0.06, 0.1), 0.85)
    ctx.fill()
    rrect(ctx, card_x, card_y, card_w, card_h, 16)
    rgba(ctx, AMBER, 0.4)
    ctx.set_line_width(2)
    ctx.stroke()
    
    draw_text(ctx, "TACTICAL SIMULATION: LAC THEATRE ATTACK", card_x + 40, card_y + 60, size=28, c=AMBER, font="Impact", anchor="l")
    line(ctx, [(card_x + 40, card_y + 90), (card_x + card_w - 40, card_y + 90)], AMBER, 1.5, 0.4)
    
    threats = [
        ("INCOMING THREATS", "50+ STEALTH FIGHTERS & CRUISE MISSILES", RED),
        ("ENEMY FLIGHT VELOCITY", "MACH 3.2 TO MACH 6.0", WHITE),
        ("ENGAGEMENT WINDOW", "< 180 SECONDS TO TARGET", AMBER),
        ("AIR DEFENSE ASSET", "S-400 TRIUMF + PROJECT KUSHA", CYAN),
        ("STATUS", "ULTRA LONG-RANGE INTERCEPTION ACTIVE", GREEN),
    ]
    for i, (k_lbl, v_lbl, clr) in enumerate(threats):
        ty = card_y + 150 + i * 80
        draw_text(ctx, k_lbl, card_x + 40, ty, size=20, c=GRAY, font="Impact", anchor="l")
        draw_text(ctx, v_lbl, card_x + 40, ty + 30, size=24, c=clr, font="Impact", anchor="l")
        
    if t > 18.0:
        pop = ease_out_cubic(clamp((t - 18.0) / 0.8))
        ctx.save()
        ctx.translate(W / 2, 780)
        ctx.scale(pop, pop)
        rrect(ctx, -500, -50, 1000, 100, 14)
        rgba(ctx, (0.05, 0.08, 0.15), 0.95)
        ctx.fill()
        rrect(ctx, -500, -50, 1000, 100, 14)
        rgba(ctx, GOLD, 0.8)
        ctx.set_line_width(2.5)
        ctx.stroke()
        draw_text(ctx, "PROJECT KUSHA: INDIA'S INDIGENOUS IRON DOME", 0, 0, size=38, c=GOLD, font="Impact", anchor="c")
        ctx.restore()

def draw_scene_2(ctx, t, d):
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 2, "The Russian Titan: S-400 Triumf in India", t)
    
    lx, ly = 460, 480
    rrect(ctx, 80, 140, 800, 680, 16)
    rgba(ctx, (0.03, 0.05, 0.09), 0.85)
    ctx.fill()
    rrect(ctx, 80, 140, 800, 680, 16)
    rgba(ctx, CYAN, 0.3)
    ctx.set_line_width(2)
    ctx.stroke()
    
    draw_text(ctx, "S-400 TRIUMF (SA-21 GROWLER)", 120, 190, size=28, c=CYAN, font="Impact", anchor="l")
    draw_text(ctx, "3 OF 5 SQUADRONS DELIVERED // LAC & WESTERN FRONTIER", 120, 226, size=18, c=GRAY, font="Impact", anchor="l")
    
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
    
    rx, rw = 940, 900
    rrect(ctx, rx, 140, rw, 680, 16)
    rgba(ctx, (0.04, 0.06, 0.1), 0.85)
    ctx.fill()
    rrect(ctx, rx, 140, rw, 680, 16)
    rgba(ctx, AMBER, 0.3)
    ctx.set_line_width(2)
    ctx.stroke()
    
    draw_text(ctx, "S-400 LAYERED MISSILE ARSENAL", rx + 40, 190, size=28, c=AMBER, font="Impact", anchor="l")
    
    specs = [
        ("91N6E BIG BIRD RADAR", "600 KM SURVEILLANCE // 300 TARGET TRACKING", CYAN),
        ("40N6E ULTRA LONG-RANGE", "RANGE: 400 KM // SPEED: MACH 14+ HYPERSONIC", GOLD),
        ("48N6DM HEAVY INTERCEPTOR", "RANGE: 250 KM // WARHEAD: 180 KG PROXIMITY", WHITE),
        ("9M96E2 MEDIUM-RANGE", "RANGE: 120 KM // ACTIVE RADAR HOMING", STEEL),
        ("DEPLOYMENT IN INDIA", "PUNJAB, RAJASTHAN & LADAKH AIR BORDER", GREEN),
    ]
    for i, (ttl, sub, clr) in enumerate(specs):
        sy = 260 + i * 105
        rrect(ctx, rx + 40, sy - 15, rw - 80, 85, 10)
        rgba(ctx, (0.06, 0.09, 0.14), 0.7)
        ctx.fill()
        rrect(ctx, rx + 40, sy - 15, rw - 80, 85, 10)
        rgba(ctx, clr, 0.25)
        ctx.set_line_width(1)
        ctx.stroke()
        draw_text(ctx, ttl, rx + 65, sy + 15, size=22, c=clr, font="Impact", anchor="l")
        draw_text(ctx, sub, rx + 65, sy + 45, size=18, c=GRAY, font="Impact", anchor="l")

def draw_scene_3(ctx, t, d):
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 3, "Why India Needs Kusha: Supply Crisis & Stealth", t)
    
    rrect(ctx, 80, 140, 840, 680, 16)
    rgba(ctx, (0.04, 0.05, 0.08), 0.88)
    ctx.fill()
    rrect(ctx, 80, 140, 840, 680, 16)
    rgba(ctx, RED, 0.4)
    ctx.set_line_width(2)
    ctx.stroke()
    
    draw_text(ctx, "CRITICAL RISK: FOREIGN DEPENDENCY", 120, 200, size=26, c=RED, font="Impact", anchor="l")
    
    risks = [
        ("RUSSIA-UKRAINE CONFLICT", "DELAYS IN SQUADRON 4 & 5 DELIVERY TIMELINE"),
        ("WARTIME SPARE PARTS", "FOREIGN SUPPLY CUTOFF RISK DURING FULL ESCALATION"),
        ("MISSILE EXPENDITURE DEPLETION", "CANNOT QUICKLY RE-SUPPLY INTERCEPTORS FROM ABROAD"),
        ("NETWORK INTEGRATION LIMITS", "DIFFICULTY LINKING RUSSIAN CODE WITH INDIAN SATNET"),
    ]
    for i, (h_txt, b_txt) in enumerate(risks):
        py = 280 + i * 120
        rrect(ctx, 120, py, 760, 95, 10)
        rgba(ctx, (0.08, 0.03, 0.03), 0.6)
        ctx.fill()
        draw_text(ctx, f"0{i+1}. {h_txt}", 145, py + 32, size=20, c=RED, font="Impact", anchor="l")
        draw_text(ctx, b_txt, 145, py + 65, size=16, c=WHITE, font="Impact", anchor="l")
        
    rx = 980
    rrect(ctx, rx, 140, 860, 680, 16)
    rgba(ctx, (0.04, 0.06, 0.1), 0.88)
    ctx.fill()
    rrect(ctx, rx, 140, 860, 680, 16)
    rgba(ctx, AMBER, 0.4)
    ctx.set_line_width(2)
    ctx.stroke()
    
    draw_text(ctx, "THE STEALTH PARADOX: CHENGDU J-20", rx + 40, 200, size=26, c=AMBER, font="Impact", anchor="l")
    
    jx, jy = rx + 430, 420
    line(ctx, [(jx, jy - 140), (jx - 160, jy + 110), (jx - 60, jy + 80), (jx, jy + 120), (jx + 60, jy + 80), (jx + 160, jy + 110), (jx, jy - 140)], STEEL, 3, 0.9)
    
    for ang_deg in [-50, -25, 0, 25, 50]:
        ang = math.radians(ang_deg)
        r_wave = 180 + 30 * math.sin(t * 5 + ang_deg)
        wx = jx + r_wave * math.sin(ang)
        wy = jy - 140 - r_wave * math.cos(ang)
        circle(ctx, wx, wy, 4, CYAN, 0.6)
        
    draw_text(ctx, "RADAR CROSS SECTION (RCS): ~0.01 m²", rx + 430, 600, size=22, c=CYAN, font="Impact", anchor="c")
    draw_text(ctx, "TRADITIONAL PESA RADARS STRUGGLE AT EXTREME RANGES", rx + 430, 640, size=18, c=GRAY, font="Impact", anchor="c")
    draw_text(ctx, "SOLUTION: BHARAT'S INDIGENOUS GaN AESA SHIELD", rx + 430, 710, size=24, c=GOLD, font="Impact", anchor="c")

def draw_scene_4(ctx, t, d):
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 4, "Project Kusha: DRDO's Ultra Long-Range Shield", t)
    
    rrect(ctx, 80, 130, W - 160, 90, 14)
    rgba(ctx, (0.05, 0.08, 0.15), 0.9)
    ctx.fill()
    rrect(ctx, 80, 130, W - 160, 90, 14)
    rgba(ctx, GOLD, 0.5)
    ctx.set_line_width(2)
    ctx.stroke()
    
    draw_text(ctx, "MOD OFFICIAL APPROVAL: ₹21,700 CRORE BUDGET", 120, 175, size=28, c=GOLD, font="Impact", anchor="l")
    draw_text(ctx, "DEVELOPED BY DRDO // THREE-TIER LONG-RANGE SAM SYSTEM", W - 120, 175, size=20, c=CYAN, font="Impact", anchor="r")
    
    col_w = 540
    gap = 70
    start_x = 80
    
    tiers = [
        ("TIER 1 INTERCEPTOR", "150 KM RANGE", "MEDIUM TO HIGH ALTITUDE", "Quick-reaction aerodynamic thrust vectoring for maneuvering jets & cruise missiles.", CYAN),
        ("TIER 2 INTERCEPTOR", "250 KM RANGE", "DUAL-PULSE MOTOR", "Extended-range interception against standoff bombers, AWACS & electronic jammer planes.", AMBER),
        ("TIER 3 HEAVY INTERCEPTOR", "350 - 400 KM RANGE", "BALLISTIC & HYPERSONIC KILL", "Kinetic hit-to-kill vehicle targeting ballistic missiles, satellites & hypersonic weapons.", GOLD),
    ]
    
    for i, (ttl, rng, tech, desc, clr) in enumerate(tiers):
        cx = start_x + i * (col_w + gap)
        cy = 260
        ch = 560
        rrect(ctx, cx, cy, col_w, ch, 14)
        rgba(ctx, (0.04, 0.06, 0.1), 0.85)
        ctx.fill()
        rrect(ctx, cx, cy, col_w, ch, 14)
        rgba(ctx, clr, 0.4)
        ctx.set_line_width(2)
        ctx.stroke()
        
        draw_text(ctx, ttl, cx + col_w / 2, cy + 45, size=24, c=clr, font="Impact", anchor="c")
        draw_text(ctx, rng, cx + col_w / 2, cy + 85, size=32, c=WHITE, font="Impact", anchor="c")
        line(ctx, [(cx + 40, cy + 120), (cx + col_w - 40, cy + 120)], clr, 1, 0.3)
        
        mx, my = cx + col_w / 2, cy + 260
        m_len = 160 + i * 40
        rrect(ctx, mx - 12, my - m_len / 2, 24, m_len, 6)
        rgba(ctx, STEEL, 0.95)
        ctx.fill()
        line(ctx, [(mx - 12, my - m_len / 2), (mx, my - m_len / 2 - 25), (mx + 12, my - m_len / 2)], clr, 2)
        ctx.set_source_rgb(*clr)
        ctx.fill()
        line(ctx, [(mx - 12, my + m_len / 2 - 30), (mx - 32, my + m_len / 2 + 10)], clr, 3)
        line(ctx, [(mx + 12, my + m_len / 2 - 30), (mx + 32, my + m_len / 2 + 10)], clr, 3)
        
        draw_text(ctx, tech, cx + col_w / 2, cy + 430, size=20, c=clr, font="Impact", anchor="c")
        draw_text(ctx, desc[:36], cx + col_w / 2, cy + 480, size=16, c=GRAY, font="Impact", anchor="c")
        draw_text(ctx, desc[36:], cx + col_w / 2, cy + 510, size=16, c=GRAY, font="Impact", anchor="c")

def draw_scene_5(ctx, t, d):
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 5, "Tech Duel: S-400 vs Project Kusha", t)
    
    rrect(ctx, 80, 130, W - 160, 320, 16)
    rgba(ctx, (0.04, 0.06, 0.1), 0.85)
    ctx.fill()
    rrect(ctx, 80, 130, W - 160, 320, 16)
    rgba(ctx, CYAN, 0.3)
    ctx.set_line_width(2)
    ctx.stroke()
    
    draw_text(ctx, "RADAR TECHNOLOGY DUEL: PESA vs GaN AESA", 120, 175, size=26, c=CYAN, font="Impact", anchor="l")
    
    rrect(ctx, 120, 210, 800, 210, 10)
    rgba(ctx, (0.06, 0.08, 0.12), 0.7)
    ctx.fill()
    draw_text(ctx, "S-400: PESA (PASSIVE ELECTRONIC SCAN)", 150, 245, size=22, c=AMBER, font="Impact", anchor="l")
    draw_text(ctx, "• Single high-power transmitter tube feeding passive array.", 150, 285, size=18, c=GRAY, font="Impact", anchor="l")
    draw_text(ctx, "• Vulnerable if central transmitter is jammed or damaged.", 150, 325, size=18, c=GRAY, font="Impact", anchor="l")
    draw_text(ctx, "• Reduced detection range against low RCS stealth (J-20).", 150, 365, size=18, c=RED, font="Impact", anchor="l")
    
    rrect(ctx, 980, 210, 820, 210, 10)
    rgba(ctx, (0.03, 0.1, 0.08), 0.7)
    ctx.fill()
    draw_text(ctx, "PROJECT KUSHA: GaN AESA (GALLIUM NITRIDE)", 1010, 245, size=22, c=GREEN, font="Impact", anchor="l")
    draw_text(ctx, "• Thousands of independent Transmit/Receive modules.", 1010, 285, size=18, c=WHITE, font="Impact", anchor="l")
    draw_text(ctx, "• 3X higher power density & extreme electronic counter-countermeasures.", 1010, 325, size=18, c=WHITE, font="Impact", anchor="l")
    draw_text(ctx, "• Micro-beams burn through stealth coating to lock targets.", 1010, 365, size=18, c=GOLD, font="Impact", anchor="l")
    
    rrect(ctx, 80, 480, W - 160, 340, 16)
    rgba(ctx, (0.04, 0.06, 0.1), 0.85)
    ctx.fill()
    rrect(ctx, 80, 480, W - 160, 340, 16)
    rgba(ctx, GOLD, 0.3)
    ctx.set_line_width(2)
    ctx.stroke()
    
    draw_text(ctx, "LETHALITY MECHANISM: PROXIMITY FRAGMENTATION vs HIT-TO-KILL", 120, 525, size=26, c=GOLD, font="Impact", anchor="l")
    
    rrect(ctx, 120, 560, 800, 230, 10)
    rgba(ctx, (0.06, 0.08, 0.12), 0.7)
    ctx.fill()
    draw_text(ctx, "S-400: PROXIMITY FRAGMENTATION BLAST", 150, 595, size=22, c=AMBER, font="Impact", anchor="l")
    draw_text(ctx, "• Missile detonates near target showering shrapnel.", 150, 635, size=18, c=GRAY, font="Impact", anchor="l")
    draw_text(ctx, "• Effective for aircraft, but hypersonic warhead may survive.", 150, 675, size=18, c=GRAY, font="Impact", anchor="l")
    draw_text(ctx, "• Shrapnel cloud spreads energy over wide area.", 150, 715, size=18, c=WHITE, font="Impact", anchor="l")
    
    rrect(ctx, 980, 560, 820, 230, 10)
    rgba(ctx, (0.03, 0.1, 0.08), 0.7)
    ctx.fill()
    draw_text(ctx, "PROJECT KUSHA: KINETIC HIT-TO-KILL (KKV)", 1010, 595, size=22, c=GOLD, font="Impact", anchor="l")
    draw_text(ctx, "• Bullet-on-bullet physical impact at combined Mach 15+.", 1010, 635, size=18, c=WHITE, font="Impact", anchor="l")
    draw_text(ctx, "• 100% kinetic energy transfer instantly vaporizes target.", 1010, 675, size=18, c=GOLD, font="Impact", anchor="l")
    draw_text(ctx, "• Total destruction of nuclear / hypersonic glide warheads.", 1010, 715, size=18, c=GREEN, font="Impact", anchor="l")

def draw_scene_6(ctx, t, d):
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 6, "Bharat's 5-Layer Iron Dome: The Outer Citadel", t)
    
    rrect(ctx, 80, 130, 760, 690, 16)
    rgba(ctx, (0.04, 0.06, 0.1), 0.85)
    ctx.fill()
    rrect(ctx, 80, 130, 760, 690, 16)
    rgba(ctx, CYAN, 0.35)
    ctx.set_line_width(2)
    ctx.stroke()
    
    draw_text(ctx, "IACCS: UNIFIED AIR DEFENSE BRAIN", 120, 180, size=26, c=CYAN, font="Impact", anchor="l")
    
    hub_x, hub_y = 460, 460
    circle(ctx, hub_x, hub_y, 70, (0.08, 0.15, 0.25), 1.0)
    circle(ctx, hub_x, hub_y, 70, CYAN, 0.8, fill=False, w=2.5)
    draw_text(ctx, "IACCS", hub_x, hub_y - 10, size=24, c=WHITE, font="Impact", anchor="c")
    draw_text(ctx, "NETWORK", hub_x, hub_y + 18, size=16, c=CYAN, font="Impact", anchor="c")
    
    nodes = [
        (hub_x - 220, hub_y - 180, "NETRA AWACS", "AIRBORNE RADAR"),
        (hub_x + 220, hub_y - 180, "INS VIKRANT", "NAVAL SENSORS"),
        (hub_x - 220, hub_y + 180, "MOUNTAIN RADARS", "HIMALAYAN SENSORS"),
        (hub_x + 220, hub_y + 180, "GSAT SATELLITES", "SPACE TRACKING"),
    ]
    for nx, ny, n_ttl, n_sub in nodes:
        line(ctx, [(hub_x, hub_y), (nx, ny)], CYAN, 2, 0.4, dash=[8, 8])
        circle(ctx, nx, ny, 50, (0.06, 0.09, 0.15), 1.0)
        circle(ctx, nx, ny, 50, GOLD, 0.6, fill=False, w=1.5)
        draw_text(ctx, n_ttl, nx, ny - 6, size=15, c=WHITE, font="Impact", anchor="c")
        draw_text(ctx, n_sub, nx, ny + 14, size=12, c=GRAY, font="Impact", anchor="c")
        
    rx, rw = 880, 960
    rrect(ctx, rx, 130, rw, 690, 16)
    rgba(ctx, (0.04, 0.06, 0.1), 0.85)
    ctx.fill()
    rrect(ctx, rx, 130, rw, 690, 16)
    rgba(ctx, GOLD, 0.35)
    ctx.set_line_width(2)
    ctx.stroke()
    
    draw_text(ctx, "THE 5-LAYER SHIELD: OUTER CITADEL LAYERS", rx + 40, 180, size=26, c=GOLD, font="Impact", anchor="l")
    
    l_layers = [
        ("LAYER 1: OUTER CITADEL (350 - 400 KM)", "PROJECT KUSHA & S-400 TRIUMF", "Longest range defense against strategic bombers, AWACS & ballistic missiles.", GOLD),
        ("LAYER 2: EXTENDED SHIELD (70 - 100 KM)", "MRSAM (BARAK-8 JOINT SYSTEM)", "Active radar seeker, 360° coverage against supersonic stealth fighters.", CYAN),
        ("LAYER 3: THE WORKHORSE (30 - 45 KM)", "AKASH PRIME & AKASH-NG", "High-mobility indigenous missile destroying cruise missiles & drone swarms.", GREEN),
    ]
    for i, (l_ttl, l_sys, l_desc, l_clr) in enumerate(l_layers):
        ly = 240 + i * 180
        rrect(ctx, rx + 40, ly, rw - 80, 150, 12)
        rgba(ctx, (0.06, 0.09, 0.14), 0.8)
        ctx.fill()
        rrect(ctx, rx + 40, ly, rw - 80, 150, 12)
        rgba(ctx, l_clr, 0.4)
        ctx.set_line_width(1.5)
        ctx.stroke()
        draw_text(ctx, l_ttl, rx + 70, ly + 36, size=24, c=l_clr, font="Impact", anchor="l")
        draw_text(ctx, l_sys, rx + 70, ly + 76, size=28, c=WHITE, font="Impact", anchor="l")
        draw_text(ctx, l_desc, rx + 70, ly + 115, size=18, c=GRAY, font="Impact", anchor="l")

def draw_scene_7(ctx, t, d):
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 7, "Layers 4 & 5: Point Defense & Terminal Iron Fist", t)
    
    lx, lw = 80, 960
    rrect(ctx, lx, 130, lw, 330, 16)
    rgba(ctx, (0.04, 0.06, 0.1), 0.85)
    ctx.fill()
    rrect(ctx, lx, 130, lw, 330, 16)
    rgba(ctx, AMBER, 0.35)
    ctx.set_line_width(2)
    ctx.stroke()
    
    draw_text(ctx, "LAYER 4: MOBILE POINT DEFENSE (15 - 30 KM)", lx + 40, 175, size=24, c=AMBER, font="Impact", anchor="l")
    draw_text(ctx, "QRSAM (QUICK REACTION SAM)", lx + 40, 220, size=32, c=WHITE, font="Impact", anchor="l")
    draw_text(ctx, "• Deployed on high-mobility Tatra 8x8 trucks for mechanized strike forces.", lx + 40, 270, size=18, c=GRAY, font="Impact", anchor="l")
    draw_text(ctx, "• Reaction time < 6 seconds while moving in full battlefield formation.", lx + 40, 310, size=18, c=GRAY, font="Impact", anchor="l")
    draw_text(ctx, "• Provides continuous mobile air umbrella to armored tank columns.", lx + 40, 350, size=18, c=GREEN, font="Impact", anchor="l")
    
    rrect(ctx, lx, 480, lw, 340, 16)
    rgba(ctx, (0.04, 0.06, 0.1), 0.85)
    ctx.fill()
    rrect(ctx, lx, 480, lw, 340, 16)
    rgba(ctx, RED, 0.35)
    ctx.set_line_width(2)
    ctx.stroke()
    
    draw_text(ctx, "LAYER 5: THE TERMINAL IRON FIST (0 - 6 KM)", lx + 40, 525, size=24, c=RED, font="Impact", anchor="l")
    draw_text(ctx, "VSHORADS & DIRECTED ENERGY LASERS", lx + 40, 570, size=32, c=WHITE, font="Impact", anchor="l")
    draw_text(ctx, "• Very Short Range Air Defense: Man-portable & vehicle mounted micro-missiles.", lx + 40, 620, size=18, c=GRAY, font="Impact", anchor="l")
    draw_text(ctx, "• High-rate multi-barrel auto-cannons creating steel wall of flak.", lx + 40, 660, size=18, c=GRAY, font="Impact", anchor="l")
    draw_text(ctx, "• Kinetic lasers burning suicide kamikaze drone swarms in final seconds.", lx + 40, 700, size=18, c=GOLD, font="Impact", anchor="l")
    
    rx, rw = 1080, 760
    rrect(ctx, rx, 130, rw, 690, 16)
    rgba(ctx, (0.04, 0.06, 0.1), 0.85)
    ctx.fill()
    rrect(ctx, rx, 130, rw, 690, 16)
    rgba(ctx, CYAN, 0.35)
    ctx.set_line_width(2)
    ctx.stroke()
    
    draw_text(ctx, "CONCENTRIC 5-LAYER AIR DEFENSE UMBRELLA", rx + rw / 2, 180, size=22, c=CYAN, font="Impact", anchor="c")
    
    dcx, dcy = rx + rw / 2, 720
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
        
    line(ctx, [(rx + 40, dcy), (rx + rw - 40, dcy)], STEEL, 3, 0.8)
    draw_text(ctx, "INDIAN AIRSPACE BORDER", dcx, dcy + 25, size=16, c=GRAY, font="Impact", anchor="c")

def draw_scene_8(ctx, t, d):
    draw_bg_grid(ctx, t)
    draw_hud_header(ctx, 8, "Strategic Sovereignty: The Road to 2028", t)
    
    tw = 400
    rrect(ctx, W / 2 - tw / 2, 130, tw, 6, 3)
    rrect(ctx, W / 2 - tw / 2, 130, tw / 3, 6, 2)
    rgba(ctx, SAFFRON, 1.0)
    ctx.fill()
    rrect(ctx, W / 2 - tw / 2 + tw / 3, 130, tw / 3, 6, 2)
    rgba(ctx, WHITE, 1.0)
    ctx.fill()
    rrect(ctx, W / 2 + tw / 6, 130, tw / 3, 6, 2)
    rgba(ctx, GREEN, 1.0)
    ctx.fill()
    
    draw_text(ctx, "BHARAT'S STRATEGIC INDEPENDENCE", W / 2, 180, size=36, c=GOLD, font="Impact", anchor="c")
    draw_text(ctx, "NO FOREIGN LEASH ON INDIAN AIR DEFENSE SOVEREIGNTY", W / 2, 225, size=20, c=CYAN, font="Impact", anchor="c")
    
    rrect(ctx, 120, 270, W - 240, 160, 16)
    rgba(ctx, (0.04, 0.06, 0.1), 0.85)
    ctx.fill()
    rrect(ctx, 120, 270, W - 240, 160, 16)
    rgba(ctx, GOLD, 0.4)
    ctx.set_line_width(2)
    ctx.stroke()
    
    milestones = [
        ("OCT 2023", "CABINET APPROVAL", "₹21,700 CR ALLOCATED"),
        ("2025 - 2026", "DEVELOPMENT TRIALS", "GaN AESA RADAR + M1/M2/M3"),
        ("2027 - 2028", "USER VALIDATION", "INDIAN AIR FORCE USER TRIALS"),
        ("2028 - 2029", "OPERATIONAL INDUCTION", "LAC FULL POWER BALANCE SHIFT"),
    ]
    for i, (m_yr, m_hd, m_sb) in enumerate(milestones):
        mx = 180 + i * 380
        my = 350
        circle(ctx, mx, my, 18, GOLD, 0.9)
        circle(ctx, mx, my, 10, (0.05, 0.08, 0.12), 1.0)
        draw_text(ctx, m_yr, mx, my - 45, size=20, c=GOLD, font="Impact", anchor="c")
        draw_text(ctx, m_hd, mx, my + 35, size=18, c=WHITE, font="Impact", anchor="c")
        draw_text(ctx, m_sb, mx, my + 60, size=14, c=GRAY, font="Impact", anchor="c")
        if i < len(milestones) - 1:
            line(ctx, [(mx + 25, my), (mx + 355, my)], GOLD, 2, 0.4)
            
    rrect(ctx, 120, 460, W - 240, 360, 16)
    rgba(ctx, (0.04, 0.07, 0.12), 0.9)
    ctx.fill()
    rrect(ctx, 120, 460, W - 240, 360, 16)
    rgba(ctx, AMBER, 0.5)
    ctx.set_line_width(2.5)
    ctx.stroke()
    
    draw_text(ctx, "THE MILLION DOLLAR STRATEGIC QUESTION", W / 2, 510, size=28, c=AMBER, font="Impact", anchor="c")
    draw_text(ctx, "KYA BHARAT KO FOREIGN AIR DEFENSE KHAREEDNA CHAHIYE YA", W / 2, 560, size=24, c=WHITE, font="Impact", anchor="c")
    draw_text(ctx, "POORI FUNDING PROJECT KUSHA JAISI INDIGENOUS SHIELDS PAR LAGANI CHAHIYE?", W / 2, 595, size=24, c=GOLD, font="Impact", anchor="c")
    
    rrect(ctx, 180, 650, 720, 120, 12)
    rgba(ctx, (0.06, 0.09, 0.15), 0.8)
    ctx.fill()
    draw_text(ctx, "[ OPTION A ]", 220, 685, size=22, c=CYAN, font="Impact", anchor="l")
    draw_text(ctx, "Buy more foreign systems (S-400 / David's Sling) for instant cover.", 220, 725, size=18, c=GRAY, font="Impact", anchor="l")
    
    rrect(ctx, 980, 650, 760, 120, 12)
    rgba(ctx, (0.04, 0.12, 0.08), 0.8)
    ctx.fill()
    draw_text(ctx, "[ OPTION B ]", 1020, 685, size=22, c=GREEN, font="Impact", anchor="l")
    draw_text(ctx, "100% focus on Project Kusha & Atmanirbhar Bharat air shield.", 1020, 725, size=18, c=WHITE, font="Impact", anchor="l")

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
        w_json = WORK_DIR / f"scene_{i+1:02d}_words.json"
        words = []
        if w_json.exists():
            with open(w_json, encoding='utf-8') as jf:
                words = json.load(jf)
        scenes_meta.append({
            "index": i,
            "start": t_acc,
            "dur": dur,
            "end": t_acc + dur,
            "words": words,
        })
        t_acc += dur
    
    # Subtitle cues
    subtitles = []
    for sc in scenes_meta:
        words = sc["words"]
        idx = 0
        while idx < len(words):
            chunk = words[idx:idx + 6]
            text = " ".join(w["word"].strip() for w in chunk)
            start_t = sc["start"] + chunk[0]["start"]
            end_t = sc["start"] + chunk[-1]["end"]
            subtitles.append({"start": start_t, "end": end_t, "text": text})
            idx += 6
            
    return scenes_meta, subtitles, t_acc

def render_thumbnail():
    thumb_path = OUT_DIR / "project_kusha_thumbnail.png"
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1920, 1080)
    ctx = cairo.Context(surf)
    
    # High-contrast tactical background
    draw_bg_grid(ctx, 0)
    
    # Split glow: Left Red/Orange (S-400), Right Cyan/Gold (Kusha)
    g_left = cairo.RadialGradient(400, 540, 50, 400, 540, 600)
    g_left.add_color_stop_rgba(0, 0.8, 0.2, 0.1, 0.35)
    g_left.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g_left)
    ctx.paint()
    
    g_right = cairo.RadialGradient(1520, 540, 50, 1520, 540, 600)
    g_right.add_color_stop_rgba(0, 0.1, 0.7, 0.9, 0.35)
    g_right.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g_right)
    ctx.paint()
    
    # Left Card: S-400
    rrect(ctx, 80, 240, 760, 560, 20)
    rgba(ctx, (0.05, 0.05, 0.08), 0.9)
    ctx.fill()
    rrect(ctx, 80, 240, 760, 560, 20)
    rgba(ctx, RED, 0.8)
    ctx.set_line_width(4)
    ctx.stroke()
    
    draw_text(ctx, "RUSSIAN TITAN", 460, 310, size=32, c=RED, font="Impact", anchor="c")
    draw_text(ctx, "S-400 TRIUMF", 460, 380, size=64, c=WHITE, font="Impact", anchor="c")
    draw_text(ctx, "• 400 KM HEAVY MISSILE", 460, 470, size=32, c=STEEL, font="Impact", anchor="c")
    draw_text(ctx, "• PESA RADAR TRACKING", 460, 530, size=32, c=STEEL, font="Impact", anchor="c")
    draw_text(ctx, "• FOREIGN SUPPLY RISKS", 460, 590, size=32, c=RED, font="Impact", anchor="c")
    
    # Right Card: PROJECT KUSHA
    rrect(ctx, 1080, 240, 760, 560, 20)
    rgba(ctx, (0.04, 0.07, 0.12), 0.9)
    ctx.fill()
    rrect(ctx, 1080, 240, 760, 560, 20)
    rgba(ctx, GOLD, 0.8)
    ctx.set_line_width(4)
    ctx.stroke()
    
    draw_text(ctx, "DRDO'S SECRET SHIELD", 1460, 310, size=32, c=GOLD, font="Impact", anchor="c")
    draw_text(ctx, "PROJECT KUSHA", 1460, 380, size=64, c=GOLD, font="Impact", anchor="c")
    draw_text(ctx, "• GaN AESA STEALTH KILLER", 1460, 470, size=32, c=CYAN, font="Impact", anchor="c")
    draw_text(ctx, "• HIT-TO-KILL KINETIC TECH", 1460, 530, size=32, c=GREEN, font="Impact", anchor="c")
    draw_text(ctx, "• 100% ATMANIRBHAR BHARAT", 1460, 590, size=32, c=GOLD, font="Impact", anchor="c")
    
    # Center VS Badge
    circle(ctx, 960, 520, 80, (0.02, 0.03, 0.05), 1.0)
    circle(ctx, 960, 520, 80, GOLD, 0.9, fill=False, w=4)
    draw_text(ctx, "VS", 960, 520, size=52, c=WHITE, font="Impact", anchor="c")
    
    # Top Eye-Catching Banner
    rrect(ctx, 120, 60, W - 240, 130, 16)
    rgba(ctx, (0.05, 0.08, 0.16), 0.95)
    ctx.fill()
    rrect(ctx, 120, 60, W - 240, 130, 16)
    rgba(ctx, GOLD, 0.9)
    ctx.set_line_width(3)
    ctx.stroke()
    draw_text(ctx, "S-400 SE BHI DANGEROUS?", W / 2, 125, size=68, c=GOLD, font="Impact", anchor="c")
    
    # Bottom Badge
    rrect(ctx, 400, 850, 1120, 120, 16)
    rgba(ctx, (0.85, 0.15, 0.15), 0.95)
    ctx.fill()
    draw_text(ctx, "BHARAT KA 400 KM AIR SHIELD!", W / 2, 910, size=56, c=WHITE, font="Impact", anchor="c")
    
    surf.write_to_png(str(thumb_path))
    print(f"Thumbnail created: {thumb_path}")
    return thumb_path

def generate_upload_kit(total_dur):
    kit_path = OUT_DIR / "project_kusha_upload_kit.md"
    content = f"""# YouTube Upload Kit: Project Kusha vs S-400

## 1. Title Options (Choose one)
- **Option 1 (Highest CTR)**: Project Kusha vs S-400: Inside India's Ultra Long-Range Air Defense Shield 🔥
- **Option 2 (Curiosity & Tech)**: S-400 से भी खतरनाक? DRDO का Project Kusha Air Defense Secret Revealed!
- **Option 3 (Documentary)**: How India Is Building an Unbreakable 5-Layer Iron Dome Shield (Project Kusha)

---

## 2. Description & Chapters (Copy-Paste Ready)
```text
Kya India ka Project Kusha Russian S-400 Triumf se zyada powerful aur dangerous hai? 

October 2023 mein Cabinet Committee on Security (CCS) ne ₹21,700 Crore ke budget ke sath DRDO ke Project Kusha ko manzoori di thi. Yeh ultra long-range surface-to-air missile system 350 se 400 kilometer door dushman ke 5th generation stealth fighters (Chengdu J-20), AWACS command aircraft, hypersonic glide vehicles aur cruise missiles ko hawa mein hi raakh banane ke liye design kiya gaya hai.

Is detailed documentary mein hum decode karenge:
- S-400 Triumf vs Project Kusha ka Tech Duel (GaN AESA vs PESA Radar)
- Hit-to-Kill kinetic interception mechanism
- Bharat ka 5-Layer Iron Dome Network (Kusha, MRSAM, Akash, QRSAM, VSHORADS)
- 2028 deployment timeline aur LAC par strategic power shift.

📌 CHAPTER TIMESTAMPS:
00:00 - The 50-Stealth Threat at LAC
00:46 - The Russian Titan: S-400 in India
01:33 - Why India Needs Kusha (Foreign Supply Crisis)
02:16 - DRDO Project Kusha Revealed (₹21,700 Cr Budget)
03:00 - Tech Duel: GaN AESA Radar & Hit-to-Kill
03:44 - IACCS & Bharat's 5-Layer Air Defense (Layers 1-3)
04:30 - Point Defense & Terminal Iron Fist (Layers 4-5)
05:11 - Strategic Sovereignty & The Road to 2028

🔔 Subscribe to RealityShift for high-voltage Indian Defense & Geopolitics deep dives!
Jai Hind! Vande Mataram!

#ProjectKusha #S400 #IndianDefense #DRDO #AirDefense #RealityShift #IndianAirForce #MakeInIndia
```

---

## 3. SEO Tags
```text
Project Kusha, S400 air defense, Project Kusha vs S400, Indian air defense shield, DRDO Project Kusha, India long range missile, S400 Triumf India, GaN AESA radar, Hit to kill missile, Indian Iron Dome, Akash Prime, MRSAM Barak 8, QRSAM, VSHORADS, RealityShift, RealityShiftByAnkit, Indian Defense news, LAC defense shield, Chengdu J20 vs Kusha
```

---

## 4. Pinned Comment (High-Engagement Debate)
```text
👇 Aapke hisab se Bharat ki strategic policy kya honi chahiye:
[A] Hume emergency cover ke liye Russia se aur foreign S-400 squadrons lene chahiye.
[B] Hume 100% budget aur priority DRDO ke Project Kusha jaise indigenous weapons par lagani chahiye.

Apna vote aur raye comment mein zaroor batayein! 🇮🇳
```
"""
    with open(kit_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Upload kit generated: {kit_path}")
    return kit_path

def render_full_video():
    scenes_meta, subtitles, total_dur = load_timeline()
    audio_mix = WORK_DIR / "final_master_mix.wav"
    out_video = OUT_DIR / "project_kusha_documentary.mp4"
    
    print(f"Total video duration: {total_dur:.2f}s (~{total_dur/60:.2f} mins)")
    print(f"Total frames at 30 FPS: {int(total_dur * FPS)}")
    
    # FFmpeg pipe setup
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
    sub_idx = 0
    
    for f_idx in range(total_frames):
        t = f_idx / FPS
        
        # Determine current scene
        while current_scene_idx < len(scenes_meta) - 1 and t >= scenes_meta[current_scene_idx]["end"]:
            current_scene_idx += 1
            
        sc = scenes_meta[current_scene_idx]
        local_t = t - sc["start"]
        drawer = SCENE_DRAWERS[sc["index"]]
        
        # Draw visual scene
        drawer(ctx, local_t, sc["dur"])
        
        # Determine active subtitle
        active_sub = ""
        for s in subtitles:
            if s["start"] <= t <= s["end"]:
                active_sub = s["text"]
                break
        if active_sub:
            draw_subtitles(ctx, active_sub)
            
        buf = surf.get_data()
        proc.stdin.write(buf)
        
        if f_idx % 300 == 0:
            elapsed = time.time() - t0
            fps_rend = (f_idx + 1) / max(elapsed, 0.001)
            eta = (total_frames - f_idx) / max(fps_rend, 0.001)
            print(f"Render progress: {f_idx}/{total_frames} frames ({f_idx/total_frames*100:.1f}%) | Speed: {fps_rend:.1f} FPS | ETA: {eta:.1f}s")
            
    proc.stdin.close()
    proc.wait()
    
    total_time = time.time() - t0
    print(f"Video render complete in {total_time:.1f}s ({total_time/60:.2f} mins)!")
    print(f"Output MP4: {out_video}")
    return out_video

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "--all"
    scenes_meta, subtitles, total_dur = load_timeline()
    
    if action in ("--thumb", "--all"):
        render_thumbnail()
    if action in ("--kit", "--all"):
        generate_upload_kit(total_dur)
    if action in ("--render", "--all"):
        render_full_video()
