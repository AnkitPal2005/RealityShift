# RealityShift Cairo Typography and Overlays Reference

This reference establishes the technical standards, coordinate systems, safe zone constraints, font fallback ladders, and PyCairo drawing implementations for scientific overlays, HUD telemetry, and kinetic subtitles in the RealityShift pipeline.

---

## 1. PyCairo Coordinate System & Rendering Architecture

### 1.1 Canvas Geometry & Buffer Creation
PyCairo renders vector graphics directly into a 32-bit ARGB NumPy memory buffer:

```python
import cairo
import numpy as np

W, H = 1080, 1920

def create_cairo_overlay():
    data = np.zeros((H, W, 4), dtype=np.uint8)
    surface = cairo.ImageSurface.create_for_data(
        data, cairo.FORMAT_ARGB32, W, H, W * 4
    )
    ctx = cairo.Context(surface)
    return surface, ctx, data
```

### 1.2 State Isolation Guardrail (Zero Matrix Leaks)
To prevent coordinate scaling, rotation, or translation transforms from bleeding across frames or flipping subsequent text:
1. Every procedural drawing function must open with `ctx.save()` and close with `ctx.restore()`.
2. Never exit a drawing block prematurely via `return` or `raise` without restoring the context.

```python
def draw_hud_element(ctx, x, y, scale, rotation):
    ctx.save()
    try:
        ctx.translate(x, y)
        ctx.scale(scale, scale)
        ctx.rotate(rotation)
        # ... perform drawing ...
    finally:
        ctx.restore()
```

---

## 2. YouTube Shorts Safe Zones: Existing Engine vs. Expanded Standards

In YouTube Shorts, native mobile UI overlays (channel avatar, subscribe button, like/comment stack on the right, sound title bar at the bottom, and top search header) obscure large portions of the screen.

### 2.1 The Two Safe Zone Specifications

```
y = 0     +-----------------------------------------+
          | TOP HEADER UI ZONE (Search, Sound, Bar) |  y in [0, 180]
y = 180   +-----------------------------------------+
          |                                         |
          |       PRIMARY VISUAL FOCUS ZONE         |
          |       (Focal subjects, planets, faces)   |  y in [180, 1150]
          |       Keep horizontal margins x: 180-900|
          |                                         |
y = 1150  +-----------------------------------------+
          | EXISTING ENGINE CAPTION: [1150, 1250]   |  core/lego.py standard
y = 1250  | PROPOSED EXTENDED BAND:  [1250, 1320]   |  2-line subtitle headroom
y = 1320  +-----------------------------------------+
          |                                         |
y = 1450  + - - - - - - - - - - - - - - - - - - - - +
          | BOTTOM CRITICAL UI DANGER ZONE          |  y in [1450, 1920]
          | Existing engine UI_CLEAR = 1520         |  Right edge x > 880 blocked
y = 1920  +-----------------------------------------+
```

| Region | Existing Engine (`core/lego.py`) | Proposed Implementation Standard | Operational Rule |
| :--- | :--- | :--- | :--- |
| **Top Header Zone** | `HEADER_Y = 120` | $y \in [100, 220]$ | Minimal telemetry only. No critical text. |
| **Visual Focal Zone** | Undefined (full frame) | $x \in [180, 900], y \in [240, 1100]$ | AI characters, cosmic bodies, diagrams must be framed here. |
| **Kinetic Caption Band**| `CAP_TOP = 1150, CAP_BOTTOM = 1250` | $y \in [1150, 1320]$ | Kinetic subtitles and primary translation cards. |
| **Bottom UI Clear Zone**| `UI_CLEAR = 1520` | $y \ge 1450$ ($y \ge 1520$ for center) | Zero informational text or key graphics. Bottom and right edge blocked by mobile client. |

---

## 3. Typography & Cross-Platform Font Resolution

### 3.1 Zero Tofu Squares (`□□□`) Rule
Cairo text rendering with Latin-only fonts does not include Devanagari glyphs. Any raw Hindi text rendered directly into PyCairo text routines will produce missing glyph boxes (`□□□`).
- **Rule**: All Cairo visual elements (HUD ribbons, metric telemetry, chapter titles, data readouts) must use capitalized Roman transliteration (e.g., `GRAVITATIONAL FIELD: COLLAPSE`, `CHANDRA MA DHOOR`, `OBLIQUITY VARIATION: 20-25 DEG`).
- The spoken narration remains authentic Hindi in the voiceover audio track.

### 3.2 Font Fallback Ladder

To ensure deterministic rendering across Windows development environments and Linux CI/CD render nodes:

| Role | Primary Font (Windows) | Fallback 1 (Windows / Mac) | Fallback 2 (Linux / CI) | Typographic Style |
| :--- | :--- | :--- | :--- | :--- |
| **Impact / Title HUD** | `Impact` | `Arial Black` | `DejaVu Sans Bold` | Heavy, condensed, all-caps. |
| **Telemetry & Metrics** | `Consolas` | `Lucida Console` | `DejaVu Sans Mono` | Monospaced, technical, sci-fi precision. |
| **Subtitles & Captions** | `Segoe UI` | `Helvetica Neue` | `DejaVu Sans` | Clean, highly legible at mobile scale. |

### 3.3 Dynamic Font Resolver in Python
```python
import os
import cairo

def select_cairo_font(ctx: cairo.Context, font_role: str):
    """Sets the appropriate font face with platform-aware fallbacks."""
    is_windows = os.name == "nt"
    if font_role == "impact":
        font_name = "Impact" if is_windows else "DejaVu Sans"
        ctx.select_font_face(font_name, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    elif font_role == "telemetry":
        font_name = "Consolas" if is_windows else "DejaVu Sans Mono"
        ctx.select_font_face(font_name, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    elif font_role == "subtitle":
        font_name = "Segoe UI" if is_windows else "DejaVu Sans"
        ctx.select_font_face(font_name, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
```

---

## 4. Sci-Fi HUD Telemetry & Vector Graphics Library

### 4.1 Technical Telemetry Box
```python
def draw_telemetry_box(ctx, x, y, width, height, label: str, value: str, cyan=(0.0, 0.9, 1.0)):
    ctx.save()
    try:
        # Background plate with 50% opacity
        ctx.set_source_rgba(0.02, 0.05, 0.10, 0.65)
        ctx.rectangle(x, y, width, height)
        ctx.fill()
        
        # Technical corner brackets
        ctx.set_source_rgba(cyan[0], cyan[1], cyan[2], 0.85)
        ctx.set_line_width(2.0)
        bracket_len = 12.0
        
        # Top-left corner
        ctx.move_to(x, y + bracket_len); ctx.line_to(x, y); ctx.line_to(x + bracket_len, y)
        # Top-right corner
        ctx.move_to(x + width - bracket_len, y); ctx.line_to(x + width, y); ctx.line_to(x + width, y + bracket_len)
        # Bottom-left corner
        ctx.move_to(x, y + height - bracket_len); ctx.line_to(x, y + height); ctx.line_to(x + bracket_len, y + height)
        # Bottom-right corner
        ctx.move_to(x + width - bracket_len, y + height); ctx.line_to(x + width, y + height); ctx.line_to(x + width, y + height - bracket_len)
        ctx.stroke()
        
        # Label text
        select_cairo_font(ctx, "telemetry")
        ctx.set_font_size(18.0)
        ctx.set_source_rgba(0.7, 0.8, 0.9, 0.8)
        ctx.move_to(x + 16, y + 24)
        ctx.show_text(label.upper())
        
        # Value text
        ctx.set_font_size(24.0)
        ctx.set_source_rgba(cyan[0], cyan[1], cyan[2], 1.0)
        ctx.move_to(x + 16, y + 54)
        ctx.show_text(value)
    finally:
        ctx.restore()
```

### 4.2 Kinetic Caption Highlight Renderer
```python
def draw_kinetic_caption(ctx, text: str, highlight_word: str, cx: float, cy: float):
    """Draws centered caption ribbon with active word highlighted in gold."""
    ctx.save()
    try:
        select_cairo_font(ctx, "subtitle")
        ctx.set_font_size(44.0)
        
        words = text.split()
        # Measure total width
        total_w = sum(ctx.text_extents(w + " ")[4] for w in words)
        start_x = cx - (total_w / 2.0)
        
        # Draw sleek backing pill
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.70)
        ctx.rectangle(start_x - 24, cy - 44, total_w + 48, 64)
        ctx.fill()
        
        # Render words
        curr_x = start_x
        for w in words:
            word_str = w + " "
            ext = ctx.text_extents(word_str)
            if w.strip().upper() == highlight_word.strip().upper():
                ctx.set_source_rgba(1.0, 0.9, 0.0, 1.0) # Yellow highlight
            else:
                ctx.set_source_rgba(1.0, 1.0, 1.0, 0.95) # Crisp white
            ctx.move_to(curr_x, cy + 8)
            ctx.show_text(word_str)
            curr_x += ext[4]
    finally:
        ctx.restore()
```

