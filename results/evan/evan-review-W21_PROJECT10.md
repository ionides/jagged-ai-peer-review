# Final AI Review — w21 Project 10
# Time Series Analysis of COVID-19 in Georgia

---

## Overall Assessment

This project tackles an interesting and timely problem — modeling the joint dynamics of COVID-19 cases and vaccination rollout in Georgia — and shows genuine ambition in building three progressively refined SEIR+vaccine POMP models. The exploratory analysis is informative, and the code is presented transparently. However, the project falls short of the core requirement of likelihood-based inference for mechanistic models. All POMP parameters are chosen by hand (eyeball fitting against forward simulations), no log-likelihood or AIC is reported for any POMP model, and the one pfilter attempt in the appendix yields -Inf likelihoods that are never resolved. Several of the unresolved -Inf likelihoods stem from identifiable implementation errors in the measurement model. Additionally, Model 3 contains a fundamental compartment error that invalidates its epidemiological interpretation. The ARMA analysis is competently presented but uses an incorrect LRT degrees of freedom and applies to a different outcome variable than the POMP section, so the two halves of the project are never quantitatively integrated. Substantial revision is needed before the POMP results can support any conclusion.

---

## Key Strengths

**ID 21.10.10 — Three vaccine-incorporation strategies**
The project proposes three distinct formulations for incorporating vaccination into a SEIR model — constant removal, constant plus linear ramp, and rate-based removal. Presenting and contrasting these alternatives demonstrates meaningful model development effort. Severity: Strength. Significance: Shows thoughtful epidemiological modeling design.

**ID 21.10.11 — Susceptible population estimation**
The EDA section constructs a running susceptible population estimate accounting for cumulative cases, COVID deaths, and vaccinations. This is a useful and methodologically transparent visualization that grounds the modeling context. Severity: Strength. Significance: Provides essential context for why a vaccine-augmented SEIR model is appropriate.

**ID 21.10.13 — Code transparency and data provenance**
Code for all three POMP models is reproduced in the manuscript and data sources are cited with URLs. This makes the implementation inspectable. Severity: Strength. Significance: Reproducibility is partially supported.

---

## Major Points

**ID 21.10.8 — No likelihood-based inference performed**
Concern: All three POMP models are parameterized entirely by hand without any optimization. Parameters are chosen to visually match the initial case count and epidemic peak. No iterated filtering (mif2) is run successfully, and no pfilter log-likelihood is reported for any model.
Why it matters: Without a reported likelihood, model adequacy cannot be assessed, models cannot be compared to each other or to benchmarks, and parameter uncertainty cannot be quantified. All interpretive claims about model fit rest solely on visual impressions from forward simulations.
Severity: Major.
Suggested author action: Run replicated pfilter at the hand-tuned parameter values and report the Monte Carlo log-likelihood estimate with its standard deviation. This alone would establish a quantitative baseline. Then diagnose why IF2 / pfilter yields -Inf (see points below), fix the implementation errors, and attempt optimization.

**ID 21.10.1 / 21.10.3 — Measurement model specification failures causing -Inf likelihoods**
Concern: The dmeas function uses `dbinom(reports, H, rho, ...)` where H is the accumulator for new recoveries in the current step. When H is small relative to observed `reports`, this returns probability zero (log-likelihood = -Inf). The attempted switch to negative binomial in the appendix uses `dnbinom(reports, H, rho, ...)`, which incorrectly treats H as the size parameter and does not resolve the structural issue.
Why it matters: This is the direct cause of the persistent -Inf likelihoods that blocked all inference attempts. The measurement model is incompatible with the data range. Fixing this is a prerequisite to any likelihood-based inference.
Severity: Major.
Suggested author action: Use a negative binomial measurement model with a separate overdispersion parameter (e.g., `dnbinom_mu(reports, mu=rho*H, size=psi, log=TRUE)`). Ensure H is scaled consistently with daily reported cases.

**ID 21.10.2 — Model 3: vaccination draws from infectious compartment (I), not susceptible (S)**
Concern: In Model 3, `dN_SV` is defined as `rbinom(I, 1-exp(-mu_SV*dt))` in both the mathematical equations and the code. But `dN_SV` represents vaccination, which removes individuals from `S`. Vaccinating the `I` compartment has no epidemiological basis and invalidates Model 3's interpretation.
Why it matters: This is a fundamental model specification error. The vaccination rate parameter `mu_SV` estimated from this model has no interpretable meaning. The "more natural curvature" observed in fig_019 is an artifact of a broken model.
Severity: Major.
Suggested author action: Replace `rbinom(I, ...)` with `rbinom(S, ...)` for `dN_SV` in both the equations and the Csnippet. Update the parameter transformation block if needed. Rerun simulations after the fix.

**ID 21.10.9 — No benchmark comparison**
Concern: The ARMA analysis focuses on vaccination counts while the POMP section models COVID case counts. No single quantitative comparison is made between any ARMA model and any POMP model on the same outcome variable.
Why it matters: Without a benchmark, it is impossible to determine whether the mechanistic SEIR model explains the case data better than a simpler statistical alternative. This is a core requirement for evaluating the value of a mechanistic model.
Severity: Major.
Suggested author action: Fit an ARIMA model directly to the COVID case time series, extract its log-likelihood, and compare it to the pfilter log-likelihood from the best POMP model (on the same data, same time period). Note that direct comparison requires both likelihoods to be evaluated on the same observation sequence.

**ID — Forward simulations are not goodness-of-fit evidence**
Concern: All model evaluation is based on visual comparison of forward simulations (fig_017, fig_018, fig_019) to observed data. Forward simulations are generated from the prior/hand-tuned parameters without conditioning on any observations — they are not posterior predictive distributions or filtering distributions. A model can produce simulations that visually resemble data even when the likelihood is extremely poor.
Why it matters: This misrepresentation of forward simulations as evidence of model fit is the root of all overconfident language ("perfectly simulated," "more natural"). The conceptual distinction between a forward simulation and a filtered trajectory conditioned on data is critical.
Severity: Major.
Suggested author action: Use the filtering distribution (from pfilter) to compare model predictions against observations. A plot of the filtering distribution (conditional mean ± uncertainty) against observed data is the appropriate diagnostic. Forward simulations are useful for exploring model behavior, not for demonstrating fit.

---

## Minor Points

**ID 21.10.5 — LRT degrees of freedom misstated**
Concern: The likelihood ratio test comparing ARIMA(1,1,1) to ARIMA(4,1,4) is stated to follow a chi-squared distribution with 2 degrees of freedom, but the parameter count difference is 6 (three additional AR, three additional MA terms). The practical conclusion (p << 0.05) is unaffected under 6 d.f., but the stated test is incorrect.
Severity: Minor.
Suggested author action: State the correct degrees of freedom (6), or use AIC as the selection criterion, which does not require nested-model assumptions.

**ID 21.10.3 — mu_EI and mu_IR unit confusion**
Concern: The text refers to "latent period equals 13 days" but sets mu_EI = 13 as a rate parameter in pomp. If mu_EI is a rate (units: per day), a value of 13 means the expected latent period is 1/13 days ≈ 1.8 hours — biologically implausible. A similar ambiguity appears for mu_IR (text states both 0.09 and 0.9 in different places). The code uses mu_IR = 0.09 in simulate(), which appears correct (1/11 days), but the text is inconsistent.
Severity: Minor.
Suggested author action: Clarify throughout whether each parameter is a rate (1/period) or a period. If mu_EI represents a rate with a target latent period of 13 days, the value should be 1/13 ≈ 0.077. Verify that code matches the intended epidemiological interpretation.

**ID — Duplicate text in Introduction and Section 2.1**
Concern: Two full paragraphs describing the data sources appear verbatim in both Section 1 (Introduction) and Section 2.1 (Data description).
Severity: Minor.
Suggested author action: Remove the duplicate from one section.

**ID — Missing figure captions**
Concern: Most figures are embedded without descriptive captions, making it difficult to interpret them without reading surrounding text carefully.
Severity: Minor.
Suggested author action: Add brief captions to all figures indicating what is plotted and what conclusion the reader should draw.

**ID — Set RNG seeds consistently**
Concern: `set.seed(10000)` appears before some simulate() calls but not all code blocks. The appendix pfilter code does not set a seed.
Severity: Minor.
Suggested author action: Set RNG seeds before all stochastic operations for reproducibility.
