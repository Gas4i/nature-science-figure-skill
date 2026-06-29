# 官方依据刷新流程

使用场景：用户要求 latest/current 规则，或最终投稿前需要复核官方规范。

## 触发条件

- 用户明确要求最新 Nature/Science 图件规范。
- 用于 `final_artwork`，且本地来源或 `references/source-links.md` 超过 12 个月未核查。
- 发现 profile 与新的官方页面/PDF 冲突。

## 流程

1. 只使用 Nature、Nature Portfolio、Science、AAAS 官方来源。
2. 打开 `references/source-links.md` 中的入口，必要时从官方页面重新下载 PDF 到本地私有目录。
3. 不要把下载的第三方 PDF、模板或文章图像提交到公开仓库。
4. 记录 URL、检查日期、文件大小、SHA256 和关键规则变化。
5. 更新对应 `profiles/*.yaml`。
6. 更新 `references/journal-profiles.md` 和 `references/source-links.md` 中的规则解释。
7. 如果无法下载或核验正文，只能把 URL 记录为待核验，不得写成已归档证据。

## 冲突处理

- 官方 PDF 优先于第三方博客、教程、模板文章。
- 新官方文件优先于旧官方文件。
- 公开版 skill 只保留摘要和链接；本地私有归档可以用于复核，但不作为公开仓库内容再分发。
