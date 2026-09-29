## Evan

**Coverage record:**
- Human Issue #1: covered (matched by findings: "25.05.1 — invalid likelihood comparison: SARIMA on log1p vs POMP on raw data"; "25.05.2 — no valid benchmark on the same data scale")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "25.05.1 — invalid likelihood comparison: SARIMA on log1p vs POMP on raw data, Jacobian correction needed")
- Human Issue #8: covered (matched by finding: "25.05.10 — reported loglik -332.02 inconsistent with printed output -331.39 and -331.08")
- Human Issue #9: missed

**Findings classification:**
- 25.05.1: B — invalid likelihood comparison between SARIMA (log1p-transformed) and POMP (raw data) (matches Human Issues #1 and #7)
- 25.05.2: B — no valid non-mechanistic benchmark on the same data scale (matches Human Issue #1)
- 25.05.3: A — sigma_M declared but never used; measurement model is pure Poisson despite text implying overdispersion
- 25.05.4: A — cumulative C tracked with accumvars but measurement model observes rho*I, not rho*C
- 25.05.5: A — convergence not demonstrated; trace plots show no convergence at iteration 100
- 25.05.6: A — no profile likelihoods or confidence intervals for any parameter
- 25.05.7: A — biologically implausible mu_EI (~2.3 day latent period) and gamma (~0.76 day infectious period) not discussed
- 25.05.11: A — N_0 = 100,000 far below Florida's actual population (~18-20 million)
- 25.05.8: C — initial r = 0.135 implausible as monthly birth rate (carryover from dengue source model)
- 25.05.10: D — reported loglik = -332.02 inconsistent with printed output (-331.39 and -331.08) (matches Human Issue #8)
- 25.05.12: C — ESS not monitored; filter degeneracy not checked
- 25.05.13: C — forward simulations misrepresented as fit assessment rather than prior predictive checks
- 25.05.M1: C — immigration model improvement marginal by AIC (DAIC ≈ +0.4 favoring simpler model)
- 25.05.15: C — notation error in SARIMA equation: missing backshift operator B in MA(1) polynomial
- 25.05.14: C — periodogram x-axis label says "cycles per year" but spec.pgram with frequency=12 produces cycles per month

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
