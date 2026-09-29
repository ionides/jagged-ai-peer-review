## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding 8: "ARMA/SARMA fitted to differenced data rather than log-transformed data — log transformation abandoned")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding 8: same finding — ARMA fitted to differenced not log-transformed data, benchmark should use log scale")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding 9: "periodogram identifies ~60-week period from fewer than 2 full cycles, inconsistent with annual flu seasonality")
- Human Issue #12: missed

**Findings classification:**
- Finding 1 (accumulator tracks recoveries not infections): A — semantic mismatch in rprocess accumulator; no human issue raised this
- Finding 2 (invalid log-likelihood comparison ARMA/SARMA vs POMP): A — likelihoods on different data and distributional families; human issue #10 asks about AIC vs likelihood for ARMA-to-SARMA comparison, a distinct specific claim
- Finding 3 (profile likelihood is single-path, not true profile): A — single IF2 run from single start, single pfilter evaluation; no human issue raised this
- Finding 4 (global search 10 replicates with Nmif=50 insufficient): A — convergence not confirmed; no human issue raised this
- Finding 5 (rho profile range ±20% far too narrow): A — singleton CI artifact of grid range; no human issue raised this (human issues #2/#3 address misinterpretation of identifiability, not the grid range methodology)
- Finding 6 (no benchmark comparison on same data): A — no valid quantitative comparison against non-mechanistic model; no human issue raised this
- Finding 7 (no quantitative model diagnostics beyond visual inspection): A — no conditional log-likelihoods, ESS, or simulation summary statistics; no human issue raised this
- Finding 8 (ARMA/SARMA fitted to differenced not log-transformed data): D — matches Human Issues #4 and #7
- Finding 9 (periodogram frequency interpretation questionable): D — matches Human Issue #11
- Finding 10 (amp logit constraint noted): C — minor note that constraint is correctly implemented; no human issue raised this
- Finding 11 (phase grid may wrap around 52-week periodicity): C — profile grid spans the periodicity boundary; no human issue raised this
- Finding 12 (only 4 of 13 parameters profiled): C — key parameters like mu_EI and mu_RS omitted; no human issue raised this
- Finding 13 (parameter estimates not compared to biological knowledge): C — rho remarkably small and not discussed; no human issue raised this
- Finding 14 (data path hard-coded as ../Data/): C — reproducibility concern; no human issue raised this
- Finding 15 (single pfilter per profile grid point introduces Monte Carlo noise): C — profile curves unreliable due to noise; no human issue raised this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |
