# Sanatan Katha

YouTube Shorts pipeline for the **Divya Rahasya** channel (the old 4,110-sub Apni Kahaniya / Silent Reality channel, renamed). It makes animated mythology stories with code-drawn
cartoon devta characters, a kathavachak-style voice-over and a synthesized devotional music bed.

It is separate from `RealityShift/` on purpose: it has its own engine copy, its own YPP gate, its own outputs
and its own `policy_history.json`. Changing one pipeline can never break the other.

## Commands (run from this folder)

```
python make.py --list               # every katha and whether it is rendered
python make.py barbarik --preview   # contact sheet of all scenes + thumbnail (fast, no voice)
python make.py barbarik --check     # YPP policy gate only
python make.py barbarik             # full render -> output/shorts/barbarik_short.mp4 + upload kit
```

Every full render writes these files to `output/shorts/`:

- `<name>_short.mp4`: the Short
- `<name>_short.json`: scene log with word timings
- `<name>_short_thumb.png`: thumbnail, plus a `_feed.png` preview of it
- `<name>_short_upload.md`: title, description and tags, with scores

## Folder

| File | What it is |
|---|---|
| `make.py` | One command per katha: render, `--check`, `--preview`, `--list` |
| `katha.py` | Shared by every katha: storyteller voice tones (`TONES`), `script_of()`, `Cued` scenes, scenery (battlefield, meadow, temple, mother), the diya header, scroll captions, the compositor, `run()` |
| `devta.py` | Character rig: Krishna, the brahmin disguise, Barbarik, the Khatu Shyam sheesh roop, plus props (peepal, divine arrow, bow, balance, diya, Kailash, trishul, army, petals, ribbon) |
| `kathas/<name>.py` | One story: SPEC, scene classes, UPLOAD and `thumbnail()` |
| `kathas/_template.py` | Copy this to start a new katha |
| `engine.py` | TTS (edge-tts, a voice per line), the "divine" music bed, SFX (ghanti, shankh, arrow, shimmer), mixing and encoding |
| `delivery.py` | Turns SPEC lines into the performed voice: tones and held pauses |
| `policy.py` | YPP gate: original script and topic, no outside media, sources, upload kit |
| `upload_kit.py` | Title scoring, description and tag checks, thumbnail |

## Making a new katha

1. Copy `kathas/_template.py` to `kathas/<name>.py`.
2. Write the script following the storytelling rules below.
3. If the story needs a new character (Shiv ji, Hanuman ji, Ashwatthama...), add it to `devta.py`. Use the same
   style as the existing characters: an ink outline, flat colours, big eyes, and `place()` / `group()` for
   position and fade.
4. Run `python make.py <name> --preview` and check every scene.
5. Run `python make.py <name>` and listen to the result.

## Storytelling rules (kathavachak)

- **Tell the story, don't read it.** Open with a hush ("Socho..."). Hold a pause before a name or a reveal.
  Speed up in action ("baan ghooma, ghooma..."). Add a narrator aside ("jaise keh raha ho—"). Whisper before
  the twist. Leave a silence before the emotional peak. Close by talking to the viewer like family.
- **Every line carries its own pause** as its 3rd element, so silences are written into the script.
- **Characters speak in their own voice.** `deva` is Krishna (deep and unhurried), `char` is a teasing old man,
  and `maa` is the mother in the female voice (hi-IN-SwaraNeural).
- **Use easy words with 2-4 light Haryanvi touches** (bhai, ghana, ib, ke kar lega).
- **Aim for 75-90 seconds.** Barbarik came out at 99s.
- **Facts:** stories that come from folk tradition get "kehte hain" in the script and a note in the
  description. List the versions that differ in `SOURCES`.
- **Respect:** keep the deities' correct colours and weapons, never make them comic, and show nothing graphic.
  For example, the sheesh daan is shown as light and petals.
- **No reused content:** every frame is drawn in code and every sound is synthesized. Nothing is downloaded.
