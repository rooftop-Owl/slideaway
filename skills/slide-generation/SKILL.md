---
triggers: [marp, marp slides, marp deck, slide deck, generate slides, generate presentation, pptx generation, editable pptx, editable powerpoint, make slides, create presentation, beamer talk, reveal slides, html slides, conference poster, academic poster]
domains: [research, presentation, communication, output]
name: slide-generation
description: Use when generating slide presentations, posters, or visual output. Multi-agent pipeline with discovery-first Phase 0 (slide-coach), 7 engines, content review (slide-reviewer), and visual QA (slide-qa). Supersedes basic presentation skill.
version: "2.2.0"
success_criteria: ["slide brief approved before generation", "engine selected appropriately", "content generated in target format", "content review passed", "design review passed", "output validated"]
---

# Slide Generation — Progressive Disclosure Armory

Multi-agent pipeline. 7 engines. Discovery-first. Every deck starts with a Slide Brief and ends with independent QA.

## Phase Flow Overview

```
Phase 0: Discovery (MANDATORY — slide-coach)
  0a. Signal parsing (silent — infer from topic)
  0b. Completeness check (Tier 1/2/3)
  0c. Smart gap-fill (AskUserQuestion, max 3 questions)
  0d. Slide Brief assembly (load slide-brief-schema.md)
  0e. Outline generation + approval gate
  HARD GATE: no Phase 1 until brief + outline approved

Phase 0.1: Environment gate (MANDATORY — verify engine deps work)

Phase 1: Engine resolution (auto from brief — never shown to user)
  1.5. Optional style preview gate (--preview)

Phase 2: Content creation (orchestrating agent + slide-generation skill)

Phase 3: Content review (slide-reviewer → fix if REVISE)

Phase 4: Design review (slide-qa → iterative loop, max 3 rounds)

Phase 4.5: Post-generation compile check (HARD GATE — compilable engines only)
  HARD GATE: no Phase 5 (delivery) until compile succeeds or failure reported honestly

Phase 5: Delivery report
```

**Default human path**: Conversational Phase 0 → automated Phases 1–5.
**Agent-to-agent path**: `--no-coach` with explicit brief → skip Phase 0 → Phases 1–5.

## Phase-Loading Rules

### Phase 0 — Discovery (slide-coach)
When the slide-coach agent is invoked for Phase 0, it MUST load:
- `references/slide-brief-schema.md` — typed contract for the Slide Brief
- `references/talk-types.md` — presentation type taxonomy for signal parsing
- `references/timing-guidelines.md` — duration → slide count calibration
- `../presentation-design-styles/references/design-foundations.md` — typography, color theory, layout composition
- `presentation-design-styles` skill — ALWAYS loaded for style selection (30 presets, mood→preset mapping, anti-slop rules)

### Phase 1 — Engine Resolution
When generating with a specific engine, you MUST read the corresponding reference file:
- Marp output → read `references/engine-marp.md`
- md2pptx output → read `references/engine-md2pptx.md`
- python-pptx output → read `references/engine-pptx.md`
- reveal.js output → read `references/engine-revealjs.md`
- Beamer/LaTeX output → read `references/engine-beamer.md`
- HTML/RISE output → read `references/engine-html.md`
- Poster output → read `references/poster-design.md`
- `--preview` enabled → run Phase 1.5 and read mood→preset mapping from `presentation-design-styles` skill before full generation

### Phase 2 — Content Creation
- For ALL outputs → read `references/design-principles.md` (presentation intelligence)
- Academic/scientific talk type specified (conference/seminar/defense/grant/journal-club) → read `references/talk-types.md`
- User specifies duration OR asks about timing/practice → read `references/timing-guidelines.md`
- Creating data-heavy slides with charts, plots, or figures → read `references/data-visualization.md`
- Need design theory (why certain typography/color/layout choices) → read `../presentation-design-styles/references/design-foundations.md`

### Phase 3 — Content Review (slide-reviewer)
- `references/design-principles.md` Section J — presentation intelligence (J.1 purpose, J.2 audience, J.3 narrative, J.4 volume)
- `../presentation-visual-qa/references/delivery-intelligence.md` — timing, pacing, delivery context
- `references/talk-types.md` — talk type taxonomy for structure matching

### Phase 4 — Design Review (slide-qa)
- `../presentation-visual-qa/references/visual-qa-automation.md` — rendering paths, PIL automation scripts, issue log, stopping criteria
- `../presentation-visual-qa/references/delivery-intelligence.md` — slide design for delivery support
- Before delivery → read `references/validation-patterns.md`

### Phase 4.5 — Compile Check
- Applies only to compilable engines: Beamer (`.tex`), Marp (`.md`)
- ALWAYS load `references/engine-beamer.md` during Phase 4.5 for Beamer — the anti-patterns and known-good preambles are required for auto-fix
- PPTX engines (python-pptx, md2pptx): no compile step — `validate_pptx.py` in Phase 4 already covers structural validation

### Legacy Rules (still apply)
- Evaluating whether slides support delivery (opening/closing/transitions/Q&A) → delegate to `slide-qa` agent with `../presentation-visual-qa/references/delivery-intelligence.md`
- Reviewing rendered slides OR using pdf_to_images.py → load `../presentation-visual-qa/references/visual-qa-automation.md`; NEVER read PDF files directly

---

## Phase 0: Discovery (MANDATORY)

> **HARD GATE**: Phase 1 (engine resolution) CANNOT start until the Slide Brief + outline are approved. No exceptions. Bad decks come from skipped planning, not bad engines.

Phase 0 is owned by the **slide-coach** agent. The orchestrating agent MUST delegate to slide-coach before any generation begins.

### Delegation Pattern (Phase 0)

```
task(
  subagent_type="hephaestus",
  description="Phase 0: slide discovery and brief",
  prompt="""
    You are the slide-coach. Load the slide-generation skill and the
    presentation-design-styles skill. Run Phase 0 discovery for:

    Topic: "{user_topic}"
    Flags: {flags}

    Follow the 6-step Phase 0 pipeline (0a–0f) from slide-coach.md.
    Output: approved Slide Brief + slide-by-slide outline.
    HARD GATE: do NOT proceed to generation.
  """,
  run_in_background=false
)
```

### Phase 0 Steps (Summary — full detail in slide-coach.md)

| Step | Name | Action |
|------|------|--------|
| 0a | Signal Parsing | Silent inference from topic string — audience, type, duration, formality, domain, narrative structure |
| 0b | Completeness Check | Classify as Tier 1 (rich), Tier 2 (moderate), or Tier 3 (sparse) |
| 0c | Smart Gap-Fill | Ask ≤3 natural questions via AskUserQuestion. Bias toward Tier 1 — infer when possible. |
| 0d | Brief Assembly | Fill all required fields from `references/slide-brief-schema.md`. Run anti-slop check. |
| 0e | Outline Generation | Slide-by-slide outline following the selected narrative structure |
| 0f | Approval Gate | Present brief + outline. Wait for explicit "go" before Phase 1. |

### Beamer Template Selection (Phase 0d)

When the brief's presentation type maps to Beamer output, select the template during brief assembly:

| Talk Type | Beamer Template | Rationale |
|-----------|----------------|-----------|
| `conference` | `templates/beamer/conference/` | Conference-optimized: section frames, bibliography, affiliation |
| `seminar` | `templates/beamer/seminar/` | Seminar-optimized: longer form, discussion prompts |
| `defense` | `templates/beamer/defense/` | Defense-optimized: committee-facing, appendix-ready |
| All other academic | `templates/beamer/metropolis/` | Clean default: metropolis theme, minimal chrome |

Record the selected template in the Slide Brief's `engine_hints.beamer_template` field so Phase 1 uses it directly.

### Duration Capture (Phase 0)

Duration MUST be captured during Phase 0 (Step 0a inference or Step 0c question) and recorded in the Slide Brief's `timing.duration_minutes` field. This value flows downstream to:
- **Phase 2**: slide count calibration (via timing-guidelines.md)
- **Phase 4**: `validate_pptx.py --duration {duration}` for structural validation

If the user does not specify duration and it cannot be inferred, default to 15 minutes and note the assumption in the brief.

---

## --no-coach Mode (Backward Compatibility)

When `--no-coach` is present, skip Phase 0 entirely. This is the legacy v2.0/v2.1 path for programmatic or agent-to-agent use.

**Behavior**:
1. Use provided flags for engine (`--engine`), style (`--style`), duration (`--slides`), format (`--format`)
2. Skip slide-coach invocation — no discovery, no brief, no approval gate
3. Proceed directly to Phase 1 (engine resolution) using the flag-based decision matrix
3.5. Run **Phase 0.1 (Environment Gate)** — this applies even on `--no-coach` path. Verify the selected engine's deps work before generating content.
4. Phases 3–4 (content review, design review) still run unless explicitly skipped

**When to use**: Automated pipelines, agent-to-agent delegation with pre-computed parameters, or users who want direct engine control without the conversational flow.

**Philosophy**: Flags are for agents. Conversation is for humans. The default human path is always Phase 0.

---

## Phase 0.1: Environment Gate (MANDATORY after engine resolution)

After Phase 0 selects an engine (or --no-coach path specifies one), verify the engine's dependencies actually work BEFORE generating any content.

### Why This Gate Exists

Without this check, the pipeline generates hundreds of lines of engine-specific code (e.g., 800+ lines of LaTeX) only to fail at compile time. Debugging broken TeX installations costs 30-60 minutes. The gate catches this in 5 seconds.

### How It Works

1. Look up the selected engine in `module.json` → `dependencies.runtime` → `check` command
2. Run the check command. If it fails → suggest installation (see `engine-beamer.md` Installation Guide) or offer engine fallback
3. For Beamer specifically: run the **smoke test** from `engine-beamer.md` → Environment Gate section (minimal metropolis + TikZ compile)
4. If smoke test fails → suggest `--engine marp --format pdf` as zero-dependency alternative
5. Only proceed to Phase 2 (generation) after the gate passes

### Engine Fallback Table

| Failed Engine | Fallback | Flag Override |
|---------------|----------|---------------|
| Beamer (no pdflatex/tectonic) | Marp PDF | `--engine marp --format pdf` |
| Marp (no marp-cli) | Standalone HTML | `--engine html` |
| reveal.js (no pandoc) | Marp HTML | `--engine marp --format html` |
| RISE (no Jupyter) | Standalone HTML | `--engine html` |
| python-pptx (no pptx module) | md2pptx (bundled) | `--engine md2pptx` |

**The agent should suggest the fallback naturally** ("Beamer isn't available on this system — I'll use Marp to generate a PDF instead"), not ask the user to install packages.

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
| Academic conference | Beamer | `tectonic slides.tex` (preferred) or `pdflatex slides.tex` |
| Full design control | Standalone HTML | Individual HTML files |
| Live code demo | RISE/Jupyter | Jupyter + RISE extension |
| Modern PDF handout | Marp | `marp slides.md --pdf` |
| Corporate template with exact positioning | python-pptx + SlideFactory | Template-based Python script |
| Academic poster | tikzposter | `tectonic poster.tex` (preferred) or `pdflatex poster.tex` |

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

"Project Name"\n"Subtitle or tagline"\n"Author / Team"\n"2026-02-23"

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

## Phase 1.5: Style Preview (--preview)

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

---

## Phase 3: Content Review (slide-reviewer)

After generation (Phase 2), delegate to the **slide-reviewer** agent for content quality verification. This is a distinct step from visual QA — it checks messaging, narrative, and audience calibration against the Slide Brief.

### Delegation Pattern (Phase 3)

```
task(
  subagent_type="hephaestus",
  description="Phase 3: content review against brief",
  prompt="""
    You are the slide-reviewer. Load the slide-generation skill.
    
    Review the generated deck at: {output_path}
    Against the Slide Brief at: {brief_path}
    
    Evaluate all 5 dimensions: message fidelity, narrative coherence,
    completeness, audience calibration, ask alignment.
    
    Output: CONTENT REVIEW verdict (PASS or REVISE with per-slide notes).
    If REVISE: provide specific revision instructions per slide.
  """,
  run_in_background=false
)
```

### Verdict Handling
- **PASS** → proceed to Phase 4 (design review)
- **REVISE** → apply revision instructions, regenerate affected slides, re-run Phase 3 (max 3 iterations)

---

## Phase 4: Design Review (slide-qa)

After content review passes, delegate to the **slide-qa** agent for visual quality assurance. This is an iterative loop with convergence guardrails.

### Phase 4.5 — Post-Generation Compile Check (HARD GATE)

For engines that produce compilable source files (Beamer `.tex`, Marp `.md`), **compile the generated output and check the exit code BEFORE visual inspection or delivery**. If compilation fails, do NOT claim success — report the failure honestly with the raw error.

> **Why**: Phase 0.1 verifies the TeX environment compiles *anything*. Phase 4.5 verifies *this specific output* compiles. They are complementary, not redundant. A correct environment with a broken preamble will pass Phase 0.1 and fail Phase 4.5.

#### Compile Commands

```bash
# Beamer (.tex) — preferred engine
tectonic slides.tex

# Beamer (.tex) — fallback if tectonic unavailable
pdflatex -halt-on-error -interaction=nonstopmode slides.tex

# Marp (.md)
npx @marp-team/marp-cli slides.md --html --allow-local-files
```

#### Auto-Fix Retry Loop (max 2 attempts)

If compilation fails:

1. **Parse the error log** — classify the failure:

| Error Pattern | Likely Cause | Auto-Fix Strategy |
|---------------|-------------|-------------------|
| `\tikzscope@linewidth undefined` | PGF scope corruption | Remove `\setbeamertemplate` overrides; use known-good preamble |
| `File '*.sty' not found` | Missing package | Add `\usepackage{pkg}` or switch to known-good preamble |
| `Undefined control sequence \setbeamertemplate` | Anti-pattern in preamble | Replace with `\setbeamercolor` equivalent |
| `Emergency stop` / `Fatal error` | Preamble syntax error | Revert to known-good preamble verbatim |
| Font not found | Missing font package | Replace with standard LaTeX font |

2. **Apply fix** — for known error patterns:
   - Replace broken preamble section with the corresponding known-good preamble from `references/engine-beamer.md`
   - Do NOT invent new template overrides — always fall back to a known-good preamble
   
3. **Recompile** — check exit code again

4. **Repeat** up to 2 total fix attempts (3 total compile attempts: original + fix 1 + fix 2)

#### HALT Path (honest failure reporting)

If all attempts fail, **DO NOT** claim the output is valid. Report honestly:

```
Phase 4.5 — Compilation FAILED after 2 fix attempts.

Engine: tectonic
Error (last attempt): [paste the relevant error lines — max 10 lines]

Deliverables:
  ✅ slides.tex — source file (uncompiled)
  ❌ slides.pdf — not generated

Recommended next steps:
  1. Inspect slides.tex preamble — compare against known-good preamble in engine-beamer.md
  2. Run manually: tectonic slides.tex
  3. Share the error output to debug further
```

**Never**: claim `validation passed`, `slides generated`, or report a success summary when the output did not compile.

> **The `--refine` flag and visual QA are meaningless if the source doesn't compile.** Phase 4.5 is the gate that makes Phase 4 visual QA trustworthy.

### Explicit validate_pptx.py Call (MANDATORY)

In Phase 4, **ALWAYS** run `validate_pptx.py` explicitly before visual inspection. Do NOT rely solely on the PostToolUse hook, which misses Bash-generated PPTX files:

```bash
python3 modules/slides/tools/validate_pptx.py output.pptx --duration {duration_from_brief}
```

Replace `{duration_from_brief}` with the target presentation duration from the Slide Brief's `timing.duration_minutes` field (e.g., `15` for a 15-minute talk). If no duration is specified in the brief, omit the `--duration` flag.

### Delegation Pattern (Phase 4)

```
task(
  subagent_type="hephaestus",
  description="Phase 4: visual QA inspection",
  prompt="""
    You are the slide-qa agent. Load the presentation-visual-qa skill.
    
    1. Run structural pre-check:
       python3 modules/slides/tools/validate_pptx.py {output_path} --duration {duration}
    
    2. Render all slides to images (Path A or B per skill).
    
    3. Run the full visual inspection checklist.
    
    4. Score across 4 dimensions: Readability, Aesthetics, Conciseness, Fidelity.
    
    5. Issue verdict: PASS (all ≥4), ITERATE (fixable), or HALT (needs content changes).
    
    If ITERATE: fix visual issues and re-inspect (max 3 rounds total).
    If HALT: report trade-offs and recommend next steps.
    
    Slide Brief at: {brief_path}
    Output deck at: {output_path}
  """,
  run_in_background=false
)
```

### Verdict Handling
- **PASS** → proceed to Phase 5 (delivery)
- **ITERATE** → slide-qa fixes visual issues and re-inspects (up to 3 rounds, with convergence rule)
- **HALT** → report trade-offs to user. May route back to slide-reviewer for content changes or regenerate with different engine.

---

## Phase 5: Delivery & Refinement

### Standard Delivery
After Phase 4 PASS, deliver the deck with:
1. Output file path
2. Slide count and duration estimate
3. Phase 3 content review summary
4. Phase 4 design review summary (final scores)
5. Any caveats or known limitations

### Refinement Loop (--refine)

Run this phase only when `--refine` is explicitly specified. If no `--refine` flag is present, skip refinement entirely.

After full generation:

1. Render all slides to images (use visual QA skill Path A or Path B).
2. Inspect rendered output against `references/design-principles.md` Section J.11 checklist plus anti-slop heuristics.
3. If issues are found, fix only affected slides and regenerate output.
4. Re-render and re-inspect after fixes; allow **max 3 rounds** total.
5. Report final QA verdict as PASS, ITERATE, or HALT with concrete issue details.

Verification separation (required):
- Producer ≠ verifier.
- The generating agent must not be the final visual inspector.
- Delegate inspection to `slide-qa` agent for independent QA judgment.


## Reference Files (Load by Phase)

- `references/slide-brief-schema.md` — Typed contract for Slide Brief (Phase 0)
- `references/engine-marp.md` — Section B (Marp CLI)
- `references/engine-md2pptx.md` — Section C (md2pptx)
- `references/engine-pptx.md` — Section D (python-pptx + SlideFactory)
- `references/engine-revealjs.md` — Section E (reveal.js)
- `references/engine-beamer.md` — Section F (Beamer LaTeX). 4 templates available: metropolis, conference, seminar, defense
- `references/engine-html.md` — Sections G + H (Standalone HTML + RISE)
- `references/poster-design.md` — Section I (tikzposter)
- `references/design-principles.md` — Section J (presentation intelligence)
- `references/validation-patterns.md` — Section K (validation and delivery gate)
- `references/talk-types.md` — Per-type depth (extends J.1)
- `references/timing-guidelines.md` — Operational timing guidance (extends J.4)
- `references/data-visualization.md` — Chart types and figure preparation
- `../presentation-design-styles/references/design-foundations.md` — Typography, color theory, layout composition
- `../presentation-visual-qa/references/delivery-intelligence.md` — Slide design for delivery support
- `../presentation-visual-qa/references/visual-qa-automation.md` — PIL automation scripts, issue log, stopping criteria
