"""P1' analysis: adaptive gain compensation. Inputs p0_out/p1_*.npz. Outputs figures/P1_adapt.png + p1_results.md"""
import glob, re, os, json
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
D = "p0_out"
def load(name):
    p = f"{D}/{name}.npz"
    if not os.path.exists(p): return None
    d = np.load(p, allow_pickle=True)
    ex = [np.asarray(e, dtype=np.float32) for e in d["exec"]]
    gh = [np.asarray(g, dtype=np.float32) for g in d["ghat"]] if "ghat" in d.files else []
    return dict(success=np.asarray(d["success"], np.float32), ex=ex, ghat=gh)
def harm(ex):
    j = []; s = []
    for x in ex:
        d1 = np.diff(x[:, :3], axis=0); j.append(np.mean(np.abs(np.diff(d1, axis=0)))); s.append(np.max(np.abs(d1)))
    return float(np.mean(j)), float(np.mean(s))
conds = [("nodrift", "no drift"), ("gain0.8", "gain ×0.8"), ("gain0.7", "gain ×0.7"), ("delay2", "delay 2 (neg. control)")]
seeds = [1000, 2000, 3000]; arms = ["E4", "E5"]; COL = {"E4": "#16a085", "E5": "#2c3e50"}
rows = []; table = {}
for arm in arms:
    for ad in (0, 1, 2):
        for c, _ in conds:
            srs = []; js = []; ms = []; gfinal = []
            for s in seeds:
                r = load(f"p1_{arm}_ad{ad}_{c}_s{s}")
                if r is None: continue
                srs.append(r["success"].mean()); jj, mm = harm(r["ex"]); js.append(jj); ms.append(mm)
                if r["ghat"]: gfinal += [g[-1] for g in r["ghat"] if len(g)]
            if srs:
                table[(arm, ad, c)] = dict(sr=np.mean(srs) * 100, sd=np.std(srs) * 100, n=len(srs), jerk=np.mean(js), maxstep=np.mean(ms),
                                           ghat=float(np.mean(gfinal)) if gfinal else float("nan"))
fig, ax = plt.subplots(1, 3, figsize=(15, 4))
x = np.arange(len(conds)); w = 0.13
ADL = {0: "frozen", 1: "always-adapt", 2: "triggered"}; ALP = {0: 0.35, 1: 0.65, 2: 1.0}
for i, arm in enumerate(arms):
    for ad in (0, 1, 2):
        vals = [table.get((arm, ad, c), {}).get("sr", np.nan) for c, _ in conds]
        errs = [table.get((arm, ad, c), {}).get("sd", 0) for c, _ in conds]
        off = (-2.5 + i * 3 + ad) * w
        ax[0].bar(x + off, vals, w, yerr=errs, capsize=2, color=COL[arm], alpha=ALP[ad],
                  label=f"{arm} {'raw' if arm=='E5' else 'interface'} · {ADL[ad]}")
ax[0].set_xticks(x); ax[0].set_xticklabels([l for _, l in conds], fontsize=8); ax[0].set_ylabel("success (%)  mean ± sd over 3 eval seeds × 100 ep")
ax[0].set_title("P1'  Adaptive gain compensation (ĝ from tracking residual)", fontsize=9.5); ax[0].legend(fontsize=7); ax[0].set_ylim(0, 105)
# ghat convergence: first 3 episodes of seed 1000, gain 0.8
for arm in arms:
    for ad, ls in ((1, "-"), (2, "--")):
        r = load(f"p1_{arm}_ad{ad}_gain0.8_s1000")
        if r and r["ghat"]:
            g = np.concatenate([gg for gg in r["ghat"][:5] if len(gg)])
            ax[1].plot(g, color=COL[arm], ls=ls, label=f"{arm} ĝ · {ADL[ad]}", lw=1.3)
ax[1].axhline(0.8, ls="--", color="#c0392b", lw=1); ax[1].set_xlabel("control-chunk steps (5 consecutive episodes)"); ax[1].set_ylabel("ĝ"); ax[1].set_title("P1'  ĝ convergence under gain ×0.8", fontsize=9.5); ax[1].legend(fontsize=8)
# harm: jerk
for i, arm in enumerate(arms):
    for ad in (0, 1, 2):
        vals = [table.get((arm, ad, c), {}).get("jerk", np.nan) for c, _ in conds]
        off = (-2.5 + i * 3 + ad) * w
        ax[2].bar(x + off, vals, w, color=COL[arm], alpha=ALP[ad])
ax[2].set_xticks(x); ax[2].set_xticklabels([l for _, l in conds], fontsize=8); ax[2].set_ylabel("executed jerk (mean |Δ²c|, pos dims)"); ax[2].set_title("P1'  Harm during adaptation (lower = smoother)", fontsize=9.5)
plt.tight_layout(); plt.savefig("figures/P1_adapt.png", dpi=160); plt.close()
with open("p1_results.md", "w", encoding="utf-8") as fo:
    fo.write("| 臂 | 适应 | 条件 | 成功率 (mean±sd, 3 seeds) | ĝ 终值 | jerk | 最大单步变化 |\n|---|---|---|---|---|---|---|\n")
    for (arm, ad, c), v in table.items():
        fo.write(f"| {arm} | {ADL[ad]} | {c} | {v['sr']:.1f} ± {v['sd']:.1f} (n={v['n']}) | {v['ghat']:.3f} | {v['jerk']:.4f} | {v['maxstep']:.3f} |\n")
json.dump({f"{a}_ad{ad}_{c}": v for (a, ad, c), v in table.items()}, open("p1_results.json", "w"), indent=1)
print(f"{'arm':<4}{'adapt':<13}{'cond':<9}{'success':>14}  {'ghat':>6}  {'jerk':>7}  {'maxstep':>7}")
for (arm, ad, c), v in table.items(): print(f"{arm:<4}{ADL[ad]:<13}{c:<9}{v['sr']:6.1f} ± {v['sd']:4.1f}  {v['ghat']:6.3f}  {v['jerk']:7.4f}  {v['maxstep']:7.3f}")
