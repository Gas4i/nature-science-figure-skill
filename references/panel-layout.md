# 小图尺寸与多 Panel 排版

使用场景：制作多 panel figure，或一个 agent 每次只产出一个小图，后续再组合成大图时阅读本文件。

## 尺寸边界

Nature 和 Science 官方主要规定整张 figure 的最终出版宽度，不直接规定每个小 panel 的固定尺寸。下面 preset 是由官方整图宽度推导出的工程规则，不是官方逐字硬性要求。

默认 gutter：

- 紧凑组合：`3 mm`
- 标准组合：`4 mm`
- 有 colorbar、scale bar 或长标签：`5-6 mm`

## Panel Preset

| Preset | 宽 | 高 | 适用 | 约束 |
|---|---:|---:|---|---|
| `micro` | `28 mm` | `24 mm` | image tile、小分布、示意单元 | minimal/no axes，共享 legend |
| `compact` | `43 mm` | `36 mm` | 小 box/violin/bar/scatter/line | compact axes，共享或外置 legend |
| `standard` | `58 mm` | `48 mm` | 常规 scatter/line/bar、小 heatmap | 默认选择，可放完整坐标轴 |
| `half_width` | `89 mm` | `65 mm` | 主 panel、带 colorbar 或局部 legend | 信息量较大时使用 |
| `wide` | `128 mm` | `70 mm` | timeline、workflow、pathway、宽 heatmap | legend 外置或右侧 |

默认：`standard`。

## 常用网格

使用 `4 mm` gutter 时：

- Nature/Science 单栏 `89-90 mm`
  - 1 panel：`half_width`
  - 2 panels：`compact`
  - 3 panels：`micro`，只用于 very small multiples
- Nature/Science 双栏 `183 mm`
  - 2 panels：`half_width`
  - 3 panels：`standard`
  - 4 panels：`compact`
  - 5-6 panels：`micro`，必须共享轴/legend

## 自动升级规则

出现以下任一情况，panel 至少升一级：

- 包含 colorbar。
- x tick 标签长或需要旋转。
- 类别数超过 5。
- legend 条目超过 4。
- 有密集 annotation 或显著性括号。
- 图像 panel 同时需要 scale bar 和 label。

只有在没有独立轴标签、视觉结构很简单时才降级。

## Legend 策略

- 多 panel 优先共享 legend。
- legend 会遮挡数据时，使用 dedicated legend panel。
- 线条很多时，优先用曲线末端直接标注。
- 不允许 legend 压住关键数据。

## Panel Label

- Nature：小写粗体 `a, b, c`。
- Science：大写粗体 `A, B, C`。
- 位置要统一，通常放在 panel 左上角或略外侧。
- 默认给 PPT 拼装的独立小图不要自动加 panel label；保持小图本身干净，避免后续拼图时出现重复或错位标签。
- 只有在生成最终多 panel 大图、用户明确要求小图自带标签，或该小图本身已经是不可再拆分的多 panel 图时，才使用 `scripts.figure_skill.add_panel_labels()`。
- 如果最终在 PowerPoint、Illustrator、Inkscape 或 Affinity Designer 中组合大图，应在组合阶段统一添加 panel label，并统一大小写、字号、粗细和相对位置。
