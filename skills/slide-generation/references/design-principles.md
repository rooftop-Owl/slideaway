## Section J — Design Principles & Presentation Intelligence (Universal)

<!-- Modularization note: If Section J exceeds ~250 lines, extract to standalone
     presentation-intelligence.md skill. See impact.md for growth path. -->

These principles apply to all 7 engines. Agent selects appropriate framework based on purpose (J.1), audience (J.2), and domain (J.8).

### Design Intelligence

For curated design styles and visual QA:
- **Style presets**: Load `presentation-design-styles` skill — 30 styles, 5 aesthetic presets, anti-pattern checklist
- **Visual QA**: Load `presentation-visual-qa` skill — rendering verification, checklist, wkhtmltoimage + Playwright

### J.1 — Purpose Taxonomy

Agent selects type based on user context (venue, audience, time allotted, format requested).

| Type | Duration | Slides | Structure | Key Constraint |
|------|----------|--------|-----------|----------------|
| **Lightning Talk** | 3–5 min | 3–5 | Single idea, rapid fire | No Q&A — exit on time |
| **Product Demo** | 5–10 min | 5–10 | Problem → Demo → CTA | Live demo must work; have screenshot fallback |
| **Conference Talk** | 12–20 min | 12–20 | Hourglass (J.3) | Strict time limit, questions after |
| **Sales/Investor Pitch** | 10–15 min | 10–15 | SCR (J.3), CTA slide required | Competitive context; explicit ask |
| **Status Update/Sprint Review** | 5–15 min | 5–10 | Pyramid (J.3): KPIs first | Stakeholders want decisions, not detail |
| **Seminar/Invited Talk** | 45–60 min | 40–55 | Hourglass + deep dives | Can afford narrative, backup slides key |
| **Thesis Defense** | 30–45 min | 30–45 | Methods-heavy Hourglass | Committee Q&A is scored; backup slides mandatory |
| **Poster Session** | 2–5 min (walk-by) | 1 (A0/A1) | Conclusion-first billboard | Must convey core message without presenter |

### J.2 — Audience Adaptation

Two-axis model. Agent assesses both axes from user context before generating slides.

- **Axis 1 — Technical depth**: Deep (expert methods, equations) ↔ Shallow (high-level concepts)
- **Axis 2 — Domain familiarity**: Insider (shared vocabulary) ↔ Outsider (needs domain grounding)

| Quadrant | Vocabulary | Depth | Figures | Example |
|----------|------------|-------|---------|---------|
| **Deep + Insider** | Full jargon, acronyms OK | Equations, methods detail | Technical plots, error bars | Physics prof → physics prof |
| **Deep + Outsider** | Define all domain terms | Keep methods, skip notation | Intuition-first figures, then technical | Engineer → product manager |
| **Shallow + Insider** | Shorthand OK, no equations | Results and implications only | Summary charts, dashboards | PI presenting to department head |
| **Shallow + Outsider** | Plain language throughout | What, so what, next steps | Infographics, analogies | Scientist → general public |

### J.3 — Narrative Structure

Agent selects framework based on J.1 purpose type. All frameworks use assertion-style headlines (see J.10).

**Hourglass Model** *(scientific default — conference talks, seminars, thesis defense)*
```
Broad context → Narrower problem → Specific contribution → Broader implications → Call to action
```
Opens wide to hook general audience, narrows to contribution, widens again to show impact.

**Assertion-Evidence Pattern** *(universal — applies to ALL headline writing regardless of framework)*
Every slide headline states a testable claim, not a topic phrase. "CO₂ levels correlate with temperature" not "CO₂ and Temperature".

**Pyramid Principle** *(executive/decision-maker — status updates, investor briefings)*
```
Conclusion first → 3 supporting reasons → Evidence for each reason
```
Audience hears the answer immediately; detail available if needed. Matches Minto/McKinsey structure.

**Situation → Complication → Resolution (SCR)** *(business default — sales pitches, product demos, sprint reviews)*
```
Situation: shared context audience already accepts →
Complication: tension or problem that breaks the status quo →
Resolution: your solution/product/recommendation
```
Creates narrative tension before the reveal. Most persuasive structure for decision-maker audiences.

### J.4 — Volume Calibration

Default rule: **1 content slide per minute**. Buffer 20% of allotted time for Q&A and transitions.

| Duration | Content Slides | + Scaffolding | Total | Pacing |
|----------|---------------|---------------|-------|--------|
| 3 min | 2–3 | 1 (title only) | 3–4 | ~1 slide/min; no Q&A |
| 5 min | 4–5 | 1–2 | 5–7 | Tight; 1 min buffer |
| 10 min | 8–9 | 2–3 | 10–12 | Title + outline + summary |
| 15 min | 12–13 | 2–3 | 14–16 | 3 min Q&A buffer |
| 20 min | 16–18 | 3–4 | 19–22 | 4 min Q&A buffer |
| 30–45 min | 24–35 | 4–6 | 28–41 | Deep dives OK; backup slides mandatory |

Scaffolding = title slide + outline + section transitions + summary/Q&A slide.
Practice with a timer. If >1.5 slides/min during rehearsal, cut content — never rush.

### J.5 — Signposting & Transitions

Helps audiences track location in the argument. Required for talks ≥10 minutes.

- **Outline slide** (after title): List 3–5 sections; return to it as section divider
- **Section transition phrases**: "Having established X, I'll now show Y", "This brings us to the core contribution"
- **Summary slide** (before Q&A): Restate 3 takeaways using same headline language as body slides
- **reveal.js vertical slides**: Use for optional deep-dive content (`↓`) — keeps main flow horizontal, extra detail accessible on demand
- **Progress indicator**: Slide numbers optional for short talks; recommended for ≥20 min

### J.6 — Depth Control

Rule of thumb: if explaining a single element takes >30 seconds, move detail to a backup slide.

| Content Type | Expert Audience | General Audience |
|--------------|----------------|-----------------|
| **Equations** | Show full derivation if novel; cite otherwise | Show result only; annotate terms |
| **Methods** | Full protocol, parameters, uncertainty | Schematic diagram; skip parameters |
| **Statistics** | Confidence intervals, effect sizes, p-values | "X is 2× larger than Y" |
| **Terminology** | Acronyms OK after first use | Define every term on first use; avoid acronyms |
| **Background** | 1–2 slides assumed shared knowledge | 3–5 slides context-building |

### J.7 — Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Bullet point walls** | Audience reads, stops listening | Replace bullets with assertion headline + 1 supporting visual |
| **Flat narrative** | No arc, no tension, no takeaway | Apply J.3 framework; add Complication before Resolution |
| **Topic-phrase headlines** | "Results" tells audience nothing | Write full-sentence assertions: "Treatment reduces cost by 40%" |
| **Decoration over data** | Clip art, gradients, stock photos obscure signal | Remove decorative elements; every pixel earns its place |
| **Hallucinated citations** | Erodes trust immediately | Cite only sources you can verify; placeholder → backup slide |
| **Uniform slide density** | Every slide looks the same — cognitive fatigue | Vary: text-heavy → figure-only → title card → diagram |
| **Missing "so what"** | Data presented, implication left implicit | End every results section with explicit implication slide |
| **Missing call-to-action** | Business deck ends without clear next step | Always close with explicit ask: "Approve budget", "Schedule follow-up" |
| **No competitive context** | Sales pitch assumes audience shares your perspective | Include positioning slide: "Others do X; we do Y because Z" |

### J.8 — Domain Conventions

Agent selects J.8a or J.8b based on J.1 purpose type.

#### J.8a — Scientific/Academic

Standard 9-section structure for conference talks and seminars:
Title → Motivation → Background → Methods → Results → Discussion → Conclusions → Acknowledgments → Backup

- **AGU/EGU style**: Include session code on title slide; 12-min talks get 2–3 min Q&A
- **QR codes**: Link to paper preprint, code repo, or dataset — place on title and conclusions slides
- **Funding acknowledgment**: Logos on final slide before backup; required for most grants
- **Backup slides**: Prepare answers to 3–5 most likely questions; label clearly as "Backup"
- **Figure attribution**: Caption format — "Source: Author et al. (Year), Journal" for all reproduced figures

#### J.8b — Business/Product

Standard structure for product demos, sales pitches, and sprint reviews:

- **CTA slide** (mandatory): Final slide states explicit ask with owner and deadline — "Approve Q3 budget by March 1 — Decision owner: CFO"
- **Competitive context slide**: "Landscape" or "Why us" — position clearly against 2–3 alternatives
- **Metrics dashboard**: Key KPIs in first 3 slides (revenue, growth, risk) — executive audiences want numbers first
- **Next steps slide**: Owner names + dates for each action item; not "we will explore" but "Alice closes contract by Apr 15"
- **Appendix structure**: Financial models, technical specs, and risk analysis go in appendix — reference during Q&A

### J.9 — Accessibility

| Dimension | Standard | Notes |
|-----------|----------|-------|
| **Color palette** | Colorblind-safe required | Okabe-Ito, ColorBrewer, Viridis; test at color-blindness.com/coblis |
| **Contrast** | ≥4.5:1 (WCAG AA) | Never use red/green as sole differentiator |
| **Font family** | Sans-serif for body | Serif acceptable for headings only (Beamer academic style) |
| **Font size** | Engine minimum enforced | See engine table below |
| **Line spacing** | ≥1.3× font size | Prevents cramping at projector distance |
| **Alt text** | Required for all figures | Write in speaker notes if slide medium doesn't support it |
| **Animation** | Functional only | Transitions for reveal sequence; avoid decorative movement |

Engine minimum font sizes:

| Engine | Minimum | Recommended | Notes |
|--------|---------|-------------|-------|
| Marp | 24px | 28–32px | Use `<!-- fit -->` for auto-sizing titles |
| Beamer | 20pt | 24–28pt | `\fontsize{24}{28}\selectfont` |
| reveal.js | 24px | 28–32px | Set in theme CSS |
| python-pptx | 20pt | 24–28pt | Via `Pt()` in slide_factory |
| HTML | 24px | 28–32px | Base font-size on `<body>` |

### J.10 — Content Principles

| Principle | Rule | Why |
|-----------|------|-----|
| **One idea per slide** | Max 1 main point | Audience absorbs one thing at a time; splitting dilutes both |
| **Assertion headlines** | Full-sentence claim, not topic phrase | Audience knows your argument even without the body slide |
| **Lead with conclusion** | State finding first, then evidence | Reduces cognitive load; works for all J.3 frameworks |
| **3 bullets maximum** | Never exceed 3 items on a slide | Tufte/assertion-evidence standard; beyond 3 → figure or split slides |
| **Figures over text** | Prefer diagrams, charts, photos | Visual memory > verbal memory; if you can visualize it, do it |
| **Speaker notes** | Write notes for every content slide | Delivery content ≠ slide content; notes survive format conversion |
| **Backup slides** | Prepare for anticipated questions | Confidence in Q&A; shows depth without cluttering main deck |

### J.11 — Pre-Presentation Checklist

- [ ] Purpose type selected (J.1) and narrative structure chosen (J.3)
- [ ] Audience level assessed on both axes — technical depth + domain familiarity (J.2)
- [ ] Slide count within volume budget for allotted duration (J.4)
- [ ] Section transitions included for talks ≥10 min (J.5)
- [ ] Depth calibrated: backup slides for anything >30s to explain (J.6)
- [ ] Domain conventions applied: J.8a (academic) or J.8b (business) (J.8)
- [ ] Max 1 idea per slide (J.10)
- [ ] All headlines are assertion sentences, not topic phrases (J.10)
- [ ] Max 3 bullet points per slide (J.10)
- [ ] All figures readable at projector resolution; captions on every figure (J.9)
- [ ] Font size ≥24pt effective for all body text (J.9)
- [ ] Colorblind-safe palettes; contrast ≥4.5:1 WCAG AA (J.9)
- [ ] Speaker notes written for every content slide (J.10)
- [ ] Backup slides prepared for anticipated questions (J.10)
- [ ] Tested on target display/projector if possible
- [ ] File format confirmed with organizers (PDF? PPTX? HTML?)
---

