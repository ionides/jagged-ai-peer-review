# Peer Review: W24 Project 01 — "A Latent Process of Democracy since 1800"

---

## Summary

This project models the global count of yearly democratic transitions as a POMP compartmental model inspired by SEIR epidemiology. The latent chain S -> P -> R -> N is mapped onto the political-economy narrative of Acemoglu and Robinson (2006). The observed outcome is the annual increment of democracies, delta-Z(t). The report presents parameter estimation results, a benchmark comparison, simulation plots, and probes. Despite an interesting theoretical motivation, the project has serious methodological and statistical weaknesses that undermine the validity of its conclusions.

---

## Weaknesses (most critical first)

### 1. [MAJOR] No mif2 (IF2) code is shown or described — algorithm identity is unclear

The report states estimation is done through "the particle filter algorithm with multiple iterations." The only computational evidence shown is a `runif_design` call that generates 200 starting points, and results loaded from a pre-saved `.rds` file (`Level 2.5.rds`). No `mif2`, `pfilter`, or any other estimation call appears anywhere in the Rmd. The reader cannot verify what algorithm was actually used, what the Nmif and Np settings were, whether the cooling schedule and rw.sd parameters were applied as described, or whether the run converged. This is a fundamental reproducibility failure.

### 2. [MAJOR] The design is a global search, not a profile likelihood — the CI construction is invalid

The report labels the scatterplot of loglik vs. each parameter a "profile likelihood confidence interval" and draws cutoffs at max(loglik) - 0.5*qchisq(0.95, df=1) and max(loglik) - 0.5*qchisq(0.975, df=1). However, profile likelihood requires that, for each fixed value of the parameter of interest, the remaining parameters are optimized. What is plotted is a pairs plot of a global search output, in which other parameters are not optimized out. This does not satisfy the definition of profile likelihood, so the resulting intervals are not statistically valid confidence intervals.

### 3. [MAJOR] The transition rate in the rprocess contradicts the stated model equation

The prose describes the S -> P transition as driven by beta * R(t) / S(t), i.e., the force is proportional to the fraction of revolutionary states. However, in the Csnippet the transition rate is written as:

```c
double dN_SP = rbinom(S, 1-exp(-Beta * N/tot_sov * dt));
```

The rate uses `N` (democracies), not `R` (revolutionary states), divided by `tot_sov` (a covariate), not `S` (the current compartment count). This is a three-way mismatch with the mathematical notation in equation (1), where the stated expected value is beta * R(t) / zeta(t). The model being estimated is not the model being described.

### 4. [MAJOR] The observation variable delta-Z(t) truncates negative values, but the measurement model ignores this

Delta Z(t) is defined as max(0, Z(t) - Z(t-1)), discarding autocratic reversals. The dmeasure uses a standard negative binomial density, which does not account for the left-censoring at zero induced by this truncation. This misspecification causes the likelihood values to be inflated relative to what a correctly specified measurement model would produce, and biases the AIC comparison.

### 5. [MAJOR] S is treated as a compartment but is also used as a covariate — the model is internally inconsistent

The covariate `tot_sov` is a cubic-spline-interpolated smoothing of the number of sovereign states. Simultaneously, S is initialized at 23 and depleted as states move through the chain. Once all 23 states in S are absorbed into P, R, or N, S = 0 and no further transitions can occur, yet the world continues to gain sovereign states through history. The model has no mechanism to add new sovereign states to S over time, so the stock of S will be exhausted while the real system continues to grow. The covariate tot_sov is used in the denominator of the transition rate but never replenishes S.

### 6. [MAJOR] The conserved total is wrong — N accumulates monotonically but is never depleted

In the Csnippet, `N += dN_RN` with no outflow. This means N only grows. In the SEIR analogy, this corresponds to modeling "recovered" as permanently accumulating, which prevents the model from capturing any decline in democratic counts. Yet the observed variable delta-Z(t) has many zero years and even the raw Z(t) shows periods of stagnation. The model can only ever predict non-decreasing democracy counts, which contradicts the data.

### 7. [MAJOR] The AIC for the IID model is computed incorrectly

The code computes `AIC.iid <- 2 - 2 * log.iid`. This formula uses 2 (implying 1 parameter) rather than 2*2 = 4 (for the two parameters of a negative binomial: size and prob). The IID negative binomial fitted via `optim` over a two-parameter vector `c(0, -5)` should yield AIC = 2*2 - 2*log.iid. The error deflates the IID AIC artificially, distorting the model comparison table.

### 8. [MAJOR] The Poisson log-likelihood is hard-coded rather than computed

The Poisson log-likelihood appears as the literal value `log.pois <- -250.7523` rather than being extracted with `logLik(pois.model)` as done for the negative binomial. Hard-coding this number makes the comparison non-reproducible and potentially incorrect.

### 9. [MODERATE] No convergence diagnostics for the global search

There is no trace plot of loglik vs. iteration, no comparison of results across multiple independent runs, and no examination of whether the likelihood surface has been adequately explored. Given that only 200 starting points and 200 iterations are used, there is no evidence that the global maximum has been found. The pairs plots of loglik vs. parameter are displayed but not used to assess convergence.

### 10. [MODERATE] Figure caption numbering is incorrect

Figure 3 is labeled "Figure 2. The Simulation Result" and Figure 7 is used twice for two different plots (the simulation plot and the probes plot). This indicates the captions were not updated after figures were added, degrading the document's readability and professional quality.

### 11. [MODERATE] The interpretation of probe results is contradictory and poorly supported

The report states the growth-rate probe shows "moderate evidence" that the model's growth rate differs from the data (correctly identifying a problem), but then concludes this "ensures the reliability of parameters rho and k" and that "the simulation works well." These two conclusions are contradictory. A failed probe is evidence of model misfit, not evidence of reliability.

### 12. [MODERATE] The substantive interpretation of the negative exponential relationship in the pair plot is unsupported

The report asserts that the negative correlation between Beta and mu_PR/mu_RN confirms Acemoglu and Robinson's theoretical prediction. However, a negative correlation between parameters in a poorly identified model is a typical symptom of unresolved parameter confounding, not substantive evidence. No sensitivity analysis or identifiability argument is provided to distinguish these interpretations.

### 13. [MINOR] The rho parameter is interpreted as "coding efficiency" rather than a reporting rate

The report describes rho as "the efficiency of past sovereign states to develop an accessible archive for the future coders of political regimes." This is an unusual and unexplained reinterpretation of the standard epidemiological reporting fraction. No theoretical justification is given for why this particular measurement-error structure (rho * N) maps onto archival quality.

### 14. [MINOR] The initial condition for S is inconsistent with data

S(0) is set to 23, stated to match the number of sovereign states in 1800. However, the covariate file shows that `tot_sov` at t=1800 is approximately 22.998, not exactly 23. More importantly, the initial conditions for P(0)=1, R(0)=2, and N(0)=1 sum to 4, implying 4 of the 23 states have already entered the chain at initialization. No justification for these specific values is given beyond brief historical claims about the U.S. and France, and there is no sensitivity analysis for the initial conditions.

### 15. [MINOR] The Poisson log-likelihood is stated as a fact without derivation

The value `log.pois <- -250.7523` is introduced without context: there is no `logLik(pois.model)` call, no mention that this was obtained from a prior run, and no reproducible code path. This makes independent verification impossible.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project01/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project01/blinded.html`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project01/df_dems.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project01/covar.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project01/Makefile`
