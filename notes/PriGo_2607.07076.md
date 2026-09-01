# PriGo: Test-Time Primitive Guidance to Diffusion and Flow Policies for Adaptive Robotic Manipulation

- **arXiv**: [2607.07076](https://arxiv.org/abs/2607.07076) | **发表**: arXiv 2026 | **团队**: 见论文
- **PDF**: [英文原文](../papers/pdf/PriGo_2607.07076.pdf) · [中文翻译](../papers/zh/PriGo_2607.07076_zh.pdf)
- **分类**: 免权重 test-time steering

## 一句话

用「动作原语」做测试时引导：轻量 PANet 从观测预测原语分布（抓/推/放…），可微原语引导在推理期把生成动作拉向语义一致的行为——即插即用于预训练扩散/流策略，LIBERO / CALVIN / SIMPLER 与真机上提升鲁棒性与长时程执行。

## 方法

1. **原语预测**：PANet 输出当前应处的原语类别分布，作为高层意图信号。
2. **可微原语引导**：原语一致性损失的梯度注入去噪/流积分过程。
3. **免重训**：基座策略冻结，只训 PANet。

## 对机器人 TTT 的意义

guidance 信号来源的又一种：不是 reward（Diffuser）、不是动力学（DynaGuide）、不是人类交互（ITPS），而是**行为语义结构**。其立论——模仿学习学的是表面动作相关而非意图——与 TT-VLA「重建好≠做得对」同向：测试时引导应对齐任务意图层。

## 局限与注意

- 原语词表需人工定义，跨任务迁移受限。
- 每步去噪加梯度回传，延迟增加。

## 关联阅读

- 引导信号谱系：[Diffuser (2205.09991)](Diffuser_2205.09991.md)、[DynaGuide (2506.13922)](DynaGuide_2506.13922.md)、[ITPS (2411.16627)](ITPS_2411.16627.md)
