# Peer Review: W24 Project 04
## "Comparative Analysis of ARIMA and SEIR Models Using COVID-19 Data"

---

## Summary

This project fits both an ARIMA model and a SEIR model to weekly COVID-19 confirmed-case data from Washington State, with the stated goal of determining whether the SEIR model provides a better fit than ARIMA. The project demonstrates familiarity with the `pomp` package and applies several optimization strategies (local Nelder-Mead, simulated-annealing via GenSA). However, the work suffers from fundamental methodological deficiencies: parameter estimation relies entirely on sum-of-squared-differences minimization rather than likelihood-based inference; no log-likelihood or AIC value is ever reported for the SEIR model; the measurement model contains a critical mis-specification (using `dnbinom` with the wrong parameterization and `rbinom` for `rmeasure`); and the comparative conclusion is drawn without a common quantitative metric. The overall analysis falls well short of what is needed to support the paper's central comparative claim.

---

## Major Issues

### 1. Ad hoc calibration instead of likelihood-based inference

The entire SEIR fitting procedure — both the local (Nelder-Mead `optim`) and global (GenSA) optimization stages — minimizes the sum of squared differences between one simulated trajectory and the observed data (see `cost_function` in the "Local search and optimization" and "Global Search and Optimization" chunks). This is not likelihood-based inference. Minimizing SSE from a single stochastic simulation trajectory is neither the likelihood of the SEIR model nor a reliable proxy for it, because a single simulation realization is a noisy draw from the model, not the expected value. Proper likelihood evaluation requires a particle filter to compute the marginal likelihood by averaging over the latent state trajectory. Wheeler et al. (2024) emphasize that ad hoc calibration "makes formal model comparison and uncertainty quantification impossible." The authors cannot claim their parameters are optimal or compare the SEIR and ARIMA models on equal footing using this approach.

**Fix:** Replace the SSE cost function with a particle filter likelihood evaluation using `pfilter()` from the `pomp` package, and use iterated filtering (`mif2()`) or similar plug-and-play methods for optimization.

---

### 2. No quantitative goodness-of-fit metrics reported for the SEIR model

No log-likelihood, AIC, or any other quantitative goodness-of-fit metric is ever computed or reported for the SEIR model in any of its three forms (initial, locally optimized, globally optimized, or "final"). The ARIMA model comparison is made purely on visual grounds and qualitative prose. The conclusion states "both models performed commendably" and implies the SEIR model captures peaks better, but this claim cannot be verified without numbers. Wheeler et al. (2024, §Quantitative goodness-of-fit) state that "visual comparisons alone are only a weak and informal measure of goodness-of-fit." The paper's central research question — which model fits better — is therefore left unanswered.

**Fix:** Compute `logLik` for the best ARIMA model and evaluate `loglik` from `pfilter()` for the SEIR model. Report these values and compare them, ideally via AIC.

---

### 3. Critical measurement model mis-specification

The `dmeasure` Csnippet uses `dnbinom(cases, I, rho, give_log)`, which invokes the base-R parameterization where the second argument is `size` and the third is `prob`. This means the measurement model is NegBinomial(size = I, prob = rho), not a typical epidemiological observation model. When I is large (hundreds of thousands of cases), this yields absurd distributions. More critically, the `rmeasure` Csnippet uses `rbinom(I, rho)` — a binomial draw — which is inconsistent with the declared negative binomial `dmeasure`. This mismatch between `dmeasure` and `rmeasure` means simulated and evaluated likelihoods are derived from different distributional assumptions, corrupting both the visual fit and any likelihood computation. Wheeler et al. (2024) document exactly this type of model-code discrepancy as a reproducibility and validity failure.

**Fix:** Use the `mu`-parameterization consistently: `dmeas` should be `dnbinom_mu(cases, k, rho*I, give_log)` and `rmeas` should be `rnbinom_mu(k, rho*I)`, matching the standard epidemiological formulation used in the course materials referenced by the authors.

---

### 4. Comparison between ARIMA and SEIR is not on a common metric

The paper's stated goal is to compare the ARIMA and SEIR models. The ARIMA model is evaluated using AIC, residual plots, ACF, and QQ plots. The SEIR model is evaluated only by visual trajectory inspection. Since no common quantitative metric bridges the two, the comparison is meaningless. Furthermore, ARIMA's AIC is on a Gaussian log-likelihood scale while any future SEIR likelihood would be on a different observation model scale (negative binomial), so a direct AIC comparison would require the same data and observation model. The conclusion that "the SEIR model… appeared to more naturally capture the specific characteristics" is unsupported.

**Fix:** Define a common evaluation framework. One valid approach is to compute the log-predictive likelihood of both models on a held-out set, or to compare conditional one-step-ahead predictive distributions.

---

### 5. No parameter identifiability assessment or uncertainty quantification

No profile likelihoods, confidence intervals, or even standard errors are reported for any SEIR parameter. The final "manually tuned" parameters (beta = 0.35, sigma = 0.3, gamma = 1/14, N = 5,000,000, rho = 0.5) appear to have been chosen by inspection rather than derived from any formal optimization. The population N is set to 5,000,000 for Washington State despite the global optimizer returning 8,830,174 and the actual Washington population being approximately 7.7 million. Without identifiability analysis, it is unknown whether these parameters are individually estimable from weekly case count data. Wheeler et al. (2024, §Parameter identifiability) require profile likelihoods for key parameters.

**Fix:** Compute profile likelihoods for at least beta, gamma, and rho. Report confidence intervals using the MCAP procedure.

---

### 6. Convergence evidence is absent and the optimization approach is unreliable

The local optimization runs a single Nelder-Mead search from one starting point, and the global optimization runs GenSA once with a fixed seed. There is no evidence of convergence: no likelihood traces across iterations, no comparison of multiple independent searches, no check that increasing computational effort improves the objective. Crucially, the cost function minimizes SSE from a single stochastic simulation, so the objective landscape itself is stochastic and Nelder-Mead convergence to a nominal minimum does not indicate statistical optimality. Wheeler et al. (2024, §Computational adequacy) require multiple searches from diverse starting points and convergence traces.

**Fix:** Run multiple independent searches from random starting points. Report the distribution of final objective values across runs. Show traces of the log-likelihood (not SSE) across iterations.

---

### 7. Final model parameters chosen by manual inspection, not systematic optimization

The "Final SEIR Model" section uses parameters (beta = 0.35, sigma = 0.3, gamma = 1/14, N = 5,000,000, rho = 0.5) that differ from both the locally and globally optimized values with no stated justification. The text says only "we again tuned and derived a SEIR model with predictions closer to the real situation." This is eyeball fitting. It is not statistically principled, cannot be reproduced, and produces results that cannot be interpreted or compared.

---

### 8. Data preprocessing introduces double-differencing and produces nonsensical values

The data preprocessing chunk (lines 611–649) computes `new_confirmed` by first taking daily confirmed-case totals cumulative from the raw data and differencing within weeks (`new_confirmed = confirmed - lag(confirmed)`), then aggregating to weekly sums of these differences (which reconstructs weekly increments). The code then applies a second difference: `weekly_data_diff <- weekly_data %>% mutate(new_confirmed = new_confirmed - lag(new_confirmed))`. This double-differencing means the SEIR model is fitted to the first difference of weekly case counts (i.e., the change in the change), not to the counts themselves. Negative values are possible under this scheme. The EDA section uses different data (downloaded directly from the API) and aggregates `confirmed` (cumulative) by week, producing entirely different values. The modeling data stored in `week.csv` is thus conceptually different from what the EDA visualizes.

---

### 9. EDA SIR models use unestimated, ad hoc parameters

The three EDA SIR models (for California, Washington, New York) use identical hard-coded parameters (Beta = 0.45, mu_IR = 0.1, eta = 0.80, rho = 0.9, k = 1, N = 1,000,000) regardless of region. No fitting is performed. The resulting simulations show "cyclical fluctuations" and S "rapidly falls close to zero," which the authors note is unrealistic, yet no corrective action is taken before moving to the SEIR section. These plots add no analytical value and their presence as EDA is misleading.

---

### 10. Model title mismatch: paper claims SEIR but EDA implements SIR

The paper is titled "Comparative Analysis of ARIMA and SEIR Models" and the SEIR section correctly includes an Exposed compartment. However, the three EDA chunks (pomp1, pomp2, pomp3) implement SIR models without the E compartment. The code defines statenames as `c("S", "I", "R", "H")` with no E state. The text does not acknowledge this inconsistency, creating confusion about what the EDA is actually demonstrating.

---

### 11. No model diagnostics

No particle filter diagnostics are presented: no effective sample size (ESS) plots, no per-time-step conditional log-likelihoods, no filtering distribution comparisons, and no convergence traces from iterative filtering. The project does not use a particle filter at all, so these diagnostics were never generated. As a consequence, there is no way to assess where and how the model fails, or whether specific periods (e.g., the Omicron surge in early 2022) are systematically mis-modeled. Wheeler et al. (2024, §Model diagnostics) require these as standard practice.

---

### 12. Stochastic optimization cost function is unreliable

The cost function used for both local and global optimization calls `simulate(seir_pomp, nsim=1, ...)` and computes SSE relative to the observed data. Because the simulation is stochastic, calling the cost function twice with the same parameters will in general return different values. This means the optimizer is minimizing a noisy, non-deterministic function. The Nelder-Mead and GenSA results are therefore not reproducible even with `set.seed(123)` (which is placed before the GenSA call but after the pomp object is constructed in a different scope), and different runs may yield substantially different parameter estimates.

---

### 13. ARIMA model selection inconsistency

The AIC table identifies ARIMA(2,1,3) as the best model, but the residual diagnostics are produced for ARIMA(3,1,1) (`arima(x = week_ts, order = c(3, 1, 1))`). The final fitted values plot also uses the ARIMA(3,1,1) model. The stated rationale for choosing ARIMA(2,1,3) — that residual plots, ACF, and QQ plots favor it — is never demonstrated, since only ARIMA(3,1,1) diagnostics are shown.

---

### 14. Population parameter N is treated as a free optimization variable but is externally known

The optimization routines estimate N freely with bounds [1, 10,000,000] for GenSA. Washington State's actual population is approximately 7.7 million. Allowing N to be a free parameter without a biologically motivated constraint means the optimizer can compensate for poor structural fit by inflating or deflating the population. The GenSA solution returns N = 8,830,174, about 15% above the actual population, without comment. The local optimizer returns N ≈ 5,031,249, about 35% below. These discrepancies are not discussed or evaluated for biological plausibility as required by Wheeler et al. (2024, §Corroboration with scientific knowledge).

---

### 15. Reproducibility and code quality issues

Several reproducibility failures are present:
- The primary dataset (`2.csv`) referenced in the `eval=FALSE` preprocessing chunk is not included in the project folder. Only the pre-processed `week.csv` is provided, so users cannot verify the preprocessing.
- The EDA chunks download data from an external URL (`storage.covid19datahub.io`). If the URL becomes unavailable, the EDA cannot be reproduced.
- `main.R` contains measles SIR code from the course materials (Consett 1948 data) that is unrelated to the project and appears to have been included by mistake.
- No `sessionInfo()` or package versions are provided. The `pomp` API changes across versions; the measurement model parameterization issue (Issue 3 above) may behave differently on different versions.
- Reference [6] cites ChatGPT for "code optimization and error correction," which is acceptable to disclose but raises concerns given the measurement model errors present in the submitted code.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project04/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project04/main.R`
