# 期刊 Profile 与官方依据

使用场景：解释或更新 `profiles/*.yaml` 时阅读本文。公开版 skill 不再分发 Nature/Science 官方 PDF、文章图像或 Illustrator 模板；规则摘要和可执行参数保存在 `profiles/`，官方来源入口保存在 `references/source-links.md`。

## 证据原则

- 优先使用 Nature、Nature Portfolio、Science、AAAS 的官方页面或官方 PDF。
- `references/source-links.md` 记录公开入口、访问对象和本 skill 已保留的规则摘要。
- 如果你在本地下载官方 PDF/模板用于审计，可以放在私有 `references/sources/` 或仓库外目录，但不要提交到公开 GitHub。
- 刷新来源时记录 URL、检查日期、文件大小和 SHA256；不要把搜索结果摘要当作最终规范。

## Nature Main

主要公开入口见 `references/source-links.md#nature-main`。

可执行规则：

- 单栏宽度 `89 mm`。
- 双栏宽度 `183 mm`。
- 必要时可使用 `120-136 mm` 的一栏半宽度，但不要作为默认。
- 字体使用 Helvetica/Arial 兼容无衬线字体。
- 普通标签目标 `7 pt`，低于 `5 pt` 警告。
- 原始研究图件使用 RGB。
- 位图元素按最终尺寸至少 `300 dpi`。
- 图表和线条图优先输出可编辑矢量文件。

## Science Main

主要公开入口见 `references/source-links.md#science-main`。

可执行规则：

- 每个 figure 作为独立文件提交，和 manuscript text 分开。
- 单栏宽度 `9 cm / 3.6 in`。
- 双栏宽度 `18.3 cm / 7.25 in`。
- 字体使用 Arial 或 Helvetica。
- panel parts 使用 `10 pt bold`。
- labels 使用 `6-9 pt`。
- 最终印刷尺寸下线宽至少 `0.28 pt`。
- photographic raster images 在最终尺寸下 `300-500 dpi`。
- vector 文件中的 embedded images 至少 `300 ppi`。
- full-color artwork 使用 RGB。
- 避免红绿组合；无法避免时必须增加形状、纹理、marker 或线型冗余编码。
- R 作图优先导出 vector SVG，再进入最终包装。

## 共享兼容层

Nature 和 Science 可以共用：

- 物理尺寸建图。
- Arial/Helvetica 兼容字体栈。
- 矢量优先导出。
- RGB 默认。
- 色盲友好配色。
- 最小线宽 `0.28 pt` 的保守底线。
- 栅格 `>=300 dpi/ppi` 的保守底线。
- PNG 预览和审计闭环。

不要共用：

- 硬编码图宽。
- panel label 大小写。
- Science 特有的 `6-9 pt labels` 和 `10 pt bold panel parts` 文案。
