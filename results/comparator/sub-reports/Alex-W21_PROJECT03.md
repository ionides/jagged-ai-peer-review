## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by findings: "SIRV1 V→I hazard uses V instead of I" and "SIRV1 S→V hazard is density-dependent, inconsistent with ODE")
- Human Issue #3: covered (matched by finding: "SIR model dismissed based on visual inspection of pair plots, not likelihood comparison")
- Human Issue #4: covered (matched by finding: "SIRV2 deterministic vaccination flow dN_SV can produce negative S without bounds check")
- Human Issue #5: covered (matched by finding: "Run level is set to 1 throughout — results computed with far too few particles and iterations")
- Human Issue #6: missed

**Findings classification:**
- Finding 1 [MAJOR] H tracks removals (dN_IR) not new infections: A — fundamental model misspecification not raised by human
- Finding 2 [MAJOR] Prediction uses initial-guess parameters not MLE: A — not raised by human
- Finding 3 [MAJOR] SIRV1 V→I hazard uses V instead of I: B — matches Human Issue #2 (ODE does not match POMP implementation)
- Finding 4 [MAJOR] SIRV1 S→V hazard is density-dependent, inconsistent with ODE: B — matches Human Issue #2 (ODE does not match POMP implementation)
- Finding 5 [MAJOR] Run level 1 throughout — too few particles and iterations: B — matches Human Issue #5 (benefits from running code longer)
- Finding 6 [MAJOR] Profile likelihood: Sigma not held fixed in first mif2 call: A — not raised by human
- Finding 7 [MAJOR] SIRV2 dN_SV can produce negative S without bounds check: B — matches Human Issue #4 (t² coded as dt² in SIRV2 vaccination term, same problematic dN_SV expression)
- Finding 8 [MODERATE] Local search uses only a single particle filter replication: C — not raised by human
- Finding 9 [MODERATE] CI cutoff for sigma computed but not plotted: C — not raised by human
- Finding 10 [MODERATE] Active cases used as I(0) conflates reported with true infectious: C — not raised by human
- Finding 11 [MODERATE] Vaccine efficacy conclusion ">80%" not supported by analysis: C — not raised by human
- Finding 12 [MODERATE] SIR model dismissed by visual inspection of pair plots, not likelihood comparison: D — matches Human Issue #3 (human notes SIRV1 improves likelihood by 8 units and an LRT would be valid)
- Finding 13 [MINOR] Vaccination regression fitted on same data used in POMP model: C — not raised by human
- Finding 14 [MINOR] Prediction plots show 5 simulations but text claims 10: C — not raised by human
- Finding 15 [MINOR] SIRV1 global search pair plot uses threshold of 1000 log units, too wide: C — not raised by human

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |
