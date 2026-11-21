# RealityShift Render Profiles and Export Reference

This reference details the encoding standards, container parameters, bitrate targets, and export profiles for generating YouTube Shorts in the RealityShift pipeline.

---

## 1. Master Output Delivery Specifications

To ensure optimal playback on the YouTube Shorts mobile player, avoid re-compression degradation, and enable immediate cloud processing, all final video files must adhere strictly to these container parameters:

```
+-------------------------------------------------------------+
| CONTAINER: MP4 (.mp4)                                       |
+-------------------------------------------------------------+
| VIDEO STREAM:                                               |
| - Dimensions: 1080 x 1920 pixels (Native 9:16 Vertical)      |
| - Frame Rate: 30.000 fps Constant Frame Rate (CFR)          |
| - Codec: H.264 / MPEG-4 AVC (libx264)                       |
| - Profile / Level: High Profile @ Level 4.2                  |
| - Pixel Format: yuv420p (8-bit, 4:2:0 chroma subsampling)   |
| - Color Space: bt709 (Rec.709 primaries and transfer)       |
| - Rate Control: CRF 18 (Constant Rate Factor) or VBR 18 Mbps|
| - Keyframe Interval (GOP): 30 frames (1 keyframe/second)    |
| - Container Flag: +faststart (moov atom moved to beginning) |
+-------------------------------------------------------------+
| AUDIO STREAM:                                               |
| - Codec: AAC-LC (Advanced Audio Coding - Low Complexity)    |
| - Bitrate: 320 kbps CBR                                     |
| - Sample Rate: 44,100 Hz (or 48,000 Hz)                     |
| - Channels: 2 (Stereo)                                      |
| - Integrated Loudness: -14.0 LUFS (± 0.5 LUFS)              |
| - Peak: -1.0 dBFS maximum                                   |
+-------------------------------------------------------------+
```

---

## 2. Render Profiles: Preview vs. Master

| Parameter | Profile A: Fast Preview (`--preview`) | Profile B: Master Delivery (`--master`) |
| :--- | :--- | :--- |
| **Purpose** | Visual pacing, subtitle verification, motion test. | Final YouTube Shorts upload master. |
| **Target Dimensions** | $540 \times 960$ (Proxy) or $1080 \times 1920$ Still Frames | $1080 \times 1920$ Full HD |
| **Video Codec** | `libx264` | `libx264` |
| **x264 Preset** | `veryfast` or `ultrafast` | `slow` or `medium` |
| **CRF Quality** | `26` | `18` |
| **Audio Mix** | Scratch voiceover + synthetic guide bed | Fully mixed & mastered multi-track audio |
| **Grain Layer** | Disabled (saves 40% render time) | Enabled ($2\text{--}4\%$ optical grain) |
| **Render Speed** | $\approx 4\times\text{--}6\times$ Real-time | $\approx 0.8\times\text{--}1.5\times$ Real-time |
| **Primary Output** | `build/preview_frames/` or `preview.mp4` | `build/final_output.mp4` |

---

## 3. MoviePy & FFmpeg Execution Syntax

### 3.1 Master Export via MoviePy
```python
def export_master_video(composite_clip, output_path: str):
    """Exports final master video using production parameters."""
    ffmpeg_params = [
        "-pix_fmt", "yuv420p",
        "-colorspace", "bt709",
        "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-movflags", "+faststart",
        "-g", "30",
        "-bf", "2"
    ]
    
    composite_clip.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        bitrate="18000k",
        audio_bitrate="320k",
        preset="medium",
        ffmpeg_params=ffmpeg_params,
        threads=4
    )
```

### 3.2 Post-Processing & Remux via Direct FFmpeg
If assembly is performed via intermediate scene files or requires remuxing with audio stems:
```bash
ffmpeg -y -i intermediate_video.mp4 -i mastered_audio.wav \
  -c:v copy \
  -c:a aac -b:a 320k -ar 44100 \
  -movflags +faststart \
  final_output.mp4
```

---

## 4. Render Logging Standards

Every execution of the video implementation runner must produce a comprehensive `render.log` in `output/work/<topic>/build/render.log`.

### 4.1 Required Log Telemetry
1. **Timestamp & Engine Version**: Execution start, Python/MoviePy/FFmpeg versions.
2. **System Environment**: OS, CPU architecture, GPU hardware acceleration availability.
3. **Asset Manifest Audit**: SHA-256 validation of all ingested assets.
4. **Scene Timing Breakdown**: Scene ID, start frame, end frame, duration, audio offset.
5. **Frame Render Statistics**: Total frames rendered, dropped frames, memory usage peak.
6. **Final Container Audit**: Output file size (MB), average bitrate, audio integrated loudness (LUFS).

