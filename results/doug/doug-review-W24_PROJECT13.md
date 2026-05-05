# Peer Review: W24 Project 13
## Taiwan COVID-19 SIQRIQR POMP Analysis

---

## Summary

This project models COVID-19 case counts in Taiwan using both a SARIMA baseline and a custom SIQRIQR POMP model, focusing on the second (Omicron) wave. The authors motivate a two-strain quarantine compartment model, implement it in pomp using IF2 (local and global searches), and compare the approaches qualitatively. While the biological motivation for the SIQRIQR structure is thoughtfully articulated, the analysis suffers from severe methodological deficiencies: no quantitative goodness-of-fit comparison between the SARIMA and POMP models, no profile likelihoods or confidence intervals, an R-code step function that contains code errors and undefined variables, a hard-coded absolute path that breaks reproducibility, insufficient computational effort (Nmif = 50, Np = 2000, only 50 global replicates), and a SARIMA period misspecification. Many POMP best-practice items from Wheeler et al. (2024) are unmet.

---

## Major Issues

### 1. No quantitative comparison between SARIMA and POMP models

The paper's stated goal is to "compare and contrast the performances of an ARIMA and POMP model," yet no quantitative comparison is provided. The SARIMA log-likelihoods and the POMP log-likelihoods are never placed side by side. The text acknowledges the SARIMA model fits less well for the second wave based only on visual inspection. Wheeler et al. (2024) emphasize that "visual comparisons alone are only a weak and informal measure of goodness-of-fit." The comparison should be made quantitatively — for instance by evaluating the SARIMA model's log-likelihood and the POMP model's log-likelihood on the same data and scale, or via AIC/BIC, so readers can judge whether the POMP model represents a genuine improvement.

### 2. Broken R-code step function with undefined variables and wrong argument signatures

The plain-R version of `siqriqr_step` (lines 448–467 of the Rmd, before the Csnippet version) contains multiple bugs that would prevent execution:

- `rbinom` is called without the required `n=1` argument (e.g., `dN_RI_b = rbinom(R_o, 1-exp(...))` is missing `n=1`).
- `dt` is used as a time increment inside the plain-R function, but the argument is named `delta.t`; `dt` is undefined.
- The state updates reference `dN_SE_o` and `dN_SE_b` which are never computed anywhere in the function; the function computes `dN_SI_o` and `dN_SI_b` instead, so the subtraction `S = S - (dN_SE_o + dN_SE_b)` would throw an error.
- The function does not return any values, so calling it would silently produce no output.

Although the Csnippet version that follows appears syntactically more consistent, the plain-R version is presented as an intermediate implementation step and its errors are never acknowledged. This calls into question whether the code was tested before submission.

### 3. Hard-coded absolute path breaks reproducibility

The POMP section reads the data with:

```r
read_csv(paste0("C:/Users/USER/Desktop/Time Series Analysis/Projects/TW_last_days.csv"))
```

This path is specific to one author's Windows machine and will fail on any other system. The code-supplement checklist (Wheeler et al. 2024; code supplement standards) explicitly flags hard-coded paths to the author's local filesystem as a critical reproducibility failure. The data file `TW_last_days.csv` is present in the project folder, so a relative path would work; the absolute path was never updated before submission.

### 4. No profile likelihoods or confidence intervals for any parameter

Neither the local search nor the global search section reports profile likelihoods, and no confidence intervals are given for any parameter. Wheeler et al. (2024) specify profile likelihoods as essential for assessing whether parameters are identifiable. The global search pairs plot shows considerable scatter in several parameters (notably `Beta_or`, `Beta_r`, and `eta`) at the high-likelihood region, but no formal identifiability assessment is performed. Without profile likelihoods, the reported point estimates have no attached uncertainty and may be unreliable.

### 5. Insufficient computational effort — too few iterations and replicates

The IF2 searches use `Nmif = 50` and `Np = 2000` throughout, and the global search uses only 50 starting replicates. The convergence traces shown for the local search reveal that several parameters (especially `eta`) have not converged after 50 iterations. The text acknowledges that eta "Does not seem to converge," yet no additional computational effort is deployed to address this. Wheeler et al. (2024) note that log-likelihood improvements are often "primarily attributed to increasing the computational effort." With `Nmif = 50`, it is plausible that the reported best log-likelihood is far from the MLE, making all downstream parameter summaries unreliable.

### 6. SARIMA period misspecification in `auto.arima`

The data are daily, but `ts()` is called with `frequency = 52`:

```r
ts_data1 <- ts(tw_df_first$new_confirmed, frequency = 52) # for weekly data
```

Daily data with weekly seasonality should have `frequency = 7`. Setting `frequency = 52` tells `auto.arima` that there are 52 observations per seasonal cycle, which is appropriate for weekly observations of yearly data (52 weeks per year), not for daily observations with a 7-day cycle. The seasonal component selected by `auto.arima` is therefore potentially incorrect for both phases. The seasonal period of 7 that the authors identify from ACF plots at lags 7, 14, 21 is inconsistent with the `frequency = 52` used in model fitting. This affects both the `auto.arima` selection and the interpretation of results.

### 7. The accumulator variable H tracks recoveries, not quarantined cases — a conceptual mismatch

The measurement model links observations (`reports`) to `rho * H`, where `H` accumulates departures from `Q_o` and `Q_b` (i.e., recoveries from quarantine). However, reported COVID-19 cases typically correspond to newly detected infections entering quarantine, not to recoveries from it. This mismatch between the biological interpretation of H and what the data actually measures is never discussed, and it could distort parameter estimates (particularly `rho` and the transition rates). The data should instead accumulate entries to the Q compartments (i.e., `dN_IQ_o + dN_IQ_b`) rather than exits.

### 8. No benchmark comparison between the POMP model and a non-mechanistic statistical model

Wheeler et al. (2024) recommend comparing mechanistic model fits against non-mechanistic baselines (e.g., ARMA, auto-regressive negative binomial) using quantitative log-likelihood or AIC comparisons. While the paper does fit a SARIMA model, the comparison is never made numerically, and the SARIMA likelihood and POMP likelihood are evaluated under different observation models on different data representations. A proper benchmark would involve fitting, for example, a negative binomial autoregression to the same 174-day case count series and comparing its likelihood directly to that of the POMP model.

### 9. Model diagnostic checks are absent

No model diagnostics are presented for the POMP model. There are no:
- Conditional log-likelihood plots to identify periods of poor fit.
- Effective sample size (ESS) traces to check for particle filter degeneracy.
- Simulations conditioned on observed data (filtering distribution) compared to forward simulations.
- Summary statistics (e.g., peak timing, peak height) comparing simulated and observed distributions.

The only visual diagnostic is a forward simulation from initial guesses before fitting. Wheeler et al. (2024) use conditional log-likelihood plots to identify misspecification events (e.g., a hurricane-driven surge) that motivated model improvements. Without these diagnostics, model adequacy cannot be assessed.

### 10. The `Beta_or` parameter appears in `paramnames` but is never used in the Csnippet

The Csnippet defines transitions using `Beta_o`, `Beta_b`, `Beta_r`, but `Beta_or` is listed in `paramnames` (line 552–554) and is included in the initial parameter vector (line 559) and in `rw.sd` (line 598). It does not appear in any transition expression in the Csnippet. This orphaned parameter inflates the model's apparent dimensionality, wastes computational degrees of freedom, and may cause the optimizer to follow gradients that have no effect on the likelihood — contributing to apparent non-convergence.

---

## Minor Issues

### 11. Confusion about which strains are modeled

The SIQRIQR model write-up uses the label "O" for Omicron and "B" for Beta, but the introduction states that the first wave corresponded to Delta, not Beta, and the second wave to Omicron. The model's state-space description (lines 419–430) refers to "beta variant" for `I_b`, `Q_b`, `R_b`, and then contradicts itself by also calling these subscript-B variables the "first variant" in one sentence. The compartment naming is inconsistent with the epidemiological narrative.

### 12. `%do%` used instead of `%dopar%` for the local search

The local search uses `%do%` (serial execution) while the global search uses `%dopar%` (parallel execution). With 20 replicate chains, serial execution significantly increases compute time. Given that convergence is already marginal at `Nmif = 50`, this choice reduces the practical feasibility of running more replicates or more iterations.

### 13. The AIC table for Phase 1 uses non-seasonal ARIMA, not SARIMA

The AIC table function fits `arima(data, order=c(p,1,q))` without a `seasonal` component, so it selects orders for a plain ARIMA(p,1,q) without any weekly seasonality. The authors justify fitting a WARIMA (weekly-seasonal ARIMA) on the basis of ACF patterns at lag 7, but the AIC table does not evaluate models with a seasonal component. The comparison between `auto.arima`'s suggestion (4,1,1 with seasonal terms) and the AIC table's suggestion (3,1,5 without seasonal terms) is therefore across non-comparable model classes.

### 14. No reported log-likelihood values in the text

Despite running both local and global searches, the final section only prints the top-10 parameter vectors and their log-likelihood values programmatically but never quotes the best log-likelihood in the prose. The text states "global search provides a better log-likelihood" without specifying the value. The best log-likelihood and its standard error should be stated explicitly to allow assessment of model fit and comparison across models.

### 15. Typographical and notational errors

- Line 167: "acll" should be "call."
- Line 380: "fous" should be "focus."
- Line 413: "dtrains" should be "strains."
- The model description mixes notation: `mu_QR_r` appears in the parameter list but is never defined as a transition rate in the biological description. Parameters `mu_QR_o` and `mu_QR_b` are defined twice in the list with different descriptions.
- The `siqriqr_init` function sets `Q_o = 100` as a fixed value regardless of population size or initial conditions, but this choice is never justified.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dataset-substitution-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-indexing-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-guess-stratification-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-rw-sd-drift-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project13/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project13/TW_last_days.csv`
