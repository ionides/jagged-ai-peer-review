# Comparator Analysis — W22 Project 23

---

## Human Issues

1. It can be important to estimate the initial value $I_0$ since it can have considerable effect on the dynamics.

2. Likelihood should not be reported to 4 decimal places. 1 or 2 is sufficient.

3. The measurement model for the SEIQR model is curious. Cases are an instantaneous measurement of Q, so individuals in Q can be counted in many measurement intervals (or none at all, if they move quickly out of Q). Generally, one needs an accumulator variable to make a reasonable measurement model.

4. Conclusion: "The log likelihood value of the SEIQR model is the lowest" is a typo, and should read "highest".

5. It would be useful to have ARMA or iid benchmarks. The SIR and SEIR log likelihoods are very low, perhaps suggesting a problem with the model.

6. One problem may be in the measurement models, which have only binomial variability. There is also no process over-dispersion. In the absence of a benchmark likelihood, it is hard to say whether these are fatal flaws.

7. SEIQR has been used in a previous STATS/DATASCI 531 project, but here the development seems to be independently derived from a separate source.

8. The initializer does not quite satisfy the constraint of summing to $N$.

9. In the implementation of the measurement model, the authors manually override the loglikelihood as -1000 whenever the loglikelihood is numerically evaluated as infinite. This requires care since it could hide other problems.

10. The local search suggests an initial susceptible rate $\eta$ from roughly 0.94 to 0.96, and the authors state that the best initial guess of parameters is with $\eta = 0.95$. However, in the global search, the authors used a range of 0.4 to 0.6 for the parameter $\eta$.

11. Where possible, numbers should not be hard-coded in the Rmd document. Rather, they should be referenced using inline R code.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "SEIQR measurement model observes Q stock instead of flow accumulator — no accumulator variable defined")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "No comparison against a non-mechanistic benchmark such as ARIMA")
- Human Issue #6: contradiction (AI says SEIQR uses Normal measurement distribution, not Binomial; human says all models have "only binomial variability")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "SIR global search finds worse MLE than local search because global search eta range 0.4–0.6 excludes local optimum near 0.95")
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (non-comparable likelihoods — SEIQR Normal vs SIR/SEIR Binomial): F — AI says SEIQR uses Normal measurement model making likelihoods incomparable; human says all models have "only binomial variability" (contradicts Human Issue #6)
- Finding 2 (SEIQR force-of-infection missing /N): A — critical error in SEIQR Beta*I*dt vs. Beta*I/N*dt; human did not raise
- Finding 3 (SEIQR observes stock Q rather than flow accumulator): B — SEIQR measurement conditions on level of Q, no H accumulator defined (matches Human Issue #3)
- Finding 4 (SEIR delta.t=7 mismatched with daily data): A — Euler step of 7 days vs. daily observations inflates modeled counts; human did not raise
- Finding 5 (SEIR pairs plot uses SIR data): A — pairs plot for SEIR local search generated with sir_lik_local instead of seir_lik_local; human did not raise
- Finding 6 (inconsistent partrans between SEIR pomp object and mif2 call): A — mu_IR omitted from log-transform in mif2 call but included in pomp object; human did not raise
- Finding 7 (SEIQR rho and eta log-transformed instead of logit): A — proportions in [0,1] receive log not logit, allowing values >1; human did not raise
- Finding 8 (global searches use sequential %do% instead of parallel %dopar%): C — computationally wasteful but does not affect correctness; human did not raise
- Finding 9 (no profile likelihoods or confidence intervals): A — no uncertainty quantification for any parameter estimate; human did not raise
- Finding 10 (population figure inconsistent — text says 18M, code uses 1.9M, actual is 8.3M): A — directly affects force-of-infection and susceptible fraction interpretation; human did not raise
- Finding 11 (SIR global search worse than local search due to misspecified eta range): D — global eta range 0.4–0.6 excludes local optimum near 0.95 (matches Human Issue #10)
- Finding 12 (no model diagnostic checks — no ESS, no residual analysis): C — absence of filter diagnostics leaves reliability of particle filter unassessed; human did not raise
- Finding 13 (text states mu_IR=0.1 but code uses 0.27): C — discrepancy between stated and implemented initial value; human did not raise
- Finding 14 (SEIR local search uses Nmif=20 vs SIR Nmif=50): C — fewer iterations for more complex model reduces comparability; human did not raise
- Finding 15 (no non-mechanistic benchmark comparison): D — no ARIMA or similar baseline to assess whether mechanistic models add value (matches Human Issue #5)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 1 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding 11: "initial conditions for E, I, Q are fixed constants, not estimated parameters")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding 2: "SEIQR measurement model observes quarantine stock Q, not daily new cases — no accumulator variable")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding 10: "no non-mechanistic benchmark comparison")
- Human Issue #6: contradiction (AI says SEIQR uses a Normal/Gaussian measurement model; human says measurement models have only binomial variability)
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (Incomparable likelihoods — Binomial vs Normal across models): A — no human issue raises cross-model likelihood incomparability due to different observation model families
- Finding 2 (SEIQR measurement model observes stock Q, not daily new cases): B — matches Human Issue #3
- Finding 3 (SEIQR force-of-infection missing /N population normalization): A — no human issue raises this
- Finding 4 (SEIR uses delta.t=7 weekly Euler steps with daily data): A — no human issue raises this
- Finding 5 (SEIQR iterated filtering shows no convergence but conclusion proceeds): A — no human issue raises this
- Finding 6 (SEIQR uses Normal measurement model for count data): F — contradicts Human Issue #6 (human states all models have "only binomial variability"; AI says SEIQR uses Normal/Gaussian)
- Finding 7 (No profile likelihoods; parameter identifiability unassessed): A — no human issue raises this
- Finding 8 (Global search uses %do% instead of %dopar%): A — no human issue raises this
- Finding 9 (SEIR likelihood surface plot displays SIR data — copy-paste error): C — no human issue raises this
- Finding 10 (No non-mechanistic benchmark comparison): D — matches Human Issue #5
- Finding 11 (Initial conditions for E, I, Q fixed, not estimated): D — matches Human Issue #1
- Finding 12 (SIR accumulator variable H tallies recoveries, not new infections): C — no human issue raises this
- Finding 13 (Population size description inconsistent — 18 million vs 1.9 million): C — no human issue raises this
- Finding 14 (No model diagnostics provided): C — no human issue raises this
- Finding 15 (SEIQR local search specifies conflicting partrans override inside mif2): C — no human issue raises this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 1 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Fixed initial conditions are not estimated or assessed for sensitivity")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "SEIQR measurement model links to Q (stock) without an accumulator, confounding the observation")
- Human Issue #4: covered (matched by finding: "Conclusion incorrectly describes log-likelihood direction")
- Human Issue #5: covered (matched by finding: "No non-mechanistic benchmark comparison")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "Global search box excludes the MLE region (SIR model)")
- Human Issue #11: missed

**Findings classification:**
- Major 1 (SEIQR rprocess omits N-normalization in force of infection): A — no matching human issue
- Major 2 (Log-likelihoods on incommensurable scales, cannot be compared): A — no matching human issue
- Major 3 (SEIQR measurement model links to Q stock without accumulator): B — (matches Human Issue #3)
- Major 4 (Non-convergence acknowledged but results interpreted substantively): A — no matching human issue
- Major 5 (SEIR Euler step size delta.t=7 inconsistent with daily data): A — no matching human issue
- Major 6 (SEIR local search pairs plot displays SIR data): A — no matching human issue
- Major 7 (No non-mechanistic benchmark comparison): B — (matches Human Issue #5)
- Major 8 (Global search box excludes MLE region — eta range mismatch): B — (matches Human Issue #10)
- Major 9 (No profile likelihoods or confidence intervals): A — no matching human issue
- Minor: Population size discrepancy in introduction: C — no matching human issue
- Minor: SEIQR global search uses %do% instead of %dopar%: C — no matching human issue
- Minor: SEIR partrans in mif2 call redundant and potentially inconsistent: C — no matching human issue
- Minor: Fixed initial conditions not estimated or assessed for sensitivity: D — (matches Human Issue #1)
- Minor: No model diagnostics beyond visual inspection: C — no matching human issue
- Minor: Conclusion incorrectly describes log-likelihood direction: D — (matches Human Issue #4)
- Minor: Computational effort is low and not justified: C — no matching human issue
- Minor: No assessment of model adequacy for the full pandemic period: C — no matching human issue

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
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "22.23.1 — Incomparable measurement models invalidate the model comparison")
- Human Issue #4: covered (matched by finding: "22.23.13 — 'Lowest log-likelihood = best model' is non-standard language")
- Human Issue #5: covered (matched by finding: "22.23.7 — No non-mechanistic benchmark")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "22.23.4 — SIR global search box excludes the local MLE region")
- Human Issue #11: missed

**Findings classification:**
- 22.23.1: B — Incomparable measurement models (SEIQR uses Q stock / dnorm vs. SIR/SEIR accumulator / dbinom) invalidate model comparison (matches Human Issue #3)
- 22.23.2: A — SEIQR force of infection missing division by N
- 22.23.3: A — SEIR uses weekly Euler step (delta.t=7) on daily data
- 22.23.4: B — SIR global search eta box [0.4, 0.6] excludes local MLE region [0.94, 0.96] (matches Human Issue #10)
- 22.23.7: B — No non-mechanistic (ARMA/SARIMA) benchmark fitted (matches Human Issue #5)
- 22.23.8: A — No profile likelihoods or confidence intervals reported
- 22.23.5: A — SEIQR declared best model despite non-converged mif2 trace plots
- 22.23.6: C — SEIR pairs plot erroneously plots SIR likelihood data (code bug)
- 22.23.9: C — mu_IR = 0.006 in SIR MLE implies 167-day infectious period, biologically implausible for Omicron
- 22.23.13: D — "Lowest log-likelihood = best model" is non-standard; should read "highest" (matches Human Issue #4)
- Diag (no ID): C — No per-time-point conditional log-likelihoods or ESS diagnostics reported

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
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 7 | 6 | 6 | 4 |
| B (AI major, human also found) | 1 | 1 | 3 | 3 |
| C (AI minor, human missed) | 4 | 5 | 6 | 3 |
| D (AI minor, human also found) | 2 | 2 | 2 | 1 |
| E (Human found, AI missed) | 7 | 7 | 6 | 7 |
| F (Human-AI contradiction) | 1 | 1 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 2 | 7 | 3/10 = 30% | 7 | 4 | 11/14 = 79% |
| Charlie | 1 | 2 | 7 | 3/10 = 30% | 6 | 5 | 11/14 = 79% |
| Doug | 3 | 2 | 6 | 5/11 = 45% | 6 | 6 | 12/17 = 71% |
| Evan | 3 | 1 | 7 | 4/11 = 36% | 4 | 3 | 7/11 = 64% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: Likelihood should not be reported to 4 decimal places. 1 or 2 is sufficient. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: SEIQR has been used in a previous STATS/DATASCI 531 project, but here the development seems to be independently derived from a separate source. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: The initializer does not quite satisfy the constraint of summing to $N$. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: In the implementation of the measurement model, the authors manually override the loglikelihood as -1000 whenever the loglikelihood is numerically evaluated as infinite. This requires care since it could hide other problems. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #11: Where possible, numbers should not be hard-coded in the Rmd document. Rather, they should be referenced using inline R code. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 5 out of 11 human issues (45%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
