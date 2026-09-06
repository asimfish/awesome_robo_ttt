"""Design-space map: every arm is a first-order filter c_t = lam*c_{t-1} + s*u_t between policy and plant.
Raw policy = (lam=0, s=1). Low-pass alpha = (alpha, 1-alpha). Derivative interface = (lam, s) with DC gain s/(1-lam) > 1.

Axes (per point):
  1 prior      BC success at itr 0 (training log)              -> POINTS json (manual, from logs)
  2 trainable  final success after 200 itr PPO (training log)  -> POINTS json
  3 smooth     frozen no-drift: mean jerk, max step             -> npz
  4 robust     frozen: gain x0.7, delay 2 (obs-noise 0.05 where available) -> npz
  5 signal     calib corr; triggered-downstream recovery at x0.7; estimator-fooled cost (delay2 trig - frozen) -> npz
Writes figures/DS_map.png, design_space_table.md/json.
"""
import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = "p0_out"
SEEDS = [1000, 2000, 3000]

# (lam, s, sigma_train, obs_state, label) + file prefixes for frozen/trig/calib
POINTS = {
    "A":  dict(lam=0.0,  s=1.0, sig=0.10, obs=False, bc=38.0, final=99.5, frozen="ctrl_A_{c}_s{s}",   trig="p1_A_ad2_{c}_s{s}",   calib="calib_A"),
    "E5": dict(lam=0.0,  s=1.0, sig=0.03, obs=False, bc=38.0, final=93.0, frozen="p1_E5_ad0_{c}_s{s}", trig="p1_E5_ad2_{c}_s{s}", calib="calib_E5"),
    "B":  dict(lam=0.8,  s=0.2, sig=0.10, obs=False, bc=23.5, final=96.0, frozen="ctrl_B_{c}_s{s}",   trig="p1_B_ad2_{c}_s{s}",   calib="calib_B"),
    "E1": dict(lam=1.0,  s=1.0, sig=0.03, obs=True,  bc=43.5, final=92.0, frozen="ctrl_E1_{c}_s{s}",  trig=None,                  calib=None),
    "E4": dict(lam=0.9,  s=1.0, sig=0.03, obs=True,  bc=49.0, final=95.0, frozen="p1_E4_ad0_{c}_s{s}", trig="p1_E4_ad2_{c}_s{s}", calib="calib_E4"),
    # new Route-A points: filled from design_space/log_*.log + eval_point.sh outputs when available
    "F1": dict(lam=0.9,  s=0.3, sig=0.03, obs=True,  bc=None, final=None, frozen="ds_F1_frozen_{c}_s{s}", trig="ds_F1_trig_{c}_s{s}", calib="ds_F1_calib"),
    "F2": dict(lam=0.7,  s=1.0, sig=0.03, obs=True,  bc=None, final=None, frozen="ds_F2_frozen_{c}_s{s}", trig="ds_F2_trig_{c}_s{s}", calib="ds_F2_calib"),
    "F3": dict(lam=0.95, s=0.5, sig=0.03, obs=True,  bc=None, final=None, frozen="ds_F3_frozen_{c}_s{s}", trig="ds_F3_trig_{c}_s{s}", calib="ds_F3_calib"),
    "F4": dict(lam=0.8,  s=0.2, sig=0.03, obs=False, bc=23.5, final=None, frozen="ds_F4_frozen_{c}_s{s}", trig="ds_F4_trig_{c}_s{s}", calib="ds_F4_calib"),
}
if os.path.exists("design_space_manual.json"):   # {"F1": {"bc": 41.0, "final": 93.5}, ...} maintained from training logs
    for k, v in json.load(open("design_space_manual.json")).items():
        if k.startswith("_") or not isinstance(v, dict):
            continue
        POINTS.setdefault(k, dict(lam=None, s=None, sig=0.03, obs=True, bc=None, final=None, frozen="ds_%s_frozen_{c}_s{s}" % k,
                                  trig="ds_%s_trig_{c}_s{s}" % k, calib="ds_%s_calib" % k)).update({kk: vv for kk, vv in v.items() if vv is not None or kk in ("bc", "final")})


def load(name):
    p = f"{D}/{name}.npz"
    if not os.path.exists(p):
        return None
    d = np.load(p, allow_pickle=True)
    return dict(success=np.asarray(d["success"], np.float32), ex=[np.asarray(e, np.float32) for e in d["exec"]],
                calib=[np.asarray(c, np.float64) for c in d["calib"]] if "calib" in d.files else [])


def agg(pattern, cond):
    sr, jk, ms = [], [], []
    for s in SEEDS:
        r = load(pattern.format(c=cond, s=s))
        if r is None:
            continue
        sr.append(r["success"].mean())
        for x in r["ex"]:
            if x.ndim == 2 and not np.isnan(x).any():
                d1 = np.diff(x[:, :3], axis=0); jk.append(np.mean(np.abs(np.diff(d1, axis=0)))); ms.append(np.max(np.abs(d1)))
    if not sr:
        return None
    return dict(sr=100 * np.mean(sr), n=len(sr), jerk=float(np.mean(jk)), maxstep=float(np.mean(ms)))


def calib_corr(name):
    r = load(name) if name else None
    if r is None or not r["calib"]:
        return np.nan
    rows = np.concatenate([c for c in r["calib"] if len(c)], axis=0)
    free = rows[:, 6] > 0.5
    cc = [np.corrcoef(rows[free, j], rows[free, 3 + j])[0, 1] for j in range(3)]
    return float(np.mean(cc))


table = {}
for k, p in POINTS.items():
    row = dict(lam=p["lam"], s=p["s"], sig=p["sig"], obs=p["obs"], dc=(p["s"] / (1 - p["lam"]) if p["lam"] < 1 else np.inf),
               bc=p.get("bc"), final=p.get("final"))
    f0 = agg(p["frozen"], "nodrift"); fg = agg(p["frozen"], "gain0.7"); fd = agg(p["frozen"], "delay2"); fo = agg(p["frozen"], "obsn0.05")
    row.update(nodrift=f0["sr"] if f0 else None, jerk=f0["jerk"] if f0 else None, maxstep=f0["maxstep"] if f0 else None,
               gain07=fg["sr"] if fg else None, delay2=fd["sr"] if fd else None, obsn=fo["sr"] if fo else None)
    tg = agg(p["trig"], "gain0.7") if p["trig"] else None; td = agg(p["trig"], "delay2") if p["trig"] else None
    row.update(recover07=(tg["sr"] - fg["sr"]) if (tg and fg) else None, fooled=(td["sr"] - fd["sr"]) if (td and fd) else None,
               calib_corr=calib_corr(p["calib"]))
    table[k] = row

# ---------------------------------------------------------------- print
cols = ["lam", "s", "sig", "dc", "bc", "final", "nodrift", "jerk", "maxstep", "gain07", "delay2", "recover07", "fooled", "calib_corr"]
fmt = lambda v: "  -  " if v is None or (isinstance(v, float) and np.isnan(v)) else (f"{v:5.2f}" if isinstance(v, float) and abs(v) < 10 else f"{v:5.1f}")
print(f"{'pt':<4}" + "".join(f"{c:>10}" for c in cols))
for k, r in table.items():
    print(f"{k:<4}" + "".join(f"{fmt(r[c]):>10}" for c in cols))

# ---------------------------------------------------------------- figure: 5 panels on the (lam, s) plane
panels = [("bc", "1  prior alignment: BC success (%)", "viridis"),
          ("final", "2  RL trainability: final success (%)", "viridis"),
          ("maxstep", "3  smoothness: max executed step (lower=better)", "viridis_r"),
          ("gain07", "4  robustness: success under gain x0.7 (%)", "viridis"),
          ("fooled", "5  adaptation: estimator-fooled cost (pp, higher=better)", "viridis")]
fig, axes = plt.subplots(2, 3, figsize=(16, 9.2)); axes = axes.ravel()
lam_grid = np.linspace(0, 1, 101); s_grid = np.linspace(0, 1.05, 101); LG, SG = np.meshgrid(lam_grid, s_grid)
bound = (1 - LG) + SG   # P3 per-step bound (C_max = 1)


def pos(r):  # same (lam, s) for two training noises -> offset in s so both stay visible
    return r["lam"], r["s"] + (0.035 if r["sig"] >= 0.1 else -0.035) if sum(1 for q in table.values() if q["lam"] == r["lam"] and q["s"] == r["s"]) > 1 else r["s"]


for ax, (key, title, cmap) in zip(axes, panels):
    cs = ax.contour(LG, SG, bound, levels=[0.4, 0.7, 1.0, 1.3, 1.6], colors="#bbbbbb", linewidths=0.7)
    ax.clabel(cs, fmt="P3 %.1f", fontsize=6, colors="#888888")
    vals = {k: r[key] for k, r in table.items() if r[key] is not None and not (isinstance(r[key], float) and np.isnan(r[key]))}
    if vals:
        vmin, vmax = min(vals.values()), max(vals.values())
        sc_ref = None
        for k, r in table.items():
            v = r[key]; has = k in vals; x, y = pos(r)
            marker = "o" if r["obs"] else ("s" if r["lam"] > 0 else "D")
            edge = "#c0392b" if r["sig"] >= 0.1 else "#2c3e50"
            if has:
                sc_ref = ax.scatter(x, y, s=280, c=[v], cmap=cmap, vmin=vmin, vmax=vmax, marker=marker, edgecolors=edge, linewidths=1.8, zorder=3)
            else:
                ax.scatter(x, y, s=120, facecolors="white", marker=marker, edgecolors=edge, linewidths=1.0, zorder=3)
            ax.annotate(f"{k}  {fmt(v).strip() if has else '(pending)'}", (x, y), xytext=(8, -3), textcoords="offset points", fontsize=7.5)
        if sc_ref is not None:
            plt.colorbar(sc_ref, ax=ax, fraction=0.046, pad=0.02)
    ax.set_xlim(-0.06, 1.06); ax.set_ylim(0.05, 1.12); ax.set_xlabel("lambda (leak)"); ax.set_ylabel("s (scale)")
    ax.set_title(title, fontsize=9.5)
ax = axes[5]; ax.axis("off")
ax.text(0.0, 0.95, "Design space of first-order action filters\n  c_t = lambda * c_{t-1} + s * u_t\n\n"
        "raw policy         = (0, 1)        DC gain 1\nlow-pass alpha      = (alpha, 1-alpha)   DC gain 1\n"
        "derivative iface   = (lambda, s)   DC gain s/(1-lambda) > 1, state in obs\n\n"
        "marker  o = filter state observable (obs_cmd)\n        s = low-pass   D = raw\nedge    red = sigma_train 0.10   dark = 0.03\n"
        "contours  P3 per-step bound (1-lambda)+s (C_max=1)\n\n"
        "points: A E5 B E1 E4 measured (3 eval seeds, 1 train seed)\n        F1 F2 F3 F4 = Route-A points, training", fontsize=9, family="monospace", va="top")
plt.tight_layout(); os.makedirs("figures", exist_ok=True); plt.savefig("figures/DS_map.png", dpi=150); plt.close()

# ---------------------------------------------------------------- H9: executed exploration noise vs trainability / robustness
def sigma_exec(r, T=400):
    """Stationary executed exploration std s*sigma/sqrt(1-lam^2); for the pure integrator (lam=1) the
    random walk never becomes stationary, so use its end-of-episode std s*sigma*sqrt(T) (T = 400 env steps)."""
    if r["lam"] is None:
        return np.nan
    if r["lam"] >= 1.0:
        return r["s"] * r["sig"] * np.sqrt(T)
    return r["s"] * r["sig"] / np.sqrt(1 - r["lam"] ** 2)


# collapsed arms from the seven-arm study (final success only; no deployment evals)
EXTRA = {"E3": dict(lam=0.9, s=1.0, sig=0.10, final=12.5, gain07=None), "C": dict(lam=1.0, s=1.0, sig=0.10, final=24.5, gain07=None)}
H9_PRED = {"F5": (0, 5), "F1": (5, 15), "F2": (25, 40), "F3": (30, 45)}   # pre-registered gain x0.7 ranges (proposal §1.10, 09-06 17:50)
fig, ax = plt.subplots(1, 2, figsize=(12, 4.4))
pts = {k: dict(r, sx=sigma_exec(r)) for k, r in table.items()}
pts.update({k: dict(v, sx=sigma_exec(v), obs=True, bc=None) for k, v in EXTRA.items()})
for k, r in pts.items():
    if r["sx"] is None or (isinstance(r["sx"], float) and np.isnan(r["sx"])):
        continue
    x = r["sx"]
    col = "#c0392b" if r["sig"] >= 0.1 else "#2c3e50"
    mk = "o" if r.get("obs") else ("s" if r["lam"] > 0 else "D")
    if r.get("final") is not None:
        ax[0].scatter(x, r["final"], s=90, c=col, marker=mk, zorder=3); ax[0].annotate(k, (x, r["final"]), xytext=(5, 4), textcoords="offset points", fontsize=8)
    if r.get("gain07") is not None:
        ax[1].scatter(x, r["gain07"], s=90, c=col, marker=mk, zorder=3); ax[1].annotate(k, (x, r["gain07"]), xytext=(5, 4), textcoords="offset points", fontsize=8)
    elif k in H9_PRED:
        lo, hi = H9_PRED[k]
        ax[1].plot([x, x], [lo, hi], color="#7f8c8d", lw=6, alpha=0.35, solid_capstyle="butt", zorder=2)
        ax[1].annotate(f"{k} pred.", (x, hi), xytext=(4, 3), textcoords="offset points", fontsize=7.5, color="#7f8c8d")
for a, ttl, yl in ((ax[0], "H9a  RL trainability vs executed exploration noise", "final success after 200 itr (%)"),
                   (ax[1], "H9b  gain x0.7 robustness vs executed exploration noise", "frozen success under gain x0.7 (%)")):
    a.set_xscale("log"); a.set_xlim(0.007, 3.0); a.set_ylim(0, 105); a.set_xlabel("sigma_exec = s*sigma/sqrt(1-lambda^2)   (lambda=1: s*sigma*sqrt(T), T=400)"); a.set_ylabel(yl); a.set_title(ttl, fontsize=9.5)
    a.axvspan(0.03, 0.10, color="#2ecc71", alpha=0.08)
fig.text(0.5, 0.005, "red = sigma_train 0.10, dark = 0.03;  o = observable filter state, s = low-pass, D = raw;  grey bars = pre-registered ranges for pending points;  green band = trainability sweet spot",
         ha="center", fontsize=7.5)
plt.tight_layout(rect=(0, 0.04, 1, 1)); plt.savefig("figures/DS_h9.png", dpi=150); plt.close()
print("saved figures/DS_h9.png")

with open("design_space_table.md", "w", encoding="utf-8") as fo:
    fo.write("| point | lam | s | sigma | DC gain | BC | final | no-drift | jerk | max step | gain x0.7 | delay 2 | recover x0.7 | fooled cost | calib corr |\n|" + "---|" * 15 + "\n")
    for k, r in table.items():
        fo.write(f"| {k} | " + " | ".join(fmt(r[c]).strip() for c in cols) + " |\n")
json.dump(table, open("design_space_table.json", "w"), indent=1, default=lambda o: None if (isinstance(o, float) and np.isnan(o)) else float(o))
print("saved figures/DS_map.png")
