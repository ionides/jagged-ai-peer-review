## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "AIC-selected ARIMA(5,5) has roots outside unit circle making model non-causal and non-invertible")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "Log-likelihood comparison between SARIMA and SEIR is invalid — SARIMA evaluated on differenced data, SEIR on raw series")
- Human Issue #8: covered (matched by finding: "Data source reproducibility issue — Kaggle snapshot version not specified")
- Human Issue #9: covered (matched by finding: "References to prior projects without independent validation of suitability for current data and variants")
- Human Issue #10: missed

**Findings classification:**
- Finding 1 (S(0)=N, no recovered population): A — S initialized to full US population, ignoring prior infections and vaccination
- Finding 2 (Accumulator H conflates recoveries with new cases): A — measurement model tracks recoveries rather than incident infections
- Finding 3 (SARIMA vs. SEIR log-likelihood comparison invalid): B — SARIMA likelihood on differenced data, SEIR on raw; not directly comparable (matches Human Issue #7)
- Finding 4 (Np=100 too small in global search): A — only 100 particles for final likelihood evaluation, unreliable MLE
- Finding 5 (Convergence absent, no remediation): A — authors acknowledge non-convergence but take estimates anyway
- Finding 6 (Gap in beta time-period specification): A — 28-day window Nov 12–Dec 8 unaccounted for in stated formulas
- Finding 7 (mu_IR fixed without justification): A — recovery rate fixed at 0.1 with no reference or sensitivity analysis
- Finding 8 (SARIMA formula typographical error): C — epsilon_n appears twice on RHS; symbol p reused for seasonal and non-seasonal AR orders
- Finding 9 (High-order ARIMA(5,5) causality/invertibility issues): D — 4 AR and 1 MA roots outside unit circle; model accepted without correction (matches Human Issue #2)
- Finding 10 (Normal approximation for count data): C — normal used for case counts without justification or comparison to negative binomial
- Finding 11 (b5 inconsistency between text and code): C — text states b5=1.5, code sets b5=0.15, factor-of-10 discrepancy
- Finding 12 (Global search box for tau far from starting value): C — search box [0.2, 0.4] while initial tau=0.001
- Finding 13 (No profile likelihood or CIs for SEIR parameters): C — only point estimates reported after global search
- Finding 14 (Data source reproducibility): D — Kaggle snapshot version/date unspecified, raw CSV date range differs from stated range (matches Human Issue #8)
- Finding 15 (Prior project borrowed without independent validation): D — model structure from W21 Project 15 used without justifying suitability for different time period and variants (matches Human Issue #9)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
