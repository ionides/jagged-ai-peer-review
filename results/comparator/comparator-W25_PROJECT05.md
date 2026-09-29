# Comparator Analysis — W25 Project 05

---

## Human Issues

1. In the conclusion, these two likelihoods are improperly compared: "as seen in the difference in likelihoods between the SARIMA model (-96) and the POMP models (-328), there is a significant scope for improvement in the mechanistic models." The SARIMA is fitted to the log of the data, and not adjusted for the transformation.

2. The STL decomposition is informative here, unlike various other epidemic time series. Here, it is not necessary to take logarithms to linearize the dynamics, because this low-prevalence situation (in US, malaria does not spread effectively) is already close to linear, additive dynamics.

3. One could consider detrending rather than concluding "differencing the series will be advisable and possibly needed."

4. Using a periodogram to infer seasonality is overkill. If the periodogram does not show anything surprising (often the case) you don't have to claim that you use it to infer annual seasonality.

5. SARIMA model AIC comparison does not take into account the loss of a datapoint when differencing; AIC is not perfectly comparable.

6. The SARIMA residual diagnostics show a good fit. The report does not explain clearly that this is fitted to the log of the data.

7. It would be nice to have the Jacobian correction so that the SARIMA log-likelihood for log-data can be properly compared to the POMP log-likelihood for the raw data.

8. Two log-likelihoods claimed to both equal -332.02 are neither equal to -332.01 (they are -331.077 and -331.386). A strange typo, but fortunately these likelihoods are indeed close.

9. Rainfall data could be very helpful as a covariate given the known ecology of the mosquito vector. Including that is beyond the expected scope for a good 531 project.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "SARIMA log-likelihood comparison (-96 vs -328) not meaningful — SARIMA fitted on log-transformed data, no Jacobian adjustment applied")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "SARIMA log-likelihood comparison (-96 vs -328) not meaningful — SARIMA fitted on log-transformed data, no Jacobian adjustment applied")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (Immigration model not incorporated into POMP object): A — critical flaw; immigration rproc never recompiled into pomp object
- Finding 2 (lambda not multiplied by dt in Euler step for dSE): A — standard Euler-Multinomial bug making model step-size dependent
- Finding 3 (SARIMA log-likelihood comparison -96 vs -328 not meaningful): B — SARIMA fitted on log-transformed data, no Jacobian adjustment, likelihoods not comparable (matches Human Issues #1 and #7)
- Finding 4 (sigma_M defined but never used in measurement model): A — model claims overdispersion but implements Poisson
- Finding 5 (Cumulative cases C accumulated but not used in measurement model): A — conceptual disconnect between state space and observation model
- Finding 6 (Population size N_0 = 100000 unrealistically small): A — never justified, affects entire transmission dynamics
- Finding 7 (Birth rate r = 0.135 implausibly large): A — biologically impossible, inconsistent with global search prior
- Finding 8 (global_inits creates duplicate parameter entries via c()): A — global search initialization unreliable
- Finding 9 (No likelihood profile or parameter uncertainty quantification): A — significant gap in inferential framework
- Finding 10 (Periodic B-spline not truly periodic): C — splines::bs() does not enforce boundary periodicity
- Finding 11 (Force of infection missing * dt in mathematical equations): C — inconsistency between SDE exposition and Euler implementation
- Finding 12 (mu_H described as immunity loss but governs natural death): C — mislabeled biological parameter
- Finding 13 (AIC model search grid too narrow): C — p_max=q_max=P=Q=1 excludes higher-order models without justification
- Finding 14 (decompose() uses additive model without justification): C — inconsistent with discussion of non-constant variance
- Finding 15 (No formal residual diagnostic tests for SARIMA): C — only visual inspection, no Ljung-Box or normality tests

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Major Issue 6 — SARIMA AIC and POMP log-likelihood compared on different scales, including that SARIMA is fit to log-transformed data and comparison requires Jacobian correction")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Major Issue 6 — SARIMA AIC and POMP log-likelihood compared on different scales, including that SARIMA is fit to log-transformed data and comparison requires Jacobian correction")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Major Issue 1 (immigration model never implemented in pomp object): A — immigration rprocess never rebuilt; all immigration results unreliable
- Major Issue 2 (rate parameters in days applied to monthly model): A — mu_EI and gamma off by factor ~30
- Major Issue 3 (measurement model code contradicts description; sigma_M unused): A — rmeas uses hardcoded 1e-6 instead of epsilon; sigma_M has no effect
- Major Issue 4 (accumulator C tracked but never used in observation model): A — C computed but discarded; dmeas uses I instead
- Major Issue 5 (no profile likelihoods and no confidence intervals): A — scatter plots are not profiles; identifiability claims unsupported
- Major Issue 6 (SARIMA AIC and POMP log-likelihood compared on different scales): B — comparison invalid because SARIMA is on log-scale and -96 is AIC not loglik; Jacobian correction needed (matches Human Issues #1 and #7)
- Major Issue 7 (global search starting points incorrectly constructed — duplicate parameter names): A — diversity of starting points defeated; effectively a local search
- Major Issue 8 (no benchmark model comparison for POMP): A — no ARMA or negative binomial baseline for raw counts
- Minor — Periodogram x-axis mislabeled: C — axis says cycles per year but unit is cycles per month
- Minor — SARIMA model equation notation error: C — missing backshift operator B in first factor
- Minor — Population size N_0 = 100,000 not justified: C — Florida population was ~18–20 million; choice unexplained
- Minor — Birth rate r = 0.135/month biologically implausible: C — implies >100% annual birth rate
- Minor — sigma_M listed in parameter table as overdispersion but never used: C — creates false impression of overdispersion in measurement model
- Minor — No formal model comparison between initial and immigration models: C — no LRT or AIC; identical loglik claimed without scrutiny
- Minor — Causal language in conclusions: C — observational model fit does not establish causal mechanism

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

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Invalid comparison between SARIMA and POMP log-likelihoods — SARIMA fitted to log-transformed data, POMP to raw counts, likelihoods not numerically comparable")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Invalid comparison between SARIMA and POMP log-likelihoods — SARIMA fitted to log-transformed data, POMP to raw counts, likelihoods not numerically comparable")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Major #1 (Invalid SARIMA/POMP log-likelihood comparison): B — SARIMA fitted to log-transformed counts under Gaussian model, POMP fitted to raw counts under Poisson; likelihoods not numerically comparable (matches Human Issues #1 and #7)
- Major #2 (Measurement model inconsistent between text and code): A — dmeasure links to I compartment but accumulator C tracks dEI; fundamental mismatch with stated model
- Major #3 (No non-mechanistic benchmark comparison on same scale): A — no auto-regressive Poisson/NB benchmark fitted to original count data
- Major #4 (Inadequate global search scale — 20 replicates, 100 iterations): A — too sparse for a 14+ parameter model
- Major #5 (No profile likelihoods or confidence intervals): A — scatter plots from global search treated as informal profiles but have no valid statistical interpretation
- Major #6 (No convergence diagnostics — no log-likelihood traces): A — parameter trace plots shown but no likelihood traces
- Major #7 (Measurement model lacks overdispersion — Poisson only): A — sigma_M in paramnames but not used in dmeasure/rmeasure
- Major #8 (Accumulator C declared in accumvars but never read by dmeasure/rmeasure — dead code): A — C accumulated but measurement links to I, making C unused
- Major #9 (Population dynamics specification implausible — N_0=100,000 for Florida, r=0.135/month): A — 200-fold population error distorts force of infection; birth rate implies >100% annual growth
- Major #10 (Global search parameter box initialization error — c() duplicate names not overridden): A — global search effectively runs 20 replicates of local search, not a genuine global search
- Minor: Notation error in SARIMA equation (missing backshift operator on theta_1): C — equation written as (1+theta_1) instead of (1+theta_1*B)
- Minor: AIC grid search is narrow (p,q only in {0,1}): C — limited grid with no justification for excluding higher orders
- Minor: No Ljung-Box or formal residual test for SARIMA: C — relies on visual ACF inspection only
- Minor: sigma_M not used in model (dead parameter in paramnames): C — appears in paramnames and parameter_trans but not in dmeasure or rmeasure
- Minor: Birth rate r=0.135/month biologically implausible: C — implies >100% annual growth, off by two orders of magnitude from Florida's actual rate
- Minor: epsilon semantics are ambiguous: C — background term described without epidemiological mechanism; may dominate force of infection at near-zero I
- Minor: No convergence traces for local search: C — local search trace plots not presented
- Minor: Simulation from best_local uses wrong parameter vector length (fragile index-based slicing): C — should select parameter columns by name
- Minor: No acknowledgment of model limitations for constant immigration rate: C — imported malaria cases likely heterogeneous in time, constant-rate Poisson may be poor approximation

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 9 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by findings: "25.05.1 — invalid likelihood comparison: SARIMA on log1p vs POMP on raw data"; "25.05.2 — no valid benchmark on the same data scale")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "25.05.1 — invalid likelihood comparison: SARIMA on log1p vs POMP on raw data, Jacobian correction needed")
- Human Issue #8: covered (matched by finding: "25.05.10 — reported loglik -332.02 inconsistent with printed output -331.39 and -331.08")
- Human Issue #9: missed

**Findings classification:**
- 25.05.1: B — invalid likelihood comparison between SARIMA (log1p-transformed) and POMP (raw data) (matches Human Issues #1 and #7)
- 25.05.2: B — no valid non-mechanistic benchmark on the same data scale (matches Human Issue #1)
- 25.05.3: A — sigma_M declared but never used; measurement model is pure Poisson despite text implying overdispersion
- 25.05.4: A — cumulative C tracked with accumvars but measurement model observes rho*I, not rho*C
- 25.05.5: A — convergence not demonstrated; trace plots show no convergence at iteration 100
- 25.05.6: A — no profile likelihoods or confidence intervals for any parameter
- 25.05.7: A — biologically implausible mu_EI (~2.3 day latent period) and gamma (~0.76 day infectious period) not discussed
- 25.05.11: A — N_0 = 100,000 far below Florida's actual population (~18-20 million)
- 25.05.8: C — initial r = 0.135 implausible as monthly birth rate (carryover from dengue source model)
- 25.05.10: D — reported loglik = -332.02 inconsistent with printed output (-331.39 and -331.08) (matches Human Issue #8)
- 25.05.12: C — ESS not monitored; filter degeneracy not checked
- 25.05.13: C — forward simulations misrepresented as fit assessment rather than prior predictive checks
- 25.05.M1: C — immigration model improvement marginal by AIC (DAIC ≈ +0.4 favoring simpler model)
- 25.05.15: C — notation error in SARIMA equation: missing backshift operator B in MA(1) polynomial
- 25.05.14: C — periodogram x-axis label says "cycles per year" but spec.pgram with frequency=12 produces cycles per month

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 8 | 7 | 9 | 6 |
| B (AI major, human also found) | 1 | 1 | 1 | 2 |
| C (AI minor, human missed) | 6 | 7 | 9 | 6 |
| D (AI minor, human also found) | 0 | 0 | 0 | 1 |
| E (Human found, AI missed) | 7 | 7 | 7 | 6 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 0 | 7 | 2/9 = 22% | 8 | 6 | 14/15 = 93% |
| Charlie | 1 | 0 | 7 | 2/9 = 22% | 7 | 7 | 14/15 = 93% |
| Doug | 1 | 0 | 7 | 2/9 = 22% | 9 | 9 | 18/19 = 95% |
| Evan | 2 | 1 | 6 | 3/9 = 33% | 6 | 6 | 12/15 = 80% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: The STL decomposition is informative here, unlike various other epidemic time series. Here, it is not necessary to take logarithms to linearize the dynamics, because this low-prevalence situation (in US, malaria does not spread effectively) is already close to linear, additive dynamics. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #3: One could consider detrending rather than concluding "differencing the series will be advisable and possibly needed." (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: Using a periodogram to infer seasonality is overkill. If the periodogram does not show anything surprising (often the case) you don't have to claim that you use it to infer annual seasonality. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: SARIMA model AIC comparison does not take into account the loss of a datapoint when differencing; AIC is not perfectly comparable. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: The SARIMA residual diagnostics show a good fit. The report does not explain clearly that this is fitted to the log of the data. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: Rainfall data could be very helpful as a covariate given the known ecology of the mosquito vector. Including that is beyond the expected scope for a good 531 project. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 6 out of 9 human issues (67%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #8: Two log-likelihoods claimed to both equal -332.02 are neither equal to -332.01 (they are -331.077 and -331.386). A strange typo, but fortunately these likelihoods are indeed close. (Covered only by Evan)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 1 |
