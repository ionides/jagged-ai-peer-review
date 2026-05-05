# Peer Review: Statistical Models for Solar Flare X-ray Flux Time Series
**Semester:** W21 | **Project:** 08

---

## Summary

This project investigates the 2019 NOAA GOES X-ray flux time series using a progression of models: baseline ARMA and GARCH, then two-state hidden Markov models (Gaussian and Student-t emission distributions), a Gaussian HMM with an AR(1) component, and finally a discretized Heston stochastic-volatility model. The stated goal is interpretable modeling of the flare dynamics rather than black-box prediction. The project is ambitious in scope and the models are implemented in pomp. Several critical methodological and reporting issues limit its scientific credibility.

---

## Weaknesses (Major to Minor)

### 1. Log-Likelihood Values Are Not Comparable Across Models (MAJOR)

The project's central conclusion is that the Heston model achieves the best log-likelihood (-21.66), followed by the Student-t HMM (-63.44), Gaussian HMM AR(1) (-78.36), and Gaussian HMM (-106.76). These numbers are presented in a summary table and used to rank the models. However, the models are not observationally equivalent: the Gaussian HMM AR(1) and the Heston model both use covariate-based filtering where the hidden state is forced to equal the observed data at each step (`Y_state = covaryt`). This means those models evaluate the likelihood on a different probability space than the direct-emission HMMs, and the raw log-likelihood numbers cannot be meaningfully compared. The Heston model's superiority may be entirely a consequence of the way the likelihood is computed, not of better fit.

### 2. t-HMM rprocess Uses `euler()` Instead of `discrete_time()` (MAJOR)

For the t-distribution HMM (`thmm2`), the rprocess is specified with `euler(thmm2_step, delta.t=1/12)` (line 641), while the Gaussian HMM and all other HMMs use `discrete_time(..., delta.t=1)`. Because the data are already on a 12-hour (half-day) scale, applying Euler steps at `delta.t=1/12` of whatever the time unit is introduces an internal mismatch. If the natural time unit is "half-day," each observation interval contains 12 sub-steps, meaning the hidden state X transitions up to 12 times per observation, which is inconsistent with the intended one-transition-per-observation HMM design. The Gaussian and t models are thus not structurally equivalent, making the likelihood comparison at -106.76 vs. -63.44 partly attributable to this inconsistency rather than the choice of emission distribution.

### 3. Gaussian HMM AR(1): Measurement Equation Is Trivial and Model Is Not a Proper POMP (MAJOR)

In Section 7, `ghmmar_rmeas` simply returns `y = Y_state`, and `Y_state` is set to `covaryt` (the observed data) in the filter snippet. This means the "measurement model" is a deterministic mapping of the hidden state to the observation, so the particle filter is computing a degenerate likelihood. The authors acknowledge that the likelihood "goes up then down" during MIF2 iterations and attribute this to possible model misspecification, but do not identify the root cause as the improper use of the covariate trick combined with a Dirac-delta measurement distribution. Consequently, the "best likelihood" of -78.36 for this model cannot be trusted, and using a "last iteration estimator" is ad hoc and statistically unjustified.

### 4. Heston Model Euler Discretization Incorrectly Applies to Log-Variance (MAJOR)

The project states (Section 8) that the Heston model is discretized with Z representing the log-variance (i.e., the state variable is Z = log V). However, the update equation written in the report is:

    V_n = V_{n-1} + kappa*(sigma_bar * exp(-V_{n-1}) - 1) - 0.5*sigma^2 + ...

and the code computes `Z` using a formula that mixes the log-variance SDE with untransformed terms. This does not correspond to a standard Euler-Maruyama discretization of either the Heston V SDE or the log(V) SDE, and the report's own written equations (where S_n = exp(Y_n) and V_n appears in a Cox-Ingersoll-Ross form) are inconsistent with the code. The project acknowledges borrowing this from a 2020 project without verifying correctness for the solar flare setting. The estimated `rho = 0.9993` (essentially 1.0) is a boundary hit that typically signals a misspecified or unidentifiable model.

### 5. No Formal Profile Likelihood Confidence Intervals (MAJOR)

The project explicitly acknowledges constructing only "poor man's profile CIs" by reusing search points, rather than proper profile likelihood traces. For the Gaussian HMM, the profile plots for `mu0` and `mu1` are shown, but the cutoff lines and the loess smoothers appear to have too few points to make the CIs reliable. No profile CI is provided for the t-HMM or the Heston model at all. Given that the primary scientific claims (distinct mu0, mu1 corresponding to two flare regimes; Heston best fit) rest on parameter estimates, the absence of proper uncertainty quantification is a significant weakness.

### 6. Pairs Plot Contains a Typo That Silently Drops a Parameter (MODERATE)

In the Gaussian HMM local search section, the pairs plot call reads:

    pairs(~loglik + mu0 + mu1 + sigma0 + sigma1 + p0 + 01, data=results, pch=16)

The variable `01` is the numeric literal 1 (zero-one), not the parameter `p1`. The pairs plot therefore omits `p1` and includes a degenerate constant column. This is a code bug that went unnoticed, suggesting that the diagnostics were not carefully checked.

### 7. Global Search for Gaussian HMM Uses Very Low Particle Count (MODERATE)

The global search for the Gaussian HMM uses `Np=200` particles for the evaluation step (line 411), while all other models use Np of 1,000-20,000. With only 200 particles and n=718 observations, the particle filter log-likelihood estimates will have very high variance, likely causing the optimization to converge to spurious local maxima. The best reported Gaussian HMM log-likelihood (-106.76) is therefore poorly resolved. The local search uses Np=200 and Nmif=50, which is also likely insufficient.

### 8. AIC Computation for the ARMA(1,3)+GARCH(1,1) Baseline Is Wrong (MODERATE)

In the baseline table, the AIC for ARMA(1,3)+GARCH(1,1) is computed as `2 * bench_fit@fit$value + 2 * 6` (line 183). The value stored in `bench_fit@fit$value` is the negative log-likelihood (the optimizer minimizes), so the AIC formula is correct only if the sign is already handled by `@fit$value`. However, for the log-likelihood, the code uses `-bench_fit@fit$value`. This inconsistency means the AIC in the table is correctly computed as positive AIC, but it is easy to confuse. More problematically, the parameter count for ARMA(1,3)+GARCH(1,1) is listed as 6, when `fGarch::garchFit` for ARMA(1,3)+GARCH(1,1) actually estimates 1 (AR) + 3 (MA) + 3 (GARCH: alpha0, alpha1, beta1) + 1 (mean) = 8 parameters, so the AIC is underpenalized.

### 9. Data Aggregation Choice (97.5th Percentile Over 12 Hours) Is Not Justified (MODERATE)

The preprocessing reduces the 1-minute GOES data to 718 half-day 97.5th-percentile values. The choice of 97.5th percentile rather than, e.g., the maximum or mean is described as "robust against outlier noises" but no sensitivity analysis is presented. The 12-hour aggregation interval is also ad hoc. Since the aggregation method determines the observed data distribution, the emission model choice (Gaussian vs. Student-t) is directly affected. The project does not discuss how the aggregation may induce the heavy-tailed marginal that motivates the t-HMM.

### 10. HMM Transition Probabilities Are Confusingly Named (MODERATE)

The two-state HMMs use parameters `p0` and `p1`, but in the `hmm_step` Csnippet, when `X == 0`, the next state is drawn as `rbinom(1, p0)`, meaning `p0` is Pr(X_{n+1} = 1 | X_n = 0), i.e., the off-diagonal transition probability. The report, however, describes the MLE values "p0=0.0968, p1=0.910" as if they were self-transition (persistence) probabilities ("9/10 times flares will retain its current strong/weak property"). The interpretation is reversed: `p1 = 0.91` is the probability of transitioning FROM state 1 (strong flare) to state 1, which is retention, but `p0 = 0.097` is the probability of transitioning FROM state 0 to state 1, i.e., weakening to strong - or the reverse, depending on how states 0/1 are labeled. The prose interpretation is unclear and potentially incorrect.

### 11. Student-t HMM dmeasure Contains a Bug for the Non-Log Case (MODERATE)

In `thmm2_dmeas`, the branch for `give_log = FALSE` computes:

    lik = (1.0 / s0) * dt((y - mu0) / s0, nu0, give_log);

Here `give_log` is `FALSE` (= 0 in C), so `dt(..., 0)` returns the density on the natural scale, and multiplying by `1/s0` is correct. However, the branch for `give_log = TRUE` computes:

    lik = -log(s0) + dt((y - mu0) / s0, nu0, give_log);

In C, `give_log` is an integer, so passing it directly to `dt()` as the log flag is correct only if pomp guarantees it is 0 or 1. More critically, in the log case the Jacobian adjustment should be `-log(s0)` (which is what is written), but the density returned by `dt(..., TRUE)` is the log-density of the standardized variable. Adding `-log(s0)` to `dt(..., TRUE)` is correct only when `dt` returns a true log-density. This is correct by R convention but the unusual coding pattern (mixing integer `give_log` as an argument and then using it in arithmetic) merits careful scrutiny and documentation.

### 12. Heston Global Search Box Contains a Non-Existent Parameter (MINOR)

The global search box for the Heston model (lines 1570-1580) includes a row for `sigma_nu = c(0.005, 0.05)`, which is not in `heston_paramnames`. This row is silently ignored by `mif2` but the `heston_params.csv` output file indeed contains a `sigma_nu` column (confirmed in the data file), meaning that results were written from a differently configured run. This suggests the saved CSV files may not correspond exactly to the code shown.

### 13. Simulation Comparison Shown for Only 1-3 Simulations (MINOR)

For most MLE evaluations (e.g., Student-t HMM and Heston model), only 1 simulation is shown alongside the data. Visual simulation-based model checking is a central diagnostic for POMP models, and with only one trajectory it is impossible to assess whether the data lies within the model's predictive envelope. The Gaussian HMM shows 11 simulations but later models reduce this, making the diagnostic less informative precisely for the models claimed to perform best.

### 14. No Residual Diagnostics or Goodness-of-Fit Tests Beyond Visual Inspection (MINOR)

The project relies entirely on log-likelihood ranking and visual overlay of a small number of simulated trajectories to evaluate model adequacy. Standard diagnostics such as PIT (probability integral transform) histograms, ACF of standardized residuals, or effective sample size (ESS) plots over time are mentioned in passing (the ESS is briefly shown for two models) but not systematically discussed. For a project claiming to provide interpretable statistical models, the lack of residual analysis is a notable gap.

### 15. Reference Numbering Error in Bibliography (MINOR)

In the references section, entries [4] are duplicated: "[4] Vlad Landa et al..." and "[4] Sunspots and Solar Flares..." appear with the same number. Subsequent reference numbers [5]-[14] are therefore off by one relative to any in-text citation.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project08/blinded.rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project08/hmm_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project08/thmm2_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project08/arghmm2_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project08/heston_params.csv`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w21/project08/xrayts.csv`
