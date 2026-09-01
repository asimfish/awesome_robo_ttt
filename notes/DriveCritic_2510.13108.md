# DriveCritic: Towards Context-Aware, Human-Aligned Evaluation for Autonomous Driving with VLMs

- **arXiv**: [2510.13108](https://arxiv.org/abs/2510.13108) | **发表**: arXiv 2025 | **团队**: 见论文
- **PDF**: [英文原文](../papers/pdf/DriveCritic_2510.13108.pdf) · [中文翻译](../papers/zh/DriveCritic_2510.13108_zh.pdf)
- **分类**: 免权重 test-time steering（人类对齐 verifier）

## 一句话

给驾驶 verifier 补上「人类对齐」维度：构建人类偏好标注的轨迹对数据集，用 RLVR 微调 VLM 做成上下文感知的轨迹裁判——成对判断与人类一致率 76%，显著超过规则指标 EPDMS。

## 方法

1. **DriveCritic 数据集**：挑选规则指标与人类判断分歧的场景，人工标注成对轨迹偏好。
2. **VLM 裁判**：视觉+符号上下文输入，推理链后输出偏好，RLVR（可验证奖励 RL）训练。
3. **发现**：EPDMS 等规则分数在上下文敏感场景（礼让、模糊路权）与人类判断系统性背离。

## 对机器人 TTT 的意义

verifier 军备竞赛的「价值观」维度：规则分数只测合规，不测合理。任何以 verifier 为目标的测试时搜索（TOAD/GTRS 系）最终会 hack 到规则与人类判断的缝隙里——DriveCritic 式人类对齐裁判是堵缝的方向。与 RoboMonkey 的合成偏好、VLA-ATTC 的相对比较合流：**偏好式（成对）监督正在取代绝对分数**。

## 局限与注意

- VLM 裁判延迟大，适合离线评测与数据筛选，车载在线需蒸馏。
- 人类偏好本身有噪声与文化差异。

## 关联阅读

- 规则 verifier 的缝隙：[TOAD (2606.07170)](TOAD_2606.07170.md)
- 偏好式同类：[VLA-ATTC (2605.01194)](VLA-ATTC_2605.01194.md)、[RoboMonkey (2506.17811)](RoboMonkey_2506.17811.md)
