# Awesome Robot Test-Time Training (awesome_robo_ttt)

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

We maintain a curated list of resources on **Test-Time Training / Test-Time Adaptation / Test-Time Scaling for robot policies and autonomous driving** — how deployed embodied agents keep learning and improving after training ends.

我们维护一份「机器人测试时训练」资源清单：涵盖 TTA/TTT 基础、部署时策略适应、TTT 新浪潮（TTT 层/测试时 RL）、机器人与驾驶的权重级 TTT、免权重 test-time steering、2025-2026 前沿、免梯度上下文适应、失败检测与适应触发，以及 TTT 之前的 RL 微调与平滑探索。

**本仓库特色（Features）**：

- 📄 **88 篇论文全部附英文 PDF**（`papers/pdf/`）
- 🇨🇳 **中文翻译 PDF**（`papers/zh/`，由 [SuperTranslate](https://github.com/asimfish/super_translate) 保版式翻译；88/88 全部完成（SuperTranslate + DeepSeek 保版式翻译））
- 📝 **88 篇逐篇中文精读笔记**（`notes/`，含方法拆解/关键数字/局限/关联阅读）
- 💡 **趋势与洞见报告**（`insights/TRENDS_AND_INSIGHTS.md`，九大趋势 + 五条核心洞见 + 开放问题）
- 🧭 **设计空间矩阵**（`insights/DESIGN_SPACE_MATRIX.md`，30+ 方法按「适应对象 / 信号 / 延迟 / 安全机制 / 闭环评测」横向对比）
- 🗺️ **研究路线图**（`insights/OUR_ROADMAP.md`，文献结论落到 CADI×TTT 方案）
- 📚 **BibTeX**（`awesome_robo_ttt.bib`，全部条目可直接引用）
- 📊 **汇总报告**：HTML 幻灯片（`report/robo_ttt_report.html`）与 Beamer PDF（`report/robo_ttt_report.pdf`）

*Maintained by [asimfish](https://github.com/asimfish). Contributions welcome — see [Contributing](#contributing).*

## [Content](#content)

<table>
<tr><td colspan="2"><a href="#1-foundations-of-ttatttt">1. Foundations of TTA/TTT (视觉时代基础)</a></td></tr>
<tr><td colspan="2"><a href="#2-deployment-time-policy-adaptation">2. Deployment-Time Policy Adaptation (部署时策略适应)</a></td></tr>
<tr><td colspan="2"><a href="#3-the-new-wave-of-ttt">3. The New Wave of TTT (TTT 新浪潮)</a></td></tr>
<tr><td colspan="2"><a href="#4-weight-level-ttt-for-robots--driving">4. Weight-Level TTT for Robots & Driving (机器人/驾驶的权重级 TTT)</a></td></tr>
<tr><td colspan="2"><a href="#5-test-time-steering-without-weight-updates">5. Test-Time Steering without Weight Updates (免权重引导/搜索/验证)</a></td></tr>
<tr><td colspan="2"><a href="#6-frontier-2025-2026">6. Frontier 2025-2026 (前沿)</a></td></tr>
<tr><td colspan="2"><a href="#7-in-context-adaptation-for-robots">7. In-Context Adaptation for Robots (免梯度上下文适应)</a></td></tr>
<tr><td colspan="2"><a href="#8-failure-detection--adaptation-triggers">8. Failure Detection & Adaptation Triggers (失败检测与适应触发)</a></td></tr>
<tr><td colspan="2"><a href="#9-rl-fine-tuning--smooth-exploration-before-ttt">9. RL Fine-Tuning & Smooth Exploration before TTT (TTT 之前的阶段)</a></td></tr>
<tr><td colspan="2"><a href="#benchmarks--simulators">10. Benchmarks & Simulators (基准与仿真器)</a></td></tr>
<tr><td colspan="2"><a href="#trends--insights">11. Trends & Insights (趋势与洞见)</a></td></tr>
</table>

**Legend / 图例**: [paper] arXiv/会议原文链接 · [pdf] 仓库内英文 PDF · [中译] 中文翻译 PDF · [解读] 中文精读笔记

### [1. Foundations of TTA/TTT](#content)

TTT/TTA 的概念源头与稳定性/安全性基础。做任何机器人 TTT 前，先读这里的成功条件（TTT++）、崩溃机理（SAR/RDumb）与攻击面（DIA）。

1. **Test-Time Training with Self-Supervision for Generalization under Distribution Shifts.** ICML 2020. [paper](https://arxiv.org/abs/1909.13231) [pdf](papers/pdf/TTT_1909.13231.pdf) [中译](papers/zh/TTT_1909.13231_zh.pdf) [解读](notes/TTT_1909.13231.md)

    *Yu Sun, Xiaolong Wang, Zhuang Liu, John Miller, Alexei A. Efros, Moritz Hardt*

2. **Test-Time Training with Masked Autoencoders.** NeurIPS 2022. [paper](https://arxiv.org/abs/2209.07522) [pdf](papers/pdf/TTT-MAE_2209.07522.pdf) [中译](papers/zh/TTT-MAE_2209.07522_zh.pdf) [解读](notes/TTT-MAE_2209.07522.md)

    *Yossi Gandelsman, Yu Sun, Xinlei Chen, Alexei A. Efros*

3. **TTT++: When Does Self-Supervised Test-Time Training Fail or Thrive?** NeurIPS 2021. [paper](https://proceedings.neurips.cc/paper/2021/file/b618c3210e934362ac261db280128c22-Paper.pdf) [pdf](papers/pdf/TTTpp_NEURIPS2021.pdf) [中译](papers/zh/TTTpp_NEURIPS2021_zh.pdf) [解读](notes/TTTpp_NEURIPS2021.md)

    *Yuejiang Liu, Parth Kothari, Bastien van Delft, Baptiste Bellot-Gurlet, Taylor Mordan, Alexandre Alahi*

4. **Tent: Fully Test-Time Adaptation by Entropy Minimization.** ICLR 2021 (Spotlight). [paper](https://arxiv.org/abs/2006.10726) [pdf](papers/pdf/TENT_2006.10726.pdf) [中译](papers/zh/TENT_2006.10726_zh.pdf) [解读](notes/TENT_2006.10726.md)

    *Dequan Wang, Evan Shelhamer, Shaoteng Liu, Bruno Olshausen, Trevor Darrell*

5. **Towards Stable Test-Time Adaptation in Dynamic Wild World (SAR).** ICLR 2023 (Oral). [paper](https://arxiv.org/abs/2302.12400) [pdf](papers/pdf/SAR_2302.12400.pdf) [中译](papers/zh/SAR_2302.12400_zh.pdf) [解读](notes/SAR_2302.12400.md)

    *Shuaicheng Niu, Jiaxiang Wu, Yifan Zhang, Zhiquan Wen, Yaofo Chen, Peilin Zhao, Mingkui Tan*

6. **Efficient Test-Time Model Adaptation without Forgetting (EATA).** ICML 2022. [paper](https://arxiv.org/abs/2204.02610) [pdf](papers/pdf/EATA_2204.02610.pdf) [中译](papers/zh/EATA_2204.02610_zh.pdf) [解读](notes/EATA_2204.02610.md)

    *Shuaicheng Niu, Jiaxiang Wu, Yifan Zhang, Yaofo Chen, Shijian Zheng, Peilin Zhao, Mingkui Tan*

7. **Continual Test-Time Domain Adaptation (CoTTA).** CVPR 2022. [paper](https://arxiv.org/abs/2203.13591) [pdf](papers/pdf/CoTTA_2203.13591.pdf) [中译](papers/zh/CoTTA_2203.13591_zh.pdf) [解读](notes/CoTTA_2203.13591.md)

    *Qin Wang, Olga Fink, Luc Van Gool, Dengxin Dai*

8. **RDumb: A Simple Approach that Questions Our Progress in Continual Test-Time Adaptation.** NeurIPS 2023. [paper](https://arxiv.org/abs/2306.05401) [pdf](papers/pdf/RDumb_2306.05401.pdf) [中译](papers/zh/RDumb_2306.05401_zh.pdf) [解读](notes/RDumb_2306.05401.md)

    *Ori Press, Steffen Schneider, Matthias Kümmerer, Matthias Bethge*

9. **Uncovering Adversarial Risks of Test-Time Adaptation (DIA).** ICML 2023. [paper](https://arxiv.org/abs/2301.12576) [pdf](papers/pdf/DIA_2301.12576.pdf) [中译](papers/zh/DIA_2301.12576_zh.pdf) [解读](notes/DIA_2301.12576.md)

    *Tong Wu, Feiran Jia, Xiangyu Qi, Jiachen T. Wang, Vikash Sehwag, Saeed Mahloujifar, Prateek Mittal*

10. **Do We Really Need to Access the Source Data? Source Hypothesis Transfer for Unsupervised Domain Adaptation (SHOT).** ICML 2020. [paper](https://arxiv.org/abs/2002.08546) [pdf](papers/pdf/SHOT_2002.08546.pdf) [中译](papers/zh/SHOT_2002.08546_zh.pdf) [解读](notes/SHOT_2002.08546.md)

    *Jian Liang, Dapeng Hu, Jiashi Feng*

11. **MEMO: Test Time Robustness via Adaptation and Augmentation.** NeurIPS 2022. [paper](https://arxiv.org/abs/2110.09506) [pdf](papers/pdf/MEMO_2110.09506.pdf) [中译](papers/zh/MEMO_2110.09506_zh.pdf) [解读](notes/MEMO_2110.09506.md)

    *Marvin Zhang, Sergey Levine, Chelsea Finn*

12. **AR-TTA: A Simple Method for Real-World Continual Test-Time Adaptation.** ICCVW 2023. [paper](https://arxiv.org/abs/2309.10109) [pdf](papers/pdf/AR-TTA_2309.10109.pdf) [中译](papers/zh/AR-TTA_2309.10109_zh.pdf) [解读](notes/AR-TTA_2309.10109.md)

    *Damian Sójka, Sebastian Cygert, Bartłomiej Twardowski, Tomasz Trzciński*

### [2. Deployment-Time Policy Adaptation](#content)

机器人经典：部署时让策略/动力学模型持续适应的四条路线——自监督梯度（PAD）、免梯度前馈推断（RMA）、在线元学习（MOLe/Continual-MAML）、可证稳的低维适应（Neural-Fly），以及在线适应的速度边界（BayesMPC 反例）。

1. **Self-Supervised Policy Adaptation during Deployment (PAD).** ICLR 2021 (Spotlight). [paper](https://arxiv.org/abs/2007.04309) [pdf](papers/pdf/PAD_2007.04309.pdf) [中译](papers/zh/PAD_2007.04309_zh.pdf) [解读](notes/PAD_2007.04309.md)

    *Nicklas Hansen, Rishabh Jangir, Yu Sun, Guillem Alenyà, Pieter Abbeel, Alexei A. Efros, Lerrel Pinto, Xiaolong Wang*

2. **RMA: Rapid Motor Adaptation for Legged Robots.** RSS 2021. [paper](https://arxiv.org/abs/2107.04034) [pdf](papers/pdf/RMA_2107.04034.pdf) [中译](papers/zh/RMA_2107.04034_zh.pdf) [解读](notes/RMA_2107.04034.md)

    *Ashish Kumar, Zipeng Fu, Deepak Pathak, Jitendra Malik*

3. **Deep Online Learning via Meta-Learning: Continual Adaptation for Model-Based RL (MOLe).** arXiv 2018. [paper](https://arxiv.org/abs/1812.07671) [pdf](papers/pdf/MOLe_1812.07671.pdf) [中译](papers/zh/MOLe_1812.07671_zh.pdf) [解读](notes/MOLe_1812.07671.md)

    *Anusha Nagabandi, Chelsea Finn, Sergey Levine*

4. **Neural-Fly Enables Rapid Learning for Agile Flight in Strong Winds.** Science Robotics 2022. [paper](https://arxiv.org/abs/2205.06908) [pdf](papers/pdf/NeuralFly_2205.06908.pdf) [中译](papers/zh/NeuralFly_2205.06908_zh.pdf) [解读](notes/NeuralFly_2205.06908.md)

    *Michael O'Connell, Guanya Shi, Xichen Shi, Kamyar Azizzadenesheli, Anima Anandkumar, Yisong Yue, Soon-Jo Chung*

5. **Online Adaptation of Learned Vehicle Dynamics Model with Meta-Learning Approach.** IROS 2024. [paper](https://arxiv.org/abs/2409.14950) [pdf](papers/pdf/ContinualMAML_2409.14950.pdf) [中译](papers/zh/ContinualMAML_2409.14950_zh.pdf) [解读](notes/ContinualMAML_2409.14950.md)

    *Yuki Tsuchiya, Thomas Balch, Paul Drews, Guy Rosman*

6. **First, Learn What You Don't Know: Active Information Gathering for Driving at the Limits of Handling.** arXiv 2024. [paper](https://arxiv.org/abs/2411.00107) [pdf](papers/pdf/BayesMPC_2411.00107.pdf) [中译](papers/zh/BayesMPC_2411.00107_zh.pdf) [解读](notes/BayesMPC_2411.00107.md)

    *Alexander Davydov, Franck Djeumou, Marcus Greiff, Makoto Suminaka, et al. (Stanford / Toyota Research Institute)*

7. **Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks (MAML).** ICML 2017. [paper](https://arxiv.org/abs/1703.03400) [pdf](papers/pdf/MAML_1703.03400.pdf) [中译](papers/zh/MAML_1703.03400_zh.pdf) [解读](notes/MAML_1703.03400.md)

    *Chelsea Finn, Pieter Abbeel, Sergey Levine*

8. **Learning to Adapt in Dynamic, Real-World Environments Through Meta-Reinforcement Learning (GrBAL/ReBAL).** ICLR 2019. [paper](https://arxiv.org/abs/1803.11347) [pdf](papers/pdf/GrBAL_1803.11347.pdf) [中译](papers/zh/GrBAL_1803.11347_zh.pdf) [解读](notes/GrBAL_1803.11347.md)

    *Anusha Nagabandi, Ignasi Clavera, Simin Liu, Ronald S. Fearing, Pieter Abbeel, Sergey Levine, Chelsea Finn*

9. **DayDreamer: World Models for Physical Robot Learning.** CoRL 2022. [paper](https://arxiv.org/abs/2206.14176) [pdf](papers/pdf/DayDreamer_2206.14176.pdf) [中译](papers/zh/DayDreamer_2206.14176_zh.pdf) [解读](notes/DayDreamer_2206.14176.md)

    *Philipp Wu, Alejandro Escontrela, Danijar Hafner, Pieter Abbeel, Ken Goldberg*

10. **Adapt On-the-Go: Behavior Modulation for Single-Life Robot Deployment (ROAM).** CoLLAs 2025. [paper](https://arxiv.org/abs/2311.01059) [pdf](papers/pdf/ROAM_2311.01059.pdf) [中译](papers/zh/ROAM_2311.01059_zh.pdf) [解读](notes/ROAM_2311.01059.md)

    *Annie S. Chen, Govind Chada, Laura Smith, Archit Sharma, Zipeng Fu, Sergey Levine, Chelsea Finn*

### [3. The New Wave of TTT](#content)

2024-2026 的范式跃迁：TTT 从「部署补丁」变成「网络层」（TTT-Layers），从视觉扩展到少样本推理（ARC）、视频生成、测试时 RL（TTRL），并与 test-time scaling 汇流。

1. **Learning to (Learn at Test Time): RNNs with Expressive Hidden States (TTT-Linear/TTT-MLP).** ICML 2025. [paper](https://arxiv.org/abs/2407.04620) [pdf](papers/pdf/TTTLayers_2407.04620.pdf) [中译](papers/zh/TTTLayers_2407.04620_zh.pdf) [解读](notes/TTTLayers_2407.04620.md)

    *Yu Sun, Xinhao Li, Karan Dalal, et al. (Stanford / UCSD / UC Berkeley / Meta)*

2. **The Surprising Effectiveness of Test-Time Training for Few-Shot Learning (ARC-TTT).** ICML 2025. [paper](https://arxiv.org/abs/2411.07279) [pdf](papers/pdf/ARC-TTT_2411.07279.pdf) [中译](papers/zh/ARC-TTT_2411.07279_zh.pdf) [解读](notes/ARC-TTT_2411.07279.md)

    *Ekin Akyürek, Mehul Damani, Linlu Qiu, Han Guo, Yoon Kim, Jacob Andreas (MIT)*

3. **One-Minute Video Generation with Test-Time Training.** CVPR 2025. [paper](https://arxiv.org/abs/2504.05298) [pdf](papers/pdf/VideoTTT_2504.05298.pdf) [中译](papers/zh/VideoTTT_2504.05298_zh.pdf) [解读](notes/VideoTTT_2504.05298.md)

    *Karan Dalal, Daniel Koceja, et al. (Stanford / UCSD / UC Berkeley / NVIDIA)*

4. **TTRL: Test-Time Reinforcement Learning.** NeurIPS 2025. [paper](https://arxiv.org/abs/2504.16084) [pdf](papers/pdf/TTRL_2504.16084.pdf) [中译](papers/zh/TTRL_2504.16084_zh.pdf) [解读](notes/TTRL_2504.16084.md)

    *Yuxin Zuo, Kaiyan Zhang, et al. (Tsinghua PRIME-RL)*

5. **In-context Reinforcement Learning with Algorithm Distillation.** ICLR 2023. [paper](https://arxiv.org/abs/2210.14215) [pdf](papers/pdf/AlgDistill_2210.14215.pdf) [中译](papers/zh/AlgDistill_2210.14215_zh.pdf) [解读](notes/AlgDistill_2210.14215.md)

    *Michael Laskin, Luyu Wang, et al. (DeepMind)*

6. **End-to-End Test-Time Training for Long Context (TTT-E2E).** arXiv 2025. [paper](https://arxiv.org/abs/2512.23675) [pdf](papers/pdf/TTT-E2E_2512.23675.pdf) [中译](papers/zh/TTT-E2E_2512.23675_zh.pdf) [解读](notes/TTT-E2E_2512.23675.md)

    *Arnuv Tandon, Karan Dalal, Xinhao Li, Daniel Koceja, Marcel Rød, et al. (Stanford / Astera / NVIDIA)*

7. **Scaling LLM Test-Time Compute Optimally Can Be More Effective than Scaling Model Parameters.** arXiv 2024. [paper](https://arxiv.org/abs/2408.03314) [pdf](papers/pdf/SnellTTC_2408.03314.pdf) [中译](papers/zh/SnellTTC_2408.03314_zh.pdf) [解读](notes/SnellTTC_2408.03314.md)

    *Charlie Snell, Jaehoon Lee, Kelvin Xu, Aviral Kumar (UC Berkeley / Google DeepMind)*

8. **A Survey of Test-Time Compute: From Intuitive Inference to Deliberate Reasoning.** arXiv 2025. [paper](https://arxiv.org/abs/2501.02497) [pdf](papers/pdf/TTCSurvey_2501.02497.pdf) [中译](papers/zh/TTCSurvey_2501.02497_zh.pdf) [解读](notes/TTCSurvey_2501.02497.md)

9. **Titans: Learning to Memorize at Test Time.** NeurIPS 2025. [paper](https://arxiv.org/abs/2501.00663) [pdf](papers/pdf/Titans_2501.00663.pdf) [中译](papers/zh/Titans_2501.00663_zh.pdf) [解读](notes/Titans_2501.00663.md)

    *Ali Behrouz, Peilin Zhong, Vahab Mirrokni (Google Research)*

10. **Test-Time Training Done Right (LaCT).** arXiv 2025. [paper](https://arxiv.org/abs/2505.23884) [pdf](papers/pdf/LaCT_2505.23884.pdf) [中译](papers/zh/LaCT_2505.23884_zh.pdf) [解读](notes/LaCT_2505.23884.md)

    *Tianyuan Zhang, Sai Bi, Yicong Hong, Kai Zhang, Fujun Luan, et al. (MIT / Adobe)*

11. **Atlas: Learning to Optimally Memorize the Context at Test Time.** arXiv 2025. [paper](https://arxiv.org/abs/2505.23735) [pdf](papers/pdf/ATLAS_2505.23735.pdf) [中译](papers/zh/ATLAS_2505.23735_zh.pdf) [解读](notes/ATLAS_2505.23735.md)

    *Ali Behrouz, Zeman Li, Praneeth Kacham, et al. (Google Research)*

12. **TNT: Improving Chunkwise Training for Test-Time Memorization.** arXiv 2025. [paper](https://arxiv.org/abs/2511.07343) [pdf](papers/pdf/TNT_2511.07343.pdf) [中译](papers/zh/TNT_2511.07343_zh.pdf) [解读](notes/TNT_2511.07343.md)

    *Zeman Li, Ali Behrouz, et al. (USC / Google Research)*

### [4. Weight-Level TTT for Robots & Driving](#content)

本仓库的核心：在部署中更新权重（或快权重）的机器人/驾驶工作。RoboTTT 与 Centaur 分别是操作与驾驶域的里程碑。

1. **RoboTTT: Context Scaling for Robot Policies.** arXiv 2026. [paper](https://arxiv.org/abs/2607.15275) [pdf](papers/pdf/RoboTTT_2607.15275.pdf) [中译](papers/zh/RoboTTT_2607.15275_zh.pdf) [解读](notes/RoboTTT_2607.15275.md)

    *NVIDIA GEAR Team*

2. **WAM-TTT: Steering World-Action Models by Watching Human Play at Test Time.** arXiv 2026. [paper](https://arxiv.org/abs/2607.06988) [pdf](papers/pdf/WAMTTT_2607.06988.pdf) [中译](papers/zh/WAMTTT_2607.06988_zh.pdf) [解读](notes/WAMTTT_2607.06988.md)

    *Yusen Feng, Bingchen Han, Jiangran Lyu, et al. (Peking University / Galbot / CASIA / Tsinghua)*

3. **On-the-Fly VLA Adaptation via Test-Time Reinforcement Learning (TT-VLA).** arXiv 2026. [paper](https://arxiv.org/abs/2601.06748) [pdf](papers/pdf/TT-VLA_2601.06748.pdf) [中译](papers/zh/TT-VLA_2601.06748_zh.pdf) [解读](notes/TT-VLA_2601.06748.md)

    *Changyu Liu, Yiyang Liu, Taowen Wang, et al.*

4. **Centaur: Robust End-to-End Autonomous Driving with Test-Time Training.** arXiv 2025. [paper](https://arxiv.org/abs/2503.11650) [pdf](papers/pdf/Centaur_2503.11650.pdf) [中译](papers/zh/Centaur_2503.11650_zh.pdf) [解读](notes/Centaur_2503.11650.md)

    *Chonghao Sima, Kashyap Chitta, Zhiding Yu, Andreas Geiger, Hongyang Li, Jose M. Alvarez (HKU / NVIDIA / Tübingen)*

5. **Model-Based Policy Adaptation for Closed-Loop End-to-End Autonomous Driving (MPA).** arXiv 2025. [paper](https://arxiv.org/abs/2511.21584) [pdf](papers/pdf/MPA_2511.21584.pdf) [中译](papers/zh/MPA_2511.21584_zh.pdf) [解读](notes/MPA_2511.21584.md)

    *Haohong Lin, Yunzhi Zhang, Wenhao Ding, Jiajun Wu, Ding Zhao (CMU / Stanford / NVIDIA)*

6. **Post-Training in End-to-End Autonomous Driving: A Unified View.** arXiv 2026 (Survey). [paper](https://arxiv.org/abs/2607.08072) [pdf](papers/pdf/PostTrainSurvey_2607.08072.pdf) [中译](papers/zh/PostTrainSurvey_2607.08072_zh.pdf) [解读](notes/PostTrainSurvey_2607.08072.md)

    *Ruining Yang, et al. (Northeastern / Purdue)*

7. **TTT-Parkour: Rapid Test-Time Training for Perceptive Robot Parkour.** arXiv 2026. [paper](https://arxiv.org/abs/2602.02331) [pdf](papers/pdf/TTTParkour_2602.02331.pdf) [中译](papers/zh/TTTParkour_2602.02331_zh.pdf) [解读](notes/TTTParkour_2602.02331.md)

### [5. Test-Time Steering without Weight Updates](#content)

不改权重的测试时改进：梯度引导（guidance）、采样+critic 重排（best-of-N）、进化/CEM 搜索、噪声空间 RL、驾驶 verifier 体系与延迟使能技术。

1. **Planning with Diffusion for Flexible Behavior Synthesis (Diffuser).** ICML 2022. [paper](https://arxiv.org/abs/2205.09991) [pdf](papers/pdf/Diffuser_2205.09991.pdf) [中译](papers/zh/Diffuser_2205.09991_zh.pdf) [解读](notes/Diffuser_2205.09991.md)

    *Michael Janner, Yilun Du, Joshua B. Tenenbaum, Sergey Levine (UC Berkeley / MIT)*

2. **Guided Conditional Diffusion for Controllable Traffic Simulation (CTG).** ICRA 2023. [paper](https://arxiv.org/abs/2210.17366) [pdf](papers/pdf/CTG_2210.17366.pdf) [中译](papers/zh/CTG_2210.17366_zh.pdf) [解读](notes/CTG_2210.17366.md)

    *Ziyuan Zhong, Davis Rempe, Danfei Xu, Yuxiao Chen, Sushant Veer, Tong Che, Baishakhi Ray, Marco Pavone (Columbia / NVIDIA)*

3. **SafeDiffuser: Safe Planning with Diffusion Probabilistic Models.** ICLR 2025. [paper](https://arxiv.org/abs/2306.00148) [pdf](papers/pdf/SafeDiffuser_2306.00148.pdf) [中译](papers/zh/SafeDiffuser_2306.00148_zh.pdf) [解读](notes/SafeDiffuser_2306.00148.md)

    *Wei Xiao, Tsun-Hsuan Wang, Chuang Gan, Daniela Rus (MIT)*

4. **IDQL: Implicit Q-Learning as an Actor-Critic Method with Diffusion Policies.** arXiv 2023. [paper](https://arxiv.org/abs/2304.10573) [pdf](papers/pdf/IDQL_2304.10573.pdf) [中译](papers/zh/IDQL_2304.10573_zh.pdf) [解读](notes/IDQL_2304.10573.md)

    *Philippe Hansen-Estruch, Ilya Kostrikov, Michael Janner, Jakub Grudzien Kuba, Sergey Levine (UC Berkeley)*

5. **Recovery RL: Safe Reinforcement Learning with Learned Recovery Zones.** IEEE RA-L 2021. [paper](https://arxiv.org/abs/2010.15920) [pdf](papers/pdf/RecoveryRL_2010.15920.pdf) [中译](papers/zh/RecoveryRL_2010.15920_zh.pdf) [解读](notes/RecoveryRL_2010.15920.md)

    *Brijen Thananjeyan, Ashwin Balakrishna, et al. (UC Berkeley)*

6. **RoboMonkey: Scaling Test-Time Sampling and Verification for Vision-Language-Action Models.** CoRL 2025. [paper](https://arxiv.org/abs/2506.17811) [pdf](papers/pdf/RoboMonkey_2506.17811.pdf) [中译](papers/zh/RoboMonkey_2506.17811_zh.pdf) [解读](notes/RoboMonkey_2506.17811.md)

    *Jacky Kwok, et al. (Stanford)*

7. **Diffusion-ES: Gradient-free Planning with Diffusion for Autonomous Driving and Zero-Shot Instruction Following.** CVPR 2024. [paper](https://arxiv.org/abs/2402.06559) [pdf](papers/pdf/DiffusionES_2402.06559.pdf) [中译](papers/zh/DiffusionES_2402.06559_zh.pdf) [解读](notes/DiffusionES_2402.06559.md)

    *Brian Yang, et al. (CMU)*

8. **Test-Time Trajectory Optimization for Autonomous Driving (TOAD).** arXiv 2026. [paper](https://arxiv.org/abs/2606.07170) [pdf](papers/pdf/TOAD_2606.07170.pdf) [中译](papers/zh/TOAD_2606.07170_zh.pdf) [解读](notes/TOAD_2606.07170.md)

    *Yihong Xu, Éloi Zablocki, et al. (valeo.ai)*

9. **Steering Your Diffusion Policy with Latent Space Reinforcement Learning (DSRL).** CoRL 2025. [paper](https://arxiv.org/abs/2506.15799) [pdf](papers/pdf/DSRL_2506.15799.pdf) [中译](papers/zh/DSRL_2506.15799_zh.pdf) [解读](notes/DSRL_2506.15799.md)

    *Andrew Wagenmaker, et al. (UC Berkeley)*

10. **Inference-Time Policy Steering through Human Interactions (ITPS).** ICRA 2025. [paper](https://arxiv.org/abs/2411.16627) [pdf](papers/pdf/ITPS_2411.16627.pdf) [中译](papers/zh/ITPS_2411.16627_zh.pdf) [解读](notes/ITPS_2411.16627.md)

    *Yanwei Wang, et al. (MIT)*

11. **DynaGuide: Steering Diffusion Policies with Active Dynamic Guidance.** NeurIPS 2025. [paper](https://arxiv.org/abs/2506.13922) [pdf](papers/pdf/DynaGuide_2506.13922.pdf) [中译](papers/zh/DynaGuide_2506.13922_zh.pdf) [解读](notes/DynaGuide_2506.13922.md)

    *Maximilian Du, Shuran Song (Stanford)*

12. **Parting with Misconceptions about Learning-based Vehicle Motion Planning (PDM-Closed).** CoRL 2023. [paper](https://arxiv.org/abs/2306.07962) [pdf](papers/pdf/PDMClosed_2306.07962.pdf) [中译](papers/zh/PDMClosed_2306.07962_zh.pdf) [解读](notes/PDMClosed_2306.07962.md)

    *Daniel Dauner, Marcel Hallgarten, Andreas Geiger, Kashyap Chitta (Tübingen / Bosch)*

13. **Hydra-MDP: End-to-end Multimodal Planning with Multi-target Hydra-Distillation.** CVPRW 2024 (E2E Challenge Winner). [paper](https://arxiv.org/abs/2406.06978) [pdf](papers/pdf/HydraMDP_2406.06978.pdf) [中译](papers/zh/HydraMDP_2406.06978_zh.pdf) [解读](notes/HydraMDP_2406.06978.md)

    *Zhenxin Li, et al. (NVIDIA)*

14. **Consistency Policy: Accelerated Visuomotor Policies via Consistency Distillation.** RSS 2024. [paper](https://arxiv.org/abs/2405.07503) [pdf](papers/pdf/ConsistencyPolicy_2405.07503.pdf) [中译](papers/zh/ConsistencyPolicy_2405.07503_zh.pdf) [解读](notes/ConsistencyPolicy_2405.07503.md)

    *Aaditya Prasad, et al. (Stanford)*

15. **ADPro: A Test-time Adaptive Diffusion Policy via Manifold-constrained Denoising and Task-aware Initialization.** arXiv 2025. [paper](https://arxiv.org/abs/2508.06266) [pdf](papers/pdf/ADPro_2508.06266.pdf) [中译](papers/zh/ADPro_2508.06266_zh.pdf) [解读](notes/ADPro_2508.06266.md)

16. **Generalized Trajectory Scoring for End-to-end Multimodal Planning (GTRS).** arXiv 2025 (CVPR 2025 Challenge Winner). [paper](https://arxiv.org/abs/2506.06664) [pdf](papers/pdf/GTRS_2506.06664.pdf) [中译](papers/zh/GTRS_2506.06664_zh.pdf) [解读](notes/GTRS_2506.06664.md)

    *Zhenxin Li, Wenhao Yao, Zi Wang, et al. (NVIDIA)*

17. **Hydra-NeXt: Robust Closed-Loop Driving with Open-Loop Training.** ICCV 2025. [paper](https://arxiv.org/abs/2503.12030) [pdf](papers/pdf/HydraNeXt_2503.12030.pdf) [中译](papers/zh/HydraNeXt_2503.12030_zh.pdf) [解读](notes/HydraNeXt_2503.12030.md)

    *Zhenxin Li, Shihao Wang, Shiyi Lan, Zhiding Yu, Zuxuan Wu, Jose M. Alvarez (NVIDIA / Fudan)*

18. **DriveCritic: Towards Context-Aware, Human-Aligned Evaluation for Autonomous Driving with Vision-Language Models.** arXiv 2025. [paper](https://arxiv.org/abs/2510.13108) [pdf](papers/pdf/DriveCritic_2510.13108.pdf) [中译](papers/zh/DriveCritic_2510.13108_zh.pdf) [解读](notes/DriveCritic_2510.13108.md)

19. **Compose Your Policies! Improving Diffusion-based or Flow-based Robot Policies via Test-time Distribution-level Composition (GPC).** ICLR 2026. [paper](https://arxiv.org/abs/2510.01068) [pdf](papers/pdf/GPC_2510.01068.pdf) [中译](papers/zh/GPC_2510.01068_zh.pdf) [解读](notes/GPC_2510.01068.md)

20. **PriGo: Test-Time Primitive Guidance to Diffusion and Flow Policies for Adaptive Robotic Manipulation.** arXiv 2026. [paper](https://arxiv.org/abs/2607.07076) [pdf](papers/pdf/PriGo_2607.07076.pdf) [中译](papers/zh/PriGo_2607.07076_zh.pdf) [解读](notes/PriGo_2607.07076.md)

21. **Closed-Loop Action Chunks with Dynamic Corrections for Training-Free Diffusion Policy (DCDP).** arXiv 2026. [paper](https://arxiv.org/abs/2603.01953) [pdf](papers/pdf/DCDP_2603.01953.pdf) [中译](papers/zh/DCDP_2603.01953_zh.pdf) [解读](notes/DCDP_2603.01953.md)

22. **ORPA: Online Residual Policy Adaptation for Robot Manipulation Control with Human Feedback.** arXiv 2026. [paper](https://arxiv.org/abs/2608.17323) [pdf](papers/pdf/ORPA_2608.17323.pdf) [中译](papers/zh/ORPA_2608.17323_zh.pdf) [解读](notes/ORPA_2608.17323.md)

### [6. Frontier 2025-2026](#content)

扩展调研新增的最前沿：可靠性协议（VANE）、潜提示接口（TTT-VLA LPO）、PRM 验证器（RoVer）、具身 TTS 参考架构（E-TTS）、自适应算力调度（ELASTIC/VLA-ATTC）、轨迹级 MCTS（SAIL）。

1. **VANE: Reliable Test-Time Training for Vision-Language-Action Models via Future Visual Representation Prediction.** arXiv 2026. [paper](https://arxiv.org/abs/2608.09448) [pdf](papers/pdf/VANE_2608.09448.pdf) [中译](papers/zh/VANE_2608.09448_zh.pdf) [解读](notes/VANE_2608.09448.md)

2. **TTT-VLA: Test-Time Latent Prompt Optimization for Vision-Language-Action Models.** arXiv 2026. [paper](https://arxiv.org/abs/2606.03127) [pdf](papers/pdf/TTTVLA-LPO_2606.03127.pdf) [中译](papers/zh/TTTVLA-LPO_2606.03127_zh.pdf) [解读](notes/TTTVLA-LPO_2606.03127.md)

3. **RoVer: Robot Reward Model as Test-Time Verifier for Vision-Language-Action Model.** arXiv 2025. [paper](https://arxiv.org/abs/2510.10975) [pdf](papers/pdf/RoVer_2510.10975.pdf) [中译](papers/zh/RoVer_2510.10975_zh.pdf) [解读](notes/RoVer_2510.10975.md)

4. **E-TTS: A New Embodied Test-Time Scaling Framework for Robotic Manipulation.** arXiv 2026. [paper](https://arxiv.org/abs/2606.27268) [pdf](papers/pdf/E-TTS_2606.27268.pdf) [中译](papers/zh/E-TTS_2606.27268_zh.pdf) [解读](notes/E-TTS_2606.27268.md)

5. **ELASTIC: Efficiently Learning to Adaptively Scale Test-Time Compute for Generative Control Policies.** arXiv 2026. [paper](https://arxiv.org/abs/2606.31132) [pdf](papers/pdf/ELASTIC_2606.31132.pdf) [中译](papers/zh/ELASTIC_2606.31132_zh.pdf) [解读](notes/ELASTIC_2606.31132.md)

6. **SAIL: Test-Time Scaling for In-Context Imitation Learning with VLM.** arXiv 2026. [paper](https://arxiv.org/abs/2603.08269) [pdf](papers/pdf/SAIL_2603.08269.pdf) [中译](papers/zh/SAIL_2603.08269_zh.pdf) [解读](notes/SAIL_2603.08269.md)

7. **VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model.** arXiv 2026. [paper](https://arxiv.org/abs/2605.01194) [pdf](papers/pdf/VLA-ATTC_2605.01194.pdf) [中译](papers/zh/VLA-ATTC_2605.01194_zh.pdf) [解读](notes/VLA-ATTC_2605.01194.md)

8. **DREAM-Chunk: Reactive Action Chunking with Latent World Model.** arXiv 2026. [paper](https://arxiv.org/abs/2606.18589) [pdf](papers/pdf/DREAMChunk_2606.18589.pdf) [中译](papers/zh/DREAMChunk_2606.18589_zh.pdf) [解读](notes/DREAMChunk_2606.18589.md)

*另见（README-only，未收录 PDF）：AR-TTA（arXiv:2309.10109，驾驶持续 TTA 基准）、LearnableBN（AAAI 2026，驾驶感知 BN-TTA）、Topology-Guided TTA（CVPRW 2026，「何时适应」分类器）、DIRECT / DA-SIP / τ0-VLA（自适应算力路由）。*

### [7. In-Context Adaptation for Robots](#content)

免梯度上下文适应：把演示直接放进上下文（或检索库），零梯度、零微调地适应新任务——与权重级 TTT 互补的「快适应」路线（另见分类③的 Algorithm Distillation）。

1. **In-Context Imitation Learning via Next-Token Prediction (ICRT).** arXiv 2024. [paper](https://arxiv.org/abs/2408.15980) [pdf](papers/pdf/ICRT_2408.15980.pdf) [中译](papers/zh/ICRT_2408.15980_zh.pdf) [解读](notes/ICRT_2408.15980.md)

    *Letian Fu, et al. (UC Berkeley)*

2. **Instant Policy: In-Context Imitation Learning via Graph Diffusion.** ICLR 2025. [paper](https://arxiv.org/abs/2411.12633) [pdf](papers/pdf/InstantPolicy_2411.12633.pdf) [中译](papers/zh/InstantPolicy_2411.12633_zh.pdf) [解读](notes/InstantPolicy_2411.12633.md)

    *Vitalis Vosylius, Edward Johns (Imperial College London)*

3. **RICL: Adding In-Context Adaptability to Pre-Trained Vision-Language-Action Models.** arXiv 2025. [paper](https://arxiv.org/abs/2508.02062) [pdf](papers/pdf/RICL_2508.02062.pdf) [中译](papers/zh/RICL_2508.02062_zh.pdf) [解读](notes/RICL_2508.02062.md)

4. **LocoFormer: Generalist Locomotion via Long-context Adaptation.** arXiv 2025 (CoRL 2025). [paper](https://arxiv.org/abs/2509.23745) [pdf](papers/pdf/LocoFormer_2509.23745.pdf) [中译](papers/zh/LocoFormer_2509.23745_zh.pdf) [解读](notes/LocoFormer_2509.23745.md)

5. **AnyCar to Anywhere: Learning Universal Dynamics Model for Agile and Adaptive Mobility.** ICRA 2025. [paper](https://arxiv.org/abs/2409.15783) [pdf](papers/pdf/AnyCar_2409.15783.pdf) [中译](papers/zh/AnyCar_2409.15783_zh.pdf) [解读](notes/AnyCar_2409.15783.md)

    *Wenli Xiao, Haoru Xue, Tony Tao, Dvij Kalaria, John M. Dolan, Guanya Shi (CMU)*

### [8. Failure Detection & Adaptation Triggers](#content)

「什么时候该适应」的传感器：运行时失败检测 / OOD 检测给 TTT 提供触发与回滚信号（另见 Centaur 的 Cluster Entropy、VLA-ATTC 的认知离合器）。

1. **Unpacking Failure Modes of Generative Policies: Runtime Monitoring of Consistency and Progress (Sentinel).** CoRL 2024. [paper](https://arxiv.org/abs/2410.04640) [pdf](papers/pdf/Sentinel_2410.04640.pdf) [中译](papers/zh/Sentinel_2410.04640_zh.pdf) [解读](notes/Sentinel_2410.04640.md)

    *Christopher Agia, Rohan Sinha, Jingyun Yang, Zi-ang Cao, Rika Antonova, Marco Pavone, Jeannette Bohg (Stanford)*

2. **Can We Detect Failures Without Failure Data? Uncertainty-Aware Runtime Failure Detection for Imitation Learning Policies (FAIL-Detect).** RSS 2025. [paper](https://arxiv.org/abs/2503.08558) [pdf](papers/pdf/FAILDetect_2503.08558.pdf) [中译](papers/zh/FAILDetect_2503.08558_zh.pdf) [解读](notes/FAILDetect_2503.08558.md)

    *Chen Xu, Tony Khuong Nguyen, Emma Dixon, et al. (Toyota Research Institute / Columbia)*

3. **SAFE: Multitask Failure Detection for Vision-Language-Action Models.** NeurIPS 2025. [paper](https://arxiv.org/abs/2506.09937) [pdf](papers/pdf/SAFE_2506.09937.pdf) [中译](papers/zh/SAFE_2506.09937_zh.pdf) [解读](notes/SAFE_2506.09937.md)

    *Qiao Gu, Yuanliang Ju, Shengxiang Sun, Igor Gilitschenski, Haruki Nishimura, Masha Itkina, Florian Shkurti*

### [9. RL Fine-Tuning & Smooth Exploration before TTT](#content)

方案专属：TTT 站在「DP 初始化 → 离线 RL → 在线 RL」管线之上。这里收录离线→在线 RL 稳定性、动作分块 RL 与平滑探索噪声的关键工作——它们解释了 on-policy 早期为何学崩、以及为何高阶导数动作接口能滤掉探索噪声。

1. **Diffusion Policy Policy Optimization (DPPO).** ICLR 2025. [paper](https://arxiv.org/abs/2409.00588) [pdf](papers/pdf/DPPO_2409.00588.pdf) [中译](papers/zh/DPPO_2409.00588_zh.pdf) [解读](notes/DPPO_2409.00588.md)

    *Allen Z. Ren, Justin Lidard, Lars L. Ankile, Anthony Simeonov, Pulkit Agrawal, Anirudha Majumdar, Benjamin Burchfiel, Hongkai Dai, Max Simchowitz*

2. **Reinforcement Learning with Action Chunking (Q-Chunking).** NeurIPS 2025. [paper](https://arxiv.org/abs/2507.07969) [pdf](papers/pdf/QChunking_2507.07969.pdf) [中译](papers/zh/QChunking_2507.07969_zh.pdf) [解读](notes/QChunking_2507.07969.md)

    *Qiyang Li, Zhiyuan Zhou, Sergey Levine (UC Berkeley)*

3. **Efficient Online Reinforcement Learning with Offline Data (RLPD).** ICML 2023. [paper](https://arxiv.org/abs/2302.02948) [pdf](papers/pdf/RLPD_2302.02948.pdf) [中译](papers/zh/RLPD_2302.02948_zh.pdf) [解读](notes/RLPD_2302.02948.md)

    *Philip J. Ball, Laura Smith, Ilya Kostrikov, Sergey Levine*

4. **Cal-QL: Calibrated Offline RL Pre-Training for Efficient Online Fine-Tuning.** NeurIPS 2023. [paper](https://arxiv.org/abs/2303.05479) [pdf](papers/pdf/CalQL_2303.05479.pdf) [中译](papers/zh/CalQL_2303.05479_zh.pdf) [解读](notes/CalQL_2303.05479.md)

    *Mitsuhiko Nakamoto, Yuexiang Zhai, Anikait Singh, Max Sobol Mark, Yi Ma, Chelsea Finn, Aviral Kumar, Sergey Levine*

5. **Efficient Online Reinforcement Learning Fine-Tuning Need Not Retain Offline Data (WSRL).** ICLR 2025. [paper](https://arxiv.org/abs/2412.07762) [pdf](papers/pdf/WSRL_2412.07762.pdf) [中译](papers/zh/WSRL_2412.07762_zh.pdf) [解读](notes/WSRL_2412.07762.md)

    *Zhiyuan Zhou, Andy Peng, Qiyang Li, Sergey Levine, Aviral Kumar*

6. **Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement Learning (HIL-SERL).** Science Robotics 2025. [paper](https://arxiv.org/abs/2410.21845) [pdf](papers/pdf/HILSERL_2410.21845.pdf) [中译](papers/zh/HILSERL_2410.21845_zh.pdf) [解读](notes/HILSERL_2410.21845.md)

    *Jianlan Luo, Charles Xu, Jeffrey Wu, Sergey Levine (UC Berkeley)*

7. **ConRFT: A Reinforced Fine-tuning Method for VLA Models via Consistency Policy.** RSS 2025. [paper](https://arxiv.org/abs/2502.05450) [pdf](papers/pdf/ConRFT_2502.05450.pdf) [中译](papers/zh/ConRFT_2502.05450_zh.pdf) [解读](notes/ConRFT_2502.05450.md)

    *Yuhui Chen, Shuai Tian, Shugao Liu, Yingting Zhou, Haoran Li, Dongbin Zhao (CASIA)*

8. **Smooth Exploration for Robotic Reinforcement Learning (gSDE).** CoRL 2021. [paper](https://arxiv.org/abs/2005.05719) [pdf](papers/pdf/gSDE_2005.05719.pdf) [中译](papers/zh/gSDE_2005.05719_zh.pdf) [解读](notes/gSDE_2005.05719.md)

    *Antonin Raffin, Jens Kober, Freek Stulp (DLR / TU Delft)*

9. **Pink Noise Is All You Need: Colored Noise Exploration in Deep Reinforcement Learning.** ICLR 2023 (Oral). [paper](https://openreview.net/forum?id=hQ9V5QN27eS) [pdf](papers/pdf/PinkNoise_ICLR2023.pdf) [中译](papers/zh/PinkNoise_ICLR2023_zh.pdf) [解读](notes/PinkNoise_ICLR2023.md)

    *Onno Eberhard, Jakob Hollenstein, Cristina Pinneri, Georg Martius (MPI-IS)*

### [Benchmarks & Simulators](#content)

本仓库论文常用的评测平台（按域分组，便于复现与对标）：

| 域 | 基准 / 仿真器 | 用途与相关论文 |
|---|---|---|
| 驾驶（非反应式） | [NAVSIM](https://github.com/autonomousvision/navsim) navtest / navhard (PDMS, EPDMS) | Centaur · Hydra-MDP · GTRS · TOAD |
| 驾驶（反应式闭环） | [Bench2Drive](https://github.com/Thinklab-SJTU/Bench2Drive) (CARLA) · [HUGSIM](https://github.com/hyzhou404/HUGSIM) (3DGS) · [nuPlan](https://github.com/motional/nuplan-devkit) | Hydra-NeXt · TOAD · PDM-Closed · Diffusion-ES |
| 驾驶（持续 TTA 流） | CLAD-C · SHIFT · nuScenes-C | AR-TTA · LearnableBN |
| 操作（仿真） | [robomimic](https://robomimic.github.io/) · [LIBERO](https://libero-project.github.io/) · [SimplerEnv](https://simpler-env.github.io/) · CALVIN · RLBench · PushT · [OGBench](https://seohong.me/projects/ogbench/) | DPPO · Q-Chunking · TTT-VLA · VANE · SAFE · ADPro · GPC |
| 操作（真机） | ALOHA · Franka / UR 系 · WidowX (Bridge) · Google Robot | HIL-SERL · ConRFT · ORPA · RoboMonkey |
| 腿足 | Isaac Gym/Lab 地形 · Go1/Go2 · 人形 parkour | RMA · LocoFormer · ROAM · TTT-Parkour |
| 持续 TTA（视觉） | CIFAR-10/100-C · ImageNet-C · CCC (RDumb) | TENT · SAR · EATA · CoTTA · RDumb |
| 长上下文 / 序列 | Pile / Books · 大海捞针 · ARC | TTT-Layers · Titans · TTT-E2E · ARC-TTT |

### [Trends & Insights](#content)

→ **[insights/TRENDS_AND_INSIGHTS.md](insights/TRENDS_AND_INSIGHTS.md)**：九大趋势（接口化适应 / 验证式准入 / verifier 军备 / 算力调度学习化 / 任务耦合自监督 / 人类数据转向信号 / 驾驶两派对垒 / 段级「重建再训练」TTT / 失败检测器成为触发标配）+ 五条核心洞见 + 开放问题清单。

→ **[insights/DESIGN_SPACE_MATRIX.md](insights/DESIGN_SPACE_MATRIX.md)**：30+ 代表方法的设计空间矩阵。

→ **[insights/OUR_ROADMAP.md](insights/OUR_ROADMAP.md)**：从文献到方案（CADI × TTT）的研究路线图。

### [Reports 汇总报告](#content)

- **HTML 幻灯片**：[report/robo_ttt_report.html](report/robo_ttt_report.html)（浏览器打开，方向键翻页）
- **Beamer PDF**：[report/robo_ttt_report.pdf](report/robo_ttt_report.pdf)

### [Repository Structure](#content)

```
awesome_robo_ttt/
├── README.md                  # 本文件（awesome 清单）
├── papers/
│   ├── pdf/                   # 88 篇英文原文 PDF
│   └── zh/                    # 中文翻译 PDF（SuperTranslate 保版式翻译）
├── notes/                     # 88 篇逐篇中文精读笔记（含索引 README.md）
├── insights/                  # 趋势与洞见 · 设计空间矩阵 · 研究路线图
├── awesome_robo_ttt.bib       # 全部条目 BibTeX
├── report/                    # 汇总报告（HTML 幻灯片 + Beamer PDF）
└── scripts/                   # 文献清单（papers.tsv）、下载与翻译脚本
```

### [Contributing](#content)

欢迎 PR 补充新论文。格式请参照现有条目：`**标题.** venue 年份. [paper] [pdf] [中译] [解读]` + 作者行；同时在 `scripts/papers.tsv` 登记并将 PDF/笔记放入对应目录。

### [Disclaimer](#content)

- 英文 PDF 均来自 arXiv/会议官网公开渠道，版权归原作者；中文翻译由 [SuperTranslate](https://github.com/asimfish/super_translate) 生成，仅供学习研究，请以英文原文为准。
- venue 标注以调研时检索结果为准，个别预印本的最终发表 venue 可能变化。

### [License](#content)

MIT（仓库结构与笔记文本）。论文 PDF 版权归各自作者与出版方。
