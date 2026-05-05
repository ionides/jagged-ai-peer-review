# Ned-Clean Analysis — W21 Project 04

---

## Human Issues

1. In Section 5.3, the bimodality in the likelihood surface (clustered values with one mode roughly 2 log units higher, corresponding to quite different values of phi and H_0) deserves further comment, interpretation, and investigation.
2. There is a possible relationship in the coherence plot at low frequencies (coherence close to 0.6 near frequency zero); it is unclear whether this is where the relationship was expected, or whether a high-frequency relationship was anticipated.
3. Models should be written out to motivate discussion of model assumptions and how well they stand up to the data analysis.
4. When making a likelihood ratio test, explain exactly what was tested and how.
5. There is room for more discussion of limitations — what sorts of relationships could exist that would not have been discovered by the investigation carried out?

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- [1] Log-likelihood comparison GARCH vs POMP not apples-to-apples: A — invalid direct comparison due to differing parameter counts and model structures, no AIC/BIC adjustment
- [2] No convergence diagnostics for MIF2: A — no trace plots of log-likelihood or parameters across iterations
- [3] Particle filter on simulated data does not demonstrate identifiability: A — only a log-likelihood is reported; no parameter re-estimation on simulated data shown
- [4] Simulation from fitted model is absent: A — no posterior predictive checks or visual overlay of simulated paths
- [5] Missing standard errors/CIs for MLE parameter estimates: A — no profile likelihood intervals or Monte Carlo standard errors for point estimates
- [6] Log-likelihood of -539.67 for simulated data implausibly large and unexplained: A — enormous discrepancy vs -25.71 for real data, suggests coding error or dataset substitution
- [7] Loess date axis incorrectly constructed (seq from=1962 instead of 1990): A — x-axis shifted ~28 years to the left
- [8] CPI data manipulation adds duplicate row without justification: A — spurious March 2021 data point manufactured from February value
- [9] GARCH model output suppressed with include=FALSE: C — full GARCH summary hidden from reader
- [10] Model closely adapted from course notes without sufficient acknowledgment: C — minimal justification for applying equity-volatility model to interest rate data
- [11] Global search box for phi restricted to (0.95, 0.99) without justification: C — constraint borrowed from equity application without motivation
- [12] LRT applied to HP-filtered data without acknowledging statistical consequences: C — HP filter introduces serial correlation that distorts chi-squared distribution of LRT
- [13] Monthly data uses first trading day, not average: C — minor timing noise up to one week per month
- [14] Title typo "Yied" should be "Yield": C — proofreading error
- [15] Conclusion conflates number of parameters with model quality: C — raw log-likelihood comparison without complexity penalty

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- [1] GARCH vs POMP likelihood comparison invalid (non-standard normalization): A — tseries package reports non-standard log-likelihood; direct comparison numerically meaningless
- [2] No non-mechanistic ARMA/ARIMA benchmark comparison: A — no ARMA fit to yield differences to test whether mechanistic complexity is warranted
- [3] Profile likelihoods absent; parameter identifiability not assessed: A — pairs plot is not a substitute; no confidence intervals for phi, sigma_eta, sigma_nu
- [4] Local search starts from single fixed initial parameter vector: A — all 20 replicates begin at params_test, providing no diversity of starting points
- [5] Convergence diagnostics (trace plots) not shown: A — no log-likelihood or parameter traces across mif2 iterations
- [6] Global search initialized from previous mif2 result (anti-pattern): A — inherits cooling schedule from if1[[1]]; replicates begin near-frozen rather than from fresh box samples
- [7] AIC comparison not discussed: C — parameter count difference between POMP (6) and GARCH (3) not accounted for in comparison
- [8] Loess span choice not justified: C — span=0.5 and span=0.1 chosen without justification or sensitivity analysis
- [9] Date axis of Loess plot misaligned (seq from=1962): C — x-axis starts 28 years before actual data start of 1990
- [10] Filtering on simulated data section incomplete: C — reports log-likelihood only; no parameter recovery (re-estimation) shown
- [11] Loess plot x-axis start year inconsistent with data range: C — duplicate of issue #9; same date misalignment described again
- [12] Missing sessionInfo() and package version documentation: C — pomp API has changed substantially; reproducibility limited
- [13] CPI LRT conclusion overstated: C — failure to reject null does not establish absence of association; should say "no significant evidence" not "no association"
- [14] CPI labeled "Customer" instead of "Consumer" Price Index: C — terminological error throughout
- [15] Monte Carlo standard error for global search log-likelihood not reported: C — best log-likelihood -25.71 reported without MC SE

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- [1] Simulated-data particle filter reported as real-data benchmark: A — -539.67 is from filtering simulated data, not real Treasury yield data; two likelihoods not comparable
- [2] Invalid direct comparison of GARCH and POMP log-likelihoods: A — tseries normalization non-standard; different measurement model conditioning
- [3] No convergence diagnostics for IF2 (trace plots absent): A — neither local nor global search shows log-likelihood or parameter traces
- [4] No profile likelihoods or parameter uncertainty quantification: A — pairs plots not a substitute; key parameters phi, sigma_eta, sigma_nu not assessed for identifiability
- [5] Global search initialized from previous mif2 result (anti-pattern): A — inherits cooling from if1[[1]]; not true fresh box starts
- [6] No model diagnostics (no simulation-based fit assessment): A — no simulated trajectories compared to observed data, no conditional log-likelihood plots
- [7] No non-mechanistic benchmark comparison for POMP model: A — no ARMA log-likelihood to establish baseline
- [8] Pairs plot filter threshold too wide in local search (20 units vs standard 10): C — includes parameter configurations far from MLE
- [9] Data download fragility and reproducibility risk: C — live URL fetch at render time; data not archived
- [10] GARCH log-likelihood reporting convention not verified: C — triple-colon access to internal function; normalization ambiguity should be acknowledged
- [11] Missing sensitivity analysis of Loess bandwidth: C — span choices not justified or tested
- [12] HP filter lambda=100 not standard for monthly data (standard is 14400): C — under-smoothing monthly series; choice not discussed
- [13] Coherency plot interpretation incomplete: C — no axis labels for economically meaningful frequencies; no significance threshold overlaid
- [14] Title typo "Yied" should be "Yield": C — proofreading error
- [15] Initial conditions not discussed for identifiability: C — H_0 varies substantially across global search; G_0 and H_0 sensitivity never discussed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- [21.04.4] Missing convergence diagnostics (mif2 trace plots): A — no trace plots of log-likelihood or parameters across iterations; convergence of MLE -25.71 unverifiable
- [21.04.5] No profile likelihoods; parameter identifiability not addressed: A — phi clustered near upper boundary (0.99), sigma_nu shows substantial spread; consistent with ridge; no CIs reported
- [21.04.9] No ARMA/ARIMA benchmark: A — only GARCH compared; no linear baseline for yield differences
- [21.04.1] Likelihood comparison incomplete (AIC absent; MC SE unreported): C — parameter count difference not accounted for; SE for best POMP log-likelihood not reported
- [M1] Normal measurement model not evaluated against fat-tailed alternatives: C — no QQ-plot of standardized residuals; excess kurtosis not checked
- [M2] No economic interpretation of fitted volatility path H_t: C — filtered H_t not plotted or annotated against known financial events
- [21.04.6] HP filter lambda=100 not standard for monthly data: C — standard is 14400; choice not justified
- [21.04.13] No sessionInfo or package versions: C — reproducibility limited
- [21.04.11] Title typo "Yied" should be "Yield": C — proofreading error

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 8 | 6 | 7 | 3 |
| B (AI major, human also found) | 0 | 0 | 0 | 0 |
| C (AI minor, human missed) | 7 | 9 | 8 | 6 |
| D (AI minor, human also found) | 0 | 0 | 0 | 0 |
| E (Human found, AI missed) | 5 | 5 | 5 | 5 |

---

## Per-Reviewer Metrics

- Human Recall = (B + D) / (B + D + E)
- AI-Unique Rate = (A + C) / (A + B + C + D)

| Reviewer | B | D | E | Human Recall | A | C | AI-Unique Rate |
|----------|--:|--:|--:|-------------:|--:|--:|---------------:|
| Alex     | 0 | 0 | 5 | 0/5 = 0.00   | 8 | 7 | 15/15 = 1.00   |
| Charlie  | 0 | 0 | 5 | 0/5 = 0.00   | 6 | 9 | 15/15 = 1.00   |
| Doug     | 0 | 0 | 5 | 0/5 = 0.00   | 7 | 8 | 15/15 = 1.00   |
| Evan     | 0 | 0 | 5 | 0/5 = 0.00   | 3 | 6 | 9/9 = 1.00     |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover (all 5 reviewers missed all 5 issues):

1. Bimodality in the likelihood surface (Section 5.3) — two distinct modes ~2 log units apart corresponding to different phi and H_0 values — deserves comment and investigation.
2. Possible low-frequency relationship in coherence plot (coherence ~0.6 near frequency zero) — unclear whether this was the expected direction of relationship.
3. Models should be written out to motivate discussion of model assumptions.
4. The likelihood ratio test lacks explanation of exactly what was tested and how.
5. More discussion of limitations needed — what relationships could exist that the investigation would not have detected.

**Count: 5 out of 5 human issues are consensus misses (5/5 = 1.00).**

### Unique finds per reviewer

Since every reviewer missed all 5 human issues and no reviewer covered any human issue, no reviewer has any "unique finds" in the sense of human issues covered by that reviewer alone.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex     | 0 |
| Charlie  | 0 |
| Doug     | 0 |
| Evan     | 0 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention. The following concerns appear across all four reviewers:

1. No convergence diagnostics / trace plots for mif2 (raised by Alex [#2], Charlie [#5], Doug [#3], Evan [21.04.4])
2. No profile likelihoods / parameter identifiability not assessed (raised by Alex [#5], Charlie [#3], Doug [#4], Evan [21.04.5])
3. Invalid GARCH vs POMP log-likelihood comparison (raised by Alex [#1], Charlie [#1], Doug [#2], Evan [21.04.1 — minor])
4. No ARMA/ARIMA non-mechanistic benchmark (raised by Charlie [#2], Doug [#7], Evan [21.04.9]; Alex did not raise this explicitly)
5. Title typo "Yied" (raised by Alex [#14], Charlie [#14 — via "Customer/Consumer" — actually that is different], Doug [#14], Evan [21.04.11])
6. HP filter lambda not standard for monthly data (raised by Charlie implicitly via coherence discussion; Doug [#12]; Evan [21.04.6]; not by Alex)

Strictly universal (all four reviewers):
- Missing convergence diagnostics / trace plots: raised by all 4 reviewers
- No profile likelihoods / identifiability not assessed: raised by all 4 reviewers
- Title typo: raised by Alex, Doug, Evan (Charlie raises a different terminological error — "Customer vs Consumer" — not the title typo; so title typo is 3 of 4 reviewers)

**Universal AI-only flags (all 4 reviewers): 2**
1. Missing convergence diagnostics / mif2 trace plots
2. No profile likelihoods / parameter identifiability not assessed
