## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "decompose() applied to daily log returns without justification")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: covered (matched by finding: "GARCH model selection selects worst-fitting model — tseries reports non-standard likelihood values and min() used instead of max()")
- Human Issue #7: covered (matched by finding: "no quantitative comparison between ARMA, GARCH, and POMP model likelihoods")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "no simulation-based model validation — ESS occasionally drops to single digits")
- Human Issue #11: covered (matched by finding: "references given as bare URLs rather than bibliographic citations")

**Findings classification:**
- Major Issue 1 (initial pfilter benchmark on simulated data): A — pfilter computed on sim1.filt (simulated data) rather than real AAPL returns, making the stated baseline meaningless
- Major Issue 2 (factual discrepancy on replicates/particles): A — text claims 20 replicates with 2000 particles; code uses 10 and 1000
- Major Issue 3 (GARCH model selection selects worst-fitting model): B — tseries reports non-standard likelihood values; min() used instead of max(), likely selecting the worst GARCH specification (matches Human Issue #6)
- Major Issue 4 (no profile likelihoods or confidence intervals): A — no profile likelihoods computed for any POMP parameter; sigma_eta and sigma_nu ranges are wide with no confidence bounds
- Major Issue 5 (no quantitative cross-model comparison): B — no log-likelihood or AIC comparison across ARMA, GARCH, and POMP; stated conclusion unsupported (matches Human Issue #7)
- Major Issue 6 (convergence failure acknowledged but not addressed): A — local search shows sigma_eta and H_0 still drifting at iteration 100 with no structural revision or increased computation
- Major Issue 7 (sigma_nu and sigma_eta near zero, scientific interpretation absent): A — near-zero estimates suggesting leverage collapse not discussed or tested against a reduced model
- Minor: no simulation-based model validation: D — ESS drops to single digits around time 400 and 800; no simulated trajectory overlays computed (matches Human Issue #10)
- Minor: decompose() applied to daily log returns without justification: D — log returns have no physical seasonality at frequency 253; component is plotted but never discussed (matches Human Issue #3)
- Minor: run_level=3 set but uses run_level=2 parameter values: C — Np=1000 and Nmif=100 at run_level=3 match run_level=2 defaults, not run_level=3 standard (Np=5000, Nmif=200)
- Minor: ARIMA section title but ARMA model fitted: C — d=0 in the fitted model; section heading is inconsistent with the specification
- Minor: references given as bare URLs rather than bibliographic citations: D — references [1]–[4] and [6] lack author, title, and date (matches Human Issue #11)
- Minor: acknowledgment of AI tool for LaTeX writing: C — reference [2] cites "CatGPT" for LaTeX; appropriateness under course policy should be clarified
- Minor: ARMA grid search excludes p=0 or q=0: C — pure AR or pure MA models not considered; best AIC from restricted grid may be suboptimal
- Minor: AIC comparison within basic GARCH grid omitted: C — log-likelihoods compared without complexity penalty; AIC would be more appropriate for model selection within the GARCH family

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 3 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
