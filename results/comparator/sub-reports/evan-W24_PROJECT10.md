## Evan

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "24.10.5 — no fitted model overlay for flu data")
- Human Issue #3: covered (matched by finding: "24.10.6 — no benchmark comparison")
- Human Issue #4: covered (matched by finding: "24.10.10 — parameter estimates not compared to literature")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- 24.10.1: A — code bug: dN_RS drawn from Infectious (I) instead of Recovered (R) compartment
- 24.10.2: A — profile likelihood for mu_SV is not a valid profile; CI is invalid
- 24.10.3: A — unexplained 30-unit loglik discrepancy between profile scatter and global search
- 24.10.4: A — mu_RS is effectively not estimated; fixed at 0.1/week without justification
- 24.10.5: B — no fitted model overlay for flu data (matches Human Issue #2)
- 24.10.6: B — no benchmark comparison against a non-mechanistic baseline (matches Human Issue #3)
- 24.10.7: A — H accumulator reset not confirmed; may produce cumulative rather than interval likelihoods
- 24.10.8: C — ACF argument for needing POMP is logically inverted
- 24.10.10: D — parameter estimates not compared to literature or given contextual discussion (matches Human Issue #4)
- 24.10.11: C — V compartment is absorbing; vaccine waning not modeled or acknowledged
- 24.10.12: C — effective sample size not monitored during particle filtering

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 3 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |
