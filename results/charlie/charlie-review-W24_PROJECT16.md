# Peer Review: Stats531 Final Project W24 — Project 16
## Modelling of the Influenza cases and spread in the Netherlands using ARIMA and POMP(SEIR) models

---

## Summary

This project fits a dual-branch SEIR POMP model to Netherlands influenza sentinel data from the 2022–2023 season, with the goal of quantifying vaccine effectiveness by estimating separate transmission parameters for vaccinated and unvaccinated subpopulations. The project has genuine scientific ambition — the vaccination stratification idea is mechanistically interesting and directly motivated by public health questions. However, the analysis suffers from several critical methodological failures: the force-of-infection formulation creates two fully isolated epidemic chains with no cross-subpopulation mixing, the MLE parameter estimates are biologically absurd (the vaccinated recovery rate implies a 12-year infectious period), the pseudo-profile likelihood plots are mislabeled and methodologically non-standard without acknowledgment, there is no non-mechanistic benchmark comparison, and the ARIMA section is used rhetorically rather than as a genuine quantitative comparator. These issues undermine the central conclusions about vaccine effectiveness.

---

## Major Issues

### 1. Force-of-infection model treats vaccinated and unvaccinated populations as fully isolated — no cross-transmission

The step function uses `Beta_v * I_v / N` for the vaccinated force of infection and `Beta_u * I_u / N` for the unvaccinated force of infection. This means vaccinated individuals can only be infected by other vaccinated infectious individuals, and unvaccinated individuals can only be infected by other unvaccinated infectious individuals. There is no cross-subpopulation transmission term. In reality, vaccinated and unvaccinated people are part of the same mixing pool: a vaccinated person can be infected by an unvaccinated infectious contact and vice versa. Without cross-terms (e.g., a shared force of infection `(I_v + I_u)/N` or separate but coupled terms), the two SEIR branches are independent epidemic chains that just happen to sum their `H` accumulators. This is not a model of vaccine effectiveness in a shared population — it is two separate epidemics. The main scientific conclusion that `Beta_v < Beta_u` proves vaccination "slows transmission" is not supported by this model structure, because the fitted Beta parameters absorb all the modeling constraints of fully segregated chains.

### 2. MLE vaccinated recovery rate is biologically absurd — a sign of model misspecification

The archived global search results (global_search.rds) show that the maximum log-likelihood is achieved at `mu_IR_v = 0.00151` per week. Since time is in weeks, the implied mean infectious period for vaccinated individuals is approximately 1/0.00151 = 661 weeks, or roughly 12 years. The top 10 results all show `mu_IR_v` well below 0.01 (ranging from 0.00015 to 0.67), while `mu_IR_u` is in a plausible range around 0.66 (infectious period ~1.5 weeks). Influenza infectious periods are typically 3–7 days regardless of vaccination status (CDC guidance). Rather than flagging this implausible estimate as potential model misspecification (as Wheeler et al. 2024 recommend), the paper interprets it as evidence that "vaccinated people that do get sick take longer to recover" — a conclusion entirely unsupported by epidemiological literature and almost certainly an artifact of the non-mixing model structure. The authors should treat this as a red flag for misspecification, not a biological finding.

### 3. No non-mechanistic benchmark comparison

The mechanistic SEIR model is never compared quantitatively against a non-mechanistic baseline. The ARIMA section is used only to argue that ARIMA is inadequate, justifying the pivot to SEIR; the ARIMA log-likelihood is never placed on a comparable scale to the SEIR log-likelihood for a formal model comparison. Wheeler et al. (2024, §Benchmark comparison) identify this as one of the most important checks: "None of the 32 papers in their Haiti cholera literature review performed such a comparison." Without comparing SEIR and ARIMA log-likelihoods on the same data, it is impossible to assess whether the mechanistic model captures meaningful structure beyond simple autocorrelation. The ARIMA(0,1,4) model has an AIC that can be directly compared (after accounting for the different likelihood scale), or an auto-regressive negative binomial benchmark could be constructed. This comparison should be performed.

### 4. Pseudo-profile plots are methodologically non-standard and mislabeled

The plots labeled "profile likelihood" for `Beta_v`, `Beta_u`, `mu_IR_v`, `mu_IR_u`, and the ratio parameters are not true profile likelihoods. A true profile likelihood for parameter `theta` fixes `theta` at a grid of values and maximizes the likelihood over all other parameters at each grid point. Instead, the code filters `profile_results` (the global search output) by `loglik > max(loglik) - 15` or `- 10`, groups by rounded parameter value, and takes the top-2 log-likelihoods per group. This is a pseudo-profile or scatter-filter approach, not profile likelihood maximization. As a result: (a) the confidence intervals implied by the chi-square cutoff line are not statistically valid, (b) the displayed parameter ranges may miss the true profile shape, and (c) the approach is not described in the text at all — readers are shown confidence-interval cutoff lines without any explanation that a non-standard method was used. Additionally, the "profile" for `ratio_beta` and `ratio_mu` (computed as post-hoc ratios of estimated parameters) is not a formal profile likelihood for those derived quantities.

### 5. Global search starting values in run.r conflict with bounds used in Rmd; mu_IR_v MLE is outside the initial search box

In the Rmd, the global search specifies `lower=c(mu_IR_v=0.1, ...)` and `upper=c(mu_IR_v=0.3, ...)`. Yet the MLE from the archived results shows `mu_IR_v = 0.00151`, which is two orders of magnitude below the stated lower bound. This means mif2 optimization drove the parameter far outside the initial search box. Because `mu_IR_v` uses a log transformation (`partrans=parameter_trans(log=c(...,"mu_IR_v",...))`) there is no hard boundary during optimization, but the starting values strongly suggest the authors did not anticipate this region of parameter space. This undiscovered region of the likelihood surface raises the possibility that the global search did not adequately explore the full parameter space, and that better optima might exist. The discrepancy between the search box and the MLE is never acknowledged. Wheeler et al. (2024, §Computational adequacy) stress the importance of diagnosing whether the optimization has genuinely converged.

### 6. No quantitative goodness-of-fit or model diagnostics reported

The paper never presents a model simulation overlaid on the data to demonstrate visual fit. There are no forward simulations from the MLE parameters compared to observed influenza counts. No effective sample size (ESS) traces from the particle filter are shown, which would indicate whether the particle filter is degenerating. No conditional log-likelihood plot is presented. The only "result" output is a scalar maximum log-likelihood (`logmeanexp(profile_results$loglik, se=TRUE)`) quoted as "-189.93" without context — no comparison baseline, no interpretation of what this value implies about fit quality. Wheeler et al. (2024, §Quantitative goodness-of-fit) note that "visual comparisons alone are only a weak and informal measure of goodness-of-fit," but here there is not even a visual comparison from the MLE fit.

### 7. Initialization formula error: text and code give different S_u formula

The text (Section "POMP Model") states the unvaccinated susceptible initial condition as:

$$S_u = \text{vaccinationRate} \times \eta_u \times N$$

However, the code initializes it as `S_u = nearbyint((1-vac_rate) * eta_u * N)`. The text formula is incorrect — it would initialize the unvaccinated group using the vaccination rate rather than its complement `(1 - vaccinationRate)`. Only the code is correct. This is a mathematical description error that undermines confidence in the model specification, as it suggests the written mathematics was not carefully checked against the implementation.

### 8. Incorrect and misleading mif2 local-search parameters in Rmd versus run.r

The Rmd runs local mif2 with `Np=2000, Nmif=300, cooling.fraction.50=0.2` and large random walk standard deviations (`rw.sd` up to 0.15 for Beta). However, the cluster run.r script uses `Np=1000, Nmif=50, cooling.fraction.50=0.6` with much smaller `rw.sd=0.02`. The two scripts implement materially different optimization settings with no explanation of why the Rmd uses different settings than the cluster version that actually generated the archived results. The local search traces shown in the Rmd (Fig. traces) are therefore from a different optimization procedure than the global search, and the relationship between local and global search results is never clarified. The `mf1 <- mifs_local[[1]]` used to seed the global search in the Rmd code is thus from a potentially inconsistent local search.

---

## Minor Issues

### 9. Inconsistency between stated goal and model output

The introduction states the goal is to study "the impact of vaccination on the transmission and progression of influenza, focusing on the differing rates of change and associated risks between vaccinated and unvaccinated populations." However, the model directly parameterizes transmission rates (Beta_v, Beta_u) and recovery rates (mu_IR_v, mu_IR_u) per subgroup without a mechanistic representation of vaccine-induced immunity reduction. The vaccine effectiveness is inferred indirectly from Beta_v/Beta_u ratio post-hoc. A clearer formulation would relate Beta_v to Beta_u via an explicit vaccine efficacy parameter (e.g., `Beta_v = (1 - VE) * Beta_u`), which is both more interpretable and more identifiable.

### 10. The "profile" plots use inconsistent loglik cutoff thresholds (10 vs. 15) without justification

Some plots filter at `loglik > max(loglik) - 15`, others at `- 10`. The statistical meaning of these cutoffs is never explained. The chi-square cutoff line corresponds to the 95% confidence interval threshold for a single parameter (0.5 * qchisq(0.95, df=1) ≈ 1.92 log-likelihood units), but the pre-filtering at 10 or 15 units introduces an asymmetry in display that may artificially truncate the profile tails. No justification for these filtering thresholds is provided.

### 11. The ARIMA section concludes incorrectly that SARIMA is inappropriate based on limited evidence

The text claims "the analysis revealed that the data did not exhibit a consistent seasonal structure when using auto ARIMA with seasonality" and therefore proceeds without SARIMA. However, with only one flu season of data (35 weeks), the absence of detected seasonality is expected and trivial — you cannot detect a seasonal pattern from a single season. The appropriate conclusion is simply that seasonality cannot be estimated from this dataset, not that the data lacks seasonal structure. The discussion of SARIMA failure is misleading.

### 12. Hard-coded absolute path in run.r breaks reproducibility

The file run.r contains `flu <- read.csv("/home/falarcon/stats531/final/Flu.csv", sep=";")` — an absolute path to the author's cluster home directory. This means run.r cannot be executed by any other user without manual path edits. The Rmd uses a GitHub raw URL instead, which is a better practice, but the two scripts read the data differently (semicolon vs. comma delimited in the source), suggesting they may not be equivalent. The code supplement checklist (Wheeler et al. 2024, §Reproducibility) explicitly flags hard-coded absolute paths as a red flag.

### 13. The k (overdispersion) parameter is fixed without justification

The paper fixes `k=10` in all runs. The parameter `k` controls overdispersion in the negative binomial measurement model — fixing it rather than estimating it forces a specific degree of variability. No sensitivity analysis, prior justification, or citation for k=10 is provided. The profile plots do not include k. Given the high variability in influenza case counts, the choice of k can significantly affect both the fit and the model comparison.

### 14. No seed is set before the parallel doParallel local search in the Rmd

The code sets `set.seed(2488820)` early in the document, but then uses `%dopar%` for the local mif2 runs without `registerDoRNG()`. The commented-out line `# registerDoRNG(542451)` in the setup chunk was not activated. Without a registered RNG for parallel execution, the local search results are not reproducible across runs, violating the POMP code supplement checklist requirement for seeded parallel operations.

### 15. Typos and minor presentation issues

- Section heading "Forcast" (line 157 in Rmd) should be "Forecast"; repeated at line 223 ("Forcase").
- The text says "immunocompromized" (line 266); should be "immunocompromised".
- The text says "slighlty" (line 612) rather than "slightly" and "inmuen systems" rather than "immune systems".
- The pairs plot axes include `eta_v` and `eta_u` but these are not discussed in the text analysis, leaving readers without interpretation.
- References list "STATS 531 slides, homeworks, and lectures" without a proper citation format; course notes should at minimum include the instructor, year, and URL.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project16/Blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project16/run.r`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project16/global_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project16/Makefile`
