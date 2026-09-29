## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "24.14.4 — notation collision: mu_IR used for both force of infection and recovery rate, creating an equation-level inconsistency")
- Human Issue #6: covered (matched by finding: "24.14.2 — single mif2 run with trace plots still trending at iteration 50; reported parameter values are effectively starting-point values")
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "24.14.1 — mif2 internal log-likelihood reported directly without replicated pfilter; the −628.8447 figure is a noisy, biased estimate")
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: "24.14.2 — single mif2 run with no global search across starting points; convergence never established")
- Human Issue #12: missed

**Findings classification:**
- 24.14.1: B — mif2 log-likelihood reported without replicated pfilter (matches Human Issue #8)
- 24.14.2: B — single mif2 run; convergence not established; parameters still trending at final iteration (matches Human Issues #6 and #11)
- 24.14.3: A — simulations exceed observed data by two orders of magnitude; authors incorrectly claim model captures trend
- 24.14.5: A — no quantitative comparison of ARIMA and POMP log-likelihoods
- 24.14.7: A — fixed population N uses 2023 U.S. value for 1953–2020 data, biasing transmission parameter throughout
- 24.14.8: A — estimated parameters imply biologically implausible latent and infectious periods for TB; not flagged
- 24.14.4: D — notation collision: mu_IR defined as both force of infection in equations and recovery rate in parameter list (matches Human Issue #5)
- 24.14.6: C — ARIMA model selection chose higher-AIC model (0,1,5) over lower-AIC model (3,1,4) without documented rationale
- 24.14.9: C — ESS collapses to near zero during 1975–1990 HIV-era resurgence period; not discussed
- 24.14.10: C — residual diagnostics for the selected ARIMA(0,1,5) model not shown in manuscript
- Reproducibility: C — no sessionInfo(), package version pins, or RNG seeds; multiple unused versions of model code not removed

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 4 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |
