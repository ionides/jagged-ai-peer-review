# Peer Review: W22 Project 03 — Subscriber Analysis (Twitch Streamer Data)

## Summary

The project analyzes the monthly subscriber trajectory of a single Twitch streamer (Félix Lengyel / xQc) using first an ARIMA(1,1,2) model and then a custom POMP compartmental model with three states (Beginning, Viewers, Subscribers). The ARIMA analysis is workmanlike: differencing, spectral analysis, and ACF/PACF inspection are all performed. The POMP section defines a BVS (Beginning–Viewers–Subscribers) model, runs both a local and global IF2 search, and reports a single log-likelihood of −866.06. While the project demonstrates awareness of POMP methodology, it is severely incomplete: no POMP analysis results are presented beyond one number, the POMP model has multiple critical code errors, the ARIMA–POMP likelihood comparison is invalid, no convergence diagnostics or profile likelihoods are shown, and the scientific motivation for the compartmental structure is unexplained and biologically incoherent. The conclusion that "ARMA performs better" rests on an apples-to-oranges likelihood comparison and on a POMP model whose specification is demonstrably broken.

---

## Major Issues

### 1. Invalid log-likelihood comparison between ARIMA and POMP models

The paper concludes that "the ARMA model performs better than the pomp model" by comparing the POMP log-likelihood of −866.06 to implicit ARIMA log-likelihoods (derivable from the AIC table). This comparison is invalid. The ARIMA model is fit on log-differenced subscriber data under a Gaussian measurement model on the transformed scale. The POMP model is fit on raw subscriber counts (integers) under a Gaussian dmeasure on the count scale. The two likelihoods are not on the same scale and cannot be compared numerically to assess relative fit. Any inference about which model is better based on these numbers is unsupported. A valid comparison would require fitting both models to the same untransformed data under the same observation model, or using a proper scoring rule (e.g., CRPS) evaluated on the original scale. See the sarima-baseline-audit skill; this is the canonical invalid-comparison pattern.

### 2. dmeasure clips the log-likelihood to zero or −100, violating proper likelihood semantics

The `bvs_dmeas` Csnippet contains:

```c
if (lik > 0) { lik = 0; }
if (lik < -100) { lik = -100; }
```

This clipping is applied to the log-likelihood returned by `dnorm(…, 1)`. A genuine dnorm log-density is always ≤ 0, so the first branch is dead code — but it signals confusion about the scale. More critically, clamping lik to −100 when the particle is highly inconsistent with the data prevents the particle filter from correctly downweighting implausible particles. Every particle that falls far outside the data distribution receives the same weight exp(−100) rather than a near-zero weight. This produces an inflated effective sample size for bad parameter values and distorts the likelihood surface, rendering the reported −866.06 meaningless as a goodness-of-fit measure.

### 3. dmeasure uses `rbinom` internally, making it stochastic and invalid as a density

Inside `bvs_dmeas`, the likelihood is evaluated as:

```c
double Views = rbinom(N-S, 1-exp(-Beta*S/N));
lik = dnorm(Subs+D-S, Views*(1-exp(-mu_VS)), Views*(1-exp(-mu_VS))/10, 1);
```

`rbinom` is a random draw, not a deterministic quantity. Every call to `dmeasure` with the same particle state and parameters returns a different value of `Views`, making `lik` a random variable rather than a proper log-density. The particle filter requires a deterministic conditional log-likelihood p(y_t | x_t, θ). Using a stochastic intermediate in `dmeasure` means the filter is evaluating a different density at each call, and the reported log-likelihood has no statistical interpretation. This is one of the most fundamental POMP implementation errors possible (see pomp-inference-misuse skill).

### 4. rmeasure and dmeasure use the same distributional family but are semantically inconsistent

`bvs_rmeas` draws:
```c
Subs = rnorm(Views*(1-exp(-mu_VS)), Views*(1-exp(-mu_VS))/10) + S - D;
```

`bvs_dmeas` evaluates:
```c
lik = dnorm(Subs+D-S, Views*(1-exp(-mu_VS)), Views*(1-exp(-mu_VS))/10, 1);
```

Setting aside the stochastic `Views` problem (Issue 3), the dmeasure evaluates the density for `Subs+D-S` while the rmeasure draws `Subs` and then adds `S-D` after the rnorm call. The quantity whose distribution is described in dmeasure is `Subs+D-S`, the net change in subscribers, while rmeasure produces `Subs` directly. These are measuring different quantities, so the simulated data from rmeasure and the likelihood weights from dmeasure do not correspond to the same observation model (see pomp-dmeas-rmeas-moment-mismatch skill).

### 5. The rprocess step function does not update the Subscribers state variable

The `bvs_step` Csnippet only updates `Beta` (via a random walk) and `D` (departing subscribers):

```c
Beta = expit(logit(Beta) + rnorm(0, Beta_sigma));
D = rbinom(S, 1-exp(-mu_SB));
```

The state variable `S` (Subscribers) is never updated in the rprocess. According to the compartmental model description, S should increase by new subscribers (Viewers → Subscribers) and decrease by D (Subscribers → Beginning). Because S is never incremented, the model cannot grow its subscriber count endogenously — any long-run subscriber growth visible in the simulation is entirely driven by the covariate that supplies the lagged subscriber count, not by the model dynamics. This makes the BVS model a trivial persistence model, not a mechanistic compartmental system.

### 6. Subscribers is supplied as a covariate and also declared as a state/observation — circular specification

The covariate table passes the lagged value of `Subscribers` (from the data) as `S` to the model. However, `S` is also the latent state being estimated. This is circular: the "latent state" at time t is simply the observed value from time t−1, so the model contains no latent dynamics at all. The particle filter has nothing to estimate because S is pinned to observed data. This defeats the purpose of POMP modeling entirely.

### 7. No convergence diagnostics presented for the POMP analysis

No convergence trace plots, no paired scatter plots of parameters vs. log-likelihood, no ESS diagnostics, and no comparison across IF2 replicates are shown. The paper reports only a single final log-likelihood number. Without these diagnostics it is impossible to assess whether the IF2 search converged, whether the reported −866.06 is near the MLE, or whether the global search explored the parameter space meaningfully. This directly violates Wheeler et al. (2024) best practice §6 (Computational adequacy).

### 8. Global IF2 search initializes from `mifs_local[[1]]` rather than the base pomp object

The global search code runs:
```r
mf1 <- mifs_local[[1]]
...
mf1 %>% mif2(Nmif=25, params=c(guess, fixed_params)) %>% mif2(Nmif=50) -> mf
```

`mf1` is the first result from the local IF2 search. Using it as the first argument to `mif2()` in the global search inherits the cooling schedule from the local chain, not from a fresh start. The global search replicates effectively continue the local search trajectory rather than exploring the parameter box from independent starting points. The reported "global maximum" is likely the same local optimum found in the first stage. See the pomp-global-search-init-audit skill for the canonical description of this anti-pattern.

### 9. No profile likelihoods, confidence intervals, or parameter identifiability assessment

No profile likelihoods are computed for any parameter. Given that the model has at least five free parameters (Beta_sigma, mu_VS, mu_SB, Beta_0, and implicitly N) and only 60 observations, parameter identifiability is a serious concern. Without profiles, there is no evidence that any parameter is identified, and the point estimates have no associated uncertainty. This violates Wheeler et al. (2024) best practice §5 (Parameter identifiability and uncertainty).

### 10. No benchmark comparison for the POMP model

Even setting aside the invalid ARIMA–POMP comparison, no proper non-mechanistic benchmark is provided. The ARIMA model was fit on a transformed scale with a different observation model; it cannot serve as a benchmark for the POMP model on raw counts. A correct benchmark would be an auto-regressive negative binomial or Gaussian model evaluated on the same data and scale as the POMP model, providing a quantitative baseline. Without this, there is no way to assess whether the BVS model captures meaningful structure. See Wheeler et al. (2024) §Benchmark comparison.

---

## Minor Issues

- **Typo in title**: "Subsciber Analysis" should be "Subscriber Analysis." The CSV column header also misspells "AvgVeiwers" (should be "AvgViewers"); this propagates into the code.

- **N is fixed at 41,500,000 without justification**: The total population parameter N = 41,500,000 is used in the force-of-infection term `Beta*S/N`. No justification is given for this value (it appears to be approximately the Twitch platform user count, not the streamer's audience). Whether this is the correct normalizing quantity for the model is never discussed, and it is never estimated or its sensitivity assessed.

- **`fixed_params` is referenced but never defined**: The global search code calls `c(guess, fixed_params)` but `fixed_params` is not defined anywhere in the visible code. This would cause a runtime error. This suggests the POMP section was adapted from a template without completing the necessary edits.

- **rw.sd values in mif2 match starting-parameter values**: The local IF2 call sets `rw.sd=rw.sd(Beta_sigma=0.2, mu_VS=0.37, mu_SB=0.05, Beta_0=ivp(0.2))`. The `mu_VS=0.37` perturbation matches the starting parameter value exactly, and `Beta_sigma=0.2` and `Beta_0=0.2` are also at their starting values. For `mu_VS`, a perturbation SD of 0.37 on a logit-transformed parameter is very large; this is the pomp-rw-sd-magnitude-error anti-pattern. Without convergence traces it is impossible to confirm diffusion, but the configuration is a concern.

- **Model description is incomplete**: The paper states "Viewers is not a cumulative category, but gets reset to 0 every month," but the rprocess never creates or resets a Viewers variable. V is described in comments as a compartment, but it is computed only in the measurement functions (dmeasure/rmeasure) as a local variable and has no role in the state vector. The text describes a different model than the code implements.

- **The "R2 = 0.983" reported for the ARIMA model is misleading**: R-squared is not a standard metric for ARIMA models, and reporting it for a model fit on differenced log-transformed data on the original count scale is misleading. The value should be interpreted cautiously, and no uncertainty is reported around it.

- **Stationarity is assessed only visually**: The paper states "the log-diff subscriber data series look stationary" based on a plot, without a formal stationarity test (ADF, KPSS, or Phillips-Perron). Given the visible slow decay in the log-diff series at the end of the sample, a formal test is needed to confirm the differencing was sufficient. The stationarity-test-conclusion-audit skill highlights this as a recurrent gap in time-series projects.

- **AIC table for ARIMA model selection applies grid search to log-differenced data, but the model is called ARIMA(1,1,2)**: The grid search is conducted on the already-differenced series `x` using ARMA models (d=0 implicitly), but the selected model is described as ARIMA(1,1,2). The differencing is applied externally before the AIC search, making the d=1 label of ARIMA(1,1,2) redundant. This is not technically incorrect but is confusing notation.

- **PDF renders a local file path in the POMP section**: Pages 8–12 of the PDF show the content from a locally-rendered HTML file (`file:///C:/Users/Ahmed/OneDrive...`), indicating these sections were screenshotted or embedded from a separate rendered file rather than being integrated into the main document. This is a reproducibility and presentation concern.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project03/blinded.pdf`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project03/twitch.csv`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-artifact-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-inference-misuse/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-simdata-benchmark-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-static-population-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/stationarity-test-conclusion-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-loglik-direction-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-moment-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-placeholder-result-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-range-misalignment/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-orphan-paramname-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rprocess-wrong-hazard-variable/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-box-domain-violation/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-wrong-variable-display-audit/SKILL.md`
