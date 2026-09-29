## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "ΔZ(t) truncation — measurement model ignores left-censoring at zero")
- Human Issue #3: covered (matched by finding: "S treated as compartment but also used as covariate — model internally inconsistent")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "N accumulates monotonically but is never depleted — model cannot capture democratic decline")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "probe results interpretation contradictory — 'moderate evidence' of misfit then claimed as reliability")
- Human Issue #9: covered (matched by finding: "negative exponential relationship in pair plot attributed to theory but is symptom of parameter confounding")
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (No mif2 code shown): A — algorithm identity and reproducibility cannot be verified
- Finding 2 (Global search, not profile likelihood): A — CI construction invalid; profiles not computed by optimizing out nuisance parameters
- Finding 3 (Transition rate contradicts model equation): A — code uses N/tot_sov, equation states β·R(t)/ζ(t); three-way mismatch
- Finding 4 (ΔZ(t) truncation, measurement model ignores left-censoring): B — matches Human Issue #2
- Finding 5 (S as compartment and covariate simultaneously): B — matches Human Issue #3
- Finding 6 (N accumulates monotonically, never depleted): B — matches Human Issue #5
- Finding 7 (AIC for IID model computed incorrectly): A — formula uses 2 instead of 4 parameters
- Finding 8 (Poisson log-likelihood hard-coded): A — non-reproducible literal value rather than logLik() extraction
- Finding 9 (No convergence diagnostics): C — no trace plots, no multi-run comparison
- Finding 10 (Figure caption numbering incorrect): C — Fig. 3 labeled "Figure 2," Fig. 7 used twice
- Finding 11 (Probe results interpretation contradictory): D — matches Human Issue #8
- Finding 12 (Negative exponential relationship interpretation unsupported): D — matches Human Issue #9
- Finding 13 (rho interpreted as "coding efficiency"): C — non-standard reinterpretation of reporting fraction without justification
- Finding 14 (Initial condition for S inconsistent with data): C — S(0)=23 with P(0)+R(0)+N(0)=4 lacks justification
- Finding 15 (Poisson log-likelihood stated without derivation): C — same underlying reproducibility issue as Finding 8; no code path shown

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |
