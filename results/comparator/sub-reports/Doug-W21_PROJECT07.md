## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Population N treated as a free parameter on normalized data — a more principled approach would model normalization in the measurement model")
- Human Issue #4: covered (matched by finding: "Pseudo-profile likelihood: no dedicated profile IF2 search was ever executed — profiles are scatter plots from global search, not constrained optimizations")

**Findings classification:**
- Finding 1 (pseudo-profile likelihood): B — profile plots are not genuine profile likelihoods; they are scatter plots from the global search with no constrained optimization (matches Human Issue #4)
- Finding 2 (no non-mechanistic benchmark): A — SIRS model never compared against any non-mechanistic baseline
- Finding 3 (run_level=1 inadequate computation): A — analysis run at debugging level with Np=100, Nmif=10
- Finding 4 (misspecified negative binomial): A — dmeasure uses H as size parameter and rho as probability, not the standard dnbinom_mu parameterization
- Finding 5 (rho excluded from rw.sd): A — rho and N frozen at random starting points during IF2 without justification
- Finding 6 (H=5 initial condition not reset): A — H initialized to 5 but accumvars mechanism resets to 0 after each observation, creating inconsistency at t=0
- Finding 7 (N as free parameter on normalized data): B — N estimated from data normalized to max 100, making N and rho uninterpretable; suggests modeling normalization in measurement model (matches Human Issue #3)
- Finding 8 (benchmark at manual params, not MLE): C — pre-search log-likelihood evaluated at hand-chosen simulation parameters
- Finding 9 (eta profile never plotted): C — profile_design constructs grid over eta but no eta profile appears in Section 5.2
- Finding 10 (Nmif argument passed incorrectly): C — Nmif passed positionally without naming it in mif2() call
- Finding 11 (goodness-of-fit purely visual): C — no AIC, no log-likelihood ratio test, no conditional log-likelihood plot
- Finding 12 (H accumulates dN_SI vs. search frequency): C — relationship between new infections accumulator and search frequency not discussed
- Finding 13 (no convergence diagnostics): C — no trace plots or pairs plots; especially problematic given run_level=1
- Finding 14 (no model corroboration with external knowledge): C — parameter estimates not compared to epidemiological or social-media literature
- Finding 15 (notation inconsistency beta vs. Beta): C — mathematical section uses lowercase β but code and results use Beta

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 8 |
| D (AI minor, human also found) | 0 |
| E (Human found, AI missed) | 2 |
| F (Human-AI contradiction) | 0 |
