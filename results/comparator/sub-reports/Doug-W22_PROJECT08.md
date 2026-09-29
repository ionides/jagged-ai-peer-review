## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "Biologically implausible initial conditions for beta-variant compartment")
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Model selection by LRT between ARIMA(2,1,1) and ARIMA(2,1,0) is applied incorrectly")
- Human Issue #5: covered (matched by finding: "Insufficient number of IF2 iterations — Nmif=50 insufficient, convergence traces confirm eta has not stabilized")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: covered (matched by finding: "Population figure error in text — N=843400 stated but Turkey's population is 84.3 million")
- Human Issue #10: missed
- Human Issue #11: missed

**Findings classification:**
- Major #1 (Fundamental mismatch between data variable and accumulator — active cases stock vs. new-recoveries flow): A
- Major #2 (Accumulator H tracks recoveries dN_IR, not new detections dN_EI): A
- Major #3 (Global search initialized from previous mif2 object, inheriting exhausted cooling schedule): A
- Major #4 (Global search box excludes region containing best-fit parameters): A
- Major #5 (Reported log-likelihood -2336 inconsistent with stored artifacts showing -2308.63): A
- Major #6 (Invalid log-likelihood comparison between ARIMA and SEIREIR — different distributional families on different data transformations): A
- Major #7 (No profile likelihoods and no parameter confidence intervals): A
- Major #8 (Biologically implausible initial conditions — R_b set to ~75.9 million at time zero for a variant not yet in existence): B — (matches Human Issue #2)
- Minor: Population figure error in text (N=843400 stated, should be 84,340,000): D — (matches Human Issue #9)
- Minor: Local search uses %do% (sequential) instead of %dopar% (parallel): C
- Minor: Global search uses Np=1000, local uses Np=2000, no justification: C
- Minor: Hard-coded beta-variant emergence at t=125 without justification: C
- Minor: No model diagnostics reported (no conditional log-likelihood plots, no ESS monitoring): C
- Minor: Insufficient IF2 iterations — Nmif=50, convergence traces confirm eta has not stabilized: D — (matches Human Issue #5)
- Minor: Model selection by LRT between ARIMA(2,1,1) and ARIMA(2,1,0) applied incorrectly — reasoning that non-rejection means "better" is flawed: D — (matches Human Issue #4)
- Minor: Notation inconsistency — equations use continuous-time differentials but implementation uses discrete-time Euler steps: C
- Minor: Code availability issue — local.RData referenced but absent from project folder: C

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |
