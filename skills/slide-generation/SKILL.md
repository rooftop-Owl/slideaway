---
triggers: [marp, marp slides, marp deck, slide deck, generate slides, generate presentation, pptx generation, editable pptx, editable powerpoint, make slides, create presentation, beamer talk, reveal slides, html slides, conference poster, academic poster]
domains: [research, presentation, communication, output]
name: slide-generation
description: Use when generating slide presentations, posters, or visual output. Comprehensive armory with 7 engines — Marp, md2pptx, python-pptx, reveal.js, Beamer, HTML, RISE. Supersedes basic presentation skill.
version: "2.0.0"
success_criteria: ["engine selected appropriately", "content generated in target format", "output validated"]
---

# Slide Generation — Progressive Disclosure Armory

7 engines. One skill. Pick the right tool, load the right reference, generate and validate before delivery.

## Phase Flow Overview

1. Select engine (Section A decision matrix)
1.5. Optional style preview gate (`--preview`, Phase 0.5)
2. Load required reference file(s)
3. Generate output with engine-specific commands
4. Validate structure/output integrity
5. Deliver with validation notes
5.5. Optional refinement loop (`--refine`, Phase 5.5)

## Phase-Loading Rules
When generating with a specific engine, you MUST read the corresponding reference file:
- Marp output → read `references/engine-marp.md`
- md2pptx output → read `references/engine-md2pptx.md`
- python-pptx output → read `references/engine-pptx.md`
- reveal.js output → read `references/engine-revealjs.md`
- Beamer/LaTeX output → read `references/engine-beamer.md`
- HTML/RISE output → read `references/engine-html.md`
- Poster output → read `references/poster-design.md`
- `--preview` enabled → run Phase 0.5 and read mood→preset mapping from `presentation-design-styles` skill before full generation
- For ALL outputs → read `references/design-principles.md` (presentation intelligence)
- Before delivery → read `references/validation-patterns.md`
- `--refine` enabled → run Phase 5.5 and apply visual QA references (`presentation-visual-qa` + design-principles J.11) with delegated `slide-qa` inspection

## Minimum Required Context

| Context Item | Requirement |
|--------------|-------------|
| Goal and audience | Purpose type + audience depth/familiarity (map to Section J guidance) |
| Output format | `pptx`, `pdf`, `html`, `notebook`, or poster |
| Editability requirement | Editable vs static output (critical for PPTX engine choice) |
| Template constraints | Existing corporate template path or style constraints |
| Runtime constraints | Offline/online, dependency availability, execution environment |
| Delivery constraints | Deadline, venue constraints, and acceptance/validation criteria |

## Canonical Entry Point: Engine Selection + UX Baseline

## Section A — Engine Selection Guide

### Decision Matrix

| Goal | Engine | Command |
|------|--------|---------|
| Quick preview | Marp | `marp slides.md -o slides.html` |
| Share editable PPTX (presentation-ready styling) | python-pptx + SlideFactory | `python3 build_slides.py` |
| Fill an existing corporate template from Markdown | md2pptx | `python3 modules/slides/tools/md2pptx/md2pptx.py output.pptx < slides.md` |
| Data-driven slides | python-pptx + SlideFactory | Python script with SlideFactory |
| Interactive web | reveal.js | `pandoc -t revealjs -s --embed-resources` |
| Academic conference | Beamer | `pdflatex slides.tex` |
| Full design control | Standalone HTML | Individual HTML files |
| Live code demo | RISE/Jupyter | Jupyter + RISE extension |
| Modern PDF handout | Marp | `marp slides.md --pdf` |
| Corporate template with exact positioning | python-pptx + SlideFactory | Template-based Python script |
| Academic poster | tikzposter | `pdflatex poster.tex` |

### Engine Resolution (no --engine flag)

When the user doesn't specify an engine, resolve by format flag.

Apply this gate before selecting editable PPTX engine:

1. If the user needs presentation-ready styling (16:9 ratio, explicit fonts, title/subtitle/author separation, header bars, slide numbering, bold-prefix bullets), use **python-pptx + SlideFactory**.
2. If the user explicitly wants template-first Markdown import with minimal styling control, use **md2pptx**.

| Flag | Engine | Rationale |
|------|--------|-----------|
| `--format pptx` | python-pptx + SlideFactory (styled default) | Reliable visual structure and formatting control |
| `--format pptx --template X` | md2pptx (template-first Markdown) | Fast markdown-to-template path, inherits template styles |
| `--format pptx --static` | Marp (image-based) | Fast, no dependencies beyond marp |
| `--format html` | Marp | Clean, fast, single file |
| `--format html --interactive` | reveal.js | Auto-Animate, fragments, 2D nav |
| `--format pdf` | Marp | PDF from Markdown, no LaTeX needed |
| `--format pdf --academic` | Beamer | Full LaTeX control, citations |
| `--format notebook` | RISE | Live code in slides |
| No format | python-pptx + SlideFactory | Default editable PPTX with production-ready styling |

**Default rule**: When in doubt, produce editable PPTX via python-pptx with SlideFactory.

**DO NOT use md2pptx for styled decks.** md2pptx is template-first and can strip Markdown emphasis, create empty separator slides, and inherit font/ratio defaults when template metadata is incomplete.

---

## Section A2 — UX Quality Checklist (Required)

If you generate slides that "run" but look like a demo, you failed the UX.

Before delivering any deck (any engine), verify these minimums:

### Content

- Slide count: >= 8 (unless user explicitly asks for fewer)
- Each slide has >= 2 meaningful bullets OR one strong visual with a caption
- No slide with only 1-2 short bullets (merge with neighbor or expand)
- Prefer complete sentences for bullets when explaining a system

### Title Slide Metadata (do not skip)

Include at least:

- Title
- Subtitle
- Author (or team)
- Date

Example:

"astraeus"\n"Adaptive AI agent orchestration"\n"Sisyphus team"\n"2026-02-23"

### Visual Hierarchy

- Title must be visually dominant (size and weight)
- Subtitle must not outshine title
- Avoid placing all content in one corner while leaving 50%+ empty space

### Engine-Specific Must-Haves

- Marp HTML: disable on-screen controller for clean export (`--bespoke.osc false`)
- reveal.js: if you use CDN assets, document that output is not offline-safe
- Standalone HTML: must be self-contained (no CDN); font sizes must be readable on a projector
- md2pptx: accept that md2pptx may add a tool info slide; prefer starting user content on slide 2

### Evidence (when asked to validate)

- PPTX: count slides via python-pptx
- HTML: screenshot at least slide 1 (and slide 2 for interactive decks)
- Beamer: if TeX missing, still generate .tex and capture the compilation error

## Section A3 — Layout Variants (Standalone HTML)

The standalone HTML template (`templates/html/slide-template.html`) supports 4 layout variants. Use the correct CSS class for each slide type.

### Variant Reference

| Variant | CSS Class | When to Use |
|---------|-----------|-------------|
| Title | `slide--title` | First slide — title, subtitle, author, date |
| Content | `slide--content` | Standard bullet or text slides |
| Section Break | `slide--section` | Transition between major sections (diagonal stripe pattern) |
| Split | `slide--split` | Two-column layouts — text+image, comparison, before/after |

### Visual Differences

- **Title** (`slide--title`): Full gradient background (`--c-accent` → darker), centered white text, large heading
- **Content** (`slide--content`): White background, colored header bar, left-aligned body content
- **Section Break** (`slide--section`): Accent background with diagonal stripe overlay pattern, centered heading — visually distinct from title slide
- **Split** (`slide--split`): Two equal columns with a vertical divider, each independently scrollable

### Jinja2 Generation Example

To generate slides programmatically from structured data:

```python
from jinja2 import Environment, FileSystemLoader
import json

env = Environment(loader=FileSystemLoader('modules/slides/templates/html/'))
template = env.get_template('slide-template.html')

# Slide data structure
slides = [
    {
        'variant': 'title',
        'title': 'Climate Risk Assessment',
        'subtitle': 'Annual Expected Impact Analysis',
        'author': 'Research Team',
        'affiliation': 'ETH Zürich',
        'date': '2026-02-24',
        'slug': 'title'
    },
    {
        'variant': 'content',
        'title': 'Methodology',
        'bullets': [
            'Hazard: IBTrACS tropical cyclone tracks (1980–2023)',
            'Exposure: LitPop v2 GDP-weighted asset distribution',
            'Vulnerability: Emanuel (2011) wind damage function',
        ],
        'slug': 'methodology'
    },
    {
        'variant': 'section',
        'title': 'Results',
        'slug': 'results-break'
    },
    {
        'variant': 'split',
        'title': 'Impact by Region',
        'left_content': '<ul><li>Coastal: +65%</li><li>Inland: +12%</li></ul>',
        'right_content': '<img src="plots/map.png" alt="Impact map">',
        'slug': 'impact-by-region'
    },
]

for i, slide in enumerate(slides, 1):
    html = template.render(**slide, slide_num=i, total=len(slides))
    with open(f'slides/slide-{i:02d}-{slide["slug"]}.html', 'w') as f:
        f.write(html)
```

### Metadata Slots

The title variant supports these metadata fields (rendered in the `.slide-meta` container):

| Slot | HTML Element | Example |
|------|-------------|---------|
| Author | `.slide-meta .author` | `Research Team` |
| Affiliation | `.slide-meta .affiliation` | `ETH Zürich` |
| Date | `.slide-meta .date` | `2026-02-24` |

### Deck Review Template

For reviewing multiple slides together, use `deck-template.html`:

- Wraps individual slides in a scrollable vertical layout
- Keyboard navigation: ↑↓←→ arrows and space bar
- Dark mode: follows OS preference via `prefers-color-scheme`
- Mobile responsive: single-column layout on screens < 800px

### HTML Template Library (13 files)

Individual slide templates in `templates/html/`. Use when each slide needs a distinct layout:

| Template | File | Use Case |
|----------|------|----------|
| Title | `slide-title.html` | Cover slide — title, subtitle, author, date |
| Content | `slide-content.html` | Standard bullets or text body |
| Two-Column | `slide-two-column.html` | Side-by-side content areas |
| Image Left | `slide-image-left.html` | Image left, text right |
| Image Right | `slide-image-right.html` | Image right, text left |
| Quote | `slide-quote.html` | Pull quote or highlight statement |
| Data | `slide-data.html` | Chart or data visualization placeholder |
| Agenda | `slide-agenda.html` | Table of contents, section overview |
| Section | `slide-section.html` | Section break divider |
| Comparison | `slide-comparison.html` | Side-by-side comparison (A vs B) |
| Timeline | `slide-timeline.html` | Chronological sequence or process steps |
| Team | `slide-team.html` | People, roles, org structure |
| Closing | `slide-closing.html` | Thank you, Q&A invite, next steps |

These supplement the 4-variant `slide-template.html` (title/content/section/split). Use individual templates for full per-slide design control; use `slide-template.html` + Jinja2 for data-driven generation (see Jinja2 example above).

### CSS Theme System (5 themes)

Themes in `templates/html/themes/`. Apply via `<link rel="stylesheet" href="themes/{name}.css">` inside any template.

| Theme | File | Tone | Best For |
|-------|------|------|----------|
| Executive | `executive.css` | Formal, navy/gold | Board decks, C-suite, governance |
| Corporate | `corporate.css` | Professional, blue | Business reviews, client-facing |
| Sage | `sage.css` | Calm, green | Sustainability, nature, ESG topics |
| Modern Dark | `modern-dark.css` | Tech, dark background | Developer talks, SaaS, API demos |
| Warm | `warm.css` | Friendly, warm tones | Creative, marketing, education |

Default: no theme applied = base styles from `slide-template.html`. Themes override CSS variables only — layout and structure are unchanged.

---

## Phase 0.5: Style Preview (--preview)

Run this phase only when `--preview` is explicitly specified. If no `--preview` flag is present, skip this phase entirely and keep default behavior unchanged.

Before full deck generation:

1. Parse the user's topic and stated mood (if given).
2. Resolve mood to **3 style presets** using the mood→preset mapping from `presentation-design-styles`.
3. Generate 3 single-slide HTML previews and save them to:
   - `.claude-design/slide-previews/preview-1.html`
   - `.claude-design/slide-previews/preview-2.html`
   - `.claude-design/slide-previews/preview-3.html`
4. Each preview must be a fully self-contained HTML file that applies the selected preset via CSS variables.
5. Present the three previews to the user for style selection.
6. Use the user-selected preset as the style baseline for full generation.

Notes:
- This is an opt-in exploration gate, not the default path.
- Do not proceed to full generation style-lock until a preset is selected (or user explicitly opts out after preview).

## Phase 5.5: Refinement Loop (--refine)

Run this phase only when `--refine` is explicitly specified. If no `--refine` flag is present, skip refinement entirely.

After full generation:

1. Render all slides to images (use visual QA skill Path A or Path B).
2. Inspect rendered output against `references/design-principles.md` Section J.11 checklist plus anti-slop heuristics.
3. If issues are found, fix only affected slides and regenerate output.
4. Re-render and re-inspect after fixes; allow **max 2 iterations** total.
5. Report final QA verdict as PASS or FAIL with concrete issue details.

Verification separation (required):
- Producer ≠ verifier.
- The generating agent must not be the final visual inspector.
- Delegate inspection to `slide-qa` agent for independent QA judgment.


## Reference Files (Load by Phase)

- `references/engine-marp.md` — Section B (Marp CLI)
- `references/engine-md2pptx.md` — Section C (md2pptx)
- `references/engine-pptx.md` — Section D (python-pptx + SlideFactory)
- `references/engine-revealjs.md` — Section E (reveal.js)
- `references/engine-beamer.md` — Section F (Beamer LaTeX)
- `references/engine-html.md` — Sections G + H (Standalone HTML + RISE)
- `references/poster-design.md` — Section I (tikzposter)
- `references/design-principles.md` — Section J (presentation intelligence)
- `references/validation-patterns.md` — Section K (validation and delivery gate)
