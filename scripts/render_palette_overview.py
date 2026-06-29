#!/usr/bin/env python
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from figure_skill import get_palette  # noqa: E402


PALETTES = [
    ("tol_hybrid", "Tol bright sequence with softened muted red"),
    ("paul_tol_bright", "High-contrast line/scatter overlays"),
    ("nature_energy_red_blue_2026", "Two-group high contrast"),
    ("nature654_gray_blue_red_2026", "Control/treatment/treatment"),
    ("nature_food_natural_2026", "Natural/profile three groups"),
    ("natmed_senescence_2026", "Muted biomedical 4-5 conditions"),
    ("natcomm_ssp_2025", "SSP scenario labels"),
    ("nature637_red_blue_2025", "Diverging red/blue gradients"),
    ("scientific_figure_house", "Semantic blue/green/red/neutral house style"),
]


def _flatten_palette(name: str) -> list[str]:
    palette = get_palette(name, as_dict=True)
    colors: list[str] = []
    if isinstance(palette, dict):
        for value in palette.values():
            if isinstance(value, list):
                colors.extend(value)
            else:
                colors.append(value)
        return colors
    return list(palette)


def render() -> list[Path]:
    out_dir = SKILL_DIR / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_h = max(5.2, len(PALETTES) * 0.58)
    fig, ax = plt.subplots(figsize=(9.2, fig_h))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(PALETTES))
    ax.axis("off")

    for row, (name, note) in enumerate(PALETTES):
        y = len(PALETTES) - row - 0.82
        ax.text(0.02, y + 0.19, name, fontsize=10, fontweight="bold", ha="left", va="center")
        ax.text(0.02, y - 0.06, note, fontsize=7.5, color="#555555", ha="left", va="center")
        colors = _flatten_palette(name)
        x0 = 0.38
        swatch_w = min(0.055, 0.54 / max(len(colors), 1))
        for i, color in enumerate(colors):
            x = x0 + i * (swatch_w + 0.008)
            ax.add_patch(Rectangle((x, y - 0.08), swatch_w, 0.30, facecolor=color, edgecolor="#FFFFFF", linewidth=0.8))
            if len(colors) <= 7:
                ax.text(x + swatch_w / 2, y - 0.14, color.upper(), fontsize=5.5, ha="center", va="top", color="#444444")
            else:
                ax.text(x + swatch_w / 2, y - 0.13, color.upper(), fontsize=4.2, rotation=45, ha="right", va="top", color="#444444")

    ax.text(0.02, len(PALETTES) - 0.15, "Nature/Science Figure Skill Palette Presets", fontsize=13, fontweight="bold")
    png = out_dir / "palette_presets_overview.png"
    svg = out_dir / "palette_presets_overview.svg"
    fig.savefig(png, dpi=220, bbox_inches="tight", facecolor="white")
    fig.savefig(svg, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return [png, svg]


def main() -> None:
    for path in render():
        print(path)


if __name__ == "__main__":
    main()
