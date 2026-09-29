## Doug

**Coverage record:**
- Human Issue #1: covered (matched by finding: "Model title mismatch: paper claims SEIR but EDA implements SIR — creates confusion about what the EDA is actually demonstrating")
- Human Issue #2: covered (matched by finding: "EDA SIR models use identical hard-coded parameters regardless of region")
- Human Issue #3: covered (matched by finding: "EDA SIR models use unestimated, ad hoc parameters — presence as EDA is misleading")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Reproducibility failures — primary dataset 2.csv not included, code cannot be verified")
- Human Issue #8: covered (matched by finding: "Ad hoc calibration via SSE/single simulation instead of likelihood-based inference")
- Human Issue #9: covered (matched by finding: "No quantitative goodness-of-fit metrics — 'both models performed commendably' claim is unsupported")
- Human Issue #10: missed
- Human Issue #11: covered (matched by findings: "Ad hoc calibration instead of likelihood-based inference"; "Final model parameters chosen by manual inspection, not systematic optimization"; "Stochastic optimization cost function — nsim=1 SSE is unreliable and non-deterministic")

**Findings classification:**
- Finding 1 (Ad hoc calibration instead of likelihood-based inference): B — SSE/single-simulation fitting instead of particle-filter MLE (matches Human Issues #8 and #11)
- Finding 2 (No quantitative goodness-of-fit metrics for SEIR): B — "commendably" claim unsupported without log-likelihood or AIC (matches Human Issue #9)
- Finding 3 (Critical measurement model mis-specification — dnbinom/rbinom mismatch): A — dmeasure/rmeasure distributional inconsistency not raised by human
- Finding 4 (Comparison between ARIMA and SEIR not on a common metric): A — no shared evaluation framework; human did not raise this specific claim
- Finding 5 (No parameter identifiability assessment or uncertainty quantification): A — profile likelihoods and confidence intervals absent; not raised by human
- Finding 6 (Convergence evidence absent, optimization approach unreliable): A — single Nelder-Mead run, no convergence traces; not raised by human
- Finding 7 (Final model parameters chosen by manual inspection, not optimization): B — eyeball-fitted parameters not statistically principled (matches Human Issue #11)
- Finding 8 (Data preprocessing introduces double-differencing, nonsensical values): A — SEIR fitted to first difference of weekly counts; not raised by human
- Finding 9 (EDA SIR models use unestimated, ad hoc parameters): B — identical hard-coded parameters for all three regions, no fitting performed (matches Human Issues #2 and #3)
- Finding 10 (Model title mismatch — SEIR claimed but EDA implements SIR): B — confusion about what EDA demonstrates (matches Human Issue #1)
- Finding 11 (No model diagnostics — no ESS, no pfilter diagnostics): A — absence of particle filter diagnostics; not raised by human
- Finding 12 (Stochastic optimization cost function unreliable): B — nsim=1 SSE objective is non-deterministic; single simulation plugged into least squares (matches Human Issue #11)
- Finding 13 (ARIMA model selection inconsistency — ARIMA(2,1,3) selected but ARIMA(3,1,1) diagnosed): A — model-order mismatch between selection and diagnostics; not raised by human
- Finding 14 (Population parameter N treated as free optimization variable): A — biologically implausible N values not discussed; not raised by human
- Finding 15 (Reproducibility and code quality issues): B — primary dataset missing, code cannot be run from scratch (matches Human Issue #7)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 7 |
| C (AI minor, human missed) | 0 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |
