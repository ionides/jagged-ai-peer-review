## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed

**Findings classification:**
- Finding 1 (GARCH/POMP likelihood comparison invalid): A — GARCH log-likelihood from `tseries` uses non-standard normalization, making the central comparison numerically meaningless
- Finding 2 (No ARMA/ARIMA benchmark): A — no non-mechanistic benchmark model compared against the SV POMP model
- Finding 3 (Profile likelihoods absent): A — no profile likelihoods computed for any of the six model parameters; identifiability not assessed
- Finding 4 (Local search from single starting point): A — all 20 local mif2 replicates start from the same `params_test` vector
- Finding 5 (Convergence diagnostics not shown): A — no trace plots shown for any mif2 run despite run_level=3
- Finding 6 (Global search from single local endpoint): A — global search continues from `if1[[1]]` rather than starting fresh from random box draws
- Finding 7 (AIC comparison not discussed): C — parameter count difference and AIC not presented alongside raw likelihood comparison
- Finding 8 (Loess span not justified): C — `span=0.5` and `span=0.1` chosen without justification or sensitivity analysis
- Finding 9 (Loess date axis misaligned): C — time axis starts from 1962 but data begins in 1990
- Finding 10 (Filtering on simulated data incomplete): C — pfilter run on simulated data but no parameter recovery attempted
- Finding 11 (Loess x-axis start year inconsistent): C — duplicate of Finding 9; date sequence from 1962 inconsistent with 1990-onset data
- Finding 12 (Missing sessionInfo): C — no package version documentation included
- Finding 13 (CPI LRT conclusion overstated): C — failure to reject null stated as absence of association rather than lack of significant evidence
- Finding 14 (CPI "Customer" vs "Consumer"): C — consistent terminological error throughout the report
- Finding 15 (Monte Carlo SE not reported for global search): C — best log-likelihood -25.71 reported without Monte Carlo standard error

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |
