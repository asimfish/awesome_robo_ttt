# DayDreamer: World Models for Physical Robot Learning

- **arXiv**: [2206.14176](https://arxiv.org/abs/2206.14176) | **发表**: CoRL 2022 | **团队**: Philipp Wu, Alejandro Escontrela, Danijar Hafner, Pieter Abbeel, Ken Goldberg（UC Berkeley）
- **PDF**: [英文原文](../papers/pdf/DayDreamer_2206.14176.pdf) · [中文翻译](../papers/zh/DayDreamer_2206.14176_zh.pdf)
- **分类**: 部署时策略适应（在线世界模型学习）

## 一句话

Dreamer 直接在真机上在线学习：四足从零 1 小时学会翻身站立行走、10 分钟内适应被推倒；机械臂视觉抓放、轮式导航——无仿真、无 reset 工程，世界模型在部署中持续更新并在想象中训练策略。

## 方法

1. **在线世界模型**：真机交互数据实时更新 RSSM 世界模型。
2. **想象中训练**：策略在世界模型的想象 rollout 里学习，样本效率远超无模型 RL。
3. **持续适应**：训练不停，环境变化（被推倒）后快速恢复。

## 对机器人 TTT 的意义

「测试时训练」在机器人上最早的完整实例之一——只是当年不叫这个名字：部署 = 训练，世界模型是持续适应的载体。今天的 AdaWorldPolicy / DREAM-Chunk / MPA 把世界模型用作测试时基础设施，DayDreamer 是这条线的起点。也是「在线学习需要 1 小时」的成本标尺——TTT 层路线追求的正是把这种适应压进前向。

## 局限与注意

- 真机在线试错有安全成本，适用于可摔倒、可重试的平台。
- 学习时间以小时计，非帧级。

## 关联阅读

- 世界模型做测试时匹配：[DREAM-Chunk (2606.18589)](DREAMChunk_2606.18589.md)
- 段级重建再训练：[TTT-Parkour (2602.02331)](TTTParkour_2602.02331.md)
