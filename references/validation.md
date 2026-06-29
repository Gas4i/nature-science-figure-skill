# 导出、合规检查与视觉 QA

使用场景：图完成前、导出最终文件前、声称 Nature/Science 合规前阅读本文件。

## 必须执行的闭环

1. 按 profile 的最终物理尺寸建图。
2. 渲染 `150-200 dpi` PNG 预览。
3. 做程序化检查。
4. 自动修复机械性硬问题。
5. 人眼或多模态 AI 读图检查剩余感知问题。
6. 导出最终矢量和栅格预览。
7. 写 `figure_audit.md` 或等价 provenance 记录。

默认下游目标是 PPT 拼装，因此 `export_figure()` 默认输出：

- `svg`：PPT 中优先插入的可编辑矢量版本。
- `png`：透明背景、高分辨率预览/兜底版本。
- `figure_audit.md`：审计记录。

只有在 `purpose="final_artwork"`、投稿归档或用户明确要求时，再额外输出 `pdf`。

## 程序化检查

检查：

- 最终宽高是否符合 profile。
- 栅格 DPI/ppi 是否符合要求。
- PDF 是否含 Type 3 字体。
- SVG 是否尽量保留文本。
- 数据图是否不合理地只有 raster 输出。
- 字体、字号、线宽是否符合 profile；panel label 只在最终多 panel 大图或用户明确要求时检查大小写。
- 普通 x-y 数据图是否默认开放轴，且没有不必要的完整外框。
- heatmap/image/map/confusion matrix/phase diagram 是否保留了定义图像区域所需的轻量边框。
- grid 是否默认关闭；若开启，是否仅为 major grid 且明显弱于数据和坐标轴。
- tick 是否向外、minor ticks 是否默认关闭，除非有明确读数需求。
- 输出格式是否包含可编辑矢量格式。

基础命令：

```bash
python scripts/figure_skill.py check figures/figure1.svg figures/figure1.png --profile nature_main
```

## 视觉检查

### 自动修复，不必询问用户

这些属于机械性硬问题，agent 应先自动处理，再重新渲染：

- tick label 重叠：旋转、缩短或减少 tick。
- legend 遮挡数据：移到图外、共享 legend 或 dedicated legend panel。
- 文本裁切：重跑 layout、增加边距、换行或升 panel 尺寸。
- 显著性标注被裁切：放宽 y-limit 或上移标注。

`scripts/visual_qa.py` 中的 `qa_figure(auto_fix=True)` 和 `export_figure(auto_fix_layout=True)` 会先尝试修复这些问题。

### 只报告，不默认改色

这些问题会影响观感或可访问性，但自动改动可能破坏语义，因此只写入 audit/WARN：

- 色盲模拟或灰度下类别难分。
- 颜色对比度偏低。
- 语义色彩与论文叙事可能冲突。
- 配色虽然可读但不够美观。

除非用户明确授权，或类别语义已经明确到可以安全映射，否则不要自动重配色。

检查 PNG 预览：

- 中文、负号、希腊字母、单位符号是否缺字或变方框。
- 标题、轴标签、legend、tick 是否被裁切。
- x tick 是否互相重叠。
- legend 是否压住数据。
- 对于最终多 panel 大图：panel label 是否对齐、大小写是否统一。
- 对于准备交给 PPT 后续拼装的独立小图：默认不应出现 panel label，除非用户明确要求。
- colorbar 是否过小、无 label、离数据太近。
- 点、线、误差棒、显著性括号是否被坐标范围裁掉。
- 红绿或低对比度类别是否不可分。
- 灰度下是否仍能区分类别。
- 多 panel 之间颜色、marker、线型、量纲是否一致。

## 回改规则

- 缺字：修字体栈，中文图启用 CJK 字体，负号用 ASCII hyphen-minus 或确认字体支持。
- 裁切：增加边距、换行、缩短标签、使用 constrained layout。
- legend 压数据：移到图外、共享 legend、dedicated legend panel 或直接标注。
- tick 重叠：旋转、缩短标签、减少 tick、升一级 panel 尺寸。
- 配色不可分：换 Paul Tol bright/colorblind-aware palette，加 marker/line/hatch。
- 数据被裁：扩大 axis limit 或使用 `ax.margins()`。

## Provenance 记录模板

每张最终图至少记录：

- journal profile 和 source date。
- 使用的官方依据文件。
- 最终物理尺寸。
- 字体和最小字号。
- 最小线宽。
- 色彩策略。
- 输出文件和 DPI。
- 程序检查结果。
- 视觉 QA 结果。
- 未解决风险。

如果这份记录无法诚实填写，不要声称图已合规。
