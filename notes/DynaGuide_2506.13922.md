# DynaGuide: Steering Diffusion Policies with Active Dynamic Guidance

- **arXiv**: [2506.13922](https://arxiv.org/abs/2506.13922) | **发表**: NeurIPS 2025 | **团队**: Maximilian Du, Shuran Song（Stanford）
- **PDF**: [英文原文](../papers/pdf/DynaGuide_2506.13922.pdf) · [中文翻译](../papers/zh/DynaGuide_2506.13922_zh.pdf)
- **分类**: 免权重 test-time steering（外挂动力学引导）

## 一句话

外挂一个潜空间动力学模型预测「当前观测+候选动作 → 未来结果」，用与期望/规避结果的嵌入距离做可微 guidance 注入去噪——可引导任何现成扩散策略，无需重训基座。

## 方法

1. **潜动力学模型**：独立训练，输入观测与动作 chunk，输出未来状态嵌入。
2. **目标距离 guidance**：期望结果（目标状态嵌入）拉近、规避结果（失败状态嵌入）推远，梯度注入去噪中期。
3. **基座无关**：guidance 只依赖外挂模型，基座扩散策略保持黑盒冻结。

## 对机器人 TTT 的意义

展示了 guidance 的正确打开方式：可微信号来自**专门训练的外挂模型**（对含噪输入鲁棒），而不是直接拿任务 reward 硬求导。「规避结果嵌入」给失败数据又一个用法——把失败时刻的状态嵌入当负极，测试时主动绕开。与 DSRL 相比：DynaGuide 每步去噪都要梯度回传（慢），但不需要在线 RL 训练。

## 局限与注意

- 动力学模型的预测误差直接变成引导偏差。
- 去噪步数多时延迟累积，需配少步蒸馏。

## 关联阅读

- 框架源头：[Diffuser (2205.09991)](Diffuser_2205.09991.md)
- 竞品（学噪声不加梯度）：[DSRL (2506.15799)](DSRL_2506.15799.md)
