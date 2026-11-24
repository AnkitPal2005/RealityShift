import os, sys, math
import cairo

base = r"c:\Users\WottaCore - 01\Desktop\Youtube-Agent\story-pipeline\BrainBlitz"
scene_path = os.path.join(base, "assets", "realistic", "mystery_scene.png")
out_dir = os.path.join(base, "output")
temp_frames = os.path.join(out_dir, "frames_riddle")
os.makedirs(temp_frames, exist_ok=True)

scene_surf = cairo.ImageSurface.create_from_png(scene_path)

W, H = 1080, 1920
FPS = 30
TOTAL_DUR = 15.0
TOTAL_FRAMES = int(TOTAL_DUR * FPS)

# Clues definitions in scene space (1080x1080)
# Scene placed in vertical canvas at Y = 280 to 1360 (size: 1080x1080)
SCENE_Y = 280

clues = [
    {"name": "2 COFFEE CUPS (HE WAS NOT ALONE!)", "cx": 730, "cy": SCENE_Y + 510, "r": 50, "reveal_t": 11.5},
    {"name": "HANDPRINT ON BROKEN WINDOW", "cx": 280, "cy": SCENE_Y + 220, "r": 70, "reveal_t": 12.5},
    {"name": "LEFT PEN VS RIGHT-HAND GUN", "cx": 520, "cy": SCENE_Y + 700, "r": 90, "reveal_t": 13.5}
]

print("Rendering Realistic Detective Riddle...")
frame_surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = cairo.Context(frame_surf)

for f_idx in range(TOTAL_FRAMES):
    t = f_idx / FPS
    
    # 1. Dark noir background
    ctx.save()
    bg = cairo.LinearGradient(0, 0, 0, H)
    bg.add_color_stop_rgb(0.0, 0.05, 0.06, 0.10)
    bg.add_color_stop_rgb(0.5, 0.02, 0.02, 0.04)
    bg.add_color_stop_rgb(1.0, 0.01, 0.01, 0.02)
    ctx.set_source(bg)
    ctx.paint()
    ctx.restore()
    
    # 2. Header: High-Stakes Detective Hook
    ctx.select_font_face("Impact", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(72)
    h_txt = "SUICIDE OR MURDER?"
    _, _, hw, hh, _, _ = ctx.text_extents(h_txt)
    # Blood red pulsing glow
    pulse = 0.8 + 0.2 * math.sin(t * 6)
    ctx.set_source_rgba(1.0, 0.15 * pulse, 0.15 * pulse, 1.0)
    ctx.move_to(W/2 - hw/2, 140)
    ctx.show_text(h_txt)
    
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(30)
    sub = "SPOT 3 CLUES BEFORE TIME RUNS OUT!"
    _, _, sw, sh, _, _ = ctx.text_extents(sub)
    ctx.set_source_rgba(1.0, 0.85, 0.2, 1.0)
    ctx.move_to(W/2 - sw/2, 210)
    ctx.show_text(sub)
    
    # 3. Main Scene Display (with slow cinematic camera push-in)
    zoom = 1.0 + 0.04 * (t / TOTAL_DUR)
    ctx.save()
    ctx.translate(W/2, SCENE_Y + 540)
    ctx.scale(zoom, zoom)
    ctx.translate(-W/2, -(SCENE_Y + 540))
    ctx.set_source_surface(scene_surf, 0, SCENE_Y)
    ctx.paint()
    ctx.restore()
    
    # Gold border around scene
    ctx.set_line_width(6)
    ctx.set_source_rgba(0.8, 0.65, 0.2, 0.8)
    ctx.rectangle(0, SCENE_Y, 1080, 1080)
    ctx.stroke()
    
    # 4. Timer Bar & Countdown (y = 1400 to 1540) - SAFE ZONE ABOVE YOUTUBE TITLE
    hud_y = 1400
    if t < 11.0:
        countdown = max(0, int(math.ceil(11.0 - t)))
        progress = max(0.0, min(1.0, (11.0 - t) / 10.0 if t >= 1.0 else 1.0))
        
        # Countdown Text
        ctx.select_font_face("Impact", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(68)
        c_txt = f"INVESTIGATING... {countdown}s"
        _, _, cw, ch, _, _ = ctx.text_extents(c_txt)
        ctx.set_source_rgba(1, 1, 1, 1)
        ctx.move_to(W/2 - cw/2, hud_y + 45)
        ctx.show_text(c_txt)
        
        # Red/Gold Progress Bar
        bar_w = 600
        bar_h = 16
        bx = (W - bar_w) / 2
        by = hud_y + 75
        ctx.set_source_rgba(0.2, 0.15, 0.15, 0.8)
        ctx.rectangle(bx, by, bar_w, bar_h); ctx.fill()
        
        fill_w = bar_w * progress
        ctx.set_source_rgba(1.0, 0.2 + 0.6*progress, 0.1, 1.0)
        ctx.rectangle(bx, by, fill_w, bar_h); ctx.fill()
    else:
        # Reveal Mode
        ctx.select_font_face("Impact", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(62)
        r_txt = "IT WAS A MURDER! 3 CLUES:"
        _, _, rw, rh, _, _ = ctx.text_extents(r_txt)
        ctx.set_source_rgba(1.0, 0.2, 0.2, 1.0)
        ctx.move_to(W/2 - rw/2, hud_y + 40)
        ctx.show_text(r_txt)
        
        ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(28)
        ans_txt = "Window forced + 2nd cup with lipstick!"
        _, _, aw, ah, _, _ = ctx.text_extents(ans_txt)
        ctx.set_source_rgba(1.0, 0.9, 0.2, 1.0)
        ctx.move_to(W/2 - aw/2, hud_y + 85)
        ctx.show_text(ans_txt)

    # 5. Glowing Magnifying Glass / Red Target Rings on Clues
    for idx, c in enumerate(clues):
        if t >= c["reveal_t"]:
            pop = min(1.0, (t - c["reveal_t"]) * 5.0)
            cx_coord = c["cx"]
            cy_coord = c["cy"]
            rad = c["r"] * (1.0 + 0.25 * (1.0 - pop))
            
            # Glowing Clue Ring
            ctx.set_line_width(6)
            ctx.set_source_rgba(1.0, 0.1, 0.1, 0.95)
            ctx.arc(cx_coord, cy_coord, rad, 0, 2*math.pi)
            ctx.stroke()
            
            # Badge Label
            ctx.select_font_face("Impact", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            ctx.set_font_size(24)
            lbl = f"CLUE #{idx+1}"
            _, _, lw, lh, _, _ = ctx.text_extents(lbl)
            
            ctx.set_source_rgba(0.9, 0.1, 0.1, 0.9)
            ctx.rectangle(cx_coord - lw/2 - 10, cy_coord - rad - 35, lw + 20, 28)
            ctx.fill()
            
            ctx.set_source_rgba(1, 1, 1, 1)
            ctx.move_to(cx_coord - lw/2, cy_coord - rad - 14)
            ctx.show_text(lbl)

    # Save frame
    frame_path = os.path.join(temp_frames, f"frame_{f_idx:04d}.png")
    frame_surf.write_to_png(frame_path)

print("Realistic Riddle frames generated successfully!")
