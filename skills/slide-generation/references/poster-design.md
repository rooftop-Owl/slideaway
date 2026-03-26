## Section I — Poster Design (LaTeX tikzposter)

For academic conference posters. tikzposter provides a column-based layout with professional typography.

### Basic Template

```latex
\documentclass[a0paper,portrait,fontscale=0.35]{tikzposter}

\title{Climate Risk Assessment for the Philippines}
\author{Author Name \and Co-Author}
\institute{ETH Zürich · Institute for Atmospheric and Climate Science}
\date{EGU 2026}

\usetheme{Default}
\usecolorstyle{Default}

\begin{document}
\maketitle

\begin{columns}

\column{0.33}

\block{Introduction}{
    Climate-related losses are increasing globally.
    We assess tropical cyclone risk for the Philippines
    using CLIMADA v4 and IBTrACS data.
}

\block{Methods}{
    \begin{itemize}
        \item Hazard: IBTrACS 1980–2023 (Holland model)
        \item Exposure: LitPop v2 GDP proxy
        \item Vulnerability: Emanuel (2011) wind function
    \end{itemize}
    \includegraphics[width=\linewidth]{plots/workflow.pdf}
}

\column{0.34}

\block{Results}{
    \includegraphics[width=\linewidth]{plots/impact_map.pdf}
    Annual expected impact: USD 2.3B (2020 values)
}

\block{Return Periods}{
    \includegraphics[width=\linewidth]{plots/exceedance_curve.pdf}
}

\column{0.33}

\block{Scenario Analysis}{
    \begin{tabular}{lrr}
        \toprule
        Scenario & 2050 AAI & Change \\
        \midrule
        SSP1-2.6 & 2.5B & +9\% \\
        SSP2-4.5 & 2.9B & +26\% \\
        SSP5-8.5 & 3.8B & +65\% \\
        \bottomrule
    \end{tabular}
}

\block{Conclusions}{
    \begin{itemize}
        \item AAI increases 9–65\% by 2050 depending on scenario
        \item Coastal provinces face highest relative increase
        \item Adaptation investment yields positive ROI under all scenarios
    \end{itemize}
}

\block{References}{
    \small
    Aznar-Siguan \& Bresch (2019). \textit{Geosci. Model Dev.}\\
    Emanuel (2011). \textit{Bull. Am. Meteorol. Soc.}\\
    Eberenz et al. (2020). \textit{Nat. Hazards Earth Syst. Sci.}
}

\end{columns}
\end{document}
```

### Compilation

```bash
pdflatex poster.tex
# or for Unicode content:
xelatex poster.tex
```

### Layout Options

| Option | Effect |
|--------|--------|
| `a0paper,portrait` | A0 portrait (standard conference) |
| `a0paper,landscape` | A0 landscape |
| `a1paper,portrait` | A1 portrait (smaller venue) |
| `fontscale=0.35` | Scale all fonts (adjust for content density) |

### Themes

```latex
\usetheme{Default}       % Clean white
\usetheme{Rays}          % Gradient background
\usetheme{Basic}         % Minimal
\usetheme{Envelope}      % Bordered
\usetheme{Wave}          % Wave decoration
```

---

