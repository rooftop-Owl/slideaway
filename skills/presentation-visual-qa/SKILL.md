---
name: presentation-visual-qa
description: Visual quality assurance workflow for presentation slides — inspect rendered output for typography, color, spacing, and anti-pattern violations
version: 1.0.0
triggers:
  - visual qa
  - check presentation quality
  - inspect slides
  - qa slides
  - verify slide output
  - screenshot slides
  - render and check
---

# Presentation Visual QA

## Overview

This skill provides a systematic workflow to render presentation slides to images and
Visually inspect each frame for design quality, anti-pattern violations, and adherence
to production-ready standards. Apply after generation to catch issues before delivery.

Two rendering paths are supported depending on the slide engine and available tooling.

---

## Rendering Paths

### Path A: wkhtmltoimage (Fast, No JavaScript)

Best for standalone HTML slides that do not rely on JavaScript for layout or animation.
`wkhtmltoimage` is a headless Qt WebKit renderer — it is fast and has no runtime JS execution.

```bash
# Install (Debian/Ubuntu)
sudo apt-get install wkhtmltopdf   # includes wkhtmltoimage

# Render a single HTML slide to PNG at 1920×1080
wkhtmltoimage \
  --width 1920 \
  --height 1080 \
  --zoom 1.0 \
  --quality 95 \
  slide-01-title.html \
  qa/slide-01-title.png

# Batch render all slides in a directory
for f in slides/slide-*.html; do
  base=$(basename "$f" .html)
  wkhtmltoimage --width 1920 --height 1080 --zoom 1.0 \
    "$f" "qa/${base}.png"
done
```

**When to use**: Marp HTML output, standalone HTML slides, deck-template.html review wrapper.

**Limitations**: No JavaScript execution; CSS animations are frozen at initial state.
If slides use JS-driven layout, use Path B instead.

---

### Path B: Playwright (Full JavaScript, Screenshots)

Best for reveal.js presentations, RISE notebooks, and any slide that requires JavaScript
execution for layout, fonts loading via JS, or dynamic content.

```bash
# Install Playwright once
pip install playwright
playwright install chromium
```

```python
# qa_screenshots.py — batch capture all slides
from playwright.sync_api import sync_playwright
import glob, os

SLIDES = sorted(glob.glob("slides/slide-*.html"))
OUTPUT_DIR = "qa"
os.makedirs(OUTPUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    for path in SLIDES:
        url = f"file://{os.path.abspath(path)}"
        page.goto(url, wait_until="networkidle")
        name = os.path.basename(path).replace(".html", ".png")
        page.screenshot(path=f"{OUTPUT_DIR}/{name}", full_page=False)
        print(f"  captured {name}")
    browser.close()

print(f"Done — {len(SLIDES)} screenshots in {OUTPUT_DIR}/")
```

**When to use**: reveal.js with CDN assets, Marp presentations with JS transitions,
any slide where JS controls layout or font loading.

**Tip**: Pass `wait_until="networkidle"` so fonts and remote assets are fully loaded
before the screenshot is taken.

---

## Visual Inspection Checklist

Visually inspect each slide by loading the rendered images in sequence and evaluating
all items below. Fail the deck if any FAIL-level item is present.

### Typography

- [ ] Title font size is visually dominant — clearly larger than body text
- [ ] Body text is legible at projected scale (effective minimum 24px / 20pt)
- [ ] No text overflow or clipping at slide edges
- [ ] Line spacing is sufficient — text blocks do not feel compressed (≥1.3× font size)
- [ ] Heading hierarchy is clear — H1 > H2 > body visually distinct

### Color & Contrast

- [ ] Text-on-background contrast passes WCAG AA (≥4.5:1 ratio)
- [ ] Accent color is used sparingly — not competing with primary content
- [ ] Color palette is internally consistent across all slides
- [ ] No red/green-only differentiation that excludes colorblind viewers

### Spacing & Alignment

- [ ] Content does not hug slide edges — padding ≥2% of slide width on all sides
- [ ] Bullet lists are left-aligned and consistently indented across slides
- [ ] Multi-column layouts have equal column widths and a visible gutter
- [ ] Footer elements (slide number, author) are consistently positioned across all slides

### Content Density

- [ ] No slide contains more than 3 top-level bullets (one idea per slide rule)
- [ ] No wall-of-text slide — if prose is unavoidable, font is ≥24px and line length ≤70 chars
- [ ] Image slides have a visible caption and do not overlap text elements

### Anti-Patterns (FAIL if present)

- [ ] No accent lines under titles — decorative horizontal rules or underlines beneath
      slide titles are an AI-slop pattern that adds visual noise without information value
- [ ] No bullet walls — slides with 7+ bullets that should be split or turned into a figure
- [ ] No stock-photo backgrounds behind text (opacity washes out contrast unpredictably)
- [ ] No ALL-CAPS body text (screaming tone, reduced legibility)
- [ ] No mixed font families within a single slide body (pick one family and hold it)
- [ ] No gradient-on-gradient backgrounds (double gradient = illegible text zone risk)
- [ ] No slide that is entirely empty except for a title

---

## Anti-AI-Slop Detection

These heuristics catch the convergent aesthetic that AI-generated slide decks produce by default.
Each item below is a FAIL-level violation — treat them identically to the Anti-Patterns checklist above.

### Banned Fonts (when used as primary deck font)

The following fonts signal generic AI output. A deck using any of these as its primary typeface
has not made a distinctive typographic choice:

| Font | Why Banned |
|------|-----------|
| Inter | Default UI font for every SaaS dashboard — zero personality |
| Roboto | Android/Material default — indistinguishable from system UI |
| Arial | Legacy Windows fallback — signals no font decision was made |
| system-ui | Literally the OS default — no intentional choice at all |
| sans-serif | Generic CSS fallback — not a font choice |

**Required**: Every deck must use a distinctive font pairing from the preset's font specification
(e.g., `Playfair Display` + `Source Sans Pro`, `Space Mono` + `IBM Plex Sans`).
If the deck uses a preset, verify the font pairing is applied — not silently overridden by a fallback.

### Banned Colors

| Color / Pattern | Hex | Why Banned |
|-----------------|-----|-----------|
| Indigo / "AI purple" | `#6366f1` | The default Tailwind indigo — appears in >60% of AI-generated UIs |
| Purple-to-blue gradient on white | — | Overused AI aesthetic; signals no palette decision |

**Check**: Inspect accent colors and gradient backgrounds. If the primary accent is `#6366f1` or a
close variant (within ±15 per channel), flag it. Purple-to-blue gradients (`#6366f1 → #3b82f6`,
`#7c3aed → #2563eb`, etc.) on white or near-white backgrounds are banned.

### Banned Layout Patterns

| Pattern | Detection Signal | Why Banned |
|---------|-----------------|-----------|
| Accent line under every title | Thin horizontal rule or border-bottom directly beneath slide H1 | Decorative noise, no information value; already in Anti-Patterns above — double-flagged here |
| Space Grotesk convergence | `Space Grotesk` used as the primary heading font without a contrasting body font | Overused AI "modern" heading choice; pair it with a distinctive body or avoid |
| Bullet walls without visual breaks | 5+ bullets with no sub-grouping, icon, divider, or figure | Dense text with no visual rhythm; split into multiple slides or add structure |
| Stock photo backgrounds | Full-bleed photographic background behind text content | Contrast unpredictable, accessibility risk, generic aesthetic |

### Detection Checklist

Run this checklist in addition to the main Visual Inspection Checklist:

- [ ] Primary font is NOT Inter, Roboto, Arial, system-ui, or sans-serif
- [ ] Accent color is NOT `#6366f1` (±15 per channel tolerance)
- [ ] No purple-to-blue gradient on a white or near-white background
- [ ] No accent line (horizontal rule / border-bottom) directly under slide titles
- [ ] Space Grotesk (if used) is paired with a contrasting body font
- [ ] No slide has 5+ bullets without a visual break or structural grouping
- [ ] No stock photo used as a full-bleed text background
- [ ] Deck uses the font pairing specified by its preset (not a silent fallback)
---

## QA Verdict

### Pass Criteria

A slide deck passes visual QA when ALL of the following are true:

1. Zero FAIL-level anti-patterns detected across all slides
2. Typography checklist: all items pass
3. Color & contrast checklist: all items pass
4. Spacing & alignment checklist: all items pass
5. Content density checklist: all items pass
6. Every slide is readable at 1920×1080 without zooming in

Record a passing verdict as:

```
QA RESULT: PASS
Slides reviewed: N
Anti-patterns found: 0
Notes: [any minor observations]
```

### Fail Criteria

A slide deck fails visual QA when ANY of the following is true:

- One or more FAIL-level anti-pattern is detected
- Contrast ratio below WCAG AA on any slide
- Text overflow or clipping on any slide
- Inconsistent styling suggests template was not applied uniformly

Record a failing verdict as:

```
QA RESULT: FAIL
Failing slides: [list slide filenames]
Issues:
  - slide-03-methods.html: accent line under title (anti-pattern)
  - slide-07-results.html: 9 bullet points on one slide (density violation)
Action required: fix listed issues and re-render before delivery
```

---

## Usage

1. **Render all slides** using Path A (wkhtmltoimage) or Path B (playwright) above.
2. Open the `qa/` output directory and review each PNG in order.
3. Work through the checklist section by section.
4. Record the verdict (PASS or FAIL) with notes.
5. If FAIL: address each flagged slide, re-render, and re-run QA.
6. If PASS: attach the verdict note to the delivery message.

## Integration with Slide Generation Skill

After generating slides via the `slide-generation` skill (Section K — Validation Patterns),
run visual QA as a second layer. Structural validation (PPTX aspect ratio, font checks)
catches machine-detectable issues; visual QA catches aesthetic regressions that only
appear in the rendered image.

Recommended order:

```
1. generate slides (slide-generation skill)
2. run validate_pptx.py (structural checks)
3. render to images (this skill — Path A or B)
4. run visual checklist (this skill — checklist above)
5. record verdict and deliver
```
