# Review: W24 Project 08
## *King County COVID-19 Weekly Cases Analysis*

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) with particle filter likelihood evaluation |
| **R packages used** | pomp, forecast, tidyverse, doParallel, doRNG |
| **Code publicly available** | Partial — provided in repository, no DOI archive |
| **Data publicly available** | Yes — JHU CSSE COVID-19 dataset |
| **Benchmark comparison included** | No |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | IF2 + replicated pfilter used correctly for SVEIPR; logmeanexp applied; SEIR analysis uses wrong data |
| 2 | Benchmark comparison | ✗ | ARIMA and POMP log-likelihoods never compared |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported for POMP models; ARIMA AIC reported but log-likelihood not extracted |
| 4 | Model diagnostics | ~ | ESS monitored via pfilter plot; trace plots shown; no conditional log-likelihood plots |
| 5 | Parameter identifiability and uncertainty | ✗ | No profile likelihoods; "poor man's profile" used informally only |
| 6 | Computational adequacy | ~ | SVEIPR uses Np=2000/5000, Nmif=200; SEIR global search uses Np=200 (low); multiple starting points used |
| 7 | Forecast methodology | N/A | No forecasts produced |
| 8 | Model variations and nested comparisons | ~ | SEIR then SVEIPR developed iteratively; no formal nested likelihood comparison |
| 9 | Stochasticity | ~ | Binomial transitions (demographic stochasticity); no environmental/process noise; normal measurement model allows negative counts |
| 10 | Reproducibility and extendability | ~ | Code provided; no package version pinning; no sessionInfo(); rm(list=ls()) present |
| 11 | Corroboration with scientific knowledge | ~ | Vaccine effectiveness gamma discussed; mu_IR and mu_PR fixed without independent justification |
| 12 | Measurement model specification | ✗ | SVEIPR uses normal approximation for count data (produces negative counts); inconsistent with negative binomial standard |
| 13 | Initial conditions | ~ | Initial conditions fixed at biologically motivated values; no sensitivity analysis |

---

## Summary

The paper analyzes COVID-19 weekly cases in King County, Washington, using an ARIMA model for baseline analysis followed by progressively complex POMP compartment models: a standard SEIR and a novel SVEIPR model incorporating vaccination, potentially-infected individuals, and time-varying transmission and vaccination rates. While the project demonstrates meaningful engagement with the POMP modeling framework and several computational best practices (logmeanexp, replicated pfilter, IF2 with multiple starting points), the analysis is undermined by a critical data error in the SEIR section, a conservation-violating bug in the SVEIPR transition equations, and the complete absence of profile likelihood confidence intervals.

**Strengths:** The SVEIPR model shows genuine modeling ambition by incorporating vaccination dynamics and time-varying parameters. The computational infrastructure for the SVEIPR analysis is solid: Np=2000 for optimization, Np=5000 for likelihood evaluation, replicated pfilter with logmeanexp, and trace plots showing convergence. The iterative model development (SEIR → SVEIPR) is scientifically motivated. The ARIMA analysis includes appropriate ACF/PACF examination and residual diagnostics.

**Weaknesses:** (1) The SEIR section silently uses Washtenaw County, Michigan data instead of King County, Washington, invalidating all SEIR-section conclusions. (2) The SVEIPR reinfection transition samples from the infected compartment I instead of the recovered compartment R, and the R compartment is never decremented, producing a population that grows artificially over time. (3) No profile likelihoods are computed for any model. (4) The ARIMA model applies d=1 differencing to data that has already been first-differenced, effectively fitting a second-differenced model. (5) The normal measurement model in SVEIPR can produce negative case counts.

---

## Major Issues

### 1. SEIR section silently uses wrong county data

In the SEIR "Model Introduction" chunk (blinded.Rmd, lines 175-184), the data loading code reads:

```r
sea_data = full_data %>% filter(Admin2 == "Washtenaw", Province_State == "Michigan")
```

This overwrites the King County variable with Washtenaw County, Michigan data and writes a new `seattle_covid.csv` that is then loaded as the SEIR model input. The introductory analysis, all motivation, and the SVEIPR model all use King County, Washington. The SEIR local search (loglik -1195) and global search (loglik -1194) are therefore conducted on data from the wrong county entirely. All parameter estimates, convergence conclusions, and simulation comparisons in the SEIR section are invalid with respect to the stated research question.

The fix is straightforward: change the filter to `Admin2 == "King", Province_State == "Washington"` in this chunk, matching the initial data processing and the SVEIPR section.

### 2. Conservation violation and wrong compartment in SVEIPR reinfection transition

The reinfection transition (R to S) contains two simultaneous bugs (blinded.Rmd, lines 599-605).

Bug 1 — wrong source compartment: `double dN_RS = rbinom(I, 1 - exp(-mu_RS * dt));` draws reinfection individuals from I (infected), not R (recovered). This means infected individuals, not recovered individuals, trigger the reinfection pathway.

Bug 2 — R compartment never decremented: In both vaccine and non-vaccine branches, R is updated as `R += dN_PR + dN_IR` with no subtraction of dN_RS. Individuals who "reinfect" are added to S but never removed from R.

The net effect is that total population S+V+E+P+I+R grows by dN_RS at every time step. Over 163 weeks with mu_RS=0.5 and a non-negligible infected population, this accumulation is substantial and invalidates the population dynamics. The correct code should draw from R and decrement R by dN_RS.

This error is course-confirmed as a genuine review point: "Compartment model that violates conservation of individuals (compartments don't sum to population)" is listed as a flawed practice in the course conventions.

### 3. No profile likelihoods computed for any parameter

Neither the SEIR nor the SVEIPR section computes profile likelihood curves. The only form of uncertainty quantification offered is an informal "poor man's profile likelihood confidence interval" described for gamma and eta in the SVEIPR global search results — this consists of reading the range of values from the pairs scatter plot for the top results, not from a proper profile. A profile likelihood requires maximizing over all nuisance parameters at each fixed value of the target parameter (Wheeler et al. 2024, §Parameter identifiability). The scatter-plot range approach produces intervals that depend on the arbitrary distribution of starting points and do not correspond to the Wilks 95% threshold.

For a model with over 20 free parameters in the SVEIPR, the absence of profiles means there is no evidence that key parameters (especially rho, tau, mu_EPI, and the b/c multipliers) are individually identifiable. The 531 weakness reference (Error 1.9) identifies this as a major issue.

### 4. Over-differencing in ARIMA model

The data processing creates `sea_df$cases` as first differences of weekly cumulative case counts — that is, weekly new cases (blinded.Rmd, lines 29-33). The ARIMA model is then fit with `arima(sea_df$cases, order=c(3,1,3))`, which applies d=1 differencing again (lines 87-88 and 105). The AIC table applies the same double-differencing consistently across all candidate models. The result is that the selected ARIMA(3,1,3) model actually fits an ARMA(3,3) to the second differences of weekly cumulative cases, not the first differences as described.

The paper states: "doing the difference operation will make it look more stationary... we choose to proceed with ARIMA(3,1,3) model," implying a single round of differencing. The discrepancy between description and implementation means the model being analyzed is not the model being described. At minimum, the ACF and PACF shown on `sea_df$cases` (Figure 2-3) describe the first-differenced series, while the fitted model operates on its second difference.

---

## Computational and Diagnostic Assessment

**Convergence:** The SVEIPR local search trace plots show loglik converging upward over ~60 iterations across 10 parallel runs, which is satisfactory. The SVEIPR global search also shows trace plots. The SEIR local search (Np=1000, Nmif=50) is modest but adequate for a simpler model. The SEIR global search, however, uses only Np=200 — well below the course run_level=2 standard of Np=1000 — making the global search likelihood evaluations during optimization unreliable.

**Particle filter:** ESS is monitored via the pfilter plot for the initial SVEIPR guess parameters. Likelihood re-evaluation uses Np=5000 with 10 replicates and logmeanexp — this is correct and appropriate. The reported loglik.se values (0.0056-0.0077 for SVEIPR) confirm the Monte Carlo variance is negligible relative to likelihood differences being compared.

**Conditional log-likelihoods:** Not plotted. The per-time-step log-likelihood plot (conditional log-likelihood) would be especially informative here given the model's difficulty capturing the peak around week 100. This tool would help diagnose whether the poor fit is localized to specific outbreak waves (Wheeler et al. 2024, §Model diagnostics).

**Profile likelihoods:** Absent — see Major Issue 3.

**Computational scale:** The SVEIPR analysis uses run_level=3 parameters (Np=2000, Nmif=200, 100 global starting points), which is appropriate. No CPU-hours are reported.

---

## Reproducibility Assessment

**Code availability:** Code is present in the repository. The SVEIPR section saves parameter files to `SVEIPR_results_run_level_3/pomp_model_params.csv`, which is a positive practice (final parameter archival). The SEIR section uses `bake()` to cache intermediate results.

**Final parameters:** The SVEIPR model archives the best parameter vector in a CSV file. This is good. The SEIR model does not explicitly archive final parameters beyond the cached `.rds` files.

**Model-code consistency:** The SVEIPR measurement model description in the text is not fully explicit (the use of a normal approximation rather than negative binomial is not announced), and the code uses `pnorm`/`rnorm` while the SEIR section uses `dnbinom_mu`/`rnbinom_mu`. This shift in measurement model design is not highlighted as a model choice in the text.

**Package versions:** No `sessionInfo()` or `renv` lockfile is provided. The `pomp` package API changes substantially across versions; results may not reproduce on current CRAN releases without version pinning.

**Code quality:** `rm(list = ls())` appears at line 414, which is flagged in reproducibility standards as a bad practice that modifies the global workspace without user consent and can silently break pipelines.

---

## Minor Issues

- The SVEIPR vaccination transition rate is `mu_SV * (I+P)/N`, making vaccination uptake proportional to current prevalence. This non-standard assumption (vaccination responding to infection levels) is not epidemiologically standard and is not justified. A fixed or covariate-driven vaccination rate would be more interpretable.

- The global search for SVEIPR sets upper bounds for b7 and b8 at 15.0, but the best model found reports b7=16.2 and b8=18.7. Since mif2 perturbs parameters after the random initialization, values can exceed the initial design bounds — but the text describes these as "in a reasonable range" without explanation of what a reasonable range for these multipliers would be. Identifiability of b7 and b8 relative to Beta is not discussed.

- The SVEIPR measurement model uses a normal approximation for count data (dmeas uses pnorm; rmeas uses rnorm). While the variance formula `sqrt((tau*H)^2 + rho*H)` produces overdispersion, the normal distribution allows negative simulated counts. The code clamps rmeas to 0, but the density dmeas does not account for this clamping, creating an inconsistency between the simulator and the evaluator.

- The paper states the SEIR model's "local search successfully converges to the local maximum log likelihood" with the loglik converging to approximately -1200. However, since this analysis uses the wrong county's data (Major Issue 1), the convergence claim pertains to the wrong optimization target.

- Several key SVEIPR rate parameters (Beta=1.01, mu_PR=0.93, mu_IR=0.98, mu_RS=0.5, alpha=0.4, mu_SV=0.5) are fixed throughout both local and global searches. These are not estimated with uncertainty, and the rationale for fixing them at these specific values (rather than optimizing them) is not provided. The transition rate from P to R (mu_PR=0.93) and from I to R (mu_IR=0.98) correspond to recovery within roughly one week on average — while these are plausible for COVID-19, they are not justified against independent clinical evidence, as recommended by Wheeler et al. (2024, §Corroboration with scientific knowledge).

- The ARIMA log-likelihood is not reported in numeric form. Only AIC values are provided. Reporting the log-likelihood of the best ARIMA model would enable an informal cross-model comparison with the POMP models, which use the same observed data and are therefore on the same likelihood scale. (Note: the AIC scales differ between ARIMA and POMP due to different observation model normalizations, so direct AIC comparison requires care per 531-conventions.md.)

- The "poor man's profile likelihood" CIs for gamma and eta are derived from the marginal range of parameter values in the top global search results, not from a proper likelihood ratio criterion. The resulting intervals (e.g., gamma in (0.806, 0.988)) depend on the coverage of the random starting-point distribution rather than the Wilks 95% threshold.

- Initial conditions for SVEIPR are fixed at E=1000, I=500, P=500. These are substantially larger than the SEIR initialization (E=20, I=5) and are not justified against the specific outbreak context. No sensitivity analysis is performed.

- The QQ-plot of ARIMA(3,1,3) residuals shows severe tail deviation (both ends). This is acknowledged but not addressed — no transformation is considered, and the heavy-tailed residuals are consistent with the overdispersed count structure of the data. A log transformation or a count-appropriate model (e.g., ARIMA on log-cases) is not explored.

---

## Recommendation

Major revision required. The two most critical issues — the wrong-data bug in the SEIR section and the compartment conservation violation in the SVEIPR reinfection pathway — must be corrected before the analysis is valid. The ARIMA over-differencing should also be corrected. Once the data and model bugs are fixed, profile likelihoods should be computed for at least the key biological parameters (rho, mu_EPI, and representative b_i) to support any inferential claims about transmission dynamics. The measurement model choice (normal vs. negative binomial) should be explained and the dmeas/rmeas inconsistency resolved.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W24/project08/blinded.Rmd`
