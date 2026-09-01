# LocoFormer: Generalist Locomotion via Long-context Adaptation

- **arXiv**: [2509.23745](https://arxiv.org/abs/2509.23745) | **发表**: arXiv 2025（CoRL 2025） | **团队**: 见论文（CMU 系）
- **PDF**: [英文原文](../papers/pdf/LocoFormer_2509.23745.pdf) · [中文翻译](../papers/zh/LocoFormer_2509.23745_zh.pdf)
- **分类**: 免梯度上下文适应

## 一句话

「全身型」通用腿足控制器：不给运动学先验，靠跨 episode 的长上下文 in-context 学习，对未见形态（Go2 轮足/腿足，甚至只用后腿的双足模式）零样本部署、数秒内适应，失败后 few-shot 逐次改进。

## 方法

1. **预训练使 in-context 学习涌现**：跨形态、跨动力学的大规模仿真，上下文跨越多个 episode（含失败经历）。
2. **架构**：长上下文 transformer 策略，适应完全在前向里发生。
3. **两种模式**：零样本（u=0）立即稳定行走；few-shot 利用前几次试验的经验改进。

## 对机器人 TTT 的意义

RMA 的升级形态：RMA 推断低维环境隐变量，LocoFormer 把整段交互历史（含摔倒）放进上下文，适应对象扩展到**形态本身**。它与 Algorithm Distillation 一样属于「适应蒸馏进权重」路线——零梯度、毫秒级，是权重级 TTT 的必要对照与快时间尺度搭档。

## 局限与注意

- 适应上限受预训练形态/动力学分布约束；全新失效模式无法处理。
- 高频控制下上下文长度与延迟的权衡。

## 关联阅读

- 前驱：[RMA (2107.04034)](RMA_2107.04034.md)
- 语言域源头：[Algorithm Distillation (2210.14215)](AlgDistill_2210.14215.md)
- 梯度路线对照：[TTT-Parkour (2602.02331)](TTTParkour_2602.02331.md)
