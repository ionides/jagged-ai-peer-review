## Charlie

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: covered (matched by finding: "Seasonal component detected by STL but not modeled in any POMP specification")
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "tau and amplitude lack parameter transformations in partrans — optimizer may propose values ≤ 0, handled only by hard clamp that may not enforce the stated [0,60] range")

**Findings classification:**
- Finding 1 (Hard-coded regime shift — data snooping): A — hard-coded windows for 2008 and 2020 constitute data snooping invalidating AIC comparison
- Finding 2 (No profile likelihoods or CIs): A — no profile likelihood computations for any parameter
- Finding 3 (Inconsistent GARCH specification): A — AIC table uses include.mean=F but final log-likelihood comparison uses include.mean=T
- Finding 4 (Daily data file missing): A — required data file for Figure 2 absent from submission
- Finding 5 (MC variability not propagated into AIC): A — stochastic log-likelihood estimates used in borderline ΔAIC ≈ 1.4 comparison without SE reporting
- Finding 6 (Global search from single local result): A — all global searches initialized from if1[[1]] rather than fresh base object
- Finding 7 (tau and amplitude lack transformations in partrans): D — optimizer may propose invalid tau values, clamp may not enforce stated [0,60] constraint (matches Human Issue #8)
- Finding 8 (No non-mechanistic benchmark): C — no IID or ARMA baseline for SV models
- Finding 9 (Seasonal component not modeled): D — STL reveals seasonality that is identified but not incorporated into any POMP model (matches Human Issue #3)
- Finding 10 (Base vs modified SV not formally compared): C — ~7 log-likelihood unit improvement described qualitatively without AIC table entry
- Finding 11 (epsilon_n not in model equations): C — epsilon_n mentioned in text but absent from equations (1)–(4)
- Finding 12 (No EDA section): C — report moves from introduction directly to model specification without dedicated EDA
- Finding 13 (Parameter perturbation sizes not discussed): C — rw.sd=1.0 for tau vs 0.02 for other parameters not justified
- Finding 14 (Conclusions overstate statistical evidence): C — ΔAIC ≈ 1.4 presented as supporting leverage hypothesis without formal test
- Finding 15 (fGarch log-likelihood normalization not verified): C — fGarch log-likelihood compared to POMP particle filter without checking normalization convention

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 0 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 2 |
| E (Human found, AI missed) | 6 |
| F (Human-AI contradiction) | 0 |
