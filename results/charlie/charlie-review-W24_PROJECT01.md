# Peer Review: W24 Project 01 — "A Latent Process of Democracy since 1800"

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) + particle filter, via pomp R package |
| **R packages used** | pomp, democracyData, tidyverse, doFuture, doParallel, doRNG, MASS, DiagrammeR, xtable |
| **Code publicly available** | Partial — Rmd and data CSV files present; optimization code not shown in document (loaded from RDS) |
| **Data publicly available** | Yes — Boix, Miller, and Rosato (2013) dataset via democracyData R package |
| **Benchmark comparison included** | Yes — IID negative binomial, Poisson regression, negative binomial regression |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | IF2 + replicated pfilter mentioned in text; not shown transparently in document |
| 2 | Benchmark comparison | ~ | Three benchmarks included, but no ARMA/ARIMA |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihood and AIC table provided, but best loglik from global search scatter |
| 4 | Model diagnostics | ~ | Probe plot included; no ESS, no conditional log-likelihood plots |
| 5 | Parameter identifiability and uncertainty | ✗ | Global search scatter misidentified as profile likelihood; no valid CIs |
| 6 | Computational adequacy | ~ | Np=2000, Nmif=200, 4-hour HPC run; no trace plots to verify convergence |
| 7 | Forecast methodology | N/A | No forecasting component |
| 8 | Model variations and nested comparisons | ✗ | No alternative model structures tested |
| 9 | Stochasticity | ~ | Binomial transitions included; no environmental/multiplicative noise |
| 10 | Reproducibility and extendability | ~ | Rmd and CSV files provided; optimization code absent from document |
| 11 | Corroboration with scientific knowledge | ~ | Parameter interpretation offered; plausibility not checked against independent evidence |
| 12 | Measurement model specification | ✗ | Cumulative state N used for annual increment observations; serious mismatch |
| 13 | Initial conditions | ~ | Fixed initial conditions justified narratively but sensitivity not assessed |

---

## Summary

This project applies a four-compartment POMP model (S → P → R → N) to annual counts of new democracies worldwide from 1800 to 2020, motivated by game-theoretic models of democratization. The model is estimated using IF2 with 200 particles/iterations from 200 global search starting points on the University of Michigan's Great Lakes HPC cluster. While the project demonstrates genuine engagement with POMP methodology and draws on a compelling political science motivation, it contains several critical errors: the transition rate implemented in code differs substantially from what is described in the text, the measurement model maps a cumulative state to an annual flow observation, the compartment totals do not conserve the population at initialization, and the "profile likelihood" figures are actually global search scatter plots that do not yield valid confidence intervals.

**Strengths:** The project applies POMP methods to a novel domain (political science), includes benchmark comparisons against multiple alternative models, provides substantive interpretation of results grounded in political science theory, and runs at an appropriate computational scale (Np=2000, Nmif=200, 4-hour HPC run).

**Weaknesses:** Model-code inconsistency in the core transition rate; measurement model mismatch between cumulative state and annual increment data; compartment conservation violation; invalid confidence intervals from global search scatter; missing MIF2 convergence trace plots.

---

## Major Issues

### 1. Model-code inconsistency in the S → P transition rate

The text states that the transition rate from sovereign states S to powerful-elite states P has expected value $\beta \cdot R(t) / \zeta(t)$, where $R(t)$ is the revolutionary threats compartment and $\zeta(t) = S(t)$ is the smoothed covariate of sovereign states. The corresponding model equation (unnumbered, appearing after "Drawing insight from SIER model") shows:

$$\tilde{N}_{SP}(t + \delta) = \tilde{N}_{SP}(t) + \text{Binomial}\!\left[\tilde{S}(t),\; 1 - \exp\!\left(-\beta \frac{\tilde{R}(t)}{\tilde{S}(t)} \Delta t\right)\right]$$

However, the `sprn_step` Csnippet implements:
```c
double dN_SP = rbinom(S, 1-exp(-Beta * N/tot_sov * dt));
```

There are two distinct discrepancies: (1) the numerator in the code is `N` (the democracy/negotiation compartment), not `R` (revolutionary threats); and (2) the denominator is `tot_sov` (the external covariate), not the dynamic state variable `S`. This means the force driving sovereign states into the "powerful elite" category depends on the fraction of existing democracies, not on revolutionary threats as stated in the text and motivated by theory. The code implementation is the opposite of the mechanism described: as democracies accumulate, more sovereign states would transition to "powerful elites," which inverts the theoretical logic. This discrepancy materially affects all parameter estimates and model conclusions. See Wheeler et al. (2024) for documentation of model-code inconsistency as a reproducibility failure.

**Fix:** Reconcile the Csnippet with the equation. If the intended force is $\beta \cdot R(t)/S(t)$, the code should read `rbinom(S, 1-exp(-Beta * R/S * dt))`. Alternatively, if `N/tot_sov` is the intended rate, the text and equations must be revised to match.

---

### 2. Measurement model maps cumulative state to annual flow observation

The observed variable is defined as $\Delta Z(t) = \max(0, Z(t) - Z(t-1))$, the annual count of new democracies. The measurement model is:

$$\Delta Z(t) \sim \text{NegBin}(\rho \cdot N(t),\; k)$$

However, the state $N(t)$ is defined as a cumulative compartment that only increases over time (it receives inflow from R via `dN_RN` and never decreases). By 2020, $N(t)$ would accumulate to approximately the total number of democracies ever created, making $\rho \cdot N(t)$ a large and steadily growing quantity. This cannot serve as the expected value for an annual flow observation that typically ranges between 0 and a few dozen per year and shows no systematic growth trend proportional to cumulative N. The expected value of new democracies per year should be related to the per-step increment `dN_RN / dt`, not the stock `N`. This mismatch means the measurement model is fundamentally misspecified relative to the data being modeled.

**Fix:** Replace $\rho \cdot N(t)$ in the measurement model with a rate based on the annual flow. One approach is to accumulate `dN_RN` within each calendar year and use that flow as the expected observation.

---

### 3. Compartment conservation violation at initialization

The initial conditions are set as $S(0)=23$, $P(0)=1$, $R(0)=2$, $N(0)=1$, summing to 27. According to the text, S represents the number of sovereign states and the covariate `tot_sov` is set to 23 at t=1800 (the first observation year). The total compartment count of 27 exceeds the stated initial number of sovereign states by 4 units. If S, P, R, and N are all subpopulations of sovereign states, their sum should equal `tot_sov` at initialization. The mismatch suggests the population accounting is not internally consistent and the compartment model does not conserve the number of sovereign states.

**Fix:** Ensure $S(0) + P(0) + R(0) + N(0) = \text{tot\_sov}(0)$ at t=1800, or explicitly justify why some compartments represent quantities outside the count of sovereign states.

---

### 4. Global search scatter misidentified as profile likelihood (CC-Yes Error 1.2)

Section 2 (Result) states: "the profile likelihood confidence interval is represented in the following plot" (Figure 4). The code generating this figure is:

```r
result |> dplyr::select(-loglik.se, -etime) |>
  pivot_longer(-6) |>
  ggplot(aes(x = value, y = loglik)) +
  geom_point() +
  geom_hline(aes(yintercept = ci.cutoff.95, ...))
```

This plots the log-likelihood vs. terminal parameter values across 200 global search runs, with a Wilks 95% cutoff line overlaid. This is not a profile likelihood. A profile likelihood requires: for each fixed value of the target parameter, re-optimize over all nuisance parameters. The scatter of terminal values from a global search does not satisfy this requirement; it reflects where optimization runs landed, not the likelihood function's shape along each parameter axis. Applying the Wilks cutoff to this scatter produces artificially wide or wide confidence intervals that lack the statistical validity of profile-based CIs. This is a course-confirmed error (STATS 531 weakness reference Error 1.2).

**Fix:** Implement proper profile likelihood computation using a design matrix that fixes each target parameter across a grid of ~20–30 values and reruns mif2 to maximize over all remaining parameters at each fixed value. Re-evaluate with replicated pfilter at each profile point.

---

### 5. Missing MIF2 convergence trace plots (CC-Yes Error 1.8)

The report provides no trace plots showing the log-likelihood trajectory or parameter convergence across IF2 iterations. Without these diagnostics, there is no evidence that the 200-run global search converged to the MLE or that the best log-likelihood found is near the global maximum. The text states the computation took approximately four hours on 36 cores with Nmif=200 and Np=2000, but neither the convergence of individual runs nor the consistency of terminal likelihoods across runs is documented. This is a course-confirmed error (STATS 531 weakness reference Error 1.8).

**Fix:** Plot the log-likelihood trace across mif2 iterations for multiple runs. Show that log-likelihoods increase consistently and that multiple runs reach similar terminal likelihoods. Parameter traces may show scatter (which is expected and acceptable for weakly identified parameters), but the log-likelihood panel should converge upward.

---

### 6. No particle filter diagnostics

The report includes no effective sample size (ESS) monitoring, no conditional log-likelihood time series, and no filtering distribution comparison. Given the known mismatches between the cumulative-N measurement model and the annual-flow data, it is likely that the particle filter degenerates at multiple time points. Without ESS plots, it is impossible to assess whether the 2000-particle filter is sufficient or whether filter degeneracy is distorting all downstream inference. Per Wheeler et al. (2024), conditional log-likelihood plots are the primary diagnostic tool for identifying periods of poor fit and motivating model revision.

**Fix:** Add ESS plots across observation times and conditional log-likelihood plots. Identify time points where the filter collapses and use these to guide structural model improvements.

---

## Minor Issues

- **POMP model outperformed by negative binomial regression without structural revision (Error 1.15):** The benchmark table shows the negative binomial regression achieves a higher log-likelihood than the POMP model despite using only two parameters. The paper acknowledges this but explains it away by saying the NegBin "does not capture the nuances of the endogenous mechanism." Per course materials and Wheeler et al. (2024), when the mechanistic model fits substantially worse than a benchmark, the correct response is to revise model structure — not to retain the model on theoretical grounds. The poor benchmark comparison is itself diagnostic information that should motivate the model-code inconsistency and measurement model issues identified above.

- **IID model AIC is incorrectly computed:** The IID model is estimated using `optim(c(0,-5), nb_lik)`, which optimizes over two parameters (`theta[1]` and `theta[2]`). However, the AIC computation uses `AIC.iid <- 2 - 2 * log.iid` (implying one parameter, 2k=2). The correct formula is `4 - 2 * log.iid` (2k=4 for two parameters). This makes the IID model appear less penalized than it should be.

- **Poisson log-likelihood is hardcoded:** `log.pois <- -250.7523` is typed as a literal constant rather than computed from `logLik(pois.model)`. This breaks reproducibility — any change to the data or model would leave this value stale without any warning.

- **No sensitivity analysis for fixed initial conditions:** Initial values $S(0)=23$, $P(0)=1$, $R(0)=2$, $N(0)=1$ are fixed and not estimated as parameters. The paper provides narrative justification but does not assess sensitivity. Per Wheeler et al. (2024), initialization strategy can substantially affect AIC and parameter estimates.

- **Probe interpretation is overly optimistic:** The probe plot (Figure 7, second instance) shows the model's simulated growth rate distribution is clearly shifted from the data's realized growth rate, and the residual standard deviation is also discrepant. The paper describes this as "moderate evidence" and frames it as confirming parameter reliability rather than signaling model misfit. A more accurate interpretation would acknowledge that the probe reveals systematic model misspecification.

- **Claim of "well identified" parameters is unsupported:** The paper states "the parameter estimates are well identified" based on the global search scatter (Figure 4). Since this scatter is not a proper profile likelihood (see Major Issue 4), it does not provide evidence of identifiability. $\mu_{PR}$ in particular spans more than two orders of magnitude in the scatter plot, suggesting it may not be well identified.

- **Duplicate and misnumbered figure captions:** `cap_fig7` is defined on line 432 and redefined on line 458, with the second definition overwriting the first; both figures display as "Figure 7." Additionally, `cap_fig3` is labeled "Figure 2" (it should be "Figure 3"), creating two "Figure 2" captions in the document. Figure numbers are inconsistent throughout.

- **Typographic errors in equations and references:** The first transition equation uses `+` where `=` is intended: $\tilde{N}_{SP}(t+\delta) + \tilde{N}_{SP}(t) + \text{Binomial}[\ldots]$ should read $\tilde{N}_{SP}(t+\delta) = \tilde{N}_{SP}(t) + \text{Binomial}[\ldots]$. The author's surname "Wheeler" is misspelled "Wheler" in multiple in-text citations and in the references section. "Diagnostic" is misspelled "diganostic" in the Conclusion. The name "Ionides" is rendered as "Iondies" in one location.

---

## Recommendation

**Major Revision.** The project applies POMP methods to an interesting novel domain and reaches an appropriate computational scale, but three fundamental errors — the model-code inconsistency in the transition rate, the mismatch between cumulative state N and annual flow observations, and the compartment conservation violation — collectively undermine the validity of all reported parameter estimates and model conclusions. These must be corrected before results can be interpreted. Additionally, the profile likelihood figures must be replaced with proper profile computations, and MIF2 convergence traces must be added. The benchmark comparison and substantive discussion demonstrate scientific engagement; with structural corrections, this project has real merit.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project01/blinded.Rmd`
