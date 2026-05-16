# Ned-Clean Analysis — W21 Project 08

## Human Issues

1. The decreasing likelihood in the HMM search is likely a symptom of model misspecification: the model needs extra noise provided by IF2 perturbations in early iterations; as perturbations decrease, the perturbed likelihood goes down even as the proper likelihood increases.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Gaussian HMM AR(1) rising-then-falling likelihood, root cause as degenerate measurement model")

**Findings classification:**
- Issue 1 — Log-likelihoods not comparable across models: A — models use different probability spaces, Heston/AR(1) use covariate trick
- Issue 2 — t-HMM rprocess uses euler() instead of discrete_time(): A — 12 sub-steps per observation introduced
- Issue 3 — Gaussian HMM AR(1) measurement trivial / degenerate likelihood: B — acknowledges rising-then-falling likelihood during MIF2, attributes to covariate trick / Dirac-delta measurement (matches Human Issue #1)
- Issue 4 — Heston Euler discretization incorrectly applies to log-variance: A — equation in report inconsistent with code
- Issue 5 — No formal profile likelihood CIs: A — "poor man's profile" not a valid profile
- Issue 6 — Pairs plot typo silently drops p1: C — code bug in pairs() call
- Issue 7 — Global search uses Np=200 particles (low): C — Monte Carlo variance too high for global search
- Issue 8 — AIC computation for ARMA+GARCH may be wrong (parameter count): C — underpenalized AIC
- Issue 9 — Data aggregation choice (97.5th percentile) not justified: C — no sensitivity analysis
- Issue 10 — HMM transition probabilities confusingly named: C — interpretation of p0/p1 may be reversed
- Issue 11 — Student-t HMM dmeasure bug for non-log case: C — unusual coding pattern for give_log
- Issue 12 — Heston global search box contains non-existent parameter sigma_nu: C — dead code leftover
- Issue 13 — Simulation comparison shown for only 1-3 simulations: C — insufficient for predictive envelope
- Issue 14 — No residual diagnostics beyond visual inspection: C — no PIT, ACF of residuals, or ESS plots
- Issue 15 — Reference numbering error: C — duplicate [4] entries

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 0 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Gaussian HMM AR(1) declining likelihood acknowledged but not addressed structurally")

**Findings classification:**
- Issue 1 — "Poor man's profile" is a likelihood slice, not a profile likelihood: A — no constrained re-optimization at each fixed parameter value
- Issue 2 — Gaussian HMM global search uses Np=200 particles (insufficient): A — Monte Carlo variance inflates reported MLE
- Issue 3 — Gaussian HMM AR(1) declining likelihood acknowledged but not addressed structurally: B — explicitly discusses rising-then-falling log-likelihood from IF2 as requiring structural model revision (matches Human Issue #1)
- Issue 4 — AIC comparison mixes ARMA/GARCH and POMP likelihoods without noting non-comparability: A — different normalization conventions across estimators
- Issue 5 — Heston global search box contains undefined parameter sigma_nu: A — leftover from prior model variant
- Issue 6 — No non-mechanistic benchmark comparison: A — common-likelihood-scale benchmark absent
- Issue 7 — Gaussian HMM AR(1) model violates POMP conditional independence requirement: A — observation density depends on past observation via covariate channel, not acknowledged
- Issue 8 — Data aggregation choice (97.5th percentile) not formally justified: C — no sensitivity check vs. max/median
- Issue 9 — Student-t HMM uses euler(delta.t=1/12) while Gaussian HMM uses discrete_time: C — 12 sub-steps per observation period, non-comparable likelihoods
- Issue 10 — "Last iteration" estimator for Gaussian HMM AR(1) is not a valid MLE: C — result included in comparison table without caveat
- Issue 11 — Heston Euler discretization formula contains an error: C — non-standard log-volatility mean-reversion term
- Issue 12 — Conditional log-likelihood diagnostic from last mif2 object, not MLE: C — perturbed parameters in diagnostics
- Issue 13 — Global search box for Heston has rho bounded between 0 and 1 only, excluding negative correlations: C — MLE at boundary, may be box constraint artifact
- Issue 14 — Typos in conclusion (likelihoos, exhbited): C — minor typographical errors
- Issue 15 — No sessionInfo() or package versions reported: C — reproducibility concern

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 0 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Gaussian HMM AR(1) Model Acknowledged to Be Misspecified But No Resolution Is Provided")

**Findings classification:**
- Issue 1 — Global Search Anti-Pattern: Prior mif2 Result Passed as First Argument: A — cooled schedule from if1[[1]] means global search is not truly global
- Issue 2 — Pseudo-Profile Likelihoods: No Constrained IF2 Optimization Was Run: A — scatter plot of global search results, not profile likelihood
- Issue 3 — Initial Particle Filter for AR-HMM Evaluated on Simulated Data, Not Real Data: A — L.pf1 is likelihood on simulated not observed data
- Issue 4 — Heston Global Search Box Contains Undeclared Parameter sigma_nu: A — parameter not in heston_paramnames
- Issue 5 — No Non-Mechanistic Benchmark Comparison: A — no common-scale ARMA or AR baseline for comparison
- Issue 6 — Inadequate Computational Effort for Heston Model (Low Particle Count): A — Np=2000 may be insufficient for 9-dimensional model; SE not reported
- Issue 7 — Gaussian HMM AR(1) Model Acknowledged to Be Misspecified But No Resolution Provided: B — explicitly addresses rising-then-falling log-likelihood and notes "last iteration estimator" is not a valid MLE (matches Human Issue #1)
- Issue 8 — Model Comparison Table Mixes Incompatible Log-Likelihoods: A — different observation models, data transformations, and likelihood definitions
- Issue 9 — Pairs Plot Error in Gaussian HMM Code (01 instead of p1): A — listed under Major Issues
- Minor: Parameter eta missing from partrans for t-HMM: C — eta not given logit transform
- Minor: Only a single simulation for MLE validation in t-HMM and Heston: C — one trajectory insufficient
- Minor: "Last iteration estimator" lacks formal statistical justification: C — heuristic not a standard estimator (distinct from Issue 7 which is the primary match)
- Minor: No model diagnostics beyond visual simulation: C — conditional log-likelihoods not interpreted
- Minor: Data aggregation choice not validated: C — 97.5th percentile not compared to alternatives
- Minor: Missing sessionInfo() and package versions: C — reproducibility concern
- Minor: Heston Euler discretization non-standard log-volatility parameterization: C — exp(-Z) in mean-reversion term not derived from standard Ito

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
- Human Issue #1: covered (matched by finding: "AR(1) HMM convergence: identifiability of (a_k, b_k) not diagnosed; last iteration estimator not a valid MLE")

**Findings classification:**
- M1 — "Poor man's profile" CIs are statistically invalid: A — selecting maximum over binned search results is not a profile
- M2 — Heston model: implausible boundary estimate for rho with no identifiability analysis: A — rho = 0.9993 at boundary, traces do not stabilize
- M3 — Heston model: undocumented log-variance reparameterization: A — equations describe V_n but code implements Z = log(V_n)
- M4 — t-HMM: factual inconsistency between text and code for MLE values: A — text reports p0=0.0920, p1=0.241; code shows p0=0.007, p1=0.994
- m1 — Global search for Gaussian HMM uses Np=200 for evaluation: C — noisy likelihood estimates may misrank parameter sets
- m2 — AR(1) HMM convergence: identifiability of (a_k, b_k) not diagnosed; last iteration estimator not valid: D — discusses rising-then-falling likelihood as "not a valid MLE" and notes the mif2 perturbation mechanism indirectly (matches Human Issue #1)
- m3 — Measurement model for aggregated percentile data not discussed: C — distributional properties of 97.5th percentile order statistic not Gaussian in general
- m4 — Heston conclusion overstates the evidence: C — higher likelihood does not confirm physical interpretation
- m5 — sigma_nu in Heston global search box is dead code: C — silently ignored or causes error
- m6 — Filter diagnostic for AR(1) HMM is from mif2 last iteration, not final MLE: C — perturbed run does not represent final model

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 0 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 4 | 6 | 8 | 4 |
| B (AI major, human also found) | 1 | 1 | 1 | 0 |
| C (AI minor, human missed) | 9 | 8 | 7 | 5 |
| D (AI minor, human also found) | 0 | 0 | 0 | 1 |
| E (Human found, AI missed) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Recall = (B + D) / (B + D + E)
AI-Unique Rate = (A + C) / (A + B + C + D)

| Reviewer | B | D | E | B+D | B+D+E | Human Recall | A | C | A+C | A+B+C+D | AI-Unique Rate |
|----------|--:|--:|--:|----:|------:|-------------:|--:|--:|----:|--------:|---------------:|
| Alex | 1 | 0 | 0 | 1 | 1 | 1.00 (1/1) | 4 | 9 | 13 | 14 | 0.929 (13/14) |
| Charlie | 1 | 0 | 0 | 1 | 1 | 1.00 (1/1) | 6 | 8 | 14 | 15 | 0.933 (14/15) |
| Doug | 1 | 0 | 0 | 1 | 1 | 1.00 (1/1) | 8 | 7 | 15 | 16 | 0.938 (15/16) |
| Evan | 0 | 1 | 0 | 1 | 1 | 1.00 (1/1) | 4 | 5 | 9 | 10 | 0.900 (9/10) |

---

## Cross-Reviewer Aggregation

**Consensus misses:** Human issues that every reviewer failed to cover.

All four reviewers covered Human Issue #1. There are no consensus misses.

Count: 0 out of 1.

---

**Unique finds per reviewer:** Human issues that only one reviewer covered and all others missed.

With only 1 human issue and all 4 reviewers covering it, there are no issues that only one reviewer found exclusively. Every reviewer independently covered the single human issue.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

---

**Universal AI-only flags:** Issues raised by every reviewer that the human did not mention.

The following concern areas were raised as issues by all four reviewers (the human did not raise them):

1. Profile likelihood invalidity — all four reviewers (Alex Issue 5, Charlie Issue 1, Doug Issue 2, Evan M1) flag that the "poor man's profile CIs" are not valid profile likelihoods.
2. Insufficient particle count for global search (Np=200 for Gaussian HMM) — Alex Issue 7, Charlie Issue 2, Doug Issue 6 (for Heston), Evan m1 all raise low particle count concerns.
3. Heston global search box contains undeclared parameter sigma_nu — Alex Issue 12, Charlie Issue 5, Doug Issue 4, Evan m5 all flag this.
4. Data aggregation choice (97.5th percentile) not justified — Alex Issue 9, Charlie Issue 8, Doug minor, Evan m3 (adjacent concern about measurement model for aggregated data).
5. Model comparison table mixes incompatible log-likelihoods — Alex Issue 1, Charlie Issue 4, Doug Issue 8, Evan (implicitly via M2/M3).

Note: Items 4 and 5 are present in 3–4 reviewers but may not meet strict "all four" universality. The strictly universal AI-only flags (all four reviewers, human missed) are:

- Profile likelihood invalidity: all four (Alex, Charlie, Doug, Evan)
- sigma_nu undeclared parameter in Heston box: all four (Alex, Charlie, Doug, Evan)

Universal AI-only count: 2 issues raised by every reviewer that the human did not mention.
