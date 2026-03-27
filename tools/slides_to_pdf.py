#!/usr/bin/env python3
"""Combine slide images into a single PDF handout using Pillow.

Usage:
    python3 slides_to_pdf.py slides/*.png -o handout.pdf --dpi 150
    python3 slides_to_pdf.py output/ -o combined.pdf -v
    python3 slides_to_pdf.py slide-001.png slide-002.png slide-003.png -o deck.pdf

Supports: PNG, JPG, JPEG, BMP, TIFF input. RGBA images auto-converted to RGB.

Requires: pip install Pillow  (part of slideaway[qa])
"""

from __future__ import annotations

import argparse
import glob
import sys
from pathlib import Path


def _import_pillow():
    """Import PIL with a graceful error message if missing."""
    try:
        from PIL import Image  # noqa: F811

        return Image
    except ImportError:
        print(
            "ERROR: Pillow (PIL) is not installed.\n"
            "Install it with: pip install Pillow\n"
            "Or install all QA dependencies: pip install slideaway[qa]",
            file=sys.stderr,
        )
        sys.exit(1)


SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"}


def _collect_images(inputs: list[str]) -> list[Path]:
    """Resolve inputs to a sorted list of image file paths.

    Accepts: explicit file paths, glob patterns, or directory paths.
    """
    paths: list[Path] = []
    for inp in inputs:
        p = Path(inp)
        if p.is_dir():
            # Collect all supported images from directory
            for ext in SUPPORTED_EXTENSIONS:
                paths.extend(p.glob(f"*{ext}"))
        elif "*" in inp or "?" in inp:
            # Glob pattern
            paths.extend(Path(g) for g in glob.glob(inp))
        elif p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS:
            paths.append(p)
        else:
            print(f"WARNING: Skipping unsupported or missing file: {inp}", file=sys.stderr)

    # Sort by name for consistent ordering
    return sorted(set(paths), key=lambda x: x.name)


def slides_to_pdf(
    inputs: list[str],
    output: str | Path = "handout.pdf",
    *,
    dpi: int = 150,
    verbose: bool = False,
) -> Path:
    """Combine image files into a single PDF.

    Args:
        inputs: List of file paths, glob patterns, or directories.
        output: Output PDF path.
        dpi: Resolution metadata for the PDF (default: 150).
        verbose: Print progress for each image.

    Returns:
        Path to the generated PDF.
    """
    Image = _import_pillow()

    image_paths = _collect_images(inputs)
    if not image_paths:
        print("ERROR: No valid image files found.", file=sys.stderr)
        sys.exit(1)

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    # Load and convert all images to RGB (PDF doesn't support RGBA)
    images = []
    for img_path in image_paths:
        img = Image.open(img_path)
        if img.mode == "RGBA":
            # Composite onto white background
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg
        elif img.mode != "RGB":
            img = img.convert("RGB")
        images.append(img)

        if verbose:
            print(f"  Added: {img_path.name} ({img.size[0]}×{img.size[1]})")

    # Save as multi-page PDF
    if len(images) == 1:
        images[0].save(str(output), "PDF", resolution=dpi)
    else:
        images[0].save(
            str(output),
            "PDF",
            resolution=dpi,
            save_all=True,
            append_images=images[1:],
        )

    # Always show the summary regardless of verbose flag
    print(f"\nCombined {len(images)} images \u2192 {output} ({dpi} DPI)")

    return output


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="slides_to_pdf",
        description="Combine slide images (PNG/JPG) into a single PDF handout (Pillow).",
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Image files, glob patterns, or directories to combine",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="handout.pdf",
        help="Output PDF path (default: handout.pdf)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=150,
        help="PDF resolution metadata (default: 150)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print progress for each image",
    )

    args = parser.parse_args()

    slides_to_pdf(
        args.inputs,
        args.output,
        dpi=args.dpi,
        verbose=args.verbose,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
