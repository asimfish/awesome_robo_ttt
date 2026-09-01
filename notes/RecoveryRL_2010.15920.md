# Recovery RL: Safe Reinforcement Learning with Learned Recovery Zones

- **arXiv**: [2010.15920](https://arxiv.org/abs/2010.15920) | **发表**: IEEE RA-L 2021 | **团队**: Brijen Thananjeyan*, Ashwin Balakrishna* 等（UC Berkeley）
- **PDF**: [英文原文](../papers/pdf/RecoveryRL_2010.15920.pdf) · [中文翻译](../papers/zh/RecoveryRL_2010.15920_zh.pdf)
- **分类**: 免权重 test-time steering（safety critic / 兜底）

## 一句话

用离线失败数据（含碰撞记录）预训练 safety critic Q_risk 估计「未来违规概率」，部署时超过阈值就切换到恢复策略——失败数据变安全资产的最直接配方。

## 方法

1. **Q_risk 预训练**：把失败 rollout 当正样本，学习状态-动作对导致约束违反的折扣概率。
2. **双策略架构**：任务策略负责性能，恢复策略负责把系统拉回安全区；Q_risk 超阈值即切换。
3. **持续更新**：在线阶段 Q_risk 可继续用新失败数据更新。

## 对机器人 TTT 的意义

TTT/steering 都需要「守门员」：适应出错时谁来兜底？Recovery RL 给出失败数据的三重用法——训 Q_risk 做一票否决硬门、做在线训练期的 safety shield、做 verifier 蒸馏的负样本源。一份失败数据三处复用，是任何测试时适应系统的标配安全组件。

## 局限与注意

- Q_risk 的可靠性取决于失败数据覆盖度，未见过的失败模式仍会漏。
- 恢复策略过度保守会牺牲任务性能（对照 Centaur 的 fallback layer 教训）。

## 关联阅读

- 保守回退的反面教材：[Centaur (2503.11650)](Centaur_2503.11650.md)（fallback 使 progress 86.5→<15）
- critic 抗高估：[IDQL (2304.10573)](IDQL_2304.10573.md)
