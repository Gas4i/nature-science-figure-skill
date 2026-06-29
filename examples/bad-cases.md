# 负例测试清单

这些不是给用户看的教程，而是用于 forward-test skill 是否会拦截常见坏图。

## 必须触发 FAIL 或 WARN

1. 字号小于 `6 pt`。
2. Science 图中 panel label 使用小写，或 Nature 图中 panel label 使用大写但未说明理由。
3. Science 图线宽低于 `0.28 pt`。
4. 图宽不是 profile preset，且没有说明用途。
5. 统计图只输出 PNG/JPEG，没有 PDF/SVG/EPS。
6. PDF 含 Type 3 字体。
7. SVG 将所有文字转成 path 或嵌入 base64 位图作为主图。
8. 图像嵌入分辨率低于 `300 ppi`。
9. RGB 图被错误转为 CMYK。
10. 红绿不可辨配色，且没有 marker/line/hatch 冗余编码。
11. 连续色图使用 `jet` 或 `rainbow`。
12. label 被裁切。
13. legend 遮挡数据。
14. linked image 或 raster source 未 embedded。
15. 用户要求显著性星号但没有提供 p 值/检验方法。

## 好例通过条件

- 选定 profile。
- 最终物理尺寸正确。
- 有可编辑矢量输出和 PNG 预览。
- 字体、线宽、panel label、DPI 通过检查。
- 有 `figure_audit.md` 或等价 provenance。
