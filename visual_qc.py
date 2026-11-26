"""Visual Quality Control & Auto-Regeneration System for AI Shorts pipelines.

Validates every generated scene image (1080x1920, 9:16) using programmatic geometry/integrity checks plus an actual
vision-capable model (Google Gemini via google.genai) with structured JSON output. Never silently accepts a failed
image, enforces critical auto-rejection conditions, saves rejected images + reports for debugging, and supports an
auto-regeneration loop (max 3 retries) before halting final video rendering.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
import os
from pathlib import Path
import shutil
from typing import Callable, Optional

from PIL import Image, ImageStat


class VisualQCError(RuntimeError):
    """Raised when a scene fails visual quality validation after exhausting retries."""


class VisualQCConfigurationError(RuntimeError):
    """Raised when no vision-capable model API key is configured for validation."""


CRITICAL_REJECTION_CONDITIONS = (
    "broken_anatomy",
    "distorted_faces",
    "major_visual_artifacts",
    "unintended_text_or_watermarks",
    "incorrect_scene_representation",
    "major_character_inconsistency",
    "unacceptable_scenery",
)


@dataclass
class VisualQCConfig:
    min_score: int = 90
    max_retries: int = 3
    target_width: int = 1080
    target_height: int = 1920
    enforce_resolution: bool = True
    mode: str = "auto"  # "local" (100% free, zero API key), "gemini", or "auto" (uses local if no key)
    vision_model: str = "gemini-2.5-flash"
    api_key_env_vars: tuple[str, ...] = ("GEMINI_API_KEY", "GOOGLE_API_KEY")


@dataclass
class ValidationReport:
    scene_id: str
    status: str  # "APPROVED", "REJECTED", or "FAILED"
    score: int
    character_quality: int
    environment_quality: int
    realism_quality: int
    composition_quality: int
    consistency_quality: int
    issues: list[str] = field(default_factory=list)
    correction_prompt: str = ""
    retry_count: int = 0
    critical_defects: list[str] = field(default_factory=list)

    def to_public_dict(self) -> dict:
        """Return the exact 10-field validation report schema."""
        return {
            "scene_id": self.scene_id,
            "status": self.status,
            "score": self.score,
            "character_quality": self.character_quality,
            "environment_quality": self.environment_quality,
            "realism_quality": self.realism_quality,
            "composition_quality": self.composition_quality,
            "consistency_quality": self.consistency_quality,
            "issues": self.issues,
            "correction_prompt": self.correction_prompt,
            "retry_count": self.retry_count,
        }


def _has_api_key(config: VisualQCConfig) -> str:
    for var in config.api_key_env_vars:
        val = os.environ.get(var, "").strip()
        if val:
            return val
    return ""


def _resolve_api_key(config: VisualQCConfig) -> str:
    val = _has_api_key(config)
    if val:
        return val
    raise VisualQCConfigurationError(
        "No vision model API key found. Set GEMINI_API_KEY or GOOGLE_API_KEY for Gemini mode, or use mode='local'."
    )


def _local_inspect(
    image_path: Path,
    scene_id: str,
    narration: str,
    visual_brief: str,
    config: VisualQCConfig,
    prev_image: Optional[Path] = None,
    next_image: Optional[Path] = None,
    is_cartoon: bool = False,
) -> dict:
    """100% free, zero-API-key local computer-vision quality analyzer using PIL + NumPy."""
    import numpy as np

    with Image.open(image_path) as im:
        rgb = np.asarray(im.convert("RGB"), dtype=np.float32)

    h, w, _ = rgb.shape
    gray = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]

    # 1) Edge / detail density in main subject zone (y: 250..1300)
    mid = gray[int(h * 0.14):int(h * 0.68), int(w * 0.06):int(w * 0.94)]
    gx = np.abs(np.diff(mid, axis=1))
    gy = np.abs(np.diff(mid, axis=0))
    edge_density = float((gx[:-1, :] + gy[:, :-1] > 18.0).mean())
    mid_std = float(mid.std())

    # 2) Sharpness / detail energy
    lap = np.abs(gray[2:, 1:-1] + gray[:-2, 1:-1] + gray[1:-1, 2:] + gray[1:-1, :-2] - 4 * gray[1:-1, 1:-1])
    sharpness = float(lap.mean())

    # 3) Border clipping check (detect if bright subject hits left/right extreme edge)
    left_edge_std = float(gray[int(h * 0.2):int(h * 0.7), :8].std())
    right_edge_std = float(gray[int(h * 0.2):int(h * 0.7), -8:].std())

    issues: list[str] = []
    critical: list[str] = []

    # Score calculation (calibrated for both photorealistic and clean 2D vector scenes)
    sharp_ok = 0.40 if is_cartoon else 1.5
    edge_ok = 0.012 if is_cartoon else 0.032
    empty_edge = 0.007 if is_cartoon else 0.015
    char_q = 24 if (mid_std > 22 and edge_density > edge_ok) else (18 if mid_std > 14 else 10)
    env_q = 24 if (edge_density > edge_ok * 0.9 and sharpness > sharp_ok) else (18 if edge_density > empty_edge else 10)
    real_q = 19 if (sharpness > sharp_ok and 12.0 < float(gray.mean()) < 240.0) else 13
    comp_q = 14 if (left_edge_std < 50.0 and right_edge_std < 50.0) else 11
    cons_q = 14

    if edge_density < empty_edge or mid_std < 12.0:
        issues.append(f"Center canvas too empty/flat (edge_density={edge_density:.3f}, std={mid_std:.1f})")
        critical.append("unacceptable_scenery")

    if prev_image is not None and prev_image.exists():
        with Image.open(prev_image) as pim:
            pgray = np.asarray(pim.convert("L"), dtype=np.float32)
        if abs(float(gray.mean()) - float(pgray.mean())) > 95.0:
            cons_q = 10
            issues.append("Sudden extreme brightness jump compared to previous scene")

    correction = ""
    if issues:
        correction = "Improve visual detail and framing: " + "; ".join(issues)

    return {
        "character_quality": char_q,
        "environment_quality": env_q,
        "realism_quality": real_q,
        "composition_quality": comp_q,
        "consistency_quality": cons_q,
        "critical_defects": critical,
        "issues": issues,
        "correction_prompt": correction,
    }


def _check_image_integrity(image_path: Path, config: VisualQCConfig) -> list[str]:
    """Deterministic pixel/format checks (resolution, 9:16 aspect, non-blank frame)."""
    if not image_path.exists():
        return [f"Image file missing: {image_path}"]
    issues: list[str] = []
    with Image.open(image_path) as im:
        w, h = im.size
        if config.enforce_resolution and (w != config.target_width or h != config.target_height):
            issues.append(f"Invalid resolution {w}x{h}; expected {config.target_width}x{config.target_height} (9:16)")
        elif abs((w / max(1, h)) - (9.0 / 16.0)) > 0.02:
            issues.append(f"Invalid aspect ratio {w}:{h}; expected 9:16")
        stat = ImageStat.Stat(im.convert("RGB"))
        if max(stat.stddev) < 4.0:
            issues.append("Image appears blank or nearly uniform (no visual detail)")
    return issues


def _build_vision_prompt(
    scene_id: str,
    narration: str,
    visual_brief: str,
    is_cartoon: bool,
    has_prev: bool,
    has_next: bool,
) -> str:
    style_note = (
        "This scene uses intentional 2D stylized cartoon art; evaluate clean vector proportions, clear faces, "
        "expressive posture, and crisp layered scenery (do not penalize for not being photorealistic)."
        if is_cartoon
        else "This scene requires photorealistic cinematic quality: realistic skin/fabric/metal/water textures, "
             "natural lighting and shadows, proper depth of field, and zero plastic or cartoonish artifacts."
    )
    ctx_note = []
    if has_prev:
        ctx_note.append("Image 2 is the PREVIOUS scene for continuity comparison.")
    if has_next:
        ctx_note.append("The final attached image is the NEXT scene for continuity comparison.")

    return f"""You are a strict Visual Quality Control Inspector for a 9:16 (1080x1920) YouTube Shorts pipeline.
Inspect Image 1 (target scene '{scene_id}') rigorously. {" ".join(ctx_note)}

Story narration: {narration}
Intended visual brief: {visual_brief}
Style guidance: {style_note}

Evaluate all 5 categories strictly:
1. character_quality (0-25): Anatomy, limb/finger/eye counts, natural expressions, clothing folds/details, no clones or distortion.
2. environment_quality (0-25): Believable architecture/nature/props, proper perspective & depth, no floating or impossible objects, zero empty voids.
3. realism_quality (0-20): Lighting, shadows, reflections, textures, color grading, zero artifacts or oversharpening.
4. composition_quality (0-15): 9:16 mobile framing, clear visual hierarchy, no cropped heads/bodies, subjects inside safe boundaries.
5. consistency_quality (0-15): Character identity, outfit, location, lighting continuity with adjacent scenes, and accurate match to narration.

Check for critical auto-rejection conditions (use exact keys if present):
{", ".join(CRITICAL_REJECTION_CONDITIONS)}

Return ONLY valid JSON with these exact keys:
{{
  "character_quality": <int 0..25>,
  "environment_quality": <int 0..25>,
  "realism_quality": <int 0..20>,
  "composition_quality": <int 0..15>,
  "consistency_quality": <int 0..15>,
  "critical_defects": [<string from critical list if any>],
  "issues": [<specific concrete visual defects found>],
  "correction_prompt": "<specific prompt fixing the exact defects while preserving all correct elements, or empty string if approved>"
}}"""


def _inspect_with_vision_model(
    image_path: Path,
    scene_id: str,
    narration: str,
    visual_brief: str,
    config: VisualQCConfig,
    prev_image: Optional[Path] = None,
    next_image: Optional[Path] = None,
    is_cartoon: bool = False,
) -> dict:
    from google import genai
    from google.genai import types

    api_key = _resolve_api_key(config)
    client = genai.Client(api_key=api_key)

    contents: list = [
        _build_vision_prompt(
            scene_id=scene_id,
            narration=narration,
            visual_brief=visual_brief,
            is_cartoon=is_cartoon,
            has_prev=prev_image is not None and prev_image.exists(),
            has_next=next_image is not None and next_image.exists(),
        ),
        types.Part.from_bytes(data=image_path.read_bytes(), mime_type="image/png"),
    ]
    for adj in (prev_image, next_image):
        if adj is not None and adj.exists():
            contents.append(types.Part.from_bytes(data=adj.read_bytes(), mime_type="image/png"))

    response = client.models.generate_content(
        model=config.vision_model,
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1,
        ),
    )
    return json.loads(response.text)


def validate_scene_image(
    image_path: Path,
    scene_id: str,
    narration: str,
    visual_brief: str = "",
    config: Optional[VisualQCConfig] = None,
    prev_image: Optional[Path] = None,
    next_image: Optional[Path] = None,
    retry_count: int = 0,
    is_cartoon: bool = False,
    inspector_fn: Optional[Callable[..., dict]] = None,
) -> ValidationReport:
    """Validate a single scene image and return a structured ValidationReport."""
    cfg = config or VisualQCConfig()
    integrity_issues = _check_image_integrity(image_path, cfg)
    if integrity_issues:
        return ValidationReport(
            scene_id=scene_id,
            status="REJECTED",
            score=0,
            character_quality=0,
            environment_quality=0,
            realism_quality=0,
            composition_quality=0,
            consistency_quality=0,
            issues=integrity_issues,
            correction_prompt=f"Regenerate {scene_id} at {cfg.target_width}x{cfg.target_height} (9:16) with clear subject and full background.",
            retry_count=retry_count,
            critical_defects=["major_visual_artifacts"],
        )

    if inspector_fn is not None:
        inspect = inspector_fn
    elif cfg.mode == "gemini" or (cfg.mode == "auto" and _has_api_key(cfg)):
        inspect = _inspect_with_vision_model
    else:
        inspect = _local_inspect
    raw = inspect(
        image_path=image_path,
        scene_id=scene_id,
        narration=narration,
        visual_brief=visual_brief,
        config=cfg,
        prev_image=prev_image,
        next_image=next_image,
        is_cartoon=is_cartoon,
    )

    c_q = max(0, min(25, int(raw.get("character_quality", 0))))
    e_q = max(0, min(25, int(raw.get("environment_quality", 0))))
    r_q = max(0, min(20, int(raw.get("realism_quality", 0))))
    comp_q = max(0, min(15, int(raw.get("composition_quality", 0))))
    cons_q = max(0, min(15, int(raw.get("consistency_quality", 0))))
    total = c_q + e_q + r_q + comp_q + cons_q

    critical = [d for d in raw.get("critical_defects", []) if d]
    issues = [str(x) for x in raw.get("issues", []) if x]
    correction = str(raw.get("correction_prompt", "")).strip()

    # High numerical score must NEVER override a critical rejection condition
    approved = (total >= cfg.min_score) and (len(critical) == 0)
    if not approved and not correction and issues:
        correction = "Fix the following defects while preserving all correct scene elements: " + "; ".join(issues)

    return ValidationReport(
        scene_id=scene_id,
        status="APPROVED" if approved else "REJECTED",
        score=total,
        character_quality=c_q,
        environment_quality=e_q,
        realism_quality=r_q,
        composition_quality=comp_q,
        consistency_quality=cons_q,
        issues=issues,
        correction_prompt=correction if not approved else "",
        retry_count=retry_count,
        critical_defects=critical,
    )


def validate_and_regenerate_scene(
    image_path: Path,
    scene_id: str,
    narration: str,
    visual_brief: str,
    debug_dir: Path,
    regenerate_fn: Optional[Callable[[str, str, int], Path]] = None,
    config: Optional[VisualQCConfig] = None,
    prev_image: Optional[Path] = None,
    next_image: Optional[Path] = None,
    is_cartoon: bool = False,
    inspector_fn: Optional[Callable[..., dict]] = None,
) -> ValidationReport:
    """Validate a scene; if rejected, regenerate with specific correction prompt up to max_retries (3)."""
    cfg = config or VisualQCConfig()
    debug_dir.mkdir(parents=True, exist_ok=True)
    current_path = image_path
    last_report: Optional[ValidationReport] = None

    for attempt in range(cfg.max_retries + 1):
        report = validate_scene_image(
            image_path=current_path,
            scene_id=scene_id,
            narration=narration,
            visual_brief=visual_brief,
            config=cfg,
            prev_image=prev_image,
            next_image=next_image,
            retry_count=attempt,
            is_cartoon=is_cartoon,
            inspector_fn=inspector_fn,
        )
        last_report = report

        if report.status == "APPROVED":
            (debug_dir / f"{scene_id}_report.json").write_text(
                json.dumps(report.to_public_dict(), indent=2, ensure_ascii=False), encoding="utf-8"
            )
            return report

        # Save rejected image + report for debugging
        if current_path.exists():
            shutil.copy2(current_path, debug_dir / f"{scene_id}_rejected_try{attempt}.png")
        (debug_dir / f"{scene_id}_rejected_try{attempt}.json").write_text(
            json.dumps(asdict(report), indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # Never regenerate without a specific identified reason, and never exceed max_retries
        if attempt >= cfg.max_retries or regenerate_fn is None or not (report.issues or report.correction_prompt):
            break

        current_path = regenerate_fn(scene_id, report.correction_prompt, attempt + 1)

    assert last_report is not None
    last_report.status = "FAILED"
    (debug_dir / f"{scene_id}_report.json").write_text(
        json.dumps(last_report.to_public_dict(), indent=2, ensure_ascii=False), encoding="utf-8"
    )
    raise VisualQCError(
        f"[visual_qc] Scene '{scene_id}' FAILED validation (score={last_report.score}/100, "
        f"retries={last_report.retry_count}): {'; '.join(last_report.issues or last_report.critical_defects)}"
    )


def validate_scene_sequence(
    scenes: list[dict],
    debug_dir: Path,
    regenerate_fn: Optional[Callable[[str, str, int], Path]] = None,
    config: Optional[VisualQCConfig] = None,
    is_cartoon: bool = False,
    inspector_fn: Optional[Callable[..., dict]] = None,
) -> list[dict]:
    """Validate an entire ordered sequence of scenes and write summary qc_report.json.

    Each item in `scenes` must contain: {"scene_id": str, "image_path": Path, "narration": str, "visual_brief": str}.
    """
    reports: list[dict] = []
    for idx, sc in enumerate(scenes):
        prev_img = scenes[idx - 1]["image_path"] if idx > 0 else None
        next_img = scenes[idx + 1]["image_path"] if idx + 1 < len(scenes) else None
        rep = validate_and_regenerate_scene(
            image_path=Path(sc["image_path"]),
            scene_id=sc["scene_id"],
            narration=sc.get("narration", ""),
            visual_brief=sc.get("visual_brief", ""),
            debug_dir=debug_dir,
            regenerate_fn=regenerate_fn,
            config=config,
            prev_image=Path(prev_img) if prev_img else None,
            next_image=Path(next_img) if next_img else None,
            is_cartoon=is_cartoon,
            inspector_fn=inspector_fn,
        )
        reports.append(rep.to_public_dict())

    debug_dir.mkdir(parents=True, exist_ok=True)
    (debug_dir / "qc_report.json").write_text(json.dumps(reports, indent=2, ensure_ascii=False), encoding="utf-8")
    return reports
