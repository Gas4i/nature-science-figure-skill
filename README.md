# Nature/Science Figure Skill

中文 | [English](#english)

一个非官方 Codex skill，用于制作、审计和打包 Nature / Science 风格的科研数据图。它面向论文主图、小图 panel、PPT 后处理拼图和投稿前图件检查，重点是让 AI agent 画图时有明确的尺寸、配色、线宽、导出和自查规则。

> 非官方声明：本项目不隶属于 Nature、Springer Nature、Science 或 AAAS，也不代表期刊官方认证。最终投稿前请以期刊官网当前说明为准。

## 主要功能

- 按 Nature / Science profile 选择最终物理尺寸，而不是随意用像素尺寸作图。
- 支持 Nature 单栏 `89 mm`、双栏 `183 mm`，Science 单栏 `90 mm`、双栏 `183 mm`。
- 提供小图 panel 尺寸建议：`micro`、`compact`、`standard`、`half_width`、`wide`。
- 默认面向 PPT 后处理输出：可编辑 `SVG` + 透明高分辨率 `PNG` + audit/provenance 记录。
- 默认普通数据图使用开放坐标轴：只保留 left / bottom spine，关闭 top / right spine。
- 默认关闭网格线；如确实需要读数辅助，只使用弱 major grid。
- 固化线宽层级：数据线强于坐标轴，坐标轴强于网格线。
- 提供色盲友好和论文启发配色：Okabe-Ito/Wong、Paul Tol bright/muted，以及若干 article-inspired palettes。
- 支持数据驱动图型选择，避免小样本均值柱状图、饼图、3D 效果、双 y 轴滥用、rainbow/jet colormap 等常见问题。
- 提供自动视觉 QA：检查裁切、tick 重叠、legend 遮挡、低对比度和色彩可访问性风险。
- 对硬性版式问题尝试自动修复；对色盲/低对比度等审美或可访问性问题写入 warning，不默认擅自改色。

## 适用场景

适合：

- 论文主图或补充图的数据图制作。
- 多 panel figure 中单个小图的标准化输出。
- 先由 AI / Python 出小图，再在 PowerPoint、Illustrator、Inkscape 或 Affinity Designer 中拼装大图。
- 需要一套可复用的 Nature / Science 风格 matplotlib 作图流程。
- 需要 AI agent 生成图后自查，并保留 audit 记录。

不适合：

- 交互式 dashboard。
- 地图制图、复杂 3D 可视化或信息图设计为主的图。
- 需要直接复刻某篇论文原图的版权材料。
- 取代最终投稿前的官方 artwork check。

## 安装

把整个文件夹复制到 Codex skills 目录：

```text
~/.codex/skills/nature-science-figure-skill
```

Windows 通常是：

```text
C:\Users\<YOUR_USER>\.codex\skills\nature-science-figure-skill
```

然后重启 Codex，或刷新 skill 索引。

也可以从 GitHub 克隆：

```powershell
git clone https://github.com/Gas4i/nature-science-figure-skill.git $HOME\.codex\skills\nature-science-figure-skill
```

## 快速使用

你可以这样请求 Codex：

```text
Use nature-science-figure-skill to plot this CSV as a Nature-style figure for PPT assembly.
```

中文示例：

```text
使用 nature-science-figure-skill，把这个 CSV 画成 Nature 风格小图，后续我要放进 PPT 拼图。
```

如果你已经有配色偏好：

```text
使用 nature-science-figure-skill，按 nature654_gray_blue_red_2026 配色画三组处理响应图。
```

## 推荐工作流

1. 明确目标期刊：`nature_main` 或 `science_main`。
2. 明确图件阶段：`draft`、`revision` 或 `final_artwork`。
3. 给出数据文件和图想表达的主要结论。
4. 让 agent 先 profile 数据，再选择图型。
5. 按 profile 的最终物理尺寸建图。
6. 导出 `SVG`、透明 `PNG` 和 audit note。
7. 在 PPT 或矢量软件中组合多个小图。
8. 最终投稿前重新核对期刊当前官方要求。

## 默认输出

默认目标是 PPT assembly，因此输出：

- `*.svg`：优先插入 PPT 或矢量软件的可编辑版本。
- `*.png`：透明背景、高分辨率预览或兜底版本。
- `*_audit.md` / `figure_audit.md`：记录 profile、尺寸、配色、导出参数、QA warning 和未解决风险。

只有在 `final_artwork`、投稿归档或用户明确要求时，才额外输出 `PDF`。

## 尺寸规则

整张 figure 的尺寸来自 profile：

| Profile | Single column | Double column | Notes |
|---|---:|---:|---|
| Nature | `89 mm` | `183 mm` | optional intermediate `120-136 mm` |
| Science | `90 mm` | `183 mm` | `9 cm` / `18.3 cm` |

小图 panel 推荐尺寸：

| Preset | Size | Typical use |
|---|---:|---|
| `micro` | `28 x 24 mm` | image tile, tiny distribution, minimal axes |
| `compact` | `43 x 36 mm` | small box, violin, bar, scatter, line |
| `standard` | `58 x 48 mm` | default small scatter, line, bar, small heatmap |
| `half_width` | `89 x 65 mm` | main panel, colorbar, local legend |
| `wide` | `128 x 70 mm` | timeline, workflow, pathway, wide heatmap |

默认小图使用 `standard`。遇到 colorbar、长标签、多 legend、密集注释时升一级。

## 样式规则

普通 x-y 数据图默认：

- left / bottom spines only；
- top / right spines off；
- tick direction outward；
- minor ticks off；
- grid off；
- legend frame off。

线宽默认：

- data line: about `1.1 pt`
- error bar: about `0.85 pt`
- axis spine: about `0.75 pt`
- major tick: about `0.60 pt`
- optional grid: about `0.30 pt`

Heatmap、image、microscopy、map、confusion matrix、phase diagram 等边界有语义的图，可以保留轻量完整边框。

## 配色

内置优先 palette：

- `okabe_ito`
- `paul_tol_bright`
- `paul_tol_muted`
- `nature_energy_red_blue_2026`
- `nature654_gray_blue_red_2026`
- `nature_food_natural_2026`
- `natcomm_ssp_2025`
- `nature637_red_blue_2025`

Article-inspired palettes 是根据论文图近似抽色整理，不是期刊官方 palette。使用它们时应保留语义匹配，并进行灰度/色盲/对比度检查。

## Python Helper 示例

```python
from pathlib import Path
import matplotlib.pyplot as plt

from scripts.figure_skill import apply_profile_style, size_inches, export_figure
from scripts.plot_helpers import make_trend, get_palette

profile = apply_profile_style("nature_main", width="single")
colors = get_palette("okabe_ito")

fig, ax = plt.subplots(
    figsize=size_inches(profile, width="single", height_mm=55),
    constrained_layout=True,
)

make_trend(
    ax,
    x=[0, 1, 2, 4],
    y_series=[[1.0, 1.4, 1.7, 2.1]],
    labels=["Treatment"],
    colors=[colors[0]],
    xlabel="Time (h)",
    ylabel="Signal (a.u.)",
)

export_figure(fig, Path("figures/example"), profile)
```

## 目录结构

```text
nature-science-figure-skill/
  SKILL.md
  README.md
  LICENSE
  agents/openai.yaml
  profiles/
  references/
  scripts/
```

关键文件：

- `SKILL.md`：Codex skill 入口和核心流程。
- `profiles/nature_main.yaml`：Nature profile。
- `profiles/science_main.yaml`：Science profile。
- `references/panel-layout.md`：小图尺寸与多 panel 组合规则。
- `references/palette-presets.md`：配色模板。
- `references/plot-recipes.md`：常见图型 recipe。
- `references/validation.md`：导出和 QA 规则。
- `scripts/figure_skill.py`：profile、尺寸、导出和检查 helper。
- `scripts/plot_helpers.py`：常见 matplotlib 作图 helper。

## 公开版说明

本仓库不分发第三方期刊指南 PDF、文章图像或 Illustrator 模板。官方来源入口和 provenance notes 放在 `references/source-links.md`。

最终投稿前，请重新核对 Nature / Science / AAAS / Springer Nature 当前官方说明。

## License

MIT License. See `LICENSE`.

---

## English

An unofficial Codex skill for creating, auditing, and packaging Nature- or Science-style scientific data figures. It is designed for manuscript figures, small panels, PPT-based figure assembly, and pre-submission visual QA.

> Disclaimer: this project is not affiliated with, endorsed by, or certified by Nature, Springer Nature, Science, or AAAS. Always verify current journal instructions before final submission.

## Features

- Uses final physical figure dimensions from Nature / Science profiles instead of arbitrary pixel sizes.
- Supports Nature single-column `89 mm`, Nature double-column `183 mm`, Science single-column `90 mm`, and Science double-column `183 mm`.
- Provides panel-size presets: `micro`, `compact`, `standard`, `half_width`, and `wide`.
- Defaults to PPT-friendly outputs: editable `SVG`, transparent high-resolution `PNG`, and an audit/provenance note.
- Uses low-clutter analytical axes by default: left/bottom spines only, top/right spines off.
- Keeps grid lines off by default; when needed, uses weak major grid lines only.
- Encodes a visual hierarchy where data lines are stronger than axes, and axes are stronger than grids.
- Provides colorblind-aware palettes and article-inspired palette presets.
- Encourages data-driven chart selection and rejects misleading defaults such as small-sample mean bars, pie charts, 3D effects, unrelated dual y-axes, and rainbow/jet colormaps.
- Runs visual QA for clipping, tick overlap, legend occlusion, low contrast, and color-accessibility warnings.
- Automatically repairs mechanical layout issues when possible; reports color/accessibility warnings without silently changing semantic colors.

## When to Use

Use this skill for:

- manuscript main figures or supplementary figures;
- standardized small panels for multi-panel figures;
- Python-generated small figures that will later be assembled in PowerPoint, Illustrator, Inkscape, or Affinity Designer;
- reusable Nature / Science-style matplotlib workflows;
- AI-agent figure generation with audit trails.

Do not use it as a replacement for official journal artwork checks.

## Installation

Copy this folder into your Codex skills directory:

```text
~/.codex/skills/nature-science-figure-skill
```

On Windows:

```text
C:\Users\<YOUR_USER>\.codex\skills\nature-science-figure-skill
```

Or clone from GitHub:

```powershell
git clone https://github.com/Gas4i/nature-science-figure-skill.git $HOME\.codex\skills\nature-science-figure-skill
```

Restart Codex or refresh the skill index after installation.

## Quick Start

Example prompt:

```text
Use nature-science-figure-skill to plot this CSV as a Nature-style figure for PPT assembly.
```

With a palette choice:

```text
Use nature-science-figure-skill and the nature654_gray_blue_red_2026 palette to plot this three-group treatment response.
```

## Recommended Workflow

1. Choose `nature_main` or `science_main`.
2. Choose the figure stage: `draft`, `revision`, or `final_artwork`.
3. Provide the dataset and the scientific claim the figure should support.
4. Let the agent profile the data before selecting a chart type.
5. Build the figure at final physical size.
6. Export SVG, transparent PNG, and an audit note.
7. Assemble multiple small panels in PPT or vector-design software.
8. Re-check the current official journal instructions before submission.

## Default Outputs

The default downstream target is PPT assembly:

- `*.svg`: editable vector output for PPT or vector editors;
- `*.png`: transparent high-resolution preview/fallback;
- `*_audit.md` / `figure_audit.md`: profile, size, palette, export settings, QA warnings, and unresolved risks.

PDF export is reserved for `final_artwork`, archival use, or explicit user requests.

## Size Rules

Full-figure dimensions:

| Profile | Single column | Double column | Notes |
|---|---:|---:|---|
| Nature | `89 mm` | `183 mm` | optional intermediate `120-136 mm` |
| Science | `90 mm` | `183 mm` | `9 cm` / `18.3 cm` |

Panel presets:

| Preset | Size | Typical use |
|---|---:|---|
| `micro` | `28 x 24 mm` | image tile, tiny distribution, minimal axes |
| `compact` | `43 x 36 mm` | small box, violin, bar, scatter, line |
| `standard` | `58 x 48 mm` | default small scatter, line, bar, small heatmap |
| `half_width` | `89 x 65 mm` | main panel, colorbar, local legend |
| `wide` | `128 x 70 mm` | timeline, workflow, pathway, wide heatmap |

The default panel preset is `standard`. Upgrade the panel size when there is a colorbar, long labels, many legend entries, or dense annotation.

## Style Defaults

Ordinary x-y analytical plots use:

- left / bottom spines only;
- top / right spines off;
- outward major ticks;
- minor ticks off;
- grid off;
- legend frame off.

Default line hierarchy:

- data line: about `1.1 pt`
- error bar: about `0.85 pt`
- axis spine: about `0.75 pt`
- major tick: about `0.60 pt`
- optional grid: about `0.30 pt`

Heatmaps, images, microscopy panels, maps, confusion matrices, and phase diagrams may use a light full frame when the plot boundary is meaningful.

## Palettes

Built-in priority palettes:

- `okabe_ito`
- `paul_tol_bright`
- `paul_tol_muted`
- `nature_energy_red_blue_2026`
- `nature654_gray_blue_red_2026`
- `nature_food_natural_2026`
- `natcomm_ssp_2025`
- `nature637_red_blue_2025`

Article-inspired palettes are approximate extractions from published figures. They are not official journal palettes.

## Python Helper Example

```python
from pathlib import Path
import matplotlib.pyplot as plt

from scripts.figure_skill import apply_profile_style, size_inches, export_figure
from scripts.plot_helpers import make_trend, get_palette

profile = apply_profile_style("nature_main", width="single")
colors = get_palette("okabe_ito")

fig, ax = plt.subplots(
    figsize=size_inches(profile, width="single", height_mm=55),
    constrained_layout=True,
)

make_trend(
    ax,
    x=[0, 1, 2, 4],
    y_series=[[1.0, 1.4, 1.7, 2.1]],
    labels=["Treatment"],
    colors=[colors[0]],
    xlabel="Time (h)",
    ylabel="Signal (a.u.)",
)

export_figure(fig, Path("figures/example"), profile)
```

## Repository Layout

```text
nature-science-figure-skill/
  SKILL.md
  README.md
  LICENSE
  agents/openai.yaml
  profiles/
  references/
  scripts/
```

## Public Distribution

This repository does not redistribute third-party journal guideline PDFs, article figures, or Illustrator templates. Official-source links and provenance notes are stored in `references/source-links.md`.

## License

MIT License. See `LICENSE`.
