## Section B — Marp CLI (Markdown → HTML / PDF / PPTX)

Marp converts Markdown to presentation-ready HTML, PDF, or PPTX. Fast, zero-config, beautiful defaults.

### Installation

```bash
npm install -g @marp-team/marp-cli
# or use npx: npx @marp-team/marp-cli slides.md -o slides.html
```

### Frontmatter

```markdown
---
marp: true
theme: slides-default
paginate: true
size: 16:9              # 16:9 | 4:3 | A4
backgroundColor: white
---
```

If you use a module-bundled theme, pass it via `--theme-set` so Marp can resolve the theme name.

### Slide Structure

```markdown
---
marp: true
theme: default
paginate: true
size: 16:9
---

# Title Slide

Author · Institution · Date

---

## Slide Two

- Bullet point one
- Bullet point two
  - Sub-bullet

---

<!-- _class: lead -->

# Section Break

---

## Two-Column Layout

<div class="columns">
<div>

### Left Column
- Item A
- Item B

</div>
<div>

### Right Column
- Item C
- Item D

</div>
</div>
```

### Directives

| Directive | Scope | Effect |
|-----------|-------|--------|
| `<!-- _class: lead -->` | Single slide | Center all content |
| `<!-- _backgroundColor: #1a1a2e -->` | Single slide | Override background |
| `<!-- _color: white -->` | Single slide | Override text color |
| `<!-- paginate: false -->` | Single slide | Hide page number |
| `<!-- header: "My Talk" -->` | Global | Add header to all slides |
| `<!-- footer: "Author · 2026" -->` | Global | Add footer to all slides |

### Images

```markdown
<!-- Background image, right 40% -->
![bg right:40%](image.png)

<!-- Background image, fit to slide -->
![bg fit](chart.svg)

<!-- Background image, cover with opacity -->
![bg opacity:0.3](background.jpg)

<!-- Inline image with width -->
![w:400px](diagram.png)

<!-- Multiple backgrounds (split) -->
![bg left](left.png)
![bg right](right.png)
```

### Speaker Notes

```markdown
## My Slide

Content here.

<!-- Speaker note: Mention the 2023 paper by Smith et al. -->
```

Notes are hidden in the presentation but visible in presenter mode.

### Auto-Fit Text

```markdown
## <!-- fit --> This Title Will Auto-Scale
```

### Commands

```bash
# Clean HTML export (recommended for screenshots)
marp slides.md -o slides.html \
  --bespoke.osc false \
  --bespoke.progress \
  --theme-set modules/slides/templates/marp \
  --theme slides-default

marp slides.md --pdf -o slides.pdf         # PDF
marp slides.md --pptx -o slides.pptx       # PPTX (non-editable images)

# Custom theme (bundled in this module)
marp slides.md -o slides.html \
  --bespoke.osc false \
  --theme-set modules/slides/templates/marp \
  --theme academic

marp -w slides.md                          # Watch mode (dev)
npx @marp-team/marp-cli slides.md -o slides.html  # Without global install
```

### ⚠️ PPTX WARNING

**Marp PPTX embeds rendered slide images — text is NOT editable in PowerPoint.**

Each slide becomes a flat image inside the PPTX container. You cannot:
- Edit text in PowerPoint
- Reformat bullets
- Change fonts or colors
- Add speaker notes in PowerPoint

For editable PPTX, use **md2pptx** (Section C) or **python-pptx** (Section D) instead.

The `--pptx-editable` flag exists but requires LibreOffice installed and is experimental.

**Rule**: Use Marp PPTX only when the recipient doesn't need to edit the file.

### Custom Themes

```css
/* academic.css */
@import 'default';

section {
  font-family: 'Source Serif Pro', serif;
  font-size: 28px;
}

section.lead {
  background: #1a3a5c;
  color: white;
}

h1 {
  color: #1a3a5c;
  border-bottom: 2px solid #1a3a5c;
}
```

Use with: `marp --theme academic.css slides.md -o out.html`

---

