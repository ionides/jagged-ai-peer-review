# Final AI Review — w24 Project 14

---

## Overall Assessment

This project analyzes U.S. tuberculosis incidence data (1953–2020) using both ARIMA and a stochastic SEIRS POMP model with a time-varying transmission rate and gamma white-noise overdispersion. The model design shows genuine engagement with the course material — the negative binomial measurement model, reporting rate, and plug-and-play inference via mif2 are all incorporated. However, the execution has several critical deficiencies: the log-likelihood is reported from the noisy mif2 internal estimate rather than replicated pfilter runs; only a single mif2 run from one starting point was conducted, with trace plots showing parameters still drifting at the final iteration; and the forward simulations from the fitted parameters are roughly two orders of magnitude above the observed data, directly contradicting the authors' conclusion that the model "reasonably captures" the declining trend. There is also no quantitative comparison between the ARIMA and POMP models. In its current state, the work demonstrates familiarity with POMP methodology but does not establish reliable parameter estimates or model adequacy.

---

## Key Strengths

**ID 24.14.11 — Appropriate measurement model**
The measurement model uses a negative binomial distribution with estimated dispersion parameter k and reporting rate rho. This correctly captures overdispersion in annual case counts and is well-matched between the mathematical description and the C implementation. Severity: strength. Confidence: high.

**ID 24.14.12 — Plug-and-play inference with mif2**
The use of mif2 (iterated filtering) as the inference engine is appropriate for a partially observed Markov process model. The structure of the pomp object — with Csnippet process model, accumvars, and parameter transformations including barycentric constraint on initial fractions — reflects careful implementation. Confidence: high.

---

## Major Points

**ID 24.14.1 — mif2 log-likelihood reported without replicated pfilter**
Concern: The paper states "the best parameters we could find with log likelihood of −628.8447" and uses `logLik(mif_out)` directly. The mif2 internal likelihood is a single, negatively biased, Monte Carlo-noisy estimate from the final filtering pass. It should not be treated as the model log-likelihood.
Why it matters: All quantitative conclusions about model adequacy rest on this number. An unreliable likelihood estimate makes it impossible to assess whether the model fits the data.
Severity: Major.
Suggested action: After the mif2 run, call `pfilter` at the final parameter estimates with Np >= 2000, repeat at least 10 times, and report `logmeanexp` of the replicate log-likelihoods along with Monte Carlo standard error.

**ID 24.14.2 — Single mif2 run; convergence not established**
Concern: Only one mif2 chain (Nmif = 50, Np = 2000) is run from a single starting point. The convergence trace plots (Figs. 10–11) show that most parameters (mu_IR, mu_RS, mu_EI, Beta_t, all initial condition fractions) are still trending monotonically at iteration 50. N is erratic throughout. There is no evidence that the optimizer has reached a neighborhood of the likelihood maximum.
Why it matters: Without convergence, the reported parameter values cannot be interpreted as estimates. Any downstream biological interpretation (e.g., implied latent period, infectious period) is unreliable.
Severity: Major.
Suggested action: Run at least 5–10 mif2 chains from diverse starting points. Show overlaid log-likelihood traces; declare convergence only when multiple chains stabilize near the same value. Increase Nmif if needed (100–200 is typical for this scale).

**ID 24.14.3 — Simulations inconsistent with data by two orders of magnitude**
Concern: Figure 8 shows model simulations reaching 600,000 or more cases, whereas observed TB cases (cyan line) remain below ~30,000 throughout the study period. The paper characterizes this as the model "captur[ing] the overall trend" — this is not supported by the figure.
Why it matters: Such a large discrepancy indicates severe model misspecification or incorrect parameter values. The model cannot be used to draw epidemiological conclusions if it cannot reproduce the scale of the observed data.
Severity: Major.
Suggested action: Acknowledge the misfit explicitly. Investigate the role of the fixed population N = 333,000,000 (2023 U.S. population) combined with the initial susceptible fraction S_0 = 0.75: this places approximately 250 million susceptibles in the system, which when multiplied by Beta = 43 generates a force of infection far exceeding what the observed incidence implies. This is the likely source of the scale discrepancy.

**ID 24.14.5 — No quantitative benchmark comparison**
Concern: The ARIMA model is used as a descriptive preliminary step but its log-likelihood is never compared to that of the POMP model. The paper motivates the POMP approach by arguing ARIMA "assumes the data is fully observed," but provides no evidence that POMP achieves better fit.
Why it matters: Without comparison, there is no basis for claiming the mechanistic model adds value over the statistical baseline.
Severity: Major.
Suggested action: Report the ARIMA(0,1,5) log-likelihood and compare to the POMP pfilter-estimated log-likelihood. Note that the two likelihood values are computed on the same observations (annual TB case counts) and are directly comparable as a measure of fit, even if the models have different parameterizations.

**ID 24.14.7 — Fixed population N = 333,000,000 (2023 value) for 1953–2020 data**
Concern: The U.S. population was approximately 160 million in 1953 and roughly 280 million in 2000. Using the 2023 value introduces a systematic error in the transmission parameters throughout the study period. The authors acknowledge this in "Further Investigation" but do not correct it.
Why it matters: The transmission rate Beta is estimated jointly with N; misspecifying N by a factor of up to 2x biases Beta substantially. This also contributes to the simulation scale problem (M3).
Severity: Major.
Suggested action: Use time-varying N derived from U.S. Census data (a covariate in the pomp object), or at minimum replace 333,000,000 with the mean population over 1953–2020 (~220 million).

**ID 24.14.8 — Biologically implausible parameter values unchecked**
Concern: The estimated parameters imply mu_EI = 129 per year (latent period ≈ 2.8 days) and mu_IR = 0.82 per year (infectious period ≈ 446 days). For TB, the latent period is weeks to months and the infectious period is weeks to months. These values are wrong by orders of magnitude and are not flagged or discussed.
Why it matters: Biologically implausible estimates are a strong signal of model misspecification or parameter non-identifiability. Interpreting these as meaningful disease parameters would be incorrect.
Severity: Major.
Suggested action: Compare estimated parameter values to published epidemiological literature on TB. If estimates fall outside plausible biological ranges, use informative priors or fixed values from the literature, and re-examine model structure.

---

## Minor Points

**ID 24.14.4 — Notation collision: mu_IR used for both force of infection and recovery rate**
Concern: In the "Process" section, the force of infection is written as `mu_IR = beta * I * S / N`, but mu_IR is also defined in the parameter list as the recovery rate (I → R). These are different quantities; the force of infection should be labeled lambda or foi.
Why it matters: This creates ambiguity about the model structure and may confuse readers.
Suggested action: Use a consistent label (e.g., lambda or foi) for the force of infection throughout.

**ID 24.14.6 — ARIMA model selection: lowest-AIC model not chosen**
Concern: The AIC table shows ARIMA(3,1,4) at AIC = 1164.32, which is lower than the selected ARIMA(0,1,5) at AIC = 1166.62. The selection criterion is stated as "AIC and smallest root" without documenting how the trade-off was resolved.
Why it matters: Model selection should be transparent; the reader should understand why a higher-AIC model was chosen.
Suggested action: Document the reasoning — if stability (smallest root > some threshold) was the primary criterion overriding AIC, state this explicitly and show the smallest root for the competing model.

**ID 24.14.9 — ESS near-zero around 1975–1985 not discussed**
Concern: Figure 9 shows effective sample size collapsing to near zero during approximately 1975–1990. This period corresponds to a temporary uptick in TB cases in the observed data (the HIV-era resurgence). The filter is losing track of the data during this period, which is consistent with the poor simulation fit in Fig. 8.
Why it matters: ESS collapse indicates the model cannot account for this sub-period of the data, which should be discussed as a limitation.
Suggested action: Note that near-zero ESS during the 1975–1990 period indicates poor model fit during the HIV-associated TB resurgence, and consider whether model modifications (e.g., a covariate for HIV prevalence) might address this.

**ID 24.14.10 — No residual diagnostics shown for selected ARIMA model**
Concern: The code defines a `build_and_diagnose_model` function that produces residual plots, QQ plots, and ACF plots, but the output for the selected ARIMA(0,1,5) model does not include these diagnostics in the manuscript.
Why it matters: Residual adequacy is a standard check for ARIMA models.
Suggested action: Include the residual plot, QQ plot, and ACF of residuals for ARIMA(0,1,5) in the output.

**Reproducibility:** No sessionInfo(), package version pins, or RNG seeds are provided. The code contains three versions of `seir_step` and `seir_rinit` (two in R, one as a Csnippet), only the last of which is used in inference. Removing or clearly marking the earlier versions would improve readability and reproducibility.
