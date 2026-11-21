# Barbarik Option A: Procedural Animation Implementation Guide

## Overview
This guide provides an architectural code walkthrough demonstrating how the approved **Barbarik Option A (Sanskrit Puranic Account)** narration script and cinematic director's blueprint map 1:1 into production-ready Python Cairo code for `story-pipeline/SanatanKatha/kathas/barbarik.py`.

> [!NOTE]
> This document is a technical reference and implementation specification. In accordance with project workflow gates, production Python files are **not** modified until human review and approval of the skill package.

---

## 1. Narration & Timing Synchronization Map

The 7 scenes are synchronized with the frozen 184-word, 9-pause ($84.5\text{s}$ provisional) narration script:

| Scene | Key | Spoken Words | Pauses | Duration | Cumulative Bounds | Primary Visual Focus |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **01** | `hook` | 20 | 2 (1.0s) | 9.7s | `00.0s – 09.7s` | Kurukshetra dusk, Barbarik, 3 divine arrows, "SHEESH KYUN?" |
| **02** | `brahma` | 45 | 2 (1.0s) | 20.6s | `09.7s – 30.3s` | Lord Brahma on lotus throne, Yaksha Suryavarcas, "BRAHMA KA VARDAAN" |
| **03** | `homa_ash` | 24 | 1 (0.5s) | 10.9s | `30.3s – 41.2s` | 3-beat homa ash sequence (Offer $\to$ Refuse $\to$ Divine advice & Accept) |
| **04** | `chakra` | 23 | 1 (0.5s) | 10.5s | `41.2s – 51.7s` | Sudarshana Chakra, head preserved by Goddess Candika, "SUDARSHAN CHAKRA" |
| **05** | `hilltop` | 28 | 2 (1.0s) | 13.2s | `51.7s – 64.9s` | Head upon Mahisagara hill overlooking battle, "YUDH KA SAKSHI" |
| **06** | `hari_hara`| 33 | 1 (0.5s) | 14.8s | `64.9s – 79.7s` | Unified Hari-Hara composite form ($x=540$) via `ctx.clip()` |
| **07** | `blessing` | 11 | 0 (0.0s) | 4.8s | `79.7s – 84.5s` | Krishna's boon, petals shower, unobstructed deity, "KALYUG KA VARDAAN" |
| **Total**| — | **184** | **9 (4.5s)**| **84.5s**| — | *Under 90s YouTube Shorts hard limit* |

---

## 2. Custom Procedural Characters Implementation

### Context Ownership Contract in Character Routines
- `place(ctx, x, y, s, t, flip)` in `core/devta.py:170` executes `ctx.save()` internally to translate and scale.
- **Ownership**: The inner `draw()` closure calling `place()` owns the obligation to call `ctx.restore()`.
- **Callers**: Scene methods (e.g. `BrahmaScene.draw()`) calling `brahma()` do **not** call `ctx.restore()`.
- **Framing & Scaling**: Seated Lord Brahma uses $s = 0.74$ placed at $y = 720$, keeping the lotus throne elevated in the celestial realm while Yaksha Suryavarcas prostrates at $s = 0.68$ on the ground plane.

### 1. Lord Brahma (`brahma`) — Scene 2
Lord Brahma does not exist as a native primitive in `core/devta.py`. He is constructed via Cairo primitives adhering strictly to the context restoration contract:

```python
def brahma(ctx, x, y, s, t, pose="bless", flip=False, a=1.0):
    """Lord Brahma: Seated upon lotus throne, four-ring golden halo, white beard, abhaya mudra."""
    def draw():
        place(ctx, x, y, s, t, flip)  # Pushes ctx.save() internally
        
        # 1. Radiant multi-ring celestial halo
        halo(ctx, 0, -660, 200, t, c=GOLD_HI)
        glow(ctx, 0, -660, 320, GOLD, 0.4)
        
        # 2. Sacred pink/gold lotus throne
        dv.lotus(ctx, 0, -40, 140, t, col=hexc("#FFB3C7"))
        
        # 3. Pitambar robes & seated torso
        skin = dv.KRISHNA_SKIN  # divine golden-fair complexion
        # Dhoti folds
        smooth(ctx, [(-120, -60), (-160, -180), (-80, -280), (80, -280), (160, -180), (120, -60)])
        ink(ctx, hexc("#E8A824"))
        
        # Upper body & sacred thread (Yajnopavita)
        smooth(ctx, [(-70, -280), (-85, -500), (0, -530), (85, -500), (70, -280)])
        ink(ctx, skin)
        line(ctx, [(-60, -490), (0, -380), (60, -260)], WHITE, 4)
        
        # 4. Ascetic white beard & serene face
        ell(ctx, 0, -590, 85, 95)
        ink(ctx, skin)
        # White beard flow
        smooth(ctx, [(-45, -570), (-55, -450), (0, -370), (55, -450), (45, -570)])
        ink(ctx, WHITE)
        
        # 5. Golden multi-tiered crown (Mukut)
        smooth(ctx, [(-65, -670), (-75, -790), (0, -870), (75, -790), (65, -670)])
        ink(ctx, GOLD_HI)
        gem(ctx, 0, -780, 14, hexc("#D61F3A"))
        
        # 6. Blessing hand (Abhaya Mudra)
        if pose == "bless":
            limb(ctx, [(70, -480), (130, -510), (130, -590)], skin, 32)
            hand(ctx, 130, -605, skin, 24)
            glow(ctx, 130, -605, 90, GOLD_HI, 0.5 + 0.2 * math.sin(t * 4))
            
        ctx.restore()  # MANDATORY: Restores context state before exiting draw()
        
    dv.group(ctx, a, draw)
```

---

### 2. Hari-Hara Composite Form (`hari_hara`) — Scene 6
A unified single figure centered at $x = 540$, split down the center using `ctx.clip()`:

```python
def hari_hara(ctx, x, y, s, t, a=1.0):
    """Unified composite form: Left Half Vishnu (Hari), Right Half Shiva (Hara)."""
    def draw():
        place(ctx, x, y, s, t, flip=False)
        
        # -------------------------------------------------------------
        # LEFT HALF: SHRI HARI VISHNU (x <= 0 in local space)
        # -------------------------------------------------------------
        ctx.save()
        ctx.rectangle(-500, -1100, 500, 1300)
        ctx.clip()
        
        # Golden halo & cyan skin
        halo(ctx, 0, -640, 195, t, c=GOLD_HI)
        glow(ctx, -100, -640, 250, hexc("#6BA4FF"), 0.4)
        
        # Vishnu body & pitambar dhoti
        skin_v = dv.KRISHNA_SKIN
        smooth(ctx, [(-75, -280), (-85, -520), (0, -540), (0, -280)])
        ink(ctx, skin_v)
        smooth(ctx, [(-110, -50), (-140, -180), (-75, -280), (0, -280), (0, -50)])
        ink(ctx, hexc("#E8A824"))
        
        # Half Face & Crown with Mor-Pankh
        ell(ctx, 0, -640, 85, 95)
        ink(ctx, skin_v)
        smooth(ctx, [(-65, -720), (-75, -830), (0, -890), (0, -720)])
        ink(ctx, GOLD_HI)
        dv.peacock_feather(ctx, -35, -850, -0.3, 130, t)
        
        # Hand holding Sudarshana Chakra
        limb(ctx, [(-75, -480), (-160, -500), (-180, -610)], skin_v, 34)
        hand(ctx, -180, -625, skin_v, 22)
        # Spinning Sudarshana Chakra
        ctx.save()
        ctx.translate(-180, -680)
        ctx.rotate(t * 8)
        circle(ctx, 0, 0, 48, GOLD_HI, 0.9)
        for k in range(8):
            ang = k / 8 * math.tau
            line(ctx, [(36 * math.cos(ang), 36 * math.sin(ang)),
                       (56 * math.cos(ang), 56 * math.sin(ang))], GOLD, 6)
        ctx.restore()
        ctx.restore()  # End Vishnu clip
        
        # -------------------------------------------------------------
        # RIGHT HALF: MAHADEV SHIVA (x >= 0 in local space)
        # -------------------------------------------------------------
        ctx.save()
        ctx.rectangle(0, -1100, 500, 1300)
        ctx.clip()
        
        # Silver halo & sacred ash skin
        halo(ctx, 0, -640, 195, t, c=WHITE)
        glow(ctx, 100, -640, 250, hexc("#E0EAF5"), 0.35)
        
        skin_s = hexc("#D8E2E6")
        smooth(ctx, [(0, -280), (0, -540), (85, -520), (75, -280)])
        ink(ctx, skin_s)
        # Tiger-skin dhoti
        smooth(ctx, [(0, -50), (0, -280), (75, -280), (140, -180), (110, -50)])
        ink(ctx, hexc("#C46A28"))
        
        # Half Face & Matted Jata with Crescent Moon
        ell(ctx, 0, -640, 85, 95)
        ink(ctx, skin_s)
        smooth(ctx, [(0, -720), (0, -890), (70, -840), (60, -720)])
        ink(ctx, hexc("#2A1810"))
        # Crescent Moon
        ctx.arc(35, -820, 22, -0.8, 1.8)
        ctx.close_path()
        rgba(ctx, WHITE, 0.95)
        ctx.fill()
        
        # Hand holding Trishul
        limb(ctx, [(75, -480), (160, -490), (170, -580)], skin_s, 34)
        hand(ctx, 170, -595, skin_s, 22)
        # Golden Trishul staff
        line(ctx, [(170, -300), (170, -880)], GOLD_HI, 8)
        # Trishul prongs
        line(ctx, [(170, -880), (170, -960)], GOLD_HI, 8)
        line(ctx, [(135, -920), (170, -880), (205, -920)], GOLD_HI, 7)
        ctx.restore()  # End Shiva clip
        
        ctx.restore()  # MANDATORY: Pops place() context state
        
    dv.group(ctx, a, draw)
```

---

## 3. Scene Classes Architectural Implementation

### Scene 2: `BrahmaScene` ($09.7\text{s} – 30.3\text{s}$, $d = 20.6\text{s}$)
```python
class BrahmaScene(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "yaksha": c("SURYAVARCAS", d * 0.20),
            "shraap": c("SHRAAP", d * 0.50),
            "vardaan": c("VARDAAN", d * 0.78),
        }

    def events(self, d):
        b = self.beats(d)
        return [
            (0.02, "soft_thud"),
            (b["shraap"], "thud"),
            (b["vardaan"], "shimmer"),
        ]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        dv.sky(ctx, hexc("#1A1230"), hexc("#482555"), hexc("#8A4252"), 0.55)
        dv.stars(ctx, count=50, t=t)
        
        # Lord Brahma seated majestically in upper celestial realm
        brahma(ctx, 540, 720, 0.74, t, pose="bless")
        
        # Yaksha Suryavarcas prostrating in lower realm
        u = clamp((t - b["shraap"]) / 0.8)
        dv.barbarik(ctx, 540, GROUND - 10, 0.68, t, pose="sharan", a=1.0)
        
        # Blessing aura rays extending downwards
        if t > b["vardaan"]:
            v = t - b["vardaan"]
            glow(ctx, 540, 850, 450, GOLD_HI, 0.4 * clamp(v / 0.5))
            dv.ribbon(ctx, "BRAHMA KA VARDAAN", 540, 280, v, size=80)
        else:
            dv.ribbon(ctx, "YAKSHA SURYAVARCAS", 540, 280, t - b["yaksha"], size=80)
```

### Scene 3: `HomaAshScene` ($30.3\text{s} – 41.2\text{s}$, $d = 10.9\text{s}$)
```python
class HomaAshScene(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "offer": c("VIJAYA", 0.0),       # Beat 1: 0.0 - 3.8s
            "refuse": c("PEHLE", 3.8),       # Beat 2: 3.8 - 7.2s
            "accept": c("DEVTAON", 7.2),     # Beat 3: 7.2 - 10.9s
        }

    def events(self, d):
        b = self.beats(d)
        return [
            (0.02, "soft_thud"),
            (b["refuse"], "ghanti"),
            (b["accept"], "shimmer"),
        ]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        meadow(ctx, t)
        
        # Sacred Yagya Kunda at center-left
        dv.yagya_kund(ctx, 420, GROUND - 10, 0.85, t, flame=1.0)
        
        # Brahmin Vijaya on left (x = 240)
        dv.brahmin(ctx, 240, GROUND - 10, 0.75, t, pose="stand")
        
        # Beat logic
        if t < b["refuse"]:
            # Beat 1: Vijaya offers sacred ash
            pose = "stand"
            msg = "YAGYA KI PAVITRA BHASMA"
            u_ribbon = t - b["offer"]
        elif t < b["accept"]:
            # Beat 2: Barbarik politely declines
            pose = "namaste"
            msg = "BARBARIK KA SANKOCH"
            u_ribbon = t - b["refuse"]
        else:
            # Beat 3: Divine advice -> Barbarik accepts
            pose = "sharan"
            msg = "DEV AAGYA SE SWEEKAR"
            u_ribbon = t - b["accept"]
            # Celestial light beam descends upon Barbarik
            glow(ctx, 820, GROUND - 300, 250, GOLD_HI, 0.45)
            
        # Barbarik on right (x = 820)
        dv.barbarik(ctx, 820, GROUND - 10, 0.75, t, pose=pose, flip=True)
        
        # Sleek top ribbon
        dv.ribbon(ctx, msg, 540, 280, u_ribbon, size=76)
```

### Scene 6: `HariHaraScene` ($64.9\text{s} – 79.7\text{s}$, $d = 14.8\text{s}$)
```python
class HariHaraScene(Cued):
    def beats(self, d):
        c = self.cue
        return {
            "form": c("HARI-HARA", d * 0.35),
            "awe": c("DARSHAN", d * 0.70),
        }

    def events(self, d):
        b = self.beats(d)
        return [
            (0.02, "soft_thud"),
            (b["form"], "boom"),
            (b["awe"], "shimmer"),
        ]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        battlefield(ctx, t, dim=0.6, armies=False)
        
        # Central unified Hari-Hara form
        hari_hara(ctx, 540, 840, 0.76, t, a=1.0)
        
        # Preserved Barbarik head on lower right vantage point looking up in awe
        head_y = GROUND - 120 + 6 * math.sin(t * 2)
        glow(ctx, 920, head_y, 140, GOLD, 0.5)
        # Sheesh drawing...
        
        dv.ribbon(ctx, "EK HI ROOP: HARI-HARA", 540, 280, t - b["form"], size=82)
```

---

## 4. Thumbnail Routine Specification

The cover art is generated at full $1080 \times 1920$ resolution:
```python
def thumbnail(ctx):
    """1080x1920 YouTube Shorts thumbnail cover for Barbarik Option A."""
    temple_bg(ctx, 0.0)
    
    # 1. Radiant central Khatu Shyam sheesh roop
    dv.shyam(ctx, 540, 1080, 1.05, 0.3, garland=1.0)
    
    # 2. Flanking celestial divine arrows
    for k in range(3):
        dv.divine_arrow(ctx, 310 + 230 * k, 620 - 45 * (k == 1), -math.pi / 2, 170, 0.3)
        
    # 3. Top gradient mask for maximum typography readability
    g = cairo.LinearGradient(0, 0, 0, 680)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.95)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    ctx.rectangle(0, 0, W, 680)
    ctx.set_source(g)
    ctx.fill()
    
    # 4. Bold two-tone title
    text(ctx, "SHEESH KYUN", 540, 240, 190, GOLD_HI, font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=24)
    text(ctx, "MAANGA?", 540, 450, 210, (1, 1, 1), font=CAPTION_FONT, bold=False, stroke=(0, 0, 0), stroke_w=24)
```

