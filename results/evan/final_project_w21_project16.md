# Final AI Review
## Project 21.16 — Volatility Analysis on the Shanghai Composite Index

---

## Overall Assessment

This project addresses a well-motivated financial time-series problem — volatility modeling of the Shanghai Composite Index — using a two-model strategy (GARCH benchmark + stochastic volatility POMP model). The data preprocessing and GARCH selection are handled competently, and the authors demonstrate awareness of proper Monte Carlo averaging by using `logmeanexp` with replicated `pfilter` evaluations. However, the project has several serious methodological issues that undermine its conclusions. The central claim — that the POMP model "performs worse" than GARCH — is unsupported as stated, because the two log-likelihoods are not verified to be on the same scale. The profile likelihood analysis is incomplete (a key phi value is missing from the text) and likely technically flawed (phi is not correctly fixed during IF2). Convergence evidence is absent because trace plots were not included in the rendered output. The project demonstrates reasonable familiarity with the pomp workflow but requires significant revision to support its quantitative conclusions.

---

## Key Strengths

**ID 21.16.8 — Correct Monte Carlo averaging**
The authors use `logmeanexp` to aggregate across replicated `pfilter` runs and report standard errors alongside log-likelihood estimates. This is the correct approach for evaluating POMP log-likelihoods and reflects genuine understanding of Monte Carlo variability in particle filter inference.

**ID 21.16.10 — Systematic GARCH model selection**
A 5×5 AIC table across GARCH(p,q) orders is computed, providing a principled basis for selecting GARCH(1,1). This avoids ad hoc model choice and is consistent with best practice.

**ID 21.16.11 — Both local and global mif2 searches**
The authors conduct both a local search (starting from a single point) and a global search (random starts over a parameter box), improving the chance of finding the global maximum. The global search yielded a higher likelihood than the local search, demonstrating the value of this strategy.

**ID 21.16.9 — Profile likelihood for phi attempted**
A profile likelihood computation for the persistence parameter phi is included, with a chi-squared cutoff shown for constructing a confidence interval. This is a meaningful effort at parameter uncertainty quantification.

---

## Major Points

**ID 21.16.1 — Log-likelihood comparison between GARCH and POMP is not validated**
Severity: Major

The paper concludes that the POMP model "have even worse log-likelihood score" (1264 vs. GARCH's 1269.58). This comparison is not valid without verifying that the two likelihoods are computed on the same observation set and using compatible conventions. `fGarch` and `pomp` define their likelihoods differently (e.g., handling of the first observation, inclusion of normalizing constants). The difference of approximately 5.5 log-likelihood units is also within the range that Monte Carlo variability could explain — the reported logLik SE from the POMP runs is not zero. The conclusion that POMP is inferior should be retracted or heavily qualified.

Suggested author action: (1) Verify that both likelihoods are computed over the same T observations. (2) Acknowledge that these are likelihoods from different model classes with potentially different normalizing conventions. (3) Note that the 5.5-unit difference may not be statistically meaningful given the MC SE in the POMP likelihood. A fair statement is that "the POMP model did not demonstrably outperform the GARCH benchmark within the computational budget of this study."

**ID 21.16.3 — Convergence diagnostics absent from rendered output**
Severity: Major

Although the code calls `plot(if1)` and `plot(if.box)`, no IF2 trace plots appear in the rendered report. Without trace plots showing log-likelihood and parameter values versus mif2 iteration, there is no evidence that the optimization converged. The gap between local search maximum (1244) and global search maximum (1264) suggests the local search may not have converged.

Suggested author action: Ensure trace plots are rendered in the output (remove `include=FALSE` or cache suppression where applicable). Include explicit discussion of convergence: have parameter traces stabilized? Does log-likelihood increase monotonically during IF2 as expected?

**ID 21.16.2 — Profile likelihood for phi likely does not correctly fix phi**
Severity: Major

In the profile computation, phi's perturbation is not explicitly set to zero in the `rw.sd` call. Only sigma_nu, mu_h, sigma_eta, G_0, and H_0 are listed in `rw.sd`, while phi is absent — the default behavior in mif2 for an absent parameter in `rw.sd` is to not perturb it, which is what is wanted. However, the `start` argument `c(unlist(guesses[i,]), params_test)` concatenates two named vectors both containing phi, and R's behavior with duplicate names is to use the first occurrence. Additionally, `guesses` contains phi at the profiled value, but `params_test` contains phi at a different value. This initialization inconsistency may cause phi to not start at the intended profiled value in some runs. Furthermore, `nprof=2` starting points per phi value is far too sparse to reliably evaluate the profile.

Suggested author action: Simplify the profile call to initialize only from `unlist(guesses[i,])` (dropping `params_test`). Verify that phi is not perturbed by confirming it is absent from `rw.sd` or explicitly set to 0. Increase `nprof` to at least 5. Fill in the missing phi value in the conclusion text.

**ID 21.16.4 — pfilter in Section 4.1 evaluates simulated data, not real SSE data**
Severity: Minor (escalated from review)

The pfilter run early in Section 4.1 applies to `sim1.filt`, which is constructed from a simulated dataset, not from the real SSE data. Its log-likelihood is not interpretable as a measure of fit to the real data. The text around this chunk ("let's check the function of pfilter for further investigation") suggests the authors know this is a software check, but the placement is confusing.

Suggested author action: Clarify in a sentence that this is a software validation run on simulated data. Alternatively, move this chunk to an appendix and present only the results from `Shanghai.filt` in the main text.

---

## Minor Points

**ID 21.16.6 — ACF conclusion overstated**
The authors claim the ACF of demeaned log-returns implies the data are "all independent." ACF measures linear autocorrelation only. Financial returns routinely exhibit volatility clustering visible in the ACF of squared returns — this is precisely the motivation for GARCH and SV models. Suggested action: Add a check of `acf(demeaned^2)` and note that while linear dependence is absent, nonlinear dependence (volatility clustering) motivates the chosen models.

**ID 21.16.7 — Missing phi value in text**
The sentence "the maximum log-likelihood over phi is achieved when phi = " contains a blank value, a knitting artifact. Suggested action: Extract the maximizing phi from the profile results and insert the value.

**ID 21.16.13 — GARCH equation omits alpha_0 (omega)**
The displayed GARCH equation reports only the alpha_1 and beta_1 coefficients. The fitted model includes an intercept term (omega in fGarch output) that is omitted. Suggested action: Report all three estimated GARCH(1,1) coefficients.

**ID 21.16.5 — No ESS monitoring**
Effective sample size during filtering is not shown. For a leverage model with small sigma_nu, particle diversity may degrade. Suggested action: Plot ESS over time from one representative pfilter run to confirm adequate particle diversity.

**Underdeveloped — sigma_nu box constraint**
The global search box for sigma_nu is (0.0005, 0.08), which excludes zero. This means the model with no leverage effect (sigma_nu = 0) is never explored. If sigma_nu is identifiable, a profile over sigma_nu would show whether the leverage effect is supported by the data.
