# Final AI Review
## Project: final_project_w21 / project11
## Title: Modeling COVID-19 Cases in Michigan: ARMA model v.s. SEIR POMP model

---

## Overall Assessment

This paper applies an ARMA model and a stochastic SEIR POMP model to the Michigan COVID-19 winter wave (October 2020 – February 2021), with the stated goal of comparing the two approaches. The authors demonstrate appropriate methodological awareness: they conduct EDA with formal stationarity tests, apply IF2 from multiple starting points, and display filter diagnostics including effective sample size and conditional log-likelihoods. However, the paper has a critical code error in the SEIR measurement model initialisation that likely degrades filter performance, and it fails to deliver the central stated contribution — a quantitative comparison between the ARMA and SEIR models. The inference is further undermined by fixing a key parameter (rho) without estimation, using a single unreplicated particle filter evaluation as the reported log-likelihood optimum, and omitting all parameter uncertainty quantification. The honest discussion of limitations in the conclusion is appreciated, but the concerns below are material enough that the SEIR results as presented cannot support the paper's conclusions.

---

## Key Strengths

- **Multiple IF2 runs with convergence diagnostics.** The local and global searches use approximately 20 and 100 runs respectively, each initialized from different starting values (S1). Convergence trace plots for all free parameters are displayed for both searches, which is the correct diagnostic practice.

- **Filter diagnostics displayed.** Effective sample size and conditional log-likelihood panels are shown for particle filter runs (S2), enabling the reader (and the authors) to observe where the filter struggles.

- **Transparent acknowledgment of limitations.** The conclusion correctly identifies the measurement model, missing covariates, and policy-change dynamics as sources of poor fit, and proposes concrete future directions (S3).

- **EDA with formal stationarity tests.** ADF and KPSS tests are applied before the ARMA analysis, providing a principled basis for the detrending decision (S4).

---

## Major Points

**21.11.1 — H initialisation error corrupts the measurement model**
- **Concern:** In `seir_init`, the accumulator `H` is initialised to `nearbyint((1-eta)*N)` — approximately 1.6 million. Because `accumvars="H"` causes pomp to reset H to zero at each observation time, the intended per-period accumulation is correct for all subsequent steps. However, H is not reset at t0, meaning the first likelihood evaluation computes `dbinom(reports, ~1,600,000, 0.1)` where `reports` is a few thousand. This gives essentially zero probability for the first observation regardless of parameter values, contributing to the observed filter failures (fig_006, fig_008 show ESS collapsing to near 1 and conditional log-likelihoods of −5,000 to −15,000 per step). While model misspecification likely also contributes to poor filter performance throughout the series, this initialisation error is a confirmed bug.
- **Why it matters:** The log-likelihoods reported from both local and global searches are evaluated under a corrupted model. No conclusions about model fit or parameter values can be reliably drawn until this is fixed.
- **Severity:** Major
- **Suggested action:** Set `H = 0` in `seir_init`. Then re-run local and global searches from scratch before drawing any conclusions about convergence or parameter estimates.

**21.11.2 — Log-likelihood optimum based on single unreplicated pfilter evaluation**
- **Concern:** The reported optimum (`loglik = -85119`) appears to derive from a single particle filter evaluation per IF2 chain rather than from averaged replicates. Monte Carlo variability in a single pfilter run with Np=1000 produces standard errors on the order of tens to hundreds of log-likelihood units — the reported `loglik.se = 136` confirms this magnitude. Reporting the maximum over chains of a single-run likelihood is not a reliable estimate of the true likelihood at any parameter point.
- **Why it matters:** The reported "best" parameter point cannot be trusted as a maximum likelihood estimate; it could differ from the true MLE by hundreds of log-likelihood units due to Monte Carlo noise.
- **Severity:** Major
- **Suggested action:** After each IF2 run, evaluate `pfilter` with `Np = 1000` at least 10 times independently, then use `logmeanexp` of the replicate log-likelihoods to obtain a Monte Carlo-corrected estimate. Select the parameter point with the highest corrected loglik.

**21.11.4 — No quantitative benchmark comparison between ARMA and SEIR**
- **Concern:** The paper's stated goal is to compare ARMA and SEIR models, and the conclusion claims "Prediction from ARMA indicates the necessity of the POMP model" — but no quantitative comparison is presented. The ARMA(2,2) AIC is in the AIC table, implying a log-likelihood of approximately −997 on the HP-filtered data. The SEIR log-likelihood is reported on 7-day smoothed data. No common metric on identical data is provided, and no overlay of fitted trajectories from both models is shown.
- **Why it matters:** Without a quantitative comparison, the paper does not deliver its central stated contribution. Given that the SEIR filter is failing badly, the ARMA model likely outperforms the SEIR on this data.
- **Severity:** Major
- **Suggested action:** After correcting the H bug and implementing replicated pfilter evaluation, compute log-likelihoods for both models on the same data (the original smoothed cases, not the HP-filtered version). Report these side-by-side with a note on scale comparability. Overlay fitted values from both models on the observed data.

**21.11.5 — rho fixed at 0.1 without estimation or profile likelihood**
- **Concern:** The reporting rate rho is fixed at 0.1 based on a literature value and the observation that it "tends to fit the data fairly well" — not through likelihood maximisation. rho is among the most influential parameters in an SEIR model: it determines the latent epidemic scale and its value propagates into estimates of Beta, mu_EI, mu_IR, and eta.
- **Why it matters:** All other parameter estimates are conditional on rho = 0.1. Without a profile likelihood for rho, neither the appropriateness of this value nor the sensitivity of other estimates to it can be assessed.
- **Severity:** Major
- **Suggested action:** Either estimate rho jointly with the other free parameters, or compute a profile likelihood for rho over a plausible range (e.g., 0.05 to 0.30) holding other parameters at their profile MLEs.

**21.11.6 — No profile likelihoods or confidence intervals for any free SEIR parameter**
- **Concern:** The paper estimates four free parameters (Beta, mu_EI, mu_IR, eta) but provides no profile likelihoods, confidence intervals, or standard errors for any of them. Qualitative descriptions of trace plot behavior ("beta varies 0.3 to 0.7," "mu_EI converged around 0") are offered instead.
- **Why it matters:** Without uncertainty quantification, the biological interpretations offered (e.g., 1/mu_IR as infectious period, eta as susceptible fraction) cannot be assessed for plausibility or precision. The suspicious near-zero convergence of mu_EI — which would imply an infinite latency period — is flagged by the authors but left unresolved.
- **Severity:** Major
- **Suggested action:** After fixing the code and obtaining reliable likelihood estimates, compute profile likelihoods for at least mu_EI and eta. If mu_EI genuinely profiles near zero, this is strong evidence of model misspecification and should be discussed as such.

---

## Minor Points

**21.11.CON — Population conservation violated at initialisation**
- **Concern:** With S = N*eta ≈ 8.4M, E = 90,000, I = 66,000, and R = N*(1-eta) ≈ 1.6M, the initial compartment sum equals N + 156,000 > N. This violates the closed-population assumption.
- **Severity:** Minor
- **Suggested action:** Set E(0) and I(0) so that S+E+I+R = N exactly. For example, reduce S(0) by E(0)+I(0): `S = nearbyint(eta*N) - E_init - I_init`.

**21.11.7 — eta not included in logit parameter transformation**
- **Concern:** The `partrans` call applies logit transforms to Beta, mu_EI, and mu_IR, but not to eta, which is also bounded in (0,1) and estimated in the IF2 procedure.
- **Severity:** Minor
- **Suggested action:** Add `eta` to the logit-transformed parameters or apply a logit transform separately.

**21.11.8 — HP filter lambda = 100 inappropriate for daily data**
- **Concern:** Lambda = 100 is the standard recommendation for quarterly macroeconomic data; the Ravn-Uhlig rule implies lambda ≈ 6.25 × 10^6 for daily data. Using lambda = 100 likely under-smooths the trend, leaving substantial trend variation in the "detrended" series.
- **Severity:** Minor
- **Suggested action:** Justify the lambda choice quantitatively, or use the daily-appropriate value and compare the resulting detrended series.

**21.11.9 — Weekly periodicity in ARMA residuals not addressed**
- **Concern:** The ACF of ARMA(2,2) residuals (fig_003) shows a prominent spike at lag 7. Daily reported COVID-19 cases are known to have strong weekly reporting cycles (fewer tests processed and reported on weekends). A seasonal ARMA(p,q) × (P,Q)_7 or SARIMA model would be the natural extension.
- **Severity:** Minor
- **Suggested action:** Fit a SARMA model with period 7 and compare AIC to the non-seasonal ARMA(2,2). Alternatively, pre-process the data with a 7-day moving average before ARMA modeling (which the SEIR analysis already does).

**21.11.3 — Confusing presentation: ARMA(1,1) output shown in ARMA(2,2) section**
- **Concern:** The code block in Section 3 prints output for `arima(x = cases_hp, order = c(1, 0, 1))` immediately after the text selects ARMA(2,2). This is confusing and may lead readers to doubt which model was actually fitted.
- **Severity:** Minor
- **Suggested action:** Remove the ARMA(1,1) output or clearly label it as a comparison step; show the ARMA(2,2) coefficient table explicitly.

**Presentation — reference list non-functional**
- All references list only "here" as the URL text with no bibliographic metadata visible in the rendered document. This makes the reference list non-verifiable.
- **Suggested action:** Replace hyperlink anchors with full bibliographic citations (authors, title, journal, year, URL).
