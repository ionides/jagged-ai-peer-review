## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "No process noise (environmental stochasticity) in transmission")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "No profile likelihoods or confidence intervals — parameter identifiability entirely unassessed")
- Human Issue #5: missed

**Findings classification:**
- Finding 1 (H accumulator tracks recoveries not cases): A — accumulator H sums dN_IR+dN_AR (recoveries) but is used as expected case count in measurement model
- Finding 2 (dmeasure subtracts deaths inconsistently): A — cases-deaths compared to rho*H (recoveries) has no mechanistic justification
- Finding 3 (rho > 1 allowed in global search box): A — search box sets rho in c(0,2) making infeasible starting values for a reporting rate
- Finding 4 (No profile likelihoods or CIs): B — parameter identifiability entirely unassessed; pairs plot insufficient substitute (matches Human Issue #4)
- Finding 5 (No non-mechanistic benchmark): A — POMP not compared against IID negative binomial or equivalent baseline
- Finding 6 (ARIMA/POMP likelihood comparison invalid): A — likelihoods evaluated on different data series and observation models, not directly comparable
- Finding 7 (Placeholder text in intervention periods): A — "x-x and x-x" never filled in; intervention periods not mapped to calendar dates
- Finding 8 (Only 8 global search replicates): C — too few replicates for 15-parameter model; standard is 40-100
- Finding 9 (Convergence plots as static PNG images): C — pre-generated images cannot be verified as coming from the described analysis
- Finding 10 (No process noise in transmission): D — binomial demographic stochasticity only; no environmental/overdispersion noise on Beta (matches Human Issue #2)
- Finding 11 (rw.sd = 0.01 uniformly for all parameters): C — uniform perturbation ignores parameter scale differences; below course standard of 0.02
- Finding 12 (Fixed initial conditions, no sensitivity analysis): C — I_0 = 250 unjustified and no sensitivity to alternative values shown
- Finding 13 (H accumulator mismatch also affects rmeasure): C — rmeas generates cases = rnorm(rho*H)+D, inconsistent with dmeas and misuses stock D vs. flow deaths
- Finding 14 (ACF interpretation overstated for stationarity): C — slow ACF decay cited for differencing without formal unit root test
- Finding 15 (AIC table may contain numerical instability): C — Gaussian ARIMA applied to non-Gaussian overdispersed counts without log-transform

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |
