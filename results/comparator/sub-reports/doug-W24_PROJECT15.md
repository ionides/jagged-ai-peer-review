## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Invalid LRT comparing ARMA and SEIRS models — non-nested, different observation models"; also matched by finding: "LRT df incorrect even ignoring non-comparability")

**Findings classification:**
- Major Issue 1 (Invalid LRT comparing ARMA and SEIRS): B — invalid likelihood ratio test comparing non-nested models evaluated under different observation models (matches Human Issue #5)
- Major Issue 2 (Accumulator variable tracks recoveries, not infections): A — C accumulates dN_IR rather than dN_EI, systematically misrepresenting the spillover process
- Major Issue 3 (Profile likelihood rho_CH drift): A — insufficient nprof and iterations render the profile curve and CI unreliable; CI reference maximum also drawn from wrong table
- Major Issue 4 (Global search initialized from prior mif2 object): A — inherited cooling schedule anchors global search near local solution
- Major Issue 5 (No convergence evidence for global search): A — no likelihood traces shown for global search; only two mif2 passes per replicate
- Major Issue 6 (dmeasure and rmeasure inconsistent scaling): A — dmeasure uses rho*C directly; rmeasure multiplies by 4, making likelihood and simulations inconsistent
- Major Issue 7 (LRT df incorrect): B — ARMA(1,4) parameter count misstated as 5 instead of 7, inflating LRT degrees of freedom (matches Human Issue #5)
- Minor: R_0 formula incorrect: C — uses Beta/mu_IR rather than the full SEIRS formula incorporating latent period survival
- Minor: Model diagram file missing: C — model.png referenced in text but not present; image does not render
- Minor: Fixed rho=1 not justified: C — near-complete surveillance assumed without citation or sensitivity analysis
- Minor: Profile CI reads from results not full parameter table: C — CI cutoff uses only profile search maximum, not global maximum
- Minor: Spectral analysis period calculation error: C — dimensional derivation of period formula is written incorrectly
- Minor: mu absent from rw.sd not acknowledged: C — camel birth/death rate fixed throughout but not noted in text
- Minor: Insufficient Np and Nmif: C — sensitivity of log-likelihoods to Np not assessed
- Minor: No model diagnostics beyond ESS: C — no conditional log-likelihood plot, filtering-distribution simulations, or residual diagnostics
- Minor: Pairs plot uses profile search results: C — global and profile scatter not compared

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 9 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 4 |
| F (Human-AI contradiction) | 0 |
