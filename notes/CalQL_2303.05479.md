# Cal-QL: Calibrated Offline RL Pre-Training for Efficient Online Fine-Tuning

- **arXiv**: [2303.05479](https://arxiv.org/abs/2303.05479) | **发表**: NeurIPS 2023 | **团队**: Mitsuhiko Nakamoto, Yuexiang Zhai 等（UC Berkeley）
- **PDF**: [英文原文](../papers/pdf/CalQL_2303.05479.pdf) · [中文翻译](../papers/zh/CalQL_2303.05479_zh.pdf)
- **分类**: TTT 之前的阶段——RL 微调与平滑探索

## 一句话

诊断离线→在线「先崩再涨」（unlearning）的根因：保守离线 RL 把 Q 值压得比真实回报还低，在线一开始 Q 被强行拉高、策略被错误更新。Cal-QL 用一行改动——把 Q 校准为不低于参考策略（行为策略）的真实值——消除初期崩溃，在线微调更快更稳。

## 方法

1. **校准下界**：CQL 的保守正则只惩罚「高于行为策略回报」的那部分 Q。
2. **零额外成本**：不改算法结构。

## 对本仓库 / 方案的意义

本仓库源头问题——「on-policy 初期为什么容易学崩」——Cal-QL 给出价值侧的答案（Q 尺度失配），我们给出动作侧的答案（探索噪声被接口放大）。两个机制正交，可叠加验证：校准价值 + 滤波接口 = 最稳的启动。

## 关联阅读

- 极简对照：[RLPD (2302.02948)](RLPD_2302.02948.md)
- 温启动理论：[WSRL (2412.07762)](WSRL_2412.07762.md)
