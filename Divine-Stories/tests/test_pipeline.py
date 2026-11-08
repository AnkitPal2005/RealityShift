"""Offline unit tests (no network): python -m pytest -q"""

import copy
import json
import math

import cairo
import numpy as np
import pytest
from PIL import Image

from audio import synth
from audio.mix import resolve_cue
from characters import library as chars
from compositor import captions, text
from config import settings as S
from generators.commons import license_ok, rights_block
from story import schema
from story.templates import TEMPLATES
from visuals import camera, effects, grade

STORY = S.STORY_LIBRARY / "shiva_neelkanth.json"


@pytest.fixture
def story():
    return json.loads(STORY.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- isolation

def test_paths_stay_inside_project():
    for p in (S.ASSETS, S.ASSET_CACHE, S.ASSET_MANIFEST, S.OUTPUT, S.TEMP, S.LOGS, S.STORY_LIBRARY):
        assert S.ROOT in p.resolve().parents or p.resolve() == S.ROOT


def test_no_reality_shift_imports():
    for py in S.ROOT.rglob("*.py"):
        if ".venv" in py.parts:
            continue
        src = py.read_text(encoding="utf-8")
        for bad in ("import engine", "from engine", "RealityShift", "generate_brahmos", "upload_kit", "stories.reality"):
            assert bad not in src or py.name == "test_pipeline.py", f"{py} references Reality Shift ({bad})"


# ---------------------------------------------------------------- story

def test_story_validates(story):
    warns = schema.validate(story)
    assert any("human source review" in w for w in warns)


def test_story_rejects_unsourced_claim(story):
    bad = copy.deepcopy(story)
    bad["scenes"][1]["claims"][0]["sources"] = []
    with pytest.raises(schema.StoryError):
        schema.validate(bad)


def test_story_rejects_bad_claim_kind(story):
    bad = copy.deepcopy(story)
    bad["scenes"][1]["claims"][0]["kind"] = "fact"
    with pytest.raises(schema.StoryError):
        schema.validate(bad)


def test_story_requires_hook_and_question(story):
    bad = copy.deepcopy(story)
    bad["scenes"][0]["beat"] = "setup"
    with pytest.raises(schema.StoryError):
        schema.validate(bad)


def test_templates_have_hook_and_end():
    for name, beats in TEMPLATES.items():
        assert beats[0][0] == "hook" and beats[-1][0] in ("question", "conclusion"), name
        assert 8 <= len(beats) <= 12


def test_popular_belief_is_labelled(story):
    for sc in story["scenes"]:
        if any(c["kind"] == "popular_interpretation" for c in sc.get("claims", [])):
            assert "लोक मान्यता" in sc["label"]


# ---------------------------------------------------------------- licensing

@pytest.mark.parametrize("code,name,ok", [
    ("pd", "Public domain", True), ("cc0", "CC0", True), ("cc-by-4.0", "CC BY 4.0", True), ("cc-by-2.0", "", True),
    ("cc-by-sa-4.0", "CC BY-SA 4.0", False), ("cc-by-nc-2.0", "", False), ("cc-by-nd-3.0", "", False),
    ("gfdl", "GFDL", False), ("", "", False), ("cc-by-sa-3.0,2.5,2.0,1.0", "", False),
])
def test_license_filter(code, name, ok):
    assert license_ok(code, name) is ok


def test_rights_override_dates():
    t = "File:Myths of the Hindus & Buddhists - Shiva drinking the World-Poison.jpg"
    assert rights_block(t, "2026-11-08")
    assert rights_block(t, "2027-01-01") is None
    assert rights_block("File:Shiva drinking Halahala.jpg", "2099-01-01")


def test_character_consistency(story):
    assert chars.check_story(story) == []
    bad = copy.deepcopy(story)
    bad["scenes"][7]["visual"]["asset"] = chars.approved("shiva")["family"]   # close-up with the wrong reference
    assert chars.check_story(bad)


# ---------------------------------------------------------------- text / visuals

def test_devanagari_shaping_forms_conjuncts():
    glyphs, adv, _ = text.shape("क्ष")          # ka + virama + ssa -> one conjunct glyph in Nirmala UI
    assert len(glyphs) == 1 and adv > 0
    glyphs2, _, _ = text.shape("कि")           # i-matra is reordered before ka
    assert len(glyphs2) == 2


def test_text_draws_pixels():
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 400, 120)
    ctx = cairo.Context(surf)
    text.draw(ctx, "नीलकंठ", 200, 60, 60, (1, 1, 1))
    a = np.frombuffer(surf.get_data(), np.uint8)
    assert a.max() > 200


def test_camera_never_leaves_artwork():
    src = Image.new("RGB", (900, 1300), (128, 64, 32))
    shot = camera.Shot(src, (0.02, 0.98), (0.5, -0.5), (1.0, 2.5), 5.0)
    for t in np.linspace(0, 5, 12):
        x0, y0, x1, y1 = shot.rect(t)
        assert x0 >= -1e-6 and y0 >= -1e-6 and x1 <= 900 + 1e-6 and y1 <= 1300 + 1e-6


def test_grades_keep_range():
    im = Image.fromarray((np.random.default_rng(0).random((64, 48, 3)) * 255).astype(np.uint8))
    for g in grade.GRADES:
        a = np.asarray(grade.apply(im, g))
        assert a.shape == (64, 48, 3) and a.std() > 5


def test_effects_draw_without_error():
    src = Image.new("RGB", (1200, 2000), (90, 80, 70))
    shot = camera.Shot(src, (0.5, 0.5), (0, 0), (1.0, 1.2), 4.0)
    env = effects.Env(shot, {"lightning": {"times": [1.0]}, "throat_glow": {"point": [0.5, 0.4]},
                             "energy_wave": {"point": [0.5, 0.4]}, "poison_smoke": {"target": [0.5, 0.4]}},
                      {"energy_wave.at": 0.5}, seed=1)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, S.W, S.H)
    ctx = cairo.Context(surf)
    effects.draw_all(ctx, set(effects.EFFECTS), 1.02, 4.0, env)
    assert np.frombuffer(surf.get_data(), np.uint8).max() > 0


def test_caption_chunks_respect_width_and_order():
    words = [{"w": w, "t": i * 0.3, "d": 0.25} for i, w in enumerate("विष से उनका कंठ नीला हो गया तभी से वे कहलाए नीलकंठ".split())]
    aligned = captions.align_tokens("विष से उनका कंठ नीला हो गया। तभी से वे कहलाए... नीलकंठ।", words)
    ch = captions.chunk(aligned, 5.0)
    assert all(len(c["words"]) <= 4 for c in ch)
    assert [c["start"] for c in ch] == sorted(c["start"] for c in ch)
    # the sentence ends a chunk (break after the danda) and no chunk is a lone word
    assert any(c["words"][-1]["disp"] == "गया।" for c in ch)
    assert all(len(c["words"]) > 1 for c in ch[:-1])


# ---------------------------------------------------------------- audio

def test_sfx_are_finite_and_bounded():
    for k in synth.SFX_KINDS:
        x = synth.sfx(k, 1)
        assert np.isfinite(x).all() and np.abs(x).max() <= 1.0 and len(x) > S.SAMPLE_RATE * 0.5


def test_score_length_and_level():
    tl = [{"start": 0, "dur": 3, "beat": "hook"}, {"start": 3, "dur": 3, "beat": "reveal"}]
    m = synth.score(tl, 6.0)
    assert m.shape == (int(6 * S.SAMPLE_RATE), 2) and np.abs(m).max() <= 0.81


def test_word_cue_resolution():
    tl = {"id": "s", "start": 10.0, "words": [{"w": "नीलकंठ", "t": 12.5}]}
    assert resolve_cue("word:नीलकंठ", tl) == 12.5
    assert resolve_cue(0.5, tl) == 10.5
    with pytest.raises(ValueError):
        resolve_cue("word:शिव", tl)


# ---------------------------------------------------------------- YPP gate

from qc import ypp_gate  # noqa: E402


def _manifest_for(story):
    from generators.commons import load_manifest
    return load_manifest()


def test_ypp_gate_passes_original_story(story):
    problems, _ = ypp_gate.evaluate(story, library={}, history={"order": []}, manifest=_manifest_for(story))
    assert problems == []


def test_ypp_gate_blocks_copied_narration(story):
    twin = copy.deepcopy(story)
    twin["slug"], twin["topic"], twin["title_hi"] = "twin", "other topic", "दूसरा शीर्षक"
    problems, _ = ypp_gate.evaluate(story, library={"twin": twin}, history={"order": []}, manifest=_manifest_for(story))
    assert any("repeats twin" in p for p in problems)


def test_ypp_gate_blocks_duplicate_topic(story):
    other = {"slug": "x", "topic": story["topic"].upper(), "title_hi": "अलग", "scenes": [{"narration": "बिल्कुल अलग कथा"}]}
    problems, _ = ypp_gate.evaluate(story, library={"x": other}, history={"order": []}, manifest=_manifest_for(story))
    assert any("topic duplicates" in p for p in problems)


def test_ypp_gate_blocks_template_run_asset_reuse_and_ending(story):
    end = " ".join(w.strip("।,.?!…").lower() for w in story["scenes"][-1]["narration"].split())
    assets = sorted({s["visual"]["asset"] for s in story["scenes"]})
    hist = {"order": [{"slug": f"p{i}", "template": story["template"], "layout": "classic", "ending": end,
                       "assets": assets} for i in range(3)]}
    problems, _ = ypp_gate.evaluate(story, library={}, history=hist, manifest=_manifest_for(story))
    joined = " | ".join(problems)
    assert "narrative template" in joined and "already used in p0" in joined and "closing question" in joined


def test_ypp_gate_blocks_static_shot_and_off_platform_cta(story):
    bad = copy.deepcopy(story)
    bad["scenes"][2]["visual"].update(zoom=[1.1, 1.12], pan=[0, 0])
    bad["scenes"][3]["visual"]["effects"] = []
    bad["scenes"][-1]["narration"] += " लिंक इन बायो।"
    problems, _ = ypp_gate.evaluate(bad, library={}, history={"order": []}, manifest=_manifest_for(story))
    joined = " | ".join(problems)
    assert "static shot" in joined and "no atmosphere" in joined and "off-platform" in joined


def test_ypp_gate_blocks_unlicensed_asset(story):
    problems, _ = ypp_gate.evaluate(story, library={}, history={"order": []}, manifest={})
    assert any("not downloaded/approved" in p for p in problems)
