## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed

**Findings classification:**
- 21.15.M2: A — profile likelihood for rho is too sparse to support the reported CI
- 21.15.M3: A — no convergence diagnostics for the global search
- 21.15.M4: C — ARMA benchmark comparison: Jacobian correction for log-transform not explained in text
- 21.15.M1: C — sensitivity of fixed mu_EI and mu_IR not reported
- 21.15.M5: C — fixed initial conditions E_0=100, I_0=200 without sensitivity analysis
- 21.15.m7: C — run-level parameters (Np, Nmif, NREPS, NSTART) not stated in text
- 21.15.m8: C — effective sample size from particle filter not reported
- 21.15.m14: C — truncated normal measurement model used without justification or comparison to negative binomial
- 21.15.new1: C — no profile likelihoods for any of the five beta parameters
- 21.15.new2: C — figures show forward simulations from MLE, not filtering-distribution-conditioned simulations
- 21.15.m6: C — pathological divergence of b3/b4 in local search traces not discussed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |
