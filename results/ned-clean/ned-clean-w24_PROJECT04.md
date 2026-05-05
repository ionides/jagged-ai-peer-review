# Ned-Clean Analysis — W24 Project 04

---

## Human Issues

1. The introduction promises an investigation of four different regions, but results are only shown for data from one. Simulation results are carried out for three cities. These simulations are discussed as if they were data, which is confusing.
2. The simulations for California, Washington and New York are rather similar with the same population, same initial conditions, and same feature that the susceptible fraction jumps straight back to 800,000 after an epidemic. It is unclear what is being plotted and why the curves are similar but different.
3. Showing simulation results as EDA is unexpected. Better for EDA to focus on data.
4. "QQ plot shows good performance" is unclear, but it should be noted that the QQ plot shows long tails.
5. The fitted values plot shows 1-step predictions, which is not very informative.
6. The code for fitting ARIMA models is derived from the `arima2` package but in fact uses `stats::arima`. It is unclear if that is intentional.
7. Readers attempting to reproduce the numerical results found that the code failed to run.
8. The authors use a software package called `GenSA`. This package is not explained. The fitting criterion seems to be least squares, leading to a fit which is essentially constant at zero. This is not very informative. Maximum likelihood, with a plausible measurement model, would be much better and was the approach taught in class.
9. This SEIR model can only fit one peak, whereas the actual pandemic had multiple waves. The report described this as a "commendable" explanation of the data, which is misleading.
10. Various projects from past years do a better job of explaining COVID-19 dynamics. One of these is cited in the project.
11. The authors plug a single simulation into least squares and optimize that function to an optimizer. That does not correspond to maximum likelihood estimation. Methods to evaluate and optimize the likelihood were taught in class and should be used. Overall, the project does not demonstrate mastery of the ideas or methods for likelihood-based inference discussed in the second half of the course.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "EDA SIR simulations use identical, arbitrary parameters regardless of region")
- Human Issue #3: covered (matched by finding: "EDA SIR simulations have no connection to main analysis; genuine EDA should examine raw data")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "Optimization is SSE not MLE; standard POMP inference never performed")
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: "Optimization is SSE not MLE; standard POMP inference never performed")

**Findings classification:**
- Finding 1 (wrong NB parameterization in dmeas): A — measurement model uses wrong parameterization; I as size, rho as prob; no overdispersion parameter k
- Finding 2 (SSE not MLE; no POMP inference): B — SSE/no likelihood matches Human Issues #8 and #11
- Finding 3 (final model hand-tuned): A — final SEIR parameters chosen by manual inspection with no justification
- Finding 4 (deterministic rmeas in global search): A — global search overwrites rmeas with nearbyint(I), making pomp object structurally incoherent
- Finding 5 (EDA simulations disconnected; identical params): B — identical arbitrary EDA parameters and no real data exploration matches Human Issues #2 and #3
- Finding 6 (double-differencing preprocessing): A — data preprocessing applies cumulative-to-incident differencing twice
- Finding 7 (no formal ARIMA vs SEIR comparison): A — no LRT, AIC, or quantitative comparison between ARIMA and SEIR
- Finding 8 (ARIMA inconsistency: (2,1,3) vs (3,1,1)): A — AIC selects ARIMA(2,1,3) but all diagnostics and fitted plot use ARIMA(3,1,1)
- Finding 9 (N treated as free variable): C — population N optimized without biological constraint; GenSA returns N exceeding actual WA population
- Finding 10 (no CI/uncertainty): C — no confidence intervals or uncertainty quantification for any model parameter
- Finding 11 (1500 data points claim vs ~160 weekly rows): C — discrepancy between stated 1500 data points and actual weekly aggregate count
- Finding 12 (main.R is unrelated measles code): C — main.R is unmodified course measles SIR example with no connection to the project
- Finding 13 ("Day" label vs weekly time units): C — time axis labels say "Day" but time variable represents sequential weeks
- Finding 14 (time-varying beta not implemented): C — model description states time-varying beta (b1/b2) but code uses single constant beta throughout
- Finding 15 (ChatGPT reference insufficient): C — ChatGPT cited without specifying which parts were AI-assisted or what errors were corrected

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "EDA SIR uses wrong data and draws unfounded conclusions; simulations discussed as epidemiological evidence")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "EDA SIR uses wrong data; genuine EDA should examine raw time series")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "Ad hoc calibration substituted for likelihood-based inference; SSE not MLE")
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: "Ad hoc calibration substituted for likelihood-based inference; SSE not MLE")

**Findings classification:**
- Major 1 (ad hoc calibration / SSE not MLE): B — SSE/no likelihood matches Human Issues #8 and #11
- Major 2 (no quantitative goodness-of-fit for SEIR): A — no log-likelihood or AIC for SEIR; comparison purely visual
- Major 3 (measurement model misspecified: wrong NB + rbinom inconsistency): A — dmeas uses wrong NB parameterization; rmeas uses rbinom; third version in global search uses nearbyint
- Major 4 (conditioning on I not H accumulator): A — model conditions on current instantaneous I rather than accumulated incidence H; accumvars never specified
- Major 5 (global opt worse than local; hand-tuned final model): A — global optimization failure unexplained; final parameters set by eyeball calibration
- Major 6 (no profile likelihoods / uncertainty): A — no confidence intervals, profile likelihoods, or parameter uncertainty for SEIR
- Major 7 (EDA SIR uses wrong data / unfounded conclusions): B — wrong aggregation and simulation-as-EDA matches Human Issues #1 and #3
- Major 8 (double-differencing preprocessing): A — data preprocessing double-differences the series; final data has unclear epidemiological meaning
- Minor 9 (ARIMA inconsistency): C — AIC selects ARIMA(2,1,3) but diagnostics and fitted plot use ARIMA(3,1,1)
- Minor 10 (no random seeds): C — no set.seed() for SEIR simulations; figures not reproducible
- Minor 11 (title SEIR but EDA implements SIR): C — paper title says SEIR; EDA code builds SIR models without E compartment
- Minor 12 (N=5M biologically implausible): C — N=5,000,000 implausible given WA population of 7.7M; global search returns N=8.83M
- Minor 13 (main.R unrelated course code): C — main.R contains measles SIR tutorial code; not referenced in Rmd
- Minor 14 (missing pfilter diagnostics): C — no pfilter used; no ESS plots or conditional log-likelihoods
- Minor 15 (ChatGPT reference undocumented): C — ChatGPT cited for code optimization; no specifics on what was changed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "EDA SIR models use identical, hard-coded parameters regardless of region")
- Human Issue #3: covered (matched by finding: "EDA SIR models use unestimated, ad hoc parameters; simulations add no analytical value as EDA")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Reproducibility failures: primary dataset not included; code cannot be independently verified")
- Human Issue #8: covered (matched by finding: "Ad hoc calibration / SSE not MLE; single stochastic simulation SSE is not likelihood")
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: "Ad hoc calibration / SSE not MLE; standard POMP inference never performed")

**Findings classification:**
- Major 1 (ad hoc calibration / SSE not MLE): B — SSE/no likelihood matches Human Issues #8 and #11
- Major 2 (no quantitative goodness-of-fit for SEIR): A — no log-likelihood or AIC for SEIR; comparison purely visual
- Major 3 (measurement model misspecified): A — wrong NB parameterization; dmeas/rmeas inconsistency; three different specifications in one document
- Major 4 (comparison not on common metric): A — ARIMA evaluated by AIC; SEIR evaluated only visually; no bridging metric
- Major 5 (no identifiability / uncertainty): A — no profile likelihoods, CI, or uncertainty for any SEIR parameter
- Major 6 (convergence evidence absent): A — single Nelder-Mead from one starting point; no likelihood traces; no evidence of convergence
- Major 7 (final model by manual inspection): A — final parameters eyeball-fitted; differ from both optimized results with no justification
- Major 8 (double-differencing preprocessing): A — data wrangling applies second difference to cumulative confirmed cases
- Major 9 (EDA SIR ad hoc params): B — identical hard-coded parameters regardless of region matches Human Issues #2 and #3
- Major 10 (title mismatch: SEIR claimed vs SIR in EDA): A — paper title says SEIR; EDA chunks define SIR without E compartment
- Major 11 (no model diagnostics / no pfilter): A — no pfilter run; no ESS plots; no per-time-step conditional log-likelihoods
- Major 12 (stochastic cost function unreliable): A — cost function calls simulate(nsim=1) and computes SSE; objective is stochastic; optimizer results non-reproducible
- Minor 13 (ARIMA inconsistency): C — AIC selects (2,1,3); diagnostics and fitted plot use (3,1,1)
- Minor 14 (N free variable despite external knowledge): C — N optimized freely; biologically implausible results not discussed
- Minor 15 (reproducibility and code quality): D — dataset not included; external URL dependency; unrelated main.R — matches Human Issue #7

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 10 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 2 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |

---

## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "EDA section presents forward simulations, not data exploration; no plots of actual observed data")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "EDA section presents forward simulations, not data exploration; EDA should reveal data features")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "SEIR model fitted without likelihood-based inference; SSE used as objective function")
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: "SEIR model fitted without likelihood-based inference; no pfilter; parameters have no statistical interpretation")

**Findings classification:**
- 24.04.1 (no likelihood-based inference / SSE): B — SSE/no likelihood matches Human Issues #8 and #11
- 24.04.2 (no quantitative goodness-of-fit): A — no log-likelihood, AIC, RMSE, or predictive score for SEIR
- 24.04.3 (optimization fails; results internally inconsistent): A — parameters collapse to near-zero; global search parameters produce flat prediction despite non-trivial values
- 24.04.4 (EDA presents forward simulations): B — simulation-not-data EDA matches Human Issues #1 and #3
- 24.04.5 (measurement model undefined; rho has no formal meaning): A — no measurement distribution specified; rho is only a scaling factor without a likelihood
- 24.04.6 (ARIMA on raw skewed counts; no transformation): A — ARIMA applied without log or sqrt transformation; QQ tail behavior and residual spike result from this
- 24.04.m1 (time-varying beta inconsistency): C — b1/b2 described in model section but single constant beta implemented
- 24.04.m2 (initial conditions not reported): C — S(0), E(0), I(0), R(0) never stated in manuscript
- 24.04.m3 (ChatGPT cited as formal reference): C — AI assistance should be disclosed in a methods acknowledgment rather than listed as a citable source
- 24.04.m4 (fig_009 vs fig_011 unexplained difference): C — two SEIR output figures differ visibly; parameter values underlying fig_011 not reported
- 24.04.m5 (redundant mu_SI notation): C — mu_SI defined as beta*I(t) but does not appear in transition equations
- 24.04.m6 (Np and mif2 iterations not reported): C — number of particles and iterations not stated; computational adequacy cannot be assessed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|-----:|--------:|-----:|-----:|
| A (AI major, human missed) | 6 | 6 | 10 | 4 |
| B (AI major, human also found) | 4 | 4 | 4 | 4 |
| C (AI minor, human missed) | 7 | 7 | 2 | 6 |
| D (AI minor, human also found) | 0 | 0 | 1 | 0 |
| E (Human found, AI missed) | 7 | 7 | 6 | 7 |

---

## Per-Reviewer Metrics

| Reviewer | Human Recall = (B+D)/(B+D+E) | AI-Unique Rate = (A+C)/(A+B+C+D) |
|----------|------------------------------:|----------------------------------:|
| Alex | 36.4% (4/11) | 76.5% (13/17) |
| Charlie | 36.4% (4/11) | 76.5% (13/17) |
| Doug | 45.5% (5/11) | 70.6% (12/17) |
| Evan | 36.4% (4/11) | 71.4% (10/14) |

---

## Cross-Reviewer Aggregation

### Consensus Misses

Human issues missed by all four reviewers (5 out of 11):

- Human Issue #4: "QQ plot shows good performance" is unclear; QQ plot actually shows long tails
- Human Issue #5: Fitted values plot shows 1-step predictions, which is not very informative
- Human Issue #6: Code for ARIMA uses `stats::arima` despite being derived from `arima2` package; unclear if intentional
- Human Issue #9: SEIR model can only fit one peak; pandemic had multiple waves; calling it "commendable" is misleading
- Human Issue #10: Various projects from past years do a better job of explaining COVID-19 dynamics

### Unique Finds Per Reviewer

Human issues covered by exactly one reviewer:

- Human Issue #7 (code failed to run): covered only by Doug (Minor 15). Missed by Alex, Charlie, Evan.

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 1 |
| Evan | 0 |

### Universal AI-Only Flags

Issues raised by all four reviewers that the human did not mention (3 issues):

1. No quantitative goodness-of-fit metric reported for the SEIR model (no log-likelihood or AIC for SEIR, making the stated comparative research question formally unanswerable): Alex Finding 7, Charlie Major 2, Doug Major 2, Evan 24.04.2
2. Measurement model misspecification (wrong NB parameterization in dmeas and/or dmeas/rmeas inconsistency): Alex Finding 1, Charlie Major 3, Doug Major 3, Evan 24.04.5
3. Final SEIR model parameters chosen by manual hand-tuning with no optimization justification: Alex Finding 3, Charlie Major 5, Doug Major 7, Evan Minor 24.04.4
