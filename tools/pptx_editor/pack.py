#!/usr/bin/env python3
"""Repack an unpacked PPTX directory back into a ``.pptx`` file.

A PPTX is a ZIP archive.  After editing the raw XML files produced by
:func:`unpack_pptx`, use this module to repack them into a valid PPTX.

File ordering matters for OOXML compliance: ``[Content_Types].xml`` must be
the first entry in the archive, followed by ``_rels/.rels``.  This module
sorts entries to respect that convention.

Example usage::

    from modules.slides.tools.pptx_editor import pack_pptx
    pack_pptx("/tmp/deck_unpacked", "deck_edited.pptx")

CLI::

    python3 pack.py /tmp/deck_unpacked/ deck_edited.pptx
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path


def _sort_key(rel_path: str) -> tuple[int, str]:
    """Return a sort key that places OOXML-required entries first.

    Order:
      0 – ``[Content_Types].xml``
      1 – ``_rels/.rels``
      2 – everything else (alphabetical)
    """
    if rel_path == "[Content_Types].xml":
        return (0, rel_path)
    if rel_path == "_rels/.rels":
        return (1, rel_path)
    return (2, rel_path)


def pack_pptx(input_dir: str, output_path: str) -> None:
    """Repack a directory of OOXML files into a ``.pptx`` archive.

    Args:
        input_dir: Directory produced by :func:`unpack_pptx`.
        output_path: Destination path for the new ``.pptx`` file.  Parent
            directories are created if they do not exist.

    Raises:
        FileNotFoundError: If *input_dir* does not exist or is not a directory.
        FileNotFoundError: If ``[Content_Types].xml`` is missing from
            *input_dir* (not a valid unpacked PPTX).

    Example::

        pack_pptx("/tmp/deck_unpacked", "/tmp/deck_repacked.pptx")
    """
    src = Path(input_dir)
    if not src.exists() or not src.is_dir():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    content_types = src / "[Content_Types].xml"
    if not content_types.exists():
        raise FileNotFoundError(
            f"[Content_Types].xml not found in '{input_dir}'. Is this a valid unpacked PPTX directory?"
        )

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Collect all files relative to the input directory
    all_files: list[Path] = [p for p in src.rglob("*") if p.is_file()]
    rel_paths: list[str] = [str(p.relative_to(src)) for p in all_files]

    # Sort with OOXML-required ordering
    sorted_pairs = sorted(zip(rel_paths, all_files), key=lambda pair: _sort_key(pair[0]))

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel_path, abs_path in sorted_pairs:
            zf.write(abs_path, arcname=rel_path)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="pack",
        description="Repack an unpacked PPTX directory back into a .pptx file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Example:\n"
            "  python3 pack.py /tmp/deck_unpacked/ deck_edited.pptx\n"
            "\n"
            "Unpack first with unpack.py, edit the XML files, then repack here.\n"
            "Use validate.py afterwards to confirm the result is well-formed."
        ),
    )
    parser.add_argument("input_dir", help="Directory of unpacked PPTX files (from unpack.py)")
    parser.add_argument("output_path", help="Destination .pptx file path")
    args = parser.parse_args()

    try:
        pack_pptx(args.input_dir, args.output_path)
        print(f"Packed '{args.input_dir}' → '{args.output_path}'")
        return 0
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
