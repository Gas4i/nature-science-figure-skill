#!/usr/bin/env python
"""Helpers for Nature/Science publication figure workflows.

This module is intentionally small. It gives agents stable contracts for
profile loading, matplotlib style setup, export, and basic file audits while
leaving domain-specific plotting code to the task.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Iterable, Mapping, Sequence


SKILL_DIR = Path(__file__).resolve().parents[1]
PROFILES_DIR = SKILL_DIR / "profiles"


EMBEDDED_PROFILES: dict[str, dict] = {
    "nature_main": {
        "journal": "Nature",
        "profile": "nature_main",
        "source_date": "2026-06-25",
        "widths": {
            "single": {"mm": 89, "inch": 3.5039},
            "double": {"mm": 183, "inch": 7.2047},
        },
        "font": {
            "family": ["Helvetica", "Arial", "DejaVu Sans", "sans-serif"],
            "label_target_pt": 7,
            "label_min_pt": 5,
            "tick_target_pt": 6,
        },
        "panel_label": {"case": "lowercase", "weight": "bold", "target_pt": 8},
        "line": {"min_pt": 0.28, "target_pt": 0.75, "data_target_pt": 1.10, "error_bar_target_pt": 0.85},
        "axis": {"default_spines": "open", "spine_width_pt": 0.75},
        "tick": {"direction": "out", "major_width_pt": 0.60, "major_length_pt": 2.50, "minor_visible": False},
        "grid": {"default": False, "major_only": True, "color": "#E5E5E5", "linewidth_pt": 0.30, "alpha": 0.28},
        "raster": {"min_dpi": 300},
        "export": {"preview_dpi": 200, "final_raster_dpi": 300},
    },
    "science_main": {
        "journal": "Science",
        "profile": "science_main",
        "source_date": "2026-06-25",
        "widths": {
            "single": {"mm": 90, "inch": 3.6},
            "double": {"mm": 183, "inch": 7.25},
        },
        "font": {
            "family": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "label_min_pt": 6,
            "label_max_pt": 9,
            "label_target_pt": 7,
            "tick_target_pt": 6,
        },
        "panel_label": {"case": "uppercase", "weight": "bold", "target_pt": 10},
        "line": {"min_pt": 0.28, "target_pt": 0.75, "data_target_pt": 1.10, "error_bar_target_pt": 0.85},
        "axis": {"default_spines": "open", "spine_width_pt": 0.75},
        "tick": {"direction": "out", "major_width_pt": 0.60, "major_length_pt": 2.50, "minor_visible": False},
        "grid": {"default": False, "major_only": True, "color": "#E5E5E5", "linewidth_pt": 0.30, "alpha": 0.28},
        "raster": {"photographic_dpi_range": [300, 500], "embedded_min_ppi": 300},
        "export": {"preview_dpi": 200, "final_raster_dpi": 300},
    },
}


OKABE_ITO = [
    "#E69F00",
    "#56B4E9",
    "#009E73",
    "#F0E442",
    "#0072B2",
    "#D55E00",
    "#CC79A7",
    "#000000",
]


PAUL_TOL_BRIGHT = [
    "#4477AA",
    "#EE6677",
    "#228833",
    "#CCBB44",
    "#66CCEE",
    "#AA3377",
    "#BBBBBB",
]


PAUL_TOL_MUTED = [
    "#332288",
    "#88CCEE",
    "#44AA99",
    "#117733",
    "#999933",
    "#DDCC77",
    "#CC6677",
    "#882255",
    "#AA4499",
    "#DDDDDD",
]


NATURE_ENERGY_RED_BLUE_2026 = {
    "primary_red": "#FA3C3C",
    "primary_blue": "#33B2FF",
}


NATURE654_GRAY_BLUE_RED_2026 = {
    "control_gray": "#C2C4C3",
    "treatment_blue": "#184B88",
    "treatment_red": "#E96465",
}


NATURE_FOOD_NATURAL_2026 = {
    "profile_1": "#C3B99E",
    "profile_2": "#527995",
    "profile_3": "#B76366",
}


NATCOMM_SSP_2025 = {
    "ssp126": "#D4A96B",
    "ssp245": "#BCAFAA",
    "ssp370": "#AC0000",
    "ssp585": "#2D332F",
}


NATURE637_RED_BLUE_2025 = {
    "red_gradient": [
        "#F8EAE1",
        "#FBE3D6",
        "#FAD4BF",
        "#F5AC8B",
        "#C6403D",
        "#A81428",
        "#780522",
    ],
    "blue_gradient": [
        "#EDF2F6",
        "#C1DDE9",
        "#84BDDA",
        "#74B0D2",
        "#3685BB",
        "#256CAE",
        "#134B87",
    ],
}


ARTICLE_INSPIRED_PALETTES = {
    "nature_energy_red_blue_2026": NATURE_ENERGY_RED_BLUE_2026,
    "nature654_gray_blue_red_2026": NATURE654_GRAY_BLUE_RED_2026,
    "nature_food_natural_2026": NATURE_FOOD_NATURAL_2026,
    "natcomm_ssp_2025": NATCOMM_SSP_2025,
    "nature637_red_blue_2025": NATURE637_RED_BLUE_2025,
}


PALETTE_PRESETS = {
    "okabe_ito": OKABE_ITO,
    "wong": OKABE_ITO,
    "paul_tol_bright": PAUL_TOL_BRIGHT,
    "paul_tol_muted": PAUL_TOL_MUTED,
    "nature_energy_red_blue_2026": NATURE_ENERGY_RED_BLUE_2026,
    "paper_palette_01": NATURE_ENERGY_RED_BLUE_2026,
    "nature654_gray_blue_red_2026": NATURE654_GRAY_BLUE_RED_2026,
    "paper_palette_02": NATURE654_GRAY_BLUE_RED_2026,
    "nature_food_natural_2026": NATURE_FOOD_NATURAL_2026,
    "paper_palette_03": NATURE_FOOD_NATURAL_2026,
    "natcomm_ssp_2025": NATCOMM_SSP_2025,
    "natcomm_heat_adaptation_2025": NATCOMM_SSP_2025,
    "nature637_red_blue_2025": NATURE637_RED_BLUE_2025,
    "nature637_stripes_2025": NATURE637_RED_BLUE_2025,
}


PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE",
    "green_2": "#AADCA9",
    "green_3": "#8BCF8B",
    "red_1": "#F6CFCB",
    "red_2": "#E9A6A1",
    "red_strong": "#B64342",
    "neutral": "#CFCECE",
    "neutral_dark": "#4D4D4D",
    "highlight": "#FFD700",
    "teal": "#42949E",
    "violet": "#9A4D8E",
}


SEMANTIC_COLORS = {
    "key": PALETTE["blue_main"],
    "primary": PALETTE["blue_main"],
    "secondary": PALETTE["blue_secondary"],
    "improvement": PALETTE["green_3"],
    "positive": PALETTE["green_3"],
    "baseline": PALETTE["neutral"],
    "reference": PALETTE["neutral_dark"],
    "comparator": PALETTE["red_strong"],
    "contrast": PALETTE["red_strong"],
    "highlight": PALETTE["highlight"],
}


DEFAULT_COLORS = OKABE_ITO


def get_palette(name: str = "okabe_ito", as_dict: bool = False):
    """Return a named palette preset.

    List palettes are for categorical cycles. Dict palettes are article-inspired
    semantic palettes; set `as_dict=True` to preserve their role names.
    """
    key = name.lower().replace("-", "_")
    if key not in PALETTE_PRESETS:
        known = ", ".join(sorted(PALETTE_PRESETS))
        raise ValueError(f"Unknown palette {name!r}. Known: {known}")
    palette = PALETTE_PRESETS[key]
    if isinstance(palette, dict):
        if as_dict:
            return dict(palette)
        values = []
        for value in palette.values():
            if isinstance(value, list):
                values.extend(value)
            else:
                values.append(value)
        return values
    return list(palette)


def _load_yaml(path: Path) -> dict | None:
    try:
        import yaml  # type: ignore
    except Exception:
        return None
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Profile is not a mapping: {path}")
    return data


def load_profile(profile_name: str | Mapping) -> dict:
    """Load a journal profile by name or return a copy of an existing mapping."""
    if isinstance(profile_name, Mapping):
        return dict(profile_name)
    path = PROFILES_DIR / f"{profile_name}.yaml"
    if path.exists():
        data = _load_yaml(path)
        if data is not None:
            return data
    if profile_name in EMBEDDED_PROFILES:
        return json.loads(json.dumps(EMBEDDED_PROFILES[profile_name]))
    known = ", ".join(sorted(EMBEDDED_PROFILES))
    raise ValueError(f"Unknown profile {profile_name!r}. Known: {known}")


def width_mm(profile: Mapping, width: str = "single") -> float:
    widths = profile.get("widths", {})
    if width not in widths:
        raise ValueError(f"Width {width!r} not present in profile {profile.get('profile')!r}")
    entry = widths[width]
    if "mm" in entry:
        return float(entry["mm"])
    if "cm" in entry:
        return float(entry["cm"]) * 10.0
    if "inch" in entry:
        return float(entry["inch"]) * 25.4
    raise ValueError(f"Cannot determine mm width for {width!r}")


def mm_to_inch(value_mm: float) -> float:
    return float(value_mm) / 25.4


def size_inches(profile: Mapping | str, width: str = "single", height_mm: float | None = None,
                aspect: float = 0.72) -> tuple[float, float]:
    """Return `(width_in, height_in)` from profile physical dimensions."""
    prof = load_profile(profile)
    w_mm = width_mm(prof, width)
    h_mm = height_mm if height_mm is not None else w_mm * aspect
    return (mm_to_inch(w_mm), mm_to_inch(h_mm))


def apply_profile_style(profile_name: str = "nature_main", width: str = "single") -> dict:
    """Apply matplotlib rcParams for the selected profile and return the profile."""
    profile = load_profile(profile_name)
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:
        raise RuntimeError("matplotlib is required for apply_profile_style") from exc

    font = profile.get("font", {})
    line = profile.get("line", {})
    axis = profile.get("axis", {})
    tick = profile.get("tick", {})
    grid = profile.get("grid", {})
    axis_width = max(float(axis.get("spine_width_pt", line.get("target_pt", 0.75))), float(line.get("min_pt", 0.28)))
    tick_width = float(tick.get("major_width_pt", 0.60))
    tick_length = float(tick.get("major_length_pt", 2.50))
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": font.get("family", ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"]),
        "font.size": font.get("label_target_pt", 7),
        "axes.labelsize": font.get("label_target_pt", 7),
        "xtick.labelsize": font.get("tick_target_pt", 6),
        "ytick.labelsize": font.get("tick_target_pt", 6),
        "legend.fontsize": font.get("tick_target_pt", 6),
        "axes.linewidth": axis_width,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": bool(grid.get("default", False)),
        "grid.color": grid.get("color", "#E5E5E5"),
        "grid.linewidth": float(grid.get("linewidth_pt", 0.30)),
        "grid.alpha": float(grid.get("alpha", 0.28)),
        "xtick.direction": tick.get("direction", "out"),
        "ytick.direction": tick.get("direction", "out"),
        "xtick.major.width": tick_width,
        "ytick.major.width": tick_width,
        "xtick.major.size": tick_length,
        "ytick.major.size": tick_length,
        "xtick.minor.visible": bool(tick.get("minor_visible", False)),
        "ytick.minor.visible": bool(tick.get("minor_visible", False)),
        "legend.frameon": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.unicode_minus": False,
        "figure.figsize": size_inches(profile, width=width),
        "savefig.dpi": int(profile.get("export", {}).get("final_raster_dpi", 300)),
        "savefig.bbox": "tight",
    })
    return profile


def _flatten_axes(axes) -> list:
    if axes is None:
        return []
    if isinstance(axes, (list, tuple)):
        out = []
        for item in axes:
            out.extend(_flatten_axes(item))
        return out
    try:
        import numpy as np
        if isinstance(axes, np.ndarray):
            return [ax for ax in axes.ravel()]
    except Exception:
        pass
    return [axes]


def add_panel_labels(fig, axes, profile: Mapping | str, start: int = 0,
                     x: float = -0.18, y: float = 1.05) -> list:
    """Add journal-profile panel labels to axes and return created Text objects."""
    prof = load_profile(profile)
    panel = prof.get("panel_label", {})
    uppercase = panel.get("case") == "uppercase"
    weight = panel.get("weight", "bold")
    fontsize = panel.get("target_pt", 8)
    labels = []
    for i, ax in enumerate(_flatten_axes(axes), start=start):
        letter = chr(ord("A" if uppercase else "a") + i)
        labels.append(ax.text(
            x, y, letter,
            transform=ax.transAxes,
            fontsize=fontsize,
            fontweight=weight,
            va="top",
            ha="left",
        ))
    return labels


def export_figure(fig, basename: str | Path, profile: Mapping | str,
                  formats: Sequence[str] | None = None,
                  dpi: int | None = None, audit: bool = True,
                  purpose: str = "ppt",
                  transparent_raster: bool | None = None,
                  auto_fix_layout: bool = True,
                  report_color_warnings: bool = True) -> list[Path]:
    """Save a figure for the intended downstream workflow.

    Default `purpose="ppt"` emits SVG + transparent PNG. SVG is the preferred
    editable file for PowerPoint assembly; PNG is the robust preview/fallback.
    PDF remains available for final artwork or explicit format requests.
    """
    prof = load_profile(profile)
    base = Path(basename)
    base.parent.mkdir(parents=True, exist_ok=True)
    dpi = int(dpi or prof.get("export", {}).get("final_raster_dpi", 300))
    if formats is None:
        if purpose == "ppt":
            formats = ("svg", "png")
        elif purpose in {"final", "final_artwork", "submission"}:
            formats = ("pdf", "svg", "png")
        else:
            formats = ("svg", "png")
    if transparent_raster is None:
        transparent_raster = purpose == "ppt"
    qa_issues: list[tuple[str, str]] = []
    qa_actions: list[str] = []
    if auto_fix_layout or report_color_warnings:
        try:
            from visual_qa import qa_figure
            qa_issues, qa_actions = qa_figure(
                fig,
                auto_fix=auto_fix_layout,
                include_color=report_color_warnings,
                allow_canvas_resize=purpose == "ppt",
            )
        except Exception as exc:
            qa_issues = [("WARN", f"visual QA skipped: {exc}")]
    saved: list[Path] = []
    for fmt in formats:
        path = base.with_suffix("." + fmt.lower().lstrip("."))
        if fmt.lower() in {"png", "jpg", "jpeg", "tif", "tiff"}:
            fig.savefig(
                path,
                dpi=dpi,
                bbox_inches="tight",
                transparent=transparent_raster,
                facecolor="none" if transparent_raster else "white",
            )
        else:
            fig.savefig(path, bbox_inches="tight", facecolor="white")
        saved.append(path)
    if audit:
        audit_path = base.with_suffix(".figure_audit.md")
        audit_path.write_text(
            render_audit(prof, saved, dpi, purpose, transparent_raster, qa_actions, qa_issues),
            encoding="utf-8",
        )
        saved.append(audit_path)
    return saved


def render_audit(profile: Mapping, files: Sequence[Path], dpi: int,
                 purpose: str = "ppt", transparent_raster: bool = False,
                 qa_actions: Sequence[str] = (),
                 qa_issues: Sequence[tuple[str, str]] = ()) -> str:
    widths = profile.get("widths", {})
    return "\n".join([
        "# Figure Audit",
        "",
        f"- profile: `{profile.get('profile')}`",
        f"- journal: `{profile.get('journal')}`",
        f"- source_date: `{profile.get('source_date')}`",
        f"- widths: `{json.dumps(widths, ensure_ascii=False)}`",
        f"- font: `{profile.get('font', {}).get('family')}`",
        f"- panel_label: `{profile.get('panel_label')}`",
        f"- line_min_pt: `{profile.get('line', {}).get('min_pt')}`",
        f"- raster_dpi: `{dpi}`",
        f"- downstream_purpose: `{purpose}`",
        f"- transparent_raster: `{transparent_raster}`",
        "- auto_layout_fixes:",
        *([f"  - {x}" for x in qa_actions] or ["  - none"]),
        "- qa_warnings:",
        *([f"  - {level}: {message}" for level, message in qa_issues] or ["  - none"]),
        "- files:",
        *[f"  - `{p.name}`" for p in files],
        "",
        "Programmatic file checks and visual QA should be recorded here after review.",
        "",
    ])


def _check_raster(path: Path, min_dpi: int) -> tuple[list[str], dict]:
    issues: list[str] = []
    info: dict = {}
    try:
        from PIL import Image
    except Exception:
        return ["WARN: Pillow not installed; skipped raster DPI check."], info
    with Image.open(path) as im:
        info["pixels"] = im.size
        dpi = im.info.get("dpi")
        info["dpi"] = dpi
        if dpi:
            dx, dy = dpi
            if min(dx, dy) + 0.5 < min_dpi:
                issues.append(f"FAIL: raster DPI {dpi} is below {min_dpi}.")
        else:
            issues.append("WARN: raster file has no embedded DPI metadata.")
    return issues, info


def _check_pdf(path: Path) -> tuple[list[str], dict]:
    issues: list[str] = []
    info: dict = {}
    try:
        from pypdf import PdfReader
    except Exception:
        return ["WARN: pypdf not installed; skipped PDF font audit."], info
    reader = PdfReader(str(path))
    info["pages"] = len(reader.pages)
    bad_fonts: set[str] = set()
    for page in reader.pages:
        resources = page.get("/Resources") or {}
        fonts = resources.get("/Font") or {}
        for _, font_obj in fonts.items():
            font = font_obj.get_object()
            subtype = str(font.get("/Subtype", ""))
            base = str(font.get("/BaseFont", "?"))
            if "Type3" in subtype:
                bad_fonts.add(base)
    if bad_fonts:
        issues.append("FAIL: PDF contains Type 3 fonts: " + ", ".join(sorted(bad_fonts)))
    return issues, info


def _check_svg(path: Path) -> tuple[list[str], dict]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    issues: list[str] = []
    if "base64" in text and "<image" in text:
        issues.append("WARN: SVG contains base64 embedded image; ensure this is intentional raster content.")
    if "<text" not in text:
        issues.append("WARN: SVG has no <text> elements; text may have been outlined.")
    return issues, {"bytes": path.stat().st_size}


def check_file(path: str | Path, profile: Mapping | str, min_dpi: int | None = None) -> tuple[list[str], dict]:
    path = Path(path)
    prof = load_profile(profile)
    min_dpi = int(min_dpi or prof.get("raster", {}).get("min_dpi")
                  or prof.get("raster", {}).get("embedded_min_ppi")
                  or 300)
    ext = path.suffix.lower()
    if ext in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}:
        return _check_raster(path, min_dpi)
    if ext == ".pdf":
        return _check_pdf(path)
    if ext == ".svg":
        return _check_svg(path)
    return [f"WARN: no checker implemented for {ext}."], {"bytes": path.stat().st_size}


def doctor() -> dict:
    checks = {"python": sys.version.split()[0]}
    for mod in ["matplotlib", "PIL", "pypdf", "yaml", "numpy"]:
        try:
            __import__(mod)
            checks[mod] = "ok"
        except Exception:
            checks[mod] = "missing"
    return checks


def _cmd_profile(args: argparse.Namespace) -> int:
    profile = load_profile(args.profile)
    print(json.dumps(profile, ensure_ascii=False, indent=2))
    return 0


def _cmd_doctor(args: argparse.Namespace) -> int:
    print(json.dumps(doctor(), ensure_ascii=False, indent=2))
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    profile = load_profile(args.profile)
    had_fail = False
    for item in args.files:
        path = Path(item)
        if not path.exists():
            print(f"{path}: FAIL missing file")
            had_fail = True
            continue
        issues, info = check_file(path, profile, min_dpi=args.min_dpi)
        verdict = "PASS"
        if any(x.startswith("FAIL") for x in issues):
            verdict = "FAIL"
            had_fail = True
        elif issues:
            verdict = "WARN"
        print(f"{path}: {verdict}")
        if info:
            print("  info:", json.dumps(info, ensure_ascii=False))
        for issue in issues:
            print(" ", issue)
    return 1 if had_fail and args.strict else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Nature/Science figure skill helpers")
    sub = parser.add_subparsers(required=True)
    p = sub.add_parser("profile", help="Print a journal profile as JSON")
    p.add_argument("profile", choices=sorted(EMBEDDED_PROFILES))
    p.set_defaults(func=_cmd_profile)

    p = sub.add_parser("doctor", help="Check optional Python dependencies")
    p.set_defaults(func=_cmd_doctor)

    p = sub.add_parser("check", help="Run basic file-level compliance checks")
    p.add_argument("files", nargs="+")
    p.add_argument("--profile", default="nature_main", choices=sorted(EMBEDDED_PROFILES))
    p.add_argument("--min-dpi", type=int, default=None)
    p.add_argument("--strict", action="store_true")
    p.set_defaults(func=_cmd_check)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
