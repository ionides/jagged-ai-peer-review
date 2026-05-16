# Ned-Clean Analysis — W25 Project 08

---

## Human Issues

1. The ADF test cannot detect non-stationary variance; concluding stationarity from rejecting the unit root is false reasoning.
2. The assertion that ARIMA(2,0,2) captures volatility dynamics is unsupported — ARIMA cannot explain volatility dynamics.
3. ARMA models are fitted but not compared against the white noise null; larger ARMA models likely have near-canceling roots.
4. More could be said about contrasting the different GARCH models (including the asymmetric t-distribution).
5. The comparison of NFLX vs. SPY volatility (NFLX higher than SPY/the aggregate) is trivially expected and lacks meaningful insight.
6. Section 7 is unrelated to course material and does not contribute to model development.
7. The mechanistic and non-mechanistic model fits could be compared (e.g., by AIC or conditional log-likelihoods of individual observations).
8. Figure numbers and captions would help the reader.
9. Too much time is spent on ARMA when GARCH and POMP models are more relevant; additional time should be spent on those instead.
10. Points with low effective sample size may indicate a longer-tailed distribution is needed.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "ACF/PACF interpretation contradicts stationarity conclusion — both identify faulty stationarity reasoning")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "GARCH summary statistics hidden via include=FALSE, preventing model contrast")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "No formal model comparison or likelihood-ratio test against GARCH benchmarks")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Finding #1 (Measurement model code/text mismatch — sigma_nu phantom): A — epsilon_n distribution discrepancy between written model and code
- Finding #2 (No formal model comparison against GARCH): B — no likelihood-ratio or AIC comparison table (matches Human Issue #7)
- Finding #3 (Non-convergence and multimodality in NFLX POMP not addressed): A — severe parameter heterogeneity not corrected
- Finding #4 (Degenerate parameter combinations not excluded): A — near-unit-root solutions included in pairs plots without screening
- Finding #5 (Spurious zero return from preprocessing): A — c(0, diff(log(Close))) prepends artificial zero to filter
- Finding #6 (ACF/PACF interpretation contradicts stationarity conclusion): B — internal contradiction between ACF description and stationarity conclusion (matches Human Issue #1)
- Finding #7 (STL decomposition on non-stationary price series): A — STL applied to prices with artificial frequency=252
- Finding #8 (GARCH summary statistics hidden with include=FALSE): D — readers cannot verify GARCH parameter estimates or contrast models (matches Human Issue #4)
- Finding #9 (Beta CI formula incorrect): C — sqrt(var(NFLX)/(n*var(SPY))) omits residual variance
- Finding #10 (Incomplete placeholder left in writeup): C — Section 8.2 contains unresolved draft comment
- Finding #11 (Global search phi box restricts range to 0.9–0.999, excluding best region): C — best local-search solutions have phi 0.75–0.89, outside global box lower bound
- Finding #12 (No out-of-sample evaluation despite defined holdout): C — holdout set defined but never used for any model
- Finding #13 (ARIMA SPY residual autocorrelation not addressed): C — Ljung-Box p=0.03 noted but no corrective action taken
- Finding #14 (Reference 12 wrong URL): C — URL points to project07 instead of project11
- Finding #15 (Repeated code block for saving SPY results): C — block appears twice with identical code

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
- Human Issue #1: covered (matched by finding: "Section 3.1 ACF/PACF interpretation error — slow decay described as non-stationarity in stationary log-returns")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Incomplete benchmark comparison for POMP versus GARCH — holdout set never evaluated")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Major #1 (Measurement model discrepancy — sigma_nu phantom): A — code implements no sigma_nu in measurement density despite text stating epsilon_n ~ N(0, sigma_nu)
- Major #2 (Global search fails to improve local search, not flagged as convergence warning): A — NFLX global best (4619.78) below local best (4622.77), attributed to surface shape rather than computational inadequacy
- Major #3 (No profile likelihoods despite clear weak identifiability): A — sigma_nu and sigma_eta show substantial variability; no MCAP intervals computed
- Major #4 (AIC comparison between SV and GARCH not methodologically valid): A — different parameterizations, Monte Carlo error, and first-observation treatment make log-likelihoods non-comparable
- Major #5 (No simulation-based model validation): A — no forward simulation plots, no ESS plots in text, no conditional log-likelihood plots
- Major #6 (Global search phi box in natural space, IF2 perturbations in transformed space): A — uniform draw in [0.9, 0.999] natural space is non-uniform in logit space, biasing toward high-persistence
- Major #7 (Holdout set never evaluated — benchmark comparison incomplete): B — holdout defined but no out-of-sample log-likelihood or RMSE computed for any model (matches Human Issue #7)
- Minor: Section 3.1 ACF/PACF interpretation error: D — stationary log-returns described as showing non-stationarity signature (matches Human Issue #1)
- Minor: Section 3.2 STL decomposition not meaningful: C — seasonal component from frequency=252 has no economic interpretation and is not used in subsequent modeling
- Minor: Section 6.1 notation inconsistency (sigma_nu roles): C — two paragraphs describe sigma_nu inconsistently
- Minor: Section 6.2 duplicate code block: C — spy_local_mif save block appears twice, second block not corrected for global results
- Minor: Section 6.3 misleading ESS claim: C — "most particles contribute effectively" stated but no ESS plots shown
- Minor: Section 8.2 incomplete placeholder: C — draft instruction "Add direct discussions..." not removed before submission
- Minor: References 5 and 6 duplicate/incorrect URLs: C — same Bloomberg URL cited twice under different labels
- Minor: Reference 12 incorrect URL: C — URL points to project07 instead of project11
- Minor: Section 7.4 beta SE formula incorrect: C — omits residual variance; OLS formula requires sigma_eps/(sqrt(n)*sd(SPY))
- Minor: No sessionInfo or package versions: C — version-sensitive packages (pomp, rugarch) not pinned
- Minor: Live data provenance (Yahoo Finance): C — data fetched live with fixed end date; subject to retrospective adjustments
- Minor: No computational cost reported: C — total CPU/wall time for IF2 runs not reported

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 11 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "ACF interpretation error in Section 3.1 — Major — slow decay in stationary log-returns described as non-stationarity")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "No benchmark comparison for POMP model — no unified AIC table for ARIMA, GARCH, and POMP")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Major #1 (Global search phi box excludes optimal region): A — phi box [0.9, 0.999] excludes the highest-likelihood local-search region (phi 0.62–0.89)
- Major #2 (Measurement model misdescription): A — blinded.rmd states epsilon_n ~ N(0, sigma_nu) but code implements epsilon_n ~ N(0,1)
- Major #3 (No unified AIC/benchmark table for all models): B — GARCH comparison table excludes POMP; claimed POMP superiority unsupported (matches Human Issue #7)
- Major #4 (No profile likelihoods): A — pairs plots show IF2 endpoints, not profiles; identifiability unquantified
- Major #5 (No model diagnostics — ESS, conditional log-likelihoods, simulations): A — diagnostics mentioned in text but no figures shown in submitted document
- Major #6 (Holdout set defined but never evaluated): A — nflx_holdout and spy_holdout defined but no RMSE, MAPE, or coverage metrics reported
- Major #7 (Insufficient computational effort — global fails to match local): A — global best 4619.8 vs. local best 4622.8; only 5 of 20 global replicates escape the phi=1 trap
- Major #8 (ACF interpretation error): B — Section 3.1 describes slow decay in stationary log-returns as non-stationarity characteristic (matches Human Issue #1)
- Minor #9 (Notation inconsistency — sigma_nu initialization value): C — text says exp(-5) but code uses exp(-6)
- Minor #10 (Unfinished draft note in Section 8.2): C — placeholder text not removed before submission
- Minor #11 (Reference issues — [11] used for two works, [12] wrong URL): C — inaccurate citations
- Minor #12 (ARIMA residual units implausible — residuals of -100): C — model fitted on log-returns; residuals of -100 impossible at that scale
- Minor #13 (Beta SE formula incorrect): C — residual variance omitted from OLS formula
- Minor #14 (STL decomposition on non-stationary prices): C — closing prices decomposed with frequency=252 without genuine seasonal cycle
- Minor #15 (First log-return set to zero rather than NA): C — c(0, diff(log(Close))) introduces spurious zero observation

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "25.08.5 — ACF interpretation contradicts stationarity claim — Minor")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "25.08.1 — Cross-model AIC/likelihood comparison is unreliable — Major")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- 25.08.1 (Cross-model AIC/likelihood comparison unreliable): B — GJR-GARCH AIC implies log-likelihood higher than POMP; normalization not verified (matches Human Issue #7)
- 25.08.6 (No profile likelihoods computed): A — pairs plots are scatter plots of IF2 endpoints, not profiles; MCAP not computed
- 25.08.4 (ARIMA model order inconsistency for SPY): A — auto.arima shows ARIMA(5,0,4) but text and tables say ARIMA(2,0,0)
- 25.08.7 (Convergence multimodality not resolved): A — two log-likelihood clusters in NFLX local search not remediated with targeted follow-up search
- 25.08.3 (sigma_nu notation inconsistency in measurement model): A — epsilon_n ~ N(0, sigma_nu) in observation equation conflicts with code initializing sigma_nu as leverage process parameter
- 25.08.5 (ACF interpretation contradicts stationarity claim): D — slow decay in stationary log-returns described as non-stationarity signature (matches Human Issue #1)
- 25.08.2 (mu_h estimates not back-transformed): C — mu_h = -7.6 and -9.4 discussed without reporting exp(mu_h/2) as implied daily volatility
- 25.08.14 (Holdout set defined but not evaluated): C — 2023–2025 holdout constructed but no model evaluated against it
- 25.08.M2 (Log-returns may not be demeaned before POMP): C — mean-zero assumption of observation equation not verified
- Additional minor: Incomplete author note in Section 8.2: C — draft placeholder "Add direct discussions..." not removed
- Additional minor: Incomplete sentence in Section 6.2: C — search procedure names omitted
- Additional minor: Beta CI approximate given ARCH evidence: C — formula labeled as standard OLS without acknowledging ARCH violations

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 5 | 6 | 6 | 4 |
| B (AI major, human also found) | 2 | 1 | 2 | 1 |
| C (AI minor, human missed) | 7 | 11 | 7 | 6 |
| D (AI minor, human also found) | 1 | 1 | 0 | 1 |
| E (Human found, AI missed) | 7 | 8 | 8 | 8 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

| Reviewer | B | D | E | Human Recall | A | C | AI-Unique Rate |
|----------|--:|--:|--:|-------------:|--:|--:|---------------:|
| Alex | 2 | 1 | 7 | 30.0% | 5 | 7 | 80.0% |
| Charlie | 1 | 1 | 8 | 20.0% | 6 | 11 | 89.5% |
| Doug | 2 | 0 | 8 | 20.0% | 6 | 7 | 86.7% |
| Evan | 1 | 1 | 8 | 20.0% | 4 | 6 | 83.3% |

- Human Recall = (B+D) / (B+D+E)
- AI-Unique Rate = (A+C) / (A+B+C+D)

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues missed by every reviewer (all four failed to cover):

- Human Issue #2: ARIMA cannot explain volatility dynamics — the assertion that ARIMA captures volatility dynamics is unsupported.
- Human Issue #3: ARMA models not compared against white noise null; larger ARMA models likely have near-canceling roots.
- Human Issue #4: More contrast needed between the different GARCH models.
- Human Issue #5: The NFLX vs. SPY volatility comparison is trivially expected — the aggregate (SPY) should almost necessarily have lower variance.
- Human Issue #6: Section 7 is unrelated to course material and does not contribute to model development.
- Human Issue #8: Figure numbers and captions would help the reader.
- Human Issue #9: Too much time spent on ARMA; additional time should be spent on GARCH and POMP instead.
- Human Issue #10: Points with low ESS may indicate a longer-tailed distribution is needed.

Count: 8 out of 10 human issues were missed by all four reviewers.

### Unique finds per reviewer

For each reviewer, human issues that only that reviewer covered and all others missed:

- Human Issue #1 was covered by all four reviewers (Alex, Charlie, Doug, Evan). Not a unique find for anyone.
- Human Issue #7 was covered by all four reviewers (Alex, Charlie, Doug, Evan). Not a unique find for anyone.

No reviewer has any unique human issue finds — every covered issue was covered by all four reviewers.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention (classified A or C in all four):

1. **Measurement model code/text mismatch (sigma_nu phantom parameter):** All four reviewers independently flag that the measurement equation in the text states epsilon_n ~ N(0, sigma_nu) but the actual code implements epsilon_n ~ N(0,1) with no sigma_nu term in the density. The parameter sigma_nu is estimated but has no effect on the likelihood.

2. **POMP computational inadequacy / convergence multimodality not resolved:** All four reviewers flag that the NFLX global search achieves a lower maximum likelihood than the local search, indicating insufficient computational effort, and that two distinct convergence clusters in the local search are not remediated with targeted follow-up runs.

3. **Incomplete draft placeholder left in Section 8.2:** All four reviewers flag that the instruction "Add direct discussions of how we expanded on the previous projects" was not removed before submission.

4. **Beta standard error formula incorrect in Section 7.4:** All four reviewers flag that the formula sqrt(var(NFLX) / (n * var(SPY))) omits the residual variance and is not the correct OLS standard error for the slope coefficient.

Total universal AI-only flags: 4
