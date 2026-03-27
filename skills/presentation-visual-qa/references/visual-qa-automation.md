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

Low contrast between text and background is the most common accessibility failure in presentations. The WCAG standard requires 4.5:1 for normal text (AA) and 7:1 for enhanced accessibility (AAA).

### When to Use

Run `check_contrast` on slides with text-heavy content, slides using colored backgrounds, and any slide where text color deviates from black-on-white.

### Full Working Script

```python
import numpy as np
from PIL import Image
from pathlib import Path


def check_contrast(image_path):
    """
    Estimate contrast ratio of a slide image using luminance percentiles.

    Uses the 95th percentile as the 'bright' reference and the 5th percentile
    as the 'dark' reference, approximating the contrast between background
    and foreground text regions.

    Args:
        image_path: Path to slide image (PNG or JPEG)

    Returns:
        Tuple of (ratio: float, passes_aa: bool)
        - ratio: Estimated contrast ratio (higher = more contrast)
        - passes_aa: True if ratio >= 4.5 (WCAG AA standard)
    """
    img = Image.open(image_path).convert('L')
    arr = np.array(img)

    bright = np.percentile(arr, 95)
    dark = np.percentile(arr, 5)

    ratio = (bright + 0.05) / (dark + 0.05)
    return ratio, ratio >= 4.5


def check_contrast_aaa(image_path):
    """
    Check contrast against WCAG AAA standard (7:1 ratio).

    Args:
        image_path: Path to slide image

    Returns:
        Tuple of (ratio: float, passes_aaa: bool)
    """
    ratio, _ = check_contrast(image_path)
    return ratio, ratio >= 7.0


def scan_contrast_all_slides(slides_dir, standard='aa'):
    """
    Scan all slides for contrast compliance.

    Args:
        slides_dir: Directory containing slide images
        standard: 'aa' (4.5:1) or 'aaa' (7:1)

    Returns:
        Dict mapping filename to (ratio, passes) tuples
    """
    slides_dir = Path(slides_dir)
    threshold = 7.0 if standard == 'aaa' else 4.5
    results = {}

    for image_path in sorted(slides_dir.glob("*.png")):
        img = Image.open(image_path).convert('L')
        arr = np.array(img)
        bright = np.percentile(arr, 95)
        dark = np.percentile(arr, 5)
        ratio = (bright + 0.05) / (dark + 0.05)
        passes = ratio >= threshold
        results[image_path.name] = (round(ratio, 2), passes)

    return results


if __name__ == "__main__":
    import sys

    slides_dir = sys.argv[1] if len(sys.argv) > 1 else "slides_images"
    standard = sys.argv[2] if len(sys.argv) > 2 else "aa"

    results = scan_contrast_all_slides(slides_dir, standard)
    failures = {f: r for f, r in results.items() if not r[1]}

    if not failures:
        print(f"✓ All slides pass WCAG {standard.upper()} contrast standard")
    else:
        print(f"⚠ Contrast failures ({standard.upper()}) in {len(failures)} slide(s):")
        for filename, (ratio, _) in failures.items():
            print(f"  {filename}: ratio = {ratio:.2f} (required: "
                  f"{'7.0' if standard == 'aaa' else '4.5'})")
```

### Interpreting Contrast Ratios

| Ratio | Standard | Interpretation |
|-------|----------|----------------|
| < 3.0 | Fails AA | Severe contrast issue — likely unreadable |
| 3.0–4.4 | Fails AA | Marginal — acceptable only for large text (18pt+) |
| 4.5–6.9 | Passes AA | Acceptable for normal text |
| 7.0+ | Passes AAA | Recommended for virtual delivery and accessibility |
| 15.0+ | Exceeds AAA | Typical for black text on white background |

### Limitations

The `np.percentile`-based approach is a global estimate. It works well for slides with clear foreground/background separation. For slides with complex imagery or gradients, supplement with manual visual review.

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
