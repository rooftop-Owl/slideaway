"""Backward compatibility regression tests for the slides module.

These tests verify that the public API surface of the slides module remains
stable across refactors and additions.  No external tools (Marp, pandoc,
pdflatex) are required — only python-pptx, which is a declared dependency.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# Ensure the worktree root is on sys.path so that `modules.slides.*` imports work
# regardless of where pytest is invoked from.
_MODULE_ROOT = Path(__file__).resolve().parents[3]  # .worktrees/slides-plugin-expansion/
if str(_MODULE_ROOT) not in sys.path:
    sys.path.insert(0, str(_MODULE_ROOT))

_SLIDES_ROOT = Path(__file__).resolve().parents[1]  # modules/slides/


# ---------------------------------------------------------------------------
# 1. Import surface
# ---------------------------------------------------------------------------


def test_slide_factory_import():
    """SlideFactory and STYLE_PRESETS must be importable from slide_factory."""
    from modules.slides.tools.slide_factory import STYLE_PRESETS, SlideFactory  # noqa: F401

    assert SlideFactory is not None, "SlideFactory should be a class"
    assert STYLE_PRESETS is not None, "STYLE_PRESETS should be a dict"


def test_validate_pptx_import():
    """validate_pptx_structure must be importable from validate_pptx and be callable."""
    from modules.slides.tools.validate_pptx import validate_pptx_structure  # noqa: F401

    assert callable(validate_pptx_structure), "validate_pptx_structure must be callable"


# ---------------------------------------------------------------------------
# 2. Style presets count
# ---------------------------------------------------------------------------


def test_style_presets_count():
    """STYLE_PRESETS must contain at least the original 10 presets."""
    from modules.slides.tools.slide_factory import STYLE_PRESETS

    assert len(STYLE_PRESETS) >= 10, (
        f"Expected at least 10 style presets, found {len(STYLE_PRESETS)}: {sorted(STYLE_PRESETS.keys())}"
    )


# ---------------------------------------------------------------------------
# 3. SlideFactory instantiation with all original presets
# ---------------------------------------------------------------------------

_ORIGINAL_PRESETS = [
    "corporate",
    "academic",
    "creative",
    "minimalist",
    "bold",
    "elegant",
    "tech",
    "warm",
    "dark",
    "nature",
]


@pytest.mark.parametrize("preset_name", _ORIGINAL_PRESETS)
def test_slide_factory_instantiation(preset_name: str):
    """SlideFactory must instantiate without errors for each of the 10 original presets."""
    from modules.slides.tools.slide_factory import SlideFactory, Theme

    theme = Theme.from_style(preset_name)
    factory = SlideFactory(theme=theme)
    assert factory is not None, f"SlideFactory with preset '{preset_name}' should not be None"


# ---------------------------------------------------------------------------
# 4. Progressive disclosure reference files
# ---------------------------------------------------------------------------

_REFERENCE_FILES = [
    "design-principles.md",
    "engine-beamer.md",
    "engine-html.md",
    "engine-marp.md",
    "engine-md2pptx.md",
    "engine-pptx.md",
    "engine-revealjs.md",
    "poster-design.md",
    "validation-patterns.md",
]


def test_progressive_disclosure_files():
    """All 9 reference files must exist under skills/slide-generation/references/."""
    references_dir = _SLIDES_ROOT / "skills" / "slide-generation" / "references"
    missing = [f for f in _REFERENCE_FILES if not (references_dir / f).exists()]
    assert not missing, f"Missing reference files in {references_dir}: {missing}"


# ---------------------------------------------------------------------------
# 5. Manifests are valid JSON
# ---------------------------------------------------------------------------


def test_manifests_parseable():
    """Both module.json and .claude-plugin/plugin.json must parse as valid JSON."""
    manifests = [
        _SLIDES_ROOT / "module.json",
        _SLIDES_ROOT / ".claude-plugin" / "plugin.json",
    ]
    for manifest_path in manifests:
        assert manifest_path.exists(), f"Manifest not found: {manifest_path}"
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            pytest.fail(f"Invalid JSON in {manifest_path}: {exc}")
        assert isinstance(data, dict), f"Expected a JSON object in {manifest_path}"
