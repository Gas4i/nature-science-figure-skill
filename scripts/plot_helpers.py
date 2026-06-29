#!/usr/bin/env python
"""Reusable matplotlib plot helpers for Nature/Science figures.

These helpers adapt the useful API style of the local scientific-figure-making
skill while keeping sizes, fonts, and line widths governed by journal profiles.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np

from figure_skill import (
    ARTICLE_INSPIRED_PALETTES,
    DEFAULT_COLORS,
    NATMED_SENESCENCE_2026,
    NATCOMM_SSP_2025,
    NATURE654_GRAY_BLUE_RED_2026,
    NATURE637_RED_BLUE_2025,
    NATURE_ENERGY_RED_BLUE_2026,
    NATURE_FOOD_NATURAL_2026,
    PALETTE,
    PALETTE_PRESETS,
    PAUL_TOL_BRIGHT,
    SCIENTIFIC_FIGURE_HOUSE,
    SEMANTIC_COLORS,
    TOL_HYBRID,
    apply_profile_style,
    export_figure,
    get_palette,
    load_profile,
    size_inches,
)


@dataclass(frozen=True)
class FigureStyle:
    """Profile-aware plotting style.

    Defaults are final-size manuscript values, not slide-sized values. Use
    `large=True` in `style_from_profile` only for a full-width comparison panel
    where larger type is still within the journal profile.
    """

    font_size: float = 7
    tick_size: float = 6
    axes_linewidth: float = 0.75
    tick_width: float = 0.60
    tick_length: float = 2.50
    line_width: float = 1.10
    error_bar_width: float = 0.85
    grid_linewidth: float = 0.30
    grid_alpha: float = 0.28
    grid_color: str = "#E5E5E5"
    marker_size: float = 18
    font_family: tuple[str, ...] = ("Arial", "Helvetica", "DejaVu Sans", "sans-serif")


def style_from_profile(profile: Mapping | str, large: bool = False) -> FigureStyle:
    prof = load_profile(profile)
    font = prof.get("font", {})
    line = prof.get("line", {})
    axis = prof.get("axis", {})
    tick_style = prof.get("tick", {})
    grid = prof.get("grid", {})
    base = float(font.get("label_target_pt", 7))
    tick = float(font.get("tick_target_pt", max(base - 1, 5)))
    if large:
        base = min(base + 1.5, float(font.get("label_max_pt", base + 1.5)))
        tick = min(tick + 1, base)
    return FigureStyle(
        font_size=base,
        tick_size=tick,
        axes_linewidth=max(float(axis.get("spine_width_pt", line.get("target_pt", 0.75))), float(line.get("min_pt", 0.28))),
        tick_width=float(tick_style.get("major_width_pt", 0.60)),
        tick_length=float(tick_style.get("major_length_pt", 2.50)),
        line_width=max(float(line.get("data_target_pt", 1.10)), float(line.get("min_pt", 0.28))),
        error_bar_width=max(float(line.get("error_bar_target_pt", 0.85)), float(line.get("min_pt", 0.28))),
        grid_linewidth=float(grid.get("linewidth_pt", 0.30)),
        grid_alpha=float(grid.get("alpha", 0.28)),
        grid_color=str(grid.get("color", "#E5E5E5")),
        marker_size=18 if not large else 24,
        font_family=tuple(font.get("family", ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"])),
    )


def apply_publication_style(profile: Mapping | str = "nature_main", width: str = "single",
                            large: bool = False) -> tuple[dict, FigureStyle]:
    """Apply profile rcParams and return `(profile, FigureStyle)`."""
    prof = apply_profile_style(profile if isinstance(profile, str) else profile.get("profile", "nature_main"), width=width)
    return prof, style_from_profile(prof, large=large)


def create_subplots(profile: Mapping | str = "nature_main", width: str = "single",
                    height_mm: float | None = None, nrows: int = 1, ncols: int = 1,
                    **kwargs):
    """Create profile-sized subplots and return `(fig, axes_flat)`."""
    import matplotlib.pyplot as plt

    prof = load_profile(profile)
    figsize = kwargs.pop("figsize", size_inches(prof, width=width, height_mm=height_mm))
    kwargs.setdefault("constrained_layout", True)
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, **kwargs)
    return fig, np.asarray(axes).reshape(-1)


def semantic_color(role: str, fallback_index: int = 0) -> str:
    """Return a semantic color, falling back to the safe qualitative cycle."""
    return SEMANTIC_COLORS.get(role, DEFAULT_COLORS[fallback_index % len(DEFAULT_COLORS)])


def recommend_palette(
    chart_type: str = "categorical",
    category_count: int | None = None,
    semantic_roles: Sequence[str] | None = None,
    quiet: bool = False,
) -> tuple[str, str]:
    """Recommend a skill palette preset and a short audit-ready reason."""
    chart = chart_type.lower().replace("-", "_").replace(" ", "_")
    roles = {role.lower().replace("-", "_").replace(" ", "_") for role in (semantic_roles or [])}
    n = category_count or 0

    if "ssp" in roles:
        return "natcomm_ssp_2025", "SSP scenario labels match the dedicated skill preset."
    if {"biomedical", "senescence"} & roles or ("biomedical" in chart and 4 <= n <= 5):
        return "natmed_senescence_2026", "Muted five-color biomedical conditions match the Nat Med senescence preset."
    if {"control", "treatment"}.issubset(roles) and n == 3:
        return "nature654_gray_blue_red_2026", "Three control/treatment-style groups match the gray-blue-red preset."
    if {"positive", "negative"} & roles or "diverging" in chart or "difference" in chart:
        return "nature637_red_blue_2025", "Signed or diverging values match the red-blue gradient preset."
    if {"key", "improvement", "baseline"} & roles or "house_style" in roles:
        return "scientific_figure_house", "Semantic blue-green-red-neutral roles match the scientific figure house palette."
    if n == 2 and ("comparison" in chart or "contrast" in chart):
        return "nature_energy_red_blue_2026", "Two-group high-contrast comparison fits the red-blue preset."
    if quiet or n > 6:
        return "scientific_figure_house", "A semantic house palette is preferable after removing the muted preset."
    if any(token in chart for token in ("line_scatter_overlay", "line", "scatter", "trend")) and 2 <= n <= 5:
        return "tol_hybrid", "Tol hybrid keeps Tol bright contrast while softening red for overlaid curves and points."
    if 3 <= n <= 8:
        return "paul_tol_bright", "Unordered categorical groups use the remaining high-contrast colorblind-aware preset."
    return "paul_tol_bright", "Default high-contrast colorblind-aware preset; document any custom alternative if this does not fit."


def _as_1d(values, name: str) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1:
        raise ValueError(f"{name} must be 1D, got shape {arr.shape}")
    return arr


def _colors(colors, count: int) -> list[str]:
    if colors is None:
        return [DEFAULT_COLORS[i % len(DEFAULT_COLORS)] for i in range(count)]
    return list(colors)


def clean_axes(ax, grid: bool = False, style: FigureStyle | None = None):
    """Apply low-clutter analytic-axis defaults."""
    style = style or FigureStyle()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(style.axes_linewidth)
    ax.spines["bottom"].set_linewidth(style.axes_linewidth)
    ax.tick_params(axis="both", which="major", direction="out", length=style.tick_length, width=style.tick_width)
    ax.tick_params(axis="both", which="minor", bottom=False, left=False)
    if grid:
        ax.grid(True, which="major", axis="y", color=style.grid_color, linewidth=style.grid_linewidth, alpha=style.grid_alpha)
        ax.grid(False, which="minor")
    else:
        ax.grid(False)
    return ax


def frame_axes(ax, style: FigureStyle | None = None):
    """Use a light full frame for heatmaps/images where the plot boundary is semantic."""
    style = style or FigureStyle()
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(style.axes_linewidth)
    ax.tick_params(axis="both", which="major", direction="out", length=style.tick_length, width=style.tick_width)
    ax.tick_params(axis="both", which="minor", bottom=False, left=False)
    ax.grid(False)
    return ax


def make_grouped_bar(ax, categories: Sequence[str], series: Sequence[Sequence[float]],
                     labels: Sequence[str], ylabel: str = "Value",
                     colors: Sequence[str] | None = None, annotate: bool = False,
                     errors: Sequence[Sequence[float]] | None = None,
                     hatches: Sequence[str] | None = None, style: FigureStyle | None = None):
    """Render a grouped bar chart with print-safe edges and optional hatches."""
    style = style or FigureStyle()
    data = np.asarray(series, dtype=float)
    if data.ndim != 2:
        raise ValueError("series must be 2D: one row per group, one column per category")
    if data.shape[1] != len(categories):
        raise ValueError("len(categories) must equal number of values per series")
    if data.shape[0] != len(labels):
        raise ValueError("len(labels) must equal number of series")

    x = np.arange(len(categories))
    width = min(0.8 / max(data.shape[0], 1), 0.28)
    colors = _colors(colors, data.shape[0])
    hatches = list(hatches or [None] * data.shape[0])
    err = np.asarray(errors, dtype=float) if errors is not None else None

    containers = []
    for i, row in enumerate(data):
        offset = (i - (data.shape[0] - 1) / 2) * width
        yerr = err[i] if err is not None else None
        bars = ax.bar(
            x + offset, row, width,
            label=labels[i],
            color=colors[i],
            edgecolor="black",
            linewidth=max(style.axes_linewidth, 0.5),
            hatch=hatches[i],
            yerr=yerr,
            capsize=2 if yerr is not None else 0,
            error_kw={"elinewidth": style.error_bar_width, "capthick": style.error_bar_width},
        )
        containers.append(bars)
        if annotate:
            annotate_bars(ax, bars, fontsize=max(style.tick_size, 5))
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel(ylabel)
    clean_axes(ax, style=style)
    return containers


def annotate_bars(ax, bars, fmt: str = "{:.2g}", fontsize: float = 6, padding: float = 2):
    """Add compact values above bars."""
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            fmt.format(height),
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, padding),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=fontsize,
        )


def make_trend(ax, x, y_series: Sequence[Sequence[float]], labels: Sequence[str],
               colors: Sequence[str] | None = None, ylabel: str | None = None,
               xlabel: str | None = None, bands: Sequence[Sequence[float]] | None = None,
               style: FigureStyle | None = None):
    """Plot 2-4 trend lines with optional symmetric uncertainty bands."""
    style = style or FigureStyle()
    x_arr = _as_1d(x, "x")
    colors = _colors(colors, len(y_series))
    band_arr = [None] * len(y_series) if bands is None else [np.asarray(b, dtype=float) for b in bands]
    for i, y in enumerate(y_series):
        y_arr = _as_1d(y, f"y_series[{i}]")
        if len(y_arr) != len(x_arr):
            raise ValueError("each y series must have same length as x")
        ax.plot(x_arr, y_arr, label=labels[i], color=colors[i], linewidth=style.line_width, marker="o", markersize=3)
        if band_arr[i] is not None:
            band = _as_1d(band_arr[i], f"bands[{i}]")
            if len(band) != len(x_arr):
                raise ValueError("each band must have same length as x")
            ax.fill_between(x_arr, y_arr - band, y_arr + band, color=colors[i], alpha=0.18, linewidth=0)
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    clean_axes(ax, style=style)
    return ax


def make_heatmap(ax, matrix, x_labels: Sequence[str] | None = None,
                 y_labels: Sequence[str] | None = None, cmap: str = "viridis",
                 cbar_label: str | None = None, annotate: bool = False,
                 fmt: str = "{:.2g}", style: FigureStyle | None = None):
    """Render a matrix heatmap with a labeled colorbar."""
    style = style or FigureStyle()
    arr = np.asarray(matrix, dtype=float)
    if arr.ndim != 2:
        raise ValueError("matrix must be 2D")
    if cmap in {"jet", "rainbow"}:
        raise ValueError("Use perceptually safer colormaps, not jet/rainbow")
    im = ax.imshow(arr, aspect="auto", cmap=cmap)
    if x_labels is not None:
        if len(x_labels) != arr.shape[1]:
            raise ValueError("x_labels length must match matrix columns")
        ax.set_xticks(np.arange(arr.shape[1]))
        ax.set_xticklabels(x_labels, rotation=45, ha="right")
    if y_labels is not None:
        if len(y_labels) != arr.shape[0]:
            raise ValueError("y_labels length must match matrix rows")
        ax.set_yticks(np.arange(arr.shape[0]))
        ax.set_yticklabels(y_labels)
    if annotate and arr.size <= 100:
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                ax.text(j, i, fmt.format(arr[i, j]), ha="center", va="center", fontsize=5)
    cbar = ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    if cbar_label:
        cbar.set_label(cbar_label)
    frame_axes(ax, style=style)
    return im


def make_scatter(ax, x, y, label: str | None = None, color: str | None = None,
                 size: float | None = None, alpha: float = 0.75,
                 style: FigureStyle | None = None):
    """Plot a single scatter series."""
    style = style or FigureStyle()
    x_arr = _as_1d(x, "x")
    y_arr = _as_1d(y, "y")
    if len(x_arr) != len(y_arr):
        raise ValueError("x and y must have the same length")
    pts = ax.scatter(
        x_arr, y_arr,
        s=size or style.marker_size,
        alpha=alpha,
        color=color or DEFAULT_COLORS[0],
        label=label,
        edgecolors="none",
    )
    clean_axes(ax, style=style)
    return pts


def dynamic_ylim(ax, values, pad_fraction: float = 0.08, include_zero: bool = False):
    """Set a readable y-limit around data without hiding values."""
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return ax
    lo, hi = float(arr.min()), float(arr.max())
    if include_zero:
        lo = min(lo, 0.0)
        hi = max(hi, 0.0)
    span = hi - lo
    pad = (span if span > 0 else max(abs(hi), 1.0)) * pad_fraction
    ax.set_ylim(lo - pad, hi + pad)
    return ax


def add_dedicated_legend(legend_ax, source_axes, ncol: int = 1, **kwargs):
    """Place a shared legend in a dedicated axis."""
    handles = []
    labels = []
    axes = np.asarray(source_axes).reshape(-1)
    for ax in axes:
        h, l = ax.get_legend_handles_labels()
        for handle, label in zip(h, l):
            if label and label not in labels:
                handles.append(handle)
                labels.append(label)
    legend_ax.set_axis_off()
    return legend_ax.legend(handles, labels, frameon=False, ncol=ncol, **kwargs)


__all__ = [
    "DEFAULT_COLORS",
    "ARTICLE_INSPIRED_PALETTES",
    "NATMED_SENESCENCE_2026",
    "NATCOMM_SSP_2025",
    "NATURE654_GRAY_BLUE_RED_2026",
    "NATURE637_RED_BLUE_2025",
    "NATURE_ENERGY_RED_BLUE_2026",
    "NATURE_FOOD_NATURAL_2026",
    "PALETTE",
    "PALETTE_PRESETS",
    "PAUL_TOL_BRIGHT",
    "SCIENTIFIC_FIGURE_HOUSE",
    "SEMANTIC_COLORS",
    "TOL_HYBRID",
    "get_palette",
    "recommend_palette",
    "FigureStyle",
    "style_from_profile",
    "apply_publication_style",
    "create_subplots",
    "semantic_color",
    "clean_axes",
    "make_grouped_bar",
    "annotate_bars",
    "make_trend",
    "make_heatmap",
    "make_scatter",
    "dynamic_ylim",
    "add_dedicated_legend",
    "export_figure",
]
