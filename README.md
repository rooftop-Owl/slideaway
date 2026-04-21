# 🎯 Slideaway

<p align="center">
  <img src="https://img.shields.io/badge/version-2.5.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/engines-7-green?style=for-the-badge" alt="7 Engines">
  <img src="https://img.shields.io/badge/styles-30-purple?style=for-the-badge" alt="30 Styles">
  <img src="https://img.shields.io/badge/agents-3-red?style=for-the-badge" alt="3 Agents">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/rooftop-Owl/slideaway?style=for-the-badge&color=green" alt="License"></a>
</p>

<p align="center">
  Slides, away from your to-do list.
</p>

---

## Installation

```bash
/plugin marketplace add rooftop-Owl/slideaway
/plugin install slideaway@slideaway-marketplace
```

After installing, the `/slides` command, 3 skills, and 3 agents are immediately available in your Claude Code session. No configuration required — engines degrade gracefully if optional dependencies are missing.


---

## Why Slideaway?

Most presentation tools generate generic AI output. Slideaway enforces quality through architecture:

- **7 engines** — choose the right tool for every context (quick preview vs. polished boardroom deck vs. academic PDF)
- **30 curated styles** — every preset was designed to avoid the "AI generated" look
- **Progressive disclosure** — the core skill is 318 lines; 9 reference files load on demand, keeping context lean
- **Separation of concerns** — generation and QA are handled by different agents


## What's Inside

### Skills

| Skill | Description |
|-------|-------------|
| **slide-generation** | Progressive disclosure core (330 lines) + 15 phase-loaded reference files. 7 engines, audience intelligence, narrative structure, academic talk types, timing guidance, data visualization. |
| **presentation-design-styles** | 30 curated styles across 6 categories. Mood→preset mapping. Anti-AI-slop font/color bans. Design foundations (typography, color theory, layout). |
| **presentation-visual-qa** | Two rendering paths (wkhtmltoimage + Playwright). Inspection checklist. PASS/FAIL verdicts. Delivery intelligence. Automated PIL scripts for edge/contrast detection. |

### Agents

| Agent | Role | Phase |
|-------|------|-------|
| **slide-coach** | Discovery & planning — audience analysis, narrative arc, brief, outline | Phase 0 |
| **slide-reviewer** | Content quality — 6-dimension review (message fidelity, narrative, completeness, audience, ask alignment, dual-channel encoding) | Phase 3 |
| **slide-qa** | Design quality — 5-dimension visual QA (readability, aesthetics, conciseness, fidelity, coherence), 3 rounds max | Phase 4 |

### Commands

| Command | Description |
|---------|-------------|
| `/slides` | Main entry point. Flags: `--preview`, `--refine`, `--style <name>` |

**Key flags:**

| Flag | Default | Description |
|------|---------|-------------|
| `--engine` | auto | `marp`, `md2pptx`, `pptx`, `reveal`, `beamer`, `html`, `rise` |
| `--format` | `pptx` | `html`, `pdf`, `pptx`, `notebook`, `all` |
| `--style <name>` | — | Named style preset (e.g., `executive-suite`). Skips style selection. |
| `--preview` | false | Generate 2–3 style previews before full deck (opt-in) |
| `--refine` | false | Auto-inspect and fix issues after generation (opt-in, max 3 rounds). Uses slide-qa agent. |
| `--from` | — | Source file: `.md`, `.tex`, `.pdf`, `.txt`, `.ipynb`. Files >50KB chunked. |
| `--slides` | `10` | Target number of slides |
| `--template` | — | Path to `.pptx` template (for md2pptx or python-pptx) |
| `--academic` | false | Use academic-oriented engine/theme |
| `--interactive` | false | Prefer interactive output (reveal.js) |
| `--output` | `./slides/` | Output directory |

### Tools

| Tool | Purpose |
|------|---------|
| `slide_factory.py` | python-pptx factory with 30 Theme presets |
| `validate_pptx.py` | Structural + style compliance + placeholder detection + `--duration` validation |
| `thumbnail_grid.py` | QA overview grid from slide screenshots |
| `pdf_to_images.py` | PDF→images converter (PyMuPDF) for visual QA workflow |
| `slides_to_pdf.py` | Combine slide images into PDF handouts (Pillow) |
| `html2pptx/` | HTML→PPTX conversion pipeline |
| `pptx_editor/` | XML-level PPTX manipulation (unpack/edit/pack) |
| `md2pptx/` | Markdown→PPTX via bundled md2pptx |

---

## Plugin Structure

```
slides/
├── README.md
├── agents/
│   ├── slide-coach.md          # Phase 0 discovery & planning agent
│   ├── slide-reviewer.md       # Phase 3 content review agent
│   └── slide-qa.md             # Phase 4 visual QA agent
├── commands/
│   └── slides.md               # /slides command definition
│   ├── slide-generation/       # 7-engine workflows + 15 reference files
│   ├── presentation-design-styles/  # 30 styles, anti-patterns, design foundations
│   └── presentation-visual-qa/ # Visual QA, delivery intelligence, automation scripts
├── tools/
│   ├── slide_factory.py        # python-pptx helper (16:9, styling)
│   ├── validate_pptx.py        # Structural PPTX inspection CLI + --duration
│   ├── thumbnail_grid.py       # Slide thumbnail grid generator
│   ├── pdf_to_images.py        # PDF→images (PyMuPDF)
│   ├── slides_to_pdf.py        # Images→PDF combiner (Pillow)
│   ├── html2pptx/              # HTML → PPTX conversion pipeline
│   ├── pptx_editor/            # PPTX editing utilities
│   └── md2pptx/                # Bundled md2pptx (NOT on PyPI)
├── templates/
│   ├── marp/                   # default.css, academic.css, .marprc.yml
│   ├── beamer/                 # 4 templates: metropolis, conference, seminar, defense
│   └── html/                   # slide-template.html, deck-template.html
├── handbook/
│   ├── getting-started.md
│   ├── engine-guide.md
│   └── style-catalog.md        # All 30 styles with descriptions
├── hooks/                      # Plugin lifecycle hooks
├── tests/                      # Test suite
└── .claude-plugin/
    ├── plugin.json
    └── marketplace.json
```
---

## Usage Examples

```
/slides "Quarterly board report on AI adoption metrics"
/slides "PhD defense: climate risk modeling with CLIMADA" --style academic
/slides "Product launch deck for Series B investors" --preview
/slides "Workshop: Introduction to RAG architectures" --refine
/slides "Team retrospective Q1 2026" --style minimalist
```

---

## Architecture

Slideaway v2.3 uses a **multi-agent pipeline** with 7 phases. Two compile-safety gates (Phase 0.1 and Phase 4.5) prevent broken output from reaching delivery.

```
/slides "topic"
    │
    ├─► Phase 0: Discovery (slide-coach)
    │       Audience analysis → narrative arc → brief → outline
    │       Conversational: asks clarifying questions before proceeding
    │
    ├─► Phase 0.1: Environment Gate (HARD GATE)
    │       Verifies engine deps compile before generating content
    │       Beamer: smoke-compiles metropolis + TikZ (5s check)
    │       Fallback routing if engine unavailable
    │
    ├─► Phase 1: Engine Resolution (auto)
    │       Marp │ md2pptx │ python-pptx │ reveal.js │ Beamer │ HTML │ RISE
    │       Resolved from --engine flag, --format, or audience context
    │
    ├─► Phase 2: Content Creation (7 engines)
    │       Style application (30 presets × 6 categories)
    │       Phase-loaded reference files per engine
    │       PostToolUse hook auto-validates .pptx output
    │
    ├─► Phase 3: Content Review (slide-reviewer)
    │       5 dimensions: accuracy, narrative flow, information density,
    │       audience alignment, citation completeness
    │
    ├─► Phase 4: Design Review (slide-qa)
    │       4 dimensions: layout, typography, color harmony, contrast
    │       Up to 3 review rounds (converges or accepts)
    │
    ├─► Phase 4.5: Compile Check (HARD GATE — compilable engines)
    │       Compiles generated output; auto-fix loop (max 2 attempts)
    │       Error classification → targeted preamble fix or known-good fallback
    │       Honest HALT if unresolvable — never claims success on broken output
    │
    └─► Phase 5: Delivery
            Final output + delivery notes (timing, speaker notes, handouts)
```

---

## Engines

| Engine | Best For | Output | Dependencies |
|--------|----------|--------|--------------|
| **Marp** | Quick markdown slides | HTML, PDF, PPTX (image) | marp-cli (npm) |
| **python-pptx** | Programmatic, styled | PPTX (editable) | python-pptx (pip) |
| **md2pptx** | Markdown→PowerPoint | PPTX (editable) | Bundled |
| **reveal.js** | Web presentations | HTML | pandoc |
| **Beamer** | Academic LaTeX | PDF | tectonic (preferred) or pdflatex |
| **HTML** | Zero-dep browser | HTML | None |
| **RISE** | Jupyter notebooks | HTML | Jupyter |

**Engine auto-resolution** (when `--engine` is omitted):

```
--format pptx                → python-pptx + SlideFactory (default)
--format pptx --template X   → md2pptx (template-first)
--format html                → Marp
--format html --interactive  → reveal.js
--format pdf                 → Marp
--format pdf --academic      → Beamer
--format notebook            → RISE
```

---

## Beamer Safety

Beamer's LaTeX pipeline is the most dependency-heavy engine. v2.3 ships two safety gates:

**Phase 0.1 — Environment Gate**: Before generating any content, slideaway smoke-compiles a minimal metropolis + TikZ document. If it fails, you get a distro-specific install guide and engine fallback (Marp PDF) instead of a 30-minute debugging session.

**Phase 4.5 — Compile Check**: After generation, the output `.tex` is compiled and the exit code verified. If compilation fails, an auto-fix loop (max 2 attempts) classifies the error and applies a targeted fix — usually swapping a broken preamble for a known-good one. If unresolvable, slideaway reports the error honestly with the `.tex` source and stops. It never claims success on a file that doesn't build.

**Known-good preambles**: Four tested Beamer preambles ship with the plugin. The generator uses these verbatim — never invents template overrides.

| Template | Theme |
|----------|-------|
| Metropolis (default) | `\usetheme{metropolis}` |
| Conference | `\usetheme{Madrid}\usecolortheme{beaver}` |
| Seminar | `\usetheme{Madrid}\usecolortheme{dolphin}` |
| Defense | `\usetheme{Boadilla}\usecolortheme{whale}` |

Rule: **Theme handles structure. Colors handle branding. Never mix.**

Install tectonic (preferred over pdflatex for conda environments):

```bash
conda install -c conda-forge tectonic   # conda
brew install tectonic                   # macOS
cargo install tectonic                  # cargo
```


## Styles

30 styles across 6 categories. Use `--style <name>` or describe your look and the engine selects the best match.

| Category | Count | Aesthetic |
|----------|-------|-----------|
| **Corporate** | 5 | Professional, brand-safe, boardroom-ready |
| **Academic** | 5 | Clean, readable, conference-appropriate |
| **Creative** | 5 | Bold, expressive, high visual impact |
| **Technical** | 5 | Code-friendly, dark themes, developer-focused |
| **Elegant** | 5 | Minimal, refined, premium feel |
| **Specialty** | 5 | Purpose-built for pitch decks, data stories, workshops |

Full style descriptions, color palettes, and typography specs: [handbook/style-catalog.md](handbook/style-catalog.md)

Use `--preview` to generate 2–3 style variants before committing to a full deck.

---

## Dependencies

```
Core: pip install python-pptx
QA:   pip install slideaway[qa]       # Pillow + PyMuPDF + NumPy
Full: pip install slideaway[all]      # QA + Playwright
```

**Python optional packages** (via `pip install slideaway[qa]`):

| Package | Version | Purpose |
|---------|---------|---------|
| `Pillow` | ≥10.0.0 | Thumbnail grids, slides_to_pdf.py, PIL automation scripts |
| `pymupdf` | ≥1.23.0 | pdf_to_images.py (PDF page → image conversion) |
| `numpy` | ≥1.24.0 | Visual QA automation scripts (edge detection, contrast) |
| `playwright` | ≥1.40.0 | Path B rendering in visual QA skill |

**Optional runtime tools:**

| Tool | Install | Required By |
|------|---------|-------------|
| `marp-cli` | `npm install -g @marp-team/marp-cli` | Marp engine |
| `pandoc` | [pandoc.org](https://pandoc.org/) | reveal.js, Beamer |
| `pdflatex` | TeX Live or MiKTeX | Beamer engine |
| `Chromium` | System package | Marp PDF/PPTX, visual QA |
| `rise` | `pip install rise` | RISE/Jupyter engine |

All dependencies are optional — engines degrade gracefully with install guidance when unavailable.

---

## Philosophy

- **Flags are for agents. Conversation is for humans.** — The `/slides` command uses flags for machine-parseable options; everything else is discovered through dialogue with slide-coach
- **Workflow over Capability** — Models improve; workflow skills get better with them
- **Progressive Disclosure** — 330-line core loads 15 reference files on demand, not everything upfront
- **Producer ≠ Verifier** — slide-coach discovers, engines generate, slide-reviewer and slide-qa inspect independently
- **Anti-AI-Slop** — Banned fonts (Inter, Roboto, Arial), banned colors (#6366f1), distinctive presets enforce visual identity
---

## Inspired By

Slideaway's multi-agent architecture draws from recent advances in automated presentation generation.
**Full provenance with adoption depth, pending items, and tracking dates: [REFERENCES.md](REFERENCES.md)**.

| System | Key Insight | Reference |
|--------|-------------|-----------|
| **PaperBanana** | 5-agent pipeline (analyst → planner → writer → designer → reviewer) proves multi-agent outperforms single-agent for slide generation | [llmsresearch/paperbanana](https://github.com/llmsresearch/paperbanana) |
| **SlideBot** | Cognitive Load Theory (CLT) + CTML as design constraints — managing intrinsic, extraneous, and germane load per slide | Xie et al. (EAAI 2026) — [arXiv:2511.09804](https://arxiv.org/abs/2511.09804) |
| **SlideGen** | Collaborative multimodal generation — LLM + diffusion model + layout optimizer working in concert | Wu et al. (2025) |
| **PPTAgent** | Generation + evaluation as dual concerns — PPTEval framework (Content, Design, Coherence) | Zheng et al. (EMNLP 2025) — [arXiv:2501.03936](https://arxiv.org/abs/2501.03936) |
| **PPTArena** | Benchmark for agentic PowerPoint editing — edit-in-place workflows | Gandhi et al. (ICLR 2026 under review) — [arXiv:2512.03042](https://arxiv.org/abs/2512.03042) |
| **corazzon/pptx-design-styles** | 30 design style presets with structured palettes and typography | [corazzon/pptx-design-styles](https://github.com/corazzon/pptx-design-styles) |

Design theory: Duarte (2008, 2010), Minto (1987), Sweller (1988), Mayer (2009), Tufte (1983). See [REFERENCES.md](REFERENCES.md) for details.

Slideaway adapts these patterns for the Claude Code plugin ecosystem: agents are skills + system prompts (not fine-tuned models), the pipeline is flag-driven (not API-driven), and quality gates are iterative (up to 3 rounds, not single-pass).

---

## Contributing

1. Fork → branch → PR
2. Keep skills under 400 lines (use phase-loading for depth)
3. New styles must pass the anti-slop checklist in `presentation-design-styles`
4. Run `python3 tools/validate_pptx.py` on any PPTX output before submitting

---

## License

MIT © rooftop-Owl

---

## Star History

[![Star History](https://api.star-history.com/svg?repos=rooftop-Owl/slideaway&type=Date)](https://star-history.com/#rooftop-Owl/slideaway&Date)
