# Peer Review: King County COVID-19 Weekly Cases Analysis
**Project:** W24 PROJECT08  
**Reviewer:** Charlie  
**Date:** 2026-04-09

---

## Summary

This project analyzes weekly COVID-19 confirmed cases in King County, Washington (January 2020 to March 2023) using a sequential approach: an ARIMA benchmark, a standard SEIR POMP model, and an extended SVEIPR model that incorporates vaccination, partial immunity, reinfection, and time-varying transmission. The most serious finding is a dataset substitution bug in the SEIR section that silently fits the model to Washtenaw County, Michigan data rather than King County data, invalidating the SEIR analysis entirely. The SVEIPR model is more carefully implemented but suffers from a process-model coding error in the reinfection transition, heavily constrained fixed parameters in the global search, no profile likelihoods or confidence intervals for key parameters, and no quantitative comparison between the ARIMA baseline and the POMP models. The paper has genuine strengths — it employs likelihood-based inference with IF2, presents convergence traces, acknowledges model failures honestly, and produces a reasonably structured SVEIPR model — but multiple validity-threatening issues require correction before the analysis can support the stated conclusions.

---

## Major Issues

### 1. Dataset substitution bug in the SEIR section invalidates that analysis

At line 177 of `blinded.Rmd`, the code block titled "Initial Investigation" silently replaces the King County data object (`sea_df`) with data from Washtenaw County, Michigan:

```r
sea_data = full_data %>% filter(Admin2 == "Washtenaw", Province_State == "Michigan")
```

The variable `sea_df` is then overwritten with this Michigan data (line 183: `write.csv(sea_df, file = "seattle_covid.csv", ...)`). All subsequent SEIR model construction, local search, global search, and simulation visualizations in the SEIR section operate on Washtenaw County data, not King County data. The EDA (Figures 1–3) and ARIMA model are on the correct King County data (the `rm(list=ls())` call at line 414 only clears the environment before the SVEIPR section). This means the SEIR results reported — log-likelihoods of approximately -1195, convergence diagnostics, simulation plots, and parameter estimates — all correspond to a different county and cannot support any claims about King County COVID-19 dynamics. The SVEIPR section correctly re-reads King County data (line 449), but the SEIR analysis is wholly invalidated. The authors must re-run the SEIR analysis on the correct dataset.

### 2. Critical process-model coding error in the reinfection transition (dN_RS drawn from I instead of R)

At line 599 of `blinded.Rmd`, the reinfection flow is drawn from the infected compartment `I` rather than the recovered compartment `R`:

```c
double dN_RS = rbinom(I, 1 - exp(-mu_RS * dt));
```

The mathematical specification (line 481) states that $\Delta N_{RS}(t) \sim \text{Binomial}(R, 1 - \exp\{-\mu_{RS}\Delta t\})$. Using `I` as the pool draws reinfection candidates from current infecteds, not recovereds, which violates the intended model structure. Furthermore, the state updates for `S` (lines 601, 608) subtract `dN_RS` rather than add it:

```c
S -= dN_SE - dN_RS;
```

This means recovered individuals who "reinfect" actually leave `S` again rather than returning to it. The combination of the wrong source compartment and the wrong sign means the reinfection mechanism as coded does not implement what the equations describe. This is a material implementation error affecting all SVEIPR results.

### 3. No quantitative comparison between ARIMA and POMP models

The paper presents an ARIMA(3,1,3) model (log-likelihood not explicitly reported in the text, though computable from the fitted object) and POMP models with log-likelihoods of approximately -1377 (SVEIPR global search). No quantitative comparison between the ARIMA model's log-likelihood and the POMP models' log-likelihoods is presented anywhere. Without this comparison, it is impossible to assess whether the mechanistic model captures structure beyond what a simple statistical model achieves. Wheeler et al. (2024) identify benchmark comparison against non-mechanistic models as the single most diagnostic check for whether a mechanistic model adds value. The ARIMA model in this paper is well-positioned to serve as exactly this benchmark, yet the comparison is never made explicit. The authors should report both log-likelihoods on a common scale (or AIC values) and discuss what the difference implies about model adequacy.

### 4. No profile likelihoods or confidence intervals for any parameter

Neither the SEIR nor the SVEIPR analysis computes profile likelihoods for any parameter. The paper mentions "poor man's profile likelihood confidence intervals" for `gamma` and `eta` (line 918) derived from the scatter of global search results, but this is an informal and unreliable substitute. Scatter across global search replicates reflects computational noise and parameter correlation, not the actual profile likelihood. For a 25-parameter model like SVEIPR, formal profile likelihoods are essential for determining which parameters are identifiable from the data. The fixed parameters in the global search (`Beta`, `mu_PR`, `mu_IR`, `mu_RS`, `alpha`, `mu_SV`) are held constant without justification; if these are poorly identified, fixing them inflates the apparent identifiability of the estimated parameters. Per Wheeler et al. (2024), profile likelihoods and MCAP confidence intervals should be computed for key parameters including at minimum `rho`, `eta`, `gamma`, and one representative transmission multiplier.

### 5. Many scientifically important parameters are fixed without justification in the SVEIPR global search

The global search for the SVEIPR model (line 865) fixes seven parameters: `Beta = 1.01`, `mu_PR = 0.93`, `mu_IR = 0.98`, `mu_RS = 0.5`, `alpha = 0.4`, `N = 2269675`, and `mu_SV = 0.5`. Of these, `Beta`, `mu_PR`, `mu_IR`, `mu_RS`, `alpha`, and `mu_SV` are epidemiologically substantive parameters that directly govern transmission and recovery dynamics. No justification is given for fixing these values. The local search does not optimize `Beta` or `mu_SV` either. In effect, the global optimization searches over only 18 of the 25 parameters. If the MLE lies at a different value of any fixed parameter, all reported results may be substantially suboptimal. The authors should either justify these constraints by reference to external estimates with uncertainty ranges, or include them in the optimization.

### 6. Insufficient computational effort for the SEIR global search

The SEIR global search (line 364) uses `Np=200` particles and `Nmif=50` iterations — far below acceptable standards for a reliable likelihood surface. With 200 particles, particle filter estimates of the likelihood are highly variable, and 50 IF2 iterations are unlikely to achieve convergence from arbitrary starting points. The local search uses only 10 replicates with `Np=1000` and `Nmif=50`. The large standard errors in the local loglik results (e.g., se = 4.37, 6.67, 10.69 for several replicates; see `local_logliks.rds`) confirm that the likelihood estimates are noisy. For the SVEIPR model the computational effort is substantially better (Np=2000, Nmif=200 for local; Np=2000, Nmif=100 for global), but even here the authors do not present evidence that further increasing computational effort would not change results. Per Wheeler et al. (2024), convergence evidence from multiple searches from diverse starting points reaching similar likelihoods is required; this is partially present for the SVEIPR model but entirely absent for SEIR.

### 7. Quantitative goodness-of-fit assessment is purely visual for the SVEIPR model

The SVEIPR model's fit to data is assessed entirely through forward simulation plots (lines 717–720, 806–818, 942–954). No quantitative goodness-of-fit statistic (log-likelihood on the data scale relative to the ARIMA baseline, AIC, or conditional log-likelihood per time point) is provided for the final SVEIPR results. The authors themselves note that "the model found by global search still can't overcome the drawbacks like delayed peaks" (line 940), yet no quantitative measure is used to calibrate how severe this misfit is. Wheeler et al. (2024) note that "visual comparisons alone are only a weak and informal measure of goodness-of-fit." Conditional log-likelihoods should be plotted to identify specific time periods of poor fit; the particle filter `plot(pf)` output (line 727) is shown for the initial (unadjusted) parameters but not for the optimized model.

### 8. Measurement model inconsistency: SEIR uses negative binomial, SVEIPR uses Gaussian approximation without justification

The SEIR model uses a negative binomial measurement model (`dnbinom_mu`, line 213), which is the appropriate overdispersed count distribution for case reports. The SVEIPR model switches to a rounded normal approximation (lines 653–673) using `pnorm` for the density and `rnorm` rounded to integer for simulation. No justification is given for this change. The Gaussian approximation can assign positive probability to negative case counts (partially handled by the truncation in `rmeas`) and may be a poor approximation in low-count periods. The `dmeas` function does not check for `reports < 0`, which could cause numerical issues. The parameter `tau` in the Gaussian standard deviation formula `sqrt((tau*H)^2 + rho*H)` is a non-standard overdispersion specification that is not explained in the text. This constitutes a discrepancy between the described model and its implementation and may affect inference.

---

## Minor Issues

- **Data quality issue: negative weekly case counts.** The differencing of cumulative counts produces some negative weekly case counts (data corrections or reporting adjustments), which are observed values fed into the measurement model. Neither the SEIR nor the SVEIPR model accounts for negative observations; the `dmeas` Gaussian approximation in SVEIPR simply sums probabilities near zero for these cases, but the SEIR negative binomial `dnbinom_mu` cannot handle them. The authors should document how many negative values are in the data and how they are handled.

- **`rm(list = ls())` at line 414 is a code quality red flag.** Using `rm(list=ls())` in the middle of an analysis document to reset the workspace is fragile and indicates poor code organization. The proper approach is to structure the analysis so that data objects flow through the document without needing the namespace cleared.

- **ARIMA model order notation is inconsistent.** The paper selects ARIMA(3,1,3) from the AIC table at line 80, but the model is fitted as `arima(sea_df$cases, order=c(3,1,3))` — i.e., it fits ARIMA on the already-once-differenced `cases` variable with an additional `d=1` inside the `arima()` call, meaning the underlying data are differenced twice (the first difference was applied when constructing `sea_df`). The correct call should be `arima(sea_df$cases, order=c(3,0,3))` for ARMA(3,3) on the differenced series, or the AIC table should use `arima(original_data, order=c(p,1,q))` on the raw cumulative series. The analysis text and EDA section describe the data as already differenced, so the double-differencing is likely a coding error.

- **The SVEIPR vaccination transition is multiplied by (I+P)/N, making it density-dependent.** The description states "people are more willing to get vaccinated to protect themselves in the event of an outbreak," but this functional form means that at the start of the pandemic (when I+P≈0), no vaccination occurs even after week 54 when vaccines became available. This is biologically implausible and inconsistent with the stated purpose of the vaccine compartment.

- **Beta is fixed at 1.01 in all SVEIPR optimization** but is listed as a parameter in `paramnames`. This creates potential confusion about the role of `Beta` versus the multiplicative adjustment factors `b1`–`b8`. The paper should clarify why the baseline `Beta` is not optimized and how its fixed value affects the interpretation of the `b_i` estimates.

- **No seed documented for the global SVEIPR search.** The SEIR global search calls `set.seed(531)` before `runif_design`, but the SVEIPR global search uses a separate `set.seed(2062379496)` only for the design matrix (line 852), and the `bake()` call wrapping the parallel optimization does not include an inner seed for the `%dopar%` loop. Reproducing the SVEIPR global search results exactly may require knowing the parallel RNG stream state.

- **The paper reports a poor man's confidence interval for gamma and eta from global search scatter** (line 918) but does not acknowledge this as informal or that it likely underestimates parameter uncertainty. The statement "gamma ∈ (0.806, 0.988)" reads as if it is a rigorous interval when it is only the range of the top solutions across search replicates.

- **The EDA stationarity conclusion is overclaimed.** The ACF plot shows autocorrelation dropping after lag 1 for the differenced series, which is consistent with stationarity, but the paper concludes "the time series appears to be stationary after differencing." No formal stationarity test (ADF, KPSS) is performed, and the pronounced spike at week ~100 (noted in the residual analysis) indicates non-stationarity of variance that simple differencing does not address.

- **The `sveipr_model.png` image is referenced** (line 469) but is not included in the submitted file listing; only `SEIR_diagram.png` is present in the directory listing. If `sveipr_model.png` is missing, the model diagram cannot be viewed.

- **Bibliography contains multiple duplicate entries.** The `.bib` file repeats `@misc{2024/hw01}`, `@misc{2024/hw02}`, `@misc{2024/lec03}`, `@misc{2024/lec05}`, `@misc{2024/lec06}`, `@misc{2024/lec07}`, `@misc{2024/solar_cycle}`, `@misc{2024/lec10}`, `@misc{2024/lec12}`, `@misc{2024/lec14}`, `@misc{2002/statistical_inference}` and others, with identical citation keys appearing multiple times. This will cause compilation warnings and potential citation rendering errors.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/final_project.bib`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/SVEIPR_results_run_level_3/lik_local_run_level_3.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/SVEIPR_results_run_level_3/lik_global_run_level_3.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/SVEIPR_results_run_level_3/pomp_model_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/local_logliks.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project08/seir_global.rds`
