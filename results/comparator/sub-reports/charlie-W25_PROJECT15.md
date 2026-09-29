## Charlie

**Coverage record:**
- Human Issue #1: covered (matched by finding: "GARCH vs POMP log-likelihood comparison acknowledged as invalid but used in conclusions")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "No consolidated model comparison table")
- Human Issue #6: covered (matched by finding: "GARCH vs POMP log-likelihood comparison acknowledged as invalid but used in conclusions")

**Findings classification:**
- Finding 1 (Breto and SSV models fitted to different data): A — cross-family log-likelihood comparisons invalid due to different data series
- Finding 2 (stew() filename collision): A — "New Global Search" silently reloads first-search results
- Finding 3 (Heston code does not implement stated equation): A — phi*sqrt(V) in code vs phi*V in text
- Finding 4 (GARCH vs POMP comparison invalid but used): B — tseries::garch likelihood not on same scale; used in conclusions despite acknowledged invalidity (matches Human Issues #1 and #6)
- Finding 5 (No profile likelihoods or confidence intervals): A — no profiles for any of the six models
- Finding 6 (sigma_nu converges to boundary): A — leverage parameter degeneracy not investigated as model misspecification
- Finding 7 (FG Index from live API): A — analysis not reproducible due to shifting API window
- Finding 8 (t df by trial-and-error): C — degrees of freedom fixed informally without reported likelihoods
- Finding 9 ("New Global Search" is local refinement): C — narrow parameter box around prior optimum, not a genuine global search
- Finding 10 (H_0 non-convergence not remediated): C — initial condition instability unaddressed
- Finding 11 (gamma sign interpretation fragile): C — sign flips between local and global optima, no profile to support conclusion
- Finding 12 (Title typo): C — missing initial "V" in document title
- Finding 13 (Np=2000 below course standard): C — run_level=3 uses Np=2000 instead of Np=5000
- Finding 14 (No consolidated model comparison table): D — six models compared without a summary table (matches Human Issue #5)
- Finding 15 (dFNG zero-padding without justification): C — ad hoc initialization of differenced FNG covariate at t=0

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 3 |
| F (Human-AI contradiction) | 0 |
