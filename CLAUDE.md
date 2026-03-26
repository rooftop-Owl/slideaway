# slideaway

Presentation plugin for Claude Code — 7 engines, 30 styles, progressive disclosure architecture.

## What This Plugin Provides

- **3 skills**: slide-generation (progressive disclosure: 318-line core + 9 reference files), presentation-design-styles (30 styles, mood mapping), presentation-visual-qa (render + inspect)
- **2 agents**: slide-designer (aesthetic direction), slide-qa (visual quality assurance)
- **1 command**: /slides (with --preview, --refine, --style flags)
- **6 tools**: slide_factory.py, validate_pptx.py, thumbnail_grid.py, html2pptx/, pptx_editor/, md2pptx/
- **1 hook**: PostToolUse PPTX validation (early-exit for non-.pptx)

## Key Conventions

- **Progressive disclosure**: Core skill is ~318 lines. Engine-specific details live in `skills/slide-generation/references/engine-{name}.md`. Agents load references on demand per phase.
- **Skills format**: All skills use subdirectory format (`skills/{name}/SKILL.md`), not flat files.
- **Style presets**: 30 unique Theme objects in `tools/slide_factory.py` STYLE_PRESETS dict. Each must have distinct primary+accent colors.
- **Anti-AI-slop**: Banned fonts (Inter, Roboto, Arial), banned colors (#6366f1), enforced in both visual-qa skill and validate_pptx.py.
- **Opt-in interactivity**: --preview and --refine are NEVER default. Default /slides behavior must remain non-interactive.
- **Viewport fitting**: All HTML templates enforce 100vh + overflow:hidden + clamp() sizing.
- **Producer ≠ Verifier**: slide-designer generates, slide-qa inspects. Never same agent for both.
- **Portable paths**: Hooks use ${CLAUDE_PLUGIN_ROOT}, never hardcoded paths.

## Dependencies

- Core: python-pptx (required)
- QA: Pillow (optional, for thumbnail_grid.py)
- Rendering: Playwright (optional, for Path B visual QA)
- Engines: Marp CLI, pandoc, pdflatex, wkhtmltoimage (all optional per engine)

## Testing

```bash
python3 -m pytest tests/test_backward_compat.py -v  # 15 tests
```
