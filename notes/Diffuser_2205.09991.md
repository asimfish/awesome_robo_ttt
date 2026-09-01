# Planning with Diffusion for Flexible Behavior Synthesis (Diffuser)

- **arXiv**: [2205.09991](https://arxiv.org/abs/2205.09991) | **发表**: ICML 2022 | **团队**: Michael Janner*, Yilun Du*（UC Berkeley / MIT，Levine 组）
- **PDF**: [英文原文](../papers/pdf/Diffuser_2205.09991.pdf) · [中文翻译](../papers/zh/Diffuser_2205.09991_zh.pdf)
- **分类**: 免权重 test-time steering（guidance 经典）

## 一句话

把整条轨迹当成扩散模型的生成对象，「采样即规划」：测试时用外挂 reward/价值模型的梯度做 classifier guidance，同一个模型换个引导函数就换了任务。

## 解决什么问题

传统模型基规划（learned dynamics + 搜索）误差随 horizon 累积，且规划器和模型目标割裂。能否把「建模」和「规划」合成一步？

## 方法

1. **轨迹级扩散**：对 (状态,动作) 序列整体去噪生成，天然满足动力学一致性与时间平滑。
2. **Classifier guidance**：训练一个 reward/价值预测器 J(τ)，采样时在每步去噪上叠加 ∇J 梯度，把样本推向高回报区域。
3. **测试时可组合**：目标条件、约束、奖励都能以 guidance 形式在推理时注入，无需重训。

## 对机器人 TTT 的意义

一切「不改权重、改采样过程」的 test-time steering 的理论源头。它确立了核心抽象：预训练生成模型 = 行为先验，测试时目标 = 外挂引导信号，两者解耦。后续 CTG（STL 规则）、DynaGuide（动力学引导）、SafeDiffuser（CBF 硬约束）都是这个框架的实例化。

## 局限与注意

- 需要「对含噪轨迹也准」的可微 J——这正是后来 Diffusion-ES 指出的根本限制。
- 逐条轨迹去噪+梯度回传，延迟对实时控制偏高。

## 关联阅读

- 驾驶规则版：[CTG (2210.17366)](CTG_2210.17366.md)
- 硬约束版：[SafeDiffuser (2306.00148)](SafeDiffuser_2306.00148.md)
- 黑盒替代：[Diffusion-ES (2402.06559)](DiffusionES_2402.06559.md)
