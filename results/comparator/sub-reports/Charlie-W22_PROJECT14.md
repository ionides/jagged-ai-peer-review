## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: covered (matched by finding: "Breto model convergence failure interpreted incorrectly — declining LL in MIF2 is model misspecification, not merely numerical difficulty")
- Human Issue #5: covered (matched by finding: "Breto model convergence failure interpreted incorrectly — declining LL in MIF2 is model misspecification, not merely numerical difficulty")
- Human Issue #6: missed
- Human Issue #7: covered (matched by finding: "No simulation-based diagnostics / goodness-of-fit assessment — no plots comparing simulated trajectories to observed data")
- Human Issue #8: missed
- Human Issue #9: missed

**Findings classification:**
- Finding 1 (Heston code vs model equation mismatch): A — phi*sqrt(V) in code vs phi*V in stated equation; all Heston results invalid
- Finding 2 (Likelihood comparison mixing AIC and log-likelihood, possible different data lengths): A — cross-model likelihood comparison treated as valid despite scale and dataset inconsistencies
- Finding 3 (No profile likelihood analysis): A — no profile likelihoods, no parameter identifiability assessment, no confidence intervals
- Finding 4 (Breto convergence failure misinterpreted): B — declining LL in MIF2 is model misspecification not numerical noise (matches Human Issues #4 and #5)
- Finding 5 (6000-unit likelihood gap between Heston and Breto unexplained): A — implausible gap not remarked upon or investigated
- Finding 6 (Variable name error eth.sd_ivp vs eth_rw.sd_ivp): A — name collision bug; outer rw.sd object would fail if run
- Finding 7 (Breto global search phi range 0.97–0.99 not truly global): A — extremely narrow box does not meaningfully explore parameter space
- Finding 8 (AIC vs POMP likelihood comparison without justification): C — different package normalizations not verified before drawing conclusions
- Finding 9 (bake() called twice on same file): C — subtle reproducibility issue; mif2 objects and log-likelihoods may not correspond
- Finding 10 (No simulation-based diagnostics): D — no plots comparing simulated trajectories to observed data (matches Human Issue #7)
- Finding 11 (Heston covariate table set up but unused): C — covaryt loaded but not referenced in rproc C snippet; harmless but confusing
- Finding 12 (Heston local search: large ivp(0.2) for V_0, only 20 reps; pairs plot commented out): C — pairs plot for global search missing; local search diagnostic incomplete
- Finding 13 (Parameter interpretation absent): C — no comparison of fitted parameter values to literature or financial domain expectations
- Finding 14 (Missing references section): C — Section 6 labeled "Reference" but empty; citations only as inline footnotes
- Finding 15 (Confusing language about likelihood scale in Section 3.2): C — numerical claims about log-unit gaps are imprecise and should be stated with actual log-likelihood values

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
