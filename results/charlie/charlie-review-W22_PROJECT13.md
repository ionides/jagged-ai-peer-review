# Peer Review: W22 Project 13
## An Analysis of Omicron Variant COVID Cases in California and Texas

---

## Summary

This project fits a time-varying SEIR model to daily COVID-19 case counts in California and Texas during the Omicron wave (December 2021 – March 2022), using the `pomp` package with iterated filtering (`mif2`) for inference. The authors separately parameterize the contact rate $\beta$ as a step function tied to policy events (mask mandates, CDC isolation guideline changes) and attempt a profile likelihood for the reporting rate $\rho$. While the project addresses a timely epidemiological question and demonstrates a reasonable model structure, it has serious computational and methodological weaknesses: the local search is run at debugging-level settings (50 particles, 5 iterations), the reported "profile likelihood" is a pseudo-profile derived from global search scatter rather than a true optimization over nuisance parameters, the global search box for $b_4$ is grossly misaligned with the actual MLE, and a code-order bug causes the Texas starting-value likelihood to be evaluated using California parameters. The analysis self-acknowledges the absence of a benchmark comparison. Taken together, these issues undermine the reliability of all quantitative conclusions.

---

## Major Issues

### 1. Profile likelihood is a pseudo-profile, not a true profile (Error 1.2, CC-Yes)

The authors describe a profile likelihood for $\rho$ and report a 95% confidence interval. However, the code used to produce the profile plot is:

```r
all = read.csv("writeup_params.csv") %>% filter(is.finite(loglik))
all %>%
  filter(loglik > max(loglik) - 10, loglik.se < 2) %>%
  group_by(round(rho, 2)) %>%
  filter(rank(-loglik) < 3)
```

This takes the top-2 log-likelihood values within each binned $\rho$ value from the global search results, rather than running a dedicated `mif2` optimization over all nuisance parameters at each fixed $\rho$ value. A proper profile requires holding $\rho$ fixed and maximizing over all other parameters for each target value. The result is a likelihood slice (the upper envelope of global search scatter), which produces artificially narrow and potentially unreliable confidence intervals. A file `writeup_profile_rho.rds` exists in the project folder and contains 232 rows with a maximum log-likelihood of $-1007.3$, which is 15 log-units better than the global search maximum of $-1022.3$. This better-performing computation is never used in the report. The confidence interval reported from the pseudo-profile is therefore unvalidated.

**Fix:** Run a dedicated profile likelihood sweep: for each fixed $\rho$ on a grid, run `mif2` optimizing over all other free parameters, then re-evaluate with replicated `pfilter`. Plot and use this for the CI.

---

### 2. Global search box misaligned with MLE region for $b_4$ (pomp-global-search-box-misalignment)

The global search for California specifies a lower bound of $b_4 = 700$:

```r
guesses = runif_design(
  lower = c(b1 = 3, b2 = 20, b3 = 0, b4 = 700, rho = 0, eta = 0, tau = 1000),
  upper = c(b1 = 10, b2 = 75, b3 = 60, b4 = 3000, rho = 1, eta = 0.3, tau = 2500),
  nseq = NSTART
)
```

However, the MLE for $b_4$ converges to approximately 221 — well below the lower search bound of 700. Inspection of `writeup_params.csv` shows that 756 of 800 global search results have $b_4 < 700$ (the iterated filtering moves far outside the starting box). This means all starting points for $b_4$ were initialized in a region far from the MLE. The optimization was forced to travel a large distance in log-parameter space purely through the mif2 perturbations, which may have made it harder to find the optimum reliably from many starting points.

**Fix:** After a preliminary local search reveals the approximate MLE, recenter the global search box around this region. The box should cover the MLE with sufficient margin rather than starting entirely above it.

---

### 3. Texas initial likelihood evaluated with California parameters (code-order bug)

The Texas POMP object (`covidSEIR`) is built with `paramnames = c("b1", "b2", "mu_EI", "mu_IR", "eta", "rho", "N", "tau")` and Texas population $N = 29{,}527{,}941$. However, the `pfilter` call for Texas starting values (lines 353–362) executes before the Texas parameter vector is defined:

```r
# Lines 353-362: Texas pfilter called with params still from California context
bake(file = "writeup_lik_starting_values_texas.rds", {
  foreach(i=1:20, .combine = c) %dopar% {
    covidSEIR %>% pfilter(params=params, Np=500)  # params is California's!
  }
})

# Lines 370-373: Texas params defined AFTER the pfilter call
params = c(b1 = 20, b2 = 200, mu_EI = 1/3, mu_IR = 1/7,
           rho = 0.4, eta = 0.01, tau = 1000, N = pop_texas)
```

At the time of the `pfilter` call, `params` is the California parameter vector: `(b1=20, b2=30, b3=100, b4=2000, mu_EI=1/3, mu_IR=1/7, rho=0.7, eta=0.01, tau=2000, N=39538223)`. The Texas POMP object will use `N=39538223` (California's population) and `rho=0.7` instead of the intended Texas starting values. The reported starting log-likelihood for Texas therefore does not reflect the intended Texas parameterization.

**Fix:** Define `params` for Texas before the `pfilter` call.

---

### 4. Insufficient computation: local search at debugging-level settings (Error 1.8, CC-Yes)

The report runs the entire analysis with `run_level = 1`, which sets `NP = 50` particles and `NMIF_S = 5` iterated filtering iterations for the local search. The Texas local search results (`writeup_lik_local_texas.rds`) show log-likelihood standard errors up to 12.5 for the apparent best run, and 1.1–2.7 for most runs. Standard errors of this magnitude mean that log-likelihood differences of 10–20 units between runs are dominated by Monte Carlo noise and cannot be interpreted as meaningful differences in fit. The course convention (run_level=2) calls for $N_p = 1{,}000$ and $N_{mif} = 50$ iterations, and run_level=3 for final writeups. The California local search SEs are smaller due to the model likelihood surface, but 5 iterations of iterated filtering is insufficient to move parameters meaningfully toward the MLE.

The text also states "50 iterations" for the local search, contradicting the actual `NMIF_S = 5` at `run_level = 1`. This inconsistency suggests the text was written for a higher run level than what was actually executed.

**Fix:** Rerun local and global searches at run_level=2 or 3. Ensure text reflects actual computational settings.

---

### 5. Global search code absent from Rmd (reproducibility failure)

The global search results in `writeup_params.csv` and `writeup_params_texas.csv` each contain 800 rows, consistent with `NSTART = 800` at `run_level = 3`. However, the Rmd code for the global search section only shows the creation of `guesses` via `runif_design` and the loading of results via `read_csv`. There is no `bake()` call or `foreach`/`mif2` loop for the global search in the displayed code. The actual computation that produced the pre-saved results is absent from the report.

This means the global search cannot be reproduced from the Rmd as written at `run_level = 1` (which would generate only 50 starting points, not 800). The pre-saved results were generated externally without transparent documentation.

**Fix:** Include the global search computation code with a `bake()` pattern, or explicitly note that the computation was run at a higher `run_level` with the corresponding code block.

---

### 6. No benchmark comparison (Error 1.6, CC-Yes)

No non-mechanistic baseline model (ARIMA, regression, or negative binomial IID) is fitted to either California or Texas. The authors acknowledge this in the conclusion: "We decided to compare pomp models and did not develop a likelihood baseline nor perform extensive diagnostics." Without a benchmark log-likelihood, it is impossible to assess whether the SEIR model captures meaningful structure beyond a simple time-series model, or whether the added complexity of 4–6 contact-rate parameters and the SEIR compartment structure is statistically justified. The California MLE of $-1022.3$ and Texas MLE of $-1026.7$ have no reference point.

**Fix:** Fit an ARIMA or negative binomial model to each state's case series and compare log-likelihoods.

---

### 7. Factor-of-14 scaling in measurement model is unjustified for daily data

The measurement model uses:

```
mean = 14 * rho * H
sd = 14 * sqrt(tau * rho * H * (1 - rho))
```

The authors state this was "needed to allow the model to reach the heights of the spike," describing it as a "fixed scaling parameter $\phi$." With daily data and `delta.t = 1`, `H` accumulates one day of $I \to R$ transitions between observations. A factor of 14 would be appropriate if observations were biweekly and $H$ accumulated over 14 days, but there is no such temporal structure here. This scaling is borrowed from a referenced project (W21 Project 15) that may have used weekly data. The ad hoc factor effectively inflates predicted case counts 14-fold, which distorts the interpretation of $\rho$ (the MLE converges to approximately 0.25, but the true reporting fraction is closer to $0.25/14 \approx 0.018$ relative to actual $I \to R$ flow). Parameters $\rho$, $\eta$, and the $\beta$ values are all confounded by this scaling.

**Fix:** Remove the factor of 14 or provide an epidemiological justification. If the model cannot fit peak heights without it, this signals model misspecification that should be addressed structurally (e.g., by adjusting initial conditions, the initial susceptible fraction, or $N$).

---

## Minor Issues

### 8. Model description inconsistency: $\rho$ described at wrong transition

The text states: "The probability of a case being reported is $\rho$, which happens between the stage E and I." However, in the code `H` accumulates $I \to R$ transitions (`H += dN_IR`), and the measurement model uses `mean = 14*rho*H`. Reporting is therefore associated with recovery, not with the $E \to I$ transition. This is a textual error that misrepresents the model structure.

---

### 9. Texas `rw.sd` specifies parameters not in the Texas model

The Texas local search uses:

```r
params_rw.sd = rw.sd(b1 = 0.01, b2 = 0.01, b3 = 0.01, b4 = 0.01,
                     rho = 0.01, tau = 0.0001, eta = ivp(0.01))
```

`b3` and `b4` are not in the Texas model's `paramnames`. While `pomp` silently ignores perturbations to undeclared parameters, this reflects a copy-paste error that creates potential confusion about what is being estimated.

---

### 10. `tau` perturbation effectively zero on the log scale

The random walk perturbation for `tau` is `rw.sd(..., tau = 0.0001, ...)`, applied on the log scale (since `tau` is in the `log` transform set). With `tau` initialized at 1000–2000, `log(tau) ~ 7–7.6`, and a perturbation of 0.0001 on this scale is negligibly small. This effectively fixes `tau` during iterated filtering, making it an unestimated nuisance parameter despite appearing in the parameter vector. If `tau` is intended to control overdispersion, it should be perturbed at a meaningful magnitude (e.g., 0.02 on the log scale per course convention).

---

### 11. Fixed epidemiological parameters without sensitivity analysis

Both $\mu_{EI} = 1/3$ and $\mu_{IR} = 1/7$ are fixed throughout and not included in estimation. While the values are justified by CDC/WebMD references, fixing these without assessing sensitivity to their values is a limitation. Small changes to the incubation or infectious period could substantially alter the estimated $\beta$ values and $\rho$.

---

### 12. No model diagnostics

The analysis includes simulation-based visual comparison but no formal diagnostics: no effective sample size (ESS) plots from the particle filter, no conditional log-likelihood plots across time, and no filtering-distribution comparison. Given that the model must fit a sharp Omicron peak with a step-function contact rate, diagnostics would reveal whether the model successfully conditions on observed data or whether the particle filter degenerates at the peak.

---

### 13. Profile likelihood computed only for $\rho$; other parameters unexamined

Only the reporting rate $\rho$ has any form of uncertainty quantification. The contact-rate parameters $b_1, \ldots, b_4$ (California) and $b_1, b_2$ (Texas), which are the scientifically most interpretable quantities, have no profile likelihoods or confidence intervals. The convergence plots from the local search show wide spread in $b$ parameters, suggesting weak identifiability that should be quantified.

---

### 14. Lack of quantitative comparison between California and Texas models

The paper analyzes both states but provides no formal comparison of their log-likelihoods (which are on the same scale given the same data length of ~89 observations), estimated contact rates, or reporting rates. The conclusion notes a difference in $\rho$ CIs between states but does not test whether this difference is statistically meaningful. A likelihood ratio test or AIC comparison between the two models is not attempted.

---

### 15. Interpretation of policy effects not grounded in identifiability

The authors infer that the CDC isolation guideline change "did not affect the spread of the virus" based on the convergence of $b_3$ and $b_4$ (the pre- and post-CDC-change contact rates). However, without profile likelihoods for these parameters and given the evidence of weak identifiability in the trace plots, this conclusion is not statistically justified. The parameters may be unidentifiable individually even if their product or ratio is constrained by the data.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_params_texas.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_local_search.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_local_search_texas.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_lik_local.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_lik_local_texas.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_lik_starting_values.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_lik_starting_values_texas.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project13/writeup_profile_rho.rds`
