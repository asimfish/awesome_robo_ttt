# TTT-VLA: Test-Time Latent Prompt Optimization for VLA Models

- **arXiv**: [2606.03127](https://arxiv.org/abs/2606.03127) | **发表**: arXiv 2026 | **团队**: 见论文
- **PDF**: [英文原文](../papers/pdf/TTTVLA-LPO_2606.03127.pdf) · [中文翻译](../papers/zh/TTTVLA-LPO_2606.03127_zh.pdf)
- **分类**: 2025-2026 前沿

## 一句话

把 TTT 的适应对象缩小到一个**潜提示向量 z**：训练时用 state grounding 代理任务学出「提示接口」，测试时只优化 z、策略主干完全冻结——「适应接口化」的代表作。

## 方法

1. **训练期**：潜提示 z 作为额外条件输入与策略联合训练；state grounding 代理任务（流匹配式预测末端位姿/夹爪状态）让 z 捕捉空间相关信息。
2. **测试期**：在当前环境收集交互数据，只用代理任务的自监督信号优化 z；策略权重不动。
3. **发现**：收益主要来自「关键决策转向」（critical decision steering）——少数关键步的修正，而非全局行为改变。

## 关键结果

- SimplerEnv 单具身（WidowX/Google Robot）与多具身（九具身 BridgeData V2 训练）设定下一致提升。

## 对机器人 TTT 的意义

「适应参数越少越安全」谱系的新端点：全模型 → BN 仿射（TENT）→ 末层（Neural-Fly）→ score decoder（Centaur）→ LoRA（ARC-TTT）→ **单个潜提示向量**。接口化的好处：审计面最小、回滚 trivial（重置 z）、不碰安全认证过的主干。「关键决策转向」的发现也重要——TTT 的价值可能集中在少数分叉点，支持触发式而非常开式适应。

## 局限与注意

- z 的容量有限，大幅域漂移（新任务语义）超出提示接口的表达范围。
- state grounding 代理需要本体状态监督，跨具身时标定成本存在。

## 关联阅读

- 可靠性增强版：[VANE (2608.09448)](VANE_2608.09448.md)
- 接口化同族：[DSRL (2506.15799)](DSRL_2506.15799.md)（噪声接口）
