# SafeDiffuser: Safe Planning with Diffusion Probabilistic Models

- **arXiv**: [2306.00148](https://arxiv.org/abs/2306.00148) | **发表**: ICLR 2025（2023 首发） | **团队**: Wei Xiao 等（MIT，Rus 组）
- **PDF**: [英文原文](../papers/pdf/SafeDiffuser_2306.00148.pdf) · [中文翻译](../papers/zh/SafeDiffuser_2306.00148_zh.pdf)
- **分类**: 免权重 test-time steering（guidance / 硬约束）

## 一句话

把控制屏障函数（CBF）嵌入每步去噪（每步解一个 QP），提出 finite-time diffusion invariance，让扩散规划的输出在生成过程结束时落入安全集——guidance 的「硬约束」版本。

## 方法

1. **每步 QP 投影**：去噪的每一步把中间轨迹投影到 CBF 定义的安全集方向，QP 求最小修正。
2. **有限时间不变性**：证明在去噪步数内轨迹收敛进安全集（注意：前提假设见下）。

## 对机器人 TTT 的意义

代表了 steering 光谱的「最强承诺」端：不是软引导而是声称硬保证。对安全关键场景（驾驶、人机共存）有吸引力，但后续工作（Safe Flow Matching, arXiv:2504.08661）指出其保证实际是**概率性的**——初始噪声必然在安全集外，违反其不变性前提。教训：不要在论文里轻易宣称 test-time guidance 带来硬安全保证。

## 局限与注意

- 每步 QP 在去噪步数多时延迟不可忽略。
- 「保证」依赖对约束集与动力学的精确建模。

## 关联阅读

- 软引导对照：[CTG (2210.17366)](CTG_2210.17366.md)
- 兜底机制的另一种做法：[Recovery RL (2010.15920)](RecoveryRL_2010.15920.md)
