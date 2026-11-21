"""Create the ultimate 16:9 YouTube Master Thumbnail for Asirgarh Documentary
using the generated Little Krishna 3D CGI background.
"""

import cairo
import numpy as np
from pathlib import Path
from PIL import Image

W, H = 1920, 1080

def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -1.5707963, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, 1.5707963)
    ctx.arc(x + r, y + h - r, r, 1.5707963, 3.1415926)
    ctx.arc(x + r, y + r, r, 3.1415926, 4.7123889)
    ctx.close_path()

def create_master_thumbnail():
    bg_path = Path("story-pipeline/SanatanKatha/output/documentary/scenes/thumb_bg.jpg")
    out_path = Path("story-pipeline/SanatanKatha/output/documentary/asirgarh_thumbnail.png")
    brain_path = Path(r"C:\Users\WottaCore - 01\.gemini\antigravity\brain\0de5c1ca-2b36-4a7b-84b9-66c16ee6d896\asirgarh_thumbnail.png")
    
    # Load 3D background image
    im = Image.open(bg_path).convert("RGBA").resize((W, H), Image.Resampling.LANCZOS)
    arr = np.array(im)
    # Convert RGBA to BGRA for Cairo
    bgra = arr[:, :, [2, 1, 0, 3]].copy()
    
    surf = cairo.ImageSurface.create_for_data(bgra, cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    
    # Subtle dark gradient at top and bottom to make thumbnail text POP
    top_g = cairo.LinearGradient(0, 0, 0, 260)
    top_g.add_color_stop_rgba(0, 0, 0, 0, 0.75)
    top_g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    ctx.rectangle(0, 0, W, 260)
    ctx.set_source(top_g)
    ctx.fill()
    
    bot_g = cairo.LinearGradient(0, H - 320, 0, H)
    bot_g.add_color_stop_rgba(0, 0, 0, 0, 0.0)
    bot_g.add_color_stop_rgba(1, 0, 0, 0, 0.85)
    ctx.rectangle(0, H - 320, W, 320)
    ctx.set_source(bot_g)
    ctx.fill()
    
    # Typography: High-Contrast Bold Impact
    ctx.select_font_face("Impact", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    
    # Badge: "5000 SAAL PURANA SHRAAP"
    ctx.set_font_size(65)
    t1 = "5000 SAAL PURANA SHRAAP"
    ext1 = ctx.text_extents(t1)
    bx = W / 2 - ext1.width / 2
    by = 130
    
    # Crimson Badge Pill
    rrect(ctx, bx - 30, by - ext1.height - 18, ext1.width + 60, ext1.height + 38, 16)
    ctx.set_source_rgba(0.85, 0.10, 0.15, 0.95)
    ctx.fill()
    rrect(ctx, bx - 30, by - ext1.height - 18, ext1.width + 60, ext1.height + 38, 16)
    ctx.set_source_rgba(1.0, 0.85, 0.25, 1.0)
    ctx.set_line_width(4)
    ctx.stroke()
    
    ctx.move_to(bx, by)
    ctx.text_path(t1)
    ctx.set_source_rgba(0.1, 0.02, 0.02, 1.0)
    ctx.set_line_width(10)
    ctx.stroke_preserve()
    ctx.set_source_rgba(1.0, 0.95, 0.8, 1.0)
    ctx.fill()
    
    # Main Hook: "AAJ BHI ZINDA?" (Colossal Font Size 140)
    ctx.set_font_size(140)
    t2 = "AAJ BHI ZINDA?"
    ext2 = ctx.text_extents(t2)
    lx = W / 2 - ext2.width / 2
    ly = H - 80
    
    # Drop shadow
    ctx.move_to(lx + 8, ly + 8)
    ctx.text_path(t2)
    ctx.set_source_rgba(0.05, 0.02, 0.02, 0.95)
    ctx.set_line_width(24)
    ctx.stroke()
    
    # Crimson Outer Border
    ctx.move_to(lx, ly)
    ctx.text_path(t2)
    ctx.set_source_rgba(0.85, 0.08, 0.15, 1.0)
    ctx.set_line_width(18)
    ctx.stroke_preserve()
    
    # White Inner Border
    ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
    ctx.set_line_width(6)
    ctx.stroke_preserve()
    
    # Radiant Yellow-Gold Gradient Fill
    yg = cairo.LinearGradient(0, ly - ext2.height, 0, ly)
    yg.add_color_stop_rgb(0, 1.0, 1.0, 0.6)
    yg.add_color_stop_rgb(0.5, 1.0, 0.82, 0.1)
    yg.add_color_stop_rgb(1.0, 1.0, 0.55, 0.05)
    ctx.set_source(yg)
    ctx.fill()
    
    # Save Image
    out_path.parent.mkdir(parents=True, exist_ok=True)
    surf.write_to_png(str(out_path))
    surf.write_to_png(str(brain_path))
    print(f"Master 3D Thumbnail Created: {out_path}")

if __name__ == "__main__":
    create_master_thumbnail()
