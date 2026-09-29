# Final AI Review: ARMA and POMP Analysis on COVID-19 Variants in the US
# Project: w22 / Project 21
# Reviewer: Evan (Treatment E)

---

## Overall Assessment

This paper applies a biologically motivated approach to COVID-19 case modeling, segmenting the US daily case time series into three variant-driven periods and fitting progressively more complex compartmental models (SEIR, SEIRV, SEIRV with breakthrough). The conceptual framing is sound and the use of IF2 with logmeanexp-aggregated pfilter evaluation is methodologically appropriate. However, the paper has several serious technical deficiencies that undermine its conclusions: the measurement model is degenerate and internally inconsistent, a declared parameter (tau) plays no role in the likelihood, the Omicron model initializes the vaccinated compartment incorrectly by a factor of ~600, and no profile likelihoods or confidence intervals are reported. These issues collectively make it difficult to trust the reported parameter estimates or assess model adequacy. The paper would benefit substantially from a principled negative binomial measurement model, profile likelihood computation, and convergence verification.

---

## Key Strengths

- **Biologically motivated segmentation:** Dividing the time series into pre-Delta, Delta, and Omicron periods and fitting distinct compartmental models to each segment is principled and allows the model structure to reflect known epidemiological changes.
- **Correct likelihood aggregation:** logmeanexp is used correctly to aggregate replicated pfilter log-likelihoods, satisfying the core computational requirement for POMP inference.
- **Escalating model complexity:** The progression from SEIR to SEIRV (Delta) to SEIRV with breakthrough (Omicron) demonstrates conceptual engagement with the epidemiological context.
- **Transparent acknowledgment of limitations:** The conclusion honestly discusses why Delta and Omicron fits are poor, citing state-level heterogeneity and non-uniform vaccination rates.

---

## Major Points

**ID: 22.21.1 | Severity: Major**
**Concern:** The measurement model is degenerate and internally inconsistent. In `dmeas`, the standard deviation is set to `sqrt(mean_cases * mean_cases) = mean_cases` (coefficient of variation = 1 at all counts), while `rmeas` uses `sqrt(rho*H)` (Poisson-like standard deviation). These are different distributions, meaning the model simulates under one measurement law and evaluates likelihood under another.
**Why it matters:** The measurement model IS the likelihood. An internally inconsistent or degenerate measurement model invalidates all reported log-likelihoods, parameter estimates, and model comparisons. Forward simulations (figures 6, 9, 11, etc.) are generated under a different stochastic law than the one being optimized, making visual fit assessment uninformative.
**Suggested author action:** Replace with a principled negative binomial measurement model: `reports ~ NegBin(mean = rho*H, size = tau)`. Use `tau` (already declared) as the overdispersion parameter. Ensure `dmeas` and `rmeas` implement the same distribution.

---

**ID: 22.21.6 | Severity: Major**
**Concern:** The parameter `tau` is declared in `paramnames`, log-transformed in `partrans`, and included in the parameter vector, but it does not appear anywhere in `dmeas` or `rmeas` in any of the three models. IF2 is "optimizing" a parameter that has no effect on the likelihood.
**Why it matters:** A parameter absent from the likelihood is completely non-identifiable. IF2 will wander randomly in this direction, adding noise to the optimization and potentially harming convergence in correlated directions. The varying tau values across search results (e.g., 0.81–1.40 for Omicron) reflect pure Monte Carlo noise.
**Suggested author action:** Either remove tau from the model or incorporate it as the overdispersion parameter in a negative binomial measurement model (recommended; addresses Issue 22.21.1 simultaneously).

---

**ID: 22.21.9 | Severity: Major**
**Concern:** The Omicron model initializes the vaccinated compartment as `V = round(N*(0.5945-0.5935)) = N*0.001 ≈ 300,000`. This represents the one-day change in vaccination percentage, not the total vaccinated fraction. At 2021-12-01, approximately 59% of Americans (~177 million) were vaccinated, so V should be initialized to approximately 1.77 × 10^8, not 3 × 10^5.
**Why it matters:** This error means the Omicron model begins with nearly the entire population susceptible to breakthrough infection when in reality ~59% had vaccine-derived protection. This fundamentally misspecifies the immune landscape for the Omicron period, making parameter estimates and simulations for this segment unreliable. It also likely causes the compartments to not sum to N (conservation violation).
**Suggested author action:** Set `V = round(N * 0.5945)` to initialize to the full cumulative vaccinated fraction. Verify that S+E+I+R+V = N at initialization.

---

**ID: 22.21.2 | Severity: Major**
**Concern:** No profile likelihoods or confidence intervals are computed for any parameter across all three model segments. Point estimates are reported from global search without any uncertainty quantification.
**Why it matters:** Without confidence intervals, it is impossible to assess whether estimated parameters are identifiable or precise. The pairs plots (figs 8, 10, 15, 20) show broad parameter clouds at near-maximum likelihoods, and the global search for pre-Delta returns results differing by ~2000 log-likelihood units, both indicating serious identifiability problems that go unexamined.
**Suggested author action:** Compute profile likelihoods over at least Beta and rho for each segment. Report MCAP confidence intervals. Even coarse profiles (5–10 points each) would characterize whether parameters are identifiable.

---

**ID: 22.21.3 | Severity: Major**
**Concern:** The ARMA(4,4) (log-lik = -9760.91) is presented as a benchmark but no quantitative comparison to the POMP models is made. The conclusion characterizes fit quality only visually.
**Why it matters:** Demonstrating that mechanistic models improve upon non-mechanistic benchmarks is a core requirement for establishing that the additional modeling complexity is warranted. Without a quantitative comparison, the reader cannot evaluate the mechanistic model's contribution.
**Suggested author action:** Fit ARMA models to each sub-segment and compare log-likelihoods to the corresponding POMP models on the same data window. Note that log-likelihoods from different model classes are directly comparable on the same data.

---

**ID: 22.21.4 | Severity: Major**
**Concern:** The pre-Delta local search trace plot (fig_007) shows log-likelihoods declining steeply at iteration 50, with chains spread over a range of ~2500 log-likelihood units and Beta spanning 12.5–25. The optimization has not converged. The pre-Delta global search best result has loglik.se = 9.7 (barely within the filter threshold of 10), making the reported best loglik = -14148 unreliable.
**Why it matters:** Parameter estimates and log-likelihoods from unconverged searches are not trustworthy. The claim that the global result is "significantly better" than local is not justified given the large Monte Carlo standard error.
**Suggested author action:** Increase Nmif to 200 for pre-Delta local search; increase global starts to 20+; show global search trace plots; use a tighter SE filter (e.g., SE < 2) and increase pfilter replicates to 50 for reliable SE estimation.

---

**ID: M1 | Severity: Major**
**Concern:** Several estimated parameters are biologically implausible and this is not discussed. The Delta global search best result has mu_IR = 0.86, implying a mean infectious period of ~1.2 days (1/mu_IR), far shorter than the known 4–10 day infectious period for COVID-19. The pre-Delta global best has rho = 0.9999 (reporting rate of ~100%), inconsistent with known substantial underreporting.
**Why it matters:** Biologically implausible estimates from a fitted model are an important diagnostic: they suggest either model misspecification or parameter non-identifiability. Neither interpretation supports using these estimates for scientific conclusions.
**Suggested author action:** Compare estimated epidemiological parameters to published literature ranges. If estimates fall outside plausible ranges, investigate whether this indicates model misspecification or identifiability failure.

---

## Minor Points

**ID: 22.21.15 | Severity: Minor**
**Concern:** The pre-Delta local search `rw.sd` only perturbs Beta, rho, and eta. Parameters mu_IR and mu_EI are not perturbed, so they remain fixed at their starting values (1.15 and 0.08 respectively) across all 20 local search chains, as confirmed by the identical values in the top-5 results table.
**Suggested author action:** Add perturbations for mu_IR and mu_EI to the `rw.sd` call, as is done in the Delta and Omicron local searches.

**ID: 22.21.7 | Severity: Minor**
**Concern:** The ARMA model is fitted to raw case counts (up to 1.26M) without log-transformation. The QQ-plot (fig_005) shows heavy tails and the ACF shows significant residual structure including at lag 7 (weekly seasonality).
**Suggested author action:** Consider a log-transformation before ARMA fitting. Acknowledge the weekly seasonal structure explicitly.

**ID: 22.21.10 | Severity: Minor**
**Concern:** No filtering diagnostics (conditional log-likelihood per time step, ESS over time) are shown for any segment. All model assessment is based on forward simulations from fitted parameters, which do not demonstrate that the model tracks the data trajectory conditional on observations.
**Suggested author action:** Add filtering diagnostic plots (e.g., `plot(pfilter(...))`) for at least one segment.

**ID: 22.21.11 | Severity: Minor**
**Concern:** The Delta segment global and local optima differ dramatically (Beta 6.5 vs 11.7, mu_IR 0.86 vs 1.75), and the pairs plot (fig_015) shows diffuse clouds with rho concentrated near 1. This strong non-identifiability is not discussed.
**Suggested author action:** Acknowledge the non-identifiability. Consider fixing parameters with strong external support (e.g., mu_IR) to improve identifiability of remaining parameters.

**ID: 22.21.13 | Severity: Minor**
**Concern:** The ARMA benchmark is fitted to the full 800+ day series while POMP models are fitted to sub-segments, making comparison inconsistent.
**Suggested author action:** Fit separate ARMA models to each sub-segment for a fair comparison to the corresponding POMP models.
