# Peer Review: W22 Project 03 — Subscriber Analysis (Twitch Streamer)

## Summary

This project analyzes monthly subscriber counts for a prominent Twitch streamer (Félix Lengyel, known as xQc) using ARIMA and POMP models. The authors apply a log-differencing transformation, select ARIMA(1,1,2) via AIC grid search, and then construct a three-compartment (Beginning-Viewer-Subscriber, BVS) POMP model fitted with iterated filtering. While the ARIMA portion is competently executed and the authors demonstrate awareness of the POMP framework, the POMP model section is severely underdeveloped: the model is conceptually ill-specified, critical diagnostics are absent, only a single scalar log-likelihood is reported with no uncertainty quantification, and the project lacks a meaningful conclusion. The writeup is also notably incomplete — the POMP section appears to have been submitted as a screen-captured HTML file embedded within a PDF, cutting off the analysis mid-sentence.

---

## Major Issues

### 1. POMP model is conceptually misspecified — measurement model uses `rbinom` inside `dmeas`

In `bvs_dmeas`, the code draws a random sample `Views = rbinom(N-S, 1-exp(-Beta*S/N))` before computing the likelihood density. A dmeasure function must be a deterministic function of the observed data and the latent state — it must compute `p(y | x, theta)`, not draw a new random variable. Drawing from `rbinom` inside the density evaluation violates the conditional independence requirement of POMP models and produces a random, non-deterministic log-likelihood value on each evaluation. This is a fundamental structural error that invalidates all downstream inference: any log-likelihood value reported from `pfilter` or `mif2` using this dmeasure is meaningless. (POMP checklist §12 — Measurement model specification.)

### 2. Single log-likelihood value reported with no Monte Carlo uncertainty

The POMP section reports a single scalar: `## -866.0623`. No replication is performed, no standard error is given, and no information is provided about which run or parameter configuration produced this value. Particle filter log-likelihood estimates are stochastic and noisy; a single evaluation cannot be used for inference or model comparison. The course standard is to replicate `pfilter` across multiple runs and aggregate with `logmeanexp(se=TRUE)`. Without this, the reported value is unreliable and cannot be compared to any other quantity. (Error 1.4 CC-Yes; POMP checklist §6.)

### 3. AIC comparison between ARIMA and POMP treated as directly valid

The conclusion states that "the ARMA model performs better than the POMP model" by implicitly comparing the ARIMA AIC (around -20.76, on log-diff-subscribers) to the POMP log-likelihood (-866.06, on raw subscriber counts). These two quantities are computed on different observation scales with different likelihood normalizations and cannot be directly compared without adjustment. The course explicitly taught that direct AIC comparison between ARIMA and POMP models requires careful attention to whether both models are evaluated on the same data and with the same observation model. (Error 2.2 CC-Yes; 531-conventions.md §Model comparison.)

### 4. No iterated filtering convergence diagnostics

No trace plots of the log-likelihood or parameters across `mif2` iterations are shown. There is no evidence that the optimizer converged, that multiple searches reached consistent terminal likelihoods, or that the reported log-likelihood is near the MLE. The local search (`mifs_local`) runs 20 replicates from a single fixed starting point, and the global search iterates over 40 random guesses — but no diagnostic output from either search is presented. Without convergence evidence, the fitted parameter values and the reported log-likelihood are uninterpretable. (Error 1.8 CC-Yes; POMP checklist §6.)

### 5. Global search uses undefined variable `fixed_params`

In the global search code, the call `mif2(Nmif=25, params=c(guess, fixed_params))` references a variable `fixed_params` that is never defined anywhere in the visible code. The parameter `N` (total users) is included in `paramnames` but does not appear in the `runif_design` bounds and is not perturbed in `rw.sd`, suggesting it was intended to be in `fixed_params`. If this code actually ran, `N` was likely set to an undefined or default value. If `fixed_params` was undefined, the code would have thrown an error and produced no results. The single reported log-likelihood may therefore come from the local search only, which was run from a single fixed point rather than a global search.

### 6. Measurement model is not a proper probability model — likelihood clamped to `[-100, 0]`

The `bvs_dmeas` code applies two hard clamps: `if (lik>0) { lik=0; }` and `if (lik<-100) { lik=-100; }`. The clamping of `lik` at 0 is numerically valid (log-probability cannot exceed 0), but the clamping at -100 is an ad hoc floor that forces severely misspecified particle weights to be treated as only moderately misspecified. This prevents the particle filter from properly downweighting particles that fail to explain the data, corrupting the filtering distribution and producing a biased likelihood estimate. The clamping at -100 is not a principled choice and is not justified in the text. (POMP checklist §12.)

### 7. Process model does not track the "Subscribers" state as a latent variable

The latent state names are `c("Beta", "D")` — Beta (a time-varying transmission rate) and D (departures from subscriber pool). The subscriber count `S` is instead supplied as a lagged covariate from the observed data rather than as a latent state. This means the model is not estimating a hidden subscriber dynamics process; it is using observed past subscribers as a covariate to predict current subscribers. The POMP framework's purpose — inferring latent states from partial observations — is thus bypassed. The model reduces to a regression on lagged observations rather than a genuine mechanistic state-space model. (POMP checklist §1 — Likelihood-based inference; §9 — Stochasticity.)

### 8. Model lacks a denominator `N` that is scientifically meaningful — N is fixed at 41,500,000 with no justification

The parameter `N` is set to 41,500,000 in the local search and is not included in the global search perturbations. The text says N is "total number of users" but provides no citation, data source, or justification for this value. At the start of the data (March 2017), the streamer had 189 subscribers; a denominator of 41.5 million is nine orders of magnitude larger than the initial subscriber pool and seven orders larger than the eventual peak (~100,000). The ratio `Beta*S/N` that drives the "viewing rate" is therefore negligibly small throughout the entire dataset, making `Beta` effectively unidentifiable. This is a model design error, not a data issue. (POMP checklist §11 — Corroboration with scientific knowledge.)

### 9. No profile likelihoods or confidence intervals for any POMP parameter

No profile likelihoods are shown for any parameter. The authors report a single MLE vector without uncertainty quantification. Without profiles, it is impossible to assess whether any of the five parameters (Beta_sigma, mu_VS, mu_SB, Beta_0, N) are identifiable from the data. Given the structural problems with the model (issue #7 above, covariate-based S), parameter identifiability is genuinely in doubt. (Error 1.9 CC-Yes, though the profile cannot fix the deeper model issues; POMP checklist §5.)

### 10. Incomplete submission — POMP section appears as screenshot of HTML file with browser chrome visible

Page 8 of the PDF shows a browser screenshot with the URL `file:///C:/Users/Ahmed/OneDrive%20-%20Umich/Documents/School/T...` and a footer reading "1 of 5 4/19/2022, 11:50 PM". The POMP analysis is rendered as a web page screenshot embedded in the PDF, not as typeset output. The final sentence cuts off mid-paragraph ("Given the results of the simulation and the log likelihood, it seems that the ARMA model performs better than / the pomp model...") and the document ends abruptly on the last page. This submission appears to be incomplete — the concluding analysis, interpretation, and any additional results were not included.

---

## Minor Issues

### 11. Log-differencing the series conflates two transformations without diagnostic justification

The data pre-processing applies first-differencing to remove the trend, then takes the logarithm of the differenced series to address heteroskedasticity. However, `log(diff(Subscribers))` is undefined when the difference is zero or negative (some months show subscriber declines, e.g., Feb-22: 83,719 vs Jan-22: 88,296). The plot labeled "log diff Subscribers" shows values between 0 and 0.8, suggesting only positive differences were log-transformed. The authors do not explain how negative differences were handled. A more principled approach would be to log-transform the raw series first and then difference on the log scale, which is the standard approach for multiplicative trend-stationary series. (Error 2.1 CC-Yes — differencing vs. detrending.)

### 12. R-squared (R2 = 0.983) is reported for an ARIMA model without clarification

The coefficient table shows `R2 = 0.983`, which appears to have been produced by a regression-style output function (possibly `sjPlot` or `stargazer`). For an ARIMA model with differencing and log transformation, R-squared is not a standard or well-defined goodness-of-fit measure and can be artificially inflated by the integrated (trend-following) component. The log-likelihood or AIC value should be the primary fit statistic; R2 is misleading here.

### 13. ACF plot for residuals does not display lag-0 spike correctly

The residual ACF plot (page 7) shows a spike at lag 0 of approximately 0.8–1.0 but the plot's y-axis ranges from -0.2 to 1.0, which is unusual. In a standard ACF plot, lag-0 is always 1.0 by definition and is typically not shown (or shown at exactly 1.0). The unusually positioned first bar may indicate the plot is not showing the correct series or the lag argument is misconfigured.

### 14. Title typo and course name typo on cover page

The title reads "Subsciber Analysis" (missing 'r') and the course is listed as "SATST531" rather than "STATS 531". These typographic errors suggest the writeup was not proofread before submission.

### 15. No data source documentation or discussion of what "Subscribers" measures on Twitch

The introduction mentions TwitchTracker.com as the data source but provides no URL, access date, or description of what the subscriber metric represents (Twitch uses both free "followers" and paid "subscribers" — these are very different quantities). The analysis assumes the growth dynamics of paid subscribers can be modeled like a population process, but this assumption is never discussed. The dataset also contains a column `AvgVeiwers` (note: misspelled in both CSV header and R code as `AvgVeiwers`) which is loaded but not used in either the ARIMA or POMP analysis.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/code-supplement-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/references/simulation-study-checklist-pomp.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project03/blinded.pdf`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w22/project03/twitch.csv`
