## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "AIC table minimum vs auto.arima choice not reconciled")
- Human Issue #7: covered (matched by finding: "No benchmark comparison between POMP and SARIMA")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: missed
- Human Issue #13: covered (matched by finding: "Non-convergent mif2 traces")
- Human Issue #14: covered (matched by finding: "No profile likelihoods or parameter uncertainty")
- Human Issue #15: missed
- Human Issue #16: missed

**Findings classification:**
- 24.13.1: A — Transmission force driven by quarantined rather than infectious individuals
- 24.13.2: A — Undisclosed hard-coded perturbation of 100 individuals injected at t=125
- 24.13.3: B — No benchmark comparison between POMP and SARIMA (matches Human Issue #7)
- 24.13.4: B — No profile likelihoods or parameter uncertainty reported (matches Human Issue #14)
- 24.13.5: B — Non-convergent mif2 traces; parameters and loglik not plateauing (matches Human Issue #13)
- 24.13.6: C — Fixed parameters used throughout searches without epidemiological justification
- 24.13.7: C — Code inconsistency between R prototype and Csnippet (undefined variables in prototype)
- 24.13.8: C — Severe Monte Carlo variability (loglik.se as high as 89.3) for some parameter sets
- 24.13.M1: C — No ESS diagnostics to assess particle filter degeneracy
- 24.13.M2: C — rho search range constrained to [0.4, 0.6] without justification
- 24.13.M3: C — Biologically inconsistent initial conditions (Q_o=100 with I_o=0)
- 24.13.9: D — AIC table optimum differs from auto.arima recommendation without reconciliation (matches Human Issue #6)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 2 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 12 |
| F (Human-AI contradiction) | 0 |
