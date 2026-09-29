## Alex

**Coverage record:**
- Human Issue #1: covered (matched by finding: "ACF/PACF interpretation contradicts subsequent analysis — slow decay labeled non-stationary but series then concluded stationary")
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "GARCH summary statistics hidden via include=FALSE, preventing verification or comparison of model estimates")
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "no formal model comparison or likelihood-ratio test against GARCH benchmarks — POMP superiority claim unsupported")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (Measurement equation epsilon_n distribution mismatch): A — code implements N(0,1) but writeup states N(0,sigma_nu); documentation error with no human counterpart
- Finding 2 (No formal model comparison against GARCH benchmarks): B — POMP log-likelihood compared to GARCH without proper scaling or AIC table (matches Human Issue #7)
- Finding 3 (Severe non-convergence and multimodality in NFLX POMP): A — extreme parameter heterogeneity across replicates not corrected; no human counterpart
- Finding 4 (Spurious degenerate parameter combinations not excluded): A — near-unit-root explosive combinations included in plots without screening; no human counterpart
- Finding 5 (Log-return preprocessing introduces spurious zero return): A — c(0, diff(...)) prepends artificial zero passed to POMP filter; no human counterpart
- Finding 6 (ACF/PACF interpretation contradicts subsequent analysis): B — ACF slow decay labeled non-stationary but conclusion is stationarity; faulty stationarity reasoning (matches Human Issue #1)
- Finding 7 (STL decomposition applied to non-stationary price series): A — STL on raw prices with artificial frequency=252 seasonal period; no human counterpart
- Finding 8 (GARCH summary statistics hidden via include=FALSE): D — parameter estimates and fit statistics invisible, preventing model contrast (matches Human Issue #4)
- Finding 9 (Beta confidence interval formula incorrect): C — SE formula ignores residual variance, producing overconfident intervals; no human counterpart
- Finding 10 (Incomplete comment left in published writeup): C — placeholder discussion text visible in rendered HTML; no human counterpart
- Finding 11 (Global search box for phi excludes best local-search region): C — phi bounds (0.9, 0.999) exclude highest-likelihood region (0.75–0.89); no human counterpart
- Finding 12 (No out-of-sample evaluation despite defined holdout set): C — holdout 2023–2025 defined but never used; no human counterpart
- Finding 13 (ARIMA residual autocorrelation for SPY not addressed): C — Ljung-Box significant (p=0.03) but no corrective action taken; no human counterpart
- Finding 14 (Reference 12 URL typo): C — URL points to project07 instead of project11; no human counterpart
- Finding 15 (Repeated code block for saving SPY results): C — identical block appears twice, indicating incomplete script cleanup; no human counterpart

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 7 |
| F (Human-AI contradiction) | 0 |
