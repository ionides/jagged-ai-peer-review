# Peer Review: W22 Project 20
## "Statistical Analysis and Modeling of Flu Reports Time Series"

---

## Summary

This project fits a SIRS compartmental model to US influenza case data (2015–2021) using the `pomp` package, with the primary scientific goal of quantifying the drop in influenza transmission during the COVID-19 pandemic (2020–2021 cycle). A SARIMA model is also fitted to pre-pandemic data as a purported benchmark. While the project demonstrates familiarity with the IF2 workflow and addresses a scientifically interesting question, it suffers from several serious methodological errors that invalidate key inferential claims: the global search is anchored to the local-search solution (anti-pattern), the profile likelihood computations allow the profiled parameter to drift, the SARIMA-vs-POMP log-likelihood comparison is doubly invalid, and the computational effort is insufficient for credible inference. The self-diagnosis in the conclusion that "profile likelihoods are not reproducible" correctly identifies that the results are preliminary, but the scope of the underlying errors is wider than acknowledged.

---

## Major Issues

### 1. Global Search Anti-Pattern: Initialized from Local IF2 Result

The global search (Section 4.6) is launched with `mf1 <- mifs_local[[1]]` as the base object, then calls `mf1 %>% mif2(params=c(unlist(guess), fixed_params), ...)`. This passes a previous IF2 chain as the first argument rather than the raw `pomp` object (`fluSIRS`). As a consequence, each global replicate inherits the cooling schedule of the local IF2 chain, which is at or near its final cooled state. The random starting parameters in `guesses` are applied, but the IF2 perturbations are already near zero due to the inherited cooling, so the optimizer effectively performs negligible exploration from those new starting points. The "global maximum" reported is therefore not meaningfully distinct from the local-search result, and the pairs plot cannot be interpreted as evidence of global coverage. The fix is to replace `mf1 %>% mif2(...)` with `fluSIRS %>% mif2(...)` in the global foreach loop.

### 2. Profile Likelihood: Profiled Parameters Not Fixed in rw.sd

For the profile over `a` (Section 4.7.2), the `mif2` call uses `rw.sd=rw.sd(b=0.02, c=0.02, d=0.02, mu_IR=0.02, mu_RS=0.02, k=0.02)`, correctly omitting `a`. However, for the profile over `b` (Section 4.7.3), the call uses `rw.sd=rw.sd(a=0.02, c=0.02, d=0.02, mu_IR=0.02, mu_RS=0.02, k=0.02)`, which also correctly omits `b`. Upon close inspection, both profiles appear to handle this correctly — `a` is excluded from the `b`-profile rw.sd and vice versa.

However, both profile IF2 calls share the same base object `mf1`, which is the first local-search result (same anti-pattern as Issue 1). This means both profile searches inherit a cooled IF2 state, so the nuisance-parameter optimization at each profile grid point is equally compromised. The profile curves produced are unreliable for the same reason as the global search.

### 3. Invalid SARIMA-vs-POMP Log-Likelihood Comparison

The conclusion states: "The SARIMA(2,1,1)×(1,1,0)_52 model is able to fit and predict the total pre-pandemic flu cases very well with the log likelihood value around -162. The SIRS model is able to fit data relatively well...with a log likelihood around -2,000." This comparison is doubly invalid:

**Dataset-length mismatch**: The SARIMA is fitted to `BoxCox_ts[1:400]` (approximately 2010–2018, about 400 observations, pre-pandemic), while the SIRS POMP model is fitted to `df_pand` (2015 to mid-2021, approximately 313 observations). The two likelihoods sum over different numbers of observations.

**Observation-model mismatch**: The SARIMA likelihood is Gaussian on Box-Cox-transformed data; the SIRS likelihood is negative binomial on original count data. These are evaluated under entirely different observation models and are not numerically comparable. A log-likelihood of -162 from a Gaussian SARIMA on ~400 transformed observations conveys no information about how well the SARIMA fits relative to the SIRS model on counts. The conclusion that the SIRS model is worse cannot be drawn from this comparison (Wheeler et al. 2024, §Benchmark comparison).

### 4. Insufficient Computational Effort

At run_level 3, the analysis uses Np=1,000 particles, Nmif=50 IF2 iterations, Nglobal=20 global starting points, Npoints_profile=20 profile grid points, and Nreps_profile=5 replicates per grid point. For a 12-parameter model (10 estimated) on approximately 313 weekly observations, these settings are marginal at best. The local search convergence traces (Section 4.5) show that several parameters (`mu_RS`, `mu_IR`, `a`, `b`, `d`) have not converged after 50 iterations — this is explicitly noted in the text but not treated as a diagnostic requiring more computation. The profile CI cutoff plots (Sections 4.7.2–4.7.3) show sparse and scattered point clouds, consistent with inadequate particle counts and/or iteration budgets. Without convergence, reported log-likelihoods may be far below the true MLE, making all downstream profile likelihood and CI calculations unreliable (Wheeler et al. 2024, §Computational adequacy).

### 5. No Benchmark Comparison

Despite including a SARIMA model, the project does not use it as a proper quantitative benchmark for the SIRS model's log-likelihood. A valid benchmark would fit both models to the same dataset, under the same observation model, or use a proper scoring rule. As noted in Issue 3, the presented comparison is invalid. Without a valid benchmark, there is no objective basis for assessing whether the SIRS model captures meaningful structure beyond what a simple statistical model would achieve (Wheeler et al. 2024, §Benchmark comparison).

### 6. Reporting Rate Fixed at an Implausible Value Without Justification

The parameter `rho` (reporting rate) is fixed at `4e-5` (4 per 100,000 infected) and never estimated. The justification in Section 4.2 is heuristic: the proportion of total US population that tests positive for influenza each year is approximately 0.004%, so the authors interpret `rho` as the fraction of infected individuals who are reported. However, the CDC data reports laboratory-confirmed positive specimens out of tested specimens, not total infections — the denominator is not the US population. The appropriate value of `rho` depends on the case ascertainment rate, which is an unknown epidemiological quantity. Fixing `rho` at a potentially misspecified value absorbs model misfit into other parameters, particularly the transmission rate `a` and dispersion parameter `k`. At minimum, a sensitivity analysis or profile likelihood over `rho` should be presented. Additionally, `N` is fixed at 325 million (average 2015–2019 US population) for a 6-year time series — while the population change over this period (~2%) is modest, fixing both `N` and `rho` simultaneously removes two degrees of freedom that could expose model misspecification.

### 7. Accumulator Semantics: H Accumulates Recoveries, Not Infections

In `sirs_step`, the accumulator is updated as `H += dN_IR` (recoveries from I to R), while the observation model is `dnbinom_mu(reports, k, rho*H, give_log)`. This means the model interprets reported flu cases as recovered individuals, not newly infected individuals. For influenza with a short infectious period (a few days to a week), `dN_IR` and `dN_SI` are numerically similar in steady state, so the bias may be modest. However, accumulating recoveries rather than new infections is semantically incorrect for a disease reporting system that counts incident cases. The POMP standard practice is to accumulate `dN_SI` (or cases entering the infectious class) as the quantity observed by surveillance (Wheeler et al. 2024, §Measurement model specification). This should be verified against the intended observation process.

---

## Minor Issues

- **Section 4.5 (local search)**: The local search uses `%do%` rather than `%dopar%`, meaning replicates run sequentially despite the parallel backend being registered. The global search correctly uses `%dopar%`. This makes the local search unnecessarily slow and should be corrected for consistency.

- **Section 3.3 (SARIMA prediction)**: The SARIMA prediction is presented visually with a claim that "the predicted line is significantly close to the original data," but no quantitative prediction error (RMSE, CRPS, coverage of prediction intervals) is reported. The visual comparison covers a held-out interval of ~100 weeks but the figure caption is minimal.

- **Model description (Section 4, equation for Beta)**: The text defines the seasonality function as `cos(2*pi*(t+d)/52)`, but the Csnippet implements `sin(2*pi*(t+d)/52)`. This discrepancy between the mathematical description and the code should be corrected; the code takes precedence for what is actually estimated, so the text is incorrect.

- **BoxCox transformation in SARIMA**: The transformation `((X + 1050)^0.2 - 1) / 0.2` uses a hardcoded shift of +1050, which is larger than many observed case counts. The justification for this offset is not explained; it appears to be chosen to avoid non-positive values but is not connected to the Box-Cox lambda reported by `BoxCox.lambda()`.

- **Section 4.2, rho justification**: The text states the number of tested individuals is around 120,000 per year with ~10% positivity, yielding ~12,000 reported cases. But the y-axis of the time series plot shows peaks of ~20,000–30,000 weekly cases (not annual). The arithmetic underlying the `rho` calculation is not shown, making it difficult to verify.

- **Section 4.7.1, "Poor man's profile likelihood"**: The text presents scatter plots of the global-search results as a preliminary profile assessment. This is an appropriate exploratory step, but the plots use all results from `sirs_lik.csv` including earlier local-search results, which may have lower likelihoods and different parameter distributions than the global-search results alone. Filtering to global-search results only would give a cleaner picture.

- **Section 5, CI not reported**: Despite running profile likelihood calculations for both `a` and `b`, the conclusion does not report the resulting confidence intervals explicitly. The `a_ci` and `b_ci` objects are computed but only mentioned in passing as "not reproducible." Reporting the specific CI bounds (even if acknowledging they are preliminary) would increase scientific value.

- **References**: Reference [0] ("Suggestions from Professor E. Ionides office hours") is cited in the introduction as the source of the claim that "the flu drop in 2020-2021 can be modeled by low mean transmission rate." This is an informal reference and cannot be verified; the claim should be supported by the paper's own analysis or a citable source.

- **Code quality**: The Rmd contains numerous commented-out code blocks (e.g., alternative parameter sets, alternative data filters, alternative fixed_params), making it difficult to determine which version of the analysis was actually run. These should be removed or clearly annotated to indicate they are experimental alternatives.

- **Missing model diagnostics**: No effective sample size (ESS) monitoring results are discussed or analyzed beyond noting "ESS struggles at the beginning of each cycle." No conditional log-likelihood plots are presented to identify specific time periods of poor fit (Wheeler et al. 2024, §Model diagnostics).

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-arima-double-invalid-comparison/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project20/blinded.Rmd`
