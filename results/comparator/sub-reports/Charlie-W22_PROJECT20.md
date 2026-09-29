## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by findings: "Profile likelihoods are degenerate: CIs collapse to single points" and "Global search box computed from full likelihood table including implausible values")
- Human Issue #3: covered (matched by finding: "BoxCox transformation introduces an arbitrary offset (+1050) with no justification")
- Human Issue #4: covered (matched by finding: "SARIMA and POMP likelihoods applied to different datasets and cannot support benchmark comparison")

**Findings classification:**
- Finding 1 (measurement model returns 0 instead of -Inf for invalid states): A — coding error silently corrupts particle filter weights
- Finding 2 (cos in writeup vs sin in code): A — mathematical model contradicts code implementation
- Finding 3 (POMP log-likelihood three orders of magnitude below SARIMA): A — magnitude gap signals fundamental misspecification but benchmark not meaningful
- Finding 4 (profile likelihoods degenerate, CIs collapse to single points): B — noisy/sparse profile makes CI claims invalid (matches Human Issue #2)
- Finding 5 (rho fixed at implausibly small value, mu_IR biologically implausible): A — unjustified fixed reporting rate with compensating parameter confound
- Finding 6 (local search uses %do% instead of %dopar%): A — sequential execution inconsistent with intended parallel design
- Finding 7 (global search box derived from full table including implausible values): B — wide box yields profile failures explaining degenerate CIs (matches Human Issue #2)
- Finding 8 (missing convergence diagnostics for global search): A — no trace plots; local search acknowledged not to have converged
- Finding 9 (SARIMA and POMP on different datasets, benchmark comparison invalid): B — different time windows and scales mean likelihoods are not comparable (matches Human Issue #4)
- Finding 10 (AIC table values are per-observation normalized, not standard scale): C — normalization undisclosed, adds to cross-model confusion
- Finding 11 (rho in partrans but in fixed_params): C — inconsistent specification, transformation defined but unused
- Finding 12 (BoxCox offset +1050 unjustified): D — arbitrary constant offset unexplained, transformation properties unclear (matches Human Issue #3)
- Finding 13 (SARIMA prediction description inaccurate): C — training window stated as through 2018 but actually ends mid-2018
- Finding 14 (no model diagnostics beyond visual simulation for SIRS): C — no conditional log-likelihoods or ESS analysis shown
- Finding 15 (pandemic cutoff hardcoded as week 260, not documented): C — fragile hardcoded threshold absent from mathematical writeup

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |
