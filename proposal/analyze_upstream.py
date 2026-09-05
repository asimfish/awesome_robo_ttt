# -*- coding: utf-8 -*-
"""Upstream vs downstream compensation (P1' proper) and controlled adaptation noise, 3 eval seeds.

p1v_{arm}_ad{1,2}_{cond}_s{seed}: 1/ghat applied on the policy output (upstream of the interface), all non-gripper dims
p1u_*: first upstream batch, position dims only (rotation gain left uncompensated) -> superseded
p1_{E4}_ad*/p1_B_ad*: 1/ghat applied on the executed command (downstream)  [from P1' / armB batches]
cn_{arm}_{up|down}_sig{s}_s{seed}, cn_A_sig{s}_s{seed}: white multiplicative noise (1+eps) on position dims
Writes figures/P1_upstream.png and upstream_results.md/json.
"""
import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = "p0_out"
SEEDS = [1000, 2000, 3000]
UP = os.environ.get("UP_PREFIX", "p1v")  # p1u_ = first batch (position-only upstream scaling, invalid); p1v_ = all non-gripper dims
COL = {"E4": "#16a085", "B": "#8e44ad", "A": "#c0392b", "E5": "#2c3e50"}


def load(name):
    p = f"{D}/{name}.npz"
    if not os.path.exists(p):
        return None
    d = np.load(p, allow_pickle=True)
    return dict(success=np.asarray(d["success"], np.float32), ex=[np.asarray(e, np.float32) for e in d["exec"]])


def harm(ex):
    j, m = [], []
    for x in ex:
        if x.ndim == 2 and not np.isnan(x).any():
            d1 = np.diff(x[:, :3], axis=0); j.append(np.mean(np.abs(np.diff(d1, axis=0)))); m.append(np.max(np.abs(d1)))
    return (float(np.mean(j)), float(np.mean(m))) if j else (np.nan, np.nan)


def agg(names):
    sr, jk, ms = [], [], []
    for n in names:
        r = load(n)
        if r is None:
            continue
        sr.append(r["success"].mean()); a, b = harm(r["ex"]); jk.append(a); ms.append(b)
    if not sr:
        return None
    return dict(sr=100 * np.mean(sr), sd=100 * np.std(sr), n=len(sr), jerk=float(np.nanmean(jk)), maxstep=float(np.nanmean(ms)))


def frozen(arm, cond):
    pre = f"p1_{arm}_ad0" if arm in ("E4", "E5") else f"ctrl_{arm}"
    return agg([f"{pre}_{cond}_s{s}" for s in SEEDS])


CONDS = [("nodrift", "no drift"), ("gain0.7", "gain x0.7"), ("delay2", "delay 2 (estimator fooled)")]
MODES = [(1, "always-on"), (2, "triggered")]
res = {"comp": {}, "noise": {}}

print("== compensation placement: success (d vs frozen) | jerk x frozen ==")
for arm in ("E4", "B"):
    for ad, mn in MODES:
        for c, _ in CONDS:
            f = frozen(arm, c)
            down = agg([f"p1_{arm}_ad{ad}_{c}_s{s}" for s in SEEDS])
            up = agg([f"{UP}_{arm}_ad{ad}_{c}_s{s}" for s in SEEDS])
            for where, v in (("down", down), ("up", up)):
                if v is None or f is None:
                    continue
                res["comp"][f"{arm}_{mn}_{c}_{where}"] = dict(v, dsr=v["sr"] - f["sr"], jr=v["jerk"] / f["jerk"], mr=v["maxstep"] / f["maxstep"])
            if down and up and f:
                print(f"{arm:<3} {mn:<10} {c:<9} down {down['sr']:5.1f} ({down['sr']-f['sr']:+5.1f}, j x{down['jerk']/f['jerk']:.2f})   "
                      f"up {up['sr']:5.1f} ({up['sr']-f['sr']:+5.1f}, j x{up['jerk']/f['jerk']:.2f})")

print("\n== controlled adaptation noise (1+eps), frozen, no drift ==")
for arm in ("E4", "B", "A"):
    f = frozen(arm, "nodrift")
    for sg in ("0.25", "0.5"):
        for where in (("up", "down") if arm != "A" else ("",)):
            names = [f"cn_{arm}_{where}_sig{sg}_s{s}" if where else f"cn_{arm}_sig{sg}_s{s}" for s in SEEDS]
            v = agg(names)
            if v is None or f is None:
                continue
            key = f"{arm}_{where or 'raw'}_{sg}"
            res["noise"][key] = dict(v, dsr=v["sr"] - f["sr"], jr=v["jerk"] / f["jerk"], mr=v["maxstep"] / f["maxstep"])
            print(f"{arm:<3} {where or 'raw':<5} sig{sg}: success {v['sr']:5.1f} ({v['sr']-f['sr']:+5.1f}, n={v['n']})   "
                  f"jerk {v['jerk']:.4f} (x{v['jerk']/f['jerk']:.2f})   maxstep {v['maxstep']:.3f} (x{v['maxstep']/f['maxstep']:.2f})")

# ---------------------------------------------------------------- figure
fig, ax = plt.subplots(1, 3, figsize=(16, 4.2))
# (1) placement: delta success, estimator fooled + gain0.7, triggered
labels, vals, cols, hatches = [], [], [], []
for arm in ("E4", "B"):
    for c in ("gain0.7", "delay2"):
        for where in ("down", "up"):
            v = res["comp"].get(f"{arm}_triggered_{c}_{where}")
            if v:
                labels.append(f"{arm}\n{'x0.7' if c=='gain0.7' else 'fooled'}\n{where}"); vals.append(v["dsr"]); cols.append(COL[arm]); hatches.append("" if where == "down" else "//")
x = np.arange(len(vals))
for i in range(len(vals)):
    ax[0].bar(x[i], vals[i], color=cols[i], hatch=hatches[i], alpha=0.85, edgecolor="k", lw=0.5)
ax[0].axhline(0, color="k", lw=0.8); ax[0].set_xticks(x); ax[0].set_xticklabels(labels, fontsize=7)
ax[0].set_ylabel("d success vs frozen (pp)"); ax[0].set_title("Triggered compensation: downstream (solid) vs upstream (hatched)", fontsize=9)
# (2) placement: jerk ratio, same cells
vals2 = []
for arm in ("E4", "B"):
    for c in ("gain0.7", "delay2"):
        for where in ("down", "up"):
            v = res["comp"].get(f"{arm}_triggered_{c}_{where}")
            if v:
                vals2.append(v["jr"])
for i in range(len(vals2)):
    ax[1].bar(x[i], vals2[i], color=cols[i], hatch=hatches[i], alpha=0.85, edgecolor="k", lw=0.5)
ax[1].axhline(1, color="k", lw=0.8); ax[1].set_xticks(x); ax[1].set_xticklabels(labels, fontsize=7)
ax[1].set_ylabel("executed jerk / frozen"); ax[1].set_title("Same cells: jerk amplification", fontsize=9)
# (3) noise: maxstep absolute vs sigma
for arm, where in (("E4", "up"), ("E4", "down"), ("B", "up"), ("B", "down"), ("A", "raw")):
    xs, ys = [0.0], [frozen(arm, "nodrift")["maxstep"]]
    for sg in ("0.25", "0.5"):
        v = res["noise"].get(f"{arm}_{where}_{sg}")
        if v:
            xs.append(float(sg)); ys.append(v["maxstep"])
    ax[2].plot(xs, ys, "o-" if where != "down" else "s--", color=COL[arm], lw=1.5, label=f"{arm} {where}")
ax[2].set_xlabel("adaptation-noise sigma (multiplicative, white)"); ax[2].set_ylabel("max executed step (P3 quantity)")
ax[2].set_title("Controlled adaptation noise: execution-space trust region", fontsize=9); ax[2].legend(fontsize=7)
plt.tight_layout(); os.makedirs("figures", exist_ok=True); plt.savefig("figures/P1_upstream.png", dpi=160); plt.close()

with open("upstream_results.md", "w", encoding="utf-8") as fo:
    fo.write("### \u8865\u507f\u4f4d\u7f6e\uff1a\u4e0b\u6e38\uff08\u6267\u884c\u6307\u4ee4\uff09vs \u4e0a\u6e38\uff08\u7b56\u7565\u8f93\u51fa\uff09\n\n| \u81c2 | \u6a21\u5f0f | \u6761\u4ef6 | \u4f4d\u7f6e | \u6210\u529f\u7387 | \u0394 vs \u51bb\u7ed3 | jerk \u500d\u6570 | \u6700\u5927\u5355\u6b65\u500d\u6570 |\n|---|---|---|---|---|---|---|---|\n")
    for k, v in res["comp"].items():
        arm, mn, c, where = k.split("_", 3)
        fo.write(f"| {arm} | {mn} | {c} | {where} | {v['sr']:.1f} \u00b1 {v['sd']:.1f} (n={v['n']}) | {v['dsr']:+.1f} | \u00d7{v['jr']:.2f} | \u00d7{v['mr']:.2f} |\n")
    fo.write("\n### \u53d7\u63a7\u9002\u5e94\u566a\u58f0\uff081+\u03b5\uff0c\u767d\u3001\u4e58\u6027\uff09\uff0c\u51bb\u7ed3\u3001\u65e0\u6f02\u79fb\n\n| \u81c2 | \u6ce8\u5165\u70b9 | \u03c3_\u03b5 | \u6210\u529f\u7387 | \u0394 | jerk | \u500d\u6570 | \u6700\u5927\u5355\u6b65 | \u500d\u6570 |\n|---|---|---|---|---|---|---|---|---|\n")
    for k, v in res["noise"].items():
        arm, where, sg = k.split("_")
        fo.write(f"| {arm} | {where} | {sg} | {v['sr']:.1f} \u00b1 {v['sd']:.1f} | {v['dsr']:+.1f} | {v['jerk']:.4f} | \u00d7{v['jr']:.2f} | {v['maxstep']:.3f} | \u00d7{v['mr']:.2f} |\n")
json.dump(res, open("upstream_results.json", "w"), indent=1)
print("saved figures/P1_upstream.png")
