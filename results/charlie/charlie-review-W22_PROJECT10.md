# Peer Review: W22 Project 10
**Title:** Modeling South Africa Omicron Variant Cases Modeling

---

## Summary

This project models daily new COVID-19 (Omicron) confirmed cases in South Africa (December 2021 to April 2022) using three approaches: ARMA(3,3), a basic POMP SIR model, and a more complex POMP SEAPIRD model. The authors correctly apply iterated filtering (mif2) with replicated particle filter likelihood evaluation (logmeanexp), and they provide a useful trajectory from simple to complex models. However, the work is undermined by several serious implementation bugs (accumulator variable misinitialization, inconsistent population size in the global search, a measurement model mismatch between rmeasure and dmeasure), the absence of profile likelihood confidence intervals, suppressed SIR convergence diagnostics, and no non-mechanistic benchmark comparison. The SEAPIRD model also uses a normal measurement model that lacks biological justification and introduces a problematic measurement model inconsistency between rmeasure and dmeasure. These issues collectively prevent readers from assessing parameter identifiability or the scientific validity of the results.

---

## Major Issues

### 1. Accumulator variable H initialized to 169 in SIR rinit (implementation bug)

In `sir_rinit` (line 199-204), the accumulator variable `H` is set to 169 at time t0:

```c
H = 169;
```

Because `H` is declared as an `accumvars` in the pomp object (line 221), the pomp framework automatically resets `H` to zero at the start of each observation interval. However, setting `H = 169` at initialization is semantically wrong: the accumulator is supposed to count transitions from I to R within each observation period, starting from 0 at t0. This initialization causes the first observation period's H to start at 169 rather than 0, biasing the first likelihood contribution. This is a direct code bug that propagates into the reported log-likelihood values for the SIR model. (See Wheeler et al. 2024, §Reproducibility, on model-code consistency.)

**Fix:** Set `H = 0` in `sir_rinit`.

---

### 2. Inconsistent population size N in the SIR global search

The SIR model pomp object is initialized with `N = 50000000` (50 million, line 229), consistent with South Africa's population. However, the global search (line 315) hard-codes `N = 500000` (500 thousand):

```r
params = c(apply(covid_box_sir,1,function(x)runif(1,x[1],x[2])), N=500000),
```

This means the global search runs with a population 100 times smaller than the model's stated value and than the local search. The infection rate, transmission dynamics, and force-of-infection term `Beta*I/N` are all distorted. The "global" best log-likelihood of -1677 (with N=500000) is not directly comparable to the local search result of -1997 (with N=50000000), rendering the comparison in the Conclusion misleading.

**Fix:** Set `N = 50000000` in the global search parameter initialization, consistent with the model description.

---

### 3. SEAPIRD rmeasure and dmeasure are inconsistent

In `seapird_rmeas` (lines 456-469), simulated cases are computed as:

```c
cases = rnorm(mean_cases, sd_cases) + D;
```

That is, reported cases = Normal(rho*H, sd) + D (current deaths).

But in `seapird_dmeas` (lines 472-485), the likelihood is evaluated as:

```c
lik = dnorm(cases - deaths, mean_cases, sd_cases, 0);
```

That is, the dmeasure treats (cases - deaths) as the observation from Normal(rho*H, sd). This means rmeasure simulates `cases = rho*H + noise + D`, while dmeasure assumes `cases - deaths = rho*H + noise`. These are equivalent only if D (the latent state) equals `deaths` (the observed deaths), which is not guaranteed. The mismatch between generative and evaluative measurement models is a recognized reproducibility failure (Wheeler et al. 2024, §Reproducibility). All likelihood values from the SEAPIRD model are suspect.

**Fix:** Align the two snippets so that rmeasure and dmeasure use identical transformations of the same quantity.

---

### 4. No profile likelihoods or confidence intervals for any parameter

Neither the SIR nor the SEAPIRD model presents profile likelihoods for any estimated parameter. Without profiles, there is no evidence that any parameter is identifiable from the data. The SEAPIRD model has 12 free parameters — identifiability is a serious concern with that many parameters and 156 observations. The text reports point estimates (e.g., beta=2.56, rho=0.993) but provides no uncertainty quantification. (Error 1.9, CC-Yes; Wheeler et al. 2024, §Parameter identifiability.)

**Fix:** Compute and display profile likelihoods for at least the scientifically key parameters (beta, rho, mu_IR). Report confidence intervals via the Wilks threshold.

---

### 5. SIR convergence diagnostics suppressed (eval=FALSE)

The chunk `SIR_diag` (lines 350-360) that produces log-likelihood convergence trace plots for the SIR model is marked `eval=FALSE` and never appears in the rendered output. The text states "the log likelihood soon converges" but no trace plot is shown for the SIR model to support this claim. Without visible convergence evidence for the SIR model, readers cannot assess whether the reported log-likelihood of -1997 is near the MLE. (Error 1.8, CC-Yes.)

**Fix:** Remove `eval=FALSE` from the SIR diagnostic chunk, or replace with the SEAPIRD-style convergence plot that is shown. At minimum, reproduce the mif2 trace plots in the rendered document.

---

### 6. No non-mechanistic benchmark comparison

The Conclusion states that "SIR model is not that competitive comparing to the basic simple ARMA model, judging from the likelihood perspective," implying an ARMA-vs-SIR comparison. However, no explicit ARMA log-likelihood is reported alongside the POMP log-likelihoods in the text, and no formal comparison table is presented. The ARMA(3,3) AIC is computed (`cbind(aic = arma_33$aic, loglikelihood = arma_33$loglik)`, line 113) but never numerically contrasted against the POMP model log-likelihoods in the discussion. A proper benchmark comparison is a key validation tool (Error 1.6, CC-Yes; Wheeler et al. 2024, §Benchmark comparison).

**Fix:** Report the ARMA(3,3) log-likelihood alongside the SIR and SEAPIRD log-likelihoods in a summary table, so the comparison is explicit and quantitative.

---

### 7. SEAPIRD measurement model uses Normal distribution without adequate justification

The SEAPIRD model uses a Gaussian measurement model: `Y_cases ~ Normal(rho*H, tau*rho*H*(1-rho))`, where the variance term `tau*rho*H*(1-rho)` is a non-standard variance specification. This choice is stated only as "since our reported cases is fairly large and the mode is around 1925." The SIR model uses a negative binomial, which is the standard overdispersed count measurement model for disease case data (Wheeler et al. 2024, §Stochasticity and §Measurement model). Using a normal distribution for non-negative integer counts allows the model to generate negative values (handled by clamping at 0 in rmeasure, but not handled correctly in dmeasure), and the variance specification does not reduce to any standard overdispersion formula. The change between SIR and SEAPIRD measurement models also makes log-likelihood comparisons between these two models non-interpretable.

**Fix:** Justify the normal measurement model with a reference or biological argument, or switch to the negative binomial used in the SIR model for consistency and interpretability.

---

### 8. Small rw.sd values likely insufficient on the natural (untransformed) scale

In the SIR local and global searches (lines 260, 319), `rw.sd` values are: `Beta=0.01, rho=0.005, mu_IR=0.005, eta=ivp(0.005), k=0.01`. For the SEAPIRD model (lines 538, 599), all parameters use `rw.sd=0.01`. These perturbation magnitudes are applied on the transformed (log/logit) scale via `partrans`. On the log scale, `rw.sd=0.01` corresponds to roughly 1% multiplicative perturbation per step, which is reasonable for some parameters. However, for the SIR model, `rho` and `mu_IR` receive `rw.sd=0.005`, which is smaller than the course standard of 0.02 (531-conventions.md, Ch 15 p31). This may slow exploration of the parameter space unnecessarily, especially given the already limited local search of only 150 iterations with Np=100 particles.

**Fix:** Consider increasing rw.sd for most parameters to at least 0.02, particularly for the local SIR search.

---

## Minor Issues

### 9. SIR local search uses only Np=100 particles

The SIR local search (line 258) uses `Np=100` particles, which is a debugging-level run_level=1 setting. With Np=100, the particle filter is highly noisy, and the resulting mif2 parameter traces and terminal log-likelihoods are unreliable. The text notes "the best log likelihood is -1997, with a standard error of 6.98," which is an extremely large Monte Carlo SE (on the order of 7 log-likelihood units), confirming that 100 particles are insufficient for reliable inference. (Error 1.4, CC-Yes.)

**Fix:** Increase Np to at least 1000 for the local SIR search, consistent with run_level=2 standard.

---

### 10. Global search best result selected without sorting by log-likelihood

In the SEAPIRD global search, the best parameter set is extracted by `unlist(global_results_seapird[1, ])` (line 612), which selects the first row of the results data frame rather than the row with the highest log-likelihood. The local search at least filters and sorts (`filter(is.finite(loglik)) %>% arrange(-loglik)`, lines 551-552). The global simulation may therefore not represent the best-found parameters.

**Fix:** Apply the same `arrange(-loglik)` logic to `global_results_seapird` before extracting the best parameters for simulation.

---

### 11. SEAPIRD initializes S = N, removing all infectious structure at t0

The `seapird_init` Csnippet (lines 445-454) sets `S = N` (500,000) and `I = 169`, implying that S + I > N since S is set to the full population N. This violates population conservation (S + E + P + A + I + R + D = N). With S = N and I = 169, the total population at t0 is N + 169 = 500,169, not N. This over-counts susceptibles at initialization.

**Fix:** Set `S = N - I` (and adjust other compartments accordingly) to enforce N = sum of all compartments at t0.

---

### 12. The SEAPIRD dN_EA / dN_EP split can produce non-integer compartment sizes

In `seapird_step` (lines 437-438):
```c
P += nearbyint((1 - alpha) * dN_EI) - dN_PI;
A += nearbyint(alpha * dN_EI) - dN_AR;
```
The transitions from E are split proportionally by alpha. However, `nearbyint((1-alpha)*dN_EI) + nearbyint(alpha*dN_EI)` may not equal `dN_EI` due to rounding. This means exposed individuals can be created or destroyed, violating population conservation. The standard approach is to draw from a binomial rather than rounding two separate fractions.

**Fix:** Use `dN_EA = rbinom(dN_EI, alpha)` and set `dN_EP = dN_EI - dN_EA` to ensure conservation.

---

### 13. Spectrum analysis frequency interpretation is not precise

The text identifies `omega_1` as "corresponding to the number of days in the data set which does not seem to be interesting." This is the DC component (frequency 0) or the lowest non-zero frequency (1/156 cycles per day), but the explanation is unclear. The authors then identify `omega_2 = 0.142` as corresponding to a period of 7 days (7-day reporting cycle), which is reasonable. However, the peak labeled `peak_freq` via `which.max(cycle_spec$spec)` (line 145) — presumably near 0 — is noted as uninteresting, while 0.142 is identified as the main signal without clarifying why `peak_freq` differs from 0.142. The description would benefit from explicitly stating the frequency and period units (cycles per day, period in days).

**Fix:** Add explicit unit labels (cycles per day, period in days) and clarify the relationship between `peak_freq` and the stated `omega_1`.

---

### 14. SEAPIRD model's intervention structure uses arbitrary 50-day cutoffs

The intervention parameters c_1, c_2, c_3 are assigned by equally dividing the 156-day observation window into three 50-day periods (`i < 50`, `50 <= i < 100`, `i >= 100`). These cutoffs are not tied to any documented government policy changes or epidemiological events. The model description mentions "local government will possibly take procedures" without citing specific interventions in South Africa during the study period.

**Fix:** Either tie the cutoff dates to documented policy events (e.g., specific lockdown announcements) or treat the breakpoints as additional estimated parameters with biological justification.

---

### 15. No discussion of parameter estimates' biological plausibility

The SEAPIRD global search yields parameter estimates including `mu_ID = 0.00000864` (an extremely small death rate, implying an infection fatality rate near zero) and `alpha = 0.0285` (only 2.85% of infectious individuals are asymptomatic, far below most published Omicron estimates of 30-70%). These extreme values are presented without any discussion of their plausibility against independent epidemiological evidence. Implausible estimates may indicate model misspecification rather than biological discovery (Wheeler et al. 2024, §Corroboration with scientific knowledge; Error 1.9 CC-Yes on identifiability).

**Fix:** Compare estimated parameters to published Omicron epidemiological literature and discuss whether the estimates are biologically credible or suggest misspecification.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project10/blinded.Rmd`
