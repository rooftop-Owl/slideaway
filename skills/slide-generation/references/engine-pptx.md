## Section D — python-pptx (Python → Editable PPTX) [STYLED DEFAULT]

python-pptx + SlideFactory is the default path for editable decks when visual quality matters.

### When to Use (and when not to)

| Scenario | Use |
|----------|-----|
| Styled editable deck (16:9, explicit fonts, hierarchy) | python-pptx + SlideFactory |
| Programmatic generation from JSON/API/dataframes | python-pptx + SlideFactory |
| Mixed text + charts + figures | python-pptx + SlideFactory |
| Corporate template with exact shape positioning | python-pptx + SlideFactory |
| Quick Markdown import into existing template | md2pptx |

### Production-Ready Factory (Bundled)

Use the shipped utility instead of writing a skeleton from scratch:

`modules/slides/tools/slide_factory.py`

Provided components:

| Component | Purpose |
|----------|---------|
| `Theme` | Palette + typography defaults (navy/teal, explicit fonts) |
| `Bullet` | Structured bullet entries with `level` and `bold_prefix` |
| `SlideFactory` | Title/bullet/image/chart builders with 16:9 layout helpers |
| `validate_pptx_structure` | Shared structural checks used by validator CLI |

### Minimal Workflow

```python
from modules.slides.tools.slide_factory import SlideFactory, Bullet

factory = SlideFactory()

factory.add_title_slide(
    title="CLIMADA",
    subtitle="Tropical Cyclone Wind Damage Risk Assessment",
    author="Research Team",
    date="2026-02-24",
    region="South Korea",
)

factory.add_bullet_slide(
    "Methodology",
    [
        Bullet("Hazard: IBTrACS tracks + Holland wind model", bold_prefix="Hazard:"),
        Bullet("Exposure: LitPop GDP-weighted assets", bold_prefix="Exposure:"),
        Bullet("Vulnerability: Emanuel (2011) impact function", bold_prefix="Vulnerability:"),
    ],
    slide_num=2,
    total_slides=10,
)

factory.add_image_slide(
    "Spatial Risk Map",
    "results/figures/publication/fig03_spatial_risk_map.png",
    caption="Annual average impact by province",
    slide_num=3,
    total_slides=10,
)

factory.save("output.pptx")
```

### Theme Overrides

```python
from pptx.dml.color import RGBColor
from modules.slides.tools.slide_factory import SlideFactory, Theme

theme = Theme(
    primary=RGBColor(0x12, 0x2B, 0x40),
    accent=RGBColor(0x0E, 0x96, 0xBE),
    font_name="Aptos",
)

factory = SlideFactory(theme=theme)
```

- Use `Theme.from_style('name')` for curated style presets — see `presentation-design-styles` skill for the full catalog.
### Template Mode

If you must preserve a specific corporate master:

```python
factory = SlideFactory(template_path="corporate-template.pptx")
```

Use `force_widescreen=True` only when you intentionally want to override template aspect ratio.

### Image Fitting Behavior

- If Pillow is available, images are measured and fitted to the available body area.
- If Pillow is missing, the factory falls back to width-first fitting and still centers the image.

### Limitations

- No animations (use reveal.js or manual PowerPoint edits)
- No SmartArt generation
- SVG should be converted to PNG/EMF before insertion
- Highly custom layouts still require explicit shape positioning

---

