#!/usr/bin/env python3
"""Unpack a PPTX file into a directory of raw XML files.

A PPTX is a ZIP archive. This module extracts every member so that
individual slide XML files (e.g. ``ppt/slides/slide1.xml``) can be
inspected or edited with a text editor or :mod:`edit_slide`.

Example usage::

    from modules.slides.tools.pptx_editor import unpack_pptx
    unpack_pptx("deck.pptx", "/tmp/deck_unpacked")

CLI::

    python3 unpack.py deck.pptx /tmp/deck_unpacked/
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path


def unpack_pptx(pptx_path: str, output_dir: str) -> None:
    """Extract all files from a PPTX archive into *output_dir*.

    Args:
        pptx_path: Path to the source ``.pptx`` file.
        output_dir: Destination directory.  Created if it does not exist.

    Raises:
        FileNotFoundError: If *pptx_path* does not exist.
        zipfile.BadZipFile: If *pptx_path* is not a valid ZIP/PPTX file.

    Example::

        unpack_pptx("presentation.pptx", "/tmp/unpacked")
        # /tmp/unpacked/ppt/slides/slide1.xml  ← editable XML
    """
    src = Path(pptx_path)
    if not src.exists():
        raise FileNotFoundError(f"PPTX not found: {pptx_path}")

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(src, "r") as zf:
        zf.extractall(out)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="unpack",
        description="Extract a PPTX file into a directory of raw XML files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Example:\n"
            "  python3 unpack.py deck.pptx /tmp/deck_unpacked/\n"
            "\n"
            "After unpacking, slide XML files are at:\n"
            "  <output_dir>/ppt/slides/slide1.xml\n"
            "  <output_dir>/ppt/slides/slide2.xml  ...\n"
            "\n"
            "Use pack.py to repack the directory back into a PPTX."
        ),
    )
    parser.add_argument("pptx_path", help="Path to the source .pptx file")
    parser.add_argument("output_dir", help="Destination directory for extracted files")
    args = parser.parse_args()

    try:
        unpack_pptx(args.pptx_path, args.output_dir)
        print(f"Unpacked '{args.pptx_path}' → '{args.output_dir}'")
        return 0
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except zipfile.BadZipFile as exc:
        print(f"ERROR: Not a valid PPTX/ZIP file — {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
