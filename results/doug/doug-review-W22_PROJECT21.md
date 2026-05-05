# Peer Review: W22 Project 21
## "ARMA and POMP Analysis on COVID-19 Variants in the US"

---

## Summary

This project analyzes US daily COVID-19 case counts from January 2020 to April 2022, segmenting the data into three variant epochs (pre-Delta, Delta, Omicron) and fitting a distinct compartmental model to each: an SEIR model for pre-Delta, and SEIRV models (adding a vaccinated compartment) for Delta and Omicron. An ARMA(4,4) is fit to the full series as a benchmark. Local and global IF2 searches are conducted for each segment. The approach of epoch-segmented mechanistic modeling is scientifically motivated, and the authors correctly use iterated filtering (mif2) with multiple restarts and particle filtering for likelihood evaluation. However, the project is undermined by several critical implementation errors — most severely a dmeasure/rmeasure moment mismatch that renders all likelihood values and parameter estimates statistically invalid, a grossly incorrect vaccinated-compartment initialization, and the use of smoothed (7-day rolling average) non-integer data with a normal measurement model whose variance specification is internally inconsistent. No profile likelihoods are computed, no model diagnostics are presented, and the ARMA benchmark comparison is not made quantitatively comparable to the POMP log-likelihoods.

---

## Major Issues

### 1. Dmeasure/Rmeasure Standard Deviation Mismatch (All Three Models)

All three models share the same `dmeas` and `rmeas` Csnippets, which specify different standard deviations for the Gaussian measurement model. In `dmeas`, the standard deviation is defined as:

```
double sd_cases = sqrt(mean_cases * mean_cases);
```

which simplifies to `|mean_cases|` (i.e., coefficient of variation = 1). In `rmeas`, the standard deviation is:

```
reports = rnorm(rho*H, sqrt(rho*H));
```

which is `sqrt(mean_cases)` (a Poisson-like, variance-equals-mean specification). At typical case counts during the pre-Delta peak (~250,000 daily cases), `dmeas` uses SD = 250,000 while `rmeas` uses SD ≈ 500 — a factor of ~500 discrepancy. This means the likelihood evaluated by the particle filter uses a nearly flat Gaussian (any observation value is almost equally probable), while forward simulations use a sharply concentrated Gaussian. All three consequences follow: (a) particle filter weights are dominated by Monte Carlo noise rather than the observation signal, (b) IF2 converges under the `dmeas` model, not the `rmeas` model, and (c) goodness-of-fit figures (which rely on `rmeas`) do not reflect the estimated model. All reported log-likelihoods and parameter estimates are invalid under either intended specification. The fix is to choose a single scientifically motivated variance function — most naturally `sd_cases = sqrt(mean_cases)` (Poisson) or a negative-binomial equivalent — and apply it identically in both snippets. (Wheeler et al. 2024, §Measurement model specification; see also `pomp-dmeas-rmeas-moment-mismatch` skill.)

### 2. Vaccinated Compartment Initialization Incorrectly Scaled (Delta and Omicron Models)

In the Delta model's `seirv_rinit`, the vaccinated compartment is initialized as:

```
V = nearbyint(N * 0.3 * 0.01);
```

With N = 3e8, this gives V ≈ 900,000. However, the authors state in the text that 31.15% of the US population was vaccinated at the start of the Delta period, which corresponds to approximately 93 million individuals. The initialization is off by a factor of roughly 103 (it initializes 0.3% rather than 30.15% of the population). This severely misrepresents the initial epidemic state. The error propagates to R, which is computed as a residual from S and V; the R compartment will be inflated by ~92 million people to compensate, distorting the susceptible fraction and all transition-rate estimates. The Omicron model has a similar problem: it uses `V = round(N*(0.5945-0.5935))` = `round(3e8 * 0.001)` ≈ 300,000, apparently treating only the incremental change in vaccination rate (0.1 percentage points) as the vaccinated population rather than the total stock (~59.4% of 300M ≈ 178 million). Both initializations are incorrect by orders of magnitude. The fix is to initialize V to the total vaccinated fraction: `V = nearbyint(N * 0.3115)` for Delta and `V = nearbyint(N * 0.5945)` for Omicron.

### 3. Smoothed (Non-Integer) Observations Passed to a Normal Approximation Measurement Model

All three models use the 7-day rolling average of daily case counts (`avg_7`) as the observed variable (`reports = avg_7` in the data preparation step). This produces non-integer, autocorrelated observations. While the authors use a normal approximation measurement model (not `dbinom` or `dpois`), which avoids the integer-requirement failure mode, the autocorrelation introduced by the rolling mean nonetheless violates the conditional independence assumption underlying the factored POMP likelihood. Each observation `y_t` is a weighted average of the raw counts over the preceding 7 days, so consecutive observations share 6 out of 7 underlying raw counts. The factored likelihood `prod(p(y_t | x_t))` treats these as independent given the latent state, understating uncertainty. The more principled approach is to model the raw daily case counts directly, allowing the measurement model's dispersion parameter to capture day-to-day noise. If smoothing is retained for visualization, it should not be used as the data fed to the particle filter. (See `pomp-smoothed-data-measurement-mismatch` skill.)

### 4. No Profile Likelihoods or Confidence Intervals

None of the three models report profile likelihoods or confidence intervals for any parameter. For a model with 7–9 free parameters applied to COVID-19 data, parameter identifiability is a genuine concern — collinearity between Beta, rho, and eta is well-known in SEIR-type models. Without profile likelihoods, it is impossible to determine whether the reported MLE values are identifiable from the data or whether the likelihood surface is flat along important directions. The pairs plots provided hint at non-identifiability (some parameters show no clear ridge), but are insufficient for a quantitative conclusion. Profile likelihoods computed via `profile_design()` with multiple restarts and replicated pfilter evaluations are needed. (Wheeler et al. 2024, §Parameter identifiability and uncertainty.)

### 5. No Model Diagnostics

The analysis lacks any model diagnostics beyond visual overlay of forward simulations on data. No conditional log-likelihood plots are shown to identify time periods of poor fit. No effective sample size (ESS) from the particle filter is reported. No filtering distribution is shown or compared to unconditioned forward simulations. For a segmented model applied across three distinct pandemic waves, it would be important to verify that the model explains the timing and magnitude of each peak, not just the general shape. The authors acknowledge that the Delta and Omicron simulations do not align well with the data, but provide no diagnostic evidence to understand why. (Wheeler et al. 2024, §Model diagnostics.)

### 6. ARMA Benchmark Not Quantitatively Comparable to POMP Log-Likelihoods

The authors fit an ARMA(4,4) to the full case series and report its log-likelihood (implicitly, via the AIC table). The three POMP models are each fit to sub-series. No comparison is made between the ARMA log-likelihood and the POMP log-likelihoods, and no such comparison is possible because: (a) the ARMA likelihood is evaluated under a Gaussian model on the full series while the POMP likelihoods are evaluated under a truncated-normal model on sub-series; (b) the observation models differ; (c) the data lengths differ. The paper uses the ARMA only for initial EDA to confirm that residuals are not IID, then abandons it. This is backwards from best practice: the ARMA should serve as a quantitative benchmark against which the mechanistic models' fit is assessed. The authors should compute a common metric (e.g., per-observation log-likelihood or RMSE on held-out data) under a consistent observation model for both model classes. (Wheeler et al. 2024, §Benchmark comparison.)

### 7. Tau Parameter Declared but Never Used in Any Model

All three pomp objects declare `tau` in `paramnames` and apply a log transformation to it in `partrans`, but `tau` does not appear in any of the three rprocess Csnippets (`seir_step`, `seirv_step`, `seirv2_step`) or in either measurement Csnippet (`dmeas`, `rmeas`). It is therefore a ghost parameter: estimated, transformed, and included in the global search box (tau ranges from 0.85–1.1 for model 1, 0–2 for model 2, 0–2 for model 3), but having no effect on the model. IF2 perturbs tau at every iteration via `rw.sd`, which wastes computational degrees of freedom and may affect convergence of the other parameters via the shared cooling schedule. The global search box for tau in model 3 (0 to 2) is also problematic because tau = 0 is on the boundary of the log transform's domain, potentially producing -Inf on the transformed scale during initialization. The fix is to either remove tau from the model entirely or define the component of the model it was intended to govern.

### 8. Accumulator H Tracks Recoveries (dN_IR), Not New Detected Cases

In all three models, the accumulator variable `H` is defined by `H += dN_IR`, where `dN_IR` is the number of individuals transitioning from I (infectious) to R (recovered). The measurement model then sets `mean_cases = rho * H`. However, the observed data (`avg_7`) records new daily confirmed cases — which epidemiologically correspond to new infections becoming symptomatic or detected (approximately `dN_EI` or `dN_SI` in a model with an exposed class), not to recoveries. Accumulating recoveries instead of new infections means the measurement model is comparing the observed "new cases" to the model's "new recoveries" — quantities that may differ systematically in scale, timing, and shape, particularly during the rising phase of an epidemic. The reporting-rate parameter `rho` will absorb the ratio of recoveries to infections, making it biologically uninterpretable. The correct implementation is `H += dN_EI` (transitions from exposed to infectious, as a proxy for becoming detectable) or `H += dN_IR` only if "reported cases" in the data means "cleared cases." For US daily reported COVID case counts, the former interpretation is standard. (See `pomp-accumvar-semantic-audit` skill.)

---

## Minor Issues

- **Local search rw.sd values are very small for the pre-Delta model.** The local search for model 1 uses `rw.sd(Beta=0.002, rho=0.002, eta=ivp(0.002))`, which perturbs Beta (starting value 12.9) by only 0.002/12.9 ≈ 0.015% per step on the natural scale (though partrans applies a log transform, so the perturbation is on the log scale). Given that 20 replicates with 50 iterations each are run, the effective exploration may be very limited. Convergence traces should be consulted to verify whether the local search actually moved parameters appreciably.

- **The global search for the pre-Delta model uses only 10 replicates, insufficient for global coverage.** Models 2 and 3 use 20 replicates, which is marginally adequate, but model 1 uses only 10. With 7 free parameters ranging over a 7-dimensional box, 10 replicates provides very sparse coverage of the parameter space. The authors should use at least 20–40 replicates and verify via pairs plots that the highest-likelihood solutions cluster.

- **Convergence traces for the local search are not described in the text.** The traces are plotted but not interpreted. The authors note that "the loglik plots look so sparse that it does not give us a clear picture" but do not diagnose what this means for convergence. Traces that show no visible decrease in parameter variance across iterations are evidence of non-convergence.

- **The pairs plot filter threshold `loglik.se < 8` for model 1 is unusually permissive.** A standard-error threshold of 8 log-likelihood units allows entries whose likelihood is very poorly estimated. Models 2 and 3 use thresholds of 5 and 0.5 respectively, suggesting the model 1 threshold was set to retain results that would otherwise be discarded. This should be explained or the threshold reduced.

- **The vaccinated compartment dynamics in the SEIRV model are dimensionally inconsistent.** The vaccination rate equation `dN_SV = rbinom(S, 1 - exp(-alpha/N * dt))` divides alpha by N before scaling by dt. With N = 3e8 and alpha = 0.05, the per-step probability is approximately 1 - exp(-0.05 / 3e8) ≈ 1.67e-10, implying essentially zero vaccinations per time step. Biologically, alpha should represent the per-capita vaccination rate (not scaled by 1/N). The equation should be `dN_SV = rbinom(S, 1 - exp(-alpha * dt))` for alpha interpreted as a daily vaccination probability. As written, the vaccination compartment is effectively frozen regardless of alpha's estimated value.

- **The Omicron model initialization computes R as a residual that may be negative.** The rinit for the Omicron model computes `R = round(N*(1-eta) - (97550 + 2*80513 + round(N*(0.5945-0.5935)) + 87248))`. Given the extremely small V initialization (~300,000) and large N*(1-eta) (at eta = 0.1, this is 270 million), and the relatively small E, I, H values, R will absorb ~270 million individuals. This is effectively the correct compartmental accounting only if one accepts that ~90% of the US population had already recovered by December 2021, which is an extreme assumption and should be justified.

- **No quantitative goodness-of-fit summary is presented for any of the three POMP models.** The reported log-likelihoods are mentioned in passing (-14148 for model 1, -2707 for model 2) but are never interpreted relative to any null or benchmark model, nor is the number of observations used to compute them stated, making per-observation comparison impossible. (Wheeler et al. 2024, §Quantitative goodness-of-fit reporting.)

- **The ARMA model is fit to the full time series including all three variant epochs without accounting for structural breaks.** Fitting a single ARMA(4,4) to a series exhibiting three qualitatively different dynamic regimes (pre-Delta, Delta, Omicron) violates the stationarity assumption of ARMA models and produces residuals that are clearly not IID (as the authors themselves note). The AIC table should be computed on a stationary segment or after appropriate differencing/transformation.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-moment-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-dmeas-rmeas-scale-inconsistency/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-semantic-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-accumvar-double-reset/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-global-search-init-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-profile-single-restart-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-rw-sd-magnitude-error/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-smoothed-data-measurement-mismatch/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-stochastic-dmeas-intermediate/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/pomp-arima-double-invalid-comparison/SKILL.md`
- `/Users/jin/Desktop/ai/week11/Skills/sarima-baseline-audit/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project21/blinded.Rmd`
