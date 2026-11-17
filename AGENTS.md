# Divya Rahasya & YouTube Agent Rules

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
    - **Speech Flow**: Keep inter-chunk pauses at `0.02 - 0.04s` and set `TAIL_PAD = 0.04`, `MAX_GAP = 0.04`. Never insert $\ge 0.3$s pauses that cause awkward stutters.
    - **No Repetitive Horns**: NEVER use the loud conch horn ("shankh" / "pooooooo") repeatedly across shorts.
    - **Music Variety**: Use cinematic devotional ambient pads (`MUSIC_STYLE = "ambient"`, 80–92 BPM, `MUSIC_VOLUME = 0.10–0.12`) so every short sounds fresh, modern, and distinct.

11. **Target Duration & Script Calibration (30 to 35 Seconds Rule)**:
    - **MANDATORY DURATION**: All YouTube Shorts (for both RealityShift and Divya Rahasya) must be strictly **30 to 35 seconds** long.
    - **Script Word Count**: 80 to 105 spoken Hindi words.
    - **Character Limit for KikiVoice**: Strictly **500 to 650 characters** in `kiki_narrator.txt` (including `((⏱=400))` pause tags). NEVER write 900+ or 1,000 character scripts unless explicitly requested.
    - **High-Retention Pacing Arc**:
      - `00:00 - 00:03`: Instant curiosity / shock hook.
      - `00:03 - 00:12`: High-stakes premise / conflict.
      - `00:12 - 00:24`: Core action / secret weapon / pivotal twist.
      - `00:24 - 00:30`: Climactic impact / victory.
      - `00:30 - 00:35`: Punchy CTA + subscribe prompt.
    - **Shorts Algorithm Advantage**: 30–35s length delivers maximal Average Percentage Viewed (APV > 100%), triggering YouTube's viral recommendation engine.

12. **Mid-Video Pacing & Re-Hook (The 15–18s Anti-Drop Rule)**:
    - **Never Plateau at Reveal**: When the secret weapon, deity name, or turning point is revealed around 15–18s, NEVER transition into slow theoretical explanations or backstory lectures (which caused the 17s drop in KALI 5000).
    - **Deliver Immediate Impact**: Immediately follow the reveal with high-impact visual action, firing, screen shake, explosion, or shock fact to hold viewers through the second half.
    - **Limit Explanation**: Keep technical/lore breakdown strictly under 1–2 punchy, vivid sentences.

13. **Outro & CTA Velocity (The 3-Second Snap & Loop Rule)**:
    - **No 6-7 Second Drag**: Outros/CTAs must NEVER drag for 6–7 seconds at the end. Viewers swipe the second they realize the story is over.
    - **Tight 3-Second Snap**: Keep the engagement prompt and subscribe ask strictly within **3 to 4 seconds** (e.g. `Comment mein 'JAI HIND' likhein aur subscribe karein Reality Shift!`).
    - **Seamless Loop**: Keep the background visuals active so the end snaps directly back to the opening hook for automatic replay bonus.



