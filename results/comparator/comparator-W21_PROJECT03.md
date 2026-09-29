# Comparator Analysis — W21 Project 03

---

## Human Issues

1. The scatterplot for the SIR global search shows that some combinations of parameters are well identified (e.g., trade-off between β, ρ and μ_IR). The flat likelihood surface shows that some combinations are unidentifiable. This is not a problem with the maximization, which reliably gets within 5-10 log units of the maximum. It is just a fact that the data follow exponential decay which can be described well by 2 or 3 parameters.

2. The ordinary differential equation (ODE) models written down do not perfectly match the POMP model implemented. The ODE is a deterministic skeleton corresponding to the POMP model.

3. The first SIRV model fits considerably better (8 units of log likelihood gained, for two degrees of freedom, the parameters u and σ). The model is still not fully identifiable, but that is not needed to do a likelihood ratio test.

4. The second SIRV model does not give this improvement in log likelihood, so gives a worse description of vaccination. One could investigate why, e.g., by looking at conditional log likelihoods to see which time points are less well described. A problem with the coding of this model is that there is a t² in the model for vaccination which is incorrectly included as dt² in the latent process model equations and code. That could explain some of the issue.

5. There could be benefits from running the code for longer, perhaps even using the greatlakes cluster.

6. For the fitted models, it might be useful for interpretation to calculate and discuss the R_0 values corresponding to the fitted parameters. Here, a simple formula is R_0 = β/μ_IR which is much less than one.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by findings: "SIRV1 V→I hazard uses V instead of I" and "SIRV1 S→V hazard is density-dependent, inconsistent with ODE")
- Human Issue #3: covered (matched by finding: "SIR model dismissed based on visual inspection of pair plots, not likelihood comparison")
- Human Issue #4: covered (matched by finding: "SIRV2 deterministic vaccination flow dN_SV can produce negative S without bounds check")
- Human Issue #5: covered (matched by finding: "Run level is set to 1 throughout — results computed with far too few particles and iterations")
- Human Issue #6: missed

**Findings classification:**
- Finding 1 [MAJOR] H tracks removals (dN_IR) not new infections: A — fundamental model misspecification not raised by human
- Finding 2 [MAJOR] Prediction uses initial-guess parameters not MLE: A — not raised by human
- Finding 3 [MAJOR] SIRV1 V→I hazard uses V instead of I: B — matches Human Issue #2 (ODE does not match POMP implementation)
- Finding 4 [MAJOR] SIRV1 S→V hazard is density-dependent, inconsistent with ODE: B — matches Human Issue #2 (ODE does not match POMP implementation)
- Finding 5 [MAJOR] Run level 1 throughout — too few particles and iterations: B — matches Human Issue #5 (benefits from running code longer)
- Finding 6 [MAJOR] Profile likelihood: Sigma not held fixed in first mif2 call: A — not raised by human
- Finding 7 [MAJOR] SIRV2 dN_SV can produce negative S without bounds check: B — matches Human Issue #4 (t² coded as dt² in SIRV2 vaccination term, same problematic dN_SV expression)
- Finding 8 [MODERATE] Local search uses only a single particle filter replication: C — not raised by human
- Finding 9 [MODERATE] CI cutoff for sigma computed but not plotted: C — not raised by human
- Finding 10 [MODERATE] Active cases used as I(0) conflates reported with true infectious: C — not raised by human
- Finding 11 [MODERATE] Vaccine efficacy conclusion ">80%" not supported by analysis: C — not raised by human
- Finding 12 [MODERATE] SIR model dismissed by visual inspection of pair plots, not likelihood comparison: D — matches Human Issue #3 (human notes SIRV1 improves likelihood by 8 units and an LRT would be valid)
- Finding 13 [MINOR] Vaccination regression fitted on same data used in POMP model: C — not raised by human
- Finding 14 [MINOR] Prediction plots show 5 simulations but text claims 10: C — not raised by human
- Finding 15 [MINOR] SIRV1 global search pair plot uses threshold of 1000 log units, too wide: C — not raised by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "SIRV Model 1 — two code errors inconsistent with stated equations")
- Human Issue #3: covered (matched by finding: "SIRV2 selected for final analysis despite SIRV1 having substantially higher log-likelihood")
- Human Issue #4: covered (matched by finding: "SIRV2 selected for final analysis despite SIRV1 having substantially higher log-likelihood")
- Human Issue #5: missed
- Human Issue #6: missed

**Findings classification:**
- Finding 1 (Major — H accumulator): A — Accumulator H tallies recoveries (dN_IR) rather than new infections (dN_SI) across all three models
- Finding 2 (Major — SIRV1 code errors): B — SIRV Model 1 two code errors inconsistent with stated equations: dN_VI uses V instead of I; dN_SV scales as S²/N rather than S/N (matches Human Issue #2)
- Finding 3 (Major — forecast uses wrong params): A — Final forecast simulation uses hand-tuned initial parameters rather than MLE stored in params_maxlik
- Finding 4 (Major — SIRV2 selected over SIRV1): B — SIRV2 selected for final analysis despite SIRV1 having ~8.75 log-likelihood units higher fit; no formal model selection criterion applied (matches Human Issues #3 and #4)
- Finding 5 (Major — overstated efficacy): A — Overstated vaccine efficacy conclusion given profile likelihood CI spanning nearly the entire (0,1) range for Sigma
- Finding 6 (Major — no benchmark): A — No non-mechanistic benchmark model fit for comparison
- Finding 7 (Major — CI cutoff omitted): A — CI cutoff line commented out of profile likelihood plot, making confidence interval endpoints unreadable
- Finding 8 (Minor — single pfilter): C — Local search log-likelihood re-evaluation uses single pfilter call without replication, producing unquantified Monte Carlo noise
- Finding 9 (Minor — no profiles for other params): C — Profile likelihoods computed only for Sigma; Beta, mu_IR, and rho identifiability never formally assessed
- Finding 10 (Minor — binomial, no overdispersion): C — Binomial measurement model used; COVID-19 case counts exhibit overdispersion warranting negative binomial
- Finding 11 (Minor — no process stochasticity): C — No environmental/process stochasticity beyond demographic noise; no multiplicative noise on transmission rates
- Finding 12 (Minor — no population bound on vaccination): C — Quadratic vaccination model extrapolation has no explicit population cap, creating potential edge cases
- Finding 13 (Minor — run level inconsistency): C — Rmd header sets run_level=1 but analysis loads cached results from run_level=2, making the code non-reproducible as submitted
- Finding 14 (Minor — no model comparison table): C — No table summarizing log-likelihoods or AIC for SIR, SIRV1, and SIRV2; comparison done informally in prose
- Finding 15 (Minor — forecast not from filtering distribution): C — Prediction simulates from t0=0 rather than conditioning on the filtering distribution at the end of the training period

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "SIRV2 vaccination rate formula inconsistency — dt² term in latent process model equations")
- Human Issue #5: covered (matched by finding: "Grossly insufficient computational effort (run_level = 1 throughout)")
- Human Issue #6: missed

**Findings classification:**
- Major 1 (Accumulator H tracks recoveries not infections): A — accumulator variable semantic mismatch across all three models
- Major 2 (Global search initialized from previous mif2 result): A — cooling schedule inherited from local search, preventing genuine global coverage
- Major 3 (Prediction step uses initial guess not MLE): A — forecast uses manually specified params instead of params_maxlik
- Major 4 (Grossly insufficient computational effort): B — run_level=1 with Np=100 and Nmif=10 throughout (matches Human Issue #5)
- Major 5 (No non-mechanistic benchmark comparison): A — no ARMA or other baseline model compared
- Major 6 (Profile likelihood sigma CI cutoff commented out): A — geom_hline for CI boundary commented out so no formal CI is shown
- Major 7 (SIRV model 1 incorrect force of infection): A — uses V/N instead of I/N in V→I transition probability
- Major 8 (Forecast not conditioned on filtering distribution): A — forward simulation from t=0 initial conditions, not from filtering distribution at Day 87
- Minor: Log-likelihood single-evaluation in local search: C — logmeanexp applied to single pfilter value
- Minor: Possible negative initial compartment R: C — R could go negative if eta approaches 1 and V0 is large
- Minor: SIRV2 vaccination rate formula inconsistency: D — dt² term in latent process model equations is the error the human identified in SIRV2 coding (matches Human Issue #4)
- Minor: No effective sample size diagnostics: C — ESS not monitored or reported
- Minor: No corroboration with scientific knowledge: C — estimated parameter values not compared to epidemiological literature
- Minor: Goodness-of-fit assessed only visually: C — no formal AIC table or quantitative model comparison
- Minor: Population scaling unit inconsistency: C — units not explicitly stated in the text
- Minor: Typo in conclusion: C — "EXISTING!" draft artifact not removed
- Minor: References year discrepancy: C — "Masaaki, Ishikawa (2012)" vs. "2021" in text

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: contradiction (AI 21.03.1 says computation is "critically insufficient" and "no conclusion... can be drawn from these results"; human says "not a problem with the maximization, which reliably gets within 5-10 log units of the maximum")
- Human Issue #2: covered (matched by finding: "SIRV1 vaccination transition probability S-dependence inconsistency — equation/code mismatch in the vaccination rate formula")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "SIRV1 outperforms SIRV2 in likelihood without explanation — SIRV2's unexplained underperformance")
- Human Issue #5: missed
- Human Issue #6: missed

**Findings classification:**
- 21.03.1: F — critically insufficient computation (contradicts Human Issue #1: AI says no conclusions can be drawn; human says maximization reliably gets within 5-10 log units)
- 21.03.2: A — no non-mechanistic benchmark comparison
- 21.03.3: A — forecast simulation uses starting-guess parameters, not MLE
- 21.03.4: A — accumulator H tracks recoveries rather than new infections
- 21.03.5: B — SIRV1 outperforms SIRV2 in likelihood without explanation (matches Human Issue #4)
- 21.03.6: C — profile likelihood for sigma has CI cutoff suppressed and too few points
- 21.03.7: D — SIRV1 vaccination transition probability has S-dependence inconsistency between equations and code (matches Human Issue #2)
- 21.03.M1: C — measurement model uses Binomial; overdispersion not considered
- 21.03.M2: C — EDA is limited; no ACF or log-scale examination
- 21.03.M3: C — computational settings hidden from rendered output
- 21.03.M4: C — minor writing errors ("agasinst", "EXISTING!")

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 1 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 3 | 5 | 7 | 3 |
| B (AI major, human also found) | 4 | 2 | 1 | 1 |
| C (AI minor, human missed) | 7 | 8 | 8 | 5 |
| D (AI minor, human also found) | 1 | 0 | 1 | 1 |
| E (Human found, AI missed) | 2 | 3 | 4 | 3 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 1 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 4 | 1 | 2 | 4/6 = 67% | 3 | 7 | 10/15 = 67% |
| Charlie | 2 | 0 | 3 | 3/6 = 50% | 5 | 8 | 13/15 = 87% |
| Doug | 1 | 1 | 4 | 2/6 = 33% | 7 | 8 | 15/17 = 88% |
| Evan | 1 | 1 | 3 | 2/5 = 40% | 3 | 5 | 8/10 = 80% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #6: For the fitted models, it might be useful for interpretation to calculate and discuss the R_0 values corresponding to the fitted parameters. Here, a simple formula is R_0 = β/μ_IR which is much less than one. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 1 out of 6 human issues (17%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
