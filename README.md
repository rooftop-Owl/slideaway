# Slides Plugin (v2.0.0)

> **Presentation armory for astraeus agents.** Generate styled slide decks, posters, and presentations from Markdown, papers, or natural language descriptions — via 7 rendering engines and 30 curated visual styles.

---

## Overview

The `slides` module extends astraeus with a full presentation generation pipeline. It provides:

- **7 rendering engines** — from quick Marp previews to polished editable PPTX to academic Beamer PDFs
- **30 curated visual styles** across 6 categories (corporate, academic, creative, technical, elegant, specialty)
- **3 skills** covering generation, design intelligence, and visual QA
- **2 specialized agents** — `slide-designer` and `slide-qa`
- **1 command** — `/slides` with engine routing, style selection, and optional preview/refine flags
- **Production tools** — `slide_factory.py`, `validate_pptx.py`, `thumbnail_grid.py`, plus bundled `html2pptx/`, `pptx_editor/`, and `md2pptx/`

The default output is a styled, editable 16:9 PPTX via `python-pptx + SlideFactory`. All dependencies are optional — engines degrade gracefully with install guidance when unavailable.

This module **supersedes** the `presentation` skill from `research-core`. The original skill remains in research-core as a lightweight fallback for projects that don't load `slides`.

---

## Quick Start

```bash
# Load the module into your project
astraeus load slides

# Generate a presentation
/slides "Create a 10-slide talk on climate risk assessment results"

# Specify engine and format
/slides "topic" --engine marp --format pdf

# Use a named style
/slides "topic" --style executive-suite

# Preview style options before committing
/slides "topic" --preview

# Auto-refine after generation (max 2 iterations via slide-qa)
/slides "topic" --refine
```

After loading, the `slide-generation` skill and `/slides` command are available in your project. The `md2pptx` bundled script is also accessible at `.claude/tools/md2pptx/md2pptx.py`.

---

## Engines

Seven engines cover every presentation use case. The default (`python-pptx + SlideFactory`) produces styled, editable PPTX with proper 16:9 layout, header/footer, bullet styling, and image fitting.

| Engine | Best For | Output | Dependency |
|--------|----------|--------|------------|
| **python-pptx** | Default — styled editable deck | Editable PPTX | `pip install python-pptx` |
| **md2pptx** | Template-first Markdown import | Editable PPTX | `python-pptx` (bundled script) |
| **Marp** | Quick preview, PDF handouts | HTML / PDF / PPTX (images) | `npm install -g @marp-team/marp-cli` |
| **reveal.js** | Web presentations, animations | Interactive HTML | `pandoc` or `npx` |
| **Beamer** | Conference talks, equations | Academic PDF | `pdflatex` (TeX Live / MiKTeX) |
| **Standalone HTML** | Full design control, version-controllable | HTML files | None |
| **RISE/Jupyter** | Live code demonstrations | Live notebook | `pip install rise` |

**Engine auto-resolution** (when `--engine` is omitted):

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

**Graceful degradation**: if an engine is unavailable, the module reports the missing dependency with its install command and offers the nearest fallback. It never silently fails.

---

## Styles

30 curated visual styles across 6 categories. Specify with `--style <name>` or describe your desired look and the command selects the best match.

| Category | Count | Aesthetic | Example Styles |
|----------|-------|-----------|----------------|
| **Corporate** | 5 | Professional, brand-safe, boardroom-ready | `corporate-blue`, `corporate-minimal`, `corporate-bold` |
| **Academic** | 5 | Clean, readable, conference-appropriate | `academic-clean`, `academic-metropolis`, `academic-poster` |
| **Creative** | 5 | Bold, expressive, high visual impact | `creative-gradient`, `creative-dark-pop`, `creative-editorial` |
| **Technical** | 5 | Code-friendly, dark themes, developer-focused | `tech-dark`, `tech-terminal`, `tech-blueprint` |
| **Elegant** | 5 | Minimal, refined, premium feel | `elegant-mono`, `elegant-serif`, `elegant-glass` |
| **Specialty** | 5 | Purpose-built for specific contexts | `pitch-deck`, `data-story`, `workshop` |

Full style descriptions, color palettes, and typography specs: [handbook/style-catalog.md](handbook/style-catalog.md)

Use `--preview` to generate 2–3 style previews before committing to a full deck.

---

## Commands

### `/slides`

7-engine presentation router. Delegates to **Hephaestus** with the `slide-generation` skill.

```
/slides "topic"                          # Default: python-pptx editable PPTX
/slides "topic" --engine md2pptx         # Template-first Markdown import
/slides "topic" --engine marp --format pdf
/slides "topic" --engine reveal --interactive
/slides "topic" --engine beamer --academic
/slides "topic" --from paper-draft.md --format pptx
/slides "topic" --style corporate-blue
/slides "topic" --preview                # Show style options first
/slides "topic" --refine                 # Auto-QA and fix after generation
```

**Key flags:**

| Flag | Default | Description |
|------|---------|-------------|
| `--engine` | auto | `marp`, `md2pptx`, `pptx`, `reveal`, `beamer`, `html`, `rise` |
| `--format` | `pptx` | `html`, `pdf`, `pptx`, `notebook`, `all` |
| `--style <name>` | — | Named style preset (e.g., `executive-suite`). Skips style selection. |
| `--preview` | false | Generate 2–3 style previews before full deck (opt-in) |
| `--refine` | false | Auto-inspect and fix issues after generation (opt-in, max 2 iterations) |
| `--from` | — | Source file: `.md`, `.tex`, `.pdf`, `.txt`, `.ipynb`. Files >50KB chunked. |
| `--slides` | `10` | Target number of slides |
| `--template` | — | Path to `.pptx` template (for md2pptx or python-pptx) |
| `--academic` | false | Use academic-oriented engine/theme |
| `--interactive` | false | Prefer interactive output (reveal.js) |
| `--output` | `./slides/` | Output directory |

---

## Agents

Two specialized agents handle generation and quality assurance:

### `slide-designer`

Generates presentation content and structure. Handles engine selection, outline creation, source content generation (Markdown, Python, LaTeX, HTML), and engine invocation. Reports output path, engine used, editability status, and validation results.

### `slide-qa`

Visual quality assurance agent. Inspects rendered slides for layout issues, font consistency, contrast ratios, and structural problems. Used automatically when `--refine` is passed to `/slides` (max 2 iterations). Can also be invoked directly for manual QA on existing decks.

---

## Plugin Structure

```
modules/slides/
├── README.md                          # This file — full documentation
├── AGENTS.md                          # → redirects to README.md
├── MODULE_CONTEXT.md                  # → redirects to README.md
├── module.json                        # Module manifest (astraeus discoverability)
│
├── agents/
│   ├── slide-designer.md              # Presentation generation agent
│   └── slide-qa.md                    # Visual QA agent
│
├── commands/
│   └── slides.md                      # /slides command definition
│
├── skills/
│   ├── slide-generation/              # 7-engine generation workflows
│   ├── presentation-design-styles/    # 30 styles, 5 presets, anti-patterns
│   └── presentation-visual-qa/        # Visual rendering checks, Playwright
│
├── tools/
│   ├── slide_factory.py               # python-pptx helper (16:9, styling)
│   ├── validate_pptx.py               # Structural PPTX inspection CLI
│   ├── thumbnail_grid.py              # Slide thumbnail grid generator
│   ├── html2pptx/                     # HTML → PPTX conversion pipeline
│   ├── pptx_editor/                   # PPTX editing utilities
│   └── md2pptx/                       # Bundled md2pptx script (NOT on PyPI)
│
├── templates/
│   ├── marp/
│   │   ├── default.css                # Clean modern 16:9 Marp theme
│   │   ├── academic.css               # Conference/academic theme
│   │   └── .marprc.yml                # Reference Marp CLI configuration
│   ├── beamer/
│   │   └── metropolis-template.tex    # Modern academic LaTeX starter
│   └── html/
│       ├── slide-template.html        # Standalone HTML (4 layout variants)
│       └── deck-template.html         # Multi-slide review wrapper
│
├── handbook/
│   ├── getting-started.md             # Step-by-step usage guide
│   ├── engine-guide.md                # Deep-dive per-engine reference
│   └── style-catalog.md              # All 30 styles with descriptions
│
├── hooks/                             # Plugin lifecycle hooks
├── tests/                             # Test suite
└── .claude-plugin/                    # Plugin metadata
```

---

## Skills

Three skills with progressive disclosure — load only what you need:

| Skill | Triggers | Content |
|-------|----------|---------|
| `slide-generation` | `marp`, `slide deck`, `generate slides`, `editable pptx`, `beamer talk`, `reveal slides`, `poster` | 7-engine armory with invocation patterns, engine resolution logic, validation steps, and graceful degradation |
| `presentation-design-styles` | `design style`, `color palette`, `font selection`, `visual style` | 30 curated styles, 5 aesthetic presets, CSS themes, anti-pattern checklist |
| `presentation-visual-qa` | `visual QA`, `screenshot check`, `render verify` | Visual rendering verification, wkhtmltoimage + Playwright workflow, checklist |

**Progressive disclosure**: `slide-generation` is the primary skill and covers all engine workflows. Load `presentation-design-styles` when style selection or design critique is needed. Load `presentation-visual-qa` for automated visual inspection.

Always load `slide-generation` when working on presentations:

```python
load_skills=["slide-generation"]
```

---

## Tools

### `slide_factory.py`

Production-ready `python-pptx` helper. Creates styled 16:9 presentations with proper header/footer, bullet styling, and image fitting. The default engine for `/slides` without flags.

### `validate_pptx.py`

Structural inspection CLI for PPTX outputs. Checks aspect ratio, font consistency, title slide presence, and slide count. Run automatically after python-pptx generation:

```bash
python3 modules/slides/tools/validate_pptx.py output.pptx
```

### `thumbnail_grid.py`

Generates a thumbnail grid image from a PPTX or HTML slide deck. Useful for quick visual review and style comparison.

### `html2pptx/`

Pipeline for converting HTML slides to PPTX format. Handles layout preservation and image extraction.

### `pptx_editor/`

Utilities for programmatic PPTX editing — modify existing decks, update text, swap images, adjust layouts.

### `md2pptx/`

Bundled standalone script (NOT on PyPI — do not `pip install md2pptx`). Converts Markdown to editable PPTX via a template-first approach.

```bash
# Correct invocation
python3 modules/slides/tools/md2pptx/md2pptx.py output.pptx < slides.md

# After astraeus load slides
python3 .claude/tools/md2pptx/md2pptx.py output.pptx < slides.md
```

Requires: `pip install python-pptx`

---

## Dependencies

All dependencies are optional — the module loads cleanly with none installed.

| Dependency | Install | Required By |
|------------|---------|-------------|
| `python-pptx` | `pip install python-pptx` | md2pptx, python-pptx engine, slide_factory |
| `marp-cli` | `npm install -g @marp-team/marp-cli` | Marp engine |
| `pandoc` | [pandoc.org](https://pandoc.org/) | reveal.js, Beamer |
| `pdflatex` | TeX Live or MiKTeX | Beamer engine |
| `Chromium` | System package | Marp PDF/PPTX (headless), visual QA |
| `rise` | `pip install rise` | RISE/Jupyter engine |

---

## Module Management

```bash
astraeus load slides      # Load into project
astraeus unload slides    # Clean removal (symlinks only)
astraeus list             # Verify module is registered
```
