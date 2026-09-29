## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "No Likelihood-Based Inference Performed for Any POMP Model"; also matched by finding: "No Parameter Estimation — All Parameters Are Hand-Tuned")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (No Likelihood-Based Inference for POMP): B — no particle filter run, no likelihood reported, no inferential content (matches Human Issue #7)
- Finding 2 (No Parameter Estimation — All Parameters Hand-Tuned): B — no mif2 local/global search, no profile likelihood (matches Human Issue #7)
- Finding 3 (Bug in Model 3: N_SV Drawn from I Instead of S): A — mathematical writeup has vaccination transition drawing from infectious compartment rather than susceptible
- Finding 4 (Binomial Measurement Model Source of -Inf Log-Likelihoods): A — dbinom called with non-integer H causing -Inf, unresolved in main body
- Finding 5 (Data Window Choice Unexplained): A — 105-day subset of 413-observation series not epidemiologically motivated
- Finding 6 (Duplicate Introduction Section Content): A — two paragraphs in Section 2.1 are verbatim copies of Section 1 text
- Finding 7 (LRT Degrees of Freedom Are Wrong): A — pchisq uses df=2 but ARIMA(4,1,4) vs ARIMA(1,1,1) difference is 6 parameters
- Finding 8 (ARMA Model Uses Wrong Data Split): A — pre-vaccination ARIMA coefficients applied to post-vaccination data without re-estimation
- Finding 9 (Susceptible Population Calculation Conflates Cumulative Cases with Active Immunity): C — deaths double-counted via both cases and deaths terms in susceptible formula
- Finding 10 (Vaccination Rate Hard-Coded in Models 1 and 2): C — fixed constant embedded in Csnippet with no corresponding estimable parameter
- Finding 11 (Model 2 Uses index as State Variable Incorrectly): C — deterministic time counter declared as stochastic state, wastes memory in particle filtering
- Finding 12 (Quadratic Vaccination Fit Without Residual Diagnostics): C — no residual plots, normality check, or ACF of residuals for the quadratic model
- Finding 13 (AIC Table Search Reaches Upper Boundary Without Expanding): C — AR5/MA5 optimal at boundary but grid not expanded; ARIMA(4,1,4) selection not formally justified
- Finding 14 (No Diagnostics for ARIMA Models): C — no ACF/PACF of residuals, no Ljung-Box test, no normality checks for any fitted ARIMA
- Finding 15 (Live URL Data Downloads Create Reproducibility Risk): C — main code blocks pull from live GitHub URLs rather than local CSV files

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |
