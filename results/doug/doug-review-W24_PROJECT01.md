# Peer Review: W24 Project 01
## "A Latent Process of Democracy since 1800"

---

## Summary

This project applies a POMP compartmental model (S-P-R-N) to explain the annual count of new democracies globally from 1800 to 2020, drawing on Acemoglu and Robinson's game-theoretic democratization theory. The model treats the transition through sovereign statehood (S), powerful-elite accumulation (P), revolutionary-threat period (R), and negotiated democracy (N) as a latent Markov chain, with the annual increment in democracies as a negative-binomial measurement. Iterated filtering (IF2) with 200 starting values is used to maximize the likelihood. While the project demonstrates genuine intellectual ambition in bridging POMP methodology with political science theory, it suffers from several critical methodological problems: a structural mismatch between the written model and the code, an unidentified parameter introduced silently under a different name, the absence of convergence diagnostics, the use of a global-aggregate series that violates fundamental modeling assumptions, and an implausible mechanistic interpretation of the fitted parameters.

---

## Major Issues

### 1. Undisclosed parameter substitution: `mu_IR` replaces `mu_PR` in the RDS results

The text describes five parameters: Beta, rho, k, mu_PR, and mu_RN. The Csnippet code uses the name `mu_PR`. However, the saved results object (`Level 2.5.rds`) contains columns Beta, rho, k, mu_RN, and **mu_IR** — not mu_PR. The column rename in the analysis code (`colnames(result)[5] <- "mu_PR"`) silently patches the mismatch at display time rather than explaining it. It is not clear whether mu_IR in the results is actually the same parameter as mu_PR in the model, whether the saved RDS was generated from a different model version, or whether the Csnippet that was actually run differs from the one shown. This discrepancy makes it impossible to verify that the displayed parameter estimates correspond to the stated model.

### 2. Critical error in the process model: `N/tot_sov` used where `R/tot_sov` is specified in the text

The mathematical specification of the S→P transition rate is:

    β * R(t) / ζ(t)

where ζ(t) = S(t) is the covariate. However, the Csnippet implements:

    double dN_SP = rbinom(S, 1 - exp(-Beta * N/tot_sov * dt));

The force of transition is driven by **N** (democracies already formed), not by **R** (revolutionary threats). The transition is therefore driven by the very outcome the model is trying to predict, rather than by the latent threat variable. This is both a mismatch between text and code and a substantive mechanistic error. The causal logic of the model — that revolutionary threats induce democratization — is not implemented.

### 3. Observation variable conflates increments and levels; measurement model is dimensionally inconsistent

The outcome modeled is ΔZ(t) = max(0, Z(t) − Z(t−1)), the annual increment of democracies. But the latent state N(t) accumulates all democracies since t=0 (it is absorbing — nothing leaves N in the Csnippet). The measurement model ΔZ(t) ~ NegBin(ρ·N(t), k) therefore maps a one-year increment onto a stock that grows monotonically to ~90 by 2020, while the observed ΔZ(t) fluctuates near zero to ~20 annually. The expected value ρ·N(t) is an ever-increasing trend, whereas ΔZ(t) shows no such systematic trend in most of the 1800–1980 period. The model is structurally misspecified for the chosen observation.

### 4. No convergence diagnostics presented

The project reports running 200 IF2 searches from random starting values but presents no convergence evidence: no log-likelihood traces across IF2 iterations, no scatter of final log-likelihoods across runs as a function of starting values, and no comparison of the best log-likelihood achieved to what would be expected if convergence were reached. The pairs plot of loglik vs. parameters (Figure 2) shows all 200 values clustered near −212, but this could equally reflect a plateau in the optimization landscape or genuine convergence. Wheeler et al. (2024, §Computational adequacy) require replicate searches reaching similar likelihoods, along with convergence traces, before concluding that the MLE has been found. Without these diagnostics, the reported best log-likelihood of −211.85 may be well above the true maximum, invalidating all subsequent inference.

### 5. The "profile likelihood" plots are not profile likelihoods

The paper labels Figure 4 "Confidence Interval of the Parameters" and uses horizontal cutoff lines at the chi-squared threshold, calling this a profile likelihood analysis. However, the plot is simply a scatter of loglik versus each parameter across the 200 global search runs, not a proper profile likelihood where all other parameters are optimized at each fixed value of the parameter of interest. Profile likelihoods constructed from random-start global search scatter will be biased upward (the envelope of suboptimal runs) and do not yield valid confidence intervals. The confidence intervals reported from this plot are therefore unreliable. A proper profile likelihood requires fixing the target parameter on a grid and re-optimizing all remaining parameters at each grid point (Wheeler et al. 2024, §Parameter identifiability).

### 6. Aggregate global count is not a POMP-appropriate observation

The unit of observation is the global total of sovereign democracies aggregated across all countries at each year. Aggregating a heterogeneous panel of 222 country-level Markov chains into a single count and then fitting a single-chain POMP model assumes that all countries are exchangeable and at the same stage of a single latent process. This is not a modeling simplification — it is a category error. The same latent state N represents simultaneously the US in 1800 and Benin in 1991. The model cannot accommodate the fact that different countries enter democracy at different times for different reasons. The meaningful POMP application would be at the country level or with a spatiotemporal model, not the global aggregate.

### 7. The POMP model is outperformed by a simple negative binomial regression; this is not adequately addressed

The benchmark comparison (Table in Section 2.2) correctly shows that a two-parameter negative binomial regression with time as the only covariate achieves a substantially better log-likelihood than the five-parameter POMP model. The paper acknowledges this but dismisses it as follows: "this does not capture the nuances of the endogenous mechanism." This dismissal is not scientifically acceptable. A more complex mechanistic model that achieves lower likelihood than a two-parameter regression represents evidence of model misspecification, not a "competitive" result. The authors should have used this failure to diagnose where the POMP model is misspecified and revised accordingly, rather than proceeding to interpret parameters from an inferior model.

### 8. Initial conditions are fixed at implausible values without justification or sensitivity analysis

The initial compartment values are fixed: S=23, P=1, R=2, N=1. The value S=23 approximates the number of sovereign states in 1800, but P=1, R=2, and N=1 are arbitrary. Given the short data period relative to the assumed transition rates, the initial conditions are likely to strongly influence the likelihood surface. No sensitivity analysis to initial conditions is presented. Wheeler et al. (2024, §Initial conditions) note that initialization strategy affected AIC by ~72 units for one model in their analysis, illustrating how consequential this choice can be.

### 9. The `mu_IR` (displayed as `mu_PR`) parameter is completely unidentified

The RDS results show that the fifth parameter (mu_IR / mu_PR) ranges from 0.035 to 839 across the 200 runs, yet the log-likelihood values are nearly identical (all near −212). This enormous spread with flat likelihood is the signature of a completely unidentifiable parameter. Despite this, the paper states that "the parameter estimates are well identified" and reports a confidence interval. The parameter is not identified, and inference based on its estimated value is meaningless.

---

## Minor Issues

### 10. Figure caption numbering error

The code assigns both Figure 7 (simulation plot) and the probes plot to `cap_fig7`, so two figures share the caption "Figure 7." Figure 4 caption also says "Figure 4" but is rendered after what is labeled as "Figure 2" for the simulation result, creating a numbering discontinuity.

### 11. The `AIC.iid` calculation uses only 2 parameters

The IID log-likelihood is computed from a two-parameter negative binomial, so `AIC.iid <- 2 - 2 * log.iid` uses `2*1` rather than `2*2 - 2*log.iid`, understating the IID model's AIC penalty. This is a minor bug but affects the table comparison.

### 12. Measurement model interpretation of ρ is non-standard and unexplained

The parameter ρ is described as "coding efficiency" — the probability that a country's historical democratic status was correctly recorded by future coders. This is a creative but unvalidated repurposing of the reporting-rate concept from epidemiology. The probability that 93% of democratic episodes were unrecorded (since ρ ≈ 0.07 at the MLE) is not plausible, and no independent evidence is offered for this interpretation.

### 13. Grammatical and presentation issues throughout

The paper contains numerous grammatical errors ("A society is said to have a democratic regime when they can determine", "both of these are plausible insights that the model suggests"), inconsistent notation (the transition equation for S→P uses both `N` and `R` in different parts of the document), and equations that are not typeset as full equalities but fragments (e.g., equation 1 has a spurious double `+` sign).

### 14. The covariate `tot_sov` is the smoothed spline interpolation of S, not S itself

The covar.csv file contains monthly interpolated values of `tot_sov` as a smoothed spline. The text states "ζ(t) = S(t) is the covariate smoothed with a cubic spline," but the model also has S as a dynamic latent state initialized at 23. The relationship between the latent S and the covariate tot_sov is not explained. In the Csnippet, `tot_sov` is used as the denominator (covariate), while S is a stock that depletes as countries gain powerful elites. Whether S and tot_sov are meant to represent different things, and how the latent S is depleted to eventually zero while tot_sov grows to ~195 by 2020, is never clarified.

### 15. No forecast or simulation from the filtering distribution

The simulation in Figure 7 generates 20 trajectories from the estimated initial conditions (t=0), not from the filtering distribution. Forward simulation from the filtering distribution (conditioning on observed data up to each point) would provide a more meaningful check of model adequacy and is standard practice in POMP analysis (Wheeler et al. 2024, §Forecasts). The divergence of simulated trajectories from data visible in Figure 7 further underscores the model misspecification issues noted above.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/meta-skill/SKILL.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project01/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project01/covar.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project01/df_dems.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project01/Level 2.5.rds`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project01/Makefile`
