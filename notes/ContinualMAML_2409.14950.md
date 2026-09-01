# Online Adaptation of Learned Vehicle Dynamics Model with Meta-Learning Approach

- **arXiv**: [2409.14950](https://arxiv.org/abs/2409.14950) | **发表**: IROS 2024 | **团队**: Yuki Tsuchiya, Thomas Balch, Paul Drews, Guy Rosman（Toyota Research Institute）
- **PDF**: [英文原文](../papers/pdf/ContinualMAML_2409.14950.pdf) · [中文翻译](../papers/zh/ContinualMAML_2409.14950_zh.pdf)
- **分类**: 部署时策略适应（车辆动力学在线适应）

## 一句话

用 Continual-MAML 在线适应学习型车辆动力学模型并接 MPPI 控制：元学习初始化 + 持续在线更新，应对轮胎磨损、路面变化等缓变漂移。

## 方法

1. **元训练**：跨路面/负载条件的动力学数据上 MAML 训练，得到「几步梯度就能适应」的初始化。
2. **在线阶段**：滑动窗口数据持续做小步梯度；检测到分布切换时可回退到元初始化（continual 机制防遗忘）。
3. **控制闭环**：适应后的模型直接供 MPPI 采样评估。

## 对机器人 TTT 的意义

把「元训练 + 在线适应」落到车辆动力学这一工业相关问题上，验证了缓变漂移（磨损、温度）场景的有效性——与 BayesMPC 的快变漂移反例（失稳边缘来不及适应）合起来，给出在线适应适用边界的完整拼图：**慢漂移用梯度适应，快突变靠前馈推断或预先主动探测**。

## 局限与注意

- 适应速度与漂移速度的竞争关系未在极限工况验证（见 BayesMPC 反例）。
- 动力学适应 ≠ 策略适应：感知-决策层漂移不在其覆盖内。

## 关联阅读

- 反例（快变场景）：[BayesMPC (2411.00107)](BayesMPC_2411.00107.md)
- 元训练必要性源头：[MOLe (1812.07671)](MOLe_1812.07671.md)
