## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "SIRV2 vaccination rate formula inconsistency — dt² term in latent process model equations")
- Human Issue #5: covered (matched by finding: "Grossly insufficient computational effort (run_level = 1 throughout)")
- Human Issue #6: missed

**Findings classification:**
- Major 1 (Accumulator H tracks recoveries not infections): A — accumulator variable semantic mismatch across all three models
- Major 2 (Global search initialized from previous mif2 result): A — cooling schedule inherited from local search, preventing genuine global coverage
- Major 3 (Prediction step uses initial guess not MLE): A — forecast uses manually specified params instead of params_maxlik
- Major 4 (Grossly insufficient computational effort): B — run_level=1 with Np=100 and Nmif=10 throughout (matches Human Issue #5)
- Major 5 (No non-mechanistic benchmark comparison): A — no ARMA or other baseline model compared
- Major 6 (Profile likelihood sigma CI cutoff commented out): A — geom_hline for CI boundary commented out so no formal CI is shown
- Major 7 (SIRV model 1 incorrect force of infection): A — uses V/N instead of I/N in V→I transition probability
- Major 8 (Forecast not conditioned on filtering distribution): A — forward simulation from t=0 initial conditions, not from filtering distribution at Day 87
- Minor: Log-likelihood single-evaluation in local search: C — logmeanexp applied to single pfilter value
- Minor: Possible negative initial compartment R: C — R could go negative if eta approaches 1 and V0 is large
- Minor: SIRV2 vaccination rate formula inconsistency: D — dt² term in latent process model equations is the error the human identified in SIRV2 coding (matches Human Issue #4)
- Minor: No effective sample size diagnostics: C — ESS not monitored or reported
- Minor: No corroboration with scientific knowledge: C — estimated parameter values not compared to epidemiological literature
- Minor: Goodness-of-fit assessed only visually: C — no formal AIC table or quantitative model comparison
- Minor: Population scaling unit inconsistency: C — units not explicitly stated in the text
- Minor: Typo in conclusion: C — "EXISTING!" draft artifact not removed
- Minor: References year discrepancy: C — "Masaaki, Ishikawa (2012)" vs. "2021" in text

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |
