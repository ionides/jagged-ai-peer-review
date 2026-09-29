# Final AI Review: w24 Project 16
## Modelling of Influenza Cases and Spread in the Netherlands using ARIMA and POMP(SEIR) Models

> Challenge skipped — Grounding signal was Strong.

---

## Overall Assessment

This project tackles a well-motivated scientific question: whether vaccination visibly alters influenza transmission dynamics as captured by a dual-branch SEIR model applied to 2022–2023 Netherlands sentinel surveillance data. The model structure — separating vaccinated and unvaccinated populations into parallel SEIR chains — is creative and appropriate to the question. The computational effort is substantial (400 global-search starting points, 1000 mif2 iterations, Np=10000, 10 replicate pfilter evaluations per starting point, HPC cluster), and particle filter diagnostics (ESS, conditional log-likelihood) are shown. However, the project's central scientific claim — that beta_v < beta_u "proves" vaccines reduce transmission — is not adequately supported by the analysis. The "profile likelihood" plots are actually raw global search scatter plots, not proper profiles, and the parameters of primary interest (Beta_v, Beta_u) are very poorly identified, with near-maximum-likelihood values spread across almost their entire search range. Additionally, the measurement model is never stated in the paper, the initial condition formula for the unvaccinated branch appears erroneous, mif2 convergence traces are absent, and the ARIMA and POMP log-likelihoods are never compared numerically despite both being reported. These gaps together undermine the reliability of the conclusions.

---

## Key Strengths

**ID: 24.16.9 / 24.16.11**
**Strength:** Correct likelihood computation and serious computational investment.
**Why it matters:** The authors correctly apply logmeanexp to replicated pfilter evaluations, a common stumbling block. Running 400 global-search starts with Np=10000 and Nmif=1000 on an HPC cluster demonstrates genuine engagement with the computational demands of POMP inference.
**Confidence:** High.

**ID: 24.16.10**
**Strength:** Particle filter diagnostics plotted.
**Why it matters:** Plotting ESS and conditional log-likelihoods (fig_011) shows the filter is operating and allows assessment of where the model struggles. This is better practice than reporting a single scalar log-likelihood.
**Confidence:** High.

**ID: 24.16.12**
**Strength:** Scientific motivation for dual-branch SEIR model.
**Why it matters:** Separating vaccinated and unvaccinated compartments is a principled design choice that directly targets the research question. The model is more ambitious than a standard single-population SEIR and is conceptually appropriate for the stated goal.
**Confidence:** High.

---

## Major Points

**ID: 24.16.2 / 24.16.3**
**Concern:** Profile likelihood plots are not proper profiles; key parameters are unidentified.
**Why it matters:** Figures 015 and 016 are scatter plots of (Beta_v, loglik) and (Beta_u, loglik) pairs from the 400-point global search — not profiles computed by fixing the focal parameter and optimizing all others. As a result, they provide no usable confidence interval information. Inspection of both figures shows near-MLE points (above the red reference line) scattered across Beta_v ≈ 0–20 and Beta_u ≈ 0–30. Figure 017 (the ratio beta_v/beta_u) similarly shows near-MLE points ranging from approximately 0 to >2.5, meaning the data are consistent with beta_v > beta_u as well as beta_v < beta_u. The central scientific claim cannot be supported without proper profiling and CI computation.
**Severity:** Major.
**Suggested author action:** Compute proper profile likelihoods: fix each focal parameter at a grid of values, re-run mif2 at each grid point to optimize over remaining parameters, and extract the resulting log-likelihood curve. Apply the MCAP or chi-squared cutoff to derive a 95% confidence interval. If Beta_v and Beta_u remain unidentifiable even with proper profiles, the authors should discuss this as a fundamental limitation.

**ID: 24.16.4**
**Concern:** Measurement model not stated in the paper.
**Why it matters:** The likelihood function evaluated by pfilter depends entirely on the measurement model (the observation equation). Parameters rho and k appear in the code (Section 6) without any mathematical definition in the text. The model diagram shows "New cases" as an output compartment but does not connect it to an observation distribution. Without this specification, a reader cannot evaluate what is being fit, cannot reproduce the analysis, and cannot assess whether the observation model is appropriate for weekly sentinel case counts.
**Severity:** Major.
**Suggested author action:** Add an observation model section stating explicitly the distribution placed on the observed counts Y_t — most likely a negative binomial with mean rho*(I_v + I_u) and dispersion parameter k — and include this in the model notation alongside the process model equations.

**ID: 24.16.1**
**Concern:** Initial condition formula for S_u appears erroneous.
**Why it matters:** The text (Section 5) states S_u = vaccinationRate * eta_u * N, which is the same formula as for S_v (with only the eta subscript differing). The unvaccinated branch should initialize with (1 - vaccinationRate), not vaccinationRate, as the base population. If this error is present in the code as well (not just the writeup), then the initial unvaccinated susceptible pool is incorrectly set to 67.9% of the population rather than 32.1%, substantially misspecifying the model.
**Severity:** Major.
**Suggested author action:** Verify the code and correct the formula. If the code is correct, fix the typo in the text. If both text and code are wrong, quantify the impact on parameter estimates.

**ID: 24.16.5**
**Concern:** mif2 convergence trace plots absent.
**Why it matters:** Without trace plots of loglikelihood and key parameters over IF2 iterations, there is no evidence that the algorithm converged. The reported MLE of -193.7 may be a plateau rather than a maximum, which would make all downstream parameter comparisons unreliable.
**Severity:** Major.
**Suggested author action:** Show loglikelihood traces for a representative set of starting points from the global search, demonstrating that likelihood plateaus before the final iteration count.

**ID: 24.16.6**
**Concern:** No quantitative benchmark comparison of ARIMA vs. POMP.
**Why it matters:** The log-likelihood for ARIMA(0,1,4) is -211.2 and for the POMP model is -193.7; these values are on the same data and are directly comparable. The improvement of ~17.5 log-likelihood units for a 9-parameter model (vs. 4 for ARIMA) should be stated explicitly. Without this comparison, the justification for the mechanistic model rests entirely on qualitative grounds ("ARIMA fails to capture complex dynamics").
**Severity:** Major.
**Suggested author action:** Add a one-paragraph comparison noting ARIMA loglik = -211.2 (AIC 432.4) and POMP loglik = -193.7. Note that the POMP model has more parameters; discuss whether the gain is justified.

**ID: 24.16.7**
**Concern:** Causal language used without causal identification.
**Why it matters:** Section 7.1 states: "This proves that vaccinations effectively slows down the transmission rate of the flu in healthy people." This is a causal claim based on an observational analysis. The SEIR model imposes structure (vaccinated and unvaccinated populations are given different betas) and estimates parameters from aggregate case counts; this does not identify a causal effect of vaccination. Furthermore, the underlying identifiability issues (Major Point 24.16.2/3) mean even the descriptive claim is uncertain.
**Severity:** Major.
**Suggested author action:** Replace "proves" with language appropriate to mechanistic modeling: "The fitted model is consistent with a lower transmission rate for vaccinated individuals, though parameter uncertainty is substantial and causal interpretation requires stronger identification assumptions."

---

## Minor Points

**ID: 24.16.13**
**Concern:** Negative spike in conditional log-likelihood (fig_011, ~week 35) not discussed.
**Why it matters:** A severe drop in conditional log-likelihood at the onset of the epidemic peak may indicate that the filter is struggling to track the data at that point, which is a potential model misspecification signal.
**Severity:** Minor.
**Suggested author action:** Comment briefly on the spike — whether it reflects data anomaly, initial condition sensitivity, or genuine model misspecification.

**ID: misc**
**Concern:** Multiple notation and presentation issues.
**Why it matters:** Notation inconsistency (mu_SE_v in diagram vs. Beta_v in code/text), the heading split rendering artifacts, and several typographical errors (Forcast/Forcase, intesive, inmuen) reduce readability and raise questions about careful proofreading.
**Severity:** Minor.
**Suggested author action:** Reconcile the model diagram parameterization with the code parameterization. Proofread the document for typos. Fix rendering artifacts in section headings.

**ID: misc-2**
**Concern:** Pairs plot (fig_013) is very low resolution and nearly illegible.
**Why it matters:** A reader cannot meaningfully assess the parameter space coverage or convergence behavior from the rendered plot.
**Severity:** Minor.
**Suggested author action:** Render fig_013 at higher resolution, or subset the pairs plot to the most important parameters.
