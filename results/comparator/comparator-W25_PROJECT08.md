# Comparator Analysis — W25 Project 08

---

## Human Issues

1. The ADF test is not designed to look for non-stationary variance which is the main issue here. The assertion "we reject the null hypothesis of a unit root and conclude that the series are stationary" is a classic example of false reasoning — not all processes without a unit root are stationary. This logical flaw has consequences for time series analysis.

2. There is a weakly supported assertion that the ARIMA(2,0,2) model captures NFLX's complex dynamics and accounts for its volatile behavior. The ARIMA model cannot explain the volatility dynamics.

3. Various ARMA models are fitted, but not compared against the null (white noise). The larger ARMA models probably have roots close to canceling. Log-returns are close to uncorrelated, so for a linear Gaussian model they are inferred (incorrectly) to be approximately independent.

4. The asymmetric t-distribution for GARCH looks like a suitable model, judged by likelihood, but more could be said about contrasting these different models.

5. The claim that "NFLX consistently exhibits higher volatility than SPY, reflecting its sensitivity to company-specific factors compared to the broader market" is questionable — it seems like the aggregate should (almost) necessarily have lower variability, so it is unclear whether this finding is meaningful.

6. Section 7 is unrelated to course material and doesn't contribute to the model development issues in earlier sections.

7. The model fit of the mechanistic and non-mechanistic models could be compared, e.g., by AIC. One can also compare conditional log-likelihoods of individual observations to see in which parts of the dataset the mechanistic hypothesis is (and is not) helpful.

8. Figure numbers and captions would help the reader.

9. All the time spent on ARMA doesn't make much sense given the GARCH and POMP models. Better to spend additional time on those, looking at additional diagnostics for the models of most interest.

10. The identified points with low effective sample size may indicate a longer-tailed distribution is needed to fit the returns.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "ACF/PACF interpretation contradicts subsequent analysis — slow decay labeled non-stationary but series then concluded stationary")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "GARCH summary statistics hidden via include=FALSE, preventing verification or comparison of model estimates")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "no formal model comparison or likelihood-ratio test against GARCH benchmarks — POMP superiority claim unsupported")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (Measurement equation epsilon_n distribution mismatch): A — code implements N(0,1) but writeup states N(0,sigma_nu); documentation error with no human counterpart
- Finding 2 (No formal model comparison against GARCH benchmarks): B — POMP log-likelihood compared to GARCH without proper scaling or AIC table (matches Human Issue #7)
- Finding 3 (Severe non-convergence and multimodality in NFLX POMP): A — extreme parameter heterogeneity across replicates not corrected; no human counterpart
- Finding 4 (Spurious degenerate parameter combinations not excluded): A — near-unit-root explosive combinations included in plots without screening; no human counterpart
- Finding 5 (Log-return preprocessing introduces spurious zero return): A — c(0, diff(...)) prepends artificial zero passed to POMP filter; no human counterpart
- Finding 6 (ACF/PACF interpretation contradicts subsequent analysis): B — ACF slow decay labeled non-stationary but conclusion is stationarity; faulty stationarity reasoning (matches Human Issue #1)
- Finding 7 (STL decomposition applied to non-stationary price series): A — STL on raw prices with artificial frequency=252 seasonal period; no human counterpart
- Finding 8 (GARCH summary statistics hidden via include=FALSE): D — parameter estimates and fit statistics invisible, preventing model contrast (matches Human Issue #4)
- Finding 9 (Beta confidence interval formula incorrect): C — SE formula ignores residual variance, producing overconfident intervals; no human counterpart
- Finding 10 (Incomplete comment left in published writeup): C — placeholder discussion text visible in rendered HTML; no human counterpart
- Finding 11 (Global search box for phi excludes best local-search region): C — phi bounds (0.9, 0.999) exclude highest-likelihood region (0.75–0.89); no human counterpart
- Finding 12 (No out-of-sample evaluation despite defined holdout set): C — holdout 2023–2025 defined but never used; no human counterpart
- Finding 13 (ARIMA residual autocorrelation for SPY not addressed): C — Ljung-Box significant (p=0.03) but no corrective action taken; no human counterpart
- Finding 14 (Reference 12 URL typo): C — URL points to project07 instead of project11; no human counterpart
- Finding 15 (Repeated code block for saving SPY results): C — identical block appears twice, indicating incomplete script cleanup; no human counterpart

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "ACF description inconsistency — text describes slow decay characteristic of non-stationary series but concludes stationarity, same faulty stationarity reasoning")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Checklist Item 2 — no formal ARMA benchmark table noted in scorecard")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Cross-model AIC comparison lacks a summary table for GARCH and POMP models")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- M1 (Measurement model text-code mismatch: sigma_nu misidentified as observation noise): A — text incorrectly places sigma_nu in dmeasure; code uses dnorm with no sigma_nu
- M2 (Global search box excludes apparent MLE region): A — mu_h box [-1,0] and phi box [0.9,0.999] both exclude the local-search optimum
- M3 (No profile likelihoods despite acknowledged identifiability problems): A — flat surfaces and wide SE ranges noted but no profile computed
- M4 (NFLX optimizer stuck in local maxima; convergence not demonstrated): A — two distinct likelihood clusters ~17 log-units apart; global search does not escape
- M5 (Holdout set created but never evaluated): A — nflx_holdout/spy_holdout 2023–2025 constructed but discarded
- m1 (Unfinished editorial text in Section 8.2): C — visible placeholder "Add direct discussions…" left in submission
- m2 (Incorrect URL in Reference 12): C — Reference 12 duplicates Reference 11 URL
- m3 (ACF description inconsistency in Section 3.1): D — slow decay described as non-stationary indicator but conclusion claims stationarity (matches Human Issue #1)
- m4 (Cross-model AIC comparison lacks a summary table): D — GARCH, GJR-GARCH, and POMP AIC values never placed in a single comparison table (matches Human Issue #7)
- m5 (First observation set to zero via c(0, diff(...))): C — artificial zero return contaminates likelihood
- m6 (Large Monte Carlo SEs in several global search runs not discussed): C — seven runs have logLik_se > 2; one reaches 10.52; not flagged in text
- m7 (Auto-installing packages without user consent): C — install.packages loop runs silently on any missing package
- m8 (pomp version not pinned): C — no renv or sessionInfo; pomp API changes may break reproducibility
- Checklist-2 (No formal ARMA benchmark table, Checklist Item 2 note): D — no comparison of ARMA models against a white-noise null (matches Human Issue #3)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "ACF interpretation error — authors describe ACF as showing non-stationary patterns then conclude stationarity, a self-contradiction that reflects the same faulty stationarity reasoning")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "no benchmark comparison — no AIC table comparing ARIMA/GARCH/POMP"; also matched by finding: "no model diagnostics including conditional log-likelihoods of individual observations")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (Global search box for phi excludes optimal parameter region): A — Major; not raised by humans
- Finding 2 (Measurement model misdescription in submitted document): A — Major; not raised by humans
- Finding 3 (No benchmark comparison for the POMP model): B — Major; no AIC table comparing ARIMA, GARCH, GJR-GARCH, and POMP-SV (matches Human Issue #7)
- Finding 4 (No profile likelihoods — parameter identifiability not quantified): A — Major; not raised by humans
- Finding 5 (No model diagnostics — conditional log-likelihoods, ESS, simulation comparisons): B — Major; absence of per-observation conditional log-likelihoods and ESS monitoring (matches Human Issue #7)
- Finding 6 (Holdout set defined but never evaluated): A — Major; not raised by humans
- Finding 7 (Insufficient computational effort — global search fails to improve on local search): A — Major; not raised by humans
- Finding 8 (ACF interpretation error in Section 3.1): B — Major; ACF described as showing non-stationary patterns for an already-stationary series, then contradicted by authors' own stationarity conclusion — same faulty stationarity reasoning as human issue (matches Human Issue #1)
- Finding 9 (Notation inconsistency in Section 6.2 — sigma_nu initialization): C — Minor; not raised by humans
- Finding 10 (Unfinished draft note left in Section 8.2): C — Minor; not raised by humans
- Finding 11 (Reference [11] used for two different works; Reference [12] URL mismatch): C — Minor; not raised by humans
- Finding 12 (ARIMA residual description uses implausible units): C — Minor; not raised by humans
- Finding 13 (Beta standard error formula is incorrect): C — Minor; not raised by humans
- Finding 14 (STL decomposition applied to non-stationary prices): C — Minor; not raised by humans
- Finding 15 (First log-return set to zero rather than NA): C — Minor; not raised by humans

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "25.08.5 — ACF interpretation contradicts stationarity claim")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "25.08.1 — Cross-model AIC/likelihood comparison is unreliable")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- 25.08.1: B — Cross-model AIC/likelihood comparison is unreliable; POMP superiority claim not established (matches Human Issue #7)
- 25.08.6: A — No profile likelihoods computed despite being promised in methods
- 25.08.4: A — ARIMA model order inconsistency for SPY (auto.arima shows ARIMA(5,0,4) but text says ARIMA(2,0,0))
- 25.08.7: A — Convergence multimodality in NFLX local search not resolved
- 25.08.3: A — sigma_nu notation inconsistency in measurement model
- 25.08.5: D — ACF interpretation contradicts stationarity claim (matches Human Issue #1)
- 25.08.2: C — mu_h estimates not back-transformed to implied volatility or half-life
- 25.08.14: C — Holdout set defined but never used to evaluate predictive accuracy
- 25.08.M2: C — Log-returns may not be demeaned before POMP fitting
- Additional minor issues: C — Incomplete author note, incomplete sentence in Section 6.2, beta CI formula ignores ARCH effects

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 5 | 5 | 4 |
| B (AI major, human also found) | 2 | 0 | 3 | 1 |
| C (AI minor, human missed) | 7 | 6 | 7 | 4 |
| D (AI minor, human also found) | 1 | 3 | 0 | 1 |
| E (Human found, AI missed) | 7 | 7 | 8 | 8 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 1 | 7 | 3/10 = 30% | 5 | 7 | 12/15 = 80% |
| Charlie | 0 | 3 | 7 | 3/10 = 30% | 5 | 6 | 11/14 = 79% |
| Doug | 3 | 0 | 8 | 2/10 = 20% | 5 | 7 | 12/15 = 80% |
| Evan | 1 | 1 | 8 | 2/10 = 20% | 4 | 4 | 8/10 = 80% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: There is a weakly supported assertion that the ARIMA(2,0,2) model captures NFLX's complex dynamics and accounts for its volatile behavior. The ARIMA model cannot explain the volatility dynamics. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: The claim that "NFLX consistently exhibits higher volatility than SPY, reflecting its sensitivity to company-specific factors compared to the broader market" is questionable — it seems like the aggregate should (almost) necessarily have lower variability, so it is unclear whether this finding is meaningful. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: Section 7 is unrelated to course material and doesn't contribute to the model development issues in earlier sections. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: Figure numbers and captions would help the reader. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #9: All the time spent on ARMA doesn't make much sense given the GARCH and POMP models. Better to spend additional time on those, looking at additional diagnostics for the models of most interest. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #10: The identified points with low effective sample size may indicate a longer-tailed distribution is needed to fit the returns. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 6 out of 10 human issues (60%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #3: Various ARMA models are fitted, but not compared against the null (white noise). The larger ARMA models probably have roots close to canceling. Log-returns are close to uncorrelated, so for a linear Gaussian model they are inferred (incorrectly) to be approximately independent. (Covered only by Charlie)
- Human Issue #4: The asymmetric t-distribution for GARCH looks like a suitable model, judged by likelihood, but more could be said about contrasting these different models. (Covered only by Alex)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 1 |
| Doug | 0 |
| Evan | 0 |
