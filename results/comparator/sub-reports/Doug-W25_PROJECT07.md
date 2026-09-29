## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: covered (matched by finding: "Reporting rate rho fixed at biologically implausible values without justification")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "ACF analysis conclusion conflates oscillating pattern with non-stationarity")
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: covered (matched by finding: "SEIR population size N is implausibly small by two orders of magnitude")
- Human Issue #11: missed

**Findings classification:**
- Finding 1 (SEIR fitted on different dataset than SIRS): A — different dataset used for SEIR vs. SIRS, invalidating likelihood comparison
- Finding 2 (Global searches anchored to local-search mif2 chain): A — anti-pattern causing global search to not explore parameter space from fresh starts
- Finding 3 (SEIR accumulator tracks recoveries not new cases): A — H += dN_IR is semantic mismatch with reported case data
- Finding 4 (SEIR N implausibly small by two orders of magnitude): B — N=3.2 million vs. correct ~335 million (matches Human Issue #10)
- Finding 5 (Invalid comparison of SARIMA and POMP log-likelihoods): A — observation models are incompatible, making direct numeric comparison invalid
- Finding 6 (No profile likelihoods for any parameter): A — identifiability and confidence intervals cannot be assessed without profiles
- Finding 7 (Reporting rate rho fixed at biologically implausible values): B — rho=1e-7 is implausible for CDC travel surveillance and contradicted by SEIR estimate of ~0.9 (matches Human Issue #5)
- Finding 8 (SEIR local search uses nbrOfWorkers() instead of Nlocal): C — replicate count varies with execution environment
- Finding 9 (Post-local-search simulations hardcode k=10): C — optimized overdispersion parameter not used in post-search simulation blocks
- Finding 10 (No particle filter diagnostic for SEIR before local search): C — no ESS or conditional log-likelihood plot to verify filter health before IF2
- Finding 11 (SIRS run-level switch has 4 values for some parameters but only 3 levels): C — inconsistency in switch() definitions, Nglobal too small
- Finding 12 (SIRS model diagnostics beyond ESS): C — conditional log-likelihood panel not discussed
- Finding 13 (Seasonal amplitude c logit-transformed — inconsistency with upper bound of 1): C — logit upper bound issue in SEIR global box search
- Finding 14 (No out-of-sample or forecasting evaluation): C — models never used to generate forecasts or assess out-of-sample performance
- Finding 15 (ACF analysis conclusion conflates oscillating pattern with non-stationarity): D — oscillating ACF is characteristic of stationary seasonal ARMA, not non-stationarity (matches Human Issue #7)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 5 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 8 |
| F (Human-AI contradiction) | 0 |
