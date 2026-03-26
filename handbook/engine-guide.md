# Engine Selection Guide

The slides module ships 7 engines. This guide helps you pick the right one for your use case.

---

## Decision Matrix

| Engine | Best For | Output | Dependencies | Editable? |
|--------|----------|--------|--------------|-----------|
| **python-pptx** | Default polished decks | PPTX | python-pptx | Yes — fully editable |
| **md2pptx** | Markdown-first PPTX import | PPTX | python-pptx (bundled script) | Yes — editable |
| **Marp** | Quick previews, PDF handouts | HTML / PDF / PPTX* | marp-cli (npm) | PDF only |
| **reveal.js** | Web presentations, animations | Interactive HTML | pandoc or npx | Source only |
| **Beamer** | Academic talks, equations | PDF | pdflatex | Source only |
| **Standalone HTML** | Full design control, version-controllable | HTML files | None | Source only |
| **RISE** | Live code demonstrations | Jupyter notebook | rise (pip) | Notebook |

*Marp PPTX output embeds slides as images — not editable text.

---

## Engine Profiles

### python-pptx — The Default

**Use when**: You need a polished, presentation-ready deck that someone will open in PowerPoint
or Keynote and possibly edit.

**Strengths**:
- Fully editable PPTX with real text, not images
- 16:9 aspect ratio, styled headers and footers
- Bullet formatting, image fitting handled automatically
- Powered by `SlideFactory` — production-ready helper

**Limitations**:
- Requires `pip install python-pptx`
- Less control over individual slide layout than raw python-pptx scripting

**Example**:
```bash
/slides "Product Roadmap Q4"
# → product-roadmap-q4.pptx (styled, editable)
```

---

### md2pptx — Markdown-First PPTX

**Use when**: You already have content in Markdown and want an editable PPTX with minimal
configuration. Good for converting notes or documents into decks.

**Strengths**:
- Markdown in → PPTX out, simple pipeline
- Template-first: inherits slide master styles
- Bundled — no PyPI install needed (just `python-pptx`)

**Limitations**:
- Less styling control than python-pptx engine
- Layout options constrained by template

**Example**:
```bash
python3 modules/slides/tools/md2pptx/md2pptx.py output.pptx < slides.md
```

> **Critical**: Do NOT run `pip install md2pptx`. The script is at
> `modules/slides/tools/md2pptx/md2pptx.py` and is NOT on PyPI.

---

### Marp — Quick Preview & PDF

**Use when**: You want a fast HTML preview or a clean PDF handout. Great for sharing before
a meeting or distributing printed notes.

**Strengths**:
- Instant HTML output from Markdown
- High-quality PDF via headless Chromium
- Custom CSS themes supported (see `templates/marp/`)
- Bespoke presenter mode

**Limitations**:
- Requires `npm install -g @marp-team/marp-cli`
- PDF/PPTX output requires Chromium installed
- PPTX output embeds slides as images (not editable text)

**Example**:
```bash
marp slides.md -o slides.html          # HTML preview
marp slides.md --pdf -o slides.pdf     # PDF handout
```

---

### reveal.js — Interactive Web Presentations

**Use when**: You're presenting in a browser and want animations, speaker notes, or embedded
interactive content. Good for conference talks with a projector.

**Strengths**:
- Keyboard navigation, speaker notes, fullscreen
- Animations and transitions
- Self-contained HTML — share as a single file
- Embed code, iframes, videos

**Limitations**:
- Requires pandoc (or npx reveal.js)
- Not editable in presentation software
- Larger file size than PDF

**Example**:
```bash
pandoc slides.md -t revealjs -s -o slides.html --embed-resources
```

---

### Beamer — Academic LaTeX PDF

**Use when**: You're giving a conference talk or academic presentation with equations, theorems,
or citations. Produces publication-quality PDF.

**Strengths**:
- Full LaTeX typesetting — equations, symbols, bibliography
- Metropolis theme included (`templates/beamer/metropolis-template.tex`)
- Professional academic appearance
- Consistent with paper formatting

**Limitations**:
- Requires pdflatex (TeX Live or MiKTeX)
- Slower compilation than other engines
- Not editable in presentation software

**Example**:
```bash
pdflatex slides.tex
# or via /slides:
/slides "Bayesian Inference Tutorial" --engine beamer
```

---

### Standalone HTML — Zero Dependencies

**Use when**: You need full design control, want version-controllable slides, or are deploying
to a web server. No tools required — just a browser.

**Strengths**:
- Zero external dependencies
- 4 layout variants: title, content, section, split
- Full CSS control
- Works offline, version-controllable in git

**Limitations**:
- Manual HTML authoring required for custom layouts
- No Markdown input (write HTML directly or use template)

**Template**: `modules/slides/templates/html/slide-template.html`

---

### RISE — Live Jupyter Notebooks

**Use when**: Your presentation involves live code execution, data exploration, or interactive
demos. The audience watches you run code in real time.

**Strengths**:
- Execute code cells during the presentation
- Show live plots, model outputs, data frames
- Notebook is the source of truth — no separate slide file

**Limitations**:
- Requires `pip install rise` and Jupyter
- Presentation tied to a running Jupyter server
- Not suitable for pre-recorded or offline delivery

**Example**:
```bash
pip install rise
jupyter notebook my-demo.ipynb
# Press Alt+R to enter presentation mode
```

---

## Quick Decision Flowchart

```
Need editable PPTX?
  ├─ Yes, from Markdown → md2pptx
  └─ Yes, styled/programmatic → python-pptx (default)

Need PDF?
  ├─ Academic / equations → Beamer
  └─ Modern / quick → Marp

Need HTML?
  ├─ Interactive / animations → reveal.js
  ├─ Zero dependencies → Standalone HTML
  └─ Live code demo → RISE
```

---

## Fallback Behavior

If your requested engine is unavailable, the module will:

1. Report the missing dependency with the exact install command
2. Offer the nearest available fallback engine
3. Never silently fail

Example: Marp not installed → suggests md2pptx for PPTX or Standalone HTML for zero-dep output.
