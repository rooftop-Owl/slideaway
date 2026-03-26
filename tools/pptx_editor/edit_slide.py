#!/usr/bin/env python3
"""Edit slide XML files extracted from a PPTX archive.

Supports two kinds of edits:

* **Text substitution** – find a text string and replace it with another.
* **Color substitution** – find a hex colour value (e.g. ``FF0000``) and
  replace it with another, affecting ``<a:srgbClr>`` and ``<a:sysClr>``
  element ``val`` attributes across the full OOXML namespace graph.

OOXML (the format used by PPTX) uses XML namespaces extensively.  This
module registers the common namespace prefixes so that the serialised output
preserves the original namespace declarations.

Example usage::

    from modules.slides.tools.pptx_editor import edit_slide_xml

    # Replace text in a slide
    edit_slide_xml("slide1.xml", find="Draft", replace="Final")

    # Replace a colour swatch
    edit_slide_xml("slide1.xml", find="1A3A5C", replace="2E86AB",
                   mode="color")

CLI::

    python3 edit_slide.py ppt/slides/slide1.xml --find "Draft" --replace "Final"
    python3 edit_slide.py ppt/slides/slide1.xml --color-find FF0000 --color-replace 00FF00
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# ---------------------------------------------------------------------------
# OOXML namespace map — register so ET serialises them with their short prefix
# ---------------------------------------------------------------------------
_NAMESPACES: dict[str, str] = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "xdr": "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "v": "urn:schemas-microsoft-com:vml",
    "o": "urn:schemas-microsoft-com:office:office",
    "p14": "http://schemas.microsoft.com/office/powerpoint/2010/main",
}

for _prefix, _uri in _NAMESPACES.items():
    ET.register_namespace(_prefix, _uri)


def _load_tree(xml_path: str) -> tuple[ET.ElementTree, ET.Element]:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    return tree, root


def _text_replace(root: ET.Element, find: str, replace: str) -> int:
    """Replace all occurrences of *find* in element text and tail.

    Returns the number of replacements made.
    """
    count = 0
    for elem in root.iter():
        if elem.text and find in elem.text:
            elem.text = elem.text.replace(find, replace)
            count += 1
        if elem.tail and find in elem.tail:
            elem.tail = elem.tail.replace(find, replace)
            count += 1
    return count


def _color_replace(root: ET.Element, find_hex: str, replace_hex: str) -> int:
    """Replace colour hex values in ``val`` attributes of colour elements.

    Targets ``<a:srgbClr val="...">`` and ``<a:sysClr val="...">`` throughout
    the element tree.  The comparison is case-insensitive; the replacement
    value is stored in the original case as supplied.

    Returns the number of attribute replacements made.
    """
    find_upper = find_hex.upper()
    count = 0
    color_tags = {
        f"{{{_NAMESPACES['a']}}}srgbClr",
        f"{{{_NAMESPACES['a']}}}sysClr",
    }
    for elem in root.iter():
        if elem.tag in color_tags:
            val = elem.get("val", "")
            if val.upper() == find_upper:
                elem.set("val", replace_hex)
                count += 1
    return count


def edit_slide_xml(
    xml_path: str,
    find: str,
    replace: str,
    mode: str = "text",
) -> None:
    """Modify a slide XML file in-place.

    Args:
        xml_path: Path to the slide XML file (e.g. ``ppt/slides/slide1.xml``).
        find: The string (text mode) or hex colour (color mode) to search for.
        replace: Replacement string or hex colour.
        mode: Either ``"text"`` (default) or ``"color"``.

    Raises:
        FileNotFoundError: If *xml_path* does not exist.
        ValueError: If *mode* is not ``"text"`` or ``"color"``.

    Example::

        edit_slide_xml("ppt/slides/slide1.xml", find="TODO", replace="Done")
        edit_slide_xml("ppt/slides/slide1.xml",
                       find="FF0000", replace="1A3A5C", mode="color")
    """
    path = Path(xml_path)
    if not path.exists():
        raise FileNotFoundError(f"XML file not found: {xml_path}")

    if mode not in {"text", "color"}:
        raise ValueError(f"mode must be 'text' or 'color', got: {mode!r}")

    tree, root = _load_tree(xml_path)

    if mode == "text":
        _text_replace(root, find, replace)
    else:
        _color_replace(root, find, replace)

    tree.write(xml_path, encoding="UTF-8", xml_declaration=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="edit_slide",
        description="Modify a slide XML file — text or colour substitution.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  # Replace text\n"
            "  python3 edit_slide.py ppt/slides/slide1.xml \\\n"
            "      --find 'Draft Title' --replace 'Final Title'\n"
            "\n"
            "  # Replace a colour (hex, no leading #)\n"
            "  python3 edit_slide.py ppt/slides/slide1.xml \\\n"
            "      --color-find FF0000 --color-replace 1A3A5C\n"
            "\n"
            "  Unpack first with unpack.py, then repack with pack.py."
        ),
    )
    parser.add_argument("xml_path", help="Path to the slide XML file")

    text_grp = parser.add_argument_group("text substitution")
    text_grp.add_argument("--find", metavar="TEXT", help="Text string to find")
    text_grp.add_argument("--replace", metavar="TEXT", help="Replacement text string")

    color_grp = parser.add_argument_group("colour substitution")
    color_grp.add_argument("--color-find", metavar="HEX", help="Hex colour to find (e.g. FF0000)")
    color_grp.add_argument("--color-replace", metavar="HEX", help="Replacement hex colour (e.g. 1A3A5C)")

    args = parser.parse_args()

    # Determine mode from provided arguments
    if args.color_find or args.color_replace:
        if not (args.color_find and args.color_replace):
            parser.error("--color-find and --color-replace must be used together")
        mode = "color"
        find_val = args.color_find
        replace_val = args.color_replace
    elif args.find or args.replace:
        if not (args.find and args.replace):
            parser.error("--find and --replace must be used together")
        mode = "text"
        find_val = args.find
        replace_val = args.replace
    else:
        parser.error("Provide either (--find + --replace) or (--color-find + --color-replace)")

    try:
        edit_slide_xml(args.xml_path, find=find_val, replace=replace_val, mode=mode)
        print(f"Edited '{args.xml_path}': replaced {mode} '{find_val}' → '{replace_val}'")
        return 0
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
