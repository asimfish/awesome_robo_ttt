# Consistency Policy: Accelerated Visuomotor Policies via Consistency Distillation

- **arXiv**: [2405.07503](https://arxiv.org/abs/2405.07503) | **发表**: RSS 2024 | **团队**: Aaditya Prasad 等（Stanford）
- **PDF**: [英文原文](../papers/pdf/ConsistencyPolicy_2405.07503.pdf) · [中文翻译](../papers/zh/ConsistencyPolicy_2405.07503_zh.pdf)
- **分类**: 免权重 test-time steering（延迟使能技术）

## 一句话

一致性蒸馏把扩散策略压到 1–3 步去噪：实测 15 步 DDIM 192ms → 单步 21ms（笔记本 GPU），为 test-time 采样与 verifier 腾出延迟预算。

## 方法

1. **CTM 式一致性蒸馏**：学生网络学会从任意噪声水平一步跳到干净动作，教师为预训练扩散策略。
2. **少步微调**：1 步为主，可选 3 步提质。

## 对机器人 TTT 的意义

它本身不做 steering，但决定了 steering 的可行域：省下来的 170ms 可以换成 N=8~32 的批量采样 + verifier 打分 + 若干轮 CEM。任何「best-of-N / 搜索 / guidance」要在 10–50ms 预算内落地，少步蒸馏几乎是前置条件。注意蒸馏也压缩了输出分布的多样性——N 个样本的覆盖度会下降，与 steering 的收益存在张力，需实测权衡。

## 关联阅读

- 需要它的方法：[IDQL (2304.10573)](IDQL_2304.10573.md)、[RoboMonkey (2506.17811)](RoboMonkey_2506.17811.md)
- 类似取舍（流匹配单步）：见 README 趋势节
