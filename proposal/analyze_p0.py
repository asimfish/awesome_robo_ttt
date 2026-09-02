"""P0 analysis: (a) executed-action spectra per arm, (b) zero-adaptation drift baselines.
Input: p0_out/*.npz downloaded from the server. Output: figures/P0_*.png + p0_results.md"""
import glob, os, re, json
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import welch

D = "p0_out"
ARMS = ["A", "B", "C", "E1", "E3", "E4", "E5"]
LAB = {"A": "A raw σ.10", "B": "B lowpass σ.10", "C": "C int λ=1 σ.10", "E1": "E1 int λ=1 σ.03",
       "E3": "E3 leak .9 σ.10", "E4": "E4 leak .9 σ.03", "E5": "E5 raw σ.03"}
COL = {"A": "#7f8c8d", "B": "#2980b9", "C": "#c0392b", "E1": "#e67e22", "E3": "#8e44ad", "E4": "#16a085", "E5": "#2c3e50"}
BAND = (0.02, 0.3)  # cycles per control step (20 Hz control → 0.4–6 Hz)

def load(name):
    p = f"{D}/{name}.npz"
    if not os.path.exists(p): return None
    d = np.load(p, allow_pickle=True)
    eps = []
    for u, ex, r in zip(d["u"], d["exec"], d["reward"]):
        eps.append(dict(u=np.asarray(u, dtype=np.float32), ex=np.asarray(ex, dtype=np.float32), r=np.asarray(r, dtype=np.float32)))
    return dict(eps=eps, success=np.asarray(d["success"], dtype=np.float32))

def psd_stats(eps, key="ex", dims=(0, 1, 2)):
    """average Welch PSD over episodes & dims; fitted slope β in BAND; smoothness metrics."""
    Ps = []; jerk = []; step = []
    for e in eps:
        x = e[key][:, list(dims)]
        if len(x) < 64: continue
        for j in range(x.shape[1]):
            f, P = welch(x[:, j] - x[:, j].mean(), nperseg=128, fs=1.0)
            Ps.append(P)
        d1 = np.diff(x, axis=0); jerk.append(np.mean(np.abs(np.diff(d1, axis=0)))); step.append(np.max(np.abs(d1)))
    P = np.mean(Ps, 0); m = (f >= BAND[0]) & (f <= BAND[1])
    beta = -np.polyfit(np.log(f[m]), np.log(P[m]), 1)[0]
    return f, P, beta, float(np.mean(jerk)), float(np.mean(step))

rows = []; fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
for mode, a in (("det", ax[0]), ("stoch", ax[1])):
    for arm in ARMS:
        r = load(f"psd_{arm}_{mode}")
        if r is None: continue
        f, P, beta, jerk, mstep = psd_stats(r["eps"], "ex")
        _, Pu, beta_u, _, _ = psd_stats(r["eps"], "u")
        rows.append(dict(arm=arm, mode=mode, success=float(r["success"].mean()), beta_exec=beta, beta_u=beta_u, jerk=jerk, max_step=mstep, n=len(r["eps"])))
        a.loglog(f[1:], P[1:], color=COL[arm], lw=2 if arm in ("E4", "E5") else 1.2, label=f"{LAB[arm]}  β̂={beta:.2f}")
    a.set_title(f"P0a  PSD of executed position command ({'deterministic' if mode=='det' else 'stochastic'} policy)", fontsize=9.5)
    a.set_xlabel("cycles / control step"); a.set_ylabel("PSD"); a.legend(fontsize=7); a.axvspan(*BAND, color="#000", alpha=0.04)
# panel 3: β̂ and jerk bars for stoch mode
st = [x for x in rows if x["mode"] == "stoch"]
if st:
    xs = np.arange(len(st)); a = ax[2]
    a.bar(xs - 0.2, [x["beta_exec"] for x in st], 0.4, color=[COL[x["arm"]] for x in st], label="β̂ (executed)")
    a.bar(xs + 0.2, [x["beta_u"] for x in st], 0.4, color="#bdc3c7", label="β̂ (policy output u)")
    a.set_xticks(xs); a.set_xticklabels([x["arm"] for x in st]); a.set_ylabel("spectral exponent β̂"); a.legend(fontsize=8)
    a.set_title("P0a  spectral exponent: executed vs policy output (stochastic)", fontsize=9.5)
    a.axhline(1.0, ls="--", color="#e67e22", lw=1)
plt.tight_layout(); plt.savefig("figures/P0_psd.png", dpi=160); plt.close()

# ---- drift baselines ----
drift_types = [("gain", [0.9, 0.8, 0.7], "actuator gain ×"), ("delay", [1, 2, 3], "control delay (steps)"),
               ("obs", [0.05, 0.1, 0.2], "obs noise std (normalized)"), ("mass", [1.5, 2.0, 3.0], "object mass ×"),
               ("fric", [0.7, 0.5, 0.3], "contact friction ×")]
drift_rows = []
fig, ax = plt.subplots(1, 5, figsize=(17, 3.6), sharey=True)
for k, (dt, levels, xlabel) in enumerate(drift_types):
    for arm in ("E4", "E5", "E1"):
        nom = load(f"psd_{arm}_det"); base = float(nom["success"].mean()) if nom else np.nan
        ys = [base]; xs_lab = ["nominal"]; harm = []
        for lv in levels:
            name = f"drift_{arm}_{dt}{lv}"
            r = load(name)
            if r is None: ys.append(np.nan); xs_lab.append(str(lv)); continue
            s = float(r["success"].mean()); ys.append(s); xs_lab.append(str(lv))
            _, _, _, jerk, mstep = psd_stats(r["eps"], "ex")
            drift_rows.append(dict(arm=arm, drift=dt, level=lv, success=s, delta=s - base, jerk=jerk, max_step=mstep, n=len(r["eps"])))
        ax[k].plot(range(len(ys)), np.array(ys) * 100, marker="o", color=COL[arm], label=LAB[arm], lw=2 if arm != "E1" else 1.2, ls="-" if arm != "E1" else "--")
    ax[k].set_xticks(range(len(levels) + 1)); ax[k].set_xticklabels(xs_lab, fontsize=8); ax[k].set_xlabel(xlabel); ax[k].set_title(f"P0b  {dt}", fontsize=10)
    ax[k].set_ylim(0, 102)
ax[0].set_ylabel("success (%)  zero adaptation, 100 ep"); ax[0].legend(fontsize=7.5)
plt.tight_layout(); plt.savefig("figures/P0_drift.png", dpi=160); plt.close()

# ---- markdown summary ----
with open("p0_results.md", "w", encoding="utf-8") as fo:
    fo.write("### P0a 执行动作频谱（100 episodes/臂，位置维 0–2，Welch nperseg=128，β̂ 拟合带 0.02–0.3 cyc/step）\n\n")
    fo.write("| 臂 | 模式 | 成功率 | β̂ 执行 | β̂ 策略输出 | 平均 jerk | 最大单步变化 |\n|---|---|---|---|---|---|---|\n")
    for x in rows:
        fo.write(f"| {LAB[x['arm']]} | {x['mode']} | {x['success']*100:.1f}% | {x['beta_exec']:.2f} | {x['beta_u']:.2f} | {x['jerk']:.4f} | {x['max_step']:.3f} |\n")
    fo.write("\n### P0b 零适应漂移基线（确定性策略，100 episodes/格；Δ = 相对各臂无漂移成功率）\n\n")
    fo.write("| 臂 | 漂移 | 强度 | 成功率 | Δ | 平均 jerk | 最大单步变化 |\n|---|---|---|---|---|---|---|\n")
    for x in drift_rows:
        fo.write(f"| {x['arm']} | {x['drift']} | {x['level']} | {x['success']*100:.1f}% | {x['delta']*100:+.1f} | {x['jerk']:.4f} | {x['max_step']:.3f} |\n")
json.dump(dict(psd=rows, drift=drift_rows), open("p0_results.json", "w"), indent=1)
print("psd rows:", len(rows), "drift rows:", len(drift_rows))
