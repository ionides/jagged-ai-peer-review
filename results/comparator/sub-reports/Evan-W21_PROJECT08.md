## Evan

**Coverage record:**
- Human Issue #1: missed

**Findings classification:**
- 21.08.M1: A — "poor man's profile" CIs are statistically invalid; not a proper profile likelihood
- 21.08.M2: A — Heston boundary estimate for rho (0.9993) with no identifiability analysis
- 21.08.M3: A — undocumented log-variance reparameterization in Heston code vs. text equations
- 21.08.M4: A — t-HMM MLE in Section 6.2 text contradicts values shown in code
- 21.08.m1: C — global search for Gaussian HMM uses Np=200, too noisy for reliable ranking
- 21.08.m2: C — AR(1) HMM pairs plots show a0/b0 linear relationship indicating identifiability failure
- 21.08.m3: C — Gaussian/t observation model not justified for 97.5th-percentile order statistic data
- 21.08.m4: C — Heston conclusion overstates physical interpretation given identifiability concerns
- 21.08.m5: C — sigma_nu in Heston global search box is dead code (copy-paste artifact)
- 21.08.m6: C — AR(1) HMM filter diagnostics come from mif2 last iteration, not fixed-parameter pfilter

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 4 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 1 |
| F (Human-AI contradiction) | 0 |
