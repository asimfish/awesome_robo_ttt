# Story card, round 0 (2026-09-09)

## Problem Anchor (frozen)

- **Bottom-line problem.** Practitioners who fine-tune imitation-learned robot policies with RL must choose an action interface: position deltas, velocities, increments integrated by the controller, low-pass filtered commands, action chunks. The choice moves fine-tuning success and deployment robustness by tens of percentage points on the same task and pipeline, and there is no model of why. Published comparisons hold the policy-side exploration noise fixed and reach conflicting conclusions.
- **Must-solve bottleneck.** Without a model, every interface proposal is evaluated as "our interface vs. one baseline at the same sigma", and such comparisons are confounded by the quantity the interface itself changes.
- **Non-goals.** A new interface; a new RL algorithm; smoothness-as-constraint tasks; real-robot validation in this paper.
- **Constraints.** DPPO pipeline, robomimic Square (second task pending), diffusion MLP policies, shared 8-GPU server; 12 trained configurations exist; camera-ready quality figures pending.
- **Success condition.** A reader who is about to compare two action interfaces knows (a) which single quantity to report and match, (b) what the interface cannot change, and (c) how to set (lambda, s, sigma) to land in the trainable, robust regime; and the paper's pre-registered predictions for held-out configurations hit.

## One-sentence thesis

An action interface has exactly one lever on the RL fine-tuning problem: it sets the exchange rate between the exploration noise the policy emits and the perturbation the plant receives within one decision period; when the policy observes the interface state, everything else about the interface is a change of coordinates.

## Contribution focus

- **Dominant contribution (mediation).** Trainability and drift robustness of RL-fine-tuned diffusion policies are functions of the executed, chunk-scale exploration noise sigma_chunk = s*sigma*sqrt(sum_{i,j<H} lambda^|i-j|) and not of interface structure. Evidence: 12 configurations across raw, low-pass, derivative interfaces and sigma in {.03,.07,.10}; trainability is an inverted U in sigma_chunk (collapse below .04 and above .5); gain-drift robustness is monotone (Spearman .76 over 10, .92 over 9); five of six pre-registered robustness ranges for held-out configurations hit; the same twin comparison at matched sigma produced +25-37 pp of spurious advantage.
- **Supporting contribution (identity).** For the derivative interface, closed-loop relabelling u_t=(a_t-lambda c_{t-1})/s substituted into c_t=lambda c_{t-1}+s u_t gives c_t=a_t: an observable-state interface is the position policy in other output coordinates, so it cannot change intent, only perturbations. Verified corollaries: labels are the demonstration pre-whitened by lambda (in the data before training; lag-1 autocorrelation predicted in closed form); deterministic execution has demonstration smoothness (jerk .07-.13 vs demo .107; unobservable low-pass twin .03); upstream corrections are absorbed (27-36% vs 92-93% for the unobservable twin).
- **Explicit non-contributions.** A recommended interface (we give a recipe, F6, as an example of the rules, not as a method); smoothing of intent (impossible with an observable state); a theory of the two below-trend points (E4, F7; hypothesis and test stated).

## Formulation

- Interface family: c_t = lambda c_{t-1} + s u_t; raw (0,1), low-pass (alpha, 1-alpha), derivative s/(1-lambda) > 1 with c_{t-1} in the observation.
- Exchange rate: white policy-side noise sigma -> executed AR(1) with sigma_exec = s sigma / sqrt(1-lambda^2); displacement visible within a chunk of H steps: sigma_chunk = sigma_exec * sqrt(sum_{i,j<H} lambda^|i-j|) (= 2 sigma for white noise at H=4; 3.5-3.9 sigma_exec for lambda in [.8,.95]).
- Identity: c_t = a_t under closed-loop relabelling with observed state; corollaries (i)-(iv).
- Design equations: choose (lambda, s, sigma) so that sigma_chunk lands in the trainable band; choose s so that label magnitude clears the generative model's output-noise floor (prior improves 49 -> 58.5 as s goes 1 -> .3); choose observability by whether intent smoothing or a derivative prior is wanted (they exclude each other).

## Claim-driven validation (existing + planned)

- Claim 1 (mediation): map of 12 points; pre-registered ranges; controls C1-C4. Planned: H in {1,4,8} at fixed sigma_exec (sigma_chunk collapse should tighten, sigma_exec's should not); a sigma_chunk-matched raw twin for the original interface; second task (Transport).
- Claim 2 (identity): dataset-label autocorrelation vs closed form; F4/F5 and B/F7 twins; upstream vs downstream compensation. Planned: lambda=0 corner points (running) separating previous-command conditioning from target scaling; history dropout for the E4/F7 residual.

## Why this is timely

RL fine-tuning of diffusion/VLA policies (DPPO, Q-chunking, ReinFlow-style) is now the default post-training recipe; every such system carries an action-interface choice as a hidden hyperparameter; the paper gives the one number to report.
