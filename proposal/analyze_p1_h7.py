"""H7 ablation analysis: E4 with vs without obs_cmd under gain drift."""
import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = "p0_out"
CONDS = [("nodrift", "no drift"), ("gain0.8", "gain �0.8"), ("gain0.7", "gain �0.7")]
SEEDS = [1000, 2000, 3000]


def load(tag, cond, seed):
    p = f"{D}/p1h7_E4_{tag}_{cond}_s{seed}.npz"
    if not os.path.exists(p):
        return None
    d = np.load(p, allow_pickle=True)
    return float(np.mean(d["success"]))


table = {}
for tag in ("full", "mask"):
    for c, _ in CONDS:
        srs = [load(tag, c, s) for s in SEEDS]
        srs = [x for x in srs if x is not None]
        if srs:
            table[(tag, c)] = dict(sr=100 * np.mean(srs), sd=100 * np.std(srs), n=len(srs))

if not table:
    open("p1_h7_results.md", "w").write("_H7 ablation pending: run `run_p1_h7_ablation.sh`._\n")
    print("No p1h7_* files yet")
    raise SystemExit(0)

fig, ax = plt.subplots(figsize=(7, 4))
x = np.arange(len(CONDS))
w = 0.35
for i, (tag, lab, col) in enumerate(
    (("full", "obs_cmd on", "#16a085"), ("mask", "obs_cmd masked", "#c0392b"))
):
    vals = [table.get((tag, c), {}).get("sr", np.nan) for c, _ in CONDS]
    errs = [table.get((tag, c), {}).get("sd", 0) for c, _ in CONDS]
    ax.bar(x + (i - 0.5) * w, vals, w, yerr=errs, capsize=3, label=lab, color=col, alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels([l for _, l in CONDS])
ax.set_ylabel("success (%)")
ax.set_title("H7  E4 frozen deployment: obs_cmd ablation under gain drift")
ax.legend()
ax.set_ylim(0, 105)
plt.tight_layout()
os.makedirs("figures", exist_ok=True)
plt.savefig("figures/P1_h7_obscmd.png", dpi=160)
plt.close()

with open("p1_h7_results.md", "w", encoding="utf-8") as fo:
    fo.write("| obs_cmd | ?? | ??? |\n|---|---|---|\n")
    for (tag, c), v in sorted(table.items()):
        fo.write(f"| {'on' if tag == 'full' else 'masked'} | {c} | {v['sr']:.1f} � {v['sd']:.1f} |\n")

if ("full", "gain0.8") in table and ("mask", "gain0.8") in table:
    gap = table[("full", "gain0.8")]["sr"] - table[("mask", "gain0.8")]["sr"]
    print(f"obs_cmd benefit at gain�0.8: {gap:+.1f} pp")

json.dump(table, open("p1_h7_results.json", "w"), indent=1)
