"""html2pptx — optional HTML-to-PPTX converter via Puppeteer.

Requires Node.js and Puppeteer (npm).  If they are not installed, importing
this package succeeds but calling ``convert()`` raises ``ImportError`` with
installation instructions.

Typical usage
-------------
>>> from modules.slides.tools.html2pptx import convert
>>> convert("slides/index.html", "output/deck.pptx")

Install Node.js dependencies
-----------------------------
    npm install -g puppeteer
    # or locally inside your project:
    npm install puppeteer
"""

from __future__ import annotations

try:
    from .converter import convert

    __all__ = ["convert"]

except ImportError as _import_error:
    # Node.js, Puppeteer, or python-pptx not available.
    # Expose a stub so that `from modules.slides.tools.html2pptx import convert`
    # always succeeds; the error surfaces only when the function is called.

    def convert(*args: object, **kwargs: object) -> None:  # type: ignore[misc]
        """Stub that raises ImportError when dependencies are missing."""
        raise ImportError(
            "html2pptx requires Node.js and Puppeteer (and python-pptx). "
            "Install Node.js from https://nodejs.org/ and then run: "
            "  npm install -g puppeteer\n"
            f"Original error: {_import_error}"
        )

    __all__ = ["convert"]
