# Final AI Review
## Project: final_project_w22 / project03
## Reviewer: Evan (Treatment E, claude-sonnet-4-6)

---

## Overall Assessment

This project applies ARIMA and a custom POMP compartmental model to monthly subscriber data for a single Twitch streamer (~60 months). The ARIMA section is organized and the grid-search approach to model selection is reasonable. However, the work has critical technical deficiencies in both its POMP implementation and its model comparison. The POMP measurement model (`dmeas`) contains a stochastic draw that violates the pomp framework's determinism requirement, combined with an illegal likelihood-clipping operation that inverts the particle filter's weighting logic; these errors make the reported log-likelihood of −866.06 uninterpretable. No convergence diagnostics are shown and no parameter estimates are reported. The stated conclusion that the ARIMA model outperforms the POMP model is completely ungrounded because the ARIMA log-likelihood is never reported in comparable units. The paper would benefit substantially from correcting the measurement model, reporting both log-likelihoods on a common scale, and showing mif2 convergence traces.

## Key Strengths

- **Systematic AIC grid search:** The 4×6 grid over ARIMA(p,1,q) orders is a principled model selection approach that demonstrates awareness of the model space.
- **Correct logmeanexp aggregation:** The POMP code correctly aggregates log-likelihoods across 8 replicated pfilter runs using `logmeanexp(se=TRUE)`, which is the appropriate method for Monte Carlo likelihood estimation.
- **Domain-motivated compartmental model:** The BVS (Beginning–Viewer–Subscriber) model connects the Twitch platform's audience funnel to a compartmental structure with a random-walk transmission rate, showing genuine modeling thought applied to a novel domain.
- **Clear EDA presentation:** The three-panel transformation plot (raw → first-difference → log-diff) is an effective visualization of the stationarity-achieving process.

## Major Points

**ID: 22.03.2**
**Concern:** The stated conclusion that the ARIMA model outperforms the POMP model is entirely ungrounded.
**Why it matters:** The POMP log-likelihood is −866.06, but the ARIMA log-likelihood is never reported anywhere in the paper. Without both values on a comparable scale, the comparison is meaningless. Furthermore, the ARIMA model may have been fitted to a transformed series (log or log-differenced) while the POMP model is fitted to raw counts, making direct likelihood comparison invalid without explicit acknowledgment.
**Severity:** Major
**Suggested author action:** Report the log-likelihood of the ARIMA model. Clarify what series each model is fitted to. If the likelihoods are on different scales, acknowledge this and either standardize or describe the limitation. Remove the claim that one model "performs better" unless a valid comparison is available.

**ID: 22.03.3 / 22.03.4**
**Concern:** The POMP measurement model (`dmeas`) is fundamentally broken in two ways.
**Why it matters:** First, `dmeas` contains the line `double Views = rbinom(N-S, 1-exp(-Beta*S/N));` — a stochastic random draw. The pomp framework requires `dmeas` to be a deterministic function of state and observation; a random draw makes particle weights non-reproducible and theoretically invalid. Second, the code clamps `lik=0` whenever `lik>0`. Since `dnorm(..., give_log=1)` returns a log-density that can be positive near the mode of a tight distribution, this clamp systematically discards the highest-weight particles, inverting the purpose of importance weighting. Together, these errors make the particle filter produce meaningless weights and the reported log-likelihood is not interpretable.
**Severity:** Major
**Suggested author action:** Rewrite `dmeas` with a deterministic mean derived from state variables only (no stochastic draws). Use a count-appropriate density function (e.g., `dpois` or `dnbinom`). Remove both `lik` clipping operations entirely.

**ID: 22.03.5**
**Concern:** No convergence diagnostics are shown for the mif2 runs.
**Why it matters:** Without trace plots of log-likelihood and key parameters vs. mif2 iteration, there is no evidence that the optimizer has found the MLE rather than a poor local optimum. The reported LL = −866.06 may substantially understate the true model likelihood.
**Severity:** Major
**Suggested author action:** Show trace plots of log-likelihood and each estimated parameter (Beta_sigma, mu_VS, mu_SB, Beta_0) vs. mif2 iteration, for at least a representative subset of starting points. Verify that multiple restarts converge to similar LL values.

**ID: 22.03.6**
**Concern:** No parameter estimates from the POMP fit are reported.
**Why it matters:** Without the fitted values of Beta_sigma, mu_VS, mu_SB, and Beta_0, the model's scientific implications cannot be assessed, the results cannot be reproduced, and it is impossible to judge whether the parameter values are domain-plausibly reasonable.
**Severity:** Major
**Suggested author action:** Report the MLE parameter vector from the best-fitting run, with units and domain interpretation for each parameter.

## Minor Points

- **22.03.1 — Transformation pipeline documentation:** The paper shows log-differencing as exploratory EDA but then fits ARIMA(1,1,2). Clarify explicitly which series (log-subscribers or log-differenced subscribers) is passed to `arima()`. If log-subscribers with d=1, the EDA plots are consistent; if log-differenced, the d=1 inside ARIMA would be redundant.

- **22.03.7 — AR root near unit circle:** The AR root of 1.01363 is noted but not discussed further. Consider whether this suggests d=2 is more appropriate or whether it reflects genuine near-unit-root behavior with implications for prediction interval validity.

- **22.03.8 — R² not appropriate for ARIMA:** R² = 0.983 is reported. R² is not a standard or meaningful metric for ARIMA models estimated by MLE; replace with log-likelihood or AIC.

- **22.03.10 — N fixed at 41.5 million without justification:** The total Twitch user base is used as the population size for one channel's subscriber model. The relevant population is the channel's audience reach, not the entire platform. Justify or estimate N from data.

- **22.03.11 — Residual ACF described as white noise prematurely:** Multiple lags (approximately lags 2–3) in the residual ACF appear to exceed the 95% band. A Ljung-Box test would quantify whether this pattern is systematic.

- **22.03.9 — Periodogram spike at f ≈ 0.5 not explained:** A prominent spike at the Nyquist frequency is visible but not commented upon. Even a brief explanation (aliasing artifact, or bimonthly pattern tested and rejected) would strengthen the analysis.

- **Presentation — missing reference list:** The single citation "[1]" in the text has no corresponding bibliography entry anywhere in the document.

- **Presentation — supplement formatting:** The POMP supplement appears to be a browser-printed HTML file exposing a local file path in the header. It should be compiled cleanly before submission.

- **Unacknowledged strength — forward simulation:** The simulation plot (supplement p. 3) shows the BVS model generating trajectories qualitatively consistent with the observed growth pattern. This should be acknowledged as preliminary evidence that the model structure is reasonable, even if quantitative fit requires further work.
