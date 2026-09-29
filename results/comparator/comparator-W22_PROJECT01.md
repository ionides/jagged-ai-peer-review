# Comparator Analysis — W22 Project 01

---

## Human Issues

1. Fig 1. "Blue line" in caption should read red line.

2. The return, $R_n=\log(y_n)-\log(y_{n-1})$, is modeled by $Y_n$. It would be easier to read if notation is set up so that $Y_n$ was a model for data $y_n$.

3. ARIMA models with different levels of integration ($D\neq 0$) do not have directly comparable likelihoods.

4. A key feature that the ARIMA models can explain here, which the GARCH and stochastic volatility cannot, is the strong weekly periodicity. People play more video games on weekends. You would have to put that into the volatility models to see if they can add value to ARMA. Or you could compare with 7-day differences. Or model weekly totals.

5. There is no particular rationale given for why a stochastic leverage model might be suitable for game play. Why would volatility be associated with increases or decreases in game play? It seemed more like an exercise in running code developed for a different situation.

6. A model (and/or exploratory analysis) explicitly linking the game growth to COVID incidence would have been nice. Since the introduction discusses an interaction between COVID levels, one may expect the work to move toward a model including such an interaction.

7. Readers might like to be told more details about the data on Steam platform.

8. The decomposition into trend + noise + cycles is unsuccessful here, for the "noise" is weekly periodicity. Frequencies for the bandpass filters should be relevant to the data being analyzed. The goal and purpose of the decomposition is not clear and not explained.

9. The choice $p=5$, $q=5$ in GARCH(p,q) is not explained.

10. The pairs plot for "Fitting the stochastic leverage model" section seems a bit sparse, perhaps the team can try `logLik>max(logLik)-40` rather than `logLik>max(logLik)-20`.

11. The conclusion on the divergence of $\mu_h$ and $\sigma_\eta$ is wrong. Maybe the authors focused on the broadness of the MIF2 convergence plot on the right end of filtering. However, the curves plotted include search traces of all starting points, including those not converging to global maxima. The convergence of these two parameters can be confirmed from the box plot. Both parameters converge well to a line ($\mu_h$ to around -7, and $\sigma_\eta$ to around 0) and the outliers require little attention since they don't correspond to global maximum.

12. In Fig 1, there is a grey interval described as a "95% confidence interval" but what that means in the current context is unclear. Is there a sensible model for which it is a reasonable estimator in this context?

---

## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "legend color mismatch in simulation plot — blue drawn, red labeled")
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "incomparable log-likelihoods invalidate model comparison table")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "applying financial leverage model to gaming data lacks justification")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: contradiction (AI says non-convergence is real and unaddressed; human says the convergence conclusion is wrong — parameters do converge per the box plot)
- Human Issue #12: missed

**Findings classification:**
- Finding 1 (incomparable log-likelihoods): B — log-likelihoods across ARIMA, GARCH, POMP are not comparable (matches Human Issue #3)
- Finding 2 (model named Fixed Leverage but implements Stochastic Leverage): A — fundamental terminological error; section heading contradicts model equations and code
- Finding 3 (particle filter run on simulated data, not real observations): A — filter log-likelihood 518.4 misrepresented as from real data
- Finding 4 (no profile likelihood or CIs for any POMP parameters): A — standard POMP step absent; no parameter uncertainty quantified
- Finding 5 (non-convergence acknowledged but not remedied): F — AI treats the authors' convergence failure claim as valid and criticizes lack of follow-up; human says the claim is wrong and parameters do converge (contradicts Human Issue #11)
- Finding 6 (GARCH labeled (5,5) but code fits GARCH(1,1)): A — claimed and implemented models differ; default order in tseries::garch is (1,1)
- Finding 7 (figure numbers skip from 5 to 7): A — Figure 6 absent; simulation diagnostic plot is unlabeled
- Finding 8 (leverage model applied to gaming data without domain justification): D — no rationale given for why leverage would exist in player-count data (matches Human Issue #5)
- Finding 9 (ARIMA model selection ignores SARIMA result, d=1 unjustified): C — SARIMA(5,0,5)(1,0,1)[7] achieves lower AIC but is dismissed without formal test
- Finding 10 (missing values loaded but never documented or handled): C — NA counts computed but never printed or discussed
- Finding 11 (legend color mismatch in simulation comparison plot): D — simulated series drawn in blue but legend labels it red (matches Human Issue #1)
- Finding 12 (ARIMA applied to already-demeaned series with additional d=1): C — double differencing not motivated; yields ARIMA(5,2,5) on original log-player series
- Finding 13 (Twitch viewership data collected but never used): C — plausible covariate retained in data frame but never incorporated or acknowledged
- Finding 14 (heavy structural borrowing from prior projects): C — Source section discloses minimal adjustments to borrowed pipeline
- Finding 15 (equation label inconsistency: R_b vs R_n): C — subscript b in leverage definition appears to be a typographical copying error

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 1 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "No benchmark comparison — ARIMA applied to differenced series vs. POMP on demeaned series, likelihoods not directly comparable due to Jacobian from differencing")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Research question and modeling strategy misaligned — no justification for why volatility characterizes COVID's effect on game play")
- Human Issue #6: covered (matched by finding: "Research question and modeling strategy misaligned — no justification for why volatility characterizes COVID's effect on game play")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: contradiction (AI says parameters mu_h, sigma_eta, phi, G_0, H_0 do not converge, agreeing with the authors; human says the conclusion of non-convergence for mu_h and sigma_eta is wrong and the box plot confirms they converge well)
- Human Issue #12: missed

**Findings classification:**
- Finding 1 (Research question and modeling strategy misaligned): B — volatility modeling not justified for COVID/game-play research question; suggests COVID-indicator model (matches Human Issues #5 and #6)
- Finding 2 (Incorrect log-likelihood adjustment for ARIMA): A — specific code error subtracting sum(log(y)) corrupts the summary table and conclusion
- Finding 3 (No profile likelihoods or confidence intervals): A — no profile likelihood computed for any POMP parameter; identifiability not formally assessed
- Finding 4 (Global search convergence not achieved): F — AI accepts authors' claim that five of six parameters fail to converge and criticizes them for reporting results anyway; human says the convergence conclusion for mu_h and sigma_eta is wrong — both converge well as confirmed by the box plot (contradicts Human Issue #11)
- Finding 5 (GARCH mislabeled): A — text says GARCH(5,5) but code fits GARCH(1,1) default; log-likelihood attributed to wrong model
- Finding 6 (No benchmark comparison on same series): B — ARIMA on differenced series vs. POMP on demeaned log-returns are not directly comparable; Jacobian from differencing changes the scale (matches Human Issue #3)
- Finding 7 (Unnecessary differencing of stationary series): A — applying d=1 to an already-stationary log-return series introduces a non-invertible MA unit root
- Finding 8 (SARIMA comparison abandoned without justification): C — SARIMA with lower AIC discarded for simplicity without a principled argument
- Finding 9 (No simulation-based goodness-of-fit diagnostic): C — only a single forward simulation from initial-guess parameters shown; no replicated trajectories from MLE or ESS profile
- Finding 10 (H_0 non-convergence not addressed): C — H_0 poorly identified; fixing or profiling over it would be appropriate
- Finding 11 (Summary table values inconsistent with code output): C — stated POMP log-likelihood of 1280 not clearly reproducible from the CSV output
- Finding 12 (Causal language without causal identification): C — introduction and conclusion use causal framing for a purely descriptive/correlational analysis
- Finding 13 (Data subsetting inconsistency): C — rescaling applied to df and player_df inconsistently; numerically harmless due to log-differencing but confusing
- Finding 14 (Figure 5 caption typos): C — "noice" (noise) and "circle" (cycle) are misspellings in the decomposition figure caption
- Finding 15 (sim1.filt vs sim1.filt2 confusion): C — initial particle filter check (loglik 518.4) evaluated on simulated data, not actual data; distinction never explained

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
- Human Issue #3: covered (matched by finding: "Invalid cross-model log-likelihood comparison — likelihoods from ARIMA, GARCH, and POMP evaluated on different data transformations cannot be ranked numerically")
- Human Issue #4: covered (matched by finding: "Seasonal ARIMA period not used in the final model — SARIMA(5,5)(1,0,1)[7] achieves AIC ~97 units lower yet authors retain ARIMA(5,1,5)")
- Human Issue #5: covered (matched by finding: "No connection between motivating question and model — leverage model has no epidemiological components and project never explains why it suits game-play data")
- Human Issue #6: covered (matched by finding: "No connection between motivating question and model — no COVID covariate included"; also matched by finding: "Research question is not answered — no event study, structural break test, or pre/post-COVID comparison")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "GARCH model misspecification in text vs. code — code uses default GARCH(1,1) not GARCH(5,5) as stated")
- Human Issue #10: missed
- Human Issue #11: contradiction (Doug says μ_h, φ, σ_η, G_0, H_0 genuinely do not converge and this invalidates the MLE; human says that conclusion is wrong — μ_h and σ_η do converge as confirmed by the box plot, and the non-converging traces correspond to non-optimal starts)
- Human Issue #12: missed

**Findings classification:**
- Major Issue 1 (Invalid cross-model log-likelihood comparison): B — likelihoods from ARIMA(5,1,5), GARCH(5,5), and POMP evaluated on different effective observation models/data transformations cannot be compared (matches Human Issue #3)
- Major Issue 2 (Global IF2 initialized from previous mif2 result): A — `mif2(if1[[1]], ...)` inherits a decayed cooling schedule, so global search does not explore from fresh starts
- Major Issue 3 (Non-convergence of most parameters): F — Doug says μ_h, σ_η and others genuinely fail to converge, invalidating the reported MLE; contradicts Human Issue #11, which says those parameters do converge and the authors' divergence conclusion is wrong
- Major Issue 4 (No profile likelihoods; identifiability unassessed): A — no profiles computed for any of the six model parameters
- Major Issue 5 (Conclusion inverts model ranking): A — conclusion is internally inconsistent even granting the invalid comparison; POMP lower than ARIMA but this is not discussed
- Major Issue 6 (No benchmark comparison appropriate for mechanistic model): A — POMP log-likelihood is lower than ARIMA but this critical finding is not discussed
- Major Issue 7 (No connection between motivating question and model): B — leverage model has no COVID/behavioral components and project never explains what inference it provides about COVID-19 (matches Human Issues #5 and #6)
- Major Issue 8 (Filtering on simulated data rather than original data): A — log-likelihood of 518.39 reported for model evaluated on simulated, not observed, data
- Minor: GARCH model misspecification in text vs. code: D — code implements GARCH(1,1) via default, not GARCH(5,5) as stated; equation shown is also GARCH(1,1) form (matches Human Issue #9)
- Minor: Seasonal ARIMA period not used in final model: D — SARIMA(5,5)(1,0,1)[7] with AIC ~97 units lower than ARIMA(5,1,5) was found but discarded; weekly periodicity not handled (matches Human Issue #4)
- Minor: ARIMA log-likelihood adjustment unexplained and non-standard: C — `ARIMA515$loglik - sum(log_df2$demean_players)` undocumented Jacobian correction not applied consistently
- Minor: Initial simulation comparison uses wrong variable: C — visualization overlays Y_state against non-demeaned log-returns while model trained on demeaned returns
- Minor: No ESS monitoring: C — ESS not reported for any particle filter run
- Minor: Pairs plot uses inconsistent log-transform: C — local search plots raw sigma_nu, global search plots log(sigma_nu), making plots non-comparable
- Minor: Research question is not answered: D — no event study, structural break test, or pre/post-COVID comparison provided (matches Human Issue #6)
- Minor: Figure numbering gap: C — figures jump from 5 to 7, Figure 6 never defined
- Minor: Computational cost not reported: C — no run time or computational resource information given

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 1 |

---

## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "22.01.1 — invalid log-likelihood comparison across model classes due to different integration levels")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "22.01.M2 — causal language without causal identification; introduction claims COVID caused player increases but analysis is purely observational")
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: contradiction (AI accepts paper's non-convergence claim as factually correct and criticizes reporting MLE despite it; human says the non-convergence conclusion is wrong and the parameters actually converge per the box plot)
- Human Issue #12: missed

**Findings classification:**
- 22.01.1: B — invalid log-likelihood comparison across model classes (ARIMA uses d=1, others use undifferenced returns; likelihoods not on same variable) (matches Human Issue #3)
- 22.01.2: A — best benchmark model not used; AIC difference misread by ~80 units; SARIMA(5,0,5)×(1,0,1)_7 outperforms selected ARIMA(5,1,5) by AIC
- 22.01.4: A — differencing of already-stationary series without justification; no ADF/KPSS test provided
- 22.01.8: F — non-convergence explicitly acknowledged but MLE reported as valid; AI accepts paper's non-convergence claim as true whereas human says non-convergence conclusion is wrong and parameters do converge (contradicts Human Issue #11)
- 22.01.3: A — sigma_nu at or near zero, a parameter boundary collapse of stochastic leverage to deterministic leverage, unremarked in paper
- 22.01.6: A — no profile likelihoods or confidence intervals for any parameter
- 22.01.G: C — GARCH model name, equation, and code are inconsistent (text says GARCH(5,5) but equation and code are GARCH(1,1))
- 22.01.5: C — filtering step run on simulated data presented as if on real data without labeling
- 22.01.M1: C — ESS not monitored during particle filtering
- 22.01.M2: D — causal language without causal identification; introduction claims COVID caused player increase but no causal strategy employed (matches Human Issue #6)
- 22.01.M3: C — title typo "Pandamic" should be "Pandemic"
- 22.01.M4: C — no sensitivity analysis for global search box bounds on G_0 and H_0

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 1 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 5 | 4 | 5 | 4 |
| B (AI major, human also found) | 1 | 2 | 2 | 1 |
| C (AI minor, human missed) | 6 | 8 | 6 | 5 |
| D (AI minor, human also found) | 2 | 0 | 3 | 1 |
| E (Human found, AI missed) | 8 | 8 | 6 | 9 |
| F (Human-AI contradiction) | 1 | 1 | 1 | 1 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 1 | 2 | 8 | 3/11 = 27% | 5 | 6 | 11/14 = 79% |
| Charlie | 2 | 0 | 8 | 3/11 = 27% | 4 | 8 | 12/14 = 86% |
| Doug | 2 | 3 | 6 | 5/11 = 45% | 5 | 6 | 11/16 = 69% |
| Evan | 1 | 1 | 9 | 2/11 = 18% | 4 | 5 | 9/11 = 82% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #2: The return, $R_n=\log(y_n)-\log(y_{n-1})$, is modeled by $Y_n$. It would be easier to read if notation is set up so that $Y_n$ was a model for data $y_n$. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #7: Readers might like to be told more details about the data on Steam platform. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: The decomposition into trend + noise + cycles is unsuccessful here, for the "noise" is weekly periodicity. Frequencies for the bandpass filters should be relevant to the data being analyzed. The goal and purpose of the decomposition is not clear and not explained. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #10: The pairs plot for "Fitting the stochastic leverage model" section seems a bit sparse, perhaps the team can try `logLik>max(logLik)-40` rather than `logLik>max(logLik)-20`. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #12: In Fig 1, there is a grey interval described as a "95% confidence interval" but what that means in the current context is unclear. Is there a sensible model for which it is a reasonable estimator in this context? (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 5 out of 12 human issues (42%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #1: Fig 1. "Blue line" in caption should read red line. (Covered only by Alex)
- Human Issue #4: A key feature that the ARIMA models can explain here, which the GARCH and stochastic volatility cannot, is the strong weekly periodicity. People play more video games on weekends. You would have to put that into the volatility models to see if they can add value to ARMA. Or you could compare with 7-day differences. Or model weekly totals. (Covered only by Doug)
- Human Issue #9: The choice $p=5$, $q=5$ in GARCH(p,q) is not explained. (Covered only by Doug)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 1 |
| Charlie | 0 |
| Doug | 2 |
| Evan | 0 |
