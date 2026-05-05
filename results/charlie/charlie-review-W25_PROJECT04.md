# Peer Review: W25 Project 04
**COVID-19 Dynamics in Kerala: ARIMA, VAR, and SEIRS POMP Models**

---

## Summary

This project models weekly COVID-19 confirmed case counts in Kerala, India (119 weeks, February 2020 – May 2022) using three classes of models: ARIMA(5,1,5), VAR(9), and a SEIRS compartmental model implemented in `pomp` with piecewise-constant transmission, reporting, and overdispersion parameters across three epidemic phases. The key contribution is a mechanistic SEIRS model that allows re-infection and time-varying observation parameters, fit via iterated filtering (IF2) with 5,000 particles and 200 iterations. The authors conduct local and global searches and present profile likelihoods for several key parameters.

Strengths include a thoughtful multi-phase model structure, use of particle filter convergence diagnostics, profile likelihood computation for several parameters, an iterative model-development narrative in the appendix, and an available SLURM script indicating HPC-based computation. However, the primary conclusion — that SEIRS outperforms ARIMA based on log-likelihood — rests on an invalid comparison between fundamentally different likelihoods. Additional problems include a biologically implausible best-fit transmission rate for the Omicron phase, incorrect profile likelihood stratification for the eta parameter, the unexplained removal of the best-performing profile result, and initial conditions that break the closed-population assumption.

---

## Major Issues

### 1. Invalid log-likelihood comparison between ARIMA and SEIRS (Conclusion section)

The paper's core conclusion is that the SEIRS model outperforms ARIMA(5,1,5) because its log-likelihood (approx. -1240) is larger than ARIMA's (-1326.52). This comparison is invalid. The ARIMA model is fitted to the *differenced* confirmed-case series (118 observations) under a Gaussian error assumption; its log-likelihood quantifies the probability of the differenced increments. The SEIRS model is fitted to the *raw weekly counts* (119 observations) under a negative binomial measurement model; its log-likelihood quantifies the probability of the observed counts. These are different quantities computed on different data objects with different distributional families, and they cannot be compared on a common AIC or log-likelihood scale. The AIC table in the conclusion section (comparing ARIMA AIC ≈ 2675 vs. SEIRS AIC ≈ 2504) inherits this error. A valid benchmark would use a non-mechanistic model fitted to the same raw counts under the same or a comparable distributional family — for example, an auto-regressive negative binomial model as recommended by Wheeler et al. (2024), whose benchmark comparison in the Haiti cholera study was conducted on exactly this basis.

**Fix:** Replace ARIMA as the benchmark with a model fitted to the raw weekly counts under a negative binomial distribution (e.g., ARMA-NegBin or simple SARIMA on log-counts). Report the log-likelihoods of both models evaluated on the same data and using the same observation distribution.

---

### 2. Biologically implausible b3 parameter estimate in SEIRS Model 1 (Section "Global Search")

The best SEIRS Model 1 parameter has b3 ≈ 0.0024 (transmission rate in the Omicron phase). The implied basic reproduction number for that phase is R0 = b3 / mu_IR ≈ 0.0024 / 0.14 ≈ 0.017 — essentially zero. A pathogen with R0 < 1 cannot sustain an epidemic. This is incompatible with the well-documented Omicron surge in Kerala and with the paper's own observation that "Omicron has a basic reproduction number estimated to be 2–3 times higher than Delta." The authors note b3 is "very small" but claim the model mechanism is too complex to diagnose. They also note b3 is outside the stated global search range of [10, 50], which means the IF2 optimizer drifted far outside the initialization box. This is a sign of a poorly constrained parameter space and possible model misspecification, not a genuine biological signal.

**Fix:** The authors must either explain mechanistically why an effectively zero transmission rate produces a third epidemic wave (and show the latent-state trajectory that drives this), or treat this as evidence of model misspecification and investigate the identifiability of b3. Profile likelihood for b3 should be computed. Lower and upper parameter constraints should be enforced using `parameter_trans()` with appropriate bounding (e.g., log-transformation with bounded initialization) to prevent implausible values.

---

### 3. Profile likelihood for eta uses incorrect stratification variable (Eta_pro.R)

The profile likelihood for the initial susceptible fraction eta is generated in `Eta_pro.R`. In that script, the global search results are grouped (stratified) by `round(mu_IR, 2)` — not by `round(eta, 2)`. This means the starting values for each profile run are binned by mu_IR, not eta. A proper profile likelihood for eta requires sweeping eta over a grid of fixed values (or ensuring starting values uniformly cover the eta range) and optimizing all other parameters for each fixed eta. The result is a pseudo-profile that does not systematically trace the likelihood as a function of eta. While the eta values in the results happen to span (0, 1) due to global search diversity, the coverage is non-uniform and the reported confidence interval (a single-point range) is unreliable.

**Fix:** Recompute the eta profile by creating a uniform grid of eta values (e.g., seq(0, 1, by = 0.02)), running mif2 for each fixed eta with all other parameters free to optimize, and ensuring the profile curve has the expected approximately quadratic shape near the maximum.

---

### 4. Unjustified removal of the highest-likelihood profile result (rho2 profile in SEIRS Model 1)

In the blinded.Rmd code for the rho2 profile (around line 1169), the authors sort the profile results and remove the top row with `arrange(rho_pro, desc(loglik))[-1, ]`. The removed entry has log-likelihood -1233.93, which is approximately 5.5 log-units above the otherwise consistent maximum of -1239.44 seen in the rho1 and rho3 profiles and the global search. The paper attributes this discrepancy to "numerical instability" and "potential maximization errors," but no diagnostic evidence is presented to support this claim. A 5.5-unit log-likelihood improvement is a substantial signal that should be investigated, not discarded. Notably, the eta profile independently finds a solution at -1234.25 in the same log-likelihood region, suggesting this region is reproducible. The removal shifts the profile maximum downward and changes the reported confidence interval, potentially making the confidence interval artificially narrow or wide.

**Fix:** Do not remove points from profile likelihood plots without quantitative justification (e.g., excessively high loglik.se). If a point appears anomalous, investigate it as a possible better optimum and update the global search to include this region. Profile confidence intervals should be computed with the true maximum as the reference point.

---

### 5. Insufficient benchmark comparison: no non-mechanistic model on raw counts (Wheeler et al. 2024, Section 2)

The paper uses ARIMA(5,1,5) as a benchmark, but as noted above, this comparison is on a different scale. More fundamentally, the paper does not compare the SEIRS model to any non-mechanistic statistical model evaluated on the same raw weekly counts with an appropriate observation model. Wheeler et al. (2024) document that among 32 published cholera models, not one included such a comparison, and the authors of that study found that some models failed to beat a simple auto-regressive negative binomial. The failure to include a valid benchmark makes it impossible to assess whether the SEIRS model captures meaningful biological structure beyond what a simpler statistical model would achieve.

**Fix:** Fit an auto-regressive negative binomial model (or a comparable non-mechanistic model) directly to the weekly case counts and compare its log-likelihood to the SEIRS model's log-likelihood, both computed on the same 119-observation series.

---

### 6. Parameter estimates suggest model may be near a boundary optimum, but this is not adequately explored (SEIRS Model 1 vs. Model 2 inconsistency)

The profile likelihood analysis for mu_IR reveals two distinct local optima: one near mu_IR ≈ 0.15 (SEIRS Model 1) and one near mu_IR ≈ 0.84–1.17 (SEIRS Model 2). The combined profile (right panel) shows this bimodality clearly. Model 2 was specifically constructed to explore the second region, and it achieves a higher log-likelihood (-1233.21 vs. -1240.03). This multi-modality in a key epidemiological parameter (recovery rate) suggests that the likelihood surface is complex and neither global search can be considered definitive. The paper presents both models but does not conclude which is more reliable or attempt a more exhaustive search. Profile likelihoods for b1, b2, b3, k1, k2, k3, mu_EI, and mu_RS are never computed, leaving parameter identifiability largely unassessed. Wheeler et al. (2024, Section on parameter identifiability) specifically recommend profiling key parameters and treating boundary optima or implausible estimates as evidence of misspecification.

**Fix:** Compute profile likelihoods for the transmission parameters b1, b2, b3 and for mu_EI to assess identifiability. Attempt a combined global search that covers both mu_IR regions simultaneously, rather than treating Models 1 and 2 as separate analyses.

---

### 7. Initial conditions violate the closed-population assumption

The `seir_init` Csnippet sets `S = nearbyint(eta*N)`, `E = 0`, `I = 1000`, `R = nearbyint((1-eta)*N)`. This gives S + E + I + R = eta*N + 1000 + (1-eta)*N = N + 1000, which is 1000 individuals more than the stated population N = 34,530,000. The process model uses N as a fixed denominator in the force-of-infection term (`Beta * I / N`), so the compartments do not sum to N, violating the closed-population assumption stated in the model description. While the absolute discrepancy (0.003%) is small, the inconsistency undermines the mathematical integrity of the model and is trivial to fix.

**Fix:** Change initialization to `I = nearbyint(I0 * N)` for a small fixed fraction I0 (e.g., I0 = 1/N or a small estimated fraction), and set `R = nearbyint((1 - eta - I0) * N)`, ensuring S + E + I + R = N.

---

### 8. Piecewise beta notation error with overlapping time intervals (Model Specification section)

In the mathematical description of the piecewise transmission rate, the paper defines:
- beta(t) = b2 for t in [62, 96]
- beta(t) = b3 for t in [63, 119]

This creates an overlap: weeks 63–96 are assigned to both b2 and b3. The corresponding code uses a covariate-based `interval` variable (with counts 61, 35, 23) and an `if/else if/else` structure, which implements a non-overlapping partition. The code is correct; the mathematical notation is in error. The same overlapping notation appears for k(t) and rho(t).

**Fix:** Correct the piecewise definitions to reflect the actual partition: [1, 61], [62, 96], [97, 119].

---

## Minor Issues

- **Commented-out vaccine data code throughout EDA section:** Lines like `#vaccine <- read.csv(...)` and `#vaccine.ts <- ...` appear multiple times in the rendered document (lines 90–98, 173–175, etc.), creating visual clutter and raising questions about whether the vaccination analysis was planned but abandoned. These should be removed.

- **Figure-caption mismatch:** Figure 4 is captioned "Figure 4: ARIMA(5,1,5) Fitted vs. Actual plot" but the corresponding variable assignment is `fig4 = "**Figure 4.** ..."` and the same variable name `fig4` is used twice (for Figure 3 and Figure 4). This is a copy-paste error that creates confusing cross-references (the text refers to "Figure 5" when describing what is Figure 4).

- **VAR log-likelihood is manually computed (Section "Model Fitting"):** The paper acknowledges computing the VAR(9) log-likelihood manually using the residual covariance matrix because the constant term "prevented direct extraction." This formula produces the Gaussian multivariate log-likelihood and is technically valid for a correctly specified VAR, but it should be noted that the resulting log-likelihood (-3229.10) is not comparable to the ARIMA or SEIRS values, since VAR models three series jointly while ARIMA and SEIRS model only confirmed cases.

- **mu_RS limitation statement is ambiguous:** The conclusion states that "mu_RS = 0.005 for SEIRS model, corresponds to 200 weeks immunity and is generally too large." A larger mu_RS corresponds to *faster* waning immunity (shorter duration). If the authors tried to increase mu_RS (e.g., to 0.02 for 50-week immunity) and obtained poor results, the limitation is that the model requires very slow immunity waning, not that the rate is "too large." The intended meaning should be clarified.

- **Profile scripts use copy-paste structure with inconsistent group-by variables:** `Eta_pro.R`, `muir_pro.R`, and `Rho3_pro.R` all begin with `group_by(cut=round(mu_IR, 2))`, which was correct only for the mu_IR profile. The copy-paste origin of these scripts without updating the stratification variable is a coding quality issue. A comment in `Eta_pro.R` even reads "Fixed variable name from rho_pro," acknowledging this history.

- **No pomp or R package version information provided:** The reproducibility checklist for POMP manuscripts requires pinning the `pomp` package version, as API changes across versions can break code silently. No `sessionInfo()` output or `renv` lockfile is present in the submission.

- **Global Search 2 has half the starting points of Global Search 1 (400 vs. 800):** The second global search uses fewer starting points despite exploring a different, newly-identified region of parameter space. Since Model 2 achieves the overall best log-likelihood, the asymmetry in computational effort is not well justified.

- **ARIMA frequency argument is inconsistent with weekly data:** The time series is specified as `ts(weekly_df$Confirmed, frequency = 7, start = c(2020, 31))`. For weekly data, `frequency = 1` (one observation per period) or `frequency = 52` (52 weeks per year) is conventional; `frequency = 7` implies daily sub-periods within a week, which creates incorrect x-axis labels and potentially affects how `forecast::Arima` handles the series.

- **No out-of-sample or holdout evaluation for any model:** The paper trains all three model types on the full dataset and evaluates in-sample fit only. A held-out evaluation period (e.g., the last 10 weeks) would provide a more objective comparison of predictive accuracy.

- **b3 outside stated global search range:** The paper states the global search for b3 spans [10, 50], but the best SEIRS Model 1 result has b3 ≈ 0.0024, far below the lower bound. IF2 is allowed to move parameters outside the initialization box via the random-walk perturbations and log-transformation. The authors note b3 converges to near zero during local search but do not acknowledge that the final result lies outside the stated search range, which would alert readers to the optimizer's behavior.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/seirs_k_rho.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Global_Rho.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Eta_pro.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/muir_pro.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Rho3_pro.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/rjob_runner.sbat`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Global_rho_800.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Rho1_profile_800.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Rho2_profile_800.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/Eta_profile_800.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_varying_k_rho/muir_profile_800.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_global2/seirs_k_rho.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_global2/Global_rho_jump.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W25/project04/results/seirs_global2/muir_profile.csv`
