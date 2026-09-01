# Reinforcement Learning with Action Chunking (Q-Chunking)

- **arXiv**: [2507.07969](https://arxiv.org/abs/2507.07969) | **发表**: NeurIPS 2025 | **团队**: Qiyang Li, Zhiyuan Zhou, Sergey Levine（UC Berkeley）
- **PDF**: [英文原文](../papers/pdf/QChunking_2507.07969.pdf) · [中文翻译](../papers/zh/QChunking_2507.07969_zh.pdf)
- **分类**: TTT 之前的阶段——RL 微调与平滑探索

## 一句话

把模仿学习里的「动作分块」搬进 TD 类 RL：直接在分块动作空间上跑带行为约束的 actor-critic——(1) 利用离线数据的时间一致行为做更有效的在线探索，(2) 无偏 n 步回传让 TD 学习更稳更快；OGBench / robomimic 长时程稀疏奖励任务上优于 RLPD、Cal-QL、FQL 等最强离线→在线方法。

## 方法

1. **分块 critic 与 actor**：Q(s, a_{t:t+h}) 与 π(a_{t:t+h}|s)，整块为原子动作。
2. **行为约束**：隐式 KL（QC）或 Wasserstein（QC-FQL，基于流匹配策略）锁住离线先验。
3. **探索红利**：分块动作天然时间相关——探索噪声在 chunk 内一致而非逐步白噪。

## 对本仓库 / 方案的意义

Q-Chunking 的探索论断与我们的导数接口发现直接相通：**时间相关（低频）探索优于逐步白噪**——分块靠「整块采样」实现相关性，导数接口靠「积分链」实现相关性，两者可叠加（分块的导数指令）。其 n 步无偏回传也解释了为何分块 RL 在长时程稀疏奖励上更稳，为「分块 + 导数接口 + RL」的组合提供了理论依据。

## 局限与注意

- 分块长度是关键超参：太长丢反应性（见 DREAM-Chunk / DCDP 的 chunk 内修正）。
- 行为约束强度决定离线先验与在线改进的平衡。

## 关联阅读

- 探索噪声频谱：[Pink Noise (ICLR 2023)](PinkNoise_ICLR2023.md)、[gSDE (2005.05719)](gSDE_2005.05719.md)
- chunk 内反应性补丁：[DREAM-Chunk (2606.18589)](DREAMChunk_2606.18589.md)
- 基线：[RLPD (2302.02948)](RLPD_2302.02948.md)、[Cal-QL (2303.05479)](CalQL_2303.05479.md)
