# Final AI Review
## Project: final_project_w22 / project19
## Title: An Analysis of the Omicron Variant of COVID-19 Cases in Wayne County

---

## Overall Assessment

This project applies both ARIMA and stochastic SEIR modeling to 121 days of Omicron-wave COVID-19 case data from Wayne County, Michigan. The paper is well-structured and demonstrates competent use of the pomp framework: logmeanexp aggregation is correctly applied, global search uses 500 starting points with multi-stage cooling, and a profile likelihood for the overdispersion parameter tau is attempted. These are meaningful contributions for a course project. However, several methodological issues limit the reliability of the conclusions. The most consequential is the direct comparison of ARIMA and SEIR log-likelihoods without acknowledging that the two are computed under different probability models; this comparison, as presented, is misleading. Additionally, the profile likelihood for tau is too sparse to yield a valid confidence interval, key parameters (beta2 in particular) show extreme instability consistent with non-identifiability, computational parameters (particle count, number of IF2 iterations) are never reported in the text, and no standard POMP diagnostics (ESS, conditional log-likelihoods) are presented. With these issues addressed, the paper would be substantially stronger.

---

## Key Strengths

**ID: 22.19.S1 — Correct likelihood aggregation**
logmeanexp is correctly applied to replicated particle filter evaluations throughout (starting-point assessment, local search evaluation, global search evaluation, and profile). This reflects proper understanding of Monte Carlo log-likelihood estimation.

**ID: 22.19.S2 — Motivated two-phase transmission model**
The choice to parameterize two separate transmission rates (beta1 for days 1–17, beta2 for days 18–121) is grounded in the documented timeline of the Omicron variant's arrival in Wayne County, making the model structure scientifically motivated rather than ad hoc.

**ID: 22.19.S3 — Global search design**
500 random starting points with multi-stage mif2 cooling (decreasing cooling.fraction.50 from 0.5 to 0.1 across seven IF2 calls) represents a serious computational effort to find the global maximum. The pairs plots of starting values vs. filtered estimates provide useful visual evidence of parameter compression.

**ID: 22.19.S4 — Overdispersed measurement model**
The truncated-normal measurement model with variance (tau*H)^2 + rho*H correctly captures both additive and Poisson-scale overdispersion and is consistently implemented in dmeas and rmeas.

---

## Major Points

**ID: 22.19.M1**
**Concern:** The log-likelihood comparison between ARIMA(4,1,4) (-618.74) and the SEIR model (-861.13) is presented as a direct model comparison, but no discussion is provided of whether the two likelihood values are on a comparable scale. The ARIMA likelihood is a Gaussian continuous-data log-likelihood; the SEIR likelihood is a particle-filter approximation to the marginal log-likelihood under a discretized truncated-normal measurement model for count data. These may differ in scale for reasons unrelated to model quality (e.g., different normalizing constants, treatment of the floor/ceiling operations on integer counts).
**Why it matters:** The conclusion that "ARIMA model performed better than the SEIR model" rests entirely on this comparison. If the comparison is not scale-valid, the conclusion is unsupported.
**Severity:** Major
**Suggested author action:** Add an explicit caveat that the two log-likelihoods are not directly comparable without further calibration, and frame the ARIMA result as a descriptive benchmark rather than a formal model selection criterion. Alternatively, compare models using a held-out predictive criterion (e.g., one-step-ahead RMSE) that is scale-neutral.

**ID: 22.19.M2**
**Concern:** The profile likelihood for tau has only two points above the chi-squared threshold (as the authors themselves acknowledge), making the reported 95% CI [0.669, 0.706] statistically meaningless. The CI is simply the minimum and maximum tau values among two points, not a principled likelihood-based interval.
**Why it matters:** Profile likelihood is the primary identifiability and uncertainty tool used in this paper. If the profile is too sparse to draw conclusions, the paper has no valid uncertainty quantification for any parameter.
**Severity:** Major
**Suggested author action:** Run a dedicated profile sweep with at least 30–50 fixed tau values spanning the plausible range (e.g., 0.1 to 0.9), maximizing over all other free parameters at each grid point, then re-report the CI. Also note that the output table incorrectly displays tau values as percentages (66.88%, 70.62%) due to a code error (`100 * min` applied to values already in [0,1]); this should be corrected.

**ID: 22.19.M3**
**Concern:** Beta2 is severely unstable across runs: local search results show beta2 values of 2.43, 33.9, 78.5, 89.9, 188.4, and 7322.1 at log-likelihoods that span only about 67 units (-884 to -951), and global search values are comparably clustered only because the search space was bounded at 10. This is consistent with near-flat likelihood in the beta2 direction over several orders of magnitude, i.e., a non-identifiability problem.
**Why it matters:** The paper's main scientific claim — whether beta2 > beta1 (supporting Omicron's greater contagiousness) or beta2 < beta1 (contradicting it) — depends directly on beta2. If beta2 is unidentifiable, neither conclusion is supported.
**Severity:** Major
**Suggested author action:** Compute profile likelihoods for both beta1 and beta2. If the profile for beta2 is flat, acknowledge that the two-beta parameterization is not supported by the data and consider either collapsing to a single beta or incorporating external constraints. Withdraw or substantially qualify the biological interpretation of beta2 vs. beta1.

**ID: 22.19.M4**
**Concern:** The particle count (NP), number of IF2 iterations in local search (NMIF_S), and number of iterations in global search (NMIF_L) are referenced throughout the code as variables but never defined or reported anywhere in the manuscript. A reader cannot assess whether the computation was adequate.
**Why it matters:** Computational adequacy is foundational to POMP inference — an underpowered particle filter produces noisy, unreliable likelihood estimates that can mislead both the optimizer and the diagnostic plots.
**Severity:** Major
**Suggested author action:** Add a single sentence or code chunk reporting the actual values: e.g., "NP = [X], NMIF_S = [Y], NMIF_L = [Z]." These values are necessary for any replication or comparability assessment.

**ID: 22.19.M5**
**Concern:** No standard POMP diagnostics are presented for any filter run: no ESS trace over time, no conditional (per-step) log-likelihood plot, no comparison of the filtering distribution against the observed data. The only visual check is a forward simulation from the MLE (Figure 15), which does not condition on observed data and cannot reveal filter degeneracy or systematic model misfit at specific time points.
**Why it matters:** Without ESS and conditional log-likelihood plots, it is impossible to know whether the particle filter is degenerating (especially near the epidemic peak), whether the model fits poorly in particular periods, or whether the likelihood estimates from pfilter are reliable.
**Severity:** Major
**Suggested author action:** For the best-fitting parameter set, produce (a) a plot of ESS vs. time step, and (b) a plot of conditional log-likelihoods vs. time. Also consider plotting the filtering distribution (mean ± 2 SD of filtered state) against observed data.

**ID: 22.19.M6**
**Concern:** mu_EI = 0.1 (incubation period 10 days) and mu_IR = 0.08 (recovery period ~12.5 days) are fixed throughout all searches with no sensitivity analysis. For Omicron specifically, incubation periods as short as 3 days have been reported, which would correspond to mu_EI ≈ 0.33. The choice of these fixed values directly affects the estimated transmission rates and the shape of the epidemic curve.
**Why it matters:** Fixing epidemiological parameters at potentially incorrect values without sensitivity analysis means the paper's transmission rate estimates and likelihood values may reflect model misspecification rather than data signal.
**Severity:** Major
**Suggested author action:** Either include mu_EI and mu_IR as free parameters with log-scale random walk perturbations, or run two to three alternative analyses with different fixed values (e.g., mu_EI = 0.2 and 0.33) and report how much the MLE and conclusions change.

---

## Minor Points

**ID: 22.19.m1**
**Concern:** Initial conditions E = 6000 and I = 15000 are hard-coded constants, not estimated parameters. Only the susceptible fraction eta is estimated.
**Why it matters:** Over a 121-day epidemic window beginning at the start of the Omicron wave, the initial exposed and infectious pool substantially influences the epidemic trajectory. Incorrect initialization can bias all subsequent parameter estimates.
**Severity:** Minor
**Suggested author action:** Either estimate E_0 and I_0 as free parameters (as initial value parameters with ivp()) or provide a sensitivity analysis showing results are stable under reasonable perturbations of these values.

**ID: 22.19.m2**
**Concern:** The biological interpretation that "the Omicron variant isn't as contagious as expected" (conclusion section) is based on the global search finding beta2 < beta1. Given the instability of beta2 documented above, this interpretation is not supported by the data.
**Why it matters:** Scientific conclusions drawn from non-identifiable parameters are unreliable and can mislead readers.
**Severity:** Minor
**Suggested author action:** Remove or qualify this claim pending resolution of the beta2 identifiability issue (see M3).

**ID: 22.19.m3**
**Concern:** The Shapiro-Wilk test is applied after the QQ plot already visually demonstrates non-normality of ARIMA residuals.
**Why it matters:** Redundant formal testing when visual evidence is conclusive adds length without analytical value.
**Severity:** Minor
**Suggested author action:** Remove the Shapiro-Wilk test or replace it with a brief statement noting the QQ plot departure is sufficient to conclude non-normality.

**ID: 22.19.m4**
**Concern:** The dominant spectrum frequency 0.011 (period ~90 days) is described as a "90-day cycle," but with only 121 data points this peak almost certainly reflects the single-wave epidemic trend rather than a genuine periodic phenomenon.
**Why it matters:** Misidentifying a trend as a cyclic period is a conceptual error that can mislead the spectral interpretation.
**Severity:** Minor
**Suggested author action:** Describe the 90-day peak as a low-frequency trend artifact and focus the periodicity discussion on the well-supported 7-day weekly cycle.

**ID: 22.19.m5**
**Concern:** All figures lack captions, making the manuscript difficult to navigate without closely following the code chunks.
**Severity:** Minor
**Suggested author action:** Add a brief descriptive caption to each figure.

**ID: 22.19.m6**
**Concern:** ARIMA(4,1,4) has near-canceling AR and MA inverse roots (noted by the authors), suggesting potential over-parameterization.
**Severity:** Minor
**Suggested author action:** Consider reporting AIC for a smaller model (e.g., ARIMA(2,1,2)) to confirm that the added parameters of ARIMA(4,1,4) are warranted.
