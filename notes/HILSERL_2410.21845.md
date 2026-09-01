# Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement Learning (HIL-SERL)

- **arXiv**: [2410.21845](https://arxiv.org/abs/2410.21845) | **发表**: arXiv 2024（Science Robotics 2025） | **团队**: Jianlan Luo, Charles Xu, Jeffrey Wu, Sergey Levine（UC Berkeley）
- **PDF**: [英文原文](../papers/pdf/HILSERL_2410.21845.pdf) · [中文翻译](../papers/zh/HILSERL_2410.21845_zh.pdf)
- **分类**: TTT 之前的阶段——RL 微调与平滑探索

## 一句话

真机视觉 RL 的系统级配方：演示 + 人类在环纠正 + 高效 off-policy RL（RLPD 系）+ 一系列工程选择，在动态操作、精密装配、双臂协调等任务上 1–2.5 小时内达到近 100% 成功率与快节拍，显著超越模仿学习。

## 方法

1. **人类纠正作为数据**：遥操介入的纠正段直接进 replay，与 RL 目标共同训练。
2. **系统设计**：预训练视觉 backbone、对称采样、集成 critic、安全边界。

## 对本仓库 / 方案的意义

「部署中人类纠正」是 RoboTTT DAgger 蒸馏、ORPA 残差反馈的同一数据源；HIL-SERL 证明这类数据在 RL 框架下能以小时级把策略推到近完美。对 TTT 的启示：把人类接管/纠正信号纳入测试时更新目标（而非只当训练数据），是把 HIL-SERL 从「训练期」推向「部署期」的自然一步。

## 关联阅读

- 纠正蒸馏进快权重：[RoboTTT (2607.15275)](RoboTTT_2607.15275.md)
- 残差式在线纠正：[ORPA (2608.17323)](ORPA_2608.17323.md)
- VLA 版：[ConRFT (2502.05450)](ConRFT_2502.05450.md)
