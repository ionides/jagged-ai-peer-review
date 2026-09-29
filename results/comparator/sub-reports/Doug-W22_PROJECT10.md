## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Normal measurement model is poorly motivated and inconsistent with NegBin used in SIR")
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Population size inconsistency between SIR local and global searches — N=500,000 vs N=50,000,000")
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed

**Findings classification:**
- Major #1 (SEAPIRD rmeasure adds D to cases while dmeasure subtracts deaths — internal inconsistency): A — code-level mismatch between dmeasure and rmeasure in SEAPIRD
- Major #2 (Normal measurement model poorly motivated for count data, inconsistent with NegBin in SIR): B — matches Human Issue #3
- Major #3 (No profile likelihoods computed for any parameter): A — parameter identifiability unassessed
- Major #4 (N=500,000 in SIR global search vs N=50,000,000 in local search and text): B — matches Human Issue #5
- Major #5 (Invalid direct log-likelihood comparison between ARMA and POMP models): A — different observation distributions make comparison invalid
- Major #6 (Insufficient computational effort — 16 replicates, Np=100 for SIR local): A — non-convergence misattributed to biology
- Major #7 (No valid benchmark comparison for mechanistic models): A — no same-scale non-mechanistic baseline
- Major #8 (SIR accumulator H tracks recoveries dN_IR, not new infections dN_SI): A — semantic mismatch between accumulator and observed data
- Minor: week-7 periodicity not incorporated in POMP observation model: C — unmodeled periodicity degrades particle filter
- Minor: SEAPIRD initial conditions set S=N ignoring initially infected, violating population conservation: C — S + I > N at time zero
- Minor: H initialized to 169 in sir_rinit despite H being an accumvar reset each step: C — initial value unexplained
- Minor: global SIR results not sorted before selecting row 1 as best: C — best parameters may not actually be best
- Minor: log-likelihood convergence diagnostic chunk marked eval=FALSE and not rendered: C — essential diagnostics excluded
- Minor: no comparison of parameter estimates to scientific literature values: C — biological plausibility unchecked
- Minor: pairs plots include non-finite log-likelihoods without filtering: C — axes distorted by -Inf values

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
