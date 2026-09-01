# ConRFT: A Reinforced Fine-tuning Method for VLA Models via Consistency Policy

- **arXiv**: [2502.05450](https://arxiv.org/abs/2502.05450) | **发表**: RSS 2025 | **团队**: Yuhui Chen 等（中科院自动化所）
- **PDF**: [英文原文](../papers/pdf/ConRFT_2502.05450.pdf) · [中文翻译](../papers/zh/ConRFT_2502.05450_zh.pdf)
- **分类**: TTT 之前的阶段——RL 微调与平滑探索

## 一句话

VLA 的「离线 + 在线」两阶段强化微调，统一用一致性策略目标：离线阶段 BC + Q-learning 从少量演示稳定抽取策略与价值；在线阶段一致性策略微调 + 人类干预保证安全探索——八个真机接触密集任务上 45–90 分钟在线微调达 96.3% 平均成功率。

## 方法

1. **一致性策略头**：单步/少步动作生成，兼顾 RL 更新效率与生成式表达力。
2. **统一目标**：离线与在线共享一致性训练目标，避免阶段切换崩溃。
3. **人类在环**：干预段进数据，保证探索安全。

## 对本仓库 / 方案的意义

把 Consistency Policy（本仓库延迟使能技术）与 RL 微调连起来：少步生成式策略既能实时推理，又能高效 RL 更新——这正是「部署期在线更新」需要的策略形态。ConRFT 的 45–90 分钟量级也标定了「训练期 RL」与「测试时 RL（TT-VLA）」之间的成本边界。

## 关联阅读

- 少步蒸馏：[Consistency Policy (2405.07503)](ConsistencyPolicy_2405.07503.md)
- 测试时 RL：[TT-VLA (2601.06748)](TT-VLA_2601.06748.md)
- 系统配方来源：[HIL-SERL (2410.21845)](HILSERL_2410.21845.md)
