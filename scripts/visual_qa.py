#!/usr/bin/env python
"""Matplotlib visual QA helpers for publication figures."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import math
import textwrap


def render_preview(fig, out_png: str | Path, dpi: int = 150) -> Path:
    """Render a preview PNG for visual inspection."""
    out = Path(out_png)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=dpi, bbox_inches="tight", facecolor="white")
    return out


def _visible_texts(fig):
    texts = []
    for ax in fig.axes:
        texts.extend([t for t in ax.texts if t.get_visible() and t.get_text()])
        texts.extend([t for t in ax.get_xticklabels() if t.get_visible() and t.get_text()])
        texts.extend([t for t in ax.get_yticklabels() if t.get_visible() and t.get_text()])
        texts.append(ax.xaxis.label)
        texts.append(ax.yaxis.label)
        if ax.get_title():
            texts.append(ax.title)
        leg = ax.get_legend()
        if leg:
            texts.extend([t for t in leg.get_texts() if t.get_visible() and t.get_text()])
    return [t for t in texts if t.get_visible() and t.get_text()]


def _tick_label_ids(fig) -> set[int]:
    ids: set[int] = set()
    for ax in fig.axes:
        ids.update(id(t) for t in ax.get_xticklabels())
        ids.update(id(t) for t in ax.get_yticklabels())
    return ids


def _bbox_overlap(a, b, tol: float = 1.0) -> bool:
    return not (
        a.x1 <= b.x0 + tol or
        b.x1 <= a.x0 + tol or
        a.y1 <= b.y0 + tol or
        b.y1 <= a.y0 + tol
    )


def _output_bbox(fig, renderer):
    try:
        return fig.get_tightbbox(renderer).transformed(fig.dpi_scale_trans)
    except Exception:
        return fig.bbox


def audit_layout(fig, clip_tol_px: float = 2.0, overlap_tol_px: float = 1.0) -> list[tuple[str, str]]:
    """Return `(severity, message)` layout issues for a matplotlib Figure.

    This deterministic audit catches common mechanical problems. It does not
    replace human/AI visual review of the rendered preview.
    """
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    fig_bbox = _output_bbox(fig, renderer)
    issues: list[tuple[str, str]] = []

    texts = _visible_texts(fig)
    tick_label_ids = _tick_label_ids(fig)
    boxes = []
    for text in texts:
        bbox = text.get_window_extent(renderer=renderer)
        boxes.append((text, bbox))
        if id(text) in tick_label_ids:
            continue
        if (bbox.x0 < fig_bbox.x0 - clip_tol_px or
                bbox.y0 < fig_bbox.y0 - clip_tol_px or
                bbox.x1 > fig_bbox.x1 + clip_tol_px or
                bbox.y1 > fig_bbox.y1 + clip_tol_px):
            label = text.get_text().replace("\n", " ")[:50]
            issues.append(("WARN", f"text may be clipped: {label!r}"))

    for ax in fig.axes:
        xticks = [t for t in ax.get_xticklabels() if t.get_visible() and t.get_text()]
        yticks = [t for t in ax.get_yticklabels() if t.get_visible() and t.get_text()]
        for axis_name, labels in [("x", xticks), ("y", yticks)]:
            tick_boxes = [t.get_window_extent(renderer=renderer) for t in labels]
            for i in range(len(tick_boxes)):
                for j in range(i + 1, len(tick_boxes)):
                    if _bbox_overlap(tick_boxes[i], tick_boxes[j], overlap_tol_px):
                        issues.append(("WARN", f"{axis_name}-tick labels overlap on an axis"))
                        break
                else:
                    continue
                break

        leg = ax.get_legend()
        if leg:
            leg_box = leg.get_window_extent(renderer=renderer)
            data_boxes = []
            for artist in ax.lines + ax.collections + ax.patches:
                try:
                    data_boxes.append(artist.get_window_extent(renderer=renderer))
                except Exception:
                    pass
            if any(_bbox_overlap(leg_box, box, overlap_tol_px) for box in data_boxes):
                issues.append(("WARN", "legend may overlap plotted data"))

    return issues


def _ticklabels_overlap(labels, renderer, tol: float = 1.0) -> bool:
    boxes = [t.get_window_extent(renderer=renderer) for t in labels if t.get_visible() and t.get_text()]
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if _bbox_overlap(boxes[i], boxes[j], tol):
                return True
    return False


def _legend_overlaps_data(ax, renderer, tol: float = 1.0) -> bool:
    leg = ax.get_legend()
    if not leg:
        return False
    leg_box = leg.get_window_extent(renderer=renderer)
    data_boxes = []
    for artist in ax.lines + ax.collections + ax.patches:
        try:
            data_boxes.append(artist.get_window_extent(renderer=renderer))
        except Exception:
            pass
    return any(_bbox_overlap(leg_box, box, tol) for box in data_boxes)


def _text_may_be_clipped(fig, renderer, clip_tol_px: float = 2.0) -> bool:
    fig_bbox = _output_bbox(fig, renderer)
    tick_label_ids = _tick_label_ids(fig)
    for text in _visible_texts(fig):
        if id(text) in tick_label_ids:
            continue
        bbox = text.get_window_extent(renderer=renderer)
        if (bbox.x0 < fig_bbox.x0 - clip_tol_px or
                bbox.y0 < fig_bbox.y0 - clip_tol_px or
                bbox.x1 > fig_bbox.x1 + clip_tol_px or
                bbox.y1 > fig_bbox.y1 + clip_tol_px):
            return True
    return False


def _relax_x_tick_labels(ax, labels) -> str:
    rotations = [abs(float(t.get_rotation() or 0.0)) for t in labels]
    max_rotation = max(rotations) if rotations else 0.0
    if max_rotation < 30:
        for tick in labels:
            tick.set_rotation(30)
            tick.set_ha("right")
        return "rotated overlapping x tick labels"
    if max_rotation < 45:
        for tick in labels:
            tick.set_rotation(45)
            tick.set_ha("right")
        return "increased x tick rotation to 45 degrees"
    if any(len(tick.get_text()) > 12 and "\n" not in tick.get_text() for tick in labels):
        ax.set_xticklabels([
            textwrap.fill(tick.get_text(), width=10, break_long_words=False)
            for tick in labels
        ])
        for tick in ax.get_xticklabels():
            tick.set_rotation(0)
            tick.set_ha("center")
            tick.set_fontsize(max(5.0, float(tick.get_fontsize()) * 0.9))
        return "wrapped crowded x tick labels"
    for tick in labels:
        tick.set_rotation(90)
        tick.set_ha("right")
        tick.set_fontsize(max(5.0, float(tick.get_fontsize()) * 0.9))
    return "rotated crowded x tick labels to 90 degrees"


def _expand_limits_for_clipped_ticks(fig, renderer, clip_tol_px: float = 2.0) -> bool:
    changed = False
    fig_bbox = _output_bbox(fig, renderer)
    for ax in fig.axes:
        y0, y1 = ax.get_ylim()
        if y1 <= y0:
            continue
        span = y1 - y0
        new_y0, new_y1 = y0, y1
        for loc, label in zip(ax.get_yticks(), ax.get_yticklabels()):
            if not (label.get_visible() and label.get_text()):
                continue
            bbox = label.get_window_extent(renderer=renderer)
            if bbox.y1 > fig_bbox.y1 - clip_tol_px and loc >= y1:
                new_y1 = max(new_y1, float(loc) + 0.03 * span)
            if bbox.y0 < fig_bbox.y0 + clip_tol_px and loc <= y0:
                new_y0 = min(new_y0, float(loc) - 0.03 * span)
        if new_y0 != y0 or new_y1 != y1:
            ax.set_ylim(new_y0, new_y1)
            changed = True
    return changed


def auto_fix_hard_layout(fig, max_passes: int = 5,
                         allow_canvas_resize: bool = True) -> list[str]:
    """Try to fix deterministic hard layout problems without user intervention.

    Fixes are intentionally conservative: rotate crowded x ticks, move legends
    outside the data area, and rerun layout. Color/accessibility warnings are
    not changed here because they can alter semantic intent.
    """
    actions: list[str] = []

    def add_action(message: str) -> None:
        if message not in actions:
            actions.append(message)

    resize_count = 0
    for _ in range(max_passes):
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        changed = False
        for ax in fig.axes:
            xticks = [t for t in ax.get_xticklabels() if t.get_visible() and t.get_text()]
            if _ticklabels_overlap(xticks, renderer):
                wrapped = any("\n" in tick.get_text() for tick in xticks)
                if wrapped and allow_canvas_resize and resize_count < 2:
                    w, h = fig.get_size_inches()
                    fig.set_size_inches(w * 1.18, h * 1.05, forward=True)
                    resize_count += 1
                    add_action("expanded canvas for crowded x tick labels")
                else:
                    add_action(_relax_x_tick_labels(ax, xticks))
                changed = True

            if _legend_overlaps_data(ax, renderer):
                leg = ax.get_legend()
                if leg:
                    handles, labels = ax.get_legend_handles_labels()
                    leg.remove()
                    ax.legend(handles, labels, loc="upper left", bbox_to_anchor=(1.02, 1.0),
                              borderaxespad=0.0, frameon=False)
                    add_action("moved legend outside data area")
                    changed = True

        try:
            fig.tight_layout(pad=0.4)
            add_action("reran tight_layout")
        except Exception:
            pass
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        if _text_may_be_clipped(fig, renderer):
            if _expand_limits_for_clipped_ticks(fig, renderer):
                add_action("expanded axis limits for clipped tick labels")
                changed = True
            try:
                fig.subplots_adjust(left=0.18, bottom=0.20, top=0.90)
                fig.tight_layout(pad=0.8)
                add_action("increased layout padding for clipped text")
                changed = True
            except Exception:
                pass
        if not changed:
            break
    return actions


def _to_rgb_tuple(color) -> tuple[float, float, float] | None:
    try:
        from matplotlib.colors import to_rgb
        return tuple(float(x) for x in to_rgb(color))
    except Exception:
        return None


def _relative_luminance(rgb: tuple[float, float, float]) -> float:
    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contrast_ratio(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    la = _relative_luminance(a)
    lb = _relative_luminance(b)
    light, dark = max(la, lb), min(la, lb)
    return (light + 0.05) / (dark + 0.05)


def _clip_rgb(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    return tuple(max(0.0, min(1.0, float(x))) for x in rgb)


def _simulate_cvd(rgb: tuple[float, float, float], mode: str) -> tuple[float, float, float]:
    """Approximate full-severity color-vision-deficiency simulation.

    This is a heuristic screening check, not a perceptual guarantee.
    """
    matrices = {
        "protanopia": (
            (0.152286, 1.052583, -0.204868),
            (0.114503, 0.786281, 0.099216),
            (-0.003882, -0.048116, 1.051998),
        ),
        "deuteranopia": (
            (0.367322, 0.860646, -0.227968),
            (0.280085, 0.672501, 0.047413),
            (-0.011820, 0.042940, 0.968881),
        ),
        "tritanopia": (
            (1.255528, -0.076749, -0.178779),
            (-0.078411, 0.930809, 0.147602),
            (0.004733, 0.691367, 0.303900),
        ),
    }
    matrix = matrices[mode]
    r, g, b = rgb
    return _clip_rgb(tuple(row[0] * r + row[1] * g + row[2] * b for row in matrix))


def _rgb_distance(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return math.dist(a, b)


def _grayscale(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    y = _relative_luminance(rgb)
    return (y, y, y)


def audit_color_accessibility(fig, min_contrast: float = 1.6,
                              min_simulated_distance: float = 0.12) -> list[tuple[str, str]]:
    """Report likely color-accessibility issues without changing the figure."""
    colors: list[tuple[float, float, float]] = []
    for ax in fig.axes:
        for line in ax.lines:
            rgb = _to_rgb_tuple(line.get_color())
            if rgb is not None:
                colors.append(rgb)
        for collection in ax.collections:
            try:
                facecolors = collection.get_facecolors()
                for rgba in facecolors[:8]:
                    colors.append(tuple(float(x) for x in rgba[:3]))
            except Exception:
                pass
        for patch in ax.patches:
            rgb = _to_rgb_tuple(patch.get_facecolor())
            if rgb is not None:
                colors.append(rgb)

    unique: list[tuple[float, float, float]] = []
    for color in colors:
        if not any(math.dist(color, existing) < 0.03 for existing in unique):
            unique.append(color)

    issues: list[tuple[str, str]] = []
    for i in range(len(unique)):
        for j in range(i + 1, len(unique)):
            if _contrast_ratio(unique[i], unique[j]) < min_contrast:
                issues.append(("WARN", "two plotted colors may be hard to distinguish in grayscale/low contrast"))
                return issues
            if _rgb_distance(_grayscale(unique[i]), _grayscale(unique[j])) < min_simulated_distance:
                issues.append(("WARN", "two plotted colors may be hard to distinguish in grayscale preview"))
                return issues
            for mode in ("protanopia", "deuteranopia", "tritanopia"):
                a = _simulate_cvd(unique[i], mode)
                b = _simulate_cvd(unique[j], mode)
                if _rgb_distance(a, b) < min_simulated_distance:
                    issues.append(("WARN", f"two plotted colors may be hard to distinguish under {mode} simulation"))
                    return issues
    return issues


def qa_figure(fig, auto_fix: bool = True, include_color: bool = True,
              allow_canvas_resize: bool = True) -> tuple[list[tuple[str, str]], list[str]]:
    """Run layout QA, optionally auto-fix hard layout issues, and report color warnings."""
    actions: list[str] = []
    if auto_fix:
        actions = auto_fix_hard_layout(fig, allow_canvas_resize=allow_canvas_resize)
    issues = audit_layout(fig)
    if include_color:
        issues.extend(audit_color_accessibility(fig))
    return issues, actions


def print_report(issues: Sequence[tuple[str, str]]) -> str:
    if not issues:
        verdict = "PASS"
        print(verdict)
        return verdict
    verdict = "FAIL" if any(level == "FAIL" for level, _ in issues) else "WARN"
    print(verdict)
    for level, message in issues:
        print(f"- {level}: {message}")
    return verdict
