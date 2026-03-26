## Section E — reveal.js (Markdown → Interactive HTML)

reveal.js creates interactive web presentations with animations, fragments, vertical slides, and presenter mode. Best for web-first presentations.

### Two Generation Paths

**Path 1: pandoc (recommended)**

If your environment does not have `pandoc`, you cannot use `--embed-resources`.
In that case:

- If offline is required: use **reveal-md** and export a static site (local assets)
- If offline is not required: use the CDN-based single-file pattern (below)

```bash
# Single self-contained HTML file
pandoc slides.md -t revealjs -s -o slides.html \
    --embed-resources \
    -V theme=white \
    -V slideNumber=true \
    -V transition=slide

# With custom CSS
pandoc slides.md -t revealjs -s -o slides.html \
    --embed-resources \
    --css custom.css \
    -V theme=white
```

**Path 2: reveal-md (Markdown-native)**

```bash
# Install
npm install -g reveal-md

# Dev server with live reload
npx reveal-md slides.md --theme white

# Export to static site
npx reveal-md slides.md --static _site

# Export to PDF
npx reveal-md slides.md --print slides.pdf
```

### Markdown Format (reveal-md)

```markdown
---
title: My Presentation
theme: white
revealOptions:
    transition: slide
    slideNumber: true
    controls: true
---

# Title Slide

Subtitle · Author · Date

---

## Regular Slide

- Bullet one
- Bullet two
- Bullet three

Note: Speaker notes go here — visible in presenter mode (press S)

---

## Vertical Slide Group

Content on this slide.

--

### Sub-slide (vertical)

Press down arrow to navigate.

---

## Fragment Animations

- <!-- .element: class="fragment" --> Appears on click
- <!-- .element: class="fragment fade-in-then-out" --> Fades in then out
- <!-- .element: class="fragment highlight-red" --> Highlights red

---

## Two Columns

<div style="display:flex; gap:2em">
<div>

### Left
- Item A
- Item B

</div>
<div>

### Right
- Item C
- Item D

</div>
</div>
```

### CDN-Based Single-File Pattern

For maximum portability, generate a single HTML file with CDN assets:

```html
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Presentation</title>
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css">
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/theme/white.css">
</head>
<body>
    <div class="reveal">
        <div class="slides">
            <section>
                <h1>Title Slide</h1>
                <p>Subtitle · Author</p>
            </section>
            <section>
                <h2>Content Slide</h2>
                <ul>
                    <li>Bullet one</li>
                    <li>Bullet two</li>
                </ul>
                <aside class="notes">Speaker notes here.</aside>
            </section>
            <section>
                <!-- Vertical slide group -->
                <section><h2>Vertical A</h2></section>
                <section><h2>Vertical B</h2></section>
            </section>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.js"></script>
    <script>
        Reveal.initialize({
            hash: true,
            slideNumber: true,
            transition: 'slide',
            plugins: []
        });
    </script>
</body>
</html>
```

### Features Beyond Marp

| Feature | How |
|---------|-----|
| Auto-Animate (FLIP) | Add `data-auto-animate` to consecutive sections |
| Fragments | `<!-- .element: class="fragment" -->` |
| Vertical slides | Nest `<section>` inside `<section>` |
| Presenter mode | Press `S` — shows notes, timer, next slide |
| Overview mode | Press `O` — bird's eye view |
| Fullscreen | Press `F` |
| Zoom | Press `Alt+Click` |

### Auto-Animate Example

```html
<section data-auto-animate>
    <h2>Before</h2>
    <p data-id="text">Initial text</p>
</section>
<section data-auto-animate>
    <h2>After</h2>
    <p data-id="text">Animated text</p>  <!-- FLIP animation -->
</section>
```

### PDF Export

```bash
# Append ?print-pdf to URL, then print via headless browser
chromium --headless --print-to-pdf=slides.pdf \
    "file:///path/to/slides.html?print-pdf"

# Or via reveal-md
npx reveal-md slides.md --print slides.pdf
```

---

