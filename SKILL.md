---
name: nature-science-figure-skill
description: Create, revise, audit, and package publication-ready scientific data figures for Nature or Science, especially matplotlib-based charts, multi-panel figures, journal-size profiles, data-driven chart selection, colorblind-safe styling, vector/raster export, visual QA, and pre-submission compliance checks. Use when a user asks for Nature/Science compliant research figures, manuscript figures, data plots, multi-panel scientific figures, figure validation, journal artwork checks, or an AI-agent plotting skill/workflow.
---

# Nature/Science Figure Skill

Use this skill to turn research data and a scientific claim into a compliant, readable, and attractive Nature/Science-style figure. The workflow is deliberately stage-gated: do not jump from data to final export.

## Core Workflow

1. **Clarify the target**
   - Require `journal_profile`: `nature_main` or `science_main`.
   - Require figure stage: `draft`, `revision`, or `final_artwork`.
   - Require the claim the figure must support. If the claim is unclear, ask or state a narrow working assumption.

2. **Profile the data before choosing a plot**
   - Inspect variable types, sample sizes, missingness, distribution shape, outliers, grouping structure, and units.
   - Use `scripts/profile_data.py` for CSV/TSV/XLSX when a tabular dataset is available.
   - Read `references/chart-selection.md` when the chart type is not already fixed.
   - Reject misleading defaults such as small-sample mean bars, pie charts, 3D effects, dual y-axes with unrelated units, rainbow/jet colormaps, and category means connected by lines.

3. **Load the journal profile**
   - Read `profiles/nature_main.yaml` or `profiles/science_main.yaml`.
   - For detailed provenance and source notes, read `references/journal-profiles.md`.
   - Use the profile dimensions as final physical size. Do not create arbitrary pixel-size figures and scale later.

4. **Choose panel size and layout**
   - Read `references/panel-layout.md` for multi-panel or reusable small-panel work.
   - Default to `standard` panel preset (`58 mm x 48 mm`) when the panel type is ordinary scatter/line/bar and no stronger reason exists.
   - Upgrade panel size when there is a colorbar, long category labels, many legend entries, or dense annotation.
   - For standalone small figures intended for later PPT assembly, do not add panel labels by default. Add `a/b/c` or `A/B/C` labels only at the final multi-panel assembly stage, unless the user explicitly requests labels on the small figure.

5. **Plot with restrained scientific style**
   - Use Arial/Helvetica-compatible sans-serif fonts.
   - Use colorblind-safe palettes and redundant encoding with marker/line/hatch when categories exceed easy color separation.
   - Read `references/palette-presets.md` before using a non-default palette or an article-inspired palette.
   - Use vector text and lines; keep raster content only for images, microscopy, scans, or heatmap-like pixel data.
   - Read `references/plot-recipes.md` for chart-specific patterns.
   - Prefer `scripts/plot_helpers.py` for common matplotlib bars, trends, scatter, heatmaps, semantic colors, dynamic y-limits, and dedicated legend panels.

6. **Handle statistics honestly**
   - Read `references/stat-annotation.md` whenever the figure includes error bars, confidence intervals, p-values, significance brackets, regression fits, or model comparisons.
   - Never invent p-values, n, replicate structure, or test methods.

7. **Export and audit**
   - Prefer `scripts/figure_skill.py` for style setup, profile loading, export, and basic compliance checks.
   - Default export is PPT-assembly friendly: editable `svg`, transparent high-resolution `png`, and audit note.
   - Use `scripts/visual_qa.py` inside plotting scripts to render a preview and catch clipping/tick/legend layout problems.
   - Auto-fix hard layout problems such as overlapping tick labels or legends covering data before export; do not stop to ask the user for these mechanical repairs.
   - For default PPT assembly output, allow small automatic canvas expansion when crowded labels cannot be repaired within the original panel; for `final_artwork`, preserve journal physical size and report any unresolved hard issue.
   - Report color-accessibility or low-contrast warnings in the audit, but do not automatically recolor unless the user asks or the intended semantic color mapping is clear.
   - Always render a PNG preview before final export.
   - Read `references/validation.md` for the required audit loop.
   - Final deliverables should include editable vector output (`svg` by default; `pdf` only when final artwork or explicitly requested), raster preview, and an audit/provenance note.

## Quick Python Pattern

```python
from pathlib import Path
import matplotlib.pyplot as plt
from scripts.figure_skill import apply_profile_style, size_inches, export_figure
from scripts.plot_helpers import make_trend, semantic_color

profile = apply_profile_style("nature_main", width="double")
fig, axes = plt.subplots(1, 3, figsize=size_inches(profile, width="double", height_mm=55), constrained_layout=True)

make_trend(axes[0], [0, 1, 2], [[1.0, 1.3, 1.5]], ["Key result"], colors=[semantic_color("key")])

# Add panel labels only when this script is producing the final multi-panel figure.
# Omit this for standalone small figures that will be assembled later in PPT.
# from scripts.figure_skill import add_panel_labels
# add_panel_labels(fig, axes, profile)
export_figure(fig, Path("figures/figure1"), profile)
```

## Resource Map

- `profiles/nature_main.yaml` and `profiles/science_main.yaml`: machine-readable journal rules.
- `references/journal-profiles.md`: official-source provenance and profile interpretation.
- `references/chart-selection.md`: data/claim to chart-type decisions and misleading-plot blockers.
- `references/panel-layout.md`: small-panel presets and multi-panel composition rules.
- `references/palette-presets.md`: approved palette presets, article-inspired palettes, sources, and usage boundaries.
- `references/plot-recipes.md`: common scientific chart recipes.
- `references/stat-annotation.md`: error bars, intervals, n, statistical labels, and caption obligations.
- `references/validation.md`: export, visual QA, compliance checks, and provenance report.
- `scripts/figure_skill.py`: lightweight executable helpers for matplotlib style, export, and file checks.
- `scripts/plot_helpers.py`: profile-aware bars, trends, heatmaps, scatter, semantic colors, and layout helper API.
- `scripts/profile_data.py`: tabular data profiling for chart-selection decisions.
- `scripts/visual_qa.py`: matplotlib preview rendering and deterministic layout audit helpers.
- `references/source-links.md`: public official-source links and provenance notes used to build the profiles; this public skill does not redistribute third-party PDF/template files.

## Non-Negotiable Rules

- Do not claim a figure is Nature/Science compliant unless it was generated at final physical size and checked against the selected profile.
- Do not use a single hard-coded template for both journals. Use shared plotting logic with journal-specific profiles.
- Do not flatten, outline, or rasterize text/line art for final vector chart output.
- Do not present visual polish as scientific validity. If the data, uncertainty, or statistical test is underspecified, say so and keep the figure honest.
