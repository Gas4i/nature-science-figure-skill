# Palette Presets

## Required Palette Routing

All new figures and revised existing figures should use a skill palette preset unless there is a documented reason not to. Record `palette_name`, why it fits the data, redundant encodings used, and any rejected alternatives in the audit/provenance note.

Default routing:

1. High-contrast line/scatter comparisons, unordered categorical groups, or curves overlaid with raw points/error bars where softer red is preferred: `tol_hybrid`.
2. Higher-saturation Paul Tol bright categorical figures: `paul_tol_bright`.
3. Control/treatment/treatment or gray/blue/red semantics: `nature654_gray_blue_red_2026`.
4. Two-group strong contrast: `nature_energy_red_blue_2026`.
5. Natural/ecological/profile categories: `nature_food_natural_2026`.
6. Muted biomedical multi-condition data, especially 4-5 related groups: `natmed_senescence_2026`.
7. SSP scenarios with matching labels: `natcomm_ssp_2025`.
8. Diverging differences, signed heatmaps, or red/blue gradients: `nature637_red_blue_2025`.
9. Semantic house-style figures where blue=key method, green=improvement, red/pink=contrast, gray=neutral/background: `scientific_figure_house`.

If none fit, propose a custom palette only after explaining why the presets are insufficient. Custom palettes must still be RGB, colorblind-aware, grayscale-checked, and paired with redundant encoding when useful.

For programmatic routing, prefer:

```python
from scripts.plot_helpers import get_palette, recommend_palette

palette_name, palette_reason = recommend_palette(
    chart_type="line_scatter_overlay",
    category_count=3,
)
colors = get_palette(palette_name)
```

使用场景：需要为 Nature/Science 风格科研图选择颜色、解释颜色来源、或避免 agent 随意套用不明来源色板时阅读本文件。

## 原则

- Nature/Science 官方规则不是固定一套 HEX 色板，而是要求 RGB、色盲友好、避免难分红绿组合、避免 `jet`/`rainbow`、必要时用 marker/line style/直接标注等冗余编码。
- 本 skill 只保留少量可解释 preset：Tol hybrid、Paul Tol bright、语义 house palette，以及用户指定的 article-inspired palettes。
- Article-inspired palette 只表示“从公开文章图像近似抽色得到的风格参考”，不要声称为 Nature/Science 官方推荐色板。
- 自动 QA 发现灰度或色盲模拟风险时，只写入 WARN；除非用户授权，不默认重配色。

## 默认分类色板

### `paul_tol_bright`

用途：高对比分类线图、散点图、组间比较。

```python
["#4477AA", "#EE6677", "#228833", "#CCBB44",
 "#66CCEE", "#AA3377", "#BBBBBB"]
```

来源：Paul Tol colour schemes。适合主图，但仍需灰度/色盲 QA。

### `tol_hybrid`

Source: Paul Tol bright sequence with the second red softened to the Paul Tol muted red (`#CC6677`). This is a local hybrid palette for figures where bright categorical contrast is useful but the default Tol bright red (`#EE6677`) is too saturated for a manuscript main figure.

Use for line/scatter overlays and three-mechanism comparisons where the first three colors map naturally to blue = simulation/key series, softened red = experiment/contrast, and green = third mechanism or positive series.

```python
["#4477AA", "#CC6677", "#228833", "#CCBB44",
 "#66CCEE", "#AA3377", "#BBBBBB"]
```
## Article-Inspired Presets
### `nature_energy_red_blue_2026`

来源：本地论文配色审计文件 `palette_01`，paper 标注为 Nature Energy 2026，DOI `10.1038/s41560-026-02024-7`。

用途：两组直接对比，尤其是实验组/对照组、处理组/基础组等强对比场景。颜色高饱和，适合重点小图或 PPT，但投稿图中需要做灰度/色盲 QA。

```python
{
    "primary_red": "#FA3C3C",
    "primary_blue": "#33B2FF",
}
```

### `nature654_gray_blue_red_2026`

来源：本地论文配色审计文件 `palette_02`，paper 标注为 Nature 654, 85-91 (2026)，DOI `10.1038/s41586-026-10557-w`。

用途：三组对照：灰色作为 control，蓝色和红色作为两个 treatment/experimental groups。

```python
{
    "control_gray": "#C2C4C3",
    "treatment_blue": "#184B88",
    "treatment_red": "#E96465",
}
```

### `nature_food_natural_2026`

来源：本地论文配色审计文件 `palette_03`，paper 标注为 Nature Food 7, 334-344 (2026)，DOI `10.1038/s43016-026-01313-4`。

用途：三组自然柔和分类，适合食品、环境、生态、群体 profile 等不希望颜色太刺眼的图。

```python
{
    "profile_1": "#C3B99E",
    "profile_2": "#527995",
    "profile_3": "#B76366",
}
```

### `natmed_senescence_2026`

Source: user-provided Nat Med 2026-style palette reference, DOI `10.1038/s41591-026-04366-x`. Approximate extraction, not an official Nature/Science palette.

Use for muted biomedical multi-condition figures with 4-5 related groups, especially when a neutral/control group plus several soft treatment/condition colors are needed.

```python
{
    "neutral_gray": "#CCCCCC",
    "warm_peach": "#F2CAAD",
    "pale_blue": "#DCE4F8",
    "soft_red": "#ECAEA9",
    "sage_green": "#ACBDA9",
}
```

### `natcomm_ssp_2025`

来源：Wu et al., Nature Communications 16, 7420 (2025), Fig. 5，DOI `10.1038/s41467-025-62871-y`。颜色为 article-inspired approximate extraction，不是期刊官方 palette。

用途：只保留原图底部 SSP 情景条的最后四个颜色，适合 `ssp126/ssp245/ssp370/ssp585` 这类情景分组。不要用它表示适应率线条，也不要作为普通无语义分类默认。

```python
{
    "ssp126": "#D4A96B",
    "ssp245": "#BCAFAA",
    "ssp370": "#AC0000",
    "ssp585": "#2D332F",
}
```

### `nature637_red_blue_2025`

来源：Bourgund et al., Nature 637, 57-62 (2025), Fig. 1，DOI `10.1038/s41586-024-08270-7`。颜色为 article-inspired approximate extraction，不是期刊官方 palette。

用途：红蓝正负/发散量、heatmap、相关矩阵、差值图。该 preset 按用户提供的 Nature 637 风格参考图整理为红色 7 阶和蓝色 7 阶渐变，不再作为离散示意图杂色板。

```python
{
    "red_gradient": [
        "#F8EAE1", "#FBE3D6", "#FAD4BF", "#F5AC8B",
        "#C6403D", "#A81428", "#780522",
    ],
    "blue_gradient": [
        "#EDF2F6", "#C1DDE9", "#84BDDA", "#74B0D2",
        "#3685BB", "#256CAE", "#134B87",
    ],
}
```

### `scientific_figure_house`

Source: local `scientific-figure-making` / figures4papers house style. This is a semantic house palette rather than an article-inspired journal palette.

Use when the figure needs consistent semantic roles across methods or panels: blue for the key/proposed method, green for improvements or positive bands, red/pink for contrasts or baselines, gray for neutral/background categories, and gold/teal/violet as limited accents.

Alias: `figures4papers_house`.

```python
{
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE",
    "green_2": "#AADCA9",
    "green_3": "#8BCF8B",
    "red_1": "#F6CFCB",
    "red_2": "#E9A6A1",
    "red_strong": "#B64342",
    "neutral": "#CFCECE",
    "highlight": "#FFD700",
    "teal": "#42949E",
    "violet": "#9A4D8E",
}
```

## 使用 API

```python
from scripts.plot_helpers import get_palette

colors = get_palette("paul_tol_bright")
scenario = get_palette("natcomm_ssp_2025", as_dict=True)
```

优先级：

1. 线图/散点/实验点与模拟曲线叠加，且希望红色更柔和：`tol_hybrid`。
2. 更高饱和度的无序分类对比：`paul_tol_bright`。
3. 三组 control/treatment/treatment：`nature654_gray_blue_red_2026`。
4. 两组强对比：`nature_energy_red_blue_2026`。
5. 三组自然柔和分类：`nature_food_natural_2026`。
6. 4-5 组柔和 biomedical 条件：`natmed_senescence_2026`。
7. SSP 情景分组且语义匹配：`natcomm_ssp_2025`。
8. 红蓝发散或正负差值图：`nature637_red_blue_2025`。
9. 蓝/绿/红/灰语义角色明确的 house-style 图：`scientific_figure_house`。
