# Data Visualization Reference

## Scope

**Covers**: Chart type selection, data simplification for slide contexts, progressive disclosure of complex data, figure preparation workflow, Python/R code for presentation-friendly defaults, color scale selection for charts.

**Does not cover**: Color theory fundamentals or color psychology (see [design-foundations.md](../../../presentation-design-styles/references/design-foundations.md)) · General layout composition · Typography hierarchy · Animation principles.

---

## Chart-Specific Color Scales

Choose scales based on data structure, not aesthetics. Wrong scale choice actively misleads audiences.

### Sequential Scales — Ordered Magnitude

Use when data has a meaningful zero or minimum and increases in one direction.

| Scale | Best For | Avoid When |
|-------|----------|------------|
| **Viridis** | Scientific data, heatmaps, continuous ranges | Categorical comparisons |
| **Blues** | Single-variable intensity, density maps | Diverging data with midpoint |
| **Greens** | Growth metrics, positive-only data | Data with negative values |
| **YlOrRd** | Risk/urgency gradients | Colorblind audiences (red-green issues) |

**Viridis hex stops** (perceptually uniform, colorblind-safe):
```
#440154 → #31688E → #35B779 → #FDE725
(dark purple → blue → green → yellow)
```

**Blues hex stops**:
```
#F7FBFF → #C6DBEF → #6BAED6 → #2171B5 → #084594
```

### Diverging Scales — Midpoint Matters

Use when data has a meaningful center (zero, baseline, average) and deviations in both directions carry meaning.

| Scale | Best For | Midpoint Color |
|-------|----------|----------------|
| **RdBu** | Temperature anomalies, sentiment, change vs. baseline | White `#F7F7F7` |
| **PiYG** | Before/after comparisons, positive/negative deltas | Light gray `#F7F7F7` |
| **BrBG** | Environmental data, soil/water metrics | White `#F5F5F5` |
| **RdYlGn** | Performance vs. target (traffic light) | Yellow `#FFFFBF` |

**RdBu hex stops**:
```
#B2182B → #EF8A62 → #FDDBC7 → #F7F7F7 → #D1E5F0 → #67A9CF → #2166AC
(red → light red → white → light blue → blue)
```

**PiYG hex stops**:
```
#8E0152 → #DE77AE → #F7F7F7 → #A1D76A → #4D9221
(magenta → pink → white → light green → dark green)
```

### Categorical Scales — Distinct Groups

Use for nominal data with no inherent order. Each color must be distinguishable in isolation.

**Okabe-Ito 8-color set** — the gold standard for colorblind-safe categorical palettes:

| Slot | Name | Hex | RGB |
|------|------|-----|-----|
| 1 | Black | `#000000` | 0, 0, 0 |
| 2 | Orange | `#E69F00` | 230, 159, 0 |
| 3 | Sky Blue | `#56B4E9` | 86, 180, 233 |
| 4 | Bluish Green | `#009E73` | 0, 158, 115 |
| 5 | Yellow | `#F0E442` | 240, 228, 66 |
| 6 | Blue | `#0072B2` | 0, 114, 178 |
| 7 | Vermillion | `#D55E00` | 213, 94, 0 |
| 8 | Reddish Purple | `#CC79A7` | 204, 121, 167 |

> **Why Okabe-Ito?** It was designed specifically for deuteranopia and protanopia (the two most common color vision deficiencies). All 8 colors remain distinguishable under all common colorblindness simulations. For the theory behind this choice, see [design-foundations.md](../../../presentation-design-styles/references/design-foundations.md#color-theory).

**Practical rule**: Use slots 2–7 for most categorical work (skip black slot 1 unless you need a "total" or "reference" series). For ≤4 categories, use slots 2, 3, 6, 7 — highest contrast combination.

---

## Chart Type Selection

Match the chart to the question, not the data shape.

| Data Type | Best Chart | Worst Chart | Presentation Optimization |
|-----------|-----------|-------------|--------------------------|
| **Part-to-whole (≤5 parts)** | Donut / Pie | Stacked bar (hard to compare) | Label directly on segments; remove legend |
| **Part-to-whole (>5 parts)** | Treemap / Stacked bar | Pie (too many slices) | Group small categories into "Other" |
| **Comparison across categories** | Horizontal bar | Vertical bar (long labels rotate badly) | Sort by value descending; highlight key bar |
| **Trend over time** | Line chart | Bar chart (implies discrete) | Annotate key events directly on line |
| **Distribution** | Box plot / Violin | Pie (meaningless) | Show individual data points if N < 50 |
| **Correlation** | Scatter plot | Line chart (implies sequence) | Add regression line + R² annotation |
| **Geospatial** | Choropleth map | Bar chart (loses spatial context) | Use diverging scale from neutral midpoint |
| **Flow / Process** | Sankey / Alluvial | Network graph (too complex) | Simplify to top 5 flows; label endpoints |
| **Ranking** | Lollipop / Dot plot | 3D bar (distorts perception) | Highlight top 3 with accent color |
| **Two variables + magnitude** | Bubble chart | 3D scatter (unreadable) | Cap bubble size range; label outliers |
| **Before / After** | Slope chart | Grouped bar (harder to track change) | Annotate delta values at endpoints |
| **Multiple time series** | Small multiples | Overlapping lines (spaghetti) | Highlight one series; gray out others |

### Projection-Specific Constraints

Slides are not papers. Apply these rules before finalizing any chart:

- **Remove gridlines** or reduce to 1pt light gray — projectors wash them out
- **Minimum font size 14pt** for any text in a figure (axis labels, tick marks, annotations)
- **Maximum 6 data series** per chart — beyond that, use small multiples
- **Aspect ratio**: 16:9 slides favor wider charts; avoid tall narrow charts
- **High contrast**: Minimum 3:1 contrast ratio between data elements and background

---

## 7 Visualization Mistakes and Solutions

### Mistake 1: Dual Y-Axes

**Problem**: Two different scales on the same chart implies a relationship that may not exist. Audiences can't compare magnitudes across axes.

**Solution**: Use two separate charts side-by-side, or use a slope chart to show change in both metrics independently.

---

### Mistake 2: 3D Charts

**Problem**: 3D perspective distorts area and length perception. The front bars appear larger than the back bars even when equal.

**Solution**: Always use 2D. If depth is needed, use small multiples or faceting.

---

### Mistake 3: Truncated Y-Axis

**Problem**: Starting the Y-axis above zero exaggerates differences. A 2% change looks like a 50% change.

**Solution**: Start at zero for bar charts (always). For line charts showing trends, truncation is acceptable if clearly labeled — add a break symbol (///) to signal the axis doesn't start at zero.

---

### Mistake 4: Rainbow Color Scales for Sequential Data

**Problem**: Rainbow (jet) scales have no perceptual ordering — the eye treats yellow as "more" than green even when the data says otherwise. They also fail colorblindness tests.

**Solution**: Use Viridis, Blues, or any single-hue sequential scale. These are perceptually uniform — equal data steps produce equal visual steps.

---

### Mistake 5: Too Many Categories

**Problem**: 12 bars in a bar chart, 8 lines in a line chart — audiences can't parse this in a 30-second slide.

**Solution**: Show top 5 (or top N that tell the story). Group the rest as "Other." If all categories matter, use a table instead of a chart.

---

### Mistake 6: Missing Context

**Problem**: A chart showing "revenue grew 40%" is meaningless without a baseline. Grew from what? Compared to what?

**Solution**: Always include: baseline/comparison period, units, data source, and N (sample size for survey data). Add a direct annotation on the chart — don't rely on the audience reading the caption.

---

### Mistake 7: Decorative Elements That Obscure Data

**Problem**: Background images, gradient fills, drop shadows, and clip art compete with the data signal.

**Solution**: Data-ink ratio (Tufte): every pixel should serve the data. Remove chart borders, remove background fills, remove 3D effects, remove decorative icons.

---

## Figure Preparation Workflow

Four stages from raw output to projection-ready figure.

### Stage 1: High-Resolution Export

Export at minimum 150 DPI for screen, 300 DPI if the deck will be printed.

```python
# matplotlib — always export at high resolution
fig.savefig('figure.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')

# For vector output (scales to any size):
fig.savefig('figure.svg', bbox_inches='tight')
fig.savefig('figure.pdf', bbox_inches='tight')
```

### Stage 2: Simplify

Remove everything that doesn't serve the audience's understanding:
- Delete gridlines (or reduce to 1pt, 20% opacity)
- Remove chart borders/spines (top and right spines especially)
- Reduce tick marks to 4–6 per axis
- Replace legend with direct labels where possible
- Round numbers in annotations (1.23M not 1,234,567)

### Stage 3: Optimize for Projection

Projection environments are hostile to fine detail:
- Minimum 14pt font for any text element
- Minimum 2pt line width for data lines
- Increase marker size by 50% vs. print defaults
- Test on a dark background if the venue uses dark rooms
- Use solid fills, not hatching (hatching disappears at distance)

### Stage 4: Add Context

The figure must be self-explanatory without the presenter:
- Headline annotation stating the key finding (not a title like "Revenue by Quarter")
- Source line in 10pt at bottom left
- Direct data labels on key values
- Callout arrow or highlight box on the critical data point

---

## Python: Presentation-Ready Defaults

Apply these `rcParams` at the top of any figure-generating script to get presentation-appropriate defaults without per-figure customization.

```python
import matplotlib.pyplot as plt
import matplotlib as mpl

# Presentation defaults — apply once at script top
mpl.rcParams.update({
    # Figure
    'figure.figsize': (10, 6),          # 16:9 aspect ratio
    'figure.dpi': 150,
    'figure.facecolor': 'white',
    'savefig.bbox': 'tight',
    'savefig.facecolor': 'white',

    # Font sizes — minimum 14pt for projection
    'font.size': 14,
    'axes.titlesize': 18,
    'axes.labelsize': 16,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14,

    # Axes — clean, minimal
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linewidth': 0.8,
    'axes.linewidth': 1.2,

    # Lines and markers — visible at distance
    'lines.linewidth': 2.5,
    'lines.markersize': 8,
    'patch.linewidth': 0,

    # Okabe-Ito categorical palette (slots 2–7)
    'axes.prop_cycle': mpl.cycler(color=[
        '#E69F00',  # Orange
        '#56B4E9',  # Sky Blue
        '#009E73',  # Bluish Green
        '#0072B2',  # Blue
        '#D55E00',  # Vermillion
        '#CC79A7',  # Reddish Purple
    ]),
})
```

### Seaborn Integration

```python
import seaborn as sns

# Presentation theme
sns.set_theme(
    style='ticks',          # Minimal spines
    context='talk',         # Larger fonts than 'paper', smaller than 'poster'
    palette=[               # Okabe-Ito slots 2–7
        '#E69F00', '#56B4E9', '#009E73',
        '#0072B2', '#D55E00', '#CC79A7'
    ],
    font_scale=1.1          # Bump up slightly for projection
)
sns.despine()               # Remove top and right spines
```

### Quick Annotation Pattern

```python
# Annotate the key data point directly on the chart
ax.annotate(
    'Peak: 2.4M units (Q3)',
    xy=(peak_x, peak_y),
    xytext=(peak_x + 0.5, peak_y * 1.08),
    fontsize=13,
    color='#1A1A1A',
    arrowprops=dict(arrowstyle='->', color='#666666', lw=1.5),
)

# Add source line
fig.text(0.01, -0.02, 'Source: Company data, FY2025',
         fontsize=10, color='#888888', ha='left')
```

---

## R: Presentation-Ready Defaults

### ggplot2 Theme

```r
library(ggplot2)
library(scales)

# Okabe-Ito palette
okabe_ito <- c(
  "#E69F00",  # Orange
  "#56B4E9",  # Sky Blue
  "#009E73",  # Bluish Green
  "#0072B2",  # Blue
  "#D55E00",  # Vermillion
  "#CC79A7",  # Reddish Purple
  "#F0E442",  # Yellow
  "#000000"   # Black
)

# Presentation theme — clean, projection-ready
theme_slides <- function(base_size = 16) {
  theme_minimal(base_size = base_size) +
    theme(
      # Remove top and right axes
      axis.line = element_line(color = "#333333", linewidth = 0.8),
      panel.grid.major = element_line(color = "#DDDDDD", linewidth = 0.5),
      panel.grid.minor = element_blank(),

      # Generous text sizes
      plot.title = element_text(size = base_size * 1.3, face = "bold",
                                 margin = margin(b = 12)),
      axis.title = element_text(size = base_size * 1.0),
      axis.text = element_text(size = base_size * 0.9),
      legend.text = element_text(size = base_size * 0.9),

      # Clean background
      plot.background = element_rect(fill = "white", color = NA),
      panel.background = element_rect(fill = "white", color = NA),

      # Legend position
      legend.position = "bottom",
      legend.box.margin = margin(t = 8)
    )
}

# Usage
ggplot(data, aes(x = category, y = value, fill = group)) +
  geom_col() +
  scale_fill_manual(values = okabe_ito) +
  theme_slides() +
  labs(
    title = "Key finding stated as assertion",
    caption = "Source: Dataset name, Year"
  )
```

### Export for Slides

```r
# Export at slide-appropriate dimensions
ggsave(
  filename = "figure.png",
  plot = last_plot(),
  width = 10,        # inches — matches 16:9 at 150 DPI
  height = 6,
  dpi = 150,
  bg = "white"
)

# Vector output (preferred for PPTX embedding)
ggsave(
  filename = "figure.pdf",
  width = 10,
  height = 6
)
```

---

## Cross-References

- **Color theory fundamentals** (why Okabe-Ito works, WCAG contrast ratios, color psychology): [design-foundations.md](../../../presentation-design-styles/references/design-foundations.md)
- **Style presets** with specific chart color overrides: [styles.md](../../../presentation-design-styles/references/styles.md)
- **Anti-patterns** including data visualization anti-patterns in slide context: [anti-patterns.md](../../../presentation-design-styles/references/anti-patterns.md)
- **Engine-specific figure embedding** (PPTX, Beamer, reveal.js): see individual `engine-*.md` reference files
