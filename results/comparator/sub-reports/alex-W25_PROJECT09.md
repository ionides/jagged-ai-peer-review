## Alex

**Coverage record:**
- Human Issue #1: covered (matched by findings: "dmeas and rmeas are inconsistent with each other" [Finding 4] and "attendance POMP model's dmeas never updated to include attendance covariate" [Finding 15])
- Human Issue #2: covered (matched by finding: "No likelihood-based model comparison; log-likelihood values are not reported or discussed" [Finding 7])
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed

**Findings classification:**
- Finding 1 (In-sample prediction as primary evaluation metric): A — no held-out test set; in-sample accuracy reported as predictive power
- Finding 2 (Accuracy from stochastic simulations vs. expected win probabilities): A — inconsistent operational definition of "prediction" across model types
- Finding 3 (Code bug: Model 3 simulates from nba_pomp, not nba_pomp_att): A — attendance model evaluation is silently reusing Model 1's object
- Finding 4 (dmeas and rmeas inconsistent with each other): B — different formulas for softmax vs. logistic with home-court adjustment (matches Human Issue #1)
- Finding 5 (sigma fixed and excluded from optimization): A — no justification for sigma = 5; truncates parameter space
- Finding 6 (Global search bounds poorly motivated and off-scale for home_court_avd): A — search interval [200, 250] is far from both initial guess and best-found value
- Finding 7 (No likelihood-based model comparison; log-likelihood values not reported): B — no LRT, AIC, or log-likelihood traces used for comparison (matches Human Issue #2)
- Finding 8 (ELO used as observed data for latent state): A — conflates deterministic post-hoc ELO with true latent team strength
- Finding 9 (t0 = 1 rather than t0 = 0; initialization indexing issues): C — one-step misalignment between POMP object and ELO covariate
- Finding 10 (BPM covariates for early games not formally documented or validated): C — boundary conditions of rolling BPM window not shown in code
- Finding 11 (No convergence diagnostics or particle filter variance assessments): C — IF2 traces shown but not analyzed; loglik.se never discussed
- Finding 12 (p_win treated as state variable rather than derived quantity): C — conceptual confusion; inflates state dimension without benefit
- Finding 13 (Hardcoded absolute file paths prevent reproducibility): C — paths tied to a specific local machine
- Finding 14 (Logistic regression in-sample baseline misleading): C — 64% accuracy is in-sample; comparison to POMP is not meaningful
- Finding 15 (Attendance POMP model's dmeas never updated to include attendance covariate): D — dmeas/rmeas inconsistency for attendance effect; same underlying issue as dmeas not matching rmeas (matches Human Issue #1)

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 6 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 5 |
| F (Human-AI contradiction) | 0 |
