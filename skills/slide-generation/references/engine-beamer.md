## Section F — LaTeX Beamer (LaTeX → PDF)

Beamer is the gold standard for academic conference talks. Full LaTeX power: equations, citations, precise layout, professional typography.

### Basic Template

```latex
\documentclass[aspectratio=169]{beamer}

\usetheme{metropolis}       % Clean, modern — prefer over default
\usepackage{booktabs}       % Professional tables
\usepackage{graphicx}       % Figures
\usepackage{siunitx}        % SI units
\usepackage{hyperref}       % Links

\title{Climate Risk Assessment Results}
\subtitle{Using CLIMADA v4}
\author{Author Name}
\institute{ETH Zürich}
\date{\today}

\begin{document}

\maketitle

\begin{frame}{Outline}
    \tableofcontents
\end{frame}

\section{Introduction}

\begin{frame}{Motivation}
    \begin{itemize}
        \item Climate-related losses increasing globally
        \item Need: quantitative risk assessment tools
        \item Approach: CLIMADA impact modeling
    \end{itemize}
    \note{Speaker notes go here — only visible in presenter mode}
\end{frame}

\section{Results}

\begin{frame}{Impact by Scenario}
    \begin{figure}
        \centering
        \includegraphics[width=0.8\textwidth]{plots/scenario_comparison.pdf}
        \caption{Annual expected impact under SSP scenarios}
    \end{figure}
\end{frame}

\begin{frame}{Two-Column Layout}
    \begin{columns}
        \begin{column}{0.5\textwidth}
            \begin{itemize}
                \item AAI increases 2× under SSP5-8.5
                \item Coastal regions most affected
            \end{itemize}
        \end{column}
        \begin{column}{0.5\textwidth}
            \includegraphics[width=\textwidth]{plots/map.pdf}
        \end{column}
    \end{columns}
\end{frame}

\section{Conclusion}

\begin{frame}{Summary}
    \begin{block}{Key Finding}
        Annual expected impact doubles under high-emission scenarios.
    \end{block}
    \begin{alertblock}{Policy Implication}
        Adaptation investment needed now.
    \end{alertblock}
\end{frame}

\end{document}
```

### Known-Good Preambles (USE VERBATIM)

Each Beamer template has a tested, minimal preamble. The generator MUST use these verbatim — never invent custom `\setbeamertemplate` overrides. Style customization is done exclusively via `\setbeamercolor` and `\definecolor`.

**Rule**: Theme handles structure. Colors handle branding. Never mix the two.

#### Metropolis (default)

```latex
\documentclass[aspectratio=169,11pt]{beamer}
\usetheme{metropolis}
% Style: color overrides ONLY
\definecolor{BrandPrimary}{HTML}{2C3E6B}
\definecolor{BrandAccent}{HTML}{E74C3C}
\setbeamercolor{frametitle}{bg=BrandPrimary, fg=white}
\setbeamercolor{progress bar}{fg=BrandPrimary}
\setbeamercolor{alerted text}{fg=BrandAccent}
\setbeamertemplate{navigation symbols}{}
% TikZ (safe with metropolis)
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning}
```

#### Conference (Madrid/beaver)

```latex
\documentclass[aspectratio=169,11pt]{beamer}
\usetheme{Madrid}
\usecolortheme{beaver}
% Style: color overrides ONLY
\definecolor{BrandPrimary}{HTML}{8B0000}
\setbeamercolor{structure}{fg=BrandPrimary}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}[frame number]
% TikZ (safe with Madrid)
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning}
```

#### Seminar (Madrid/dolphin)

```latex
\documentclass[aspectratio=169,11pt]{beamer}
\usetheme{Madrid}
\usecolortheme{dolphin}
% Style: color overrides ONLY
\definecolor{BrandPrimary}{HTML}{1A5276}
\setbeamercolor{structure}{fg=BrandPrimary}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}[frame number]
% Section dividers (safe — uses built-in template, not custom)
\AtBeginSection[]{
  \begin{frame}
    \vfill\centering
    \usebeamerfont{title}\insertsectionhead\par
    \vfill
  \end{frame}
}
% TikZ (safe with Madrid)
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning}
```

#### Defense (Boadilla/whale)

```latex
\documentclass[aspectratio=169,11pt]{beamer}
\usetheme{Boadilla}
\usecolortheme{whale}
% Style: color overrides ONLY
\definecolor{BrandPrimary}{HTML}{1B2A4A}
\setbeamercolor{structure}{fg=BrandPrimary}
\setbeamertemplate{navigation symbols}{}
% Frame number footline (safe — uses built-in mechanism)
\setbeamertemplate{footline}{
  \hfill\insertframenumber{}/\inserttotalframenumber\hspace*{2ex}\vskip2pt
}
% Section dividers
\AtBeginSection[]{
  \begin{frame}
    \vfill\centering
    \usebeamerfont{title}\insertsectionhead\par
    \vfill
  \end{frame}
}
% TikZ (safe with Boadilla)
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning}
```

#### Adapting Colors for a Style Preset

To apply a slideaway style preset (#16, #17, etc.) to Beamer:
1. Look up the preset's `primary`, `accent`, and `text` hex values from `presentation-design-styles/references/styles.md`
2. `\definecolor{BrandPrimary}{HTML}{...}` with the preset's primary color
3. `\definecolor{BrandAccent}{HTML}{...}` with the preset's accent color
4. Apply via `\setbeamercolor` — NEVER via `\setbeamertemplate`
5. Do NOT set `background canvas` or `normal text` bg colors — let the theme handle backgrounds
### Compilation

**Preferred: `tectonic`** (auto-downloads packages, no TikZ version issues):
```bash
# Single command — handles all passes, bibliography, and package downloads
tectonic slides.tex
```

**Fallback: `pdflatex`** (requires full TeX Live installation):
```bash
# Standard (two passes for references)
pdflatex slides.tex && pdflatex slides.tex

# Unicode support (recommended for international content)
xelatex slides.tex

# With bibliography
pdflatex slides.tex && bibtex slides && pdflatex slides.tex && pdflatex slides.tex
```

### Known Issue: conda texlive-core + TikZ

> **`\tikzscope@linewidth` undefined** — conda's `texlive-core` package ships a minimal TeX distribution that lacks TikZ/PGF scope internals required by Beamer themes (Madrid, Boadilla, etc.). The format file (`pdflatex.fmt`) may also fail to generate (`Can't locate mktexlsr.pl in @INC`).
>
> **Do NOT** attempt to fix by downgrading Beamer themes — the issue is in the TeX distribution, not the templates.

### Installation Guide (by distro)

| Environment | Command | Notes |
|-------------|---------|-------|
| **tectonic (recommended)** | `conda install -c conda-forge tectonic` or `cargo install tectonic` | Zero-config: auto-downloads ALL packages on first compile. Works everywhere. |
| **Ubuntu/Debian** | `sudo apt install texlive-latex-extra texlive-fonts-recommended` | System TeX Live with Beamer + fonts |
| **Rocky/RHEL 8-9** | `sudo dnf install texlive-scheme-basic texlive-beamer` | NOT `scheme-medium` (doesn't exist on RHEL 8) |
| **Fedora** | `sudo dnf install texlive-scheme-medium` | Includes Beamer and metropolis |
| **macOS** | `brew install --cask mactex-no-gui` | Full TeX Live |
| **conda** | ⚠️ `texlive-core` has broken pdflatex — use `tectonic` instead | `mktexfmt` fails with Perl path errors |
| **No root access** | Download installer from [tug.org/texlive](https://tug.org/texlive/) → install to `~/texlive/` | Manual profile creation, ~10 min |
| **Zero-install** | `tectonic` via conda or single binary | [github.com/tectonic-typesetting/tectonic](https://github.com/tectonic-typesetting/tectonic) |

**After installing, verify with the smoke test (see Environment Gate below).**

### Environment Gate (Phase 0.1 — MANDATORY before Beamer generation)

Between engine selection and content generation, run a **5-line smoke test** to verify the TeX toolchain actually works:

```bash
# Smoke test: minimal metropolis + TikZ
cat > /tmp/_slideaway_beamer_smoke.tex << 'SMOKE'
\documentclass{beamer}
\usetheme{metropolis}
\usepackage{tikz}
\begin{document}
\begin{frame}{Smoke Test}
\begin{tikzpicture}\draw (0,0) -- (1,1);\end{tikzpicture}
\end{frame}
\end{document}
SMOKE

# Clean up temp files on exit
trap 'rm -f /tmp/_slideaway_beamer_smoke.*' EXIT

# Try tectonic first, fall back to pdflatex
if command -v tectonic &>/dev/null; then
  tectonic /tmp/_slideaway_beamer_smoke.tex -o /tmp/ 2>&1
elif command -v pdflatex &>/dev/null; then
  pdflatex -halt-on-error -interaction=nonstopmode -output-directory=/tmp /tmp/_slideaway_beamer_smoke.tex 2>&1
else
  echo 'ERROR: No TeX engine found. Install tectonic or texlive.'
  exit 1
fi

# Check exit code
if [ $? -eq 0 ]; then
  echo 'BEAMER SMOKE TEST: PASS'
else
  echo 'BEAMER SMOKE TEST: FAIL'
  echo 'Beamer engine is not usable. Suggestions:'
  echo '  1. Install tectonic: conda install -c conda-forge tectonic'
  echo '  2. Use Marp as alternative: /slides "topic" --engine marp --format pdf'
  exit 1
fi
```

**If smoke test fails**: the agent MUST suggest Marp (`--engine marp --format pdf`) as zero-dependency alternative and NOT proceed with Beamer generation. Do NOT generate 800 lines of LaTeX that will fail to compile.

### Beamer Gotchas

| Pattern | Why | What Happens Otherwise |
|---------|-----|----------------------|
| `aspectratio=169` | Modern projectors are 16:9 | Black bars on sides |
| `metropolis` theme | Clean, readable, modern | Default beamer looks dated |
| Max 6 bullet points per slide | Audience attention limit | Information overload |
| PDF figures only | Vector graphics scale | Pixelated on projector |
| `\note{}` for speaker notes | Separate content from delivery | Notes mixed with slides |
| `xelatex` for Unicode | Handles non-ASCII | Encoding errors with pdflatex |
| `tectonic` for conda envs | Auto-downloads missing packages | `\tikzscope@linewidth` undefined |

### Beamer Anti-Patterns (HARD FAIL — never generate these)

These patterns cause PGF scope corruption when TikZ diagrams are present in any frame. The generator MUST NOT produce them.

| Anti-Pattern | Why It Breaks | Safe Alternative |
|-------------|--------------|-----------------|
| `\setbeamertemplate{frametitle}{...custom...}` | Corrupts `\tikzscope@linewidth` for TikZ in same frame | `\setbeamercolor{frametitle}{bg=Color, fg=white}` (color only) |
| `\usetheme{default}` + custom templates | Loses PGF-safe template internals from real themes | Always use a named theme: `metropolis`, `Madrid`, `Boadilla` |
| Custom `beamercolorbox` footline | PGF scope leak across frames | `\setbeamertemplate{frame numbering}[fraction]` or theme's built-in footline |
| `\setbeamercolor{background canvas}{bg=...}` | Different PGF scope management than theme default | Let the theme handle background (empty bg) |
| `\setbeamercolor{normal text}{bg=...}` | Same scope issue as background canvas | Only set `fg`, never `bg` on normal text |

**The safe pattern** (verified on tectonic + pdflatex + xelatex):

```latex
% SAFE — use theme + color overrides ONLY
\usetheme{metropolis}
\definecolor{ResearchBlue}{HTML}{2C3E6B}
\definecolor{AccentRed}{HTML}{E74C3C}
\setbeamercolor{frametitle}{bg=ResearchBlue, fg=white}
\setbeamercolor{progress bar}{fg=ResearchBlue}
\setbeamercolor{alerted text}{fg=AccentRed}
% DO NOT override: frametitle template, footline template, background canvas bg
```

**The dangerous pattern** (generates PGF scope corruption with TikZ):

```latex
% DANGEROUS — do NOT generate this
\usetheme{default}  % <-- loses all PGF-safe internals
\setbeamertemplate{frametitle}{%  % <-- corrupts TikZ scope
  \vspace{0.4em}%
  \insertframetitle\par
}  
\setbeamertemplate{footline}{%  % <-- PGF scope leak
  \hbox{\begin{beamercolorbox}[wd=0.7\paperwidth]{footline}...
}  
```

### Compilation Gate (MANDATORY after generation)

> After generating a `.tex` file, ALWAYS compile it before reporting success.
> If compilation fails, fix the preamble (usually by removing custom template overrides) and retry.
> Max 2 fix attempts. If still broken, report the compilation error to the user.
>
> ```bash
> tectonic slides.tex  # preferred
> # fallback: pdflatex -halt-on-error -interaction=nonstopmode slides.tex
> ```
>
> **The `--refine` flag is useless if the file doesn't compile.** Compilation check MUST precede visual QA.

### Useful Environments

```latex
% Highlighted block
\begin{block}{Title}
    Content here.
\end{block}

% Warning block (red)
\begin{alertblock}{Warning}
    Important warning.
\end{alertblock}

% Example block (green)
\begin{exampleblock}{Example}
    Example content.
\end{exampleblock}

% Overlay (reveal on click)
\begin{itemize}
    \item<1-> Always visible
    \item<2-> Appears on click 2
    \item<3-> Appears on click 3
\end{itemize}
```

### Template Location

Module includes a ready-to-use template at:
`modules/slides/templates/beamer/metropolis-template.tex`

---

