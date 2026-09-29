## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: contradiction (Alex's Finding 10 says ACF of squared residuals IS shown and uses it in critique; human says this plot is NOT shown)
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (Negative Heston parameter estimates): A — physically impossible negative v0 and sigma in Heston model dismissed without justification
- Finding 2 (No AIC/BIC for POMP models): A — likelihood comparison in Table 5 lacks penalty for model complexity
- Finding 3 (ARMA order inconsistency in code vs. prose): A — code labels say ARMA(1,1) while prose says ARMA(2,2)
- Finding 4 (Profile likelihood does not fix kappa in rw.sd): A — kappa omitted from rw.sd makes profile computation implicit rather than explicit
- Finding 5 (Single particle filter evaluation per replicate): A — stochastic likelihood estimates from a single pfilter run introduce Monte Carlo variance
- Finding 6 (Data extends beyond stated analysis period): A — data.csv contains observations through April 2025 but paper claims December 2024 cutoff
- Finding 7 (Regime trajectory from simulation, not filtered states): A — "Inferred Regime" plot uses simulate() rather than posterior filter output
- Finding 8 (No confidence intervals for profile likelihoods): A — profile likelihood plots lack likelihood-ratio-based CIs
- Finding 9 (Inconsistent figure numbering): C — Figure 3 label is reused, causing duplicate numbering
- Finding 10 (GARCH AIC table description): F — Alex says ACF of squared residuals is shown and uses it in critique; human says this plot is not shown (contradicts Human Issue #6)
- Finding 11 (Hardcoded log-likelihood values in Table 5): C — displayed values may not match runtime-computed values
- Finding 12 (No ESS diagnostics): C — effective sample size not reported despite claims of numerical stability
- Finding 13 (Course projects cited as published studies): C — prior student projects treated as peer-reviewed literature comparisons
- Finding 14 (Heston model lacks leverage effect): C — correlation between return and volatility innovations omitted despite discussion of asymmetry
- Finding 15 (Typos in section headers): C — "Stationairty" and "neccessary" misspellings remain despite stated use of ChatGPT for proofreading

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 1 |
