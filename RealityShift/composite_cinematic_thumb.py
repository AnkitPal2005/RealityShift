import os, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

bg_path = r'C:\Users\WottaCore - 01\.gemini\antigravity\brain\0de5c1ca-2b36-4a7b-84b9-66c16ee6d896\defense_split_screen_thumbnail_1794994781661.jpg'
out_path = Path('story-pipeline/RealityShift/output/documentary/project_kusha_thumbnail.png')
font_impact = 'C:/Windows/Fonts/impact.ttf'

base = Image.open(bg_path).convert('RGBA')
W, H = 1920, 1080
if base.size != (W, H):
    base = base.resize((W, H), Image.Resampling.LANCZOS)

def draw_text_with_outline(draw_obj, text, x, y, font, fill_color, outline_color, outline_width=6, shadow_offset=(6, 8), shadow_color=(0, 0, 0, 220)):
    if shadow_offset:
        sx, sy = shadow_offset
        draw_obj.text((x + sx, y + sy), text, font=font, fill=shadow_color, anchor='mm')
    
    if outline_width > 0:
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx*dx + dy*dy <= outline_width*outline_width:
                    draw_obj.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor='mm')
                    
    draw_obj.text((x, y), text, font=font, fill=fill_color, anchor='mm')

# 1. Subtle top and bottom dark gradient overlay for text readability
grad = Image.new('RGBA', (W, H), (0, 0, 0, 0))
g_draw = ImageDraw.Draw(grad)
for y in range(220):
    alpha = int(180 * (1.0 - y / 220.0))
    g_draw.line([(0, y), (W, y)], fill=(5, 8, 15, alpha))
for y in range(860, 1080):
    alpha = int(210 * ((y - 860) / 220.0))
    g_draw.line([(0, y), (W, y)], fill=(5, 8, 15, alpha))

base = Image.alpha_composite(base, grad)
overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# 2. Top Header Ribbon
top_font = ImageFont.truetype(font_impact, 92)
r_box = (140, 45, W - 140, 195)
draw.rounded_rectangle(r_box, radius=24, fill=(10, 14, 22, 230), outline=(255, 204, 0, 255), width=5)
draw_text_with_outline(draw, 'S-400 SE BHI DANGEROUS?', W // 2, 120, top_font, (255, 215, 0), (0, 0, 0), outline_width=8)

# 3. Left Badge (Russian S-400)
badge_font = ImageFont.truetype(font_impact, 44)
draw.rounded_rectangle((80, 270, 520, 370), radius=16, fill=(15, 18, 25, 230), outline=(255, 45, 85, 255), width=4)
draw_text_with_outline(draw, 'RUSSIAN S-400', 300, 320, badge_font, (255, 255, 255), (0, 0, 0), outline_width=5)

# 4. Right Badge (Project Kusha)
draw.rounded_rectangle((W - 520, 270, W - 80, 370), radius=16, fill=(15, 18, 25, 230), outline=(0, 229, 255, 255), width=4)
draw_text_with_outline(draw, 'PROJECT KUSHA', W - 300, 320, badge_font, (0, 229, 255), (0, 0, 0), outline_width=5)

# 5. Center VS Badge
vs_x, vs_y = W // 2, 530
draw.ellipse((vs_x - 85, vs_y - 85, vs_x + 85, vs_y + 85), fill=(10, 12, 18, 245), outline=(255, 204, 0, 255), width=6)
draw.ellipse((vs_x - 96, vs_y - 96, vs_x + 96, vs_y + 96), outline=(255, 51, 0, 200), width=4)
vs_font = ImageFont.truetype(font_impact, 88)
draw_text_with_outline(draw, 'VS', vs_x, vs_y - 2, vs_font, (255, 255, 255), (255, 23, 68), outline_width=8)

# 6. Bottom Banner (High CTR Callout)
bot_font = ImageFont.truetype(font_impact, 64)
draw.rounded_rectangle((240, 895, W - 240, 1025), radius=22, fill=(215, 0, 0, 240), outline=(255, 255, 255, 255), width=4)
draw_text_with_outline(draw, 'BHARAT KA 400 KM AIR SHIELD!', W // 2, 960, bot_font, (255, 255, 255), (0, 0, 0), outline_width=8)

final_thumb = Image.alpha_composite(base, overlay)
final_thumb.convert('RGB').save(out_path, quality=95)
print('Done!')
