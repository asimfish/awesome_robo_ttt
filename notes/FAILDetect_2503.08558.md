# Can We Detect Failures Without Failure Data? Uncertainty-Aware Runtime Failure Detection for Imitation Learning Policies (FAIL-Detect)

- **arXiv**: [2503.08558](https://arxiv.org/abs/2503.08558) | **发表**: arXiv 2025（RSS 2025） | **团队**: Chen Xu 等（Toyota Research Institute / Columbia）
- **PDF**: [英文原文](../papers/pdf/FAILDetect_2503.08558.pdf) · [中文翻译](../papers/zh/FAILDetect_2503.08558_zh.pdf)
- **分类**: 失败检测与适应触发

## 一句话

只用成功数据就能检测失败：把问题建模为序列 OOD 检测——先把策略输入/输出蒸馏成与失败相关、承载认知不确定性的标量信号（含新提出的流式密度估计器），再用共形预测给出带统计保证的时间变化阈值。

## 方法

1. **两阶段**：信号学习（学习型/后验型标量，如观测-动作对的流式密度、扩散重建误差）→ 共形预测校准动态阈值。
2. **无需失败数据**：训练只用成功演示，失败=偏离成功分布。
3. **实证**：学习型信号（尤其流式密度）最稳定；检测更准更快于 SOTA。

## 对机器人 TTT 的意义

解决了触发器设计的数据困境——真实失败数据稀缺且模式不可预知。「成功分布密度 + 共形阈值」给 TTT 系统一个**有统计保证的适应开关**：密度掉出阈值 → 启动适应/回退。共形预测的引入也回应了 TTA 领域的老问题（TENT/SAR 的阈值多为手调）。

## 局限与注意

- OOD ≠ 失败（新但成功的情形会误报），是 SAFE 指出的方法学缺口。
- 密度估计的表征质量决定一切。

## 关联阅读

- 两类失败的分工：[Sentinel (2410.04640)](Sentinel_2410.04640.md)
- 有监督对照：[SAFE (2506.09937)](SAFE_2506.09937.md)
- 不确定性触发的 TTT 实例：[VLA-ATTC (2605.01194)](VLA-ATTC_2605.01194.md)
