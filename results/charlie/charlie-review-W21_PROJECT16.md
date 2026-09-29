# Peer Review: W21 Project 16
## "Volatility analysis on the Shanghai Composite Index"

---

## Paper Metadata

| Field | Details |
|-------|---------|
| **Inference method** | IF2 (mif2) + replicated pfilter for log-likelihood evaluation |
| **R packages used** | pomp, tseries, fGarch, doParallel, foreach, doRNG |
| **Code publicly available** | Yes (submitted with project, bake/RDS files included) |
| **Data publicly available** | Yes (CSV included: "Shanghai Composite Historical Data.csv") |
| **Benchmark comparison included** | Yes — GARCH(1,1) used as benchmark |

---

## POMP Checklist Scorecard

| # | Practice | Status | Notes |
|---|----------|--------|-------|
| 1 | Likelihood-based inference | ~ | IF2 + replicated pfilter used correctly; logmeanexp applied properly |
| 2 | Benchmark comparison | ~ | GARCH(1,1) compared on log-likelihood, but AIC not used to account for parameter count difference |
| 3 | Quantitative goodness-of-fit reporting | ~ | Log-likelihoods reported for both models; no AIC comparison |
| 4 | Model diagnostics | ✗ | No forward simulation, no ESS monitoring, no conditional log-likelihoods; trace plots produced but never discussed |
| 5 | Parameter identifiability and uncertainty | ~ | Profile likelihood computed for phi only; no confidence interval explicitly stated; phi MLE value missing from text |
| 6 | Computational adequacy | ~ | run_level=2 parameters used; convergence traces produced but not discussed |
| 7 | Forecast methodology | N/A | No forecasting attempted |
| 8 | Model variations and nested comparisons | ✗ | Only one POMP model considered |
| 9 | Stochasticity | ✓ | Stochastic volatility model with process and measurement noise |
| 10 | Reproducibility and extendability | ~ | Code and data included; no package version pinning; no sessionInfo() |
| 11 | Corroboration with scientific knowledge | ✗ | phi estimated near 1 but not compared to financial literature |
| 12 | Measurement model specification | ✓ | Gaussian measurement model consistent between text and code |
| 13 | Initial conditions | ~ | G_0 and H_0 estimated; sensitivity not assessed |

---

## Summary

This project fits a stochastic volatility (SV-in-Mean) POMP model to weekly log-returns of the Shanghai Composite Index (SSE) from 2010 to 2021, using GARCH(1,1) as a benchmark. The model adopts the Breto (2014) specification with leverage effects, and inference is performed via IF2 with replicated particle filter likelihood evaluation. While the project correctly applies the core POMP workflow (local search, global search, profile likelihood), the POMP model underperforms the GARCH benchmark (log-likelihood 1264 vs. 1269.58) and the authors draw an incorrect conclusion about how to address this. The profile likelihood analysis is left incomplete — the phi MLE value is missing from the text — and the paper lacks the simulation-based diagnostics that are essential for validating a POMP model.

**Strengths:**
- Correct use of logmeanexp for aggregating replicated particle filter estimates
- Profile likelihood computed over phi with appropriate Wilks cutoff for 95% CI
- Global search implemented with a parameter box to escape local optima
- GARCH benchmark included with quantitative log-likelihood comparison

**Weaknesses:**
- Independence concluded from ACF of demeaned returns without checking squared returns (ACF of squared returns would motivate the volatility model)
- POMP underperforms GARCH but the authors respond by recommending "increase computational force" rather than revising model structure
- Profile likelihood conclusion is literally incomplete: "when phi = ." with the value missing
- No simulation-based model diagnostics (no forward simulation, no ESS monitoring)
- Global search phi box (0.9950, 0.9999) is far too narrow relative to the profile range (0.80, 0.9999)

---

## Major Issues

### 1. Incorrect conclusion that returns are "independent" from ACF; missing ARCH-effect diagnostic

The ACF of demeaned log-returns shows no significant autocorrelation, and the authors conclude: "we can safely assume that the data are all independent" (Section 2.1). This conclusion is wrong for two reasons.

First, ACF measures only *linear* autocorrelation; absence of linear autocorrelation does not imply independence. The standard motivation for volatility models (GARCH and stochastic volatility) is volatility clustering, which appears as autocorrelation in the *squared* returns, not the returns themselves. The ACF of squared returns is the canonical diagnostic for ARCH effects and is essential for motivating this class of models. The paper never shows this plot.

Second, by declaring independence, the paper undercuts its own motivation: if the data were truly independent, neither GARCH nor a stochastic volatility model would add value over an i.i.d. model. The authors should replace the independence claim with a statement about the absence of linear autocorrelation in the levels, and add an ACF of squared returns to demonstrate the ARCH effects that motivate the models.

### 2. POMP underperforms GARCH; wrong response recommended (Error 1.15, CC-Yes)

The POMP model achieves a maximum log-likelihood of 1264 (from global search) compared to GARCH(1,1)'s log-likelihood of 1269.58 — a gap of approximately 5.6 log-likelihood units. The POMP model also has more parameters (6: sigma_nu, mu_h, phi, sigma_eta, G_0, H_0) vs. GARCH(1,1)'s 3 (omega, alpha1, beta1), so on an AIC basis the POMP model performs even worse: ΔAIC ≈ 2*(5.6) + 2*(6−3) = 17.2 in favor of GARCH.

The conclusion (Section 5) attributes this outcome to "limitation of time and computational sources" and recommends: "it is necessary to use this preliminary results from the POMP model and increase the computational force to achieve a better result subsequently." This is the classic student misconception explicitly tested in MT2 Q4-02: when a mechanistic model fits substantially worse than a benchmark, the correct first response is to revise the *model structure* — examine residuals, add overdispersion, reconsider the specification — not to simply increase Np or Nmif. More computation can only help if the model is fundamentally sound. The authors should instead examine why the stochastic volatility model fails to surpass GARCH (e.g., whether the leverage effect or the random walk component in G_n is helping), and consider structural modifications.

### 3. Profile likelihood conclusion is incomplete: phi MLE value missing from text

Section 4.4 concludes: "the maximum log-likelihood over phi is achieved when phi = ." — the actual phi value is absent from the sentence. No confidence interval for phi is reported either. The profile plot shows the 95% Wilks cutoff (red horizontal line at max(logLik) − 0.5*qchisq(0.95, df=1) ≈ max − 1.92), but the text never states the point estimate or the interval endpoints. This renders the profile likelihood analysis incomplete as a scientific result.

The text also states the result "looks contradicted to our assumption" and that "as phi approaches 1, the likelihood becomes unstable" — but these observations are not quantified. The authors should report the phi MLE and the 95% confidence interval explicitly.

### 4. No simulation-based model diagnostics

The POMP model is built and optimized but never subjected to the standard simulation-based validation checks. Specifically missing are:

- Forward simulation from the fitted model parameters: no plots comparing simulated log-return trajectories to observed data
- Effective sample size (ESS) monitoring: the paper does not report or discuss ESS during filtering, so it is unknown whether the particle filter is degenerating
- Conditional log-likelihoods per time step: no per-observation likelihood plots to identify periods of poor fit
- Filtering distribution: simulations from the filtering distribution (conditioned on observed data) are not distinguished from unconditioned forward projections

Per the POMP checklist (Wheeler et al. 2024, §Model diagnostics), simulation-based diagnostics are the primary tool for understanding where and how a model succeeds or fails. Their absence means the model's fit is assessed only through summary log-likelihood values, which cannot detect temporal periods of misfit.

### 5. Global search parameter box for phi is inconsistent with profile range

The global search box (Section 4.3) specifies `phi = c(0.9950, 0.9999)`, constraining phi to a very narrow interval near 1. However, the profile likelihood (Section 4.4) examines phi across the range [0.80, 0.9999]. This inconsistency means the global search cannot explore lower phi values that the profile later examines. If the true MLE lies at phi < 0.995 — which the profile might reveal — the global search will miss it entirely. The global search box for phi should be expanded to match or exceed the profile range.

### 6. Convergence diagnostics produced but never discussed

The code calls `plot(if1)` (local search trace) and `plot(if.box)` (global search trace), which presumably generate IF2 convergence plots in the HTML output. However, the text contains no interpretation of these plots. The paper never states whether the log-likelihood converges upward across iterations, whether the terminal likelihoods from different runs are consistent, or whether any signs of non-convergence are present. Per the course standard (Error 1.8), reporting convergence diagnostics requires both showing the plots and interpreting them. The authors should discuss what the trace plots show.

---

## Computational and Diagnostic Assessment

**Convergence:** IF2 convergence trace plots are generated by `plot(if1)` and `plot(if.box)` but are not referenced or interpreted in the text. The local search uses 20 replicate mif2 runs (Nreps_local=20), and the global search uses 50 (Nreps_global=50), both with Nmif=50 iterations. The run_level=2 settings (Np=2000, Nmif=50) are reasonable for preliminary work. Without discussion of the trace plots, convergence cannot be assessed from the text alone.

**Particle filter:** ESS is not monitored or reported. The particle count (Np=2000 for local/global search, Np=1000 for profile) is stated in the code but not discussed. No evidence is presented that the particle count is sufficient for stable estimates.

**Conditional log-likelihoods:** Not computed or plotted. The authors report only the summary (maximum) log-likelihood.

**Profile likelihoods:** Profile computed over phi using 50 grid points from 0.80 to 0.9999 (log scale) with nprof=2 starts per grid point (100 total runs). The 95% Wilks cutoff is correctly applied. However: (a) only 2 optimization starts per phi value is sparse; (b) the profile uses Np=1000 rather than the Np=2000 used for optimization; (c) neither the phi MLE nor the confidence interval is stated in the text.

**Computational scale:** The paper uses `bake()` for caching, and intermediate RDS files are included in the submission. Total CPU-time is not reported.

---

## Reproducibility Assessment

**Code availability:** Code is embedded in the Rmd file with bake/RDS caching. Intermediate RDS files (pf1-2.rds, mif1-2.rds, box_eval-2.rds, profile_phi-2.rds) and parameter CSV (Shanghai_params.csv) are included, allowing result reproduction without full re-optimization.

**Final parameters:** Shanghai_params.csv is provided. The final MLE parameter vector can be extracted from this file.

**Model-code consistency:** The measurement model `dmeasure = dnorm(y, 0, exp(H/2), give_log)` is consistent with the mathematical specification `Y_n = exp(H_n/2) * epsilon_n` where epsilon_n ~ N(0,1).

**Package versions:** No sessionInfo() or renv lockfile is provided. Package versions for pomp, fGarch, tseries are not pinned.

**Auxiliary data:** The CSV data file is included. No additional covariates are needed beyond the closing price data.

---

## Minor Issues

- **Missing intercept in GARCH model equation (Section 3.2):** The model summary states "GARCH(1,1) model is V_n = 0.143 Y²_{n-1} + 0.822 V_{n-1}" — the constant term α_0 (omega) is omitted. The correct GARCH(1,1) specification is V_n = α_0 + α_1 Y²_{n-1} + β_1 V_{n-1}. The fGarch summary output includes omega ≈ 0.000048 which should appear in the equation.

- **Double-logarithm in exploratory plot (Section 2.1 code):** The code `plot(Date, log(Price), type="l", log="y", ...)` first takes log(Price) then applies `log="y"` to the axis, effectively displaying log(log(Price)). The authors should either plot `Price` with `log="y"` or plot `log(Price)` without `log="y"`.

- **Heavy-tailed residuals inadequately addressed (Section 3.2):** The QQ-plot shows clear heavy tails for GARCH residuals. The authors note this "violates the normality assumption" but explain it as "the sample is a little biased to the true distribution." This explanation is vague. A more appropriate discussion would consider using a Student-t innovation distribution for the GARCH model, which is standard practice for financial returns.

- **Local search uses a single starting parameter set:** All 20 mif2 runs in the local search start from the same `params_test`. A proper multi-start local search should use diverse starting values to better characterize the likelihood surface.

- **AIC not used for POMP vs GARCH comparison:** The log-likelihood comparison (1264 vs 1269.58) does not account for the parameter count difference. The POMP model has 6 parameters vs. GARCH(1,1)'s 3. Using AIC would further widen the gap in favor of GARCH and should be reported.

- **tseries::garch used for model selection, fGarch::garchFit for fitting (Error 2.9):** The AIC table uses `tseries::garch` while the actual model summary uses `fGarch::garchFit`. Different packages may use different likelihood normalizations. The minimum AIC from tseries (-2528.11) corresponds to a log-likelihood of approximately (2528.11 − 2k)/2, and the fact that this roughly aligns with fGarch's 1269.58 suggests the normalizations are similar here, but this consistency should be verified explicitly.

- **Data description ambiguity:** The paper describes the data as "570 observations of weekly average closing price" but closing prices are point-in-time observations, not weekly averages. The data description should clarify whether each observation is an end-of-week closing price or a weekly average.

- **Profile nprof=2 is sparse per phi value:** With only 2 optimization starts per phi grid point, the profile envelope may miss the true maximum at some phi values, particularly where the likelihood surface is multimodal.

---

## Recommendation

**Major Revision.** The core POMP workflow (IF2, replicated pfilter, profile likelihood, global search) is implemented, showing familiarity with the course methods. However, several critical deficiencies must be addressed before this constitutes a satisfactory analysis:

1. The independence conclusion in Section 2.1 must be replaced with a correct interpretation, and ACF of squared returns must be added to motivate the volatility model.
2. The missing phi value in the profile conclusion must be filled in, and a 95% confidence interval for phi must be stated.
3. Simulation-based model diagnostics (forward simulation, ESS monitoring) must be added.
4. The conclusion about "increasing computational force" must be replaced with a discussion of model structure revisions motivated by the POMP model's underperformance relative to GARCH.
5. The global search phi box must be expanded to be consistent with the profile range.
6. Convergence trace plots must be interpreted in the text.

---

## Files Consulted

**Skill files:**
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/guided-pomp-review/assets/rev_template_pomp.qmd`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/rerun/isolated/Skills/531_references/531-weakness-reference.md`

**Project files:**
- `/Users/jin/Desktop/ai/rerun/isolated/projects_Material/project/final_project_W21/project16/blinded.Rmd`
