# RealityShift Asset Manifest Template

Use this template to catalog and audit all external media assets ingested for an episode in the RealityShift pipeline.

---

## 1. Markdown Asset Registry Table

```markdown
# Asset Manifest: [EPISODE_TOPIC]

| Asset ID | Scene | Type | Relative File Path | Dimensions | Format / Color Space | SHA-256 Checksum | Validation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `IMG_SH01_A` | Scene 01 | Image | `images/processed/SH01_A_img.png` | 1440x2560 | PNG / sRGB | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | PASS |
| `IMG_SH02_A` | Scene 02 | Image | `images/processed/SH02_A_img.png` | 1440x2560 | PNG / sRGB | `...` | PASS |
| `VID_SH03_A` | Scene 03 | Video | `videos/processed/SH03_A_vid.mp4` | 1080x1920 | H.264 / yuv420p / 30fps | `...` | PASS |
| `AUD_VO_MST` | Master | Audio | `files/narrator.mp3` | N/A | MP3 / 320 kbps / 44.1 kHz | `...` | PASS |
| `AUD_SC01` | Scene 01 | Audio | `files/scene_01_l00.wav` | N/A | WAV / 16-bit / 44.1 kHz | `...` | PASS |
| `SFX_RISER` | Transition| SFX | `sfx/warp_riser.wav` | N/A | WAV / 24-bit / 48.0 kHz | `...` | PASS |
```

---

## 2. Machine-Readable JSON Manifest (`manifest.json`)

Save this file in `story-pipeline/RealityShift/output/work/<topic>/images/manifest.json`:

```json
{
  "topic": "example_topic_slug",
  "generated_at": "2026-11-16T12:00:00Z",
  "engine_version": "RealityShift Core 2.0",
  "assets": [
    {
      "asset_id": "IMG_SH01_A",
      "scene_id": "Scene 01",
      "type": "image",
      "relative_path": "images/processed/SH01_A_img.png",
      "width": 1440,
      "height": 2560,
      "aspect_ratio": "9:16",
      "color_space": "sRGB",
      "file_size_bytes": 4512980,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "generator_model": "Flux.1 Pro",
      "validation_status": "PASS",
      "ken_burns_eligible": true
    },
    {
      "asset_id": "VID_SH03_A",
      "scene_id": "Scene 03",
      "type": "video",
      "relative_path": "videos/processed/SH03_A_vid.mp4",
      "width": 1080,
      "height": 1920,
      "fps": 30.0,
      "pixel_format": "yuv420p",
      "codec": "h264",
      "duration_seconds": 6.42,
      "sha256": "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
      "generator_model": "Runway Gen-3 Alpha",
      "validation_status": "PASS",
      "artifacts_detected": false
    }
  ]
}
```

