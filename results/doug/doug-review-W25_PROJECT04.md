# Peer Review: W25 Project 04
## COVID-19 Epidemic Modeling in Kerala: ARIMA, VAR, and SEIRS POMP Analysis

---

## Summary

This project models weekly COVID-19 confirmed cases in Kerala, India (Feb 2020 – May 2022) using three successive approaches: ARIMA(5,1,5), VAR(9), and a SEIRS POMP model with piecewise time-varying transmission rates, reporting rates, and dispersion parameters. The primary strength is the substantive model-development narrative, which motivates adding time-varying k and rho through iterative model comparison and shows genuine engagement with parameter interpretability. Two global searches and follow-up profile analysis reveal a bimodal likelihood surface in mu_IR that is scientifically interesting. However, the project is undermined by a set of serious methodological errors concentrated in the profile likelihood analysis, a fundamental problem with the accumulator variable semantic, invalid cross-model log-likelihood comparisons, and the global search initialization anti-pattern. These errors collectively invalidate the stated confidence intervals and weaken the model-comparison conclusions.

---

## Major Issues

### 1. All profile likelihoods are pseudo-profiles: the profiled parameter is never fixed

The profile scripts (Eta_pro.R, muir_pro.R, Rho3_pro.R) do not hold the profiled parameter fixed at a grid of values during optimization. Instead, each script groups the global-search results by `round(mu_IR, 2)` — regardless of which parameter is being profiled — and then runs `mif2()` with a `rw.sd` that assigns non-zero perturbations to the profiled parameter (e.g., Eta_pro.R line 28 includes `rho1=.02, rho2=.02, rho3=.02, mu_EI=0.005, mu_IR=0.005` but has no entry for `eta` at all in rw.sd, and critically does not set `eta=0` to fix it). The parameter is therefore free to drift throughout the search.

Inspection of the saved CSV artifacts confirms this: the "Eta_profile_800.csv" contains 98 distinct values of eta (rounded to 2 decimal places) across 443 rows — far more than any fixed profile grid. Similarly, the Rho3 profile contains 63 distinct values of rho3, and the Rho2 profile contains 27 distinct values of rho2. None of these represent a true profile likelihood.

The consequences are severe:
- The chi-squared CI cutoffs (`max(loglik) - 0.5 * qchisq(df=1, p=0.95)`) applied to these scatter plots have no valid statistical interpretation, because the plotted curves are not profile likelihoods.
- All reported confidence intervals (Table for rho1, rho2, rho3, eta, and mu_IR) are invalid.

The fix: For each profiled parameter, construct a grid of fixed values using `profile_design()` or a manual `seq()`, run a separate `mif2()` call at each grid point with the profiled parameter excluded from `rw.sd` (perturbation explicitly set to zero), and evaluate the log-likelihood via `logmeanexp` over replicated `pfilter()` calls. Apply the chi-squared threshold against the global maximum log-likelihood. See Wheeler et al. (2024), Section on parameter identifiability and uncertainty.

### 2. Profile guess stratification is wrong for all profile computations

Beyond the rw.sd drift error, all three profile R scripts stratify starting guesses by `round(mu_IR, 2)` regardless of which parameter is being profiled. Eta_pro.R profiles eta but groups by mu_IR (line 17: `group_by(cut=round(mu_IR,2))`). Rho3_pro.R profiles rho3 but also groups by mu_IR. muir_pro.R at least groups by mu_IR while profiling mu_IR, making it the only one where the stratification is consistent with the target — though the rw.sd still includes mu_IR with a non-zero perturbation (0.005 in muir_pro.R line 28 would need to be 0 for a true profile).

Stratifying guesses by a parameter other than the profiled parameter does not guarantee coverage of the target parameter's range. The profile plots may therefore have uneven or sparse coverage over the profiled parameter axis, making CI bounds artifacts of coverage gaps.

### 3. Global search initialization inherits state from local search chain

In Global_Rho.R (the script generating Global_rho_800.csv), the global search initializes each replicate as `mf1 |> mif2(params=c(guess,fixed_params))` where `mf1 <- mifs_local[[1]]` (line 124-131). Passing a previous mif2 result object as the first argument to `mif2()` causes the global search to inherit the cooling schedule from the completed local chain. The cooling schedule for mifs_local[[1]] is already at or near its terminal cooling state after 200 iterations with `cooling.fraction.50=0.5`, so the global search effectively performs very few functional IF2 iterations from each new random starting point before perturbations shrink to near zero. The reported "global maximum" may therefore be the same local optimum reached from different starting points without genuine global exploration.

The fix: replace `mf1 |> mif2(params=c(guess, fixed_params))` with `COVID_SEIR |> mif2(params=c(guess, fixed_params), Np=NP, Nmif=NMIF, cooling.fraction.50=0.5, rw.sd=step_size, ...)` using the base pomp object. See the pomp-global-search-init-audit skill for details.

### 4. Accumulator variable H accumulates recoveries rather than new infections

In the SEIRS Csnippet (`seirs_k_rho.R` line 47: `H += dN_IR`), the accumulator variable H counts individuals transitioning from I to R (recoveries). However, the observation data (`weekly_df$Confirmed`) records newly confirmed infections, which epidemiologically corresponds to transitions into the infectious class (I) or newly detected cases — not recoveries out of it. This semantic mismatch means the measurement model `Y(t) ~ NegBin(rho * H, ...)` links reported cases to the number of people leaving the infectious compartment, not the number entering detection.

In an SEIRS model with mean infectious period 1/mu_IR (estimated at ~1 week in Model 2), the flows dN_EI and dN_IR are closely correlated at scale, so the model may still produce plausible-looking trajectories. However, the estimated reporting rate rho will absorb the ratio between recoveries and actual new cases, and parameter estimates for mu_IR will be distorted to compensate. All downstream policy conclusions about transmission rates and reporting rates are potentially unreliable.

The fix: change `H += dN_IR` to `H += dN_EI` in the seir_step Csnippet to accumulate new infectious cases (I entries) rather than recoveries (I exits), as this better corresponds to newly detected/confirmed cases. Alternatively, use `H += dN_SE` if the data tracks newly exposed individuals. The choice should be justified by how the Kerala surveillance system records cases.

### 5. Invalid log-likelihood and AIC comparison between ARIMA and SEIRS models

The conclusion section (lines 1492–1528) directly compares the log-likelihoods and AIC values of ARIMA(5,1,5) and the two SEIRS candidates. This comparison is statistically invalid because the two model families use fundamentally different observation models: ARIMA assumes a Gaussian error distribution on the differenced series, while the SEIRS model uses a negative binomial distribution on the original weekly count data. Log-likelihoods from these two models are not on the same scale and cannot be compared numerically or via AIC.

Concluding that "both SEIRS candidates have significantly larger log-likelihood and smaller AIC values" is therefore not a valid model comparison. Wheeler et al. (2024) note that even visually plausible models can have substantially lower likelihoods — but this applies only when the likelihoods are evaluated under the same observation model.

The fix: evaluate both models under a common observation model and the same untransformed data (e.g., fit an auto-regressive negative binomial to the count data and compare its log-likelihood to the SEIRS log-likelihood), or use a proper scoring rule such as CRPS that does not require matching distributions. See Wheeler et al. (2024), §Benchmark comparison, and the sarima-baseline-audit skill.

### 6. mu_RS is fixed at a biologically implausible value with no sensitivity analysis

The immunity loss rate mu_RS is fixed at 0.005 per week throughout all analyses (corresponding to approximately 200 weeks, or ~3.8 years, of immunity). The authors acknowledge this is "generally too large" (line 1544) and note that they tried other values but observed poor convergence. However, there is no sensitivity analysis showing how results change with different mu_RS values, and the parameter is effectively removed from estimation without formal justification.

The consequence is that the R->S pathway is nearly closed, making the model behave similarly to a standard SEIR (without re-infection) for the observation window. This undermines the stated scientific motivation for choosing SEIRS over SEIR — namely, to allow re-infections due to waning immunity during the Omicron wave.

### 7. No non-mechanistic statistical benchmark for the SEIRS model

The project compares the SEIRS model against ARIMA, but this comparison is invalid (see Issue 5). A valid benchmark comparison requires fitting a non-mechanistic model with the same observation model (e.g., an auto-regressive negative binomial) to the confirmed case counts and comparing log-likelihoods on the same scale. Wheeler et al. (2024) found that none of the 32 papers in their COVID literature review performed such a comparison, and that some mechanistic models failed to outperform the statistical benchmark — a critical diagnostic for whether the mechanistic model adds genuine value. The authors should provide this comparison before claiming the SEIRS model is the best candidate for the data.

---

## Minor Issues

### 8. Piecewise interval definition contains a typographical error

In the piecewise functions for beta(t), k(t), and rho(t) (lines 688–707), the third interval is stated as `t ∈ [63, 119]` but should be `t ∈ [97, 119]` (following the second interval `t ∈ [62, 96]`). The code correctly implements `interval = c(61, 35, 23)` with the covariate table, so this is a documentation-only error rather than a computational one, but it may confuse readers and should be corrected.

### 9. The time series frequency is set incorrectly for ARIMA analysis

The ts objects are created with `frequency = 7` (lines 161, 164, 167, 188, 221), which R interprets as 7 observations per "year" unit. Since the data is weekly (52 weeks per year), the correct setting is `frequency = 52` for seasonal modeling purposes. With `frequency = 7`, the `start = c(2020, 31)` argument means week 31 of a 7-period cycle, not week 31 of 2020. Although the non-seasonal ARIMA model used here is not affected by this misspecification (there are no seasonal components), the spectral analysis (periodogram with `frequency = 7`) will display frequencies incorrectly, and the ACF/PACF lag labels will be in units of "7-unit years" rather than weeks.

### 10. The rho2 profile plot drops the highest-likelihood row without justification

In the rho2 profile computation (blinded.Rmd line 1169): `rho_pro = arrange(rho_pro, desc(loglik))[-1, ]`. The highest log-likelihood row is silently dropped. The same operation is applied in the eta profile (line 1225) and in seirs_global2 local results (line 1329). No explanation is given for why the best result is excluded. If this is intended to remove an outlier, it should be justified; if it is an artifact of a scripting error (perhaps to remove a header row), it should be investigated and fixed, since it artificially lowers the maximum used for the chi-squared CI reference.

### 11. Initial infected count is fixed at I(0) = 1000 without justification

The initial condition sets I = 1000 at t0 (seir_init Csnippet). With Kerala's population of 34.5 million, this corresponds to an initial infection prevalence of approximately 0.003%. No justification or sensitivity analysis is provided. The choice of initial conditions can substantially affect the likelihood (Wheeler et al. (2024) note an AIC difference of ~72 units from initialization choices in their analysis). At minimum, I(0) should be estimated or a sensitivity analysis should be presented.

### 12. The VAR log-likelihood is manually computed using an approximation

The log-likelihood for the VAR(9) model (lines 480–483) is computed manually using the formula for a multivariate Gaussian: `-(n*k/2)*log(2*pi) - (n/2)*log(det(Sigma_u)) - (n*k/2)`. This approximation treats the residual covariance as exact rather than accounting for parameter uncertainty in the coefficient matrix, and uses `Sigma_u` from the OLS summary rather than the MLE. The text acknowledges that direct extraction from the model was prevented by the presence of a constant, but the manual formula produces an approximate value and should be noted as such rather than presented without qualification.

### 13. The ARIMA model selection ignores parsimony: ARIMA(5,1,5) near non-invertibility

The stability check for ARIMA(5,1,5) notes that several MA roots lie "near or on the boundary" of the unit circle (line 373). Near-unit-root MA components indicate poor conditioning of the optimization problem and may reflect overfitting. The paper acknowledges that ARIMA(3,1,3) has nearly the same AIC but does not follow up on why ARIMA(5,1,5) is preferred despite the invertibility concern. A model selection criterion that penalizes near-boundary roots (or a simpler model selection procedure) should be considered.

### 14. Figure cross-referencing errors

The paper labels Figure 4 in the caption text as "Figure 4" but the figure produced is described in text as "time series plot (Figure 5)" (line 311). Similar numbering inconsistencies appear throughout (e.g., `fig4 = "**Figure 3.**..."` for what is labeled fig3). These variable assignments to figure captions do not affect the rendered output captions but indicate the caption text is not synchronized with the chunk labels.

### 15. ChatGPT use disclosure lacks specificity

Reference [20] credits ChatGPT as "used for debugging and proof-reading" with no specifics about which analyses, code sections, or text passages were generated or revised with AI assistance. Some journals and course policies require more detailed disclosure of AI use, including whether AI-generated code was incorporated directly into the analysis pipeline.

---

## Files Consulted

**Skill files:**
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
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-pseudo-profile-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-pre-global-seed-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`

**Project files:**
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/seirs_k_rho.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Global_Rho.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Eta_pro.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/muir_pro.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Rho3_pro.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Global_rho_800.csv` (inspected via R)
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Rho1_profile_800.csv` (inspected via R)
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Rho2_profile_800.csv` (inspected via R)
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Rho3_profile_800.csv` (inspected via R)
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Eta_profile_800.csv` (inspected via R)
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/muir_profile_800.csv` (inspected via R)
