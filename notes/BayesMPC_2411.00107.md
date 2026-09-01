# First, Learn What You Don't Know: Active Information Gathering for Driving at the Limits of Handling

- **arXiv**: [2411.00107](https://arxiv.org/abs/2411.00107) | **发表**: arXiv 2024（v2 2025.07） | **团队**: Alexander Davydov, Franck Djeumou, Marcus Greiff 等（Stanford / Toyota Research Institute）
- **PDF**: [英文原文](../papers/pdf/BayesMPC_2411.00107.pdf) · [中文翻译](../papers/zh/BayesMPC_2411.00107_zh.pdf)
- **分类**: 部署时策略适应（重要反例）

## 一句话

贝叶斯 last-layer 元学习车辆动力学 + 主动信息采集 MPC，真车 Toyota Supra 漂移验证；核心结论是个反例——**极限工况下仅靠在线适应不够**，失稳时间常数快于适应收敛速度，必须预先主动探测。

## 方法

1. **贝叶斯末层**：动力学模型末层做贝叶斯线性回归，不确定性显式量化。
2. **主动信息采集**：MPC 目标里加入信息增益项，在进入极限工况**之前**主动激励系统（小幅打滑）以收缩后验。
3. **真车验证**：Supra 漂移，在轮胎摩擦极限处对比被动适应与主动探测。

## 对机器人 TTT 的意义

给所有在线适应方法划了一条硬边界：**当漂移速度 > 适应收敛速度时，TTT 来不及**。紧急避让、湿滑路面恰是最需要适应的时刻，也是适应最可能迟到的时刻。对策不是更快的梯度，而是（1）前馈推断（RMA 式毫秒级）兜底、（2）在还来得及的时候主动采集信息（本文）、（3）结构性安全垫（底层控制器限幅）。

## 局限与注意

- 主动探测本身有安全成本（故意小幅失稳），民用场景接受度存疑。
- 结论针对动力学漂移；感知层慢漂移仍适合梯度 TTA。

## 关联阅读

- 被动适应的正面案例：[ContinualMAML (2409.14950)](ContinualMAML_2409.14950.md)
- 毫秒级兜底：[RMA (2107.04034)](RMA_2107.04034.md)
