## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: C5 — k fixed at 10 without profiling)
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: C3 — likelihood slice CI is invalid)
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- C1: A — H accumulator likely zeroed before dmeas evaluation
- C2: A — profile likelihood for rho truncated at its lower boundary
- C4: A — gamma biologically implausible and identifiability-entangled with mu_RS
- C3: D — CI drawn from likelihood slice is invalid (matches Human Issue #8)
- C5: D — k fixed at 10 without profiling or random-walk standard deviation (matches Human Issue #1)
- C6: C — log-likelihood standard errors vary; evaluation protocol not documented
- X2: C — "posterior predictive check" terminology is incorrect
- X3: C — number of mif2 starting points for main model global searches not reported

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |
