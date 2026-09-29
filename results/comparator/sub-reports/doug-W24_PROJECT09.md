## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "ARIMA AIC table selects wrong model; ARMA(5,5) likely numerically unstable with near-unit-circle roots")
- Human Issue #6: covered (matched by finding: "Convergence not adequately demonstrated; loglik increases then decreases, not interpreted as misspecification")
- Human Issue #7: covered (matched by finding: "Convergence not adequately demonstrated; loglik increases then decreases, not interpreted as misspecification")
- Human Issue #8: covered (matched by finding: "Inconsistent notation — code uses sigma_eta but no equation reconciles it with the model description")
- Human Issue #9: missed

**Findings classification:**
- Major #1 (pomp-simdata-benchmark-error): A — initial pfilter run on simulated data, not real NASDAQ returns
- Major #2 (pomp-global-search-init-audit): A — global IF2 search initialized from previous mif2 result instead of base pomp object
- Major #3 (profile likelihood wrong parameter source): A — L.prof evaluates coef(if.box[[i]]) instead of coef(if.prof[[i]])
- Major #4 (invalid cross-model log-likelihood comparison): A — GARCH and POMP log-likelihoods compared without AIC/BIC adjustment for parameter count
- Major #5 (computationally unfair no-leverage comparison): A — no-leverage model run at drastically lower computational budget than full model
- Major #6 (convergence not adequately demonstrated): B — loglik increases then decreases not flagged as misspecification; global search convergence unverified (matches Human Issues #6 and #7)
- Major #7 (ARIMA AIC anomaly): B — ARMA(5,5) anomalously low AIC likely reflects numerical instability, near-unit-circle roots (matches Human Issue #5)
- Minor (periodogram frequency units): C — peak frequency not converted to interpretable cycles-per-year units
- Minor (text vs. output discrepancies): C — narrative log-likelihood values inconsistent with rendered output
- Minor (inconsistent notation/sigma_eta): D — code's sigma_eta not reconciled with model equation notation (matches Human Issue #8)
- Minor (sigma_nu converging to zero): C — sigma_nu near zero not flagged as potential unidentifiability of leverage state G
- Minor (missing CI for leverage comparison): C — no likelihood ratio test or confidence interval for leverage vs. no-leverage improvement
- Minor (timing.box assignment error): C — .system.time reference likely out of scope, reported timing unreliable
- Minor (no POMP model diagnostics): C — no ESS trace, conditional log-likelihood plot, or filtering-distribution simulation shown
- Minor (data mislabeling): C — title says NASDAQ 100 but data is NASDAQ Composite (^IXIC)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |
