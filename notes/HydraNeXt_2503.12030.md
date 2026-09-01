# Hydra-NeXt: Robust Closed-Loop Driving with Open-Loop Training

- **arXiv**: [2503.12030](https://arxiv.org/abs/2503.12030) | **发表**: ICCV 2025 | **团队**: Zhenxin Li, Shihao Wang, Shiyi Lan, Zhiding Yu, Zuxuan Wu, Jose M. Alvarez（NVIDIA / 复旦）
- **PDF**: [英文原文](../papers/pdf/HydraNeXt_2503.12030.pdf) · [中文翻译](../papers/zh/HydraNeXt_2503.12030_zh.pdf)
- **分类**: 免权重 test-time steering（推理时精化）

## 一句话

用「多分支 + 推理时精化」弥合开环训练与闭环部署的鸿沟：轨迹分支管长时规划、控制分支管短时快反应、精化网络在推理时按运动学约束修正决策——Bench2Drive 65.89 DS（超前 SOTA 22.98）。

## 方法

1. **三分支**：轨迹预测（一般规划）+ 控制预测（短期动作，快反应）+ 轨迹精化网络。
2. **推理时精化**：扩散策略产生候选 + 集成 + 最近邻匹配投影到运动学可行集。
3. **开环训练、闭环收益**：全程无需专家在环的数据采集。

## 对机器人 TTT 的意义

「测试时精化」在反应式闭环基准（Bench2Drive/CARLA）上的强证据——注意与 Centaur（非反应式 NAVSIM）的评测差异。其「长时轨迹 + 短时控制」双时间尺度分支与本仓库洞见 B（三时间尺度分工）互为印证：闭环鲁棒性来自架构里显式的快慢分工，而非单一头的容量。

## 局限与注意

- 精化是固定规则（运动学投影）+集成，不含学习型 verifier；与 GTRS/TOAD 的可学习打分互补。
- 仍依赖开环模仿信号，因果混淆问题未根除。

## 关联阅读

- 同团队 scorer 路线：[Hydra-MDP (2406.06978)](HydraMDP_2406.06978.md)、[GTRS (2506.06664)](GTRS_2506.06664.md)
- 闭环 vs 开环评测的立论：[PDM-Closed (2306.07962)](PDMClosed_2306.07962.md)
