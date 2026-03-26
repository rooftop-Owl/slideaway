#!/usr/bin/env python3
"""HTML-to-image renderer via Puppeteer subprocess.

Renders an HTML file to a PNG image using Node.js + Puppeteer.
Node.js and Puppeteer are OPTIONAL — raises ImportError if not found.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

# Inline Puppeteer script executed via `node -e`
# Arguments: html_path output_image
_PUPPETEER_SCRIPT = r"""
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
  const htmlPath = process.argv[2];
  const outputPath = process.argv[3];

  if (!htmlPath || !outputPath) {
    console.error('Usage: node -e <script> <html_path> <output_path>');
    process.exit(1);
  }

  const absHtml = path.resolve(htmlPath);
  if (!fs.existsSync(absHtml)) {
    console.error('HTML file not found: ' + absHtml);
    process.exit(2);
  }

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 720 });
    await page.goto('file://' + absHtml, { waitUntil: 'networkidle0' });
    await page.screenshot({ path: outputPath, type: 'png', fullPage: false });
  } finally {
    await browser.close();
  }
})();
"""


def _find_node() -> str:
    """Return path to node binary, or raise ImportError."""
    node = shutil.which("node")
    if node is None:
        raise ImportError(
            "html2pptx requires Node.js to be installed and on PATH. "
            "Install Node.js from https://nodejs.org/. "
            "Puppeteer must also be available (npm install -g puppeteer or locally)."
        )
    return node


def _find_puppeteer_module(node: str) -> None:
    """Probe that puppeteer can be require()'d; raises ImportError if not."""
    probe = "try { require('puppeteer'); process.exit(0); } catch(e) { process.exit(1); }"
    result = subprocess.run(
        [node, "-e", probe],
        capture_output=True,
        timeout=15,
    )
    if result.returncode != 0:
        raise ImportError(
            "html2pptx requires the 'puppeteer' npm package. "
            "Install it with: npm install -g puppeteer  "
            "or locally: npm install puppeteer"
        )


def render_html_to_image(html_path: str, output_image: str) -> None:
    """Render an HTML file to a PNG image via Puppeteer.

    Parameters
    ----------
    html_path:
        Absolute or relative path to the source HTML file.
    output_image:
        Path where the PNG screenshot will be written.

    Raises
    ------
    ImportError
        If Node.js or Puppeteer is not available.
    RuntimeError
        If Puppeteer rendering fails (non-zero exit code).
    FileNotFoundError
        If *html_path* does not exist.
    """
    html_path = str(Path(html_path).resolve())
    if not Path(html_path).exists():
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    node = _find_node()
    _find_puppeteer_module(node)

    # Write the inline script to a temp file to avoid shell-quoting issues
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, encoding="utf-8") as tmp:
        tmp.write(_PUPPETEER_SCRIPT)
        script_path = tmp.name

    try:
        result = subprocess.run(
            [node, script_path, html_path, output_image],
            capture_output=True,
            text=True,
            timeout=60,
        )
    finally:
        Path(script_path).unlink(missing_ok=True)

    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"Puppeteer rendering failed (exit {result.returncode}): {stderr}")


__all__ = ["render_html_to_image"]
