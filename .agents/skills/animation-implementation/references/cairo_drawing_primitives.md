# Cairo Drawing Primitives & API Catalog

## Overview
This catalog documents the verified procedural drawing primitives available in `story-pipeline/SanatanKatha/core/devta.py` and `core/katha.py`. Every function signature, coordinate constraint, and parameter type has been audited against actual engine code.

The engine divides capabilities into three distinct tiers:
1. **Tier 1: Native Primitives** (Call directly from `core.devta` or `core.katha`)
2. **Tier 2: Custom Procedural Routines** (Must be authored inside `kathas/<story>.py`)
3. **Tier 3: Unsupported Features** (Strictly prohibited by engine architecture)

---

## Tier 1: Native Primitives Catalog

### 1. Characters (`core/devta.py`)

#### `dv.barbarik(ctx, x, y, s, t, pose="stand", arrows=0, look=(0, 0), mood="calm", a=1.0)`
Renders warrior Barbarik with warrior mukut, armor, earrings, and quiver.
- `x, y`: Coordinate of feet baseline (standard $y \approx 1170$).
- `s`: Scale (recommended standard $0.68 \le s \le 0.80$ for standing dialogue; $0.30–0.60$ for distant figures; $0.85–1.10$ for close-up/thumbnails).
- `t`: Local scene time in seconds (powers breathing and ornament sway).
- `pose`:
  - `"stand"`: Neutral warrior stance.
  - `"bow"`: Archer pose holding bow.
  - `"aim"`: Full draw aiming at target.
  - `"namaste"`: Palms pressed together in reverence.
  - `"sharan"`: Prostrating or kneeling in surrender.
- `arrows`: Integer ($0 \dots 3$). Number of divine arrows visibly resting in his back quiver.
- `look`: `(dx, dy)` normalized gaze direction for pupils.
- `mood`: `"calm"`, `"determined"`, or `"humble"`.
- `a`: Opacity multiplier ($0.0 \dots 1.0$).

#### `dv.krishna(ctx, x, y, s, t, pose="flute", flip=False, a=1.0, look=(0, 0))`
Renders Shri Krishna with blue skin, pitambar yellow dhoti, mor-pankh, and golden ornaments.
- `pose`:
  - `"flute"`: Classic Tribhanga posture playing bansuri.
  - `"bless"`: Abhaya mudra blessing posture with right hand raised.
  - `"ask"`: Hand extended demanding charity (*daan*).
  - `"chakra"`: Holding spinning Sudarshana Chakra on index finger.
- `flip`: If `True`, flips character horizontally to face left.

#### `dv.brahmin(ctx, x, y, s, t, pose="stand", flip=False, a=1.0)`
Renders Shri Krishna disguised as an elderly, witty ascetic brahmin.
- Rustic cotton dhoti, wooden walking staff, tilak, and gentle white beard.
- `pose`: `"stand"`, `"test"` (challenging with raised finger), `"smile"`.

#### `dv.shyam(ctx, x, y, s, t, garland=1.0, a=1.0)`
Renders the consecrated Khatu Shyam divine idol / sheesh roop.
- Glowing blue/black sheesh, intricate golden crown, pearl necklaces, and fresh rose garlands.
- `garland`: Float ($0.0 \dots 1.0$) controlling garland bloom and decoration detail.

#### `dv.devi(ctx, x, y, s, t, pose="bless", flip=False, a=1.0)`
Renders the Divine Mother / Goddess Candika.
- Radiant crimson sari, golden crown, multiple celestial arms with blessing mudras and lotus.

---

### 2. Sacred Props & Celestial Artifacts (`core/devta.py`)

#### `dv.divine_arrow(ctx, x, y, ang, L, t, trail=0.0, a=1.0)`
Renders a glowing celestial arrow with golden shaft, energy tip, and light fletching.
- `x, y`: Center of arrowhead.
- `ang`: Angle of flight in radians ($-\pi/2$ points straight up, $0$ points right, $\pi$ points left).
- `L`: Arrow length in pixels (standard $\approx 150 - 170\text{px}$).
- `trail`: Trail glow intensity ($0.0 \dots 1.0$).

#### `dv.yagya_kund(ctx, x, y, s, t, flame=1.0)`
Renders a sacred Vedic sacrificial fire altar (*homa kunda*).
- Multi-tiered copper/brick steps, glowing embers, and animated licking fire tongues.
- `flame`: Scale multiplier for active flame height.

#### `dv.peepal(ctx, x, y, s, t, leaves=True)`
Renders the sacred Peepal tree (*Ficus religiosa*) with sweeping branches and hanging roots.
- Provides access to leaf coordinates via `dv.LEAVES` list.

#### `dv.balance(ctx, x, y, s, tilt, t, labels=("JEET", "HAAR"))`
Renders golden scales of justice / dharma.
- `tilt`: Angle of balance beam in radians (positive tilts right side down).
- `labels`: Tuple of two Roman uppercase strings displayed on left and right pans.

#### `dv.lotus(ctx, x, y, r, t, col=None, a=1.0)`
Renders a sacred blossoming lotus flower with radiating petals and glowing stamens.

#### `dv.petals(ctx, t, count=40, seed=1, col=None)`
Renders a shower of gentle celestial flower petals floating and tumbling down the screen.

---

### 3. Atmospheric Scenery & Backgrounds (`core/katha.py` & `core/devta.py`)

#### `battlefield(ctx, t, dim=1.0, armies=True)`
Renders the Kurukshetra dusk battlefield.
- Multi-stop dusk gradient sky (purple to rust orange).
- Red-tinted setting sun disc on the horizon ($y = 900$).
- Layered rolling hill silhouettes with atmospheric haze.
- Distant marching army silhouettes on left and right flanks.
- Drifting ground war dust particles.

#### `meadow(ctx, t)`
Renders a bright, peaceful Vedic forest meadow.
- Morning azure and amber sky gradient.
- Rolling green meadow slopes with animated blades of grass.

#### `temple_bg(ctx, t)`
Renders a sacred temple sanctum interior.
- Deep crimson/mahogany temple darkness.
- Rotating golden light rays radiating from central sanctum.

#### `dv.sky(ctx, c_top, c_mid, c_bot, split=0.5)`
Creates a three-stop vertical atmosphere gradient across the entire $1080 \times 1920$ canvas.

#### `dv.stars(ctx, count=80, seed=1, twinkle=True, t=0.0)`
Renders a celestial starfield across the upper canvas.

---

### 4. UI & Graphics Primitives (`core/devta.py` & `core/engine.py`)

#### `dv.ribbon(ctx, msg, x, y, u, size=84, sub=None)`
Renders a sleek cinematic graphic banner.
- `msg`: **MUST be Roman uppercase transliteration** (e.g. `"KARM CHAKRA"`, `"SHEESH KYUN?"`).
- `x, y`: Screen position (standard center $x = 540, y = 280 - 320$).
- `u`: Animation progress parameter ($u = t - \text{beat\_time}$). Automatically handles `ease_out_back` entry.
- `size`: Typography size.
- `sub`: Optional smaller subtitle line beneath main title (Roman uppercase).

#### `glow(ctx, x, y, r, col, a=1.0)`
Renders a multi-stop radial glow aura centered at $(x, y)$ with radius $r$.

#### `circle(ctx, x, y, r, col, a=1.0)`
Renders a filled anti-aliased circle.

#### `line(ctx, pts, col, w=2, a=1.0)`
Renders a connected multi-point polyline with stroke width $w$.

#### `rrect(ctx, x, y, w, h, r)`
Constructs a rounded rectangle path with corner radius $r$.

---

## Tier 2: Custom Procedural Extensions Catalog

When a scriptural narrative requires a figure or visual structure not packaged natively in `core/devta.py`, the animator implements a dedicated procedural function directly inside `kathas/<story_name>.py`.

### 1. Lord Brahma (`brahma`)
*Required for: Skanda Purana Barbarik curse/boon narrative.*
- **Anatomy**:
  - Throne: Seated in Padmasana atop `dv.lotus(ctx, 0, -30, 120, t)`.
  - Aura: Four-ring concentric golden halo (`halo(ctx, 0, -640, 190, t, c=GOLD_HI)`).
  - Beard: Majestic ascetic white beard (`smooth`, white ink).
  - Crown: Triple-peaked golden mukut with glowing jewel.
  - Hands: Right hand in Abhaya mudra blessing rays, left hand holding sacred kamandalu.

### 2. Hari-Hara Composite Form (`hari_hara`)
*Required for: Skanda Purana Barbarik battlefield vision.*
- **Anatomy**: Single unified torso centered at $x = 540$, partitioned cleanly via `ctx.clip()`:
  - **Left Half (Hari / Vishnu)**:
    - Cyan skin (`dv.KRISHNA_SKIN`), yellow silk pitambar dhoti.
    - Peaked royal mukut adorned with peacock feather (`dv.peacock_feather`).
    - Hand holding rotating golden Sudarshana Chakra with divine energy arcs.
  - **Right Half (Hara / Shiva)**:
    - Fair / sacred ash skin (`#D8E2E6`), tiger-skin dhoti.
    - Matted ascetic locks (*jata*) adorned with silver crescent moon.
    - Hand holding golden Trishul with damaru.

### 3. Maryada Purushottam Shri Ram (`shri_ram`)
*Required for: Ramayana / Hanuman Leela stories.*
- **Anatomy**:
  - Royal Ayodhya warrior mukut (NO peacock feather!).
  - Raghuvanshi tilak on forehead.
  - Golden Kodanda bow slung on left shoulder.
  - Deep saffron and gold warrior robes.

### 4. Pawanputra Hanuman (`hanuman`)
*Required for: Ramayana / Sundarkand narratives.*
- **Anatomy**:
  - Glowing sindoori-orange complexion (`#E05B16`).
  - Heroic vanara facial structure and golden mukut.
  - Either seated in true Padmasana or standing with golden Gada.
  - Peaceful curving tail resting behind.

---

## Tier 3: Unsupported Engine Capabilities (Strictly Prohibited)

| Proposed Feature | Why It Is Incompatible | Mandatory Procedural Solution |
| :--- | :--- | :--- |
| **Devanagari text on ribbons** | Cairo `Impact` font lacks Hindi glyphs; renders empty tofu boxes (`□□□`). | Use capitalized Roman transliteration (e.g. `"JAI SHRI KRISHNA"`). |
| **3D Mesh Rigging / Skeletal Bones** | Engine is pure 2D vector path rendering on CPU. | Use trigonometric rotation (`math.sin(t * freq)`) and layer layering. |
| **GPU Fragment / GLSL Shaders** | Engine renders via Pycairo surfaces to NumPy CPU arrays. | Use multi-stop radial and linear gradients (`cairo.RadialGradient`). |
| **Fluid / Particle Physics Engines** | No PhysX or Box2D integrations. | Use deterministic sinusoidal particle loops with `rnd()` hash seeds. |
| **Graphic Decapitation / Gore** | Violates channel dignity and YouTube advertiser-friendly guidelines. | Use celestial light dissolution, golden aura flares, and lotus flower showers. |

