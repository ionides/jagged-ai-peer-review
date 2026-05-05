# Peer Review: W24 Project 15 — Analysis of MERS-CoV in Saudi Arabia

## Summary

This project analyzes weekly MERS-CoV case counts in Saudi Arabia (January 2014 – May 2016) using both an ARMA benchmark and a mechanistic SEIRS POMP model applied to the camel population. The modeling motivation is sound and is grounded in the peer-reviewed Lin et al. (2018) paper. Several components are executed competently (particle filtering, local and global MIF2 searches, a profile likelihood), but there are significant methodological and implementation flaws that undermine the conclusions.

---

## Weaknesses

### 1. (Major) Measurement Model Inconsistency: dmeasure Does Not Match rmeasure

The density function (`seirs_dmeas`) evaluates the likelihood of `reports` given `rho*C`, but `seirs_rmeas` generates `reports = total_to_primary * rnbinom_mu(k, rho*C)` — multiplying the draw by 4. The `dmeas` snippet does not account for this factor-of-4 scaling. Concretely, `dnbinom_mu(reports, k, rho*C, give_log)` uses the un-scaled mean, while observations are generated from `4 * NegBin(k, rho*C)`. This mismatch means the particle filter is evaluating the wrong density, producing incorrect likelihood estimates and biasing all parameter estimates from MIF2.

### 2. (Major) Process Model Error: `C` Accumulates `dN_IR` Instead of Primary Spillover

The accumulator variable `C` is incremented as `C += dN_IR * rho_CH` (line 408), meaning it counts a fraction of camel recoveries — not camel-to-human spillover events. The biological interpretation is that primary human cases arise from contact with *infectious* camels, so the accumulation should be proportional to the force of infection on humans from camels (proportional to `I`), not the number of camels recovering in the interval. This is a fundamental error in translating the Lin et al. model to code; the model description says $Z_i = \int \rho_{CH} \mu_{IR} I \, dt$, which corresponds to `dN_IR * rho_CH`, but this conflates the recovery hazard with the spillover hazard and the integration is not properly carried out.

### 3. (Major) Likelihood Ratio Test Between Non-Nested Models Is Invalid

The project uses a Wilks-theorem-based chi-squared LRT to compare the ARMA(1,4) model (log-likelihood −422.77) to the SEIRS model (log-likelihood −378.33), computing a p-value via `pchisq`. The ARMA and SEIRS models are not nested — an ARMA model on count data is not a special case of the SEIRS model — so the Wilks approximation does not apply and the resulting p-value is meaningless. Even setting this aside, the likelihoods are computed on different scales/representations (Gaussian ARMA vs. negative binomial SEIRS), making direct comparison via LRT formally inappropriate without further justification.

### 4. (Major) Profile Likelihood Is Truncated at Its Maximum

The authors acknowledge that "the $\rho_{CH}$ with the largest log-likelihood is on the edge of the interval (0.001)." This means the profile was not constructed over a range wide enough to contain the maximum. A profile likelihood used for confidence interval construction must contain the maximum in its interior; when it is on the boundary, the resulting CI (which the authors report as "approximately 0.001") is not a valid 95% CI. The authors note this issue but do not fix it.

### 5. (Major) Global Search Uses Only One Additional MIF2 Run (Nmif=50) Without Cooling Restart

In the global search, each starting guess is filtered through `mif2(params=c(unlist(guess), fixed_params))` followed by `mif2(Nmif=50)`, with no explicit `cooling.fraction.50` setting for the second run and no third MIF2 pass to stabilize estimates. In contrast, the profile likelihood correctly does three passes including explicit cooling (`cooling.fraction.50=0.3`). The global search results may therefore be less reliable because the optimizer has not fully converged before likelihood evaluation.

### 6. (Major) Weak Identifiability of Initial Condition Parameters Is Dismissed

The authors observe that $\eta$ and $\eta_2$ do not converge during local search and attribute this to "weak identifiability," but then state "as the likelihood seems to be maximized correctly, this should not be too problematic." Non-convergence of initial condition parameters is a substantive issue in epidemiological POMP models: when initial states are poorly identified, all downstream inferences about transmission parameters and $R_0$ are unreliable. No further investigation (e.g., fixing initial conditions, shrinking search ranges, or adding biological constraints) is performed.

### 7. (Major) No Profile Likelihood or Confidence Intervals for Key Parameters ($\beta$, $R_0$, $\mu_{RS}$)

Only $\rho_{CH}$ is profiled. The most epidemiologically important parameters — the transmission rate $\beta$, the recovery rate $\mu_{IR}$, and consequently $R_0 = \beta/\mu_{IR}$ — receive no uncertainty quantification. The $R_0$ estimate of 2.6 is reported as a point estimate without any confidence interval. Given parameter non-identifiability concerns already flagged by the authors, this is a major gap.

### 8. (Moderate) `mu_RS` Is Not Included in the Random Walk for the Profile Likelihood

In the profile likelihood search, the `rw.sd` specification includes `Beta`, `eta`, `eta2`, `mu_EI`, `mu_IR`, and `k`, but not `mu_RS`. Yet in the local search, `mu_RS` is included and the authors note it "continues to increase." Omitting `mu_RS` from the profile's random walk means the optimizer cannot re-optimize over `mu_RS` while profiling `rho_CH`, potentially producing a biased profile.

### 9. (Moderate) ARMA Applied to Count Data Without Addressing Non-Negativity

The ARMA model is fitted to weekly case counts (a non-negative integer process) using a Gaussian ARMA, which can generate negative predicted values. The residual histogram shows non-Gaussian features and the residual plot shows heteroscedasticity, both of which the authors note but do not resolve. A log transformation or a model appropriate for count data (e.g., ARIMA with Poisson/negative binomial errors) would be more appropriate. The ARMA model's validity as a benchmark for the SEIRS model is weakened when it violates basic assumptions.

### 10. (Moderate) `dN_Nmu = rbinom(N, 1 - exp(-mu*dt))` Draws From Total Population $N$ Instead of From Complement

New susceptible births are modeled as `dN_Nmu = rbinom(N, 1-exp(-mu*dt))` where `N` is the total population (a fixed constant, 270,000). This draws the number of births from all 270,000 camels uniformly, which is not how a demographic birth-death process is properly coded in a POMP Euler step. Typically births enter S at the same rate as total deaths leave the compartments, but drawing from `N` (a parameter, not a state variable) means the death process and birth process are independent draws that may create conservation violations beyond the `fmax` safeguards.

### 11. (Moderate) `fmin` Used to Prevent Negative States May Introduce Bias

Lines 404–407 use `fmin(S, dN_SE + dN_Smu)` to prevent states from going negative. While preventing negative values is necessary, truncating draws with `fmin` creates a biased process because the binomial draws are effectively clipped after the fact, making the realized transition rates smaller than specified. A proper implementation would ensure the draws are bounded before use (e.g., by constructing multi-nomial transitions or using a single compound draw). The authors credit office hours for this approach, but the statistical consequences are not discussed.

### 12. (Moderate) Parameter Count in LRT Is Incorrect (SEIRS Has More Than 8 Free Parameters)

The LRT uses $D_1 = 8$ parameters for the SEIRS model. Inspecting the code: the estimated parameters are $\beta, \eta, \eta_2, \mu_{EI}, \mu_{IR}, \mu_{RS}, \rho_{CH}, k$ (8), while $N$, $\rho$, and $\mu$ are fixed. However, the initial conditions (`S0`, `E0`, `I0` as determined by $\eta$ and $\eta_2$) should arguably be counted separately, and the measurement model's multiplicative factor of 4 is hard-coded without being estimated. The reported count of 8 appears correct for estimated parameters, but the comparison with ARMA's 5 parameters ($\phi_1, \psi_{1:4}, \mu$) omits the intercept/mean parameter from ARMA, which should make it 7 not 5. This affects the degrees of freedom in the LRT.

### 13. (Minor) Model Diagram Reference to `model.png` Is Missing From the Submitted Files

The Rmd references `![SEIRS Model Structure](model.png)` but `model.png` is not present in the project folder. The image therefore does not render, and readers cannot see the model flow diagram.

### 14. (Minor) Spectral Analysis Period Is Dismissed Without Adequate Justification

The smoothed periodogram identifies a dominant period of approximately 7 months. The authors dismiss this as not matching "any particular length of period" and finding "no evidence in the literature" for it, but the MERS seasonal pattern in Saudi Arabia is known to be associated with camel breeding season (roughly spring), which is roughly annual with a possible sub-annual component. Dismissing the spectral finding without examining whether it could reflect a biological process reduces rigor.

### 15. (Minor) No Seed Set Before Global Search Starting Point Generation, Only Before Profile

A seed is set before `runif_design` for the global search (`set.seed(2062379496)`), but the global `bake()` call uses `dependson=guesses`. The local search uses `registerDoRNG(987654321)` correctly. This is acceptable, but the replicated particle filter block (lines 499–518, `eval=F`) sets `set.seed(123456789)` outside `foreach` without `registerDoRNG`, which would not guarantee reproducibility in a parallel context. Since this chunk is `eval=F` it does not affect results, but it is a reproducibility concern if that code were run.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project15/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W24/project15/weekly_clean.csv`
