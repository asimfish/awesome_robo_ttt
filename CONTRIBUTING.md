# Contributing / 贡献指南

欢迎补充论文、修正错误、改进笔记。

## 添加一篇论文

1. **登记**：在 `scripts/papers.tsv` 追加一行（Tab 分隔）：`key<TAB>arxiv_id<TAB>category<TAB>venue<TAB>title`
   - `key` 用短驼峰/缩写，不含空格（如 `RoboTTT`）；非 arXiv 论文的 `arxiv_id` 填 venue 标识并在 `scripts/download_pdfs.sh` 里加 URL 映射。
   - `category` 取值：`1-foundations` / `2-policy-adaptation` / `3-new-wave` / `4-robot-driving-ttt` / `5-test-time-steering` / `6-frontier` / `7-in-context` / `8-failure-detection` / `9-rl-before-ttt`。
2. **下载**：`./scripts/download_pdfs.sh`（幂等，只补缺失）；用 `pdftotext -l 1` 核对标题。
3. **翻译**（可选）：参照 `scripts/translate_batch3.sh` 用 [SuperTranslate](https://github.com/asimfish/super_translate) 生成 `papers/zh/<key>_<arxiv>_zh.pdf`。
4. **精读笔记**：在 `notes/<key>_<arxiv>.md` 按现有模板写：基本信息 → 一句话 → 方法 → 关键结果 → 对机器人 TTT 的意义 → 局限 → 关联阅读。
5. **索引**：在 `README.md` 对应分类下按格式追加条目 —— `**标题.** venue 年份. [paper] [pdf] [中译] [解读]` + 作者行；同时更新 `notes/README.md`。
6. **BibTeX**：运行 `./scripts/make_bibtex.sh` 重新生成 `awesome_robo_ttt.bib`。

## 质量要求

- venue 以论文页/官方 proceedings 为准，预印本写 `arXiv YYYY`；不确定的加「（venue 存疑）」。
- 笔记中的数字必须能在原文找到；不确定的标「[存疑]」。
- 提交前运行链接检查（README 中所有相对链接必须可解析）。
- 提交信息格式：`[scope/op]: title`（如 `[papers/feat]: add XXX`）。

## 报告

`report/robo_ttt_report.html`（自包含幻灯片）与 `report/robo_ttt_report.tex`（xelatex + Hiragino Sans GB）为汇总报告源文件；改动分类/篇数时请同步更新。
