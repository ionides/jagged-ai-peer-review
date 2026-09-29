# Human Issues — W25 Project 16

1. Plotting, ACF, spectral analysis and ARMA are all best done on a log scale. Then, the log-ARMA likelihood needs to be computed with care (see the measles case study in Chapter 18).

2. The reporting rate is estimated to be close to one, and there is no depletion of susceptibles since cases are much less than N=48×10^6. This particular mechanistic model is not doing a good job. The real reporting rate for pertussis is probably very low, since mild or asymptomatic infections are common.

3. The implemented SEIR model has no overdispersion in the process model and no seasonality. There are various things to try to fix it up. The main contribution of the benchmark likelihoods is to remind us that the mechanistic model is not fully effective yet and needs more work.

4. Given the identified problems with the mechanistic model, it would be good to provide diagnostic plots (effective sample size, likelihood anomalies, etc). Without these, it is difficult to assess whether the POMP models failed due to misspecification, poor initialization, or numerical instability.

5. ARCH is quite an unintuitive model for epidemics; it makes sense when the conditional mean is always constant, i.e., when the integrated process is random variation around exponential growth.

6. For comparing SEIR with ARCH, likelihood is a better measure than relying on a few hold-out timepoints.

7. Section/equation/figure numbers would be helpful to the reader.

8. The report would benefit from a consolidated summary table showing model type, log-likelihood, parameter estimates, and perhaps notes on model stability or convergence.
