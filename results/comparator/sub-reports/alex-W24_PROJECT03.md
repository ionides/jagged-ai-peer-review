## Alex

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: covered (matched by finding: "SARIMA notation inconsistency: B^12 in equations but period=4 in code")
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: missed
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: "Rate units mismatch: transition rates treated as per-week despite being described as per-day")
- Human Issue #12: covered (matched by finding: "Rate units mismatch: transition rates treated as per-week despite being described as per-day")

**Findings classification:**
- Finding 1 (Rate units mismatch): B — transition rates μ_EI and μ_IR treated as per-week but described as per-day, implying 10-week durations (matches Human Issues #11 and #12)
- Finding 2 (Implausible eta): A — initial susceptible fraction of 3–9% is biologically impossible for a novel pathogen
- Finding 3 (Global Search 1 worse than local search): A — non-monotone likelihood trajectory across searches never investigated
- Finding 4 (Profile CI from only 3 points): A — 95% CI for rho derived from only 3 filtered estimates above the chi-squared cutoff
- Finding 5 (Profile not anchored to MLE region): A — profile for rho uses local-search base model far from globally-optimized parameter region
- Finding 6 (Simulation uses manually chosen parameters): A — final simulation uses hand-picked values inconsistent with the stated MLE
- Finding 7 (Highly unstable b4): A — b4 ranges from 0.97 to 3042 across top solutions; effectively unidentified, never discussed
- Finding 8 (SEIR covers only 46.8% of data): C — model truncated at 2021, missing largest Japanese COVID waves
- Finding 9 (ARMA and SEIR never formally compared): C — no AIC/BIC comparison, no residual analysis for SEIR, no synthesis
- Finding 10 (SARIMA notation inconsistency B^12 vs period=4): D — equations use B^12 but code implements period=4 (matches Human Issue #2)
- Finding 11 (Non-convergence in local search): C — b4, eta, tau still varying at final iteration; not addressed before proceeding to global search
- Finding 12 (tau 12-fold increase never discussed): C — initial tau=0.05 grows to ~0.60 at MLE; sign of process misspecification, never interpreted
- Finding 13 (Misleading section title): C — "Not Based on Local Search" section still uses mifs_local[[1]] as base object
- Finding 14 (Low particle count): C — global searches use Np=1000 vs Np=10000 in profile; mixing precision levels
- Finding 15 (Weekly subsampling imprecise): C — every-7th-row sampling risks date misalignment with stated period start

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 1 |
| C (AI minor, human missed) | 7 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |
