# Learning to Adapt in Dynamic, Real-World Environments Through Meta-Reinforcement Learning (GrBAL / ReBAL)

- **arXiv**: [1803.11347](https://arxiv.org/abs/1803.11347) | **发表**: ICLR 2019 | **团队**: Anusha Nagabandi, Ignasi Clavera 等（UC Berkeley）
- **PDF**: [英文原文](../papers/pdf/GrBAL_1803.11347.pdf) · [中文翻译](../papers/zh/GrBAL_1803.11347_zh.pdf)
- **分类**: 部署时策略适应

## 一句话

模型基元强化学习做在线适应：元训练动力学模型使其能用最近 M 步经验一次梯度（GrBAL）或循环网络隐状态（ReBAL）快速适应；真机六足在断腿、滑面、斜坡上毫秒级重规划，样本效率高 1.5–3 个量级。

## 方法

1. **在线适应的元目标**：用过去 M 步适应、预测未来 K 步——训练时就模拟部署时的滑窗适应。
2. **两种适应器**：梯度式（GrBAL，MAML 内环）vs 循环式（ReBAL，隐状态即适应）。
3. **MPC 闭环**：适应后的模型供 MPC 规划。

## 对机器人 TTT 的意义

这是「梯度适应 vs 隐状态适应」的最早正面对比——正是今天 TTT 层（梯度写入快权重）与 in-context（隐状态）两条路线的雏形；结论是两者各有胜场，梯度式在分布外更稳。真机断腿实验也是「在线适应处理硬件故障」的经典证据。

## 关联阅读

- 元学习基石：[MAML (1703.03400)](MAML_1703.03400.md)
- 非平稳扩展：[MOLe (1812.07671)](MOLe_1812.07671.md)
- 现代对应：[TTT-Layers (2407.04620)](TTTLayers_2407.04620.md) vs [LocoFormer (2509.23745)](LocoFormer_2509.23745.md)
