# Peer Review: W21 Project 11
**"Modeling COVID-19 Cases in Michigan: ARMA model v.s. SEIR POMP model"**

---

## Summary

This project fits an ARMA model (to HP-filtered data) and a stochastic SEIR POMP model to daily COVID-19 case counts in Michigan during the "winter spike" (October 1, 2020 -- February 1, 2021). The stated goal is to compare the two approaches. While the project correctly implements the particle filter and iterated filtering (IF2) framework and provides genuine convergence traces, it suffers from a critical semantic mismatch between the accumulator variable and what the observation data records, a data-smoothing/measurement-model incompatibility, a global-search initialization error that anchors exploration near the local-search solution, and a systematic absence of quantitative model diagnostics. The paper also lacks any non-mechanistic benchmark comparison on the same scale, profile likelihoods, or biological corroboration of parameter estimates. The ARMA model is fitted on a transformed (HP-filtered) series that is incommensurable with the SEIR log-likelihood, so the paper's central comparison is not supported by valid evidence.

---

## Major Issues

### 1. Accumulator variable accumulates recoveries, not new reported cases

In the Csnippet, `H += dN_IR` — that is, H accumulates transitions from the I compartment to R (recoveries). The measurement model then sets `lik = dbinom(reports, H, rho, give_log)`, linking observed new reported COVID cases to the count of recoveries per day. The data records newly confirmed COVID-19 infections; the natural accumulation for that quantity is `dN_EI` (new symptomatic cases) or `dN_SE` (new exposures), not `dN_IR`. Because recovery follows infection by the infectious period (here ~5--10 days), this mismatch distorts the timing structure of the model and systematically biases all transition-rate estimates. The reporting rate `rho` absorbs the ratio of recoveries to new detections, not the true detection fraction. This is a fundamental specification error that invalidates all parameter estimates and the reported log-likelihoods. (POMP checklist §12; `pomp-accumvar-semantic-audit`.)

**Fix**: Replace `H += dN_IR` with `H += dN_EI` (or `H += dN_SE` if E represents the pre-symptomatic detected pool), and re-run all inference.

---

### 2. Smoothed data (7-day rolling average) fed to a binomial measurement model

The POMP model is fitted using `Cases_RA` (a 7-day rolling average of daily counts) as the observation series. The `dmeasure` Csnippet evaluates `dbinom(reports, H, rho, give_log)`. The binomial distribution requires its first argument to be a non-negative integer; a rolling average of integers is generally fractional. Passing fractional values to `dbinom` in C either silently returns zero or evaluates at the floor, making the particle filter log-likelihood incorrect at every observation time. Additionally, consecutive observations of the rolling average are autocorrelated by construction, violating the conditional independence assumption underlying the factored POMP likelihood. The observation series passed to the POMP model should be the raw daily case counts, not the 7-day smoothed series. (`pomp-smoothed-data-measurement-mismatch`.)

**Fix**: Replace `Cases_RA` with the raw daily case counts as the observation variable for the POMP model. If smoothing is desired for visualization, apply it only to plots, not to the data argument of `pomp()`.

---

### 3. Global search initialized from previous mif2 result, not from the base pomp object

The global search code sets `mf1 <- mifs_local1[[1]]` and then inside the foreach loop calls `mf1 %>% mif2(params=c(unlist(guess),fixed_params))`. Passing `mf1` -- a completed IF2 result object -- as the first argument to `mif2()` inherits the cooling schedule from `mifs_local1[[1]]`, which is already at or near its final (heavily cooled) state after 50 iterations. Each global replicate therefore starts with near-zero perturbations, making the random starting parameters in `guesses` largely ineffective as diverse initializations. The "global search" in effect performs another highly cooled local search near the solution found by `mifs_local1[[1]]`. The claimed global coverage of the parameter space is not achieved. (`pomp-global-search-init-audit`.)

**Fix**: Replace `mf1 %>% mif2(params=...)` with `covSEIR %>% mif2(params=...)` in the global search foreach loop, where `covSEIR` is the base pomp object. This ensures each replicate starts from fresh cooling.

---

### 4. No quantitative benchmark comparison

The paper compares an ARMA(2,2) model fitted to HP-filtered case counts with a SEIR POMP model fitted to the smoothed rolling-average series. These two models have different observation variables (HP-filtered residuals vs. smoothed counts), different distributional families (Gaussian vs. binomial), and different data transformations. Their log-likelihoods are therefore on entirely different scales and cannot be numerically compared. The paper does not compare the SEIR model against any non-mechanistic statistical benchmark (e.g., auto-regressive negative binomial) fitted to the same raw data with the same observation model. Without such a comparison, it is impossible to assess whether the mechanistic SEIR structure captures meaningful dynamics beyond what a simple statistical model would achieve. (Wheeler et al. 2024, §Benchmark comparison; POMP checklist §2.)

**Fix**: Fit an ARIMA or negative-binomial autoregressive model directly to the raw daily case counts, evaluate its log-likelihood on the same data and measurement model, and compare quantitatively to the SEIR log-likelihood.

---

### 5. No profile likelihoods; parameter identifiability not assessed

No profile likelihoods are computed for any parameter. The convergence traces show that `mu_EI` converges to near zero (infinite latency), `Beta` varies widely between 0.3 and 0.7, and `mu_IR` converges to approximately 0.09. These patterns are acknowledged but not interpreted as potential signs of model misspecification or parameter unidentifiability. Without profile likelihoods, it is impossible to determine whether parameters are identified from the data, and the reported point estimates may reflect a flat or multimodal likelihood surface rather than a unique MLE. (Wheeler et al. 2024, §Parameter identifiability; POMP checklist §5.)

**Fix**: Compute profile likelihoods for the key parameters (`Beta`, `mu_EI`, `mu_IR`, `eta`) using `profile_design()`, with each profiled parameter excluded from `rw.sd` in the profile IF2 calls.

---

### 6. Insufficient computational effort; Monte Carlo standard errors too large

The global search uses only Np=1000 particles and Nmif=50 iterations, with 10 pfilter replicates (via `logmeanexp`) per global replicate. The saved artifact `new_global2.csv` shows loglik.se values ranging from approximately 1 to over 2355 across the 300 global replicates, with the best replicate (loglik = -10,633) having loglik.se of only 1.1. However, many high-likelihood replicates have loglik.se > 100, indicating that the Monte Carlo uncertainty in the likelihood estimate far exceeds the signal. With Np=1000 for a daily COVID series of ~124 observations with up to ~10,000 new cases per day, particle degeneracy is likely at the large-case periods. No evidence is presented that increasing Np was explored. (Wheeler et al. 2024, §Computational adequacy; POMP checklist §6.)

**Fix**: Increase Np to at least 5,000--10,000 for the final reported searches. Use `loglik.se < 1` as a threshold for acceptable Monte Carlo precision, and discard or re-run replicates that do not meet it.

---

### 7. mu_EI convergence to zero is evidence of model misspecification, not reported as such

Both the local and global searches show `mu_EI` converging to values near zero, implying an essentially infinite latency period. The authors note this as "suspicious" but do not interpret it as a sign of model misspecification (e.g., the latency structure being unidentifiable from daily case counts, or the model overparameterizing the incubation-detection pathway). Wheeler et al. (2024) demonstrate that implausible parameter estimates -- such as immunity-loss rate equal to zero or human-to-human transmission equal to zero -- should be interpreted as evidence of model misspecification rather than biological findings. The same reasoning applies here: `mu_EI = 0` is epidemiologically implausible for COVID-19 and warrants reformulation, not acceptance. (POMP checklist §11.)

---

### 8. No model diagnostics (conditional log-likelihoods, ESS, filtering distribution)

The only diagnostic presented is the IF2 convergence trace (parameter traces across iterations). There are no: (a) plots of per-observation conditional log-likelihoods to identify specific time periods of poor fit; (b) effective sample size (ESS) monitoring for the particle filter; (c) comparisons of the filtering distribution against forward simulations; or (d) analysis of reconstructed latent states (S, E, I, R trajectories). The authors note that the tails of the series are poorly fit but do not quantify this with conditional log-likelihoods. (Wheeler et al. 2024, §Model diagnostics; POMP checklist §4.)

---

### 9. Reporting rate rho fixed without justification or sensitivity analysis

The reporting rate rho is fixed at 0.1 throughout all analyses, based on a literature citation. However, the cited source (an MIT preprint) provides a range of estimates, and fixing rho at a single value without exploring how sensitive results are to this assumption is a significant limitation. Fixing rho prevents the model from compensating for misspecification in the accumulator variable (see Issue 1) and interacts with the estimation of all other parameters. No sensitivity analysis of the rho assumption is performed. (POMP checklist §12.)

---

## Minor Issues

### 10. HP filter lambda choice is not appropriate for daily data

The Hodrick-Prescott filter is applied with lambda=100, citing a course slide reference for this as "standard practice." However, lambda=100 is the conventional choice for quarterly macroeconomic data; for daily data a much larger lambda (on the order of 10^6 or higher) is typically used to separate trend from cycle. The current choice will over-smooth the trend and leave substantial trend residuals in the "detrended" series passed to ARMA modeling, potentially inflating ARMA model order selection and distorting the stationarity test conclusions.

### 11. ARMA fitted to HP-filtered residuals while POMP fitted to smoothed counts: comparison is invalid

The paper's stated comparison ("ARMA model v.s. SEIR POMP model") juxtaposes two models fitted to fundamentally different observation series (HP-filtered residuals vs. 7-day rolling average counts). Even if individual models were correctly specified, their log-likelihoods cannot be compared because the data, distributional family, and observation scale differ. Any conclusion about relative model adequacy is unsupported.

### 12. Data loaded from a GitHub URL inside the POMP section, bypassing the local CSV

In the POMP section, data is re-read from `https://raw.githubusercontent.com/jeremyny/G6_Final/main/MI_COVID19_data.csv` rather than from the local `covid_data.csv`. If the GitHub repository becomes unavailable or the file is modified, the document will not reproduce. The local file should be used for reproducibility. (Code supplement checklist, Reproducibility.)

### 13. partrans declares logit for Beta, mu_EI, mu_IR but not for eta

The `partrans` argument applies `logit` to `Beta`, `mu_EI`, and `mu_IR` but not to `eta`, which is also a fraction (susceptibility fraction bounded to (0,1)). During IF2, eta is therefore perturbed on its natural scale and can drift outside (0,1), causing invalid probability arguments in `seir_init`. The local search shows eta varying between 0.7 and 0.9, which happens to be within (0,1), but this is not guaranteed. (`pomp-partrans-undeclared-param`.)

**Fix**: Add `eta` to the `logit = c(...)` list in `parameter_trans()`.

### 14. No forecast or policy-relevant prediction from the fitted SEIR model

Given the stated motivation (modeling a pandemic surge in Michigan), the paper would benefit substantially from generating forward predictions from the fitted model (conditioned on the filtering distribution), with uncertainty quantification. No forecast is provided, and the conclusion discusses only parameter interpretation. (POMP checklist §7.)

### 15. Initial conditions for E and I are fixed, not estimated; sensitivity not assessed

E(0) = 90,000 and I(0) = 66,000 are calculated from case counts and fixed. These values depend on the assumed reporting rate (rho=0.1) and the assumed latency period. No sensitivity analysis of these initial conditions is presented. Given that mu_EI converges to near zero in the optimization, the initial E compartment may have an outsized influence on the entire trajectory. (POMP checklist §13.)

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
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
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-param-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-override-bug/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-cross-model-param-reconciliation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-closed-environment-reproducibility-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simulate-as-latent-state-inference/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stew-filename-collision/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-partrans-undeclared-param/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-negligible-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-prediction-wrong-params/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-orphan-paramname-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-wrong-variable-display-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-aic-median-loglik-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-design-variable-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/ode-compartment-observation-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-smoothed-data-measurement-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project11/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project11/cov_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project11/new_global2.csv`
