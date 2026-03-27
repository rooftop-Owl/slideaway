#!/usr/bin/env python3
"""Convert PDF pages to individual images using PyMuPDF.

Usage:
    python3 pdf_to_images.py presentation.pdf output/slide --dpi 150 --format png
    python3 pdf_to_images.py thesis.pdf slides/ --first 5 --last 10 --dpi 200

DPI guide:
    150 = screen review (default, fast)
    200 = detailed inspection
    300 = print quality

Requires: pip install pymupdf  (part of slideaway[qa])
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _import_fitz():
    """Import fitz with a graceful error message if missing."""
    try:
        import fitz  # noqa: F811

        return fitz
    except ImportError:
        print(
            "ERROR: PyMuPDF (fitz) is not installed.\n"
            "Install it with: pip install pymupdf\n"
            "Or install all QA dependencies: pip install slideaway[qa]",
            file=sys.stderr,
        )
        sys.exit(1)


def pdf_to_images(
    pdf_path: str | Path,
    output_prefix: str | Path = "slide",
    *,
    dpi: int = 150,
    fmt: str = "png",
    first: int | None = None,
    last: int | None = None,
    quiet: bool = False,
) -> list[Path]:
    """Convert PDF pages to individual image files.

    Args:
        pdf_path: Path to the PDF file.
        output_prefix: Output path prefix. Files are named {prefix}-001.{fmt}.
        dpi: Resolution in dots per inch (150=screen, 200=detail, 300=print).
        fmt: Image format ('png' or 'jpg').
        first: First page to convert (1-indexed, inclusive). None = page 1.
        last: Last page to convert (1-indexed, inclusive). None = last page.
        quiet: Suppress progress messages.

    Returns:
        List of output file paths.
    """
    fitz = _import_fitz()

    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        print(f"ERROR: PDF file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    output_prefix = Path(output_prefix)
    output_prefix.parent.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    total_pages = len(doc)

    # Resolve page range (1-indexed input → 0-indexed internal)
    start = max(0, (first or 1) - 1)
    end = min(total_pages, last or total_pages)

    if start >= end:
        print(f"ERROR: Invalid page range: first={first}, last={last}, total={total_pages}", file=sys.stderr)
        sys.exit(1)

    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)

    output_files: list[Path] = []
    for page_idx in range(start, end):
        page = doc[page_idx]
        pix = page.get_pixmap(matrix=matrix)

        page_num = page_idx + 1
        out_path = Path(f"{output_prefix}-{page_num:03d}.{fmt}")

        if fmt == "jpg":
            pix.save(str(out_path), output="jpeg")
        else:
            pix.save(str(out_path))

        output_files.append(out_path)

        if not quiet:
            print(f"  Page {page_num}/{total_pages} → {out_path}")

    doc.close()

    if not quiet:
        print(f"\nConverted {len(output_files)} pages from {pdf_path.name} at {dpi} DPI")

    return output_files


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="pdf_to_images",
        description="Convert PDF pages to individual images (PyMuPDF). PPTX-only limitation: this tool handles PDFs. For PPTX validation, use validate_pptx.py.",
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument(
        "output_prefix",
        nargs="?",
        default="slide",
        help="Output path prefix (default: 'slide' → slide-001.png, slide-002.png, ...)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=150,
        help="Resolution: 150=screen (default), 200=detail, 300=print",
    )
    parser.add_argument(
        "--format",
        dest="fmt",
        choices=["png", "jpg"],
        default="png",
        help="Output image format (default: png)",
    )
    parser.add_argument(
        "--first",
        type=int,
        default=None,
        help="First page to convert (1-indexed, inclusive)",
    )
    parser.add_argument(
        "--last",
        type=int,
        default=None,
        help="Last page to convert (1-indexed, inclusive)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress messages",
    )

    args = parser.parse_args()

    pdf_to_images(
        args.pdf_path,
        args.output_prefix,
        dpi=args.dpi,
        fmt=args.fmt,
        first=args.first,
        last=args.last,
        quiet=args.quiet,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
