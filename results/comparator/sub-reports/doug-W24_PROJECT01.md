## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "tot_sov is the smoothed spline of S while S is also a dynamic latent state — relationship unexplained")
- Human Issue #4: covered (matched by finding: "observation variable conflates increment ΔZ(t) with accumulating stock N(t) — measurement model dimensionally inconsistent")
- Human Issue #5: covered (matched by finding: "observation variable conflates increment ΔZ(t) with accumulating stock N(t) — measurement model dimensionally inconsistent")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (mu_IR replaces mu_PR — undisclosed parameter substitution): A — column rename silently patches RDS/code mismatch; human did not raise it
- Finding 2 (N/tot_sov used where R/tot_sov specified): A — code uses N (democracies) instead of R (revolutionary threats) in S→P transition; human did not raise it
- Finding 3 (observation conflates increment and stock; measurement model dimensionally inconsistent): B — ΔZ(t) is a one-year increment but model maps it to accumulating stock N(t); N is absorbing (matches Human Issues #4 and #5)
- Finding 4 (no convergence diagnostics): A — no LL traces, no scatter of final LLs across runs; human did not raise it
- Finding 5 (profile likelihoods are not proper profiles): A — plots are global-search scatter, not re-optimized profiles; human did not raise it
- Finding 6 (aggregate global count not POMP-appropriate): A — treating all countries as one latent chain is a category error; human did not raise it
- Finding 7 (POMP outperformed by 2-parameter NegBin regression): A — lower likelihood than simpler benchmark not adequately addressed; human did not raise it
- Finding 8 (initial conditions implausible and unjustified): A — P=1, R=2, N=1 are arbitrary; no sensitivity analysis; human did not raise it
- Finding 9 (mu_IR/mu_PR completely unidentified): A — parameter ranges 0.035–839 with flat likelihood across 200 runs; human did not raise this parameter specifically
- Finding 10 (figure caption numbering error): C — two figures share "Figure 7" caption; human did not raise it
- Finding 11 (AIC.iid uses only 2 parameters): C — understates IID model's AIC penalty; human did not raise it
- Finding 12 (ρ interpretation as "coding efficiency" non-standard and implausible): C — ρ ≈ 0.07 implies 93% of democratic episodes unrecorded; human did not raise it
- Finding 13 (grammatical and notation inconsistencies throughout): C — transition equation inconsistently uses both N and R in different parts; human did not raise it
- Finding 14 (tot_sov is smoothed spline interpolation of S, not S itself): D — latent S and covariate tot_sov relationship unexplained; S depletes to ~0 while tot_sov grows to ~195 (matches Human Issue #3)
- Finding 15 (no forecast from filtering distribution): C — simulations from t=0, not from filtering distribution; human did not raise it

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |
