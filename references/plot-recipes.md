# 科研图 Recipe

使用场景：需要决定具体图型实现细节时阅读本文件。

## 共享风格

- 多数 analytic plots 关闭 top/right spines。
- 普通 x-y 数据图默认使用开放坐标轴：只保留 left/bottom spines；不要给普通折线、散点、柱状、box/violin 图加完整矩形框。
- heatmap、image、microscopy、map、confusion matrix、phase diagram 等边界本身有语义的图，使用轻量完整边框。
- 坐标轴、tick 和 grid 是导航元素，不是数据元素；视觉权重必须低于数据线、点、误差棒和主要标注。
- 默认线宽层级：数据线约 1.1 pt，误差棒约 0.85 pt，坐标轴约 0.75 pt，tick 约 0.60 pt，grid 约 0.30 pt。
- tick 默认向外，major tick 长度约 2.5 pt；minor ticks 默认关闭。
- grid 默认关闭。只有 time-series、dose-response、calibration curve、large dynamic range、engineering performance comparison 等读数确实重要的图才开启。
- 开启 grid 时只用 major grid，不用 minor grid；优先 y-axis grid，浅灰、低 alpha，且必须弱于坐标轴和数据。
- legend 无边框；若遮挡数据，移到图外或放入 dedicated legend panel。
- 网格线轻量或不用。
- 标签直接服务数据解释，不做装饰。
- 使用 `pdf.fonttype=42`、`ps.fonttype=42`、`svg.fonttype="none"`。
- 禁止装饰性渐变、3D 效果、厚重背景阴影。
- 同一语义对象在多 panel 中必须保持同色、同 marker、同线型。
- 多指标比较图可以使用更宽横向布局，但最终宽度仍必须来自 journal profile。

## 配色

需要选择 palette 时先读 `references/palette-presets.md`。

默认规则：

1. 无语义分类默认使用 `get_palette("okabe_ito")`。
2. 高对比分类使用 `get_palette("paul_tol_bright")`。
3. 更安静或类别较多的论文主图使用 `get_palette("paul_tol_muted")`。
4. 只有当图的语义明确匹配时，才使用 article-inspired palette。
5. 类别超过颜色舒适区时，增加 marker、line style、直接标注；不要继续堆颜色。
6. 禁用 `jet` 和 `rainbow`。

连续色图：

- 顺序数据：`viridis`、`magma`、`cividis`。
- 发散数据：`RdBu_r` 等，并以有意义的参考点居中。
- 不要把发散 colormap 用在没有中心参考值的数据上。

## 组间比较

优先 box/violin + raw points 或 dot/interval。只有当数值本身就是聚合量且误差定义明确时，才使用柱状图。

可用 helper：

```python
from scripts.plot_helpers import make_grouped_bar, annotate_bars
```

规则：

- `series` 必须是二维结构：每行一个组，每列一个 category。
- 使用 bar 时必须考虑误差定义；小样本时叠加原始点或换成 box/strip。
- Science 场景可使用 hatch 提升灰度打印可分性；Nature 场景优先 marker/线型/直接标注，hatch 作为最后手段。

## 时间序列

用线 + 置信/SEM 阴影。每个 axis 的主要曲线控制在 2-4 条；更多曲线用 small multiples。

可用 helper：

```python
from scripts.plot_helpers import make_trend
```

规则：

- `x` 和每条 `y` 长度必须一致。
- 误差带通过 `bands` 传入，图注必须说明是 SD/SEM/CI。
- 曲线超过 4 条时，优先拆 panel 或用直接末端标注。
- SSP 情景分组可考虑 `natcomm_ssp_2025`，但需保留 `ssp126/ssp245/ssp370/ssp585` 的语义对应关系。

## 散点/相关

密集点用透明度。拟合线必须说明模型。轴标签写变量名和单位。

可用 helper：

```python
from scripts.plot_helpers import make_scatter
```

规则：

- 不要把无序点连线。
- 拟合线和 CI 只有在模型合理且方法说明清楚时添加。
- 数据很密时降低 alpha，必要时改用 hexbin/density。

## 热图/矩阵

必须有 colorbar label 和单位。矩阵较大时不要给每个格子塞小字。标签密集时升级 panel 尺寸。

可用 helper：

```python
from scripts.plot_helpers import make_heatmap
```

规则：

- `jet` 和 `rainbow` 会被 helper 拒绝。
- annotations 只适合小矩阵；大矩阵用 colorbar 和少量重点标注。
- 发散数据要选发散 colormap 并明确 center/reference；若需要 Nature 637 风格红蓝分级，可用 `nature637_red_blue_2025` 的 `red_gradient`/`blue_gradient` 组合。

## 图像/显微图

图像数据保留 raster；文字、箭头、scale bar 尽量保持 vector/editable。必须有 scale bar 或等价尺度信息。

## PCA/UMAP/Embedding

只有解释几何距离时才强制 equal aspect。provenance 中记录预处理和降维方法。

## Confusion Matrix

使用感知均匀顺序色图。说明显示的是 count、percent 还是 normalized rate。

## Volcano/Forest/Survival

遵守领域惯例，同时继续执行 profile 尺寸、字体、颜色和统计定义检查。

## 布局 Helper

```python
from scripts.plot_helpers import (
    create_subplots,
    dynamic_ylim,
    add_dedicated_legend,
    clean_axes,
)
```

- `create_subplots`：按 profile 最终尺寸创建 figure。
- `dynamic_ylim`：收紧 y 轴范围，但不能隐藏数据；比例/概率图通常仍应包含 0。
- `add_dedicated_legend`：legend 很大时放到专门 axis，避免遮挡数据。
- `clean_axes`：关闭 top/right spine，使用 outward major ticks，关闭 minor ticks，默认关闭 grid；只有传入 `grid=True` 时才开弱 major y-grid。
- `frame_axes`：heatmap/image 类边界有语义的图使用轻量完整边框。
