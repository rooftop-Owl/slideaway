## Section G — Standalone HTML (Individual HTML Files)

For maximum design control, generate individual HTML files per slide. Useful when each slide needs unique layout, custom animations, or embedded interactives.

### Naming Convention

Use numeric prefix + semantic suffix for ordering and partial regeneration:

```
slide-01-title.html
slide-02-agenda.html
slide-03-motivation.html
slide-04a-method-overview.html
slide-04b-method-detail.html
slide-05-results.html
slide-06-discussion.html
slide-07-conclusion.html
slide-08-backup-data.html
```

The `a/b` suffix allows inserting sub-slides without renumbering.

### Slide Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Slide: Title</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            width: 1920px;
            height: 1080px;
            font-family: 'Source Sans Pro', 'Helvetica Neue', sans-serif;
            background: white;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .slide-header {
            background: #1a3a5c;
            color: white;
            padding: 20px 40px;
            font-size: 36px;
            font-weight: 600;
        }
        .slide-body {
            flex: 1;
            padding: 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .slide-footer {
            padding: 10px 40px;
            font-size: 18px;
            color: #666;
            border-top: 1px solid #eee;
            display: flex;
            justify-content: space-between;
        }
        ul { padding-left: 1.5em; }
        li { margin: 0.5em 0; font-size: 28px; }
        .columns { display: flex; gap: 40px; }
        .column { flex: 1; }
    </style>
</head>
<body>
    <div class="slide-header">Slide Title</div>
    <div class="slide-body">
        <ul>
            <li>Bullet point one</li>
            <li>Bullet point two</li>
        </ul>
    </div>
    <div class="slide-footer">
        <span>Author · Institution</span>
        <span>5 / 20</span>
    </div>
</body>
</html>
```

Module includes a ready-to-use template at:
`modules/slides/templates/html/slide-template.html`

### When to Use

- Each slide has a completely different layout
- Embedding interactive D3.js or Plotly charts
- Custom CSS animations per slide
- Generating slides from a template engine (Jinja2)

### Jinja2 Generation Pattern

```python
from jinja2 import Environment, FileSystemLoader
import json

env = Environment(loader=FileSystemLoader("templates/"))
template = env.get_template("slide-template.html")

slides = json.load(open("slides.json"))
for i, slide in enumerate(slides, 1):
    html = template.render(**slide, slide_num=i, total=len(slides))
    with open(f"slide-{i:02d}-{slide['slug']}.html", "w") as f:
        f.write(html)
```

---

## Section H — RISE/Jupyter (Notebook → Slides)

RISE turns Jupyter notebooks into live slideshows. Best for presentations where you want to run code live during the talk.

### Installation

```bash
pip install rise
# or
conda install -c conda-forge rise
```

### Cell Tagging

In Jupyter, use the "Slideshow" cell toolbar (View → Cell Toolbar → Slideshow):

| Tag | Effect |
|-----|--------|
| Slide | New horizontal slide |
| Sub-Slide | New vertical slide (press down) |
| Fragment | Reveal on click within current slide |
| Skip | Hidden in slideshow, visible in notebook |
| Notes | Speaker notes (shown in presenter mode) |

### Notebook Metadata

Add to notebook metadata (Edit → Edit Notebook Metadata):

```json
{
  "rise": {
    "scroll": true,
    "theme": "white",
    "transition": "slide",
    "slideNumber": true,
    "enable_chalkboard": true,
    "autolaunch": false
  }
}
```

### Activation

1. Open notebook in Jupyter
2. Click "Enter RISE Slideshow" button (bar chart icon in toolbar)
3. Or press `Alt+R`

### Live Code in Slides

```python
# Cell tagged as "Slide"
import matplotlib.pyplot as plt
import numpy as np

# This code runs live during the presentation
x = np.linspace(0, 2*np.pi, 100)
plt.plot(x, np.sin(x))
plt.title("Live sine wave")
plt.show()
```

### Export to Static Slides

```bash
# Export to reveal.js HTML (static, no live code)
jupyter nbconvert --to slides notebook.ipynb --post serve

# Export to PDF
jupyter nbconvert --to slides notebook.ipynb
# Then print from browser with ?print-pdf
```

### When to Use

- Live code demonstrations during talks
- Data exploration presentations where audience may ask "what if?"
- Teaching sessions where running code is part of the lesson
- Reproducible research presentations

---

