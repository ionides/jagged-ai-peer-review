# Comparator Analysis — W21 Project 08

---

## Human Issues

1. The decreasing likelihood in the HMM search is likely a symptom of model misspecification: the model needs extra noise to explain the data, and this noise is provided by the perturbations in early iterations of the IF2 optimization. As the optimization algorithm decreases the perturbations, the perturbed likelihood goes down even as the proper likelihood (of the actual model, without perturbations) increases.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Gaussian HMM AR(1) likelihood goes up then down during MIF2, root cause is degenerate measurement via covariate trick")

**Findings classification:**
- Finding 1 (Log-Likelihood Not Comparable Across Models): A — log-likelihoods incomparable because Heston and AR(1) HMM use covariate filtering on a different probability space
- Finding 2 (t-HMM rprocess Uses euler() Instead of discrete_time()): A — structural mismatch makes t-HMM incomparable to Gaussian HMM
- Finding 3 (Gaussian HMM AR(1) Measurement Equation Is Trivial): B — authors note likelihood goes up then down in MIF2; Alex identifies root cause as degenerate covariate-trick measurement (matches Human Issue #1)
- Finding 4 (Heston Euler Discretization Incorrect for Log-Variance): A — code equations inconsistent with stated SDE; rho near 1.0 signals misspecification
- Finding 5 (No Formal Profile Likelihood CIs): A — only "poor man's" profile CIs used; no profiles for t-HMM or Heston
- Finding 6 (Pairs Plot Typo Silently Drops Parameter): C — `01` numeric literal used instead of `p1`; p1 omitted from diagnostic plot
- Finding 7 (Global Search Very Low Particle Count): C — Np=200 for Gaussian HMM global search vs. 1000-20000 elsewhere
- Finding 8 (AIC Parameter Count for ARMA+GARCH Wrong): C — parameter count listed as 6, should be 8
- Finding 9 (97.5th Percentile Aggregation Unjustified): C — no sensitivity analysis for choice of percentile or 12-hour window
- Finding 10 (HMM Transition Probabilities Confusingly Named): C — p0 is off-diagonal transition; prose interpretation potentially reversed
- Finding 11 (t-HMM dmeasure Unusual Coding Pattern): C — give_log passed as integer to dt(); correct but merits documentation
- Finding 12 (Heston Global Search Box Has Non-Existent Parameter): C — sigma_nu in search box not in heston_paramnames; silently ignored
- Finding 13 (Only 1-3 Simulations Shown): C — too few trajectories for predictive-envelope assessment
- Finding 14 (No Residual Diagnostics Beyond Visual): C — no PIT histograms, ACF of residuals, or systematic ESS discussion
- Finding 15 (Reference Numbering Error): C — entry [4] duplicated; subsequent numbers off by one

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 10 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 0 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by findings: "Gaussian HMM AR(1) declining likelihood acknowledged but not addressed structurally" and "last iteration estimator used in comparison table without caveat")

**Findings classification:**
- Finding 1 (poor man's profile is a likelihood slice, not profile likelihood): A — no corresponding human issue
- Finding 2 (Gaussian HMM global search uses Np=200, insufficient): A — no corresponding human issue
- Finding 3 (Gaussian HMM AR(1) declining likelihood acknowledged but not addressed structurally): B — matches Human Issue #1
- Finding 4 (AIC table mixes ARMA/GARCH and POMP likelihoods without noting non-comparability): A — no corresponding human issue
- Finding 5 (Heston global search box contains undefined parameter sigma_nu): A — no corresponding human issue
- Finding 6 (no non-mechanistic benchmark comparison): A — no corresponding human issue
- Finding 7 (Gaussian HMM AR(1) violates POMP conditional independence requirement): A — no corresponding human issue
- Finding 8 (data aggregation choice of 97.5th percentile not formally justified): C — no corresponding human issue
- Finding 9 (Student-t HMM uses euler(delta.t=1/12) while Gaussian HMM uses discrete_time): C — no corresponding human issue
- Finding 10 (last iteration estimator used in comparison table without caveat): D — matches Human Issue #1
- Finding 11 (Heston Euler discretization formula for log-volatility process contains error): C — no corresponding human issue
- Finding 12 (conditional log-likelihood diagnostic from last mif2 object, not MLE): C — no corresponding human issue
- Finding 13 (Heston global search box restricts rho to [0,1], excluding negative correlations): C — no corresponding human issue
- Finding 14 (typos "likelihoos" and "exhbited" in conclusion): C — no corresponding human issue
- Finding 15 (no sessionInfo or package versions reported): C — no corresponding human issue

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 0 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Gaussian HMM AR(1) Model Is Acknowledged to Be Misspecified But No Resolution Is Provided — decreasing log-likelihood during IF2 iterations is identified as a classical signature of model misspecification")

**Findings classification:**
- Major Issue 1 (Global Search Anti-Pattern): A — prior mif2 result passed as first argument to mif2 in global search, anchoring near local optimum
- Major Issue 2 (Pseudo-Profile Likelihoods): A — no constrained IF2 optimization run; scatter plots of global-search results used in place of true profile likelihoods; chi-squared CIs statistically invalid
- Major Issue 3 (Initial Particle Filter on Simulated Data): A — AR-HMM initial particle filter evaluated on simulated data (sim1.filt) rather than real data
- Major Issue 4 (Heston Box Contains Undeclared Parameter sigma_nu): A — sigma_nu present in global search box but absent from heston_paramnames, creating silent mismatch
- Major Issue 5 (No Non-Mechanistic Benchmark): A — no comparison of POMP models against a simple non-mechanistic benchmark on a common likelihood scale
- Major Issue 6 (Inadequate Computational Effort for Heston): A — only 2,000 particles used for 9-dimensional Heston model; SE of log-likelihood not reported
- Major Issue 7 (AR-HMM Misspecification Unresolved): B — log-likelihood increases then decreases during IF2 iterations, identified as classical signature of model misspecification; model still included in formal comparison (matches Human Issue #1)
- Major Issue 8 (Model Comparison Table Mixes Incompatible Log-Likelihoods): A — ARMA, GARCH, and POMP log-likelihoods placed in same table without acknowledging incompatible observation models
- Major Issue 9 (Pairs Plot Typo): A — column name "01" is a typo for "p1" in the Gaussian HMM pairs plot call
- Minor Issue (eta missing from partrans): C — eta not given logit transform in t-HMM partrans despite being in (0,1)
- Minor Issue (single simulation for MLE validation): C — only nsim=1 trajectory used for visual MLE validation in t-HMM and Heston
- Minor Issue (last iteration estimator lacks justification): C — "last iteration estimator" used as heuristic when likelihood trace is non-monotone without formal statistical justification
- Minor Issue (no model diagnostics beyond visual simulation): C — conditional log-likelihood plots and ESS traces computed but not interpreted to identify model failure periods
- Minor Issue (data aggregation choice not validated): C — 97.5th percentile aggregation to 12-hour windows not compared to alternatives
- Minor Issue (missing sessionInfo and package versions): C — no R or package version record; reproducibility undermined
- Minor Issue (Heston non-standard log-volatility parameterization): C — Euler discretization uses exp(-Z) in mean-reversion term rather than standard Heston SDE form; justification not provided

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 0 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed

**Findings classification:**
- 21.08.M1: A — "poor man's profile" CIs are statistically invalid; not a proper profile likelihood
- 21.08.M2: A — Heston boundary estimate for rho (0.9993) with no identifiability analysis
- 21.08.M3: A — undocumented log-variance reparameterization in Heston code vs. text equations
- 21.08.M4: A — t-HMM MLE in Section 6.2 text contradicts values shown in code
- 21.08.m1: C — global search for Gaussian HMM uses Np=200, too noisy for reliable ranking
- 21.08.m2: C — AR(1) HMM pairs plots show a0/b0 linear relationship indicating identifiability failure
- 21.08.m3: C — Gaussian/t observation model not justified for 97.5th-percentile order statistic data
- 21.08.m4: C — Heston conclusion overstates physical interpretation given identifiability concerns
- 21.08.m5: C — sigma_nu in Heston global search box is dead code (copy-paste artifact)
- 21.08.m6: C — AR(1) HMM filter diagnostics come from mif2 last iteration, not fixed-parameter pfilter

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 4 | 6 | 8 | 4 |
| B (AI major, human also found) | 1 | 1 | 1 | 0 |
| C (AI minor, human missed) | 10 | 7 | 7 | 6 |
| D (AI minor, human also found) | 0 | 1 | 0 | 0 |
| E (Human found, AI missed) | 0 | 0 | 0 | 1 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 0 | 0 | 1/1 = 100% | 4 | 10 | 14/15 = 93% |
| Charlie | 1 | 1 | 0 | 1/1 = 100% | 6 | 7 | 13/15 = 87% |
| Doug | 1 | 0 | 0 | 1/1 = 100% | 8 | 7 | 15/16 = 94% |
| Evan | 0 | 0 | 1 | 0/1 = 0% | 4 | 6 | 10/10 = 100% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

(none)

Total consensus misses: 0 out of 1 human issues (0%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
