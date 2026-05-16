# Ned-Clean Analysis — W24 Project 05

---

## Human Issues

1. Figures lack captions and numbers; the time plot should show dates not just week numbers; frequency analysis should give units in text and plot.
2. Spectral analysis to detect annual seasonality is unnecessary and unsurprising; the report could acknowledge this.
3. The ARMA grid search is too small (no more than 2 lags) — was this intentional?
4. The fraction of the project devoted to ARMA and linear time series analysis is too large.
5. Infectious disease dynamics are better modeled by ARMA on a log scale.
6. Log likelihoods for differenced models are not directly comparable to those for original data without accounting for the transformation.
7. In the initial pfilter, ESS is always between 1990 and 2000, which is surprising — perhaps the measurement model is extremely flat.
8. The measurement model is not described in the text.

---

## Alex

**Coverage record:**
- Human Issue #1 (figures, captions, dates, units): missed
- Human Issue #2 (spectral analysis unnecessary): missed
- Human Issue #3 (ARMA grid search too small): missed
- Human Issue #4 (too much of project on ARMA/linear analysis): missed
- Human Issue #5 (log-scale ARMA for infectious disease): missed
- Human Issue #6 (log likelihoods for differenced models not comparable): covered (matched by finding: "Log-likelihood comparison between SARIMA and POMP is invalid — SARIMA on differenced data with Gaussian likelihood vs POMP on original counts with NB likelihood")
- Human Issue #7 (ESS always 1990–2000, suspicious): missed
- Human Issue #8 (measurement model not described in text): missed

**Findings classification:**
- Issue 1 (Invalid log-likelihood comparison SARIMA vs POMP): B — comparison of non-comparable likelihoods (matches Human Issue #6)
- Issue 2 (H accumulator never reset between obs times in initial model): A — code bug in accumvars usage
- Issue 3 (SARIMA period=12 instead of period=52 in grid search): A — wrong seasonal period used for model selection
- Issue 4 (No profile likelihoods; poor man's profiles not a substitute): A — parameter identifiability unassessed
- Issue 5 (Sinusoidal forcing from ChatGPT without epidemiological justification): A — model choice unjustified
- Issue 6 (Epidemiological parameters not interpreted or validated): A — biologically implausible estimates not discussed
- Issue 7 (Arbitrary dataset truncation to 2011–2015): A — unjustified data restriction
- Issue 8 (Initial state parameters fixed after local search without diagnostic support): C — premature fixing of parameters
- Issue 9 (ARMA grid search uses flu_ts — dataset consistency note): C — dataset scoping observation
- Issue 10 (Measurement model mismatch: dmeas uses H=dN_IR, not dN_EI): C — epidemiological basis of measurement equation questioned
- Issue 11 (rw.sd values uniform and small; scale-inappropriate perturbations): C — perturbation scale concern
- Issue 12 (Poor man's profile filtering inconsistency): C — internal inconsistency in profiling
- Issue 13 (SARIMA notation B_{12} inconsistent with period=52 code): C — notation/code mismatch
- Issue 14 (eta parameter in initial params but absent from model): C — unused phantom parameter
- Issue 15 (Reproducibility: RNG seed not controlled per run-level): C — reproducibility concern

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1 (figures, captions, dates, units): missed
- Human Issue #2 (spectral analysis unnecessary): missed
- Human Issue #3 (ARMA grid search too small): missed
- Human Issue #4 (too much of project on ARMA/linear analysis): missed
- Human Issue #5 (log-scale ARMA for infectious disease): missed
- Human Issue #6 (log likelihoods for differenced models not comparable): covered (matched by finding: "SARIMA and POMP log-likelihoods are not directly comparable, invalidating the main conclusion")
- Human Issue #7 (ESS always 1990–2000, suspicious): missed
- Human Issue #8 (measurement model not described in text): missed

**Findings classification:**
- Major Issue 1 (SARIMA and POMP log-likelihoods not directly comparable): B — invalid main conclusion (matches Human Issue #6)
- Major Issue 2 (SARIMA grid search uses period=12, not period=52): A — wrong seasonal period in model selection
- Major Issue 3 (Reporting rate rho ~0.13% biologically implausible): A — implausible parameter estimate not discussed
- Major Issue 4 (No profile likelihoods; parameter identifiability unassessed): A — identifiability unaddressed
- Major Issue 5 (No non-mechanistic benchmark in POMP framework): A — no valid benchmark comparison
- Major Issue 6 (Log-likelihood direction misstated in local search narrative): A — direction of improvement confused
- Minor: SARIMA text inconsistency B_{12} notation: C — notation inconsistency
- Minor: rw.sd for phase extremely small: C — perturbation scale concern
- Minor: k and initial conditions fixed during global search: C — parameters prematurely fixed
- Minor: Phantom eta parameter: C — unused parameter in initial model
- Minor: Inconsistency between claimed (750) and actual search count (1354 rows): C — computational reporting inconsistency
- Minor: No quantitative goodness-of-fit summary for POMP simulations: C — validation limited to visual inspection
- Minor: Rationale for restricting data to 2011–2015 requires stronger justification: C — data restriction rationale weak
- Minor: Decomposition section misstates seasonal period (says "daily or weekly"): C — conceptual error in EDA interpretation
- Minor: No discussion of model limitations beyond parameter estimation: C — incomplete discussion of model constraints
- Minor: Total computational cost not reported: C — reproducibility/effort assessment missing

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 10 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1 (figures, captions, dates, units): missed
- Human Issue #2 (spectral analysis unnecessary): missed
- Human Issue #3 (ARMA grid search too small): missed
- Human Issue #4 (too much of project on ARMA/linear analysis): missed
- Human Issue #5 (log-scale ARMA for infectious disease): missed
- Human Issue #6 (log likelihoods for differenced models not comparable): covered (matched by finding: "ID 24.05.7 — Conclusion treats non-comparable likelihoods as directly comparable")
- Human Issue #7 (ESS always 1990–2000, suspicious): missed
- Human Issue #8 (measurement model not described in text): missed

**Findings classification:**
- ID 24.05.1 (Wrong seasonal period in SARIMA, period=12 vs 52): A — misspecified SARIMA model selection
- ID 24.05.3 (Parameters mu_IR and mu_RS not identified): A — flat likelihood surface, unidentifiable parameters
- ID 24.05.4 (Profile likelihoods absent; no parameter confidence intervals): A — identifiability and uncertainty unaddressed
- ID 24.05.2 (Global search likelihoods likely from mif2, not replicated pfilter): A — unreliable likelihood estimates used for selection
- ID 24.05.7 (Conclusion treats non-comparable likelihoods as directly comparable): B — invalid log-likelihood comparison (matches Human Issue #6)
- ID 24.05.6 (Short estimated immune period ~13 weeks, implausible): C — biologically implausible estimate not discussed
- ID 24.05.8 (Unused parameter eta in initial code): C — phantom parameter
- ID 24.05.12 (loglik.se not reported): C — Monte Carlo standard error omitted
- ID 24.05.13 (Fixed parameter values not documented in text): C — parameter fixing undocumented
- ID 24.05.NEW1 (Result RDS/CSV files not archived in submission): C — reproducibility concern
- ID 24.05.NEW2 (No per-chain convergence traces for global searches): C — convergence unverifiable

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1 (figures, captions, dates, units): missed
- Human Issue #2 (spectral analysis unnecessary): missed
- Human Issue #3 (ARMA grid search too small): missed
- Human Issue #4 (too much of project on ARMA/linear analysis): missed
- Human Issue #5 (log-scale ARMA for infectious disease): missed
- Human Issue #6 (log likelihoods for differenced models not comparable): covered (matched by finding: "ID 24.05.7 — Conclusion treats non-comparable likelihoods as directly comparable")
- Human Issue #7 (ESS always 1990–2000, suspicious): missed
- Human Issue #8 (measurement model not described in text): missed

**Findings classification:**
- ID 24.05.1 (Possible wrong seasonal period in SARIMA, period=12 vs 52): A — misspecified SARIMA model selection
- ID 24.05.3 (Parameters mu_IR and mu_RS not identified across global searches): A — unidentifiable parameters, flat likelihood
- ID 24.05.4 (Profile likelihoods absent; no parameter confidence intervals): A — identifiability and uncertainty unaddressed
- ID 24.05.2 (Global search likelihoods likely from mif2, not replicated pfilter): A — unreliable likelihood estimates used for selection
- ID 24.05.7 (Conclusion treats non-comparable likelihoods as directly comparable): B — invalid log-likelihood comparison (matches Human Issue #6)
- ID 24.05.6 (Short estimated immune period ~13 weeks, implausible): C — biologically implausible parameter estimate
- ID 24.05.8 (Unused parameter eta in initial code): C — phantom parameter
- ID 24.05.12 (loglik.se not reported): C — Monte Carlo standard error omitted
- ID 24.05.13 (Fixed parameter values not documented): C — parameter fixing undocumented
- ID 24.05.NEW1 (Result RDS/CSV files not archived): C — reproducibility concern
- ID 24.05.NEW2 (No per-chain convergence traces for global searches): C — convergence unverifiable

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 5 | 4 | 4 |
| B (AI major, human also found) | 1 | 1 | 1 | 1 |
| C (AI minor, human missed) | 8 | 10 | 6 | 6 |
| D (AI minor, human also found) | 0 | 0 | 0 | 0 |
| E (Human found, AI missed) | 7 | 7 | 7 | 7 |

---

## Per-Reviewer Metrics

Human Recall = (B + D) / (B + D + E)
AI-Unique Rate = (A + C) / (A + B + C + D)

| Reviewer | B | D | E | Human Recall | A | C | AI-Unique Rate |
|----------|--:|--:|--:|-------------:|--:|--:|---------------:|
| Alex | 1 | 0 | 7 | 1/8 = 12.5% | 6 | 8 | 14/15 = 93.3% |
| Charlie | 1 | 0 | 7 | 1/8 = 12.5% | 5 | 10 | 15/16 = 93.8% |
| Doug | 1 | 0 | 7 | 1/8 = 12.5% | 4 | 6 | 10/11 = 90.9% |
| Evan | 1 | 0 | 7 | 1/8 = 12.5% | 4 | 6 | 10/11 = 90.9% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover (all four missed):

1. Figures lack captions and numbers; time plot should show dates; frequency analysis should give units.
2. Spectral analysis to detect annual seasonality is unnecessary and unsurprising.
3. The ARMA grid search is too small (no more than 2 lags).
4. The fraction of the project devoted to ARMA and linear time series analysis is too large.
5. Infectious disease dynamics are better modeled by ARMA on a log scale.
7. In the initial pfilter, ESS is always between 1990 and 2000 — perhaps the measurement model is extremely flat.
8. The measurement model is not described in the text.

Count: 7 out of 8 human issues were missed by all four reviewers.

### Unique finds per reviewer

Human issues covered by only one reviewer (and missed by all others):

- Human Issue #6 (log likelihoods for differenced models not comparable) was covered by ALL four reviewers — it is not a unique find for any single reviewer.

No human issue was covered by exactly one reviewer while all others missed it.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

1. Wrong seasonal period in SARIMA grid search (period=12 instead of period=52) — raised as Major by Alex, Charlie, Doug, and Evan.
2. No profile likelihoods computed; parameter identifiability unassessed — raised as Major by Alex, Charlie, Doug, and Evan.

Count: 2 universal AI-only Major flags.
