# Aesthetic Presets

> 5 named aesthetic presets with CSS custom property definitions.
> Each preset defines 8 core variables that control all slide theming.
> Apply by setting `:root` overrides or scoping to a `.theme-*` class on the `.slide` element.

---

## Variable Reference

All presets define the same 8 CSS custom properties:

| Variable | Role |
|----------|------|
| `--bg-primary` | Main slide background |
| `--bg-secondary` | Subtle inset areas, code blocks, alternate rows |
| `--bg-dark` | Title slides, section breaks, high-contrast overlays |
| `--text-primary` | Body text and primary headings |
| `--text-secondary` | Captions, metadata, secondary labels |
| `--text-light` | Text on dark surfaces (`--bg-dark`) |
| `--accent` | Single key-color for emphasis, markers, CTA |
| `--border` | Subtle dividers, table lines, card edges |

---

## Preset 1: Blueprint

Technical drawing aesthetic: drafting-table blue ground, crisp white linework, and measured cyan accents. Mimics engineering plans, architecture sheets, and CAD overlays.

**Best for**: Architecture walkthroughs, system diagrams, infrastructure reviews, process maps.

```css
:root {
  --bg-primary:    #0D2A45;
  --bg-secondary:  #12365A;
  --bg-dark:       #071A2B;
  --text-primary:  #EAF4FF;
  --text-secondary:#9FB7CC;
  --text-light:    #FFFFFF;
  --accent:        #53D1FF;
  --border:        #2F5E86;
}
```

**Typography pairing**: `"Space Mono", "IBM Plex Mono", ui-monospace` for headings and labels; `"Public Sans", ui-sans-serif` for body copy.
**Tone**: Precise, engineered, schematic.
**Note**: Optional background micro-grid should stay low contrast so text remains dominant.

---

## Preset 2: Editorial

High typographic contrast with serif-forward rhythm, warm paper whites, and earth-toned neutrals plus a restrained crimson accent. Feels like premium print magazine or long-form newspaper layout.

**Best for**: Keynotes, strategy narratives, media briefings, storytelling-heavy talks.

```css
:root {
  --bg-primary:    #FFFEF9;
  --bg-secondary:  #F2EDE3;
  --bg-dark:       #1A1713;
  --text-primary:  #191611;
  --text-secondary:#6C5B4E;
  --text-light:    #FFF9F1;
  --accent:        #B13A2F;
  --border:        #D8CCBB;
}
```

**Typography pairing**: `"Playfair Display", "EB Garamond", ui-serif` for display headings; `"Source Serif 4", ui-serif` for body.
**Tone**: Confident, literary, human.
**Note**: Keep accent usage sparse (one major callout per slide) for editorial discipline.

---

## Preset 3: Paper/ink

Warm cream canvas with sepia and charcoal text values. Organic, handwritten-adjacent character with understated brown borders for notebook-like framing.

**Best for**: Workshop decks, reflective talks, design process journals, teaching materials.

```css
:root {
  --bg-primary:    #FAF7F0;
  --bg-secondary:  #F2EBDD;
  --bg-dark:       #3A2F28;
  --text-primary:  #2F241D;
  --text-secondary:#7A6558;
  --text-light:    #FDF8EF;
  --accent:        #8C5A3C;
  --border:        #CDB7A0;
}
```

**Typography pairing**: `"Caveat", "Patrick Hand", cursive` for accent labels; `"Lora", ui-serif` for headings; `"Source Sans 3", ui-sans-serif` for body.
**Tone**: Warm, tactile, reflective.
**Note**: Reserve handwritten font for short labels only; keep paragraphs in serif/sans for readability.

---

## Preset 4: Monochrome

Terminal-like dark canvas with grayscale hierarchy and a single phosphor-green accent. Purposefully constrained palette designed for signal over decoration.

**Best for**: CLI demos, incident postmortems, protocol briefings, minimal technical talks.

```css
:root {
  --bg-primary:    #0B0B0B;
  --bg-secondary:  #151515;
  --bg-dark:       #000000;
  --text-primary:  #E8E8E8;
  --text-secondary:#9A9A9A;
  --text-light:    #FFFFFF;
  --accent:        #9EFF6A;
  --border:        #2E2E2E;
}
```

**Typography pairing**: `"JetBrains Mono", "IBM Plex Mono", ui-monospace` for headings and body.
**Tone**: Stark, focused, command-line native.
**Note**: Keep only one accent hue active across charts, links, and callouts.

---

## Preset 5: IDE-inspired

Code editor aesthetics translated for slides: syntax-like contrast, dense dark backgrounds, and accent channels tuned for long technical sessions.

**Best for**: Live coding talks, developer education, API deep dives, architecture debug sessions.

```css
:root {
  --bg-primary:    #1E1E2E;
  --bg-secondary:  #25273A;
  --bg-dark:       #11111B;
  --text-primary:  #CDD6F4;
  --text-secondary:#A6ADC8;
  --text-light:    #F5F7FF;
  --accent:        #89B4FA;
  --border:        #45475A;
}
```

**Typography pairing**: `"Fira Code", "JetBrains Mono", ui-monospace` for code and headings; `"Atkinson Hyperlegible", ui-sans-serif` for prose blocks.
**Tone**: Immersive, technical, high-focus.
**IDE sub-variants**:
- `Dracula`: `#282A36`, `#44475A`, `#F8F8F2`, `#BD93F9`, `#FF79C6`
- `Nord`: `#2E3440`, `#3B4252`, `#ECEFF4`, `#88C0D0`, `#81A1C1`
- `Catppuccin`: `#1E1E2E`, `#313244`, `#CDD6F4`, `#89B4FA`, `#F5C2E7`
- `Solarized`: `#002B36`, `#073642`, `#93A1A1`, `#B58900`, `#2AA198`
- `Gruvbox`: `#282828`, `#3C3836`, `#EBDBB2`, `#FABD2F`, `#B8BB26`
- `One Dark`: `#282C34`, `#3E4451`, `#ABB2BF`, `#61AFEF`, `#E06C75`
- `Rose Pine` (Rosé Pine): `#191724`, `#26233A`, `#E0DEF4`, `#9CCFD8`, `#EB6F92`
**Note**: Pick one variant per deck; avoid mixing token systems across sections.

---

## Applying Presets

### Method A: Global Override

Apply a preset to the entire deck by overriding `:root`:

```css
/* In slide-deck.html <style> block */
:root {
  /* Paste preset variables here */
  --bg-primary: #0D2A45;
  /* ... */
}
```

### Method B: Scoped Class

Apply per-slide or per-section without affecting the whole deck:

```css
.theme-blueprint {
  --bg-primary:    #0D2A45;
  --bg-secondary:  #12365A;
  --bg-dark:       #071A2B;
  --text-primary:  #EAF4FF;
  --text-secondary:#9FB7CC;
  --text-light:    #FFFFFF;
  --accent:        #53D1FF;
  --border:        #2F5E86;
}
```

```html
<section class="slide theme-blueprint">
  <!-- Slide content with Blueprint preset -->
</section>
```

### Method C: Data Attribute (Agent-Generated Decks)

For programmatically generated decks, use a `data-theme` attribute and a single CSS rule:

```css
[data-theme="blueprint"]    { /* Blueprint variables    */ }
[data-theme="editorial"]    { /* Editorial variables    */ }
[data-theme="paper-ink"]    { /* Paper/ink variables    */ }
[data-theme="monochrome"]   { /* Monochrome variables   */ }
[data-theme="ide-inspired"] { /* IDE-inspired variables */ }
```

```html
<div id="deck" data-theme="blueprint">
  <!-- All slides inherit the preset -->
</div>
```
