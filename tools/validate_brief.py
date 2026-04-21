#!/usr/bin/env python3
"""validate_brief.py — Machine-checkable validator for Slide Brief JSON files.

Validates against slide-brief.schema.json plus semantic rules that JSON Schema
cannot express (time-block sums, slide-range bounds, cross-field constraints).

Exit codes:
  0  Valid — no failures, no warnings
  1  Warnings only (non-blocking)
  2  One or more hard failures

Hard failures (exit 2):
  F1  JSON parse error or missing required field
  F2  Invalid enum value
  F3  schema_version mismatch
  F5  time_blocks minutes do not sum to duration_minutes (±1 min tolerance)
  F6  A slide_range upper bound exceeds slide_count_target + 2

Warnings (exit 1):
  W1  attention_budget=low with duration > 30 min
  W2  talk_type=lightning with duration > 5 min
  W3  talk_type=tutorial with no source_material entries
  W4  anti_slop_verified is false or absent (not yet confirmed at Phase 0f)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_json(path: str) -> tuple[dict | None, str | None]:
    """Return (parsed_dict, None) or (None, error_message)."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f), None
    except FileNotFoundError:
        return None, f"file not found: {path}"
    except json.JSONDecodeError as e:
        return None, f"JSON parse error: {e}"


def _validate_schema(brief: dict) -> list[str]:
    """Run jsonschema validation if available; fall back to manual required-field check."""
    failures: list[str] = []

    schema_path = (
        Path(__file__).resolve().parents[1]
        / "skills"
        / "slide-generation"
        / "references"
        / "slide-brief.schema.json"
    )

    if schema_path.exists():
        try:
            import jsonschema  # type: ignore[import]
        except ImportError:
            pass  # fall through to manual check
        else:
            try:
                with open(schema_path, encoding="utf-8") as f:
                    schema = json.load(f)
                validator = jsonschema.Draft7Validator(schema)
                for error in sorted(
                    validator.iter_errors(brief),
                    key=lambda e: ".".join(str(p) for p in e.path),
                ):
                    path = ".".join(str(p) for p in error.path) or "<root>"
                    failures.append(f"F2 schema: {path}: {error.message}")
                return failures
            except Exception as e:
                failures.append(f"F1 schema validation error: {e}")
                return failures

    # Manual required-field check when jsonschema is unavailable
    required_top = ["schema_version", "audience", "purpose", "structure", "style", "delivery"]
    for field in required_top:
        if field not in brief:
            failures.append(f"F1 missing required field: {field}")

    if "audience" in brief:
        for f in ["current_state", "desired_state", "quadrant", "attention_budget"]:
            if f not in brief["audience"]:
                failures.append(f"F1 missing required field: audience.{f}")

    if "purpose" in brief:
        for f in ["the_one_thing", "the_ask", "talk_type"]:
            if f not in brief["purpose"]:
                failures.append(f"F1 missing required field: purpose.{f}")

    if "structure" in brief:
        for f in ["duration_minutes", "slide_count_target", "narrative_arc", "time_blocks"]:
            if f not in brief["structure"]:
                failures.append(f"F1 missing required field: structure.{f}")

    if "style" in brief:
        for f in ["preset", "engine", "anti_slop_verified"]:
            if f not in brief["style"]:
                failures.append(f"F1 missing required field: style.{f}")

    if "delivery" in brief:
        if "medium" not in brief["delivery"]:
            failures.append("F1 missing required field: delivery.medium")

    return failures


def _check_semantic_failures(brief: dict) -> list[str]:
    """Semantic rules that JSON Schema cannot express."""
    failures: list[str] = []

    # F3: schema_version — only fires when key is present; absence is already F1
    if "schema_version" in brief:
        sv = brief["schema_version"]
        if sv != "slide-brief/1.0":
            failures.append(f"F3 schema_version must be 'slide-brief/1.0', got: '{sv}'")

    structure = brief.get("structure", {})
    duration = structure.get("duration_minutes")
    slide_count = structure.get("slide_count_target")
    time_blocks = structure.get("time_blocks", [])

    # F5: time_blocks sum — skip if duration is non-numeric (e.g. extractor wrote 0 for unknown)
    if (
        duration is not None
        and isinstance(duration, (int, float))
        and duration > 0
        and isinstance(time_blocks, list)
        and time_blocks
    ):
        total = sum(b.get("minutes", 0) for b in time_blocks if isinstance(b, dict))
        if abs(total - duration) > 1:
            failures.append(
                f"F5 time_blocks sum ({total:.1f} min) does not match "
                f"duration_minutes ({duration} min) — difference {abs(total - duration):.1f} min exceeds 1-min tolerance"
            )

    # F6: slide_range upper bound — skip if slide_count is non-integer
    if (
        slide_count is not None
        and isinstance(slide_count, int)
        and slide_count > 0
        and isinstance(time_blocks, list)
    ):
        limit = slide_count + 2
        for i, block in enumerate(time_blocks):
            if not isinstance(block, dict):
                continue
            sr = block.get("slide_range")
            if sr is None or not isinstance(sr, list) or len(sr) < 2:
                continue
            upper = sr[1]
            if isinstance(upper, int) and upper > limit:
                section = block.get("section", f"block {i}")
                failures.append(
                    f"F6 slide_range upper bound {upper} in '{section}' exceeds "
                    f"slide_count_target + 2 = {limit}"
                )

    return failures


def _check_warnings(brief: dict) -> list[str]:
    """Cross-field warnings — non-blocking."""
    warnings: list[str] = []

    audience = brief.get("audience", {})
    purpose = brief.get("purpose", {})
    structure = brief.get("structure", {})
    constraints = brief.get("constraints", {})

    attention = audience.get("attention_budget")
    duration = structure.get("duration_minutes", 0)
    talk_type = purpose.get("talk_type")

    # W1: low attention + long talk
    if attention == "low" and isinstance(duration, (int, float)) and duration > 30:
        warnings.append(
            f"W1 attention_budget=low with duration={duration} min — "
            "audience calibration mismatch: a low-attention audience is unlikely to stay engaged for 30+ minutes"
        )

    # W2: lightning talk too long
    if talk_type == "lightning" and isinstance(duration, (int, float)) and duration > 5:
        warnings.append(
            f"W2 talk_type=lightning with duration={duration} min — "
            "lightning talks conventionally run ≤5 min"
        )

    # W3: tutorial with no source material
    if talk_type == "tutorial":
        source_material = constraints.get("source_material", [])
        if not source_material:
            warnings.append(
                "W3 talk_type=tutorial with no constraints.source_material — "
                "tutorial decks should reference the material they teach"
            )

    # W4: anti_slop_verified not confirmed — extractors always write false; human confirms at 0f
    if "style" in brief and not brief["style"].get("anti_slop_verified", False):
        warnings.append(
            "W4 style.anti_slop_verified is false — the style preset has not been confirmed "
            "at the Phase 0f approval gate; slide-coach must verify before generation"
        )

    return warnings


def validate_brief(brief_path: str) -> tuple[list[str], list[str]]:
    """Return (failures, warnings). Caller should exit 2 on failures, 1 on warnings-only."""
    brief, parse_error = _load_json(brief_path)
    if parse_error or brief is None:
        return [f"F1 {parse_error or 'unknown parse error'}"], []

    failures: list[str] = []
    failures.extend(_validate_schema(brief))
    failures.extend(_check_semantic_failures(brief))

    warnings = _check_warnings(brief)
    return failures, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="validate_brief",
        description="Validate a Slide Brief JSON file against the slide-brief/1.0 schema.",
    )
    parser.add_argument("brief_path", help="Path to brief .json file")
    parser.add_argument(
        "--quiet", action="store_true",
        help="Suppress passing output; still prints failures to stderr",
    )
    args = parser.parse_args()

    try:
        failures, warnings = validate_brief(args.brief_path)
    except Exception as e:
        print(f"validate_brief: unexpected error: {e}", file=sys.stderr)
        return 2

    for w in warnings:
        print(f"WARN {w}")

    for f in failures:
        print(f"FAIL {f}", file=sys.stderr)

    if not failures and not warnings and not args.quiet:
        print(f"✓ validate_brief: {args.brief_path} is valid")

    if failures:
        return 2
    if warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
