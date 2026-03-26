#!/usr/bin/env python3

from __future__ import annotations

import argparse
import glob
import math
import sys
from pathlib import Path
from typing import cast

pil_import_error: ImportError | None = None
try:
    from PIL import Image
except ImportError as exc:
    Image = None
    pil_import_error = exc


def parse_thumb_size(value: str) -> tuple[int, int]:
    try:
        width_str, height_str = value.lower().split("x", 1)
        width = int(width_str)
        height = int(height_str)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("--thumb-size must be in WIDTHxHEIGHT format (e.g. 480x270)") from exc

    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("--thumb-size values must be positive integers")

    return width, height


def expand_input_paths(patterns: list[str]) -> list[Path]:
    expanded: list[Path] = []
    for pattern in patterns:
        matches = sorted(glob.glob(pattern))
        if matches:
            expanded.extend(Path(match) for match in matches)
        else:
            expanded.append(Path(pattern))

    png_paths = [path for path in expanded if path.suffix.lower() == ".png" and path.exists()]
    unique_paths = sorted(set(png_paths), key=lambda path: str(path))
    return unique_paths


def build_thumbnail_grid(
    input_paths: list[Path],
    output_path: Path,
    columns: int,
    thumb_size: tuple[int, int],
) -> None:
    if Image is None:
        raise RuntimeError("Pillow is not installed. Install it with: pip install Pillow") from pil_import_error

    thumb_width, thumb_height = thumb_size
    rows = math.ceil(len(input_paths) / columns)

    canvas = Image.new("RGB", (columns * thumb_width, rows * thumb_height), color=(255, 255, 255))

    for index, input_path in enumerate(input_paths):
        with Image.open(input_path) as image:
            thumbnail = image.convert("RGB").resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)

        x = (index % columns) * thumb_width
        y = (index // columns) * thumb_height
        canvas.paste(thumbnail, (x, y))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="thumbnail_grid",
        description="Create a thumbnail grid overview from PNG slide screenshots.",
    )
    _ = parser.add_argument(
        "inputs",
        nargs="+",
        help="Input PNG paths and/or glob patterns (e.g. 'shots/*.png').",
    )
    _ = parser.add_argument(
        "--output",
        required=True,
        help="Output image path for the generated thumbnail grid PNG.",
    )
    _ = parser.add_argument(
        "--columns",
        type=int,
        default=4,
        help="Number of columns in the output grid (default: 4).",
    )
    _ = parser.add_argument(
        "--thumb-size",
        type=parse_thumb_size,
        default=(480, 270),
        metavar="WIDTHxHEIGHT",
        help="Thumbnail size for each image (default: 480x270).",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    columns = cast(int, args.columns)
    output = cast(str, args.output)
    thumb_size = cast(tuple[int, int], args.thumb_size)
    inputs = cast(list[str], args.inputs)

    if columns <= 0:
        parser.error("--columns must be a positive integer")

    input_paths = expand_input_paths(inputs)
    if not input_paths:
        parser.error("No existing PNG files found from provided inputs/globs")

    try:
        build_thumbnail_grid(
            input_paths=input_paths,
            output_path=Path(output),
            columns=columns,
            thumb_size=thumb_size,
        )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Saved thumbnail grid: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
