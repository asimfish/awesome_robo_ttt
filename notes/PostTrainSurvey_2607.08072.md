# Post-Training in End-to-End Autonomous Driving: A Unified View

- **arXiv**: [2607.08072](https://arxiv.org/abs/2607.08072) | **发表**: arXiv 2026（综述） | **团队**: Ruining Yang 等（Northeastern / Purdue）
- **PDF**: [英文原文](../papers/pdf/PostTrainSurvey_2607.08072.pdf) · [中文翻译](../papers/zh/PostTrainSurvey_2607.08072_zh.pdf)
- **分类**: 机器人/驾驶的权重级 TTT（综述/坐标系）

## 一句话

把端到端驾驶的后训练方法统一为四族——蒸馏、偏好对齐、强化学习、测试时精化（test-time refinement），并把测试时精化进一步二分为「改权重的 TTT」与「不改权重的 refinement」。

## 核心内容

1. **四族分类**：
   - 蒸馏（从规则教师/大模型蒸馏，如 Hydra-MDP）；
   - 偏好对齐（人类反馈/偏好数据，如 TrajHF 类）；
   - 强化学习（闭环 RL 微调）；
   - **测试时精化**：部署阶段提升性能的所有手段。
2. **测试时精化的二分法**：
   - **Test-Time Training（改权重）**：Centaur 式在线梯度更新；
   - **Test-Time Refinement（不改权重）**：候选轨迹重排、搜索、引导（TOAD、DriveCritic、Fast-dDrive 等）。
3. **车载延迟是该方向的第一瓶颈**：综述明确指出算力与延迟约束决定了哪些方法能上车。

## 对机器人 TTT 的意义

提供了本仓库第 4、5 两个分类的官方坐标系：权重级 TTT 与免权重 steering 是同一枚硬币的两面，评价维度（延迟、安全认证、性能上限）也由此展开。写论文时的 related work 定位可直接引用其分类学。

## 局限与注意

- 综述性质，对单个方法的技术细节覆盖有限。
- 其中提及的 DriveCritic、Fast-dDrive 等工作细节未在本仓库逐一核实。

## 关联阅读

- 改权重代表：[Centaur (2503.11650)](Centaur_2503.11650.md)
- 不改权重代表：[TOAD (2606.07170)](TOAD_2606.07170.md)、[Hydra-MDP (2406.06978)](HydraMDP_2406.06978.md)
- 更上位的概念地图：[Test-Time Compute Survey (2501.02497)](TTCSurvey_2501.02497.md)
