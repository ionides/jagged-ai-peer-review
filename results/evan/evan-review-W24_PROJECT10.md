# Final AI Review: w24 Project 10
# POMP Analysis on Covid-19 Cases in Malaysia and Influenza in the U.S.

---

## Overall Assessment

This project takes on an ambitious dual-dataset design, applying a SEIRV compartmental model to COVID-19 data from Malaysia and influenza data from the U.S. The authors show analytical honesty in acknowledging and explaining the model's failure on the COVID-19 data, and they demonstrate familiarity with the IF2 workflow including correct use of `logmeanexp` for aggregating replicated particle filter evaluations. However, the flu analysis — which constitutes the main positive result — is undermined by a critical code error in the process model, a methodologically invalid profile likelihood, and the absence of any benchmark comparison. The primary inferential claim of the paper, a 90% confidence interval for the vaccination rate mu_SV, is derived from a flawed procedure and cannot be trusted. These issues require substantial revision before the results can be interpreted.

---

## Key Strengths

**24.10.S1 — Correct Monte Carlo likelihood aggregation**
The code consistently uses `logmeanexp` over 10 replicated `pfilter` evaluations in local search, global search, and profile runs. This correctly accounts for Monte Carlo variability in particle filter log-likelihood estimates and is applied properly throughout.

**24.10.S2 — Honest acknowledgment of model failure**
The COVID-19 analysis openly reports non-convergence (fig_006) and provides a substantive qualitative explanation referencing multi-peak dynamics, rapid viral mutation, and non-uniform vaccination rollout. This level of analytical transparency is commendable and demonstrates genuine understanding of the model's limitations.

**24.10.S3 — Reasonable computational effort for flu analysis**
The global search uses 100 starting points with Np=5000 and Nmif=100+50, and the local search uses 20 chains with Np=5000 and Nmif=100. This represents reasonable effort at the course level.

---

## Major Points

**24.10.1 — Code bug: dN_RS drawn from wrong compartment**
Severity: Major

In `seirv_step`, the waning-immunity transition is `rbinom(I, 1-exp(-mu_RS*dt))`, drawing from the Infectious compartment I rather than the Recovered compartment R. This breaks conservation of individuals: individuals leave R at a rate governed by the size of I rather than the size of R, which is not the intended SEIRV structure. This bug applies to both the COVID-19 and flu analyses.

Why it matters: The waning-immunity pathway is biologically central to the model's motivation, and R-to-S transitions computed from I rather than R produce incorrect dynamics.

Suggested action: Replace `rbinom(I, 1-exp(-mu_RS*dt))` with `rbinom(R, 1-exp(-mu_RS*dt))` in the Csnippet, verify conservation of N = S+E+I+R+V at all time steps, and rerun all analyses.

**24.10.2 — Profile likelihood for mu_SV is not a valid profile**
Severity: Major

The profile code groups starting guesses by rounded values of `rho` (not `mu_SV`), does not fix `mu_SV` to a grid, and does not include `mu_SV` in the perturbation schedule. The resulting fig_011 is a scatter of (mu_SV, loglik) pairs from an unstructured set of starting values — it is not a profile likelihood. The 90% confidence interval of approximately [0.08, 0.12] derived from this plot is invalid.

Why it matters: The profile likelihood for mu_SV is the primary inferential result of the paper. Its invalidity means the paper's main quantitative conclusion cannot be supported.

Suggested action: Implement a proper profile over a fixed grid of mu_SV values (e.g., 25–30 points spanning [0, 0.25]), holding mu_SV fixed while optimizing all other parameters at each grid point, then report the maximum loglik at each fixed mu_SV value and derive CI using the chi-squared threshold.

**24.10.3 — Loglik discrepancy between profile and global search is unexplained**
Severity: Major

The global search reports a best loglik of -306.821, but points in the profile scatter (fig_011) reach approximately -275 — roughly 30 log-likelihood units better. A 30-unit improvement would be a substantial finding, but it is neither reported nor discussed.

Why it matters: If the profile run genuinely found a better optimum, the reported MLE and all parameter estimates from the global search are suboptimal. If it is a numerical artifact, it indicates instability in the fitting procedure.

Suggested action: Identify the parameter vector corresponding to the best loglik in the profile results, verify it with replicated pfilter evaluations, and report it as the new MLE if confirmed. Investigate why the global search missed this region.

**24.10.4 — mu_RS is effectively not estimated**
Severity: Major

The waning-immunity rate mu_RS is excluded from `rw.sd` in the local search and profile, and perturbed only minimally (rw.sd=0.002) in the global search. The flu trace plots (fig_008) show mu_RS flat at 0.1 throughout all chains. The fixed value of 0.1/week implies a mean waning time of 10 weeks, but this is never justified against epidemiological evidence.

Why it matters: mu_RS governs whether recovered individuals re-enter the susceptible pool, which is a key structural assumption of the SEIRV model. Fixing it without justification means one of the model's differentiating features is not being exploited.

Suggested action: Include mu_RS in `rw.sd` with an appropriate perturbation magnitude, expand the search range, and report the estimated value with a comparison to immunological literature for flu.

**24.10.5 — No fitted model overlay for flu data**
Severity: Major

After completing the global search and profile, the paper provides no comparison of the fitted SEIRV against the observed flu data. There is no forward simulation, no filtering distribution plot, and no table of predicted vs. observed counts.

Why it matters: Without a fit check, it is impossible to assess whether the model captures the epidemic peak shape, magnitude, and timing. A loglik of -306.821 is difficult to interpret without context.

Suggested action: Run `simulate()` with the best-fit parameter vector and overlay simulated trajectories on observed flu data. Alternatively, compute and plot the filtering distribution using `pfilter()` at the MLE.

**24.10.6 — No benchmark comparison**
Severity: Major

Neither dataset is compared against a non-mechanistic baseline. Without a benchmark, it is unknown whether the SEIRV model provides explanatory value beyond a simple time series model.

Why it matters: The entire rationale for POMP over ARMA rests on the assumption that the mechanistic model captures something the data-driven model does not. This assumption is untested.

Suggested action: Fit an ARMA(p,q) model to the transformed flu data and report the log-likelihood alongside the SEIRV log-likelihood. Likelihoods from different model classes are directly comparable for the same data.

**24.10.7 — H accumulator reset not confirmed**
Severity: Major

The measurement model uses `rho*H` as the mean of the negative-binomial observation, where H accumulates `dN_IR`. If H is not reset to 0 at each observation time via the `accumvars` argument in the `pomp()` call, the measurement model sees a cumulative total rather than an interval count, making all reported log-likelihoods incorrect.

Why it matters: If H is not reset, every reported loglik value is computed on a cumulative scale — a fundamental error affecting the entire inference chain.

Suggested action: Confirm that `accumvars="H"` is passed to the `pomp()` call. Show this in the code excerpt. If absent, add it and rerun all analyses.

---

## Minor Points

**24.10.8 — ACF argument for POMP is logically inverted**
Severity: Minor

The paper argues that the flu ACF "drops quickly after the first lag," suggesting a "more complex model like POMP is needed." A quickly dropping ACF indicates that a simple MA(1) or low-order ARMA model would fit adequately. The motivation for POMP should be stated in terms of mechanistic interpretability and epidemiological structure, not ACF behavior.

**24.10.10 — Parameter estimates not compared to literature**
Severity: Minor

The best-fit mu_IR ≈ 0.30/week implies a mean infectious period of approximately 3.3 days. This is biologically plausible for influenza but the paper does not compare this estimate against epidemiological literature. The estimated mu_SV should also be evaluated against known influenza vaccination campaign rates.

**24.10.11 — V compartment is absorbing — vaccine waning not modeled**
Severity: Minor

The equations show no pathway from V back to S. Given that the paper explicitly motivates the R-to-S loop based on reinfection possibility, the analogous concern about vaccine waning should either be included in the model or explicitly acknowledged as a simplifying assumption.

**24.10.12 — ESS not monitored during filtering**
Severity: Minor

Effective sample size during particle filtering is a standard diagnostic for detecting particle degeneracy. The paper shows trace plots but does not report or plot ESS across time steps during any pfilter run. Including ESS monitoring would strengthen confidence in the particle filter performance.
