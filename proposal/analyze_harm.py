# -*- coding: utf-8 -*-
"""Misadaptation harm - the surviving claim, against strong controls.

Panel 1-2: estimator fooled (delay 2 read as gain): success loss and jerk ratio vs frozen,
           for E4 (interface), E5 (matched raw), A (strong raw), B (lowpass) x {always-on, triggered, v2}.
Panel 3-4: controlled misadaptation (executed gain x1.2/1.4/1.6 on frozen policies): success and jerk vs error.
Writes figures/P1_harm.png and harm_results.md/json.
"""
import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = "p0_out"
SEEDS = [1000, 2000, 3000]
COL = {"E4": "#16a085", "E5": "#2c3e50", "A": "#c0392b", "B": "#8e44ad"}
LAB = {"E4": "E4 interface (leak .9, \u03c3=.03)", "E5": "E5 raw (\u03c3=.03)", "A": "A raw (\u03c3=.10)", "B": "B raw+lowpass (\u03c3=.10)"}
MODES = [(1, "always-on"), (2, "triggered"), (5, "lag-aligned v2")]


def frozen_name(arm, c, s):
    return f"p1_{arm}_ad0_{c}_s{s}" if arm in ("E4", "E5") else f"ctrl_{arm}_{c}_s{s}"


def mode_name(arm, ad, c, s):
    return f"p1f_{arm}_ad{ad}_{c}_s{s}" if ad in (3, 5) else f"p1_{arm}_ad{ad}_{c}_s{s}"


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


res = {"fooled": {}, "overgain": {}}
# ---------------------------------------------------------------- estimator fooled (delay 2)
for arm in ("E4", "E5", "A", "B"):
    f = agg([frozen_name(arm, "delay2", s) for s in SEEDS]); f0 = agg([frozen_name(arm, "nodrift", s) for s in SEEDS])
    if f is None:
        continue
    res["fooled"][f"{arm}_frozen"] = dict(f, dsr=0.0, jr=1.0)
    for ad, mn in MODES:
        m = agg([mode_name(arm, ad, "delay2", s) for s in SEEDS])
        if m is None:
            continue
        res["fooled"][f"{arm}_ad{ad}"] = dict(m, dsr=m["sr"] - f["sr"], jr=m["jerk"] / f["jerk"], mode=mn)

# ---------------------------------------------------------------- controlled over-gain
for arm in ("E4", "E5", "A", "B"):
    f0 = agg([frozen_name(arm, "nodrift", s) for s in SEEDS])
    if f0 is None:
        continue
    res["overgain"][f"{arm}_1.0"] = dict(f0, g=1.0, jr=1.0)
    for g in (0.7, 0.8):
        m = agg([frozen_name(arm, f"gain{g}", s) for s in SEEDS])
        if m:
            res["overgain"][f"{arm}_{g}"] = dict(m, g=g, jr=m["jerk"] / f0["jerk"])
    for g in (1.2, 1.4, 1.6):
        m = agg([f"og_{arm}_gain{g}_s{s}" for s in SEEDS])
        if m:
            res["overgain"][f"{arm}_{g}"] = dict(m, g=g, jr=m["jerk"] / f0["jerk"])

# ---------------------------------------------------------------- print
print("== estimator fooled (delay 2 read as gain): dSuccess vs frozen | jerk ratio vs frozen ==")
for arm in ("E4", "E5", "A", "B"):
    for ad, mn in MODES:
        v = res["fooled"].get(f"{arm}_ad{ad}")
        if v:
            print(f"{arm:<3} {mn:<15} success {v['sr']:5.1f} (d {v['dsr']:+6.1f}, n={v['n']})   jerk x{v['jr']:.2f}   maxstep {v['maxstep']:.3f}")
print("\n== controlled over-gain (frozen): success | jerk ratio ==")
for arm in ("E4", "E5", "A", "B"):
    row = [(v["g"], v["sr"], v["jr"], v["n"]) for k, v in res["overgain"].items() if k.startswith(arm + "_")]
    row.sort()
    print(f"{arm:<3} " + "  ".join(f"x{g}: {sr:5.1f}% (j{jr:.2f},n{n})" for g, sr, jr, n in row))

# ---------------------------------------------------------------- figure
fig, ax = plt.subplots(1, 4, figsize=(20, 4.2))
arms = [a for a in ("E4", "E5", "A", "B") if f"{a}_frozen" in res["fooled"]]
x = np.arange(len(arms)); w = 0.26
for i, (ad, mn) in enumerate(MODES):
    d = [res["fooled"].get(f"{a}_ad{ad}", {}).get("dsr", np.nan) for a in arms]
    j = [res["fooled"].get(f"{a}_ad{ad}", {}).get("jr", np.nan) for a in arms]
    ax[0].bar(x + (i - 1) * w, d, w, color=[COL[a] for a in arms], alpha=0.45 + 0.25 * i, label=mn)
    ax[1].bar(x + (i - 1) * w, j, w, color=[COL[a] for a in arms], alpha=0.45 + 0.25 * i, label=mn)
ax[0].axhline(0, color="k", lw=0.8); ax[0].set_xticks(x); ax[0].set_xticklabels(arms)
ax[0].set_ylabel("\u0394 success vs frozen (pp)"); ax[0].set_title("Estimator fooled (delay 2 \u2192 wrong 1/g\u0302): success loss", fontsize=9.5); ax[0].legend(fontsize=7)
ax[1].axhline(1, color="k", lw=0.8); ax[1].set_xticks(x); ax[1].set_xticklabels(arms)
ax[1].set_ylabel("executed jerk / frozen jerk"); ax[1].set_title("Estimator fooled: jerk amplification", fontsize=9.5)
for a in ("E4", "E5", "A", "B"):
    row = sorted([(v["g"], v["sr"], v["jr"]) for k, v in res["overgain"].items() if k.startswith(a + "_")])
    if row:
        gs, srs, jrs = zip(*row)
        ax[2].plot(gs, srs, "o-", color=COL[a], label=LAB[a], lw=1.6)
        ax[3].plot(gs, jrs, "o-", color=COL[a], label=LAB[a], lw=1.6)
ax[2].axvline(1, color="k", lw=0.8, ls=":"); ax[2].set_xlabel("executed gain factor (wrong compensation)"); ax[2].set_ylabel("success (%)")
ax[2].set_title("Controlled misadaptation: success vs gain error", fontsize=9.5); ax[2].legend(fontsize=7); ax[2].set_ylim(0, 105)
ax[3].axvline(1, color="k", lw=0.8, ls=":"); ax[3].axhline(1, color="k", lw=0.8, ls=":"); ax[3].set_xlabel("executed gain factor"); ax[3].set_ylabel("jerk / no-drift jerk")
ax[3].set_title("Controlled misadaptation: jerk vs gain error", fontsize=9.5)
plt.tight_layout(); os.makedirs("figures", exist_ok=True); plt.savefig("figures/P1_harm.png", dpi=160); plt.close()

with open("harm_results.md", "w", encoding="utf-8") as fo:
    fo.write("### \u4f30\u8ba1\u5668\u88ab\u9a97\uff08\u5ef6\u8fdf 2 \u88ab\u8bfb\u6210\u589e\u76ca\uff09\n\n| \u81c2 | \u6a21\u5f0f | \u6210\u529f\u7387 | \u0394 vs \u51bb\u7ed3 | jerk \u500d\u6570 | \u6700\u5927\u5355\u6b65 |\n|---|---|---|---|---|---|\n")
    for arm in ("E4", "E5", "A", "B"):
        for ad, mn in MODES:
            v = res["fooled"].get(f"{arm}_ad{ad}")
            if v:
                fo.write(f"| {arm} | {mn} | {v['sr']:.1f} ± {v['sd']:.1f} (n={v['n']}) | {v['dsr']:+.1f} | ×{v['jr']:.2f} | {v['maxstep']:.3f} |\n")
    fo.write("\n### \u53d7\u63a7\u8bef\u9002\u5e94\uff08\u51bb\u7ed3\u7b56\u7565\uff0c\u6267\u884c\u589e\u76ca \u2260 1\uff09\n\n| \u81c2 | \u00d70.7 | \u00d70.8 | \u00d71.0 | \u00d71.2 | \u00d71.4 | \u00d71.6 |\n|---|---|---|---|---|---|---|\n")
    for arm in ("E4", "E5", "A", "B"):
        cells = []
        for g in (0.7, 0.8, 1.0, 1.2, 1.4, 1.6):
            v = res["overgain"].get(f"{arm}_{g}")
            cells.append(f"{v['sr']:.1f} (j×{v['jr']:.2f})" if v else "-")
        fo.write(f"| {arm} | " + " | ".join(cells) + " |\n")
json.dump(res, open("harm_results.json", "w"), indent=1)
print("saved figures/P1_harm.png")
