# Final AI Review — project06 (w21)
# "To The Moon or Not - Analysis on GameStop Stock Price"

---

## Overall Assessment

This paper analyzes GameStop (GME) daily log-returns using ARMA, GARCH, and a POMP-based stochastic leverage model (Breto 2014), comparing models by log-likelihood and AIC to argue that the POMP model provides the best fit. The computational setup is commendable — IF2 with run_level=3, Np=2000, Nmif=200, and both local and global searches with 100 restarts — and the correct use of `logmeanexp` for combining particle filter likelihoods reflects good methodological understanding. However, three major gaps limit the conclusions: the best-fit parameter values are never reported, no uncertainty quantification is provided for any POMP parameter, and the scientifically central question — whether stochastic leverage improves over fixed leverage — is never formally tested. These gaps prevent the reader from assessing what the model has learned about GME volatility dynamics.

## Key Strengths

| ID | Strength | Why it matters |
|----|---------|----------------|
| 21.06.7 | Correct application of logmeanexp and replicated pfilter for likelihood evaluation | Fundamental to valid POMP inference; many projects make errors here |
| 21.06.8 | Substantial computation: run_level=3 with 20 local and 100 global IF2 restarts | Reduces risk of local optima; demonstrates good practice |
| 21.06.9 | Both local and global searches conducted with randomized starting values | Standard defense against convergence to local maxima |

## Major Points

**21.06.5 — MLE parameter estimates not reported**

The code writes optimal parameters to `GME_params.csv` but no table or inline listing appears in the paper. Without knowing the values of phi, sigma_eta, mu_h, sigma_nu, G_0, and H_0 at the maximum log-likelihood, the reader cannot assess scientific interpretability (e.g., is estimated phi near 1, suggesting near-unit-root volatility persistence?). The maximum log-likelihood of 240.1 is reported, but it is a number without scientific content unless the underlying parameters are disclosed.

Severity: Major. Suggested action: Add a table of MLE parameters at the global search maximum log-likelihood. Discuss whether estimated phi and sigma_eta are consistent with typical stochastic volatility findings in the financial literature.

**21.06.14 — No profile likelihoods or confidence intervals**

No uncertainty quantification is provided for any POMP parameter. The trace plots show spread in phi and sigma_eta across multiple IF2 runs, which likely reflects weak identifiability for these parameters in the stochastic volatility model — a well-known challenge. Without profile likelihoods, it is impossible to determine whether the estimated parameters are identifiable from this dataset.

Severity: Major. Suggested action: Compute profile likelihoods for at least phi (persistence) and sigma_nu (leverage variability) using the MCAP procedure. Report approximate 95% confidence intervals. If profiles are flat, note that these parameters are weakly identified.

**21.06.4 — Fixed leverage model not compared to stochastic leverage model**

The paper introduces the fixed leverage model (sigma_nu = 0 special case) as motivation for the stochastic leverage extension, but never formally compares the two via log-likelihood. This is the primary scientific question of the POMP section: does time-varying leverage improve fit over constant leverage? A likelihood ratio test or AIC comparison between the two nested models would directly address this.

Severity: Major. Suggested action: Fit the fixed leverage model (constrain sigma_nu = 0 or start from a very small sigma_nu initial value and examine convergence) and report its log-likelihood. Compare to the stochastic leverage log-likelihood via AIC or likelihood ratio.

**21.06.2 — GARCH AIC table shows signs of numerical instability**

The GARCH AIC table shows large non-monotone swings: GARCH(3,2) = -399.47, GARCH(4,2) = -417.42 (17-unit jump adding one parameter), then GARCH(4,3) = -361.84 (55-unit reversal adding another parameter). Additionally, the GARCH(4,2) coefficient b2 ≈ 1.576e-11 is effectively zero, suggesting a degenerate fit. These patterns indicate the optimizer has not converged reliably for the higher-order GARCH models. The selection of GARCH(1,1) as baseline is defensible, but the large model AIC table is unreliable as presented.

Severity: Major. Suggested action: Investigate GARCH fits for higher-order models using multiple starting values or a more robust package (e.g., `rugarch`). Report any optimizer convergence warnings. If numerical issues persist, limit the GARCH comparison to GARCH(1,1) and note the instability.

## Minor Points

- **21.06.1 — AIC cross-class comparison needs qualification.** The AIC values for ARMA, GARCH, and POMP are presented as directly comparable (and technically they are, if all likelihoods evaluate the same marginal density over observed returns). However, the ARMA model captures only the mean process, not volatility structure, so its lower likelihood partly reflects model scope rather than inferior optimization. The conclusions should note this: the POMP advantage over ARMA reflects modeling a richer data feature, not just a better optimizer.

- **21.06.3 — phi and sigma_eta identifiability.** The trace plots show phi and sigma_eta converging slowly relative to other parameters. This is likely weak identifiability rather than optimizer failure (phi near 1 and sigma_eta are notoriously difficult to separate in stochastic leverage models). Rather than framing this as a convergence problem to solve with more iterations, the paper should note that profile likelihoods are needed to assess whether these parameters are identifiable from GME data.

- **21.06.12 — ARMA residual ACF.** The residual ACF shows significant correlations at multiple lags. The authors acknowledge this and attribute it to unmodeled seasonality, but do not attempt any alternative ARMA specification. Since ARMA is used only as a baseline, a brief note that ARMA(1,3) underfit the serial structure — motivating the volatility models — is sufficient, but the claim of "significant correlation at several different lags" should be specific about which lags.

- **21.06.13 — Filtering-on-simulated-data section.** The log-likelihood of 171.85 (SE = 0.065) is from filtering on data simulated with `params_test` (arbitrary initial parameters), not the real GME data. The text does not make this explicit. A reader may misinterpret this as a preliminary real-data result. Clarify: this is a sanity check confirming that the particle filter runs correctly on synthetic data.

- **ESS not monitored.** The effective sample size (ESS) during particle filtering is never reported. With Np=2000 and GME's extreme January 2021 spike, filter degeneracy is a plausible concern. Reporting ESS at each time step (or at least the minimum ESS) would provide confidence that the filter is functioning throughout the sample.

- **Gaussian measurement model.** The GARCH and ARMA residual QQ plots document heavy tails in GME returns. The POMP model uses a Gaussian measurement (dnorm), which may underfit the tails. A brief discussion of whether a Student-t measurement model would be preferable, or an acknowledgment that the Gaussian model is a simplification, would strengthen the paper.

- **Typographical errors.** "log-golatility" should be "log-volatility" (appears in model description and conclusions). "loglikelihood" and "log-likelihood" are used inconsistently.
