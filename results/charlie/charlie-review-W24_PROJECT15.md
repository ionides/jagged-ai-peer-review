# Peer Review: W24 Project 15
## "Analysis of Middle-East Respiratory Syndrome coronavirus in Saudi Arabia"

---

## Summary

This project analyzes weekly MERS-CoV case data from Saudi Arabia (January 2014 to May 2016) using two complementary approaches: an ARMA benchmark and a SEIRS POMP model. The SEIRS model treats camel-to-human spillover as the primary infection pathway, following Lin et al. (2018), with camels as the hidden state population. The authors successfully implement likelihood-based inference using iterated filtering (IF2) in the `pomp` package, conduct both local and global searches, and profile the spillover rate parameter. While the project demonstrates genuine engagement with POMP methodology and produces a model that beats the ARMA benchmark, several critical issues undermine the validity of the conclusions: the measurement model contains a fundamental inconsistency between `dmeas` and `rmeas`, the profile likelihood is truncated at the boundary of its search grid, the LRT between ARMA and SEIRS is statistically invalid, and parameter identifiability is acknowledged but not adequately resolved.

---

## Major Issues

### 1. Inconsistency between `dmeas` and `rmeas` in the measurement model

The density function (`dmeas`) and the simulation function (`rmeas`) implement different observation models, which is a direct reproducibility and correctness failure.

In `dmeas` (line 426):
```
lik = dnbinom_mu(reports, k, rho*C, give_log);
```
This evaluates the likelihood that `reports` equals the raw count of primary camel-infected human cases, scaled only by the reporting rate `rho`.

In `rmeas` (lines 429-432):
```
int total_to_primary = 4;
reports = total_to_primary * rnbinom_mu(k, rho*C);
```
This multiplies by 4 to convert primary cases to total human cases. The observation model in `dmeas` never applies this factor of 4.

As a result, the likelihood is evaluated as though the data are primary cases alone, while the simulations (used visually to assess fit) produce total human cases. The model is fitting a different quantity than it is simulating, making the visual fit comparisons misleading and the reported log-likelihoods uninterpretable in terms of the stated observation model. Wheeler et al. (2024) document this exact class of code-text discrepancy as a concrete reproducibility failure. The authors must align `dmeas` and `rmeas` so both operate on the same observable quantity.

### 2. Profile likelihood is truncated at the search boundary

The profile for $\rho_{CH}$ is constructed over [0.0001, 0.001] (line 751), but the authors report that "the $\rho_{CH}$ with the largest log-likelihood is on the edge of the interval (0.001)." This means the MLE lies outside the profiled range. A profile likelihood whose maximum sits at the boundary provides no information about the confidence interval: the reported CI of "approximately 0.001" is simply the upper boundary of the grid, not a statistically meaningful interval.

The authors acknowledge this problem in their text ("We would argue that we may choose a wider range") but do not fix it. The profile should be extended to bracket the true maximum, and the CI should be recomputed from the corrected profile. As it stands, the profile likelihood analysis provides no valid inference for $\rho_{CH}$. (Wheeler et al. 2024, §Parameter identifiability and uncertainty.)

### 3. Likelihood Ratio Test between ARMA and SEIRS is statistically invalid

The LRT comparing ARMA(1,4) (log-likelihood -422.77, 5 parameters) against the SEIRS model (log-likelihood -378.33, 8 parameters) is presented as a formal nested model comparison using the chi-squared approximation of Wilks' theorem (lines 683-697). This test is invalid for two reasons:

First, the two models are not nested in any meaningful statistical sense. The ARMA model is a Gaussian linear time-series model for case counts, while the SEIRS model is a nonlinear stochastic mechanistic model with a negative-binomial measurement model. Wilks' theorem does not apply to non-nested comparisons.

Second, even if the models were treated as nested, the Wilks approximation requires that both models be estimated on the same likelihood scale with identical observation models. Given the `dmeas`/`rmeas` discrepancy described in Issue 1, the SEIRS log-likelihood is not comparable to the ARMA log-likelihood anyway.

The comparison of log-likelihoods as an informal indication of relative fit is reasonable and should be retained, but the formal p-value and chi-squared test should be removed or replaced with an explicit acknowledgment that this is an informal comparison.

### 4. Global search uses only a single IF2 run per starting value (inadequate computational effort)

In the global search (lines 643-657), each of the 400 starting points runs `mif2()` once using inherited settings from `mf1`, followed by `mif2(Nmif=50)`. There is only one IF2 chain per guess, meaning there is no convergence check per starting point. More critically, the second call `mif2()` at line 774 in the profile search is called with no arguments at all — it simply repeats the previous run unchanged, contributing no additional optimization.

The local search itself uses only Nmif=100 iterations. Evidence of convergence requires multiple independent chains from diverse starting values reaching similar likelihoods. The convergence traces show that $\mu_{RS}$ has not converged after 100 iterations, yet this is dismissed as not problematic. Insufficient computation can make a well-specified model appear to fit poorly and undermines the reported MLE. (Wheeler et al. 2024, §Computational adequacy.)

### 5. Initial conditions are partially misspecified: `R` initialization does not sum to `N`

In `seirs_rinit` (lines 417-423):
```
S = nearbyint(eta*N);
E = nearbyint(eta2*N);
I = nearbyint(eta2*N);
R = nearbyint((1-eta-eta2-eta2)*N);
```
The formula for R is `(1-eta-eta2-eta2)*N = (1-eta-2*eta2)*N`. Combined, S+E+I+R = eta*N + eta2*N + eta2*N + (1-eta-2*eta2)*N = N. This is algebraically correct.

However, if `nearbyint` rounding causes S+E+I+R to differ from N by small integer amounts, the constraint S+E+I+R=N is violated silently. No validation is performed. More substantively, the step function adds `dN_Nmu` new susceptibles (births) drawn from `rbinom(N, 1-exp(-mu*dt))`, where N is the fixed parameter. If the actual S+E+I+R total drifts from N, the birth rate becomes decoupled from the living population, breaking the constant-population assumption. This should be checked.

### 6. No model diagnostics beyond ESS: conditional log-likelihoods and filtering simulations absent

The project does not plot per-observation (per-time-step) conditional log-likelihoods from the particle filter, which are the most informative diagnostic for identifying periods of model-data mismatch. The authors note that the model cannot capture the peak around week 80 (line 473) but use only visual trajectory comparison to reach this conclusion.

No filtering-distribution simulations are shown. All simulation plots use forward simulation from estimated initial conditions. Filtering-distribution simulations (conditioned on all data up to each time point) and forward simulations serve distinct diagnostic purposes and should be distinguished. (Wheeler et al. 2024, §Model diagnostics; Simulation-study checklist §10.)

### 7. Profile likelihood constructed using mifs_local[[1]] rather than the global MLE

At line 763, the profile search initializes with `mf1 <- mifs_local[[1]]`, which is the first (not best) result from the local search. The global search identifies a MLE of -378.33, substantially better than the local search results shown in the traces. By initializing the profile from a suboptimal local-search run, the profiled likelihoods may be systematically too low, resulting in a CI that is too wide or incorrectly centered. The profile should be initialized from the global MLE. (Wheeler et al. 2024, §Parameter identifiability and uncertainty.)

---

## Minor Issues

- **References section is empty.** The References section at the end of the document contains no entries despite several inline footnote citations to Lin et al. (2018), Shumway and Stoffer (2017), and others throughout the text. These should be compiled into a formal reference list.

- **`rho` is fixed at 1 without justification from data.** The authors state "almost all camel-infected human cases are recorded" as justification for fixing `rho=1`. However, MERS surveillance in Saudi Arabia is known to be imperfect, and reporting rates estimated in the literature are substantially below 1. Sensitivity to the fixed value of `rho` should be assessed, or the justification should cite surveillance data explicitly.

- **The $R_0$ formula omits mortality.** The reproduction number is computed as $R_0 = \beta / \mu_{IR}$ (line 731). In a SEIRS model with non-negligible mortality rate $\mu$ (here $\mu = 1/(52 \times 14)$ per week), the correct formula for the camel-endemic equilibrium is $R_0 = \beta / (\mu_{IR} + \mu)$. Given $\mu_{IR}$ is estimated near 1.75/week while $\mu \approx 0.00137$/week, the correction is negligible numerically, but the formula stated is technically incorrect.

- **ACF/PACF interpretation leading to AR(1) is overconfident.** The conclusion that "the process underlying the data could be modeled as AR(1)" is based solely on the PACF cutting off after lag 1. The AIC table then selects ARMA(1,4), which includes MA(4) terms that are not anticipated by the PACF analysis. The ARMA(1,4) selection should take precedence over the preliminary ACF/PACF-based AR(1) suggestion.

- **Seasonality analysis period of 7 months is dismissed without exploring structural reasons.** The smoothed periodogram identifies a dominant period of approximately 7 months. The authors discard this finding because it does not match common calendar periods, but the MERS literature discusses seasonal patterns linked to camel calving and Hajj pilgrimage timing. A brief engagement with whether 7 months might reflect a biological seasonality would strengthen the analysis.

- **`rw.sd` for $\eta_2$ is 0.0001 in the logit-transformed space, which may be too small.** The random-walk standard deviation for `eta2` is set to `ivp(0.0001)` (line 545). Since `eta2` is logit-transformed, this corresponds to an extremely small perturbation on the logit scale for an initial-value parameter that ranges roughly from 0 to 0.01. Nonconvergence of `eta2` traces may be partly attributable to this too-small perturbation rather than genuine weak identifiability.

- **`saudi_mers_params.csv` is written conditionally but read unconditionally.** The code at line 595 reads `saudi_mers_params.csv` inside an `else` branch, but the initial particle filter block (lines 499-518, marked `eval=F`) that creates this file is never executed during normal knitting. If the file does not exist prior to running the Rmd, the local search likelihood evaluation will fail. The dependency chain for pre-computed files is not clearly documented.

- **No `sessionInfo()` or package version documentation.** The supplement does not record R or `pomp` package versions. The `pomp` API has changed substantially across versions and results may not reproduce on current CRAN releases without version pinning. (Code supplement checklist, §Documentation.)

- **Model diagram (`model.png`) referenced but not present in the submitted files.** The Rmd includes `![SEIRS Model Structure](model.png)` (line 374), but only `blinded.Rmd`, `blinded.html`, `Makefile`, and `weekly_clean.csv` are present in the project folder. The figure may be embedded in the HTML but is not archived as a standalone file for reproducibility.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project15/blinded.Rmd`
