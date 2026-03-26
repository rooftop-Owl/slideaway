---
name: /slides
description: Generate presentations via 7-engine armory (Marp, md2pptx, python-pptx, reveal.js, Beamer, HTML, RISE)
agent: hephaestus
deployable: true
source: slides
---

# /slides

Generate presentations, slide decks, and posters via a 7-engine armory. Default output: styled editable PPTX via python-pptx + SlideFactory.

Delegates to **Hephaestus** with subdirectory skill `slide-generation` via `load_skills=["slide-generation"]`.

## Usage

```
/slides "Create a 10-slide talk on climate risk assessment results"
/slides "topic" --engine md2pptx
/slides "topic" --engine marp --format pdf
/slides "topic" --engine pptx --template corporate.pptx
/slides "topic" --engine reveal --interactive
/slides "topic" --engine beamer --academic
/slides "topic" --from paper-draft.md --format pptx
```

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `<topic>` | required | Natural language description of desired presentation |
| `--engine` | auto | Engine: `marp`, `md2pptx`, `pptx`, `reveal`, `beamer`, `html`, `rise` |
| `--format` | `pptx` | Output: `html`, `pdf`, `pptx`, `notebook`, `all` |
| `--theme` | `default` | Theme name or path to custom CSS/template |
| `--from` | — | Source file to base slides on. Supported: `.md`, `.tex`, `.pdf`, `.txt`, `.ipynb`. Files >50KB chunked automatically. |
| `--slides` | `10` | Target number of slides |
| `--output` | `./slides/` | Output directory |
| `--academic` | false | Use academic-oriented engine/theme |
| `--interactive` | false | Prefer interactive output (reveal.js) |
| `--static` | false | For PPTX: use Marp image-based instead of editable |
| `--template` | — | Path to `.pptx` template (for md2pptx or python-pptx) |
| `--preview` | false | Generate 2-3 style previews before full deck (opt-in). Shows visual options for style selection. |
| `--refine` | false | After generation, auto-inspect and fix issues (opt-in, max 2 iterations). Uses slide-qa agent. |
| `--style <name>` | — | Use a specific style preset by name (e.g., --style executive-suite). Skips style selection. |

## Theme Usage

Bundled Marp themes are in `templates/marp/`. Pass them via `--theme-set`:

```bash
# Default theme (clean modern)
marp slides.md -o slides.html \
  --theme-set modules/slides/templates/marp \
  --theme slides-default \
  --bespoke.osc false --bespoke.progress

# Academic theme (serif headings, three-line tables)
marp slides.md -o slides.html \
  --theme-set modules/slides/templates/marp \
  --theme academic \
  --bespoke.osc false --bespoke.progress

# PDF with academic theme
marp slides.md --pdf -o slides.pdf \
  --theme-set modules/slides/templates/marp \
  --theme academic
```

## Deck Review Mode

For reviewing multiple slides at once, use the deck-template wrapper:

```bash
# Open deck-template.html in a browser to review all slides in a scrollable view.
# The template supports:
#   - Keyboard navigation (arrow keys, space bar)
#   - Dark mode (follows OS preference)
#   - Responsive layout for mobile/tablet
```

Template: `modules/slides/templates/html/deck-template.html`

## Layout Variants (Standalone HTML)

The standalone HTML template supports 4 layout variants via CSS classes:

| Class | Use Case | Visual |
|-------|----------|--------|
| `slide--title` | Title/cover slide | Gradient background, centered text |
| `slide--content` | Standard content | Header bar, bullet list |
| `slide--section` | Section break | Diagonal stripe pattern, centered heading |
| `slide--split` | Two-column layout | Side-by-side content areas |

## Engine Resolution (when no `--engine` specified)

```
--format pptx                → python-pptx + SlideFactory (styled editable default)
--format pptx --template X   → md2pptx (template-first markdown import)
--format pptx --static       → Marp (image-based)
--format html                → Marp (clean, fast)
--format html --interactive  → reveal.js (animations, fragments)
--format pdf                 → Marp (modern)
--format pdf --academic      → Beamer (traditional)
--format notebook            → RISE
No format specified          → python-pptx + SlideFactory
```

Routing rule: if styling quality is required (16:9, explicit fonts, title/subtitle separation, slide numbers), prefer python-pptx. Use md2pptx only for template-first markdown workflows.

## Orchestration Flow

```
User request
    │
    ├─[1]─► Parse arguments, resolve engine (see resolution logic above)
    │
    ├─[2]─► Check engine dependencies available
    │       If missing: report issue, suggest install command,
    │       offer fallback engine (e.g., md2pptx for template-first markdown,
    │       or Marp static if editable path unavailable)
    │
    ├─[3]─► Generate presentation structure (outline)
    │       Agent creates slide-by-slide outline:
    │       - Slide 1: Title
    │       - Slide 2: Motivation/Problem
    │       - Slides 3-N: Content
    │       - Slide N+1: Summary/Conclusion
    │       - Speaker notes per slide
    │
    ├─[4]─► Generate source content
    │       Engine-specific format:
    │       - Marp/md2pptx: Marp-flavored or standard Markdown
    │       - python-pptx: Python script with SlideFactory
    │       - reveal.js: Markdown with YAML frontmatter
    │       - Beamer: LaTeX document
    │       - HTML: Individual HTML files
    │       - RISE: Tagged Jupyter notebook
    │
    ├─[4.5]► Convert via engine
    │        Run engine command. Check exit code.
    │        If non-zero: capture stderr, report:
    │        "Engine failed: {stderr}. Check: dependencies installed?
    │         Source syntax correct? Output path writable?"
    │
    ├─[5]─► Validate output
    │       - File exists and is non-empty
    │       - For PPTX: mandatory structural inspection
    │         (`python3 modules/slides/tools/validate_pptx.py output.pptx`)
    │       - For HTML: optionally screenshot via chrome-devtools
    │       - For PDF: check page count with pdfinfo
    │
    └─[6]─► Report
            "✓ Generated 10-slide presentation
             Engine: python-pptx + SlideFactory (editable PPTX)
             Output: ./slides/climate-risk-talk.pptx
             Editable: ✅ Yes — open in PowerPoint to edit
             Validation: structural inspection passed
             Source: ./slides/build_slides.py (edit and re-run)"
```

## Skill Required

This command loads the subdirectory skill `slide-generation` into Hephaestus. The skill contains all engine-specific workflows, invocation patterns, and validation steps.

If `slides` module is not loaded, run:
```bash
astraeus load slides
```
