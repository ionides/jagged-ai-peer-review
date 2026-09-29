## Evan

**Coverage record:**
- Human Issue #1: covered (matched by finding: "25.15.4 — GARCH benchmark comparison needs clarification; tseries::garch likelihoods may reflect normalization conventions rather than actual log-likelihoods")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "25.15.M3 — Missing consolidated model comparison table with all likelihoods")
- Human Issue #6: covered (matched by finding: "25.15.4 — GARCH benchmark comparison needs clarification; tseries::garch likelihoods cannot be directly compared yet are used as a beaten benchmark")

**Findings classification:**
- 25.15.1: A — SSV process equation inconsistency between code and stated model (phi*sqrt(V) vs phi*V)
- 25.15.2: A — No profile likelihoods or confidence intervals reported for any model
- 25.15.3: A — Gamma_fng sign instability between local and global search; sign of key parameter unidentified
- 25.15.4: B — GARCH benchmark comparison needs clarification; tseries::garch likelihood normalization issues make the comparison invalid (matches Human Issues #1 and #6)
- 25.15.5: A — Gamma interpretation conflates changes in FNG index with levels
- 25.15.M1: C — ACF used without formal test (ADF/KPSS) to justify differencing of FG index
- 25.15.M2: C — Degrees of freedom for t-distribution selected informally without likelihood justification
- 25.15.M3: D — Missing consolidated model comparison table with all likelihoods and parameter counts (matches Human Issue #5)
- 25.15.M4: C — Inconsistent reported likelihood for SSV normal model (3899.52 vs 3957.105)
- 25.15.M5: C — sigma_nu converges near zero in modified Breto models suggesting weak leverage identification
- 25.15.M6: C — No reproducibility archive or standalone script linked
- 25.15.M7: C — Typos and text errors throughout

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |
