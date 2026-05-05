# Final AI Review — Hungarian Chickenpox Infections
## Project 25.06 | STATS 531 W25

---

## Overall Assessment

This project tackles an ambitious comparative analysis of Hungarian chickenpox dynamics using three fundamentally different modeling paradigms: ARMA time-series models, a stochastic seasonally-forced SEIR implemented via the POMP framework, and a deep learning pipeline combining variational mode decomposition with N-BEATS. The breadth of approach is a genuine strength. The SEIR-POMP component is methodologically sound in broad strokes — the negative binomial measurement model, Euler-discretized stochastic transitions, seasonal cosine forcing, and run_level=3 computation (Np=5000, Nmif=100, 20 local + 100 global runs) reflect serious effort. However, several substantive issues affect the reliability of reported results: the profile likelihood for the reporting rate rho is not constructed using standard methods and uses an incorrect confidence interval threshold; the seasonal amplitude parameter amp does not converge across local search chains; and fitted parameter values for the latent period are biologically implausible for chickenpox without any acknowledgment or explanation. The cross-model comparison also lacks a common evaluation framework, limiting what can be concluded from the stated results.

---

## Key Strengths

- **S1. Multi-framework comparative design.** Applying three methodologically distinct approaches (ARMA, POMP, deep learning) to the same dataset is unusual and valuable. The project explicitly frames the comparison around interpretability, forecasting accuracy, and mechanistic realism.

- **S2. Sound SEIR-POMP specification.** The negative binomial measurement model with overdispersion parameter k, stochastic binomial transitions with Euler approximation, and cosine seasonal forcing are all appropriate choices. The model includes waning immunity (omega), making it a genuine SEIRS structure.

- **S3. Serious computational investment.** run_level=3 with 5000 particles, 100 mif2 iterations, 20 independent local chains, and 100 global starting points represents substantial HPC usage for a course project. Both local and global search strategies are employed.

- **S4. Deep learning section is technically substantive.** The VMD + N-BEATS pipeline is clearly motivated, the architecture is explained with appropriate mathematical detail, and the low validation MAPE (2.5–3%) demonstrates that the implementation is functional.

- **S5. Correct handling of AIC comparability.** The authors correctly note that AIC from ARMA on log-transformed vs. original-scale data are not directly comparable, avoiding a common course error.

---

## Major Points

**25.06.M2 — Profile likelihood for rho is not a valid profile; CI threshold is incorrect**

The "Profile Likelihood for rho" (figure 14) is constructed by filtering global search results by rho value and applying a threshold of `maxloglik - 4`. This is not a standard profile likelihood. A true profile fixes rho at a sequence of values, re-optimizes all remaining parameters at each fixed value, and takes the conditional maximum. The approach used here is a "poor man's profile" approximation — acknowledged in the text — but the CI threshold is additionally incorrect: the standard 95% CI threshold is `maxloglik - 0.5 * qchisq(0.95, df=1)` = `maxloglik - 1.92`, not `maxloglik - 4`. The current threshold is too lenient and will produce an interval that is wider than the nominal 95% level. The reported CI (rho: 0.869 to 0.987) should be treated as unreliable.

Severity: Major. Suggested action: Either construct a proper profile by running mif2 at fixed rho values on a grid of at least 10–15 points, or explicitly label figure 14 as a "poor man's profile approximation," correct the threshold to maxloglik - 1.92, and add caveats about the limitations of this approach.

**25.06.M5 — amp parameter does not converge in local search; not acknowledged**

Figure 9 (local search traces) clearly shows that the `amp` (seasonal amplitude) parameter drifts without stabilization across all 20 chains at 100 iterations. The trace for amp spans approximately 2.1 to 2.9 at the final iteration with no sign of collapse toward a common value. The text states "parameters stabilized relatively quickly" and attributes "persistent drift or high variability" to unnamed parameters without identifying amp specifically. Non-convergence in the seasonal amplitude — a key parameter for this seasonal disease — undermines the reliability of all reported parameter estimates and the conclusion that local search "offered a reliable foundation" for inference.

Severity: Major. Suggested action: Identify amp (and mu_IR) explicitly as non-converging parameters. Consider extending to 200 or 300 mif2 iterations for a second stage. Qualify all parameter estimates with the caveat that the optimization may not have reached a stable maximum for these parameters.

**25.06.NEW-A — Fitted latent period is biologically implausible for chickenpox**

The fitted mu_EI values from the local search consistently fall between 0.129 and 0.158 per week. A rate of 0.13/week corresponds to a mean time in the Exposed compartment of approximately 7.7 weeks (54 days). For varicella-zoster virus, the standard incubation period is 10–21 days, corresponding to mu_EI of approximately 0.33–0.7 per week. The fitted value is 2–5 times lower than epidemiologically expected. This discrepancy is not acknowledged or discussed anywhere in the manuscript. It suggests either model misspecification (e.g., the E compartment is absorbing dynamics that should be elsewhere) or parameter non-identifiability in which mu_EI is compensating for another poorly constrained parameter.

Severity: Major. Suggested action: Compare fitted mu_EI to published estimates for chickenpox incubation periods. Discuss whether the discrepancy reflects structural model limitations or identifiability issues. If mu_EI is not identifiable from this data, consider fixing it to a biologically justified value and profiling other parameters.

**25.06.M9 — Lambda importation term described mathematically but absent from code**

The mathematical formulation includes a lambda term in the dI equation ("dI = sigma*E - gamma*I - mu*I + lambda"), described as an importation rate for random infectious arrivals. However, the seir_step Csnippet contains no lambda term — the update for I is simply `I += dN_EI - dN_IR`. The paramnames vector also does not include lambda. This is a direct discrepancy between the stated model and the implemented model.

Severity: Major. Suggested action: Either add lambda to the code with an appropriate value and justification, or remove it from the mathematical description. If importation was intentionally excluded from the final implementation, state this explicitly.

---

## Minor Points

- **25.06.M4 — No seasonal ARMA component despite strong 52-week periodicity.** The data shows clear annual cycles (visible in figures 1 and 2). The ARMA(4,4) model contains no seasonal terms. The near-unit-root AR polynomial (two roots at modulus 1.0008, figure 7) suggests the model is straining to approximate seasonal structure. A SARIMA(p,d,q)(P,D,Q)[52] specification would be a natural extension. Severity: Minor.

- **25.06.M3 — ARMA residual ACF x-axis is in normalized units, not lags in weeks.** Figure 5 shows the lag axis running from 0 to 1.0 rather than showing integer lag values 0–50. This makes it impossible to identify which specific lags are borderline significant, undermining the residual diagnostic. Severity: Minor.

- **25.06.M7 — No common evaluation framework across the three methods.** ARMA is evaluated on training-set MAPE (37%), the deep learning model on validation-set MAPE for 1–2 step forecasts (2.5–3%), and POMP is shown only visually. These use different data splits, different forecast horizons, and different inputs. The deep learning model uses 20-county multivariate data (1220 features) while ARMA and POMP use only national aggregates — a substantial information advantage that is not acknowledged. Comparative superiority claims are not supported by the evidence as presented. Severity: Minor.

- **25.06.M1 — Best POMP log-likelihood not reported in text.** The global and local search tables contain log-likelihood values but the text never extracts and states the maximum log-likelihood from the POMP model. Comparing ARMA loglik (-3603.27) to the best POMP loglik would directly quantify the value (or cost) of mechanistic structure. Severity: Minor.

- **25.06.NEW-B — ESS monitoring absent.** Effective sample size trajectories from the particle filter are not shown. ESS is a standard diagnostic for particle degeneracy. Its absence makes it impossible to assess the quality of the likelihood approximation. Severity: Minor.

- **25.06.M12 — Model is SEIRS but called SEIR throughout.** The model includes waning immunity (omega, R→S transitions), making it a SEIRS model. The text consistently calls it SEIR. Severity: Minor.

- **25.06.M6b — loglik.se filter threshold of 10 is too loose.** The code retains runs with loglik.se < 10. Standard practice uses se < 1 (or < 0.5). A threshold of 10 may retain runs where the likelihood estimate has very high Monte Carlo noise, compromising parameter selection. Severity: Minor.
