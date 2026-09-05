# -*- coding: utf-8 -*-
"""Unified P1 family table: arms (E4 interface, E5 matched raw, A strong raw) x adaptation modes x drift.

Modes: ad0 frozen | ad1 always-on | ad2 triggered | ad3 delay-aware v1 (hard veto) | ad5 lag-aligned v2.
Files:  E4/E5 frozen/always/trig -> p1_*, v1 -> p1d_*, v2 -> p1a_*;  A frozen -> ctrl_A_*, A modes -> p1_A_*.
Outputs figures/P1_all.png, p1_all_results.md/.json, and lag-choice diagnostics for v2.
"""
import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = "p0_out"
SEEDS = [1000, 2000, 3000]
CONDS = [("nodrift", "no drift"), ("gain0.8", "gain x0.8"), ("gain0.7", "gain x0.7"), ("delay2", "delay 2 (neg. ctrl)")]
MODES = [(0, "frozen"), (1, "always-on"), (2, "triggered"), (3, "delay-aware v1 (veto)"), (5, "lag-aligned v2")]
ARMS = [("E4", "interface (leak .9, s=.03)"), ("E5", "raw, matched s=.03"), ("A", "raw, s=.10"), ("B", "raw + lowpass, s=.10")]
COL = {"E4": "#16a085", "E5": "#2c3e50", "A": "#c0392b", "B": "#8e44ad"}
ALP = {0: 0.30, 1: 0.50, 2: 0.70, 3: 0.85, 5: 1.0}


def fname(arm, ad, c, s):
    if arm in ("A", "B"):
        if ad == 0:
            return f"ctrl_{arm}_{c}_s{s}"
        if ad in (3, 5):
            return f"p1f_{arm}_ad{ad}_{c}_s{s}"
        return f"p1_{arm}_ad{ad}_{c}_s{s}"
    if ad in (3, 5):
        # fixed reruns only (history-reset bug in the first P1'' batches: p1d_/p1a_/p1_A_ad5 are invalid)
        return f"p1f_{arm}_ad{ad}_{c}_s{s}"
    return f"p1_{arm}_ad{ad}_{c}_s{s}"


def load(name):
    p = f"{D}/{name}.npz"
    if not os.path.exists(p):
        return None
    d = np.load(p, allow_pickle=True)
    r = dict(success=np.asarray(d["success"], np.float32),
             ex=[np.asarray(e, np.float32) for e in d["exec"]],
             ghat=[np.asarray(g, np.float32) for g in d["ghat"]] if "ghat" in d.files else [],
             lag=[np.asarray(g, np.int8) for g in d["lag"]] if "lag" in d.files else [])
    return r


def jerk(ex):
    j = []
    for x in ex:
        if x.ndim == 2 and not np.isnan(x).any():
            d1 = np.diff(x[:, :3], axis=0); j.append(np.mean(np.abs(np.diff(d1, axis=0))))
    return float(np.mean(j)) if j else float("nan")


table = {}
for arm, _ in ARMS:
    for ad, _ in MODES:
        for c, _ in CONDS:
            srs, js, gh, act, lags = [], [], [], [], []
            for s in SEEDS:
                r = load(fname(arm, ad, c, s))
                if r is None:
                    continue
                srs.append(r["success"].mean()); js.append(jerk(r["ex"]))
                if r["ghat"] and any(len(x) for x in r["ghat"]):
                    g = np.concatenate([x for x in r["ghat"] if len(x)])
                    on = g[np.abs(g - 1) > 1e-6]
                    act.append(np.mean(np.abs(g - 1) > 1e-6)); gh.append(np.mean(on) if len(on) else np.nan)
                if r["lag"] and any(len(x) for x in r["lag"]):
                    lags.append(np.concatenate([x for x in r["lag"] if len(x)]))
            if srs:
                lagdist = None
                if lags:
                    L = np.concatenate(lags); lagdist = [float(np.mean(L == k)) for k in range(4)]
                table[(arm, ad, c)] = dict(sr=100 * np.mean(srs), sd=100 * np.std(srs), n=len(srs), jerk=float(np.nanmean(js)),
                                           ghat=float(np.nanmean(gh)) if gh else float("nan"),
                                           active=float(np.mean(act)) if act else float("nan"), lagdist=lagdist)

# ---------------------------------------------------------------- print
print(f"{'arm':<4}{'mode':<24}{'cond':<9}{'success':>14}  {'g^|on':>6} {'active':>7} {'jerk':>7}  lag-dist(0..3)")
for arm, _ in ARMS:
    for ad, mn in MODES:
        for c, _ in CONDS:
            v = table.get((arm, ad, c))
            if v is None:
                continue
            ld = "" if v["lagdist"] is None else " ".join(f"{x:.2f}" for x in v["lagdist"])
            print(f"{arm:<4}{mn:<24}{c:<9}{v['sr']:6.1f} ± {v['sd']:4.1f} ({v['n']})  {v['ghat']:6.3f} {100*v['active']:6.1f}% {v['jerk']:7.4f}  {ld}")
    print()

# ---------------------------------------------------------------- misadaptation cost + recovery
print("== recovery at gain x0.7 (mode - frozen) and misadaptation cost (no-drift / delay2, mode - frozen) ==")
for arm, _ in ARMS:
    f = {c: table.get((arm, 0, c), {}).get("sr", np.nan) for c, _ in CONDS}
    for ad, mn in MODES[1:]:
        if (arm, ad, "gain0.7") not in table:
            continue
        rec = table[(arm, ad, "gain0.7")]["sr"] - f["gain0.7"]
        mis0 = table.get((arm, ad, "nodrift"), {}).get("sr", np.nan) - f["nodrift"]
        misd = table.get((arm, ad, "delay2"), {}).get("sr", np.nan) - f["delay2"]
        print(f"{arm:<4}{mn:<24} recovery x0.7 {rec:+6.1f}   cost nodrift {mis0:+6.1f}   cost delay2 {misd:+6.1f}")

# ---------------------------------------------------------------- figure
fig, axes = plt.subplots(1, 4, figsize=(21, 4.2), sharey=True)
x = np.arange(len(CONDS)); w = 0.16
for k, (arm, desc) in enumerate(ARMS):
    ax = axes[k]
    for i, (ad, mn) in enumerate(MODES):
        vals = [table.get((arm, ad, c), {}).get("sr", np.nan) for c, _ in CONDS]
        errs = [table.get((arm, ad, c), {}).get("sd", 0) for c, _ in CONDS]
        ax.bar(x + (i - 2) * w, vals, w, yerr=errs, capsize=2, color=COL[arm], alpha=ALP[ad], label=mn)
    ax.set_xticks(x); ax.set_xticklabels([l for _, l in CONDS], fontsize=8)
    ax.set_title(f"{arm}: {desc}", fontsize=10); ax.set_ylim(0, 105)
    if k == 0:
        ax.set_ylabel("success (%)  mean ± sd over eval seeds x 100 ep")
    ax.legend(fontsize=7, loc="lower left")
fig.suptitle("Parameter-level TTT (residual-driven gain compensation): interface vs matched raw vs strong raw", fontsize=10.5)
plt.tight_layout(); os.makedirs("figures", exist_ok=True)
plt.savefig("figures/P1_all.png", dpi=160); plt.close()

with open("p1_all_results.md", "w", encoding="utf-8") as fo:
    fo.write("| ? | ?? | ?? | ??? | ?(?) | ??? | jerk | lag ?? 0/1/2/3 |\n|---|---|---|---|---|---|---|---|\n")
    for (arm, ad, c), v in table.items():
        mn = dict(MODES)[ad]
        ld = "" if v["lagdist"] is None else "/".join(f"{x:.2f}" for x in v["lagdist"])
        fo.write(f"| {arm} | {mn} | {c} | {v['sr']:.1f} ± {v['sd']:.1f} (n={v['n']}) | {v['ghat']:.3f} | {100*v['active']:.0f}% | {v['jerk']:.4f} | {ld} |\n")
json.dump({f"{a}_ad{ad}_{c}": v for (a, ad, c), v in table.items()}, open("p1_all_results.json", "w"), indent=1)
print("saved figures/P1_all.png")
