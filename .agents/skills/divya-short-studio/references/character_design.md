# Character design - how to draw beautiful, alive Cairo characters

Study these first (they are the approved look):
- `kathas/ghatotkach_akshauhini.py` -> `_ghatotkach_body` (giant rakshasa prince), `_duryodhan_body` (villain king),
  `soldier` (crowd unit)
- `core/devta.py` -> `_krishna_body/_krishna_head`, `_karna_body/_karna_head`

## 1. The style in one line
Flat bright colours + a dark ink outline round EVERY shape + one soft white sheen + big expressive eyes + gold
ornaments. Built only from `ell`, `smooth` (spline), `limb`, `rrect`, `circle`, `gem`. Never trace or copy art.

Core helpers (`core/devta.py`):
| helper | use |
|---|---|
| `smooth(ctx, pts, k=1/6)` then `ink(ctx, colour)` | any organic shape: torso, dhoti, hair, crown. `k=0.05-0.08` = sharper points (crown, horns, flames), `k=0.12` = soft body |
| `limb(ctx, [shoulder, elbow, hand], skin, width)` | arms/legs as inked tubes - draw upper arm and forearm as two calls so the elbow bends cleanly |
| `ell(...)` + `ink(...)` | head, feet, pauldrons, ears |
| `sheen(ctx, x, y, rx, ry, 0.15-0.22)` | one cel highlight on head + chest = instant "3D" |
| `eye(ctx, x, y, rx, ry, t, look=(lx, ly), iris=..., lid=0..1, skin=skin, seed=n)` | blinks by itself; `look` aims the pupils; `lid` = angry/sleepy |
| `gem(ctx, x, y, r, colour)` | crown, belt, armour centre - always with its white glint |
| `glow(ctx, x, y, r, colour, a)` | aura, fire, eye glow, hit flash |

## 2. Local coordinate system (every character uses the same one)
- Feet at (0, 0), y is negative upward. Full height ~900-1000 units (crown top).
- Shoulders y ~ -515 (normal) / -680 (giant), head centre y ~ -690 / -805, waist ~ -360 / -440.
- Drawn on screen with scale 0.68-0.80 so the crown lands at y ~ 480-550.

## 3. Draw order (back to front) - never change it
1. Hair mass / cape / anything BEHIND the head (so the face sits on top)
2. Legs + feet (+ gold anklets)
3. Dhoti / lower garment (+ gold hem line)
4. Torso, then chest details (muscle arcs, armour plates, straps, belt + gem)
5. Weapon held behind the arm (gada raised overhead)
6. Arms (upper + fore), armlets, hands
7. Shoulder pieces (pauldrons) over the arm joints
8. Neck -> ears/earrings -> head -> sheen
9. Crown/horns -> brows -> eyes -> nose -> moustache -> mouth -> tusks
10. Effects that belong to the character (palm fire, hit glow) last

## 4. Make every character instantly recognisable (silhouette + palette)
Give each one 3 signature features and a 3-colour palette nobody else uses:
| character | skin | signature features | palette |
|---|---|---|---|
| Ghatotkach | storm blue `#3D6F8E` | flame hair with red tips, small ivory horns, upward tusks, ember-orange glowing eyes, spiked bronze pauldrons, giant gada | blue / crimson dhoti / bronze-gold |
| Duryodhan | wheat `#D29A68` | tall 5-point mukut, curled moustache, brows angled down to centre, upright gada | purple-maroon armour / indigo dhoti / gold |
| Karna | `#D99A62` | golden kavach scales, kundal, Surya disc on mukut, bow | gold / saffron / maroon belt |
| Krishna | blue `#4F86E0` | mor-pankh, flute or abhaya, pitambar | blue / yellow / gold |
| Soldiers | `#C98A5A` | bronze helmet, maroon tunic, spear + shield | kept small and simple so heroes pop |
Rules: royals get crowns, commoners/rishis never; never reuse one sprite for two different people; demon/rakshasa =
fierce but not ugly or gory (heroic, cartoon).

## 5. Faces carry the emotion
- Brows: `line()` from outer-high to inner-low = angry; inner-high = sad/worried; flat = calm.
- Eyes: `look=(0.6, 0)` to face the other character (eye contact!), `(0, -0.6)` looking up in fear/awe,
  `(0, 0.6)` lowered in guilt/doubt. `lid=0.2` = fierce.
- Mouth: closed line = calm; `ell` dark-red opening with a strip of white teeth = roar/shout;
  animate the size with `roar = 0.4 + 0.6 * abs(math.sin(t * 2.2))` so the shout pulses.
- Glow behind eyes (`glow(... FIRE_O, 0.55)`) for supernatural power.

## 6. Poses = a `pose=` argument that only changes arm/hand points
```python
Ls, Rs = (-195, -682), (195, -682)          # shoulders
if pose == "roar":   arms = [(Ls, (-300, -800), (-262, -930)), (Rs, (300, -650), (372, -720))]
elif pose == "hit":  arms = [(Ls, (-245, -540), (-70, -600)), (Rs, (245, -540), (70, -610))]
else:                arms = [(Ls, (-262, -540), (-250, -410)), (Rs, (285, -540), (175, -470))]
```
Write a pose for every action the voice-over names (roar, point, panic, raise, throw, hit, namaste, bless...).
Adding a pose to a shared rig in `core/devta.py` = add a NEW `elif`, never edit an old one.

## 7. Rig template (copy, rename, fill)
```python
def hero(ctx, x, y, s, t, pose="stand", look=(0.0, 0.0), rot=0.0, a=1.0):
    def draw():
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(rot)                               # falls/tilts pivot on the feet
        ctx.scale(s, s * (1 + 0.014 * math.sin(t * 2.4)))   # breathing = always alive
        _hero_body(ctx, t, pose, look)
        ctx.restore()                                 # ALWAYS - a missing restore mirrors all later text
    dv.group(ctx, a, draw)                            # whole-figure fade without seams
```
Idle life for free: breathing scale, `eye()` blinks, hair/flag `math.sin(t * k)` sway, aura `pulse`.

## 8. Crowds and scale contrast
A crowd unit is ~140 local units tall drawn at s 0.4-0.55, in two rows (back row smaller and 75% alpha).
Modes stand / look (eyes up, mouth open) / panic (running legs `sin(t*14)`, arms up). Tiny crowd next to a 0.80 hero
= the hero feels gigantic without breaking the scale rule.

## 9. Self-check on the preview sheet
Crown below y ~ 480? Nothing cut at the screen edge? Face not hidden by an effect? Each character readable as a
silhouette? Two characters looking AT each other? If any answer is no, fix before showing the user.
