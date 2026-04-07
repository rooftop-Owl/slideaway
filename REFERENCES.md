# References & Provenance

> Maintainer document. Tracks every external source that influenced slideaway's architecture,
> design intelligence, and evaluation methodology — with adoption depth, pending items, and
> last-checked dates so upstream progress can be followed systematically.
>
> **Update protocol**: When adopting or reviewing an external pattern, update the relevant
> entry here. When adding a new source, follow the entry template at the bottom.

---

## Academic Papers

### PPTAgent — Edit-Based Generation + PPTEval

- **Paper**: *PPTAgent: Generating and Evaluating Presentations Beyond Text-to-Slides*
- **Authors**: Zheng, Guan, Kong, Zheng, Zhou, Lin, Lu, He, Han, Sun (ISCAS / UCAS)
- **Venue**: EMNLP 2025 (submitted Jan 2025, revised Feb 2025 v3)
- **ArXiv**: https://arxiv.org/abs/2501.03936
- **Code**: https://github.com/icip-cas/PPTAgent
- **Dataset**: Zenodo10K — 10,448 presentations from Zenodo (public, multi-domain)

#### What We Adopted

| Pattern | Where in Slideaway | Notes |
|---------|--------------------|-------|
| Dual generation + evaluation concern separation | `slide-reviewer` (content) + `slide-qa` (design) as independent agents | Core architectural principle: Producer ≠ Verifier |
| Structured outline before generation | Phase 0 Slide Brief + outline → approval gate before Phase 1 | PPTAgent generates outline entries with reference slides; we generate a Slide Brief with schema |
| Self-correction on failure | Phase 4.5 compile check → auto-fix loop (max 2 attempts) | PPTAgent uses REPL feedback; we use compile error classification + known-good preamble swap |

#### What We Haven't Adopted (Pending Review)

| Pattern | Description | Relevance | Priority |
|---------|-------------|-----------|----------|
| **PPTEval Coherence dimension** | Deck-level evaluation: do all slides structurally belong together? Structural roles (opening/section/closing) visually distinct from content slides? | **High** — our slide-qa scores 4 per-slide dimensions but has no cross-deck coherence metric | Next version |
| **Edit-based generation** | Instead of creating slides from scratch, analyze reference presentations → extract functional types + content schemas → generate editing actions on reference slides | **Medium** — fundamentally different paradigm; would require template library | Evaluate feasibility |
| **Slide clustering / functional typing** | Categorize slides into structural (opening, section break, closing) vs. content (bullet-point, data, diagram) types before generation | **Medium** — could improve layout archetype selection in Phase 2 | Evaluate |
| **REPL-based self-correction** | Execute editing actions in REPL; failures feed back to LLM for refinement (vs. our error-classification approach) | **Low** — our compile-check loop serves similar purpose for Beamer | Monitor |
| **Zenodo10K dataset** | 10,448 multi-domain presentations for benchmarking | **Low** — useful if we build eval harness | Future |

- **Last checked**: 2026-04-07
- **Next check**: When planning v2.4 — review v3 paper for new evaluation criteria

---

### SlideBot — CLT + CTML Multi-Agent Framework

- **Paper**: *SlideBot: A Multi-Agent Framework for Generating Informative, Reliable, Multi-Modal Presentations*
- **Authors**: Xie, Waterfield, Kennedy, Zhang (University of Virginia)
- **Venue**: EAAI 2026 (accepted Nov 2025)
- **ArXiv**: https://arxiv.org/abs/2511.09804
- **Code**: Not publicly released as of last check

#### What We Adopted

| Pattern | Where in Slideaway | Notes |
|---------|--------------------|-------|
| Multi-agent pipeline concept | slide-coach → orchestrator → slide-reviewer → slide-qa | SlideBot uses retriever + summarizer + figure-gen + formatter; our roles differ but the multi-agent principle is shared |
| CLT as a conceptual reference | Referenced in digests and enhancement tracking | Conceptual awareness only — not yet operationalized |

#### What We Haven't Adopted (Pending Review)

| Pattern | Description | Relevance | Priority |
|---------|-------------|-----------|----------|
| **CTML dual-channel optimization** | Every slide should encode its core idea in BOTH a verbal channel (text/title) AND a visual channel (figure/diagram/chart). Mayer's Multimedia Principle. | **High** — we have no QA rule checking "does this slide have a visual element or is it text-only?" | Next version |
| **Intrinsic load management** | Structured planning to cap content complexity per slide — not just bullet count but conceptual density | **High** — our 6×6 rule and 3-bullet max are crude proxies; CLT provides a theory-grounded metric | Next version |
| **Extraneous load reduction via visual macros** | Consistent visual patterns (not just anti-slop bans) that reduce cognitive effort: same chart style, same caption placement, same color encoding across the deck | **High** — our anti-slop rules catch bad patterns but we lack positive consistency rules | Next version |
| **Retrieval integration** | External source retrieval for factual grounding of slide content | **Medium** — relevant for research workflows; could integrate with Zotero plugin | Evaluate |
| **Instructor collaboration loop** | Interactive refinement where the instructor reviews and adjusts generated slides iteratively | **Low** — our Phase 0 approval gate serves a similar purpose | Monitor |

- **Last checked**: 2026-04-07
- **Next check**: Monitor for code release and any follow-up paper

---

### PPTArena — Benchmark for Agentic PowerPoint Editing

- **Paper**: *PPTArena: A Benchmark for Computer-Use Agents on PowerPoint Tasks*
- **Authors**: Gandhi, Suryanarayanan, Shaik, Anwar, Desai, Nguyen, Raza, Chowdhary, Neubig (CMU et al.)
- **OpenReview**: https://openreview.net/forum?id=Dl1S4EvFwh
- **ArXiv**: https://arxiv.org/abs/2512.03042 (Dec 2025)
- **Venue**: Under review at ICLR 2026

#### What We Adopted

Nothing yet — discovered 2026-04-07.

#### What We Haven't Adopted (Pending Review)

| Pattern | Description | Relevance | Priority |
|---------|-------------|-----------|----------|
| **Agentic editing benchmark** | Tests computer-use agents on editing *existing* PowerPoint decks — not generating from scratch | **Medium** — signals the field is moving toward edit-in-place workflows | Monitor |
| **Task taxonomy for PPT operations** | Categorizes PPT editing tasks (content update, layout change, style modification, etc.) | **Medium** — could inform a structured slide editing command | Evaluate when published |

- **Last checked**: 2026-04-07
- **Next check**: After ICLR 2026 decisions (expected mid-2026)

---

### SlideGen — Collaborative Multimodal Generation

- **Paper**: *SlideGen: Collaborative Multimodal Slide Generation*
- **Authors**: Wu et al. (2025)
- **ArXiv**: Not confirmed — referenced in README `Inspired By` section
- **Code**: Not publicly available

#### What We Adopted

| Pattern | Where in Slideaway | Notes |
|---------|--------------------|-------|
| Multimodal awareness | `data-visualization.md` reference file; figure handling in content generation | General principle: slides should contain more than text |

#### What We Haven't Adopted (Pending Review)

| Pattern | Description | Relevance | Priority |
|---------|-------------|-----------|----------|
| **Layout optimizer** | Automated spatial optimization of slide elements | **Medium** — we rely on template-based layout; no algorithmic optimization | Future |
| **Diffusion model integration** | Image generation for slide figures | **Low** — out of scope for a Claude Code plugin | Not planned |

- **Last checked**: 2026-04-07
- **Next check**: Low priority — verify paper exists and get ArXiv link

---

## Open-Source Repositories

### PaperBanana — 5-Agent Slide Pipeline

- **Repository**: https://github.com/llmsresearch/paperbanana (1.3k stars)
- **License**: Check repo
- **Key insight**: 5-agent pipeline (analyst → planner → writer → designer → reviewer) proves multi-agent outperforms single-agent for slide generation

#### What We Adopted

| Pattern | Where in Slideaway | Notes |
|---------|--------------------|-------|
| Multi-agent role separation | slide-coach (analyst+planner), orchestrator (writer+designer), slide-reviewer, slide-qa (reviewer) | Our roles are consolidated differently but the separation principle comes from here |
| Discovery-first approach | Phase 0 mandatory discovery before generation | PaperBanana's analyst phase inspired our slide-coach |

#### What We Haven't Adopted (Pending Review)

| Pattern | Description | Relevance | Priority |
|---------|-------------|-----------|----------|
| **OpenRouter multi-provider routing** | Wiki updated Feb 2026 — integrating multi-provider model routing | **Low** — astraeus handles model routing at the platform level | Monitor |

- **Last checked**: 2026-04-07 (wiki activity detected Feb 2026)
- **Next check**: Quarterly — check releases and wiki for architectural changes

---

### corazzon/pptx-design-styles — Design Style System

- **Repository**: https://github.com/corazzon/pptx-design-styles
- **License**: Check repo
- **Key insight**: Structured design presets with palette, typography, and layout principles

#### What We Adopted

| Pattern | Where in Slideaway | Notes |
|---------|--------------------|-------|
| Style preset structure | `presentation-design-styles` skill — 30 named styles | Adapted and expanded significantly; original presets were the seed |
| 7-value color palette per style | `styles.md` — Primary, Secondary, Accent, Background, Text Primary, Text Secondary, Border | Format matches their structure |

#### Modifications We Made

- Expanded from their original set to 30 styles across 6 categories
- Added typography pairing (heading/body/caption) per style — not in original
- Added layout principles and anti-patterns per style — not in original
- Added mood→preset mapping for conversational selection

- **Last checked**: 2026-04-07
- **Next check**: Low priority — stable source, unlikely to change significantly

---

### vkehfdl1/slides-grab — Slide Generation Harness + Linter

- **Repository**: https://github.com/vkehfdl1/slides-grab
- **License**: Check repo
- **Key insight**: Dedicated slide linter as a first-class pipeline step (not just visual QA)

#### What We Adopted

Nothing yet — noted in 2026-04-04 digest.

#### What We Haven't Adopted (Pending Review)

| Pattern | Description | Relevance | Priority |
|---------|-------------|-----------|----------|
| **Programmatic slide linter** | Lint rules (bullet count, heading presence, font bans, color violations) as code — runs before visual QA | **High** — our `validate_pptx.py` does structural validation but not content linting | Next version |
| **Harness architecture** | Wraps generation + linting + QA into a repeatable harness | **Medium** — our Phase pipeline is similar conceptually | Evaluate |

- **Last checked**: 2026-04-07
- **Next check**: Check for recent releases/features

---

### zarazhangrui/frontend-slides — Claude Frontend Slide Generation

- **Repository**: https://github.com/zarazhangrui/frontend-slides
- **License**: Check repo
- **Key insight**: Claude-native frontend-first slide generation approach

#### What We Adopted

Nothing yet — noted in digests.

- **Last checked**: 2026-04-07
- **Next check**: Low priority — evaluate if approach is relevant to our engine set

---

## Design Theory & Methodology

### Duarte — Slide:ology + Resonate

- **Sources**:
  - Nancy Duarte, *Slide:ology* (O'Reilly, 2008)
  - Nancy Duarte, *Resonate* (Wiley, 2010)
- **Widely cited**: PPTAgent cites Duarte (2008, 2010) as foundation for their Content/Design/Coherence evaluation dimensions

#### What We Adopted (Uncited Until Now)

| Pattern | Where in Slideaway | Notes |
|---------|--------------------|-------|
| Audience quadrant model (depth × familiarity) | `design-principles.md` J.2 | 4-quadrant audience adaptation — deep/shallow × insider/outsider |
| Narrative structure frameworks | `design-principles.md` J.3 — Hourglass, Pyramid, SCR | Hourglass and SCR models |
| Assertion-Evidence headline pattern | `design-principles.md` J.10 | "State the finding, not the topic" |
| Volume calibration | `design-principles.md` J.4 — 1 slide/minute rule | Duration → slide count mapping |
| Pre-presentation checklist | `design-principles.md` J.11 | Content + visual + narrative validation |

- **Status**: Heavily adopted but **never cited** in any skill or reference file. This is the most significant attribution gap.

---

### Minto — Pyramid Principle

- **Source**: Barbara Minto, *The Pyramid Principle* (Pearson, 1987/2009)
- **Adopted in**: `design-principles.md` J.3 — Pyramid Principle narrative structure
- **Citation**: Referenced as "Minto/McKinsey structure" in J.3 (line 60) — partially cited
- **Status**: Adequately attributed

---

### Sweller — Cognitive Load Theory (CLT)

- **Sources**:
  - Sweller, J. (1988). Cognitive load during problem solving. *Cognitive Science*, 12(2), 257–285.
  - Sweller, J., Ayres, P., & Kalyuga, S. (2011). *Cognitive Load Theory*. Springer.
- **Adopted in**: Referenced conceptually via SlideBot
- **Status**: Name-checked but not operationalized. See SlideBot entry for pending adoption items.

---

### Mayer — Cognitive Theory of Multimedia Learning (CTML)

- **Sources**:
  - Mayer, R. E. (2009). *Multimedia Learning* (2nd ed.). Cambridge University Press.
  - Mayer, R. E. (2014). *The Cambridge Handbook of Multimedia Learning* (2nd ed.).
- **Key principles**: Multimedia Principle (words + pictures > words alone), Coherence Principle (remove extraneous material), Signaling Principle (highlight key information), Spatial Contiguity (place text near related visuals)
- **Adopted in**: Not yet adopted. See SlideBot entry.
- **Status**: **Not adopted.** CTML's dual-channel optimization is the highest-priority design intelligence gap.

---

### Tufte — Information Display

- **Sources**:
  - Tufte, E. R. (1983). *The Visual Display of Quantitative Information*. Graphics Press.
  - Tufte, E. R. (2006). *Beautiful Evidence*. Graphics Press.
- **Adopted in**: `design-principles.md` J.10 — "Figures over text" principle; `data-visualization.md` — data-ink ratio concept
- **Citation**: Referenced as "Tufte/assertion-evidence standard" in J.10 (line 176) — partially cited
- **Status**: Influence is present but attribution is thin. Tufte's "data-ink ratio" concept underlies our chart guidance but is never named.

---

### Okabe-Ito — Colorblind-Safe Palette

- **Source**: Okabe, M. & Ito, K. (2002). *Color Universal Design (CUD)*.
  https://jfly.uni-koeln.de/color/
- **Adopted in**: Style 18 (Scientific Data) color palette; `design-principles.md` J.9 accessibility standards
- **Status**: Used correctly. Attribution is implicit via the "Okabe-Ito" name in `styles.md` (Style 18).

---

### WCAG — Web Content Accessibility Guidelines

- **Source**: W3C, *Web Content Accessibility Guidelines 2.1* (2018).
  https://www.w3.org/TR/WCAG21/
- **Adopted in**: `design-foundations.md` contrast requirements (4.5:1 AA); `presentation-visual-qa/SKILL.md` contrast checks; `slide-patterns.md` Step 4
- **Status**: Correctly referenced by standard name. No attribution gap.

---

## Commercial Tools (Competitive Intelligence)

These are not sources we adopted from, but tools whose capabilities inform our design intelligence gaps.

### Beautiful.ai

- **URL**: https://www.beautiful.ai
- **Key capability**: "DesignAI" engine — automatic layout optimization, smart slide templates that adapt to content
- **Relevance**: Their design rules engine is what our style presets approximate manually. They solve layout selection algorithmically.
- **Last checked**: 2026-04-07

### Gamma

- **URL**: https://gamma.app
- **Key capability**: Generates entire documents/presentations from prompts; AI-native format (not constrained to traditional slides)
- **Relevance**: Represents the "beyond slides" direction — cards, nested layouts, web-native. Different paradigm from our 7-engine approach.
- **Last checked**: 2026-04-07

### Pitch

- **URL**: https://pitch.com
- **Key capability**: Collaborative presentation design with AI assistance; strong template system
- **Relevance**: Their collaboration model (real-time multi-user editing) is not relevant, but their template intelligence is.
- **Last checked**: 2026-04-07

---

## Provenance Summary

Quick reference: what influenced what.

| Slideaway Component | Primary Sources | Attribution Status |
|--------------------|-----------------|--------------------|
| Multi-agent pipeline architecture | PaperBanana, PPTAgent | ✅ Cited in README |
| Phase 0 discovery / Slide Brief | PaperBanana (analyst phase), Duarte (audience model) | ⚠️ PaperBanana cited; Duarte uncited |
| 30 design style presets | corazzon/pptx-design-styles | ✅ Cited in styles.md header |
| Audience quadrant model (J.2) | Duarte (2010) | ❌ Uncited |
| Narrative structures (J.3) | Duarte (2010), Minto (1987) | ⚠️ Minto partially cited; Duarte uncited |
| Assertion-evidence headlines (J.10) | Alley & Neeley (2005), Duarte (2008) | ❌ Uncited |
| Volume calibration (J.4) | Duarte (2008), presentation practitioner consensus | ❌ Uncited |
| Anti-AI-slop rules | Original to slideaway + community observation | ✅ Original work |
| WCAG contrast standards | W3C WCAG 2.1 | ✅ Cited by standard name |
| Colorblind palette (Style 18) | Okabe & Ito (2002) | ✅ Cited by name |
| CLT / CTML design theory | Sweller (1988), Mayer (2009) via SlideBot | ❌ Not adopted, not cited |
| PPTEval evaluation framework | PPTAgent (EMNLP 2025) | ⚠️ Partially adopted; Coherence dimension pending |
| 5-step design methodology | Visual communication practitioner consensus | ⚠️ `slide-patterns.md` says "Adapted from visual communication principles" — vague |
| Slide linter concept | vkehfdl1/slides-grab | ❌ Not adopted, not cited |

---

## Entry Template

When adding a new reference, copy this template:

```markdown
### [Name] — [One-Line Description]

- **Paper/Source**: [Full title]
- **Authors**: [Names]
- **Venue/Year**: [Where published, when]
- **URL**: [ArXiv, GitHub, DOI, or homepage]
- **Code**: [Repository URL if available]
- **License**: [License type]

#### What We Adopted

| Pattern | Where in Slideaway | Notes |
|---------|--------------------|-------|
| ... | ... | ... |

#### What We Haven't Adopted (Pending Review)

| Pattern | Description | Relevance | Priority |
|---------|-------------|-----------|----------|
| ... | ... | ... | ... |

- **Last checked**: YYYY-MM-DD
- **Next check**: [When/why to revisit]
```
