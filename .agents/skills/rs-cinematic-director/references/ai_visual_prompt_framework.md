# RealityShift: AI Visual Prompt Engineering Framework

This reference guide establishes the tool-agnostic prompt architecture, formatting standards, and negative constraint protocols for generating photorealistic cinematic visuals for RealityShift (@RealityShiftByAnkit).

---

## 1. The RealityShift Prompting Philosophy

AI visual generation in RealityShift must reject generic, vague buzzwords like *"make it 8k, hyperrealistic, trending on artstation"*. Instead, prompts must use **precise optical, physical, photographic, and cinematic vocabulary**:

1. **Photographic Specificity**: Specify camera sensor, lens focal length, aperture, lighting rig, and atmospheric medium as if directing a live-action high-budget sci-fi cinematographer.
2. **Strict Tool-Agnostic Structure**: Formulated so the prompt works cleanly across Midjourney v6, Flux.1, Stable Diffusion XL, or video models (Runway Gen-3, Luma Dream Machine, Kling, Pika).
3. **The Zero-Text Rule**: **Never ask the AI generator to render readable text, numbers, HUD symbols, or logos**. Generative models mangle typography into unreadable gibberish. All graphic overlays, HUD elements, numbers, and subtitles are planned as separate post-production layers for Skill 4.

---

## 2. Standardized AI Image Prompt Architecture

Every image asset prompt must follow this 7-part modular schema:

```text
[ASSET ID: AST-XX]
Format: 9:16 Vertical Canvas (--ar 9:16)
Type: Photorealistic AI Still

PROMPT:
[1. SUBJECT & ACTION]: Core astronomical object, landscape, character, or device.
[2. PHYSICAL DETAILS & TEXTURE]: Specific material properties, crater depths, cloud bands, metallic sheen.
[3. ENVIRONMENT & SETTING]: Deep space void, orbital plane, coastal mudflat, cleanroom, atmospheric haze.
[4. COMPOSITION & FRAMING]: Vertical 9:16, extreme wide / close-up, rule-of-thirds, camera elevation.
[5. LIGHTING & EXPOSURE]: Directional key light, harsh unshielded solar glare, earthshine fill, volumetric rim.
[6. CINEMATOGRAPHY & OPTICS]: 35mm / 65mm IMAX, anamorphic lens, shallow depth of field, sharp focus, RAW photo.
[7. COLOR TREATMENT & MOOD]: Palette hex/color names, saturation control, contrast balance.

NEGATIVE PROMPT / CONSTRAINTS:
--no text, letters, words, watermark, logo, cartoon, anime, illustration, 3d render plastic, saturated neon, low quality, blurry, deformed, oversaturated
```

### 2.1 Concrete Example
```text
AST-01 (Full Moon in Space Dissolving)
Format: 9:16 Vertical (--ar 9:16)

Prompt:
An astronomical wide-angle view from high Earth orbit showing the full luminous Moon in deep space, its silver-grey regolith and Tycho crater sharply focused, beginning to subtly dissolve into faint cosmic vapor particles at its upper rim. Below in the lower third of the vertical frame, the curved horizon of Earth is visible in crescent shadow, rimmed by a thin, glowing sapphire-blue atmospheric line. Harsh directional sunlight from the left casts deep, razor-sharp black shadows inside lunar craters. Cold obsidian black space void background with pinpoint distant stars. 65mm IMAX cinematography, Hasselblad medium format satellite photography, ultra-fine texture, authentic NASA Apollo archival realism, cinematic exposure balance. --ar 9:16 --style raw

Negative Prompt:
--no text, watermark, signature, cartoon, illustration, drawing, giant explosion, fire in space, neon colors, CGI gloss, plastic texture
```

---

## 3. Standardized AI Video Prompt Architecture

When generating dynamic video clips through temporal models (Runway Gen-3, Luma, Kling), prompts must focus on **temporal motion, camera trajectory, and physical dynamics**:

```text
[VIDEO PROMPT SCHEMA]
[CAMERA MOTION]: Slow continuous push-in / vertical tilt / locked-off static hold.
[SUBJECT DYNAMICS]: Subtle water surface displacement / cloud band circulation / slow orbital wobble.
[ENVIRONMENTAL MOTION]: Subtle cosmic dust drift / starlight twinkle / atmospheric glow pulse.
[TEMPORAL PACE]: 4 to 6 seconds duration, smooth cinematic 24fps motion, zero jitter or morphing.
```

### 3.1 Concrete Example (Runway Gen-3 / Kling)
```text
AST-04-VID (Low-Tide Coastal Harbor Vignette)
[ILLUSTRATIVE VIGNETTE NOTE]: Illustrative local coastal low-tide setting to visually convey altered tidal dynamics; does not imply universal immediate ocean drainage.
Camera: Slow high-angle aerial drone descent looking down at an intertidal bay under starlit night.
Subject Dynamics: Calm coastal water resting at low tide, gently lapping against exposed wet mudflats, shallow sandbars, and anchored wooden fishing boats resting on their hulls.
Atmosphere & Lighting: Deep blue twilight with zero moonlight; distant city streetlights reflect softly on the wet mud. Sharp pinpoint stars in the clear night sky above.
Motion Quality: Photorealistic fluid mechanics, smooth cinematic water dissipation, zero unnatural wave morphing, steady camera movement.
```

---

## 4. Image-to-Video (I2V) & 2.5D Motion Instructions

When direct video generation risks hallucination, RealityShift uses **Image-to-Video (I2V) animation** or **2.5D Parallax Pan/Zoom** based on high-resolution stills:

1. **Ken Burns Motion Control (2.5D)**:
   - *Pan/Zoom Vector*: Define starting frame box and ending frame box within the $1080 \times 1920$ canvas.
   - *Scale Trajectory*: e.g. Start at $100\%$ scale at $t=0$, smoothly ease to $106\%$ scale at $t=4.0\text{s}$ using cubic ease-out.
2. **Depth Map Parallax**:
   - Separate Foreground (cranes/promenade) from Midground (harbor) and Background (sky) using depth maps.
   - Translate FG laterally by $+40\text{px}$, MG by $+15\text{px}$, and keep BG static to create genuine 3D depth on vertical screens.
3. **Subtle Particle Overlays**:
   - Overlay slow-drifting cosmic dust or light mist loops (10-15% opacity, screen blend mode) to keep static space frames alive without distracting from narration.
