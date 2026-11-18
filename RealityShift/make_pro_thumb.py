"""High-CTR Cinematic Thumbnail Generator for Project Kusha vs S-400.
Widescreen 16:9 (1920x1080).
"""

import math
import cairo
from pathlib import Path

W, H = 1920, 1080

def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))

GOLD = hexc("#FFCC00")
AMBER = hexc("#FF9900")
FIRE = hexc("#FF3300")
RED = hexc("#FF1744")
CYAN = hexc("#00E5FF")
GREEN = hexc("#00E676")
WHITE = (1.0, 1.0, 1.0)
BLACK = (0.0, 0.0, 0.0)
DARK_BG = hexc("#080B12")
STEEL = hexc("#B0BEC5")
SAFFRON = hexc("#FF6F00")

def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()

def circle(ctx, cx, cy, r, c, a=1.0, fill=True, w=2):
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.set_source_rgba(c[0], c[1], c[2], a)
    if fill:
        ctx.fill()
    else:
        ctx.set_line_width(w)
        ctx.stroke()

def line(ctx, pts, c, w=2, a=1.0, dash=None):
    if len(pts) < 2:
        return
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.set_source_rgba(c[0], c[1], c[2], a)
    ctx.set_line_width(w)
    if dash:
        ctx.set_dash(dash)
    ctx.stroke()
    ctx.set_dash([])

def draw_bold_text(ctx, text, x, y, size=80, c=WHITE, stroke_c=BLACK, stroke_w=8, font="Impact"):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)
    ext = ctx.text_extents(text)
    tx = x - ext.width / 2 - ext.x_bearing
    ty = y - ext.height / 2 - ext.y_bearing
    
    # Deep Shadow
    ctx.move_to(tx + 6, ty + 8)
    ctx.set_source_rgba(0, 0, 0, 0.9)
    ctx.show_text(text)
    
    # Outer Stroke
    if stroke_w > 0:
        ctx.move_to(tx, ty)
        ctx.text_path(text)
        ctx.set_source_rgba(stroke_c[0], stroke_c[1], stroke_c[2], 1.0)
        ctx.set_line_width(stroke_w)
        ctx.stroke()
        
    # Main Fill
    ctx.move_to(tx, ty)
    ctx.set_source_rgba(c[0], c[1], c[2], 1.0)
    ctx.show_text(text)

def generate_pro_thumbnail():
    out_path = Path("story-pipeline/RealityShift/output/documentary/project_kusha_thumbnail.png")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    
    # 1. Base Dark Tactical Gradient
    g_bg = cairo.LinearGradient(0, 0, 0, H)
    g_bg.add_color_stop_rgb(0, *hexc("#0A0F1D"))
    g_bg.add_color_stop_rgb(1, *hexc("#030508"))
    ctx.set_source(g_bg)
    ctx.paint()
    
    # 2. Left Red/Amber Battlefield Glow (S-400 side)
    g_left = cairo.RadialGradient(300, 540, 50, 300, 540, 750)
    g_left.add_color_stop_rgba(0, 0.85, 0.15, 0.05, 0.55)
    g_left.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    ctx.set_source(g_left)
    ctx.paint()
    
    # 3. Right Gold/Cyan Divine Tech Glow (Kusha side)
    g_right = cairo.RadialGradient(1600, 540, 50, 1600, 540, 750)
    g_right.add_color_stop_rgba(0, 0.0, 0.75, 0.95, 0.45)
    g_right.add_color_stop_rgba(0.5, 0.95, 0.75, 0.1, 0.3)
    g_right.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    ctx.set_source(g_right)
    ctx.paint()
    
    # 4. Diagonal Lightning / Energy Split in the middle
    fissure = [(980, 0), (950, 280), (990, 480), (930, 720), (970, 1080)]
    line(ctx, fissure, WHITE, 8, 0.9)
    line(ctx, fissure, GOLD, 18, 0.5)
    line(ctx, fissure, CYAN, 36, 0.25)
    
    # 5. LEFT SIDE: Russian S-400 Launcher
    lx, ly = 440, 760
    # Mountain / Terrain backdrop
    line(ctx, [(0, 850), (250, 780), (600, 840), (950, 760), (950, 1080), (0, 1080)], (0.05, 0.07, 0.1), 2)
    ctx.set_source_rgb(0.04, 0.06, 0.09)
    ctx.fill()
    
    # S-400 Truck Chassis
    rrect(ctx, lx - 300, ly - 30, 600, 90, 12)
    ctx.set_source_rgb(0.18, 0.22, 0.20)
    ctx.fill()
    # 8x8 Wheels
    for wx in [-240, -160, -80, 80, 160, 240]:
        circle(ctx, lx + wx, ly + 65, 38, (0.08, 0.09, 0.11))
        circle(ctx, lx + wx, ly + 65, 20, STEEL)
        
    # S-400 Vertical Canisters (Elevated 55 degrees)
    ctx.save()
    ctx.translate(lx - 120, ly - 30)
    ctx.rotate(-math.radians(55))
    # 4 Tubes
    rrect(ctx, 0, -65, 480, 130, 14)
    ctx.set_source_rgb(0.24, 0.28, 0.26)
    ctx.fill()
    ctx.set_line_width(4)
    ctx.set_source_rgb(*AMBER)
    ctx.stroke()
    # Canister caps
    circle(ctx, 480, -35, 25, FIRE)
    circle(ctx, 480, 35, 25, FIRE)
    ctx.restore()
    
    # S-400 Badge & Flag on Left
    rrect(ctx, 100, 280, 480, 110, 16)
    ctx.set_source_rgba(0.05, 0.05, 0.08, 0.95)
    ctx.fill()
    rrect(ctx, 100, 280, 480, 110, 16)
    ctx.set_source_rgba(FIRE[0], FIRE[1], FIRE[2], 0.9)
    ctx.set_line_width(4)
    ctx.stroke()
    draw_bold_text(ctx, "RUSSIAN S-400", 340, 335, size=48, c=WHITE, stroke_w=4)
    
    # 6. RIGHT SIDE: DRDO Project Kusha Hypersonic Interceptor
    rx, ry = 1480, 780
    # Launchpad platform
    rrect(ctx, rx - 320, ry - 10, 640, 100, 14)
    ctx.set_source_rgb(0.12, 0.16, 0.22)
    ctx.fill()
    # Big Kusha 3-Tier Hypersonic Rocket ascending at 65 degrees!
    ctx.save()
    ctx.translate(rx - 80, ry - 30)
    ctx.rotate(-math.radians(65))
    
    # Massive Rocket Exhaust Flame & Smoke Plume
    g_flame = cairo.RadialGradient(-120, 0, 20, -120, 0, 300)
    g_flame.add_color_stop_rgba(0, 1, 1, 1, 1)
    g_flame.add_color_stop_rgba(0.3, 1, 0.7, 0, 0.9)
    g_flame.add_color_stop_rgba(0.7, 1, 0.2, 0, 0.6)
    g_flame.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g_flame)
    circle(ctx, -140, 0, 200, FIRE)
    
    # Rocket Body
    rrect(ctx, 0, -45, 580, 90, 12)
    ctx.set_source_rgb(0.92, 0.95, 0.98) # Pristine White body
    ctx.fill()
    # Saffron stripe on missile
    rrect(ctx, 100, -45, 70, 90, 0)
    ctx.set_source_rgb(*SAFFRON)
    ctx.fill()
    # Green stripe on missile
    rrect(ctx, 170, -45, 70, 90, 0)
    ctx.set_source_rgb(*GREEN)
    ctx.fill()
    # Nosecone Tip
    line(ctx, [(580, -45), (680, 0), (580, 45)], GOLD, 4)
    ctx.set_source_rgb(*GOLD)
    ctx.fill()
    # Grid fins
    line(ctx, [(20, -45), (-40, -110)], STEEL, 8)
    line(ctx, [(20, 45), (-40, 110)], STEEL, 8)
    ctx.restore()
    
    # Project Kusha Badge & Flag on Right
    rrect(ctx, 1340, 280, 500, 110, 16)
    ctx.set_source_rgba(0.04, 0.08, 0.15, 0.95)
    ctx.fill()
    rrect(ctx, 1340, 280, 500, 110, 16)
    ctx.set_source_rgba(GOLD[0], GOLD[1], GOLD[2], 0.95)
    ctx.set_line_width(4)
    ctx.stroke()
    draw_bold_text(ctx, "PROJECT KUSHA", 1590, 335, size=48, c=GOLD, stroke_w=4)
    
    # 7. TOP CORNER TARGET LOCK: J-20 in reticle
    tx, ty = 1400, 160
    circle(ctx, tx, ty, 60, RED, 0.8, fill=False, w=3)
    line(ctx, [(tx - 80, ty), (tx + 80, ty)], RED, 2, 0.8)
    line(ctx, [(tx, ty - 80), (tx, ty + 80)], RED, 2, 0.8)
    draw_bold_text(ctx, "J-20 STEALTH LOCKED!", tx, ty + 85, size=22, c=RED, stroke_w=3)
    
    # 8. CENTER BIG "VS" EMBLEM
    circle(ctx, 960, 520, 90, (0.05, 0.07, 0.12), 1.0)
    circle(ctx, 960, 520, 90, GOLD, 1.0, fill=False, w=6)
    circle(ctx, 960, 520, 102, FIRE, 0.8, fill=False, w=3)
    draw_bold_text(ctx, "VS", 960, 520, size=86, c=WHITE, stroke_c=FIRE, stroke_w=8)
    
    # 9. TOP ULTRA-HOOK TITLE (Massive 3D Typography)
    # Background ribbon for contrast
    rrect(ctx, 160, 50, W - 320, 150, 24)
    ctx.set_source_rgba(0.02, 0.03, 0.06, 0.95)
    ctx.fill()
    rrect(ctx, 160, 50, W - 320, 150, 24)
    ctx.set_source_rgba(GOLD[0], GOLD[1], GOLD[2], 0.9)
    ctx.set_line_width(4)
    ctx.stroke()
    
    draw_bold_text(ctx, "S-400 SE BHI DANGEROUS?", W / 2, 125, size=86, c=GOLD, stroke_c=BLACK, stroke_w=10)
    
    # 10. BOTTOM HIGHLIGHT BADGE (High CTR Punch)
    rrect(ctx, 280, 890, W - 560, 130, 24)
    # Glowing red/orange banner
    g_bar = cairo.LinearGradient(280, 0, W - 280, 0)
    g_bar.add_color_stop_rgb(0, *hexc("#D50000"))
    g_bar.add_color_stop_rgb(0.5, *hexc("#FF3D00"))
    g_bar.add_color_stop_rgb(1, *hexc("#D50000"))
    ctx.set_source(g_bar)
    ctx.fill()
    rrect(ctx, 280, 890, W - 560, 130, 24)
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(4)
    ctx.stroke()
    
    draw_bold_text(ctx, "BHARAT KA 400 KM AIR SHIELD! 🇮🇳", W / 2, 955, size=64, c=WHITE, stroke_c=BLACK, stroke_w=8)
    
    surf.write_to_png(str(out_path))
    print("New high-CTR professional thumbnail generated successfully at:", out_path)
    return out_path

if __name__ == "__main__":
    generate_pro_thumbnail()
