# Hydra-MDP: End-to-end Multimodal Planning with Multi-target Hydra-Distillation

- **arXiv**: [2406.06978](https://arxiv.org/abs/2406.06978) | **发表**: CVPR 2024 E2E 挑战赛冠军（技术报告） | **团队**: NVIDIA（NVlabs）
- **PDF**: [英文原文](../papers/pdf/HydraMDP_2406.06978.pdf) · [中文翻译](../papers/zh/HydraMDP_2406.06978_zh.pdf)
- **分类**: 免权重 test-time steering（verifier 蒸馏）

## 一句话

离线对整个轨迹词表跑规则模拟打分，把各 PDM 子指标分别蒸馏进多头解码器，推理时一次前向输出全部候选的分数——把 verifier 的延迟压到零。

## 解决什么问题

规则式轨迹打分（PDM score）可靠但慢（要做前向模拟），车载延迟预算内跑不了大候选集。如何让打分「免费」？

## 方法

1. **离线打分工厂**：对轨迹词表中每条候选，在日志场景中做规则模拟，算出 NC（无过错碰撞）、DAC（可行驶区域合规）、TTC、Comfort、EP（自车进度）各子分。
2. **多头蒸馏**：每个子指标一个预测头，把规则分数蒸馏进网络；PDM score = NC × DAC × DDC × (5·TTC + 2·C + 5·EP)/12。
3. **关键消融**：分头蒸馏各子指标 **优于** 直接蒸馏总分——标量总分有信息瓶颈。

## 关键结果

- CVPR 2024 端到端驾驶挑战赛冠军；推理时打分成本 ≈ 0（藏进主干前向）。

## 对机器人 TTT 的意义

「把 verifier 蒸馏到零延迟」的工程标准答案。任何 best-of-N / 搜索式 steering 想上车，打分这一步都绕不过延迟问题，Hydra-MDP 给出了范本：离线模拟产数据 + 子指标多头蒸馏。其消融（分头 > 总分）也是 reward hacking 讨论的重要证据。

## 局限与注意

- 词表固定：TOAD 实证其蒸馏头对词表外轨迹失准，不能直接当搜索目标。
- 规则教师的盲区会被蒸馏继承。

## 关联阅读

- 规则打分源头：[PDM-Closed (2306.07962)](PDMClosed_2306.07962.md)
- 其头的 OOD 弱点：[TOAD (2606.07170)](TOAD_2606.07170.md)
- 在其之上做 TTT：[Centaur (2503.11650)](Centaur_2503.11650.md)
