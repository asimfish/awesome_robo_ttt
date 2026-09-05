"""P1'' analysis: delay-aware vs plain triggered adaptation.

Expects p0_out/p1d_* (adapt=3) alongside p1_* (adapt=2) from P1'.
Outputs figures/P1_delay_aware.png + p1_delay_results.md
"""
import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = "p0_out"
CONDS = [("nodrift", "no drift"), ("gain0.8", "gain �0.8"), ("gain0.7", "gain �0.7"), ("delay2", "delay 2")]
SEEDS = [1000, 2000, 3000]
ARMS = ["E4", "E5"]
COL = {"plain": "#95a5a6", "delay": "#16a085", "E5": "#2c3e50"}


def load(name):
    p = f"{D}/{name}.npz"
    if not os.path.exists(p):
        return None
    d = np.load(p, allow_pickle=True)
    ex = [np.asarray(e, dtype=np.float32) for e in d["exec"]]
    gh = [np.asarray(g, dtype=np.float32) for g in d.get("ghat", [])]
    return dict(success=np.asarray(d["success"], np.float32), ex=ex, ghat=gh)


def harm(ex):
    j, s = [], []
    for x in ex:
        d1 = np.diff(x[:, :3], axis=0)
        j.append(np.mean(np.abs(np.diff(d1, axis=0))))
        s.append(np.max(np.abs(d1)))
    return float(np.mean(j)), float(np.mean(s))


def agg(prefix, arm, cond):
    srs, js, ghs = [], [], []
    for s in SEEDS:
        r = load(f"{prefix}_{arm}_ad3_{cond}_s{s}")
        if r is None:
            continue
        srs.append(r["success"].mean())
        jj, _ = harm(r["ex"])
        js.append(jj)
        if r["ghat"]:
            ghs += [g[-1] for g in r["ghat"] if len(g)]
    if not srs:
        return None
    return dict(sr=100 * np.mean(srs), sd=100 * np.std(srs), n=len(srs),
                jerk=np.mean(js), ghat=float(np.mean(ghs)) if ghs else float("nan"))


table = {}
for arm in ARMS:
    for ad, tag in ((2, "plain"), (3, "delay")):
        pref = "p1" if ad == 2 else "p1d"
        for c, _ in CONDS:
            srs, js, ghs = [], [], []
            for s in SEEDS:
                r = load(f"{pref}_{arm}_ad{ad}_{c}_s{s}")
                if r is None:
                    continue
                srs.append(r["success"].mean())
                jj, _ = harm(r["ex"])
                js.append(jj)
                if r["ghat"]:
                    ghs += [g[-1] for g in r["ghat"] if len(g)]
            if srs:
                table[(arm, tag, c)] = dict(
                    sr=100 * np.mean(srs), sd=100 * np.std(srs), n=len(srs),
                    jerk=np.mean(js), ghat=float(np.mean(ghs)) if ghs else float("nan"),
                )

if not any(k[1] == "delay" for k in table):
    print("No p1d_* files yet � run run_p1_delay.sh on server first.")
    open("p1_delay_results.md", "w").write(
        "_P1'' pending: no `p0_out/p1d_*` rollouts found. Run `run_p1_delay.sh`._\n"
    )
    raise SystemExit(0)

fig, ax = plt.subplots(1, 2, figsize=(12, 4))
x = np.arange(len(CONDS))
w = 0.18
for i, arm in enumerate(ARMS):
    for j, (tag, col, alpha) in enumerate(
        (("plain", COL["plain"], 0.55), ("delay", COL["delay"] if arm == "E4" else COL["E5"], 0.95))
    ):
        vals = [table.get((arm, tag, c), {}).get("sr", np.nan) for c, _ in CONDS]
        errs = [table.get((arm, tag, c), {}).get("sd", 0) for c, _ in CONDS]
        off = (-1.5 + i * 2 + j) * w
        ax[0].bar(
            x + off, vals, w, yerr=errs, capsize=2, color=col, alpha=alpha,
            label=f"{arm} {'triggered' if tag == 'plain' else 'delay-aware'}",
        )
ax[0].set_xticks(x)
ax[0].set_xticklabels([l for _, l in CONDS], fontsize=8)
ax[0].set_ylabel("success (%)")
ax[0].set_title("P1''  Delay-aware triggered vs plain triggered (adapt=3 vs 2)")
ax[0].legend(fontsize=7)
ax[0].set_ylim(0, 105)

# misadaptation cost on delay2 only
labels, vals = [], []
for arm in ARMS:
    for tag, name in (("plain", "trig"), ("delay", "delay-aware")):
        fr = table.get((arm, tag, "delay2"))
        if fr:
            labels.append(f"{arm} {name}")
            vals.append(fr["sr"])
if vals:
    ax[1].bar(range(len(vals)), vals, color=[COL["delay"] if "E4" in l else COL["E5"] for l in labels], alpha=0.85)
    ax[1].set_xticks(range(len(labels)))
    ax[1].set_xticklabels(labels, fontsize=8, rotation=15)
    ax[1].set_ylabel("success under delay 2")
    ax[1].set_title("Negative control: delay drift (higher = less misadaptation)")

plt.tight_layout()
os.makedirs("figures", exist_ok=True)
plt.savefig("figures/P1_delay_aware.png", dpi=160)
plt.close()

with open("p1_delay_results.md", "w", encoding="utf-8") as fo:
    fo.write("| ? | ?? | ?? | ??? | ? | jerk |\n|---|---|---|---|---|---|\n")
    for (arm, tag, c), v in sorted(table.items()):
        mode = "triggered" if tag == "plain" else "delay-aware triggered"
        fo.write(
            f"| {arm} | {mode} | {c} | {v['sr']:.1f} � {v['sd']:.1f} (n={v['n']}) | "
            f"{v['ghat']:.3f} | {v['jerk']:.4f} |\n"
        )

# Key deltas for proposal text
if ("E4", "plain", "delay2") in table and ("E4", "delay", "delay2") in table:
    d = table[("E4", "delay", "delay2")]["sr"] - table[("E4", "plain", "delay2")]["sr"]
    print(f"E4 delay2 recovery vs plain triggered: {d:+.1f} pp")

json.dump(
    {f"{a}_{t}_{c}": v for (a, t, c), v in table.items()},
    open("p1_delay_results.json", "w"),
    indent=1,
)
