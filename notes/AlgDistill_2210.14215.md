# In-context Reinforcement Learning with Algorithm Distillation (AD)

- **arXiv**: [2210.14215](https://arxiv.org/abs/2210.14215) | **发表**: ICLR 2023 | **团队**: Michael Laskin 等（DeepMind）
- **PDF**: [英文原文](../papers/pdf/AlgDistill_2210.14215.pdf) · [中文翻译](../papers/zh/AlgDistill_2210.14215_zh.pdf)
- **分类**: TTT 新浪潮（免梯度对照）

## 一句话

用 causal transformer 自回归建模 RL 算法的整条**训练历史**（跨 episode），模型学会的不是策略而是「策略改进算子」——部署时纯前向即可在上下文内自我改进，零梯度更新。

## 方法

1. **数据 = 学习历史**：把源 RL 算法在多任务上的完整训练轨迹（从差到好）当序列数据。
2. **跨 episode 上下文**：上下文窗口横跨多个 episode，迫使模型捕捉「回报随经验增长」的规律。
3. **部署**：新任务上模型以自己的交互历史为上下文，行为逐 episode 变好——in-context RL。

## 对机器人 TTT 的意义

「免梯度 TTT」的代表：适应能力被蒸馏进权重，推理时只需前向，延迟最优、零崩溃风险。局限同样清晰——适应上限被预训练时见过的「学习历史分布」封顶，出分布的漂移无法处理。与梯度 TTT 是互补关系：in-context 管快反应，梯度管真学习。RoboTTT 同时利用了两者（fast weights 兼具两种性格）。

## 局限与注意

- 上下文长度限制适应量；任务分布外泛化弱。
- 需要源算法的完整训练历史，数据工程量大。

## 关联阅读

- 机器人系近亲：RMA（[2107.04034](RMA_2107.04034.md)，前馈推断环境隐变量）
- 混合形态：[RoboTTT (2607.15275)](RoboTTT_2607.15275.md)
