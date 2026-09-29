# Comparator Analysis — W24 Project 15

---

## Human Issues

1. It is okay to use data from Kaggle, but the description of datasets on Kaggle can be limited. It is better to identify an original source with a complete description.

2. For highly peaked count data, consider plotting on a log(x+1) scale.

3. Linear models and autocorrelation analysis may also be better applied on a log scale in such cases.

4. The seasonality plot is a good way to infer absence of a clear seasonality.

5. The likelihood ratio test is used to compare two models, where one is a nested version of the other. It is not correct to use the LRT to compare an ARMA and POMP model in this context.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "ARMA Applied to Count Data Without Addressing Non-Negativity — log transformation suggested as more appropriate")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Likelihood Ratio Test Between Non-Nested Models Is Invalid")

**Findings classification:**
- Finding 1 (dmeasure/rmeasure inconsistency): A — measurement model density does not account for factor-of-4 scaling in rmeasure
- Finding 2 (C accumulates wrong quantity): A — accumulator C increments camel recoveries instead of spillover events
- Finding 3 (LRT non-nested models): B — LRT applied to non-nested ARMA and SEIRS models; Wilks approximation does not apply (matches Human Issue #5)
- Finding 4 (profile likelihood truncated at boundary): A — profile maximum lies on the boundary of the searched interval; CI is invalid
- Finding 5 (global search convergence): A — global search uses only one additional MIF2 run without cooling restart
- Finding 6 (weak identifiability dismissed): A — non-convergence of initial condition parameters dismissed without further investigation
- Finding 7 (no profile for beta/R0/mu_RS): A — key epidemiological parameters have no uncertainty quantification
- Finding 8 (mu_RS omitted from profile random walk): C — optimizer cannot re-optimize mu_RS while profiling rho_CH
- Finding 9 (ARMA on count data): D — log transformation or count-appropriate model recommended for non-negative integer process (matches Human Issue #3)
- Finding 10 (dN_Nmu draws from fixed N): C — birth process draws from fixed parameter N rather than compartment states, risking conservation violations
- Finding 11 (fmin truncation bias): C — clipping binomial draws with fmin creates biased transition rates
- Finding 12 (parameter count in LRT): C — ARMA degrees of freedom likely undercounted; affects chi-squared test
- Finding 13 (model.png missing): C — referenced model diagram file not present in submitted folder
- Finding 14 (spectral period dismissed): C — dominant 7-month period dismissed without examining biological plausibility
- Finding 15 (seed reproducibility): C — set.seed outside foreach in parallel block does not guarantee reproducibility

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Non-Gaussian ARMA residuals not addressed; log transform or Poisson/NB ARMA suggested for overdispersed count data")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "LRT applied to non-nested models — Wilks approximation invalid for ARMA vs. SEIRS comparison")

**Findings classification:**
- Major 1 (dmeas/rmeas factor-of-4 inconsistency): A — critical measurement model error invalidating all log-likelihoods
- Major 2 (profile likelihood MLE at boundary): A — rho_CH profile hits upper search boundary; CI is degenerate
- Major 3 (LRT on non-nested models): B — Wilks approximation misapplied to non-nested ARMA vs. SEIRS (matches Human Issue #5)
- Major 4 (mif2 internal log-likelihood used for ARMA comparison): A — mif2 trace log-likelihood is biased; should not be compared to ARMA benchmark
- Major 5 (no profile likelihoods for Beta, mu_IR, R0): A — key parameters lack profiles and CIs; R0 reported as point estimate only
- Major 6 (global search: no likelihood distribution shown): A — 400 starting points run but only best result reported; no histogram or scatter plot
- Minor: single pfilter without MC SE: C — preliminary check uses one run with no standard error reported
- Minor: Non-Gaussian ARMA residuals not addressed: D — log transform or NB ARMA suggested for overdispersed count data (matches Human Issue #3)
- Minor: rw.sd too small for rho_CH and eta2: C — perturbation scale may severely limit IF2 exploration
- Minor: fmin clamping may break population conservation: C — clamping can violate S+E+I+R=N without verification
- Minor: no filtering-distribution simulations: C — forward simulations only; filtering-conditioned trajectories absent
- Minor: no out-of-sample evaluation: C — no held-out data or forecast attempted
- Minor: R0 uncertainty (minor bullet): C — R0 = 2.6 reported without CI (reiterated from Major 5; listed separately in minor section)
- Minor: model.png missing from repository: C — broken image in rendered output
- Minor: CLUSTER.R referenced but absent: C — sourced file not in repository; purpose unclear
- Minor: conclusion overstates profile likelihood result: C — claims narrow CI despite boundary-hitting MLE (reiterated from Major 2)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Invalid LRT comparing ARMA and SEIRS models — non-nested, different observation models"; also matched by finding: "LRT df incorrect even ignoring non-comparability")

**Findings classification:**
- Major Issue 1 (Invalid LRT comparing ARMA and SEIRS): B — invalid likelihood ratio test comparing non-nested models evaluated under different observation models (matches Human Issue #5)
- Major Issue 2 (Accumulator variable tracks recoveries, not infections): A — C accumulates dN_IR rather than dN_EI, systematically misrepresenting the spillover process
- Major Issue 3 (Profile likelihood rho_CH drift): A — insufficient nprof and iterations render the profile curve and CI unreliable; CI reference maximum also drawn from wrong table
- Major Issue 4 (Global search initialized from prior mif2 object): A — inherited cooling schedule anchors global search near local solution
- Major Issue 5 (No convergence evidence for global search): A — no likelihood traces shown for global search; only two mif2 passes per replicate
- Major Issue 6 (dmeasure and rmeasure inconsistent scaling): A — dmeasure uses rho*C directly; rmeasure multiplies by 4, making likelihood and simulations inconsistent
- Major Issue 7 (LRT df incorrect): B — ARMA(1,4) parameter count misstated as 5 instead of 7, inflating LRT degrees of freedom (matches Human Issue #5)
- Minor: R_0 formula incorrect: C — uses Beta/mu_IR rather than the full SEIRS formula incorporating latent period survival
- Minor: Model diagram file missing: C — model.png referenced in text but not present; image does not render
- Minor: Fixed rho=1 not justified: C — near-complete surveillance assumed without citation or sensitivity analysis
- Minor: Profile CI reads from results not full parameter table: C — CI cutoff uses only profile search maximum, not global maximum
- Minor: Spectral analysis period calculation error: C — dimensional derivation of period formula is written incorrectly
- Minor: mu absent from rw.sd not acknowledged: C — camel birth/death rate fixed throughout but not noted in text
- Minor: Insufficient Np and Nmif: C — sensitivity of log-likelihoods to Np not assessed
- Minor: No model diagnostics beyond ESS: C — no conditional log-likelihood plot, filtering-distribution simulations, or residual diagnostics
- Minor: Pairs plot uses profile search results: C — global and profile scatter not compared

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Gaussian ARMA applied to skewed count data without flagging as limitation")
- Human Issue #4: missed
- Human Issue #5: covered (matched by findings: "Invalid likelihood ratio test comparing ARMA and SEIRS" and "Conclusion section overstates statistical evidence")

**Findings classification:**
- 24.15.1: B — Invalid likelihood ratio test comparing ARMA and SEIRS (matches Human Issue #5)
- 24.15.2: A — Profile likelihood for ρ_CH has maximum outside the evaluated range
- 24.15.3: A — No replicated pfilter evaluations; log-likelihoods presented as exact
- 24.15.4: A — IF2 non-convergence for mu_RS and rho_CH
- 24.15.5: A — Global search reveals extreme parameter dispersion
- 24.15.17: B — Conclusion section overstates statistical evidence based on invalid LRT (matches Human Issue #5)
- 24.15.6: C — R₀ = 2.6 reported without confidence interval or identifiability check
- 24.15.7: D — Gaussian ARMA applied to skewed count data without flagging as limitation (matches Human Issue #3)
- 24.15.8: C — Best-fit parameter vector from global search not shown
- 24.15.9: C — Same parameter η₂ used for initial E and I without sensitivity
- 24.15.18: C — The "4× multiplier" for total human cases is an external fixed assumption

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 6 | 5 | 5 | 4 |
| B (AI major, human also found) | 1 | 1 | 2 | 2 |
| C (AI minor, human missed) | 7 | 9 | 9 | 4 |
| D (AI minor, human also found) | 1 | 1 | 0 | 1 |
| E (Human found, AI missed) | 3 | 3 | 4 | 3 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 1 | 3 | 2/5 = 40% | 6 | 7 | 13/15 = 87% |
| Charlie | 1 | 1 | 3 | 2/5 = 40% | 5 | 9 | 14/16 = 88% |
| Doug | 2 | 0 | 4 | 1/5 = 20% | 5 | 9 | 14/16 = 88% |
| Evan | 2 | 1 | 3 | 2/5 = 40% | 4 | 4 | 8/11 = 73% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: It is okay to use data from Kaggle, but the description of datasets on Kaggle can be limited. It is better to identify an original source with a complete description. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: For highly peaked count data, consider plotting on a log(x+1) scale. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: The seasonality plot is a good way to infer absence of a clear seasonality. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 3 out of 5 human issues (60%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

(none)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 0 |
| Evan | 0 |
