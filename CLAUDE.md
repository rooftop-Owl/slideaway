# slideaway

Presentation plugin for Claude Code — multi-agent pipeline (slide-coach + slide-reviewer + slide-qa), 7 engines, 30 styles, discovery-first progressive disclosure architecture.

## What This Plugin Provides

- **3 skills**: slide-generation (Phase 0 discovery-first pipeline: audience analysis, narrative structure, Slide Brief, outline → Phase 2 content creation with 7 engines + progressive disclosure), presentation-design-styles (30 styles, mood mapping, design foundations), presentation-visual-qa (render + inspect + delivery intelligence + automation scripts)
- **3 agents**:
  - **slide-coach**: Phase 0 discovery/planning — audience analysis, narrative structure, Slide Brief, outline generation
  - **slide-reviewer**: Phase 3 content quality — 5-dimension review (narrative, messaging, completeness, audience calibration, ask alignment)
  - **slide-qa**: Phase 4 design quality — 4-dimension scoring (readability, aesthetics, conciseness, fidelity), iterative fix loop (max 3 rounds)
- **1 command**: /slides (with --preview, --refine, --style flags)
- **8 tools**: slide_factory.py, validate_pptx.py (+ --duration, --quiet), thumbnail_grid.py, pdf_to_images.py, slides_to_pdf.py, html2pptx/, pptx_editor/, md2pptx/
- **1 hook**: PostToolUse PPTX validation (early-exit for non-.pptx)

## Key Conventions

- **Progressive disclosure**: Core skill is ~330 lines. Engine-specific details live in `skills/slide-generation/references/engine-{name}.md`. Academic references (talk-types, timing, data-viz) load conditionally. Design foundations and delivery intelligence cross-reference from sibling skills.
- **Skills format**: All skills use subdirectory format (`skills/{name}/SKILL.md`), not flat files.
- **Style presets**: 30 unique Theme objects in `tools/slide_factory.py` STYLE_PRESETS dict. Each must have distinct primary+accent colors.
- **Anti-AI-slop**: Banned fonts (Inter, Roboto, Arial), banned colors (#6366f1), enforced in both visual-qa skill and validate_pptx.py.
- **Opt-in interactivity**: --preview and --refine are NEVER default. Default /slides behavior must remain non-interactive.
- **Viewport fitting**: All HTML templates enforce 100vh + overflow:hidden + clamp() sizing.
- **Producer ≠ Verifier**: slide-coach plans, the orchestrating agent generates, slide-reviewer and slide-qa inspect independently. Never same agent for both.
- **Portable paths**: Hooks use ${CLAUDE_PLUGIN_ROOT}, never hardcoded paths.

## Dependencies

- Core: python-pptx (required)
- QA: Pillow, PyMuPDF, NumPy (optional — `pip install slideaway[qa]`)
- Rendering: Playwright (optional — `pip install slideaway[browser]`)
- Engines: Marp CLI, pandoc, pdflatex, wkhtmltoimage (all optional per engine)

## Testing

```bash
python3 -m pytest tests/test_backward_compat.py -v  # 15 tests
```
