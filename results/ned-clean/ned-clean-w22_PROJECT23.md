# Ned-Clean Analysis — W22 Project 23

---

## Human Issues

1. It can be important to estimate the initial value I_0 since it can have considerable effect on the dynamics.
2. Likelihood should not be reported to 4 decimal places. 1 or 2 is sufficient.
3. The measurement model for the SEIQR model is curious. Cases are an instantaneous measurement of Q, so individuals in Q can be counted in many measurement intervals (or none at all, if they move quickly out of Q). Generally, one needs an accumulator variable to make a reasonable measurement model.
4. Conclusion: "The log likelihood value of the SEIQR model is the lowest" is a typo, and should read "highest".
5. It would be useful to have ARMA or iid benchmarks. The SIR and SEIR log likelihoods are very low, perhaps suggesting a problem with the model.
6. One problem may be in the measurement models, which have only binomial variability. There is also no process over-dispersion. In the absence of a benchmark likelihood, it is hard to say whether these are fatal flaws.
7. SEIQR has been used in a previous STATS/DATASCI 531 project, but here the development seems to be independently derived from a reference.
8. The initializer does not quite satisfy the constraint of summing to N.
9. In the implementation of the measurement model, the authors manually override the loglikelihood as -1000 whenever the loglikelihood is numerically evaluated as infinite. This requires care since it could hide other problems.
10. The local search suggests an initial susceptible rate eta from roughly 0.94 to 0.96, but in the global search, the authors used a range of 0.4 to 0.6 for the parameter eta.
11. Where possible, numbers should not be hard-coded in the Rmd document. Rather, they should be referenced using inline R code.

---

## Alex

**Coverage record:**
- Human Issue #1 (estimate I_0): missed
- Human Issue #2 (likelihood decimal places): missed
- Human Issue #3 (SEIQR needs accumulator variable): covered (matched by finding: "SEIQR measurement model observes stock Q instead of new cases")
- Human Issue #4 ("lowest" typo): missed
- Human Issue #5 (ARMA/iid benchmarks): covered (matched by finding: "No comparison against a non-mechanistic benchmark")
- Human Issue #6 (only binomial variability, no overdispersion): missed
- Human Issue #7 (SEIQR used in prior project): missed
- Human Issue #8 (initializer sum to N): missed
- Human Issue #9 (manual override loglik -1000): missed
- Human Issue #10 (global search eta range mismatch): covered (matched by finding: "Global SIR finds worse MLE than local search")
- Human Issue #11 (hard-coded numbers): missed

**Findings classification:**
- Issue 1 (Incomparable likelihoods — different measurement distributions): A — incomparable log-likelihood scales across models (Critical)
- Issue 2 (Missing /N in SEIQR force of infection): A — SEIQR force of infection missing N normalization (Critical)
- Issue 3 (SEIQR observes stock Q, no accumulator): B — stock vs flow mismatch in SEIQR measurement model (matches Human Issue #3) (Critical)
- Issue 4 (SEIR delta.t=7 with daily data): A — weekly Euler step mismatched with daily observations (Major)
- Issue 5 (SEIR pairs plot uses SIR data): A — copy-paste error in SEIR likelihood surface plot (Major)
- Issue 6 (Inconsistent partrans between SEIR pomp object and mif2): A — parameter transformation inconsistency in SEIR (Major)
- Issue 7 (SEIQR partrans uses log instead of logit): A — wrong transformation for bounded parameters rho and eta (Major)
- Issue 8 (Global searches use sequential %do%): C — computationally wasteful sequential global search (Minor)
- Issue 9 (No profile likelihoods): A — no parameter uncertainty assessment (Major)
- Issue 10 (Population figure incorrect): A — population description inconsistency 18M vs 1.9M (Major)
- Issue 11 (Global SIR worse MLE than local): D — global search underperforms local search due to excluded eta region (matches Human Issue #10) (Minor)
- Issue 12 (No filter diagnostics): C — no ESS or residual analysis (Minor)
- Issue 13 (Text mu_IR=0.1 vs code mu_IR=0.27): C — stated vs implemented initial value discrepancy (Minor)
- Issue 14 (SEIR fewer IF2 iterations than SIR): C — asymmetric computational effort across models (Minor)
- Issue 15 (No non-mechanistic benchmark): D — no ARMA or baseline comparison (matches Human Issue #5) (Minor)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1 (estimate I_0): covered (matched by finding: "Initial conditions for E, I, Q are fixed constants, not estimated parameters")
- Human Issue #2 (likelihood decimal places): missed
- Human Issue #3 (SEIQR needs accumulator variable): covered (matched by finding: "SEIQR measurement model observes the quarantine stock, not daily new cases")
- Human Issue #4 ("lowest" typo): missed
- Human Issue #5 (ARMA/iid benchmarks): covered (matched by finding: "No non-mechanistic benchmark comparison")
- Human Issue #6 (only binomial variability, no overdispersion): missed
- Human Issue #7 (SEIQR used in prior project): missed
- Human Issue #8 (initializer sum to N): missed
- Human Issue #9 (manual override loglik -1000): missed
- Human Issue #10 (global search eta range mismatch): missed
- Human Issue #11 (hard-coded numbers): missed

**Findings classification:**
- Major #1 (Incomparable likelihoods across models): A — different distribution families make likelihoods incomparable (Major)
- Major #2 (SEIQR observes quarantine stock Q): B — stock vs flow mismatch in SEIQR measurement (matches Human Issue #3) (Major)
- Major #3 (SEIQR missing /N in force of infection): A — SEIQR force of infection missing N normalization (Major)
- Major #4 (SEIR delta.t=7 with daily data): A — weekly Euler step mismatched with daily data (Major)
- Major #5 (SEIQR non-convergence but conclusion proceeds): A — non-converged IF2 used to draw substantive conclusions (Major)
- Major #6 (SEIQR Normal measurement for count data): A — Gaussian measurement inappropriate for count data (Major)
- Major #7 (No profile likelihoods): A — no parameter identifiability assessment (Major)
- Major #8 (Global uses %do% not %dopar%): A — computationally inefficient sequential global search (Major)
- Minor #9 (SEIR pairs plot uses SIR data): C — copy-paste error in SEIR likelihood surface plot (Minor)
- Minor #10 (No non-mechanistic benchmark): D — no ARMA or baseline comparison (matches Human Issue #5) (Minor)
- Minor #11 (Initial conditions fixed, not estimated): D — fixed initial conditions for E, I, Q not optimized (matches Human Issue #1) (Minor)
- Minor #12 (SIR accumulator tallies recoveries not infections): C — accumulator variable incremented on wrong transition (Minor)
- Minor #13 (Population size description inconsistent): C — 18M stated vs 1.9M used in code (Minor)
- Minor #14 (No model diagnostics): C — no ESS or conditional log-likelihood plots (Minor)
- Minor #15 (SEIQR partrans inconsistency in mif2): C — conflicting parameter transformation override in local search (Minor)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1 (estimate I_0): covered (matched by finding: "Fixed initial conditions are not estimated or assessed for sensitivity")
- Human Issue #2 (likelihood decimal places): missed
- Human Issue #3 (SEIQR needs accumulator variable): covered (matched by finding: "SEIQR measurement model links to Q (stock) without an accumulator")
- Human Issue #4 ("lowest" typo): covered (matched by finding: "Conclusion incorrectly describes log-likelihood direction")
- Human Issue #5 (ARMA/iid benchmarks): covered (matched by finding: "No non-mechanistic benchmark comparison")
- Human Issue #6 (only binomial variability, no overdispersion): missed
- Human Issue #7 (SEIQR used in prior project): missed
- Human Issue #8 (initializer sum to N): missed
- Human Issue #9 (manual override loglik -1000): missed
- Human Issue #10 (global search eta range mismatch): covered (matched by finding: "Global search box excludes the MLE region — SIR eta 0.4-0.6 vs local 0.95")
- Human Issue #11 (hard-coded numbers): missed

**Findings classification:**
- Major #1 (SEIQR rprocess omits N-normalization): A — SEIQR force of infection missing N (Major)
- Major #2 (Log-likelihoods on incommensurable scales): A — incomparable likelihood scales across models (Major)
- Major #3 (SEIQR observes Q stock without accumulator): B — stock vs flow mismatch in SEIQR measurement (matches Human Issue #3) (Major)
- Major #4 (Non-convergence acknowledged but results interpreted): A — non-converged IF2 used to support conclusions (Major)
- Major #5 (SEIR delta.t=7 with daily data): A — weekly Euler step mismatched with daily data (Major)
- Major #6 (SEIR pairs plot uses SIR data): A — copy-paste error in SEIR likelihood surface plot (Major)
- Major #7 (No non-mechanistic benchmark): B — no ARMA or baseline comparison (matches Human Issue #5) (Major)
- Major #8 (Global search box excludes MLE region): B — eta range 0.4-0.6 excludes local search optimum 0.94-0.96 (matches Human Issue #10) (Major)
- Major #9 (No profile likelihoods): A — no parameter identifiability assessment (Major)
- Minor: Population size inconsistency: C — 18M stated vs 1.9M used in code (Minor)
- Minor: SEIQR %do% instead of %dopar%: C — sequential global search wastes computation (Minor)
- Minor: SEIR partrans redundant/inconsistent in mif2: C — mu_IR omitted from log-transform in mif2 override (Minor)
- Minor: Fixed initial conditions not estimated: D — E and I initial values fixed, not optimized (matches Human Issue #1) (Minor)
- Minor: No model diagnostics: C — no ESS or conditional log-likelihood diagnostics (Minor)
- Minor: Conclusion loglik direction error ("lowest"): D — "lowest" should be "highest" log-likelihood (matches Human Issue #4) (Minor)
- Minor: Computational effort low and not justified: C — Nmif and Np choices underjustified (Minor)
- Minor: No assessment for full pandemic period: C — restriction to 58-day window not evaluated (Minor)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1 (estimate I_0): missed
- Human Issue #2 (likelihood decimal places): missed
- Human Issue #3 (SEIQR needs accumulator variable): covered (matched by finding: "22.23.1 — Incomparable measurement models; SEIQR uses Q stock vs H accumulator")
- Human Issue #4 ("lowest" typo): covered (matched by finding: "22.23.13 — 'Lowest log-likelihood = best model' is non-standard language")
- Human Issue #5 (ARMA/iid benchmarks): covered (matched by finding: "22.23.7 — No non-mechanistic benchmark")
- Human Issue #6 (only binomial variability, no overdispersion): missed
- Human Issue #7 (SEIQR used in prior project): missed
- Human Issue #8 (initializer sum to N): missed
- Human Issue #9 (manual override loglik -1000): missed
- Human Issue #10 (global search eta range mismatch): covered (matched by finding: "22.23.4 — SIR global search box excludes the local MLE region")
- Human Issue #11 (hard-coded numbers): missed

**Findings classification:**
- 22.23.1 (Incomparable measurement models invalidate model comparison): B — incomparable likelihood scales; SEIQR uses Q stock vs accumulator H (matches Human Issue #3) (Major)
- 22.23.2 (SEIQR missing /N in force of infection): A — SEIQR force of infection missing N normalization (Major)
- 22.23.3 (SEIR weekly Euler step on daily data): A — weekly Euler step mismatched with daily data (Major)
- 22.23.4 (SIR global search box excludes local MLE): B — eta range 0.4-0.6 excludes local optimum near 0.95 (matches Human Issue #10) (Major)
- 22.23.7 (No non-mechanistic benchmark): B — no ARMA or baseline comparison (matches Human Issue #5) (Major)
- 22.23.8 (No profile likelihoods): A — no parameter uncertainty assessment (Major)
- 22.23.5 (SEIQR declared best despite non-convergence): A — non-converged IF2 used to support conclusions (Major)
- 22.23.6 (SEIR pairs plot uses SIR data): C — copy-paste error in SEIR likelihood surface plot (Minor)
- 22.23.9 (mu_IR biologically implausible): C — mean infectious period of 167 days implausible for Omicron (Minor)
- 22.23.13 ("Lowest" non-standard language): D — "lowest" should be "highest" log-likelihood (matches Human Issue #4) (Minor)
- No model diagnostics (unlabeled): C — no conditional log-likelihoods or ESS reported (Minor)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 8 | 7 | 6 | 4 |
| B (AI major, human also found) | 1 | 1 | 3 | 3 |
| C (AI minor, human missed) | 4 | 5 | 6 | 3 |
| D (AI minor, human also found) | 2 | 2 | 2 | 1 |
| E (Human found, AI missed) | 8 | 8 | 6 | 7 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

**Alex:**
- Human Recall = (B+D) / (B+D+E) = (1+2) / (1+2+8) = 3/11 = **27.3%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (8+4) / (8+1+4+2) = 12/15 = **80.0%**

**Charlie:**
- Human Recall = (B+D) / (B+D+E) = (1+2) / (1+2+8) = 3/11 = **27.3%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (7+5) / (7+1+5+2) = 12/15 = **80.0%**

**Doug:**
- Human Recall = (B+D) / (B+D+E) = (3+2) / (3+2+6) = 5/11 = **45.5%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (6+6) / (6+3+6+2) = 12/17 = **70.6%**

**Evan:**
- Human Recall = (B+D) / (B+D+E) = (3+1) / (3+1+7) = 4/11 = **36.4%**
- AI-Unique Rate = (A+C) / (A+B+C+D) = (4+3) / (4+3+3+1) = 7/11 = **63.6%**

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer (Alex, Charlie, Doug, Evan) failed to cover:

- Human Issue #2: Likelihood should not be reported to 4 decimal places.
- Human Issue #6: Measurement models have only binomial variability; no process over-dispersion.
- Human Issue #7: SEIQR has been used in a previous STATS/DATASCI 531 project.
- Human Issue #8: The initializer does not quite satisfy the constraint of summing to N.
- Human Issue #9: Authors manually override loglikelihood as -1000 when evaluated as infinite.
- Human Issue #11: Numbers should not be hard-coded; use inline R code.

**Total: 6 out of 11 human issues were missed by all reviewers (55%)**

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #4 ("lowest" typo): covered only by Doug and Evan — not uniquely covered by any single reviewer (both Doug and Evan covered it).
- Human Issue #1 (estimate I_0): covered by Charlie and Doug — not uniquely covered by any single reviewer.
- Human Issue #3 (accumulator variable): covered by Alex, Charlie, Doug, and Evan — covered by all.
- Human Issue #5 (ARMA benchmarks): covered by Alex, Charlie, Doug, and Evan — covered by all.
- Human Issue #10 (global search eta mismatch): covered by Alex, Doug, and Evan — not uniquely covered by any single reviewer.

No human issue was covered by exactly one reviewer and missed by all others.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised as Major by every reviewer that the human did not mention:

- **Missing /N normalization in SEIQR force of infection**: raised as Major by Alex (#2), Charlie (#3), Doug (#1), Evan (22.23.2). Human did not mention this.
- **SEIR delta.t=7 weekly step with daily data**: raised as Major by Alex (#4), Charlie (#4), Doug (#5), Evan (22.23.3). Human did not mention this.
- **No profile likelihoods or confidence intervals**: raised as Major by Alex (#9), Charlie (#7), Doug (#9), Evan (22.23.8). Human did not mention this.

Issues raised as Major by three or more reviewers that the human did not mention:
- **Incomparable likelihoods across models (different measurement distributions)**: Alex (#1 Critical), Charlie (#1 Major), Doug (#2 Major), Evan (22.23.1 Major, assigned B to Human #3). Note: the incomparable-likelihoods issue (as distinct from the stock-vs-flow issue) was not flagged by the human.
- **SEIQR non-convergence acknowledged but conclusion proceeds**: Charlie (#5 Major), Doug (#4 Major), Evan (22.23.5 Major). Not raised by human.
- **SEIR pairs plot uses SIR data**: Alex (#5 Major), Charlie (#9 Minor), Doug (#6 Major), Evan (22.23.6 Minor). Not raised by human.

**Universal AI-only flags count (raised Major by all four reviewers): 3**
