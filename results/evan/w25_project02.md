# Final AI Review
## Examining Explanatory Role of Momentum in Baseball
## STATS 531/631 Final Report — Winter 2025

---

## Overall Assessment

This paper addresses a clearly motivated question — whether team-level momentum contributes to game-to-game variation in offensive performance — using a well-structured POMP framework applied to the 2024 Detroit Tigers season. The model design is sensible: an AR(1) latent state for momentum, a log-linear Poisson observation model with an opponent-quality covariate, and a likelihood ratio test comparing the AR(1) model against a static-skill null. The project demonstrates good awareness of POMP diagnostics (ESS monitoring, trace plots, pairwise scatter of global search results) and commendably includes a sensitivity analysis under a negative binomial observation model. However, the core conclusion — that momentum significantly explains offensive performance — is built on a sequence of methodological problems that, taken together, make it unreliable: the primary conclusion uses a known-misspecified measurement model (Poisson, when the paper's own cited literature and the sensitivity analysis both favor the negative binomial), the likelihood ratio test does not account for Monte Carlo variability, the Wilks approximation is applied at a boundary point, and the "profile likelihood" used to assess identifiability is not a genuine profile. Under the better-specified negative binomial model, the evidence for momentum disappears entirely. The paper is honest in reporting these difficulties, but the framing — presenting the Poisson result as the main finding — should be revised.

---

## Key Strengths

**ID: 25.02.S1**
**Strength:** Well-motivated research question with careful model design.
**Why it matters:** The centered opponent-quality covariate Z_n is a thoughtful design choice that separates batting performance from pitcher context in an interpretable way. The choice to compare AR(1) vs. static latent skill via a nested LRT is conceptually correct.
**Confidence:** High

**ID: 25.02.S2**
**Strength:** ESS diagnostics are satisfactory and shown.
**Why it matters:** Figure 3 shows ESS consistently above 1600 throughout the filtering run, indicating the particle filter is operating well under the initial parameter configuration. This is positive evidence that the observation model is not catastrophically misspecified.
**Confidence:** High

**ID: 25.02.S3**
**Strength:** Sensitivity analysis with negative binomial observation model is included.
**Why it matters:** The authors fit all four model variants (AR1 Poisson, static Poisson, AR1 NB, static NB), report likelihoods for each, and honestly acknowledge the reversal. This is genuinely good practice.
**Confidence:** High

**ID: 25.02.S4**
**Strength:** Convergence diagnostics are shown for both local and global searches.
**Why it matters:** Trace plots (Figure 4) and the pairwise global-search scatter (Figure 6) are provided, enabling the reader to assess convergence quality. The identifiability issue is self-identified and flagged transparently.
**Confidence:** High

---

## Major Points

**ID: 25.02.M1**
**Concern:** Primary conclusion drawn from a known-misspecified measurement model.
**Why it matters:** The paper's own cited literature (baseball analytics blogs, footnote 8-9) states that runs-per-game is not well-described by the Poisson distribution. The negative binomial is better supported, and under the negative binomial model the likelihoods for AR1 and static models are essentially identical (~-396.46 for both), meaning there is no evidence for momentum. Presenting the Poisson result as the primary finding and the negative binomial as a secondary sensitivity check reverses the appropriate epistemic priority.
**Severity:** Major
**Suggested author action:** Restructure the conclusion to lead with the negative binomial result as the primary finding, and present the Poisson result as a sensitivity check. The revised conclusion should be that current evidence does not support the role of momentum in team-level batting performance, with the Poisson result noted as a model-dependent artifact. Alternatively, pursue a more appropriate marginal observation model (e.g., the specialized distributions cited in the baseball analytics literature) before drawing strong conclusions.

**ID: 25.02.M2**
**Concern:** Likelihood ratio test does not account for Monte Carlo variability.
**Why it matters:** The LRT computes 2*(l1 - l0) ~ chi^2_2 using point estimates of log-likelihood from particle filtering. These estimates are subject to Monte Carlo noise whose magnitude is unknown because (a) Np and Nmif are never reported, and (b) no replicated pfilter evaluations at the MLE are shown. If the MC standard error on each log-likelihood estimate is even a few units, the test statistic is unreliable. The 40-unit spread in global search log-likelihoods also raises the possibility that -397.81 is not the true MLE.
**Severity:** Major
**Suggested author action:** Report Np, Nmif, and the number of global search starts. Run at least 5-10 independent pfilter evaluations at the reported MLE for both the AR1 and static models and report mean and standard deviation. Confirm that the MC standard error is small relative to the log-likelihood difference (approximately 40 units) before drawing conclusions. If the MLE itself is uncertain, run additional global searches to narrow the range.

**ID: 25.02.M3**
**Concern:** Wilks' approximation is invalid because sigma = 0 is a boundary constraint.
**Why it matters:** The null hypothesis constrains sigma to zero, which is a boundary of the parameter space (sigma is log-transformed, so sigma = 0 corresponds to log(sigma) -> -infinity). Standard Wilks' theory assumes the null is in the interior of the parameter space. At a boundary, the asymptotic reference distribution is a mixture of chi^2 distributions rather than chi^2_2. Even if the overall 40-unit log-likelihood difference is large, the p-value reported using the chi^2_2 approximation is not formally correct.
**Severity:** Major
**Suggested author action:** Acknowledge the boundary issue and use a parametric bootstrap to obtain the correct reference distribution for the test statistic. Alternatively, fix sigma at a small positive value (e.g., 0.001) rather than exactly zero as the null, or cite theoretical results on boundary likelihood ratio tests and justify why chi^2 is an adequate approximation in this setting.

**ID: 25.02.M4**
**Concern:** Poor man's profile is not a proper profile likelihood; no confidence intervals are provided for any parameter.
**Why it matters:** Figure 7 shows the upper envelope of global search results as a function of phi — not a profile likelihood computed by fixing phi and re-optimizing all other parameters. The flat region identified (~[-0.15, 0.05] in phi) could reflect genuine flatness or insufficient optimization at those phi values. Without a proper profile, no confidence interval for phi can be constructed. The claim that "the data is not informative in estimating precise phi values" is asserted but not formally demonstrated.
**Severity:** Major
**Suggested author action:** Compute a proper profile likelihood for phi by fixing phi on a grid of 20-30 values and running mif2 from multiple starting points at each fixed value. Report MCAP confidence intervals. If the 95% CI for phi contains 0, that is further evidence against the momentum hypothesis. This would replace the current "poor man's profile" and substantially strengthen the identifiability analysis.

**ID: 25.02.M5**
**Concern:** Typographical error in the latent transition density (Equation 1).
**Why it matters:** The density as written, f(x_n | x_{n-1}) proportional to exp(-(phi*x_{n-1})^2 / (2*sigma^2)), does not depend on x_n and does not define a proper conditional density. The correct expression is exp(-(x_n - phi*x_{n-1})^2 / (2*sigma^2)). The code is correct; this is a presentation error, but it can mislead readers about the model specification.
**Severity:** Major (presentation)
**Suggested author action:** Correct Equation (1) to include the term (x_n - phi*x_{n-1}) in the numerator of the exponent.

**ID: 25.02.M6**
**Concern:** No comparison against a non-mechanistic benchmark.
**Why it matters:** Without a benchmark (e.g., ARIMA, negative binomial regression with AR errors, or a simple Poisson GLM with no temporal structure), there is no way to know whether the POMP model captures structure beyond what a simple time-series model would find. If an ARMA model achieves comparable or better log-likelihood than the POMP, the mechanistic structure is not contributing meaningfully.
**Severity:** Major
**Suggested author action:** Fit an ARIMA model or Poisson/negative binomial regression with autocorrelated errors to the runs-per-game series. Report its log-likelihood alongside the POMP likelihoods (noting that likelihoods from different model classes on the same data are directly comparable in principle, though the scales should be checked). Even a brief comparison would substantially contextualize the POMP results.

---

## Minor Points

**ID: 25.02.m1**
**Concern:** Computational settings (Np, Nmif, number of random starts) not reported in the main text.
**Why it matters:** Without these values, the computational adequacy of the search cannot be assessed, and the results cannot be reproduced by others.
**Severity:** Minor
**Suggested author action:** Add a table or paragraph reporting Np, Nmif, number of random starts, and run_level settings used for all model-fitting runs.

**ID: 25.02.m2**
**Concern:** Parameter transformation log-transforms mu, implicitly constraining mu > 0 (expected runs > 1 per game).
**Why it matters:** mu is the log-expected runs, which can in principle be negative. The constraint mu > 0 may restrict the optimization unnecessarily, though it is plausible in practice.
**Severity:** Minor
**Suggested author action:** Either document this as a deliberate prior constraint or remove the log-transform on mu (using identity transformation, which allows mu to take any real value).

**ID: 25.02.m3**
**Concern:** Fixed initial condition X_0 = 0 without sensitivity analysis.
**Why it matters:** If the Tigers began the 2024 season with non-neutral momentum (e.g., following a poor or strong spring training), this assumption is violated.
**Severity:** Minor
**Suggested author action:** Report at least a brief sensitivity check: refit the model with X_0 estimated or initialized from a different value and compare log-likelihoods.

**ID: 25.02.m4**
**Concern:** Figure 2 (model simulations vs. observed) is difficult to read because many blue simulated traces obscure the observed series.
**Why it matters:** The purpose of the figure is to assess whether simulations are consistent with data, but visual assessment is impaired when traces overlap.
**Severity:** Minor
**Suggested author action:** Show a small number of representative simulated trajectories (3-5) alongside the observed series, or use simulation envelopes (e.g., pointwise quantile bands).

**ID: 25.02.m5**
**Concern:** The dramatic dip in conditional log-likelihoods near Game 90 (Figure 3, bottom panel) is not discussed.
**Why it matters:** Localized drops in conditional log-likelihood can indicate model misspecification or unusual observations that the model fits poorly.
**Severity:** Minor
**Suggested author action:** Identify which game is near index 90, check whether there was an unusual run total, and briefly comment on whether the model adequately captures that observation.

**ID: 25.02.m6**
**Concern:** phi converges to approximately -1 during the local search (Figure 4), which is not adequately explained scientifically.
**Why it matters:** phi = -1 would produce an alternating (oscillating) AR(1) pattern — good performance followed by poor performance in strict alternation — which is scientifically implausible as a model of team momentum.
**Severity:** Minor
**Suggested author action:** Discuss whether phi values near -1 (or the apparent local optimum) are scientifically meaningful or represent a pathological mode of the model. Consider constraining phi to (-1, 1) if stationarity is desired, or justifying the unconstrained search.

**ID: 25.02.m7**
**Concern:** The covariate Z_n uses season-level pitching statistics that include games played after game n, introducing a small look-ahead bias.
**Why it matters:** Formally, Z_n should use only information available before game n. The authors acknowledge this in the Discussion, but it should also be flagged in the Model section.
**Severity:** Minor
**Suggested author action:** Add a brief note in the Model section (when Z_n is defined) acknowledging this limitation, and reference the Discussion for elaboration.
