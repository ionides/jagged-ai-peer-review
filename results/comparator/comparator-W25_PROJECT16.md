# Comparator Analysis — W25 Project 16

---

## Human Issues

1. Plotting, ACF, spectral analysis and ARMA are all best done on a log scale. Then, the log-ARMA likelihood needs to be computed with care (see the measles case study in Chapter 18).

2. The reporting rate is estimated to be close to one, and there is no depletion of susceptibles since cases are much less than N=48×10^6. This particular mechanistic model is not doing a good job. The real reporting rate for pertussis is probably very low, since mild or asymptomatic infections are common.

3. The implemented SEIR model has no overdispersion in the process model and no seasonality. There are various things to try to fix it up. The main contribution of the benchmark likelihoods is to remind us that the mechanistic model is not fully effective yet and needs more work.

4. Given the identified problems with the mechanistic model, it would be good to provide diagnostic plots (effective sample size, likelihood anomalies, etc). Without these, it is difficult to assess whether the POMP models failed due to misspecification, poor initialization, or numerical instability.

5. ARCH is quite an unintuitive model for epidemics; it makes sense when the conditional mean is always constant, i.e., when the integrated process is random variation around exponential growth.

6. For comparing SEIR with ARCH, likelihood is a better measure than relying on a few hold-out timepoints.

7. Section/equation/figure numbers would be helpful to the reader.

8. The report would benefit from a consolidated summary table showing model type, log-likelihood, parameter estimates, and perhaps notes on model stability or convergence.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by findings: "SEIR model failure treated as finding rather than investigated" and "Local MIF2 convergence claimed but ESS and other convergence diagnostics not reported")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Finding 1 (Log-likelihood comparison ARCH vs SEIR invalid): A — different observation spaces make likelihood values non-commensurable; human did not raise this
- Finding 2 (Missing data interpolation undescribed, no sensitivity analysis): A — over two years of missing data handled opaquely; human did not raise this
- Finding 3 (SEIR model failure not diagnosed, pairs plot commented out): B — failure treated as finding rather than investigated, no root-cause analysis (matches Human Issue #4)
- Finding 4 (k overdispersion parameter fixed without justification): A — observation-model k fixed at arbitrary values, no profile; human did not raise this
- Finding 5 (H accumulator tracks recoveries N_IR instead of infections): A — biological measurement model error causing phase shift; human did not raise this
- Finding 6 (ADF test cited in bibliography but never performed): A — stationarity test absent despite citation; human did not raise this
- Finding 7 (ARCH vs ARMA comparison uses mismatched sample sizes): A — different effective n in log-likelihood table; human did not raise this
- Finding 8 (SIR global search bounds implausibly wide, mu_IR unidentifiable): C — biologically implausible upper bound, no profile; human did not raise this
- Finding 9 (MIF2 convergence claimed but ESS and diagnostics absent): D — no quantitative convergence criterion, no ESS from final filter (matches Human Issue #4)
- Finding 10 (rw.sd ifelse misuse applies wrong perturbations to beta): C — MIF2 API misuse in perturbation schedule; human did not raise this
- Finding 11 (Vaccination data from Michigan extrapolated to four other states): C — no validation of representativeness; human did not raise this
- Finding 12 (SEIR initializes accumulator H=1 instead of H=0): C — biases measurement likelihood for first observation; human did not raise this
- Finding 13 (Deaths plot y-axis mislabeled "Births"): C — copy-paste labeling error; human did not raise this
- Finding 14 (Pairs plot for full SEIR global search commented out): C — parameter identifiability cannot be assessed; human did not raise this
- Finding 15 (Citation URL for project2024-2 points to 2020 page): C — minor citation error; human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "SIR global search parameters are biologically implausible but not fully discussed")
- Human Issue #3: covered (matched by finding: "SEIR model consistently fails to capture the outbreak without structural revision")
- Human Issue #4: covered (matched by finding: "Missing convergence diagnostics for the SEIR model used in the ARCH comparison")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major Issue 1 (Invalid likelihood comparison between ARCH and SEIR POMP): A — invalid ARCH vs. SEIR likelihood comparison due to different data transformations and different handling of missing observations
- Major Issue 2 (No profile likelihoods computed; no confidence intervals): A — no profile likelihoods for any parameter; parameters unverified and biologically uninterpreted
- Major Issue 3 (Accumulator tracks recoveries not new infections): A — H += dN_IR instead of dN_SI/dN_EI, systematically misrepresenting what reported cases measure
- Major Issue 4 (Missing convergence diagnostics for comparison SEIR): B — trace plots commented out for the SEIR model driving the key comparison; convergence unverifiable (matches Human Issue #4)
- Major Issue 5 (SEIR consistently fails to capture outbreak without structural revision): B — model simulations systematically underperform and authors do not pursue iterative structural revision (matches Human Issue #3)
- Minor: Vaccination data from one state extrapolated to five: C — Michigan-only vaccination coverage applied uniformly across all five states without sensitivity analysis
- Minor: Overdispersion parameter k fixed without justification: C — k=10 (SIR) and k=5 (SEIR) in the measurement model fixed without estimation or motivation
- Minor: Missing data treatment not stated in text: C — ISNA-based zero log-likelihood contribution for ~127 missing weeks never mentioned in the text
- Minor: Initial H value set to 1 instead of 0: C — accumulator H initialized to 1 in seir_rinit biases first predicted observation
- Minor: Hard-coded outbreak start time not estimated: C — week 332 breakpoint between base_beta and outbreak_beta fixed by visual inspection with no sensitivity analysis
- Minor: Unused variable pertussis_diff_adjusted in ARCH code: C — dead variable created but not used in the ugarchfit call, creating confusion about what data was actually fit
- Minor: Differencing applied without formal stationarity test: C — no ADF or KPSS test before differencing; series may be trend-stationary rather than unit-root
- Minor: SIR global search parameters biologically implausible: D — beta=259 per week and mu_IR=6.92 (infectious period ~1 day) are far outside known pertussis biology, indicating model misspecification (matches Human Issue #2)
- Minor: ARMA(2,4) selected despite convergence problems: C — model with numerical convergence issues used for log-likelihood comparison; multiple starting points not tried

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "SEIR parameter implausibility not discussed")
- Human Issue #3: covered (matched by finding: "No benchmark comparison for the mechanistic models")
- Human Issue #4: covered (matched by findings: "No convergence traces shown for SEIR global search" and "No model diagnostics")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major 1 (Invalid log-likelihood comparison between ARCH and POMP models): A — flags the likelihood comparison as statistically invalid due to different observation models and data transformations; human does not raise this concern
- Major 2 (Global search initialized from previous mif2 result objects): A — IF2 cooling-schedule inheritance defect across all three global searches; human does not raise this
- Major 3 (Accumulator variable H tracks recoveries, not new infections): A — semantic mismatch between dN_IR accumulator and surveillance data meaning; human does not raise this
- Major 4 (SIR global search box excludes region containing the MLE): A — Beta upper bound of 250 is below the MLE of 259; human does not raise this
- Major 5 (SEIR model fails to distinguish outbreak from endemic transmission): A — base_beta ≈ outbreak_beta at MLE; parameter non-identifiability; human does not raise this
- Major 6 (No benchmark comparison for the mechanistic models): B — no count-data statistical benchmark against POMP; matches Human Issue #3 (benchmark likelihoods important for showing mechanistic model inadequacy)
- Minor (Label error in EDA plot): C — y-axis labeled "Births" but data is Deaths; human does not raise this
- Minor (ARCH-X specification off-by-one alignment): C — potential length mismatch between differenced series and lagged external regressor; human does not raise this
- Minor (rw.sd for global SIR search not explicitly set): C — computational parameters inherited from local mif object and not verifiable; human does not raise this
- Minor (SEIR initial conditions E=15, I=25 hardcoded): C — fixed initial conditions not estimated and no sensitivity analysis; human does not raise this
- Minor (Missing data imputation not documented for POMP): C — 2022 interpolation method undescribed; human does not raise this
- Minor (No convergence traces shown for SEIR global search): D — pairs plot for SEIR global search suppressed despite only 5/500 replicates converging; matches Human Issue #4 (diagnostic plots for POMP model needed)
- Minor (No model diagnostics): D — no ESS traces, conditional log-likelihoods per time point, or filtering simulations reported; matches Human Issue #4
- Minor (SEIR parameter implausibility not discussed): D — mu_IR = 64/week and eta = 78.7% are biologically implausible; matches Human Issue #2 (implausible reporting rate and model failure)
- Minor (No profile likelihoods reported): C — profile likelihoods absent for all key parameters; human does not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "25.16.3 — biologically implausible mu_IR estimates indicate mechanistic model misspecification")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "25.16.2 — large loglik.se and no replicated pfilter evaluation leave reported MLE reliability uncertain")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- 25.16.1: A — ARCH vs. POMP log-likelihood comparison is invalid because the two likelihoods are computed on different datasets under different observation models
- 25.16.4: A — no profile likelihoods computed; identifiability claims rest on pair-plot scatter alone
- 25.16.3: B — mu_IR estimates (6.92 and 37.9–64.2) imply infectious periods of hours to one day, never diagnosed or discussed (matches Human Issue #2)
- 25.16.11: A — mu_EI traces spike to >150 then collapse in SEIR local search, signaling non-identifiability or severe likelihood ridges, not discussed in text
- 25.16.2: B — SIR local search reports loglik.se = 1.06 and no replicated pfilter validation is performed for any model (matches Human Issue #4)
- 25.16.7: C — base_beta and outbreak_beta return nearly identical values (8.76 vs. 8.72) in SEIR global search, suggesting the time-switching beta is not being exploited
- 25.16.5: C — ARMA(2,3) shows suspiciously low AIC (~14 units below neighbors) yet ARMA(2,4) is selected; anomaly not investigated
- 25.16.13: C — first differencing applied without unit root test or explicit stationarity justification
- Misc-1: C — Np and Nmif values never stated explicitly in the text, harming reproducibility
- Misc-2: C — several typographical errors throughout the manuscript

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 3 | 5 | 3 |
| B (AI major, human also found) | 1 | 2 | 1 | 2 |
| C (AI minor, human missed) | 7 | 8 | 6 | 5 |
| D (AI minor, human also found) | 1 | 1 | 3 | 0 |
| E (Human found, AI missed) | 7 | 5 | 5 | 6 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 1 | 7 | 1/8 = 12% | 6 | 7 | 13/15 = 87% |
| Charlie | 2 | 1 | 5 | 3/8 = 38% | 3 | 8 | 11/14 = 79% |
| Doug | 1 | 3 | 5 | 3/8 = 38% | 5 | 6 | 11/15 = 73% |
| Evan | 2 | 0 | 6 | 2/8 = 25% | 3 | 5 | 8/10 = 80% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Plotting, ACF, spectral analysis and ARMA are all best done on a log scale. Then, the log-ARMA likelihood needs to be computed with care (see the measles case study in Chapter 18). (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: ARCH is quite an unintuitive model for epidemics; it makes sense when the conditional mean is always constant, i.e., when the integrated process is random variation around exponential growth. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: For comparing SEIR with ARCH, likelihood is a better measure than relying on a few hold-out timepoints. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: Section/equation/figure numbers would be helpful to the reader. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: The report would benefit from a consolidated summary table showing model type, log-likelihood, parameter estimates, and perhaps notes on model stability or convergence. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 5 out of 8 human issues (62%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
