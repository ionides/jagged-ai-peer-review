# Peer Review: W25 Project 12
## "Comparative Analysis of Volatility Models for Daily Gold Prices"

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) + particle filter (pfilter) for POMP; MLE via rugarch for GARCH; MLE via arima() for ARIMA |
| **R packages used** | pomp, rugarch, tseries, ggplot2, foreach, doParallel, coda, bayesplot |
| **Code publicly available** | Partial — git repo submission, no external archive or DOI |
| **Data publicly available** | Yes — data.csv included in submission |
| **Benchmark comparison included** | Yes — ARIMA and GARCH serve as benchmarks against POMP models |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | IF2 + pfilter used, but single pfilter runs only — no logmeanexp |
| 2 | Benchmark comparison | ~ | ARIMA and GARCH compared, but log-likelihoods in Table 5 have labeling errors |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported but without Monte Carlo standard errors |
| 4 | Model diagnostics | ~ | Trace plots shown; ESS not monitored; no conditional log-likelihood plots |
| 5 | Parameter identifiability and uncertainty | ~ | Profile likelihoods computed but no CIs derived; negative estimates unaddressed |
| 6 | Computational adequacy | ~ | Np=5000, Nmif=500, 20 global replicates — adequate scale but single pfilter evals |
| 7 | Forecast methodology | N/A | No forecasting performed |
| 8 | Model variations and nested comparisons | ~ | Heston and RS models compared; no likelihood ratio tests |
| 9 | Stochasticity | ~ | Stochastic latent process; measurement model is Gaussian (adequate for returns) |
| 10 | Reproducibility and extendability | ~ | Code present; no sessionInfo, no pinned package versions |
| 11 | Corroboration with scientific knowledge | ~ | Negative variance/vol-of-vol estimates dismissed without critique |
| 12 | Measurement model specification | ~ | Heston measurement model in code matches text |
| 13 | Initial conditions | ~ | v0 estimated as a free parameter; negative estimate is problematic |

---

## Summary

This project fits ARIMA, GARCH (normal and Student-t innovations), and two POMP models (Heston stochastic volatility and a discrete regime-switching model) to daily gold log-returns from 2022–2024, comparing all five specifications by log-likelihood. The main finding is that GARCH(1,1) with Student-t innovations achieves the best log-likelihood per parameter, while the POMP models offer richer latent-state interpretations at greater computational cost. The project is ambitious in scope and uses the IF2 framework correctly in broad strokes.

**Strengths:** Two distinct POMP models are implemented and compared; global search with 20 replicates provides meaningful coverage of the parameter space; trace plots are shown for both models; profile likelihoods are computed for one parameter per model; the Discussion section engages substantively with prior course projects.

**Weaknesses:** All POMP log-likelihoods are evaluated from single particle filter runs without replication, making the key model comparisons unreliable. Physically impossible parameter estimates in the Heston model are dismissed rather than treated as evidence of misspecification. The RS model's regime visualization uses unconditional forward simulation rather than the filtering distribution. Table 5 carries incorrect GARCH model labels. Multiple code-level inconsistencies undermine reproducibility.

---

## Major Issues

### 1. Log-likelihoods evaluated from single pfilter runs without replication (CC-Yes, Error 1.4)

Throughout the POMP analysis, log-likelihoods are computed from a single `pfilter` call per parameter setting. The course standard (Ch 15, p37) requires replicated evaluation followed by `logmeanexp`:

```r
replicate(Nreps_eval, logLik(pfilter(m, Np = Np))) |> logmeanexp(se = TRUE)
```

Instead, the code uses:
- Heston evaluation: `logLik(pfilter(heston_model, params = coef(m), Np = 5000))` — single run
- RS evaluation: `logLik(pfilter(m, params = coef(m), Np = 5000))` — single run
- Profile likelihood points: `logLik(pf)` — single run per point
- Model comparison (chunk `Model_Comparison_Table`): two fresh single-run evaluations

The consequence is critical here: Table 5 compares POMP models differing by only ~3 log-likelihood units (Heston 2536.8 vs. RS 2539.7). A single pfilter run with Np=5000 on this data can easily produce Monte Carlo noise on the order of 1–3 units. The apparent superiority of RS over Heston may be entirely attributable to Monte Carlo variability. No standard errors are reported. Actionable fix: replace all pfilter log-likelihood evaluations with replicated runs (Nreps_eval ≥ 10) and report `logmeanexp(se=TRUE)`.

### 2. Physically impossible parameter estimates dismissed rather than treated as model misspecification signals

The Heston model reports v0 = -2.38e-5 (negative initial latent variance) and sigma = -0.0051 (negative volatility-of-volatility). The text states: "While the negative estimates of σ and v0 may seem concerning, they fall within acceptable ranges given the variability inherent in the particle filtering process."

This interpretation is incorrect on two counts. First, v0 is the initial latent variance; variance cannot be negative by definition. Second, sigma is a scale parameter governing random fluctuations in the volatility path; a negative point estimate signals that the optimizer has found a degenerate region, not a legitimate MLE. Per Wheeler et al. (2024, Section "Parameter identifiability and uncertainty"): "Implausible parameter estimates flagged as potential signs of model misspecification." The correct response is model revision — for example, enforcing positivity by parameterizing v0 and sigma on the log scale — not dismissal. The current finding that the MLE lands at v0 < 0 and sigma < 0 is strong evidence that the Heston model as specified is misspecified for this dataset. This conclusion is never drawn.

### 3. Profile likelihoods computed but confidence intervals not derived

Both the Heston kappa profile (Section 5.1) and the RS sigma2 profile (Section 5.2) are computed and plotted, but neither profile is used to derive a confidence interval. The correct procedure is to apply the Wilks threshold: the 95% CI is the set of parameter values where the profile log-likelihood is within 1.92 units of its maximum. The text instead describes the profiles qualitatively ("the data strongly disfavor very high reversion speeds," "a relatively moderate high-volatility level is optimal") without providing any interval. A profile computed but not used for inference provides no inferential value. Actionable fix: add a horizontal reference line at max(loglik) - 1.92 and read off the CI endpoints.

### 4. RS "Inferred Regime Over Time" plot uses unconditional forward simulation

The regime visualization in Section 5.2 is generated by:

```r
sim <- simulate(rs_model, params = coef(best_mif), nsim = 1, include.data = TRUE)
```

The `simulate()` function draws a single forward trajectory from the model's initial condition, conditioning on no observed data. This is an unconditional sample from the prior predictive distribution, not an estimate of the regime sequence given the data. The particle filter implicitly estimates the filtering distribution of the latent regime at each time step, but this is never extracted or displayed. A single unconditional simulation provides no information about which regime the market was actually in on any given day. The figure caption calling this "Inferred Regime Over Time" is therefore misleading. To correctly display the filtering distribution, the authors should extract regime state estimates from particle filter output (e.g., by saving particle states from `pfilter`).

### 5. Table 5 model labels inconsistent with fitted code

Table 5 (Section 6) lists two GARCH entries as "GARCH (1, 3)" with Gaussian and Student-t innovations, with log-likelihoods 2528.7 and 2543.4. However, the models actually fitted in Sections 4.1–4.3 are GARCH(1,1), not GARCH(1,3):

```r
spec_norm <- ugarchspec(variance.model = list(model = "sGARCH", garchOrder = c(1,1)), ...)
spec_std  <- ugarchspec(variance.model = list(model = "sGARCH", garchOrder = c(1,1)), ...)
```

Table 4 also reports log-likelihoods of 2528.66 and 2543.41 for GARCH(1,1) under normal and t distributions respectively — exactly matching the Table 5 values to rounding. The GARCH(1,3) that achieves the lowest AIC in Table 3 is never fitted and its likelihood is never reported. Table 5 therefore mislabels GARCH(1,1) results as GARCH(1,3), an error that affects the stated comparison.

### 6. armaOrder specification in GARCH AIC table may produce a different mean model than the final fitted models

The GARCH model selection function uses:

```r
mean.model = list(armaOrder = c(2, 0, 2), include.mean = TRUE)
```

In the `rugarch` package, `armaOrder` is a two-element vector `c(AR_order, MA_order)`. Passing a three-element vector `c(2, 0, 2)` is non-standard; R may silently use only the first two elements `c(2, 0)`, fitting an ARMA(2,0) mean model for the AIC comparison. The final selected models use `armaOrder = c(2, 2)`, which is ARMA(2,2). If the AIC table compares ARMA(2,0)+GARCH(p,q) models while the final model is ARMA(2,2)+GARCH(1,1), the selection results from Table 3 are not applicable to the final model choice. The authors should verify which mean specification was actually used in the AIC table by inspecting `best_garch_norm@model$modelinc` or equivalent, and rerun with the correct specification if necessary.

---

## Computational and Diagnostic Assessment

**Convergence:** Trace plots across mif2 iterations are shown for both the Heston model (Section 5.1) and the RS model (Section 5.2). The log-likelihood panels show upward convergence, and most parameters stabilize after 150–200 iterations. The use of 20 global replicates with Nmif=500 and Np=5000 is computationally substantial and represents appropriate effort for a student project at run_level=3 scale.

**Particle filter:** ESS is not monitored at any point in the analysis. Persistent ESS collapse would indicate model-data mismatch or particle degeneracy and should be checked, particularly given that the Heston model produces implausible parameter estimates. Per Wheeler et al. (2024), ESS monitoring is a standard diagnostic. The number of particles (Np=5000) is reported and is at the high end of course expectations.

**Conditional log-likelihoods:** Not computed or plotted. Per-time-step log-likelihood plots would identify specific periods where the model fails to explain the data — especially useful for the RS model, which should exhibit different log-likelihood patterns in different regimes.

**Profile likelihoods:** Computed for kappa (Heston) and log_sigma2 (RS) with 20 profile points each. Adequate density, but CIs are not derived (see Major Issue 3). The target parameter is correctly excluded from rw.sd during each profile mif2 run, consistent with course requirements.

**Computational scale:** Np=5000 and Nmif=500 per replicate, 20 global replicates, 20 profile points — this is a credible computational investment. Single pfilter evaluation per setting remains the key deficiency.

---

## Reproducibility Assessment

**Code availability:** Code is embedded in the Rmd file and a data.csv is provided. All major computations are reproducible in principle from the Rmd.

**Final parameters:** Final MLE parameter vectors are printed in result tables but not saved to standalone files (e.g., CSV or RDS). Readers must re-run the optimization to reproduce results.

**Model-code consistency:** The Heston measurement model in code (`dnorm(y, mu, sqrt(v), give_log)`) matches the mathematical description in Section 5.1. The RS measurement model (`dnorm(y, ..., sigma, give_log)` where `sigma = exp(log_sigma1)` or `exp(log_sigma2)`) is also consistent with the text.

**Package versions:** No `sessionInfo()` output is included. The `pomp` and `rugarch` APIs have changed across versions; without pinned versions, results may not reproduce on current CRAN releases.

**Auxiliary data:** The data.csv is included and the data loading code is straightforward. No auxiliary inputs are required beyond this file.

**HPC reproducibility:** No HPC scripts provided, though computation scale (20 × 500 × 5000 particles) suggests runs on a multi-core local machine are feasible.

---

## Minor Issues

- **Duplicate Figure 3 labels**: Section 2.2 assigns the log-return time series as "Figure 3. Log-Return Gold Price Series" and Section 4 assigns the ACF of squared log-returns as "Figure 3. ACF of Squared Log Returns". Two distinct figures share the same label number.

- **GARCH diagnostic plot titles are mislabeled**: The QQ-plot and ACF titles in Section 4.1 (generated by `acf(stdres^2, main = "ARMA(1,1)+GARCH(1,1) \n ACF of Squared Residuals")`) state "ARMA(1,1)+GARCH(1,1)" but the fitted model is ARMA(2,2)+GARCH(1,1).

- **Discussion claims 2025 hold-out evaluation but none is implemented**: Section 7 states that a prior project weakness is comparing models fitted on different windows, and the fix is "scoring them on a common 2025 hold-out." No out-of-sample evaluation appears in the project; the claim in the Discussion is aspirational rather than descriptive.

- **GARCH(1,1) selected over AIC-best GARCH(1,3) without adequate statistical justification**: Table 3 shows GARCH(1,3) has the lowest AIC, but GARCH(1,1) is selected as "most standard and practical." This choice is not backed by a likelihood ratio test or an explicit AIC comparison showing the difference is small. The selected model is then called GARCH(1,3) in Table 5, compounding the confusion.

- **No Monte Carlo standard errors reported for any POMP log-likelihood**: Beyond the core issue of single-run evaluation, even a note on the expected magnitude of Monte Carlo noise would allow readers to judge whether the 3-unit difference between Heston and RS is meaningful. Standard errors from `logmeanexp(se=TRUE)` are trivial to add once replication is implemented.

- **Figure 3 y-axis labeled "Log(Price)" but plots log-return**: In the ggplot call in Section 2.2, the y-axis is `y = "Log(Price)"` but the plotted variable is `gold_data$LogReturn`, which is the first difference of log prices. The label should read "Log Return" or "d(log Price)."

- **`simple_arima_model` fitted but never referenced**: In Section 3.2, the code fits `simple_arima_model <- arima(gold_log_returns, order = c(0, 0, 1))` immediately after `best_arima_model`, but this simpler model is never discussed, compared, or motivated. It appears to be an artifact of code development.

- **Missing sessionInfo or package version documentation**: No reproducible environment specification (renv, Docker, or sessionInfo output) is provided. This is particularly important given that pomp and rugarch versions affect behavior.

- **v0 parameterized without a positivity constraint**: Although the Heston rprocess floors v at 1e-6, the rinit sets v = v0 without any floor. A negative v0 initializes the latent state at an invalid value. The recommended course practice (Ch 16) of parameterizing initial compartments on a transformed scale (log or logit) would prevent this.

---

## Recommendation

**Major Revision Required.**

The core inferential comparison in this project — whether Heston, regime-switching, or GARCH best characterizes gold return volatility — rests on log-likelihood values that are each computed from a single particle filter run. Given the small numerical differences between models (approximately 3 log-likelihood units between the two POMP models), Monte Carlo noise from single-run evaluation is large enough to reverse the ranking. This must be corrected before any comparison can be trusted. The negative parameter estimates in the Heston model, if properly diagnosed as a model failure rather than a numerical artifact, would also substantially change the conclusions about that model's performance. The regime visualization error (using unconditional simulation as if it were a filtered state estimate) and the GARCH label inconsistency in Table 5 are additional substantive corrections required. The minor issues (duplicate figure numbers, plot title errors, missing sessionInfo) are straightforward to fix.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project12/blinded.Rmd`
