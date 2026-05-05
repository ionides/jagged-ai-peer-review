# Review: W24 Project 06
## *Volatility Analysis of NASDAQ*

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (iterated filtering via `mif2`) with particle filter likelihood evaluation |
| **R packages used** | pomp, rugarch, fGarch, doParallel, doRNG (versions not specified) |
| **Code publicly available** | Partial — code embedded in Rmd but no archive DOI |
| **Data publicly available** | Yes — NDAQ.csv included in project folder |
| **Benchmark comparison included** | Yes — ARMA, GARCH, ARMA+GARCH models fitted for comparison |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | mif2/pfilter used correctly, but likelihood comparison to GARCH models is invalid (different observation models) |
| 2 | Benchmark comparison | ~ | ARMA and GARCH models fitted, but log-likelihood values are not directly comparable across model families |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihood values reported but cannot be compared meaningfully; AIC not reported for POMP model |
| 4 | Model diagnostics | ~ | Convergence trace shown via `plot(if.box)` but no ESS monitoring, no conditional log-likelihoods |
| 5 | Parameter identifiability and uncertainty | ✗ | No profile likelihoods; two parameters (H_0, mu_h) explicitly noted as non-converging; no CIs |
| 6 | Computational adequacy | ~ | Np=2000, Nmif=200, Nreps_global=100 reported; only one starting region for local search; convergence of H_0 and mu_h unresolved |
| 7 | Forecast methodology | ✗ | No forecasting performed |
| 8 | Model variations and nested comparisons | ✗ | Only one POMP model specification; no nested comparisons |
| 9 | Stochasticity | ✓ | Stochastic volatility model with process and measurement noise |
| 10 | Reproducibility and extendability | ~ | stew() caching used; no package versions; no sessionInfo(); no final MLE archive |
| 11 | Corroboration with scientific knowledge | ✗ | Fitted parameters not compared to known financial volatility literature |
| 12 | Measurement model specification | ~ | Gaussian measurement model; rmeasure and dmeasure consistent, but no overdispersion considered |
| 13 | Initial conditions | ✗ | H_0 and G_0 estimated but noted as non-converging; no sensitivity analysis |

---

## Summary

This project fits a stochastic volatility POMP model to NASDAQ log return data (approximately 5 years of daily observations), alongside ARMA, GARCH, and ARMA+GARCH baselines. The POMP model is a leverage-adjusted stochastic volatility specification following course notes, implemented in the `pomp` framework with IF2 for parameter estimation. While the project demonstrates familiarity with the POMP workflow and makes a reasonable effort at multi-model comparison, it suffers from several critical methodological flaws: the log-likelihoods from GARCH and POMP models are compared directly despite being evaluated under incompatible observation models, two key parameters fail to converge, no profile likelihoods or confidence intervals are computed, and the conclusion that POMP "performs worse" than ARMA+GARCH is not validly supported by the evidence presented.

**Strengths:**
- Demonstrates a complete POMP workflow including local and global IF2 search with `stew()` caching for reproducibility.
- Motivates the GARCH and POMP models with appropriate financial time series context.
- Provides an initial simulation comparison and convergence plot.

**Weaknesses:**
- Direct log-likelihood comparison across ARMA, GARCH, and POMP models is statistically invalid.
- H_0 and mu_h fail to converge; this is acknowledged but left unresolved.
- No profile likelihoods or confidence intervals for any POMP parameter.
- The pairs plot uses a threshold of `logLik > max(logLik) - 300`, which is far too wide and obscures the region of interest.
- No ESS monitoring, no conditional log-likelihood diagnostics, and no model variations.

---

## Major Issues

### 1. Invalid direct log-likelihood comparison across model families

The conclusions state that "the global maximum log likelihood is 3510," which "performs worse than ARMA+GARCH model" (log-likelihood 3550.09). This comparison is invalid. The ARMA log-likelihood (3324.91) is computed under a Gaussian observation model on the log-returns. The GARCH log-likelihood (3476.553) is the value returned by `likelihood(ugarchfit(...))` — which is a likelihood, not a log-likelihood, as confirmed by the code calling both `likelihood(...)` and `log(likelihood(...))`, with the latter yielding ~8.17. The POMP log-likelihood of ~3510 is evaluated using the particle filter under a Gaussian measurement model on the demeaned returns. These three quantities are computed under different observation models on different scales, and cannot be directly compared. The conclusion that POMP "performs worse" rests entirely on this invalid comparison and is therefore unsupported.

The SARIMA Baseline Audit skill flags exactly this failure mode: GARCH likelihoods from `ugarchfit` are not on the same scale as ARIMA or POMP log-likelihoods and should not be numerically compared. The fix is to either evaluate all models under a common observation model and data transformation, or to use a proper out-of-sample scoring rule (e.g., mean one-step-ahead log predictive density) that does not conflate model families.

### 2. Non-convergence of mu_h and H_0 left unresolved

The authors state: "H_0 and mu_h do not converge." This is a major finding that is acknowledged and then entirely dropped. Non-converging parameters in a POMP model are one of two things: (a) evidence of parameter non-identifiability from the data, or (b) evidence of an insufficient global search box or too few IF2 iterations. In either case, the reported maximum log-likelihood of 3510 may not be a true MLE, rendering all model comparison conclusions unreliable. Per Wheeler et al. (2024, §Parameter identifiability), implausible or non-converging parameter estimates should be interpreted as potential model misspecification, not simply noted and set aside. The authors must either (a) demonstrate convergence through a wider or better-designed search box, or (b) profile over mu_h and H_0 to determine whether they are identifiable from the NASDAQ data.

### 3. No profile likelihoods or parameter uncertainty quantification

No profile likelihoods are computed for any of the four regular parameters (sigma_nu, mu_h, phi, sigma_eta), and no confidence intervals are reported. The pairs plot provides a visual impression of the likelihood surface but uses a threshold of `logLik > max(logLik) - 300`, which is 156 log-likelihood units wider than the standard 1.92-unit cutoff used for 95% confidence intervals. At a -300 threshold, virtually all searched parameter combinations are included, making the pairs plot uninformative about parameter precision. Without profile likelihoods, it is impossible to determine whether phi and sigma_eta are well-identified (Wheeler et al. 2024, §Parameter identifiability).

### 4. Global search initialized from only one local-search run (if1[[1]])

The global box search is initialized by continuing from `if1[[1]]` — a single local search replicate — rather than from fresh starting points drawn uniformly from the search box:

```r
if.box <- foreach(i=1:NADQ_Nreps_global, ...) %dopar% {
  mif2(if1[[1]], params=apply(NADQ_box,1,function(x)runif(1,x)))
}
```

Calling `mif2(if1[[1]], ...)` with new `params` continues from the parameter values in `if1[[1]]` and overwrites only the initial parameters, but retains the IF2 cooling schedule and filter state of the first local run. This is a subtle but important misuse: the global search should start fresh, not restart from a previous IF2 chain. The standard practice is to call `mif2(NADQ.filt, params=..., ...)` with the base pomp object in the global search, not a previous IF2 result. This implementation bias means the global search may be anchored near the local-search solution rather than exploring the full box.

### 5. Likelihood evaluation after global search uses the base POMP object but is compared to parameters from the global runs

In the likelihood evaluation loop following the global search, `pfilter(NADQ.filt, params=coef(if.box[[i]]), Np=NADQ_Np)` correctly uses the base filter object with coerced parameters. However, the local-search likelihood evaluation (`pfilter(NADQ.filt, params=coef(if1[[i]]), ...)`) also filters correctly. This is consistent but the authors do not explicitly verify that the two are comparable, and the intermediate sim1.filt object (built from a single simulated trajectory) is used for the initial particle filter evaluation but the base NADQ.filt object is used for the mif2 and likelihood evaluation steps. This discrepancy is not explained.

### 6. Misinterpretation of GARCH likelihood output

The code reports `likelihood(nasdaq_garch41_normal)` as 3476.553, then calls `log(likelihood(...))` to obtain 8.1538, and labels both in the text: "This model has a likelihood of 3476.553 and a log likelihood of 8.1538." This means 3476.553 is the likelihood (not the log-likelihood) — a value that the authors then compare directly to the ARMA log-likelihood of 3324.91 and the POMP log-likelihood of 3510. This is a fundamental confusion between likelihood and log-likelihood. The actual GARCH(4,1) log-likelihood is 8.1538 (or equivalently, `rugarch` often reports this on a per-observation basis, which when multiplied by sample size would give the total log-likelihood). This confusion pervades the comparison section and the conclusion. The authors must clarify the scale of each reported value and confirm whether they are comparable.

---

## Computational and Diagnostic Assessment

**Convergence:** A convergence trace is produced via `plot(if.box)`, and the authors read off approximate convergence for sigma_eta (~0.005), sigma_nu (~0), G_0 (~0.5), and phi (~0.8). The acknowledgment that H_0 and mu_h do not converge is appropriate but insufficient — no action is taken to resolve this failure.

**Particle filter:** Np=2000 particles at run_level 3 is reasonable for a 2-state, 4-parameter model, but effective sample size (ESS) is not monitored during filtering. Particle filter degeneracy is therefore undetected. The Nreps_eval=20 likelihood evaluations at the final parameters provide a reasonable Monte Carlo average, and standard errors are reported.

**Conditional log-likelihoods:** Not computed. No per-time-step diagnostic is provided. The conditional log-likelihood plot would be particularly informative here given the well-known volatility regime shift during the COVID-19 period (early 2020) that likely falls within the 5-year window.

**Profile likelihoods:** Not computed. See Major Issue 3 above.

**Computational scale:** CPU time is captured in `timing.box` but not reported in the text. The computational cost is not communicated to the reader.

---

## Reproducibility Assessment

**Code availability:** Code is embedded in the Rmd file. No archive DOI is provided. The `stew()` calls cache intermediate results to `.rda` files (e.g., `pf1_3.rda`, `mif1_3.rda`, `box_eval_3.rda`), but these files are not included in the project folder, meaning reproduction requires re-running the computationally expensive optimization.

**Final parameters:** No standalone CSV or RDS of the MLE parameter vector is explicitly archived for inspection without rerunning optimization. The code writes to `NADQ_params.csv` via `write.table(..., append=TRUE)`, but this file is not present in the submitted materials.

**Model-code consistency:** The dmeasure and rmeasure Csnippets are internally consistent: both use the Gaussian distribution centered at 0 with standard deviation exp(H/2). The mathematical description in the text matches the code.

**Package versions:** No `sessionInfo()` output or package version documentation is provided. The `pomp` API has changed across versions and results may not reproduce on the current CRAN release without version pinning.

**Auxiliary data:** NDAQ.csv is included in the project folder. No additional auxiliary data is required for this model.

**HPC reproducibility:** The code uses `doParallel` with SLURM detection, suggesting the analysis was run on a cluster. No SLURM job scripts or environment specifications are provided, making full reproduction on a cluster non-trivial.

---

## Minor Issues

- The title of the POMP model section is "Model Discription" — a typo for "Description."
- The ACF/PACF interpretation at the end of the EDA section is reversed: the text states "the number of significant spikes in the ACF plot is 1, hence, we can assume that the AR term has value 1. Likewise, the number of significant spikes in the PACF plot is 4. Hence, it can be inferred that the MA term is 4." This confuses the standard identification rule: AR order is suggested by PACF cutoff, MA order by ACF cutoff — not the other way around.
- The ARMA(4,4) model has 9 parameters (4 AR, 4 MA, 1 intercept). Combined with the GARCH(1,1) component, the ARMA(4,4)+GARCH(1,1) model has even more parameters. The use of AIC appropriately penalizes for this, but the text does not comment on the risk of overfitting relative to the simpler GARCH(1,1) model.
- The parameter `sigma_nu` converges near zero in the global search. This is a boundary value suggesting the leverage random walk may be degenerate (G_n becomes deterministic). This could indicate model misspecification or a constraint that phi captures the same information. This is not discussed.
- The pairs plot threshold `logLik > max(logLik) - 300` is far too wide to be informative about parameter uncertainty. The standard threshold for a 95% confidence region is `max(logLik) - 1.92`.
- The variable naming uses `NADQ` throughout (e.g., `NADQ_statenames`) but the index is NASDAQ (ticker symbol NDAQ). This inconsistency is minor but notable.
- References are cited only as URLs or partial citations. Reference [2] is a course slides URL, and reference [5] repeats reference [2]. Peer-reviewed citations should be used where possible (e.g., the original Bretó et al. or King et al. papers on pomp).
- `ts(time_series_data$Log_Return, start = c(2019, 4), frequency = 1)` sets frequency=1, which treats the data as annual observations, one per year. For daily financial data this should be frequency=252 (trading days per year) or similar if seasonality is to be considered. The authors themselves note the absence of seasonality analysis as a limitation.
- The QQ-plot for GARCH(1,1) with t-distribution is not a proper t QQ-plot — the code plots the theoretical quantiles against themselves on both axes (`plot(t_quantiles, t_quantiles, type='l')`) as the reference line, then overlays the sample quantiles. While functional, this is non-standard and potentially confusing.
- The `beta_n` formula in the text ("Where beta_n = Y_n * sigma_eta * sqrt(1 - phi^2)") defines beta as a function of the observed return Y_n, but in the rproc code, `beta = Y_state * sigma_eta * sqrt(1 - phi*phi)` uses the latent state variable Y_state. This inconsistency between text notation (using observed Y_n) and code (using the latent state) should be clarified.

---

## Recommendation

**Major Revision.** The project demonstrates a reasonable working knowledge of the POMP workflow but contains critical flaws that undermine all of its comparative conclusions. Most importantly: (1) the log-likelihood values across ARMA, GARCH, and POMP models are not comparable due to incompatible observation models and a fundamental confusion between likelihood and log-likelihood, (2) two key POMP parameters fail to converge and this is left unresolved, and (3) no profile likelihoods or confidence intervals are provided. The conclusion that POMP "performs worse" than ARMA+GARCH is therefore not supported. The authors must correct the likelihood comparison, investigate the non-convergence of mu_h and H_0, provide profile likelihoods for key parameters, and revise the conclusion accordingly before publication.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project06/blinded.rmd`
