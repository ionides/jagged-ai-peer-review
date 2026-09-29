# Final AI Review
# Study of daily COVID-19 Infected cases in the United States
# STATS 531 W21 — Project 02

> Challenge skipped — Grounding signal was Strong.

---

## Overall Assessment

This project attempts an ambitious comparison of three mechanistic compartmental models (SEIR, SECSDR, SEIQR) fitted to 14 months of US daily COVID-19 case counts using iterated filtering in the pomp framework. The honest admission that none of the models can reproduce the multi-wave epidemic trajectory is commendable and scientifically appropriate — the data genuinely challenges simple SIR-family models with fixed parameters. However, the analysis has a cluster of measurement model errors that undermine every log-likelihood value reported, several code-level structural inconsistencies (a phantom parameter, a missing compartment, a 10-fold population size error across models), no non-mechanistic baseline for comparison, and no uncertainty quantification. These problems mean that the reported likelihoods cannot be trusted as measures of model fit, and the conclusion that the models "fail" may reflect coding errors as much as genuine model inadequacy. The project demonstrates familiarity with the pomp workflow but requires substantial corrections before its conclusions can be taken at face value.

---

## Key Strengths

**21.02.S1 — Multiple model structures compared**
Three distinct compartmental models are constructed and fitted. The progression from SEIR to SECSDR (adding a carrier/asymptomatic compartment) to SEIQR (adding quarantine) reflects genuine scientific motivation about COVID-19 transmission biology. The side-by-side comparison at the design level is informative even if the fitting results are unreliable.

**21.02.S2 — Honest reporting of model failure**
The authors do not attempt to overfit or selectively report runs that happen to look reasonable. Figures 6, 10, and 15 all show simulated trajectories that clearly diverge from the observed data, and this is acknowledged directly. The conclusion offers substantive qualitative explanations for why these models struggle with a 14-month US epidemic.

**21.02.S3 — Filter diagnostics included**
Filter diagnostics (ESS and conditional log-likelihoods) are shown for SECSDR (Figure 8) and SEIQR (Figure 13). This is the correct practice for particle-filter-based inference and is commendable even if the results reveal numerical problems.

---

## Major Points

**21.02.1 — Inconsistent measurement model in SEIR (dmeas/rmeas mismatch)**
Severity: Major

In the SEIR model, `dmeas` sets `sd_cases = sqrt(mean_cases * mean_cases)`, which equals `mean_cases = rho*H` — a Normal distribution with mean equal to its standard deviation. Meanwhile, `rmeas` uses `sqrt(rho*H)` as the standard deviation. These two snippets describe different distributions: one has variance proportional to the square of the mean, the other proportional to the mean. A mismatch between `dmeas` and `rmeas` produces incorrect likelihoods because particles are sampled from one distribution and scored under another, making the reported log-likelihood of -5504 meaningless.

Suggested author action: Adopt a single consistent noise model in both `dmeas` and `rmeas`. For count data, a negative binomial model (e.g., `dnbinom_mu(Infected, mu=rho*H, size=psi, give_log)`) is the standard course approach and handles overdispersion cleanly.

---

**21.02.2 — Phantom parameter `tau` in SEIR**
Severity: Major

`tau` is declared in `paramnames` and assigned a log-transform in `partrans`, but it appears nowhere in `seir_step`, `dmeas`, or `rmeas`. The global search reports an estimated value of tau = 4.61, meaning the optimizer is spending resources on a parameter with no effect. This wastes search capacity and is likely symptomatic of an incomplete refactoring of the measurement model (tau may have been intended as an overdispersion parameter but was never implemented).

Suggested author action: Remove `tau` from `paramnames` and `partrans`, or implement it as an overdispersion parameter in the measurement model (e.g., the size parameter of a negative binomial).

---

**21.02.3 — E compartment absent from SECSDR statenames and rinit**
Severity: Major

The SECSDR model diagram (Figure 7) shows a six-compartment system S→E→Ca→Sy→Di→R. However, `covid_statenames <- c("S","Ca","Sy","R","Di")` omits E entirely, and the rinit does not initialize E. The transition code draws `dN_SE = rbinom(S, ...)` (the number leaving S) and then immediately `dN_ECa = rbinom(dN_SE, ...)` — in effect, individuals transition from S to Ca in a single time step without any E residence time. This collapses the S→E→Ca pathway into a single instantaneous transition, contradicting the model's stated biological motivation of an exposed-but-not-yet-infectious period.

Suggested author action: Add E to statenames, initialize it in rinit, and split the transition into two separate steps: `dN_SE = rbinom(S, ...)` removing individuals from S into E, and `dN_ECa = rbinom(E, ...)` moving individuals from E to Ca.

---

**21.02.4 — SEIQR population size N=32,000,000 inconsistent with US scale**
Severity: Major

The SEIR and SECSDR models use N ≈ 300–328 million (US population). The SEIQR model hard-codes N=32,000,000 — approximately California's population, not the US total. Daily observed cases peak at approximately 300,000 during the winter 2020–21 wave. With N=32M, a single day at that peak infects roughly 1% of the total susceptible population; over a few months the model would exhaust susceptibles. This order-of-magnitude discrepancy in the population parameter fundamentally alters epidemic dynamics and makes the SEIQR log-likelihoods (-7125) incomparable to those from the other models.

Suggested author action: Set N = 328,000,000 (or the same value used in other models) for SEIQR. Check that initial conditions scale appropriately and rerun the global search.

---

**21.02.5 — SEIQR and SECSDR measurement models use rho as noise parameter, not reporting rate**
Severity: Major

In both SECSDR (`dnorm(Infected, Di, rho*Di+1e-10, give_log)`) and SEIQR (`dnorm(Infected, Q, rho*Q+1e-10, give_log)`), the expected observation equals the latent compartment count (Di or Q) directly — there is no separate reporting fraction. `rho` controls only the standard deviation of the noise. This means the model assumes all diagnosed or quarantined individuals are observed exactly (100% reporting), which is implausible for a nationwide COVID-19 dataset during a period of known testing shortages. Estimated rho values of 0.25–0.48 imply that the standard deviation is 25–48% of the latent count, an extremely wide observation distribution.

Suggested author action: Introduce an explicit reporting fraction parameter (conventionally also called rho, but used as the mean: `rnorm(rho*Q, sigma*sqrt(rho*Q))`) and a separate overdispersion parameter for the noise. This follows course conventions and is more epidemiologically interpretable.

---

**21.02.6 — No non-mechanistic benchmark**
Severity: Major

No ARMA, ARIMA, or other non-mechanistic model is fitted or compared. Without a quantitative baseline, it is impossible to judge whether the mechanistic models' log-likelihoods represent a meaningful gain or loss relative to a simple time-series model, and impossible to assess whether the model failures are due to structural inadequacy or numerical problems. For example, the SECSDR achieves a best log-likelihood of -3509; whether this is competitive with an ARMA model on the same data is unknown.

Suggested author action: Fit an ARIMA model to the log-transformed daily case series and report its log-likelihood. This provides a quantitative anchor for assessing all three POMP models.

---

**21.02.7 — Numerically absurd log-likelihood values in SEIQR convergence diagnostics**
Severity: Major

Figure 13 (filter diagnostics for SEIQR, last iteration) shows conditional log-likelihoods reaching approximately -1.5e+13. Figure 14 (MIF2 convergence traces for SEIQR) shows overall log-likelihoods near -2e+14. These values are orders of magnitude below what any particle filter on 430 daily observations should produce — even a completely misspecified model would not yield values below about -50,000. Values around -1e14 indicate a numerical overflow, a probability evaluation returning zero for all particles, or a unit error in the measurement model. The "top five log likelihoods" in Section 5.2 (-7125 to -8147) appear inconsistent with the trace values and may come from a different code path.

Suggested author action: Inspect the SEIQR pfilter for zero-probability events (e.g., `rho*Q+1e-10` becoming effectively zero when Q=0 at the start). Add a floor to the standard deviation and ensure Q does not collapse to zero for all particles. Reconcile why the global search likelihoods differ so dramatically from the trace-plot values.

---

**21.02.8 — No profile likelihoods or confidence intervals**
Severity: Major

All three models report only point MLE estimates from global search with no uncertainty quantification. Profile likelihood plots, MCAP confidence intervals, and Monte Carlo standard errors on the log-likelihood are all absent. Given that the MIF2 convergence diagnostics show parameter traces that fail to converge (Figures 9, 14 — traces are flat from iteration 0 with no systematic movement), the reported MLEs may not represent true maxima. Without profiles, the claimed parameter values have no associated uncertainty and cannot be compared to external literature.

Suggested author action: Compute profile likelihoods for at least one key parameter per model (e.g., Beta for transmission rate). A 5-point coarse profile is sufficient for a run_level=2 analysis. Report Monte Carlo standard errors on the reported log-likelihoods.

---

## Minor Points

**21.02.m1 — Np and Nmif not reported for any model**
The number of particles and mif2 iterations are not stated anywhere in the manuscript. Without this information, the computational adequacy cannot be assessed and the results cannot be reproduced. The global search table refers to "result.30", "result.46" etc., implying at least 46 starting points, but the total number is not given.

Suggested author action: Report Np, Nmif, and number of global search starts for each model in a brief computational settings table or inline statement.

---

**21.02.m2 — N=328,000,000 hard-coded in SECSDR rinit but inconsistent with no E tracking**
The SECSDR rinit sets S=328,000,000 with Ca=10, Sy=10, R=0 — and since E is absent from statenames, no initial exposed population is set. The initial conditions effectively assume zero individuals are currently exposed, which may or may not be appropriate for day 0 (January 22, 2020), but is not justified.

Suggested author action: After fixing the E compartment omission, initialize E to a small positive value consistent with the known early spread in the US.

---

**21.02.m3 — No EDA or preliminary time-series analysis**
Section 2 provides only a single raw time-series plot. The multi-wave structure visible in Figure 1 (at least three distinct peaks) is directly relevant to why single-parameter SIR-family models fail, but this is not discussed. No ACF, log-transformation, or spectral analysis is presented.

Suggested author action: Add a brief EDA section: plot log(Infected+1), compute the ACF, and comment on the non-stationary, multi-wave structure. This motivates both the model choice and the eventual failure.

---

**21.02.m4 — Data description incomplete**
The data source (IHME) is cited but it is unclear what "Infected" represents — new daily confirmed cases, new hospitalizations, or another metric. The distinction matters for measurement model specification.

Suggested author action: State explicitly in Section 2 what the "Infected" variable represents and how it was collected.

---

**21.02.m5 — Reference list is minimal**
Only course notes and two prior student projects are cited. No primary epidemiological literature on COVID-19 parameter estimation or multi-wave modeling is referenced.

Suggested author action: Add 2–3 references from the COVID-19 modeling literature (e.g., papers estimating R0, incubation period, or reporting rates for the US epidemic) to contextualize the parameter choices and model adequacy.
