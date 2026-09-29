# Comparator Analysis — W24 Project 04

---

## Human Issues

1. The introduction promises an investigation of four different regions, but results are only shown for data from one. Simulation results are carried out for three cities. These simulations are discussed as if they were data, which is confusing.

2. The simulations for California, Washington and New York are rather similar. They all have the same population, the same in initial conditions, the same feature that the susceptible fraction jumps straight back to 800,000 after an epidemic. It is unclear, even from the code, what is being plotted and why the curves modeling these three cities are similar but different.

3. Showing simulation results as EDA is unexpected. Better for EDA to focus on data.

4. "QQ plot shows good performance" is unclear, but it should be noted that the QQ plot shows long tails.

5. The fitted values plot shows 1-step predictions, which is not very informative.

6. The code for fitting arima models is derived from the `arima2` package but in fact uses `stats::arima`. It is unclear if that is intentional.

7. Readers attempting to reproduce the numerical results found that the code failed to run.

8. The authors say they use a software package called `GenSA`. This package is not explained. The fitting criterion seems to be least squares, leading to a fit which is essentially constant at zero. This is not very informative. Maximum likelihood, with a plausible measurement model, would be much better - and was the approach taught in class.

9. This SEIR model can only fit one peak, whereas the actual pandemic had multiple waves. The report described this as a "commendable" explanation of the data, which is misleading.

10. Various projects from past years do a better job of explaining COVID-19 dynamics. One of these is cited in the project.

11. The authors plug a single simulation into least squares and optimize that function to an optizer. That does not correspond to maximum likelihood estimation. Methods to evaluate and optimize the likelihood were taught in class, and should be used. Overall, the project does not demonstrate mastery of the ideas or methods for likelihood-based inference discussed in the second half of the course.

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "EDA SIR simulations have no connection to main analysis — simulation-only exercises presented as EDA, not genuine data examination")
- Human Issue #2: covered (matched by finding: "EDA SIR simulations have no connection to main analysis — identical arbitrarily chosen parameters used for all three states")
- Human Issue #3: covered (matched by finding: "EDA SIR simulations have no connection to main analysis — genuine EDA should examine raw time series, not forward-simulate a mis-parameterized model")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "optimization done by minimizing SSE, not maximizing likelihood — standard POMP inference never performed")
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by findings: "optimization done by minimizing SSE, not maximizing likelihood" and "final SEIR model parameters chosen by manual hand-tuning with no justification")

**Findings classification:**
- Finding 1 (wrong negative binomial parameterization): A — dmeas coded with I as size and rho as prob, wrong NB parameterization, no dispersion parameter
- Finding 2 (SSE optimization, not likelihood): B — optimization minimizes sum of squared errors over a single simulation, never uses pfilter/mif2/likelihood (matches Human Issues #8 and #11)
- Finding 3 (hand-tuned final SEIR parameters): B — after failed optimization, authors manually assign beta=0.35 etc. with no criterion or justification (matches Human Issue #11)
- Finding 4 (incorrect rmeas in global search): A — rmeasure overwritten to deterministic cases = nearbyint(I), inconsistent with stated NB model
- Finding 5 (EDA SIR simulations disconnected from analysis): B — three-state SIR simulations with identical arbitrary parameters presented as EDA instead of examining raw data (matches Human Issues #1, #2, and #3)
- Finding 6 (double-differencing in data preprocessing): A — weekly grouping sums cumulative counts then differences, may not yield correct weekly incidence
- Finding 7 (no formal ARIMA vs SEIR comparison): A — no log-likelihoods, AIC, or statistical test; comparative research question never formally addressed
- Finding 8 (ARIMA model selection inconsistency): A — AIC selects ARIMA(2,1,3) but ARIMA(3,1,1) used for all diagnostics and fitted values
- Finding 9 (N treated as free variable, exceeds WA population): C — global search returns N=8,830,174 exceeding actual ~7.7M population with no comment
- Finding 10 (no confidence intervals or uncertainty quantification): C — neither ARIMA nor SEIR section presents any uncertainty estimates
- Finding 11 (claimed 1500 data points vs ~160 weekly rows): C — introduction states 1500 data points but week.csv contains ~160 weekly aggregates
- Finding 12 (main.R is unmodified measles SIR example): C — submitted main.R is standard course code for Consett measles data, unrelated to project
- Finding 13 (time axis labels say "Day" but model uses weekly units): C — plot axes labeled "Day" while time variable represents weeks
- Finding 14 (time-varying beta described but not implemented): C — model description states beta switches values mid-period but code uses constant beta throughout
- Finding 15 (ChatGPT reference insufficient): C — cites ChatGPT for "code optimization and error correction" without specifying what was generated or verified

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "EDA SIR plots labeled as 'SEIR' — three-city simulations in EDA introduced as if part of SEIR analysis, connection between simulations and data not explained")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "EDA SIR plots labeled as 'SEIR' — three-city simulations in EDA introduced as if part of SEIR analysis, connection between simulations and data not explained")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "Major Issue 1 — ad hoc SSE calibration via GenSA/optim instead of likelihood-based inference; SSE on a single simulation is both statistically incorrect and noisy; MIF2/pfilter should be used")
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: "Major Issue 1 — ad hoc SSE calibration via GenSA/optim instead of likelihood-based inference; SSE on a single simulation is both statistically incorrect and noisy; MIF2/pfilter should be used")

**Findings classification:**
- Major Issue 1 (SSE calibration instead of likelihood): B — ad hoc SSE minimization via GenSA/optim on a single stochastic simulation instead of likelihood-based inference; pfilter/mif2 never called (matches Human Issues #8 and #11)
- Major Issue 2 (incorrect dnbinom parameterization): A — dnbinom(cases, I, rho) sets size=I (time-varying state), not a fixed overdispersion parameter; pathological likelihood behavior
- Major Issue 3 (prevalence vs incidence conflation): A — measurement model conditions on I (prevalence stock) but data are weekly new cases (incidence flow); accumulator variable needed
- Major Issue 4 (ARIMA code contradicts AIC selection): A — AIC selects ARIMA(2,1,3) but code fits ARIMA(3,1,1); all diagnostics apply to wrong model
- Major Issue 5 (no quantitative goodness-of-fit for SEIR): A — no log-likelihood, AIC, or any quantitative fit measure reported for SEIR model; comparison with ARIMA cannot be answered
- Major Issue 6 (no convergence diagnostics): A — no replicated searches, no likelihood traces; SSE trace plots do not indicate likelihood convergence
- Major Issue 7 (no parameter identifiability or uncertainty): A — no profile likelihoods, no confidence intervals for any SEIR parameter
- Major Issue 8 (no quantitative ARIMA vs SEIR comparison): A — central research question answered only by visual inspection; no log-likelihood or AIC comparison
- Minor: title mismatch (SEIR vs SIR in EDA): C — title says SEIR but EDA section implements SIR+H model
- Minor: hand-tuned final parameters: C — final SEIR parameters manually chosen, not derived from optimization, with no explanation
- Minor: population N unjustified: C — N=5,000,000 used without justification; local and global searches recover very different values
- Minor: ChatGPT cited as numbered reference: C — AI tool listed as a literature reference rather than in acknowledgments
- Minor: rmeasure inconsistency across sections: C — local search uses rbinom(I, rho), global search uses nearbyint(I); two different simulation models without explanation
- Minor: residual spike around 2022 not investigated: C — text notes spike but offers no analysis of Omicron wave or structural break
- Minor: EDA SIR plots labeled as "SEIR": D — three-city simulation plots (CA, WA, NY) introduced in EDA as if part of SEIR analysis; connection between EDA simulations and data not explained (matches Human Issues #1 and #3)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Model title mismatch: paper claims SEIR but EDA implements SIR — creates confusion about what the EDA is actually demonstrating")
- Human Issue #2: covered (matched by finding: "EDA SIR models use identical hard-coded parameters regardless of region")
- Human Issue #3: covered (matched by finding: "EDA SIR models use unestimated, ad hoc parameters — presence as EDA is misleading")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Reproducibility failures — primary dataset 2.csv not included, code cannot be verified")
- Human Issue #8: covered (matched by finding: "Ad hoc calibration via SSE/single simulation instead of likelihood-based inference")
- Human Issue #9: covered (matched by finding: "No quantitative goodness-of-fit metrics — 'both models performed commendably' claim is unsupported")
- Human Issue #10: missed
- Human Issue #11: covered (matched by findings: "Ad hoc calibration instead of likelihood-based inference"; "Final model parameters chosen by manual inspection, not systematic optimization"; "Stochastic optimization cost function — nsim=1 SSE is unreliable and non-deterministic")

**Findings classification:**
- Finding 1 (Ad hoc calibration instead of likelihood-based inference): B — SSE/single-simulation fitting instead of particle-filter MLE (matches Human Issues #8 and #11)
- Finding 2 (No quantitative goodness-of-fit metrics for SEIR): B — "commendably" claim unsupported without log-likelihood or AIC (matches Human Issue #9)
- Finding 3 (Critical measurement model mis-specification — dnbinom/rbinom mismatch): A — dmeasure/rmeasure distributional inconsistency not raised by human
- Finding 4 (Comparison between ARIMA and SEIR not on a common metric): A — no shared evaluation framework; human did not raise this specific claim
- Finding 5 (No parameter identifiability assessment or uncertainty quantification): A — profile likelihoods and confidence intervals absent; not raised by human
- Finding 6 (Convergence evidence absent, optimization approach unreliable): A — single Nelder-Mead run, no convergence traces; not raised by human
- Finding 7 (Final model parameters chosen by manual inspection, not optimization): B — eyeball-fitted parameters not statistically principled (matches Human Issue #11)
- Finding 8 (Data preprocessing introduces double-differencing, nonsensical values): A — SEIR fitted to first difference of weekly counts; not raised by human
- Finding 9 (EDA SIR models use unestimated, ad hoc parameters): B — identical hard-coded parameters for all three regions, no fitting performed (matches Human Issues #2 and #3)
- Finding 10 (Model title mismatch — SEIR claimed but EDA implements SIR): B — confusion about what EDA demonstrates (matches Human Issue #1)
- Finding 11 (No model diagnostics — no ESS, no pfilter diagnostics): A — absence of particle filter diagnostics; not raised by human
- Finding 12 (Stochastic optimization cost function unreliable): B — nsim=1 SSE objective is non-deterministic; single simulation plugged into least squares (matches Human Issue #11)
- Finding 13 (ARIMA model selection inconsistency — ARIMA(2,1,3) selected but ARIMA(3,1,1) diagnosed): A — model-order mismatch between selection and diagnostics; not raised by human
- Finding 14 (Population parameter N treated as free optimization variable): A — biologically implausible N values not discussed; not raised by human
- Finding 15 (Reproducibility and code quality issues): B — primary dataset missing, code cannot be run from scratch (matches Human Issue #7)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 7 |
| C (AI minor, human missed) | 0 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "24.04.4 — EDA section presents forward simulations, not data exploration; simulations discussed as if data")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "24.04.4 — EDA section presents forward simulations, not data exploration")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by findings: "24.04.1 — SEIR uses least-squares not likelihood"; "24.04.3 — optimization fails, near-zero params and flat prediction"; "24.04.5 — measurement model undefined")
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by findings: "24.04.1 — SEIR uses least-squares not likelihood"; "24.04.2 — no quantitative goodness-of-fit metric for SEIR model")

**Findings classification:**
- 24.04.1: B — SEIR model fitted without likelihood-based inference; uses least-squares cost function, no pfilter (matches Human Issues #8 and #11)
- 24.04.2: B — no quantitative goodness-of-fit metric for SEIR model; conclusion unverifiable (matches Human Issue #11)
- 24.04.3: B — optimization appears to fail; near-zero parameters and essentially flat prediction are internally inconsistent (matches Human Issue #8)
- 24.04.4: B — EDA section presents forward simulations rather than observed data; simulations treated as if they were data (matches Human Issues #1 and #3)
- 24.04.5: B — measurement model undefined; rho has no statistical meaning without a specified observation distribution (matches Human Issue #8)
- 24.04.6: A — ARIMA fitted to raw, non-transformed highly skewed counts; violates constant-variance assumption
- 24.04.m1: C — b1/b2 time-varying beta described but optimization reports a single beta; inconsistency unresolved
- 24.04.m2: C — initial conditions S(0), E(0), I(0), R(0) never stated in manuscript
- 24.04.m3: C — reference [6] cites ChatGPT as a formal source
- 24.04.m4: C — fig_009 vs fig_011 show visibly different curves with no explanation of what changed
- 24.04.m5: C — mu_SI defined but never used in transition equations; redundant notation
- 24.04.m6: C — number of particles and mif2 iterations not reported; computational adequacy cannot be assessed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 1 |
| B (AI major, human also found) | 5 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 7 | 8 | 1 |
| B (AI major, human also found) | 3 | 1 | 7 | 5 |
| C (AI minor, human missed) | 7 | 6 | 0 | 6 |
| D (AI minor, human also found) | 0 | 1 | 0 | 0 |
| E (Human found, AI missed) | 6 | 7 | 4 | 7 |
| F (Human-AI contradiction) | 0 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 3 | 0 | 6 | 5/11 = 45% | 5 | 7 | 12/15 = 80% |
| Charlie | 1 | 1 | 7 | 4/11 = 36% | 7 | 6 | 13/15 = 87% |
| Doug | 7 | 0 | 4 | 7/11 = 64% | 8 | 0 | 8/15 = 53% |
| Evan | 5 | 0 | 7 | 4/11 = 36% | 1 | 6 | 7/12 = 58% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #4: "QQ plot shows good performance" is unclear, but it should be noted that the QQ plot shows long tails. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: The fitted values plot shows 1-step predictions, which is not very informative. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #6: The code for fitting arima models is derived from the `arima2` package but in fact uses `stats::arima`. It is unclear if that is intentional. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #10: Various projects from past years do a better job of explaining COVID-19 dynamics. One of these is cited in the project. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 4 out of 11 human issues (36%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #7: Readers attempting to reproduce the numerical results found that the code failed to run. (Covered only by Doug)
- Human Issue #9: This SEIR model can only fit one peak, whereas the actual pandemic had multiple waves. The report described this as a "commendable" explanation of the data, which is misleading. (Covered only by Doug)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 2 |
| Evan | 0 |
