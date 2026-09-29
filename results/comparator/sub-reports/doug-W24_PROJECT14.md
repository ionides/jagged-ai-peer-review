## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "ARIMA fitted to unlogged counts, log transform preferable given wide dynamic range")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "force-of-infection equation inconsistent between text and Csnippet"; also matched by finding: "discrete stochastic transition equations inconsistent with stated ODE system")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "no assessment of initial condition sensitivity, values not discussed for plausibility")
- Human Issue #11: covered (matched by finding: "no global parameter search performed"; also matched by finding: "no profile likelihoods or confidence intervals for any parameter")
- Human Issue #12: covered (matched by finding: "hard-coded absolute path to external image file — diagram will not render for any reader")

**Findings classification:**
- Finding 1 (accumulator tracks recoveries not new infections): A — semantic mismatch between H accumulator and reported TB incidence counts
- Finding 2 (no global parameter search): B — no global search performed, estimates unreliable (matches Human Issue #11)
- Finding 3 (no benchmark comparison): A — POMP model never compared quantitatively to ARIMA or other baseline
- Finding 4 (no profile likelihoods or CIs): B — no uncertainty quantification for any of 13 parameters (matches Human Issue #11)
- Finding 5 (force-of-infection inconsistent between text and Csnippet): B — narrative uses mu_IR label for foi, Csnippet defines foi differently (matches Human Issue #5)
- Finding 6 (fixed population N ignores demographic change): A — N fixed at 333M for 1953–2020, inflating transmission rate estimates
- Finding 7 (measurement model Rate vs Number mismatch across code blocks): A — intermediate R-function uses Rate, final Csnippet uses Number; different measurement models
- Finding 8 (discrete stochastic equations inconsistent with stated ODE): B — written difference equations omit time-varying Beta_t term present in Csnippet (matches Human Issue #5)
- Finding 9 (single mif2 convergence trace without discussion): C — biologically implausible mu_EI and mu_RS values not flagged
- Finding 10 (ARIMA caption says incidence rate, model fitted to counts; log scale issue): D — log transform preferable given wide dynamic range of counts (matches Human Issue #2)
- Finding 11 (hard-coded absolute path to external image): D — diagram will not render for any reader other than author (matches Human Issue #12)
- Finding 12 (ARIMA model selection on AIC alone, simulation_times=0, root near unit circle): C — adequacy checks computed but not discussed, smallest root 1.05
- Finding 13 (no goodness-of-fit beyond single log-likelihood value): C — -628.8447 reported with no context, no comparison to saturated model or AIC
- Finding 14 (ESS not monitored during particle filtering): C — particle degeneracy not assessed with Np=2000 and 13 parameters
- Finding 15 (no assessment of initial condition sensitivity): D — initial proportions estimated but plausibility not discussed (matches Human Issue #10)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |
