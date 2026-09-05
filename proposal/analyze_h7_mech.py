"""H7 mechanistic test from existing frozen rollouts (no new experiments needed).

Compensation ratio  R(g) = mean|exec_pos| under gain drift g / mean|exec_pos| no-drift.
  Integral-action hypothesis: interface arms (E1 ?=1, E4 ?=0.9) have R(g) > g
  (the integrator winds up to offset the multiplicative loss); the raw arm (E5) has R(g) ? g
  (a position-domain policy re-emits the same delta, so the executed delta stays scaled by g).
Also reports the lag-aligned alignment scores and the adaptation "active fraction" for
adapt=2 (plain triggered) vs adapt=3 (delay-aware v1, hard veto) to diagnose the veto rate.
"""
import os, json
import numpy as np

D = "p0_out"


def load(name):
    p = f"{D}/{name}.npz"
    if not os.path.exists(p):
        return None
    d = np.load(p, allow_pickle=True)
    out = dict(success=np.asarray(d["success"], np.float32),
               ex=[np.asarray(e, dtype=np.float32) for e in d["exec"]],
               u=[np.asarray(e, dtype=np.float32) for e in d["u"]])
    out["ghat"] = [np.asarray(g, dtype=np.float32) for g in d["ghat"]] if "ghat" in d.files else []
    return out


def mean_abs_exec(r, dims=(0, 1, 2)):
    vals = []
    for x in r["ex"]:
        if x.ndim == 2 and not np.isnan(x).any():
            vals.append(np.mean(np.abs(x[:, list(dims)])))
    return float(np.mean(vals)) if vals else float("nan")


def mean_abs_u(r, dims=(0, 1, 2)):
    return float(np.mean([np.mean(np.abs(x[:, list(dims)])) for x in r["u"]]))


# ---------------------------------------------------------------- compensation ratio
print("== H7 compensation ratio (frozen arms, 3 eval seeds) ==")
rows = []
arms = {"E4": "p1_E4_ad0", "E5": "p1_E5_ad0"}
# P0b single-seed files for E1 if present
p0_names = {"E1": "P0_E1", "E4p0": "P0_E4", "E5p0": "P0_E5"}
for arm, pref in arms.items():
    base_ex, base_u = [], []
    for s in (1000, 2000, 3000):
        r = load(f"{pref}_nodrift_s{s}")
        if r:
            base_ex.append(mean_abs_exec(r)); base_u.append(mean_abs_u(r))
    b_ex, b_u = np.mean(base_ex), np.mean(base_u)
    for g in (0.8, 0.7):
        ex_g, u_g, sr = [], [], []
        for s in (1000, 2000, 3000):
            r = load(f"{pref}_gain{g}_s{s}")
            if r:
                ex_g.append(mean_abs_exec(r)); u_g.append(mean_abs_u(r)); sr.append(r["success"].mean())
        R_exec = np.mean(ex_g) / b_ex
        R_u = np.mean(u_g) / b_u
        rows.append(dict(arm=arm, gain=g, R_exec=R_exec, R_policy=R_u, success=100 * np.mean(sr)))
        print(f"{arm}  gain x{g}:  R_exec = {R_exec:.3f}  (g = {g}, full comp = 1.0)   "
              f"policy-output ratio = {R_u:.3f}   success {100*np.mean(sr):.1f}%")

# E1 from P0 batch (single eval seed) if available
for tag in ("E1", "E4", "E5"):
    files = [f for f in os.listdir(D) if f.startswith(f"P0_{tag}_") or f.startswith(f"p0_{tag}_")]
    if not files:
        continue
    nod = [f for f in files if "nodrift" in f or "base" in f]
    print(f"   (P0 files for {tag}: {sorted(files)[:6]}{' ...' if len(files)>6 else ''})")

# ---------------------------------------------------------------- veto / active fraction
print("\n== adaptation active fraction (share of control steps with ? != 1) ==")
act = {}
for arm in ("E4", "E5"):
    for ad, pref in ((2, "p1"), (3, "p1d")):
        for c in ("nodrift", "gain0.8", "gain0.7", "delay2"):
            fr, gh, sr = [], [], []
            for s in (1000, 2000, 3000):
                r = load(f"{pref}_{arm}_ad{ad}_{c}_s{s}")
                if r is None or not r["ghat"]:
                    continue
                g = np.concatenate([x for x in r["ghat"] if len(x)])
                fr.append(np.mean(np.abs(g - 1.0) > 1e-6))
                on = g[np.abs(g - 1.0) > 1e-6]
                gh.append(float(np.mean(on)) if len(on) else np.nan)
                sr.append(r["success"].mean())
            if fr:
                act[(arm, ad, c)] = dict(active=float(np.mean(fr)), ghat_on=float(np.nanmean(gh)),
                                         success=100 * float(np.mean(sr)), n=len(fr))
                print(f"{arm} adapt={ad} {c:8s}: active {100*np.mean(fr):5.1f}%  ?|on {np.nanmean(gh):.3f}  "
                      f"success {100*np.mean(sr):5.1f}  (n={len(fr)})")

json.dump(dict(compensation=rows, active={f"{a}_ad{ad}_{c}": v for (a, ad, c), v in act.items()}),
          open("h7_mech_results.json", "w"), indent=1)
