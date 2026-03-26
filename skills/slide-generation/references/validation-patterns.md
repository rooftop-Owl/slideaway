## Section K — Validation Patterns

Always validate output before delivering to the user.

For PPTX outputs, structural inspection is mandatory. File-exists checks are not enough.

### Mandatory Structural Inspection (PPTX)

Run from repository root:

```bash
python3 modules/slides/tools/validate_pptx.py output.pptx
```

Template-first md2pptx mode (font inheritance allowed):

```bash
python3 modules/slides/tools/validate_pptx.py output.pptx --allow-font-inheritance
```

Hard-fail checks (must pass):

- Slide count > 0
- Aspect ratio close to 16:9 (~1.78)
- Title slide has separate text blocks for title/subtitle/author-date (>=3 non-empty text blocks)
- No empty slides
- No `font=None` runs unless `--allow-font-inheritance` is set

Warning checks (review before shipping):

- Shapes outside slide bounds
- Footer numbering partial or inconsistent

### Quick Inline Structural Check (fallback)

```python
from modules.slides.tools.slide_factory import validate_pptx_structure

result = validate_pptx_structure("output.pptx")
print("OK" if result.ok else "FAIL")
print("WARN:", result.warnings)
print("ERROR:", result.errors)
assert result.ok, "Structural validation failed"
```

### File Existence and Size

```bash
test -s output.pptx && echo "✓ PPTX generated" || echo "✗ PPTX missing or empty"
test -s output.pdf  && echo "✓ PDF generated"  || echo "✗ PDF missing or empty"
test -s output.html && echo "✓ HTML generated" || echo "✗ HTML missing or empty"
```

### PDF Page Count

```bash
pdfinfo output.pdf | grep "^Pages:"
```

### HTML Render Structure Check

```python
from html.parser import HTMLParser

class SlideCounter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slide_count = 0

    def handle_starttag(self, tag, attrs):
        if tag == "section":
            self.slide_count += 1

with open("output.html") as f:
    html = f.read()

counter = SlideCounter()
counter.feed(html)
print(f"✓ {counter.slide_count} <section> elements")
assert counter.slide_count > 0, "FAIL: no slide sections found"
```

### Engine Execution Checks

md2pptx:

```bash
python3 modules/slides/tools/md2pptx/md2pptx.py output.pptx < slides.md \
    && echo "✓ md2pptx completed" \
    || echo "✗ md2pptx failed"
```

Marp:

```bash
marp slides.md -o output.html && test -s output.html \
    && echo "✓ Marp HTML generated" \
    || echo "✗ Marp failed"
```

Beamer:

```bash
pdflatex -interaction=nonstopmode slides.tex \
    && test -s slides.pdf \
    && echo "✓ Beamer PDF compiled" \
    || echo "✗ Beamer compilation failed"
```

### Delivery Rule

- Do not ship when structural inspection reports any `FAIL`.
- If `WARN` exists, mention it explicitly in the delivery message.
- If you used md2pptx template mode with `--allow-font-inheritance`, state that validation mode in the report.
