"""Render an ultra-vibrant, colorful 16:9 YouTube Thumbnail for Asirgarh Documentary.
Zero black silhouettes, zero dark voids - rich, vibrant, warm golden-orange, emerald green,
and divine temple colors.
"""

import math
import cairo
import numpy as np
from pathlib import Path

W, H = 1920, 1080

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

def line(ctx, pts, c, w=2, a=1.0):
    if len(pts) < 2:
        return
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    rgba(ctx, c, a)
    ctx.set_line_width(w)
    ctx.stroke()

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

def render_colorful_thumbnail():
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    
    # 1. Vibrant Sunset / Twilight Sky Gradient (Rich Purple to Fiery Orange to Golden Yellow)
    sky = cairo.LinearGradient(0, 0, 0, H)
    sky.add_color_stop_rgb(0.0, 0.28, 0.12, 0.45)   # Deep Royal Purple
    sky.add_color_stop_rgb(0.35, 0.75, 0.22, 0.35)  # Crimson Magenta
    sky.add_color_stop_rgb(0.65, 0.98, 0.45, 0.12)  # Fiery Sunset Orange
    sky.add_color_stop_rgb(1.0, 1.0, 0.78, 0.25)   # Radiant Warm Gold
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(sky)
    ctx.fill()
    
    # Rising Golden Moon / Sun disc in upper center
    glow(ctx, 1050, 240, 380, (1.0, 0.85, 0.4), 0.65)
    circle(ctx, 1050, 240, 110, (1.0, 0.96, 0.82))
    
    # 2. Lush Satpura Mountain Ridges (Emerald Greens and Forest Tones)
    # Ridge 1 (Far - Blue green)
    ctx.move_to(0, H)
    for x in range(0, W + 1, 40):
        ctx.line_to(x, 480 + 35 * math.sin(x / 140))
    ctx.line_to(W, H)
    ctx.close_path()
    rgba(ctx, (0.18, 0.38, 0.42))
    ctx.fill()
    
    # Ridge 2 (Mid - Emerald Forest)
    ctx.move_to(0, H)
    for x in range(0, W + 1, 40):
        ctx.line_to(x, 560 + 45 * math.cos(x / 180))
    ctx.line_to(W, H)
    ctx.close_path()
    rgba(ctx, (0.12, 0.45, 0.28))
    ctx.fill()

    # 3. Asirgarh Fortress Ramparts (Warm Ancient Sandstone & Gold Highlights)
    fort_y = 520
    # Fort plateau rock base
    ctx.move_to(650, H)
    ctx.line_to(750, fort_y + 120)
    ctx.line_to(920, fort_y)
    ctx.line_to(1800, fort_y)
    ctx.line_to(1920, fort_y + 80)
    ctx.line_to(1920, H)
    ctx.close_path()
    rgba(ctx, (0.55, 0.42, 0.28)) # Warm Sandstone
    ctx.fill()
    
    # Fort rampart battlements (Kanguras)
    for bx in range(920, 1820, 45):
        rrect(ctx, bx, fort_y - 28, 28, 35, 4)
        rgba(ctx, (0.68, 0.52, 0.35))
        ctx.fill()
        # Highlight on top of stones
        line(ctx, [(bx, fort_y - 28), (bx + 28, fort_y - 28)], (0.9, 0.75, 0.5), 3)

    # Watchtower Burj with glowing torch
    tx = 1380
    rrect(ctx, tx - 45, fort_y - 120, 90, 130, 14)
    rgba(ctx, (0.62, 0.48, 0.32))
    ctx.fill()
    # Domed cupola
    circle(ctx, tx, fort_y - 120, 48, (0.75, 0.58, 0.38))
    # Glowing window
    glow(ctx, tx, fort_y - 70, 75, (1.0, 0.45, 0.05), 0.8)
    rrect(ctx, tx - 15, fort_y - 85, 30, 42, 10)
    rgba(ctx, (1.0, 0.88, 0.3))
    ctx.fill()

    # 4. Sacred Ancient Gupteshwar Mahadev Sanctum on the RIGHT
    # Sandstone archway pillar framing the right
    rrect(ctx, 1260, 280, 620, 780, 40)
    rgba(ctx, (0.48, 0.36, 0.24), 0.92)
    ctx.fill()
    rrect(ctx, 1260, 280, 620, 780, 40)
    rgba(ctx, (0.85, 0.65, 0.35))
    ctx.set_line_width(8)
    ctx.stroke()
    
    # Inner Sanctum warm golden divine glow
    glow(ctx, 1570, 680, 380, (1.0, 0.65, 0.15), 0.75)
    glow(ctx, 1570, 680, 220, (1.0, 0.88, 0.45), 0.9)
    
    # Sacred Stone Pedestal (Yoni Peetham)
    base_x, base_y = 1570, 840
    rrect(ctx, base_x - 220, base_y, 440, 140, 20)
    rgba(ctx, (0.32, 0.34, 0.38))
    ctx.fill()
    line(ctx, [(base_x - 220, base_y), (base_x + 220, base_y)], (0.6, 0.65, 0.7), 6)
    
    # Shivling (Deep Polished Granite with Golden Highlights)
    sl_w, sl_h = 150, 280
    rrect(ctx, base_x - sl_w/2, base_y - sl_h + 60, sl_w, sl_h, 72)
    rgba(ctx, (0.18, 0.20, 0.25))
    ctx.fill_preserve()
    rgba(ctx, (0.6, 0.7, 0.85), 0.7)
    ctx.set_line_width(5)
    ctx.stroke()
    
    # Polished specular light sheen on Shivling
    rrect(ctx, base_x - sl_w/2 + 15, base_y - sl_h + 65, 25, sl_h - 50, 12)
    rgba(ctx, (1.0, 1.0, 1.0), 0.35)
    ctx.fill()
    
    # Sacred White Sandalwood (Chandan) Tripundra & Red Kumkum
    for ty in (-150, -135, -120):
        line(ctx, [(base_x - 40, base_y + ty), (base_x + 40, base_y + ty)], (1.0, 0.98, 0.92), 7)
    circle(ctx, base_x, base_y - 135, 10, (0.9, 0.12, 0.15))
    
    # Vibrant Yellow Marigold (Genda) Garland around Shivling base!
    for mx in range(-120, 130, 28):
        my = base_y + 15 + 10 * math.sin(mx / 30)
        circle(ctx, base_x + mx, my, 18, (1.0, 0.72, 0.05))
        circle(ctx, base_x + mx, my, 12, (1.0, 0.45, 0.02))
        circle(ctx, base_x + mx, my, 5, (1.0, 0.9, 0.3))

    # Bright Fresh Red Hibiscus (Gudhal) Flower on top of Shivling!
    fl_y = base_y - sl_h + 60
    glow(ctx, base_x, fl_y, 110, (1.0, 0.15, 0.25), 0.8)
    for ang in range(0, 360, 72):
        rad = math.radians(ang)
        circle(ctx, base_x + 26 * math.cos(rad), fl_y + 26 * math.sin(rad), 20, (0.95, 0.08, 0.15))
    circle(ctx, base_x, fl_y, 12, (1.0, 0.85, 0.2)) # Golden pollen
    circle(ctx, base_x - 8, fl_y - 8, 4, (1.0, 1.0, 1.0), a=0.95) # Dewdrop
    
    # Bright Green Bilva (Bel) Leaves on Shivling
    for lx, ly in [(-35, base_y - 60), (35, base_y - 70), (0, base_y - 30)]:
        circle(ctx, base_x + lx, ly, 16, (0.15, 0.75, 0.35))
        line(ctx, [(base_x + lx - 10, ly), (base_x + lx + 10, ly)], (0.1, 0.5, 0.2), 3)

    # Brass Diyas with dancing bright flame on left and right of Shivling
    for dx in (base_x - 170, base_x + 170):
        # Brass bowl
        rrect(ctx, dx - 25, base_y + 40, 50, 24, 8)
        rgba(ctx, (0.9, 0.72, 0.15))
        ctx.fill()
        # Bright flame
        glow(ctx, dx, base_y + 25, 60, (1.0, 0.5, 0.05), 0.85)
        circle(ctx, dx, base_y + 30, 14, (1.0, 0.85, 0.1))
        circle(ctx, dx, base_y + 24, 7, (1.0, 1.0, 0.8))

    # 5. Colorful, Towering Ashwatthama Warrior on the LEFT (NO BLACK SILHOUETTE!)
    # Imposing, Muscular, Saffron & Gold Warrior
    ash_x = 420
    ash_y = 650
    
    # Divine / Haunting Golden-Crimson Aura behind Ashwatthama
    glow(ctx, ash_x, ash_y - 120, 340, (1.0, 0.45, 0.12), 0.55)
    glow(ctx, ash_x, ash_y - 240, 220, (0.9, 0.15, 0.2), 0.7)
    
    # Muscular Chest & Shoulders in Golden Kavach Armor
    # Saffron Angavastra / Cape flowing behind
    smooth(ctx, [(ash_x - 180, ash_y + 280), (ash_x - 160, ash_y - 80), 
                 (ash_x + 160, ash_y - 80), (ash_x + 190, ash_y + 280)], closed=True)
    rgba(ctx, (0.95, 0.42, 0.08)) # Radiant Saffron Cape
    ctx.fill()
    
    # Warrior Golden Armored Torso
    rrect(ctx, ash_x - 110, ash_y - 70, 220, 240, 30)
    rgba(ctx, (0.85, 0.65, 0.18)) # Polished Gold Armor
    ctx.fill_preserve()
    rgba(ctx, (0.55, 0.38, 0.08))
    ctx.set_line_width(6)
    ctx.stroke()
    # Armor muscle lines & Royal engravings
    circle(ctx, ash_x - 45, ash_y + 20, 35, (0.75, 0.55, 0.12), fill=False, w=4)
    circle(ctx, ash_x + 45, ash_y + 20, 35, (0.75, 0.55, 0.12), fill=False, w=4)
    line(ctx, [(ash_x, ash_y - 60), (ash_x, ash_y + 120)], (0.75, 0.55, 0.12), 5)
    
    # Royal Golden Neck Armor / Hansuli
    smooth(ctx, [(ash_x - 70, ash_y - 65), (ash_x + 70, ash_y - 65), 
                 (ash_x + 45, ash_y - 30), (ash_x - 45, ash_y - 30)], closed=True)
    rgba(ctx, (1.0, 0.85, 0.35))
    ctx.fill()
    
    # Muscular Warrior Neck & Face (Rich Wheatish Warrior Skin)
    rrect(ctx, ash_x - 42, ash_y - 120, 84, 70, 16)
    rgba(ctx, (0.78, 0.58, 0.44)) # Warrior Skin
    ctx.fill()
    
    # Face & Head
    circle(ctx, ash_x, ash_y - 170, 82, (0.82, 0.62, 0.48))
    # Intense Warrior Jawline
    smooth(ctx, [(ash_x - 72, ash_y - 170), (ash_x - 45, ash_y - 95), 
                 (ash_x + 45, ash_y - 95), (ash_x + 72, ash_y - 170)], closed=True)
    rgba(ctx, (0.75, 0.55, 0.42))
    ctx.fill()
    
    # Intense Warrior Beard and Mustache
    smooth(ctx, [(ash_x - 65, ash_y - 150), (ash_x - 30, ash_y - 88), 
                 (ash_x + 30, ash_y - 88), (ash_x + 65, ash_y - 150),
                 (ash_x + 40, ash_y - 130), (ash_x - 40, ash_y - 130)], closed=True)
    rgba(ctx, (0.28, 0.20, 0.16)) # Dark Brown Beard
    ctx.fill()
    
    # Fierce Glowing Warrior Eyes
    for ex in (ash_x - 32, ash_x + 32):
        circle(ctx, ex, ash_y - 175, 12, (1.0, 1.0, 1.0))
        circle(ctx, ex, ash_y - 175, 6, (0.85, 0.15, 0.15)) # Glowing Crimson Iris
        circle(ctx, ex - 2, ash_y - 177, 2.5, (1.0, 1.0, 1.0)) # Eye sparkle
        # Intense Eyebrow
        line(ctx, [(ex - 18, ash_y - 192), (ex + 18, ash_y - 188)], (0.2, 0.15, 0.12), 6)
        
    # Long Flowing Warrior Hair (Matted Jatas with Red Headband)
    for hx, hy in [(-85, -120), (-95, -60), (-75, 20), (85, -120), (95, -60), (75, 20)]:
        circle(ctx, ash_x + hx, ash_y + hy, 28, (0.24, 0.18, 0.14))
    # Red Warrior Headband (Pattika)
    smooth(ctx, [(ash_x - 82, ash_y - 200), (ash_x + 82, ash_y - 200), 
                 (ash_x + 82, ash_y - 225), (ash_x - 82, ash_y - 225)], closed=True)
    rgba(ctx, (0.85, 0.12, 0.18))
    ctx.fill()
    
    # THE SACRED CRATER: Unhealing Crimson Gem Wound on Forehead!
    wound_x, wound_y = ash_x, ash_y - 212
    # Radiating holy/cursed energy
    glow(ctx, wound_x, wound_y, 140, (1.0, 0.1, 0.15), 0.9)
    glow(ctx, wound_x, wound_y, 65, (1.0, 0.45, 0.2), 1.0)
    circle(ctx, wound_x, wound_y, 22, (0.75, 0.05, 0.08)) # Crater edge
    circle(ctx, wound_x, wound_y, 12, (0.35, 0.02, 0.02)) # Deep cavity
    circle(ctx, wound_x, wound_y, 6, (1.0, 0.95, 0.4))   # Spark of eternal energy
    
    # Dripping crimson tear lines
    line(ctx, [(wound_x - 12, wound_y + 18), (wound_x - 16, wound_y + 65)], (0.8, 0.08, 0.12), 4)
    line(ctx, [(wound_x + 12, wound_y + 18), (wound_x + 18, wound_y + 80)], (0.8, 0.08, 0.12), 4)
    
    # Giant Bow (Kodanda/Dhanush) on his shoulder
    bow_pts = [(ash_x - 140, ash_y - 360), (ash_x - 180, ash_y - 120), 
               (ash_x - 170, ash_y + 160), (ash_x - 120, ash_y + 380)]
    line(ctx, bow_pts, (0.75, 0.55, 0.20), 18)
    line(ctx, bow_pts, (1.0, 0.85, 0.40), 6) # Gold trim on bow
    # Bowstring
    line(ctx, [(ash_x - 140, ash_y - 360), (ash_x - 120, ash_y + 380)], (0.95, 0.95, 1.0), 3)

    # 6. Ultra-High Retention Thumbnail Text in Center-Left: "AAJ BHI ZINDA?"
    # Placed in bold, vibrant 3-tier colors with heavy contrast drop-shadow
    ctx.save()
    ctx.select_font_face("Impact", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    
    # Line 1: "5000 SAAL PURANA" (Yellow-Gold with Crimson Outline)
    ctx.set_font_size(68)
    l1_text = "5000 SAAL PURANA"
    l1_ext = ctx.text_extents(l1_text)
    l1_x = 980 - l1_ext.width / 2
    l1_y = 120
    
    # Badge backdrop for Line 1
    rrect(ctx, l1_x - 30, l1_y - l1_ext.height - 15, l1_ext.width + 60, l1_ext.height + 35, 16)
    rgba(ctx, (0.85, 0.12, 0.18), 0.92) # Radiant Crimson Badge
    ctx.fill()
    rrect(ctx, l1_x - 30, l1_y - l1_ext.height - 15, l1_ext.width + 60, l1_ext.height + 35, 16)
    rgba(ctx, (1.0, 0.85, 0.25))
    ctx.set_line_width(4)
    ctx.stroke()
    
    ctx.move_to(l1_x, l1_y)
    ctx.text_path(l1_text)
    rgba(ctx, (0.2, 0.02, 0.02))
    ctx.set_line_width(10)
    ctx.stroke_preserve()
    rgba(ctx, (1.0, 0.95, 0.8))
    ctx.fill()
    
    # Line 2: "AAJ BHI ZINDA?" (Colossal Font Size 135, Radiant Golden Yellow, 3D Pop!)
    ctx.set_font_size(135)
    l2_text = "AAJ BHI ZINDA?"
    l2_ext = ctx.text_extents(l2_text)
    l2_x = W / 2 - l2_ext.width / 2 + 60
    l2_y = 960
    
    # Shadow offset
    ctx.move_to(l2_x + 8, l2_y + 8)
    ctx.text_path(l2_text)
    rgba(ctx, (0.1, 0.02, 0.02), 0.9)
    ctx.set_line_width(22)
    ctx.stroke()
    
    # Outer Crimson Glow Stroke
    ctx.move_to(l2_x, l2_y)
    ctx.text_path(l2_text)
    rgba(ctx, (0.85, 0.08, 0.15))
    ctx.set_line_width(18)
    ctx.stroke_preserve()
    
    # Inner White Border
    rgba(ctx, (1.0, 1.0, 1.0))
    ctx.set_line_width(6)
    ctx.stroke_preserve()
    
    # Radiant Yellow-Gold Fill
    yg = cairo.LinearGradient(0, l2_y - l2_ext.height, 0, l2_y)
    yg.add_color_stop_rgb(0, 1.0, 0.98, 0.6)  # Bright White-Gold top
    yg.add_color_stop_rgb(0.5, 1.0, 0.82, 0.1) # Pure Gold mid
    yg.add_color_stop_rgb(1.0, 1.0, 0.55, 0.05) # Deep Golden-Orange bottom
    ctx.set_source(yg)
    ctx.fill()
    
    ctx.restore()
    
    # Save Image
    out_path = Path("story-pipeline/SanatanKatha/output/documentary/asirgarh_thumbnail.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    surf.write_to_png(str(out_path))
    print(f"Colorful Thumbnail Rendered Successfully: {out_path}")

if __name__ == "__main__":
    render_colorful_thumbnail()
