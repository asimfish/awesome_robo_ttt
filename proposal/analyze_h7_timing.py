"""Why does the interface arm survive actuator-gain drift? Test the 'speed headroom' explanation.

Episodes always run to 400 env steps (no early termination), success = any reward > 0.
Time-to-success T = first chunk index with reward > 0 (x act_steps=4 for env steps).
If both arms simply slow down by 1/g and the horizon is the binding constraint, then
  T_drift ? T_nodrift / g  and  success(g) ? P[T_nodrift / g < 400].
We also inspect gripper-close timing (first u[6] > 0) as a proxy for the grasp phase.
"""
import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = "p0_out"
ACT = 4
H = 400


def load(name):
    p = f"{D}/{name}.npz"
    if not os.path.exists(p):
        return None
    d = np.load(p, allow_pickle=True)
    return dict(success=np.asarray(d["success"], np.float32),
                reward=[np.asarray(r, np.float32) for r in d["reward"]],
                u=[np.asarray(x, np.float32) for x in d["u"]])


def tts(rw):
    idx = np.nonzero(rw > 0)[0]
    return (idx[0] + 1) * ACT if len(idx) else np.nan


def first_close(u):
    idx = np.nonzero(u[:, 6] > 0)[0]
    return idx[0] if len(idx) else np.nan


out = {}
print(f"{'arm':<4}{'cond':<9}{'succ%':>6}  {'T50':>5} {'T90':>5} {'Tmax':>5}  {'grasp50':>7}  {'noGrasp%':>8}")
for arm in ("E4", "E5", "A", "B"):
    pref = f"p1_{arm}_ad0" if arm in ("E4", "E5") else f"ctrl_{arm}"
    for c in ("nodrift", "gain0.8", "gain0.7", "delay2"):
        T, G, S = [], [], []
        for s in (1000, 2000, 3000):
            r = load(f"{pref}_{c}_s{s}")
            if r is None:
                continue
            S += list(r["success"])
            T += [tts(rw) for rw in r["reward"]]
            G += [first_close(u) for u in r["u"]]
        if not S:
            continue
        T = np.asarray(T); G = np.asarray(G)
        ok = ~np.isnan(T)
        q = np.nanpercentile(T[ok], [50, 90, 100]) if ok.any() else [np.nan] * 3
        g50 = np.nanmedian(G)
        nog = 100 * np.mean(np.isnan(G))
        out[f"{arm}_{c}"] = dict(success=100 * float(np.mean(S)), T50=float(q[0]), T90=float(q[1]),
                                Tmax=float(q[2]), grasp50=float(g50), no_grasp_pct=float(nog),
                                T_all=[float(x) for x in T])
        print(f"{arm:<4}{c:<9}{100*np.mean(S):6.1f}  {q[0]:5.0f} {q[1]:5.0f} {q[2]:5.0f}  {g50:7.0f}  {nog:8.1f}")

# headroom prediction: success(g) predicted from nodrift T distribution assuming T/g
print("\n== speed-headroom prediction:  P[T_nodrift / g <= 400] vs observed ==")
for arm in ("E4", "E5", "A", "B"):
    k = f"{arm}_nodrift"
    if k not in out:
        continue
    T0 = np.asarray(out[k]["T_all"])
    for g in (0.8, 0.7):
        kk = f"{arm}_gain{g}"
        if kk not in out:
            continue
        pred = 100 * np.mean(np.nan_to_num(T0, nan=1e9) / g <= H)
        print(f"{arm} gain x{g}:  predicted {pred:5.1f}%   observed {out[kk]['success']:5.1f}%   "
              f"(nodrift T50={out[k]['T50']:.0f}, T90={out[k]['T90']:.0f})")

# figure: time-to-success CDFs
fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
COL = {"E4": "#16a085", "E5": "#2c3e50", "A": "#7f8c8d", "B": "#8e44ad"}
LS = {"nodrift": "-", "gain0.8": "--", "gain0.7": ":"}
for arm in ("E4", "E5"):
    for c in ("nodrift", "gain0.8", "gain0.7"):
        k = f"{arm}_{c}"
        if k not in out:
            continue
        T = np.asarray(out[k]["T_all"]); T = np.where(np.isnan(T), 1e9, T)
        xs = np.arange(0, H + 1, 4)
        cdf = [np.mean(T <= x) for x in xs]
        ax[0].plot(xs, 100 * np.asarray(cdf), color=COL[arm], ls=LS[c], lw=1.6,
                   label=f"{arm} {'interface' if arm=='E4' else 'raw'} - {c}")
ax[0].axvline(H, color="#c0392b", lw=1, ls="-.")
ax[0].set_xlabel("env steps"); ax[0].set_ylabel("cumulative success (%)")
ax[0].set_title("Time-to-success CDF under actuator-gain drift (frozen, 3 eval seeds)", fontsize=9.5)
ax[0].legend(fontsize=7); ax[0].set_ylim(0, 100)
# predicted vs observed bars
labels, pred, obs = [], [], []
for arm in ("E4", "E5", "A", "B"):
    k = f"{arm}_nodrift"
    if k not in out:
        continue
    T0 = np.asarray(out[k]["T_all"])
    for g in (0.8, 0.7):
        kk = f"{arm}_gain{g}"
        if kk in out:
            labels.append(f"{arm}\nx{g}")
            pred.append(100 * np.mean(np.nan_to_num(T0, nan=1e9) / g <= H))
            obs.append(out[kk]["success"])
x = np.arange(len(labels)); w = 0.38
ax[1].bar(x - w / 2, pred, w, color="#bdc3c7", label="predicted by speed headroom (T0/g <= 400)")
ax[1].bar(x + w / 2, obs, w, color=[COL[l.split('\n')[0]] for l in labels], label="observed")
ax[1].set_xticks(x); ax[1].set_xticklabels(labels, fontsize=8); ax[1].set_ylabel("success (%)")
ax[1].set_title("Does slowing alone explain the drop?", fontsize=9.5); ax[1].legend(fontsize=7); ax[1].set_ylim(0, 105)
plt.tight_layout(); os.makedirs("figures", exist_ok=True)
plt.savefig("figures/H7_timing.png", dpi=160); plt.close()
json.dump({k: {kk: vv for kk, vv in v.items() if kk != "T_all"} for k, v in out.items()},
          open("h7_timing_results.json", "w"), indent=1)
print("saved figures/H7_timing.png")
