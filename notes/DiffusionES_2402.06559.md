# Diffusion-ES: Gradient-free Planning with Diffusion for Autonomous Driving

- **arXiv**: [2402.06559](https://arxiv.org/abs/2402.06559) | **发表**: CVPR 2024 | **团队**: Brian Yang 等（CMU，Fragkiadaki 组）
- **PDF**: [英文原文](../papers/pdf/DiffusionES_2402.06559.pdf) · [中文翻译](../papers/zh/DiffusionES_2402.06559_zh.pdf)
- **分类**: 免权重 test-time steering（进化搜索）

## 一句话

进化搜索 × 扩散先验：采轨迹 → 黑盒 PDM reward 打分 → 高分个体用「截断加噪-去噪」变异（保持在数据流形上），nuPlan 闭环追平规则冠军 PDM-Closed——证明不可微 reward 也能引导扩散策略。

## 方法

1. **截断扩散变异**：对精英轨迹加部分噪声再去噪，得到「流形内」的邻域变体——比高斯扰动更不容易产生物理不可行轨迹。
2. **黑盒 reward**：驾驶规则打分（碰撞/舒适/进度）无需可微，直接当适应度。
3. **关键论断**：reward-gradient guidance 需要「对含噪样本也准」的打分器，而这在驾驶规则上不成立——黑盒搜索绕开了这个根本限制。

## 关键结果

- nuPlan 闭环与 PDM-Closed 持平（学习方法首次），零样本跟随语言指令（LLM 生成 reward 函数）。
- 计算量大：population 128 × 100 步去噪 × 多轮进化，秒级延迟，非实时。

## 对机器人 TTT 的意义

在「guidance vs 搜索」的选择上给出清晰依据：驾驶/机器人 reward 大多不可微、不平滑，黑盒搜索（截断扩散变异 + 规则打分）比强行做梯度引导更稳。其流形内变异技巧被 TOAD 等后续工作以更轻量的形式（CEM + warm-start）继承。

## 局限与注意

- 延迟远超车载预算，需大幅裁剪（小 population、少轮次）才可能上线。
- 搜索会主动利用 scorer 盲区（Goodhart），需限制搜索半径。

## 关联阅读

- 轻量后继：[TOAD (2606.07170)](TOAD_2606.07170.md)
- reward 来源：[PDM-Closed (2306.07962)](PDMClosed_2306.07962.md)
