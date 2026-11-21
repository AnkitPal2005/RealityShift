# Cairo Animation Engine: Concrete Capabilities, Catalog & Constraints

This reference document establishes the verified inventory of procedural rendering primitives, coordinate systems, camera math, and technical boundaries supported by the **Sanatan Katha** animation pipeline (`story-pipeline/SanatanKatha/core/`).

---

## 1. Canvas Specification & Coordinate System

- **Resolution**: 1080 $\times$ 1920 pixels (9:16 vertical video for YouTube Shorts).
- **Frame Rate**: 30 FPS (`FPS = 30`).
- **Global Time (`t`)**: Floating-point seconds from the start of the Short.
- **Scene Local Time (`tl`)**: Floating-point seconds within current scene (`0.0 \le tl \le \text{dur}`).
- **Normalized Progress (`u`)**: $\text{clamp}(tl / \text{dur}, 0.0, 1.0)$.
- **Ground Datum**: `GROUND = 1180` (character feet sit at `GROUND - 10` $\approx 1170$).
- **Top Safe Line**: $y \approx 280$ (below header diya bar $y = 78–146$).
- **Bottom Safe Line**: $y \approx 1220$ (above bottom kinetic captions at `CAP_Y = 1290`).

### The 5 Visual Stacking Layers:
```
Layer 5 (Top Overlay): Diya Header (y = 78–146) + Scroll Captions (y = 1290)
       ↑
Layer 4 (UI Ribbon): Single sleek title ribbon at x = 540, y = 280–320 (Roman transliteration)
       ↑
Layer 3 (Foreground Atmosphere): Floating lotus petals (dv.petals), drifting battle dust, light flares
       ↑
Layer 2 (Midground Stage): Ground rect (y = 1180), active characters, fire altar, props
       ↑
Layer 1 (Background Environment): Celestial sky gradients, sun/moon discs, hills, trees, army silhouettes
```

---

## 2. Supported Camera Transformations (2D Affine Matrix)

The compositor operates on an unaccelerated 2D Cairo surface. All camera movements are achieved via matrix transformations inside `ctx.save()` / `ctx.restore()` blocks:

### 2.1 Smooth Zoom / Push-in
```python
ctx.save()
zoom = 1.0 + 0.12 * ease_out_cubic(clamp(tl / dur))
# Zoom towards subject at (cx, cy):
ctx.translate(cx, cy)
ctx.scale(zoom, zoom)
ctx.translate(-cx, -cy)
# ... draw world elements ...
ctx.restore()
```

### 2.2 Multi-Layer Parallax Panning
```python
# Layer 1 (Far BG hills): moves slowly
hill_x = -30 * u
# Layer 2 (Midground trees): moves medium
tree_x = -70 * u
# Layer 3 (Foreground characters): moves full speed
char_x = lerp(x0, x1, ease_in_out(u))
```

### 2.3 Divine Impact Shake
```python
if impact_active:
    dx = (rnd(tl * 30, 1.0) - 0.5) * 14.0
    dy = (rnd(tl * 30, 2.0) - 0.5) * 14.0
    ctx.translate(dx, dy)
```

---

## 3. Detailed Primitive Catalog: Supported vs. Custom vs. Unsupported

### 3.1 Fully Supported in `core/devta.py` (Ready for Direct Call)

| Primitive | Signature | Supported Options / Controls | Visual Purpose |
| :--- | :--- | :--- | :--- |
| **`dv.krishna`** | `(ctx, x, y, s, t, pose, look, smile, flip, a, aura)` | `pose="stand"`, `"flute"`, `"bless"`, `aura=True`, `smile=1.0` | Shri Krishna / Vishnu avatar. |
| **`dv.barbarik`** | `(ctx, x, y, s, t, pose, mood, draw_amt, arrows, look, flip, a)` | `pose="stand"`, `"aim"`, `"shot"`, `mood="fierce"`, `"calm"`, `arrows=3` | Barbarik as royal warrior/archer. |
| **`dv.devi`** | `(ctx, x, y, s, t, pose, look, flip, a, aura)` | `pose="bless"`, `aura=True` | Goddess Candika / Durga / Devi manifestations. |
| **`dv.brahmin`** | `(ctx, x, y, s, t, pose, mood, look, flip, a, hint)` | `pose="stand"`, `mood="smile"`, `hint=0.0` | Elderly Brahmin, Sage Vijaya, disguised ascetics. |
| **`dv.shyam`** | `(ctx, x, y, s, t, garland, a, aura)` | `garland=1.0`, `aura=1.0` | Khatu Shyam crowned sacred sheesh roop. |
| **`dv.yagya_kund`** | `(ctx, x, y, s, t, a)` | Tiered brick altar with procedural leaping flame ribbons | Homa, yagya rituals, sacred fire. |
| **`dv.peepal`** | `(ctx, x, y, s, t, marks, hidden)` | Heart-shaped foliage, leaf pierce markers, hidden leaf | Sacred Peepal tree. |
| **`dv.balance`** | `(ctx, x, y, s, tilt, t, labels, a)` | Scales with customizable balance pans (`JEET`, `HAAR`) | Moral weighing, vows. |
| **`dv.hill`** | `(ctx, x, y, w, h, c)` | Layered parabolic silhouettes | Mountain peaks, Kurukshetra ridges. |
| **`dv.army`** | `(ctx, x0, x1, y, n, c, t, flag_c, seed, a)` | Silhouetted marching battalions with waving flags | Kurukshetra battle line. |
| **`dv.petals`** | `(ctx, t, n, seed, a)` | Drifting, rotating pink sacred lotus petals | Devotional showers, divine blessings, non-violent death. |
| **`dv.lotus`** | `(ctx, x, y, s, c, a)` | Blooming lotus flower | Divine thrones, offerings. |
| **`dv.divine_arrow`**| `(ctx, x, y, ang, L, t, a, trail)` | Glowing arrow with motion trail and angular orientation | Astras, arrows in flight. |
| **`dv.sun_disc`** | `(ctx, x, y, r, t, a, rays)` | Solar disc with animated rotating rays | Celestial radiance, Surya, cosmic energy. |
| **`dv.stars`** | `(ctx, t, n, a)` | Twinkling multi-point starlight | Night skies, cosmic realms. |
| **`dv.sky`** | `(ctx, top, mid, bottom, mid_at)` | 3-stop smooth vertical background gradient | Sky and atmosphere. |
| **`dv.ribbon`** | `(ctx, label, x, y, u, c, size, sub, rot)` | Animated entrance ribbon at $x=540, y=280–320$ | Capitalized Roman title cards. |
| **`dv.silhouette`**| `(ctx, draw, c, a)` | Renders any drawing routine as a flat backlit shadow | Past-life incarnations, shadows, mystery figures. |

---

### 3.2 Partially Supported (Requires Custom Katha-Level Procedural Routine)

These entities do not have a pre-built single function in `devta.py`, but are **fully implementable in procedural Cairo** by defining a local function inside the katha module (following the proven pattern in `mahadev_ganga.py` and `ram_hanuman.py`):

1. **Lord Brahma (`brahma`)**:
   - *Implementation Pattern*: Procedural figure with golden crown, white beard, yellow-white robes, seated upon `dv.lotus`, holding akshamala and kamandalu, with an expansive golden halo (`dv.halo`).
2. **Unified Hari-Hara (`hari_hara`)**:
   - *Implementation Pattern*: A single composite body rig centered at $x=540$, split down the central axis using Cairo clipping paths (`ctx.clip()`):
     - Left half: Ash-smeared skin (`#B0C4DE`), matted hair (*jata*), crescent moon, tiger skin sash, holding `dv.trishul`.
     - Right half: Cyan-blue skin (`#74B4E8`), golden *kirita mukut*, yellow Pitambar dhoti, Kaustubha gem, holding rotating Sudarshana Chakra.
3. **Lord Shiva / Mahadev (`mahadev`)**:
   - *Implementation Pattern*: Precedent established in `mahadev_ganga.py` using blue skin (`#8CB0D4`), tiger skin, Ganga fountain from jata, and crescent moon.
4. **Shri Rama (`shri_ram`)**:
   - *Implementation Pattern*: Precedent established in `ram_hanuman.py` using deep saffron dhoti, warrior mukut (NO peacock feather), Kodanda bow on shoulder, and Raghuvanshi tilak.

---

### 3.3 Completely Unsupported Features (NEVER Propose)

| Unsupported Feature | Why It Fails in Engine | Mandatory Workaround |
| :--- | :--- | :--- |
| **3D Mesh Deformation / Rigging** | Engine is an unaccelerated 2D vector Cairo surface; no 3D vertex pipeline exists. | Use multi-part 2D vector limb articulation (`dv.limb`, `dv.smooth`). |
| **GLSL / HLSL GPU Shaders** | Engine renders CPU-bound Cairo frames to NumPy buffers; no OpenGL/DirectX context. | Use layered vector gradients (`glow()`, radial gradients, multi-stop `dv.sky()`). |
| **Devanagari Font on Ribbon** | Cairo `CAPTION_FONT` (`Impact`) lacks Devanagari glyphs; causes empty tofu boxes (`□□□`). | All ribbons must use **capitalized Roman transliteration** (e.g., `SUDARSHAN CHAKRA`). |
| **Fluid Simulation (Blood / Water)** | No Navier-Stokes or fluid particle solver exists. | Use expanding concentric circles, wave arcs, and drifting petals (`dv.petals`). |
| **Graphic Decapitation / Violence** | Violates YouTube YPP policies and sacred devotional decorum. | Depict sacrifice through blinding white light (`flash()`), ascending prana, and lotus showers. |

---

## 4. Staging Rules & Proportions (Zero Screen Clipping)

- **Character Scale**: Strictly between **`0.68` and `0.80`** (standard single character: `0.74–0.78`).
- **Single Character Staging**: Centered horizontally at $x = 540$, feet on `GROUND - 10` ($y \approx 1170$).
- **Two Character Staging**:
  - Left character: $x \approx 240–280$.
  - Right character: $x \approx 760–800$ (`flip=True` to face left).
  - Keeps a clean 500px interaction corridor in the center for props (`dv.yagya_kund`, `dv.balance`).
- **Three Character Staging**:
  - Central deity/prop at $x = 540$.
  - Flanking characters at $x = 220$ and $x = 860$ (scale reduced to `0.65–0.68`).
