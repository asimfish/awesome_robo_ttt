# AnyCar to Anywhere: Learning Universal Dynamics Model for Agile and Adaptive Mobility

- **arXiv**: [2409.15783](https://arxiv.org/abs/2409.15783) | **发表**: ICRA 2025 | **团队**: Wenli Xiao 等（CMU，Guanya Shi 组）
- **PDF**: [英文原文](../papers/pdf/AnyCar_2409.15783.pdf) · [中文翻译](../papers/zh/AnyCar_2409.15783_zh.pdf)
- **分类**: 免梯度上下文适应

## 一句话

Transformer 通用车辆动力学模型：多仿真器/多物理后端生成不同尺寸、质量、地形的车辆数据训练，模型以最近状态-动作历史为上下文推断当前车的动力学，配 MPC 实现敏捷控制；真机在大状态估计误差下仍能适应。

## 方法

1. **数据工厂**：统一多个仿真器，随机化车辆物理与地形。
2. **in-context 动力学**：历史窗口作为上下文，前向推断当前动力学——无梯度。
3. **鲁棒训练 + 真机微调**：注意力掩码/噪声增广抗估计误差。

## 对机器人 TTT 的意义

Neural-Fly 与 RMA 的合流：动力学适应完全 in-context 化，与 MPC 组合直接控到极限工况。对本仓库源头方案的启示——低层跟踪控制器的模型也可以做成 in-context 自适应的，把「适应」在上层策略（TTT）与下层动力学（in-context）之间分工。

## 局限与注意

- 仿真分布外的车辆/地形失效；BayesMPC 的极限工况警告依然适用。

## 关联阅读

- 梯度式动力学适应：[Continual-MAML (2409.14950)](ContinualMAML_2409.14950.md)、[Neural-Fly (2205.06908)](NeuralFly_2205.06908.md)
- 边界反例：[BayesMPC (2411.00107)](BayesMPC_2411.00107.md)
