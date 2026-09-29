# Comparator Analysis — W22 Project 14

---

## Human Issues

1. One could use t-distributed returns within a stochastic volatility model, with or without leverage.

2. The ARMA models should have been fitted to the return (difference of log price) rather than the raw data. It is not immediately clear from the text what is intended, but the code reveals they are fitted to the raw data.

3. The AR-Garch model is undefined. Better to write out a model specification when doing applied statistics, but especially for a model that may be unfamiliar to the reader.

4. The convergence diagnostics for the Breto model are disappointing, showing decreasing likelihoods and substantial variation. This could indicate model misspecification of some kind.

5. The local search for the stochastic volatility model has nice consistent results, but also shows a steady decline in the likelihood as the random walk variance on parameters is reduced, indicative of model misspecification. Maybe t-distributed returns would help with this?

6. In the Heston model, the authors also illustrate the model formulas and useful notations. However, for the first plot, there is no proper interpretation or caption to describe which row is the simulated volatility or the actual volatility.

7. It would be helpful (and maybe interesting) to compare simulations from all the fitted models.

8. Typo: The Heston model notation for the Brownian motions is a bit unclear. Maybe, $W=(W^s,W^\nu)$ should be a bivariate Brownian motion?

9. Typo: Fixing $\mu=1$ looks like a typo; fixing $\mu=0$ is a more natural simplification and matches what happened in the code (or, rather, the returns are de-meaned to make $\mu=0$ appropriate).

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (Critical State Equation Mismatch Between Model and Code): A — Heston C code uses `phi*sqrt(V)` instead of `phi*V`, fundamentally altering the stochastic process
- Finding 2 (Bake/Stew Files Are Absent): A — cached output files missing; results cannot be independently reproduced
- Finding 3 (Mixing Caching Mechanisms Inconsistently): A — Breto uses `bake()`/`.rds` while Heston uses `stew()`/`.rda`; duplicate bake calls risk cache mismatch
- Finding 4 (Log-Likelihood Comparison on Different Scales/Datasets): A — ARMA-GARCH fit on 9000-obs subset while POMP models use full dataset, making raw log-likelihood comparison invalid
- Finding 5 (Variable Name Typo Breaks Breto Local Search Code): A — `eth.sd_ivp` (dot) referenced but declared variable uses underscore `eth_rw.sd_ivp`
- Finding 6 (Global Search Box Contains Physically Unreasonable Ranges): A — `theta` up to 4 implies 200% SD of returns, orders of magnitude beyond observed data scale
- Finding 7 (No AIC or Likelihood Ratio Test for Formal Model Comparison): A — conclusion that Heston is best rests on raw log-likelihoods with no penalty for parameters or SE of estimate
- Finding 8 (No Simulation-Based Diagnostic for Heston Model): A — Section 4.2 particle filter runs on simulated data rather than real data, conflating diagnostics
- Finding 9 (Misidentification of May 19 2021 Crash Source): C — attributes broad crypto selloff to Russian hackers stealing Bitcoin rather than China's mining restrictions
- Finding 10 (Reference Section Is Empty): C — Section 6 heading has no content; references are embedded only as footnotes
- Finding 11 (Heston Process Constraints Are Weak): C — `if(V < 0){V = 0;}` reflecting boundary not part of Heston model; may bias parameter estimates
- Finding 12 (eth_Nreps_local Set to 20 for Both Local and Global Breto Searches): C — asymmetry in computational effort between POMP models not discussed
- Finding 13 (Cooling Schedule Fixed Without Justification): C — `cooling.fraction.50 = 0.5` used in both POMP models with no sensitivity analysis
- Finding 14 (Heston Model Description Credits Project 16 W18 But Departs Without Explanation): C — source project adaptation not fully transparent given additional departure in state equation
- Finding 15 (Pairs Plot Filtering Inconsistency): C — Breto pairs plot filters to top 50 log units but Heston pairs plot uses all runs unfiltered

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Breto model convergence failure interpreted incorrectly — declining LL in MIF2 is model misspecification, not merely numerical difficulty")
- Human Issue #5: covered (matched by finding: "Breto model convergence failure interpreted incorrectly — declining LL in MIF2 is model misspecification, not merely numerical difficulty")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "No simulation-based diagnostics / goodness-of-fit assessment — no plots comparing simulated trajectories to observed data")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (Heston code vs model equation mismatch): A — phi*sqrt(V) in code vs phi*V in stated equation; all Heston results invalid
- Finding 2 (Likelihood comparison mixing AIC and log-likelihood, possible different data lengths): A — cross-model likelihood comparison treated as valid despite scale and dataset inconsistencies
- Finding 3 (No profile likelihood analysis): A — no profile likelihoods, no parameter identifiability assessment, no confidence intervals
- Finding 4 (Breto convergence failure misinterpreted): B — declining LL in MIF2 is model misspecification not numerical noise (matches Human Issues #4 and #5)
- Finding 5 (6000-unit likelihood gap between Heston and Breto unexplained): A — implausible gap not remarked upon or investigated
- Finding 6 (Variable name error eth.sd_ivp vs eth_rw.sd_ivp): A — name collision bug; outer rw.sd object would fail if run
- Finding 7 (Breto global search phi range 0.97–0.99 not truly global): A — extremely narrow box does not meaningfully explore parameter space
- Finding 8 (AIC vs POMP likelihood comparison without justification): C — different package normalizations not verified before drawing conclusions
- Finding 9 (bake() called twice on same file): C — subtle reproducibility issue; mif2 objects and log-likelihoods may not correspond
- Finding 10 (No simulation-based diagnostics): D — no plots comparing simulated trajectories to observed data (matches Human Issue #7)
- Finding 11 (Heston covariate table set up but unused): C — covaryt loaded but not referenced in rproc C snippet; harmless but confusing
- Finding 12 (Heston local search: large ivp(0.2) for V_0, only 20 reps; pairs plot commented out): C — pairs plot for global search missing; local search diagnostic incomplete
- Finding 13 (Parameter interpretation absent): C — no comparison of fitted parameter values to literature or financial domain expectations
- Finding 14 (Missing references section): C — Section 6 labeled "Reference" but empty; citations only as inline footnotes
- Finding 15 (Confusing language about likelihood scale in Section 3.2): C — numerical claims about log-unit gaps are imprecise and should be stated with actual log-likelihood values

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Non-Convergence of Both POMP Models Is Explicitly Acknowledged but Results Are Still Interpreted")
- Human Issue #5: covered (matched by finding: "Non-Convergence of Both POMP Models Is Explicitly Acknowledged but Results Are Still Interpreted")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (Breto Global Search Initialized from Previous mif2 Result): A — global search inherits cooled perturbation schedule from prior IF2 chain, invalidating coverage claim
- Finding 2 (Breto Initial Particle Filter Evaluated on Simulated Data): A — pfilter run on sim1.filt not eth.filt, making the benchmark log-likelihood meaningless for real-data comparison
- Finding 3 (Heston rprocess Algebraically Misspecified): A — code applies sqrt(V) to autoregressive term, departing from stated equation phi*V
- Finding 4 (Non-Convergence of Both POMP Models Acknowledged but Results Still Interpreted): B — authors explicitly note convergence failures yet report and compare log-likelihood values as if they are MLEs (matches Human Issues #4 and #5)
- Finding 5 (No Profile Likelihoods or Confidence Intervals): A — key parameters estimated with no uncertainty quantification and no identifiability assessment
- Finding 6 (AIC Comparison Does Not Account for Monte Carlo Noise): A — exact GARCH/ARMA likelihoods compared to noisy POMP estimates without SE reporting
- Finding 7 (bake() Cache Double-Evaluation Pattern): A — same cache filename called twice; fragile code structure that would break if cache is cleared
- Finding 8 (Missing Model Diagnostics: No Conditional Log-Likelihoods, ESS Plots, or Simulation Envelopes): A — no conditional log-likelihoods, no ESS time series, no simulation envelopes overlaid on observed returns
- Finding 9 (Undefined Variable eth.sd_ivp in Breto rw.sd): C — dead code with typo in outer rw.sd definition; does not affect cached computation
- Finding 10 (Heston phi Search Box Spans (0,1) on logit-Transformed Scale): C — box effectively unconstrained on logit scale, inconsistent with text's implied constraint
- Finding 11 (Breto sigma_eta Search Box Implausibly Wide at 0.5–600): C — three-order-of-magnitude range not discussed; no check whether MLE is interior or boundary
- Finding 12 (Heston Local Search rw.sd Defined but Different Value Effectively Used): C — unused crypto_rw.sd_rp/ivp variables create confusion about which rw.sd was applied
- Finding 13 (Log-Likelihood Numbers Presented Without SE): C — bare integers reported in conclusion with no Monte Carlo standard errors
- Finding 14 (Stationarity Assessment Informal and Potentially Incorrect): C — stationarity asserted from visual inspection without any formal test
- Finding 15 (Missing References and Reproducibility Information): C — empty references section, no repository, no cached files, no tabulated MLE vectors

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "22.14.3 — Severe ESS Collapse / Gaussian Measurement Model, suggesting t-distributed measurement model")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "22.14.4 — Breto Model Non-Convergence")
- Human Issue #5: covered (matched by finding: "22.14.5 — Heston Local Search: Declining MIF2 Log-Likelihood Trace")
- Human Issue #6: covered (matched by finding: "Missing figure captions — none of the 23 figures have descriptive captions")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- 22.14.3 (Severe ESS Collapse / Gaussian Measurement Model): B — pervasive ESS collapse indicates Gaussian noise misspecification; recommends t-distributed model (matches Human Issue #1)
- 22.14.4 (Breto Model Non-Convergence): B — sigma_eta drifts to extreme values, chains not converged after 200 iterations (matches Human Issue #4)
- 22.14.5 (Heston Local Search Declining Trace): B — loglik declines monotonically during local search, opposite of expected pattern (matches Human Issue #5)
- 22.14.6 (No Profile Likelihoods or Confidence Intervals): A — no profile likelihoods computed for any parameter in either model
- 22.14.M2 (V_0 Non-Convergence in Heston): A — initial condition V_0 still spreading after 200 MIF2 iterations, not identified
- 22.14.1r (Cross-Model Likelihood Comparison): C — comparison of raw log-likelihoods across garchFit and pomp not explicitly justified
- 22.14.M3 (ARMA Model Selection): C — ARMA(4,4) fits better by ~14.6 AIC units but AR(4) selected "for simplicity" without acknowledgment
- 22.14.13 (Reproducibility): C — no sessionInfo() or R package version information provided
- Typographical errors: C — "Simple Sotchastic Volatility," "Comparsion," "time-seris" should be corrected
- Missing figure captions: D — none of the 23 figures have descriptive captions (matches Human Issue #6)
- Citation quality: C — Heston model cited via Wikipedia instead of original Heston 1993 source

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 8 | 6 | 7 | 2 |
| B (AI major, human also found) | 0 | 1 | 1 | 3 |
| C (AI minor, human missed) | 7 | 7 | 7 | 5 |
| D (AI minor, human also found) | 0 | 1 | 0 | 1 |
| E (Human found, AI missed) | 9 | 6 | 7 | 5 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 0 | 9 | 0/9 = 0% | 8 | 7 | 15/15 = 100% |
| Charlie | 1 | 1 | 6 | 3/9 = 33% | 6 | 7 | 13/15 = 87% |
| Doug | 1 | 0 | 7 | 2/9 = 22% | 7 | 7 | 14/15 = 93% |
| Evan | 3 | 1 | 5 | 4/9 = 44% | 2 | 5 | 7/11 = 64% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: The ARMA models should have been fitted to the return (difference of log price) rather than the raw data. It is not immediately clear from the text what is intended, but the code reveals they are fitted to the raw data. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #3: The AR-Garch model is undefined. Better to write out a model specification when doing applied statistics, but especially for a model that may be unfamiliar to the reader. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: Typo: The Heston model notation for the Brownian motions is a bit unclear. Maybe, $W=(W^s,W^\nu)$ should be a bivariate Brownian motion? (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: Typo: Fixing $\mu=1$ looks like a typo; fixing $\mu=0$ is a more natural simplification and matches what happened in the code (or, rather, the returns are de-meaned to make $\mu=0$ appropriate). (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 4 out of 9 human issues (44%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #1: One could use t-distributed returns within a stochastic volatility model, with or without leverage. (Covered only by Evan)
- Human Issue #6: In the Heston model, the authors also illustrate the model formulas and useful notations. However, for the first plot, there is no proper interpretation or caption to describe which row is the simulated volatility or the actual volatility. (Covered only by Evan)
- Human Issue #7: It would be helpful (and maybe interesting) to compare simulations from all the fitted models. (Covered only by Charlie)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 1 |
| Doug | 0 |
| Evan | 2 |
