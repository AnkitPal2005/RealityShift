# Divya Rahasya & YouTube Agent Rules

> **Making a Divya Rahasya Short?** Read and follow `.agents/skills/divya-short-studio/SKILL.md` first (full
> step-by-step playbook). Gold example: `story-pipeline/SanatanKatha/kathas/ghatotkach_akshauhini.py`.

## 🆕 Latest Decisions (user, 23 Nov 2026) - these OVERRIDE older numbers below

1. **Length**: Shorts 30-45 s (never over 45 s), ~100 spoken Hindi words. Story must finish, calm pace, no rushing.
2. **Payoff in the LAST 2 seconds**: no reaction/blessing/kneeling scene after the reveal (Sapt Saal: reveal at 0:16 + 5 s
   reaction = APV stuck at 64%). Final words loop into the hook.
3. **Debate topics**: every topic needs ONE question with two defensible sides, put in the title/hook and in the pinned
   comment (posted within 30 min). Pick little-known stories. Debate stays inside the story/tech: NEVER religion vs
   religion, caste, party politics, or hate against a nation/real person.
4. **Voice = KikiVoice Multilingual** (user approved). It pauses ~1 s after each line:
   - Shorts: `narrator.mp3` = `ffmpeg -i kikivoice-*.mp3 -af atempo=1.05 narrator.mp3` (max 1.10, never slow down);
     module `TAIL_PAD = 0.22`, `MAX_GAP = 0.25`. Never write ".mp3"/"voice" in module comments (policy gate blocks).
   - Long-form: squeeze every pause to 0.45 s (keep head+tail of the pause, drop the middle), keep raw files in
     `files/raw_kiki/`, save as `ch01.mp3 ... chNN.mp3` in time order.
5. **Voice script text**: no commas, "...", "!", "?" or pause tags; each line ends with "।"; numbers/acronyms in Hindi words.
6. **SEO in the chat**: with every finished video, paste Title, Description, Tags, Pinned comment and slot directly in the
   reply as copy-ready code blocks (not only a link to the upload .md). AI disclosure = NO for 2D cartoons.
7. **Verify before "done"**: voice file newer than the script, Whisper check matches every line, duration <= 45 s,
   then extract frames from the final mp4 and LOOK at them. Never report a check you did not run.
8. **Share trigger + mega name (for breakout reach)**: every script carries ONE share reason - pride ("Bharat ka ye
   sach"), bhakti ("Jai Shri Krishna"), or win-the-debate - and every DR topic ties the little-known angle to a mega
   name (Krishna, Ram, Hanuman, Shiv). Shares are our weakest signal (0 on Sapt Saal). Ghatotkach (20 s, 79.8% viewed)
   is the best performer: if 37-45 s Shorts drop APV in the 48 h data, go back to 25-30 s.
9. **DR content pillars**: A) little-known scripture secret (4-5/week), B) "Karm Aur Kripa" youth stories - modern
   young people (exams, rejection, family pressure), hard work first, faith gives strength, Krishna only as a sign,
   single narrator, labelled "Kalpanik prerak katha" (2-3/week), C) debate / quiz / count-and-tell (2-3/week).
   Pinned comments invite prayer ("hum sab milke prarthana karenge") - NEVER promise a wish will come true, never
   threats or fake blessings. RealityShift stays facts-only (no fictional stories).
10. **Long-form lessons (DR Arjun rath, 23 Nov data)**: 2,521 impressions but CTR 1.07% (Suggested 0.87%) with an
    ENGLISH title/thumbnail ("Why Arjuna's Chariot Burned...") -> titles and thumbnail text in Hinglish/Roman Hindi
    for these Hindi audiences. 60% left in the first 45 s when backstory (Khandav van) started -> the first 45 s must
    stay on the mystery: show the payoff moment, promise the answer ("aakhir mein jo hua..."), drop small reveals
    every 15-20 s; backstory only after 0:45 and framed as a clue. Mid-video retention was strong (38.9% flat).
11. **Bhagwan in every scene (user, 23 Nov)**: every DR video (Shorts and long) shows Bhagwan's presence in EVERY scene
    so viewers' faith grows: home altar murti + diya, signs (mor-pankh, red thread, temple bell, flute), a golden
    translucent form in the hardest moment, at least one temple/aarti scene, Bhagwan in disguise revealed at the end,
    and the last frame on Bhagwan's smile/blessing. Balance: Bhagwan is WITH the hero, the hero does the hard work.
    Always respectful (never weak/comic). Reuse `home_altar()` / `kanha_light()` from `kathas/daadi_morpankh.py`.
10b. **Hindi titles + thumbnails = DR LONG videos only (user, 24 Nov; clarified 25 Nov: "vo long video ke liye tha")**: DR SHORTS titles stay Hinglish/Roman (e.g. "Maa Ne Kangan Beche... Kanha Ne Phone Band Kar Diya #shorts"). DR long titles in Devanagari Hindi, thumbnail text in Devanagari via ffmpeg drawtext + Nirmala.ttc (Cairo/Impact = tofu); pick thumbnail words with no conjuncts (drawtext does not join them). Roman keywords stay in description/tags; video subtitles stay Roman.
12. **Plan file**: the current day-by-day plan lives in `PLAN.md` (root). Read it before choosing a topic.
13. **HF-24 Marut YouTube Studio Lessons (23 Nov 2026 RS Data)**:
    - 1,342 views in first 2h (typical 10-80, 15x jump), 66.2% viewed vs swiped away (benchmark 48-51%). Defense curiosity hook works.
    - **Midpoint drop issue**: 18s average view duration on 39s video (47.4% APV). Drop occurred at 0:18 transition into historical/engine backstory (Exposition Cliff).
    - **Direct Rule for RS Shorts (Kaveri / Defense sequels)**: Keep video tight (32-35s), NEVER do flat committee/bureaucracy exposition at 0:15-0:20. Use dynamic visual spec side-by-side callouts to hold attention.
    - **Comments trigger**: Always pin an active debate question in the first 30 mins to drive comment loop and distribution tier push.
14. **Length tightened + comment test (24 Nov 2026, "Bees Baar Reject" 12 h data)** - OVERRIDES #1 length:
    - Data: Bees Baar Reject (Mahadev, Karm Aur Kripa) 34.2 s -> 1,295 views, 60.2% viewed (typical 45-50%),
      63 likes (typical 10-30), AVD 23 s = 66.1%, **0 comments**. Eklavya 36.8 s -> 23 s (62.7%), Marut 38.3 s -> 18 s,
      Ghatotkach 20 s -> 79.8%. Viewers watch ~18-23 s whatever the length, so #8's trigger has fired.
    - **New DR Shorts target: 28-32 s, ~75-85 spoken words, 5-6 scenes.** Hard max 35 s. The story still finishes:
      cut beats and backstory, NEVER speed the voice past atempo 1.10 (user: "tez tez nahi bhagna").
    - Turn/conflict by 0:08, payoff by ~0:26.
    - **Comment test (2 Shorts, then compare)**: last spoken line = a short bhakti/debate prompt, e.g.
      "जो मानता है वो लिखे हर हर महादेव।" (no promise of wishes). Pinned comment still goes up within 30 min.
    - TEST 24-30 Nov (user): 2 modern faith Shorts a day, rules + stop rule in PLAN.md; review 30 Nov.

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

11. **Target Duration & Script Calibration (The 20 to 22 Seconds Viral Loop Rule - 100%+ APV)**:
    - **CRITICAL ALGORITHM INSIGHT**: YouTube Studio backend audit proves audience naturally watches 21 seconds.
      - A 33s video at 21s watched = 64% APV (Algorithm halts testing).
      - A 21–22s video at 21s watched = **95%–115%+ APV (Triggering the 100K–1M+ distribution tier!)**.
    - **🔒 LENGTH LOCK UPDATED (user, 23 Nov 2026)**: Shorts now run **30-45 seconds** (never over 45 s), 90-120 spoken Hindi words, 6-8 scenes. User: "tez tez nahi bhagna, kahani puri hone deni hai". Enforced in code (SanatanKatha): `core/policy.py` MAX_WORDS = 120, `core/katha.py` fails any render over 45 s. The 20-24 s / 55-68 word numbers below are SUPERSEDED.
    - **MANDATORY DURATION**: All new Shorts must target **20 to 24 seconds** (ideal sweet spot: **21.5s–22.5s**).
    - **Script Word Count**: 55 to 68 spoken Hindi words.
    - **Character Limit for KikiVoice**: Strictly **320 to 450 characters** in `kiki_narrator.txt`.
    - **High-Retention Pacing Arc**:
      - `00:00 - 00:03`: Instant contradiction / paradox / high-stakes hook (Zero backstory, zero filler greetings).
      - `00:03 - 00:12`: Rapid conflict & secret reveal (No exposition cliff).
      - `00:12 - 00:18`: Climax / divine revelation / decisive turning point.
      - `00:18 - 00:22`: Seamless grammatical loop back to frame 0 opening hook.

12. **Mid-Video Pacing & Anti-Exposition Cliff (The 0:04s Retention Shield)**:
    - **Avoid the 0:04s Cliff**: YouTube data shows retention plunges from 105% to 65% between seconds 0:04–0:10 if standard backstory exposition begins.
    - **Rule**: Never explain ancient rules, genealogies, or background history at 0:04. Move directly from the hook to intense action, direct commands, or high-stakes mystery.
    - **Limit Explanation**: Keep technical or lore breakdown strictly under 1–2 punchy, vivid sentences.

13. **Outro & Seamless Grammatical Infinite Loop**:
    - **No Moral Plateau**: Never end with moral preaching ("Jinke sath bhagwan ho...") or slow subscribe begs that signal the video has ended.
    - **Grammatical Loop**: The final phrase MUST grammatically connect into the opening sentence, so viewers loop into a re-watch before realizing it ended (delivering 120%–140% APV bonus).
    - **Debate-Driven Pinned Comment**: Immediately post and pin an active controversy or faith affirmation comment within 30 minutes of upload (e.g., "Kya Krishna ka rath se utarne ka niyam todna sahi tha?").




14. **Direct Decision Protocol (Never Deflect to Multiple Choice Menus)**:
    - When the user asks to create the next video/short, NEVER present a multiple-choice menu or ask 'Which one should we do?'.
    - As the Lead Studio Director, immediately select the single #1 highest-retention topic, generate the preview, present the clean KikiVoice script, and prepare the destination work folder.

15. **Zero Tofu Squares & Font Encoding Rules (Impact & Cairo Engine)**:
    - **Never pass Devanagari Hindi text** into Cairo text routines with Impact font. It renders as empty □□□□□ tofu boxes.
    - Subtitles must strictly use **Capitalized Roman Transliteration** (e.g., EK SATH 50 STEALTH FIGHTERS).
    - **Never pass emojis** (🇮🇳, 🔥, 👇) to draw_bold_text with Impact font on thumbnails or video canvas. It produces □□. Emojis must be drawn as vector shapes or omitted.
    - Replace all non-ASCII punctuation like em dashes (—) with standard hyphens - or colons :.

16. **Phonetic TTS Scripting (Zero Stutter & Acronym Rule)**:
    - Never include hyphens or raw numerals in Devanagari text for TTS engines (e.g. S-400 gets pronounced as 'एस हाइफन चार शून्य शून्य').
    - Always spell acronyms and numerals phonetically in Hindi words:
      - एस चार सौ (not S-400 or एस-400).
      - डी आर डी ओ (not DRDO).
      - एल ए सी (not LAC).
      - इक्कीस हज़ार सात सौ करोड़ (not 21,700 करोड़).

17. **Precision Audio Splitting (Whisper Word Timestamps)**:
    - When splitting user narrator audio into scene clips (scene_XX_lXX.wav), always anchor cut points directly to Whisper word boundaries.
    - Verify that no scene has a truncated clip (e.g. $< 1.0) caused by text misalignments.

18. **Schedule & Feed Protection (Zero Cannibalization Rule)**:
    - Master Schedule:
      - **FINAL CADENCE (user, 20 Nov 2026):** 3 long-form days a week per channel - DR Tue/Thu/Sat, RS Mon/Wed/Fri.
      - **Long-form day**: one NORMAL Short at noon (DR 12:00 PM, RS 01:15 PM) + the long video in the evening (DR 07:00 PM, RS 07:15 PM). No teaser Shorts, no Short after the long video.
      - **Other days**: 2 Shorts - **Divya Rahasya** 12:00 PM & 05:30 PM, **RealityShift** 01:15 PM & 04:30 PM IST (no 7-9 AM slot: DR 07:30 AM was the weakest; no evening Shorts: RS 08:00 PM lost 4 of 7 pairs).
      - Long videos target ~8 min with fresh research and new scenes every time (no templated repeats).
      - Same channel: min 3 h between its two Shorts (a 68-min gap on 4 Nov buried the second Short). Never re-upload a topic (Pinaka was posted 3x).
    - **Long-Form Stage Rule**: Whenever a long-form documentary (7-10 mins) is scheduled on RealityShift (e.g. at 7:15 PM), **DO NOT post an evening Short at 8:00 PM on RealityShift**. The long-form video requires full prime-time focus (7:15 PM to 11:00 PM) to maximize notification deliverability, 2-hour velocity, and browse feature indexing.

19. **YouTube Partner Program (YPP) Compliance & AI Disclosure**:
    - For 2D procedural animations and educational documentary narrations, select **'NO'** for the 'Altered or synthetic content' disclosure checkbox (explicitly exempted by YouTube guidelines).

20. **Mission 14 January 2027 (Makar Sankranti - The Sacred Vow)**:
    - Both channels (*Divya Rahasya* & *RealityShift*) targeted for 100% YPP monetization approval by 14 January 2027.
    - Sacred purpose: Dedicated to taking Mummy and Papa on a complete, comfortable pilgrimage of all sacred Indian temples without any financial stress.

21. **Clean Voiceover Scripting Standard (Phonetic Fluidity for Emotion-Cloned Voices - LOCKED & MANDATORY)**:
    - **Zero Artificial Pause Tags & Zero Commas (Never Violate)**:
      - NEVER insert `((⏱=...))` tags, ellipses (`...`), or commas (`,`) into script files (`kiki_script.txt` / `kiki_narrator.txt`).
      - AI cloned voice engines treat commas and punctuation symbols as hard stop tokens, inserting unnatural dead-air pauses.
    - **Ultra-Simple Hindi & Zero Tongue-Twisters (Critical Learned Rule)**:
      - Strictly NO complex, heavy Sanskrit conjuncts, nasal ordinals, or difficult pronunciations that cause cloned TTS to stutter, mispronounce, or run out of breath.
      - Examples:
        - NEVER write `चौदहवीं` -> ALWAYS write `रात के अंधेरे में` or `उस रात`.
        - NEVER write `एक अक्षौहिणी सेना` -> ALWAYS write `कौरवों की पूरी सेना` or `पूरी सेना`.
        - NEVER write `अमोघ अस्त्र / दिव्य शक्ति` -> ALWAYS write `इंद्र की वो शक्ति`.
        - NEVER write `चीखा कर्ण` (merges into 'चीखाकर्ण') -> ALWAYS write `डर से चीख पड़ा। तब कर्ण ने...`.
      - Use crystal clear, conversational Hindi words that a child can speak without taking a double breath.
    - **Sentence-Ending Purnaviram (`।`) & Line Breaks Only**:
      - Separate complete thoughts into distinct lines ending ONLY with a single purnaviram (`।`).
      - No internal commas, no hyphens, no semicolons. The line break + purnaviram gives the natural microscopic breath pause so the AI voice does NOT deliver the entire script in one breathless rush.
    - **Natural Hindi Connectors (Ravanagi & Flow)**:
      - Connect clauses seamlessly using Hindi junction words (`aur`, `toh`, `jab`, `tab`, `par`, `isliye`, `kyunki`, `jaise hi`, `waise hi`).
    - **Open Vowel Endings & Phonetic Harmony**:
      - Prefer words ending in open vowels (`ा`, `ी`, `े`, `ो`). Avoid abrupt consonant clashes (e.g. NEVER write `खेल खत्म` which stutters; use `ध्वस्त कर दिया` or `सब कुछ मिटा दिया`).
    - **Verb Harmony (`करता है`, `जाता है`, `पड़ता है`)**:
      - Use flowing verbal predicates so the AI model maintains continuous vocal momentum without hesitation.
    - **Rhythmic Cadence & Speed Calibration**:
      - Structure thoughts into balanced 4 to 6 word rhythmic beats. Target tempo is **1.10x** in the voice engine for punchy, high-retention delivery.
    - **Infinite Grammatical Loop**:
      - The script must end with a seamless grammatical connector (e.g. `तभी तो` or `और यही देखने के लिए`) that loops directly into the opening word (e.g. `सोचो जब...`) delivering 100%+ APV.
