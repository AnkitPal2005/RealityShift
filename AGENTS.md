# Divya Rahasya & YouTube Agent Rules

> **NOTE (23 Nov 2026):** the root `AGENTS.md` -> "Latest Decisions" section wins wherever this file disagrees
> (length 30-45 s, no commas or pause tags in Kiki text, Multilingual voice processing, gaps).


## Voiceover & Shorts Creation Workflow

1. **User Voiceover Preference**:
   - The user provides their own voiceover audio (recorded or generated via KikiVoice).
   - Do NOT use fallback AI TTS (like edge-tts) for final videos. Only use preview stills (`--preview`) to show scenes and visual flow.
   - The agent's role is to write the scenes, visuals, animations, hooks, and script.

2. **Step-by-Step Short Pipeline**:
   - **Step 1 - Script & Scenes**: Present the full scene breakdown, dialogue/voiceover text, visual preview sheet, and thumbnail to the user.
   - **Step 2 - Voiceover Preparation**: Provide the clean text for the user to record/generate and tell them where to save it: `story-pipeline/SanatanKatha/output/work/<topic>/files/`.
   - **Step 3 - Audio Handling**:
     - Check `output/work/<topic>/files/` for the user's voice file (e.g. `kikivoice-tts-file-*.mp3` or `narrator.mp3`).
     - If it has a KikiVoice default name (`kikivoice-*.mp3`), automatically copy/rename it to `narrator.mp3`.
   - **Step 4 - Whisper Alignment & Splitting**:
     - Accurately align and split `narrator.mp3` into scene clips (`scene_01_l00.wav`, ..., `scene_08_l00.wav`) and generate their corresponding `.json` word timings.
   - **Step 5 - Video Rendering**:
     - Render using the local audio clips (`--engine files`), preserving the user's voiceover, background devotional music bed, dynamic subtitles, and SFX.
   - **Step 6 - Delivery**:
     - Output clickable file links for the `.mp4` video, YouTube thumbnail cover, and complete YouTube upload kit (Title, Description, Tags, Pinned Comment).

## Visual & Animation Quality Rules (Never Violate)

1. **Typography & Script (Zero Tofu Squares `□□□`)**:
   - Cairo text rendering with `CAPTION_FONT` (`Impact`) lacks Devanagari glyphs. Any raw Hindi characters in on-screen UI (ribbons, cards, wheels, bubbles) will produce empty squares / tofu boxes (`□□□`).
   - **Rule**: ALWAYS use capitalized Roman transliteration for all on-screen graphics, ribbons, cards, and titles (e.g. `KARM CHAKRA`, `JAI SHRI KRISHNA`, `KSHAMA PRABHU!`, `SHEESH KYUN?`). The spoken voiceover stays authentic Hindi.

2. **Character Scaling & Framing (Zero Screen Clipping)**:
   - Standard character scale in SanatanKatha must stay between **`0.68` and `0.80`** (NEVER `1.0+` or `1.3`–`1.5`).
   - Feet must always sit at `GROUND - 10` (`y ≈ 1170`).
   - At this scale, the top of the crown/mor-pankh stays at `y ≈ 500–550`, leaving clean breathing room under the top header (`y = 78–146`) and avoiding collisions with bottom captions (`CAP_Y = 1290`).
   - In 2-character scenes, position characters at `x ≈ 230–250` and `x ≈ 750–850` (~500px apart) so neither clips against screen borders.

3. **Character Authenticity & Avatar Distinction (Zero Clones)**:
   - When depicting different avatars or deities across Yugas (e.g. Shri Rama vs. Shri Krishna):
     - **Shri Rama (Treta Yuga)**: Royal warrior mukut (NO peacock feather!), Raghuvanshi tilak, Kodanda bow on shoulder, deep saffron robes.
     - **Shri Krishna (Dwapara Yuga)**: Mor-pankh (peacock feather), flute or Abhaya blessing mudra, Pitambar yellow dhoti.
     - Never duplicate identical Krishna sprites for Rama and Krishna.
   - Non-royal figures (like hunter Jara, rishis, commoners) must NOT wear golden king crowns (`mukut`). Use rustic attire, headband/topknot, quivers, or traditional garments matching their lore.

4. **UI Placement & Layout (Never Obscure Deities)**:
   - Never place a large comment box or bubble over the central deity or character's body (`y = 800–1000`).
   - In CTA scenes, keep the deity's full divine form visible and unobstructed. Place clean prompt ribbons at the top (`y = 280–380`) and use an animated pointer arrow directing to the YouTube Shorts comment button.
   - Never use oversized multi-line speech bubbles that stretch across the screen width. Use compact ribbons instead.

5. **Rich Atmospheric Backgrounds (No Flat Voids)**:
   - Backgrounds must have depth: multi-stop sunset/twilight sky gradients, glowing celestial sun/moon disc, layered rolling hills/forest silhouettes, sacred Peepal tree, ground vegetation, and floating spiritual dust/petals.

6. **Cairo Context State Isolation (Zero Transform Leaks & No Mirrored Text)**:
   - `place(ctx, x, y, s, t, flip)` issues an internal `ctx.save()`. Every custom character or prop drawing routine (`shri_ram`, `hanuman`, etc.) MUST call `ctx.restore()` before exiting (`group(ctx, a, draw)`).
   - If `ctx.restore()` is omitted, the flipped coordinate matrix (`scale(-s, s)`) leaks into the global Cairo context. This causes subsequent characters to be thrown completely off-screen and all subsequent text/subtitles to be rendered reversed / mirrored ("ulta").

7. **Weapons & Prop Directionality (Correct Arrow & Bow Orientation)**:
   - **Arrowhead Direction**: The arrowhead MUST always point forward towards the target/adversary (never inverted or pointing backwards into the deity/archer's own body).
   - **Fletching & String**: The feathers/nock must sit back at the bowstring. When drawn on a flipped character, account for local vs. world coordinates (`ang = math.pi` inside flipped space to point forward).
   - **Shoot & Release**: When an arrow is released, transition the archer to `pose="shot"` (bowstring relaxed/straight, arm follow-through) so a static arrow is never stuck on the bow while another flies through the air. Flying arrows must track their true flight angle (`math.atan2(dy, dx)`).

8. **Zero On-Screen Text Clutter (Only Subtitles Rule)**:
   - **CRITICAL**: Screen par **SIRF aur SIRF dynamic subtitles** rahenge. 
   - NEVER draw extra floating ribbons, large title cards, info bubbles, or telemetry blocks that clutter the screen.
   - The entire visual canvas belongs to the animated characters, background depth, and divine/cinematic action.
   - Subtitles stay locked to the bottom safe zone (`y ≈ 1220–1290`).

9. **Character-Driven High-Retention Animation & Multi-Character Dynamics**:
   - Every short must be character-rich to hook audience attention:
     - Multi-character scenes (e.g. Bhishma vs Arjuna, Krishna blessing devotee, Rishi confronting king, Commander vs operator).
     - Characters must visibly perform their unique actions: dialogues, eye contact, expressions, weapon draws, folded hands, bowing, or panicking.
   - **Exact Voiceover-Matched Motion**: Characters MUST physically execute what the voiceover narrates in real time:
     - Surrender/Sharan -> Prostrating / kneeling at the feet (`pose="sharan"`).
     - Dhyan / Tapasya -> Seated in Padmasana (lotus pose) on the ground.
     - Anger / Challenge -> Weapon raised, stance widened, forward lunge.
     - Fear / Confusion -> Trembling, wiping sweat, looking around, stepping back.
     - Miracles / Blessings -> Golden aura pulse, blooming lotus, Abhaya mudra blessing.
     - Every action must transition smoothly with time `t` synchronized to the word cues.

10. **Audio Flow & Music Quality (Zero Gaps & Fresh Music)**:
    - **Speech Flow (user, 22 Nov 2026)**: KikiVoice text = one paragraph; commas for breaths, story told in time order with FULL sentences only (no fragments like "कारगिल, उन्नीस सौ निन्यानवे,"), every comma phrase 4–7 words so the speed stays even, written as a steady "lay": short 4–5 word lines of near-equal length with the SAME short tag `((⏱=230))` after EVERY line (KikiVoice rushes long untagged stretches) — never `...`, never English words like "twist". Render keeps those beats: `MAX_GAP ≈ 0.28`, `TAIL_PAD ≈ 0.23` (0.04 made it sound like a paragraph read too fast).
    - **No Repetitive Horns**: NEVER use the loud conch horn ("shankh" / "pooooooo") repeatedly across shorts.
    - **Music Variety**: Use cinematic devotional ambient pads (`MUSIC_STYLE = "ambient"`, 80–92 BPM, `MUSIC_VOLUME = 0.10–0.12`) so every short sounds fresh, modern, and distinct.

11. **Target Duration & Script Calibration (22–30 s, YouTube Studio plan - BOTH Channels)**:
    - **🔒 LENGTH LOCK (user, 22 Nov 2026 — follows YouTube Ask Studio audit)**: Shorts run **22–30 seconds**, never over 30 s. The story MUST be complete — beginning, conflict, climax and resolution all told; never cut a story short just to save seconds. Target 60-80 spoken Hindi words, 350-520 KikiVoice characters (pause tags included), 5-7 scenes. Enforced in code (SanatanKatha): `core/policy.py` blocks scripts over 80 words, `core/katha.py` fails any render over 30 s.
    - **RealityShift aims for 22–25 s** inside this lock (YouTube Studio, 22 Nov 2026: its ~36 s Shorts fell from 35 % to 8 % in the last 8 s, and 4–10 s is the big drop — no character intro, action from frame 1, a pure-Hindi escalation line around 12 s, e.g. "तो सब हैरान रह गए!" — never the English word "twist", KikiVoice can't say it).
    - 60–80 s Shorts killed retention (30–42 % viewed) — never go back to long Shorts. Best performer so far: Ghatotkach, 20 s, 79.8 % viewed.
    - **High-Retention Pacing Arc (<= 30 s)**:
      - `00:00 - 00:02`: Paradox hook as the first spoken line (zero backstory, no static character intro).
      - `00:02 - 00:12`: Conflict + the one line of "why" (no exposition cliff). Visual cut / SFX change around 5–7 s.
      - `00:12 - 00:22`: Climax / turning point shown physically.
      - `00:22 - 00:29`: Resolution so the story feels complete, then a grammatical loop back into the hook (no slow CTA; the comment/subscribe ask goes in the pinned comment).

12. **Mid-Video Pacing & Re-Hook (The 15–18s Anti-Drop Rule - BOTH Channels)**:
    - **Never Plateau at Reveal**: When the secret weapon, turning point, or deity leela is revealed around 15–18s, NEVER transition into slow theoretical explanations, philosophical lectures, or textbook backstory (which caused the 17s drop in KALI 5000).
    - **Deliver Immediate Impact**:
      - **Divya Rahasya**: Follow the reveal immediately with divine miracle shock, golden aura pulse, Sudarshan Chakra spin, lightning thunder, or bowstring release.
      - **RealityShift**: Follow the reveal immediately with firing, supersonic dash, screen shake, radar alert, or explosion shock.
    - **Limit Explanation**: Keep technical or lore breakdown strictly under 1–2 punchy, vivid sentences.

13. **Outro & CTA Velocity (The 3-Second Snap & Loop Rule - BOTH Channels)**:
    - **No 6-7 Second Drag**: Outros/CTAs must NEVER drag for 6–7 seconds at the end. Viewers swipe the exact second they realize the core story is over.
    - **Tight Snap (only if it fits inside 30 s)**: Prefer the loop ending; if a CTA is used keep it under **2 seconds**:
      - **Divya Rahasya**: `Comment mein 'JAI SHRI KRISHNA' / 'HAR HAR MAHADEV' likhein aur subscribe karein Divya Rahasya!`
      - **RealityShift**: `Comment mein 'JAI HIND' likhein aur subscribe karein Reality Shift!`
    - **Seamless Loop**: Keep background visuals and dynamic animation running during CTA so the video snaps seamlessly back into the opening hook for automatic replay bonus.



