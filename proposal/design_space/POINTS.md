# Design-space map points (Route A)

Unified notation: integrator `c_t = ? c_{t-1} + s�clip(u_t)`; lowpass `e_t = ? e_{t-1} + (1-?) u_t` ? `(?=?, s=1-?)`.

| ID | ? | s | mode | ?_train | obs_cmd | status | notes |
|---|---|---|------|---------|---------|--------|-------|
| A | � | � | off (raw) | 0.10 | � | **done** | strongest raw baseline |
| B | 0.8 | 0.2 | lowpass | 0.10 | � | **done** | filter null hypothesis |
| E1/C | 1.0 | 1.0 | integrate | 0.03/0.10 | yes | **done** | pure integrator |
| E3/E4 | 0.9 | 1.0 | integrate | 0.03 | yes | **done** | main interface arm |
| E5 | � | � | off | 0.03 | � | **done** | matched-budget weak twin |
| **F1** | 0.9 | 0.3 | integrate | 0.03 | yes | **train** | tighter P3 bound, same ? as E4 |
| **F2** | 0.7 | 1.0 | integrate | 0.03 | yes | **train** | pink-noise ? (P1) |
| **F3** | 0.95 | 0.5 | integrate | 0.03 | yes | **train** | high-? moderate scale |
| **F4** | 0.8 | 0.2 | lowpass | **0.03** | � | **train** | B with matched exploration budget |

Five evaluation axes (frozen deploy, 3 eval seeds � 100 ep unless noted):
1. BC prior (itr-0 success)
2. RL trainability (final success, seed 42)
3. Execution smoothness (jerk, max step, ??)
4. Deploy robustness (gain �0.7, obs noise ?=0.05)
5. Signal quality (calib corr, delay fooled cost)

| **F5** | 0.8 | 0.2 | integrate | 0.03 | yes | **train** | same filter as B; isolates retrained prior + observable state from DC gain |

BC-gate readings (09-06 07:40, seed 42, 200 ep): F1 58.5, F2 54.0, F3 59.5 (E4 49.0, E1 43.5, A/E5 38.0, B/F4 23.5 stock prior).
Smaller s -> better prior (label range utilization), opposite to the pre-registered Q1 direction.

| **F6** | 0.9 | 0.3 | integrate | **0.07** | yes | **train** (09-07 02:56) | F1's prior fine-tuned at sigma .07 (sigma_exec .048): candidate recommended configuration |

Finals: F1 94.0, F2 98.0, F3 99.0, F4 77.5. Gain x0.7 frozen: F1 15.0, F2 38.7, F3 45.7, F4 1.0 (H9 ranges hit 3/3; E4/E5 below trend).
