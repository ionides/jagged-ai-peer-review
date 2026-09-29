## Doug

**Coverage record:**
- Human Issue #1: missed
- Human Issue #2: missed
- Human Issue #3: missed
- Human Issue #4: missed
- Human Issue #5: missed
- Human Issue #6: missed
- Human Issue #7: missed
- Human Issue #8: covered (matched by finding: "SEIR model cannot mechanistically explain multiple epidemic waves without waning immunity")
- Human Issue #9: missed
- Human Issue #10: missed
- Human Issue #11: covered (matched by finding: "mu_EI and mu_IR fixed; unit conversion wrong — 0.1/week should be ~1.08/week"; also matched by finding: "Unit error in mu_EI and mu_IR initialization")
- Human Issue #12: covered (matched by finding: "mu_EI and mu_IR fixed; unit conversion wrong — 0.1/week should be ~1.08/week"; also matched by finding: "Unit error in mu_EI and mu_IR initialization")

**Findings classification:**
- Major 1 (Global searches worse than local; best MLE never identified): A — no human issue raised this
- Major 2 (Tau severely constrained in all searches except profile): A — no human issue raised this
- Major 3 (mu_EI and mu_IR fixed; unit conversion wrong, 0.1/week should be ~1.08/week): B — matches Human Issues #11 and #12
- Major 4 (No benchmark comparison between SEIR and SARIMA): A — no human issue raised this
- Major 5 (Profile CI for rho rests on only three grid points): A — no human issue raised this
- Major 6 (b4 and b2 unidentifiable at likelihood optimum): A — no human issue raised this
- Major 7 (No model diagnostics: ESS, conditional log-likelihoods, filtering checks): A — no human issue raised this
- Major 8 (SEIR cannot explain multiple waves without waning immunity): B — matches Human Issue #8
- Minor: Unit error in mu_EI and mu_IR initialization: D — matches Human Issues #11 and #12
- Minor: Inappropriate auto-installing of packages: C — no human issue raised this
- Minor: Duplicate library(tidyverse) call: C — no human issue raised this
- Minor: registerDoParallel() called twice with conflicting arguments: C — no human issue raised this
- Minor: global_search_2.rds referenced but not discussed in text: C — no human issue raised this
- Minor: rho CI interpretation questionable (reporting rate 66–93% implausibly high): C — no human issue raised this
- Minor: SARIMA seasonal period 4 weeks but spectral peak at ~4.3 weeks: C — no human issue raised this
- Minor: No convergence traces for global searches: C — no human issue raised this
- Minor: Measurement model description slightly inconsistent (rmeasure vs dmeasure): C — no human issue raised this
- Minor: Missing pomp package version: C — no human issue raised this
- Minor: No RNG seeds before second global search: C — no human issue raised this
- Minor: Data truncation at Dec 26 not Dec 31 as stated: C — no human issue raised this

**Counts:**

| Category | Count |
|----------|------:|
| A (AI major, human missed) | 6 |
| B (AI major, human also found) | 2 |
| C (AI minor, human missed) | 11 |
| D (AI minor, human also found) | 1 |
| E (Human found, AI missed) | 9 |
| F (Human-AI contradiction) | 0 |
