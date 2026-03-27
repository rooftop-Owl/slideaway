## Section C — md2pptx (Markdown → Editable PPTX) [TEMPLATE-FIRST ENGINE]

md2pptx is a strong option when you need to pour Markdown content into an existing `.pptx` template quickly.

md2pptx is **not** the default engine for styled presentations. For presentation-ready formatting control, use python-pptx + SlideFactory (Section D).

### Where md2pptx Fits Best

| Property | md2pptx | python-pptx + SlideFactory |
|----------|---------|----------------------------|
| Text editable in PowerPoint | ✅ Yes | ✅ Yes |
| Template inheritance from existing `.pptx` | ✅ Excellent | ✅ Excellent |
| Styling control without template | ⚠️ Limited | ✅ Full |
| Programmatic layout control | ⚠️ Low | ✅ High |
| Data-driven charts/tables | ⚠️ Limited | ✅ High |
| Requires LaTeX | ❌ No | ❌ No |

### Installation

**NOT on PyPI.** Bundled as a git clone in `modules/slides/tools/md2pptx/`.

```bash
# Included in module — no separate install needed.
# To update: git -C modules/slides/tools/md2pptx pull
# Requires: pip install python-pptx
pip install python-pptx  # Only dependency
```

After plugin installation, also available via symlink:
```bash
python3 .claude/tools/md2pptx/md2pptx.py output.pptx < slides.md
```

### Invocation

```bash
# Standard invocation (stdin → file)
python3 modules/slides/tools/md2pptx/md2pptx.py output.pptx < slides.md

# With explicit input file
python3 modules/slides/tools/md2pptx/md2pptx.py output.pptx slides.md

# Via symlink after plugin installation
python3 .claude/tools/md2pptx/md2pptx.py output.pptx < slides.md
```

**⚠️ Invocation anti-patterns** (do not use these):
 Module invocation (`-m md2pptx`) fails — md2pptx is a standalone script, not a Python module
 Installing via pip fails — md2pptx is NOT on PyPI; use the bundled copy in `modules/slides/tools/md2pptx/`

### Markdown Format

```markdown
template: path/to/template.pptx

### Slide Title

* Bullet point one
  * Sub-bullet indented
  * Another sub-bullet
* Bullet point two
* Bullet point three

---

### Second Slide

Some paragraph text here.

* More bullets
* Another point

---

### Two-Column Slide
<!-- md2pptx: contentsplitdirn: h -->

* Left column content
* More left content

---split---

* Right column content
* More right content

---

### Image Slide

![]( plots/figure.png)

---

### Card Layout
<!-- md2pptx: cardlayout: 2x2 -->

#### Card One
Content for card one.

#### Card Two
Content for card two.

#### Card Three
Content for card three.

#### Card Four
Content for card four.
```

### Key Directives

| Directive | Effect |
|-----------|--------|
| `template: path/to/template.pptx` | Use corporate template for branding |
| `<!-- md2pptx: contentsplitdirn: h -->` | Horizontal split (two columns) |
| `<!-- md2pptx: contentsplitdirn: v -->` | Vertical split (two rows) |
| `<!-- md2pptx: cardlayout: 2x2 -->` | 2×2 card grid layout |
| `<!-- md2pptx: cardlayout: 1x3 -->` | 1×3 card layout |
| `---split---` | Split point for two-column slides |

### Template Support

The `template:` directive at the top of the Markdown file points to any `.pptx` file for brand consistency:

```markdown
template: /path/to/corporate-template.pptx

### Slide Title
...
```

The template's slide layouts, fonts, colors, and master slides are inherited. This is the primary way to ensure corporate branding.

Module includes templates at: `modules/slides/templates/pptx/`

### Known Limitations (must acknowledge before choosing md2pptx)

- Markdown emphasis such as `**bold**` may be flattened into plain text depending on template and parser path.
- `---` separators can create empty slides when section breaks are malformed.
- Default output may remain 4:3 if the input template is 4:3 and no widescreen template is supplied.
- Run-level fonts may stay `None` and inherit from master theme; this is acceptable only in template-first workflows.
- Proper title slide separation (title/subtitle/author/date in distinct shapes) is not guaranteed.

If these are unacceptable for the task, switch to python-pptx + SlideFactory.

### Output Properties

- Real text boxes — fully editable in PowerPoint and LibreOffice
- Real bullet hierarchies — indent levels preserved
- Speaker notes — accessible in presenter mode
- Images — embedded, not linked
- Tables — native PPTX tables

### Reference

Source: https://github.com/MartinPacker/md2pptx (MIT License, standalone script, bundled — NOT on PyPI)

---

