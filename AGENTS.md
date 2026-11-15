# Divya Rahasya & RealityShift YouTube Agent Rules

## Core Production Philosophy (Mandatory for ALL Channels)

1. **Text Kam (Minimal On-Screen Text)**:
   - Never clutter the screen with heavy text boxes, giant paragraphs, or multi-line speech bubbles.
   - Use ultra-sleek, minimal, high-impact cue ribbons (single short line) placed cleanly at the top (`y = 280–380`).
   - Let the animation, characters, camera composition, and voiceover breathe.

2. **Character Jyada (High Character Density & Variety)**:
   - Always feature multiple distinct, richly detailed, expressive characters across the scenes.
   - For historical/mythological topics: include devotees, priests, architects, kings, deities, witnesses, or colonial figures.
   - For tech/geopolitics (RealityShift): include engineers, diplomats, scientists, commanders, leaders, and civilian observers.
   - Ensure every character has authentic attire, expressive eyes, distinct poses, and lore/context-accurate props.

3. **Real Jaisa Look (Realistic Visual Depth & Atmospheric Fidelity)**:
   - Render realistic perspective, detailed material textures (chiselled granite, architectural carvings, metallic sheen, stone flagstones).
   - Realistic lighting: multi-stop celestial/ambient skies, warm glowing oil lamps (deepams) or tactical lighting, soft floor shadows, light rays passing through gaps, and subtle floating particles (incense smoke, spiritual dust, or atmospheric haze).

---

## YPP Anti-Repetition & Rotation Policy (Every 2 Shorts)

To strictly prevent YouTube Partner Program (YPP) from flagging content as "repetitive", "templated", or "inauthentic mass-produced content":

1. **Background Music Rotation (Every 2 Shorts)**:
   - Never use the same music style or sound bed for more than 2 shorts in a row.
   - Rotate `MUSIC_STYLE` across available synthesized engines:
     - `divine` (sacred bells, devotional tanpura/flute beds)
     - `ambient` (ethereal, spacious atmospheric beds)
     - `tension` (suspenseful, mystery-building beds)
     - `pulse` (driving, technological/action pulse)
     - `march` (majestic, rhythmic, grand historical beats)
   - Change `MUSIC_BPM` by at least **6 to 14 BPM** between consecutive shorts (e.g., 74 -> 82 -> 92 -> 78).

2. **Structural & Scene Count Rotation**:
   - Do NOT produce 3 shorts in a row with the exact same scene count (e.g. 7 scenes, 7 scenes, 7 scenes).
   - Rotate scene structures: 5 scenes (fast punchy), 6 scenes (balanced narrative), 7 scenes (deep lore), 8 scenes (epic journey).
   - Vary the opening hook style (mystery hush vs. shocking action vs. direct historical challenge).
   - Vary the closing CTA / sign-off wording and ending visual device (diya/trishul vs. map/globe vs. character namaste).

---

## Voiceover & Shorts Creation Workflow

1. **User Voiceover Preference**:
   - The user provides their own voiceover audio (recorded or generated via KikiVoice).
   - Do NOT use fallback AI TTS (like edge-tts) for final videos. Only use preview stills (`--preview`) to show scenes and visual flow.
   - The agent's role is to write the scenes, visuals, animations, hooks, and script.

2. **Script Language & Phrasing Rules (TTS Accent & Audience Engagement)**:
   - **Simple & Conversational Hindi (Zero Boring Pure-Sanskrit Jargon)**:
     - Never use heavy, archaic Sanskritized Hindi that sounds like a dry textbook or Doordarshan documentary (avoid e.g. `अथाह गहराइयों`, `महाविनाशक अस्त्र`, `परमाणु भट्टी`, `खोजी तरंगों`, `जासूसी उपग्रह`).
     - Use thrilling, natural, everyday conversational Hindi that keeps Shorts viewers hooked (e.g. `समंदर के गहरे पानी में`, `चुपचाप तैर रहा है`, `सीधा नियम है`, `सारे ठिकाने उड़ा भी दिए`, `परमाणु ताकत`, `पानी को चीरती हुई`, `काली परत`, `दुश्मन की पकड़ में नहीं आने देती`).
   - **Zero English Words in Spoken Hindi (Strict TTS Accent Glitch Prevention)**:
     - KikiVoice and Indic TTS engines abruptly switch accents to an awkward robotic/English tone when encountering English words, units, or transliterations.
     - Never include English loanwords in the spoken Hindi narration: avoid `मीटर` (meter), `नो फर्स्ट यूज़`, `डीज़ल सबमरीन`, `न्यूक्लियर रिएक्टर`, `गैस प्रेशर`, `एनेकोइक टाइल्स`, `सैटेलाइट`, `रडार`, `बेस`, `कमेंट`, `सब्सक्राइब`.
     - Replace them with clean, simple Hindi phrases that flow naturally and effortlessly in KikiVoice.
   - **On-Screen Text Stays Capitalized Roman**:
     - Visual graphics (ribbons, cards, wheels, bottom subtitles) strictly remain capitalized Roman transliteration to avoid Cairo font tofu squares (`□□□`). Only the spoken voiceover text stays clean Hindi.

3. **Step-by-Step Short Pipeline**:
   - **Step 1 - Script & Scenes**: Present the full scene breakdown, dialogue/voiceover text, visual preview sheet, and thumbnail to the user.
   - **Step 2 - Voiceover Preparation**:
     - Provide the clean text for the user to record/generate.
     - Save export text in:
       - Divya Rahasya: `SanatanKatha/output/work/<topic>/files/kiki_narrator.txt`
       - RealityShift: `RealityShift/output/work/<topic>/files/kiki_narrator.txt`
   - **Step 3 - Audio Handling**:
     - Check `output/work/<topic>/files/` for the user's voice file (e.g. `kikivoice-tts-file-*.mp3` or `narrator.mp3`).
     - If it has a KikiVoice default name (`kikivoice-*.mp3`), automatically copy/rename it to `narrator.mp3`.
   - **Step 4 - Whisper Alignment & Splitting**:
     - Accurately align and split `narrator.mp3` into scene clips (`scene_01_l00.wav`, ..., `scene_0N_l00.wav`) and generate their corresponding `.json` word timings.
     - Ensure Whisper uses shared `.cache/whisper` (or `<pipeline>/.cache/whisper`) inside the workspace.
   - **Step 5 - Video Rendering**:
     - Render using the local audio clips (`--engine files`), preserving the user's voiceover, rotated background music bed, dynamic subtitles, and SFX.
   - **Step 6 - Delivery**:
     - Output clickable file links for the `.mp4` video, YouTube thumbnail cover, and complete YouTube upload kit (Title, Description, Tags, Pinned Comment).

---

## Visual & Animation Quality Rules (Never Violate)

1. **Typography & Script (Zero Tofu Squares `□□□`)**:
   - Cairo text rendering with `CAPTION_FONT` (`Impact`) lacks Devanagari glyphs. Any raw Hindi characters in on-screen UI (ribbons, cards, wheels, bubbles) will produce empty squares / tofu boxes (`□□□`).
   - **Rule**: ALWAYS use capitalized Roman transliteration for all on-screen graphics, ribbons, cards, and titles (e.g. `KARM CHAKRA`, `JAI SHRI KRISHNA`, `HAWA MEIN JHULTA KHAMBHA`, `LE PAKSHI!`, `OPERATION MEGHDOOT`). The spoken voiceover stays authentic Hindi.

2. **Character Scaling & Framing (Zero Screen Clipping)**:
   - Standard character scale must stay between **`0.68` and `0.80`** (NEVER `1.0+` or `1.3`–`1.5` in standard full-body scenes).
   - Feet must always sit at `GROUND - 10` (`y ≈ 1170`).
   - At this scale, the top of the head/crown stays at `y ≈ 500–550`, leaving clean breathing room under the top header (`y = 78–146`) and avoiding collisions with bottom captions (`CAP_Y = 1290`).
   - In 2-character scenes, position characters at `x ≈ 230–250` and `x ≈ 750–850` (~500px apart) so neither clips against screen borders.

3. **Character Authenticity & Avatar Distinction (Zero Clones)**:
   - When depicting different avatars or deities across Yugas (e.g. Shri Rama vs. Shri Krishna):
     - **Shri Rama (Treta Yuga)**: Royal warrior mukut (NO peacock feather!), Raghuvanshi tilak, Kodanda bow on shoulder, deep saffron robes.
     - **Shri Krishna (Dwapara Yuga)**: Mor-pankh (peacock feather), flute or Abhaya blessing mudra, Pitambar yellow dhoti.
     - Never duplicate identical Krishna sprites for Rama and Krishna.
   - Non-royal figures (like hunter Jara, rishis, commoners, engineers) must NOT wear golden king crowns (`mukut`). Use authentic context-driven attire matching their lore/profession.

4. **UI Placement & Layout (Never Obscure Key Subjects)**:
   - Never place a large comment box or bubble over the central deity or character's body (`y = 800–1000`).
   - In CTA scenes, keep the central figure/monument visible and unobstructed. Place clean prompt ribbons at the top (`y = 280–380`) and use an animated pointer arrow directing to the YouTube Shorts comment button.
