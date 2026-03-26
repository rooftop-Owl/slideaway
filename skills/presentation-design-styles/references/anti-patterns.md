# Presentation Design Anti-Patterns

> Quick-reference checklist for agents generating slides. Scan before generating any deck.
> 
> **Severity levels:**
> - **CRITICAL** — Always wrong. Never do this, regardless of context or style.
> - **WARNING** — Context-dependent. Wrong in most situations; requires deliberate justification.
> - **STYLE** — Preference/taste. Avoid by default; acceptable if the brief explicitly calls for it.
>
> For positive style guidance, see `styles.md` and `aesthetic-presets.md`.

---

## CRITICAL: Always Wrong

These patterns are prohibited without exception. They signal AI-generated content or produce inaccessible output.

### CRITICAL-01 — Accent lines under titles
**Do not place a decorative horizontal rule or accent line directly below a heading.**

This is the most recognized AI-generated content marker in slide design. It signals automated, template-recycled output and immediately undermines the presenter's credibility. A heading that needs a decorative underline to assert hierarchy has failed typographically.

```
# BAD — AI-slop fingerprint
Project Roadmap
─────────────────   ← never do this

# GOOD — Heading asserts hierarchy through size, weight, and spacing alone
Project Roadmap
```

- Source: Anthropic design conventions (inherited anti-pattern from frontend-design skill)
- Cross-reference: SKILL.md §Anti-Patterns (Universal), presentation-visual-qa.md §1

---

### CRITICAL-02 — Text-only slides with no visual hierarchy
**Do not generate slides that are solid blocks of undifferentiated text.**

A slide where all text is the same size, weight, and color communicates nothing — the audience has no entry point. Every slide needs at least one visual hierarchy signal: a dominant heading, a key statistic, an emphasized callout, or a structural separator.

Minimum hierarchy markers per slide:
- A title at least 2× the body font size
- At least one visual weight contrast (bold, color accent, or size)

---

### CRITICAL-03 — Inter + violet/indigo + gradient text combination
**The combination of Inter as the sole font, violet or indigo as the primary palette, and gradient-filled text is a recognized AI-slop fingerprint.**

Each element alone is acceptable. Together, they produce output that registers immediately as machine-generated. If Inter is the selected font (acceptable on its own), pair it with a non-violet accent and solid text. If violet/indigo is used, pair it with a different font family.

Forbidden combination:
- Font: Inter (alone, no display font pairing)
- Color: violet `#7C3AED`, indigo `#4F46E5`, or nearby hues as the primary palette
- Text style: gradient-filled or color-gradient headings

---

### CRITICAL-04 — Neon dashboard aesthetic for non-technical contexts
**Neon color palettes (electric greens, magentas, cyans) on dark backgrounds belong only in specific contexts: cybersecurity, gaming, deep tech, or AI product launches (Style 13: Electric Neon).**

Applying neon aesthetics to academic research, corporate briefings, wellness presentations, or professional services is a severe context mismatch. The aesthetic signals "gamer/hacker" and undermines professional credibility outside its domain.

Forbidden outside Style 13 context:
- Neon green as a primary accent on dark slides
- Electric pink or magenta as body-text contrast
- Multiple saturated neon colors on a single slide

---

### CRITICAL-05 — Gradient mesh backgrounds
**Do not use gradient mesh or multi-stop color gradient backgrounds as the primary slide surface.**

Gradient mesh backgrounds — multiple interpolated color stops creating a flowing color wash — are one of the most overused and immediately recognizable AI-generation patterns. They add visual complexity without information, distract from content, and age rapidly.

Prohibited uses:
- Full-slide gradient mesh as the background
- Three or more color stops blending across the slide background
- Animated gradient backgrounds in HTML slides

Acceptable alternatives: solid colors, single-directional gradients at 5–10% opacity for subtle depth, photographic backgrounds with a dark overlay.

---

### CRITICAL-06 — Purple gradients (generic AI aesthetic)
**Do not default to purple-to-dark or purple-to-blue gradient backgrounds.**

The purple gradient — specifically the `#7B2FF7 → #0D0D0D` or `#6C63FF → #311B92` family — is the single most overused AI-generated presentation color. It appears in 40–60% of AI-generated slide decks and signals zero design intent. Even if purple is appropriate for the brand, use it as a flat solid or accent, never as a full-slide gradient.

---

## WARNING: Context-Dependent (Wrong in Most Situations)

These patterns are wrong in standard contexts. They require an explicit brief or domain justification to use.

### WARNING-01 — Overused fonts: Inter, Roboto, Arial as the only typeface
**Using Inter, Roboto, or Arial as the sole typeface produces generic, forgettable slides.**

These fonts are legible and neutral — properties that make them useful as body fonts but poor as the complete typographic system. Without a pairing font with personality, all decks look identical.

Rule: if using Inter, Roboto, or Arial for body text, pair with a distinctive display font (Playfair Display, Syne, Raleway, DM Serif Display, etc.) for headings. Do not use the same neutral sans-serif for every text element.

Overuse indicators:
- Inter Bold as the heading font
- Inter Regular as body text
- Inter Light for captions
- No other typeface in the deck

---

### WARNING-02 — Generic blue as sole accent (`#0070C0`, `#2196F3`)
**Default Microsoft-blue or Material-blue as the only accent color signals template recycling.**

These blues appear in PowerPoint defaults, Google Slides defaults, and Bootstrap defaults. They communicate "I used the default" rather than "I made a deliberate choice." Use contextually appropriate accent colors. See `styles.md` for per-style accent recommendations.

Banned as default accents:
- `#0070C0` — PowerPoint default blue
- `#2196F3` — Material Design primary blue
- `#0078D4` — Fluent Design blue
- `#0066CC` — Apple-adjacent blue (acceptable only in Style 06: Clean White)

---

### WARNING-03 — Equal-weight color palettes with no hierarchy
**A palette where five or six colors appear in roughly equal proportion creates visual chaos.**

Every palette needs a hierarchy: one dominant background color (~70%), one secondary/supporting color (~20–25%), and one accent used sparingly (~5–10%). When multiple colors compete for equal visual weight, no element receives emphasis and the slide loses structure.

Signal: if you cannot identify the accent color on a slide, the palette hierarchy is broken.

---

### WARNING-04 — Comic Sans, Papyrus, Curlz MT
**These typefaces are incompatible with professional presentation contexts.**

Comic Sans: perceived as childish in non-children's contexts. Papyrus: overused in spa, wellness, and vaguely Egyptian contexts, now a cultural cliché. Curlz MT: decorative script with near-zero legibility at projector size. None of these are acceptable in business, academic, or professional settings.

No-use list (unconditional for professional decks):
- Comic Sans MS
- Papyrus
- Curlz MT
- Jokerman
- Brush Script MT
- Chiller

---

### WARNING-05 — All-caps body text
**Do not use uppercase styling for body paragraphs or bullet points.**

Uppercase reduces reading speed by 10–14% (research: Miles Tinker, 1967) and eliminates the ascender/descender variation that enables rapid word recognition. Uppercase is acceptable for short labels, headers of 1–3 words, and caption metadata. It is not acceptable for body text, bullet points, or any text longer than 5 words.

Acceptable uppercase uses:
- Category tags: `METHODOLOGY`, `RESULTS`
- Caption attribution: `SOURCE: IMF 2024`
- Short slide labels in constrained spaces

---

### WARNING-06 — More than 3 font families per deck
**Three font families is the maximum for a coherent deck. Two is better. One (with weight variation) is acceptable.**

Each additional typeface introduces visual noise and risks family clashes. A deck with four or more distinct typefaces looks assembled, not designed.

Rule: heading font + body font + (optional) monospace for code/captions = 3-family maximum.

---

### WARNING-07 — Bullet points with 7 or more items
**Lists of 7 or more bullets overwhelm working memory and force the audience to choose what to read.**

The research-backed limit is 3–5 items for effective working memory load. Beyond 5, audience attention splits between reading and listening. Beyond 7, the slide becomes a document page that belongs in an appendix.

If your list exceeds 5 items:
- Split into multiple slides with thematic groupings
- Collapse into a diagram, icon-grid, or 2×2 matrix
- Move details to backup slides

Cross-reference: slide-generation.md §J.10 (3 bullets maximum for optimal impact)

---

### WARNING-08 — Font size below 18pt for body text
**Text below 18pt effective size is not legible at projector distance (3–10m).**

The projector distance rule: assume the last row of seats is 10× the screen height away. At 10m from a 1m-tall screen, 18pt text subtends ~0.5° of visual angle — the minimum for comfortable reading.

Engine minimum requirements:
- Marp: 24px minimum, 28–32px recommended
- Beamer: 20pt minimum, 24–28pt recommended
- reveal.js: 24px minimum, 28–32px recommended
- python-pptx: 20pt minimum, 24–28pt recommended
- Standalone HTML: 24px minimum, 28–32px recommended

Cross-reference: slide-generation.md §J.9 (font size table)

---

### WARNING-09 — Mixing warm reds with cool corporate blues
**Warm reds (`#C0392B`, `#B91C1C`) and cool blues (`#0057A8`, `#1A3A5C`) in the same palette create visual discord.**

These colors sit opposite each other in temperature and fight for dominance. The combination appears in poorly adapted templates and signals accidental color choice. Warm palettes (reds, oranges, earth tones) should pair with neutral or warm-toned blues. Cool palettes (navy, corporate blue, slate) pair with cool-spectrum accents.

Cross-reference: Style 02 §Anti-Patterns

---

### WARNING-10 — Low-contrast text (below WCAG AA 4.5:1)
**Never use text that fails WCAG AA contrast (4.5:1 for normal text, 3:1 for large text).**

This is a WARNING rather than CRITICAL because dark-on-dark combinations may be intentional in Style 04 (Enterprise Dark), where they require careful validation. In all other contexts, failing WCAG AA is an error.

Common failures:
- Gray body text on off-white backgrounds (`#718096` on `#F8FAFC` = 3.9:1 — fails)
- Light-colored text on medium-colored backgrounds
- Any text on photographic background without dark overlay

Tools: contrast-ratio.com, APCA checker

---

### WARNING-11 — No competitive context in business decks
**Sales pitches, product demos, and investor briefings without a competitive positioning slide signal weak market awareness.**

Audiences for business decks assume you know your competition. A deck that never mentions alternatives is either naive or evasive. Include at minimum: "Others do X; we do Y because Z."

Cross-reference: slide-generation.md §J.8b (Business/Product conventions)

---

### WARNING-12 — No CTA slide in business decks
**Every business presentation must close with an explicit call-to-action slide.**

"Thank you" is not a closing slide. The CTA must include: specific ask, decision owner, and deadline. "Approve Q3 budget by March 1 — Decision owner: CFO" is a CTA. "We appreciate your time" is not.

Cross-reference: slide-generation.md §J.8b

---

## STYLE: Preference and Taste

These patterns produce suboptimal results in most contexts but may be intentional in specific brief contexts.

### STYLE-01 — Centered body text
**Default to left-aligned body text. Centered text reduces reading speed for multi-line content.**

Centered text is appropriate for: single-line slide titles, pull quotes, callout numbers, section break headings. It is inappropriate for: body paragraphs, bullet lists, captions with more than one line.

Reason: centered multi-line text creates a ragged left edge that the eye must search for on each new line, increasing cognitive load.

Acceptable centered uses:
- Title slide headline
- Full-slide pull quote (1–2 lines)
- Section break label
- Single statistic callout

---

### STYLE-02 — Drop shadows on every element
**Drop shadows should be used on at most 1–2 elements per slide to create depth hierarchy.**

When every element has a drop shadow, the depth cue loses meaning — everything floats equally and nothing recedes. Use shadows selectively: one card or image elevated above a flat background. Apply no shadow to text, icons, or small UI elements.

---

### STYLE-03 — Clipart and generic stock photo overuse
**Clipart images and search-result stock photography undermine design quality.**

Clipart (illustrated icons from Microsoft Office, early-web clipart libraries) signals effort level and reads as amateurish in professional contexts. Generic stock photography (businessman shaking hands, lightbulb on white background, team high-fiving) communicates "I did not have time to find real imagery."

Alternatives:
- Unsplash / Pexels for authentic photography
- System UI icons or a consistent icon set (Heroicons, Lucide, Phosphor)
- Simple geometric shapes that carry meaning without pretending to be illustrations
- Real screenshots, data visualizations, or diagrams

---

### STYLE-04 — Mismatched slide aspect ratios
**All slides in a deck must use the same aspect ratio.**

Mixing 16:9 slides with 4:3 slides, or inserting a poster-format slide (portrait) into a landscape deck, creates disruptive visual jumps and often results in cropped or letter-boxed output on projectors.

Standard ratios:
- `16:9` (1920×1080) — default for all modern screens and projectors
- `4:3` — legacy projectors and older formats only
- Never mix within a single deck

---

### STYLE-05 — Inconsistent spacing between elements
**Maintain consistent spacing units throughout a deck.**

Inconsistent spacing (some headings have 24px top margin, others have 12px, others have 0px) creates visual noise that the audience perceives as lack of care without knowing why. Establish a 4px or 8px base unit and use multiples exclusively.

Spacing hierarchy example:
- Section padding: 48pt
- Between title and body: 24pt
- Between bullets: 12pt
- Between caption and element: 8pt

---

### STYLE-06 — Slide numbers missing on long decks
**Decks of 10 or more slides should include slide numbers.**

Without slide numbers, audience members cannot reference specific slides during Q&A ("can you go back to that chart?") and reviewers cannot provide precise feedback. Slide numbers are optional for short decks (≤8 slides) and lightning talks where brevity is the convention.

Cross-reference: Style 02 §Layout Principles (slide numbers bottom-right, consistent every slide)

---

### STYLE-07 — Animations on every element
**Motion should be purposeful and reserved for high-impact moments.**

One well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions on every element. Animations applied to every bullet, icon, and text block produce motion sickness-adjacent cognitive overload and slow down delivery.

Reserved animation uses:
- Title slide entrance (one staggered sequence, max 3 elements)
- Data reveal (animated chart line drawing)
- Section transition (full-slide crossfade)

Never animate:
- Individual bullet points (use fragments only if content requires staged revelation)
- Background elements
- Decorative shapes

---

### STYLE-08 — Missing speaker notes
**Every content slide should have speaker notes.**

Slides without notes force presenters to memorize or improvise, increasing error rates. Notes survive format conversion (PPTX → PDF presenter view, HTML → reveal.js presenter mode). They also serve as accessibility documentation for screen reader users reviewing distributed decks.

Cross-reference: slide-generation.md §J.10 (Speaker notes: write notes for every content slide)

---

## Per-Style Anti-Patterns (Representative Sample)

These are style-specific prohibitions from `styles.md`. For the full per-style "Avoid" section, always consult `styles.md` directly — do not duplicate specs here.

### Style 01 (Executive Suite) — Avoid
- Gradients (flat color blocks only)
- More than two accent touches per slide (gold must be sparse)
- Rounded corners (use sharp rectangles)
- Decorative illustrations or stock photography backgrounds

### Style 04 (Enterprise Dark) — Avoid
- Pure black `#000000` background (too harsh, not modern)
- Low-contrast text (light gray on near-white — accessibility failure)
- Warm color accents (orange-red — jarring against cool palette)
- Printed handout derivation (dark backgrounds consume ink)

### Style 06 (Clean White) — Avoid
- Multiple focal points per slide (one emphasis point only)
- Filling whitespace with content (whitespace IS the design)
- Gradients, textures, or visual-noise backgrounds
- Bullet-point lists (convert to individual statement slides)

### Style 13 (Electric Neon) — Avoid
- Neon aesthetic outside AI/cybersecurity/gaming context (CRITICAL-04 above)
- Warm background colors (destroys the dark-surface neon contrast)
- Serif body fonts (neon is a sans-serif aesthetic)
- Print derivation without palette inversion

### Style 16 (Academic Classic) — Avoid
- Decorative elements that compete with content
- Warm or saturated accent colors (academic register requires restraint)
- Full-bleed photographic backgrounds
- Sans-serif headings (Academic Classic is a serif-first style)

### Style 26 (Midnight Premium) — Avoid
- Bright saturated colors (undermines the luxury register)
- More than one accent touch per slide (scarcity = luxury)
- Sans-serif body fonts (Midnight Premium is typographically formal)
- Stock photography (original or no photography)

---

## AI-Slop Detection Summary

When reviewing generated slides, flag any deck that exhibits 2 or more of these simultaneous markers:

| Marker | Severity |
|--------|----------|
| Accent line under slide title | CRITICAL |
| Inter font as sole typeface | WARNING |
| Violet/indigo gradient mesh background | CRITICAL |
| Purple gradient backdrop (`#7B2FF7`, `#6C63FF` family) | CRITICAL |
| Generic blue accent only (`#0070C0`, `#2196F3`) | WARNING |
| Gradient text fill on headings | CRITICAL (when combined with above) |
| Neon palette outside tech/gaming context | CRITICAL |
| Equal-weight 5-color palette | WARNING |
| All body text centered | STYLE |
| Every element has drop shadow | STYLE |

Three or more simultaneous markers indicate AI-generated default output. Regenerate with an explicit style selection from `styles.md` and verify against this checklist before delivery.

---

## Checklist: Pre-Delivery Scan

Agents must verify these before delivering any deck:

### CRITICAL checks (all must pass)
- [ ] No accent lines under any heading
- [ ] Visual hierarchy present on every slide (minimum: dominant title + body contrast)
- [ ] Not using Inter + violet + gradient text simultaneously
- [ ] No neon palette outside Style 13 context
- [ ] No gradient mesh background
- [ ] No purple gradient backdrop (unless explicit brief)

### WARNING checks (flag if present)
- [ ] Font: if Inter/Roboto/Arial, confirm a display font pairing exists
- [ ] Accent color: not defaulting to `#0070C0` or `#2196F3` as sole accent
- [ ] Color palette: clear dominant/secondary/accent hierarchy visible
- [ ] No Comic Sans, Papyrus, Curlz MT, or unprofessional display fonts
- [ ] Body text: all UPPERCASE body text reviewed and justified
- [ ] Font families: ≤3 distinct families in the deck
- [ ] Bullet lists: no list exceeds 5 items (3 preferred)
- [ ] Font size: body text ≥18pt effective (≥24px on screen)
- [ ] Contrast: all text passes WCAG AA 4.5:1 minimum
- [ ] Business deck: includes competitive context slide
- [ ] Business deck: closes with explicit CTA slide

### STYLE checks (review with user if flagged)
- [ ] Body text: left-aligned (not centered) for multi-line content
- [ ] Drop shadows: ≤2 elevated elements per slide
- [ ] Imagery: no clipart or generic stock photography
- [ ] Aspect ratio: consistent 16:9 throughout
- [ ] Spacing: consistent base unit throughout
- [ ] Slide numbers: present on decks ≥10 slides
- [ ] Animations: reserved for ≤3 key moments, not every element
- [ ] Speaker notes: present on all content slides

---

*Cross-references: `styles.md` (30 style specs), `aesthetic-presets.md` (5 CSS presets), `slide-generation.md` §J.7 (narrative anti-patterns), §J.9 (accessibility), §J.10 (content principles), §J.11 (pre-presentation checklist)*
