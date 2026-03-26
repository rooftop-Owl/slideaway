# Style Catalog

The slides module includes 30 curated visual styles across 6 categories. Styles control color
palettes, typography, spacing, and overall aesthetic. Specify a style with `--style` or describe
your desired look and the command will select the best match.

---

## Overview

| Category | Count | Aesthetic |
|----------|-------|-----------|
| Corporate | 5 | Professional, brand-safe, boardroom-ready |
| Academic | 5 | Clean, readable, conference-appropriate |
| Creative | 5 | Bold, expressive, high visual impact |
| Technical | 5 | Code-friendly, dark themes, developer-focused |
| Elegant | 5 | Minimal, refined, premium feel |
| Specialty | 5 | Purpose-built for specific contexts |

---

## Corporate Styles

Designed for business presentations, investor decks, and internal reports. Safe for all audiences,
brand-neutral unless customized.

| Style | Description | Best For |
|-------|-------------|----------|
| `corporate-blue` | Navy + white, sans-serif headings | Executive briefings, board decks |
| `corporate-slate` | Dark slate + accent orange | Strategy presentations, OKR reviews |
| `corporate-minimal` | White + black, maximum whitespace | Consulting deliverables, proposals |
| `corporate-warm` | Warm gray + gold accents | Sales decks, client presentations |
| `corporate-bold` | High-contrast black + brand color | Product launches, announcements |

---

## Academic Styles

Optimized for conference talks, thesis defenses, and lecture slides. Emphasizes readability and
content density over visual flair.

| Style | Description | Best For |
|-------|-------------|----------|
| `academic-clean` | White background, serif headings, Linux fonts | Conference talks, seminars |
| `academic-metropolis` | Metropolis Beamer theme port | Academic PDF presentations |
| `academic-dark` | Dark background, high contrast | Lecture halls, large screens |
| `academic-journal` | Two-column layout, citation-ready | Paper presentations, reviews |
| `academic-poster` | Large text, section blocks | Conference posters (A0/A1) |

---

## Creative Styles

High visual impact for marketing, design reviews, and creative pitches. Uses bold typography,
gradients, and expressive color.

| Style | Description | Best For |
|-------|-------------|----------|
| `creative-gradient` | Vibrant gradient backgrounds | Marketing pitches, brand reveals |
| `creative-duotone` | Two-color photo treatment | Photography, portfolio reviews |
| `creative-typographic` | Large display type, minimal imagery | Design critiques, brand identity |
| `creative-dark-pop` | Dark background + neon accents | Product demos, startup pitches |
| `creative-editorial` | Magazine-style layouts | Content strategy, editorial reviews |

---

## Technical Styles

Built for developer talks, architecture reviews, and technical deep-dives. Code blocks are
first-class citizens with syntax highlighting.

| Style | Description | Best For |
|-------|-------------|----------|
| `tech-dark` | Dark theme, monospace accents, syntax highlighting | Engineering talks, demos |
| `tech-terminal` | Terminal-inspired, green-on-black | CLI tools, DevOps, security |
| `tech-blueprint` | Blueprint grid, technical diagrams | Architecture reviews, system design |
| `tech-minimal` | Clean white, code-first layout | API docs, developer onboarding |
| `tech-hacker` | High-contrast, dense information | CTF talks, security research |

---

## Elegant Styles

Refined and minimal. Lets content breathe. Suited for premium product launches, design
showcases, and high-stakes presentations.

| Style | Description | Best For |
|-------|-------------|----------|
| `elegant-white` | Pure white, thin typography, generous margins | Luxury products, design awards |
| `elegant-cream` | Warm off-white, serif body text | Publishing, editorial, culture |
| `elegant-charcoal` | Dark charcoal + gold, premium feel | Finance, legal, high-stakes pitches |
| `elegant-rose` | Soft rose + black, contemporary | Fashion, lifestyle, consumer brands |
| `elegant-mono` | Monochrome photography, minimal text | Art direction, photography |

---

## Specialty Styles

Purpose-built for specific contexts that don't fit the standard categories.

| Style | Description | Best For |
|-------|-------------|----------|
| `data-viz` | Optimized for charts and graphs, neutral backgrounds | Data reports, analytics reviews |
| `scientific-poster` | A0 poster layout, abstract + results blocks | Academic conference posters |
| `pitch-deck` | VC-style 12-slide structure, metric callouts | Startup fundraising |
| `workshop` | Activity-friendly, large prompts, breakout sections | Workshops, training sessions |
| `keynote-style` | Full-bleed imagery, large type | Keynote talks, product launches |

---

## Quick Selection Table

Use this table to find the right style for your context at a glance.

| Context | Recommended Style |
|---------|-------------------|
| Board / executive meeting | `corporate-blue` or `corporate-minimal` |
| Sales / client pitch | `corporate-warm` or `pitch-deck` |
| Conference talk (academic) | `academic-clean` or `academic-metropolis` |
| Conference talk (technical) | `tech-dark` or `tech-blueprint` |
| Thesis defense | `academic-clean` |
| Startup fundraising | `pitch-deck` or `creative-dark-pop` |
| Product launch | `keynote-style` or `corporate-bold` |
| Developer talk / demo | `tech-dark` or `tech-terminal` |
| Architecture review | `tech-blueprint` |
| Data / analytics report | `data-viz` |
| Workshop / training | `workshop` |
| Marketing / brand | `creative-gradient` or `creative-typographic` |
| Academic poster | `scientific-poster` or `academic-poster` |
| Premium / luxury | `elegant-white` or `elegant-charcoal` |

---

## Using Styles

```bash
# Specify style by name
/slides "Q3 Results" --style corporate-blue

# Describe the look you want (command selects best match)
/slides "Q3 Results" --style "professional, blue, minimal"

# Apply to a specific engine
/slides "Architecture Overview" --engine marp --style tech-blueprint
```

CSS theme files for Marp are in `modules/slides/templates/marp/`. Beamer themes are in
`modules/slides/templates/beamer/`.
