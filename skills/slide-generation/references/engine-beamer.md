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

### Compilation

```bash
# Standard (two passes for references)
pdflatex slides.tex && pdflatex slides.tex

# Unicode support (recommended for international content)
xelatex slides.tex

# With bibliography
pdflatex slides.tex && bibtex slides && pdflatex slides.tex && pdflatex slides.tex
```

### Beamer Gotchas

| Pattern | Why | What Happens Otherwise |
|---------|-----|----------------------|
| `aspectratio=169` | Modern projectors are 16:9 | Black bars on sides |
| `metropolis` theme | Clean, readable, modern | Default beamer looks dated |
| Max 6 bullet points per slide | Audience attention limit | Information overload |
| PDF figures only | Vector graphics scale | Pixelated on projector |
| `\note{}` for speaker notes | Separate content from delivery | Notes mixed with slides |
| `xelatex` for Unicode | Handles non-ASCII | Encoding errors with pdflatex |

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

