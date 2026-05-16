# Ned-Clean Analysis — w25 Project 16

---

## Human Issues

1. Analysis (plotting, ACF, spectral, ARMA) should be done on a log scale; the log-ARMA likelihood also needs care.
2. The reporting rate estimated close to one and no susceptible depletion indicate the mechanistic model is not working well; the true pertussis reporting rate is likely very low.
3. The SEIR model has no overdispersion in the process model and no seasonality; the mechanistic model needs more work.
4. Diagnostic plots (effective sample size, likelihood anomalies, etc.) are missing, making it hard to assess whether POMP model failures are due to misspecification, poor initialization, or numerical instability.
5. ARCH is an unintuitive/inappropriate model for epidemics.
6. For comparing SEIR with ARCH, likelihood is a better measure than relying on a few hold-out timepoints.
7. Section/equation/figure numbers would be helpful to the reader.
8. The report would benefit from a consolidated summary table (model type, log-likelihood, parameter estimates, model stability/convergence notes).

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Local MIF2 convergence — ESS and convergence diagnostics not reported")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Finding 1 (MAJOR): A — Invalid log-likelihood comparison between ARCH and SEIR
- Finding 2 (MAJOR): A — Missing data handled by interpolation with no sensitivity analysis
- Finding 3 (MAJOR): A — SEIR model fails to reproduce 2024 outbreak; root cause not diagnosed
- Finding 4 (MAJOR): A — k (overdispersion parameter) fixed throughout all POMP models without justification
- Finding 5 (MAJOR): A — H accumulator tracks recoveries (dN_IR), not infections; measurement model inconsistent
- Finding 6 (MAJOR): A — ADF stationarity test referenced in bibliography but never performed
- Finding 7 (MAJOR): A — ARCH vs ARMA(2,4) comparison uses mismatched sample sizes
- Finding 8 (MODERATE/Minor): C — Global SIR search box extremely wide; mu_IR unidentifiable; no likelihood profile
- Finding 9 (MODERATE/Minor): D — Local MIF2 convergence claimed but ESS and quantitative criteria absent (matches Human Issue #4)
- Finding 10 (MODERATE/Minor): C — rw.sd for beta uses ifelse producing incorrect perturbation schedule
- Finding 11 (MODERATE/Minor): C — Vaccination data from Michigan extrapolated to five states without validation
- Finding 12 (MODERATE/Minor): C — SEIR model initializes H=1 rather than H=0; first measurement biased
- Finding 13 (MINOR): C — Deaths plot y-axis mislabeled "Births"
- Finding 14 (MINOR): C — Pairs plot for full SEIR global search commented out
- Finding 15 (MINOR): C — Scholarship section cites incorrect URL for project2024-2

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Key diagnostics commented out; ESS never reported")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major Issue 1: A — Invalid log-likelihood comparison between ARCH and SEIR
- Major Issue 2: A — H accumulator tracks recoveries rather than new infections
- Major Issue 3: A — Biologically implausible parameter estimates (mu_IR, eta, base_beta ≈ outbreak_beta) not discussed
- Major Issue 4: A — Severe parameter non-identifiability not addressed with profile likelihoods
- Major Issue 5: A — rw.sd argument uses data vector rather than time variable in SEIR local searches
- Major Issue 6: A — No non-mechanistic benchmark comparison on count scale
- Major Issue 7: B — Key diagnostics commented out; ESS never reported (matches Human Issue #4)
- Minor Issue 8: C — Missing data interpolation not documented
- Minor Issue 9: C — ARMA log-likelihood inconsistency between sections (−1368 vs −1366)
- Minor Issue 10: C — ARMA(2,4) convergence failure not addressed
- Minor Issue 11: C — No formal stationarity test before differencing
- Minor Issue 12: C — ARCH(1) order not justified; GARCH not explored despite residual test failures
- Minor Issue 13: C — Omega parameter omitted from ARCH variance equation
- Minor Issue 14: C — SIR local search does not perturb mu_IR
- Minor Issue 15: C — Population assumed constant with no demographic processes

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

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "No model diagnostics — no conditional log-likelihoods, ESS traces, or filtering-distribution simulations")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major Issue 1: A — Invalid log-likelihood comparison between ARCH and POMP models
- Major Issue 2: A — Global search initialized from previous mif2 result objects, not base pomp object
- Major Issue 3: A — Accumulator variable H tracks recoveries (dN_IR), not new infections
- Major Issue 4: A — SIR global search box upper bound for Beta (250) is below the MLE found at 259
- Major Issue 5: A — SEIR model fails to distinguish outbreak from endemic transmission (base_beta ≈ outbreak_beta)
- Major Issue 6: A — No benchmark comparison for mechanistic models
- Minor (label error): C — Deaths plot y-axis labeled "Births" (copy-paste error)
- Minor (ARCH-X spec): C — Potential off-by-one alignment between differenced series and lagged external regressor
- Minor (rw.sd not explicit): C — Global SIR search computational parameters inherited from local mif object, never explicitly stated
- Minor (SEIR initial conditions): C — E=15, I=25 hardcoded initial conditions; no sensitivity analysis
- Minor (missing data imputation): C — Interpolation method for ARMA analysis not documented
- Minor (no SEIR pairs plot): C — Pairs plot for SEIR global search commented out; critical given poor convergence (5/500 replicates within 5 LL units)
- Minor (no model diagnostics): D — No conditional log-likelihoods, ESS traces, or filtering-distribution simulations reported (matches Human Issue #4)
- Minor (SEIR implausibility): C — SEIR MLE has mu_IR = 64 per week and eta = 0.787; biological implausibility not discussed
- Minor (no profile likelihoods): C — Neither SIR nor SEIR reports profile likelihoods; point estimates have unknown uncertainty

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- ID 25.16.1 (Major): A — ARCH vs POMP log-likelihood comparison not valid
- ID 25.16.4 (Major): A — No profile likelihoods computed; identifiability claims drawn from pair-plot scatter only
- ID 25.16.3 (Major): A — Biologically implausible mu_IR estimates (2 hours to 1 day) not diagnosed or discussed
- ID 25.16.11 (Major): A — mu_EI trace spikes and collapses in SEIR local search; instability not discussed
- ID 25.16.2 (Major): A — SIR local search loglik.se = 1.06; no replicated pfilter evaluation for any model
- ID 25.16.7 (Minor): C — SEIR global search finds base_beta ≈ outbreak_beta; time-varying beta structure not exploited
- ID 25.16.5 (Minor): C — Unusually low AIC at ARMA(2,3) = 2739.09 is suspicious given ARMA(2,4) selected
- ID 25.16.13 (Minor): C — First differencing not formally justified; no unit root test (ADF or KPSS)
- Misc-1 (Minor): C — Np and Nmif not stated explicitly in text
- Misc-2 (Minor): C — Several typographical errors in manuscript

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 7 | 6 | 6 | 5 |
| B (AI major, human also found) | 0 | 1 | 0 | 0 |
| C (AI minor, human missed) | 7 | 8 | 8 | 5 |
| D (AI minor, human also found) | 1 | 0 | 1 | 0 |
| E (Human found, AI missed) | 7 | 7 | 7 | 8 |

---

## Per-Reviewer Metrics

| Reviewer | Human Recall | AI-Unique Rate |
|----------|-------------:|---------------:|
| Alex | (0+1)/(0+1+7) = 1/8 = 12.5% | (7+7)/(7+0+7+1) = 14/15 = 93.3% |
| Charlie | (1+0)/(1+0+7) = 1/8 = 12.5% | (6+8)/(6+1+8+0) = 14/15 = 93.3% |
| Doug | (0+1)/(0+1+7) = 1/8 = 12.5% | (6+8)/(6+0+8+1) = 14/15 = 93.3% |
| Evan | (0+0)/(0+0+8) = 0/8 = 0.0% | (5+5)/(5+0+5+0) = 10/10 = 100.0% |

---

## Cross-Reviewer Aggregation

### Consensus Misses

Human issues that every reviewer failed to cover (7 out of 8):

- **Human Issue #1** — Analysis should be done on log scale; log-ARMA likelihood needs care. (4/4 reviewers missed)
- **Human Issue #2** — Reporting rate estimated near one; no susceptible depletion; true pertussis reporting rate likely very low. (4/4 reviewers missed)
- **Human Issue #3** — SEIR model has no overdispersion in process model and no seasonality; mechanistic model needs more work. (4/4 reviewers missed)
- **Human Issue #5** — ARCH is an unintuitive/inappropriate model for epidemics. (4/4 reviewers missed)
- **Human Issue #6** — Likelihood is a better measure than a few hold-out timepoints for comparing SEIR with ARCH. (4/4 reviewers missed)
- **Human Issue #7** — Section/equation/figure numbers would be helpful to the reader. (4/4 reviewers missed)
- **Human Issue #8** — Report would benefit from a consolidated summary table. (4/4 reviewers missed)

Human Issue #4 (diagnostic plots / ESS) was covered by Alex (D), Charlie (B), and Doug (D) — missed only by Evan.

### Unique Finds Per Reviewer

No human issue was covered by exactly one reviewer. Human Issue #4 was covered by Alex, Charlie, and Doug (three reviewers).

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-Only Flags

Issues raised by every reviewer that the human did not mention (2 total):

1. **Invalid log-likelihood comparison between ARCH and SEIR/POMP models** — All four reviewers raised this as a Major finding. The human's only comment on this comparison was positive (praising the "almost-comparability" argument), which was excluded as praise.

2. **No profile likelihoods computed; parameter identifiability not formally assessed** — All four reviewers flagged the absence of profile likelihoods. Alex raised it as a Minor concern (no likelihood profile over mu_IR); Charlie as Major Issue 4; Doug as a Minor bullet; Evan as Major ID 25.16.4.
