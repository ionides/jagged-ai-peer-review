# Comparator Analysis — W24 Project 02

---

## Human Issues

1. Explain acronyms at first occurrence, e.g., CPUE.

2. The alternative prey hypothesis (mentioned in the project title) could be explained in the introduction. It becomes clearer later on, in the model section.

3. The description of what is denoted by 'peak_rodent_year' was a bit lacking. It was only described; "Peak rodent year is scored as "yes", otherwise 'no'" but it does not describe what is meant by that or how it is decided or when.

4. It could have been explicitly explained why the log of CPUE was used in the model instead of the CPUE itself.

5. ARIMA with differencing parameter I>0 does not have immediately comparable likelihood, so is not appropriate as a benchmark. One could use ARMA with a trend (linear, quadratic, or exponential) instead.

6. If the formal null and alternative hypotheses are defined for the KPSS test, it may be clearer what can legitimately be concluded from it.

7. The log-likelihood search is incomplete, as evidenced by the local search beating the preliminary global search.

8. In Fig 3.1, the effective sample size is usually 1, and never more than 2.2. This indicates serious particle depletion. Evidently, Np=50 particles is insufficient, though model improvements may be needed as well as extra computational effort.

9. Diagnostic plot. The starting point has very low likelihood. A search starting from not such a poor place might be easier.

10. To acknowledge the preliminary nature of the mechanistic model, it is premature to conclude that "ARMA is a better fit to the data".

11. There is a mismatch between the text reported log-likelihood (-205) and the value in the R output (-288).

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "POMP/ARIMA log-likelihoods not comparable due to differencing transformation; conclusion ARMA fits better is invalid")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Global search range is extremely narrow and biologically unmotivated")
- Human Issue #8: covered (matched by finding: "Particle filter uses Np=5 for likelihood evaluation after mif2")
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "POMP/ARIMA log-likelihoods not comparable due to differencing transformation; conclusion ARMA fits better is invalid")
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (ARIMA/POMP log-likelihoods not comparable, ARMA-better conclusion invalid): B — matches Human Issues #5 and #10
- Finding 2 (Fox population latent state with no data, model unidentifiable): A
- Finding 3 (Particle filter uses Np=5 for likelihood evaluation after mif2): B — matches Human Issue #8
- Finding 4 (Same noise process W_t^F in both fox and bird equations, math/code inconsistency): A
- Finding 5 (Negative binomial stated but normal distribution implemented): A
- Finding 6 (logCPUE obs_names code error, silently ignored argument): A
- Finding 7 (Global search range is extremely narrow and biologically unmotivated): B — matches Human Issue #7
- Finding 8 (Convergence diagnostics as static images with absolute file paths, non-reproducible): A
- Finding 9 (Log transform on parameters that can be negative or zero): C
- Finding 10 (logRho parameter naming and interpretation confused): C
- Finding 11 (ARIMA model selection has a label error in the text): C
- Finding 12 (Only 2 rows in bird_params_middle.csv, global search nearly failed): C
- Finding 13 (No profile likelihood or confidence intervals computed): C
- Finding 14 (dt=1/52 weekly step size not justified for annual data): C
- Finding 15 (Bibliography file path hardcoded to absolute local path): C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: contradiction (Charlie explicitly endorses the ARIMA benchmark comparison as "commendable" and uses the likelihood gap as evidence of POMP failure; human says ARIMA with I>0 does not have immediately comparable likelihood and is not appropriate as a benchmark)
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Global search produces worse likelihood than local search; poorly designed parameter bounds")
- Human Issue #8: covered (matched by finding: "Np=5 used for particle filter likelihood re-evaluation")
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (POMP fits drastically worse than ARIMA, no corrective action): F — explicitly treats ARIMA(0,1,5) likelihood as a valid comparable benchmark and praises the benchmarking choice as "commendable" (contradicts Human Issue #5)
- Finding 2 (Measurement model discrepancy: negative binomial in text, normal in code): A — major finding, no human issue raised it
- Finding 3 (Np=5 used for particle filter likelihood re-evaluation): B — major finding, matches Human Issue #8 (insufficient particle count causing depletion and unreliable estimates)
- Finding 4 (mif2 internal log-likelihood used directly without pfilter re-evaluation): A — major finding, no human issue raised it
- Finding 5 (Global search worse than local search; poorly designed parameter bounds): B — major finding, matches Human Issue #7 (log-likelihood search is incomplete, evidenced by local search beating global)
- Finding 6 (No profile likelihoods; no parameter uncertainty quantification): A — major finding, no human issue raised it
- Finding 7 (No convergence diagnostics for global search): A — major finding, no human issue raised it
- Finding 8 (No simulation-based model diagnostics): C — minor finding, no human issue raised it
- Finding 9 (Hard-coded absolute file paths undermine reproducibility): C — minor finding, no human issue raised it
- Finding 10 (Noise variable labeling inconsistency in Equation 2): C — minor finding, no human issue raised it
- Finding 11 (Large Monte Carlo SE on local search log-likelihood, SE=8.2): C — minor finding, no human issue raised it
- Finding 12 (ACF figure cross-reference error): C — minor finding, no human issue raised it
- Finding 13 (Global search c(guess, fixed_params) creates ambiguous parameter initialization): C — minor finding, no human issue raised it
- Finding 14 (Local search uses only Nmif=50, insufficient for 12-parameter model): C — minor finding, no human issue raised it
- Finding 15 (Bibliography path is absolute and non-portable): C — minor finding, no human issue raised it

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 1 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "POMP never out-performs ARIMA benchmark; likelihoods not on same scale" and also by finding: "ARMA and POMP log-likelihoods not on same scale")
- Human Issue #6: covered (matched by finding: "KPSS test p-value truncation / null hypothesis semantics misstated")
- Human Issue #7: covered (matched by finding: "Global search critically underpowered — only 2 valid results" and also by finding: "Global search parameter space disconnected from local search region")
- Human Issue #8: covered (matched by finding: "Particle count for likelihood evaluation too small (Np=5)")
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "POMP never out-performs ARIMA benchmark; likelihoods not on same scale")
- Human Issue #11: missed

**Findings classification:**
- M1 (POMP never out-performs ARIMA; likelihoods not on same scale; conclusion dismisses gap): B — POMP model never out-performs ARIMA; conclusion premature; likelihoods not comparable (matches Human Issues #5 and #10)
- M2 (Global search critically underpowered — only 2 valid results of 50): B — global search yields only 2 finite-likelihood results, confirming search is incomplete (matches Human Issue #7)
- M3 (Particle count too small, Np=5 in key evaluation): B — particle count far too small, producing unreliable likelihood estimates and particle depletion (matches Human Issue #8)
- M4 (No profile likelihoods; identifiability unassessed): A — no profile likelihoods computed for any of 12 parameters
- M5 (Bird equation uses fox noise term — model/equation inconsistency): A — bird dynamics equation uses W_t^F instead of W_t^B, inconsistent with code
- M6 (Measurement model states Negative Binomial but code uses Normal): A — text claims Negative Binomial measurement model; code implements Normal distribution
- M7 (Global search parameter space disconnected from local search region): B — global search range excludes local search MLE region, explaining why local beats global (matches Human Issue #7)
- M8 (IF2 convergence not demonstrated; only 50 iterations): A — trace plots show non-convergence at Nmif=50; no convergence evidence provided
- mn1 (Bibliography hard-coded to local path): C — bibliography YAML path is a local absolute path, preventing reproduction
- mn2 (Data path hard-coded): C — read_excel uses absolute local path despite data file being in project's data/ directory
- mn3 (Q_fit_bird_local_mifs.rds contains extra parameters not in Rmd model): C — artifact contains 20 parameters belonging to a different, undescribed model
- mn4 (ARMA and POMP log-likelihoods not on same scale): D — ARIMA fitted to differenced series; POMP on undifferenced logCPUE; comparison invalid without Jacobian adjustment (matches Human Issue #5)
- mn5 (eval=FALSE on global search chunk): C — global search chunk not executed from provided Rmd; results loaded from absolute local path
- mn6 (KPSS test p-value truncation / null hypothesis semantics misstated): D — p-value > 0.05 described as "proving" stationarity; KPSS null is stationarity so this merely fails to reject (matches Human Issue #6)
- mn7 (Parameter γ can produce negative predation rates if γ>1): C — model does not constrain γ ≤ 1; (1−γR_t) can be negative
- mn8 (No simulation-based model validation): C — no forward simulation or filtering distribution comparison; only diagnostic plot from arbitrary starting parameters
- mn9 (ACF section cross-reference error): C — text references wrong figure label; PACF caption reads "ACF of logCPUE"
- mn10 (Missing sessionInfo() and package version documentation): C — no R session info or package versions documented beyond passing mention of pomp version
- mn11 (Rodent covariate treated as known without uncertainty): C — peak rodent year derived from six sources over 140 years; uncertainty not discussed or propagated
- mn12 (Species name misspelling): C — Latin name written as Lapagos lapagos instead of Lagopus lagopus

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 10 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "24.02.1 — ARIMA fit to first-differenced series vs POMP fit to undifferenced series makes log-likelihoods incomparable")
- Human Issue #6: missed
- Human Issue #7: covered (matched by findings: "24.02.4 — global search worse than local search is a clear diagnostic of optimization failure" and "24.02.5 — global search worse than local search, search is broken")
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "24.02.4 — convergence inadequately demonstrated; recommends diverse starting points")
- Human Issue #10: covered (matched by finding: "24.02.1 — conclusion that ARIMA outperforms POMP is unsupported because comparison is invalid")
- Human Issue #11: covered (matched by finding: "24.02.2 — reported log-likelihoods including -205 likely from unreplicated pfilter or mif2 internal estimates; pfilter output shows -288.64 with SE 30.88")

**Findings classification:**
- 24.02.1: B — invalid ARIMA vs POMP log-likelihood comparison; ARIMA fit to differenced series, POMP to undifferenced; conclusion of ARIMA superiority unsupported (matches Human Issues #5 and #10)
- 24.02.2: B — mif2 likelihoods reported without replicated pfilter; SE ~31 log units renders estimates meaningless; -205 vs shown -288.64 discrepancy (matches Human Issue #11)
- 24.02.4: B — convergence inadequately demonstrated; 20-iteration trace plots; global search worse than local search; recommends diverse starting points (matches Human Issues #7 and #9)
- 24.02.3: A — no profile likelihoods or confidence intervals; scatter plot shows non-identifiable parameters
- 24.02.5: B — global search worse than local search; global search is broken or miscoded (matches Human Issue #7)
- 24.02.6: C — measurement model noise structure biologically unusual; logRho initialization at 3 unexplained
- 24.02.7: C — inconsistent notation alternating between log.CPUE and logCPUE
- 24.02.8: C — Figure 2.4 caption says ACF but displays PACF
- 24.02.11: C — ARIMA residuals not validated; no residual ACF shown
- 24.02.13: C — no parameter estimate table; best-found parameter values not reported
- 24.02.15: C — AIC table inconsistency; text states 204.48 but table shows 204.21

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 1 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 4 | 4 | 1 |
| B (AI major, human also found) | 3 | 2 | 4 | 4 |
| C (AI minor, human missed) | 7 | 8 | 10 | 6 |
| D (AI minor, human also found) | 0 | 0 | 2 | 0 |
| E (Human found, AI missed) | 7 | 8 | 6 | 6 |
| F (Human-AI contradiction) | 0 | 1 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 3 | 0 | 7 | 4/11 = 36% | 5 | 7 | 12/15 = 80% |
| Charlie | 2 | 0 | 8 | 2/10 = 20% | 4 | 8 | 12/14 = 86% |
| Doug | 4 | 2 | 6 | 5/11 = 45% | 4 | 10 | 14/20 = 70% |
| Evan | 4 | 0 | 6 | 5/11 = 45% | 1 | 6 | 7/11 = 64% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: Explain acronyms at first occurrence, e.g., CPUE. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: The alternative prey hypothesis (mentioned in the project title) could be explained in the introduction. It becomes clearer later on, in the model section. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #3: The description of what is denoted by 'peak_rodent_year' was a bit lacking. It was only described; "Peak rodent year is scored as "yes", otherwise 'no'" but it does not describe what is meant by that or how it is decided or when. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: It could have been explicitly explained why the log of CPUE was used in the model instead of the CPUE itself. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 4 out of 11 human issues (36%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #6: If the formal null and alternative hypotheses are defined for the KPSS test, it may be clearer what can legitimately be concluded from it. (Covered only by Doug)
- Human Issue #9: Diagnostic plot. The starting point has very low likelihood. A search starting from not such a poor place might be easier. (Covered only by Evan)
- Human Issue #11: There is a mismatch between the text reported log-likelihood (-205) and the value in the R output (-288). (Covered only by Evan)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 2 |
