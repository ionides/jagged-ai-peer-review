## Doug

**Coverage record:**
- Human Issue #1: covered (matched by findings: "Global search initialized from prior IF2 result", "Profile likelihood: only nprof=2 starts per grid point", "Profile likelihood: phi not fixed in rw.sd / profile anti-pattern", "POMP fails to beat GARCH without acknowledging computational limitations", "Inadequate number of particles and iterations")
- Human Issue #2: missed
- Human Issue #3: missed

**Findings classification:**
- Finding 1 (Global search initialized from prior IF2 result): B — global search inherits cooling state of local chain, invalidating global coverage claim (matches Human Issue #1)
- Finding 2 (Profile likelihood: phi not fixed in rw.sd / profile also uses if1[[1]] anti-pattern): B — profile optimization also improperly initialized and suffers same computational deficiency as global search (matches Human Issue #1)
- Finding 3 (Profile likelihood: only nprof=2 starts per grid point): B — too few starts for reliable constrained optimization, making profile and any derived CI unreliable (matches Human Issue #1)
- Finding 4 (Incomplete sentence in conclusion — placeholder result): A — "phi = " with no value filled in; this placeholder finding is not raised by any human issue
- Finding 5 (POMP fails to beat GARCH without acknowledging computational limitations): B — AIC comparison ignores Monte Carlo noise and the unreliable global search initialization; computational shortcomings undermine the conclusion (matches Human Issue #1)
- Finding 6 (Inadequate number of particles and iterations): B — Np=2000, Nmif=50, profile Np=1000 insufficient for reliable inference; convergence not discussed (matches Human Issue #1)
- Finding 7 (No model diagnostics beyond visual convergence traces): A — no ESS plots, conditional log-likelihood, or simulated trajectory comparisons; not raised by any human issue
- Finding 8 (Profile likelihood plot: maximum phi value missing, confidence interval not reported): A — profile contributes no interpretable scientific content without bounds; not raised by any human issue
- Finding 9 (Stationarity claim without formal test): C — visual ACF inspection used to assert independence without ADF/KPSS; not raised by any human issue
- Finding 10 (GARCH AIC table starts at p=1, q=1; no p=0 or q=0 rows): C — simpler submodels excluded from AIC comparison; not raised by any human issue
- Finding 11 (QQ-plot explanation is superficial): C — heavy tails attributed to sample bias rather than inherent leptokurtosis; not raised by any human issue
- Finding 12 (Missing AIC comparison for POMP): C — comparison done by log-likelihood only without adjusting for parameter count difference; not raised by any human issue
- Finding 13 (Data description inconsistency — 570 vs 569): C — text states 570 observations but model is fitted to 569 returns; not raised by any human issue
- Finding 14 (rw.sd values identical for all regular parameters): C — uniform rw.sd=0.02 applied across parameters on very different scales; not raised by any human issue
- Finding 15 (No benchmark comparison against ARMA baseline): C — no ARMA on squared/absolute returns as simpler non-mechanistic comparison; not raised by any human issue

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 3 |
| B (AI major, human also found) | 5 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |
