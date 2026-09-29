# Comparator Analysis — W24 Project 09

---

## Human Issues

1. Too much unformatted and undescribed R output. Figure numbers and captions would help the reader.

2. ARMA modeling is known to be a poor choice for financial markets, so may not be worth much space in the report. Here, there are many ARMA figures, which are not explained and don't contribute much.

3. Perhaps ARMA-garch is less well motivated than t-garch? The latter can fit long tails (which are present) and does not attempt to explain autocorrelations (which are expected to be small anyway, according to the efficient market hypothesis).

4. It is interesting to investigate the possibility of simplifying the leverage model - that is the sort of analysis which the flexibility of the POMP model class permits.

5. The ARMA(5,5) inverse roots are essentially on the unit circle, indicating numerical instability at the boundary of the causal, invertible parameter space. Concluding this is a good, stable model is wrong. There is no point making the diagnostic plots if you ignore the problems they reveal.

6. The decreasing likelihood through the search iterations suggests model misspecification: the noise in the parameters included for the parameter search is needed to explain the data.

7. The global search has not converged; `H_0` continues to decrease, for example.

8. The code variable `sigma_eta` is not explained in the mathematical description of the model.

9. When phi=1, the model has some singular behavior, since then sigma^2_{w,n}=0 for all choices of sigma_eta and G. Values close to phi=1 occur often. This problem can only be seen if the full model is written out, or one looks at the code. Nevertheless, it may explain some weird convergence diagnostic plots that could have been noticed and used to track down the issue.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "ARIMA fitting is applied to the wrong target variable — models conditional mean, not variance")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "No formal likelihood ratio test between Breto model and no-leverage model")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Global search box bounds for the no-leverage model are implausibly wide")
- Human Issue #8: covered (matched by finding: "Definition of sigma_w^2 in the no-leverage model is stated but never verified; sigma_eta has different effective meanings across the two models")
- Human Issue #9: missed

**Findings classification:**
- Finding 1: A — Profile likelihood construction uses wrong particle filter object (if.box instead of if.prof)
- Finding 2: A — Likelihood comparison across models is not valid due to different data, parameterization, and sign conventions
- Finding 3: A — Periodogram applied to demeaned returns rather than squared/absolute returns (volatility proxy)
- Finding 4: B — ARIMA fitting applied to wrong target variable; models conditional mean not variance (matches Human Issue #2)
- Finding 5: A — No simulation-based model checking for the POMP Breto model
- Finding 6: B — No formal likelihood ratio test between Breto model and no-leverage model (matches Human Issue #4)
- Finding 7: B — Global search box bounds for the no-leverage model are implausibly wide, causing degenerate runs (matches Human Issue #7)
- Finding 8: C — Inconsistency in text-reported vs. output fGarch log-likelihood values
- Finding 9: C — ACF computed on demeaned returns rather than squared demeaned returns in the EDA
- Finding 10: C — Local search uses only a single starting point with no randomization
- Finding 11: C — run_level for the no-leverage model silently reduced to 2, creating unequal computational effort comparison
- Finding 12: C — Initial particle filter test applies to simulated data (sim1.filt) rather than real data (ndx.filt)
- Finding 13: C — No convergence diagnostics for the profile likelihood run
- Finding 14: D — Definition of sigma_w^2 never verified and sigma_eta not connected across the two models (matches Human Issue #8)
- Finding 15: C — Conclusion mischaracterizes the profile likelihood result as validation

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "leverage and no-leverage models compared at incomparable computational levels")
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "declining log-likelihood during local search misdiagnosed as overfitting")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Major 1 (profile likelihood code evaluates global search parameters): A — profile logLik evaluation loop draws from if.box instead of if.prof, invalidating the CI
- Major 2 (incomparable computational run levels for leverage vs. no-leverage): B — leverage and no-leverage models fitted at run_level=3 vs. run_level=2 (matches Human Issue #4)
- Major 3 (declining log-likelihood misdiagnosed as overfitting): B — paper attributes declining local-search trajectory to overfitting rather than model misspecification (matches Human Issue #6)
- Major 4 (profile design uses only 100 of 600 starting points): A — loop bound of 100 covers only ~2–3 sigma_eta values out of 40 designed
- Major 5 (profile CI upper bound at boundary of search range): A — upper CI bound of 1 lies outside searched range [0.5, 0.95], indicating sigma_eta is not identified from above
- Minor: text misquotes its own numerical output: C — text reports max log-likelihood as 3483 when output shows 43483
- Minor: tseries::garch log-likelihood normalization not verified: C — normalization difference between tseries and fGarch not reconciled before comparison
- Minor: no formal AIC/LRT comparison for nested leverage/no-leverage models: C — raw log-likelihood comparison used without chi-squared test for 2 additional parameters
- Minor: no simulation-based goodness-of-fit from fitted model: C — only pre-fitting simulation shown; no forward simulations from MLE overlaid on observed returns
- Minor: initial pfilter applied to simulated data, not real data: C — initial likelihood test uses sim1.filt (simulated returns) rather than actual NASDAQ data
- Minor: spectral analysis applied to returns rather than squared returns: C — periodogram of demeaned returns tests conditional-mean autocorrelation rather than volatility cycles
- Minor: no profiles for phi, mu_h, or sigma_nu: C — only sigma_eta is profiled; identifiability of other key parameters unassessed
- Minor: model selection criteria switch between ARIMA and GARCH sections: C — AIC used for ARMA(5,5) selection but significance used for ARMA+GARCH order reduction
- Minor: stew cache files absent from repository: C — .rda cache files not submitted; reproduction requires multi-hour HPC re-run

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "ARIMA AIC table selects wrong model; ARMA(5,5) likely numerically unstable with near-unit-circle roots")
- Human Issue #6: covered (matched by finding: "Convergence not adequately demonstrated; loglik increases then decreases, not interpreted as misspecification")
- Human Issue #7: covered (matched by finding: "Convergence not adequately demonstrated; loglik increases then decreases, not interpreted as misspecification")
- Human Issue #8: covered (matched by finding: "Inconsistent notation — code uses sigma_eta but no equation reconciles it with the model description")
- Human Issue #9: missed

**Findings classification:**
- Major #1 (pomp-simdata-benchmark-error): A — initial pfilter run on simulated data, not real NASDAQ returns
- Major #2 (pomp-global-search-init-audit): A — global IF2 search initialized from previous mif2 result instead of base pomp object
- Major #3 (profile likelihood wrong parameter source): A — L.prof evaluates coef(if.box[[i]]) instead of coef(if.prof[[i]])
- Major #4 (invalid cross-model log-likelihood comparison): A — GARCH and POMP log-likelihoods compared without AIC/BIC adjustment for parameter count
- Major #5 (computationally unfair no-leverage comparison): A — no-leverage model run at drastically lower computational budget than full model
- Major #6 (convergence not adequately demonstrated): B — loglik increases then decreases not flagged as misspecification; global search convergence unverified (matches Human Issues #6 and #7)
- Major #7 (ARIMA AIC anomaly): B — ARMA(5,5) anomalously low AIC likely reflects numerical instability, near-unit-circle roots (matches Human Issue #5)
- Minor (periodogram frequency units): C — peak frequency not converted to interpretable cycles-per-year units
- Minor (text vs. output discrepancies): C — narrative log-likelihood values inconsistent with rendered output
- Minor (inconsistent notation/sigma_eta): D — code's sigma_eta not reconciled with model equation notation (matches Human Issue #8)
- Minor (sigma_nu converging to zero): C — sigma_nu near zero not flagged as potential unidentifiability of leverage state G
- Minor (missing CI for leverage comparison): C — no likelihood ratio test or confidence interval for leverage vs. no-leverage improvement
- Minor (timing.box assignment error): C — .system.time reference likely out of scope, reported timing unreliable
- Minor (no POMP model diagnostics): C — no ESS trace, conditional log-likelihood plot, or filtering-distribution simulation shown
- Minor (data mislabeling): C — title says NASDAQ 100 but data is NASDAQ Composite (^IXIC)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by AI strength finding 24.09.8: "leverage effect tested via nested model comparison")
- Human Issue #5: covered (matched by finding: "24.09.1 — AIC table anomaly for ARMA(5,5) suggesting numerical optimization failure")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "24.09.6 — convergence not achieved for phi and mu_h")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- 24.09.1: B — AIC table anomaly for ARMA(5,5) indicates numerical optimization failure, making model selection unreliable (matches Human Issue #5)
- 24.09.3/24.09.2: A — mif2-internal likelihood not a valid substitute for replicated pfilter evaluation; max across mif2 runs may overstate true log-likelihood
- 24.09.5: A — profile likelihood too sparse and noisy for reliable 95% CI on sigma_eta
- 24.09.6: B — phi and mu_h fail to converge in global search; conclusions about parameter values and model comparison drawn despite non-convergence (matches Human Issue #7)
- 24.09.4: A — likelihood comparability between GARCH and POMP not fully justified; unexplained ~100 unit discrepancy between fGARCH and tseries GARCH implementations
- Notation inconsistency: C — sigma_{w,n} in full model vs sigma_w in simplified model is ambiguous
- Ljung-Box test: C — Ljung-Box p-values used for model selection rather than AIC-based selection
- ESS not monitored: C — effective sample size from particle filter never reported or discussed
- No summary comparison table: C — no table consolidating log-likelihoods and parameter counts for all four models
- Run level parameters: C — Np and Nmif values scattered across sections rather than in a consolidated run-level table
- sigma_w^2 structural constraint: C — simplified model's constraint sigma_w^2 = sigma_eta^2*(1-phi^2) used without justification
- Strogatz citation: C — reference to Strogatz nonlinear dynamics in conclusion without connection to any methodological claim
- Proofreading: C — multiple typos throughout the manuscript

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 4 | 3 | 5 | 3 |
| B (AI major, human also found) | 3 | 2 | 2 | 2 |
| C (AI minor, human missed) | 7 | 9 | 7 | 8 |
| D (AI minor, human also found) | 1 | 0 | 1 | 0 |
| E (Human found, AI missed) | 5 | 7 | 5 | 6 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 3 | 1 | 5 | 4/9 = 44% | 4 | 7 | 11/15 = 73% |
| Charlie | 2 | 0 | 7 | 2/9 = 22% | 3 | 9 | 12/14 = 86% |
| Doug | 2 | 1 | 5 | 4/9 = 44% | 5 | 7 | 12/15 = 80% |
| Evan | 2 | 0 | 6 | 3/9 = 33% | 3 | 8 | 11/13 = 85% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Too much unformatted and undescribed R output. Figure numbers and captions would help the reader. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #3: Perhaps ARMA-garch is less well motivated than t-garch? The latter can fit long tails (which are present) and does not attempt to explain autocorrelations (which are expected to be small anyway, according to the efficient market hypothesis). (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: When phi=1, the model has some singular behavior, since then sigma^2_{w,n}=0 for all choices of sigma_eta and G. Values close to phi=1 occur often. This problem can only be seen if the full model is written out, or one looks at the code. Nevertheless, it may explain some weird convergence diagnostic plots that could have been noticed and used to track down the issue. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 3 out of 9 human issues (33%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #2: ARMA modeling is known to be a poor choice for financial markets, so may not be worth much space in the report. Here, there are many ARMA figures, which are not explained and don't contribute much. (Covered only by Alex)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
