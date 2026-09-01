# Test-Time Training with Masked Autoencoders (TTT-MAE)

- **arXiv**: [2209.07522](https://arxiv.org/abs/2209.07522) | **发表**: NeurIPS 2022 | **团队**: Yossi Gandelsman*, Yu Sun* 等（UC Berkeley / Meta）
- **PDF**: [英文原文](../papers/pdf/TTT-MAE_2209.07522.pdf) · [中文翻译](../papers/zh/TTT-MAE_2209.07522_zh.pdf)
- **分类**: TTA/TTT 基础

## 一句话

把 TTT 的自监督任务换成 MAE 重建（mask 75%）：每个测试样本约 20 步 SGD，跨四个基准大幅超越旋转预测版，并给出 bias-variance 理论解释 TTT 何时有益。

## 方法

1. **重建代理任务**：MAE 掩码重建的梯度信息量远大于 4 类旋转分类。
2. **每样本重训**：从同一初始化出发对每个样本独立适应（非 online），20 步梯度。
3. **理论**：TTT 在「测试分布靠近训练分布的样本上牺牲一点 bias，换取 OOD 样本上的大幅 variance 降低」。

## 对机器人 TTT 的意义

确立「重建类目标是 TTT 的强代理任务」——WAM-TTT 的视频预测、RoboTTT 的观测-动作流重建都是它的时序推广。同时它的成本（20 步/样本）标出了裸 TTT 的延迟上限，倒逼后来的结构化路线（TTT 层把 20 步摊平进前向）。

## 局限与注意

- 20 步/样本对实时控制完全不可行。
- TT-VLA 的警告适用：重建得好 ≠ 控制得好，操作任务上重建目标与任务需求可能错位。

## 关联阅读

- 时序推广：[WAM-TTT (2607.06988)](WAMTTT_2607.06988.md)
- 目标错位批评：[TT-VLA (2601.06748)](TT-VLA_2601.06748.md)
