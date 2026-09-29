## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: contradiction (Doug says no ESS monitoring was done; human says ESS was observed and often close to zero)
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (accumulator variable accumulates recoveries not cases): A — H += dN_IR is a fundamental specification error; human did not raise this
- Finding 2 (smoothed data fed to binomial measurement model): A — fractional rolling-average inputs to dbinom; human did not raise this specific concern
- Finding 3 (global search initialized from prior mif2 result): A — cooled starting state makes global search ineffective; human did not raise this
- Finding 4 (no quantitative benchmark comparison): A — ARMA and SEIR fitted to different data so log-likelihoods cannot be compared; human did not raise this
- Finding 5 (no profile likelihoods): A — parameter identifiability not assessed; human did not raise this
- Finding 6 (insufficient computational effort; SE too large): A — Np=1000, loglik.se values up to 2355; human did not raise this
- Finding 7 (mu_EI convergence to zero as model misspecification): A — implausible infinite latency not interpreted as misspecification; human did not raise this
- Finding 8 (no model diagnostics including ESS): F — Doug says ESS monitoring is absent; human says ESS was observed and was often close to zero (contradicts Human Issue #7)
- Finding 9 (rho fixed without justification or sensitivity analysis): A — reporting rate fixed at 0.1 with no sensitivity; human did not raise this
- Finding 10 (HP filter lambda inappropriate for daily data): C — lambda=100 designed for quarterly data; human did not raise this
- Finding 11 (ARMA on HP-filtered vs SEIR on smoothed: comparison invalid): C — models on incommensurable observation series; human did not raise this
- Finding 12 (data loaded from GitHub URL, not local file): C — reproducibility concern; human did not raise this
- Finding 13 (partrans omits logit for eta): C — eta can drift outside (0,1) during IF2; human did not raise this
- Finding 14 (no forecast from fitted SEIR model): C — no forward predictions generated; human did not raise this
- Finding 15 (initial conditions fixed, not estimated): C — E(0) and I(0) fixed with no sensitivity analysis; human did not raise this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 8 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 1 |
