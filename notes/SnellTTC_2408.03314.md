# Scaling LLM Test-Time Compute Optimally Can Be More Effective than Scaling Model Parameters

- **arXiv**: [2408.03314](https://arxiv.org/abs/2408.03314) | **发表**: arXiv 2024（ICLR 2025） | **团队**: Charlie Snell 等（UC Berkeley / Google DeepMind）
- **PDF**: [英文原文](../papers/pdf/SnellTTC_2408.03314.pdf) · [中文翻译](../papers/zh/SnellTTC_2408.03314_zh.pdf)
- **分类**: TTT 新浪潮（test-time scaling 辨析）

## 一句话

系统研究测试时算力（搜索、修订，不改参数）的最优分配：按题目难度自适应分配预算，效率比 best-of-N 高 4 倍；小模型+测试时算力可胜 14 倍大模型。

## 方法

1. **两条杠杆**：修订链（顺序自我修正）与 verifier 搜索（PRM 引导的并行/树搜索）。
2. **compute-optimal 策略**：难度低用顺序修订、难度高用并行搜索，按预估难度动态分配。

## 对机器人 TTT 的意义

概念辨析的锚点：**test-time scaling 改变输出分布（不改权重），TTT 改权重——两者正交、可叠加**。机器人语境里：best-of-N/搜索/verifier 是 scaling 一族（本仓库第 5 类），梯度更新是 TTT 一族（第 4 类）。其「按难度分配预算」的思想对应机器人按不确定性触发适应（Centaur 的选择性触发）。

## 局限与注意

- 结论依赖可靠 verifier 与难度估计——机器人域两者都比数学题难获得。

## 关联阅读

- 概念地图：[TTC Survey (2501.02497)](TTCSurvey_2501.02497.md)
- 机器人版 scaling law：[RoboMonkey (2506.17811)](RoboMonkey_2506.17811.md)
