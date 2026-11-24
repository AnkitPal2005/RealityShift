import os, sys, math, random, subprocess, wave
import numpy as np
import cairo

BASE = r"c:\Users\WottaCore - 01\Desktop\Youtube-Agent\story-pipeline\BrainBlitz"
NAME = "spot_diff_02_cyber_ramen"
OUT = os.path.join(BASE, "output", NAME)
os.makedirs(OUT, exist_ok=True)

W, H, FPS, DUR = 1080, 1920, 30, 16.0
PX, PW, PH = 60, 960, 640
PA_Y, PB_Y = 250, 930
PUZZLE_END = 10.0
FONT = "Impact"

# 3 Differences on Panel B:
# (local x, local y, r, reveal_t, tag)
DIFFS = [
    (310, 230, 65, 11.0, "EASY"),                    # Diff 1: Neon Lantern Symbol
    (670, 350, 70, 12.1, "MEDIUM"),                  # Diff 2: Cyber Cat Mask Visor Color (Cyan vs Pink)
    (480, 480, 50, 13.2, "99% FAILED THIS!"),        # Diff 3: Ramen Bowl Topping (Naruto Swirl vs Boiled Egg)
]

def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))

def ease_out_back(x):
    c1, c3 = 1.70158, 2.70158
    x = clamp(x)
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()

def lin(ctx, x0, y0, x1, y1, stops):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    for o, c in stops:
        g.add_color_stop_rgba(o, *c) if len(c) == 4 else g.add_color_stop_rgb(o, *c)
    return g

def text_c(ctx, s, cx, cy, size, fill, stroke=(0, 0, 0), sw=10, scale=1.0, alpha=1.0):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(scale, scale)
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    xb, yb, tw, th, _, _ = ctx.text_extents(s)
    x, y = -tw / 2 - xb, -yb - th / 2
    # shadow
    ctx.move_to(x + 4, y + 6)
    ctx.text_path(s)
    ctx.set_source_rgba(0, 0, 0, 0.5 * alpha)
    ctx.set_line_width(sw)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.stroke_preserve()
    ctx.fill()
    ctx.move_to(x, y)
    ctx.text_path(s)
    ctx.set_source_rgba(*stroke, alpha)
    ctx.stroke_preserve()
    ctx.set_source_rgba(*fill, alpha)
    ctx.fill()
    ctx.restore()

# ----------------------------------------------------------------- THE ARTWORK
def draw_cyber_ramen(ctx, variant, t=0.0):
    """Rich Cyberpunk Japanese Ramen Bar (960x640 local space)."""
    A = (variant == "A")
    
    # 1. Dark Cyber Tokyo Night Backdrop
    ctx.set_source(lin(ctx, 0, 0, 0, 420, [
        (0.0, (0.05, 0.04, 0.12)),
        (0.6, (0.08, 0.05, 0.18)),
        (1.0, (0.14, 0.08, 0.22))
    ]))
    ctx.rectangle(0, 0, 960, 420)
    ctx.fill()
    
    # Distant Neon City Buildings
    rnd = random.Random(42)
    for bx in range(0, 960, 60):
        bh = rnd.randint(120, 260)
        bw = rnd.randint(45, 75)
        ctx.set_source_rgb(0.03, 0.02, 0.07)
        ctx.rectangle(bx, 420 - bh, bw, bh); ctx.fill()
        # Cyber windows
        ctx.set_source_rgba(0.0, 0.85, 1.0, 0.25)
        for wy in range(420 - bh + 20, 400, 30):
            for wx in range(bx + 8, bx + bw - 10, 15):
                if rnd.random() > 0.4:
                    ctx.rectangle(wx, wy, 8, 14); ctx.fill()
                    
    # 2. Wooden Ramen Counter & Roof Eaves
    # Roof Eaves at top
    ctx.set_source(lin(ctx, 0, 0, 0, 90, [(0, (0.20, 0.12, 0.10)), (1, (0.10, 0.05, 0.04))]))
    ctx.rectangle(0, 0, 960, 80); ctx.fill()
    # Roof tiles
    ctx.set_line_width(3); ctx.set_source_rgba(0.9, 0.3, 0.1, 0.4)
    for x in range(0, 960, 40):
        ctx.move_to(x, 0); ctx.line_to(x, 80); ctx.stroke()
    ctx.rectangle(0, 80, 960, 12); ctx.set_source_rgb(0.8, 0.25, 0.1); ctx.fill()

    # Wooden Counter (Y: 420 to 640)
    ctx.set_source(lin(ctx, 0, 420, 0, 640, [(0, (0.35, 0.18, 0.10)), (1, (0.18, 0.09, 0.05))]))
    ctx.rectangle(0, 420, 960, 220); ctx.fill()
    # Countertop polished glossy bar
    ctx.set_source(lin(ctx, 0, 410, 0, 440, [(0, (0.55, 0.30, 0.18)), (1, (0.28, 0.14, 0.08))]))
    ctx.rectangle(0, 410, 960, 30); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.15)
    ctx.rectangle(0, 412, 960, 4); ctx.fill() # specular reflection line

    # 3. NEON LANTERN (DIFFERENCE 1: Local x=310, y=230)
    # Lantern Hanging wire
    ctx.set_line_width(3); ctx.set_source_rgb(0.2, 0.2, 0.2)
    ctx.move_to(310, 92); ctx.line_to(310, 160); ctx.stroke()
    # Red Paper Lantern
    ctx.save()
    ctx.translate(310, 230)
    # Glowing Aura
    aura = cairo.RadialGradient(0, 0, 20, 0, 0, 130)
    aura.add_color_stop_rgba(0, 1.0, 0.2, 0.1, 0.35)
    aura.add_color_stop_rgba(1, 1.0, 0.2, 0.1, 0.0)
    ctx.set_source(aura); ctx.arc(0, 0, 130, 0, 2*math.pi); ctx.fill()
    # Lantern body
    ctx.set_source(lin(ctx, 0, -65, 0, 65, [(0, (1.0, 0.3, 0.2)), (0.5, (0.9, 0.1, 0.05)), (1, (0.6, 0.05, 0.02))]))
    ctx.scale(55, 75); ctx.arc(0, 0, 1, 0, 2*math.pi); ctx.fill()
    ctx.restore()
    # Lantern ribs
    ctx.set_line_width(2); ctx.set_source_rgba(0, 0, 0, 0.4)
    for ly in [185, 210, 235, 260, 285]:
        ctx.move_to(270, ly); ctx.curve_to(310, ly + 8, 310, ly + 8, 350, ly); ctx.stroke()
    # LANTERN SYMBOL (DIFFERENCE 1):
    ctx.save()
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(36)
    if A:
        # Variant A: Golden Ramen Bowl / Sun icon (Bold 'RAMEN')
        ctx.set_source_rgb(1.0, 0.9, 0.2)
        ctx.move_to(285, 242); ctx.show_text("RAMEN")
    else:
        # Variant B: Electric Cyan Kanji/Text (Bold 'NOODLE') (DIFFERENCE 1)
        ctx.set_source_rgb(0.0, 0.9, 1.0)
        ctx.move_to(278, 242); ctx.show_text("TOKYO")
    ctx.restore()

    # 4. CYBER CAT CHEF (Center at x=670, y=350)
    # Cat Chef Body in Kimono / Cyber Jacket
    ctx.set_source(lin(ctx, 600, 320, 740, 480, [(0, (0.12, 0.15, 0.25)), (1, (0.05, 0.08, 0.15))]))
    ctx.arc(670, 420, 95, 0, 2*math.pi); ctx.fill()
    # White apron
    ctx.set_source_rgb(0.92, 0.92, 0.95)
    ctx.arc(670, 440, 65, 0, 2*math.pi); ctx.fill()
    # Paws on counter holding chopsticks
    ctx.set_source_rgb(1, 1, 1)
    ctx.arc(610, 440, 20, 0, 2*math.pi); ctx.fill()
    ctx.arc(730, 440, 20, 0, 2*math.pi); ctx.fill()
    
    # Cat Head
    ctx.set_source(lin(ctx, 620, 240, 720, 360, [(0, (0.95, 0.95, 0.98)), (1, (0.80, 0.82, 0.88))]))
    ctx.arc(670, 310, 75, 0, 2*math.pi); ctx.fill()
    # Cat Ears
    ctx.move_to(600, 270); ctx.line_to(585, 200); ctx.line_to(640, 250); ctx.close_path(); ctx.fill()
    ctx.move_to(740, 270); ctx.line_to(755, 200); ctx.line_to(700, 250); ctx.close_path(); ctx.fill()
    # Inner pink ears
    ctx.set_source_rgb(1.0, 0.6, 0.7)
    ctx.move_to(605, 265); ctx.line_to(595, 215); ctx.line_to(635, 250); ctx.close_path(); ctx.fill()
    ctx.move_to(735, 265); ctx.line_to(745, 215); ctx.line_to(705, 250); ctx.close_path(); ctx.fill()
    
    # CYBER CAT MASK / VISOR (DIFFERENCE 2: Local x=670, y=310)
    ctx.save()
    rrect(ctx, 615, 280, 110, 38, 12)
    if A:
        # Variant A: Electric Neon CYAN Visor
        ctx.set_source_rgb(0.0, 0.9, 1.0)
    else:
        # Variant B: Hot Neon MAGENTA/PINK Visor (DIFFERENCE 2)
        ctx.set_source_rgb(1.0, 0.1, 0.6)
    ctx.fill_preserve()
    ctx.set_line_width(3); ctx.set_source_rgb(1, 1, 1); ctx.stroke()
    # Visor Reflection slit
    ctx.set_source_rgba(1, 1, 1, 0.7)
    ctx.rectangle(630, 285, 45, 5); ctx.fill()
    ctx.restore()
    # Cute cat nose & mouth
    ctx.set_source_rgb(1.0, 0.4, 0.5)
    ctx.move_to(666, 332); ctx.line_to(674, 332); ctx.line_to(670, 338); ctx.close_path(); ctx.fill()
    # Whiskers
    ctx.set_line_width(2.5); ctx.set_source_rgb(0.2, 0.2, 0.2)
    ctx.move_to(610, 335); ctx.line_to(550, 330); ctx.stroke()
    ctx.move_to(610, 345); ctx.line_to(555, 350); ctx.stroke()
    ctx.move_to(730, 335); ctx.line_to(790, 330); ctx.stroke()
    ctx.move_to(730, 345); ctx.line_to(785, 350); ctx.stroke()

    # 5. GIANT STEAMING RAMEN BOWL (Center at x=480, y=490)
    # Steam rising
    ctx.save()
    ctx.set_line_width(4); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgba(1, 1, 1, 0.35)
    for sx in [440, 480, 520]:
        ctx.move_to(sx, 440)
        ctx.curve_to(sx - 15, 410, sx + 20, 380, sx, 350)
        ctx.stroke()
    ctx.restore()
    
    # Outer Red Ceramic Bowl
    ctx.save()
    ctx.translate(480, 510)
    ctx.set_source(lin(ctx, -140, 0, 140, 90, [(0, (0.9, 0.15, 0.1)), (1, (0.5, 0.05, 0.05))]))
    # Bowl shape
    ctx.move_to(-140, 0)
    ctx.curve_to(-130, 90, 130, 90, 140, 0)
    ctx.close_path(); ctx.fill()
    # Gold rim band
    ctx.set_line_width(5); ctx.set_source_rgb(1.0, 0.8, 0.1)
    ctx.move_to(-140, 0); ctx.curve_to(-130, 90, 130, 90, 140, 0); ctx.stroke()
    # Bowl interior soup (Rich Tonkotsu golden broth)
    ctx.scale(136, 32); ctx.arc(0, 0, 1, 0, 2*math.pi)
    ctx.set_source_rgb(0.95, 0.75, 0.25); ctx.fill()
    ctx.restore()
    
    # Ramen Noodles swirl
    ctx.set_line_width(4); ctx.set_source_rgb(1.0, 0.92, 0.55)
    for ny in [495, 505, 515]:
        ctx.move_to(400, ny); ctx.curve_to(440, ny-6, 520, ny+6, 560, ny); ctx.stroke()
    # Green scallions sprinkled
    ctx.set_source_rgb(0.1, 0.75, 0.2)
    for gx, gy in [(430, 500), (450, 520), (510, 510), (530, 500), (470, 495)]:
        ctx.arc(gx, gy, 5, 0, 2*math.pi); ctx.fill()

    # RAMEN TOPPING (DIFFERENCE 3: Local x=480, y=505)
    ctx.save()
    if A:
        # Variant A: Iconic Japanese Naruto Fishcake (White disc with Pink swirl)
        ctx.set_source_rgb(1, 1, 1)
        ctx.arc(480, 505, 22, 0, 2*math.pi); ctx.fill()
        # Pink swirl
        ctx.set_line_width(4); ctx.set_source_rgb(1.0, 0.3, 0.6)
        ctx.arc(480, 505, 12, 0, 1.5*math.pi); ctx.stroke()
    else:
        # Variant B: Boiled Ramen Egg (White oval with Golden Liquid Yolk) (DIFFERENCE 3)
        ctx.translate(480, 505)
        ctx.scale(26, 20)
        ctx.set_source_rgb(1, 1, 1); ctx.arc(0, 0, 1, 0, 2*math.pi); ctx.fill()
        ctx.scale(0.65, 0.65)
        ctx.set_source_rgb(1.0, 0.55, 0.0); ctx.arc(0, 0, 1, 0, 2*math.pi); ctx.fill()
    ctx.restore()

    # Chopsticks resting across the bowl
    ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_source_rgb(0.35, 0.18, 0.08)
    ctx.move_to(360, 490); ctx.line_to(580, 530); ctx.stroke()
    ctx.move_to(365, 498); ctx.line_to(585, 538); ctx.stroke()

    # 6. Neon Shop Signs on Left & Right
    # Left sign: 'OPEN'
    rrect(ctx, 40, 140, 130, 55, 10)
    ctx.set_source_rgba(0.08, 0.05, 0.15, 0.85); ctx.fill_preserve()
    ctx.set_line_width(3); ctx.set_source_rgb(0.0, 1.0, 0.4); ctx.stroke()
    text_c(ctx, "OPEN", 105, 168, 36, (0.0, 1.0, 0.4), sw=2)

    # Right sign: '24H'
    rrect(ctx, 790, 140, 130, 55, 10)
    ctx.set_source_rgba(0.08, 0.05, 0.15, 0.85); ctx.fill_preserve()
    ctx.set_line_width(3); ctx.set_source_rgb(1.0, 0.8, 0.0); ctx.stroke()
    text_c(ctx, "24H", 855, 168, 36, (1.0, 0.8, 0.0), sw=2)

# ----------------------------------------------------------------- SOUNDTRACK
def render_soundtrack(wav_path):
    SR = 44100
    total_s = int(DUR * SR)
    master = np.zeros(total_s, dtype=np.float32)

    def write_wav(path, samples):
        samples = np.clip(samples, -1.0, 1.0)
        int_s = (samples * 32767).astype(np.int16)
        with wave.open(path, 'w') as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
            wf.writeframes(int_s.tobytes())

    # Synth whoosh
    t = np.linspace(0, 0.8, int(SR * 0.8), False)
    whoosh = np.sin(2 * np.pi * np.linspace(120, 700, len(t)) * t) * (t / 0.8) * np.exp(-(0.8 - t) * 3) * 0.6
    
    # Crisp Woodblock Tick
    t = np.linspace(0, 0.06, int(SR * 0.06), False)
    tick = np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 110) * 0.8

    # Fast Urgency Tick (higher pitch)
    t = np.linspace(0, 0.05, int(SR * 0.05), False)
    tick_fast = np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 130) * 0.9

    # Bell Reveal Chime
    t = np.linspace(0, 0.8, int(SR * 0.8), False)
    bell = (np.sin(2 * np.pi * 1400 * t) * 0.7 + np.sin(2 * np.pi * 2800 * t) * 0.3) * np.exp(-t * 7) * 0.9

    # Bass Drop at Reveal
    t = np.linspace(0, 0.9, int(SR * 0.9), False)
    boom = np.sin(2 * np.pi * np.linspace(180, 45, len(t)) * t) * np.exp(-t * 4) * 0.8

    def overlay(snd, st, vol=1.0):
        si = int(st * SR); ei = min(len(master), si + len(snd))
        master[si:ei] += snd[:ei-si] * vol

    overlay(whoosh, 0.0, 0.7)
    for sec in range(1, 10):
        overlay(tick, float(sec), 0.75)
        if sec >= 7:
            overlay(tick_fast, float(sec) + 0.5, 0.85)

    overlay(boom, 10.0, 0.9)
    overlay(bell, 11.0, 0.9)
    overlay(bell, 12.1, 0.9)
    overlay(bell, 13.2, 1.0)

    write_wav(wav_path, master)

# ----------------------------------------------------------------- FULL COMPOSITOR
def draw_frame(ctx, t, surfA, surfB):
    # Background
    ctx.set_source(lin(ctx, 0, 0, 0, H, [(0, (0.05, 0.03, 0.10)), (1, (0.02, 0.01, 0.05))]))
    ctx.paint()

    # Panel A at top (y = 250)
    ctx.save()
    ctx.translate(PX, PA_Y)
    ctx.set_source_surface(surfA, 0, 0); ctx.paint()
    rrect(ctx, 0, 0, PW, PH, 24)
    ctx.set_line_width(8); ctx.set_source_rgb(0.0, 0.9, 1.0); ctx.stroke()
    ctx.restore()
    text_c(ctx, "IMAGE 1", PX + 85, PA_Y + 45, 30, (1, 1, 1), sw=6)

    # Panel B at bottom (y = 930)
    ctx.save()
    ctx.translate(PX, PB_Y)
    ctx.set_source_surface(surfB, 0, 0); ctx.paint()
    rrect(ctx, 0, 0, PW, PH, 24)
    ctx.set_line_width(8); ctx.set_source_rgb(1.0, 0.2, 0.6); ctx.stroke()
    ctx.restore()
    text_c(ctx, "IMAGE 2", PX + 85, PB_Y + 45, 30, (1, 1, 1), sw=6)

    # HEADER (Top Area) - Instant Bold Hook
    pulse = 1.0 + 0.03 * math.sin(t * 8)
    text_c(ctx, "SPOT 3 DIFFERENCES!", W/2, 110, 84, (1.0, 0.9, 0.1), stroke=(0, 0, 0), sw=12, scale=pulse)
    text_c(ctx, "⚡ ONLY 1% FIND THE 3RD ONE! ⚡", W/2, 185, 32, (0.0, 0.95, 1.0), stroke=(0, 0, 0), sw=6)

    # TIMER / HUD (Bottom HUD y = 1620 to 1860)
    hud_cy = 1710
    if t < PUZZLE_END:
        rem = max(0, int(math.ceil(PUZZLE_END - t)))
        prog = clamp((PUZZLE_END - t) / PUZZLE_END)
        
        # Countdown Bar
        bw, bh = 860, 26
        bx, by = (W - bw)/2, hud_cy + 40
        rrect(ctx, bx, by, bw, bh, 13)
        ctx.set_source_rgba(0.15, 0.1, 0.25, 0.8); ctx.fill()
        
        # Active bar
        rrect(ctx, bx, by, bw * prog, bh, 13)
        col = (1.0, 0.2, 0.1) if prog < 0.3 else ((1.0, 0.8, 0.0) if prog < 0.6 else (0.0, 0.9, 0.4))
        ctx.set_source_rgb(*col); ctx.fill()
        
        # Text
        text_c(ctx, f"TIME: {rem:02d}s", W/2, hud_cy - 15, 78, (1, 1, 1), sw=10)
    else:
        # Time Up / Answers
        text_c(ctx, "TIMES UP! HERE THEY ARE!", W/2, hud_cy - 20, 68, (1.0, 0.2, 0.2), sw=10)
        text_c(ctx, "KITNE MILE? 1, 2 YA 3? COMMENT! 👇", W/2, hud_cy + 45, 36, (1.0, 0.9, 0.2), sw=6)

    # DIFFERENCE REVEAL RINGS ON PANEL B
    for idx, (lx, ly, r, rev_t, tag) in enumerate(DIFFS):
        if t >= rev_t:
            dt = t - rev_t
            s = ease_out_back(dt * 3.5)
            # Global coords
            gx = PX + lx
            gy = PB_Y + ly
            
            ctx.save()
            ctx.translate(gx, gy)
            ctx.scale(s, s)
            
            # Glowing Ring
            ctx.set_line_width(8)
            ctx.set_source_rgb(1.0, 0.1, 0.1)
            ctx.arc(0, 0, r, 0, 2*math.pi); ctx.stroke()
            
            # Badge
            ctx.restore()
            text_c(ctx, f"#{idx+1} {tag}", gx, gy - r - 28, 28, (1.0, 0.9, 0.1), stroke=(0, 0, 0), sw=6)

print("Starting Cyber Ramen short render...")

# Render Static Panel Images First
surfA = cairo.ImageSurface(cairo.FORMAT_ARGB32, PW, PH)
draw_cyber_ramen(cairo.Context(surfA), "A")
surfA.write_to_png(os.path.join(OUT, "panel_A.png"))

surfB = cairo.ImageSurface(cairo.FORMAT_ARGB32, PW, PH)
draw_cyber_ramen(cairo.Context(surfB), "B")
surfB.write_to_png(os.path.join(OUT, "panel_B.png"))

# Render Audio
wav_path = os.path.join(OUT, "audio.wav")
render_soundtrack(wav_path)

# Render Frames via FFmpeg pipe (Fast & Zero Disk Waste)
mp4_path = os.path.join(OUT, "spot_diff_02_cyber_ramen.mp4")
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{W}x{H}",
    "-pix_fmt", "bgra",
    "-r", str(FPS),
    "-i", "-",
    "-i", wav_path,
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "19",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    mp4_path
]

pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
frame_surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
frame_ctx = cairo.Context(frame_surf)

TOTAL_FRAMES = int(DUR * FPS)
for f in range(TOTAL_FRAMES):
    t = f / FPS
    # Last 0.5s loops back to t=0 for seamless replay!
    if t >= DUR - 0.5:
        comp_t = 0.0
    else:
        comp_t = t
    draw_frame(frame_ctx, comp_t, surfA, surfB)
    pipe.stdin.write(frame_surf.get_data())

pipe.stdin.close()
pipe.wait()

# Extract thumbnail at t=5.0
thumb_path = os.path.join(OUT, "thumbnail.png")
subprocess.run([
    "ffmpeg", "-y", "-ss", "00:00:05", "-i", mp4_path,
    "-vframes", "1", thumb_path
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Short #02 Rendered successfully!")
print("Video:", mp4_path)
print("Thumbnail:", thumb_path)
