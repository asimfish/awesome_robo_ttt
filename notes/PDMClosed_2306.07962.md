# Parting with Misconceptions about Learning-based Vehicle Motion Planning (PDM-Closed)

- **arXiv**: [2306.07962](https://arxiv.org/abs/2306.07962) | **发表**: CoRL 2023 | **团队**: Daniel Dauner 等（Tübingen / Bosch，Geiger 组）
- **PDF**: [英文原文](../papers/pdf/PDMClosed_2306.07962.pdf) · [中文翻译](../papers/zh/PDMClosed_2306.07962_zh.pdf)
- **分类**: 免权重 test-time steering（驾驶 verifier 体系）

## 一句话

nuPlan 2023 冠军：15 个候选（3 横向偏移 × 5 IDM 速度）→ 常速度预测下模拟 4 秒 → 按规则指标打分选优 + 2 秒内预测碰撞即紧急制动——全管线 91ms，定义了驾驶「模拟-打分-择优」的字典。

## 方法

1. **候选生成**：中心线 3 个横向偏移 × 5 档 IDM 目标速度 = 15 条 proposal。
2. **前向模拟**：他车常速度外推，自车候选逐条 rollout 4 秒。
3. **打分结构**：乘法硬门（at-fault 碰撞、可行驶区域、行驶方向）× 加权软分（progress、TTC、comfort）。
4. **兜底**：预测 2 秒内碰撞 → 最大制动 fallback。

## 关键结果

- nuPlan 2023 挑战赛冠军；PDM-Closed 91ms / PDM-Open 7ms / Hybrid 96ms。
- 揭穿误区：简单规则基线在闭环中胜过大量学习方法——闭环评测与开环模仿指标脱节。

## 对机器人 TTT 的意义

驾驶 verifier 的原型：后续 Hydra-MDP（蒸馏它）、Centaur（在它的头上做 TTT）、TOAD/Diffusion-ES（拿它当搜索 reward）全部构建在这套打分结构之上。「乘法硬门 × 加权软分 + 紧急制动」的三层结构是任何 test-time 择优系统可以直接照抄的骨架。

## 局限与注意

- 常速度他车预测在交互密集场景失真。
- 规则打分依赖感知输出，感知误差直接污染。

## 关联阅读

- 蒸馏进网络：[Hydra-MDP (2406.06978)](HydraMDP_2406.06978.md)
- 当搜索 reward：[Diffusion-ES (2402.06559)](DiffusionES_2402.06559.md)、[TOAD (2606.07170)](TOAD_2606.07170.md)
