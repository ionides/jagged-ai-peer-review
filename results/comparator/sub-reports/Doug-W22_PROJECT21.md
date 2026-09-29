## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Tau parameter declared but never used in any model — ghost parameter with no effect on model dynamics")
- Human Issue #7: covered (matched by finding: "Vaccinated compartment initialization incorrectly scaled for Delta and Omicron models")
- Human Issue #8: covered (matched by finding: "ARMA benchmark not quantitatively comparable to POMP log-likelihoods — different observation models, data lengths, and series coverage")
- Human Issue #9: covered (matched by finding: "Convergence traces for local search not described or interpreted; no-decrease in parameter variance is evidence of non-convergence")

**Findings classification:**
- Major #1 (dmeas/rmeas SD mismatch): A — dmeasure uses SD = mean_cases while rmeasure uses SD = sqrt(mean_cases), a ~500x discrepancy at peak counts, invalidating all likelihoods and parameter estimates
- Major #2 (vaccinated compartment init scaled incorrectly): B — Delta model initializes V at ~900,000 instead of ~93 million; Omicron uses only the incremental vaccination rate change rather than the total stock (matches Human Issue #7)
- Major #3 (smoothed observations in measurement model): A — 7-day rolling average introduces autocorrelation that violates the conditional independence assumption of the factored POMP likelihood
- Major #4 (no profile likelihoods): A — no profile likelihoods or confidence intervals computed for any of the three models despite 7–9 free parameters and known collinearity risks
- Major #5 (no model diagnostics): A — no conditional log-likelihood plots, no ESS reported, no filtering distribution shown; alignment problems with Delta and Omicron acknowledged but undiagnosed
- Major #6 (ARMA benchmark not comparable to POMP): B — ARMA fit to full series under Gaussian model while POMP models fit to sub-series; no common metric computed (matches Human Issue #8)
- Major #7 (tau declared but never used): B — tau in paramnames and perturbed by rw.sd in IF2 but never appears in rprocess or measurement Csnippets; ghost parameter wasting computational degrees of freedom (matches Human Issue #6)
- Major #8 (accumulator H tracks recoveries not infections): A — H += dN_IR accumulates recoveries but observed data records new confirmed cases; rho absorbs the ratio, becoming biologically uninterpretable
- Minor (rw.sd very small for pre-Delta): C — local search perturbs Beta by ~0.015% per step on natural scale; effective exploration likely very limited
- Minor (only 10 replicates for pre-Delta global search): C — 10 replicates provides very sparse coverage of 7-dimensional parameter box; models 2 and 3 use 20
- Minor (convergence traces not interpreted): D — traces plotted but not interpreted; authors note loglik plots are sparse without diagnosing non-convergence (matches Human Issue #9)
- Minor (loglik.se < 8 threshold permissive): C — model 1 pairs plot retains entries with SE up to 8 log-likelihood units while models 2 and 3 use 5 and 0.5 respectively
- Minor (alpha/N vaccination rate dimensionally inconsistent): C — dN_SV uses rbinom(S, 1 - exp(-alpha/N * dt)) producing essentially zero vaccinations per step; alpha should not be divided by N
- Minor (Omicron R initialization may be negative): C — R computed as residual absorbing ~270 million individuals under extreme assumption that ~90% of US population already recovered by December 2021
- Minor (no quantitative goodness-of-fit summary): C — reported log-likelihoods not interpreted relative to any null or benchmark, and number of observations not stated
- Minor (ARMA fit ignores structural breaks): C — single ARMA(4,4) applied to series spanning three qualitatively different dynamic regimes violates stationarity assumption

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |
