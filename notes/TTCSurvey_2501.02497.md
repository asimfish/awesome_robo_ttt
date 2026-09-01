# A Survey of Test-Time Compute: From Intuitive Inference to Deliberate Reasoning

- **arXiv**: [2501.02497](https://arxiv.org/abs/2501.02497) | **发表**: arXiv 2025（综述） | **团队**: 见论文
- **PDF**: [英文原文](../papers/pdf/TTCSurvey_2501.02497.pdf) · [中文翻译](../papers/zh/TTCSurvey_2501.02497_zh.pdf)
- **分类**: TTT 新浪潮（综述/概念地图）

## 一句话

把测试时计算二分为 System-1（参数更新/输入修改 = TTA/TTT）与 System-2（重复采样/自我修正/树搜索 = test-time scaling），给整个领域画了概念地图。

## 核心内容

1. **System-1 分支**：测试时适应（TTA）、测试时训练（TTT）——通过更新参数或修改输入让模型「感知」变准。
2. **System-2 分支**：CoT、self-refine、best-of-N、MCTS——通过更多推理步骤让模型「思考」变深。
3. **两分支的资源观**：同一份测试时算力，花在梯度上还是花在采样上，是贯穿全书的取舍。

## 对机器人 TTT 的意义

本仓库的组织框架与之对应：第 1–4 类（TTA 基础、策略适应、TTT 新浪潮、机器人 TTT）是 System-1；第 5 类（steering/搜索/verifier）是 System-2。机器人系统设计时应显式回答：延迟预算内，梯度和采样各分多少？

## 关联阅读

- System-1 代表：[TTT (1909.13231)](TTT_1909.13231.md)
- System-2 代表：[Snell 2024 (2408.03314)](SnellTTC_2408.03314.md)
- 驾驶域对应综述：[Post-Training Survey (2607.08072)](PostTrainSurvey_2607.08072.md)
