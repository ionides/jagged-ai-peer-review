## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Filtering for simulated data is inconclusive and undiagnosed — simulated data much more volatile than actual data, initial parameter miscalibration noted")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "Filtering for simulated data is inconclusive and undiagnosed — simulated data much more volatile than actual data, initial parameter miscalibration noted")
- Human Issue #7: covered (matched by findings: "Missing convergence diagnostics for iterated filtering" and "No model diagnostics beyond visual residuals")

**Findings classification:**
- Finding 1 (Invalid cross-model AIC comparison): A — GARCH likelihood normalization not verified before comparing AIC across models
- Finding 2 (Missing convergence diagnostics): B — no trace plots or convergence evidence for mif2 (matches Human Issue #7)
- Finding 3 (No profile likelihoods): A — profile likelihoods absent for all six parameters
- Finding 4 (Global search initialized from local search result): A — each global replicate inherits state from if1[[1]] rather than a fresh pomp object
- Finding 5 (Filtering for simulated data inconclusive and undiagnosed): B — simulated data much more volatile than actual data; initial parameter miscalibration unaddressed (matches Human Issues #3 and #6)
- Finding 6 (Np = 2000 below course standard): C — run_level 3 uses 2000 particles vs. course standard of 5000
- Finding 7 (No benchmark comparison on POMP likelihood scale): C — no IID or simple AR benchmark on particle-filter likelihood scale
- Finding 8 (No model diagnostics beyond visual residuals): D — no conditional log-likelihoods, no ESS monitoring, no period-specific diagnostics (matches Human Issue #7)
- Finding 9 (Nasdaq-500 error throughout conclusion): C — index name is factually incorrect in conclusion and references
- Finding 10 (Breto 2014 not cited as primary reference): C — model equations taken from Breto (2014) but that paper absent from reference list
- Finding 11 (Pairs plot threshold not justified): C — logLik > max - 30 threshold not explained or distinguished from formal confidence set
- Finding 12 (Nreps_local = 20 below course standard): C — run_level 3 uses 20 local replicates vs. course standard of 40
- Finding 13 (No discussion of parameter interpretation): C — estimated parameters not compared to published estimates or assessed for plausibility
- Finding 14 (Causal/predictive language unsupported): C — conclusion claims model is "appropriate" based only on in-sample AIC
- Finding 15 (Missing sessionInfo): C — package versions not reported despite version-sensitive pomp API

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |
