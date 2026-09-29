## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "21.07.M3 — population size N has no clear physical interpretation given the normalized Google Trends data")
- Human Issue #4: covered (matched by finding: "21.07.2 — profile likelihood computation iterates over the wrong grid, making the profile plots invalid")

**Findings classification:**
- 21.07.1: A — debug-scale computations throughout (run_level=1)
- 21.07.2: B — profile likelihood computation uses the wrong grid, invalidating all profile plots and CIs (matches Human Issue #4)
- 21.07.3: A — no benchmark comparison against non-mechanistic model
- 21.07.4: A — no convergence diagnostics (no IF2 trace plots)
- 21.07.5: C — measurement model passes H (accumulator) as the negative binomial size/dispersion parameter
- 21.07.6: C — rho and N excluded from rw.sd despite being listed as variable parameters
- 21.07.7: C — spectral analysis subsets to last 43 days without justification
- 21.07.M1: C — ESS not monitored during particle filtering
- 21.07.M2: C — best log-likelihood not stated in narrative prose
- 21.07.M3: D — population size N has no clear physical interpretation given normalized Google Trends data (matches Human Issue #3)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |
