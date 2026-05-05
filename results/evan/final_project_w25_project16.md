# Final AI Review: Analyzing Whooping Cough with ARMA and POMP
## Project 16, w25

---

## Overall Assessment

This project tackles a relevant public health question — the 2024 whooping cough resurgence in the East North Central US — using both ARMA/ARCH time-series methods and POMP-based compartmental models (SIR and SEIR). The project is ambitious in scope, incorporating vaccination, birth, and death covariates and attempting to model both a focused outbreak period and a longer 2017–2025 time horizon. The authors are commendably honest about their failures: the SEIRV model collapses susceptibles, the SEIR simulations fail to capture observed dynamics, and missing 2022 data creates genuine difficulties. These honest admissions are a strength, but they also expose underlying methodological gaps that need to be addressed. The central comparative claim — that the ARCH model outperforms the POMP model — rests on a methodologically invalid log-likelihood comparison and should be withdrawn or significantly qualified. Additionally, the SEIR model produces biologically implausible parameter estimates that are never diagnosed, and key inferential tools (profile likelihoods, replicated pfilter validation) are absent.

---

## Key Strengths

**ID: 25.16.8** — Convergence trace plots are provided for both local and global mif2 searches, making the optimization behavior visible. Multiple starting points are used, allowing the reader to assess whether the optimizer is finding a consistent region of the parameter space.

**ID: 25.16.9** — The measurement model uses a negative-binomial distribution with an estimated dispersion parameter k, which is appropriate for over-dispersed count data and more realistic than a Poisson assumption.

**ID: 25.16.10** — The project progresses through increasing model complexity (SIR for 2024 only → SEIR for 2017–2025 → SEIRV with vaccination covariates), providing a structured comparison of model variants. The decision to restrict the SIR to the 2024 outbreak period and then expand is a reasonable scientific strategy.

**ID: 25.16.12** — The missing 2022 data issue is acknowledged clearly, its likely cause (pandemic-era reporting failure) is explained, and it is identified as a genuine limitation affecting the full-period SEIR model. This kind of transparency about data quality is important.

---

## Major Points

**ID: 25.16.1**
**Concern:** The ARCH vs. POMP log-likelihood comparison is not valid as presented.
**Why it matters:** The paper's primary quantitative conclusion — that ARCH (log-likelihood −1203) outperforms the SEIR model (log-likelihood −1442) — depends on this comparison being valid. If it is not, the conclusion is unsupported.
**Severity:** Major
**Suggested author action:** The ARCH model is fitted to the first-differenced series and uses a Gaussian observation model for the differences. The SEIR model is fitted to the original weekly count series using a negative-binomial observation model. These two likelihoods measure the density of different datasets under different observation models; they are not directly comparable. The "constant Jacobian" argument would allow converting between densities of differences and levels for the same model — it does not make likelihoods from two different models applicable to two different data representations comparable. The authors should either: (a) acknowledge that no direct statistical comparison of log-likelihoods is possible here and discuss the models qualitatively; (b) refit the ARCH model to the same level data with a comparable count-based observation model (e.g., negative-binomial INGARCH, which the Discussion already mentions as future work); or (c) frame the comparison as purely illustrative of the different modeling philosophies. The caution already stated in the manuscript ("this advantage should be interpreted with caution") is a step in the right direction but is insufficient given how prominently the comparison features in the conclusions.

**ID: 25.16.4**
**Concern:** No profile likelihoods are computed; identifiability claims are drawn from pair-plot scatter alone.
**Why it matters:** Profile likelihoods are the standard method for assessing parameter identifiability and computing confidence intervals in POMP analyses. Scatter plots from global searches show the joint geometry of the likelihood surface but cannot confirm marginal identifiability.
**Severity:** Major
**Suggested author action:** For the SIR model (which has the best-behaved convergence), compute profile likelihood curves for at least β and ρ. A profile that shows a clear maximum and curvature supports the identifiability claim; a flat profile does not. The MCAP procedure can then provide confidence intervals. The claim "we can identify β, ρ, and η but not mu_IR" (SIR Global Search section) should not be made without this evidence.

**ID: 25.16.3**
**Concern:** The estimated mu_IR values (6.92 from SIR global search, 37.9–64.2 from SEIR searches) are biologically implausible for whooping cough. These estimates imply an infectious period of 2 hours to 1 day, whereas the typical infectious period is 1–3 weeks (mu_IR ≈ 0.07–0.14 per week). This is never diagnosed or discussed.
**Why it matters:** Biologically implausible parameter estimates are a diagnostic signal of model misspecification. If mu_IR cannot be recovered at plausible values, the model's representation of disease dynamics is fundamentally incorrect, and any epidemiological interpretation of other parameters (β, ρ, η) is unreliable.
**Severity:** Major
**Suggested author action:** Flag mu_IR explicitly as implausible and diagnose the likely cause. Common explanations include: (a) compensatory interaction between β and mu_IR (a fast-recovery / high-transmission trade-off that produces similar observed trajectories); (b) the measurement model absorbing the infectious period dynamics; (c) the model being effectively mis-specified (e.g., treating weekly data as if it were finer-grained). Bounding mu_IR at a biologically plausible range during optimization is one practical fix. Alternatively, fixing mu_IR to a literature value and treating it as a known constant would be defensible.

**ID: 25.16.11**
**Concern:** In the SEIR local search (fig_013), the mu_EI trace spikes from approximately 5–10 to over 150 within the first 10 iterations for some chains, then collapses to near-zero by iteration 50. This behavior — large oscillations followed by collapse — is a strong signal that mu_EI is either non-identifiable in this model formulation or that the likelihood surface has severe ridges that prevent stable optimization. This is not discussed in the text.
**Why it matters:** If mu_EI (the rate of progression from exposed to infectious) cannot be stably estimated, the SEIR model's latent state dynamics are untrustworthy. The reported log-likelihood of −1480 from the local search and −1471 from the global search may correspond to parameter configurations where mu_EI takes arbitrary values without substantially changing the likelihood.
**Severity:** Major
**Suggested author action:** Diagnose why mu_EI traces are unstable. One approach is to fix mu_EI to a plausible value (the mean incubation period for pertussis is approximately 7–10 days, giving mu_EI ≈ 0.7–1.0 per week) and verify that the remaining parameters then show stable convergence. If fixing mu_EI substantially changes the best log-likelihood, this suggests a trade-off with other parameters that profile likelihood analysis would reveal.

**ID: 25.16.2**
**Concern:** The SIR local search reports loglik.se = 1.06, which is a large Monte Carlo standard error. The reliability of the reported MLE (loglik = −212) is therefore uncertain. No replicated pfilter evaluation is described for any of the models.
**Why it matters:** mif2 internal log-likelihood estimates are known to be noisy and biased downward; they should not be used as the final reported log-likelihood. Standard practice is to evaluate the MLE by running multiple independent pfilter calls at the estimated parameters and computing logmeanexp of the resulting log-likelihood estimates.
**Severity:** Major
**Suggested author action:** For each reported best-parameter vector, run at least 10 independent pfilter replications (preferably with Np larger than used during mif2) and report logmeanexp ± standard error as the validated log-likelihood. For the SIR model with loglik.se = 1.06, increasing Np until loglik.se < 0.5 is a reasonable target.

---

## Minor Points

**ID: 25.16.7**
**Concern:** The SEIR global search finds base_beta = 8.76 and outbreak_beta = 8.72 — values that are nearly identical. If the optimizer returns essentially the same value for the two regimes, the time-switching beta structure is not being exploited. This suggests the SEIR model may not actually be capturing any systematic change at the designated switch point.
**Severity:** Minor
**Suggested author action:** Check whether the likelihood improves meaningfully when base_beta and outbreak_beta are allowed to differ versus when they are constrained to be equal. If there is no improvement, the time-varying beta formulation adds parameters without benefit.

**ID: 25.16.5**
**Concern:** The AIC table shows an unusually low value at ARMA(2,3) = 2739.09, approximately 14 AIC units below its nearest neighbors. This is suspicious given that the paper ultimately selects ARMA(2,4) as the best model.
**Severity:** Minor
**Suggested author action:** Re-run the ARMA(2,3) optimization to verify that this is a stable minimum and not an artifact of a particular starting point. If ARMA(2,3) genuinely achieves AIC = 2739, it should be selected as the preferred model with discussion of convergence diagnostics; if it does not replicate, note that the table entry may be unreliable.

**ID: 25.16.13**
**Concern:** The paper states that first differencing is applied to "remove trends and center the series." However, the original series shows relatively flat behavior from 2017–2023 with a single 2024 outbreak — this does not straightforwardly meet the criteria for an I(1) process. No unit root test is reported.
**Severity:** Minor
**Suggested author action:** Briefly justify the differencing choice either by running an ADF or KPSS test, or by acknowledging that the differencing choice is motivated by modeling convenience (avoiding heteroskedasticity in levels) rather than strict stationarity requirements.

**ID: Misc-1**
**Concern:** The Np (number of particles) and Nmif (number of mif2 iterations) are visible from output tibbles and figure x-axes (Nmif = 50 is visible in trace plots) but are never stated explicitly in the text.
**Severity:** Minor
**Suggested author action:** Add a brief sentence stating the run_level parameters: Np = [value], Nmif = 50, number of mif2 restarts = [value from trace plot chain count]. This aids reproducibility.

**ID: Misc-2**
**Concern:** Several typographical errors appear in the manuscript: "chacterized," "orignally," "pandemic-ero reporting issues," "Futhermore."
**Severity:** Minor
**Suggested author action:** Proofread before final submission.
