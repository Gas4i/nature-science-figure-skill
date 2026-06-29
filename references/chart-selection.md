# 图型选择与误导性图表拦截

使用场景：用户没有明确指定图型，或指定图型可能不适合数据/论证目标时阅读本文件。

## 作图前必须确认

1. 这张图要支持什么结论。
2. 数据列类型：连续、分类、有序、时间、空间/图像、矩阵、网络、生存。
3. 样本量与重复结构：生物重复、技术重复、受试者、试验、测量点。
4. 分组结构：单分组、交叉分组、嵌套分组、配对/重复测量。
5. 单位、转换、归一化和排除规则。

如果结论或重复结构缺失，先问用户；若继续执行，必须明确写出工作假设。

## 决策表

| 数据形态 | 主要论证 | 首选图型 | 避免 |
|---|---|---|---|
| 单个连续变量 | 分布 | histogram、density、rug、box/violin + points | 只画均值柱 |
| 分类 + 连续 | 组间比较 | box/violin + strip、dot/interval、estimation plot | 小样本 mean-only bar |
| 两个连续变量 | 相关/关联 | scatter + 合理拟合/CI | 无序点硬连线 |
| 时间/顺序 + 数值 | 趋势 | line + uncertainty band、small multiples | 无顺序分类变量折线 |
| 多变量 | 结构/相关 | heatmap、clustered heatmap、pair grid、PCA/UMAP | 过载 grouped bar |
| 矩阵/图像 | 强度/空间结构 | heatmap/image + colorbar + units | rainbow/jet、无 colorbar |
| 比例/组成 | 组成变化 | stacked bar、100% bar、rate dot/interval | 默认 pie chart |
| 模型性能 | 多指标比较 | grouped dot/bar + interval、表格化 panel | 超大 legend 或无单位轴 |

## 必须拦截

- 每组 `n < 10` 却计划画不带原始点的均值柱。
- 有误差棒但未说明 SD/SEM/CI/IQR。
- 用户要求显著性星号但没有提供检验方法和结果。
- 双 y 轴用于无关量纲。
- 2D 数据使用 3D 柱、3D 饼或装饰性 3D。
- 连续色图使用 `jet` 或 `rainbow`。
- 分类变量用折线连接组均值，暗示不存在的顺序。
- legend 超过 5 类且没有直接标注、分组、拆图或共享 legend 策略。

## 论证优先

一张 figure 只讲一个核心结论。多个结论应该拆成 panel 或拆成不同 figure。多 panel 的顺序应服务于论文叙事，而不是服务于把所有结果塞满。
