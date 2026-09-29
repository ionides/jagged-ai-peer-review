## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Invalid direct comparison of ARIMA, GARCH, and POMP log-likelihoods — GARCH LLH from rugarch reports sum of log-densities of standardized residuals, not the marginal likelihood, making cross-family comparison invalid")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Invalid direct comparison of ARIMA, GARCH, and POMP log-likelihoods — paper claims Student-t GARCH is the best model via a comparison that also reveals t-GARCH outperforms POMP SV models")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (Invalid direct comparison of ARIMA, GARCH, and POMP log-likelihoods): B — cross-family LL comparison invalid; GARCH rugarch LLH is not the marginal likelihood; t-GARCH reported as best model via invalid scale (matches Human Issues #3 and #7)
- Finding 2 (Negative estimates of sigma and v0 in Heston model dismissed without justification): A — negative sigma and v0 are outside model domain; optimizer crossed feasible boundary with no parameter transformation
- Finding 3 (Profile likelihood uses single restart per grid point with single pfilter evaluation; no CI reported): A — Monte Carlo noise dominates profile near peak; no chi-squared threshold applied; identifiability/CI purpose of profiling unfulfilled
- Finding 4 (Regime sequence plot uses forward simulation, not filtering distribution): A — simulate() used instead of pfilter() filtering distribution; "Inferred Regime" label is scientifically incorrect
- Finding 5 (No benchmark comparison of mechanistic POMP models against non-mechanistic alternatives): A — GARCH does not constitute proper non-mechanistic benchmark for SV models; comparison confounds observation models and parameter counts
- Finding 6 (Regime-switching model p11 near 0.5 implies near-random switching): A — logit(p11)=0.09 gives p11≈0.522; low-volatility regime has no persistence; no identifiability diagnostic or CI for p11
- Finding 7 (Figure numbering inconsistent): C — at least two distinct figures labeled "Figure 3"
- Finding 8 (ARIMA model description inconsistency about mean specification): C — (2,0,2), (2,2), and (1,1) ARMA orders used inconsistently across sections
- Finding 9 (rw_sd for global search reuses local-search object without adjustment): C — perturbation SD of 0.005 too small for global box range of ~3 units; defeats purpose of broad initialization
- Finding 10 (ESS trajectories claimed monitored but not shown): C — no ESS plot or minimum ESS value reported despite claiming it as a distinguishing feature
- Finding 11 (Heston profile pfilter called on heston_model not modified pomp object): C — inconsistency between object used for optimization and object used for evaluation
- Finding 12 (No model diagnostics beyond trace plots and profile likelihood): C — no conditional log-likelihood plots, no ESS trajectories, no simulated-vs-observed comparison
- Finding 13 (Heston sigma and v0 not constrained to be positive; no parameter transformations): C — lack of partrans argument allows optimizer to explore infeasible domain for sigma and v0
- Finding 14 (Final MLE parameter vectors not archived): C — re-running mif2 required to reproduce results; Wheeler et al. minimum reproducibility requirement not met
- Finding 15 (ADF test interpretation: "rejecting the null of stationarity"): C — phrasing slightly imprecise; recommends also applying KPSS test for corroborating evidence

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |
