# Ned-Clean Analysis — W21 Project 12

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
- Human Issue #1 (returns in reverse order): missed
- Human Issue #2 (negative autocorrelation at lag 1): missed
- Human Issue #3 (initial simulation at MLE): missed
- Human Issue #4 (routine analysis, extend scope): missed
- Human Issue #5 (follows previous projects): missed
- Human Issue #6 (trial simulation implausible): covered (matched by finding: "Filtering for simulated data adds little value — simulated data much more volatile than actual returns")
- Human Issue #7 (diagnostic plots/convergence): covered (matched by finding: "No MIF2 convergence diagnostics shown")

**Findings classification:**
- Finding #1 — mu_h outside search box: A — estimated mu_h far outside the specified search box; convergence not achieved
- Finding #2 — No MIF2 convergence diagnostics: B — no trace plots for log-likelihood or parameters across iterations (matches Human Issue #7)
- Finding #3 — No likelihood evaluation for pf1: A — simulated data particle filter result (L.pf1) not shown
- Finding #4 — Global search from if1[[1]]: A — global search inherits cooling schedule from local result rather than fresh start
- Finding #5 — Inconsistent dmrt vs dmean_z: A — two different demeaned return series used across model sections without explanation
- Finding #6 — frequency=365 incorrect: A — ts object constructed with frequency=365 for trading-day data (~252 per year)
- Finding #7 — phi discrepancy 0.95 vs 0.995: A — text describes phi=0.95 but code sets phi=0.995 in params_test
- Finding #8 — No parameter interpretation: C — POMP parameter estimates reported but never interpreted financially
- Finding #9 — AIC comparison potentially non-comparable: C — ARMA, GARCH, and POMP AICs compared without verifying same normalization convention
- Finding #10 — No likelihood profile/CI: C — only point estimates reported, no profile likelihoods or confidence intervals
- Finding #11 — Filtering for simulated data adds little: D — L.pf1 never shown, no re-estimation from simulated data; section notes simulated data much more volatile than actual returns (matches Human Issue #6)
- Finding #12 — ARMA model selection inconsistent: C — AIC table favors ARMA(4,5) by ~34 units but ARMA(3,1) chosen without showing MA roots numerically
- Finding #13 — Nasdaq-500 naming error: C — conclusion and references incorrectly call the index "Nasdaq-500"
- Finding #14 — Hard-coded unexplained date: C — doy set to 2016-11-04 in data-cleaning code but data starts April 2016; discrepancy unexplained
- Finding #15 — Breto citation incomplete: C — reference [2] points to course lecture notes, not the Breto (2014) journal paper

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1 (returns in reverse order): missed
- Human Issue #2 (negative autocorrelation at lag 1): missed
- Human Issue #3 (initial simulation at MLE): covered (matched by finding: "Filtering for simulated data inconclusive — simulated data much more volatile, should revise model or initial parameters")
- Human Issue #4 (routine analysis, extend scope): missed
- Human Issue #5 (follows previous projects): missed
- Human Issue #6 (trial simulation implausible): covered (matched by finding: "Filtering for simulated data inconclusive — simulated data much more volatile")
- Human Issue #7 (diagnostic plots/convergence): covered (matched by finding: "Missing convergence diagnostics for iterated filtering")

**Findings classification:**
- Finding 1 — Invalid AIC comparison (GARCH normalization): A — tseries GARCH log-likelihood uses non-standard normalization; cross-model AIC comparison invalid
- Finding 2 — Missing convergence diagnostics: B — no trace plots for MIF2 log-likelihood or parameters across iterations (matches Human Issue #7)
- Finding 3 — No profile likelihoods: A — no profile likelihoods or confidence intervals computed for any parameter
- Finding 4 — Global search from single local result (if1[[1]]): A — cooling schedule inherited from local search, defeating purpose of global search
- Finding 5 — Filtering for simulated data inconclusive: B — section reports very low likelihood with no diagnosis, and simulated data is much more volatile than actual returns, suggesting model misspecification; no structural revision follows (matches Human Issues #3 and #6)
- Finding 6 — Np=2000 below course standard: C — course standard for run_level=3 is Np=5000; choice not justified
- Finding 7 — No benchmark comparison on POMP likelihood scale: C — no IID or simple AR model baseline computed on particle-filter likelihood scale
- Finding 8 — No model diagnostics beyond visual residuals: C — no conditional log-likelihoods, no ESS monitoring, no filtering-distribution simulation comparison
- Finding 9 — Nasdaq-500 error: C — conclusion consistently calls index "Nasdaq-500"
- Finding 10 — Breto (2014) not cited: C — reference [2] points to course notes, not Breto (2014) journal paper
- Finding 11 — Pairs plot threshold not justified: C — logLik > max-30 threshold is much wider than Wilks 95% set; distinction not noted
- Finding 12 — Nreps_local=20 below course standard: C — course standard for run_level=3 is 40 replicates
- Finding 13 — No parameter interpretation: C — estimated parameters not compared to published stochastic volatility estimates
- Finding 14 — Causal/predictive language unsupported: C — conclusion claims model is "appropriate" based only on in-sample AIC with no out-of-sample validation
- Finding 15 — Missing sessionInfo: C — package versions not recorded; results may not reproduce on current CRAN releases

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 10 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

Note: Finding 5 (Major) covers two human issues (#3 and #6); B count reflects human issues covered by Major findings.

---

## Doug

**Coverage record:**
- Human Issue #1 (returns in reverse order): missed
- Human Issue #2 (negative autocorrelation at lag 1): missed
- Human Issue #3 (initial simulation at MLE): covered (matched by finding: "Missing forward simulation from best-fit parameters")
- Human Issue #4 (routine analysis, extend scope): missed
- Human Issue #5 (follows previous projects): missed
- Human Issue #6 (trial simulation implausible): covered (matched by finding: "Simulated-data particle filter result presented as real-data benchmark")
- Human Issue #7 (diagnostic plots/convergence): covered (matched by finding: "No convergence diagnostics presented")

**Findings classification:**
- Major 1 — Invalid AIC comparison across likelihood scales: A — ARMA, GARCH, and POMP AICs compared without verifying same normalization; Monte Carlo variance in POMP likelihood not quantified
- Major 2 — AIC from median vs maximum logLik: A — per-chain logLik estimates noisy; max() selects chain with largest MC noise realization, creating optimistic bias
- Major 3 — Global IF2 search from previous mif2 object: A — cooling schedule inherited from local search if1[[1]] rather than fresh start from ndx.filt
- Major 4 — Simulated-data pfilter as real-data benchmark: B — simulated data much more volatile than actual returns; section misrepresents this as baseline for real-data fit (matches Human Issue #6)
- Major 5 — No convergence diagnostics: B — no trace plots for log-likelihood or parameters across IF2 iterations (matches Human Issue #7)
- Major 6 — No profile likelihoods/CI: A — no profile likelihoods or confidence intervals; pairs plot is not a substitute
- Major 7 — No non-mechanistic benchmark comparison: A — GARCH is not a non-mechanistic baseline; no IID or EGARCH model provided
- Major 8 — Erroneous claim of POMP improvement over GARCH: A — 109-unit AIC difference claimed without accounting for Monte Carlo variance in POMP likelihood
- Minor — Inconsistent index name (Nasdaq-500): C — conclusion uses "Nasdaq-500" three times
- Minor — Parameter initialization discrepancy (phi 0.95 vs 0.995): C — text and code inconsistent on phi value
- Minor — mu_h not transformed, G_0/H_0 unconstrained: C — potential for optimizer to drift outside search box for G_0 and H_0
- Minor — No ESS monitoring: C — effective sample size not reported; particle degeneracy during COVID-19 period not assessed
- Minor — rproc2.sim vs rproc2.filt not explained: C — split between simulation and filter process not explained for readers unfamiliar with the template
- Minor — Global search box from pairs plot alone: C — only 20 local replicates used to construct box; phi box (0.95, 0.99) may be too narrow
- Minor — No sessionInfo: C — package versions not documented; reproducibility at risk
- Minor — Missing forward simulation from best-fit parameters: D — simulation section uses test parameters not MLE; no post-fit simulation comparison shown (matches Human Issue #3)
- Minor — No financial interpretability of estimated parameters: C — estimated parameters not interpreted or compared to published stochastic volatility literature

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1 (returns in reverse order): missed
- Human Issue #2 (negative autocorrelation at lag 1): missed
- Human Issue #3 (initial simulation at MLE): missed
- Human Issue #4 (routine analysis, extend scope): missed
- Human Issue #5 (follows previous projects): missed
- Human Issue #6 (trial simulation implausible): covered (matched by finding: "Simulated data pfilter result not reported — numerical value not shown, simulation check uninformative")
- Human Issue #7 (diagnostic plots/convergence): covered (matched by finding: "Missing IF2 convergence diagnostics")

**Findings classification:**
- ID 21.12.7 — Missing IF2 convergence diagnostics: B — no trace plots for log-likelihood or parameter values across IF2 iterations (matches Human Issue #7)
- ID 21.12.8 — No profile likelihoods/CI: A — no profile likelihoods or confidence intervals; point estimates only; pairs plot is not a substitute
- ID 21.12.6 — No ESS monitoring: C — effective sample size not reported; particle degeneracy during COVID-19 period not assessed
- ID 21.12.5 — Simulated data pfilter not reported: D — text states "log likelihood seems to be very low" for initial parameters on simulated data but L.pf1 not printed; simulation check uninformative without baseline value (matches Human Issue #6)
- ID 21.12.1 revised — AIC comparison lacks qualification: C — ARMA, GARCH, and POMP AICs compared without noting potential normalization differences; brief note recommended
- ID M1 — Normal measurement model for heavy-tailed returns: C — Gaussian measurement model inappropriate given heavy-tailed residuals; Student-t extension noted as standard in financial SV literature
- ID M2 — Conclusion overstates model adequacy: C — "appropriate for Nasdaq-500 data" too strong given unverified convergence, unassessed identifiability, and unaddressed tail issues
- ID 21.12.4 — Extreme sigma_eta values in pairs plot: C — some IF2 replicates produce sigma_eta near ~300; outlier runs not commented on; may indicate numerical issues
- ID 21.12.10 — Naming error (Nasdaq-500): C — conclusion refers to "Nasdaq-500" three times
- ID 21.12.11 — ACF figure ambiguity: C — Figure 5 labeled "Nasdaq-100 Index return" but appears in ARMA(3,1) residual diagnostics context; label ambiguous

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 1 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 3 | 6 | 1 |
| B (AI major, human also found) | 1 | 3 | 2 | 1 |
| C (AI minor, human missed) | 7 | 10 | 8 | 8 |
| D (AI minor, human also found) | 1 | 0 | 1 | 1 |
| E (Human found, AI missed) | 5 | 4 | 4 | 5 |

---

## Per-Reviewer Metrics

Human Recall = (B + D) / (B + D + E)
AI-Unique Rate = (A + C) / (A + B + C + D)

| Reviewer | B | D | E | Human Recall | A | C | AI-Unique Rate |
|----------|--:|--:|--:|-------------:|--:|--:|---------------:|
| Alex | 1 | 1 | 5 | 2/7 = 28.6% | 6 | 7 | 13/15 = 86.7% |
| Charlie | 3 | 0 | 4 | 3/7 = 42.9% | 3 | 10 | 13/16 = 81.3% |
| Doug | 2 | 1 | 4 | 3/7 = 42.9% | 6 | 8 | 14/17 = 82.4% |
| Evan | 1 | 1 | 5 | 2/7 = 28.6% | 1 | 8 | 9/11 = 81.8% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: The returns are shown in reverse order in the EDA section. The ARMA model also fits them in reverse order.
- Human Issue #2: The returns show substantial negative autocorrelation at lag 1, which is somewhat surprising. Is this due to a few outliers? Or is it a robust finding?
- Human Issue #4: This is a fairly routine analysis; could be extended to ask better questions — about alternative models, pandemic financial shocks, etc.
- Human Issue #5: Follows many previous 531 final projects, finds similar conclusions. One could target a more specific question.

Count: 4 out of 7 human issues (57.1%) were missed by all four reviewers.

### Unique finds per reviewer

Human issues that only one reviewer covered and all others missed:

- Alex: HI#6 (trial simulation implausible) — Alex covers via finding #11 (Minor); Charlie, Doug, and Evan also cover HI#6, so Alex has no unique finds on this issue. Let me reconsider...

Rechecking who covers each human issue:
- HI#3 (initial simulation at MLE): Charlie (B via #5), Doug (D via Minor "Missing forward simulation") — Alex and Evan miss it.
- HI#6 (trial simulation implausible): Alex (D via #11), Charlie (B via #5), Doug (B via Major #4), Evan (D via #5) — all four cover it.
- HI#7 (diagnostic plots/convergence): Alex (B via #2), Charlie (B via #2), Doug (B via Major #5), Evan (B via ID 21.12.7) — all four cover it.

Human issues covered by exactly one reviewer:
- HI#3 is covered by Charlie and Doug but not Alex and Evan. Not unique to one reviewer.
- HI#6 is covered by all four.
- HI#7 is covered by all four.

No human issue was covered by exactly one reviewer.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |

### Universal AI-only flags

Issues raised by every reviewer that the human did not mention:

Checking for AI findings raised by all four reviewers that are classified A or C (human missed):

- No convergence diagnostics / MIF2 trace plots: All four raise this — but it DOES match HI#7, so it is not AI-only.
- No profile likelihoods/CI: Alex (C #10), Charlie (A #3), Doug (A #6), Evan (A ID 21.12.8) — all four raise this. Human did not raise it. Universal AI-only flag.
- Global search initialized from previous mif2 result (if1[[1]]): Alex (A #4), Charlie (A #4), Doug (A #3) raise it. Evan does NOT raise it explicitly. Not universal.
- Invalid AIC comparison across model families: Alex (C #9), Charlie (A #1), Doug (A #1), Evan (C ID 21.12.1) — all four raise this. Human did not raise it. Universal AI-only flag.
- Nasdaq-500 naming error: Alex (C #13), Charlie (C #9), Doug (C Minor), Evan (C ID 21.12.10) — all four raise this. Human did not raise it. Universal AI-only flag.
- No parameter interpretation / financial interpretability: Alex (C #8), Charlie (C #13), Doug (C Minor), Evan (C ID M2 — partially) — all four raise this. Human did not raise it. Universal AI-only flag.

Universal AI-only flags (raised by all four reviewers, human missed):
1. No profile likelihoods or confidence intervals for POMP parameters
2. Invalid/unverified cross-model AIC comparison (ARMA, GARCH, POMP on different or unverified likelihood scales)
3. "Nasdaq-500" naming error in conclusion
4. No financial interpretation of estimated POMP parameters

Count: 4 universal AI-only flags.
