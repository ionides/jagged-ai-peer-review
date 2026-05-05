# Final AI Review: Flu Cases in Michigan (w25, Project 03)

---

## Overall Assessment

This project demonstrates a solid understanding of the POMP modeling pipeline applied to Michigan influenza data. The authors correctly implement mif2 with replicated pfilter evaluation using logmeanexp, use a negative binomial measurement model, conduct both local and global searches, and explicitly acknowledge the unreliability of mif2's internal log-likelihood — all signs of methodological awareness. The inclusion of a quantitative benchmark comparison (ARIMA versus POMP) is a genuine strength. However, the paper has three significant technical problems that undermine its central claims. First, the log-likelihood comparison between ARIMA and POMP models is based on likelihoods of different data transformations and cannot be interpreted as direct evidence of superiority. Second, the profile likelihood analysis uses too few grid points and a single optimization path per point, rendering the reported confidence intervals — including two singleton intervals — unreliable. Third, standard particle filter diagnostics (effective sample size, per-step conditional log-likelihoods) are absent, making it impossible to assess where the model struggles. Addressing these issues would substantially strengthen the paper's conclusions.

---

## Key Strengths

**ID: 25.03.9 | Correct log-likelihood aggregation**
logmeanexp is applied correctly when combining replicated pfilter outputs (Sections 4.2 and 4.3), and the authors explicitly acknowledge that mif2's internal log-likelihood is unreliable. This shows command of a common POMP pitfall. Confidence: High.

**ID: 25.03.10 | Appropriate measurement model**
The negative binomial measurement model (dnbinom_mu with size parameter k) is well-suited to overdispersed weekly count data. The code matches the mathematical description. Confidence: High.

**ID: 25.03.12 | Quantitative benchmark comparison**
Log-likelihoods for ARMA(0,1), SARMA(0,1)×(1,0)₅₂, and SEIRS POMP are reported in a comparison table (Section 5.1). Providing numerical rather than purely qualitative comparisons is appropriate practice. Confidence: Moderate (subject to the scale issue described below).

**ID: 25.03.13 | Global search with diverse starting points**
The global search samples parameters uniformly across a broad range, substantially reducing the risk of local optima that can trap single-start optimization. Confidence: Moderate.

---

## Major Points

**ID: 25.03.1 | Log-likelihood comparison is across incompatible scales**
Severity: Major
Why it matters: The paper's central quantitative conclusion — that the SEIRS POMP model is substantially better than ARMA/SARMA (log-likelihood improvement from ~-495 to ~-376) — rests on this comparison. However, the ARIMA models are fit to first-differenced raw case counts (`diff_flu_ts`), while the POMP model is fit to the raw weekly counts. These are likelihoods of different random variables, and they cannot be directly compared on a numerical scale. The ~120 unit improvement is therefore uninterpretable as evidence of model fit superiority.
Suggested author action: Either (a) fit an ARIMA model on the same data as POMP (without pre-differencing, using `d=1` within arima() so the likelihood is evaluated on the original scale), compute the Jacobian-adjusted log-likelihood, then compare; or (b) acknowledge explicitly that the comparison is informal and that the log-likelihood improvement partly reflects the different data transformations. A textual disclaimer in Section 5.1 would be a minimum correction.

**ID: 25.03.2 | Profile likelihood is under-powered and CIs are unreliable**
Severity: Major
Why it matters: Section 6 is dedicated to parameter uncertainty quantification, which is a core part of POMP analysis. The procedure uses only 10 grid points per parameter and runs a single mif2 chain per grid point. The resulting singleton confidence intervals for `phase` ([2.7, 2.7]) and `rho` ([0.00015, 0.00015]) are interpreted as evidence that these parameters are unidentifiable. However, 10 points cannot resolve the shape of a likelihood curve, and a single mif2 path per point will not reliably find the conditional maximum. The singletons almost certainly reflect computational limitations rather than intrinsic unidentifiability.
Suggested author action: Run at least 20–30 grid points covering a wider range. For each grid point, run 3–5 independent mif2 chains and take the best. Replace the single pfilter evaluation per point with logmeanexp over 5–10 replicates. The reported CIs for all four parameters should be treated as provisional until this is done.

**ID: 25.03.5 | No particle filter diagnostics**
Severity: Major
Why it matters: There are no effective sample size (ESS) plots and no per-time-step conditional log-likelihood plots in the paper. Without these, it is impossible to detect particle filter degeneracy, to identify which time periods are poorly fit (e.g., the large 2024-2025 outbreak spike), or to assess whether the model's stochastic structure is compatible with the data.
Suggested author action: Plot ESS over time from at least one representative pfilter run at the MLE parameter values. Plot the per-step log-likelihood contributions. These are standard outputs from pomp's pfilter() object and require minimal additional code.

**ID: 25.03.14 | No profile likelihood for transition rate parameters**
Severity: Major
Why it matters: The transition rates mu_EI, mu_IR, and mu_RS determine the incubation period, infectious period, and duration of immunity — the most biologically interpretable parameters in an SEIRS model. The paper profiles only amp, Beta0, phase, and rho (reporting rate), leaving the scientifically central parameters without any uncertainty quantification. Section 6.2 notes computational constraints but does not flag this as a substantive limitation of the conclusions.
Suggested author action: Profile at least mu_EI and mu_IR. These two rates, together with Beta0, determine R0 and the epidemic timescale. Even a coarse profile (10–15 points) would provide more information than none. The estimated values (mu_EI ≈ 0.74/week → incubation ~1.4 weeks; mu_IR ≈ 3.3/week → infectious period ~0.3 weeks) should be compared to published influenza natural history; a 2-day infectious period is at the short end of the biological range.

---

## Minor Points

**ID: 25.03.3 | Initial condition parameters effectively fixed during mif2**
Severity: Minor
Why it matters: S0, E0, I0, R0 appear in the parameter vector and in the barycentric transformation, but no random walk standard deviations are specified for them in the rw_sd object (which lists only Beta0, amp, phase, mu_EI, mu_IR, mu_RS, rho, k). This means the initial compartment proportions are frozen at their starting values throughout mif2 and are not estimated. The paper presents them as estimated parameters without disclosing this.
Suggested author action: Either add rw.sd entries for the initial state parameters and re-run the optimization, or explicitly state that initial conditions were held fixed at the values listed in Section 4.1 and discuss sensitivity.

**ID: 25.03.4 | Log transformation described but not applied to ARMA fitting data**
Severity: Minor
Why it matters: Section 3 describes applying a log transformation to handle skewness and non-stationarity, then produces an ACF of the log-transformed series. However, the differencing and all ARMA/SARMA model fitting is applied to `diff_flu_ts`, which is the first difference of the raw (non-log-transformed) counts. Fitting ARMA to heavily right-skewed undifferenced data or to its raw difference, without log-transforming, can produce poorly-specified residuals.
Suggested author action: Clarify whether ARMA fitting was intentionally applied to differenced raw counts. If so, justify this choice. If the log-transformed differenced series was intended, correct the code accordingly.

**ID: 25.03.7 | Single pfilter per mif2 run used for selecting the best local result**
Severity: Minor
Why it matters: The best local run is selected using a single pfilter evaluation (Np=2000) per mif2 output. The Monte Carlo variance of a single pfilter call is non-trivial, which introduces noise into the selection step.
Suggested author action: Use logmeanexp over 3–5 pfilter replicates when comparing mif2 runs to select the best.

**ID: 25.03.6 | Reporting rate rho not compared to independent estimates**
Severity: Minor
Why it matters: The MLE reporting rate rho ≈ 0.00015 (0.015%) implies that fewer than 1 in 6,000 influenza infections in Michigan are being captured in the dataset. This is extremely low and merits discussion. If rho is genuinely this small, the implied total infection burden would far exceed any published estimates.
Suggested author action: Compare the implied rho to published estimates of case ascertainment for influenza in the US (typically 5–20% of symptomatic cases are reported). Discuss whether the low rho reflects underreporting, model misspecification, or parameter-compensation by other parameters.

**ID: 25.03.15 | Pair plots with 10 points support limited identifiability conclusions**
Severity: Minor
Why it matters: Figures 11 and 14 show pair plots of parameter values versus log-likelihood from the local and global searches, respectively, each based on 10 runs. Ten-point scatter plots are described as revealing "parameter identifiability and sensitivity" (Section 4.3), but with only 10 points the patterns are very noisy.
Suggested author action: Interpret pair plots qualitatively only, and note that the small number of runs limits what can be concluded about identifiability from these figures.
