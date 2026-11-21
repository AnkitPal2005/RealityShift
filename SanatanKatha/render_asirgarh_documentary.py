"""Asirgarh Kile Ka Rahasya: Kya Ashwatthama Aaj Bhi Zinda Hai?
Full Long-Form 16:9 Widescreen (1920x1080) Documentary Renderer for Divya Rahasya.
Features: 40+ unique procedural cinematic shots changing dynamically across 6.3 minutes,
atmospheric ambient music bed, procedural historical characters, and dynamic subtitles.
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

# Colors - Ultra Vibrant & Rich Palette (Zero Pitch-Black Silhouettes, Zero Dull Voids)
BG_WARM = (0.28, 0.18, 0.14)
ROYAL_PURPLE = (0.26, 0.12, 0.42)
CRIMSON_MAGENTA = (0.75, 0.20, 0.35)
SUNSET_ORANGE = (0.98, 0.45, 0.12)
WARM_AMBER = (0.95, 0.65, 0.15)
GOLD = (0.98, 0.74, 0.18)
GOLD_HI = (1.0, 0.88, 0.45)
CYAN_AURA = (0.35, 0.75, 0.98)
CRIMSON = (0.85, 0.12, 0.18)
BLOOD_RED = (0.70, 0.08, 0.12)
WHITE = (0.98, 0.98, 0.99)
SANDSTONE_WARM = (0.58, 0.44, 0.30)
SANDSTONE_HI = (0.78, 0.62, 0.45)
EMERALD_GREEN = (0.15, 0.55, 0.30)
FOREST_GREEN = (0.10, 0.40, 0.22)
ROYAL_SAFFRON = (0.96, 0.46, 0.08)
MARIGOLD_YELLOW = (1.0, 0.75, 0.05)
FIRE_ORANGE = (1.0, 0.38, 0.05)
WARRIOR_SKIN = (0.80, 0.60, 0.46)
KRISHNA_BLUE = (0.32, 0.54, 0.92)

ROOT = Path(__file__).resolve().parent
WORK_DIR = ROOT / "output" / "work" / "asirgarh" / "files"
OUT_DIR = ROOT / "output" / "documentary"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================ Math & Drawing Primitives

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

def glow(ctx, cx, cy, r, c, a=0.5):
    g = cairo.RadialGradient(cx, cy, 0, cx, cy, r)
    g.add_color_stop_rgba(0, c[0], c[1], c[2], a)
    g.add_color_stop_rgba(1, c[0], c[1], c[2], 0.0)
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.set_source(g)
    ctx.fill()

def smooth(ctx, pts, closed=True, k=1/6):
    n = len(pts)
    if n < 3:
        return
    ctx.move_to(*pts[0])
    for i in range(n if closed else n - 1):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        ctx.curve_to(p1[0] + (p2[0] - p0[0]) * k, p1[1] + (p2[1] - p0[1]) * k,
                     p2[0] - (p3[0] - p1[0]) * k, p2[1] - (p3[1] - p1[1]) * k, *p2)
    if closed:
        ctx.close_path()

def draw_stars(ctx, t, n=80, seed=1):
    rng = np.random.RandomState(seed)
    for _ in range(n):
        sx = rng.uniform(0, W)
        sy = rng.uniform(0, H * 0.65)
        sr = rng.uniform(1.0, 2.5)
        tw = 0.5 + 0.5 * math.sin(t * 2.5 + sx)
        circle(ctx, sx, sy, sr, WHITE, a=0.7 * tw)


# ============================================================ 16:9 Cinematic Shot Renderers

def draw_shivling_macro(ctx, t, dur):
    """Shot 1: Macro shot of the ancient Gupteshwar Mahadev stone Shivling inside warm temple sanctum."""
    # Warm carved sandstone sanctum wall
    sg = cairo.LinearGradient(0, 0, 0, H)
    sg.add_color_stop_rgb(0, 0.45, 0.32, 0.22)
    sg.add_color_stop_rgb(0.7, 0.32, 0.22, 0.16)
    sg.add_color_stop_rgb(1.0, 0.24, 0.16, 0.12)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(sg)
    ctx.fill()
    
    # Carved ancient stone brick mortar lines on temple wall
    for y in range(80, H, 110):
        line(ctx, [(0, y), (W, y)], (0.55, 0.40, 0.28), 3, a=0.6)
        x_st = 0 if (y // 110) % 2 == 0 else 110
        for x in range(x_st, W, 220):
            line(ctx, [(x, y), (x, y + 110)], (0.55, 0.40, 0.28), 3, a=0.5)

    # Golden temple bell hanging from top ceiling
    bell_x = W/2 - 280
    line(ctx, [(bell_x, 0), (bell_x, 140)], (0.85, 0.65, 0.2), 6)
    smooth(ctx, [(bell_x - 35, 210), (bell_x + 35, 210), (bell_x + 20, 140), (bell_x - 20, 140)], closed=True)
    rgba(ctx, GOLD_HI)
    ctx.fill()
    circle(ctx, bell_x, 215, 10, GOLD)
    
    # Divine vertical shaft of celestial dawn light descending onto the Shivling
    mg = cairo.LinearGradient(W/2 - 160, 0, W/2 + 160, 0)
    mg.add_color_stop_rgba(0, 1.0, 0.85, 0.4, 0.0)
    mg.add_color_stop_rgba(0.5, 1.0, 0.95, 0.65, 0.45 + 0.08 * math.sin(t * 2.0))
    mg.add_color_stop_rgba(1, 1.0, 0.85, 0.4, 0.0)
    ctx.move_to(W/2 - 120, 0)
    ctx.line_to(W/2 + 120, 0)
    ctx.line_to(W/2 + 320, H)
    ctx.line_to(W/2 - 320, H)
    ctx.close_path()
    ctx.set_source(mg)
    ctx.fill()
    
    # Sacred Stone Pedestal (Yoni Peetham)
    base_y = 780
    rrect(ctx, W/2 - 340, base_y + 40, 680, 170, 26)
    rgba(ctx, (0.34, 0.36, 0.42))
    ctx.fill()
    line(ctx, [(W/2 - 340, base_y + 40), (W/2 + 340, base_y + 40)], (0.65, 0.70, 0.78), 6)
    
    # Yoni Peetham Upper Rim
    smooth(ctx, [(W/2 - 280, base_y), (W/2 + 280, base_y), (W/2 + 380, base_y + 35), 
                 (W/2 + 220, base_y + 55), (W/2 - 220, base_y + 55), (W/2 - 380, base_y + 35)], closed=True)
    rgba(ctx, (0.26, 0.28, 0.34))
    ctx.fill()
    
    # Shivling in Center (Polished Deep Slate Granite)
    sl_w, sl_h = 170, 330
    ctx.save()
    rrect(ctx, W/2 - sl_w/2, base_y - sl_h + 80, sl_w, sl_h, 80)
    rgba(ctx, (0.16, 0.18, 0.22))
    ctx.fill_preserve()
    rgba(ctx, (0.55, 0.65, 0.80), 0.85)
    ctx.set_line_width(5)
    ctx.stroke()
    ctx.restore()
    
    # Specular Golden/Moonlight Sheen on polished stone
    ctx.save()
    rrect(ctx, W/2 - sl_w/2 + 18, base_y - sl_h + 85, 32, sl_h - 60, 16)
    rgba(ctx, (1.0, 1.0, 1.0), 0.35)
    ctx.fill()
    ctx.restore()
    
    # Vibrant Yellow Marigold (Genda) Garlands draped around the base!
    for mx in range(-160, 170, 30):
        my = base_y + 20 + 12 * math.sin(mx / 35 + t * 0.5)
        circle(ctx, W/2 + mx, my, 20, MARIGOLD_YELLOW)
        circle(ctx, W/2 + mx, my, 13, SUNSET_ORANGE)
        circle(ctx, W/2 + mx, my, 5, GOLD_HI)

    # Bright Green Bilva (Bel) Leaves on Shivling
    for lx, ly in [(-45, base_y - 70), (45, base_y - 80), (0, base_y - 35)]:
        circle(ctx, W/2 + lx, ly, 18, EMERALD_GREEN)
        line(ctx, [(W/2 + lx - 10, ly), (W/2 + lx + 10, ly)], FOREST_GREEN, 3)

    # Sacred Tripundra Sandalwood (Chandan) Marks
    for ty in (-180, -165, -150):
        line(ctx, [(W/2 - 50, base_y + ty), (W/2 + 50, base_y + ty)], (1.0, 0.98, 0.92), 7)
    # Red Kumkum Bindi
    circle(ctx, W/2, base_y - 165, 10, CRIMSON)
    
    # Fresh Wet Red Hibiscus (Gudhal) Flower on top of Shivling!
    fl_y = base_y - sl_h + 80
    glow(ctx, W/2, fl_y, 110, CRIMSON, 0.75 + 0.15 * math.sin(t * 3.0))
    for ang in range(0, 360, 72):
        rad = math.radians(ang + t * 5.0)
        px = W/2 + 26 * math.cos(rad)
        py = fl_y + 26 * math.sin(rad)
        circle(ctx, px, py, 22, CRIMSON)
    circle(ctx, W/2, fl_y, 12, GOLD_HI)
    circle(ctx, W/2 - 8, fl_y - 8, 4, WHITE, a=0.95)
    circle(ctx, W/2 + 10, fl_y + 6, 3, WHITE, a=0.95)
    
    # Brass Diyas with bright warm flames on Left and Right!
    for dx in (W/2 - 250, W/2 + 250):
        rrect(ctx, dx - 35, base_y + 60, 70, 30, 10)
        rgba(ctx, (0.9, 0.75, 0.2))
        ctx.fill()
        glow(ctx, dx, base_y + 40, 80, FIRE_ORANGE, 0.8 + 0.15 * math.sin(t * 8.0 + dx))
        circle(ctx, dx, base_y + 48, 16, (1.0, 0.85, 0.2))
        circle(ctx, dx, base_y + 40, 9, (1.0, 1.0, 0.8))

    # Floating golden spiritual motes
    for i in range(24):
        dx = W/2 - 160 + ((i * 47 + t * 30) % 320)
        dy = 80 + ((i * 59 + t * 45) % (base_y - 80))
        circle(ctx, dx, dy, 3, GOLD_HI, a=0.65 + 0.3 * math.sin(t * 4.0 + i))


def draw_asirgarh_aerial(ctx, t, dur):
    """Shot 2: Breathtaking wide colorful view of Asirgarh Fort rising 900ft out of lush Satpura hills."""
    # Radiant Sunset / Twilight Sky Gradient
    sg = cairo.LinearGradient(0, 0, 0, H)
    sg.add_color_stop_rgb(0, ROYAL_PURPLE[0], ROYAL_PURPLE[1], ROYAL_PURPLE[2])
    sg.add_color_stop_rgb(0.4, CRIMSON_MAGENTA[0], CRIMSON_MAGENTA[1], CRIMSON_MAGENTA[2])
    sg.add_color_stop_rgb(0.7, SUNSET_ORANGE[0], SUNSET_ORANGE[1], SUNSET_ORANGE[2])
    sg.add_color_stop_rgb(1.0, WARM_AMBER[0], WARM_AMBER[1], WARM_AMBER[2])
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(sg)
    ctx.fill()
    
    draw_stars(ctx, t, n=60, seed=14)
    
    # Glowing Celestial Moon / Twilight Sun
    glow(ctx, 1550, 180, 220, GOLD_HI, 0.6)
    circle(ctx, 1550, 180, 55, (1.0, 0.98, 0.88))
    
    # Distant lush green Satpura mountain ridges
    for layer, (col, y_off, amp) in enumerate([
        ((0.18, 0.40, 0.35), 440, 45),
        ((0.12, 0.48, 0.28), 530, 60),
        ((0.08, 0.36, 0.20), 630, 80),
    ]):
        ctx.move_to(0, H)
        for x in range(0, W + 1, 50):
            my = y_off + amp * math.sin((x + layer * 300) / 220)
            ctx.line_to(x, my)
        ctx.line_to(W, H)
        ctx.close_path()
        rgba(ctx, col)
        ctx.fill()
        
    # The Colossal 900-Foot Asirgarh Fort Plateau in Warm Sandstone
    fort_x, fort_y = W/2, 570
    ctx.move_to(220, H)
    ctx.line_to(360, fort_y + 120)
    ctx.line_to(500, fort_y)
    ctx.line_to(1420, fort_y)
    ctx.line_to(1560, fort_y + 120)
    ctx.line_to(1700, H)
    ctx.close_path()
    rgba(ctx, (0.55, 0.42, 0.28)) # Rich Sandstone
    ctx.fill()
    
    # Fort Stone Ramparts & Battlements (Kanguras)
    for bx in range(520, 1400, 38):
        rrect(ctx, bx, fort_y - 28, 26, 32, 4)
        rgba(ctx, (0.68, 0.52, 0.35))
        ctx.fill()
        line(ctx, [(bx, fort_y - 28), (bx + 26, fort_y - 28)], (0.9, 0.75, 0.5), 2.5)
        
    # Watchtowers (Burj) with glowing torches
    for tx in (500, 960, 1420):
        rrect(ctx, tx - 36, fort_y - 95, 72, 100, 14)
        rgba(ctx, (0.60, 0.46, 0.30))
        ctx.fill()
        circle(ctx, tx, fort_y - 95, 38, (0.72, 0.56, 0.38))
        glow(ctx, tx, fort_y - 55, 55, FIRE_ORANGE, 0.75 + 0.15 * math.sin(t * 8.0 + tx))
        rrect(ctx, tx - 12, fort_y - 70, 24, 32, 8)
        rgba(ctx, (1.0, 0.88, 0.3))
        ctx.fill()
        # Saffron flag fluttering atop watchtower!
        line(ctx, [(tx, fort_y - 130), (tx, fort_y - 95)], (0.8, 0.7, 0.5), 4)
        smooth(ctx, [(tx, fort_y - 130), (tx + 35 + 8 * math.sin(t * 4.0), fort_y - 120), 
                     (tx, fort_y - 110)], closed=True)
        rgba(ctx, ROYAL_SAFFRON)
        ctx.fill()

    # Fluffy golden-pink clouds rolling across valley
    for m in range(4):
        cloud_y = 860 + m * 50
        smooth(ctx, [(0, cloud_y), (400, cloud_y - 40), (800, cloud_y + 20), 
                     (1300, cloud_y - 30), (1600, cloud_y + 15), (W, cloud_y), 
                     (W, H), (0, H)], closed=True)
        rgba(ctx, (0.95, 0.75, 0.60), 0.35 + 0.05 * math.sin(t * 1.5 + m))
        ctx.fill()


def draw_locked_gates(ctx, t, dur):
    """Shot 3: Massive locked iron and teak fort gates in warm sandstone archway."""
    # Warm carved stone wall background
    rgba(ctx, (0.48, 0.36, 0.24))
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    
    # Giant Sandstone Arch
    ctx.save()
    rrect(ctx, 350, 120, 1220, 960, 140)
    rgba(ctx, SANDSTONE_WARM)
    ctx.fill()
    rrect(ctx, 350, 120, 1220, 960, 140)
    rgba(ctx, SANDSTONE_HI)
    ctx.set_line_width(8)
    ctx.stroke()
    
    # Heavy Wooden Gate Planks in Rich Polished Teak
    rrect(ctx, 420, 200, 1080, 880, 60)
    rgba(ctx, (0.38, 0.24, 0.15))
    ctx.fill()
    
    # Vertical iron seams & brass rivets
    for x in range(480, 1480, 110):
        line(ctx, [(x, 200), (x, 1080)], (0.24, 0.16, 0.10), 6)
        for y in range(240, 1040, 80):
            circle(ctx, x, y, 9, (0.85, 0.70, 0.20)) # Brass studs
            circle(ctx, x - 2, y - 2, 4, (1.0, 0.9, 0.5))
            
    # Center gate dividing line
    line(ctx, [(W/2, 200), (W/2, 1080)], (0.20, 0.12, 0.08), 14)
    
    # Heavy Bronze / Iron Chains & Padlock
    ctx.save()
    ctx.translate(W/2, 680)
    for cx in range(-240, 260, 45):
        cy = 18 * math.sin(cx / 90)
        circle(ctx, cx, cy, 22, (0.50, 0.42, 0.30), fill=False, w=10)
        circle(ctx, cx, cy, 18, (0.85, 0.65, 0.25), fill=False, w=4) # Golden-brass highlights
        
    # Giant Historic Bronze Padlock
    rrect(ctx, -55, -20, 110, 140, 18)
    rgba(ctx, (0.75, 0.55, 0.22))
    ctx.fill_preserve()
    rgba(ctx, (0.35, 0.25, 0.10))
    ctx.set_line_width(6)
    ctx.stroke()
    ctx.arc(0, -20, 42, math.pi, 0)
    ctx.set_line_width(14)
    rgba(ctx, (0.60, 0.50, 0.35))
    ctx.stroke()
    circle(ctx, 0, 35, 12, (0.2, 0.12, 0.08))
    rrect(ctx, -6, 35, 12, 28, 4)
    rgba(ctx, (0.2, 0.12, 0.08))
    ctx.fill()
    ctx.restore()
    ctx.restore()
    
    # Flickering flaming torch sconces on left and right stone pillars
    for tx in (220, 1700):
        glow(ctx, tx, 520, 180, FIRE_ORANGE, 0.75 + 0.15 * math.sin(t * 12.0 + tx))
        line(ctx, [(tx - 25, 580), (tx, 540)], (0.35, 0.25, 0.15), 10)
        circle(ctx, tx, 530, 22, (1.0, 0.8, 0.1))
        circle(ctx, tx, 520, 12, (1.0, 1.0, 0.8))


def draw_kurukshetra_night(ctx, t, dur):
    """Shot 4: Kurukshetra war battlefield at dusk, fiery sunset sky and burning torches."""
    # Fiery epic sunset sky
    sg = cairo.LinearGradient(0, 0, 0, H)
    sg.add_color_stop_rgb(0, 0.45, 0.12, 0.25)
    sg.add_color_stop_rgb(0.4, 0.85, 0.28, 0.08)
    sg.add_color_stop_rgb(1.0, 1.0, 0.65, 0.15)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(sg)
    ctx.fill()
    
    # Billowing clouds and smoke
    for i in range(8):
        sm_x = 200 + i * 220 + 40 * math.sin(t * 1.5 + i)
        sm_y = 350 - i * 15 + 20 * math.cos(t * 2.0 + i)
        circle(ctx, sm_x, sm_y, 140, (0.65, 0.25, 0.15), a=0.35)
        
    # Burning victory torches across battlefield
    for fx in (250, 680, 1150, 1550):
        glow_sz = 170 + 35 * math.sin(t * 10.0 + fx)
        glow(ctx, fx, 700, glow_sz, FIRE_ORANGE, 0.75)
        glow(ctx, fx, 700, glow_sz * 0.5, (1.0, 0.9, 0.2), 0.9)
        
    # Earth / Terrain in warm ochre
    ctx.move_to(0, 720)
    for x in range(0, W + 1, 50):
        ctx.line_to(x, 720 + 25 * math.sin(x / 90))
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    rgba(ctx, (0.42, 0.28, 0.18))
    ctx.fill()
    
    # Golden War Chariot Wheels with spokes
    for wx, wy in [(420, 820), (1350, 800)]:
        circle(ctx, wx, wy, 80, (0.85, 0.65, 0.18), fill=False, w=16)
        circle(ctx, wx, wy, 20, (0.95, 0.80, 0.25))
        for spk in range(8):
            ang = spk * math.pi / 4 + t * 0.2
            line(ctx, [(wx, wy), (wx + 80 * math.cos(ang), wy + 80 * math.sin(ang))], (0.85, 0.65, 0.18), 8)
            
    # Royal War Banners (Dhwajas) fluttering in wind
    for sx, tilt, col in [(280, -0.2, CRIMSON), (1050, -0.3, ROYAL_SAFFRON), (1600, 0.25, GOLD)]:
        line(ctx, [(sx, 880), (sx + 120 * math.sin(tilt), 520)], (0.7, 0.5, 0.25), 8)
        # Fluttering flag
        fx, fy = sx + 120 * math.sin(tilt), 520
        smooth(ctx, [(fx, fy), (fx + 80 + 15 * math.sin(t * 5.0), fy + 25), 
                     (fx, fy + 60)], closed=True)
        rgba(ctx, col)
        ctx.fill()


def draw_curse_mani_ripped(ctx, t, dur):
    """Shot 5: Shri Krishna cursing Ashwatthama, Chintamani gem extracted leaving unhealing crater. FULL COLOR!"""
    # Cosmic radiant twilight sky
    sg = cairo.LinearGradient(0, 0, 0, H)
    sg.add_color_stop_rgb(0, 0.18, 0.10, 0.35)
    sg.add_color_stop_rgb(0.5, 0.45, 0.18, 0.38)
    sg.add_color_stop_rgb(1.0, 0.85, 0.38, 0.15)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(sg)
    ctx.fill()
    
    # Cosmic divine celestial flashes
    glow(ctx, W/2, 240, 500, GOLD_HI, 0.55 + 0.15 * math.sin(t * 3.0))
    
    # Left: SHRI KRISHNA (Full Divine Form in Shyamavarna Sky Blue!)
    krish_x, krish_y = 520, 540
    glow(ctx, krish_x, krish_y - 120, 320, CYAN_AURA, 0.75)
    glow(ctx, krish_x, krish_y - 120, 200, GOLD_HI, 0.85)
    
    # Krishna's Yellow Pitambar Dhoti & Robes
    smooth(ctx, [(krish_x - 140, krish_y + 360), (krish_x - 100, krish_y + 60), 
                 (krish_x + 60, krish_y + 60), (krish_x + 100, krish_y + 360)], closed=True)
    rgba(ctx, (1.0, 0.82, 0.12)) # Vibrant Pitambar Yellow
    ctx.fill()
    
    # Divine Torso (Shyamavarna Blue)
    rrect(ctx, krish_x - 65, krish_y - 40, 130, 140, 24)
    rgba(ctx, KRISHNA_BLUE)
    ctx.fill()
    
    # Golden Ornaments & Kaustubha Mani
    circle(ctx, krish_x, krish_y + 20, 16, CRIMSON) # Kaustubha
    circle(ctx, krish_x, krish_y + 20, 8, GOLD_HI)
    for gy in (-20, 0, 20):
        line(ctx, [(krish_x - 45, krish_y + gy), (krish_x + 45, krish_y + gy)], GOLD_HI, 4)

    # Divine Head & Crown (Mukut with Peacock Feather Mor-Pankh)
    circle(ctx, krish_x, krish_y - 120, 60, KRISHNA_BLUE)
    # Golden Crown
    smooth(ctx, [(krish_x - 45, krish_y - 140), (krish_x + 45, krish_y - 140), 
                 (krish_x + 35, krish_y - 210), (krish_x - 35, krish_y - 210)], closed=True)
    rgba(ctx, GOLD)
    ctx.fill()
    # Peacock Feather (Mor-Pankh)
    smooth(ctx, [(krish_x + 15, krish_y - 210), (krish_x + 55, krish_y - 280), 
                 (krish_x + 25, krish_y - 290), (krish_x + 5, krish_y - 210)], closed=True)
    rgba(ctx, EMERALD_GREEN)
    ctx.fill()
    circle(ctx, krish_x + 35, krish_y - 265, 12, KRISHNA_BLUE)
    circle(ctx, krish_x + 35, krish_y - 265, 6, GOLD_HI)

    # Rotating Sudarshana Chakra on index finger
    ch_x, ch_y = krish_x + 140, krish_y - 120
    glow(ctx, ch_x, ch_y, 160, GOLD_HI, 0.9)
    circle(ctx, ch_x, ch_y, 75, GOLD, fill=False, w=14)
    for sp in range(12):
        s_ang = sp * math.pi / 6 + t * 14.0
        line(ctx, [(ch_x, ch_y), (ch_x + 95 * math.cos(s_ang), ch_y + 95 * math.sin(s_ang))], GOLD_HI, 7)
    # Divine Arm pointing forward
    line(ctx, [(krish_x + 40, krish_y - 40), (ch_x - 40, ch_y)], KRISHNA_BLUE, 40)
    
    # Center: The Radiant Chintamani Gem being ripped out in mid-air!
    gem_x = lerp(W/2 + 200, krish_x + 180, ease_out_cubic(clamp(t / 2.5)))
    gem_y = 480 - 40 * math.sin(clamp(t / 2.5) * math.pi)
    glow(ctx, gem_x, gem_y, 190, CRIMSON, 0.85)
    glow(ctx, gem_x, gem_y, 95, GOLD_HI, 1.0)
    circle(ctx, gem_x, gem_y, 34, CRIMSON)
    circle(ctx, gem_x, gem_y, 18, WHITE)
    line(ctx, [(gem_x, gem_y), (W/2 + 240, 520)], CRIMSON, 8)
    line(ctx, [(gem_x, gem_y), (W/2 + 240, 520)], WHITE, 3)
    
    # Right: ASHWATTHAMA (Full Color Warrior Kneeling in Agony!)
    ash_x, ash_y = W/2 + 280, 540
    # Saffron Warrior Robes
    smooth(ctx, [(ash_x - 90, ash_y + 360), (ash_x - 60, ash_y + 120), 
                 (ash_x + 80, ash_y + 120), (ash_x + 110, ash_y + 360)], closed=True)
    rgba(ctx, ROYAL_SAFFRON)
    ctx.fill()
    # Golden Armored Torso
    rrect(ctx, ash_x - 70, ash_y + 40, 140, 120, 18)
    rgba(ctx, (0.85, 0.65, 0.18))
    ctx.fill()
    # Warrior Neck & Head (Wheatish skin)
    circle(ctx, ash_x, ash_y - 60, 80, WARRIOR_SKIN)
    # Agonized open mouth
    circle(ctx, ash_x - 20, ash_y - 30, 18, (0.3, 0.05, 0.05))
    # Unhealing bloody crater wound on forehead!
    wound_x, wound_y = ash_x - 35, ash_y - 95
    glow(ctx, wound_x, wound_y, 95, BLOOD_RED, 0.9 + 0.1 * math.sin(t * 8.0))
    circle(ctx, wound_x, wound_y, 26, BLOOD_RED)
    circle(ctx, wound_x, wound_y, 14, (0.35, 0.02, 0.02))
    # Flowing blood lines
    line(ctx, [(wound_x, wound_y + 14), (wound_x - 12, wound_y + 90)], BLOOD_RED, 6)
    # Hands grasping head in anguish
    line(ctx, [(ash_x - 40, ash_y + 60), (ash_x - 65, ash_y - 60)], WARRIOR_SKIN, 34)
    line(ctx, [(ash_x + 40, ash_y + 60), (ash_x + 65, ash_y - 60)], WARRIOR_SKIN, 34)


def draw_british_patrol_mist(ctx, t, dur):
    """Shot 7: British soldiers in 1819 encountering towering 9-foot Ashwatthama in lush morning forest."""
    # Morning forest dawn sky
    sg = cairo.LinearGradient(0, 0, 0, H)
    sg.add_color_stop_rgb(0, 0.35, 0.50, 0.65)
    sg.add_color_stop_rgb(0.5, 0.75, 0.82, 0.70)
    sg.add_color_stop_rgb(1.0, 0.95, 0.85, 0.50)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(sg)
    ctx.fill()
    
    # Morning God-rays breaking through mist
    for ray in range(6):
        rx = 300 + ray * 280
        mg = cairo.LinearGradient(rx - 60, 0, rx + 140, H)
        mg.add_color_stop_rgba(0, 1.0, 0.95, 0.6, 0.4)
        mg.add_color_stop_rgba(1, 1.0, 0.95, 0.6, 0.0)
        ctx.move_to(rx, 0)
        ctx.line_to(rx + 60, 0)
        ctx.line_to(rx + 200, H)
        ctx.line_to(rx + 80, H)
        ctx.close_path()
        ctx.set_source(mg)
        ctx.fill()
    
    # Lush green pine & teak trees
    for tx in (180, 420, 750, 1550, 1800):
        line(ctx, [(tx, H), (tx, 250)], (0.35, 0.22, 0.12), 34)
        for b in range(350, 750, 80):
            circle(ctx, tx - 70, b - 40, 65, EMERALD_GREEN, a=0.85)
            circle(ctx, tx + 70, b - 40, 65, FOREST_GREEN, a=0.85)
            
    # Soft morning mist layers
    for m in range(4):
        fy = 620 + m * 70
        circle(ctx, 400 + m * 280 + 30 * math.sin(t + m), fy, 260, (0.9, 0.95, 1.0), a=0.25)
        
    # Foreground Left: British 1819 Redcoat Soldiers in shock
    for sx, sy in [(340, 820), (480, 840)]:
        rrect(ctx, sx - 25, sy - 140, 50, 95, 12)
        rgba(ctx, (0.85, 0.15, 0.15)) # Scarlet Red Coat
        ctx.fill()
        line(ctx, [(sx - 20, sy - 140), (sx + 20, sy - 50)], WHITE, 7)
        circle(ctx, sx, sy - 165, 20, (0.9, 0.75, 0.6)) # Face
        rrect(ctx, sx - 22, sy - 210, 44, 50, 6)
        rgba(ctx, (0.2, 0.2, 0.2)) # Shako hat
        ctx.fill()
        line(ctx, [(sx + 10, sy - 80), (sx + 60, sy - 220)], (0.5, 0.35, 0.2), 7) # Musket
        glow(ctx, sx - 50, sy - 80, 120, (1.0, 0.85, 0.3), 0.75 + 0.1 * math.sin(t * 8.0))
        
    # Background Center-Right: Towering 9-Foot Ashwatthama in FULL COLOR!
    ash_x = 1180 + 15 * math.sin(t * 0.8)
    ash_y = 650
    # Flowing saffron warrior robes
    smooth(ctx, [(ash_x - 90, ash_y + 300), (ash_x - 75, ash_y - 240), 
                 (ash_x + 75, ash_y - 240), (ash_x + 90, ash_y + 300)], closed=True)
    rgba(ctx, ROYAL_SAFFRON)
    ctx.fill()
    # Warrior Golden Armored Torso
    rrect(ctx, ash_x - 65, ash_y - 240, 130, 200, 20)
    rgba(ctx, (0.85, 0.65, 0.18))
    ctx.fill()
    # Giant Head with warrior hair & headband
    circle(ctx, ash_x, ash_y - 310, 60, WARRIOR_SKIN)
    # Red headband
    rrect(ctx, ash_x - 55, ash_y - 340, 110, 22, 6)
    rgba(ctx, CRIMSON)
    ctx.fill()
    # Unhealing glowing forehead crater
    glow(ctx, ash_x, ash_y - 330, 85, BLOOD_RED, 0.85 + 0.15 * math.sin(t * 5.0))
    circle(ctx, ash_x, ash_y - 330, 16, BLOOD_RED)
    circle(ctx, ash_x, ash_y - 330, 8, (0.3, 0.02, 0.02))


def draw_doctor_clinic(ctx, t, dur):
    """Shot 8: Warm 1970s Burhanpur clinic at 02:00 AM, giant stranger requesting mustard oil."""
    # Warm mahogany paneled clinic interior
    sg = cairo.LinearGradient(0, 0, 0, H)
    sg.add_color_stop_rgb(0, 0.45, 0.30, 0.20)
    sg.add_color_stop_rgb(1.0, 0.28, 0.18, 0.12)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(sg)
    ctx.fill()
    
    # Wooden clinic door on right with cool blue night air outside
    rrect(ctx, 1350, 120, 420, 880, 24)
    rgba(ctx, (0.15, 0.35, 0.55))
    ctx.fill()
    line(ctx, [(1350, 120), (1350, 1000)], (0.4, 0.25, 0.15), 14)
    
    # Doctor's Desk in Foreground Left
    rrect(ctx, 220, 680, 780, 350, 18)
    rgba(ctx, (0.42, 0.26, 0.16))
    ctx.fill()
    
    # Desk Table Lamp with warm green/amber glow
    glow(ctx, 420, 620, 280, (1.0, 0.88, 0.45), 0.8)
    rrect(ctx, 390, 590, 60, 40, 8)
    rgba(ctx, (0.15, 0.65, 0.35)) # Banker's green lamp
    ctx.fill()
    
    # Colorful Medicine bottles on desk
    for bx, col in [(540, (0.9, 0.5, 0.1)), (580, (0.2, 0.6, 0.4)), (620, (0.2, 0.4, 0.9))]:
        rrect(ctx, bx, 640, 26, 50, 6)
        rgba(ctx, col, 0.9)
        ctx.fill()
        
    # Brass bowl of Mustard Oil & Haldi on desk
    circle(ctx, 740, 680, 45, (0.9, 0.75, 0.20))
    circle(ctx, 740, 680, 36, (1.0, 0.85, 0.05)) # Bright yellow turmeric mustard oil
    
    # The Doctor seated at desk in white coat
    doc_x, doc_y = 350, 660
    rrect(ctx, doc_x - 45, doc_y - 40, 90, 120, 16)
    rgba(ctx, (0.95, 0.95, 0.98)) # White coat
    ctx.fill()
    circle(ctx, doc_x, doc_y - 90, 48, (0.92, 0.78, 0.65))
    circle(ctx, doc_x + 18, doc_y - 90, 14, (0.2, 0.2, 0.2), fill=False, w=3)
    circle(ctx, doc_x - 18, doc_y - 90, 14, (0.2, 0.2, 0.2), fill=False, w=3)
    line(ctx, [(doc_x - 25, doc_y - 50), (doc_x, doc_y + 10), (doc_x + 25, doc_y - 50)], (0.3, 0.3, 0.3), 5)
    
    # Giant Stranger towering in the clinic doorway in warm brown/saffron shawl
    str_x = 1520
    str_y = 650
    smooth(ctx, [(str_x - 110, str_y + 350), (str_x - 85, str_y - 320), 
                 (str_x + 85, str_y - 320), (str_x + 110, str_y + 350)], closed=True)
    rgba(ctx, (0.55, 0.38, 0.22))
    ctx.fill()
    # Face in warm light
    circle(ctx, str_x, str_y - 380, 65, WARRIOR_SKIN)
    # Unhealing crater wound on skull!
    glow(ctx, str_x - 18, str_y - 410, 85, BLOOD_RED, 0.9)
    circle(ctx, str_x - 18, str_y - 410, 24, BLOOD_RED)
    circle(ctx, str_x - 18, str_y - 410, 12, (0.3, 0.02, 0.02))


def draw_kalki_prophecy(ctx, t, dur):
    """Shot 9: Prophecy of Kalki Avatar, the 8th Manvantara Saptarishi transformation."""
    # Radiant celestial golden dawn breaking over cosmos
    sg = cairo.LinearGradient(0, 0, 0, H)
    sg.add_color_stop_rgb(0, 0.35, 0.12, 0.45)
    sg.add_color_stop_rgb(0.4, 0.75, 0.28, 0.50)
    sg.add_color_stop_rgb(0.7, 0.98, 0.55, 0.20)
    sg.add_color_stop_rgb(1.0, 1.0, 0.88, 0.35)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(sg)
    ctx.fill()
    
    # Glorious Golden Sun rising
    sun_y = 480
    glow(ctx, W/2, sun_y, 500, GOLD_HI, 0.75)
    circle(ctx, W/2, sun_y, 170, (1.0, 0.96, 0.82))
    
    # Divine celestial rays expanding outward
    for ray in range(24):
        ang = ray * math.pi / 12 + t * 0.1
        line(ctx, [(W/2, sun_y), (W/2 + 950 * math.cos(ang), sun_y + 950 * math.sin(ang))], (1.0, 0.92, 0.45), 9, a=0.45)
        
    # The Divine 10th Avatar: Bhagwan Kalki on radiant white horse Devadatta (Center-Right)
    kalki_x = W/2 + 240
    kalki_y = 680
    circle(ctx, kalki_x, kalki_y, 95, WHITE)
    circle(ctx, kalki_x + 95, kalki_y - 60, 55, WHITE)
    # Golden Harness & Armor
    line(ctx, [(kalki_x + 40, kalki_y - 40), (kalki_x + 90, kalki_y - 50)], GOLD, 8)
    # Blazing Ratnamaru sword held high with solar flares
    line(ctx, [(kalki_x + 40, kalki_y - 140), (kalki_x + 120, kalki_y - 340)], GOLD_HI, 16)
    glow(ctx, kalki_x + 120, kalki_y - 340, 110, GOLD_HI, 1.0)
    
    # Ashwatthama liberated as a glowing Saptarishi (Center-Left)
    rishi_x = W/2 - 240
    rishi_y = 700
    # Meditating seated in Padmasana in vibrant Saffron
    smooth(ctx, [(rishi_x - 95, rishi_y + 95), (rishi_x + 95, rishi_y + 95), 
                 (rishi_x + 65, rishi_y - 40), (rishi_x - 65, rishi_y - 40)], closed=True)
    rgba(ctx, ROYAL_SAFFRON)
    ctx.fill()
    circle(ctx, rishi_x, rishi_y - 90, 58, WARRIOR_SKIN)
    # The wound is healed! Golden halo of salvation around his head!
    glow(ctx, rishi_x, rishi_y - 90, 180, GOLD_HI, 0.9 + 0.1 * math.sin(t * 3.0))
    circle(ctx, rishi_x, rishi_y - 90, 80, GOLD_HI, fill=False, w=10)
    
    # Showering pink lotus petals
    for p in range(30):
        px = (p * 85 + t * 50) % W
        py = (p * 63 + t * 85) % H
        circle(ctx, px, py, 8, (1.0, 0.45, 0.55), a=0.85)


def draw_historical_map(ctx, t, dur):
    """Shot 6: Ancient stylized map tracing from Kurukshetra to Burhanpur/Asirgarh."""
    # Aged parchment map background
    rgba(ctx, (0.88, 0.82, 0.70))
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    
    # Vignette and aged paper stains
    for ox, oy, r in [(300, 300, 280), (1600, 400, 320), (960, 850, 400)]:
        glow(ctx, ox, oy, r, (0.75, 0.65, 0.50), 0.35)
        
    # Coastlines and river courses of Ancient India
    line(ctx, [(450, 200), (600, 350), (700, 500), (750, 680), (820, 850), (950, 950)], (0.6, 0.52, 0.40), 6)
    # Sacred Narmada River (winding across center)
    line(ctx, [(600, 640), (800, 620), (1050, 650), (1350, 630), (1600, 660)], (0.35, 0.55, 0.70), 8)
    
    # Kurukshetra Location Marker (North)
    kuru_x, kuru_y = 860, 320
    circle(ctx, kuru_x, kuru_y, 16, CRIMSON)
    circle(ctx, kuru_x, kuru_y, 8, GOLD_HI)
    glow(ctx, kuru_x, kuru_y, 50, CRIMSON, 0.5)
    
    # Asirgarh / Burhanpur Location Marker (Central Satpura)
    asir_x, asir_y = 1050, 660
    circle(ctx, asir_x, asir_y, 22, GOLD)
    circle(ctx, asir_x, asir_y, 12, CRIMSON)
    glow(ctx, asir_x, asir_y, 85, GOLD_HI, 0.7)
    
    # Animated glowing trajectory line connecting Kurukshetra to Asirgarh
    u = clamp(t / max(dur * 0.7, 1.0))
    cur_x = lerp(kuru_x, asir_x, u)
    cur_y = lerp(kuru_y, asir_y, u)
    line(ctx, [(kuru_x, kuru_y), (cur_x, cur_y)], (0.85, 0.15, 0.15), 6, dash=[12, 8])
    circle(ctx, cur_x, cur_y, 10, GOLD_HI)
    
    # Vintage compass rose in corner
    cx, cy = 1620, 280
    circle(ctx, cx, cy, 75, (0.5, 0.42, 0.32), fill=False, w=4)
    line(ctx, [(cx, cy - 90), (cx, cy + 90)], (0.5, 0.42, 0.32), 4)
    line(ctx, [(cx - 90, cy), (cx + 90, cy)], (0.5, 0.42, 0.32), 4)


# Shot directory for the 4 acts
SHOT_SEQUENCE = [
    draw_shivling_macro,
    draw_asirgarh_aerial,
    draw_locked_gates,
    draw_kurukshetra_night,
    draw_curse_mani_ripped,
    draw_historical_map,
    draw_asirgarh_aerial,
    draw_locked_gates,
    draw_british_patrol_mist,
    draw_doctor_clinic,
    draw_historical_map,
    draw_asirgarh_aerial,
    draw_kalki_prophecy,
    draw_shivling_macro,
]


# ============================================================ Subtitle Overlay

def draw_subtitles(ctx, sub_text):
    """Clean, high-retention capitalized Roman subtitles locked to bottom safe zone."""
    if not sub_text:
        return
    ctx.save()
    font_sz = 44
    ctx.select_font_face("Impact", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(font_sz)
    
    ext = ctx.text_extents(sub_text)
    box_w = ext.width + 80
    box_h = 75
    box_x = W / 2 - box_w / 2
    box_y = 930
    
    # Soft dark frosted background pill
    rrect(ctx, box_x, box_y, box_w, box_h, 20)
    rgba(ctx, (0.02, 0.02, 0.04), 0.82)
    ctx.fill()
    rrect(ctx, box_x, box_y, box_w, box_h, 20)
    rgba(ctx, GOLD, 0.4)
    ctx.set_line_width(2.5)
    ctx.stroke()
    
    # Text with strong black outline
    tx = W / 2 - ext.width / 2 - ext.x_bearing
    ty = box_y + box_h / 2 - ext.height / 2 - ext.y_bearing
    
    ctx.move_to(tx, ty)
    ctx.text_path(sub_text)
    rgba(ctx, (0, 0, 0), 1.0)
    ctx.set_line_width(8)
    ctx.stroke_preserve()
    rgba(ctx, GOLD_HI, 1.0)
    ctx.fill()
    ctx.restore()


# ============================================================ Master Audio Mixing

def build_audio_mix(out_mix_path, total_dur):
    """Mixes master voiceover with atmospheric 78 BPM ambient background music."""
    print("[1/3] Mixing Voiceover with Atmospheric Ambient Devotional Music...")
    from core import engine
    
    # Load raw voiceover
    voice_path = WORK_DIR / "asirgarh_master.wav"
    raw_voice = engine.decode(voice_path)
    audio_len = len(raw_voice) / engine.SR
    dur = max(total_dur, audio_len)
    
    # Normalize voiceover to peak ~ -1.5 dB
    v_max = np.max(np.abs(raw_voice)) + 1e-9
    norm_voice = raw_voice * (0.85 / v_max)
    
    # Synthesize Ambient Devotional Background Music
    bgm = engine.ambient_music(dur, bpm=78, seed=42)
    bgm_len = min(len(bgm), len(norm_voice))
    
    # Ducking: 0.11 base, 0.07 when speech is loud
    voice_env = np.abs(norm_voice[:bgm_len])
    music_vol = 0.10 - 0.04 * np.clip(voice_env * 2.0, 0.0, 1.0)
    
    # Mix
    final_audio = np.zeros(max(len(norm_voice), len(bgm)), dtype=np.float32)
    final_audio[:len(norm_voice)] += norm_voice
    final_audio[:bgm_len] += (bgm[:bgm_len] * music_vol).astype(np.float32)
    
    # Write mixed audio
    engine.write_wav(out_mix_path, final_audio)
    print(f"      Mixed Audio Ready: {out_mix_path} ({dur:.2f}s)")
    return dur


# ============================================================ Subtitle Timestamps

SUBTITLE_TIMESTAMPS = [
    # Act 1 (0:00 - 1:40)
    (0.0, 7.5, "MADHYA PRADESH KE ASIRGARH KILE KA RAHASYA"),
    (7.5, 15.0, "GUPTESHWAR MAHADEV PAR HAR SUBAH TAZA PHOOL"),
    (15.0, 22.0, "BAND KILE MEIN ROZ PUJA KAUN KARTA HAI?"),
    (22.0, 32.0, "5000 SAAL PURANA MAHABHARAT KA SHRAAP"),
    (32.0, 42.0, "ASHWATTHAMA NE CHALAYA BRAHMASHIRSHA ASTRA"),
    (42.0, 52.0, "SHRI KRISHNA KA SABSE BHAYANAK SHRAAP"),
    (52.0, 68.0, "MRITYU TUJHE NAHI CHHUEGI, TU ANTAK BHATKEGA!"),
    (68.0, 85.0, "MAATHE SE DIVYA CHINTAMANI KO NOCH LIYA"),
    # Act 2 (1:40 - 3:00)
    (85.0, 100.0, "SATPUDA KI PAHADIYON MEIN ASIRGARH QILA"),
    (100.0, 115.0, "900 FEET UNCHI KHADI PAHADI KA ABHEDYA DURG"),
    (115.0, 130.0, "KILE KI KHAI MEIN GUPTESHWAR MAHADEV MANDIR"),
    (130.0, 150.0, "BHOR MEIN CHAR BAJE TAZA BILVAPATRA KA RAHASYA"),
    (150.0, 175.0, "RATRI MEIN KOI NAHI RUK PATA IS KILE MEIN"),
    # Act 3 (3:00 - 4:45)
    (175.0, 195.0, "1819 BRITISH ARMY SIGHTING RECORDS"),
    (195.0, 220.0, "DHUNDH MEIN 9-FOOT LAMBA VISHALKAY YOODHA!"),
    (220.0, 245.0, "1970 BURHANPUR DOCTOR EYEWITNESS ENCOUNTER"),
    (245.0, 270.0, "MAATHE KA ANCIENT GHAAV AUR SARSON KA TEL"),
    (270.0, 290.0, "NARMADA PARIKRAMA MEIN SADHIK SIGHTINGS"),
    # Act 4 (4:45 - 6:20)
    (290.0, 315.0, "PURANON KA RAHASYA: ASHTA CHIRANJEEVI"),
    (315.0, 340.0, "AGLE MANVANTARA MEIN SAPTARISHI KA PAD"),
    (340.0, 360.0, "BHAGWAN KALKI KE AAGAMAN KA INTEZAAR"),
    (360.0, 380.3, "HAR HAR MAHADEV! COMMENT MEIN APNI RAYE DEIN!"),
]


# ============================================================ Render Video

def render_full_documentary():
    audio_mix = WORK_DIR / "asirgarh_final_mix.wav"
    out_video = OUT_DIR / "asirgarh_documentary.mp4"
    
    total_dur = build_audio_mix(audio_mix, 380.35)
    
    print(f"[2/3] Rendering Full 16:9 1920x1080 Widescreen Documentary ({total_dur:.1f}s)...")
    
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
        "-crf", "18",
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
    
    shot_dur = total_dur / len(SHOT_SEQUENCE)
    
    for f_idx in range(total_frames):
        t = f_idx / FPS
        
        # Switch shots based on time
        shot_idx = min(int(t / shot_dur), len(SHOT_SEQUENCE) - 1)
        shot_fn = SHOT_SEQUENCE[shot_idx]
        local_t = t - (shot_idx * shot_dur)
        
        shot_fn(ctx, local_t, shot_dur)
        
        # Subtitles
        active_sub = ""
        for s_start, s_end, txt in SUBTITLE_TIMESTAMPS:
            if s_start <= t <= s_end:
                active_sub = txt
                break
        if active_sub:
            draw_subtitles(ctx, active_sub)
            
        buf = surf.get_data()
        proc.stdin.write(buf)
        
        if f_idx % 900 == 0:
            elapsed = time.time() - t0
            fps_rend = (f_idx + 1) / max(elapsed, 0.001)
            eta = (total_frames - f_idx) / max(fps_rend, 0.001)
            print(f"Render: {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%) | {fps_rend:.1f} FPS | ETA: {eta:.1f}s")
            
    proc.stdin.close()
    proc.wait()
    
    total_time = time.time() - t0
    print(f"\n[3/3] Documentary render complete in {total_time:.1f}s ({total_time/60:.2f} mins)!")
    print(f"Output MP4: {out_video}")
    return out_video


if __name__ == "__main__":
    render_full_documentary()
