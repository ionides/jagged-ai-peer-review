## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "ARMA applied to non-stationary series without transformation" and also by finding: "no stationarity analysis precedes ARMA modeling")
- Human Issue #5: contradiction (AI says I=1 is "a common convention... plausible but not justified"; human says I_0=1 is "wildly implausible")
- Human Issue #6: covered (matched by finding: "tau unused in dmeas/rmeas despite appearing in paramnames" and also by finding: "mu_EI and mu_IR fixed throughout pre-Delta local search")
- Human Issue #7: covered (matched by finding: "vaccination compartment initialization numerically negligible for Delta and Omicron")
- Human Issue #8: covered (matched by finding: "no comparison of log-likelihoods across segments or to any null model")
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (measurement model SD=mean, CV=1): A — measurement model uses sqrt(mean^2)=mean as SD; tau never appears in dmeas/rmeas
- Finding 2 (tau completely unused): B — tau declared and log-transformed but never used in dmeas, rmeas, or rprocess (matches Human Issue #6)
- Finding 3 (vaccination compartment initialization wrong): B — Delta V initialized to 0.3% of N instead of ~31%; Omicron V initialized to difference of two vaccination rates (~0.1%) instead of cumulative ~59% (matches Human Issue #7)
- Finding 4 (mu_EI and mu_IR fixed in pre-Delta local search): B — rw.sd for pre-Delta perturbs only Beta, rho, eta; mu_EI and mu_IR held fixed throughout (matches Human Issue #6)
- Finding 5 (pre-Delta global search uses only 10 starting points): A — 10 starts for the longest, most complex segment vs. 20 for Delta and Omicron
- Finding 6 (ARMA applied to non-stationary series without transformation): B — raw undifferenced daily counts spanning three waves fitted to ARMA with no log transformation or differencing (matches Human Issue #4)
- Finding 7 (no profile likelihood or confidence intervals): A — no profile likelihoods computed for any parameter across any of the three models
- Finding 8 (SE filter threshold of 8 too permissive for pre-Delta): C — loglik.se < 8 filter is far too loose; Omicron uses 0.5 by comparison
- Finding 9 (Delta local search Np=2000): C — only 5 replicates at Np=2000 for Delta evaluation, vs. Np=20000 for pre-Delta
- Finding 10 (no log-likelihood comparison across segments or to null): D — three POMP log-likelihoods reported in isolation with no per-observation normalization or ARMA benchmark comparison (matches Human Issue #8)
- Finding 11 (pairs plot mixes local and global search without labeling): C — bind_rows combines both search types with no color-coding or faceting
- Finding 12 (rmeas/dmeas inconsistency in SD formula): C — rmeas uses sqrt(rho*H) as SD; dmeas uses rho*H as SD
- Finding 13 (initial pfilter uses only Np=100): C — Np=100 too small for hundreds of observations; yields unreliable initial log-likelihood
- Finding 14 (no stationarity analysis precedes ARMA modeling): D — ARMA section jumps to AIC table without ACF/PACF, unit root tests, or stationarity discussion (matches Human Issue #4)
- Finding 15 (pre-Delta E=0, I=1 initial condition): F — AI calls I=1 "a common convention... plausible but not justified"; human says I_0=1 is "wildly implausible" (contradicts Human Issue #5)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 4 |
| C (AI minor, human missed) | 5 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 1 |
