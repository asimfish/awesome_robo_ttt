# RoboMonkey: Scaling Test-Time Sampling and Verification for VLA Models

- **arXiv**: [2506.17811](https://arxiv.org/abs/2506.17811) | **发表**: CoRL 2025（PMLR 305:3200-3217） | **团队**: Jacky Kwok 等（Stanford，Pavone/Mirhoseini 组）
- **PDF**: [英文原文](../papers/pdf/RoboMonkey_2506.17811.pdf) · [中文翻译](../papers/zh/RoboMonkey_2506.17811_zh.pdf)
- **分类**: 免权重 test-time steering（采样 + verifier）

## 一句话

VLA 采 N 个动作 → 高斯拟合+扰动采样 → 7B VLM verifier 择优；实证动作误差随采样数呈**指数幂律下降**——机器人版的 test-time scaling law，并给出合成偏好数据训 verifier 的完整管线。

## 方法

1. **采样策略**：VLA 采多个动作后拟合高斯再扰动采样，兼顾多样性与合理性。
2. **VLM verifier**：微调 7B 视觉语言模型对 (观测, 候选动作) 打分；用 SGLang 服务化。
3. **Verifier 数据工厂**：无人工标注——用仿真回放自动构造偏好对，verifier 精度随合成数据规模单调提升。

## 关键结果

- 动作误差 ~ N 的幂律：N=1→16 收益最大，之后边际急剧递减。
- 跨模拟与真机任务一致提升，即插即用于不同 VLA。

## 对机器人 TTT 的意义

回答了「N 取多少」这个所有 best-of-N 方法都要回答的问题：N=8~32 就吃掉绝大部分收益，不必堆大 N。verifier 合成数据管线也是可迁移资产。但 7B VLM 的打分延迟决定了它适合准静态操作，高频控制场景需要把 verifier 蒸馏小（参照 Hydra-MDP 路径）。

## 局限与注意

- verifier 延迟高（大模型前向），车载/高频场景不可行。
- 合成偏好的分布偏差会传导进 verifier。

## 关联阅读

- verifier 零延迟化：[Hydra-MDP (2406.06978)](HydraMDP_2406.06978.md)
- scaling law 的语言域源头：[Snell 2024 (2408.03314)](SnellTTC_2408.03314.md)
