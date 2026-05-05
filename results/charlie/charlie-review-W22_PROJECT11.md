# Peer Review: Hungarian Chickenpox POMP Model Analysis
**Semester:** W22 | **Project:** 11

---

## Summary

This project fits a modified SEIR model — augmented with a vaccination compartment — to weekly Hungarian chickenpox case counts (2005–2014) using iterated filtering (mif2) and particle filtering (pfilter) in the `pomp` framework. The authors conduct local and global parameter searches, present trace plots and pairwise scatter plots, and simulate forward from the best-found parameters. Key strengths include a well-motivated biological extension (vaccination), use of population/birthrate covariates with spline smoothing, and correct use of `logmeanexp` for likelihood aggregation. However, the project has several substantial weaknesses: biologically implausible parameter estimates from the global search go unaddressed, the global search produces a lower likelihood than the local search (an inversion the authors acknowledge but do not resolve), no non-mechanistic benchmark is compared against the POMP model, no formal profile likelihoods are computed for any parameter, and an important implementation bug causes negative `iota` values at the MLE. These issues, taken together, undermine confidence in both the reported parameter estimates and the model's claimed adequacy.

---

## Major Issues

### 1. Biologically implausible MLE parameters from the global search are accepted uncritically

The "best" global-search parameter set reported in the table (loglik = -3478.08) contains:

- R0 = 202.49 (literature value is 7–12; the authors themselves cite 9–10 on page 1)
- gamma = 922.49 (recovery rate implying infectious period of ~0.4 days)
- iota = -0.429 (negative disease import rate, which is physically meaningless)
- rho = 0.968 (97% reporting rate, far above the 43% the authors calculated from data)
- vr = 0.625 (62.5% vaccination rate, contradicting the paper's own premise that Hungarian vaccination is very low)

The authors note in the Discussion that R0 "came out to be extremely high" but offer no diagnosis and draw no corrective conclusion. Implausible estimates of this kind are a canonical signal of model misspecification (Wheeler et al. 2024, §Parameter identifiability), not a numerical optimization artifact. The authors should (a) treat these as evidence of structural problems in the model, (b) examine whether the data actually support the estimated values, and (c) revise the model rather than reporting these as the global MLE. At minimum, the authors should not simulate forward from a parameter set containing a negative iota (see Issue 2).

### 2. Negative iota parameter is used as the nominal best-fit parameter

The `iota` (disease import rate) parameter has value -0.4295 in the global-search MLE and is used directly in the forward simulation on line 743 of `blinded.Rmd`. Inspection of `global_search_1.rds` confirms that 71 of 400 global search trajectories terminated at negative iota values. The `iota` parameter enters the force-of-infection expression as `pow(I + iota, alpha)` in the rprocess C-snippet (line 216). Negative iota makes this expression undefined when I is small and alpha is non-integer — it will produce NaN or nonsensical values. No constraint or transformation is applied to iota in the parameter transformations (the `parameter_trans` call uses `log` for `sigmaSE`, `psi`, `R0`, `sigma`, `gamma` but not for `iota`). This is a code-level bug: `iota` should be constrained to be non-negative (e.g., via a log transformation). The absence of this constraint compromises the global search and invalidates the stated best-fit parameters.

### 3. Global search likelihood is lower than local search likelihood, with no resolution

The authors report a local search best loglik of -3400.71 and a global search best loglik of -3478.08 — a gap of approximately 77 log-likelihood units, meaning the global search found a substantially worse optimum. The authors acknowledge this discrepancy and attribute it to lower run-level computational resources during the global search, but this explanation is incomplete: the global search uses 400 starting points vs. the local search's 20, and the global search was not seeded from the local MLE region. In a sound analysis the global search should either (a) confirm the local MLE (supporting its validity) or (b) find a higher likelihood (identifying a better mode). When the global search finds a lower likelihood, it signals either insufficient global computation or that the local MLE was found at a local optimum. Neither interpretation is explored. The authors should use the global search best point as a new starting point for additional local searches, or explain why the two likelihoods cannot be reconciled (Wheeler et al. 2024, §Computational adequacy).

### 4. No non-mechanistic benchmark comparison

The POMP model's fit is never compared against a non-mechanistic baseline such as an ARMA, seasonal ARIMA, or IID negative-binomial model. Without such a comparison, it is impossible to assess whether the mechanistic SEIR structure captures meaningful structure beyond what a simple statistical model would achieve. The best local loglik is -3400.71; without knowing what a simple benchmark achieves on the same data, there is no way to evaluate whether the SEIR model adds value. This is a core validation step (Wheeler et al. 2024, §Benchmark comparison; Error 1.6, CC-Yes).

### 5. No formal profile likelihoods computed; identifiability not assessed

No profile likelihoods are computed for any parameter. The "poor man's profile" for `vr` shown in the report (plotting loglik vs. vr for global search results within 10 log-likelihood units of the maximum) is not a proper profile likelihood: it does not maximize over nuisance parameters at each fixed value of vr. The authors correctly identify vr as weakly identified from this plot, but the same analysis is not applied to R0, rho, gamma, or other parameters that converge to implausible values. Without profile likelihoods, no confidence intervals can be reported and identifiability of key parameters cannot be established (Wheeler et al. 2024, §Parameter identifiability; Error 1.2, CC-Yes).

### 6. Cooling fraction is very aggressive (0.1), potentially harming convergence

The local search uses `cooling.fraction.50 = 0.1` (perturbations halved after every 50 iterations), compared to the standard course value of 0.5. At this aggressive cooling schedule, parameter perturbations become negligibly small very early in the search (after ~50 iterations at run_level=3 with Nmif=400, the rw.sd has already been reduced to 0.1^(400/50) = 0.1^8 of its initial value, which is effectively zero). This means the optimizer cannot escape local modes in the later iterations and may converge prematurely to suboptimal parameter estimates. The standard guidance is cooling.fraction.50 = 0.5 (Ch 15, p31-32). The choice of 0.1 is not justified anywhere in the report, and the unusually large spread in log-likelihoods across local search runs (range -10556.15 to -3400.71; see `lik_local_3_runagain.rds`) is consistent with a search that has not adequately explored parameter space before cooling. The authors should either justify this choice or rerun with cooling.fraction.50 = 0.5.

### 7. Large Monte Carlo standard error in some local search likelihood evaluations

Inspection of `lik_local_3_runagain.rds` reveals that several of the 20 local search runs have very large loglik.se values: 99.32, 14.31, 11.67, 5.36, and 2.36. These values are far too large to treat the reported log-likelihoods as reliable estimates. The authors report the maximum loglik across these 20 runs (-3400.71, with se=0.22), but do not flag that multiple runs produced unreliable estimates. For runs with se >> 1, the reported loglik may differ from the true loglik by many units, making valid model comparison impossible (Error 1.4, CC-Yes; Wheeler et al. 2024, §Computational adequacy).

---

## Minor Issues

### 8. R0 from local search also biologically implausible

The local search MLE reports R0 = 82.67, which is far above the literature range of 7–12 cited in the paper itself. The authors flag this in the Discussion but do not attempt to constrain R0 to a biologically plausible range or diagnose the cause. If R0 is not identifiable at a reasonable value, this is a sign of model misspecification (e.g., collinearity between R0 and other transmission parameters), and a profile likelihood for R0 would be the appropriate diagnostic.

### 9. Outlier removal from the data is not adequately justified

Six weekly observations are removed from the 522-week time series, described as "possible data entry errors." No formal criterion is given for identifying these observations as outliers (e.g., Cook's distance, residual threshold, or comparison with county-level data). Removing data points without justification can bias both parameter estimates and likelihood values.

### 10. Global search fixes initial conditions rather than estimating them

The global search fixes `S_0`, `E_0`, `I_0`, and `R_0` at values taken from the local search output (`fixed_params <- c(mu=0.0001, S_0=0.00477, E_0=2.66e-05, I_0=2.081e-05, R_0=.9522)`) rather than optimizing over them. Since the sensitivity of SEIR model fits to initial conditions can be large (Wheeler et al. 2024, §Initial conditions note that initialization strategy can affect AIC by ~72 units), fixing these values introduces a potentially large bias in the global likelihood surface.

### 11. Simulation diagnostics use only one simulation trajectory

Both the local-search and global-search model evaluation sections show a single forward simulation trajectory overlaid on the data (`nsim=1`). A single simulation is not informative about model uncertainty — it cannot reveal whether the data fall within the model's predictive distribution. Standard practice is to simulate many trajectories (e.g., Nsim=100 or 500) and display quantiles (Ch 16).

### 12. iota parameter lacks a log transformation in partrans

As noted in Issue 2, `iota` is included in the estimated parameters but has no transformation applied in `parameter_trans`. Parameters estimated as constrained-positive quantities (import rate, mixing coefficient) should be log-transformed to ensure the optimizer searches on an unconstrained scale. Without this, the optimizer can move to negative iota values silently, and the perturbation noise (rw.sd=0.02 on the untransformed scale) is not scale-invariant.

### 13. No ARIMA / spectral analysis baseline for the EDA

The EDA section shows a time series and a bar chart of cases by month, but does not perform any ARIMA, ACF/PACF, or spectral analysis. Given that the data have clear annual seasonality, a quantitative characterization (dominant spectral frequency, SARIMA model) would have strengthened the EDA and provided a natural benchmark.

### 14. R code visible in eval=FALSE blocks includes errors that would fail at runtime

The code block for constructing `results_local` (line 502 in blinded.Rmd) references `liks_local` and `mifs_local` — objects defined in a prior `eval=FALSE` block that would not exist at runtime. A similar issue appears at line 647 for `liks_global` and `mifs_global`. These code blocks cannot be run as written, undermining reproducibility.

### 15. The vaccination implementation double-counts individuals removed from S

In the rprocess C-snippet, the vaccination count `vac` is computed from `br` (birthrate) rather than from the susceptible stock, and the recovered compartment is updated as `R = pop - S - E - I + vac` rather than by tracking transitions. This formulation assumes R absorbs all residual individuals, but adding `vac` to the population balance in this way may not correctly account for the flow of vaccinated individuals (who were already counted in the `S` update as `S += births - trans[0] - trans[1] - vac`). The population balance should be verified to ensure S + E + I + R = pop at all times, and the description in the text should match the code precisely.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project11/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project11/finalProject.R`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project11/global_search_1.rds` (inspected via R)
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project11/local_search_3_runagain.rds` (inspected via R)
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W22/project11/lik_local_3_runagain.rds` (inspected via R)
