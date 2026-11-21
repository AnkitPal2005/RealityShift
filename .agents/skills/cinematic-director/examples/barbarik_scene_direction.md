# Cinematic Scene Direction: Barbarik (Option A — Sanskrit Puranic Account)

- **Topic**: `BARBARIK SKANDA PURANA`
- **Video Format**: 9:16 Vertical Video (1080 $\times$ 1920 pixels, 30 FPS)
- **Target Engine**: Sanatan Katha Procedural Cairo Engine (`story-pipeline/SanatanKatha`)
- **Voiceover Timing Status**: Provisional Timings (calculated from approved 184-word narration at 2.3 w/s + 4.5s pauses; subject to exact synchronization upon actual voiceover recording).

---

## Scene 1: Hook — Sudarshan Se Sheesh? (00.0s – 09.7s)

- **1. Scene Objective**: Instantly arrest viewer scrolling on YouTube Shorts by juxtaposing an enigmatic warrior silhouette with three glowing arrows against a sudden celestial revelation of the Sudarshana Chakra.
- **2. Voiceover Dialogue**:
  ```text
  ज़रा सोच के देखो... [PAUSE 0.5s]
  महाभारत युद्ध से ठीक पहले,
  श्री कृष्ण ने बर्बरीक का शीश सुदर्शन चक्र से क्यों काटा? [PAUSE 0.5s]
  ```
- **3. Duration & Timestamps**:
  - *Duration*: 9.7 seconds (Provisional)
  - *Time Span*: `00.0s – 09.7s`
  - *Word Count*: 20 words | 2 pauses (1.0s)
- **4. Characters Present**:
  - `dv.barbarik`: Centered at $x = 540, y = 1170$, scale `0.74`. Drawn as a backlit, noble warrior silhouette against the crimson sunset.
- **5. Character Actions & Expressions**:
  - Starts in calm standing posture (`pose="stand"`, `mood="fierce"`).
  - Subtle breathing cycle (`math.sin(t * 3)` elevates chest by 4px).
  - At $t_l = 3.5\text{s}$, his eyes glow softly as his hand rests on his unstrung bow.
- **6. Background & Environment**:
  - Setting: Dusk Kurukshetra battlefield perimeter.
  - Sky: Deep twilight gradient using `dv.sky(ctx, "#2B1238", "#C2492E", "#3A1A12", 0.5)`.
  - Distant silhouettes of rolling hills (`dv.hill`) and fluttering war standards.
- **7. Layer Stacking Order**:
  - *Layer 1 (Far BG)*: Dusk sky gradient with faint evening stars (`dv.stars(ctx, t, n=30)`).
  - *Layer 2 (Mid BG)*: Dark hills (`dv.hill`) and silhouetted chariot banners.
  - *Layer 3 (Stage)*: Ground line (`GROUND = 1180`), Barbarik centered at $x = 540$.
  - *Layer 4 (FG Atmosphere)*: Drifting golden dust motes drifting across horizontally (`circle` with alpha 0.15).
  - *Layer 5 (UI)*: Top header (~DIVYA RAHASYA~), ribbon `SUDARSHAN SE SHEESH?` at $x = 540, y = 300$, kinetic captions at $y = 1290$.
- **8. Camera Movement**:
  - Slow, relentless push-in zoom:
    $$\text{scale} = 1.0 + 0.10 \times \text{ease\_out\_cubic}(t_l / 9.7) \quad \text{centered at } (540, 800)$$
- **9. Lighting & Atmosphere**:
  - Dark, brooding, high-contrast silhouette with a rich amber rim-light.
  - At $t_l = 5.0\text{s}$, a pulsing cyan-gold radial glow (`glow(ctx, 540, 600, 350, "#4AE5FF", 0.35)`) flares behind him, foreshadowing Krishna's Sudarshana Chakra.
- **10. Particles & Visual Effects**:
  - Three distinct fiery light beams illuminate above his quiver.
  - Subtle drifting ember dust (`speed = 40px/s`).
- **11. Transition to Next Scene**:
  - Soft cross-dissolve (0.5s duration) into the celestial golden aura of Satyaloka.
- **12. Existing Engine Primitives Used**:
  - `dv.sky`, `dv.hill`, `dv.barbarik`, `dv.stars`, `dv.ribbon`, `glow`, `circle`.
- **13. Unsupported Features / Technical Limitations**:
  - No 3D volumetric smoke; atmospheric haze is rendered via layered alpha circles and sky gradients.

---

## Scene 2: Lord Brahma Pronouncing the Curse (09.7s – 30.3s)

- **1. Scene Objective**: Establish the theological origin of the sacrifice in the previous cosmic Yuga—Yaksha Suryavarcas's boast before Lord Brahma and the creator's fateful curse.
- **2. Voiceover Dialogue**:
  ```text
  स्कंद पुराण के अनुसार, भीम के पोते बर्बरीक पिछले जन्म में सूर्यवर्चा नाम के यक्ष थे। [PAUSE 0.5s]
  जब उन्होंने कहा कि वे अकेले धरती का सारा बोझ हल्का कर सकते हैं,
  तब ब्रह्मा जी ने शाप दिया— [PAUSE 0.5s]
  कि महायुद्ध से पहले स्वयं भगवान उनका शीश काटेंगे।
  ```
- **3. Duration & Timestamps**:
  - *Duration*: 20.6 seconds (Provisional)
  - *Time Span*: `09.7s – 30.3s`
  - *Word Count*: 45 words | 2 pauses (1.0s)
- **4. Characters Present**:
  - Yaksha Suryavarcas (rendered via `dv.silhouette(dv.barbarik, c="#2A101C", a=0.9)` at $x = 260, y = 1170$, scale `0.72`).
  - Lord Brahma (`brahma` [Katha-level procedural routine] at $x = 760, y = 1050$, scale `0.74`, seated upon golden celestial lotus `dv.lotus`, with white beard, golden crown, and radiant halo `dv.halo`).
- **5. Character Actions & Expressions**:
  - *Beat 1 (0.0s – 8.0s)*: Yaksha Suryavarcas stands proudly before Lord Brahma, boasting of his independent power to relieve the Earth's burden.
  - *Beat 2 (8.0s – 14.5s)*: Lord Brahma raises his right hand in stern divine decree, eyes flashing with cosmic authority as he pronounces the curse.
  - *Beat 3 (14.5s – 20.6s)*: Yaksha's proud posture collapses; he bows his head submissively before the creator deity.
- **6. Background & Environment**:
  - Setting: Celestial assembly in Satyaloka.
  - Sky: Shimmering gold and deep violet gradient (`dv.sky(ctx, "#18061F", "#661C4C", "#D9822B", 0.55)`).
  - Floating cosmic lotus petals and 70 twinkling stars (`dv.stars`).
- **7. Layer Stacking Order**:
  - *Layer 1*: Deep violet-cosmic sky with celestial ray wheel (`dv.sun_disc` behind Brahma).
  - *Layer 2*: Distant celestial cloud tiers.
  - *Layer 3*: Ground mist platform at $y = 1180$; Yaksha silhouette ($x=260$), Lord Brahma seated on lotus throne ($x=760$).
  - *Layer 4*: Radiating golden light beams cascading down from Brahma toward the Yaksha.
  - *Layer 5*: Ribbon `BRAHMA KA SHRAP` at $x = 540, y = 300$, kinetic captions.
- **8. Camera Movement**:
  - Slow diagonal camera drift: camera gently pans rightward and upward from the Yaksha toward Lord Brahma ($dx = 30 \times u, dy = -20 \times u$).
- **9. Lighting & Atmosphere**:
  - High-key celestial golden backlight from Brahma's halo, casting long dramatic rim lighting on the Yaksha silhouette.
- **10. Particles & Visual Effects**:
  - Rotating solar rays behind Brahma's crown (`rays=24`).
  - Shimmering starlight field.
- **11. Transition to Next Scene**:
  - Warm amber dissolve into the sacred sacrificial flames of Sage Vijaya.
- **12. Existing Engine Primitives Used**:
  - `dv.sky`, `dv.sun_disc`, `dv.stars`, `dv.lotus`, `dv.halo`, `dv.silhouette`, `dv.barbarik`, `dv.ribbon`, `glow`.
- **13. Unsupported Features / Technical Limitations**:
  - Lord Brahma is a custom katha-level composite routine (using `devta.py` primitives like `smooth`, `ell`, `eye`, `lotus`, `halo`), as `dv.brahma` is not pre-built in the shared engine.

---

## Scene 3: Three Beats of Sacred Homa Ash (30.3s – 41.2s)

- **1. Scene Objective**: Faithfully depict the exact scriptural event of *Skanda Purana* Ch. 63, vv. 73–81—Vijaya offering the sacred ash, Barbarika's initial refusal, and his subsequent acceptance upon divine advice—as three distinct visual beats.
- **2. Voiceover Dialogue**:
  ```text
  विजय नाम के ब्राह्मण ने उन्हें यज्ञ की पवित्र भस्म दी। [PAUSE 0.5s]
  बर्बरीक ने पहले मना किया, पर देवताओं के कहने पर उसे ले लिया।
  ```
- **3. Duration & Timestamps**:
  - *Duration*: 10.9 seconds (Provisional)
  - *Time Span*: `30.3s – 41.2s`
  - *Word Count*: 24 words | 1 pause (0.5s)
- **4. Characters Present**:
  - Brahmin Vijaya (`dv.brahmin` at $x = 280, y = 1170$, scale `0.72`, holding staff).
  - Fire Altar (`dv.yagya_kund` at $x = 540, y = 1180$, scale $0.85$).
  - Barbarika (`dv.barbarik` at $x = 800, y = 1170$, scale `0.72`, `flip=True`, facing left).
- **5. Character Actions & Expressions (Three Distinct Visual Beats)**:
  - *Beat 1 — The Offering ($t_l = 0.0\text{s} - 3.8\text{s}$)*:
    Vijaya stands beside the leaping fire of `dv.yagya_kund`, holding out a leaf-bowl containing glowing sacred ash toward Barbarika.
  - *Beat 2 — The Initial Refusal ($t_l = 3.8\text{s} - 7.2\text{s}$)*:
    Barbarika steps back slightly, raises his open palms upward in polite refusal, shaking his head gently (`look=(-0.2, 0.0)`), expressing ascetic non-attachment.
  - *Beat 3 — Divine Counsel & Acceptance ($t_l = 7.2\text{s} - 10.9\text{s}$)*:
    Golden celestial light rays descend from the upper sky (representing the Devas' advice); Barbarika's expression softens in understanding. He steps forward, bows his head, and cups his hands forward, reverently accepting the sacred ash.
- **6. Background & Environment**:
  - Setting: Sacred hermitage at Guptakshetra / Mahisagara Sangama.
  - Sky: Dawn twilight gradient (`#1C2A3A` to `#F49E42` to `#3B1E12`).
  - Foliage silhouettes in the distant background.
- **7. Layer Stacking Order**:
  - *Layer 1*: Dawn sky gradient.
  - *Layer 2*: Distant forest tree silhouettes.
  - *Layer 3*: Ground line, Brahmin Vijaya ($x=280$), Yagya Kund with leaping flame ($x=540$), Barbarika ($x=800$).
  - *Layer 4*: Rising translucent smoke and glowing fire sparks drifting upward; descending celestial light beam in Beat 3.
  - *Layer 5*: Ribbon `PAVITRA BHASMA` at $x = 540, y = 300$, captions.
- **8. Camera Movement**:
  - Static two-shot during Beats 1 & 2; subtle push-in toward Barbarika's hands in Beat 3.
- **9. Lighting & Atmosphere**:
  - Warm, flickering orange firelight cast from `dv.yagya_kund` (`math.sin(t * 11)` dynamic intensity).
- **10. Particles & Visual Effects**:
  - Procedural leaping flame ribbons in `dv.yagya_kund`.
  - Floating glowing ash motes rising gently from the altar.
- **11. Transition to Next Scene**:
  - Rapid snap-cut to the tense battle skies of Kurukshetra.
- **12. Existing Engine Primitives Used**:
  - `dv.brahmin`, `dv.yagya_kund`, `dv.barbarik`, `dv.sky`, `dv.ribbon`, `glow`.
- **13. Unsupported Features / Technical Limitations**:
  - Ash powder cannot be simulated with dynamic fluid meshes; rendered symbolically through glowing golden particles moving between characters.

---

## Scene 4: Sudarshana Decapitation (41.2s – 51.7s)

- **1. Scene Objective**: Execute the dramatic turning point—Shri Krishna releasing the Sudarshana Chakra to fulfill Brahma's decree, depicted with supreme devotional majesty and zero graphic violence.
- **2. Voiceover Dialogue**:
  ```text
  ब्रह्मा जी के शाप को पूरा करने के लिए,
  श्री कृष्ण ने सुदर्शन चक्र से बर्बरीक का शीश धड़ से अलग कर दिया। [PAUSE 0.5s]
  ```
- **3. Duration & Timestamps**:
  - *Duration*: 10.5 seconds (Provisional)
  - *Time Span*: `41.2s – 51.7s`
  - *Word Count*: 23 words | 1 pause (0.5s)
- **4. Characters Present**:
  - Shri Krishna (`dv.krishna` at $x = 260, y = 1170$, scale `0.76`, `pose="stand"`, `aura=True`).
  - Barbarika (`dv.barbarik` at $x = 800, y = 1170`, scale `0.72`, `flip=True`, facing Krishna).
- **5. Character Actions & Expressions**:
  - Krishna extends his right hand; above his finger, the Sudarshana Chakra spins at high speed.
  - Barbarika lowers his bow with a serene smile of total surrender (*Sharanagati*).
  - At $t_l = 5.2\text{s}$, the Chakra sweeps forward in an arc of blinding white-gold light.
- **6. Background & Environment**:
  - Setting: Kurukshetra battle perimeter, stormy twilight sky with thunderous violet-red clouds.
  - Armies visible in the deep background (`dv.army`).
- **7. Layer Stacking Order**:
  - *Layer 1*: Dramatic stormy sky.
  - *Layer 2*: Distant battle lines (`dv.army` left and right).
  - *Layer 3*: Ground stage; Krishna ($x=260$), Barbarika ($x=800$).
  - *Layer 4*: Blinding sweep of the Sudarshana Chakra, expanding white flash, burst of pink lotus petals (`dv.lotus`, `dv.petals`).
  - *Layer 5*: Ribbon `SUDARSHAN CHAKRA` at $x = 540, y = 300$, captions.
- **8. Camera Movement**:
  - At $t_l = 5.2\text{s}$ (the strike), execute an instantaneous 6-frame camera impact shake (`dx = (rnd(t*30)-0.5)*12px`), followed by a smooth full-screen white flash (`flash(ctx, u, dur=0.5)`).
- **9. Lighting & Atmosphere**:
  - Deep blue and golden contrasting halos. Instantaneous screen-clearing flash of pure white celestial light (`#FFFFFF`) upon impact.
- **10. Particles & Visual Effects**:
  - Spinning procedural Chakra disc with radiating teeth.
  - Barbarika's physical torso dissolves into expanding golden light particles (NO blood, NO wounds, NO severed flesh).
- **11. Transition to Next Scene**:
  - Blinding white light dissolves smoothly to reveal the high mountain summit touching the sky.
- **12. Existing Engine Primitives Used**:
  - `dv.krishna`, `dv.barbarik`, `dv.army`, `dv.sky`, `dv.lotus`, `dv.petals`, `dv.ribbon`, `flash`, `glow`.
- **13. Unsupported Features / Technical Limitations**:
  - Explicit graphic decapitation is strictly prohibited; handled procedurally via divine flash, light dissolution, and flower showers.

---

## Scene 5: Goddess Candika & Amrita Immortality (51.7s – 64.9s)

- **1. Scene Objective**: Reveal Goddess Candika's appearance to sanctify the severed head with celestial nectar (*amrita*), immortalizing Barbarika to witness the entire war.
- **2. Voiceover Dialogue**:
  ```text
  तभी देवी चंडिका ने कटे शीश पर अमृत छिड़क कर उसे अमर कर दिया। [PAUSE 0.5s]
  भगवान के वरदान से, उस शीश को पहाड़ की चोटी पर रख दिया गया। [PAUSE 0.5s]
  ```
- **3. Duration & Timestamps**:
  - *Duration*: 13.2 seconds (Provisional)
  - *Time Span*: `51.7s – 64.9s`
  - *Word Count*: 28 words | 2 pauses (1.0s)
- **4. Characters Present**:
  - Goddess Candika (`dv.devi` at $x = 300, y = 1170$, scale `0.74`, `pose="bless"`, glowing with vibrant red-gold aura).
  - Mountain peak (`dv.hill` spanning $x = 600$ to $1080$, height $450\text{px}$).
  - Conscious Sheesh Roop (`dv.shyam` at $x = 820, y = 780$, scale `0.65`, resting atop the mountain peak).
- **5. Character Actions & Expressions**:
  - Goddess Candika raises her right hand in *Abhaya/Varada Mudra*; her divine countenance radiates motherly grace.
  - From her palm, cascading droplets of luminous golden nectar fall toward the head.
  - The conscious head opens its radiant eyes with a calm, peaceful expression; a brilliant divine halo blooms around it.
- **6. Background & Environment**:
  - Setting: Lofty mountain peak overlooking Kurukshetra, swirling ethereal clouds at sunset.
  - Sky: Vibrant twilight gradient with soft stars above.
- **7. Layer Stacking Order**:
  - *Layer 1*: Celestial mountain sky with drifting evening clouds.
  - *Layer 2*: Mountain peak silhouette (`dv.hill`).
  - *Layer 3*: Ground line; Goddess Candika at left ($x=300$), conscious head atop peak at right ($x=820, y=780$).
  - *Layer 4*: Cascading amrita light sparkles and drifting lotus petals (`dv.petals`).
  - *Layer 5*: Ribbon `AMRIT VARDAAN` at $x = 540, y = 300$, captions.
- **8. Camera Movement**:
  - Gentle upward tilt and push-in: camera starts at ground level with Goddess Candika and slowly floats upward toward the radiant head on the summit.
- **9. Lighting & Atmosphere**:
  - Heavenly pink-gold radiance from Goddess Candika (`#FF6B8B`), balanced by the serene cyan-white glow of the immortal head.
- **10. Particles & Visual Effects**:
  - Cascading golden nectar droplets (`circle` with pulsating radius and golden glow).
  - Drifting sacred lotus petals (`dv.petals(ctx, t, n=25)`).
- **11. Transition to Next Scene**:
  - Slow dissolve shifting perspective to the wide, panoramic battle viewed from the mountain peak.
- **12. Existing Engine Primitives Used**:
  - `dv.devi`, `dv.hill`, `dv.shyam`, `dv.sky`, `dv.petals`, `dv.ribbon`, `glow`.
- **13. Unsupported Features / Technical Limitations**:
  - Nectar fluid dynamics are rendered procedurally using descending particle rings and alpha tracers.

---

## Scene 6: The Unified Hari-Hara Form (64.9s – 79.7s)

- **1. Scene Objective**: Faithfully depict Barbarik's Puranic testimony (*Skanda Purana* Ch. 66, vv. 90–94) as a single unified composite deity (*Hari-Hara*) fighting the enemies—NOT two separate characters standing side-by-side.
- **2. Voiceover Dialogue**:
  ```text
  युद्ध के अंत में बर्बरीक के शीश ने बताया— [PAUSE 0.5s]
  कि मैदान में उन्होंने एक ही रूप देखा,
  जिसमें शिव और विष्णु दोनों एक साथ थे!
  एक ओर त्रिशूल, तो दूसरी ओर सुदर्शन चक्र!
  ```
- **3. Duration & Timestamps**:
  - *Duration*: 14.8 seconds (Provisional)
  - *Time Span*: `64.9s – 79.7s`
  - *Word Count*: 33 words | 1 pause (0.5s)
- **4. Characters Present**:
  - Unified Hari-Hara Cosmic Form (centered at $x = 540, y = 1170$, scale `0.78`):
    - **Single composite body** split down the exact vertical center:
      - *Left Half (Hara / Shiva)*: Ash-smeared pale skin (`#B0C4DE`), crescent moon in matted hair (*jata*), tiger skin drape, holding the glowing golden `dv.trishul` in aloft left arm.
      - *Right Half (Hari / Vishnu)*: Radiant dark cyan-blue skin (`#74B4E8`), golden *kirita mukut*, yellow Pitambar dhoti, Kaustubha jewel on chest, holding the spinning Sudarshana Chakra aloft in right arm.
  - Observing conscious head (`dv.shyam`) in the foreground corner ($x = 180, y = 480$, scale `0.50`).
- **5. Character Actions & Expressions**:
  - The unified Hari-Hara figure radiates majestic cosmic power.
  - The left hand brandishes the glowing golden trident; the right hand rotates the luminous Sudarshana Chakra.
  - Pulsing dual-colored halo (`#E6F0FA` on the Shiva side, `#FFD700` on the Vishnu side).
- **6. Background & Environment**:
  - Setting: Vast, cosmic battlefield plain seen under a surreal celestial twilight sky.
  - Below, distant armies are reduced to miniature silhouetted specks.
- **7. Layer Stacking Order**:
  - *Layer 1*: Cosmic nebula sky (`dv.sky` blending deep violet, crimson, and golden amber).
  - *Layer 2*: Distant battlefield horizon.
  - *Layer 3*: Central unified Hari-Hara divine form ($x=540$).
  - *Layer 4*: Expanding concentric shockwaves of silver and golden light; Trishul and Chakra trails.
  - *Layer 5*: Barbarik's head in observing foreground ($x=180$), ribbon `SHIV-VISHNU EK ROOP` at $x=540, y=300$, captions.
- **8. Camera Movement**:
  - Epic slow pull-back revealing the staggering cosmic scale:
    $$\text{scale} = 1.10 - 0.10 \times \text{ease\_out\_cubic}(t_l / 14.8)$$
- **9. Lighting & Atmosphere**:
  - Split-chroma lighting: Sacred ash-white and lunar silver light on the left; golden-amber and solar-cyan radiance on the right.
- **10. Particles & Visual Effects**:
  - Swirling celestial energy aura; dual light trails emanating from the Trishul and Sudarshana Chakra simultaneously.
- **11. Transition to Next Scene**:
  - Harmonious, warm cross-fade into the sacred sanctum darshan.
- **12. Existing Engine Primitives Used**:
  - `dv.krishna`, `dv.trishul`, `dv.shyam`, `dv.sky`, `dv.ribbon`, `glow`, `circle`.
- **13. Unsupported Features / Technical Limitations**:
  - The unified Hari-Hara form is implemented as a custom katha-level composite routine using Cairo vertical clipping (`ctx.clip()`) to merge the Shiva half and Vishnu half onto a single anatomical rig.

---

## Scene 7: Devotional Salutation & CTA (79.7s – 84.5s)

- **1. Scene Objective**: Provide a peaceful, reverent devotional conclusion, celebrating the sanctity of Barbarik's Puranic sacrifice and leaving the audience in contemplative surrender.
- **2. Voiceover Dialogue**:
  ```text
  स्कंद पुराण की इस पावन कथा को प्रणाम।
  जय श्री कृष्ण।
  ```
- **3. Duration & Timestamps**:
  - *Duration*: 4.8 seconds (Provisional)
  - *Time Span*: `79.7s – 84.5s`
  - *Word Count*: 11 words | 0 pauses
- **4. Characters Present**:
  - Shri Krishna in supreme blessing pose (`dv.krishna` at $x = 540, y = 1170$, scale `0.78`, `pose="bless"`, smiling with full divine radiance).
- **5. Character Actions & Expressions**:
  - Right hand raised in eternal *Abhaya Mudra*; eyes filled with boundless compassion.
  - Continuous gentle breathing motion; peacock feather swaying softly in divine breeze.
- **6. Background & Environment**:
  - Setting: Luminous temple sanctum glow.
  - Sky: Warm saffron and deep gold gradient (`#2A0A14` to `#7A1A28` to `#D9822B`).
- **7. Layer Stacking Order**:
  - *Layer 1*: Warm sanctum gradient with 20 rotating golden light rays (`temple_bg`).
  - *Layer 2*: Soft sacred diya glow at base.
  - *Layer 3*: Shri Krishna centered at $x = 540, y = 1170$.
  - *Layer 4*: Cascading sacred lotus petals falling across the screen (`dv.petals`).
  - *Layer 5*: Ribbon `JAI SHRI KRISHNA` at $x = 540, y = 300$, clean bottom CTA prompt.
- **8. Camera Movement**:
  - Very slow, dignified push-in toward Krishna's serene eyes:
    $$\text{scale} = 1.0 + 0.05 \times \text{ease\_out\_cubic}(t_l / 4.8)$$
- **9. Lighting & Atmosphere**:
  - Rich, warm devotional gold and saffron atmosphere. Soft radial bloom filling the screen.
- **10. Particles & Visual Effects**:
  - Drifting sacred pink lotus petals (`dv.petals(ctx, t, n=35)`).
  - Pulsing divine halo behind Krishna's crown.
- **11. Transition to Next Scene**:
  - Clean fade to black (1.0s duration).
- **12. Existing Engine Primitives Used**:
  - `dv.krishna`, `temple_bg`, `dv.petals`, `dv.ribbon`, `glow`.
- **13. Unsupported Features / Technical Limitations**:
  - None. All primitives exist in `core/devta.py` and `core/katha.py`.
