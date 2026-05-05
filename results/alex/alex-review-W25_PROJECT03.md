# Peer Review: W25 Project 03 — Flu Cases in Michigan

## Summary

This project analyzes weekly influenza cases in Michigan (2023–2025) using ARMA/SARMA baseline models and a POMP-based SEIRS model with seasonal transmission. The overall structure is reasonable and covers the expected components: data exploration, frequency analysis, classical time series fitting, compartmental POMP modeling, local/global search, and profile likelihood. However, there are a number of methodological, interpretive, and implementation weaknesses that limit the reliability of the conclusions.

---

## Weaknesses (Most Critical First)

### 1. Profile Likelihood is Methodologically Flawed — Single-Path Rather Than Multi-Start

The profile likelihood for each parameter is computed by fixing that parameter, running a single `mif2()` call from the MLE, and evaluating with one `pfilter()` call. This is not a valid profile likelihood procedure. A proper profile requires running optimization over all other parameters for each fixed value, typically using `profile_design()` with multiple starting points within a high-likelihood region to avoid local optima. With only one optimization path per grid point, the resulting curve reflects the behavior of a particular local optimizer rather than the true profile likelihood surface. The authors acknowledge this limitation but still report and interpret the resulting confidence intervals as if they were valid. The CIs reported (e.g., [0.526, 0.570] for `amp`, singleton CIs for `phase` and `rho`) cannot be trusted as genuine 95% confidence intervals.

### 2. Singleton Confidence Intervals Misinterpreted

The profile likelihood analysis yields singleton CIs for `phase` ([2.7, 2.7]) and `rho` ([0.00015, 0.00015]). The paper characterizes these as evidence of "limited identifiability" and "poor identifiability," respectively, but this is the wrong interpretation. Singleton CIs result when the likelihood drops below the cutoff threshold on both sides of a single grid point — this is a symptom of a poorly resolved profile (too coarse a grid, or a non-monotone/jagged curve from particle filter noise), not a sharp peak indicating identifiability. The profile grid for `rho` uses only ±20% of the MLE value (10 points), and for `phase` only ±10 weeks (10 points), which are far too coarse and narrow to characterize the profile reliably. The authors then conclude "the MLE is highly sensitive to small variations," which is the opposite of what a singleton CI from a coarse grid indicates.

### 3. Log-Likelihood Comparison Between ARMA/SARMA and POMP is Inappropriate

The paper compares log-likelihoods directly across ARMA (-497.31, -495.40) and SEIRS POMP (-375.79) models and concludes the POMP model is superior. However, the ARMA models are fitted to first-differenced data (not the original series), while the SEIRS model is fitted to the original case counts. These likelihoods are computed under different transformations and are therefore not directly comparable. The comparison is presented without any acknowledgment of this inconsistency.

### 4. Data File Path Inconsistency

The Rmd reads the data as `read.csv("../Data/flu_michigan.csv")`, but the data file `flu_michigan.csv` resides in the project folder itself (`project03/flu_michigan.csv`), and there is no `Data/` subdirectory under `final_project_w25/`. This means the Rmd as submitted would fail to load data when rendered from the project directory. The HTML output was presumably generated with a different working directory or path. This is a reproducibility failure.

### 5. Insufficient Global Search — Only 10 Starting Points, 50+50 Iterations

The global search uses only 10 random starting points with `Np = 1000` particles and `Nmif = 50` followed by `continue(Nmif = 50)` — for a 13-dimensional parameter space (8 dynamic parameters plus 4 initial state proportions plus N). This is a very small global search. Standard practice for a model of this complexity uses at least 50–200 starting points and more iterations. The reported improvement over local search is negligible (log-likelihood of -375.77 vs -375.83), suggesting the global search barely explored beyond the local optimum. The authors claim "the global search successfully explored regions of the parameter space that the local search did not reach," but this is not supported by such marginal improvement.

### 6. Amplitude Parameter Constrained Incorrectly

The seasonal transmission rate is defined as `Beta(t) = Beta0 * (1 + amp * cos(...))`. For this to represent a physically meaningful (always positive) transmission rate, `amp` must satisfy `0 <= amp <= 1`. The `partrans` specification applies a logit transform to `amp`, which correctly constrains it to (0, 1) on the transformed scale. However, the initial starting parameter value for `amp` is 0.47, and the global search samples `amp ~ runif(1, 0.01, 0.9)`. The profile likelihood grid spans the reported MLE ± 0.1. The reported MLE amplitude from global search and its CI are in the range 0.526–0.570 — near the constraint boundary but not flagged as potentially boundary-constrained. No discussion is given about whether the logit-transformed `amp` converges near its boundary, which would signal a potential constraint issue.

### 7. Frequency Analysis Interpretation Error

The authors identify the dominant frequency as approximately 0.0167 (cycles per week), corresponding to a period of ~60 weeks (~1.15 years). However, the data spans only about 116 weeks (roughly 2.2 years), so there are fewer than two complete cycles in the dataset. For an annual flu phenomenon, the expected dominant frequency would be approximately 1/52 ≈ 0.019 cycles per week. The authors do not reconcile the discrepancy between the periodogram-derived period of ~60 weeks and the known annual flu seasonality, nor do they discuss whether this is an artifact of the short data span, the strong outbreak in weeks 105–116, or a genuine feature of the signal.

### 8. ARMA Differencing Applied to the Wrong Series

In the ARMA section, the code applies differencing to `flu_ts` (the original time series) but then fits `arma_aic_table(diff_flu_ts, ...)` with `D=0`. This means the series used for model fitting is the first-differenced original (not the log-transformed) series, even though the paper states "we first applied a log transformation" and then differenced "the transformed data." The code on line 109 differences `flu_ts`, not `log_flu_ts`. This inconsistency between the narrative and the code undermines the stated rationale for the transformation.

### 9. Very Small Number of Particles in Local Search Likelihood Evaluation

The local search uses `Np = 1000` during `mif2()` and `Np = 2000` for the immediate post-mif2 likelihood evaluation within the foreach loop. The final consolidated log-likelihood is re-evaluated using `Np = 5000` particles over only 10 replicates. While 5000 particles is reasonable for a single evaluation, using only `Np = 2000` during the initial across-replicate comparison means the "best" trajectory was selected using a noisy likelihood estimate. Monte Carlo error in the particle filter likelihood can be substantial with 2000 particles for an epidemic model over 116 time points.

### 10. Profile Likelihood Grid is Too Coarse and Narrow

Each profile likelihood analysis uses only 10 grid points. For `amp`, the grid spans ±0.1 around the MLE; for `Beta0`, ±0.5; for `phase`, ±10 weeks; and for `rho`, ±20% of the MLE value. With only 10 points per profile and a single noisy pfilter evaluation at each point, the resulting curves will have substantial Monte Carlo noise that can produce artifacts (e.g., non-monotone behavior near the peak), making CI boundary detection unreliable. Best practice uses at least 20–40 grid points and multiple pfilter replicates averaged with `logmeanexp` at each point.

### 11. Phase Parameter Value Exceeds Natural 52-Week Range at MLE

The global search reports a best-fit `phase` value of approximately 52.64 weeks. Since the cosine function has period 52, a phase of 52.64 is nearly identical to a phase of 0.64 (modulo 52). The local search reports `phase = 1.27`. The summary states "higher phase value (52.64 vs 1.27), suggesting a different seasonality pattern." This interpretation is incorrect — 52.64 and 1.27 are nearly the same phase after modular arithmetic with period 52. This is an important interpretive error that also signals a lack of identifiability for the phase parameter that the authors missed.

### 12. Initial State Proportions Not Estimated in Global Search

The global search samples initial state proportions `S0 ~ runif(1, 0.01, 0.8)`, `E0 ~ runif(1, 0.001, 0.1)`, `I0 ~ runif(1, 0.001, 0.1)`, `R0 ~ runif(1, 0.001, 0.5)` independently and uniformly. However, these proportions are constrained by the barycentric transform in `partrans`, which enforces `S0 + E0 + I0 + R0 = 1` (they are treated as simplex coordinates). Sampling them independently with uniform marginals and potentially summing to values very different from 1 means many starting points will have poorly conditioned initial states before the barycentric normalization. More importantly, the initial state proportions are allowed to vary in the global search starting design but their rw.sd is not included in the local random walk template, meaning they are fixed during the mif2() runs in the global search. This means the initial conditions are not being optimized — only the eight dynamic parameters are. If initial conditions matter for fit, this is a significant omission.

### 13. Residual Diagnostics Are Cursory

The ARMA and SARMA residual diagnostics are performed using `checkresiduals()` (from the `forecast` package) but are discussed minimally. The Ljung-Box test results from `checkresiduals()` are not explicitly reported or discussed. The paper notes "certain events or seasonality that have not been captured" and "residuals are normally distributed but contain some extreme values," but no quantitative assessment is given. Furthermore, for a flu epidemic with heavy-tailed counts, the normality assumption implicit in standard ARMA residual assessment is not appropriate, and this is not acknowledged.

### 14. SEIRS Model Borrowed Heavily from a Prior Project Without Sufficient Adaptation

The authors acknowledge adapting the SEIRS model from a W24 Group 5 project and that the code structure and initialization approach are taken from that source. The seasonal transmission function was modified to use cosine instead of sine. While citation is present, the analytical contribution from this project is limited: the core model architecture, initialization scaling trick, and overall parameter estimation workflow appear to be essentially carried over. The modifications (cosine vs. sine, Michigan population) are incremental. The report would benefit from a deeper original contribution.

### 15. SARMA Model Comparison with Fixed (p, q) from ARMA Is Not Fully Justified

The authors fix the regular ARMA order at (p=0, q=1) from the ARMA AIC table and then search only over seasonal (P, Q). This sequential selection procedure does not guarantee the globally optimal SARMA model — the optimal seasonal parameters may differ for different regular ARMA orders. A more rigorous approach would jointly optimize over (p, q, P, Q). Additionally, only the differenced original series (not log-differenced) is used for SARMA fitting, which may not be appropriate given the non-constant variance in the original series.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project03/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w25/project03/flu_michigan.csv`
