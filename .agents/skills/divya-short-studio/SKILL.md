---
name: divya-short-studio
description: >-
  End-to-end playbook for making one Divya Rahasya (Sanatan Katha) YouTube Short the way the user likes it:
  pick the angle, write a full-story Hindi script, build the katha module, LOOK at the preview and fix it, hand the
  KikiVoice script, then rename/split/render the user's voice and deliver the upload kit. Use whenever the user says
  "short banao", "naya short", "<topic> wala short", "voice paste kar di", "is voice pe short bana do", or similar.
  It orchestrates the katha-writer, cinematic-director and animation-implementation skills - read this one first.
---

# Divya Rahasya Short Studio (master playbook)

You are the lead director. The user only listens, records the voice in KikiVoice, and uploads. **You** decide the
angle, write, animate, check, render and deliver. Never send the user a multiple-choice menu ("kaunsa topic?").
Pick the strongest option, do it, and say what you chose in one line.

Gold reference (copy its structure, not its story): `story-pipeline/SanatanKatha/kathas/ghatotkach_akshauhini.py`
(user-approved, 19 Nov 2026). Rules that must never break are in the root `AGENTS.md` - read it every time.
**Only learn from the gold file.** Older kathas (karna.py, ashwatthama.py, old ghatotkach.py ...) break rules
(on-screen text, scale > 0.80, static characters, wrong lore like "Kaumodaki" for Ghatotkach's gada) - do not copy them.

Must-read references in this skill:
- `references/viral_formula.md` - READ FIRST, before choosing a topic: what makes a Divya Rahasya Short
  break the ~1,200-view ceiling, the channel's real numbers and goal, cadence, 48 h report card, weekly review.

Also read both of these before Phase 2:
- `references/character_design.md` - how to draw beautiful, recognisable, alive characters (style, draw order,
  faces, poses, rig template).
- `references/voice_sync.md` - how every character action lands exactly on the spoken word (beat table, cue(),
  easing formulas, verification on the real audio).

---

## Phase 0 - Read before you write (5 min, saves hours)

1. Root `AGENTS.md` (visual + audio rules). If `story-pipeline/AGENTS.md` disagrees, the newer file wins; say which
   one you followed in one line.
2. `kathas/` - is this topic already done? If yes, the new Short MUST take a **different angle** (example: old
   Ghatotkach = "Krishna kyun naache"; new = "marte marte bhi akshauhini kuchal di"). `TOPIC` must be unique.
3. `core/devta.py` function list (`grep -n "^def " core/devta.py`) - reuse characters (krishna, karna, devi, raja...)
   and props (army, petals, bow, divine_arrow). Custom characters from other kathas can be imported
   (`from kathas.ghatotkach import arjuna`).

## Phase 1 - Script: a COMPLETE story, not half - in <= 25 seconds

The user rejected a 22-second version with "ye to adhi script hai". A Short must answer every "why" the viewer has.
Checklist before you show the script:

- [ ] **Hook (0-3s)**: the most shocking result first, zero backstory. ("मरते मरते भी, घटोत्कच ने, कौरवों की पूरी एक अक्षौहिणी कुचल दी!")
- [ ] **Who / why it matters** in ONE punchy line (or skip it if the hook already says it).
  With only 55-68 words, merge beats: every line must be action or stakes. No slow backstory, no
  'maa ke garbh mein suna tha' style exposition - the user called that script 'bekar'.
- [ ] **Action** (fast, no pauses): growth, fire, army fleeing.
- [ ] **Conflict voice**: a character screams/commands (Duryodhan: "कर्ण, वो शक्ति चलाओ!").
- [ ] **The stakes of the turning point** (the Shakti works only once, it was saved for Arjun).
- [ ] **Climax** shown physically (falls ON the army).
- [ ] **Twist / meaning** (Krishna smiles - Arjun is saved).
- [ ] **Loop ending**: last words grammatically run into the first line ("...और" -> "मरते मरते भी...").

Format rules:
- 🔒 **HARD LOCK: never longer than 25 s.** 5-6 scenes, **20-24 s**, **55-68 spoken words**, **320-450 characters**
  in the KikiVoice text (pause tags included). `core/policy.py` blocks > 68 words; `core/katha.py` fails a render
  > 25 s. Count words BEFORE showing the script. (The old 30-35 s / 7-scene rule is cancelled.)
- Pure spoken Hindi, 4-8 word phrases, commas for breath, "..." for a held beat, "!" for shouts.
- **Never a "?" in the middle of a line** (KikiVoice drops the next word). Numbers/acronyms spelled in Hindi words.
- Folk/variant facts: note them in `SOURCES` and in the description ("kuch sanskaranon mein...").

SPEC shape (one `vo` line per scene, short caption chunks so subtitles change fast):
```python
{"key": "vasavi", "text": "VASAVI SHAKTI", "visual": "...",
 "vo": [("low", [("वो इंद्र की शक्ति,", "WO INDRA KI SHAKTI,"),
                 ("जो बस एक बार चलती थी,", "JO BAS EK BAAR CHALTI THI,"), ...], 0.04)]}
```
Captions = capitalised Roman (Impact font has no Devanagari - Hindi on screen = tofu boxes).

## Phase 2 - Build the module

Module header: `MUSIC_STYLE` (pick by mood: war = "march", mystery = "tension", devotion = "ambient"),
`MUSIC_BPM` >= 6 away from the last katha, `MUSIC_VOLUME = 0.12`, `TAIL_PAD = 0.04`, `MAX_GAP = 0.04`.

Every scene is a `Cued` class:
- `beats(d)`: times from the spoken words, e.g. `self.cue("CHALA DI", d * 0.82) + 0.3`. Every big visual
  (grow, throw, impact, smile) MUST hang on the word that says it.
- `events(d)`: SFX on those beats (boom, thud, soft_thud, whoosh, arrow, shimmer, ghanti). No repeated shankh.
- `draw(ctx, t, d)`: background -> crowd -> characters -> effects. Screen shake = `ctx.save(); ctx.translate(...)`
  ... `ctx.restore()` inside draw; draw backgrounds from x = -80 to W + 80 so the shake never shows an edge.

What makes it "takadta-bhadakta" (copy these patterns from the gold file):
- **Scale contrast**: tiny crowd (`kaurava_mob`, soldiers ~90 px) vs hero at scale 0.70-0.80.
- **Growth on the word**: `s = lerp(0.62, 0.80, ease_out_back(...))`.
- **Projectiles with true angle**: `ang = math.atan2(ty - sy, tx - sx)`; head always points at the target;
  thrower switches to a follow-through pose after release (`pose="throw"`), never a weapon in hand AND in the air.
- **Falls**: rotate about the feet (`rot`), ease-in like gravity, then dust + flash + shake decaying with `exp(-u*4)`.
- **Hit feedback**: glow burst on the chest, pose change to "hit", flash 0.35-0.4 s.
- **Rich background**: 4+ stop sky, moon/sun disc, 3 hill layers, camp fires, wreckage, embers.
- **Loop**: the last scene cross-fades (last 0.45 s) into the hook's first frame
  (`ctx.push_group(); Hook().draw(ctx, 0.0, d); ctx.pop_group_to_source(); ctx.paint_with_alpha(x)`).
- Nothing graphic: a crushed army = dust clouds + flying helmets/shields, never blood.
- Only subtitles on screen. No ribbons, title cards or labels in video frames (thumbnail is the only place for text).

New character rig: own function with `ctx.save()/translate/rotate/scale ... ctx.restore()` (or `dv.place` +
`ctx.restore()`) wrapped in `dv.group(ctx, a, draw)`. Poses as a `pose=` argument. If you add a pose to a shared rig in
`core/devta.py`, ADD a new branch - never change existing poses (older kathas use them).

## Phase 3 - LOOK at your work and fix it (the step most agents skip)

```
cd story-pipeline/SanatanKatha
python make.py <name> --preview      # output/preview/<name>_sheet.png + <name>_thumb.png
python make.py <name> --check        # YPP policy gate must print OK
```
**Open the sheet image and actually inspect every tile** (2 moments per scene). Ask:
- Is the hero hidden by dust/effects? (Hook dust once covered Ghatotkach -> drew dust BEHIND the body.)
- Does every weapon point at its target? (Thumbnail spear once pointed up-left -> fixed to `math.pi - 0.3`.)
- Does anything overlap a character's body / feet? (Background fallen giant sat at Krishna's feet -> moved back
  and scaled 0.30.)
- Any clipping at screen edges, any crown above y ~ 480, anything over the subtitle zone?
- Would a viewer understand the scene with the sound OFF?
Fix, re-run preview, look again. Only then show the user: scene table + preview sheet + thumbnail + Kiki script.

## Phase 4 - KikiVoice script

`python make.py <name> --kiki-export` writes `output/work/<name>/files/kiki_narrator.txt`. Also write
`kiki_script.txt` = all scenes in one paragraph joined by `((⏱=150))` - the user pastes that single block.
Count characters (tags included) and words; no Latin letters; no "?".

Suspense pass (when the user asks for "suspense / emotion in the voice"): KikiVoice has NO emotion tags - only
`((⏱=ms))` pauses. Make suspense with:
- held pauses 250-400 ms only right before a reveal ("...बचाकर रखी थी... ((⏱=400)) कर्ण ने..."),
- "..." for slow drawn-out phrases, "!" for shouts, NO pauses inside action lines,
- the reveal word alone as its own caption chunk (`("गिरा!", "GIRA!")`) and the visual impact cued to it.
Keep pause tags OUT of the SPEC text (they would break Whisper matching) - add them only in `kiki_script.txt`.

## Phase 5 - The user's voice -> video

1. Find the file in `output/work/<name>/files/` (or `~/Downloads`, newest `kikivoice-*.mp3`). Copy it to `narrator.mp3`.
2. **Check WHICH script that voice was made from** (file time vs. when you changed the script). If the user recorded
   an older version, put the SPEC text back to exactly what was spoken before splitting. Captions and cues must
   match the actual audio, not your latest idea.
3. `python make.py <name> --kiki-split --check-voice` - every scene clip must contain its full line in the Whisper
   check, no clip < 1 s.
4. `python make.py <name> --engine files`. On Windows moviepy can crash at the very end with
   `PermissionError ... TEMP_MPY_wvf_snd.mp4` - the mp4 is usually fine, but the alignment JSON, thumbnail and upload
   kit were not written. Re-run with a tolerant `os.remove`:
   ```
   python -c "import os,sys;sys.path.insert(0,'.');_r=os.remove
   def f(p,*a,**k):
       try:_r(p,*a,**k)
       except PermissionError:pass
   os.remove=f
   from core import katha;katha.run('<name>','files')"
   ```
   Then delete the leftover `*TEMP_MPY*` file.
5. Verify: `ffprobe` duration <= 25 s (20-24 ideal), then grab a frame strip
   (`ffmpeg -i x.mp4 -vf "select='eq(n,30)+eq(n,330)+...',scale=270:480,tile=8x1" -frames:v 1 strip.png`) and LOOK
   at it - grow/throw/impact must land on their words.

## Phase 6 - Delivery message (Hinglish, short)

Clickable links to the mp4, thumbnail and upload md, then paste-ready: Title (best scorer), Description (remove the
duplicate hashtag line the kit appends), Tags, a **debate-style pinned comment** ("Kya Karna ki sabse badi galti thi,
ya Duryodhan ki?"), schedule slot (Divya Rahasya 12:00 PM / 05:30 PM IST), AI disclosure = NO for 2D cartoons.
Report honestly what you checked and anything that failed.

## Hard checks before you say "done" (learned from the Abhimanyu test, 19 Nov)
- **SFX names must exist.** Allowed ONLY: `boom thud soft_thud whoosh arrow shimmer ghanti zap pop tick tock beep
  pick alarm dingdong kaching` (`shankh` exists but avoid). `hit`, `clang`, `shout`, `bell`, `tension`, `brass` do
  NOT exist - preview will not catch it, the final render crashes with KeyError. Verify:
  `grep -oE 'bank\["[a-z_]+"\]' core/engine.py`.
- **No disguised clones.** `dv.karna(..., kavach=0)` is NOT Arjun. If a character has no rig, BUILD one (or import
  an existing one, e.g. `from kathas.ghatotkach import arjuna`). Never say "no clones" without grepping your calls.
- **Lore research before the script.** List the 3-5 canonical beats of the story and make sure the script contains
  them (Chakravyuh: learned entry in the womb but not exit; Jayadratha held the Pandavas at the gate; Drona told
  Karna to cut the bow from behind; Arjun vowed to kill Jayadratha before next sunset). Weapon/name check:
  Kodanda = Shri Ram's bow, Kaumodaki = Vishnu/Krishna's gada, Gandiva = Arjun's bow.
- **Every spoken action visible.** For each verb in the VO ("tod diye", "ghus gaya", "gher liya", "kaato") the
  sheet must show it happening - a standing character is a fail.
- **Never claim a fix or check you did not prove.** Back each claim with the file/line or the image.
- **Fresh preview only.** Re-run `--preview` AFTER your last code edit; the sheet's file time must be newer than the
  module's (`ls -la --time-style=+%H:%M kathas/<name>.py output/preview/<name>_sheet.png`). Describing an old sheet
  is a false report.
- **Count, don't guess.** Caption chunk sizes: run a loop over SPEC and print every chunk with > 5 words; long chunks
  shrink the subtitle. Same for characters/words of the Kiki text.
- **The hero must act, not pose.** If the main character has the same pose in 5+ tiles, the short is static - give
  him a pose per verb (run, shoot, look back, kneel, lift, fall) and move his x across the screen when he "enters".

- **A pose is real only if the rig has its branch AND it looks different.** `grep -n 'pose == "<name>"'` in the rig;
  an unknown pose silently falls back to the default. Then render a pose-test strip (every pose side by side at
  sheet size) - if "run" looks like "stand", exaggerate it (lean the torso, split the legs, swing the arms).
- **The 2-tile sheet hides most of the scene.** Run `scripts/probe_moments.py <name> out.png` (5 moments x every scene) and render in-between moments (e.g. t = 1.0 / 2.5 / 4.0 / 5.5 of
  each scene with the same fake timing as make.py preview) before claiming a run, kneel or throw happens.
- **Don't reuse a deity rig for a human.** `dv.devi` is Chhathi Maiya (halo, crown, blessing hand) - Subhadra,
  Draupadi, Kunti etc. need their own rig. Same for any other deity sprite.
- **Arrow direction = shooter -> target.** If Abhimanyu (left) shoots, `ang = atan2(ty - sy, tx - sx)` with sx at
  HIS bow; arrows flying from the enemy side towards him are a rule-7 violation.

- **The hook frame must SHOW the hook line's emotion.** "Dar gaye the" = enemies visibly afraid (eyes up/wide,
  mouth open, stepping back, shields up) around a glowing hero. If the 0-3 s tile could be muted and still shock,
  it passes. The hook gets the best composition of the whole short.
- **Never repeat a composition.** If two scenes look like the same line-up of the same characters, change one:
  camera distance, who is in front, a crowd, a close-up, a different background. 5-6 scenes = 5-6 different pictures.
- **Every noun in the VO that can be drawn must be drawn.** "Kaurav sena bikhar gayi" needs an army that scatters
  (import `kaurava_mob` / `soldier` from `kathas/ghatotkach_akshauhini.py`).
- **Timestamps are pasted, not typed.** Run `ls -la --time-style=+%H:%M:%S <module> <sheet> <probe>` as the LAST
  command before writing the report and paste its raw output. Writing "zero edits after X" from memory was wrong
  five times in a row on the Abhimanyu test.

- **Voice-version gate = STOP, not a footnote.** Before `--kiki-split`, compare the voice file's time with the time
  the current SPEC was written (and/or Whisper the whole narrator.mp3 against the NARRATION). If they differ: STOP,
  tell the user "this voice is from the old script - please record the new kiki_script.txt", and do nothing else.
  On the Abhimanyu test a 14:47 voice (old 108-word script) was split and rendered against the new 68-word SPEC:
  every clip held the wrong words, the 34.6 s render tripped the LENGTH LOCK, and "beat timings" were reported
  as if valid. Never report beats, frames or an upload kit for a mismatched or failed render, and rename such an
  mp4 `*_WRONG_VOICE_DO_NOT_UPLOAD.mp4` so it can't be uploaded by mistake.

## Things the user dislikes (learned)
- Half stories / missing "why" -> always the full arc above.
- Multiple-choice menus -> decide yourself.
- Edge-TTS in finals -> only the user's KikiVoice.
- Text clutter on screen, Hindi text in Cairo, mirrored text (missing `ctx.restore()`), clones of Krishna for other
  characters, crowns on commoners.
- Long gaps in speech (>0.3 s outside deliberate suspense beats).
