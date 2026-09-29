## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "cross-model log-likelihood comparisons are invalid due to different datasets/measurement distributions")
- Human Issue #6: covered (matched by finding: "no benchmark comparison against non-mechanistic models; GARCH log-likelihood acknowledged as incomparable but conclusions still drawn from it")

**Findings classification:**
- Finding 1 (IF2 global search initialized from previous mif2 result): A — global search for all POMP models anchored to local optimum by passing prior mif2 result instead of base pomp object
- Finding 2 (initial particle filter on simulated data): A — initial log-likelihood benchmarks computed on simulated rather than real data, making them meaningless as real-data benchmarks
- Finding 3 (Heston process equation mismatch): A — implemented Csnippet uses phi*sqrt(V) instead of phi*V, producing materially different dynamics from the stated model
- Finding 4 (no profile likelihoods): A — no profile likelihoods computed for any model; parameter identifiability not formally assessed despite noted convergence anomalies
- Finding 5 (no benchmark comparison; invalid GARCH comparison): B — GARCH log-likelihood acknowledged as not directly comparable to POMP log-likelihoods yet conclusions still assert POMP outperforms GARCH without quantitative basis (matches Human Issue #6)
- Finding 6 (duplicate stew() filename): A — second global search for basic Breto uses same filename as first search, so stew() loads prior results rather than running new search
- Finding 7 (cross-model log-likelihood comparisons invalid): B — models use different data objects and measurement distributions, making log-likelihood comparisons across the six model families numerically invalid (matches Human Issue #5)
- Finding 8 (degrees of freedom fixed without justification): C — Student's t df=5 chosen by informal visual inspection rather than likelihood maximization or quantitative model selection
- Finding 9 (FG Index fetched live from API): C — Fear & Greed Index fetched at render time from live API, violating reproducibility; results will differ on different render dates
- Finding 10 (stationarity assessed only by ACF): C — FG Index stationarity concluded from ACF inspection alone with no formal unit-root test (ADF, KPSS, or Phillips-Perron)
- Finding 11 (sigma_nu converges to zero): C — sigma_nu convergence to zero implies degenerate leverage process; text notes it but does not investigate via profile likelihood
- Finding 12 (title typo): C — YAML title reads "olatility" missing initial 'V'
- Finding 13 (H_0 non-convergence dismissed): C — H_0 non-convergence noted but dismissed without investigation; affects reliability of all co-moving parameter estimates
- Finding 14 (no final MLE parameter table): C — final MLE parameter vectors only appear inline in print() calls; no consolidated table for all six models
- Finding 15 (model comparison narrative inconsistent): C — text treats initial particle filter log-likelihoods at test parameters as evidence of fitted model performance rather than global-search MLE values

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |
