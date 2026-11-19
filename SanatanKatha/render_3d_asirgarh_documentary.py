"""Asirgarh Kile Ka Rahasya: 3D CGI Cinematic Documentary Renderer for Divya Rahasya.
Features: 8 high-resolution Little Krishna 3D animated scene plates,
Ken Burns 2.5D camera zoom and pan, dynamic particle/lighting overlays,
rotating 3D Sudarshana Chakra, floating lotus petals, and dynamic subtitles
synchronized to the 380s master voiceover audio.
"""

import math
import os
import sys
import time
import subprocess
import cairo
import numpy as np
from pathlib import Path
from PIL import Image

W, H = 1920, 1080
FPS = 30

ROOT = Path(__file__).resolve().parent
SCENES_DIR = ROOT / "output" / "documentary" / "scenes"
WORK_DIR = ROOT / "output" / "work" / "asirgarh" / "files"
OUT_DIR = ROOT / "output" / "documentary"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Helper Math & Cairo Primitives
def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))

def lerp(a, b, u):
    return a + (b - a) * u

def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -1.5707963, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, 1.5707963)
    ctx.arc(x + r, y + h - r, r, 1.5707963, 3.1415926)
    ctx.arc(x + r, y + r, r, 3.1415926, 4.7123889)
    ctx.close_path()

def circle(ctx, cx, cy, r, c, a=1.0, fill=True, w=2):
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.set_source_rgba(c[0], c[1], c[2], a)
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
    ctx.set_source_rgba(c[0], c[1], c[2], a)
    ctx.set_line_width(w)
    ctx.stroke()

# Load 3D Scene Plates into Memory
print("Loading 3D CGI Scene Plates...")
SCENE_KEYS = [
    "scene_01", # Gupteshwar Mahadev Temple
    "scene_02", # Asirgarh Fort Plateau
    "scene_03", # Locked Fort Gates
    "scene_04", # Kurukshetra War Ruins
    "scene_05", # Krishna Cursing Ashwatthama
    "scene_06", # 1819 British Encounter
    "scene_07", # 1970 Doctor Clinic
    "scene_08", # Kalki Avatar Prophecy
]

SCENE_SURFACES = {}
for k in SCENE_KEYS:
    p = SCENES_DIR / f"{k}.jpg"
    if not p.exists():
        raise FileNotFoundError(f"Missing scene: {p}")
    # Render with generous margin for Ken Burns zoom
    im = Image.open(p).convert("RGBA").resize((int(W * 1.15), int(H * 1.15)), Image.Resampling.LANCZOS)
    arr = np.array(im)
    bgra = arr[:, :, [2, 1, 0, 3]].copy()
    surf = cairo.ImageSurface.create_for_data(bgra, cairo.FORMAT_ARGB32, im.width, im.height)
    SCENE_SURFACES[k] = surf
    print(f"  Loaded {k}: {im.width}x{im.height}")

# Dynamic Subtitles
SUBTITLE_TIMESTAMPS = [
    (0.0, 7.5, "MADHYA PRADESH KE ASIRGARH KILE KA RAHASYA"),
    (7.5, 15.0, "GUPTESHWAR MAHADEV PAR HAR SUBAH TAZA PHOOL"),
    (15.0, 22.0, "BAND KILE MEIN ROZ PUJA KAUN KARTA HAI?"),
    (22.0, 32.0, "5000 SAAL PURANA MAHABHARAT KA SHRAAP"),
    (32.0, 42.0, "ASHWATTHAMA NE CHALAYA BRAHMASHIRSHA ASTRA"),
    (42.0, 52.0, "SHRI KRISHNA KA SABSE BHAYANAK SHRAAP"),
    (52.0, 68.0, "MRITYU TUJHE NAHI CHHUEGI, TU ANTAK BHATKEGA!"),
    (68.0, 85.0, "MAATHE SE DIVYA CHINTAMANI KO NOCH LIYA"),
    (85.0, 100.0, "SATPUDA KI PAHADIYON MEIN ASIRGARH QILA"),
    (100.0, 115.0, "900 FEET UNCHI KHADI PAHADI KA ABHEDYA DURG"),
    (115.0, 130.0, "KILE KI KHAI MEIN GUPTESHWAR MAHADEV MANDIR"),
    (130.0, 150.0, "BHOR MEIN CHAR BAJE TAZA BILVAPATRA KA RAHASYA"),
    (150.0, 175.0, "RATRI MEIN KOI NAHI RUK PATA IS KILE MEIN"),
    (175.0, 195.0, "1819 BRITISH ARMY SIGHTING RECORDS"),
    (195.0, 220.0, "DHUNDH MEIN 9-FOOT LAMBA VISHALKAY YODDHA!"),
    (220.0, 245.0, "1970 BURHANPUR DOCTOR EYEWITNESS ENCOUNTER"),
    (245.0, 270.0, "MAATHE KA ANCIENT GHAAV AUR SARSON KA TEL"),
    (270.0, 290.0, "NARMADA PARIKRAMA MEIN SADHIK SIGHTINGS"),
    (290.0, 315.0, "PURANON KA RAHASYA: ASHTA CHIRANJEEVI"),
    (315.0, 340.0, "AGLE MANVANTARA MEIN SAPTARISHI KA PAD"),
    (340.0, 360.0, "BHAGWAN KALKI KE AAGAMAN KA INTEZAAR"),
    (360.0, 380.3, "HAR HAR MAHADEV! COMMENT MEIN APNI RAYE DEIN!"),
]

def draw_subtitles(ctx, sub_text):
    if not sub_text:
        return
    ctx.save()
    font_sz = 46
    ctx.select_font_face("Impact", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(font_sz)
    
    ext = ctx.text_extents(sub_text)
    box_w = ext.width + 80
    box_h = 76
    box_x = W / 2 - box_w / 2
    box_y = 930
    
    # Frosted pill
    rrect(ctx, box_x, box_y, box_w, box_h, 20)
    ctx.set_source_rgba(0.04, 0.02, 0.02, 0.88)
    ctx.fill()
    rrect(ctx, box_x, box_y, box_w, box_h, 20)
    ctx.set_source_rgba(1.0, 0.85, 0.25, 0.95)
    ctx.set_line_width(2.5)
    ctx.stroke()
    
    # Text
    tx = W / 2 - ext.width / 2 - ext.x_bearing
    ty = box_y + box_h / 2 - ext.height / 2 - ext.y_bearing
    
    ctx.move_to(tx, ty)
    ctx.text_path(sub_text)
    ctx.set_source_rgba(0.0, 0.0, 0.0, 1.0)
    ctx.set_line_width(8)
    ctx.stroke_preserve()
    ctx.set_source_rgba(1.0, 0.95, 0.45, 1.0)
    ctx.fill()
    ctx.restore()

# Scene Timeline Mapping across 380.35 seconds
TIMELINE_SCENES = [
    # (start_time, end_time, scene_key, zoom_dir: 1 for zoom-in, -1 for zoom-out, pan_x)
    (0.0, 22.0, "scene_01", 1, 0),        # Shivling Macro & Flowers
    (22.0, 48.0, "scene_04", 1, 30),      # Kurukshetra War
    (48.0, 85.0, "scene_05", 1, -20),     # Krishna Cursing Ashwatthama
    (85.0, 120.0, "scene_02", -1, 40),    # Asirgarh Fort Plateau
    (120.0, 150.0, "scene_01", 1, 0),     # Shivling Morning Flowers
    (150.0, 175.0, "scene_03", 1, 0),     # Locked Fort Gates
    (175.0, 220.0, "scene_06", 1, -30),   # 1819 British Encounter
    (220.0, 275.0, "scene_07", 1, 25),    # 1970 Doctor Clinic
    (275.0, 310.0, "scene_02", 1, -30),   # Asirgarh Mountain Ridge
    (310.0, 355.0, "scene_08", 1, 0),     # Kalki Avatar & Saptarishi
    (355.0, 380.4, "scene_01", 1, 0),     # Gupteshwar Mahadev Outro
]

def render_3d_frame(ctx, t):
    # Find active scene
    active_seg = TIMELINE_SCENES[-1]
    for seg in TIMELINE_SCENES:
        if seg[0] <= t < seg[1]:
            active_seg = seg
            break
            
    st, en, key, z_dir, pan_target = active_seg
    u = clamp((t - st) / max(en - st, 0.01))
    
    surf = SCENE_SURFACES[key]
    sw, sh = surf.get_width(), surf.get_height()
    
    # 2.5D Ken Burns Camera Math
    base_scale = W / (sw / 1.15)
    if z_dir == 1:
        cur_scale = lerp(1.0, 1.10, u)
    else:
        cur_scale = lerp(1.10, 1.0, u)
        
    cur_pan_x = lerp(0, pan_target, u)
    
    ctx.save()
    # Center origin
    ctx.translate(W / 2 + cur_pan_x, H / 2)
    ctx.scale(cur_scale, cur_scale)
    ctx.translate(-sw / 2, -sh / 2)
    
    ctx.set_source_surface(surf, 0, 0)
    ctx.paint()
    ctx.restore()
    
    # Scene-Specific Dynamic VFX Overlays
    if key == "scene_05":
        # Rotating Radiant 3D Sudarshana Chakra on Krishna's finger
        ch_x, ch_y = 520, 520
        glow(ctx, ch_x, ch_y, 140, (1.0, 0.88, 0.35), 0.75 + 0.15 * math.sin(t * 12.0))
        for sp in range(12):
            ang = sp * math.pi / 6 + t * 14.0
            line(ctx, [(ch_x, ch_y), (ch_x + 85 * math.cos(ang), ch_y + 85 * math.sin(ang))], (1.0, 0.95, 0.5), 6)
        circle(ctx, ch_x, ch_y, 65, (1.0, 0.85, 0.2), fill=False, w=10)
        # Divine floating sparks
        for i in range(8):
            spk_x = ch_x + 75 * math.cos(t * 10.0 + i * 0.8)
            spk_y = ch_y + 75 * math.sin(t * 10.0 + i * 0.8)
            circle(ctx, spk_x, spk_y, 3, (1.0, 1.0, 0.8), a=0.9)
            
    elif key == "scene_01":
        # Flickering Diya Warmth and floating golden dust
        glow(ctx, W/2 - 240, 780, 95, (1.0, 0.55, 0.05), 0.5 + 0.15 * math.sin(t * 9.0))
        glow(ctx, W/2 + 240, 780, 95, (1.0, 0.55, 0.05), 0.5 + 0.15 * math.sin(t * 11.0))
        # Floating golden spiritual motes
        for i in range(15):
            mx = W/2 - 180 + ((i * 53 + t * 25) % 360)
            my = 350 + ((i * 67 + t * 35) % 450)
            circle(ctx, mx, my, 2.5, (1.0, 0.9, 0.4), a=0.65 + 0.25 * math.sin(t * 3.0 + i))
            
    elif key == "scene_08":
        # Blazing solar radiance on Kalki's celestial blade
        glow(ctx, W/2 + 220, 420, 180, (1.0, 0.88, 0.4), 0.7 + 0.2 * math.sin(t * 8.0))
        # Showering pink lotus petals
        for p in range(25):
            px = (p * 85 + t * 45) % W
            py = (p * 63 + t * 75) % H
            circle(ctx, px, py, 7, (1.0, 0.45, 0.60), a=0.85)

def render_full_3d_documentary():
    audio_mix = WORK_DIR / "asirgarh_final_mix.wav"
    out_video = OUT_DIR / "asirgarh_documentary.mp4"
    total_dur = 380.35
    
    print(f"Rendering 3D CGI Cinematic Documentary ({total_dur:.1f}s, {int(total_dur * FPS)} frames)...")
    
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
    
    for f_idx in range(total_frames):
        t = f_idx / FPS
        render_3d_frame(ctx, t)
        
        # Subtitle overlay
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
            print(f"3D Render: {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%) | {fps_rend:.1f} FPS | ETA: {eta:.1f}s")
            
    proc.stdin.close()
    proc.wait()
    
    total_time = time.time() - t0
    print(f"\n3D Documentary Render Complete in {total_time:.1f}s ({total_time/60:.2f} mins)!")
    print(f"Output MP4: {out_video}")
    return out_video

if __name__ == "__main__":
    render_full_3d_documentary()
