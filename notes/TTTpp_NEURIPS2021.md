# TTT++: When Does Self-Supervised Test-Time Training Fail or Thrive?

- **论文**: [NeurIPS 2021 Proceedings](https://proceedings.neurips.cc/paper/2021/file/b618c3210e934362ac261db280128c22-Paper.pdf) | **团队**: Yuejiang Liu 等（EPFL）
- **PDF**: [英文原文](../papers/pdf/TTTpp_NEURIPS2021.pdf) · [中文翻译](../papers/zh/TTTpp_NEURIPS2021_zh.pdf)
- **分类**: TTA/TTT 基础

## 一句话

回答「TTT 何时有效」：理论下界表明收益随自监督任务与主任务的**相关性**增大而增大；据此提出对比学习 + 在线特征对齐的 TTT++。

## 方法

1. **理论**：主任务风险的改善量由 SSL 任务梯度与主任务梯度的对齐程度下界控制——相关性低时适应梯度只是噪声。
2. **TTT++**：对比学习做 SSL 任务 + 用训练集统计量做在线特征分布对齐（防漂移）。

## 对机器人 TTT 的意义

「自监督目标怎么选」的第一性原理：**任务相关性高于一切**。它解释了 PAD 的消融（控制任务 IDM 赢、导航任务旋转赢）、TT-VLA 的批评（重建与操作无关）、Centaur 的选择（决策置信度目标直接挂在规划头上）。机器人系统选 TTT 目标时的检查清单第一条。

## 关联阅读

- 经验对应：[PAD (2007.04309)](PAD_2007.04309.md)
- 现代反例：[TT-VLA (2601.06748)](TT-VLA_2601.06748.md)
