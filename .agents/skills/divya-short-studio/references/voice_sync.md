# Voice sync - characters move exactly on the spoken words

The rule: **whatever the narrator says, the viewer SEES at that same instant.** "Bada hua" -> he grows on "BADA".
"Chala di" -> the spear leaves the hand on "CHALA". "Gira" -> the body hits the ground on "GIRA".

## 1. How timing reaches your scene
- Each scene's `vo` line is split into caption chunks: `("वो आसमान तक बढ़ा,", "WO AASMAAN TAK BADHA,")`.
- At render, Whisper word timings of the user's KikiVoice clip give every chunk a start time inside the scene.
- `self.cue("WORD", default)` returns the start of the first chunk whose caption contains WORD
  (`default` is used in `--preview`, where chunks are spread evenly).
So: **keep chunks short (2-5 words) and put the action word near the start of its chunk.** If the action word sits at
the end of a long chunk, add an offset (`+ 0.3`) or split the chunk (`("गिरा!", "GIRA!")` alone).

## 2. Step 1 - write a beat table BEFORE coding
For each scene list: spoken word -> what moves -> SFX.
| scene | word (cue) | visual | sfx |
|---|---|---|---|
| raat | BHEEM | Ghatotkach switches stand -> roar | thud |
| raat | DUGNI | violet aura rings + scale 0.62 -> 0.70 | whoosh + boom |
| maya | AASMAAN | grows 0.70 -> 0.80 (ease_out_back) | boom |
| maya | AAG | fireballs start, crowd panics | whoosh + thuds on impacts |
| bhagdad | CHEEKHA | Duryodhan panic -> point + shouting mouth | whoosh |
| vasavi | INDRA / ARJUN | spear glows in raised hand / Karna lowers eyes | shimmer |
| vasavi | CHALA DI | throw pose, spear flies 0.35 s, hit flash + shake | arrow, boom |
| gira | PAHAAD | grows + rumble | whoosh + thud |
| gira | SEEDHA ... GIRA | topples, impact on GIRA | whoosh, boom |
| twist | KRISHNA / ARJUN | Krishna smile + abhaya / Arjun shock -> namaste | shimmer / ghanti |

## 3. Step 2 - code it with beats(), events(), draw()
```python
class Vasavi(Cued):
    FLIGHT = 0.35
    def beats(self, d):
        throw = self.cue("CHALA DI", d * 0.82) + 0.3        # land on the word, not the chunk start
        return {"arjun": self.cue("ARJUN", d * 0.4), "throw": throw, "hit": throw + self.FLIGHT}

    def events(self, d):                                       # SFX on the SAME beats
        b = self.beats(d)
        return [(b["throw"], "arrow"), (b["hit"], "boom")]

    def draw(self, ctx, t, d):
        b = self.beats(d)
        thrown = t >= b["throw"]
        doubt = b["arjun"] <= t < b["throw"]                   # eyes down while the line talks about Arjun
        dv.karna(ctx, 830, GROUND - 10, 0.72, t, pose="throw" if thrown else "raise",
                 look=(0.0, 0.6) if doubt else (-0.7, 0.0))
        ...
```
Always use `beats()` in both `events()` and `draw()` so sound and picture can never drift apart.

## 4. Step 3 - motion that feels alive, not switched
Never jump a value at the beat; ease it over 0.3-0.9 s starting AT the beat:
| motion | formula |
|---|---|
| grow / pop in | `lerp(a, b, ease_out_back(clamp((t - beat) / 0.8), s=1.2))` |
| fade in | `clamp((t - beat) / 0.4)` as alpha |
| fall (gravity) | `rot = 1.42 * ease_in((t - fall) / 0.9)` with `ease_in(u) = u*u` |
| projectile | `f = (t - throw) / FLIGHT`; `lerp` start->target; angle `math.atan2(ty - sy, tx - sx)` |
| shake after impact | `amp = 22 * math.exp(-(t - impact) * 4)`; `ctx.translate(amp*sin(t*47), amp*cos(t*41))` |
| flash | `flash(ctx, t - impact, dur=0.35)` |
| shouting / roaring | `0.4 + 0.6 * abs(math.sin(t * 9))` while the character speaks |
| idle (always on) | breathing, blinking, flags/hair `sin(t*k)`, embers drifting |
Pose changes (`stand -> roar`, `raise -> throw`, `shock -> namaste`) happen exactly at the beat; the easing on
scale/glow/position around them hides the switch.

## 5. Map spoken meaning -> body language
| narrator says | character does |
|---|---|
| anger, challenge, "chalao!" | weapon up, mouth open pulsing, arm pointing at the other character |
| fear, "bhaagi" | crowd panic mode, running away, eyes up |
| doubt, sacrifice ("Arjun ke liye bachakar rakhi thi") | eyes lowered `look=(0, 0.6)` |
| power grows | scale up + aura rings + eye glow |
| hit / death | pose "hit", chest glow burst, flash, then fall - nothing graphic |
| divine calm, blessing | Krishna `pose="bless"`, golden glow pulse, petals |
| gratitude, surrender | namaste / kneel |
Two characters in one scene must LOOK at each other (`look` toward the other side) while one talks.

## 6. Scene joins and the loop
- Each scene's last frame should match the next scene's first (hit pose in vasavi end -> hit pose in gira start).
- Last scene: cross-fade the final 0.45 s into the hook's first frame so the loop is invisible.

## 7. Verify with the REAL audio (not the preview)
1. After render, read `output/shorts/<name>_short.json`: every caption chunk with its absolute time.
2. Compute each beat (scene start + cue + offset) and check it falls on the right word.
3. Grab frames at those times (`ffmpeg ... select='eq(n,<frame>)' ... tile=8x1`) and LOOK: is the spear leaving the
   hand on "chala", is the body on the ground on "gira"? If not, shift the offset and re-render.
4. If the user recorded an older script version, first make the SPEC text match what was actually spoken -
   otherwise every cue lands on the wrong word.
