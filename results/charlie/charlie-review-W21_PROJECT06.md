# Peer Review: W21 Project 06
**"To The Moon or Not — Analysis on GameStop Stock Price"**

---

## Summary

This project applies ARMA, GARCH, and a stochastic leverage POMP model (following Breto 2014) to demeaned log-returns of GameStop (GME) stock over one year (April 2020–April 2021). The primary goal is to compare model fit via log-likelihood and AIC. The POMP model (stochastic volatility with random-walk leverage) is the methodological centerpiece, and the analysis follows the standard course template for stochastic volatility closely. While the project demonstrates familiarity with the `pomp` workflow and correctly uses `logmeanexp` for likelihood aggregation, several serious methodological and reporting weaknesses undermine confidence in the conclusions. The AIC comparison across ARMA, GARCH, and POMP models is treated as directly valid without accounting for different likelihood normalizations. Profile likelihoods are entirely absent, leaving parameter identifiability unassessed. The local search (run_level=3 settings) uses only 20 replicates with 2,000 particles, which may be insufficient for this highly non-Gaussian return series. Convergence is explicitly noted as incomplete for key parameters, yet no corrective action is taken before final conclusions are drawn.

---

## Major Issues

### 1. Direct AIC comparison across ARMA, GARCH, and POMP is invalid without justification (CC-Yes, Error 2.2 / Error 1.14)

The conclusion section directly compares AIC scores of ARMA(1,3) (AIC = -262.88), GARCH(1,1) (AIC = -400.89), GARCH(4,2) (AIC = -442.88), and the POMP model (AIC = -466.6) and selects the POMP model on this basis. The ARMA AIC is computed from a Gaussian ARMA likelihood evaluated on demeaned log-returns. The GARCH AIC is computed using `tseries:::logLik.garch`, which may use a non-standard normalization (see Error 2.9 in the weakness reference). The POMP AIC is computed from a particle-filter log-likelihood. These three likelihood functions are not guaranteed to use the same normalization convention for the same observed data. In particular, the `tseries::garch` package is known to report non-standard likelihood values (quiz Q12-02 explicitly tested this). The report states these quantities are being compared "with respect to the same data," but does not verify that all three likelihoods use the same constant terms. Without this verification, the AIC comparison is unreliable and the conclusion that POMP outperforms GARCH by AIC is unsupported. **Fix:** Verify the normalization conventions for each package and either harmonize them or clearly note the caveat.

### 2. Profile likelihoods are entirely absent (CC-Yes, Error 1.9; Wheeler et al. checklist item #5)

No profile likelihoods are computed for any of the six POMP model parameters (sigma_nu, mu_h, phi, sigma_eta, G_0, H_0). The project draws conclusions about model fit from point estimates and pairs plots but never assesses whether these estimates are identifiable or what their uncertainty is. The GME_params.csv data shows that sigma_nu values span from approximately 0.0001 to 0.68 across the global search runs (rows with logLik near 232 have sigma_nu ~ 0.68, while rows near 239 have sigma_nu ~ 0.001), suggesting the parameter is poorly identified. Without profile likelihoods, the CI for any parameter cannot be reported and it is unclear whether the point estimates are reliable. **Fix:** Compute profile likelihoods for at least the key parameters (phi, sigma_eta, mu_h) and report 95% CIs using the Wilks threshold.

### 3. Incomplete convergence acknowledged but not addressed before drawing conclusions

The report explicitly states: "for H_0 and sigma_nu, they seem not converge" (local search) and in the global search discussion: "phi and sigma_eta seems to converge to a certain range, but their converging rate seems to be slower." Despite acknowledging non-convergence in two or more parameters, the project proceeds directly to the conclusion section without attempting to resolve the issue. The "easy solution" of more iterations is mentioned but not implemented. This means the reported maximum log-likelihood of ~239.8 and associated parameter values may not be at the true MLE. When convergence diagnostics show non-convergence, the resulting parameter estimates and likelihood values are unreliable as stated conclusions. **Fix:** Re-run with increased Nmif (e.g., 300) or wider perturbation for the non-converging parameters, verify convergence, and then draw conclusions.

### 4. Global search starts from a single local search replicate (if1[[1]]), not the best one

The global search code reads:
```r
if.box <- foreach(i=1:GME_Nreps_global, .packages='pomp', .combine=c) %dopar%
  mif2(if1[[1]], params=apply(GME_box, 1, function(x) runif(1, x)))
```
The global search initializes all 100 replicates by continuing from `if1[[1]]` (the first local search replicate) with random parameters drawn from the box. This is a known course-template pattern, but the issue is that `if1[[1]]` is an arbitrary replicate — not necessarily the one with the best likelihood. The correct approach is to use any completed `mif2` object merely to inherit the model structure, not to use its parameter values (which are overwritten by `params=apply(GME_box,...)` anyway). While in this case the random params override the starting values, the mif2 internal state (perturbation schedule, cooling) is inherited from `if1[[1]]`. This may result in a non-standard cooling trajectory for some runs. The effect is minor but worth noting.

### 5. Insufficient particle count for a highly non-Gaussian return series (run_level=3 with Np=2,000)

The project uses `GME_Np = 2e3` (2,000 particles) at run_level=3. The standard course convention for run_level=3 is Np=5,000 (see 531-conventions.md). The GameStop return series has an extreme spike in January 2021 (returns of several hundred percent in a day), which produces highly non-Gaussian behavior. The stochastic volatility measurement model is `dmeasure = dnorm(y, 0, exp(H/2), give_log)`, which assigns near-zero density to extreme observations unless H is very large. This creates a particle degeneracy problem at the January 2021 spike. Using only 2,000 particles rather than the recommended 5,000 for run_level=3 increases the risk of particle collapse at exactly the time point that most challenges the model. The log-likelihood standard errors in the CSV (column 2) range from ~0.05 to 0.14, which are somewhat larger than typical for a well-behaved run with 5,000 particles. **Fix:** Re-run with Np=5,000 and verify that log-likelihood standard errors decrease, confirming numerical stability.

### 6. GARCH AIC comparison uses tseries::garch with potentially non-standard log-likelihood (CC-Yes, Error 2.9)

The GARCH log-likelihoods are extracted via `tseries:::logLik.garch`. The quiz Q12-02 explicitly warned students that `tseries::garch` reports non-standard log-likelihood values that may not be directly comparable to other packages. The GARCH(1,1) log-likelihood of 203.44 and GARCH(4,2) of 228.44 are treated as directly comparable to the POMP log-likelihood of 239.3 without any verification. If the tseries normalization omits a constant factor that the POMP particle filter includes, the apparent "improvement" of POMP over GARCH could be partially artifactual. **Fix:** Verify the normalization by comparing to rugarch or fGarch output for the same data, or explicitly note this caveat.

---

## Minor Issues

### 7. No non-mechanistic (ARMA/IID) benchmark comparison for the POMP model (Wheeler et al. checklist item #2; CC-Yes Error 1.6)

While the project does compare ARMA, GARCH, and POMP, the ARMA model is a baseline on the *mean* of returns, not a true volatility benchmark. The natural benchmark for a stochastic volatility POMP model is an IID or GARCH model on the same observational scale. The report partially addresses this with the GARCH comparison, but the GARCH comparison is contaminated by the normalization issue described in issue #6. A clean likelihood comparison against a properly normalized IID negative binomial or Gaussian benchmark on the log-returns would provide a more reliable baseline.

### 8. The ARMA model selection criterion (AIC table) contains no discussion of numerical stability

The AIC table for ARMA(p,q) shows ARMA(1,3) with AIC -260.88, but ARMA(4,5) and other high-order models with AIC values not far below this. There is no check for whether the ARMA likelihood optimizer converged for the higher-order models, and no use of multiple starting points. For an AIC comparison involving models within 2 units of each other, numerical optimization failure is a genuine concern (MT1 Q3-01 / Q3-03). The conclusion that ARMA(1,3) is the best model is not fully supported without convergence checks.

### 9. Simulation-based model diagnostics are absent (Wheeler et al. checklist item #4)

Beyond the convergence trace plots (`plot(if1)` and `plot(if.box)`), no simulation-based diagnostics are shown. The project does not compare simulated trajectories from the fitted POMP model to the observed data (beyond a single simulation from the initial test parameters, which visually deviates substantially). Conditional log-likelihood plots per observation would reveal whether the model's poor fit at the January 2021 spike is addressed by the final parameter estimates.

### 10. The initial test simulation does not match the data and this discrepancy is insufficiently explained

The text states: "the simulated data deviates from the volatility of the observed data, especially for the earlier times, where the simulated data have extremely high volatility but the observed data seem to have low volatility." This is noted and attributed to "arbitrary parameters," but no post-fitting simulation is shown to demonstrate that the fitted model does better. The reader cannot assess whether the final POMP model actually captures the GME volatility dynamics, including the January 2021 spike.

### 11. ARMA(1,3) residual ACF shows significant correlation at several lags, but this is inadequately addressed

The text acknowledges significant residual autocorrelation in the ARMA(1,3) residuals and mentions that "seasonality might improve the fit." However, stock returns do not typically have seasonal patterns, and the residual autocorrelation is more likely attributable to volatility clustering (GARCH effects) — which is exactly what the GARCH model addresses. The explanation is therefore misleading and should be corrected.

### 12. Pairs plots are shown but not interpreted

Two pairs plots are produced (after local search and global search), but neither is interpreted in the text. The pairs plots reveal that the sigma_nu estimates cluster near zero for the high-likelihood runs, and a subset of global search runs have very different (mu_h ~ 0, sigma_eta ~ 5-20) parameter values with lower log-likelihoods (around 232-233). This multi-modality in the likelihood surface is visible in the GME_params.csv data and is scientifically important — it suggests two qualitatively different model regimes — but is not discussed.

### 13. AIC for the POMP model is computed using only the median log-likelihood, introducing bias

The report states "the POMP model gives median loglikelihood of 239.30." AIC requires the *maximum* log-likelihood, not the median. The maximum from the global search (reading from GME_params.csv) appears to be approximately 239.82. Using the median rather than the maximum underestimates the POMP model's AIC performance. This is a minor inaccuracy in reporting.

### 14. The rproc code correctly uses tanh(G) for leverage but this is not explained

The leverage term `tanh(G)` implements R_n = tanh(G_n), which is the fixed-leverage model when sigma_nu = 0. The text describes R_n = (e^{2Gn}-1)/(e^{2Gn}+1), which is mathematically equivalent to tanh(G_n). However, the report never explains why tanh is used in the code in place of the formula shown in the text. A reader unfamiliar with the identity might suspect a coding error. This is a minor presentation issue.

### 15. Minor: the ARMA(1,3) equation contains a typographical error

The fitted ARMA(1,3) model is written as: `R_n = -0.55 R_{n-1} + 0.61 epsilon_n + 0.21 epsilon_{n-1} + 0.42 epsilon_{n-2} + 0.016`. This is labeled ARMA(1,3) (p=1, q=3) but the MA component shows only 3 epsilon terms including the contemporaneous one (epsilon_n, epsilon_{n-1}, epsilon_{n-2}), which corresponds to q=2, not q=3. An ARMA(1,3) model should have epsilon_n through epsilon_{n-3}. Either the model selection table gives a different order than what was fitted, or the equation is incorrectly transcribed. The arima() call uses `order=c(1,0,3)`, confirming q=3, so the written equation is missing the epsilon_{n-3} term.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/Skills/guided-pomp-review/SKILL_pomp.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-conventions.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/531-weakness-reference.md`
- `/Users/jin/Desktop/ai/week11/Skills/531_references/README.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project06/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_W21/project06/GME_params.csv`
