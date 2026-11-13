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


