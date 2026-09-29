## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by findings: "Gaussian HMM AR(1) declining likelihood acknowledged but not addressed structurally" and "last iteration estimator used in comparison table without caveat")

**Findings classification:**
- Finding 1 (poor man's profile is a likelihood slice, not profile likelihood): A — no corresponding human issue
- Finding 2 (Gaussian HMM global search uses Np=200, insufficient): A — no corresponding human issue
- Finding 3 (Gaussian HMM AR(1) declining likelihood acknowledged but not addressed structurally): B — matches Human Issue #1
- Finding 4 (AIC table mixes ARMA/GARCH and POMP likelihoods without noting non-comparability): A — no corresponding human issue
- Finding 5 (Heston global search box contains undefined parameter sigma_nu): A — no corresponding human issue
- Finding 6 (no non-mechanistic benchmark comparison): A — no corresponding human issue
- Finding 7 (Gaussian HMM AR(1) violates POMP conditional independence requirement): A — no corresponding human issue
- Finding 8 (data aggregation choice of 97.5th percentile not formally justified): C — no corresponding human issue
- Finding 9 (Student-t HMM uses euler(delta.t=1/12) while Gaussian HMM uses discrete_time): C — no corresponding human issue
- Finding 10 (last iteration estimator used in comparison table without caveat): D — matches Human Issue #1
- Finding 11 (Heston Euler discretization formula for log-volatility process contains error): C — no corresponding human issue
- Finding 12 (conditional log-likelihood diagnostic from last mif2 object, not MLE): C — no corresponding human issue
- Finding 13 (Heston global search box restricts rho to [0,1], excluding negative correlations): C — no corresponding human issue
- Finding 14 (typos "likelihoos" and "exhbited" in conclusion): C — no corresponding human issue
- Finding 15 (no sessionInfo or package versions reported): C — no corresponding human issue

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 0 |
| F (Human-AI contradiction) | 0 |
