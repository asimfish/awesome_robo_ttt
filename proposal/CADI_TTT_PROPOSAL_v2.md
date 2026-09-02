---
title: "CADI × TTT 研究方案 v2：结构化动作接口作为部署期适应的安全壳"
subtitle: "Structured Action Interfaces as the Safety Shell for Deployment-Time Adaptation"
date: 2026-09-02
---

> **版本说明**。本文取代 `IDEA_REPORT_20260826` 中与 RL 微调稳定性/TTT 相关的部分，保留其约束原生（第二幕）与 SNR 诊断工具的定位。依据：(i) 七臂 CADI 实验全部跑完（robomimic Square，seed 42，200 itr）；(ii) `awesome_robo_ttt` 88 篇文献的系统解读。全文数字均可在 §1 表格或仓库 `notes/` 中找到出处；单 seed 的数字一律标注。

---

## 0. 一页摘要

**发生了什么**。8/26 方案的先导实验是「滤波器等价性杀死测试」：如果导数动作接口（CADI）的收益能被一个匹配带宽的低通滤波器复现，接口主张即死。七臂实验给出的答案是——**在匹配探索噪声预算（σ=0.03）下，泄漏接口 E4 = 95.0%、原版 DPPO E5 = 93.0%、纯积分接口 E1 = 92.0%，差异在单 seed 噪声内**；而未匹配预算时接口崩溃（C 24.5%、E3 12.5%）、原版不崩（A 99.5%）。按预注册判据，「接口提升 RL 微调成功率」的主张在准静态任务上**不成立**；被单变量证实的是一条机理：**积分型接口把上游白噪声染成红噪声（β→2），方差随时间线性增长，直到泄漏（λ<1）或降噪把它拉回**。

**这意味着什么**。接口不是性能助推器，而是一个**可控的扰动整形器**：它对任何上游扰动——RL 探索噪声、或部署期 TTT 的梯度更新——都施加同一个闭式变换，参数 λ 是唯一旋钮。这个属性对 RL 微调（上游扰动可以直接调 σ 抵消）价值有限，但对**部署期适应**正好命中三个死穴：TTT 的更新扰动不可预先调节（崩溃）、必须在闭环里实时发生（延迟）、且改权重的后果需要可证的界（安全）。

**v2 主张**。分层动作接口（冻结生成先验 → 可适应低维接口 → 泄漏积分 + 低层跟踪）是部署期适应的**结构性安全壳**：
(a) 它给出 TTT 更新扰动到执行行为的**闭式传播界**（命题 P2/P3：执行空间的隐式信任域，与上游参数改动量无关）；
(b) 它天然产出**任务耦合的自监督信号**（命题 P4：跟踪残差 = 在线动力学一致性），解决 TTT 目标错配；
(c) 它让权重级 TTT 与免权重路线（DSRL、best-of-N）共享同一低维接口，首次可在同一系统内公平对比。
评测重心从「名义成功率」转向**适应中的伤害**（瞬态偏差、约束违反、jerk、长流稳定性）与**恢复速度**——这正是文献缺口（Category 4 无反应式闭环权重级 TTT 先例；无人给出扰动传播界）。

**P0 免费实验已完成（§1.5）**：P1 在真实策略上成立（接口把执行谱指数从 ≈1 抬到 ≈2.1–2.5）；零适应漂移基线上接口首次显示清晰收益——执行器增益 ×0.8 时 79% vs 原版 42%，观测噪声 σ=0.05 时 78% vs 49%，且执行 jerk 在噪声下保持不变；纯积分臂同样稳健，指向**积分作用抵消乘性执行误差**这一经典机制（新增 H7）。对 P3 的修正：执行空间信任域需 s<1 才实质收紧。

**证伪条件**（§5.5）：若 TTT-on-interface 在动力学漂移上不优于零适应 ≥10 pp，信号主张死；若 TTT-on-raw 的瞬态伤害不高于 TTT-on-interface，结构性安全主张死；若 DSRL 同预算全面持平，权重级 TTT 主张降级。三条判据在实验前写死。

---

## 1. 证据现状：七臂实验与 kill test 裁决

### 1.1 结果总表（robomimic Square，DPPO 微调 200 itr，每 10 itr 评 200 episodes，seed 42）

| 臂 | 接口 | 探索噪声 σ | BC 起点 | 终值 | 读法 |
|---|---|---|---|---|---|
| A | 原版 DPPO（位置域） | 0.10 | 38.0% | **99.5%** | 锚点：此任务上原版不崩 |
| B | 位置域 + 输出低通 | 0.10 | 23.5% | 96.0% | 零假设：滤波本身略伤先验、不伤微调 |
| C | 纯积分 λ=1 + obs_cmd | 0.10 | 43.5% | 24.5% | **崩溃**（噪声积成随机游走） |
| E1 | 同 C | **0.03** | 43.5% | 92.0% | 单变量证实：降噪即恢复 |
| E3 | 泄漏 λ=0.9 | 0.10 | **49.0%** | 12.5% | 泄漏单独不够（先验最好、可训性最差） |
| E4 | 泄漏 λ=0.9 | **0.03** | 49.0% | **95.0%** | 结构 + 预算 |
| E5 | 原版 DPPO | **0.03** | 38.0% | 93.0% | 公平对照：只降噪 |

![七臂学习曲线与 kill-test 读法](figures/E1_seven_arms.png)

### 1.2 被证实的机理（三条）

1. **积分接口放大探索噪声**：C→E1 单变量（只改 σ）从 24.5% 到 92.0%；A→E5 同样改动只从 99.5% 到 93.0%。接口对噪声预算的敏感度远高于原版——与命题 P1 的方差公式 $\mathrm{Var}[c_t]\to s^2\sigma^2 t$（λ=1）一致。
2. **泄漏改善先验、恶化可训性**：E3/E4 的 BC 起点 49.0% 是七臂最高，但 σ=0.1 下 E3 崩得比 C 更彻底（12.5%）。先验质量与 RL 可训性是两个独立维度——泄漏把有效上下文变短，同一 σ 下等效探索更「碎」。
3. **积分器状态必须可观测**：无 obs_cmd 时导数 DP 先验 0%（cmd 不可辨识，POMDP）；加入后恢复到 43.5%。同理，导数标签必须闭环重标注而非开环差分。

### 1.3 被否定的主张（一条）

> 「导数域接口在机理上修复位置域 DP + on-policy RL 的崩溃」——**在 Square 上不成立**：原版 DPPO 根本不崩（99.5%），接口在匹配预算下也无优势（95.0 vs 93.0，单 seed）。8/26 判据「C≤B ⇒ 接口就是个滤波器」触发。

### 1.4 未决问题（两条，转入 v2 实验）

- 接口在**需要平滑/约束的任务**（液体、易碎接触、驾驶舒适）上的价值未测——那里的指标不是成功率而是违规/jerk，白噪探索本身就是伤害。
- 接口在**部署期适应**中的价值未测——那里的扰动源不是可调的 σ 而是不可预调的梯度更新。**v2 以第二条为主线。**

### 1.5 P0 免费实验结果（2026-09-02，已完成）

用七臂的 `state_200.pt` 直接 rollout（每格 100 episodes，评测 seed 与训练评测不同），不做任何适应。脚本 `p0/rollout_record.py` + `DriftWrapper`（`make_figures.py` 同目录 `analyze_p0.py`）。

**P0a · 执行动作频谱（P1 在真实策略上成立）**

![P0a 执行动作 PSD 与谱指数](figures/P0_psd.png)

| 臂 | 成功率(det/stoch) | β̂ 执行 (det/stoch) | β̂ 策略输出 | 平均 jerk (stoch) | 最大单步变化 (stoch) |
|---|---|---|---|---|---|
| A raw σ.10 | 100 / 97 | 1.04 / 0.73 | 1.04 / 0.73 | 0.277 | 0.899 |
| B lowpass σ.10 | 97 / 92 | 2.44 / 2.28 | 0.86 / 0.70 | **0.041** | **0.190** |
| E1 int λ=1 σ.03 | 87 / 74 | 2.49 / 2.30 | 0.59 / 0.44 | 0.136 | 0.793 |
| E4 leak .9 σ.03 | 97 / 87 | 2.09 / 2.06 | 0.32 / 0.31 | 0.137 | 0.795 |
| E5 raw σ.03 | 89 / 84 | 1.06 / 0.90 | 1.06 / 0.90 | 0.181 | 0.774 |

读法：(i) 原版 DPPO 的执行谱天然接近粉噪（β̂≈1）；(ii) 接口臂的执行谱被抬到 β̂≈2.1–2.5（红），而其策略输出反而更白（0.3–0.6）——**执行 = 积分后的策略输出**，P1 的谱整形在学到的策略上定量成立（Δβ̂≈+1.7）；(iii) 接口臂的 jerk 比匹配预算的原版低约 25%（0.137 vs 0.181），但**最大单步变化并不更小**（0.795 vs 0.774）——因为 s=1.0 时 P3 的界 (1−λ)C_max+s≈1.1 并不比原版的 2 紧多少。**对 P3 的修正**：执行空间信任域只有在 s<1 时才实质收紧，s 是安全余量的第二旋钮，须与 BC 先验对齐（§1.2 第 3 条的 scale 教训）联合设计。(iv) 所有臂在 0.25 cyc/step 有尖峰 = 动作块周期（act_steps=4）的重规划不连续，接口臂该峰相对更低。

**P0b · 零适应漂移基线（首次看到接口的清晰收益）**

![P0b 漂移基线](figures/P0_drift.png)

| 漂移 | 强度 | E4 leak | E5 raw | E1 int | E4−E5 | jerk E4 / E5 |
|---|---|---|---|---|---|---|
| 无漂移 | — | 97 | 89 | 87 | +8 | 0.129 / 0.161 |
| 执行器增益 × | 0.9 / 0.8 / 0.7 | 95 / 79 / 25 | 85 / 42 / 5 | 89 / 77 / 43 | +10 / **+37** / +20 | 0.100 / 0.140 (×0.8) |
| 控制延迟（步） | 1 / 2 / 3 | 96 / 84 / 87 | 83 / 78 / 77 | 88 / 83 / 73 | +13 / +6 / +10 | 0.132 / 0.162 |
| 观测噪声 σ | 0.05 / 0.1 / 0.2 | 78 / 18 / 0 | 49 / 6 / 0 | 76 / 22 / 0 | **+29** / +12 / 0 | 0.139 / **0.210→0.417** |
| 物体质量 × | 1.5 / 2 / 3 | 94 / 94 / 95 | 88 / 89 / 89 | 87 / 88 / 94 | +6 / +5 / +6 | 0.132 / 0.166 |
| 接触摩擦 × | 0.7 / 0.5 / 0.3 | 88 / 92 / 98 | 83 / 89 / 91 | 92 / 91 / 90 | +5 / +3 / +7 | 0.132 / 0.166 |

读法：
- **执行器增益漂移**是接口的主场：×0.8 时 +37 pp，×0.7 时原版几乎归零而接口仍有 25%；**纯积分 E1 同样稳健**（77% / 43%）→ 起作用的是积分结构而非泄漏。经典控制的解释是**积分作用抵消乘性执行误差**：接口把策略变成增量域的反馈控制器，观测到状态未达预期就持续累加指令（新增假设 H7，见 §5.4；备择解释：obs_cmd 让策略显式看到「意图指令」从而能检测执行偏差）。
- **观测噪声**：σ=0.05 时 +29 pp；执行 jerk 上接口维持 0.139 不变，原版从 0.21 涨到 0.42——这是 P1「接口滤掉上游噪声」在真实策略上的直接体现，也是 §5.3「适应伤害」指标要抓的现象。
- **延迟** +6~+13；**质量/摩擦**两臂都稳健（Square 的方形螺母质量对任务影响小），差异在噪声内。
- **注意**：单训练 seed；本次评测无漂移时 E4 已领先 8 pp，但增益与观测噪声下的差距（+37/+29）远超该基线差；E1 的同步稳健性是独立于 E4 的第二个证据点。K0（先验对齐）与 K2（结构性伤害）的预判：**均倾向不触发**。

**P0 对方案的影响**：(1) 主线不变，但「结构性安全壳」从纯理论主张升级为有初步经验支撑的主张；(2) 漂移套件里执行器增益与观测噪声应作为主战场，质量/摩擦降为次要；(3) 新增 H7 并把「s 的选择」写进 P3 的设计方程；(4) 5 seeds 复现列为 P2 的第一项。

---

## 2. 重新定位：问题与文献坐标

### 2.1 问题陈述

部署中的机器人策略需要继续学习（分布漂移：物体质量/摩擦、执行器增益、传感退化、光照）。权重级 TTT 的三个死穴（`insights/TRENDS_AND_INSIGHTS.md`）：
- **崩溃**：长时程在线更新几乎必然退化（RDumb），batch=1 流式是最不稳定 regime（SAR）；
- **延迟**：每帧梯度与实时控制预算冲突（Centaur 需异步工程；RoboTTT 需 TTT 层重构骨干）；
- **安全**：改权重 = 运行未认证的新模型，且打开投毒攻击面（DIA）；现有工作对「一次更新最坏能让执行行为偏多少」**没有任何闭式界**。

### 2.2 最近邻与切割

| 最近邻 | 它做了什么 | 它缺什么（我们的切入） |
|---|---|---|
| RoboTTT (2607.15275) | TTT 层入 VLA，30Hz 真机，重建式自监督 | BC 系、桌面准静态；无扰动传播界；适应对象是骨干快权重 |
| Centaur (2503.11650) | 驾驶规划头异步单步 TTT，Cluster Entropy | 非反应式 NAVSIM；无结构性安全垫；改的是 score decoder |
| VANE (2608.09448) | 潜提示 TTT + 提案-验证-提交 | 可靠性靠协议而非结构；无控制层 |
| DSRL (2506.15799) | 噪声空间 RL，基座冻结 | 需在线 RL；不解释扰动如何到达执行器 |
| Neural-Fly (2205.06908) | 末层增益在线适应 + 稳定性证明 | 动力学残差而非策略；无生成先验 |
| PAD (2007.04309) | 逆动力学自监督更新编码器 | 更新范围大（编码器）；无界 |
| REFINE-DP | 联合微调跟踪器降跟踪误差 | 训练期方法；不做部署期适应 |
| ATACOM / Policy Decorator | 约束流形动作空间 / 冻结基座 + 有界残差 | 前者需已知约束几何；后者残差界是超参而非推导 |

**三条稀缺属性**（沿用 8/31 路线图，本文给出形式化）：反应式闭环 + RL 微调后的策略 + 权重级 TTT 无人占坑；扰动传播的**闭式界**无人给出；**免费的任务耦合自监督信号**（跟踪残差）无人用于 TTT。

---

## 3. 方法

### 3.1 三层架构

记观测 $o_t$，冻结的生成先验（DP / 流匹配策略）为 $\pi_\phi$，它输出一个**导数域**动作块 $u_{t:t+H} = \pi_\phi(o_t, c_{t-1}; \theta_a)$，其中 $\theta_a$ 是**接口头**（最后一层 MLP 或一个潜提示向量 $z$）——这是部署期唯一允许更新的参数。接口把导数指令积分成参考指令：

$$c_t = \lambda\, c_{t-1} + s\, \mathrm{clip}(u_t,\,-1,\,1), \qquad \lambda\in(0,1],\ s>0,$$

低层跟踪控制器 $G$（PID / 笛卡尔阻抗，1 kHz）跟踪 $c_t$ 得到执行状态 $x_t$。$c_{t-1}$ 进入观测（obs_cmd，§1.2 第 3 条）。三层的分工：

| 层 | 内容 | 部署期是否更新 | 理由 |
|---|---|---|---|
| L1 感知 + 生成先验 | 视觉编码器、DP 主干 | **冻结** | 安全认证一次；Centaur/PAD/SAR 证据一致指向冻结感知 |
| L2 可适应接口 | 接口头 $\theta_a$（+ 可选潜提示 $z$）、接口参数 $(\lambda, s)$ | **更新 $\theta_a$**；$(\lambda,s)$ 由 §4 设计方程离线定 | 低维、审计面小、回滚 trivial |
| L3 泄漏积分 + 跟踪 | $c_t$ 递推、控制器 $G$ | 冻结 | 结构性安全垫（P2/P3） |

### 3.2 部署期更新规则（TTT-I，Interface-level TTT）

每个控制周期，异步线程执行一步：
$$\theta_a \leftarrow \theta_a - \eta\, \nabla_{\theta_a}\big[\mathcal{L}_{\text{dyn}} + \beta\,\mathcal{L}_{\text{conf}}\big] - \eta\,\rho\, F\odot(\theta_a - \theta_a^{0}),$$
其中 $F$ 为源域 Fisher 对角（EATA 信任域），$\theta_a^0$ 为部署初值；更新在影子副本上计算，**只有当后续 $k$ 步的验证指标（§3.4）不劣化时才提交**（VANE 协议）；每 $N$ 步或触发器熄灭后**硬重置**到 $\theta_a^0$（RDumb 默认开）。与 Centaur 一致：梯度计算与推理并行，不阻塞控制环；单步 + $m$ 帧梯度缓冲平均。

### 3.3 自监督信号（两路，分管两类失败）

**信号一：动力学一致性残差**（管动力学漂移）。执行层给出免费监督：
$$r_t = c_{t-\tau} - \dot{x}_t \quad(\text{速度档})\quad\text{或}\quad r_t = \ddot c_{t-\tau} - \ddot{x}_t \quad(\text{加速度档}),$$
$\tau$ 为跟踪延迟。在分布内、跟踪充分时 $\mathbb{E}[r_t]\approx 0$，其统计漂移是质量/摩擦/增益变化的直接读数（P4）。TTT 损失取 PAD 式逆动力学形态：辅助头 $h$ 从 $(o_t, o_{t+1})$ 预测执行残差，$\mathcal{L}_{\text{dyn}} = \| h(o_t,o_{t+1};\theta_a) - r_t\|^2$——梯度直接流经接口头。

**信号二：决策置信度**（管感知/决策漂移）。DP 采 $N$ 个导数块，按方向聚类计算聚类熵 $\mathcal{H}_{\text{cl}}$（Centaur 的 Cluster Entropy 在导数域的直接移植），$\mathcal{L}_{\text{conf}} = \mathcal{H}_{\text{cl}}$。

**为什么两路都要**：Sentinel 实证一种不确定性度量抓不到所有失败——熵类信号对「自信地做错」是盲区；动力学残差对纯视觉漂移不敏感。两路正交覆盖。

### 3.4 触发与验证

- **触发**（何时开更新）：FAIL-Detect 式——在成功演示上拟合 $(o_t, u_t, r_t)$ 的流式密度，共形预测给出时间变化阈值；密度掉出阈值 **或** $\mathcal{H}_{\text{cl}}$ 超阈值 → 开启 TTT-I。分布内 99% 的时间不更新（消除 EATA/RDumb 都指出的「更新噪声全程存在」问题）。
- **验证**（更新能否提交）：影子副本执行后 $k$ 步的 $|r|$ 均值与 $\mathcal{H}_{\text{cl}}$ 均不高于提交前 → 提交；否则丢弃并计一次「拒绝」。
- **启动**（WSRL 教训）：部署开始先以影子模式跑 $T_0$ 步收集统计量，校准密度与阈值，再允许更新。

### 3.5 安全壳（三层）

1. **结构性**（本文贡献）：P2 给出执行偏差的闭式上界，P3 给出执行空间的隐式信任域——**与 $\theta_a$ 改了多少无关**。
2. **算法性**：Fisher 信任域（EATA）+ 周期重置（RDumb）+ 提案-验证-提交（VANE）+ 触发式（Centaur/VLA-ATTC）。
3. **兜底**：用失败 rollout 训 $Q_{\text{risk}}$（Recovery RL），超阈值切保守策略；低层控制器限幅与紧急停止始终在线。

### 3.6 训练期预埋（不做即失败——洞见 D）

- 辅助头 $h$ 与策略联合训练（PAD/TTT 的必要条件）；
- RL 微调末期加元学习外环：每条 rollout 先做内环 TTT-I 更新、再以更新后的策略算 RL 损失优化初始化（TTT-E2E 配方：只更 MLP、内环 mini-batch）；
- $\lambda$ 课程：训练期从 $\lambda_{\text{train}}$ 渐进到部署值，避免 E3 式「先验好、可训性差」的错配。

---

## 4. 理论：四个命题

> P1–P3 是线性系统事实而非实验主张；它们的作用是把「接口更安全」从经验声明变成**可验证的界与设计方程**。数值验证见图 T1/T2（合成，`proposal/make_figures.py`）。

**记号**。上游扰动序列 $\delta u_t$（探索噪声或 TTT 更新引起的输出变化），接口 $c_t=\lambda c_{t-1}+s\,u_t$（略去 clip，clip 只会收紧所有界），跟踪控制器闭环脉冲响应 $g_k$，$\|g\|_1=\sum_k|g_k|<\infty$（稳定）。

### P1 谱整形（explains Arm C / E1 / E3）

若 $\delta u_t$ 为白噪声（方差 $\sigma^2$），则 $\delta c_t$ 的功率谱为
$$S_c(f)=\frac{s^2\sigma^2}{|1-\lambda e^{-i2\pi f}|^2}=\frac{s^2\sigma^2}{1-2\lambda\cos 2\pi f+\lambda^2},$$
稳态方差 $\mathrm{Var}[\delta c]=s^2\sigma^2/(1-\lambda^2)$（$\lambda<1$）；$\lambda=1$ 时 $\mathrm{Var}[\delta c_t]=s^2\sigma^2 t$ 无界（随机游走）。低频段谱指数 $\beta(\lambda)$ 从 0（$\lambda=0$，白）单调升至 2（$\lambda\to1$，红）。**推论**：$\lambda$ 是探索/适应噪声的「颜色旋钮」；Pink Noise（ICLR 2023）的最优 $\beta\approx1$ 对应 $\lambda\approx0.7$（图 T1b 数值拟合 $\hat\beta=0.89$）。E3/E4 用的 $\lambda=0.9$ 对应 $\hat\beta\approx1.6$——偏红，这为「E3 先验最好但可训性最差」提供了一个可检验的解释（§5.4 H3）。

![P1 数值验证](figures/T1_spectrum_shaping.png)

### P2 有界传播（TTT 单步伤害界）

若 $|\delta u_t|\le\Delta\ \forall t$（TTT 更新引起的输出变化有界——由信任域或 clip 保证），则
$$|\delta c_t|\le \frac{s\Delta}{1-\lambda}\quad\text{且}\quad |\delta x_t|\le \|g\|_1\frac{s\Delta}{1-\lambda}\qquad(\lambda<1),$$
证明：$\delta c_t=s\sum_{k\ge0}\lambda^k\delta u_{t-k}$，取绝对值求和几何级数；$\delta x=g*\delta c$ 用 Young 不等式。$\lambda=1$ 时界为 $s\Delta t$，随时间线性增长。**设计方程**：给定安全余量 $M$（允许的最大执行偏差），选 $(\lambda,s)$ 使 $\|g\|_1 s\Delta/(1-\lambda)\le M$。图 T2 展示 $\Delta=0.05$ 的持续偏置在 $\lambda\in\{1,0.97,0.9,0.7\}$ 下的传播。

![P2 数值验证](figures/T2_bounded_propagation.png)

### P3 执行空间的隐式信任域

相邻执行指令之差
$$|c_t-c_{t-1}|=|(\lambda-1)c_{t-1}+s\,u_t|\le(1-\lambda)|c_{t-1}|+s\,|u_t|\le(1-\lambda)C_{\max}+s,$$
**与上游策略参数的改动量无关**。**但注意**（P0a 修正）：该界的松紧由 s 决定——s=1 时界为 ≈1.1，与原版的 2 相差不大（实测最大单步变化 0.795 vs 0.774）；要让执行空间信任域实质收紧必须 s<1，而 s 又受 BC 先验对齐约束（§1.2），因此 (λ, s) 须作为一对联合设计。对比：TRPO/PPO/EATA 约束的是参数或分布空间的改动（$\mathrm{KL}$、Fisher 范数），本接口约束的是**执行空间**的改动——TTT 可以在上游做激进更新，执行行为的单步变化仍被结构性封顶。这是「安全壳」的精确含义：安全性质由 L3 的线性结构保证，不依赖 L2 更新的良好行为。

### P4 残差信号的可识别性

设真实执行动力学为 $\dot x_t = c_{t-\tau}+w_t(\vartheta)$，$w_t(\vartheta)$ 为由物理参数 $\vartheta$（质量、摩擦、增益）决定的未建模项。则残差 $r_t = -w_t(\vartheta)$ 经控制器带宽滤波后是 $\vartheta$ 漂移的充分统计量的低通版本：$\mathbb{E}[r_t]$ 在分布内为零、在漂移后偏移量与 $\|\vartheta-\vartheta_0\|$ 同阶（一阶展开）。因此 (i) $r_t$ 的统计漂移是动力学分布偏移的**直接检测器**（比视觉密度更早、更专一），(ii) 以 $r_t$ 为目标的 TTT 梯度与任务目标高度相关（TTT++ 的相关性条件），(iii) $r_t$ 对纯视觉漂移不响应——正是需要信号二的原因。

### 与探索文献的关系（用于论文理论段）

Pink Noise 证明 $\beta\approx1$ 的探索噪声在连续控制上最优；gSDE 从噪声生成端做平滑；Q-Chunking 靠分块获得时间相关性。P1 表明积分接口在**执行端**做同一件事，且 $\lambda$ 给出连续可调的 $\beta$。三者可叠加，也可互为对照：若 P1 成立，则「原版 DPPO + 粉噪探索」应能复现 E4 的效果——这是 §5.6 的一条消融。

---

## 5. 实验方案（预注册）

### 5.1 平台与部署漂移套件

**主平台**：robomimic（Square、Transport、ToolHang），MuJoCo 2.3.2，DPPO 代码栈（已在 `dppo/` 上跑通七臂）。**驾驶延伸**：Bench2Drive（CARLA，反应式闭环）作为 Phase D。

**部署漂移套件 $\mathcal{D}$**（每项三档强度，部署时才施加，训练期不可见）：

| 类别 | 漂移 | 命中的信号 |
|---|---|---|
| 动力学 | 物体质量 ×{1.5, 2, 3}；接触摩擦 ×{0.7, 0.5, 0.3} | 残差 $r_t$ |
| 执行器 | 关节增益 ×{0.9, 0.8, 0.7}；控制延迟 +{1, 2, 3} 步 | 残差 $r_t$ |
| 感知 | 观测噪声 σ_obs ×{2, 4, 8}；相机偏移/光照（图像任务） | 聚类熵 |
| 复合 | 上述随机组合，按 CCC 方式平滑连续切换（长流） | 两者 |

### 5.2 方法臂

| 臂 | 说明 | 回答 |
|---|---|---|
| M0 冻结 | 无适应（E4/E5 checkpoint 直接部署） | 漂移伤害基线 |
| M1 TTT-raw | 原版策略，更新末端 MLP，$\mathcal{L}_{\text{dyn}}$（预测本体下一状态）+ $\mathcal{L}_{\text{conf}}$ | 无接口的权重级 TTT |
| M2 TTT-I（本文） | 接口头 $\theta_a$ 更新，§3.2 全套（触发 + 信任域 + 重置 + 验证） | 主方法 |
| M3 TTT-I−shell | M2 去掉信任域/重置/验证（裸梯度） | 结构性 vs 算法性安全的贡献分解 |
| M4 DSRL | 冻结策略 + 噪声空间 RL（同交互预算） | 免权重「会学习」路线 |
| M5 best-of-N+critic | N=16 采样 + IQL critic 重排 | 免权重不学习路线 |
| M6 RMA-style | 前馈推断动力学隐变量（训练期域随机化） | 免梯度对照 |
| M7 Oracle | 在漂移环境上重新微调到收敛 | 上界 |

### 5.3 指标（四组，缺一不可）

1. **适应收益**：成功率随适应步数的恢复曲线；到达 M0+10 pp 所需步数（恢复速度）。
2. **适应伤害**（本文重心）：适应期间执行指令的最大单步变化 $\max_t|c_t-c_{t-1}|$、jerk 均值、约束违反次数（接触力峰值 / 工作空间越界 / 速度上限）、最坏 episode 的偏差 $\max_t|\delta x_t|$——与 P2/P3 的界并列报告（**界是否被违反是可直接检验的**）。
3. **长流稳定性**（RDumb 协议）：10 万步连续漂移流上的成功率轨迹、适应增益的衰减曲线、崩溃次数、重置触发次数。
4. **系统开销**：更新触发率、每次更新的墙钟、验证拒绝率、推理延迟 P99。

### 5.4 假设与预注册预测

| # | 假设 | 预测（写死） |
|---|---|---|
| H1 | 动力学漂移下 TTT-I 显著优于冻结 | M2 − M0 ≥ 10 pp（质量/摩擦/增益档 2 以上），5 seeds 均值，95% CI 不含 0 |
| H2 | 接口结构降低适应伤害 | M2 的 $\max|c_t-c_{t-1}|$ 与违规次数低于 M1；M3（去算法壳）仍低于 M1——**结构性贡献独立于算法壳** |
| H3 | P1 的颜色解释 | 执行动作实测 PSD 的 $\hat\beta$ 随 $\lambda$ 单调；$\lambda\approx0.7$ 附近 RL 可训性最佳（补 λ∈{0.5,0.7,0.8,0.9,0.95} 扫描） |
| H4 | 残差信号专一性 | $r_t$ 统计量在动力学漂移下先于视觉密度报警；在纯感知漂移下不报警（P4） |
| H5 | 长流下重置不可省 | M2 在 10 万步流上无崩溃；M3 出现 ≥1 次崩溃（RDumb 复现） |
| H6 | 与 DSRL 的关系 | 同预算下 M2 恢复速度 ≥ M4；DSRL 伤害指标与 M2 相当（同享接口） |
| H7 | 积分作用抵消执行器增益漂移（P0b 观察） | 5 seeds 下增益 ×0.8 时接口臂（E1/E4 型）比匹配原版高 ≥15 pp；去掉 obs_cmd 的接口臂若同样稳健，则机制归于积分结构而非可观测意图 |

### 5.5 Kill 判据（任一触发即按写定路径转向）

- **K1**（信号）：H1 不成立 → 残差信号不足以驱动适应 → 保留 P1–P3 作分析章节，论文转「适应扰动的谱整形与传播界」（理论 + 诊断工具型）。
- **K2**（结构）：H2 不成立（M1 的伤害 ≤ M2） → 结构性安全主张死 → 只剩算法壳（无新意），并入 DSRL 路线做「接口 for DSRL」。
- **K3**（必要性）：H6 中 M4 在全部指标持平或更好 → 权重级 TTT 非必要 → 论文改为 DSRL 上的接口研究（仍可发，主张弱一档）。
- **K0**（先验对齐）：任一任务上接口 BC 起点低于原版 ≥15 pp → 该任务退出主表（8/26 匹配先验协议）。

### 5.6 消融

- $\lambda$ 扫描（H3）×动作块长度 $H\in\{4,8,16\}$（Q-Chunking 交叉）；
- 触发式 vs 常开式更新（误触发代价）；
- 两路信号各自单独 vs 联合；
- 元学习预埋有/无（§3.6）；
- 原版 DPPO + 粉噪探索（$\beta=1$）vs E4（P1 的反向验证）；
- 价值侧校准（Cal-QL）× 接口 的 2×2，剥离 on-policy 早期崩溃的两个机制。

### 5.7 统计

≥5 seeds/臂；报告均值 ± 95% bootstrap CI；成功率用 200 episodes/评测点；伤害指标报最坏 episode 与分位数。**七臂现有数字全部为单 seed，在 v2 中只作动机，不作证据。**

### 5.8 算力与时间表（服务器 4×GPU，当前七臂已释放）

| 阶段 | 内容 | 成本 | 时间 |
|---|---|---|---|
| **P0 免费实验（已完成 09-02）** | E4/E5/E1 checkpoint 在 $\mathcal{D}$ 上的零适应退化（M0）+ 七臂执行动作 PSD 实测 → §1.5 | 纯评测（59 组 rollout，<1 h） | 已完成 |
| P1 信号与触发 | 实现辅助头/残差/密度/共形阈值；H4 单独验证 | 小 | 1 周 |
| P2 主对比 | M0–M6 × 2 任务 × 3 类漂移 × 5 seeds（适应期短，每 run ≤1 h） | ~180 GPU·h | 1.5 周 |
| P3 长流 | M2/M3/M4 × 10 万步 CCC 式流 × 3 seeds | ~100 GPU·h | 1 周 |
| P4 消融 + 元学习预埋 | §5.6；预埋需重训 ≈ 6 × 12 h | ~150 GPU·h | 1.5 周 |
| P5 驾驶延伸（可选） | Bench2Drive 上 M0/M2/M5 | 视资源 | 2 周 |

K0 在 P0 结束时判定；K1/K2 在 P2 结束时判定；K3 在 P3 结束时判定。

---

## 6. 论文骨架

**标题候选**
1. *Structured Action Interfaces as a Safety Shell for Test-Time Training of Robot Policies*
2. *Adapt Upstream, Execute Smoothly: Bounded-Harm Test-Time Training via Leaky-Integrator Action Interfaces*
3. *When TTT Meets the Controller: Spectrum Shaping and Harm Bounds for Deployment-Time Policy Adaptation*

**摘要草稿**（英）
> Deployed robot policies must keep learning, yet test-time training (TTT) of a policy's weights is fragile: updates can collapse over long horizons, compete with real-time control, and change executed behavior by amounts no one can bound. We show that *where* a policy is allowed to change matters as much as *how*. We freeze the perception and generative prior, adapt only a low-dimensional interface head, and route its derivative-domain output through a leaky integrator tracked by a low-level controller. This structure yields (i) a closed-form bound on how far any bounded upstream update can move the executed trajectory, independent of the parameter change; (ii) an implicit trust region in execution space; and (iii) a free, task-coupled self-supervised signal—the tracking residual—whose drift both detects dynamics shift and drives adaptation. The same interface also colors exploration noise with a single knob λ, recovering the known pink-noise optimum. On robomimic tasks under deployment-time dynamics and perception shifts, interface-level TTT recovers most of the lost performance while incurring substantially less transient harm than TTT on the raw policy, and remains stable over 100k-step drift streams where unshielded TTT collapses. We release a deployment-shift benchmark and the design equations for choosing λ.

**贡献三条**
1. 分层动作接口作为 TTT 安全壳的形式化：P1–P3（谱整形、有界传播、执行空间信任域）与 $\lambda$ 设计方程。
2. 任务耦合的两路自监督 TTT（残差 + 聚类熵）与触发-验证-提交协议，在反应式闭环上首个权重级 TTT 系统研究（含与 DSRL/best-of-N/RMA 的同接口公平对比）。
3. 部署漂移基准 + 「适应伤害」评测协议（瞬态偏差、违规、长流衰减曲线），以及一个诚实的负结果：接口不提升准静态任务的名义 RL 微调成功率。

**章节**：1 引言 → 2 相关工作（TTA/TTT 基础；机器人部署适应；免权重 steering；接口/残差/约束动作空间）→ 3 方法（§3）→ 4 理论（§4）→ 5 实验（§5）→ 6 讨论（负结果、λ 的选择、与 RoboTTT/DSRL 的组合、驾驶延伸）→ 7 局限。

**图表清单**：Fig1 三层架构与两路信号；Fig2 P1/P2 数值验证（现成）；Fig3 七臂动机图（现成，标注单 seed）；Fig4 漂移套件恢复曲线（M0–M6）；Fig5 适应伤害 vs P2 界；Fig6 长流稳定性；Fig7 λ 扫描与 PSD；Tab1 最近邻切割；Tab2 主结果；Tab3 消融。

---

## 7. 风险登记与预案

| 风险 | 概率 | 预案 |
|---|---|---|
| 残差信号在 robomimic 的低阻抗仿真里太小（跟踪太好） | 中 | 增大漂移强度档；改用加速度档残差；或转 Transport（负载大） |
| 触发器误触发率高，常开与触发式无差 | 中 | 共形阈值放宽 + 用拒绝率调参；最坏退回常开 + 重置 |
| TTT-I 与 TTT-raw 伤害指标无差（K2） | 中 | 提前用 P0 的 PSD 实测预判：若接口执行谱与原版无差，K2 大概率触发，立即转 K2 路径 |
| DSRL 同预算全面持平（K3） | 中高 | 已写定降级路径；DSRL 本身也吃接口红利，仍是正结果 |
| 元学习预埋训练不稳（TBPTT） | 中 | 只更 MLP、内环 mini-batch（TTT-E2E）；实在不稳则去掉预埋作为消融项报告 |
| 单 seed 结论翻转 | 高 | v2 全部结论以 5 seeds 为准；现有七臂只作动机 |
| 审稿人：「这就是低通滤波/残差策略」 | 高 | P3 给出与低通的本质区别（对上游参数变化的不变性）；Policy Decorator 的残差界是超参、我们是推导；实验含滤波匹配臂 |

---

## 8. 与 8/26 方案的差异对照

| 项 | 8/26（IDEA_REPORT） | v2（本文） | 变更原因 |
|---|---|---|---|
| 核心主张 | 导数接口在机理上修复 DP+RL 崩溃 | 接口是部署期适应的结构性安全壳 | kill test：匹配预算下 E4≈E5 |
| TTT 地位 | I8 被杀（撞 RoboTTT） | 主线 | 88 篇地图给出差异化：适应对象/信号/界/闭环设定全部不同 |
| 理论 | 谱整形叙述性 | P1–P4 命题 + 数值验证 + 设计方程 | 把「更安全」变成可检验的界 |
| 主指标 | 成功率、崩溃率 | 适应伤害 + 恢复速度 + 长流稳定性 | 接口的价值不在名义性能 |
| 先导实验 | 滤波器等价性四臂 | 部署漂移套件 M0–M7 | 前者已完成并给出裁决 |
| 约束原生第二幕 | 保留 | 保留（不变） | 未受本轮影响 |
| SNR 诊断工具 | 分析章节 | 分析章节（不变） | 未受本轮影响 |

---

## 附录 A · 符号

$o_t$ 观测；$\pi_\phi$ 冻结先验；$\theta_a$ 接口头；$u_t$ 导数指令；$c_t$ 参考指令；$\lambda$ 泄漏；$s$ 尺度；$G, g_k$ 跟踪控制器及其脉冲响应；$x_t$ 执行状态；$r_t$ 残差；$\mathcal{H}_{\text{cl}}$ 聚类熵；$F$ Fisher 对角；$\Delta$ 上游扰动界；$M$ 安全余量。

## 附录 B · 实现入口

- 接口与数据：`s2drive_proposal/embodied/exp/derivative_action.py`（`DerivativeActionWrapper`：`off/lowpass/integrate`、`obs_cmd`、`leak`）、`make_derivative_dataset.py`（闭环重标注）、`replay_scale_check.py`、`probe_prior.py`。
- 服务器：`/home/dataset-local/liyufeng/cadi/`（七臂日志 `run_*.log`、checkpoint 在 `dppo/log/`）。
- 已实现（P0）：`dppo/env/gym_utils/wrapper/drift.py`（`DriftWrapper`：执行动作记录 + 增益/延迟/观测噪声/质量/摩擦漂移）、`p0/rollout_record.py`（checkpoint rollout 记录）、`p0/run_p0_batch.sh`、本地 `analyze_p0.py`（PSD/β̂/jerk/漂移表）。
- 待实现：`ttt_interface.py`（异步更新线程 + 影子副本 + 验证提交）、`signals.py`（残差/聚类熵/密度+共形）、`harm_metrics.py`（把 P0 的 jerk/最大单步变化正式化）。
- 图：`proposal/make_figures.py`。

## 附录 C · 本方案依赖的文献（均在 `awesome_robo_ttt/notes/`）

TTT 形态与安全壳：RoboTTT、Centaur、VANE、TTT-E2E、EATA、RDumb、SAR、DIA。信号：PAD、TTT++、TT-VLA、Sentinel、FAIL-Detect、SAFE。接口与控制：Neural-Fly、RMA、ORPA、Policy Decorator（README 另见）。探索谱：Pink Noise、gSDE、Q-Chunking、DPPO。对照路线：DSRL、IDQL、RoboMonkey。稳定性：RLPD、Cal-QL、WSRL。评测：RDumb（CCC）、AR-TTA、Bench2Drive。
