## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by findings: "no likelihood-based inference performed on any POMP model"; "no convergence diagnostics, no mif2 runs in main analysis"; "no quantitative goodness-of-fit statistics reported for any model")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (No likelihood-based inference on any POMP model): B — no likelihood maximization performed; all parameters hand-selected; pfilter/mif2 abandoned (matches Human Issue #7)
- Finding 2 (No convergence diagnostics, no mif2 runs): B — main analysis has no iterated filtering runs or likelihood traces (matches Human Issue #7)
- Finding 3 (Smoothed non-integer data fed to binomial measurement model): A — 7-day rolling mean produces non-integer values passed to dbinom, causing undefined or silently wrong likelihood
- Finding 4 (Model 3 math inconsistent with code): A — equations specify binomial draw from I but code draws from S
- Finding 5 (LRT uses wrong df and mismatched data): A — ARIMA(4,1,4) vs ARIMA(1,1,1) tested with df=2 instead of df=6; LRT applied to different series than AIC table
- Finding 6 (No quantitative goodness-of-fit statistics for any SEIR variant): B — model comparison done entirely by visual inspection (matches Human Issue #7)
- Finding 7 (No benchmark comparison for POMP model): A — no non-mechanistic benchmark compared against SEIR using a common quantitative metric
- Finding 8 (H accumulator tracks recoveries, compared to new case reports): A — dN_IR used as basis for reported case counts, but reports measure new positive tests
- Finding 9 (Data duplication in introduction and Section 2.1): C — identical paragraphs about data sources appear in both sections
- Finding 10 (Vaccine constant V applied per Euler substep, not per day): C — V=2500 per substep yields 20,000 vaccinations/day with 8 substeps; hard-coded, not estimated
- Finding 11 (No residual diagnostics for ARIMA models): C — ACF/PACF of residuals and Ljung-Box test absent for both ARIMA models
- Finding 12 (Model selection ignores upper-boundary issue in AIC table): C — AR5/MA5 discarded without extending search to verify optimum is not at boundary
- Finding 13 (ARIMA model applied to post-vaccination data after pre-vaccination selection): C — no justification that pre-vaccination ARIMA structure persists; vaccination covariate coefficient reported as very small with no hypothesis test
- Finding 14 (Inconsistent parameter values between text and equations): C — text states mu_IR=0.9 but code uses mu_IR=0.09
- Finding 15 (Data loaded from live external URLs without local backup): C — reproducibility risk if GitHub URLs become unavailable

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 3 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |
