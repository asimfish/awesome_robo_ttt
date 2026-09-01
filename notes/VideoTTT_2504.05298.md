# One-Minute Video Generation with Test-Time Training (Video-TTT)

- **arXiv**: [2504.05298](https://arxiv.org/abs/2504.05298) | **发表**: CVPR 2025 | **团队**: Karan Dalal 等（Stanford / UCSD / UC Berkeley / NVIDIA，Yu Sun 团队）
- **PDF**: [英文原文](../papers/pdf/VideoTTT_2504.05298.pdf) · [中文翻译](../papers/zh/VideoTTT_2504.05298_zh.pdf)
- **分类**: TTT 新浪潮

## 一句话

在预训练视频 DiT（CogVideoX-5B）中后插 TTT-MLP 层负责全局长上下文（局部注意力保留），生成 63 秒连贯多场景动画，人评超 Mamba2 / Gated DeltaNet 等基线 34 Elo。

## 方法

1. **后插 TTT 层**：冻结大部分预训练权重，只训新插入的 TTT-MLP 层与门控——TTT 层可以「加装」进已训好的模型。
2. **分工**：局部自注意力管 3 秒片段内细节，TTT 层管跨片段的全局叙事一致性。
3. **工程**：针对 TTT-MLP 写了专用 on-chip 内核缓解 I/O 瓶颈。

## 对机器人 TTT 的意义

「后插改造」证明：不必从头预训练，就能给现成大模型（类比：已训好的 DP/VLA）加装 TTT 记忆——这大幅降低机器人团队采用 TTT 层的门槛。视频的「跨场景一致性」与机器人的「跨片段任务上下文」是同构问题。

## 局限与注意

- 只在 5B 视频模型 + 卡通域验证；长上下文里 TTT-MLP 的训练稳定性仍需大量工程。
- 推理虽然线性，但绝对成本仍高于纯局部注意力。

## 关联阅读

- 层的定义：[TTT-Layers (2407.04620)](TTTLayers_2407.04620.md)
- 机器人平移：[WAM-TTT (2607.06988)](WAMTTT_2607.06988.md)（视频预测喂快权重）
