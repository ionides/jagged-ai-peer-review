## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "25.03.2 — profile likelihood under-powered; singleton CIs for phase and rho wrongly interpreted as evidence of unidentifiability")
- Human Issue #3: covered (matched by finding: "25.03.2 — profile likelihood under-powered; singleton CIs for phase and rho wrongly interpreted as evidence of unidentifiability")
- Human Issue #4: covered (matched by finding: "25.03.4 — log transformation described but ARMA fitting applied to raw non-log-transformed differenced counts")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "25.03.4 — log transformation described but ARMA fitting applied to raw non-log-transformed differenced counts")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: missed

**Findings classification:**
- 25.03.1: A — log-likelihood comparison between ARIMA (fit to differenced raw counts) and POMP (fit to raw counts) is across incompatible scales and uninterpretable
- 25.03.2: B — profile likelihood under-powered (10 grid points, single mif2 path per point); singleton CIs for phase and rho wrongly interpreted as unidentifiability (matches Human Issues #2 and #3)
- 25.03.5: A — no particle filter diagnostics (ESS plots, per-step conditional log-likelihoods) are present
- 25.03.14: A — no profile likelihood computed for transition rate parameters mu_EI, mu_IR, mu_RS
- 25.03.3: C — initial condition parameters S0, E0, I0, R0 have no rw.sd entries and are effectively fixed during mif2, but presented as estimated
- 25.03.4: D — log transformation described in Section 3 but all ARMA/SARMA fitting applied to raw non-log-transformed differenced counts (matches Human Issues #4 and #7)
- 25.03.7: C — single pfilter evaluation used to select the best local mif2 run, introducing Monte Carlo noise into the selection step
- 25.03.6: C — reporting rate rho ≈ 0.00015 (1 in 6,000 infections captured) not compared to published influenza ascertainment estimates
- 25.03.15: C — pair plots based on only 10 runs are too noisy to support identifiability conclusions

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |
