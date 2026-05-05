# Peer Review: W22 Project 20 — Statistical Analysis and Modeling of Flu Reports Time Series

## Summary

This project fits a SARIMA model and a SIRS-POMP model to US weekly influenza case counts from CDC data (2010–2022), with the primary scientific goal of explaining the near-total disappearance of flu cases during the 2020–2021 COVID-19 pandemic cycle. The SIRS model introduces a step-change in the mean transmission rate (parameter `b` for the pandemic year vs. `a` for all other years) and a sinusoidal seasonal modulation. Profile likelihoods over `a` and `b` are computed but the central inference goal — formally testing whether `a` differs from `b` — is not completed. The report is well-organized and shows genuine effort, but contains a collection of methodological and coding deficiencies that limit the validity of its conclusions.

---

## Major Weaknesses

### 1. Critical Bug: Profile Trace for `b` Groups by `a` Instead of `b`

In the profile trace chunk `a_b_profile_trace_2` (Section 4.7.3), the code operating on `profile_results_b` groups observations by `round(a, 5)` instead of `round(b, 5)`, and then plots the resulting filtered points with `x = a` and `y = b`. This means the "profile trace" for parameter `b` is actually an artifact based on the wrong grouping variable. The confidence interval calculation for `b` (`b_ci`) is unaffected (it filters on `loglik > ci.cutoff_b`), but the trace visualization does not represent the actual behavior of `b`'s profile and produces a misleading plot. The trace code for `a` correctly groups by `round(a, 5)` and plots `(a, b)`.

Evidence: Line 997 reads `group_by(round(a,5))` inside a block operating on `profile_results_b`.

### 2. Degenerate Profile Likelihood Confidence Intervals

The reported profile likelihood confidence intervals are degenerate. For parameter `a`, the output shows `min = 0.253, max = 0.253` (a single point), and for parameter `b`, `min = 1.78, max = 1.78` (another single point). A valid 95% CI should span a range. This suggests the profile likelihood surface is too flat or the search was too coarse to identify the full parameter range above the cutoff. The authors do not discuss this failure; instead they present single-point "confidence intervals" without comment. No scientific conclusions can be drawn from single-point CIs.

Evidence: HTML output at section 4.7.2 shows `## 1 0.253 0.253` and at section 4.7.3 shows `## 1  1.78  1.78`.

### 3. sin vs. cos Inconsistency in Seasonality Model

The mathematical equation in the text (Section 4, model description) states the seasonal transmission rate as `beta(t) = beta_0(t)(1 + c*cos(2*pi*(t+d)/52))`, using cosine. However, the C snippet implementing `sirs_step` uses `sin`: `Beta = Beta0*(1 + c*sin(2*pi*(t+d)/52))`. Cosine and sine represent phase-shifted versions of the same function, so with a free phase parameter `d` the model fit is equivalent, but the discrepancy between stated model and implemented model is a documentation error that undermines reproducibility and scientific clarity. The text should either use sine consistently or explain the equivalence.

Evidence: Equation at line 310 of the Rmd uses `cos`; C snippet at line 432 uses `sin`.

### 4. Null Hypothesis Test for Transmission Rate Difference Not Executed

The stated scientific goal is to determine whether the pandemic caused a reduction in flu transmission (i.e., whether `b < a` significantly). The conclusion acknowledges that "Such explanation in general might be wrong and requires rigorous statistical support, for example, by obtaining reproducible profile likelihoods and confidence intervals" and that this was left for future work. However, the profile likelihoods for both `a` and `b` are already computed — the natural next step (performing a likelihood ratio test or checking whether the CIs for `a` and `b` overlap) is not taken. The core scientific question posed in the introduction is therefore unanswered. The paper's primary conclusion ("note that having parameter `b` smaller than `a` helps to fit pandemic cases drop quite well") is a qualitative observation, not a statistical inference.

### 5. Very Poor Final POMP Likelihood Despite Run Level 3

The best log-likelihood from the SIRS model reported in the HTML output (from the local search result) has an order of magnitude far below what a reasonable model fit for approximately 300 weekly observations should achieve (the best shown result from the local search table: `a=5.06, b=4.11, loglik` not explicitly printed in the table excerpt shown, though the conclusion states "around -2,000"). The parameter box for the profile likelihood reveals the worst stored observation has loglik = -355,362 and the best is -1,922. The range is extremely wide, suggesting neither the local nor global search reliably found the likelihood maximum. The `mif2` parameter convergence traces shown for local search already note that several parameters "do not show evidence of convergence yet." At run level 3, using `Nmif=50` and `Np=1000` for a 300-observation flu dataset is modest; the lack of convergence calls the entire optimization into question.

### 6. Local Search Uses Sequential `%do%` Instead of Parallel `%dopar%`

The local search (Section 4.5) uses `foreach(i=1:20, .combine=c) %do% {}` (sequential execution) while all other parallel tasks in the project use `%dopar%`. Given that the local search runs 20 separate `mif2` chains, this misses the opportunity for parallel execution available on the Great Lakes cluster. The `registerDoParallel(cores)` setup at the top goes unused for this computation. The inconsistency also means the baked `local_search.rds` file was produced sequentially, making it slower than necessary.

### 7. Incomparable Likelihoods Between SARIMA and SIRS Models

The conclusion states the SIRS model log-likelihood of around -2,000 is "an order of magnitude different from the SARIMA's one" of around -162. However, these are computed on entirely different data subsets: the SARIMA uses Box-Cox transformed data on the pre-pandemic period (weeks 1–400 from 2010), while the SIRS uses raw case counts on a different time window (2015 week 40 through June 2021, approximately 300 weeks). Likelihoods are not comparable across different transformations, different sample sizes, or different distributional families. The conclusion presents this magnitude difference as potentially meaningful without acknowledging that the comparison is methodologically invalid.

### 8. Measurement Model Uses `lik = 0` Instead of `lik = (give_log ? -Inf : 0)` for Boundary Cases

The `dmeasure` C snippet `sirs_dflu` returns `lik = 0` when `k < 0`, `rho < 0`, or `H < 0`, with a comment "quick fix: may need a better solution." When `give_log = 1` (the log-likelihood is requested), returning 0 instead of `-Inf` corresponds to a likelihood of 1 (log-probability of 0), not a probability of 0. This numerical corruption could cause the particle filter to treat boundary-violating parameter configurations as having a log-likelihood of 0 (best possible) rather than negative infinity (worst possible), potentially biasing the search toward invalid parameter regions. The correct fix is to return `lik = (give_log ? -Inf : 0)` or equivalently `lik = give_log ? R_NegInf : 0`.

### 9. Section 4.4 Is Missing

The section numbering jumps from 4.3 ("Particle filter and likelihood for initial guess") to 4.5 ("Local search"), skipping section 4.4. This is not explained and may indicate a section that was dropped or planned but never written. The absence creates confusion about whether an intermediate step (e.g., sensitivity analysis or model diagnosis) was planned.

---

## Minor Weaknesses

### 10. BoxCox Transformation Is Applied to Shifted Data With Arbitrary Constant

The Box-Cox transformation is applied as `(cases + 1050)^0.2 - 1)/0.2`. The constant 1050 is added to avoid zero and negative values but is not justified in the text. The computed `BoxCox.lambda` is 0.2099, and the authors use 0.2, which is close but not identical. More importantly, the additive constant 1050 appears arbitrary — its choice affects all model estimates but is not discussed. The authors should explain why 1050 was chosen and whether results are sensitive to this choice.

### 11. SARIMA Fit and Prediction Data Subsets Are Described Inaccurately

The text states "we use the data in the interval 2010-2018 to predict the total flu cases in the interval 2018-2020." The code shows `BoxCox_ts <- ts(ts_bc[1:400], ...)`, which starting from week 40 of 2010 with 400 observations reaches week 40 of 2018 approximately. The forecast of 100 steps then covers roughly 2018–2020, consistent with the description. However, the inverse Box-Cox transformation uses `(fit$pred * 0.2 + 1)^5 - 1050`, which is the exact inverse of a lambda=0.2 Box-Cox only if `x = (y^0.2 - 1)/0.2`, meaning the inverse is `(x*0.2 + 1)^5`. This is correct algebraically, but the chosen start date for plotting `mod_fore` (`start = c(2018, 23)` and initial `start = c(2016, 51)`) is not explained in the text.

### 12. rho Is Fixed at an Approximated and Imprecisely Justified Value

The reporting rate `rho` is fixed at 4e-5 throughout the POMP analysis. The justification provided is that approximately 10% of 120,000 tested individuals per year test positive, yielding ~12,000/year or ~230/week out of 325 million people, which is roughly 7e-7, not 4e-5. The text's arithmetic ("10% of specimens tested is around 4e-5") appears inconsistent. This parameter is fixed and excluded from all search and profile likelihood computations, yet it directly scales the expected reported counts (`rho*H`). Fixing `rho` at a potentially wrong value will distort estimates of all other parameters that appear in `H`.

### 13. Global Search Dispersion Across Parameter Space Appears Unreliable

The parameter box for profile likelihood (Section 4.7) shows the range of stored `sirs_lik.csv` results: `mu_IR` ranges from 0.96 to 44.9 and `mu_RS` ranges from 0.22 to 10.75. An `mu_IR` of 44.9/week would imply a flu recovery period of less than half a day, which is biologically implausible (typical recovery is 5–7 days). The global search is clearly finding solutions in biologically unreasonable parameter regions without constraints, and the authors do not filter or comment on these implausible values.

### 14. Missing Convergence Diagnostics for Global Search

The report provides convergence traces for the local search (Section 4.5) but does not provide equivalent traces for the global search (Section 4.6). For POMP analyses it is standard practice to show that `mif2` chains from the global search converge to similar log-likelihood values, confirming a reliable likelihood maximum was found. Without this, it is impossible to assess whether the global search improved on the local search or simply scattered across the parameter space.

### 15. The Wavelet Transform Section Adds Little Scientific Value and Contains a Minor Error

The wavelet analysis in Section 2.3 demonstrates that the flu time series has a stable 52-week period before the pandemic. While visually informative, the wavelet transform formula presented contains a typo: the integral variable is `t` in the Morlet formula (`e^{i\omega x} e^{-x^2/2}`) but the integration limits are written as `dt` while the variable of integration inside the formula is `x`, creating inconsistency. More substantively, the wavelet result (that there is a 52-week periodic component that disappears in 2020) is observable directly from the raw time series plot and the standard ACF, making the wavelet section largely redundant. Its use as a motivation for restricting SARIMA to pre-pandemic data is reasonable, but the same conclusion could be reached with simpler tools already shown.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project20/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project20/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project20/README.txt`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project20/US_influenza_2010-2022.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project20/Makefile`
