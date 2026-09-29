# Final AI Review: Dengue Fever in the U.S. States and Territories (2022–2023)
## STATS 531 W25 — Project 07

---

## Overall Assessment

This project demonstrates solid ambition by fitting two stochastic compartmental models (SIRS and SEIR) to weekly travel-associated dengue case counts and benchmarking both against a SARIMA(2,0,0)×(0,0,1)[53] model. The mechanistic pipeline has many correct elements: MIF2-based parameter estimation, particle filtering for likelihood evaluation, negative binomial measurement noise, and ESS monitoring. The SARIMA benchmark is properly fitted with log-likelihood reported, enabling direct numerical comparison. However, several problems substantially undermine the reliability of the reported conclusions. Most critically, the SIRS global search produces a reporting rate ρ ≈ 4×10^-5 — effectively zero — which is a sign of model degeneracy or severe misspecification that is never acknowledged. The SEIR global search produces a recovery rate of μ_IR = 35.6 per week (implying a ~5-hour infectious period for dengue), which is equally implausible. The two models are also fitted with population sizes that differ by a factor of ~100 (N = 3.25×10^8 for SIRS vs. N = 3.2×10^6 for SEIR), making their log-likelihoods not directly comparable. No profile likelihoods are computed for any parameter, so identifiability is entirely unassessed. A structural "pandemic switch" at week 29 is introduced without biological justification and never tested against a simpler alternative. Taken together, these issues mean the central claim — that both mechanistic models perform comparably to SARIMA — is not adequately supported in its current form.

---

## Key Strengths

**S1 — Quantitative SARIMA benchmark.** A SARIMA(2,0,0)×(0,0,1)[53] model is fitted to the same data and its log-likelihood (−444.63) is reported alongside the POMP model results. This is the correct approach for evaluating mechanistic model performance.

**S2 — Negative binomial measurement model.** Both SIRS and SEIR use a negative binomial observation model with overdispersion parameter k, which is appropriate for weekly count data with excess variance.

**S3 — ESS and conditional log-likelihood diagnostics.** Effective sample size and per-observation conditional log-likelihoods are plotted for the initial SIRS particle filter run, providing appropriate filter health monitoring.

**S4 — Both local and global parameter searches conducted.** The authors carry out MIF2 local searches from plausible starting points and global searches over broad parameter boxes, representing a reasonable effort to find the global maximum.

---

## Major Points

**ID: 25.07.1 | Concern: Degenerate reporting rate in SIRS global search | Severity: Major**

The SIRS global search reports ρ = 4.000000×10^-5. A reporting rate this close to zero means the measurement model exerts almost no constraint on the latent process: the filter can place essentially any trajectory in the latent compartments without incurring a likelihood penalty. The log-likelihood of ~−440 obtained under this parametrization does not reflect a genuine fit to the observed data. The text does not comment on this value.

*Why it matters:* The SIRS log-likelihood (~−440), which the conclusion treats as evidence that the mechanistic model performs comparably to SARIMA, is computed under a degenerate observation model. This conclusion is not supported.

*Suggested author action:* Investigate why ρ collapsed. Check whether the population size N is inconsistent with the data scale (if N is too large relative to the case counts, ρ will be driven to zero to compensate). Constrain ρ to a biologically plausible range (e.g., 0.001–0.5 for travel-associated surveillance), refit, and report the resulting log-likelihood. Profile ρ to assess whether it is identified within that range.

---

**ID: 25.07.2 | Concern: Different N values across models invalidate the log-likelihood comparison | Severity: Major**

The SIRS model uses N = 3.25×10^8 (U.S. population) in the global search. The SEIR model uses N = 3,200,000 (3.2 million). These differ by approximately a factor of 100. Population size enters the force of infection (β×I/N) and the scaling of initial conditions, so models with different N are fitting different dynamical systems to the same data. The conclusion compares log-likelihoods across SIRS, SEIR, and SARIMA as if they are on the same footing, but the SIRS and SEIR models differ in their observation model definition.

*Why it matters:* Model comparison via log-likelihood is only valid when the same data are being modeled under the same observation framework. Comparing SIRS at N = 3.25×10^8 with SEIR at N = 3.2×10^6 does not satisfy this condition.

*Suggested author action:* Choose a single biologically justified N for both models. State the epidemiological rationale (e.g., the U.S. traveling population at risk for dengue, or a sentinel surveillance population). Refit both models with the same N and document the choice explicitly.

---

**ID: 25.07.3 | Concern: SEIR global search produces μ_IR = 35.6, biologically implausible | Severity: Major**

The SEIR global search reports μ_IR = 35.6 per week. This implies a mean infectious period of 1/35.6 ≈ 0.028 weeks ≈ 5 hours. Dengue has an established infectious period of approximately 4–12 days (~0.6–1.7 weeks). This estimate indicates the optimizer converged to a degenerate solution, analogous to the ρ collapse in the SIRS model. The text presents this as a successful global search result without flagging the problem.

*Why it matters:* A degenerate μ_IR indicates the model is not fitting the data through realistic dengue dynamics. The reported log-likelihood (−446.79) under this parametrization reflects compensating parameter combinations, not a biologically interpretable fit.

*Suggested author action:* Constrain μ_IR to a biologically plausible range (e.g., 0.5–5 per week, corresponding to 1.4 days to 2 weeks). Refit the global search and report results. If μ_IR still hits the boundary, this is evidence of structural model misspecification.

---

**ID: 25.07.5 | Concern: Pandemic switch at week 29 is unjustified and untested | Severity: Major**

The SIRS model introduces a transmission switch at week 29: β₀ = a before week 29, β₀ = b after. The motivation given is purely data-driven ("we noticed that the second peak after week 29 is larger"). No external biological or epidemiological justification is provided for week 29 as a structural break. No comparison is made between the switch model and a simpler constant-β₀ model. Additionally, the text says "we set a > b because the second peak is larger" — but the second peak occurs after week 29, when β₀ = b, so this implies b > a, which contradicts a > b.

*Why it matters:* An unjustified structural break can absorb variance from model misspecification, inflating apparent fit without providing scientific insight. The internal contradiction (a > b yet the larger peak occurs in the b-phase) also suggests the model may not be behaving as described.

*Suggested author action:* Either provide external evidence for the break at week 29 (e.g., COVID travel policy changes in mid-2022), or compare the switch model to a no-switch model via AIC. Correct the apparent contradiction regarding which phase has higher transmission.

---

**ID: 25.07.6 | Concern: No profile likelihoods or confidence intervals for any parameter | Severity: Major**

No profile likelihoods are computed for any parameter in either the SIRS or SEIR model. With 7–9 estimated parameters and 106 weekly observations, identifiability is a genuine concern. The near-identical a and b values in the SIRS local search (a = 2.794, b = 2.788) suggest these two transmission-phase parameters may not be distinguishable from each other.

*Why it matters:* Without profile likelihoods, there is no valid basis for reporting parameter estimates as meaningful values, for drawing conclusions about dengue transmission dynamics, or for comparing models on mechanistic grounds. Unidentifiable parameters can appear well-estimated in point estimates while having flat profile likelihoods spanning biologically meaningless ranges.

*Suggested author action:* Compute profile likelihoods for at minimum ρ, β (or a/b), and μ_IR in both models. Report 95% confidence intervals using the MCAP procedure. If profiles are computationally expensive, document this as a limitation.

---

## Minor Points

**ID: 25.07.7 | Concern: SEIR k fixed at 10 throughout both local and global searches | Severity: Minor**

The SEIR local and global search results both show k = 10.0 in the parameter tables, suggesting k is fixed rather than estimated. This is not stated explicitly in the text. Since k directly controls the log-likelihood value via the negative binomial variance, fixing it without disclosure affects the interpretation of model comparisons.

*Suggested author action:* State explicitly whether k is fixed or estimated in the SEIR searches. If fixed, justify the choice. If estimated, the optimization should show k varying from its starting value.

---

**ID: 25.07.8 | Concern: ACF interpretation in EDA contradicts SARIMA choice | Severity: Minor**

The EDA section claims the oscillating ACF pattern "supports that the data is non-stationary." An oscillating, slowly decaying ACF is characteristic of a seasonal stationary process, not evidence of non-stationarity. The chosen SARIMA model uses d = 0 and D = 0 (no differencing), which is correct for a stationary seasonal series. The EDA narrative contradicts the modeling decision.

*Suggested author action:* Revise the EDA narrative: an oscillating ACF with gradual damping supports the presence of seasonal autocorrelation within a stationary process, which motivates SARIMA(p,0,q)(P,0,Q) rather than SARIMA with differencing.

---

**ID: M1 | Concern: R0 derivation not connected to fitted parameters | Severity: Minor**

The paper derives R0 = β/γ analytically and discusses endemic equilibrium conditions, but never evaluates R0 using the fitted parameter estimates. The SIRS local search gives a ≈ 2.79 and μ_IR ≈ 2.97, implying R0 ≈ 2.79/2.97 ≈ 0.94 (below the epidemic threshold of 1), which would suggest dengue cannot sustain an epidemic — yet the model clearly tracks a seasonal epidemic. This tension is not discussed.

*Suggested author action:* Compute R0 from the maximum-likelihood estimates for both SIRS and SEIR and interpret the result in the context of dengue epidemiology. Discuss whether the fitted R0 is consistent with the observed dynamics.

---

**Additional minor items:**

- The SIRS model uses sin(2π(t+d)/52) while the SEIR uses cos(2π(t−φ)/T) for seasonal forcing. These differ by a 90-degree phase shift and the notation for the phase parameter (d vs. φ) is not reconciled between models.

- The SMA root in the SARIMA fit is |z| = 1.266, relatively close to the unit circle; borderline invertibility is worth noting.

- Typos in the manuscript: "misspeciification," "noncovergence" (Introduction); "incorporateed," "consturcted," "Both od the," "theses approaches" (Conclusion).

- Reference [2] cites ChatGPT for AIC table functions. The generated functions should be included in full in the appendix to allow verification.
