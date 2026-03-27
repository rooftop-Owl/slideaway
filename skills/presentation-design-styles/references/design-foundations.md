# Design Foundations Reference

## Scope

**Covers**: Typography theory for slides, color theory and psychology, WCAG accessibility standards, layout composition principles, animation and build principles.

**Does not cover**: Specific named style presets (see [styles.md](styles.md)) · Anti-patterns catalog (see [anti-patterns.md](anti-patterns.md)) · Chart-specific color scales (see [data-visualization.md](../../slide-generation/references/data-visualization.md)) · Engine-specific implementation details. Complements J.9 from design-principles.md — this file covers the theory; J.9 covers application rules.

---

## 1. Typography Theory

Typography is the single highest-impact design decision in a slide deck. Font choice signals credibility, tone, and professionalism before the audience reads a word.

### Sans-Serif vs. Serif

| Dimension | Sans-Serif | Serif |
|-----------|-----------|-------|
| **Projection readability** | Excellent — clean strokes survive low-res projectors | Good at large sizes; thin serifs disappear below 24pt |
| **Tone** | Modern, technical, approachable | Traditional, authoritative, academic |
| **Best for** | Tech, startup, product, data-heavy decks | Academic papers, law, finance, executive boardroom |
| **Body text at 18pt** | Highly readable | Readable |
| **Body text at 14pt** | Readable | Marginal — serif details blur |
| **Examples** | DM Sans, Outfit, Plus Jakarta Sans | Playfair Display, Libre Baskerville, Lora |

**Rule**: Serif headings + sans-serif body is a classic pairing that works. Sans-serif throughout is safe. Serif throughout is risky at small sizes. Two serifs together almost never works.

**Banned fonts** (AI-slop signal): Inter, Roboto, Arial, Helvetica Neue, Open Sans. These are defaults — they communicate "no design decision was made."

### Font Size Hierarchy

Every size tier serves a specific purpose. Violating the hierarchy collapses the visual structure.

| Tier | Element | Size Range | Weight | Notes |
|------|---------|------------|--------|-------|
| **T1** | Slide title | 36–54pt | Bold | Assertion-style headline (J.3) — never a topic phrase |
| **T2** | Section header / Subtitle | 28–34pt | SemiBold | Used sparingly; max 1 per slide |
| **T3** | Body text / Bullet points | 24–28pt | Regular | Minimum for readable projection |
| **T4** | Supporting detail | 20–22pt | Regular | Use only when T3 is insufficient |
| **T5** | Labels / Captions / Sources | 14–18pt | Regular or Light | Never below 14pt on projected slides |

> **Room Test**: Can you read every text element from the back of the room? If you're unsure, the font is too small. Default assumption: the room is 15 meters deep and the screen is 2.5 meters wide.

### The 6×6 Rule

**Maximum 6 bullet points per slide. Maximum 6 words per bullet.**

This is a hard constraint, not a guideline. Slides are not documents. If the content requires more than 6×6, split it across two slides or move it to a handout.

| Violation | Symptom | Fix |
|-----------|---------|-----|
| Too many bullets | Audience reads ahead, stops listening | Split slide or use progressive reveal |
| Too many words per bullet | Bullets become sentences | Extract the key noun + verb; cut the rest |
| Full sentences as bullets | Slide becomes a teleprompter | Rewrite as fragments; speak the context |

### Emphasis Do's and Don'ts

| Do | Don't |
|----|-------|
| **Bold** for the single most important word or phrase per slide | Bold entire paragraphs |
| *Italic* for titles of works, technical terms, or gentle emphasis | Italic for emphasis (too subtle at distance) |
| Color accent on one key term (use the style's accent color) | Underline (implies hyperlink) |
| Increase size by 1 tier for a key callout | ALL CAPS for body text (reduces readability) |
| Whitespace to isolate important content | Strikethrough (confusing in presentation context) |

---

## 2. Color Theory

### Color Psychology in Presentation Contexts

Color primes emotional and cognitive responses before the audience processes content. Use this deliberately.

| Color | Primary Association | Presentation Use | Caution |
|-------|-------------------|-----------------|---------|
| **Blue** (`#0072B2` range) | Trust, stability, authority, competence | Corporate, finance, technology, healthcare | Cold/distant if overused; avoid pure `#0000FF` |
| **Green** (`#009E73` range) | Growth, success, sustainability, go/positive | Environmental, financial growth, positive metrics | Avoid red-green pairing (colorblindness) |
| **Red** (`#D55E00`–`#CC0000` range) | Urgency, danger, importance, stop | Alerts, critical metrics, call-to-action | Overuse creates anxiety; use sparingly |
| **Orange** (`#E69F00` range) | Energy, creativity, enthusiasm, warmth | Startup, innovation, creative fields | Can feel informal; test against brand |
| **Purple** (`#8E0152`–`#6A0DAD` range) | Premium, innovation, wisdom, mystery | Luxury, research, academic | Overused in AI-generated decks — avoid `#6366f1` |
| **Yellow** (`#F0E442` range) | Optimism, attention, caution | Highlights, warnings, energy | Low contrast on white; use on dark backgrounds |
| **Black/Dark gray** | Sophistication, authority, formality | Executive, luxury, editorial | Heavy; use as accent, not dominant background |
| **White/Light** | Clarity, space, cleanliness | Minimalist, medical, tech | Needs strong contrast elements to avoid blandness |

### WCAG Accessibility Standards

**WCAG AA (minimum standard)**: 4.5:1 contrast ratio for normal text, 3:1 for large text (18pt+ or 14pt+ bold).

**WCAG AAA (enhanced standard)**: 7:1 contrast ratio for normal text, 4.5:1 for large text.

For presentations, target **WCAG AA as the floor**. Projection environments reduce effective contrast — what passes on screen may fail on a projector.

| Pairing | Contrast Ratio | WCAG Level | Slide Verdict |
|---------|---------------|------------|---------------|
| Black `#000000` on White `#FFFFFF` | 21:1 | AAA | Excellent |
| Dark Navy `#1A3A5C` on White `#FFFFFF` | 12.4:1 | AAA | Excellent |
| White `#FFFFFF` on Dark Navy `#1A3A5C` | 12.4:1 | AAA | Excellent |
| Okabe-Ito Blue `#0072B2` on White | 5.9:1 | AA | Good |
| Okabe-Ito Orange `#E69F00` on White | 2.3:1 | Fail | Too low — use on dark backgrounds only |
| Okabe-Ito Yellow `#F0E442` on White | 1.2:1 | Fail | Never use yellow text on white |
| Medium Gray `#888888` on White | 3.5:1 | AA (large only) | Captions only, 14pt+ |

**Testing tools**:
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) — paste hex values, get ratio instantly
- [Coblis](https://www.color-blindness.com/coblis-color-blindness-simulator/) — simulate how your slide looks under 8 types of color vision deficiency
- [Color Oracle](https://colororacle.org/) — desktop app, real-time colorblindness simulation overlay

### Okabe-Ito Palette — Full Specification

The Okabe-Ito palette is the recommended default for any multi-color slide element. It was designed to be distinguishable under all common colorblindness types.

| Slot | Name | Hex | RGB | Use |
|------|------|-----|-----|-----|
| 1 | Black | `#000000` | 0, 0, 0 | Reference/total series |
| 2 | Orange | `#E69F00` | 230, 159, 0 | Primary series |
| 3 | Sky Blue | `#56B4E9` | 86, 180, 233 | Secondary series |
| 4 | Bluish Green | `#009E73` | 0, 158, 115 | Tertiary series |
| 5 | Yellow | `#F0E442` | 240, 228, 66 | Highlight (dark bg only) |
| 6 | Blue | `#0072B2` | 0, 114, 178 | Fourth series |
| 7 | Vermillion | `#D55E00` | 213, 94, 0 | Fifth series / Alert |
| 8 | Reddish Purple | `#CC79A7` | 204, 121, 167 | Sixth series |

> For chart-specific color scale recommendations (sequential, diverging), see [data-visualization.md](../../slide-generation/references/data-visualization.md).

### Color Count Rules

| Slide Type | Max Colors | Rationale |
|-----------|-----------|-----------|
| Text-only slide | 2 (primary + accent) | More creates visual noise |
| Chart slide | 6 (Okabe-Ito slots 2–7) | Beyond 6, use small multiples |
| Infographic | 4 | Complexity requires restraint |
| Title/section break | 3 | Bold statement, not a rainbow |
| Full-bleed image slide | 1 (text overlay only) | Image provides visual richness |

---

## 3. Layout & Composition

### Rule of Thirds

Divide the slide into a 3×3 grid. Place key content at the intersections — these are the natural focal points of human visual attention.

```
┌─────────┬─────────┬─────────┐
│         │         │         │
│         ●         ●         │
│         │         │         │
├─────────┼─────────┼─────────┤
│         │         │         │
│         ●         ●         │
│         │         │         │
├─────────┼─────────┼─────────┤
│         │         │         │
│         │         │         │
│         │         │         │
└─────────┴─────────┴─────────┘
          ● = power points
```

**Application**:
- Place the headline at the top-left power point (top-left third intersection)
- Place the key visual or data element at the right-center or center-right power point
- Leave the bottom third for supporting detail, source lines, or breathing room

### White Space

**Target: 40–50% of slide area should be empty.**

White space is not wasted space — it directs attention and signals confidence. Slides that fill every pixel communicate anxiety, not information.

| White Space Level | Audience Perception | Appropriate For |
|------------------|--------------------|----|
| <30% | Cluttered, overwhelming | Never appropriate |
| 30–40% | Dense but readable | Data-heavy technical slides |
| 40–50% | Balanced, professional | Most presentation types |
| 50–60% | Spacious, confident | Executive briefings, keynotes |
| >60% | Minimalist, editorial | Impact statements, section breaks |

### 5 Layout Patterns

Each pattern suits a specific content type. Don't force content into the wrong pattern.

**Pattern 1: Title + Full-Width Content**
```
┌────────────────────────────────┐
│  HEADLINE ASSERTION            │
├────────────────────────────────┤
│                                │
│   [Primary content area]       │
│   Chart / Image / Key stat     │
│                                │
│                                │
└────────────────────────────────┘
```
*Use for*: Single chart, single image, single big number. The most common and most effective pattern.

---

**Pattern 2: Two-Column Split**
```
┌─────────────────┬──────────────┐
│  HEADLINE        │              │
├──────────────────┤              │
│                  │  [Visual]    │
│  [Text / List]   │  Chart or   │
│                  │  Image      │
│                  │              │
└──────────────────┴──────────────┘
```
*Use for*: Concept + example, problem + solution, before + after. Keep columns balanced in visual weight.

---

**Pattern 3: Three-Column Comparison**
```
┌──────────┬──────────┬──────────┐
│  HEADLINE SPANNING ALL COLUMNS │
├──────────┼──────────┼──────────┤
│          │          │          │
│  [Col 1] │  [Col 2] │  [Col 3] │
│  Option  │  Option  │  Option  │
│    A     │    B     │    C     │
│          │          │          │
└──────────┴──────────┴──────────┘
```
*Use for*: Feature comparisons, three-option decisions, three-step processes. Never use for more than 3 columns — use a table instead.

---

**Pattern 4: Big Number / Statement**
```
┌────────────────────────────────┐
│                                │
│                                │
│         ╔══════════╗           │
│         ║   2.4M   ║           │
│         ╚══════════╝           │
│    Units shipped in Q3         │
│                                │
└────────────────────────────────┘
```
*Use for*: Key metrics, milestone announcements, section openers. The number should be 80–120pt. Supporting text at 24pt.

---

**Pattern 5: Image Bleed + Text Overlay**
```
┌────────────────────────────────┐
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│  ┌─────────────────────────┐  │
│  │  WHITE TEXT ON OVERLAY  │  │
│  └─────────────────────────┘  │
└────────────────────────────────┘
```
*Use for*: Section breaks, emotional impact slides, keynote openers. Requires a dark overlay (50–70% opacity black) behind white text to ensure WCAG contrast compliance.

### Alignment Principles

| Principle | Rule | Why |
|-----------|------|-----|
| **Left-align body text** | Default for all body content | Ragged right is more readable than justified |
| **Center only headlines** | Title slides and section breaks only | Centering body text creates weak left edge |
| **Consistent margins** | 48–64pt on all sides | Prevents content from feeling cramped at edges |
| **Align to grid** | Every element snaps to the underlying grid | Random placement looks accidental |
| **Group related items** | Reduce space between related items; increase between groups | Proximity signals relationship (Gestalt) |

---

## 4. Animation & Builds

### When to Use Animation

Animation is a communication tool, not a decoration. Every animation must serve comprehension.

| Use Animation | Don't Use Animation |
|--------------|---------------------|
| Revealing complex diagrams step by step | Making text fly in from the left |
| Progressive disclosure of a process flow | Adding motion to static content that needs no sequence |
| Directing attention to a specific data point | Transitions between slides (use Fade or None) |
| Showing before/after states | Demonstrating that you know how to use PowerPoint |
| Building a chart series one element at a time | Any animation that takes >0.5 seconds |

**Core rule**: If removing the animation doesn't reduce comprehension, remove it.

### Animation Types

| Type | Timing | Use Case | Avoid When |
|------|--------|---------|-----------|
| **Appear** | Instant (0s) | Revealing list items, showing/hiding elements | Content needs smooth transition |
| **Fade In** | 0.3–0.5s | Overlays, callout boxes, emphasis elements | Fast-paced slides (feels slow) |
| **Wipe (Left→Right)** | 0.4–0.6s | Timeline reveals, process steps, bar chart builds | Non-sequential content |
| **Zoom** | 0.3–0.5s | Focusing on a detail within a larger diagram | General content (disorienting) |
| **Morph/Transform** | 0.5–0.8s | Showing data change over time, before/after | Complex slides with many elements |

**Timing rules**:
- Entrance animations: 0.3–0.5s maximum
- Exit animations: 0.2–0.3s (faster than entrance — audience has already seen it)
- Slide transitions: Fade at 0.3s or None — never Cube, Flip, or Dissolve
- Delay between sequential builds: 0s (click-triggered) or 0.8–1.2s (auto-advance)

### Progressive Disclosure Pattern

For complex diagrams or multi-step processes, reveal one element per click rather than showing everything at once.

```
Slide: "How the system works"

Click 1: Show Step 1 box only
Click 2: Add arrow + Step 2 box (Step 1 remains visible)
Click 3: Add arrow + Step 3 box (Steps 1–2 remain visible)
Click 4: Highlight the critical path in accent color
```

This keeps the audience focused on the current step while maintaining context. It also gives the presenter natural pause points.

### Animation Accessibility

- Never rely on animation alone to convey information — the static final state must be complete
- Avoid rapid flashing animations (>3 flashes/second triggers photosensitivity)
- Provide a "no animation" version for distributed decks (animations don't survive PDF export)
- Test builds in Presenter View before the actual presentation

---

## Quick Reference Card

| Decision | Rule |
|----------|------|
| Font for headlines | Distinctive display font, 36–54pt bold |
| Font for body | Readable sans-serif, 24–28pt regular |
| Minimum font size | 14pt (for labels/captions) |
| Bullet limit | 6 bullets × 6 words (6×6 rule) |
| Color count | 2–4 colors per slide |
| Categorical palette | Okabe-Ito (colorblind-safe) |
| Contrast minimum | WCAG AA: 4.5:1 |
| White space target | 40–50% of slide area |
| Animation duration | 0.3–0.5s maximum |
| Slide transition | Fade 0.3s or None |
| Layout default | Rule of Thirds, left-aligned content |
| Image text overlay | Dark overlay required for WCAG compliance |
