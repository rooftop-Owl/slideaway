# Slide Design Methodology

> A 5-step framework for creating effective, visually coherent presentation slides.
> Adapted from visual communication principles for agent-assisted slide generation.

---

## Step 1: Define the Message

Every effective slide starts with a single, clear message — not a topic, but a claim.

**Key questions to ask:**
- What is the one thing the audience must remember after this slide?
- What decision or insight does this slide enable?
- Is this message actionable, specific, and falsifiable?

**Patterns:**
- Write the slide title as a complete sentence stating the conclusion, not a noun phrase.
  - Poor: "Revenue Trends"
  - Better: "Revenue grew 42% YoY driven by enterprise upsell"
- If you cannot state the message in one sentence, the slide covers too much ground.
- Each slide earns its place by advancing the narrative — eliminate slides that merely fill time.

**Anti-patterns to avoid:**
- Vague titles like "Overview" or "Background" that force readers to infer the point.
- Multiple unrelated claims on a single slide.
- Content that is background knowledge rather than argument.

---

## Step 2: Choose the Style

The visual style should be deliberately matched to context: audience, venue, and purpose.

**Style axes to consider:**

| Axis | Options |
|------|---------|
| Tone | Formal ↔ Casual |
| Density | Sparse ↔ Information-rich |
| Color temperature | Warm ↔ Cool |
| Typography weight | Light/editorial ↔ Bold/punchy |

**Matching style to context:**
- **Executive briefings**: High contrast, large type, minimal decoration — every pixel earns its keep.
- **Academic conferences**: Serif headings, readable body type, data-forward with clear axis labels.
- **Product demos**: Clean interface-like layouts, generous whitespace, visual metaphors over text walls.
- **Technical deep-dives**: Monospace code blocks prominent, muted palette, diagram-centric.

**Consistency rule**: Commit to one aesthetic preset for the entire deck. Mixing styles within a deck signals carelessness. Use the aesthetic presets defined in `aesthetic-presets.md` for named, reproducible styles.

---

## Step 3: Structure the Layout

Layouts control attention. Readers scan in Z-pattern or F-pattern — design to intercept that scan.

**Primary layout archetypes:**

1. **Title slide** — Full bleed color or image. Presenter name, date, event. No bullet points.
2. **Section break** — Single statement, often full-bleed accent color. Reorients audience.
3. **Content slide** — Heading + body. Limit to 5–7 bullet points maximum; prefer 3–4.
4. **Two-column (split)** — Compare two items, show before/after, or present data + commentary.
5. **Diagram-first** — Diagram occupies 70%+ of slide area; caption is secondary.
6. **Data slide** — Single chart occupies primary area. Title states the finding, not the variable.

**Spatial hierarchy rules:**
- The largest element draws first attention — make it your most important content.
- Breathing room (whitespace) is not wasted space — it reduces cognitive load.
- Align elements to an invisible grid; consistent margins signal professionalism.
- Group related items visually (proximity) and separate unrelated items clearly.

**What to avoid:**
- Header + 8-line bullet block + 3-column table on one slide.
- Decorative clipart or stock illustrations that don't add meaning.
- Accent lines or horizontal rules directly under heading text (signals AI-generated content).

---

## Step 4: Apply Color and Typography

Color and typography are not decoration — they encode meaning and establish hierarchy.

**Color application principles:**

- **Background**: Use `--bg-primary` for most slides; `--bg-secondary` for section variants.
- **Text hierarchy**: `--text-primary` for body; `--text-secondary` for captions and metadata.
- **Accent**: Reserve `--accent` for the single most important element per slide — a callout number, a highlighted data point, or a CTA.
- **Dark surfaces**: Use `--bg-dark` for title slides or section breaks to create visual punctuation.

**Typography rules:**
- Limit to 2 typeface families maximum: one for headings, one for body.
- Prefer system font stacks for portability: `ui-serif`, `ui-sans-serif`, `ui-monospace`.
- Body text minimum: 18px at 1080p; 24px preferred for projected presentations.
- Heading size: 2×–3× body size for clear hierarchy.
- Never use more than 3 font sizes on a single slide.
- Avoid decorative scripts, display fonts with poor legibility, or fonts requiring paid licenses.

**Contrast requirements:**
- Body text on background must achieve WCAG AA (4.5:1 contrast ratio).
- Large text (18px+ bold or 24px+ normal) may use 3:1 ratio.
- Test dark-mode and light-mode variants if the deck will be used in both environments.

---

## Step 5: Validate and Refine

A slide that looks right in isolation may fail in context. Validate across three dimensions.

**Content validation:**
- [ ] Every slide has a clear, single message stated in the title.
- [ ] Bullet count is 5 or fewer per slide.
- [ ] No slide contains text smaller than readable at projected size.
- [ ] Data visualizations have labeled axes and a stated conclusion.
- [ ] Acronyms and jargon are defined at first use.

**Visual validation:**
- [ ] Consistent use of CSS custom properties (no hard-coded one-off colors).
- [ ] Accent color appears on at most one key element per slide.
- [ ] No decorative horizontal rules under headings.
- [ ] Whitespace is generous — content does not feel cramped.
- [ ] All images and diagrams are high resolution (no blurry or pixelated assets).

**Narrative validation:**
- [ ] Slides 1 → N form a logical argument; each slide sets up the next.
- [ ] Title slide, at minimum one section break per major topic, and a closing slide are present.
- [ ] Total slide count matches available time: ~1–2 minutes per slide for spoken delivery.
- [ ] The final slide provides a clear call-to-action or takeaway summary.

**Iteration protocol:**
1. Review deck in presentation mode at target resolution (1280×720 or 1920×1080).
2. Read titles only — do they tell the story without body text?
3. Have a peer who was not present for the briefing read the deck cold — what did they miss?
4. Remove any slide that cannot justify its place in the narrative.
5. Re-apply consistency checks after any structural edit.
