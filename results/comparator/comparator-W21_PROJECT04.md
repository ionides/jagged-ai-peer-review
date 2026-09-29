# Comparator Analysis — W21 Project 04

---

## Human Issues

1. In Section 5.3, notice the indications of bimodality in the likelihood surface (clustered values in the maximized log likelihood). One mode has likelihood roughly 2 log units higher. They correspond to quite different values of phi and H_0. This would be worth further comment, interpretation and maybe investigation.

2. There is a possibility of a relationship in the coherence plot at low frequencies (e.g., a coherence close to 0.6 at frequency close to zero). Is this where you would expect the relationship, or were you expecting a high frequency relationship?

3. Models should be written out. This can help to motivate discussion of model assumptions and how well they stand up to the data analysis.

4. Similarly, when making a likelihood ratio test, explain exactly what was tested and how.

5. There is room for more discussion of limitations. What sorts of relationships could exist that would not have been discovered by the investigation carried out?

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Finding 1: A — GARCH vs POMP log-likelihood comparison invalid without AIC/BIC or parameter-count adjustment
- Finding 2: A — No MIF2 convergence diagnostics or trace plots
- Finding 3: A — Simulated-data particle filter does not demonstrate parameter recovery/identifiability
- Finding 4: A — No simulation from the fitted POMP model
- Finding 5: A — No standard errors or confidence intervals for MLE parameter estimates
- Finding 6: A — Simulated-data log-likelihood of -539.67 versus real-data -25.71 is unexplained
- Finding 7: A — Loess date axis incorrectly starts at 1962 instead of 1990
- Finding 8: A — CPI data has a duplicate row manufactured without justification
- Finding 9: C — GARCH model output suppressed with include=FALSE
- Finding 10: C — Model closely adapted from course notes without sufficient acknowledgment or justification for interest rate data
- Finding 11: C — phi search box restricted to (0.95, 0.99) without justification
- Finding 12: C — LRT for yield-CPI association applied to HP-filtered data without acknowledging statistical consequences
- Finding 13: C — Monthly data uses first trading day rather than average or end-of-month
- Finding 14: C — Title contains typo "Yied" instead of "Yield"
- Finding 15: C — Conclusion conflates number of parameters with model quality

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
- Finding 1 (GARCH/POMP likelihood comparison invalid): A — GARCH log-likelihood from `tseries` uses non-standard normalization, making the central comparison numerically meaningless
- Finding 2 (No ARMA/ARIMA benchmark): A — no non-mechanistic benchmark model compared against the SV POMP model
- Finding 3 (Profile likelihoods absent): A — no profile likelihoods computed for any of the six model parameters; identifiability not assessed
- Finding 4 (Local search from single starting point): A — all 20 local mif2 replicates start from the same `params_test` vector
- Finding 5 (Convergence diagnostics not shown): A — no trace plots shown for any mif2 run despite run_level=3
- Finding 6 (Global search from single local endpoint): A — global search continues from `if1[[1]]` rather than starting fresh from random box draws
- Finding 7 (AIC comparison not discussed): C — parameter count difference and AIC not presented alongside raw likelihood comparison
- Finding 8 (Loess span not justified): C — `span=0.5` and `span=0.1` chosen without justification or sensitivity analysis
- Finding 9 (Loess date axis misaligned): C — time axis starts from 1962 but data begins in 1990
- Finding 10 (Filtering on simulated data incomplete): C — pfilter run on simulated data but no parameter recovery attempted
- Finding 11 (Loess x-axis start year inconsistent): C — duplicate of Finding 9; date sequence from 1962 inconsistent with 1990-onset data
- Finding 12 (Missing sessionInfo): C — no package version documentation included
- Finding 13 (CPI LRT conclusion overstated): C — failure to reject null stated as absence of association rather than lack of significant evidence
- Finding 14 (CPI "Customer" vs "Consumer"): C — consistent terminological error throughout the report
- Finding 15 (Monte Carlo SE not reported for global search): C — best log-likelihood -25.71 reported without Monte Carlo standard error

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
- Human Issue #1: covered (matched by finding: "Initial Conditions Not Discussed for Identifiability — H_0 varied substantially across global search, suggesting weak identification, same underlying concern about H_0/phi behavior in likelihood surface")
- Human Issue #2: covered (matched by finding: "Coherency Plot Interpretation Incomplete — no significance threshold, no axis labels for meaningful frequencies, conclusion of no association unsupported")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Invalid Direct Comparison of GARCH and POMP Log-Likelihoods — comparison invalid due to normalization mismatch and differing observation models"; also matched by finding: "GARCH Log-Likelihood Reporting Convention Not Verified — tseries internal function may omit normalization constants")
- Human Issue #5: missed

**Findings classification:**
- Finding 1 (Simulated-Data Particle Filter as Real-Data Benchmark): A — pfilter run on simulated data, reported log-likelihood of -539.67 compared to -25.71 from real data, datasets differ
- Finding 2 (Invalid GARCH/POMP Log-Likelihood Comparison): B — comparison invalid due to tseries normalization mismatch and differing observation models; POMP "better" conclusion unsupported (matches Human Issue #4)
- Finding 3 (No IF2 Convergence Diagnostics): A — no trace plots for local or global search, impossible to assess IF2 convergence
- Finding 4 (No Profile Likelihoods or Parameter Uncertainty Quantification): A — only point estimates, no profiles, no confidence intervals; identifiability unknown
- Finding 5 (Global Search Anti-Pattern — initialized from mif2 result): A — global replicates inherit cooled perturbations from if1[[1]], not a true global search
- Finding 6 (No Model Diagnostics): A — no simulated trajectories, no conditional log-likelihoods, no filtering distribution plots
- Finding 7 (No Non-Mechanistic Benchmark for POMP): A — no ARMA baseline comparison; GARCH comparison undermined by normalization issue
- Finding 8 (Pairs Plot Filter Threshold Too Wide in Local Search): C — local search uses 20-unit threshold instead of standard 10-unit threshold
- Finding 9 (Data Download Fragility): C — live URL fetch at render time, no archived dataset, inconsistency with local CPI CSV
- Finding 10 (GARCH Log-Likelihood Reporting Convention Not Verified): D — tseries:::logLik.garch may omit normalization constants making GARCH/POMP comparison invalid (matches Human Issue #4)
- Finding 11 (Missing Loess Bandwidth Sensitivity Analysis): C — span=0.5 and span=0.1 unjustified, no sensitivity analysis
- Finding 12 (HP Filter Lambda Not Justified): C — lambda=100 used for monthly data instead of standard 14400, substantially under-smooths
- Finding 13 (Coherency Plot Interpretation Incomplete): D — no significance threshold, no axis labels for economic cycles, conclusion of no association unsupported (matches Human Issue #2)
- Finding 14 (Title Typo): C — "Yied" should be "Yield"
- Finding 15 (Initial Conditions Not Discussed for Identifiability): D — H_0 varied substantially in global search pairs plots suggesting weak identification; role of initial conditions unknown (matches Human Issue #1)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "21.04.5 — No profile likelihoods; parameter identifiability not addressed — pairs plot shows substantial spread in phi clustered near upper boundary, consistent with concerning structure in likelihood surface")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- 21.04.4: A — Missing convergence diagnostics (no mif2 trace plots shown)
- 21.04.5: B — No profile likelihoods; pairs plot shows spread in phi and sigma_nu consistent with problematic likelihood surface structure (matches Human Issue #1)
- 21.04.9: A — No ARMA/ARIMA benchmark provided alongside GARCH comparison
- 21.04.1: C — Likelihood comparison incomplete; AIC not computed, MC SE unreported for real-data MLE
- M1: C — Normal measurement model not evaluated against fat-tailed alternatives
- M2: C — No economic interpretation or plot of the fitted volatility path H_t
- 21.04.6: C — HP filter lambda = 100 not standard for monthly data (Ravn-Uhlig recommend 14,400)
- 21.04.13: C — No sessionInfo or package versions reported
- 21.04.11: C — Title typo ("Yied" should be "Yield")

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 8 | 6 | 6 | 2 |
| B (AI major, human also found) | 0 | 0 | 1 | 1 |
| C (AI minor, human missed) | 7 | 9 | 5 | 6 |
| D (AI minor, human also found) | 0 | 0 | 3 | 0 |
| E (Human found, AI missed) | 5 | 5 | 2 | 4 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 0 | 5 | 0/5 = 0% | 8 | 7 | 15/15 = 100% |
| Charlie | 0 | 0 | 5 | 0/5 = 0% | 6 | 9 | 15/15 = 100% |
| Doug | 1 | 3 | 2 | 3/5 = 60% | 6 | 5 | 11/15 = 73% |
| Evan | 1 | 0 | 4 | 1/5 = 20% | 2 | 6 | 8/9 = 89% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #3: Models should be written out. This can help to motivate discussion of model assumptions and how well they stand up to the data analysis. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: There is room for more discussion of limitations. What sorts of relationships could exist that would not have been discovered by the investigation carried out? (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 2 out of 5 human issues (40%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #2: There is a possibility of a relationship in the coherence plot at low frequencies (e.g., a coherence close to 0.6 at frequency close to zero). Is this where you would expect the relationship, or were you expecting a high frequency relationship? (Covered only by Doug)
- Human Issue #4: Similarly, when making a likelihood ratio test, explain exactly what was tested and how. (Covered only by Doug)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 2 |
| Evan | 0 |
