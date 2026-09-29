# Review: W25 Project 07
## *Dengue Fever in the U.S. States and Territories (2022–2023)*

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) + particle filter (pfilter) |
| **R packages used** | pomp, forecast (Arima), denguedatahub, doFuture, doParallel |
| **Code publicly available** | Yes — Rmd submitted via course git repo |
| **Data publicly available** | Yes — via `denguedatahub` R package |
| **Benchmark comparison included** | Yes — SARIMA(2,0,0)(0,0,1)[53] |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | mif2 + pfilter used correctly; logmeanexp applied |
| 2 | Benchmark comparison | ~ | SARIMA fitted; log-likelihood compared but AIC scale difference not noted |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported numerically; no AIC table for POMP models |
| 4 | Model diagnostics | ~ | ESS/conditional loglik shown for SIRS only; no analogous diagnostics for SEIR |
| 5 | Parameter identifiability and uncertainty | ✗ | No profile likelihoods computed for any model; code variables defined but never used |
| 6 | Computational adequacy | ~ | SEIR adequate; SIRS global search uses only 20 starting points and Nmif=50 |
| 7 | Forecast methodology | N/A | No forecasting performed |
| 8 | Model variations and nested comparisons | ~ | SIRS and SEIR compared, but only qualitatively |
| 9 | Stochasticity | ✓ | Both models use binomial transitions; negative binomial measurement model |
| 10 | Reproducibility and extendability | ~ | Code present; no package version pinning; no sessionInfo(); some hardcoded indices |
| 11 | Corroboration with scientific knowledge | ~ | Parameter values loosely grounded in WHO/literature; population size choices not justified |
| 12 | Measurement model specification | ~ | Negative binomial used; k fixed without justification in SEIR |
| 13 | Initial conditions | ~ | SIRS parameterizes all initial fractions (good); SEIR hardcodes E=10, I=70 |

---

## Summary

This project analyzes weekly travel-associated dengue case counts for U.S. states and territories (2022–2023, 106 weeks) using three modeling approaches: a SARIMA benchmark, a stochastic SIRS model with a two-phase seasonal transmission rate, and a stochastic SEIR model with cosine-modulated seasonality. Parameters are estimated via iterated filtering (mif2) with particle filter likelihood evaluation. Both mechanistic models achieve log-likelihoods close to the SARIMA benchmark (~-440 vs. -445), which the authors interpret as favorable.

**Strengths:** The project demonstrates solid command of the POMP workflow — model specification via Csnippets, run_level framework, local and global searches, logmeanexp aggregation, and simulation-based visualization. Including a SARIMA benchmark and comparing log-likelihoods is commendable. The SIRS ESS and conditional log-likelihood diagnostics are appropriately presented.

**Weaknesses:** Neither model computes profile likelihoods, leaving parameter identifiability entirely unaddressed. The SIRS global search is severely underpowered relative to the SEIR search. The SEIR overdispersion parameter k is never estimated. Both models rely on population sizes that are epidemiologically implausible and unjustified. The SEIR initial conditions for E and I are hard-coded integers rather than estimated parameters. These gaps collectively undermine the reliability of the reported parameter estimates and model comparisons.

---

## Major Issues

### 1. No profile likelihoods for any model parameter

Neither the SIRS nor the SEIR model computes profile likelihoods. The Rmd defines `Npoints_profile` and `Nreps_profile` in both run_level blocks (lines 345–346 for SIRS; lines 934–935 for SEIR), but these variables are never used. Without profile likelihoods, it is impossible to assess whether any parameter is identifiable from the data, and the reported point estimates (β, γ, ξ, μ_EI, μ_IR, R₀) carry no quantified uncertainty. This is the most critical gap. Per Wheeler et al. (2024), §Parameter identifiability, "profile likelihoods should be computed to assess whether parameters are identifiable from the data." The authors should compute at minimum 2–3 profile likelihoods for key epidemiological parameters (e.g., β, recovery rate) and report MCAP confidence intervals.

(CC-Yes: Error 1.9 — Profile likelihood too sparse to identify the maximum; here the profile is entirely absent.)

### 2. SIRS global search severely underpowered relative to SEIR

The SIRS run_level block (lines 340–347) has four switch values and at run_level=3 evaluates to Nglobal=20 and Nmif=50. The SEIR run_level block (lines 931–938) has three switch values and at run_level=3 evaluates to Nglobal=100 and Nmif=100. This five-fold difference in global starting points and two-fold difference in mif2 iterations means the SIRS global search is far less thorough than the SEIR search. With only 20 starting points, the SIRS global optimum may not have been found, making the SIRS log-likelihood comparison unreliable. The four-value switch structure for SIRS (with the extra level appearing to be an aspirational run_level=4) suggests the intended high-effort settings were never executed. The SIRS global search should be re-run with at least Nglobal=100 and Nmif=100 before drawing conclusions from the SIRS–SEIR–SARIMA comparison.

(CC-Yes: Error 1.8 — Missing convergence diagnostics / inadequate search effort.)

### 3. Biologically implausible and inconsistent population size N

The SIRS model uses N=4e9 (4 billion) for initial simulations and the local search (line 427: `N=4e9`), then switches to N=3.25e8 (325 million) for the global search (line 599) without explanation. The SEIR model uses N=3.2e6 (3.2 million) throughout. These values span three orders of magnitude and none is justified. Four billion exceeds the entire world population and is physically impossible as a susceptible pool for U.S. travel-associated dengue. The relevant epidemiological denominator for travel-associated cases is ambiguous (U.S. travelers to dengue-endemic regions? U.S. population?), but the choice of N is directly confounded with the reporting rate ρ and the transmission rate β. Without fixing N on defensible grounds and justifying ρ accordingly, the fitted β values are not interpretable as transmission rates. The authors should specify the intended population, justify N, and verify that the product N × ρ is consistent with observed case counts.

### 4. SEIR overdispersion parameter k is never estimated

The SEIR `partrans` includes k in the log-transform list (line 842: `log=c("Beta","mu_EI","mu_IR","k","phi")`), suggesting k was intended to be estimated. However, the local search rw.sd specification (line 954) omits k, and the global search explicitly fixes k via `fixed_params <- coef(measSEIR, c("N","k"))` (line 1076). Consequently k=10 throughout, set by the initial guess. The overdispersion parameter directly controls the width of the negative binomial measurement distribution and thus affects all likelihood values. Fixing k at an arbitrary initial value without sensitivity analysis or justification materially affects the reported log-likelihoods and the simulation uncertainty bands. The authors should either estimate k jointly with other parameters or provide a principled justification for fixing k=10.

### 5. SEIR initial conditions E and I are hard-coded integers, not estimated

The SEIR `seir_rinit` Csnippet (lines 806–811) hard-codes E=10 and I=70, estimating only S via the parameter η. With only 106 data points, the latent initial state can have a substantial influence on the fitted likelihood. Hard-coding E and I at round-number guesses — with no sensitivity analysis and no exploration of alternative starting conditions — introduces an unquantified systematic error into the SEIR results. By contrast, the SIRS model correctly parameterizes all initial compartment fractions (S_0, I_0, R_0) as barycentric coordinates that are estimated via mif2. The SEIR model should parameterize E_0 analogously, or at minimum demonstrate robustness to the choice of initial conditions.

### 6. SIRS reporting rate rho is fixed at epidemiologically implausible values

The SIRS model fixes rho=1e-7 (one in ten million) in the initial and local-search phase (line 431: `fixed_params <- c(N=4e9, rho=1e-7)`), then silently changes to rho=4e-5 (one in 25,000) for the global search (line 599–601) without explanation. With N=4e9 and rho=1e-7, a weekly peak of ~200 reported cases would require ~2 billion actual infections, which is impossible. With N=3.25e8 and rho=4e-5, ~200 reported cases imply ~5 million actual infections per week in the U.S., which is also implausible for imported dengue. The combination of N and rho is not independently identifiable without external constraints; the authors must provide a principled argument for at least one of these values using surveillance coverage data or published estimates of reporting rates for dengue in the U.S.

### 7. No particle filter diagnostics for SEIR model

The SIRS section includes ESS and conditional log-likelihood diagnostics via `plot(sirs_pf)` at initial parameters (lines 466–476), and the authors correctly interpret the ESS and per-time-step log-likelihoods. The SEIR section contains no analogous diagnostics at any stage — no ESS plot, no conditional log-likelihood trace, no `plot(pfilter(...))` output. Without these diagnostics it is impossible to assess whether the SEIR particle filter is functioning adequately (e.g., detecting filter degeneracy or early-time-point poor fit). This asymmetry is unjustified given that the SEIR model is presented as the primary epidemiological contribution. The authors should add SEIR particle filter diagnostics at the MLE parameters before drawing conclusions about model fit.

### 8. Seasonal period inconsistency: SARIMA uses 53 weeks, POMP models use 52

The SARIMA model uses a seasonal period of 53 (lines 92, 103, 125: `period=53`) based on the correct observation that the dataset has 53 weeks per year. However, the SIRS transmission formula (line 369) divides by 52 (`2*pi*(t+d)/52`), and the SEIR transmission formula (lines 789–790) also uses `period=52`. This means the POMP models impose a seasonal cycle of exactly 52 weeks rather than the 53-week cycle in the data, introducing a systematic phase drift of approximately one week per year — visible over a two-year dataset. The POMP models should use period=53 to be consistent with the data structure, or the authors should explain why a 52-week period is the appropriate biological assumption.

---

## Computational and Diagnostic Assessment

**Convergence:** SIRS local search trace plots (lines 507–515) show parameter convergence across 20 mif2 runs. The log-likelihood panel appears to plateau around -440, suggesting adequate local convergence. SEIR local search traces (lines 962–969) are also shown. However, no global search convergence traces are presented for either model — only pairs plots of terminal parameter values. Pairs plots cannot distinguish whether the global search converged or whether the apparent cluster is a large local maximum.

**Particle filter:** ESS is monitored for SIRS at initial parameters. For SEIR, no ESS monitoring is performed at any stage. The SEIR local and global searches use Np=2000 (lines 977, 1094), which is adequate. The SIRS global search uses Np=1000 (from the switch at run_level=3, line 340).

**Conditional log-likelihoods:** Shown for SIRS initial parameters only. Absent for SEIR and for post-optimization SIRS.

**Profile likelihoods:** Not computed for any model (see Major Issue 1).

**Computational scale:** SEIR: Nglobal=100, Nmif=100, Np=2000. SIRS: Nglobal=20, Nmif=50, Np=1000. CPU-hours not reported. The discrepancy between model effort is substantial and unexplained.

---

## Reproducibility Assessment

**Code availability:** Complete Rmd submitted with bake() caching. All computational results are cached in `.rds` files keyed by run_level, enabling reproduction without full re-runs.

**Final parameters:** The SIRS local search results are written to `sirs_lik.csv` (lines 529, 674–679). SEIR results are stored in `results` and `local_logliks` objects but not written to standalone CSV files for the final parameters. Archiving final SEIR MLE parameters to a CSV would improve reproducibility.

**Model-code consistency:** The SIRS measurement model in code (`dnbinom_mu(reports, k, rho*H, give_log)`, line 393) and the SEIR measurement model (`dnbinom_mu(reports, k, rho*H, give_log)`, line 818) are consistent with the text description (negative binomial with mean rho*H).

**Package versions:** No `sessionInfo()` output, no `renv.lock`, and no explicit version pinning for `pomp`. The `pomp` API has changed substantially across versions; without version pinning, reproduction is not guaranteed on future package versions.

**Auxiliary data:** Data sourced from the `denguedatahub` package, which is publicly available. The SEIR data is loaded via hardcoded row indices `data[637:nrow(data), ]` (line 777). If the upstream package is updated and rows are added or reordered, this will silently select the wrong data.

---

## Minor Issues

- **rw.sd values below course standard for SIRS:** The SIRS local search uses rw.sd=0.01 for all parameters (lines 495–500). The course standard is rw.sd=0.02 on the log/logit scale (Ch 15, p31). Perturbations of 0.01 may slow convergence without being harmful, but the choice is unexplained.

- **ACF interpretation contradicts SARIMA specification:** The text states (lines 79–80) "The oscillating pattern...supports that the data is non-stationary," but the fitted SARIMA has d=0, D=0 (i.e., no differencing), implying the authors treated the series as stationary for fitting purposes. A sinusoidal ACF pattern is characteristic of a stationary seasonal process, not evidence of non-stationarity per se. This internal contradiction should be resolved.

- **SEIR phi parameter: log-transform is inappropriate for a phase shift:** The SEIR `partrans` includes phi in the log-transform list (line 842: `log=c("Beta","mu_EI","mu_IR","k","phi")`). This forces phi > 0, which may be appropriate if phi is defined in weeks (expected range 20–32 based on the global search bounds). However, the SIRS phase parameter d is unconstrained and ranges from -40 to 10 (line 606). The two models use different conventions for the phase shift (cosine vs. sine, d vs. phi), making direct comparison of phase estimates impossible. The authors should clarify these differences.

- **"Pandemic switch" terminology and justification:** The SIRS model's structural break is called a "pandemic switch" (lines 305, 338) but the data are from 2022–2023, after the acute COVID-19 pandemic phase. The text later acknowledges this represents "increased international travel during summer." Using the term "pandemic" for a seasonal travel-pattern break is misleading. Additionally, with week 29 falling in the first year of the two-year dataset, the switch fires once in year 1 (week 29) and once in year 2 (week 82), but the text implies it is a one-time structural break. This needs clarification.

- **SEIR global search pairs plot includes all results within 1000 log-likelihood units of max:** The filter `filter(results, loglik > max(loglik) - 1000)` (line 1108) retains results that are 1000 log-likelihood units below the maximum. For a dataset of 106 observations, 1000 log-likelihood units is an enormous range (roughly 9.4 per observation), producing a pairs plot that mixes runs that are essentially at the global optimum with runs that are catastrophically bad fits. A tighter filter (e.g., within 50 units of the maximum) would yield a more informative visualization.

- **SIRS pairs plot includes guess points without label contrast:** The SIRS pairs plot (lines 686–692) plots guesses in grey and results in red. However, the `all` data frame includes `bind_rows(guesses)` which introduces rows with NA log-likelihoods into the panel. The `loglik` panel of the pairs plot will contain NA rows, potentially distorting axis scaling. This should be verified in the output.

- **Missing ACF for residuals of SARIMA model:** The residual analysis for the SARIMA model (lines 218–229) presents a time series plot, histogram, and QQ-plot but omits an ACF of the residuals. ACF of residuals is the primary diagnostic for whether the model has captured all serial correlation. The text claims "no strong autocorrelation" but does not show the ACF residual plot to substantiate this claim.

---

## Recommendation

Major Revision. The project demonstrates solid technical execution of the POMP workflow and commendably includes a SARIMA benchmark comparison. However, the complete absence of profile likelihoods for either mechanistic model is a fundamental gap: without identifiability checks and confidence intervals, the reported parameter estimates cannot be interpreted or trusted. The severely underpowered SIRS global search, the unjustified and inconsistent population size choices, the hard-coded SEIR initial conditions, and the unfixed overdispersion parameter together cast doubt on whether the reported likelihoods represent genuine MLEs. The seasonal period inconsistency (52 vs. 53 weeks) is an additional structural error that should be corrected. The authors should (1) compute profile likelihoods for key parameters in both models, (2) re-run the SIRS global search with at least Nglobal=100, (3) justify and harmonize population size choices, (4) either estimate k in SEIR or justify fixing it, and (5) correct the seasonal period to be consistent across all models.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/README.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W25/project07/blinded.Rmd`
