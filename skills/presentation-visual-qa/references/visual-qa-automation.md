# Visual QA Automation Reference

**Scope**: Automation tools and protocols for the visual QA workflow. Covers the NEVER-read-PDF rule, PIL-based edge-content detection, PIL-based contrast checking, issue log format, and stopping criteria. Complements `presentation-visual-qa/SKILL.md`.

---

## 1. CRITICAL RULE: Never Read PDF Presentations Directly

### The Rule

**NEVER use a file-reading tool to read a PDF presentation for visual QA.**

This is not a preference — it is a hard constraint. Violating it produces fabricated QA results.

### Why This Fails

PDF presentations are binary files. When a language model attempts to "read" a PDF:
- The binary content triggers buffer overflow in text extraction
- Slide content is partially decoded, partially garbled, or silently dropped
- The model hallucinates slide content based on surrounding context
- Visual properties (font size, contrast, layout, whitespace) are completely invisible
- The resulting QA report describes slides that may not exist

**There is no partial compliance here.** Even "just checking the title" via PDF read is unreliable.

### The ONLY Correct Workflow

```
1. Generate the PDF from LaTeX/PowerPoint/reveal.js
2. Convert to images using pdf_to_images.py:
       python pdf_to_images.py presentation.pdf --output-dir slides_images/
3. Review the images using mcp_look_at or PIL-based scripts
4. Log issues in the issue log (see Section 4)
5. Fix issues in the source file
6. Regenerate PDF and repeat from step 2
```

### Explicit ❌ List

The following actions are NEVER acceptable for visual QA:

- ❌ `Read(filePath="presentation.pdf")`
- ❌ `cat presentation.pdf`
- ❌ `pdftotext presentation.pdf -` (text extraction misses visual properties)
- ❌ Any tool call that reads PDF bytes and passes them to a language model for interpretation
- ❌ "I'll just quickly check the PDF to see if the title looks right"

### Correct ✅ Actions

- ✅ `python pdf_to_images.py presentation.pdf --output-dir slides_images/`
- ✅ `mcp_look_at(file_path="slides_images/slide_001.png", goal="Check font size and contrast")`
- ✅ `detect_edge_content("slides_images/slide_001.png")`
- ✅ `check_contrast("slides_images/slide_001.png")`

---

## 2. Automated Edge-Content Detection

Content near slide edges is at risk of being cut off during printing, projection, or PDF rendering. The safe zone is typically 5–10% inset from each edge.

### When to Use

Run `detect_edge_content` on every slide image after conversion. Any slide returning a non-empty list requires manual review.

### Full Working Script

```python
import numpy as np
from PIL import Image
from pathlib import Path


def detect_edge_content(image_path, threshold=10):
    """
    Detect non-white content within `threshold` pixels of any slide edge.

    Args:
        image_path: Path to slide image (PNG or JPEG)
        threshold: Pixel distance from edge to check (default: 10)

    Returns:
        List of edge names ('left', 'right', 'top', 'bottom') where
        non-white content was detected. Empty list = no edge issues.
    """
    img = Image.open(image_path).convert('L')
    arr = np.array(img)

    edges = {
        'left':   arr[:, :threshold],
        'right':  arr[:, -threshold:],
        'top':    arr[:threshold, :],
        'bottom': arr[-threshold:, :]
    }

    return [side for side, region in edges.items() if np.any(region < 240)]


def scan_all_slides(slides_dir, threshold=10):
    """
    Scan all PNG images in a directory for edge content.

    Args:
        slides_dir: Directory containing slide images
        threshold: Pixel distance from edge to check

    Returns:
        Dict mapping filename to list of affected edges
    """
    slides_dir = Path(slides_dir)
    results = {}

    for image_path in sorted(slides_dir.glob("*.png")):
        affected_edges = detect_edge_content(image_path, threshold)
        if affected_edges:
            results[image_path.name] = affected_edges

    return results


if __name__ == "__main__":
    import sys

    slides_dir = sys.argv[1] if len(sys.argv) > 1 else "slides_images"
    issues = scan_all_slides(slides_dir)

    if not issues:
        print("✓ No edge-content issues detected")
    else:
        print(f"⚠ Edge-content issues found in {len(issues)} slide(s):")
        for filename, edges in issues.items():
            print(f"  {filename}: content near {', '.join(edges)} edge(s)")
```

### Interpreting Results

| Result | Meaning | Action |
|--------|---------|--------|
| Empty list | No content within threshold pixels of any edge | Pass — no action needed |
| `['bottom']` | Content near bottom edge | Check footnotes, slide numbers, captions |
| `['left', 'right']` | Content near both side edges | Check if margins are set correctly |
| All four edges | Full-bleed background image | Likely intentional — verify visually |

### Threshold Guidelines

- `threshold=10`: Strict — catches content within 10px of edge
- `threshold=20`: Standard — catches content within 20px (recommended default)
- `threshold=40`: Loose — only catches severely out-of-bounds content

---

## 3. Automated Contrast Checking

Low contrast between text and background is the most common accessibility failure in presentations. WCAG 2.1 requires 4.5:1 for normal text (AA) and 3:1 for large text (≥18pt or ≥14pt bold).

**Authority model** (V2.5): Element-level checks are authoritative for QA pass/fail where the engine permits. The percentile pre-filter below runs first as a fast screen — a slide failing the pre-filter needs element-level investigation; a slide passing it is NOT cleared, because the pre-filter cannot see element pairs.

### Engine-Aware Check Selection

| Engine | Authoritative method | Pre-filter |
|--------|---------------------|------------|
| Marp, reveal.js, HTML | Playwright DOM (computed fg/bg per text node) | percentile |
| md2pptx, python-pptx | python-pptx text frame scan | percentile |
| beamer, RISE | Percentile only (known-weak fallback — flagged in QA report) | percentile |

### Step 1 — Percentile Pre-Filter (All Engines)

Runs on rendered PNG images. **Does not constitute a WCAG pass/fail judgment.** A slide with a bright chart region can have a high percentile ratio while all text fails AA against its local background.

```python
import numpy as np
from PIL import Image
from pathlib import Path


def percentile_prefilter(image_path: str) -> tuple[float, bool]:
    """
    Fast contrast pre-filter using global luminance percentiles.

    Returns (ratio, has_any_contrast) where has_any_contrast=False means
    the entire slide is near-uniform — almost certainly a rendering failure,
    not a contrast failure. Does NOT constitute WCAG compliance.
    """
    img = Image.open(image_path).convert('L')
    arr = np.array(img)
    bright = np.percentile(arr, 95)
    dark = np.percentile(arr, 5)
    ratio = (bright + 0.05) / (dark + 0.05)
    return ratio, ratio >= 1.5  # threshold: any meaningful contrast at all
```

### Step 2A — Element-Level Check: HTML Engines (Playwright)

Use for Marp, reveal.js, and any HTML-rendering engine. Extracts computed `color` and `background-color` for each text node from the DOM **before** screenshot — the only approach that gives WCAG-valid element pairs.

```python
from playwright.sync_api import sync_playwright


def check_contrast_html(html_path: str, slide_index: int = 1) -> dict:
    """
    Extract element-level fg/bg pairs and compute WCAG 2.1 contrast ratios.

    Returns:
        {
          "slide": slide_index,
          "failures": [
            {"text": "...", "fg": "#rrggbb", "bg": "#rrggbb",
             "ratio": 3.2, "required": 4.5}
          ]
        }
    """
    def relative_luminance(hex_color: str) -> float:
        hex_color = hex_color.lstrip('#')
        r, g, b = (int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))
        def linearize(c: float) -> float:
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)

    def contrast_ratio(fg: str, bg: str) -> float:
        l1 = relative_luminance(fg)
        l2 = relative_luminance(bg)
        lighter, darker = max(l1, l2), min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)

    failures = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(f"file://{html_path}", wait_until="networkidle")

        text_nodes = page.evaluate("""() => {
            const results = [];
            const walker = document.createTreeWalker(
                document.body, NodeFilter.SHOW_TEXT,
                { acceptNode: n => n.textContent.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP }
            );
            let node;
            while ((node = walker.nextNode())) {
                const el = node.parentElement;
                const style = window.getComputedStyle(el);
                const text = node.textContent.trim().slice(0, 60);
                const fontSize = parseFloat(style.fontSize);
                const fontWeight = style.fontWeight;
                results.push({
                    text,
                    fg: style.color,
                    bg: style.backgroundColor,
                    fontSize,
                    bold: parseInt(fontWeight) >= 700,
                });
            }
            return results;
        }""")

        browser.close()

    def parse_rgb(css: str) -> str | None:
        import re
        m = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', css)
        if not m:
            return None
        return '#{:02x}{:02x}{:02x}'.format(*map(int, m.groups()))

    for node in text_nodes:
        fg = parse_rgb(node['fg'])
        bg = parse_rgb(node['bg'])
        if not fg or not bg or fg == bg:
            continue
        ratio = contrast_ratio(fg, bg)
        large_text = node['fontSize'] >= 18 or (node['fontSize'] >= 14 and node['bold'])
        required = 3.0 if large_text else 4.5
        if ratio < required:
            failures.append({
                "text": node['text'],
                "fg": fg,
                "bg": bg,
                "ratio": round(ratio, 2),
                "required": required,
            })

    return {"slide": slide_index, "failures": failures}
```

### Step 2B — Element-Level Check: PPTX Engines (python-pptx)

Use for `md2pptx`, `pptx`, and `python-pptx`-based engines. Iterates text frames, resolves theme colors, and computes contrast against the slide background fill or the shape's own fill.

```python
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor


def _resolve_color(color_format, theme_colors: dict) -> str | None:
    """Resolve a pptx ColorFormat to a hex string, consulting theme if needed."""
    try:
        if color_format.type is not None:
            rgb = color_format.rgb
            return f'#{rgb.red:02x}{rgb.green:02x}{rgb.blue:02x}'
    except Exception:
        pass
    return None


def _relative_luminance(hex_color: str) -> float:
    hex_color = hex_color.lstrip('#')
    r, g, b = (int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))
    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def check_contrast_pptx(pptx_path: str) -> list[dict]:
    """
    Scan all slides for element-level contrast failures.

    Returns list of per-slide dicts:
        {"slide": N, "failures": [{"text", "fg", "bg", "ratio", "required"}]}
    """
    prs = Presentation(pptx_path)
    results = []

    for slide_idx, slide in enumerate(prs.slides, 1):
        failures = []

        # Slide background color (best-effort)
        bg_hex = '#ffffff'
        try:
            bg_fill = slide.background.fill
            if bg_fill.type is not None:
                rgb = bg_fill.fore_color.rgb
                bg_hex = f'#{rgb.red:02x}{rgb.green:02x}{rgb.blue:02x}'
        except Exception:
            pass

        for shape in slide.shapes:
            tf = getattr(shape, 'text_frame', None)
            if tf is None:
                continue
            shape_bg = bg_hex
            try:
                if shape.fill.type is not None:
                    rgb = shape.fill.fore_color.rgb
                    shape_bg = f'#{rgb.red:02x}{rgb.green:02x}{rgb.blue:02x}'
            except Exception:
                pass

            for para in tf.paragraphs:
                for run in para.runs:
                    if not run.text.strip():
                        continue
                    fg = _resolve_color(run.font.color, {})
                    if fg is None:
                        continue
                    l1 = _relative_luminance(fg)
                    l2 = _relative_luminance(shape_bg)
                    lighter, darker = max(l1, l2), min(l1, l2)
                    ratio = (lighter + 0.05) / (darker + 0.05)
                    size_pt = run.font.size.pt if run.font.size else 12
                    bold = run.font.bold or False
                    large = size_pt >= 18 or (size_pt >= 14 and bold)
                    required = 3.0 if large else 4.5
                    if ratio < required:
                        failures.append({
                            "text": run.text[:60],
                            "fg": fg,
                            "bg": shape_bg,
                            "ratio": round(ratio, 2),
                            "required": required,
                        })

        results.append({"slide": slide_idx, "failures": failures})

    return results
```

### Output Format

Both checkers produce the same structure so downstream QA logic is engine-agnostic:

```json
{"slide": 3, "failures": [
  {"text": "Key finding", "fg": "#777777", "bg": "#888888",
   "ratio": 1.1, "required": 4.5}
]}
```

A slide with `"failures": []` passes element-level WCAG AA. Report failures with slide number, failing text excerpt, computed ratio, and required threshold.

### Interpreting Contrast Ratios

| Ratio | Standard | Interpretation |
|-------|----------|----------------|
| < 3.0 | Fails AA (all text) | Severe — unreadable at projection distance |
| 3.0–4.4 | Fails AA (normal); passes large text | Acceptable only for ≥18pt or ≥14pt bold |
| 4.5–6.9 | Passes AA | Acceptable for normal text |
| 7.0+ | Passes AAA | Recommended for virtual delivery and accessibility |

### Known Gaps (V2.5)

- **Beamer / RISE**: No element-level implementation. QA reports must note "contrast check: percentile pre-filter only — not WCAG authoritative" for these engines. Closing in V2.5.1.
- **Gradient backgrounds**: python-pptx cannot reliably resolve gradient fill stops to a single background color. Report as "indeterminate" rather than inventing a ratio.
- **Translucent overlays**: Playwright computes `background-color` of the immediate parent; stacked translucent layers are not resolved. Flag for manual review when opacity < 1.

---

## 4. Issue Log Template

Track all identified issues in a structured log. This enables prioritization, progress tracking, and handoff between review sessions.

### Log Format

| Slide # | Issue Category | Description | Severity | Status |
|---------|---------------|-------------|----------|--------|
| 3 | Contrast | Body text fails AA (ratio: 3.2) | High | Open |
| 7 | Edge Content | Figure caption cut off at bottom | Medium | Fixed |
| 12 | Font Size | Caption text at 10pt (min: 18pt virtual) | High | Open |
| 15 | Density | 8 bullet points on single slide | Medium | Open |
| 18 | Layout | Title overlaps figure in top-left | High | Open |

### Issue Categories

| Category | What It Covers |
|----------|---------------|
| **Contrast** | Text/background contrast ratio failures |
| **Edge Content** | Content within unsafe margin zone |
| **Font Size** | Text below minimum readable size |
| **Density** | Too much content per slide |
| **Layout** | Overlapping elements, misalignment |
| **Consistency** | Inconsistent fonts, colors, spacing across slides |
| **Accessibility** | Missing alt text, colorblind-unsafe palettes |
| **Data Integrity** | Axis labels missing, units absent, truncated values |

### Severity Levels

| Severity | Definition | Examples |
|----------|-----------|---------|
| **Critical** | Slide is unreadable or data is wrong | Blank slide, corrupted figure, wrong numbers |
| **High** | Significantly impairs comprehension | Contrast failure, text cut off, font too small |
| **Medium** | Reduces quality but slide is functional | Density too high, minor misalignment |
| **Low** | Polish issue, minimal impact | Inconsistent spacing, minor color variation |

### Status Values

- **Open**: Issue identified, not yet addressed
- **In Progress**: Fix underway
- **Fixed**: Fix applied, pending re-verification
- **Verified**: Fix confirmed in regenerated PDF images
- **Won't Fix**: Accepted as-is with documented rationale

### Example Issue Log Entry

```markdown
## Issue Log — presentation.pdf
Last updated: 2026-03-15

| Slide # | Issue Category | Description | Severity | Status |
|---------|---------------|-------------|----------|--------|
| 1 | Font Size | Subtitle at 16pt — increase to 20pt minimum | Medium | Fixed |
| 4 | Contrast | Blue text on light blue background, ratio 2.8 | High | Open |
| 4 | Edge Content | Left edge: x-axis label partially clipped | High | Open |
| 9 | Density | 7 bullets — reduce to 5 maximum | Medium | In Progress |
| 11 | Layout | Legend overlaps data region in bottom-right | High | Open |
| 14 | Data Integrity | Y-axis missing units label | Critical | Open |
```

---

## 5. Iterative Improvement Stopping Criteria

Visual QA is iterative. Knowing when to stop is as important as knowing what to check.

### Minimum Standards (Must Pass Before Presenting)

All items must be **Verified** before the presentation is considered ready:

- [ ] No **Critical** issues remain open
- [ ] No **High** severity issues remain open
- [ ] All slides pass WCAG AA contrast (4.5:1 ratio minimum)
- [ ] No content detected within 10px of any slide edge
- [ ] All font sizes ≥ 20pt for body text (≥ 24pt for virtual delivery)
- [ ] All figures have axis labels and units
- [ ] Slide numbers visible on every slide

### Ideal Standards (Target for High-Stakes Presentations)

- [ ] All slides pass WCAG AAA contrast (7:1 ratio)
- [ ] No **Medium** severity issues remain open
- [ ] Content density ≤ 5 bullet points per slide
- [ ] All figures have captions
- [ ] Consistent font family and size hierarchy throughout
- [ ] Color palette verified as colorblind-safe (deuteranopia + protanopia)

### Prioritization Tiers

**Fix Immediately** (blocks presentation):
- Critical issues (unreadable slides, wrong data)
- High contrast failures on text-heavy slides
- Content cut off by edge clipping

**Fix Before Presenting** (degrades quality):
- High density slides (>6 bullets)
- Medium contrast failures
- Missing axis labels or units

**Fix If Time Permits** (polish):
- Minor alignment inconsistencies
- Low severity spacing issues
- Font size at minimum threshold (not below)

### Stopping Decision Flowchart

```
All Critical issues resolved?
  No → Keep fixing
  Yes ↓

All High issues resolved?
  No → Keep fixing (or document accepted risk)
  Yes ↓

Passes Minimum Standards checklist?
  No → Address remaining checklist items
  Yes ↓

STOP — presentation is ready for delivery
(Continue to Ideal Standards if time permits)
```

### Re-Verification Protocol

After fixing any issue:
1. Regenerate the PDF from source
2. Re-run `pdf_to_images.py` on the updated PDF
3. Re-run `detect_edge_content` and `check_contrast` on affected slides
4. Update issue log status from "Fixed" to "Verified"
5. Do NOT mark as Verified based on source file inspection alone — always verify from the rendered image

---

*This reference covers automation tooling for visual QA. For the full QA protocol and review workflow, see the parent `SKILL.md`. For slide design principles that inform what to look for, see `delivery-intelligence.md`.*
