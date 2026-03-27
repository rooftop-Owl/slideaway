# Getting Started with Slides

The slides module gives you a 7-engine presentation armory — from quick Markdown-to-PDF previews
to polished editable PPTX decks. All engines are optional; the module loads cleanly with none
installed and degrades gracefully.

---

## Overview

The `/slides` command routes your request to the best engine for the job:

- **Default output**: Editable PPTX via `python-pptx` + SlideFactory (16:9, styled, presentation-ready)
- **Quick preview**: HTML or PDF via Marp CLI
- **Academic talks**: LaTeX Beamer PDF
- **Web presentations**: reveal.js interactive HTML
- **Zero-dependency**: Standalone HTML (no tools required)
- **Live code demos**: RISE in Jupyter notebooks

You can override the engine with `--engine` or let the command pick the best fit based on your
requested output format.

---

## Prerequisites

All dependencies are **optional**. The module loads without any of them installed. Install only
what you need for the engines you plan to use.

| Dependency | Install Command | Required By |
|------------|-----------------|-------------|
| `python-pptx` | `pip install python-pptx` | python-pptx engine, md2pptx |
| `marp-cli` | `npm install -g @marp-team/marp-cli` | Marp engine |
| `pandoc` | See [pandoc.org](https://pandoc.org/installing.html) | reveal.js, Beamer |
| `pdflatex` | TeX Live or MiKTeX | Beamer engine |
| Chromium | System package manager | Marp PDF/PPTX output |
| `rise` | `pip install rise` | RISE/Jupyter engine |

**Minimum setup** (recommended for most users):

```bash
pip install python-pptx
```

This unlocks the default engine (python-pptx) and md2pptx.

---

## Quick Start

### Install the plugin

```bash
/plugin marketplace add rooftop-Owl/slideaway
/plugin install slideaway@slideaway-marketplace
```

This adds the `/slides` command and `slide-generation` skill to your project.

### Generate your first deck

```bash
# Default: styled editable PPTX
/slides "Introduction to Machine Learning"

# Specify engine
/slides "Q3 Results" --engine marp --format pdf

# From existing Markdown file
/slides --input my-notes.md --engine md2pptx
```

---

## Your First Deck

### Option 1: Let the command decide

```
/slides "Climate Change: Causes and Solutions"
```

The command will:
1. Outline a 10-slide structure
2. Generate content for each slide
3. Produce a styled PPTX using python-pptx + SlideFactory
4. Save to `climate-change-causes-and-solutions.pptx`

### Option 2: From your own Markdown

Write your slides in Markdown first:

```markdown
# My Talk

---

## Introduction

- Point one
- Point two
- Point three

---

## Key Findings

Content here...
```

Then convert:

```bash
# Editable PPTX from Markdown
python3 modules/slides/tools/md2pptx/md2pptx.py output.pptx < slides.md

# HTML preview
marp slides.md -o slides.html

# PDF
marp slides.md --pdf -o slides.pdf
```

> **Note**: `md2pptx` is bundled at `modules/slides/tools/md2pptx/md2pptx.py`. Do NOT run
> `pip install md2pptx` — it is not on PyPI.

---

## Output Formats

| Format | Engine | Command Flag | Notes |
|--------|--------|--------------|-------|
| Editable PPTX | python-pptx | `--format pptx` | Default. Fully editable in PowerPoint/Keynote |
| Editable PPTX | md2pptx | `--engine md2pptx` | Template-first Markdown import |
| HTML preview | Marp | `--format html` | Fast, shareable in browser |
| PDF (modern) | Marp | `--format pdf` | Requires Chromium |
| PDF (academic) | Beamer | `--engine beamer` | LaTeX quality, equations |
| Interactive HTML | reveal.js | `--engine revealjs` | Animations, speaker notes |
| Standalone HTML | HTML | `--engine html` | Zero dependencies |
| Live notebook | RISE | `--engine rise` | Jupyter + RISE extension |

---

## Next Steps

- **Choose an engine**: See [Engine Selection Guide](engine-guide.md) for a decision matrix
- **Pick a style**: See [Style Catalog](style-catalog.md) for 30 curated visual styles
- **Validate output**: Run `python3 modules/slides/tools/validate_pptx.py output.pptx` to check
  structure (aspect ratio, fonts, title slide)
- **Templates**: Pre-built templates are in `modules/slides/templates/` for Marp, Beamer, and HTML
