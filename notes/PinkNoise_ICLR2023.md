# Pink Noise Is All You Need: Colored Noise Exploration in Deep Reinforcement Learning

- **论文**: [OpenReview (ICLR 2023 Oral/Spotlight)](https://openreview.net/forum?id=hQ9V5QN27eS) · [作者主页 PDF](https://onnoeberhard.com/bib/eberhard-2023-pink/doc.pdf) | **团队**: Onno Eberhard, Jakob Hollenstein, Cristina Pinneri, Georg Martius（MPI-IS Tübingen）
- **PDF**: [英文原文](../papers/pdf/PinkNoise_ICLR2023.pdf) · [中文翻译](../papers/zh/PinkNoise_ICLR2023_zh.pdf)
- **分类**: TTT 之前的阶段——RL 微调与平滑探索

## 一句话

把探索噪声统一到「有色噪声」家族（功率谱 ∝ 1/f^β）：白噪声 β=0、OU/布朗红噪声 β=2；在 MPO/SAC 上系统评测发现 **β=1 的粉噪声**在广泛环境上显著优于白噪、OU 与其他替代——建议作为连续控制的默认动作噪声。

## 方法与发现

1. **频谱视角**：噪声「颜色」决定探索的时间相关性；红噪覆盖远、白噪覆盖局部，粉噪兼顾。
2. **实证**：20 个随机种子、多环境，粉噪一致最优或并列最优。
3. **开源包** `pink-noise-rl`。

## 对本仓库 / 方案的意义

给 CADI 提供最直接的理论坐标：**导数接口 + 积分链本质是把上游白噪声「染红」**（积分一次 β+2）。纯积分器把白噪变成红噪（无界随机游走，对应 Arm C 崩溃），泄漏积分器把颜色拉回中间（对应 E3 恢复）——泄漏系数就是我们的「噪声颜色旋钮」，粉噪最优的结论预示了最优泄漏系数的存在。这一对应关系可写成方案的理论支撑段。

## 局限与注意

- 结论基于 off-policy（SAC/MPO）；on-policy PPO 上的有色噪声见后续工作（arXiv:2312.11091）。

## 关联阅读

- 状态依赖平滑：[gSDE (2005.05719)](gSDE_2005.05719.md)
- 分块相关性：[Q-Chunking (2507.07969)](QChunking_2507.07969.md)
- 扩散策略的结构化探索：[DPPO (2409.00588)](DPPO_2409.00588.md)
