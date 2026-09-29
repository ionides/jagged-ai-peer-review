# Comparator Analysis — W25 Project 12

---

## Human Issues

1. In Sec. 2.2. the ADF test is not appropriate to examine non-stationary variance.

2. ARMA is described as modeling "key autocorrelation patterns" but the sample ACF and the AIC table show that the key here is that there are no evident autocorrelation patterns.

3. The likelihood values are quite close. We saw in class (Quiz 2, Q12-02) that quantities called log-likelihood for GARCH software are sometimes not exactly the log-likelihood. It would be worth saying how you know the GARCH likelihood is actually a likelihood not a conditional likelihood of some kind.

4. The advantage of the POMP framework is that it easily allows you to use creativity to improve the model. For example, it is easy to stick a t-distribution into the measurement model. There is a missed opportunity to use that creativity for the return distribution, which is very simple to code and various other groups did it for similar situations.

5. This group did attempt some novelty, taking advantage of the flexibility of the POMP framework to test out a switching model. However, that does not help much, and they note that modeling longer tails might be more important.

6. "The ACF of squared residuals does not show significant spikes after lag1". Various uninformative plots of ARMA residuals are shown, but this potentially informative one is not.

7. "This log-likelihood [of the stochastic volatility (SV) model] is notably higher than our ARIMA and GARCH benchmarks": this is true except for the t-distributed GARCH model. That suggests including a t-distribution in the SV model.

8. The GARCH AIC values in Table 3 are not quite mathematically consistent. This should be noted, and the consequences of imperfect maximization should be discussed.

9. The Table 3 lowest AIC value is referenced as -5046.13 in the text, but that number does not appear in the table.

---

## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: contradiction (Alex's Finding 10 says ACF of squared residuals IS shown and uses it in critique; human says this plot is NOT shown)
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (Negative Heston parameter estimates): A — physically impossible negative v0 and sigma in Heston model dismissed without justification
- Finding 2 (No AIC/BIC for POMP models): A — likelihood comparison in Table 5 lacks penalty for model complexity
- Finding 3 (ARMA order inconsistency in code vs. prose): A — code labels say ARMA(1,1) while prose says ARMA(2,2)
- Finding 4 (Profile likelihood does not fix kappa in rw.sd): A — kappa omitted from rw.sd makes profile computation implicit rather than explicit
- Finding 5 (Single particle filter evaluation per replicate): A — stochastic likelihood estimates from a single pfilter run introduce Monte Carlo variance
- Finding 6 (Data extends beyond stated analysis period): A — data.csv contains observations through April 2025 but paper claims December 2024 cutoff
- Finding 7 (Regime trajectory from simulation, not filtered states): A — "Inferred Regime" plot uses simulate() rather than posterior filter output
- Finding 8 (No confidence intervals for profile likelihoods): A — profile likelihood plots lack likelihood-ratio-based CIs
- Finding 9 (Inconsistent figure numbering): C — Figure 3 label is reused, causing duplicate numbering
- Finding 10 (GARCH AIC table description): F — Alex says ACF of squared residuals is shown and uses it in critique; human says this plot is not shown (contradicts Human Issue #6)
- Finding 11 (Hardcoded log-likelihood values in Table 5): C — displayed values may not match runtime-computed values
- Finding 12 (No ESS diagnostics): C — effective sample size not reported despite claims of numerical stability
- Finding 13 (Course projects cited as published studies): C — prior student projects treated as peer-reviewed literature comparisons
- Finding 14 (Heston model lacks leverage effect): C — correlation between return and volatility innovations omitted despite discussion of asymmetry
- Finding 15 (Typos in section headers): C — "Stationairty" and "neccessary" misspellings remain despite stated use of ChatGPT for proofreading

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 1 |

---

## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Major Issue 1 (single-pfilter log-likelihoods): A — all POMP log-likelihoods computed from single pfilter runs without replication, making model comparisons unreliable
- Major Issue 2 (negative parameter estimates dismissed): A — Heston v0 and sigma negative estimates described as acceptable rather than treated as model misspecification
- Major Issue 3 (profile CIs not derived): A — profile likelihoods computed for kappa and log_sigma2 but no confidence intervals extracted via Wilks threshold
- Major Issue 4 (RS regime plot unconditional simulation): A — "Inferred Regime Over Time" figure generated by simulate() rather than filtering distribution from pfilter
- Major Issue 5 (Table 5 GARCH label error): A — Table 5 labels GARCH(1,1) results as GARCH(1,3), misidentifying the compared models
- Major Issue 6 (armaOrder three-element vector): A — three-element armaOrder c(2,0,2) in AIC table may silently use only c(2,0), making AIC comparison inapplicable to final ARMA(2,2) model
- Minor: duplicate Figure 3 labels: C — two distinct figures both labeled "Figure 3"
- Minor: GARCH diagnostic titles mislabeled: C — ACF and QQ-plot titles state ARMA(1,1)+GARCH(1,1) but fitted model is ARMA(2,2)+GARCH(1,1)
- Minor: 2025 hold-out claimed but not implemented: C — Discussion references out-of-sample evaluation on 2025 data that does not appear in the project
- Minor: GARCH(1,1) chosen over AIC-best GARCH(1,3) without justification: C — selection not backed by likelihood ratio test or explicit AIC comparison
- Minor: no Monte Carlo SEs for POMP log-likelihoods: C — magnitude of Monte Carlo noise not reported, making the 3-unit Heston vs. RS difference uninterpretable
- Minor: Figure 3 y-axis labeled "Log(Price)" instead of "Log Return": C — axis label does not match the plotted variable (log-return, not log-price)
- Minor: simple_arima_model fitted but never referenced: C — artifact of code development left in the Rmd without motivation or discussion
- Minor: missing sessionInfo/package versions: C — no reproducible environment specification provided
- Minor: v0 without positivity constraint in rinit: C — negative v0 initializes latent variance at invalid value; log-scale parameterization recommended

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |

---

## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Invalid direct comparison of ARIMA, GARCH, and POMP log-likelihoods — GARCH LLH from rugarch reports sum of log-densities of standardized residuals, not the marginal likelihood, making cross-family comparison invalid")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Invalid direct comparison of ARIMA, GARCH, and POMP log-likelihoods — paper claims Student-t GARCH is the best model via a comparison that also reveals t-GARCH outperforms POMP SV models")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (Invalid direct comparison of ARIMA, GARCH, and POMP log-likelihoods): B — cross-family LL comparison invalid; GARCH rugarch LLH is not the marginal likelihood; t-GARCH reported as best model via invalid scale (matches Human Issues #3 and #7)
- Finding 2 (Negative estimates of sigma and v0 in Heston model dismissed without justification): A — negative sigma and v0 are outside model domain; optimizer crossed feasible boundary with no parameter transformation
- Finding 3 (Profile likelihood uses single restart per grid point with single pfilter evaluation; no CI reported): A — Monte Carlo noise dominates profile near peak; no chi-squared threshold applied; identifiability/CI purpose of profiling unfulfilled
- Finding 4 (Regime sequence plot uses forward simulation, not filtering distribution): A — simulate() used instead of pfilter() filtering distribution; "Inferred Regime" label is scientifically incorrect
- Finding 5 (No benchmark comparison of mechanistic POMP models against non-mechanistic alternatives): A — GARCH does not constitute proper non-mechanistic benchmark for SV models; comparison confounds observation models and parameter counts
- Finding 6 (Regime-switching model p11 near 0.5 implies near-random switching): A — logit(p11)=0.09 gives p11≈0.522; low-volatility regime has no persistence; no identifiability diagnostic or CI for p11
- Finding 7 (Figure numbering inconsistent): C — at least two distinct figures labeled "Figure 3"
- Finding 8 (ARIMA model description inconsistency about mean specification): C — (2,0,2), (2,2), and (1,1) ARMA orders used inconsistently across sections
- Finding 9 (rw_sd for global search reuses local-search object without adjustment): C — perturbation SD of 0.005 too small for global box range of ~3 units; defeats purpose of broad initialization
- Finding 10 (ESS trajectories claimed monitored but not shown): C — no ESS plot or minimum ESS value reported despite claiming it as a distinguishing feature
- Finding 11 (Heston profile pfilter called on heston_model not modified pomp object): C — inconsistency between object used for optimization and object used for evaluation
- Finding 12 (No model diagnostics beyond trace plots and profile likelihood): C — no conditional log-likelihood plots, no ESS trajectories, no simulated-vs-observed comparison
- Finding 13 (Heston sigma and v0 not constrained to be positive; no parameter transformations): C — lack of partrans argument allows optimizer to explore infeasible domain for sigma and v0
- Finding 14 (Final MLE parameter vectors not archived): C — re-running mif2 required to reproduce results; Wheeler et al. minimum reproducibility requirement not met
- Finding 15 (ADF test interpretation: "rejecting the null of stationarity"): C — phrasing slightly imprecise; recommends also applying KPSS test for corroborating evidence

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
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
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "25.12.2 — AIC value for ARIMA stated in text does not match the table or the log-likelihood")

**Findings classification:**
- 25.12.1: A — physically impossible Heston parameter estimates (sigma < 0, v0 < 0); not raised by human
- 25.12.2: B — AIC value for ARIMA(2,0,2) stated in text is inconsistent with both the table and the log-likelihood (matches Human Issue #9)
- 25.12.3: A — GARCH specification mislabeled in final comparison table (Table 5 says GARCH(1,3) but Section 4 selects GARCH(1,1)); not raised by human
- 25.12.4: A — kappa profile flat on the left, no lower confidence bound determinable despite claim of identifiability; not raised by human
- 25.12.5: A — sigma_2 profile shows two local maxima with a valley, inconsistent with reliable profiling; not raised by human
- 25.12.6: A — logit inversion error (p11 computed incorrectly) and resulting near-random regime switching; not raised by human
- 25.12.7: A — ESS not monitored or reported for particle filter; not raised by human
- 25.12.8: A — no confidence intervals reported for any parameter; not raised by human
- 25.12.M3: A — introduction promises predictive accuracy evaluation but only in-sample log-likelihoods are presented; not raised by human
- 25.12.10: C — Heston trace plots interpreted as "strong convergence" without noting algorithm converged to a physically inadmissible region; not raised by human
- 25.12.11: C — number of pfilter replicates and logmeanexp aggregation not stated; not raised by human
- 25.12.12: C — ARMA(2,2) selected in Section 3 but Section 4 twice refers to ARMA(1,1)+GARCH(1,1); not raised by human
- Notation/presentation: C — LaTeX rendering error in GARCH-t variance equation, inconsistent figure numbering, Wikipedia reference, y-axis label cut off; not raised by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |

---

## Combined Summary Table

| Category | Alex | Charlie | Doug | Evan |
|----------|--------:|--------:|--------:|--------:|
| A (AI major, human missed) | 8 | 6 | 5 | 8 |
| B (AI major, human also found) | 0 | 0 | 1 | 1 |
| C (AI minor, human missed) | 6 | 9 | 9 | 4 |
| D (AI minor, human also found) | 0 | 0 | 0 | 0 |
| E (Human found, AI missed) | 8 | 9 | 7 | 8 |
| F (Human-AI contradiction) | 1 | 0 | 0 | 0 |

---

## Per-Reviewer Metrics

Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues
AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings

| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |
|----------|--:|--:|--:|--------------:|--:|--:|---------------:|
| Alex | 0 | 0 | 8 | 0/8 = 0% | 8 | 6 | 14/14 = 100% |
| Charlie | 0 | 0 | 9 | 0/9 = 0% | 6 | 9 | 15/15 = 100% |
| Doug | 1 | 0 | 7 | 2/9 = 22% | 5 | 9 | 14/15 = 93% |
| Evan | 1 | 0 | 8 | 1/9 = 11% | 8 | 4 | 12/13 = 92% |

---

## Cross-Reviewer Aggregation

### Consensus misses

Human issues that every reviewer failed to cover:

- Human Issue #1: In Sec. 2.2. the ADF test is not appropriate to examine non-stationary variance. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #2: ARMA is described as modeling "key autocorrelation patterns" but the sample ACF and the AIC table show that the key here is that there are no evident autocorrelation patterns. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #4: The advantage of the POMP framework is that it easily allows you to use creativity to improve the model. For example, it is easy to stick a t-distribution into the measurement model. There is a missed opportunity to use that creativity for the return distribution, which is very simple to code and various other groups did it for similar situations. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #5: This group did attempt some novelty, taking advantage of the flexibility of the POMP framework to test out a switching model. However, that does not help much, and they note that modeling longer tails might be more important. (Missed by all 4 reviewers — 4 out of 4)
- Human Issue #8: The GARCH AIC values in Table 3 are not quite mathematically consistent. This should be noted, and the consequences of imperfect maximization should be discussed. (Missed by all 4 reviewers — 4 out of 4)

Total consensus misses: 5 out of 9 human issues (56%).

### Unique finds per reviewer

Human issues covered by exactly one reviewer and missed by all others:

- Human Issue #3: The likelihood values are quite close. We saw in class (Quiz 2, Q12-02) that quantities called log-likelihood for GARCH software are sometimes not exactly the log-likelihood. It would be worth saying how you know the GARCH likelihood is actually a likelihood not a conditional likelihood of some kind. (Covered only by Doug)
- Human Issue #7: "This log-likelihood [of the stochastic volatility (SV) model] is notably higher than our ARIMA and GARCH benchmarks": this is true except for the t-distributed GARCH model. That suggests including a t-distribution in the SV model. (Covered only by Doug)
- Human Issue #9: The Table 3 lowest AIC value is referenced as -5046.13 in the text, but that number does not appear in the table. (Covered only by Evan)

| Reviewer | Unique finds |
|----------|-------------:|
| Alex | 0 |
| Charlie | 0 |
| Doug | 2 |
| Evan | 1 |
