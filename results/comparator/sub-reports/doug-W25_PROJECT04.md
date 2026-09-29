## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "ARIMA(5,1,5) near non-invertibility — several MA roots near/on unit circle, same underlying concern about roots suggesting poor model conditioning")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: missed
- Human Issue #12: covered (matched by finding: "ARIMA(5,1,5) near non-invertibility — questions why ARIMA(5,1,5) is preferred despite parsimony concerns, same underlying issue as human's 'not the lowest AIC' point")
- Human Issue #13: missed
- Human Issue #14: missed
- Human Issue #15: missed
- Human Issue #16: missed

**Findings classification:**
- Finding 1 (Pseudo-profiles): A — all profile likelihoods are pseudo-profiles; profiled parameter never fixed during optimization
- Finding 2 (Profile guess stratification): A — profile guess stratification groups by mu_IR regardless of which parameter is being profiled
- Finding 3 (Global search initialization): A — global search inherits cooling schedule from local search chain, undermining genuine global exploration
- Finding 4 (Accumulator variable H): A — H accumulates recoveries (dN_IR) rather than new infections, mismatching the observation data
- Finding 5 (Invalid LL/AIC comparison): A — log-likelihood and AIC comparison between ARIMA and SEIRS models is invalid due to different observation model distributions
- Finding 6 (mu_RS implausible): A — mu_RS fixed at biologically implausible value (200-week immunity) with no sensitivity analysis
- Finding 7 (No valid benchmark): A — no non-mechanistic statistical benchmark with matching observation model for the SEIRS model
- Finding 8 (Piecewise interval typo): C — third piecewise interval stated as [63, 119] but should be [97, 119]; documentation-only error
- Finding 9 (Time series frequency): C — ts objects created with frequency=7 instead of frequency=52, causing incorrect spectral/ACF lag labeling
- Finding 10 (Rho2 profile drops best row): C — highest log-likelihood row silently dropped without justification in rho2, eta profiles, and seirs_global2
- Finding 11 (Initial I(0)=1000): C — initial infected count fixed at 1000 without justification or sensitivity analysis
- Finding 12 (VAR LL approximation): C — VAR log-likelihood manually computed using approximation rather than directly from the model
- Finding 13 (ARIMA parsimony/invertibility): D — ARIMA(5,1,5) near non-invertibility with MA roots near unit circle; model selection ignores parsimony (matches Human Issues #3 and #12)
- Finding 14 (Figure cross-referencing errors): C — figure caption text not synchronized with chunk labels; numbering inconsistencies throughout
- Finding 15 (ChatGPT disclosure): C — AI use disclosure lacks specificity about which analyses or code sections used AI assistance

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 7 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 14 |
| F (Human-AI contradiction) | 0 |
