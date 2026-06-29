# Palette Presets

使用场景：需要为 Nature/Science 风格科研图选择颜色、解释颜色来源、或避免 agent 随意套用不明来源色板时阅读本文件。

## 原则

- Nature/Science 官方规则不是固定一套 HEX 色板，而是要求 RGB、色盲友好、避免难分红绿组合、避免 `jet`/`rainbow`、必要时用 marker/line style/直接标注等冗余编码。
- 本 skill 只保留少量可解释 preset：Okabe-Ito/Wong、Paul Tol bright/muted、以及用户指定的两套 article-inspired palette。
- Article-inspired palette 只表示“从公开文章图像近似抽色得到的风格参考”，不要声称为 Nature/Science 官方推荐色板。
- 自动 QA 发现灰度或色盲模拟风险时，只写入 WARN；除非用户授权，不默认重配色。

## 默认分类色板

### `okabe_ito`

用途：无语义分类、2-8 个类别的默认选择。

```python
["#E69F00", "#56B4E9", "#009E73", "#F0E442",
 "#0072B2", "#D55E00", "#CC79A7", "#000000"]
```

来源：Okabe-Ito / Wong 常用色盲友好科研色板。黄色在白底上线/点较弱，必要时换顺序、加黑边或 marker。

### `paul_tol_bright`

用途：高对比分类线图、散点图、组间比较。

```python
["#4477AA", "#EE6677", "#228833", "#CCBB44",
 "#66CCEE", "#AA3377", "#BBBBBB"]
```

来源：Paul Tol colour schemes。比 Okabe-Ito 更柔和一些，适合主图，但仍需灰度/色盲 QA。

### `paul_tol_muted`

用途：类别较多、希望图面更安静的论文主图。

```python
["#332288", "#88CCEE", "#44AA99", "#117733", "#999933",
 "#DDCC77", "#CC6677", "#882255", "#AA4499", "#DDDDDD"]
```

来源：Paul Tol colour schemes。类别多时不要只靠颜色，配合 marker/line style。

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

## 使用 API

```python
from scripts.plot_helpers import get_palette

colors = get_palette("okabe_ito")
scenario = get_palette("natcomm_ssp_2025", as_dict=True)
```

优先级：

1. 无语义分类：`okabe_ito`。
2. 更高对比：`paul_tol_bright`。
3. 更安静、多类别：`paul_tol_muted`。
4. 两组强对比：`nature_energy_red_blue_2026`。
5. 三组 control/treatment/treatment：`nature654_gray_blue_red_2026`。
6. 三组自然柔和分类：`nature_food_natural_2026`。
7. SSP 情景分组且语义匹配：`natcomm_ssp_2025`。
8. 红蓝发散或正负差值图：`nature637_red_blue_2025`。
