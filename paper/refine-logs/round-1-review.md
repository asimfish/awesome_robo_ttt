# Round 1 review: the mediation-first story card (2026-09-09)

Reviewer role: ICLR area chair, robot learning and RL, fresh read.
Files read in full: refine-logs/round-0-story.md (mediation-first card), paper/main.tex v0.3
(identity-first draft), paper/REVIEW_iclr_story_v0.1.md, proposal/design_space_table.md,
proposal/upstream_results.md.

Bottom line: the mediation-first thesis as carded ("exactly one lever", "not of interface
structure") is contradicted by Table 1 of the draft. The two-part thesis, in which the identity
explains why three quantities are left (noise exchange rate, previous-command conditioning,
target scale) and the map prices each, is the version that is true on the data and the one I
recommend. Details follow.

Notation (plain ASCII throughout): sigma_exec = s * sigma / sqrt(1 - lambda^2);
sigma_chunk = sigma_exec * sqrt(sum over i, j < H of lambda^|i-j|), with H = 4 so the
multiplier is 2.00 at lambda 0, 3.29 at 0.7, 3.52 at 0.8, 3.75 at 0.9, 3.88 at 0.95.
"O" means the policy observes c_{t-1}; "U" means it does not.

Evidence base for this review, recomputed from Table 1 and ordered by sigma_chunk:

    sigma_chunk  point  class  gain x0.7  delay 2  prior  final
    0.035        F4     U       1.0       64.7     23.5   77.5
    0.035        F5     O       4.0       73.3     59.5   94.0
    0.060        E5     U       3.7       80.0     38.0   93.0
    0.078        F1     O      12.0       74.7     58.5   94.0
    0.117        B      U      41.0       87.0     23.5   96.0
    0.117        F7     O      28.7       86.7     59.5   99.5
    0.138        F2     O      38.7       80.0     54.0   98.0
    0.181        F6     O      38.3       67.3     58.5   99.5
    0.186        F3     O      45.7       84.0     59.5   99.0
    0.200        A      U      81.3       91.0     38.0   99.5
    0.258        E4     O      28.3       87.3     49.0   95.0
    (E1, lambda = 1, non-stationary: gain 45.3, delay 83.0, prior 43.5, final 92.0)

Experimental scale is discussed only where it fixes how a claim must be worded.


## 1. KILL ARGUMENT

The headline claims one lever: the exchange rate from policy-side noise to executed
chunk-scale displacement, after which interface structure has no residual effect. Table 1
refutes it. Between the unobservable low-pass B (sigma_chunk 0.12, 41% under gain drift) and
the raw policy A (0.20, 81%) sit three observable-state configurations at 0.14 to 0.19, all at
38 to 46%, and above A sits E4 (0.26) at 28%. Either A is on the curve, so every
observable-state point above 0.12 lies below it by a deficit that grows from 12 points at 0.12
to 53 at 0.26, or A is the outlier, so robustness saturates near 45% and "the raw policy at
sigma 0.10 is the most robust configuration on the map" describes one run. The draft asserts
both. The cleanest twin, B against its observable-state copy F7 at identical lambda, s and
sigma, differs by 12 points; the 0.92 correlation is obtained by dropping the point with the
largest deficit, and a rank correlation cannot see a between-group offset. The paper's own
lemma predicts the residual: the observable-state
interface is the position policy plus previous-command conditioning, the textbook source of
shortcuts that actuator drift breaks. Trainability repeats the pattern: the sole low-noise
collapse (F4, 77.5%) has an observable twin at identical sigma_chunk that reaches 94%. Admit
the second lever and what remains is that more executed noise buys more gain-drift robustness,
a known result in a coordinate the interface rescales, plus a 12-to-53-point conditioning
penalty the framing has to call noise.


## 2. DEFENSE

The attack decomposes into six atomic points. Classification key:
answered_by_current_evidence = the data in hand answer it and only wording changes;
partially_answered = the data in hand address it and a small analysis or run closes it;
still_unresolved = the claim must be reworded now and a new run decides the fact.

### R1. "Structure has no residual effect after conditioning on sigma_chunk; E4 and F7 are two outliers."

Classification: still_unresolved.

Numbers that bear on it. Against the line joining the two unobservable points that bracket the
high-noise range, B (0.117, 41.0) and A (0.200, 81.3), the observable-state deficits are
F2 -13 (log-scale interpolation -15), F6 -33 (-35), F3 -29 (-30); E4 is 53 below A at a higher
sigma_chunk; F7 is 12 below B at the same sigma_chunk; F5 and F1 sit within 4 points of the
unobservable curve at low noise. So the penalty is 0 at sigma_chunk 0.035, 12 at 0.12, 13 at
0.14, 29 to 33 at 0.18 to 0.19, 53 at 0.26: a monotone interaction between observability and
noise, not two outliers. Five training seeds put E4 at 25.9 +/- 7.5, so the largest deficit is
not seed noise. Figure h9 is drawn against sigma_exec, where A (0.100) sits at twice the
abscissa of F3 and F6 (0.048) and the step reads as slope; in sigma_chunk, the coordinate the
text argues for, A, F3 and F6 are within 10% of one another on the x-axis and 35 to 43 points
apart on the y-axis. The draft cannot use sigma_chunk to repair the E5/B pair and sigma_exec to
hide the A/F3/F6 step. Two smaller wording errors follow from the same framing: L219 says E4
and E5 "both lie below the curve", but E5 (0.06, 3.7%) sits at the bottom of the curve, on it;
and observability is perfectly confounded with "retrained on relabelled data" for every
derivative point, because derivative labels are not identifiable without c_{t-1} (the 0% pilot),
so the map cannot currently say whether the penalty is conditioning or the prior.

What resolves it. Wording, now: replace "no residual effect except a penalty at two
observable-state points" with "an observability penalty that is zero at sigma_chunk 0.035, 12
points at 0.12 and 30 to 53 points at 0.18 to 0.26"; re-plot Figure h9 in sigma_chunk with the
two classes marked; word "the raw policy at sigma 0.10 is the most robust configuration on the
map" as a fact about one configuration and not about the trend. Evidence, three runs: (i) the
raw policy with c_{t-1} appended to its observation, fine-tuned at sigma 0.10 (same sigma_chunk
as A; if it falls from 81 toward 40 the penalty is conditioning and nothing else, and R1 becomes
the paper's second result); (ii) a raw policy at sigma 0.13 (sigma_chunk 0.26, E4's; already in
the plan as the sigma_chunk-matched twin); (iii) the unobservable low-pass (0.8, 0.2) at sigma
0.17 (sigma_chunk 0.20). Runs (ii) and (iii) fix the top of the unobservable curve; run (i)
separates conditioning from the retrained prior.

### R2. "rho = 0.92 is post hoc; a rank correlation does not test mediation; the counts are wrong; the pre-registration is unverifiable."

Classification: partially_answered.

Numbers that bear on it. The draft reports 0.76 with E4 and 0.92 without. Recomputed from
Table 1: eleven stationary points (twelve minus E1) give rho about 0.75 against sigma_chunk and
0.77 against sigma_exec; ten points without E4 give about 0.92. The values are right; the
counts in the text ("ten" and "nine") are off by one. The card asserts five of six
pre-registered ranges hit, and the text says F5 and F6 landed inside ranges predicted from
sigma_exec (4.0 and 38.3), but the six configurations, their predicted ranges and the miss
appear nowhere in the draft. From the numbers, F7 is the likely miss (predicted near B's 41 at
the same sigma_exec; observed 28.7). If so, the one miss is one of the two points the headline
calls outliers, and the pre-registration is evidence for R1, not against it.

What resolves it. Fix the counts. Report 0.76 as the headline statistic and 0.92 only inside
the same sentence as "excluding E4". Add the actual mediation test, which is cheap: residuals
from a monotone fit of gain-drift robustness on log sigma_chunk, split by observability (seven
against four), with a rank-sum test; if the observable residuals are systematically negative,
R1 is confirmed and belongs in the contributions. Print the pre-registration table
(configuration, predicted range, observed, hit or miss) in the appendix.

### R3. "The headline coordinate is chunk-scale, but nothing in the headline statistic prefers it to stationary variance."

Classification: partially_answered.

Numbers that bear on it. rho is 0.76 for both forms. The chunk form corrects two orderings the
stationary form gets wrong: E5 (sigma_exec 0.030, 3.7%) against B (0.033, 41.0%), and E5
against F1 (0.021, 12.0%). The mechanism is stated and is the right one: white noise
accumulates by a factor 2 over H = 4 while AR(1) noise at lambda 0.8 to 0.9 accumulates by 3.5
to 3.75, so at equal stationary variance the coloured noise is 1.75 to 1.9 times more visible
to a policy that replans every four steps. The H in {1, 4, 8} sweep that discriminates the two
forms is planned and not run. Note the coupling with R1: the coordinate that repairs E5/B is
the coordinate that exposes the A/F3/F6 step. The chunk-scale story and the no-residual story
cannot both be kept.

What resolves it. Wording: "sigma_chunk is the form that orders the two low-noise pairs
sigma_exec misorders; the H-sweep at fixed sigma_exec is the pre-registered discriminating
test." Do not headline "chunk-scale" as established. Evidence: the H-sweep, three
configurations.

### R4. "Drift robustness means actuator gain x0.7; delay robustness does not follow the trend; observation noise is measured for two points."

Classification: answered_by_current_evidence (a scope change; no new data).

Numbers that bear on it. The delay-2 column, in sigma_chunk order, is 64.7, 73.3, 80.0, 74.7,
87.0, 86.7, 80.0, 67.3, 84.0, 91.0, 87.3. There is no monotone relation; F6 at sigma_chunk 0.18
is the second-worst point on the map. The recipe F6 costs 20 points of delay robustness against
the original E4 (67.3 against 87.3) and 24 against A; the phrase "against the original on every
axis but delay" (L244) hides a 20-point loss. Observation-noise robustness appears for F6
against E4 (+11) and in the pilot (+29) and is not a column of Table 1.

What resolves it. Every mediation sentence says "actuator-gain drift". One added sentence in
Sec. 6: "Delay robustness is not ordered by sigma_chunk (Table 1). Training noise perturbs
displacement, not timing; the mediation covers perturbations in the span of the training
perturbation." Put the observation-noise column into Table 1 or remove observation noise from
the claims. State F6's delay cost where the recipe is given.

### R5. "Trainability is not a function of sigma_chunk alone."

Classification: answered_by_current_evidence (wording, plus moving two existing points into the table).

Numbers that bear on it. F4 (stock prior 23.5, unobservable) reaches 77.5% and F5 (retrained
prior 59.5, observable) reaches 94.0% at identical sigma_chunk 0.035; B (stock prior at sigma
0.10) reaches 96.0%. The right-arm collapses (12.5% at sigma_chunk about 0.86, 24.5% for a pure
integrator at sigma 0.10) are pilot points absent from Table 1; E1 (lambda = 1, sigma 0.03)
trains to 92.0%. The Sec. 6 sentence "94 to 99.5% for every point with sigma_exec in
[0.02, 0.10] and collapses outside it" is contradicted by F5 (sigma_exec 0.010, 94.0%), and the
card's "collapse below .04" is contradicted by the same point.

What resolves it. "Fine-tuning reaches 92 to 99.5% for sigma_chunk in [0.035, 0.26] whenever
the prior is at least 38%; at 0.035 the mismatched stock prior stalls at 77.5%; at sigma_chunk
0.86, and for a pure integrator at sigma 0.10, it collapses to 12.5 and 24.5%." Add the two
collapsed pilot points to Table 1; they exist.

### R6. "More noise gives more robustness is DART and dynamics randomization; the contribution is a bookkeeping rule."

Classification: partially_answered.

Numbers that bear on it. What is new is the coordinate and its invariance across interfaces:
raw (E5, A), low-pass (F4, B) and derivative (F5, F1, F2) points lie on one rising curve up to
sigma_chunk 0.14 (1.0, 4.0, 3.7, 12.0, 41.0, 38.7), the interface rescales the coordinate by
s / sqrt(1 - lambda^2) at stationary scale and by a further 1.75 to 1.9 at chunk scale without
any change to the policy-side sigma, and a comparison at matched policy-side sigma credited the
interface with 25 to 37 points it did not have. That the invariance breaks above 0.14 for
observable-state points (R1) is a second finding, not a refutation of the first.

What resolves it. One positioning sentence in the introduction: "DART and dynamics
randomization establish that training perturbation buys robustness; we establish the coordinate
in which that effect is invariant across action interfaces, and show that the interface rescales
it silently." Make the 25-to-37-point inflation the introduction's motivating example rather
than an appendix confession.


## 3. STORY VERDICT

### (a) Mediation-first, identity-first, or two-part

Neither single headline survives alone. Identity-first is the more defensible: the identity is
algebra a reviewer grants in one line, its corollaries are verified by predictions that cost no
rollouts (the lag-1 autocorrelation of the relabelled labels, demonstration-level jerk, absorbed
upstream corrections), and the impossibility result is the sentence people will quote. But it
does not carry the finding practitioners will act on, the noise-matching rule, and a reviewer
will say the identity concerns intent while every advertised benefit of a derivative interface
concerns exploration and robustness. Mediation-first carries the rule but, as carded, asserts a
one-lever law that Table 1 contradicts at matched sigma_chunk, and the framing forces the
authors to describe three observable-state points as a trend and two more as outliers. The
two-part thesis is stronger than either because it is the only one of the three that is true on
the paper's own data: the identity says an observable-state interface is a coordinate change
plus three quantities that integration does not create (the executed-noise exchange rate,
previous-command conditioning, target scale); the map prices each; and the observability
penalty stops being a residual and becomes the second finding, predicted by the lemma and
matching the copycat literature the draft already cites. It also gives the paper one
falsification test per quantity: the H-sweep for the exchange rate, the raw policy with c_{t-1}
appended for conditioning, the lambda = 0 corners for target scale. Headline the decomposition,
with the noise-matching rule as its first consequence and the conditioning penalty as its
second.

### (b) Score for the mediation-first story, experiments assumed adequate

5 / 10. The paper has a methodological result that changes practice (compare interfaces at
matched executed noise; matching policy-side sigma inflated an advantage by 25 to 37 points), a
twelve-point map built around named controls, pre-registered predictions, and an honestly
reported residual. Those are the ingredients of an accepted "what matters" analysis paper, which
at ICLR sits at 6 to 7. It scores 5 because the headline is falsified by the paper's own table
(R1), the headline coordinate is not preferred by the headline statistic (R3), the robustness
claim holds for one of the three perturbations the paper measures (R4), and the trainability
claim is contradicted by a twin pair in the table (R5). Each is a wording fix, but a paper whose
thesis sentence is false as printed does not get a champion at a 30% venue; reviewers reject
overclaims more reliably than they reject modest claims, and the overclaim here is one Table 1
exposes in ten minutes. The same material under the two-part thesis is a 6 on wording alone and
a 7 with the raw-plus-previous-command run, because that run converts the largest weakness into
the second result.

### (c) The thesis sentence, true given the evidence and its caveats

With the filter state observed, a derivative action interface is the position policy in other
coordinates, so it acts on RL fine-tuning through three quantities that integration does not
create: the target scale, which sets the imitation prior through label signal-to-noise; the
exchange rate from policy-side exploration noise to the displacement the plant sees within one
decision period, which sets the exploration fine-tuning tolerates and the actuator-gain-drift
robustness that exploration buys, and on which interfaces must be matched before they are
compared; and conditioning on the previous command, which raises the prior and costs drift
robustness that grows with that displacement.

Compact form for the first line of an abstract: An observable-state action interface is the
position policy in other coordinates; what it changes is how much exploration the plant sees,
how the target is scaled, and whether the policy sees its last command, and the map prices
each.

### (d) Title and abstract for the recommended version

Title: The Policy Inverts the Filter: Action Interfaces Reduce to a Noise Exchange Rate and a
Conditioning Choice

Alternative: What an Action Interface Can Change: An Identity, an Exchange Rate and a
Conditioning Cost

Abstract (124 words):

Velocity, increment and low-pass action interfaces promise smoother execution, easier RL
fine-tuning and robustness. All are one first-order filter, and when the policy observes the
filter state, as derivative labels require, the interface is the position policy in other
coordinates: integration changes nothing about intent. Two levers remain. Executed,
chunk-scale exploration displacement sets the exploration fine-tuning tolerates and the
actuator-drift robustness that exploration buys, so interfaces must be compared at matched
executed noise; matched policy-side noise credited one interface with 25 to 37 spurious points. Observing the previous command, with a rescaled target, raises the imitation
prior by 11 to 21 points and costs 12 to 53 points of drift robustness at high noise. Smoothing
intent and a trainable derivative prior are mutually exclusive.

### (e) Changes to the story card that would most raise the score, ranked

1. Rewrite the thesis and the contribution focus as the three-quantity decomposition; promote
   the observability penalty from "explicit non-contribution" to the second finding, sized as a
   function of sigma_chunk (0 at 0.035, 12 at 0.12, 30 to 53 at 0.18 to 0.26); delete "exactly
   one lever" and "not of interface structure". Reason: the current thesis is false on Table 1
   and the rewritten one is confirmed by it; the two points the card disowns become the
   evidence for the second result.

2. Add the decisive run to the validation plan: the raw policy with c_{t-1} appended to its
   observation, fine-tuned at sigma 0.10 and drift-tested, together with the already planned
   sigma_chunk-matched raw twin (sigma 0.13) and one unobservable low-pass at sigma_chunk about
   0.20. Reason: on the current map, conditioning is perfectly confounded with retraining on
   relabelled data, and the top of the unobservable curve is one configuration; these three runs
   decide whether the penalty is conditioning and whether A anchors a curve or is an anomaly.
   Without them the paper can only word the "no interface beats the raw policy at matched noise"
   claim as a fact about one raw configuration.

3. Scope "drift robustness" to actuator-gain drift everywhere; add the delay column to the
   claims as a stated negative with the displacement-versus-timing mechanism; state F6's 20-point
   delay cost next to the recipe. Reason: the delay data are already in Table 1 and contradict the
   unscoped claim; the recipe's success condition in the card ("land in the trainable, robust
   regime") is not met on delay.

4. Downgrade "chunk-scale" to "the form that orders the two low-noise pairs sigma_exec
   misorders" and keep the H-sweep as the pre-registered test; fix the point counts (eleven with
   E4, ten without); print the six pre-registered predictions with ranges and the miss; re-plot
   Figure h9 in sigma_chunk with observability marked. Reason: the headline statistic does not
   prefer the headline coordinate, and an off-by-one count plus an unnamed miss are the kind of
   detail that costs a paper its reviewers' trust in every other number.

5. Restate trainability as a plateau over sigma_chunk in [0.035, 0.26] with a prior-dependent
   low edge (F4 77.5 against F5 94.0 at identical noise) and an upper collapse, and move the two
   collapsed pilot points into Table 1. Reason: "inverted U in sigma_chunk" currently rests on one
   confounded point on the left and two off-table points on the right, and the Sec. 6 sentence
   about it is contradicted by F5.


## 4. WRITING NOTES

Line numbers refer to main.tex v0.3. Quotes are rendered from LaTeX to plain text.

1. L49, Introduction (project chronology and confession in the introduction).
   Current: "The map was built with four controls that we state in general form because our own
   pilot study, which compared the interface only against a raw policy fine-tuned at the same
   policy-side sigma, drew the opposite conclusions on three of the five axes (Appendix A)."
   Replacement: "Four controls (Sec. 5) decide which comparisons on the map are informative. The
   one most often omitted, matching executed rather than policy-side noise, reverses the
   conclusion on three of the five axes when it is left out (Appendix A)."

2. L47, Introduction (a "not what was advertised" hook with no content, then a cliche that delays
   the claim).
   Current: "Everything a derivative action space is said to buy follows from this identity, and
   most of it is not what was advertised." and, in the same paragraph, "Exploration noise is
   shaped, by the AR(1) transfer of (1), and this is a double-edged property: a high-DC-gain
   interface amplifies the executed noise by 1/sqrt(1-lambda^2) and therefore has to be fine-tuned
   at a smaller policy-side sigma, and it is the executed noise that governs both trainability
   and zero-shot robustness."
   Replacement: "The identity fixes what a derivative action space can buy: a prior from
   conditioning and target scale, coloured exploration noise, and nothing on smoothness of
   intent." and "The filter shapes exploration noise through the AR(1) transfer of (1): a
   high-DC-gain interface amplifies executed noise by 1/sqrt(1 - lambda^2), so it must be
   fine-tuned at a smaller policy-side sigma, and executed noise is what governs trainability and
   actuator-gain-drift robustness."

3. L54, Contribution 2, echoed at L33 in the abstract (a false clause carried by "not X"
   scaffolding, plus chronology).
   Current: "after conditioning on it, structure has no residual effect except a penalty at two
   observable-state points consistent with copycat-type causal confusion. Comparisons between
   action spaces must match sigma_chunk, not the policy-side sigma; matched-sigma comparisons
   produced +25 to +37 percentage points of spurious advantage in our pilot."
   Replacement: "Trainability and actuator-gain-drift robustness rise with the executed,
   chunk-scale exploration noise for raw, low-pass and derivative interfaces (Spearman 0.76 over
   eleven configurations). Observable-state policies pay a drift penalty on top, zero at low noise
   and 12 to 53 points at sigma_chunk above 0.1, consistent with copycat-type causal confusion.
   Comparisons between action spaces must therefore match sigma_chunk; a comparison at matched
   policy-side sigma credited one interface with 25 to 37 points it did not have."
   Abstract L33, current: "Trainability and drift robustness are mediated by the executed,
   chunk-scale exploration noise, not by structure". Replacement: "Trainability and
   actuator-gain-drift robustness follow the executed, chunk-scale exploration noise for every
   interface, with an observability penalty of 12 to 53 points on top at high noise".

4. L244, Sec. 8 (buries the paper's most important number behind a wrong attribution; "still
   does not match" is defensive).
   Current: "It still does not match the raw policy at sigma=0.10 on zero-shot robustness (38 vs
   81%), as rule 1 predicts."
   Replacement: "At nearly matched executed noise (sigma_chunk 0.18 against 0.20) it trails the
   raw policy by 43 points on gain-drift robustness and 24 points on delay; the gap is the
   observability penalty of Sec. 6, and the recipe buys its other gains at the price of delay
   robustness."
   Rule 1 (match executed noise) does not predict this gap: F6 and A are already matched to
   within 10% in sigma_chunk.

5. L180, Sec. 5 (a sentence whose only function is to pre-empt the objection that whitening makes
   the filter inert; the measurement carries the point alone).
   Current: "Fact 1 is nonetheless real for perturbations: in stochastic rollouts the executed
   exponent of E4 rises to 2.1-2.5 against 0.9 for its raw twin."
   Replacement: "The filter's shaping is visible where the identity says it should be, on
   perturbations: in stochastic rollouts E4's executed spectral exponent is 2.1 to 2.5 against
   0.9 for its raw twin."
   The same pattern recurs at L223 ("the bound is real": delete the clause, the 1.40x against
   6.11x jerk ratio is the bound) and at L252 ("We hope the map, the identity and the four
   controls make the next action-space proposal cheaper to evaluate and harder to over-claim":
   replace with "The map, the identity and the four controls give the next action-space proposal
   a null hypothesis to beat and one number to match").
