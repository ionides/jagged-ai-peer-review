# Final AI Review
## Project: final_project_w22 / project16
## Title: Modeling Covid-19 With Multivariate POMP Model

---

## Overall Assessment

This paper proposes two POMP compartmental models for Covid-19 deaths in Moscow: a multivariate SIR-CDR model that jointly measures confirmed cases, deaths, and recoveries, and a simpler SIR-D model targeting daily deaths only. The authors deserve credit for honest, transparent reporting — they document optimization failures, near-zero ESS, implausible parameter estimates, and a failed profile likelihood without obscuring these results. The multivariate POMP formulation is a genuine technical contribution that goes beyond single-outcome compartmental models. However, neither model achieves an adequate fit, and the paper's analysis reveals several concrete structural errors that likely explain the fitting failures. Addressing these errors would substantially improve the work.

## Key Strengths

**Transparent reporting of model difficulties.** The authors clearly report near-zero ESS in the SIR-CDR particle filter, diverging IF2 optimizations, and the implausible Mu_SyR estimates in the SIR-D model. This level of transparency is scientifically valuable and sets up an informative case study in model diagnosis.

**Multivariate POMP formulation.** The SIR-CDR model's joint measurement of confirmed cases, deaths, and recoveries is a methodologically interesting extension. This structure could, in principle, better identify the model's parameters by leveraging multiple observation streams.

**Appropriate overdispersion in SIR-D.** Using a Negative Binomial measurement model for daily death counts in the SIR-D model is correct and reflects awareness of the overdispersion common in epidemic count data.

## Major Points

**ID: 22.16.A | Process model error in dN_SyD | Severity: Major**

The death transition in the SIR-D model (process model, p. 7) is specified as `dN_SyD ~ Binom(Sy, 1 - exp(-D_rate * Mu_SyR * dt))`. This couples the death hazard to the symptomatic recovery rate `Mu_SyR` multiplicatively. These are biologically distinct quantities. The optimizer can increase the likelihood by inflating `Mu_SyR` (since this increases the death-transition probability), which is a likely primary contributor to the estimated Mu_SyR of 157 (implying ~100% recovery per day — biologically impossible). The SIR-CDR model has a dedicated `mu_SyD` parameter for this transition; the SIR-D model should adopt the same structure. Suggested fix: replace `D_rate * Mu_SyR` with a dedicated death-hazard parameter `mu_SyD` and estimate it independently.

**ID: 22.16.B | Profile likelihood range excludes the MLE | Severity: Major**

The profile likelihood for Mu_SyR (fig_011, fig_012) is computed over [0, 1], but the global search consistently finds optimal values in the range 54–228. The computed profile is entirely outside the likelihood ridge, so the resulting figure is uninformative about the parameter. Suggested fix: extend the profile to cover the range suggested by the global search, or re-run after correcting the dN_SyD formulation.

**ID: 22.16.C | No benchmark comparison | Severity: Major**

Neither model is compared against a non-mechanistic baseline (ARIMA on log-deaths, negative binomial count regression, or any time-series model). Without a benchmark log-likelihood, it is impossible to quantify how much worse the mechanistic models perform, or whether the difficulties arise from model structure versus computational insufficiency. Suggested fix: fit at least one ARMA-type model and compare log-likelihoods.

**ID: 22.16.D | SIR-CDR measurement model uses Poisson (underdispersed) | Severity: Major**

The SIR-CDR model specifies Poisson distributions for all three observations (deaths, confirmed, recovered). For Covid-19 daily counts in a city of 12 million, overdispersion is expected and the variance-to-mean ratio is typically far above 1. The particle filter collapses (near-zero ESS) when the measurement model assigns near-zero probability to the observed data given the latent states — which is exactly what an underdispersed Poisson will do when counts are more variable than Poisson. The SIR-D model correctly uses Negative Binomial; the same should be applied to SIR-CDR. This change alone may be sufficient to make SIR-CDR particle filtering tractable.

**ID: 22.16.E | Sequential binomial draws from shared compartment | Severity: Major**

The process model draws two independent binomial flows from the same compartment S (dN_SA and dN_SSy) and similarly from A and Sy. Multiple independent binomial draws from the same count violate the conservation of individuals. The authors address this with clipping (setting negative counts to zero), but clipping is not equivalent to a proper Euler-Multinomial step and introduces subtle biases in the transition probabilities. The standard approach is a single multinomial draw: `(dN_SA, dN_SSy, remainder) ~ Multinomial(S, p_A, p_Sy, 1-p_A-p_Sy)`. The same applies to compartments A and Sy.

## Minor Points

**ID: 22.16.F | Cap parameter unspecified | Severity: Minor**

The SIR-CDR model includes a hospital capacity parameter `Cap` in the description of the capacity-limited hospitalization mechanism, but this parameter does not appear in the parameter list or in any optimization results. It is unclear whether Cap is fixed, estimated, or effectively ignored in the implementation.

**ID: 22.16.G | k not perturbed in local search | Severity: Minor**

The manuscript states that perturbation is applied to β, μ_AR, μ_SyR, μ_ASy in the local search, and fig_006 confirms k = 10.000 is flat throughout. The overdispersion parameter k is thus not optimized in the local search. Whether this is intentional should be clarified, and it should be either optimized or justified as fixed.

**ID: 22.16.H | Spread in converged global search runs suggests flat likelihood | Severity: Minor**

Among the global search runs that converged (fig_007, right cluster), the log-likelihood range spans roughly -1175 to -1195. This ~20-unit spread among nominally converged runs suggests either a flat likelihood surface or that 10 pfilter replicates introduce substantial Monte Carlo noise in the evaluation. Either interpretation reinforces the identifiability concerns already noted.

**ID: 22.16.I | dN_SyH appears twice in SIR-CDR equations | Severity: Minor**

In the SIR-CDR process model equations (p. 6), `dN_SyH` appears on both line 6 (Sy-to-H) and line 8, where the context indicates `dN_SyD` was intended. This typographical error should be corrected.

**ID: 22.16.J | ESS trace not shown for SIR-D | Severity: Minor**

ESS collapse is noted for SIR-CDR but no ESS diagnostics are shown for either model. For the SIR-D model, an ESS trace would help distinguish computational inadequacy from model misspecification as the source of poor fit.
