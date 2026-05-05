# Peer Review: W24 Project 09 — Volatility Analysis of NASDAQ 100

---

## Summary

This project fits ARIMA, GARCH, and POMP stochastic-volatility models to 53 years of NASDAQ Composite daily returns (1971–2024). The POMP component uses the Breto leverage model (6 parameters) and a simplified no-leverage model (4 parameters). The main conclusion is that the POMP model outperforms GARCH and ARIMA by log-likelihood, and that the leverage term is necessary.

---

## Weaknesses (Priority Order)

### 1. (Major) Profile likelihood construction uses wrong particle filter object

In the profile likelihood section, `L.prof` is evaluated with `pfilter(ndx.filt, params=coef(if.box[[i]]), Np=2000)` — indexing `if.box` instead of `if.prof`. This means the profile likelihood curve is computed using the parameters from the earlier global search runs, not from the profile-constrained mif2 runs. The profile likelihood therefore does not reflect maximization over the nuisance parameters at each fixed value of `sigma_eta`, which is the entire point of profile likelihood. The CI derived from this curve is unreliable.

**Evidence (Rmd lines 501–504):**
```r
L.prof <- foreach(i=1:100,.packages='pomp',.combine=rbind) %dopar% {
  logmeanexp(replicate(ndx_Nreps_eval, logLik(
    pfilter(ndx.filt,params=coef(if.box[[i]]),Np=2000))),se=TRUE)
}
```

### 2. (Major) Likelihood comparison across models is not valid — models differ in data, parameterization, and implementation

The authors compare log-likelihoods across four model families (ARIMA, GARCH via fGarch, GARCH via tseries, and POMP) as though they are directly comparable. However: (a) `fGarch` and `tseries::garch` produce different log-likelihoods for equivalent models with no explanation beyond a StackExchange post; (b) the ARIMA AIC table shows negative values (~-79000) consistent with a Gaussian log-likelihood on demeaned returns, while the GARCH log-likelihoods (~43000) and POMP log-likelihoods (~43000) are of opposite sign convention and different scope; (c) no formal likelihood ratio test or AIC-normalized comparison is performed. The statement that "POMP outperformed GARCH" based solely on these raw numbers is not supported by a rigorous comparison.

### 3. (Major) Periodogram is applied to demeaned returns rather than to squared returns or absolute returns (volatility proxy)

The project applies a spectral analysis (periodogram) to the demeaned returns directly. The purpose of the EDA section is to understand volatility clustering, for which the appropriate transformation is squared returns or absolute returns. The periodogram of raw returns is largely uninformative for this goal (as the authors themselves note: "no periodic behaviors"). This is a methodological mismatch between stated goals (volatility modeling) and EDA procedure.

### 4. (Major) ARIMA fitting is applied to the wrong target variable

The paper fits ARIMA models to the demeaned returns and uses this as a model for volatility. ARIMA on returns models the conditional mean, not the conditional variance. Heteroscedasticity in the residuals is expected and is not a finding that justifies moving to GARCH — it is simply evidence that ARIMA on returns is not a volatility model. The framing conflates modeling of returns with modeling of volatility throughout the ARIMA section.

### 5. (Major) No simulation-based model checking for the POMP model

There is no posterior predictive check or simulation overlay for the full Breto POMP model (the simplified no-leverage model shows one simulated path, but the primary Breto model does not). Without checking whether model-simulated data resemble the observed series in key features (variance clustering, tail behavior), it is impossible to assess model adequacy beyond likelihood value alone.

### 6. (Major) No formal likelihood ratio test between Breto model and no-leverage model

The two POMP models are nested (the no-leverage model is the Breto model with `sigma_nu = 0` and `G_0 = 0`). This nesting should be tested with a likelihood ratio test (or at minimum an AIC/BIC comparison accounting for the difference in parameter count). The text simply compares raw log-likelihoods (43485 vs. 43280) without noting that one model has 6 parameters and the other has 4, nor computing a p-value. Given the standard error on the estimates (~1.4 for Breto), the apparent difference of ~200 log-likelihood units is large, but the comparison is still incomplete without a formal test.

### 7. (Major) Global search box bounds for the no-leverage model are implausibly wide

For the no-leverage model, the global search box specifies `sigma_eta = c(0, 60)` and `mu_h = c(-16, 5)`. An upper bound of 60 for `sigma_eta` (noise on the log-volatility process) is far outside any physically reasonable range for daily equity returns, and will cause many failed particles during filtering. The prior on `mu_h` reaching +5 implies a mean log-volatility of exp(5/2) ≈ 12, which is nonsensical for daily returns expressed as fractions. These uninformed bounds likely explain why the global search summary shows a minimum logLik of 39559 — far below even the local search — indicating many degenerate runs.

### 8. (Minor) Inconsistency in the text about fGarch log-likelihood values

The text states "the log-likelihood value is about 43341" for ARMA(5,5)+GARCH(1,1), but the HTML output clearly shows the log-likelihood is 43360.37. Then the text says ARMA(4,4)+GARCH(1,1) gives "43361.47" but the output shows 43363.89. These discrepancies suggest the text was written from earlier runs and not updated after the final runs.

### 9. (Minor) The ACF is computed on demeaned returns rather than squared demeaned returns in the EDA

The ACF of demeaned returns is shown and interpreted as suggesting "multiple significant lags popped up after lag=7." For volatility modeling, the more informative diagnostic is the ACF of squared returns (or absolute returns), which captures volatility clustering. The ACF of raw demeaned returns primarily captures mean autocorrelation, which is not the modeling focus. This point is never addressed.

### 10. (Minor) Local search uses only a single starting point (`params_test`) with no randomization

Both the local search for the Breto model and the no-leverage model start all chains from a single fixed `params_test` vector. This means all `ndx_Nreps_local` chains start at the same point, which makes the "local search" essentially equivalent to running multiple identical chains. Randomization of starting points within a neighborhood should be used to assess sensitivity.

### 11. (Minor) The run_level for the no-leverage model is silently reduced to 2

The Breto model is run at `run_level = 3` (Np=2000, Nmif=500), but when the no-leverage model is introduced, `run_level` is reset to 2 (Np=100, Nmif=50) without explanation. This means the two models are compared on unequal computational effort, biasing the likelihood comparison against the no-leverage model.

**Evidence (Rmd lines 648–653):**
```r
run_level <- 2
ndx_Np <- switch(run_level, 50, 100, 1e3)
ndx_Nmif <- switch(run_level, 5, 50, 200)
```

### 12. (Minor) The initial particle filter test applies to `sim1.filt` (simulated data) rather than `ndx.filt` (real data)

In the section "Test the model and likelihood estimate," `pfilter` is applied to `sim1.filt`, which was created from a simulation of the model at `params_test`. The resulting log-likelihood (about -17965) reflects filtering simulated data, not the actual NASDAQ data. The text does not clarify this distinction and reports the value as if it were a baseline for the real data. This is misleading.

**Evidence (Rmd lines 337–341):** `pf1 <- foreach(...) %dopar% pfilter(sim1.filt, Np=ndx_Np)`

### 13. (Minor) Lack of convergence diagnostics for the profile likelihood run

The profile likelihood section reports no convergence diagnostics (trace plots or pair plots) for the `if.prof` runs. Given that the Breto model's global search already showed poor convergence in several parameters, it is important to verify that the profile runs have converged before drawing conclusions about the CI for `sigma_eta`.

### 14. (Minor) Definition of `sigma_w^2` in the no-leverage model is stated but never verified

The no-leverage model states `sigma_w^2 = sigma_eta^2 * (1 - phi^2)`. The R implementation uses `omega = rnorm(0, sigma_eta * sqrt(1 - phi*phi))` which is consistent with this definition. However, the paper does not verify that the stationary variance of the latent H process is `sigma_eta^2`, nor does it connect this parameterization to the Breto model's `sigma_eta` for interpretive comparison. The parameter `sigma_eta` has different effective meanings in the two models (since the Breto model's omega term additionally involves `tanh(G)` scaling).

### 15. (Minor) The conclusion mischaracterizes the profile likelihood result

The conclusion states "the profile likelihood validated that the parameters found in the global search." However, the profile likelihood was computed incorrectly (see Issue 1) and its CI estimate of 0.54 to 1.0 for `sigma_eta` is extremely wide and based on very sparse coverage of the parameter space (only about 4–5 points above the cutoff based on the filter output). Calling this "validation" overstates what was demonstrated.

---

## Files Consulted

- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project09/blinded.Rmd`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project09/blinded.md`
- `/Users/jin/Desktop/ai/week11/projects_Material/project/final_project_w24/project09/^IXIC_quote.csv`
