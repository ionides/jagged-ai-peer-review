# Peer Review: W24 Project 10
**Title:** POMP Analysis on Covid-19 Cases in Malaysia and Influenza in the U.S.

---

## Summary

The paper applies a stochastic SEIRV compartmental model to two disease datasets: COVID-19 weekly cases in Malaysia (2021–2022) and U.S. weekly influenza A cases (2017–2018 season). The authors fit the model using IF2 via `mif2()`, perform a global parameter search for the flu model, and compute a profile likelihood for the vaccination rate parameter `mu_SV`. While the choice of a stochastic POMP framework is appropriate and the use of particle-filter-based inference is methodologically sound, the paper contains several critical implementation bugs that undermine the validity of the stated model. The COVID-19 analysis is effectively abandoned after a failed local search, and the flu analysis, while more complete, suffers from a mis-specified profile likelihood design, missing benchmark comparisons, absent diagnostics, and reproducibility problems.

---

## Major Issues

### 1. Critical Csnippet bug in COVID model: R→S transition draws from wrong compartment

In the COVID SEIRV step Csnippet (lines 222–224), the waning immunity transition is coded as:

```c
double dN_RS = rbinom(I, 1-exp(-mu_RS*dt));
R -= dN_RS;
S += dN_RS;
```

The draw is from `I` (infectious individuals), not from `R` (recovered individuals). This means the code does not implement waning immunity from R to S at all; instead it removes individuals proportionally from I again (double-counting). The model being fitted is not the SEIRV model described in the text. This is a foundational correctness failure for the COVID analysis. The fix is to replace `rbinom(I, ...)` with `rbinom(R, 1-exp(-mu_RS*dt))`.

### 2. Flu Csnippet silently removes the R→S transition entirely

The flu model Csnippet (lines 357–369) does not contain any `dN_RS` transition. The compartment R accumulates individuals from I but no individuals ever leave R. The parameter `mu_RS` is listed in `paramnames`, included in `rw.sd` during the local search, and profiled in the global search — but it has no effect on the model's dynamics whatsoever. The flu model is therefore a SEIRV model with a permanent recovered class, not the looped SEIRV described in the text and motivated by the literature on reinfection. All parameter estimates for `mu_RS` and any biological interpretation drawn from them are invalid.

### 3. Profile likelihood over mu_SV is mis-designed: starting guesses selected by rho, not mu_SV

The profile likelihood chunk (lines 556–562) constructs starting guesses by grouping the global search results on `round(rho, 2)` and keeping the top 5 by log-likelihood within each rho group. The intent of a profile over `mu_SV` is to seed starting values that span the range of `mu_SV` values, so that each fixed value of `mu_SV` is explored by at least one run. Grouping by `rho` instead provides no coverage guarantee over the `mu_SV` axis. The resulting profile may have large gaps in `mu_SV` coverage while over-representing certain `rho` values, rendering the reported confidence interval unreliable. The correct design is to partition starting guesses by `round(mu_SV, 2)` (or use a `profile_design()` grid over `mu_SV`).

### 4. Profile confidence interval threshold is nonstandard and its application is inconsistent

The profile plot horizontal line and the CI bounds both use `0.5 * qchisq(df=1, p=0.90)` as the cutoff (lines 614, 618). This corresponds to a 90% confidence interval by the Wilks approximation. The text (line 623) correctly states this is a 90% CI; however, this is a weaker standard than the conventional 95% and is not justified. More critically, the CI bounds in lines 617–619 are computed directly from `results`, which is the object produced by the profile search. However, `results` was appended back into `final_params_2.csv` (lines 593–597) which comingles global search points with profile search points. The `max(results$loglik)` used as the reference likelihood in the CI computation is the maximum over the profile search results only (after the append), which may differ from the true global maximum. A correct profile CI should use the global maximum log-likelihood as the reference value.

### 5. No benchmark comparison for either disease model

Neither the COVID nor the flu analysis includes a comparison to any non-mechanistic statistical benchmark (e.g., ARIMA, auto-regressive negative binomial). Without such a comparison it is impossible to assess whether the SEIRV model captures meaningful structure beyond what a simple time-series model would achieve. This is particularly important for the flu model, where the authors claim the model "fits the data well." Wheeler et al. (2024) found that none of 32 cholera papers they reviewed included this comparison, and when they added one, some mechanistic models failed to outperform it. The authors should fit at least one ARIMA baseline and compare log-likelihoods on a common scale.

### 6. No model diagnostics of any kind

The paper presents no diagnostic tools beyond visual trace plots and the global pairs plot. There are no: conditional log-likelihoods per time step (to identify specific periods of poor fit), effective sample size (ESS) monitoring during filtering, comparison of filtering-distribution simulations to observed data, or summary statistics comparing simulated and observed epidemic curves. The single forward-simulation figure for the flu model at fixed parameter values is insufficient. These diagnostics are essential for understanding where and why the model succeeds or fails, and their absence makes the claim that the flu model "captures disease dynamics effectively" unsubstantiated. (Wheeler et al. 2024, §Model diagnostics)

### 7. No quantitative goodness-of-fit or model comparison reported for the COVID analysis

The COVID analysis is terminated after a local search with no reported log-likelihood value. Only visual inspection of trace plots is used to conclude the model failed. The authors should report the best log-likelihood achieved in the local search and compare it to the flu model's log-likelihood on a per-observation basis to support any comparative claims. As stated in Wheeler et al. (2024): "visual comparisons alone are only a weak and informal measure of goodness-of-fit."

### 8. Parameter identifiability not assessed for key parameters

No profile likelihoods are computed for `Beta`, `mu_EI`, `mu_IR`, or any parameter other than `mu_SV`. The global pairs plot shows that the red points for several parameters (including `Beta`, `mu_EI`, and `mu_IR`) do not form a well-defined ridge. The authors themselves note (line 542) that "the curve formed by red dots in Beta ~ loglik, mu_EI ~ loglik, and mu_IR ~ loglik did not clearly show a trend of convergence." This is a signal of potential non-identifiability that requires profile likelihood investigation, not a suggestion to "increase the search range." Unidentifiable parameters undermine all confidence intervals and biological interpretations. (Wheeler et al. 2024, §Parameter identifiability)

---

## Minor Issues

- **Hard-coded absolute paths**: Lines 119 and 147 reference `/Users/ganjingrui/Desktop/cases_malaysia.csv` and `/Users/ganjingrui/Desktop/FluData.csv`. These paths are local to one author's machine and will cause the document to fail to render on any other system. The data should be loaded from relative paths or from the URLs already used elsewhere in the document (line 184 uses a GitHub URL for the same COVID data; a similar approach should be used for the flu data).

- **Flu population size N=1,000,000 unjustified**: The total population parameter is fixed at N=1,000,000 (line 393) for a model of U.S. national influenza. The U.S. population is approximately 330 million. The rationale for this choice — presumably that the surveillance data captures a fixed effective population, not the full U.S. population — is never stated. This choice directly scales `Beta` and therefore the estimated transmission rate has no interpretable biological meaning without justification. The parameter should either be estimated, or its fixed value and the biological interpretation of the effective sentinel population should be justified.

- **COVID local search uses rw.sd values equal to parameter starting values**: In the COVID local search (lines 312), the random walk standard deviations are set equal to the parameter values used in the simulation (`Beta=2`, `mu_EI=0.25`, etc.), which is extremely large perturbation relative to typical IF2 practice. This likely contributed to the convergence failure observed in the trace plots but is not discussed.

- **Global search `mif2` calls chained with a second `mif2(Nmif=50)` refinement**: The global search (line 511) chains a second `mif2(Nmif=50)` call on the first result. This is a legitimate refinement step but is not explained. The cooling schedule for the refinement step is inherited from the first call, which means the second call effectively starts from a highly cooled state and may add little exploration. The purpose and effect of this chaining should be documented.

- **Profile search `mu_SV` not included in `rw.sd`**: In the profile chunk (line 577), `mu_SV` is absent from the `rw.sd` argument. For a valid profile over `mu_SV`, the parameter should be fixed (excluded from perturbation), which is the intended behavior; however, the code also omits `mu_SV` from `partrans` (line 578), meaning `mu_SV` is passed on the natural (untransformed) scale but receives no perturbation. Whether this correctly fixes `mu_SV` at the guess value or allows it to drift via numerical issues in the optimizer should be verified.

- **90% confidence interval level not justified**: The choice of 90% rather than the standard 95% for the profile confidence interval is not motivated. Standard practice reports 95% CIs; deviation should be justified explicitly.

- **No `sessionInfo()` or package version documentation**: The project does not document R or package versions. The `pomp` API has changed across versions and results may not reproduce on a different installation without version pinning.

- **Duplicate and inconsistent reference numbering**: References 4 and 6 in Section 8 are identical URLs (`https://www.cdc.gov/coronavirus/2019-ncov/your-health/reinfection.html`). Additionally, references in the text use angle-bracket notation such as `[<8>]` which is not a standard citation format in R Markdown.

- **Methodology section heading misspelling**: Section 3 is titled "Methodlogy" (line 35).

- **No out-of-sample evaluation or forecast**: The paper does not attempt any forecast or out-of-sample evaluation. Given that the stated motivation includes informing public health interventions, at minimum a brief discussion of how the fitted model would be used for projection — and acknowledgment that forecasts should be conditioned on the filtering distribution — would strengthen the conclusion. (Wheeler et al. 2024, §Forecasts)

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dataset-substitution-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project10/blinded.Rmd`
