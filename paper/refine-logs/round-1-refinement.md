# Round 1 refinement (2026-09-09)

Reviewer verdict on the round-0 (mediation-first) card: 5/10; the "one lever / no residual effect of structure" thesis is contradicted by Table 1 (observable-state points sit 12-53 points below unobservable ones at equal sigma_chunk). Recommended: two-part thesis = identity + three quantities (target scale, noise exchange rate, previous-command conditioning), with the observability penalty as the second finding.

## Adopted (paper v0.4, deck v0.4)
- Thesis rewritten as the three-quantity decomposition; title: "What an Action Interface Can Change: An Identity, a Noise Exchange Rate, and a Conditioning Cost"; abstract from the review (adapted).
- Contribution 3 = conditioning cost, sized as a function of sigma_chunk (+3 at 0.035, -12 at 0.12, -30/-35 at 0.18-0.19, -53 at 0.26); B vs F7 as the cleanest pair; 6/7 observable residuals negative, mean -21 (sign test p=0.062).
- Robustness claims scoped to actuator-gain drift; delay reported as a stated negative with the displacement-vs-timing mechanism; F6's 20-point delay cost stated next to the recipe; the F6-vs-A gap attributed to the conditioning cost, not to rule 1.
- Trainability restated as a plateau over sigma_chunk in [0.035, 0.26] with a prior-dependent low edge (F4 77.5 vs F5 94.0) and an upper collapse; E3 and C pilot points added to Table 1.
- Counts fixed (eleven stationary points / ten without E4; rho 0.74 / 0.90 in sigma_chunk; 0.76 / 0.92 in sigma_exec); pre-registration table (6 rows, F7 = miss) in Appendix B.
- Figure 2 re-plotted in sigma_chunk with observability marked and the unobservable reference curve (figures/DS_h9_chunk.png).
- Writing notes 1-5 applied: no chronology or confession in the introduction; "not X but Y" scaffolds removed; pre-emptive clauses ("the bound is real", "nonetheless real") deleted; conclusion sentence replaced.
- Case study kept as Appendix A, reframed as "what a matched-sigma comparison credited to the interface".

## Launched (server, 09-09 01:51)
- R1: raw policy + c_{t-1} in observation (C2 prior), fine-tuned at sigma .10 (sigma_chunk 0.20 = A). Prediction: conditioning-cost hypothesis -> gain x0.7 falls from 81 toward 40; retraining hypothesis -> stays near 81.
- R0: C1 prior (no obs, retrained) at sigma .10: retraining control.
- R2: raw at sigma .13 (sigma_chunk 0.26 = E4). R3: unobserved low-pass (0.8,0.2) at sigma .17 (sigma_chunk 0.20). Prediction: both >= 75 under gain x0.7 (top of the unobservable curve).
- lambda=0 corner points C1-C4 (BC only) finishing ~03:00.

## Still open
- H-sweep (chunk-scale vs stationary coordinate); history dropout (causal-confusion test); second task.
- Figure polish for camera-ready; code URL; affiliation.
