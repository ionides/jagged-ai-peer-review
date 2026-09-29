# Final AI Review — Volatility Analysis on Ethereum (w22 Project 22)

## Overall Assessment

This project demonstrates competent use of the POMP framework for stochastic volatility modeling on Ethereum returns. The authors correctly implement replicated pfilter with logmeanexp for likelihood evaluation, apply both local and global IF2 searches, and compare three POMP model variants quantitatively. The principled simplification of the leverage model — motivated by observing sigma_nu converge to zero — is a genuine scientific contribution that shows engagement with the model structure rather than mechanical application of course code. However, the analysis has several important gaps that prevent the conclusions from being fully supported. Most critically, no profile likelihoods are computed, leaving parameter identifiability and uncertainty entirely uncharacterized. The key comparative claim — that the simplified model is preferred — rests on a log-likelihood difference of approximately one unit, which is within the Monte Carlo standard error of the pfilter estimates at run_level = 2. No non-mechanistic benchmark is included, and convergence is incomplete across all three models. These issues collectively mean that the reported conclusions are suggestive but not statistically substantiated.

## Key Strengths

- **Correct likelihood evaluation protocol.** The project uses replicated pfilter with logmeanexp consistently, avoiding the common error of using the internally reported mif2 likelihood or a single pfilter run. This is foundational to reliable POMP inference.

- **Principled model simplification.** The observation that sigma_nu converges to zero in the original model is used to justify dropping the leverage random walk, yielding a simpler model. This demonstrates scientific reasoning about model structure. Consider making this reasoning more prominent in the introduction and conclusions.

- **Multiple model variants with quantitative comparison.** Three POMP model variants are compared using the same inference protocol, enabling direct log-likelihood comparisons. Consider adding a unified summary comparison table with logLik, logLik SE, number of parameters, and AIC for all models.

## Major Points

**22.22.C1 — No profile likelihoods or confidence intervals for any parameter.**
No profile likelihood is computed for any parameter in any of the three POMP models. The pairs plots from mif2 runs are not a substitute for profile confidence intervals. Without profiles, it is unknown whether phi, sigma_eta, or mu_h are well-identified, and the reported point estimates may lie in a flat or weakly curved region of the likelihood surface. This matters because the paper's model comparisons and parameter interpretations rest on the assumption that the reported MLEs are reliable.
Severity: Major.
Suggested author action: Compute profile likelihoods for at least phi and sigma_eta in the simplified POMP model. Use the MCAP procedure or standard profile approach and report 95% confidence intervals.

**22.22.C2 — No non-mechanistic benchmark comparison.**
The POMP models are compared only against GARCH variants, not against any ARMA or simpler non-mechanistic baseline. GARCH is itself a structured parametric volatility model; the improvement over GARCH does not establish that the stochastic volatility structure adds value beyond simpler time-series methods. Without a naive benchmark, it is unclear whether the mechanistic complexity is warranted.
Severity: Major.
Suggested author action: Fit an ARMA(p,q) on the demeaned returns and report its log-likelihood for comparison. If a midterm project ARMA result is available for this data, it may be cited directly.

**22.22.C3 — Convergence incomplete; key comparative claim within Monte Carlo noise.**
All three models show parameter traces that are "still fluctuating" after 100 IF2 iterations at run_level = 2. More importantly, the log-likelihood difference between the simplified and original POMP models is approximately 1 unit, which is within the logLik SE of roughly 0.3–0.5 units for the better-behaved runs (and much larger, ~1.67, for the force-negative model). The conclusion that the simplified model is "best" is therefore not statistically meaningful at the current computational level.
Severity: Major.
Suggested author action: Run the simplified model at run_level = 3 (Nmif = 200, Np = 2000). If the logLik difference increases and traces stabilize, the conclusion is supported. If not, acknowledge that the models are effectively equivalent at the achieved precision and report this honestly.

## Minor Points

**22.22.C4 — AIC values not numerically reported for POMP models.**
The claim "AIC favors POMP" appears throughout but no AIC values are tabulated for any POMP model.
Severity: Minor.
Suggested author action: Compute AIC = -2 * logLik + 2 * k for each model and add to a comparison table alongside the GARCH AIC table.

**22.22.C5 — logLik SE not discussed relative to model comparison differences.**
The force-negative model has logLik SE of 1.67, and differences between models are 1–2 units. When SE is comparable to the comparison difference, the result is not meaningful without noting this.
Severity: Minor.
Suggested author action: Note in the model comparison sections that comparisons should be interpreted cautiously when logLik SE approaches the magnitude of model differences.

**22.22.C8 — GARCH vs. POMP log-likelihood comparison not explicitly verified.**
The paper compares GARCH and POMP log-likelihoods as if they are directly comparable without stating that both are computed on the same data with the same density convention. In principle this comparison is valid, but the paper should confirm it explicitly.
Severity: Minor.
Suggested author action: Add one sentence confirming that both log-likelihoods are computed on the same demeaned return series and that the normalizing constants are consistent.

**22.22.C7 — Train/test split defined but never used.**
The test set (`eth[1807:2171,]`) is defined in the EDA code but never referenced again in the analysis.
Severity: Minor.
Suggested author action: Remove the test set definition, or use it for out-of-sample evaluation of the best model.

**22.22.New1 — Conditional log-likelihood diagnostic not computed.**
No cond.logLik plot is shown for any model. This diagnostic would reveal whether the model fails at specific time points (e.g., the sharp 2021 price surge that falls in the training period).
Severity: Minor.
Suggested author action: Extract and plot cond.logLik from the final pfilter run for the simplified model to identify any periods of systematic poor fit.

**22.22.New2 — Normal measurement model not discussed in light of observed heavy tails.**
The GARCH residual Q-Q plots (Fig. 4) demonstrate heavy tails relative to the Normal distribution. The POMP observation model also uses a Normal density (dnorm). The paper does not connect these two observations or discuss whether a Student-t measurement model would be more appropriate.
Severity: Minor.
Suggested author action: Note that the heavy-tailed GARCH residuals motivate considering a Student-t observation density in the POMP model, and briefly explain why Normal was retained.

**22.22.C10 — Force-negative model has arbitrary fixed G_0 = -0.05 without justification.**
The G_0 = -0.05 constant is hard-coded without estimation or sensitivity analysis. Since tanh(-0.05) ≈ -0.05 is nearly zero, the actual leverage imposed is very small, and the name "Force Negative" is somewhat misleading.
Severity: Minor.
Suggested author action: Provide a brief sensitivity analysis over a range of G_0 values (e.g., -0.01, -0.1, -0.5), or estimate G_0 with a negativity constraint.
