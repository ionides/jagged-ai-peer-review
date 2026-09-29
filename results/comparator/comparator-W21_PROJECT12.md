# Comparator Analysis — W21 Project 12

---

## Human Issues

1. The returns are shown in reverse order in the EDA section. The ARMA model also fits them in reverse order.

2. The returns show substantial negative autocorrelation at lag 1, which is somewhat surprising (inconsistent with the efficient market hypothesis, GARCH models and stochastic volatility models). Is this due to a few outliers? Or is it a robust finding?

3. The initial simulation is much too variable to match the data, but that is just a consequence of the initial guess parameters. Better to present simulations at plausible parameter values, say the MLE.

4. This is a fairly routine analysis, carrying out standard GARCH, ARMA and POMP models and comparing model fit. Good to see, but could be extended to ask questions — about alternative models, or how well the pandemic financial shocks fit (or don't fit) the model assumptions, etc.

5. Follows many previous 531 final projects, and finds similar conclusions. One could target the analysis at a more specific question.

6. The trial simulation for the stochastic volatility model does not take plausible values, compared to the data. This may be fixed after likelihood maximization, but could use checking and discussing.

7. Did the authors look at diagnostic plots to investigate model specification and convergence issues?

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by findings: "mu_h lies outside search box — convergence not achieved" and "no MIF2 convergence diagnostics (trace plots) are shown")

**Findings classification:**
- Finding 1 (mu_h outside search box): B — MIF2 convergence failure identified through parameter estimates lying outside the search region (matches Human Issue #7)
- Finding 2 (no MIF2 trace plots): B — no convergence diagnostic plots shown for iterated filtering (matches Human Issue #7)
- Finding 3 (no pf1 likelihood reported): A — likelihood evaluation for simulated data never displayed, making simulation study uninformative
- Finding 4 (global search inherits cooled if1[[1]]): A — global search uses a locally-warmed MIF2 chain, defeating the purpose of global search
- Finding 5 (inconsistent dmrt vs dmean_z): A — two distinct demeaned return series used across model sections without explanation
- Finding 6 (frequency=365 on trading-day data): A — ts object constructed with incorrect annual frequency for trading-day data
- Finding 7 (phi=0.95 in text vs phi=0.995 in code): A — discrepancy between stated initial parameters in text and actual code values
- Finding 8 (no parameter interpretation): C — estimated POMP parameters reported but never interpreted in financial terms
- Finding 9 (AIC comparison potentially non-comparable): C — ARMA, GARCH, and POMP likelihoods may not be evaluated on the same conditional density
- Finding 10 (no likelihood profile or CIs): C — only a single point estimate reported; no profile likelihood or confidence intervals for any POMP parameter
- Finding 11 (simulation subsection adds little value): C — filtering on simulated data never shows L.pf1 and performs no re-estimation
- Finding 12 (ARMA model selection inconsistency): C — ARMA(3,1) chosen despite a ~34-unit AIC gap from ARMA(4,5), without showing MA root values numerically
- Finding 13 (Nasdaq-500 misnomer): C — index repeatedly and incorrectly called "Nasdaq-500" in conclusion and references
- Finding 14 (hard-coded unexplained date in data cleaning): C — strftime date 2016-11-04 used in ts construction differs from actual data start with no explanation
- Finding 15 (incomplete Breto citation): C — model attributed to "Breto (2014)" but reference [2] points to course lecture notes, not the original journal paper

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Filtering for simulated data is inconclusive and undiagnosed — simulated data much more volatile than actual data, initial parameter miscalibration noted")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Filtering for simulated data is inconclusive and undiagnosed — simulated data much more volatile than actual data, initial parameter miscalibration noted")
- Human Issue #7: covered (matched by findings: "Missing convergence diagnostics for iterated filtering" and "No model diagnostics beyond visual residuals")

**Findings classification:**
- Finding 1 (Invalid cross-model AIC comparison): A — GARCH likelihood normalization not verified before comparing AIC across models
- Finding 2 (Missing convergence diagnostics): B — no trace plots or convergence evidence for mif2 (matches Human Issue #7)
- Finding 3 (No profile likelihoods): A — profile likelihoods absent for all six parameters
- Finding 4 (Global search initialized from local search result): A — each global replicate inherits state from if1[[1]] rather than a fresh pomp object
- Finding 5 (Filtering for simulated data inconclusive and undiagnosed): B — simulated data much more volatile than actual data; initial parameter miscalibration unaddressed (matches Human Issues #3 and #6)
- Finding 6 (Np = 2000 below course standard): C — run_level 3 uses 2000 particles vs. course standard of 5000
- Finding 7 (No benchmark comparison on POMP likelihood scale): C — no IID or simple AR benchmark on particle-filter likelihood scale
- Finding 8 (No model diagnostics beyond visual residuals): D — no conditional log-likelihoods, no ESS monitoring, no period-specific diagnostics (matches Human Issue #7)
- Finding 9 (Nasdaq-500 error throughout conclusion): C — index name is factually incorrect in conclusion and references
- Finding 10 (Breto 2014 not cited as primary reference): C — model equations taken from Breto (2014) but that paper absent from reference list
- Finding 11 (Pairs plot threshold not justified): C — logLik > max - 30 threshold not explained or distinguished from formal confidence set
- Finding 12 (Nreps_local = 20 below course standard): C — run_level 3 uses 20 local replicates vs. course standard of 40
- Finding 13 (No discussion of parameter interpretation): C — estimated parameters not compared to published estimates or assessed for plausibility
- Finding 14 (Causal/predictive language unsupported): C — conclusion claims model is "appropriate" based only on in-sample AIC
- Finding 15 (Missing sessionInfo): C — package versions not reported despite version-sensitive pomp API

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Missing forward simulation from best-fit parameters — initial simulation uses test params and is much more volatile than data; no post-fit simulation shown")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Missing forward simulation from best-fit parameters — initial simulation uses test params and is much more volatile than data; no post-fit simulation shown")
- Human Issue #7: covered (matched by findings: "No convergence diagnostics presented" and "No ESS monitoring reported")

**Findings classification:**
- Major Issue 1 (Invalid cross-model AIC comparison): A — AIC comparison across ARMA, GARCH, and POMP is invalid due to different likelihood scales and Monte Carlo noise
- Major Issue 2 (AIC from noisy max log-likelihood): A — per-chain log-likelihood uses only 20 PF replicates; max() selects chain with largest Monte Carlo noise, biasing AIC
- Major Issue 3 (Global IF2 initialized from previous mif2 result): A — global search passes if1[[1]] as first argument, inheriting decayed cooling schedule instead of starting fresh
- Major Issue 4 (Simulated-data PF result presented as real-data benchmark): A — particle filter on simulated data (sim1.filt) misleadingly compared to real-data fit
- Major Issue 5 (No convergence diagnostics): B — no log-likelihood vs. iteration or parameter trace plots for local or global IF2 searches (matches Human Issue #7)
- Major Issue 6 (No profile likelihoods or CIs): A — no profile likelihoods computed for any parameter; identifiability unassessed
- Major Issue 7 (No non-mechanistic benchmark comparison): A — ARMA and GARCH are not true non-mechanistic baselines; no formal LRT or uncertainty-aware AIC comparison
- Major Issue 8 (Erroneous POMP superiority claim): A — POMP AIC advantage of ~109 units reported without log-likelihood SE or acknowledgment of Monte Carlo variance
- Minor: Inconsistent index name (Nasdaq-100 vs Nasdaq-500): C — conclusion section refers to "Nasdaq-500" three times; straightforward factual error
- Minor: Parameter initialization discrepancy: C — text states phi=0.95 but code sets phi=0.995
- Minor: mu_h/G_0/H_0 partrans: C — G_0 and H_0 left untransformed; optimizer may drift outside search box bounds
- Minor: No ESS monitoring: D — ESS not reported or plotted for any particle filter run (matches Human Issue #7)
- Minor: rproc2.sim vs rproc2.filt not explained: C — split between simulation and filter process snippets is unexplained
- Minor: Global search box constructed from local-search pairs plot alone: C — only 20 local replicates; phi box (0.95, 0.99) may be too narrow
- Minor: No sessionInfo() or package version documentation: C — package versions not recorded; reproducibility at risk
- Minor: Missing forward simulation from best-fit parameters: D — no simulation from fitted MLE shown; initial simulation acknowledges over-volatility but no post-fit comparison provided (matches Human Issues #3 and #6)
- Minor: No financial interpretability of estimated parameters: C — claims parameters are "easier to interpret" but provides no interpretation of specific MLE values

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 4 |
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
- Human Issue #7: covered (matched by finding: "Missing IF2 convergence diagnostics — no trace plots to verify convergence")

**Findings classification:**
- ID 21.12.7: B — Missing IF2 convergence diagnostics; no trace plots of log-likelihood or parameter values vs. iteration (matches Human Issue #7)
- ID 21.12.8: A — No profile likelihoods or confidence intervals reported for POMP parameters
- ID 21.12.6: C — No ESS monitoring reported during particle filtering
- ID 21.12.5: C — Simulated data pfilter log-likelihood noted as very low but numerical value from L.pf1 not printed
- ID 21.12.1: C — AIC comparison across ARMA, GARCH, and POMP model classes lacks qualification about same-scale computation
- ID M1: C — Gaussian measurement model used despite heavy-tailed returns; Student-t not considered
- ID M2: C — Conclusion overstates model adequacy given unverified convergence and unassessed identifiability
- ID 21.12.4: C — Extreme sigma_eta values in pairs plot from some IF2 replicates are not commented on
- ID 21.12.10: C — Conclusion refers to "Nasdaq-500" three times; correct index is Nasdaq-100
- ID 21.12.11: C — ACF figure labeled "Nasdaq-100 Index return" but appears in ARMA residual diagnostics context; ambiguous whether raw returns or residuals

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 1 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 3 | 7 | 1 |
| B (AI major, human also found) | 2 | 2 | 1 | 1 |
| C (AI minor, human missed) | 8 | 9 | 7 | 8 |
| D (AI minor, human also found) | 0 | 1 | 2 | 0 |
| E (Human found, AI missed) | 6 | 4 | 4 | 6 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 2 | 0 | 6 | 1/7 = 14% | 5 | 8 | 13/15 = 87% |
| Charlie | 2 | 1 | 4 | 3/7 = 43% | 3 | 9 | 12/15 = 80% |
| Doug | 1 | 2 | 4 | 3/7 = 43% | 7 | 7 | 14/17 = 82% |
| Evan | 1 | 0 | 6 | 1/7 = 14% | 1 | 8 | 9/10 = 90% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: The returns are shown in reverse order in the EDA section. The ARMA model also fits them in reverse order. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: The returns show substantial negative autocorrelation at lag 1, which is somewhat surprising (inconsistent with the efficient market hypothesis, GARCH models and stochastic volatility models). Is this due to a few outliers? Or is it a robust finding? (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: This is a fairly routine analysis, carrying out standard GARCH, ARMA and POMP models and comparing model fit. Good to see, but could be extended to ask questions — about alternative models, or how well the pandemic financial shocks fit (or don't fit) the model assumptions, etc. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: Follows many previous 531 final projects, and finds similar conclusions. One could target the analysis at a more specific question. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 4 out of 7 human issues (57%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
