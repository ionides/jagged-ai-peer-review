## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "title spelling error and writeup extremely terse, project submitted in incomplete state")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "title spelling error and writeup extremely terse, project submitted in incomplete state")
- Human Issue #7: missed

**Findings classification:**
- Finding 1: A — POMP process model never updates latent state S; model uses observed data as covariate
- Finding 2: A — dmeas uses rbinom (random draw) instead of a deterministic conditional density, making particle filter invalid
- Finding 3: A — no IF2 convergence diagnostics (no trace plots, no likelihood profile, no pairs plot)
- Finding 4: A — global search references undefined object `fixed_params`, making the global search unrunnable
- Finding 5: A — AIC comparison between ARIMA and POMP log-likelihoods is invalid because models are fitted on different scales
- Finding 6: A — log(diff(Subscribers)) transformation is undefined for negative differences, which occur in the data
- Finding 7: A — ARIMA(1,1,2) model order inconsistent with pre-differenced series (effectively double-differencing)
- Finding 8: A — no POMP model diagnostics (no ESS over time, no filter mean trajectories, no particle degeneracy check)
- Finding 9: A — compartmental model structure not formally defined, no diagram, no justification, parameter N unexplained
- Finding 10: A — R-squared reported for ARIMA is not a standard or meaningful diagnostic for ARIMA models
- Finding 11: C — residual ACF plot y-axis range is misleading and no formal test (e.g., Ljung-Box) supports the white-noise claim
- Finding 12: C — data reversal from twitch.csv to twitch2.csv is undocumented, raising reproducibility questions
- Finding 13: C — estimated parameter values from the final POMP fit are never reported
- Finding 14: D — title spelling error and writeup extremely terse; project submitted in incomplete state (matches Human Issues #1 and #6)
- Finding 15: C — spectral analysis uses unlabeled variable "x"; smoothed spectral estimate not provided

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 10 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |
