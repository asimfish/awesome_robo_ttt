"""Figures for the CADI x TTT proposal v2.
T1/T2: numerical checks of Propositions 1-2 (synthetic, no experimental claim).
E1/E2: real seven-arm results from the CADI Square experiments (single seed, s42)."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import welch
rng = np.random.default_rng(0)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
C = {"A":"#7f8c8d","B":"#2980b9","C":"#c0392b","E1":"#e67e22","E3":"#8e44ad","E4":"#16a085","E5":"#2c3e50"}

# ---------- T1: spectrum shaping by a leaky integrator ----------
def leaky(eps, lam, s=1.0):
    c = np.zeros_like(eps); acc = 0.0
    for t, e in enumerate(eps):
        acc = lam*acc + s*e; c[t] = acc
    return c
T = 2**15; eps = rng.standard_normal(T)
lams = [0.0, 0.7, 0.9, 0.97, 1.0]
fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
betas = []
for lam in lams:
    c = leaky(eps, lam); f, P = welch(c, nperseg=2048)
    m = (f > 0.005) & (f < 0.2)
    b = -np.polyfit(np.log(f[m]), np.log(P[m]), 1)[0]; betas.append(b)
    ax[0].loglog(f[1:], P[1:], label=f"λ={lam}  (β̂={b:.2f})")
ax[0].set_xlabel("normalized frequency"); ax[0].set_ylabel("PSD of executed command c_t")
ax[0].set_title("T1a  White noise → leaky integrator: spectrum coloring"); ax[0].legend(fontsize=8)
lam_grid = np.linspace(0, 0.995, 40); bg = []
for lam in lam_grid:
    c = leaky(eps, lam); f, P = welch(c, nperseg=2048); m = (f > 0.005) & (f < 0.2)
    bg.append(-np.polyfit(np.log(f[m]), np.log(P[m]), 1)[0])
ax[1].plot(lam_grid, bg, color="#16a085"); ax[1].axhline(1.0, ls="--", color="#e67e22", lw=1)
ax[1].text(0.02, 1.05, "pink noise β=1 (Eberhard et al. 2023 optimum)", color="#e67e22", fontsize=8)
ax[1].set_xlabel("leak λ"); ax[1].set_ylabel("fitted spectral exponent β̂"); ax[1].set_title("T1b  λ is a noise-colour knob")
for lam in [1.0, 0.97, 0.9, 0.7]:
    c = leaky(rng.standard_normal(2000), lam)
    ax[2].plot(np.abs(c), lw=0.8, label=f"λ={lam}")
ax[2].set_xlabel("step"); ax[2].set_ylabel("|c_t|  (σ=1, s=1)"); ax[2].set_title("T1c  λ=1: random walk (Arm C); λ<1: bounded")
ax[2].legend(fontsize=8)
plt.tight_layout(); plt.savefig("figures/T1_spectrum_shaping.png", dpi=160); plt.close()

# ---------- T2: bounded propagation of an upstream perturbation ----------
def track(cmd, kp=8.0, kd=4.0, dt=0.05):
    """double-integrator plant tracked by a PD controller; cmd is the position reference."""
    x = v = 0.0; xs = []
    for r in cmd:
        a = kp*(r-x) - kd*v; v += a*dt; x += v*dt; xs.append(x)
    return np.array(xs)
N = 200; delta = 0.05  # sustained upstream bias Δ (units of derivative command)
fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
for lam in [1.0, 0.97, 0.9, 0.7]:
    bias = np.full(N, delta); c = leaky(bias, lam, s=1.0)
    ax[0].plot(c, label=f"λ={lam}" + ("  (unbounded)" if lam==1 else f"  → sΔ/(1-λ)={delta/(1-lam):.2f}"))
    ax[1].plot(track(c), label=f"λ={lam}")
ax[0].set_title("T2a  Sustained bias Δ=0.05 in policy output → command deviation"); ax[0].set_xlabel("step"); ax[0].set_ylabel("δc_t"); ax[0].legend(fontsize=8)
ax[1].set_title("T2b  Plant deviation after PD tracking"); ax[1].set_xlabel("step"); ax[1].set_ylabel("δx_t"); ax[1].legend(fontsize=8)
plt.tight_layout(); plt.savefig("figures/T2_bounded_propagation.png", dpi=160); plt.close()

# ---------- E1/E2: real seven-arm results (robomimic Square, seed 42, itr 0..200 step 10) ----------
raw = {
 "A  raw DPPO, σ=0.10":            ("A", [0.3800,0.5250,0.6250,0.7250,0.8050,0.8250,0.8900,0.8900,0.9500,0.9450,0.9450,0.9400,0.9850,0.9700,0.9900,0.9850,0.9750,0.9850,1.0000,0.9950,0.9950]),
 "B  lowpass, σ=0.10":             ("B", [0.2350,0.2950,0.3650,0.4350,0.5350,0.6200,0.7000,0.7700,0.7500,0.7850,0.8050,0.8550,0.9100,0.9000,0.9300,0.9350,0.9350,0.9550,0.9400,0.9350,0.9600]),
 "C  integrator λ=1, σ=0.10":      ("C", [0.4350,0.0200,0.0200,0.0300,0.0350,0.0300,0.0350,0.0350,0.0250,0.0500,0.0600,0.0550,0.0600,0.0300,0.1100,0.1300,0.1200,0.1400,0.2400,0.2050,0.2450]),
 "E1 integrator λ=1, σ=0.03":      ("E1",[0.4350,0.1750,0.1250,0.2550,0.3900,0.4250,0.6000,0.6050,0.6900,0.6950,0.7750,0.8950,0.8700,0.8700,0.9050,0.8750,0.8600,0.8700,0.8650,0.9250,0.9200]),
 "E3 leaky λ=0.9, σ=0.10":         ("E3",[0.4900,0.0000,0.0000,0.0000,0.0050,0.0150,0.0050,0.0200,0.0150,0.0400,0.0150,0.0600,0.0450,0.0600,0.0450,0.1400,0.1150,0.0700,0.0900,0.0600,0.1250]),
 "E4 leaky λ=0.9, σ=0.03":         ("E4",[0.4900,0.3150,0.4250,0.5100,0.5100,0.5150,0.7050,0.7050,0.7900,0.8200,0.8450,0.9300,0.8650,0.8900,0.9350,0.8950,0.9300,0.9000,0.9350,0.9150,0.9500]),
 "E5 raw DPPO, σ=0.03":            ("E5",[0.3800,0.3650,0.5300,0.5850,0.5900,0.5950,0.6600,0.7750,0.7950,0.7550,0.7700,0.7600,0.7950,0.8000,0.8800,0.8650,0.8600,0.9100,0.8600,0.8550,0.9300]),
}
itrs = np.arange(0, 201, 10)
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
for name, (k, ys) in raw.items():
    ax[0].plot(itrs, np.array(ys)*100, color=C[k], lw=2 if k in ("E4","E5") else 1.3, ls="-" if "0.03" in name else "--", label=name)
ax[0].set_xlabel("DPPO fine-tuning iteration"); ax[0].set_ylabel("success rate (%)  [200 eval episodes]")
ax[0].set_title("E1  Seven arms, robomimic Square (seed 42; dashed σ=.10, solid σ=.03)", fontsize=9.5); ax[0].legend(fontsize=7.5, loc="lower right"); ax[0].set_ylim(0, 102)
names = ["A","B","C","E1","E3","E4","E5"]; finals = [99.5,96.0,24.5,92.0,12.5,95.0,93.0]; starts=[38.0,23.5,43.5,43.5,49.0,49.0,38.0]
x = np.arange(len(names))
ax[1].bar(x-0.2, starts, 0.4, color="#bdc3c7", label="BC start (itr 0)")
ax[1].bar(x+0.2, finals, 0.4, color=[C[n] for n in names], label="after 200 itr")
for i,(s,f) in enumerate(zip(starts,finals)): ax[1].text(i+0.2, f+1, f"{f:.1f}", ha="center", fontsize=8)
ax[1].set_xticks(x); ax[1].set_xticklabels(["A raw\nσ.10","B lowpass\nσ.10","C int\nσ.10","E1 int\nσ.03","E3 leak\nσ.10","E4 leak\nσ.03","E5 raw\nσ.03"], fontsize=8)
ax[1].set_ylabel("success rate (%)"); ax[1].set_title("E2  Kill-test read: at matched σ=.03, E4 ≈ E5 ≈ E1 (single seed)", fontsize=9.5); ax[1].legend(fontsize=8)
ax[1].axhspan(90, 100, color="#16a085", alpha=0.07)
plt.tight_layout(); plt.savefig("figures/E1_seven_arms.png", dpi=160); plt.close()
print("betas for", lams, "->", [round(b,2) for b in betas])
